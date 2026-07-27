#!/bin/bash
# launch_hunt.sh -- wave-2 merged-engine long hunt: 10 workers, shared harvest
# dir for cross-pollination.  Usage: ./launch_hunt.sh <total_seconds>
cd "$(dirname "$0")/work" || exit 1
TOTAL=${1:-8100}
OUT=../runs_hunt
mkdir -p "$OUT"
AG=../..   # campaign_87/agents

# --- THE priority: Jean's verified 88@7 (any 87 is >=4 masks away: favor
#     coneinj 4-12 and big-destroy+peel) ---
nohup python3 hunt_worker.py w1_88_cone   lns seeds/IMPORTED_88.json "$OUT" 101 "$TOTAL" \
  '{"op_mix":{"coneinj":0.7,"small":0.3},"cone_lo":4,"cone_hi":12}' >/dev/null 2>&1 &
nohup python3 hunt_worker.py w2_88_big    lns seeds/IMPORTED_88.json "$OUT" 202 "$TOTAL" \
  '{"op_mix":{"biginj":0.5,"coneinj":0.3,"small":0.2},"peel_window":8}' >/dev/null 2>&1 &
nohup python3 hunt_worker.py w3_88_alt    alt seeds/IMPORTED_88.json "$OUT" 303 "$TOTAL" \
  '{}' >/dev/null 2>&1 &
nohup python3 hunt_worker.py w4_88_cone2  lns seeds/IMPORTED_88.json "$OUT" 404 "$TOTAL" \
  '{"op_mix":{"coneinj":0.5,"small":0.3,"biginj":0.2},"cone_lo":3,"cone_hi":8,"kshake":16}' >/dev/null 2>&1 &
nohup python3 hunt_worker.py w5_88_walk   walk seeds/IMPORTED_88.json "$OUT" 505 "$TOTAL" \
  '{}' >/dev/null 2>&1 &

# --- other basins ---
nohup python3 hunt_worker.py w6_syl89     alt seeds/IMPORTED_89_sunyangli.json "$OUT" 606 "$TOTAL" \
  '{}' >/dev/null 2>&1 &
nohup python3 hunt_worker.py w7_hyb90     alt "$AG/basin-diversity/portfolio/div_21_g90_d7_j127.json" "$OUT" 707 "$TOTAL" \
  '{}' >/dev/null 2>&1 &
nohup python3 hunt_worker.py w8_div89a    alt "$AG/basin-diversity/portfolio/div_00_g89_d7_j107.json" "$OUT" 808 "$TOTAL" \
  '{}' >/dev/null 2>&1 &
nohup python3 hunt_worker.py w9_div89b    alt "$AG/basin-diversity/portfolio/div_11_g89_d6_j118.json" "$OUT" 909 "$TOTAL" \
  '{}' >/dev/null 2>&1 &
nohup python3 hunt_worker.py w10_sym94    alt "$AG/structure-algebra/symlns_94gates_seed44.json" "$OUT" 1010 "$TOTAL" \
  '{}' >/dev/null 2>&1 &
echo "launched 10 workers for ${TOTAL}s into $OUT"
jobs -p
