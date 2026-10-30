# Candidate intervention files

**Status:** Phase 2 working drafts. They are not approved, installed, or validated interventions.
The exact bytes can change until the study team freezes them.
The researcher approved checklist version 0.2.0 separately.
That approval does not approve these instructions.
See the [intervention design review](../intervention-design-review.md) for the comparisons and rationale.

| File | Proposed role |
| --- | --- |
| `checklist-instruction.txt` | Shared D instruction for all checklist-based conditions. |
| `prompt-guidance.txt` | P project instruction; no host-enforced gate. |
| `spv-accessibility/SKILL.md` | S skill instruction; the diagnostic is advisory. |
| `spv-accessibility/*.schema.json` | Draft diagnostic request and response contracts. |
| `reviewer/plan-phase.txt` | A and X generator instruction for the plan-only phase. |
| `reviewer/reviewer-instruction.txt` | A and X separate reviewer instruction. |
| `reviewer/approval-continuation.txt` | Host instruction after a valid approval. |
| `reviewer/*.schema.json` | Draft plan and reviewer decision contracts. |
| `candidate-manifest.json` | Draft versions and SHA-256 hashes for the files and checklist. |

## Condition input

For B, send the original task bytes as the only study user message.
For D, P, S, A, and X, use this byte sequence:

```text
ORIGINAL_TASK_BYTES
UTF8("\n\n--- BEGIN ACCESSIBILITY REQUEST ---\n")
CHECKLIST_INSTRUCTION_BYTES
UTF8("--- BEGIN CHECKLIST ---\n")
CHECKLIST_MARKDOWN_BYTES
UTF8("--- END CHECKLIST ---\n--- END ACCESSIBILITY REQUEST ---\n")
```

The instruction and checklist files must each end with one newline.
The original task bytes are inserted without any edit.
The placeholder names above are not literal text sent to a model.
Record the original task hash and assembled-message hash for each future run.
Do not send the source tasks to a hosted model until the rights question is resolved.

All five checklist-based arms receive the same D user message.
P, S, A, and X add their respective runner or host components.
The candidate uses the full approved checklist in D, P, S, A, and X.
The checklist includes process text and the illustrative task-type section.
Record that extra information when interpreting comparisons with B.
The model self-report is a claim and is not the independent evaluation.
For G items, an unselected technique is not automatically a WCAG failure.
For P items, a model may report only its observed work or research-team responsibility.

## P: prompt guidance

Load `prompt-guidance.txt` through the selected runner's project-instruction mechanism.
Record the actual delivery channel and native runner context.
Do not call a project instruction a system-role message unless the runner uses that role.
An API system-role variant is a distinct delivery variant.
No host gate is part of P.
The draft requests an observable `spv-plan.md` when file writing is available.
For a chat-only runner, it requests the plan in the response before code.
If the plan or execution order is not observable, record it as unknown.

## S: skill

Load the draft skill through the runner's supported skill mechanism.
The skill requests a `verify_plan` diagnostic when one is available.
The Phase 2 package does not implement that tool or its provider adapters.
The host does not block implementation in S.
Record activation, tool calls, unavailable capabilities, and unknowns.
The model supplies only plan text and questions to the proposed diagnostic.
The host attaches the run ID, task ID, and checklist version from the study schedule.
The model must not guess those identifiers.

## A: reviewer and gate

The host requests a plan in a read-only phase.
A separate reviewer inspects the task, checklist, and plan.
Only a valid `APPROVE` permits a writable implementation phase.
`REVISE` and `INSUFFICIENT_EVIDENCE` return findings for revision.
The proposed maximum is two revised plans after the first review.
The host records `BLOCKED` after the limit without approval.
The host must reject malformed decisions and missing required findings.
The host must reject plans with no required features or blank material-risk fields.
The JSON schema does not enforce every host rule.
An explicit `unknown` answer is allowed and must be reviewed.
The host can prevent pre-approval file writes and acceptance of implementation.
It cannot prevent a model from emitting code as text.

The host, isolation boundary, diagnostic, and provider adapters have not been built here.
The [prior prompt pack](../../../experiment-protocol-2026-10-30/02-prompt-pack.md) contains draft JSON contracts.
Those schemas and the reviewer behavior need separate validation before use.
Treat plan approval as a planning decision, not a WCAG pass.

## X: combined package

Use one D message, P guidance, the S skill, and the A host gate.
Do not add a second checklist or a second gate.
When P says to implement after planning, the host gate determines when writing is permitted.
The S diagnostic is advisory; the A reviewer controls the gate decision.
The independent evaluator is separate from the A reviewer.

## Answer policy and scope

This candidate uses AI-generated questions and AI answers.
One-shot refers to one initial user submission, not one internal model call.
It does not measure a human's decision-making or overreliance.
A future human-answer condition needs its own protocol.
