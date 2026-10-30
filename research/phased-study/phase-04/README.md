# Phase 4: prompt and skill package

**Status:** Development candidate, 30 October 2026. The skill and diagnostic have offline fixture tests.
The development Codex adapter provisions this skill in mock runs.
It has not been assessed against a real model output.
The final wording is not frozen.

## Prompt guidance

[prompt-guidance.txt](prompt-guidance.txt) is the P condition's exact project instruction.
Its bytes match the Phase 2 candidate used for the earlier P development runs.
An adapter can put it in a supported project-instruction file or a system message.
Record the actual channel. These channels can produce different behavior.
P has no enforced gate and adds no diagnostic.

The original task and the common checklist instruction remain separate from this file.
See the [condition input guide](../phase-06/README.md) for exact assembly.

## Skill

The reusable [spv-accessibility](spv-accessibility/SKILL.md) package follows the Agent Skills file structure.
The runner must load the skill through its supported mechanism.
For a runner with project-level discovery, provision the package in the run's isolated skill directory.
Record whether the skill was discovered and actually invoked.
This repository does not install it globally.
Do not load the skill in B, D, P, or A runs.

The skill asks for an accessibility plan and questions with concrete answers.
When available, it requests the `verify_plan` diagnostic.
The diagnostic is advisory; S has no host-enforced gate.

## Advisory diagnostic

The [script](spv-accessibility/scripts/verify_plan.py) uses only the Python standard library.
It reads a JSON request from standard input or a file and returns a JSON response.
The request and response schemas are in the skill's `references` folder.
The [tool adapter](tool_adapter.py) binds run and task IDs outside model-supplied arguments.
The [OpenAI Responses function definition](spv-accessibility/references/openai-responses-function.json) is a structural example.
Its object requirements were checked locally. It has not been submitted to a live API.
The Codex adapter exposes the diagnostic as a skill script, not a registered API function.
Other provider or harness adapters remain to be built and tested.

Example with synthetic text:

```powershell
'{"plan_text":"Create a modal.","questions_and_answers":[]}' | python research/phased-study/phase-04/spv-accessibility/scripts/verify_plan.py
```

The diagnostic looks for a small set of text signals for questions, contrast, dialogs, status, labels, and keyboard use.
It reports `WARN` or `NO_WARNING` with explicit limitations.
It can miss real problems and flag acceptable approaches.
It does not inspect generated HTML, rendered colors, keyboard behavior, or assistive technology.
In particular, `NO_WARNING` is not a pass or conformance finding.

For normal and large text, WCAG 2.2 contrast thresholds and exceptions are different.
The diagnostic does not measure either threshold.
The [W3C contrast explanation](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) states the applicable conditions.

## Sources for packaging

- The [Agent Skills specification](https://agentskills.io/specification) defines the skill folder and required frontmatter.
- [OpenAI's function-calling guide](https://developers.openai.com/api/docs/guides/function-calling) describes its Responses function shape and strict object requirements.
- The approved [study checklist](../../accessibility/master-action-checklist.md) supplies the diagnostic's item IDs.

These sources justify formats and references. They do not establish that the skill improves accessibility.
