#!/usr/bin/env python3
"""N3 -- InvMixColumns = MixColumns^3 at the CIRCUIT level.

Chains three copies of the record 88-gate MixColumns circuit and emits the
result as an InvMixColumns circuit.  This is a free upper bound (any n-gate
MixColumns circuit gives a 3n-gate InvMixColumns circuit) and it is also an
independent, circuit-level confirmation of the matrix identity M_fwd^3 = M_inv
checked algebraically in spec/derive_invmc.py (control C3).

Run:  python3 make_composition_circuit.py
Then: python3 ../tools/verify_slp_generic.py --target ../spec/invmc_matrix.json \
              ../circuits/invmc_from_mc_cubed_264.json
"""
import json
import os
import sys

R = '/home/joebachir20/xor_ui/slp-plateau-search'
P = os.path.join(R, 'wrapup/phase2')
sys.path.insert(0, os.path.join(P, 'tools'))
from baseline_naive import strip_dead, depth_of            # noqa: E402
from verify_slp_generic import load_target, load_index_pairs  # noqa: E402

BASE = os.path.join(R, 'evidence/circuits/mixcolumns_88gates_depth5.json')
OUT = os.path.join(P, 'circuits/invmc_from_mc_cubed_264.json')

print("N3  InvMixColumns = MixColumns^3 at the CIRCUIT level")
print(f"    base: {BASE}")
pairs = load_index_pairs(json.load(open(BASE)))
fwd, _, _ = load_target(os.path.join(P, 'spec/mixcolumns_matrix.json'))
inv, _, _ = load_target(os.path.join(P, 'spec/invmc_matrix.json'))

gates = []
cur = list(range(32))                     # global signal index of each stage input
for stage in range(3):
    loc2glob = {i: cur[i] for i in range(32)}
    for k, (a, b) in enumerate(pairs):
        gates.append([loc2glob[a], loc2glob[b]])
        loc2glob[32 + k] = 32 + len(gates) - 1
    sig = [1 << i for i in range(32)]
    for a, b in pairs:
        sig.append(sig[a] ^ sig[b])
    pos = {}
    for i, s in enumerate(sig):
        pos.setdefault(s, i)
    cur = [loc2glob[pos[t]] for t in fwd]   # stage outputs, in target order
    print(f"    stage {stage + 1}: cumulative gates {len(gates)}")

gates = strip_dead(gates, inv, 32)
json.dump({"gates": gates,
           "provenance": {
               "tool": "wrapup/phase2/controls/make_composition_circuit.py",
               "method": "three chained copies of "
                         "evidence/circuits/mixcolumns_88gates_depth5.json",
               "fact": "InvMixColumns = MixColumns^3 in GF(2^8)[y]/(y^4+1)",
               "gates": len(gates), "depth": depth_of(gates, 32)}},
          open(OUT, 'w'), indent=1)
print(f"    emitted {OUT}: {len(gates)} gates, depth {depth_of(gates, 32)}")
