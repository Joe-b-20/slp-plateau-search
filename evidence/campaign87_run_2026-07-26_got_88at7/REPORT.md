# merged-engine — REPORT (wave 2)

**HEADLINE: an INDEPENDENT, oracle-verified 88-gate circuit
(`BREAKTHROUGH_88gates_depth7.json`, 88@7) was found by the merged engine
from OUR ρ²-symmetric 94-gate seed — the first search-found 88 in this
project. It shares only 61/88 masks with Jean's 88 (J=0.530): a genuinely
different circuit. No ≤87 was found. Second headline: Jean's "drift-frozen"
88 plateau is NOT frozen under the exact repair — the merged walk harvested
~85,000 distinct 88-gate mask sets in one evening (wave-1: zero drift).**

## Part A — the merge (work/engines.py)

All pieces ported from the wave-1 agents' folders (sources untouched), in
the brief's priority order; equivalence tests + a smoke run after each step.

| # | source | what was taken | status |
|---|--------|----------------|--------|
| 1 | relax-kernel | level-BFS `relax` (+ `relax_reference` fallback for duplicate masks); realizability-only `feasible_at` for cap=None | merged verbatim |
| 2 | closure-kernel | `_closure_core` worklist closure (+ stop-at-targets), worklist `closure`/`realizable`/`trim_masks`, `_WalkState` incremental `remove_query`, `_walk_gates` topo emission at cap=None, improve-only-on-change in walk | merged verbatim |
| 3 | lns-extract | `_extract` cost-class API (int list, bool back-compat); victim-repool at cost 3 (victims always in rebuild candidates → 100% feasible iterations) | merged; `useful`/`restarts` NOT merged (lns-extract's own report measured them marginal/diversity-negative) |
| 4 | lns-destroy | `dag_info`, `_inject`, `_cone_pick`; coneinj + biginj destroy operators as knob-controlled op-mix (default small .35 / coneinj .45 / biginj .20); PEEL-BEFORE-ACCEPT for near-miss rebuilds (nu < r ≤ nu+peel_window) | merged (their key unexploited fix now in) |
| 5 | repair-move | exact complete `_repair` (C ∩ P2 enumeration) + forbid-just-removed + min-trim choice | merged verbatim |
| 6 | lns-pool | scored hot-multiset pool sampling (hot_frac=0.5); peel cache (frozenset-keyed, shared with peel-before-accept) | merged; `vk` per-victim candidates superseded by coneinj `_inject` |
| 7 | knob-sweep / acceptance-schedule | champ_fast knobs (kmax=4, kshake=12, snapback=12, nsamp=(12,12), up_prob=0.5, up_slack=4); SA-with-reheat acceptance (T0=1.2, cool=0.9997, reheat@4000 stagnant) default | merged |
| + | new (wave-2 plan) | PLATEAU HARVESTING: every distinct equal-best-size mask set → `<label>.pop.jsonl`; CROSS-POLLINATION: each lns worker merges new masks from ALL sibling pop files into its pool every 120s | new code |
| + | new (this agent) | `alt` worker mode in `work/hunt_worker.py`: alternate 300s walk chunks (spray/descend) with 600s lns chunks (punch), one shared harvest | new code |

Conflict resolutions:
- walk repair: closure-kernel `_repair_fast` vs repair-move exact `_repair` —
  composable, both kept: `_WalkState.remove_query` answers the removal and
  its exact closure feeds repair-move's exact `_repair`.
- acceptance: SA-with-reheat over kick2 (comparable measured drift, simpler,
  no clash with victim-repool cost classes).

Equivalence tests (all passed): relax==reference on 5 seeds incl.
IMPORTED_88; feasible_at==depth-fixpoint verdicts on 150 damaged subsets;
worklist closure==naive on 100 subsets; remove_query==full closure on 250
queries; exact `_repair` returns only realizable sets; `_walk_gates` and
`indexpairs_from_masks` outputs oracle-VALID.

### Measured throughput (this box, fleet-loaded)
| engine | base | merged | note |
|---|---|---|---|
| walk | ~70-110 it/s | **480-640 it/s** (289k iters in one 600s chunk under full load) | ~6x; plus ~2-3k distinct harvested plateau sets/min |
| lns | ~60-100 it/s | ~100-180 it/s | ~2x raw, but neighborhoods far richer: coneinj kk 3-12 and biginj kk 8-16 now productive; peel-before-accept recovered 2630 near-miss rebuilds in a 2-min probe (previously 100% auto-rejected) |

Smoke gate: 60s from seed_90_at_depth5 — walk found verified 89@5 in 42s.

## Part B — the long hunt (8400s, 10 workers, `runs_hunt/`)

Initial fleet (21:35): w1/w2/w3/w4/w5 on IMPORTED_88 (coneinj 4-12 / biginj /
alt / coneinj 3-8 / pure walk), w6 SYL-89 alt, w7 hybrid-90@7 alt,
w8 div_00 89 alt, w9 div_11 89 alt, w10 ρ²-symmetric-94 alt.
Mid-hunt redirections (documented in hunt log below): after the independent
88 appeared, w2→new-88 basin, w8→new-88, w9→most-distant harvested 88;
after coordinator's message, w6→orbit-ladder ρ²-90 basin2, w7→syl-move 88
sibling sib_88g_j85_05.

### Hunt log
- 21:35 launch, all workers adopt seeds (88@7 / 89s / 94).
- 21:37 w5 (pure walk on Jean 88): 3559 distinct 88-sets in 114s —
  **the 88 plateau is highly mobile under exact repair** (wave-1: frozen).
- 21:44 w10 already 94→89@7 (asymmetric polish of the symmetric basin);
  w7 hybrid 90→89@5.
- 22:00 33k distinct 88-sets; drift radius to Jean J=0.796 (10 masks).
- **22:08 w10 walk finds 88 (it=45614), immediately Pareto-driven
  88@11→88@7. Oracle-VALID. J to Jean 88 = 0.530, J to SYL 89 = 0.526,
  J to our 89@5 = 0.539 → INDEPENDENT 88, saved as
  `BREAKTHROUGH_88gates_depth7.json`.**
- 22:11 w2 redirected to the new 88 (coneinj 3-10).
- 22:33 41.5k distinct 88-sets across two families (Jean-side minJ 0.52,
  new88-side minJ 0.50 — cross-pollination bridging).
- 22:45 w8→new88 (fresh RNG), w9→most-distant harvested 88
  (`runs_hunt/distant88_seed.json`, maxJ 0.743 to both anchors, verified).
- 23:07 66k distinct 88-sets.
- 23:23 coordinator seeds: w6→orbit-ladder ρ²-90 basin2, w7→syl-move 88
  sibling (both verified on import).
- 23:29 w7_sylsib holds 88@7; 23:40 w6_orbit90 90→89@5 in 15 min.
- 23:55 deadline; clean shutdown. **No ≤87 from any track.**

### Where every track ended (all oracle-verified)
| track | seed | end best |
|---|---|---|
| w1_88_cone | Jean 88 | 88@7 (plateau explored, no 87) |
| w2_88_big → w2_new88 | Jean 88 → new 88 | 88@7 |
| w3_88_alt | Jean 88 | 88@7 |
| w4_88_cone2 | Jean 88 | 88@7 |
| w5_88_walk | Jean 88 | 88@7 (biggest single harvester) |
| w6_syl89 (→23:23) | SYL 89 | 89@6 |
| w6_orbit90 (23:23→) | orbit ρ²-90 basin2 | 89@5 (young basin, still descending at cutoff) |
| w7_hyb90 (→23:23) | hybrid 90@7 | 89@5 |
| w7_sylsib (23:23→) | syl-move 88 sibling | 88@7 |
| w8_div89a (→22:45) | div_00 89@7 | 89@6 |
| w8_new88b (22:45→) | new 88 | 88@7 |
| w9_div89b (→22:45) | div_11 89@6 | 89@6 |
| w9_dist88 (22:45→) | distant harvested 88 | 88@7 |
| w10_sym94 | ρ²-symmetric 94 | **88@7 (the independent 88)** |

## Artifacts
- `BREAKTHROUGH_88gates_depth7.json` — independent verified 88@7.
- `portfolio88/` — manifest + 8 verified maximally-diverse 88@7-9 circuits
  (k-center picks over the harvest; J to Jean 0.517-0.796, J to new88
  0.504-0.796) + the breakthrough entry.
- `runs_hunt/*.pop.jsonl` — **84,989 distinct 88-gate mask sets** (379 MB)
  + tens of thousands of 89-sets: the plateau population for wave-3.
- `runs_hunt/distant88_seed.json` — verified bridge 88.
- `work/` — the merged engine (engines.py, hunt_worker.py) — drop-in for
  worker.py/ladder_parallel.py (same run_engine interface).

## Most promising next step
The 88 plateau is a huge connected cloud (≥85k states, ≥2 families
J≈0.5 apart) and k≤3 irreducibility was proven only for Jean's single point.
Feed the harvested population to the exact-k4 / sat-window agents: run exact
budget-2/3 (fast: µs/window) over the k=2/k=3 windows of THOUSANDS of
harvested 88 states instead of one — the first state with a reducible small
window IS the 87. Secondarily: asymmetric polish of orbit-ladder basins
(90→89 took 15 min; they are young) and coneinj hunts from all
portfolio88/ representatives.
