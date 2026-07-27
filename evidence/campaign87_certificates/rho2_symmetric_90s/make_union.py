#!/usr/bin/env python3
"""Union two or more circuits' sigma-symmetrized orbit sets into one seed
circuit JSON (realizable superset; orbit_search will trim+peel it).
Usage: make_union.py out.json in1.json in2.json [...]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mixcolumns_core as core
import engines_relax as ER
from orbit_engine import flatten, state_from_masks

out = sys.argv[1]
reps = set()
for p in sys.argv[2:]:
    reps |= state_from_masks(core.load_circuit_masks(p) | core.TARGET_SET)
F = flatten(reps)
gates = ER.indexpairs_from_masks(F, None)
r = core.verify(gates)
assert r["ok"], r
core.save(gates, out, extra={"depth": r["depth"], "union_of": sys.argv[2:]})
print("union: %d reps, %d gates, depth %d -> %s" % (len(reps), len(F),
                                                    r["depth"], out))
