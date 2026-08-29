#!/usr/bin/env python3
"""Turn SCIP incumbents into REAL depth-3 circuits and verify them.

Any integer point of the model is an actual depth-3 MixColumns circuit of
32 + |L1| + |L2| gates, so every incumbent SCIP reports is a candidate record
for the depth-3 class (the repo's best is 97).

Unlike primal3.materialise this builds each target ONLY from inputs / level-1 /
level-2 signals, so the emitted circuit is depth 3 by construction rather than
by luck -- materialising a target from a previously emitted target would give a
valid MixColumns circuit of depth 4, which is not what is being claimed.  The
result is then handed to the repo's independent oracle with max_depth = 3.

Usage: harvest_primal.py <incumbents.jsonl> [more.jsonl ...]
"""
import sys, os, json, subprocess, itertools

HERE = '/home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3'
VERIFY = '/home/joebachir20/xor_ui/slp-plateau-search/verify_circuit.py'
sys.path.insert(0, HERE)
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/pipeline')
from mixcolumns_core import TARGETS
from model3 import pc, BITS


def materialise_depth3(L1, L2):
    """gate list; every target is built from level-<=2 signals only."""
    sig = {1 << i: i for i in range(32)}          # mask -> signal index
    lvl = {1 << i: 0 for i in range(32)}
    gates = []

    def emit(a, b):
        gates.append([sig[a], sig[b]])
        m = a ^ b
        if m not in sig:
            sig[m] = 32 + len(gates) - 1
            lvl[m] = max(lvl[a], lvl[b]) + 1
        return m

    for e in L1:                                  # level 1
        bs = BITS(e)
        if e not in sig:
            emit(1 << bs[0], 1 << bs[1])
    for m in L2:                                  # level 2
        if m in sig:
            continue
        bs = BITS(m)
        done = False
        if pc(m) == 4:
            for i, j, k in ((1, 2, 3), (2, 1, 3), (3, 1, 2)):
                e1 = (1 << bs[0]) | (1 << bs[i]); e2 = (1 << bs[j]) | (1 << bs[k])
                if e1 in sig and e2 in sig and lvl[e1] <= 1 and lvl[e2] <= 1:
                    emit(e1, e2); done = True; break
        else:
            for i in range(3):
                e = m ^ (1 << bs[i])
                if e in sig and lvl[e] <= 1:
                    emit(1 << bs[i], e); done = True; break
        if not done:
            return None, 'level-2 mask %d not buildable from the given edges' % m
    low = [s for s in sig if lvl[s] <= 2]          # inputs + L1 + L2 only
    for t in TARGETS:                              # level 3
        if t in sig and lvl[t] <= 3:
            continue
        hit = None
        for a in low:
            b = t ^ a
            if b != a and b in sig and lvl[b] <= 2:
                hit = (a, b); break
        if hit is None:
            return None, 'target %d not expressible from level<=2 signals' % t
        emit(*hit)
    return gates, None


def verify(path, max_depth=3):
    r = subprocess.run([sys.executable, VERIFY, path, str(max_depth)],
                       capture_output=True, text=True)
    return r.returncode == 0, r.stdout.strip()


def main():
    best = None
    seen = set()
    for src in sys.argv[1:]:
        if not os.path.exists(src):
            print('missing %s' % src); continue
        for line in open(src):
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            key = (tuple(sorted(rec['L1'])), tuple(sorted(rec['L2'])))
            if key in seen:
                continue
            seen.add(key)
            n = 32 + len(rec['L1']) + len(rec['L2'])
            if best is not None and n >= best[0]:
                continue
            gates, err = materialise_depth3(rec['L1'], rec['L2'])
            if gates is None:
                print('%s: obj %s -> %s' % (src, rec.get('obj'), err)); continue
            path = os.path.join(HERE, 'depth3_%dgates_harvest.json' % len(gates))
            json.dump({'gates': gates}, open(path, 'w'))
            ok, msg = verify(path)
            print('%d gates | %s | %s' % (len(gates), msg.replace('\n', ' | '),
                                          'ACCEPTED' if ok else 'REJECTED'))
            if ok:
                best = (len(gates), path)
                if len(gates) <= 87:
                    print('!!! <=87 AT DEPTH 3 -- STOP AND AUDIT: this would '
                          'contradict the lower-bound model. Do not report '
                          'before auditing model3/build_lp.')
            else:
                os.remove(path)
    print('BEST verified depth-3 circuit from incumbents: %s' % (best,))
    if best:
        print('bracket update: N_depth3 <= %d' % best[0])


if __name__ == '__main__':
    main()
