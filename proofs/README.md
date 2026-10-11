# Proof and claim registry

Six claim records are registered. Files named `TEMPLATE` remain
forms only; literature results are tracked under S IDs in the source registry.

| ID | Exact statement and scope | State | Canonical source | Review record |
| --- | --- | --- | --- | --- |
| [P001](P001_clause_relaxation.md) | Every clause-sum LP with clause lengths at least two contains the all-one-half point; UNSAT proper k-CNFs exist for every k >= 2. | `proof-written` | [LaTeX](P001_clause_relaxation.tex), v1, 2026-10-10 | Independent review queued; author self-check only. |
| [P002](P002_few_clauses.md) | Every proper k-CNF with m < 2^k is SAT; at least 2^(n-k)(2^k-m) assignments satisfy it. The universal clause-count bound is sharp when unused variables and repeated clauses are allowed. | `proof-written` | [LaTeX](P002_few_clauses.tex), v1, 2026-10-11 | Independent review queued; author self-check only; standard result recorded in S037. |
| [P003](P003_discrete_kinematics.md) | Exact cubical intersection, projection and overlap identities; expected random-SAT face counts; explicit nonemptiness and log-concavity obstructions. | `internally-reviewed` | [LaTeX](P003_discrete_kinematics.tex), v2, 2026-10-11 | Authored by discrete_kinematics; independently reviewed by analytic_transfer at recorded hash. |
| [P004](P004_hitting_time_tails.md) | Exact real mgf domain of the proper-clause hitting time and a four-coupon counterexample to an unmodified Poisson variance bound. | `internally-reviewed` | [LaTeX](P004_hitting_time_tails.tex), v1, 2026-10-11 | Authored by analytic_transfer; independently reviewed by discrete_kinematics at recorded hash. |
| [P005](P005_rare_core_obstruction.md) | Polynomial early-UNSAT mass refutes the proposed uniform two-sided n-sub-gamma bound for every fixed k >= 2; shrinking negative tilts exhibit variance at least order n²/log n. | `internally-reviewed` | [LaTeX](P005_rare_core_obstruction.tex), v1, 2026-10-11 | Authored by analytic_transfer; [review](P005_review_2026-10-11.md) by discrete_kinematics. |
| [P006](P006_tilted_continuation.md) | Exact tilted continuation kernel and variance-occupation identity; conditional right-tail implication under the explicitly unproved (H+). | `internally-reviewed` | [LaTeX](P006_tilted_continuation.tex), v1, 2026-10-11 | Authored by root; [review](P006_review_2026-10-11.md) by analytic_transfer. |

For a new claim, copy [RECORD_TEMPLATE.md](RECORD_TEMPLATE.md) and
[TEMPLATE.tex](TEMPLATE.tex), using the next unused P ID (currently P007).
Do not reuse existing IDs. Substantial mathematics belongs in the
LaTeX source; the Markdown record tracks its scope, provenance, and review.

States: `draft`, `proof-written`, `internally-reviewed`, `gap-found`,
`superseded`. A `P` ID alone does not mean a claim is proved. Review must identify
the source version and its scope; internal review is distinct from external
refereeing and formal verification. Reopen review after substantive changes.

Proved counterexamples and obstructions belong here too; link to the affected
attempt. Link every dependency by ID or exact source location. Numerical checks
belong in the experiment registry and never replace a proof. Include canonical
fragments from the report with `\input{../proofs/P001_short_name}`; build the
report to obtain a reading copy. See [reports/README.md](../reports/README.md).
