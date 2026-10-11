# E001: feasibility of SAT phase-transition diagrams

**State:** completed bounded runtime calibration; larger diagrams are proposed.
**Date:** 2026-10-11. **Author:** delegated computational-feasibility agent.
**Question:** Can a useful finite-size random k-SAT phase diagram be generated
with ordinary CPU resources before preparing cluster jobs?

See [findings.md](findings.md) for the design, estimates, and limitations.
This is an exploratory runtime measurement, not a theorem or a threshold estimate.

## Reproduction and provenance

The original command from the repository root was:

```sh
uv run --with python-sat==1.9.dev15 python experiments/E001_diagram_feasibility/calibrate.py
```

[calibrate.py](calibrate.py) deliberately refuses to overwrite `run001`.
Reproduce in a separate checkout/directory or change only the output run ID,
recording the resulting script hash. The RNG and all 60 seeds are recorded;
the preserved DIMACS inputs are the definitive inputs across Python versions.
Clauses use three distinct uniformly sampled variables, independent fair signs,
and independent sampling between clauses, including possible repeated clauses.

Hardware: Apple M3, macOS 26.6.2 arm64, one solver process at a time.
Python 3.12.4; PySAT 1.9.dev15; CaDiCaL 1.9.5; default solver options;
no proof logging. [metadata.json](run001/metadata.json) records configuration,
script hash and environment. There is no Git repository, so no Git revision
was available. [loaded_dependencies.json](run001/loaded_dependencies.json)
identifies actual imported modules, six 1.17.0, and the solver-extension hash;
`dependencies.json` inventories the wider visible environment and may include
shadowed package versions.

Each of 60 subprocesses received a 0.75-second wall-time cutoff including
Python startup, input parsing, initialization, solving and result serialization.
Total solver-process CPU time was 29.35 seconds; total elapsed time 30.89 seconds.
The planned aggregate child time allowance was 45 seconds plus termination
overhead. There were no solver errors. All 30 timeouts remain `unknown`.
All 21 SAT models were checked by exact integer clause evaluation and saved.
The nine UNSAT outputs are **unchecked solver reports**, with no retained proofs.
They must not be counted as certified UNSAT evidence in a publication.

Raw results: [results.jsonl](run001/results.jsonl),
[summary.json](run001/summary.json), [inputs](run001/inputs/),
[witnesses](run001/witnesses/). All 60 input hashes and all 21 SAT models were
rechecked after completion by [verify.py](verify.py), which also regenerates
all inputs from their seeds and checks the original calibration script hash.
Run `python3 experiments/E001_diagram_feasibility/verify.py`; the completed
check is saved in [verification.json](run001/verification.json).
These are author self-checks, with no claim of independent review.
No floating-point tolerance enters witness checking;
floating-point durations are descriptive timing measurements.

No GPU experiment, cluster connection, SLURM script, or full diagram was produced.
No failed runs or timeouts were discarded. Any larger timing extrapolation is
conditional; five instances per cell cannot estimate probabilities accurately.
