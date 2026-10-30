# Phased experiment roadmap

**Status:** Working plan, 30 October 2026. Exploratory runs have started; the final benchmark has not run.
The numbered phases below clarify the requested sequence.
They do not change the selected task texts.

| Phase | Purpose | Status and exit condition |
| --- | --- | --- |
| 1 | Establish the five selected requests and the study plan. | All five requests are selected. The full study plan remains a draft. |
| 2 | Review the checklist and draft the exact intervention wording. | Checklist 0.2.0 is approved by the researcher. Specialist review and intervention wording remain open. |
| 3 | Produce baseline and prompt-guidance development runs. | Fourteen scheduled turns completed, one failed, and one supplemental turn completed. Nine initial static scans are available. |
| 4 | Build and assess the skill package. | Draft instructions exist. Diagnostic implementation, integration, and S comparison remain open. |
| 5 | Build and assess the reviewer agent and host gate. | Draft instructions and schemas exist. The study gate, integration, and A comparison remain open. |
| 6 | Combine prompt guidance, skill, and reviewer. | Proposed design only. The combined package and X comparison remain open. |
| 7 | Freeze the protocol and run the full comparison. | Final protocol, independent review, full multi-runner batch, and analysis remain open. |

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
- [Researcher checklist approval](phase-02/checklist-approval.json).
- [Intervention design review](phase-02/intervention-design-review.md).
- [Candidate intervention files](phase-02/interventions/README.md).
- [Per-item review ledger](phase-02/checklist-review-ledger.json).
- [Current checklist](../accessibility/master-action-checklist.md).
- [Previous checklist snapshot](../accessibility/versions/0.1.0/master-action-checklist.md).

The earlier PDF contains checklist version 0.1.0.
The researcher approved the current Phase 2 checklist, version 0.2.0.
Independent expert review of its content remains open.
The Arena agreement restricts transfers, but it does not explicitly discuss hosted inference of individual prompts.
The researcher chose to proceed with the selected prompts despite that uncertainty.
See the [dataset-use note](phase-03/arena-dataset-use.md).

[Phase 3 preparation](phase-03/README.md) describes the B, D, and P comparison and its offline input checker.
