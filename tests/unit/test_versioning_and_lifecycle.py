from __future__ import annotations

import unittest

from backend.domain.models import DocumentState
from tests.support.foundation import AuthorizationError, EDMSTestFoundation, ValidationError


class TestVersioningAndLifecycle(unittest.TestCase):
    def setUp(self) -> None:
        self.foundation = EDMSTestFoundation()
        self.foundation.assign_role("qa.approver", "approver")
        self.foundation.register_credentials("qa.approver", "correct-horse")
        self.foundation.create_draft("DOC-001", "SOP Sterility", "author.1")

    def test_version_numbers_increment_and_supersession_links_previous(self) -> None:
        first = self.foundation.add_version("DOC-001", "s3://doc/v1", "abc", "author.1")
        second = self.foundation.add_version("DOC-001", "s3://doc/v2", "def", "author.1")

        self.assertEqual(1, first.version_number)
        self.assertEqual(2, second.version_number)
        self.assertEqual(second.version_id, self.foundation.superseded_versions[first.version_id])

    def test_state_transition_happy_path(self) -> None:
        self.foundation.add_version("DOC-001", "s3://doc/v1", "abc", "author.1")

        self.foundation.submit_review("DOC-001", "author.1")
        self.foundation.approve("DOC-001", "qa.approver", "correct-horse", "I approve this for release")
        self.foundation.make_effective("DOC-001", "qa.approver")
        self.foundation.mark_obsolete("DOC-001", "qa.approver")

        self.assertEqual(DocumentState.ARCHIVED, self.foundation.documents["DOC-001"].state)

    def test_invalid_state_transition_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            self.foundation.make_effective("DOC-001", "qa.approver")

    def test_authority_checks_require_approver_role(self) -> None:
        self.foundation.add_version("DOC-001", "s3://doc/v1", "abc", "author.1")
        self.foundation.submit_review("DOC-001", "author.1")

        with self.assertRaises(AuthorizationError):
            self.foundation.approve("DOC-001", "author.1", "wrong", "approved")


if __name__ == "__main__":
    unittest.main()
