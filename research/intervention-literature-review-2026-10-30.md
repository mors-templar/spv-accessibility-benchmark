# Research review: instructions, skills, and agents for accessible web development

**Date:** 2026-10-30. **Status:** exploratory literature review for discussion. This review does not finalize a study design, build an intervention, or run a benchmark.

## Main conclusions

1. Closely related work already exists. CodeA11y used accessibility instructions, three specialized agents, and an accessibility checker. It evaluated the complete package with developers. A new study must explain its specific difference from this work.
2. Some studies find benefits from explicit accessibility instructions. That does not show that a skill, reviewer agent, or Socratic gate will add value beyond those instructions.
3. Recent skill benchmarks report different results. Their tasks, skills, models, and measures differ. Some report regressions and extra cost. Most skill-specific sources below are preprints; peer-reviewed status was not established for those versions.
4. A human reviewing a plan and a model criticizing its own output are different interventions. Claims about human overreliance require observations of human decisions.
5. A reviewer agent can miss or invent issues. Its verdict needs independent checking. A successful tool call or generated plan is not proof of accessibility.

These are interpretations of the literature, not results for our project. Our five selected tasks and checklist are unchanged.

## Scope and source method

This is a targeted, non-systematic review of accessible code generation, skill evaluation, agentic software development, and human plan review. Searches included peer-reviewed conference and journal papers, recent preprints, and primary technical documentation. Methods and results sections were inspected where accessible. The review is not exhaustive, a systematic review, or a claim of novelty. The source URLs and version numbers below support follow-up reading.

Sources are grouped by evidence type. A published peer-reviewed study is evidence for its own sample and methods. A preprint is useful but its peer-review status is unconfirmed here. Documentation describes a format or product behavior; it is not an effectiveness study. Links were checked on 2026-10-30.

## What the terms mean

| Term | Meaning for discussion | Important distinction |
| --- | --- | --- |
| Prompt-level guidance | Instructions given to the model or loaded into its working context. They can request accessibility practices or plan reflection. | A project instruction file is not automatically the model's system message. Its actual role and priority depend on the runner. Instructions alone do not guarantee a stop before code. |
| Agent skill | A reusable package of instructions and, optionally, scripts and references. | A skill need not contain tools or an enforced gate. A runner may discover, load, or ignore it in different ways. |
| Agent or sub-agent | A model-driven component with a defined task, context, and possible tools. A sub-agent is delegated part of another workflow. | A second role or model call does not make its conclusions independent ground truth. |
| Plan review | Examination of an intended sequence or accessibility decision before implementation. | Review can be by a human, by the same model, by a separate reviewer, or by a deterministic rule. Those are different mechanisms. |
| Post-generation review | Examination of generated code or a running site. | This measures a different stage from pre-code plan review. A correct-looking plan need not produce an accessible site. |
| Harness | The surrounding runner that loads instructions, provides tools and permissions, captures traces, and controls execution. | Model and harness effects can be entangled. A model name alone does not describe the full configuration. |

The [Agent Skills specification](https://agentskills.io/specification) defines a directory with `SKILL.md` and optional resources. It is a format specification, not evidence that a particular skill works. The [Gemini CLI documentation](https://geminicli.com/docs/cli/gemini-md/) describes `GEMINI.md` as project context. The [official OpenAI Codex prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide) describes discovered `AGENTS.md` files as user-role context messages in that documented configuration. Actual behavior must be checked for the version and host used; this does not establish identical behavior in other products.

## Peer-reviewed studies: accessibility and agent design

### CodeA11y: accessibility instructions plus specialized agents

[Mowar et al., CHI 2025, CodeA11y](https://arxiv.org/html/2502.10884): a formative study involved 16 developers. The authors then built a GitHub Copilot extension with a responder agent, an accessibility-linter correction agent, and a reminder agent. The paper explains each agent's role, context sources, instruction highlights, and handoffs. In a separate within-subjects comparison, 20 novice developers used CodeA11y and a baseline assistant on web tasks. The reported results differed by task.

**Relevance:** This is a close precedent for accessibility guidance, multiple agent roles, lint feedback, and human review. It shows the importance of inspecting the meaning of code and any manual steps, not only the presence of an attribute. The evaluation tests the CodeA11y package as a whole; it does not by itself establish which of its three agents caused an outcome. Its tasks and participants also differ from our selected website requests.

### Guriţă and Vatavu: prompting and self-reflection for accessible interfaces

[When LLM-Generated Code Perpetuates User Interface Accessibility Barriers, W4A 2025](https://mintviz.usv.ro/publications/2025.W4A.3.pdf): the authors crossed two model choices with accessibility-agnostic and accessibility-oriented prompts, with ten initial UIs per combination. This produced 40 initial UIs. They then requested self-reflection and improvements, producing a further 40. Their evaluation included automated checks and expert review for selected criteria.

**Relevance:** This is a direct precedent for comparing ordinary and accessibility-oriented instructions. It also treats self-reflection as a separate step. Their banking-interface task, models, prompt content, selected criteria, and generated outputs limit transfer to our five tasks. Do not read the additional 40 revised UIs as independent initial generations.

### GenA11y: a reviewer needs appropriate evidence

[He, Huq, and Malek, FSE 2025, GenA11y](https://ics.uci.edu/~seal/publications/2025_FSE_GenA11y.pdf): the authors studied detection on existing websites. Their system extracts relevant page information and prompts an LLM to inspect accessibility. An ablation compared a base model, extraction only, prompting only, and their combined system. The paper reports that missing visual or structural context can cause omissions or incorrect reports.

**Relevance:** This is a useful example of defining a reviewer by its inputs, outputs, and evidence. Source HTML alone can omit information needed to judge rendered contrast or the meaning of an image. This paper evaluates detection, not whether an agent produces accessible websites from our tasks.

### Accessible components with explicit instructions

[Abu Doush and Kassem, Universal Access in the Information Society, 2025](https://link.springer.com/article/10.1007/s10209-025-01250-2): the accessible abstract describes 11 component types and four model products. The authors used a detailed foundation prompt, a component request, manual keyboard and screen-reader checks, and follow-up prompts for identified issues.

**Relevance:** The study gives a component-level example of documenting instructions and manual testing. This review relies on its abstract; the full methods and detailed results were not independently inspected. Its guided component tasks do not establish an effect for our proposed packages.

### ChatDev: roles, handoffs, and ablations

[Qian et al., ACL 2024, ChatDev](https://aclanthology.org/2024.acl-long.810/): the system organizes software development into stages and assigns agents roles for communication and review. The authors describe the sequence and compare variants with phases or roles removed. They also discuss time and token use.

**Relevance:** The useful precedent is to specify the actual roles, handoffs, and component comparisons. Its software tasks and quality measures are not an accessibility study. More roles or a longer process cannot be assumed to help our tasks.

### SWE-agent and Agentless: interfaces and simpler comparators

[Yang et al., NeurIPS 2024, SWE-agent](https://proceedings.neurips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html) studies how an agent's commands and environment interface affect repository-level software engineering. It evaluates on software-repair benchmarks and examines interface choices.

[Xia et al., FSE 2025, Agentless](https://lingming.cs.illinois.edu/publications/fse2025.pdf) uses a staged localization, repair, and validation pipeline. It compares the pipeline with agent-based software-repair approaches and studies components, including generated reproduction tests.

**Relevance:** The runner and its tools are part of a system's behavior. A simpler staged process can be a meaningful comparison. Neither paper proves which architecture works best for accessible website generation.

### Self-Refine: model feedback without a separate agent

[Madaan et al., NeurIPS 2023, Self-Refine](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html) uses one model to generate, provide feedback, and revise. The authors compare iterative feedback and refinement with one-step generation over several tasks.

**Relevance:** A critique-and-revision workflow can exist without a multi-agent system or a human quiz. Its results do not prove that self-critique detects WCAG failures or improves our target outputs.

### Validating the validator

[Shankar et al., UIST 2024, Who Validates the Validators?](https://people.eecs.berkeley.edu/~bjoern/papers/shankar-validators-uist2024.pdf) studies human involvement in checking LLM-based evaluators against evaluation requirements. It addresses a general problem: an evaluator generated with an LLM can make errors itself.

**Relevance:** This is a reason to review a validation agent's misses and false alarms rather than equating its verdict with correctness. It is not a WCAG validation study.

### Human cognitive forcing and plan review

[Buçinca, Malaya, and Gajos, CSCW 2021](https://arxiv.org/html/2102.09692): the authors studied cognitive forcing interventions with 199 people in AI-assisted decision tasks. They compared forcing designs with explainable-AI conditions and a no-AI baseline. They report reduced overreliance in their setting, alongside less favorable subjective ratings for the most effective designs.

**Relevance:** This supports investigating human cognitive forcing and its usability costs. It does not establish effects for accessibility coding or for a model answering its own questions.

## Recent preprints: useful but not established as peer-reviewed here

### SkillsBench: paired skills evaluation

[Li et al., SkillsBench, arXiv v4](https://arxiv.org/html/2602.12670v4): this version compares a no-skills condition with curated skills on 87 terminal tasks across 18 model-harness configurations. The study uses reproducible environments and task verifiers. Its diagnostic comparisons also consider self-generated skills. The authors report that effects differ across tasks and harnesses, and identify cases where skills hurt.

**Relevance:** The study makes a skill the object being evaluated and records whether the harness makes it available. Its tasks are not a web-accessibility benchmark, and its deterministic checks do not replace accessibility review. The authors note limits for GUI and multi-agent settings.

### SWE-Skills-Bench: matched software tasks

[Han et al., SWE-Skills-Bench, arXiv v2](https://arxiv.org/html/2603.15401v2): the 27 October 2026 revision describes 98 skills, ten requirements per skill, four agent-model configurations, and 3,920 paired requirement/configuration evaluations. Each pair uses the same repository, requirement, environment, and verifier, with or without the skill. In v2 the target skill is explicitly invoked. The authors report that 92 of 98 skills did not show a statistically significant overall effect under their classification.

**Relevance:** This is a useful example of matched comparisons and of measuring skill effects by model and harness. A non-significant result is not proof of no effect. The requirements are derived from the skills, so the task set differs from independently collected website requests. Executable tests measure the paper's chosen requirements, not all aspects of product quality.

**Version warning:** The [earlier v1](https://arxiv.org/html/2603.15401v1) describes one configuration and autonomous skill discovery. It should not be combined with v2's four-configuration numbers or explicit invocation. One paper-index service returned v2 metadata with v1 text; the v2 record above was checked directly against arXiv.

### WebDev-Skills-Bench: length controls and conflicting outcomes

[Yang and Ding, Signal or Noise?, arXiv v1](https://arxiv.org/html/2608.23067v1): this study evaluates web-development skills against matched no-skill runs. It also uses an approximately length-matched irrelevant skill and removes parts of target skills in an ablation. The paper reports negative average functional performance effects for its studied configurations, with different effects for individual skill, project, and model combinations.

**Relevance:** Added context length, added knowledge, and the specific skill instructions are distinct possible explanations. The authors state that their Playwright evaluation measures functional correctness rather than accessibility, visual fidelity, or user experience. Therefore its findings are not evidence that accessibility skills harm accessibility.

### Plan-focused cognitive forcing

[Ghosh et al., AI-assisted writing plans, arXiv v1](https://arxiv.org/html/2601.18033v1): the authors compared assumption questions, what-if questions, both, and a no-forcing control. Their online study included 214 participants; a separate interview study included 12. Participants saw fixed AI-generated plans and drafts for writing tasks, including planned errors.

**Relevance:** This is a close precedent for questioning an AI plan before accepting its output. It predates any proposed claim that plan-focused questioning itself is new. Its writing tasks, fixed materials, and human participants differ from an autonomous coding-agent experiment. The authors explicitly caution against direct transfer to technical domains.

### Multi-agent scaling

[Kim et al., Towards a Science of Scaling Agent Systems, arXiv](https://arxiv.org/abs/2512.08296) compares single- and multiple-agent architectures under controlled settings and reports task-dependent benefits and coordination costs.

**Relevance:** It is counterevidence to an assumption that more agents always improve results. Its benchmark tasks and architectures are not our proposed accessibility intervention. Its online versions have changed; cite an exact version for any numerical claim.

## Practical prior art and standards

- [Community Access: Accessibility Agents](https://github.com/Community-Access/accessibility-agents) is an existing community software project with accessibility-focused agent and skill materials. It is practical prior art, not a peer-reviewed effectiveness result. Its contents, version, licensing, and compatibility would need separate review before use or comparison.
- [W3C WCAG 2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/) defines the target accessibility criteria. [W3C ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) provides informative patterns. These are standards and guidance, not studies demonstrating an intervention effect.
- [W3C evaluation guidance](https://www.w3.org/WAI/test-evaluate/) states that no tool alone determines whether a site meets accessibility standards. Human judgment is needed for many questions.

## What this means for our technical discussion

### Prompt guidance

Accessibility instructions have a direct research precedent. The open questions are which instructions to include, where the runner loads them, and whether the instruction requests a plan, an internal reflection, a human response, or some combination. The exact delivery mechanism matters when describing the work. A text instruction asking for a pause is not a demonstrated host-enforced gate.

### Skills

A skill can hold a reusable procedure, reference materials, and optional code. It is a packaging and workflow mechanism, rather than a guarantee of better results. The skill benchmarks show the importance of task fit, activation, cost, and the ability to distinguish the effect of content from the effect of extra context. They do not identify an established best accessibility skill for our study.

### Review agents and sub-agents

CodeA11y demonstrates accessibility-specific agent roles. GenA11y shows how a reviewer can use structured page information. The unresolved questions include what a reviewer receives, whether it assesses a plan or a rendered site, how it supports a finding, and whether it merely advises or can prevent later actions. An agent's label or confident verdict is not evidence that its judgment is correct.

### Combined approach

Combining instructions, a skill, and a reviewer changes several mechanisms at once. It may improve outcomes, add cost, have no measurable benefit, or introduce errors. The papers provide reasons to investigate each possibility. They do not establish that the combination is best.

### Human versus model review

Human plan questioning can investigate reliance, critical engagement, or usability when those behaviors are measured. Model self-questioning instead studies model-side critique or refinement. Both can be useful, but they support different claims. A researcher manually checking final websites does not on its own measure automation bias.

## Questions the literature leaves open for our project

These are questions for later discussion, not decisions made in this review:

1. Which exact plan-level accessibility decisions matter for the selected requests, and which are already addressed by ordinary accessibility guidance?
2. What evidence would distinguish a useful skill from a longer instruction file containing the same information?
3. Does a reviewer examine plans, generated artifacts, running behavior, or some combination? How are its claims checked?
4. Is the intended Socratic interaction human-facing, model-facing, or are these distinct versions of the concept?
5. How would the work differ from CodeA11y, prior plan-focused cognitive forcing, existing accessibility agent packages, and direct accessibility prompting?
6. How can later work separate the effect of information, planning, tools, review, extra model calls, and added execution time?
7. Which claims can the five selected tasks support, given their differing scopes and the existing accessibility language in task 8?

Before collecting comparative results, the team still needs to settle the intervention definitions, evaluation procedures, rights to the selected source prompts, and appropriate claims. No unique novelty or improvement has been established by this review.
