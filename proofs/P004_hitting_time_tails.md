# P004: hitting-time mgf domain and a Poisson-bound obstruction

- **State:** `internally-reviewed`.
- **Version:** 2026-10-11, v1.
- **Canonical source:** [P004_hitting_time_tails.tex](P004_hitting_time_tails.tex).
- **Author:** `analytic_transfer` agent.
- **Independent internal reviewer:** `discrete_kinematics` agent.
- **Reviewed SHA-256:** `934470137063cb724fb5013420f80f2b8fad15809885ffbd6f419741d845fa16`.
- **Review:** [scoped review](P004_review_2026-10-11.md).
- **Related attempt:** [A001](../attempts/A001_discrete_geometry/README.md).

## Exact scope

For every fixed n >= k >= 2 and m >= 0 in the common proper-clause process,
q^m <= Pr(T_n > m) <= 2^n q^m, with q=1-2^(-k). Thus T_n is finite almost
surely and its real mgf domain is exactly theta < -log(q), excluding the
positive endpoint. Explicit mgf bounds and their proof are in the source.
At n=k=2, E T_n=25/3 and Var T_n=130/9: the unmodified rotation-volume
variance inequality Var(I)<=E I fails for T_n.

The argument uses a fixed assignment, the finite union bound and Tonelli
for nonnegative summands; the example uses independent geometric waiting
times in a four-coupon collection process. This is an elementary observation,
not a novelty claim. S003 Theorem 6.1 identifies the geometric bound being
compared; the proof does not assume a threshold theorem.

## Review and limitations

The independent reviewer checked the full argument, both mgf-domain
directions and boundary, geometric conventions and moments, and implication
scope. No gap was found. This is internal review, not external refereeing
or formal verification. The canonical source matches the reviewed bytes.
No numerical test is part of the proof.

The result rules out an all-real Poisson cgf bound for this unbounded hitting
time. It does not rule out finite-tilt sub-gamma bounds, k-dependent variance
constants, or different observables. Obtaining such a bound remains an
unproved proposed step in A001, with no new open-status or novelty claim.
