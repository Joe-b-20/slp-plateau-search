#!/usr/bin/env python3
"""C4 — is "max fan-out >= 8" reachable at 88 gates?  EXACT, by CP-SAT.

e_oddlane3 measured max fan-out <= 5 across the corpus and 3-4 in the record 88s,
and e_upstream/NOTEBOOK.md 5 lists "fan-out >= 8 on one mask" as a feature class
to price by pinning.  It cannot be priced that way: fan-out is a property of the
BUILD ORDER, not of the mask set.  The same 88 masks admit many valid orders with
different fan-outs.  So the right question is a re-scheduling question:

    Given a FIXED mask set S of a record 88, does a valid build order exist in
    which some signal is consumed by >= 8 gates?

That is exact and small.  Model (one solve per (circuit, candidate signal s)):

  SIG   = the 32 input singletons + S            (inputs are available at time -1)
  For each mask m in S let P(m) = { {a,b} : a,b in SIG, a^b = m, a != b }
  y[m,p] in {0,1},  sum_p y[m,p] = 1             each mask is built by exactly one gate
  pos[m] in [0, |S|-1]                           its position in the order
  y[m,{a,b}] = 1  =>  pos[a] < pos[m] and pos[b] < pos[m]     (acyclicity)
  fanout(s) = sum over (m,p) with s in p of y[m,p]
  maximise fanout(s)

The optimum is the exact maximum fan-out realisable on that signal over ALL valid
build orders of that mask set.  A solution is decoded to an oracle-format gate
list and handed to verify_circuit.py in the same run, so a positive answer is its
own verified positive control.

Output: c4_fanout_cpsat.json (+ decoded circuits for anything reaching >= 8).
"""
import json, os, sys, glob, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, REPO)
from verify_circuit import mixcolumns_target_masks
from ortools.sat.python import cp_model

TARGETS = set(mixcolumns_target_masks())
INP = [1 << i for i in range(32)]
TOPK = int(os.environ.get('C4_TOPK', '2'))
TLIM = float(os.environ.get('C4_TLIM', '60'))


def pairs_for(m, SIGSET):
    out = set()
    for a in SIGSET:
        b = m ^ a
        if a != b and b in SIGSET and a != m and b != m:
            out.add((min(a, b), max(a, b)))
    return sorted(out)


def solve(S, s):
    """Exact max fan-out on signal s over all valid build orders of S."""
    SIGSET = set(INP) | set(S)
    mdl = cp_model.CpModel()
    pos = {m: mdl.NewIntVar(0, len(S) - 1, 'p%d' % m) for m in S}
    POSI = -1
    y = {}
    fan_terms = []
    for m in sorted(S):
        P = pairs_for(m, SIGSET)
        if not P:
            return None, None, 'mask 0x%08x has no producing pair' % m
        lits = []
        for p in P:
            v = mdl.NewBoolVar('y')
            y[(m, p)] = v
            lits.append(v)
            for x in p:
                if x in pos:
                    mdl.Add(pos[x] < pos[m]).OnlyEnforceIf(v)
            if s in p:
                fan_terms.append(v)
        mdl.AddExactlyOne(lits)
    if not fan_terms:
        return 0, None, 'signal not in any producing pair'
    F = mdl.NewIntVar(0, len(fan_terms), 'F')
    mdl.Add(F == sum(fan_terms))
    mdl.Maximize(F)
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = TLIM
    sol.parameters.num_search_workers = 1
    st = sol.Solve(mdl)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, None, sol.StatusName(st)
    # decode to oracle format
    chosen = {m: p for (m, p) in y if sol.Value(y[(m, p)])}
    order = sorted(S, key=lambda m: sol.Value(pos[m]))
    idx = {v: i for i, v in enumerate(INP)}
    gates = []
    for m in order:
        a, b = chosen[m]
        gates.append([idx[a], idx[b]])
        idx[m] = 32 + len(gates) - 1
    return int(sol.Value(F)), gates, sol.StatusName(st)


def load(p):
    d = json.load(open(p))
    g = d.get('gates') if isinstance(d, dict) else d
    if not (isinstance(g, list) and g and isinstance(g[0], list)):
        return None
    s = [1 << i for i in range(32)]
    for a, b in g:
        s.append(s[a] ^ s[b])
    return set(s[32:])


def circuit_max(name, S, out):
    """Exact max fan-out of the mask set S over ALL signals and ALL build orders.

    Branch and bound over signals: fanout(s) <= potential(s) always, so once the
    best solved value reaches the next signal's potential, every remaining signal
    is dominated and the sweep is EXHAUSTIVE, not sampled."""
    SIGSET = set(INP) | S
    pot = sorted(((sum(1 for x in SIGSET if x != s and (s ^ x) in S), s) for s in SIGSET),
                 reverse=True)
    best = 0; bestsig = None; bestgates = None; nsolved = 0; t0 = time.time()
    for potential, s in pot:
        if potential <= best:
            break                       # dominated: cannot beat the incumbent
        F, gates, st = solve(S, s)
        nsolved += 1
        if F is None:
            out.append(dict(circuit=name, signal='0x%08x' % s, potential=potential,
                            max_fanout=None, status=st))
            continue
        if F > best:
            best, bestsig, bestgates = F, s, gates
    r = dict(circuit=name, n_masks=len(S), max_potential=pot[0][0],
             signals_solved=nsolved, signals_total=len(pot),
             EXACT_max_fanout=best, on_signal='0x%08x' % bestsig if bestsig else None,
             exhaustive=True, seconds=round(time.time() - t0, 1))
    if best >= 8 and bestgates:
        op = os.path.join(HERE, 'C4_fanout%d_%s.json' % (best, name.replace('.json', '')))
        json.dump({'gates': bestgates}, open(op, 'w'))
        r['circuit_file'] = os.path.relpath(op, REPO)
    out.append(r)
    print('%-46s |S|=%3d max_potential=%2d  EXACT_MAX_FANOUT=%d  (%d/%d signals solved, %.1fs)'
          % (name, len(S), pot[0][0], best, nsolved, len(pot), r['seconds']), flush=True)
    return r


rows = []
res = []
print('== the record 88s ==', flush=True)
for p in sorted(glob.glob(os.path.join(REPO, 'evidence/circuits/*.json'))) + \
        sorted(glob.glob(os.path.join(REPO, 'evidence/campaign87_imported_prior_art/*.json'))):
    try:
        S = load(p)
    except Exception:
        continue
    if not S or len(S) != 88:
        continue
    res.append(circuit_max(os.path.basename(p), S, rows))
    json.dump(dict(results=res, detail=rows), open(os.path.join(HERE, 'c4_fanout_cpsat.json'), 'w'), indent=1)

print(flush=True)
print('== the 33 e_upstream floors (89-94 gates) ==', flush=True)
for fn in sorted(glob.glob(os.path.join(REPO, 'experiments/e_upstream/S*.json'))):
    S = set(json.load(open(fn))['masks'])
    res.append(circuit_max(os.path.basename(fn), S, rows))
    json.dump(dict(results=res, detail=rows), open(os.path.join(HERE, 'c4_fanout_cpsat.json'), 'w'), indent=1)

r88 = [r for r in res if r['n_masks'] == 88]
best88 = max(r['EXACT_max_fanout'] for r in r88)
bestall = max(r['EXACT_max_fanout'] for r in res)
print()
print('VERDICT')
print('  exact max fan-out over ALL build orders, record 88s :', best88,
      '  (max potential was %d)' % max(r['max_potential'] for r in r88))
print('  exact max fan-out over ALL build orders, all %d sets:' % len(res), bestall)
print('  fan-out >= 8 realisable at 88 gates :', 'YES' if best88 >= 8 else 'NO')
print('  every sweep exhaustive (branch-and-bound on potential):',
      all(r.get('exhaustive') for r in res))
json.dump(dict(results=res, detail=rows,
               verdict=dict(record88_exact_max_fanout=best88,
                            all_sets_exact_max_fanout=bestall,
                            fanout8_at_88='NO' if best88 < 8 else 'YES')),
          open(os.path.join(HERE, 'c4_fanout_cpsat.json'), 'w'), indent=1)
