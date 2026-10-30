# Execution plan: AI website accessibility study

> An expanded draft with candidate prompts, metrics, and diagrams is available in
> [the experiment protocol package](experiment-protocol-2026-10-30/README.md).
> Both plans remain proposals until the research team approves a final protocol.

> The [phased study roadmap](phased-study/README.md) tracks the current Phase 2 work.
> The earlier protocol and PDF describe checklist version 0.1.0.

Date: 2026-10-29. Status: draft for discussion. The five task inputs are selected. The experimental conditions, run budget, test plan, and analysis have not been finalized or registered. No study result is claimed here.

## The objective

Investigate how a defined accessibility intervention changes the websites produced for the five selected requests. Compare the baseline, a direct accessibility-guidance control, and the proposed prompt, skill, agent, and combined packages. Record functionality, accessibility, intervention behavior, and resources separately.

The same original task message must be used for each condition for a given task. One run is one independently generated website in a fresh session. A task, a model, and a runner are not interchangeable units. If a runner hides its model or instructions, record the combination and its unknowns.

## Phase 0: Resolve rights and agree the scope

**Done:** Five Arena first messages were selected, and their UTF-8 hashes and source identifiers were recorded in the local workspace. A private repository and public task index exist. No generated benchmark outputs exist yet.

**Before sending those messages to hosted models:** Clarify how the [WebDev Arena agreement](https://huggingface.co/datasets/lmarena-ai/webdev-arena-preference-10k) applies to submission to providers, publication, sharing outputs, and collaboration. Its terms restrict transfers of the dataset. The scope of individual prompt use is an unresolved question, not an established permission or prohibition.

Agree on the model-runner combinations, available budget, and whether a human answers the verification questions. Codex and Antigravity are possible runners; the actual models and versions must be recorded. Comparing two model-runner bundles does not isolate the model from the runner.

The selected set is purposive and small. One request already asks for accessible contrast and semantic HTML. The requests differ in scope and technical detail. Do not claim they represent all website requests or all users. Public training-data exposure is unknown.

**Exit:** Rights for the intended use are clarified, the task hashes still match, and the scope and answer policy are written down.

## Phase 1: Build and validate the evaluation

For each task, write a small, reviewable test specification before viewing comparative outputs. Map each check to a task requirement or an applicable WCAG 2.2 criterion. Keep the test and its expected outcomes separate from the generator's instructions.

| Task | Proposed core journey | Examples to review |
| --- | --- | --- |
| Services page | Navigate the page and use its tabbed content. | Keyboard access, tab name and state, structure, contrast, and the requested order action. |
| Consulting page | Navigate content and use the page's relevant calls to action. | Heading structure, focus, contrast, and motion. The source already asks for some accessibility. |
| Cinema | Find a film and choose a screening and time. | Accessible names, selection states, keyboard use, and confirmation where implemented. |
| Dashboard | Add or edit a task and interact with the task board or filters. | Keyboard use, applicable alternatives to dragging, control states, and meaningful chart information. |
| Portfolio | Navigate between the featured project and about content. | Headings, landmarks, link names, visible focus, and image alternatives where relevant. |

These are starting points, not finalized tests. A task may allow different valid designs. Do not demand a specific ARIA attribute when native behavior or another conforming method meets the relevant requirement. If a required feature is missing, record a functionality failure; do not treat it as a passed accessibility check.

Create Playwright checks for the agreed journeys and relevant rendered states. Decide whether to add axe-core, then pin its version, rule configuration, browser, viewport, and environment. Prepare a manual checklist for keyboard, focus, labels, content meaning, and other applicable concerns. Use assistive technology and independent review where available; record who reviewed what.

Validate the evaluator on separate known-good and known-bad fixtures, including native controls and dynamic states. Check that it catches deliberate defects and accepts valid alternatives. Record false positives, test failures, and unresolved checks. The current local browser pilot is not a full evaluator for the five tasks.

**Exit:** The task rubrics, fixture checks, manual form, and evaluation environment are reviewed and versioned. [W3C](https://www.w3.org/WAI/test-evaluate/tools/selecting/) and [Playwright](https://playwright.dev/docs/accessibility-testing) explain why automated checks need human review.

## Phase 2: Build the intervention packages

Develop against separate examples and fixtures. We already know the selected task prompts, so do not describe them as fully blind or contamination-free. Do not give task-specific evaluation answers to the generator during the study.

1. **Prompt guidance:** Define the requested plan, accessibility considerations, questions, and response behavior. Adapt the guidance to each runner's supported instruction format. A prompt-level pause is advisory unless a host enforces it.
2. **Skill:** Package the procedure and any tools with clear activation instructions and versioned inputs and outputs. Test whether each runner discovers and actually invokes it.
3. **Validation agent:** Define what it can inspect, its decision and evidence format, and whether its decision is merely advisory or enforced. Keep the final evaluator separate from the intervention agent.
4. **Combined:** Specify how the three packages interact without contradictory or duplicate gates.
5. **Control:** Prepare direct accessibility guidance without the Socratic quiz, with similar substantive accessibility coverage where feasible.

Define the answer policy, number of attempts, timeouts, overrides, and what happens when no question is produced. Record whether code or files were produced before an expected gate. Test flawed and valid plans, empty inputs, bypass attempts, and host enforcement on fixtures. A quiz answer does not by itself establish that the plan or output is correct.

[CodeA11y, CHI 2025](https://doi.org/10.1145/3706598.3713335), is a related developer-tool study. [Buçinca et al., CSCW 2021](https://doi.org/10.1145/3449287), studied cognitive forcing in a different human decision setting. They motivate these designs; they do not validate this intervention.

**Exit:** Each package has a version and hash. Its actual invocation, decision behavior, limitations, and fixture results are recorded.

## Phase 3: Freeze a practical study protocol

Proposed conditions:

| ID | Condition |
| --- | --- |
| B | Baseline: original task, no study-specific accessibility intervention. |
| C | Direct accessibility checklist or guidance. |
| P | Prompt guidance only. |
| S | Skill package only. |
| A | Validation-agent package only. |
| X | Combined prompt, skill, and agent package. |

These compare packages against the baseline. They do not isolate all interactions between the three mechanisms. If the main claim concerns the quiz itself, add a plan-only control and a comparable plan-plus-quiz condition. A full three-factor interaction analysis requires all eight combinations of prompt, skill, and agent.

Before the comparison, decide and record the model-runner configurations, settings, repetitions, answer policy, randomized order, time and token limits, allowed setup actions, recovery rules, and primary outcome. Keep the same environment where feasible. Record hidden settings as unknown instead of assuming they match.

For scale, five tasks times two model-runner combinations times six conditions times three independent runs is **180 generated websites**. This is an illustration, not an agreed budget or a power calculation. A smaller pilot can establish feasibility but limits the comparison; select the actual scope before collecting final data.

Use different development tasks for tool debugging. If the team first inspects baseline outputs from the five selected tasks and uses them to tune the intervention, label that work exploratory. Do not later portray those task results as an untouched evaluation.

**Exit:** A versioned protocol records the decisions, evaluation criteria, schedule, and deviations policy before the comparative batch begins.

## Phase 4: Generate and preserve each run

For each scheduled task, model-runner combination, condition, and repetition:

1. Start a fresh session and clean output directory. Verify the original task text against its recorded hash.
2. Apply only the designated study condition. Record persistent runner settings and any inaccessible context.
3. Send the original task once. For a condition with a verification gate, record the planned additional exchange and who answers. Do not silently add task-specific follow-ups to the baseline.
4. Save the initial project, transcript where permitted, intervention files and hashes, model and runner identifiers, timing, tool calls, gate decisions, and any errors.
5. Preserve the generated artifact before repair or evaluator feedback. If generation, build, or launch fails, record it; do not discard or silently replace the run.

Randomize or counterbalance the order within task and runner when feasible. Hosted services may change or produce different outputs; preserving settings and inputs supports procedural reproducibility, not a guarantee of identical output.

Keep source prompts, private transcripts, and unreviewed artifacts in the local ignored `private/` area or another appropriately controlled location. The private repository's `docs/` directory is the public Pages source.

**Exit:** Every scheduled attempt has a unique ID, preserved artifacts or a documented failure, and a complete run record where information is available.

## Phase 5: Evaluate each preserved artifact

1. **Build and functionality:** Record setup, launch, and the required task journey. Use the same rule for all conditions. Distinguish a missing feature from an environment or evaluator failure.
2. **Automated accessibility:** Run the agreed Playwright assertions and, if selected, axe on the same defined states. Save raw reports, tool versions, rule IDs, affected nodes, impact labels, and incomplete checks.
3. **Human review:** The researcher inspects relevant keyboard, focus, content, and visual behavior using the recorded checklist. Mask condition labels where feasible; record limitations and uncertainty. If another qualified reviewer or screen-reader user is available, document their separate role and any disagreements.
4. **Intervention and cost:** Record actual skill and agent activation, gate decisions and bypasses, time, retries, tokens, and cost when available.

Record individual checks as pass, fail, not applicable, or unassessable with a reason. Do not equate an axe impact label with a WCAG severity category. A zero-violation scan does not establish WCAG conformance. A single researcher review is not an independent expert audit or a user study.

**Exit:** Each run has functionality results, automated findings, human review status, evidence paths, and explicit unknowns.

## Phase 6: Compare and report

One possible primary outcome is the fraction of attempted runs that both complete the prespecified core journey and pass the selected applicable automated accessibility checks. This is a combined operational measure, not a universal accessibility score. Keep functionality and accessibility findings separate as well. Confirm the primary outcome before the final batch.

Count failed builds and missing required journeys as failures of that combined outcome. Do not call them measured accessibility violations. Treat unavailable observations or evaluator errors as indeterminate when they prevent a decision. With N attempted runs, report pass/N and, when there are U indeterminate runs, the upper bound (pass + U)/N.

Show the individual task and model-runner results. Compare like tasks and configurations. Repeated generations of five tasks are not a larger independent sample of website tasks. Report practical differences, uncertainty, time, costs, failures, and counterexamples. Five purposively selected tasks support an exploratory conclusion, not a universal ranking or proof of a best method.

Publishing a generated site or its evidence requires a separate rights and privacy check. GitHub Pages serves static files; preserve the original runnable artifacts and document any static export or hosting limitation. Do not change the evaluated artifact silently to make it fit Pages. [GitHub Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

Human automation bias, learning, and workload are separate questions. Claiming an effect on them needs a participant study with defined measures, consent, and any applicable institutional review. The [ProjectEval paper](https://aclanthology.org/2025.findings-acl.1036/) provides a project-level interaction-evaluation precedent, not an accessibility or human-bias result for this study.

**Exit:** The private evidence record is complete; any public results are clearly labeled, supported by the underlying permitted evidence, and consistent with the actual scope.

## Decisions for our next discussion

- Who or what answers SPV questions during each run?
- Which model-runner combinations and repetition budget are available?
- Is the primary question about the combined package, the individual packages, or the quiz mechanism?
- What exact core journey and checks will be required for each task?
- Can an independent accessibility reviewer or assistive-technology review be included?
- What rights clarification and publication policy are needed for the original prompts and generated artifacts?
