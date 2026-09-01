#!/usr/bin/env python3
"""tripwire.py -- point this at an XOR circuit and it tells you, in seconds,
whether a gate can be deleted from it.

Standard library only. No dependencies. Python 3.6+. It is meant to be run on
SOMEBODY ELSE'S circuit file: yours, a paper's, a competitor's, one you just
found. Nothing about it is specific to this project's circuits.


WHAT IT IS FOR
==============

If it fires, you have a smaller circuit, and getting it is a deletion -- no
search, no solver, no re-synthesis. If it stays silent, you have learned that
the one free check there is has nothing to say, which is worth the two seconds
it took.


WHAT IT DOES *NOT* DO
=====================

**It does not check that your circuit is correct.** That is not this tool's
job. It will happily analyse a file that computes the wrong function and tell
you about its duplicate gates. Run a verifier first
(`python3 verify_circuit.py <file>` in this project's records repository
rebuilds AES MixColumns from the GF(2^8) field arithmetic and checks all 32
output bits at once).

It also does not prove your circuit is minimal. Silence means "no gate is
deletable by the two mechanisms below", not "no smaller circuit exists".


THE THREE THINGS IT COMPUTES
============================

Write the MASK of a gate for the set of circuit inputs it XORs together, as a
32-bit number. Call a gate an OUTPUT GATE if its mask is one of the q masks
the circuit is supposed to produce.

1. DUPLICATE MASKS. Two gates computing the same mask. The later one is
   redundant: rewire its consumers to the earlier one and delete it.
   -> an (n-1)-gate circuit, immediately.

2. DEAD GATES. A non-output gate that nothing later consumes. Delete it.
   -> an (n-1)-gate circuit, immediately.

3. B, and what it should be. B = the number of gates that are NOT output
   gates and DO have a consumer -- the working intermediates.

       B <= n - q   always, and   B == n - q   unless (1) or (2) fired.

   Why: validity puts all q target masks on gates, so at least q gates are
   output gates, so at most n - q are not, so B <= n - q. Equality can only
   fail if some gate is counted out -- and the only two ways for a non-output
   gate to be missing from B are that it has no consumer (case 2) or that a
   target mask sits on two gates so fewer than n-q gates are left over
   (case 1). Both hand you a deletion.

   So B != n - q on a valid circuit is not a curiosity: it IS a one-gate
   improvement, constructively.

   READ THE ARROW THE RIGHT WAY ROUND. B != n - q implies a gate is
   deletable. The converse is FALSE, and this tool demonstrates it: if two
   gates duplicate a mask that is NOT one of the q targets, and both have
   consumers, then exactly q gates carry targets and all n - q others are
   working, so B == n - q on the nose -- while check (1) still finds the
   deletable gate. B is a screen, not a decision procedure. Run all three.

For AES MixColumns q = 32, so a valid, irreducible 88-gate circuit has
B = 56 exactly. That number is a **sanity screen with a two-line proof**, not a
deep theorem, and this tool is what it is for.


INPUT FORMATS
=============

  1. JSON object   {"gates": [[a, b], ...]}   (extra keys ignored)
  2. JSON array    [[a, b], ...]
  3. JSON object   {"gates": [{"m":..,"a":..,"b":..}, ...]}   mask triples
  4. Plain text    one gate per line, "a b". Blank lines and # comments skipped.

Signals 0..31 are the circuit inputs; gate k (0-based) produces signal 32 + k;
both parents of a gate must be strictly earlier signals.


TARGET
======

By default the target set is AES MixColumns (forward), rebuilt here from
GF(2^8) with modulus 0x11B -- the code IS the specification, nothing is
transcribed. For any other map, pass `--target matrix.txt`: 32 lines (one per
output) of 32 characters '0'/'1' (one per input), where row i column j is 1 iff
output bit i depends on input bit j.


USAGE
=====

    python3 tripwire.py circuit.json
    python3 tripwire.py *.json
    python3 tripwire.py --target matrix.txt theirs.txt
    python3 tripwire.py --selftest          # prove the instrument can fire

EXIT STATUS
    0  every file examined was silent (no deletable gate found)
    1  the tripwire fired on at least one file, or a self-test failed
    2  a file could not be read
"""

import argparse
import json
import os
import sys


# ------------------------------------------------ the target specification --
def _xtime(a):
    a <<= 1
    return (a ^ 0x11B) & 0xFF if (a & 0x100) else (a & 0xFF)


def _gf_mul(a, b):
    r, t = 0, a
    for i in range(8):
        if (b >> i) & 1:
            r ^= t
        t = _xtime(t)
    return r & 0xFF


def mixcolumns_target_masks():
    """The 32 output masks of AES MixColumns, from the field, not a table.

    Convention: signal index j = 8 * byte + bit, LSB-first inside the byte;
    mask bit c is set iff that output depends on input signal c.
    """
    coef = [2, 3, 1, 1]
    M = [[0] * 32 for _ in range(32)]
    for col in range(4):
        for k in range(4):
            c, ib = coef[k], (col + k) % 4
            for in_bit in range(8):
                v = _gf_mul(c, 1 << in_bit)
                for out_bit in range(8):
                    if (v >> out_bit) & 1:
                        M[col * 8 + out_bit][ib * 8 + in_bit] ^= 1
    masks = []
    for r in range(32):
        m = 0
        for c in range(32):
            if M[r][c]:
                m |= 1 << c
        masks.append(m)
    w = [bin(m).count("1") for m in masks]
    assert w.count(5) == 20 and w.count(7) == 12, "MixColumns self-check failed"
    return masks


def load_target_matrix(path):
    """32 lines of 32 '0'/'1' -> the list of masks. Any n x m is accepted."""
    with open(path) as f:
        rows = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    if not rows:
        raise ValueError("%s: no rows" % path)
    width = len(rows[0])
    masks = []
    for i, row in enumerate(rows):
        if len(row) != width or set(row) - set("01"):
            raise ValueError("%s: row %d is not %d characters of 0/1"
                             % (path, i, width))
        masks.append(sum(1 << c for c in range(width) if row[c] == "1"))
    return masks, width


# --------------------------------------------------------------- parsing ---
def _pairs_from_obj(data):
    gates = data if isinstance(data, list) else data.get("gates")
    if gates is None:
        raise ValueError('JSON object has no "gates" key')
    if not gates:
        return []
    if isinstance(gates[0], dict):
        idx = {(1 << i): i for i in range(32)}
        pairs = []
        for k, g in enumerate(gates):
            m = int(g["m"]) & 0xFFFFFFFF
            a = int(g["a"]) & 0xFFFFFFFF
            b = int(g["b"]) & 0xFFFFFFFF
            if a not in idx or b not in idx:
                raise ValueError("gate %d: parent mask not built yet" % k)
            pairs.append([idx[a], idx[b]])
            idx.setdefault(m, 31 + len(pairs))
        return pairs
    return [[int(g[0]), int(g[1])] for g in gates]


def _pairs_from_text(text):
    pairs = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.replace(",", " ").split()
        if len(parts) != 2:
            raise ValueError("line %d: expected two integers, got %r"
                             % (lineno, raw))
        pairs.append([int(parts[0]), int(parts[1])])
    return pairs


def load_pairs(path):
    with open(path) as f:
        text = f.read()
    if text.lstrip()[:1] in "[{":
        return _pairs_from_obj(json.loads(text))
    return _pairs_from_text(text)


# --------------------------------------------------------------- analysis --
def analyse(pairs, targets, n_in=32):
    tset = set(targets)
    q = len(tset)
    n = len(pairs)

    mask = [1 << i for i in range(n_in)]
    consumers = [0] * n_in
    for k, (a, b) in enumerate(pairs):
        top = n_in + k
        if not (0 <= a < top and 0 <= b < top):
            raise ValueError("gate %d references signal %d/%d, which is not "
                             "strictly earlier" % (k, a, b))
        mask.append(mask[a] ^ mask[b])
        consumers.append(0)
        consumers[a] += 1
        consumers[b] += 1

    is_out = [mask[n_in + k] in tset for k in range(n)]

    seen, dups = {}, []
    for k in range(n):
        m = mask[n_in + k]
        if m in seen:
            dups.append((seen[m], k, m))
        else:
            seen[m] = k

    dead = [k for k in range(n) if not is_out[k] and consumers[n_in + k] == 0]
    B = sum(1 for k in range(n) if not is_out[k] and consumers[n_in + k] > 0)

    built = sum(1 for t in tset if t in seen)

    return {
        "gates": n, "inputs": n_in, "targets": q,
        "targets_present": built,
        "B": B, "expected_B": n - q,
        "duplicate_pairs": dups,
        "dead_gates": dead,
        "fired": bool(dups) or bool(dead) or B != n - q,
    }


def report(path, r):
    name = os.path.basename(path)
    print("=" * 72)
    print(name)
    print("-" * 72)
    print("  %d gates over %d inputs; the target map has %d outputs."
          % (r["gates"], r["inputs"], r["targets"]))
    print("  %d of those %d target values appear somewhere in the circuit."
          % (r["targets_present"], r["targets"]))
    if r["targets_present"] < r["targets"]:
        print("  NOTE: this circuit does not build the whole target map. That "
              "may be")
        print("        the wrong target, or the wrong bit convention, or a "
              "broken")
        print("        circuit -- this tool does not check correctness. The "
              "counts")
        print("        below are still computed, but read them with that in "
              "mind.")
    print()
    print("  duplicate values : %d" % len(r["duplicate_pairs"]))
    print("  dead gates       : %d" % len(r["dead_gates"]))
    print("  working values B : %d   (expected %d = %d gates - %d outputs)"
          % (r["B"], r["expected_B"], r["gates"], r["targets"]))
    print()

    if not r["fired"]:
        print("  RESULT: nothing to delete.")
        print("          No gate computes a value another gate already has,")
        print("          nothing is computed and then ignored, and B is "
              "exactly")
        print("          what an irreducible circuit's B has to be. This test")
        print("          has no objection to the circuit. It has not shown "
              "the")
        print("          circuit is minimal -- that is a different and much")
        print("          harder question.")
        return

    print("  RESULT: *** A GATE CAN BE DELETED. ***")
    print("          You are holding a %d-gate circuit for this map."
          % (r["gates"] - 1))
    print()
    if r["duplicate_pairs"]:
        print("  %d duplicated value(s): two gates compute the same thing."
              % len(r["duplicate_pairs"]))
        print("  Delete the later gate and point whatever read it at the "
              "earlier one.")
        for a, b, m in r["duplicate_pairs"][:10]:
            print("     gate %d and gate %d both compute 0x%08x" % (a, b, m))
        if len(r["duplicate_pairs"]) > 10:
            print("     ... and %d more" % (len(r["duplicate_pairs"]) - 10))
        print()
    if r["dead_gates"]:
        print("  %d dead gate(s): computed, not a target, and nothing reads "
              "them." % len(r["dead_gates"]))
        print("  Delete them outright.")
        print("     gate(s): %s%s"
              % (", ".join(str(g) for g in r["dead_gates"][:10]),
                 " ..." if len(r["dead_gates"]) > 10 else ""))
        print()
    if not r["duplicate_pairs"] and not r["dead_gates"]:
        print("  B is off but neither known cause is present. This should be")
        print("  impossible on a valid circuit; if the circuit really does "
              "build")
        print("  the whole target map, please report the file.")
        print()


# -------------------------------------------------------------- self-test --
def selftest(targets, base_pairs):
    """An instrument that cannot fire is not evidence. Prove this one fires."""
    print("=" * 72)
    print("SELF-TEST")
    print("-" * 72)
    ok = True

    r = analyse(base_pairs, targets)
    good = not r["fired"]
    print("  1. the clean circuit as given            -> %s  (must be silent)"
          % ("silent" if good else "FIRED"))
    ok &= good

    g = [list(p) for p in base_pairs]
    g.append(list(g[len(g) // 2]))
    r = analyse(g, targets)
    good = bool(r["duplicate_pairs"]) and r["fired"]
    print("  2. same circuit + one duplicated gate    -> %s  (must fire)"
          % ("FIRED" if good else "silent -- BROKEN"))
    ok &= good

    g = [list(p) for p in base_pairs]
    g.append([0, 1])
    r = analyse(g, targets)
    good = bool(r["dead_gates"]) and r["fired"]
    print("  3. same circuit + one gate nobody reads  -> %s  (must fire)"
          % ("FIRED" if good else "silent -- BROKEN"))
    ok &= good

    print()
    print("  SELF-TEST: %s" % ("PASS" if ok else "FAIL"))
    print()
    return ok


def main():
    ap = argparse.ArgumentParser(
        description="Find a deletable gate in an XOR circuit, in seconds.")
    ap.add_argument("files", nargs="*", help="circuit files")
    ap.add_argument("--target", metavar="matrix.txt",
                    help="target map as a 0/1 matrix; default is AES "
                         "MixColumns rebuilt from GF(2^8)")
    ap.add_argument("--selftest", action="store_true",
                    help="run the positive/negative controls against the "
                         "first file given (required: the controls plant "
                         "defects into a circuit you supply)")
    ap.add_argument("--quiet", action="store_true",
                    help="one line per file")
    args = ap.parse_args()

    if args.target:
        try:
            targets, n_in = load_target_matrix(args.target)
        except (ValueError, OSError) as e:
            sys.stderr.write("ERROR: %s\n" % e)
            sys.exit(2)
        print("target: %s  (%d outputs over %d inputs)"
              % (args.target, len(targets), n_in))
    else:
        targets, n_in = mixcolumns_target_masks(), 32
        print("target: AES MixColumns (forward), rebuilt from GF(2^8) mod "
              "0x11B -- 32 outputs, 32 inputs")
    print("rule:   B = gates - outputs = n - %d on any valid, irreducible "
          "circuit;" % len(targets))
    print("        any other value hands you an (n-1)-gate circuit by "
          "deletion.")
    print("note:   this tool does NOT check that the circuit is correct.")
    print()

    ok = True
    if args.selftest:
        if args.files:
            try:
                base = load_pairs(args.files[0])
            except (ValueError, OSError) as e:
                sys.stderr.write("ERROR: %s\n" % e)
                sys.exit(2)
        else:
            sys.stderr.write(
                "ERROR: --selftest needs a circuit file to plant defects "
                "into.\n       Give it any valid circuit for the target map, "
                "e.g.\n         python3 tripwire.py --selftest "
                "circuits/mixcolumns_88gates_depth5.json\n")
            sys.exit(2)
        ok &= selftest(targets, base)

    fired_on = []
    for path in args.files:
        try:
            pairs = load_pairs(path)
            r = analyse(pairs, targets, n_in)
        except (ValueError, OSError, json.JSONDecodeError) as e:
            sys.stderr.write("ERROR: %s: %s\n" % (path, e))
            sys.exit(2)
        if args.quiet:
            print("  %-52s n=%-4d B=%-4d expect=%-4d %s"
                  % (os.path.basename(path), r["gates"], r["B"],
                     r["expected_B"],
                     "FIRED" if r["fired"] else "silent"))
        else:
            report(path, r)
        if r["fired"]:
            fired_on.append(path)
            ok = False

    if args.files:
        print("=" * 72)
        if fired_on:
            print("%d of %d file(s) have a deletable gate: %s"
                  % (len(fired_on), len(args.files),
                     ", ".join(os.path.basename(p) for p in fired_on)))
        else:
            print("%d file(s) examined, none has a deletable gate."
                  % len(args.files))
    elif not args.selftest:
        ap.print_help()
        sys.exit(2)

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
