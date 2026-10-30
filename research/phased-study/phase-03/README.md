# Phase 3: prepare the first comparison

**Status:** Offline preparation. The benchmark has not run.
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
Do not use the selected Arena tasks with a hosted model until the source terms are clarified.
This utility does not resolve rights or connect to any model.

## Before the comparison runs

1. Resolve the Arena dataset terms for the intended hosted providers and publication.
2. Review and freeze the candidate instructions for the development comparison.
3. Specify the required journeys, fixture rules, and evaluation states for each task.
4. Identify the exact model-runner configurations and their effective instructions.
5. Define the time limit, repetitions, failure handling, and result storage.
6. Keep independent evaluation materials out of generator workspaces.
7. Record each attempted run and preserve its artifact or failure.

The earlier protocol gives a proposed full-batch design.
Development outputs remain exploratory if the team changes packages after inspecting them.
The Phase 3 utility does not start a run or install an intervention.

## Check the utility

The unit tests use synthetic task text and local checklist files.
They do not call an AI model or use the selected Arena task texts.

```powershell
python -m unittest discover -s research/phased-study/phase-03 -p 'test_*.py' -v
```
