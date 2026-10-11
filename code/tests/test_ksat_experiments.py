"""Software checks only; no concentration theorem is established by these tests."""
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest

SOURCE = Path(__file__).resolve().parents[1]/'ksat_experiments.py'
spec = importlib.util.spec_from_file_location('ksat_experiments', SOURCE)
ksat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ksat)


def config():
    return dict(name='test', k=3, n_values=[5,8], alpha_values=['0.00','2.50'],
                repetitions=3, base_seed=71, chunk_size=5, solve_timeout_seconds=1,
                check_timeout_seconds=1, memory_mb=512, proof_policy='required')


class EnsembleTests(unittest.TestCase):
    def test_exact_rounding_unique_seeds_and_proper_clauses(self):
        c = ksat.validate_config(config())
        rows = ksat.instance_grid(c)
        self.assertEqual(len(rows), 12)
        self.assertEqual(len({r['seed'] for r in rows}), 12)
        self.assertEqual(rows[-1]['chunk_id'], 2)
        self.assertEqual(rows[3]['m'], 12)  # floor(2.50*5)
        for row in rows:
            clauses = list(ksat.clauses_for(row))
            self.assertEqual(clauses, list(ksat.clauses_for(row)))
            self.assertEqual(len(clauses), row['m'])
            for clause in clauses:
                self.assertEqual(len({abs(x) for x in clause}), row['k'])
                self.assertTrue(all(1 <= abs(x) <= row['n'] for x in clause))

    def test_invalid_configs_and_integer_aliases_rejected(self):
        for change in ({'alpha_values':['0.1','0.11']}, {'n_values':[2]},
                       {'proof_policy':'trust-me'}, {'solve_timeout_seconds':float('nan')},
                       {'repetitions':0}, {'base_seed':-1}):
            with self.assertRaises(ValueError):
                ksat.validate_config(dict(config(), **change))

    def test_decimal_clause_count_is_exact(self):
        self.assertEqual(ksat.clause_count('0.3333333333333333333333333333333333333',3), 0)
        self.assertEqual(ksat.clause_count('4.30',100), 430)

    def test_witness_checker_against_truth_tables(self):
        clauses = [[1,2],[-1,2],[1,-2],[-1,-2]]
        for m in range(5):
            accepted = 0
            for signs in itertools.product((-1,1), repeat=2):
                model = [(i+1)*s for i,s in enumerate(signs)]
                accepted += ksat.verify_model(2, clauses[:m], model)
            self.assertEqual(accepted, 4-m)
        for invalid in ([1,-1], [0], [3], [True]):
            self.assertFalse(ksat.verify_model(2, [], invalid))

    def test_plan_refuses_overwrite_and_detects_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            cpath, run = temp/'config.json', temp/'run'
            cpath.write_text(json.dumps(config()))
            ksat.plan(cpath, run)
            original = (run/'manifest.json').read_bytes()
            with self.assertRaises(FileExistsError):
                ksat.plan(cpath, run)
            self.assertEqual(original, (run/'manifest.json').read_bytes())
            ksat.load_manifest(run)
            tampered = json.loads(original)
            tampered['instances'][0]['seed'] += 1
            (run/'manifest.json').write_text(json.dumps(tampered))
            with self.assertRaises(ValueError):
                ksat.load_manifest(run)

    def test_atomic_record_preserves_existing_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'record.json'
            ksat.atomic_json(path, {'first':1})
            with self.assertRaises(FileExistsError):
                ksat.atomic_json(path, {'second':2})
            self.assertEqual(json.loads(path.read_text()), {'first':1})

    def test_process_timeout_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            result = ksat.run_process([sys.executable, '-c', 'import time; time.sleep(5)'],
                                      0.05, Path(temp)/'timeout.log')
            self.assertTrue(result['timeout'])
            self.assertNotEqual(result['returncode'], 0)

    def test_interruption_stops_supervised_process(self):
        with tempfile.TemporaryDirectory() as temp:
            timer = threading.Timer(0.1, ksat.STOP.set)
            timer.start()
            try:
                result = ksat.run_process([sys.executable, '-c', 'import time; time.sleep(10)'],
                                          15, Path(temp)/'interrupted.log')
                self.assertTrue(result['interrupted'])
                self.assertFalse(result['timeout'])
                self.assertNotEqual(result['returncode'], 0)
                self.assertLess(result['wall_seconds'], 3)
            finally:
                timer.join()
                ksat.STOP.clear()


if __name__ == '__main__':
    unittest.main()
