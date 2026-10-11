# Git and uv workflow for Blythe

The source travels through Git. Each machine builds its own Python environment
from `pyproject.toml`, `.python-version` and `uv.lock`. The project uses Python
3.12; the lock fixes package versions and distributions across supported
platforms. The Python patch version may differ between hosts and is recorded
by experiment setup. Environments and compiled checkers are machine-specific.
See uv's [project guide](https://docs.astral.sh/uv/guides/projects/) and
[locking/sync documentation](https://docs.astral.sh/uv/concepts/projects/sync/).

## Initialize and publish once

The project files are prepared. This workspace denied creation of `.git`, so
local initialization must be run in your own terminal:

```sh
cd /Users/u1774790/Projects/ksat
git init -b main
git status --short --ignored
git add .
git diff --cached --stat
git commit -m "Initialize random k-SAT research and uv experiment workflow"
```

Review the staged inventory before committing. `.gitignore` excludes `.venv`,
caches, `cluster-runs/`, raw historical runs, downloaded reference originals,
saved SCRTP websites and rebuildable report outputs. It retains source code,
tests, small validation/provenance records, configurations, mathematical sources
and source notes. The vendored checker includes its original MIT license.
Existing local files are preserved; ignoring them does not delete them.

Create an **empty** GitHub repository with the visibility you want, then replace
`OWNER/REPOSITORY` with its actual path:

```sh
git remote add origin git@github.com:OWNER/REPOSITORY.git
git push -u origin main
```

No GitHub repository, remote or commit was created by this setup. Use your
normal GitHub authentication; an HTTPS remote works too.

## Clone and prepare on Blythe

Use your actual group share and repository URL:

```sh
cd /springbrook/share/YOUR_GROUP
git clone git@github.com:OWNER/REPOSITORY.git ksat
cd ksat
uv --version
cc --version
bash experiments/E002_blythe_phase_diagrams/slurm/setup_environment.sh
```

Have [uv](https://docs.astral.sh/uv/getting-started/installation/) and a C
compiler available on the login node. If necessary, set `KSAT_MODULES` to
actual site module names before setup, and keep that selection when submitting.
No Python module is required when uv can provision Python. Setup may download
Python/packages; the compute jobs use the prepared `.venv/bin/python` directly
without downloading or syncing anything. Do not copy the laptop `.venv`.

Setup runs `uv sync --locked`, compiles the pinned DRAT-trim source, and records
Python/package/module/checker versions and hashes in
`.venv/ksat-environment.json` plus a dated history file. Submission and workers
reject stale locks or mismatching environments. `KSAT_ENV_DIR` optionally
selects another environment; the scripts map it to `UV_PROJECT_ENVIRONMENT`.
Running `uv sync` alone does not build or record the checker.

## Plan the pilot, then submit

Planning only writes the run manifest; it does not solve the pilot on the
login node. Choose a fresh destination for each new plan:

```sh
export KSAT_RUN_DIR="$PWD/cluster-runs/3sat-pilot-001"
.venv/bin/python code/ksat_experiments.py plan \
  --config experiments/E002_blythe_phase_diagrams/configs/pilot-3sat.json \
  --output "$KSAT_RUN_DIR"
bash experiments/E002_blythe_phase_diagrams/slurm/submit_array.sh "$KSAT_RUN_DIR"
```

The last command prints the proposed `sbatch` command. Add `--submit` to run it;
see the [SLURM guide](../experiments/E002_blythe_phase_diagrams/slurm/README.md)
for resource/account overrides and retries. The actual submission is:

```sh
bash experiments/E002_blythe_phase_diagrams/slurm/submit_array.sh \
  "$KSAT_RUN_DIR" --submit
```

The helper queues `run_array.sbatch`; solver and certificate work runs on
compute nodes in a non-interactive SLURM allocation. Do not run the solver or
batch worker directly on a login node. Monitor with `squeue -u "$USER"` and
`sacct -j JOB_ID --format=JobID,State,ExitCode,Elapsed`, replacing `JOB_ID` with
the returned array ID. Jobs continue after disconnecting SSH. No jobs have
been submitted during preparation.

After the array finishes, submit collection and plotting as another batch job:

```sh
mkdir -p "$KSAT_RUN_DIR/slurm-logs"
sbatch --parsable --export=ALL --chdir="$PWD" \
  --output="$KSAT_RUN_DIR/slurm-logs/plot-%j.out" \
  --error="$KSAT_RUN_DIR/slurm-logs/plot-%j.err" \
  experiments/E002_blythe_phase_diagrams/slurm/plot_results.sbatch \
  "$KSAT_RUN_DIR" "$KSAT_RUN_DIR/analysis-v1"
```

This also keeps the potentially large artifact-hashing workload off the login
node. If required, put `--account=ACCOUNT` before the script path; plain
`sbatch` does not automatically use `KSAT_ACCOUNT`. Append `--allow-partial`
after the directory arguments to retain missing jobs as unresolved. Use a
fresh analysis output directory for each collection. The complete
[E002 walkthrough](../experiments/E002_blythe_phase_diagrams/README.md#run-on-blythe-through-non-interactive-slurm-jobs)
covers logs, resource requests, retries and scaling beyond the pilot.

Save the Git revision
(`git rev-parse HEAD`), setup record and lock with the run archive. Inputs,
certificates, timings, seeds and runtime provenance are recorded by the runner.
Numerical phase diagrams do not prove concentration of T_n.

## Pull updates and develop

Finish queued/running jobs before changing their checkout or environment. Use
a separate clone and environment when campaigns must retain older versions.
On an idle Blythe checkout:

```sh
git pull --ff-only
bash experiments/E002_blythe_phase_diagrams/slurm/setup_environment.sh
```

For local development, use `uv sync --locked` followed by
`uv run --locked python -m unittest discover -s code/tests -v`. Change dependencies
with `uv add`/`uv remove`, then commit both `pyproject.toml` and `uv.lock` and
rerun checks. Do not regenerate the lock as part of a routine cluster pull.
An existing run also checks the runner source hash; code changes may require
a new plan even if dependencies are unchanged.

The environment guard checks the **current checkout**, not a dependency lock
embedded in the run manifest. Resuming an old plan after redoing setup can
therefore mix dependency environments, although each chunk records its runtime
provenance. Create a fresh plan after dependency changes to keep campaign
timings comparable; do not pool mixed-environment timings without accounting
for the change.

## Source and data storage

A fresh clone contains the experiment implementation and vendored checker.
It does not require local papers or historical raw data to run. Those materials
remain in the original working copy and should be backed up separately;
links to local PDFs or previous raw runs may be absent in a fresh clone.
Reports can be rebuilt with `make report` when LaTeX/latexmk are available.
Restore supplied/downloaded papers separately when doing source-based research.

Keep large run directories on the shared filesystem, and archive completed
inputs/results/proofs outside the live cluster storage. Commit small configs,
reading notes and validation records. Do not commit virtual environments,
generated datasets, credentials, or third-party downloads by forcing ignored
paths into Git. No repository-wide license has been chosen for this research.
