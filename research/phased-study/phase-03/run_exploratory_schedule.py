#!/usr/bin/env python3
"""Run the recorded exploratory Codex schedule once, stopping on runner failure."""

import json
import shutil
from pathlib import Path

import prepare_trial as trial
import run_codex_development as development


HERE = Path(__file__).resolve().parent
SCHEDULE = HERE / "exploratory-schedule.json"
LEDGER = development.RUNS / "exploratory-batch-ledger.json"


def checked_schedule():
    schedule_bytes = SCHEDULE.read_bytes()
    schedule = json.loads(schedule_bytes)
    attempts = schedule["attempts"]
    ids = [item["run_id"] for item in attempts]
    pairs = [(item["task_id"], item["condition"]) for item in attempts]
    if len(attempts) != 15 or len(set(ids)) != 15 or len(set(pairs)) != 15:
        raise ValueError("The schedule must contain 15 unique attempts and task-condition pairs.")
    if set(item["condition"] for item in attempts) != {"B", "D", "P"}:
        raise ValueError("The schedule must use conditions B, D, and P.")
    manifest = json.loads(development.TASK_MANIFEST.read_text(encoding="utf-8"))
    task_ids = {item["task_id"] for item in manifest["tasks"]}
    if set(pairs) != {(task_id, condition) for task_id in task_ids for condition in ("B", "D", "P")}:
        raise ValueError("The schedule does not cover all five selected tasks and three conditions.")
    verify_hashes(schedule)
    return schedule, trial.sha256(schedule_bytes)


def verify_hashes(schedule):
    files = {
        "runner_sha256": Path(development.__file__),
        "candidate_manifest_sha256": development.REPOSITORY / trial.PHASE2 / "interventions/candidate-manifest.json",
        "task_manifest_sha256": development.TASK_MANIFEST,
    }
    for key, path in files.items():
        if trial.sha256(path.read_bytes()) != schedule[key]:
            raise ValueError(f"The recorded {key} does not match the current file.")


def main():
    schedule, schedule_hash = checked_schedule()
    codex = shutil.which("codex")
    if not codex:
        raise ValueError("Codex CLI is not available on PATH.")
    development.RUNS.mkdir(parents=True, exist_ok=True)
    if LEDGER.exists() or any((development.RUNS / item["run_id"]).exists() for item in schedule["attempts"]):
        raise FileExistsError("A batch ledger or run directory already exists. Do not overwrite it.")
    ledger = {
        "purpose": schedule["purpose"],
        "schedule_sha256": schedule_hash,
        "started_utc": development.now_utc(),
        "status": "running",
        "attempts": [{**item, "status": "planned"} for item in schedule["attempts"]],
    }
    development.write_json(LEDGER, ledger)
    for item in ledger["attempts"]:
        try:
            verify_hashes(schedule)
            selected, task = development.read_task(item["task_id"])
            assets = trial.load_intervention_assets(development.REPOSITORY, item["condition"]) if item["condition"] != "B" else None
            item["status"] = "starting"
            development.write_json(LEDGER, ledger)
            print(json.dumps({"event": "starting", **item}), flush=True)
            record = development.run_attempt(development.RUNS, item["run_id"], item["task_id"], task,
                                             selected["prompt_sha256_utf8"], item["condition"], assets,
                                             codex, schedule["timeout_seconds"])
            item["status"] = record["status"]
            item["record"] = str(development.RUNS / item["run_id"] / "record.json")
            development.write_json(LEDGER, ledger)
            print(json.dumps({"event": "finished", **item}), flush=True)
            if record["status"] != "turn_completed_unassessed":
                ledger["status"] = "stopped_after_runner_failure"
                break
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
            item["status"] = "preflight_or_runner_error"
            item["error_type"] = type(exc).__name__
            ledger["status"] = "stopped_after_runner_failure"
            break
    else:
        ledger["status"] = "all_turns_completed_unassessed"
    ledger["ended_utc"] = development.now_utc()
    development.write_json(LEDGER, ledger)
    print(json.dumps({"event": "batch_stopped", "status": ledger["status"]}), flush=True)
    return 0 if ledger["status"] == "all_turns_completed_unassessed" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=development.sys.stderr)
        raise SystemExit(1)
