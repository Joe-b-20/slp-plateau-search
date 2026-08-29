#!/usr/bin/env python3
"""SCIP 10 branch-and-cut on the strengthened complete depth-3 model.

Same system as mip3.py (HiGHS) -- build_lp.build(True, level), every row a
theorem about depth-3 circuits -- but solved by SCIP, whose cut loop and
node LPs are much stronger.  Two products, both wanted:

  DUAL side   : the proved dual bound d gives   N_depth3 >= 32 + ceil(d).
                d = 56  ==>  N_depth3 >= 88  ==>  "every <=87-gate MixColumns
                circuit has depth >= 4".  This is a SOLVER CLAIM (a log), not
                a certificate; certify.py remains the certified channel.
  PRIMAL side : every incumbent is a genuine depth-3 circuit of 32+obj gates
                (the model is exact, not a relaxation, on the x/y variables).
                Incumbents are dumped the instant SCIP finds them so a killed
                run still leaves its circuits behind.

Controls (mandatory, both run before the solve):
  * the verified 97-gate depth-3 circuit is evaluated against every row and
    against the objective cap; any violation aborts.  A model that cuts off a
    real circuit would make every bound here vacuous.
  * that same point is handed to SCIP as a start solution and SCIP must accept
    it at objective 65.

Usage:
  scip_mip.py <seconds> <level> <tag> [--cap 65] [--fixE E] [--fixY Y]
              [--fixY4 Y4] [--threads N] [--emph dual|default]

--fixE/--fixY/--fixY4 solve one node of the branch tree (sum x_e == E etc.).
An INFEASIBLE verdict there closes that node.  Note the 97@3 control point has
(E,Y) = (27,38), so on a fixed node the control is checked against the base
rows only -- the node equations are a branch of an exhaustive case split, not
claimed to hold for every circuit.
"""
import sys, os, json, time, math

HERE = '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3'
sys.path.insert(0, HERE)
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/pipeline')
from build_lp import build, control_point
from model3 import pc


def parse_args(argv):
    a = {'secs': float(argv[1]), 'level': int(argv[2]), 'tag': argv[3],
         'cap': 65, 'fixE': None, 'fixY': None, 'fixY4': None,
         'threads': 1, 'emph': 'dual'}
    i = 4
    while i < len(argv):
        k = argv[i].lstrip('-')
        a[k] = argv[i + 1]
        i += 2
    for k in ('cap', 'fixE', 'fixY', 'fixY4', 'threads'):
        if a[k] is not None:
            a[k] = int(a[k])
    return a


def main():
    A = parse_args(sys.argv)
    t0 = time.monotonic()
    rows, cost, meta = build(True, A['level'])
    nvar, base = meta['nvar'], meta['base']
    print('[%.1fs] model: %d rows, %d vars (%d costed)'
          % (time.monotonic() - t0, len(rows), nvar, base), flush=True)

    # ---------------- CONTROL 1: the verified 97@3 circuit ----------------
    p = control_point(meta)
    bad = [t for terms, rhs, t in rows if sum(c * p[j] for j, c in terms) < rhs]
    obj97 = sum(cost[j] * p[j] for j in range(nvar))
    print('CONTROL 97@3: violations=%d  objective=%d' % (len(bad), obj97), flush=True)
    if bad:
        print('CONTROL FAILED -> every bound from this model is VACUOUS'); return 2
    if obj97 != 65:
        print('CONTROL FAILED: control objective %d != 65' % obj97); return 2
    if A['cap'] is not None and obj97 > A['cap']:
        print('CONTROL FAILED: cap %d cuts off the real circuit' % A['cap']); return 2

    xs = [meta['xi'][e] for e in meta['E']]
    ys = [meta['yi'][m] for m in meta['L2']]
    y4 = [meta['yi'][m] for m in meta['L2'] if pc(m) == 4]
    node = A['fixE'] is not None or A['fixY'] is not None or A['fixY4'] is not None
    if node:
        print('NODE: E=%s Y=%s Y4=%s (control point has E=%d Y=%d Y4=%d)'
              % (A['fixE'], A['fixY'], A['fixY4'],
                 sum(p[j] for j in xs), sum(p[j] for j in ys),
                 sum(p[j] for j in y4)), flush=True)

    # ---------------- build the SCIP problem ----------------
    from pyscipopt import (Model, quicksum, SCIP_PARAMSETTING, SCIP_PARAMEMPHASIS,
                           SCIP_EVENTTYPE, Eventhdlr)

    m = Model('depth3_L%d_%s' % (A['level'], A['tag']))
    V = [m.addVar(vtype='B', name='p%d' % j, obj=float(cost[j])) for j in range(nvar)]
    m.setMinimize()
    for terms, rhs, tag in rows:
        m.addCons(quicksum(float(c) * V[j] for j, c in terms) >= float(rhs))
    if A['cap'] is not None:
        m.addCons(quicksum(V[j] for j in range(base)) <= float(A['cap']), name='objcap')
    if A['fixE'] is not None:
        m.addCons(quicksum(V[j] for j in xs) == float(A['fixE']), name='fixE')
    if A['fixY'] is not None:
        m.addCons(quicksum(V[j] for j in ys) == float(A['fixY']), name='fixY')
    if A['fixY4'] is not None:
        m.addCons(quicksum(V[j] for j in y4) == float(A['fixY4']), name='fixY4')
    print('[%.1fs] SCIP model built' % (time.monotonic() - t0), flush=True)

    # ---------------- CONTROL 2: SCIP accepts the real circuit ------------
    # The control point is fed whenever it satisfies the node equations too.
    # On the node E=27 (its own edge count) this is the mandatory POSITIVE
    # control for the fixE machinery: if SCIP ever called that node infeasible
    # the branch machinery would be closing branches by a bug, and every
    # "infeasible" verdict elsewhere would be worthless.
    ctrl_fits = (
        (A['fixE'] is None or A['fixE'] == sum(p[j] for j in xs)) and
        (A['fixY'] is None or A['fixY'] == sum(p[j] for j in ys)) and
        (A['fixY4'] is None or A['fixY4'] == sum(p[j] for j in y4)))
    if ctrl_fits:
        s = m.createSol()
        for j in range(nvar):
            m.setSolVal(s, V[j], float(p[j]))
        ok = m.checkSol(s)
        acc = m.addSol(s, free=True)
        print('CONTROL start-solution: checkSol=%s addSol=%s (node=%s)'
              % (ok, acc, node), flush=True)
        if not ok:
            print('CONTROL FAILED: SCIP rejects the verified 97@3 circuit'); return 2
    else:
        print('control point does not satisfy the node equations '
              '(expected off-node); base-row control above still applies',
              flush=True)

    m.setParam('limits/time', A['secs'])
    m.setParam('limits/gap', 0.0)
    m.setParam('display/freq', 100)
    m.setParam('display/verblevel', 4)
    if A['emph'] == 'dual':
        m.setEmphasis(SCIP_PARAMEMPHASIS.OPTIMALITY)
        m.setSeparating(SCIP_PARAMSETTING.AGGRESSIVE)
    elif A['emph'] == 'proof':
        m.setEmphasis(SCIP_PARAMEMPHASIS.PHASEPROOF)
        m.setSeparating(SCIP_PARAMSETTING.AGGRESSIVE)
    elif A['emph'] == 'feas':
        m.setEmphasis(SCIP_PARAMEMPHASIS.FEASIBILITY)
    # closecuts computes a relative-interior point by solving an auxiliary LP;
    # on this model that ate 190 s of a 245 s smoke run for +0.000 dual.
    for k, v in (('separating/closecuts/freq', -1),
                 ('separating/closecuts/maxlpiterfactor', 0.0)):
        try:
            m.setParam(k, v)
        except Exception:
            pass
    try:
        m.setParam('limits/memory', 6000.0)
    except Exception:
        pass
    try:
        m.setParam('parallel/maxnthreads', A['threads'])
    except Exception:
        pass

    RES = os.path.join(HERE, 'scip_result_%s.json' % A['tag'])
    TRJ = os.path.join(HERE, 'scip_traj_%s.jsonl' % A['tag'])
    INC = os.path.join(HERE, 'scip_incumbents_%s.jsonl' % A['tag'])
    trj = open(TRJ, 'a', buffering=1)
    inc = open(INC, 'a', buffering=1)

    class H(Eventhdlr):
        def eventinit(self):
            self.model.catchEvent(SCIP_EVENTTYPE.BESTSOLFOUND, self)
            self.model.catchEvent(SCIP_EVENTTYPE.NODESOLVED, self)
            self.last = 0.0
            self.bestdb = None

        def eventexit(self):
            self.model.dropEvent(SCIP_EVENTTYPE.BESTSOLFOUND, self)
            self.model.dropEvent(SCIP_EVENTTYPE.NODESOLVED, self)

        def eventexec(self, event):
            M = self.model
            et = event.getType()
            now = time.monotonic()
            if et == SCIP_EVENTTYPE.BESTSOLFOUND:
                sol = M.getBestSol()
                o = M.getSolObjVal(sol)
                rec = {'t': now - t0, 'obj': o, 'dual': M.getDualbound(),
                       'L1': [e for e in meta['E']
                              if M.getSolVal(sol, V[meta['xi'][e]]) > 0.5],
                       'L2': [mm for mm in meta['L2']
                              if M.getSolVal(sol, V[meta['yi'][mm]]) > 0.5]}
                rec['gates'] = 32 + len(rec['L1']) + len(rec['L2'])
                inc.write(json.dumps(rec) + '\n')
                print('### INCUMBENT obj=%.1f -> %d gates at depth 3 (t=%.0fs)'
                      % (o, rec['gates'], now - t0), flush=True)
            else:
                if now - self.last < 30.0:
                    return
                self.last = now
                db = M.getDualbound()
                trj.write(json.dumps(
                    {'t': now - t0, 'dual': db, 'primal': M.getPrimalbound(),
                     'nodes': M.getNNodes(),
                     'N_depth3_ge': 32 + math.ceil(db - 1e-9)}) + '\n')

    h = H()
    m.includeEventhdlr(h, 'traj', 'dual bound trajectory')

    m.optimize()
    wall = time.monotonic() - t0
    db = m.getDualbound()
    out = {'model': 'depth3_strong_scip', 'tag': A['tag'], 'level': A['level'],
           'cap': A['cap'], 'fixE': A['fixE'], 'fixY': A['fixY'], 'fixY4': A['fixY4'],
           'status': m.getStatus(), 'wall_monotonic': wall,
           'nodes': m.getNNodes(), 'gap': m.getGap(),
           'dual_bound': db, 'primal_bound': m.getPrimalbound(),
           'control_violations': 0, 'control_obj': obj97,
           'N_depth3_lower_bound': 32 + math.ceil(db - 1e-9),
           'scip_version': str(m.version())}
    if m.getStatus() == 'infeasible':
        out['node_closed'] = True
    print(json.dumps(out, indent=1), flush=True)
    json.dump(out, open(RES, 'w'), indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
