#!/usr/bin/env python3
"""Deletion certificates for the 33 e_upstream floors (2026-08-29).

Mask-set analogue of e15's B=56 tripwire (wrapup/CORPUS88.md 4): if a non-target
mask can be dropped with the remaining set still realizable from the 32 input
singletons, the circuit is secretly one gate cheaper.

Reports, per floor:
  - every single non-target mask whose deletion leaves a realizable set
  - whether any such deletion preserves the pinned mask
  - for the pin specifically: which masks become unbuildable if it is removed

The pair-deletion sweep (58,496 pairs, 265 s) is banked separately in
deletion_pairs.log -- it is the same predicate over all non-target pairs.
"""
import json, os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, REPO)
from verify_circuit import mixcolumns_target_masks

T = set(mixcolumns_target_masks())
INP = frozenset(1 << i for i in range(32))
LANE = [sum(1 << (8 * b + j) for b in range(4)) for j in range(8)]
def nodd(m): return sum(1 for j in range(8) if bin(m & LANE[j]).count('1') & 1)


def unbuildable(S):
    av = set(INP)
    rem = set(S) - av
    prog = True
    while rem and prog:
        prog = False
        for m in list(rem):
            for a in av:
                if (m ^ a) in av:
                    av.add(m); rem.discard(m); prog = True; break
    return rem


rows = []
n_red = n_pinpres = 0
for fn in sorted(glob.glob(os.path.join(REPO, 'experiments/e_upstream/S*.json'))):
    d = json.load(open(fn))
    S = set(d['masks']); pin = d['pinned']
    dels = [m for m in S if m not in T and not unbuildable(S - {m})]
    keep = [m for m in dels if m != pin]
    casc = sorted(unbuildable(S - {pin}))
    r = dict(
        name=os.path.basename(fn)[:-5], n=len(S), pin='0x%08x' % pin,
        n_nontarget=len(S - T),
        deletable=['0x%08x' % m for m in dels],
        deletable_is_only_the_pin=(dels == [pin]),
        pin_preserving_deletions=['0x%08x' % m for m in keep],
        cascade_on_pin_removal=['0x%08x%s' % (m, ' TARGET' if m in T else '') for m in casc],
        n_cascade=len(casc), n_cascade_targets=sum(1 for m in casc if m in T),
    )
    rows.append(r)
    n_red += bool(dels); n_pinpres += len(keep)
    print('%-26s n=%d nontarget=%d deletable=%d only_pin=%s pin_preserving=%d '
          'cascade_on_pin=%d (targets %d)'
          % (r['name'], r['n'], r['n_nontarget'], len(dels), r['deletable_is_only_the_pin'],
             len(keep), r['n_cascade'], r['n_cascade_targets']))

summary = dict(n_floors=len(rows), floors_reducible_by_1=n_red,
               pin_preserving_deletions_total=n_pinpres,
               floors_where_only_deletable_mask_is_the_pin=sum(
                   1 for r in rows if r['deletable']and r['deletable_is_only_the_pin']))
print()
print(json.dumps(summary, indent=1))
json.dump(dict(summary=summary, floors=rows), open(os.path.join(HERE, 'deletions.json'), 'w'), indent=1)
