"""Offline fixture tests. These tests never submit a task to a model."""
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
PHASES = HERE.parent
ROOT = HERE.parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gate = load("test_gate", PHASES / "phase-05/gate.py")
diagnostic = load("test_diagnostic", PHASES / "phase-04/spv-accessibility/scripts/verify_plan.py")
adapter = load("test_adapter", PHASES / "phase-04/tool_adapter.py")
prepare = load("test_prepare", HERE / "prepare_condition.py")
demo = load("test_demo", HERE / "simulate_synthetic.py")
codex_adapter = load("test_codex_adapter", HERE / "run_codex_review.py")


def d_message(task, instruction, checklist):
    return (task + "\n\n--- BEGIN ACCESSIBILITY REQUEST ---\n" + instruction
            + "--- BEGIN CHECKLIST ---\n" + checklist
            + "--- END CHECKLIST ---\n--- END ACCESSIBILITY REQUEST ---\n")


def valid_plan():
    return {"required_features": ["F01"], "risks": [{"feature": "F01", "risk": "Focus can be lost.",
            "question": "Where does focus go?", "planned_answer": "Return focus to the trigger.",
            "checklist_item_ids": ["ACT-127"]}], "unknowns": []}


def revise():
    return {"decision": "REVISE", "findings": [{"feature": "F01", "question": "Where does focus go?",
            "reason": "No useful focus behavior.", "plan_evidence": "The answer is absent.",
            "checklist_item_ids": ["ACT-127"]}]}


class DiagnosticTests(unittest.TestCase):
    def test_warns_on_recognized_gaps(self):
        result = diagnostic.verify_plan({"plan_text": "A modal and a form show async status.",
                                         "questions_and_answers": []})
        ids = {w["warning_id"] for w in result["warnings"]}
        self.assertTrue({"SPV-QUESTIONS", "SPV-CONTRAST", "SPV-DIALOG-FOCUS", "SPV-DIALOG-RETURN",
                         "SPV-STATUS", "SPV-FORM-LABEL", "SPV-KEYBOARD"}.issubset(ids))
        self.assertEqual(result["diagnostic_status"], "WARN")

    def test_no_warning_still_has_limitations(self):
        request = {"plan_text": "Native button; keyboard focus; check text contrast.",
                   "questions_and_answers": [{"question": "How?", "answer": "Use a native button."}]}
        result = diagnostic.verify_plan(request)
        self.assertEqual(result["diagnostic_status"], "NO_WARNING")
        self.assertTrue(any("not evidence" in x for x in result["limitations"]))

    def test_unknown_and_valid_modal_focus_return(self):
        request = {"plan_text": "Modal: keyboard focus enters; return focus to trigger; text contrast.",
                   "questions_and_answers": [{"question": "Result?", "answer": "Unknown"}]}
        ids = {w["warning_id"] for w in diagnostic.verify_plan(request)["warnings"]}
        self.assertIn("SPV-UNKNOWN", ids)
        self.assertNotIn("SPV-DIALOG-RETURN", ids)

    def test_invalid_inputs_and_duplicate_json_keys(self):
        for request in ({}, {"plan_text": " ", "questions_and_answers": []},
                        {"plan_text": "x", "questions_and_answers": [{"question": "?", "answer": ""}]},
                        {"plan_text": "x", "questions_and_answers": [], "run_id": "injected"}):
            with self.subTest(request=request), self.assertRaises(ValueError):
                diagnostic.verify_plan(request)
        with self.assertRaises(ValueError):
            diagnostic.parse_json('{"plan_text":"x","plan_text":"y"}')

    def test_cli_outputs_json_and_invalid_input_fails(self):
        script = PHASES / "phase-04/spv-accessibility/scripts/verify_plan.py"
        request = {"plan_text": "A button", "questions_and_answers": []}
        call = subprocess.run([sys.executable, str(script)], input=json.dumps(request), text=True,
                              capture_output=True, check=False)
        self.assertEqual(call.returncode, 0)
        self.assertEqual(json.loads(call.stdout), diagnostic.verify_plan(request))
        bad = subprocess.run([sys.executable, str(script)], input="{oops", text=True,
                             capture_output=True, check=False)
        self.assertNotEqual(bad.returncode, 0)

    def test_host_identifiers_are_not_model_arguments(self):
        tool = adapter.AdvisoryTool("run_1", "task_1")
        result = tool.verify_plan({"plan_text": "Page", "questions_and_answers": []})
        self.assertEqual(result["diagnostic_status"], "WARN")
        self.assertEqual(tool.events[0]["run_id"], "run_1")
        with self.assertRaises(ValueError):
            tool.verify_plan({"plan_text": "Page", "questions_and_answers": [], "run_id": "other"})
        self.assertEqual(len(tool.events), 2)

    def test_responses_function_parameters_match_request_schema(self):
        base = PHASES / "phase-04/spv-accessibility/references"
        request = json.loads((base / "verify-plan-request.schema.json").read_text(encoding="utf-8"))
        tool = json.loads((base / "openai-responses-function.json").read_text(encoding="utf-8"))
        self.assertTrue(tool["strict"])
        self.assertEqual(tool["parameters"], request)
        def inspect(node):
            if isinstance(node, dict):
                if node.get("type") == "object":
                    self.assertFalse(node["additionalProperties"])
                    self.assertEqual(set(node["properties"]), set(node["required"]))
                for child in node.values():
                    inspect(child)
            elif isinstance(node, list):
                for child in node:
                    inspect(child)
        inspect(tool["parameters"])


class GateTests(unittest.TestCase):
    def setUp(self):
        self.calls = []
        self.task = "Create a modal."
        self.checklist = "ACT-127: Return focus when appropriate.\n"
        self.instruction = "Use the checklist.\n"
        self.plan = valid_plan()
        self.decision = {"decision": "APPROVE", "findings": []}

    def run_gate(self, planner=None, reviewer=None, builder=None, **overrides):
        def default_planner(request):
            self.calls.append(("plan", copy.deepcopy(request)))
            return json.dumps(self.plan)
        def default_reviewer(request):
            self.calls.append(("review", copy.deepcopy(request)))
            return json.dumps(self.decision)
        def default_builder(request):
            self.calls.append(("build", copy.deepcopy(request)))
            return {"file_count": 0}
        kwargs = dict(run_id="run_1", original_task=self.task, checklist=self.checklist,
            common_instruction=self.instruction, user_message=d_message(self.task, self.instruction, self.checklist),
            checklist_ids=["ACT-127"],
            planner=planner or default_planner, reviewer=reviewer or default_reviewer, builder=builder or default_builder,
            planner_session_id="plan_1", reviewer_session_id="review_1",
            planning_isolation={"verified": True, "evidence": "Synthetic test callbacks"})
        kwargs.update(overrides)
        return gate.run_gate(**kwargs)

    def test_valid_approval_builds_only_after_review(self):
        result = self.run_gate()
        self.assertEqual(result["status"], "BUILD_INVOKED")
        self.assertEqual([c[0] for c in self.calls], ["plan", "review", "build"])
        self.assertEqual(self.calls[-1][1]["approved_plan"], self.plan)
        self.assertIn("schema", self.calls[0][1])
        self.assertIn("schema", self.calls[1][1])

    def test_rejection_is_bounded_and_never_builds(self):
        self.decision = revise()
        result = self.run_gate()
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual([c[0] for c in self.calls], ["plan", "review"] * 3)
        self.assertEqual(self.calls[2][1]["feedback"]["reviewer_findings"], revise()["findings"])

    def test_feedback_can_lead_to_approval(self):
        def reviewer(_request):
            self.calls.append(("review", None))
            return json.dumps(revise() if len([x for x in self.calls if x[0] == "review"]) == 1
                              else {"decision": "APPROVE", "findings": []})
        result = self.run_gate(reviewer=reviewer)
        self.assertEqual(result["status"], "BUILD_INVOKED")
        self.assertEqual([x[0] for x in self.calls], ["plan", "review", "plan", "review", "build"])

    def test_missing_feature_and_invalid_checklist_references_block(self):
        for mutate in (lambda p: p.update(required_features=[]),
                       lambda p: p["risks"][0].update(checklist_item_ids=["ACT-999"]),
                       lambda p: p.update(risks=[]),
                       lambda p: p["risks"][0].update(planned_answer=" ")):
            self.plan = valid_plan()
            mutate(self.plan)
            self.calls = []
            with self.subTest(plan=self.plan):
                self.assertEqual(self.run_gate()["status"], "BLOCKED")
                self.assertFalse(any(x[0] in ("review", "build") for x in self.calls))

    def test_unknown_plan_blocks_even_when_reviewer_approves(self):
        for mutate in (lambda p: p.update(unknowns=["Focus target is unknown."]),
                       lambda p: p["risks"][0].update(planned_answer="unknown")):
            self.plan = valid_plan()
            mutate(self.plan)
            self.calls = []
            self.assertEqual(self.run_gate()["block_reason"], "unresolved_plan")
            self.assertFalse(any(x[0] == "build" for x in self.calls))

    def test_bad_reviews_and_exceptions_block(self):
        variants = ["not JSON", '{"decision":"APPROVE","decision":"APPROVE","findings":[]}',
                    json.dumps({"decision": "APPROVE", "findings": revise()["findings"]}),
                    json.dumps({"decision": "REVISE", "findings": []})]
        for response in variants:
            self.calls = []
            with self.subTest(response=response):
                self.assertEqual(self.run_gate(reviewer=lambda _r: response)["status"], "BLOCKED")
                self.assertFalse(any(x[0] == "build" for x in self.calls))
        def broken(_request):
            raise RuntimeError("synthetic failure")
        self.assertEqual(self.run_gate(reviewer=broken)["block_reason"], "invalid_review_or_reviewer_error")

    def test_fenced_code_in_plan_is_rejected(self):
        self.plan["risks"][0]["planned_answer"] = "```html\n<button>Go</button>\n```"
        result = self.run_gate()
        self.assertEqual(result["status"], "BLOCKED")
        self.assertFalse(any(x[0] in ("review", "build") for x in self.calls))

    def test_unverified_isolation_blocks_all_callbacks(self):
        result = self.run_gate(planning_isolation={"verified": False, "evidence": "No isolation probe"})
        self.assertEqual(result["block_reason"], "planning_isolation_unverified")
        self.assertEqual(self.calls, [])

    def test_same_session_and_changed_message_rejected(self):
        with self.assertRaises(ValueError):
            self.run_gate(reviewer_session_id="plan_1")
        with self.assertRaises(ValueError):
            self.run_gate(user_message=self.task + " modified " + self.checklist)

    def test_real_checklist_size_is_accepted(self):
        checklist = (ROOT / "research/accessibility/master-action-checklist.md").read_bytes().decode("utf-8")
        result = self.run_gate(checklist=checklist, user_message=d_message(self.task, self.instruction, checklist))
        self.assertEqual(result["checklist_sha256"], "2a73ea4045012d195d0286c21867af009c955303bd969842a8e1d1cd92510575")

    def test_builder_error_is_not_reported_as_success(self):
        def broken(_request):
            raise OSError("synthetic build failure")
        result = self.run_gate(builder=broken)
        self.assertEqual(result["status"], "BUILD_FAILED")
        self.assertEqual(result["block_reason"], "builder_error")

    def test_mock_flawed_and_good_paths(self):
        self.assertEqual(demo.simulate("flawed")["status"], "BLOCKED")
        self.assertEqual(demo.simulate("good")["status"], "BUILD_INVOKED")


class ConditionTests(unittest.TestCase):
    def test_six_conditions_share_exact_inputs(self):
        task = b"Create a synthetic page."
        expected = hashlib.sha256(task).hexdigest()
        rows = {name: prepare.prepare(task, expected, name) for name in ("B", "D", "P", "S", "A", "X")}
        self.assertEqual(rows["B"][0], task)
        self.assertTrue(all(rows[name][0] == rows["D"][0] for name in ("P", "S", "A", "X")))
        self.assertEqual(rows["P"][1]["prompt_guidance_sha256"], rows["X"][1]["prompt_guidance_sha256"])
        self.assertEqual(rows["P"][1]["prompt_guidance_sha256"],
                         rows["P"][1]["shared_checklist_details"]["prompt_guidance_sha256"])
        self.assertEqual(rows["X"][1]["package"], ["prompt_guidance", "spv_accessibility_skill",
                         "advisory_diagnostic", "independent_reviewer", "host_gate"])
        self.assertFalse(rows["X"][1]["sent_to_model"])

    def test_incorrect_task_hash_fails(self):
        with self.assertRaises(ValueError):
            prepare.prepare(b"Synthetic task", "0" * 64, "X")

    def test_package_detects_changed_file(self):
        original = Path.read_bytes
        target = (ROOT / "research/phased-study/phase-04/prompt-guidance.txt").resolve()
        def modified(path):
            data = original(path)
            return data + b"changed" if path.resolve() == target else data
        with patch.object(Path, "read_bytes", modified):
            with self.assertRaises(ValueError):
                prepare.verify_package()


class CodexAdapterTests(unittest.TestCase):
    def setUp(self):
        local = ROOT / "local"
        local.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=local)
        self.path = Path(self.temp.name)
        self.assertTrue(self.path.resolve().is_relative_to(local.resolve()))
        self.commands = []

    def tearDown(self):
        self.temp.cleanup()

    def fake_process(self, command, *, input, stdout, stderr, timeout, env, check):
        role_dir = Path(command[command.index("-C") + 1]).parent
        role = role_dir.name.rsplit("-", 1)[-1]
        self.commands.append((role, command, input))
        event = {"type": "thread.started", "thread_id": "fake-thread-" + str(len(self.commands))}
        stdout.write((json.dumps(event) + "\n" + json.dumps({"type": "turn.completed", "usage": {}}) + "\n").encode())
        if role == "plan":
            response = valid_plan()
        elif role == "review":
            response = {"decision": "APPROVE", "findings": []}
        else:
            response = "Synthetic builder complete."
        message = json.dumps(response) if isinstance(response, dict) else response
        Path(command[command.index("--output-last-message") + 1]).write_text(message, encoding="utf-8")
        return types.SimpleNamespace(returncode=0)

    def test_mock_codex_combined_flow_and_private_event_log(self):
        task = b"Synthetic modal."
        result = codex_adapter.run(task_id="TEST_A", task=task, expected_sha256=hashlib.sha256(task).hexdigest(),
            run_id="mock_x", condition="X", executable="fake-codex", version="fake-version",
            model="fake-model", reasoning="high", timeout=10,
            isolation={"verified": True, "evidence": "synthetic fake only"},
            run_root=self.path, process=self.fake_process)
        self.assertEqual(result["status"], "BUILD_INVOKED")
        self.assertEqual([item[0] for item in self.commands], ["plan", "review", "build"])
        for role, command, _ in self.commands:
            expected_mode = "workspace-write" if role == "build" else "read-only"
            self.assertEqual(command[command.index("--sandbox") + 1], expected_mode)
            workspace = Path(command[command.index("-C") + 1])
            self.assertEqual((workspace / ".agents/skills/spv-accessibility/SKILL.md").exists(), role != "review")
        self.assertTrue(self.commands[0][2].startswith(task))
        self.assertEqual(self.commands[0][2].count(b"--- BEGIN CHECKLIST ---"), 1)
        self.assertTrue((self.path / "mock_x/host-events.jsonl").is_file())
        self.assertEqual(result["skill_activation"], "unknown")

    def test_unverified_preflight_is_rejected(self):
        source = HERE / "isolation-preflight-template.json"
        with self.assertRaises(ValueError):
            codex_adapter.check_preflight(source, "fake-version")

    def test_skill_only_starts_one_ungated_build(self):
        task = b"Synthetic skill task."
        result = codex_adapter.run(task_id="TEST_S", task=task, expected_sha256=hashlib.sha256(task).hexdigest(),
            run_id="mock_s", condition="S", executable="fake-codex", version="fake-version",
            model="fake-model", reasoning="high", timeout=10,
            isolation={"verified": True, "evidence": "synthetic fake only"},
            run_root=self.path, process=self.fake_process)
        self.assertEqual(result["status"], "BUILD_INVOKED")
        self.assertEqual([item[0] for item in self.commands], ["build"])
        workspace = Path(self.commands[0][1][self.commands[0][1].index("-C") + 1])
        self.assertTrue((workspace / ".agents/skills/spv-accessibility/SKILL.md").exists())
        self.assertEqual((workspace / "AGENTS.md").read_text(encoding="utf-8"), "")

    def test_skill_only_requires_isolation(self):
        task = b"Synthetic skill task."
        result = codex_adapter.run(task_id="TEST_S", task=task, expected_sha256=hashlib.sha256(task).hexdigest(),
            run_id="mock_s_block", condition="S", executable="fake-codex", version="fake-version",
            model="fake-model", reasoning="high", timeout=10,
            isolation={"verified": False, "evidence": "synthetic fake only"},
            run_root=self.path, process=self.fake_process)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertFalse(self.commands)

    def test_reused_codex_thread_cannot_approve_build(self):
        def reused(command, **kwargs):
            result = self.fake_process(command, **kwargs)
            stdout = kwargs["stdout"]
            stdout.seek(0)
            event = {"type": "thread.started", "thread_id": "same-fake-thread"}
            stdout.write((json.dumps(event) + "\n" + json.dumps({"type": "turn.completed"}) + "\n").encode())
            stdout.truncate()
            return result
        task = b"Synthetic modal."
        result = codex_adapter.run(task_id="TEST_A", task=task, expected_sha256=hashlib.sha256(task).hexdigest(),
            run_id="mock_reuse", condition="A", executable="fake-codex", version="fake-version",
            model="fake-model", reasoning="high", timeout=10,
            isolation={"verified": True, "evidence": "synthetic fake only"},
            run_root=self.path, process=reused)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertNotIn("build", [item[0] for item in self.commands])


if __name__ == "__main__":
    unittest.main()
