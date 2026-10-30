# Initial Codex development comparison

**Status:** Exploratory. The first baseline was generated before this note was written.
This is not a preregistered comparison or the final benchmark.

The first pilot uses selected task `ARENA_01_SERVICES` once in each condition.
The planned order is B, D, then P. The order is not randomized.
`dev01` is B, `dev02` is D, and `dev03` is P.
The local `record.json` for each attempt is the source for its actual status.

| Setting | Recorded choice |
| --- | --- |
| Requested runner | Codex CLI 0.165.0-alpha.1.2 on Windows 11, Python 3.13.9 |
| Requested model | `gpt-6.1-terra`, high reasoning effort |
| Workspaces | A new local directory for each attempt. P has a candidate `AGENTS.md` file. |
| Message | Original task bytes for B; the same task plus the common checklist package for D and P. |
| Checklist | Researcher-approved version 0.2.0; its hash is in the run records. |
| Prompt guidance | Candidate revision `2026-10-30-r2`; P adds it through `AGENTS.md`. |
| Cap | 1,200 seconds per attempt; a timeout is retained as an outcome. |
| Script SHA-256 | `2c754c515e925d69800408ff008d97313ca3612125719b735c348ef0f8e0f9c4` |

The runner passes the prepared bytes to the CLI on standard input.
The CLI does not expose the server-side message bytes in these records.
The records therefore do not prove how the service internally represents them.
Native instructions, available skills, and other hidden defaults are not fully observable.

A synthetic test confirmed that the Windows workspace sandbox can write in the work directory.
Another synthetic test confirmed that this CLI setup can load a project `AGENTS.md` instruction.
The CLI marks `prefer_mxc` as an under-development feature.
The workspace sandbox does not prove that files outside the working directory cannot be read.
Review the captured event logs for unintended access before interpreting a run.

## Exploratory initial-state scan

After generation, use the existing browser pilot on the initial `index.html` state.
Use its fixed 1280 by 720 viewport and default axe rules for each available artifact.
The installed pilot uses Playwright 1.62.1, its axe adapter 4.10.2, and axe-core 4.10.3.
The pilot records the browser version, blocked requests, raw rule results, and affected nodes.
It blocks non-target origins and requests other than GET and HEAD.
Record a missing or failed page as unassessable for this scan.

This scan covers only one rendered state.
It does not assess keyboard journeys, screen readers, task completion, or WCAG conformance.
The scan protocol was recorded after the first artifact was generated.
It is exploratory and does not replace the final independent evaluator.

The checklist, task contracts, and independent evaluation procedure are not all frozen for the final study.
Do not claim an accessibility improvement from generation alone.
The evaluator must handle missing features, failed builds, timeouts, and unknown checks.
The five requests were chosen purposively and do not represent all websites.

Store attempts under ignored `local/phase-03-development/`.
Do not publish raw prompts, logs, or generated artifacts without a separate release review.
