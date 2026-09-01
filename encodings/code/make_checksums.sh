#!/bin/sh
# make_checksums.sh -- regenerate SHA256SUMS over the SHIPPED artifacts.
#
#   sh code/make_checksums.sh      # from the pack root
#   sha256sum -c SHA256SUMS
#
# Covered: the instance, the CNFs, the code, the documents, the positive
# control's inputs and its banked expected answer.
#
# NOT covered, on purpose: results/, the files run_all.sh derives
# (positive_control/*.model, *_gates.json, k6_SUB_U4tgts.cnf), and the
# uncompressed proofs/*.drat that run_proofs.sh emits or `xz -dk` unpacks.
# Those are outputs of a run, not shipped artifacts; a reader who re-runs the
# pack will and should overwrite them.  The shipped proofs/*.drat.xz ARE
# covered, and the digests of the uncompressed proofs are in proofs/README.md.
set -e
cd "$(dirname "$0")/.."
find . -type f \
     ! -path './results/*' \
     ! -name 'SHA256SUMS' \
     ! -name '*.model' \
     ! -name '*_gates.json' \
     ! -name 'k6_SUB_U4tgts.cnf' \
     ! -name '*.drat' \
     ! -name '*.pyc' \
     ! -path '*/__pycache__/*' \
     | LC_ALL=C sort | xargs sha256sum > SHA256SUMS
wc -l < SHA256SUMS | sed 's/^/files checksummed: /'
