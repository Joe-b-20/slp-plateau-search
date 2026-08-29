#!/usr/bin/env python3
"""CERTIFIED branch-and-bound on the edge count |L1| = sum_e x_e.

|L1| is an integer, so
    min over depth-3 circuits of (|L1|+|L2|)  >=  min over E >= 0 of LP_E,
where LP_E is the LP relaxation with sum_e x_e == E.  Branches with E >= B
need no work: the objective already contains sum_e x_e = E >= B.  The
remaining finitely many branches each get an EXACT certificate.

Certificate arithmetic (rigorous, no floating point in the claim).  All model
variables are 0/1 in any integer solution, so 0 <= p_j <= 1.  For any u >= 0,
    c.p  >=  u.A.p - sum_j max(0, (A^T u)_j - c_j) . p_j
         >=  u.b   - sum_j max(0, (A^T u)_j - c_j)
Thus a *rounded* dual u (whose Aᵀu may overshoot c by a hair) still certifies
the bound  u.b - total_overshoot.  We take u from the primal LP's marginals
(free), clip to u >= 0, scale to denominator 10^12, and evaluate both terms
in exact integer arithmetic.

Infeasible branches are certified separately by farkas.py.

Usage: branch_certify.py <Emin> <Emax>
"""
import sys, json, time, math
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3')
from build_lp import build

HERE = '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3'
DEN = 10 ** 12


def exact_bound(rows, cost, u_num, den):
    """returns (numerator of certified bound, overshoot numerator) or None."""
    n = len(cost)
    acc = [0] * n
    for i, (terms, rhs, tag) in enumerate(rows):
        ui = u_num[i]
        if ui == 0:
            continue
        if ui < 0:
            return None
        for j, cf in terms:
            acc[j] += cf * ui
    over = 0
    for j in range(n):
        d = acc[j] - cost[j] * den
        if d > 0:
            over += d
    val = sum(u_num[i] * rows[i][1] for i in range(len(rows)))
    return val - over, over


def main():
    E0, E1 = int(sys.argv[1]), int(sys.argv[2])
    rows0, cost, meta = build(True, 1)
    n = meta['nvar']
    xs = [meta['xi'][e] for e in meta['E']]
    out, certs, best = [], {}, None
    for E in range(E0, E1 + 1):
        rows = rows0 + [([(j, 1) for j in xs], E, 'edgeE'),
                        ([(j, -1) for j in xs], -E, 'edgeE_ub')]
        r, ci, va, b = [], [], [], []
        for i, (terms, rhs, tag) in enumerate(rows):
            for j, cf in terms:
                r.append(i); ci.append(j); va.append(cf)
            b.append(rhs)
        A = coo_matrix((va, (r, ci)), shape=(len(rows), n)).tocsr()
        c = np.array(cost, dtype=float)
        bb = np.array(b, dtype=float)
        t0 = time.monotonic()
        res = linprog(c, A_ub=(-A).tocsc(), b_ub=-bb, bounds=[(0, 1)] * n,
                      method='highs')
        rec = {'E': E, 'wall': time.monotonic() - t0}
        if res.status == 2:
            rec['infeasible'] = True
        elif res.status != 0:
            rec['solver_status'] = res.status
        else:
            rec['lp'] = float(res.fun)
            u = np.maximum(-np.asarray(res.ineqlin.marginals), 0.0)
            un = [int(round(v * DEN)) for v in u]
            got = exact_bound(rows, cost, un, DEN)
            if got is None:
                rec['certified'] = None
            else:
                val, over = got
                rec['certified_numerator'] = val
                rec['denominator'] = DEN
                rec['overshoot_numerator'] = over
                rec['certified_bound'] = math.ceil(val / DEN - 1e-15)
                certs[str(E)] = [[i, v] for i, v in enumerate(un) if v]
                best = rec['certified_bound'] if best is None else min(best, rec['certified_bound'])
        out.append(rec)
        print(json.dumps(rec), flush=True)
        json.dump({'branches': out, 'min_certified_bound_so_far': best,
                   'n_base_rows': len(rows0)},
                  open(HERE + '/branch_summary.json', 'w'), indent=1)
        json.dump(certs, open(HERE + '/branch_certificates.json', 'w'))
    print('MIN certified branch bound over E in [%d,%d] = %s => N_depth3 >= %s'
          % (E0, E1, best, (32 + best) if best else None), flush=True)


if __name__ == '__main__':
    main()
