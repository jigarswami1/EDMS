from __future__ import annotations

import pytest
from sqlalchemy import select

from backend.audit.models import AuditEvent
from backend.auth.models import Role
from backend.documents.service import add_version, create_document


def test_audit_trail_append_only_and_utc(db_session):
    create_document(db_session, "DOC-3", "Policy", "author1")
    add_version(db_session, "DOC-3", "hello", "author1", Role.AUTHOR)
    events = db_session.scalars(select(AuditEvent).order_by(AuditEvent.id)).all()
    assert len(events) >= 2
    assert all(evt.created_at.tzinfo is not None for evt in events)

    event = events[0]
    event.event_type = "TAMPERED"
    with pytest.raises(ValueError):
        db_session.flush()
