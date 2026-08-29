#!/usr/bin/env python3
"""Exact LP relaxation of the strengthened complete depth-3 model (HiGHS).

Gives the CEILING of every LP-based dual bound for this formulation:
   N_depth3 >= 32 + ceil(LP)      (valid, since every constraint used is a
                                   theorem about depth-3 circuits)
Usage:  python3 lp3.py [--nocuts]
"""
import sys, json, time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/pipeline')
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3')
from mixcolumns_core import TARGETS
from model3 import candidates, pc
import cuts as CUT

USE_CUTS = '--nocuts' not in sys.argv


def main():
    t0 = time.monotonic()
    decomp, L2, E = candidates()
    Eset = set(E)
    xi = {e: i for i, e in enumerate(E)}
    yi = {m: len(E) + i for i, m in enumerate(L2)}
    nz = 0
    zidx = {}
    base = len(E) + len(L2)
    for t in TARGETS:
        for k in range(len(decomp[t])):
            zidx[(t, k)] = base + nz
            nz += 1
    widx = {}
    nw = 0
    if USE_CUTS:
        from model3 import buildings
        for m in L2:
            if pc(m) == 4:
                for j in range(3):
                    widx[(m, j)] = base + nz + nw
                    nw += 1
    N = base + nz + nw
    rows, cols, vals, rhs = [], [], [], []
    r = 0

    def add(terms, b):
        """sum terms >= b, terms = list of (var_index, coef)"""
        nonlocal r
        for v, c in terms:
            rows.append(r); cols.append(v); vals.append(float(c))
        rhs.append(float(b)); r += 1

    # target cover:  sum_k z_{t,k} >= 1
    for t in TARGETS:
        add([(zidx[(t, k)], 1) for k in range(len(decomp[t]))], 1)
    # z_{t,k} <= parent   ->   parent - z >= 0
    for t in TARGETS:
        for k, (a, b) in enumerate(decomp[t]):
            for v in (a, b):
                if pc(v) == 2:
                    add([(xi[v], 1), (zidx[(t, k)], -1)], 0)
                elif pc(v) >= 3:
                    add([(yi[v], 1), (zidx[(t, k)], -1)], 0)
    ncore = r
    if USE_CUTS:
        for xs, ys, b in CUT.cuts_building(L2):
            add([(xi[e], 1) for e in xs] + [(yi[m], c) for m, c in ys], b)
        for xs, ys, b in CUT.cuts_target_l2(decomp, TARGETS):
            add([(xi[e], 1) for e in xs] + [(yi[m], c) for m, c in ys], b)
        for xs, ys, b in CUT.cuts_w7_matching(TARGETS, Eset):
            add([(xi[e], 1) for e in xs], b)
        for xs, ys, b in CUT.cuts_w5(TARGETS, Eset):
            add([(xi[e], 1) for e in xs], b)
        xs, ys, b = CUT.cut_aggregate_degree(decomp, TARGETS)
        add([(yi[m], c) for m, c in ys], b)
        for xs, ys, b in CUT.cuts_aggregate_by_weight(decomp, TARGETS):
            add([(yi[m], c) for m, c in ys], b)
        # C8 -- conditional weight-5 edge floor.
        # A weight-5 target decomposed as {1,4} or {2,3} has BOTH parents
        # inside t and forces two disjoint edges inside t; only the {4,3}
        # decomposition overlapping in a bit z outside t escapes with one.
        #   sum_{e subset t} x_e + sum_{k in OVERLAP(t)} z_{t,k} >= 2
        for t in TARGETS:
            if pc(t) != 5:
                continue
            ov = [k for k, (a, b) in enumerate(decomp[t])
                  if pc(a) + pc(b) > pc(t)]
            add([(xi[e], 1) for e in CUT.sub_edges(t) if e in Eset]
                + [(zidx[(t, k)], 1) for k in ov], 2)
        # EXACT extended formulation of the weight-4 building disjunction
        # (m = e1 ^ e2 for one of the 3 perfect matchings of m's 4 bits):
        #   y_m <= sum_j w_{m,j},   w_{m,j} <= x_{e},  e in matching j.
        from model3 import buildings
        for m in L2:
            if pc(m) != 4:
                continue
            add([(widx[(m, j)], 1) for j in range(3)] + [(yi[m], -1)], 0)
            for j, (e1, e2) in enumerate(buildings(m)):
                for e in (e1, e2):
                    add([(xi[e], 1), (widx[(m, j)], -1)], 0)
    print('vars %d  constraints %d (core %d, cuts %d)' % (N, r, ncore, r - ncore), flush=True)

    A = coo_matrix((vals, (rows, cols)), shape=(r, N))
    c = np.zeros(N)
    c[:base] = 1.0                      # minimise |L1| + |L2|
    res = linprog(c, A_ub=(-A).tocsc(), b_ub=-np.array(rhs),
                  bounds=[(0, 1)] * N, method='highs')
    out = {'status': res.status, 'message': res.message,
           'lp_objective': res.fun, 'lp_lower_bound_total': None,
           'cuts': USE_CUTS, 'wall': time.monotonic() - t0,
           'n_vars': N, 'n_cons': r}
    if res.status == 0:
        import math
        out['lp_lower_bound_total'] = 32 + math.ceil(res.fun - 1e-7)
    print(json.dumps(out, indent=1), flush=True)
    tag = 'cuts' if USE_CUTS else 'nocuts'
    json.dump(out, open('/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3/lp3_%s.json' % tag, 'w'), indent=1)


if __name__ == '__main__':
    main()
