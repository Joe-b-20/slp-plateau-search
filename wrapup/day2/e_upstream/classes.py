#!/usr/bin/env python3
"""Price the five never-priced e_upstream feature classes by pure counting,
over (a) the 33 verified e_upstream floor circuits, (b) the 72 from-scratch
roots, (c) the six record 88s.  No solver.

Classes (e_upstream/NOTEBOOK.md 5):
  C1 |odd(m)| >= 4
  C2 the 388 weight-2 masks in e_w2novel/candidates.json
  C3 mask weight >= 12
  C4 fan-out >= 8 on one mask         (DAG property, not mask-set property)
  C5 the column-parity hubs T_j = 0x01010101<<j absent from every record 88
"""
import json, os, sys, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, REPO)
from verify_circuit import mixcolumns_target_masks

T = set(mixcolumns_target_masks())
LANE = [sum(1 << (8 * b + j) for b in range(4)) for j in range(8)]
def nodd(m): return sum(1 for j in range(8) if bin(m & LANE[j]).count('1') & 1)
def nlane(m): return sum(1 for j in range(8) if m & LANE[j])
W2NOVEL = set(json.load(open(os.path.join(REPO, 'experiments/e_w2novel/candidates.json'))))
ALLW2 = {(1 << i) | (1 << j) for i in range(32) for j in range(i + 1, 32)}

print('== sanity on the class definitions ==')
print('weight-2 masks total C(32,2) =', len(ALLW2))
print('e_w2novel candidates =', len(W2NOVEL), 'all weight 2:',
      all(bin(m).count('1') == 2 for m in W2NOVEL), 'subset of all w2:', W2NOVEL <= ALLW2)
print('implied weight-2 masks PRESENT in the corpus =', len(ALLW2) - len(W2NOVEL))
print('hubs T_j =', ['0x%08x' % x for x in LANE], 'nodd', [nodd(x) for x in LANE],
      'weight', [bin(x).count('1') for x in LANE])
print()


def report(name, masks, pairs=None):
    S = set(masks)
    nt = [m for m in S if m not in T]
    fan = None
    if pairs:
        c = collections.Counter()
        for a, b in pairs:
            c[a] += 1; c[b] += 1
        fan = max(c.values())
    return dict(
        name=name, n=len(S),
        c1_odd4=sorted('0x%08x' % m for m in nt if nodd(m) >= 4),
        c1_odd3=sorted('0x%08x' % m for m in nt if nodd(m) == 3),
        c2_w2novel=sorted('0x%08x' % m for m in S if m in W2NOVEL),
        c3_w12=sorted('0x%08x' % m for m in nt if bin(m).count('1') >= 12),
        maxwt=max(bin(m).count('1') for m in nt),
        c4_maxfanout=fan,
        c5_hubs=[j for j in range(8) if LANE[j] in S],
    )


rows = []
print('== (a) the 33 e_upstream floor circuits ==')
for fn in sorted(glob.glob(os.path.join(REPO, 'experiments/e_upstream/S*.json'))):
    d = json.load(open(fn))
    base = os.path.basename(fn)[:-5]
    cp = os.path.join(HERE, 'circuits', base + '.json')
    pairs = json.load(open(cp))['gates'] if os.path.exists(cp) else None
    r = report(base, d['masks'], pairs)
    rows.append(r)
    print('%-26s n=%d odd4=%d odd3=%d w2novel=%d w>=12=%d maxwt=%d maxfan=%s hubs=%s'
          % (r['name'], r['n'], len(r['c1_odd4']), len(r['c1_odd3']), len(r['c2_w2novel']),
             len(r['c3_w12']), r['maxwt'], r['c4_maxfanout'], r['c5_hubs']))

agg = dict(
    n_floors=len(rows),
    floors_with_odd4=sum(1 for r in rows if r['c1_odd4']),
    floors_with_w2novel=sum(1 for r in rows if r['c2_w2novel']),
    floors_with_w12=sum(1 for r in rows if r['c3_w12']),
    floors_with_fanout8=sum(1 for r in rows if r['c4_maxfanout'] and r['c4_maxfanout'] >= 8),
    max_fanout_over_floors=max(r['c4_maxfanout'] for r in rows),
    max_weight_over_floors=max(r['maxwt'] for r in rows),
    hubs_seen=sorted(set(j for r in rows for j in r['c5_hubs'])),
    w2novel_seen=sorted(set(m for r in rows for m in r['c2_w2novel'])),
    odd4_seen=sorted(set(m for r in rows for m in r['c1_odd4'])),
)
print()
print('aggregate over the 33 floors:', json.dumps(agg, indent=1))

print()
print('== (b) the 72 from-scratch roots (upstream abundance) ==')
rootrows = []
for f in sorted(glob.glob(os.path.join(REPO, 'campaign_87/novelty/roots/*.json'))):
    try:
        g = json.load(open(f))['gates']
    except Exception:
        continue
    s = [1 << i for i in range(32)]
    for a, b in g:
        s.append(s[a] ^ s[b])
    M = set(s[32:])
    c = collections.Counter()
    for a, b in g:
        c[a] += 1; c[b] += 1
    nt = [m for m in M if m not in T]
    rootrows.append(dict(
        f=os.path.basename(f), gates=len(g),
        odd3=sum(1 for m in nt if nodd(m) >= 3),
        odd4=sum(1 for m in nt if nodd(m) >= 4),
        odd5=sum(1 for m in nt if nodd(m) >= 5),
        w2novel=sum(1 for m in M if m in W2NOVEL),
        w12=sum(1 for m in nt if bin(m).count('1') >= 12),
        maxfan=max(c.values()),
        hubs=[j for j in range(8) if LANE[j] in M],
    ))
print('roots:', len(rootrows))
for k in ('odd3', 'odd4', 'odd5', 'w2novel', 'w12'):
    n = sum(1 for r in rootrows if r[k])
    tot = sum(r[k] for r in rootrows)
    print('  roots carrying %-8s : %2d/%d   total occurrences %d' % (k, n, len(rootrows), tot))
print('  roots with max fan-out >= 8 : %d/%d  (max over roots = %d)'
      % (sum(1 for r in rootrows if r['maxfan'] >= 8), len(rootrows),
         max(r['maxfan'] for r in rootrows)))
hubcnt = collections.Counter(j for r in rootrows for j in r['hubs'])
print('  hub T_j occurrences over roots:', dict(sorted(hubcnt.items())))

print()
print('== (c) the record 88s ==')
recs = []
for p in sorted(glob.glob(os.path.join(REPO, 'evidence/circuits/*.json'))) + \
        sorted(glob.glob(os.path.join(REPO, 'evidence/campaign87_imported_prior_art/*.json'))):
    try:
        d = json.load(open(p))
    except Exception:
        continue
    g = d.get('gates') if isinstance(d, dict) else d
    if not (isinstance(g, list) and g and isinstance(g[0], list) and len(g) == 88):
        continue
    s = [1 << i for i in range(32)]
    for a, b in g:
        s.append(s[a] ^ s[b])
    r = report(os.path.basename(p), s[32:], g)
    recs.append(r)
    print('%-58s hubs=%s maxfan=%d maxwt=%d w2novel=%d odd3=%d'
          % (r['name'], r['c5_hubs'], r['c4_maxfanout'], r['maxwt'],
             len(r['c2_w2novel']), len(r['c1_odd3'])))
present = sorted(set(j for r in recs for j in r['c5_hubs']))
print('hubs present in >=1 record 88:', present)
print('hubs absent from EVERY record 88:', [j for j in range(8) if j not in present])

json.dump(dict(floors=rows, aggregate=agg, roots=rootrows, records=recs),
          open(os.path.join(HERE, 'classes.json'), 'w'), indent=1)
