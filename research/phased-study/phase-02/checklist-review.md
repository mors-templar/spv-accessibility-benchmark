# Phase 2: checklist review

**Status:** Draft 0.2.0. Researcher and accessibility-specialist review remain open.
No website, model, or human participant was evaluated in this phase.

## What is in the checklist

The list contains 188 actions with stable IDs.
It has 81 WCAG-derived actions, 81 guidance actions, and 26 research-process actions.
Its crosswalk refers to all 55 active WCAG 2.2 Level A and AA criterion IDs.
This is reference coverage, not proof that every rule, exception, or disability need is covered.

We screened the 81 R items against the linked A and AA criterion text.
This was a first technical pass by an AI assistant.
It was not an independent expert review or a complete review of every exception.
The G and P items still need systematic review.

R actions summarize possible WCAG outcomes.
G actions describe guidance or possible techniques.
The underlying outcome of a G action can still be a WCAG requirement.
P actions describe study procedures and are not website features.
Consult the original [WCAG 2.2 Recommendation](https://www.w3.org/TR/2024/REC-WCAG22-20241212/) for each judgment.

## Changes made in version 0.2.0

The previous 0.1.0 Markdown and JSON remain in `research/accessibility/versions/0.1.0/`.
The existing PDF remains a 0.1.0 snapshot.
The stable action IDs and criterion mappings were preserved.
These are focused technical edits, not an independent expert validation.

| Action IDs | Criterion | Change and reason |
| --- | --- | --- |
| ACT-016 | [1.3.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#meaningful-sequence) | Specify a correct programmatically determinable reading sequence. |
| ACT-031 | [1.1.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-content) | Add the CAPTCHA purpose text alternative and sensory alternatives. |
| ACT-032 | [2.4.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#link-purpose-in-context) | Refer to the criterion exception for ambiguous link purpose. |
| ACT-034 | [1.4.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#use-of-color) | Include actions, response prompts, and distinctions as well as information. |
| ACT-035 | [1.4.5](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#images-of-text) | State the technology condition and criterion exceptions. |
| ACT-042, ACT-043 | [1.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#contrast-minimum) | Include images of text in the applicable contrast checks. |
| ACT-044 | [1.4.11](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#non-text-contrast) | Focus on visual information needed to identify components and states. |
| ACT-046 | [1.4.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#resize-text) | Include resizing without assistive technology. |
| ACT-047, ACT-048 | [1.4.10](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#reflow) | Add the two-dimensional scrolling and content-loss conditions. |
| ACT-051 | [1.4.13](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#content-on-hover-or-focus) | Clarify dismissal without moving hover or keyboard focus when required. |
| ACT-062, ACT-063 | [2.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#no-keyboard-trap) | Specify keyboard-only exit and notice for nonstandard exit methods. |
| ACT-065 | [2.4.7](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-visible) | Use the criterion's mode-of-operation framing. |
| ACT-066 | [2.4.11](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#focus-not-obscured-minimum) | Specify keyboard focus and the criterion notes. |
| ACT-067 | [2.1.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#character-key-shortcuts) | Specify the non-printable key condition for remapping. |
| ACT-068 | [2.5.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#pointer-gestures) | Specify a single-pointer alternative without a path-based gesture. |
| ACT-070 | [2.5.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#pointer-cancellation) | Name the criterion's permitted cancellation conditions. |
| ACT-075 | [3.2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#on-input) | Clarify automatic context changes and advance notice. |
| ACT-085 | [3.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-identification) | Specify the input item with an automatically detected error. |
| ACT-087 | [3.3.4](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-prevention-legal-financial-data) | Include covered data changes and test responses as well as transactions. |
| ACT-088 | [3.3.7](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#redundant-entry) | Include information previously provided to the user. |
| ACT-112 | [4.1.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#name-role-value) | Clarify that change notifications are available to user agents. |
| ACT-158, ACT-159 | [1.2.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#audio-only-and-video-only-prerecorded) | Identify the appropriate prerecorded media alternatives. |
| ACT-161 | [1.2.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#audio-description-or-media-alternative-prerecorded) | Specify an alternative for time-based media or audio description. |
| ACT-164 | [1.4.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#audio-control) | Name the pause, stop, and independent volume options. |
| ACT-165 | [2.2.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#timing-adjustable) | State that the criterion has exceptions. |
| ACT-168 | [2.3.1](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#three-flashes-or-below-threshold) | State the flash-frequency and threshold alternatives. |

The checklist's G-label description now distinguishes guidance from an underlying required outcome.
The crosswalk list has a blank line before it for consistent Markdown rendering.

## Remaining review work

1. An accessibility specialist reviews each R summary against its full criterion and exceptions.
2. The specialist reviews the G techniques and their intended context.
3. The research team reviews P items as study procedures.
4. The team defines task-specific applicability, required journeys, and fixtures.
5. The team writes independent procedures for selected criteria and states.
6. The team records agreement, disagreements, and any unsupported checks.
7. The team freezes the approved checklist and its hash before the final comparison.

The [review ledger](checklist-review-ledger.json) lists all 188 items.
It records the 30 actions changed in this technical pass.
Every item remains pending expert review.
Do not treat a line item as a complete test procedure or a conformance decision.

The full checklist includes research-process text and an illustrative section about the five task types.
Those sections will be visible to the model in the proposed D, P, S, A, and X inputs.
This adds information beyond the original task and may influence results.
The team must deliberately approve that choice before freezing the study.

## Legacy scaffold warning

The older `work/avenues/02_agent_skills/SKILL.md` is an unvalidated prototype.
It claims universal compatibility and prevention of regressions without supporting evidence.
It asks a human to answer questions, which differs from this draft's autonomous one-shot workflow.
It also treats some patterns as mandatory implementations.
Do not deploy it as the Phase 2 study skill.
W3C's [modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) is guidance for that pattern.
It must be interpreted alongside WCAG and the actual interaction.
