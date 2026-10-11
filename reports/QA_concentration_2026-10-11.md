# Concentration report: build and presentation checks

**Date:** 2026-10-11. **Final PDF:** 10 pages, A4.
[PDF](output/pdf/concentration-2026-10-11.pdf) |
[Editable source](concentration-2026-10-11.tex).

## Build and visual checks

Built from the root with:

```sh
make report REPORT_MAIN=concentration-2026-10-11 REPORT_NAME=concentration-2026-10-11
```

The final LaTeX/BibTeX logs have no errors, warnings, undefined references or
citations, or overfull/underfull boxes. All pages were rendered with Poppler
and visually inspected for equations, headings, page breaks, margins and
bibliography legibility. The initial 11-page layout stranded a short paragraph
on a mostly empty page. Removing forced breaks before the canonical proofs
reduced this to ten pages; keeping the references together gives the final
bibliography. Pages 9-10 were re-rendered and inspected after that change.
Intermediate renders and build logs remain under
`tmp/pdfs/concentration-2026-10-11/`.

## Mathematical review is separate

- P005 source: `77d70d65ea2b2330ee3ab786731ecfbda4842dfe49de24e1eff638b6951f386a`.
  [Independent review](../proofs/P005_review_2026-10-11.md) covers the rare-core
  obstruction, mean bound, shrinking tilts and tilted-variance result.
- P006 source: `333a6efa6397d068fe1f93768fc6b9a68f015d08958acf30228275c062b04a79`.
  [Independent review](../proofs/P006_review_2026-10-11.md) covers the tilted
  kernel, variance identity and the implication conditional on (H+).
  The estimate (H+) remains unproved.
- [Report scope review](concentration_scope_review_2026-10-11.md) checks the
  exposition against the canonical claims; a separate source auditor checked
  the attributions. Two clarifications attribute collision accounting to
  S032/S033 and explain that E002 estimates survival marginals without recording
  coupled hitting-time samples.

No simulation, finite search or software test establishes these mathematical
claims. Internal reviews are not external refereeing or formal verification.
The build verifies presentation only. The original model and failed target
are preserved; the general concentration programme remains open.

## Provenance

Final report source SHA-256:
`86d441debac2d3115f4c9ad304d9ee1ed146a562472ee7eb8864df44c483751d`.

Final PDF SHA-256:
`db57e46b4fcb1959db2d4c8222200e4410f59bc4088c48cf24b9ae38dabd0ba2`.

The [snapshot manifest](source_snapshot_concentration_2026-10-11.json) records
canonical sources, reviews, bibliography and consulted paper hashes. The prior
survey PDF (`feeeefb8...`) and feasibility PDF (`4dca7756...`) retain their
previous full hashes; neither was overwritten. AGENTS.md is unchanged.
