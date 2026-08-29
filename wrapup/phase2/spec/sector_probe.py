#!/usr/bin/env python3
"""sector_probe.py -- what the fleet8 generator's frame does on InvMixColumns.

Reuses fleet8/unified/code/theory.py's FIELD-ONLY machinery (which is unchanged
for the inverse: same GF(2^8)/0x11B, same dual basis, same dual xtime chain,
same QLINES / TAPS / CLEAN / PARENT) and points it at the [e,b,d,9] targets.
It changes nothing in theory.py; it only measures.

Answers, with numbers, the question fleet5_8.md's Generality block raises:
  "The inverse matrix's coefficients do not have this two-part shape, so this
   decomposition -- and with it laws.workset (L1), the block line-sets, and the
   whole ten-block architecture -- has to be RE-DERIVED, not re-typed."

Prints:
  1. c(y) and c_inv(y) expanded in the v-basis (v = y+1) over GF(2^8), and the
     GF(2)-scalar structure that W = 0x7 came from.
  2. c_inv == c^3 in R = GF(2^8)[y]/(y^4+1)  (the AES ring fact, independently
     of the 32x32 check in derive_invmc.py).
  3. per-target line supports, forward vs inverse: the workset widths that L1
     feeds to the block architecture.
"""
import os
import sys

ROOT = '/home/joebachir20/xor_ui/slp-plateau-search'
sys.path.insert(0, os.path.join(ROOT, 'fleet8/unified/code'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theory                                              # noqa: E402
from derive_invmc import build_matrix, matrix_to_masks, FWD_COEF, INV_COEF  # noqa: E402

fmul = theory.fmul


# --------------------------------------------- R = GF(2^8)[y]/(y^4+1) arithmetic
def rmul(a, b):
    """multiply two length-4 coefficient vectors mod y^4 + 1."""
    out = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            out[(i + j) % 4] ^= fmul(a[i], b[j])
    return out


def to_v_basis(c):
    """c(y) with y = 1+v  ->  coefficients in the v basis, mod v^4 (= y^4+1)."""
    out = [0, 0, 0, 0]
    for j, cj in enumerate(c):
        # (1+v)^j = sum_i C(j,i) v^i, binomial mod 2
        for i in range(j + 1):
            b = 1
            for t in range(i):
                b = b * (j - t) // (t + 1)
            if b & 1:
                out[i] ^= cj
    return out


def tinv(a):
    """inverse of a unit of T = F2[v]/(v^4)  (units are those with a&1)."""
    assert a & 1, "not a unit of T"
    for b in range(16):
        if theory.tmul(a, b) == 1:
            return b
    raise AssertionError


def chain_coords(k, i):
    """dual-basis coordinates of (2^i * d_k): the set of m with 2^i d_k = sum d_m.
    i=0 is d_k itself; i=1 is theory.xtime_dual_coords(k) (= QLINES[k])."""
    val = theory.DUALS[k]
    for _ in range(i):
        val = fmul(val, 2)
    return frozenset(m for m in range(8) if theory.ftr(fmul(val, 1 << m)))


def solve_chain(L, chains):
    """Express the line vector L as sum_i c_i * (2^i d_k), c_i in T.

    t_m = sum_i a_{i,m} c_i  with a_{i,m} in F2 (a = the chain incidence matrix).
    Solve the 8x4 F2 system once per T-bit-plane; returns (c0,c1,c2,c3) or None.
    """
    A = [[1 if m in chains[i] else 0 for i in range(4)] for m in range(8)]
    c = [0, 0, 0, 0]
    for bit in range(4):
        rhs = [(L[m] >> bit) & 1 for m in range(8)]
        rows = [A[m][:] + [rhs[m]] for m in range(8)]
        piv, r = [], 0
        for col in range(4):
            p = next((i for i in range(r, 8) if rows[i][col]), None)
            if p is None:
                continue
            rows[r], rows[p] = rows[p], rows[r]
            for i in range(8):
                if i != r and rows[i][col]:
                    rows[i] = [a ^ b for a, b in zip(rows[i], rows[r])]
            piv.append(col)
            r += 1
        for i in range(r, 8):
            if rows[i][4] and not any(rows[i][:4]):
                return None                       # inconsistent
        sol = [0, 0, 0, 0]
        for i, col in enumerate(piv):
            sol[col] = rows[i][4]
        for i in range(4):
            if sol[i]:
                c[i] |= (1 << bit)
    return tuple(c)


def show_poly(name, c, var):
    terms = [f"{c[i]:02x}*{var}^{i}" for i in range(4) if c[i]]
    print(f"   {name:<10} = " + " + ".join(terms))


def scalar_bits(coeffs):
    """for each v-power, which powers of x (= the field element 2) appear."""
    out = {}
    for i, c in enumerate(coeffs):
        out[i] = [b for b in range(8) if (c >> b) & 1]
    return out


def main():
    print("=" * 74)
    print("sector_probe.py -- the fleet8 frame applied to InvMixColumns")
    print("=" * 74)
    print(f"field-only constants (UNCHANGED for the inverse: same 0x11B)")
    print(f"   DUALS  = {[f'{d:02x}' for d in theory.DUALS]}")
    print(f"   QLINES = {{k: sorted(theory.QLINES[k]) for k}} -> "
          f"{ {k: sorted(theory.QLINES[k]) for k in range(8)} }")
    print(f"   TAPS   = {theory.TAPS}   CLEAN = {theory.CLEAN}")
    print(f"   PARENT = {theory.PARENT}")
    print()

    # ---- 1. the column polynomials
    # FIPS-197: out_byte[col] = sum_k coef[k]*in_byte[(col+k)%4].  As an element
    # of R the column polynomial has coefficient coef[k] on y^k.
    cf = list(FWD_COEF)
    ci = list(INV_COEF)
    print("-- 1. the column polynomials in R = GF(2^8)[y]/(y^4+1) " + "-" * 18)
    show_poly("c_fwd", cf, "y")
    show_poly("c_inv", ci, "y")
    vf, vi = to_v_basis(cf), to_v_basis(ci)
    print("   substitute y = 1 + v   (v = y+1, v^4 = 0 in this ring):")
    show_poly("c_fwd", vf, "v")
    show_poly("c_inv", vi, "v")
    print()
    print("   GF(2)-scalar structure -- which powers of x (=the byte 0x02) appear")
    print("   on each v-power.  theory.py's (p,q) split assumes EXACTLY x^0 and x^1:")
    print(f"     c_fwd : {scalar_bits(vf)}")
    print(f"     c_inv : {scalar_bits(vi)}")
    fs = sorted({b for bs in scalar_bits(vf).values() for b in bs})
    is_ = sorted({b for bs in scalar_bits(vi).values() for b in bs})
    print(f"     x-powers used:  forward {fs}   inverse {is_}")
    print(f"   => forward needs the dual chain to depth {max(fs)} (p-part + ONE tap"
          f" 2*d_k)")
    print(f"   => inverse needs it to depth {max(is_)} (p-part + taps 2,4,8 * d_k):"
          f" the (p,q) pair coordinate is NOT enough")
    print()

    # ---- 1b. W = 0x7 : the computation that produced it
    print("-- 1b. where W = 0x7 and SECTOR_TARGETS actually come from " + "-" * 15)
    W = theory.W
    fwd_masks = matrix_to_masks(build_matrix(FWD_COEF))
    # MEASURE the (p,q) coordinates of the forward targets with theory's own
    # readout: k = sector_of(L); p = L[k]; q = L[PARENT[k]].
    meas = {}
    for idx, m in enumerate(fwd_masks):
        col, ob = divmod(idx, 8)
        L = theory.mask_to_lines(m)
        k = theory.sector_of(L)
        assert k == ob, (idx, k, ob)
        meas.setdefault(col, set()).add((L[k], L[theory.PARENT[k]]))
    print("   measured (p,q) per output column, over all eight sectors.")
    print("   NOTE the index map: SECTOR_TARGETS is indexed by the RING EXPONENT")
    print("   a, output byte col = (4-a) mod 4 (theory.YBYTE; trace duality")
    print("   reverses byte order).")
    for col in range(4):
        assert len(meas[col]) == 1, (col, meas[col])
        p, q = next(iter(meas[col]))
        a = (4 - col) % 4
        print(f"     column {col} (exponent a={a}): (p,q) = (0x{p:x}, 0x{q:x})"
              f"   SECTOR_TARGETS[{a}] = "
              f"(0x{theory.SECTOR_TARGETS[a][0]:x}, 0x{theory.SECTOR_TARGETS[a][1]:x})"
              f"   {'==' if (p, q) == theory.SECTOR_TARGETS[a] else '!!'}")
    # W is then SOLVED for, not chosen: p_0 = y * W  =>  W = y^{-1} p_0.
    yinv = tinv(theory.Y)
    p0 = next(iter(meas[0]))[0]
    q0 = next(iter(meas[0]))[1]
    Wsolved = theory.tmul(yinv, p0)
    print(f"   y = 0x{theory.Y:x}, y^-1 = 0x{yinv:x} in T = F2[v]/(v^4)")
    print(f"   W := y^-1 * p(column 0) = 0x{Wsolved:x}"
          f"   theory.W = 0x{W:x}   {'==' if Wsolved == W else '!!'}")
    print(f"   cross-check q(column 0) = v * W ?  v*W = 0x{theory.tmul(0x2, W):x}"
          f"  measured 0x{q0:x}   {'==' if theory.tmul(0x2, W) == q0 else '!!'}")
    ok_closed = all(theory.SECTOR_TARGETS[(4 - col) % 4] == next(iter(meas[col]))
                    for col in range(4))
    print(f"   closed form SECTOR_TARGETS[a] = (y^(a+1) W, v y^a W) reproduces all"
          f" four columns: {'PASS' if ok_closed else 'FAIL'}")
    print("   => THE COMPUTATION: measure (p,q) of the targets in the dual-chain")
    print("      frame, observe they are column-shifts of one another, solve for")
    print("      the unit W.  It is a two-coordinate frame ONLY because c_fwd's")
    print("      scalars are {x^0, x^1}.  For the inverse this readout does not")
    print("      even parse: see section 3 (0/32 sector-pure) and section 4.")
    print()

    # ---- 2. c_inv == c_fwd^3 in the ring
    print("-- 2. the ring fact  c_inv == c_fwd^3  mod y^4+1 " + "-" * 25)
    c3 = rmul(rmul(cf, cf), cf)
    c4 = rmul(c3, cf)
    print(f"   c_fwd^3 = {[f'{x:02x}' for x in c3]}   c_inv = {[f'{x:02x}' for x in ci]}"
          f"   {'PASS' if c3 == ci else 'FAIL'}")
    print(f"   c_fwd^4 = {[f'{x:02x}' for x in c4]}   (== 1)  "
          f"{'PASS' if c4 == [1, 0, 0, 0] else 'FAIL'}")
    print(f"   c_fwd*c_inv = {[f'{x:02x}' for x in rmul(cf, ci)]}  (== 1)  "
          f"{'PASS' if rmul(cf, ci) == [1, 0, 0, 0] else 'FAIL'}")
    print()

    # ---- 3. line supports of the targets
    print("-- 3. targets in line coordinates (theory.mask_to_lines) " + "-" * 17)
    for label, coef in (("forward", FWD_COEF), ("inverse", INV_COEF)):
        masks = matrix_to_masks(build_matrix(coef))
        sup, pure, wsets = [], 0, []
        for idx, m in enumerate(masks):
            L = theory.mask_to_lines(m)
            s = theory.support(L)
            sup.append(len(s))
            wsets.append(s)
            if theory.sector_of(L) is not None:
                pure += 1
        from collections import Counter
        print(f"   {label}: line-support sizes {dict(sorted(Counter(sup).items()))}"
              f"   mean {sum(sup)/32:.2f}")
        print(f"           sector-pure under theory.sector_of(): {pure}/32")
        # L1 workset comparison: forward L1 is {j} u QLINES[j]
        widths = []
        for ob in range(8):
            u = set()
            for col in range(4):
                u |= wsets[8 * col + ob]
            widths.append(len(u))
        print(f"           union of the four column targets per output bit-line:"
              f" widths {widths}")
        print(f"           L1 forward workset |{{j}} u QLINES[j]| = "
              f"{[len({k} | theory.QLINES[k]) for k in range(8)]}")
    print()

    # ---- 4. the GENERALISED sector: does a 4-tap chain frame the inverse?
    print("-- 4. re-deriving the sector frame for the inverse " + "-" * 23)
    print("   forward sector S_k = span{d_k, 2 d_k} (x) T  (two taps, from the")
    print("   scalars {x^0, x^1} of c_fwd).  c_inv uses {x^0..x^3}, so try")
    print("   S'_k = span{d_k, 2 d_k, 4 d_k, 8 d_k} (x) T.")
    CH = [[chain_coords(k, i) for i in range(4)] for k in range(8)]
    GEN = [set().union(*CH[k]) for k in range(8)]
    print(f"   |S'_k| line-support per k: {[len(GEN[k]) for k in range(8)]}")
    inv_masks = matrix_to_masks(build_matrix(INV_COEF))
    pure, coords = 0, {}
    for idx, m in enumerate(inv_masks):
        col, ob = divmod(idx, 8)
        L = theory.mask_to_lines(m)
        s = theory.support(L)
        hits = [k for k in range(8) if s <= GEN[k]]
        c = None
        for k in hits:
            c = solve_chain(L, CH[k])
            if c is not None:
                pure += 1
                coords.setdefault(col, set()).add((k, c))
                break
    print(f"   inverse targets expressible as p d_k + q 2d_k + r 4d_k + s 8d_k"
          f" for a single k: {pure}/32")
    if pure == 32:
        base = None
        for col in range(4):
            cs = {c for _, c in coords[col]}
            a = (4 - col) % 4
            print(f"     column {col} (exponent a={a}): {len(cs)} distinct"
                  f" (p,q,r,s) across the 8 sectors ->"
                  f" {[tuple(hex(x) for x in c) for c in sorted(cs)]}")
            if a == 0:
                base = next(iter(cs))
        # does the same y^a column-shift law hold?
        shift_ok = True
        for col in range(4):
            a = (4 - col) % 4
            want = tuple(theory.tmul(theory.ypow(a), t) for t in base)
            got = next(iter({c for _, c in coords[col]}))
            shift_ok &= (want == got)
        print(f"   universal quadruple at a=0: {tuple(hex(t) for t in base)}"
              f"   (= (y*W, v*W, v^2, v^3) with W = 0x{W:x})")
        print(f"   column-shift law  SECTOR_TARGETS_inv[a] = y^a * that quadruple:"
              f" {'PASS' if shift_ok else 'FAIL'}")
        print("   => the inverse HAS a universal sector problem too, on a FOUR-")
        print("      coordinate frame.  laws.workset (L1) must be widened from")
        print("      {j} u QLINES[j] to the 4-tap line set above.")
    else:
        print("   => the 4-tap chain does NOT frame all inverse targets; the")
        print("      re-derivation must search a wider frame (see PORT_NOTES.md).")
    print()
    print("=" * 74)


if __name__ == '__main__':
    main()
