# Evaluation and analysis plan

**Status:** Draft 0.1. No evaluation has been performed.
The numbers below define planned measures, not observed results.

## 1. Evaluation model

Evaluate the saved artifact after generation stops.
The study reviewer must not use the generator's self-report as the answer key.
The evaluation has three layers: task function, automated checks, and human review.
The researcher plans to conduct the human review.
Record their training and experience without claiming expert status by default.

Use [WCAG 2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/) A and AA as the requirement reference.
Use the [WCAG evaluation methodology](https://www.w3.org/TR/2026/NOTE-wcag-em-2-20260723/) to guide scope, sampling, and reporting.
The methodology is a W3C Group Note.
This planned study is a scoped evaluation, not a claim of full WCAG conformance.

## 2. Define the test unit

An accessibility test record has these fields:

- Run ID and task ID.
- Requirement or guidance ID and version.
- Page, component, and interaction state.
- Intended behavior, applicability rule, and procedure.
- Result, evidence, reviewer, and test tool version.

Use five outcome labels: `PASS`, `FAIL`, `NOT_APPLICABLE`, `UNASSESSABLE`, and `NOT_TESTED`.
Explain every label with a short reason.
Use `NOT_APPLICABLE` only when the criterion truly does not apply.
A required feature that is missing is a task failure.
Record dependent accessibility tests as unassessable where necessary.
Do not count optional guidance failures as WCAG violations.

## 3. Task function

Before generation, write a task contract for each original request.
List the minimum required journeys, states, and expected outcomes.
Document unresolved dependencies and a consistent fixture policy.
Review the contracts against the original text and obtain subject review.
Do not specify a visual style or technology that the request does not require.

For each scheduled attempt, record:

1. Whether an artifact was returned.
2. Whether the preserved artifact can be built and started.
3. Whether each required journey completes under the contract.
4. Whether a failure came from the artifact, provider, environment, or evaluator.

An approved agent plan without a working artifact is not task completion.
A blocked agent attempt is a workflow failure for task-completion reporting.
An external infrastructure or evaluation failure is indeterminate.
Predefine the classification rules and keep the evidence.

### Candidate task-specific concerns

The following are starting points for expert review.
They are not the final task contracts or mandatory UI designs.

| Task | Candidate core journey | Candidate accessibility checks |
| --- | --- | --- |
| T01 services | Explore services and the requested navigation. Resolve the unavailable order form. | Keyboard access, names, focus, and expanded-state behavior for controls that exist. |
| T02 consulting | Reach requested page content and any required animation. | Requested contrast and semantic structure; keyboard focus and motion controls where applicable. |
| T03 cinema | Browse listings and complete the specified ticket flow under the frozen fixture rule. | Labels, errors, focus, updates, and selection behavior where applicable. |
| T04 dashboard | Exercise the requested task-management and chart functions. | Keyboard access, a non-dragging pointer alternative, names, and chart information where applicable. |
| T05 portfolio | Navigate the delivered portfolio content. | Page structure, links, names, focus, contrast, and image alternatives where applicable. |

For T04, distinguish keyboard operation from the single-pointer alternative to dragging.
WCAG 2.2 criterion 2.5.7 has exceptions that the evaluator must inspect.
Do not require a feature simply because it appears in this illustrative table.

## 4. Common accessibility checks

The team must convert these areas into precise, versioned procedures.
Each procedure must state its WCAG criterion and exceptions.
Record the routes and interactive states under test.

| Area | Example criterion | Example method |
| --- | --- | --- |
| Page title and language | 2.4.2, 3.1.1 | Inspect the browser title and document language. |
| Structure and relationships | 1.3.1 | Inspect headings, labels, groups, and information relationships. |
| Keyboard and traps | 2.1.1, 2.1.2 | Traverse and operate relevant controls with a keyboard. |
| Focus | 2.4.7, 2.4.11 | Observe focus in relevant states and layouts. |
| Name, role, and value | 4.1.2 | Inspect accessible names and state changes for controls. |
| Contrast | 1.4.3 | Check rendered text colors and applicable exceptions. |
| Reflow | 1.4.10 | Inspect the specified viewport and applicable exceptions. |
| Images and media | 1.1.1 and relevant media criteria | Review alternatives for the content that exists. |
| Form errors | 3.3.1, 3.3.2, 3.3.3 | Submit invalid data and inspect messages and labels. |
| Status messages | 4.1.3 | Inspect relevant dynamic messages and programmatic exposure. |

Do not infer screen-reader announcements from an HTML attribute alone.
Record actual assistive-technology tests when the team can perform them.
WAI-ARIA Authoring Practices describe patterns; they are not mandatory WCAG text.

### Draft test cards

These cards illustrate the level of detail needed before the final test suite is frozen.
They still require accessibility review and task-specific state selection.

**KBD-01: Keyboard access to a required journey**

- Reference: WCAG 2.2, criterion 2.1.1, including its exception.
- Preconditions: The task contract defines the journey and the site starts.
- Steps: Start with keyboard focus on the page. Traverse and operate each required control without a pointer.
- Pass: The user completes the journey with a keyboard when the criterion applies.
- Fail: A required function cannot be operated by keyboard and no exception applies.
- Unassessable: The function is missing or another fault prevents the journey.
- Evidence: Record the route, keys, control, and observed result.

**FOCUS-01: Visible keyboard focus**

- Reference: WCAG 2.2, criterion 2.4.7.
- Preconditions: A keyboard-operable user interface component exists in a selected state.
- Steps: Move focus to the component with the keyboard. Observe the indicator at the frozen viewport.
- Pass: The keyboard focus indicator is visible for the applicable component.
- Fail: The indicator cannot be seen when it is required.
- Evidence: Record the component, state, browser, and screenshot.

**CONTRAST-01: Rendered text contrast**

- Reference: WCAG 2.2, criterion 1.4.3, including its exceptions.
- Preconditions: Text exists in a selected page state and its applicable threshold is known.
- Steps: Measure the rendered text and adjacent background. Inspect images, overlays, and gradients when present.
- Pass: Normal text reaches 4.5:1, or large text reaches 3:1, when the criterion applies.
- Fail: The applicable ratio is below the threshold and no exception applies.
- Unassessable: The evaluator cannot determine the relevant rendered colors reliably.
- Evidence: Record text, state, measured ratio, threshold, and method.

**DRAG-01: Pointer alternative to dragging**

- Reference: WCAG 2.2, criterion 2.5.7, including its exceptions.
- Preconditions: A dragging interaction exists in the task dashboard.
- Steps: Attempt the same function with a single pointer without dragging.
- Pass: An applicable equivalent operation can be completed without dragging.
- Fail: No such operation exists and no criterion exception applies.
- Evidence: Record the operation, alternative, input method, and result.

Do not treat these four examples as the complete primary test set.
Each task contract must list the full selected criteria and states.
Report the number of WCAG criteria that the final test set does not assess.

### Security, privacy, and ethics scope

The main outcome is accessibility and task function.
The proposed checks do not measure general website security, privacy, or ethical quality.
The [OWASP Top 10:2025](https://top10.owasp.org/2025/) is a security risk reference.
It does not supply this study's accessibility criteria.

Run generated code in an isolated environment with test data and no production credentials.
Restrict network access according to the frozen task contract.
Record when that restriction prevents an intended function from being assessed.
If the team adds security checks, freeze their procedures and report their results separately.
Do not claim that a site is secure because the accessibility checks passed.

## 5. Playwright and axe-core

Use Playwright to start the artifact and exercise the frozen user journeys.
Use the same interaction policy and states across conditions.
Use semantic locators when feasible; allow equivalent valid interfaces.
Capture the exact failing action and relevant evidence.

Run axe-core on the agreed initial and interactive states.
Pin the browser, Playwright, axe-core, enabled rules, tags, and configuration.
The existing local pilot used axe-core 4.10.3 with `target-size` disabled.
That historical setting is not a recommendation for the new study.
Decide rule coverage explicitly before the run.

Save raw axe `violations`, `passes`, `incomplete`, and `inapplicable` results.
Record rule IDs, affected nodes, page state, and axe `impact`.
Report axe impact counts as critical, serious, moderate, and minor where present.
Keep unknown impact values separate.
Deduplicate repeated observations by a frozen component-and-rule policy.
Retain links to every state where the observation occurred.

An axe impact is the tool's classification.
WCAG does not define those four severity grades.
If the team adds human severity, define it separately and do not merge the two scales.
An automated result can need human confirmation.
Zero automated violations do not prove accessibility or conformance.

## 6. Human review

The researcher reviews the frozen artifact using the written procedures.
The review includes keyboard use, focus, rendered contrast, content, and required flows.
Review the relevant opened, error, success, and other interaction states.
Record browser, operating system, viewport, zoom, and input method.
When available, record the screen reader and version for assistive-technology tests.

Mask condition labels and randomize artifact IDs before review where practical.
The reviewer must not see the intervention transcript before scoring.
Some artifacts can reveal their condition; record any suspected unmasking.
Calibrate procedures on separate development fixtures.
Do not change the scoring rules after seeing study results.

An independent accessibility specialist or person with relevant lived experience would strengthen review.
Record who reviewed each result and which checks they performed.
If a second reviewer is available, score a predefined overlap independently.
Report exact agreement and, where appropriate, Cohen's kappa.
Explain missing labels, low prevalence, and undefined kappa values.
Resolve disagreements with a documented adjudication record.
A single review is still useful, but does not measure inter-rater reliability.

## 7. Proposed primary outcome

**Scoped demonstrated success** is a run with all three conditions:

1. A runnable artifact exists.
2. Every frozen required task journey passes.
3. Every applicable selected primary accessibility check passes independently.

An unknown or untested required check cannot demonstrate success.
The primary outcome is not full WCAG conformance.
It covers only the specified checks, states, and conditions.

For each condition and configuration, let `N` be all scheduled attempts.
Let `P` be demonstrated successes and `U` be indeterminate attempts.
Report `P / N` and the uncertainty bound `(P + U) / N`.
Label `P / N` as the demonstrated-success rate.
It is a lower bound, not an estimate that all unknowns failed.
Report known workflow failures and accessibility failures separately.

For example, model refusal, gate block, or a broken generated build is not success.
It is not automatically a WCAG violation.
An unrelated provider outage or evaluator defect is indeterminate.
Prespecify the boundary and retain all scheduled attempts in `N`.

If a known failure and an unrelated unknown occur in one attempt, classify the run as known non-success.
Reserve `U` for attempts that could have met the full outcome if the unknown were resolved.
When a missing required feature makes a check unassessable, classify task completion as failed.

## 8. Secondary measures

| Measure | Definition | Important limit |
| --- | --- | --- |
| Required-journey completion | Attempts with every required journey passed / scheduled attempts. | Use bounds for external unknowns. |
| Assessed accessibility failure fraction | `FAIL / (PASS + FAIL)` over selected applicable criterion-state records. | Show the denominator and coverage; do not treat unknowns as passes. |
| Assessment coverage | `(PASS + FAIL) / (PASS + FAIL + UNASSESSABLE + NOT_TESTED)` for expected applicable records. | Report `NOT_APPLICABLE` separately. |
| axe findings | Counts by rule and tool impact after stated deduplication. | A finding count is not a count of all barriers. |
| Model false-pass fraction | Independent `FAIL` among model `pass` claims with comparable assessed results / comparable model `pass` claims. | Exclude and report missing, unassessed, or unmatched records separately. |
| Model false-fail fraction | Independent `PASS` among model `fail` claims with comparable assessed results / comparable model `fail` claims. | This is a claim-based fraction, not a test's false-positive rate. |
| Skill activation | Runs with observed skill invocation / scheduled S or X attempts. | Unknown activation is not non-activation; show both. |
| Gate outcomes | Counts of approvals, revisions, blocks, invalid responses, and leaks. | Plan approval does not prove site quality. |
| Resources | Wall time, model calls, token counts, cost, and retries. | Report unavailable values; do not infer hidden tokens. |

Checklist item and criterion-state records may not match one-to-one.
Before analysis, define a reviewed mapping and a compatible aggregation level.
If there is no valid mapping, do not calculate self-report agreement for that item.

## 9. Analysis and interpretation

Compare X with D as the proposed main contrast.
Also show B versus D and each package versus B and D.
Use percentage-point differences with actual numerators and denominators.
Show results by task and model-runner configuration.
Show all failures and individual repeat outcomes.
Do not treat repeat number 1 in two conditions as a matched pair by itself.

Do not treat repeats as independent sampled tasks.
Do not make a general population claim from five purposively selected requests.
With this small design, report descriptive results and limits.
Any later inferential model needs a justified sampling plan and power analysis.
Do not present an arbitrary composite or a tool score as a universal accessibility percentage.

The five prompts were public before this study.
Unknown model training data create a contamination risk.
Prompt length, tokens, calls, tools, and time differ between packages.
The package comparisons cannot attribute gains to one component alone.
Provider updates and hidden settings limit exact reproducibility.

## 10. Reporting table template

| Task | Model and runner | Condition | Repeats | Demonstrated success | Known non-success | Indeterminate | Evidence |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| T01 | TBD | B | 3 planned | TBD | TBD | TBD | TBD |
| T01 | TBD | D | 3 planned | TBD | TBD | TBD | TBD |
| T01 | TBD | P | 3 planned | TBD | TBD | TBD | TBD |
| T01 | TBD | S | 3 planned | TBD | TBD | TBD | TBD |
| T01 | TBD | A | 3 planned | TBD | TBD | TBD | TBD |
| T01 | TBD | X | 3 planned | TBD | TBD | TBD | TBD |

Replicate this structure for all tasks and configurations.
Publish no filled values until the evidence exists and release rights are clear.
