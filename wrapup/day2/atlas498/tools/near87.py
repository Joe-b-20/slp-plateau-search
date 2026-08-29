#!/usr/bin/env python3
"""Every pair of the 498 whose mask sets overlap in 87 gives an 87-MASK SET
that still contains all 32 MixColumns targets (targets are in every valid 88).
The only remaining question for such a set is REALISABILITY as an XOR-SLP.
Test it with wrapup/tools/corpus88.py:realisable (the project's own check).

Also does the same for every single-mask deletion of every one of the 498
(88 x 498 = 43,824 candidate 87-mask sets) -- the exhaustive deletion test,
strictly stronger than the B = 56 test, which only asks whether a middle has
a consumer, not whether its consumers have an alternative derivation.
"""
import os, sys, json, glob, time
from collections import Counter
ROOT = "/home/joebachir20/xor_ui/slp-plateau-search"
sys.path.insert(0, ROOT); sys.path.insert(0, ROOT + "/wrapup/tools")
sys.path.insert(0, ROOT + "/atlas")
from verify_circuit import mixcolumns_target_masks
from anatomy import replay
from corpus88 import realisable
T = set(mixcolumns_target_masks())

recs = [json.loads(l) for l in open(ROOT + "/wrapup/day2/atlas498/profiles.jsonl")]
sets = []
for r in recs:
    p, ln = r["src"].split("#L")
    v = [int(x) for x in open(os.path.join(ROOT, p)).read().splitlines()[int(ln) - 1].split()]
    pairs = [(v[1 + 2 * i], v[2 + 2 * i]) for i in range(88)]
    sets.append(set(replay(pairs)[32:]))

# --- 1. pairs at overlap 87 -------------------------------------------------
hits = []
for i in range(len(sets)):
    for j in range(i + 1, len(sets)):
        inter = sets[i] & sets[j]
        if len(inter) == 87:
            hits.append((i, j, inter))
print("pairs of the 498 with |M_i cap M_j| = 87:", len(hits))
ok = 0
for i, j, inter in hits:
    assert T <= inter, "targets not contained!"
    if realisable(inter):
        ok += 1
        print("!!! REALISABLE 87-MASK SET", recs[i]["canon"], recs[j]["canon"])
print("  all contain the 32 targets:", all(T <= h[2] for h in hits))
print("  realisable as an XOR-SLP:", ok, "/", len(hits))

# --- 2. exhaustive single-mask deletion over all 498 ------------------------
# Necessary condition first (cheap): with A = inputs u S, x in S\{m} must keep
# at least one pair {a,b} c A\{m} with a^b = x.  Survivors get the full greedy.
INP = [1 << i for i in range(32)]
t0 = time.monotonic()
tot = del_ok = survivors = 0
for k, S in enumerate(sets):
    A = set(INP) | S
    deriv = {x: [] for x in S}            # x -> list of frozenset pairs
    Al = sorted(A)
    for a in Al:
        for b in Al:
            if b <= a:
                continue
            x = a ^ b
            if x in deriv:
                deriv[x].append((a, b))
    for m in S:
        if m in T:
            continue                      # deleting a target loses an output
        tot += 1
        bad = False
        for x, ps in deriv.items():
            if x == m:
                continue
            if not any(m != a and m != b for a, b in ps):
                bad = True
                break
        if bad:
            continue
        survivors += 1
        if realisable(S - {m}):
            del_ok += 1
            print("!!! DELETABLE", recs[k]["canon"], "%08x" % m)
print("single-mask deletions tested (non-target masks only):", tot,
      "passed the necessary condition:", survivors,
      "realisable:", del_ok, "secs", round(time.monotonic() - t0, 1))
json.dump({"pairs_overlap87": len(hits),
           "pairs_overlap87_all_contain_targets": bool(all(T <= h[2] for h in hits)),
           "pairs_overlap87_realisable": ok,
           "deletions_tested": tot, "deletions_realisable": del_ok,
           "pairs": [[recs[i]["canon"], recs[j]["canon"]] for i, j, _ in hits]},
          open(ROOT + "/wrapup/day2/atlas498/near87.json", "w"), indent=1)
