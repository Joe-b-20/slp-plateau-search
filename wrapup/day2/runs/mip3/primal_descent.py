#!/usr/bin/env python3
"""PRIMAL DESCENT on the depth-3 record, with the rung ladder as its by-product.

Rung K asks whether the complete depth-3 model admits |L1|+|L2| <= K.  The two
verdicts are both wins, in opposite directions:

  SAT   -> a genuine depth-3 MixColumns circuit of 32+K gates.  The repo's best
           is 97 (K=65), so any K <= 64 that comes back SAT is a RECORD for the
           depth-3 class and narrows the bracket from above.
  UNSAT -> N_depth3 >= 32+K+1, a lower bound in the ladder's evidence class.

Every SAT witness is materialised into an actual gate list (depth 3 by
construction) and handed to the repo's independent oracle at max_depth 3; a
witness that does not verify is discarded, never reported.

Guards.
  * the rung-65 POSITIVE CONTROL is re-run first: it must come back SAT, else
    the encoding is over-constrained and every UNSAT below it is vacuous.
  * the certified floor |L1|+|L2| >= 48 (cert_depth3.json) is asserted as a
    constraint, which prunes hard and is free.
  * a witness at K <= 55 would mean a <=87-gate depth-3 circuit, contradicting
    the lower-bound programme -- it is flagged LOUDLY and not celebrated until
    model3/build_lp have been audited.

Usage: primal_descent.py <Kstart> <Kfloor> <seconds-per-rung>
"""
import sys, os, json, time, subprocess

HERE = '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3'
VERIFY = '/home/joebachir20/xor_ui/slp-plateau-search/verify_circuit.py'
sys.path.insert(0, HERE)
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/pipeline')
from rungs import run as rung_run
from harvest_primal import materialise_depth3

LEDGER = os.path.join(HERE, 'primal_descent.jsonl')
CERTIFIED_FLOOR = 48          # cert_depth3.json, exact rational


def record(d):
    with open(LEDGER, 'a') as f:
        f.write(json.dumps(d) + '\n')
    print(json.dumps({k: v for k, v in d.items() if k not in ('L1', 'L2')}),
          flush=True)


def main():
    K0, KF = int(sys.argv[1]), int(sys.argv[2])
    tlim = float(sys.argv[3])

    print('=== POSITIVE CONTROL: rung 65 must be SAT ===', flush=True)
    c = rung_run(65, 900.0, 1, None)
    if c['status'] not in ('OPTIMAL', 'FEASIBLE'):
        print('!!! CONTROL FAILED: rung 65 is %s -- the encoding is vacuous, '
              'aborting.' % c['status'])
        return 2
    print('control OK (rung 65 SAT, |L1|=%d |L2|=%d)' % (c['n_L1'], c['n_L2']),
          flush=True)

    best = 97
    for K in range(K0, KF - 1, -1):
        t0 = time.monotonic()
        r = rung_run(K, tlim, 1, CERTIFIED_FLOOR)
        r['wall'] = time.monotonic() - t0
        st = r['status']
        if st == 'INFEASIBLE':
            r['claim'] = 'N_depth3 >= %d (rung ladder, solver evidence class)' % (32 + K + 1)
            record(r)
            print('=> rung %d UNSAT: N_depth3 >= %d. Ladder direction reached; '
                  'stopping the descent.' % (K, 32 + K + 1))
            break
        if st == 'UNKNOWN':
            r['claim'] = None
            record(r)
            print('=> rung %d UNDECIDED in %.0fs; stopping.' % (K, tlim))
            break
        # SAT: materialise and verify for real
        gates, err = materialise_depth3(r['L1'], r['L2'])
        if gates is None:
            r['materialise_error'] = err
            record(r)
            print('=> rung %d SAT but not materialisable: %s' % (K, err))
            continue
        path = os.path.join(HERE, 'depth3_%dgates.json' % len(gates))
        json.dump({'gates': gates}, open(path, 'w'))
        v = subprocess.run([sys.executable, VERIFY, path, '3'],
                           capture_output=True, text=True)
        r['gates'] = len(gates)
        r['verify_stdout'] = v.stdout.strip()
        r['verified'] = (v.returncode == 0)
        r['path'] = path
        record(r)
        if not r['verified']:
            print('=> rung %d SAT but the circuit FAILED the oracle -- discarded'
                  % K)
            os.remove(path)
            continue
        best = min(best, len(gates))
        print('=> VERIFIED depth-3 circuit with %d gates (was 97). '
              'N_depth3 <= %d' % (len(gates), best))
        if len(gates) <= 87:
            print('!!!!! <=87 AT DEPTH 3. STOP AND AUDIT model3.py/build_lp.py '
                  'before any claim: this contradicts the depth-3 lower-bound '
                  'programme.')
            break
    print('BEST verified depth-3 gate count this run: %d' % best)


if __name__ == '__main__':
    main()
