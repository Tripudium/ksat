#!/usr/bin/env python3
"""Exact truth-table check of retained tiny software-smoke cases only."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--run-dir', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
manifest = json.loads((args.run_dir/'manifest.json').read_text())
checked = []
for row in manifest['instances']:
    if row['n'] > 12:
        raise ValueError('This checker is restricted to n <= 12 software fixtures')
    paths = list((args.run_dir/'attempts'/row['id']).glob('*/result.json'))
    if not paths:
        raise ValueError('Missing completed instance')
    for path in paths:
        result = json.loads(path.read_text())
        data = (args.run_dir/result['input']).read_bytes()
        if hashlib.sha256(data).hexdigest() != result['input_sha256']:
            raise ValueError('Input changed')
        lines = data.decode().splitlines()
        clauses = [list(map(int,line.split()))[:-1] for line in lines if not line.startswith(('c','p'))]
        sat_count = 0
        for assignment in itertools.product((False,True), repeat=row['n']):
            if all(any(assignment[abs(lit)-1] == (lit>0) for lit in clause) for clause in clauses):
                sat_count += 1
        expected = 'SAT-verified' if sat_count else 'UNSAT-verified'
        if result['status'] != expected:
            raise ValueError(f'Unexpected outcome {result["status"]} for exact {expected}')
        checked.append({'id':row['id'],'attempt_id':result['attempt_id'],
                        'n':row['n'],'m':row['m'],'exact_satisfying_assignments':sat_count})
record = {'scope':'Exact enumeration of these retained n<=12 software-smoke instances only; no threshold or concentration conclusion',
          'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'instances':len(manifest['instances']),'attempts_checked':len(checked),'records':checked}
with args.output.open('x') as f:
    json.dump(record,f,indent=2)
    f.write('\n')
print(f'Exact truth tables agree for {len(checked)} retained attempts')
