# WCAG checklist coverage verification

The checklist is a research-authored annotation of WCAG 2.2, not a copy of the full normative text and not an accessibility certification.

## Source

- Normative standard: [WCAG 2.2 Recommendation, 12 December 2024](https://www.w3.org/TR/2024/REC-WCAG22-20241212/).
- Machine-readable metadata: [W3C WCAG 2.2 JSON serialization](https://www.w3.org/WAI/WCAG22/wcag.json), retrieved 2026-10-29.
- Source snapshot SHA-256: `3a034865a879a7d874b60ff2aec7f430cf37bc1597a1e00985680fd80ef5cf75`.
- W3C's [serialization notes](https://github.com/w3c/wcag/tree/main/11ty/json) describe attribution and the distinction between W3C content and added annotations.

The local `wcag22-criteria-index.json` retains unchanged W3C numbers, short names, levels, anchors, and principle names for the 86 active criteria. The checklist's explanatory descriptions are separate research-authored summaries. The obsolete 4.1.1 Parsing entry is excluded because the W3C serialization does not list it as a WCAG 2.2 criterion.

## Run the checks

From the repository root:

```powershell
python research/accessibility/verify_coverage.py
```

To also compare the index to the matching local W3C snapshot:

```powershell
python research/accessibility/verify_coverage.py --w3c-json D:/projects/research/se4all-2027/work/.arena-research-cache/w3c-wcag22-20261029.json
```

The validator checks exact IDs, levels, short names, anchors, duplicates, and totals: 31 A, 24 AA, and 31 AAA. It also checks the snapshot's SHA-256 and compares all retained metadata when the snapshot is supplied. W3C's JSON can change; a later download with a different hash must be reviewed rather than treated as the same snapshot.

This verification proves coverage of the criterion index and matching metadata. It does not prove that each paraphrase is complete, that any criterion applies to a particular site, or that a site conforms. Review the original W3C text and applicable exceptions, and validate test procedures before using the checklist for research.
