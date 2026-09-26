#!/usr/bin/env python3
"""Referee's independent checker for a split-price certificate  L_cf(M) >= claim.

Written from the statement only (no code shared with the lane).  Python 3 stdlib,
exact integer / Fraction arithmetic throughout.

Object checked.  Integer prices n[t][(S,{A,S\\A})] >= 0 over a denominator D, one per
(row t of the matrix, mask S inside supp(t) with |S| >= 2, unordered split {A, S\\A}
of S into two non-empty parts), subject to

    (C')  for every (S, {A, S\\A}):   sum over rows t of n[t][(S,{A,S\\A})]  <=  D.

Bound.  B = (1/D) * sum_t min_H sum_{(S,split) in H} n[t][(S,split)], H ranging over
all full binary split hierarchies of supp(t) (root supp(t), every node of size >= 2
split into two non-empty disjoint children, leaves = the singletons, which cost 0).
Every cancellation-free circuit for the matrix has >= B gates (argument in REFEREE.md,
item 2), so L_cf >= ceil(B).

What is recomputed here (nothing is read from the certificate except D and the prices):
  K  key syntax: "S:A" hex; S, A parsed strictly (hex digits only, no 0x/_/space);
     duplicate JSON keys inside one table are detected (not silently overwritten);
     two spellings of one (S, split) inside one table are detected.
  P  every price is a JSON integer (not bool/float/string) and >= 0.
  S  every key is well formed: S inside supp(t), |S| >= 2, A a non-empty proper
     subset of S.  Orientation: an unordered split has two spellings; a key whose A
     does NOT contain the lowest bit of S is normalised to (S, S^A) and counted.
  C  (C') over the normalised keys, summed over ALL rows (keys shared by several rows
     are summed together), exact integers.
  D1 per row: DP over the subsets of supp(t) in local coordinates, enumerating EVERY
     non-empty proper submask a of s (both spellings of each split; splits with no
     price cost 0), price looked up by the normalised global key.
  D2 per row: the minimum by brute force over ALL full binary hierarchies of supp(t)
     ((2w-3)!! of them: 105 for w=5, 10395 for w=7), no DP at all; must equal D1.
  W  an argmin hierarchy is extracted, re-validated as a full binary hierarchy of
     supp(t) and re-priced; its price must equal D1.
  B  numerator = sum_t D1(t); B = numerator/D; ceil(B) by integer arithmetic.

usage:
  check96_independent.py --matrix PATH --cert PATH [--claim 96] [--aes-crosscheck]
                         [--no-bruteforce] [--quiet]
exit 0 iff every check passes and ceil(B) >= claim.
"""
import argparse
import json
import re
import sys
from fractions import Fraction

HEX = re.compile(r'^[0-9a-fA-F]+$')


def popcount(x):
    return bin(x).count('1')


# ---------------------------------------------------------------- matrix
def parse_matrix(path):
    rows = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if set(line) - {'0', '1'}:
                raise SystemExit('matrix row %r is not a 0/1 string' % line)
            rows.append(line)
    if not rows or len({len(r) for r in rows}) != 1:
        raise SystemExit('matrix rows missing or of unequal length')
    # convention: string position c  <->  input bit c
    return [sum(1 << c for c, ch in enumerate(r) if ch == '1') for r in rows], len(rows[0])


def aes_mixcolumns_rows():
    """FIPS-197 MixColumns as 32 row masks; bit 8*j+b = bit b of input byte j."""
    def gmul(a, b):
        p = 0
        for i in range(8):
            if (b >> i) & 1:
                p ^= a << i
        for d in range(15, 7, -1):
            if (p >> d) & 1:
                p ^= 0x11B << (d - 8)
        return p
    out = []
    for r in range(4):
        for ob in range(8):
            m = 0
            for j in range(4):
                c = (2, 3, 1, 1)[(j - r) % 4]
                for ib in range(8):
                    if (gmul(c, 1 << ib) >> ob) & 1:
                        m |= 1 << (8 * j + ib)
            out.append(m)
    return out


# ---------------------------------------------------------------- keys
def canon(S, A):
    """Normalised spelling of the unordered split {A, S^A}: the part holding lowbit(S)."""
    return (S, A) if A & S & -S else (S, S ^ A)


def _pairs_hook(pairs):
    seen = {}
    dups = []
    for k, v in pairs:
        if k in seen:
            dups.append(k)
        seen[k] = v
    if dups:
        seen['__duplicate_json_keys__'] = dups
    return seen


def load_certificate(path, targets, report):
    raw = json.load(open(path), object_pairs_hook=_pairs_hook)
    ok = True
    if '__duplicate_json_keys__' in raw:
        report('FAIL', 'K', 'duplicate top-level JSON keys %r' % raw['__duplicate_json_keys__'])
        ok = False
    D = raw.get('denominator')
    if type(D) is not int or D <= 0:
        report('FAIL', 'P', 'denominator %r is not a positive JSON integer' % (D,))
        return None, None, False, {}
    tabs = raw.get('prices')
    if not isinstance(tabs, list) or len(tabs) != len(targets):
        report('FAIL', 'T', 'prices must be a list of %d tables, got %r' % (
            len(targets), type(tabs).__name__ if not isinstance(tabs, list) else len(tabs)))
        return None, None, False, {}
    tables = []
    stats = dict(entries=0, zero=0, reversed=0, merged=0, bad_syntax=0, bad_value=0,
                 bad_key=0, dup_json=0)
    for ti, (t, tab) in enumerate(zip(targets, tabs)):
        if not isinstance(tab, dict):
            report('FAIL', 'T', 'table %d is not an object' % ti)
            ok = False
            tables.append({})
            continue
        if '__duplicate_json_keys__' in tab:
            stats['dup_json'] += len(tab['__duplicate_json_keys__'])
            ok = False
            report('FAIL', 'K', 'table %d has duplicate JSON keys %r' % (ti, tab['__duplicate_json_keys__'][:3]))
            tab = {k: v for k, v in tab.items() if k != '__duplicate_json_keys__'}
        norm = {}
        for k, v in tab.items():
            stats['entries'] += 1
            parts = k.split(':')
            if len(parts) != 2 or not all(HEX.match(p) for p in parts):
                stats['bad_syntax'] += 1
                ok = False
                report('FAIL', 'K', 'table %d key %r is not "hex:hex"' % (ti, k))
                continue
            S, A = int(parts[0], 16), int(parts[1], 16)
            if type(v) is not int or v < 0:          # bool is not int here: type() check
                stats['bad_value'] += 1
                ok = False
                report('FAIL', 'P', 'table %d key %s price %r not a non-negative integer' % (ti, k, v))
                continue
            if v == 0:
                stats['zero'] += 1
            if (S & ~t) or popcount(S) < 2 or A == 0 or (A & ~S) or A == S:
                stats['bad_key'] += 1
                ok = False
                report('FAIL', 'S', 'table %d key %s malformed for target %x' % (ti, k, t))
                continue
            key = canon(S, A)
            if key != (S, A):
                stats['reversed'] += 1
            if key in norm:
                stats['merged'] += 1          # two spellings of one split in one table
                norm[key] += v
            else:
                norm[key] = v
        tables.append(norm)
    return D, tables, ok, stats


# ---------------------------------------------------------------- DP (D1)
def dp_min(t, table, want_witness=False):
    bits = [i for i in range(t.bit_length()) if (t >> i) & 1]
    w = len(bits)
    full = (1 << w) - 1
    glob = [0] * (1 << w)
    for s in range(1, 1 << w):
        low = s & -s
        glob[s] = glob[s ^ low] | (1 << bits[low.bit_length() - 1])
    g = [0] * (1 << w)
    arg = [0] * (1 << w)
    for s in sorted(range(1, 1 << w), key=popcount):
        if popcount(s) < 2:
            continue
        best = None
        a = (s - 1) & s
        while a:                          # every non-empty proper submask: both spellings
            b = s ^ a
            v = table.get(canon(glob[s], glob[a]), 0) + g[a] + g[b]
            if best is None or v < best:
                best, arg[s] = v, a
            a = (a - 1) & s
        g[s] = best
    if not want_witness:
        return g[full], None
    wit = []
    stack = [full]
    while stack:
        s = stack.pop()
        if popcount(s) < 2:
            continue
        a = arg[s]
        wit.append((glob[s], glob[a]))
        stack += [a, s ^ a]
    return g[full], wit


# ---------------------------------------------------------------- brute force (D2)
def _submasks_proper(x):
    s = (x - 1) & x
    while s:
        yield s
        s = (s - 1) & x


def all_hierarchies(S, memo):
    """All full binary hierarchies of S, each a tuple of (node, one part) pairs."""
    if S in memo:
        return memo[S]
    if popcount(S) == 1:
        res = [()]
    else:
        res = []
        low = S & -S
        rest = S ^ low
        parts = [low | sub for sub in _submasks_proper(rest)] + [low]   # A holds lowbit, A != S
        for A in parts:
            B = S ^ A
            for h1 in all_hierarchies(A, memo):
                for h2 in all_hierarchies(B, memo):
                    res.append(((S, A),) + h1 + h2)
    memo[S] = res
    return res


def double_factorial_odd(k):
    r = 1
    while k > 1:
        r *= k
        k -= 2
    return r


def brute_min(t, table, memo):
    H = all_hierarchies(t, memo)
    w = popcount(t)
    expect = double_factorial_odd(2 * w - 3) if w >= 2 else 1
    assert len(H) == expect, (len(H), expect)
    assert len(set(frozenset(h) for h in H)) == len(H)
    return min(sum(table.get(canon(S, A), 0) for S, A in h) for h in H), len(H)


def validate_hierarchy(t, wit):
    """wit: list of (S, A).  Full binary hierarchy of supp(t)?"""
    nodes = {S for S, _ in wit}
    if len(nodes) != len(wit) or t not in nodes:
        return False
    if len(wit) != popcount(t) - 1:
        return False
    children = []
    for S, A in wit:
        B = S ^ A
        if A == 0 or B == 0 or (A & ~S):
            return False
        for X in (A, B):
            if popcount(X) >= 2 and X not in nodes:
                return False
            children.append(X)
    # every node except the root is the child of exactly one node; leaves are all singletons of t
    ch_nodes = [X for X in children if popcount(X) >= 2]
    leaves = [X for X in children if popcount(X) == 1]
    return (sorted(ch_nodes) == sorted(nodes - {t}) and sorted(leaves) ==
            sorted(1 << i for i in range(t.bit_length()) if (t >> i) & 1))


# ---------------------------------------------------------------- main
def check(matrix_path, cert_path, claim=None, aes=False, brute=True, quiet=False):
    lines = []

    def report(status, tag, msg):
        lines.append((status, tag, msg))
        if not quiet or status == 'FAIL':
            print('  [%s] %-2s %s' % (status, tag, msg))

    targets, ncols = parse_matrix(matrix_path)
    print('matrix : %s  (%d rows x %d columns, row weights %s)' % (
        matrix_path, len(targets), ncols, sorted({popcount(t) for t in targets})))
    allok = True
    if aes:
        ok = targets == aes_mixcolumns_rows()
        report('PASS' if ok else 'FAIL', 'A', 'matrix equals FIPS-197 MixColumns rebuilt here, row for row')
        allok &= ok
    D, tables, ok, stats = load_certificate(cert_path, targets, report)
    if tables is None:
        print('RESULT: FAIL (certificate unreadable)')
        return False, None
    allok &= ok
    report('PASS' if ok else 'FAIL', 'K',
           '%d priced entries parsed strictly; bad syntax %d, bad value %d, malformed key %d, '
           'duplicate JSON keys %d' % (stats['entries'], stats['bad_syntax'], stats['bad_value'],
                                       stats['bad_key'], stats['dup_json']))
    report('INFO', 'K', 'keys spelt with A NOT holding lowbit(S): %d (normalised); two spellings of '
           'one split inside one table: %d; zero prices: %d' % (stats['reversed'], stats['merged'], stats['zero']))
    # (C')
    col = {}
    rows_of = {}
    for ti, tab in enumerate(tables):
        for key, v in tab.items():
            col[key] = col.get(key, 0) + v
            rows_of.setdefault(key, set()).add(ti)
    mx = max(col.values()) if col else 0
    over = [k for k, v in col.items() if v > D]
    tight = sum(1 for v in col.values() if v == D)
    shared = sum(1 for k in col if len(rows_of[k]) > 1)
    okc = not over
    report('PASS' if okc else 'FAIL', 'C',
           "(C') %d distinct (S,split) columns, %d priced by >= 2 rows; max column sum %d / D=%d; "
           'columns over D: %d; tight columns: %d' % (len(col), shared, mx, D, len(over), tight))
    allok &= okc
    # DPs
    num = 0
    memo = {}
    per = []
    okd = True
    nh = 0
    for ti, t in enumerate(targets):
        if popcount(t) < 2:
            per.append(0)
            continue
        v1, wit = dp_min(t, tables[ti], want_witness=True)
        wv = sum(tables[ti].get(canon(S, A), 0) for S, A in wit)
        good = validate_hierarchy(t, wit) and wv == v1
        if brute:
            v2, k = brute_min(t, tables[ti], memo)
            nh += k
            good = good and v2 == v1
        okd &= good
        per.append(v1)
        num += v1
    report('PASS' if okd else 'FAIL', 'D',
           'per-row minima: DP over all submasks%s; argmin hierarchies re-validated and re-priced' % (
               (' == brute force over all %d hierarchies' % nh) if brute else ''))
    allok &= okd
    B = Fraction(num, D)
    ceilB = -(-num // D)
    report('INFO', 'B', 'numerator %d, D %d, B = %s = %.7f, ceil(B) = %d' % (num, D, B, num / D, ceilB))
    if claim is not None:
        okb = ceilB >= claim
        report('PASS' if okb else 'FAIL', 'B', 'ceil(B) = %d  %s claim %d' % (ceilB, '>=' if okb else '<', claim))
        allok &= okb
    print('RESULT: %s  (B = %.7f, ceil = %d)' % ('certificate VALID' if allok else 'FAIL', num / D, ceilB))
    return allok, dict(num=num, D=D, B=B, ceil=ceilB, per=per, col=col, tables=tables, targets=targets)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--matrix', required=True)
    ap.add_argument('--cert', required=True)
    ap.add_argument('--claim', type=int, default=None)
    ap.add_argument('--aes-crosscheck', action='store_true')
    ap.add_argument('--no-bruteforce', action='store_true')
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    ok, _ = check(a.matrix, a.cert, a.claim, a.aes_crosscheck, not a.no_bruteforce, a.quiet)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
