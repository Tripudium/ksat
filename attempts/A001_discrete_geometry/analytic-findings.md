# Analytic transfer from the supplied geometry papers

**Later outcome, 2026-10-11:** the historical proposals below are preserved.
P005 refutes the displayed two-sided finite-tilt target by a rare-core argument.
P006 supplies an exact tilted-process identity and a separately conditional
one-sided criterion. See the [current A001 record](README.md).

Reading note, 2026-10-11. This is a scoped source comparison and research proposal, not a new threshold proof or independent review of the sources. The original PDFs were read through their local text extractions. Page numbers below are printed page numbers; PDF page numbers are included where useful. No external theorem absent from the supplied/current project sources is needed for the observations below.

## 1. What the sharp-phase paper actually does

Source: Martin Lotz and Joel A. Tropp, *Sharp Phase Transitions in Euclidean Integral Geometry*, supplied `papers/sharp-phase.pdf`, published 2026 chapter, DOI `10.1007/978-3-032-06057-0_8`; existing S003. Its method is more specific than “convex sets concentrate.”

1. The generalized Steiner formula, Fact 7.2, equation (7.1), p. 222 (PDF p. 36), represents every suitable distance integral as a linear combination of intrinsic volumes. Positivity of the intrinsic volumes makes their normalized coefficients a probability law.
2. For rotation volumes, Proposition 8.1, pp. 223–224, turns an exponential tilt of that discrete law into a mixture of gamma distributions. The continuous potential is `J_theta(x)=2*pi*exp(theta)*dist(x,K)`. Its convexity makes the associated measure proportional to `exp(-J_theta)` log-concave.
3. Let `L(theta)=log E exp(theta I)` for the rotation-volume index. Lemma 8.3, equation (8.5), pp. 225–226 (PDF pp. 39–40), gives the exact cancellation

   `L''(theta) = Var_{mu_theta}(J_theta) - (n-L'(theta))`.

4. Fact 8.4 (Nguyen, Wang), equation (8.7), p. 226, says `Var_mu(J)<=n` for a convex potential on R^n and a probability density proportional to `exp(-J)`. Combined with the previous identity this gives `L''(theta)<=L'(theta)` for every real theta: Proposition 6.2, p. 217, completed p. 227.
5. Integrating that differential inequality yields `Var(I)<=E I` and the centered Poisson cgf bound `log E exp(theta(I-EI)) <= EI*(exp(theta)-theta-1)` for every real theta: Theorem 6.1, pp. 216–217 (PDF pp. 30–31). Exact integral-geometric identities then turn concentration into a transition; for example equation (10.2) and its use in Section 10.1, pp. 234–235.

The rigid-motion case uses another mixture/potential, not the same log-concave measure. Theorem 6.3, pp. 218–219, gives `Var(I)<=2*mu*(n+1-mu)/(n+1)`. Proposition 6.4, p. 219, establishes its counterpart under every exponential tilt. The analytic engine is Fact 9.5 (Nguyen), p. 231 (PDF p. 45): an inverse-Hessian variance inequality for density proportional to `J^(-(n+1))`, with J positive, twice differentiable and strongly convex. Lemma 9.4, pp. 230–232, uses `J=(1+exp(-2 theta)*dist(x,K)^2)^(1/2)`, a strong-convexity perturbation, and its gradient/Hessian identities. Its conclusion is

`Var(J^-2) <= 4/(n+4) * E(J^-2) * E(1-J^-2)`.

Thus an abstract discrete Poincare inequality alone is insufficient: one also needs a SAT-relevant observable and the analogue of the mixture identity/cancellation. The available curvature/convexity controls do not automatically hold for Boolean solutions.

Proposition 3.7, p. 200 (PDF p. 14), proves log-concavity of the weighted intrinsic volumes through Alexandrov–Fenchel and ultra-log-concavity of intrinsic volumes. The ensuing paragraph points to an alternative route through general ultra-log-concave concentration. Appendix D, Theorem 12.1, pp. 250–251 (PDF pp. 64–65), discusses stronger intrinsic-volume variance/cgf bounds. It is necessary to identify which discrete sequence is alleged to have this property: an arbitrary solution-count sequence is not automatically an intrinsic-volume sequence.

## 2. What the conic paper actually does

Source: Amelunxen, Lotz, McCoy and Tropp, *Living on the edge*, `papers/iau005.pdf`, Information and Inference 3 (2014), 224–294, DOI `10.1093/imaiai/iau005`; S002.

- Fact 5.7, equation (5.6), p. 251 (PDF p. 28), is a spherical Steiner mixture identity. It represents a projection probability using conic intrinsic volumes and reference probabilities for subspaces.
- Theorem 6.1, p. 254 (PDF p. 31), concentrates intrinsic-volume tails around statistical dimension, with width controlled by `sqrt(min(delta(C),delta(C^polar)))`.
- Its proof in Section 6.3, pp. 255–256, passes through Lemma 6.3, equation (6.8), a concentration bound for the squared projection of a spherical random vector. Polarity yields the opposite tail via equation (6.9).
- Appendix E.3, pp. 290–293, supplies the analytic engine. Fact E.2, equation (E.1), p. 291, comes from Gaussian logarithmic Sobolev. Sublemma E.3, equation (E.2), p. 291, gives a centered projection cgf bound of the form `2*theta^2*delta/(1-4*abs(theta))` for `abs(theta)<1/4`. The decisive self-bounding differential identity is equation (E.3): for `F(g)=||Pi_C(g)||^2-delta(C)`, `||grad F(g)||^2=4||Pi_C(g)||^2`.
- Theorem 7.1, pp. 257–258, then combines concentration with exact kinematics. A Boolean analogue needs both elements, including a link to exact feasibility. Gaussian Poincare appears elsewhere in the paper (e.g. Appendix C), but the main intrinsic-volume concentration proof uses Gaussian log-Sobolev and the projection identity above.

## 3. Precise obstructions to copying the inequalities

### A. Rotation-volume Poisson concentration does not hold for T_n verbatim

This is an elementary exact observation, not a simulation. Put `q=1-2^-k`. For every fixed n>=k and every integer m>=0,

`q^m <= Pr(T_n>m) <= 2^n q^m`.

The lower bound retains one fixed assignment; the upper bound is the union bound over all assignments. Consequently the positive mgf domain of T_n is exactly `theta < -log(q)`. At and above this positive boundary the mgf diverges. It therefore cannot obey an all-real Poisson cgf bound like sharp-phase Theorem 6.1.

Already at n=k=2, UNSAT occurs when all four sign-pattern clauses have appeared. T_n is the four-coupon collection time, a sum of independent geometric waiting times with success probabilities 1, 3/4, 1/2 and 1/4. Hence

`E T_n = 25/3`, `Var(T_n) = 130/9 > E T_n`.

Thus even the unmodified variance inequality fails. This refutes a literal transfer, not the prospect of a finite-tilt sub-gamma estimate with k-dependent constants.

### B. A universal square-root window would be wrong for k=2

The established 2-SAT window has order n^(2/3) clauses (S006, Theorem 1.1). Therefore one cannot transfer the conic square-root-in-dimension scale uniformly across all k. For k>=3, S032–S033 already record recent manuscript claims of linear hitting-time variance; proposing that order as a new result would require comparing those sources. A useful contribution might be an alternative structural proof or stronger quantitative tails.

### C. Boolean solution measures need not be log-concave or connected

The proper 2-CNF `(x or not y) and (not x or y)` has solution set `{00,11}`. Its Hamming-weight counts are `(1,0,1)`, which fail even ordinary log-concavity. Its uniform solution measure has positive covariance between the two bits, and single-coordinate moves cannot connect its two support points. Consequently an unrestricted assertion of ultra-log-concavity, negative dependence, or a positive single-bit Glauber spectral gap for SAT solution measures is false.

This is not merely a k=2 exception to the proposed counting geometry: when n=k, arbitrary subsets of the Boolean cube can be realized as proper k-CNF solution sets by including the clause excluding each unwanted assignment. For exact 3-CNF, the solution set `{000,111}` is obtained by excluding the other six assignments and has weight counts `(1,0,0,1)`.

One may still find a better observable or a probabilistic property of typical formulas. The counterexample only rules out attributing the required functional inequality to arbitrary Boolean solution sets.

## 4. Testable analytic programmes, ordered by usefulness

### Route 1: finite-tilt thermal variance for the clause hitting time

This keeps the central proof architecture of sharp-phase and already has an exact link to SAT: `p_m=Pr(T_n>m)`. Let `L_n(theta)=log E exp(theta T_n)`. Seek a local thermal variance inequality for `L_n''`, valid on a k-dependent interval inside `(-infinity,-log(1-2^-k))`, sufficient to establish a finite-tilt sub-gamma bound such as

`log E exp(theta(T_n-E T_n)) <= C_k*n*theta^2/[2*(1-b_k*abs(theta))]`

for a stated finite theta range and k>=3. This displayed inequality is a research target, not an established conclusion of this note; k=2 requires different scaling. It would be stronger than an untilted O(n) variance result and yield exponential tails.

The first unproved transfer is a local gradient/deletion or conditional-variance inequality for T_n which plays the role of the conic identity `||grad F||^2=4||Pi||^2`. T_n is not deterministically Lipschitz in clause replacement: one critical clause can complete an UNSAT core while replacing it with a repeat can postpone UNSAT arbitrarily far along a sequence. The supplied S001 already studies deletion/prolongation and forced variables; compare its argument before treating this mechanism as new. The root agent is recording the exact frozen-coordinate hazard identity separately.

The original clause input is a product measure, but weighting histories by `exp(theta T_n)` or conditioning on SAT generally destroys that product structure. Thus tensorization for the untilted input cannot simply be asserted for the tilted law. In sharp-phase, the Steiner-mixture representation is what supplies a controlled family of tilted measures; a discrete argument must replace this step explicitly.

First finite tests: compute/estimate tilted variance-to-mean ratios at modest n, including the exact coupon-collector boundary case; inspect whether any candidate inequality survives both signs of theta. Failure of a proposed inequality is informative. Numerical success is not a proof of uniform control.

### Route 2: transfer product-space concentration to softened SAT observables

For a fixed formula define `H_F(x)` as the number of violated clauses and `Z_beta(F)=sum_x exp(-beta H_F(x))`. Replacing one clause changes `H_F(x)` by at most one for every x. Therefore `log Z_beta` changes by at most beta, and `U(F)=min_x H_F(x)` changes by at most one. Because clauses are independent, product-space bounded-difference/entropy methods apply immediately. This uses the reusable analytic principle underlying the geometry papers without assuming fictitious Boolean convexity.

The first missing step is the connection from these concentration inequalities to exact SAT near the threshold. `U=0` is a boundary atom: O(sqrt(m)) fluctuations do not distinguish U=0 from U=1. For all formulas,

`-beta U <= log Z_beta <= n log 2 - beta U`.

Taking beta large enough to resolve a one-unit ground-state gap makes the simple beta*sqrt(m) concentration scale unhelpful. Applying functional inequalities instead to the tilted assignment measure requires a uniform spectral-gap/entropy estimate; the two-solution example shows why this can degenerate as beta grows. A high-temperature or weak-interaction restriction could be tractable, but it must not be silently substituted for the near-SAT threshold regime.

### Route 3: search for a positive, SAT-relevant discrete Steiner profile

A Hamming-distance partition identity is always available: for nonempty S and `a_r(S)=#{x:d_H(x,S)=r}`, `sum_x h(d_H(x,S))=sum_r a_r(S)h(r)`. This is a starting point, not an analogue with the full force of Steiner: no intrinsic-volume positivity transform, curvature estimate, polarity law, or intersection convolution has been supplied. The profile is undefined in this form for empty S, precisely the event to detect.

First specify the proposed coefficients and an exact formula relating their tails or convolution to survival under random clauses. Then test their positivity/log-concavity on explicit proper CNFs, including equality constraints and disjoint-variable products. Only after this identity survives should one seek a discrete Brascamp–Lieb, ultra-log-concavity, or entropy bound. Hamming-weight solution counts already fail the simplest test above. The integral-geometric agent/root is better placed to pursue exact cube-intersection identities.

Follow-up: `discrete_kinematics` has supplied an exact cubical face-count averaging identity in `tmp/geometry-transfer/discrete-lemma.tex`, together with explicit failures of Euler/nonemptiness equivalence, sufficiency of the face vector for intersection probability, and face-count log-concavity. The independent review is in `tmp/geometry-transfer/P003-review.md`. These examples sharpen the missing-step diagnosis for this route.

## Recommendation

Prioritize Route 1 with the finite-tilt domain stated explicitly, alongside an exact cube-incidence/hazard bridge. Route 2 supplies immediate rigorous concentration for useful diagnostic observables but does not by itself resolve exact satisfiability. Treat Route 3 as exploratory until a probability-valued coefficient sequence and an exact intersection identity are established. Avoid importing either a universal sqrt(n) scale or an all-real Poisson cgf from the continuous papers.
