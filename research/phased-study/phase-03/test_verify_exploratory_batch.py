"""Check local provenance validation using synthetic artifacts."""

import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import prepare_trial as trial
import run_codex_development as development
import verify_exploratory_batch as verifier


class ProvenanceValidationTests(unittest.TestCase):
    def setUp(self):
        temp_parent = trial.REPOSITORY / "local"
        temp_parent.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=temp_parent)
        self.addCleanup(self.temporary.cleanup)
        self.runs = Path(self.temporary.name)
        self.workspace = self.runs / "case/workspace"
        self.workspace.mkdir(parents=True)
        self.task = b"Synthetic website request."
        self.digest = trial.sha256(self.task)
        self.item = {"run_id": "case", "task_id": "PRACTICE", "condition": "B"}
        message, metadata = trial.prepare(self.task, self.digest, "B")
        _, roots = development.isolation_config()
        (self.workspace / "index.html").write_text("<html></html>", encoding="utf-8")
        self.record = {
            **self.item, "status": "turn_completed_unassessed", "task_sha256": self.digest,
            "user_message_sha256": trial.sha256(message), "user_message_bytes": len(message),
            "input_metadata": metadata, "runner_sha256": "f" * 64,
            "requested_model": development.DEFAULT_MODEL, "requested_reasoning_effort": "high",
            "requested_subagents": "disabled",
            "requested_sandbox": "benchmark profile: workspace write, minimal and runtime read, other root denied",
            "requested_runtime_read_roots": roots, "timeout_seconds": development.DEFAULT_TIMEOUT_SECONDS,
            "initial_workspace": {"files": []},
            "final_workspace": development.artifact_manifest(self.workspace),
        }

    def validate(self, record):
        with patch.object(development, "RUNS", self.runs):
            return verifier.record_problems(self.item, record, self.task, self.digest, None, "f" * 64)

    def test_accepts_matching_local_evidence(self):
        self.assertEqual(self.validate(self.record), [])

    def test_detects_changed_input_and_sandbox_setting(self):
        record = copy.deepcopy(self.record)
        record["user_message_sha256"] = "0" * 64
        record["requested_subagents"] = "enabled"
        problems = self.validate(record)
        self.assertIn("local_message_mismatch", problems)
        self.assertIn("subagent_setting_mismatch", problems)

    def test_detects_changed_generated_file(self):
        (self.workspace / "index.html").write_text("changed", encoding="utf-8")
        self.assertIn("artifact_manifest_mismatch", self.validate(self.record))


if __name__ == "__main__":
    unittest.main()
