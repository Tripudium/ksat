# Blythe CPU batches

These scripts prepare one Python process pool per array task, with one CPU
worker per solver instance. Defaults: `compute`, one node, 16 CPUs, 2048 MB per
CPU, 45 minutes, and at most four array tasks at a time. They request no GPUs.
The defaults are planning choices; no Blythe timing measurement has been made.

The scripts have been prepared locally. They have **not** installed anything on
Blythe, connected to the cluster, or submitted a job.

## Set up in the project share

Copy the repository into your actual `/springbrook/share/<group>/...` project
directory and enter it. The scripts derive the project directory from their
location; set `KSAT_PROJECT_DIR` only if you need an explicit override. Use a
compute-visible absolute run directory in that share. Do not use a desktop mount
or assume `/scratch` exists on Blythe.

The supplied HTML does not name a CPU Python module. Find an available Python
3.10-or-newer module and compatible C compiler with `module avail` or site
support. Set `KSAT_MODULES` to the space-separated module names. Scripts run
`module purge` and reload exactly those names. Alternatively, after preparing
the module environment yourself, set `KSAT_USE_CURRENT_ENV=1` and leave
`KSAT_MODULES` unset; the submitted job then inherits that environment.

```sh
# Run from the uploaded repository, after selecting the site modules.
export KSAT_ENV_DIR="$PWD/.venv-ksat-blythe"
bash experiments/E002_blythe_phase_diagrams/slurm/setup_environment.sh
export KSAT_DRAT_TRIM="$KSAT_ENV_DIR/bin/drat-trim"
```

Setup creates the virtual environment, installs the pinned requirements, and
checks the vendored source hash before compiling the checker with
`cc -std=c99 -O2`. Set `CC` to an available
compiler executable if needed. It needs package-download access for pip once;
the vendored checker requires no Git/network access. A repeated setup updates
only that dedicated environment and writes a new dated provenance record.
Jobs never install packages. Setup and run scripts use the same Python modules.

## Plan and review the submission

Use the configuration supplied in the experiment's main README:

```sh
"$KSAT_ENV_DIR/bin/python" code/ksat_experiments.py plan \
  --config path/to/config.json --output /absolute/project/run-directory
bash experiments/E002_blythe_phase_diagrams/slurm/submit_array.sh \
  /absolute/project/run-directory
```

The submit helper reads `manifest.json`, derives the zero-based array range,
creates `slurm-logs/` before submission, and **prints the command by default**.
This does not run preflight or a solver on the login node. Add `--submit` when
you intend to submit the reviewed command:

```sh
bash experiments/E002_blythe_phase_diagrams/slurm/submit_array.sh \
  /absolute/project/run-directory --submit
```

No account name is assumed. If your site/account association needs one, use
`--account YOUR_ACTUAL_ACCOUNT` or set `KSAT_ACCOUNT`. The supplied documents
do not prescribe a universal account argument.

Use `--cpus`, `--concurrency`, `--time HH:MM:SS`, and `--mem-per-cpu` to adjust
resources. Respect the measured workload and your allocation. Saved site limits
are 168 CPUs/node, 4591 MB/CPU and 48 hours/job; the script checks these limits.
A conservative chunk-time estimate is
`ceil(instances_in_chunk / workers) * (solve_cutoff + check_cutoff + overhead)`.
Keep it comfortably below the requested wall limit. Startup, proof serialization
and storage can matter, so inspect the initial jobs before scaling.

## Runtime and retries

The worker script takes the absolute run path as an argument and uses the
exported project path, falling back to `SLURM_SUBMIT_DIR`. It does not derive
paths from SLURM's copied batch-script location. Each task first runs proof-checker
preflight inside its allocation and saves an independently named JSON record.
It then launches the chunk with `--workers "$SLURM_CPUS_PER_TASK"` under `srun`.
BLAS/OpenMP thread counts are one to avoid oversubscribing the process pool.

SLURM stdout and stderr are `slurm-logs/<array-job>_<task>.out` and `.err`.
The pipeline's per-instance records, certificates and unknown outcomes remain
in the run directory. Restarting a chunk skips completed results by default;
`--retry-unknown` requests new attempts for unknown outcomes while retaining
previous attempts. SLURM-killed or failed tasks are not silently treated as
UNSAT or as completed measurements. Use the pipeline's aggregation/audit to
identify incomplete work before plotting.

The shared filesystem has no backup guarantee. Preserve important inputs,
proofs and result records elsewhere after runs. These scripts do not delete
proof logs, clean run directories, or auto-submit follow-up jobs.

## Local checks

`python3 experiments/E002_blythe_phase_diagrams/slurm/check_scripts.py` checks
shell syntax and runs isolated tests with mocked `sbatch`, `srun`, and pipeline
commands. It exercises default dry-run behavior, resource limits, required
module selection, paths containing spaces, optional accounts, retries, and a
worker whose batch script has been copied away from the repository. Results
are saved in `local_checks.json`. These checks do not install the environment,
run the module stack, invoke real SLURM, or establish cluster performance.
