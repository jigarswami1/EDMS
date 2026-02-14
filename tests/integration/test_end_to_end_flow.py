from __future__ import annotations

import unittest

from backend.domain.models import DocumentState
from tests.support.foundation import EDMSTestFoundation


class TestEndToEndLifecycle(unittest.TestCase):
    def test_draft_review_approval_effective_obsolete_flow(self) -> None:
        foundation = EDMSTestFoundation()
        foundation.assign_role("qa.approver", "approver")
        foundation.register_credentials("qa.approver", "approve-me")

        foundation.create_draft("DOC-E2E", "Validation Master Plan", "author.1")
        foundation.add_version("DOC-E2E", "s3://doc/v1", "abc", "author.1")
        foundation.submit_review("DOC-E2E", "author.1")
        foundation.approve("DOC-E2E", "qa.approver", "approve-me", "Approved for effective use")
        foundation.make_effective("DOC-E2E", "qa.approver")
        foundation.mark_obsolete("DOC-E2E", "qa.approver")

        self.assertEqual(DocumentState.ARCHIVED, foundation.documents["DOC-E2E"].state)
        action_names = [entry.action for entry in foundation.get_audit_entries("DOC-E2E")]
        self.assertEqual(
            [
                "draft_created",
                "version_created",
                "review_submitted",
                "document_approved",
                "made_effective",
                "marked_obsolete",
            ],
            action_names,
        )


if __name__ == "__main__":
    unittest.main()
