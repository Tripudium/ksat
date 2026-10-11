#!/usr/bin/env python3
"""Check retained E001 inputs, regeneration, hashes and SAT witnesses; no SAT solving."""
import hashlib
import json
from pathlib import Path
import random

root = Path(__file__).resolve().parent
run = root / 'run001'
rows = [json.loads(line) for line in (run/'results.jsonl').read_text().splitlines()]
meta = json.loads((run/'metadata.json').read_text())
assert len(rows) == 60
assert hashlib.sha256((root/'calibrate.py').read_bytes()).hexdigest() == meta['script_sha256']
checked = 0
for row in rows:
    source = (root/row['input']).read_bytes()
    assert hashlib.sha256(source).hexdigest() == row['input_sha256']
    rng = random.Random(row['seed'])
    clauses = []
    for _ in range(row['m']):
        variables = rng.sample(range(1, row['n']+1), 3)
        clauses.append([v if rng.getrandbits(1) else -v for v in variables])
    regenerated = (f"p cnf {row['n']} {row['m']}\n"+
                   ''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode()
    assert source == regenerated
    assert all(len({abs(lit) for lit in clause}) == 3 for clause in clauses)
    if row['status'] == 'SAT-verified':
        witness = (root/row['witness']).read_bytes()
        assert hashlib.sha256(witness).hexdigest() == row['witness_sha256']
        literals = json.loads(witness)
        model = set(literals)
        assert len(model) == len(literals) == len({abs(lit) for lit in model})
        assert all(1 <= abs(lit) <= row['n'] for lit in model)
        assert all(any(lit in model for lit in clause) for clause in clauses)
        checked += 1
assert checked == 21
print(json.dumps({'input_hashes_checked':len(rows), 'inputs_regenerated':len(rows),
                  'sat_witnesses_checked':checked, 'unsat_proofs_checked':0,
                  'unknowns_preserved':sum(r['status']=='unknown' for r in rows),
                  'calibration_script_hash_checked':True,
                  'scope':'Author self-check of retained data; no independent review.'}))
