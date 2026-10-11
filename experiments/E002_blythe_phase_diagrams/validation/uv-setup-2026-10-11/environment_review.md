# E002 uv environment and SLURM migration review

- Reviewer: independent `analytic_transfer` agent; not the implementation author.
- Date: 2026-10-11.
- Scope: the project dependency specification and lock, Python selection, ignore rules, environment guard, setup/submission/worker scripts, and local shell-check harness. This is a scoped software review, not formal verification or validation on Blythe.
- Verdict: no remaining consequential defect found in the reviewed versions. One test-harness portability defect was identified, corrected by the implementation agent, and independently rechecked below.

## Checks and findings

Read the implementation and followed setup, dry-run submission, actual-submission gating, and spooled-worker execution paths. The guard checks the three project input hashes, full installed distribution name/version map, Python version, module selection/state, pinned checker source, and compiled checker hash against the prepared environment record. Submission and workers require that record and do not run `uv sync`, install dependencies, or compile the checker. Setup verifies the vendored source digest before compiling. Argument arrays and quoted absolute paths preserve spaces through these paths.

Checked the TOML dependency graph without changing the environment: all locked dependency names resolve, the virtual project metadata matches the three exact top-level pins, and the project and lock both select Python 3.12. The lock includes relevant macOS ARM and Linux x86-64 wheel alternatives. This does not verify installation against the actual Blythe module stack or ABI.

The initial mock `sbatch` and `srun` scripts used a Python shebang containing `sys.executable`, which fails when that interpreter path contains spaces. The corrected harness creates separate Python bodies and `/bin/sh` launchers that use `shlex.quote` for interpreter/script paths and forward `"$@"`. Independently inspected the corrected code and its revision-2 record. Each fixture now uses an interpreter and command directory containing spaces; the implementation agent additionally ran the harness through an actual interpreter path containing spaces. No full fixture rerun was performed by this reviewer after that correction.

Inspected `.gitignore` for the documented defaults: environment/cache directories, raw run directories, smoke artifacts, downloaded papers/site material, report outputs, and compiled checker binaries are excluded while source and dependency specifications remain eligible for tracking. No Git command was run; no initialized repository was available for a real index/staging audit. Nonstandard environment or result destinations need corresponding ignore rules or placement outside the checkout.

## Evidence inspected

- `../../slurm/local_checks_uv_2026-10-11_revision2.json`: shell syntax, mocked submission/dry run, quoted paths, resource validation, spooled worker, and rejection of stale locks, missing records, changed package records, and changed checker binaries. These are mocked scheduler checks: zero real SLURM, solver, or uv calls.
- This directory's `environment.json`, `checks.json`, `preflight.json`, and `exact-smoke-check.json`: coordinator-retained evidence of local macOS Python 3.12.8 setup, certificate preflight, 24 small smoke instances checked by exhaustive enumeration, plotting, submission dry run, and 23 unit tests reported passed. The coordinator reports setup used an offline uv cache. These executions were performed by the coordinator, not this reviewer.

## Limits and retained caveat

The guard binds the prepared environment to the **current checkout**, not to a dependency-lock snapshot in each run manifest. Rebuilding the environment after a dependency change can therefore permit an older run to resume with changed dependencies if its runner still matches. Runtime provenance can reveal a mixture, but does not prevent it. Use a new campaign plan after dependency changes when comparing timings; the updated documentation records this limitation. The frozen core runner was not changed for this setup task.

Python is pinned to the 3.12 minor series, not a single patch release; the prepared record captures and checks the actual patch version. Package version/hash checks are operational provenance checks, not a cryptographic attestation of every installed package file. No cluster allocation, real scheduler call, Linux installation, shared-filesystem concurrency test, or scientific concentration claim was validated here.

## Reviewed SHA-256 snapshots

Paths beginning `slurm/` are relative to `experiments/E002_blythe_phase_diagrams/`; others are relative to the repository root.

| File | SHA-256 |
| --- | --- |
| `pyproject.toml` | `d89a1041e5e772873417d2c728392e63da4e27e0c5f7526bbf6df5f6a174e794` |
| `uv.lock` | `509f78b96cedc768308525fb92daea9c8fc9095e75924c7bd498c89176516f4f` |
| `.python-version` | `7b55f8e67b5623c4bef3fa691288da9437d79d3aba156de48d481db32ac7d16d` |
| `.gitignore` | `9d3d5b97b630911f092d670209a632b389cc6ba3b7970c0bbac4a71bbb8b68d6` |
| `slurm/environment_guard.py` | `7245ad6fb6a1a16c42a3b09bb3e91b16506c0192678afa6f3e6b51187ada57bf` |
| `slurm/common.sh` | `9f42ecef25f85c5b07ee07550834246d790c5cad3e20d2c3dfe5ff1e5db41be5` |
| `slurm/setup_environment.sh` | `c9348f4126471b586cc83a8675c900cae7f7bcc107f9ad87cda45532b059fc61` |
| `slurm/submit_array.sh` | `0086ab23b1f9df38d2eeff237d516a29f0ff7d371b3de00dab2256cc7c943db1` |
| `slurm/run_array.sbatch` | `61ea849555c3dd7c2e7094e4df5350577564b36ab9c59b2a88819518cce4106e` |
| `slurm/check_scripts.py` | `2658c658f107d7714e51c793e435f829e720e3a61f8d35376ca4ed6e63e840ba` |
| `slurm/local_checks_uv_2026-10-11_revision2.json` | `570702bd860cf70c3e24220811f61aadcae4763ca885128fdf311e92550fa5ad` |
| `code/ksat_experiments.py` (unchanged runner boundary) | `197799ce3762883f03c64f06593bbe439823d3574c492391694bfdbdd7d5b1d0` |
