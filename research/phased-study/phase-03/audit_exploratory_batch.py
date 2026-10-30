#!/usr/bin/env python3
"""Audit preserved static entry points after the exploratory batch stops."""

import json
import subprocess
import sys

import audit_initial_state as audit
import run_codex_development as development
import run_exploratory_schedule as batch


LEDGER = development.RUNS / "exploratory-axe-ledger.json"
AUDIT_SHA256 = "786754f2cf78ab87bc48410ba07ee3469ff4b822d3e2655bbeafa416578c8240"
LOCK_SHA256 = "e4b8bc447d066ccae571bccf26581dba217fdb4095724c3d0f2e5a845337422e"


def main():
    if LEDGER.exists():
        raise FileExistsError("The exploratory audit ledger already exists.")
    schedule, schedule_hash = batch.checked_schedule()
    generation = json.loads(batch.LEDGER.read_text(encoding="utf-8"))
    if generation["status"] == "running":
        raise ValueError("Wait until the generation batch has stopped.")
    if generation["schedule_sha256"] != schedule_hash:
        raise ValueError("The generation ledger does not match this schedule.")
    if audit.sha256_file(audit.PILOT / "audit.js") != AUDIT_SHA256:
        raise ValueError("The browser audit script differs from the recorded pilot.")
    if audit.sha256_file(audit.PILOT / "package-lock.json") != LOCK_SHA256:
        raise ValueError("The browser audit dependencies differ from the recorded pilot.")
    if [(i["run_id"], i["task_id"], i["condition"]) for i in generation["attempts"]] != [
        (i["run_id"], i["task_id"], i["condition"]) for i in schedule["attempts"]
    ]:
        raise ValueError("The generation ledger has different attempts from the schedule.")

    ledger = {
        "purpose": "exploratory_initial_state_only",
        "schedule_sha256": schedule_hash,
        "started_utc": development.now_utc(),
        "status": "running",
        "attempts": [],
    }
    development.write_json(LEDGER, ledger)
    for item in generation["attempts"]:
        row = {"run_id": item["run_id"], "task_id": item["task_id"], "condition": item["condition"]}
        run_dir = development.RUNS / item["run_id"]
        if item["status"] != "turn_completed_unassessed":
            row["status"] = "not_assessed_generation_incomplete"
        else:
            try:
                record = audit.checked_workspace(run_dir)
                if record["run_id"] != item["run_id"] or record["task_id"] != item["task_id"] or record["condition"] != item["condition"]:
                    raise ValueError("The run record does not match the schedule.")
                if not (run_dir / "workspace/index.html").is_file():
                    row["status"] = "not_assessed_no_static_index"
                elif audit.needs_build(run_dir / "workspace/index.html"):
                    row["status"] = "not_assessed_source_requires_build"
                else:
                    process = subprocess.run([sys.executable, str(audit.__file__), "--run-id", item["run_id"]],
                                             capture_output=True, text=True, timeout=240, check=False)
                    metadata_path = run_dir / "initial-axe-metadata.json"
                    metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.is_file() else {}
                    row["status"] = metadata.get("status", "audit_failed")
                    if process.returncode == 0:
                        report = json.loads((run_dir / "initial-axe-report.json").read_text(encoding="utf-8"))
                        row["summary"] = report["summary"]
                        row["browser_version"] = report["browser_version"]
                        row["axe_engine"] = report["axe_engine"]
                        row["blocked_requests"] = len(report["blocked_requests"])
                        row["render_preflight"] = metadata.get("render_preflight")
                        row["report"] = str(run_dir / "initial-axe-report.json")
            except (OSError, ValueError, KeyError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
                row["status"] = "audit_failed"
                row["error_type"] = type(exc).__name__
        ledger["attempts"].append(row)
        development.write_json(LEDGER, ledger)
        print(json.dumps({"event": "audit_finished", "run_id": row["run_id"], "status": row["status"]}), flush=True)
    ledger["status"] = "finished_with_recorded_gaps" if any(row["status"] != "completed" for row in ledger["attempts"]) else "all_initial_scans_completed"
    ledger["ended_utc"] = development.now_utc()
    development.write_json(LEDGER, ledger)
    print(json.dumps({"event": "audit_batch_finished", "status": ledger["status"]}), flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
