#!/usr/bin/env python3
"""check_proof_format.py -- structural validation of a DRAT proof file.

    python3 code/check_proof_format.py proofs/k9_joint_W3U4.drat \
            --cnf cnf/k9_joint_W3U4.cnf

**This is NOT a proof check.** It does not replay a single lemma and it cannot
tell a valid refutation from an invalid one. Only a DRAT checker does that, and
the command for one is in gen_and_solve.md §2. What this script does is confirm
the file is a well-formed DRAT proof of *this* CNF before anyone spends an hour
checking it:

  * every line parses as a clause: signed integers terminated by 0, optionally
    prefixed by `d ` for a deletion;
  * every variable mentioned is within the CNF's variable count (a proof over
    the wrong formula usually fails here immediately);
  * the file ends in the **empty clause**, which is what makes it a refutation
    rather than a log;
  * counts of added lemmas and deletions, and the file's sha256.

Exits 1 if any of that fails.
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from solve_dimacs import parse_dimacs, sha256  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("proof")
    ap.add_argument("--cnf", default=None,
                    help="the CNF the proof refutes, for the variable-range check")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    nv = None
    if a.cnf:
        nv, _, _ = parse_dimacs(a.cnf)

    additions = deletions = lines = 0
    maxvar = 0
    empty_clause_at = None
    bad = []
    with open(a.proof) as f:
        for i, raw in enumerate(f, 1):
            s = raw.strip()
            if not s:
                continue
            lines += 1
            is_del = False
            if s.startswith("d ") or s == "d":
                is_del = True
                s = s[1:].strip()
            toks = s.split()
            if not toks or toks[-1] != "0":
                bad.append((i, "does not end in 0"))
                if len(bad) > 5:
                    break
                continue
            lits = []
            ok = True
            for t in toks[:-1]:
                try:
                    x = int(t)
                except ValueError:
                    bad.append((i, "non-integer token %r" % t))
                    ok = False
                    break
                if x == 0:
                    bad.append((i, "interior 0"))
                    ok = False
                    break
                lits.append(x)
                maxvar = max(maxvar, abs(x))
            if not ok:
                if len(bad) > 5:
                    break
                continue
            if is_del:
                deletions += 1
            else:
                additions += 1
                if not lits:
                    empty_clause_at = i

    rep = {
        "proof": os.path.basename(a.proof),
        "proof_sha256": sha256(a.proof),
        "proof_bytes": os.path.getsize(a.proof),
        "lines": lines,
        "added_lemmas": additions,
        "deletions": deletions,
        "max_variable_in_proof": maxvar,
        "cnf": os.path.basename(a.cnf) if a.cnf else None,
        "cnf_nv": nv,
        "variables_within_cnf": (nv is None or maxvar <= nv),
        "ends_in_empty_clause": (empty_clause_at is not None
                                 and empty_clause_at == lines),
        "empty_clause_line": empty_clause_at,
        "malformed_lines": bad[:6],
        "NOTE": "well-formedness only -- this does NOT verify the refutation",
    }
    ok = (not bad and rep["variables_within_cnf"]
          and rep["ends_in_empty_clause"])
    rep["VERDICT"] = "WELL-FORMED DRAT" if ok else "MALFORMED"
    print(json.dumps(rep, indent=1))
    if a.json:
        json.dump(rep, open(a.json, "w"), indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
