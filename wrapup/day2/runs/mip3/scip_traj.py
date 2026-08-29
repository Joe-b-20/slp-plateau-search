#!/usr/bin/env python3
"""Dual-bound trajectory from SCIP's own display lines.

The Eventhdlr in scip_mip.py only fires on NODESOLVED, and these runs sit in
the ROOT cut loop for hours, so the authoritative trajectory is SCIP's display
table.  Each line gives (time, dualbound, primalbound); the reportable claim is

    N_depth3 >= 32 + ceil(dualbound)

for a whole-model run, or -- for a run with --fixE E -- the bound contributed
by that single branch, to be combined by  min over E  (see scip_branches.py).

Usage: scip_traj.py logs/scip_M1.log [more logs ...]
"""
import sys, os, re, json, math

ROW = re.compile(r'^[a-zA-Z*]?\s*([0-9.]+)s\|\s*(\d+)\s*\|.*\|\s*'
                 r'([-+0-9.eE]+)\s*\|\s*([-+0-9.eE]+)\s*\|')


def traj(path):
    out = []
    for line in open(path, errors='replace'):
        m = ROW.match(line)
        if not m:
            continue
        t, node, db, pb = m.groups()
        try:
            db = float(db)
        except ValueError:
            continue
        try:
            pb = float(pb)
        except ValueError:
            pb = None
        out.append({'t': float(t), 'node': int(node), 'dual': db, 'primal': pb,
                    'bound_L1L2': math.ceil(db - 1e-9)})
    return out


def main():
    for p in sys.argv[1:]:
        if not os.path.exists(p):
            print('missing %s' % p); continue
        T = traj(p)
        tag = os.path.basename(p).replace('scip_', '').replace('.log', '')
        if not T:
            print('%-6s : no display rows yet' % tag); continue
        f, l = T[0], T[-1]
        print('%-6s : %4d rows | first %.0fs dual %.4f | last %.0fs dual %.4f '
              '(|L1|+|L2| >= %d) | primal %s | nodes %d'
              % (tag, len(T), f['t'], f['dual'], l['t'], l['dual'],
                 l['bound_L1L2'], l['primal'], l['node']))
        json.dump(T, open(p.replace('logs/', '').replace('.log', '') + '_traj.json'
                          if False else
                          os.path.join(os.path.dirname(os.path.dirname(p)) or '.',
                                       'scip_trajectory_%s.json' % tag), 'w'), indent=1)


if __name__ == '__main__':
    main()
