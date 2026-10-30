"""Test masked review copies using synthetic artifacts."""

import json
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import prepare_review_cases as review
import prepare_trial as trial
import run_codex_development as development


class ReviewCopyTests(unittest.TestCase):
    def setUp(self):
        temp_parent = trial.REPOSITORY / "local"
        temp_parent.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=temp_parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.run = self.root / "run"
        self.workspace = self.run / "workspace"
        self.workspace.mkdir(parents=True)
        (self.workspace / "index.html").write_bytes(b"<html>fixture</html>")
        (self.workspace / "style.css").write_bytes(b"body { color: black; }")
        (self.workspace / "AGENTS.md").write_text("hidden guidance", encoding="utf-8")
        (self.workspace / "spv-plan.md").write_text("hidden plan", encoding="utf-8")
        (self.workspace / "accessibility-self-report.md").write_text("hidden report", encoding="utf-8")
        record = {"status": "turn_completed_unassessed", "final_workspace": development.artifact_manifest(self.workspace)}
        (self.run / "record.json").write_text(json.dumps(record), encoding="utf-8")

    def test_copies_site_bytes_without_condition_sidecars(self):
        target = self.root / "case/site"
        manifest = review.copy_site(self.run, target)
        self.assertEqual((target / "index.html").read_bytes(), (self.workspace / "index.html").read_bytes())
        self.assertEqual((target / "style.css").read_bytes(), (self.workspace / "style.css").read_bytes())
        self.assertFalse((target / "AGENTS.md").exists())
        self.assertEqual(len(manifest["excluded_sidecars"]), 3)

    def test_refuses_artifact_changed_after_generation(self):
        (self.workspace / "style.css").write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "differs"):
            review.copy_site(self.run, self.root / "case/site")

    def test_batch_preparation_keeps_missing_static_pages_as_gaps(self):
        runs = self.root / "runs"
        runs.mkdir()
        self.run.rename(runs / "run1")
        first_record_path = runs / "run1/record.json"
        first_record = json.loads(first_record_path.read_text(encoding="utf-8"))
        first_record.update({"run_id": "run1", "task_id": "TASK1", "condition": "B"})
        first_record_path.write_text(json.dumps(first_record), encoding="utf-8")
        second_workspace = runs / "run2/workspace"
        second_workspace.mkdir(parents=True)
        (second_workspace / "App.tsx").write_text("export default function App() {}", encoding="utf-8")
        second_record = {"run_id": "run2", "task_id": "TASK2", "condition": "P",
                         "status": "turn_completed_unassessed",
                         "final_workspace": development.artifact_manifest(second_workspace)}
        (runs / "run2/record.json").write_text(json.dumps(second_record), encoding="utf-8")
        third_workspace = runs / "run3/workspace"
        third_workspace.mkdir(parents=True)
        (third_workspace / "index.html").write_text('<script type="module" src="/src/main.jsx"></script>', encoding="utf-8")
        third_record = {"run_id": "run3", "task_id": "TASK3", "condition": "D",
                        "status": "turn_completed_unassessed",
                        "final_workspace": development.artifact_manifest(third_workspace)}
        (runs / "run3/record.json").write_text(json.dumps(third_record), encoding="utf-8")
        entries = [
            {"run_id": "run1", "task_id": "TASK1", "condition": "B", "status": "turn_completed_unassessed"},
            {"run_id": "run2", "task_id": "TASK2", "condition": "P", "status": "turn_completed_unassessed"},
            {"run_id": "run3", "task_id": "TASK3", "condition": "D", "status": "turn_completed_unassessed"},
        ]
        generation = self.root / "ledger.json"
        generation.write_text(json.dumps({"status": "all_turns_completed_unassessed", "schedule_sha256": "hash",
                                          "attempts": entries}), encoding="utf-8")
        target = self.root / "review"
        with patch.object(review, "REVIEW_ROOT", target), patch.object(development, "RUNS", runs), \
             patch.object(review.batch, "LEDGER", generation), \
             patch.object(review.batch, "checked_schedule", return_value=({"attempts": entries}, "hash")), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(review.main(), 0)
        mapping = json.loads((target / "private-mapping.json").read_text(encoding="utf-8"))
        self.assertEqual({case["status"] for case in mapping["cases"]},
                         {"ready_static_copy", "no_static_index", "source_requires_build"})
        self.assertEqual(mapping["status"], "prepared_with_gaps")


if __name__ == "__main__":
    unittest.main()
