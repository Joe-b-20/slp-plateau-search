#!/usr/bin/env python3
"""emit_proof.py -- solve a shipped DIMACS file with proof logging on and write
the DRAT refutation.

    python3 code/emit_proof.py cnf/k9_joint_W3U4.cnf --out proofs/k9_joint_W3U4.drat

An UNSAT verdict is a solver's word.  A DRAT proof is a certificate: an
independent checker replays it against the CNF and needs to trust nothing about
the solver that produced it.  This script produces that certificate; checking it
is a separate program and a separate command (see gen_and_solve.md).

The formula handed to the solver is parsed OUT OF THE DIMACS FILE, so the proof
is a refutation of the shipped artifact and not of something rebuilt in memory.

Output is a text DRAT file: one clause per line, terminated by `0`; a line
beginning `d ` deletes a clause.  The empty clause ends the file.  This is what
`drat-trim` and `cake_lpr` consume.

Exits 3 if the formula turns out to be SAT (there is no refutation to write).
"""
import argparse, hashlib, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from solve_dimacs import parse_dimacs, sha256  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cnf")
    ap.add_argument("--out", required=True, help="where to write the DRAT proof")
    ap.add_argument("--solver", default="cadical195",
                    help="a proof-logging pysat solver (cadical195, "
                         "cadical153, glucose42, lingeling)")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    from pysat.solvers import Solver

    nv, ncl, clauses = parse_dimacs(a.cnf)
    rep = {
        "cnf": os.path.basename(a.cnf),
        "cnf_sha256": sha256(a.cnf),
        "nv": nv, "nclauses": len(clauses),
        "solver": a.solver,
        "clauses_from": "the DIMACS FILE, not an encoder",
        "proof_format": "DRAT (text, with deletion lines)",
    }

    t0 = time.monotonic()
    with Solver(name=a.solver, bootstrap_with=clauses, with_proof=True) as S:
        sat = S.solve()
        proof = None if sat else S.get_proof()
    rep["wall_seconds"] = round(time.monotonic() - t0, 2)
    rep["status"] = "SAT" if sat else "UNSAT"

    print("s %s" % ("SATISFIABLE" if sat else "UNSATISFIABLE"))
    if sat:
        print("c SAT: there is no refutation to certify")
        rep["VERDICT"] = "SAT -- no proof written"
        print(json.dumps(rep, indent=1))
        if a.json:
            json.dump(rep, open(a.json, "w"), indent=1)
        return 3

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    h = hashlib.sha256()
    n = 0
    with open(a.out, "w") as f:
        for line in proof:
            line = line.rstrip()
            if not line:
                continue
            b = (line + "\n")
            f.write(b)
            h.update(b.encode())
            n += 1
        if not proof or proof[-1].strip() not in ("0", "0 "):
            f.write("0\n")
            h.update(b"0\n")
            n += 1

    rep["proof_file"] = os.path.basename(a.out)
    rep["proof_lines"] = n
    rep["proof_bytes"] = os.path.getsize(a.out)
    rep["proof_sha256"] = h.hexdigest()
    rep["ends_in_empty_clause"] = True
    rep["VERDICT"] = "DRAT PROOF WRITTEN"

    print("c proof written to %s  (%d lines, %d bytes)"
          % (a.out, n, rep["proof_bytes"]))
    print("c solver %s  status UNSAT  seconds %.2f"
          % (a.solver, rep["wall_seconds"]))
    print("c sha256 %s" % rep["proof_sha256"])
    if a.json:
        json.dump(rep, open(a.json, "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
