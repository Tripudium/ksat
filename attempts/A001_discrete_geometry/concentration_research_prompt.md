# Research task: concentration of the random k-SAT hitting time

> **Outcome update, 2026-10-11:** the original brief below is preserved.
> Its concrete two-sided finite-tilt target is refuted by the independently
> reviewed [P005](../../proofs/P005_rare_core_obstruction.md). An exact tilted
> process and a separately conditional one-sided criterion appear in
> [P006](../../proofs/P006_tilted_continuation.md). See the
> [follow-up report](../../reports/output/pdf/concentration-2026-10-11.pdf).
> This refutes that target, not the general concentration programme.

Investigate rigorous concentration inequalities for the first unsatisfiable time in random k-SAT. Work across relevant areas of mathematics; the supplied convex-geometry papers are sources of ideas, not a restriction on methods. Seek a proof, a sharper intermediate statement, or a precisely demonstrated obstruction. Do not assume the proposed bound is true. Distinguish recovering an existing theorem, improving its proof, strengthening its conclusion, and proposing a genuinely new statement.

All paths below are relative to the repository root. First read `AGENTS.md`, `PROBLEM.md`, `STATUS.md`, the proof/attempt/experiment/source registries, and `attempts/A001_discrete_geometry/README.md`. Consult its analytic/discrete reading notes and `reports/geometry-feasibility-2026-10-11.tex`. Read the canonical arguments and independent review records for P003 and P004; their elementary conclusions are internally reviewed, not externally refereed or formally verified.

## Exact model and objective

For integers \(n\ge k\ge2\), sample an infinite sequence \(C_1,C_2,\ldots\) of independent clauses. Each clause chooses a uniform \(k\)-element subset of the \(n\) available variables and independent unbiased literal signs. Each clause therefore contains exactly \(k\) distinct variables; whole clauses may repeat and variables may remain unused. There are \(2^k\binom nk\) equally likely clause types. Set

\[
F_k(n,0)=\mathrm{True},\qquad F_k(n,m)=\bigwedge_{i=1}^m C_i,
\qquad T_n=\min\{m\ge0:F_k(n,m)\text{ is UNSAT}\}.
\]

All formulas for one \(n,k\) use successive prefixes of this same sequence. Thus, exactly,

\[
p_{n,k}(m):=\Pr(F_k(n,m)\text{ is SAT})=\Pr(T_n>m).
\]

Study fluctuations about \(\mathbb ET_n\), distinguishing variance bounds, fixed-level quantile windows, exponential tails, limiting distributions, and convergence of the center. A concentration result around \(\mathbb ET_n\) does not automatically locate that center within the same scale of \(\alpha_k n\). Keep \(k\) fixed as \(n\to\infty\); track every dependence on \(k\). Do not substitute planted, conditioned-SAT, regular, biased, or different clause models without a proved transfer.

One concrete target to investigate is:

> For every integer \(k\ge3\), do there exist finite constants \(C_k,b_k>0\), independent of \(n\), with \(1/b_k<a_k:=-\log(1-2^{-k})\), such that for every integer \(n\ge k\) and every real \(\theta\) with \(|\theta|<1/b_k\),

\[
\log\mathbb E\exp\!\left[\theta(T_n-\mathbb ET_n)\right]
\le \frac{C_k n\theta^2}{2(1-b_k|\theta|)}?
\]

This finite-tilt bound is a research target, not an established project theorem. Derive any claimed tail or quantile consequences explicitly, including dependence on the confidence level. Accept useful weaker or differently shaped bounds as intermediate results, but state exactly what they establish and what remains missing. Any restriction to sufficiently large \(n\), one tail, a smaller tilt interval, or a special ensemble must remain visible.

## Established constraints and source audit

P004 proves, with \(q=1-2^{-k}\),

\[
q^m\le\Pr(T_n>m)\le2^nq^m\qquad(m\ge0).
\]

Consequently \(T_n\) is finite almost surely and its real mgf is finite **exactly** for \(\theta<a_k\); the positive endpoint is excluded. An all-real Poisson cgf bound is impossible. At \(n=k=2\), \(T_n\) is a four-coupon collection time, with mean \(25/3\) and variance \(130/9\). Therefore even the unmodified inequality \(\operatorname{Var}T_n\le\mathbb ET_n\) fails. Published 2-SAT theory gives an \(n^{2/3}\) clause window (S006); use it as a control, not as evidence for an all-\(k\) square-root law.

P003 supplies exact cubical intersection, projection, and overlap identities, but also decisive limitations. A proper 3-CNF can have a nonempty solution complex with Euler characteristic zero. The sets \(\{000,110\}\) and \(\{000,111\}\) have identical face vectors but different random-intersection probabilities. A proper 6-CNF has face vector \((26,4,1,0,\ldots)\), violating log-concavity. These refute particular substitutions, not all discrete-geometric approaches. The clause-sum LP also always admits the all-one-half point for \(k\ge2\) (P001), including UNSAT cases.

Read actual primary sources, not only their summaries. Audit S001 (`papers/TR26-229.pdf`) and compare S032–S033 before making any novelty or open-status claim. For fixed \(k\ge3\), S001 claims \(\operatorname{Var}T_n=O_k(n^{1+2/k})\). S033 claims linear variance for \(k\ge4\) and an earlier \(O(n\log n)\) bound for \(k=3\); S032 subsequently claims linear variance for \(k=3\). Their complete proofs and any associated formal artifacts have not been checked by this project. Record versions, exact theorem locations, hypotheses, dependencies, corrections, and the precise scope of any audit. Do not treat a repository label or abstract as proof verification.

Two useful identities already appear in S001, equations (2.4)–(2.5), p. 5. If a nonempty solution set \(S\) has \(b\) coordinates constant across **all** its solutions, then a fresh random clause destroys \(S\) with probability

\[
h(S)=\frac{\binom bk}{2^k\binom nk},\qquad \binom bk=0\text{ if }b<k.
\]

Let \(r(F)\) be the expected number of clauses from a fresh independent continuation needed to make \(F\) UNSAT, setting \(r(F)=0\) for UNSAT \(F\). For SAT \(F\),

\[
\mathbb E_C r(F\land C)=r(F)-1.
\]

Do not confuse this fresh continuation with a clause selected by being the observed final destroying clause.

## Explore methods without committing prematurely

Compare several concrete approaches before choosing priorities. Possibilities include martingales and stopping-time inequalities; entropy, Efron–Stein, exchangeable-pair or self-bounding methods; structured covering and coupon-collector arguments; Boolean influences and sharp-threshold machinery; random restrictions and variable deletion; overlap/second-moment or interpolation methods; discrete geometry, isoperimetry and spectral methods; and generating functions, change of measure or information inequalities. Introduce other methods when their hypotheses fit. For each route, identify an exact observable, the desired lemma, the available structural input, and the first unproved implication.

The geometry papers suggest a reusable architecture: an exact probabilistic identity, control under exponential tilts, then concentration. Consult S003 (`papers/sharp-phase.pdf`, Sections 6–9) and S002 (`papers/iau005.pdf`, Appendix E.3) for the actual analytic mechanisms. For \(\theta<a_k\), set \(L_n(\theta)=\log\mathbb E e^{\theta T_n}\). Then \(L_n''(\theta)=\operatorname{Var}_\theta(T_n)\), where \(d\mathbb P_\theta/d\mathbb P=e^{\theta T_n-L_n(\theta)}\). This tilted law generally loses clause independence. Neither ordinary tensorization nor an untilted variance estimate automatically controls it. Clause replacement can postpone \(T_n\) arbitrarily far along an individual sequence, so deterministic unit bounded differences do not apply directly.

Softened observables may help but need a proved bridge: for \(\beta>0\), let \(U(F)\) be the minimum violated-clause count and \(Z_\beta(F)=\sum_x e^{-\beta H_F(x)}\), where \(H_F(x)\) counts clauses violated by \(x\). Replacing one clause changes \(U\) by at most one and \(\log Z_\beta\) by at most \(\beta\), while

\[
-\beta U(F)\le\log Z_\beta(F)\le n\log2-\beta U(F).
\]

Concentration on these scales does not itself decide the atom \(U=0\). Expose such missing bridges rather than treating a proxy as exact satisfiability.

## Independent investigation and evidence standards

Use complementary proof, counterexample and referee roles, with separate agents where available. The referee must not be the argument's author. Challenge every proposed inequality at boundary cases, small \(n=k\), repeated clauses, rare histories, both signs of the tilt, and its claimed parameter limits. Distinguish a pointwise assertion from one holding on typical states; quantify exceptional contributions before using expectations or exponential moments.

Numerics may guide conjectures or locate counterexamples, **never establish a general theorem**. Fits, simulations, symbolic output and unsuccessful searches do not prove concentration or exclude unsearched failures. Verify alleged counterexamples exactly or with rigorous certificates. A computer-assisted proof requires a proved reduction, justified exhaustive coverage, rigorous arithmetic/error control, and a checkable certificate or documented verification procedure with trusted components identified. Retain seeds, inputs, versions, precision, tolerances, timeouts, failed runs and contradictory outcomes. E001 is only runtime calibration; it supplies no concentration evidence.

Track every dependency. Label conditional conclusions as conditional; do not promote convenient assumptions into the model. Check nontrivial differentiation, limit exchanges, integrability, stopping arguments, and constant uniformity. Preserve failed routes with the exact obstruction. If independent review is unavailable, retain `proof-written`; self-checking cannot justify `internally-reviewed`.

## Deliverables and handoff

Maintain traceable source notes and verified bibliography entries; allocate unused P/A/E/S IDs from the current registries. Store substantial arguments in canonical LaTeX with explicit hypotheses and dependencies, separate review records with source hashes, and reproducible experiment records where applicable. Update relevant registries and `STATUS.md` to reflect actual progress. Build reports with `make report` and inspect the PDF; a successful build validates presentation, not mathematics.

Conclude with the strongest established statement, its proof/review scope, any refuted auxiliary claims, unresolved assumptions, the first remaining gap, and the next discriminating step. Do not claim exhaustive literature coverage, novelty, current open status, or a solved research programme without evidence. A precise obstruction or well-supported reduction is a useful outcome when a full concentration proof is unavailable.
