#!/usr/bin/env python3
"""MANDATORY CONTROL for the strengthened depth-3 LP.

Checks that the verified 97-gate depth-3 circuit is a FEASIBLE point of the
LP with objective 65.  Consequences:
  * the LP is a genuine relaxation (its optimum <= 65), so any bound it
    proves is <= 97 in total -- it cannot be vacuously above the truth;
  * every valid inequality is satisfied by a real depth-3 circuit.
A FAIL here makes every bound from this model VACUOUS.
"""
import sys
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3')
from build_lp import build, control_point
from collections import Counter


def main():
    rows, cost, meta = build(True)
    p = control_point(meta)
    obj = sum(c * v for c, v in zip(cost, p))
    bad = Counter()
    for terms, rhs, tag in rows:
        if sum(c * p[j] for j, c in terms) < rhs:
            bad[tag] += 1
    print('rows %d  vars %d' % (len(rows), meta['nvar']))
    print('row tags:', dict(Counter(t for _, _, t in rows)))
    print('control objective |L1|+|L2| = %d  (total %d gates)' % (obj, obj + 32))
    print('violated rows:', dict(bad) if bad else 'NONE')
    ok = (not bad) and obj == 65
    print('CONTROL', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
