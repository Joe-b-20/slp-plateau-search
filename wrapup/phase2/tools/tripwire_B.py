#!/usr/bin/env python3
"""tripwire_B.py -- the B = n - q counter, ported to an arbitrary GF(2) target.

PORTED FROM  experiments/e15_campaign3/tools/sweep.py:count_B (line ~296), whose
docstring carries the theorem (AUDIT3-verified; ARCH3 R53, binding).  The
counting logic is reused verbatim; only the source of the target set and the
constant 56 are generalised.

    B(C) = #{ gates g : g is NOT an output gate AND g has a consumer }

THEOREM (general form).  Let T be a target set of q DISTINCT masks, none of
them an input mask, and let C be a valid n-gate XOR circuit for T.  Then

        B(C) <= n - q            always, and
        B(C) == n - q            unless an (n-1)-gate circuit for T exists.

Proof sketch (the sweep.py argument, unchanged).  Validity puts all q targets
on gates, so the number of gates carrying a target mask is >= q, hence the
number of non-output gates is <= n - q and B <= n - q.  Equality fails in
exactly two ways, and each hands you an (n-1):
  * two gates carry the SAME mask -> the later one is redundant; rewire its
    consumers to the earlier and delete it;
  * a non-output gate has no consumer -> it is dead; delete it.
So B != n - q on a VALID n-gate circuit is a constructive one-gate improvement.

    for this project: n = 88, q = 32  =>  B = 56 on every irreducible 88.
    for InvMixColumns: same q = 32; B = n - 32 for whatever n turns up.

CONTRAPOSITIVE = AN (n-1) DETECTOR.  It is free, it is always-on, and it is
sound on ANY circuit from ANY source -- which is what makes it the right first
instrument to point at a foreign circuit.

Usage:
  python3 tripwire_B.py --target <matrix.json> <circuit.json> [more.json ...]
  python3 tripwire_B.py --target <matrix.json> --list paths.txt [--jsonl out]
  python3 tripwire_B.py --calibrate --target <matrix.json>
Exit 0 iff every circuit examined is valid and clean (B == n - q).
Exit 1 if any circuit trips the wire or fails validity.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from verify_slp_generic import load_target, load_index_pairs, Refused   # noqa: E402


class Circ:
    """Minimal circuit model -- the fields count_B needs, generalised.

    Ported from experiments/e15_campaign3/tools/cut.py:Circ; identical
    construction of sig / cons / isout, with TSET supplied instead of imported
    from the MixColumns spec.
    """

    def __init__(self, gates, tset, n_in=32):
        self.gates = gates
        self.n = len(gates)
        self.n_in = n_in
        self.sig = [1 << i for i in range(n_in)]
        for a, b in gates:
            self.sig.append(self.sig[a] ^ self.sig[b])
        self.cons = [[] for _ in range(self.n)]
        self.prod = [[] for _ in range(self.n)]
        for k, (a, b) in enumerate(gates):
            for x in (a, b):
                if x >= n_in:
                    self.cons[x - n_in].append(k)
                    self.prod[k].append(x - n_in)
        self.isout = [self.sig[n_in + k] in tset for k in range(self.n)]


def count_B(c):
    """B = number of non-output gates that have a consumer.

    VERBATIM from sweep.py:count_B -- the body is one line and this is it.
    """
    return sum(1 for g in range(c.n) if not c.isout[g] and c.cons[g])


def analyse(path, spec, n_in=32):
    """Returns a dict: validity, n, q, B, expected, verdict, and the cause."""
    tset = set(spec)
    q = len(tset)
    try:
        pairs = load_index_pairs(json.load(open(path)))
    except Exception as e:
        return {"file": path, "error": f"unreadable: {e}", "ok": False}
    for k, g in enumerate(pairs):
        if len(g) != 2 or not (0 <= g[0] < n_in + k) or not (0 <= g[1] < n_in + k):
            return {"file": path, "error": f"gate {k} malformed/forward-referencing",
                    "ok": False}
    c = Circ([tuple(g) for g in pairs], tset, n_in)
    built = len(set(c.sig[n_in:]) & tset)
    n = c.n
    B = count_B(c)
    exp = n - q
    r = {"file": path, "n": n, "q": q, "outputs_built": built,
         "valid": built == q, "B": B, "expected_B": exp, "clean": B == exp}
    # localise the cause when the wire trips
    if not r["clean"]:
        seen, dup = {}, []
        for g in range(n):
            m = c.sig[n_in + g]
            if m in seen:
                dup.append((seen[m], g, hex(m)))
            else:
                seen[m] = g
        dead = [g for g in range(n) if not c.isout[g] and not c.cons[g]]
        outgates = sum(1 for g in range(n) if c.isout[g])
        r["duplicate_masks"] = dup[:8]
        r["n_duplicate_masks"] = len(dup)
        r["dead_gates"] = dead[:8]
        r["n_dead_gates"] = len(dead)
        r["output_carrying_gates"] = outgates
        causes = []
        if dup:
            causes.append(f"{len(dup)} duplicated mask(s) -> delete the later one")
        if dead:
            causes.append(f"{len(dead)} consumer-less non-output gate(s) -> delete")
        r["cause"] = "; ".join(causes) or "unexplained (investigate)"
    r["ok"] = r["valid"] and r["clean"]
    return r


def fmt(r):
    if "error" in r:
        return f"  {os.path.basename(r['file']):<48} ERROR {r['error']}"
    tag = "clean" if r["clean"] else "TRIPPED"
    v = "valid" if r["valid"] else "INVALID"
    s = (f"  {os.path.basename(r['file']):<48} n={r['n']:<4} q={r['q']} "
         f"B={r['B']:<4} expect n-q={r['expected_B']:<4} {v} {tag}")
    if not r["clean"]:
        s += (f"\n      cause: {r['cause']}"
              f"\n      => an ({r['n'] - 1})-gate circuit is available by deletion")
    return s


# --------------------------------------------------------------- calibration
def _synth(base_pairs, kind):
    """Build a positive control from a clean circuit (law 6: an instrument that
    cannot fail is not evidence)."""
    g = [list(p) for p in base_pairs]
    if kind == "dead":
        # append a gate nobody consumes and which carries no target mask
        g.append([0, 1])
    elif kind == "dup":
        # append a gate recomputing an existing gate's mask (duplicate)
        a, b = g[10]
        g.append([a, b])
    return g


def calibrate(spec, base, n_in=32):
    print("-- calibration (positive + negative controls) " + "-" * 28)
    tset = set(spec)
    q = len(tset)
    pairs = load_index_pairs(json.load(open(base)))
    ok = True

    r = analyse(base, spec, n_in)
    good = r["valid"] and r["clean"]
    print(f"   NEGATIVE control (must stay silent): {os.path.basename(base)}")
    print(fmt(r))
    print(f"     -> {'PASS' if good else 'FAIL'}")
    ok &= good

    import tempfile
    for kind, why in (("dead", "consumer-less non-output gate"),
                      ("dup", "duplicated gate mask")):
        gg = _synth(pairs, kind)
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
            json.dump({"gates": gg}, f)
            p = f.name
        r = analyse(p, spec, n_in)
        fired = r["valid"] and not r["clean"]
        print(f"   POSITIVE control (must fire): base + {why}")
        print(fmt(r))
        print(f"     -> {'PASS' if fired else 'FAIL'}")
        ok &= fired
        os.unlink(p)
    print(f"   CALIBRATION: {'PASS' if ok else 'FAIL'}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--target', required=True, help='target matrix json (with provenance)')
    ap.add_argument('files', nargs='*')
    ap.add_argument('--list', help='file containing one circuit path per line')
    ap.add_argument('--jsonl', help='write one json record per circuit here')
    ap.add_argument('--calibrate', metavar='BASE_CIRCUIT', nargs='?', const=True,
                    help='run the calibration controls on a known-clean circuit')
    a = ap.parse_args()

    try:
        spec, n_in, info = load_target(a.target)
    except Refused as e:
        print(f"REFUSED: {e}")
        sys.exit(3)
    print(f"target={info['name']} q={len(spec)} inputs={n_in} rank={info['rank']} "
          f"rows_sha256={info['sha256'][:16]}")
    print(f"target rebuilt: {info['rederived']}")
    print(f"theorem: B = n - {len(spec)} on any valid, irreducible circuit; "
          f"B != n - {len(spec)} yields an (n-1) by deletion")
    print()

    files = list(a.files)
    if a.list:
        with open(a.list) as f:
            files += [l.strip() for l in f if l.strip() and not l.startswith('#')]

    ok = True
    if a.calibrate:
        base = a.calibrate if a.calibrate is not True else (files[0] if files else None)
        if not base:
            print("--calibrate needs a known-clean base circuit")
            sys.exit(2)
        ok &= calibrate(spec, base, n_in)
        print()

    if files:
        print("-- circuits " + "-" * 62)
        recs = []
        for p in files:
            r = analyse(p, spec, n_in)
            recs.append(r)
            print(fmt(r))
            ok &= r["ok"]
        if a.jsonl:
            with open(a.jsonl, 'w') as f:
                for r in recs:
                    f.write(json.dumps(r) + '\n')
        n_clean = sum(1 for r in recs if r.get("ok"))
        print(f"   {n_clean}/{len(recs)} valid and clean (B == n - {len(spec)})")

    print()
    print("VERDICT:", "ALL CLEAN" if ok else "TRIPWIRE FIRED / CONTROL FAILED")
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
