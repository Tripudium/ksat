# Mathematical research project template

A reusable workspace for substantial mathematical research. No particular problem,
research finding, or literature claim is built in. The organization follows MaMu;
the LaTeX design is adapted from PNP's Palatino-style type, navy headings, and teal
accents. Everything needed to use this template lives in this folder.

## Start a project

1. Copy this folder to the new project location, including `.gitignore`. Omit
   `reports/build/` and `tmp/` if present; they contain generated files.
2. Fill in [PROBLEM.md](PROBLEM.md): the exact target, definitions, hypotheses,
   quantifiers, and success criteria. Keep it authoritative about the scope.
3. Set the date and initial priorities in [STATUS.md](STATUS.md). Read
   [AGENTS.md](AGENTS.md) before beginning research.
4. Add relevant papers to `papers/` and other source material to `references/`.
   Catalogue them in [references/README.md](references/README.md), record what
   was actually checked, and add verified citations to `reports/references.bib`.
5. Edit `reports/metadata.tex` and replace the instructional text in
   `reports/sections/`. Copy the record templates when starting a proof, attempt,
   experiment, or source note; the templates are not live registry entries.
6. Run `make report` from the project root. The editable source is
   [reports/main.tex](reports/main.tex); the reading copy is
   `reports/output/pdf/report.pdf`. See [reports/README.md](reports/README.md)
   for prerequisites and customization.

## Layout

| Path | Purpose |
| --- | --- |
| `PROBLEM.md` | Mathematical objective, scope, notation, and success criteria. |
| `STATUS.md` | Current conclusions, gaps, and ordered next actions. |
| `AGENTS.md` | Research, evidence, review, and handoff instructions. |
| `proofs/` | Precise claims, substantial LaTeX proofs, and review records. |
| `attempts/` | Open approaches, obstacles, failed variants, and counterexamples. |
| `experiments/` | Reproducible numerical, symbolic, and finite searches. |
| `code/` | Reusable implementation shared by experiments. |
| `papers/` | Primary literature, normally PDFs with stable filenames. |
| `references/` | Source catalogue, reading notes, and other reference material. |
| `reports/` | LaTeX report, bibliography, figures, and compiled output. |

Use stable IDs: `P001` for a proof/claim record, `A001` for an attempt, `E001`
for an experiment, and `S001` for a source note. IDs link the records; they do
not certify their contents. The first real record starts at `001` in each registry.

**Numerical experiments are not proofs.** Finite tests, plots, floating-point
calculations, and symbolic output may suggest or challenge a claim, but do not
establish a general theorem. A completed argument must justify its full scope,
including any computer-assisted proof component. Source claims must be checked
against the actual material in `papers/` or `references/`, with assumptions and
precise theorem/page locations recorded.

Markdown is used for project management and short records. Mathematical reports
and substantial proof write-ups use LaTeX, with editable sources and compiled PDFs.
