#!/usr/bin/env python3
"""HiGHS branch-and-cut on the strengthened complete depth-3 model.

scipy.optimize.milp exposes HiGHS' MIP solver, which reports a proved DUAL
BOUND (res.mip_dual_bound) even on timeout.  Since every row of build_lp is a
theorem about depth-3 circuits,
        N_depth3 >= 32 + ceil(mip_dual_bound).
HiGHS' own cut generators (Gomory, clique, knapsack-cover) sit on top of a
root LP that is already at 47.598, which CP-SAT never reproduces.

Usage: mip3.py <seconds> [level]
"""
import sys, json, time, math
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3')
from build_lp import build

HERE = '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3'


def main():
    tlim = float(sys.argv[1]) if len(sys.argv) > 1 else 3600.0
    level = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    rows, cost, meta = build(True, level)
    n = meta['nvar']
    r, ci, va, b = [], [], [], []
    for i, (terms, rhs, tag) in enumerate(rows):
        for j, cf in terms:
            r.append(i); ci.append(j); va.append(cf)
        b.append(rhs)
    # valid: the verified 97-gate depth-3 circuit realises |L1|+|L2| = 65,
    # so capping the objective there cannot cut off the optimum.
    # STEWARD 2026-08-29: the banked N_depth3 >= 82 trajectory
    # (logs/mip3_L1_uncapped.log, dual bound 49.47825234 at 538.7 s) came from
    # the variant WITHOUT this cap; the capped variant reached only 48.4498 in
    # 599.5 s.  Both are sound -- the cap is valid because the verified 97-gate
    # depth-3 circuit realises |L1|+|L2| = 65 -- but we reproduce the better
    # trajectory.  argv[3] = 'capped' restores the original behaviour.
    capped = (len(sys.argv) > 3 and sys.argv[3] == 'capped')
    nrows = len(rows)
    if capped:
        base = meta['base']
        for j in range(base):
            r.append(len(rows)); ci.append(j); va.append(-1)
        b.append(-65)
        nrows = len(rows) + 1
    A = coo_matrix((va, (r, ci)), shape=(nrows, n)).tocsc()
    print('MIP: %d rows x %d cols, nnz %d, level %d (%s)'
          % (A.shape[0], n, A.nnz, level,
             'objective capped at 65' if capped else 'uncapped'), flush=True)
    con = LinearConstraint(A, np.array(b, dtype=float), np.inf)
    t0 = time.monotonic()
    res = milp(c=np.array(cost, dtype=float), constraints=con,
               integrality=np.ones(n), bounds=Bounds(0, 1),
               options={'time_limit': tlim, 'disp': True, 'mip_rel_gap': 0.0})
    wall = time.monotonic() - t0
    db = res.mip_dual_bound
    out = {'model': 'depth3_strong_highs_mip', 'level': level,
           'status': res.status, 'message': res.message,
           'wall_monotonic': wall,
           'primal': res.fun, 'mip_dual_bound': db,
           'mip_gap': res.mip_gap,
           'N_depth3_lower_bound': (32 + math.ceil(db - 1e-6)) if db is not None else None}
    print(json.dumps({k: v for k, v in out.items()}, indent=1), flush=True)
    json.dump(out, open(HERE + '/mip3_result_L%d.json' % level, 'w'), indent=1)
    if res.x is not None:
        p = res.x
        E, L2 = meta['E'], meta['L2']
        json.dump({'L1': [e for e in E if p[meta['xi'][e]] > 0.5],
                   'L2': [m for m in L2 if p[meta['yi'][m]] > 0.5]},
                  open(HERE + '/mip3_primal_L%d.json' % level, 'w'))


if __name__ == '__main__':
    main()
