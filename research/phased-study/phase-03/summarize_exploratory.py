#!/usr/bin/env python3
"""Summarize recorded exploratory attempts without treating gaps as zero findings."""

import json
import sys

import audit_exploratory_batch as audit_batch
import run_codex_development as development
import run_exploratory_schedule as batch


JSON_OUTPUT = development.RUNS / "exploratory-summary.json"
MARKDOWN_OUTPUT = development.RUNS / "exploratory-summary.md"


def summarize_row(generation, audit):
    row = {"run_id": generation["run_id"], "task_id": generation["task_id"],
           "condition": generation["condition"], "generation_status": generation["status"],
           "audit_status": audit.get("status", "not_assessed"), "axe": None}
    if audit.get("status") in {"completed", "completed_with_render_warnings"} and "summary" in audit:
        summary = audit["summary"]
        impact = summary["violations_by_impact"]
        row["axe"] = {
            "total_rules": summary["total_rules"], "total_nodes": summary["total_nodes"],
            "incomplete_rules": summary["incomplete_rules"],
            "nodes_by_impact": {level: impact.get(level, {}).get("nodes", 0)
                                for level in ("critical", "serious", "moderate", "minor", "unknown")},
            "blocked_requests": audit.get("blocked_requests"),
        }
    return row


def markdown(rows):
    lines = ["# Exploratory Codex batch: initial-state scan", "",
             "These are development observations, not final benchmark results.",
             "A dash means no comparable initial-state scan; it does not mean zero findings.",
             "Impact counts are axe-reported affected nodes, not distinct WCAG violations.",
             "Incomplete rules need review. A zero count does not establish accessibility.", "",
             "| Task | Condition | Generation | Initial scan | Critical | Serious | Moderate | Minor | Unknown impact | Incomplete rules |",
             "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for row in rows:
        values = ["-", "-", "-", "-", "-", "-"]
        if row["axe"] is not None:
            nodes = row["axe"]["nodes_by_impact"]
            values = [str(nodes[key]) for key in ("critical", "serious", "moderate", "minor", "unknown")]
            values.append(str(row["axe"]["incomplete_rules"]))
        lines.append("| " + " | ".join([row["task_id"], row["condition"], row["generation_status"],
                                         row["audit_status"], *values]) + " |")
    lines.extend(["", "Human review, required journeys, keyboard operation, and screen-reader behavior are not scored here.",
                  "The selected tasks were purposive. The design scheduled one exploratory attempt per condition and task.",
                  "The interrupted attempt remains recorded and is not replaced by a zero.", ""])
    return "\n".join(lines)


def main():
    if JSON_OUTPUT.exists() or MARKDOWN_OUTPUT.exists():
        raise FileExistsError("An exploratory summary already exists; do not overwrite it.")
    schedule, schedule_hash = batch.checked_schedule()
    generation = json.loads(batch.LEDGER.read_text(encoding="utf-8"))
    audit = json.loads(audit_batch.LEDGER.read_text(encoding="utf-8"))
    if generation["status"] == "running" or audit["status"] == "running":
        raise ValueError("Generation and initial scans must have stopped.")
    if generation["schedule_sha256"] != schedule_hash or audit["schedule_sha256"] != schedule_hash:
        raise ValueError("The ledgers do not match the schedule.")
    expected = [(i["run_id"], i["task_id"], i["condition"]) for i in schedule["attempts"]]
    for ledger in (generation, audit):
        actual = [(i["run_id"], i["task_id"], i["condition"]) for i in ledger["attempts"]]
        if actual != expected:
            raise ValueError("A ledger has different attempts from the schedule.")
    rows = [summarize_row(g, a) for g, a in zip(generation["attempts"], audit["attempts"])]
    rows.sort(key=lambda row: (row["task_id"], row["condition"]))
    result = {"purpose": "exploratory_initial_state_not_final_evaluation", "schedule_sha256": schedule_hash,
              "created_utc": development.now_utc(), "rows": rows}
    with JSON_OUTPUT.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    with MARKDOWN_OUTPUT.open("x", encoding="utf-8") as stream:
        stream.write(markdown(rows))
    print(json.dumps({"status": "created", "rows": len(rows), "markdown": str(MARKDOWN_OUTPUT)}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
