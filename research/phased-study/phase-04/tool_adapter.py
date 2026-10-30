"""Bind host-owned run identifiers to the advisory skill diagnostic."""
import copy
import hashlib
import importlib.util
import json
import re
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "spv-accessibility/scripts/verify_plan.py"
SPEC = importlib.util.spec_from_file_location("spv_verify_plan", SCRIPT)
DIAGNOSTIC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DIAGNOSTIC)


class AdvisoryTool:
    """Return the tool response and retain a private, host-owned call ledger."""

    def __init__(self, run_id, task_id, checklist_version="0.2.0"):
        for value in (run_id, task_id):
            if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", value):
                raise ValueError("Run and task IDs must be valid identifiers.")
        if checklist_version != "0.2.0":
            raise ValueError("This development package uses checklist 0.2.0.")
        self.run_id = run_id
        self.task_id = task_id
        self.checklist_version = checklist_version
        self.events = []

    def verify_plan(self, arguments):
        """Accept model-supplied arguments; attach identifiers only to the host ledger."""
        request = copy.deepcopy(arguments)
        event = {"run_id": self.run_id, "task_id": self.task_id,
                 "checklist_version": self.checklist_version, "request": request,
                 "response": None, "error": None}
        try:
            response = DIAGNOSTIC.verify_plan(request)
            event["response"] = copy.deepcopy(response)
            encoded = json.dumps(request, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            event["request_sha256"] = hashlib.sha256(encoded).hexdigest()
            return response
        except (TypeError, ValueError) as exc:
            event["error"] = type(exc).__name__ + ": " + str(exc)[:500]
            raise
        finally:
            self.events.append(event)
