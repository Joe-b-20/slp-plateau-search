#!/bin/bash
# Controls for wrapup/phase2/tools/verify_slp_generic.py
# O1  three record circuits, forward matrix: VALID, stats identical to verify_circuit.py
# O2  a deliberately mutated circuit: rejected by BOTH oracles
# O3  a target file with the provenance header stripped: REFUSED
# O4  a target file with one row bit flipped (digest intact): REFUSED
# O5  the inverse matrix loads, and a forward circuit fails against it
R=/home/joebachir20/xor_ui/slp-plateau-search
G="nice -n 19 python3 $R/wrapup/phase2/tools/verify_slp_generic.py"
V="nice -n 19 python3 $R/verify_circuit.py"
FWD=$R/wrapup/phase2/spec/mixcolumns_matrix.json
INV=$R/wrapup/phase2/spec/invmc_matrix.json
T=$R/wrapup/phase2/controls/_tmp
mkdir -p "$T"

echo "=========================================================================="
echo "O1  three record circuits, forward matrix"
echo "=========================================================================="
for f in mixcolumns_88gates_depth5 mixcolumns_88gates_depth6 mixcolumns_97gates_depth3; do
  c=$R/evidence/circuits/$f.json
  echo "--- $f"
  a=$($G --target "$FWD" "$c" 2>&1); ra=$?
  b=$($V "$c" 2>&1); rb=$?
  echo "$a" | sed 's/^/   generic: /'
  echo "$b" | sed 's/^/   builtin: /'
  sa=$(echo "$a" | grep -o 'gates=.*problems=[0-9]*')
  sb=$(echo "$b" | grep -o 'gates=.*problems=[0-9]*')
  if [ "$sa" = "$sb" ] && [ $ra -eq 0 ] && [ $rb -eq 0 ] && \
     echo "$a" | grep -q '^VERDICT: VALID'; then
    echo "   O1[$f]: PASS  (stats line identical, both exit 0)"
  else
    echo "   O1[$f]: FAIL  ('$sa' vs '$sb', exits $ra/$rb)"
  fi
done

echo
echo "=========================================================================="
echo "O2  deliberately mutated circuit (gate 40 rewired to [0,1])"
echo "=========================================================================="
python3 - "$R/evidence/circuits/mixcolumns_88gates_depth5.json" "$T/mutant.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
g = d['gates'] if isinstance(d, dict) else d
old = list(g[40]); g[40] = [0, 1]
json.dump(d, open(sys.argv[2], 'w'))
print(f"   mutation: gate 40  {old} -> [0, 1]")
PY
a=$($G --target "$FWD" "$T/mutant.json" 2>&1); ra=$?
b=$($V "$T/mutant.json" 2>&1); rb=$?
echo "$a" | sed 's/^/   generic: /'
echo "$b" | sed 's/^/   builtin: /'
if [ $ra -ne 0 ] && [ $rb -ne 0 ] && echo "$a" | grep -q 'INVALID'; then
  echo "   O2: PASS  (both reject, exits $ra/$rb)"
else
  echo "   O2: FAIL  (exits $ra/$rb)"
fi

echo
echo "=========================================================================="
echo "O3  target file with the provenance header stripped"
echo "=========================================================================="
python3 - "$FWD" "$T/noprov.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1])); d.pop('provenance')
json.dump(d, open(sys.argv[2], 'w'))
PY
a=$($G --target "$T/noprov.json" "$R/evidence/circuits/mixcolumns_88gates_depth5.json" 2>&1); ra=$?
echo "$a" | sed 's/^/   /'
[ $ra -eq 3 ] && echo "   O3: PASS  (exit 3, refused)" || echo "   O3: FAIL (exit $ra)"

echo
echo "=========================================================================="
echo "O4  target file with one matrix bit flipped"
echo "=========================================================================="
python3 - "$FWD" "$T/flipped.json" <<'PY'
import json, sys, hashlib
d = json.load(open(sys.argv[1]))
r = list(d['rows'][7]); r[3] = '1' if r[3] == '0' else '0'
d['rows'][7] = ''.join(r)
# keep the digest self-consistent so it is the RE-DERIVATION that must catch it
d['provenance']['rows_sha256'] = hashlib.sha256('\n'.join(d['rows']).encode()).hexdigest()
d.pop('masks_hex', None)
json.dump(d, open(sys.argv[2], 'w'))
print("   flipped rows[7][3]; digest and mask list re-made to be self-consistent")
PY
a=$($G --target "$T/flipped.json" "$R/evidence/circuits/mixcolumns_88gates_depth5.json" 2>&1); ra=$?
echo "$a" | sed 's/^/   /'
[ $ra -eq 3 ] && echo "   O4: PASS  (exit 3, refused by the from-scratch re-derivation)" \
             || echo "   O4: FAIL (exit $ra)"

echo
echo "=========================================================================="
echo "O5  the InvMixColumns target loads; a forward circuit fails against it"
echo "=========================================================================="
a=$($G --target "$INV" "$R/evidence/circuits/mixcolumns_88gates_depth5.json" 2>&1); ra=$?
echo "$a" | sed 's/^/   /'
if [ $ra -eq 1 ] && echo "$a" | grep -q 'target rebuilt: from GF'; then
  echo "   O5: PASS  (inverse target re-derived from the field; forward 88 builds 0/32)"
else
  echo "   O5: FAIL (exit $ra)"
fi
rm -rf "$T"
