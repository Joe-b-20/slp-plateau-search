#!/usr/bin/env python3
"""Convert e_upstream S*.json / FLOOR*.json mask-set files to oracle format.

The e_upstream floors are stored as {"pinned":m,"root":..,"gates_reached":n,
"masks":[...]}.  verify_circuit.py needs index pairs (signals 0..31 = inputs,
gate k -> signal 32+k).  We recover a build order by greedy topological
construction: repeatedly emit any not-yet-built mask that is the XOR of two
already-available signals.  If the set is realizable this terminates with every
mask emitted, and the emitted order IS a valid straight-line program.

Output: wrapup/day2/e_upstream/circuits/<name>.json  {"gates": [[a,b],...]}
"""
import json, os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, REPO)
from verify_circuit import mixcolumns_target_masks

T = set(mixcolumns_target_masks())
LANE = [sum(1 << (8 * b + j) for b in range(4)) for j in range(8)]
def nodd(m): return sum(1 for j in range(8) if bin(m & LANE[j]).count("1") & 1)
def nlane(m): return sum(1 for j in range(8) if m & LANE[j])


def build(masks):
    """Return list of index pairs, or None if not fully realizable."""
    sig = [1 << i for i in range(32)]
    idx = {sig[i]: i for i in range(32)}
    rem = [m for m in masks if m not in idx]
    pairs = []
    progress = True
    while rem and progress:
        progress = False
        nxt = []
        for m in rem:
            if m in idx:
                continue
            found = None
            for a_m, a_i in idx.items():
                b_m = m ^ a_m
                b_i = idx.get(b_m)
                if b_i is not None and b_m != m:
                    found = (a_i, b_i)
                    break
            if found:
                pairs.append([found[0], found[1]])
                idx[m] = 32 + len(pairs) - 1
                progress = True
            else:
                nxt.append(m)
        rem = nxt
    if rem:
        return None, len(rem)
    return pairs, 0


def main():
    outdir = os.path.join(HERE, 'circuits')
    os.makedirs(outdir, exist_ok=True)
    rows = []
    files = sorted(glob.glob(os.path.join(REPO, 'experiments/e_upstream/S*.json')) +
                   glob.glob(os.path.join(REPO, 'experiments/e_upstream/FLOOR*.json')))
    for fn in files:
        d = json.load(open(fn))
        masks = d['masks']
        S = set(masks)
        pin = d['pinned']
        pairs, nbad = build(masks)
        base = os.path.basename(fn)[:-5]
        rec = {
            'file': os.path.relpath(fn, REPO),
            'gates_reached': d['gates_reached'],
            'n_masks': len(masks),
            'n_distinct': len(S),
            'pin': '0x%08x' % pin,
            'pin_nodd': nodd(pin),
            'pin_nlane': nlane(pin),
            'pin_weight': bin(pin).count('1'),
            'pin_present': pin in S,
            'pin_is_target': pin in T,
            'targets_present': len(T & S),
            'root': d['root'],
            'realizable': pairs is not None,
            'unbuildable': nbad,
            'n_gates_emitted': len(pairs) if pairs else None,
            'nodd3_masks': sorted('0x%08x' % m for m in S if m not in T and nodd(m) >= 3),
        }
        if pairs is not None:
            op = os.path.join(outdir, base + '.json')
            json.dump({'gates': pairs}, open(op, 'w'))
            rec['oracle_file'] = os.path.relpath(op, REPO)
        rows.append(rec)
    json.dump(rows, open(os.path.join(HERE, 'convert.json'), 'w'), indent=1)
    for r in rows:
        print('%-28s masks=%d distinct=%d gates=%s targets=%d pin=%s nodd=%d present=%s bad=%d nodd3=%d'
              % (os.path.basename(r['file']), r['n_masks'], r['n_distinct'],
                 r['n_gates_emitted'], r['targets_present'], r['pin'], r['pin_nodd'],
                 r['pin_present'], r['unbuildable'], len(r['nodd3_masks'])))


main()
