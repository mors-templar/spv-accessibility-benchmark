#!/usr/bin/env python3
"""Count recognizable checklist statuses in a model report without assessing truth."""

import argparse
import collections
import json
import re
from pathlib import Path

import prepare_trial as trial
import run_codex_development as development


TABLE = re.compile(r"^\s*\|\s*(ACT-\d{3})\s*\|\s*([^|]+)\|(?:\s*([^|]+)\|)?", re.IGNORECASE)
BULLET = re.compile(r"^\s*[-*]\s*(?:\*\*|__)?(ACT-\d{3})(?:\s*\[([RGP])\])?\s*(?::|[-—–])\s*(.*)$",
                    re.IGNORECASE)
ALLOWED = {
    "R": {"pass", "fail", "not applicable", "unassessed"},
    "G": {"pass", "fail", "not applicable", "unassessed"},
    "P": {"observed", "researcher responsibility", "unassessed"},
}
STATUS = re.compile(
    r"^(?:\*\*|__)?(researcher responsibility|not applicable|not_applicable|unassessed|observed|pass|fail)"
    r"(?:\*\*|__)?(?=\s|[—–:;,.]|$)", re.IGNORECASE,
)


def approved_checklist(record):
    approval_bytes = (development.REPOSITORY / trial.PHASE2 / "checklist-approval.json").read_bytes()
    approval = json.loads(approval_bytes)
    if approval.get("decision") != "approved_by_researcher" or approval.get("checklist_version") != "0.2.0":
        raise ValueError("The checklist approval record is not valid for this parser.")
    if record.get("condition") in {"D", "P"} and record.get("input_metadata", {}).get("approval_record_sha256") != trial.sha256(approval_bytes):
        raise ValueError("The checklist approval record differs from the generation record.")
    return trial.checked_record(development.REPOSITORY, approval["files"], "research/accessibility/action-checklist.json")


def parse_claims(report, items):
    expected = {item["id"]: item["basis"] for item in items}
    if len(expected) != len(items):
        raise ValueError("Checklist IDs must be unique.")
    entries = collections.defaultdict(list)
    for line in report.splitlines():
        table = TABLE.match(line)
        bullet = BULLET.match(line) if not table else None
        if table:
            item_id, first, second = table.groups()
            claimed_basis = first.strip().strip("*_").upper()
            if claimed_basis in ALLOWED and second is not None:
                value = second
            else:
                claimed_basis = None
                value = first
        elif bullet:
            item_id, claimed_basis, value = bullet.groups()
            claimed_basis = claimed_basis.upper() if claimed_basis else None
        else:
            continue
        item_id = item_id.upper()
        value = value.strip()
        found = STATUS.match(value)
        normalized = found.group(1).lower().replace("_", " ") if found else None
        entries[item_id].append((normalized, claimed_basis))

    counts = {basis: collections.Counter() for basis in ALLOWED}
    missing = []
    duplicate = []
    unrecognized = []
    invalid_for_basis = []
    basis_mismatch = []
    for item_id, basis in expected.items():
        values = entries.get(item_id, [])
        if not values:
            missing.append(item_id)
        elif len(values) != 1:
            duplicate.append(item_id)
        elif values[0][1] is not None and values[0][1] != basis:
            basis_mismatch.append(item_id)
        elif values[0][0] is None:
            unrecognized.append(item_id)
        elif values[0][0] not in ALLOWED[basis]:
            invalid_for_basis.append(item_id)
        else:
            counts[basis][values[0][0]] += 1
    return {
        "expected_items": len(expected),
        "recognized_unique_items": sum(sum(values.values()) for values in counts.values()),
        "status_counts_by_basis": {basis: dict(sorted(values.items())) for basis, values in counts.items()},
        "missing_ids": missing,
        "duplicate_ids": duplicate,
        "unrecognized_status_ids": unrecognized,
        "invalid_status_for_basis_ids": invalid_for_basis,
        "basis_mismatch_ids": basis_mismatch,
        "extra_ids": sorted(set(entries) - set(expected)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", args.run_id):
        raise ValueError("Run ID must use letters, numbers, underscores, or hyphens.")
    run_dir = development.RUNS / args.run_id
    record = json.loads((run_dir / "record.json").read_text(encoding="utf-8"))
    if record["status"] != "turn_completed_unassessed":
        raise ValueError("The generation turn did not complete.")
    if development.artifact_manifest(run_dir / "workspace") != record["final_workspace"]:
        raise ValueError("The workspace differs from its recorded artifact manifest.")
    report = run_dir / "workspace/accessibility-self-report.md"
    output = run_dir / "model-claim-coverage-v2.json"
    if output.exists():
        raise FileExistsError("The claim coverage record already exists.")
    checklist = approved_checklist(record)
    items = json.loads(checklist)["items"]
    result = {
        "run_id": args.run_id,
        "condition": record["condition"],
        "purpose": "descriptive_parser_coverage_not_claim_accuracy",
        "parser_version": "0.2.0",
        "parser_sha256": trial.sha256(Path(__file__).read_bytes()),
        "checklist_json_sha256": trial.sha256(checklist),
        "report_present": report.is_file(),
        "limitations": [
            "Only recognizable table and bullet formats are parsed.",
            "Counts are model claims and do not establish accessibility or correctness.",
            "A missing file does not rule out a report in the model response."
        ],
    }
    if report.is_file():
        report_bytes = report.read_bytes()
        result["report_sha256"] = trial.sha256(report_bytes)
        result["coverage"] = parse_claims(report_bytes.decode("utf-8"), items)
    development.write_json(output, result)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=development.sys.stderr)
        raise SystemExit(1)
