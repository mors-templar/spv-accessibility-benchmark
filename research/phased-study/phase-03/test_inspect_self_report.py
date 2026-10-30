"""Check conservative parsing of synthetic model self-reports."""

import unittest

import inspect_self_report as claims


class SelfReportParserTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            {"id": "ACT-001", "basis": "R"},
            {"id": "ACT-002", "basis": "G"},
            {"id": "ACT-003", "basis": "P"},
            {"id": "ACT-004", "basis": "R"},
        ]

    def test_parses_table_and_bullet_statuses(self):
        report = "\n".join([
            "| ACT-001 | pass | Synthetic evidence |",
            "- ACT-002 [G]: **not applicable** - no matching component",
            "- ACT-003 [P]: **researcher responsibility** - study task",
            "| ACT-004 | unassessed | Not checked |",
        ])
        result = claims.parse_claims(report, self.items)
        self.assertEqual(result["recognized_unique_items"], 4)
        self.assertEqual(result["status_counts_by_basis"]["R"], {"pass": 1, "unassessed": 1})
        self.assertEqual(result["missing_ids"], [])

    def test_does_not_count_duplicate_or_invalid_claims(self):
        report = "\n".join([
            "| ACT-001 | pass | first |",
            "| ACT-001 | fail | second |",
            "| ACT-002 | maybe | unclear |",
            "| ACT-003 | pass | invalid for process item |",
            "| ACT-999 | pass | not in checklist |",
        ])
        result = claims.parse_claims(report, self.items)
        self.assertEqual(result["recognized_unique_items"], 0)
        self.assertEqual(result["duplicate_ids"], ["ACT-001"])
        self.assertEqual(result["unrecognized_status_ids"], ["ACT-002"])
        self.assertEqual(result["invalid_status_for_basis_ids"], ["ACT-003"])
        self.assertEqual(result["missing_ids"], ["ACT-004"])
        self.assertEqual(result["extra_ids"], ["ACT-999"])

    def test_does_not_treat_pass_as_prefix_of_another_word(self):
        result = claims.parse_claims("| ACT-001 | passionate | text |", self.items)
        self.assertEqual(result["unrecognized_status_ids"], ["ACT-001"])


if __name__ == "__main__":
    unittest.main()
