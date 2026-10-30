# Phase 5: reviewer and host gate

**Status:** Development candidate, 30 October 2026. The gate has offline fixture tests.
The Codex adapter has mock-process tests. Real sessions and the planning boundary remain unverified.
The final wording and policy are not frozen.

## Components

- [Plan instruction](reviewer/plan-instruction.txt) asks the generator for a structured plan.
- [Reviewer instruction](reviewer/reviewer-instruction.txt) asks a separate reviewer to compare that plan with the request and checklist.
- [Plan schema](reviewer/plan.schema.json) and [decision schema](reviewer/decision.schema.json) define the exchanged objects.
- [Approval continuation](reviewer/approval-continuation.txt) tells the generator when to implement.
- [gate.py](gate.py) provides the host orchestration API.

The generator answers its own plan questions.
The reviewer issues `APPROVE`, `REVISE`, or `INSUFFICIENT_EVIDENCE`.
The host accepts no more than two revised plans after the initial plan by default.
Invalid output and callback errors consume an attempt.
A block does not create a final website through the gate's build callback.
The record includes every returned plan and review in the host's in-memory trace.

## Programmatic contract

Call `run_gate` with `original_task`, `checklist`, `common_instruction`, and the exact assembled `user_message`.
Supply the checklist IDs from the approved JSON checklist.
Provide distinct planner and reviewer callbacks and distinct session IDs.
The planner and reviewer callbacks receive a dictionary and return JSON text.
The request includes the exact instruction and JSON schema for that phase.
The planner's `user_message` contains the task and one checklist.
Send it once; do not append another task or checklist.
The reviewer receives the original task, checklist, and plan separately.
The builder receives the same user message, approved plan, and continuation instruction.
It returns JSON-compatible metadata.

`run_gate` checks the shared-message assembly, JSON shape, feature names, checklist IDs, and decision consistency.
It rejects empty feature lists and requires a risk and question for each listed feature.
It rejects unresolved material unknowns and recognized unknown answers before build.
It rejects recognizable fenced code in plan responses.
It invokes the builder only after a valid approval and successful host checks.
`BUILD_INVOKED` means the build callback returned. It does not prove a usable site exists.

The plan's feature list comes from the generator.
The host cannot determine all missing request features by JSON validation.
The separate reviewer must compare the list with the original task.
An incorrect reviewer approval can still occur.
The code-fence check cannot detect all code or stop a model emitting code as text.
The reviewer can also be affected by misleading text in a plan.
Do not count a plan approval as an accessibility result.

## Isolation boundary

The host checks a `planning_isolation` record before it calls the planner.
The record contains a boolean and a reference to the actual verification evidence.
This record is an adapter assertion. It does not establish isolation by itself.
Before a real A or X run, verify a read-only planning boundary on that runner.
Also verify that no planner tool can write into the output workspace before approval.
The host controls callback order. Python callbacks in one process are not an operating-system security boundary.
Likewise, distinct session IDs alone do not prove the sessions are independent.
Inspect the actual runner and retain the preflight results.

Run the separate [synthetic demonstration](../phase-06/simulate_synthetic.py) to inspect the gate behavior.
The demonstration uses fake callbacks. It does not call a model or test filesystem isolation.
The caller must save the returned trace in a private run directory.
The in-memory trace does not survive a process interruption by itself.
The development Codex adapter saves separate call logs as it runs.
