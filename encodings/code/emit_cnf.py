#!/usr/bin/env python3
"""emit_cnf.py -- write the DIMACS file for one level of one instance.

    python3 code/emit_cnf.py --k 9  --out /tmp/k9.cnf
    python3 code/emit_cnf.py --k 6  --no-pin \
            --instance positive_control/instance_SUB_U4tgts.json \
            --out positive_control/k6_SUB_U4tgts.cnf

THIS SCRIPT ADDS NO ENCODING OF ITS OWN.  It calls the shipped encoder,

    slp_opt.build_cnf(r, in_vals, tgt_vals, k, symmetry=True)

and serialises `cnf.clauses` verbatim, in order.  It adds no clause and no
variable.  The CNF is built TWICE and the two clause lists compared, so the
emission is checked to be deterministic before anything is written.

The shipped CNFs in cnf/ were produced by exactly this call.  Their `c` header
comments differ from the ones written here -- comments are not part of the
formula and no solver reads them -- so compare the CLAUSE BODY, which is what
`code/check_cnf.py` does, literal for literal and in order, and what the
clause-order sha256 in each file's header records.  The shipped bytes are the
provenance: regenerating is a check, never a substitute for them.
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from instance_io import (load_slp_opt, load_instance, clause_digest,  # noqa
                         sha256_file)


def write_dimacs(path, cnf, header_comments):
    with open(path, "w") as f:
        for line in header_comments:
            f.write("c %s\n" % line)
        f.write("p cnf %d %d\n" % (cnf.nv, len(cnf.clauses)))
        for cl in cnf.clauses:
            f.write(" ".join(str(x) for x in cl))
            f.write(" 0\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, required=True)
    ap.add_argument("--instance", default=None)
    ap.add_argument("--no-pin", action="store_true")
    ap.add_argument("--no-symmetry", action="store_true")
    ap.add_argument("--out", required=True)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    SO = load_slp_opt()
    instd, checks = load_instance(a.instance, pin=not a.no_pin)
    inst = SO.Instance(instd["dim"], instd["inputs"], instd["targets"])
    sym = not a.no_symmetry

    cnf, V, Z = SO.build_cnf(inst.r, inst.in_vals, inst.tgt_vals, a.k,
                             symmetry=sym)
    cnf2, _, _ = SO.build_cnf(inst.r, inst.in_vals, inst.tgt_vals, a.k,
                              symmetry=sym)
    if cnf.clauses != cnf2.clauses or cnf.nv != cnf2.nv:
        raise SystemExit("encoder is not deterministic -- refusing to write")

    write_dimacs(a.out, cnf, [
        "instance canonical sha256 %s" % checks["canonical_sha256"],
        "rank r=%d  free signals m=%d  targets t=%d  k=%d  symmetry=%s"
        % (inst.r, inst.m, len(inst.tgt_vals), a.k, sym),
        "encoder slp_opt.build_cnf, clauses emitted verbatim and in order",
        "clause-order sha256 %s" % clause_digest(cnf.clauses),
    ])

    rep = {"out": os.path.basename(a.out), "k": a.k, "symmetry": sym,
           "nv": cnf.nv, "nclauses": len(cnf.clauses),
           "r": inst.r, "m": inst.m, "n_targets": len(inst.tgt_vals),
           "clause_order_sha256": clause_digest(cnf.clauses),
           "file_sha256": sha256_file(a.out),
           "instance": checks, "deterministic": True}
    print(json.dumps(rep, indent=1))
    if a.json:
        json.dump(rep, open(a.json, "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
