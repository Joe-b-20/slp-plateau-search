"""Unit tests for the method's core invariants.

Covers: the MixColumns specification, the oracle (accept good circuits,
reject broken ones), the eight record circuits at their stated depths and their
failure one level tighter, the value-set machinery (realizability, depth-aware
reconstruction, trimming),
the rebuilt kernels of the merged engine (level-BFS `relax`, incremental
closure / `remove_query`, exact complete `_repair`) against plain reference
implementations written out in this file, bounded live runs of both search
engines through the verify-before-claim path, and the standalone verifier CLI.

Everything here is stdlib-only, deterministic apart from the two time-boxed
engine runs, and the whole module is meant to stay well under two minutes.
"""
from __future__ import annotations

import hashlib
import json
import random
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "pipeline"))

import mixcolumns_core as core   # noqa: E402
import engines                   # noqa: E402

CIRCUIT_DIR = ROOT / "evidence" / "circuits"
CIRCUITS = sorted(CIRCUIT_DIR.glob("mixcolumns_*.json"))

# The record list, exactly as CI verifies it: 97@3, 92@4, 89@5 and five 88s -- two
# at depth 5 and one each at depths 6, 7 and 8. Each is verified at its stated
# depth AND asserted to fail at depth-1, so the depths are tight rather than
# merely claimed.
# 88 is Jean's published count (ePrint 2026/1481) and Jean has priority: 88@7
# matches it with a different circuit, 88@6 and the from-scratch 88@5 were found
# from scratch and are distinct families, and the derived 88@5 and the 88@8 have
# seed chains that pass through Jean's circuit (derived work).
#
# CAREFUL: two records share the (gates, depth) pair (88, 5). Nothing in this
# module -- including the generated test-method names below -- may key on that
# pair; the file name is the identity.
RECORDS = {
    "mixcolumns_97gates_depth3.json": (97, 3),
    "mixcolumns_92gates_depth4.json": (92, 4),
    "mixcolumns_89gates_depth5.json": (89, 5),
    "mixcolumns_88gates_depth5_fromscratch.json": (88, 5),
    "mixcolumns_88gates_depth5.json": (88, 5),
    "mixcolumns_88gates_depth6.json": (88, 6),
    "mixcolumns_88gates_depth7.json": (88, 7),
    "mixcolumns_88gates_depth8_thirdfamily.json": (88, 8),
}

RECORD_89 = CIRCUIT_DIR / "mixcolumns_89gates_depth5.json"
RECORD_88_5_FS = CIRCUIT_DIR / "mixcolumns_88gates_depth5_fromscratch.json"
RECORD_88_5 = CIRCUIT_DIR / "mixcolumns_88gates_depth5.json"
RECORD_88_6 = CIRCUIT_DIR / "mixcolumns_88gates_depth6.json"
RECORD_88_7 = CIRCUIT_DIR / "mixcolumns_88gates_depth7.json"
RECORD_88_8 = CIRCUIT_DIR / "mixcolumns_88gates_depth8_thirdfamily.json"
SEED_90 = ROOT / "pipeline" / "seeds" / "seed_90_at_depth5.json"


# ==========================================================================
# Reference implementations: the slow, obvious way to compute what the
# engine's rebuilt kernels compute. Deliberately independent of engines.py.
# ==========================================================================
def ref_closure(masks):
    """(buildable, unbuildable) for `masks`, by re-scanning everything until
    nothing changes. A mask v is buildable once two already-buildable signals
    XOR to it, i.e. some available a has v ^ a available."""
    avail = set(core.INPUTS)
    pending = [m for m in set(masks) if m not in avail]
    changed = True
    while changed:
        changed = False
        still = []
        for v in pending:
            if any((v ^ a) in avail for a in avail):
                avail.add(v)
                changed = True
            else:
                still.append(v)
        pending = still
    return avail, set(pending)


def ref_depths(masks):
    """(depth-of-every-buildable-mask, unbuildable) by level-by-level
    relaxation: a mask sits at depth d as soon as both its parents are known
    at depth <= d-1."""
    dep = {m: 0 for m in core.INPUTS}
    pending = set(masks) - set(dep)
    d = 0
    while pending:
        d += 1
        newly = {v for v in pending if any((v ^ a) in dep for a in dep)}
        if not newly:
            break
        for v in newly:
            dep[v] = d
        pending -= newly
    return dep, pending


def ref_feasible(masks, cap):
    """Reference verdict for engines.feasible_at."""
    dep, unbuildable = ref_depths(masks)
    if unbuildable:
        return False
    if cap is None:
        return True
    return all(dep[m] <= cap for m in masks)


def ref_repairs(avail, stuck, universe):
    """Every mask in `universe` whose addition to a closed set `avail` unblocks
    all 32 targets. `stuck` is what could not be built without it."""
    good = []
    for w in universe:
        if w in avail:
            continue
        av = set(avail)
        av.add(w)
        rem = set(stuck)
        changed = True
        while changed:
            changed = False
            for v in sorted(rem):
                if any((v ^ a) in av for a in av):
                    av.add(v)
                    rem.discard(v)
                    changed = True
        if not (rem & core.TARGET_SET):
            good.append(w)
    return set(good)


# A few tiny hand-written value-sets, plus the real ones, to exercise the
# kernels away from record-sized inputs.
SMALL_CASES = [
    set(),                                   # empty
    {0b0011},                                # one weight-2 mask, depth 1
    {0b0011, 0b1100, 0b1111},                # depth 2, all buildable
    {0b1111},                                # weight 4 alone: not buildable
    {0b0011, 0b1111},                        # buildable at depth 2
    {0b0011, 0b0110, 0b0101, 0b1001},        # a small realizable fan
    {0b111},                                 # weight 3 alone: not buildable
]


def circuit_masks(path):
    return core.load_circuit_masks(str(path))


# ==========================================================================


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


class RecordCircuits(unittest.TestCase):
    """One generated test per record; the eight are attached below."""

    def test_directory_holds_exactly_the_eight_records(self):
        self.assertEqual(len(CIRCUITS), 8)
        self.assertEqual({p.name for p in CIRCUITS}, set(RECORDS))

    def test_two_distinct_circuits_share_the_gates_depth_point(self):
        """(88, 5) is held by two different value sets -- the from-scratch
        circuit and the derived one. They must be genuinely different, and the
        generated tests below must not have collapsed onto one another."""
        a = set(circuit_masks(RECORD_88_5_FS))
        b = set(circuit_masks(RECORD_88_5))
        self.assertEqual(len(a), 88)
        self.assertEqual(len(b), 88)
        self.assertNotEqual(a, b)
        self.assertLess(len(a & b) / len(a | b), 0.7)   # not even the same family
        at_88_5 = [n for n, gd in RECORDS.items() if gd == (88, 5)]
        self.assertEqual(len(at_88_5), 2)
        for name in at_88_5:
            self.assertTrue(hasattr(RecordCircuits, "test_record_" + name[:-5]),
                            "generated test missing for " + name)

    def test_spectrum_manifest_matches_the_files_on_disk(self):
        """spectrum.json is the published manifest of the record set: it must
        list exactly these eight circuits, with their gate counts, depths and
        the sha256 of the file as it actually stands."""
        spectrum = json.loads((CIRCUIT_DIR / "spectrum.json").read_text(encoding="utf-8"))
        self.assertEqual(len(spectrum), len(RECORDS))
        listed = {}
        for entry in spectrum:
            path = ROOT / "evidence" / entry["file"]
            self.assertTrue(path.is_file(), entry["file"])
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(entry["sha256"], digest, entry["file"])
            listed[path.name] = (entry["gates"], entry["depth"])
        self.assertEqual(listed, RECORDS)

    def _check_record(self, name, gate_count, depth):
        path = CIRCUIT_DIR / name
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["gateCount"], gate_count, name)
        self.assertEqual(data["depth"], depth, name)
        self.assertEqual(len(data["gates"]), gate_count, name)
        v = core.verify(data["gates"], max_depth=depth)
        self.assertTrue(v["ok"], f"{name}: {v}")
        self.assertEqual(v["gates"], gate_count, name)
        self.assertEqual(v["depth"], depth, name)
        # the stated depth is the true depth, so one less must fail
        self.assertFalse(core.verify(data["gates"], max_depth=depth - 1)["ok"], name)


def _attach_record_tests():
    """One test per record FILE. The method name is derived from the file name,
    not from (gates, depth): two records share the point (88, 5), and keying on
    the pair would silently drop one of them."""
    for name, (gate_count, depth) in sorted(RECORDS.items()):
        def test(self, name=name, gate_count=gate_count, depth=depth):
            self._check_record(name, gate_count, depth)
        test.__doc__ = "%d gates at depth %d verifies (%s)" % (gate_count, depth, name)
        attr = "test_record_" + name[:-5]
        assert not hasattr(RecordCircuits, attr), "duplicate test name: " + attr
        setattr(RecordCircuits, attr, test)


_attach_record_tests()


class OracleInvariants(unittest.TestCase):
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
            masks = circuit_masks(path)
            self.assertTrue(engines.feasible_at(masks, data["depth"]), path.name)
            gates = engines.indexpairs_from_masks(masks, data["depth"])
            self.assertEqual(len(gates), len(masks), path.name)
            v = core.verify(gates, max_depth=data["depth"])
            self.assertTrue(v["ok"], f"{path.name}: {v}")

    def test_trim_keeps_realizability_and_never_grows(self):
        for path in (RECORD_89, RECORD_88_5_FS, RECORD_88_5, RECORD_88_6,
                     RECORD_88_7, RECORD_88_8):
            masks = circuit_masks(path)
            trimmed = engines.trim_masks(set(masks))
            self.assertTrue(engines.realizable(trimmed), path.name)
            self.assertLessEqual(len(trimmed), len(masks), path.name)

    def test_infeasible_at_too_small_cap(self):
        masks = circuit_masks(RECORD_89)
        self.assertFalse(engines.feasible_at(masks, 2))  # depth 2 impossible


class FastKernelsMatchReference(unittest.TestCase):
    """The campaign rewrote relax/closure for speed (17.5x and 21.9x). These
    tests pin them to the plain implementations above: same answers, on the
    record circuits, the seeds and a handful of tiny sets."""

    def _mask_cases(self):
        cases = [("small#%d" % i, s) for i, s in enumerate(SMALL_CASES)]
        cases.append(("naive", core.naive_masks()))
        cases.append(("targets-only", set(core.TARGETS)))
        for path in CIRCUITS:
            cases.append((path.name, circuit_masks(path)))
        cases.append(("seed_90_at_depth5", circuit_masks(SEED_90)))
        return cases

    def test_relax_matches_reference_depths(self):
        for label, masks in self._mask_cases():
            ml = sorted(masks)
            avail = list(engines.INPUTS) + ml
            dep, pos = engines.relax(avail)
            ref, unbuildable = ref_depths(ml)
            for m in ml:
                got = dep[pos[m]]
                if m in unbuildable:
                    self.assertGreaterEqual(got, engines.INF, "%s: %08x" % (label, m))
                else:
                    self.assertEqual(got, ref[m], "%s: %08x" % (label, m))

    def test_relax_reference_agrees_and_covers_duplicates(self):
        """relax falls back to relax_reference on duplicate masks; both must
        give the same depths as each other on a clean set."""
        ml = sorted(circuit_masks(RECORD_88_7))
        avail = list(engines.INPUTS) + ml
        fast, pos = engines.relax(avail)
        slow, pos2 = engines.relax_reference(avail)
        self.assertEqual(pos, pos2)
        self.assertEqual(list(fast), list(slow))
        dup = avail + [ml[0]]                     # duplicate -> reference path
        depd, _ = engines.relax(dup)
        self.assertEqual(depd[pos[ml[0]]], fast[pos[ml[0]]])

    def test_closure_and_realizable_match_reference(self):
        for label, masks in self._mask_cases():
            avail, _order, _parents = engines.closure(set(masks))
            ref_avail, _ = ref_closure(masks)
            self.assertEqual(avail, ref_avail, label)
            self.assertEqual(engines.realizable(set(masks)),
                             core.TARGET_SET <= ref_avail, label)

    def test_realizable_rejects_damaged_record_sets(self):
        """Removing any single mask from a record circuit either breaks it or
        leaves it realizable -- whichever it is, engines.realizable must agree
        with the reference closure."""
        masks = circuit_masks(RECORD_88_7)
        broke = 0
        for v in sorted(masks)[:25]:
            S2 = set(masks) - {v}
            ref_avail, _ = ref_closure(S2)
            ref_ok = core.TARGET_SET <= ref_avail
            self.assertEqual(engines.realizable(S2), ref_ok, "%08x" % v)
            broke += 0 if ref_ok else 1
        self.assertGreater(broke, 0, "no single removal broke the 88@7")

    def test_feasible_at_matches_reference_at_caps(self):
        for path in CIRCUITS:
            depth = RECORDS[path.name][1]
            masks = circuit_masks(path)
            for cap in (None, depth + 1, depth, depth - 1, 2):
                self.assertEqual(engines.feasible_at(masks, cap),
                                 ref_feasible(masks, cap),
                                 "%s at cap %s" % (path.name, cap))
        for label, masks in [("small#%d" % i, s) for i, s in enumerate(SMALL_CASES)]:
            for cap in (None, 1, 2, 3):
                self.assertEqual(engines.feasible_at(masks, cap),
                                 ref_feasible(masks, cap),
                                 "%s at cap %s" % (label, cap))

    def test_remove_query_matches_reference_closure(self):
        """_WalkState answers 'what breaks if I drop these masks?' incrementally;
        the answer must be the closure of S - D, computed from scratch."""
        masks = set(circuit_masks(RECORD_89))
        st = engines._WalkState(masks)
        nont = sorted(m for m in masks if m not in core.TARGET_SET)
        rng = random.Random(20260727)
        removals = [(v,) for v in nont[:10]]
        removals += [tuple(rng.sample(nont, 2)) for _ in range(10)]
        for D in removals:
            ok, avail2, unrealized = st.remove_query(D)
            ref_avail, ref_unreal = ref_closure(masks - set(D))
            self.assertEqual(avail2, ref_avail, str(D))
            self.assertEqual(unrealized, ref_unreal, str(D))
            self.assertEqual(ok, core.TARGET_SET <= ref_avail, str(D))
        # the state itself must be unchanged by the queries
        self.assertEqual(st.S, masks)


class ExactRepair(unittest.TestCase):
    """_repair enumerates every single-mask repair instead of sampling. So it
    must (i) only ever return a repair that really works, and (ii) never miss
    one that exists -- in particular the mask just removed."""

    def _first_breaking_removal(self, masks, st):
        for v in sorted(m for m in masks if m not in core.TARGET_SET):
            ok, avail2, _ = st.remove_query((v,))
            if not ok:
                return v, avail2
        self.fail("no single removal broke the circuit")

    def test_only_returns_valid_repairs(self):
        masks = set(circuit_masks(RECORD_89))
        st = engines._WalkState(masks)
        rng = random.Random(11)
        checked = 0
        for v in sorted(m for m in masks if m not in core.TARGET_SET)[:30]:
            ok, avail2, _ = st.remove_query((v,))
            if ok:
                continue
            S2 = masks - {v}
            fixed = engines._repair(S2, rng, avail2)
            # the removed mask is itself a repair, so exhaustive enumeration
            # cannot come back empty-handed
            self.assertIsNotNone(fixed, "%08x" % v)
            self.assertEqual(len(fixed), len(S2) + 1, "%08x" % v)
            self.assertTrue(S2 < fixed, "%08x" % v)
            self.assertTrue(engines.realizable(fixed), "%08x" % v)
            checked += 1
            if checked >= 8:
                break
        self.assertGreater(checked, 0)

    def test_repaired_set_builds_a_circuit_the_oracle_accepts(self):
        masks = set(circuit_masks(RECORD_89))
        st = engines._WalkState(masks)
        v, avail2 = self._first_breaking_removal(masks, st)
        fixed = engines._repair(masks - {v}, random.Random(12), avail2)
        self.assertIsNotNone(fixed)
        trimmed = engines.trim_masks(fixed)
        gates = engines._walk_gates(trimmed, None)
        vfy = core.verify(gates)
        self.assertTrue(vfy["ok"], vfy)
        self.assertEqual(vfy["gates"], len(trimmed))

    def test_enumeration_is_complete_against_reference(self):
        """Against a brute-force repair set: the planted repair (the removed
        mask) is found, the chosen repair is one of the valid ones, and
        forbidding every valid repair leaves nothing to return."""
        masks = set(circuit_masks(RECORD_89))
        st = engines._WalkState(masks)
        v, avail2 = self._first_breaking_removal(masks, st)
        S2 = masks - {v}
        stuck = (S2 | core.TARGET_SET) - avail2
        universe = {u ^ a for u in stuck for a in avail2}
        universe.add(v)
        universe = {w for w in universe if w and core.wt(w) > 1}
        valid = ref_repairs(avail2, stuck, universe)
        self.assertIn(v, valid, "the planted repair must be valid")

        fixed = engines._repair(S2, random.Random(13), avail2)
        self.assertIsNotNone(fixed)
        chosen = set(fixed) - S2
        self.assertEqual(len(chosen), 1)
        self.assertIn(chosen.pop(), valid, "_repair returned an invalid repair")

        self.assertIsNone(engines._repair(S2, random.Random(14), avail2,
                                          forbid=frozenset(valid)),
                          "_repair found a repair the reference says cannot work")

    def test_repair_is_a_noop_on_an_intact_set(self):
        masks = set(circuit_masks(RECORD_88_7))
        out = engines._repair(masks, random.Random(15))
        self.assertEqual(set(out), masks)


class _StubCtx:
    """The run context the engines talk to, reduced to the verify-before-claim
    contract: every candidate an engine surfaces is oracle-verified here."""

    def __init__(self, testcase, cap=None):
        self.tc = testcase
        self.cap = cap
        self.claimed = []
        self.logs = []

    def log(self, msg):
        self.logs.append(msg)

    def improve(self, gates, masks, note=""):
        v = core.verify(gates, max_depth=self.cap)
        self.tc.assertTrue(v["ok"], "engine surfaced an unverified circuit: %s" % v)
        # the value-set an engine reports must be the circuit it just handed over
        sig = [1 << i for i in range(32)]
        for a, b in gates:
            sig.append(sig[a] ^ sig[b])
        self.tc.assertEqual(set(sig[32:]), set(masks),
                            "reported masks do not match the reported gates")
        self.claimed.append((v["gates"], v["depth"]))
        return True


class EngineVerifyBeforeClaim(unittest.TestCase):
    """Bounded live runs. Short on purpose: this checks the contract, not the
    search quality."""

    def test_walk_only_surfaces_verified_circuits(self):
        ctx = _StubCtx(self)
        seed = circuit_masks(SEED_90)
        knobs = dict(hub_move_p=0.35, close_hamming=4, repair_hub=40,
                     repair_one=24, plateau_slack_p=0.02)
        engines.run_engine("walk", seed, None, None, 6, [3], knobs, ctx)
        self.assertTrue(ctx.claimed)
        self.assertLessEqual(min(g for g, _ in ctx.claimed), 90)

    def test_lns_only_surfaces_verified_circuits_within_the_cap(self):
        ctx = _StubCtx(self, cap=5)
        seed = circuit_masks(SEED_90)
        knobs = dict(op_mix={"small": 0.5, "coneinj": 0.5},
                     kmax=4, cone_lo=2, cone_hi=4, kshake=12,
                     nsamp=(8, 8), hot_frac=0.5, vic_cost=3, peel_window=4,
                     accept="sa", sa_T0=1.2, sa_cool=0.9997, sa_reheat=4000,
                     snapback=12)
        engines.run_engine("lns", seed, 5, None, 6, [7], knobs, ctx)
        self.assertTrue(ctx.claimed)
        self.assertLessEqual(min(g for g, _ in ctx.claimed), 90)
        self.assertTrue(all(d <= 5 for _, d in ctx.claimed))


class VerifierCLI(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "verify_circuit.py")]
                              + [str(a) for a in args],
                              capture_output=True, text=True)

    def test_no_args_prints_usage_and_exits_2(self):
        r = self._run()
        self.assertEqual(r.returncode, 2)
        self.assertIn("usage:", r.stdout)

    def test_every_record_passes_at_its_depth(self):
        for name, (gate_count, depth) in sorted(RECORDS.items()):
            r = self._run(CIRCUIT_DIR / name, depth)
            self.assertEqual(r.returncode, 0, name + ": " + r.stdout + r.stderr)
            self.assertIn("VALID", r.stdout)
            self.assertIn("gates=%d depth=%d outputs_built=32/32" % (gate_count, depth),
                          r.stdout)

    def test_every_record_fails_one_level_tighter(self):
        """Through the CLI, for all eight: the stated depth is the true depth, so
        the same circuit must be rejected at depth-1 with exit code 1."""
        for name, (_gate_count, depth) in sorted(RECORDS.items()):
            r = self._run(CIRCUIT_DIR / name, depth - 1)
            self.assertEqual(r.returncode, 1, name + ": " + r.stdout + r.stderr)
            self.assertIn("VIOLATED", r.stdout)
            self.assertIn("INVALID", r.stdout)


if __name__ == "__main__":
    unittest.main()
