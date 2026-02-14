from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from .models import AuditEvent, Document, DocumentState, Role, User, utc_now


class EDMSError(Exception):
    """Base error for EDMS starter kit."""


class EDMSPermissionError(EDMSError):
    """Raised when a user tries an action without the required role."""


class EDMSStateError(EDMSError):
    """Raised when a workflow transition is invalid."""


@dataclass
class EDMS:
    documents: Dict[str, Document] = field(default_factory=dict)

    def _assert_role(self, user: User, required_role: Role) -> None:
        if user.role != required_role:
            raise EDMSPermissionError(
                f"Action requires role '{required_role.value}', but got '{user.role.value}'."
            )

    def _add_event(self, document: Document, action: str, actor: User, comment: str = "") -> None:
        document.audit_trail.append(
            AuditEvent(action=action, actor=actor.user_id, timestamp=utc_now(), comment=comment)
        )

    def create_document(self, user: User, document_id: str, title: str, content: str) -> Document:
        self._assert_role(user, Role.AUTHOR)
        if document_id in self.documents:
            raise ValueError(f"Document ID '{document_id}' already exists.")

        document = Document(document_id=document_id, title=title, content=content)
        self._add_event(document, action="created", actor=user, comment="Initial draft created")
        self.documents[document_id] = document
        return document

    def submit_for_review(self, user: User, document_id: str, comment: str = "") -> None:
        self._assert_role(user, Role.AUTHOR)
        document = self.documents[document_id]

        if document.state != DocumentState.DRAFT:
            raise EDMSStateError("Only draft documents can be submitted for review.")

        document.state = DocumentState.REVIEW
        self._add_event(document, action="submitted_for_review", actor=user, comment=comment)

    def approve(self, user: User, document_id: str, comment: str = "") -> None:
        self._assert_role(user, Role.APPROVER)
        document = self.documents[document_id]

        if document.state != DocumentState.REVIEW:
            raise EDMSStateError("Only documents in review can be approved.")

        document.state = DocumentState.APPROVED
        self._add_event(document, action="approved", actor=user, comment=comment)

    def list_approved(self) -> list[Document]:
        return [doc for doc in self.documents.values() if doc.state == DocumentState.APPROVED]
