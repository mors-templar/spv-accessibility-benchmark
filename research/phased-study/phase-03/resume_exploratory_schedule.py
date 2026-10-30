#!/usr/bin/env python3
"""Continue only untouched scheduled attempts after a recorded runner stop."""

import json
import shutil
import sys

import prepare_trial as trial
import run_codex_development as development
import run_exploratory_schedule as batch


def checked_ledger(schedule, schedule_hash):
    ledger = json.loads(batch.LEDGER.read_text(encoding="utf-8"))
    if ledger["status"] != "stopped_after_runner_failure":
        raise ValueError("Only a batch stopped after a runner failure can be continued.")
    if ledger["schedule_sha256"] != schedule_hash:
        raise ValueError("The ledger does not match the frozen schedule.")
    expected = [(i["run_id"], i["task_id"], i["condition"]) for i in schedule["attempts"]]
    actual = [(i["run_id"], i["task_id"], i["condition"]) for i in ledger["attempts"]]
    if expected != actual:
        raise ValueError("The ledger attempts differ from the frozen schedule.")
    for item in ledger["attempts"]:
        run_dir = development.RUNS / item["run_id"]
        if item["status"] == "planned":
            if run_dir.exists():
                raise ValueError("A planned attempt already has a directory; do not overwrite it.")
        elif item["status"] == "starting":
            raise ValueError("A starting attempt needs manual investigation before continuing.")
        elif not (run_dir / "record.json").is_file():
            raise ValueError("An attempted run is missing its record.")
        else:
            record = json.loads((run_dir / "record.json").read_text(encoding="utf-8"))
            if any(record.get(key) != item[key] for key in ("run_id", "task_id", "condition", "status")):
                raise ValueError("An attempted run does not match its ledger record.")
    return ledger


def main():
    schedule, schedule_hash = batch.checked_schedule()
    ledger = checked_ledger(schedule, schedule_hash)
    codex = shutil.which("codex")
    if not codex:
        raise ValueError("Codex CLI is not available on PATH.")
    pending = [item for item in ledger["attempts"] if item["status"] == "planned"]
    if not pending:
        raise ValueError("There are no untouched planned attempts to continue.")
    resume = {"started_utc": development.now_utc(), "planned_count": len(pending), "status": "running"}
    ledger.setdefault("resumptions", []).append(resume)
    ledger["status"] = "running"
    development.write_json(batch.LEDGER, ledger)
    for item in pending:
        try:
            batch.verify_hashes(schedule)
            selected, task = development.read_task(item["task_id"])
            assets = trial.load_intervention_assets(development.REPOSITORY, item["condition"]) if item["condition"] != "B" else None
            item["status"] = "starting"
            development.write_json(batch.LEDGER, ledger)
            print(json.dumps({"event": "starting", **item}), flush=True)
            record = development.run_attempt(development.RUNS, item["run_id"], item["task_id"], task,
                                             selected["prompt_sha256_utf8"], item["condition"], assets,
                                             codex, schedule["timeout_seconds"])
            item["status"] = record["status"]
            item["record"] = str(development.RUNS / item["run_id"] / "record.json")
            development.write_json(batch.LEDGER, ledger)
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
        ledger["status"] = "all_attempts_accounted_for_with_failures"
    resume["status"] = ledger["status"]
    resume["ended_utc"] = development.now_utc()
    ledger["ended_utc"] = resume["ended_utc"]
    development.write_json(batch.LEDGER, ledger)
    print(json.dumps({"event": "resume_stopped", "status": ledger["status"]}), flush=True)
    return 0 if ledger["status"] == "all_attempts_accounted_for_with_failures" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
