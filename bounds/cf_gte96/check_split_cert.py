#!/usr/bin/env python3
"""Checker for a SPLIT-PRICE certificate  L_cf(M) >= bound  over cancellation-free XOR-SLPs.

Python 3 standard library only. Exact integer arithmetic. No solver anywhere.

The certificate is a JSON file: {"denominator": D, "prices": [table_0, ..., table_31], "bound": b}.
Table t (one per row t of the matrix) maps keys "S:A" (hex) to non-negative integers:
S is a mask inside supp(t) with |S| >= 2, and {A, S^A} is a split of S into two non-empty
parts. Prices are n[t][(S,A)] = value / D. One constraint family:

    (C')  for every (S, A):   sum over targets t of  n[t][(S,A)]  <=  D .

Soundness (holds for EVERY cancellation-free circuit, minimum or not).
In a cancellation-free SLP the two operands of every gate have disjoint supports, so every
path count is 0 or 1, every value below a target t is a subset of supp(t), and the gates that
feed t form a full binary split hierarchy H_t of supp(t): t splits into its two operand masks,
each of those splits into its own two operand masks, down to single inputs. Every internal node
of H_t is an actual gate m, split exactly one way -- by its own parent pair s(m). Let G be the
gate set. Then

    |G| =  sum_{m in G} 1
        >= sum_{m in G} sum_t n[t][(m, s(m))] / D                       by (C')
        >= sum_t sum_{m in H_t} n[t][(m, s(m))] / D                     H_t is a subset of G
        >= sum_t min_H sum_{(S,A) in H} n[t][(S,A)] / D   =:  B ,

so L_cf(M) >= ceil(B). The minimum over hierarchies is a dynamic programme over the subsets
of supp(t): g[S] = min over splits (A, S^A) of n[t][(S,A)] + g[A] + g[S^A], g[singleton] = 0.
A split with no price entry costs 0 for that (S,A). Prices that do not depend on the split are
the mask-only certificates of ../cf_gte92; this family contains that one.

usage (from bounds/):  python3 cf_gte96/check_split_cert.py [--matrix ../matrix.txt]
                       [--cert cf_gte96/cert_cf96_split.json] [--aes-crosscheck] [--expect N]
"""
import argparse, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load_matrix(path):
    rows = [l.strip() for l in open(path) if l.strip()]
    if any(len(r) != len(rows) or set(r) - {'0', '1'} for r in rows):
        raise SystemExit('matrix file is not a square 0/1 matrix: %s' % path)
    return [sum(1 << c for c in range(len(r)) if r[c] == '1') for r in rows]


def aes_mixcolumns_rows():
    """FIPS-197 MixColumns over GF(2^8)/0x11B: output byte r = 2 a_r + 3 a_{r+1} + a_{r+2} + a_{r+3}.
    Row 8*ob + j is output bit j (bit 0 = least significant) of output byte ob; column 8*ib + jj is
    input bit jj of input byte ib."""
    def xt(x):
        x <<= 1
        return (x ^ 0x11B) & 0xFF if x & 0x100 else x
    def mul(c, x):
        return {1: x, 2: xt(x), 3: xt(x) ^ x}[c]
    coef = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
    rows = []
    for ob in range(4):
        for j in range(8):
            m = 0
            for ib in range(4):
                for jj in range(8):
                    if (mul(coef[ob][ib], 1 << jj) >> j) & 1:
                        m |= 1 << (8 * ib + jj)
            rows.append(m)
    return rows


def parse_tables(cert, targets):
    """Returns (tables, n_priced, bad): tables[t] maps normalised (S, A) -> int price."""
    tables, n_priced, bad = [], 0, 0
    for ti, table in enumerate(cert['prices']):
        t = targets[ti] if ti < len(targets) else 0
        pp = {}
        for k, v in table.items():
            try:
                s_hex, a_hex = k.split(':')
                S, A = int(s_hex, 16), int(a_hex, 16)
                ok = (type(v) is int and v >= 0)
            except (ValueError, AttributeError):
                S, A, ok = 0, 0, False
            low = S & -S
            if ok and S and A and A != S and not (A & ~S) and not (S & ~t) and bin(S).count('1') >= 2:
                if not (A & low):
                    A = S ^ A                       # the other spelling of the same split
                if (S, A) in pp:
                    ok = False                      # the same split priced twice in one table
            else:
                ok = False
            if not ok:
                bad += 1
                continue
            pp[(S, A)] = v
            n_priced += 1
        tables.append(pp)
    return tables, n_priced, bad


def cheapest_hierarchy(t, prices):
    """min over full binary split hierarchies of supp(t) of the summed prices (integers)."""
    g = {}
    subs = []
    s = t
    while s:
        subs.append(s)
        s = (s - 1) & t
    subs.sort(key=lambda x: bin(x).count('1'))
    for S in subs:
        if bin(S).count('1') < 2:
            g[S] = 0
            continue
        low = S & -S
        rest = S ^ low
        best = None
        sub = rest
        while True:
            A = low | sub
            B = S ^ A
            if B:
                v = prices.get((S, A), 0) + g[A] + g[B]
                if best is None or v < best:
                    best = v
            if sub == 0:
                break
            sub = (sub - 1) & rest
        g[S] = best
    return g[t]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--matrix', default=os.path.join(HERE, '..', 'matrix.txt'))
    ap.add_argument('--cert', default=os.path.join(HERE, 'cert_cf96_split.json'))
    ap.add_argument('--aes-crosscheck', action='store_true',
                    help='also rebuild AES MixColumns from GF(2^8) and compare it row for row with --matrix')
    ap.add_argument('--expect', type=int, default=None,
                    help='required value of ceil(B); defaults to the certificate\'s own "bound" field')
    a = ap.parse_args()

    T = load_matrix(a.matrix)
    raw = open(a.matrix, 'rb').read()
    cert = json.load(open(a.cert))
    D = cert['denominator']
    if type(D) is not int or D <= 0:
        raise SystemExit('bad denominator')
    print('matrix       : %s' % os.path.relpath(a.matrix))
    print('  sha256     : %s' % hashlib.sha256(raw).hexdigest())
    print('  shape      : %d rows x %d columns, total row weight %d' % (len(T), len(T), sum(bin(t).count('1') for t in T)))
    print('certificate  : %s' % os.path.relpath(a.cert))
    print('  denominator: %d, %d price tables' % (D, len(cert['prices'])))
    print()
    ok = True

    def report(name, passed, what, text):
        nonlocal ok
        ok = ok and passed
        print('  [%s] CHECK %s  %-46s %s' % ('PASS' if passed else 'FAIL', name, what, text))

    if a.aes_crosscheck:
        aes = aes_mixcolumns_rows()
        report('A', aes == T, 'matrix is AES MixColumns (GF(2^8) rebuild)',
               'row-for-row identical' if aes == T else 'DIFFERS from the GF(2^8) rebuild')
    report('T', len(cert['prices']) == len(T), 'one price table per target',
           '%d tables, %d targets' % (len(cert['prices']), len(T)))
    if len(cert['prices']) != len(T):
        print('\nRESULT: certificate INVALID.'); return 1

    tables, n_priced, bad = parse_tables(cert, T)
    report('0', bad == 0, 'keys well formed, prices non-negative integers',
           '%d priced (target,mask,split) triples, %d bad' % (n_priced, bad))

    col = {}
    for pp in tables:
        for key, v in pp.items():
            col[key] = col.get(key, 0) + v
    mx = max(col.values()) if col else 0
    report('1', mx <= D, 'column constraint  sum_t n[t][(S,A)] <= D',
           'max column sum = %d / %d = %.7f  over %d distinct (mask,split) columns' % (mx, D, mx / D, len(col)))

    num = sum(cheapest_hierarchy(t, tables[ti]) for ti, t in enumerate(T))
    lb = -(-num // D)
    report('2', True, 'hierarchy DPs evaluated', 'numerator = %d,  B = %d/%d = %.7f' % (num, num, D, num / D))

    expect = a.expect if a.expect is not None else cert.get('bound')
    if expect is None:
        report('3', True, 'stated bound', 'none stated; computed ceil(B) = %d' % lb)
    else:
        report('3', lb == expect, 'computed bound matches the stated bound',
               'computed ceil(B) = %d, %s states %d' % (lb, 'certificate' if a.expect is None else '--expect', expect))

    print()
    print('=' * 74)
    if ok:
        print('RESULT: certificate VALID.')
        print('  B = %d/%d = %.7f' % (num, D, num / D))
        print('  => L_cf(M) >= %d' % lb)
        print('  => every cancellation-free XOR-SLP for this matrix has >= %d gates;' % lb)
        print('     equivalently, every SLP with <= %d gates contains a cancelling gate.' % (lb - 1))
        return 0
    print('RESULT: certificate INVALID (see the FAIL lines above).')
    return 1


if __name__ == '__main__':
    sys.exit(main())
