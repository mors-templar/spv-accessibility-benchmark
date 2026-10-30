# Build and execution plan

**Status:** Draft 0.1. This document does not authorize or start the study runs.

## 1. Planned components

| Component | Responsibility | Required evidence |
| --- | --- | --- |
| Task registry | Identify each original task without changing its bytes. | Dataset revision, task ID, source ID, original SHA-256, rights decision. |
| Condition registry | Define B, D, P, S, A, and X. | Exact instruction files, checklist version, content hashes. |
| Runner adapter | Start a fresh model-and-runner session for one attempt. | Configuration, visible settings, user-message hash, transcript when permitted. |
| Skill adapter | Load the skill and expose the diagnostic where supported. | Skill hash, invocation, tool input and output, unsupported capabilities. |
| Plan supervisor | Enforce read-only planning and the approved transition for A and X. | State transitions, reviewer decisions, revisions, leaks, stop reason. |
| Artifact store | Preserve the final site and generated reports. | File manifest, hashes, original archive, build logs. |
| Evaluation harness | Run frozen function tests, Playwright, and axe. | Browser and tool versions, routes, states, raw reports, evidence. |
| Human review pack | Present masked artifacts and assessment forms. | Reviewer, procedures, observations, disagreements, evidence. |
| Analysis | Compute fixed summaries from completed records. | Analysis version, denominators, missing-data table, output tables. |

These are planned responsibilities.
Existing prototype files must be audited before reuse.
Do not describe them as ready merely because they exist.

## 2. Proposed directory layout

```text
study/
  protocol/                   Frozen study protocol and registry
  interventions/
    prompt-guidance/          P instruction and hash
    spv-accessibility/        S skill and diagnostic contract
    reviewer/                 A prompts, schemas, and host rules
    combined/                 X package manifest
  fixtures-dev/               Separate development tasks and known outcomes
  evaluator/
    task-contracts/           Required journeys and fixture policies
    checks/                   Accessibility procedures and mappings
    playwright/               Browser actions and assertions
    axe/                      Rule settings and result handling
  adapters/                   Runner-specific invocation code
  analysis/                   Frozen metric calculations
  private-runs/               Prompts, transcripts, outputs, and reports
  public-release/             Only material cleared for release
```

`private-runs/` must be excluded from version control and the public site.
The active repository currently publishes `docs/` through GitHub Pages.
Do not place protected prompts or unreviewed outputs in `docs/`.
Generated sites can contain copied or sensitive source content.
Inspect each artifact before any public release.

## 3. Build the task contracts

1. Read each authorized source task in the controlled local environment.
2. List exact task requirements and their acceptance checks.
3. Record ambiguous details and unavailable services or source data.
4. Define a single fixture or mock policy for each affected task.
5. State how the rule is supplied without modifying the original task text.
6. Review the contract with an accessibility reviewer.
7. Freeze the contract before generation.

For T01, resolve the missing order-form source.
For T03, resolve film data and email or QR confirmation.
A fake email service cannot prove email delivery.
Do not accept a mock as full delivery unless the frozen task contract says so.
If a required service cannot be provided consistently, revise the study design before the run.

The evaluator can use fixed data without leaking expected results to the generator.
If a generator needs data access, provide the same documented resource to every condition.
Record differences that a runner cannot control.

## 4. Build and check the interventions

Implement the candidate prompts from [02-prompt-pack.md](02-prompt-pack.md).
Keep the full checklist unchanged across D, P, S, A, and X.
Use the same original task in every arm.
Hash the checklist, prompt files, skill, schemas, and supervisor version.

For P, log the effective instruction delivery and any code before the plan.
Do not add a host gate in P.

For S, validate the skill metadata against the published format.
Use provider-specific wrappers for the common tool contract.
Test the actual tool invocation and its unsupported-capability path.
Test valid plans that use native HTML without unnecessary ARIA.
Treat diagnostics as prompts for review, not as conformance decisions.

For A and X, implement the supervisor as a small state machine:

```text
START -> PLAN_READ_ONLY -> REVIEW -> APPROVED -> BUILD_WRITABLE -> COMPLETE
                              |
                              +-> REVISE -> PLAN_READ_ONLY
                              +-> INSUFFICIENT_EVIDENCE -> PLAN_READ_ONLY
                              +-> INVALID -> STOP OR RETRY UNDER FROZEN POLICY
                              +-> RETRY_LIMIT -> BLOCKED
```

The proposed limit is two plan revisions after the initial plan.
The host checks the review response against the frozen schema.
Only `APPROVE` permits the writable phase.
Do not mount the writable output project in the plan phase.
Use a temporary read-only environment and prevent pre-approval artifact acceptance.
If a platform cannot enforce this boundary, mark A and X unsupported there.
Do not rename an advisory prompt as an enforced gate.

Develop representative fixtures outside the five study tasks.
Include missing keyboard operation, contradictory state handling, and valid native controls.
Label the expected plan outcomes with expert review.
Test malformed responses, extra fields, retries, timeouts, bypass attempts, and write denial.
Record confusion counts for reviewer decisions on the labeled fixtures.
Precision and recall need both positive and negative cases.
Report undefined values when a denominator is zero.
Fixture performance does not establish website accessibility.

## 5. Build the independent evaluator

Write a separate evaluation procedure for each primary check.
Each procedure needs an ID, WCAG source, preconditions, steps, expected outcome, and exceptions.
Use frozen state-entry steps and expected outcomes.
Include positive and negative evaluator fixtures where technically feasible.
Validate that a test does not pass merely because a required feature is absent.
Review false positives and false negatives with an accessibility specialist.

Use Playwright for browser actions and task journeys.
Use axe-core for the frozen automated rule set.
Keep a manual assessment form for checks that need judgment.
Add assistive-technology checks if the team has the required skills and tools.
Record the checks that the available team cannot assess.
Freeze the evaluator before comparative generation.
Keep evaluator code and hidden expected outcomes outside generator workspaces.

The existing checklist is a shared knowledge reference in the intervention arms.
It is not a replacement for separate test procedures and human observations.

## 6. Runner compatibility and fairness

Choose specific accessible configurations before scheduling.
For each, document model, runner, version, operating system, interface, and execution date.
Record native tools and whether the runner can load project instructions, skills, and subagents.
Record hidden defaults as unknown.
Do not call a runner a model, or assume two runners use the same model.

Give all conditions the same base workspace and native tool permissions.
Add only the condition-specific files, tools, and gate.
Check parent directories and global configuration for loaded project instructions.
Remove unintended study instructions from the baseline when the runner permits it.
Keep unavoidable native instructions and record what the runner exposes.
For A and X, the read-only plan phase is part of the intervention.
If the native runner changes tools, instructions, or UI defaults, record that difference.
The interventions use different resources by design.
Report time, calls, and cost alongside outcome changes.

The tentative wall-clock limit is 20 minutes per attempt.
This is a planning value for review, not a validated fairness threshold.
Apply the approved cap to every condition and retain timeouts.
Use each provider's supported settings and record them.
Do not invent a temperature or model seed when the interface hides it.

## 7. Freeze and schedule

Before any study attempt, approve and version these items:

1. Dataset permissions and task hashes.
2. Checklist version and complete assembled input for each condition.
3. Task contracts, fixtures, routes, states, and assessment procedures.
4. Prompt and skill files, reviewer schemas, and host transition rules.
5. Runner versions, model identifiers, settings, time caps, and retry limits.
6. Primary outcome, secondary measures, unknown handling, and analysis plan.
7. Reviewer masking, review allocation, and release policy.

Use a reproducible schedule randomization seed, proposed `314159`.
That seed orders attempts; it does not control model randomness.
Store the schedule, seed, software version, and timestamp.
Interleave conditions within task and runner where the environment allows.
Record outages and provider version changes by date.

Treat earlier experiments or known project outputs as development information.
The selected requests are already known to the team and cannot be called a fully blinded holdout.
Do not tune interventions on comparative outputs and then present those same outputs as untouched evaluation.

## 8. Procedure for one scheduled attempt

1. Assign a unique run ID and the randomized position.
2. Start a clean session and a clean workspace.
3. Verify the original task bytes and the condition package hashes.
4. Assemble the user message according to the selected condition.
5. Apply the scheduled runner configuration and record effective settings.
6. Submit the task once; record any internal model calls.
7. Apply gate decisions and retry limits when the condition requires them.
8. Stop at completion, block, refusal, or timeout.
9. Preserve the raw response, generated files, logs, and hashes where permitted.
10. Do not repair the artifact before the independent evaluation.
11. Create a masked evaluation copy and record its relationship to the original.

If the model provides code in chat, use a frozen extraction rule.
Do not fix defects during extraction.
Record any changes needed to start an artifact and their justification.
If extraction or setup needs a semantic code change, preserve both versions.
Report the original as unable to run under the unmodified-artifact rule.

## 9. Minimal run record

```json
{
  "run_id": "T01-R1-B-01",
  "task_id": "ARENA_01_SERVICES",
  "task_sha256": "record-from-manifest",
  "condition": "B",
  "repeat": 1,
  "model_id": "unknown-until-run",
  "runner_id": "unknown-until-run",
  "runner_version": "unknown-until-run",
  "settings": {"temperature": "unknown", "model_seed": "unknown"},
  "user_message_sha256": "not-yet-computed",
  "intervention_hashes": [],
  "schedule_seed": 314159,
  "status": "planned",
  "artifact_sha256": null,
  "gate_decisions": [],
  "skill_activation": "not-applicable",
  "start_utc": null,
  "end_utc": null,
  "token_counts": null,
  "cost": null,
  "missing_data_reason": null
}
```

This is an example schema, not a real attempt.
Use `null` or a defined unknown value for unavailable data.
Add provider, operating system, allowed tools, storage paths, and evaluator versions.
Validate all records against a versioned schema before analysis.

## 10. Release and audit

Keep raw source text, transcripts, and artifacts in controlled storage.
Record rights decisions and a release review for every shared item.
Publish the protocol and analysis code when permitted.
Publish allowed artifact hashes, test specifications, and results with clear limits.
GitHub Pages serves public static content even when its source repository is private.
Do not assume a generated dynamic site will work unchanged on Pages.
Archive the exact evaluated artifact and document any separate static export.

Any planned participant research needs an independent ethics and consent review where applicable.
The current plan contains no human participants in the intervention loop.
