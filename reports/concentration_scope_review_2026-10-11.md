# Concentration report: scoped consistency review

- **Reviewer:** `discrete_kinematics` agent.
- **Date:** 2026-10-11.
- **Reviewed report:** `reports/concentration-2026-10-11.tex`.
- **Reviewed report SHA-256:** `ce3b969e55c8b333a8cf4f61ac2ce5dd42ed8ce0bfe6ecb3e49611dbad4a2777`.
- **P005 source:** `77d70d65ea2b2330ee3ab786731ecfbda4842dfe49de24e1eff638b6951f386a`.
- **P006 source:** `333a6efa6397d068fe1f93768fc6b9a68f015d08958acf30228275c062b04a79`.
- **Verdict:** the report's mathematical summary, method comparisons, claim
  states and limitations are consistent with these canonical fragments and
  their recorded independent reviews. No substantive overclaim found.

## Scope checked

The report preserves the original independent proper-clause model and exact
failed two-sided target. The mean lower bound, rare-prefix event probability,
fixed-negative-tilt contradiction, shrinking tilt A log(n)/n, and tilted
variance of at least order n^2/log(n) match P005. The tilted-variance statement
is correctly an existence statement about an n-dependent negative tilt.

The compatibility discussion expressly restricts potential linear untilted
variance and square-root fixed-confidence windows to k>=3. It separately
identifies the k=2 clause-window scale n^(2/3). No ordinary-variance theorem,
location of the mean, or positive-tail concentration theorem is deduced from
the rare-core obstruction.

P006 is consistently described as exact tilted-kernel and variance-occupation
identities with a conditional concentration implication. Hypothesis (H+)
remains unproved; no independence under the tilted law, efficient computation
of the state function, lower-tail bound or center location is asserted.

The source-audit summary agrees with the separate dated audit record's stated
scope: manually checked portions and manuscript claims are distinguished from
unverified external dependencies, appendices and formal artifacts. This report
review did not repeat that external literature audit or P006's full proof.
P005 was separately fully reviewed by this reviewer at the hash above.

## Minor clarity suggestion

The last paragraph accurately says E002 generates independent fixed-density
formulas rather than coupled paths. For clarity, it can additionally state
that its SAT probabilities nevertheless estimate the marginal survival
function Pr(T_n>m); what it does not record is individual hitting-time samples
or coupled clause paths. This is an expository refinement, not a mathematical
gap. The coordinator was notified before final layout/export.

This is a source-text consistency review, not visual PDF QA, external refereeing,
formal verification or a new proof. The hash identifies the checked snapshot;
subsequent layout-only edits or the suggested final-paragraph clarification
should be recorded separately and do not imply an unperformed re-review.

## Final source recheck, 2026-10-11

- **Final report SHA-256:** `88ee157dd9866f8bd140e58a8fc066f89047fcb23585e9ced4a6f78fe6a7cd9d`.
- **Canonical sources:** P005 and P006 retain the hashes recorded above.
- **Verdict:** the scoped consistency verdict extends to this final source.

The final E002 paragraph correctly states that independent fixed-density SAT
probabilities estimate the marginal survival function Pr(T_n>m), while the
workflow does not record coupled clause paths or individual hitting-time
samples. The source comparison now attributes explicit averaging of rare
collision environments only to S032 and S033, consistently with the separate
source audit. The distinctions between the k>=3 variance/window discussion,
the k=2 control case, the shrinking negative tilt and the unproved hypothesis
(H+) remain intact. Replacing three page-break directives with vertical space
does not change the mathematical content.

This append-only recheck preserves the initial snapshot verdict. It is limited
to source-text consistency; visual PDF QA and the independent proof/source
reviews remain separately recorded.

### Final bibliography layout snapshot

The subsequent final report source has SHA-256
`86d441debac2d3115f4c9ad304d9ee1ed146a562472ee7eb8864df44c483751d`.
The bibliography page break was restored; the two proof-section spacing
changes and both prose clarifications checked above remain present. P005 and
P006 hashes are unchanged. This presentation adjustment does not alter the
scoped verdict. This reviewer checked the source and hashes, not the rendered
pagination; the coordinator records the final build and visual inspection.
