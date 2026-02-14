from __future__ import annotations

import hashlib

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.audit.service import log_event
from backend.auth.models import Role
from backend.auth.rbac import PermissionDenied
from backend.documents.models import Document, DocumentVersion
from backend.workflow.state_machine import DocumentState, ensure_transition_allowed


class DocumentError(Exception):
    pass


def create_document(session: Session, doc_number: str, title: str, owner_username: str) -> Document:
    document = Document(doc_number=doc_number, title=title, owner_username=owner_username)
    session.add(document)
    session.flush()
    log_event(session, "DOCUMENT_CREATE", owner_username, {"title": title}, "document", doc_number)
    return document


def add_version(session: Session, doc_number: str, content: str, created_by: str, actor_role: Role) -> DocumentVersion:
    if actor_role not in {Role.AUTHOR, Role.ADMIN}:
        raise PermissionDenied("Only Author/Admin can version a document")
    document = session.scalar(select(Document).where(Document.doc_number == doc_number))
    if not document:
        raise DocumentError("Document not found")
    if document.locked:
        raise DocumentError("Document is locked after approval")
    checksum = hashlib.sha256(content.encode("utf-8")).hexdigest()
    current_max = session.scalars(select(DocumentVersion).where(DocumentVersion.document_id == document.id)).all()
    version_no = len(current_max) + 1
    version = DocumentVersion(
        document_id=document.id,
        version_no=version_no,
        content=content,
        checksum=checksum,
        created_by=created_by,
    )
    session.add(version)
    session.flush()
    log_event(session, "VERSION_ADD", created_by, {"version_no": version_no, "checksum": checksum}, "document", doc_number)
    return version


def transition_document(session: Session, doc_number: str, target_state: DocumentState, actor: str, actor_role: Role) -> Document:
    document = session.scalar(select(Document).where(Document.doc_number == doc_number))
    if not document:
        raise DocumentError("Document not found")
    if document.locked and target_state != DocumentState.ARCHIVED:
        raise DocumentError("Document is locked")
    if target_state == DocumentState.REVIEW and actor_role not in {Role.AUTHOR, Role.ADMIN}:
        raise PermissionDenied("Only Author/Admin can submit to review")
    if target_state == DocumentState.APPROVED and actor_role not in {Role.APPROVER, Role.ADMIN}:
        raise PermissionDenied("Only Approver/Admin can approve")
    ensure_transition_allowed(document.state, target_state)
    old_state = document.state
    document.state = target_state
    if target_state == DocumentState.APPROVED:
        document.locked = True
    log_event(session, "STATE_CHANGE", actor, {"from": old_state.value, "to": target_state.value}, "document", doc_number)
    return document
