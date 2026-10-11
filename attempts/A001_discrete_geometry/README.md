# A001: discrete geometry and concentration for random k-SAT

- **State:** active; original two-sided target refuted by P005, general programme open.
- **Created / updated:** 2026-10-11.
- **Target:** explore the supplied geometry papers' methods in the unchanged
  proper random k-SAT model, and assess the cost of informative diagrams.
- **Report:** [editable LaTeX](../../reports/geometry-feasibility-2026-10-11.tex)
  and [PDF](../../reports/output/pdf/geometry-feasibility-2026-10-11.pdf).

## Concentration investigation, 11 October 2026

The user explicitly invoked the research prompt. The exact two-sided finite-tilt
target is **refuted**, without changing the independent proper-clause model.
[P005](../../proofs/P005_rare_core_obstruction.md) proves a linear mean lower
bound and exhibits polynomially rare prefixes with T_n=2^k. These force failure
of the proposed n-sub-gamma bound, even at negative tilts of order log(n)/n.
Some such tilt has variance at least order n²/log n. The proof has an independent
internal review and uses no numerical evidence.

[P006](../../proofs/P006_tilted_continuation.md) gives an exact tilted
continuation kernel and variance-occupation identity. Its positive-tilt
criterion (H+) implies a right-tail bound only **conditionally**; (H+) is
unproved. This is a separately labelled research choice, not a silent repair
of the refuted target. The original target remains in the prompt.

The [dated source audit](../../references/concentration_source_audit_2026-10-11.md)
compares actual S001/S032/S033 proof mechanisms and current versions. Their
variance/Chebyshev conclusions do not assert the refuted exponential bound.
Fixed-confidence square-root windows for k >= 3 are not excluded by P005.
The follow-up is available as [LaTeX](../../reports/concentration-2026-10-11.tex)
and [PDF](../../reports/output/pdf/concentration-2026-10-11.pdf).

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

The former two-sided gap is now a proved obstruction (P005). For a separately
stated one-sided route, the first unproved estimate is P006's (H+): control
of the variance-occupation term under positive tilts with constants uniform
in n for fixed k >= 3. The exact state-dependent tilted kernel is available;
ordinary tensorization is still unavailable. Any lower-tail replacement must
retain exceptional mass compatible with P005. Removing a few observed core
types is not a proved transfer to the unconditional model.

For the integral-geometric route, find an invariant that both controls
nonemptiness and admits the required concentration/correlation estimate.
Preserve the P003 counterexamples: they invalidate the naive auxiliary
claims, not the general programme.

## Experiments and next action

[E001](../../experiments/E001_diagram_feasibility/README.md) is a completed
60-instance runtime calibration with checked SAT witnesses, unchecked UNSAT
reports and preserved unknowns. It supports a modest CPU-first diagram
study; it is not a threshold estimate or proof of a scaling law.

Next mathematical action: test a positive-tilt analogue of source clause-omission
estimates against the P006 kernel, or formulate a bound with explicit exceptional
lower-tail mass. No profile experiment was run. E002 subsequently supplied the
authorized SLURM/uv workflow. The user reports successful login-node setup on
Blythe; a certified compute-node pilot remains the next experimental step.
No new scientific experiment was run for P005/P006.

## Supporting reading notes

- [Analytic mechanisms and limitations](analytic-findings.md).
- [Discrete integral geometry and complementary identities](discrete-findings.md).
- [Ready-to-use concentration research prompt](concentration_research_prompt.md),
  including the exact model, finite-tilt target, source audits, multiple methods
  and proof/evidence standards. Its original target is preserved with a dated
  outcome notice; execution is recorded by P005/P006.

These are exploratory reading notes. Substantial completed proofs are in
canonical P003-P006 LaTeX and included in dated reports. No hypothesis of the
main model is weakened and no general random-SAT result is marked solved.
