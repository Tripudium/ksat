#!/usr/bin/env bash
#SBATCH --job-name=ksat-phase
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=2048
#SBATCH --time=00:45:00
#
# Use submit_array.sh to supply array range, existing log directories and paths.
# One SLURM task owns a Python pool, with one complete-solver process per worker.
set -euo pipefail

project_dir=${KSAT_PROJECT_DIR:-${SLURM_SUBMIT_DIR:-}}
[[ -n "$project_dir" ]] || { printf 'KSAT_PROJECT_DIR or SLURM_SUBMIT_DIR must identify the repository.\n' >&2; exit 1; }
source "$project_dir/experiments/E002_blythe_phase_diagrams/slurm/common.sh"
ksat_paths
ksat_modules
ksat_venv
ksat_checker
ksat_single_thread_libraries

[[ $# -eq 1 ]] || ksat_fail "Expected one absolute RUN_DIR argument from submit_array.sh."
run_dir=$1
[[ "$run_dir" = /* && -f "$run_dir/manifest.json" ]] || ksat_fail "RUN_DIR must be absolute and contain manifest.json."
[[ "${SLURM_ARRAY_TASK_ID:-}" =~ ^[0-9]+$ ]] || ksat_fail "This script must run as a SLURM array task."
[[ "${SLURM_CPUS_PER_TASK:-}" =~ ^[1-9][0-9]*$ ]] || ksat_fail "SLURM_CPUS_PER_TASK must be set."
[[ "$SLURM_CPUS_PER_TASK" -le 168 ]] || ksat_fail "This pool uses one Blythe compute node, at most 168 CPUs."
cd -- "$KSAT_PROJECT_DIR"
mkdir -p -- "$run_dir/slurm-logs"
identity="${SLURM_ARRAY_JOB_ID:-${SLURM_JOB_ID:-manual}}_${SLURM_ARRAY_TASK_ID}_${SLURM_RESTART_COUNT:-0}_$$"
printf 'UTC start: %s\nHost: %s\nProject: %s\nRun: %s\nChunk: %s\nWorkers: %s\n' \
    "$(date -u +%FT%TZ)" "$(hostname)" "$KSAT_PROJECT_DIR" "$run_dir" \
    "$SLURM_ARRAY_TASK_ID" "$SLURM_CPUS_PER_TASK"
if type module >/dev/null 2>&1; then module list 2>&1; fi

# Preflight is deliberately performed inside the allocation, not on a login CPU.
srun --ntasks=1 --cpus-per-task=1 "$KSAT_PYTHON" "$KSAT_PIPELINE" preflight \
    --drat-trim "$KSAT_DRAT_TRIM" --output "$run_dir/slurm-logs/preflight-$identity.json"
arguments=(run --run-dir "$run_dir" --chunk-id "$SLURM_ARRAY_TASK_ID"
    --workers "$SLURM_CPUS_PER_TASK" --drat-trim "$KSAT_DRAT_TRIM")
if [[ "${KSAT_RETRY_UNKNOWN:-0}" = 1 ]]; then arguments+=(--retry-unknown); fi
srun --ntasks=1 --cpus-per-task="$SLURM_CPUS_PER_TASK" \
    "$KSAT_PYTHON" "$KSAT_PIPELINE" "${arguments[@]}"
printf 'UTC finish: %s\n' "$(date -u +%FT%TZ)"
