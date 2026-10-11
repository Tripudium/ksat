# Geometry and computational feasibility: delivery checks

**Artifact:** [10-page feasibility note](output/pdf/geometry-feasibility-2026-10-11.pdf).
**Date:** 2026-10-11. **Document QA:** coordinating agent.

## Scope and mathematical review

The note reads the analytic and integral-geometric mechanisms of S002/S003,
records exact discrete identities and counterexamples, proposes a finite-tilt
research target, and assesses computational diagrams. It does not prove a
transferred threshold theorem or report a measured phase diagram.

- P003 v2, authored by `discrete_kinematics`, was independently reviewed by
  `analytic_transfer`. P004 v1 has the reverse author/reviewer assignment.
  Both canonical sources match the hashes in their scoped review records.
- P003 covers face counts, Euler characteristic, random restrictions and
  distance moments, including empty and endpoint cases. P004 covers the
  exact mgf domain and the coupon-collector obstruction.
- A final read-only check of the main analytic exposition by
  `analytic_transfer` found no substantive overstatement. Its two requested
  clarifications were incorporated: define remaining lifetime with a fresh
  continuation and zero UNSAT boundary value; describe the missing projection
  product rule as unestablished here, rather than claiming nonexistence.
- These are internal reviews, not external refereeing or formal verification.
  The full external threshold and variance manuscripts were not audited.

## Computational evidence

E001 retains 60 generated inputs, seeds, dependency versions and hashes,
raw solver outcomes, 21 checked SAT witnesses, 9 unchecked UNSAT reports and
30 unknown timeouts. Its verification regenerated all inputs and checked
their hashes. This is a bounded runtime calibration with a 0.75-second
process cutoff; it cannot establish a maximum feasible size, a threshold
curve or uncensored mean runtime. No UNSAT proof was independently checked.

Budget tables are arithmetic scenarios. Sampling error, timeout censoring,
certification cost, hardware specificity and GPU limitations are explicit.
The SCRTP facts come from a saved HTML snapshot; live allocations were not
queried. No SLURM scripts, cluster jobs or GPU runs were created.

## Build and visual checks

Built from the root with:

```sh
make report REPORT_MAIN=geometry-feasibility-2026-10-11 REPORT_NAME=geometry-feasibility-2026-10-11
```

The final build has no LaTeX/BibTeX warnings, undefined citations/references,
or overfull/underfull boxes. The PDF has 10 A4 pages and 12 resolved bibliography
items. All pages were rendered at 100 dpi using `pdftoppm` and inspected in
contact sheets; the pilot table and long proof displays received full-page
checks. After the final exposition clarifications, all pages were rendered
again. Only pages 2 and 3 changed; both were inspected at full-page size.
No clipping, overlap, broken equations or visible layout defect was found.
Logs, rendered pages, extracted text and render comparisons are retained under
`tmp/pdfs/geometry-2026-10-11/`.

## Reproduction and preservation

The shared Makefile now accepts `REPORT_MAIN`; the existing default still
builds the survey. The feasibility report has its own output filename.
AGENTS.md and the survey v1.1 PDF retain their previous hashes. Original
source files and prior dated reports/manifests are preserved.

See [source snapshot](source_snapshot_geometry_2026-10-11.json),
[source-original manifest](../references/source_manifest_geometry_2026-10-11.json)
and [editable bundle](output/geometry-feasibility-source-2026-10-11.zip).
The bundle contains report sources, canonical proofs/reviews, source notes,
project records and E001 scripts and raw data. Third-party source PDFs and
the supplied SCRTP website snapshot remain in the repository.
