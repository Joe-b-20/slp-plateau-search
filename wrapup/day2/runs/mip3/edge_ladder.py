#!/usr/bin/env python3
"""Ladder on the edge floor: the largest cap that is UNSAT is the payoff.

UNSAT at cap C  =>  every depth-3 MixColumns circuit has |L1| >= C+1, which
composes with the CERTIFIED per-branch LP profile for free:

    N_depth3 >= 32 + min over E >= C+1 of certified LP_E

    C+1 = 21 -> 81   23 -> 82   24 -> 83   25 -> 84   26 -> 85   27 -> 85

27 is the ceiling: the verified 97@3 circuit uses 27 edges, so the true floor
is at most 27 and this route cannot on its own reach the 56 (=> 88) target.

UNSAT at a higher cap is the STRONGER statement (|X| <= 19 implies |X| <= 22),
so the ladder climbs and stops at the first cap that is SAT or undecided.

Usage: edge_ladder.py <cap0> <cap1> <seconds per cap>
"""
import sys, os, json, time, subprocess

HERE = '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3'
LEDGER = os.path.join(HERE, 'edge_ladder.jsonl')


def payoff(F):
    s = json.load(open(os.path.join(HERE, 'branch_summary_E18_48.json')))
    prof = {r['E']: r.get('certified_bound') for r in s['branches']}
    vals = [prof[E] for E in range(F, 49) if prof.get(E) is not None]
    vals += [E + 8 for E in range(max(F, 49), 56)]
    return min(vals + [56]) if vals else 56


def main():
    c0, c1 = int(sys.argv[1]), int(sys.argv[2])
    secs = float(sys.argv[3])
    floor = 18                      # certified: branches E <= 17 are infeasible
    for cap in range(c0, c1 + 1):
        t0 = time.monotonic()
        r = subprocess.run([sys.executable, '-u',
                            os.path.join(HERE, 'edge_floor.py'),
                            str(secs), 'all', str(cap)],
                           cwd=HERE, capture_output=True, text=True)
        out = r.stdout
        verdict = ('UNSAT' if 'UNSAT at cap' in out else
                   'SAT' if 'SAT at cap' in out else 'UNKNOWN')
        rec = {'cap': cap, 'verdict': verdict,
               'wall_monotonic': time.monotonic() - t0, 'seconds_budget': secs,
               'stdout_tail': out.strip().split('\n')[-1] if out.strip() else ''}
        if verdict == 'UNSAT':
            floor = cap + 1
            b = payoff(floor)
            rec['edge_floor'] = floor
            rec['bound_L1L2'] = b
            rec['N_depth3_ge'] = 32 + b
            rec['claim'] = ('|L1| >= %d (CP-SAT UNSAT, solver evidence class) '
                            'composed with the certified LP_E profile '
                            '=> N_depth3 >= %d' % (floor, 32 + b))
        with open(LEDGER, 'a') as f:
            f.write(json.dumps(rec) + '\n')
        print(json.dumps(rec), flush=True)
        if verdict != 'UNSAT':
            print('ladder stops at cap %d (%s); best floor established = %d '
                  '=> N_depth3 >= %d' % (cap, verdict, floor, 32 + payoff(floor)),
                  flush=True)
            break
    print('FINAL edge floor %d => N_depth3 >= %d' % (floor, 32 + payoff(floor)))


if __name__ == '__main__':
    main()
