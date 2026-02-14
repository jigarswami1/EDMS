from __future__ import annotations

import unittest

from backend.domain.models import DocumentState
from backend.workflows import assert_transition_allowed


class TestWorkflowStateMachine(unittest.TestCase):
    def test_allows_valid_transitions(self) -> None:
        assert_transition_allowed(
            DocumentState.DRAFT, DocumentState.IN_REVIEW
        )
        assert_transition_allowed(
            DocumentState.IN_REVIEW, DocumentState.APPROVED
        )
        assert_transition_allowed(
            DocumentState.APPROVED, DocumentState.EFFECTIVE
        )
        assert_transition_allowed(
            DocumentState.EFFECTIVE, DocumentState.ARCHIVED
        )

    def test_rejects_invalid_transition(self) -> None:
        with self.assertRaises(ValueError):
            assert_transition_allowed(
                DocumentState.DRAFT, DocumentState.EFFECTIVE
            )

    def test_rejected_document_can_return_to_draft(self) -> None:
        assert_transition_allowed(DocumentState.REJECTED, DocumentState.DRAFT)


if __name__ == "__main__":
    unittest.main()