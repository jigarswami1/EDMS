from __future__ import annotations

import hashlib
from sqlalchemy import select

from backend.auth.models import Role
from backend.documents.models import DocumentVersion
from backend.documents.service import add_version, create_document


def test_data_integrity_alcoa_plus(db_session):
    create_document(db_session, "DOC-5", "WI", "author1")
    content = "authoritative content"
    version = add_version(db_session, "DOC-5", content, "author1", Role.AUTHOR)
    persisted = db_session.scalar(select(DocumentVersion).where(DocumentVersion.id == version.id))

    assert persisted.created_by == "author1"
    assert persisted.checksum == hashlib.sha256(content.encode("utf-8")).hexdigest()
    assert persisted.created_at.tzinfo is not None
