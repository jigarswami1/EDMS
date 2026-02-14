from __future__ import annotations

import hashlib

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.audit.service import log_event
from backend.auth.models import Role
from backend.auth.rbac import PermissionDenied
from backend.documents.models import Document, DocumentVersion
from backend.documents.service import transition_document
from backend.signatures.models import ElectronicSignature
from backend.workflow.state_machine import DocumentState


class SignatureError(Exception):
    pass


def sign_and_approve(session: Session, doc_number: str, signer_username: str, meaning: str, actor_role: Role) -> ElectronicSignature:
    if actor_role not in {Role.APPROVER, Role.ADMIN}:
        raise PermissionDenied("Only Approver/Admin can sign")
    if not meaning.strip():
        raise SignatureError("Signature meaning is required")
    document = session.scalar(select(Document).where(Document.doc_number == doc_number))
    if not document:
        raise SignatureError("Document not found")
    latest_version = session.scalar(
        select(DocumentVersion)
        .where(DocumentVersion.document_id == document.id)
        .order_by(DocumentVersion.version_no.desc())
    )
    if not latest_version:
        raise SignatureError("No version available for signature")

    signature_hash = hashlib.sha256(
        f"{doc_number}|{latest_version.id}|{signer_username}|{meaning}".encode("utf-8")
    ).hexdigest()
    signature = ElectronicSignature(
        document_id=document.id,
        version_id=latest_version.id,
        signer_username=signer_username,
        meaning=meaning,
        signature_hash=signature_hash,
    )
    session.add(signature)
    session.flush()

    transition_document(session, doc_number, DocumentState.APPROVED, signer_username, actor_role)
    log_event(
        session,
        "DOCUMENT_SIGNED",
        signer_username,
        {"signature_hash": signature_hash, "meaning": meaning},
        "document",
        doc_number,
    )
    return signature
