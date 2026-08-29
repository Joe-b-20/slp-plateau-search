#!/usr/bin/env python3
"""Class C4 (fan-out >= 8 on one mask) is a DAG property, not a mask-set
property: the same 88 masks admit many build orders with different fan-outs.

For a mask set S (32 input singletons + S) define, for each signal s,

    potential(s) = |{ x in SIG, x != s : s ^ x in S }|

i.e. how many masks of S could be produced by a gate that consumes s.  Every
build order realises fan-out(s) <= potential(s), and fan-out(s) can be pushed
towards potential(s) by choosing, for each such mask, the pair that uses s.
(Not always simultaneously achievable -- acyclicity and the "each mask is built
once" rule constrain it -- so potential is an UPPER bound and the greedy figure
is a LOWER bound.)

We report both for the record 88s and the 33 e_upstream floors, plus a greedy
fan-out-maximising scheduler that gives a constructive LOWER bound.
"""
import json, os, sys, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, REPO)
from verify_circuit import mixcolumns_target_masks
T = set(mixcolumns_target_masks())


def potential(S):
    SIG = [1 << i for i in range(32)] + sorted(S)
    SIGSET = set(SIG)
    Sset = set(S)
    best = 0; arg = None
    for s in SIG:
        c = sum(1 for x in SIGSET if x != s and (s ^ x) in Sset)
        if c > best:
            best = c; arg = s
    return best, arg


def greedy_fanout(S, hub):
    """Build S in a valid order, always preferring a pair that uses `hub`."""
    idx = {1 << i: i for i in range(32)}
    rem = set(m for m in S if m not in idx)
    pairs = []
    fan = collections.Counter()
    prog = True
    while rem and prog:
        prog = False
        # pass 1: masks buildable using hub
        for m in sorted(rem):
            if hub in idx and (m ^ hub) in idx and (m ^ hub) != m:
                pairs.append([idx[hub], idx[m ^ hub]])
                fan[hub] += 1; fan[m ^ hub] += 1
                idx[m] = 32 + len(pairs) - 1
                rem.discard(m); prog = True
        if prog:
            continue
        for m in sorted(rem):
            got = None
            for a in idx:
                b = m ^ a
                if b in idx and b != m:
                    got = (a, b); break
            if got:
                pairs.append([idx[got[0]], idx[got[1]]])
                fan[got[0]] += 1; fan[got[1]] += 1
                idx[m] = 32 + len(pairs) - 1
                rem.discard(m); prog = True
    if rem:
        return None, None
    return max(fan.values()), fan[hub] if hub in fan else 0


def run(name, S):
    p, arg = potential(S)
    g, gh = greedy_fanout(S, arg)
    print('%-58s |S|=%3d  potential_max_fanout=%2d (on 0x%08x)  greedy_max=%s  greedy_on_that_signal=%s'
          % (name, len(S), p, arg, g, gh))
    return dict(name=name, n=len(S), potential=p, hub='0x%08x' % arg, greedy_max=g, greedy_on_hub=gh)


rows = []
print('== record 88s ==')
for pth in sorted(glob.glob(os.path.join(REPO, 'evidence/circuits/*.json'))) + \
        sorted(glob.glob(os.path.join(REPO, 'evidence/campaign87_imported_prior_art/*.json'))):
    try:
        d = json.load(open(pth))
    except Exception:
        continue
    g = d.get('gates') if isinstance(d, dict) else d
    if not (isinstance(g, list) and g and isinstance(g[0], list) and len(g) == 88):
        continue
    s = [1 << i for i in range(32)]
    for a, b in g:
        s.append(s[a] ^ s[b])
    rows.append(run(os.path.basename(pth), set(s[32:])))

print()
print('== e_upstream floors ==')
for fn in sorted(glob.glob(os.path.join(REPO, 'experiments/e_upstream/S*.json'))):
    d = json.load(open(fn))
    rows.append(run(os.path.basename(fn)[:-5], set(d['masks'])))

json.dump(rows, open(os.path.join(HERE, 'fanout.json'), 'w'), indent=1)
