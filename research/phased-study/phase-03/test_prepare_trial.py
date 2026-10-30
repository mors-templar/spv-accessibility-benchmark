"""Check input preservation using synthetic text and local study files."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import prepare_trial as trial


class InputAssemblyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.task = "Synthetic task: café page.\r\n".encode("utf-8")
        cls.digest = trial.sha256(cls.task)
        cls.d_assets = trial.load_intervention_assets(trial.REPOSITORY, "D")
        cls.p_assets = trial.load_intervention_assets(trial.REPOSITORY, "P")

    def test_baseline_is_exact_task_without_intervention(self):
        message, metadata = trial.prepare(self.task, self.digest, "B")
        self.assertEqual(message, self.task)
        self.assertFalse(metadata["checklist_added"])
        self.assertIsNone(metadata["prompt_guidance_sha256"])

    def test_checklist_and_prompt_share_identical_user_message(self):
        direct, direct_meta = trial.prepare(self.task, self.digest, "D", self.d_assets)
        prompt, prompt_meta = trial.prepare(self.task, self.digest, "P", self.p_assets)
        expected = (
            self.task + trial.PREFIX + self.d_assets["instruction"]
            + trial.CHECKLIST_START + self.d_assets["checklist"] + trial.SUFFIX
        )
        self.assertEqual(direct, expected)
        self.assertEqual(prompt, expected)
        self.assertEqual(direct[:len(self.task)], self.task)
        self.assertIsNone(direct_meta["prompt_guidance_sha256"])
        self.assertEqual(prompt_meta["prompt_guidance_sha256"], trial.sha256(self.p_assets["guidance"]))

    def test_rejects_wrong_task_hash(self):
        with self.assertRaisesRegex(ValueError, "do not match"):
            trial.prepare(self.task, "0" * 64, "B")

    def test_rejects_changed_approved_checklist(self):
        temp_parent = trial.REPOSITORY / "local"
        temp_parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp_parent) as temporary:
            root = Path(temporary)
            relative_files = [
                trial.PHASE2 / "checklist-approval.json",
                trial.PHASE2 / "interventions/candidate-manifest.json",
                Path(trial.CHECKLIST_PATH),
                Path(trial.INSTRUCTION_PATH),
            ]
            for relative in relative_files:
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(trial.REPOSITORY / relative, destination)
            target = root / trial.CHECKLIST_PATH
            target.write_bytes(target.read_bytes() + b"changed")
            with self.assertRaisesRegex(ValueError, "differs from its recorded hash"):
                trial.load_intervention_assets(root, "D")

    def test_cli_outputs_metadata_without_task_text(self):
        temp_parent = trial.REPOSITORY / "local"
        temp_parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp_parent) as temporary:
            task_path = Path(temporary) / "practice.txt"
            task_path.write_bytes(self.task)
            result = subprocess.run(
                [sys.executable, str(Path(trial.__file__)), "--task-file", str(task_path),
                 "--expected-task-sha256", self.digest, "--condition", "P",
                 "--task-id", "PRACTICE", "--run-id", "PRACTICE-P-01"],
                capture_output=True, check=True,
            )
        self.assertNotIn(self.task, result.stdout)
        record = json.loads(result.stdout)
        self.assertFalse(record["sent_to_model"])
        self.assertEqual(record["task_sha256"], self.digest)
        self.assertEqual(record["metadata"]["candidate_status"], "draft_not_frozen")


if __name__ == "__main__":
    unittest.main()
