# Independent runner review

- Reviewer: `analytic_transfer` agent, independently of the runner's author/coordinator.
- Date: 2026-10-11.
- Reviewed source: `code/ksat_experiments.py`.
- Reviewed SHA-256: `197799ce3762883f03c64f06593bbe439823d3574c492391694bfdbdd7d5b1d0`.
- Method: source inspection, mathematical checking of sampling and classification logic, and review of the changes addressing the earlier findings. This reviewer did not edit the runner, execute its solver/checker campaign, or submit cluster jobs.
- Verdict: **No remaining consequential ensemble or outcome-classification error identified in the reviewed runner source, within the scope and trust assumptions below.** This is a scoped software/scientific review, not formal verification or validation of target-cluster performance.

## Sampling and reproducibility

The generator selects distinct variables with a sparse partial Fisher–Yates procedure: at each step it draws from the remaining index range and replaces the selected entry with the current last entry. The dictionary update preserves that invariant, including selections of the last entry and k=n. Given uniform input words, rejection before reduction modulo the bound removes modulo bias, and the subsequent draws modulo two give fair literal signs. The dictionary resets per clause, so whole clauses can repeat. There is no conditioning on SAT, planted assignment, variable coverage, solver success or previously observed outcomes.

The implementation uses a specified SHA-256 counter stream, with 32-byte seed, 8-byte big-endian counter and first 8 digest bytes. Its instance-ID namespace explicitly changes to `proper-kcnf-sha256-v1`, separating it from the earlier Python-random generator. The deterministic byte-level operations avoid dependence on Python's sampling-algorithm version. This is pseudorandom simulation; the review does not claim that fixed SHA-256 outputs are mathematically independent random variables.

Instance IDs depend on base seed, k, n, integer m and replicate. They do not depend on scheduling order or worker count. The manifest identifies an independent grid rather than coupled hitting-time paths. Exact integer arithmetic on a decimal's integer ratio now computes floor(alpha*n), fixing the previously demonstrated context-rounding error for long decimal strings. Duplicate integer clause counts are rejected for each n. The manifest's reconstructed instance grid and chunk count are checked; the runner hash is pinned, and planning preserves a source snapshot. Exact density is determined by integer n and m; `alpha_actual` is a floating-point display value.

## Outcomes and certificates

The child rejects unexpected non-Boolean solver answers. A SAT outcome is upgraded only after explicit integer clause evaluation checks a consistent, in-range model. Missing variable assignments are acceptable only when every clause already has an assigned true literal; such a partial model extends to a total satisfying assignment. This also treats the empty formula correctly.

A timeout or supervisor interruption is recorded as unknown. A solver failure remains an error. A bare UNSAT report or failed/timed-out certificate check remains `UNSAT-unchecked`, not a certified outcome. Positive verification requires completed checking, exit code zero and an explicit `s VERIFIED` verdict. The negative preflight control now requires completion, exit code one and explicit `s NOT VERIFIED`; a crash or timeout cannot masquerade as a successful rejection. Essential preflight solver calls and checks no longer depend on Python assertions, so optimization mode cannot remove them.

The Glucose 4.2 label and solver construction agree. This review does not transfer the historical E001 CaDiCaL runtime measurements into Glucose performance claims. Coordinator-run preflight and smoke/exhaustive checks are separate validation evidence; they are not represented here as executions performed by this reviewer.

## Resume, duplicates and retained evidence

Per-instance nonblocking filesystem locks prevent simultaneous attempts through this runner. Completed JSON records are published by atomic hard-link creation without overwriting a prior record. New attempts use distinct directories, retaining earlier outcomes and artifacts. Prior result identities and manifest hashes are checked; retained input/witness/proof hashes are rechecked before accepting those records. Conflicting verified statuses cause an error. Verified instances are skipped, while unresolved instances require an explicit retry option; retries verify that regenerated CNF hashes match earlier recorded input.

The manifest retains every planned replicate. Skipped, locked, not-started, errored and unknown cases must still be included appropriately by the collector; this runner review does not independently validate the collector's denominators or confidence intervals. Abrupt interruption before a final result leaves its immutable started record and any partial artifacts for diagnosis and later retry.

## Resource and signal handling

In run mode, SIGINT/SIGTERM set a stop event. Active child supervision checks it repeatedly, kills the corresponding process group, reaps the process and records interruption. Queued instances observe the event before starting. The finally block cleans up a still-running child; a race in which the process group has already exited is handled. This fixes the previous ordinary-termination orphaning path. SIGKILL, node loss and filesystem failure remain outside graceful-shutdown guarantees; a completed result must not be inferred from a started record.

Solver and checker processes have separately configured wall-time limits. Address-space limits are applied on Linux and explicitly recorded as unenforced on other platforms. Generator work, parent-side artifact hashing and supervisor memory are not covered by those child limits. Allocation sizing therefore still needs headroom, and cluster wall limits must account for the whole workflow. The standalone preflight does not install run mode's signal handler; its tiny fixed controls and separately supervised checker are a narrower operational path.

## Trust and scope limitations

The trusted computational components include Python, the sampler implementation, the solver-to-DIMACS/proof interface, the pinned DRAT-trim source and compiled binary, the operating system, and filesystem behavior. Recording hashes and validating positive/negative controls does not formally verify those components. Target-node memory limits, network-filesystem lock/hard-link behavior and SLURM signal delivery require the planned cluster validation; they were not exercised by this review.

Inspection of the retained upstream checker found a conservative edge case: its trivial-input-UNSAT branch may print `s VERIFIED` while returning one. The runner will leave such a result unchecked, never upgrade it falsely. The generated proper k>=2 inputs contain no empty or unit clauses and therefore do not enter that initial trivial-UNSAT path. The upstream source was preserved. This observation does not authorize treating exit-one verdicts as verified.

The review does not establish statistical independence beyond the documented pseudorandom simulation convention, unbiased estimation after arbitrary external selection of runs, a feasible maximum n, or any concentration theorem. Any substantive runner change after the recorded hash reopens the affected review.
