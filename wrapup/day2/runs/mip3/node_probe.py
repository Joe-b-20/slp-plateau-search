#!/usr/bin/env python3
"""Probe one node of the certified branch tree.

A node fixes aggregate counts:  sum_e x_e == E,  sum_m y_m == Y,
optionally sum_{wt(m)=4} y_m == Y4.  Reports LP feasibility / value and, when
feasible, the EXACT certified bound for that node (same arithmetic as
branch_certify.py: dual from the primal marginals, overshoot charged against
the 0<=p<=1 bounds).

Usage: node_probe.py E Y [Y4min Y4max]
"""
import sys, json, time, math
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3')
from build_lp import build
from model3 import pc
from branch_certify import exact_bound

HERE = '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3'
DEN = 10 ** 12


def solve(rows0, cost, meta, extra):
    n = meta['nvar']
    rows = rows0 + extra
    r, ci, va, b = [], [], [], []
    for i, (terms, rhs, tag) in enumerate(rows):
        for j, cf in terms:
            r.append(i); ci.append(j); va.append(cf)
        b.append(rhs)
    A = coo_matrix((va, (r, ci)), shape=(len(rows), n)).tocsr()
    res = linprog(np.array(cost, float), A_ub=(-A).tocsc(),
                  b_ub=-np.array(b, float), bounds=[(0, 1)] * n, method='highs')
    if res.status == 2:
        return {'infeasible': True}
    if res.status != 0:
        return {'status': res.status}
    u = np.maximum(-np.asarray(res.ineqlin.marginals), 0.0)
    un = [int(round(v * DEN)) for v in u]
    got = exact_bound(rows, cost, un, DEN)
    out = {'lp': float(res.fun)}
    if got:
        val, over = got
        out.update(certified_numerator=val, denominator=DEN,
                   overshoot_numerator=over,
                   certified_bound=math.ceil(val / DEN - 1e-15))
    return out


def main():
    E, Y = int(sys.argv[1]), int(sys.argv[2])
    rows0, cost, meta = build(True, 1)
    xs = [meta['xi'][e] for e in meta['E']]
    ys = [meta['yi'][m] for m in meta['L2']]
    y4 = [meta['yi'][m] for m in meta['L2'] if pc(m) == 4]
    base = [([(j, 1) for j in xs], E, 'E'), ([(j, -1) for j in xs], -E, 'E_ub'),
            ([(j, 1) for j in ys], Y, 'Y'), ([(j, -1) for j in ys], -Y, 'Y_ub')]
    if len(sys.argv) > 4:
        recs = []
        for v in range(int(sys.argv[3]), int(sys.argv[4]) + 1):
            t0 = time.monotonic()
            r = solve(rows0, cost, meta,
                      base + [([(j, 1) for j in y4], v, 'Y4'),
                              ([(j, -1) for j in y4], -v, 'Y4_ub')])
            r.update(E=E, Y=Y, Y4=v, wall=time.monotonic() - t0)
            recs.append(r)
            print(json.dumps(r), flush=True)
            json.dump(recs, open(HERE + '/node_E%d_Y%d.json' % (E, Y), 'w'), indent=1)
    else:
        t0 = time.monotonic()
        r = solve(rows0, cost, meta, base)
        r.update(E=E, Y=Y, wall=time.monotonic() - t0)
        print(json.dumps(r), flush=True)


if __name__ == '__main__':
    main()
