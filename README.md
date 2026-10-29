# AI website accessibility study

This repository contains a static research index and five task pages. The site is a preparation workspace. No model runs or accessibility results have been published.

## Structure

- `docs/index.html`: entry page for all five tasks.
- `docs/tasks/`: individual task pages.
- `docs/methodology.html`: the proposed evaluation approach.
- `research/study-working-decisions.md`: detailed research decisions and questions for further discussion. This is outside the public Pages source.
- `research/execution-plan.md`: the proposed phases, run procedure, evaluation, and reporting plan. This is outside the public Pages source.
- `research/accessibility/`: the draft WCAG 2.2 checklist, source review, and criterion coverage verification. These files are outside the public Pages source.
- `data/tasks.json`: public-safe task summaries and current status labels.
- `tools/build_site.py`: regenerates the static pages from the summaries.

To rebuild and preview from this folder:

```powershell
python tools/build_site.py
python -m http.server 18877 --bind 127.0.0.1 --directory docs
```

Visit `http://127.0.0.1:18877/`. Relative links also work when the local HTML files are opened directly.

The intended GitHub Pages source is the `docs` directory. Pages from a private repository depends on the owning account's plan. A published Pages site is public unless the hosting product provides and enables a different visibility mode. See [GitHub Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Source and study status

The task descriptions are short summaries. The original WebDev Arena messages are not in this repository. The dataset has a custom agreement; clarify rights before submitting its prompts to hosted services or publishing prompt copies. The task provenance manifest and local copies are maintained separately in the research workspace.

The intervention conditions and evaluation plan are proposals. Review and freeze the protocol before comparative data collection. Status fields must reflect actual evidence; do not publish a result until it has been run and checked.
