#!/usr/bin/env python3
"""Checker for the adaptive-gate-elimination lower bound  L(M) >= 56.

Reads a 0/1 matrix (matrix.txt, one row per line, one character per column)
and a certificate (cert56.json) and verifies every hypothesis of Theorem N
that is checkable in closed form.  Python 3 standard library only.

WHAT THIS SCRIPT PROVES BY ITSELF
---------------------------------
Theorem N (see STATEMENT.md) gives, for a family F of keep-sets covering every
m-subset of the columns,

        L(M) >= m + min_{K in F} [ (n - |K|) + (#targets) + e_K ] ,

where e_K is a lower bound on minE(K) -- the minimum number of extra masks
needed on top of the restricted target set M|_K.  Everything in that formula
except e_K is a finite structural check, and this script performs all of it:

    A  matrix well-formed; columns nonzero and pairwise distinct; rows weight>=2
    B  the certificate's permutation sigma is an automorphism of the matrix
    C  every sigma-conjugate of K is Theorem-N admissible
       (restricted rows pairwise distinct, each of weight >= 2)
    D  the level-m covering hypothesis holds
    E  the necessary screen  e_K <= jam(K)  (minE is never above the free-closure
       jam, so a certificate claiming e_K > jam(K) would be self-refuting)
    F  the arithmetic of the bound
    G  positive control: the recorded 4-extra witness for the FAILING keep-set
       cert1 really does complete it, so the realizability predicate used here
       is the same one the exhaustive searcher used

WHAT THIS SCRIPT DOES NOT PROVE BY ITSELF
-----------------------------------------
    e_K = 5.  That is the output of a depth-4 exhaustion (two independent
    implementations, 9.43e10 and 4.75e9 nodes) and is NOT a short certificate.
    Its provenance is recorded in cert56.json and printed below.
    Pass --minE-depth D to re-run the exhaustion here with the shipped searcher:
      --minE-depth 3   certifies minE >= 4, hence L(M) >= 55   (~1 s, one core)
      --minE-depth 4   certifies minE >= 5, hence L(M) >= 56   (~3 min, one core)
    Both use mine.c's two documented prunings.  The independent UNPRUNED
    depth-4 exhaustion (9.43e10 nodes) is cited, not re-run.

Usage:
    python3 check_gte56.py [--matrix PATH] [--cert PATH]
                           [--minE-depth D] [--mine PATH]
Exit 0 iff every checkable hypothesis holds.
"""

import argparse
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def show(path):
    """Print paths relative to the caller's directory, so transcripts are
    reproducible across machines."""
    try:
        return os.path.relpath(os.path.normpath(path))
    except ValueError:
        return path


# ---------------------------------------------------------------- matrix I/O

def load_matrix(path):
    """matrix.txt -> list of row masks.  Row r's mask has bit c set iff M[r][c]=1."""
    rows = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if any(ch not in '01' for ch in line):
                raise SystemExit('matrix %s: row %r is not a 0/1 string' % (path, line))
            rows.append(line)
    n = len(rows[0])
    if any(len(r) != n for r in rows):
        raise SystemExit('matrix %s: rows have unequal length' % path)
    masks = [sum(1 << c for c in range(n) if row[c] == '1') for row in rows]
    return masks, n


def popcount(x):
    return bin(x).count('1')


def columns(masks, n):
    return [sum(((masks[r] >> c) & 1) << r for r in range(len(masks))) for c in range(n)]


def restrict(masks, K):
    """Rows of M restricted to the columns in K, re-indexed 0..|K|-1."""
    out = []
    for m in masks:
        v = 0
        for i, c in enumerate(K):
            if (m >> c) & 1:
                v |= 1 << i
        out.append(v)
    return out


def admissible(masks, K):
    """Theorem-N admissibility of a keep-set."""
    rr = restrict(masks, K)
    if any(popcount(v) < 2 for v in rr):
        return False, 'a restricted row has weight < 2'
    if len(set(rr)) != len(rr):
        return False, 'restricted rows are not pairwise distinct'
    return True, 'ok'


def conjugates(K, perm, order):
    out = [sorted(K)]
    for _ in range(order - 1):
        out.append(sorted(perm[c] for c in out[-1]))
    return out


def free_closure(targets, k):
    """Masks derivable with NO extras: start from the k unit masks, repeatedly
    commit any target that is the XOR of two already-available masks."""
    avail = set(1 << i for i in range(k))
    todo = set(targets) - avail
    while True:
        add = [t for t in todo if any((t ^ a) in avail for a in avail)]
        if not add:
            break
        for t in add:
            avail.add(t)
            todo.discard(t)
    return avail, todo


def realizable_with(targets, k, extras):
    """Fixpoint realizability check: can the target set be completed using
    exactly the given extra masks?  (Independent of any search order.)"""
    avail = set(1 << i for i in range(k))
    pend_t = set(targets) - avail
    pend_e = set(extras)
    while True:
        progress = False
        for pending in (pend_t, pend_e):
            for m in list(pending):
                if any((m ^ a) in avail for a in avail):
                    avail.add(m)
                    pending.discard(m)
                    progress = True
        if not progress:
            break
    return (not pend_t) and (not pend_e), len(pend_t)


# ---------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--matrix', default=os.path.join(HERE, '..', 'matrix.txt'))
    ap.add_argument('--cert', default=os.path.join(HERE, 'cert56.json'))
    ap.add_argument('--minE-depth', type=int, default=None,
                    help='re-run the extras exhaustion at this depth with mine.c '
                         '(D certifies minE >= D+1); 3 is seconds, 4 is the '
                         'published multi-core run')
    ap.add_argument('--mine', default=os.path.join(HERE, 'mine'),
                    help='path to the compiled searcher (cc -O2 -o mine mine.c)')
    args = ap.parse_args()

    cert = json.load(open(args.cert))
    masks, n = load_matrix(args.matrix)
    args.matrix = show(args.matrix)
    args.cert_shown = show(args.cert)
    K = cert['keep_set']
    m = cert['m']
    e_K = cert['e_K']
    perm = cert['symmetry']['perm']
    order = cert['symmetry']['order']

    print('matrix        : %s  (%d rows x %d columns)' % (args.matrix, len(masks), n))
    print('certificate   : %s  (%s)' % (args.cert_shown, cert['name']))
    print('technique     : %s' % cert['technique'])
    print()

    fails = []

    def check(tag, ok, detail):
        print('  [%s] %-58s %s' % ('PASS' if ok else 'FAIL', tag, detail))
        if not ok:
            fails.append(tag)

    # ---- A  matrix hypotheses (Lemma 1 / Lemma F preconditions)
    print('A. matrix hypotheses')
    cols = columns(masks, n)
    check('A1 square', len(masks) == n, '%d rows, %d columns' % (len(masks), n))
    check('A2 columns nonzero', all(c != 0 for c in cols),
          '%d/%d nonzero' % (sum(1 for c in cols if c), n))
    check('A3 columns pairwise distinct', len(set(cols)) == n,
          '%d distinct' % len(set(cols)))
    check('A4 every row has weight >= 2', all(popcount(r) >= 2 for r in masks),
          'min row weight = %d' % min(popcount(r) for r in masks))
    check('A5 rows pairwise distinct', len(set(masks)) == len(masks),
          '%d distinct targets' % len(set(masks)))
    print()

    # ---- B  the symmetry is a real automorphism of THIS matrix
    print('B. the certificate symmetry is an automorphism of the matrix')
    ok_perm = sorted(perm) == list(range(n))
    check('B1 sigma is a permutation of the columns', ok_perm, '')
    if ok_perm:
        Mset = set()
        for r in range(len(masks)):
            for c in range(n):
                if (masks[r] >> c) & 1:
                    Mset.add((r, c))
        ok_auto = all(((perm[r], perm[c]) in Mset) == ((r, c) in Mset)
                      for r in range(len(masks)) for c in range(n))
        check('B2 M[sigma(r)][sigma(c)] == M[r][c] for all r,c', ok_auto,
              'checked all %d entries' % (len(masks) * n))
        p = list(range(n))
        for _ in range(order):
            p = [perm[i] for i in p]
        check('B3 sigma has order %d' % order, p == list(range(n)), '')
    print()

    # ---- C  admissibility of every conjugate
    print('C. Theorem-N admissibility of K and all its sigma-conjugates')
    CJ = conjugates(K, perm, order)
    for j, Kj in enumerate(CJ):
        ok, why = admissible(masks, Kj)
        check('C%d |K|=%d admissible' % (j + 1, len(Kj)), ok and len(Kj) == len(K),
              '%s  K=%s' % (why, Kj))
    print()

    # ---- D  the level-m covering hypothesis
    print('D. level-m covering hypothesis (m = %d)' % m)
    # Complement D_Kj = [n] \ Kj.  Level-m covering: every m-subset of [n] is
    # contained in some D_Kj.  For m = 1 that is: every column lies outside some
    # conjugate, i.e. the intersection of the conjugates is empty.
    if m == 1:
        inter = set(range(n))
        for Kj in CJ:
            inter &= set(Kj)
        check('D1 every column is avoided by some conjugate', not inter,
              'intersection of the %d conjugates = %s' % (len(CJ), sorted(inter) or '{}'))
    else:
        import itertools
        bad = [A for A in itertools.combinations(range(n), m)
               if not any(not (set(A) & set(Kj)) for Kj in CJ)]
        check('D1 every %d-subset avoided by some conjugate' % m, not bad,
              '%d uncovered subsets' % len(bad))
    print()

    # ---- E  the free-closure screen on e_K
    print('E. necessary screen on the claimed e_K')
    tgt = restrict(masks, K)
    avail0, todo = free_closure(tgt, len(K))
    jam = len(todo)
    check('E1 e_K <= jam(K)  (a jam of t rows is always completable with t extras)',
          e_K <= jam, 'e_K = %d, jam(K) = %d, free closure %d/%d, |avail| = %d'
          % (e_K, jam, len(tgt) - jam, len(tgt), len(avail0)))
    print()

    # ---- F  arithmetic
    print('F. the bound arithmetic')
    terms = cert['bound_terms']
    total = m + (n - len(K)) + len(masks) + e_K
    check('F1 m + (n-|K|) + #targets + e_K == stated bound',
          total == cert['bound'],
          '%d + %d + %d + %d = %d' % (m, n - len(K), len(masks), e_K, total))
    check('F2 stated terms match the matrix and certificate',
          terms['m'] == m and terms['n_minus_K'] == n - len(K)
          and terms['n_targets'] == len(masks) and terms['e_K'] == e_K, '')
    print()

    # ---- G  positive control on the realizability predicate
    print('G. control: the recorded 4-extra witness for the FAILING keep-set')
    nc = cert['negative_control']
    tgt1 = restrict(masks, nc['keep_set'])
    ok_w, undone = realizable_with(tgt1, len(nc['keep_set']), nc['witness_extras'])
    check('G1 witness completes %s with %d extras' % (nc['name'], len(nc['witness_extras'])),
          ok_w, 'extras %s, undone targets = %d  => minE(%s) <= %d'
          % (nc['witness_extras_hex'], undone, nc['name'], len(nc['witness_extras'])))
    ok_none, undone0 = realizable_with(tgt1, len(nc['keep_set']), [])
    check('G2 the same keep-set is NOT completable with 0 extras', not ok_none,
          'undone targets with no extras = %d' % undone0)
    print()

    # ---- H  optional: re-run the exhaustion
    print('H. e_K: the one term that is not a closed-form check')
    prov = cert['e_K_provenance']
    print('     status : %s' % prov['status'])
    print('     claim  : %s' % prov['statement'])
    print('     method : %s' % prov['method'])
    for run in prov['runs']:
        print('     run    : %-56s %s, %s branches, %s shards, %.3g nodes'
              % (run['implementation'], run['result'], run['root_branches'],
                 run['shards'], run['nodes']))
    if args.minE_depth is not None:
        if not os.path.exists(args.mine):
            check('H1 searcher present', False,
                  'compile it first:  cc -O2 -o %s %s'
                  % (args.mine, os.path.join(HERE, 'mine.c')))
        else:
            d = args.minE_depth
            print('     re-running the exhaustion at depth %d ...' % d)
            t0 = time.monotonic()
            cmd = [args.mine, str(len(K)), ','.join(str(x) for x in tgt), str(d), '-p', '-o']
            proc = subprocess.run(cmd, capture_output=True, text=True)
            dt = time.monotonic() - t0
            out = proc.stdout.strip()
            print('     %s   (%.1f s)' % (out, dt))
            check('H1 depth-%d exhaustion finds no completion => minE >= %d' % (d, d + 1),
                  'result=NONE' in out,
                  're-derived bound with e_K = %d is %d'
                  % (d + 1, m + (n - len(K)) + len(masks) + d + 1))
    else:
        print('     (not re-run; pass --minE-depth 3 for the seconds-long '
              'depth-3 re-derivation of minE >= 4)')
    print()

    print('=' * 74)
    if fails:
        print('RESULT: FAIL -- %d check(s) failed: %s' % (len(fails), ', '.join(fails)))
        return 1
    print('RESULT: every closed-form hypothesis of Theorem N holds for this matrix.')
    print('  Self-contained here            :  L(M) >= %d + %d + %d + e_K'
          % (m, n - len(K), len(masks)))
    print('  With e_K = %d (cited exhaustion) :  L(M) >= %d'
          % (e_K, cert['bound']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
