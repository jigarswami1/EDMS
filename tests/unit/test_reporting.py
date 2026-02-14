from __future__ import annotations

import unittest
from datetime import datetime, timedelta

from tests.support.foundation import EDMSTestFoundation


class TestReporting(unittest.TestCase):
    def setUp(self) -> None:
        self.foundation = EDMSTestFoundation()
        self.foundation.create_draft("DOC-301", "Deviation Procedure", "author.1")
        self.foundation.add_version("DOC-301", "s3://doc/v1", "abc", "author.1")
        self.foundation.submit_review("DOC-301", "author.1")

    def test_overdue_tasks_report(self) -> None:
        now = datetime.utcnow()
        self.foundation.create_task("DOC-301", "reviewer.1", now - timedelta(days=1))
        self.foundation.create_task("DOC-301", "reviewer.2", now + timedelta(days=1))

        overdue = self.foundation.report_overdue_tasks(as_of=now)

        self.assertEqual(1, len(overdue))
        self.assertEqual("reviewer.1", overdue[0].assignee_id)

    def test_pending_approvals_report(self) -> None:
        pending = self.foundation.report_pending_approvals()

        self.assertEqual(1, len(pending))
        self.assertEqual("DOC-301", pending[0].document_id)

    def test_inspection_ready_audit_export(self) -> None:
        rows = self.foundation.export_audit_for_inspection("DOC-301")

        self.assertGreaterEqual(len(rows), 3)
        self.assertTrue({"entry_id", "occurred_at", "actor_id", "action", "metadata"}.issubset(rows[0].keys()))


if __name__ == "__main__":
    unittest.main()
