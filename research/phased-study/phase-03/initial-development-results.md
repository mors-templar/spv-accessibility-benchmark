# Initial development observations: one task

**Status:** Exploratory, 30 October 2026. These are not final benchmark results.
The scan plan was recorded after the first artifact was generated.
No accessibility specialist, keyboard reviewer, or screen-reader user has assessed these pages.

The researcher chose to use the five selected Arena prompts.
This pilot used `ARENA_01_SERVICES` once with each of B, D, and P.
All three Codex turns completed and produced an `index.html` file.
The task and test procedures were not frozen before generation.
The plan and runner details are in [development-run-plan.md](development-run-plan.md).

## Initial browser scan

The same local pilot scanned the initial page state for each artifact.
The browser was Chromium 151.0.7922.34, Playwright 1.62.1, and axe-core 4.10.3.
The viewport was 1280 by 720 pixels. No requests were reported blocked.

| Condition | Violated axe rules | Affected nodes | Critical nodes | Serious nodes | Moderate nodes | Incomplete rules |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| B: original request | 3 | 17 | 0 | 15 | 2 | 2 |
| D: checklist | 1 | 4 | 0 | 4 | 0 | 2 |
| P: checklist and plan guidance | 0 | 0 | 0 | 0 | 0 | 2 |

The B and D serious findings came from the `color-contrast` rule.
The B moderate findings came from `heading-order` and `region`.
Those two rules are tagged as best practice, not automatic WCAG failures.
All three scans reported `aria-prohibited-attr` and `color-contrast` as incomplete.
Incomplete findings require further investigation and are not passes.
The scan reported no minor findings in these initial states.

P produced a `spv-plan.md` file and a model self-report.
D produced a model self-report.
The P event log contains a successful command referencing the plan before a successful command referencing `index.html`.
That observation is not an assessment of plan quality or site accessibility.

## Interpretation

The reported counts are axe findings, not a general accessibility score.
They cover only one initial browser state per generated page.
The scan did not assess required journeys, keyboard operation, focus, screen-reader output, or alternate states.
The two incomplete rules and untested areas prevent a conclusion that P is accessible or WCAG conformant.

This is one run per condition for one request and one requested model configuration.
The sequence was B, D, P. The outputs were not independently reviewed before the scan plan was written.
The observed differences do not establish that the packages will improve other tasks or models.
Further development runs and a frozen independent evaluation are needed.

The recorded generation times were 95.467 seconds for B, 91.574 seconds for D, and 133.658 seconds for P.
The event records contain token usage and cached-input fields.
They do not establish monetary cost or hidden provider settings.

Raw reports, events, and artifacts are stored in the ignored local run directories `dev01`, `dev02`, and `dev03`.
Do not publish raw source prompts or generated artifacts without a release review.
