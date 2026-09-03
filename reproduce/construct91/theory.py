#!/usr/bin/env python3
"""theory.py — Lane G: the whole algebraic frame, re-derived from scratch.

NOTHING in this file is copied from a record circuit, and nothing is imported
from atlas/ or fleet1/.  Everything is derived from two inputs only:

  (a) the AES field GF(2^8) = F2[x]/(x^8+x^4+x^3+x+1);
  (b) the FIPS-197 MixColumns matrix (coefficients [2,3,1,1] circulant over
      the four bytes of a column).

Derived here, in order:

  1. Tr : F -> F2, and the trace-dual basis  D = {d_0..d_7}  of the bit basis
     {x^0..x^7}   (Tr(d_k x^l) = delta_kl).
  2. The mask <-> ring dictionary.  R = F[v]/(v^4), v = y+1, y = the byte
     rotation.  A 32-bit mask (a linear functional on the 32 input bits) is
     the ring element z with <m,a> = Tr_0(z * a(y)).
  3. LINE COORDINATES.  z = sum_m d_m (x) t_m with t_m in T = F2[v]/(v^4)
     (a nibble, bit i = v^i).  This is the coordinate system the whole
     project's "sector / ladder" frame lives in.
  4. The DUAL XTIME CHAIN  2 d_k = d_{k-1} + tau_k d_7  and, from it, the
     LADDER: sector S_k = span{d_k, 2 d_k} (x) T; clean sectors and tap
     sectors, and each sector's q-line.  DERIVED, not tabulated.
  5. The UNIVERSAL SECTOR PROBLEM: the four sector targets in (p,q)-nibble
     coordinates are the same four elements of T^2 in every sector.

Self-test: `python3 theory.py`.
"""

AES = 0x11B


# ---------------------------------------------------------------- GF(2^8)
def fmul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        if a & 0x100:
            a ^= AES
        b >>= 1
    return r


def ftr(a):
    """absolute trace F256 -> F2 (sum of the 8 Frobenius conjugates)."""
    t, x = 0, a
    for _ in range(8):
        t ^= x
        x = fmul(x, x)
    return t & 1


def build_duals():
    """trace-dual basis of the bit basis: Tr(d_k x^l) = delta_{kl}."""
    G = [[ftr(fmul(1 << t, 1 << l)) for t in range(8)] for l in range(8)]
    n = 8
    M = [G[i][:] + [1 if i == j else 0 for j in range(n)] for i in range(n)]
    r = 0
    for c in range(n):
        p = next((i for i in range(r, n) if M[i][c]), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        for i in range(n):
            if i != r and M[i][c]:
                M[i] = [a ^ b for a, b in zip(M[i], M[r])]
        r += 1
    inv = [row[n:] for row in M]
    duals = []
    for k in range(8):
        val = 0
        for t in range(8):
            if inv[t][k]:
                val ^= (1 << t)
        duals.append(val)
    for k in range(8):
        for l in range(8):
            assert ftr(fmul(duals[k], 1 << l)) == (1 if k == l else 0)
    return duals


DUALS = build_duals()                      # d_0 .. d_7


# ------------------------------------------------------- the MixColumns spec
def mixcolumns_target_masks():
    """32 target masks, rebuilt from FIPS-197.  Row (byte col, bit ob) is
    index 8*col+ob; input bit (byte ib, bit inb) is index 8*ib+inb."""
    coef = [2, 3, 1, 1]
    M = [[0] * 32 for _ in range(32)]
    for col in range(4):
        for k in range(4):
            c, ib = coef[k], (col + k) % 4
            for in_bit in range(8):
                v = 0
                b = 1 << in_bit
                for i in range(8):
                    if (c >> i) & 1:
                        t = b
                        for _ in range(i):
                            t = ((t << 1) ^ AES) & 0xFF if (t << 1) & 0x100 \
                                else (t << 1) & 0xFF
                        v ^= t
                for out_bit in range(8):
                    if (v >> out_bit) & 1:
                        M[col * 8 + out_bit][ib * 8 + in_bit] ^= 1
    masks = []
    for r in range(32):
        m = 0
        for c in range(32):
            if M[r][c]:
                m |= (1 << c)
        masks.append(m)
    return masks


TARGET_MASKS = mixcolumns_target_masks()


# ------------------------------------------------------ mask <-> ring <-> lines
def _radd(z, w):
    return tuple(z[i] ^ w[i] for i in range(4))


def mask_to_ring(m):
    """y-coordinates (mu_0..mu_3) of the ring element of a 32-bit mask."""
    z = (0, 0, 0, 0)
    for j in range(4):
        for k in range(8):
            if (m >> (8 * j + k)) & 1:
                e = [0, 0, 0, 0]
                e[(4 - j) % 4] = DUALS[k]
                z = _radd(z, tuple(e))
    return z


def ring_to_mask(z):
    m = 0
    for j in range(4):
        for k in range(8):
            if ftr(fmul(z[(4 - j) % 4], 1 << k)):
                m |= 1 << (8 * j + k)
    return m


def to_v(z):
    """y-coordinates -> v-coordinates (v = y+1, so y = 1+v)."""
    mu0, mu1, mu2, mu3 = z
    return (mu0 ^ mu1 ^ mu2 ^ mu3, mu1 ^ mu3, mu2 ^ mu3, mu3)


def from_v(w):
    w0, w1, w2, w3 = w
    return (w0 ^ w1 ^ w2 ^ w3, w1 ^ w3, w2 ^ w3, w3)


def mask_to_lines(m):
    """32-bit mask -> (t_0..t_7), T-nibbles: z = sum_m d_m (x) t_m."""
    w = to_v(mask_to_ring(m))
    out = []
    for line in range(8):
        t = 0
        for i in range(4):
            if w[i] and ftr(fmul(w[i], 1 << line)):
                t |= (1 << i)
        out.append(t)
    return tuple(out)


def lines_to_mask(lines):
    w = [0, 0, 0, 0]
    for m in range(8):
        t = lines[m]
        for i in range(4):
            if (t >> i) & 1:
                w[i] ^= DUALS[m]
    return ring_to_mask(from_v(tuple(w)))


def support(lines):
    return frozenset(m for m in range(8) if lines[m])


def hexlines(lines):
    return "[" + " ".join(f"{t:x}" if t else "." for t in lines) + "]"


# --------------------------------------------------- T = F2[v]/(v^4) algebra
def tmul(a, b):
    r = 0
    for i in range(4):
        if (b >> i) & 1:
            r ^= (a << i)
    return r & 0xF


Y = 0x3          # y = 1 + v
W = 0x7          # w = 1 + v + v^2   (the unit factor of c)


def ypow(j):
    r = 1
    for _ in range(j):
        r = tmul(r, Y)
    return r


RAWS = [ypow(j) for j in range(4)]                       # 0x1,0x3,0x5,0xF
# ring exponent a  <->  input byte (-a) mod 4  (trace duality reverses order)
YBYTE = {a: (4 - a) % 4 for a in range(4)}
PAIRS = sorted({ypow(a) ^ ypow(b)
                for a in range(4) for b in range(a + 1, 4)})
# = [0x2,0x4,0x6,0xA,0xC,0xE] : the six pair-differences y^a + y^b.
UNITS = RAWS


# ------------------------------------- the dual xtime chain and the LADDER
def xtime_dual_coords(k):
    """express 2*d_k in the dual basis: returns the set of indices m with
    2 d_k = sum_m d_m.  (This IS the chain 2 d_k = d_{k-1} + tau_k d_7.)"""
    val = fmul(DUALS[k], 2)
    # coordinates of val in the dual basis: coefficient on d_m is Tr(val * x^m)
    return frozenset(m for m in range(8) if ftr(fmul(val, 1 << m)))


QLINES = {k: xtime_dual_coords(k) for k in range(8)}
# derived: sector k's q-part lives on the line set QLINES[k].
TAPS = sorted(k for k in range(8) if len(QLINES[k]) > 1)
CLEAN = sorted(k for k in range(8) if len(QLINES[k]) == 1)
PARENT = {}          # k -> the non-7 line of QLINES[k] (the "parent column")
for _k in range(8):
    _s = set(QLINES[_k])
    if len(_s) == 1:
        PARENT[_k] = next(iter(_s))
    else:
        _o = _s - {7}
        assert len(_o) == 1, (_k, _s)
        PARENT[_k] = next(iter(_o))


def sector_value_lines(k, p, q):
    """the sector-k value with p-part p (on line k) and q-part q (on 2 d_k)."""
    t = [0] * 8
    t[k] ^= p
    for m in QLINES[k]:
        t[m] ^= q
    return tuple(t)


# ----------------------------------------- the universal sector problem
# target for output byte j of sector k, in (p,q) nibble coordinates.
SECTOR_TARGETS = [(tmul(ypow(j + 1), W), tmul(tmul(0x2, ypow(j)), W))
                  for j in range(4)]
# packed 8-bit form used by the sector oracle: p | q<<4
SECTOR_TARGETS_PACKED = [p | (q << 4) for p, q in SECTOR_TARGETS]


def sector_of(lines):
    """which sector a value lies in (None if it is glue)."""
    s = support(lines)
    if not s:
        return None
    for k in range(8):
        ql = QLINES[k]
        if not (s <= ({k} | set(ql))):
            continue
        if len(ql) == 1:
            return k
        par = PARENT[k]
        if lines[par] == lines[7]:
            return k
    return None


# ---------------------------------------------------------------- self-test
def selftest():
    import random
    for _ in range(300):
        m = random.getrandbits(32)
        assert lines_to_mask(mask_to_lines(m)) == m
        assert ring_to_mask(mask_to_ring(m)) == m
    # the chain
    for k in range(8):
        s = set(QLINES[k])
        if k == 0:
            assert s == {7}, s
        else:
            assert (s - {7}) == {k - 1}, (k, s)
    tau = {k for k in range(8) if 7 in QLINES[k] and k != 0}
    assert tau == {1, 3, 4}, tau        # bits of 0x1B, shifted; d_{-1}=0
    assert TAPS == [1, 3, 4], TAPS
    assert CLEAN == [0, 2, 5, 6, 7], CLEAN
    # input bit (byte j, bit k) is d_k (x) y^{-j} : support {k}
    # (trace duality reverses byte order: ring y^a  <->  byte (-a) mod 4)
    for j in range(4):
        for k in range(8):
            L = mask_to_lines(1 << (8 * j + k))
            assert support(L) == {k}, (j, k, L)
            assert L[k] == ypow((4 - j) % 4), (j, k, L)
    assert YBYTE == {0: 0, 1: 3, 2: 2, 3: 1}
    # every target is sector-pure and equals the universal (p,q) target
    for idx, tm in enumerate(TARGET_MASKS):
        col, ob = divmod(idx, 8)
        L = mask_to_lines(tm)
        k = sector_of(L)
        assert k == ob, (idx, k, ob, hexlines(L))
        p, q = L[k], L[PARENT[k]]
        assert (p, q) in SECTOR_TARGETS, (idx, hex(p), hex(q))
    # the four sector targets are hit exactly once per sector, by byte
    for k in range(8):
        got = set()
        for j in range(4):
            p, q = SECTOR_TARGETS[j]
            got.add(lines_to_mask(sector_value_lines(k, p, q)))
        want = {TARGET_MASKS[8 * c + k] for c in range(4)}
        assert got == want, k
    # pair shapes are 2-bit masks on any line => depth-1 currency
    for t in PAIRS:
        for col in range(8):
            L = [0] * 8
            L[col] = t
            assert bin(lines_to_mask(tuple(L))).count("1") == 2, (t, col)
    print("theory selftest OK")
    print("  DUALS      =", [f"{d:02x}" for d in DUALS])
    print("  QLINES     =", {k: sorted(QLINES[k]) for k in range(8)})
    print("  TAPS       =", TAPS, " CLEAN =", CLEAN)
    print("  PARENT     =", PARENT)
    print("  RAWS       =", [f"{t:x}" for t in RAWS])
    print("  PAIRS      =", [f"{t:x}" for t in PAIRS])
    print("  SECTOR_TGT =", [(f"{p:x}", f"{q:x}") for p, q in SECTOR_TARGETS])


if __name__ == "__main__":
    selftest()
