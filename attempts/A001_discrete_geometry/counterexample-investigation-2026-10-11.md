# Counterexample investigation: rare early UNSAT histories

**Date:** 2026-10-11. **Role:** `discrete_kinematics`, counterexample investigator
and prospective independent referee. **Scope:** the exact two-sided finite-tilt
target in `concentration_research_prompt.md`, under its unchanged proper-clause
model. The initial rare-prefix obstruction was proposed by the coordinator.
No novelty claim is made. Canonical proof authorship is assigned separately to
`analytic_transfer` under P005; this note does not substitute for its review.

## Finding

The proposed two-sided bound is incompatible with rare, constant-size UNSAT
prefixes once the mean hitting time has an elementary linear lower bound.
The obstruction affects the **negative** tilt, even though the mgf is finite
there. It is different from P004's finite positive mgf boundary.

Fix k >= 2 and let r=2^k. Prescribe the first r clauses to be all sign patterns
on one specified k-element variable set, in one specified order. This event has
probability

\[
 [2^k\binom nk]^{-r}\ge 2^{-kr}n^{-kr}.
\]

On that event T_n=r: all r clauses are jointly UNSAT, whereas every proper
subset of these patterns leaves a satisfying assignment. Thus a deviation
of order n below a linear mean has at least polynomial, rather than
exponentially small, probability. Clause repetition being permitted does not
invalidate this distinct-clause event; it is a positive-probability event in
the exact sampling model.

## Independent check of a source-free linear mean lower bound

There is no need to import a full threshold theorem. A matching from clauses
to distinct incident variables gives a satisfying assignment: set each matched
variable to satisfy its own clause. Other occurrences do not undo that already
satisfied literal. Hall failure implies a set of t clauses whose variables lie
in some (t-1)-element variable set. Therefore, with m=floor(cn),

\[
 \Pr(F_k(n,m)\text{ UNSAT})
 \le\sum_{t=1}^{m}\binom mt\binom n{t-1}
       \left[\frac{\binom{t-1}k}{\binom nk}\right]^t.
\]

The author's proposed refinement, independently checked here, takes
c=1/(4e^2). Using
binom(n,t-1)=binom(n,t)t/(n-t+1), the standard binomial estimate, and
binom(t-1,k)/binom(n,k) <= (t/n)^k gives an upper bound

\[
 \frac{1}{(1-c)n}\sum_{t\ge1}t4^{-t}
 =\frac{D}{n},\qquad D=\frac4{9(1-c)}<1.
\]

Consequently E T_n >= (m+1)(1-D/n) >= cn/2 for all n>=k>=2. The m=0
case causes no problem: the failure sum is empty and F_0 is SAT. This route
uses only a finite matching argument, not S001/S032/S033 or any claimed
formalization. An augmenting-path explanation can make the matching dependency
self-contained in the canonical proof.

For comparison, my initial independent union bound indexed variable sets of
size s directly. With m=floor(n/10), it bounds matching failure by
e(1/10)^2 sum_(s>=k)(e^2/10)^s < 243/1000, giving E T_n>=n/40 for n>=20.
The author's O(1/n) bound above is cleaner and stronger; the initial route is
retained here solely as investigation provenance.

## Why a restricted negative-tilt interval still fails

Write mu_n=E T_n and K_n(theta)=log E exp(theta(T_n-mu_n)). The explicit
prefix event gives, for every lambda>0,

\[
 K_n(-\lambda)\ge\lambda(\mu_n-r)-kr\log n-kr\log2.
\]

Since mu_n>=gamma n with gamma=1/(8e^2), this lower bound is linear in
lambda at scale n. For any proposed constants C,b>0, choose a sufficiently
small fixed lambda in (0,1/b) so that the proposed quadratic upper coefficient
C lambda^2/[2(1-b lambda)] is strictly below gamma lambda. The log n terms
cannot close the gap as n grows.

The failure is visible at vanishing tilts too. Take lambda_n=L log n/n,
where L gamma>kr. Then

\[
 K_n(-\lambda_n)\ge(L\gamma-kr)\log n-O_{k,L}(1),
\]

whereas the target right side is O_(C,L)(log^2 n/n), tending to zero.
For sufficiently large n, lambda_n<1/b automatically. More generally, for
each fixed lambda>0 the exact prefix bound and E exp(-lambda T_n)<=1 imply
log E exp(-lambda T_n)=O_(k,lambda)(log n), so
K_n(-lambda)=lambda mu_n+O_(k,lambda)(log n).

These are analytic consequences of an explicit event, not numerical evidence.
The canonical author was informed of the vanishing-tilt strengthening before
the formal review stage.

## What this does and does not exclude

- It refutes the stated unconditional two-sided sub-gamma target with variance
  proxy C_k n on any n-independent neighborhood of zero, for every fixed k>=3
  (indeed the same obstruction applies for k=2).
- The finite positive mgf domain from P004 is fully compatible with the
  argument; the requirement 1/b_k<a_k does not repair a negative-tilt failure.
- It does **not** refute linear ordinary variance, a fixed-confidence square-root
  window, or an upper-tail-only sub-gamma inequality. The specified rare event
  has probability of order n^(-k2^k), and its individual contribution to the
  ordinary second moment is of order n^(2-k2^k), using P004's linear mean upper
  bound. This observation is not itself a proof of any variance/window claim.
- It does not supply a positive-tilt bound. P004 gives an exponential upper tail
  beyond the first-moment center (n log 2)/a_k, but that center can be separated
  from E T_n by order n; this cannot be relabeled mean-centered square-root
  concentration.
- Possible replacements include a visibly one-sided target, or an upper bound
  with an explicit exceptional polynomial term. Those remain research targets;
  no such bound has been established here. Conditioning away rare cores would
  change the ensemble and must be stated as a separate result.

## Source and review scope

Read the invoked prompt, project specification/status, P003/P004 canonical
records and independent reviews, A001 notes, and S001/S032/S033 source notes.
The relevant supplied arguments previously read are S003's exact-identity plus
tilted-variance architecture and S002's intrinsic-volume concentration. None
of their geometric inequalities is assumed for T_n. The current obstruction
does not depend on the recent external threshold or variance manuscripts and
does not independently verify them. Formal review of P005 awaits its frozen
canonical source and hash; this note is an investigation record only.
