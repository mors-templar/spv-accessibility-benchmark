"""Check schedule coverage and input-hash guards without starting a model."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import prepare_trial as trial
import run_exploratory_schedule as batch


class ExploratoryScheduleTests(unittest.TestCase):
    def test_all_five_tasks_have_three_conditions(self):
        schedule, _ = batch.checked_schedule()
        pairs = {(item["task_id"], item["condition"]) for item in schedule["attempts"]}
        self.assertEqual(len(pairs), 15)
        self.assertEqual(len({task for task, _ in pairs}), 5)

    def test_changed_runner_hash_is_rejected(self):
        schedule, _ = batch.checked_schedule()
        schedule["runner_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "runner_sha256"):
            batch.verify_hashes(schedule)

    def test_duplicate_attempt_is_rejected(self):
        schedule, _ = batch.checked_schedule()
        schedule["attempts"][1] = dict(schedule["attempts"][0])
        temp_parent = trial.REPOSITORY / "local"
        temp_parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp_parent) as temporary:
            path = Path(temporary) / "schedule.json"
            path.write_text(json.dumps(schedule), encoding="utf-8")
            with patch.object(batch, "SCHEDULE", path):
                with self.assertRaisesRegex(ValueError, "unique"):
                    batch.checked_schedule()


if __name__ == "__main__":
    unittest.main()
