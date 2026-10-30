"""Validate artifact selection with synthetic files; do not start a browser."""

import json
import tempfile
import unittest
from pathlib import Path

import audit_initial_state as audit
import prepare_trial as trial
import run_codex_development as development


class ArtifactSelectionTests(unittest.TestCase):
    def setUp(self):
        temp_parent = trial.REPOSITORY / "local"
        temp_parent.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=temp_parent)
        self.addCleanup(self.temporary.cleanup)
        self.run = Path(self.temporary.name)
        (self.run / "workspace").mkdir()
        self.index = self.run / "workspace/index.html"
        self.index.write_text("<html>fixture</html>", encoding="utf-8")
        self.record = {
            "status": "turn_completed_unassessed",
            "final_workspace": development.artifact_manifest(self.run / "workspace"),
        }
        self.save()

    def save(self):
        (self.run / "record.json").write_text(json.dumps(self.record), encoding="utf-8")

    def test_accepts_unchanged_recorded_page(self):
        _, index = audit.checked_index(self.run)
        self.assertEqual(index, self.index)

    def test_rejects_page_changed_after_generation(self):
        self.index.write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "differs"):
            audit.checked_index(self.run)

    def test_refuses_failed_generation(self):
        self.record["status"] = "timeout"
        self.save()
        with self.assertRaisesRegex(ValueError, "unassessable"):
            audit.checked_index(self.run)

    def test_identifies_uncompiled_jsx_entry(self):
        self.index.write_text('<script type="module" src="/src/main.JSX?version=1"></script>', encoding="utf-8")
        self.assertTrue(audit.needs_build(self.index))

    def test_plain_javascript_entry_is_not_automatically_classified_as_build_required(self):
        self.index.write_text('<script src="app.js"></script>', encoding="utf-8")
        self.assertFalse(audit.needs_build(self.index))


if __name__ == "__main__":
    unittest.main()
