---
name: spv-accessibility
description: Plan accessibility for a website request using the supplied study checklist and an advisory diagnostic.
---

# Accessibility plan

Read the website request and the supplied accessibility checklist.
Keep the requested features and identify the main user journeys.
Identify the checklist outcomes that apply to those journeys.
For each material risk, ask a question and give a specific planned answer.
Mark an answer as unknown when you cannot support it.

Before implementation, make a plan and question-and-answer list.
When a `verify_plan` tool is available, call it with that material.
Otherwise, use `scripts/verify_plan.py` from this skill when shell execution is available.
The script accepts a JSON object on standard input and returns JSON on standard output.
The input format is in `references/verify-plan-request.schema.json`.
Consider each warning and record any unresolved risk.
The diagnostic is advisory. It cannot establish accessibility or WCAG conformance.

Save the plan in `spv-plan.md` if the current phase permits file writes.
Otherwise, return the plan in the response.
Follow any host instruction that restricts implementation until a review is complete.
When implementation is permitted, build the requested website.
Use the supplied checklist to create the requested self-report.
Record checks that you could not perform as unassessed.
Do not claim conformance without supporting evidence.
