#!/usr/bin/env python3
"""Is a circuit's depth a property of its VALUE SET, or of its build order?

For each shipped circuit this prints two numbers:

  measured  - the depth the circuit actually has, from the standalone verifier
  ASAP      - the depth of the as-soon-as-possible least-fixpoint schedule over
              that circuit's mask set, which is the SHALLOWEST schedule ANY
              circuit on that mask set admits

If the two are equal, the circuit is already as shallow as its own value set
permits and no rescheduling can make it shallower.  Rebuilding the wiring is
then not a route to a lower depth: only changing the value set is.

Stdlib only.  Run from the repository root:

    python3 corpus/depth_forced/asap_depth.py

Exit 0 iff measured == ASAP for every circuit.
"""
import os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import mixcolumns_core as core
import engines as E

CIRC = os.path.join(ROOT, "evidence", "circuits")
TIDX = {m: i for i, m in enumerate(core.TARGETS)}


def asap(masks):
    """Least-fixpoint ASAP depth over a mask set, and the depth profile.

    engines.relax computes, for every available value, the smallest depth at
    which it can be produced from the inputs using only values in the set.  It
    is a least fixpoint, so no build order over this mask set can do better.
    """
    avail = list(core.INPUTS) + list(masks)
    dep, _ = E.relax(avail)
    real = [dep[i] for i in range(32, len(avail))]
    prof = {}
    for d in real:
        prof[d] = prof.get(d, 0) + 1
    crit = sorted(TIDX[avail[i]] for i in range(32, len(avail))
                  if avail[i] in TIDX and dep[i] == max(real))
    return max(real), prof, crit


def main():
    files = sorted(f for f in os.listdir(CIRC)
                   if f.endswith(".json") and f != "spectrum.json")
    bad = 0
    print("%-46s %5s %9s %5s  %s" % ("circuit", "gates", "measured", "ASAP", "verdict"))
    print("-" * 96)
    for f in files:
        masks = list(core.load_circuit_masks(os.path.join(CIRC, f)))
        with open(os.path.join(CIRC, f)) as fh:
            v = core.verify(json.load(fh)["gates"])
        a, prof, crit = asap(masks)
        ok = (a == v["depth"])
        bad += not ok
        print("%-46s %5d %9d %5d  %s" %
              (f, len(masks), v["depth"], a,
               "already minimal" if ok else "*** RESCHEDULABLE ***"))
        print("      depth profile %s" % sorted(prof.items()))
        print("      output rows pinned at the top level: %s" % crit)
    print("-" * 96)
    if bad:
        print("%d circuit(s) could be made shallower by rescheduling alone." % bad)
    else:
        print("All %d circuits sit at the shallowest depth their own mask set "
              "admits." % len(files))
        print("Depth here is a property of the value set, not of the build order:")
        print("no rewiring makes any of them shallower.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
