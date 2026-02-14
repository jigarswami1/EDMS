from __future__ import annotations

import pytest
from sqlalchemy import select

from backend.audit.models import AuditEvent
from backend.auth.models import Role
from backend.auth.service import AuthError, create_user, login, validate_token


def test_authentication_password_policy_and_session_control(db_session):
    create_user(db_session, "author1", "ComplexPass123", Role.AUTHOR)
    token = login(db_session, "author1", "ComplexPass123")
    claims = validate_token(db_session, token)
    assert claims["sub"] == "author1"

    with pytest.raises(AuthError):
        login(db_session, "author1", "wrong")

    events = db_session.scalars(select(AuditEvent).where(AuditEvent.event_type.in_(["LOGIN_SUCCESS", "LOGIN_FAILED"]))).all()
    assert len(events) >= 2
