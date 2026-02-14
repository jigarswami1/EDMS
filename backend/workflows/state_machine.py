"""Document lifecycle transition guards for EDMS workflows."""

from __future__ import annotations

from backend.domain.models import DocumentState


ALLOWED_TRANSITIONS: dict[DocumentState, set[DocumentState]] = {
    DocumentState.DRAFT: {DocumentState.IN_REVIEW},
    DocumentState.IN_REVIEW: {DocumentState.APPROVED, DocumentState.REJECTED},
    DocumentState.REJECTED: {DocumentState.DRAFT},
    DocumentState.APPROVED: {DocumentState.EFFECTIVE},
    DocumentState.EFFECTIVE: {DocumentState.ARCHIVED},
    DocumentState.ARCHIVED: set(),
}


def assert_transition_allowed(current: DocumentState, target: DocumentState) -> None:
    """Validate a lifecycle transition.

    Raises:
        ValueError: When a transition is outside the configured EDMS lifecycle.
    """

    allowed_targets = ALLOWED_TRANSITIONS.get(current)
    if allowed_targets is None:
        raise ValueError(f"Unknown document state: {current!r}")
    if target not in allowed_targets:
        raise ValueError(f"Transition not allowed: {current.value} -> {target.value}")
