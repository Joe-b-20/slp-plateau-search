#!/usr/bin/env python3
"""Is this circuit inside the corpus mask vocabulary, or outside it?

`vocab.json` is the set of every DISTINCT non-target gate mask that occurs
anywhere in the 88-gate corpus re-census -- 1,778 values, drawn from
107,803,640 non-target gate slots across 1,925,065 accepted circuit rows.  That
is the entire vocabulary the accumulated search has ever spoken in.

This script replays a circuit, subtracts the 32 MixColumns target masks, and
reports which of the remaining masks are NOT in that vocabulary.  A non-empty
answer means the circuit uses a value the corpus has never once produced -- it
is evidence that the corpus vocabulary is a property of the SEARCH, not a
property of the PROBLEM.

Standard library only.

  usage: oov_check.py <vocab.json> <circuit.json>

Exit 0 if at least one out-of-vocabulary mask is found, 1 if the circuit is
entirely inside the vocabulary.
"""
import json
import sys


def _xtime(a):
    a <<= 1
    return (a ^ 0x11B) & 0xFF if (a & 0x100) else (a & 0xFF)


def _gf_mul(a, b):
    r = 0
    for i in range(8):
        if (b >> i) & 1:
            t = a
            for _ in range(i):
                t = _xtime(t)
            r ^= t
    return r & 0xFF


def target_masks():
    coef = [2, 3, 1, 1]
    M = [[0] * 32 for _ in range(32)]
    for col in range(4):
        for k in range(4):
            c, ib = coef[k], (col + k) % 4
            for in_bit in range(8):
                v = _gf_mul(c, 1 << in_bit)
                for out_bit in range(8):
                    if (v >> out_bit) & 1:
                        M[col * 8 + out_bit][ib * 8 + in_bit] ^= 1
    return [sum(1 << c for c in range(32) if M[r][c]) for r in range(32)]


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    vocab = set(json.load(open(sys.argv[1])))
    d = json.load(open(sys.argv[2]))
    gates = d['gates'] if isinstance(d, dict) else d

    sig = [1 << i for i in range(32)]
    for a, b in gates:
        sig.append(sig[a] ^ sig[b])
    masks = sig[32:]
    T = set(target_masks())
    nontarget = sorted(set(masks) - T)
    oov = [m for m in nontarget if m not in vocab]

    print('vocabulary            : %d distinct non-target masks' % len(vocab))
    print('circuit               : %d gates, %d distinct masks'
          % (len(gates), len(set(masks))))
    print('  of which targets    : %d / 32' % len(set(masks) & T))
    print('  non-target masks    : %d' % len(nontarget))
    print('  IN  the vocabulary  : %d' % (len(nontarget) - len(oov)))
    print('  OUT of the vocabulary: %d' % len(oov))
    for m in oov:
        print('    0x%08x  (decimal %d, Hamming weight %d)'
              % (m, m, bin(m).count('1')))
    if oov:
        print('\nVERDICT: OUT OF VOCABULARY. %d mask(s) in this circuit occur '
              'in no\n         entry of the 1,778-value corpus vocabulary.'
              % len(oov))
    else:
        print('\nVERDICT: entirely inside the corpus vocabulary.')
    sys.exit(0 if oov else 1)


if __name__ == '__main__':
    main()
