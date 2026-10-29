# Arena accessibility study: working decisions

Date: 2026-10-29. Status: decisions and proposals for further discussion. This is not a preregistration or a report of results.

An initial copy is also in `work/experiments/spv-study-site/research/study-working-decisions.md`. Keep the copies synchronized when the plan changes.

## Decisions from the researcher

- Use selected Arena candidates 7, 8, 18, 19, and 1 as the five task inputs. The local manifest records the source IDs and hashes.
- Use the same original task message across conditions for a given task.
- Create a private GitHub repository and a public GitHub Pages site. The site will have one main index and task subpages.
- Use Playwright and human review for accessibility evaluation. The researcher intends to conduct the human review.
- Discuss the intervention design, controls, and evaluation in detail before freezing the study protocol.

## Proposed intervention comparison

| Condition | Proposed change | Interpretation |
| --- | --- | --- |
| Baseline | The original task in a fresh session, with no study-specific intervention. | Reference under the documented model and runner. |
| Accessibility checklist | The original task with direct accessibility guidance. | A control for providing accessibility information. |
| Prompt guidance | The task plus prompt-level plan verification guidance. | A prompt-only package; no host-enforced gate is assumed. |
| Skill | The task plus a versioned skill and its available tools. | A package comparison; record whether the skill and tools actually run. |
| Validation agent | The task plus a defined reviewer-agent workflow. | A package comparison; specify what is reviewed and how decisions are applied. |
| Combined | The task plus the selected prompt, skill, and agent packages. | Measures this combination as a package. |

These are proposed arms. The user agreed to discuss them further; the exact intervention files, control wording, answer policy, model settings, and budgets remain undecided. These six arms do not isolate all interactions between the three mechanisms. A full three-factor design would require all eight combinations; a separate plan-only control would help isolate any effect of a quiz.

## Building the interventions

1. Derive the accessibility concerns from WCAG 2.2 and applicable WAI-ARIA design patterns. Record which rules are requirements and which are pattern guidance.
2. Define the plan, questions, answer source, validation decision, retries, and stop conditions. Record the point at which the runner may generate or write code.
3. Develop on separate examples and test the verifier with known-good and known-bad fixtures. Include native controls that meet a criterion without unnecessary ARIA.
4. Version and hash each intervention. Record effective instructions, tools, actual activation, gates, overrides, and additional resources.
5. Freeze the selected study inputs and tests before the comparative runs. Avoid tuning on those outputs while presenting the same runs as an untouched evaluation.

The researcher already knows the five chosen tasks. They should not be described as a fully blinded holdout. Publicly available prompts also carry a possible model-training contamination risk.

## Proposed evaluation

- Record build and launch status, required functionality, automated accessibility checks, human observations, and cost separately.
- Specify task-specific journeys and expected behavior before inspecting comparison outputs. Assess the relevant states and avoid requiring controls the task does not require.
- Use Playwright to exercise interactions and keyboard behavior. Consider axe-core in the same environment, with its version and enabled rules recorded.
- Document the human reviewer, evaluation steps, browser, viewport, and evidence. Mask conditions where feasible. An additional independent reviewer and assistive-technology review would strengthen the work, if available.
- Preserve failures, missing features, indeterminate cases, and reasons. A failed or incomplete site must not appear more accessible because it exposes fewer elements.
- Report each task and runner separately, with repeat runs and uncertainty when feasible. Five tasks support an exploratory pilot, not a claim of universal superiority.
- Define the primary outcome, test applicability, sample size, order, stopping rules, and analysis before confirmatory runs. The earlier 180-run calculation was illustrative, not a power calculation or an agreed budget.

A comparison of generated artifacts cannot by itself establish a change in human automation bias. That claim needs a distinct participant study and any applicable institutional review.

## Research foundations

- [CodeA11y, CHI 2025](https://doi.org/10.1145/3706598.3713335): peer-reviewed research on accessibility assistance in coding workflows, including developer evaluation. It does not validate this proposed system.
- [Buçinca et al., CSCW 2021](https://doi.org/10.1145/3449287): peer-reviewed evidence on cognitive forcing in human AI-assisted decisions, with observed tradeoffs. It does not establish an effect on this project.
- [ProjectEval, Findings of ACL 2025](https://aclanthology.org/2025.findings-acl.1036/): peer-reviewed precedent for evaluating generated projects through user-interaction simulation. Its tests do not constitute our accessibility oracle.
- [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) and [W3C evaluation-tool guidance](https://www.w3.org/WAI/test-evaluate/tools/selecting/): standards and guidance, not peer-reviewed research studies.
- [Playwright accessibility documentation](https://playwright.dev/docs/accessibility-testing): tooling guidance, not proof that automated checks cover every barrier.

## Hosting and rights

GitHub states that Pages from private repositories depends on the account plan. A published Pages site is normally public even if its source repository is private. Confirm the account and actual deployment state before claiming the site is available.

The Arena dataset has a custom agreement. Clarify whether the intended hosted-model submissions and publication of copies are permitted. Keep original prompts and unreviewed artifacts out of the public site until rights are clear. Source information remains in `work/experiments/benchmarks/selected_arena_baselines/manifest.json` and the ignored local cache.
