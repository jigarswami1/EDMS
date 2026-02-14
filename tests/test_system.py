import unittest

from edms.models import DocumentState, Role, User
from edms.system import EDMS, EDMSPermissionError, EDMSStateError


class EDMSTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.system = EDMS()
        self.author = User(user_id="u-author", full_name="Author User", role=Role.AUTHOR)
        self.approver = User(user_id="u-approver", full_name="Approver User", role=Role.APPROVER)
        self.reviewer = User(user_id="u-reviewer", full_name="Reviewer User", role=Role.REVIEWER)

    def test_happy_path_create_submit_approve(self) -> None:
        doc = self.system.create_document(
            user=self.author,
            document_id="DOC-001",
            title="SOP Cleaning",
            content="Step 1...",
        )
        self.system.submit_for_review(self.author, "DOC-001", "Please review")
        self.system.approve(self.approver, "DOC-001", "Approved for use")

        self.assertEqual(DocumentState.APPROVED, doc.state)
        self.assertEqual(3, len(doc.audit_trail))
        self.assertEqual(["DOC-001"], [d.document_id for d in self.system.list_approved()])

    def test_only_author_can_create(self) -> None:
        with self.assertRaises(EDMSPermissionError):
            self.system.create_document(self.reviewer, "DOC-002", "Wrong", "No")

    def test_submit_requires_draft(self) -> None:
        self.system.create_document(self.author, "DOC-003", "Spec", "v1")
        self.system.submit_for_review(self.author, "DOC-003")

        with self.assertRaises(EDMSStateError):
            self.system.submit_for_review(self.author, "DOC-003")

    def test_approve_requires_approver_role(self) -> None:
        self.system.create_document(self.author, "DOC-004", "Policy", "v1")
        self.system.submit_for_review(self.author, "DOC-004")

        with self.assertRaises(EDMSPermissionError):
            self.system.approve(self.author, "DOC-004")

    def test_duplicate_document_id_rejected(self) -> None:
        self.system.create_document(self.author, "DOC-005", "One", "v1")

        with self.assertRaises(ValueError):
            self.system.create_document(self.author, "DOC-005", "Two", "v2")


if __name__ == "__main__":
    unittest.main()
