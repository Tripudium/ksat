#!/usr/bin/env bash
# Build a Blythe sbatch command. Default: print it; --submit actually submits.
set -euo pipefail
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
source "$script_dir/common.sh"

usage() {
    cat <<'USAGE'
Usage: bash submit_array.sh RUN_DIR [options]
  --submit                 Execute sbatch (otherwise print the command only).
  --cpus N                 CPU workers per array task, 1..168 (default: 16).
  --concurrency N          Maximum simultaneous array tasks (default: 4).
  --time HH:MM:SS           Wall limit <=48 hours (default: 00:45:00).
  --mem-per-cpu MB         Memory per CPU, 1..4591 (default: 2048).
  --account ACCOUNT       Optional actual account/share; no invented default.
  --retry-unknown          Retry recorded unknown outcomes; retain earlier attempts.
Environment: KSAT_MODULES (or KSAT_USE_CURRENT_ENV=1), KSAT_ENV_DIR,
             KSAT_DRAT_TRIM; optional KSAT_PROJECT_DIR, KSAT_ACCOUNT.
USAGE
}

[[ $# -ge 1 ]] || { usage; exit 2; }
if [[ "$1" = --help || "$1" = -h ]]; then usage; exit 0; fi
run_dir=$1; shift
cpus=16 concurrency=4 walltime=00:45:00 memory=2048 submit=0 retry=0
account=${KSAT_ACCOUNT:-}
while [[ $# -gt 0 ]]; do
    case "$1" in
        --submit) submit=1; shift ;;
        --retry-unknown) retry=1; shift ;;
        --cpus|--concurrency|--time|--mem-per-cpu|--account)
            [[ $# -ge 2 ]] || ksat_fail "Missing value after $1"
            case "$1" in
                --cpus) cpus=$2;; --concurrency) concurrency=$2;; --time) walltime=$2;;
                --mem-per-cpu) memory=$2;; --account) account=$2;;
            esac
            shift 2 ;;
        *) ksat_fail "Unknown option: $1" ;;
    esac
done
[[ "$cpus" =~ ^[1-9][0-9]*$ && "$cpus" -le 168 ]] || ksat_fail "--cpus must be 1..168."
[[ "$concurrency" =~ ^[1-9][0-9]*$ ]] || ksat_fail "--concurrency must be positive."
[[ "$memory" =~ ^[1-9][0-9]*$ && "$memory" -le 4591 ]] || ksat_fail "--mem-per-cpu must be 1..4591 MB."
[[ "$walltime" =~ ^([0-9]{1,2}):([0-9]{2}):([0-9]{2})$ ]] || ksat_fail "--time must have HH:MM:SS format."
hours=$((10#${BASH_REMATCH[1]})); minutes=$((10#${BASH_REMATCH[2]})); seconds=$((10#${BASH_REMATCH[3]}))
total_seconds=$((3600*hours+60*minutes+seconds))
[[ "$minutes" -lt 60 && "$seconds" -lt 60 && "$total_seconds" -gt 0 && "$total_seconds" -le 172800 ]] || ksat_fail "Invalid wall time or more than 48 hours."

ksat_paths
ksat_modules
ksat_venv
ksat_checker
[[ -d "$run_dir" ]] || ksat_fail "Run directory does not exist: $run_dir"
run_dir=$(cd -- "$run_dir" && pwd -P)
[[ -f "$run_dir/manifest.json" ]] || ksat_fail "Run plan missing: $run_dir/manifest.json"
num_chunks=$("$KSAT_PYTHON" - "$run_dir/manifest.json" <<'PY'
import json, sys
with open(sys.argv[1]) as stream:
    manifest = json.load(stream)
count = manifest.get('num_chunks')
if type(count) is not int or count < 1:
    raise SystemExit('manifest.num_chunks must be a positive integer')
print(count)
PY
)
mkdir -p -- "$run_dir/slurm-logs"
export KSAT_RETRY_UNKNOWN=$retry
last_chunk=$((num_chunks-1))
command=(sbatch --parsable --partition=compute --nodes=1 --ntasks=1
    "--cpus-per-task=$cpus" "--mem-per-cpu=$memory" "--time=$walltime"
    "--array=0-$last_chunk%$concurrency" "--chdir=$KSAT_PROJECT_DIR"
    "--output=$run_dir/slurm-logs/%A_%a.out" "--error=$run_dir/slurm-logs/%A_%a.err"
    --export=ALL)
if [[ -n "$account" ]]; then command+=("--account=$account"); fi
command+=("$script_dir/run_array.sbatch" "$run_dir")
printf 'Planned %s chunks, at most %s concurrent tasks x %s CPUs.\n' "$num_chunks" "$concurrency" "$cpus"
printf 'Command: '; printf '%q ' "${command[@]}"; printf '\n'
if [[ "$submit" = 1 ]]; then
    type sbatch >/dev/null 2>&1 || ksat_fail "sbatch is unavailable; execute submission on the Blythe login node."
    "${command[@]}"
else
    printf 'Dry run only. Add --submit to submit this command on Blythe.\n'
fi
