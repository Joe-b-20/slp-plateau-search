#!/usr/bin/env python3
"""Checker for the laminar price certificate  L_cf(M) >= 92.

L_cf(M) is the minimum size of a CANCELLATION-FREE XOR-SLP for M: one in which
every gate's two operand masks have disjoint support (equivalently, no gate
ever cancels a bit that an earlier gate produced).

The certificate is a price table n[t][m] >= 0 over a common denominator D, one
price per (target t, mask m inside supp(t)), subject to the single constraint

        for every mask m :      sum_t n[t][m]  <=  D .                    (C)

Soundness, three lines and no solver, and NO optimality of the table needed
(see STATEMENT.md for the hierarchy lemma).  Let G be the gate set of any
cancellation-free SLP for M.  Each target t owns a laminar hierarchy H_t of
subsets of supp(t) whose internal masks all lie in G.  Then

    |G|  =  sum_{m in G} 1
         >= sum_{m in G} sum_t n[t][m] / D                            by (C)
         >= sum_t sum_{m in H_t} n[t][m] / D                          H_t subset G
         >= sum_t min_H sum_{m in H} n[t][m] / D   =:  B .

So B is a valid lower bound for ANY table satisfying (C), and L_cf(M) >= ceil(B).

Checking a certificate is therefore:
    CHECK 0   every priced mask lies inside its target's support
    CHECK 1   the column constraint (C), one sum per mask
    CHECK 2   32 independent subset DPs, each over 2^w(t) <= 2^7 = 128 states

All in exact integer arithmetic.  Python 3 standard library only, solver-free.

Usage:
    python3 check_cf_cert.py [--matrix PATH] [--cert PATH] [--aes-crosscheck]
Exit 0 iff the certificate is valid and clears the stated bound.
"""

import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def show(path):
    """Print paths relative to the caller's directory, so transcripts are
    reproducible across machines."""
    try:
        return os.path.relpath(os.path.normpath(path))
    except ValueError:
        return path


def load_matrix(path):
    rows = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if any(ch not in '01' for ch in line):
                raise SystemExit('%s: row %r is not a 0/1 string' % (path, line))
            rows.append(line)
    n = len(rows[0])
    if any(len(r) != n for r in rows):
        raise SystemExit('%s: rows have unequal length' % path)
    return [sum(1 << c for c in range(n) if row[c] == '1') for row in rows], n


def aes_mixcolumns_masks():
    """Rebuild the MixColumns bit matrix from GF(2^8)/0x11B, from the spec, so
    that a reader can confirm matrix.txt is the map they think it is."""
    def xt(b):
        b <<= 1
        return b ^ 0x11B if b & 0x100 else b
    out = []
    for orow in range(4):
        for obit in range(8):
            m = 0
            for icol in range(4):
                coef = [2, 3, 1, 1][(icol - orow) % 4]
                for ibit in range(8):
                    v = 1 << ibit
                    p = 0
                    if coef & 1:
                        p ^= v
                    if coef & 2:
                        p ^= xt(v)
                    if (p >> obit) & 1:
                        m |= 1 << (icol * 8 + ibit)
            out.append(m)
    return out


def hierarchy_dp(target, prices):
    """min over full laminar hierarchies of supp(target) of the summed prices of
    the internal (size >= 2) nodes.  Integer numerators over the common D."""
    bits = [1 << i for i in range(target.bit_length()) if (target >> i) & 1]
    n = len(bits)
    g = [0] * (1 << n)
    for S in range(1, 1 << n):
        if bin(S).count('1') < 2:
            continue
        mm = 0
        for i in range(n):
            if (S >> i) & 1:
                mm |= bits[i]
        low = S & -S
        rest = S ^ low
        best = None
        sub = rest
        while True:
            S1 = low | sub
            S2 = S ^ S1
            if S2:
                v = g[S1] + g[S2]
                if best is None or v < best:
                    best = v
            if sub == 0:
                break
            sub = (sub - 1) & rest
        g[S] = prices.get(mm, 0) + best
    return g[(1 << n) - 1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--matrix', default=os.path.join(HERE, '..', 'matrix.txt'))
    ap.add_argument('--cert', default=os.path.join(HERE, 'cert_cf92.json'))
    ap.add_argument('--aes-crosscheck', action='store_true',
                    help='also rebuild AES MixColumns from GF(2^8) and confirm '
                         'the supplied matrix is it (row order included)')
    args = ap.parse_args()

    targets, n = load_matrix(args.matrix)
    digest = hashlib.sha256(open(args.matrix, 'rb').read()).hexdigest()
    cert = json.load(open(args.cert))
    D = cert['denominator']
    raw = cert['prices'] if 'prices' in cert else cert['p']
    P = [{int(k, 16): int(v) for k, v in d.items()} for d in raw]

    print('matrix       : %s' % show(args.matrix))
    print('  sha256     : %s' % digest)
    print('  shape      : %d rows x %d columns, total row weight %d'
          % (len(targets), n, sum(bin(t).count('1') for t in targets)))
    print('certificate  : %s' % show(args.cert))
    print('  denominator: %d, %d price tables' % (D, len(P)))
    print()

    fails = []

    def check(tag, ok, detail):
        print('  [%s] %-50s %s' % ('PASS' if ok else 'FAIL', tag, detail))
        if not ok:
            fails.append(tag)

    if args.aes_crosscheck:
        ref = aes_mixcolumns_masks()
        check('CHECK A  matrix is AES MixColumns (GF(2^8) rebuild)',
              ref == targets,
              'row-for-row identical' if ref == targets else
              ('SAME SET, DIFFERENT ORDER' if sorted(ref) == sorted(targets)
               else 'DIFFERENT MATRIX'))

    check('CHECK T  one price table per target', len(P) == len(targets),
          '%d tables, %d targets' % (len(P), len(targets)))
    if len(P) != len(targets):
        print('\nRESULT: FAIL')
        return 1

    bad = []
    for ti, t in enumerate(targets):
        for m, v in P[ti].items():
            if v < 0:
                bad.append((ti, m, 'negative price'))
            if m & ~t:
                bad.append((ti, m, 'mask not inside supp(target)'))
            if bin(m).count('1') < 2:
                bad.append((ti, m, 'mask of weight < 2'))
    check('CHECK 0  prices non-negative, inside their target support',
          not bad, '%d priced (target,mask) pairs, %d bad'
          % (sum(len(d) for d in P), len(bad)))
    if bad:
        for b in bad[:5]:
            print('        target %d mask 0x%x: %s' % b)

    tot = {}
    for d in P:
        for m, v in d.items():
            tot[m] = tot.get(m, 0) + v
    mx = max(tot.values()) if tot else 0
    check('CHECK 1  column constraint  sum_t n[t][m] <= D',
          mx <= D, 'max column sum = %d / %d = %.7f  over %d distinct masks'
          % (mx, D, mx / D, len(tot)))

    num = 0
    for ti, t in enumerate(targets):
        num += hierarchy_dp(t, P[ti])
    B = num / D
    lb = -(-num // D)                                   # ceil
    check('CHECK 2  hierarchy DPs evaluated', True,
          'numerator = %d,  B = %d/%d = %.7f' % (num, num, D, B))

    stated = cert.get('bound')
    if stated is not None:
        check('CHECK 3  computed bound matches the stated bound', lb == stated,
              'computed ceil(B) = %d, certificate states %d' % (lb, stated))

    print()
    print('=' * 74)
    if fails:
        print('RESULT: FAIL -- %s' % ', '.join(fails))
        return 1
    print('RESULT: certificate VALID.')
    print('  B = %d/%d = %.7f' % (num, D, B))
    print('  => L_cf(M) >= %d' % lb)
    print('  => every cancellation-free XOR-SLP for this matrix has >= %d gates;'
          % lb)
    print('     equivalently, every SLP with <= %d gates contains a cancelling gate.'
          % (lb - 1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
