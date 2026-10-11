# Discrete integral geometry: scoped findings

**Prepared:** 2026-10-11. **Status:** author derivations and checks; no novelty or
independent-review claim. No shared registry or report was edited.
The canonical draft requested by the coordinator is
[P003_discrete_kinematics.tex](../../proofs/P003_discrete_kinematics.tex).

## What actually transfers from the supplied geometry papers

In **S003, sharp-phase.pdf**, Section 4.3, printed p. 211, the stated strategy
is: rewrite an exact integral-geometric identity as a convolution of positive
weighted intrinsic-volume sequences; interpret it probabilistically; apply
concentration. Section 3.4, pp. 199-200, explains that the concentration proof
uses Steiner's formula to replace the discrete index by a continuous variable
under a concave measure. Section 3.6, Proposition 3.7, p. 200, identifies the
Alexandrov-Fenchel source of log-concavity. Section 5, pp. 211 onward, separates
the general generating-function argument from the geometric input; equations
(5.5)-(5.6) identify the first two cgf derivatives with tilted mean and variance.

In **S002, iau005.pdf**, Fact 2.1, printed p. 228, already gives a formula for
the *nontrivial-intersection probability*, not merely expected intersection
size. Fact 5.5, pp. 250-251, supplies positivity, normalization, polarity,
Gauss-Bonnet, and product convolution for conic intrinsic volumes. Theorem 6.1
and Theorem 7.1 provide concentration and its kinematic application.

Boolean signed coordinate permutations supply a genuine finite replacement
for averaging over rotations. What does not transfer automatically is the
valuation/nonemptiness bridge or positivity plus concentration of the right
coefficients. The Euclidean theorem about an integrated *weighted volume*
also should not be silently described as an intersection probability.

## Exact cubical analogue and decisive obstructions

For S contained in Q_n={0,1}^n, form the cubical complex K(S) consisting of all
coordinate faces whose vertices all lie in S. Let f_j(S) count j-faces and
N_j=2^(n-j) binom(n,j). A uniform signed coordinate permutation g acts
transitively on j-faces, so

    E_g f_j(S intersect gT) = f_j(S) f_j(T) / N_j.

Consequently an exact bilinear formula also holds for Euler characteristic,
with alternating coefficients (-1)^j. The full proof and empty/boundary cases
are in the LaTeX draft. There are two distinct, exact obstructions:

1. The proper 3-CNF (x∨y∨z) AND (¬x∨¬y∨¬z) leaves six cube vertices forming a
   6-cycle. Its Euler characteristic is zero although it is satisfiable.
2. S={000,110} and U={000,111} have the same face vector (2,0,0,0), but
   P(S intersect gS nonempty)=5/12 and P(S intersect gU nonempty)=1/2.
   Thus the face vector cannot determine intersection probability. Each set
   is itself the solution set of a proper 3-CNF with six clauses.

Nonnegativity and group invariance of f_j survive. Log-concavity does not:
an explicit n=k=6 example in the draft has f=(26,4,1,0,...), so 4²<26·1.
The normalized counts f_j/N_j fail as well. This refutes a universal claim
for these particular counts, not a typical-instance theorem for fixed k.
A finite enumeration agreed with the exact elementary face count; the
counting proof, rather than enumeration, is the justification.

For random k-SAT with independent clauses, the draft also proves

    E f_j(S_m) = N_j (1-q_j)^m,
    q_j = sum_r binom(n-j,r) binom(j,k-r) 2^(-r) / binom(n,k).

Here q_j is the probability that one clause excludes at least one vertex of
a fixed j-face. This gives a cheap analytic diagram of expected face counts
or Euler characteristic, but such a diagram is not a SAT-probability diagram.

There is also a simple finite-set valuation obstruction: a valuation v on
*all* subsets of Q_n, with v(empty)=0 and invariance under this transitive
group, is a constant multiple of cardinality. Indeed, finite additivity
gives v(S)=sum_{x in S}v({x}), and all singleton values agree. Nonemptiness
is not a valuation on arbitrary subsets. Enlarging to cubical complexes
permits richer valuations, but introduces the topology obstruction above.

## Overlaps and Fourier levels: a richer positive replacement

Let N=2^n and let A_d(S) count ordered pairs (x,y) in S² at Hamming distance d.
For Z=|S intersect gT|, transitivity on ordered pairs of each distance gives

    E Z = |S||T|/N,
    E Z² = sum_(d=0)^n A_d(S) A_d(T) / [N binom(n,d)].

The proof is identical to the face proof: for fixed x,y at distance d,
(g^(-1)x,g^(-1)y) is uniform over N binom(n,d) ordered pairs. Hence

    (E Z)² / E Z² <= P(Z>0) <= min(1,E Z)

when E Z>0; if either set is empty the probability is zero. The lower bound
is Cauchy-Schwarz applied to Z·1_{Z>0}. It is informative only when overlap
correlations keep E Z² sufficiently close to (E Z)².

For the normalized Walsh transform hat(f)(I)=N^(-1) sum_x f(x)(-1)^(sum_I x_i),
put W_r(S)=sum_{|I|=r} hat(1_S)(I)^2. Then W_r>=0,
sum_r W_r=|S|/N, and W_0=(|S|/N)^2. Averaging translations first, then
coordinate permutations, gives the equivalent positive identity

    E Z² = N² sum_(r=0)^n W_r(S)W_r(T)/binom(n,r).

With K_r(d)=sum_l (-1)^l binom(d,l)binom(n-d,r-l), a direct character sum gives

    sum_d A_d(S) K_r(d) = N² W_r(S) >= 0.

These are the familiar Hamming/Fourier positivity constraints behind
Delsarte's method, not new results. Product sets have convolution of their
W-profiles. But even the solution set of one proper 2-clause has normalized
spectral weights W_r/(|S|/N)=(3/4,1/6,1/12), which fail log-concavity.
For unrestricted cube subsets the even-parity set has normalized weights
half at r=0 and half at r=n, giving variance n²/4. Its direct representation
uses proper n-clauses, so this does not refute a fixed-small-k variance bound.

A primary-source orientation checked online is Michael Navon and Alex
Samorodnitsky, *Linear programming bounds for codes via a covering argument*,
arXiv:math/0702425, later Discrete & Computational Geometry 41(2) (2009),
199-207, DOI 10.1007/s00454-008-9128-0. The inspected ten-page author manuscript
has the Hamming/Fourier viewpoint in its Introduction, pp. 1-2, and Fourier
preliminaries in Section 2.1. No SAT theorem is attributed to this paper.
[Primary manuscript](https://people.csail.mit.edu/dmoshkov/courses/codes/lec8-LP-bound.pdf)
and [arXiv record](https://arxiv.org/abs/math/0702425).

For one new k-clause, assignments at distance d survive simultaneously with
probability

    a_d = 1 - 2^(1-k) + 2^(-k) binom(n-d,k)/binom(n,k).

Both assignments falsify the clause exactly when all its variables lie in
their agreement coordinates and the signs match the unique false pattern.
Thus for Z_m=|S_m|,

    E Z_m² = N sum_d binom(n,d) a_d^m.

This is the elementary unweighted second-moment route in geometric notation.
First moments alone give an upper bound on SAT probability, not a matching
lower bound. Spectral positivity alone does not control the second moment
at the satisfiability threshold.

## A literal discrete Crofton identity

Let I be a uniform r-subset of coordinates, b uniform in {0,1}^I, and
H={x:x_I=b}, a uniform codimension-r coordinate face. Then exactly

    P(S intersect H nonempty)
      = sum_{|I|=r}|projection_I(S)| / [2^r binom(n,r)].

For fixed I, the right numerator counts precisely the b admitting an
extension in S. The identity includes r=0,n and empty S. It provides a
natural random-restriction statistic: the fraction of partial assignments
extendable to a solution. However, projections do not preserve intersection
(already {00} and {01} have intersecting first-coordinate projections but
empty intersection). Therefore projection counts do not acquire the simple
intersection product rule of the face counts. Computing them is a projected
solution-counting problem, not a free polynomial-time geometric calculation.

The coordinator separately found the exact forced-variable hazard in S001,
equation (2.5), p. 5. It should be cited there, not presented as a new discovery.

## First unresolved step and a useful next investigation

The exact finite identities above are complete elementary derivations.
The first unresolved step toward a transferred phase-transition proof is
an invariant or distribution with BOTH (i) a valid relation to the SAT
nonemptiness event and (ii) a sufficiently strong variance/tilted-variance
bound for this random-clause model. Neither the face vector nor its Euler
characteristic supplies (i); the overlap/Fourier approach exposes precisely
the missing correlation estimate in (ii).

A useful limited investigation is to compare, at small exhaustively solvable
n, the face profile, projection profile, overlap profile, forced-variable
count, and SAT status across the transition. This would test candidate
inequalities and expose counterexamples; it would not prove a scaling law.
Record such exploratory work separately if authorized and run. No solver
benchmark or large experiment was performed by this subagent.
