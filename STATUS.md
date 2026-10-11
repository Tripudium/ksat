# Project status

**Updated:** 2026-10-11.
**Phase:** survey and feasibility assessment delivered; Blythe experiment workflow
and concentration research prompt prepared. The research programme remains open.
**Objective:** [PROBLEM.md](PROBLEM.md).

## Current deliverables

- The [18-page survey, v1.1](reports/output/pdf/report.pdf) covers thresholds,
  algorithms, certificates, practical sizes and GPUs. Section 2.1 contains the
  sharp m < 2^k guarantee; Section 2.3 explains coupled clause sequences.
  Its source is [reports/main.tex](reports/main.tex).
- The separate [10-page feasibility note](reports/output/pdf/geometry-feasibility-2026-10-11.pdf)
  examines discrete analytic and integral-geometric transfers, proves elementary
  identities and obstructions, and assesses CPU phase diagrams. Its source is
  [reports/geometry-feasibility-2026-10-11.tex](reports/geometry-feasibility-2026-10-11.tex).
- [E002](experiments/E002_blythe_phase_diagrams/README.md) supplies Blythe SLURM
  scripts, seeded batch configurations, a certificate-checking runner and plots
  with explicit censoring/sampling uncertainty. The cluster campaign is not run.
- The [Git/uv guide](docs/blythe-uv.md), root Python 3.12 project and `uv.lock`
  support separate local/Blythe environments. Setup builds the pinned checker;
  submission/workers reject stale environment records. Git initialization was
  blocked by this workspace's `.git` write restriction; terminal commands are
  documented. No remote repository or commit has been created.
- The [concentration research prompt](attempts/A001_discrete_geometry/concentration_research_prompt.md)
  specifies the exact target, source audits, known obstructions, varied methods
  and standards for numerical evidence and independent proof review.
- Sources are catalogued as [S001-S043](references/README.md). The original
  survey PDF, dated bundles, supplied source papers and AGENTS.md are preserved.

## Mathematical and literature position

S001 states a limiting random k-SAT threshold for every fixed k >= 3 in a
recent ECCC preprint; its full proof has not been independently reviewed here.
Published theorems, small-k cavity predictions and recent threshold/variance
manuscript claims remain distinguished by status and scope.

| Claim ID | Exact scope | State | Review |
| --- | --- | --- | --- |
| [P001](proofs/P001_clause_relaxation.md) | Clause-sum LP relaxations for clauses of length >= 2 contain the all-one-half point, including UNSAT proper k-CNF examples. | `proof-written` | Independent review queued. |
| [P002](proofs/P002_few_clauses.md) | Every proper k-CNF with m < 2^k is SAT; sharp when unused variables and repeated clauses are allowed. | `proof-written` | Standard result, S037; independent review queued. |
| [P003](proofs/P003_discrete_kinematics.md) | Cubical intersection, projection and overlap identities; expected random-SAT face counts; exact obstructions to face-vector transfers. | `internally-reviewed` | v2 by discrete_kinematics; reviewed independently by analytic_transfer at the recorded hash. |
| [P004](proofs/P004_hitting_time_tails.md) | Exact real mgf domain of T_n and a coupon-collector obstruction to the unmodified Poisson variance inequality. | `internally-reviewed` | v1 by analytic_transfer; reviewed independently by discrete_kinematics at the recorded hash. |

Internal review is neither external refereeing nor formal verification.
P003/P004 establish elementary statements, not a new sharp-threshold theorem.

## Approaches and experiments

[A001](attempts/A001_discrete_geometry/README.md) records the proposed transfer
programme. The prioritized analytic route seeks a finite-tilt variance/entropy
bound for T_n. Its first gap is a model-specific conditional-variance or
clause-deletion estimate under the tilted law. The geometric route needs an
invariant that both detects nonemptiness and admits useful concentration or
correlation estimates. The naive Euler/face-vector substitutions fail by P003.

[E001](experiments/E001_diagram_feasibility/README.md) completed a 60-instance
3-SAT runtime calibration on an Apple M3 with a 0.75-second process cutoff.
It retained 21 checked SAT witnesses, 9 unchecked UNSAT reports and 30 unknown
timeouts. All 20 sampled n=100/200 cases returned; larger sizes frequently
timed out. This supports a modest initial CPU pilot, not a maximum feasible
size, threshold estimate or validated scaling law. All inputs and verification
records are retained. That feasibility stage created no SLURM scripts or cluster
campaign. Saved SCRTP documentation was consulted as a snapshot.

E002 now provides the authorized scripts and independent-grid experiment code.
The default pilot has 600 3-SAT instances; a separate full grid has 24,800 and
a 2-SAT control has 8,400. Default arrays allocate four concurrent tasks of
16 CPU workers. Glucose42 through PySAT 1.9.dev15 supplies proofs checked by
a pinned DRAT-trim build. A local CaDiCaL proof-interface preflight failed
and is preserved; E001's timings do not calibrate this new certified workflow.
The exact model and sampling denominator are unchanged by solver timeouts.

## Checks and remaining gaps

The feasibility report built with no LaTeX/BibTeX or layout-box warnings;
all 10 pages were rendered and inspected. The canonical reviewed proof
hashes and source provenance are recorded. See
[feasibility QA](reports/QA_geometry_2026-10-11.md) and the preserved
[survey QA](reports/QA_2026-10-11.md). Builds and visual checks validate the
document, not the mathematics. External threshold proofs were not audited.

E002 validation passed 23 software tests, mocked SLURM checks, positive and
negative certificate preflight, and a 24-instance tiny smoke run whose 19 SAT
and 5 UNSAT classifications match exact truth tables. All five UNSAT proofs
were checked. Resume skipped existing results; output plots were inspected.
A separate agent reviewed the final runner at its recorded source hash.
See [E002 validation](experiments/E002_blythe_phase_diagrams/validation/README.md).
No Blythe jobs, target-node timings, production diagrams or GPU runs exist.

The later [uv validation](experiments/E002_blythe_phase_diagrams/validation/uv-setup-2026-10-11/README.md)
repeated the 23 tests and the same 24-case smoke configuration in a fresh locked
environment: 19 checked SAT and 5 checked UNSAT again agreed with exact truth
tables, and all plots were generated/inspected. Setup and a real helper dry run
passed. These repeated fixtures are software checks, not additional independent
scientific samples. Previous records and raw data are preserved.

## Ordered next actions

1. Derive the deletion/influence terms for the stated finite-tilt target,
   comparing the existing S032-S033 variance claims before claiming novelty.
2. Initialize/publish the prepared Git sources, clone on Blythe and run the
   locked uv/checker setup with an available compiler. Run E002's prepared
   certified pilot, and use its timings/censoring/storage to choose the final
   grid before submitting a larger batch. Preserve all unresolved outcomes.
3. Explore projection/overlap statistics at exhaustively accessible sizes;
   no such profile experiment has yet been run.
4. Queue scoped independent review of external threshold claims and P001/P002.

## Latest handoff

Converted environment setup to the root uv project, preserving the earlier
pip delivery and validation. Each machine creates its own `.venv`; the lock,
project metadata, exact installed packages, Python and checker are checked
before submission and again inside workers. Dependency downloads occur only
during explicit setup. The workflow supports optional site modules, with no
invented Python/compiler module names. The local uv environment and compiled
checker are ready. Git metadata creation is blocked by workspace permissions;
the guide gives the remaining local initialization and later GitHub commands.
This changes deployment, not the mathematical target or clause model.

## Previous handoff: Blythe preparation

Prepared E002 with source snapshots, immutable attempts, certificate artifacts,
machine-readable summaries, publication-format plotting, pinned dependencies,
site-specific SLURM scripts and local validation. Added S042 (Blythe job/storage
docs), S043 (checker source), and the A001 concentration prompt. Submission is
available through the helper's explicit --submit option; preparation made no
real scheduler call. The original setup left CPU Python/compiler module
selection to the user; the later uv setup can provision Python itself.
The first missing mathematical estimate remains unchanged.

## Previous handoff: feasibility assessment

Added A001, E001, P003/P004 and S038-S041, a separately compiled feasibility
report, source notes, canonical arguments and independent internal reviews.
The model remains independent proper k-clauses. Useful CPU diagrams are
feasible at modest sizes; scenario budgets are conditional on measured mean
runtime and are not forecasts. The user requested this assessment before
SLURM preparation, subsequently authorized above. The first missing mathematical step is the tilted-law
estimate; the first missing computational evidence is a longer certified
target-node pilot. No general transfer theorem or solved research programme
is claimed.
