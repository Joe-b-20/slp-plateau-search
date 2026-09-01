#!/usr/bin/env python3
"""Agreement control: the ORIGINAL PYTHON deletion test, run on the same
records the C tool reads, printing the same three aggregates.

The C tool `delcert` is a ~300x-faster port of two Python checks that predate
it.  A port is worth nothing unless it is diffed against the thing it ports, so
this file carries the Python -- the local necessary condition and the greedy
closure -- transcribed verbatim, with no import from the project, and prints
`tested`, `local_pass`, `realisable` for a slice of a mask file.  Run it and
`delcert` on the same slice; the three numbers must be identical.

Standard library only.

  usage: pycheck.py <masks.bin> [start] [count]

`masks.bin` is 88 x uint32 little-endian per record.
"""
import struct
import sys
import time


# --- MixColumns target masks, rebuilt from GF(2^8) (the spec IS this code) ---
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


def realisable(masks):
    """Greedy topological check: can this multiset be built by 2-input XORs
    from the 32 inputs?  Monotone and order-free, so the fixpoint decides it."""
    avail = set(1 << i for i in range(32))
    rem = list(masks)
    prog = True
    while rem and prog:
        prog = False
        nxt = []
        for m in rem:
            got = False
            for s in avail:
                if (m ^ s) in avail:
                    got = True
                    break
            if got:
                avail.add(m)
                prog = True
            else:
                nxt.append(m)
        rem = nxt
    return not rem


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 300

    T = set(target_masks())
    INP = [1 << i for i in range(32)]

    f = open(path, 'rb')
    f.seek(start * 352)
    t0 = time.monotonic()
    tot = del_ok = survivors = 0
    r = -1
    for r in range(count):
        b = f.read(352)
        if len(b) < 352:
            r -= 1
            break
        S = set(struct.unpack('<88I', b))
        assert len(S) == 88 and T <= S
        A = set(INP) | S

        # local necessary condition: every remaining mask must keep at least
        # one derivation pair once m is gone
        deriv = {x: [] for x in S}
        Al = sorted(A)
        for a in Al:
            for b2 in Al:
                if b2 <= a:
                    continue
                x = a ^ b2
                if x in deriv:
                    deriv[x].append((a, b2))
        for m in S:
            if m in T:
                continue                      # deleting a target loses an output
            tot += 1
            bad = False
            for x, ps in deriv.items():
                if x == m:
                    continue
                if not any(m != a and m != b2 for a, b2 in ps):
                    bad = True
                    break
            if bad:
                continue
            survivors += 1
            if realisable(S - {m}):           # full greedy closure
                del_ok += 1
                print('!!! DELETABLE record %d mask %08x' % (start + r, m),
                      flush=True)
    print('{"PYTHON":1,"start":%d,"count":%d,"tested":%d,"local_pass":%d,'
          '"realisable":%d,"secs":%.1f}'
          % (start, r + 1, tot, survivors, del_ok, time.monotonic() - t0))


if __name__ == '__main__':
    main()
