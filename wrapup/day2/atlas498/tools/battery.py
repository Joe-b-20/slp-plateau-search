#!/usr/bin/env python3
"""Structural battery over the 498 distinct 88-gate mask sets in
atlas/corner/out/*.plat.  Reuses, does not reinvent:

  atlas/corner/socle.py   l3_of              (l3 / s3, socle plane)
  atlas/anatomy.py        replay/target_masks/rho/wt/byte_pat
  atlas/economy.py        classify, sectors_of, SECTOR_SPAN   (8-sector profile)
  atlas/sectors.py        span_dim, xtime_sector              (plane usage)
  atlas/ring.py           mask_to_ring, to_v
  e17_pure/laneY/code/ylib.py  Analysis      (kappa / counted / Y / A*)
  wrapup/tools/corpus88.py     canon, replay, count_B         (identity, B)
  verify_circuit.py            mixcolumns_target_masks

Writes wrapup/day2/atlas498/profiles.jsonl   (one row per distinct mask set).
Single thread, no writes outside the output dir.
"""
import os, sys, glob, json, hashlib, itertools
from collections import Counter, defaultdict

ROOT = "/home/joebachir20/xor_ui/slp-plateau-search"
ATLAS = os.path.join(ROOT, "atlas")
CORNER = os.path.join(ATLAS, "corner")
OUT = os.path.join(ROOT, "wrapup/day2/atlas498")
RECORDS = "/home/joebachir20/xor_ui/aes_mc_records"

sys.path.insert(0, ROOT)
sys.path.insert(0, ATLAS)
sys.path.insert(0, CORNER)
sys.path.insert(0, os.path.join(ROOT, "experiments/e17_pure/laneY/code"))

from verify_circuit import mixcolumns_target_masks
from socle import l3_of
from anatomy import replay, rho, wt, byte_pat
from economy import classify, sectors_of
from sectors import span_dim, xtime_sector
from ring import mask_to_ring, to_v
import ylib

TARGETS = mixcolumns_target_masks()
TSET = set(TARGETS)


def canon(masks):
    return hashlib.sha256(
        ','.join('%08x' % m for m in sorted(masks)).encode()).hexdigest()[:16]


def depth_of(pairs):
    dep = [0] * 32
    for a, b in pairs:
        dep.append(max(dep[a], dep[b]) + 1)
    return max(dep)


def count_B(pairs, masks):
    n = len(pairs)
    cons = [0] * n
    for a, b in pairs:
        for x in (a, b):
            if x >= 32:
                cons[x - 32] += 1
    return sum(1 for g in range(n) if masks[g] not in TSET and cons[g])


# ------------------------------------------------------------------ ingest
seen = {}          # key -> record
order = []
rows88 = 0
for p in sorted(glob.glob(os.path.join(CORNER, "out/*.plat"))):
    rel = os.path.relpath(p, ROOT)
    for ln, line in enumerate(open(p)):
        t = line.split()
        if not t or int(t[0]) != 88:
            continue
        rows88 += 1
        v = [int(x) for x in t[1:]]
        pairs = [(v[2 * i], v[2 * i + 1]) for i in range(88)]
        sig = replay(pairs)
        masks = sig[32:]
        key = tuple(sorted(masks))
        if key in seen:
            seen[key]["n_rows"] += 1
            if len(seen[key]["rows"]) < 4:
                seen[key]["rows"].append("%s#L%d" % (rel, ln + 1))
            continue
        seen[key] = {"canon": canon(masks), "src": "%s#L%d" % (rel, ln + 1),
                     "rows": ["%s#L%d" % (rel, ln + 1)], "n_rows": 1,
                     "pairs": pairs, "masks": masks, "sig": sig}
        order.append(key)
print("88-gate plat rows:", rows88, " distinct mask sets:", len(seen),
      file=sys.stderr)

# --------------------------------------------------- reference 88s (records)
REF88 = {}
for n, f in [("88@5", "mixcolumns_88gates_depth5.json"),
             ("88@5fs", "mixcolumns_88gates_depth5_fromscratch.json"),
             ("88@6", "mixcolumns_88gates_depth6.json"),
             ("88@7", "mixcolumns_88gates_depth7.json"),
             ("88@8", "mixcolumns_88gates_depth8.json")]:
    d = json.load(open(os.path.join(RECORDS, "circuits", f)))
    g = d["gates"] if isinstance(d, dict) else d
    pr = [(x[0], x[1]) if not isinstance(x, dict) else (x["a"], x["b"]) for x in g]
    REF88[n] = set(replay(pr)[32:])

# --------------------------------------------------------------- per-circuit
recs = []
for key in order:
    e = seen[key]
    pairs, masks, sig = e["pairs"], e["masks"], e["sig"]
    cnt = Counter(masks)

    # --- structural battery ---------------------------------------------
    n_distinct = len(cnt)
    dup_masks = sum(c - 1 for c in cnt.values() if c > 1)

    use = Counter()
    for a, b in pairs:
        use[a] += 1
        use[b] += 1
    dead = [k for k in range(88) if use[32 + k] == 0 and masks[k] not in TSET]

    rho_equivariant = all(cnt[m] == cnt[rho(m)] for m in cnt)
    rho_present = sum(1 for m in masks if cnt[rho(m)] > 0)

    whist = Counter(wt(m) for m in masks)
    bhist = Counter(sum(byte_pat(m)) for m in masks)

    # 8-sector profile + plane usage (economy.classify / sectors.span_dim)
    kinds = Counter()
    sect_use = Counter()          # gates confined to exactly sector k
    dimhist = Counter()
    xt_ok = 0
    xt_sectors = Counter()
    for k in range(88):
        z = to_v(mask_to_ring(masks[k]))
        kind, arg = classify(z)
        kinds[kind] += 1
        ss = sectors_of(z)
        if len(ss) == 1:
            sect_use[ss[0]] += 1
        d, _ = span_dim([c for c in z if c])
        dimhist[d] += 1
        s = xtime_sector(z)
        if s is not None:
            xt_ok += 1
            xt_sectors["%02x" % s] += 1

    # socle plane
    l3 = l3_of(pairs)

    # e17 kappa / counted / Y / A*  + the {p,q} tap profile
    an = ylib.Analysis([list(x) for x in pairs], T=TARGETS)
    aprof = tuple(sorted(wt(m) for m in an.Astar))

    # distance to the five published 88s
    ms = set(masks)
    dref = {n: len(ms & r) for n, r in REF88.items()}

    recs.append({
        "canon": e["canon"], "src": e["src"], "n_plat_rows": e["n_rows"],
        "gates": 88, "depth": depth_of(pairs), "B": count_B(pairs, masks),
        "n_masks_distinct": n_distinct, "dup_masks": dup_masks,
        "n_dead": len(dead),
        "l3": l3, "s3": 88 - l3,
        "kappa": an.kappa, "counted": len(an.counted), "Y": an.Y,
        "Astar": len(an.Astar), "Astar_weights": list(aprof),
        "Y_minus_kappa": an.Y - an.kappa,
        "partition_exact": bool(88 == an.kappa + len(an.counted) + an.Y),
        "tree_ok": bool(an.tree_ok),
        "rho_equivariant": bool(rho_equivariant),
        "masks_with_rho_image": rho_present,
        "weight_hist": {str(k): v for k, v in sorted(whist.items())},
        "bytes_touched_hist": {str(k): v for k, v in sorted(bhist.items())},
        "econ_kinds": {str(k): v for k, v in sorted(kinds.items())},
        "sector_use": {str(k): sect_use.get(k, 0) for k in range(8)},
        "n_sector_confined": sum(sect_use.values()),
        "n_glue": kinds.get("glue", 0),
        "span_dim_hist": {str(k): v for k, v in sorted(dimhist.items())},
        "xtime_confined": xt_ok,
        "xtime_sector_use": dict(sorted(xt_sectors.items())),
        "overlap_records88": dref,
        "max_overlap_records88": max(dref.values()),
        "rows": e["rows"],
    })

# ------------------------------------------------------- pairwise distances
sets = [set(seen[k]["masks"]) for k in order]
best = [0] * len(sets)
bestj = [None] * len(sets)
pairhist = Counter()
for i in range(len(sets)):
    for j in range(i + 1, len(sets)):
        o = len(sets[i] & sets[j])
        pairhist[o] += 1
        if o > best[i]:
            best[i], bestj[i] = o, j
        if o > best[j]:
            best[j], bestj[j] = o, i
for i, r in enumerate(recs):
    r["nn_overlap"] = best[i]
    r["nn_canon"] = recs[bestj[i]]["canon"] if bestj[i] is not None else None

with open(os.path.join(OUT, "profiles.jsonl"), "w") as f:
    for r in recs:
        f.write(json.dumps(r) + "\n")

summ = {
    "plat_rows_88": rows88, "distinct": len(seen),
    "l3_hist": dict(sorted(Counter(r["l3"] for r in recs).items())),
    "depth_hist": dict(sorted(Counter(r["depth"] for r in recs).items())),
    "B_hist": dict(sorted(Counter(r["B"] for r in recs).items())),
    "dup_masks_nonzero": sum(1 for r in recs if r["dup_masks"]),
    "dead_nonzero": sum(1 for r in recs if r["n_dead"]),
    "rho_equivariant": sum(1 for r in recs if r["rho_equivariant"]),
    "kappa_hist": dict(sorted(Counter(r["kappa"] for r in recs).items())),
    "Astar_hist": dict(sorted(Counter(r["Astar"] for r in recs).items())),
    "Astar_weight_multiset_top20": {
        str(k): v for k, v in sorted(
            Counter(tuple(r["Astar_weights"]) for r in recs).items(),
            key=lambda kv: -kv[1])[:20]},
    "Astar_weight_support_hist": dict(sorted(Counter(
        w for r in recs for w in r["Astar_weights"]).items())),
    "glue_hist": dict(sorted(Counter(r["n_glue"] for r in recs).items())),
    "sector_confined_hist": dict(sorted(
        Counter(r["n_sector_confined"] for r in recs).items())),
    "span_dim_hist_agg": dict(sorted(Counter(
        int(k) for r in recs for k, v in r["span_dim_hist"].items()
        for _ in range(v)).items())),
    "max_overlap_records88_hist": dict(sorted(
        Counter(r["max_overlap_records88"] for r in recs).items())),
    "pair_overlap_hist": dict(sorted(pairhist.items())),
    "pair_overlap_max": max(pairhist),
    "best_neighbour_hist": dict(sorted(Counter(best).items())),
    "partition_exact": sum(1 for r in recs if r["partition_exact"]),
    "tree_ok": sum(1 for r in recs if r["tree_ok"]),
}
json.dump(summ, open(os.path.join(OUT, "summary.json"), "w"), indent=1)
print(json.dumps(summ)[:4000])
