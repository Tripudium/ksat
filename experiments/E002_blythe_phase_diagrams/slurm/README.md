# Blythe CPU batches with uv

The scripts use the repository's `pyproject.toml`, `uv.lock` and Python 3.12
selection. Clone the repository into your actual
`/springbrook/share/<group>/...` project directory on Blythe. Each checkout gets
its own `.venv`; create it on Blythe rather than copying a laptop environment.

Defaults remain `compute`, one node, 16 CPU workers, 2048 MB per CPU, 45 minutes,
and at most four array tasks concurrently. These are initial planning choices,
not a measured optimal configuration. No GPU is requested.

## Prepare after cloning or pulling

Have `uv` and a C compiler available on the login node. A Python module is
optional: uv can provision the project's Python during setup. If a compiler
module is needed, select an available one using the site's `module avail`; set
`KSAT_MODULES` to the exact space-separated module names. When nonempty, scripts
run `module purge` and load those modules. When empty, the current environment
is retained. No module version is guessed from the supplied documentation.

Run from the cloned repository:

```sh
bash experiments/E002_blythe_phase_diagrams/slurm/setup_environment.sh
```

Setup runs `uv sync --locked`, verifies the vendored proof-checker source hash,
and compiles `drat-trim` into `.venv/bin/` with `cc -std=c99 -O2`. Set `CC` to a
different compiler executable if needed. This login-node step can download
Python and locked packages. Jobs use the prepared executable directly and
never run uv, sync packages, or make package-installation network requests.

Optional paths:

- `KSAT_PROJECT_DIR`: explicit repository path; normally inferred correctly.
- `KSAT_ENV_DIR`: environment path instead of `.venv`; the scripts map it to
  `UV_PROJECT_ENVIRONMENT` for uv. Relative values are relative to the repository.
- `KSAT_DRAT_TRIM`: alternate checker path, accepted only if its binary matches
  the prepared checker hash. The default is the selected environment's checker.

Setup writes a dated record and `.venv/ksat-environment.json` with the project
file hashes, complete resolved package versions, Python version, module selection,
compiler and source/binary hashes. Submission and each worker check that record
against the current checkout and environment. A changed `uv.lock`, project
specification, Python selection, package set or checker produces a clear error
before solving. After `git pull`, rerun setup to prepare and record the updated
environment. Running `uv sync` alone does not build the checker or renew its
setup record.

Finish active jobs before updating their checkout/environment; use a separate
checkout and environment when old jobs must keep running with their original
code and dependencies. Existing experiment manifests pin the runner code, but
**do not pin the dependency lock for the entire campaign**. The environment
guard checks the current checkout, not a campaign-specific historical lock.
After changing dependencies, create a new plan for comparable runtime results.
Resuming an older plan after successful setup can otherwise mix separately
recorded environments within that campaign; it does not make its timings
directly comparable. This is a reproducibility limitation, not a change to SAT
witness or UNSAT proof checking.

## Plan and review a submission

Use the configuration documented in the main experiment README. For the default
environment, run:

```sh
.venv/bin/python code/ksat_experiments.py plan \
  --config path/to/config.json --output /absolute/project/run-directory
bash experiments/E002_blythe_phase_diagrams/slurm/submit_array.sh \
  /absolute/project/run-directory
```

Use `$KSAT_ENV_DIR/bin/python` if you selected a different environment. Run data
must reside on the compute-visible shared filesystem; do not assume `/scratch`
or desktop mounts exist on Blythe.

The helper validates the prepared environment, reads `manifest.json`, derives
the zero-based array range, creates `slurm-logs/`, and **prints the command by
default**. It runs no solver preflight on the login node. Add `--submit` to submit:

```sh
bash experiments/E002_blythe_phase_diagrams/slurm/submit_array.sh \
  /absolute/project/run-directory --submit
```

No account is assumed. Supply an actual account/share with `--account` or
`KSAT_ACCOUNT` if your association requires one. Adjust `--cpus`, `--concurrency`,
`--time HH:MM:SS`, and `--mem-per-cpu` after measuring the initial jobs. The saved
site limits are 168 CPUs/node, 4591 MB/CPU, and 48 hours/job.

A conservative chunk-time estimate is
`ceil(instances_in_chunk/workers) * (solve_cutoff + check_cutoff + overhead)`.
Keep it comfortably below the wall limit. Startup, proof serialization and
storage need allowance as well.

## Worker execution and retries

The worker uses the exported absolute project path, falling back to
`SLURM_SUBMIT_DIR`; it does not derive paths from SLURM's copied batch script.
It checks the environment, performs proof-checker preflight inside its allocation,
then runs the chunk with `--workers "$SLURM_CPUS_PER_TASK"` under `srun`.
BLAS/OpenMP thread counts are one to avoid oversubscribing the process pool.

Stdout and stderr go to `slurm-logs/<array-job>_<task>.out` and `.err`.
Preflight JSON files have independent names. The pipeline preserves results,
certificates and unknown outcomes. Repeating a chunk skips completed results;
`--retry-unknown` requests new attempts while retaining earlier records.
Failed or killed work is not counted as UNSAT. Audit and aggregate results
before plotting. Archive important results away from the live GPFS filesystem,
whose saved documentation provides no backup guarantee.

## Local validation and previous delivery

Run `uv run --locked python experiments/E002_blythe_phase_diagrams/slurm/check_scripts.py`
for isolated shell integration checks. These use mocked `sbatch`, `srun` and
pipeline commands: they exercise dry runs, resource validation, paths containing
spaces (including actual mock interpreter/command paths), accounts, retries,
spooled-script paths and rejection of stale locks,
missing setup records, changed packages and changed checker binaries.
They do not sync/install anything, run a module stack, or contact SLURM.

The final validation record is `local_checks_uv_2026-10-11_revision2.json`,
which includes the interpreter-path portability correction. The preceding uv
record `local_checks_uv_2026-10-11.json` is preserved unchanged.
Original pip/venv scripts, documentation and validation records are preserved
under `archive/pip-workflow-2026-10-11/`; original `local_checks*.json` files remain
unchanged. They describe the earlier delivery and are not claims that the uv
workflow ran on Blythe. No cluster job has been submitted during preparation.
