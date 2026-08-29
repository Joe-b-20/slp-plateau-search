#!/usr/bin/env python3
"""derive_invmc.py -- the AES InvMixColumns specification, from first principles.

NOTHING here is copied from a table.  The only inputs are:

  (a) the AES field  GF(2^8) = F2[x]/(x^8 + x^4 + x^3 + x + 1),  modulus 0x11B;
  (b) FIPS-197 sec. 5.3.3: InvMixColumns multiplies each column by the
      polynomial  {0b}y^3 + {0d}y^2 + {09}y + {0e}, i.e. the circulant column
      of coefficients [0x0e, 0x0b, 0x0d, 0x09] = [14, 11, 13, 9];
  (c) FIPS-197 sec. 5.1.3: MixColumns is the same with [0x02, 0x03, 0x01, 0x01].

BIT/BYTE CONVENTION  (read off verify_circuit.py:37-55, not from memory):

    out row index  = 8*col    + out_bit      (col = output byte, 0..3)
    in  col index  = 8*in_byte + in_bit
    bit i of a byte is the coefficient of x^i  ->  LSB-FIRST inside the byte.
    M[r][c] = 1  iff  output bit r depends on input bit c.
    mask(r)  = sum_c M[r][c] << c            (a 32-bit int; bit c = input c)

    output byte `col` = sum_k coef[k] * in_byte[(col+k) % 4]        (circulant)

Emits, into this directory:
    invmc_matrix.json        32x32 GF(2) matrix + provenance header
    invmc_target_masks.json  the 32 masks, same convention as the corpus
    mixcolumns_matrix.json   the forward control, same format
    mixcolumns_target_masks.json

CONTROLS (all mandatory, all printed; exit non-zero on any failure):
  C1  forward derivation == verify_circuit.mixcolumns_target_masks()  (the
      oracle's own spec code) AND == fleet8/unified/code/theory.py's
      TARGET_MASKS (an independent second in-repo derivation).
  C2  M_fwd * M_inv == I  and  M_inv * M_fwd == I   over GF(2).
  C3  M_fwd^3 == M_inv    (the AES ring fact: c(y)^-1 = c(y)^3 mod y^4+1).
  C4  weight self-check on the forward masks: 20 rows of weight 5, 12 of
      weight 7 (verify_circuit.py:99's own assertion).

Usage: python3 derive_invmc.py [--out DIR]
"""
import argparse
import datetime
import hashlib
import json
import os
import sys

ROOT = '/home/joebachir20/xor_ui/slp-plateau-search'
AES_MODULUS = 0x11B

FWD_COEF = [0x02, 0x03, 0x01, 0x01]      # FIPS-197 5.1.3  MixColumns
INV_COEF = [0x0E, 0x0B, 0x0D, 0x09]      # FIPS-197 5.3.3  InvMixColumns


# ------------------------------------------------------------------ GF(2^8)
def xtime(a):
    a <<= 1
    return (a ^ AES_MODULUS) & 0xFF if (a & 0x100) else (a & 0xFF)


def gf_mul(a, b):
    """a * b in GF(2^8)/0x11B.  Same shape as verify_circuit.py:26."""
    r = 0
    for i in range(8):
        if (b >> i) & 1:
            t = a
            for _ in range(i):
                t = xtime(t)
            r ^= t
    return r & 0xFF


# ----------------------------------------------------- the 32x32 GF(2) matrix
def build_matrix(coef):
    """32x32 GF(2) matrix of the circulant byte map with column `coef`.

    This is verify_circuit.py:37-47 with the coefficient list lifted out --
    identical index arithmetic, identical field code.
    """
    M = [[0] * 32 for _ in range(32)]
    for col in range(4):
        for k in range(4):
            c, ib = coef[k], (col + k) % 4
            for in_bit in range(8):
                v = gf_mul(c, 1 << in_bit)
                for out_bit in range(8):
                    if (v >> out_bit) & 1:
                        M[col * 8 + out_bit][ib * 8 + in_bit] ^= 1
    return M


def matrix_to_masks(M):
    """row r -> 32-bit int with bit c set iff M[r][c] == 1."""
    masks = []
    for r in range(32):
        m = 0
        for c in range(32):
            if M[r][c]:
                m |= (1 << c)
        masks.append(m)
    return masks


def masks_to_matrix(masks):
    return [[(m >> c) & 1 for c in range(32)] for m in masks]


# --------------------------------------------------------- GF(2) linear algebra
def mat_mul(A, B):
    """(A*B)[i][j] = sum_k A[i][k] B[k][j] over GF(2).  A,B are 32x32."""
    n = len(A)
    Bcols = [0] * n                      # Bcols[k] = row k of B, packed
    for k in range(n):
        v = 0
        for j in range(n):
            if B[k][j]:
                v |= 1 << j
        Bcols[k] = v
    out = []
    for i in range(n):
        acc = 0
        for k in range(n):
            if A[i][k]:
                acc ^= Bcols[k]
        out.append([(acc >> j) & 1 for j in range(n)])
    return out


def identity(n=32):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def mat_eq(A, B):
    return all(A[i][j] == B[i][j] for i in range(len(A)) for j in range(len(A)))


def density(M):
    return sum(sum(row) for row in M)


def gf2_rank(M):
    rows = [int(''.join(str(b) for b in reversed(r)), 2) for r in M]
    rank = 0
    for bit in range(len(M[0])):
        p = next((i for i in range(rank, len(rows)) if (rows[i] >> bit) & 1), None)
        if p is None:
            continue
        rows[rank], rows[p] = rows[p], rows[rank]
        for i in range(len(rows)):
            if i != rank and (rows[i] >> bit) & 1:
                rows[i] ^= rows[rank]
        rank += 1
    return rank


# ------------------------------------------------------------------ emission
def rows_as_bitstrings(M):
    """row r as a 32-char string; character at position c is M[r][c].
    Position c IS input index c = 8*in_byte + in_bit (LSB-first in the byte).
    Reading the string left-to-right therefore walks input index 0 -> 31."""
    return [''.join(str(b) for b in row) for row in M]


def rows_digest(M):
    return hashlib.sha256('\n'.join(rows_as_bitstrings(M)).encode()).hexdigest()


def matrix_doc(name, coef, M, script):
    masks = matrix_to_masks(M)
    return {
        "provenance": {
            "name": name,
            "spec": ("FIPS-197 sec. 5.3.3 InvMixColumns" if name.startswith("aes_inv")
                     else "FIPS-197 sec. 5.1.3 MixColumns"),
            "field": "GF(2^8) = F2[x]/(x^8+x^4+x^3+x+1)",
            "modulus": AES_MODULUS,
            "mds_column": coef,
            "structure": "circulant: out_byte[col] = XOR_k coef[k] * in_byte[(col+k)%4]",
            "convention": {
                "out_row_index": "8*out_byte + out_bit",
                "in_col_index": "8*in_byte + in_bit",
                "bit_order": "LSB-first: bit i of a byte is the coefficient of x^i",
                "mask": "mask(r) = OR_c M[r][c] << c  (bit c = input index c)",
                "rows_field": "rows[r][c] as a character: '1' iff output bit r depends on input bit c",
                "source_of_truth": "verify_circuit.py:37-55 (this repo)",
            },
            "derived_by": script,
            "derived_utc": datetime.datetime.now(datetime.timezone.utc)
                                   .strftime("%Y-%m-%dT%H:%M:%SZ"),
            "rows_sha256": rows_digest(M),
            "controls": "see wrapup/phase2/controls/",
        },
        "n_inputs": 32,
        "n_outputs": 32,
        "rank_gf2": gf2_rank(M),
        "density": density(M),
        "rows": rows_as_bitstrings(M),
        "row_weights": [sum(r) for r in M],
        "masks_hex": [f"0x{m:08x}" for m in masks],
    }


def masks_doc(name, coef, M, script):
    masks = matrix_to_masks(M)
    d = matrix_doc(name, coef, M, script)
    return {
        "provenance": d["provenance"],
        "n_targets": 32,
        "target_masks": masks,
        "target_masks_hex": [f"0x{m:08x}" for m in masks],
        "weights": [bin(m).count("1") for m in masks],
    }


# ------------------------------------------------------------------- controls
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.dirname(os.path.abspath(__file__)))
    a = ap.parse_args()
    script = 'wrapup/phase2/spec/derive_invmc.py'
    log = []

    def say(s=''):
        print(s)
        log.append(s)

    say("=" * 74)
    say("derive_invmc.py -- AES InvMixColumns from first principles")
    say("=" * 74)
    say(f"field modulus        0x{AES_MODULUS:03X}")
    say(f"forward  coefficients {[hex(c) for c in FWD_COEF]}  = {FWD_COEF}")
    say(f"inverse  coefficients {[hex(c) for c in INV_COEF]}  = {INV_COEF}")
    say()

    Mf = build_matrix(FWD_COEF)
    Mi = build_matrix(INV_COEF)
    mf = matrix_to_masks(Mf)
    mi = matrix_to_masks(Mi)
    ok = True

    # ---- C1 : forward control vs the two independent in-repo derivations
    say("-- C1  forward derivation vs the repo's own spec code " + "-" * 20)
    sys.path.insert(0, ROOT)
    from verify_circuit import mixcolumns_target_masks as oracle_spec
    ref = oracle_spec()
    diffs = [(r, mf[r], ref[r]) for r in range(32) if mf[r] != ref[r]]
    say(f"   verify_circuit.mixcolumns_target_masks(): 32 masks")
    say(f"   differing rows: {len(diffs)}")
    for r, a1, b1 in diffs[:8]:
        say(f"     row {r}: derived 0x{a1:08x} != oracle 0x{b1:08x}")
    ok &= (not diffs)
    say(f"   C1a verify_circuit.py           : {'PASS' if not diffs else 'FAIL'}")

    sys.path.insert(0, os.path.join(ROOT, 'fleet8/unified/code'))
    try:
        import theory
        d2 = [r for r in range(32) if mf[r] != theory.TARGET_MASKS[r]]
        say(f"   C1b fleet8 theory.TARGET_MASKS  : {'PASS' if not d2 else 'FAIL'}"
            f"  (differing rows: {len(d2)})")
        ok &= (not d2)
    except Exception as e:                                  # pragma: no cover
        say(f"   C1b theory.py unavailable: {e}")
        ok = False

    # full row-by-row transcript of the forward diff (banked)
    say("   full forward transcript (row: derived | oracle | equal):")
    for r in range(32):
        say(f"     {r:2d}  0x{mf[r]:08x}  0x{ref[r]:08x}  {'==' if mf[r] == ref[r] else '!!'}")
    say()

    # ---- C4 : the oracle's own weight self-check
    w = [bin(m).count("1") for m in mf]
    c4 = (w.count(5) == 20 and w.count(7) == 12)
    say(f"-- C4  forward weight profile: 5->{w.count(5)}  7->{w.count(7)}"
        f"   expect 20 / 12 : {'PASS' if c4 else 'FAIL'}")
    ok &= c4

    # ---- C2 : the two matrices are mutually inverse over GF(2)
    say("-- C2  M_fwd * M_inv == I  and  M_inv * M_fwd == I " + "-" * 22)
    I = identity()
    p1 = mat_mul(Mf, Mi)
    p2 = mat_mul(Mi, Mf)
    c2a, c2b = mat_eq(p1, I), mat_eq(p2, I)
    say(f"   M_fwd*M_inv == I : {'PASS' if c2a else 'FAIL'}"
        f"   (off-identity ones: {density([[p1[i][j] ^ I[i][j] for j in range(32)] for i in range(32)])})")
    say(f"   M_inv*M_fwd == I : {'PASS' if c2b else 'FAIL'}")
    ok &= c2a and c2b

    # ---- C3 : InvMixColumns == MixColumns^3
    say("-- C3  M_fwd^3 == M_inv  (c(y)^4 == 1 in F[y]/(y^4+1)) " + "-" * 18)
    M3 = mat_mul(mat_mul(Mf, Mf), Mf)
    c3 = mat_eq(M3, Mi)
    say(f"   M_fwd^3 == M_inv : {'PASS' if c3 else 'FAIL'}")
    M4 = mat_mul(M3, Mf)
    say(f"   M_fwd^4 == I     : {'PASS' if mat_eq(M4, I) else 'FAIL'}  (order of c divides 4)")
    say(f"   M_fwd^2 == I     : {'PASS(!)' if mat_eq(mat_mul(Mf, Mf), I) else 'no (order is exactly 4)'}")
    ok &= c3

    # ---- structural readout
    say()
    say("-- structure " + "-" * 60)
    wf, wi = [sum(r) for r in Mf], [sum(r) for r in Mi]
    say(f"   forward  rank {gf2_rank(Mf)}   density {density(Mf)}   "
        f"row weights: min {min(wf)} max {max(wf)} mean {density(Mf)/32:.3f}")
    say(f"   inverse  rank {gf2_rank(Mi)}   density {density(Mi)}   "
        f"row weights: min {min(wi)} max {max(wi)} mean {density(Mi)/32:.3f}")
    from collections import Counter
    say(f"   forward  weight histogram {dict(sorted(Counter(wf).items()))}")
    say(f"   inverse  weight histogram {dict(sorted(Counter(wi).items()))}")
    say(f"   naive XOR-tree cost (sum popcount - 32):"
        f"   forward {density(Mf) - 32}   inverse {density(Mi) - 32}")
    say(f"   coefficient popcounts: forward {[bin(c).count('1') for c in FWD_COEF]}"
        f"   inverse {[bin(c).count('1') for c in INV_COEF]}")

    # ---- emit
    os.makedirs(a.out, exist_ok=True)
    files = {
        'invmc_matrix.json': matrix_doc('aes_inv_mixcolumns', INV_COEF, Mi, script),
        'invmc_target_masks.json': masks_doc('aes_inv_mixcolumns', INV_COEF, Mi, script),
        'mixcolumns_matrix.json': matrix_doc('aes_mixcolumns', FWD_COEF, Mf, script),
        'mixcolumns_target_masks.json': masks_doc('aes_mixcolumns', FWD_COEF, Mf, script),
    }
    say()
    say("-- emitted " + "-" * 63)
    for fn, doc in files.items():
        p = os.path.join(a.out, fn)
        with open(p, 'w') as f:
            json.dump(doc, f, indent=1)
            f.write('\n')
        say(f"   {p}")
        say(f"     rows_sha256 {doc['provenance']['rows_sha256']}")

    say()
    say("=" * 74)
    say("ALL CONTROLS PASS" if ok else "CONTROL FAILURE")
    say("=" * 74)
    with open(os.path.join(a.out, 'derivation_transcript.txt'), 'w') as f:
        f.write('\n'.join(log) + '\n')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
