# Phase 3: prepare the first comparison

**Status:** Exploratory development. The final benchmark has not run.
The selected checklist is version 0.2.0.
The intervention instructions remain candidate wording.

Compare these conditions on each unchanged selected request:

| ID | User message | Extra study instruction |
| --- | --- | --- |
| B | Original task bytes only. | None. |
| D | Original task plus the common instruction and full approved checklist. | None. |
| P | The same user message as D. | Candidate prompt guidance in the runner's project context. |

P adds project guidance; it does not alter the original task.
The complete user message for D and P is longer than B.
P has no study-specific host gate.
Record the actual runner channel and any hidden defaults.

## Offline input check

`prepare_trial.py` is a zero-dependency Python utility for Python 3.9 or later.
It checks task and intervention hashes and assembles the input in memory.
It prints metadata and hashes only; it sends no request and writes no task text.
It verifies the approved checklist for D and P.
It records the separate prompt-guidance hash for P.
It does not prove what a runner actually receives or whether an intervention works.

Example with a locally created practice file:

```powershell
python research/phased-study/phase-03/prepare_trial.py `
  --task-file path/to/practice-request.txt `
  --expected-task-sha256 THE_64_CHARACTER_SHA256 `
  --condition P --task-id PRACTICE --run-id PRACTICE-P-01
```

Replace the placeholder hash before running the command.
The researcher chose to proceed with the selected prompts despite uncertainty about the agreement.
The agreement does not explicitly discuss hosted inference of individual prompts.
See the [dataset-use note](arena-dataset-use.md).
This utility does not resolve rights or connect to any model.

## Before the comparison runs

1. Record the dataset terms, the researcher's decision, and any later clarification.
2. Review and freeze the candidate instructions for the development comparison.
3. Specify the required journeys, fixture rules, and evaluation states for each task.
4. Identify the exact model-runner configurations and their effective instructions.
5. Define the time limit, repetitions, failure handling, and result storage.
6. Keep independent evaluation materials out of generator workspaces.
7. Record each attempted run and preserve its artifact or failure.

The earlier protocol gives a proposed full-batch design.
Development outputs remain exploratory if the team changes packages after inspecting them.
The input checker does not start a run or install an intervention.
The separate development runner can submit one attempt to the Codex CLI.
See the [development run record](development-run-plan.md).
The [initial observations](initial-development-results.md) cover one task and one automated page state.
The [task contracts](task-contracts-draft.md) and [manual review form](manual-review-template.md) are drafts for independent review.
`audit_exploratory_batch.py` can scan preserved static entry points after the batch stops.
`inspect_self_report_batch.py` describes recognizable model claims without judging their accuracy.
Both keep unassessed attempts in their ledgers.
`verify_exploratory_batch.py` checks the local inputs, requested configuration, and recorded artifact hashes.
It cannot observe hidden provider instructions or prove what the service received internally.

## Local manual review view

After generation stops, `prepare_review_cases.py` creates condition-masked copies of available static pages.
It verifies copied file hashes and keeps the run-to-case mapping in a separate local file.
It excludes project instructions, plans, self-reports, `.git`, and `node_modules`.
If an excluded file is needed by the site, record the affected review as unassessable.
Pages without an `index.html` need a separate, documented build procedure.
Pages with uncompiled JSX or TypeScript entry points also need a suitable build or runtime.
The automated preflight does not treat a blank rendered page as an accessibility pass.

Run `serve_review_cases.py` to open a loopback-only review index.
Each case uses a separate local origin so root-relative assets can load.
The index hides condition labels but cannot guarantee blinding.
Page content or prior knowledge can reveal the condition.
The manual browser is not subject to the automated audit's network blocking.
Record the network policy and any external content used during human review.

## Check the utility

The unit tests use synthetic task text and local checklist files.
They do not call an AI model or use the selected Arena task texts.

```powershell
python -m unittest discover -s research/phased-study/phase-03 -p 'test_*.py' -v
```
