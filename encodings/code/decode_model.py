#!/usr/bin/env python3
"""decode_model.py -- turn a SAT model of a shipped CNF into an XOR program,
and check it.

    python3 code/decode_model.py MODELFILE --k 14
    python3 code/decode_model.py positive_control/k7_SUB_U4tgts.model --k 7 \
            --instance positive_control/instance_SUB_U4tgts.json --no-pin
    python3 code/decode_model.py --verify-circuit CIRCUIT.json 7

MODELFILE is whatever your solver printed: DIMACS `s`/`v` lines, a bare list of
signed integers, or a JSON list of signed integers.  Only the sign of each
literal is used, and `v` lines may be split however the solver likes.

What it does, in order:

  1. Rebuilds the CNF with the SAME call the shipped file was written from
     (`code/slp_opt.py: build_cnf(r, in_vals, tgt_vals, k, symmetry=True)`),
     which recovers the variable blocks V and Z.
  2. RE-EVALUATES EVERY CLAUSE under the model.  A decoder that trusts the
     solver is not a check; this one checks.
  3. Reads the one-hot Z[i] block of each gate i and emits the straight-line
     program `gates = [[a,b], ...]`: signal a XOR signal b, where signals
     0..n_inputs-1 are the block's free input signals and signal n_inputs+i is
     the output of gate i.
  4. Replays that program over the block's free values and checks that every
     target appears, using the encoder's own `verify_slp`.  THIS is the
     decisive check: at k it certifies a k-gate program for the block.

`--verify-circuit CIRCUIT.json [DEPTH]` skips all of the above and runs the
standalone MixColumns oracle `code/verify_circuit.py` on a finished 32-in/32-out
circuit.  The oracle rebuilds MixColumns from GF(2^8) arithmetic; it does not
read the matrix from a file.

Exit codes: 0 valid, 2 the model does not satisfy the formula, 3 the decoded
program does not compute the targets.
"""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from instance_io import load_slp_opt, load_instance  # noqa: E402

VERIFIER = os.path.join(HERE, "verify_circuit.py")


def read_model(path):
    """Accept DIMACS v-lines, a bare int list, or a JSON list of ints."""
    raw = open(path).read().strip()
    lits = []
    if raw.startswith("["):
        lits = [int(x) for x in json.loads(raw)]
    else:
        saw_v = any(l.startswith("v") for l in raw.splitlines())
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            head = line[0]
            if head in "cs" and len(line) > 1 and line[1] in " \t":
                if head == "s" and "UNSAT" in line.upper():
                    raise SystemExit("model file says UNSATISFIABLE: %s" % line)
                continue
            if head == "v":
                line = line[1:]
            elif saw_v:
                continue                      # ignore non-v chatter
            for tok in line.split():
                x = int(tok)
                if x != 0:
                    lits.append(x)
    if not lits:
        raise SystemExit("no literals found in %s" % path)
    return lits


def check_model(clauses, lits, nv):
    """Re-evaluate every clause under the model.  Returns (ok, report)."""
    val = {}
    for x in lits:
        v, s = abs(x), x > 0
        if v in val and val[v] != s:
            return False, {"error": "model assigns variable %d twice" % v}
        val[v] = s
    unassigned = [v for v in range(1, nv + 1) if v not in val]
    bad = []
    for i, cl in enumerate(clauses):
        if not any(val.get(abs(x), False) == (x > 0) for x in cl):
            bad.append(i)
            if len(bad) > 5:
                break
    return (not bad), {"vars_in_model": len(val), "nv": nv,
                       "unassigned_vars": len(unassigned),
                       "unsatisfied_clause_indices": bad,
                       "clauses_checked": len(clauses)}


def run_verify_circuit(circuit, depth=None):
    cmd = [sys.executable, VERIFIER, circuit] + \
          ([str(depth)] if depth is not None else [])
    p = subprocess.run(cmd, capture_output=True, text=True)
    return {"cmd": " ".join(os.path.basename(c) if c.endswith(".py") else c
                            for c in cmd),
            "returncode": p.returncode,
            "stdout_tail": p.stdout.strip().splitlines()[-6:],
            "stderr_tail": p.stderr.strip().splitlines()[-3:],
            "VALID": p.returncode == 0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model", nargs="?", help="solver output / model file")
    ap.add_argument("--k", type=int, help="the level the model belongs to")
    ap.add_argument("--instance", default=None)
    ap.add_argument("--no-pin", action="store_true",
                    help="skip the merged-block sha256 pin (control instances)")
    ap.add_argument("--no-symmetry", action="store_true")
    ap.add_argument("--out", default=None, help="where to write the gates JSON")
    ap.add_argument("--json", default=None, help="where to write this report")
    ap.add_argument("--verify-circuit", nargs="+", metavar="ARG",
                    help="CIRCUIT.json [DEPTH]: run the oracle and stop")
    a = ap.parse_args()

    if a.verify_circuit:
        c = a.verify_circuit[0]
        d = a.verify_circuit[1] if len(a.verify_circuit) > 1 else None
        r = run_verify_circuit(c, d)
        r["circuit"] = os.path.basename(c)
        r["gates"] = len(json.load(open(c))["gates"])
        print(json.dumps(r, indent=1))
        if a.json:
            json.dump(r, open(a.json, "w"), indent=1)
        return 0 if r["VALID"] else 1

    if not a.model or a.k is None:
        ap.error("a model file and --k are required (or use --verify-circuit)")

    SO = load_slp_opt()
    instd, checks = load_instance(a.instance, pin=not a.no_pin)
    inst = SO.Instance(instd["dim"], instd["inputs"], instd["targets"])
    sym = not a.no_symmetry
    cnf, V, Z = SO.build_cnf(inst.r, inst.in_vals, inst.tgt_vals, a.k,
                             symmetry=sym)

    lits = read_model(a.model)
    ok, mrep = check_model(cnf.clauses, lits, cnf.nv)
    rep = {"model_file": os.path.basename(a.model), "k": a.k,
           "instance": checks, "model_check": mrep,
           "model_satisfies_cnf": ok}
    if not ok:
        rep["VERDICT"] = "MODEL DOES NOT SATISFY THE FORMULA"
        print(json.dumps(rep, indent=1))
        if a.json:
            json.dump(rep, open(a.json, "w"), indent=1)
        return 2

    # the encoder's OWN decoder, not a re-implementation
    slp_int = SO.decode_model({x for x in lits if x > 0}, V, Z, inst.m, a.k)
    gates = SO.internal_to_original(inst, slp_int)
    good, why = SO.verify_slp(instd["inputs"], instd["targets"], gates)

    rep["gates"] = gates
    rep["n_gates"] = len(gates)
    rep["slp_internal"] = [list(g) for g in slp_int]
    rep["verify_slp"] = {"ok": bool(good), "why": why,
                         "n_inputs": len(instd["inputs"]),
                         "n_targets": len(instd["targets"])}
    rep["VERDICT"] = ("VALID %d-gate program for the block" % len(gates)) \
        if good else "DECODED PROGRAM DOES NOT COMPUTE THE TARGETS"

    out = a.out or (os.path.splitext(a.model)[0] + "_gates.json")
    with open(out, "w") as f:
        json.dump({"gates": gates, "n_inputs": len(instd["inputs"]),
                   "n_gates": len(gates), "k": a.k,
                   "instance_canonical_sha256": checks["canonical_sha256"],
                   "verify_slp": bool(good),
                   "note": "block-level straight-line program: signal i < %d is "
                           "a free input signal of the block, signal %d+j is "
                           "gate j.  This is a program for ONE block, not yet a "
                           "32-in/32-out MixColumns circuit."
                           % (len(instd["inputs"]), len(instd["inputs"]))},
                  f, indent=1)
    rep["gates_json"] = os.path.basename(out)

    print(json.dumps(rep, indent=1))
    if a.json:
        json.dump(rep, open(a.json, "w"), indent=1)
    return 0 if good else 3


if __name__ == "__main__":
    sys.exit(main())
