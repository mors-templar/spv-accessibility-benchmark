# Phase 2: intervention design review

**Status:** Candidate wording for discussion, 30 October 2026.
The researcher approved checklist version 0.2.0.
The intervention wording and study conditions have not been approved or frozen.
The final benchmark has not run. Exploratory Phase 3 generation has started.

## 1. The baseline and shared checklist

Use the five selected task messages without edits.
Condition B receives the original task as its only study user message.
Condition D adds the common checklist instruction and the complete approved checklist.
Conditions P, S, A, and X receive that same D message.
They also receive the respective intervention below.

The approved checklist contains 188 items and an illustrative section on the task types.
That extra material can influence the generator.
The D-to-B comparison measures the complete checklist and self-report package.
It does not isolate the effect of each individual checklist item.

The [common checklist instruction](interventions/checklist-instruction.txt) sets self-report rules.
It distinguishes WCAG-derived outcomes, guidance, and study activities.
It asks for evidence and labels unknown checks as unassessed.
The model's report is a claim for independent review, not the evaluation result.

## 2. P: prompt guidance

The exact draft is [prompt-guidance.txt](interventions/prompt-guidance.txt).
It asks the generator to list features and risks, then ask and answer plan questions.
It requests an observable plan file before implementation when writing is available.
For a chat-only runner, it requests the plan in the response before code.
It does not add a host gate or a new diagnostic tool.

**Main comparison:** P versus D.
It measures this guidance package under the recorded delivery channel.
The same wording in a project instruction file and an API system message uses different channels.
Record those channels and analyze them separately.
If plan execution is hidden, record the relevant process result as unknown.

## 3. S: skill

The exact draft is [spv-accessibility/SKILL.md](interventions/spv-accessibility/SKILL.md).
It packages the planning workflow in the [Agent Skills format](https://agentskills.io/specification).
It asks the generator to use an advisory `verify_plan` tool when available.
The host provides the run ID, task ID, and checklist version from its schedule.
The model supplies the plan and question-answer pairs.

**Main comparison:** S versus D.
This compares the whole skill-and-tool package with the checklist condition.
It cannot isolate skill packaging from the procedure or diagnostic.
Record actual activation and tool use, including unknown activation.
The diagnostic, provider adapters, and real skill behavior are not yet implemented or validated.

## 4. A: review agent

The exact draft is [reviewer-instruction.txt](interventions/reviewer/reviewer-instruction.txt).
A separate reviewer inspects the requested features, checklist, and proposed plan.
It returns `APPROVE`, `REVISE`, or `INSUFFICIENT_EVIDENCE`.
The reviewer must not approve missing or unresolved material behavior.

**Main comparison:** A versus D.
The proposed host permits writable implementation only after valid approval.
The host can deny file writes; it cannot prevent a model from emitting code as text.
The planned limit is two revisions after the first plan.
Record a block after the limit, and retain every decision.
Plan approval is not a completed-site accessibility result.

The [plan instruction](interventions/reviewer/plan-phase.txt),
[plan schema](interventions/reviewer/plan.schema.json),
and [decision schema](interventions/reviewer/decision.schema.json) define the draft interface.
The schemas alone do not enforce all host rules.
The host, read-only boundary, and reviewer still need implementation and fixture testing.

## 5. X: combination

X receives the same D message plus P, S, and A.
The host gate controls the transition to writable implementation.
The skill diagnostic remains advisory.
The study's human and browser evaluators remain separate from the reviewer agent.

**Main comparison:** X versus D.
This measures the combination as a package.
It does not prove that all three parts were individually necessary.
A full interaction study also needs P+S, P+A, and S+A conditions.

## 6. Illustrative example

Assume a separate practice request includes an expandable FAQ.
This example is not one of the five Arena prompts and has not been run.

- P asks how keyboard users will open the FAQ and records a proposed answer.
- S uses its skill procedure and calls the advisory diagnostic if the host provides it.
- A reviews the plan. Missing keyboard behavior can lead to a revision request.
- X combines those steps and requires host approval before a writable build phase.
- The independent evaluator later inspects the finished FAQ and records evidence.

The actual task determines which checks apply.
A missing feature, an unknown check, and an accessibility failure are different results.

## 7. Scientific rationale and limits

| Design choice | Supporting source | What it does not prove |
| --- | --- | --- |
| Compare checklist guidance with an unmodified request. | [Guriţă and Vatavu, W4A 2025](https://mintviz.usv.ro/publications/2025.W4A.3.pdf). | Their banking task and measures do not validate our checklist. |
| Investigate a reusable skill. | [Agent Skills specification](https://agentskills.io/specification) and [Ding et al., EMNLP 2026](https://aclanthology.org/2026.findings-emnlp.1427/). | A standard package format does not establish a performance gain. |
| Investigate accessibility-aware review. | [CodeA11y, CHI 2025](https://arxiv.org/html/2502.10884) and [GenA11y, FSE 2025](https://ics.uci.edu/~seal/publications/2025_FSE_GenA11y.pdf). | These systems differ from our plan reviewer and do not isolate its effect. |

The packages differ in added context, instructions, calls, and time.
Record these differences and avoid a causal claim about any one component.
Phases 3 to 6 are exploratory if the team changes packages after seeing outputs.
Freeze the final protocol before Phase 7.

The draft uses AI-generated questions and AI answers.
One-shot means one initial user submission; internal agent calls can follow.
This design does not test human review, comprehension, or automation bias.

## 8. Work remaining before a real run

- Review the wording and select the actual runner channels.
- Complete the task contracts and fixture policies.
- Clarify whether the Arena agreement permits hosted-model submission.
- Obtain the intended accessibility review and record reviewer qualifications.
- Build and validate each runner, diagnostic, and host gate in its planned phase.
- Freeze the evaluation and result handling before the final comparative batch.

The [candidate manifest](interventions/candidate-manifest.json) records current file hashes.
It is a draft manifest, not an approved or preregistered protocol.
