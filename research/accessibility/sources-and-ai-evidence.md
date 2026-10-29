# Accessibility sources and evidence about AI-generated sites

Date checked: 2026-10-29. Status: research notes for review, not legal advice and not a completed benchmark. This document separates standards, law, platform guidance, published research, and hypotheses for our own study.

## What the main sources contribute

| Source | Type and scope | How to use it |
| --- | --- | --- |
| [WCAG 2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/) | W3C Recommendation. It defines testable success criteria, conformance levels, definitions, and conformance requirements. | Use A and AA as the proposed technical baseline. Apply the original conditions and exceptions. A and AA together have 55 active criteria in the verified serialization. |
| [How to Meet WCAG](https://www.w3.org/WAI/WCAG22/quickref/) | W3C reference for criteria, understanding materials, techniques, and failures. | Use it to find explanations and examples. Techniques are informative methods, not the only way to meet a criterion. |
| [WCAG Evaluation Methodology 2.0](https://www.w3.org/TR/2026/NOTE-wcag-em-2-20260723/) | W3C Group Note, published 23 July 2026. It provides a structured product-evaluation process. | Define scope, explore the product, select samples, evaluate, and report. It does not replace WCAG or establish whole-site conformance from a sample alone. |
| [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) | Informative component patterns and examples. | Use for dialogs, tabs, menus, comboboxes, and other interactions when those patterns are present. It does not require every site to include them. |
| [Cognitive accessibility guidance](https://www.w3.org/TR/coga-usable/) | W3C Working Group Note. | Consider clarity, navigation, recovery, and cognitive needs beyond the WCAG AA checklist. Label recommendations that are not WCAG requirements. |
| [ICT Testing Baseline for Web](https://ictbaseline.access-board.gov/web-baselines/) | US Access Board baseline for evaluating Revised Section 508 web requirements. | Use as a public testing-reference source. Section 508 and WCAG 2.2 have different scopes and versions. |
| [Playwright accessibility guidance](https://playwright.dev/docs/accessibility-testing) and [W3C tool guidance](https://www.w3.org/WAI/test-evaluate/tools/selecting/) | Tool and evaluation guidance. | Automate selected checks and complement them with manual and assistive-technology review. A clean scan is not proof of conformance. |

WCAG Level AA includes all Level A and AA success criteria. A criterion can be satisfied because its relevant content does not exist; our study should record that as not applicable for transparency. Accessibility of the actual complete page and its relevant processes matters. The [W3C conformance explanation](https://www.w3.org/WAI/WCAG22/Understanding/conformance) also explains that meeting WCAG does not guarantee usability for every person.

## What published studies observed

These are findings in specific samples and conditions. They are not a prevalence estimate for current ChatGPT, Gemini, Codex, Antigravity, or AI systems in general. The selected study has not yet been run.

| Study | Evidence and limits | Implication for this checklist |
| --- | --- | --- |
| [Guriţă and Vatavu, W4A 2025](https://mintviz.usv.ro/publications/2025.W4A.3.pdf) | Peer-reviewed conference paper. It examined banking interfaces from GPT-4-turbo and Claude 3.5 Haiku under two prompt styles, with automated checks, expert review, and a later self-reflection step. It reports issues including keyboard access, text alternatives, structure, focus, and status messages. Accessibility-oriented instructions improved some results in this experiment, while some checks still had problems. | Include semantic relationships, keyboard operation, focus, alternatives, contrast, and dynamic status in the candidate risk set. Keep a direct-guidance control. Do not generalize its rates to our tasks or current models. |
| [Mowar et al., CodeA11y, CHI 2025](https://arxiv.org/html/2502.10884) | Peer-reviewed conference paper. A formative study involved 16 developers; a separate evaluation involved 20 novice developers. The authors observed missing accessibility prompting and incomplete manual follow-through, including placeholder alternative text. | Review the meaning of labels and image descriptions, not only whether attributes exist. Record whether review or reminders are actually used. |
| [Panchanadikar et al., ASSETS 2025](https://doi.org/10.1145/3663547.3759755) | Conference poster. Its abstract describes six generated websites and reports issues including contrast, labels, structure, and cognitive accessibility. | Include these areas as hypotheses for evaluation. The six-site sample is too small for a general model failure rate. |
| [Abu Doush and Kassem, Universal Access in the Information Society, 2025](https://link.springer.com/article/10.1007/s10209-025-01250-2) | Journal article. The accessible abstract describes 11 component types, four model products, detailed accessibility instructions, and manual keyboard and screen-reader evaluation. The full paper was not available during this review. | Use as an abstract-level precedent for component-level checks. Do not infer its per-component results or independent verification from the abstract alone. |
| [Aljedaani and Mollik, W4A 2026](https://arxiv.org/html/2605.13873) | Conference systematic review of LLM and web-accessibility research. The available version describes WCAG as a common reference and notes limited coverage of cognitive needs and disabled-user involvement. Its abstract says 38 studies, while its introduction and methods say 33, and a figure uses 36. | Use its source map and caution about evaluation gaps. Do not quote a definitive sample count without checking the final published version or resolving the discrepancy. |
| [Microsoft A11y LLM Eval](https://microsoft.github.io/a11y-llm-eval-report/) | Vendor research report and benchmark, not presented here as a peer-reviewed paper. It uses selected automated rules and task-specific assertions and compares control, instructions, and skills. | Useful engineering precedent. Its reported passes apply only to its own checks and samples. |
| [Suh et al., 2025 preprint](https://arxiv.org/html/2503.15885) | The available preprint compares generated and human-written web code and several prompting approaches. It reports mixed results by tool and setting, including cases where generated code did better on measured checks. Peer-reviewed publication was not established in this review. | Treat it as counterevidence to a blanket claim that AI code is always worse. Do not treat its findings as validation of our method. |

## Candidate issue register: what may be missed

| Candidate issue | Basis | What our study should observe |
| --- | --- | --- |
| Missing or unhelpful text alternatives | CodeA11y observed placeholder completion problems; W4A 2025 reports non-text alternatives as a problem in its sample. | Inspect informative image purpose and actual alternative text. Do not score an arbitrary attribute as sufficient. |
| Weak semantic structure and relationships | W4A 2025 reports semantic structure problems. | Inspect headings, landmarks, groups, tables, and form relationships where present. |
| Keyboard access and visible focus | W4A 2025 reports keyboard and focus issues in its evaluated interfaces. | Execute actual keyboard journeys and record focus visibility and order. |
| Text contrast | W4A 2025 and the ASSETS poster report contrast problems in their studied outputs. | Measure relevant rendered text and states, applying size thresholds and exceptions. |
| Form labels and instructions | CodeA11y and the ASSETS poster examine form and labeling problems. | Check visible labels, programmatic names, error identification, and correction where inputs exist. |
| Dynamic status information | W4A 2025 examined missing or improper status-message handling in its sample. | Test actual state changes, success and error feedback, and accessibility-tree exposure. Review announcements with assistive technology where feasible. |
| Modals, focus return, drag alternatives, and complex widgets | These are standards- and pattern-based candidates. The cited studies do not establish that our five tasks or every model will contain them. | Test only when the relevant widget exists or is required. Use the appropriate W3C pattern and criterion. |
| Cognitive clarity and reduced motion | W3C COGA and WCAG guidance, plus the ASSETS poster's small sample. | Review understandable instructions, recovery, motion, and preferences. Separate AA criteria from additional guidance. |

The appropriate claim after running our own experiment is specific: for a named task, version, condition, and tested state, a reviewer observed a defined issue. Record actual evidence before calling an issue an observed AI omission.

## Applying this to the five selected requests

| Selected task | Initial areas to consider | Scope warning |
| --- | --- | --- |
| Services landing page | Structure, navigation, tab interaction, text contrast, and the requested download action. | The order form is not supplied. Record missing required behavior and unresolved inputs. Do not assume the FAQ must be an accordion. |
| Consulting landing page | Contrast, semantics, headings, focus, calls to action, and motion. | The original request explicitly asks for accessible contrast and semantic HTML. Reduced-motion support may be a best practice or AAA concern depending on the test. |
| Cinema booking | Film information, choices, labels, keyboard navigation, state, confirmation, and media alternatives if media exists. | Film data and external confirmation behavior are not specified in full. Do not assume all video or email capabilities exist. |
| Task dashboard | Task creation and editing, control names, filters, status changes, drag alternatives, and charts. | Assess keyboard access and WCAG 2.5.7's single-pointer alternative separately when applicable. Named libraries and broad scope can affect feasibility. |
| Personal portfolio | Reading order, headings, navigation, link names, visible focus, and meaningful image alternatives if images exist. | The request is brief. Do not invent forms or widgets as task requirements. |

These are preliminary mappings. The actual test plan must specify observable behavior, applicable criteria, states, expected results, evidence, and reviewer before comparative runs. The presence or absence of a feature should be confirmed from each generated artifact.

## Law and institutional or platform requirements

These examples show why a technical standard and a legal obligation are not the same thing. Actual applicability depends on jurisdiction, entity, product or service, dates, exceptions, and local implementation. This is a research overview, not a legal conclusion.

| Source | Scope and relationship to the checklist |
| --- | --- |
| [US ADA Title II regulations](https://www.ada.gov/law-and-regs/regulations/title-ii-2010-regulations/) | The web and mobile rule applies to covered state and local public entities. It references WCAG 2.1 A and AA and contains deadlines and exceptions. It does not make that particular rule automatically applicable to every private website. |
| [US Revised Section 508](https://www.section508.gov/test/websites/) | Federal information and communications technology requirements include WCAG 2.0 A and AA for covered web content. It is not a universal rule for every website. |
| [UK public-sector guidance](https://www.gov.uk/guidance/accessibility-requirements-for-public-sector-websites-and-apps) | Guidance for covered public-sector sites and apps refers to WCAG 2.2 AA and accessibility statements, with specified exceptions. |
| [EU Web Accessibility Directive standards](https://digital-strategy.ec.europa.eu/en/policies/web-accessibility-directive-standards-and-harmonisation) | The directive covers public-sector websites and mobile apps. The cited EN 301 549 v3.2.1 draws on WCAG 2.1 and contains additional requirements. |
| [EN 301 549 v4.1.1 update](https://accessible-eu-centre.ec.europa.eu/content-corner/news/european-accessibility-standard-en-301-549-has-been-updated-2026-09-07_en) | The September 2026 update adopts WCAG 2.2. The cited EU guidance says v4.1.1 was not yet the legal reference when published. Recheck Official Journal citations and national law before making any current legal claim. Do not assume the same harmonization status for every directive. |
| [European Accessibility Act](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX%3A32019L0882) | Applies to specified products and services, including certain e-commerce services, from the applicable dates. Its scope, microenterprise service exemption, transition rules, and national laws matter. |
| [GDPR Article 12](https://eur-lex.europa.eu/eli/reg/2016/679/) | Concerns accessible, clear communication about personal-data processing and rights. It is a privacy law, not a complete WCAG checklist. Assess privacy separately. |
| [OWASP ASVS](https://asvs.owasp.org/) | An application-security verification standard. It is relevant to a separately scoped security assessment, not the web-accessibility standard. |
| [AICPA SOC 2](https://www.aicpa-cima.com/news/article/become-a-soc-er-player-and-win-at-risk-management) | Reporting on service-organization controls related to security and other trust-service categories. It is not a WCAG accessibility checklist. |
| [Apple accessibility guidance](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels/) | Platform-specific guidance and evaluation criteria for communicating support for features such as VoiceOver and reduced motion in apps. Do not present it as a universal legal requirement for websites. |
| [Android accessibility guidance](https://developer.android.com/guide/topics/ui/accessibility/views/apps-views) | Guidance for Android apps, including a recommended 48 dp touch target. Do not conflate Android dp guidance with WCAG 2.2's 24 CSS pixel minimum and exceptions. |

Legal and standards references should be rechecked when the actual evaluation is conducted. WCAG 2.2 AA is a proposed study target; passing a subset of this checklist does not establish legal compliance.

## How to report results without overclaiming

- Fix the task-specific scope and checks before comparing outputs. Keep the original messages unchanged across conditions.
- For each criterion and task, report how many runs were attempted, applicable, assessable, passed, failed, or unassessable. Define the denominator before analysis.
- A criterion-level failure rate can be reported as observed failures divided by assessed applicable runs, with the attempted and unassessable counts alongside it. Do not hide missing required features or failed builds.
- Keep rule-level and affected-node counts separate. Do not treat repeated scans of the same issue as independent observations without a deduplication policy.
- Distinguish a researcher-authored manual review from an independent expert review or disabled-user study. State which assistive technologies were actually used.
- Show results per task, model-runner combination, condition, and repetition. Five selected tasks do not support a general prevalence claim across all AI tools or websites.
- Treat the source papers' findings as motivation and comparators. They do not prove the effectiveness of any future intervention in this project.
