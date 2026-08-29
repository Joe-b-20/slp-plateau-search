#!/usr/bin/env python3
"""Stage the depth-4 record circuit for ~/xor_ui/aes_mc_records.

READ-ONLY against both repositories. Writes exactly one file, into this
drafts directory: mixcolumns_91gates_depth4.json.

Source circuit:
  ~/xor_ui/slp-plateau-search/campaign_87/cascade6/FRONTIER_91gates_depth4.json

The source carries gateCount/gates/depth/provenance but NOT the records-repo
schema keys (id, model, inputCount, outputSignals, outputConvention).
outputSignals is DERIVED here from the MixColumns specification rebuilt from
GF(2^8) -- the same specification verify.py builds -- by locating, for each
target mask, a signal whose dependency mask equals it.

Then every check in ~/xor_ui/aes_mc_records/verify.py is re-run against the
staged file, plus the two SHA-256 fields the repo's bounds.json schema needs.
"""
import hashlib
import json
import os

SRC = os.path.expanduser(
    "~/xor_ui/slp-plateau-search/campaign_87/cascade6/FRONTIER_91gates_depth4.json"
)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "mixcolumns_91gates_depth4.json")

MODEL = ("2-input XOR circuit over GF(2). Signals 0..31 are the 32 input bits. "
         "Gate k (k>=0) produces signal 32+k = signal[gates[k][0]] XOR "
         "signal[gates[k][1]]. Both parents have strictly smaller index.")
OUTCONV = ("output j (j in 0..31) is MixColumns output bit j; bit j = bit "
           "(j mod 8) of state byte (j div 8), least-significant-bit-first "
           "within each byte. It is produced at internal signal index "
           "outputSignals[j].")


# --- spec rebuilt from GF(2^8), byte-identical to aes_mc_records/verify.py ---
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


def canonical_gate_hash(gates):
    canon = json.dumps({"inputCount": 32, "gates": gates}, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def simulate(gates, n_in=32):
    sig = [1 << i for i in range(n_in)]
    depth = [0] * n_in
    for a, b in gates:
        sig.append(sig[a] ^ sig[b])
        depth.append(max(depth[a], depth[b]) + 1)
    return sig, depth


def main():
    spec = mixcolumns_target_masks()
    wts = [bin(m).count("1") for m in spec]
    assert wts.count(5) == 20 and wts.count(7) == 12, "spec self-check failed"
    print("AES MixColumns rebuilt from GF(2^8): weight profile 20x5 + 12x7  [OK]")

    src = json.load(open(SRC))
    gates = [list(g) for g in src["gates"]]
    sig, depth = simulate(gates)

    # derive outputSignals: latest signal carrying each target mask (unique here)
    outs = []
    for j in range(32):
        hits = [i for i, s in enumerate(sig) if s == spec[j]]
        assert hits, f"output {j}: no signal carries the target mask"
        outs.append(hits[-1])
    print(f"outputSignals derived: 32/32 targets located "
          f"(min {min(outs)}, max {max(outs)})")

    circuit = {
        "id": "mixcolumns_91gates_depth4",
        "model": MODEL,
        "inputCount": 32,
        "gateCount": len(gates),
        "depth": max(depth),
        "gates": gates,
        "outputSignals": outs,
        "outputConvention": OUTCONV,
    }
    with open(OUT, "w") as f:
        f.write(json.dumps(circuit, indent=1))
        f.write("\n")

    # ---- re-run every verify.py check against the staged bytes ----
    raw = open(OUT, "rb").read()
    data = json.loads(raw)
    g2 = data["gates"]
    sig2, depth2 = simulate(g2, data["inputCount"])
    problems = []
    for k, g in enumerate(g2):
        if len(g) != 2:
            problems.append(f"gate {k} is not 2-input")
        a, b = g
        if not (0 <= a < 32 + k and 0 <= b < 32 + k):
            problems.append(f"gate {k} references a non-earlier signal")
    for j in range(32):
        if sig2[data["outputSignals"][j]] != spec[j]:
            problems.append(f"output {j} wrong")
    if data["gateCount"] != len(g2):
        problems.append("gateCount mismatch")
    if data["depth"] != max(depth2):
        problems.append("depth mismatch")

    print(f"structural (2-input XOR, parents strictly earlier): "
          f"{'OK' if not problems else 'FAIL'}")
    print(f"gateCount declared {data['gateCount']} == actual {len(g2)}")
    print(f"depth declared {data['depth']} == measured {max(depth2)}")
    print(f"outputs correct: {sum(1 for j in range(32) if sig2[data['outputSignals'][j]] == spec[j])}/32")
    print(f"live gates (reverse-reachable from outputs): {live_count(g2, data['outputSignals'])}/{len(g2)}")
    print(f"distinct gate masks: {len(set(sig2[32:]))}/{len(g2)}")
    print()
    print(f"sha256_circuit_json    = {hashlib.sha256(raw).hexdigest()}")
    print(f"sha256_canonical_gates = {canonical_gate_hash(g2)}")
    print()
    print("ALL CHECKS PASS." if not problems else f"PROBLEMS: {problems[:6]}")


def live_count(gates, outs):
    n = 32 + len(gates)
    live = set(outs)
    for k in range(len(gates) - 1, -1, -1):
        if 32 + k in live:
            live.update(gates[k])
    return sum(1 for k in range(len(gates)) if 32 + k in live)


if __name__ == "__main__":
    main()
