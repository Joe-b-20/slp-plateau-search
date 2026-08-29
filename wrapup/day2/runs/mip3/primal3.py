#!/usr/bin/env python3
"""PRIMAL side of the depth-3 question: how small can a depth-3 MixColumns
circuit actually be?  The repo's best is 97 (|L1|+|L2| = 65).

Any feasible point of the complete model at |L1|+|L2| = K materialises into a
real depth-3 circuit of 32+K gates, which is written out and must be checked
with verify_circuit.py.  This both (a) improves the depth-3 record and
(b) tells the rung ladder where its ceiling is.

Usage: primal3.py <K> <seconds> [workers]
"""
import sys, os, json, time
HERE = '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3'
sys.path.insert(0, HERE)
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/pipeline')
from mixcolumns_core import TARGETS
from model3 import pc, BITS
from rungs import build_model, hint_control
from ortools.sat.python import cp_model


def materialise(L1, L2, path):
    """Turn a model solution into a gate list and write it in repo format."""
    sig = {1 << i: i for i in range(32)}
    gates = []

    def emit(a, b):
        gates.append([sig[a], sig[b]])
        sig[a ^ b] = 32 + len(gates) - 1
        return a ^ b
    for e in L1:
        bs = BITS(e); emit(1 << bs[0], 1 << bs[1])
    for m in L2:
        bs = BITS(m)
        done = False
        if pc(m) == 4:
            for i, j, k in [(1, 2, 3), (2, 1, 3), (3, 1, 2)]:
                e1 = (1 << bs[0]) | (1 << bs[i]); e2 = (1 << bs[j]) | (1 << bs[k])
                if e1 in sig and e2 in sig:
                    emit(e1, e2); done = True; break
        else:
            for i in range(3):
                e = m ^ (1 << bs[i])
                if e in sig:
                    emit(1 << bs[i], e); done = True; break
        if not done:
            raise SystemExit('level-2 mask %d not buildable' % m)
    for t in TARGETS:
        found = False
        for a in list(sig):
            b = t ^ a
            if b in sig and a != b:
                emit(a, b); found = True; break
        if not found:
            raise SystemExit('target %d not buildable' % t)
    json.dump({'gates': gates}, open(path, 'w'))
    return len(gates)


def main():
    K = int(sys.argv[1]); tlim = float(sys.argv[2])
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    mdl, x, y, E, L2 = build_model(K, None)
    hint_control(mdl, x, y)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tlim
    s.parameters.num_search_workers = workers
    s.parameters.linearization_level = 2
    t0 = time.monotonic()
    st = s.Solve(mdl)
    name = s.StatusName(st)
    print('K=%d status %s  %.1f s' % (K, name, time.monotonic() - t0), flush=True)
    if name in ('OPTIMAL', 'FEASIBLE'):
        l1 = [e for e in E if s.Value(x[e])]
        l2 = [m for m in L2 if s.Value(y[m])]
        path = os.path.join(HERE, 'depth3_%dgates.json' % (32 + len(l1) + len(l2)))
        n = materialise(l1, l2, path)
        print('wrote %s with %d gates (|L1|=%d |L2|=%d)' % (path, n, len(l1), len(l2)))
    with open(os.path.join(HERE, 'rung_ledger.jsonl'), 'a') as f:
        f.write(json.dumps({'primal_K': K, 'status': name,
                            'wall_monotonic': time.monotonic() - t0}) + '\n')


if __name__ == '__main__':
    main()
