from __future__ import annotations

from sqlalchemy import select

from backend.auth.models import Role
from backend.documents.models import Document
from backend.documents.service import add_version, create_document, transition_document
from backend.signatures.models import ElectronicSignature
from backend.signatures.service import sign_and_approve
from backend.workflow.state_machine import DocumentState


def test_signature_binding_and_lock(db_session):
    create_document(db_session, "DOC-4", "Spec", "author1")
    version = add_version(db_session, "DOC-4", "content", "author1", Role.AUTHOR)
    transition_document(db_session, "DOC-4", DocumentState.REVIEW, "author1", Role.AUTHOR)
    sig = sign_and_approve(db_session, "DOC-4", "approver1", "QA Approval", Role.APPROVER)

    persisted = db_session.scalar(select(ElectronicSignature).where(ElectronicSignature.id == sig.id))
    doc = db_session.scalar(select(Document).where(Document.doc_number == "DOC-4"))
    assert persisted.version_id == version.id
    assert doc.locked is True
