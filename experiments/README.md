# Experiment registry

One bounded runtime calibration is complete and a Blythe workflow is prepared.
Numerical experiments are not proofs, including
when every tested instance agrees with a conjecture. Exact finite checks still
need a justified reduction and coverage argument to establish a wider claim.

| ID | Question | Run state | Main observation and limits | Record |
| --- | --- | --- | --- | --- |
| [E001](E001_diagram_feasibility/README.md) | Feasibility of finite-size SAT-probability diagrams | Completed 60-instance calibration | At a 0.75 s process cutoff, all 20 n=100/200 cases returned; 30 of 60 cases overall timed out. 21 checked SAT witnesses and 9 unchecked UNSAT reports; not a threshold estimate. | [Findings](E001_diagram_feasibility/findings.md), raw inputs/results and verification under run001. |
| [E002](E002_blythe_phase_diagrams/README.md) | Certified finite-size SAT-probability diagrams on Blythe | uv/SLURM workflow prepared, including batch collection/plotting; cluster campaign not run | Local software validation only: 23 tests and 24 tiny formulas checked against exact truth tables; batch scripts checked with scheduler mocks; no threshold estimate. | Locked dependencies, SLURM walkthrough and scripts, configs, runner, plotter, raw smoke data and scoped review. |

For a new experiment, use the next unused ID (currently E003) and copy [TEMPLATE.md](TEMPLATE.md)
to its `README.md`. Keep scripts, inputs, raw outputs, and logs together; place
reusable implementation in `../code/`. Use dated or numbered run subfolders to
preserve earlier results. Do not commit a large dataset without considering a
retrieval manifest and checksums instead.

Record commands relative to the project root, dependency versions or a lockfile,
code version, parameters, seeds, arithmetic, tolerances, and stopping conditions.
Keep raw data behind figures and link report figures to their producing run.
Distinguish `planned`, `running`, `completed`, `failed`, and `interrupted` runs.
Never report a planned, failed, or interrupted run as completed validation.

A candidate numerical counterexample must be verified exactly or by rigorous
certification before it refutes a claim. Promote an actual computer-assisted
argument to `proofs/` only with its reduction, coverage, certificates/checker,
and trusted assumptions fully documented.
