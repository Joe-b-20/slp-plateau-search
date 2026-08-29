#!/usr/bin/env python3
"""Exact FARKAS certificates for the infeasible branches of branch_certify.py.

Branch E is the LP  A p >= b, p >= 0  with the two extra rows
sum_e x_e >= E and -sum_e x_e >= -E.  If it is infeasible, a vector u >= 0
with A^T u <= 0 and u.b > 0 proves it (for any feasible p we would get
0 >= (A^T u).p >= u.(A p) >= u.b > 0).  The verification is exact integer
arithmetic, same as certify.py.

Usage: farkas.py <Emin> <Emax>   ->  farkas_certificates.json
"""
import sys, json, time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3')
from build_lp import build

HERE = '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3'
DEN = 10 ** 12


def check(rows, n, u_num, den):
    acc = [0] * n
    for i, (terms, rhs, tag) in enumerate(rows):
        ui = u_num[i]
        if ui == 0:
            continue
        if ui < 0:
            return None
        for j, cf in terms:
            acc[j] += cf * ui
    if any(a > 0 for a in acc):
        return None
    return sum(u_num[i] * rows[i][1] for i in range(len(rows)))


def main():
    E0, E1 = int(sys.argv[1]), int(sys.argv[2])
    rows0, cost, meta = build(True, 1)
    n = meta['nvar']
    xs = [meta['xi'][e] for e in meta['E']]
    out = {}
    for E in range(E0, E1 + 1):
        rows = rows0 + [([(j, 1) for j in xs], E, 'edgeE'),
                        ([(j, -1) for j in xs], -E, 'edgeE_ub')]
        r, ci, va, b = [], [], [], []
        for i, (terms, rhs, tag) in enumerate(rows):
            for j, cf in terms:
                r.append(i); ci.append(j); va.append(cf)
            b.append(rhs)
        A = coo_matrix((va, (r, ci)), shape=(len(rows), n)).tocsr()
        bb = np.array(b, dtype=float)
        m = len(rows)
        # max u.b  s.t.  A^T u <= -eps (strict),  0 <= u <= 1
        eps = 1e-7
        res = linprog(-bb, A_ub=A.T.tocsc(), b_ub=-eps * np.ones(n),
                      bounds=[(0, 1)] * m, method='highs')
        ok = False
        if res.status == 0 and -res.fun > 1e-9:
            un = [int(np.floor(v * DEN)) for v in np.maximum(res.x, 0)]
            val = check(rows, n, un, DEN)
            if val is not None and val > 0:
                out[str(E)] = {'value_numerator': val, 'denominator': DEN,
                               'u_nonzero': [[i, v] for i, v in enumerate(un) if v]}
                ok = True
        print('E=%d farkas %s%s' % (E, 'OK' if ok else 'FAILED',
                                    '' if ok else ' (status %s)' % res.status), flush=True)
        json.dump(out, open(HERE + '/farkas_certificates.json', 'w'))
    print('certified infeasible for E in', sorted(int(k) for k in out))


if __name__ == '__main__':
    main()
