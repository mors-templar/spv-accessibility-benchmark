"""Check that resuming cannot overwrite an attempted run."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import prepare_trial as trial
import resume_exploratory_schedule as resume
import run_codex_development as development


class ResumeScheduleTests(unittest.TestCase):
    def setUp(self):
        temp_parent = trial.REPOSITORY / "local"
        temp_parent.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=temp_parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.ledger_path = self.root / "ledger.json"
        self.attempts = [
            {"run_id": "case1", "task_id": "T1", "condition": "B", "status": "runner_failed_or_incomplete"},
            {"run_id": "case2", "task_id": "T1", "condition": "P", "status": "planned"},
        ]
        self.schedule = {"attempts": [{k: item[k] for k in ("run_id", "task_id", "condition")} for item in self.attempts]}
        (self.root / "case1").mkdir()
        (self.root / "case1/record.json").write_text(json.dumps(self.attempts[0]), encoding="utf-8")
        self.save()

    def save(self):
        self.ledger_path.write_text(json.dumps({"status": "stopped_after_runner_failure", "schedule_sha256": "hash",
                                                "attempts": self.attempts}), encoding="utf-8")

    def check(self):
        with patch.object(resume.batch, "LEDGER", self.ledger_path), patch.object(development, "RUNS", self.root):
            return resume.checked_ledger(self.schedule, "hash")

    def test_preserves_failed_attempt_and_allows_untouched_entry(self):
        ledger = self.check()
        self.assertEqual(ledger["attempts"][0]["status"], "runner_failed_or_incomplete")
        self.assertEqual(ledger["attempts"][1]["status"], "planned")

    def test_existing_planned_directory_is_not_overwritten(self):
        (self.root / "case2").mkdir()
        with self.assertRaisesRegex(ValueError, "do not overwrite"):
            self.check()

    def test_unresolved_starting_attempt_needs_investigation(self):
        self.attempts[1]["status"] = "starting"
        self.save()
        with self.assertRaisesRegex(ValueError, "manual investigation"):
            self.check()


if __name__ == "__main__":
    unittest.main()
