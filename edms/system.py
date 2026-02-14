from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

from .models import (
    AuditEvent,
    ControlledPrint,
    Document,
    DocumentState,
    DocumentVersion,
    Role,
    Signature,
    User,
    new_identifier,
    utc_now,
)


class EDMSPermissionError(PermissionError):
    """Raised when a user does not have required role permissions."""


class EDMSStateError(ValueError):
    """Raised when a workflow action is attempted in an invalid state."""


@dataclass
class EDMS:
    documents: Dict[str, Document] = field(default_factory=dict)

    def _assert_role(self, user: User, allowed_roles: Iterable[Role]) -> None:
        if user.role not in set(allowed_roles):
            raise EDMSPermissionError(
                f"User role '{user.role.value}' is not authorized for this action."
            )

    def _assert_password(self, user: User, password_confirmation: str) -> None:
        if user.password != password_confirmation:
            raise EDMSPermissionError("Signature re-authentication failed.")

    def create_document(
        self,
        user: User,
        title: str,
        document_type: str,
        department: str,
        product_site: str,
        content: str,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Document:
        self._assert_role(user, [Role.AUTHOR, Role.QA_ADMIN, Role.SYSTEM_ADMIN])

        doc_id = new_identifier("DOC")
        version = DocumentVersion(
            version_id="v1.0",
            major=1,
            minor=0,
            content=content,
            metadata=metadata or {},
            state=DocumentState.DRAFT,
        )
        version.audit_trail.append(
            AuditEvent("document_created", user.user_id, utc_now(), {"version": "v1.0"})
        )

        document = Document(
            document_id=doc_id,
            title=title,
            document_type=document_type,
            department=department,
            product_site=product_site,
            versions=[version],
        )
        self.documents[doc_id] = document
        return document

    def submit_for_review(self, user: User, document_id: str, comment: str) -> None:
        self._assert_role(user, [Role.AUTHOR, Role.QA_ADMIN, Role.SYSTEM_ADMIN])
        version = self.documents[document_id].current_version()
        if version.state != DocumentState.DRAFT:
            raise EDMSStateError("Only draft documents can be submitted for review.")
        version.state = DocumentState.REVIEW
        version.audit_trail.append(
            AuditEvent("submitted_for_review", user.user_id, utc_now(), {"comment": comment})
        )

    def complete_review(self, user: User, document_id: str, review_comment: str) -> None:
        self._assert_role(user, [Role.REVIEWER, Role.QA_ADMIN, Role.SYSTEM_ADMIN])
        version = self.documents[document_id].current_version()
        if version.state != DocumentState.REVIEW:
            raise EDMSStateError("Only documents in review can complete review.")

        version.signatures.append(
            Signature(
                signed_by=user.user_id,
                meaning="reviewed",
                comment=review_comment,
                timestamp=utc_now(),
            )
        )
        version.state = DocumentState.APPROVAL
        version.audit_trail.append(
            AuditEvent(
                "review_completed",
                user.user_id,
                utc_now(),
                {"comment": review_comment},
            )
        )

    def approve_document(
        self,
        user: User,
        document_id: str,
        comment: str,
        password_confirmation: str,
    ) -> None:
        self._assert_role(user, [Role.APPROVER, Role.QA_ADMIN, Role.SYSTEM_ADMIN])
        self._assert_password(user, password_confirmation)

        version = self.documents[document_id].current_version()
        if version.state != DocumentState.APPROVAL:
            raise EDMSStateError("Only documents in approval can be approved.")

        version.signatures.append(
            Signature(
                signed_by=user.user_id,
                meaning="approved",
                comment=comment,
                timestamp=utc_now(),
            )
        )
        version.state = DocumentState.EFFECTIVE
        version.audit_trail.append(
            AuditEvent("approved", user.user_id, utc_now(), {"comment": comment})
        )

        self._supersede_previous_effective_versions(document_id, version.version_id, user.user_id)

    def _supersede_previous_effective_versions(
        self, document_id: str, current_version_id: str, actor: str
    ) -> None:
        document = self.documents[document_id]
        for version in document.versions:
            if version.version_id != current_version_id and version.state == DocumentState.EFFECTIVE:
                version.state = DocumentState.OBSOLETE
                version.audit_trail.append(
                    AuditEvent(
                        "superseded",
                        actor,
                        utc_now(),
                        {"superseded_by": current_version_id},
                    )
                )

    def revise_document(
        self,
        user: User,
        document_id: str,
        content: str,
        metadata: Optional[Dict[str, str]] = None,
    ) -> DocumentVersion:
        self._assert_role(user, [Role.AUTHOR, Role.QA_ADMIN, Role.SYSTEM_ADMIN])
        document = self.documents[document_id]
        latest = document.current_version()

        next_minor = latest.minor + 1
        version_id = f"v{latest.major}.{next_minor}"
        revision = DocumentVersion(
            version_id=version_id,
            major=latest.major,
            minor=next_minor,
            content=content,
            metadata=metadata or latest.metadata.copy(),
            state=DocumentState.DRAFT,
        )
        revision.audit_trail.append(
            AuditEvent(
                "revision_created",
                user.user_id,
                utc_now(),
                {"based_on": latest.version_id},
            )
        )
        document.versions.append(revision)
        return revision

    def _effective_version(self, document: Document) -> DocumentVersion:
        for version in reversed(document.versions):
            if version.state == DocumentState.EFFECTIVE:
                return version
        raise EDMSStateError("Document has no effective version.")

    def controlled_print(self, user: User, document_id: str) -> ControlledPrint:
        self._assert_role(user, [Role.PRINT_CUSTODIAN, Role.QA_ADMIN, Role.SYSTEM_ADMIN])
        document = self.documents[document_id]
        version = self._effective_version(document)

        copy_number = len(version.controlled_prints) + 1
        print_copy = ControlledPrint(
            print_id=new_identifier("PRINT"),
            copy_number=copy_number,
            printed_by=user.user_id,
            printed_at=utc_now(),
            source_version=version.version_id,
        )
        version.controlled_prints.append(print_copy)
        version.audit_trail.append(
            AuditEvent(
                "controlled_print_issued",
                user.user_id,
                utc_now(),
                {
                    "print_id": print_copy.print_id,
                    "copy_number": str(copy_number),
                },
            )
        )
        return print_copy

    def reconcile_print_copy(
        self, user: User, document_id: str, print_id: str, note: str
    ) -> ControlledPrint:
        self._assert_role(user, [Role.PRINT_CUSTODIAN, Role.QA_ADMIN, Role.SYSTEM_ADMIN])
        document = self.documents[document_id]
        for version in reversed(document.versions):
            for print_copy in version.controlled_prints:
                if print_copy.print_id == print_id:
                    print_copy.reconciled = True
                    print_copy.reconciliation_note = note
                    version.audit_trail.append(
                        AuditEvent(
                            "controlled_print_reconciled",
                            user.user_id,
                            utc_now(),
                            {"print_id": print_id, "note": note},
                        )
                    )
                    return print_copy
        raise EDMSStateError(f"Print copy '{print_id}' was not found.")

    def list_effective_documents(self) -> List[Document]:
        return [
            doc
            for doc in self.documents.values()
            if any(version.state == DocumentState.EFFECTIVE for version in doc.versions)
        ]
