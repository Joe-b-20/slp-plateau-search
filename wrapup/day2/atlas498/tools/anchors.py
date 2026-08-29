#!/usr/bin/env python3
"""Extract every l3 <= 66 row of atlas/corner/out/*.plat as a proper circuit
JSON under wrapup/day2/atlas498/anchors/, and decompose l3 into the three
mechanisms socle.py:l3_of uses (socle-valued / class-alias / DCE-dead)."""
import os, sys, json, hashlib
ROOT = "/home/joebachir20/xor_ui/slp-plateau-search"
ATLAS = ROOT + "/atlas"; CORNER = ATLAS + "/corner"
OUT = ROOT + "/wrapup/day2/atlas498/anchors"
sys.path.insert(0, ROOT); sys.path.insert(0, ATLAS); sys.path.insert(0, CORNER)
from anatomy import replay, target_masks
from socle import proj
from verify_circuit import mixcolumns_target_masks
os.makedirs(OUT, exist_ok=True)
TSET = set(mixcolumns_target_masks())


def l3_parts(gates):
    """Same walk as socle.l3_of, but reporting where the 88-l3 gates go."""
    sig = replay(gates)
    n = len(sig)
    rep = {}; alias = list(range(n))
    for i in range(32):
        rep.setdefault(proj(sig[i]), i); alias[i] = rep[proj(sig[i])]
    keep = []; socle_valued = 0; class_alias = 0
    for k, (a, b) in enumerate(gates):
        i = 32 + k; c = proj(sig[i])
        if c == 0:
            alias[i] = -1; socle_valued += 1; continue
        if c in rep:
            alias[i] = rep[c]; class_alias += 1; continue
        rep[c] = i; alias[i] = i; keep.append(i)
    need = set()
    for t in target_masks():
        c = proj(t)
        if c in rep:
            need.add(rep[c])
    stack = list(need)
    while stack:
        i = stack.pop()
        if i < 32:
            continue
        a, b = gates[i - 32]
        for x in (alias[a], alias[b]):
            if x >= 32 and x not in need:
                need.add(x); stack.append(x)
    l3 = len([i for i in keep if i in need])
    return dict(l3=l3, s3=len(gates) - l3, socle_valued=socle_valued,
                class_alias=class_alias, dce_dead=len(keep) - l3,
                new_classes=len(keep))


prof = {json.loads(l)["canon"]: json.loads(l)
        for l in open(ROOT + "/wrapup/day2/atlas498/profiles.jsonl")}
want = {c: r for c, r in prof.items() if r["l3"] <= 66}
rows = []
for c, r in sorted(want.items(), key=lambda kv: (kv[1]["l3"], kv[1]["src"])):
    path, ln = r["src"].split("#L")
    line = open(os.path.join(ROOT, path)).read().splitlines()[int(ln) - 1]
    v = [int(x) for x in line.split()]
    assert v[0] == 88
    gates = [[v[1 + 2 * i], v[2 + 2 * i]] for i in range(88)]
    sig = replay([tuple(g) for g in gates])
    name = "atlas498_l3_%d_%s.json" % (r["l3"], c)
    outsig = [sig.index(t) for t in mixcolumns_target_masks()]
    json.dump({"name": name[:-5], "gateCount": 88, "depth": r["depth"],
               "gates": gates, "outputSignals": outsig,
               "provenance": {"source": r["src"], "canon": c,
                              "extracted": "wrapup/day2/atlas498 (2026-08-29)",
                              "note": "row of the atlas corrected-ruler "
                                      "plateau walker, never analysed by the "
                                      "atlas session"},
               "l3": r["l3"], "s3": r["s3"]},
              open(os.path.join(OUT, name), "w"), indent=1)
    p = l3_parts([tuple(g) for g in gates])
    assert p["l3"] == r["l3"], (p, r["l3"])
    rows.append(dict(file=name, canon=c, src=r["src"], depth=r["depth"],
                     kappa=r["kappa"], Astar=r["Astar"], glue=r["n_glue"],
                     nn=r["nn_overlap"], maxref=r["max_overlap_records88"],
                     **p))
json.dump(rows, open(ROOT + "/wrapup/day2/atlas498/anchors_l3le66.json", "w"),
          indent=1)
for r in rows:
    print("%3d s3=%2d socle=%2d alias=%2d dce=%2d d=%2d kap=%2d %s"
          % (r["l3"], r["s3"], r["socle_valued"], r["class_alias"],
             r["dce_dead"], r["depth"], r["kappa"], r["file"]))
