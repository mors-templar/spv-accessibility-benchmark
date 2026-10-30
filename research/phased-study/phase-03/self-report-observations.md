# Exploratory model self-report coverage

**Status:** Descriptive development observation, 30 October 2026.
This does not assess whether the model's claims are correct.

The scheduled batch contains ten completed D and P turns.
Each produced a local `accessibility-self-report.md` file.
The second parser recognized one status for all 188 checklist IDs in each of those ten files.
It found no duplicated IDs, unknown statuses, or type-label mismatches in those parsed entries.

The first parser could not recognize several table and bullet formats used by the models.
Its ledger is preserved as `exploratory-claim-ledger.json` in the ignored local run directory.
The second parser was revised after inspecting those formats.
Its results are in `exploratory-claim-ledger-v2.json` and per-run versioned files.
This post-hoc parser adjustment is exploratory and is not independent validation.

A recognized status is only a model claim.
It does not prove that the item applies, that the stated evidence exists, or that the page is accessible.
Items marked unassessed or not applicable still need independent review when relevant.
Baseline B did not request a checklist self-report.

The parser supports selected table and bullet formats.
Other valid report layouts can remain unrecognized.
The model may also place a report in its response rather than in a file.
The parser does not inspect that response as a fallback.
