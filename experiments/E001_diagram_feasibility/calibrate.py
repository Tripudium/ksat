#!/usr/bin/env python3
"""Tiny bounded calibration, not a probability-estimation experiment.

Run: uv run --with python-sat==1.9.dev15 python experiments/E001_diagram_feasibility/calibrate.py
Each child has a 0.75-second process-wall-time limit, including initialization.
60 children therefore receive at most 45 seconds of aggregate run budget.
"""
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import random
import resource
import subprocess
import sys
import time
from datetime import datetime, timezone


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def worker(path):
    from pysat.formula import CNF
    from pysat.solvers import Cadical195
    formula = CNF(from_file=path)
    start = time.perf_counter()
    with Cadical195(bootstrap_with=formula.clauses, use_timer=True) as solver:
        answer = solver.solve()
        result = dict(sat=answer, solve_cpu_seconds=solver.time(),
                      setup_and_solve_wall_seconds=time.perf_counter()-start,
                      stats=solver.accum_stats(),
                      model=solver.get_model() if answer else None)
    print(json.dumps(result), flush=True)


def main():
    root = Path(__file__).resolve().parent
    out = root / 'run001'
    out.mkdir(exist_ok=False)
    (out / 'inputs').mkdir()
    (out / 'witnesses').mkdir()
    start = time.perf_counter()
    meta = dict(started_utc=datetime.now(timezone.utc).isoformat(),
                command='uv run --with python-sat==1.9.dev15 python experiments/E001_diagram_feasibility/calibrate.py',
                python=sys.version, python_executable=sys.executable,
                python_sat=importlib.metadata.version('python-sat'),
                solver='CaDiCaL 1.9.5, default options, one process per instance',
                platform=platform.platform(), processor=platform.processor(),
                logical_cpu_count=os.cpu_count(), script_sha256=sha(Path(__file__)),
                cutoff_process_wall_seconds=0.75, k=3,
                sizes=[100,200,300,400,600,800], alphas=[4.2,4.3], repeats=5,
                rng='random.Random(seed); sample(range(1,n+1),3); independent getrandbits(1) signs',
                seed_rule='202610110000 + 100000*n + 100*alpha_tenths + replicate',
                proof_logging=False, exact_checks='integer SAT witness evaluation; no numerical tolerance')
    for command, key in [(['git','rev-parse','HEAD'],'git_head'),
                         (['sysctl','-n','machdep.cpu.brand_string'],'cpu_brand')]:
        proc = subprocess.run(command,capture_output=True,text=True)
        meta[key] = proc.stdout.strip() if proc.returncode == 0 else 'unavailable: '+proc.stderr.strip()
    (out/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
    rows=[]
    with (out/'results.jsonl').open('x') as log:
        for n in meta['sizes']:
            for at in [42,43]:
                m=at*n//10
                for rep in range(5):
                    seed=202610110000+100000*n+100*at+rep
                    rng=random.Random(seed)
                    clauses=[[v if rng.getrandbits(1) else -v for v in rng.sample(range(1,n+1),3)] for _ in range(m)]
                    ident=f'n{n}_a{at}_r{rep}'
                    path=out/'inputs'/f'{ident}.cnf'
                    path.write_text(f'p cnf {n} {m}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses))
                    row=dict(id=ident,n=n,m=m,k=3,alpha=at/10,replicate=rep,seed=seed,
                             input=str(path.relative_to(root)),input_sha256=sha(path))
                    begun=time.perf_counter()
                    before=resource.getrusage(resource.RUSAGE_CHILDREN)
                    try:
                        proc=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker',str(path)],
                                            capture_output=True,text=True,timeout=0.75)
                        if proc.returncode:
                            row.update(status='error',returncode=proc.returncode,stderr=proc.stderr,stdout=proc.stdout)
                        else:
                            result=json.loads(proc.stdout)
                            model=result.pop('model')
                            if result.pop('sat'):
                                assignment=set(model)
                                valid=(len({abs(x) for x in assignment})==len(assignment)
                                       and all(any(lit in assignment for lit in clause) for clause in clauses))
                                if not valid:
                                    raise RuntimeError('SAT witness validation failed: '+ident)
                                witness=out/'witnesses'/f'{ident}.json'
                                witness.write_text(json.dumps(model)+'\n')
                                row.update(status='SAT-verified',witness=str(witness.relative_to(root)),witness_sha256=sha(witness))
                            else:
                                row.update(status='UNSAT-unchecked',certificate_status='solver report only; no proof logged')
                            row.update(result)
                    except subprocess.TimeoutExpired as exc:
                        row.update(status='unknown',reason='process wall-time cutoff',
                                   partial_stdout=(exc.stdout or b'').decode(errors='replace'),
                                   partial_stderr=(exc.stderr or b'').decode(errors='replace'))
                    after=resource.getrusage(resource.RUSAGE_CHILDREN)
                    row.update(process_wall_seconds=time.perf_counter()-begun,
                               process_cpu_seconds=(after.ru_utime+after.ru_stime)-(before.ru_utime+before.ru_stime))
                    log.write(json.dumps(row)+'\n');log.flush();rows.append(row)
            print(json.dumps({'n':n,'statuses':{s:sum(r['n']==n and r['status']==s for r in rows) for s in ('SAT-verified','UNSAT-unchecked','unknown','error')}}),flush=True)
    summary=dict(completed_utc=datetime.now(timezone.utc).isoformat(),
                 elapsed_wall_seconds=time.perf_counter()-start,
                 total_child_cpu_seconds=sum(r['process_cpu_seconds'] for r in rows),
                 total_child_wall_seconds=sum(r['process_wall_seconds'] for r in rows),
                 statuses={s:sum(r['status']==s for r in rows) for s in ('SAT-verified','UNSAT-unchecked','unknown','error')})
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--worker': worker(sys.argv[2])
    else: main()
