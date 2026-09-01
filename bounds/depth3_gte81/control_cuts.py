#!/usr/bin/env python3
"""SOUNDNESS CONTROL: every cut in cuts.py must be satisfied by the verified
97-gate depth-3 circuit (and by any other real depth-3 circuit we can get).

A cut violated by a genuine depth-3 circuit is an UNSOUND cut and every bound
derived with it is VACUOUS.  This is the mandatory positive control for the
strengthened model.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys, json
from mcmatrix import TARGETS
from model3 import candidates, pc
import cuts as CUT
from control_primal import masks_and_depths, CIRC


def main():
    g = json.load(open(CIRC))['gates']
    sig, dep = masks_and_depths(g)
    X = set(); Y = set()
    for k in range(len(g)):
        m, d = sig[32 + k], dep[32 + k]
        if d == 1:
            X.add(m)
        elif d == 2:
            Y.add(m)
    decomp, L2, E = candidates()
    Eset = set(E)
    fam = [('C1/C2 building', CUT.cuts_building(L2)),
           ('C3 target-L2', CUT.cuts_target_l2(decomp, TARGETS)),
           ('C4/C5 w7 matching', CUT.cuts_w7_matching(TARGETS, Eset)),
           ('C6 w5 edges', CUT.cuts_w5(TARGETS, Eset)),
           ('C7 aggregate', [CUT.cut_aggregate_degree(decomp, TARGETS)])]
    bad_total = 0
    for name, cs in fam:
        bad = 0
        for xs, ys, b in cs:
            lhs = sum(1 for e in xs if e in X) + sum(c for m, c in ys if m in Y)
            if lhs < b - 1e-9:
                bad += 1
                if bad <= 3:
                    print('   VIOLATION in %s: lhs=%s rhs=%s' % (name, lhs, b))
        print(' %-22s %6d cuts, %d violated' % (name, len(cs), bad))
        bad_total += bad
    print(' CONTROL', 'PASS' if bad_total == 0 else 'FAIL (%d)' % bad_total)
    return 0 if bad_total == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
