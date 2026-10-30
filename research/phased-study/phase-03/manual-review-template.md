# Manual review template for one exploratory artifact

**Status:** Draft. Complete one copy for each artifact.
This form does not establish full WCAG conformance.
Use the [draft task contracts](task-contracts-draft.md) to select applicable journeys.
Do not read the model's plan or self-report before recording observations.
The optional [review record schema](review-record.schema.json) checks required fields and evidence structure.
It does not verify the accuracy of a review.

## Review details

| Field | Record |
| --- | --- |
| Masked artifact ID | |
| Artifact archive or manifest hash and version | |
| Reviewer and relevant experience | |
| Date and time | |
| Operating system and browser version | |
| Viewport and zoom | |
| Input method and any assistive technology version | |
| Condition hidden from reviewer? | Yes / No / Unknown |
| Suspected unmasking and reason | |
| Fixture data and network restrictions | |

## Result labels

- `PASS`: The specified observable behavior met the stated criterion.
- `FAIL`: The observed behavior did not meet the applicable criterion.
- `NOT_APPLICABLE`: The criterion does not apply in this state. Explain why.
- `UNASSESSABLE`: A missing feature, dependency, or other fault prevented the check.
- `NOT_TESTED`: The reviewer did not perform the check.

Do not mark a missing required feature as an accessibility pass.
Record the missing feature as a task failure and the dependent check as unassessable.
Do not infer a screen-reader announcement from an attribute alone.

## Task journeys

Record every required journey from the relevant task contract.
Record the starting state, action, expected result, observed result, and evidence.

| Task check ID | State and action | Expected result | Observed result | Result | Evidence |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

For missing source data or an unavailable external service, describe the limitation.
A simulated confirmation does not prove that a real email was delivered.

## Keyboard and focus

1. Start with a fresh browser context and load the reviewed page.
2. Use Tab and Shift+Tab to reach interactive controls.
3. Use the appropriate activation keys to operate each required control.
4. Review focus visibility, focus order, and whether the user can leave each component.
5. Repeat in relevant open, error, success, and other changed states.
6. Record the keys used, control, state, observed result, and any exception.

For a drag interaction, test the keyboard path and a single-pointer non-dragging alternative separately.
Apply the exceptions in the relevant WCAG criteria.
Do not require one ARIA pattern when a different implementation meets the applicable outcome.

| Check and criterion | Component and state | Steps and observation | Result | Evidence |
| --- | --- | --- | --- | --- |
| Keyboard operation: 2.1.1 | | | | |
| No keyboard trap: 2.1.2 | | | | |
| Focus order: 2.4.3 | | | | |
| Visible focus: 2.4.7 | | | | |
| Focus not obscured: 2.4.11 | | | | |
| Dragging alternative: 2.5.7, if applicable | | | | |

## Content, structure, and appearance

Inspect headings, landmarks, labels, text alternatives, and control names in the relevant states.
Measure text contrast where the criterion applies, including applicable exceptions.
Inspect reflow at the viewport specified by the final procedure.
Record the measurement method and result. Mark unknown measurements as unassessable.

| Check and criterion | Component and state | Observation or measurement | Result | Evidence |
| --- | --- | --- | --- | --- |
| Information and relationships: 1.3.1 | | | | |
| Non-text alternatives: 1.1.1 | | | | |
| Text contrast: 1.4.3 | | | | |
| Reflow: 1.4.10 | | | | |
| Name, role, value: 4.1.2 | | | | |
| Status messages: 4.1.3, if applicable | | | | |
| Error identification: 3.3.1, if applicable | | | | |

## Follow-up and unresolved checks

Record automated findings that need confirmation and any states not reached.
List any assistive-technology checks not performed.
Do not repair the original artifact during review.

| Item | Reason or observation | Evidence | Follow-up |
| --- | --- | --- | --- |
| | | | |
