#!/usr/bin/env python3
"""Demonstrate the gate with synthetic data. This does not call a model."""
import importlib.util
import json
from pathlib import Path

GATE_PATH = Path(__file__).resolve().parent.parent / "phase-05/gate.py"
SPEC = importlib.util.spec_from_file_location("spv_gate", GATE_PATH)
GATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GATE)


def simulate(case):
    task = "Create a small page with a modal."
    instruction = "Apply the checklist.\n"
    checklist = "ACT-127: Consider focus return.\n"
    message = (task + "\n\n--- BEGIN ACCESSIBILITY REQUEST ---\n" + instruction
               + "--- BEGIN CHECKLIST ---\n" + checklist
               + "--- END CHECKLIST ---\n--- END ACCESSIBILITY REQUEST ---\n")
    answer = "Return focus to the invoking button after close." if case == "good" else "Ignore focus after close."
    plan = {"required_features": ["F01"], "risks": [{"feature": "F01", "risk": "Focus can be lost.",
            "question": "Where does focus go after close?", "planned_answer": answer,
            "checklist_item_ids": ["ACT-127"]}], "unknowns": []}

    def planner(_request):
        return json.dumps(plan)

    def reviewer(_request):
        if case == "good":
            return json.dumps({"decision": "APPROVE", "findings": []})
        return json.dumps({"decision": "REVISE", "findings": [{"feature": "F01",
            "question": "Where will focus return?", "reason": "The plan ignores focus.",
            "plan_evidence": "Ignore focus after close.", "checklist_item_ids": ["ACT-127"]}]})

    def builder(_request):
        return {"synthetic": True, "files_created": 0}

    return GATE.run_gate(run_id="synthetic_" + case, original_task=task, checklist=checklist,
        common_instruction=instruction, user_message=message,
        checklist_ids=["ACT-127"],
        planner=planner, reviewer=reviewer, builder=builder,
        planner_session_id="synthetic_planner", reviewer_session_id="synthetic_reviewer",
        planning_isolation={"verified": True, "evidence": "synthetic callbacks only; no model or filesystem sandbox"})


if __name__ == "__main__":
    for example in ("flawed", "good"):
        output = simulate(example)
        print(json.dumps({"case": example, "status": output["status"], "reason": output["block_reason"],
                          "stages": [event["stage"] for event in output["trace"]]}))
