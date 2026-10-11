# uv environment validation, 11 October 2026

**Question:** does the locked project environment support the existing
certificate-checking and plotting workflow? **State:** local checks complete;
Blythe execution is untested. No threshold or concentration conclusion follows.

## Environment and commands

The project uses Python 3.12 and root `pyproject.toml`/`uv.lock`. This check used
uv 0.6.6, Python 3.12.8 and Apple M3/macOS. The exact resolved package versions,
compiler, source and binary hashes are in [environment.json](environment.json).
The lock was generated using uv, not edited manually. Setup ran successfully:

```sh
UV_OFFLINE=1 UV_CACHE_DIR=/tmp/ksat-uv-cache \
  bash experiments/E002_blythe_phase_diagrams/slurm/setup_environment.sh
```

The environment had already been populated using `uv sync --locked`; the
offline setup verified that lock, compiled DRAT-trim and wrote its prepared
environment record. [checks.json](checks.json) records exact smoke commands,
exit codes, source/lock hashes and the separate 23-test unit-suite result.
The unittests' console output was observed, not saved as a second raw log.
AGENTS.md and both core Python implementation files retain their previous hashes.

## Outcomes

- All **23 software tests** passed in the new `.venv`.
- [Preflight](preflight.json) checked a SAT witness, verified an UNSAT proof,
  and rejected the deliberately invalid proof with an explicit verdict.
- The same `configs/smoke.json` seeded grid was run into a fresh
  `../uv-smoke001/` directory: n=6,8; densities 0,1,4,8; three repetitions per
  cell, base seed 20261012000, two workers, 5-second solve/check cutoffs.
  It produced **19 checked SAT and 5 checked UNSAT**, with zero unresolved.
- Independent exact truth tables agreed for all 24 formulas; see
  [exact-smoke-check.json](exact-smoke-check.json). The finite enumeration uses
  integer/Boolean arithmetic and no numerical tolerance.
- The plotter wrote eight cell summaries, CSV/JSON and three PNG/PDF pairs.
  All three PNGs were visually inspected: readable labels/legends, zero
  unresolved fraction and explicit software-smoke labels. Their source is the
  unchanged plotter at the hash in `checks.json`. Matplotlib reported its usual
  fallback to a temporary cache because this sandbox cannot write the default
  user cache; plotting completed successfully and the message remains in its log.
- The real submission helper accepted the prepared environment and printed
  a two-chunk `sbatch` command in **dry-run mode**. No scheduler call occurred.
  Separate mocked shell checks, including stale-lock rejection and paths with
  spaces, are recorded in
  [the final shell record](../../slurm/local_checks_uv_2026-10-11_revision2.json).
- A separate agent completed a scoped [environment review](environment_review.md).
  The review identified a test-launcher quoting issue, independently checked
  its correction, and found no remaining consequential defect within the
  recorded scope. This is internal software review, not cluster validation.

Raw inputs, certificates, attempts and plots remain in `../uv-smoke001/`, which
is excluded from Git along with other generated runs; the small validation
records here remain available in the source checkout. Reproduce using fresh
destinations and the commands in `checks.json`. Preserve this record and earlier
pip-era runs rather than overwriting them.

## Limits

This tests the local platform only. Linux memory limits, Blythe's modules,
filesystem and scheduler still need the certified pilot. The guard validates
the current checkout and packages, not one dependency lock pinned forever to a
run manifest; use a fresh plan after dependency changes for comparable timings.
Workspace permissions blocked `git init` from creating `.git`; no commit or
remote was created. This is unrelated to the successful uv/software checks.
