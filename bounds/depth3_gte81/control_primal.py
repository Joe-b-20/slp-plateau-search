#!/usr/bin/env python3
"""POSITIVE CONTROL for the depth-3 model.

Takes the repo's verified 97-gate depth-3 circuit, checks that it fits the
structure theorem (32 target gates at level 3, all other gates weight-2 edges
or weight-3/4 level-2 masks drawn from the candidate sets), and reports the
model objective it realises.  The model's optimum must be <= that value, and
any dual bound we ever claim must be <= it.  A dual bound above this number
would prove the model (or the cut set) UNSOUND.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys, json
from mcmatrix import TARGETS
from model3 import candidates, pc, buildings

CIRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
        'mixcolumns_97gates_depth3.json')


def masks_and_depths(gates):
    sig = [1 << i for i in range(32)]
    dep = [0] * 32
    for a, b in gates:
        sig.append(sig[a] ^ sig[b])
        dep.append(max(dep[a], dep[b]) + 1)
    return sig, dep


def main():
    g = json.load(open(CIRC))['gates']
    sig, dep = masks_and_depths(g)
    G = len(g)
    tgt = set(TARGETS)
    print('gates %d  depth %d' % (G, max(dep)))
    decomp, L2, E = candidates()
    L2s, Es = set(L2), set(E)
    lvl = {1: [], 2: [], 3: []}
    ok = True
    for k in range(G):
        m, d = sig[32 + k], dep[32 + k]
        lvl.setdefault(d, []).append(m)
    for d in sorted(lvl):
        print(' level %d : %d gates, weights %s' %
              (d, len(lvl[d]), sorted(set(pc(m) for m in lvl[d]))))
    l1 = set(lvl.get(1, []))
    l2 = set(lvl.get(2, []))
    l3 = set(lvl.get(3, []))
    print(' level-3 masks == targets:', l3 == tgt, len(l3))
    bad_e = [m for m in l1 if m not in Es]
    bad_m = [m for m in l2 if m not in L2s]
    print(' level-1 masks outside edge candidate set:', len(bad_e))
    print(' level-2 masks outside L2 candidate set  :', len(bad_m))
    obj = len(l1) + len(l2)
    print(' model objective realised (|L1|+|L2|) = %d  -> total %d' % (obj, obj + 32))
    ok = (l3 == tgt) and not bad_e and not bad_m
    print(' CONTROL', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
