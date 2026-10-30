# Draft task contracts for exploratory review

**Status:** Draft, 30 October 2026. These are not frozen final-study contracts.
They were written after the first task's pilot outputs were generated.
The other exploratory runs were already scheduled when this draft was prepared.
The team must review these checks against the original messages before final use.

The local manifest at `work/experiments/benchmarks/selected_arena_baselines/manifest.json` records the source IDs and hashes.
The source is the [WebDev Arena dataset](https://huggingface.co/datasets/lmarena-ai/webdev-arena-preference-10k).
The original message remains the generator input.
This document guides independent assessment and must not be loaded into a generator workspace.

## Common result rules

For each required feature, record `PASS`, `FAIL`, or `UNASSESSABLE` with evidence.
Use `UNASSESSABLE` when a missing external service or evaluator fault prevents a judgment.
If a required feature is absent, record a task failure.
Do not mark its dependent accessibility behavior as passed.

For accessibility, record the criterion, page state, method, result, and evidence.
Use the five labels in the [evaluation plan](../../experiment-protocol-2026-10-30/03-evaluation.md).
Test keyboard access, visible focus, labels, state exposure, structure, and contrast where applicable.
Use a real screen reader before claiming an announcement was verified.
The axe scan is one source of evidence, not a complete accessibility assessment.

Use fresh browser storage for each review.
Record browser, version, viewport, zoom, input method, route, and state.
Use fictional names and data. Do not submit information to real services.
The team has not yet frozen a common service, dependency, or fixture policy.

## T01: services landing page

| ID | Required observation | Accessibility review |
| --- | --- | --- |
| T01-01 | The requested navigation and landing-page sections are present. | Check landmarks, heading relationships, link names, and keyboard navigation. |
| T01-02 | The page presents the requested service features, process, and placeholder imagery. | Check meaningful image alternatives and reading order. |
| T01-03 | The application section permits users to select and read the requested categories. | Check keyboard operation, focus, names, and state exposure for the actual control design. |
| T01-04 | The FAQ presents the requested information. Test an expanded state if it is interactive. | Check keyboard operation, names, state, and visible focus when controls exist. |
| T01-05 | The order-form call to action provides the behavior shown by the artifact. | Check its accessible name and operation. |
| T01-06 | Inspect the requested page title and search and social metadata. | Check that the document title describes the page. |
| T01-07 | Inspect requested client-logo placeholders, footer, and responsive layout. | Check image alternatives, landmarks, and reflow where applicable. |

The source request refers to an order form but does not provide its content.
A generated placeholder or text file does not establish that a real ordering workflow exists.
Record the delivered behavior; do not claim production ordering or email delivery.

## T02: consulting landing page

| ID | Required observation | Accessibility review |
| --- | --- | --- |
| T02-01 | The requested hero, service representations, visual treatment, and call to action are present. | Check headings, names, keyboard access, and visible focus. |
| T02-02 | The page adapts to desktop, tablet, and mobile viewport sizes. | Check reflow and horizontal scrolling under the applicable WCAG conditions. |
| T02-03 | The requested motion appears where the artifact implements it. | Check applicable pause requirements and reduced-motion behavior separately. |
| T02-04 | Inspect the delivered source and build for the requested framework and libraries. | Mark this check unassessable if dependencies cannot be inspected or installed. |
| T02-05 | Check the request's explicit contrast and semantic-HTML requirements. | Measure rendered contrast and inspect semantic relationships in relevant states. |

Reduced-motion support is useful guidance.
Do not label every missing motion preference as the same WCAG failure without checking the criterion and exceptions.

## T03: cinema and ticket selection

| ID | Required observation | Accessibility review |
| --- | --- | --- |
| T03-01 | Film entries expose the requested poster, rating, duration, synopsis, and hall information. | Check text alternatives and programmatic relationships. |
| T03-02 | Users can find films by the available search or organization features. | Check labels, keyboard access, focus, and result updates. |
| T03-03 | A booking flow presents screening mode, time, and language choices. | Check names, group labels, keyboard operation, selection state, and validation. |
| T03-04 | Inspect region-related currency or language choices and the responsive layout. | Check names, state, reflow, and contrast. |
| T03-05 | Inspect trailer and social-sharing affordances. | Check names and keyboard access; record unavailable external media. |
| T03-06 | Inspect the requested email confirmation or QR-ticket outcome. | Check accessible confirmation and any relevant status message. |

Film data, a mail service, and a ticket provider are not supplied.
A fictional, readable QR code can demonstrate a local interface path only.
It does not prove entry at a real cinema or delivery of an email.
Record blocked network requests and fixture decisions before interpreting an unavailable outcome.

## T04: task and analytics dashboard

| ID | Required observation | Accessibility review |
| --- | --- | --- |
| T04-01 | The board presents the three requested task statuses and task details. | Check landmarks, labels, relationships, and keyboard traversal. |
| T04-02 | Add, edit, and delete a task using fictional input. | Check labels, errors, focus handling, and status messages. |
| T04-03 | Move a task between statuses and inspect the resulting state. | Test keyboard operation and the applicable non-dragging pointer alternative separately. |
| T04-04 | Exercise the requested filters and search. | Check control names, keyboard use, state, and result updates. |
| T04-05 | Inspect status charts, deadline visualization, and task progress. | Check that equivalent information is available in text or another accessible form. |
| T04-06 | Inspect export, theme switching, and action notifications. | Check names, focus, contrast, and applicable status messages. |
| T04-07 | Inspect source and dependencies for the named libraries and requested responsive behavior. | Mark an unavailable build or dependency with its observed cause. |

Use a predeclared fictional task and deadline when the team freezes a fixture.
Do not assume a chart is inaccessible solely because it uses a canvas or a library.
Apply the WCAG dragging criterion and its exceptions to the implemented interaction.

## T05: personal portfolio

| ID | Required observation | Accessibility review |
| --- | --- | --- |
| T05-01 | A prominent hero presents a featured project. | Check heading structure, text alternatives, and contrast. |
| T05-02 | Navigation reaches other project content. | Check names, keyboard operation, focus, and link targets. |
| T05-03 | An about section is present and reachable. | Check structure, reading order, and navigation. |

The request does not specify project count, content sources, a backend, or a visual design.
Do not invent those details as mandatory task requirements.

## Open decisions before final evaluation

- Review each requirement and procedure with the researcher and an accessibility reviewer if available.
- Freeze fixture data, external-network policy, build dependencies, viewports, and time limits.
- Define precise steps and expected observations for every selected criterion and state.
- Decide how to mask artifacts and record suspected reviewer unmasking.
- Keep exploratory results separate from any later frozen final batch.
