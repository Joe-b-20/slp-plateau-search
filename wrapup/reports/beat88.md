# Slice report: beat88

Agent model: claude-opus-5[1m] (Opus 5, 1M context). Date: 2026-08-29.

**Summary.** `beat88/` (47 GB, 1,463,947 files) is the whole "beat 88" campaign of
2026-08-13 → 2026-08-16: a four-then-five-lane method program (M1 cartography,
M2 oracle, M3 census, M4 inverse, M5 backbone/verify), a shared instrument suite,
a nine-lane "understanding" program (U1–U7, V1, V2), a 26-report retrospective
of the *previous* codebase (`analysis/`), and 38 GB of data salvaged off two
rented pods before they were terminated. It found **no 87** and never claimed one
— the smallest circuit anywhere in this slice is 88 gates, and the smallest
`FOUND_*` alarm file across all 44,249 of them is 89. What it did produce is
large: a **verified depth record 91 gates @ depth 4** (re-verified by me today:
`VERDICT: VALID`), **~1.53 million exported oracle-checkable 88-gate circuit
records** across three hosts (incl. 167 at depth 5), the **"88 wall"** theorems
(no 87 within remove-2-add-1 of all 33,010 known 88 gauge-orbits; no 87 within
remove-3-add-1 of all 64 known 89s), two refereed-grade lower bounds
(`54 ≤ L(MC)` and `L_cf(MC) ≥ 92`), and a large stock of measured negative
results about search methods. The 47 GB is *not* mostly results: **31.4 GB is
descriptor-telemetry `*.cells.jsonl` archives** (search-engine memory, each row
carrying a bit-exact replay tuple), 1.8 GB is three `MANIFEST.jsonl` files, and
1.7 GB is byte-identical `.log`/`.nohup` duplicate pairs. The irreplaceable
material — every circuit, every ledger, every certificate, the compressed
harvest — is **under 3 GB**.

---

## 1. INVENTORY

Commands: `du -sh beat88/`, `du -sh beat88/*/`, then `du -sh <dir>/*` drilling
into the heavy ones. `find . -type f | wc -l` for counts.

```
beat88/                         47 G   1,463,947 files
├── ALLOCATION.md                4.6K  core-allocation ledger + 12 dated revisions
│                                      (the operational history of the whole campaign)
├── pod_salvage/                38 G   data pulled off the two rented pods before termination
│   ├── salvage.log, salvage2.log      the pull logs (POD1_DONE / POD2_DONE / SALVAGE_COMPLETE)
│   ├── pod1/                   16 G
│   │   ├── beat88/methods/m3_census/   15 G  (runs/pod1 12 G incl. archive 11 G; exports 2.8 G)
│   │   ├── beat88/methods/m2_oracle/  1.3 G  (runs 1.1 G — the pod-side exact sweeps + FOUND files)
│   │   ├── beat88/methods/{shared,m5_backbone}/  ~600 K
│   │   └── shared_analysis/    116 K
│   └── pod2/                   22 G
│       ├── beat88/methods/m3_census/   21 G  (runs/pod2 18 G incl. archive 16 G; exports 2.6 G)
│       ├── beat88/methods/m2_oracle/  1.4 G
│       ├── exports_pod2.tar.zst 49 M
│       └── u7/                 568 K  (U7's pod-side representation sweep)
├── methods/                    9.0 G  the five Phase-2 method lanes + shared instruments
│   ├── DESIGN_NOTES.md          the Phase-2 method designs, written from the analysis
│   ├── m3_census/              8.1 G  mass basin discovery (runs 6.8 G, exports 1.3 G)
│   ├── m2_oracle/              482 M  exact deciders / SAT / cuttability census
│   ├── shared/                 461 M  B1–B5 instrument suite (index/pop88 = 460 M)
│   ├── m1_cartography/          33 M  quotient-graph move-class mapping (RETRACTED + corrected)
│   ├── m5_backbone/            744 K  backbone/obligation calculus + the 204-family Phase-B search
│   └── m4_inverse/             276 K  fixed-87 infeasible population search (dropped day 1)
├── understanding/              319 M  the nine "understanding" lanes (U1–U7, V1, V2)
│   ├── PROGRAM_STATE.md, CANON.md (1,437 lines, ~50 laws), MANIFESTO.md, ARCHIVE_…md
│   ├── u2_walls/               290 M  (data/census.jsonl 179 M + data/u4_gates.jsonl 109 M)
│   ├── u4_economy/              22 M  u5_heavycorner/ 2.0 M  u1_obligations/ 1.6 M
│   └── u6_spec87/ 1.1 M  v2_no_vocab/ 820 K  u7_representation/ 516 K
│       v1_vocab_theory/ 460 K  u3_lowerbound/ 164 K
├── analysis/                    78 M  Phase-1 retrospective of the PREVIOUS codebase
│   ├── SYNTHESIS.md (465 lines) — the arbitrating document
│   ├── BRIEF.md (48 lines) — the analysis charter
│   ├── code/                   456 K  14 reports, one per code chunk
│   ├── ideas/                  312 K  12 reports, one per idea
│   └── scratch/                 77 M  541 files in 62 dirs; 98 % measurement dumps, 2 % scripts
└── ops/                        8.0 K  backup_rsync.log (contains: BACKUP_COMPLETE)
```

**File-type breakdown** (`find . -type f | sed -n 's/.*\.\([A-Za-z0-9]\{1,8\}\)$/\1/p' | sort | uniq -c | sort -rn`):

| ext | count | what |
|---|---|---|
| `.json` | 1,460,453 | overwhelmingly single-circuit exports (~900 B each) |
| `.zst` | 1,084 | compressed harvest segments (1,083 `*.pop.*.jsonl.zst`, 337 MB total) + 1 tarball |
| `.jsonl` | 700 | ledgers, worklists, label files, and the huge `*.cells.jsonl` archives |
| `.py` | 591 | instruments |
| `.log` | 481 / `.nohup` 125 | run logs (3.4 GB; **1.73 GB of it duplicated**) |
| `.md` | 120 | writeups |

**Documentation quality.** This slice is unusually well documented. Every method
lane carries `THESIS.md` (pre-registered bet + kill test), `LEDGER.md` (dated
narrative), `STATE.md` (operational/resume detail), and most carry a `FINAL.md`.
Every understanding lane carries `NOTEBOOK.md` + `PROOFCHECK.md`. The only
genuinely opaque areas are:

- `methods/m3_census/runs/*/archive/*.cells.jsonl` — 31.4 GB, schema readable but
  never summarised anywhere except through `ledger.py`'s scoreboard;
- `pod_salvage/*/beat88/methods/m2_oracle/runs/` — the pod-side sweep outputs, of
  which only aggregate counts made it into `LEDGER.md`;
- `analysis/scratch/` — 77 MB of benchmark dumps, described only obliquely by the
  26 reports beside them.

---

## 2. METHODS

Two populations of methods live here. **§2A** are methods *executed in this slice*
(the five M-lanes, the shared instruments, the nine U/V lanes). **§2B** is the
retrospective catalog `analysis/` built of the *previous* codebase — those
implementations live in `pipeline/` and `campaign_87/`, so I give them compactly
with their measured numbers and a pointer, since another slice owns the code.

### 2A — methods executed inside beat88

#### m1-quotient-graph-cartography
- **Family:** structural-analysis / exact BFS
- **What it does:** Treats each circuit as a node in a graph whose edges are
  "move classes" (union crossing, double transposition, remove-1-add-2 then
  remove-2-add-1), and expands that graph deterministically and exhaustively,
  hoping the −1 transition is an edge between basins that random walking cannot
  reach.
- **Twist vs siblings:** No sampling and no score — every CPU-hour yields either
  an 87 or a certified "no 87 within these classes from these roots".
- **Measured performance:** **Dead by its own kill test.** All 3,293 products
  classified against the BFS'd *true* neutral component: **0 escapes (0.0 %)**
  across MC-A (2 products), MC-B double transposition (3,006), MC-C composition
  (81 + 204). Complete `C(56,2)` remove-2-add-1 shells on every expanded state:
  540 cores, ~830,000 complete k≤2 decisions, **zero descents to 87**. Real
  contribution: **corrected true gauge-component sizes** — 88@5 from-scratch
  2,187 = 3⁷; 88@5 derived 729 = 3⁶; 88@6 **10,935**; 88@8 third family
  **59,697**; 88@7 **112,833** (all closed). Only the two depth-5 records are
  products. Salvage result that stands: **36 oracle-VALID 89-gate states** from
  one 90-gate seed, 20 distinct canon buckets exported (7 at depth 5).
  (`beat88/methods/m1_cartography/FINAL.md`)
- **Retraction, important:** M1's first-round escape verdicts (MC-B 27.6 %,
  MC-C 47.7 % "PASS") were **artifacts** — escape was tested against the *local
  product* `core × ∏slots` instead of the component. On 88@7 the product
  under-estimates the component **464×**. Full account:
  `beat88/methods/m1_cartography/analysis/RETRACTION-escape-verdicts.md`.
  Standing rule left behind: `canon` is a dedup bucket key only; any
  distinctness/escape claim must classify against `shared.gauge.orbit_bfs`.
- **Cost:** 4 local + 6 pod cores, ~1 day (2026-08-13 → 08-14a retirement).
- **Code:** `beat88/methods/m1_cartography/{bin,lib}/` (notably
  `bin/t_escape_recheck.py` — the escape instrument done correctly, and
  `bin/t_corpus_check.py`).
- **Logs/results:** `beat88/methods/m1_cartography/runs/` (32 MB),
  `exports/` (88 K, 21 files), `FINAL.md`, `LEDGER.md`,
  `analysis/{escape-verdicts,b5-gauge-canonicaliser,quotient-map,move-classes,b1-integration}.md`.
- **Generality:** CIRCUIT-GENERIC. Move classes and the component BFS are about
  XOR closure; only the target set is instance-specific.
- **Phase-2 verdict:** dead-end as a search; **keeper as instrumentation** —
  `t_escape_recheck.py` is the correct way to ask "did this move class leave the
  gauge component?" for any new move class on any circuit.

#### m2-exact-window-decider-at-net-minus-2 (A1)
- **Family:** exact-window
- **What it does:** Takes a circuit that is *above* the record (an 89 or a 90),
  removes k masks, and asks a complete decider whether ≤3 new masks restore all
  32 outputs. On an 89 that is a net −2, i.e. an 87. Same decider the previous
  campaign used, aimed at a question whose YES is the goal instead of a question
  whose NO is a certificate.
- **Twist vs siblings:** identical code and cost to the campaign's certification
  sweeps; only the anchor stratum and the arithmetic of the answer differ.
- **Measured performance:** **Sampled tier CLOSED:** 24 anchors, **837,395 k=5
  windows, all irreducible, 1,680/1,680 planted controls green.** Superseded
  mid-lane by *complete small-core shells*, which are cheaper and are theorems:
  a complete k=3/b=1 shell settles core-3 for an 89 in **6 seconds**, where the
  sampled tier spent ~230 core-hours to say less. **Measured blind spot is in the
  sampler, not the decider:** 10k k=5 windows on a 90 catch a core-3 descent
  96.1 % of the time, core-4 **11.1 %**, core-5 **0.2 %**
  (`beat88/methods/m2_oracle/analysis/natural-descent-density.md`).
- **Cost:** pod 20–28 procs under PyPy for ~2 days.
- **Code:** `beat88/methods/m2_oracle/code/{a1_driver.py,a1_driver_b.py,a1_shell_driver.py,anchors.py,gen_windows.py}`.
- **Logs/results:** `beat88/methods/m2_oracle/runs/` (263 MB) and
  `pod_salvage/pod1|pod2/beat88/methods/m2_oracle/runs/` (1.1–1.3 GB);
  `windows/` (174 MB, 93 window files).
- **Generality:** MIXED — the decider machinery is circuit-generic; `TSET` and
  the anchor corpus are MixColumns-specific.
- **Phase-2 verdict:** **superseded-by-`m2-complete-small-core-shells`** for
  negatives, **keeper** as the only formulation whose YES is an 87.

#### m2-complete-small-core-shells (the "88 wall" / "89 wall")
- **Family:** exact-window
- **What it does:** Instead of sampling windows, enumerates the *complete*
  remove-k shell of a circuit at budget k−1 and decides every window. A completed
  zero-win shell is a theorem: no smaller circuit exists within that radius.
- **Twist vs siblings:** completeness rather than coverage; each run's output is
  a proof rather than a statistic. Complete `C(n,2)` and `C(n,3)` shells are
  cheap enough to run on entire populations.
- **Measured performance (all with planted controls; every negative a theorem):**

  | theorem | scope | scale |
  |---|---|---|
  | **88 wall, core-2** — no 87 within remove-2-add-1 | 36,810 orbits incl. **all 33,010** of the complete known 88 population | `runs/pop88_lab{0,1,2}.jsonl` = 11,004+11,003+11,003 rows, **0 cuttable** |
  | **88 wall, core-3** — no 87 within remove-3-add-2 | six canonical families + 506 random + 1,137 descent-reached 88s | `runs/k3b2_*.jsonl` |
  | **89 wall, core-3** — no 87 within remove-3-add-1 | **64/64** known 89 anchors | 1,872,640 windows |
  | **89 wall, core-4** — no 87 within remove-4-add-2 | 13/64 anchors complete (incl. shipped 89, Sun–Yang–Li, from-scratch) | 395,010 windows on the shipped 89 alone, 790/790 controls |

  Structural finding that outlives the arms: **tightness, not gate count, governs
  local reducibility** — every *tight* circuit from 89 to 97 has exactly zero
  core-3 descents; the only circuits that descend carry dead gates
  (`lad94_sym94`, 2 dead gates, 689 `FOUND_lad94_*` files, all 91–92 gates).
  A 97 nine gates above the record is as locally rigid as an 89.
- **Cost:** complete k=3/b=1 shell of an 89 = **6 s**. Complete `C(57,5)` shell of
  the record 89 = 4,187,106 windows, **reached 789,584 (19 %) before shutdown** —
  still open.
- **Code:** `beat88/methods/m2_oracle/code/{census_cut.py,gen_k3_shell.py,a1_shell_driver.py,exact_window.py,exact_k4.py}` (guarded copies of the deciders).
- **Logs/results:** `beat88/methods/m2_oracle/runs/{pop88_lab*,s89_lab*,l89b_lab*,census_pod*,census_inbox}.jsonl` (~200 MB).
- **Generality:** MIXED — same as above.
- **Phase-2 verdict:** **keeper, the strongest instrument in the slice.** Aiming it
  at another circuit needs only a new target set and a corpus of anchors.

#### m2-cuttability-census (with pre-registered signature analysis)
- **Family:** structural-analysis over exact labels
- **What it does:** Labels each gauge-orbit of a circuit population with a single
  exhaustive bit — "does its complete remove-2-add-1 shell contain a descent?" —
  then runs a *pre-registered* statistical analysis for which structural features
  predict that bit.
- **Twist vs siblings:** the analysis plan was written and committed before any
  label was computed (`LEDGER.md` 2026-08-14 "pre-registration, written BEFORE any
  label"), and every negative carries a planted-positive control at the same
  budget; a control miss aborts the run.
- **Measured performance:** **85,446 gauge-orbits labelled, 1,076 cuttable.**
  Signature that survived Bonferroni + ≥2-strata replication: **neutral repair
  richness** — `deg_max` (AUC 0.913, median 8 cuttable vs 5 rigid), `deg_mean`,
  `sh_out_neutral`, `sh_out_repairs` — all four measuring one quantity. Explicitly
  rejected as source-confounded / non-replicating: `sh_fixed_masks` (AUC 0.935 but
  fails cross-stratum), depth, ρ²-fraction. Excluded as label-leaky:
  `sh_out_improving`, `sh_out_total`. Corpus lesson: **line counts are not corpus
  size** — the "107k 89-cluster" is 42 gauge orbits, and `layer89`'s 19.7 %
  cuttability is an artifact of the file's ordering (its first 60k records;
  0.03 % thereafter).
- **Cost:** measured ~5,800 orbits/hour on a 6-way local pool.
- **Code:** `beat88/methods/m2_oracle/code/{census_cut.py,census_watch.py,census_controls.py,census_analyze.py,cuttable_breakdown.py,pop88_reps.py,stratum89_reps.py,layer89_more.py}`.
- **Logs/results:** `runs/census_*.jsonl`, `runs/census_watch.log` (92 K),
  `analysis/cuttable-breakdown.md`.
- **Generality:** CIRCUIT-GENERIC given a decider and a gauge canonicaliser.
- **Phase-2 verdict:** **keeper.** It is the campaign's alarm system (a cut on an
  88 *is* an 87) and its retention-bias oracle for any future fleet.

#### m2-union-subset-and-PB-covering-SAT (A2)
- **Family:** SAT-joint-levels / pseudo-Boolean
- **What it does:** Instead of bounding the radius around one circuit, bounds the
  *universe*: "is there a realizable ≤87-mask subset of the union of these known
  circuits' masks?" Radius-unbounded — a YES anywhere in the pool is an 87.
- **Twist vs siblings:** the only exact question in the campaign that is not
  local to some anchor.
- **Measured performance:** **427 UNSAT verdicts, 0 SAT**, across CP-SAT, the
  fast band, and the PB escalation. Fast band: **118 pools, 118 UNSAT, max 5.6 s.**
  The **PB/covering encoder (`a2_pb_union.py`) is called "the single biggest
  capability gain"** of the lane — it decided in seconds pools a pre-registered
  "pair-density law" had predicted were impossible. That law itself is a first-rate
  methodological negative: it pre-registered, went **6/6 out-of-sample**, and was
  still **an artifact of the CP-SAT encoding, not a fact about the problem**.
  *Out-of-sample replication tests the law, not its subject.*
- **Cost:** 2 local cores; individual pools seconds to 7,200 s caps.
- **Code:** `beat88/methods/m2_oracle/code/{a2_union_sat.py,a2_pb_union.py,a2_pb_escalate.py,a2_fastband.py,a2_pair_density.py}`.
- **Logs/results:** `runs/a2_*.{jsonl,log}` (~250 K).
- **Generality:** CIRCUIT-GENERIC — needs only a mask universe and a target set.
- **Phase-2 verdict:** **keeper**, and the escalation ladder (pairwise unions →
  cross-lane core ∪ basin vocab → the full 1,979-mask vocabulary) was never
  climbed to the top.

#### m2-slot-order-free-window-SAT (A3)
- **Family:** SAT-joint-levels
- **What it does:** Encodes a window as "these kept masks must each equal *some*
  free slot's value", removing the arbitrary slot ordering that made earlier
  window-SAT UNSATs caveated.
- **Twist vs siblings:** the CNF is a function of the kept *set*, so an UNSAT is
  a real theorem rather than a statement about one ordering.
- **Measured performance:** **408-job run at maxslots 12 → 399 UNSAT, 0 SAT.**
  Cost curve measured on real windows: 9 slots 4.4 s, 11 slots 9.7 s, 12 slots
  **76.0 s** — ~7.8× per slot, extrapolating to ~600 s at 13 and ~4,700 s at 14.
  **Recommendation recorded: do not run the 13–14 escalation** (order 10⁴
  core-hours).
- **Code:** `beat88/methods/m2_oracle/code/{a3_window_sat.py,gsat_sbd.py,a3_sbd_headtohead.py}`.
- **Logs/results:** `runs/a3_results.jsonl`, `runs/a3_run.log`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper, but blocked on encoding** — a slot bump is not
  affordable; the next gain needs an encoding improvement (incremental SAT /
  cube-and-conquer were never installed).

#### m2-cone-window-exact-synthesis (A4) + the SB-D symmetry break
- **Family:** exact-window / SAT
- **What it does:** Cuts a window by *output cone* (pick 16 of 32 outputs, delete
  every mask private to them) and exactly re-synthesizes that sub-circuit with one
  fewer gate. Every deleted slot is free by construction.
- **Twist vs siblings:** window chosen by circuit structure rather than by k, so
  there is no slot-order caveat at all.
- **Measured performance:** **Kill test met.** The frontier is ~10–12 free slots;
  the literal |O| = 16 cone problem needs **31–34 slots** — the THESIS's "15–18
  private masks" was an *interior-only* count and never described a reachable
  instance. **7 genuine cone UNSAT theorems banked** (on cones whose controls
  passed; the driver declined to ask the real question on any cone whose control
  had not resolved — controls 8/8 then 4/6 + 2 timeouts, **0 refuted**).
  **THE KEEPER: SB-D symmetry breaking** — slots sorted by non-decreasing depth,
  equal-depth neighbours tie-broken by mask lex. Sound and complete; mutually
  exclusive with SB-F. **19.6 s vs 222.7 s head-to-head (11×) ≈ +3 slots of
  reach** on cone geometry. Second finding: **the depth cap is a major cost
  driver**, so gate-count-only questions should run at loose caps.
- **Important negative on SB-D's transfer:** ported to A3 it is **1.21× SLOWER**
  (SB-F 26.2 s vs SB-D 31.8 s over 9 decisive pairs), because A3 runs `cap=None`
  and SB-D must pay for a full depth ladder it does not otherwise need. The
  head-to-head harness *first printed "SB-D DISAGREES — UNSOUND"* and was wrong —
  it compared a `timeout` against an `unsat`. Fixed to classify only sat-vs-unsat
  as unsound. Recorded as a near-miss false alarm.
- **Code:** `beat88/methods/m2_oracle/code/a4_cone.py`, `gsat_sbd.py`.
- **Logs/results:** `runs/a4_results.jsonl`, `runs/a4_cone.log`.
- **Generality:** CIRCUIT-GENERIC (cone structure is generic; the 16-output split
  is MixColumns-shaped).
- **Phase-2 verdict:** **dead-end as specified** (frontier 10–12 vs 31–34 slots);
  **SB-D is a keeper for any depth-capped encoder.**

#### m3-mass-basin-census (the fleet)
- **Family:** plateau-search at fleet scale, under invented intrinsic coordinates
- **What it does:** Runs thousands of cheap descents from freshly constructed
  roots that read no existing circuit, and archives every state by an *intrinsic*
  descriptor (per-output ASAP depth profile, ρ²-defect band, gauge canon) rather
  than by distance to known circuits. The archive is the objective: descents whose
  descriptor is already known get killed at the ~100-gate waypoint.
- **Twist vs siblings:** earlier archives measured "distance to known families",
  which is provably blind to productive-vs-barren *unknown*; this one measures
  novelty intrinsically. Also harvests the 89/90 strata and depth ≥ 7 strata as
  first-class output (the old archive's depth-Pareto gate discarded 12 of 14 new
  families).
- **Measured performance** (`beat88/methods/m3_census/FINAL.md`):
  **6,304 descents, 747 core-hours, 1,546,597 oracle-verified ≤88 claims,
  2,722 new families, 12,596 novel 88-orbits handed to the labeller, 5,268
  labelled exhaustively, 0 cuttable, 1 depth record (91@4), 0 eighty-sevens.**
  Supporting counters: 3,679 descents killed at the waypoint by descriptor
  triage; 15.2 M archive cells suppressed as gauge duplicates; 12.0 M equal-gate
  elite swaps under the `deg_max` bias; **2,274 firings of M1's k=5 escape hatch,
  0 hits**; 462 roots rejected as depth-illegal.
  Five things it *proved*: (1) reaching 88 is cheap and the supply of 88-families
  is large (2,722 in 747 core-hours vs the old campaign's 13 CPU-hours per
  family, marginal rate never saturating); (2) **the 88 plateau is rigid at the
  shape we can decide exhaustively** — 7,125 orbits across structurally
  independent generators, every one proved to admit no remove-2-add-1 net −1 cut;
  (3) the depth axis is softer than the gate axis (92@4 → 91@4 fell in four
  minutes of one core; 97@3 and 88@5 never moved; depth-capped components are
  tiny cages — **644 distinct states at cap 3, measured live**); (4) **roots are
  RNG seeds, not structural donors** — all four arms statistically
  indistinguishable at the 100-gate waypoint; (5) determinism is worth building
  for — iteration-denominated budgets made every descent bit-replayable and
  turned engine changes into same-trajectory A/Bs, which is how the pure-C kernel
  was caught landing **two gates worse at equal iterations while looking 5.5×
  faster on the clock**.
  Honest limits it states: the row-depth descriptor has **no resolution at the
  100-gate waypoint** (84 independent descents, pairwise Hamming 18–32 of 32,
  0 % kill at any radius); the triage is worth **1.31×, not an order of
  magnitude**; 4,732 of its orbits were still unlabelled at close.
- **Cost:** 747 core-hours over ~70 lanes on three hosts, 2026-08-13 → 08-15.
- **Code:** `beat88/methods/m3_census/code/{descent.py,archive.py,roots.py,m3descriptors.py,m3kernel.py,backend.py,replay.py,anneal3.py,k5.py,cuttability.py,ledger.py,waypoint_census.py,calibrate_radius.py,validate_engine.py}`, `fleet.sh`, `ship_harvest.sh`, `run_{local,pod,pod1_skeleton}.sh`.
- **Logs/results:** `runs/` 6.8 GB local + 12 GB pod1 + 18 GB pod2;
  `exports/` 1.3 + 2.8 + 2.6 GB; `analysis/00–05*.md`.
- **Generality:** MIXED. Engine, archive, descriptors and replay are
  circuit-generic; `mcore.py`'s target set and the ρ² symmetry are MixColumns.
  Aiming it at `aes_inv_mixcolumns` needs: a new target set, a new instance
  automorphism for the ρ²-defect coordinate (or drop it), and re-measured root
  distributions.
- **Phase-2 verdict:** **keeper as a corpus generator, dead-end as an 87 hunt.**
  Its own words: "searching harder in the same shape has a well-measured expected
  value now, and it is zero."

#### m3-depth-capped-lane (how the 91@4 record was actually made)
- **Family:** plateau-search with a hard depth constraint + a from-scratch
  constructive root
- **What it does:** Compose two things neither of which works alone: a
  partition/pairing annealer (`anneal3`, run as pure ILS with **no SA phase at
  all**) that builds a depth-3 root from the MixColumns spec itself reading no
  file, then a `--cap 4` walk that refuses any state whose ASAP depth exceeds 4.
- **Twist vs siblings:** depth is a *constraint*, never a tie-break, and the lane
  is restart-heavy rather than long-walk, because depth-capped components are
  measured cages (644 distinct states at cap 3, then nothing).
- **Measured performance:** **91 gates at depth 4** — beats the project's own
  92@4. I re-verified today:
  `python3 verify_circuit.py beat88/methods/m3_census/exports/RECORD_mixcolumns_91gates_depth4.json 4`
  → `gates=91 depth=4 outputs_built=32/32 problems=0 / depth<= 4: OK / VERDICT: VALID`.
  34 distinct verified 91@4 circuits locally, 32 distinct gauge orbits,
  `live_gates == 91` on every one; **pod2's manifest holds 15,650 further
  91-gate depth-4 records** (see LEADS). Against the archived 92@4: plain J 0.346,
  periphery J 0.144, row-depth Hamming 11 — a different circuit. Replayable
  bit-for-bit: `replay.py --spec 'anneal3' --root-seed 6130 --walk-seed 6137
  --iters 363964`. **Neither half would have done it**: the annealer stops at
  97–99, and a generic capped walk from a naive root stalls at 96 under cap 4
  (and at **111** under cap 3).
- **Cost:** the 92→91 step took **four minutes of one core**; roots cost ~25–37 s
  each in pure Python.
- **Code:** `beat88/methods/m3_census/code/{descent.py (--cap/--claim-max),anneal3.py,roots.py,replay.py}`; write-up `analysis/05-depth-capped-lane.md`.
- **Logs/results:** `exports/RECORD_mixcolumns_91gates_depth4.json`,
  `exports/DEPTH_RECORD`, `exports/FRONTIER.json`.
- **Generality:** MIXED — the cap machinery is generic; `anneal3` is
  **MC-HARDCODED and depth-3-only** (its emitter cannot express depth ≥ 4, and
  target weights 5/7 are baked in).
- **Phase-2 verdict:** **keeper — the highest measured return-per-core in the
  whole slice**, and the one that produced a publishable record. The
  gates-vs-depth Pareto frontier it leaves is
  `{3:97, 4:91, 5:88, 6:88, …, 16:88}` (`exports/FRONTIER.json`).

#### m4-fixed-87-infeasible-population-search
- **Family:** evolutionary / quality-diversity over program genomes
- **What it does:** Fixes the program length at exactly 87 gates — almost always
  infeasible — and scores by how many of the 32 targets it builds, over a batched
  numpy verifier at ~400 k circuits/s. The search never touches the 88 plateau and
  never walks feasibly.
- **Twist vs siblings:** the genome is the *derivation* (a gate list), a
  representation the value-set frame quotients away; and the objective is
  distance-to-feasible rather than gate count.
- **Measured performance:** **Dropped on day 1 by its own pre-registered kill
  test, harder than written.** `32 − built` has no signal outside balls of radius
  ≈ 8–10 operand edits around circuits already owned: **99.91 % of random 87-gate
  genomes score 0; 99.996 % of all local moves are neutral**; the *complete*
  one-edit shell of *every* one-gate truncation of all five known 88s and the 89
  (529 base genomes, **6,832,408 genomes, exhaustive**) contains **zero** genomes
  at 32/32 with live ≤ 87, best score 31. The decisive control is **Control B,
  which fails**: at fixed length 89, seeded from 3-gate truncations of the 92@4,
  the search reaches only 30 of 32 (steepest ascent) / 29 (QD, 203,770
  evaluations) even though a valid 89 provably exists and ships. So the 87 hunt's
  failure (31/32 over 208,329 evaluations) **carries no information**.
- **Cost:** ~1 day, 2 local cores. The 87 hunt itself was 420 s.
- **Code:** `beat88/methods/m4_inverse/{verifier.py,genome.py,search.py,scan_thinker_c.py,realize_completion.py}`.
- **Logs/results:** `out/{landscape.json,control_recover.json,control_89.json,hunt87.json,thinker_c_rebase.json,rebase_control.json,shell_all.json}`, `analysis/landscape.md`, `LEDGER.md`.
- **Generality:** CIRCUIT-GENERIC (the failure mode is about XOR having no metric,
  which transfers).
- **Phase-2 verdict:** **dead-end**, cleanly and cheaply killed. But it left three
  keepers: `verifier.py` (adopted as shared B2), `realize_completion.py`
  (value-set → program → oracle in one call), and one open door — use **`r2`
  (targets within one pair-sum), not `32 − built`**, the only relaxation measured
  with real gradient.

#### m4-thinker_c-exhaustive-completion-scan
- **Family:** exact enumeration over a relaxed population
- **What it does:** Uses the sound reduction "an 87 exists ⟺ some 86-mask,
  31-target state completes", and exhaustively re-bases and scans the entire
  31-target population the previous campaign had generated and never analysed.
- **Twist vs siblings:** it *closes* a whole pre-existing population rather than
  searching a new one.
- **Measured performance:** **629,274 states scanned, 282,970 at |S| = 86, 0
  completions, 6,487 positive controls at |S| = 87.** The completion predicate was
  validated by the only authority that counts: `realize_completion.py` turned 12
  of them into circuits, **12/12 VALID at 88 gates**. Net effect: the thinker_c
  population is **CLOSED** and no other lane need spend budget there.
- **Cost:** hours, 2 local cores.
- **Code:** `beat88/methods/m4_inverse/{scan_thinker_c.py,realize_completion.py}`.
- **Logs/results:** `out/thinker_c_rebase.json`, `out/rebase_control.json`.
  ⚠ The 6,487 verified-88 completions are **counts only — not materialised on
  disk**; using them as donors needs `scan_thinker_c.py` re-run with a dump.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper** — the pattern "find a sound relaxation whose
  population already exists, then close it exhaustively" is cheap and produced a
  real theorem-shaped negative.

#### m5-backbone-obligation-calculus + the physical k−1 search (`shot87`)
- **Family:** structural-analysis → exact search
- **What it does:** Decomposes an 88 into a *core* (masks constant across its
  local neutral component) plus `k` repair coordinates, computes the core's
  pending **components** (= repair obligations), and then asks physically whether
  the core can be finished with `k−1` gates — which would be an 87.
- **Twist vs siblings:** the unit of analysis is a *family/core*, not a circuit or
  a window; and the search is over gate-constructions from the live closure with a
  set-cover lower-bound prune, not over mask windows.
- **Measured performance:**
  - Phase A profiled **all 204 families, 0 errors**:
    `k ∈ {4:2, 5:29, 6:60, 7:59, 8:39, 9:9, 10:6}`; `all-ternary` **54 yes / 150
    no**; `comps − k` ∈ {−2:2, −1:6, 0:40, 1:53, 2:37, 3:36, 4:20, 5:8, 6:2}.
  - Phase B decided **22 of 204: 15 sound NO-87, 7 INCONCLUSIVE at the 25 M node
    cap, 22/22 planted controls PASS.** Node counts 25,190 → 20,901,823; largest
    sound negative `f91b_7|d11` at 19,833,401 nodes.
  - **The headline structural fact:** `n_components ≥ k` in **60 of 62** profiled
    families — a family almost always has at least as many independent repair
    obligations as it spends gates, and in 26 families exactly one more. *That is
    the structural reason 87 is hard here: the obligations are already nearly in
    bijection with the gates.*
  - **Four distinct gauge orbits** are provably (modulo an E3 caveat) unable to
    finish with `k−1` gates — the obstruction is not unique to any one family.
  - **Negative on the incumbent "22+5 backbone" picture:** it is **family-local,
    not a property of 88-gate circuits.** Only 17 of 62 families have all slots
    ternary; the rest carry exchange classes of size 5–11. Cores run 78–83, so
    "the" 22-mask backbone is anywhere from 18 to 26. **No lower bound can be
    built on it.**
  - A soundness bug caught before it shipped: an early prune (`|R| > gates_left +
    free`) returned "NO COMPLETION, 5,990 nodes" in 6 s for the campaign's top 87
    lead — a confident false negative, because one mask can serve several
    components. Replaced with an exact set-cover DP bound over all `2^ncomp`
    subsets. **The 6-second runtime was itself the tell.**
- **Cost:** Phase A ~10 min on 30 pod procs; Phase B ~1 h/family at the 25 M cap.
- **Code:** `beat88/methods/m5_backbone/{m5,pending,abstract4,e3fix,routing,cash}.py`
  and `verify/{shot87.py,census.py,run_census.py,sweep87.py,close42.py,close_core.py,fiber10.py,fourgate.py,neg39.py,m5lib.py}`.
- **Logs/results:** `verify/{census204_full.jsonl,phaseB_verdicts.jsonl,phaseB_run.log,phaseB_remaining.json,census_rows.jsonl,VERIFICATION.md,PHASE2.md,EVIDENCE_CROSSCHECK.md,U1_DEFECTS_RESPONSE.md,STATE.md}` (744 K total).
- **Generality:** CIRCUIT-GENERIC — `Decomposition.from_circuit` is
  exterior-parameterised and runs on any circuit; obligations are a closure
  property.
- **Phase-2 verdict:** **keeper, and the most under-finished method in the
  slice** — 182 of 204 families never decided, including 7 of the 8
  compound-obligation frames that are the best leads (see §5).

#### m5-routing-constructor (demand-flow rerouting)
- **Family:** constructive / hand-reasoning
- **What it does:** Holds a circuit's mask set `A` frozen and re-routes only the
  *demand flow* (which gate serves which output), searching the fiber of routings
  over the same masks.
- **Twist vs siblings:** it changes nothing about which values exist, only how
  they are consumed — an axis no other method in the campaign touched.
- **Measured performance:** **108 → 99 gates by rerouting alone**, oracle-VALID at
  depth 4 (`verify/fiber_best_99gates.json`). Same masks, ≥5 gates apart.
  **The recursive descent past 99 was never run.**
- **Cost:** minutes (`fiber10.log`).
- **Code:** `beat88/methods/m5_backbone/routing.py`, `verify/fiber10.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper, unfinished** — "the routing axis is real and
  unexploited" (PHASE2.md §5.5).

#### m5-independent-reimplementation-verification
- **Family:** verification methodology
- **What it does:** Rebuilds an external document's claims from its *definitions*
  rather than its code, then checks each numeric claim against the oracle and the
  campaign's own census.
- **Twist vs siblings:** deliberately inherits no code, so agreement is evidence
  and disagreement is a finding.
- **Measured performance:** 8 verdicts. **Reproduced:** the (F,B) bi-mask layer
  (184 AES incidences; §5's table matched to three decimals on all eight archived
  circuits; both side-counts 57/97 and 28/88 exact); "15 of 4,459" exactly; both
  alien 88s reconstruct oracle-VALID. **Corrected:** the "243 = 3⁵ manifold" is
  actually **729 = 3⁶** once the sixth coordinate is unfrozen (729/729
  oracle-VALID). **Resolved:** the manifold is a *known* gauge orbit — its 5 planes
  are 5 of the derived 88@5's 6 triangle slots. **FALSIFIED:** the claim that the
  alien 88s lie outside the campaign's language — both are already in the
  850,784-state census, ids 511933 / 512103, same gauge orbit as the derived 88@5.
  Also found two defects in the source document (§40's 297, §42's E3 hole).
- **Cost:** ~1 day, ≤10 local cores.
- **Code/results:** `beat88/methods/m5_backbone/verify/VERIFICATION.md` (467
  lines), `EVIDENCE_CROSSCHECK.md`, `U1_DEFECTS_RESPONSE.md`.
- **Generality:** methodology, CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper as a protocol** — it is how the campaign priced
  outside claims without inheriting their frames.

#### shared-instrument-suite (B1–B5)
- **Family:** infrastructure
- **What it does:** Five validated primitives every lane imports: a C closure /
  feasibility / trim / complete-repair / complete-neighbourhood kernel (B1), a
  batched numpy verifier with a live-gate count (B2), a streaming population index
  (B3), intrinsic descriptors (B4), and a gauge canonicaliser (B5).
- **Measured validation** (`beat88/methods/shared/README.md`, all logs in
  `shared/analysis/`):

  | # | instrument | validation | result |
  |---|---|---|---|
  | B1 `kernel.py` | 60,001 randomised states vs `pipeline/engines.py` | **885,634 comparisons, 0 mismatches** |
  | B5 `gauge.py` | both closed 88@5 components, every state | 2,187 → 1 core; 729 → 1 core |
  | B2 `verifier.py` | M4's 25 checks + 100,009-circuit fuzz | 0 failures |
  | B3 `popindex.py` | 850,784 states, brute-force cross-check | 0 mismatches, 33 MB RAM |
  | B4 `descriptors.py` | vs `engines.relax`, the oracle, a Python enumeration | 0 mismatches |
  | — `fixes.py` (#10, #11) | 10,000 sets + a backwards-clock harness | 0 mismatches |

  Speeds: `feasible()` 8 µs, `trim()` ~25 µs, `repair_degrees()` ~5 ms, complete
  `neighbours()` 7–20 ms. Whole suite passes on local (gcc 13) and the pod mirror
  (gcc 11.4), ctypes only (the pods had no `cffi`).
  **Recorded hazard:** the C `trim` is witness-dependent — **14.5 % mismatch vs
  Python (327/2,253), concentrated entirely above 88 masks, 0/1,671 at exactly 88**
  (the unique-DAG boundary). Any structure that records trimmed states must not
  swap trim backends mid-stream.
- **Code:** `beat88/methods/shared/{kernel.py,gauge.py,verifier.py,popindex.py,descriptors.py,fixes.py,csrc/,lib/,tests/}`.
- **Data:** `shared/index/pop88/` (460 MB: `post.u32` 299 MB, `states.u16` 150 MB,
  plus 8 small `.npy`) — the built index over the whole 88-gate population.
- **Generality:** CIRCUIT-GENERIC except the target set in `kernel.load_circuit`.
- **Phase-2 verdict:** **keeper, port-first.** These are the cheapest thing to
  carry to `aes_inv_mixcolumns`: swap the target matrix and the suite runs.

#### understanding-program (U1–U7, V1, V2) — the theory half of the slice

After 2026-08-15 the campaign pivoted from searching to *understanding*, and this
is where the two publishable theorems came from. `understanding/CANON.md` (1,437
lines) is the authority: a statement enters only after a full write-up **and** a
second-agent check; computations only when an exact program on a stated finite
set was re-run independently. Below, one entry per distinct method; every lane
also carries a `NOTEBOOK.md` and (except u2, u5) a `PROOFCHECK.md`.

##### u1-obligation-calculus (`understanding/u1_obligations/`, 1.6 MB)
- **Family:** structural-analysis / combinatorial accounting
- **What it does:** Formalises "an 88 = gauge core `C` + `k` repair gates", defines
  an *obligation* as a connected component of the dead set, and asks exactly when
  `k−1` gates could finish the core (which would be an 87).
- **Twist:** it is the only lane that tries to make obligation cost a *number per
  obligation* rather than per frame.
- **Measured:** the counting identity `k = Σ_j m_j` holds **204/204** (+5,100
  witnesses). The conjecture `n_components ≥ k` is **FALSE — 8 of 204 violate**
  (M5 had found 2 of 62): `f91b_7|d8`, `mix_6|d12`, `rho_2|d14`, `rho_2|d7`,
  `m3a|d6`, `m3b|d14`, `m3k|d11`, `m3l|d10`. **Self-refutation, referee-forced:**
  marginal cost is **witness-dependent** (U1-8), so every compound/free/surplus
  column of the first census is a witness artifact — the whole D4.2 line is
  retracted in `NOTEBOOK.md` §14. Repaired by `canonical-cost-census`
  (`canon_cost.py`): a witness-free cost ρ, under which `n_expensive ≥ 1` holds
  203/204 and the disjunction `n_expensive ≥ 1 ∨ cover ≥ k` holds **204/204**;
  the cash law is exact **425/425**.
- **Generality:** the definitions (`cl`, `A`, `D`, obligations, `cons`) are
  CIRCUIT-GENERIC; the instrument is MC-HARDCODED through the 204-family census.
- **Verdict:** **keeper** (the ρ version); the witness-dependent version is
  explicitly RETRACTED.

##### u1-exact-k-minus-1-shell (|W| = 1 and |W| = 2) — the strongest exact negative
- **Family:** exhaustive completeness search over all 2³²
- **What it does:** Asks whether any `k−1`-set of the form `(R∖{r₁,r₂}) ∪ {g}` —
  or `(R∖{r₁,r₂,r₃}) ∪ {g₁,g₂}` — completes the core, for **arbitrary masks over
  the whole 2³² universe**, not a vocabulary. Completeness comes from an
  *unlock-event argument* (the first unlock must be E1 or E3), which restricts
  candidates to a provably sufficient finite set.
- **Twist:** the only 87-hunting instrument in the program whose negatives are
  exact over all 2³² **and** reached by an argument rather than by enumeration.
  The |W|=2 version adds a three-branch exhaustive case split, one of which (B3,
  "enabler-first") is the *deception-door* shape — a gate that unlocks nothing and
  exists only to make the next gate derivable.
- **Measured:** **U1-14** — 4,127 pairs, 28,167 exact states, **0 completions**.
  **U1-23** — 7,223 triples, 464,522 B1 pairs, 2,159,283 B3 pairs, 474,511
  B2/kernel tests, **0 completions**. Certified on 4,127 *true positives* with all
  three branches firing; screen accepts 4,127/4,127. Closed region: *delete ≤3
  repair gates, add ANY ≤2 masks, all 204 families.* Instrument certificate
  U1-24: `Repair.fast_unlock` validated on **815,974 cases, 0 mismatches**.
- **Code:** `u1_obligations/{pc_km1_exact.py,km2_exact.py,run_km2.py}`.
- **Generality:** MIXED — the completeness argument is CIRCUIT-GENERIC (it uses
  only the E1/E3 event taxonomy); retargeting needs a new target set, a corpus of
  near-optimal circuits for the new matrix, and a re-audit of `fast_unlock`.
- **Verdict:** **keeper — the best exact instrument in the understanding half.**

##### u2-walls-as-a-dataset (`understanding/u2_walls/`, 290 MB)
- **Family:** structural-analysis over the exact labels the search lanes produced
- **What it does:** Treats the campaign's millions of exact negatives and ~1,100
  positives (cuttable 89s) as a *dataset* and asks what smaller object separates
  cuttable from rigid.
- **Measured, and this lane's results are unusually sharp:**
  - **Dataset:** 90,110 rows → **89,744 unique orbits, 0 label disagreements**;
    1,076 cuttable (89: 1,063 · 90: 8 · 91: 5 · **88: 0**); 1,143 distinct cuts,
    1,140 aligned at ρ-rotation k=0, no alignment failures.
  - **The lineage-independence control — the lane's most important result.** At
    Jaccard ≥ 0.90 the 1,063 cuttable orbits collapse to **13 clusters** (largest
    686, then 295; two basins hold 92 %), while a size-matched rigid null gives
    850 clusters. **Every statistic computed over "1,076 cuttable orbits" has
    effective n ≈ 13.**
  - **Cut factorization (H2): 1,121 / 1,121 cuts factor in BOTH orderings, zero
    exceptions, in 6.1 s.** A cut is *not* a two-gate rearrangement — it is **one
    mask `c` whose addition kills two gates at once**. The added mask takes only
    **49 distinct values (29 up to ρ)**, and **92.2 % of all cuts ever found add
    one of just two masks** (`08808c0c` 47.8 %, `0808848c` 44.4 %).
  - **Repair-relation marginals:** cuttability of a tight circuit ⟺
    `max_w vac(w) ≥ 2`, **299/300** against the exhaustive label; **`deg_max ≤ 4
    ⟹ rigid`, 0 / 22,247**, screening 48 % of the tight-89 corpus. **And it
    refutes the campaign's own retention advice:** `P(cuttable | deg_max)` is
    **non-monotone** — peak 29.7 % at `deg_max = 10`, **0 % at 12 and 14** — so
    "prefer `deg_max ≥ 13`" is wrong.
  - **Collision mechanism:** H3 (collision = self-dependence) is **dead** — the
    repair is still constructible in **480/480**. What separates cashing from
    colliding is **adjacency of the served pair** (`m₁⊕m₂ ∈ S ∪ INPUTS`): 58.8 %
    vs 10.4 %, a **5.6× rate ratio**, neither necessary nor sufficient. Among
    high-mobility *rigid* circuits, **53 of 100 already have a doubly-serving
    repair and are stopped purely by collision.**
  - **Within-lineage descriptor control:** `deg_max` AUC **0.823 naive → 0.662
    within-lineage** (half the signal is lineage confound); `sh_out_neutral`
    **dies** (0.555) despite being one of the four named signature descriptors;
    `sh_fixed_masks` **survives** at 0.660 — the campaign had rejected it using
    cross-*source* replication, the wrong control.
  - **Chain-rule retraction:** the chain rule minted **1** novel 88-orbit, not
    1,137 — 1,114 of 1,115 cut-children were already in the pre-chain index. Root
    cause: `gauge.canon` returns a 128-bit core hash but `cores.npy` is `uint64`
    and stores the **low 64 bits**. Standing rule adopted: membership is
    `PopIndex.find()`, never `cores.npy`.
  - **Per-gate re-sweep (the U4 hand-off):** 3,441 circuits, **307,694 gates**.
    Population A (27 extreme-sharing gates): **25 of 27 buy the single mask
    Λ = 0x80808080**, none in a 91/92/97. Population B (drop-0 "useless" gates)
    **enable nothing** — and the placement hypothesis *inverts*: 88s carry **1.99
    drop-0 gates each vs 0.41 for 97s (5×)** and place them **later**.
  - **Λ probe:** `deg(Λ) = 0` in **100/100** circuits containing it (baseline
    P = 0.834, so all-100 by chance ≈ 1.3 × 10⁻⁸); Λ is never a valid repair
    column where absent. Λ-containing tight 89s cut at **0.02 % vs 2.76 % — 138×
    less** — but the lineage control shows none of the 2,205 orbits in any *mixed*
    basin contains Λ, so it is a basin marker, usable as a screen, **not** as
    evidence.
- **Dead in u2, with cause of death recorded:** the T1–T5 algebraic cut-type
  ladder (T3/T4 split is an artifact of the ladder's own ordering); and the
  Φ-drop parity lemma, **refuted by its own checker with drop-30–32 witnesses in
  every parity class** — because 4 of the 32 inputs (`e₇, e₁₅, e₂₃, e₃₁`) are
  themselves φ-odd.
- **Generality:** methods CIRCUIT-GENERIC, data MC-HARDCODED. Note this lane is
  the **only unrefereed lane**, and the one part of it that was refereed was
  refuted.
- **Verdict:** **keeper — the highest density of transferable methodology in the
  slice.** The lineage-independence control in particular should be applied to
  every corpus-wide statistic the campaign published.

##### u3-column-zeroing-lower-bound (Theorem A) → `L(M) ≥ 51`
- **Family:** gate-elimination combinatorics
- **What it does:** Picks a column set `K` such that `M|_K` has 32 pairwise-distinct
  rows of weight ≥ 2; zeroing each of the `32−|K|` outside columns provably kills
  ≥ 1 gate, and the surviving matrix still needs 32. Bound = `(32−|K|) + 32`.
- **Twist:** entirely solver-free — thirteen integers and a five-line argument.
- **Measured:** `L(M) ≥ 51` with `K = [2,8,10,13,15,18,20,21,22,23,24,29,31]`.
  **51 is the EXACT optimum of the technique**, upgraded from MILP-asserted to
  exhaustively proved: **all 462,411,532 subsets of [32] of size ≤ 12 enumerated
  in C.** On **Mᵀ the same technique gives only 49**, so the transposed frame —
  the campaign's one free change of frame — is *worse* as a proof frame.
- **Cost:** verification is instant (`python3 verify_bound.py`, stdlib, 1 s).
- **Generality:** **CIRCUIT-GENERIC and explicitly so — which is its own stated
  ceiling.** `RESULT.md` §6: "the argument nowhere uses the fact that this matrix
  is MixColumns"; on a random invertible 32×32 it would give a *larger* number.
  Retargeting to `aes_inv_mixcolumns` is a **one-line change** and would likely
  give a **better** bound, since inv-MixColumns rows are denser and survive more
  column-zeroing.
- **Verdict:** **keeper — publishable, unpublished.**

##### u3-minE-forced-extras (Theorem B) → `L(M) ≥ 54`
- **Family:** bounded exhaustive realizability search
- **What it does:** At a keep-set `K`, computes `minE_K` = the fewest extra masks
  that must be adjoined to the restricted rows to make them realizable over the
  kept inputs. Bound = `(32−|K|) + 32 + minE_K`.
- **Twist vs Theorem A:** it is the only place in either bound lane where more
  compute buys more bound.
- **Measured:** `L(M) ≥ 54` at `|K| = 14`; a second, largely-disjoint keep-set
  gives 54 independently. **The phase transition is sharp:** `minE = 0` at
  `|K| ≤ 13` and `≥ 4` at `|K| = 14` — and `minE = 0` was verified on **all 72**
  `|K|=13` keep-sets with `q = 32`, so **Theorem B provably adds nothing at the
  Theorem-A optimum.** Verified by **three independent implementations** (pruned
  Python, unpruned Python, a referee's C searcher validated against brute force on
  700 random small instances).
- **Cost:** depth 3 = **7.0 M nodes / 286 s** on one core in Python (a 30k-node /
  1.2 s variant already gives ≥ 53). Depth 4 (→ 55) is ~10⁹–10¹⁰ nodes: out of
  reach in Python, "plausible in C, ~hours on 2 cores".
- **Verdict:** **keeper** — and by U3's own §7 the highest bound-per-hour work left.
- **Context number worth carrying:** the *counting* bound for this dimension is
  **73–74** — i.e. almost every invertible 32×32 needs ≥ 74 — and the record 88
  sits above it. That is why "prove 88 optimal" is not reachable by counting.
- **Dead routes in u3, each with a cause of death:** output-side (transposed)
  elimination is **provably vacuous** (Tellegen accounting cancels the gain
  exactly — only input-side elimination has teeth); fanout refinement is blocked
  because `K` must be fixed before the circuit is known; the cancellation-free
  knapsack gives 47 < 51 (**but see LEAD U-9 — U6 revived exactly this object and
  got 92**); Valiant superconcentrators do not apply; and the Boyar–Peralta
  potential route is **REFUTED** — `sup maxdrop = 32`, attained by an explicit
  construction embedded in an oracle-verified 188-gate SLP. Standing instruction
  in the notebook: *"do not re-derive maxdrop ≤ 6. It is false."*
- **Integrity incident, recorded on purpose** (`u3_lowerbound/NOTEBOOK.md` §5): an
  earlier revision carried a confident citation table written **before any search
  result was in hand**; withdrawn in full and caught only by checking timestamps.
  Rule adopted: no citation enters without retrieved text or an explicit tier label.

##### u4-cut-trajectory-economy (`understanding/u4_economy/`, 22 MB)
- **Family:** conservation laws over telescoping cut functionals
- **What it does:** Defines the cut `A_k = inputs ∪ {g₀…g_{k−1}}`, runs a backward
  demand pass over the suffix, and checks the cut identity at every one of the
  `n+1` cuts; then measures expression mass `L`, factorisation area `V`, and
  cancellation debt `D = V − 184` along the whole trajectory.
- **Measured:** corpus **26,222 verified circuits / 2.32 M gates**. Laws verified
  with **0 violations**: `L₀ = 184`, `Lₙ = 32`, `V₀ = Vₙ = 184`, `D_k ≥ 0` at
  every cut, `L ≥ 152`. **The one genuine conservation law is `V`** — area returns
  to 184, an invariant of the AES matrix rather than of the circuit.
  **The efficiency inversion:** the greedy-108 sits *exactly on the floor*
  `L = 152` with debt 0 at every cut — and is the **worst** circuit measured;
  `W = L − 152` runs 0 → 18 → 52 → 60 → **92** down the 108 → 97 → 92 → 89 → 88
  ladder. At *fixed depth* the premise inverts outright: 89-gate circuits serve as
  many or more outputs per gate than 88s from depth 7 up (AUC(89>88) = 0.78 for
  `s̄`, **0.87 for `V`**), and the correlation of `s̄` with gate count at depth 8 is
  **+0.26 — the wrong sign for the whole premise.**
- **Verdict:** **keeper.**

##### u4-counting-LP-as-a-method-ceiling — why the counting route is closed
- **Family:** LP duality over a basis of cut functionals
- **What it does:** Builds a basis of symmetric cut functionals and solves
  `max ⟨u, swing⟩ s.t. ⟨u, Δφ_k⟩ ≤ 1` over every observed per-gate increment
  vector. **The optimum is the best bound *any* linear counting argument over that
  basis could ever give.**
- **Twist:** the only instrument in the campaign that prices a *whole class of
  proof techniques* instead of trying one.
- **Measured:** 23-functional basis over **44,738 distinct increment vectors** of
  2.32 M gates → **n ≥ 37.85**. The control recovers the trivial bound exactly.
  An enriched 86-dimensional basis over 43,947 increment vectors → **n ≥ 46.21**.
  *"Multiplying the basis by 3.7× bought 18 %, against a factor of 1.9 still
  needed."*
- **The uniformity theorem (U4-5), the reason this matters:** any cut functional
  whose endpoints are fixed by `M` yields a bound of exactly
  `88 · (mean Δφ / max Δφ)` — **hence never above 88**, and equal to 88 only if the
  increment is constant on every gate of every 88. Measured uniformity ratio:
  **0.43–0.53.** **Design consequence, the single most actionable sentence in the
  understanding half:** *introduce a quantity whose endpoint values are NOT
  determined by `184 → 32`.* U6's price certificate is the one such quantity in
  the whole program, and it is the only one that clears 88.
- **Generality:** CIRCUIT-GENERIC machinery (it is a theorem about the shape of
  counting arguments); the conclusion is MC-specific.
- **Verdict:** **keeper — the most transferable idea in the lane.**

##### u4-boyar-peralta-drop-profile
- **Family:** rigorous potential accounting
- **Measured:** `max drop ≤ 6` is **FALSE** — 27 gates in the corpus at drop 7/8/9,
  re-verified by an independent non-incremental second pass. Drop-9 witness:
  `beat88/methods/m3_census/exports/m3_family_89g_d7_u36_m3j.json` gate 43 buying
  `0x80808080`, Φ 71 → 62. **Of the 27 gates with drop ≥ 7, 25 buy `0x80808080`;
  only three distinct masks in the whole corpus can push a gate past 6.** Bound
  arithmetic: universal caps degrade monotonically with corpus size
  (88 → 82 → 76 → 66 → 62); provable today is `⌈152/9⌉ = 17`, below trivial.
- **Verdict:** **superseded as a bound route** (the lane says so itself) but
  **keeper for its by-products** — the Λ discovery and the drop-0 gate population
  both came out of it.

##### u5-heavy-corner-projection-and-exhaustion (`understanding/u5_heavycorner/`, 2.0 MB)
- **Family:** linear projection + complete BFS
- **What it does:** Projects onto the four weight-11 columns {7,15,23,31} — the
  GF(2⁸) reduction bits. π is linear, so a gate's heavy class is the XOR of its
  parents': **the heavy world of *any* circuit is an SLP over a 16-element
  universe**, small enough to exhaust.
- **Measured:**
  - **U5-0, the matrix's only heavy-world identity:**
    `t₇ ⊕ t₁₅ ⊕ t₂₃ ⊕ t₃₁ = Λ = 0x80808080` — unique, established exhaustively
    (536,154 subsets of size ≤ 7 tested; `rank(P₀) = 23`, kernel 1-dimensional).
    All 276 pairwise XORs of `P₀` are distinct (a Sidon set); no heavy target is
    the XOR of two free masks. This **mechanically explains Λ's measured
    frozenness** in u2.
  - **U5-2 / U5-3, rank-based floors:** every circuit contains **≥ 19 route-A
    heavy gates**, hence **≥ 27 gates with nonzero heavy part** — stated for
    arbitrary SLPs, checked **204/204, 0 violations**, measured slack 13–22.
    **Explicit non-compounding result, recorded so nobody re-derives it:**
    `27 + 12 = 39 < 54`, and it does **not** add to Theorem B, because in a
    14-column projection `rank(P₀) = 23` collapses to ≤ 14.
  - **The exhaustive library:** exact cost-to-go over **all 1,857 reachable
    states**; **all 1,857 can still finish — the heavy corner never traps a
    constructor, it only prices one.** **4,510** plans at `c = 8` and **336,484**
    at `c = 9` fully enumerated. Cost law: heavy gates ≥ 19 + c.
  - **Census over 204 families:** heavy gates 43–51 (mean 47.6) against a floor
    of 27; classes realised `c` ∈ {9: 11, 10: 89, 11: 104} — **never 8**; and
    **not one of the 4,510 `c=8` plans is used by any known 88** (nor by 1,200
    further sampled 88s: `c ≥ 9` in **1,404/1,404**).
  - **The load-bearing negative:** the `c = 8` region is not unexplored — **the
    archived 97-gate depth-3 ladder lives there.** Across 97 → 92 → 89 → 88 the
    heavy corner *grows* 38 → 42 → 46 → 47.6 while light shrinks 59 → 50 → 43 →
    40.2. **A constructor that minimises heavy activity walks toward the 97, not
    toward an 87.**
- **Artifact:** `u5_heavycorner/heavy_corner_library.json` (1.3 MB) — self-contained,
  a function of `M_AES` alone.
- **Generality:** MC-HARDCODED constants, CIRCUIT-GENERIC technique. For
  `aes_inv_mixcolumns` the analogue is "project onto the anomalously heavy
  columns" — but the inverse matrix's column weights are uniformly dense, so the
  projection would be larger and probably less useful. **That is the main porting
  question for this method.**
- **Verdict:** **keeper**; ⚠ this lane has **no PROOFCHECK.md**, so its results are
  not in CANON.

##### u6-laminar-price-certificate → `L_cf(M) ≥ 92` — the best single instrument in the program
- **Family:** Lagrangian dual / projected subgradient ascent producing a
  **solver-free, exact-integer certificate**
- **What it does:** In a cancellation-free SLP every target is built as a *laminar
  hierarchy* over its support. Assign integer prices `n[t][m] ≥ 0` over a
  denominator `D`, with the column constraint `Σ_t n[t][m] ≤ D` (a mask is one
  gate however many targets want it). Then `B = (1/D)·Σ_t min_H Σ_{S∈H} n[t][mask(S)]`,
  each inner term a `2^{w_t}`-state subset DP over ≤ 128 states.
- **Twist — and this is why it is the only bound in the campaign that clears 88:**
  soundness needs three lines and **no optimality of the price table**, and it is
  the **only quantity in the program whose endpoint values are not fixed by
  `184 → 32`** — exactly the escape U4-5 demanded.
- **Measured:** `cert_exact.json` (D = 10⁶) → `B = 90.80458` → **`L_cf ≥ 91`**;
  `cert_exact_v2.json` (D = 10⁷) → `B = 91.0019782` → **`L_cf ≥ 92`**, refereed by
  delta-check. The improvement came from replacing a proportional rescale with a
  **true Euclidean projection** onto `{x ≥ 0, Σ_t x ≤ 1}` plus a Polyak step with
  the exactly-constant subgradient norm `‖g‖² = Σ_t(w_t − 1) = 152`.
  **Consequence: every XOR-SLP for MixColumns with ≤ 91 gates contains at least
  one cancelling gate.**
- **Cost:** **verify in ~2 s, stdlib only, solver-free.** Generation:
  `push.py 20000 10000000` ≈ 25 min.
- **Generality:** **CIRCUIT-GENERIC machinery, MC-HARDCODED certificate.** The
  hierarchy lemma, the DP and the pricing all take an arbitrary target set; the
  mask universe (1,648 masks here) is *derived* per matrix by Lemma 1, not
  assumed. Retargeting to `aes_inv_mixcolumns`: rebuild `TARGETS`, re-run the
  ascent, re-verify. **This is the most portable high-value method in the
  campaign.**
- **Verdict:** **keeper — refereed, publishable, unpublished.**

##### u6-two-price-lambda-lift → `U ≥ 2` cancelling gates, and a clean ceiling
- **What it does:** Two price families and a rational multiplier give
  `U ≥ (G(λ) − n)/(λ − 1)`, where `U` is the number of cancelling gates.
- **Measured:** `cert_u63_7_2.json`, `G(7/2) = 90.996546` → **`U ≥ 2` at n = 87 and
  at n = 88**; `U ≥ 1` at n = 90. All eight `cert_u63_*.json` numerators were
  re-derived to the digit by an independent exact-integer checker over a
  separately rebuilt `M`. **The lane originally left this in floating point and
  the referee caught it.**
  **U6-3′ — an exact NEGATIVE recorded so the compute is not spent again:**
  `U ≥ 3` is **not reachable by this instrument.** The measured curve `G(λ)` over
  λ = 2.85 … 3.75 tops the ratio `(G−87)/(λ−1)` out at **1.599**. Cause of death:
  per-target hierarchy costs **cannot be equalised** because the masks targets buy
  are shared, and the column constraints bind long before costs level. *"`U ≥ 3`
  needs a structurally better relaxation, not a better λ and not more ascent."*
- **Verdict:** **keeper**, and the `U ≥ 3` negative is a **keeper as a dead-end
  certificate**.

##### u6-spec87-joint-satisfiability — why "prove 88 optimal" was abandoned
- **What it does:** Takes every proven constraint on an 87 and asks whether they
  jointly pinch.
- **Measured:** **the certified joint floor of the entire proven hard spec is 54,
  not 88 — slack 33 gates. There is no pinch and no optimality proof.** `Σ drop =
  152`, `Σ ρ = 152` and `Σ serve ≥ 152` are all the *same* `152 = wt(M) − 32` in
  three coordinates, and the third is an **inequality**, never an equality
  (measured `Σ serve = 218` on the 88@5, 244 on the 88@6; only the greedy-108 sits
  at 152). The containment law caps **only the first gate**.
- **Verdict:** **keeper** — this is the document that closed the optimality route.
- **Dead in u6, each with cause of death:** "a nonzero cancellation count follows
  from the containment counting bound" (dead — counting permits `U = 0` at every
  `n ≥ 47`; **the laminar structure, not the counting, is what makes the
  certificate work**); "the optimal price vector is `p_m = 1/c(m)`" (dead
  instructively — that family's optimum is exactly `244/3 = 81.33`, **below 88**;
  the bound only crosses 88 once prices are made **target-dependent**); "87 vs 88
  shows up in the mean drop" (dead as a lever: 1.7471 vs 1.7273 against a per-gate
  range of 0…32).

##### u7-two-closure-representation (CANC) + cf-exact-synthesis
- **Family:** representation design + exact CP-SAT synthesis over a *proved* universe
- **What it does:** Splits any circuit as `n = |cfcl(S)| + |Dcf(S)|` — the
  cancellation-free closure plus "the masks cancellation cannot avoid". Then
  minimises a cancellation-free family exactly, over a universe proved complete.
- **Twist:** two structural facts do all the work and both are proved — (i) **no
  acyclicity encoding is needed**, because parts of a CF gate are strictly smaller
  subsets, so any derivation is well-founded by `|S|`, killing every level/order
  variable; (ii) **the universe is proved** — in a minimal CF family every member
  is contained in some required output, giving exactly **1,648 masks** for the 32
  AES targets. Model: 1,648 booleans / 12,604 split literals; a weight-w mask has
  `2^{w−1}−1 ≤ 63` splits against the ~4,000–6,500 pairs a general XOR encoding
  carries.
- **Measured:** **the greedy-108 is cancellation-free (`|Dcf| = 0`); the 88s
  destroy 23–33 masks. So the entire 108 → 88 gap *is* the cancellation layer.**
  Exact synthesis reached `CF(M) ≤ 103` with a lower bound of 79 and **was still
  closing when the run was stopped**. End-to-end planted positive: the
  88@5-derived plan re-synthesised at budget 65 and decoded to
  `verify_circuit.py: gates=88 depth=5 VALID`. Pre-registered dead: **`|Dcf|` as a
  quality score inverts at the frontier exactly like U4's `V`.**
- **Generality:** **CIRCUIT-GENERIC** — the 1,648-mask universe is *derived* from
  the target set by the lemma, so retargeting needs only a new `TARGETS`. (The
  universe will be much larger for inv-MixColumns; that is the cost question.)
- **Verdict:** **keeper, and unfinished.**

##### u7-tier1-cf-layer-reoptimization — THE campaign's cleanest structural result
- **What it does:** For each of the five canonical 88 donors, freeze the
  cancellation plan `Z` with the donor's own parent pairs, and **exactly minimise
  the cancellation-free layer over all 2³²**.
- **Measured** (each run < 1 s): 88@5 derived (|Z| = 23, own CF 65) → **65,
  OPTIMAL**; 88@5 scratch (27, 61) → **61, OPTIMAL**; 88@6 (30, 58) →
  **INFEASIBLE at 57**; 88@7 (27, 61) → **INFEASIBLE at 60**; 88@8 third (33, 55)
  → **INFEASIBLE at 54**.
  > **In all five canonical 88 families the cancellation-free layer is already
  > exactly optimal for its own required-output list, over the whole 2³² mask
  > universe. An 87 cannot come from building better.**
  Strictly sharper than irreducibility. Scope stated plainly: conditional on
  freezing `Z` *and* the donor's exact parent pairs.
- **Companion (tier-2 dropscan):** delete one element of `Z` and re-minimise.
  88@7 — **27/27 attempted, 26 proven necessary, 1 undecided, 0 droppable**;
  88@6 — 30/30 attempted, 19 necessary, **11 undecided (timeout)**, 0 droppable.
  **The 88s are tight in BOTH layers simultaneously.**
- **Verdict:** **keeper — the single best "why 88" result in the slice.**

##### u7-heavy-corner × plan join (U7 × U5)
- **Measured:** **the cancellation plan `Z` is essentially a choice of which
  targets to build by cancellation** — 24 of 27 `Z` elements are AES targets on
  the 88@7, 26 of 30 on the 88@6. U5's heavy class count `c` is the coarse
  coordinate sliding `|Z|` against `|cf|` **along the plateau at constant sum 88**
  (`c=9 → (23,65)`, `c=11 → (33,55)`). `Z` is heavy-enriched in every frontier
  circuit (59–75 %) and **heavy-POOR in the 97 (33 %)** — the cancellation layer
  *becomes* the heavy layer as circuits improve. Two universal heavy-critical plan
  elements appear in **7 of 7** circuits. **And the Λ coupling, priced:** a
  full-class mask is cheap to build (a disjoint union of four heavy inputs, living
  in the CF layer) but **every consumer of it toward a target must cancel**,
  because no target has heavy pattern `H` — "buy a gate that appears useless", now
  with a proof and a price tag. By U5-0 the four triple-class targets are linearly
  coupled through Λ, so any `Z′` removing one must account for the other three.
- **Verdict:** **keeper — the sharpest joint finding in the program.**

##### u7-tier3-plan-substitution — VOID, and instructively so
- **What it does:** Make *which targets are cancelled* and *what the cancelling
  gates' parents are* into CP-SAT decision variables, so one solve per plan size
  covers the whole plan space instead of enumerating ≥ 10¹² plans.
- **Measured — a triple failure, recorded in full:**
  - **tier3:** the planted positive **PASSES** (rediscovers an 88, decodes
    oracle-VALID, 21 s). All five real runs at budget 87 returned **UNKNOWN at
    ~5,944 s**. Void twice — procedurally (nothing decided) and substantively:
    the control passed only because the donor was one of the five circuits the
    vocabulary `W` was built from — **a circular control**.
  - **tier3b/sweepC** (pod2, 32 cores, 143 decided configs): **VOID.** A follow-up
    re-solve of four sampled INFEASIBLE-at-87 configs found **three of four are
    provably INFEASIBLE at budget 115 — twenty-seven gates above the record.**
    They were not expensive plans, they were *impossible* ones. sweepC measured
    plan incoherence, not the 87 question. **Rule earned: a negative from a
    sampled instance requires a positive control on a SAMPLED instance.**
  - **tier3c** (pool redesign, 4,036,311 CF literals): **UNKNOWN at 1,020 s, C1
    control FAIL.** The two constraints are in direct opposition — a real plan has
    1.05 children per overlap, so faithfulness needs `p ≈ K`, which is exactly
    what explodes the universe. **"There is no pool size that is both faithful and
    buildable."**
- **Verdict:** **dead-end as run; the design is a keeper** — the lane wrote a full
  successor-instrument spec (per-child overlap candidate sets) that was **designed,
  sized, and never built**.

##### v1-overlap-parameterisation and the vocabulary-blindness audit
- **Family:** structure theorem + whole-corpus census
- **What it does:** Proves the cancellation layer's vocabulary has exactly one
  unknown, and it is not a set of masks — it is the **overlaps**. V1-1: every mask
  of a circuit is a subset of a target or of a cancel-parent. V1-2: a cancelling
  gate is *exactly* a triple `(child z, overlap O, split A)` with parents `A|O` and
  `(z∖A)|O`. Feedstock is not free-floating: it is `z ⊔ O` cut in two.
- **Measured:**
  - **Frontier anatomy** over 8 oracle-VALID circuits: **178 cancelling gates, 80
    distinct overlaps, 80/80 with `cover = 1`** — null probability ≈ **4 × 10⁻³¹**
    against the measured base rates. **176 of 178 cancelling gates are `split`**;
    the intuitive "build a superset, strip it" nested shape occurs **twice**.
  - **Corpus census:** **381,613 JSON files → 324,121 distinct live-trimmed
    circuits, 9,557,026 cancelling gates, in ~200 s.** At live size 88: 242,974
    circuits, 7,158,511 cancelling gates, `cover(O) = 1` in **99.917 %**,
    `cover(O) = 2` in 5,941, **`cover(O) ≥ 3` in ZERO**; only **546 distinct
    overlaps and 2,228 distinct cancel-parents across a quarter of a million
    circuits.** *Every mask of every one of the 242,974 known 88s lies in `V₂`*
    (subsets of 3-target unions); 97.6 % lie in `V₁`.
  - **The audit that voided the program's main line:** the entire known 88
    population uses **2,646 distinct masks; tier-3's 3,961-mask vocabulary `W`
    contains 1,113 of them — 42 %.** At 89 it is 30 %, at 90 it is 23 %. Good news
    attached: **`W ⊂ V₁` entirely (3,961/3,961)** — the corpus-derived vocabulary
    is a *sample* of a set writable from the matrix alone. Sizes:
    `|V₀| = 1,648`, `|V₁| = 532,457`, `|V₂| ≤ 2.13 × 10⁸`.
  - **Span cone bound (V1-6):** `|cone(u) ∪ cone(v)| ≥ wt(z) + wt(O) − 1`, proved
    for **arbitrary** SLPs (strengthened from CF parents, which matters because
    feedstock is often itself produced by a cancelling gate — measured 45 of 356
    parent slots). Consequence: **a cancelling gate costs `wt(O) + 1` extra unless
    the overlap's cone is shared.**
  - **A clean impossibility-of-this-approach (V1-8):** the natural inequality
    system's least upper bound on `cover` is **8 — the ambient one** — so it
    yields exactly the whole space `F₂³²`. Stated precisely why, and explicitly
    scoped as a statement about *this* inequality system.
- **Verdict:** **keeper**, and V1-2(b) — re-parameterising tier-3's cancel mode as
  `(z, O from 1,680 theorem-derived masks, A over splits)` so feedstock is
  *constructed* rather than *inherited* — is the highest-leverage unimplemented
  design in the campaign.

##### v2-vocabulary-free formulation (IN/OUT partition) + pseudo-Boolean
- **Family:** encoding design + PB cutting planes
- **What it does:** Partitions signals into `IN` (theorem-named, 1,648 masks by
  U6's Lemma 1) and everything else as **free 32-bit vectors over all 2³²**. The
  scope of a verdict becomes **two integers `(S, E)`**, both functions of `M`,
  with a *complete* limit `(S = 55, E = 87)`.
- **Twist:** the coordinates are not distances to anything known, so it passes the
  blindness test that tier-3 fails. The complete 87 instance is a
  **176,474-variable / 53,762-constraint model that builds in 9 s**, and the
  `S!`/`E!` symmetry is **completely** broken.
- **Measured:**
  - **The tiny-exact ground-truth control — the best control artifact in the
    campaign:** on small random GF(2) matrices, **14/14 exact optima reproduced
    with no vocabulary** (INFEASIBLE at `L−1`, OPTIMAL at `L`, every time). Three
    of the 14 are load-bearing: their optimum **cannot** be reached
    cancellation-free, so the free machinery is what finds it — simultaneously a
    positive control on the free machinery and a negative control on the named
    layer. It runs on random matrices by construction, so it is **fully
    CIRCUIT-GENERIC**.
  - **The calibration finding that redirected the lane:** `S = 0, E = 0` *is* CF
    synthesis, and U6 says every budget ≤ 91 must be UNSAT. CP-SAT's frontier is
    INFEASIBLE at 33 (0 s) and 36 (2 s), then **UNKNOWN at 40, 45, 50, 55 and 60
    (> 659 s)**. **The engine is ~53 gates short on the easiest slice the
    instrument has.** Diagnosis: the formulation is correct, complete and cheap to
    build — **CP-SAT is simply a poor infeasibility prover for a covering /
    cardinality problem.**
  - **Pseudo-Boolean (Exact 2.2.1), pre-registered before any run, and it held:**
    budget 60 — where CP-SAT burned 659 s and returned nothing — **falls to
    cutting planes in 1 second.** Positive control at MixColumns scale passes
    (pinned at 146: SAT 0 s; at 145: UNSAT 0 s). **The one genuinely new and
    reusable law: Exact's *optimisation* mode (dual bound 88) is far stronger than
    its own *decision* ladder (stuck between 60 and 70) — any future PB work on
    this problem should be run in optimisation mode, never as a budget ladder.**
    Known encoding limit recorded before it bites: order-encoded acyclicity levels
    cost `O(P·L)` per parent and are **not encodable as written** at MixColumns
    scale with events — *"this is the wall the 87 rung will hit, and it needs a
    level-free acyclicity argument, not a bigger machine."*
  - **The CF incumbent:** minimising the `S = E = 0` slice in optimisation mode
    produced an oracle-verified **102-gate, depth-5, zero-cancelling-gate
    circuit** (`v2_no_vocab/data/cf_incumbent.json`), giving **`92 ≤ L_cf(M) ≤ 102`
    with both ends solid.** Every previously reported upper number is superseded:
    104 was an unextracted HiGHS incumbent, 103 a `best:` line from a log cut off
    mid-solve, 133 a referee's circuit.
  - **A cleanly closed route (V2-2):** U6's certificate is literally the LP dual of
    a Dantzig–Wolfe reformulation; replacing "hierarchy" by "derivation" makes the
    LP an *exact* reformulation of `L(M)` and **simultaneously collapses its dual
    to ≤ 32**, with a constructive escape exhibited for all 32 targets. So the
    91.0 comes entirely from Lemma 1 restricting the columns. Branch-and-price
    inherits an LP bound ≤ 32 against a target of 87 and is closed too.
  - **A retracted theorem ladder, recorded in full:** the first `horizon87`
    S-sweep was **wrong** — it swept `S` as a cap, which silently excludes
    circuits with `s < S` needing more events. The referee demonstrated it
    computationally on three small instances where the rung returns INFEASIBLE
    although the circuit provably exists. **Nothing was banked**, and the repaired
    version pins `S` exactly.
- **Generality:** **CIRCUIT-GENERIC** — `IN` is derived from the target set by
  theorem; retargeting is a new `TARGETS`.
- **Verdict:** **keeper — the best-scoped instrument and the best-measured engine
  work in the campaign.**

### 2B — the retrospective catalog in `analysis/` (methods of the *previous* codebase)

`beat88/analysis/` is not a search lane: it is a 26-report forensic audit of the
codebase that produced the five 88s, arbitrated by `SYNTHESIS.md` (465 lines).
The implementations live in `pipeline/` and `campaign_87/` (other slices), so
these entries are compact; the full catalog entries with citations are in
`beat88/analysis/code/*.md` (14 reports) and `beat88/analysis/ideas/*.md` (12).

**SYNTHESIS.md's own reconciled verdict** is worth quoting whole in the public
write-up: *"the old method is one machine wearing five costumes"* — state = value
set (a proved cost-exact quotient, so the representation is not the obstacle);
search = descend from cheap random ~140-gate roots through feasible-at-every-step
states, alternating walk and LNS under a lexicographic (gates, depth) ratchet in
120–600 s chunks; **memory = one circuit and two integers**, with the 10⁵–10⁶
verified plateau states per fleet going to files nothing read back; proof =
verify-before-claim (**zero false claims ever**) plus exact k ≤ 3 certificates.

And its four interlocking reasons the machine produced no 87, all measured:
1. moves are radius ≤ 2 in a metric where every observed improvement needs
   **k ≥ 8, median 42**;
2. the search could never *reside* where transitions live — the walk is provably
   monotone non-increasing (`plateau_slack_p` is arithmetically inert) and the
   LNS's uphill excursions happen at 93–98 gates;
3. at 88 the neutral move class **degenerates into gauge rotations** (2187 = 3⁷,
   729 = 3⁶), so "≈139,878 distinct states" over-counts orbit points ~100×;
4. **every instrument was anchored on the known** — and the one mechanism that
   demonstrably produced novelty (fresh roots reading nothing) got ~6 % of the
   compute.

| method (report) | family | headline measured number | verdict |
|---|---|---|---|
| `plateau-walk-neutral-swap` (`code/engine-walk.md`) | local-search | every 88 came from walk chunks; NEW BEST attribution **walk 736 vs LNS 22**; improvement probability at 88 measured **zero** (0/324,815 free removals) | keeper as descender, dead-end at frontier |
| `exact-single-mask-repair` (`code/repair-code.md`) | local-search | completeness re-verified 0 misses on 362 breaking removals; ~7× plateau mobility; **the `valid[:4]` prescreen deletes 30–37 % of true plateau edges** | keeper; delete the selection rule |
| `bfs-plateau-enumeration` (`code/engine-walk.md`) | local-search/exact | full neighbourhood of an 88 in **0.1 s**; 2,465 expanded / 6,324 discovered in 300 s at **0 % revisit** vs the walk's 22–68 % | keeper, dominates the walk as an instrument |
| `gauge-quotient-canonicalisation` (`ideas/exact-repair.md`) | structural | plateau closes at **2187 = 3⁷** / **729 = 3⁶**; one harvest file 518,253 lines → ≤ 9 gauge components (**~100× overcount**) | keeper — mandatory hygiene |
| `complete-remove1-add2` (`code/repair-code.md`) | local-search | 126 s/state → 3,070 distinct 89s + 79 88s, **63 unreachable by the shipped move** | keeper |
| `lns-destroy-and-greedy-rebuild` (`code/engine-lns.md`) | local-search | **effective radius 0.24 masks**; 84–85 % of accepted moves are literal no-ops; 4 distinct 88-states in 300 s vs the walk's 10,124 | superseded / dead-end at frontier |
| `anneal3` depth-3 partition annealer (`code/engine-anneal3.md`) | class-pricing | **97@3 from scratch**, never below 97 in 16 seeds nor in 21 core-hours; CP-SAT on the exact ILP reaches only 101 with dual bound frozen at 32 | keeper as a root generator |
| `from-scratch root constructors` (`code/fleet-worker.md`) | class-pricing | yield per lane: naive 8.6 CPU-h/88, anneal3 10.2, paar 20.5, bp 39.9; **root shares 8/56 periphery masks with its 88 — same as an unrelated root** | keeper (cheapest wins) |
| `fleet-restart-loop` (`code/fleet-worker.md`) | orchestration | 169 restarts, **14 reached 88 (8.3 %), 14/14 opened a never-seen pocket, zero repeats**, yield curve flat | **keeper — the only demonstrated novelty mechanism** |
| `chunked-reseed-from-best` (`code/orchestrator.md`) | orchestration | chunk reset wins on every axis (23.3 % vs 5.6 % of ≥10-mask changes); coordinator reseed **offers: 17 in the entire archive** | keeper (the reset), superseded (the memory) |
| `plateau-harvester` (`code/harvester.md`) | memory | **provably causally inert**; corpus 15,461,215 raw lines → **836,598 distinct 88-gate states**, vocabulary 1,979 masks; 919 B/state vs 13–16 B as deltas (57–72×) | keeper as recorder, dead-end as designed |
| `map-elites-structural-archive` (`ideas/diversity-metrics-and-roots.md`) | orchestration | 24,473 submissions → 585 accepted, 198/2500 cells, **0 new families**; structurally blind (barren and productive basins share far bins) | dead-end as built |
| `exact-window-decider (b≤2)` (`code/exact-window-code.md`) | exact-window | **~165 M production verdicts, all NO**; 4,200 planted-YES windows, 0 misses; **defect: 414/450 false "irreducible" on target windows** | keeper as machinery, superseded as used |
| `exact-k4 budget-3 decider` (`code/exact-k4-code.md`) | exact-window | 53,126 budget-3 decisions, 0 wins; **removal monotonicity proved** (297 planted, 1,630 sub-windows, 0 violations); **cost nearly flat in k** (1.295 s at k=4 → 2.370 s at k=12) | keeper, most under-used instrument |
| `certifier-inverted-into-move-generator` (`code/exact-window-code.md`) | exact→local | complete radius-2 exchange neighbourhood of an 89 in **56 s single-core, 521 distinct sibling 89s** | keeper |
| `depth-capped component enumeration` (`ideas/pareto-depth-tiebreak.md`) | exact | 88@5's depth-5 component is **exactly 135 states in 18 s** — the same 135 a multi-day fleet found by replaying 37,305 states over 20 h | keeper |
| `windowed-SAT-FSK` (`ideas/windowed-sat.md`) | SAT | 138 verdicts, 0 SAT; **123 of 128 arbitrary slot orderings manufacture UNSAT** | superseded by the order-free lift |
| `slot-order-free window SAT` (`ideas/windowed-sat.md`) | SAT | **first caveat-free UNSAT** in the project; 1 CNF digest across orderings; brackets the practical cut-off at `nB + r ≈ 12` | keeper (became M2's A3) |
| `slotless covering SAT (PB)` (`ideas/exact-certificates.md`) | SAT/PB | depth-3 layer UNSATs in 1–4 s each; the global instance blew to **35 M clauses purely from the cardinality encoding** — size was never the obstacle | keeper (became M2's A2 PB route) |
| `union-subset / vocabulary SAT` (`ideas/exact-certificates.md`) | SAT | union of two known 88s = 109–137 masks; all six = 223; prior `XV190_K87` UNSAT in 13,023 s | keeper (became M2's A2) |
| `spec-oracle` (`code/spec-oracle.md`) | infrastructure | zero false claims campaign-wide; **automorphism group proved exactly ℤ/4**; all 8 shipped circuits audit `live=88 dead=0` | keeper unconditionally |
| `value-set representation` (`ideas/value-set-representation.md`) | structural | proved a **cost-exact quotient**; at the frontier **the derivation DAG is unique** — a gate-list representation buys nothing at 88 | keeper (settles a framing question) |
| `Mᵀ dual frame + double transposition` (`ideas/symmetry-orbits.md`) | structural | round trips give 46–59 distinct 88s from 60 trips, symdiff up to 16; **but Mᵀ descends significantly worse (p = 1.2 × 10⁻⁴)** and M1 later closed the move (3,006 products, 0 escapes) | dead-end as a move |
| `ρ²-orbit search` (`ideas/symmetry-orbits.md`) | structural | **every known 88 has asymmetry defect u ∈ {17,…,40}; the engine's budget was u ≤ 3** — it searched a region provably disjoint from every 88 | dead-end as a constraint |
| `ρ²-defect as a coordinate` (`ideas/symmetry-orbits.md`) | descriptor | harvested band [0.536, 0.786]; **the two from-scratch record 88s sit at 0.286 = −10.63σ** | keeper (became B4) |
| `row-depth-profile descriptor` (`ideas/diversity-metrics-and-roots.md`) | descriptor | within-family Hamming 0–3, cross-family **11–28** — clean gap, correct on every known call | keeper (became B4) |
| `neutral-degeneracy observable` (`ideas/exact-certificates.md`) | descriptor | monotone bands 97→68/80/86 … 88→**12–21, with 25 of 29 exactly 16**; 0.1 s per circuit | keeper (became B4) |
| `union crossing, plain` (`ideas/symmetry-orbits.md`) | recombination | **13 of 15 pairwise crossings beat the symmetrize-first path by ~4.6 gates**; two land at 89/90 from cold | keeper — but M1 later measured the class as gauge-confined and anti-correlated with parent distance |
| `thinker_c 31-target relaxation` (`ideas/value-set-representation.md`) | reformulation | **612,949 distinct sub-88 states**, never censused | closed by M4 |
| `closure kernel / relax / walkstate` (`code/closure-kernel.md`, `relax-depth.md`, `walkstate-incremental.md`) | infrastructure | C closure **3.1 µs = 65–110×**; `relax` decremental 2.62× end-to-end; **numpy and GPU are measured traps** | became shared B1 |
| `reproduce-harness` (`code/reproduce-harness.md`) | infrastructure | **`hunt_88.py` reproduced the record 88@d7 gate-for-gate**, every iteration index, 18 days and one refactor later — *the search is deterministic* | keeper |

---

## 3. ARTIFACTS (counts + labels)

### 3.1 Verified circuits (exported, oracle-checkable)

All export records carry the mask/gate list plus a replay tuple. I spot-verified
two at random today and both printed `VERDICT: VALID` (the 91@4 record, and
`exports/m3_m3f_88g_d5_5189230a.json` at depth 5).

**Command** (per host manifest):
`grep -o '"gates": [0-9]*' <MANIFEST.jsonl> | sort | uniq -c`
and
`grep '"gates": 88' <MANIFEST.jsonl> | grep -o '"depth": [0-9]*' | sort | uniq -c`

| host | manifest path | records | 88 | 89 | 91 | 92 | 97 |
|---|---|---|---|---|---|---|---|
| local | `beat88/methods/m3_census/exports/MANIFEST.jsonl` (396 MB) | 296,514 | 295,005 | 1,201 | 34 | 105 | 169 |
| pod1 | `beat88/pod_salvage/pod1/beat88/methods/m3_census/exports/MANIFEST.jsonl` (715 MB) | 621,701 | 620,485 | 719 | 0 | 0 | 497 |
| pod2 | `beat88/pod_salvage/pod2/beat88/methods/m3_census/exports/MANIFEST.jsonl` (717 MB) | 631,104 | 614,605 | 693 | **15,650** | 0 | 156 |
| **total** | | **1,549,319** | **1,530,095** | **2,613** | **15,684** | **105** | **822** |

**88-gate records by depth** (same commands, summed):

| depth | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| local | 63 | 1,018 | 29,767 | 111,994 | 79,124 | 44,404 | 7,184 | 15,802 | 4,128 | 1,017 | 457 | 47 | 0 |
| pod1 | 57 | 138 | 33,050 | 310,062 | 168,039 | 68,928 | 18,196 | 17,354 | 3,120 | 1,032 | 457 | 45 | 7 |
| pod2 | 47 | 673 | 31,717 | 273,026 | 183,118 | 84,115 | 16,973 | 20,297 | 3,370 | 897 | 352 | 20 | 0 |
| **total** | **167** | **1,829** | **94,534** | **695,082** | **430,281** | **197,447** | **42,353** | **53,453** | **10,618** | **2,946** | **1,266** | **112** | **7** |

⚠ These are **records (gauge-inflated states)**, not distinct gauge orbits. The
authoritative distinct-orbit figure the campaign uses is **33,010** for the whole
known 88 population (`beat88/methods/m2_oracle/runs/pop88_worklist.jsonl`,
33,010 lines), and M3 contributed **2,722 new families / 12,596 novel orbits** on
top of the pre-campaign corpus.

**Circuit files on disk** (`find <exports> -maxdepth 1 -type f | wc -l`):
local 230,889 · pod1 532,724 · pod2 487,517 · **total 1,251,130 files, 1.1 GB
apparent / 6.7 GB on disk.**

**Other verified-circuit stashes:**

| label | count | path | note |
|---|---|---|---|
| record 91 @ depth 4 | 1 canonical + 33 siblings (32 gauge orbits) locally | `beat88/methods/m3_census/exports/RECORD_mixcolumns_91gates_depth4.json`, `exports/DEPTH_RECORD` | re-verified today |
| M1's 89-gate cores from one 90-gate seed | 20 (7 at depth 5) of 36 oracle-VALID states | `beat88/methods/m1_cartography/exports/` (21 files) | `find … -type f \| wc -l` |
| M5's rerouted 99 @ depth 4 | 1 | `beat88/methods/m5_backbone/verify/fiber_best_99gates.json` | 108 → 99 by rerouting alone |
| M2's adopted anchors | 6 high-mobility 88s (depths 10–13) + ladder/natgt/chain/M1 anchor sets | `beat88/methods/m2_oracle/code/{k4b3_anchors,ladder_anchors,natgt_anchors,m1_anchors}/` | all oracle-VALID at registration (free-gate audit mandatory) |
| natural 89-gate descents | **10,089** | `beat88/pod_salvage/pod1/beat88/methods/m2_oracle/runs/natgt_descents_89/` | these are the "ground truth" positives that proved the decider fires |

### 3.2 `FOUND_*` alarm files — and what they are not

`find beat88 -name 'FOUND_*' | wc -l` → **44,249.**
Gate-count distribution over every one of them
(`find … -print0 | xargs -0 -n 500 grep -h -o '"gateCount": [0-9]*' | sort | uniq -c`):

| gateCount | 89 | 90 | 91 | 92 |
|---|---|---|---|---|
| files | 12,704 | 30,856 | 16 | 673 |

**There is no `FOUND_*` file below 89 gates anywhere in the slice.** By
location: 30,856 in `pod1/…/runs/quarantine_GT90k3_netzero` (the aborted k=3
complete shell's net-zero defect — the driver logged every "win" at any size,
including re-adding what it removed), 10,089 in `natgt_descents_89` (real 89s),
2,609 in `quarantine_idcollision` + 6 local (the non-injective-window-id defect),
689 in `ladder_wins_lad94_sym94` (the dead-gate 94's descendants). All four
classes are documented as expected and non-campaign-relevant in
`beat88/methods/m2_oracle/{STATE.md,LEDGER.md}`.

### 3.3 Bound / UNSAT certificates and exhaustion theorems

| label | what it certifies | count / scale | path |
|---|---|---|---|
| **88 wall, core-2** | no 87 within remove-2-add-1 | 36,810 orbits incl. all 33,010 known 88s; `pop88_lab{0,1,2}.jsonl` = 33,010 rows, `grep -c '"cuttable": true'` → **0** | `beat88/methods/m2_oracle/runs/pop88_lab*.jsonl` |
| **88 wall, core-3** | no 87 within remove-3-add-2 | six canonical families + 506 random + 1,137 descent-reached | `runs/k3b2_*.jsonl` |
| **89 wall, core-3** | no 87 within remove-3-add-1 of any known 89 | 64/64 anchors, 1,872,640 windows | `runs/`, `LEDGER.md` §Theorems banked |
| **89 wall, core-4** | no 87 within remove-4-add-2 | 13/64 anchors complete | `runs/k4b3_*.jsonl` |
| **union UNSATs** | no 87 realizable in that mask universe | **427** | `runs/a2_{results,pb_results,pb_escalate,density}.jsonl` |
| **A3 window UNSATs** | order-free, slot ≤ 12 | **399 UNSAT / 0 SAT** (408 jobs) | `runs/a3_results.jsonl` |
| **A4 cone UNSATs** | no gate saving in that cone | **7** (controls passed) | `runs/a4_results.jsonl` |
| **M1 rigidity** | 3,293 move-class products, 0 escapes from the true gauge component; complete C(56,2) shells on 540 cores (~830,000 k≤2 decisions), 0 descents | | `m1_cartography/FINAL.md`, `runs/escape_recheck.log` |
| **M5 Phase-B** | sound "NO 87" for an 88-family's `k−1` completion | **15** sound + 7 inconclusive of 204 | `m5_backbone/verify/phaseB_verdicts.jsonl` |
| **M4 thinker_c closure** | the whole 31-target population admits no completion at \|S\| ≤ 86 | 629,274 states, 282,970 at \|S\|=86, 6,487 positive controls | `m4_inverse/out/thinker_c_rebase.json` |
| **M4 one-edit exhaustion** | no 87 within one operand edit of any one-gate truncation of the five 88s and the 89 | 529 base genomes, **6,832,408 genomes** | `m4_inverse/analysis/landscape.md` |
| **lower bounds** (understanding lanes) | `54 ≤ L(MixColumns)`; `L_cf(MixColumns) ≥ 92` | 2 refereed-grade theorems, 1 s verifier | `understanding/u3_lowerbound/RESULT.md` + `verify_bound.py`; `understanding/u6_spec87/RESULT_CF.md`, `cert_u63_7_2.json` |

### 3.4 Labelled-orbit ledgers (append-only)

`wc -l` and `grep -c '"cuttable": true'` per file, in
`beat88/methods/m2_oracle/runs/`:

| file | rows | cuttable | stratum |
|---|---|---|---|
| `pop88_lab0/1/2.jsonl` | 11,004 / 11,003 / 11,003 | **0 / 0 / 0** | the complete 88 population |
| `s89_lab0/1.jsonl` | 16,539 / 16,544 | 534 / 522 | the 89 stratum (a cut here yields an 88 — expected) |
| `l89b_lab0/1.jsonl` | 6,293 / 6,290 | 2 / 2 | `layer89` extension |
| `census_pod0/1/2.jsonl` | 1,994 / 1,993 / 2,249 | 3 / 7 / 7 | pod census shards |
| `census_inbox.jsonl` | 5,369 | **1** (a 90-gate circuit, i.e. a 90→89 cut) | M3's novel orbits, labelled live |
| `census.jsonl` | 8 | 0 | seed rows |
| worklists | `pop88_worklist` 33,010 · `stratum89_worklist` 31,950 · `layer89b_worklist` 18,865 · `census_worklist` 5,980 · `k3b2_worklist` 506 · `k3b2_chain_worklist` 300 | | |

Plus `code/census_inbox/processed/` — **11,219 drained circuit files**
(`find … -type f | wc -l`), 0 pending, 0 unreadable.

### 3.5 Descriptor archives and compressed harvest

| class | files | size | command |
|---|---|---|---|
| `*.cells.jsonl` descriptor archives | **127** | **31.4 GB** | `find . -name '*.cells.jsonl' -printf '%s\n' \| awk '{s+=$1;n++}END{print n,s}'` |
| `MANIFEST.jsonl` (3 big + 4 small) | 7 | 1.8 GB | `find . -name 'MANIFEST.jsonl' …` |
| compressed harvest segments `*.pop.*.jsonl.zst` | **1,083** | **337 MB** | `find . -name '*.pop.*.jsonl.zst' \| wc -l` |
| run logs `.log` + `.nohup` | 606 | 3.4 GB (**1.73 GB duplicated**) | see §4 |
| other `.jsonl` (ledgers, labels, worklists, windows) | 566 | 3.48 GB | `find . -name '*.jsonl' ! -name '*.cells.jsonl' ! -name 'MANIFEST.jsonl' …` |

The `.zst` segments are the **complete** population harvest at ~150:1 (the
`KEEP_CAP_MB` of 40,000 was never approached, so nothing was pruned) — 337 MB
standing in for roughly 50 GB of raw plateau population.

### 3.6 Writeups

`find beat88 -name '*.md' | wc -l` → **120.** The load-bearing ones:
`ALLOCATION.md`; per-lane `THESIS/LEDGER/STATE/FINAL` ×5 (`m1_cartography/FINAL.md`,
`m3_census/FINAL.md`, `m4_inverse/STATE.md`, `m5_backbone/verify/{VERIFICATION,PHASE2,STATE,EVIDENCE_CROSSCHECK,U1_DEFECTS_RESPONSE}.md`,
`m2_oracle/{LEDGER,STATE}.md` — 1,714 lines of ledger alone);
`methods/DESIGN_NOTES.md`; `methods/shared/README.md` + 6 `shared/analysis/b*.md`;
`m3_census/analysis/00–05*.md`; `m2_oracle/analysis/{cuttable-breakdown,decider-validation,natural-descent-density}.md`;
`analysis/SYNTHESIS.md` + 26 reports; `understanding/{PROGRAM_STATE,CANON,MANIFESTO}.md`
+ per-lane `NOTEBOOK/PROOFCHECK/RESULT`.

---

## 4. KEEP / DELETE proposal

Reclaim if every DELETE-CANDIDATE below is taken: **≈ 33 GB of 47 GB**, leaving
**≈ 14 GB**; with the optional archival repacking of §4.3 as well, **≈ 6 GB**.
Nothing in `pod_salvage` that is *unique* is proposed for deletion.

⚠ **Read §6.0 first: the entire `beat88/` tree is untracked in git.** Every
deletion here is permanent and has no second copy.

### 4.1 Unambiguous DELETE-CANDIDATES

| item | size | why |
|---|---|---|
| **113 byte-identical `.nohup` copies of `.log` files** | **1.73 GB** | Verified identical pair-by-pair with `cmp -s` (113 identical / 8 differing / 4 with no `.log` partner). The 8 differing and 4 orphans stay. Command used: a `while read` loop over `find . -name '*.nohup'` with `cmp -s "$n" "$b.log"`. |
| `**/__pycache__/` (173 `.pyc`) | ~2 MB | build artifacts |
| `runs/*/**.stale` (26 files) | small | superseded run markers |

### 4.2 DELETE-CANDIDATE with a judgement call: the descriptor archives

| item | size | assessment |
|---|---|---|
| `**/archive/*.cells.jsonl` (127 files) — local 5.1 GB, pod1 11 GB, pod2 16 GB | **31.4 GB (67 % of the slice)** | **This is the single decision that determines the slice's footprint.** These are *not* circuits: each row is one descriptor cell — `{cell, n, depth, rowdepth, crit, u, off_census, deg_max, deg_mean, canon, gauge_dup, provenance{seed, walk_seed, max_iters, kernel, backend}}` — the fleet's novelty/dedup memory. **No mask list, no gate list.** Every circuit worth keeping was already written out to `exports/` and indexed in `MANIFEST.jsonl`. The rows carry bit-exact replay tuples and the campaign demonstrated bit-exact replay works, so they are regenerable *in principle* — but only at 747 core-hours, and only on the same kernel/backend. What they uniquely support is the *coverage* claim ("we visited N cells, of which M were new"), which `ledger.py`'s scoreboard already summarises. |
| | | **My recommendation: compress rather than delete.** They are highly repetitive JSONL; zstd on this shape reliably gives 10–20×, so `zstd -12` in place would take 31.4 GB → **~2 GB**, reclaiming ~29 GB while losing nothing. If the user wants a straight deletion instead, delete the two pod archives (27 GB) and keep the local 5.1 GB as a sample — but compression strictly dominates. ⚠ `zstd` is **not installed** on this box and there is no `zstandard` Python module (I could not decompress the existing `.zst` segments to inspect them); installing it is a prerequisite. |

### 4.3 Optional repacking (keeps every byte of content)

| item | now | after | note |
|---|---|---|---|
| the three `exports/` circuit trees — 1,251,130 files | **6.7 GB on disk / 1.1 GB apparent** | ~150 MB as three `.tar.zst` | 5.6 GB of the 6.7 is 4 KB-block overhead on ~900-byte files (`du -sb` vs `du -sh`: local 576 MB apparent / 1.3 G disk; pod1 1,174 MB / 2.8 G; pod2 1,137 MB / 2.6 G). Also removes 1.25 M inodes. **Keep `MANIFEST.jsonl` uncompressed and outside the tarball** — it is the index and is grepped constantly. |
| the three `MANIFEST.jsonl` files | 1.8 GB | ~200 MB compressed | but they are the working index; I'd leave them raw. |
| `analysis/scratch/` bulk dumps (`.pop.jsonl`, `.pkl`, `.log`, `.out`) | ~76 MB of the 77 MB | 0 | deterministic re-runnable output of the ~1.45 MB of scripts stored beside them. **Exception — keep these four files**, they are unique verified artifacts: `scratch/reproduce-harness/found_88at7_walkonly_seed1011.json` (a *third* distinct 88 @ depth 7, oracle-VALID, in no `evidence/` file), `scratch/value-set-representation/rt_new_mixcolumns_88gates_depth5.json`, `scratch/engine-anneal3/fast97.json`, and `scratch/negative-results/b_nbr_*.json`. Also keep the C prototypes (`closure-kernel/closure_c2.c`) and the SAT encoder (`windowed-sat/gsat.py`, `lift_validate.py`). |

### 4.4 KEEP unconditionally

| item | size | why |
|---|---|---|
| every `.md` (120 files) | ~2 MB | the ledgers, theses, kill tests, retractions and final reports — this is the campaign's memory and the raw material for the method catalog |
| all `exports/*.json` circuits + the three `MANIFEST.jsonl` | 6.7 GB (1.1 GB apparent) | 1.53 M oracle-checkable circuit records; irreplaceable at 747 core-hours |
| all `*.pop.*.jsonl.zst` harvest segments (1,083) | 337 MB | **the complete compressed population harvest**, ~150:1; the densest value-per-byte in the slice |
| every label/worklist/result `.jsonl` in `m2_oracle/runs/` and `pod_salvage/*/…/m2_oracle/runs/` | ~2.5 GB | the theorem evidence — every "88 wall" claim is a line count in these files |
| `shared/index/pop88/` | 460 MB | the built 850,784-state population index; ~1 day to rebuild and it needs the raw harvest |
| `m5_backbone/verify/*` incl. `phaseB_remaining.json` | 744 KB | the resume order for the 182 undecided families — the campaign's best remaining leads |
| all 44,249 `FOUND_*` files | ~500 MB | *(uncertain — see note)* they are all 89–92 gates and documented as expected, so they could be deleted; but they are 12,704 verified 89-gate circuits plus two quarantined defect corpora that document real bugs. **KEEP + note:** if space is needed, the 30,856 `quarantine_GT90k3_netzero` files are the safest to drop (they are the net-zero artifact of a known driver defect and their 90-gate content is not scarce). |
| `analysis/{SYNTHESIS.md,BRIEF.md,code/,ideas/}` | 770 KB | the 26-report retrospective — the most reusable prose in the repo |
| `understanding/` — every `NOTEBOOK.md`, `PROOFCHECK.md`, `CANON.md`, `PROGRAM_STATE.md`, all code, all certificates | ~13 MB | the two publishable theorems and their solver-free verifiers live here; see §4.5 |

### 4.5 `understanding/` (319 MB) — a clean 306 MB reclaim, with one precondition

The lane declares its own scratch. `understanding/u2_walls/data/.gitignore` names
exactly four files as *"derived intermediates, rebuildable from m2_oracle/runs by
../code/build_dataset.py"* (~30 s to rebuild).

| item | size | disposition |
|---|---|---|
| `u2_walls/data/census.jsonl` (89,744 rows) | 178.4 MB | **DELETE-CANDIDATE** — self-declared regenerable ⚠ *only if* `methods/m2_oracle/runs/` survives; if those runs are deleted this becomes the sole copy of an 89,744-orbit labelled census |
| `u2_walls/data/u4_gates.jsonl` (307,694 rows) | 108.3 MB | **DELETE-CANDIDATE** — self-declared regenerable by `u2_walls/code/u4_gates.py` |
| `u2_walls/data/{cuts,cuts_typed}.jsonl` | 2.5 MB | DELETE-CANDIDATE — same `.gitignore` |
| `u4_economy/{sw_rows,prof}.jsonl` | 16.5 MB | **DELETE-CANDIDATE** — regenerable by the exact commands in `u4_economy/NOTEBOOK.md` §8 |
| `u4_economy/corpus{,_ext,_bp}.txt` | 4.0 MB | **KEEP** — these are the *definition* of the 26,222-circuit corpus every U4 number is computed over; without them no U4 result is reproducible even though the machinery is |
| `u1_obligations/identity_rows.jsonl` + the retracted lanes' logs | ~0.5 MB | DELETE-CANDIDATE — data of an explicitly RETRACTED instrument (keep the `.py`) |
| `u5_heavycorner/heavy_corner_library.json` | 1.3 MB | **KEEP** — the lane's deliverable, self-contained, a function of `M_AES` alone |
| `u6_spec87/cert*.json` (11 certificates incl. the eight `cert_u63_*`) | ~800 KB | **KEEP** — the refereed exact-integer bound certificates; ~2 s to verify, solver-free |
| `v2_no_vocab/data/cf_incumbent.json` | 4 KB | **KEEP** — the oracle-verified 102-gate cancellation-free circuit; the upper end of `92 ≤ L_cf ≤ 102` |
| all `.txt` summaries in `u2_walls/data/` | < 1 MB | **KEEP** — these *are* the results |
| everything else (u1, u3, u5, u6, u7, v1, v2 in full) | ~6.7 MB | **KEEP** — code, notebooks, proofchecks, certificates, small logs |

Net: **≈ 306 MB DELETE-CANDIDATE, ≈ 13 MB KEEP.**

---

## 5. LEADS (sharp-eye findings)

### L1 — 182 of 204 families were never decided, and the 8 best leads are among them (VERIFIED-IN-LOG)

M5's Phase-B queue was **ordered by `Δ = n_components − k` ascending** so the
most-compound obligation frames would run first — but `imap_unordered` writes
results as they *finish*, so **the 22 rows that exist are the fast ones**. Seven
of the eight compound-obligation frames are undecided, **including both `Δ = −2`
frames**, which are the most compound in the corpus and appear in no earlier
sample:

| family | k | comps | Δ | status |
|---|---|---|---|---|
| `m3k\|d11` (n=6) | 7 | 5 | **−2** | UNDECIDED |
| `m3l\|d10` (n=15) | 7 | 5 | **−2** | UNDECIDED |
| `f91b_7\|d8` (n=13003) | 8 | 7 | −1 | UNDECIDED (search was *still running* when stopped) |
| `rho_2\|d14` (n=113) | 8 | 7 | −1 | UNDECIDED |
| `rho_2\|d7` (n=827) | 8 | 7 | −1 | UNDECIDED |
| `m3b\|d14` (n=2) | 8 | 7 | −1 | UNDECIDED |
| `m3a\|d6` (n=17) | 9 | 8 | −1 | UNDECIDED |
| `mix_6\|d12` (n=363) | 5 | 4 | −1 | decided NO 87, 1,682,696 nodes |

`Δ < 0` means the family spends more gates than it has independent obligations,
so a merged repair is **not excluded by counting** — these are the only frames in
the corpus where the campaign's own structural argument does not rule out an 87.
The resume path is exact and cheap: `phaseB_remaining.json` holds all 182 in
order; `verify/shot87.py` runs one family at a time on a single local box. The
lane's own STATE.md says "**a successor should start here**". Sources:
`beat88/methods/m5_backbone/verify/{STATE.md §4, PHASE2.md §7, phaseB_run.log, phaseB_remaining.json}`.
Caveat the lane binds to it (U1 Cor. 7.2): a `k−1` completion is **sufficient**
for an 87; its absence is **not necessary** for `C_AES ≥ 88`.

### L2 — the `|W| = 2` instrument was never built (VERIFIED-IN-LOG)

`m5_backbone/verify/STATE.md` §6.3: *"The `|W| = 2` instrument was never built —
remove-3-add-2 discharging a compound obligation two-for-one. U1 and U2 both name
it as the open door, and Theorem 4 says it is exactly where a compound
obligation's marginal cost could drop. That is the next thing to build, and the
`Δ<0` frames above are its natural inputs."* This is a named, motivated, unbuilt
instrument pointed at the campaign's best-identified structural gap.

### L3 — `f91b_7|d8`'s budget-7 search was running when it was killed (VERIFIED-IN-LOG)

STATE.md §3: *"The local budget-7 search was still running when it was stopped and
produced no verdict. Its planted positive control passed (`k=8` discharges all 7
obligations); the `k−1 = 7` question is **open**."* This is a timeout, not a
refutation: a bracket with a passed control on the largest family in the corpus
(13,003 siblings). It is not counted in the 22.

### L4 — the complete `C(57,5)` shell of the record 89 stopped at 19 % (VERIFIED-IN-LOG)

`m2_oracle/STATE.md`: 789,584 of 4,187,106 windows. A zero-win *completion* would
prove, via removal monotonicity, that **no sub-88 circuit adds ≤ 3 new masks
relative to the shipped 89@5** — i.e. it would close core-5 for the record
circuit, the single question M2 names as "the last open question for the record
circuit". At the measured rate this is ~1.7 pod-days under PyPy, or ~2 h with the
C kernel. Resume command is written out verbatim in STATE.md.

### L5 — pod2 holds 15,650 depth-4 91-gate records that no writeup accounts for (VERIFIED-IN-LOG, interpretation PLAUSIBLE)

`grep '"gates": 91' pod2/…/MANIFEST.jsonl | grep -o '"depth": [0-9]*' | sort | uniq -c`
→ **15,650, all at depth 4.** `m3_census/FINAL.md` §3.1 reports the record as
"**34** distinct verified 91@4 circuits, 32 distinct gauge orbits" — that is the
*local* count. Nothing in the slice analyses pod2's 15,650. They are almost
certainly gauge-inflated states of a small number of orbits, but nobody ran
`gauge.canon` over them, and the 91@4 stratum is exactly where the campaign
measured the depth axis to be soft. **Cheap and unambiguous next step:** canon
those 15,650 and count distinct orbits; if it is more than 32, the depth-4
frontier is wider than the record file suggests, and a depth-4 census is a new,
publishable object. (Also: `beat88/methods/m3_census/exports/FRONTIER.json` is
the campaign's gates-vs-depth Pareto frontier — `{3:97, 4:91, 5:88, 6:88, …}` —
and nothing has ever attacked 96@3.)

### L6 — the routing constructor reached 99 by rerouting alone and was never pushed further (VERIFIED-IN-LOG)

`m5_backbone/verify/STATE.md` §6.5: *"The routing constructor is unfinished and
promising: 108 → 99 by rerouting alone with `A` frozen
(`fiber_best_99gates.json`, oracle-VALID depth 4). **The recursive descent past 99
was never run.**"* PHASE2.md §5.5 calls the routing axis "real and unexploited":
same masks, ≥5 gates apart. This is an axis orthogonal to every other method in
the campaign, and it has a one-line unfinished next step.

### L7 — `n_components ≥ k` is the campaign's most lower-bound-shaped fact and was never turned into a bound (VERIFIED-IN-LOG)

Holds in **60 of 62** profiled families (and the full 204-family Phase-A profile
shows `comps − k ≥ 0` in 196 of 204). PHASE2.md §1b: *"That is the structural
reason 87 is hard here — the obligations are already nearly in bijection with the
gates."* And §1c found **four distinct gauge orbits** where `k−1` provably cannot
finish the core — *"the most lower-bound-shaped result in this phase"*. The
caveat is explicit and the follow-up is named: those 5 exclusions used a
relaxation that does **not** cover the gate-pair (E3) channel, so they are "not
yet sound"; §2 built the sound version (`close_core.py`) and it was run to
completion **only for the derived 88@5's frame**. *"Re-running the 5 exclusions
through `close_core.py` is the immediate follow-up"* — and it never happened
(`close_core.py` was killed as "superseded by the physical searcher", which then
only decided 22 families). **This is the clearest unfinished path toward a real
obstruction argument in the slice.**

### L8 — the "22 + 5 backbone" picture is falsified, which matters for anyone reading the incumbent frame (VERIFIED-IN-LOG)

PHASE2.md §1a: only **17 of 62** families have all repair slots ternary; slot
sizes run to 11; cores run 78–83 so the "22-mask backbone" ranges 18–26; and in
7 families `k ≠ n_slots`, including the archived 88@7 (`core=81, n_slots=6, k=7`
— two masks in the same gauge slot, the exact failure mode `b5-gauge.md` warns
about, in the wild). *"So the 22+5 decomposition is not lower-bound material. Any
argument of the shape 'every 88 has this backbone, and this backbone needs 5
repairs' is dead at the first clause."* If a public page describes the structure
of 88s, it must not use the 22+5 story.

### L9 — 31.4 GB of descriptor telemetry was generated and never analysed beyond a scoreboard (SMELL, but cheap to test)

The `*.cells.jsonl` archives record, for every one of ~15 M visited states, its
row-depth profile, critical rows, ρ²-defect, neutral out-degree (`deg_max`,
`deg_mean`), gauge canon, and off-census fraction. The only consumer was
`ledger.py`'s growth scoreboard and the waypoint calibration. Two specific
questions the data can answer *without new compute*:
(a) M2's cuttability signature is `deg_max`, and M2 recorded that **118 orbits in
the corpus sit at `deg_max = 13`, above both canonical families** — the archives
carry `deg_max` for every visited state, so the highest-mobility states ever
visited can be extracted by one grep and fed to the labeller;
(b) `analysis/ideas/exact-certificates.md` records that **25 of 29 certified 88s
have neutral out-degree exactly 16, with outliers at 12, 14, 20, 21, and the four
outliers were never identified** — the archives contain the out-degree of every
88 the fleet ever touched. **Do this before compressing or deleting the archives.**

### L10 — M3's own top open thread was never picked up (VERIFIED-IN-LOG)

`m3_census/STATE.md` "Open threads, in the order I would pick them up", item 1:
finish the **92-gate waypoint calibration**. The design assumed the row-depth
descriptor would triage at the ~100-gate waypoint; measurement showed it has *no*
resolution there (84 independent descents, pairwise Hamming 18–32 of 32, 0 % kill
at any radius) and the triage is worth 1.31× rather than an order of magnitude.
The 92-gate calibration data exists (`analysis/waypoint_census_92.{jsonl,txt}`)
and the conclusion — *"the row-depth profile only becomes a basin coordinate at
the frontier itself"* — was never drawn or refuted. This is a small, finished
piece of analysis waiting to be written.

### L11 — a third distinct 88 @ depth 7 sits in a scratch directory (VERIFIED-IN-LOG)

`beat88/analysis/scratch/reproduce-harness/found_88at7_walkonly_seed1011.json`:
oracle-VALID `gates=88 depth=7`, 80/88 masks shared with the record (J = 0.833),
matching no file in `evidence/circuits/`, produced by a **one-word change**
(`ENGINE="walk"`) in 18.5 min against the shipped path's 34.4 min. Provenance
clean. It has never been registered, canon'd, or fed to the labeller.

### L12 — 2,274 firings of the k=5 escape operator, 0 hits — and the sampling was the thinnest possible (VERIFIED-IN-LOG)

`m3_census/FINAL.md` §4 "Did not prove" #4 is explicit: the null is *"consistent
with M1's own measured yield (9 attributable hits from a map that reached 24,719
90-cores), not a refutation of it. It was fired at retirement points only, which
is the cheapest possible sampling and also the thinnest."* M1 established that
`remove1_add2` + trim **is** a complete k=5 descent operator that reached 89s no
k ≤ 2 shell contains — 9 of 36 hits carry its signature. The operator has never
been run as a fleet-wide move at volume, which is exactly how M1 said to use it.

### L13 — pod1's copy of the local shipped harvest may not have been salvaged (SMELL / possible data gap)

`ship_harvest.sh` sends each host's sealed segments to
`/root/slp87/…/runs/${FLEET}_shipped` on **pod1** and deletes the local copy after
a remote hash check; the local `${FLEET}_shipped` dir is a capped local KEEP copy.
`pod_salvage/pod1/…/runs/` contains only `pod1` and `pod1_shipped` — **no
`local_shipped`**. Locally `methods/m3_census/runs/local_shipped` holds 229
segments (66 MB) against pod1's 427 and pod2's 427. Either local shipped less, or
local's pod-side segments were not pulled before termination. I could not verify
which, because `zstd` is absent and `ship_local.log` (560 K) records shipments
but I did not reconcile it segment-by-segment. **Worth 10 minutes of someone's
time before anyone deletes anything.**

### L14 — the census inbox drained, and 4,732 orbits were never labelled (VERIFIED-IN-LOG, mild contradiction)

`m3_census/FINAL.md` says *"4,732 of my orbits are still unlabelled at close. The
labelling loop stays alive; a cut in that queue is still an 87."* But
`code/census_inbox/` now has **0 pending, 11,219 in `processed/`, 0 unreadable**,
and `census_watch.log`'s last lines read `batch: 2 labeled (102 pending)` →
`labeled 2 new; positives 1076 -> 1076`. So the loop drained the queue after
FINAL.md was written and then stopped with the box. The 4,732 either got labelled
(and the "12,596 novel orbits" figure was never reconciled against the 5,369 rows
in `census_inbox.jsonl`) or were never enqueued. **Reconcile
`census_inbox.jsonl` (5,369 rows, dedup by `canon_id`) against M3's 12,596 before
quoting either number publicly.**

### L15 — no lower bound above the trivial 32 came out of any *search-side* method; both real bounds came from the understanding lanes (VERIFIED-IN-LOG)

`analysis/ideas/exact-certificates.md`: the depth-3 4-output CP-SAT relaxation
gives `OPT ≥ 37` after 100 s and does not close; the 12-output relaxation gives a
dual bound of 0. Meanwhile `understanding/u3_lowerbound/RESULT.md` and
`u6_spec87/RESULT_CF.md` carry **`54 ≤ L(MC)`** and **`L_cf(MC) ≥ 92`** with
1-second verifiers. For the public repo: the honest bracket to state is the
refereed one, and the search-side methods should be described as producing
*locality* theorems (the 88/89 walls), not bounds.

### The understanding lanes' leads (U-series)

These come from `beat88/understanding/`. They are separated because they are
theory leads rather than search leads, and several are cheaper than anything in
the L-series.

**U-1 — the two Δ = −2 compound frames, seen from the theory side (VERIFIED-IN-LOG).**
U1's own census found **8 of 204 families violate `n_components ≥ k`** (M5 had
found 2 of 62): `f91b_7|d8`, `mix_6|d12`, `rho_2|d14`, `rho_2|d7`, `m3a|d6`,
`m3b|d14`, `m3k|d11`, `m3l|d10`. These spend more gates than they have
obligations — the *only* frames where the campaign's own structural argument does
not exclude an 87. This is the same set as L1, arrived at independently, which
strengthens it.

**U-2 — `f91b_7|d8`'s double-hit dead mask: an anomaly mentioned once and dropped
(VERIFIED-IN-LOG; the sharpest single anomaly in the slice).**
`understanding/u1_obligations/NOTEBOOK.md` §5, check 3: for `f91b_7|d8` the two E3
gates satisfy `00010203 ⊕ 83800001 = 83810202`, which **is** the singleton dead
mask of comp6 — *"and, remarkably, a second pair of that family's repair gates
hits the same dead mask: `00810283 ⊕ 83000081 = 83810202`."* **Two independent
gate pairs in one family XOR to the same obligation.** Nothing anywhere in the
tree explains, generalises or exploits this. It is exactly the shape of a
redundancy an 87 could exploit, and it sits in the one frame the campaign named as
its best remaining lead.

**U-3 — the "87 must be preceded by a gate that serves nothing" theory, with a
mechanism and a price, and no instrument pointed at it (VERIFIED-IN-LOG).**
U1-15 prices the only known escape exactly: `γ(U) = 3` for the 87-mask state
`U = exterior61 ∪ n16`, with the cheapest schedule `enabler → trigger → bridge`
and **the middle gate not constructible from `A`**. U7 §8.7(f) supplies the
mechanism and the price: a full-class (Λ) mask is cheap to build but **every
consumer of it toward a target must cancel**, because no target has heavy pattern
`H`. So "buy a gate that appears useless" is now a theorem-shaped requirement with
a price tag. **And every search instrument in the campaign — tier-3, novocab, all
the deciders — buys only from `cons(A)` and therefore cannot reproduce the one
completion the canon has priced.** This is the most coherent positive theory of
where an 87 lives that the campaign produced, and nothing was ever aimed at it.

**U-4 — WHY 88: the frontier-tightening triple (VERIFIED-IN-LOG; the best "why 88"
evidence in the slice).**
Three independent statistics of the cancellation overlap all get *tighter* as
circuits get *better*, measured over **9.5 M cancelling gates**, with the
**largest** stratum giving the **tightest** bound (so not a sample-size artifact
in the flattering direction):
`cover(O) ≤ 2` at 88 vs ≤ 3 at 89/90; `max wt(O) = 7` at 88 vs 9 at 89/90 (**and 7
is exactly the heaviest target weight**); `max wt(σ) = 14` at 88 against a proved
ambient 32. V1's own reading: *"If it is a law rather than sampling, an 87 would
have `cover(O) = 1` throughout and `V₁` would be complete exactly where it
matters. This is the cheapest lead in the lane."* **Nobody tested it — and the
obvious test is the lineage control u2 already built** (u2 showed exactly this kind
of corpus-wide statistic loses half its signal to basin confounding).
CANON's honesty caveat travels with it: cite as *"the proved ambient bound is 2.3×
the largest span anyone has observed"*, never as *"a factor of 2.3 remains"*.

**U-5 — WHY 88: efficiency inverts four independent ways (VERIFIED-IN-LOG).**
Every plausible "good circuit" signal points at the 97, not at an 87.
(a) The greedy-108 sits *exactly* on the `L = 152` floor with debt 0 at every cut
and is the **worst** circuit measured; `W = L − 152` runs 0 → 18 → 52 → 60 → 92
down to 88. (b) At fixed depth 8, AUC(89 > 88) is 0.78 for service and **0.87 for
`V`**, and the correlation of service with gate count is **+0.26 — the wrong
sign**. (c) 97 → 88 sheds ~19 light gates and *buys* ~10 heavy ones; the `c = 8`
region the heavy cost law prices lowest is **where the 97 lives**. (d) `|Dcf|`
inverts at the frontier exactly like `V`, and the five canonical 88s' CF layers
are already exactly optimal. Plus two from u2: drop-0 "useless" gates are **5×
more common in 88s than 97s and placed later**, and Λ-containing 89s look *better*
on `deg_max` and cut **138× less**.
**The best circuits carry the most waste. Any constructor that optimises a legible
efficiency metric is walking uphill.** This is the single most important sentence
for a public write-up, and it is measured six ways.

**U-6 — WHY 88: the plateau is a `c`-fibre, and `c` is exhausted and never searched
(VERIFIED-IN-LOG).**
There are exactly 11 non-zero non-singleton heavy classes, so `c ∈ [8, 11]` and
**nothing else exists**. Known 88s occupy {9, 10, 11} (11/89/104 of 204); `c = 8`
is the 97; and `c` slides `|Z|` against `|cf|` **at constant sum 88**
(`c = 9 → 23 + 65`, `c = 11 → 33 + 55`). So an 87 must move *within* a `c`-fibre —
precisely what U5's `plans8` (4,510) and `plans9` (336,484) enumerations
parameterise. **Nobody ever searched inside a fibre.** That is a concrete, finite,
fully-enumerated search space that was mapped and then abandoned at shutdown
(`understanding/u5_heavycorner/heavy_corner_library.json`, 1.3 MB).

**U-7 — the cheapest remaining +1 on the lower bound (VERIFIED-IN-LOG).**
U7's `cfE` ceiling instrument settled `minE_{K′} = 4` exactly (so that rung is
exhausted at 54) but left the other keep-set bracketed at `minE_K ∈ [4, 6]`. U3
§7: depth 4 → `minE ≥ 5` → **`L(M) ≥ 55`**, ~10⁹–10¹⁰ nodes, "plausible in C,
~hours on 2 cores". U7's own FINAL STATUS labels this *"gift to U3, unused"*.
Related and even cheaper: **only 3 keep-sets per size were ever swept and only 2
taken to depth 3**; enumerating all `|K| = 14` sets with `q = 32` needs no new
solver. And the `cfE` ceiling curve keeps rising to **81 at `|K| = 24`** — so
Theorem B is not information-starved, contradicting U3's own "realistic ceiling
mid-to-high 50s".

**U-8 — banked, resumable timeouts across the theory lanes (VERIFIED-IN-LOG).**
(a) **U5's `E ≥ 8`:** budget 6 refuted in 1 node; the budget-7 run was **stopped
after ~10 CPU-minutes without terminating** (memoisation memory) — *"rerun with a
node cap or a support-size prune"*. If `E ≥ 8` held, the heavy floor becomes 28.
And even then it decides only the `z = 1` sub-branch; `z ≥ 2` is untouched.
(b) **11 undecided tier-2 dropscan elements on the 88@6** — re-running them at
4 CP-SAT workers (~44 s each) closes tier-2 on a second family. ⚠ **Systematic
caveat:** every timed-out result in u7 and v2 was run at **1–2 workers**, where
contention manufactures UNKNOWNs; the standing warning is to never trust an
UNKNOWN from those runs in either direction.
(c) **`cfsynth cfm` was never finished** — `CF(M) ∈ [79, 103]` and closing, now
interacting with V2's oracle-verified 102, so `CF(M)`'s exact value in [79, 102]
is genuinely open with the machinery on disk.

**U-9 — the LP already knows more than the certificate (VERIFIED-IN-LOG, SMELL).**
`understanding/u6_spec87/cfree.log`: the exact CF MILP (HiGHS, 14,456 binaries)
reached **dual bound 92.63 at 790 s / 2,038 nodes and was still running when
stopped**. The refereed certificate gives 92. **So the LP relaxation has already
seen ≥ 93 and nobody extracted it.** With V2's verified 102 upper end, the real
live bracket is `[93 on HiGHS trust, 102 verified]`, gap 9 —
`PROGRAM_STATE.md` names closing the CF MILP as **the only live lower-bound
route**. Related and cautionary: U3 declared the cancellation-free route dead at
`CF ≥ 47 < 51`; **U6 revived the same object with target-dependent prices and
column constraints and got 92.** *The difference between 47 and 92 was the choice
of relaxation, not the object* — which is a live warning to re-ask every route
this campaign declared dead by evaluating one weak relaxation.

**U-10 — a free 4× on every solve, never taken (VERIFIED-IN-LOG).**
The `ℤ/4` byte-lane gauge is verified **completely unbroken** in V2's model:
rotation maps `TARGETS` onto `TARGETS` and permutes the 1,648-mask `IN` universe
onto itself for all three `k`, so **every solution comes in orbits of up to 4**.
Breaking it is a lex-leader constraint on the `IN`-indicator vector. *"Not done
here."*

**U-11 — the one region the theory says matters was ruled out of scope in a single
line (VERIFIED-IN-LOG; the deepest structural gap in the campaign).**
CANON's **U1-17 is labelled "Load-bearing"**: the equivalence "87 ⟺ some 88-mask
set's core admits a `k−1` completion" runs through **reducible** 88-mask sets,
and every corpus in this repo holds only **irreducible** ones. Therefore *"no
irreducible 88 family admits a `k−1` completion" would NOT prove `C_AES ≥ 88`.*
U7 §4 records that the reducible-88 layer was **killed before staffing as
circular**. **So: if an 87 exists, U1-16 says it certifies as a `k−1` completion
of a *reducible* 88 — which nothing in the campaign ever searched.** Every
negative in both halves of the slice is scoped away from exactly that region.

**U-12 — U2's own #1 next step, never run (VERIFIED-IN-LOG).**
*"Among adjacent served pairs, 91 of 221 still collide — what distinguishes those?
This is the only obstruction standing between the 4,600 high-mobility rigid 89s
and an 88, and 53 % of them are stopped by it alone."* Small, well-posed, cheap;
the lane closed without running it. Adjacent to it: **`vac(w) ≥ 3` ⟺
remove-3-add-1 ⟺ an 87 from an 89** — sized at ~77 core-hours by the shell route
or "a small job" by the `vac` route, and never run on the 46,318-orbit 89 census
(only on the 64 known anchors). ⚠ The equivalence is a **conjecture**; a positive
would be an 87 unconditionally, but a negative needs a control against complete
k=3/b=1 shells first.

**U-13 — untried alternative universes and unbuilt successors (VERIFIED-IN-LOG).**
(a) `U₁` as the named universe (38,240 masks, 665,024 CF-split literals, contains
84/88 of the 88@5's masks) — intrinsic and complete for its index, **untried**;
given that V2's diagnosis is that *slot/cardinality* reasoning is what kills these
solves, trading slots for a 50× bigger covering layer is plausibly the right
trade. (b) **V1-2(b)'s successor tier-3 model** — re-parameterise the cancel mode
as `(z, O from 1,680 theorem-derived masks, A over splits)`, removing the corpus
from the vocabulary entirely and making the scope of a NO "exact for `V₁`" rather
than "exact for a list taken from five circuits". Fully specified, sized, with
both mandatory control gates written down. **Never built.**

**U-14 — A2 has never been asked the right way (VERIFIED-IN-LOG).**
The 223-mask union question at budget 87 has timed out three times (SAT 2,013.6 s;
PB 3,601 s). But the **pinned control now SATs in 1 s** — the admissibility control
the question never had — and V2's own measured law says PB should be run in
**optimisation mode, never as a budget ladder**. A2 has only ever been run as a
decision at a fixed budget. It now has a validated model attached and has never
been retried under the lesson the same lane learned.

**U-15 — small unanswered structural questions, each cheap (VERIFIED-IN-LOG).**
(a) **What do the diagonal-class heavy gates buy?** The classes `{7,23}` and
`{15,31}` hold **no target at all**, are seeded by 168 and 173 of 204 families,
carry 3–5 gates each, and *"nothing in this lane explains what they buy"*. Listed
in `PROGRAM_STATE.md` as **unassigned**. Every known 88 pays for at least one
target-free class and nobody knows why. (b) **The cashing law should be provable
outright** — 425/425 measured, with a stated proof route (it is Theorem 4 at
budget 1); proving it would upgrade u2's cuttability criterion from a 299/300
empirical rule to a theorem.

**U-16 — four different counts of the same 88 population are in circulation
(VERIFIED-IN-LOG; a contradiction flagged and never reconciled).**
33,010 (`pop88_worklist.jsonl`) / 35,999 (`PROGRAM_STATE.md`) / 36,810
(`m2_oracle/LEDGER.md`) / 41,108 (u2's deduplicated census). U6's notebook flags
the last two as *"unreconciled and an open item"*; it was never resolved. Given
u2's demonstration that `cores.npy` calls known-old 88s novel (the 128-bit /
64-bit truncation bug), **any public claim of the form "we covered the entire
known 88 population" inherits this ambiguity and must be reconciled first.**

**U-17 — data generated and never analysed (SMELL, both cheap to check).**
(a) `understanding/u7_representation/data/boundprobe_{7,42,99}.{json,log}` — three
seeded runs completed 2026-08-14, 61-byte JSONs, **no discussion anywhere** in the
notebook or `REPRESENTATIONS.md`. (b)
`understanding/u2_walls/data/mask_enrichment.json` — produced by
`mask_enrichment.py`, and the notebook's standing-claims section contains no
mask-enrichment claim. Given that **92.2 % of every cut ever found adds one of two
masks**, a mask-enrichment analysis is exactly the follow-up that would say
whether those two masks are enriched anywhere else.

**U-18 — a path in the record points at a directory that does not exist locally
(VERIFIED-IN-LOG, harmless but it will mislead).**
`u7_representation/NOTEBOOK.md`'s FINAL STATUS cites
`u7_representation/data/QUARANTINE_unvalidated/` (143 decided configurations).
That directory is **not** under `understanding/`; it is at
`beat88/pod_salvage/pod2/u7/beat88/understanding/u7_representation/data/QUARANTINE_unvalidated`.
Anyone reading the notebook alone will conclude the data was lost. (It is *void*
data, so nothing depends on it — but fix the path in the record.)

**U-19 — U6 wrote its spec believing U5 did not exist (VERIFIED-IN-LOG).**
`u6_spec87/NOTEBOOK.md` §4: *"To U5 (heavy corner). Not present in
`beat88/understanding/` as of this writing."* U5 existed and was built the same
day. So `SPEC87.md`'s Phase B specifies only an *interface* to a heavy-corner
library it never saw, and **the U5 × U6 join was never made** — in particular,
whether the ≥ 27 heavy-gate floor interacts with the price certificate. U7 made
the U5 × U7 join; this one is missing.

---

## 6. HAZARDS

0. **THE WHOLE SLICE IS UNTRACKED IN GIT.** `git ls-files beat88 | wc -l` → **0**;
   `git status --porcelain beat88` → `?? beat88/`. Not one of the 1,463,947 files
   — including all 120 write-ups, both refereed lower-bound certificates,
   `CANON.md`, and every export — is under version control. There is no second
   copy of anything except where `pod_salvage/` happens to mirror a lane. **Every
   deletion proposed in §4 is irreversible, and the 47 GB has no backup.** Before
   any deletion, the `.md`/`.py`/certificate layer (~15 MB) should be committed or
   copied off the box.

1. **`pod_salvage/` is irreplaceable and its sources are gone.** Both pods
   (38.80.152.147:41863 and 213.173.105.99:42056) were terminated on 2026-08-15/16.
   `pod_salvage/pod1` and `pod_salvage/pod2` are the only copies of ~18 GB of pod1
   and ~21 GB of pod2 run data, including 1,020,241 exported circuits, two 715 MB
   manifests, the 854 pod-side harvest segments, and every pod-side M2 sweep
   result. **Nothing under `pod_salvage/` should be moved or renamed without
   updating nothing** — but see #4 below on paths.
2. **`understanding/PROGRAM_STATE.md` records a standing backup warning:**
   *"REMINDER: campaign_87 (13.7 GiB population) now exists ONLY on this box."*
   That is a different slice, but the warning was issued from this one and should
   travel with the wrap-up.
3. **Nothing in `beat88/` is live.** I confirmed: `ps -eo pid,cmd | grep -E
   'beat88|census_watch|m3_census|m2_oracle|m5_backbone'` returns nothing, and no
   process has a cwd under `beat88/` (`ls -l /proc/*/cwd | grep beat88` → empty).
   The `STOP` / `STOP_SHIPPER` sentinel files in `m3_census/runs/{local,local_prev}/`
   are the *stopped* state and should be left in place — removing them would let a
   restarted fleet resume writing.
4. **Absolute paths are hardcoded in the resume commands, not in the code.** The
   code uses `kernel.repo_root()` (which finds the checkout from either the local
   or the pod layout, overridable with `SLP_ROOT`) and
   `sys.path.insert(0, "<repo>/beat88/methods/shared")`. But the *documented
   resume commands* in `m2_oracle/STATE.md`, `m5_backbone/verify/STATE.md` §5, and
   `m3_census/FINAL.md` §6 are written against `beat88/methods/<lane>/code` as the
   cwd and against pod paths `/root/slp87`, `/root/slp87_pod2`. Reorganising the
   lane directories breaks every documented resume path.
5. **`m5_backbone/verify/shot87.py`'s resume reads
   `beat88/methods/m3_census/exports/<FILE>.json` directly.** If the exports tree
   is repacked into a tarball (§4.3), the 182-family resume path in
   `phaseB_remaining.json` breaks until it is unpacked. Keep at least the families
   named in `phaseB_remaining.json` extracted.
6. **`shared/lib/libslpkernel.so` is a build artifact that `kernel.py` rebuilds
   on import if missing or stale.** Deleting it is safe; deleting `csrc/` is not.
7. **No symlinks anywhere in the slice** (`find beat88 -type l` → empty), so there
   is no link-following hazard — but note that pod2's repo relied on
   `/root/slp87 -> /root/slp87_pod2`, which is why pod2-origin logs contain
   `/root/slp87` paths that were really pod2.
8. **Trim-backend hazard, if anything is ever re-run:** the C `trim` disagrees
   with Python on 14.5 % of states *above* 88 masks (0/1,671 at exactly 88). Any
   re-processing of `*.cells.jsonl` or the harvest must not switch trim backends
   mid-stream (`m1_cartography/analysis/b1-integration.md`).
9. **The wall clock on this box steps backwards** (`ALLOCATION.md` header; defect
   #11). Everything in beat88 was moved to `time.monotonic`, but any script
   resurrected from an older tree must be checked.

---

## 7. GAPS

1. **I could not read the compressed harvest.** `zstd` is not installed and
   Python has no `zstandard` module, so the 1,083 `*.pop.*.jsonl.zst` segments
   (337 MB) are characterised only by `ship_harvest.sh`'s documented format
   (sealed `.pop.jsonl` population segments, zstd -12, sha256-verified) and by
   filename. I therefore could not confirm their line counts, gate distribution, or
   whether local's pod-side segments were salvaged (LEAD L13).
2. **Distinct-orbit counts are not recomputed.** All 88/89/91 counts in §3 are
   *record* counts from the manifests. Turning them into distinct gauge orbits
   needs `shared/gauge.canon` over 1.55 M records (~0.087 s/state ⇒ ~37 core-hours)
   — outside the CPU budget for this wave. The one authoritative orbit count I
   can cite is 33,010, from `pop88_worklist.jsonl`'s line count.
3. **I did not reconcile the pod manifests against the local one for duplicates.**
   The three hosts ran disjoint lane labels (`local_*`, `pod1_*`, `pod2_*`) so
   overlap should be small, but shared labels exist (`p3a`, `m3a`…`m3l`, `res_12`,
   `warm_13`) and `m2_oracle/STATE.md` documents a real **split-brain** for
   `m3u9` and `chain91_000` k=4 rows existing on both pods. Any public "N circuits
   available" number must dedupe by `canon_id` first.
4. **The 8 `.nohup` files that differ from their `.log` partner were not
   diffed.** I confirmed only that they differ, not why (probably a truncated tail
   from a killed shipper).
5. **`understanding/` was read by a delegated sub-agent, not by me directly.** Its
   findings are integrated in §2A and §5; where that read is thin — particularly
   the internals of `u2_walls/data/{census.jsonl 179 MB, u4_gates.jsonl 109 MB}` —
   I have marked the files KEEP pending a closer look rather than proposing
   deletion.
6. **No bulk re-verification.** Per the brief I verified two circuits
   (`RECORD_mixcolumns_91gates_depth4.json` and one depth-5 88), both VALID. The
   remaining 1.25 M export files are unverified *by me*; they were verified by the
   fleet at export time (`live_gates` recorded per record) and the campaign's
   oracle has a documented zero-false-claim record.
7. **Compression ratios in §4 are estimates.** I could not run `zstd` to measure
   the actual ratio on `*.cells.jsonl`; the 10–20× figure is inferred from the
   file shape (highly repetitive JSONL with long repeated key sets) and from
   `ship_harvest.sh`'s own measured ~150:1 on the more repetitive `.pop.jsonl`.
