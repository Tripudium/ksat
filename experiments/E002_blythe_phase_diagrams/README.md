# E002: Blythe random k-SAT phase diagrams

**State:** workflow prepared and locally validated; cluster campaign **not run**.
**Blythe setup update:** the user reports successful login02 setup on
2026-10-11. A compiler feature-selection warning was addressed in the helper;
see the [POSIX follow-up](validation/posix-checker-2026-10-11/README.md).
Compute-node preflight and the scientific pilot remain unrun by this project.
**Date:** 2026-10-11. **Question:** estimate finite-size SAT probabilities as a
function of variable count and clause density, with visible computational and
sampling uncertainty. This is an empirical study, not a concentration proof.

The [Blythe scripts](slurm/README.md) follow the supplied
[documentation](blythe_documentation.md). The reusable
[runner](../../code/ksat_experiments.py) and
[plotter](../../code/plot_ksat_phase.py) preserve raw evidence and generate
CSV/JSON summaries plus vector PDF and PNG diagrams.

## Prepared batches

| Configuration | Sizes n | Requested densities | Repetitions/cell | Instances |
| --- | --- | --- | ---: | ---: |
| [pilot-3sat.json](configs/pilot-3sat.json) | 50, 100, 150, 200, 250 | 3.50, 4.00, 4.20, 4.30, 4.50, 5.00 | 20 | 600 |
| [grid-3sat.json](configs/grid-3sat.json) | 50, 75, 100, 125, 150, 175, 200, 250 | 3.50–5.00 in steps of 0.05 | 100 | 24,800 |
| [control-2sat.json](configs/control-2sat.json) | 100, 200, 400, 800 | 0.50–1.50 in steps of 0.05 | 100 | 8,400 |
| [smoke.json](configs/smoke.json) | 6, 8 | 0, 1, 4, 8 | 3 | 24 |

Run the pilot first. Include n=250 in the full grid only if the pilot supports
it; edit a copied configuration before planning. Production configurations
use distinct base seeds, so pilot observations are not reused as fresh samples.
Each row is a separate plan; batches are not submitted automatically.
The smoke configuration tests software and certificate handling only.

The 3-SAT defaults allow 30 seconds for the solver process and a further
30 seconds for proof checking. The 2-SAT control uses 10 + 10 seconds. Process
budgets include interpreter startup and serialization. Each process has a
1536 MiB address-space limit on Linux. The scheduler requests 2048 MB per CPU
to leave headroom for supervision; wall-clock limits also bound stalled runs.
Chunks contain at most 128 instances. At 16 workers, the 3-SAT capped work
is about eight minutes per full chunk, plus generation/storage and preflight;
the job requests 45 minutes. These are caps and planning choices, not timings.

## Setup, plan, submit, plot

Clone the project into your actual Blythe `/springbrook/share/<group>/...`
share; see the [Git and uv guide](../../docs/blythe-uv.md). From that repository
root, make uv and a C compiler available. Setup uses `uv sync --locked` with
the root lockfile and Python 3.12 selection, then builds the pinned checker.
uv can provision Python, so a Python module is optional. If site modules are
needed, set `KSAT_MODULES` as described in [slurm/README.md](slurm/README.md).
No module name is invented from the incomplete supplied examples:

```sh
bash experiments/E002_blythe_phase_diagrams/slurm/setup_environment.sh

export KSAT_RUN_DIR="$PWD/cluster-runs/3sat-pilot-001"
.venv/bin/python code/ksat_experiments.py plan \
  --config experiments/E002_blythe_phase_diagrams/configs/pilot-3sat.json \
  --output "$KSAT_RUN_DIR"

# Print the complete sbatch command without submitting.
bash experiments/E002_blythe_phase_diagrams/slurm/submit_array.sh "$KSAT_RUN_DIR"

# Submit on Blythe when ready to run the prepared batch.
bash experiments/E002_blythe_phase_diagrams/slurm/submit_array.sh \
  "$KSAT_RUN_DIR" --submit

# After jobs finish; choose a new analysis directory for each collection.
.venv/bin/python code/plot_ksat_phase.py \
  --run-dir "$KSAT_RUN_DIR" --output "$KSAT_RUN_DIR/analysis-v1"
```

These commands use the default `.venv`. If you override `KSAT_ENV_DIR`, use its
`bin/python` instead. Setup records project/lock hashes, Python, packages,
modules and checker provenance. Submission and workers validate that record;
compute jobs perform no dependency sync or installation. Rerun setup after
pulling dependency changes, and keep active jobs' checkout/environment fixed.
The guard binds the environment to the current checkout; a run manifest pins
runner code but does not pin the dependency lock. Start a fresh plan after
dependency changes to keep campaign timings comparable. An old plan can
otherwise resume under a new recorded environment.

Defaults are the `compute` partition, one node and 16 CPUs per array task,
at most four concurrent tasks (64 CPUs). An actual account can be supplied
with `--account`; none is assumed. Job IDs are printed by `sbatch --parsable`.
Use normal site tools such as `squeue -u "$USER"` and `sacct -j JOB_ID` to
inspect state; there is no polling loop or automatic resubmission.

Plotting may run locally after copying the complete run directory. Add
`--allow-partial` to include missing jobs as unresolved entries. A retry of the
same submission skips completed outcomes; `--retry-unknown` also retries
unresolved completed attempts. Every earlier attempt remains intact. Correct
systematic errors before retrying; an invalid retained certificate or conflicting
outcomes requires investigation rather than silent replacement. Changing the
runner or cutoff requires a fresh plan, which preserves the earlier run.

## Model, solver and certificates

Each formula has n available variables and m=floor(alpha*n) independent proper
k-clauses: k distinct uniformly sampled variables, independent fair signs,
and possible repetitions of whole clauses. The decimal floor uses exact integer
arithmetic. Densities that collapse to the same integer m at a given n are
rejected. Generation uses a versioned SHA-256 counter stream with rejection
sampling and a partial Fisher–Yates sampler. Seeds derive from base seed, k,
n, m and replicate; generation is invariant to scheduling and Python's sampling
implementation. Saved DIMACS files are the definitive inputs. Pseudorandom
sampling is an implementation of the ensemble, not a proof of true randomness.

The default solver is **Glucose 4.2 through PySAT 1.9.dev15**, with proof logging.
SAT requires an exactly checked, retained assignment. UNSAT requires a retained
DRAT proof and an explicit successful verdict from the separately compiled
[DRAT-trim](../../code/vendor/drat-trim/SOURCE.json) checker. A cutoff, failure,
or unchecked UNSAT remains unresolved. The checker and runtime are trusted
software components; this is not formal verification of a general theorem.

A positive and negative certificate preflight runs in each allocated task.
Local testing found that the pinned PySAT/CaDiCaL interface returned an empty
proof on the chosen UNSAT test, so E002 uses the tested Glucose interface.
The failed preflight is retained. E001's CaDiCaL timings do not calibrate
Glucose with proof generation/checking. No GPU acceleration is assumed.

## Recorded results and plots

See [RESULTS.md](RESULTS.md) for the schema. Each plan records the exact grid,
seeds, source hash and a runner snapshot. Each chunk records Python/package
versions, solver-extension/checker hashes, hardware and SLURM metadata. Each
attempt retains the input/hash, logs, solver statistics, timings, witness or
proof, certificate result and final status. Partial attempts retain a start
record. Atomic publication and instance locks prevent competing writes;
historical records are never overwritten.

Plots include SAT-fraction lower/upper bounds, unresolved fractions,
complete-cell estimates with empirical 5/50/95% contours, and finite-size
curves. Every planned replicate remains in the denominator. With S checked
SAT and U checked UNSAT among R planned instances, the observed sample SAT
fraction lies in [S/R, 1-U/R]. Population sampling uncertainty is separately
shown using a conservative 95% pointwise Hoeffding envelope. These are not
simultaneous confidence bands over the entire image. There is no fit imposing
monotonicity or an assumed scaling exponent. Each grid cell samples independent
formulas; this workflow does not measure coupled-path T_n samples or their
empirical variance.

Keep grid/cutoff choices fixed for the final run and use fresh seeds after
pilot-based refinement. Curves and numerical fits are not mathematical proofs.
Timeout patterns depend on the solver and resources as well as the ensemble.

## Reproduction, storage and validation

Keep the Git revision, `uv.lock`, dated setup record and environment/source
hashes in each run. The old `requirements.txt` describes the initial pip
delivery; the root uv files now govern setup. Never edit an active plan.
To reproduce with changed code,
make a new plan with the same configuration and compare the saved CNF hashes.
Runner source changes are rejected against an existing plan.

Retaining inputs, certificates and logs creates many files: roughly 150,000–
225,000 for the full 24,800-instance grid before retries, with proof sizes
depending strongly on the instance. Measure bytes and filesystem load in the
600-instance pilot before scaling. Archive completed run directories for
transfer and backup; the scripts deliberately perform no cleanup or deletion.
The supplied shared-filesystem documentation provides no backup guarantee.

[Validation records](validation/README.md) distinguish software tests and exact
small-instance checks from scientific measurements. No real Blythe submission,
target-node benchmark, GPU run, or full phase diagram has been performed.
