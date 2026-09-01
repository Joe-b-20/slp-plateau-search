#!/usr/bin/env python3
"""instance_facts.py -- report the checkable facts about a shipped instance.

    python3 code/instance_facts.py
    python3 code/instance_facts.py --instance positive_control/instance_SUB_U4tgts.json --no-pin

Prints, all computed and none asserted:

  r, m, t          rank, number of distinct non-zero free signals, targets
  lower_bound_L2   the encoder's admissible combinatorial lower bound.  It is a
                   PROVED bound (see the (L2) proof in code/slp_opt.py's
                   docstring): distinct target values need distinct gates, and a
                   target whose value needs d inputs cannot sit before position
                   d.  This is what makes the UNSAT ladder start at k = L2 and
                   not lower -- the symmetry-broken CNF is not by itself
                   monotone in k, so the ladder needs a floor it did not solve
                   for.
  greedy_upper     a program found by the encoder's own greedy heuristic, and
                   whether replaying it actually computes every target.  This is
                   the sanity control that the instance is solvable at all.
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from instance_io import load_slp_opt, load_instance  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", default=None)
    ap.add_argument("--no-pin", action="store_true")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    SO = load_slp_opt()
    instd, checks = load_instance(a.instance, pin=not a.no_pin)
    inst = SO.Instance(instd["dim"], instd["inputs"], instd["targets"])

    d0 = SO.delta_array(inst.r, inst.in_vals)
    lb = int(SO.lower_bound(d0, inst.tgt_vals))

    _, ub = SO.greedy_upper_bound(inst)
    gates = SO.internal_to_original(inst, ub)
    good, why = SO.verify_slp(instd["inputs"], instd["targets"], gates)

    rep = {
        "instance": checks,
        "rank_r": inst.r,
        "free_signals_m": inst.m,
        "targets_unrealised": len(inst.tgt_vals),
        "lower_bound_L2": lb,
        "greedy_upper_bound": len(gates),
        "greedy_verify_slp": bool(good),
        "greedy_why": why,
    }
    print(json.dumps(rep, indent=1))
    if a.json:
        json.dump(rep, open(a.json, "w"), indent=1)
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
