#!/usr/bin/env python3
"""Check local selected-task hashes and six input assemblies without printing prompts."""
import hashlib
import json
import sys
from pathlib import Path

import prepare_condition

STUDY = Path(__file__).resolve().parents[3]
PROJECT = STUDY.parents[2]
SELECTION = PROJECT / "work/experiments/benchmarks/selected_arena_baselines/manifest.json"
PROMPTS = PROJECT / "work/.arena-research-cache/selected-baseline-prompts"


def main():
    try:
        selected = json.loads(SELECTION.read_text(encoding="utf-8"))
        if len(selected["tasks"]) != 5:
            raise ValueError("Expected five selected tasks.")
        results = []
        for task in selected["tasks"]:
            filename = task["local_filename"]
            if Path(filename).name != filename:
                raise ValueError("Task filename must not include a path.")
            raw = (PROMPTS / filename).read_bytes()
            task_hash = hashlib.sha256(raw).hexdigest()
            if task_hash != task["prompt_sha256_utf8"]:
                raise ValueError("A selected task differs from its source hash.")
            rows = {condition: prepare_condition.prepare(raw, task_hash, condition)
                    for condition in ("B", "D", "P", "S", "A", "X")}
            if rows["B"][0] != raw or any(rows[c][0] != rows["D"][0] for c in ("P", "S", "A", "X")):
                raise ValueError("Condition input assembly differs from the protocol.")
            results.append({"task_id": task["task_id"], "task_sha256": task_hash,
                            "b_message_sha256": rows["B"][1]["user_message_sha256"],
                            "shared_message_sha256": rows["D"][1]["user_message_sha256"],
                            "conditions_checked": list(rows), "sent_to_model": False})
        print(json.dumps({"status": "PASS", "tasks": results}, indent=2))
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
