#!/usr/bin/env bash
# Shared setup. Sourcing this file does not install software or submit jobs.

ksat_fail() { printf 'Error: %s\n' "$*" >&2; exit 1; }

ksat_paths() {
    local source_dir default_project
    source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
    default_project=$(cd -- "$source_dir/../../.." && pwd -P)
    KSAT_PROJECT_DIR=${KSAT_PROJECT_DIR:-$default_project}
    [[ -d "$KSAT_PROJECT_DIR" ]] || ksat_fail "Project directory does not exist: $KSAT_PROJECT_DIR"
    KSAT_PROJECT_DIR=$(cd -- "$KSAT_PROJECT_DIR" && pwd -P)
    KSAT_ENV_DIR=${KSAT_ENV_DIR:-"$KSAT_PROJECT_DIR/.venv"}
    [[ "$KSAT_ENV_DIR" = /* ]] || KSAT_ENV_DIR="$KSAT_PROJECT_DIR/$KSAT_ENV_DIR"
    KSAT_PIPELINE="$KSAT_PROJECT_DIR/code/ksat_experiments.py"
    [[ -f "$KSAT_PIPELINE" ]] || ksat_fail "Missing experiment pipeline: $KSAT_PIPELINE"
    export KSAT_PROJECT_DIR KSAT_ENV_DIR UV_PROJECT_ENVIRONMENT="$KSAT_ENV_DIR"
}

ksat_modules() {
    # uv can provision Python during setup. Site modules are optional, e.g. GCC.
    if [[ -n "${KSAT_MODULES:-}" ]]; then
        type module >/dev/null 2>&1 || ksat_fail "The module command is unavailable in this shell."
        module purge
        local -a requested_modules
        read -r -a requested_modules <<< "$KSAT_MODULES"
        module load "${requested_modules[@]}"
    fi
    export KSAT_MODULES="${KSAT_MODULES:-}"
}

ksat_venv() {
    KSAT_PYTHON="$KSAT_ENV_DIR/bin/python"
    [[ -x "$KSAT_PYTHON" ]] || ksat_fail "Missing virtual-environment Python: $KSAT_PYTHON; run setup_environment.sh first."
    "$KSAT_PYTHON" -c 'import sys; assert sys.version_info[:2] == (3, 12), "The project requires Python 3.12"'
}

ksat_environment_check() {
    "$KSAT_PYTHON" "$KSAT_PROJECT_DIR/experiments/E002_blythe_phase_diagrams/slurm/environment_guard.py" \
        check --project "$KSAT_PROJECT_DIR" --environment "$KSAT_ENV_DIR" --checker "$KSAT_DRAT_TRIM"
}

ksat_checker() {
    KSAT_DRAT_TRIM=${KSAT_DRAT_TRIM:-"$KSAT_ENV_DIR/bin/drat-trim"}
    [[ "$KSAT_DRAT_TRIM" = /* ]] || KSAT_DRAT_TRIM="$KSAT_PROJECT_DIR/$KSAT_DRAT_TRIM"
    [[ -x "$KSAT_DRAT_TRIM" ]] || ksat_fail "Checker is not executable: $KSAT_DRAT_TRIM"
    export KSAT_DRAT_TRIM
}

ksat_single_thread_libraries() {
    export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
    export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
    export PYTHONUNBUFFERED=1 PYTHONNOUSERSITE=1
}
