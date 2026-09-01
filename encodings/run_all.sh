#!/bin/sh
# run_all.sh -- every reproducible step of this pack, in order, from the pack
# root.  This is the script that produced the pasted output in RUN.md.
#
#   sh run_all.sh
#
# It re-runs only the cheap levels (k = 9, 10, 11) and the controls.  It never
# starts k = 12, 13 or 14: those cost hours to days of a core and their banked
# verdicts are documented in logs/BANKED_LOGS.md.
#
# Everything runs single-threaded, one solve at a time, at nice -n 19.
set -e
cd "$(dirname "$0")"
mkdir -p results

N="nice -n 19"
say() { printf '\n===== %s\n' "$1"; }

say "0. instance facts (rank, free signals, proved lower bound, greedy control)"
$N python3 -u code/instance_facts.py --json results/instance_facts_merged.json

say "1. file identity: each shipped CNF vs a fresh build of the same formula"
for k in 9 10 11 12 13 14; do
  $N python3 -u code/check_cnf.py "cnf/k${k}_joint_W3U4.cnf" --k "$k" \
      --json "results/identity_k${k}.json" > /dev/null
  python3 - "$k" <<'PY'
import json, sys
k = sys.argv[1]
d = json.load(open("results/identity_k%s.json" % k))
print("k=%-3s %-10s nv=%-6d clauses=%-7d roundtrip=%s digests=%s"
      % (d["k"], d["VERDICT"], d["encoder_nv"], d["encoder_nclauses"],
         d["roundtrip_identical"], d["digests_match"]))
PY
done

say "2. re-run k = 9   (expect UNSAT)"
$N python3 -u code/solve_dimacs.py cnf/k9_joint_W3U4.cnf \
    --json results/solve_k9.json | tee results/solve_k9.log

say "3. re-run k = 10  (expect UNSAT)"
$N python3 -u code/solve_dimacs.py cnf/k10_joint_W3U4.cnf \
    --json results/solve_k10.json | tee results/solve_k10.log

say "4. re-run k = 11  (expect UNSAT)"
$N python3 -u code/solve_dimacs.py cnf/k11_joint_W3U4.cnf \
    --json results/solve_k11.json | tee results/solve_k11.log

say "5. positive control, identity and facts"
$N python3 -u code/check_cnf.py positive_control/k7_SUB_U4tgts.cnf --k 7 \
    --no-pin --instance positive_control/instance_SUB_U4tgts.json \
    --json results/identity_control_k7.json > /dev/null
python3 - <<'PY'
import json
d = json.load(open("results/identity_control_k7.json"))
print("control k=7 %s nv=%d clauses=%d roundtrip=%s"
      % (d["VERDICT"], d["encoder_nv"], d["encoder_nclauses"],
         d["roundtrip_identical"]))
PY
$N python3 -u code/instance_facts.py \
    --instance positive_control/instance_SUB_U4tgts.json --no-pin \
    --json results/instance_facts_control.json > /dev/null
python3 - <<'PY'
import json
d = json.load(open("results/instance_facts_control.json"))
print("control: r=%d m=%d targets=%d  proved lower bound=%d  greedy=%d verified=%s"
      % (d["rank_r"], d["free_signals_m"], d["targets_unrealised"],
         d["lower_bound_L2"], d["greedy_upper_bound"], d["greedy_verify_slp"]))
PY

say "6. positive control, NEGATIVE leg: k = 6 must be UNSAT"
$N python3 -u code/emit_cnf.py --k 6 --no-pin \
    --instance positive_control/instance_SUB_U4tgts.json \
    --out positive_control/k6_SUB_U4tgts.cnf \
    --json results/emit_k6_negative_control.json > /dev/null
$N python3 -u code/solve_dimacs.py positive_control/k6_SUB_U4tgts.cnf \
    --json results/solve_negative_control_k6.json \
    | tee results/solve_negative_control_k6.log

say "7. positive control, POSITIVE leg: k = 7 must be SAT"
$N python3 -u code/solve_dimacs.py positive_control/k7_SUB_U4tgts.cnf \
    --model positive_control/k7_SUB_U4tgts.model \
    --json results/solve_positive_control_k7.json \
    | tee results/solve_positive_control_k7.log

say "8. decode the model into a program, and check it"
$N python3 -u code/decode_model.py positive_control/k7_SUB_U4tgts.model --k 7 \
    --instance positive_control/instance_SUB_U4tgts.json --no-pin \
    --out positive_control/k7_SUB_U4tgts_gates.json \
    --json results/decode_positive_control_k7.json > results/decode_positive_control_k7.log
python3 - <<'PY'
import json
d = json.load(open("results/decode_positive_control_k7.json"))
m = d["model_check"]
print("model_check: %d/%d vars assigned, %d clauses checked, %d unsatisfied"
      % (m["vars_in_model"], m["nv"], m["clauses_checked"],
         len(m["unsatisfied_clause_indices"])))
print("gates:", json.dumps(d["gates"], separators=(",", ":")))
print("verify_slp: %s  (%d inputs, %d targets)"
      % ("ok" if d["verify_slp"]["ok"] else "FAILED",
         d["verify_slp"]["n_inputs"], d["verify_slp"]["n_targets"]))
print("VERDICT:", d["VERDICT"])
PY

say "9. the decoded program vs the independently found witness"
python3 - <<'PY'
import json
a = [list(g) for g in json.load(open("positive_control/expected_witness.json"))["slp_original"]]
b = [list(g) for g in json.load(open("positive_control/k7_SUB_U4tgts_gates.json"))["gates"]]
print("independently banked witness:", json.dumps(a, separators=(",", ":")))
print("decoded from the SAT model  :", json.dumps(b, separators=(",", ":")))
print("GATE-FOR-GATE IDENTICAL:", a == b)
json.dump({"witness_matches_decoded": a == b, "gates": b},
          open("results/witness_agreement.json", "w"), indent=1)
raise SystemExit(0 if a == b else 1)
PY

say "10. the decoder must REJECT a corrupted model"
python3 - <<'PY'
lits = []
for line in open("positive_control/k7_SUB_U4tgts.model"):
    if line.startswith("v"):
        lits += [int(t) for t in line[1:].split()]
lits = [x for x in lits if x != 0]
for i, x in enumerate(lits):          # flip one value bit
    if abs(x) == 1:
        lits[i] = -x
        break
with open("positive_control/k7_SUB_U4tgts_CORRUPT.model", "w") as f:
    f.write("s SATISFIABLE\n")
    row = []
    for x in lits:
        row.append(str(x))
        if len(row) == 20:
            f.write("v " + " ".join(row) + "\n"); row = []
    if row:
        f.write("v " + " ".join(row) + "\n")
    f.write("v 0\n")
PY
set +e
$N python3 -u code/decode_model.py positive_control/k7_SUB_U4tgts_CORRUPT.model \
    --k 7 --instance positive_control/instance_SUB_U4tgts.json --no-pin \
    --out /dev/null --json results/decode_corrupt_control_k7.json \
    > results/decode_corrupt_control_k7.log
rc=$?
set -e
echo "decoder exit code = $rc   (2 = model does not satisfy the formula)"
[ "$rc" -eq 2 ] || { echo "EXPECTED the corrupt model to be rejected"; exit 1; }
python3 -c "import json;d=json.load(open('results/decode_corrupt_control_k7.json'));print('VERDICT:',d['VERDICT']);print('unsatisfied clauses named:',d['model_check']['unsatisfied_clause_indices'])"

say "11. the oracle, on a complete MixColumns circuit"
$N python3 -u code/decode_model.py \
    --verify-circuit positive_control/mixcolumns_88gates_depth7.json 7 \
    --json results/verify_circuit_88gates.json | tee results/verify_circuit_88gates.log

say "12. checksums"
sha256sum -c SHA256SUMS 2>/dev/null | grep -c ': OK$' | sed 's/^/files verified: /'

say "ALL STEPS COMPLETE"
