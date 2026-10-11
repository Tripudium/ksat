#!/usr/bin/env python3
"""Independent-grid proper random k-SAT experiments, with retained certificates.

Planning uses only the Python standard library. Solving needs python-sat;
certified UNSAT needs the pinned DRAT-trim executable. See E002/README.md.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from decimal import Decimal
import fcntl
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import resource
import signal
import subprocess
import sys
import tempfile
import threading
import time
import uuid

SCHEMA = 1
SCRIPT = Path(__file__).resolve()
VERIFIED = {'SAT-verified', 'UNSAT-verified'}
STOP = threading.Event()
IDENTITY = ('id', 'n', 'k', 'm', 'alpha_requested', 'alpha_actual',
            'replicate', 'seed', 'chunk_id')


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def atomic_json(path, value):
    """Publish a complete JSON file, refusing to replace an existing record."""
    path = Path(path)
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    with temp.open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    try:
        os.link(temp, path)  # Atomic, fails if destination exists.
    finally:
        temp.unlink()


def validate_config(c):
    required = {'name', 'k', 'n_values', 'alpha_values', 'repetitions', 'base_seed',
                'chunk_size', 'solve_timeout_seconds', 'check_timeout_seconds',
                'memory_mb', 'proof_policy'}
    if set(c) != required:
        raise ValueError(f'Config keys: missing {required-set(c)}, extra {set(c)-required}')
    if not isinstance(c['name'], str) or not c['name'].strip():
        raise ValueError('name must be nonempty')
    for key in ('k', 'repetitions', 'chunk_size', 'memory_mb'):
        if type(c[key]) is not int or c[key] <= 0:
            raise ValueError(f'{key} must be a positive integer')
    if c['k'] < 2 or c['memory_mb'] < 256:
        raise ValueError('Require k >= 2 and memory_mb >= 256')
    if type(c['base_seed']) is not int or c['base_seed'] < 0:
        raise ValueError('base_seed must be a nonnegative integer')
    if not c['n_values'] or any(type(n) is not int or not c['k'] <= n < 2**31 for n in c['n_values']):
        raise ValueError('Require k <= n < 2^31')
    if len(set(c['n_values'])) != len(c['n_values']):
        raise ValueError('Duplicate n')
    if not c['alpha_values'] or any(not isinstance(a, str) for a in c['alpha_values']):
        raise ValueError('alpha_values must be nonempty decimal strings')
    alphas = [Decimal(a) for a in c['alpha_values']]
    if any(not a.is_finite() or a < 0 for a in alphas):
        raise ValueError('Densities must be finite and nonnegative')
    for n in c['n_values']:
        ms = [clause_count(a, n) for a in alphas]
        if len(set(ms)) != len(ms):
            raise ValueError(f'Densities give duplicate integer clause counts at n={n}')
    for key in ('solve_timeout_seconds', 'check_timeout_seconds'):
        if type(c[key]) not in (int, float) or not math.isfinite(c[key]) or c[key] <= 0:
            raise ValueError(f'{key} must be finite and positive')
    if c['proof_policy'] not in ('required', 'solver_only'):
        raise ValueError('proof_policy must be required or solver_only')
    return c


def clause_count(alpha, n):
    numerator, denominator = Decimal(alpha).as_integer_ratio()
    return numerator*n//denominator


def instance_grid(c):
    rows = []
    for n in sorted(c['n_values']):
        for alpha in sorted(c['alpha_values'], key=Decimal):
            m = clause_count(alpha, n)
            for rep in range(c['repetitions']):
                key = f'proper-kcnf-sha256-v1:{c["base_seed"]}:{c["k"]}:{n}:{m}:{rep}'
                hashed = hashlib.sha256(key.encode()).hexdigest()
                rows.append(dict(id=hashed, n=n, k=c['k'], m=m,
                                 alpha_requested=alpha, alpha_actual=m/n,
                                 replicate=rep, seed=int(hashed, 16),
                                 chunk_id=len(rows)//c['chunk_size']))
    return rows


def plan(config, output):
    c = validate_config(json.loads(Path(config).read_text()))
    rows = instance_grid(c)
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    for name in ('attempts', 'chunks', 'logs', 'locks', 'source'):
        (output/name).mkdir()
    (output/'source'/SCRIPT.name).write_bytes(SCRIPT.read_bytes())
    atomic_json(output/'manifest.json', dict(
        schema_version=SCHEMA, created_utc=now(), experiment_id='E002',
        config=c, instances=rows, num_chunks=(len(rows)+c['chunk_size']-1)//c['chunk_size'],
        generator='sha256-counter-v1: 256-bit seed, 64-bit big-endian counter, first 64 digest bits; rejection randbelow; partial Fisher-Yates; fair sign draws',
        coupling='Independent pseudorandom streams for each (base_seed,k,n,m,replicate); not coupled T_n paths',
        script_sha256=digest(SCRIPT), planning_python=sys.version,
        config_sha256=digest(config)))
    print(json.dumps({'run_dir': str(output), 'instances': len(rows),
                      'num_chunks': (len(rows)+c['chunk_size']-1)//c['chunk_size']}))


class HashRNG:
    """Versioned pseudorandom stream, independent of Python random.sample versions."""
    def __init__(self, seed):
        self.seed = seed.to_bytes(32, 'big')
        self.counter = 0

    def below(self, bound):
        limit = 2**64 - (2**64 % bound)
        while True:
            word = hashlib.sha256(self.seed + self.counter.to_bytes(8, 'big')).digest()[:8]
            self.counter += 1
            value = int.from_bytes(word, 'big')
            if value < limit:
                return value % bound


def clauses_for(row):
    rng = HashRNG(row['seed'])
    for _ in range(row['m']):
        swaps, variables = {}, []
        for i in range(row['k']):
            j = rng.below(row['n']-i)
            variables.append(swaps.get(j, j)+1)
            swaps[j] = swaps.get(row['n']-i-1, row['n']-i-1)
        yield [v if rng.below(2) else -v for v in variables]


def write_cnf(path, n, clauses):
    clauses = list(clauses)
    with Path(path).open('x') as f:
        f.write(f'p cnf {n} {len(clauses)}\n')
        for clause in clauses:
            f.write(' '.join(map(str, clause)) + ' 0\n')


def verify_model(n, clauses, model):
    if not isinstance(model, list) or any(type(x) is not int or x == 0 or abs(x) > n for x in model):
        return False
    if len({abs(x) for x in model}) != len(model):
        return False
    assigned = set(model)
    return all(any(x in assigned for x in clause) for clause in clauses)


def impose_memory_limit(memory_mb):
    # RLIMIT_AS is effective on Linux; macOS does not provide equivalent semantics.
    if sys.platform.startswith('linux'):
        cap = int(memory_mb)*1024*1024
        resource.setrlimit(resource.RLIMIT_AS, (cap, cap))


def solve_child(cnf_path, attempt, memory_mb, proof):
    impose_memory_limit(memory_mb)
    from pysat.formula import CNF
    from pysat.solvers import Glucose42
    formula = CNF(from_file=str(cnf_path))
    begun = time.perf_counter()
    with Glucose42(bootstrap_with=formula.clauses, with_proof=proof, use_timer=True) as solver:
        answer = solver.solve()
        if answer is not True and answer is not False:
            raise RuntimeError('Solver returned neither SAT nor UNSAT')
        raw = dict(solver_answer='SAT' if answer else 'UNSAT',
                   solve_cpu_seconds=solver.time(),
                   solver_stats=solver.accum_stats())
        if answer:
            atomic_json(attempt/'witness.json', solver.get_model() or [])
        elif proof:
            with (attempt/'proof.drat').open('x') as f:
                for line in solver.get_proof():
                    f.write(line+'\n')
        raw['setup_solve_serialize_wall_seconds'] = time.perf_counter()-begun
    raw['max_rss_platform_units'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    atomic_json(attempt/'solver.json', raw)


def run_process(command, timeout, log):
    begun = time.perf_counter()
    with Path(log).open('xb') as f:
        if STOP.is_set():
            return dict(returncode=-signal.SIGTERM, timeout=False, interrupted=True, wall_seconds=0)
        process = subprocess.Popen(command, stdout=f, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        expired = False
        interrupted = False
        try:
            while process.poll() is None:
                remaining = timeout-(time.perf_counter()-begun)
                if STOP.is_set() or remaining <= 0:
                    interrupted, expired = STOP.is_set(), not STOP.is_set()
                    kill_group(process.pid)
                    break
                try:
                    process.wait(timeout=min(0.2, remaining))
                except subprocess.TimeoutExpired:
                    pass
        finally:
            if process.poll() is None:
                kill_group(process.pid)
            code = process.wait()
    return dict(returncode=code, timeout=expired, interrupted=interrupted,
                wall_seconds=time.perf_counter()-begun)


def kill_group(pid):
    try:
        os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def check_proof(checker, cnf, proof, timeout, memory_mb, log):
    result = run_process([sys.executable, str(SCRIPT), '_check', '--memory-mb', str(memory_mb),
                          '--checker', str(checker), '--cnf', str(cnf), '--proof', str(proof)],
                         timeout, log)
    # Some checker error/memory branches return zero. A positive verdict is essential.
    with Path(log).open(errors='replace') as f:
        verdicts = {line.strip() for line in f if line.strip().startswith('s ')}
    completed = not result['timeout'] and not result['interrupted']
    result['verified'] = completed and result['returncode'] == 0 and 's VERIFIED' in verdicts
    result['rejected'] = completed and result['returncode'] == 1 and 's NOT VERIFIED' in verdicts
    return result


def environment(checker=None):
    import pysolvers
    return dict(recorded_utc=now(), python=sys.version, executable=sys.executable,
                platform=platform.platform(), machine=platform.machine(), hostname=platform.node(),
                python_sat=importlib.metadata.version('python-sat'),
                dependencies={p.metadata['Name']: p.version for p in importlib.metadata.distributions()},
                solver='Glucose 4.2 via Glucose42, default options, single-thread process',
                solver_extension_sha256=digest(pysolvers.__file__),
                script_sha256=digest(SCRIPT), checker=str(checker) if checker else None,
                checker_sha256=digest(checker) if checker else None,
                memory_limit='RLIMIT_AS' if sys.platform.startswith('linux') else 'not enforced on this platform',
                slurm={k:v for k,v in os.environ.items() if k.startswith('SLURM_')},
                threads={k:os.environ.get(k) for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')})


def evaluate_instance(row, run_dir, config, checker, manifest_hash, provenance_path, retry_unknown=False):
    if STOP.is_set():
        return {'id':row['id'], 'status':'not-started-interruption'}
    lock_path = run_dir/'locks'/row['id']
    with lock_path.open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {'id':row['id'], 'status':'locked-by-another-task'}
        parent = run_dir/'attempts'/row['id']
        parent.mkdir(exist_ok=True)
        previous = [json.loads(p.read_text()) for p in parent.glob('*/result.json')]
        for result in previous:
            if result['manifest_sha256'] != manifest_hash or any(result[k] != row[k] for k in IDENTITY):
                raise ValueError('Existing result does not match manifest')
            for artifact in ('input', 'witness', 'proof'):
                if artifact in result:
                    path = (run_dir/result[artifact]).resolve()
                    if not path.is_relative_to(run_dir) or digest(path) != result[artifact+'_sha256']:
                        raise ValueError(f'Changed or missing retained artifact: {artifact}')
        confirmed = {r['status'] for r in previous if r['status'] in VERIFIED}
        if len(confirmed) > 1:
            raise ValueError('Conflicting verified outcomes; inspect retained certificates')
        if confirmed or (previous and not retry_unknown):
            return {'id': row['id'], 'status':'already-recorded'}
        attempt_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'-'+uuid.uuid4().hex
        attempt = parent/attempt_id
        attempt.mkdir()
        result = dict(row, schema_version=SCHEMA, attempt_id=attempt_id, started_utc=now(),
                      manifest_sha256=manifest_hash, provenance=str(provenance_path.relative_to(run_dir)),
                      status='error', reason='not completed', proof_policy=config['proof_policy'])
        atomic_json(attempt/'started.json', result)
        begun = time.perf_counter()
        try:
            clauses = list(clauses_for(row))
            cnf = attempt/'input.cnf'
            write_cnf(cnf, row['n'], clauses)
            result.update(input=str(cnf.relative_to(run_dir)), input_sha256=digest(cnf))
            if any(r.get('input_sha256', result['input_sha256']) != result['input_sha256'] for r in previous):
                raise ValueError('Regenerated input differs from an earlier attempt')
            command = [sys.executable, str(SCRIPT), '_solve', '--cnf', str(cnf),
                       '--attempt', str(attempt), '--memory-mb', str(config['memory_mb'])]
            if config['proof_policy'] == 'required':
                command.append('--proof')
            proc = run_process(command, config['solve_timeout_seconds'], attempt/'solver.log')
            result['solver_process'] = proc
            if proc['interrupted']:
                result.update(status='unknown', reason='supervisor interrupted')
            elif proc['timeout']:
                result.update(status='unknown', reason='solver process wall-time cutoff')
            elif proc['returncode'] != 0 or not (attempt/'solver.json').exists():
                result.update(status='error', reason='solver process failed; see solver.log')
            else:
                raw = json.loads((attempt/'solver.json').read_text())
                result.update(raw)
                if raw['solver_answer'] == 'SAT':
                    witness = attempt/'witness.json'
                    if not verify_model(row['n'], clauses, json.loads(witness.read_text())):
                        result.update(status='error', reason='invalid SAT witness')
                    else:
                        result.update(status='SAT-verified', reason='integer clause evaluation',
                                      witness=str(witness.relative_to(run_dir)), witness_sha256=digest(witness))
                elif config['proof_policy'] == 'solver_only':
                    result.update(status='UNSAT-unchecked', reason='proof policy solver_only')
                else:
                    proof = attempt/'proof.drat'
                    result.update(proof=str(proof.relative_to(run_dir)), proof_sha256=digest(proof))
                    checked = check_proof(checker, cnf, proof, config['check_timeout_seconds'],
                                          config['memory_mb'], attempt/'checker.log')
                    result['proof_check'] = checked
                    if checked['verified']:
                        result.update(status='UNSAT-verified', reason='DRAT-trim s VERIFIED with exit 0')
                    else:
                        result.update(status='UNSAT-unchecked', reason='proof checker cutoff or failure; see checker.log')
        except Exception as exc:
            result.update(status='error', reason=f'{type(exc).__name__}: {exc}')
        result.update(completed_utc=now(), process_wall_seconds=time.perf_counter()-begun)
        atomic_json(attempt/'result.json', result)
        return {'id':row['id'], 'status':result['status']}


def load_manifest(run_dir):
    path = Path(run_dir)/'manifest.json'
    manifest = json.loads(path.read_text())
    if manifest['schema_version'] != SCHEMA:
        raise ValueError('Unsupported schema')
    validate_config(manifest['config'])
    if manifest['instances'] != instance_grid(manifest['config']):
        raise ValueError('Manifest instance grid is inconsistent')
    expected_chunks = (len(manifest['instances'])+manifest['config']['chunk_size']-1)//manifest['config']['chunk_size']
    if manifest['num_chunks'] != expected_chunks:
        raise ValueError('Manifest chunk count is inconsistent')
    if manifest['script_sha256'] != digest(SCRIPT):
        raise ValueError('Runner changed since planning; create a new plan with a fresh run directory')
    return manifest, digest(path)


def run_chunk(args):
    STOP.clear()
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda signum, frame: STOP.set())
    run_dir = Path(args.run_dir).resolve()
    manifest, manifest_hash = load_manifest(run_dir)
    config = manifest['config']
    if args.workers <= 0 or not 0 <= args.chunk_id < manifest['num_chunks']:
        raise ValueError('Invalid worker count or chunk ID')
    allocated = os.environ.get('SLURM_CPUS_PER_TASK')
    if allocated and args.workers > int(allocated):
        raise ValueError('workers exceeds SLURM_CPUS_PER_TASK')
    checker = Path(args.drat_trim).resolve() if args.drat_trim else None
    if config['proof_policy'] == 'required' and (not checker or not os.access(checker, os.X_OK)):
        raise ValueError('Proof policy required: supply an executable --drat-trim')
    env = environment(checker)
    if env['python_sat'] != '1.9.dev15':
        raise ValueError('This workflow pins python-sat==1.9.dev15')
    token = f'chunk-{args.chunk_id:05d}-{uuid.uuid4().hex}'
    provenance_path = run_dir/'chunks'/f'{token}.json'
    atomic_json(provenance_path, dict(env, command=sys.argv, manifest_sha256=manifest_hash,
                                     chunk_id=args.chunk_id, workers=args.workers))
    rows = [r for r in manifest['instances'] if r['chunk_id'] == args.chunk_id]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        # Threads supervise isolated, single-threaded solver/checker processes.
        outcomes = list(pool.map(lambda r: evaluate_instance(r, run_dir, config, checker,
                        manifest_hash, provenance_path, args.retry_unknown), rows))
    atomic_json(run_dir/'chunks'/f'{token}-completion.json', dict(completed_utc=now(), outcomes=outcomes))
    counts = {s:sum(r['status'] == s for r in outcomes) for s in sorted({r['status'] for r in outcomes})}
    print(json.dumps({'chunk_id':args.chunk_id, 'counts':counts}))
    return 130 if STOP.is_set() else (1 if counts.get('error',0) else 0)


def preflight(checker, output):
    checker = Path(checker).resolve()
    if not os.access(checker, os.X_OK):
        raise ValueError('Checker is not executable')
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError(output)
    env = environment(checker)
    if env['python_sat'] != '1.9.dev15':
        raise ValueError('Require python-sat==1.9.dev15')
    from pysat.solvers import Glucose42
    sat_clauses = [[1,2]]
    unsat_clauses = [[1,2],[1,-2],[-1,2],[-1,-2]]
    with tempfile.TemporaryDirectory(prefix='ksat-preflight-') as temp:
        temp = Path(temp)
        sat, unsat, proof = temp/'sat.cnf', temp/'unsat.cnf', temp/'proof.drat'
        write_cnf(sat, 2, sat_clauses)
        write_cnf(unsat, 2, unsat_clauses)
        with Glucose42(bootstrap_with=sat_clauses) as solver:
            if not solver.solve() or not verify_model(2, sat_clauses, solver.get_model()):
                raise RuntimeError('SAT preflight failed')
        with Glucose42(bootstrap_with=unsat_clauses, with_proof=True) as solver:
            if solver.solve():
                raise RuntimeError('UNSAT preflight failed')
            proof.write_text('\n'.join(solver.get_proof())+'\n')
        valid = check_proof(checker, unsat, proof, 15, 1536, temp/'valid.log')
        invalid = check_proof(checker, sat, proof, 15, 1536, temp/'invalid.log')
        record = dict(env, sat_witness_checked=True, valid_proof=valid,
                      false_unsat_rejected=invalid['rejected'], invalid_proof=invalid,
                      valid_checker_log=(temp/'valid.log').read_text(),
                      invalid_checker_log=(temp/'invalid.log').read_text())
        atomic_json(output, record)
        if not valid['verified'] or not invalid['rejected']:
            raise RuntimeError('Certificate preflight failed; see retained output')
    print(json.dumps({'preflight':'passed', 'output':str(output)}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('plan')
    p.add_argument('--config', required=True)
    p.add_argument('--output', required=True)
    p = sub.add_parser('run')
    p.add_argument('--run-dir', required=True)
    p.add_argument('--chunk-id', required=True, type=int)
    p.add_argument('--workers', type=int, default=1)
    p.add_argument('--drat-trim')
    p.add_argument('--retry-unknown', action='store_true')
    p = sub.add_parser('preflight')
    p.add_argument('--drat-trim', required=True)
    p.add_argument('--output', required=True)
    p = sub.add_parser('_solve')
    p.add_argument('--cnf', type=Path, required=True)
    p.add_argument('--attempt', type=Path, required=True)
    p.add_argument('--memory-mb', type=int, required=True)
    p.add_argument('--proof', action='store_true')
    p = sub.add_parser('_check')
    p.add_argument('--checker', required=True)
    p.add_argument('--cnf', required=True)
    p.add_argument('--proof', required=True)
    p.add_argument('--memory-mb', type=int, required=True)
    args = parser.parse_args()
    if args.cmd == 'plan':
        plan(args.config, args.output)
    elif args.cmd == 'run':
        return run_chunk(args)
    elif args.cmd == 'preflight':
        preflight(args.drat_trim, args.output)
    elif args.cmd == '_solve':
        solve_child(args.cnf, args.attempt, args.memory_mb, args.proof)
    elif args.cmd == '_check':
        impose_memory_limit(args.memory_mb)
        os.execv(args.checker, [args.checker, args.cnf, args.proof])
    return 0


if __name__ == '__main__':
    sys.exit(main())
