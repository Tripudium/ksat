# Concentration-source audit: S001, S032, S033

Date: 2026-10-11. Auditor: `diagram_feasibility`, literature-audit role.
Task: the explicitly invoked [concentration research prompt](../attempts/A001_discrete_geometry/concentration_research_prompt.md).

## Verdict and scope

**The proposed two-sided, `O_k(n)` variance-proxy subgamma bound is not a theorem of any of these three sources.** Their central concentration conclusions are variance bounds, fixed-level quantile windows, and Chebyshev tails. Their exponential estimates concern a far-right tail beyond a sufficiently large linear cap, or auxiliary root-incidence counts. Neither kind supplies centered exponential concentration.

The rare fixed-variable UNSAT core identified during this project is compatible with all three sources. Their model includes repeated clauses and unused variables, and their proofs do not condition away early UNSAT instances. In particular, the two clause-omission papers retain and average the exceptional collision environments.

This audit checked the statements, model, relevant inequalities, conditioning, and exceptional-event accounting described below. It did **not** verify every theorem, external dependency, appendix, or any formal artifact. No whole-paper correctness, external refereeing, novelty, or literature-wide open-status claim follows. Older S001/S032/S033 notes are preserved.

## Sources and current-version check

All page numbers below are both printed page numbers and one-based PDF page numbers.

| ID | Source/version | Stored PDF SHA256 |
| --- | --- | --- |
| S001 | Gaia Carenini, *A polynomial scaling window for random k-SAT and a proof of the satisfiability conjecture*, ECCC TR26-229, public 5 October 2026 | `38243eedfd7a4b89abb2c862d3476924ed238ecb8efd9f67577bc75707fdcd40` |
| S032 | OpenAI, *Linear Variance of the Random 3-SAT Hitting Time*, preprint dated 5 October 2026 | `01f912a6aaba76c36cb38913ae3d902329696e1e5502feed9b71903d42b8bc08` |
| S033 | OpenAI, *Variance of the Random k-SAT Hitting Time*, preprint dated 27 September 2026 | `9e47a7c16a835f9111435037d4103a0dd974111512c62c0f0e9c96ea14bc2d56` |

Primary locations inspected on the audit date:

- [ECCC record](https://eccc.weizmann.ac.il/report/2026/229/) and [current PDF](https://eccc.weizmann.ac.il/report/2026/229/download). The record lists publication on 5 October 2026 and no correction/revision notice. A fresh download has exactly the stored S001 hash above.
- [S032 directory](https://github.com/openai/math/tree/main/preprints/Linear-Variance-of-the-Random-3-SAT-Hitting-Time-October-5-2026) and [PDF](https://raw.githubusercontent.com/openai/math/main/preprints/Linear-Variance-of-the-Random-3-SAT-Hitting-Time-October-5-2026/linear-variance-of-the-random-3-sat-hitting-time.pdf).
- [S033 directory](https://github.com/openai/math/tree/main/preprints/Variance-of-the-Random-k-SAT-Hitting-Time-September-27-2026) and [PDF](https://raw.githubusercontent.com/openai/math/main/preprints/Variance-of-the-Random-k-SAT-Hitting-Time-September-27-2026/article.pdf).
- Both fresh OpenAI PDF downloads have exactly the stored hashes above. Each directory's public GitHub API commit history, requested with `per_page=100`, returned only `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, committed 2026-10-06T21:58:50Z, message `Initial commit`.
- The two directory READMEs contain their title, author, date, and citation, with no correction/withdrawal notice. The repository [history](https://raw.githubusercontent.com/openai/math/main/history.md) describes unrelated October 7 corrections and withdrawals. Its [contents](https://raw.githubusercontent.com/openai/math/main/CONTENTS.md) describes these papers as variance results. This is a dated check of the named primary locations, not an exhaustive search for every possible subsequent comment.

Metadata snapshot hashes: S032 README `f435147e898481123456e8b44343feb28e3b23e5108e70f31e605fc30df51a48`; S033 README `33506da04b06e52ad3eaf4514116ab942958e7054906f70d871e5af1fdb66b31`; repository `history.md` `41c2a2d470014b3628695c7aabf5fd0c93f6f687621fca172062f22b59ed6a1e`; `CONTENTS.md` `cc7c0b8a1cdedd845a777e77cf682657308503daf8346c1349e06e9259d063c2`.

The audit used the actual retained PDFs and their text extractions. Theorem 1.3 on S001 p.2, the collision estimate on S032 p.7, and Lemma 6.1/proof on S033 pp.17–18 were also inspected as rendered PDF pages.

## Model and exact concentration claims

The sources' `T_n` (S001) and `H_n` (S032/S033) are the project's first UNSAT prefix index: iid uniform proper clauses, fair independent signs, distinct variables within each clause, repetitions between clauses allowed. The empty prefix is SAT. No planted, conditioned-SAT, regular, or distinct-clause substitution is involved.

| Source | Exact relevant statement | What it does not assert |
| --- | --- | --- |
| S001, Theorems 1.1/1.3, p.2 | Fixed `k>=3`: `Var(T_n)<=C_k n^(1+2/k)`; for every `x>0`, tail at most `min(1,C_k n^(1+2/k)/x^2)`. For each fixed `eta` in `(0,1/2)`, central window `O_(k,eta)(n^(1/2+1/k))`. | Exponential centered tails or a cumulant bound. The source explicitly invokes Chebyshev. |
| S032, Theorem 1.1, p.1; Corollary 5.2, pp.9–10 | For `k=3`, upper `Var(H_n)<=Cn` for all `n>=3`, lower `>=cn` eventually; each fixed central window is `Theta_eta(sqrt(n))`. | An estimate uniform as the quantile level tends to zero exponentially in `n`; an MGF bound; concentration around `alpha_3 n` at square-root scale. |
| S033, Theorem 1.1, pp.1–2; Corollary 5.2, pp.16–17 | `Var(H_n)<=C_k n ell_k(n)`, where `ell_3=log(en)` and `ell_k=1` for `k>=4`; eventual lower `c_k n`. Capped upper bounds hold at every fixed positive density. Equation (5.11) gives a `C_k/t^2` tail at scale `sqrt(n ell_k(n))`. | Centered exponential tails, higher-cumulant control, or a rate for `EH_n-alpha_k n`. The latter limitation is explicit on p.17. |

The variance lower bounds and central-window lower bounds use Wilson's Corollary 4. That external theorem was not re-proved in this audit. The expected-time lower bound below does not require it or the existence of a limiting threshold.

## Checks of the relevant proof mechanisms

### S001: remaining lifetime and variable deletion

Sections 2–4, pp.5–9, were read and the following steps checked:

- Equations (2.2)–(2.4): the assignment union bound, finite expected lifetime, and the exact one-step drift of fresh remaining lifetime. These apply also after exceptionally early UNSAT; the lifetime is defined to be zero at an UNSAT state.
- Equation (2.5) and the additive-error comparison (2.6): one-clause killing is determined by globally frozen coordinates. The error is needed when exactly `k-1` coordinates are frozen.
- Lemma 2.1, p.6: the Poisson interpolation, Jensen step, survival submultiplicativity, and integration giving the shorter-clause replacement estimate. This concerns a fresh independent continuation from an arbitrary deterministic SAT state, not the terminal observed killing clause.
- Lemma 3.1, p.7: a concave potential, ordinary conditional expectation, telescoping, and monotone convergence give an **untilted** occupation estimate. Proposition 3.2 then uses Poisson splitting and independent variable branches.
- Equation (4.1) uses Aldous's covering inequality, quoted as Theorem 4.1 on p.8. The subsequent terminal-state decomposition and (4.2)–(4.1) estimate yield the stated variance order. This audit checked that algebra and conditioning, but did not independently audit the Aldous primary theorem or the separate Abbe–Montanari threshold-convergence argument.

No missing step was found in these checked local arguments. Their output is a second-moment estimate. An extension of Lemma 3.1 or the variable-deletion identity to a law weighted by `exp(theta T_n)` is not supplied.

### S032: the complete main upper-bound chain

The core upper-bound argument in Sections 2–5.1, pp.3–9, was read and checked at the following points:

1. Lemmas 2.1–2.2: the `u^-3` boundary error, Jensen/power-sum inequalities, and the telescoping bounded potential `P_d=sum_(j<d) q_j`.
2. Lemma 3.1: coordinate omission bounds the capped variance by `sum_i E D_i^2`; it is a martingale orthogonality argument under the original independent-clause law.
3. Section 3.1 and Lemma 3.2, pp.5–6: revealing future root types does not reveal future ordinary contents. The smaller filtration hides root-test parts; the larger one knows pivotality. Root-flip tests are independent in the smaller filtration. The conditional product law was checked by counting allowed nonroot completions at each independent clause index.
4. Lemma 4.1, Corollary 4.2 and Proposition 4.3, pp.6–7: the potential telescopes only over ordinary steps, with nonordinary steps bounded separately. Conditioning first on the larger filtration, then on the smaller one, validly combines duration and pivotality. The collision cases are all retained:
   `E[D_i^2|E] <= 2K^2 d^3 1_(V=0) + 2KL d^(3/2) 1_(V=1) + L^2 1_(V>=2)`.
5. Lemma 4.4, p.8: incidence moments and collision-weighted incidence moments are taken **before** fixing the exposure. Independence at distinct positions yields `P(V>=2)=O(n^-2)`. Thus multiplying by the deterministic squared cap `L^2`, with `L=10n`, is harmless for a second moment.
6. Equations (5.1)–(5.2), pp.8–9: the first-moment survival tail controls the second moment of the excess beyond `10n`; `2(7/8)^10<1`. The finitely many `3<=n<6` cases are covered by the same elementary tail bound.

No gap was identified in this checked upper-bound chain. This remains a scoped manual source audit, not formal verification of the paper or its Wilson-dependent lower bound. In particular, the second-moment handling of collisions does not bound their contribution after a fixed negative hitting-time tilt.

### S033: conditioning and exceptional environments

Checked the deterministic-set/fresh-clause conditioning in Lemma 2.2 and Proposition 2.3 (pp.6–7); the two filtrations and root-flip argument in Lemmas 3.2–3.4 (pp.8–10); conditional occupation and its layer-cake integration in Lemmas 4.1–4.2 (pp.11–13); and collision accounting in Proposition 4.3 and Lemma 4.4 (pp.13–14). No gap was identified in those checked steps. The underlying block-comparison Lemma 2.1 and the appendices were not fully independently audited here.

The decisive exceptional-case estimate is (4.5): a collision-free term, a one-collision term of size `L d^beta`, and an unrestricted `L^2 1_(V>=2)` term. Lemma 4.4 proves, for each fixed moment order and collision count, `E[d^p 1_(V>=r)]<=C_(k,B,p,r)n^-r`. It does **not** discard high-incidence or collision events. These are polynomial probability estimates sufficient for the claimed squared deletion delays.

## Linear mean lower bound without a threshold theorem

S033 Lemma 6.1, pp.17–18, states, for every `0<c<exp(-2)`, every integer `k>=3`, every `n>=k`, and `j=floor(cn)`,

\[
\Pr(T_n\le j)\le \frac{ec}{n^2}
\sum_{t=1}^{\infty}t^2(e^2c)^t=O_c(n^{-2}).
\]

Its proof was independently checked. A matching of all clause positions to distinct incident variables supplies a SAT assignment, regardless of signs. Hall failure implies that some `t` variables contain at least `t+1` complete clauses. Independence gives the union bound

\[
\sum_{1\le t\le n,\ t+1\le j}
\binom nt\binom j{t+1}(t/n)^{k(t+1)}.
\]

The falling-factorial containment probability is at most `(t/n)^k`, with probability zero for `t<k`. Using `k>=3`, `j<=cn` and the standard binomial bound gives the summand at most `ec(e^2c)^t(t/n)^(t+2)`, hence the displayed convergent series. Boundary cases with no summands cause no problem. Consequently

\[
\mathbb ET_n\ge (\lfloor cn\rfloor+1)
\bigl(1-O_c(n^{-2})\bigr),
\]

and in particular `ET_n=Omega(n)`. This sparse-prefix estimate allows polynomially unlikely small cores; it never asserts exponential suppression of them.

## Rare cores, exponential moments, and the first failed extension

Put `r=2^k` and fix one set of `k` variables. The event that the first `r` clauses are all `r` sign patterns on those variables, in any order, has probability

\[
\frac{r!}{\bigl(r\binom nk\bigr)^r}>0.
\]

It forces `T_n=r`, using P002's SAT guarantee below `r` clauses (reproved within P005). For fixed `k`, this event has polynomial probability in `n`. It is allowed by every source's model. This observation and the preceding linear mean lower bound give a fixed-negative-tilt obstruction to the proposed `O(n)` two-sided subgamma target. The project's canonical claim/proof record, prepared separately, carries the full counterexample; this note records its compatibility with the literature.

In detail, the contribution of this event to the centered MGF at `theta=-s<0` has logarithm at least `s(ET_n-r)-O_k(log n)`. For arbitrarily small fixed `s>0`, this is linear in `s n`, whereas a uniform subgamma bound with constants depending only on `k` is quadratic in `s` near zero. A variance bound or any fixed central quantile window does not make that contribution disappear. Clipping only the **upper** tail at `Bn` leaves the early-core event intact.

The relevant exponential statements in the sources are narrower:

- S001 (2.2), p.5; S032 (5.1), p.8; S033 (5.1), p.15: `P(T_n>m)<=2^n(1-2^-k)^m`. This gives exponentially small excess beyond `Bn` when `B>log(2)/[-log(1-2^-k)]`. It also proves finiteness of positive exponential moments below that endpoint; the project's P004 additionally proves the endpoint is exact.
- S032 Lemma 4.4, p.8, and S033 Lemma 4.4, pp.13–14: the bounded exponential moment is `E exp(Z)`, where `Z` counts clauses incident to a fixed set of roots through a linear cap. It is not a centered hitting-time MGF.
- No checked theorem supplies factorial higher-cumulant bounds, an estimate for `Var_theta(T_n)` on a fixed two-sided tilt interval, or a bound on the exponentially weighted collision costs.

**First unproved extension:** replacing the original product law in a variance, drift, replacement, or root-test estimate by the globally tilted law `dP_theta proportional to exp(theta T_n)dP`. Fresh ordinary clauses and root-test families need not retain their conditional product laws under this reweighting. The sources' proofs explicitly need those laws. Moreover, no repair can establish the stated unconditional two-sided target, because the early-core obstruction already contradicts it. A positive-tilt-only statement, a different error term, or a conditioned/trimmed model would be a new statement requiring an explicit model/target change and its own proof; none is established by this audit.

## Handoff

No new S ID is needed: this is a dated audit of S001/S032/S033. No bibliography or global registry was edited. The coordinator should link this note from the relevant source records and distinguish the checked proof scope from complete source verification. The next mathematical action is to record and independently review the rare-core obstruction, then revise the concentration target explicitly before further work on exponential tilts.
