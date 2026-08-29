#!/usr/bin/env python3
"""EDGE FLOOR by SAT, with a DRAT proof: the highest-leverage lower-bound lever.

WHY THIS AND NOT THE FULL MODEL.  The certified per-branch profile
(branch_summary_E18_48.json) already gives an exact rational LP_E for every
edge count E, and it rises steadily.  So a floor F on |L1| alone composes with
it for free:

    |L1| >= F   =>   |L1|+|L2| >= min over E >= F of LP_E   =>   N_depth3 >= 32 + that

    F=21 -> 81      F=23 -> 82      F=25 -> 84      F=26 -> 85
    F=22 -> 81      F=24 -> 83                      F=27 -> 85  (the ceiling:
                                                    the verified 97@3 circuit
                                                    uses 27 edges, so F <= 27)

and the subproblem carries **496 real variables instead of 29,180**, because it
drops every level-2 counting variable and keeps only the edge structure forced
by the structure theorem (THEOREM.md §1.6/§1.7):

  wt(t)=7 : three pairwise disjoint edges inside t, covering 6 of its 7 bits.
  wt(t)=5 : (N) two disjoint edges inside t covering 4 of its 5 bits; or
            (O) parents {4,3} overlapping in a bit z outside t -- the wt-4
                parent a = {z} + 3 bits of t splits into two disjoint edges,
                AND the wt-3 parent b = (t \\ a) + {z} contains an edge.

Dropping any of that only weakens the relaxation, so every UNSAT verdict here
is a sound theorem about all depth-3 MixColumns circuits.

EVIDENCE CLASS.  kissat emits a DRAT proof, so an UNSAT verdict is
independently checkable (drat-trim) rather than a solver's word -- the same
evidence class as certify.py, unlike a CP-SAT "INFEASIBLE".

CONTROLS (mandatory).
  * the 27 edges of the verified 97@3 circuit must satisfy every target clause
    (checked in Python, before any solving);
  * cap = 27 must come back SAT -- a ladder whose positive control is UNSAT is
    vacuous, and would mean the encoding is over-constrained.

Usage: edge_floor_sat.py <cap> <seconds> [--proof]
"""
import sys, os, json, time, itertools, subprocess

HERE = '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3'
KISSAT = '/home/joebachir20/xor_ui/slp-plateau-search/campaign_87/agents/frontier-sat/kissat/build/kissat'
sys.path.insert(0, HERE)
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/pipeline')
from mixcolumns_core import TARGETS
from model3 import candidates, pc, BITS
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool


def matchings(bits):
    if not bits:
        yield ()
        return
    a = bits[0]
    for i in range(1, len(bits)):
        b = bits[i]
        for m in matchings(bits[1:i] + bits[i + 1:]):
            yield ((1 << a) | (1 << b),) + m


def patterns(t, Eset):
    """admissible edge-sets for target t (frozensets of edge masks)"""
    out = set()
    B = BITS(t)
    if pc(t) == 7:
        for skip in B:
            rest = [b for b in B if b != skip]
            for m in matchings(rest):
                if all(e in Eset for e in m):
                    out.add(frozenset(m))
    else:                                       # weight 5
        for skip in B:                          # case (N)
            rest = [b for b in B if b != skip]
            for m in matchings(rest):
                if all(e in Eset for e in m):
                    out.add(frozenset(m))
        for z in range(32):                     # case (O)
            if (t >> z) & 1:
                continue
            for A3 in itertools.combinations(B, 3):
                a = (1 << z) | sum(1 << i for i in A3)          # wt-4 parent
                b = (1 << z) | (t ^ sum(1 << i for i in A3))    # wt-3 parent
                for m in matchings(BITS(a)):
                    if not all(e in Eset for e in m):
                        continue
                    # b = input + edge, that edge lies inside b
                    for bb in BITS(b):
                        e3 = b ^ (1 << bb)
                        if e3 in Eset:
                            out.add(frozenset(set(m) | {e3}))
    return sorted(out, key=lambda s: (len(s), sorted(s)))


def main():
    cap = int(sys.argv[1])
    tlim = float(sys.argv[2])
    proof = '--proof' in sys.argv
    t0 = time.monotonic()
    decomp, L2, E = candidates()
    Eset = set(E)

    pool = IDPool()
    xv = {e: pool.id(('x', e)) for e in E}
    cls = []
    pats = {}
    npat = 0
    for t in TARGETS:
        P = patterns(t, Eset)
        pats[t] = P
        if not P:
            print('target %d has no admissible pattern -- encoding bug' % t); return 2
        sel = []
        for i, p in enumerate(P):
            v = pool.id(('p', t, i)); npat += 1
            for e in p:
                cls.append([-v, xv[e]])          # pattern -> its edges
            sel.append(v)
        cls.append(sel)                          # at least one pattern per target

    # ---------------- CONTROL 1: the verified 97@3 edge set ----------------
    from control_primal import masks_and_depths, CIRC
    g = json.load(open(CIRC))['gates']
    sig, dep = masks_and_depths(g)
    X97 = {sig[32 + k] for k in range(len(g)) if dep[32 + k] == 1}
    miss = [t for t in TARGETS if not any(set(p) <= X97 for p in pats[t])]
    print('CONTROL 97@3: |L1|=%d, targets with no satisfied pattern: %d'
          % (len(X97), len(miss)), flush=True)
    if miss:
        print('CONTROL FAILED: the real circuit violates the encoding -> any '
              'floor from it would be VACUOUS'); return 2

    card = CardEnc.atmost(lits=[xv[e] for e in E], bound=cap, vpool=pool,
                          encoding=EncType.seqcounter)
    cls.extend([list(c) for c in card.clauses])
    nv = pool.top
    print('CNF: %d vars (%d edge, %d pattern), %d clauses, cap %d  [%.1fs]'
          % (nv, len(E), npat, len(cls), cap, time.monotonic() - t0), flush=True)

    cnf = os.path.join(HERE, 'work/edgefloor_cap%d.cnf' % cap)
    os.makedirs(os.path.dirname(cnf), exist_ok=True)
    with open(cnf, 'w') as f:
        f.write('p cnf %d %d\n' % (nv, len(cls)))
        f.write(''.join(' '.join(map(str, c)) + ' 0\n' for c in cls))

    cmd = [KISSAT, '--time=%d' % int(tlim), cnf]
    prf = os.path.join(HERE, 'work/edgefloor_cap%d.drat' % cap)
    if proof:
        cmd = [KISSAT, '--time=%d' % int(tlim), cnf, prf]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = r.stdout
    verdict = ('UNSAT' if 's UNSATISFIABLE' in out else
               'SAT' if 's SATISFIABLE' in out else 'UNKNOWN')
    rec = {'cap': cap, 'verdict': verdict, 'wall_monotonic': time.monotonic() - t0,
           'time_limit': tlim, 'cnf': cnf, 'n_vars': nv, 'n_clauses': len(cls),
           'control_L1_97': len(X97), 'kissat_exit': r.returncode,
           'proof': prf if proof and os.path.exists(prf) else None}
    if verdict == 'UNSAT':
        rec['edge_floor'] = cap + 1
        rec['claim'] = ('every depth-3 MixColumns circuit has |L1| >= %d; '
                        'combine with the certified LP_E profile' % (cap + 1))
    elif verdict == 'SAT':
        rec['claim'] = 'an edge set of size <= %d satisfies the relaxation' % cap
    with open(os.path.join(HERE, 'edge_floor_sat.jsonl'), 'a') as f:
        f.write(json.dumps(rec) + '\n')
    print(json.dumps(rec, indent=1), flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
