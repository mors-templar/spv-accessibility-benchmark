"""Ensure exploratory summaries retain missing scans and axe impact counts."""

import unittest

import summarize_exploratory as summary


class SummaryTests(unittest.TestCase):
    def setUp(self):
        self.generation = {"run_id": "case1", "task_id": "TASK1", "condition": "B",
                           "status": "turn_completed_unassessed"}

    def test_missing_scan_is_not_treated_as_zero(self):
        row = summary.summarize_row(self.generation, {"status": "not_assessed_source_requires_build"})
        self.assertIsNone(row["axe"])
        self.assertIn("| - | - | - | - | - | - |", summary.markdown([row]))

    def test_completed_scan_records_node_counts_and_incomplete_rules(self):
        audit = {"status": "completed", "blocked_requests": 0,
                 "summary": {"total_rules": 1, "total_nodes": 3, "incomplete_rules": 2,
                             "violations_by_impact": {"serious": {"rules": 1, "nodes": 3}}}}
        row = summary.summarize_row(self.generation, audit)
        self.assertEqual(row["axe"]["nodes_by_impact"]["serious"], 3)
        self.assertEqual(row["axe"]["nodes_by_impact"]["critical"], 0)
        self.assertEqual(row["axe"]["incomplete_rules"], 2)


if __name__ == "__main__":
    unittest.main()
