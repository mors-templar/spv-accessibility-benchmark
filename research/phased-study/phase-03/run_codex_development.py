#!/usr/bin/env python3
"""Run one exploratory B, D, or P attempt using the local Codex CLI."""

import argparse
import datetime
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import prepare_trial as trial


REPOSITORY = trial.REPOSITORY
PROJECT = REPOSITORY.parents[2]
TASK_MANIFEST = PROJECT / "work/experiments/benchmarks/selected_arena_baselines/manifest.json"
TASK_CACHE = PROJECT / "work/.arena-research-cache/selected-baseline-prompts"
RUNS = REPOSITORY / "local/phase-03-development"
DEFAULT_MODEL = "gpt-6.1-terra"
DEFAULT_TIMEOUT_SECONDS = 1200


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def isolation_config():
    """Restrict model commands to the workspace and required runtime directories."""
    runtime = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies"
    node = shutil.which("node")
    if not runtime.is_dir() or not node:
        raise ValueError("The bundled Codex runtime or Node executable is unavailable.")
    roots = list(dict.fromkeys([str(runtime.resolve()), str(Path(node).resolve().parent),
                                str(Path(sys.executable).resolve().parent)]))
    entries = ['":root"="deny"', '":minimal"="read"']
    entries.extend(json.dumps(root) + '="read"' for root in roots)
    return "{ " + ", ".join(entries) + " }", roots


def read_task(task_id):
    manifest = json.loads(TASK_MANIFEST.read_text(encoding="utf-8"))
    matches = [task for task in manifest["tasks"] if task["task_id"] == task_id]
    if len(matches) != 1:
        raise ValueError("Task ID must match exactly one selected task.")
    selected = matches[0]
    name = selected["local_filename"]
    if Path(name).name != name:
        raise ValueError("Task file must be a filename inside the local cache.")
    path = (TASK_CACHE / name).resolve()
    if not path.is_relative_to(TASK_CACHE.resolve()):
        raise ValueError("Task file is outside the local cache.")
    return selected, path.read_bytes()


def artifact_manifest(workspace):
    files = []
    excluded = []
    root = workspace.resolve()
    for path in sorted(workspace.rglob("*")):
        relative = path.relative_to(workspace)
        if any(part in {"node_modules", ".git"} for part in relative.parts):
            continue
        if path.is_symlink():
            excluded.append({"path": relative.as_posix(), "reason": "symbolic_link"})
            continue
        if not path.is_file():
            continue
        if not path.resolve().is_relative_to(root):
            excluded.append({"path": relative.as_posix(), "reason": "outside_workspace"})
            continue
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        files.append({"path": relative.as_posix(), "bytes": path.stat().st_size, "sha256": digest.hexdigest()})
    return {"files": files, "excluded_paths": excluded, "excluded_directories": [".git", "node_modules"]}


def inspect_events(path):
    summary = {"thread_id": None, "turn_completed": False, "turn_failed": False, "usage": None, "invalid_lines": 0}
    with path.open(encoding="utf-8", errors="replace") as stream:
        for line in stream:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                summary["invalid_lines"] += 1
                continue
            if not isinstance(event, dict):
                summary["invalid_lines"] += 1
                continue
            if event.get("type") == "thread.started":
                summary["thread_id"] = event.get("thread_id")
            elif event.get("type") == "turn.completed":
                summary["turn_completed"] = True
                summary["usage"] = event.get("usage")
            elif event.get("type") in {"turn.failed", "error"}:
                summary["turn_failed"] = True
    return summary


def run_attempt(run_root, run_id, task_id, task, expected_hash, condition, assets, codex, timeout_seconds, run_process=subprocess.run):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", run_id):
        raise ValueError("Run ID must use letters, numbers, underscores, or hyphens.")
    if timeout_seconds <= 0:
        raise ValueError("Timeout must be positive.")
    message, input_metadata = trial.prepare(task, expected_hash, condition, assets)
    filesystem, runtime_roots = isolation_config()
    run_root.mkdir(parents=True, exist_ok=True)
    run_dir = run_root / run_id
    run_dir.mkdir(exist_ok=False)
    workspace = run_dir / "workspace"
    workspace.mkdir()

    if condition == "P":
        (workspace / "AGENTS.md").write_bytes(assets["guidance"])
    initial_files = artifact_manifest(workspace)
    command = [
        str(codex), "exec", "--json", "--ephemeral", "--ignore-user-config",
        "--enable", "prefer_mxc", "--disable", "multi_agent", "--skip-git-repo-check",
        "-c", 'default_permissions="benchmark"',
        "-c", "agents.enabled=false",
        "-c", 'permissions.benchmark.extends=":workspace"',
        "-c", "permissions.benchmark.filesystem=" + filesystem,
        "--model", DEFAULT_MODEL, "-c", "model_reasoning_effort=high", "-C", str(workspace), "-",
    ]
    record = {
        "record_version": "0.2.0",
        "purpose": "exploratory_development_not_final_benchmark",
        "run_id": run_id,
        "task_id": task_id,
        "condition": condition,
        "task_sha256": trial.sha256(task),
        "user_message_sha256": trial.sha256(message),
        "user_message_bytes": len(message),
        "input_metadata": input_metadata,
        "requested_model": DEFAULT_MODEL,
        "requested_reasoning_effort": "high",
        "requested_subagents": "disabled",
        "requested_sandbox": "benchmark profile: workspace write, minimal and runtime read, other root denied",
        "requested_runtime_read_roots": runtime_roots,
        "runner_sha256": trial.sha256(Path(__file__).read_bytes()),
        "python_version": platform.python_version(),
        "operating_system": platform.platform(),
        "effective_hidden_instructions": "unknown",
        "effective_server_message_bytes": "not_observed",
        "cli_flags": command[1:-1],
        "timeout_seconds": timeout_seconds,
        "initial_workspace": initial_files,
        "status": "started",
        "start_utc": now_utc(),
    }
    write_json(run_dir / "record.json", record)
    environment = os.environ.copy()
    for name in ("OPENAI_API_KEY", "CODEX_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"):
        environment.pop(name, None)

    started = time.monotonic()
    events_path = run_dir / "events.jsonl"
    try:
        with events_path.open("wb") as events, (run_dir / "stderr.log").open("wb") as errors:
            completed = run_process(command, input=message, stdout=events, stderr=errors, env=environment,
                                    timeout=timeout_seconds, check=False)
        record["process_exit_code"] = completed.returncode
        event_summary = inspect_events(events_path)
        record["events"] = event_summary
        if completed.returncode == 0 and event_summary["turn_completed"] and not event_summary["turn_failed"]:
            record["status"] = "turn_completed_unassessed"
        else:
            record["status"] = "runner_failed_or_incomplete"
    except subprocess.TimeoutExpired:
        record["status"] = "timeout"
        record["descendant_process_termination"] = "not_verified"
    except OSError as exc:
        record["status"] = "runner_start_failed"
        record["error_type"] = type(exc).__name__
    finally:
        record["elapsed_seconds"] = round(time.monotonic() - started, 3)
        record["end_utc"] = now_utc()
        record["final_workspace"] = artifact_manifest(workspace)
        write_json(run_dir / "record.json", record)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--condition", choices=("B", "D", "P"), required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    args = parser.parse_args()
    codex = shutil.which("codex")
    if not codex:
        raise ValueError("Codex CLI is not available on PATH.")
    selected, task = read_task(args.task_id)
    assets = trial.load_intervention_assets(REPOSITORY, args.condition) if args.condition != "B" else None
    record = run_attempt(RUNS, args.run_id, args.task_id, task, selected["prompt_sha256_utf8"],
                         args.condition, assets, codex, args.timeout_seconds)
    print(json.dumps({"run_id": record["run_id"], "task_id": record["task_id"], "condition": record["condition"],
                      "status": record["status"], "record": str(RUNS / args.run_id / "record.json")}, indent=2))
    return 0 if record["status"] == "turn_completed_unassessed" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=os.sys.stderr)
        raise SystemExit(1)
