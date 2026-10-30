"""Check audit preconditions using synthetic ledgers."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import audit_exploratory_batch as audit_batch
import prepare_trial as trial


class AuditBatchTests(unittest.TestCase):
    def setUp(self):
        temp_parent = trial.REPOSITORY / "local"
        temp_parent.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=temp_parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.generation = self.root / "generation.json"
        self.output = self.root / "audit.json"

    def test_refuses_to_audit_while_generation_is_running(self):
        self.generation.write_text(json.dumps({"status": "running"}), encoding="utf-8")
        with patch.object(audit_batch, "LEDGER", self.output), \
             patch.object(audit_batch.batch, "LEDGER", self.generation), \
             patch.object(audit_batch.batch, "checked_schedule", return_value=({}, "hash")):
            with self.assertRaisesRegex(ValueError, "Wait"):
                audit_batch.main()
        self.assertFalse(self.output.exists())

    def test_refuses_a_different_schedule(self):
        self.generation.write_text(json.dumps({"status": "stopped", "schedule_sha256": "other"}), encoding="utf-8")
        with patch.object(audit_batch, "LEDGER", self.output), \
             patch.object(audit_batch.batch, "LEDGER", self.generation), \
             patch.object(audit_batch.batch, "checked_schedule", return_value=({}, "hash")):
            with self.assertRaisesRegex(ValueError, "does not match"):
                audit_batch.main()
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
