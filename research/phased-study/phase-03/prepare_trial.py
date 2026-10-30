#!/usr/bin/env python3
"""Check B, D, and P input assembly without submitting or printing task text."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[3]
PHASE2 = Path("research/phased-study/phase-02")
PREFIX = b"\n\n--- BEGIN ACCESSIBILITY REQUEST ---\n"
CHECKLIST_START = b"--- BEGIN CHECKLIST ---\n"
SUFFIX = b"--- END CHECKLIST ---\n--- END ACCESSIBILITY REQUEST ---\n"
CHECKLIST_PATH = "research/accessibility/master-action-checklist.md"
INSTRUCTION_PATH = "research/phased-study/phase-02/interventions/checklist-instruction.txt"
GUIDANCE_PATH = "research/phased-study/phase-02/interventions/prompt-guidance.txt"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def checked_record(repo, records, relative_path):
    """Read a file only after checking its manifest path, length, and hash."""
    matches = [entry for entry in records if entry["path_from_repo_root"] == relative_path]
    if len(matches) != 1:
        raise ValueError(f"Expected one manifest record for {relative_path}.")
    root = repo.resolve()
    path = (root / relative_path).resolve()
    if not path.is_relative_to(root):
        raise ValueError("A manifest path is outside the study repository.")
    data = path.read_bytes()
    expected = matches[0]
    if len(data) != expected["bytes"] or sha256(data) != expected["sha256"]:
        raise ValueError(f"File differs from its recorded hash: {relative_path}.")
    return data


def load_intervention_assets(repo, condition):
    """Read the approved checklist and applicable candidate guidance."""
    if condition not in ("D", "P"):
        raise ValueError("Intervention assets apply to D or P only.")
    approval_path = repo / PHASE2 / "checklist-approval.json"
    manifest_path = repo / PHASE2 / "interventions/candidate-manifest.json"
    approval_bytes = approval_path.read_bytes()
    manifest_bytes = manifest_path.read_bytes()
    approval = json.loads(approval_bytes)
    manifest = json.loads(manifest_bytes)
    if approval["decision"] != "approved_by_researcher":
        raise ValueError("The checklist approval record is missing.")
    if approval["checklist_version"] != "0.2.0" or manifest["checklist_version"] != "0.2.0":
        raise ValueError("The checklist version differs from the approval.")

    checklist = checked_record(repo, approval["files"], CHECKLIST_PATH)
    if checklist != checked_record(repo, manifest["files"], CHECKLIST_PATH):
        raise ValueError("The candidate checklist differs from the approved file.")
    instruction = checked_record(repo, manifest["files"], INSTRUCTION_PATH)
    if not checklist.endswith(b"\n") or not instruction.endswith(b"\n"):
        raise ValueError("The checklist and instruction must end with a newline.")

    guidance = None
    if condition == "P":
        guidance = checked_record(repo, manifest["files"], GUIDANCE_PATH)
    return {
        "checklist": checklist,
        "instruction": instruction,
        "guidance": guidance,
        "approval_sha256": sha256(approval_bytes),
        "candidate_manifest_sha256": sha256(manifest_bytes),
        "candidate_revision": manifest.get("candidate_revision", "unknown"),
        "candidate_status": manifest.get("status", "unknown"),
    }


def prepare(task, expected_sha256, condition, assets=None):
    """Return the assembled user message and metadata; no network activity occurs."""
    if condition not in ("B", "D", "P"):
        raise ValueError("Condition must be B, D, or P.")
    if not task:
        raise ValueError("The task input is empty.")
    if not re.fullmatch(r"[0-9a-fA-F]{64}", expected_sha256):
        raise ValueError("The expected task SHA-256 must contain 64 hexadecimal characters.")
    if sha256(task) != expected_sha256.lower():
        raise ValueError("The task bytes do not match the expected SHA-256.")
    try:
        task.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("The task is not valid UTF-8.") from exc

    if condition == "B":
        return task, {"checklist_added": False, "prompt_guidance_sha256": None}
    if assets is None:
        raise ValueError("D and P require the approved checklist assets.")
    if condition == "P" and assets["guidance"] is None:
        raise ValueError("P requires a prompt-guidance file.")
    message = task + PREFIX + assets["instruction"] + CHECKLIST_START + assets["checklist"] + SUFFIX
    return message, {
        "checklist_added": True,
        "checklist_version": "0.2.0",
        "checklist_sha256": sha256(assets["checklist"]),
        "checklist_instruction_sha256": sha256(assets["instruction"]),
        "prompt_guidance_sha256": sha256(assets["guidance"]) if condition == "P" else None,
        "candidate_manifest_sha256": assets["candidate_manifest_sha256"],
        "candidate_revision": assets["candidate_revision"],
        "candidate_status": assets["candidate_status"],
        "approval_record_sha256": assets["approval_sha256"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-file", type=Path, required=True)
    parser.add_argument("--expected-task-sha256", required=True)
    parser.add_argument("--condition", choices=("B", "D", "P"), required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args(argv)
    for value in (args.task_id, args.run_id):
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", value):
            raise ValueError("Task and run IDs must use letters, numbers, underscores, or hyphens.")
    task = args.task_file.read_bytes()
    assets = load_intervention_assets(REPOSITORY, args.condition) if args.condition != "B" else None
    message, metadata = prepare(task, args.expected_task_sha256, args.condition, assets)
    result = {
        "status": "prepared_in_memory_only",
        "sent_to_model": False,
        "task_id": args.task_id,
        "run_id": args.run_id,
        "condition": args.condition,
        "task_sha256": sha256(task),
        "task_bytes": len(task),
        "user_message_sha256": sha256(message),
        "user_message_bytes": len(message),
        "metadata": metadata,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
