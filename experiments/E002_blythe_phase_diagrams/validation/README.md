# E002 local validation

**Date:** 2026-10-11. These checks validate software behavior on the local
Apple M3/macOS environment. They are not Blythe benchmarks, measurements of
a phase transition, or proofs of concentration.

## Follow-up: explicit batch workflow and collection

The E002 and Git/uv guides now separate login-node preparation/submission from
compute-node work. The new [plotting batch script](../slurm/plot_results.sbatch)
also keeps artifact hashing and plotting inside SLURM. The existing solver
array, numerical implementation, configurations and recorded results are
unchanged.

The updated shell integration checks passed with mocked scheduler commands;
see [the batch check record](../slurm/local_checks_batch_2026-10-11.json).
They cover the plotting script's SLURM requirement, spooled-script location,
paths containing spaces, partial-result flag, output preservation, stale
environment rejection and propagation of collector failures. An independent
read-only review by `slurm_workflow_review` found no required correction to
the worker or submission instructions. These checks made no real SLURM,
solver or uv calls; compute-node execution remains untested here.

## Follow-up: root uv project

The later [POSIX checker follow-up](posix-checker-2026-10-11/README.md) records
the user's successful Blythe login-node setup and a compiler-warning fix,
with separate local build/preflight checks. It does not establish a completed
Blythe compute-node run.

The [uv validation record](uv-setup-2026-10-11/README.md) checks the subsequent
root `pyproject.toml`/`uv.lock` workflow: locked sync and checker setup, the
23-test suite, certificate preflight, a fresh 24-formula exact smoke check,
plot generation and the real helper in dry-run mode all passed locally.
The original records below remain unchanged evidence of the earlier pip-based
delivery. Current setup instructions are in the [uv guide](../../../docs/blythe-uv.md).

## Checks completed

- `python3 -m unittest discover -s code/tests -v`: **23 tests passed**.
  [Log](unit-tests.log). Includes exact decimal rounding, proper clauses and
  stable seeds, truth-table witness checks, overwrite/tamper protection,
  timeout/interruption handling, duplicate/conflicting attempts, missing or
  changed certificates, partial grids and unresolved-sample bounds.
- `python3 experiments/E002_blythe_phase_diagrams/slurm/check_scripts.py`:
  shell syntax and mocked submission tests passed. Paths containing spaces,
  resource limits, explicit module selection, dry-run behavior, accounts,
  retries and SLURM's copied batch-script path are covered. These mocks make
  no scheduler calls. Agent records are in [../slurm/](../slurm/).
- [preflight-final.json](preflight-final.json): Glucose 4.2 produced a checked
  SAT witness and a DRAT-trim-verified UNSAT proof. The negative control
  completed with an explicit rejection. Checker crashes/timeouts do not count
  as successful rejection. Source, solver-extension and binary hashes, package
  versions and checker logs are retained.
- [smoke002](smoke002/): final runner processed **24** seeded formulas with
  n=6 or 8, using two workers, producing **19 checked SAT** and **5 checked
  UNSAT** results. All exact classifications agree with independent truth-table
  enumeration by [verify_smoke.py](verify_smoke.py), as recorded in
  [exact-smoke-check.json](exact-smoke-check.json).
- Re-running smoke002 chunk 0 skipped all 12 completed instances; no earlier
  attempt was replaced. Its additional chunk provenance remains in the run.
- The plotter generated CSV/JSON and three PNG/PDF figure pairs from smoke002.
  These explicitly display `local-smoke-not-threshold-data`.
  The final [analysis-v2 plots](smoke002/analysis-v2/) were visually inspected
  for readable labels, bounds and legends. The earlier analysis-v1 output had
  footer overlap; it is preserved and superseded by the corrected layout.
- [runner_review.md](runner_review.md) records a separate agent's scoped
  read-only review of the final runner. This is internal software review,
  not external refereeing or formal verification.

## Preserved preliminary checks

[local-preflight.json](local-preflight.json) is the **failed** CaDiCaL195
preflight: PySAT returned an empty proof on the selected UNSAT test, and
DRAT-trim correctly did not verify it. It is not a completed positive check.
The source hash and environment are recorded, but this transient first script
version was not separately frozen. This finding motivated the Glucose42
interface used for E002; it says nothing about CaDiCaL's general proof capability.

[local-preflight-glucose42.json](local-preflight-glucose42.json) is an earlier
positive Glucose check. The final version additionally requires an explicit
negative-control rejection. [smoke001](smoke001/) retains the earlier 24-case
run and its frozen source before that preflight refinement. These records are
preserved; the delivery validation uses smoke002 and preflight-final.

## Reproduce in fresh destinations

The commands below reproduce the historical local validation on a workstation,
not a Blythe login node. On Blythe use the
[batch workflow](../README.md#run-on-blythe-through-non-interactive-slurm-jobs),
selecting `configs/smoke.json` for a small software check. From the project root,
with the pinned requirements available:

```sh
cc -std=c99 -O2 code/vendor/drat-trim/drat-trim.c -o /tmp/ksat-drat-trim
python code/ksat_experiments.py preflight \
  --drat-trim /tmp/ksat-drat-trim --output /tmp/ksat-preflight-new.json
python code/ksat_experiments.py plan \
  --config experiments/E002_blythe_phase_diagrams/configs/smoke.json \
  --output /tmp/ksat-smoke-new
python code/ksat_experiments.py run --run-dir /tmp/ksat-smoke-new \
  --chunk-id 0 --workers 2 --drat-trim /tmp/ksat-drat-trim
python code/ksat_experiments.py run --run-dir /tmp/ksat-smoke-new \
  --chunk-id 1 --workers 2 --drat-trim /tmp/ksat-drat-trim
python experiments/E002_blythe_phase_diagrams/validation/verify_smoke.py \
  --run-dir /tmp/ksat-smoke-new --output /tmp/ksat-truth-table-check-new.json
python code/plot_ksat_phase.py --run-dir /tmp/ksat-smoke-new \
  --output /tmp/ksat-smoke-new/analysis-v1
```

The actual local solver and plot commands used `uv run --cache-dir
/tmp/ksat-uv-cache --with python-sat==1.9.dev15 ...` and the equivalent
`--with matplotlib==3.10.8`, respectively. Final cluster setup instead creates
the dedicated environment described in the main README. Linux address-space
limits, the real module stack, shared filesystem behavior and scheduler
execution have not been tested on Blythe; the pilot is the next check.
