"""Test masked review copies using synthetic artifacts."""

import json
import tempfile
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
