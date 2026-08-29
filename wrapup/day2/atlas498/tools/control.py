#!/usr/bin/env python3
"""Control arm: run the same battery on (a) the five published 88s and
(b) a seeded random sample of the e15 Run-A census (pop88.pkl), so the 498 can
be compared to something.  Same tools, same code path as battery.py."""
import os, sys, json, random, pickle, time
from collections import Counter
ROOT = "/home/joebachir20/xor_ui/slp-plateau-search"
ATLAS = ROOT + "/atlas"; CORNER = ATLAS + "/corner"
RECORDS = "/home/joebachir20/xor_ui/aes_mc_records"
OUT = ROOT + "/wrapup/day2/atlas498"
sys.path.insert(0, ROOT); sys.path.insert(0, ATLAS); sys.path.insert(0, CORNER)
sys.path.insert(0, ROOT + "/experiments/e17_pure/laneY/code")
from verify_circuit import mixcolumns_target_masks, load_index_pairs
from socle import l3_of, proj
from anatomy import replay, rho, wt
from economy import classify, sectors_of
from sectors import span_dim
from ring import mask_to_ring, to_v
import ylib
TARGETS = mixcolumns_target_masks(); TSET = set(TARGETS)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 800


def row(pairs, tag):
    sig = replay(pairs); masks = sig[32:]
    cnt = Counter(masks)
    use = Counter()
    for a, b in pairs:
        use[a] += 1; use[b] += 1
    dep = [0] * 32
    for a, b in pairs:
        dep.append(max(dep[a], dep[b]) + 1)
    cons = [0] * len(pairs)
    for a, b in pairs:
        for x in (a, b):
            if x >= 32:
                cons[x - 32] += 1
    kinds = Counter(); sect = Counter(); dimh = Counter()
    for m in masks:
        z = to_v(mask_to_ring(m))
        kinds[classify(z)[0]] += 1
        ss = sectors_of(z)
        if len(ss) == 1:
            sect[ss[0]] += 1
        dimh[span_dim([c for c in z if c])[0]] += 1
    an = ylib.Analysis([list(x) for x in pairs], T=TARGETS)
    return dict(tag=tag, n=len(pairs), depth=max(dep),
                B=sum(1 for g in range(len(pairs))
                      if masks[g] not in TSET and cons[g]),
                dup=sum(c - 1 for c in cnt.values() if c > 1),
                dead=sum(1 for k in range(len(pairs))
                         if use[32 + k] == 0 and masks[k] not in TSET),
                l3=l3_of(pairs), kappa=an.kappa, Astar=len(an.Astar), Y=an.Y,
                Astar_weights=sorted(wt(m) for m in an.Astar),
                rho_eq=all(cnt[m] == cnt[rho(m)] for m in cnt),
                glue=kinds.get("glue", 0), sect_conf=sum(sect.values()),
                span_dim=dict(sorted(dimh.items())))


def pairs_of(path):
    return [tuple(x) for x in load_index_pairs(json.load(open(path)))]


out = []
for n, f in [("88@5", "mixcolumns_88gates_depth5.json"),
             ("88@5fs", "mixcolumns_88gates_depth5_fromscratch.json"),
             ("88@6", "mixcolumns_88gates_depth6.json"),
             ("88@7", "mixcolumns_88gates_depth7.json"),
             ("88@8", "mixcolumns_88gates_depth8.json")]:
    out.append(row(pairs_of(os.path.join(RECORDS, "circuits", f)), n))
for r in out:
    print(json.dumps(r))

pop = pickle.load(open(ROOT + "/experiments/e15_campaign3/tools/pop88.pkl", "rb"))
random.seed(20260829)
samp = random.sample(range(len(pop)), min(N, len(pop)))
cen = []
t0 = time.monotonic(); miss = 0
for i in samp:
    p = pop[i][0]
    try:
        cen.append(row(pairs_of(p), "census"))
    except Exception:
        miss += 1
print("census sampled", len(cen), "missing/unreadable", miss,
      "secs", round(time.monotonic() - t0, 1), file=sys.stderr)
json.dump({"records5": out, "census_sample": cen, "census_n": len(cen),
           "census_seed": 20260829, "census_requested": N,
           "census_unreadable": miss},
          open(OUT + "/control.json", "w"))


def h(rs, k):
    return dict(sorted(Counter(r[k] for r in rs).items()))


for k in ("l3", "kappa", "Astar", "depth", "B", "glue", "sect_conf", "dup",
          "dead", "rho_eq", "Y"):
    print("census", k, h(cen, k))
