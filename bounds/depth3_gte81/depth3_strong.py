#!/usr/bin/env python3
"""STRENGTHENED complete depth-3 model for min-XOR AES MixColumns.

Same complete model as this project's earlier, unpublished exact depth-3
model (N_depth3 = 32 + min |L1|+|L2| over the exhaustive candidate space), plus the
valid inequalities of cuts.py, each of which is a theorem about depth-3
circuits and each of which is checked against the verified 97-gate depth-3
circuit by control_cuts.py / control_lp.py.

Reports CP-SAT's proved dual bound.  N_depth3 >= 32 + dual.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys, os, json, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
from mcmatrix import TARGETS
from model3 import candidates, buildings, pc, BITS
import cuts as CUT
from ortools.sat.python import cp_model


def main():
    tlim = float(sys.argv[1]) if len(sys.argv) > 1 else 3600.0
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    tag = sys.argv[3] if len(sys.argv) > 3 else 'strong'
    decomp, L2, E = candidates()
    Eset = set(E)
    mdl = cp_model.CpModel()
    x = {e: mdl.NewBoolVar('x%d' % e) for e in E}
    y = {m: mdl.NewBoolVar('y%d' % m) for m in L2}
    # --- exact model ---------------------------------------------------
    for m in L2:
        bs = buildings(m)
        ws = []
        for k, (e1, e2) in enumerate(bs):
            w = mdl.NewBoolVar('w%d_%d' % (m, k))
            for e in (e1, e2):
                if pc(e) == 2:
                    mdl.AddImplication(w, x[e])
            ws.append(w)
        mdl.AddBoolOr(ws + [y[m].Not()])
    zv = {}
    for t in TARGETS:
        zs = []
        for k, (a, b) in enumerate(decomp[t]):
            z = mdl.NewBoolVar('z%d_%d' % (t, k))
            for v in (a, b):
                if pc(v) == 2:
                    mdl.AddImplication(z, x[v])
                elif pc(v) >= 3:
                    mdl.AddImplication(z, y[v])
            zs.append(z); zv[(t, k)] = z
        mdl.AddBoolOr(zs)
    # --- valid inequalities (cuts.py) ----------------------------------
    ncut = 0
    def lin(xs, ys, b):
        nonlocal ncut
        mdl.Add(sum(x[e] for e in xs) + sum(c * y[m] for m, c in ys) >= b)
        ncut += 1
    for xs, ys, b in CUT.cuts_building(L2):
        lin(xs, ys, b)
    for xs, ys, b in CUT.cuts_target_l2(decomp, TARGETS):
        lin(xs, ys, b)
    for xs, ys, b in CUT.cuts_w7_matching(TARGETS, Eset):
        lin(xs, ys, b)
    for xs, ys, b in CUT.cuts_w5(TARGETS, Eset):
        lin(xs, ys, b)
    xs, ys, b = CUT.cut_aggregate_degree(decomp, TARGETS)
    lin(xs, ys, b)
    for xs, ys, b in CUT.cuts_aggregate_by_weight(decomp, TARGETS):
        lin(xs, ys, b)
    # C8 conditional weight-5 edge floor
    for t in TARGETS:
        if pc(t) != 5:
            continue
        ov = [k for k, (a, b_) in enumerate(decomp[t]) if pc(a) + pc(b_) > pc(t)]
        mdl.Add(sum(x[e] for e in CUT.sub_edges(t) if e in Eset)
                + sum(zv[(t, k)] for k in ov) >= 2)
        ncut += 1
    tot = sum(x.values()) + sum(y.values())
    mdl.Add(tot <= 65)          # from the verified 97-gate depth-3 circuit
    mdl.Minimize(tot)
    print('cuts added: %d' % ncut, flush=True)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tlim
    s.parameters.num_search_workers = workers
    s.parameters.linearization_level = 2
    s.parameters.log_search_progress = True
    t0 = time.monotonic()
    st = s.Solve(mdl)
    res = {'model': 'depth3_strong', 'tag': tag, 'status': s.StatusName(st),
           'wall_monotonic': time.monotonic() - t0, 'n_cuts': ncut,
           'dual_bound_nontarget': s.BestObjectiveBound(),
           'N_depth3_lower_bound': 32 + s.BestObjectiveBound(),
           'primal_nontarget': (s.ObjectiveValue()
                                if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None)}
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        res['circuit_L1'] = [e for e in E if s.Value(x[e])]
        res['circuit_L2'] = [m for m in L2 if s.Value(y[m])]
    print(json.dumps({k: v for k, v in res.items() if not k.startswith('circuit')},
                     indent=1), flush=True)
    json.dump(res, open(os.path.join(HERE, 'depth3_strong_%s.json' % tag), 'w'), indent=1)


if __name__ == '__main__':
    main()
