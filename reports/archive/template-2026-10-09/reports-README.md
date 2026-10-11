# LaTeX reports

The report uses an A4 article layout with Palatino-style text and mathematics,
navy section headings, teal accents, a title page, a linked contents page, and
numbered theorem environments. The design is adapted from PNP; no PNP files or
project-specific mathematical claims are required.

## Build

Install a TeX distribution such as TeX Live or MacTeX providing `latexmk`,
`pdflatex`, BibTeX, and the packages loaded in `preamble.tex`. No shell escape,
network access, external fonts, or Python runtime is needed to compile.

From the project root:

```sh
make report
```

Or from this directory:

```sh
make pdf
```

The PDF is written to `output/pdf/report.pdf`; auxiliary files stay in `build/`.
`make clean` removes auxiliary files and retains the compiled PDFs. To change
the delivery filename, use `make -C reports pdf REPORT_NAME=progress-note`.

Without Make, run these commands from `reports/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
mkdir -p output/pdf
cp build/main.pdf output/pdf/report.pdf
```

## Customize

| File / directory | Edit here for |
| --- | --- |
| `metadata.tex` | Title, subtitle, author, date, short running title, report status, bibliography switch. |
| `main.tex` | Section order, title page, front matter, and bibliography. |
| `preamble.tex` | Typography, page geometry, colors, theorem environments. |
| `macros.tex` | Shared mathematical notation. |
| `sections/` | Problem, sources, results, attempts, experiments, and next steps. |
| `references.bib` | Verified bibliographic entries. |
| `figures/` | Figures with links to producing experiment/source records. |
| `../proofs/` | Canonical proof fragments included by the report. |

Replace the instructional prose when initializing a project. The explicit page
breaks in `main.tex` organize this short sample; change them as the report grows.
The sample includes `../proofs/TEMPLATE.tex` only to demonstrate shared sources;
replace that input with real `P` records. The template is not a theorem or a
completed proof. Keep the cover's status statement accurate.

The environments `theorem`, `lemma`, `proposition`, `corollary`, `definition`,
`conjecture`, `example`, and `remark` share a section-based counter. Use `proof`
only for a complete argument, and `proofoutline` for an incomplete derivation;
the latter has no end-of-proof symbol. Use `\label` and `\ref`/`\eqref` for
cross-references, and `\claimstatus{...}` for explicit scope and review state.

Proof fragments have no preamble or `\begin{document}`. Include them from a
section with `\input{../proofs/P001_short_name}`. Use labels containing the ID
to avoid collisions. Shared notation belongs in `macros.tex`. Do not maintain
separate mutable copies of the same argument in proofs and reports.

## Citations

The starter bibliography contains comments only: there are no invented sources.
After checking a source in `papers/` or `references/`, add a real BibTeX entry,
cite it with `\citet{key}` or `\citep[Theorem 2.1, p.~7]{key}`, and change
`\reportbibliographyfalse` to `\reportbibliographytrue` in `metadata.tex`.
`latexmk` then runs BibTeX and resolves the citations. Keep detailed verification
notes in `references/`; publication metadata alone does not check a result.

## Delivery checks

Resolve build errors, undefined references/citations, and overfull boxes. Inspect
the final PDF for clipped mathematics, poor page breaks, and unreadable figures.
Check that every result has the right scope and evidence label, and that all
figures can be traced to their source. A successful build is not a proof audit.
Keep both sources and PDF. For dated reports, preserve a source snapshot or
commit reference as well as the PDF so its exact contents can be reconstructed.
