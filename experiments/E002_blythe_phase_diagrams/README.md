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

## Run on Blythe through non-interactive SLURM jobs

**Run experiments and result collection as SLURM batch jobs.** The login node
is used for environment setup, lightweight planning, submission and monitoring.
`bash submit_array.sh ... --submit` calls **`sbatch`**; it returns after queuing
the work. The solvers and certificate checks run on allocated compute nodes
through [run_array.sbatch](slurm/run_array.sbatch). Do not run that batch script
with `bash`, run the Python solver directly on the login node, or use an
interactive session for this campaign. Jobs continue after you disconnect.

| Step | Where it runs | Entry point |
| --- | --- | --- |
| Prepare dependencies and checker | Login node | `setup_environment.sh` |
| Write the seeded run manifest (no solving) | Login node | `ksat_experiments.py plan` |
| Queue the experiment array | Submit from login node; compute on allocated nodes | `submit_array.sh RUN_DIR --submit` |
| Audit results and produce plots | Submit from login node; compute on an allocated node | `sbatch ... plot_results.sbatch RUN_DIR OUTPUT_DIR` |

### 1. Prepare the environment and pilot plan

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
```

Use a fresh run directory. Planning writes the configuration, source snapshot
and instance metadata; it does not generate or solve the formulas. The pilot
contains 600 instances in five array tasks (at most 128 instances per task).

### 2. Submit the pilot with SLURM

```sh
# Print the complete sbatch command without submitting.
bash experiments/E002_blythe_phase_diagrams/slurm/submit_array.sh "$KSAT_RUN_DIR"

# Queue the non-interactive job array on Blythe.
bash experiments/E002_blythe_phase_diagrams/slurm/submit_array.sh \
  "$KSAT_RUN_DIR" --submit
```

Defaults are the `compute` partition, one node and 16 CPUs per array task,
2048 MB per CPU, 45 minutes per task, and at most four concurrent tasks
(64 CPUs). The helper derives the array range from the plan: the pilot uses
`--array=0-4%4`. It prints the command and then the job ID returned by SLURM.
Supply an actual account with `--account ACCOUNT` if your association requires
one. Resource options include `--cpus`, `--concurrency`, `--time` and
`--mem-per-cpu`; see the [script guide](slurm/README.md).

### 3. Monitor jobs and inspect logs

Replace `12345` below with the array job ID printed at submission:

```sh
KSAT_ARRAY_JOB_ID=12345
squeue -u "$USER"
sacct -j "$KSAT_ARRAY_JOB_ID" --format=JobID,State,ExitCode,Elapsed
```

Task logs are in `$KSAT_RUN_DIR/slurm-logs/<job>_<task>.out` and `.err`;
certificate-preflight JSON files are recorded there too. Check all task states
and logs before collecting results. A completed job can still contain timed-out
or unresolved formulas; the plots retain these outcomes. To cancel this array,
use `scancel "$KSAT_ARRAY_JOB_ID"`. There is no automatic resubmission.

### 4. Submit result collection and plotting as a batch job

After all array tasks have finished, submit this from the repository root:

```sh
mkdir -p "$KSAT_RUN_DIR/slurm-logs"
sbatch --parsable --export=ALL --chdir="$PWD" \
  --output="$KSAT_RUN_DIR/slurm-logs/plot-%j.out" \
  --error="$KSAT_RUN_DIR/slurm-logs/plot-%j.err" \
  experiments/E002_blythe_phase_diagrams/slurm/plot_results.sbatch \
  "$KSAT_RUN_DIR" "$KSAT_RUN_DIR/analysis-v1"
```

This serial job requests one CPU, 4096 MB and 30 minutes on `compute`.
If needed, add `--account=ACCOUNT` **before** the script path; the array
helper's `KSAT_ACCOUNT` setting is not automatically applied by plain `sbatch`.
The collector reads and hashes retained input/certificate files, so large
collections also belong on a compute node. It writes `summary.csv`,
`instances.csv`, `summary.json`, and PDF/PNG plots in `analysis-v1`.
Use a new output directory for every collection, including after a failed one.

If tasks failed or were interrupted, either retry first or append
`--allow-partial` **after** the two directory arguments to include missing
results as unresolved. To retry, repeat the array submission; completed
outcomes are skipped. Add `--retry-unknown` to request new attempts for
unresolved completed outcomes while retaining earlier attempts. Investigate
invalid certificates or conflicting outcomes before retrying. Alternatively,
copy the complete run directory to your own workstation and run the plotter
there; direct plotting is not the Blythe login-node workflow.

### 5. Scale up after reviewing the pilot

Check runtime, unresolved fractions, proof sizes and filesystem load first.
If the pilot supports the prepared full grid, create and submit a fresh plan:

```sh
export KSAT_RUN_DIR="$PWD/cluster-runs/3sat-grid-001"
.venv/bin/python code/ksat_experiments.py plan \
  --config experiments/E002_blythe_phase_diagrams/configs/grid-3sat.json \
  --output "$KSAT_RUN_DIR"
bash experiments/E002_blythe_phase_diagrams/slurm/submit_array.sh \
  "$KSAT_RUN_DIR" --submit
```

This grid has 194 array tasks. For the 66-task 2-SAT control, use
`experiments/E002_blythe_phase_diagrams/configs/control-2sat.json` and another
fresh run directory. Repeat steps 3–4 with the new run path. Reduce the grid
in a copied configuration if the pilot shows excessive costs.
The arrays process separate chunks; extra concurrency increases throughput
across formulas, not the speed of one SAT solve.

### Environment and reproducibility

These commands use the default `.venv`. If you override `KSAT_ENV_DIR`, use its
`bin/python` for planning instead. Setup records project/lock hashes, Python,
packages, modules and checker provenance. Submission and workers validate that
record; compute jobs perform no dependency sync or installation. Keep the same
exported `KSAT_MODULES` selection used for setup. Rerun setup after pulling
dependency changes, and keep active jobs' checkout/environment fixed.

The guard binds the environment to the current checkout; a run manifest pins
runner code but does not pin the dependency lock. Start a fresh plan after
dependency changes to keep campaign timings comparable. An old plan can
otherwise resume under a new recorded environment. Changing the runner or
cutoff also requires a fresh plan, preserving the earlier run.

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
