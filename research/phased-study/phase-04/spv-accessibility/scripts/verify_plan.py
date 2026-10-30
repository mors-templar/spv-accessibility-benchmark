#!/usr/bin/env python3
"""Advisory signal checks for a plan. This is not a WCAG evaluator."""
import argparse
import json
import re
import sys
from pathlib import Path

MAX_INPUT = 500_000


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def parse_json(text):
    if len(text.encode("utf-8")) > MAX_INPUT:
        raise ValueError("Input exceeds the size limit.")
    return json.loads(text, object_pairs_hook=_pairs, parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Invalid JSON constant.")))


def verify_plan(request):
    """Return deterministic warnings for recognized signals in a supplied plan."""
    if not isinstance(request, dict) or set(request) != {"plan_text", "questions_and_answers"}:
        raise ValueError("Expected plan_text and questions_and_answers only.")
    plan = request["plan_text"]
    questions = request["questions_and_answers"]
    if not isinstance(plan, str) or not plan.strip():
        raise ValueError("plan_text must be a nonempty string.")
    if not isinstance(questions, list) or len(questions) > 1000:
        raise ValueError("questions_and_answers must be an array of at most 1000 entries.")
    for qa in questions:
        if not isinstance(qa, dict) or set(qa) != {"question", "answer"}:
            raise ValueError("Each question entry must have question and answer only.")
        if any(not isinstance(qa[k], str) or not qa[k].strip() for k in ("question", "answer")):
            raise ValueError("Questions and answers must be nonempty strings.")

    # Signals in an answer can describe a planned behavior as well as the plan text.
    text = "\n".join([plan] + [qa["answer"] for qa in questions]).lower()
    warnings = []

    def has(pattern):
        return bool(re.search(pattern, text, flags=re.IGNORECASE))

    def warn(identifier, reason, evidence, ids):
        warnings.append({"warning_id": identifier, "reason": reason,
                         "plan_evidence": evidence, "checklist_item_ids": ids})

    if not questions:
        warn("SPV-QUESTIONS", "Record questions and planned answers for material risks.",
             "The question-and-answer list is empty.", [])
    if any(re.fullmatch(r"\s*(unknown|unresolved|tbd|not yet known|unsure)\s*[.!]?\s*", qa["answer"], re.I) for qa in questions):
        warn("SPV-UNKNOWN", "Review unresolved answers before implementation.",
             "At least one answer is marked unknown or unresolved.", [])
    if not has(r"\bcontrast\b|4\.5\s*:\s*1"):
        warn("SPV-CONTRAST", "Consider text contrast and relevant exceptions.",
             "No recognized text contrast signal was found.", ["ACT-042", "ACT-043"])
    if has(r"\b(modal|dialog|lightbox)\b"):
        if not has(r"\bfocus\b"):
            warn("SPV-DIALOG-FOCUS", "Consider focus entry and containment for a modal.",
                 "A dialog is mentioned, with no recognized focus signal.", ["ACT-123", "ACT-125"])
        if not has(r"(?:return|restore|restor|back to|previous|invok|trigger).{0,60}focus|focus.{0,60}(?:return|restore|restor|back to|previous|invok|trigger)"):
            warn("SPV-DIALOG-RETURN", "Consider the logical focus destination when a dialog closes.",
                 "A dialog is mentioned, with no recognized focus-return signal.", ["ACT-127"])
    if has(r"\b(async|asynchronous|toast|status message|live update|validation error)\b"):
        if not has(r"\b(announc\w*|live region|aria-live|role=.status|role=.alert|screen reader)\b"):
            warn("SPV-STATUS", "Consider how applicable status messages reach assistive technology.",
                 "A possible status update is mentioned, with no recognized announcement signal.", ["ACT-113", "ACT-116"])
    if has(r"\b(form|input|text field|search field)\b") and not has(r"\blabel\w*\b|accessible name"):
        warn("SPV-FORM-LABEL", "Consider labels for fields that need user input.",
             "A form or field is mentioned, with no recognized label signal.", ["ACT-082"])
    if has(r"\b(button|link|menu|dialog|modal|form|tab|slider|control)\b") and not has(r"\b(keyboard|tab key|tab navigation|native|focus)\b"):
        warn("SPV-KEYBOARD", "Consider keyboard operation for interactive features.",
             "An interactive feature is mentioned, with no recognized keyboard signal.", ["ACT-060"])

    return {
        "diagnostic_status": "WARN" if warnings else "NO_WARNING",
        "warnings": warnings,
        "limitations": [
            "Keyword signals can miss risks and can warn about valid plans.",
            "The diagnostic checks neither rendered behavior nor WCAG conformance.",
            "A missing warning is not evidence that a requirement is met."
        ]
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="JSON file. Defaults to standard input.")
    args = parser.parse_args(argv)
    try:
        text = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read(MAX_INPUT + 1)
        result = verify_plan(parse_json(text))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
