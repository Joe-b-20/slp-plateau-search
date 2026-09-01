#!/usr/bin/env python3
"""Credibility control for the adaptive-gate-elimination machinery of ../gte56/.

A lower-bound method is only worth reading if it cannot produce a bound ABOVE
the truth.  This script runs the *same* machinery -- the same Theorem-N formula
and the same `mine` searcher -- on small GF(2) matrices whose minimum XOR-SLP
size has been PROVED EXACTLY by a completely different method (iterated SAT,
with the level below the optimum recorded UNSAT), and checks:

  0. PRECONDITIONS  the matrix hypotheses Lemma F and Theorem N actually need
                 (columns nonzero and pairwise distinct) are CHECKED, not
                 assumed.  One instance in the suite deliberately fails them,
                 to show what the machinery would claim if they were skipped.
  1. SOUNDNESS   every Theorem-N bound is <= the known optimum.
  2. AGREEMENT   the searcher's own exact answer, #targets + minE(full column
                 set), equals the SAT optimum.  These are two unrelated code
                 paths -- a C extras-tree exhaustion and a CNF/CaDiCaL decision
                 procedure -- so agreement is a real cross-check of both.
  3. SLACK       how much the bound loses when the keep-set is forced to be
                 small, which is the regime the MixColumns certificate is
                 actually in.

Why  #targets + minE  IS the optimum.  In a minimum SLP no gate mask repeats
(a repeat is deletable), and every target of weight >= 2 must itself be a gate
mask.  So the gate set is exactly (targets) union (extras), and the minimum
size is #targets + minE where minE is the minimum number of extra masks over
all realizable mask sets containing the targets -- which is exactly what
`mine` decides, by exhausting depth by depth.

Theorem N, restated for an arbitrary matrix with n columns and T targets:
for a family F of admissible keep-sets covering every m-subset of the columns,

        L(M) >= m + min_{K in F} [ (n - |K|) + T + minE_K ].

At m = 0 a single keep-set suffices, and K = all columns makes the bound
exactly the optimum -- so the m = 0 row is a tightness self-check, not news.
The informative rows are the ones with |K| capped, and the m = 1 covering row,
which is the exact analogue of the MixColumns certificate.

Usage:
    python3 run_validation.py [--mine PATH] [--instance NAME] [--max-depth D]
Exit 0 iff every soundness and agreement check passes.
"""

import argparse
import itertools
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def load_matrix(path):
    rows = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(line)
    n = len(rows[0])
    return [sum(1 << c for c in range(n) if row[c] == '1') for row in rows], n


def popcount(x):
    return bin(x).count('1')


def restrict(masks, K):
    out = []
    for m in masks:
        v = 0
        for i, c in enumerate(K):
            if (m >> c) & 1:
                v |= 1 << i
        out.append(v)
    return out


def admissible(masks, K):
    rr = restrict(masks, K)
    return all(popcount(v) >= 2 for v in rr) and len(set(rr)) == len(rr)


def columns(masks, n):
    return [sum(((masks[r] >> c) & 1) << r for r in range(len(masks)))
            for c in range(n)]


def preconditions(masks, n):
    """The matrix hypotheses Lemma F needs.  A zero column is an input no
    target uses: Theorem N charges >= 1 gate for every column outside the
    keep-set, and that charge is Lemma 1 applied to a LIVE column, so a zero
    column would be charged for nothing.  Duplicate columns break Lemma F's
    fan-out argument outright."""
    cols = columns(masks, n)
    zero = [c for c in range(n) if cols[c] == 0]
    seen, dup = {}, []
    for c, v in enumerate(cols):
        if v == 0:
            continue
        if v in seen:
            dup.append((seen[v], c))
        else:
            seen[v] = c
    return zero, dup


def drop_columns(masks, n, drop):
    keep = [c for c in range(n) if c not in set(drop)]
    return [sum(((m >> c) & 1) << i for i, c in enumerate(keep)) for m in masks], len(keep)


class Searcher(object):
    """Thin wrapper around mine.c, with memoisation."""

    def __init__(self, path, max_depth):
        self.path = path
        self.max_depth = max_depth
        self.cache = {}
        self.nodes = 0
        self.seconds = 0.0

    def minE(self, k, targets):
        key = (k, tuple(sorted(targets)))
        if key in self.cache:
            return self.cache[key]
        arg = ','.join(str(t) for t in targets)
        for d in range(0, self.max_depth + 1):
            t0 = time.monotonic()
            p = subprocess.run([self.path, str(k), arg, str(d), '-p', '-o'],
                               capture_output=True, text=True)
            self.seconds += time.monotonic() - t0
            out = p.stdout.strip()
            for tok in out.split():
                if tok.startswith('nodes='):
                    self.nodes += int(tok[6:])
            if 'COMPLETION' in out:
                self.cache[key] = d
                return d
        self.cache[key] = None                     # exceeded the depth budget
        return None


def theorem_n_table(masks, n, S):
    """For every admissible keep-set K, its Theorem-N value."""
    T = len(masks)
    vals = {}
    for size in range(2, n + 1):
        for K in itertools.combinations(range(n), size):
            K = list(K)
            if not admissible(masks, K):
                continue
            e = S.minE(size, restrict(masks, K))
            if e is None:
                continue
            vals[tuple(K)] = (n - size) + T + e
    return vals


def best_covering_bound(vals, n, m):
    """max over families F covering every m-subset of  m + min_{K in F} value.

    Equivalently: the largest threshold v such that the keep-sets of value >= v
    still cover every m-subset, plus m."""
    if not vals:
        return None, None
    best = None
    bestfam = None
    for v in sorted(set(vals.values()), reverse=True):
        fam = [K for K, val in vals.items() if val >= v]
        if m == 0:
            covered = bool(fam)
        else:
            covered = all(any(not (set(A) & set(K)) for K in fam)
                          for A in itertools.combinations(range(n), m))
        if covered:
            best = m + v
            bestfam = fam
            break
    return best, bestfam


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mine', default=os.path.join(HERE, '..', 'gte56', 'mine'))
    ap.add_argument('--instance', default=None)
    ap.add_argument('--max-depth', type=int, default=12)
    args = ap.parse_args()

    if not os.path.exists(args.mine):
        raise SystemExit('searcher not found: %s\ncompile it with:\n'
                         '  cc -O2 -o ../gte56/mine ../gte56/mine.c' % args.mine)

    spec = json.load(open(os.path.join(HERE, 'known_optima.json')))
    insts = spec['instances']
    if args.instance:
        insts = [i for i in insts if i['name'] == args.instance]

    fails = []
    print('control: the bound machinery of ../gte56/ must never exceed a known optimum')
    print('searcher: %s' % os.path.relpath(os.path.normpath(args.mine)))
    print()

    def sweep(label, masks, n, opt, S, must_be_sound):
        """Run the whole Theorem-N table on one matrix and report."""
        T = len(masks)
        vals = theorem_n_table(masks, n, S)
        print('  [%s] admissible keep-sets : %d' % (label, len(vals)))
        print()
        print('    %-6s %-8s %-8s %-8s %s'
              % ('level', 'bound', 'optimum', 'slack', 'verdict'))
        worst = None
        for m in (0, 1, 2):
            b, _ = best_covering_bound(vals, n, m)
            if b is None:
                print('    m=%-4d %-8s %-8d %-8s no covering family' % (m, '-', opt, '-'))
                continue
            ok = b <= opt
            worst = b if worst is None else max(worst, b)
            print('    m=%-4d %-8d %-8d %-8d %s'
                  % (m, b, opt, opt - b, 'sound' if ok else 'OVERCLAIM'))
            if must_be_sound and not ok:
                fails.append('%s [%s]: m=%d bound %d > optimum %d'
                             % (inst['name'], label, m, b, opt))
        # the capped-keep-set regime: what the method gets when the exhaustion
        # can only afford small keep-sets, which is the MixColumns situation
        print()
        print('    %-14s %-8s %-8s %s'
              % ('|K| capped at', 'best m=1', 'optimum', 'verdict'))
        for cap in range(2, n + 1):
            sub = {K: v for K, v in vals.items() if len(K) <= cap}
            b, _ = best_covering_bound(sub, n, 1)
            if b is None:
                continue
            ok = b <= opt
            print('    %-14d %-8d %-8d %s' % (cap, b, opt, 'sound' if ok else 'OVERCLAIM'))
            if must_be_sound and not ok:
                fails.append('%s [%s]: |K|<=%d m=1 bound %d > optimum %d'
                             % (inst['name'], label, cap, b, opt))
        print()
        return worst

    for inst in insts:
        path = os.path.join(HERE, inst['matrix'])
        masks, n = load_matrix(path)
        T = len(masks)
        opt = inst['known_optimum']
        role = inst.get('role', 'positive')
        S = Searcher(args.mine, args.max_depth)

        print('-' * 74)
        print('instance %s   (%d targets over %d columns)   role: %s'
              % (inst['name'], T, n, role))
        print('  known optimum         : %d   [%s]' % (opt, inst['optimum_status']))
        print('  proved by             : %s' % inst['proof']['method'].split(';')[0])
        print('  ladder                : %s' % inst['proof']['ladder'])

        # ---- 2. AGREEMENT: the searcher's own exact answer (basis-independent,
        #        so it is meaningful even when Theorem N's preconditions fail)
        t0 = time.monotonic()
        e_full = S.minE(n, masks)
        dt = time.monotonic() - t0
        if e_full is None:
            print('  searcher exact answer : DEPTH BUDGET EXCEEDED')
            fails.append('%s: searcher did not close' % inst['name'])
            continue
        exact = T + e_full
        agree = (exact == opt)
        print('  searcher exact answer : %d targets + minE %d = %d   [%s]  (%.1f s)'
              % (T, e_full, exact, 'AGREES' if agree else 'DISAGREES', dt))
        if not agree:
            fails.append('%s: searcher %d vs SAT %d' % (inst['name'], exact, opt))

        # ---- 0. PRECONDITIONS
        zero, dup = preconditions(masks, n)
        clean = not zero and not dup
        print('  preconditions         : %s'
              % ('columns nonzero and pairwise distinct -- OK' if clean
                 else 'VIOLATED: zero columns %s, duplicate column pairs %s'
                      % (zero, dup)))
        print()

        if role == 'positive':
            if not clean:
                fails.append('%s: declared positive but violates the preconditions'
                             % inst['name'])
                continue
            sweep('as given', masks, n, opt, S, must_be_sound=True)

        elif role == 'precondition_negative_control':
            if clean:
                fails.append('%s: declared a precondition negative control but its '
                             'preconditions hold' % inst['name'])
                continue
            print('  This instance is in the suite to show that the precondition is')
            print('  LOAD-BEARING.  Applying Theorem N anyway, ignoring the gate:')
            print()
            worst = sweep('precondition IGNORED', masks, n, opt, S,
                          must_be_sound=False)
            exp = inst.get('expected_raw_overclaim')
            if worst is not None and worst > opt:
                print('  => it OVERCLAIMS: %d against a true optimum of %d.  That is'
                      % (worst, opt))
                print('     the documented behaviour, and it is why check_gte56.py')
                print('     checks A2 (columns nonzero) and A3 (columns distinct)')
                print('     before it reports anything.')
                if exp is not None and worst != exp:
                    fails.append('%s: expected overclaim %d, got %d'
                                 % (inst['name'], exp, worst))
            else:
                fails.append('%s: expected an overclaim without the precondition '
                             'gate, saw none' % inst['name'])
            print()
            masks2, n2 = drop_columns(masks, n, zero)
            print('  Now the same matrix with its %d zero column(s) dropped -- an'
                  % len(zero))
            print('  input no target uses cannot change the optimum, so the known')
            print('  optimum %d still applies, and now the machinery must be sound:'
                  % opt)
            print()
            z2, d2 = preconditions(masks2, n2)
            if z2 or d2:
                print('  [reduced] preconditions STILL violated: zero %s dup %s'
                      % (z2, d2))
                fails.append('%s: reduction did not clear the preconditions'
                             % inst['name'])
            else:
                sweep('reduced, %d columns' % n2, masks2, n2, opt, S,
                      must_be_sound=True)
        else:
            fails.append('%s: unknown role %r' % (inst['name'], role))

        print('  searcher work for this instance: %.3g nodes, %.1f s'
              % (S.nodes, S.seconds))
        print()

    print('=' * 74)
    if fails:
        print('RESULT: FAIL')
        for f in fails:
            print('  ' + f)
        return 1
    print('RESULT: PASS on %d instance(s).' % len(insts))
    print('  * The searcher independently reproduced every SAT-proved optimum'
          ' exactly.')
    print('  * No Theorem-N bound exceeded a known optimum on any instance whose')
    print('    preconditions hold, at any covering level or keep-set size.')
    print('  * The precondition negative control overclaimed exactly as documented')
    print('    when its gate was ignored, and became sound once reduced.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
