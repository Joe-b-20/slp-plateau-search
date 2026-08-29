#!/usr/bin/env python3
"""E-DECOMPOSED dual bound: run SCIP on each branch  sum_e x_e == E  separately.

Why this beats one monolithic run.  |L1| = sum_e x_e is an integer, so

    min (|L1|+|L2|)  =  min over E >= 0 of  MIP_E                       (*)

and the branches split into three kinds:

  E <= 17          LP-infeasible          (certified, branch_summary.json)
  18 <= E <= 55    needs work             (certified LP_E in branch_summary.json;
                                           this script raises them with SCIP)
  E >= 56          trivially >= 56        (objective >= sum_e x_e = E)

The certified LP profile already puts LP_E >= 56 for every E >= 30 and
LP_18 = 57.37, so the only branches that can hold the bound below 56 are
E in {19,...,29} -- ELEVEN subproblems, each far more constrained than the
whole.  The overall solver-proved bound is

    min( min_E scip_dual[E] , min over untouched E of certified LP_E )

Each round gives every listed E the same time slice, then the slice doubles,
so the weakest branch is never starved.  State is append-only in
scip_branches_state.json; killing and restarting the script resumes.

Usage: scip_branches.py <Elist, comma separated> <first-round seconds> <rounds>
"""
import sys, os, json, time, subprocess

HERE = '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3'
STATE = os.path.join(HERE, 'scip_branches_state.json')


def certified_lp_profile():
    """certified LP_E from branch_summary.json (exact rational bounds)."""
    s = json.load(open(os.path.join(HERE, 'branch_summary.json')))
    prof, infeas = {}, []
    for r in s['branches']:
        if r.get('infeasible'):
            infeas.append(r['E'])
        elif 'certified_bound' in r:
            prof[r['E']] = r['certified_bound']
    return prof, infeas


# C7 is the single row  sum_m deg(m) y_m >= 44  with max_m deg(m) = 6
# (verified: degree histogram 1:5020 2:2052 3:584 4:157 5:68 6:16), so
#        |L2| >= ceil(44/6) = 8
# for EVERY depth-3 circuit.  Hence branch E contributes at least E + 8, which
# already exceeds 56 for every E >= 49 -- no LP needed up there.
L2_FLOOR = 8


def overall(state, prof, infeas):
    """min over ALL E of the best known bound -- the reportable number.

    E <= 17        LP-infeasible                       (certified)
    18 <= E <= 48  certified LP profile + SCIP duals
    E >= 49        E + L2_FLOOR >= 57                  (certified, C7)
    """
    worst, arg = None, None
    for E in range(0, 56):
        if E in infeas:
            continue
        v = prof.get(E)
        if v is None and E >= 49:
            v = E + L2_FLOOR
        s = state.get(str(E), {}).get('best_dual_ceil')
        if s is not None:
            v = s if v is None else max(v, s)
        if v is None:
            return None, E          # an uncovered branch: no claim possible
        if worst is None or v < worst:
            worst, arg = v, E
    return min(worst, 56), arg


def main():
    Es = [int(v) for v in sys.argv[1].split(',')]
    secs = float(sys.argv[2])
    rounds = int(sys.argv[3])
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    prof, infeas = certified_lp_profile()
    print('certified LP profile covers E=%s; infeasible E=%s'
          % (sorted(prof), infeas), flush=True)

    for rd in range(rounds):
        for E in Es:
            k = str(E)
            tag = 'E%d' % E
            t0 = time.monotonic()
            cmd = [sys.executable, '-u', os.path.join(HERE, 'scip_mip.py'),
                   str(secs), '1', tag, '--fixE', str(E), '--emph', 'dual']
            print('=== round %d  E=%d  %.0fs ===' % (rd, E, secs), flush=True)
            subprocess.run(cmd, cwd=HERE,
                           stdout=open(os.path.join(HERE, 'logs/scip_%s.log' % tag), 'a'),
                           stderr=subprocess.STDOUT)
            res = os.path.join(HERE, 'scip_result_%s.json' % tag)
            rec = state.setdefault(k, {'E': E, 'seconds': 0.0})
            rec['seconds'] += time.monotonic() - t0
            if os.path.exists(res):
                r = json.load(open(res))
                rec['status'] = r['status']
                if r['status'] == 'infeasible':
                    if E == 27:
                        # POSITIVE CONTROL: the verified 97@3 circuit lives on
                        # E=27.  Calling it infeasible means the fixE machinery
                        # is broken and every other "closed" verdict is void.
                        state['_CONTROL_FAILED'] = 'E=27 reported infeasible'
                        json.dump(state, open(STATE, 'w'), indent=1)
                        print('!!! CONTROL FAILED: E=27 infeasible. ABORTING; '
                              'all branch verdicts are void.', flush=True)
                        return 2
                    rec['best_dual_ceil'] = 10 ** 6      # branch closed
                    rec['closed'] = True
                else:
                    import math
                    c = 32 + math.ceil(r['dual_bound'] - 1e-9) - 32
                    rec['dual_bound'] = r['dual_bound']
                    rec['best_dual_ceil'] = max(rec.get('best_dual_ceil', 0), c)
                    rec['nodes'] = r['nodes']
                    rec['primal_bound'] = r['primal_bound']
            ov, arg = overall(state, prof, infeas)
            state['_overall'] = {'bound_L1L2': ov, 'argmin_E': arg,
                                 'N_depth3_ge': (32 + ov) if ov else None}
            json.dump(state, open(STATE, 'w'), indent=1)
            print('>>> E=%d -> %s ; OVERALL |L1|+|L2| >= %s (weakest branch E=%s)'
                  ' => N_depth3 >= %s'
                  % (E, rec.get('best_dual_ceil'), ov, arg,
                     (32 + ov) if ov else None), flush=True)
        secs *= 2


if __name__ == '__main__':
    main()
