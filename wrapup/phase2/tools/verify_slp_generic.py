#!/usr/bin/env python3
"""Standalone independent verifier for an XOR circuit against ANY GF(2) target.

This is `verify_circuit.py` (repo root) with the built-in MixColumns spec
replaced by a target-matrix file.  Everything else is preserved verbatim:
the accepted circuit encodings, the replay semantics, the printed line
format, the VERDICT line, the exit code.

TRUST NOTHING.  The oracle never believes a mask list:

  1. the matrix file MUST carry a `provenance` header (name, field, modulus,
     mds_column, convention, rows_sha256).  No header => REFUSED, exit 3.
  2. the target masks are REBUILT from `rows` (the 32x32 bit matrix), never
     read from the file's own `masks_hex` / `target_masks` field -- those are
     recomputed and cross-checked, and a mismatch is REFUSED.
  3. `rows_sha256` is recomputed over the rows and must match the header.
  4. if the header declares `mds_column` + `modulus`, the whole matrix is
     RE-DERIVED from GF(2^8) here, in this file, and must equal `rows`.
     That is the property that made the original oracle the definition of
     VALID: the spec IS this code, not a table someone typed.
  5. the target must have full GF(2) rank over its 32 inputs.

Accepted circuit encodings (unchanged from verify_circuit.py):
  A) {"gates": [[a,b], ...]}             index pairs; inputs are signals 0..31,
                                         gate k produces signal 32+k = sig[a]^sig[b]
  B) {"gates": [{"m":..,"a":..,"b":..}]} mask triples in build order (a^b==m)
  C) {"gateCount":..,"gates":[[a,b]..],"outputSignals":[..]}
  D) a bare list  [[a,b], ...]           same as A

Usage:  python3 verify_slp_generic.py --target <matrix.json> <circuit.json> [max_depth]
        python3 verify_slp_generic.py <matrix.json> <circuit.json> [max_depth]
Exit 0 iff all outputs correct (and depth<=max_depth if given).
Exit 1 invalid circuit.  Exit 2 usage.  Exit 3 target file refused.
"""
import hashlib
import json
import sys


# --------------------------------------------------------------- GF(2^8) spec
def xtime(a, modulus):
    a <<= 1
    return (a ^ modulus) & 0xFF if (a & 0x100) else (a & 0xFF)


def gf_mul(a, b, modulus):
    r = 0
    for i in range(8):
        if (b >> i) & 1:
            t = a
            for _ in range(i):
                t = xtime(t, modulus)
            r ^= t
    return r & 0xFF


def build_circulant_matrix(coef, modulus):
    """The repo convention, verbatim: out row 8*col+out_bit, in col 8*ib+in_bit,
    LSB-first inside each byte, out_byte[col] = XOR_k coef[k]*in_byte[(col+k)%4]."""
    M = [[0] * 32 for _ in range(32)]
    for col in range(4):
        for k in range(4):
            c, ib = coef[k], (col + k) % 4
            for in_bit in range(8):
                v = gf_mul(c, 1 << in_bit, modulus)
                for out_bit in range(8):
                    if (v >> out_bit) & 1:
                        M[col * 8 + out_bit][ib * 8 + in_bit] ^= 1
    return M


def gf2_rank(rows_int, nbits):
    rows = list(rows_int)
    rank = 0
    for bit in range(nbits):
        p = next((i for i in range(rank, len(rows)) if (rows[i] >> bit) & 1), None)
        if p is None:
            continue
        rows[rank], rows[p] = rows[p], rows[rank]
        for i in range(len(rows)):
            if i != rank and (rows[i] >> bit) & 1:
                rows[i] ^= rows[rank]
        rank += 1
    return rank


# ------------------------------------------------------------- target loading
REQUIRED_PROVENANCE = ("name", "field", "modulus", "convention", "rows_sha256")


class Refused(Exception):
    pass


def load_target(path):
    """Returns (masks, n_inputs, info dict).  Raises Refused on any doubt."""
    with open(path) as f:
        doc = json.load(f)
    if not isinstance(doc, dict):
        raise Refused("target file is not a JSON object")
    prov = doc.get("provenance")
    if not isinstance(prov, dict):
        raise Refused("target file has no `provenance` header "
                      "(a bare mask list is not a specification)")
    missing = [k for k in REQUIRED_PROVENANCE if k not in prov]
    if missing:
        raise Refused(f"provenance header missing fields: {missing}")
    rows = doc.get("rows")
    if not isinstance(rows, list) or not rows:
        raise Refused("target file has no `rows` matrix")
    n_in = doc.get("n_inputs", len(rows[0]))
    for r, s in enumerate(rows):
        if not isinstance(s, str) or len(s) != n_in or set(s) - set("01"):
            raise Refused(f"row {r} is not a {n_in}-character 0/1 string")

    # (3) rows digest
    dig = hashlib.sha256('\n'.join(rows).encode()).hexdigest()
    if dig != prov["rows_sha256"]:
        raise Refused(f"rows_sha256 mismatch: computed {dig}, header says "
                      f"{prov['rows_sha256']}")

    # (2) masks REBUILT from rows; the file's own mask list is only cross-checked
    masks = [sum(1 << c for c in range(n_in) if s[c] == '1') for s in rows]
    for key, conv in (("masks_hex", lambda x: int(x, 16)),
                      ("target_masks", int),
                      ("target_masks_hex", lambda x: int(x, 16))):
        if key in doc:
            stated = [conv(x) for x in doc[key]]
            if stated != masks:
                bad = [i for i in range(min(len(stated), len(masks)))
                       if stated[i] != masks[i]]
                raise Refused(f"`{key}` disagrees with the rebuilt rows at "
                              f"{len(bad)} position(s), first {bad[:4]}")

    # (4) re-derive from the field, if the header says how
    rederived = "not declared"
    if "mds_column" in prov and len(rows) == 32 and n_in == 32:
        M = build_circulant_matrix(prov["mds_column"], int(prov["modulus"]))
        want = [''.join(str(b) for b in row) for row in M]
        if want != rows:
            bad = [i for i in range(32) if want[i] != rows[i]]
            raise Refused(f"rows do NOT match a from-scratch GF(2^8) derivation "
                          f"from mds_column={prov['mds_column']} modulus="
                          f"0x{int(prov['modulus']):X}; {len(bad)} bad rows, "
                          f"first {bad[:4]}")
        rederived = (f"from GF(2^8)/0x{int(prov['modulus']):X} column "
                     f"{[hex(c) for c in prov['mds_column']]}")

    # (5) rank
    rank = gf2_rank(masks, n_in)
    if rank != n_in:
        raise Refused(f"target has GF(2) rank {rank} < {n_in} inputs")

    if len(set(masks)) != len(masks):
        raise Refused("target mask list contains duplicates")

    return masks, n_in, {"name": prov["name"], "rederived": rederived,
                         "rank": rank, "sha256": dig,
                         "density": sum(bin(m).count("1") for m in masks)}


# ---------------------------------------------------- circuit loading (verbatim)
def load_index_pairs(data):
    """Normalize any accepted encoding to a list of index pairs [a,b] where
    signals 0..31 are inputs and gate k yields signal 32+k."""
    if isinstance(data, list):
        gates = data
    else:
        gates = data["gates"]
    if gates and isinstance(gates[0], dict):
        idx = {(1 << i): i for i in range(32)}
        pairs = []
        for g in gates:
            m, a, b = g["m"] & 0xFFFFFFFF, g["a"] & 0xFFFFFFFF, g["b"] & 0xFFFFFFFF
            if a not in idx or b not in idx:
                raise SystemExit(f"gate {len(pairs)}: parent signal not yet built "
                                 f"({a:#x} or {b:#x})")
            pairs.append([idx[a], idx[b]])
            if m not in idx:
                idx[m] = 31 + len(pairs)
        return pairs
    return [list(g) for g in gates]


def usage():
    print("usage: python3 verify_slp_generic.py --target <matrix.json> "
          "<circuit.json> [max_depth]")
    print()
    print("  <matrix.json>   target specification with a provenance header,")
    print("                  e.g. wrapup/phase2/spec/invmc_matrix.json")
    print("  <circuit.json>  path to a circuit file. Accepted encodings:")
    print('                    {"gates": [[a,b], ...]}       index pairs; signals 0..31')
    print("                                                  are inputs, gate k -> signal 32+k")
    print('                    {"gates": [{"m","a","b"},..]} mask triples in build order')
    print("                    [[a,b], ...]                  a bare list of index pairs")
    print("  [max_depth]     optional integer; also FAIL if circuit depth exceeds it")
    print()
    print("  examples:")
    print("    python3 verify_slp_generic.py --target wrapup/phase2/spec/mixcolumns_matrix.json \\")
    print("            evidence/circuits/mixcolumns_88gates_depth5.json 5")
    sys.exit(2)


def main():
    argv = sys.argv[1:]
    if not argv:
        usage()
    if argv[0] == "--target":
        argv = argv[1:]
    if len(argv) < 2:
        usage()
    tgt_path, path = argv[0], argv[1]
    max_depth = int(argv[2]) if len(argv) > 2 else None

    try:
        spec, n_in, info = load_target(tgt_path)
    except Refused as e:
        print(f"target={tgt_path}")
        print(f"REFUSED: {e}")
        print("VERDICT: TARGET REFUSED")
        sys.exit(3)

    print(f"target={info['name']} inputs={n_in} outputs={len(spec)} "
          f"rank={info['rank']} density={info['density']} "
          f"rows_sha256={info['sha256'][:16]}")
    print(f"target rebuilt: {info['rederived']}")

    targets = set(spec)
    pairs = load_index_pairs(json.load(open(path)))
    sig = [1 << i for i in range(n_in)]
    depth = [0] * n_in
    problems = []
    for k, g in enumerate(pairs):
        if len(g) != 2:
            problems.append(f"gate {k} not 2-input"); sig.append(0); depth.append(0); continue
        a, b = g
        idx = n_in + k
        if not (0 <= a < idx and 0 <= b < idx):
            problems.append(f"gate {k} references non-earlier signal")
            sig.append(0); depth.append(0); continue
        sig.append(sig[a] ^ sig[b])
        depth.append(max(depth[a], depth[b]) + 1)
    built = sum(1 for t in spec if t in set(sig))
    D = max(depth) if depth else 0
    ok = (built == len(spec)) and not problems and (max_depth is None or D <= max_depth)
    print(f"gates={len(pairs)} depth={D} outputs_built={built}/{len(spec)} "
          f"problems={len(problems)}")
    for p in problems[:8]:
        print("  -", p)
    if max_depth is not None:
        print(f"depth<= {max_depth}: {'OK' if D <= max_depth else 'VIOLATED'}")
    print("VERDICT:", f"VALID {info['name']} circuit" if ok else "INVALID")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
