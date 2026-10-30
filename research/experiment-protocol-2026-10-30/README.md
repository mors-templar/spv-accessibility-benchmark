# Study protocol package

**Status:** Draft for review. No experiment has run.

This package and the existing PDF describe checklist version 0.1.0.
The [Phase 2 review](../phased-study/phase-02/checklist-review.md) introduces version 0.2.0.
The original 0.1.0 checklist remains in `../accessibility/versions/0.1.0/`.
The current candidate intervention files and schemas are in the [Phase 2 package](../phased-study/phase-02/interventions/README.md).

Open [index.html](index.html) for the complete illustrated plan.
The page combines the five source documents below.

| File | Contents |
| --- | --- |
| [01-study-design.md](01-study-design.md) | Study questions, tasks, conditions, diagrams, and decisions. |
| [02-prompt-pack.md](02-prompt-pack.md) | Candidate prompts, skill instructions, reviewer, and JSON contracts. |
| [03-evaluation.md](03-evaluation.md) | Human review, Playwright, axe, metrics, and analysis. |
| [04-build-and-run.md](04-build-and-run.md) | Components, preparation, run records, and release rules. |
| [05-evidence.md](05-evidence.md) | Peer-reviewed sources, standards, and claim limits. |
| [references.bib](references.bib) | Portable verified bibliography entries for this plan. |
| [diagrams](diagrams/) | Three figures in PNG and editable SVG form. |
| [build_visuals.py](build_visuals.py) | Source script for the figures and review page. |

Run `python build_visuals.py` from this directory to rebuild the page and figures.
The script needs the Python `matplotlib` and `markdown` packages.
The exact task text remains outside this package.
Clarify dataset rights before sending it to a hosted model or publishing it.
