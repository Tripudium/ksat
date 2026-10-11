# Random k-SAT: thresholds, algorithms, and practical computation

**State:** initialized from the user's survey request.
**Last substantive revision:** 2026-10-11.

## Objective

Prepare a source-based survey of random k-SAT covering satisfiability thresholds,
algorithms for deciding satisfiability and finding satisfying assignments,
practical instance sizes, and GPU acceleration. Explain the relationship to the
supplied work on convex cone intersections and Euclidean integral geometry.
This initial project phase does not posit a new conjecture or seek to prove P=NP.

The next authorized phase explores discrete counterparts of the analytic and
integral-geometric arguments in the supplied convex-geometry papers. Identify
exact bridges to Boolean nonemptiness, explicit obstructions and the first
unproved estimate, without claiming a transferred theorem prematurely.
Separately assess the complexity of ALMT-style random-SAT phase diagrams
through a delegated feasibility study. Report cost and suitable initial sizes
before preparing SLURM scripts or launching a cluster campaign; saved SCRTP
documentation is available under `scrtp/`.

After receiving that feasibility assessment, the user authorized preparation of
Blythe SLURM experiment batches, reproducible result recording and plotting,
and a ready-to-use research prompt for concentration of T_n. Supply a locally
validated workflow and explicit site configuration; preparation does not imply
that a cluster campaign has been submitted or completed.

The user subsequently requested a Git-based transfer workflow and uv-managed
dependencies: prepare local repository files and the locked Python environment
so Blythe can clone/pull source and create its own environment. Remote GitHub
creation and actual cluster submission remain separate actions.

## Concentration investigation and outcome

The user explicitly invoked the A001 concentration research prompt on
2026-10-11. Its concrete target was a two-sided centered exponential-moment
bound C_k n theta²/[2(1-b_k|theta|)] for all n >= k and
|theta| < 1/b_k < -log(1-2^-k), with constants depending only on fixed k >= 3.
[P005](proofs/P005_rare_core_obstruction.md) refutes that exact target in the
unchanged model: polynomially rare early UNSAT cores obstruct negative tilts.
The original statement remains in the prompt with a dated outcome notice.

The broader investigation remains open. [P006](proofs/P006_tilted_continuation.md)
proves an exact tilted-process identity and an explicitly conditional
positive-tilt implication. Its hypothesis (H+) is not part of the model and is
not established. One-sided bounds or bounds with exceptional lower-tail mass
are separate possible research targets; no conditioned ensemble is substituted.

## Model and conventions

For integers n >= k >= 2, a clause contains k distinct variables selected
uniformly, with independent unbiased literal signs. F_k(n,m) is the conjunction
of m independent clauses; repeated clauses are allowed. Write alpha=m/n and
usually m=floor(alpha*n). Unless expressly stated otherwise, k and alpha are
fixed and n tends to infinity. “With high probability” means probability
tending to one over the random formula (and, where specified, algorithmic coins).
The empty formula is satisfiable.

Distinguish this distribution from planted, regular, biased, conditioned-SAT,
and industrial instances. Translate results from other clause models explicitly.
Natural logarithms are used. Running times distinguish worst-case guarantees,
average-case guarantees, measurements, and proposed planning budgets.

## Scope and evidence

- Separate existence of a sharp transition, convergence of its location,
  identification of its value, and finite-size window bounds.
- Separate decision, witness search, and certification of unsatisfiability.
  A timeout is unknown; a density prediction is not an instance certificate.
- Label published theorems, recent preprint statements, cavity predictions,
  empirical observations, and this survey's recommendations.
- Consult the supplied originals and primary algorithm/benchmark sources.
  Record exact locations, versions, applicability, and limitations under S IDs.
- Discuss convex geometry as a comparison. No transfer of geometric theorems
  to Boolean random k-SAT is assumed.

## Deliverables and completion criteria

Provide editable LaTeX, a bibliography, source notes, and a PDF built with
`make report`. Resolve build warnings affecting citations, references, or layout;
render and inspect the PDF. Practical size claims must identify their ensemble
and evidence. No new solver benchmark is required for this survey; any proposed
benchmark must be explicitly labelled as not run.

For the follow-up, provide a separate source-based feasibility note and any
canonical elementary arguments, with review scope recorded. A bounded local
runtime calibration may inform the complexity assessment; retain all inputs,
outcomes and unknowns. It is not a threshold measurement or a large CPU/GPU
campaign. Diagram plans must distinguish SAT probability from time-limited
solver success and specify sampling error, censoring and the status of UNSAT
certificates.

The survey literature cutoff is 2026-10-10, with targeted rather than exhaustive
coverage. The follow-up has additional targeted source checks dated 2026-10-11.
Full independent audits of the external threshold proofs remain separate tasks;
internal reviews of new elementary arguments are recorded under their P IDs.

## Supplied material

`papers/TR26-229.pdf` is Carenini's October 2026 random k-SAT preprint.
`papers/iau005.pdf` and `papers/sharp-phase.pdf` are the supplied geometry papers.
Contrary to the initial description of the inventory, `papers/montanari-phase.pdf`
is Montanari and Wang on neural-network feature learning, not a second k-SAT
paper. Preserve all four originals and acquire relevant k-SAT background.

## Revision history

| Date | Change | Effect |
| --- | --- | --- |
| 2026-10-10 | Initialize the former template from the user's stated topic and survey request. | No prior project claims existed; scope is a literature survey. |
| 2026-10-11 | Add the user-requested discrete-geometry exploration and delegated diagram-feasibility assessment. | The proper-clause model is unchanged; no new main conjecture or threshold theorem is asserted. |
| 2026-10-11 | Prepare the requested Blythe experiment workflow and concentration research prompt. | E002 records software validation separately from the unrun cluster campaign; the mathematical objective/model are unchanged. |
| 2026-10-11 | Prepare Git/uv project metadata and adapt Blythe setup to a shared lockfile. | Deployment changes only; local Git initialization is blocked by workspace permissions and remote creation remains pending. |
| 2026-10-11 | Execute the concentration research prompt; record P005/P006 and a scoped source audit. | The original two-sided target is refuted, the clause model is unchanged, and the positive-tilt implication remains conditional on (H+). |
