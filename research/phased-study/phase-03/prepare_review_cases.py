#!/usr/bin/env python3
"""Make condition-masked local copies of completed static exploratory pages."""

import json
import random
import shutil
import sys
from pathlib import Path

import audit_initial_state as audit
import run_codex_development as development
import run_exploratory_schedule as batch


REVIEW_ROOT = development.REPOSITORY / "local/phase-03-review"
MASK_SEED = 271828
PRIVATE_SIDECARS = {"agents.md", "spv-plan.md", "accessibility-self-report.md"}


def copy_site(run_dir, target):
    record, _ = audit.checked_index(run_dir)
    source = (run_dir / "workspace").resolve()
    target.mkdir(parents=True, exist_ok=False)
    included = []
    excluded = []
    for item in record["final_workspace"]["files"]:
        relative = Path(item["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("The recorded artifact path is not relative.")
        if relative.name.lower() in PRIVATE_SIDECARS:
            excluded.append(relative.as_posix())
            continue
        src = source / relative
        if src.is_symlink() or not src.resolve().is_relative_to(source):
            raise ValueError("An artifact path is a link or outside the workspace.")
        if audit.sha256_file(src) != item["sha256"]:
            raise ValueError("An artifact file changed after generation.")
        dst = target / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        if audit.sha256_file(dst) != item["sha256"]:
            raise ValueError("The review copy does not match the source artifact.")
        included.append(item)
    return {"included_files": included, "excluded_sidecars": excluded,
            "excluded_directories": record["final_workspace"]["excluded_directories"]}


def main():
    if REVIEW_ROOT.exists():
        raise FileExistsError("The review-case directory already exists; do not overwrite it.")
    schedule, schedule_hash = batch.checked_schedule()
    ledger = json.loads(batch.LEDGER.read_text(encoding="utf-8"))
    if ledger["status"] == "running":
        raise ValueError("Wait until the generation batch has stopped.")
    if ledger["schedule_sha256"] != schedule_hash:
        raise ValueError("The generation ledger does not match the schedule.")
    expected = [(i["run_id"], i["task_id"], i["condition"]) for i in schedule["attempts"]]
    actual = [(i["run_id"], i["task_id"], i["condition"]) for i in ledger["attempts"]]
    if expected != actual:
        raise ValueError("The generation ledger has different attempts from the schedule.")
    shuffled = list(ledger["attempts"])
    random.Random(MASK_SEED).shuffle(shuffled)
    REVIEW_ROOT.mkdir(parents=True, exist_ok=False)
    mapping = {
        "purpose": "condition_masked_exploratory_manual_review",
        "schedule_sha256": schedule_hash,
        "mask_seed": MASK_SEED,
        "created_utc": development.now_utc(),
        "status": "preparing",
        "limitations": [
            "Condition labels are hidden in the review view; blinding is not guaranteed.",
            "The researcher already knows the tasks and saw the first pilot results.",
            "Project instructions and model self-reports are excluded from review copies.",
            "Excluded files or dependencies can affect behavior; record such cases as unassessable."
        ],
        "cases": [],
    }
    development.write_json(REVIEW_ROOT / "private-mapping.json", mapping)
    for index, item in enumerate(shuffled, 1):
        case = {"case_id": f"CASE-{index:02d}", "run_id": item["run_id"],
                "task_id": item["task_id"], "condition": item["condition"]}
        run_dir = development.RUNS / item["run_id"]
        if item["status"] != "turn_completed_unassessed":
            case["status"] = "generation_incomplete"
        else:
            try:
                record = audit.checked_workspace(run_dir)
                if any(record.get(key) != item[key] for key in ("run_id", "task_id", "condition")):
                    raise ValueError("The run record does not match the schedule.")
                if not (run_dir / "workspace/index.html").is_file():
                    case["status"] = "no_static_index"
                elif audit.needs_build(run_dir / "workspace/index.html"):
                    case["status"] = "source_requires_build"
                else:
                    case.update(copy_site(run_dir, REVIEW_ROOT / "cases" / case["case_id"] / "site"))
                    case["status"] = "ready_static_copy"
            except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
                case["status"] = "copy_failed"
                case["error_type"] = type(exc).__name__
        mapping["cases"].append(case)
        development.write_json(REVIEW_ROOT / "private-mapping.json", mapping)
    mapping["status"] = "prepared_with_gaps" if any(c["status"] != "ready_static_copy" for c in mapping["cases"]) else "all_static_copies_ready"
    mapping["finished_utc"] = development.now_utc()
    development.write_json(REVIEW_ROOT / "private-mapping.json", mapping)
    print(json.dumps({"status": mapping["status"], "cases": len(mapping["cases"]),
                      "ready": sum(c["status"] == "ready_static_copy" for c in mapping["cases"])}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
