from __future__ import annotations

import unittest

from tests.support.foundation import EDMSTestFoundation, ValidationError


class TestControlledPrinting(unittest.TestCase):
    def setUp(self) -> None:
        self.foundation = EDMSTestFoundation()
        self.foundation.create_draft("DOC-201", "Labeling SOP", "author.1")
        self.version = self.foundation.add_version("DOC-201", "s3://doc/v1", "abc", "author.1")
        self.print_event = self.foundation.request_print("DOC-201", self.version.version_id, "issuer.1", quantity=3)

    def test_unique_copy_numbering_and_watermark_metadata(self) -> None:
        issued = self.foundation.issue_print(self.print_event.event_id, "issuer.1", quantity=3)

        self.assertEqual([1, 2, 3], [row["copy_number"] for row in issued])
        self.assertEqual(self.print_event.event_id, issued[0]["watermark"]["print_event_id"])
        self.assertEqual("DOC-201", issued[0]["watermark"]["document_id"])

    def test_issuance_and_return_reconciliation(self) -> None:
        self.foundation.issue_print(self.print_event.event_id, "issuer.1", quantity=2)

        self.foundation.reconcile_print(self.print_event.event_id, "issuer.1", returned_copy_numbers=[1, 2])

        self.assertTrue(self.foundation.print_events[self.print_event.event_id].reconciled)

    def test_reprint_restrictions_after_reconciliation(self) -> None:
        self.foundation.issue_print(self.print_event.event_id, "issuer.1", quantity=1)
        self.foundation.reconcile_print(self.print_event.event_id, "issuer.1", returned_copy_numbers=[1])

        with self.assertRaises(ValidationError):
            self.foundation.issue_print(self.print_event.event_id, "issuer.1", quantity=1)

    def test_issue_cannot_exceed_requested_quantity(self) -> None:
        with self.assertRaises(ValidationError):
            self.foundation.issue_print(self.print_event.event_id, "issuer.1", quantity=4)


if __name__ == "__main__":
    unittest.main()
