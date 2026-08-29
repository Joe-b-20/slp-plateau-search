#!/usr/bin/env python3
"""The depth-UNRESTRICTED side, for the record.

What is provable here without new circuit-complexity technique:

  (1) N >= 32.  The 32 targets are distinct, nonzero, and none of them is an
      input (all have weight 5 or 7), so 32 distinct gates emit them.

  (2) N >= 33.  Every target t = p ^ q needs a parent that is neither an
      input nor a target:
        - both parents inputs  => wt(t) <= 2, but wt(t) in {5,7};
        - input + target       => t ^ (1<<i) would be a target;
        - target + target      => t ^ t' would be a target.
      This script checks the last two exhaustively (both counts are 0), so at
      least one support gate exists.

  (3) The bit-plane work bound is NOT binding.  For each of the 8 planes the
      required projections are 8 distinct non-input vectors of F_2^4, so any
      circuit contains >= 8 gates with a new plane-p projection and
      sum_p n_p >= 64.  But a cross-plane gate is counted in every plane it
      touches, and G = sum_p n_p - #2plane - 2*#3plane, so turning this into
      a bound on G needs an UPPER bound on cross-plane gates, which nothing
      supplies; measured sum_p n_p in real 88-gate circuits is 171-176 versus
      the floor 64 (W5 burn/handreduce/WAVE2_INSIGHTS.md).  Angle dead.

Run: python3 general_bound.py
"""
import sys, itertools
sys.path.insert(0, '/home/joebachir20/xor_ui/slp-plateau-search/pipeline')
from mixcolumns_core import TARGETS

pc = lambda m: bin(m).count('1')


def main():
    T = set(TARGETS)
    assert len(T) == 32 and 0 not in T
    assert all(pc(t) >= 5 for t in T), 'a target of weight <= 1 would be an input'
    tt = [t for t in TARGETS if any((t ^ u) in T and (t ^ u) != u for u in TARGETS)]
    ti = [t for t in TARGETS if any((t ^ (1 << i)) in T for i in range(32))]
    print('targets of the form target ^ target : %d' % len(tt))
    print('targets of the form target ^ input  : %d' % len(ti))
    print('min pairwise XOR weight among targets: %d'
          % min(pc(a ^ b) for a, b in itertools.combinations(TARGETS, 2)))
    ok = not tt and not ti
    print('=> every target has a non-input non-target parent:', ok)
    print('UNCONDITIONAL, ANY DEPTH:  N >= %d' % (33 if ok else 32))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
