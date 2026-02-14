from __future__ import annotations

import pytest

from backend.auth.models import Role
from backend.auth.rbac import PermissionDenied
from backend.documents.service import add_version, create_document, transition_document
from backend.workflow.state_machine import DocumentState, WorkflowError


def test_workflow_and_role_enforcement(db_session):
    create_document(db_session, "DOC-1", "SOP", "author1")
    add_version(db_session, "DOC-1", "content-v1", "author1", Role.AUTHOR)
    transition_document(db_session, "DOC-1", DocumentState.REVIEW, "author1", Role.AUTHOR)

    with pytest.raises(PermissionDenied):
        transition_document(db_session, "DOC-1", DocumentState.APPROVED, "reviewer1", Role.REVIEWER)


def test_document_lock_after_approval(db_session):
    create_document(db_session, "DOC-2", "BMR", "author1")
    add_version(db_session, "DOC-2", "content-v1", "author1", Role.AUTHOR)
    transition_document(db_session, "DOC-2", DocumentState.REVIEW, "author1", Role.AUTHOR)
    transition_document(db_session, "DOC-2", DocumentState.APPROVED, "approver1", Role.APPROVER)

    with pytest.raises(Exception):
        add_version(db_session, "DOC-2", "content-v2", "author1", Role.AUTHOR)

    with pytest.raises(WorkflowError):
        transition_document(db_session, "DOC-2", DocumentState.DRAFT, "admin1", Role.ADMIN)
