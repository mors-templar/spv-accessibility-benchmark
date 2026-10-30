"""Test rendered-page readiness on synthetic loopback fixtures."""

import functools
import contextlib
import http.server
import io
import json
import os
import shutil
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

import audit_initial_state as audit
import prepare_trial as trial
import run_codex_development as development


@unittest.skipUnless(os.environ.get("SPV_RUN_LOOPBACK_TESTS") == "1", "loopback test is opt-in")
class BrowserPreflightTests(unittest.TestCase):
    def setUp(self):
        temp_parent = trial.REPOSITORY / "local"
        temp_parent.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=temp_parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(self.root))
        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, timeout=5)
        self.addCleanup(self.httpd.server_close)
        self.addCleanup(self.httpd.shutdown)

    def preflight(self, content):
        (self.root / "index.html").write_text(content, encoding="utf-8")
        env = os.environ.copy()
        env["PLAYWRIGHT_BROWSERS_PATH"] = str(audit.BROWSERS)
        command = [shutil.which("node"), str(audit.PREFLIGHT), str(audit.PILOT),
                   f"http://127.0.0.1:{self.httpd.server_port}/"]
        result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=30, check=True)
        return json.loads(result.stdout)

    def test_blank_page_is_not_reported_ready(self):
        result = self.preflight("<!doctype html><html><body><div id='root'></div></body></html>")
        self.assertEqual(result["status"], "blank_initial_state")

    def test_visible_text_is_observed_without_claiming_completeness(self):
        result = self.preflight("<!doctype html><html><body><h1>Synthetic heading</h1></body></html>")
        self.assertEqual(result["status"], "visible_text_observed")
        self.assertGreater(result["visible_text_characters"], 0)
        self.assertIn("does not prove", result["limitation"])

    def test_blank_artifact_does_not_receive_an_axe_report(self):
        runs = self.root / "runs"
        run = runs / "fixture"
        workspace = run / "workspace"
        workspace.mkdir(parents=True)
        (workspace / "index.html").write_text("<!doctype html><html><body><div id='root'></div></body></html>", encoding="utf-8")
        record = {"status": "turn_completed_unassessed", "condition": "B", "task_id": "SYNTHETIC",
                  "final_workspace": development.artifact_manifest(workspace)}
        (run / "record.json").write_text(json.dumps(record), encoding="utf-8")
        with patch.object(development, "RUNS", runs), patch("sys.argv", ["audit", "--run-id", "fixture"]), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(audit.main(), 1)
        metadata = json.loads((run / "initial-axe-metadata.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["status"], "not_assessed_blank_initial_state")
        self.assertFalse((run / "initial-axe-report.json").exists())

    def test_visible_artifact_can_receive_an_axe_report(self):
        runs = self.root / "runs"
        run = runs / "fixture"
        workspace = run / "workspace"
        workspace.mkdir(parents=True)
        (workspace / "index.html").write_text(
            "<!doctype html><html lang='en'><head><title>Fixture</title></head><body><main><h1>Test</h1></main></body></html>",
            encoding="utf-8",
        )
        record = {"status": "turn_completed_unassessed", "condition": "B", "task_id": "SYNTHETIC",
                  "final_workspace": development.artifact_manifest(workspace)}
        (run / "record.json").write_text(json.dumps(record), encoding="utf-8")
        with patch.object(development, "RUNS", runs), patch("sys.argv", ["audit", "--run-id", "fixture"]), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(audit.main(), 0)
        metadata = json.loads((run / "initial-axe-metadata.json").read_text(encoding="utf-8"))
        self.assertEqual(metadata["status"], "completed")
        self.assertTrue((run / "initial-axe-report.json").is_file())


if __name__ == "__main__":
    unittest.main()
