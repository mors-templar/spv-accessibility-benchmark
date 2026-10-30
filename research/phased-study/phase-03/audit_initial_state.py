#!/usr/bin/env python3
"""Run the existing axe browser pilot on one preserved exploratory artifact."""

import argparse
import datetime
import functools
import hashlib
import http.server
import json
import os
import re
import shutil
import subprocess
import threading
from pathlib import Path

import run_codex_development as development


PILOT = development.PROJECT / "work/avenues/04_evaluation_testbed/browser_pilot"
BROWSERS = development.PROJECT / "work/.playwright-browsers"


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def checked_index(run_dir):
    record = json.loads((run_dir / "record.json").read_text(encoding="utf-8"))
    if record["status"] != "turn_completed_unassessed":
        raise ValueError("Generation did not complete; the initial page is unassessable.")
    workspace = run_dir / "workspace"
    if development.artifact_manifest(workspace) != record["final_workspace"]:
        raise ValueError("The generated workspace differs from its recorded artifact manifest.")
    matches = [item for item in record["final_workspace"]["files"] if item["path"] == "index.html"]
    index = run_dir / "workspace/index.html"
    if len(matches) != 1 or not index.is_file() or index.is_symlink():
        raise ValueError("The preserved run does not contain a regular index.html.")
    if sha256_file(index) != matches[0]["sha256"]:
        raise ValueError("The page differs from the recorded generated artifact.")
    return record, index


class LocalHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        requested = Path(self.translate_path(self.path)).resolve()
        root = Path(self.directory).resolve()
        if not requested.is_relative_to(root):
            self.send_error(404)
            return None
        return super().send_head()

    def log_message(self, format, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", args.run_id):
        raise ValueError("Run ID must use letters, numbers, underscores, or hyphens.")
    run_dir = development.RUNS / args.run_id
    record, index = checked_index(run_dir)
    output = run_dir / "initial-axe-report.json"
    metadata_path = run_dir / "initial-axe-metadata.json"
    if output.exists() or metadata_path.exists():
        raise FileExistsError("An initial audit already exists for this run.")
    node = shutil.which("node")
    if not node or not (PILOT / "node_modules").is_dir() or not BROWSERS.is_dir():
        raise ValueError("Node, the browser pilot dependencies, or the local browser cache is missing.")

    handler = functools.partial(LocalHandler, directory=str(index.parent))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}/"
    command = [node, str(PILOT / "audit.js"), "--url", url, "--output", str(output)]
    environment = os.environ.copy()
    environment["PLAYWRIGHT_BROWSERS_PATH"] = str(BROWSERS)
    metadata = {
        "run_id": args.run_id,
        "condition": record["condition"],
        "task_id": record["task_id"],
        "artifact_index_sha256": sha256_file(index),
        "artifact_manifest_checked": True,
        "artifact_manifest_excludes": record["final_workspace"]["excluded_directories"],
        "audit_script_sha256": sha256_file(PILOT / "audit.js"),
        "package_lock_sha256": sha256_file(PILOT / "package-lock.json"),
        "purpose": "exploratory_initial_state_only",
        "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "status": "started",
    }
    development.write_json(metadata_path, metadata)
    try:
        completed = subprocess.run(command, cwd=PILOT, env=environment, capture_output=True, timeout=120, check=False)
        (run_dir / "initial-axe-stdout.log").write_bytes(completed.stdout)
        (run_dir / "initial-axe-stderr.log").write_bytes(completed.stderr)
        metadata["process_exit_code"] = completed.returncode
        metadata["status"] = "completed" if completed.returncode == 0 and output.is_file() else "audit_failed"
        if output.is_file():
            metadata["report_sha256"] = sha256_file(output)
    except subprocess.TimeoutExpired:
        metadata["status"] = "timeout"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        metadata["ended_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
        development.write_json(metadata_path, metadata)
    print(json.dumps(metadata, indent=2))
    return 0 if metadata["status"] == "completed" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=os.sys.stderr)
        raise SystemExit(1)
