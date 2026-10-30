"""Provider-neutral host orchestration for an independently reviewed plan.

The host orders callbacks. The caller must supply and verify operating-system or
runner isolation. Same-process callbacks are not a security boundary.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_RESPONSE_BYTES = 500_000
MAX_ITEMS = 1000
ID_PATTERN = re.compile(r"[A-Za-z0-9_-]{1,80}\Z")
UNKNOWN_ANSWER = re.compile(r"\s*(unknown|unresolved|tbd|not yet known|unsure)\s*[.!]?\s*\Z", re.I)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def _parse(text):
    if not isinstance(text, str):
        raise ValueError("The response must be JSON text.")
    if len(text.encode("utf-8")) > MAX_RESPONSE_BYTES:
        raise ValueError("The response exceeds the size limit.")
    def reject_constant(_):
        raise ValueError("Invalid JSON constant.")
    return json.loads(text, object_pairs_hook=_unique_object, parse_constant=reject_constant)


def _object(value, keys, name):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError(name + " has missing or unexpected fields.")


def _string(value, name):
    if not isinstance(value, str) or not value.strip() or len(value) > 20_000:
        raise ValueError(name + " must be a nonempty string of at most 20000 characters.")
    return value


def _document(value, name):
    if not isinstance(value, str) or not value.strip() or len(value.encode("utf-8")) > 1_000_000:
        raise ValueError(name + " must be a nonempty UTF-8 document of at most 1000000 bytes.")
    return value


def _list(value, name):
    if not isinstance(value, list) or len(value) > MAX_ITEMS:
        raise ValueError(name + " must be an array of at most 1000 entries.")
    return value


def _identifier(value, name):
    _string(value, name)
    if not ID_PATTERN.fullmatch(value):
        raise ValueError(name + " has an invalid identifier.")
    return value


def _ids(value, valid_ids, name, allow_empty=False):
    values = _list(value, name)
    if not values and not allow_empty:
        raise ValueError(name + " must include a checklist ID.")
    for item in values:
        _identifier(item, name)
        if item not in valid_ids:
            raise ValueError(name + " contains an unknown checklist ID.")
    if len(set(values)) != len(values):
        raise ValueError(name + " contains duplicate checklist IDs.")


def validate_plan(plan, valid_checklist_ids):
    """Check structure, the plan's own feature coverage, and checklist references."""
    _object(plan, ("required_features", "risks", "unknowns"), "plan")
    features = _list(plan["required_features"], "required_features")
    if not features:
        raise ValueError("The plan has no required features.")
    for feature in features:
        _string(feature, "planned feature")
    if len(set(features)) != len(features):
        raise ValueError("The plan repeats a feature ID.")
    feature_ids = set(features)
    risks = _list(plan["risks"], "risks")
    covered = set()
    for risk in risks:
        _object(risk, ("feature", "risk", "question", "planned_answer", "checklist_item_ids"), "risk")
        feature = _string(risk["feature"], "risk feature")
        if feature not in feature_ids:
            raise ValueError("A risk refers to a feature outside the plan's list.")
        covered.add(feature)
        for key in ("risk", "question", "planned_answer"):
            _string(risk[key], "risk " + key)
        _ids(risk["checklist_item_ids"], valid_checklist_ids, "risk checklist IDs")
    if covered != feature_ids:
        raise ValueError("Each listed feature needs a risk and question.")
    for item in _list(plan["unknowns"], "unknowns"):
        _string(item, "unknown")


def validate_decision(decision, valid_checklist_ids):
    _object(decision, ("decision", "findings"), "review decision")
    verdict = decision["decision"]
    if verdict not in ("APPROVE", "REVISE", "INSUFFICIENT_EVIDENCE"):
        raise ValueError("Unrecognized reviewer decision.")
    findings = _list(decision["findings"], "findings")
    if verdict == "APPROVE" and findings:
        raise ValueError("An approval must have no findings.")
    if verdict != "APPROVE" and not findings:
        raise ValueError("A non-approval needs at least one finding.")
    for finding in findings:
        _object(finding, ("feature", "question", "reason", "plan_evidence", "checklist_item_ids"), "finding")
        for key in ("feature", "question", "reason", "plan_evidence"):
            _string(finding[key], "finding " + key)
        _ids(finding["checklist_item_ids"], valid_checklist_ids, "finding checklist IDs", allow_empty=True)


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _text_asset(name):
    return (HERE / "reviewer" / name).read_text(encoding="utf-8")


def _schema_asset(name):
    return json.loads(_text_asset(name))


def run_gate(*, run_id, original_task, checklist, common_instruction, user_message,
             checklist_ids, planner, reviewer, builder, planner_session_id,
             reviewer_session_id, planning_isolation, max_revisions=2):
    """Execute bounded planning and review before invoking the build callback.

    Callbacks receive a dict. Planner and reviewer return JSON text. Builder
    returns JSON-compatible metadata. Save the returned trace privately.
    """
    _identifier(run_id, "run ID")
    _document(original_task, "original task")
    _document(checklist, "checklist")
    _document(common_instruction, "common instruction")
    _document(user_message, "user message")
    if not checklist.endswith("\n") or not common_instruction.endswith("\n"):
        raise ValueError("The checklist and common instruction must end with a newline.")
    expected_message = (original_task + "\n\n--- BEGIN ACCESSIBILITY REQUEST ---\n" + common_instruction
                        + "--- BEGIN CHECKLIST ---\n" + checklist
                        + "--- END CHECKLIST ---\n--- END ACCESSIBILITY REQUEST ---\n")
    if user_message != expected_message:
        raise ValueError("The shared message differs from the specified D assembly.")
    ids = _list(checklist_ids, "checklist_ids")
    for item in ids:
        _identifier(item, "checklist ID")
    if not ids or len(set(ids)) != len(ids):
        raise ValueError("Checklist IDs must be nonempty and unique.")
    valid_ids = set(ids)
    _identifier(planner_session_id, "planner session ID")
    _identifier(reviewer_session_id, "reviewer session ID")
    if planner_session_id == reviewer_session_id or planner is reviewer:
        raise ValueError("Planning and review require separate sessions and callbacks.")
    if type(max_revisions) is not int or not 0 <= max_revisions <= 5:
        raise ValueError("max_revisions must be an integer from zero to five.")
    if not all(callable(cb) for cb in (planner, reviewer, builder)):
        raise ValueError("Planner, reviewer, and builder must be callable.")
    _object(planning_isolation, ("verified", "evidence"), "planning isolation")
    if type(planning_isolation["verified"]) is not bool:
        raise ValueError("Planning isolation verified must be a boolean.")
    _string(planning_isolation["evidence"], "isolation evidence")

    result = {
        "run_id": run_id, "status": "BLOCKED", "block_reason": None,
        "original_task_sha256": sha256(original_task),
        "checklist_sha256": sha256(checklist), "user_message_sha256": sha256(user_message),
        "planner_session_id": planner_session_id, "reviewer_session_id": reviewer_session_id,
        "planning_isolation": copy.deepcopy(planning_isolation),
        "max_revisions": max_revisions, "trace": [], "build_metadata": None
    }
    if not planning_isolation["verified"]:
        result["block_reason"] = "planning_isolation_unverified"
        return result

    feedback = None
    for attempt in range(1, max_revisions + 2):
        request = {"user_message": user_message, "feedback": copy.deepcopy(feedback),
                   "instruction": _text_asset("plan-instruction.txt"),
                   "schema": _schema_asset("plan.schema.json"), "attempt": attempt}
        event = {"attempt": attempt, "stage": "plan", "raw_response": None, "error": None}
        started = time.monotonic()
        try:
            raw = planner(request)
            event["raw_response"] = raw if isinstance(raw, str) and len(raw.encode("utf-8")) <= MAX_RESPONSE_BYTES else None
            if isinstance(raw, str) and "```" in raw:
                raise ValueError("The plan response contains a code fence.")
            plan = _parse(raw)
            validate_plan(plan, valid_ids)
        except Exception as exc:
            event["error"] = type(exc).__name__ + ": " + str(exc)[:500]
            event["elapsed_seconds"] = round(time.monotonic() - started, 6)
            result["trace"].append(event)
            feedback = {"host_issues": ["The plan was invalid: " + event["error"]], "reviewer_findings": []}
            result["block_reason"] = "invalid_plan_or_planner_error"
            continue
        event["elapsed_seconds"] = round(time.monotonic() - started, 6)
        result["trace"].append(event)

        review_request = {"original_task": original_task, "checklist": checklist,
                          "plan": copy.deepcopy(plan),
                          "instruction": _text_asset("reviewer-instruction.txt"),
                          "schema": _schema_asset("decision.schema.json"), "attempt": attempt}
        event = {"attempt": attempt, "stage": "review", "raw_response": None, "error": None}
        started = time.monotonic()
        try:
            raw = reviewer(review_request)
            event["raw_response"] = raw if isinstance(raw, str) and len(raw.encode("utf-8")) <= MAX_RESPONSE_BYTES else None
            decision = _parse(raw)
            validate_decision(decision, valid_ids)
        except Exception as exc:
            event["error"] = type(exc).__name__ + ": " + str(exc)[:500]
            event["elapsed_seconds"] = round(time.monotonic() - started, 6)
            result["trace"].append(event)
            feedback = {"host_issues": ["The review was invalid: " + event["error"]], "reviewer_findings": []}
            result["block_reason"] = "invalid_review_or_reviewer_error"
            continue
        event["elapsed_seconds"] = round(time.monotonic() - started, 6)
        result["trace"].append(event)
        issues = []
        if plan["unknowns"] or any(UNKNOWN_ANSWER.fullmatch(r["planned_answer"]) for r in plan["risks"]):
            issues.append("The plan contains unresolved material decisions.")
        if decision["decision"] == "APPROVE" and not issues:
            build_request = {"user_message": user_message, "approved_plan": copy.deepcopy(plan),
                             "instruction": _text_asset("approval-continuation.txt")}
            build_event = {"attempt": attempt, "stage": "build", "error": None}
            started = time.monotonic()
            try:
                metadata = builder(build_request)
                json.dumps(metadata, allow_nan=False)
                result["build_metadata"] = copy.deepcopy(metadata)
                result["status"] = "BUILD_INVOKED"
                result["block_reason"] = None
            except Exception as exc:
                build_event["error"] = type(exc).__name__ + ": " + str(exc)[:500]
                result["status"] = "BUILD_FAILED"
                result["block_reason"] = "builder_error"
            build_event["elapsed_seconds"] = round(time.monotonic() - started, 6)
            result["trace"].append(build_event)
            return result
        feedback = {"host_issues": issues, "reviewer_findings": copy.deepcopy(decision["findings"])}
        result["block_reason"] = "unresolved_plan" if issues else "review_not_approved"
    return result
