#!/usr/bin/env python3
"""Standalone independent verifier for an AES MixColumns XOR circuit.

Rebuilds MixColumns from GF(2^8) (the spec IS this code), then replays a
circuit and reports: gate count, depth, how many of the 32 outputs are built,
and whether it is a fully valid MixColumns circuit.

Accepts several circuit encodings in the input JSON file:
  A) {"gates": [[a,b], ...]}            index pairs; inputs are signals 0..31,
                                        gate k produces signal 32+k = sig[a]^sig[b]
  B) {"gates": [{"m":..,"a":..,"b":..}]} mask triples in build order (a^b==m)
  C) {"gateCount":..,"gates":[[a,b]..],"outputSignals":[..]}  (kit circuits/ format)
  D) a bare list  [[a,b], ...]          same as A

Usage:  python3 verify_circuit.py <circuit.json> [max_depth]
Exit 0 iff all 32 outputs correct (and depth<=max_depth if given).
"""
import json, sys


def xtime(a):
    a <<= 1
    return (a ^ 0x11B) & 0xFF if (a & 0x100) else (a & 0xFF)


def gf_mul(a, b):
    r = 0
    for i in range(8):
        if (b >> i) & 1:
            t = a
            for _ in range(i):
                t = xtime(t)
            r ^= t
    return r & 0xFF


def mixcolumns_target_masks():
    coef = [2, 3, 1, 1]
    M = [[0] * 32 for _ in range(32)]
    for col in range(4):
        for k in range(4):
            c, ib = coef[k], (col + k) % 4
            for in_bit in range(8):
                v = gf_mul(c, 1 << in_bit)
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


def load_index_pairs(data):
    """Normalize any accepted encoding to a list of index pairs [a,b] where
    signals 0..31 are inputs and gate k yields signal 32+k."""
    if isinstance(data, list):
        gates = data
    else:
        gates = data["gates"]
    if gates and isinstance(gates[0], dict):
        # mask triples -> rebuild index pairs
        idx = {(1 << i): i for i in range(32)}
        pairs = []
        for g in gates:
            m, a, b = g["m"] & 0xFFFFFFFF, g["a"] & 0xFFFFFFFF, g["b"] & 0xFFFFFFFF
            if a not in idx or b not in idx:
                raise SystemExit(f"gate {len(pairs)}: parent signal not yet built ({a:#x} or {b:#x})")
            pairs.append([idx[a], idx[b]])
            if m not in idx:
                idx[m] = 31 + len(pairs)
        return pairs
    return [list(g) for g in gates]


def main():
    if len(sys.argv) < 2:
        print("usage: python3 verify_circuit.py <circuit.json> [max_depth]")
        print()
        print("  <circuit.json>  path to a circuit file. Accepted encodings:")
        print('                    {"gates": [[a,b], ...]}       index pairs; signals 0..31')
        print("                                                  are inputs, gate k -> signal 32+k")
        print('                    {"gates": [{"m","a","b"},..]} mask triples in build order')
        print("                    [[a,b], ...]                  a bare list of index pairs")
        print("  [max_depth]     optional integer; also FAIL if circuit depth exceeds it")
        print()
        print("  examples:")
        print("    python3 verify_circuit.py evidence/circuits/mixcolumns_89gates_depth5.json 5")
        print("    python3 verify_circuit.py reproduce/out_97.json 3")
        sys.exit(2)
    path = sys.argv[1]
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else None
    spec = mixcolumns_target_masks()
    wts = [bin(m).count("1") for m in spec]
    assert wts.count(5) == 20 and wts.count(7) == 12, "spec self-check failed"
    targets = set(spec)

    pairs = load_index_pairs(json.load(open(path)))
    sig = [1 << i for i in range(32)]
    depth = [0] * 32
    problems = []
    for k, g in enumerate(pairs):
        if len(g) != 2:
            problems.append(f"gate {k} not 2-input"); sig.append(0); depth.append(0); continue
        a, b = g
        idx = 32 + k
        if not (0 <= a < idx and 0 <= b < idx):
            problems.append(f"gate {k} references non-earlier signal"); sig.append(0); depth.append(0); continue
        sig.append(sig[a] ^ sig[b])
        depth.append(max(depth[a], depth[b]) + 1)
    built = sum(1 for t in spec if t in set(sig))
    D = max(depth) if depth else 0
    ok = (built == 32) and not problems and (max_depth is None or D <= max_depth)
    print(f"gates={len(pairs)} depth={D} outputs_built={built}/32 problems={len(problems)}")
    for p in problems[:8]:
        print("  -", p)
    if max_depth is not None:
        print(f"depth<= {max_depth}: {'OK' if D <= max_depth else 'VIOLATED'}")
    print("VERDICT:", "VALID MixColumns circuit" if ok else "INVALID")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
