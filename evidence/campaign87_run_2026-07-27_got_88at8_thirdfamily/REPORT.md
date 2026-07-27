# hunt-deeper — REPORT (wave 3)

**HEADLINE: a THIRD independent 88-gate family was found and oracle-verified —
`BREAKTHROUGH_88gates_depth8_THIRDFAMILY.json` (88@8, J=0.455 to Jean's 88,
J=0.544 to merged-engine's independent 88; both far below the 0.7 family
threshold). It emerged from the continued descent of orbit-ladder's
ρ²-symmetric 90-gate basin1 (`BEST_90gates_depth9_rho2symmetric.json`):
90@5 → 89@7 (60 min) → 89@6 → 88@8 (125 min), worker d3_orb90a, alt engine,
no repulsion needed — exactly the "young basins never converged" bet of this
wave. Its k≤3 shell is VIRGIN (the exact-k4 irreducibility theorems cover
only the two old families). No ≤87 was found. 54,889 NEW distinct verified
88-gate mask sets were harvested beyond wave-2's 84,989 (project total now
≈139,878), of which 53,902 belong to the new third family.**

## What ran (12 workers, 4.25 h, merged-engine's engine + two new mechanisms)

New code (knob-gated, in `work/engines.py` + `work/hunt_worker.py`):
1. **Family repulsion** (`repel_file`/`repel_pen`/`repel_up_p`): a 57-mask
   "family core" set (union of both 88 anchors + masks in >=30% of the wave-2
   88-harvest, minus targets and wt-2 masks; `repel_masks.json`).  LNS bumps
   the pull-in cost class of repel masks; both engines veto most
   overlap-increasing plateau moves.
2. **Drift mode** (`drift_refs` in hunt_worker): instead of reseeding every
   chunk from the frozen Pareto best (which silently discarded ALL plateau
   drift each chunk — the reason wave-2's drift radius stalled), reseed from
   the most family-DISTANT best-size state harvested in the last chunk
   (window pick with +0.05 slack ratchet).
3. `census.py`: incremental dedupe of all harvested 88s + online Jaccard
   family detector (flagged the third family within minutes of its birth,
   saved 25 verified representatives as `NEWFAMILY_88_*.json`).

## Per-track endpoints (all oracle-verified)

| track | seed | end best | note |
|---|---|---|---|
| d3_orb90a | ρ²-sym-90 basin1 | **88@8 THIRD FAMILY** | 90→89@7→89@6→88@8; the headline |
| n3_cone / n3_big / n3_walk | third-family 88 | 88@8 | swarm launched 03:10; mapped 53.9k states; no 87 |
| n3_edge | most distant f3 state (maxJ 0.725) | 88@8 | family-frontier expansion |
| d1_hyb90cont | hybrid-90 endpoint 89@5 | 89@5 | fell into record basin (Jrec89 0.87) — hybrid line is CONVERGED; retired 03:10 |
| d2_hyb90fresh | hybrid 90@7 | 89@5 | same conclusion; retasked to d2_punchS |
| d4_orb90bcont / d5_orb90bfr | ρ²-90 basin2 (+endpoint) | 89@5 | basin2 converges to 89@5 (Jrec 0.51-0.53, a distinct rim basin); retired 03:10 |
| p1_syl / p2_sylcont / d2_punchS | SYL-89 lineage | 89@6 | SYL cluster (pairwise J 0.82) holds at 89 |
| p3_out89 / p4_div00 / p5_div11 / p6_div04 | out_89 + diverse 89s, repel+drift | 89@6 | all four merged into ONE remote 89-cluster at maxJ_fam=0.331 (pairwise J 0.84-0.87); >107k distinct 89s harvested there; NO 88 in it despite 2 dedicated lns punchers (p5_punchA/p6_punchB) for 3 h |
| f1_dist88 | distant-88 corner p88_00 | 88@7 | soft+strong repel pushed new88-family minJ 0.743→0.467; 987 new 88s on that side; never crossed below J 0.7 to both old anchors |

## New-family census (population88_new.jsonl, 54,889 new distinct 88s)

Assignment by max Jaccard to the three anchors (family iff J>=0.7):
- **third family (orb88): 53,902** — J to Jean 0.455-0.56, J to new88 0.467-0.58
- new88 family: 987 (f1's frontier work)
- Jean family: 0 (no worker was tasked there this wave)
- unaffiliated (J<0.7 to all three): **0 — no fourth family found**

The remote 89-cluster at maxJ 0.331 is the obvious fourth-family candidate,
but it refuses to yield an 88: >100k distinct 89s, two operator-mix lns
punchers, repulsion and drift — nothing. Either its 88 floor needs a >=4-mask
jump or it genuinely bottoms at 89.

## Artifacts
- `BREAKTHROUGH_88gates_depth8_THIRDFAMILY.json` — the third-family 88@8
  (verify_circuit.py: VALID).
- `NEWFAMILY_88_00..24_*.json` — 25 verified early representatives.
- `portfolio_family3/` — manifest + 8 verified k-center-diverse third-family
  reps (J_orb88 0.725-0.814; all at J 0.455-0.517 to both old families).
- `population88_new.jsonl` — 54,889 new distinct 88 sets (49 MB), deduped
  against wave-2's 84,989 (census/preseen.txt).
- `family_refs.json` — the three family anchor mask sets (jean/new88/orb88).
- `runs_hunt/remote_seed_[ab].json`, `frontier88_seed.json`,
  `n3edge_seed.json` — verified reseed points.
- `work/` — merged engine + repulsion + drift mode; `census.py`,
  `monitor_pass.sh`, `launch_hunt.sh`.

## Most promising next step
**Run the exact k<=3 sweep (exact-k4 agent's budget-1/2 cascade) over the
third family NOW**: all existing irreducibility theorems cover only the two
old families; 53,902 fresh states x k=2/k=3 windows is exactly the compute
shape that wave-2 finished in hours, and the first reducible window IS an 87.
Secondarily: SAT cone-windows (k=10-16, budget 87) on
`BREAKTHROUGH_88gates_depth8_THIRDFAMILY.json` — sat-deep's method on a
circuit nobody has windowed yet.
