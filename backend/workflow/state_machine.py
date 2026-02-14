from __future__ import annotations

from enum import Enum


class DocumentState(str, Enum):
    DRAFT = "Draft"
    REVIEW = "Review"
    APPROVED = "Approved"
    ARCHIVED = "Archived"


ALLOWED_TRANSITIONS: dict[DocumentState, set[DocumentState]] = {
    DocumentState.DRAFT: {DocumentState.REVIEW},
    DocumentState.REVIEW: {DocumentState.APPROVED, DocumentState.DRAFT},
    DocumentState.APPROVED: {DocumentState.ARCHIVED},
    DocumentState.ARCHIVED: set(),
}


class WorkflowError(Exception):
    pass


def ensure_transition_allowed(current: DocumentState, new: DocumentState) -> None:
    if new not in ALLOWED_TRANSITIONS[current]:
        raise WorkflowError(f"Transition not allowed: {current.value} -> {new.value}")
