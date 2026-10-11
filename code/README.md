# Shared research code

## Random k-SAT experiment workflow

- [ksat_experiments.py](ksat_experiments.py): immutable plans, versioned
  generation, isolated complete solves, certificate checks and resumable chunks.
- [plot_ksat_phase.py](plot_ksat_phase.py): audit results and generate CSV/JSON,
  phase-probability bounds, complete-cell contours and uncertainty curves.
- [E002 guide](../experiments/E002_blythe_phase_diagrams/README.md): dependencies,
  commands, Blythe settings, interpretation and validation records.
- [tests/](tests/): run `uv run --locked python -m unittest discover -s code/tests -v`
  from the root after `uv sync --locked`.

The third-party DRAT-trim source is preserved with its MIT license and exact
upstream commit in [vendor/drat-trim/SOURCE.json](vendor/drat-trim/SOURCE.json).
No general random-SAT claim follows from the software checks.

## General code conventions

Put reusable implementation here and keep experiment-specific drivers and run
records in `experiments/`. Python 3.12 and the dependency set are managed by
the root `pyproject.toml`, `.python-version` and `uv.lock`. Update and commit the
manifest and lock together; rerun experiment setup after dependency changes.
The scripts run directly from the checkout; no package build is required.

Document public inputs, outputs, mathematical conventions, and arithmetic
assumptions. Test consequential implementation behavior against exact small
cases or independently derived invariants where feasible. Passing software
tests is not a proof of the research claim. Record the code version used by
each experiment and preserve reproducible entry points.
