# P003: cubical intersection identities and transfer obstructions

- **State:** `internally-reviewed`.
- **Version:** 2026-10-11, v2 (first canonical publication).
- **Canonical source:** [P003_discrete_kinematics.tex](P003_discrete_kinematics.tex).
- **Author:** `discrete_kinematics` agent.
- **Independent internal reviewer:** `analytic_transfer` agent.
- **Reviewed SHA-256:** `bf060fc4240e2ea0a4b8bf45d0255e8e31c240f1e54fe62ba07ec0ef9cb0da28`.
- **Review:** [scoped review](P003_review_2026-10-11.md).
- **Related attempt:** [A001](../attempts/A001_discrete_geometry/README.md).

## Exact scope

For all n >= 1 and all subsets S,U of the Boolean cube, uniform signed
coordinate permutations give the exact face-count and Euler-characteristic
intersection identities. Projection counts give the exact probability of
meeting a uniformly random coordinate face; ordered Hamming-distance pair
counts give the exact second moment of intersection size and its elementary
nonemptiness lower bound. For n >= k >= 2, expected cubical face counts under
the independent proper-clause model are explicit, including m=0 separately.

Explicit proper-CNF examples show that Euler characteristic can vanish for
a nonempty solution set, equal face vectors can give different intersection
probabilities, and both raw and normalized face counts can fail log-concavity.
These are elementary finite identities and obstructions, with no novelty
claim. They do not disprove a typical-instance or different-invariant approach.

## Dependencies, review and remaining gap

Proofs use transitivity of the finite cube group, finite counting, clause
independence where stated, and Cauchy-Schwarz. They do not depend on a new
external theorem or experiment. The reviewer checked every statement,
normalization, empty case and boundary case in the frozen source, including
the 5/12 versus 1/2 counterexample. No gap was identified in this scope.
This is internal review, not external refereeing or formal verification.

The first missing step for A001 is a SAT-relevant discrete profile together
with a usable concentration/correlation bound near the random threshold.
The present identities alone do not supply a phase-transition theorem.

## History

The working v1 source and its review are retained in
[archive/P003_working_v1](archive/P003_working_v1/). Version 2 adds proved
projection and ordered-distance identities. A wording issue in the
ordered-pair transitivity proof was corrected before its final review.
The canonical source is a byte-identical copy of the reviewed v2.
