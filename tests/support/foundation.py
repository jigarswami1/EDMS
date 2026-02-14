"""In-memory EDMS testing foundation used by unit and integration suites."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Any
from uuid import uuid4

from backend.domain.models import Document, DocumentState, DocumentVersion, PrintEvent, SignatureEvent


@dataclass(frozen=True, slots=True)
class AuditRecord:
    entry_id: str
    document_id: str
    actor_id: str
    action: str
    metadata: MappingProxyType[str, Any]
    occurred_at: datetime


@dataclass(slots=True)
class Task:
    task_id: str
    document_id: str
    assignee_id: str
    due_at: datetime
    status: str = "pending"


class AuthorizationError(PermissionError):
    """Raised when an actor attempts an operation without the required role."""


class ValidationError(ValueError):
    """Raised when an operation violates EDMS guardrails."""


class EDMSTestFoundation:
    """Simple in-memory EDMS domain simulation for test scenarios."""

    def __init__(self) -> None:
        self.documents: dict[str, Document] = {}
        self.versions: dict[str, list[DocumentVersion]] = {}
        self.superseded_versions: dict[str, str] = {}
        self.roles: dict[str, set[str]] = {}
        self.credentials: dict[str, str] = {}
        self.signatures: list[SignatureEvent] = []
        self.print_events: dict[str, PrintEvent] = {}
        self.print_copy_registry: set[tuple[str, str, int]] = set()
        self.audit: list[AuditRecord] = []
        self.tasks: list[Task] = []

    def assign_role(self, actor_id: str, role: str) -> None:
        self.roles.setdefault(actor_id, set()).add(role)

    def register_credentials(self, actor_id: str, secret: str) -> None:
        self.credentials[actor_id] = secret

    def create_draft(self, document_id: str, title: str, owner_id: str) -> Document:
        document = Document(document_id=document_id, title=title, owner_id=owner_id)
        self.documents[document_id] = document
        self._log(document_id, owner_id, "draft_created", {"state": document.state.value})
        return document

    def add_version(self, document_id: str, content_ref: str, checksum: str, created_by: str) -> DocumentVersion:
        versions = self.versions.setdefault(document_id, [])
        version = DocumentVersion(
            version_id=f"ver-{uuid4().hex[:8]}",
            document_id=document_id,
            version_number=len(versions) + 1,
            content_ref=content_ref,
            checksum=checksum,
            created_by=created_by,
        )
        if versions:
            self.superseded_versions[versions[-1].version_id] = version.version_id
        versions.append(version)
        self._log(
            document_id,
            created_by,
            "version_created",
            {"version_id": version.version_id, "version_number": version.version_number},
        )
        return version

    def submit_review(self, document_id: str, actor_id: str) -> None:
        self._transition(document_id, actor_id, DocumentState.DRAFT, DocumentState.IN_REVIEW, "review_submitted")

    def approve(self, document_id: str, actor_id: str, secret: str, signature_meaning: str) -> SignatureEvent:
        self._require_role(actor_id, "approver")
        if self.credentials.get(actor_id) != secret:
            raise AuthorizationError("reauthentication failed for approval signature")
        if not signature_meaning.strip():
            raise ValidationError("signature meaning is required")
        document = self.documents[document_id]
        if document.state != DocumentState.IN_REVIEW:
            raise ValidationError("approval only allowed from in_review")
        document.state = DocumentState.APPROVED
        event = SignatureEvent(
            event_id=f"sig-{uuid4().hex[:8]}",
            document_id=document_id,
            version_id=self.versions[document_id][-1].version_id,
            signer_id=actor_id,
            outcome="approved",
            signature_provider="local-test",
        )
        self.signatures.append(event)
        self._log(
            document_id,
            actor_id,
            "document_approved",
            {"signature_meaning": signature_meaning, "signature_id": event.event_id},
        )
        return event

    def make_effective(self, document_id: str, actor_id: str) -> None:
        self._transition(document_id, actor_id, DocumentState.APPROVED, DocumentState.EFFECTIVE, "made_effective")

    def mark_obsolete(self, document_id: str, actor_id: str) -> None:
        self._transition(document_id, actor_id, DocumentState.EFFECTIVE, DocumentState.ARCHIVED, "marked_obsolete")

    def request_print(self, document_id: str, version_id: str, requested_by: str, quantity: int) -> PrintEvent:
        event = PrintEvent(
            event_id=f"prt-{uuid4().hex[:8]}",
            document_id=document_id,
            version_id=version_id,
            requested_by=requested_by,
            quantity=quantity,
        )
        self.print_events[event.event_id] = event
        self._log(
            document_id,
            requested_by,
            "print_requested",
            {"print_event_id": event.event_id, "quantity": quantity},
        )
        return event

    def issue_print(self, print_event_id: str, actor_id: str, quantity: int) -> list[dict[str, Any]]:
        event = self.print_events[print_event_id]
        if event.reconciled:
            raise ValidationError("cannot issue copies after reconciliation")
        if event.issued_quantity + quantity > event.quantity:
            raise ValidationError("issued quantity exceeds request")
        issued_rows = []
        for _ in range(quantity):
            copy_number = event.issued_quantity + 1
            key = (event.document_id, event.version_id, copy_number)
            if key in self.print_copy_registry:
                raise ValidationError("duplicate copy number detected")
            self.print_copy_registry.add(key)
            event.issued_quantity += 1
            issued_rows.append(
                {
                    "copy_number": copy_number,
                    "watermark": {
                        "document_id": event.document_id,
                        "version_id": event.version_id,
                        "print_event_id": event.event_id,
                    },
                }
            )
        self._log(event.document_id, actor_id, "print_issued", {"issued_quantity": quantity})
        return issued_rows

    def reconcile_print(self, print_event_id: str, actor_id: str, returned_copy_numbers: list[int]) -> None:
        event = self.print_events[print_event_id]
        missing = sorted(set(range(1, event.issued_quantity + 1)).difference(returned_copy_numbers))
        if missing:
            raise ValidationError(f"missing issued copies during reconciliation: {missing}")
        event.reconciled = True
        self._log(event.document_id, actor_id, "print_reconciled", {"returned_copy_numbers": returned_copy_numbers})

    def create_task(self, document_id: str, assignee_id: str, due_at: datetime) -> Task:
        task = Task(task_id=f"tsk-{uuid4().hex[:8]}", document_id=document_id, assignee_id=assignee_id, due_at=due_at)
        self.tasks.append(task)
        return task

    def report_overdue_tasks(self, as_of: datetime) -> list[Task]:
        return [task for task in self.tasks if task.status == "pending" and task.due_at < as_of]

    def report_pending_approvals(self) -> list[Document]:
        return [document for document in self.documents.values() if document.state == DocumentState.IN_REVIEW]

    def export_audit_for_inspection(self, document_id: str) -> list[dict[str, Any]]:
        rows = [entry for entry in self.audit if entry.document_id == document_id]
        rows.sort(key=lambda entry: entry.occurred_at)
        return [
            {
                "entry_id": entry.entry_id,
                "occurred_at": entry.occurred_at.isoformat(),
                "actor_id": entry.actor_id,
                "action": entry.action,
                "metadata": dict(entry.metadata),
            }
            for entry in rows
        ]

    def get_audit_entries(self, document_id: str) -> tuple[AuditRecord, ...]:
        return tuple(entry for entry in self.audit if entry.document_id == document_id)

    def _transition(
        self,
        document_id: str,
        actor_id: str,
        expected: DocumentState,
        new_state: DocumentState,
        action: str,
    ) -> None:
        document = self.documents[document_id]
        if document.state != expected:
            raise ValidationError(f"expected state {expected.value}, got {document.state.value}")
        document.state = new_state
        self._log(document_id, actor_id, action, {"state": new_state.value})

    def _require_role(self, actor_id: str, role: str) -> None:
        if role not in self.roles.get(actor_id, set()):
            raise AuthorizationError(f"{actor_id} lacks required role {role}")

    def _log(self, document_id: str, actor_id: str, action: str, metadata: dict[str, Any]) -> None:
        immutable_metadata = MappingProxyType(dict(metadata))
        self.audit.append(
            AuditRecord(
                entry_id=f"aud-{uuid4().hex[:8]}",
                document_id=document_id,
                actor_id=actor_id,
                action=action,
                metadata=immutable_metadata,
                occurred_at=datetime.utcnow(),
            )
        )
