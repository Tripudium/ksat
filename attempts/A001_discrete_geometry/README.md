# A001: discrete geometry and concentration for random k-SAT

- **State:** proposed; exact supporting identities and obstructions recorded.
- **Created / updated:** 2026-10-11.
- **Target:** explore the supplied geometry papers' methods in the unchanged
  proper random k-SAT model, and assess the cost of informative diagrams.
- **Report:** [editable LaTeX](../../reports/geometry-feasibility-2026-10-11.tex)
  and [PDF](../../reports/output/pdf/geometry-feasibility-2026-10-11.pdf).

## Routes and established facts

1. Transfer the tilted-variance proof architecture of S003, or the
   self-bounding entropy argument of S002, to the clause hitting time.
   The exact nonemptiness bridge is Pr(T_n>m)=Pr(F_k(n,m) SAT).
   S001 equations (2.4)-(2.5), p. 5, give the remaining-lifetime drift and
   globally forced-coordinate hazard. No new discovery of those identities
   is claimed.
2. Use finite cube symmetries, random coordinate restrictions and overlap
   distributions as discrete integral geometry. P003 supplies exact formulas
   and explicit failures of Euler/face-count substitutions.
3. Use softened energy observables for diagnostics; product-space
   concentration alone does not resolve the zero-energy atom defining SAT.

[P003](../../proofs/P003_discrete_kinematics.md) and
[P004](../../proofs/P004_hitting_time_tails.md) have independent internal
reviews at recorded source hashes. They are finite elementary results,
not a transferred sharp-threshold theorem.

## First unresolved step

For the prioritized analytic route, prove a useful tilted conditional-variance
or clause-deletion/influence bound with constants controlled uniformly in n
for fixed k >= 3. Tilting/conditioning destroys the original clause product
law; ordinary tensorization is insufficient. A finite-tilt sub-gamma bound
is a stated research target, not an established result. Compare S032-S033
before making novelty claims about variance order or concentration.

For the integral-geometric route, find an invariant that both controls
nonemptiness and admits the required concentration/correlation estimate.
Preserve the P003 counterexamples: they invalidate the naive auxiliary
claims, not the general programme.

## Experiments and next action

[E001](../../experiments/E001_diagram_feasibility/README.md) is a completed
60-instance runtime calibration with checked SAT witnesses, unchecked UNSAT
reports and preserved unknowns. It supports a modest CPU-first diagram
study; it is not a threshold estimate or proof of a scaling law.

Next mathematical action: specify one finite-tilt inequality and derive its
clause-deletion terms, or examine projection/overlap statistics at small
exhaustively accessible n. No such profile experiment has been run.
Next computational action: a longer target-node calibration including UNSAT
proof checking, then choose sizes, repetitions and batches before producing
SLURM scripts. The user requested the complexity assessment first.

## Supporting reading notes

- [Analytic mechanisms and limitations](analytic-findings.md).
- [Discrete integral geometry and complementary identities](discrete-findings.md).
- [Ready-to-use concentration research prompt](concentration_research_prompt.md),
  including the exact model, finite-tilt target, source audits, multiple methods
  and proof/evidence standards. Preparing this prompt is not a new proof attempt.

These are exploratory reading notes. Substantial completed proofs are in
canonical P003/P004 LaTeX and included in the report. No hypothesis of the
main model is weakened and no general random-SAT result is marked solved.
