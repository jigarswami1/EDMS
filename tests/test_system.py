import unittest

from edms.models import DocumentState, Role, User
from edms.system import EDMS, EDMSPermissionError, EDMSStateError


class EDMSTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.edms = EDMS()
        self.author = User("u-author", "Author", Role.AUTHOR, "author-pass")
        self.reviewer = User("u-review", "Reviewer", Role.REVIEWER, "review-pass")
        self.approver = User("u-approve", "Approver", Role.APPROVER, "approve-pass")
        self.printer = User("u-print", "Printer", Role.PRINT_CUSTODIAN, "print-pass")

    def test_happy_path_workflow_with_controlled_print(self) -> None:
        document = self.edms.create_document(
            user=self.author,
            title="SOP for Line Clearance",
            document_type="SOP",
            department="QA",
            product_site="Site-A",
            content="Initial SOP content",
            metadata={"effective_date_target": "2026-03-01"},
        )
        self.edms.submit_for_review(self.author, document.document_id, "Ready for QA review")
        self.edms.complete_review(self.reviewer, document.document_id, "Reviewed and acceptable")
        self.edms.approve_document(
            self.approver,
            document.document_id,
            "Approved for release",
            password_confirmation="approve-pass",
        )

        effective = self.edms.list_effective_documents()
        self.assertEqual(1, len(effective))
        self.assertEqual(DocumentState.EFFECTIVE, document.current_version().state)

        print_copy = self.edms.controlled_print(self.printer, document.document_id)
        self.assertEqual(1, print_copy.copy_number)
        self.assertFalse(print_copy.reconciled)

        reconciled = self.edms.reconcile_print_copy(
            self.printer,
            document.document_id,
            print_copy.print_id,
            "Returned and destroyed",
        )
        self.assertTrue(reconciled.reconciled)

    def test_approval_requires_signature_password_confirmation(self) -> None:
        document = self.edms.create_document(
            self.author, "WI", "Work Instruction", "MFG", "Site-B", "content"
        )
        self.edms.submit_for_review(self.author, document.document_id, "review it")
        self.edms.complete_review(self.reviewer, document.document_id, "ok")

        with self.assertRaises(EDMSPermissionError):
            self.edms.approve_document(
                self.approver,
                document.document_id,
                "approving",
                password_confirmation="wrong-pass",
            )

    def test_role_based_access_enforced(self) -> None:
        document = self.edms.create_document(
            self.author, "Policy", "Policy", "QA", "Site-C", "policy"
        )
        with self.assertRaises(EDMSPermissionError):
            self.edms.complete_review(self.author, document.document_id, "not allowed")

    def test_revisions_keep_prior_effective_version_obsolete(self) -> None:
        document = self.edms.create_document(
            self.author, "Spec", "Specification", "QC", "Site-A", "v1"
        )
        self.edms.submit_for_review(self.author, document.document_id, "review")
        self.edms.complete_review(self.reviewer, document.document_id, "good")
        self.edms.approve_document(
            self.approver, document.document_id, "approve", "approve-pass"
        )

        revision = self.edms.revise_document(self.author, document.document_id, "v1.1")
        self.assertEqual("v1.1", revision.version_id)

        self.edms.submit_for_review(self.author, document.document_id, "review rev")
        self.edms.complete_review(self.reviewer, document.document_id, "good rev")
        self.edms.approve_document(
            self.approver, document.document_id, "approve rev", "approve-pass"
        )

        self.assertEqual(DocumentState.OBSOLETE, document.versions[0].state)
        self.assertEqual(DocumentState.EFFECTIVE, document.current_version().state)

    def test_invalid_state_transition_rejected(self) -> None:
        document = self.edms.create_document(
            self.author, "Batch Record", "Batch Record", "MFG", "Site-Z", "data"
        )
        with self.assertRaises(EDMSStateError):
            self.edms.approve_document(
                self.approver,
                document.document_id,
                "cannot approve",
                "approve-pass",
            )

    def test_effective_doc_remains_listed_during_draft_revision(self) -> None:
        document = self.edms.create_document(
            self.author, "Form", "Form", "QA", "Site-A", "v1"
        )
        self.edms.submit_for_review(self.author, document.document_id, "review")
        self.edms.complete_review(self.reviewer, document.document_id, "good")
        self.edms.approve_document(
            self.approver, document.document_id, "approve", "approve-pass"
        )

        self.edms.revise_document(self.author, document.document_id, "v1.1 draft")

        effective = self.edms.list_effective_documents()
        self.assertEqual([document.document_id], [doc.document_id for doc in effective])

    def test_controlled_print_uses_effective_version_when_revision_is_draft(self) -> None:
        document = self.edms.create_document(
            self.author, "Procedure", "SOP", "QA", "Site-A", "v1"
        )
        self.edms.submit_for_review(self.author, document.document_id, "review")
        self.edms.complete_review(self.reviewer, document.document_id, "good")
        self.edms.approve_document(
            self.approver, document.document_id, "approve", "approve-pass"
        )
        self.edms.revise_document(self.author, document.document_id, "v1.1 draft")

        print_copy = self.edms.controlled_print(self.printer, document.document_id)
        self.assertEqual("v1.0", print_copy.source_version)

    def test_reconcile_print_created_before_revision(self) -> None:
        document = self.edms.create_document(
            self.author, "Logbook", "Template", "MFG", "Site-B", "v1"
        )
        self.edms.submit_for_review(self.author, document.document_id, "review")
        self.edms.complete_review(self.reviewer, document.document_id, "good")
        self.edms.approve_document(
            self.approver, document.document_id, "approve", "approve-pass"
        )

        print_copy = self.edms.controlled_print(self.printer, document.document_id)
        self.edms.revise_document(self.author, document.document_id, "v1.1 draft")

        reconciled = self.edms.reconcile_print_copy(
            self.printer,
            document.document_id,
            print_copy.print_id,
            "Returned after draft created",
        )
        self.assertTrue(reconciled.reconciled)


if __name__ == "__main__":
    unittest.main()
