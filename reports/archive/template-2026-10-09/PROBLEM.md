# Research problem: [project title]

**State:** unconfigured template; no mathematical target has been selected.
**Last substantive revision:** [YYYY-MM-DD when this project is initialized].

This file is authoritative about the target and its scope. Progress and next
actions belong in [STATUS.md](STATUS.md); working hypotheses belong in the
[attempt registry](attempts/README.md) until explicitly adopted here.

## 1. Primary objective

[State the mathematical question in plain language and then precisely. Give the
desired theorem, construction, classification, bound, or counterexample, with
all quantifiers. Say what would settle the question in either direction.]

- **Objects and ambient setting:** [spaces, structures, fields, categories, etc.]
- **Inputs and parameters:** [domains, dimensions, parameter ranges].
- **Target statement:** [a precise quantified assertion].
- **Success criterion:** [the exact deliverable that establishes the target].
- **Acceptable intermediate progress:** [useful partial results, explicitly
  distinguished from a solution of the primary problem].

## 2. Definitions, notation, and assumptions

| Item | Definition or convention | Why it matters |
| --- | --- | --- |
| [symbol/object] | [precise definition] | [where it is used] |
| [hypothesis] | [exact condition and range] | [scope it restricts] |

Specify, where relevant: base field and characteristic; topology and regularity;
normalization; exact versus approximate computation; norms and error tolerances;
cost model; uniformity; dependence of constants; probability space; and the
order of limits and quantifiers. Address degenerate and boundary cases.

## 3. Scope and related formulations

- **Primary setting:** [the full class covered by the target].
- **Restricted or conditional settings:** [useful variants and their extra
  hypotheses; do not silently substitute them for the primary setting].
- **Required transfers:** [reductions or equivalences that need proofs before
  results in one setting can resolve another].
- **Secondary objectives:** [optional related questions].
- **Out of scope:** [deliberate exclusions].

## 4. Starting literature and reference material

Start with the relevant papers supplied in [papers/](papers/README.md) and the
material catalogued in [references/](references/README.md). Read the sources
needed for an argument; do not rely solely on abstracts, filenames, remembered
statements, or summaries. Record source IDs and exact theorem/lemma/page
locations, translate the notation, and check every hypothesis against this
project's setting. Distinguish published results, preprints, informal notes,
and unchecked assertions. Note version/date and any known corrections.

| Source ID | Relevant result and exact location | Applicability or mismatch |
| --- | --- | --- |
| [Snnn] | [fill after reading the source] | [checked hypotheses / open issue] |

No starting source has been selected. This row is a form, not a literature claim.
Add missing literature when needed; record what was checked and what remains
unavailable. Keep verified citation metadata in `reports/references.bib`.

## 5. Evidence and proof standards

**Numerical experiments are not treated as proofs.** Plots, floating-point
agreement, random tests, finite searches, asymptotic fits, and computer algebra
output are evidence about the cases checked, not proofs of universal statements.
Failure to find a counterexample is not a proof of nonexistence. A suspected
numerical counterexample needs an exact or rigorously certified verification.

A computer-assisted proof must separately justify its reduction to a finite or
certified task, exhaustive coverage, arithmetic/error bounds, and the checker or
certificate. Keep exploratory code and proof-bearing certificates distinct.
Neither an exact finite computation nor symbolic simplification alone proves an
unrestricted theorem.

Every proved statement must specify its hypotheses, conclusion, dependencies,
and complete argument. Label conjectures, heuristics, conditional results, and
unresolved steps explicitly. Independent internal review, formal verification,
external refereeing, and verification of a cited source are different activities.
Do not assert novelty or a problem's current open status without appropriate
literature checking and a stated scope/date for that checking.

## 6. Completion and revision criteria

[Specify what must be proved, written up, checked, and delivered for this project
to be complete. Set milestones without presupposing that the main target is true.]

Record substantive changes to the target, explain why they were made, and state
their effect on existing claims. A refuted auxiliary lemma does not by itself
refute the primary conjecture. A restricted theorem does not resolve a broader
target without the missing transfer.

| Date | Change | Reason and effect on claims |
| --- | --- | --- |
| [YYYY-MM-DD] | [initial specification or revision] | [explanation] |
