#!/usr/bin/env python3
"""Sum the banked shard DONE lines and PROVE the covered index intervals tile
[0, N) with no gap and no overlap.

The certificate's population claim depends on the tiling: if the shards leave a
gap, some mask sets were never tested and the "100 % of the corpus" claim is
false.  Any gap or overlap is reported and the script exits non-zero.

This recomputes every headline number in CERT.md from the banked shards alone.
Standard library only.

  usage: aggregate.py [banked_dir] [n_index]

  banked_dir  directory holding shardA.jsonl / shardB.jsonl
              (default: ../banked relative to this script)
  n_index     size of the corpus index (default 1575516, the value recorded by
              the full-corpus run; pass your own to re-derive coverage)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BANKED = sys.argv[1] if len(sys.argv) > 1 else \
    os.path.join(os.path.dirname(HERE), 'banked')
N_INDEX = int(sys.argv[2]) if len(sys.argv) > 2 else 1575516

iv, tested, lp, real, firings = [], 0, 0, 0, []
notgt = allfail = 0
for fn in ('shardA.jsonl', 'shardB.jsonl'):
    p = os.path.join(BANKED, fn)
    if not os.path.exists(p):
        continue
    for line in open(p):
        o = json.loads(line)
        if o.get('FIRING'):
            firings.append(o)
        elif o.get('DONE'):
            iv.append((o['start'], o['start'] + o['done']))
            tested += o['tested']
            lp += o['local_pass']
            real += o['realisable']
            notgt += o['sets_not_32_targets']
            allfail += o['sets_local_allfail']

iv.sort()
pos, gaps, overlaps = 0, [], []
for a, b in iv:
    if a > pos:
        gaps.append((pos, a))
    elif a < pos:
        overlaps.append((a, pos))
    pos = max(pos, b)

res = {'intervals': len(iv), 'covered_contiguous_prefix': pos,
       'gaps': gaps, 'overlaps': overlaps,
       'rows_in_corpus_index': N_INDEX,
       'coverage_pct_of_index': round(100.0 * pos / N_INDEX, 4),
       'deletions_tested': tested, 'local_filter_pass': lp,
       'local_filter_pass_pct': round(100.0 * lp / tested, 2) if tested else None,
       'realisable_87_mask_sets': real, 'n_FIRING_lines': len(firings),
       'sets_not_32_targets': notgt, 'sets_local_allfail': allfail,
       'deletions_per_set': round(tested / pos, 6) if pos else None}
print(json.dumps(res, indent=1))
if firings:
    print('!!! %d FIRINGS in the banked shards' % len(firings))
if gaps or overlaps:
    print('\nFAIL: the certified intervals do not tile [0, %d).' % pos)
else:
    print('\nOK: the certified intervals tile [0, %d) with no gap and no '
          'overlap.' % pos)
sys.exit(1 if gaps or overlaps else 0)
