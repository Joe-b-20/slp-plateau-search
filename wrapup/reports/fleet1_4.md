# Slice report: fleet1–fleet4 (fleet campaign waves 1–4, 2026-08-19 → 2026-08-22)

Agent model: Claude Opus 5 (1M). Date: 2026-08-29. Read-only pass; the only file
written is this one.

**Summary.** Nine lanes, ~45 MB, 6,750 files, all nine with a full `RESULT.md`
and four with an independent adversarial `REFEREE.md`. This is the best-documented
part of the tree I have seen: every lane re-derives its numbers from an append-only
ledger, every negative carries a named fired control, and three lanes' referees
overturned or narrowed their own lane's conclusions in writing. The four waves are
one continuous arc: wave 1 built the **V2 region-pricing model** (lane A) and the
**quotient-counting** floor method (lane B), plus a proof-side survey (lane C) and a
hygiene sweep (lane D); wave 2 turned the model into a **record-free generator**
(lane G) and produced the first unconditional link between `L` and `L_cf` (lane P);
wave 3 **closed the flagship-cell 87 door by refereed theorem** (lane CB) and found
the one missing modelling rule — the tap plane is *shared*, not exported — which
built a from-scratch **VALID 88** (lane F4); wave 4 added a **depth-capped exact SLP
oracle** and reproduced record 88@5 block-for-block at depth 5 (lane DEPTH). No
circuit ≤ 87 was found anywhere in the slice, and no `experiments/STOP` exists.
I catalogue **34 distinct methods**, count the artifacts, and record **11 leads** —
of which four are results that *landed after their RESULT.md was written and were
never collected*, including one (a possible 90 @ depth 4) that would move a repo
frontier if a single still-undecided SAT call comes back SAT.

---

## 1. INVENTORY

```
du -sh fleet1 fleet2 fleet3 fleet4
15M fleet1   18M fleet2   11M fleet3   628K fleet4     (~45 MB)
find fleet1 fleet2 fleet3 fleet4 -type f | wc -l   ->  6750
```

| path | size | files | what it IS | documented? |
|---|---|---|---|---|
| `fleet1/laneA_v2pricing` | 4.1M | 786 | The **V2 model**: mask↔8-nibble line coordinates, blocks by value support, exact per-block pricing of 22 known circuits; the flagship-cell R01 architecture sweep | `RESULT.md` (196 L), `ledger.jsonl` (667 rows), `code/tally.py` |
| `fleet1/laneB_regionbounds` | 1.1M | 161 | **Region lower bounds** for R01/R34 by T-structured quotient counting + lemma-fortified CNF climbing; cube-banked exact search | `RESULT.md` (266 L), ledger 87 rows, `cubes/*.jsonl` |
| `fleet1/laneC_proofside` | 488K | 59 | **Proof side**: `C_c` conjecture attack, `L2` socle-tower bracket `[17,26]→[22,26]`, ladder repricing errata, cap table | `RESULT.md` (781 L) — the most self-critical document in the slice |
| `fleet1/laneD_completions` | 8.7M | 647 | **Completions/hygiene**: V1.5 optimist-DP, basin edit-closure sweeps, corrected backward search, records-update note | `RESULT.md` (521 L) + `RECORDS_UPDATE_NOTE.md` (154 L); 3 ledgers |
| `fleet2/laneG_generator` | 13M | 2992 | The **standalone theory-first generator** + the derivation of the committed interface sets; 1383-class module sweep; ladder DP | `RESULT.md` (575 L), `referee/REFEREE.md` (278 L), `notes/` (2 digests) |
| `fleet2/laneP_proof` | 4.7M | 89 | **The cancellation budget**: Theorems P1/P2, residual hierarchy certificates, the LP-integrality-gap obstruction (route ceiling 83) | `RESULT.md` (864 L), `referee/REFEREE.md` (492 L), `verify1/` independent falsifier (8,074-row ledger) |
| `fleet3/laneCB_completeness` | 9.7M | 1821 | **Completeness / the 87 door**: is the diagonal narrowing complete, and is the flagship-cell R01 87 door shut? Answer: yes and yes, by refereed theorem | `RESULT.md` (520 L), `referee/REFEREE.md` (258 L) + a **forgery sandbox** |
| `fleet3/laneF4_rule` | 1000K | 147 | **The shared-plane rule** + `gen(88)`: a from-scratch VALID 88-gate circuit built from theory with no search over circuits | `RESULT.md` (908 L), **`WALKTHROUGH.md` (155 L)**, `referee/REFEREE.md` (370 L, two sessions), `check_indep/`, `audit_gap/` |
| `fleet4/laneDEPTH` | 624K | 48 | **Depth**: an exact min-gates-under-a-depth-cap SLP oracle with levelled inputs; gates-vs-depth curves; 88 @ depth 5 emitted | `RESULT.md` (535 L), ledger 267 rows, `results/dcache.jsonl` |

**Nothing in this slice is opaque.** Every subdirectory is covered by a
`RESULT.md`; every `code/` has a `tally.py` that re-derives the prose numbers.

File-type breakdown (the bulk is regenerable solver plumbing):

```
find <lane> -path '*/inst/*' -type f | wc -l ; ... -path '*/logs/*' ...
lane                     inst   logs   .py   .json
laneA_v2pricing           358    379    14    382
laneB_regionbounds         82     14     6     88
laneC_proofside             0      0    18     12
laneD_completions           0      0     3    619   (601 = bwd_out/)
laneG_generator          1453   1470    22   1474
laneP_proof                 0     10    34     22
laneCB_completeness       795    864    62    851
laneF4_rule                38     43    31     44
laneDEPTH                   0      5    22      4
```

`inst/` + `logs/` alone: laneG 11.3 MB, laneCB 6.6 MB, laneA 3.0 MB = **~21 MB of
the 45 MB slice**.

---

## 2. METHODS

### v2-region-pricing
- **Family:** class-pricing model / exact block decomposition.
- **What it does:** Changes coordinates so a 32-bit mask becomes 8 nibbles on
  "lines"; partitions a circuit's gates by the line support of each gate's *value*
  into ~10 blocks (currency per line, plus region blocks); prices each block by an
  exact minimum-gates decision given a committed interface. The sum is a true lower
  bound for any circuit in the class realizing that configuration.
- **Twist vs siblings:** The first model that contains the records' *joint* region
  economy — currency, sector work, tap supply and hosting priced **together**
  (folded `W07`/`W3` blocks). M1/V1.5 priced chains; the tightness theorem priced
  sector work *given* imports; this prices the entanglement natively.
- **Measured performance:** All 14 known 88s decompose with zero residue and price
  at **exactly 88**; 89@5/89@10 → 89; two compiled M1-optima → 91. **~50 exact block
  decisions, 18 heavy probes + full control tier, ALL TIGHT** — every decision the
  solver finished returned exactly the record's own block size; zero sub-witness
  blocks in the whole campaign. In-cell R01 core values exactly constant across
  records (18,18,18,19,19,19); R34 core (22×10, 23×4).
  `fleet1/laneA_v2pricing/RESULT.md` §"budget table", `§Joint-block probes`.
- **Cost:** `ledger.jsonl` 667 rows, 26 `exact`, 9 `crash_or_timeout`; overnight
  campaigns across 2 days on 6 cores. Undecided brackets left: `U3` at nb=11–13 (2–8 h
  timeouts each).
- **Code:** `fleet1/laneA_v2pricing/code/{v2lib,decompose,subblocks,extract_configs,price,control,probes}.py`
- **Logs/results:** `results/decomp_*.json` (22), `results/configs.json`,
  `results/solve_cache.jsonl` (359 rows), `inst/` 358, `logs/` 379 (1.5 M each).
- **Generality:** MC-HARDCODED in its coordinates (the trace-dual basis and the
  tap ladder come from the AES field), CIRCUIT-GENERIC in method. For
  `aes_inv_mixcolumns` the ladder `2·d_k = d_{k-1} + τ_k d_7` re-derives
  mechanically from the same reduction polynomial; the block list and the sector
  target `(p_j,q_j)` must be recomputed.
- **Phase-2 verdict:** **keeper — the backbone.** Every downstream lane
  (G, CB, F4, DEPTH, and fleet5/8/9/12) reads its `configs.json`.

### joint-block-probe (folded W07 / W3)
- **Family:** class-pricing, twist on `v2-region-pricing`.
- **What it does:** Instead of pricing `COL0` and `U07` separately, folds them into
  one block and asks the exact oracle for the joint minimum, so the solver may
  spend a gate that serves two roles.
- **Twist:** prices *multi-role* gates, which a per-block model structurally cannot see.
- **Measured performance:** 18 folded probes, 18 tight. Mechanism read off an
  optimal witness (88@5fs `U07`, exact 8): **7 of its 8 gates ARE instance targets**
  — the supply exported downstream *is* the sector work.
- **Cost:** minutes to 8 h per probe (`solve_cache.jsonl`).
- **Code:** `fleet1/laneA_v2pricing/code/probes.py`.
- **Generality:** MIXED. **Phase-2 verdict: keeper** — the cheapest way to detect
  that a decomposition is losing gates at a seam.

### g01-singleton-exhaustion
- **Family:** exhaustive committed-value sweep.
- **What it does:** For a fixed cell, asks for every single candidate interface value
  `w` whether committing it lets the downstream block come in under the record
  (`U1({w}) ≤ 7`), each an exact capped UNSAT.
- **Twist vs `ambient-relaxation`:** decides one value at a time — complete over
  singletons, structurally blind to jointly-enabling sets.
- **Measured performance:** **240/240 candidate values individually useless, 0
  timeouts** (`ledger kind=g01_single`, 504 rows / 480 `useless` across two arms).
  Hence `G01 = 18` against every `|Q'| = 1` configuration. The multi-value closure
  it could not reach was later decided by lane CB.
- **Cost:** ~a day of a 6-core arm.
- **Code:** `fleet1/laneA_v2pricing/code/g01sweep.py`, `g01stage2.sh`.
- **Generality:** CIRCUIT-GENERIC given a block model.
- **Phase-2 verdict:** **superseded-by-ambient-relaxation** (lane CB decides all
  sizes at once, SAT-free, in 0.4 s) — but it stands as the independent
  computational leg of that closure.

### fullspan-closure-solve
- **Family:** monolithic exact solve (a **negative methodological result**).
- **What it does:** Offers the downstream block the entire 255-value span free and
  asks for the optimum at the improving level — one solve deciding all committed
  sizes at once.
- **Measured performance:** **Failed, three times, in three lanes.** Lane A: 4 h,
  `status=crash_or_timeout`, **0-byte solver log** (the `SLPV` redirection hazard) —
  no lower bound at all. Lane G reproduced the failure (263 inputs, timeout at
  240 s, bracket only). Lane CB: 66 min without completing even `k=4`, logged
  `kind=oracle_attempt status=aborted_no_level`, explicitly **not** a negative.
- **Cost:** ~5 h wasted across three lanes.
- **Code:** `fleet1/laneA_v2pricing/code/fullspan.py`.
- **Phase-2 verdict:** **dead-end.** Three independent measurements say
  `atlas/slp_opt.py` cannot decide a 263-input dim-12 instance. The lesson lane CB
  extracted is the reusable one: *push constraints into the instance rather than
  sweeping loose ones — a 4-element `Q` decides in 24–70 s where a singleton does
  not decide in 3100 s.*

### quotient-counting-lemma
- **Family:** structural lower bound (new to the project in wave 1).
- **What it does:** For a region module `M = lines ⊗ T` and any subspace `W` of the
  line space, projecting along `W⊗T` maps any valid program for the region to a
  valid program for the quotient instance (delete zero and duplicate projections).
  So `L(region) ≥ L(π_W-instance)` unconditionally, and the quotient instances are
  dimension 4 or 8 — decidable — where the region is 12 or 16 and is not.
- **Twist vs siblings:** it is a *floor transfer*, not a search accelerant; all its
  solves are one or two dimensions below the cost wall.
- **Measured performance:** R01 (floor to beat 15): `qk2 = 13`, `qk3 = 11`,
  `qk5 = 10` EXACT; `qk4 (kill-d7) ≥ 14` at write-up. **Reading: killing the d7 line
  — deleting the C7 import currency — is what makes the region expensive.** That is
  the economic signature of the records' entanglement, measurable for the first time.
  Honest ceiling stated in the lane: `max_W L(π_W)` — no LP combination beats the max,
  because a full-line-support gate is visible to every quotient.
- **Cost:** measured level curve for `qk4` (local CPU-s): k=11: 58, k=12: 689,
  k=13: 17,469 — ×10–25 per level. **See LEAD L1: k=14 landed after write-up.**
- **Code:** `fleet1/laneB_regionbounds/code/{quotients,qsolve,mklemmas,pricing}.py`
- **Logs/results:** `cubes/*.jsonl` (ground truth, one record per cube),
  `inst/` 14 R01 + 65 R34 quotient instances.
- **Generality:** **CIRCUIT-GENERIC** wherever the target module has a tensor
  structure `lines ⊗ T`. This is the most portable lower-bound tool in the slice.
- **Phase-2 verdict:** **keeper** — it certifies `R01 ≥ 14` at ~1/10 the compute of
  the direct route.

### lemma-fortified-cnf (tight mode)
- **Family:** SAT encoding augmentation; twist on `quotient-counting-lemma`.
- **What it does:** Injects "at least `m` of the `k` gates project nonzero under
  `π_W`" as cardinality clauses into the region CNF — a proven consequence, so UNSAT
  stays a theorem and every witness survives. **Tight mode:** when the level being
  decided equals a lemma bound, every gate's projection must be nonzero, distinct
  and new, so the projected program is itself minimal — much stronger propagation
  exactly at the frontier level.
- **Measured performance:** **SOUND but MARGINAL as an accelerant.** Matched-cube
  measurement at k=13, same host: fortified/plain = **0.82×** (~1.2× faster).
  Static soundness control: the verified 22-gate witness satisfies every lemma.
  Dynamic planted control (`tighttest`): SAT with verified witness at `k = bound`.
  Two instrument bugs found in review and logged (vacuous cardinality counter —
  never unsound; qsolve EXACT-overclaim at capped kmax — erratum for `qk6`).
- **Code:** `fleet1/laneB_regionbounds/code/fortify.py` (proof in the docstring).
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper with the honest caveat** — the value is arithmetic
  floor transfer, not solver speed. Lane P then proved the *strictly stronger*
  version (see `quotient-exact-form`) that lane B never got to run.

### cube-banked-resumable-exact-search (qsolve / split2)
- **Family:** cube-and-conquer engineering.
- **What it does:** Splits the level-`k` decision into cubes (and split2: a two-level
  partition into 1008 cells), banks one JSONL record per cube, and treats a level as
  proven only at full cube coverage. Process death costs nothing.
- **Measured performance:** k=12 (1008/1008 UNSAT, 1,793 CPU-s), k=13 (1008/1008,
  19,741 CPU-s), **k=14 (1008/1008, 484,561 CPU-s)** — see LEAD L1. Also re-proved
  the pod's plain k=12 and k=13 R01 UNSATs locally from scratch (120/120 cubes each).
- **Cost:** measured **local-CPU per pod-wall-second: 29.3× (k=12), 24.9× (k=13)**.
- **Code:** `fleet1/laneB_regionbounds/code/qsolve.py` (`--shard`, split2).
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper** — the correct default for any long exact search.

### cost-curve-pricing
- **Family:** methodology / campaign planning.
- **What it does:** Measures the per-level cost growth of an exact search on real
  levels, then extrapolates to price the next rungs in pod-hours before spending them.
- **Measured performance:** Killed generic climbing with a number: at the measured
  10–17.5× per-level growth, certifying `R01 = 22` costs **7.7e10 – 3.7e12 pod-seconds
  (~2,400 – 117,000 pod-years)**. `R34` is astronomically worse. **No compute budget
  certifies the record regions by climbing.** Same technique repriced lane C's ladder
  (`minE ≥ 7` at `|K| = 15` = 1e15–1e16 nodes = pod-*months*, not the pod-day the
  predecessor note had budgeted) and lane C's `L2` exact (a 2e15-node problem).
- **Code:** `fleet1/laneB_regionbounds/code/pricing.py`; lane C §2.3, §3.3.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper — the single highest-leverage habit in the slice.**
  It saved this project pod-months twice in one wave.

### minE-exhaustion (orderly generation)
- **Family:** certificate over a combinatorial characterisation.
- **What it does:** A minimal circuit and a minimal *realizable mask set* containing
  the targets are the same object (dedup and stripping weight-<2 masks never grow a
  set), so `L = #targets + minE` **exactly** for the right instances. Exhausting the
  "extra masks" search to depth `k` then proves `L ≥ #targets + 1 + k`. Two prunings,
  each with a proof: P1 (last-level candidates must close a target) and P2 (orderly
  generation — skip `c < prev` if `c` was already a candidate).
- **Twist:** the reduction, not the pruning, is what makes it work; both were
  re-derived independently by two agents.
- **Measured performance:** `L2` bracket **`[17,26] → [22,26]`**. Depth 5 exhausted
  **three times**: pruned (294,188,302 nodes), **pruning-free** (80,092,627,410 nodes,
  8/8 shards NONE, 4 h 26 m), and by an independent from-scratch implementation
  (1,795,955,245 nodes). The two *unpruned* trees are node-for-node identical
  (425,649,382 vs 425,649,383 at k=4 — a root-counting offset). Nodes ×~50 per level.
- **Cost:** ~5 h wall for the pruning-free run at 2 concurrent.
- **Code:** `fleet1/laneC_proofside/code/mine2.c`, `l2_build.py`, `validate.py`;
  independent implementation in `verify1/`.
- **Logs/results:** `runs/l2_k5_unpruned_s*.out`, `validation.jsonl` (120 rows).
- **Generality:** **CIRCUIT-GENERIC** — the `L = n + minE` identity needs only
  "targets distinct, weight ≥ 2, none an input, inputs a basis".
- **Phase-2 verdict:** **keeper.** But note the strategic caveat lane C states and
  nobody else had: **every bound from a tower rung is capped at 51 (level 3) or 26
  (level 2), both below the refereed 56** — so exact `L2`/`L3` cannot improve
  `L(M)` at all. Use it for calibration, never as a bound route.

### brute-force-oracle-validation
- **Family:** instrument control.
- **What it does:** Decides random small instances twice — once by the searcher under
  test, once by a definitional brute force over the *full* mask universe — and
  requires the batch to contain genuine negatives or be declared **vacuous and
  discarded**.
- **Measured performance:** 120/120 agreement; distribution `0:1, 1:23, 2:42, 3:30,
  >3:24` (24 genuine negatives). **This control caught a real bug**: the first
  `mine2.c` failed 8/120 (a stale candidate-map entry made it *miss* completions,
  i.e. produce false negatives). The independent verifier's *first* 120-instance
  batch produced zero genuine negatives — it declared the batch **vacuous and
  regenerated it with a weight-4 target floor**, unprompted.
- **Code:** `fleet1/laneC_proofside/code/validate.py`, `verify1/{oracle,xcheck}.py`.
- **Phase-2 verdict:** **keeper — the discipline, not the code.** Every negative in
  this slice traces back to a control of this shape.

### provably-optimal-census (c0_census)
- **Family:** structural measurement.
- **What it does:** Samples admissible keep-sets `K` where `minE_K` is known exactly
  *with no search at all* (`minE = 0`: the free target closure completes;
  `minE = 1`: one extra completes), giving provably optimal mask sets for matrices at
  the bottom of a Theorem-N chain, then measures a structural quantity on them.
- **Twist:** every prior measurement of the same quantity in this project was taken
  on circuits nobody had proved optimal.
- **Measured performance:** 8,000 sampled 14-sets → **527 provably optimal mask
  sets** (181 + 346). Best wiring: `z = 0` in 485, `z = 1` in 42, **max z = 1**. At
  cert 5, `L(M|_K5) = 37` exactly and its 37-mask optimum can be wired so **every one
  of the 14 live inputs has fanout ≥ 2** — `C_0` at the bottom rung.
- **Code:** `fleet1/laneC_proofside/code/{c0_census,cert5_exact}.py`; `c0_census.json`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper** — this is how you get evidence about optimal
  objects without being able to find optimal objects.

### forced-fanout-rewiring
- **Family:** structural measurement.
- **What it does:** An SLP is a mask set *plus* a parent-pair choice; separates what
  is a property of the set from what is a wiring artefact. "Forced" = the number of
  live inputs `x` having at most one available mask `m` with `m ⊕ x` also available —
  such an `x` has fanout 1 in *every* wiring.
- **Measured performance:** `88@5: z=3 (forced 3)`, `88@5fs: 5 (4)`, `88@6: 5 (5)`,
  `88@7: 6 (3)`, `88@8: 6 (3)`, `89@5: 1 (1)`, `92@4: 3 (3)`, `97@3: 0 (0)`. Every
  re-wiring quoted was replayed and produces all 32 rows.
- **Code:** `fleet1/laneC_proofside/code/rewire.py`; `rewire.json`.
- **Phase-2 verdict:** **keeper.** Lane P's independent agent later *exhausted* the
  wiring space and found **four of the five record 88s have a UNIQUE valid wiring** —
  which is what makes any per-circuit structural claim meaningful.

### transvection-sibling-matrix
- **Family:** structural analysis / exact accounting.
- **What it does:** From the `z` fanout-1 live inputs of a circuit builds an explicit
  invertible `Q` (invertible **by triangularity in program order**, not by composing
  transvections), forms `M' = M·Q^{-1}`, emits the shortened program and replays it.
  Gives `L(A) − Σ wt(m_x) ≤ L(A·Q^{-1}) ≤ L(A) − z`.
- **Measured performance:** `88@5 → 85`, `88@5fs → 83`, `88@6 → 83`, `88@7 → 82`,
  `88@8 → 82`, `89 → 88`, `92 → 89`, `97 → 97`, `91@4 → 89`. Sharp form on 88@5 and
  88@6 (every `u_x` is an input): `L(M·Q^{-1}) = L(M) − 3` and `− 5` **exactly**, for
  two explicit matrices in `M`'s column-operation orbit. Referee re-executed on six
  record 88s with row-by-row verification.
- **Code:** `fleet1/laneC_proofside/code/transvect.py`; `sibling_matrix.json`.
- **Phase-2 verdict:** **keeper as accounting; the obstruction reading was WITHDRAWN
  in the lane itself** (rigidity implies `C_c`, not conversely; "for all invertible
  `E`" is vacuous since `E = M^{-1}` gives `L = 0`).

### counterexample-family-construction
- **Family:** hand-reasoning + exact verification.
- **What it does:** Builds an explicit matrix family `A_k` whose optimum and whose
  *unique* optimal SLP are both provable by hand, then confirms with an exhaustive
  solver at small `k`.
- **Measured performance:** `L(A_k) = 5k`, every optimal SLP has exactly `k` fanout-1
  inputs. Referee re-derived it, ran `atlas/slp_opt.py` to exhaustively proven optima
  (`L(A_2)=10`, `L(A_3)=15`) and enumerated **all** optimal SLPs for `k = 1..6` —
  exactly one each. **Kills the class-level form of `C_c`** — but the referee then
  bounded what it shows: `A_k` needs `#rows/#cols ≥ 1.67` while the chain invokes
  `C_c` only at `≤ 1.39`, so the missing hypothesis is **coarse** ("average row
  weight ≥ 4"), not fine structure of `M`.
- **Code:** `fleet1/laneC_proofside/verify2/{ak,ak2,claim3}.py`.
- **Phase-2 verdict:** **keeper — the cheapest way to kill a conjecture's class-level
  form**, and the referee's regime analysis is the template for not over-reading it.

### cap-table-analysis
- **Family:** structural analysis (survey).
- **What it does:** Classifies every unconditional lower-bound technique in the
  repository as a *reduction*, a *charge*, or a *certificate*, and gives each family
  a proved or measured ceiling.
- **Measured performance:** Lemma P ~40; class-rank 32; heavy-corner ledger 52; edge
  counting 33 (**refuted by the records**, which evaluate to 31–33); linear-counting
  LP 46.2; Theorem-N chain 56 today, ≤ 73 under `C_0`; tower rung 51; backward
  identity **circular** (`a = F − 64 + c + 2d` identically — a change of variables
  carrying zero information). **Exactly one family is above 88: `L_cf(M) ≥ 92`.**
  Plus a proved payment-budget theorem: every adaptive chain from `M` to `M|_{K5}`
  pays ≤ 51 total, so a uniform per-stage payment of 3 is **refuted unconditionally
  by the record circuit**, and the `C_c` family stops at 73 even at `c = 0`.
- **Phase-2 verdict:** **keeper — read this before funding any bound work.** Its
  conclusion ("the whole optimality question is exactly *what does cancellation
  buy?*") is what wave 2's lane P then executed.

### optimist-pessimist-bound-DP
- **Family:** class lower bound over a partial corpus.
- **What it does:** Runs the class DP twice — once with each unpriced cell at its
  proven *upper* bound (pessimist: reproduces the published class optimum, the
  control) and once at its proven *lower* bound (optimist: a valid class lower
  bound). Adds a floor-sensitivity sweep to see how far the family can go.
- **Measured performance:** **The V1.5 optimist shortcut is DEAD, and not narrowly.**
  Pessimist returns **exactly 91** with a σ table 11× larger than the original —
  the control fires. Optimist returns **58**. Floor sweep: 4→58, 5→66, 6→74, 7→82,
  8→90, 9→91 — **exactly +8 per unit of floor** (one per sector), so ≥ 88 needs a
  universal per-sector floor of 8, and **553 measured exact cells sit at σ = 6**, so
  floor 8 is refuted *by measurement*. Honest bracket: V1.5 class optimum ∈ **[58, 91]**,
  not "= 91". Corpus completion priced at **≥ 2,000 CPU-h** (201,976 instances).
- **Code:** `fleet1/laneD_completions/code/v15_dp_lane.py`; `optimist_dp.log`,
  `pessimist_dp.log`, `floor_sweep.log`.
- **Generality:** MIXED (the corpus is MC-specific; the two-mode + sensitivity
  pattern is generic).
- **Phase-2 verdict:** **keeper as a pattern** (run the DP in both modes and sweep
  the floor *before* buying corpus); the specific V1.5 route is a **dead-end**.

### targeted-cell-pricing (lazy / cutting-plane)
- **Family:** partial exact pricing; twist on the DP above.
- **What it does:** Identifies which unpriced cells the optimist chain actually leans
  on and solves exactly just those, then re-runs the DP.
- **Measured performance:** Five cells priced at 9 / 9 / 10 / ≥10 / ≥10 against a
  floor of 4 — **individual cells are cheap to lift, and even a timed-out `slp_opt`
  run pays** (the UNSAT ladder it completed is a machine-checked lower bound).
  **But installing all five moves the bound 58 → 58**: the argmin simply relocates to
  another of the 271,109 unpriced cells. **~2,900 solver-seconds bought zero gates.**
- **Code:** `fleet1/laneD_completions/code/v15_targeted.py`; `v15_targeted_results/` (15 files).
- **Phase-2 verdict:** **dead-end for this corpus** (the unpriced set is too large
  for cut generation) — but the "a timeout is a bracket, not a refutation" lesson is
  a keeper and is applied everywhere else in the slice.

### basin-edit-closure-sweep
- **Family:** plateau-search / neighbourhood exhaustion.
- **What it does:** For a known circuit, deletes `k` non-target masks, **forbids**
  them, and asks whether the targets can be re-completed for ≤ `k` gates. A `k−1`
  completion would be a descent (an 87); a `k` completion is a lateral move on the
  plateau.
- **Twist vs local descent:** the forbid step is what makes a `none` verdict mean
  something — the instrument cannot re-derive what it deleted.
- **Measured performance:** Controls re-fired in-session on both geometries before
  any negative was banked: AU0 0 violations / AU2 0 mismatches / AU3 0 of 143 & 0 of
  120 / **PC-PLANT 40/40** / **PC-BYPASS 22 completions, 22 oracle-VALID**.
  Both sweeps then ran to completion: **27,720 / 27,720 triples each**.
  **Zero completions at k ≤ 2, i.e. zero 87 candidates.** See LEAD L2 for the
  HIT-3 counts, which are much larger than the RESULT.md's snapshot.
- **Cost:** ~13,000–40,000 s per geometry on 2 workers.
- **Code:** `atlas/thinktank/phase2_alt_run.py` driven from
  `fleet1/laneD_completions/`; ledgers `basin_88at5fs.jsonl`, `basin_88at6.jsonl`
  (2.9 MB each, 27,720 rows each).
- **Generality:** CIRCUIT-GENERIC given a verified circuit to sit on.
- **Phase-2 verdict:** **keeper** — the only method in the slice that generated
  *new verified circuits* at the record gate count, and its negatives are the
  strongest local-rigidity statements available.

### backward-frontier-search
- **Family:** randomized constructive search (backward from targets).
- **What it does:** Saturates backwards from the targets under a scored candidate
  order, with a *safe closure* engine (the previous engine "free-split through open
  children" stranded 2–4 nodes on a realizable 88).
- **Measured performance:** **The published 96 does not survive the fix.** Mandatory
  plumbing control fired first: planted 88 node sets on three basins come back as
  oracle-VALID 88s with **0 stranded**. 400 runs in the published regime: **best 104,
  median 112**. Control arm with the *old* published policy on the *new* saturator:
  **106 — worse.** The two-step hop scorer `bwd9`: best 107 at n=64, **20–40× more
  expensive per run**, and trips a cycle defect at ~3–6%.
- **New instrument defect found (reported, not fixed):** `risky_close_one` can still
  reach a state whose χ relation contains a cycle — 0/400 (bwd8 rerank 1), 1/100
  (bwd8 rerank 0), 2/64 (bwd9). Always caught by `dag_to_gates`, so nothing invalid
  escapes, but it aborts sweeps and contradicts `tri_search.md` §2.2's "no ancestor
  test is needed at all" for the *risky* path.
- **Code:** `fleet1/laneD_completions/code/{bwd_frontier,run_bwd}.{py,sh}`;
  `bwd_out/` 601 files 2.4 MB, `bwd_best/` 4 files.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **dead-end at this budget** (frontier 104 vs record 88), and
  the lane says so honestly ("400 runs is under a third of the old budget;
  UNDECIDED, bracket [?, 104]"). Keep the *fix* and the plumbing control.

### records-hygiene-audit
- **Family:** bookkeeping.
- **What it does:** Re-verifies every claimed record file through the repo oracle
  today, re-derives gate counts from the JSON (not filenames), recomputes both hash
  conventions, recomputes pairwise Jaccards, and writes a maintainer-facing
  line-by-line change list without touching any published file.
- **Measured performance:** Found that **the published depth-4 frontier point is
  understated by a gate**: three independent oracle-verified 91@4 circuits exist on
  disk (cascade ladder / m3 census / atlas-M1 reschedule; Jaccards 0.556 / 0.433 /
  0.358 — three genuinely distinct lineages) while `README.md`, `spectrum.json`,
  `PAPER.md` and `PRIOR_ART.md` all still say 92@4. The shipped-92 file hash
  reproduces `spectrum.json`'s pin exactly, validating the hash convention used.
- **Code/results:** `fleet1/laneD_completions/RECORDS_UPDATE_NOTE.md` (154 lines,
  advisory, nothing edited).
- **Phase-2 verdict:** **keeper — and ACT ON IT** (see LEAD L11). This is directly
  goal-3/4 material for the public repos.

### theory-first-generator
- **Family:** class-pricing generator (the inverse of search).
- **What it does:** Derives the algebra from GF(2^8) and FIPS-197 alone (absolute
  trace, trace-dual basis by inverting the trace Gram matrix, mask↔line dictionary,
  the dual xtime chain **computed rather than tabulated**), decomposes the 32-target
  problem into ~10 blocks of dimension 8–16, asks the exact oracle for each block's
  provable minimum, replays the block programs into one global mask set, and verifies
  twice. **No search over circuits; no record circuit read at run time.**
- **Twist vs plateau search:** it constructs rather than searches, so a "miss" is
  loud (non-zero exit) instead of a silent claim.
- **Measured performance:** Emitted and oracle-VALID: **116@3** (0 oracle calls),
  **91@5**, **92@4**, **94@5**, plus 95/99/103 where the model price was an *upper*
  bound and the mask set de-duplicated below it (reported as the realised count).
  Referee re-ran all four and verified each with its own fresh subprocess. Derived
  dual basis `29 b0 58 05 a6 53 a4 52` matches `atlas/ring.py` independently.
- **Cost:** seconds to minutes per emission (block solves cached).
- **Code:** `fleet2/laneG_generator/generate.py`, `code/{theory,build,recipes,modules}.py`.
- **Generality:** **MIXED, and this is the most portable asset in the slice.** The
  ladder derives from the reduction polynomial (`τ_k`), so `aes_inv_mixcolumns`
  needs: a new target list from its own matrix, a re-run of the module sweep, and a
  new currency-menu source (flag F1 — see HAZARDS).
- **Phase-2 verdict:** **keeper — the centrepiece for aiming at another circuit.**

### module-sweep (capped σ predicate)
- **Family:** exhaustive table building.
- **What it does:** Generates the canonical sector interfaces from theory and asks
  the exact oracle the *capped* question `σ ≤ 7?` for each — cheap because a capped
  UNSAT terminates early.
- **Measured performance:** **1383 canonical classes, 3022 s wall, ZERO timeouts.**
  92 YES (σ = 7 with a 7-gate witness), 1291 NO (exhaustive capped UNSAT, σ ≥ 8).
  **Independent cross-check:** all six `(kind,|P|,|Q|)` σ-7 counts equal those from
  `atlas/m1_sigma.json` (13,153 rows, different session, different generator,
  different solver invocations); referee extended it to 466 shared decided classes,
  **0 disagreements**.
- **Code:** `fleet2/laneG_generator/code/{modules,sweep}.py`; `results/modules.jsonl`
  (1,409 rows, 461 KB).
- **Generality:** CIRCUIT-GENERIC given a sector decomposition.
- **Phase-2 verdict:** **keeper.** Two independently produced tables agreeing
  cell-by-cell is the strongest control in the slice.

### ladder-chain-DP (price spectrum)
- **Family:** exact DP over configurations.
- **What it does:** Outer loop over the hub menu, inner chain over the column menus,
  taps reading the hub; keeps a witness configuration for **every** achievable price,
  not only the minimum.
- **Measured performance:** achievable prices **91…107**, optimum **91**, and the
  optimal configuration independently re-derives `atlas/all7_config.json` — a genuine
  cross-lane agreement, not an import. Referee precision note: there are **exactly 2**
  configs at 91 and they are global `y`-rotations of each other, so "the DP selects
  `C_7 = {2,4,a,c}`" holds only up to that symmetry.
- **Code:** `fleet2/laneG_generator/code/ladder.py`; `results/spectrum.json`.
- **Phase-2 verdict:** **keeper.** Keeping the whole spectrum (not just the argmin)
  is what made `depthscan` and the 92@4 emission possible.

### min-depth-rescheduler
- **Family:** scheduling (no search).
- **What it does:** Depth is a property of the *schedule*, not the mask set. Level-BFS
  (level `L` = exactly the masks that are an XOR of two masks of level `< L`) gives
  the provable minimum level of every mask, hence the depth-optimal schedule for a
  fixed set.
- **Measured performance:** **Control fires the right way**: the eight record
  circuits are already depth-optimal for their own mask sets and come back unchanged
  — the tool is not manufacturing artefacts. It *does* find a full level of slack in
  the theory-compiled 91: `atlas/compiled_m1.json` **5 → 4**, verified
  `gates=91 depth=4 outputs_built=32/32 VALID` — equal to the best 91@4 on disk.
  Lane G's own naive 116-mask scheme: 4 → 3.
- **Code:** `fleet2/laneG_generator/code/build.py::min_depth_schedule` (copied into
  lane F4 and lane DEPTH).
- **Generality:** **CIRCUIT-GENERIC, zero adaptation needed.**
- **Phase-2 verdict:** **keeper — free gates-for-nothing at depth.** (`e4_depth`
  measured only 2 hits in 38,711 sets, so its yield on *found* circuits is small;
  its yield on *compiled* circuits was a full level.)

### free-supply-derivation
- **Family:** exact-oracle instrument. **The single most re-used method in waves 2–4.**
- **What it does:** Offers a downstream block a supply set `S` at **zero gate cost**
  and asks for the exact minimum. Because `S` is free, `U(S) ≤ U(Q)` for every
  `Q ⊆ S`: the answer is a machine-checked **lower bound for the whole family at
  once**, *and* the optimal witness hands back a concrete committed set.
- **Twist vs point probes:** one solve replaces `2^{|S|}` point probes, and the
  witness is a derivation rather than a fit.
- **Measured performance:** Lane A ran this with the entire 255-value span and it
  **timed out at 4 h**. Lane G narrowed the candidate family *from theory* (240 → 15
  tap diagonals; §4.1) and the instance dropped from 263 inputs to 35, solving in
  **170 s** with **`U1 = 6` EXACT** and derived set `Q1 = {(d0+d7)⊗4, ⊗6, ⊗e}`.
  Pricing the upstream block with it: `COL0 0 + U07 12 + U1 6 = 18` — **exactly the
  R01 core of every record at this cell**, reached without ever looking at a record.
  **5 of 5 derived committed sets are bases of `vT` realised as tap diagonals**,
  every one a different basis. Lane F4 then used the same instrument family-wide
  (Test F): offered all 24 one-gate shared-plane values, got `W3 = 8` EXACT in 1505 s,
  and the witness **independently selected `u(5,4)` — record 88@7's own stepping
  stone**, with no record read at any step.
- **Cost:** 2 s – 1500 s per solve depending on how narrow the family is.
- **Code:** `fleet2/laneG_generator/code/freesupply.py`; `fleet3/laneF4_rule/code/f4model.py`.
- **Generality:** **CIRCUIT-GENERIC.**
- **Phase-2 verdict:** **keeper — the best single tool in the slice.** The rule it
  teaches is: *narrow the family from theory first, then let the solver pick a
  member; never hand-pick one* (see `stepping-stone-non-interchangeability`).

### depthscan (min-depth configuration search)
- **Family:** search over the *model's* configuration space; twist on `ladder-chain-DP`.
- **What it does:** At a fixed model price, searches configurations for the one whose
  mask set schedules shallowest.
- **Measured performance:** the all-σ-7 family contains exactly 2 configurations
  priced 91 and **both schedule to depth 5**. A 91@4 configuration does exist
  (`compiled_m1`'s) but its `C_2` carries only 2 levels and so has σ = 8, putting it
  **outside** the swept family. **UNDECIDED: does an all-σ-7 91@4 exist?**
- **Code:** `fleet2/laneG_generator/code/depthscan.py`.
- **Phase-2 verdict:** **superseded-by-`depth-capped-exact-oracle`** (lane DEPTH),
  which puts depth inside the block decision instead of filtering afterwards.

### cancellation-weight-budget (Theorem P1)
- **Family:** structural theorem linking two complexity measures.
- **What it does:** For each target, unrolls its cone stopping at inputs and at
  cancelling gates ("maximal clean tree"); the leaf supports partition the target's
  support and the internal nodes are distinct clean gates. Refining each non-singleton
  leaf by a fixed hierarchy turns any SLP into a hierarchy family, so
  `|C| ≥ L_cf(M) − Σ_{m∈A*}(wt(m) − 2)`.
- **Twist:** the first theorem in the program that makes `L_cf(M) ≥ 92` a bound on
  `L(M)` at all — previously it was explicitly fenced off.
- **Measured performance:** Every 88 must spend a cancellation weight budget of ≥ 4,
  every 87 ≥ 5. Verified on all 11 wired circuits on disk; the records **overspend by
  a factor of ~19–22** (75/83/90/86/83 against a required 4), which is the honest
  measure of how lossy the crude refinement is. **Refereed — CONFIRMED** (proof
  rebuilt from scratch, non-circular against `L_cf ≥ 92`).
- **Code:** `fleet2/laneP_proof/code/{cflib,measure}.py`.
- **Generality:** **CIRCUIT-GENERIC** — needs only `L_cf` for the target matrix.
- **Phase-2 verdict:** **keeper.**

### residual-hierarchy-certificate (Theorem P2 + exactification)
- **Family:** certificate / LP over hierarchies.
- **What it does:** Splits every gate three ways — `n = κ + |counted| + Y` (κ =
  cancelling, counted = clean gates with an all-clean path to a target, Y =
  "dedicated" clean gates that exist only to feed cancellation) — then prices
  `counted` by a partial-hierarchy DP with the cancelling masks as free leaves.
  Re-optimises the price table *per circuit* by projected subgradient ascent, then
  **exactifies** it into integers over `D = 10^7` so a standalone verifier can
  re-check it.
- **Measured performance:** Instrument control reproduces U6-2 **to the digit**
  (numerator `910019782`, universe 1648, `c`-distribution `{1:1396,2:204,3:44,6:4}`);
  an independent ascent from scratch reaches 91.02172 vs the published 91.0019782.
  **On `88@7` the chain evaluates to exactly 88.000 (κ=26, Y=27, B=35.000 = |counted|
  — the residual LP is integral there).** For `88@7` and `88@5` the chain proves
  `n ≥ 88` **in exact integers, solver-free** — *"this circuit cannot be improved to
  87 without changing its cancellation apparatus"* is now machine-checkable. That is
  the first optimality-strength statement about a record circuit in this program.
- **Cost:** 6000 subgradient iterations per circuit, minutes.
- **Code:** `fleet2/laneP_proof/code/{resid,exactify,verify_exact,localize}.py`;
  `results/exact_*.json`.
- **Generality:** CIRCUIT-GENERIC given a cancellation-free certificate.
- **Phase-2 verdict:** **keeper.**

### lp-dual-gap-recovery
- **Family:** obstruction proof from the dual side.
- **What it does:** Settles "is this gap a true integrality gap or an undertrained
  ascent?" **without more iterations**: the LP's dual is combinatorial (a
  distribution over each target's partial hierarchies), so averaging the ascent's
  argmin hierarchies over its last quarter yields a *feasible dual* and hence an
  upper bound on the LP value.
- **Measured performance:** On `88@5fs`, `|counted| = 39` but the recovered dual
  evaluates to **34.0000** → **proven gap ≥ 5** → **no certificate of this family can
  push the chain above 83.000**, whatever the missing lemma says. Referee recomputed
  its own mixture dual in exact `Fraction` arithmetic: **exactly 34**. **Control
  fired:** the same instrument returns ~0 gap on four circuits and pins `88@7` at
  exactly 35.00 = `|counted|`.
- **Consequence (a correction to the whole program's standing plan):** the route
  needs **two** new tools, not one — the named span-cone-union lemma *and* an
  **integral** (non-LP) bound for the residual hierarchy-union problem.
  `PROGRAM_STATE.md` and lane C §5 both name only the first.
- **Code:** `fleet2/laneP_proof/code/lpgap.py`.
- **Phase-2 verdict:** **keeper — the highest-value negative in the slice.** It
  stops a pod-scale certificate campaign that could not have worked.

### candidate-lemma-falsification
- **Family:** cheap refutation.
- **What it does:** States the natural candidate lemmas and tests each against every
  wired circuit on disk. Seconds of compute.
- **Measured performance:** **Four dead on arrival**, each with an explicit witness:
  Y1 "every cancelling gate has an off-hierarchy operand" fails on 9 of 11 (this is
  the one most people would try first); Y2 `Y ≥ κ` fails on 4; Y4 fails on 9; Y5
  fails on 5. Y3 `Y ≥ κ − 5` survives 11/11 but yields a vacuous bound.
  **Each failure names the next candidate**: the surviving shape is a *counting*
  lemma over the union of cones, not a *charging* lemma over individual gates.
- **Code:** `fleet2/laneP_proof/code/ycand.py`; `results/ycand.json`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper — run this before any proof attempt.** Cost:
  seconds. Value: months.

### exhaustive-wiring-enumeration (rigidity)
- **Family:** exhaustive structural census.
- **What it does:** Enumerates the *entire* wiring space of a mask set and computes
  the exact minimum of a structural quantity over all valid wirings.
- **Measured performance:** Over 10 named circuits, the exact minimum equals the
  shipped value on **10/10**, from code sharing nothing with the lane's. **Four of the
  five record 88s have a UNIQUE valid wiring** (88@8 has 4; 92@4 has 64; 97@3 has 16).
  Census re-run over **3,254 known 88s**: minimum budget 78 against a requirement of 4,
  0 violations; **2,509 with a unique valid wiring, 745 with more than one.**
- **Code:** `fleet2/laneP_proof/verify1/rigidity.py`.
- **Phase-2 verdict:** **keeper.** Uniqueness of wiring is what makes per-circuit
  structural claims about a *mask set* legitimate.

### quotient-exact-form (Route 2)
- **Family:** structural theorem; strict strengthening of `quotient-counting-lemma`.
- **What it does:** Partitions the gates by their value under the projection:
  `N = #{v ∈ W⊗T} + #{distinct nonzero projections} + #{collisions} ≥ z_W + m_W + col_W`.
  Also proves there is **no composition theorem to find**: for `W1 ∩ W2 = 0` the pair
  map is injective on values, so the joint relaxation *is* the original problem.
- **Measured performance:** On lane B's own record-universal 22-gate R01 witness the
  exact form is worth **21 of 22** (at `W = span{d1}`) against lane B's transferred
  **14**. Control fired: `z_{qk2} = 4` independently reproduces lane B's own
  line-support profile "4 gates pure d1".
- **Actionable hand-off (never executed):** add `z_W + col_W ≤ k − m_W` for **every**
  kernel simultaneously to the fortified region CNF. At `k = 15` that forces
  `z+col ≤ 1` under qk4, `≤ 2` under qk2, `≤ 2` under qk6, `≤ 3` under qk7 *at the
  same time*, while the record spends 2, 8, 0, 2 there. Lane B's "tight mode" is the
  special case `z_W + col_W = 0` for one `W`. **Refereed — CONFIRMED.** See LEAD L4.
- **Code:** `fleet2/laneP_proof/code/` (snippet in `logs/`), `results/`.
- **Phase-2 verdict:** **keeper, and UNSPENT.**

### ambient-relaxation-single-solve
- **Family:** exhaustive decision by relaxation.
- **What it does:** Instead of sweeping committed sets, hands the block **the whole
  ambient value space free, simultaneously**, so one decision ranges over every set
  of every size at once. The honest cap is then on *gates*, not on `|Q|`.
- **Twist vs `g01-singleton-exhaustion`:** decides jointly-enabling sets, which the
  singleton sweep is structurally blind to.
- **Measured performance:** **`U1(Q1) ≥ 6` for every committed set of every size from
  the whole 255-value span — diagonal, skew, pure-hub, anything — and 6 is attained.**
  So lane G's 15-diagonal narrowing loses **nothing** at this cell: its ansatz becomes
  a **derivation**, and `= 5` is refuted. Also discharges flag F2 (the measured caps
  `|Q1| ≤ 5` etc.) for this question entirely. Correction banked with no compute: the
  bracket was already `[5,6]` before the lane ran anything, because lane G's exact
  `U1(15 diagonals) = 6` is an upper bound for the ambient instance (strict subset of
  inputs, identical targets).
- **Code:** `fleet3/laneCB_completeness/code/{cbtheory,decide}.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper — supersedes singleton sweeps outright.**

### greedy-schedule-lemma-enumeration (SAT-free exact engines)
- **Family:** exact combinatorial search without a solver.
- **What it does:** Proves that a valid program can always be reordered as "build
  every currently-buildable target, then introduce the next extra", so a `k`-gate
  program with `t` targets has exactly `k − t` extras and the search is over that many
  values. With 4 targets, deciding `k = 5` is a search over **one** value.
- **Measured performance:** Three independent engines, all exhaustive, all agreeing:
  `min_gates_naive` (0.16 s), `AmbientFast` (0.03 s / 20 s), and the **relaxed sweep**
  which iterates the *whole 4096-value 12-bit space* handing each value over free —
  proving the strictly stronger "there is no value at all, buildable or not" — in
  **0.39 s**. This is where a SAT solver had burned 4 h + 66 min + 240 s across three
  lanes and produced nothing.
- **Controls:** CTRL-A (reproduces two other lanes' oracle value 6), CTRL-B (UNSAT at
  5 as their solver logged), CTRL-C (empty supply UNSAT at 6), **CTRL-D planted
  positive, shape-matched** — the ambient instance plus one free value taken from the
  interior of a real 6-gate program returns **5** on both engines. The negative is not
  vacuous.
- **Code:** `fleet3/laneCB_completeness/code/{enum_exact,check_relaxed,decide}.py`.
- **Generality:** CIRCUIT-GENERIC for small-target-count blocks.
- **Phase-2 verdict:** **keeper — check whether the target count makes the problem
  SAT-free before reaching for a solver.** Speedup here was ~4 orders of magnitude.

### program-census (census6 / census7)
- **Family:** complete enumeration of optima.
- **What it does:** Enumerates **every** `k`-gate program of an instance, then for
  each surviving value set enumerates every build order and every operand choice and
  reads off which interface values it consumes.
- **Measured performance:** census6: 4.8 M states in 68 s → 4 distinct extra-pairs →
  **exactly TWO optimal committed sets**, both tap-diagonal bases of `vT`:
  `{4,6,a}` (= record 88@7's own set) and `{4,6,e}` (= lane G's derived set).
  *There are exactly two optima and the two lanes found one each* — which retires the
  referee's "witness luck" caveat in both directions and answers lane G's open
  necessity question: at the optimum, a `vT` basis is **necessary**, not merely
  sufficient, at this cell.
  census7: **21,872 seven-gate programs**, complete, banked — and it produced a real
  **negative about a cheap route**: the value union covers **243 of 243** admissible
  values, so the filter "`Q1 ⊆ U`" is vacuous.
- **Cost:** 68 s + 3 × ~1415 s.
- **Code:** `fleet3/laneCB_completeness/code/{census6,census7}.py`;
  `results/census7_sols_shard*.json` (3 files, 230 KB each).
- **Phase-2 verdict:** **keeper.** Enumerating *all* optima, not one, is what turned
  an ansatz into a derivation.

### minimal-set-extraction + monotone upstream sweep
- **Family:** complete case split via monotonicity.
- **What it does:** Inverts a badly-priced sweep. Rather than pricing 240 loose
  singletons (measured **>3100 s each** for the UNSAT half → ~150+ core-hours), it
  enumerates the *minimal* committed sets from the complete program census, then
  prices those — multi-element instances are far more constrained and decide in
  **24–147 s**. Monotonicity then lifts each decision to all supersets.
- **Measured performance:** `L` = **740 minimal committed sets** (92 of size 3, 648 of
  size 4). Swept to completion: **720 exhaustive UNSATs at cap 10 + 20 audited
  monotonicity prunes, 0 leads, 0 timeouts, 11.85 core-hours.** Together with the
  census this is a **complete case split on `U1(Q1)`** and yields the theorem below.
- **The theorem:** at the flagship cell, `core(Q1) = U07(Q1) + U1(Q1) ≥ 18` for
  **every** committed set — any subset of the 255-value span, any size, no cap,
  diagonal or skew — and 18 is attained. **The in-class 87 door at this cell is SHUT.**
  Non-trivially so: every single `vT` diagonal is upstream-**free** (`U07({w}) = 10`
  exactly), so the obstruction is joint and rank-driven and **no singleton filter
  could ever have found it**.
- **Controls:** CTRL-E (`U1({4,6,e})` = 6 SAT in 62.7 s on the same harness and cap
  where 28 rank-≤2 sets return exhaustive UNSAT); **CTRL-F planted positive**
  (three values from a real optimal 10-gate upstream program → 10 SAT, 18.0 s).
- **Code:** `fleet3/laneCB_completeness/code/{extract_L,sweepL}.py`;
  `results/L_minimal.json`, `results/branchL_shard*.jsonl` (4 × 185 rows).
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper — the single best "how to price an interface" recipe
  in the slice**, and the lesson generalises: *on these instances more targets is
  cheaper; always push constraints into the instance rather than sweeping loose ones.*

### audit-from-banked-artifacts
- **Family:** referee-facing self-audit, **with a demonstrated limitation**.
- **What it does:** Re-checks a theorem from the banked artefacts only — that the
  decided rows are exactly the claimed set with no duplicates or extras, that every
  row is a capped UNSAT or a well-founded prune, that all 720 solver logs
  independently report `exhaustive: true`, that all 720 instances rebuild
  byte-exactly, and that the named controls fired.
- **Measured performance:** PASSES every check. **But the referee's finding F-6:
  passing is a *consistency* check, not tamper-evidence — it can be defeated by a
  forged log+instance pair.** The referee built two sandboxes to demonstrate this
  (`referee/sandbox/X1_forged_log`, `X2_bogus_prune`) and then re-executed the oracle
  itself rather than trusting the audit.
- **Code:** `fleet3/laneCB_completeness/code/audit_door.py`; sandboxes 536 KB.
- **Phase-2 verdict:** **keeper, with the caveat shipped alongside it.** The
  forgery-sandbox technique — attack your own audit script and keep the attack — is
  itself worth copying.

### stratified-attribution
- **Family:** structural analysis of a price gap.
- **What it does:** Takes a modelled price that is loose by `n` gates and re-stratifies
  both sides by *exact* line support until the gap localises to one stratum. Per-gate
  assertion that each gate's value is the XOR of its operands' values in line
  coordinates, so the coordinate dictionary is checked gate by gate.
- **Measured performance:** **Corrected the referee's own diagnosis.** The referee had
  localised "the bulk" of lane G's 3-gate R34 gap to the F4 *line* restriction.
  Re-stratified: `COL3 0 / Q27 +3 / D37 +1 / W3 0 / U4 −1` — **all of it sits at the
  tap-3 interface.** And the line restriction is *empirically free*: across all 14
  known 88s, **0 of 107 `U4` gates carry line 2 in their value AND 0 carry it in an
  operand**. What lane G's model actually deleted was the **export edge** `D37 → W3`:
  of the 52 `{3,7}`-stratum gates across the 14 records, **46 feed the sector-3 work
  and 27 are consumed by BOTH blocks; 14/14 circuits have ≥ 1 dual-role gate.**
  Control: `code/blocks.py` re-implements the block classification from scratch and
  reproduces lane A's per-block sizes on **22/22 circuits exactly**.
- **Code:** `fleet3/laneF4_rule/code/{blocks,r34anat,strata,attrib,walk88at7}.py`.
- **Generality:** MC-HARDCODED in the strata, CIRCUIT-GENERIC in method.
- **Phase-2 verdict:** **keeper — this is how you find out *where* a model is wrong.**

### defect-calculus-rule-derivation
- **Family:** hand-derivation + exhaustive machine checking.
- **What it does:** Defines a per-sector "defect" `Δ_k = t_{k−1} + t_7` (zero exactly
  on sector-k values), tabulates how each elementary move changes `(p_k, Δ_k)` and who
  else can use it, and reads off the rule. Every identity is then machine-checked
  exhaustively over `T × T`.
- **The rule (RULE F4):** a tap's interface plane pays for itself **exactly when the
  tap sits immediately above another tap (or above the root)**. From the reduction
  polynomial alone: AES taps `{1,3,4}`; `1−1 = 0` (root) → shared; `4−1 = 3 ∈ TAPS` →
  shared; `3−1 = 2 ∉ TAPS` → **unshared**. So this field has exactly ONE unshared tap
  interface, at tap 3 — **which is precisely where all 3 gates of the gap sit and
  precisely where every record keeps the interface rank at ≤ 1.** That is content
  beyond the fit: it names, from the polynomial, which interface must not be greedily
  filled.
- **Measured performance:** identities I1–I5 all PROVED exhaustively (256/256,
  240/240). Prescription measured against all 14 records: tap 1 rank ≥ 2 always;
  tap 4 rank ≥ 2 in 13/14; **tap 3 rank ≤ 1 in 14/14**, and **every one of the 14
  records' `D27` values is a one-gate value.**
- **Code:** `fleet3/laneF4_rule/code/{rule,prescribe,planeenum}.py`.
- **Generality:** **CIRCUIT-GENERIC over any field with a reduction polynomial** —
  the rule is stated in terms of `τ_k`, so it transfers to `aes_inv_mixcolumns` and
  to other MDS matrices directly. **This is the most transferable *idea* in the slice.**
- **Phase-2 verdict:** **keeper — the one modelling rule that closed 91 → 88.**
  Under lane G's F4-restricted model the same cell prices 91; with the rule it prices
  88 and **builds a VALID 88-gate circuit** (`results/gen_f4_88_D4.json`, sha256
  `5e81e854…`, re-verified by me today: `gates=88 depth=10 32/32 VALID`).

### replay-bound
- **Family:** free lower bound by program replay.
- **What it does:** If a producer block's inputs are all available to its consumer,
  the consumer can simply replay the producer's whole program verbatim. Hence
  `B37 + U4(D37) ≥ U4(no D37)` for **any** commitment whatsoever — costing one solve
  of the consumer *with no supply at all*.
- **Measured performance:** `U4(no D37)` = **11 EXACT** (k=6..10 exhaustively UNSAT,
  k=11 SAT; 17,199 s), independently re-solved by the referee on a differently packed
  instance at 23,673 s. Consequences: (1) the measured "conservation law"
  `B37 + U4 = 11` becomes a **proven, tight floor** — every configuration measured
  sits exactly on it, so **no re-choice of the tap-4 interface can ever gain a gate**;
  (2) with `W3 ≥ 8` family-wide, `B ≥ 12 + W3 ≥ 20` — **no 87 at the 88@7 cell** in
  the derived family; (3) it **resolved a lane-G-referee UNDECIDED**: the merged
  `U347` was bracketed `{10,11}` and reported as "the split costs at most 1"; the
  answer is 11, so **the split costs exactly 0**.
  The referee then walked `W3 ≥ 8` from the lane's 24-value family out to the
  **complete 64-value one-gate family** (48-value solve: `k=7` UNSAT 3944 s,
  `k=8` SAT), strengthening the lane's own bound.
- **Code:** `fleet3/laneF4_rule/code/f4model.py` (the `no-supply` instances).
- **Generality:** **CIRCUIT-GENERIC** wherever a block model has nested input sets.
- **Phase-2 verdict:** **keeper — a lower bound for the price of one solve.**

### stepping-stone-non-interchangeability (Test G)
- **Family:** falsification of a derivation rule; twist on `free-supply-derivation`.
- **What it does:** When a derived family has few members, prices *each* member rather
  than assuming the choice is immaterial.
- **Measured performance:** The derived family of one-gate stepping stones has
  **exactly two** members; record 88@7 uses `u(5,4)` and record 88@8 uses `u(1,4)`, so
  the lane predicted the choice was immaterial and priced the other to prove it.
  **MISS:** `W3` = 8 with `u(5,4)`, **9** with `u(1,4)`. Assembling the alternative
  end to end emits a **VALID 89** — reported as the 89 it is, not the 88 it was aimed
  at. **So "pick any member of the derived family" is REFUTED as a derivation rule;
  the family-wide free-supply solve is not** (Test F reached `u(5,4)` with no record
  input). *That distinction is the difference between a derivation and a fit.*
- **Phase-2 verdict:** **keeper — this is the methodological lesson of wave 3.**

### prediction-scoring
- **Family:** methodology.
- **What it does:** Writes every prediction to the ledger with
  `kind=prediction` **before** the corresponding solve, then scores strictly from the
  ledger, not from prose.
- **Measured performance:** Lane F4: **15 of 18 met**; all three misses (Tests B, D, G)
  turned into structure rather than being explained away. Lane DEPTH: **MET 3 ·
  MISS 7 · SPLIT 2 · UNDECIDED 2** over 14 predictions — and its RESULT.md records
  that an earlier draft said "MET 4", *"the ledger says 3, and the ledger wins"*.
  The misses are where the findings came from: P1's falsifier identified the depth
  cause, P11/P12 exposed the interface-level law, P14 turned the depth-4 rung from a
  guess into a single decidable question.
- **Phase-2 verdict:** **keeper — adopt as standing practice.** A 7-miss lane
  produced more than a 15-hit lane precisely because the misses were logged.

### depth-capped-exact-SLP-oracle (dslp)
- **Family:** SAT-based exact decision; a genuinely new instrument.
- **What it does:** Decides *min gates subject to a depth cap*, with **levelled
  inputs** (a block's inputs are not free — currency arrives at level 1/2/3, an
  interface value arrives wherever its producer put it) and **per-target caps** (one
  block must deliver its own targets by level `D` but its exported interface several
  levels earlier). Order-encoded level variables `a[i][l]` = "level(gate i) ≤ l" plus
  `z → level(i) ≥ level(operand)+1`; each normalisation rule argued depth-safe in the
  docstring. An exact reachability precheck over the whole `2^r` value space reports
  `infeasible_depth` rather than letting a solver grind.
- **Twist:** the base CNF is **re-implemented rather than imported**, so "cap off
  reproduces `slp_opt`" is a two-implementation control and not a tautology.
- **Measured performance / controls, all three fired:** (A) cap-off vs `slp_opt`
  **10/10** on real block instances, plus at full scale (`U07` uncapped = 12, `W3`
  uncapped = 8, reproducing lane F4); (B) exhaustive brute force **40/40** uniform
  caps and **60/60** per-target caps against a BFS enumeration sharing no code with
  the SAT path — and it certifies every UNSAT level, not just the value;
  (C) planted positive found at 5 gates and replaying at depth 3, with the same
  targets at cap 2 correctly `infeasible_depth`.
- **Cost:** **91 exact depth-capped block decisions, 5 timeouts, 13,215 s** of solver
  wall at `--cores 6`, plus 80 exhaustive currency curves with no solver at all.
- **Code:** `fleet4/laneDEPTH/code/{dslp,selftest_dslp,model,genD}.py`;
  `results/dcache.jsonl` (97 rows), ledger 267 rows.
- **Generality:** **CIRCUIT-GENERIC.** The instrument itself knows nothing about
  MixColumns.
- **Phase-2 verdict:** **keeper — the most reusable new tool of wave 4**, and the
  only oracle in the repo that can price depth.

### level-BFS-depth-diagnosis
- **Family:** structural analysis (no solver).
- **What it does:** Level-BFS gives the provable minimum level of every mask; each
  mask is attributed to a block by the line support of its value, so the critical path
  is annotated block by block.
- **Measured performance:** **Every critical path crosses at most three block tags and
  is dominated by ONE block's internal span.** The theory-generated 88 burns levels
  2..8 on a nine-mask `U07`; `88@7` has `U3` spanning six; shallow circuits have no
  block spanning more than four. **Diagnosis: the depth is burnt inside block
  programs**, because `slp_opt` minimises gates and depth never enters its objective.
  Assembly order is worth **exactly zero** — for all 12 circuits measured, as-written
  depth equals the level-BFS minimum of the same mask set (a second, independent
  confirmation of `e4_depth`'s 2-hits-in-38,711).
- **Code:** `fleet4/laneDEPTH/code/diag.py`; `results/diag_circuits.json`.
- **Phase-2 verdict:** **keeper.** Cheap, solver-free, and it aimed the whole lane.

### exhaustive-currency-curve
- **Family:** complete enumeration, no solver.
- **What it does:** Breadth-first enumeration over `T` for a line's menu, giving the
  exact gates-vs-depth curve — so `None` means **provably impossible**, not "not found".
- **Measured performance:** Over all 19 cells on record, **every cell's whole currency
  is buildable at depth 2 for 0–2 gates over the gate-minimum, and depth 1 is
  infeasible at every cell.** At the 88@7 cell: 22 gates at depth ≥ 3, 23 at depth 2 —
  forcing all currency to level ≤ 2 costs exactly one gate. So supply chains are
  nearly free and were never the depth problem.
- **Code:** `fleet4/laneDEPTH/code/currency.py`.
- **Phase-2 verdict:** **keeper.**

### interface-level-curve
- **Family:** parametric exact sweep; the sharpest finding of wave 4.
- **What it does:** Separates two effects everything else conflates — sweeps the
  *arrival level of the committed interface value* independently of the total depth cap,
  for producer and consumer separately, and finds where the two curves cross.
- **Measured performance:** **`U07`'s price is a function of the INTERFACE cap alone;
  the total depth cap does not enter it.** `Q1` at level 2 → 14 gates, level 3 → 13,
  level ≥ 4 → 12 — and **13 is 13 at `D=5`, `D=6` and `D=7` alike.** The consumer runs
  the other way: `U1 = 6` with `Q1` at level ≤ 3, `≥ 9` at level 4. So the R01 depth-5
  optimum is `l1=3: 13+6 = 19` against `18` uncapped — **the whole depth-5 premium of
  the region is +1 gate and it sits entirely at the tap-1 interface level.** This is
  the depth-axis analogue of lane F4's gate-axis conservation law.
- **Consequence:** *depth is substantially a property of the CELL.* The identical
  model, code and depth cap give **88 at the 88@5 cell and 90 at the 88@7 cell** —
  the sharpest available statement of why the five known 88s sit at five different
  depths.
- **Code:** `fleet4/laneDEPTH/code/curves.py`, `frontier.py`.
- **Phase-2 verdict:** **keeper, and UNFINISHED** — the lane's own #2 next step
  ("run the interface-level curve at every tap, at both cells") is a 3-parameter
  search with minute-scale solves and was never run. See LEAD L7.

### positive-only-probe
- **Family:** honest-negative discipline.
- **What it does:** A probe whose miss carries **no** negative information, logged as
  such so nobody later reads it as a refutation.
- **Measured performance:** `repair.py` on the cached 10-gate depth-5 `W3` witness:
  three of its four targets sit at level 5 and no single added mask (of the 227
  level-feasible over the whole `2^12` span) brings all three down to 4. Logged
  `kind=repair, found=false, note="positive-only probe; a miss carries no negative
  information"`. It legitimately **shifts a prior** without becoming evidence.
- **Phase-2 verdict:** **keeper — the cleanest example of the discipline in the slice.**

---

## 3. ARTIFACTS (counts + labels)

### 3.1 Verified full MixColumns circuits produced or held in the slice

Command (histogram over every JSON in the slice with a `gates` list > 60 long):

```
python3 - <<'EOF'
import json,os,collections
c=collections.Counter()
for root in ['fleet1','fleet2','fleet3','fleet4']:
  for dp,dn,fn in os.walk(root):
    for f in fn:
      if not f.endswith('.json'): continue
      p=os.path.join(dp,f)
      try:
        if os.path.getsize(p)>400000: continue
        d=json.load(open(p))
      except Exception: continue
      if isinstance(d,dict) and isinstance(d.get('gates'),list) and len(d['gates'])>60:
        c[len(d['gates'])]+=1
print(sorted(c.items()))
EOF
```

Result: **660 circuit-shaped JSONs**, histogram
`88:24, 89:3, 90:1, 91:6, 92:3, 94:2, 95:1, 97:1, 98:1, 99:1, 103:1, 104:3, 105:10,
106:8, 107:23, 108:36, …, 128:1`. Broken down honestly:

| label | count | where | note |
|---|---|---|---|
| **NEW circuits emitted in-slice, oracle-VALID** | **6** | see below | I re-verified 5 of them today with `python3 verify_circuit.py <file>` — all VALID |
| — `NEW88_from_88at6_hit3_depth9.json` | 1 | `fleet1/laneD_completions/` | **88 gates, depth 9.** A lateral edit-distance-3 move off 88@6, double-verified in-lane; **shares 85 of 88 masks with 88@6 and was never checked against the 139,878-circuit census** |
| — `gen_f4_88_D4.json` | 1 | `fleet3/laneF4_rule/results/` | **88 gates, depth 10**, sha256 `5e81e854…`, built from theory with no search over circuits; model price 88 == emitted 88 (no dedup leak) |
| — `gen_f4_88_D4alt.json` | 1 | `fleet3/laneF4_rule/results/` | 89 gates — the neighbouring configuration, reported as what it is |
| — `genD_88at5_record_D5_c3_322.json` | 1 | `fleet4/laneDEPTH/results/` | **88 gates @ depth 5, depth-TIGHT** (same file at depth 4 → INVALID, rc=1). **Jaccard 1.000 to record 88@5 — a re-derivation, stated against itself by the lane** |
| — `genD_88at7_D5_c3_323.json` | 1 | `fleet4/laneDEPTH/results/` | 90 gates @ depth 5 |
| — lane G generator emissions | 7 | `fleet2/laneG_generator/results/` | 116@3, 91@5, 92@4, 94@5, and 95/99/103 where the model price was an upper bound |
| **Referee re-emissions (independent verification copies)** | 6 | `fleet2/laneG_generator/referee/results/` (5, incl. `ref_91g_d4.json` = a **91 @ depth 4**), `fleet3/laneF4_rule/referee/prov/results/` (1) | not new circuits; independent re-runs |
| **Decompositions of known circuits (analysis, not new circuits)** | 22 | `fleet1/laneA_v2pricing/results/decomp_*.json` | 14×88, 89@5, 89@10, 91@6, 92@4, 97@3, 98@3, 2×compiled-91 |
| **Backward-search outputs** | 601 + 4 | `fleet1/laneD_completions/bwd_out/` (2.4 MB), `bwd_best/` | 6 are planted-88 controls (`c1_*`, all oracle-VALID at F=88, 0 stranded); the rest are 104–128-gate frontier runs. Best 4 preserved: **104/105/105/106**, each independently oracle-VALID |
| **Lateral 88s found but never compiled** | **99** | `basin_88at5fs.jsonl` (42), `basin_88at6.jsonl` (57) | recorded as `{triple deleted+forbidden, 3 gates paid}` only — **see LEAD L2** |

### 3.2 Certificates and machine-checked bounds

| label | what it certifies | count | path / command |
|---|---|---|---|
| **DOOR-SHUT sweep** | `U07(M) ≥ 11` for every minimal committed set with `U1 ≤ 7`, hence `core(Q1) ≥ 18` for *every* `Q1` at the flagship cell | **740 decided** (720 exhaustive capped UNSAT + 20 audited monotonicity prunes), 0 timeouts, 11.85 core-h | `fleet3/laneCB_completeness/results/branchL_shard*.jsonl` — `wc -l` = 185 each |
| **complete 7-gate program census** | every 7-gate ambient program (basis of the case split) | **21,872** | `results/census7_sols_shard*.json` (3 files) |
| **complete 6-gate census** | exactly 2 optimal committed sets exist | 4 extra-pairs → 2 sets | `results/` + `code/census6.py` |
| **singleton exhaustion** | every single committed value is individually useless at the flagship cell | **240/240** exact capped UNSAT | `fleet1/laneA_v2pricing/ledger.jsonl`, `kind=g01_single` (504 rows, 480 `useless`) |
| **module table** | `σ = 7` or `σ ≥ 8` for each canonical sector class | **1383** (92 YES / 1291 exhaustive capped UNSAT), 0 timeouts | `fleet2/laneG_generator/results/modules.jsonl` (1,409 rows) |
| **quotient exact-search cubes** | per-level UNSAT at full cube coverage | k=12/13/14 at **1008/1008 cubes each**; 7 R01 quotients + 65 R34 instances | `fleet1/laneB_regionbounds/cubes/*.jsonl` (516 KB) |
| **`minE` exhaustions → `L2 ≥ 22`** | depth-5 exhaustion, three times, one of them pruning-free | 294,188,302 / **80,092,627,410** / 1,795,955,245 nodes | `fleet1/laneC_proofside/runs/l2_k5*.out`, `ledger.jsonl` |
| **integer residual certificates** | `n ≥ 88` for `88@7` and `88@5` given their apparatus, solver-free | 3 (`88@5`, `88@7`, `89@5`) | `fleet2/laneP_proof/results/exact_*.json`, re-checkable by `code/verify_exact.py` |
| **LP dual certificate** | integrality gap ≥ 5 on `88@5fs` ⇒ route ceiling **83.000** | 1 (+ 4 ~0-gap controls) | `fleet2/laneP_proof/results/lpgap.json` |
| **depth-capped block decisions** | exact min gates under a depth cap | **91 exact + 5 timeouts**, 13,215 s | `fleet4/laneDEPTH/results/dcache.jsonl` (97 rows) |
| **exhaustive currency curves** | gates-vs-depth per menu, solver-free (`None` = provably impossible) | **80** over 19 cells | `fleet4/laneDEPTH/code/currency.py` |
| **F4 oracle decisions** | block minima at the 88@7 cell | 24 exact + 1 timeout (now 25 exact, LEAD L3), 32 invocations, 46,675 s | `fleet3/laneF4_rule/results/cache.jsonl`, `ledger.jsonl` (66 rows) |

### 3.3 Writeups and ledgers

```
find fleet1 fleet2 fleet3 fleet4 -name '*.md' | wc -l   ->  18
```
9 `RESULT.md` (one per lane), 4 `REFEREE.md`, 1 `WALKTHROUGH.md`, 1
`RECORDS_UPDATE_NOTE.md`, 2 lane-G `notes/` digests, 1 `cubes/README.md`
(a document explaining why a directory is deliberately **empty** — worth
copying as a practice).

Ledger rows (`wc -l` on each):
`basin_88at6` 27,720 · `basin_88at5fs` 27,720 · `laneP/verify1` 8,074 ·
`laneP referee snapshot` 8,057 (sha256 `497b8da7…` final / `bc77f0fd…` frozen) ·
`laneP referee b9_census` 3,255 · `laneG modules` 1,409 · `laneCB u07_cache` 788 ·
`laneA` 667 · `laneD` 442 · `laneA solve_cache` 359 · `laneDEPTH` 267 ·
`laneD rerank0` 141 · `laneC validation` 120 · `laneCB` 107 · `laneDEPTH dcache` 97 ·
`laneB` 87 · `laneD bwd9` 81 · `laneP` 79 · `laneF4` 66.

### 3.4 Raw logs and instances (the deletion surface)

```
for L in <lanes>; do echo "$L inst=$(find $L -path '*/inst/*' -type f|wc -l) logs=$(find $L -path '*/logs/*' -type f|wc -l)"; done
```
laneG 1453 inst / 1470 logs (11.3 MB) · laneCB 795 / 864 (6.6 MB) ·
laneA 358 / 379 (3.0 MB) · laneB 82 / 14 · laneF4 38 / 43 · laneDEPTH 0 / 5.
19 `__pycache__` directories, 808 KB total.

---

## 4. KEEP / DELETE proposal

**Net proposal: delete ~0.8 MB with certainty, and ~5 MB more only if disk is
actually tight. This slice is 45 MB and is the most valuable documentation in the
tree; I recommend keeping essentially all of it.**

| item | verdict | why | size |
|---|---|---|---|
| All 18 `.md` files | **KEEP — highest value in the slice** | goals 2–4 material; `WALKTHROUGH.md` is the public-page template (§5, LEAD L10) | ~350 KB |
| All `ledger*.jsonl`, `*cache.jsonl`, `cubes/*.jsonl`, `branchL_shard*.jsonl` | **KEEP** | append-only ledgers are the *only* authority for every number in every RESULT.md; `tally.py` in each lane reads them | ~6 MB |
| All `code/` | **KEEP** | this is the phase-2 toolkit | ~1.3 MB |
| `fleet1/laneA_v2pricing/results/configs.json` | **KEEP — LOAD-BEARING, DO NOT MOVE** | read at import by fleet5, fleet8, fleet9, fleet12 (see HAZARDS) | 40 KB |
| Emitted circuits (`gen_*.json`, `genD_*.json`, `NEW88_*.json`, `bwd_best/`) | **KEEP** | verified artefacts; 5 re-verified today | ~200 KB |
| `basin_88at5fs.jsonl` / `basin_88at6.jsonl` | **KEEP** | 55,440 completed decisions and the 99 unexamined HIT-3 rows (LEAD L2); this is unique data | 5.8 MB |
| `fleet2/laneP_proof/verify1/ledger.jsonl` (8,074) **and** `referee/results/verify1_ledger_snapshot_20260820.jsonl` (8,057) | **KEEP BOTH** | the snapshot is the *refereed reference* (frozen because the live file was moving); deleting either breaks a citation | 3.7 MB |
| `fleet2/laneP_proof/ledger.jsonl.prev` | **DELETE-CANDIDATE** | superseded copy of a 79-row ledger that `code/mkledger.py` regenerates | 24 KB |
| 19 `__pycache__` directories | **DELETE-CANDIDATE** | regenerable bytecode | **808 KB** |
| `fleet1/laneC_proofside/_tmp_inst.txt` | **DELETE-CANDIDATE** | named `_tmp`; `l2_inst.txt` is the kept copy | small |
| `fleet2/laneG_generator/{inst,logs}` (1453 + 1470 files) | **KEEP + note** | regenerable *in principle* (each is `sweep.py`'s instance + solver transcript, ~50 min to rebuild the table) — but `RESULT.md` §8 cites them as "every instance and solver log referenced above" and the referee audited against them. **If disk is needed, this is the first place to go**: `tar.zst` the pair to a few hundred KB rather than deleting | 11.3 MB |
| `fleet3/laneCB_completeness/{inst,logs}` (795 + 864) | **KEEP + note** | same argument, and stronger: `audit_door.py` re-reads **all 720 solver logs** and rebuilds all 720 instances byte-exactly. **Deleting these destroys the audit trail of the DOOR-SHUT theorem.** Archive, never delete | 6.6 MB |
| `fleet1/laneA_v2pricing/{inst,logs}` | **KEEP + note** | `solve_cache.jsonl` references each by name; one log is famously **0 bytes** (the `SLPV` hazard) and is itself evidence | 3.0 MB |
| `fleet3/laneCB_completeness/referee/sandbox/X1_forged_log`, `X2_bogus_prune` | **KEEP — but LABEL LOUDLY** | these contain **deliberately forged solver logs and a deliberately bogus prune**, built by the referee to prove `audit_door.py` is not tamper-evident. They are valuable methodology and dangerous data. A `README` at the sandbox root saying "SYNTHETIC / FORGED — never cite" is the one edit I would ask for | 536 KB |
| `fleet1/laneD_completions/bwd_out/` (601 files) | **KEEP for now** | the 400-run frontier is a measurement (best 104); the per-run circuits are 104–128 gates and of no record value, but re-running costs ~400 runs × ~5 s plus the 100+64 control arms. Low priority DELETE-CANDIDATE at 2.4 MB | 2.4 MB |
| `fleet2/laneG_generator/notes/{lanes_bcd.md, v2_spec.md}` | **KEEP** | 94 KB of subagent digests that are the readable spec of the V2 model — good public-page raw material |  |

Anything not listed: **KEEP**.

---

## 5. LEADS (sharp-eye findings)

### L1 — `R01 ≥ 15` was PROVEN by the quotient route after lane B closed, and `k=15` was one cube in — **VERIFIED-IN-LOG**
Lane B's `RESULT.md` reports `qk4 ≥ 14` with "k=14 in flight" and prices k=14 at
"~200–450 ks local CPU → R01 floor ties 15". **It landed.**
```
ledger.jsonl: {"tag":"R01_qk4_s2","k":14,"status":"UNSAT",
               "stats":{"cubes":1008,"ran":1008,"wall":101990.2,"cpu_secs":484560.6}}
cubes/R01_qk4_s2_k14.jsonl -> 1008 rows, all UNSAT
```
So `m_qk4 ≥ 15` and the quotient ladder independently certifies **R01 ≥ 15** — the
pod floor, reproduced by a completely different method at a fraction of the direct
cost. **And `cubes/R01_qk4_s2_k15.jsonl` contains exactly one row** (`cube 0:0, UNSAT,
0.09 s`) — the k=15 level, whose completion would give **R01 ≥ 16, the first floor
past the pods**, started and was abandoned 1/1008 of the way in. Lane B priced it at
~2–9 Ms local CPU / **1–4 pod-days**. This is a fully specified, resumable,
already-launched job whose result is a new lower bound. Nobody collected it and no
later wave mentions it.
*Also uncollected:* `R34_qk1_8_9` k=14 finished UNSAT (28/28 cubes, 13,118 CPU-s),
verdict `bracket, lower_bound_proven: 15, ub 18`.

### L2 — the basin sweeps finished and found **99 lateral 88s**, not 1 — **VERIFIED-IN-LOG**
Lane D's `RESULT.md` reports the sweeps as "RESTARTED, PRODUCING, RUNNING" with
`{88@5fs: 4,944 banked, 0 escapes}` and `{88@6: 4,480 banked, 1 HIT-3}`, and draws the
conclusion *"edit-closure rigidity is basin-dependent, since 88@5's basin gave 0
escapes in >10,000 triples"* and *"88@5fs 4,944 so far, 0"*. Both sweeps then ran to
completion:
```
wc -l basin_88at5fs.jsonl basin_88at6.jsonl   -> 27720  27720
verdict tally: 88@5fs {none: 27678, HIT-3: 42}    88@6 {none: 27663, HIT-3: 57}
```
**42 escapes in the 88@5fs basin, 57 in 88@6 — 99 in total, against the 1 the
write-up knows about.** Consequences nobody has drawn:
1. The lane's headline ("rigidity is basin-dependent; 88@5fs gave 0") is **wrong as
   stated** — 88@5fs is not rigid either. The true statement is that 88@5's basin is
   the anomalous one (0 escapes in 10,266 triples) and the other two are not.
2. **99 distinct oracle-VALID-shaped 88-gate mask sets exist as data and have never
   been compiled, verified, deduplicated, or checked against the 139,878-circuit 88
   census.** Each row is `{triple deleted+forbidden, 3 gates paid}` and the one that
   *was* compiled verified VALID first time (I re-verified it today).
3. **Zero completions at `k ≤ 2` across all 55,440 triples** — that is a much
   stronger no-87 statement than the write-up claims, and it is free.
This is the largest block of generated-but-unexamined data in the slice.

### L3 — lane F4's `W3_noshare` landed at **11 EXACT**, and it changes the lane's own attribution — **VERIFIED-IN-LOG**
`RESULT.md` §3.2 leaves `W3_noshare(Q27={δ₃(c)})` as `≥ 10 PROVEN; exact value
UNDECIDED` and decomposes the 3-gate gap as *"the rank cut alone buys ≤ 1, the edge
buys the other ≥ 2 — both ingredients are needed; neither alone accounts for 3."*
The re-queued solve finished:
```
results/cache.jsonl  name=bW3_noshare_2dd8cbb10c3d  status=exact  min_gates=11  wall=33876.6  verified=true
ledger.jsonl  kind=task tag=W3noshare_Q27c_exact  status=exact  min_gates=11
```
With `W3_noshare = 11` the four measured points become
`(rank3, no share) = 4+8 = 12`, `(rank1, no share) = 1+11 = 12`,
`(rank1, share) = 1+8 = 9`, `(rank0, share) = 0+10 = 10`.
**The rank cut alone buys ZERO and the sharing edge buys all 3.** The lane's
"both ingredients are needed" is refuted by the lane's own late solve. (The lane F4
referee spotted exactly this and lists it as refutation (ii) in its BOTTOM LINE — but
`RESULT.md` was never corrected, so the two documents now disagree.)
**Independent confirmation of the same thing, also uncollected:** lane G's §7b
in-flight solve (`U3` with tier-1 rank-2 supply) finished at **10 exact**, not the
hoped-for 9 (`logs/free_U3_tier1_t1_09d4d5136dea.out`: k=9 UNSAT 3552 s, k=10 SAT).
So `(U27,U3)` stays at `2+10 = 12` — **the tap-3 rank reduction buys nothing on
either side of the model.** Lane G's §4.4(b) "moves from 12 towards 11" is measured
to move nowhere. **Two lanes independently measured the same fact and neither
RESULT.md says it.**

### L4 — lane P handed lane B a strictly stronger tool and it was never used — **VERIFIED-IN-LOG**
Lane P §4.3 proves `N ≥ m_W + z_W + col_W` and measures it on lane B's own 22-gate
R01 witness: **21 of 22** at `W = span{d1}`, against the 14 lane B was transferring.
It states the actionable form — add `z_W + col_W ≤ k − m_W` for **every kernel
simultaneously** to the fortified CNF, which at `k=15` forces `z+col ≤ 1, ≤2, ≤2, ≤3`
under qk4/qk2/qk6/qk7 at once while the record spends 2, 8, 0, 2 — and says *"Lane B
can add them in an afternoon"*. Lane B had already finalized (2026-08-20; lane P
reported 2026-08-20 too). **`grep -c fortify fleet1/laneB_regionbounds/ledger.jsonl`
shows the fortify arm stopped at k=13.** This is the one mechanism in the projection
family that lane P believes can push R01 past 15, it is proved, it is cheap, and it
was never run. **PLAUSIBLE — high value.**

### L5 — a possible **90 @ depth 4** hangs on one undecided SAT call — **VERIFIED-IN-LOG**
Lane DEPTH §3.2/§3.3 prices the depth-4 rung at the 88@5 cell as
`79 + W3(D=4) ≥ 90`, exactly 90 iff `W3(D=4) ≤ 11`, and notes that **the repo's best
verified depth-4 circuit is 91** — so a SAT answer is a new repo frontier point. It
says "collect from `logs/queue4.out` / `results/dcache.jsonl` (tag
`DECIDE_W3_D4_le11`, take the LAST row)". Collected:
```
tag=DECIDE_W3_D4_le11     status=timeout  lower_bound_proven=null  wall=36014.75
tag=DECIDE_W3_D4_le11_c2  status=timeout  lower_bound_proven=11    wall=36093.89
    log: k=6 UNSAT 39.7s, k=7 66.3s, k=8 250.8s, k=9 1243.3s, k=10 7973.7s
```
**Both timed out at 10 h.** So the honest state is unchanged — `W3(D=4) ≥ 11`
machine-checked, rung `≥ 90`, endpoint **UNDECIDED, never a refutation** — but the
question is *exactly one capped SAT call* (`max_gates=11`, so UNSAT would be a
machine-checked negative and not a timeout), and the payoff is a repo frontier move.
The lane's own positive-only repair probe shifts the prior toward 12 (three targets
each needing to lose a level), which would leave the frontier at 91. Note also the
two runs differ in one input level (index 6: 3 vs 2), so `_c2` is a variant, not a
retry. **This is the single most decision-relevant unfinished computation in the slice.**

### L6 — the `SLPV` empty-log hazard destroyed a 4-hour solve and is a repo-wide trap — **VERIFIED-IN-LOG**
`atlas/slp_opt.py` emits nothing under redirection without `-v`, so long solves must
run with `SLPV=1` or their completed levels are lost. Lane A's `g01_fullspan` row is
`status=crash_or_timeout, lower_bound_proven=null, wall=14520` with a **0-byte solver
log** — 4 hours that banked *no* lower bound. Lane CB found it, named it, and lane A
recorded it as a "known repo hazard, re-hit from a new direction". **SMELL:** nothing
in the slice suggests a repo-wide fix landed; any phase-2 campaign should make
`SLPV=1` (or `-v`) non-optional in the driver.

### L7 — the cheapest unexplored axis in the whole slice is named and unrun — **PLAUSIBLE**
Lane DEPTH's own next-steps #2 and #3: (a) run the interface-level curve at *every*
tap at *both* cells — "the whole depth premium is one number per interface, the level
at which the producer's and consumer's curves cross", a 3-parameter search with
minute-scale solves; (b) **sweep the CELL against depth** — "the same model gives
88@5 at one cell and 90@5 at another … ten cells at ~1 h each would answer *which
cells support 88@5?* — and that question has never been asked in this repo." The 19
cells' currency curves are already computed and free. Lane F4's next-steps #3 and #4
point at the same gap from the gate axis ("sweep `C_3` alone — the cheapest genuinely
new axis in the whole configuration space, and it is how 88@5fs buys `B = 19`";
"re-run the stratified attribution at the other five R34 cells"). **Every lane-level
theorem in waves 3–4 is cell-conditional at one cell (88@7 or 88@5), and the other
cells were never touched.**

### L8 — evidence about **why 88 keeps appearing** (structure shared by all 88s) — **VERIFIED-IN-LOG**
Collected from across the slice, this is the strongest body of "why 88" evidence I
found, and it has never been assembled in one place:
- **Two conservation laws, both proved tight.** *Gate axis* (lane F4): on the shared
  tap-4 plane, `B37 + U4 = 11` invariant over every configuration measured — the gate
  you save minting a `vT` dimension as a skew value is exactly the gate you pay
  de-skewing it downstream — and the replay bound `U4(no D37) = 11` proves this is a
  **floor** that every measured configuration sits exactly on. *Depth axis* (lane
  DEPTH): a gate saved upstream by letting the interface sink one level is more than
  paid back downstream; the whole depth-5 premium of R01 is +1 gate.
- **Flat basins that are cell-conditional, not global.** In-cell R01 core values are
  *exactly* constant across records (18,18,18,19,19,19); R34 cores take only 22 and 23.
- **All-tight everywhere.** ~50 exact block decisions in lane A, 18 heavy joint probes,
  **zero sub-witness blocks in the entire campaign.**
- **The 22 is record-universal**: 12 of 14 known 88s spend *exactly* 22 in-region gates
  on the R01 landmark instance — so certifying `R01 = 22` would certify *the mechanism*,
  not one circuit's choice.
- **κ is monotone against `n` across the whole spectrum** (9,10 → 18,18,19 → 21 →
  22..28 as `n` goes 97 → 91/92 → 89 → 88): cancellation is what buys the gates, at
  roughly one dedicated clean gate apiece — and **the cone union sits at 53–56 clean
  gates for every circuit from 88 to 92, and 33–35 for the 97s.** Lane P: *"any correct
  Y-lemma must reproduce that number. A lemma that explains that number is the lemma."*
- **`L_cf(M) ≥ 92`** is the only proved quantity in the program above 88, so the whole
  question is literally "how much do cancelling gates buy?" — the records answer "at
  least 4", an 87 would answer "at least 5".
- **And the caveat that must ship with all of it** (lane F4 §3.3, from its independent
  checker): the same structural properties hold for 97@3, 92@4 and 89@5, so these are
  *facts about MixColumns SLPs in this basis*, **not a signature of the 88 plateau**.

### L9 — three obstructions that should stop future funding, each with a certificate — **VERIFIED-IN-LOG**
Worth surfacing together because each kills a plan someone would otherwise pay for:
(a) **route ceiling 83** — no Lagrangian certificate of the residual family can push
`κ+Y+B(A*)` above 83.000 on `88@5fs`, referee-confirmed in exact rationals; the program
needs an *integral* residual bound as well as the span-cone lemma, and
`PROGRAM_STATE.md` names only the latter. (b) **no quotient-composition theorem
exists** — for `W1 ∩ W2 = 0` the pair map is injective, so the joint relaxation *is*
the original problem. (c) **tower rungs are capped below the refereed 56** (51 at
level 3, 26 at level 2), so exact `L2`/`L3` cannot improve `L(M)` at all. Plus lane C's
arithmetic erratum: the predecessor's "next purchase `k(6)` at `|K|=15`, expected value
+1" is **wrong by its own formula** (`1+17+32+6 = 56`, no gain), and the real route
costs pod-months at low probability.

### L10 — `WALKTHROUGH.md` is the right template for the public rewrite — **assessment**
The brief asked me to assess `fleet3/laneF4_rule/WALKTHROUGH.md` as a model. **It is,
and I would adopt its structure directly.** 155 lines. What it does right:
1. **Opens with the command and what it produces**, not with context.
2. **§1 redefines the object in one screen with zero jargon** — "forget gates and
   wires; every wire is described by which input bits it XORs together … a circuit is
   a *set of masks*. That is the whole game." Any reader is now equipped.
3. **§2 explains the coordinate change as the load-bearing idea**, with the three
   consequences numbered — including the one sentence that makes the whole project
   legible: *"one 32-dimensional search becomes ~10 puzzles of dimension 8–16, each
   small enough for an exact SAT solver to prove the minimum."*
4. **A table of the ten blocks** — concrete, scannable, no prose.
5. **§4 names the single edge that buys the last 3 gates and points at the one marked
   line of code.**
6. **§5 shows the arithmetic adding to 88 and immediately disclaims the fit**:
   *"Nobody fitted these to 88. Each is the proven optimum of its own block."*
7. **§6 states the honest weakness (depth 10 vs the records' 5) in the same voice as
   the success**, and explains the verification discipline including the FOUND/STOP rule.
8. **§7 "What is honestly *not* derived"** — two named record-matched parameters and
   the known repair. A public page that does this earns trust nothing else can buy.
9. **Closes with a file map**, so the reader can act.
Two changes for a public version: it assumes the reader knows what `Q27`/`D37`/`vT`
are (add one sentence each, or drop the symbols), and its §4 claim needs the
correction from LEAD L3 (the rank cut buys 0, the edge buys all 3). Everything else
transfers as-is. **The pattern to name for the other pages: command → object →
coordinate change → block table → the one idea → the arithmetic → the honest
weakness → what is not derived → file map.**

### L11 — the published depth-4 frontier is understated by a gate and nobody has acted — **VERIFIED-IN-LOG**
`RECORDS_UPDATE_NOTE.md` (2026-08-19) is a complete, line-numbered, hash-bearing
maintainer instruction for changing `README.md` lines 9/14/44/88/168,
`evidence/circuits/spectrum.json`, and the records repo's `PAPER.md`
(14/26/44/89/97/168/182/192), `PRIOR_ART.md` (12/55/67/90), `bounds.json`,
`CITATION.cff`, `verilog/`, `listings/`, `tests/`. Ten days later the git log shows
v3.0.0 and v3.1.0 releases about 88s and **no depth-4 correction**. The claim itself
is strong: three oracle-verified 91@4 circuits from three distinct lineages (Jaccard
0.556/0.433/0.358), **15,912 distinct verified-realizable 91@4 mask sets** in the repo,
no dead-gate defect, and 91@4 exactly optimal inside the whole measured depth-4
vocabulary by RC2 MaxSAT. Lane G's referee independently emitted a fourth
(`ref_91g_d4.json`). The note is careful about what must *not* be claimed (91@4 is not
proved optimal; a 90@4 outside the vocabulary is UNDECIDED, not refuted). **This is
ready-to-execute goal-3 work and it is the only place in the slice where the public
record is wrong.**

---

## 6. HAZARDS

1. **`fleet1/laneA_v2pricing/results/configs.json` is LOAD-BEARING ACROSS FOUR LATER
   WAVES. Do not move, rename, or delete it.** It is read *at import*, on every
   invocation, by:
   ```
   grep -rn "configs.json" --include=*.py fleet5 fleet8 fleet9 fleet12
   fleet5/laneMENU/code/cells_all.py:18      fleet5/laneMERGE/code/cells.py
   fleet8/unified/code/cells.py:33           fleet9/laneENUM/code/v2inst.py:32
   fleet9/laneENUM/snapshot/code/cells.py:33 fleet12/laneF1/diffcheck.py:28
   ```
   `fleet12/laneALGO/ALGORITHM.md:33` calls it *"the algorithm's one external data
   dependency"*. A reorganization that repoints these paths must update all seven
   call sites plus the `fleet12` audit documents that cite the path verbatim.
2. **Three more cross-lane file paths are hardcoded** and would break the same way:
   `fleet1/laneA_v2pricing/inst/g01full_88at7_f8cd1048a1b76bf2d5a6.json`,
   `fleet2/laneG_generator/inst/free_U1_diag_flag_a246c12491b9.json`,
   `fleet2/laneG_generator/referee/inst/refU1_diag_49f138ea64.json` — all read by
   `fleet3/laneCB_completeness/code/crosscheck.py` (and its two sandbox copies) to
   prove the three lanes price the same object. **These are the evidence that "no
   encoding disagreement exists between the lanes"; deleting the `inst/` trees breaks
   that check.**
3. **75 absolute-path hardcodes** (`/home/joebachir20/...`) in 30 files across the
   slice:
   ```
   grep -rln "/home/joebachir20" --include=*.py --include=*.sh fleet1 fleet2 fleet3 fleet4 | wc -l  -> 30
   ```
   Concentrated in `laneB/code/*.sh` (nanny chains, launchers),
   `laneCB/code/launch_*.sh` + `ctrl_rank2.sh`, `laneD/code/run_bwd.sh`, and several
   `.py` (`v2lib.py`, `price.py`, `resttab.py`, `quotients.py`, `qsolve.py`,
   `fortify.py`, `rtheory.py`, `u07.py`). Any move of the repo root breaks them.
4. **`fleet3/laneCB_completeness/referee/sandbox/{X1_forged_log, X2_bogus_prune}`
   contain deliberately FORGED solver logs and a deliberately bogus prune** (536 KB,
   including a full `ledger.jsonl` of 116 rows each and complete `inst/`+`logs/`
   trees). They were built by the referee to demonstrate that `audit_door.py` passing
   is a consistency check and not tamper-evidence. **They are indistinguishable in
   shape from real data.** Keep them, but they need a loud `README` — a future counting
   pass will otherwise fold their 232 ledger rows and their forged instances into the
   real totals.
5. **Two ledgers of the same object exist by design**:
   `fleet2/laneP_proof/verify1/ledger.jsonl` (8,074 rows, sha256 `497b8da7…`, the
   final file) and `referee/results/verify1_ledger_snapshot_20260820.jsonl` (8,057
   rows, sha256 `bc77f0fd…`, **the refereed reference**, frozen because the live file
   was still being appended to). Lane P §6 quotes the snapshot figures with the final
   figures in parentheses. Deleting either breaks a citation; treating them as
   duplicates and deduplicating would corrupt the referee's record.
6. **No process from this slice is running.** I checked every `python3` PID's
   `/proc/<pid>/cwd`: the only live ones are 20 in `fleet11/laneCUBE` (the live lane,
   untouched) and 1 in `fleet12/laneHALO`. **Nothing in fleet1–4 is live**, so the
   slice is safe to reorganize from an operational standpoint.
7. Lane G's and lane F4's `code/theory.py` and `code/build.py` are **copies**, not
   imports (lane F4 §7 and lane DEPTH `code/f4/` say so explicitly, with cache and
   ledger paths re-pointed). De-duplicating them into a shared module would break the
   provenance claim that each lane's algebra was independently instantiated — and
   would silently couple three lanes that are currently independent.

---

## 7. GAPS

1. **I did not re-run any tally.** Every lane ships a `code/tally.py` that re-derives
   its RESULT.md numbers from its ledger; running nine of them is exactly the kind of
   bulk compute the brief forbids. I re-derived counts directly from the ledgers with
   `wc -l` and small `json` tallies instead, and cross-checked those against the prose.
   Where they disagree I have said so (LEAD L2, L3).
2. **I verified 5 circuits, not 660.** `verify_circuit.py` on
   `gen_f4_88_D4.json` (88/d10), `gen_f4_88_D4alt.json` (89/d10),
   `genD_88at5_record_D5_c3_322.json` (88/d5), `genD_88at7_D5_c3_323.json` (90/d5),
   `NEW88_from_88at6_hit3_depth9.json` (88/d9) — all VALID. The 601 `bwd_out/` files,
   the 7 lane G emissions and the 6 referee copies were **not** re-verified; their
   status is taken from their lanes' logs and referee reports.
3. **I did not compile or deduplicate the 99 HIT-3 lateral 88s** (LEAD L2). Doing so
   requires running `phase2_fin`'s compiler 99 times and cross-checking against the
   139,878-circuit census — real compute, and outside a read-only pass. I have
   confirmed only that the rows exist, that the one that *was* compiled verifies, and
   that all 99 are distinct as `(basin, paid-gate-set)` pairs.
4. **I did not read the four `REFEREE.md` files in full** (1,398 lines total) — I read
   their headlines, bottom lines and verdict tables. If a referee buried a further
   correction in a later section, I would have missed it. The lane G referee's row 7b
   and the lane F4 referee's refutations (i)–(iii) are the ones I did catch, and both
   contradict their lane's `RESULT.md` (LEAD L3).
5. **I did not audit `fleet3/laneF4_rule/audit_gap/audit.py` (18 KB) or
   `check_indep/recheck.py` (15 KB)** beyond their `.out` summaries, nor
   `fleet2/laneG_generator/notes/{lanes_bcd,v2_spec}.md` (94 KB) beyond confirming
   they are subagent digests of the V2 spec and of lanes B/C/D.
6. **Regenerability of `inst/` and `logs/` is an inference, not a measurement.** I
   assume `sweep.py` rebuilds lane G's 1,453 instances (its RESULT.md says ~50 min)
   and that lane CB's 795 rebuild byte-exactly (its `audit_door.py` claims to do
   precisely that). I did not test either, so my archive-don't-delete recommendation
   stands on the audit-trail argument rather than on a verified rebuild.
7. **`experiments/e2_outputcost`'s final numbers** are referenced by lane D task 4(b)
   as ~12 h from draining, with `code/report.py` never run. That directory is outside
   my slice; whoever holds it should confirm whether the report was ever produced.
