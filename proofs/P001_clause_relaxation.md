# P001: the elementary clause relaxation is always feasible

**State:** `proof-written`.
**Version:** 2026-10-10, v1.
**Canonical source:** [P001_clause_relaxation.tex](P001_clause_relaxation.tex).
**Reading copy:** Section 7 of [the survey](../reports/output/pdf/report.pdf).

## Exact statement and scope

For every CNF whose clauses each contain at least two literals, the linear
relaxation obtained by summing literal values and requiring each sum to be
at least one, with variables in [0,1], is feasible. The all-one-half point
is feasible. For each fixed k >= 2, all 2^k sign patterns on the same k
distinct variables give an UNSAT proper k-CNF with this feasible relaxation.

This elementary expository observation is not claimed to be novel. It rules
out this specific relaxation as an exact SAT decision method. It does not
rule out stronger lifts or a different connection to convex geometry.

## Dependencies and checks

Dependencies are the Boolean literal conventions in [PROBLEM.md](../PROBLEM.md)
and elementary arithmetic; there is no external theorem dependency.
The authoring agent checked the boundary k=2 (all sums equal one), k>2
(positive slack), the empty formula, and the all-sign-pattern counterexample
symbolically in the written argument. No numerical experiment is needed.

## Review

- Author: Codex, 2026-10-10.
- Independent reviewer: not assigned.
- Independent review: queued; self-checking does not justify `internally-reviewed`.
- Source snapshot: survey v1.0, 2026-10-10; checksum recorded in the report manifest.
- Remaining review task: check the quantified statement, the Boolean encoding
  and the limits of the geometric inference in Section 7.
