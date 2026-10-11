#!/usr/bin/env bash
# Run explicitly on the Blythe login node after cloning/pulling the project.
# Only this setup step may sync/download; compute jobs use prepared executables.
set -euo pipefail
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
source "$script_dir/common.sh"
ksat_paths
ksat_modules
ksat_single_thread_libraries

type uv >/dev/null 2>&1 || ksat_fail "uv is unavailable; install or load uv on the login node before setup."
compiler=${CC:-cc}
type "$compiler" >/dev/null 2>&1 || ksat_fail "C compiler unavailable: $compiler; load an available compiler module or set CC."
for project_file in pyproject.toml uv.lock .python-version; do
    [[ -r "$KSAT_PROJECT_DIR/$project_file" ]] || ksat_fail "Missing uv project file: $project_file"
done
checker_source="$KSAT_PROJECT_DIR/code/vendor/drat-trim/drat-trim.c"
[[ -r "$checker_source" ]] || ksat_fail "Missing vendored proof-checker source: $checker_source"
if [[ -e "$KSAT_ENV_DIR" && ! -f "$KSAT_ENV_DIR/pyvenv.cfg" ]]; then
    ksat_fail "Existing path is not a virtual environment: $KSAT_ENV_DIR"
fi
cd -- "$KSAT_PROJECT_DIR"
uv sync --locked
ksat_venv
"$KSAT_PYTHON" - "$checker_source" <<'PY'
import hashlib, pathlib, sys
actual = hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest()
expected = 'd834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee'
if actual != expected:
    raise SystemExit('Vendored drat-trim source does not match the pinned revision.')
PY

checker_target="$KSAT_ENV_DIR/bin/drat-trim"
checker_temp="$checker_target.build.$$"
trap 'rm -f -- "$checker_temp"' EXIT
"$compiler" -std=c99 -O2 "$checker_source" -o "$checker_temp"
mv -- "$checker_temp" "$checker_target"
trap - EXIT
export KSAT_DRAT_TRIM="$checker_target"
ksat_checker
"$KSAT_PYTHON" "$script_dir/environment_guard.py" record \
    --project "$KSAT_PROJECT_DIR" --environment "$KSAT_ENV_DIR" \
    --checker "$checker_target" --compiler "$compiler" --uv-version "$(uv --version)"
ksat_environment_check
printf 'Environment ready: %s\nChecker ready: %s\n' "$KSAT_ENV_DIR" "$KSAT_DRAT_TRIM"
printf 'Use the same optional KSAT_MODULES selection when submitting. Rerun setup after changing the uv project lock.\n'
