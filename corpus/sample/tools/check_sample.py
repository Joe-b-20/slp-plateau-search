#!/usr/bin/env python3
"""Re-check every row of the shipped corpus sample.

Needs nothing but this pack and a Python 3 interpreter.  Standard library only.

For each of the sampled 88-gate mask sets it re-derives, from scratch:
  * the 32 MixColumns target masks, rebuilt from GF(2^8) arithmetic;
  * that the row carries exactly 88 DISTINCT masks;
  * that all 32 target masks are present among them;
  * that the row's `canon` id is the sha256-16 of its own sorted mask list;
  * that the .jsonl row and the corresponding .bin record agree bit for bit.

It also re-prints the stratum composition and re-computes the two file hashes
recorded in SAMPLE.sha256.

  usage: check_sample.py [sample_dir]        (default: this script's parent)
"""
import collections
import hashlib
import json
import os
import struct
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


def canon(masks):
    return hashlib.sha256(
        ','.join('%08x' % m for m in sorted(masks)).encode()).hexdigest()[:16]


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else \
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    jpath = os.path.join(d, 'corpus88_sample.jsonl')
    bpath = os.path.join(d, 'corpus88_sample.bin')

    T = set(target_masks())
    wts = sorted(collections.Counter(bin(m).count('1') for m in T).items())
    assert wts == [(5, 20), (7, 12)], 'MixColumns spec self-check failed'
    print('MixColumns target masks rebuilt from GF(2^8) mod 0x11B: '
          '32 masks, weight profile 20x5 + 12x7  [OK]')

    rows = [json.loads(l) for l in open(jpath)]
    bf = open(bpath, 'rb')
    comp = collections.Counter()
    seen = set()
    published = []
    bad = 0

    for i, r in enumerate(rows):
        masks = [int(x, 16) for x in r['masks']]
        S = set(masks)
        try:
            assert len(masks) == 88, 'not 88 masks'
            assert len(S) == 88, 'masks not distinct'
            assert T <= S, 'missing %d target mask(s)' % len(T - S)
            assert r['canon'] == canon(masks), 'canon id does not match masks'
            assert r['canon'] not in seen, 'duplicate mask set in the sample'
            brec = list(struct.unpack('<88I', bf.read(352)))
            assert brec == sorted(masks), '.bin record disagrees with .jsonl'
        except AssertionError as e:
            print('  ROW %d (%s): FAIL -- %s' % (i, r['canon'], e))
            bad += 1
            continue
        seen.add(r['canon'])
        comp[r['source']] += 1
        if r.get('record_circuit'):
            published.append(r['record_circuit'])

    assert not bf.read(1), 'the .bin file has more records than the .jsonl'

    print('\nchecked %d rows: %d distinct mask sets, each 88 distinct masks '
          'with all 32 targets' % (len(rows), len(seen)))
    print('failures: %d' % bad)
    print('\nstratum composition')
    for k, v in comp.most_common():
        print('  %-22s %4d' % (k, v))
    print('  %-22s %4d' % ('TOTAL', sum(comp.values())))
    print('\nthe five published record 88s are present:')
    for p in sorted(published):
        print('  %s' % p)

    print('\nfile hashes')
    print('  %s  corpus88_sample.jsonl' % sha256(jpath))
    print('  %s  corpus88_sample.bin' % sha256(bpath))
    expect = os.path.join(d, 'SAMPLE.sha256')
    if os.path.exists(expect):
        print('\nrecorded in SAMPLE.sha256:')
        sys.stdout.write(''.join('  ' + l for l in open(expect)))

    print('\nVERDICT: %s' % ('ALL ROWS PASS' if bad == 0 else '%d ROW(S) FAILED'
                             % bad))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
