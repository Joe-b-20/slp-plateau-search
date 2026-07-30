#!/usr/bin/env python3
"""Exhaustive k=2 / k=3 shell sweep of one circuit, with the repo's own decider.

    python3 shell_sweep.py <circuit.json> <k> <out.log> [shard nshards]

k=2 enumerates every C(p,2) window of the p non-target masks and asks the
budget-1 decider "can one new mask restore all 32 targets?"; k=3 enumerates
every C(p,3) window at budget 2. Both budgets are exhaustive -- complete by the
first-unlock case analysis proved in the docstring of
../../campaign87_certificates/code/exact_window.py -- so `irreducible` on every
window is a machine-checked proof for that radius, not a failed search. A
`win`/`free` verdict would be an 87-gate circuit and is logged loudly.

Sharding is by window index and is only for wall-clock; the union of the shards
is the full enumeration. Written for the two 88s added in v3.0.0; it works on
any circuit JSON the repo's oracle accepts.
"""
import itertools
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
sys.path.insert(0, os.path.join(ROOT, "evidence", "campaign87_certificates", "code"))
import mixcolumns_core as core          # noqa: E402
import exact_window as ew               # noqa: E402

path, k, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
shard, nsh = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (0, 1)
S = frozenset(core.load_circuit_masks(path))
nont = sorted(S - set(core.TARGETS))
budget = k - 1
t0 = time.time()
n = hits = 0
stats = {}
with open(out, "w") as fh:
    print("circuit %s  masks=%d periphery=%d  k=%d budget=%d  shard %d/%d"
          % (os.path.basename(path), len(S), len(nont), k, budget, shard, nsh),
          file=fh, flush=True)
    for i, w in enumerate(itertools.combinations(nont, k)):
        if i % nsh != shard:
            continue
        r = ew.solve_window(S, set(w), budget)
        st = r["status"]
        stats[st] = stats.get(st, 0) + 1
        n += 1
        if st in ("win", "free"):
            hits += 1
            print("HIT %s %s %s" % (st, [hex(m) for m in w], r.get("masks")),
                  file=fh, flush=True)
        if n % 2000 == 0:
            print("progress %d %.0fs %s" % (n, time.time() - t0, stats),
                  file=fh, flush=True)
    print("DONE windows=%d hits=%d %.0fs stats=%s"
          % (n, hits, time.time() - t0, stats), file=fh, flush=True)
print("%s k=%d shard %d: windows=%d hits=%d %.0fs %s"
      % (os.path.basename(path), k, shard, n, hits, time.time() - t0, stats))
