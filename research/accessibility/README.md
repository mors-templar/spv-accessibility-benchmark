# Accessibility research materials

- [Master action checklist](master-action-checklist.md): practical, conditional actions for developers and reviewers, with WCAG links, guidance labels, review methods, and a 55-criterion crosswalk.
- [Master criterion index](master-checklist.md): all WCAG 2.2 A and AA criteria, all AAA criteria as an extension, and additional interaction guidance.
- [Sources and AI evidence](sources-and-ai-evidence.md): standards, legal and platform context, published observations, and limits.
- [Coverage verification](coverage-verification.md): how the checklist is checked against the W3C criterion index.
- `wcag22-criteria-index.json`: W3C criterion metadata, attributed and separated from our checklist annotations.
- `assessment-template.json`: a blank research record for the 55 A and AA criteria. It is not a result.
- `action-checklist.json`: the machine-readable version of the action checklist. It is a research draft, not a validated intervention.
- `build_action_checklist.py`: the editable action catalog and generator. Run `python research/accessibility/build_action_checklist.py --check` from the study-site root to check the generated outputs.

These are drafts for review. A complete criterion index and mapped action list are not complete test procedures or conformance claims. Task-specific applicability and tests remain to be defined before the study. Keep the baseline prompt unchanged and separate from the evaluation materials.
