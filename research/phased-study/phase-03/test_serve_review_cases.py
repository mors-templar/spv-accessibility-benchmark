"""Test the condition-masked review view with synthetic cases."""

import functools
import http.server
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch

import prepare_review_cases as review
import prepare_trial as trial
import run_codex_development as development
import serve_review_cases as server


class ReviewServerTests(unittest.TestCase):
    def setUp(self):
        temp_parent = trial.REPOSITORY / "local"
        temp_parent.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=temp_parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.site = self.root / "cases/CASE-01/site"
        self.site.mkdir(parents=True)
        (self.site / "index.html").write_bytes(b"<html>fixture</html>")

    def test_index_does_not_render_condition_and_escapes_text(self):
        page = server.review_html([{"case_id": "CASE-01", "task_id": "<script>",
                                    "url": "http://127.0.0.1:1234/", "condition": "secret-condition"}])
        self.assertNotIn("secret-condition", page)
        self.assertIn("&lt;script&gt;", page)

    def test_refuses_modified_review_copy(self):
        case = {"case_id": "CASE-01", "included_files": development.artifact_manifest(self.site)["files"]}
        (self.site / "index.html").write_text("changed", encoding="utf-8")
        with patch.object(review, "REVIEW_ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "differs"):
                server.verified_site(case)

    @unittest.skipUnless(os.environ.get("SPV_RUN_LOOPBACK_TESTS") == "1", "loopback test is opt-in")
    def test_loopback_server_blocks_private_sidecars(self):
        (self.site / "AGENTS.md").write_text("synthetic private", encoding="utf-8")
        handler = functools.partial(server.CaseHandler, directory=str(self.site))
        httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, timeout=5)
        self.addCleanup(httpd.server_close)
        self.addCleanup(httpd.shutdown)
        base = f"http://127.0.0.1:{httpd.server_port}"
        with urllib.request.urlopen(base + "/", timeout=5) as response:
            self.assertEqual(response.read(), b"<html>fixture</html>")
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(base + "/AGENTS.md", timeout=5)
        self.assertEqual(error.exception.code, 404)

    @unittest.skipUnless(os.environ.get("SPV_RUN_LOOPBACK_TESTS") == "1", "loopback test is opt-in")
    def test_hub_does_not_serve_private_mapping(self):
        server.HubHandler.content = b"synthetic hub"
        httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), server.HubHandler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join, timeout=5)
        self.addCleanup(httpd.server_close)
        self.addCleanup(httpd.shutdown)
        base = f"http://127.0.0.1:{httpd.server_port}"
        with urllib.request.urlopen(base + "/", timeout=5) as response:
            self.assertEqual(response.read(), b"synthetic hub")
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(base + "/private-mapping.json", timeout=5)
        self.assertEqual(error.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
