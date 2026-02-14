from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError

from tests.support.foundation import AuthorizationError, EDMSTestFoundation, ValidationError


class TestPart11Compliance(unittest.TestCase):
    def setUp(self) -> None:
        self.foundation = EDMSTestFoundation()
        self.foundation.assign_role("approver.1", "approver")
        self.foundation.register_credentials("approver.1", "approved-secret")
        self.foundation.create_draft("DOC-011", "Batch Record", "author.1")
        self.foundation.add_version("DOC-011", "s3://doc/v1", "abc", "author.1")
        self.foundation.submit_review("DOC-011", "author.1")

    def test_signature_requires_reauthentication(self) -> None:
        with self.assertRaises(AuthorizationError):
            self.foundation.approve("DOC-011", "approver.1", "bad-secret", "Approved for use")

    def test_signature_meaning_is_captured(self) -> None:
        self.foundation.approve("DOC-011", "approver.1", "approved-secret", "Quality approval")
        entries = self.foundation.get_audit_entries("DOC-011")

        self.assertEqual("Quality approval", entries[-1].metadata["signature_meaning"])

    def test_audit_entries_are_immutable(self) -> None:
        self.foundation.approve("DOC-011", "approver.1", "approved-secret", "Quality approval")
        entry = self.foundation.get_audit_entries("DOC-011")[-1]

        with self.assertRaises(TypeError):
            entry.metadata["signature_meaning"] = "tampered"
        with self.assertRaises(FrozenInstanceError):
            entry.action = "tampered"

    def test_signature_meaning_cannot_be_empty(self) -> None:
        with self.assertRaises(ValidationError):
            self.foundation.approve("DOC-011", "approver.1", "approved-secret", "   ")


if __name__ == "__main__":
    unittest.main()
