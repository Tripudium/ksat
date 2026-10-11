# Blythe documentation used for E002

**Read:** 2026-10-11. **Scope:** saved SCRTP HTML supplied in `scrtp/`.
These are documented settings, not a live cluster inspection or allocation.
No connection, package installation on Blythe, or job submission was performed
while preparing the scripts.

## Settings supported by the supplied pages

| Setting | Documentation and implication |
| --- | --- |
| Execution mode | “HPC clusters FAQ”, How does HPC differ from a standard computer: calculations normally run unattended through the batch queue; long calculations should not routinely use interactive sessions. The user explicitly requires E002's larger computations to use non-interactive SLURM. Both experiment arrays and result collection now have batch scripts. |
| CPU partition | “SLURM concepts (HPC)”, Partition: default `compute`; scripts name it explicitly. |
| CPU nodes | “Hardware”, Blythe / Compute nodes: two 84-core AMD 9634 Genoa processors, 168 cores total, 768 GB physical RAM. |
| CPU task resources | “Blythe job scripts”: one task using multiple CPUs is `--nodes=1 --ntasks-per-node=1 --cpus-per-task=N`; a Python child-process pool uses the same resource pattern. |
| Memory request limit | “Blythe job scripts” and “Resource limits and job priority”, Standard compute nodes: 4591 MB per CPU maximum. |
| Wall time | “Resource limits and job priority”, Standard compute nodes: 48 hours maximum. |
| Short jobs | Same page, Development queues / Blythe: no dedicated development queue; jobs shorter than an hour receive higher priority. This is a documented scheduling preference, not a queue-time guarantee. |
| Project files | “Files and storage”, Home directory / Blythe: project work is intended for `/springbrook/share/<group>`; group is the user's real HPC share. New shared data goes to SSD, with later automatic tiering. |
| Home directory | Same page: `/springbrook/home/<first-letter>/<username>`. It is not assumed to contain the uploaded project. |
| Scratch and desktop mounts | The special `/scratch` instructions and `/desktop` mounts concern Avon; they are not hard-coded for Blythe. Runs use the shared project filesystem. |
| Module initialization | “Blythe job scripts” recommends `module purge`, then the modules required by the application. Its GCC/13.3.0 example concerns compiled OpenMP code, not a verified Python environment. |
| Submission directory | “Blythe job scripts” says jobs inherit the submission working directory. The helper additionally passes `--chdir` and exports an absolute project path; the worker accepts an absolute run path. |
| Output | “Submitting and managing jobs”, Job output: use `--output` and `--error` to choose log files. The helper creates their parent directory before invoking `sbatch`. |
| Accounts and limits | The saved examples omit a universal `--account` requirement. The scripts accept a real supplied account/share, but invent none. Node-per-job and node-per-user entries for Blythe are `??`; the scripts use one node per task and an adjustable small array concurrency. |

The default request is **16 CPUs × at most 4 concurrent array tasks**, 2048 MB
per CPU, and 45 minutes per task. These are conservative initial experiment
choices, not site requirements or a measured optimal configuration. One Python
pool uses the task's allocated CPUs, with BLAS/OpenMP libraries set to one thread
per process. No GPU resource is requested for the complete-decision baseline.

## Information not available in the saved material

The Blythe example index lists CPU “Python jobs (serial)” and “Python
multiprocessing”, but their content was not among the supplied HTML pages.
The linked official pages could not be fetched through the browsing tool:

- `https://docs.scrtp.warwick.ac.uk/hpc-pages/blythe-slurm-examples/blythe-python.html`
- `https://docs.scrtp.warwick.ac.uk/hpc-pages/blythe-slurm-examples/blythe-multiprocessing.html`

Consequently no site Python module/version or compiler/Python module combination
is invented. The initial pip delivery required a user-selected Python >=3.10
module environment; its scripts and instructions are preserved in
[the archive](slurm/archive/pip-workflow-2026-10-11/).

The subsequent [uv workflow](slurm/README.md) uses the root Python 3.12
selection and `uv.lock`. uv can provision Python during login-node setup;
`KSAT_MODULES` is optional for available site/compiler modules. A C compiler
is still required for the vendored checker. Submission and workers check the
prepared environment against the lock and recorded packages/checker. This
software choice does not supply the missing site documentation or establish
that the workflow has run on Blythe.

The GPU multiprocessing example has a prose sentence mentioning 168 CPUs while
its actual GPU batch directives request 30 CPUs. E002 follows the consistent
CPU compute-node specification instead of copying that GPU prose.

## Safety and reproducibility relevant to this workload

The saved storage documentation explicitly states there is no GPFS backup or
disaster recovery, and warns about excessive tiny-file workloads. Keep result
chunks moderate, retain source/input hashes and certificates, and archive completed
results outside the live cluster filesystem. The scripts do not remove results
or certificates, scrape the scheduler repeatedly, or auto-submit follow-up jobs.
The checker is compiled from vendored source at upstream commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; the root pipeline records the
actual binary hash and runs positive/negative proof-checker preflight in each
allocation before experimental work.

## Snapshot hashes

Each filename below is in `scrtp/` and has suffix
` — scrtp-docs 0.1 documentation.html`.

| File stem | SHA-256 |
| --- | --- |
| Hardware | `ebd980ccb3ebf8bef02ed668ed4b70581a9194e97df472cc3f6bd8a12378908c` |
| Blythe job scripts | `23a5da54c6fd111f044d661edbd5b599ade8e82b62ee1126d8fd685531a9ea4d` |
| SLURM concepts (HPC) | `c1431d67fd33a7633756a8f7e690edd1816e7799c7504e0b872bb7b5a0516fbc` |
| Resource limits and job priority | `9007200a7de652a06e7b5c4c829a67aaaeca18a09eeff239ed43a4047361e9b9` |
| Files and storage | `b538b8c458197e9391243a262a6143e872c3ba48b346018a0209c03a314b08a8` |
| Submitting and managing jobs | `32c001361a3e16b29e4701ad6c517b8094339d755345b35c6f3636a8878b1b54` |
| Blythe | `49ae3e24fa102e51c6528e2f6387bbbfb964b93bf6ae797bfc926448c0cb6dc1` |
| Python multiprocessing pool with GPUs | `2b161d1a6cacb0e6da2266f4b21bd2957bd174554a6b51dc38e31985d2750b0f` |
| HPC clusters FAQ | `ed06744c13338441d64db0af7b5c83d2557304d65e1e89798f23d77e711a37cd` |
