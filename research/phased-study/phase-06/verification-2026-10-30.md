# Development package verification

**Date:** 30 October 2026.
**Scope:** Offline fixtures, local input hashes, and mock CLI processes.
No selected task was submitted to a model during these checks.

| Check | Result |
| --- | --- |
| Phase 4 to 6 Python fixture suite | 27 passed. |
| Skill frontmatter validator | Valid. |
| Four request, response, plan, and decision schemas | Valid JSON Schema structure. |
| OpenAI Responses function shape | Local object and required-field checks passed. No live API call was made. |
| Synthetic rejected plan | Blocked after three plan and review attempts. |
| Synthetic approved plan | The build callback was invoked after review. |
| Mock Codex adapter | S used one build call; X used separate plan, review, and build calls. |
| Mock Codex thread reuse | Rejected before build. |
| Unverified preflight template | Command-line attempt stopped before a task was submitted. No run folder was created. |
| Five selected task hashes | All matched the local source manifest. |
| Six condition assemblies for each task | B retained the task bytes; D, P, S, A, and X used the same assembled message. |
| Existing Phase 3 fixture suite | 52 tests ran; 46 passed and six loopback tests were skipped. |
| Existing project test suite | 22 passed using a writable workspace temporary directory. |

The first existing-project test run had two temporary-directory setup errors.
The tests passed when the temporary directory was set inside the workspace.
The [input integrity record](selected-input-integrity.json) contains task IDs and hashes, without prompt text.

The development package manifest SHA-256 was:

`49b0e6d1a9a417b0ca47dd826e64448060d5cca9f10c80f9e97cec425ca2d547`

The local Python version was 3.13.9.
The installed Codex CLI reported version `0.165.0-alpha.1.2`.
The mock process tests did not execute that CLI.

## What these checks do not establish

- Skill activation or diagnostic use by a real model.
- Planning isolation or independent review in a real runner.
- Accessibility, WCAG conformance, security, or task completion of a generated site.
- A treatment effect or a best intervention.
- Final protocol approval or preregistration.

The package remains a development candidate.
Re-run the checks and update this record if the protected package files change.
