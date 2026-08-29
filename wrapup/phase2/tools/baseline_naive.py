#!/usr/bin/env python3
"""baseline_naive.py -- the two day-0 numbers for any target matrix.

  NAIVE XOR-TREE   sum_r (popcount(row r) - 1) = density - q.
                   No sharing at all; the number every later result is
                   measured against.  (Catalog B2's "naive root" is a random
                   *tree shape* over this same gate count.)

  PAAR1 GREEDY     the classical cancellation-free common-subexpression greedy
                   (Paar, 1997): repeatedly adopt the pair of current base
                   signals that co-occurs in the most unfinished target rows.
                   Circuit-generic by construction -- it reads only the target
                   matrix.  Ties broken by a seeded RNG, so --restarts prices
                   the tie-break spread.

Emits a real circuit (index pairs, dead gates stripped) so the result can be
handed straight to verify_slp_generic.py -- a baseline that has not been
oracled is not a baseline.

Usage:
  python3 baseline_naive.py --target <matrix.json> [--restarts N] [--seed S]
                            [--emit best_circuit.json]
"""
import argparse
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from verify_slp_generic import load_target, Refused          # noqa: E402


def naive_cost(masks):
    return sum(bin(m).count("1") for m in masks) - len(masks)


def paar1(masks, n_in, rng):
    """Returns (gate_pairs, cost).  gate k produces signal n_in+k."""
    sig = [1 << i for i in range(n_in)]        # value of each base signal
    pairs = []                                 # gate parents, index form
    rows = []                                  # target -> set of base indices
    for m in masks:
        rows.append(set(i for i in range(n_in) if (m >> i) & 1))
    val2idx = {v: i for i, v in enumerate(sig)}

    while any(len(r) > 1 for r in rows):
        # count co-occurrence of every pair of base indices over unfinished rows
        cnt = {}
        for r in rows:
            if len(r) < 2:
                continue
            s = sorted(r)
            for a in range(len(s)):
                for b in range(a + 1, len(s)):
                    k = (s[a], s[b])
                    cnt[k] = cnt.get(k, 0) + 1
        best = max(cnt.values())
        cands = [k for k, v in cnt.items() if v == best]
        i, j = cands[rng.randrange(len(cands))]
        v = sig[i] ^ sig[j]
        if v in val2idx:
            # the pair's value already exists as a signal: reuse, no new gate
            new = val2idx[v]
        else:
            sig.append(v)
            pairs.append([i, j])
            new = len(sig) - 1
            val2idx[v] = new
        for r in rows:
            if i in r and j in r:
                r.discard(i); r.discard(j); r.add(new)
    return pairs, len(pairs)


def strip_dead(pairs, masks, n_in):
    """Catalog A9: every emitted count gets its dead gates stripped."""
    sig = [1 << i for i in range(n_in)]
    for a, b in pairs:
        sig.append(sig[a] ^ sig[b])
    need = set()
    tset = set(masks)
    stack = [k for k in range(len(pairs)) if sig[n_in + k] in tset]
    while stack:
        k = stack.pop()
        if k in need:
            continue
        need.add(k)
        for x in pairs[k]:
            if x >= n_in:
                stack.append(x - n_in)
    keep = sorted(need)
    remap = {n_in + k: n_in + i for i, k in enumerate(keep)}
    out = []
    for k in keep:
        a, b = pairs[k]
        out.append([remap.get(a, a), remap.get(b, b)])
    return out


def depth_of(pairs, n_in):
    d = [0] * n_in
    for a, b in pairs:
        d.append(max(d[a], d[b]) + 1)
    return max(d) if d else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--target', required=True)
    ap.add_argument('--restarts', type=int, default=20)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--emit')
    a = ap.parse_args()
    try:
        masks, n_in, info = load_target(a.target)
    except Refused as e:
        print(f"REFUSED: {e}")
        sys.exit(3)

    print(f"target={info['name']} inputs={n_in} outputs={len(masks)} "
          f"rank={info['rank']} density={info['density']}")
    print(f"target rebuilt: {info['rederived']}")
    print(f"row weights: {sorted(bin(m).count('1') for m in masks)}")
    print()
    nv = naive_cost(masks)
    print(f"NAIVE XOR-TREE   density - q = {info['density']} - {len(masks)} = {nv}")

    best, bestc, costs = None, None, []
    rng = random.Random(a.seed)
    for t in range(a.restarts):
        pairs, c = paar1(masks, n_in, random.Random(rng.randrange(1 << 30)))
        pairs = strip_dead(pairs, masks, n_in)
        c = len(pairs)
        costs.append(c)
        if bestc is None or c < bestc:
            bestc, best = c, pairs
    costs.sort()
    print(f"PAAR1 GREEDY     restarts={a.restarts}  best={costs[0]}  "
          f"median={costs[len(costs)//2]}  worst={costs[-1]}")
    print(f"                 saving vs naive: {nv - costs[0]} gates "
          f"({100.0*(nv-costs[0])/nv:.1f}%)")
    print(f"                 best circuit depth = {depth_of(best, n_in)}")
    if a.emit:
        with open(a.emit, 'w') as f:
            json.dump({"gates": best,
                       "provenance": {"tool": "wrapup/phase2/tools/baseline_naive.py",
                                      "method": "Paar1 greedy",
                                      "target": info['name'],
                                      "target_rows_sha256": info['sha256'],
                                      "restarts": a.restarts, "seed": a.seed,
                                      "gates": len(best),
                                      "depth": depth_of(best, n_in)}}, f, indent=1)
        print(f"emitted {a.emit}  ({len(best)} gates)  -- now run verify_slp_generic.py on it")


if __name__ == '__main__':
    main()
