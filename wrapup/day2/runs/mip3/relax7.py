#!/usr/bin/env python3
"""RELAXATION R7: the weight-7 sub-instance of the complete depth-3 model.

Every depth-3 MixColumns circuit contains, for each of the 12 weight-7
targets t, a decomposition t = m4 ^ m3 with wt(m4)=4, wt(m3)=3, m4,m3
DISJOINT and both contained in t (forced: parents have weight <=4 and
4+3 = 7 = wt(t), so the split is exact and non-overlapping).  Both parents
are level-2 gates.  m4 is a disjoint union of two selected edges; m3 is an
input plus one selected edge contained in m3.

Dropping every other requirement (the 20 weight-5 targets, and any level-2
mask not contained in a weight-7 target) can only lower the cost, so

    opt(R7) <= |L1| + |L2|,   i.e.  N_depth3 >= 32 + opt(R7).

The model is exact and complete for that sub-requirement.
"""
import sys, json, itertools, time
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/pipeline')
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3')
from mixcolumns_core import TARGETS
from model3 import pc, BITS
from ortools.sat.python import cp_model


def build():
    T7 = [t for t in TARGETS if pc(t) == 7]
    Y, X = set(), set()
    pairs = {}
    for t in T7:
        ps = []
        for c in itertools.combinations(BITS(t), 4):
            m4 = sum(1 << i for i in c)
            m3 = t ^ m4
            ps.append((m4, m3))
            Y.add(m4); Y.add(m3)
        pairs[t] = ps
    for m in Y:
        for c in itertools.combinations(BITS(m), 2):
            X.add(sum(1 << i for i in c))
    return T7, sorted(Y), sorted(X), pairs


def main():
    tlim = float(sys.argv[1]) if len(sys.argv) > 1 else 600.0
    T7, Y, X, pairs = build()
    print('R7: %d wt7 targets, %d level-2 masks, %d edges' % (len(T7), len(Y), len(X)), flush=True)
    mdl = cp_model.CpModel()
    y = {m: mdl.NewBoolVar('y%d' % m) for m in Y}
    x = {e: mdl.NewBoolVar('x%d' % e) for e in X}
    for t in T7:
        zs = []
        for k, (m4, m3) in enumerate(pairs[t]):
            z = mdl.NewBoolVar('z%d_%d' % (t, k))
            mdl.AddImplication(z, y[m4]); mdl.AddImplication(z, y[m3])
            zs.append(z)
        mdl.AddBoolOr(zs)
    # building constraints (exact, not cuts)
    for m in Y:
        b = BITS(m)
        if len(b) == 4:
            ws = []
            for i, j, k in [(1, 2, 3), (2, 1, 3), (3, 1, 2)]:
                e1 = (1 << b[0]) | (1 << b[i]); e2 = (1 << b[j]) | (1 << b[k])
                w = mdl.NewBoolVar('w%d_%d' % (m, i))
                mdl.AddImplication(w, x[e1]); mdl.AddImplication(w, x[e2])
                ws.append(w)
            mdl.AddBoolOr(ws + [y[m].Not()])
            # valid cuts: every bit of m must be covered by a selected sub-edge
            for bb in b:
                mdl.Add(sum(x[e] for e in x if (e >> bb) & 1 and (e | m) == m) >= 1).OnlyEnforceIf(y[m])
        else:
            ws = []
            for i in range(3):
                e = m ^ (1 << b[i])
                w = mdl.NewBoolVar('v%d_%d' % (m, i))
                mdl.AddImplication(w, x[e]); ws.append(w)
            mdl.AddBoolOr(ws + [y[m].Not()])
    tot = sum(x.values()) + sum(y.values())
    mdl.Minimize(tot)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tlim
    s.parameters.num_search_workers = 1
    s.parameters.linearization_level = 2
    s.parameters.log_search_progress = True
    t0 = time.monotonic()
    st = s.Solve(mdl)
    res = {'model': 'R7', 'status': s.StatusName(st), 'wall': time.monotonic() - t0,
           'n_y': len(Y), 'n_x': len(X),
           'obj': s.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None,
           'dual': s.BestObjectiveBound(),
           'implied_N_depth3_lower_bound': 32 + s.BestObjectiveBound()}
    print(json.dumps(res, indent=1), flush=True)
    json.dump(res, open('/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3/relax7_result.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
