"""Unit tests for the method's core invariants.

Covers: the MixColumns specification, the oracle (accept good circuits,
reject broken ones), the value-set machinery (realizability, depth-aware
reconstruction, trimming), a bounded live engine run through the
verify-before-claim path, and the standalone verifier CLI.
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline"))

import mixcolumns_core as core   # noqa: E402
import engines                   # noqa: E402

CIRCUITS = sorted((ROOT / "evidence" / "circuits").glob("mixcolumns_*.json"))
RECORD_89 = ROOT / "evidence" / "circuits" / "mixcolumns_89gates_depth5.json"


class SpecInvariants(unittest.TestCase):
    def test_target_weight_profile(self):
        """MixColumns has exactly 20 weight-5 and 12 weight-7 output masks."""
        wts = [core.wt(m) for m in core.TARGETS]
        self.assertEqual(wts.count(5), 20)
        self.assertEqual(wts.count(7), 12)
        self.assertEqual(len(set(core.TARGETS)), 32)

    def test_naive_circuit_is_valid_and_depth3(self):
        v = core.verify(core.naive_circuit(), max_depth=3)
        self.assertTrue(v["ok"], v)


class OracleInvariants(unittest.TestCase):
    def test_all_record_circuits_verify_at_their_depth(self):
        self.assertEqual(len(CIRCUITS), 3)
        for path in CIRCUITS:
            data = json.loads(path.read_text(encoding="utf-8"))
            v = core.verify(data["gates"], max_depth=data["depth"])
            self.assertTrue(v["ok"], f"{path.name}: {v}")
            self.assertEqual(v["gates"], data["gateCount"], path.name)
            self.assertEqual(v["depth"], data["depth"], path.name)

    def test_rejects_forward_reference(self):
        gates = [list(g) for g in json.loads(RECORD_89.read_text())["gates"]]
        gates[0] = [0, 9999]
        self.assertFalse(core.verify(gates)["ok"])

    def test_rejects_truncated_circuit(self):
        # the final gate of a dead-gate-free circuit must carry an output,
        # so dropping it must break correctness
        gates = json.loads(RECORD_89.read_text())["gates"]
        self.assertFalse(core.verify(gates[:-1])["ok"])

    def test_rejects_depth_cap_violation(self):
        gates = json.loads(RECORD_89.read_text())["gates"]
        self.assertFalse(core.verify(gates, max_depth=4)["ok"])
        self.assertTrue(core.verify(gates, max_depth=5)["ok"])


class ValueSetInvariants(unittest.TestCase):
    def test_masks_reconstruct_within_depth_and_size(self):
        """value-set -> gate-list reconstruction respects the cap and never
        adds gates: |gates| == |value-set|, and the result verifies."""
        for path in CIRCUITS:
            data = json.loads(path.read_text(encoding="utf-8"))
            masks = core.load_circuit_masks(str(path))
            self.assertTrue(engines.feasible_at(masks, data["depth"]), path.name)
            gates = engines.indexpairs_from_masks(masks, data["depth"])
            self.assertEqual(len(gates), len(masks), path.name)
            v = core.verify(gates, max_depth=data["depth"])
            self.assertTrue(v["ok"], f"{path.name}: {v}")

    def test_trim_keeps_realizability_and_never_grows(self):
        masks = core.load_circuit_masks(str(RECORD_89))
        trimmed = engines.trim_masks(set(masks))
        self.assertTrue(engines.realizable(trimmed))
        self.assertLessEqual(len(trimmed), len(masks))

    def test_infeasible_at_too_small_cap(self):
        masks = core.load_circuit_masks(str(RECORD_89))
        self.assertFalse(engines.feasible_at(masks, 2))  # depth 2 impossible


class EngineVerifyBeforeClaim(unittest.TestCase):
    def test_walk_only_surfaces_verified_circuits(self):
        """Run the walk engine briefly from a seed; every candidate it claims
        must pass the oracle, and the best must not exceed the seed size."""
        claimed = []

        class Ctx:
            def log(self, msg):
                pass

            def improve(self, gates, masks, note=""):
                v = core.verify(gates)
                assert v["ok"], "engine surfaced an unverified circuit"
                claimed.append(v["gates"])
                return True

        seed = core.load_circuit_masks(str(ROOT / "pipeline" / "seeds" / "seed_90_at_depth5.json"))
        knobs = dict(hub_move_p=0.35, close_hamming=4, repair_hub=40,
                     repair_one=24, plateau_slack_p=0.02)
        engines.run_engine("walk", seed, None, None, 8, [3], knobs, Ctx())
        self.assertTrue(claimed)
        self.assertLessEqual(min(claimed), 90)


class VerifierCLI(unittest.TestCase):
    def test_no_args_prints_usage_and_exits_2(self):
        r = subprocess.run([sys.executable, str(ROOT / "verify_circuit.py")],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("usage:", r.stdout)

    def test_record_circuit_passes_with_depth_bound(self):
        r = subprocess.run([sys.executable, str(ROOT / "verify_circuit.py"),
                            str(RECORD_89), "5"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("VALID", r.stdout)

    def test_record_circuit_fails_tighter_depth_bound(self):
        r = subprocess.run([sys.executable, str(ROOT / "verify_circuit.py"),
                            str(RECORD_89), "4"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()
