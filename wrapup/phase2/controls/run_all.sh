#!/bin/bash
# Reproduce every control in this kit, from scratch.  Single-thread, nice -19.
# Writes each transcript into this directory and prints a summary table.
set -u
R=/home/joebachir20/xor_ui/slp-plateau-search
P=$R/wrapup/phase2
C=$P/controls
N="nice -n 19"
declare -a CTLNAME CTLRES

run() { CTLNAME+=("$1"); shift; "$@"; CTLRES+=($?); }

echo "### C1-C4  spec derivation (forward control, GF(2) inverse, M^3 identity)"
run "C1-C4 spec derivation" bash -c \
  "$N python3 $P/spec/derive_invmc.py > $C/C1-C4_spec_derivation.txt 2>&1"

echo "### S1  sector probe (the fleet8 frame on the inverse)"
run "S1 sector probe" bash -c \
  "$N python3 $P/spec/sector_probe.py > $C/S1_sector_probe.txt 2>&1"

echo "### O1-O5  generic oracle"
run "O1-O5 oracle" bash -c \
  "bash $C/run_oracle_controls.sh > $C/O1-O5_oracle.txt 2>&1 && ! grep -q FAIL $C/O1-O5_oracle.txt"

echo "### B1  tripwire, five published 88s must all read B=56"
run "B1 tripwire" bash -c \
  "$N python3 $P/tools/tripwire_B.py --target $P/spec/mixcolumns_matrix.json \
     --calibrate $R/evidence/circuits/mixcolumns_88gates_depth5.json \
     $R/evidence/circuits/mixcolumns_88gates_depth5.json \
     $R/evidence/circuits/mixcolumns_88gates_depth5_fromscratch.json \
     $R/evidence/circuits/mixcolumns_88gates_depth6.json \
     $R/evidence/circuits/mixcolumns_88gates_depth7.json \
     $R/evidence/circuits/mixcolumns_88gates_depth8_thirdfamily.json \
     $R/evidence/circuits/mixcolumns_89gates_depth5.json \
     $R/evidence/circuits/mixcolumns_92gates_depth4.json \
     $R/evidence/circuits/mixcolumns_97gates_depth3.json \
     --jsonl $C/B_ledger.jsonl > $C/B1_tripwire.txt 2>&1"

echo "### N2  the emitted baseline circuits still oracle VALID"
run "N2 baselines oracled" bash -c \
  "$N python3 $P/tools/verify_slp_generic.py --target $P/spec/invmc_matrix.json \
     $P/circuits/invmc_paar1.json > /dev/null 2>&1 && \
   $N python3 $P/tools/verify_slp_generic.py --target $P/spec/invmc_matrix.json \
     $P/circuits/invmc_from_mc_cubed_264.json > /dev/null 2>&1 && \
   $N python3 $P/tools/verify_slp_generic.py --target $P/spec/mixcolumns_matrix.json \
     $P/circuits/mixcolumns_paar1.json > /dev/null 2>&1"

echo
echo "=========================== SUMMARY ==========================="
fail=0
for i in "${!CTLNAME[@]}"; do
  s=${CTLRES[$i]}
  [ "$s" -eq 0 ] || fail=1
  printf "  %-28s %s\n" "${CTLNAME[$i]}" "$([ "$s" -eq 0 ] && echo PASS || echo "FAIL(exit $s)")"
done
echo "==============================================================="
[ $fail -eq 0 ] && echo "ALL CONTROLS PASS" || echo "CONTROL FAILURE"
exit $fail
