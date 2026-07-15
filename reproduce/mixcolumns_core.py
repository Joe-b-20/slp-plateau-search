#!/usr/bin/env python3
"""
mixcolumns_core.py  --  shared math + verification for the reproducers.

This module holds the parts that are pure fact, not tuning: the AES MixColumns
specification (rebuilt from GF(2^8)), a couple of bit helpers, and the
independent verifier used as the ground-truth oracle for every method.

There are NO tunable parameters in this file.  All knobs live in the CONFIG
block at the top of reproduce.py.  Import from here; don't edit here.

A "circuit" throughout this project is a list of index pairs:
    gates = [[a, b], ...]
where signals 0..31 are the inputs x0..x31 (signal i has mask 1<<i) and gate k
produces signal 32+k whose mask = sig[a] ^ sig[b].  Both parents must be
earlier signals (index < 32+k).
"""
import json

# --------------------------------------------------------------------------
# AES MixColumns specification, rebuilt from GF(2^8) so the spec IS this code.
# (Same derivation the standalone verifier uses.)
# --------------------------------------------------------------------------
def _xtime(a):
    """Multiply a byte by 2 in GF(2^8) mod 0x11B (the AES field)."""
    a <<= 1
    return (a ^ 0x11B) & 0xFF if (a & 0x100) else (a & 0xFF)


def _gf_mul(a, b):
    """Multiply two bytes in GF(2^8)."""
    r = 0
    for i in range(8):
        if (b >> i) & 1:
            t = a
            for _ in range(i):
                t = _xtime(t)
            r ^= t
    return r & 0xFF


def mixcolumns_masks():
    """Return the 32 MixColumns output masks y0..y31.

    Bit i of a mask means "input x_i feeds this output".  Bit index i = bit
    (i mod 8) of state byte (i div 8), least-significant-bit first.  Built
    directly from the column matrix [2,3,1,1] over GF(2^8).
    """
    coef = [2, 3, 1, 1]
    M = [[0] * 32 for _ in range(32)]
    for col in range(4):                       # output byte
        for k in range(4):                     # input byte (col+k)%4, coeff coef[k]
            c, ib = coef[k], (col + k) % 4
            for in_bit in range(8):
                v = _gf_mul(c, 1 << in_bit)
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


TARGETS = mixcolumns_masks()          # the 32 outputs, as bit-masks
TARGET_SET = frozenset(TARGETS)
INPUTS = [1 << i for i in range(32)]  # the 32 input signals
INPUT_SET = frozenset(INPUTS)

# self-check: MixColumns has 20 weight-5 and 12 weight-7 outputs
assert sorted(bin(m).count("1") for m in TARGETS).count(5) == 20
assert sorted(bin(m).count("1") for m in TARGETS).count(7) == 12


def bits_of(m):
    """List the set bit positions of mask m (i.e. which inputs it XORs)."""
    return [b for b in range(32) if (m >> b) & 1]


def wt(m):
    """Popcount (Hamming weight) of a mask."""
    return bin(m).count("1")


# --------------------------------------------------------------------------
# The independent verifier / oracle.
# --------------------------------------------------------------------------
def verify(gates, max_depth=None):
    """Replay an index-pair circuit and check it against the MixColumns spec.

    Returns a dict:
        gates    : number of 2-input XOR gates
        depth    : measured circuit depth (inputs are depth 0)
        outputs  : how many of the 32 targets are produced (want 32)
        ok       : True iff all 32 outputs are built, every gate references
                   earlier signals, and (if max_depth given) depth <= max_depth
        problems : list of structural error strings (empty when ok)
    """
    sig = [1 << i for i in range(32)]
    depth = [0] * 32
    problems = []
    for k, g in enumerate(gates):
        if len(g) != 2:
            problems.append("gate %d is not 2-input" % k)
            sig.append(0)
            depth.append(0)
            continue
        a, b = g
        idx = 32 + k
        if not (0 <= a < idx and 0 <= b < idx):
            problems.append("gate %d references a non-earlier signal" % k)
            sig.append(0)
            depth.append(0)
            continue
        sig.append(sig[a] ^ sig[b])
        depth.append(max(depth[a], depth[b]) + 1)
    built = set(sig)
    outputs = sum(1 for t in TARGETS if t in built)
    D = max(depth) if depth else 0
    ok = outputs == 32 and not problems and (max_depth is None or D <= max_depth)
    return {"gates": len(gates), "depth": D, "outputs": outputs,
            "ok": ok, "problems": problems}


def save(gates, path, extra=None):
    """Write an index-pair circuit to JSON as {"gateCount", "gates", ...}."""
    obj = {"gateCount": len(gates), "gates": gates}
    if extra:
        obj.update(extra)
    with open(path, "w") as f:
        json.dump(obj, f)
    return path
