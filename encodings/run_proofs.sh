#!/bin/sh
# run_proofs.sh -- re-emit the DRAT refutations for every level this pack can
# afford to prove, and structurally validate each one.
#
#   sh run_proofs.sh
#
# Separate from run_all.sh because it is heavier: proof logging roughly doubles
# solve time and the four proofs total about 1 GB uncompressed.  Budget about
# SEVEN minutes of one core and 1 GB of free disk: ~129 s is the proof logging
# itself, and the rest is the `xz -9` pass over that 1 GB.  Measured end to end
# at 376.8 s.  (An earlier header said "under four minutes", which priced only
# the logging half.)
#
# It does NOT check the proofs.  Checking is drat-trim's job and is one command
# away -- see proofs/README.md.
set -e
cd "$(dirname "$0")"
mkdir -p proofs results

N="nice -n 19"
say() { printf '\n===== %s\n' "$1"; }

emit() {   # emit <name> <cnf> <proof>
  say "$1: emit the DRAT refutation"
  $N python3 -u code/emit_proof.py "$2" --out "$3" --json "results/proof_$1.json"
  say "$1: structural validation (well-formedness, NOT a proof check)"
  $N python3 -u code/check_proof_format.py "$3" --cnf "$2" \
      --json "results/proof_format_$1.json" > /dev/null
  python3 - "$1" <<'PY'
import json, sys
d = json.load(open("results/proof_format_%s.json" % sys.argv[1]))
print("%-24s %-18s lemmas=%-7d deletions=%-7d maxvar=%d <= nv=%d  ends in empty clause=%s"
      % (d["proof"], d["VERDICT"], d["added_lemmas"], d["deletions"],
         d["max_variable_in_proof"], d["cnf_nv"], d["ends_in_empty_clause"]))
PY
}

emit k6  positive_control/k6_SUB_U4tgts.cnf proofs/k6_SUB_U4tgts.drat
emit k9  cnf/k9_joint_W3U4.cnf              proofs/k9_joint_W3U4.drat
emit k10 cnf/k10_joint_W3U4.cnf             proofs/k10_joint_W3U4.drat
emit k11 cnf/k11_joint_W3U4.cnf             proofs/k11_joint_W3U4.drat

say "compress (the pack ships the .xz form)"
for f in proofs/*.drat; do
  $N xz -9 -T1 -f -k "$f"
done
ls -l proofs/

say "PROOFS EMITTED.  To CHECK one, see proofs/README.md"
