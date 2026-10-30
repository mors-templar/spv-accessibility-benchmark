#!/usr/bin/env python3
"""Prepare and fingerprint six study conditions without making a model call."""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
PHASES = REPO / "research/phased-study"
MANIFEST = PHASES / "phase-06/package-manifest.json"
PACKAGE_FILES = {
    "research/accessibility/master-action-checklist.md",
    "research/accessibility/action-checklist.json",
    "research/phased-study/phase-02/checklist-approval.json",
    "research/phased-study/phase-02/interventions/candidate-manifest.json",
    "research/phased-study/phase-02/interventions/checklist-instruction.txt",
    "research/phased-study/phase-02/interventions/prompt-guidance.txt",
    "research/phased-study/phase-03/prepare_trial.py",
    "research/phased-study/phase-04/prompt-guidance.txt",
    "research/phased-study/phase-04/tool_adapter.py",
    "research/phased-study/phase-04/spv-accessibility/SKILL.md",
    "research/phased-study/phase-04/spv-accessibility/scripts/verify_plan.py",
    "research/phased-study/phase-04/spv-accessibility/references/verify-plan-request.schema.json",
    "research/phased-study/phase-04/spv-accessibility/references/verify-plan-response.schema.json",
    "research/phased-study/phase-04/spv-accessibility/references/openai-responses-function.json",
    "research/phased-study/phase-05/gate.py",
    "research/phased-study/phase-05/reviewer/plan-instruction.txt",
    "research/phased-study/phase-05/reviewer/reviewer-instruction.txt",
    "research/phased-study/phase-05/reviewer/approval-continuation.txt",
    "research/phased-study/phase-05/reviewer/plan.schema.json",
    "research/phased-study/phase-05/reviewer/decision.schema.json",
    "research/phased-study/phase-06/prepare_condition.py",
    "research/phased-study/phase-06/run_codex_review.py",
    "research/phased-study/phase-06/isolation-preflight-template.json",
}
SPEC = importlib.util.spec_from_file_location("phase03_prepare_trial", PHASES / "phase-03/prepare_trial.py")
TRIAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TRIAL)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_package(repo=REPO):
    manifest_path = repo / "research/phased-study/phase-06/package-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["status"] != "development_not_frozen":
        raise ValueError("Unexpected intervention package status.")
    seen = set()
    for record in manifest["files"]:
        name = record["path_from_repo_root"]
        if name in seen:
            raise ValueError("Duplicate package manifest path.")
        seen.add(name)
        path = (repo / name).resolve()
        if not path.is_relative_to(repo.resolve()):
            raise ValueError("Package manifest path is outside the repository.")
        data = path.read_bytes()
        if len(data) != record["bytes"] or digest(data) != record["sha256"]:
            raise ValueError("Package file differs from its recorded bytes: " + name)
    if seen != PACKAGE_FILES:
        raise ValueError("The package manifest does not list the expected files.")
    return manifest


def prepare(task_bytes, expected_sha256, condition, repo=REPO):
    """Return exact user-message bytes and metadata for a local runner adapter."""
    if condition not in ("B", "D", "P", "S", "A", "X"):
        raise ValueError("Condition must be B, D, P, S, A, or X.")
    manifest = verify_package(repo)
    assets = None
    if condition != "B":
        assets = TRIAL.load_intervention_assets(repo, "P" if condition in ("P", "X") else "D")
    message, meta = TRIAL.prepare(task_bytes, expected_sha256, "B" if condition == "B" else "D", assets)
    package = []
    if condition in ("P", "X"):
        guidance = (repo / "research/phased-study/phase-04/prompt-guidance.txt").read_bytes()
        if guidance != assets["guidance"]:
            raise ValueError("Development guidance differs from the Phase 2 candidate.")
        meta["prompt_guidance_sha256"] = digest(guidance)
        package.append("prompt_guidance")
    if condition in ("S", "X"):
        package.extend(["spv_accessibility_skill", "advisory_diagnostic"])
    if condition in ("A", "X"):
        package.extend(["independent_reviewer", "host_gate"])
    metadata = {
        "condition": condition, "package": package, "package_version": manifest["version"],
        "package_status": manifest["status"], "original_task_sha256": digest(task_bytes),
        "package_manifest_sha256": digest((repo / "research/phased-study/phase-06/package-manifest.json").read_bytes()),
        "original_task_bytes": len(task_bytes), "user_message_sha256": digest(message),
        "user_message_bytes": len(message), "shared_checklist_details": meta,
        "prompt_guidance_sha256": digest(guidance) if condition in ("P", "X") else None,
        "sent_to_model": False,
    }
    return message, metadata


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-file", required=True, type=Path)
    parser.add_argument("--expected-task-sha256", required=True)
    parser.add_argument("--condition", required=True, choices=("B", "D", "P", "S", "A", "X"))
    args = parser.parse_args(argv)
    try:
        _, metadata = prepare(args.task_file.read_bytes(), args.expected_task_sha256, args.condition)
        print(json.dumps(metadata, indent=2, ensure_ascii=False))
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
