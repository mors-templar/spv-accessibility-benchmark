# Evidence and claim limits

**Status:** Source-linked rationale for draft protocol 0.1.
This is a targeted review, not a systematic literature review.
The cited papers do not validate our proposed package.

The keys below are recorded in the project's canonical bibliography.
A portable copy is available in [references.bib](references.bib).
An older entry, `mowar2024p052`, gives the CodeA11y paper the wrong year.
Use the verified `mowar2025codea11y` entry for that 2025 paper.
The older bibliography needs a separate audit before use in a paper.

## Peer-reviewed research

| Source | Study relevance | Limit for this protocol |
| --- | --- | --- |
| [`gurita2025w4a`: Guriţă and Vatavu, W4A 2025](https://mintviz.usv.ro/publications/2025.W4A.3.pdf) | Compares accessibility-agnostic and accessibility-oriented UI requests. Uses automated checks, expert review, and model self-reflection. | One banking task and selected criteria cannot establish the effect on our tasks. Expert and automated aggregates moved differently. |
| [`mowar2025codea11y`: CodeA11y, CHI 2025](https://arxiv.org/html/2502.10884) | Studies an accessibility-aware coding assistant with a developer evaluation. | Its package combines features; it does not isolate our prompt, skill, or gate. |
| [`he2025gena11y`: GenA11y, FSE 2025](https://ics.uci.edu/~seal/publications/2025_FSE_GenA11y.pdf) | Uses extracted page evidence and detailed prompts for issue detection. | Detection on existing pages differs from generating websites. A reviewer can still be wrong. |
| [`ding2026skillassessment`: Ding et al., Findings of EMNLP 2026](https://aclanthology.org/2026.findings-emnlp.1427/) | Reviews skill evaluation, routing, and benchmark coverage. | It does not prove a particular skill improves accessible web generation. |
| [`liu2025projecteval`: ProjectEval, Findings of ACL 2025](https://aclanthology.org/2025.findings-acl.1036/) | Evaluates generated projects with simulated user interactions. | Its benchmark is not our WCAG evaluation oracle. |
| [`bucinca2021forcing`: Buçinca et al., CSCW 2021](https://iis.seas.harvard.edu/papers/bucinca21trust.pdf) | Studies cognitive forcing in human AI-assisted decisions. | Our autonomous plan review has no human participant and cannot establish reduced human overreliance. |

The prior [intervention evidence review](../why-these-interventions-2026-10-30.md) gives additional paper-specific details.
It also distinguishes peer-reviewed articles, preprints, and vendor reports.
The six proposed arms are our design choice, not a published validated protocol.

## Standards, specifications, and tool documentation

| Source | Use in this plan | Status |
| --- | --- | --- |
| [`w3c2024wcag22`: WCAG 2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/) | Defines the accessibility criteria and exceptions. | W3C Recommendation. |
| [`w3c2026wcagem2`: WCAG-EM 2.0](https://www.w3.org/TR/2026/NOTE-wcag-em-2-20260723/) | Guides scope, sample, evaluation, and reporting. | W3C Group Note; it does not replace WCAG. |
| [`playwrightaccessibilitydocs`: Playwright accessibility testing](https://playwright.dev/docs/accessibility-testing) | Guides browser-driven accessibility checks. | Tool documentation; not proof of complete coverage. |
| [`dequeaxeapi`: axe-core API](https://www.deque.com/axe/core-documentation/api-documentation/) | Defines result fields and tool impact labels. | Vendor documentation; impact labels are not WCAG severity grades. |
| [`agentskillsspecification`: Agent Skills](https://agentskills.io/specification) | Defines the portable skill package format. | Format specification; provider support still needs verification. |
| [`arena2025webdevdataset`: WebDev Arena dataset](https://huggingface.co/datasets/lmarena-ai/webdev-arena-preference-10k) | Source of the five researcher-selected requests. | Custom agreement includes transfer restrictions; intended use needs clarification. |
| [`owasp2025top10`: OWASP Top 10:2025](https://top10.owasp.org/2025/) | Reference for a separately scoped security study. | An awareness list is not an accessibility standard or a complete security test. |
| [`asdste100issue9`: ASD-STE100 downloads](https://www.asd-ste100.org/STE_downloads.html) | Official source for the controlled-language specification. | The full specification and dictionary have not been checked for this draft. |

The official ASD site offers a free copy by request.
It warns that plausible AI text may still fail the specification.
This draft uses short, active sentences and defined technical terms.
It has not passed a formal ASD-STE100 rules and dictionary audit.

## What the evidence can and cannot establish

The papers support investigation of requirements, skills, review, and workflow evaluation.
They do not establish that every avenue will help.
They do not establish that combining all avenues will be best.
Our proposed experiment can assess a bounded package comparison if the protocol is followed.
Five selected requests cannot prove performance on all web development tasks.
Further studies would need broader sampling, independent review, and justified statistical power.
