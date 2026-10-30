#!/usr/bin/env python3
"""Verify local provenance and artifact hashes after exploratory generation."""

import json
import sys

import prepare_trial as trial
import run_codex_development as development
import run_exploratory_schedule as batch


OUTPUT = development.RUNS / "exploratory-validation.json"


def record_problems(item, record, task, expected_task_hash, assets, runner_hash):
    problems = []
    for field in ("run_id", "task_id", "condition"):
        if record.get(field) != item[field]:
            problems.append(f"{field}_mismatch")
    if record.get("status") != "turn_completed_unassessed":
        problems.append("generation_not_completed")
        return problems
    message, metadata = trial.prepare(task, expected_task_hash, item["condition"], assets)
    if record.get("task_sha256") != trial.sha256(task):
        problems.append("task_hash_mismatch")
    if record.get("user_message_sha256") != trial.sha256(message) or record.get("user_message_bytes") != len(message):
        problems.append("local_message_mismatch")
    if record.get("input_metadata") != metadata:
        problems.append("input_metadata_mismatch")
    if record.get("runner_sha256") != runner_hash:
        problems.append("runner_hash_mismatch")
    if record.get("requested_model") != development.DEFAULT_MODEL or record.get("requested_reasoning_effort") != "high":
        problems.append("model_configuration_mismatch")
    if record.get("requested_subagents") != "disabled":
        problems.append("subagent_setting_mismatch")
    if record.get("requested_sandbox") != "benchmark profile: workspace write, minimal and runtime read, other root denied":
        problems.append("sandbox_profile_mismatch")
    _, roots = development.isolation_config()
    if record.get("requested_runtime_read_roots") != roots:
        problems.append("runtime_roots_mismatch")
    if record.get("timeout_seconds") != development.DEFAULT_TIMEOUT_SECONDS:
        problems.append("timeout_mismatch")
    initial_files = record.get("initial_workspace", {}).get("files", [])
    if item["condition"] == "P":
        expected_initial = [{"path": "AGENTS.md", "bytes": len(assets["guidance"]),
                             "sha256": trial.sha256(assets["guidance"])}]
    else:
        expected_initial = []
    if initial_files != expected_initial:
        problems.append("initial_workspace_mismatch")
    run_dir = development.RUNS / item["run_id"]
    if development.artifact_manifest(run_dir / "workspace") != record.get("final_workspace"):
        problems.append("artifact_manifest_mismatch")
    return problems


def main():
    if OUTPUT.exists():
        raise FileExistsError("The exploratory validation record already exists.")
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
    rows = []
    for item in generation["attempts"]:
        row = {"run_id": item["run_id"], "task_id": item["task_id"], "condition": item["condition"]}
        if item["status"] != "turn_completed_unassessed":
            row["status"] = "not_completed"
            row["problems"] = [item["status"]]
        else:
            try:
                selected, task = development.read_task(item["task_id"])
                assets = trial.load_intervention_assets(development.REPOSITORY, item["condition"]) if item["condition"] != "B" else None
                record = json.loads((development.RUNS / item["run_id"] / "record.json").read_text(encoding="utf-8"))
                row["problems"] = record_problems(item, record, task, selected["prompt_sha256_utf8"],
                                                  assets, schedule["runner_sha256"])
                row["status"] = "local_checks_passed" if not row["problems"] else "local_checks_failed"
            except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
                row["status"] = "local_checks_failed"
                row["problems"] = [type(exc).__name__]
        rows.append(row)
    result = {
        "purpose": "local_provenance_checks_not_accessibility_evaluation",
        "schedule_sha256": schedule_hash,
        "checked_utc": development.now_utc(),
        "attempts": rows,
        "limitations": [
            "The service-side message and hidden instructions are not observed.",
            "The recorded artifact manifest excludes .git and node_modules.",
            "These checks do not establish task completion or accessibility."
        ],
    }
    development.write_json(OUTPUT, result)
    print(json.dumps({"status": "all_local_checks_passed" if all(r["status"] == "local_checks_passed" for r in rows)
                      else "checks_have_failures_or_incomplete_attempts",
                      "attempts": len(rows), "record": str(OUTPUT)}, indent=2))
    return 0 if all(row["status"] == "local_checks_passed" for row in rows) else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
