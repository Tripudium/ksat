# Phase-diagram result schema and interpretation

The collector reads a **schema-version 1** `manifest.json` and retained runner
records under `attempts/INSTANCE_ID/ATTEMPT_ID/result.json`. A completed
`result.json` is the attempt-completion marker. Work directories without this
file remain pending. These instructions describe planned outputs; they are not
evidence that a cluster experiment has run.

## Collect and render

From the repository root, in the pinned Python environment:

```sh
python code/plot_ksat_phase.py --run-dir /path/to/run --output /path/to/new-plots
python code/plot_ksat_phase.py --run-dir /path/to/run --output /path/to/new-partial-plots --allow-partial
```

The output directory must not exist. Use a new directory for each collection;
the collector never edits retained attempts. Without `--allow-partial`, every
planned instance needs a completed attempt. An unresolved completed attempt
(including a timeout) is permitted, and remains unresolved in the plots.
`--allow-partial` retains missing results as `pending`, with their planned
replicates included in all denominators.

## Validation and repeated attempts

Every attempt is checked against the manifest's exact file SHA-256 and copied
identity fields: `id`, `n`, `k`, `m`, `alpha_requested`, `alpha_actual`,
`replicate`, `seed`, and `chunk_id`. The attempt ID must match its directory.
Every supplied `input`, `witness` or `proof` artifact path must remain within
the run directory, exist, and match its corresponding SHA-256. Verified SAT
requires retained input and witness artifacts; verified UNSAT requires retained
input and proof artifacts. Malformed records, identity/hash
mismatches, inconsistent input hashes, or conflicting verified SAT/UNSAT
outcomes classify the **instance** as `error`; they are never silently dropped.
Diagnostics appear in `instances.csv` and `summary.json`.

Otherwise the earliest verified outcome is selected, ordered by timezone-aware
`started_utc` and then `attempt_id`. If none is verified, the latest completed
attempt is selected. Repeated attempts are one formula instance, not additional
independent replicates. A later timeout does not erase an earlier verified
outcome. Verification labels are runner records: the collector does not rerun
the SAT witness or UNSAT proof checker.

The manifest must describe a complete configured grid, with unique IDs and
cell/replicate pairs. Requested densities mapping to the same integer clause
count at a given n are rejected. Results for unplanned IDs stop collection.

## Cell summaries and uncertainty

`summary.csv` contains one row per **(n, k, m)**, with requested alpha, actual
`m/n`, planned repetitions R, and separate counts:

- `sat_verified`, `unsat_verified`: accepted decision outcomes;
- `unsat_unchecked`, `unknown`, `error`, `pending`: unresolved outcomes;
- `unresolved` and `unresolved_fraction`: their sum and fraction of R.

Every planned replicate stays in R. If S and U denote verified SAT and UNSAT
counts, the observed sample's SAT fraction lies in

```text
p_lower = S/R
p_upper = 1 - U/R
```

`p_estimate` is populated **only when all R outcomes are verified**; otherwise
it is JSON `null` and an empty CSV field. In particular, the collector never
uses S/(S+U) to conceal timeouts or unchecked decisions.

Sample censoring is distinct from random-sampling uncertainty. With independent
formula replicates from the stated ensemble, the **95% pointwise** Hoeffding
envelope is

```text
epsilon = sqrt(log(40)/(2R))
confidence_lower_95 = max(0, p_lower - epsilon)
confidence_upper_95 = min(1, p_upper + epsilon)
```

This conservative envelope contains the full-observation Hoeffding interval
for any resolution of the unresolved outcomes. It is not a simultaneous 95%
band over all cells, and narrow bounds are not guaranteed at small R.

## Files and figures

- `summary.csv`: cell counts, bounds, confidence envelope and complete flag.
- `instances.csv`: one selected outcome per planned instance, attempt count,
  input hash and audit diagnostics.
- `summary.json`: the same data, configuration, exact manifest hash, assumptions,
  collector hash, Python/Matplotlib versions and output inventory.
- `phase_bounds.png` and `.pdf`: SAT lower bound, SAT upper bound and unresolved
  fraction. Every planned cell is displayed.
- `phase_complete_estimates.png` and `.pdf`: produced if any cell is completely
  resolved. Unresolved cells are gray. Optional 5%, 50% and 95% contours use only
  grid squares with all four corners resolved and with data spanning that level.
- `finite_size_curves.png` and `.pdf`: actual-density curves; markers are fully
  resolved estimates, dashed bounds/darker fill show sample censoring, and the
  pale envelope shows pointwise sampling uncertainty.

Heatmap axes are discrete **requested-density** and n grid cells; their spacing
is categorical, not proportional to physical distances. Curves use the actual
numerical density m/n. Connecting lines and empirical contours interpolate
between measured grid points; no monotonic constraint, smoothing, scaling law
or asymptotic threshold is fitted. A contour can be absent because the grid,
resolution status or probability range does not support it.

Every plot displays `config.name` in its footer, including local smoke-run labels.
An explicitly marked `synthetic_fixture` manifest additionally labels plot titles
as software-test fixtures. Neither synthetic tests nor local smoke runs should be
presented as adequately sampled threshold measurements.

These are finite-size satisfiability diagrams, not algorithm-success diagrams:
an incomplete solver's failure remains unknown. Publish the bounds and unresolved
fraction alongside any estimate plot. Keep raw runs, manifest and provenance
with exported figures. Artifact hashes are streamed, so collection also reads
the retained proof files; allow time and storage throughput for large proofs.
If rendering fails after output creation, keep that
partial output for diagnosis and rerun into a new directory.

## Checks

```sh
python -m unittest discover -s code/tests -p 'test_plot_ksat_phase.py'
```

Fixtures are explicitly synthetic collector tests. They exercise censored
denominators, pending results, repeat attempts, conflicting verified outcomes,
invalid identities/manifests and overwrite refusal. They are not empirical
random-k-SAT data and must not be incorporated into threshold figures.
