#!/bin/bash
# launch_hunt.sh -- wave-3 hunt-deeper: 12 workers.
#   Track D (descent, 5): the young basins that were still descending.
#   Track P (prospect, 6): repulsion from BOTH known 88 families, diverse 89 seeds.
#   Track F (frontier, 1): most distant harvested 88 corner, pushed further out.
# Usage: ./launch_hunt.sh <total_seconds>
cd "$(dirname "$0")/work" || exit 1
TOTAL=${1:-15300}
OUT=../runs_hunt
mkdir -p "$OUT"
AG=../..   # campaign_87/agents
ME=../../merged-engine
REPEL='{"lns":{"repel_file":"../repel_masks.json","repel_pen":2,"repel_up_p":0.25},"walk":{"repel_file":"../repel_masks.json","repel_up_p":0.25}}'
REPELSOFT='{"lns":{"repel_file":"../repel_masks.json","repel_pen":1,"repel_up_p":0.4},"walk":{"repel_file":"../repel_masks.json","repel_up_p":0.4}}'

# --- Track D: continue the never-converged young basins ---
nohup python3 hunt_worker.py d1_hyb90cont  alt "$ME/runs_hunt/retired_w7_hyb90_best.json" "$OUT" 3101 "$TOTAL" '{}' >/dev/null 2>&1 &
nohup python3 hunt_worker.py d2_hyb90fresh alt "$AG/basin-diversity/portfolio/div_21_g90_d7_j127.json" "$OUT" 3202 "$TOTAL" '{}' >/dev/null 2>&1 &
nohup python3 hunt_worker.py d3_orb90a     alt "$AG/orbit-ladder/BEST_90gates_depth9_rho2symmetric.json" "$OUT" 3303 "$TOTAL" '{}' >/dev/null 2>&1 &
nohup python3 hunt_worker.py d4_orb90bcont alt "$ME/runs_hunt/w6_orbit90_best.json" "$OUT" 3404 "$TOTAL" '{}' >/dev/null 2>&1 &
nohup python3 hunt_worker.py d5_orb90bfr   alt "$AG/orbit-ladder/BEST_90gates_depth7_rho2symmetric_basin2.json" "$OUT" 3505 "$TOTAL" '{}' >/dev/null 2>&1 &

# --- Track P: third-family prospecting (Jaccard repulsion from BOTH 88 families) ---
nohup python3 hunt_worker.py p1_syl        alt seeds/IMPORTED_89_sunyangli.json "$OUT" 3606 "$TOTAL" "$REPEL" >/dev/null 2>&1 &
nohup python3 hunt_worker.py p2_sylcont    alt "$ME/runs_hunt/retired_w6_syl89_best.json" "$OUT" 3707 "$TOTAL" "$REPEL" >/dev/null 2>&1 &
nohup python3 hunt_worker.py p3_out89      alt seeds/out_89.json "$OUT" 3808 "$TOTAL" "$REPEL" >/dev/null 2>&1 &
nohup python3 hunt_worker.py p4_div00      alt "$AG/basin-diversity/portfolio/div_00_g89_d7_j107.json" "$OUT" 3909 "$TOTAL" "$REPEL" >/dev/null 2>&1 &
nohup python3 hunt_worker.py p5_div11      alt "$AG/basin-diversity/portfolio/div_11_g89_d6_j118.json" "$OUT" 4010 "$TOTAL" "$REPEL" >/dev/null 2>&1 &
nohup python3 hunt_worker.py p6_div04      alt "$AG/basin-diversity/portfolio/div_04_g89_d10_j107.json" "$OUT" 4111 "$TOTAL" "$REPEL" >/dev/null 2>&1 &

# --- Track F: push the distant-88 frontier below J=0.7 to both anchors ---
nohup python3 hunt_worker.py f1_dist88     alt "../portfolio88/p88_00_d8_jJean517_jNew743.json" "$OUT" 4212 "$TOTAL" "$REPELSOFT" >/dev/null 2>&1 &

date +%s > ../hunt_deadline_start
echo "$(( $(date +%s) + TOTAL ))" > ../hunt_deadline
echo "launched 12 workers for ${TOTAL}s into $OUT"
