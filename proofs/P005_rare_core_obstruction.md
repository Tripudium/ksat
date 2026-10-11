# P005: rare early cores obstruct two-sided concentration

- **State:** `internally-reviewed` at the frozen version below.
- **Created / updated:** 2026-10-11, version 1.
- **Author:** `analytic_transfer` agent.
- **Canonical source:** [P005_rare_core_obstruction.tex](P005_rare_core_obstruction.tex), theorem `thm:P005-target-refuted`.
- **Frozen source SHA-256:** `77d70d65ea2b2330ee3ab786731ecfbda4842dfe49de24e1eff638b6951f386a`.
- **Related attempt:** [A001](../attempts/A001_discrete_geometry/README.md).
- **Affected target:** the exact two-sided finite-tilt inequality in [the concentration research prompt](../attempts/A001_discrete_geometry/concentration_research_prompt.md).

## Exact statement and scope

In the unchanged independent proper-clause model, for every fixed k >= 2 there are **no** finite positive C,b, independent of n, for which the centered cgf is at most C n theta^2/[2(1-b|theta|)] for all sufficiently large n and all |theta|<1/b. In particular, the stated k >= 3 target fails. The proof uses negative tilts only and is independent of the exact positive mgf boundary.

The source proves an elementary uniform lower bound E T_n >= n/(8e^2) using a clause-to-variable matching argument. Writing B=2^k, the first B clauses can be all B sign patterns on one fixed set of k variables, in any order. This event has exact probability B!/[B binom(n,k)]^B and forces T_n=B. Its probability is polynomially small in n for fixed k.

For each fixed s>0, log E exp(-sT_n)/n tends to zero, while the centered cgf divided by n has lower limit at least s/(8e^2). That linear dependence on s contradicts the proposed uniform quadratic bound near zero. Failure also occurs at s_n=A log(n)/n for every fixed A>k 2^k/(1/(8e^2)): the centered cgf grows at least a positive multiple of log n, while the proposed upper bound tends to zero. On [−s_n,0] the tilted variance consequently reaches at least a positive k,A-dependent multiple of n^2/log n.

This refutes the specified two-sided target, not the general research programme, a linear untilted variance claim, fixed-confidence square-root windows, or positive-tilt-only concentration. Removing early cores by conditioning changes the ensemble and is not an implicit repair.

## Dependencies and source comparison

The proof is elementary and reproduces the needed matching, union-bound, and few-clause arguments. P002's clause-count guarantee is proved again within the fragment, so its unreviewed record is not assumed. P004 supplies finite moments and the mgf domain; the upper-tail union bound needed for finite moments is also stated explicitly. Twice differentiating on a nonpositive compact tilt interval is justified by integrable domination and a positive normalizer.

The relevant supplied originals were consulted through their retained text extractions: S001, Section 2, equations (2.2)–(2.5), printed p. 5, and S003, Theorem 6.1/Proposition 6.2 and their reduction, printed pp. 216–218. The argument contradicts neither source's stated geometric theorem nor S001's variance theorem. S032/S033 are being audited separately; no claim from those manuscripts is used in this proof. P003/P004 and their review records were read to distinguish previously established obstructions from this new investigation. No novelty or exhaustive literature claim is made.

## Argument status and checks

No gap is identified in the author's completed argument. The Hall union bound handles m=0, deficient sets smaller than k, repeated clause indices as distinct left vertices, unused variables, arbitrary literal signs, and n=k. All asymptotic statements keep k fixed. The early-core probability is a lower bound for Pr(T_n=B), not an asserted classification of every minimal cover.

No simulations, numerical fitting, or finite-search evidence form part of the proof. No scientific experiment was run. The independent review covers the frozen canonical source; report compilation and presentation are separate checks.

## Review and next action

- **Independent reviewer:** `discrete_kinematics`, 2026-10-11; [full review](P005_review_2026-10-11.md).
- **Review scope:** full proof, constants, every quantifier, matching criterion, core event count, shrinking tilt, differentiability and tilted-variance conclusion at the frozen hash above. No gap found.
- **External/formal status:** none claimed.
- **Next action:** investigate a separately stated one-sided or exceptional-tail replacement; retain the exact refuted target and unchanged ensemble.
