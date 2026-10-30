# Phased experiment roadmap

**Status:** Working plan, 30 October 2026. No benchmark has run.
The numbered phases below clarify the requested sequence.
They do not change the selected task texts.

| Phase | Purpose | Status and exit condition |
| --- | --- | --- |
| 1 | Establish the five selected requests and the study plan. | The requests are selected. Baseline outputs do not yet exist. |
| 2 | Review the checklist and draft the exact intervention wording. | In progress. Resolve expert review, task contracts, runner capabilities, and source rights before use. |
| 3 | Produce baseline and prompt-guidance development runs. | After Phase 2 decisions, compare B, D, and P using the same task text. |
| 4 | Build and assess the skill package. | Compare S with B and D; record actual skill and tool activation. |
| 5 | Build and assess the reviewer agent and host gate. | Compare A with B and D; record decisions, retries, and blocks. |
| 6 | Combine prompt guidance, skill, and reviewer. | Compare X with B and D; preserve the exact package and its extra work. |
| 7 | Freeze the protocol and run the full comparison. | Evaluate every scheduled attempt and report limitations. |

The user named Phase 3 twice.
The table assigns one number to each distinct phase.
The complete test is Phase 7.

## The comparison conditions

| ID | Study input and package |
| --- | --- |
| B | Original task alone. |
| D | Original task plus the common checklist instruction and full checklist. |
| P | D plus project or system-level plan guidance. |
| S | D plus the accessibility skill and its available diagnostic. |
| A | D plus a separate plan reviewer and a host-enforced gate. |
| X | D plus P, S, and A together. |

The complete input changes when guidance is added.
The original task text remains byte-for-byte unchanged.
The D condition shows what the checklist package alone does.
P, S, A, and X are candidate packages, not proven improvements.
The exact role or channel for each model must be recorded.

## A key design boundary

Treat Phases 3 to 6 as development and exploratory work if the team changes packages after seeing results.
Freeze the exact Phase 7 conditions and evaluation before the final batch.
Start fresh sessions and do not carry earlier outputs into those sessions.
Do not reuse exploratory artifacts as final-batch results after adapting the packages or tests.
The proposed 180-attempt final batch excludes the earlier development runs.
The five selected prompts are already known to the team.
Fresh sessions do not make those tasks a previously unseen holdout.
Five purposively selected tasks do not establish a universal best method.

The current proposed SPV flow has the AI answer its own plan questions.
This keeps one initial user submission per run.
A reviewer agent can make extra internal model calls.
This does not measure human automation bias or human comprehension.
A human-question condition requires a separate design and any applicable ethics review.

## Phase 2 materials

- [Checklist review and change record](phase-02/checklist-review.md).
- [Candidate intervention files](phase-02/interventions/README.md).
- [Per-item review ledger](phase-02/checklist-review-ledger.json).
- [Current checklist](../accessibility/master-action-checklist.md).
- [Previous checklist snapshot](../accessibility/versions/0.1.0/master-action-checklist.md).

The earlier PDF contains checklist version 0.1.0.
The current Phase 2 checklist is version 0.2.0 and remains a research draft.
The original Arena agreement requires clarification before hosted submission or release of its source text.
