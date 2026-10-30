#!/usr/bin/env python3
"""Record self-report parsing coverage after exploratory generation stops."""

import json
import subprocess
import sys
from pathlib import Path

import inspect_self_report as claims
import prepare_trial as trial
import run_codex_development as development
import run_exploratory_schedule as batch


LEDGER = development.RUNS / "exploratory-claim-ledger.json"


def main():
    if LEDGER.exists():
        raise FileExistsError("The exploratory claim ledger already exists.")
    schedule, schedule_hash = batch.checked_schedule()
    generation = json.loads(batch.LEDGER.read_text(encoding="utf-8"))
    if generation["status"] == "running":
        raise ValueError("Wait until the generation batch has stopped.")
    if generation["schedule_sha256"] != schedule_hash:
        raise ValueError("The generation ledger does not match this schedule.")
    if [(i["run_id"], i["task_id"], i["condition"]) for i in generation["attempts"]] != [
        (i["run_id"], i["task_id"], i["condition"]) for i in schedule["attempts"]
    ]:
        raise ValueError("The generation ledger has different attempts from the schedule.")
    ledger = {
        "purpose": "descriptive_model_claim_coverage_not_accuracy",
        "schedule_sha256": schedule_hash,
        "parser_sha256": trial.sha256(Path(claims.__file__).read_bytes()),
        "started_utc": development.now_utc(),
        "status": "running",
        "attempts": [],
    }
    development.write_json(LEDGER, ledger)
    for item in generation["attempts"]:
        row = {"run_id": item["run_id"], "task_id": item["task_id"], "condition": item["condition"]}
        if item["condition"] == "B":
            row["status"] = "report_not_requested"
        elif item["status"] != "turn_completed_unassessed":
            row["status"] = "not_assessed_generation_incomplete"
        else:
            run_dir = development.RUNS / item["run_id"]
            try:
                record = json.loads((run_dir / "record.json").read_text(encoding="utf-8"))
                if record["run_id"] != item["run_id"] or record["task_id"] != item["task_id"] or record["condition"] != item["condition"]:
                    raise ValueError("The run record does not match the schedule.")
                process = subprocess.run([sys.executable, claims.__file__, "--run-id", item["run_id"]],
                                         capture_output=True, text=True, timeout=30, check=False)
                row["status"] = "parser_failed" if process.returncode else "parsed"
                if process.returncode == 0:
                    result = json.loads((run_dir / "model-claim-coverage.json").read_text(encoding="utf-8"))
                    if result["report_present"]:
                        row["coverage"] = result["coverage"]
                    else:
                        row["status"] = "file_absent_chat_not_checked"
            except (OSError, ValueError, KeyError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
                row["status"] = "parser_failed"
                row["error_type"] = type(exc).__name__
        ledger["attempts"].append(row)
        development.write_json(LEDGER, ledger)
        print(json.dumps({"event": "claim_inspection_finished", "run_id": row["run_id"], "status": row["status"]}), flush=True)
    ledger["status"] = "finished"
    ledger["ended_utc"] = development.now_utc()
    development.write_json(LEDGER, ledger)
    print(json.dumps({"event": "claim_batch_finished", "status": ledger["status"]}), flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
