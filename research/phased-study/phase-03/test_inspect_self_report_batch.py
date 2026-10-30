"""Check claim-inspection preconditions using synthetic ledgers."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import inspect_self_report_batch as claim_batch
import prepare_trial as trial


class ClaimBatchTests(unittest.TestCase):
    def setUp(self):
        temp_parent = trial.REPOSITORY / "local"
        temp_parent.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=temp_parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.generation = self.root / "generation.json"
        self.output = self.root / "claims.json"

    def check_refusal(self, ledger, message):
        self.generation.write_text(json.dumps(ledger), encoding="utf-8")
        with patch.object(claim_batch, "LEDGER", self.output), \
             patch.object(claim_batch.batch, "LEDGER", self.generation), \
             patch.object(claim_batch.batch, "checked_schedule", return_value=({}, "hash")):
            with self.assertRaisesRegex(ValueError, message):
                claim_batch.main()
        self.assertFalse(self.output.exists())

    def test_refuses_running_generation(self):
        self.check_refusal({"status": "running"}, "Wait")

    def test_refuses_different_schedule(self):
        self.check_refusal({"status": "stopped", "schedule_sha256": "other"}, "does not match")


if __name__ == "__main__":
    unittest.main()
