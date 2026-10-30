"""Exercise the runner using synthetic tasks and a fake process."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import prepare_trial as trial
import run_codex_development as runner


class DevelopmentRunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.task = "Synthetic website request: café.\r\n".encode("utf-8")
        cls.digest = trial.sha256(cls.task)
        cls.d_assets = trial.load_intervention_assets(trial.REPOSITORY, "D")
        cls.p_assets = trial.load_intervention_assets(trial.REPOSITORY, "P")

    def setUp(self):
        temp_parent = trial.REPOSITORY / "local"
        temp_parent.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=temp_parent)
        self.runs = Path(self.temporary.name) / "runs"
        self.addCleanup(self.temporary.cleanup)

    def successful_process(self, captured):
        def run(command, **kwargs):
            captured.append(kwargs["input"])
            workspace = Path(command[command.index("-C") + 1])
            (workspace / "index.html").write_bytes(b"<html>synthetic</html>")
            kwargs["stdout"].write(b'{"type":"thread.started","thread_id":"synthetic"}\n')
            kwargs["stdout"].write(b'{"type":"turn.completed","usage":{"output_tokens":3}}\n')
            return subprocess.CompletedProcess(command, 0)
        return run

    def attempt(self, run_id, condition, assets, fake):
        return runner.run_attempt(self.runs, run_id, "PRACTICE", self.task, self.digest,
                                  condition, assets, "fake-codex", 30, run_process=fake)

    def test_baseline_preserves_input_and_records_artifact(self):
        captured = []
        record = self.attempt("run1", "B", None, self.successful_process(captured))
        self.assertEqual(captured, [self.task])
        self.assertEqual(record["status"], "turn_completed_unassessed")
        self.assertEqual(record["events"]["thread_id"], "synthetic")
        self.assertEqual(record["final_workspace"]["files"][0]["path"], "index.html")
        self.assertFalse((self.runs / "run1/workspace/AGENTS.md").exists())
        self.assertNotIn(self.task.decode("utf-8"), json.dumps(record))

    def test_d_and_p_send_same_message_but_only_p_has_guidance(self):
        captured = []
        fake = self.successful_process(captured)
        d_record = self.attempt("run2", "D", self.d_assets, fake)
        p_record = self.attempt("run3", "P", self.p_assets, fake)
        self.assertEqual(captured[0], captured[1])
        self.assertEqual(d_record["user_message_sha256"], p_record["user_message_sha256"])
        self.assertFalse((self.runs / "run2/workspace/AGENTS.md").exists())
        self.assertEqual((self.runs / "run3/workspace/AGENTS.md").read_bytes(), self.p_assets["guidance"])

    def test_failure_and_timeout_are_recorded(self):
        def fail(command, **kwargs):
            raise OSError("synthetic failure")
        def timeout(command, **kwargs):
            raise subprocess.TimeoutExpired(command, kwargs["timeout"])
        self.assertEqual(self.attempt("run4", "B", None, fail)["status"], "runner_start_failed")
        self.assertEqual(self.attempt("run5", "B", None, timeout)["status"], "timeout")
        self.assertEqual(json.loads((self.runs / "run5/record.json").read_text())["status"], "timeout")

    def test_existing_run_id_is_not_overwritten(self):
        self.attempt("run6", "B", None, self.successful_process([]))
        with self.assertRaises(FileExistsError):
            self.attempt("run6", "B", None, self.successful_process([]))

    def test_event_parser_rejects_invalid_lines(self):
        path = Path(self.temporary.name) / "events.jsonl"
        path.write_bytes(b'not json\n[]\n{"type":"turn.completed"}\n')
        parsed = runner.inspect_events(path)
        self.assertEqual(parsed["invalid_lines"], 2)
        self.assertTrue(parsed["turn_completed"])


if __name__ == "__main__":
    unittest.main()
