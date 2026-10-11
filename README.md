# Random k-SAT research

The initial project deliverable is a survey of satisfiability thresholds,
decision and witness algorithms, practical instance sizes, GPU acceleration,
and the connection to phase transitions in convex geometry.

- [Git, uv and Blythe setup](docs/blythe-uv.md): clone/pull the source and create
  a separate locked environment on each machine.
- [Read the survey PDF](reports/output/pdf/report.pdf).
- [Discrete geometry and diagram feasibility](reports/output/pdf/geometry-feasibility-2026-10-11.pdf),
  with exact elementary arguments and a bounded CPU calibration.
- [Blythe experiment workflow](experiments/E002_blythe_phase_diagrams/README.md):
  SLURM batches, retained certificates, CSV/JSON data and phase-diagram plotting.
- [Concentration research prompt](attempts/A001_discrete_geometry/concentration_research_prompt.md).
- [Concentration investigation](reports/output/pdf/concentration-2026-10-11.pdf):
  the proposed two-sided bound is refuted by rare early UNSAT cores; exact
  tilted-process identities and a conditional one-sided route are recorded.
- [Editable LaTeX entry point](reports/main.tex) and [bibliography](reports/references.bib).
- [Problem specification](PROBLEM.md), [current status](STATUS.md), and
  [source catalogue](references/README.md).
- [Claim registry](proofs/README.md), [attempts](attempts/README.md),
  [experiments](experiments/README.md).

Build from this directory with `make report` (requires LaTeX and latexmk).
The survey literature snapshot is 10 October 2026; the follow-up has targeted
source checks dated 11 October. [E001](experiments/E001_diagram_feasibility/README.md)
records a 60-instance local runtime calibration, not a threshold measurement.
Benchmark numbers in the survey belong to the cited papers.
The existing [AGENTS.md](AGENTS.md) was preserved unchanged.

## Python setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run
from the repository root:

```sh
uv sync --locked
uv run --locked python -m unittest discover -s code/tests -v
```

Python 3.12 and dependencies are specified by `.python-version`,
`pyproject.toml` and the shared `uv.lock`. This is a script-based research
project, not an installable Python library. For experiments, prepare the
vendored C proof checker as well:

```sh
bash experiments/E002_blythe_phase_diagrams/slurm/setup_environment.sh
```

That setup command requires uv and a C compiler; it also performs the locked
sync. Follow the [E002 guide](experiments/E002_blythe_phase_diagrams/README.md)
to plan, review and submit a pilot. Each machine creates its own `.venv`.
Downloaded papers, saved SCRTP pages, raw run directories, compiled reports
and local environments remain outside Git; see the setup guide for the
source/data boundary. No real Blythe campaign has been run.
# ksat
