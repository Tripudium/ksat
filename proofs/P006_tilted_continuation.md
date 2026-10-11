# P006: tilted continuation and a conditional right-tail criterion

- **State:** `internally-reviewed` at the frozen source below.
- **Created / updated:** 2026-10-11, version 1.
- **Author:** coordinator (`root`).
- **Canonical source:** [P006_tilted_continuation.tex](P006_tilted_continuation.tex).
- **Frozen SHA-256:** `333a6efa6397d068fe1f93768fc6b9a68f015d08958acf30228275c062b04a79`.
- **Related attempt:** [A001](../attempts/A001_discrete_geometry/README.md).

## Exact statement and scope

For every n >= k >= 2 and real theta < -log(1-2^-k), the finite solution-set
process has an explicit normalized tilted continuation kernel. The tilted
variance of its absorption time equals the expected sum of one-step variances
of tilted remaining means along the absorbed path. The empty starting state
has lifetime zero and is included explicitly.

A separate conditional corollary for k >= 3 shows that the additional
positive-tilt occupation estimate (H+) would imply a right-tail sub-gamma
inequality and a confidence-dependent upper-quantile bound. It supplies no
proof of (H+), no lower tail and no location of the mean.

## Dependencies and sources

The tail argument of P004 extends directly to every fixed solution set;
the extension is proved here. Other steps use conditioning, finite telescoping,
dominated differentiation and monotone convergence. S001 equation (2.4), p. 5,
already states the untilted drift; no novelty claim is made for it or for
standard Markov tilting. P005 is used only in the closing scope remark.

## Remaining gap and checks

The identities and conditional implication have complete written proofs.
The first unproved concentration step is precisely (H+), an added assumption
of the corollary rather than of the project model. No simulation or numerical
check is used as mathematical evidence.

## Review

Independent review by `analytic_transfer`, 2026-10-11, who did not author
this fragment: [review record](P006_review_2026-10-11.md). The full frozen
source passed the stated checks with no gap found. The review does not
establish (H+). No external refereeing or formal verification is claimed.
