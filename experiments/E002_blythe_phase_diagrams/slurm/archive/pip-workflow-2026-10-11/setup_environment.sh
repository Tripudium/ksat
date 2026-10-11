#!/usr/bin/env bash
# Run explicitly on Blythe before submission. Installs only into the selected venv.
# This script is supplied for the user to run; preparation does not execute it.
set -euo pipefail
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
source "$script_dir/common.sh"
ksat_paths
ksat_modules
ksat_single_thread_libraries

base_python=${KSAT_BASE_PYTHON:-python3}
compiler=${CC:-cc}
type "$base_python" >/dev/null 2>&1 || ksat_fail "Python executable unavailable: $base_python"
type "$compiler" >/dev/null 2>&1 || ksat_fail "C compiler unavailable: $compiler; load a compatible compiler module."
"$base_python" -c 'import sys; assert sys.version_info >= (3, 10), "Select a Python >=3.10 module"'
requirements="$KSAT_PROJECT_DIR/experiments/E002_blythe_phase_diagrams/requirements.txt"
checker_source="$KSAT_PROJECT_DIR/code/vendor/drat-trim/drat-trim.c"
[[ -r "$requirements" ]] || ksat_fail "Missing pinned requirements: $requirements"
[[ -r "$checker_source" ]] || ksat_fail "Missing vendored proof-checker source: $checker_source"
"$base_python" - "$checker_source" <<'PY'
import hashlib, pathlib, sys
actual = hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest()
expected = 'd834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee'
if actual != expected:
    raise SystemExit('Vendored drat-trim source does not match the pinned revision.')
PY

if [[ -e "$KSAT_ENV_DIR" && ! -f "$KSAT_ENV_DIR/pyvenv.cfg" ]]; then
    ksat_fail "Existing path is not a virtual environment: $KSAT_ENV_DIR"
fi
if [[ ! -d "$KSAT_ENV_DIR" ]]; then "$base_python" -m venv "$KSAT_ENV_DIR"; fi
ksat_venv
"$KSAT_PYTHON" -m pip install --disable-pip-version-check --requirement "$requirements"

checker_target="$KSAT_ENV_DIR/bin/drat-trim"
checker_temp="$checker_target.build.$$"
trap 'rm -f -- "$checker_temp"' EXIT
"$compiler" -std=c99 -O2 "$checker_source" -o "$checker_temp"
mv -- "$checker_temp" "$checker_target"
trap - EXIT
export KSAT_DRAT_TRIM="$checker_target"
ksat_checker

# Preserve dated setup provenance if setup is repeated after an environment change.
setup_record="$KSAT_ENV_DIR/setup-$(date -u +%Y%m%dT%H%M%SZ)-$$.json"
"$KSAT_PYTHON" - "$requirements" "$checker_source" "$checker_target" "$setup_record" "$compiler" <<'PY'
from datetime import datetime, timezone
import hashlib, importlib.metadata, json, os, pathlib, platform, subprocess, sys
requirements, source, binary, output, compiler = map(str, sys.argv[1:])
sha = lambda path: hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
record = {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'python': sys.version, 'python_executable': sys.executable,
    'platform': platform.platform(),
    'packages': {name: importlib.metadata.version(name)
                 for name in ('python-sat', 'six', 'matplotlib')},
    'pip_freeze': subprocess.run([sys.executable, '-m', 'pip', 'freeze'],
                                 text=True, capture_output=True, check=True).stdout,
    'module_selection': os.environ.get('KSAT_MODULES', ''),
    'use_current_environment': os.environ.get('KSAT_USE_CURRENT_ENV', '0'),
    'requirements_sha256': sha(requirements),
    'drat_trim_upstream_commit': '2e3b2dc0ecf938addbd779d42877b6ed69d9a985',
    'drat_trim_source_sha256': sha(source), 'drat_trim_binary_sha256': sha(binary),
    'compiler': compiler, 'compiler_flags': ['-std=c99', '-O2'],
    'compiler_version': subprocess.run([compiler, '--version'], text=True,
                                      capture_output=True, check=False).stdout,
    'proof_checker_preflight': 'Not run here; run_array.sbatch performs it inside the allocation.',
}
with open(output, 'x') as stream:
    json.dump(record, stream, indent=2); stream.write('\n')
print(output)
PY
printf 'Environment ready: %s\nChecker ready: %s\n' "$KSAT_ENV_DIR" "$KSAT_DRAT_TRIM"
printf 'Use the same KSAT_MODULES (or prepared shell) when planning and submitting.\n'
