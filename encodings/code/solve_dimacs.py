#!/usr/bin/env python3
"""solve_dimacs.py -- solve a shipped DIMACS file and report the verdict.

Self-contained: it needs Python 3 and `python-sat` (pysat) and nothing else
from this pack.  It exists so that a reader without a compiled kissat/cadical
binary can still reproduce every level in this pack; if you have a binary,
prefer it -- see gen_and_solve.md for the command lines.

    python3 code/solve_dimacs.py cnf/k9_joint_W3U4.cnf
    python3 code/solve_dimacs.py cnf/k9_joint_W3U4.cnf --solver kissat404
    python3 code/solve_dimacs.py positive_control/k7_SUB_U4tgts.cnf \
            --model positive_control/k7_SUB_U4tgts.model

Output is DIMACS-shaped on stdout ("s UNSATISFIABLE" / "s SATISFIABLE" plus
"v" lines when --model is given) with a machine-readable JSON summary written
by --json.  Timing is `time.monotonic`, single solver, one thread.

The clauses handed to the solver are the ones PARSED OUT OF THE FILE, never
rebuilt in memory: this is a measurement of the shipped artifact.
"""
import argparse, hashlib, json, os, sys, time


def parse_dimacs(path):
    """Return (nv, nclauses_from_header, clauses).  Strict: the file must end
    on a clause terminator."""
    nv = ncl = None
    clauses, cur = [], []
    with open(path) as f:
        for line in f:
            if not line or line[0] in "c%":
                continue
            if line[0] == "p":
                parts = line.split()
                nv, ncl = int(parts[2]), int(parts[3])
                continue
            for tok in line.split():
                x = int(tok)
                if x == 0:
                    clauses.append(cur)
                    cur = []
                else:
                    cur.append(x)
    if cur:
        raise SystemExit("dangling clause: the file does not end with a 0")
    return nv, ncl, clauses


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf")
    ap.add_argument("--solver", default="cadical195",
                    help="pysat solver name (cadical195, cadical300, "
                         "kissat404, glucose42, minisat22, ...)")
    ap.add_argument("--model", default=None,
                    help="write the satisfying assignment here (SAT only)")
    ap.add_argument("--json", default=None, help="write a JSON summary here")
    a = ap.parse_args()

    from pysat.solvers import Solver

    nv, ncl, clauses = parse_dimacs(a.cnf)
    used = max((abs(x) for cl in clauses for x in cl), default=0)
    rep = {
        "cnf": os.path.basename(a.cnf),
        "cnf_sha256": sha256(a.cnf),
        "header_nv": nv,
        "header_nclauses": ncl,
        "parsed_nclauses": len(clauses),
        "max_var_used": used,
        "header_matches_body": (ncl == len(clauses) and used <= (nv or 0)),
        "solver": a.solver,
        "clauses_from": "the DIMACS FILE, not an encoder",
    }
    if not rep["header_matches_body"]:
        raise SystemExit("header/body mismatch in %s" % a.cnf)

    t0 = time.monotonic()
    with Solver(name=a.solver, bootstrap_with=clauses) as S:
        sat = S.solve()
        model = S.get_model() if sat else None
    rep["wall_seconds"] = round(time.monotonic() - t0, 2)
    rep["status"] = "SAT" if sat else "UNSAT"

    print("s %s" % ("SATISFIABLE" if sat else "UNSATISFIABLE"))
    if sat and a.model:
        with open(a.model, "w") as f:
            f.write("s SATISFIABLE\n")
            row = []
            for x in model:
                row.append(str(x))
                if len(row) == 20:
                    f.write("v " + " ".join(row) + "\n")
                    row = []
            if row:
                f.write("v " + " ".join(row) + "\n")
            f.write("v 0\n")
        rep["model_file"] = os.path.basename(a.model)
        print("c model written to %s" % a.model)
    print("c solver %s  status %s  seconds %.2f"
          % (a.solver, rep["status"], rep["wall_seconds"]))

    if a.json:
        with open(a.json, "w") as f:
            json.dump(rep, f, indent=1)
            f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
