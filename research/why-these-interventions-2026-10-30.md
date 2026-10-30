# Why investigate prompts, skills, and review agents?

**Date:** 2026-10-30. **Status:** research-only analysis for discussion. No practice task, benchmark, or intervention was run in this work.

## What this document answers

The research question is why these three intervention avenues deserve investigation for accessible website generation. This document examines what the papers changed, what they measured, their results, and what those results do and do not justify.

**Main finding:** The literature supports each avenue as a reasonable candidate. It does not establish that all three must be used together, that their combination is optimal, or that a particular SPV implementation works. Those are hypotheses for future investigation, not conclusions to assume.

This is a targeted, non-systematic research review. Peer-reviewed articles, preprints, and vendor material are identified separately. The exact implementations, models, tasks, and measures differ between studies. Results cannot be transferred directly to our five website requests.

## The proposed causal roles

| Avenue | The problem it is intended to address | Intervention mechanism | What a positive result could mean |
| --- | --- | --- | --- |
| Prompt guidance | Accessibility may not be specified in a user's website request. | Place general accessibility requirements in the model's context. | The added instructions helped on the measured tasks and checks. |
| Skill | A short rule may not supply enough detail for complex or recurring work. | Package a reusable procedure, references, and optional tools for relevant situations. | The complete skill package helped under the tested conditions. Further comparisons are needed to separate packaging from the information it contains. |
| Review agent | A generator may miss an issue or inaccurately assess its own output. | Assign review to a separate role or process with defined evidence and access. | That reviewer workflow helped on the tested conditions. It does not follow that its every decision is correct. |
| Combined | Each avenue addresses a different possible failure. | Make guidance, procedures, and review available within a workflow. | The particular combination helped under the tested conditions. It does not automatically prove each part was necessary. |

These are proposed mechanisms. They overlap: a skill contains instructions, and an agent also uses instructions. A package can add information, steps, model calls, tools, and time at the same time. The research must avoid crediting one of those changes without a comparison that distinguishes it.

## 1. Why use accessibility instructions?

### Direct peer-reviewed evidence

[Guriţă and Vatavu, W4A 2025](https://mintviz.usv.ro/publications/2025.W4A.3.pdf), studied one banking-homepage request. They compared two models and two request variants: one accessibility-agnostic and one listing accessibility requirements. They generated ten initial interfaces per combination, or 40 initial outputs. Two accessibility experts and automated checks evaluated selected criteria. The models later produced 40 revisions after self-reflection.

The authors report that the **mean expert-assessed criterion violation rate** fell from 58% to 19% for accessibility-oriented requests. That is a difference of 39 percentage points in the study's reported aggregate, not a claim that 39% of websites were made compliant. The same paper's automated aggregate violation rate went from 15.93% to 17.32%, and individual criteria varied. The expert and automated measures have different scopes; neither is a complete accessibility judgment. The study used WCAG 2.1 and one application type, so its results are not estimates for our five tasks or WCAG 2.2 as a whole.

**Why it supports this avenue:** Explicit requirements can change what a model considers during generation, and the study observed improvements in several expert-assessed outcomes. It provides a reason to investigate guidance instead of assuming accessibility will be inferred.

**What it does not establish:** The study added requirements to the user request. It did not establish that a true system-role message is superior to a project instruction file, a user message, or a skill containing the same information. It does not show that instructions alone are sufficient.

### Additional peer-reviewed support

[CodeA11y, CHI 2025](https://arxiv.org/html/2502.10884), used accessibility-focused instructions as one part of a larger assistant. It added linter-informed correction and reminders for human work. In a later study with 20 novice developers, the authors reported better outcomes on some assessed component tasks than the baseline assistant. There was no comparable statistically significant improvement on their link-label task. The notification UI changed after the first eight participants, which the authors acknowledge as a source of variability.

**Interpretation:** This shows that an accessibility-aware assistance package is feasible and can help on some measured tasks. Because the package contains several features, it does not isolate the effect of instructions alone.

### Why delivery position matters

An `AGENTS.md` or `GEMINI.md` file is a runner-loaded project context mechanism. It is not automatically the same as a model API's system-role message. The [Codex documentation](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide) and [Gemini CLI documentation](https://geminicli.com/docs/cli/gemini-md/) describe different loading mechanisms. We should describe what each tested runner actually receives. A prompt instruction asking the model to pause is also not, by itself, evidence of host-enforced blocking.

## 2. Why use a skill?

### Peer-reviewed research foundation

[Ding et al., Findings of EMNLP 2026](https://aclanthology.org/2026.findings-emnlp.1427/), survey skill evaluation and identify separate questions of task success, retrieval and routing, skill generation, safety, and real-world use. They note gaps in cost, latency, error types, verifier reliability, and provenance. The survey is peer-reviewed; the individual benchmarks it discusses must still be assessed according to their own publication status and version.

The [Agent Skills specification](https://agentskills.io/specification) defines a reusable package with `SKILL.md` and optional scripts, references, and assets. The format supports structured reuse. It does not itself establish that a skill is activated, that its instructions are followed, or that it improves outcomes.

**Why it supports this avenue:** A skill is a practical way to package a focused procedure and resources for repeated use. For example, a skill could describe how to identify the relevant interaction pattern, check available evidence, and record uncertainties. That is a design hypothesis, not an implemented or validated skill in this document.

### Controlled skill studies: useful but conflicting

**[SkillsBench v4](https://arxiv.org/html/2602.12670v4), preprint:** The authors compare no-skill and curated-skill conditions across 87 terminal tasks and 18 model-harness configurations. Their reported mean pass rate was 33.9% without skills and 50.5% with curated skills, a 16.6 percentage-point difference on their verifiers. Their tasks and matched skills were curated; the authors identify a gap between this setting and ordinary skill use. Their evaluated tasks do not establish accessibility gains for web pages.

**[SWE-Skills-Bench v2](https://arxiv.org/html/2603.15401v2), preprint:** The authors compare the same requirement and repository state with and without a targeted skill across four agent-model configurations. They report 92 of 98 skills without a statistically detectable overall directional effect under their classification, and an aggregate pass ratio of 76.59% versus 76.93%. Lack of significance is not proof that a skill has zero effect. The authors derived requirements from each skill, which differs from independently chosen website prompts.

**[WebDev-Skills-Bench v1](https://arxiv.org/html/2608.23067v1), preprint:** Researchers compared matched web-development tasks with no skill, a relevant skill, and an approximately length-matched irrelevant skill. Across their four tested models, average Pass@2 decreased by 1.3 to 4.2 percentage points with the relevant skill. The metric measures the authors' functional Playwright checks, not accessibility, so the finding must not be presented as a measured accessibility regression.

**Interpretation:** A skill is worth studying because it may provide reusable, task-relevant procedural knowledge. The studies show outcomes depend on the skill, task, agent, and evaluator. They do not show that skill packaging independently outperforms the same accessibility knowledge delivered as plain instructions.

**Version warning:** SkillsBench v4 reports 87 tasks across eight domains. The peer-reviewed EMNLP survey describes an earlier SkillsBench snapshot with different counts. SWE-Skills-Bench v1 and v2 also differ in setup. Do not mix these counts or methods as one experiment.

## 3. Why use a reviewer or sub-agent?

### The need for independent evidence

[GenA11y, FSE 2025](https://ics.uci.edu/~seal/publications/2025_FSE_GenA11y.pdf), is a peer-reviewed accessibility-detection study. In an ablation on its accessibility-tool audit dataset, the paper reports 57 issues detected by its base model, 93 with extracted information, 104 with detailed prompting, and 127 with both. These are counts for that detection dataset, not a percentage of all WCAG failures or an experiment on generating our websites.

The authors describe why context matters. Rendered colors, font sizes, and images may not be available from raw HTML. Their evaluator also checks whether the reported elements and reasons match known issues.

**Why it supports this avenue:** A reviewer with relevant criteria and evidence from the actual page can identify issues a simple reading of source code might miss. This supports investigation of structured review and tool-provided observations. It does not isolate the effect of adding a second agent to website generation.

[CodeA11y](https://arxiv.org/html/2502.10884) is closer to that workflow: it combines a responder, correction agent, reminder agent, and checker feedback. Its complete package performed better on some tasks. Because the comparison evaluates the package, the result cannot establish how much improvement came from a particular agent.

### A direct accessibility-agent tradeoff

[Mishra et al., Agentic Web Accessibility Auditing, arXiv v2](https://arxiv.org/html/2609.09379v2), is a 2026 preprint. It studies a reviewer workflow using 250 page-criterion records derived from expert reports on scholarly platforms. Its reference worker recovered 67 of 78 reference-positive records, while 53 reported positives were absent from those reports. The authors report precision 0.56 and recall 0.86 for that configuration against their labels.

**Important limitations:** Missing findings in historical reports were used as inferred negatives, rather than independently checked negative cases. Agreement at page-criterion level does not prove that the agent identified the correct element. The sources, tools, and models also differ across some comparisons. This study supports a reviewer as a candidate, while showing why its confident findings require independent validation.

### Plan review versus code review

[Jiang et al., ACM TOSEM 2024](https://ligechina.github.io/My%20Papers/2024%20-%20TOSEM%20-%20Self-Planning%20Code%20Generation%20with%20Large%20Language%20Model.pdf), studied planning before code generation. In one HumanEval comparison with a fixed base model, the reported pass@1 was 48.1% for direct generation and 60.3% with self-planning. That is a 12.2 percentage-point difference, or the paper's 25.4% relative improvement. Its function-generation tasks and older model differ from our web tasks.

In contrast, [Review Beats Planning, arXiv v1](https://arxiv.org/html/2603.03406v1), a preprint, reports that a particular two-model plan-then-code workflow underperformed its single-coder baseline on HumanEval+, while code review and revision performed better. Its tasks were primarily single-function coding problems, and the review workflow used additional model calls.

**Interpretation:** Planning and review both have credible reasons for investigation. The evidence does not establish that reviewing before coding, reviewing after coding, or adding agents is always best. A reviewer agent's output is a claim; observed page behavior and human judgment remain separate evidence.

## 4. Does prior work prove the three should be combined?

No identified study establishes that our exact three mechanisms must be combined. GenA11y reports an advantage for its combination of extraction and prompting on its detection dataset. CodeA11y reports outcomes for a combined accessibility assistant. Neither independently tests our proposed prompt, skill, reviewer, and combined packages on our website tasks.

The defensible justification is therefore: the three avenues address distinct plausible gaps, have relevant precedents, and can be compared. A combined approach is a hypothesis because additional information, procedures, or independent checking might help. It might also add cost, conflicting instructions, or errors. The conclusion should reflect the results eventually observed, including a null or negative result.

## 5. The checklist-in-the-prompt idea

This is a well-motivated question. [Guriţă and Vatavu](https://mintviz.usv.ro/publications/2025.W4A.3.pdf) directly compared an ordinary website request with an accessibility-oriented one. Microsoft's [A11y LLM Eval](https://microsoft.github.io/a11y-llm-eval-report/index.html), a vendor research report rather than a peer-reviewed paper, also compares a control, instruction sets, and an accessibility skill. Its skill condition includes a generation turn followed by a review-and-remediation turn. Its measures come from selected automated checks, and the variants use different amounts of agent work. Therefore the report does not isolate the value of skill packaging or establish complete conformance.

The question has two parts:

1. **Implementation:** Does the generated website satisfy the applicable checklist outcomes?
2. **Self-report:** When asked to mark the checklist, does the model accurately identify what it did, what does not apply, and what remains unverified?

These are different outcomes. A model can say an item is complete while the page still has a barrier. A criterion can also be irrelevant because its feature does not exist. A required but missing feature must be recorded separately; it must not produce a misleading accessibility pass.

In the W4A 2025 study, the authors report 76% alignment between model-identified issues and expert findings during self-reflection, and note that the models underreported keyboard problems. Their stated alignment measure should not be relabeled as a full-audit accuracy or precision estimate. [Guriţă and Vatavu](https://mintviz.usv.ro/publications/2025.W4A.3.pdf)

In the 2026 audit preprint, criterion-enumerated requests found more reference-positive page-criterion records than brief requests in the reported coding-agent configurations, but also produced more findings absent from the reports. For one configuration, the paper reports recall against its reference labels changing from 25/78 to 42/78, while reported positives absent from the reports changed from 10 to 24. The inferred-negative labels and differences between configurations limit interpretation. This study audits existing pages rather than generating websites. [Mishra et al.](https://arxiv.org/html/2609.09379v2)

Our current [action checklist](accessibility/master-action-checklist.md) has 188 items: 81 WCAG-derived outcomes, 81 guidance items, and 26 research-process items. It is not a list of 188 mandatory website features. Many items apply only when a feature exists. Guidance items can describe one possible technique rather than a required implementation. Research-process items are study activities, not website components. W3C's original criteria and exceptions remain the authority.

For any future comparison, giving the same original task text plus the checklist is an **intervention condition**. The original task wording can be preserved byte-for-byte, but the total model input differs from the untouched baseline. Reviewers should also examine the generated artifact independently rather than accepting the model's own ticks as evidence. [W3C evaluation guidance](https://www.w3.org/WAI/test-evaluate/) explains why automated tools and human evaluation both matter.

This review makes no claim about whether a model actually completed our checklist. The user has directed that the project remain research-only for now.

## 6. Implications for future research framing

- **Motivation for prompts:** Evidence from accessible UI generation shows that explicit accessibility requirements can influence measured outcomes, with important variation by criterion and evaluation method.
- **Motivation for skills:** Skills provide a documented mechanism for reusable procedures. The empirical evidence is mixed, task-dependent, and largely preprint-level for the studies examined here.
- **Motivation for review agents:** Related systems show that structured review and extracted evidence can identify issues. Their findings can also be incomplete or inaccurate.
- **Motivation for combining:** The mechanisms address different plausible gaps. Their combination remains a testable hypothesis.
- **Motivation for a checklist control:** It tests whether supplying accessibility information alone is enough to explain an improvement, before attributing it to a particular packaging or review mechanism.
- **Motivation for SPV:** Planning and cognitive forcing have related precedents. An AI checking its own plan, an agent reviewing it, and a human answering questions are different mechanisms. A human-overreliance claim needs measured human behavior.

The exact intervention text, any checklist subset, and the study design remain open. No benchmark result or universal best method is asserted.
