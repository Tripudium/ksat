#!/usr/bin/env bash
#SBATCH --job-name=ksat-plots
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4096
#SBATCH --time=00:30:00
#
# Submit with sbatch from the repository root; see ../README.md for log paths.
# Usage: sbatch [options] plot_results.sbatch RUN_DIR OUTPUT_DIR [--allow-partial]
set -euo pipefail

[[ -n "${SLURM_JOB_ID:-}" ]] || {
    printf 'Submit this script with sbatch; result collection must run in a SLURM allocation.\n' >&2
    exit 1
}
project_dir=${KSAT_PROJECT_DIR:-${SLURM_SUBMIT_DIR:-}}
[[ -n "$project_dir" ]] || { printf 'KSAT_PROJECT_DIR or SLURM_SUBMIT_DIR must identify the repository.\n' >&2; exit 1; }
source "$project_dir/experiments/E002_blythe_phase_diagrams/slurm/common.sh"
[[ $# -ge 2 && $# -le 3 ]] || ksat_fail "Expected absolute RUN_DIR OUTPUT_DIR and optional --allow-partial."
run_dir=$1
output_dir=$2
[[ "$run_dir" = /* && -f "$run_dir/manifest.json" ]] || ksat_fail "RUN_DIR must be absolute and contain manifest.json."
[[ "$output_dir" = /* ]] || ksat_fail "OUTPUT_DIR must be absolute."
[[ ! -e "$output_dir" && ! -L "$output_dir" ]] || ksat_fail "OUTPUT_DIR already exists; choose a new analysis directory."
arguments=(--run-dir "$run_dir" --output "$output_dir")
if [[ $# -eq 3 ]]; then
    [[ "$3" = --allow-partial ]] || ksat_fail "Only --allow-partial is accepted after OUTPUT_DIR."
    arguments+=(--allow-partial)
fi

ksat_paths
ksat_modules
ksat_single_thread_libraries
ksat_venv
ksat_checker
ksat_environment_check
cd -- "$KSAT_PROJECT_DIR"
printf 'UTC start: %s\nHost: %s\nSLURM job: %s\nRun: %s\nOutput: %s\n' \
    "$(date -u +%FT%TZ)" "$(hostname)" "$SLURM_JOB_ID" "$run_dir" "$output_dir"

# Collection hashes retained CNFs, witnesses and proofs before plotting.
# Keep this potentially substantial filesystem/CPU work inside the allocation.
srun --ntasks=1 --cpus-per-task=1 \
    "$KSAT_PYTHON" "$KSAT_PROJECT_DIR/code/plot_ksat_phase.py" "${arguments[@]}"
printf 'UTC finish: %s\n' "$(date -u +%FT%TZ)"
