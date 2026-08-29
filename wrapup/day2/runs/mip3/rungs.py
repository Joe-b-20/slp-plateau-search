#!/usr/bin/env python3
"""RUNG LADDER on the complete depth-3 model.

Rung K asks: does the complete depth-3 candidate space admit |L1|+|L2| <= K?
  UNSAT  =>  N_depth3 >= 32 + K + 1.
  SAT    =>  the ladder stops (and the witness is a depth-3 circuit of
             32+K gates, which we materialise and hand to verify_circuit.py).

Positive control (MANDATORY, run as rung 65): the verified 97-gate depth-3
circuit gives |L1|+|L2| = 65, so rung 65 MUST come back SAT on the same
encoding.  A rung ladder whose control is UNSAT is vacuous.

Usage: rungs.py <Kstart> <Kend> <seconds-per-rung> [workers]
"""
import sys, os, json, time, itertools
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/pipeline')
HERE = '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3'
sys.path.insert(0, HERE)
from mixcolumns_core import TARGETS
from model3 import candidates, buildings, pc, BITS
import cuts as CUT
from ortools.sat.python import cp_model


def build_model(K, lb=None):
    decomp, L2, E = candidates()
    Eset, L2set = set(E), set(L2)
    mdl = cp_model.CpModel()
    x = {e: mdl.NewBoolVar('x%d' % e) for e in E}
    y = {m: mdl.NewBoolVar('y%d' % m) for m in L2}
    for m in L2:
        ws = []
        for k, (e1, e2) in enumerate(buildings(m)):
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

    def lin(xs, ys, b):
        mdl.Add(sum(x[e] for e in xs) + sum(c * y[m] for m, c in ys) >= b)
    for f in (CUT.cuts_building(L2), CUT.cuts_target_l2(decomp, TARGETS),
              CUT.cuts_w7_matching(TARGETS, Eset), CUT.cuts_w5(TARGETS, Eset),
              [CUT.cut_aggregate_degree(decomp, TARGETS)],
              CUT.cuts_aggregate_by_weight(decomp, TARGETS),
              CUT.cuts_w7_bits(TARGETS, L2set),
              CUT.cuts_w7_global(TARGETS, L2set, Eset)):
        for xs, ys, b in f:
            lin(xs, ys, b)
    for t in TARGETS:
        if pc(t) != 5:
            continue
        ov = [k for k, (a, b_) in enumerate(decomp[t]) if pc(a) + pc(b_) > pc(t)]
        mdl.Add(sum(x[e] for e in CUT.sub_edges(t) if e in Eset)
                + sum(zv[(t, k)] for k in ov) >= 2)
    tot = sum(x.values()) + sum(y.values())
    mdl.Add(tot <= K)
    if lb is not None:
        mdl.Add(tot >= lb)          # certified by certify.py (cert_depth3.json)
    return mdl, x, y, E, L2


def hint_control(mdl, x, y):
    """Hint the verified 97-gate depth-3 circuit (rung-65 positive control)."""
    from build_lp import build, control_point
    import json as _j
    from control_primal import masks_and_depths, CIRC
    g = _j.load(open(CIRC))['gates']
    sig, dep = masks_and_depths(g)
    X = {sig[32 + k] for k in range(len(g)) if dep[32 + k] == 1}
    Y = {sig[32 + k] for k in range(len(g)) if dep[32 + k] == 2}
    for e, v in x.items():
        mdl.AddHint(v, 1 if e in X else 0)
    for m, v in y.items():
        mdl.AddHint(v, 1 if m in Y else 0)


def run(K, tlim, workers, lb):
    mdl, x, y, E, L2 = build_model(K, lb)
    if K >= 65:
        hint_control(mdl, x, y)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tlim
    s.parameters.num_search_workers = workers
    s.parameters.linearization_level = 2
    s.parameters.log_search_progress = False
    t0 = time.monotonic()
    st = s.Solve(mdl)
    wall = time.monotonic() - t0
    rec = {'rung_K': K, 'status': s.StatusName(st), 'wall_monotonic': wall,
           'workers': workers, 'time_limit': tlim,
           'implies_N_depth3_ge': (32 + K + 1) if s.StatusName(st) == 'INFEASIBLE' else None,
           'stamp': time.strftime('%Y-%m-%dT%H:%M:%S')}
    if s.StatusName(st) in ('OPTIMAL', 'FEASIBLE'):
        rec['L1'] = [e for e in E if s.Value(x[e])]
        rec['L2'] = [m for m in L2 if s.Value(y[m])]
        rec['n_L1'], rec['n_L2'] = len(rec['L1']), len(rec['L2'])
    with open(os.path.join(HERE, 'rung_ledger.jsonl'), 'a') as f:
        f.write(json.dumps(rec) + '\n')
    print(json.dumps({k: v for k, v in rec.items() if k not in ('L1', 'L2')}), flush=True)
    return rec


def main():
    k0, k1 = int(sys.argv[1]), int(sys.argv[2])
    tlim = float(sys.argv[3])
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    lb = int(sys.argv[5]) if len(sys.argv) > 5 else None
    for K in range(k0, k1 + 1):
        r = run(K, tlim, workers, lb)
        if r['status'] != 'INFEASIBLE':
            print('ladder stops at K=%d (%s)' % (K, r['status']), flush=True)
            break


if __name__ == '__main__':
    main()
