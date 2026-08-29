#!/usr/bin/env python3
"""EXACT floor on |L1| (the level-1 edge count) from the matching structure.

This is a *relaxation of the depth-3 model that keeps only the edges*, so its
optimum is an unconditional lower bound on |L1| for every depth-3 MixColumns
circuit -- and every branch E < that floor is closed with no LP at all.

The structure theorem (THEOREM.md §1.6/§1.7) forces, for every target t:

  wt(t) = 7 :  t = m1(wt 4) + m2(wt 3), disjoint, m1 = e1+e2 (disjoint edges
               inside m1), m2 = input + e3 (e3 inside m2).  So X contains
               THREE PAIRWISE DISJOINT EDGES inside t covering 6 of its 7 bits.

  wt(t) = 5 :  either (N) both parents inside t -- {1,4} or {2,3} -- which
               forces TWO DISJOINT EDGES inside t covering 4 of its 5 bits;
               or (O) parents {4,3} overlapping in one bit z outside t, where
               the wt-4 parent a (which contains z) is a disjoint union of two
               edges and the wt-3 parent b contains an edge.  In case (O) the
               two edges building a are disjoint and lie inside t+{z}.

Both cases are enumerated exactly; a target is satisfied if ANY of its
admissible edge-configurations is fully selected.  Minimising |X| over that
disjunction is a small set-cover-with-patterns ILP (496 edge variables, a few
thousand pattern variables) that CP-SAT settles outright.

Controls: the verified 97@3 circuit's own 27 edges must be a FEASIBLE point
(else the encoding is over-constrained and any floor it reports is vacuous),
and the reported floor must not exceed 27.

Usage: edge_floor.py [seconds] [mode]
   mode = w7      only the 12 weight-7 targets   (weakest, fastest)
          all     all 32 targets                 (the real floor)
"""
import sys, json, time, itertools
HERE = '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3'
sys.path.insert(0, HERE)
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/pipeline')
from mixcolumns_core import TARGETS
from model3 import candidates, pc, BITS
from ortools.sat.python import cp_model


def matchings(bits):
    """all perfect matchings (as tuples of 2-bit masks) of an even bit list"""
    if not bits:
        yield ()
        return
    a = bits[0]
    for i in range(1, len(bits)):
        b = bits[i]
        rest = bits[1:i] + bits[i + 1:]
        for m in matchings(rest):
            yield ((1 << a) | (1 << b),) + m


def patterns(t, Eset):
    """admissible edge-configurations for target t, as frozensets of edges"""
    out = set()
    w = pc(t)
    B = BITS(t)
    if w == 7:
        for skip in B:                       # the bit left uncovered
            rest = [b for b in B if b != skip]
            for m in matchings(rest):        # 3 disjoint edges, 6 bits
                if all(e in Eset for e in m):
                    out.add(frozenset(m))
    elif w == 5:
        for skip in B:                       # case (N): 2 disjoint edges
            rest = [b for b in B if b != skip]
            for m in matchings(rest):
                if all(e in Eset for e in m):
                    out.add(frozenset(m))
        for z in range(32):                  # case (O): overlap bit z outside t
            if (t >> z) & 1:
                continue
            for a4 in itertools.combinations(B, 3):
                a = (1 << z) | sum(1 << i for i in a4)   # wt-4 parent, holds z
                for m in matchings(BITS(a)):
                    if all(e in Eset for e in m):
                        out.add(frozenset(m))
    return sorted(out, key=lambda s: (len(s), sorted(s)))


def main():
    tlim = float(sys.argv[1]) if len(sys.argv) > 1 else 300.0
    mode = sys.argv[2] if len(sys.argv) > 2 else 'all'
    t0 = time.monotonic()
    decomp, L2, E = candidates()
    Eset = set(E)
    TS = [t for t in TARGETS if pc(t) == 7] if mode == 'w7' else list(TARGETS)

    # the STRENGTHENED pattern set (case (O) also forces the edge inside the
    # wt-3 parent); strictly smaller feasible set than the local `patterns`,
    # so a UNSAT verdict remains a sound theorem.
    from edge_floor_sat import patterns as patterns_strong

    mdl = cp_model.CpModel()
    x = {e: mdl.NewBoolVar('x%d' % e) for e in E}
    npat = 0
    pats = {}
    for t in TS:
        P = patterns_strong(t, Eset)
        pats[t] = P
        if not P:
            print('target %d has NO admissible pattern -- encoding bug' % t)
            return 2
        sel = []
        for i, p in enumerate(P):
            v = mdl.NewBoolVar('p%d_%d' % (t, i)); npat += 1
            for e in p:
                mdl.AddImplication(v, x[e])
            sel.append(v)
        mdl.AddBoolOr(sel)
        # redundant but strongly propagating: every admissible pattern for a
        # wt-7 target has 3 edges inside t and every one for a wt-5 target has
        # >= 2 edges inside t+{z}; the plain edge-count form is what CP-SAT
        # actually propagates on.
        ins = [x[e] for e in E if e & t == e]
        if ins:
            mdl.Add(sum(ins) >= (3 if pc(t) == 7 else 1))
    # DECISION form: "is |X| <= cap achievable?"  UNSAT is the useful verdict
    # (floor >= cap+1) and CP-SAT settles it far more readily than it proves an
    # optimisation bound, where the pattern LP is fractional and useless.
    cap = int(sys.argv[3]) if len(sys.argv) > 3 else None
    if cap is not None:
        mdl.Add(sum(x.values()) <= cap)
    else:
        mdl.Minimize(sum(x.values()))
    print('edge-floor model: %d edge vars, %d pattern vars, %d targets (%s), '
          'built in %.1fs' % (len(E), npat, len(TS), mode, time.monotonic() - t0),
          flush=True)

    # ---------------- CONTROL: the verified 97@3 circuit ------------------
    import json as J
    from control_primal import masks_and_depths, CIRC
    g = J.load(open(CIRC))['gates']
    sig, dep = masks_and_depths(g)
    X97 = {sig[32 + k] for k in range(len(g)) if dep[32 + k] == 1}
    miss = [t for t in TS if not any(set(p) <= X97 for p in pats[t])]
    print('CONTROL 97@3: |L1|=%d ; targets with no pattern inside it: %d'
          % (len(X97), len(miss)), flush=True)
    if miss:
        print('CONTROL FAILED: the real circuit is not a feasible point '
              '-> the floor would be VACUOUS'); return 2

    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tlim
    s.parameters.num_search_workers = 1
    st = s.Solve(mdl)
    name = s.StatusName(st)
    out = {'mode': mode, 'cap': cap, 'status': name,
           'control_L1_97': len(X97), 'wall_monotonic': time.monotonic() - t0,
           'n_targets': len(TS), 'n_pattern_vars': npat}
    if cap is None:
        lb = int(s.BestObjectiveBound())
        out['edge_floor_lower_bound'] = lb
        out['best_solution'] = int(s.ObjectiveValue()) if name in ('OPTIMAL', 'FEASIBLE') else None
        tail = ('=> every depth-3 MixColumns circuit has |L1| >= %d '
                '(branches E < %d are closed)' % (lb, lb))
    else:
        if name == 'INFEASIBLE':
            out['edge_floor_lower_bound'] = cap + 1
            tail = ('=> UNSAT at cap %d: every depth-3 MixColumns circuit has '
                    '|L1| >= %d (branches E <= %d are CLOSED)' % (cap, cap + 1, cap))
        elif name == 'OPTIMAL' or name == 'FEASIBLE':
            out['witness_L1'] = sorted(e for e in E if s.Value(x[e]))
            tail = ('=> SAT at cap %d: the edge relaxation alone cannot close '
                    'E <= %d' % (cap, cap))
        else:
            tail = '=> %s at cap %d (undecided)' % (name, cap)
    print(json.dumps(out, indent=1), flush=True)
    json.dump(out, open(HERE + '/edge_floor_%s_cap%s.json' % (mode, cap), 'w'), indent=1)
    print(tail)
    return 0


if __name__ == '__main__':
    sys.exit(main())
