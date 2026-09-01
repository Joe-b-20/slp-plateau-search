#!/usr/bin/env python3
"""check_cnf.py -- prove a shipped DIMACS file IS the formula the encoder
builds, and (optionally) solve the file itself.

    python3 code/check_cnf.py cnf/k14_joint_W3U4.cnf --k 14
    python3 code/check_cnf.py cnf/k9_joint_W3U4.cnf --k 9 --solve   # UNSAT
    python3 code/check_cnf.py positive_control/k7_SUB_U4tgts.cnf --k 7 \
            --instance positive_control/instance_SUB_U4tgts.json --no-pin

Two independent checks:

 1. ROUND TRIP.  Parse the DIMACS file back into a clause list and compare it
    literal-for-literal, IN ORDER, with a fresh `slp_opt.build_cnf(...)` on the
    same instance and k, and compare the variable counts.  This is what makes
    "the file is the formula" a checked statement instead of an assertion.
    Comments are ignored: they are not part of the formula.

 2. BEHAVIOUR (--solve).  Bootstrap a solver from the clauses PARSED OUT OF THE
    FILE, never from the in-memory object, and report SAT/UNSAT.  Run at a level
    whose verdict is banked, this shows the shipped file behaves like the
    instance that was decided.
"""
import argparse, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from instance_io import (load_slp_opt, load_instance, clause_digest,  # noqa
                         sha256_file)
from solve_dimacs import parse_dimacs                                # noqa


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf")
    ap.add_argument("--k", type=int, required=True)
    ap.add_argument("--instance", default=None)
    ap.add_argument("--no-pin", action="store_true")
    ap.add_argument("--no-symmetry", action="store_true")
    ap.add_argument("--solve", action="store_true")
    ap.add_argument("--solver", default="cadical195")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    SO = load_slp_opt()
    instd, checks = load_instance(a.instance, pin=not a.no_pin)
    inst = SO.Instance(instd["dim"], instd["inputs"], instd["targets"])
    sym = not a.no_symmetry

    nv, ncl, parsed = parse_dimacs(a.cnf)
    cnf, V, Z = SO.build_cnf(inst.r, inst.in_vals, inst.tgt_vals, a.k,
                             symmetry=sym)

    rep = {
        "cnf": os.path.basename(a.cnf),
        "cnf_sha256": sha256_file(a.cnf),
        "header_nv": nv, "header_nclauses": ncl,
        "parsed_nclauses": len(parsed),
        "encoder_nv": cnf.nv, "encoder_nclauses": len(cnf.clauses),
        "header_matches_body": (nv == cnf.nv and ncl == len(parsed)),
        "max_var_used": max((abs(x) for cl in parsed for x in cl), default=0),
        "roundtrip_identical": (parsed == cnf.clauses),
        "clause_order_sha256_file": clause_digest(parsed),
        "clause_order_sha256_encoder": clause_digest(cnf.clauses),
        "instance_checks": checks,
        "k": a.k, "symmetry": sym,
    }
    rep["digests_match"] = (rep["clause_order_sha256_file"] ==
                            rep["clause_order_sha256_encoder"])
    ok = (rep["roundtrip_identical"] and rep["header_matches_body"]
          and rep["digests_match"] and nv == cnf.nv)

    if a.solve:
        from pysat.solvers import Solver
        t0 = time.monotonic()
        with Solver(name=a.solver, bootstrap_with=parsed) as S:
            sat = S.solve()
        rep["solve"] = {"solver": a.solver,
                        "status": "SAT" if sat else "UNSAT",
                        "wall_seconds": round(time.monotonic() - t0, 2),
                        "clauses_from": "the DIMACS FILE, not the encoder"}

    rep["VERDICT"] = "IDENTICAL" if ok else "MISMATCH"
    print(json.dumps(rep, indent=1))
    if a.json:
        json.dump(rep, open(a.json, "w"), indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
