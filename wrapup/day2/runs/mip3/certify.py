#!/usr/bin/env python3
"""EXACT rational dual certificate for the depth-3 lower bound.

The LP  min c.p  s.t.  A p >= b,  p >= 0   is a relaxation of the complete
depth-3 model (build_lp.py; every row a theorem, control_lp.py checks them
against the verified 97-gate depth-3 circuit).  Weak duality: for ANY vector
u >= 0 with A^T u <= c we have  c.p >= u.A.p >= u.b  for every feasible p.

So a rational u with those two properties is a self-contained, machine
checkable proof of  |L1| + |L2| >= u.b, i.e.  N_depth3 >= 32 + ceil(u.b).
This script finds u with HiGHS (with a slack margin), rounds it to a common
denominator, and then VERIFIES u >= 0 and A^T u <= c in exact integer
arithmetic before reporting the bound.  Nothing floating point enters the
final claim.

Writes cert_depth3.json  (u as integer numerators over a common denominator)
and is re-checkable by  python3 certify.py --check cert_depth3.json
"""
import sys, json, time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3')
from build_lp import build

HERE = '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3'
DEN = 10 ** 12


def matrices():
    rows, cost, meta = build(True)
    r, cix, val, b = [], [], [], []
    for i, (terms, rhs, tag) in enumerate(rows):
        for j, cf in terms:
            r.append(i); cix.append(j); val.append(cf)
        b.append(rhs)
    m, n = len(rows), meta['nvar']
    A = coo_matrix((val, (r, cix)), shape=(m, n)).tocsr()
    return A, np.array(b, dtype=float), np.array(cost, dtype=float), meta, rows


def exact_check(rows, cost, u_num, den):
    """u = u_num/den.  Verify u >= 0 and A^T u <= c exactly (integers)."""
    n = len(cost)
    acc = [0] * n
    for i, (terms, rhs, tag) in enumerate(rows):
        ui = u_num[i]
        if ui == 0:
            continue
        if ui < 0:
            return None, 'negative dual on row %d' % i
        for j, cf in terms:
            acc[j] += cf * ui
    for j in range(n):
        if acc[j] > cost[j] * den:
            return None, 'A^T u > c at variable %d (%d > %d)' % (j, acc[j], cost[j] * den)
    val = sum(u_num[i] * rows[i][1] for i in range(len(rows)))
    return val, den


def main():
    if len(sys.argv) > 2 and sys.argv[1] == '--check':
        cert = json.load(open(sys.argv[2]))
        rows, cost, meta = build(True)
        assert len(rows) == cert['n_rows'], 'row count mismatch'
        u = [0] * len(rows)
        for i, v in cert['u_nonzero']:
            u[i] = v
        val, den = exact_check(rows, cost, u, cert['denominator'])
        if val is None:
            print('CERTIFICATE INVALID:', den); return 1
        import math
        print('exact dual value = %d/%d = %.6f' % (val, den, val / den))
        print('=> |L1|+|L2| >= %d  =>  N_depth3 >= %d'
              % (-(-val // den), 32 + (-(-val // den))))
        return 0

    t0 = time.monotonic()
    A, b, c, meta, rows = matrices()
    m, n = A.shape
    print('A: %d rows x %d cols, nnz %d' % (m, n, A.nnz), flush=True)
    # primal value with p >= 0 only (no upper bounds) -- the certifiable LP
    res_p = linprog(c, A_ub=(-A).tocsc(), b_ub=-b, bounds=[(0, None)] * n,
                    method='highs')
    print('primal LP (p>=0, no ub): status %d  value %s'
          % (res_p.status, res_p.fun), flush=True)
    # dual with a slack margin so that rounding stays feasible
    AT = A.T.tocsc()
    val = None
    for delta in (1e-6, 1e-7, 1e-8, 1e-9):
        res = linprog(-b, A_ub=AT, b_ub=c - delta, bounds=[(0, None)] * m,
                      method='highs')
        print('dual LP delta=%g: status %d  value %s  (%.1f s)'
              % (delta, res.status, -res.fun if res.fun is not None else None,
                 time.monotonic() - t0), flush=True)
        if res.status != 0:
            continue
        u = np.maximum(res.x, 0.0)
        u_num = [int(np.floor(v * DEN)) for v in u]
        val, den = exact_check(rows, c, u_num, DEN)
        if val is not None:
            break
        print('  rounded certificate infeasible:', den, flush=True)
    if val is None:
        print('no certificate obtained'); return 1
    lb = -(-val // den)                      # ceil
    print('EXACT dual value %d/%d = %.6f' % (val, den, val / den))
    print('CERTIFIED |L1|+|L2| >= %d   =>   N_depth3 >= %d' % (lb, 32 + lb))
    cert = {'n_rows': m, 'n_vars': n, 'denominator': den,
            'u_nonzero': [[i, v] for i, v in enumerate(u_num) if v],
            'exact_dual_value_numerator': val,
            'bound_L1L2': lb, 'bound_N_depth3': 32 + lb,
            'note': 'weak duality certificate for build_lp.build(True); '
                    'verify with python3 certify.py --check cert_depth3.json'}
    json.dump(cert, open(HERE + '/cert_depth3.json', 'w'))
    print('wrote cert_depth3.json (%d nonzero duals)' % len(cert['u_nonzero']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
