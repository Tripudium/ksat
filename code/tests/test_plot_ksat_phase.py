"""Synthetic collector fixtures; these are NOT random-k-SAT threshold data."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SPEC = importlib.util.spec_from_file_location(
    "plot_ksat_phase", Path(__file__).resolve().parents[1] / "plot_ksat_phase.py"
)
plot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(plot)


class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ksat-synthetic-collector-")
        self.addCleanup(self.temporary.cleanup)
        self.run = Path(self.temporary.name)
        self.manifest = {
            "schema_version": 1,
            "synthetic_fixture": True,
            "config": {
                "k": 3, "n_values": [4], "alpha_values": ["1"],
                "repetitions": 4, "base_seed": 7, "chunk_size": 2,
                "solve_timeout_seconds": 5, "check_timeout_seconds": 5,
                "memory_mb": 1024, "proof_policy": "required",
            },
            "num_chunks": 2,
            "instances": [
                {
                    "id": f"synthetic-{r}", "n": 4, "k": 3, "m": 4,
                    "alpha_requested": "1", "alpha_actual": 1.0,
                    "replicate": r, "seed": 100 + r, "chunk_id": r // 2,
                }
                for r in range(4)
            ],
        }
        self.write_manifest()

    def write_manifest(self):
        data = (json.dumps(self.manifest, indent=2) + "\n").encode()
        (self.run / "manifest.json").write_bytes(data)
        self.manifest_hash = hashlib.sha256(data).hexdigest()

    def result(self, replicate, status, *, attempt="attempt-1", started="2026-10-11T12:00:00Z", **changes):
        instance = self.manifest["instances"][replicate]
        directory = self.run / "attempts" / instance["id"] / attempt
        directory.mkdir(parents=True, exist_ok=True)
        input_path = directory / "input.cnf"
        input_path.write_text("c synthetic collector fixture, not threshold data\np cnf 4 0\n")
        artifacts = {
            "input": str(input_path.relative_to(self.run)),
            "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        }
        if status in plot.VERIFIED:
            artifact = "witness" if status == "SAT-verified" else "proof"
            artifact_path = directory / (artifact + ".synthetic")
            artifact_path.write_text("synthetic collector fixture; not a mathematical certificate\n")
            artifacts.update({
                artifact: str(artifact_path.relative_to(self.run)),
                artifact + "_sha256": hashlib.sha256(artifact_path.read_bytes()).hexdigest(),
            })
        value = {
            **instance, "status": status, "reason": "synthetic fixture only",
            "manifest_sha256": self.manifest_hash, **artifacts,
            "process_wall_seconds": 0.25, "started_utc": started,
            "attempt_id": attempt, "solver_stats": {},
            **changes,
        }
        path = self.run / "attempts" / instance["id"] / attempt / "result.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def fill_other_unknowns(self, start=1):
        for replicate in range(start, 4):
            self.result(replicate, "unknown")

    def test_censored_denominator_includes_unknown_and_unchecked(self):
        for replicate, status in enumerate(("SAT-verified", "UNSAT-verified", "unknown", "UNSAT-unchecked")):
            self.result(replicate, status)
        summary = plot.collect_run(self.run)
        cell = summary["cells"][0]
        self.assertEqual(cell["planned_repetitions"], 4)
        self.assertEqual((cell["p_lower"], cell["p_upper"]), (0.25, 0.75))
        self.assertIsNone(cell["p_estimate"])
        self.assertEqual(cell["unresolved"], 2)
        self.assertEqual(cell["unresolved_fraction"], 0.5)
        self.assertEqual(cell["confidence_lower_95"], 0)
        self.assertEqual(cell["confidence_upper_95"], 1)

    def test_missing_requires_explicit_partial_and_remains_in_denominator(self):
        self.result(0, "SAT-verified")
        with self.assertRaisesRegex(plot.CollectionError, "3/4 planned instances"):
            plot.collect_run(self.run)
        summary = plot.collect_run(self.run, allow_partial=True)
        cell = summary["cells"][0]
        self.assertEqual(cell["pending"], 3)
        self.assertEqual((cell["p_lower"], cell["p_upper"]), (0.25, 1))
        self.assertIsNone(cell["p_estimate"])

    def test_duplicate_attempts_are_one_sample_and_first_verified_wins(self):
        self.result(0, "unknown", attempt="early", started="2026-10-11T10:00:00Z")
        self.result(0, "SAT-verified", attempt="verified-first", started="2026-10-11T11:00:00Z")
        self.result(0, "SAT-verified", attempt="verified-later", started="2026-10-11T12:00:00Z")
        self.result(0, "error", attempt="latest", started="2026-10-11T13:00:00Z")
        self.fill_other_unknowns()
        summary = plot.collect_run(self.run)
        self.assertEqual(summary["instances"][0]["selected_attempt_id"], "verified-first")
        self.assertEqual(summary["instances"][0]["completed_attempt_count"], 4)
        self.assertEqual(summary["cells"][0]["sat_verified"], 1)
        self.assertEqual(summary["cells"][0]["planned_repetitions"], 4)

    def test_conflicting_verified_certificates_become_unresolved_error(self):
        self.result(0, "SAT-verified", attempt="sat")
        self.result(0, "UNSAT-verified", attempt="unsat")
        self.fill_other_unknowns()
        summary = plot.collect_run(self.run)
        self.assertEqual(summary["instances"][0]["status"], "error")
        self.assertIn("Conflicting", summary["instances"][0]["reason"])
        self.assertEqual(summary["cells"][0]["sat_verified"], 0)
        self.assertEqual(summary["cells"][0]["unsat_verified"], 0)
        self.assertEqual((summary["cells"][0]["p_lower"], summary["cells"][0]["p_upper"]), (0, 1))

    def test_wrong_manifest_hash_invalidates_even_a_verified_outcome(self):
        self.result(0, "SAT-verified", manifest_sha256="b" * 64)
        self.fill_other_unknowns()
        record = plot.collect_run(self.run)["instances"][0]
        self.assertEqual(record["status"], "error")
        self.assertIn("manifest_sha256 mismatch", record["diagnostics"][0])

    def test_wrong_identity_invalidates_an_attempt(self):
        self.result(0, "UNSAT-verified", seed=999)
        self.fill_other_unknowns()
        record = plot.collect_run(self.run)["instances"][0]
        self.assertEqual(record["status"], "error")
        self.assertIn("identity mismatch: seed", record["diagnostics"][0])

    def test_latest_completed_selected_if_no_verified_result(self):
        self.result(0, "unknown", attempt="earlier", started="2026-10-11T10:00:00+00:00")
        self.result(0, "UNSAT-unchecked", attempt="later", started="2026-10-11T12:00:00+01:00")
        self.fill_other_unknowns()
        record = plot.collect_run(self.run)["instances"][0]
        self.assertEqual(record["selected_attempt_id"], "later")
        self.assertEqual(record["status"], "UNSAT-unchecked")

    def test_all_resolved_has_an_estimate(self):
        for replicate in range(4):
            self.result(replicate, "SAT-verified" if replicate < 3 else "UNSAT-verified")
        cell = plot.collect_run(self.run)["cells"][0]
        self.assertTrue(cell["complete"])
        self.assertEqual(cell["p_estimate"], 0.75)
        self.assertEqual(cell["p_lower"], cell["p_upper"])

    def test_malformed_attempt_is_an_error_not_an_extra_missing_sample(self):
        path = self.result(0, "unknown")
        path.write_text("{broken", encoding="utf-8")
        self.fill_other_unknowns()
        summary = plot.collect_run(self.run)
        self.assertEqual(summary["counts"]["error"], 1)
        self.assertEqual(summary["counts"]["pending"], 0)

    def test_inconsistent_input_hashes_are_errors(self):
        self.result(0, "SAT-verified", attempt="one")
        path = self.result(0, "SAT-verified", attempt="two")
        result = json.loads(path.read_text())
        changed_input = self.run / result["input"]
        changed_input.write_text("c different synthetic formula\np cnf 4 0\n")
        result["input_sha256"] = hashlib.sha256(changed_input.read_bytes()).hexdigest()
        path.write_text(json.dumps(result))
        self.fill_other_unknowns()
        self.assertEqual(plot.collect_run(self.run)["instances"][0]["status"], "error")

    def test_removed_proof_invalidates_verified_status(self):
        path = self.result(0, "UNSAT-verified")
        result = json.loads(path.read_text())
        (self.run / result["proof"]).unlink()
        self.fill_other_unknowns()
        record = plot.collect_run(self.run)["instances"][0]
        self.assertEqual(record["status"], "error")
        self.assertIn("missing proof artifact", record["diagnostics"][0])

    def test_changed_witness_invalidates_verified_status(self):
        path = self.result(0, "SAT-verified")
        result = json.loads(path.read_text())
        (self.run / result["witness"]).write_text("changed")
        self.fill_other_unknowns()
        record = plot.collect_run(self.run)["instances"][0]
        self.assertEqual(record["status"], "error")
        self.assertIn("witness_sha256 artifact mismatch", record["diagnostics"][0])

    def test_verified_status_requires_artifact_fields(self):
        path = self.result(0, "SAT-verified")
        result = json.loads(path.read_text())
        del result["witness"]
        path.write_text(json.dumps(result))
        self.fill_other_unknowns()
        record = plot.collect_run(self.run)["instances"][0]
        self.assertEqual(record["status"], "error")
        self.assertIn("witness artifact path", record["diagnostics"][0])

    def test_duplicate_planned_ids_rejected(self):
        self.manifest["instances"][1]["id"] = self.manifest["instances"][0]["id"]
        self.write_manifest()
        with self.assertRaisesRegex(plot.CollectionError, "Duplicate planned instance"):
            plot.collect_run(self.run, allow_partial=True)

    def test_existing_output_is_never_modified(self):
        output = self.run / "existing-output"
        output.mkdir()
        marker = output / "keep.txt"
        marker.write_text("preserved", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            plot.write_outputs({}, output)
        self.assertEqual(marker.read_text(encoding="utf-8"), "preserved")


if __name__ == "__main__":
    unittest.main()
