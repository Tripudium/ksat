# P002: the sharp universal clause-count guarantee

**State:** `proof-written`.
**Version:** 2026-10-11, v1.
**Canonical source:** [P002_few_clauses.tex](P002_few_clauses.tex).
**Reading copy:** Section 2.1 of [the survey](../reports/output/pdf/report.pdf).

## Exact statement and scope

For integers n >= k >= 2 and m >= 0, every formula consisting of m proper
k-clauses on n available variables has at least 2^(n-k)(2^k-m) satisfying
assignments. Thus every such formula is SAT when m < 2^k. Conversely,
for each m >= 2^k an UNSAT formula exists, provided unused variables and
repeated clauses are allowed, as in the project model.

This is a standard elementary result, not a novelty claim or a random-SAT
threshold estimate. If clauses may have fewer than k distinct variables,
the stated universal guarantee need not hold.

## Dependencies and checks

Dependencies are the proper-clause conventions in [PROBLEM.md](../PROBLEM.md)
and the finite union bound. [S037](../references/S037.md), Theorem A and
the sharpness paragraph on page 4, gives the standard result. The canonical
fragment supplies a self-contained counting proof and the UNSAT construction.

The authoring agent checked m=0 (all 2^n assignments satisfy), m=2^k-1
(the lower bound is positive), m=2^k (the all-sign-pattern construction),
n=k, unused variables for n>k, and padding by repeats for m>2^k.
The four-clause k=2 example is written explicitly in Section 2.1.
No numerical experiment or solver run was used.

## Review

- Author: Codex, 2026-10-11.
- Independent reviewer: not assigned; independent review is queued.
- Scope of self-check: quantified statement, counting proof, sharpness,
  and distinction between exactly k and at most k literals.
- Source snapshot: survey v1.1, 2026-10-11; recorded in the report manifest.
- No unresolved step in the elementary written argument was identified;
  self-checking does not justify `internally-reviewed`.
