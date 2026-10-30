"""Check audit preconditions using synthetic ledgers."""

import json
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import audit_exploratory_batch as audit_batch
import prepare_trial as trial
import run_codex_development as development


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

    def test_uncompiled_jsx_is_a_gap_not_a_clean_scan(self):
        runs = self.root / "runs"
        workspace = runs / "run1/workspace"
        workspace.mkdir(parents=True)
        (workspace / "index.html").write_text('<script type="module" src="/src/main.jsx"></script>', encoding="utf-8")
        item = {"run_id": "run1", "task_id": "TASK1", "condition": "D", "status": "turn_completed_unassessed"}
        record = {**item, "final_workspace": development.artifact_manifest(workspace)}
        (runs / "run1/record.json").write_text(json.dumps(record), encoding="utf-8")
        self.generation.write_text(json.dumps({"status": "stopped", "schedule_sha256": "hash", "attempts": [item]}),
                                   encoding="utf-8")
        with patch.object(audit_batch, "LEDGER", self.output), patch.object(development, "RUNS", runs), \
             patch.object(audit_batch.batch, "LEDGER", self.generation), \
             patch.object(audit_batch.batch, "checked_schedule", return_value=({"attempts": [item]}, "hash")), \
             patch.object(audit_batch.subprocess, "run", side_effect=AssertionError("browser must not run")), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(audit_batch.main(), 0)
        ledger = json.loads(self.output.read_text(encoding="utf-8"))
        self.assertEqual(ledger["attempts"][0]["status"], "not_assessed_source_requires_build")
        self.assertNotIn("summary", ledger["attempts"][0])


if __name__ == "__main__":
    unittest.main()
