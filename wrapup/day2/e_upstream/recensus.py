#!/usr/bin/env python3
"""Day-2 re-census of the 88-gate corpus vocabulary, for e_upstream/RESULT.md.

Re-checks the e_oddlane3 claim "|odd(m)| >= 3 has 0 occurrences in ~184M mask
slots" against a NAMED, reproducible population rather than census.py's
first-line-sniffed file list.

Population P (the five mask-bearing 88-gate banks of wrapup/CORPUS88.md 2.1,
plus the evidence record circuits):
  A campaign_87/wave5_2026-08-04/nrpa/out/sub92.jsonl        (rows with gates==88)
  B campaign_87/agents/merged-engine/runs_hunt/*.pop.jsonl   (bare lists, len 88)
  C campaign_87/agents/hunt-deeper/population88_new.jsonl    (bare lists)
  D beat88/methods/m2_oracle/runs/pop88_worklist.jsonl       ("masks_hex")
  E campaign_87/hunt87_layer89/found88.jsonl                 ({"masks":[...]})
  F evidence/circuits/*.json + the imported Jean 88          (gate lists)

Per accepted row (exactly 88 masks) it measures, over the NON-TARGET masks only
(the same convention as e_oddlane3/census.py):
  #odd-lanes histogram, #lanes histogram, weight histogram,
  the distinct-mask vocabulary V, the weight-2 masks present,
  and the per-circuit count of column-parity hubs LANE[j] present.
Rows missing any of the 32 targets are counted separately and EXCLUDED.

Output: wrapup/day2/e_upstream/recensus.json
"""
import json, os, sys, glob, collections, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, REPO)
from verify_circuit import mixcolumns_target_masks

TARGETS = mixcolumns_target_masks()
T = set(TARGETS)
LANE = [sum(1 << (8 * b + j) for b in range(4)) for j in range(8)]
LANESET = set(LANE)

_st = {}
def st(m):
    r = _st.get(m)
    if r is None:
        nl = no = 0
        for j in range(8):
            v = m & LANE[j]
            if v:
                nl += 1
                if bin(v).count('1') & 1:
                    no += 1
        r = (nl, no, bin(m).count('1'))
        _st[m] = r
    return r

V = set()
lane = collections.Counter(); odd = collections.Counter(); wt = collections.Counter()
hub = collections.Counter()          # #LANE[j] hubs present per circuit
hubj = collections.Counter()         # which j
w2present = set()
nrows = 0; nbadlen = 0; nmissingtarget = 0; nslots = 0
c_odd3 = 0; c_4lane = 0; c_w11 = 0; c_w12 = 0; c_odd4 = 0
odd3_examples = []
persrc = collections.Counter()
t0 = time.time()


def take(ms, src):
    global nrows, nbadlen, nmissingtarget, nslots, c_odd3, c_4lane, c_w11, c_w12, c_odd4
    if len(ms) != 88:
        nbadlen += 1
        return
    S = set(ms)
    if not T <= S:
        nmissingtarget += 1
        return
    nrows += 1
    persrc[src] += 1
    h3 = h4 = h11 = h12 = ho4 = False
    nh = 0
    for m in ms:
        if m in LANESET:
            nh += 1
            hubj[LANE.index(m)] += 1
        if m in T:
            continue
        nl, no, w = st(m)
        V.add(m); lane[nl] += 1; odd[no] += 1; wt[w] += 1
        nslots += 1
        if w == 2:
            w2present.add(m)
        if no >= 3:
            h3 = True
            if len(odd3_examples) < 20:
                odd3_examples.append(['0x%08x' % m, src])
        if no >= 4: ho4 = True
        if nl >= 4: h4 = True
        if w >= 11: h11 = True
        if w >= 12: h12 = True
    hub[nh] += 1
    c_odd3 += h3; c_odd4 += ho4; c_4lane += h4; c_w11 += h11; c_w12 += h12


def parse_list(s):
    return [int(x) for x in s.split(',')]


# ---- A: NRPA sub92 -------------------------------------------------------
p = os.path.join(REPO, 'campaign_87/wave5_2026-08-04/nrpa/out/sub92.jsonl')
for line in open(p):
    if '"gates": 88,' not in line:
        continue
    i = line.find('"masks": [')
    if i < 0:
        continue
    j = line.find(']', i)
    take(parse_list(line[i + 10:j]), 'nrpa_sub92')
print('A nrpa done', nrows, time.time() - t0, flush=True)

# ---- B: merged-engine ----------------------------------------------------
for p in sorted(glob.glob(os.path.join(REPO, 'campaign_87/agents/merged-engine/runs_hunt/*.pop.jsonl'))):
    for line in open(p):
        line = line.strip()
        if not line.startswith('['):
            continue
        take(parse_list(line[1:-1]), 'merged_engine')
print('B merged done', nrows, time.time() - t0, flush=True)

# ---- C: population88_new -------------------------------------------------
p = os.path.join(REPO, 'campaign_87/agents/hunt-deeper/population88_new.jsonl')
for line in open(p):
    line = line.strip()
    if line.startswith('['):
        take(parse_list(line[1:-1]), 'population88_new')
print('C pop88new done', nrows, time.time() - t0, flush=True)

# ---- D: beat88 worklist --------------------------------------------------
p = os.path.join(REPO, 'beat88/methods/m2_oracle/runs/pop88_worklist.jsonl')
for line in open(p):
    i = line.find('"masks_hex": "')
    if i < 0:
        continue
    j = line.find('"', i + 14)
    take([int(x, 16) for x in line[i + 14:j].split(',')], 'beat88_worklist')
print('D beat88 done', nrows, time.time() - t0, flush=True)

# ---- E: found88_layer89 --------------------------------------------------
p = os.path.join(REPO, 'campaign_87/hunt87_layer89/found88.jsonl')
for line in open(p):
    i = line.find('"masks": [')
    if i < 0:
        continue
    j = line.find(']', i)
    take(parse_list(line[i + 10:j]), 'found88_layer89')
print('E layer89 done', nrows, time.time() - t0, flush=True)

# ---- F: evidence record circuits ----------------------------------------
for p in sorted(glob.glob(os.path.join(REPO, 'evidence/circuits/*.json')) +
                glob.glob(os.path.join(REPO, 'evidence/campaign87_imported_prior_art/*.json'))):
    try:
        d = json.load(open(p))
    except Exception:
        continue
    g = d.get('gates') if isinstance(d, dict) else d
    if not (isinstance(g, list) and g and isinstance(g[0], list)):
        continue
    s = [1 << i for i in range(32)]
    for a, b in g:
        s.append(s[a] ^ s[b])
    take(s[32:], 'evidence_records')
print('F evidence done', nrows, time.time() - t0, flush=True)

out = {
    'population': 'wrapup/day2/e_upstream/recensus.py sources A-F',
    'rows_accepted_88_with_all_targets': nrows,
    'rows_rejected_wrong_length': nbadlen,
    'rows_rejected_missing_targets': nmissingtarget,
    'non_target_mask_slots': nslots,
    'distinct_non_target_masks': len(V),
    'odd_lane_histogram': dict(sorted(odd.items())),
    'lane_histogram': dict(sorted(lane.items())),
    'weight_histogram': dict(sorted(wt.items())),
    'circuits_with_odd3': c_odd3,
    'circuits_with_odd4': c_odd4,
    'circuits_with_4lane': c_4lane,
    'circuits_with_weight11': c_w11,
    'circuits_with_weight12': c_w12,
    'odd3_examples': odd3_examples,
    'hub_count_per_circuit_histogram': dict(sorted(hub.items())),
    'hub_j_occurrences': dict(sorted(hubj.items())),
    'weight2_masks_present': sorted(w2present),
    'n_weight2_present': len(w2present),
    'per_source_rows': dict(persrc),
    'seconds': round(time.time() - t0, 1),
}
json.dump(out, open(os.path.join(HERE, 'recensus.json'), 'w'), indent=1)
json.dump(sorted(V), open(os.path.join(HERE, 'vocab.json'), 'w'))
for k, v in out.items():
    if k not in ('weight2_masks_present',):
        print(k, '=', v)
print('vocab written', len(V))
