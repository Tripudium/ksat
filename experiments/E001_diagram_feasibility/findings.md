# Computational feasibility of phase-transition diagrams

**Assessment, 2026-10-11:** useful finite-size diagrams are feasible on CPUs.
Start with random 3-SAT at 50–200 variables; extend the upper range after a
longer pilot with UNSAT proof checking. A cluster buys independent repetitions
and more time for difficult instances. It does not guarantee tractability for
arbitrarily large near-threshold formulas. GPUs are an optional later comparison.

## What to plot

For fixed k, estimate `p(n,m)=Pr[F_k(n,m) is SAT]` with horizontal coordinate
`n` and vertical coordinate `alpha=m/n`; use separate panels for k=2,3,4.
Show empirical SAT probability, 5/50/95% probability contours, and a separate
timeout/unknown panel. This exposes the location and narrowing density window.
The corresponding clause-count width is `m_0.05(n)-m_0.95(n)` because SAT
probability decreases with m. Plot both clause width and width divided by n.
A heat map of solver success within a time budget is a separate algorithmic
observable and must not be labelled the satisfiability phase diagram.

Unlike ALMT, standard random k-SAT has no second continuous sparsity parameter
at fixed ambient dimension. Varying n and density is the cleanest two-axis
analogue. A fixed-n panel varying integer k and density is also possible, but
changing k changes the ensemble and input size sharply. A curve from a cavity
prediction or fitted scaling law must be labelled conjectural/empirical;
the geometric papers do not provide a proved k-SAT boundary curve.

ALMT's supplied `iau005.pdf`, Figure 1 (printed p. 226; PDF page 3), Figure 5
(p. 235; PDF page 12), and Appendix A.1 (pp. 273–274; PDF pages 50–51) use
independent trials per grid cell. All four pages were rendered and visually
inspected. Figure 1 shows brightness maps; Figure 5 adds 5/50/95% contours
and a separate yellow theory curve. The
d=100 compressed-sensing panel specifies 100 choices of sparsity × 100
measurement counts × 50 repetitions, i.e. 500,000 convex solves. A separate
low-rank experiment took nearly a month on a desktop. Appendix A.3 fits
logistic curves. A similarly dense grid is unnecessary for the first SAT figure.

## A small measurement already completed

E001 tested 60 independent proper random 3-CNF inputs at alpha=4.2 and 4.3,
five instances per density and size. One CaDiCaL 1.9.5 process per instance
ran on an Apple M3 through PySAT 1.9.dev15, with a 0.75-second subprocess
cutoff **including startup and initialization**. All inputs, seeds, software
metadata and SAT models are retained in `run001/`.

| n | SAT, witness checked | UNSAT, unchecked report | Unknown | Mean process wall time, including cutoffs |
| ---: | ---: | ---: | ---: | ---: |
| 100 | 6 | 4 | 0 | 0.074 s |
| 200 | 5 | 5 | 0 | 0.257 s |
| 300 | 4 | 0 | 6 | 0.620 s |
| 400 | 5 | 0 | 5 | 0.612 s |
| 600 | 1 | 0 | 9 | 0.747 s |
| 800 | 0 | 0 | 10 | 0.754 s |

Total elapsed time was 30.89 s and aggregate child CPU time 29.35 s. The
pilot establishes that useful small instances are cheap and that runtime
censoring already matters at a few hundred variables under this short budget.
It does **not** establish a largest solvable size, the true mean completion
time for censored cells, a probability curve, an exponential growth rate, or a
ranking of modern solvers. UNSAT proof-generation/checking cost was not measured.

## Sampling designs and uncertainty

**Independent cells:** a first figure might use 8 sizes × 31 densities ×
100 formulas, or 24,800 solver runs. Begin with n=50,75,100,125,150,175,200
and an optional 250 after checking its timeout rate. Use a broad coarse density
range (e.g. 3.5–5.0 for k=3), then refine where probabilities change. Record the
actual integer m, since nearby densities may yield the same m at small n.
Determine the refinement grid with separate pilot samples, then use fresh
formulas for reported fixed-cell uncertainty; this avoids casually treating
adaptively selected data as a fixed design. Start k=4 with a separate pilot
around n=30–100 rather than carrying over the k=3 size recommendation.

At p approximately 1/2, 95% Wilson interval half-widths are about 0.134 for
50 trials, 0.096 for 100, and 0.049 for 400. These are **pointwise** intervals,
not simultaneous guarantees for the full heat map. Fifty trials can make an
illustrative image, but give little information about the 5% and 95% contours.
More repetitions improve statistical precision, not the solver's ability to
classify the hard instances.

**Coupled paths:** independently sample R clause sequences for each n and
estimate their first-UNSAT times T_n. Then every sequence contributes to the
whole survival curve `p(n,m)=Pr(T_n>m)`. If a path has certified SAT at L and
certified UNSAT at U, its hitting time lies in `(L,U]`; bisection determines it
with at most `ceil(log2(U-L))` further complete SAT calls. Without a proved
upper endpoint, retain right-censoring; an unknown internal query does not
determine a new side of the bracket. Exact T is certified by a SAT witness at
T-1 and a checked UNSAT proof at T. Incremental CaDiCaL can reuse work while
adding clauses, but removing them for bisection needs a fresh solver or correctly
implemented activation assumptions. Benchmark this against fresh-instance
solving: assumptions and repeated hard boundary queries may cost more.

For fully classified independent paths, Dvoretzky–Kiefer–Wolfowitz gives a
uniform-in-m 95% absolute error bound `sqrt(log(40)/(2R))`; R=738 suffices
for error 0.05 along one n-row. Across J rows, the union-bound choice is
`sqrt(log(2J/0.05)/(2R))`. Dependencies along a path are intentional; uncertainty
resampling must use whole paths, not pretend their prefixes are independent.
No logistic shape should be assumed without a goodness-of-fit check.

## Certification and unknowns

Save the raw status, elapsed time, solver version/options, input hash and seed.
Check each SAT witness directly against the original CNF. For publication-grade
UNSAT classifications, retain DRAT/LRAT proofs and check them with a specified
checker, including preprocessing and formula reconstruction in the certificate
chain. A solver saying UNSAT is weaker evidence than a checked proof; preserve
that distinction as in E001. Proof-checking time/storage belongs in the budget.

For R formulas with S verified SAT and U verified UNSAT outcomes, the empirical
SAT fraction is only known to lie in `[S/R,1-U/R]`. This is a censoring bound,
not a confidence interval for the population. Add sampling uncertainty (for
example binomial bounds for the verified-SAT and verified-UNSAT indicator
probabilities). Never call timeouts UNSAT or discard them when fitting a curve.

## Complexity and budget

Formula generation and witness checking cost O(km); a packed input needs about
4km bytes for 32-bit literals alone. Known general complete algorithms for
k>=3 have exponential worst-case bounds; no exponential lower bound for every
algorithm is asserted here. No polynomial-in-n runtime guarantee is supplied
by knowing the random threshold. For k=2, a strongly connected components solver
gives O(n+m) decision and assignment extraction, providing a useful scalable
control panel. At near-threshold larger k, m is itself of order 2^k n, so literal
count and proof memory must be considered as well as n.

Let t be the **measured mean per-instance total processing time, including
timeouts at the chosen cutoff and certification costs**, on the target CPU.
For approximately 25,000 runs, total work is 25,000t/3600 core-hours:

| Mean t | CPU core-hours | Ideal elapsed time on 64 CPU workers |
| ---: | ---: | ---: |
| 0.1 s | 0.69 | 39 s |
| 1 s | 6.94 | 6.5 min |
| 10 s | 69.4 | 1.09 h |
| 60 s | 416.7 | 6.51 h |

These are budget arithmetic, **not forecasts from E001**. Divide by efficiency
eta as well as worker count for wall time; queue delays are extra. At very short
times, use batches to amortize process and scheduler overhead. Dynamic work
distribution mitigates long-tail stragglers. Prefer independent single-core
solver instances before dedicating many cores to each SAT instance. Separate
formula-level parallelism from within-instance portfolio speedup.

## CPU cluster and GPU recommendation

The supplied SCRTP hardware snapshot lists 168-core AMD Genoa Blythe compute
nodes with 768 GB RAM, and GPU nodes with three L40 48 GB GPUs. Such CPU nodes
are a natural fit for independent-instance batches. These are saved-document
facts, not a live allocation or benchmark. The same snapshot gives Avon an
August 2026 expected end of life; confirm current site configuration before
creating submission scripts. No cluster access or SLURM work was attempted.

Published ParaFROST work supports GPU acceleration of inprocessing, and
FastFourierSAT supports parallel continuous/local-search kernels. Neither
establishes a universal GPU advantage for complete near-threshold random-CNF
decision. GPU searches can certify SAT via checked assignments but do not
turn failure to find one into UNSAT. Use CPU CDCL and proof checking for the
first diagram; consider GPUs later for batched witness searches or a separately
labelled solver-success diagram. Benchmark matched end-to-end verified-answer
cost, including transfers, restarts, CPU fallbacks and proof checking.

## Sources checked

- S002: supplied ALMT original, Figure 1/5 and Appendix A.1–A.3, printed
  pp. 226, 235, 273–274; [published article](https://doi.org/10.1093/imaiai/iau005).
- S025: Biere et al. (2024), Sections I and IV of the retained solver paper;
  [CaDiCaL repository](https://github.com/arminbiere/cadical).
- [PySAT solver API](https://pysathq.github.io/docs/html/api/solvers.html),
  accessed 2026-10-11: incremental interfaces, assumptions and model extraction;
  the actual calibration pins 1.9.dev15 / CaDiCaL 1.9.5.
- S027/S028: retained ParaFROST and published FastFourierSAT papers, plus
  their existing detailed source notes; no new GPU measurements.
- `scrtp/Hardware — scrtp-docs 0.1 documentation.html`, local saved original;
  hardware sections read 2026-10-11. Snapshot freshness was not established.
- The standard one-sample DKW–Massart bound is restated in Wei and Dudley,
  [Section 1, equation (1)](https://arxiv.org/html/1107.5356v2), arXiv
  1107.5356v2 (11 August 2011); that statement was checked. The original
  Massart (1990) paper was inaccessible through the browser. The numerical
  sample-size choices above are arithmetic consequences of the stated bound,
  not applications of the paper's different two-sample results.

[source_provenance.json](source_provenance.json) retains local source hashes
and visual page locators. In particular, the saved hardware HTML has SHA-256
`ebd980ccb3ebf8bef02ed668ed4b70581a9194e97df472cc3f6bd8a12378908c`.

**Next action:** agree a modest n-range and uncertainty target, run a longer
CPU/proof-checking pilot on the selected SCRTP node, and then prepare the
batch-generation and SLURM workflow from the supplied site documentation.
