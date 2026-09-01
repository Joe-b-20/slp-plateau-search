#!/usr/bin/env python3
"""overlap.py -- how much do two XOR circuits for the same map have in common?

Standard library only. No dependencies. Python 3.6+.

WHAT IT MEASURES
----------------
Every gate in a straight-line XOR circuit over 32 inputs computes an XOR of
some subset of those inputs.  Write that subset as a 32-bit number and call it
the gate's MASK (elsewhere: its "intermediate value").  A circuit of n gates
therefore has a set of at most n masks -- what it knows how to build.

    shared      = | masks(A)  &  masks(B) |
    Jaccard     = | masks(A)  &  masks(B) |  /  | masks(A) | masks(B) |

Two circuits found by unrelated searches for the same map will still share a
lot: the 32 output masks are forced, and low-weight combinations are hard to
avoid.  So a high overlap is NOT by itself evidence that one was copied from
the other, and a low overlap is NOT a proof of independence.  This script
reports a number; the interpretation belongs in prose next to a calibration
pair.  (This project uses 0.7 as its "same family" line, and reports the
Jaccard between two independently PUBLISHED circuits alongside its own, so the
reader can see what independence actually looks like for this map.)

The comparison is over SETS, so it does not care about gate order, about which
signal index a mask lands on, or about how the file was formatted.

WHAT IT DOES NOT DO
-------------------
It does not check that either circuit is correct.  Feed it two files of
nonsense and it will happily tell you how much nonsense they share.  Run the
verifier first.

INPUT FORMATS (both files may be in different formats)
------------------------------------------------------
  1. JSON object   {"gates": [[a, b], ...]}          (extra keys ignored)
  2. JSON array    [[a, b], ...]
  3. JSON object   {"gates": [{"m":..,"a":..,"b":..}, ...]}   mask triples
  4. Plain text    one gate per line, "a b" (whitespace separated).
                   Blank lines and lines starting with # are skipped.

In every index form: signals 0..31 are the circuit inputs, and gate k (0-based)
produces signal 32 + k.  Both parents of a gate must be strictly earlier
signals.

USAGE
-----
    python3 overlap.py A.json B.json
    python3 overlap.py A.json B.txt --inputs 32
    python3 overlap.py A.json B.json --list-shared
    python3 overlap.py A.json B.json --json

EXIT STATUS
-----------
    0  both files parsed and the report was printed
    2  a file could not be parsed as any accepted format
"""

import argparse
import json
import os
import sys


# --------------------------------------------------------------- parsing ---
def _pairs_from_obj(data):
    """Normalise any accepted JSON shape to a list of [a, b] index pairs."""
    gates = data if isinstance(data, list) else data.get("gates")
    if gates is None:
        raise ValueError('JSON object has no "gates" key')
    if not gates:
        return []
    if isinstance(gates[0], dict):
        # mask triples in build order: rebuild the index pairs
        idx = {(1 << i): i for i in range(32)}
        pairs = []
        for k, g in enumerate(gates):
            m = int(g["m"]) & 0xFFFFFFFF
            a = int(g["a"]) & 0xFFFFFFFF
            b = int(g["b"]) & 0xFFFFFFFF
            if a not in idx or b not in idx:
                raise ValueError(
                    "gate %d: a parent mask is not built yet (%#x or %#x)" % (k, a, b))
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
            raise ValueError("line %d: expected two integers, got %r" % (lineno, raw))
        pairs.append([int(parts[0]), int(parts[1])])
    return pairs


def load_pairs(path):
    """Read a circuit file in any accepted format. Returns [[a, b], ...]."""
    with open(path) as f:
        text = f.read()
    stripped = text.lstrip()
    if stripped[:1] in "[{":
        try:
            return _pairs_from_obj(json.loads(text))
        except ValueError as e:
            raise ValueError("%s: not a readable circuit JSON (%s)" % (path, e))
    try:
        return _pairs_from_text(text)
    except ValueError as e:
        raise ValueError("%s: not a readable 'a b' per line file (%s)" % (path, e))


# ---------------------------------------------------------------- masks ----
def masks_of(pairs, n_in=32):
    """The mask each gate computes, in build order. Inputs are 1<<i."""
    sig = [1 << i for i in range(n_in)]
    for k, (a, b) in enumerate(pairs):
        top = n_in + k
        if not (0 <= a < top and 0 <= b < top):
            raise ValueError(
                "gate %d references signal %d/%d, which is not strictly earlier"
                % (k, a, b))
        sig.append(sig[a] ^ sig[b])
    return sig[n_in:]


# --------------------------------------------------------------- report ----
def compare(pa, pb, n_in=32):
    ma, mb = masks_of(pa, n_in), masks_of(pb, n_in)
    sa, sb = set(ma), set(mb)
    inter = sa & sb
    union = sa | sb
    return {
        "gates_a": len(ma), "gates_b": len(mb),
        "distinct_masks_a": len(sa), "distinct_masks_b": len(sb),
        "repeated_masks_a": len(ma) - len(sa),
        "repeated_masks_b": len(mb) - len(sb),
        "shared": len(inter), "union": len(union),
        "jaccard": (len(inter) / len(union)) if union else 0.0,
        "shared_masks": sorted(inter),
        "only_a": len(sa - sb), "only_b": len(sb - sa),
    }


def main():
    ap = argparse.ArgumentParser(
        description="Shared intermediate values between two XOR circuits.")
    ap.add_argument("a", help="first circuit file")
    ap.add_argument("b", help="second circuit file")
    ap.add_argument("--inputs", type=int, default=32,
                    help="number of circuit inputs (default 32)")
    ap.add_argument("--list-shared", action="store_true",
                    help="also print every shared mask in hex")
    ap.add_argument("--json", action="store_true",
                    help="emit the report as one JSON object and nothing else")
    args = ap.parse_args()

    try:
        pa = load_pairs(args.a)
        pb = load_pairs(args.b)
        r = compare(pa, pb, args.inputs)
    except (ValueError, OSError) as e:
        sys.stderr.write("ERROR: %s\n" % e)
        sys.exit(2)

    if args.json:
        if not args.list_shared:
            r.pop("shared_masks")
        else:
            r["shared_masks"] = ["0x%08x" % m for m in r["shared_masks"]]
        print(json.dumps(r, indent=2))
        return

    na, nb = os.path.basename(args.a), os.path.basename(args.b)
    w = max(len(na), len(nb), 6)
    print("overlap of intermediate values (masks)")
    print("-" * 62)
    print("  A  %-*s  %d gates, %d distinct masks%s"
          % (w, na, r["gates_a"], r["distinct_masks_a"],
             "" if not r["repeated_masks_a"]
             else "  (%d gate(s) recompute a mask another gate already has)"
                  % r["repeated_masks_a"]))
    print("  B  %-*s  %d gates, %d distinct masks%s"
          % (w, nb, r["gates_b"], r["distinct_masks_b"],
             "" if not r["repeated_masks_b"]
             else "  (%d gate(s) recompute a mask another gate already has)"
                  % r["repeated_masks_b"]))
    print()
    print("  shared      %d" % r["shared"])
    print("  only in A   %d" % r["only_a"])
    print("  only in B   %d" % r["only_b"])
    print("  union       %d" % r["union"])
    print()
    print("  shared / |A|   = %d/%d = %.3f"
          % (r["shared"], r["distinct_masks_a"],
             r["shared"] / r["distinct_masks_a"] if r["distinct_masks_a"] else 0))
    print("  shared / |B|   = %d/%d = %.3f"
          % (r["shared"], r["distinct_masks_b"],
             r["shared"] / r["distinct_masks_b"] if r["distinct_masks_b"] else 0))
    print("  Jaccard        = %d/%d = %.3f"
          % (r["shared"], r["union"], r["jaccard"]))
    if args.list_shared:
        print()
        print("  shared masks (hex, bit j = input signal j):")
        for i in range(0, len(r["shared_masks"]), 6):
            print("    " + "  ".join("0x%08x" % m
                                     for m in r["shared_masks"][i:i + 6]))
    print()
    print("  NOTE: this script does not check that either circuit is correct.")
    print("        Overlap is not evidence of derivation in either direction;")
    print("        circuits for the same map share their forced output masks")
    print("        no matter who found them.")


if __name__ == "__main__":
    main()
