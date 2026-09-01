#!/usr/bin/env python3
"""Cancellation-freeness checker for an XOR-SLP.

Replays a circuit against a 0/1 matrix and reports, independently:

    gates            how many XOR gates it uses
    targets built    how many of the matrix's rows appear as gate outputs
    kappa            how many gates CANCEL, i.e. how many gates have two
                     operand masks with overlapping support
    depth            longest input-to-output path, COMPUTED, not asserted

An SLP is cancellation-free exactly when kappa = 0: every gate is a "clean"
XOR of two disjoint sets of inputs, so no bit produced earlier is ever
destroyed.  A cancellation-free circuit with g gates and all targets built is
a witness for  L_cf(M) <= g.

Circuit format:  JSON with {"gates": [[a, b], ...]}  (an optional "gateCount"
is cross-checked).  Signals 0..n-1 are the inputs; gate k outputs signal
n + k = signal[a] XOR signal[b].  A bare list of pairs is also accepted.

Python 3 standard library only.

Usage:
    python3 check_cancellation_free.py CIRCUIT.json [--matrix PATH]
                                                    [--require-cancellation-free]
Exit 0 iff every matrix row is built (and, with the flag, kappa = 0).
"""

import argparse
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


def load_gates(path):
    obj = json.load(open(path))
    if isinstance(obj, list):
        return obj, None
    if 'gates' not in obj:
        raise SystemExit('%s: no "gates" key' % path)
    return obj['gates'], obj.get('gateCount')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('circuit')
    ap.add_argument('--matrix', default=os.path.join(HERE, '..', 'matrix.txt'))
    ap.add_argument('--require-cancellation-free', action='store_true')
    args = ap.parse_args()

    targets, n = load_matrix(args.matrix)
    gates, stated = load_gates(args.circuit)

    sig = [1 << i for i in range(n)]
    dep = [0] * n
    kappa = 0
    cancelling = []
    for k, g in enumerate(gates):
        if len(g) != 2:
            raise SystemExit('gate %d is not a pair: %r' % (k, g))
        a, b = g
        if not (0 <= a < len(sig) and 0 <= b < len(sig)):
            raise SystemExit('gate %d references a signal that does not exist yet '
                             '(a=%d b=%d, %d signals so far)' % (k, a, b, len(sig)))
        if sig[a] & sig[b]:
            kappa += 1
            cancelling.append(k)
        sig.append(sig[a] ^ sig[b])
        dep.append(max(dep[a], dep[b]) + 1)

    produced = set(sig[n:])
    built = sum(1 for t in targets if t in produced)
    depth = max(dep) if dep else 0

    print('circuit          : %s' % show(args.circuit))
    print('matrix           : %s  (%d rows x %d columns)'
          % (show(args.matrix), len(targets), n))
    print()
    print('  gates          : %d%s' % (len(gates),
          '' if stated is None else '   (file states gateCount = %d, %s)'
          % (stated, 'MATCHES' if stated == len(gates) else 'MISMATCH')))
    print('  targets built  : %d of %d' % (built, len(targets)))
    print('  kappa          : %d   (gates whose two operand masks overlap)' % kappa)
    print('  depth          : %d   (computed from the gate list, not asserted)' % depth)
    if cancelling:
        print('  cancelling at  : gate indices %s%s'
              % (cancelling[:10], ' ...' if len(cancelling) > 10 else ''))
    print()

    ok = built == len(targets) and (stated is None or stated == len(gates))
    if args.require_cancellation_free:
        ok = ok and kappa == 0

    print('=' * 74)
    if not ok:
        print('RESULT: FAIL')
        return 1
    if kappa == 0:
        print('RESULT: VALID and CANCELLATION-FREE.')
        print('  All %d rows are built and no gate cancels, so this circuit is a'
              % len(targets))
        print('  witness for  L_cf(M) <= %d.' % len(gates))
    else:
        print('RESULT: VALID, but NOT cancellation-free (kappa = %d).' % kappa)
        print('  It witnesses L(M) <= %d; it says nothing about L_cf(M).' % len(gates))
    return 0


if __name__ == '__main__':
    sys.exit(main())
