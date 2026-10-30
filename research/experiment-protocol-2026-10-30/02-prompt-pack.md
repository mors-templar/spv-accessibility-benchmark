# Candidate intervention prompt pack

**Status:** Draft 0.1. These instructions have not been tested or frozen.
Review them with the team before implementation.

## 1. Input assembly rules

The original task is stored outside this document.
Never change its words, punctuation, or whitespace for one condition.
Verify the original UTF-8 bytes against the task manifest before assembly.
Do not send the protected task to a hosted service before rights are clear.

For B, send exactly the original task text as the study user message.
For D, P, S, A, and X, send the original task followed by the same block below.
The separator and block are added bytes.
Record both the original task hash and the full assembled-message hash.
Use the same checklist file bytes and the same assembly rule in every intervention arm.

The D message is longer than B.
Its self-report also requires work that B does not request.
Those changes are part of the D package.
Do not attribute the full B-to-D difference to the checklist text alone.

The placeholders below describe how the host assembles messages.
They are not literal text to send.

```text
<ORIGINAL_TASK_UTF8_BYTES>

--- BEGIN ACCESSIBILITY REQUEST ---
Use the accessibility checklist below while you complete the request above.
Keep all required features from the original request.
Apply each checklist item only when it is relevant to the requested site.
The R items describe possible WCAG outcomes and include conditions and exceptions.
The G items describe guidance and possible techniques.
The P items describe research activities rather than mandatory site features.
Do not claim a check passed unless you have observed supporting evidence.
Do not call a missing requested feature not applicable.
Mark any item you cannot assess as unassessed.
Create an accessibility self-report for all checklist item IDs.
For each R or G item, record pass, fail, not applicable, or unassessed.
For each P item, record research activity and do not call it a site defect.
Give a short reason and evidence for each status.
If your environment cannot create a file, include the report in your response.
The independent study team will review the finished site separately.
--- BEGIN CHECKLIST ---
<EXACT_MASTER_ACTION_CHECKLIST_UTF8_BYTES>
--- END CHECKLIST ---
--- END ACCESSIBILITY REQUEST ---
```

The `pass` status for a G item means the suggested technique was used.
It is not a WCAG conformance judgment.
An R-item pass is the model's claim, not an independent result.
The full checklist text may introduce links and research instructions.
The team must review and freeze those bytes before any run.

## 2. P: prompt-level guidance

Put this text in the runner's persistent project instruction file.
Use the runner's supported format and record the actual delivery channel.
Do not claim a system role when the runner loads a project file as user context.
The P condition has no study-specific tool gate.

An actual API system-role message is a different delivery variant.
Record and analyze it separately from a project-file variant.
Do not assume those channels have the same instruction priority.

```text
For the current website request, plan accessibility before implementation.
Identify requested features and relevant accessibility risks.
For each risk, ask a short question that can verify the intended behavior.
Answer with a specific implementation plan or mark the answer unknown.
Keep the requested features in the plan.
Apply checklist items only when their conditions apply.
Use the WCAG criterion and its exceptions for requirement decisions.
Guidance is not automatically a mandatory implementation technique.
Implement the website after you record the plan and questions.
Use the tools already available in the runner when needed.
Record checks that you did not perform.
Do not claim the finished site conforms to WCAG without evidence.
Continue without asking a human to answer the plan questions.
```

The runner may expose the plan in a transcript or a generated report.
Record missing plans and any code emitted before the plan.
The prompt does not prove that the model complied.

## 3. S: skill instructions

The future skill directory must be named `spv-accessibility`.
Its `SKILL.md` begins with this candidate text.
The [Agent Skills specification](https://agentskills.io/specification) defines the package format.

```markdown
---
name: spv-accessibility
description: Plan and check accessibility for a requested website using the supplied checklist and a plan diagnostic.
---

# Website accessibility plan

1. Read the original website request and the supplied checklist.
2. Identify required user journeys and interface features.
3. Identify relevant R items and optional G guidance for those features.
4. Write a plan for keyboard use, names, states, visual presentation, and errors when relevant.
5. Ask a question for each material accessibility risk.
6. Answer each question with a concrete plan or mark it unknown.
7. Call `verify_plan` with the plan when that tool is available.
8. Consider every diagnostic warning before implementation.
9. Keep the user's required features in the implementation.
10. Test observable behavior with available tools.
11. Mark unobserved checklist items as unassessed.
12. Record the diagnostic result and any unresolved risks.
```

The host may expose `verify_plan` through a tool adapter.
The diagnostic output is advisory in S.
It must not approve an inaccessible site or enforce a code gate.
Tool availability and actual invocation are measured separately.
If the skill is not invoked, keep the run and record non-activation.

### Proposed tool contract

This contract is runner-independent JSON Schema.
Each adapter must translate it to the provider's required wrapper.
Do not assume all providers accept one wrapper or support skill files.

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "task_id": {"type": "string", "minLength": 1},
    "checklist_version": {"type": "string", "minLength": 1},
    "plan_text": {"type": "string", "minLength": 1},
    "questions_and_answers": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "properties": {
          "question": {"type": "string"},
          "answer": {"type": "string"}
        },
        "required": ["question", "answer"]
      }
    }
  },
  "required": ["task_id", "checklist_version", "plan_text", "questions_and_answers"]
}
```

The proposed response contract is:

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "diagnostic_status": {
      "type": "string",
      "enum": ["WARN", "NO_WARNING", "UNASSESSED"]
    },
    "warnings": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "properties": {
          "warning_id": {"type": "string"},
          "reason": {"type": "string"},
          "plan_evidence": {"type": "string"},
          "checklist_item_ids": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["warning_id", "reason", "plan_evidence", "checklist_item_ids"]
      }
    },
    "limitations": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["diagnostic_status", "warnings", "limitations"]
}
```

`NO_WARNING` does not mean the plan or site is approved.
The diagnostic can identify missing keywords or malformed input.
Those signals do not prove a WCAG failure or a correct implementation.
The schemas and provider wrappers still need implementation and validation.

## 4. A: reviewer agent and host gate

The host creates a fresh generator context and a separate reviewer context.
The generator's first phase must have no write access to the output project.
The host asks for a plan, not an implementation.
The host validates the phase output before the next step.

### Plan-phase instruction

```text
This phase prepares a website plan for independent review.
Do not create or modify website files in this phase.
Do not provide implementation code in this phase.
Return the requested plan as a JSON object.
List required features, accessibility risks, questions, and proposed answers.
Identify unknown inputs and service dependencies.
For each applicable risk, cite the relevant checklist item IDs.
Describe planned behavior, not claims about a finished website.
```

The following plan schema is a starting contract.
The host must implement, validate, and version it before the study.

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "required_features": {"type": "array", "items": {"type": "string"}},
    "risks": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "properties": {
          "feature": {"type": "string"},
          "question": {"type": "string"},
          "planned_answer": {"type": "string"},
          "checklist_item_ids": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["feature", "question", "planned_answer", "checklist_item_ids"]
      }
    },
    "unknowns": {"type": "array", "items": {"type": "string"}}
  },
  "required": ["required_features", "risks", "unknowns"]
}
```

The host rejects malformed plan output.
The host also rejects empty required-feature lists and blank plan answers.
An explicit `unknown` answer is allowed and must be reviewed.
An exposed code block is logged as a plan-phase leak.
Read-only file access cannot prevent a model from emitting code as text.
The host must prevent accepting or applying implementation before approval.
Retain leaked text only in the controlled trace when permitted.

### Reviewer instruction

```text
You review a proposed website plan before implementation.
You receive the original request, the checklist, and the generator's plan.
Do not implement the website.
Check that the plan covers required user journeys.
Check whether relevant accessibility risks have concrete planned behaviors.
Use R items as conditional outcomes and G items as optional techniques.
Do not require a particular ARIA attribute when an equivalent valid method exists.
Ask a precise question for each material missing or unclear behavior.
Refer to evidence in the plan for each finding.
Use APPROVE when the plan is sufficiently specific for implementation.
Use REVISE when a material planned behavior is missing or contradictory.
Use INSUFFICIENT_EVIDENCE when the available plan cannot support a decision.
Return the decision and findings in the host's required JSON format.
Do not claim the finished site passes accessibility tests.
```

### Reviewer decision contract

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "decision": {
      "type": "string",
      "enum": ["APPROVE", "REVISE", "INSUFFICIENT_EVIDENCE"]
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "properties": {
          "feature": {"type": "string"},
          "question": {"type": "string"},
          "reason": {"type": "string"},
          "plan_evidence": {"type": "string"},
          "checklist_item_ids": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["feature", "question", "reason", "plan_evidence", "checklist_item_ids"]
      }
    }
  },
  "required": ["decision", "findings"]
}
```

`APPROVE` means approval of a plan for implementation.
It does not mean that an unbuilt website passes WCAG.
The reviewer can approve a plan with an empty findings list.
The host must reject invalid JSON and unsupported decisions.
For `REVISE` or `INSUFFICIENT_EVIDENCE`, require at least one actionable finding.

### Host continuation after approval

```text
The plan review is APPROVE.
Implement the website using the approved plan and the original request.
Keep all required features.
Complete the requested accessibility self-report.
Record unperformed checks and unknown results.
```

For `REVISE` or `INSUFFICIENT_EVIDENCE`, send the findings back to the generator.
The proposed limit is two revised plans after the first review.
If the third review does not approve, record `BLOCKED` and stop that attempt.
The generator must not receive a writable build phase when blocked.
Preserve every review, rejection, retry, and error in the run log.

## 5. X: combined package

Use the same D user message once.
Load the P guidance and the S skill.
Use the A reviewer and host gate for the plan phase.
Do not add a second gate or duplicate the checklist.
The host starts the writable build phase only after reviewer approval.
Record whether the skill and diagnostic actually ran.

The P instruction to implement after planning is conditional on the host gate in X.
The host sends the approval continuation only after approval.
The S diagnostic remains advisory; the A reviewer makes the gate decision.

## 6. Common examples of useful questions

These are examples, not mandatory answers for every website.

| If the feature exists | Plan question | Independent check later |
| --- | --- | --- |
| Expandable navigation | How can a keyboard user open and close it? | Exercise it with keyboard input. |
| Modal dialog | Where does focus go on open and close? | Test focus movement and return. |
| Form validation | How will a user find and understand an error? | Submit invalid data and inspect the result. |
| Drag interaction | How can a user complete the same task without dragging? | Test the intended alternative and its pointer operation. |
| Informative chart | How is the chart's information available in text? | Inspect its accessible alternative in context. |

These examples are design prompts.
The task and WCAG criterion determine whether a check applies.
The test specification must allow valid alternative implementations.
