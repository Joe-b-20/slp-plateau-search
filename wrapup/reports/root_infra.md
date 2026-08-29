# Slice report: root_infra (repo root files, pipeline/, reproduce/, evidence/, docs/, tests/, .github/) + git map

Agent model: Opus 5 (1M). Date: 2026-08-29. READ-ONLY pass; this file is the only
thing written.

**Summary.** This slice is the *published* half of the project — everything that
is git-tracked and that the public GitHub repo actually serves. It is small
(≈8 MB), unusually well documented (13 README/PROVENANCE/RESULTS/CERTIFICATES
files, all internally cross-referenced and dated), and almost entirely
result-bearing: 8 oracle-verified record circuits, 9 provenance-labelled seeds,
7 untouched run archives, ~165 M exact-window certificate decisions summarised in
147 verdict JSONs, and 23 append-only JSONL ledgers. It contains the ORACLE
(`verify_circuit.py`) that every other slice's claims are keyed on, and the
original v1/v2 plateau-search pipeline that found every record in the repo,
including all five 88s. Three campaign-era markdown documents sit loose at the
root (`side_work.md`, `side_work_REVIEW.md`, `new-representation.md`) — they are
not scratch, they are two substantial external structural analyses plus a
referee review, and the review is the single most useful methodological document
in the slice. Almost nothing here is a deletion candidate: the recoverable
scratch is ~600 KB of `__pycache__` plus 6 dead one-line stray logs (≈700 bytes).
The one live defect: **`README.md`, `evidence/RESULTS.md`, `docs/frontier.svg`
and the CI workflow all still state 92 @ depth 4 as the depth-4 frontier point,
and the repo has held a verified 91 @ depth 4 since at least 2026-08-18, in
three independent lineages.** Git state: 629 tracked files, 30 untracked entries
(all campaign work, gitignored or never added), and **one unpushed commit,
`23d80d7`**, which is the most important commit in the repo's history — it is the
one that withdraws the inference "certificates ⇒ 87 is unlikely".

---

## 1. INVENTORY

### 1.1 Sizes

```
du -sh pipeline reproduce evidence docs tests __pycache__ .pytest_cache .github
```

| path | size | what it IS | documented? |
|---|---|---|---|
| `evidence/` | 4.9 M | the archive: 8 record circuits, 7 untouched run archives, the certificate corpus, imported prior art | **yes** — `RESULTS.md` (59 K), `CERTIFICATES.md` (18 K), 6 `PROVENANCE.md`, `HARVEST.md`, 7 `CODE_PROVENANCE.md` + `CONFIG_AS_RUN.md` pairs |
| `pipeline/` | 2.3 M | the v2 record-hunting engine (4 modules, 2 014 LOC) + 9 seeds + 6 local run folders | **yes** — `pipeline/README.md` (12 K), `pipeline/seeds/README.md` (provenance table) |
| `reproduce/` | 284 K | one command per record; carries the *frozen v1 per-method code* | **yes** — `reproduce/README.md`, the best-written file in the slice |
| `tests/` | 128 K | `test_invariants.py`, 541 LOC, 24 tests | self-documenting docstring |
| `docs/` | 108 K | `frontier.svg` + `lineage.svg` and the two generators that emit them | scripts carry header docstrings |
| `.github/` | 12 K | `workflows/verify.yml` — CI that re-verifies all 8 records and asserts depth-tightness | inline comments |
| `__pycache__/` `.pytest_cache/` | 48 K | build scratch (gitignored) | n/a |

Root markdown/scripts: `README.md` (14 K), `METHODS.md` (59 K), `CITATION.cff`,
`LICENSE` (MIT), `verify_circuit.py` (4.9 K), `CHECK_SOLVER.sh` (1.8 K),
`FLEET_PLAN.md` (5.3 K), `SESSION_PROMPT.md` (5.3 K), `side_work.md` (22 K),
`side_work_REVIEW.md` (18 K), `new-representation.md` (43 K), 6 stray logs.

### 1.2 `evidence/` subdir inventory — what each bundle certifies

```
du -sh evidence/*   |   for d in evidence/*/; do find $d -type f | wc -l; done
```

| subdir | size | files | what it certifies |
|---|---|---|---|
| `campaign87_certificates/` | 1.3 M | 203 | ≈165 M exact remove-k/restore-fewer window decisions, zero reducible, over 47 canonical 88s + 105 801 of ≈139 878 known 88-gate states; plus 130 windowed-SAT verdicts (UNSAT relative to slot order). Ships the two deciders verbatim in `code/`. **Read §7a of `CERTIFICATES.md` before quoting any number in it.** |
| `parallel_ladder_run_2026-07-13/` | 920 K | 59 | the v1 *old-acceptance-rule* cascade: from-scratch 97 @ 3, and 89 @ 6 at rung d10. `HARVEST.md` has the per-rung table and the full cascade timeline |
| `campaign87_run_2026-07-27_got_88at8_thirdfamily/` | 712 K | 118 | 88 @ depth 8, third distinct family — **DERIVED**, lineage through Jean's published 88 via a symmetrized 92 |
| `campaign87_run_2026-07-26_got_88at7/` | 448 K | 80 | 88 @ depth 7, own lineage, no imported material — matches the published record with an independent circuit (61/88 shared masks) |
| `cascade_run_2026-07-14_from_scratch_newlogic/` | 436 K | 61 | 92 @ depth 4 from scratch, with the rewritten Pareto-tie-break + continuous-reseeding coordinator |
| `campaign87_run_2026-07-28_got_88at6_fromscratch/` | 396 K | 23 | 88 @ depth 6, **first 88 found from scratch** (root `constructors.build("naive", 2163)`), + its exhaustive k≤3 shell logs |
| `campaign87_run_2026-07-29_got_88at5_derived/` | 316 K | 20 | 88 @ depth 5 **DERIVED** (through Jean's 88); retained as the record of how depth 5 was first reached and of the seed-rotation bug that made it derived |
| `campaign87_run_2026-07-30_got_88at5_fromscratch/` | 244 K | 14 | 88 @ depth 5 **from scratch** (root `naive#1958`) — the frontier point; + its exhaustive k≤3 shell logs |
| `sub89_run_2026-07-14_got_89at5/` | 152 K | 21 | 89 @ depth 5 (byte-identical code to the cascade run, re-aimed at the frontier) |
| `circuits/` | 40 K | 9 | the 8 canonical record circuits + `spectrum.json` (SHA-256 manifest) |
| `campaign87_imported_prior_art/` | 24 K | 3 | Jean 88 (ePrint 2026/1481) and Sun–Yang–Li 89 (ePrint 2025/1493), transcribed, oracle-verified, credited |

`campaign87_certificates/` subdirs: `exact_window/` (19 f), `exact_k4/` (33),
`pop_decider/` (29), `family3_exact/` (71), `sat_deep/` (8), `loose_sat/` (12),
`family3_sat/` (11), `rho2_symmetric_90s/` (14), `code/` (5).

### 1.3 File-type breakdown of `evidence/`

```
find evidence -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
```
373 json · 95 log · 43 py · 29 md · 23 jsonl · 21 stdout · 15 pyc · 9 out · 4 sh

### 1.4 The three loose root documents

- **`side_work.md`** (1 847 lines) — user-supplied external analysis: the
  "circle representation" of the 32 inputs, `Δ = I + R`, `M = I + LΔ + Δ³`, the
  carrier/difference (C/D) dichotomy, the `88 = 24 + 15 + 17 + 32` census, gauge
  freedom, and a 30-section status table. Ends at §30 with an explicit open
  question and a stated next step.
- **`side_work_REVIEW.md`** (338 lines, dated 2026-08-21) — the project's
  adversarial review of the above. Re-derives every claim; confirms ~20, refutes
  5 with population census data, and closes the document's route to 87. **This is
  the highest-value methodological document in the slice** (see §5).
- **`new-representation.md`** (2 223 lines) — a second, larger external record:
  the forward/backward bi-mask (F, B) demand-flow representation, the frozen-
  exterior module decomposition (61 + 27 = 88), the five ternary repair planes
  (3⁵ = 243 optimal modules over a 22-mask backbone), and the backbone defect
  graph. 64 sections, ending with two named next objects.

### 1.5 The stray root logs — confirmed dead

```
cat w1.nohup wshB1.log wshB2.log wshC1.log wshC2.log d3_b.out
```
All six are single-line "file not found" errors from launches whose scripts no
longer exist (`worker.sh`, `satfix_hunt.py`, `satfix_hunt2.py`, `deep_extras.py`).
Total ≈700 bytes. **Dead scratch, confirmed.**

---

## 2. METHODS

### oracle-verify-circuit
- **Family:** verification / ground truth.
- **What it does:** rebuilds the 32×32 MixColumns matrix from GF(2⁸) arithmetic
  (the code *is* the spec — `xtime`, `gf_mul`, coefficients `[2,3,1,1]`), then
  replays a circuit gate by gate over 32-bit integer masks and reports gates,
  depth, how many of the 32 target masks appear among the built signals, and
  structural problems (non-2-input gates, forward references). Exits 0 iff all
  32 outputs are built with no problems and (optionally) depth ≤ a cap.
- **Twist vs siblings:** it is the *only* independent verifier — `pipeline/`,
  `reproduce/` and the certificate code all use `mixcolumns_core.py` copies, and
  this file shares no code with them. It has a built-in spec self-check
  (`wts.count(5)==20 and wts.count(7)==12`) that fails loudly if the rebuilt
  matrix is wrong. Accepts four circuit encodings (index pairs, mask triples,
  the kit format, bare list).
- **Measured performance:** every circuit claim in the whole tree is defined as
  "this printed VALID". CI runs it on all 8 records at their depth and asserts
  each FAILS one level tighter (`.github/workflows/verify.yml`).
- **Cost:** milliseconds per circuit.
- **Code:** `/home/joebachir20/xor_ui/slp-plateau-search/verify_circuit.py` (129 LOC).
- **Logs/results:** `evidence/RESULTS.md` carries its output for all 8 records.
- **Generality:** **MIXED, ~30 lines from CIRCUIT-GENERIC.** Only
  `mixcolumns_target_masks()` (lines 37–55) and the weight self-check (line 99)
  are MixColumns-specific. For `aes_inv_mixcolumns` change the coefficient row to
  `[14, 11, 13, 9]` and recompute the expected weight profile; everything else —
  the replay loop, the depth computation, the four encodings, the CLI — is target-
  agnostic. This is the single highest-leverage file to port to a new target.
- **Phase-2 verdict:** **keeper, first thing to port.** Nothing downstream is
  trustworthy without it.

### anneal3-depth3-annealer
- **Family:** plateau-search / from-scratch construction.
- **What it does:** models each of the 32 outputs as A ⊕ B where A and B partition
  its target bits into depth-≤2 parts; auxiliary signals are refcount-costed so a
  shared part is paid once. Simulated annealing over the per-output split choices,
  then greedy descent and iterated local search with random kicks. Depth ≤ 3 holds
  by construction.
- **Twist vs siblings:** the only from-scratch constructor that is *depth-first*
  rather than gate-count-first, and the only engine untouched by the v2 rebuild.
- **Measured performance:** **97 @ depth 3 from scratch**, beating the published
  99 @ 3 (Shi–Feng–Xu ToSC 2023). Re-validated 2026-07-27: cost 97 on its first
  RNG seed after 81.1 s on one core (23.5 s annealing, then ILS); 60–156 s across
  earlier runs. Independently re-derived by the demand-flow work gate-for-gate.
- **Cost:** ~81 s, one core.
- **Code:** `pipeline/engines.py:engine_anneal3`; frozen v1 copy in
  `reproduce/reproduce.py`.
- **Logs/results:** `evidence/parallel_ladder_run_2026-07-13/d3.log`,
  `reproduce/out_97.json`.
- **Generality:** **MIXED.** The A⊕B partition model is generic for any GF(2)
  linear map; the target masks come from `mixcolumns_core.py`. Port = swap the
  spec module.
- **Phase-2 verdict:** **keeper.** It is the cheapest known way to get a good
  shallow root for a new target, and it is the root of the project's entire
  own-lineage chain.

### naive-random-xor-tree-root
- **Family:** from-scratch construction (seedless root generator).
- **What it does:** `constructors.build("naive", <int>)` generates randomized
  balanced XOR trees over the 32 raw inputs with opportunistic reuse, producing a
  valid but large depth-3 circuit (139 and 146 gates for the two recorded seeds)
  as a pure function of one integer.
- **Twist vs siblings:** unlike `anneal3` it makes no attempt at quality — its
  entire value is *provenance*: the root reads nothing from disk, so everything
  descended from it is certifiably free of imported material.
- **Measured performance:** the roots of **both** from-scratch 88s.
  `naive#2163` → 139 @ d3 → 88 @ d6 (restart 18, 18.96 h in). `naive#1958` →
  146 @ d3 → 93 → 91 → 90 → 89 → **88 @ d6 at t = 69 192.7 s** → **88 @ d5**
  (session 5, restart 16, 19.22 h in). Both reproduce their logged roots exactly
  from the integer.
- **Cost:** milliseconds to build; the descent from it took ~19 h of one worker
  inside a 16-process fleet.
- **Code:** `evidence/campaign87_run_2026-07-28_got_88at6_fromscratch/code/`
  (the 07-30 archive hash-pins the same code rather than duplicating it).
- **Generality:** **CIRCUIT-GENERIC** apart from the input count.
- **Phase-2 verdict:** **keeper** — this is how a new target gets a clean-
  provenance starting point in one line.

### lns-destroy-rebuild (v2 merged engine)
- **Family:** plateau-search / large-neighbourhood search.
- **What it does:** repeatedly destroys a connected cone (or a large injected
  block) of the current value set and rebuilds it from a scored pool, accepting on
  a simulated-annealing schedule with reheat. Rebuilds are peeled before being
  judged; victims are re-pooled at a higher cost class so a rebuild can never
  dead-end; the depth cap is enforced by a level-BFS `relax`.
- **Twist vs siblings:** vs the v1 LNS, the v2 engine adds five separately
  measured mechanisms — victim repooling (~34× accepted moves/s; feasible
  iterations 1.2 % → 100 %), scored hot pools (~11× accepted moves, 16–18× pool
  hit rate), peel-before-accept (2 630 near-miss rebuilds recovered in a 2-min
  probe), SA-with-reheat (~2× drift), and the `coneinj`/`biginj` destroy mix
  (uniform destroys measured dead: 0 accepts in 5 633).
- **Measured performance:** ~100–180 it/s on a loaded box (v1: 60–100). Re-found
  **89 @ depth 5 at t = 0.3 s of its first chunk** (LNS iteration 18), twice, on a
  seed the v1 engine needed 592 s for. All five 88s were found inside runs of this
  engine (though the 88s themselves came from *walk* chunks).
- **Cost:** the 88-hunting runs are hours to days of many cores.
- **Code:** `pipeline/engines.py:engine_lns` (1 204 LOC total in the file).
- **Logs/results:** `evidence/campaign87_run_*/runs_hunt/*.log`,
  `pipeline/runs_parallel/*/`.
- **Generality:** **MIXED.** The engine is written against value-sets of 32-bit
  masks with a fixed 32-target set; retargeting = new spec module + the width
  constants. Nothing in the acceptance/destroy/rebuild logic is AES-aware.
- **Phase-2 verdict:** **keeper** — it is the workhorse, and the measured-good
  knob values ship as defaults.

### walk-valueset-plateau
- **Family:** plateau-search / neutral walking.
- **What it does:** remove-1 and hub moves over the incremental closure of a value
  set, with exact complete repair enumeration; walks sideways across equal-size
  circuits rather than descending.
- **Twist vs siblings:** it is the *plateau sprayer* — it does not try to improve,
  it tries to move. The Pareto tie-break (accept equal gates at strictly lower
  depth) is what converts its lateral motion into depth wins.
- **Measured performance:** **480–640 it/s** on a loaded box (v1: ~70–110). Both
  campaign-era 88s and both from-scratch 88s were surfaced by walk chunks. In the
  88 @ 7 run the walk found the 88 masks at depth 11 and the Pareto tie-break
  carried the same mask set to depth 7 **5.3 s later**.
- **Cost:** as above.
- **Code:** `pipeline/engines.py:engine_walk`.
- **Logs/results:** `evidence/campaign87_run_2026-07-26_got_88at7/runs_hunt/w10_sym94.log`.
- **Generality:** **MIXED**, same as `lns`.
- **Phase-2 verdict:** **keeper** — the only engine that has ever produced an 88.

### hub-move-remove2add1 (the twist that named the repo)
- **Family:** plateau-search / local move class.
- **What it does:** removes two masks from a value set and adds one, using the
  complete repair machinery to enumerate every legal single replacement.
- **Twist vs siblings:** it is the one move class that can strictly reduce gate
  count by one in a single step, which is why the repo is named after it.
- **Measured performance:** **DEAD at the frontier, exactly and repeatedly.**
  0 successes in ~2.24 M repair samples across all seeds; then proven exactly —
  the remove-2-add-1 neighbourhood of *every one of the five 89 seeds* is empty
  (1 596 windows each, exhaustive), and empty inside every certified k ≤ 3 shell.
  Independently re-confirmed by the demand-flow work (1 596 cases, 0 moves).
- **Cost:** seconds per circuit to exhaust.
- **Code:** `pipeline/engines.py` (inside `engine_walk`); `reproduce/reproduce.py`
  method `"89"` is the clean readable statement of it.
- **Logs/results:** `METHODS.md` §8; `evidence/campaign87_certificates/exact_window/k2_*.json`.
- **Generality:** **CIRCUIT-GENERIC.**
- **Phase-2 verdict:** **dead-end at the frontier, keeper as a first probe** on a
  *new* target — it cut 90 → 89 in 150 s historically, and on an unexplored
  circuit the frontier is far away.

### cascade-depth-ladder
- **Family:** pipeline / search orchestration.
- **What it does:** rung d3 starts from nothing with `anneal3`; each time the
  frontier rung beats its baseline (or times out) the next deeper rung launches
  seeded from it; all rungs keep running and reseed one another.
- **Twist vs siblings:** depth is the *schedule variable*, not a constraint — the
  ladder deliberately buys depth slack to find gate count, then lets the Pareto
  tie-break pull the result back down.
- **Measured performance:** produced **92 @ depth 4 from scratch** at
  t = 9 610 s (2.67 h). Full cascade timeline in
  `evidence/cascade_run_2026-07-14_from_scratch_newlogic/coordinator.log`
  (d3 97 → d4 96 → d5 95 → d6 94 → d7 93 → d8 92 → …). The v1 version of the
  same shape (21 h) gave the per-rung table 97/94/92/91/89/90/90/89/90/90 in
  `evidence/parallel_ladder_run_2026-07-13/HARVEST.md`.
- **Cost:** hours (2.7 h to 92 @ 4; the v1 run 21 h).
- **Code:** `pipeline/ladder_parallel.py` (`--mode cascade`, 459 LOC).
- **Logs/results:** the two run archives above (436 K + 920 K).
- **Generality:** **CIRCUIT-GENERIC** orchestration over a MIXED engine set.
- **Phase-2 verdict:** **keeper** — this is the canonical "point it at a new
  circuit and walk away" recipe, and it is the only one with a from-scratch
  Pareto frontier to show for it.

### pareto-tiebreak-and-continuous-reseeding
- **Family:** pipeline / acceptance rule (a coordinator twist, separately
  load-bearing).
- **What it does:** the improve rule accepts fewer gates **or** equal gates at
  strictly lower depth, and the engines were changed to *surface* equal-size
  shallower candidates instead of dropping them; the coordinator continuously
  offers every worker the best circuit feasible at that worker's depth cap.
- **Twist vs siblings:** the v1 rule accepted strictly-fewer-gates only. That rule
  provably could not have produced any of the depth records — it would have
  discarded an 89 @ depth 5 while holding an 89 @ depth 6, which is exactly the
  situation the archive shows.
- **Measured performance:** the 92 @ 4 exists *only* because of it (found by the
  depth-8 rung searching with slack). The 88 @ 7 reached depth 7 from depth 11 in
  5.3 s through it. `reproduce/README.md` documents that stopping on gate count
  alone yields 88 @ depth 8–11 instead.
- **Cost:** free.
- **Code:** `pipeline/ladder_parallel.py`, `pipeline/worker.py`.
- **Logs/results:** `pipeline/README.md` "How the pipeline evolved", chapters 1–3.
- **Generality:** **CIRCUIT-GENERIC.**
- **Phase-2 verdict:** **keeper, non-negotiable.** The single cheapest mechanism
  in the repo per record produced.

### alt-worker-mode
- **Family:** pipeline / worker schedule.
- **What it does:** alternates a 300 s `walk` chunk with a 600 s `lns` chunk from
  the worker's own best — the walk sprays across the plateau, the LNS punches down
  from wherever it landed.
- **Twist vs siblings:** not an engine; a schedule. It exists because walk and lns
  fail differently (walk cannot descend, lns cannot diversify).
- **Measured performance:** the mode of the record worker `w10_sym94` that found
  **88 @ depth 7** at t = 1 973 s, and of `c_naive` that found **88 @ d6 and
  88 @ d5 from scratch**. Single-worker re-run 2026-07-27 reached 88 @ depth ≤ 7
  in **19.4 min**, with the first chunk reproducing the archived worker's
  iteration numbers to the digit (92 @ it=27, 91 @ it=32, 90 @ it=603/622/670/723,
  89 @ it=58 504, 89 @ 7 @ it=58 795).
- **Cost:** 19–33 min for the 88 @ 7 on one core.
- **Code:** `pipeline/worker.py`; aimed by `reproduce/hunt_88.py` (198 LOC).
- **Logs/results:** `evidence/campaign87_run_2026-07-26_got_88at7/runs_hunt/`.
- **Generality:** **CIRCUIT-GENERIC.**
- **Phase-2 verdict:** **keeper** — the highest hit-rate configuration in the
  slice.

### plateau-harvesting
- **Family:** structural-analysis / data generation.
- **What it does:** appends every distinct equal-best mask set the search walks
  over to a `<label>.pop.jsonl` population file, instead of discarding siblings.
- **Twist vs siblings:** it costs nothing and turns a search into a census. It is
  the reason the project has a *population* to reason about at all.
- **Measured performance:** produced the **≈139 878 distinct known 88-gate
  states** (84 989 families 1–2 + 53 902 family 3). That population is what every
  certificate sweep, every family census and (per `side_work_REVIEW.md`) every
  falsification of a single-circuit theory has been run over. All five 88s were
  found inside harvesting runs.
- **Cost:** disk — "a few MB per worker-minute"; it is the file that fills a disk
  on a long run.
- **Code:** `pipeline/engines.py:_Harvester`; knob `harvest` (on by default).
- **Logs/results:** the populations themselves are in the raw campaign archive,
  not in this slice.
- **Generality:** **CIRCUIT-GENERIC.**
- **Phase-2 verdict:** **keeper, and arguably the most underrated method here.**
  On a new target, turn it on from day one — the population is worth more than the
  record.

### rho2-symmetric-orbit-search (symmetrize → orbit-peel → orbit-LNS → union-cross)
- **Family:** structural-analysis / symmetry-reduced search.
- **What it does:** byte rotation ρ (order 4) commutes with MixColumns, so it acts
  on value-sets. The half-rotation ρ² is used to search in orbit space, where a
  move adds or removes a whole orbit at once; existing circuits are symmetrized
  and peeled into the symmetric subspace; and progress is made by **union
  crossings** of two symmetric circuits rather than by local moves.
- **Twist vs siblings:** full ρ-symmetry costs about +19 gates (best fully
  symmetric ≈108), so the method deliberately uses only the *half* rotation, where
  the elite basin is already 79–81 % symmetric. The 12 ρ²-fixed masks turn out to
  be the classic (x0^x2)/(x1^x3) sharing trick, rediscovered rather than imposed.
- **Measured performance:** ~90–120 walk it/s vs ~5 for naive orbit search. Two
  **exactly ρ²-symmetric 90-gate circuits** (depth 9 and depth 7, Jaccard 0.463
  apart) — previous best exactly symmetric was 94. Both machine-certified locally
  optimal in orbit space: every remove-1-orbit and all **666** remove-2-orbits-
  add-≤1 moves fail, zero equal-cost remove-2 swaps. As a *seeding device*: the
  ρ²-symmetric 94 @ 5 is the seed from which the 88 @ 7 was found, and the
  ρ²-symmetric 90 @ 9 is the seed of the 88 @ 8.
- **Cost:** the 90 → 89 @ 5 descent from a symmetric basin took ~15 min.
- **Code:** the orbit engine is not in this slice (raw campaign archive);
  `evidence/campaign87_certificates/rho2_symmetric_90s/make_union.py` is the
  (three-line) union tool.
- **Logs/results:** `evidence/campaign87_certificates/rho2_symmetric_90s/`
  (72 K, 14 files: `cert90_90g.json`, `cert90_best.json`, `symA.log`, `sym88.log`,
  `uA88.log`, `union_A88.json`); `METHODS.md` §11.
- **Generality:** **MIXED — but the *method* is CIRCUIT-GENERIC.** What is needed
  for a new target is its automorphism group. For `aes_inv_mixcolumns` the byte
  rotation is the same Z/4, so this ports essentially unchanged and is probably
  the fastest route to a good seed there.
- **Phase-2 verdict:** **keeper** — two of the five 88s trace to it, and it is the
  only method in the slice that made progress by *crossing* rather than editing.

### exact-window-decider (budgets 1–2, k ≤ 3)
- **Family:** exact local certificate.
- **What it does:** "remove a window of k masks from a verified circuit; can k−1
  or fewer new masks restore all 32 targets?" Frontier-cascade closure with
  rollback. A `None` answer is a *proof* for that window, backed by a first-unlock
  case analysis in the module docstring. Exact at k=2 and k=3; above that it does
  an honest partial DFS whose runs are recorded as `nosol`, never as irreducible.
- **Twist vs siblings:** the completeness proof is what separates it from the SAT
  certificates — a "no" here is a theorem, a "no" there is evidence.
- **Measured performance:** ~113 000 windows decided. **All 1 540 k=2 and all
  27 720 k=3 windows of Jean's 88 exhaustive, all irreducible** (⇒ any 87 differs
  from it by ≥4 masks). The remove-2-add-1 neighbourhood of all five 89 seeds is
  exactly empty. Validated 25/25 and 12/12 against independent brute force; then
  branch-validated on **4 200 planted YES windows over 74 circuits, 4 200/4 200
  correct**, with cases 1b and 2a tested in isolation (462/462 and 33/33).
- **Cost:** hours per circuit at k=3 (27 720 windows).
- **Code:** `evidence/campaign87_certificates/code/exact_window.py` (358 LOC,
  stdlib-only, shipped verbatim as archived).
- **Logs/results:** `evidence/campaign87_certificates/exact_window/` (80 K, 19 f);
  per-run shells in `campaign87_run_*/certificates/`.
- **Generality:** **MIXED.** The decider is generic over a target mask set; it
  imports `mixcolumns_core` and (inside `rebuild_circuit()` only) `engines`.
  Retarget = swap the spec module.
- **Phase-2 verdict:** **keeper — but read §7a first.** See LEAD L1: this
  instrument cannot distinguish an optimal circuit from one nine gates too big.

### exact-k4-decider (budget 3, k = 4)
- **Family:** exact local certificate (the k=4 sibling).
- **What it does:** the same question at "remove 4, restore with ≤ 3", with its own
  completeness proof.
- **Twist vs siblings:** budget 3 needs a different case analysis; and at k=4 the
  window count (367 290 per circuit) makes exhaustion infeasible, so it runs
  *prioritised* — every all-diff quad and every structural window first.
- **Measured performance:** validated on **1 257 instances against independent
  complete brute force, 100 % agreement including 122 genuine NOs**, identically
  under CPython 3.10 and PyPy 3.11. On Jean's 88: 32 685 / 367 290 windows (8.9 %)
  decided exactly, all irreducible. On the family-3 anchor: 20 432 / 367 290
  (5.6 %). On the project's independent 88 @ 7: **9 windows** — the least-certified
  circuit in the corpus.
- **Cost:** ~16.8 M exact decisions logged from this module.
- **Code:** `evidence/campaign87_certificates/code/exact_k4.py` (342 LOC).
- **Logs/results:** `evidence/campaign87_certificates/exact_k4/` (188 K, 33 f).
- **Generality:** **MIXED**, as above.
- **Phase-2 verdict:** **keeper**, with the same §7a caveat.

### population-k2-k3-sweep
- **Family:** exact local certificate at population scale (a deployment twist, not
  a new decider).
- **What it does:** runs the two deciders over the *harvested population* rather
  than over hand-picked circuits, ordered most-distant-from-Jean first so the
  least-covered half of the population is the swept half.
- **Twist vs siblings:** it converts a per-circuit certificate into a statement
  about a plateau. It is also fully resumable from an append-only progress JSONL.
- **Measured performance:** families 1–2: **51 899 / 84 989 states (61.1 %) fully
  swept at k=2, every one irreducible — 79 924 460 exact decisions**; the entire
  symdiff ≥ 55 band is closed; 33 090 states remain (~2.9 h uncontended).
  Family 3: **53 902 / 53 902 (100 %), 83 009 080 exact decisions in 10 841 s —
  the family is CLOSED at k=2.** First k=3 theorems on 19 theorem-starved
  population states: 526 680 exact decisions, all irreducible. Sanity gate: 12/12
  sampled population states rebuilt to full circuits and passed the oracle at 88.
- **Cost:** ~64.1 M + ~84.0 M decisions; the f3 k=2 pass alone 10 841 s.
- **Code:** the two deciders above, driven from the campaign archive.
- **Logs/results:** `evidence/campaign87_certificates/pop_decider/` (168 K, 29 f),
  `family3_exact/` (344 K, 71 f). **Resumable frontiers all present on disk** —
  see §6.
- **Generality:** **MIXED**, as the deciders.
- **Phase-2 verdict:** **keeper as an instrument, superseded as an argument** —
  §7a shows population coverage does not buy evidence about 87.

### windowed-sat-fsk (CaDiCaL)
- **Family:** SAT / bounded synthesis.
- **What it does:** encodes "remove a window of k masks, resynthesise the circuit
  with ≤ k−1 new gates" as a sound Fuhs–Schneider–Kamp CNF where any model is a
  whole realizable circuit; runs CaDiCaL in killable child processes; every
  window's removal set is logged with its verdict so every run resumes; every
  model found is re-verified through the oracle.
- **Twist vs siblings:** it reaches window sizes the exact deciders cannot
  (k = 9–16 vs k ≤ 4), at the cost of being **UNSAT relative to the encoding's
  fixed slot order** — strong evidence, not a completeness proof.
- **Measured performance:** **48 windows on Jean's 88 at k = 9–16: 34 UNSAT,
  14 timeout, 0 SAT.** Max window proven UNSAT: **k = 16** (previous frontier 12).
  Hardness anti-correlates with nB (broken kept masks), not k: every window with
  nB ≥ 19 was decided. Pipeline self-test: a planted r=k window came back SAT in
  1.6 s and decoded to an oracle-VALID 88 @ 7.
- **Cost:** individual UNSATs up to 1 509 s.
- **Code:** not in this slice (raw campaign archive).
- **Logs/results:** `evidence/campaign87_certificates/sat_deep/` (76 K, 8 f;
  `results.jsonl` 21 K, `selftest.jsonl`, `phaseA/B/C.log`).
- **Generality:** **CIRCUIT-GENERIC encoding, MIXED harness** — the CNF is over an
  arbitrary target set.
- **Phase-2 verdict:** **keeper** — the only method here that reaches radius 16,
  which is the regime §7a says actually matters.

### windowed-sat-kissat-symbreak
- **Family:** SAT / bounded synthesis (the symmetry-breaking twist).
- **What it does:** the same encoding plus two knob-gated, soundness-proved
  symmetry-breaking layers — SB-P (parent commutativity) and SB-F (guarded lex on
  adjacent free slots) — solved with Kissat 4.0.4. Clauses are only added, so an
  UNSAT can never be manufactured.
- **Twist vs siblings:** SAT-preservation is what needs proving here, and it was
  measured: 7/7 planted self-tests all decoded to verified 88s.
- **Measured performance:** the three slowest CaDiCaL UNSATs (960/1 000/1 509 s)
  re-decided in 28/45/106 s — **14–34× faster**. Re-adjudicated the 14 survivors
  of `sat_deep`: **10 UNSAT, 4 undecided, 0 SAT**, including the two loosest
  windows (nB = 3, nB = 5). Final standing on Jean's 88 across both:
  **48 windows → 44 UNSAT, 4 undecided, 0 SAT, frontier k = 16.** On the project's
  independent 88 @ 7: 8 cone windows → 5 UNSAT, 3 undecided, 0 SAT, including an
  nB = 1 (near-pure synthesis) window in 34 s — *this is the only SAT coverage the
  independent 88 has.*
- **Cost:** 28–106 s per previously-slow window.
- **Code:** not in this slice.
- **Logs/results:** `evidence/campaign87_certificates/loose_sat/` (92 K, 12 f);
  the third-family application in `family3_sat/` (152 K, 11 f: anchor 50 windows →
  37 UNSAT/13 undecided, **entire k ≤ 12 regime UNSAT, 28/28**; 8 reps → 25 UNSAT
  / 7 undecided).
- **Generality:** **CIRCUIT-GENERIC.**
- **Phase-2 verdict:** **keeper — the best cost/coverage instrument in the slice.**
  Its named residual gap (fixed slot order) is quantified, not hand-waved.

### certificate-control-audit (the repricing)
- **Family:** meta-method / instrument validation.
- **What it does:** runs a negative-result instrument on inputs whose ground truth
  is *known to be positive*, to measure whether the instrument has any
  discriminating power for the question it is being read as answering. Three
  parts: (1) run the exact decider on circuits known to be improvable; (2)
  branch-validate the completeness proof by deleting earlier cases and checking
  the later ones still recover planted witnesses; (3) measure how much a SAT
  verdict depends on an encoding choice by permuting that choice.
- **Twist vs siblings:** it is the only method here whose subject is another
  method. It produced the repo's most consequential result by *withdrawing* an
  inference rather than adding one.
- **Measured performance:**
  (1) **97 @ 3, 94 @ 4, 92 @ 5, 91 @ 5, 90 @ 5, 89 @ 9 and Jean's 88 @ 7 all have
  exhaustively empty k=2 shells (12 241 windows) and no reducible k=3 window in
  8 400 sampled.** A 97-gate circuit — nine gates above best known — is
  indistinguishable from an 88 by this instrument. The reason is scale: over 45
  circuits with a smaller verified circuit available, the distance to that better
  circuit is **median 42 masks, min 3, max 48; 44 of 45 need k ≥ 8**. Certified
  radius is 3.
  (2) 4 200/4 200 planted YES windows answered correctly; 462/462 and 33/33 with
  earlier branches deleted. **No completeness bug — the ~165 M verdicts stand.**
  (3) On provably-SAT windows the encoding returns UNSAT under **123 of 128
  arbitrary mask orderings**, but under **128/128 legitimate topological
  reorderings the verdict does not move** (and the seed's own gate order is in
  that class). The depth-capped encoder's CNF is byte-identical under every
  reordering of the kept set.
- **Cost:** one day (2026-07-30).
- **Code:** `campaign_87/cert_audit/` (outside this slice, present on disk).
- **Logs/results:** `METHODS.md` §§10a–10c; `evidence/RESULTS.md` §9;
  `CERTIFICATES.md` §7a; commit **`23d80d7`** (unpushed).
- **Generality:** **CIRCUIT-GENERIC — it is a discipline, not code.**
- **Phase-2 verdict:** **keeper, and it should be a gate on every negative result
  in phase 2.** Cheapest single improvement to method quality in the whole tree.

### reproduce-legacy-single-move-demos
- **Family:** plateau-search (frozen v1 per-method code, kept as documentation).
- **What it does:** three self-contained demonstrations of one move each, on
  *superseded* records: method `"91"` (plateau walk over equal-size circuits from
  the published Xiang–Zeng–Lin–Bao–Zhang 92 until one gate becomes removable →
  91 @ 6, **6.7 s**); method `"89"` (value-set walk, remove-1 + remove-2-add-1
  hub, cutting 90 → 89 at unconstrained depth, **150 s**); method `"90"`
  (irreducibility proof of a 91: duplicate scan, peel, all-pairs remove-2-add-1,
  **0.2 s**).
- **Twist vs siblings:** each reads as *one move* rather than as a tuned kernel.
  Deliberately frozen at v1 and not touched by the v2 rebuild.
- **Measured performance:** as above, all re-validated 2026-07-27 on one core.
  Honest negative recorded in the README: from nothing, method `"89"`'s walk floors
  near 92 — the 89 needs its seed.
- **Cost:** seconds.
- **Code:** `reproduce/reproduce.py` (996 LOC), `reproduce/seeds.py` (77 LOC).
- **Logs/results:** `reproduce/out_91.json` (91), `reproduce/out_89.json` (89),
  `reproduce/out_90.json` (**contains 91 gates** — the irreducibility demo, as the
  README says), `reproduce/out_97.json` (97), `reproduce/out_88hunt.json` (88).
- **Generality:** **MIXED**; `mixcolumns_core.py` here is byte-identical to
  `pipeline/mixcolumns_core.py` and `diff` proves it.
- **Phase-2 verdict:** **keeper as pedagogy / smoke tests**, superseded as search
  by the v2 engines.

### depth-tightness-ci and reference-differential-unit-tests
- **Family:** verification hygiene.
- **What it does:** (a) CI verifies all 8 records at their stated depth **and
  asserts each FAILS one level tighter**, keyed on the *file* never on the
  (gates, depth) pair (two records share (88, 5)); plus `unittest discover` and
  `compileall`. (b) 24 unit tests check the spec's weight profile, oracle
  rejection of forward references / truncation / depth violations, the eight
  records against `spectrum.json` SHA-256s, value-set realizability and trimming,
  and — the valuable part — the v2 fast kernels (`relax`, incremental closure,
  `remove_query`, exact `_repair`) against **plain reference implementations
  written out in the same file**, plus bounded live engine runs through the
  verify-before-claim path.
- **Twist vs siblings:** differential testing of a fast kernel against a slow
  obvious one, in-file, is what makes the engine's negatives believable.
- **Measured performance:** whole module runs "well under two minutes",
  stdlib-only, deterministic apart from two time-boxed engine runs.
- **Cost:** < 2 min.
- **Code:** `tests/test_invariants.py` (541 LOC),
  `.github/workflows/verify.yml`.
- **Generality:** **MIXED** — the record list and weight profile are hardcoded;
  the differential-testing pattern is generic.
- **Phase-2 verdict:** **keeper, and the pattern should be copied** for any new
  target's kernels.

### demand-flow-search (F,B bi-mask routing) — *documented here, implemented elsewhere*
- **Family:** representation change / search.
- **What it does:** gives every signal a forward mask F (which inputs it XORs) and
  a **backward demand mask** B (which of the 32 outputs currently depend on it).
  The circuit becomes a sequence of rank-one factorizations `M = ⊕ B_v F_vᵀ`. A
  *routing* move rewrites B through an existing XOR triangle at **zero gate cost**;
  a *materialization* move buys `c = a⊕b` for one gate and simultaneously buys a
  new routing direction.
- **Twist vs siblings:** it separates two things the value-set representation
  fuses. Two states with identical materialized masks can have different B and
  therefore different continuation costs.
- **Measured performance:** the controlled experiment is the result — **same first
  ten masks, different routing: completion cost 108 vs 100 gates**, and the better
  routing was *uglier* by the naive expression metric (L: 146 → 156). Descent
  108 → 100 → 99 → 98 @ depth 4, then a saved artifact reached **the project's
  known 97 @ 3 gate-for-gate** from a weak greedy basin (a strong regression
  control). Demand-intersection greedy alone stalls at 108; a one-step exact fiber
  oracle only reaches ~105. Diagnostic finding: average outputs served per gate
  rises monotonically with circuit quality (97@3: 1.753 → 88@6: 2.773), and
  "cancellation debt" `V − 184` rises too (97@3 max 18 → 88s reach 74–106).
- **Cost:** not recorded in this slice.
- **Code:** **not in this slice** — described only in `new-representation.md`.
- **Logs/results:** `/home/joebachir20/xor_ui/slp-plateau-search/new-representation.md`
  §§1–14 (43 K).
- **Generality:** **CIRCUIT-GENERIC** — B is defined for any target matrix.
- **Phase-2 verdict:** **keeper, and the strongest single idea in the slice's
  documents.** It is the only method here with a *positive* control that the
  ordinary representation provably fails (the 108/100 experiment).

### frozen-exterior-module-search (backbone + ternary repair planes + defect graph)
- **Family:** structural-analysis / exact finite decision.
- **What it does:** freezes 61 of an 88's masks and treats the remaining 27 as a
  variable *module*; an 87 in that exterior is exactly a 26-mask module. Then
  exhaustively decides small module rewrites with arbitrary (not
  vocabulary-restricted) replacement gates.
- **Twist vs siblings:** it is the only method that produced a *structural
  classification* of the 88 plateau rather than a list of circuits.
- **Measured performance:** the 88 modules collapse to a **22-mask backbone plus
  five disjoint GF(2) repair planes**, giving exactly **3⁵ = 243** optimal modules;
  the 15 plane masks are provably *exactly* the complete one-step repair frontier
  of the backbone (15 of 4 459 constructible next gates make progress, and they are
  precisely those 15). Exact finite optimum over the 37-mask quotient = 27 (primal
  = dual). Negatives, all exhaustive within their scope: 22-backbone + any four
  arbitrary XOR gates cannot complete (all four first-progress branches closed,
  including the pathological one, via a six-component quotient over-approximation);
  85 293 arbitrary 2→1 descents from all 243 modules — zero; 5 346 backbone
  deletions + one arbitrary restore — zero; 8 910 and 56 133 deduplicated 2→2 cases
  — zero; 5 940 one-backbone+two-plane 87 shells — zero; **6 918 660** 3→3
  combinations in the 36-mask defect language — zero; 249/249 edge-containing
  arbitrary 3→3 backbone triples (with 15 zero-byte timeout placeholders re-run
  individually) — zero. Positives: verified **new 88 @ depth 6 circuits using masks
  outside the original 801-mask vocabulary**, an uphill 26→27→28→29 escape where
  the first gate made zero progress, real cross-defect sharing (a verified 89 @ 6
  with two backbone masks absent), and 4 valid double-backbone 89 modules.
- **Cost:** not recorded in this slice.
- **Code:** **not in this slice** — described in `new-representation.md`.
- **Logs/results:** `new-representation.md` §§15–64.
- **Generality:** **CIRCUIT-GENERIC method, instance-specific results.**
- **Phase-2 verdict:** **keeper as a method, superseded as an argument** — its
  every negative is a small-radius statement (see LEAD L1), and its explicitly
  open case (the 1 291 edge-free triples) was later closed elsewhere (LEAD L5).

### carrier-difference-census (the circle / C-D frame)
- **Family:** structural-analysis / algebraic representation.
- **What it does:** places the 32 inputs on a circle so byte rotation is a 90°
  turn; defines `Δ = I + R`; classifies every signal as a **carrier** `C_j` (still
  carries one absolute bit-lane identity) or a **difference** `D` (pure rotational
  information); and censuses each circuit as counts of `C+C→D`, `D+D→D`, `C+D→C`
  gates.
- **Twist vs siblings:** it is a *typing discipline* over masks, cheap to compute,
  and — used as a **population statistic** — it falsifies single-circuit theories
  in about a minute.
- **Measured performance (from the review, which re-derived everything):** exact
  and confirmed — `o_{r+8} = R(o_r)` for all 32 outputs; the 32 outputs form **5**
  rotation orbits (sizes 4/4/**16**/4/4); `Δ⁴ = 0` with ranks 32→24→16→8→0;
  **`M = I + LΔ + Δ³`** verified on all 32 basis vectors; the first 20 gates of the
  from-scratch 88 @ 5 are exactly **15 quarter-chords + 5 diameters**; exactly 24
  extraction events, 3 per lane, 20 immediate + `{g47,g51,g62,g63}` delayed; the
  four delayed lanes are exactly 0, 3, 4, 6; internal carriers per lane
  `(2,2,2,3,2,2,2,2)` = 17; exactly two cross-lane extraction vectors. Used as a
  population instrument it produced the refutations in LEAD L2.
- **Cost:** ~1 minute over the 58 143-circuit corpus.
- **Code:** review scripts described as throwaway but each result restated in
  full; `atlas/ring.py` holds the correct ring `GF(2⁸)[v]/(v⁴)`.
- **Logs/results:** `side_work.md`, `side_work_REVIEW.md` §1 and §2.
- **Generality:** **MIXED** — the C/D typing needs the target's lane structure;
  for `aes_inv_mixcolumns` the same circle and the same Δ apply (same Z/4).
- **Phase-2 verdict:** **keeper as an instrument, dead-end as a theory** — the
  review shows the theory generalises from a 0.25 % tail circuit.

---

## 3. ARTIFACTS (counts + labels)

### Verified circuits

| label | count | command | path |
|---|---|---|---|
| **canonical record circuits** (97@3, 92@4, 89@5, 88@5 ×2, 88@6, 88@7, 88@8) | **8** | `ls evidence/circuits/*.json \| grep -v spectrum \| wc -l` | `evidence/circuits/` |
| SHA-256 manifest of those 8 | 1 | `evidence/circuits/spectrum.json` | same |
| **provenance-labelled seed circuits** (2 imported, 3 derived, 4 own) | **9** | `ls pipeline/seeds/*.json \| wc -l` | `pipeline/seeds/` (table in `seeds/README.md`) |
| **imported prior-art circuits** (Jean 88, Sun–Yang–Li 89) | **2** | `ls evidence/campaign87_imported_prior_art/*.json` | that dir |
| reproduction outputs | 5 | `ls reproduce/out_*.json` | `reproduce/` — 88, 89, **91** (`out_90.json`, the irreducibility demo), 91, 97 |
| local pipeline run bests | 6 | `ls pipeline/runs_parallel/*/best_overall.json` | 89@5 ×3, 89@6, 97@3, 92@4 |
| ρ²-symmetric certificate circuits (2 exactly-symmetric 90s + orbit certs + union seeds/ancestors) | **9** | `ls evidence/campaign87_certificates/rho2_symmetric_90s/*.json` | all re-checked VALID |
| all JSON in the slice | 469 | `find evidence pipeline reproduce -name "*.json" \| wc -l` | — |

Depth-4 note: **the slice's own record set is one gate stale.** Two files
*outside* this slice re-verify at 91 @ depth 4 (see LEAD L4):
```
python3 verify_circuit.py campaign_87/cascade6/FRONTIER_91gates_depth4.json 4
python3 verify_circuit.py experiments/e4_depth/out/resched/atlas_compiled_m1_91gates_depth4.json 4
# both: gates=91 depth=4 outputs_built=32/32  VERDICT: VALID MixColumns circuit
```

### Certificates

| label | count / magnitude | what it certifies | path |
|---|---|---|---|
| certificate verdict JSONs | **147** (`find evidence/campaign87_certificates -name "*.json" \| wc -l`) | per-window / per-subject exact verdicts | `evidence/campaign87_certificates/` |
| exact window decisions, total | **≈165 M** | remove-k/restore-fewer, zero reducible | `CERTIFICATES.md` §4 table |
| circuits with **exhaustively empty k ≤ 3 shells** | **47 canonical** (Jean's 88 + 12 syl-siblings + family-3 anchor + 33 reps) **+ 2 from-scratch** (88@6, 88@5fs, logs in their run archives) | any 87 differs from each by ≥ 4 masks | `exact_k4/`, `family3_exact/`, `campaign87_run_*/certificates/` |
| population states swept at k=2 | **105 801 of ≈139 878** (51 899 fam 1–2 + 53 902 fam 3; family 3 is **100 % closed**) | any 87 differs from each by ≥ 3 masks | `pop_decider/`, `family3_exact/` |
| windowed-SAT window verdicts | **130** — Jean's 88: 48 windows → 44 UNSAT / 4 undecided / 0 SAT, frontier k=16; family-3 anchor: 50 → 37 UNSAT / 13 undecided; 8 reps: 32 → 25 UNSAT / 7 undecided; independent 88@7: 8 → 5 UNSAT / 3 undecided | UNSAT **relative to the encoding's fixed slot order** | `sat_deep/`, `loose_sat/`, `family3_sat/` |
| orbit-space local-optimality certs | 2 circuits (+1 at 91) | locally optimal under all remove-1-orbit and all **666** remove-2-orbit-add-≤1 moves | `rho2_symmetric_90s/cert90_*.json` |
| **decider validation records** | 25/25 + 12/12 brute-force; 1 257 instances @ 100 % incl. 122 NOs; **4 200/4 200** planted positives; 462/462 + 33/33 branch-isolated | that the completeness proofs hold | `exact_k4/full_test_{cpython,pypy}.log`, `METHODS.md` §10b |
| **control record (the repricing)** | 12 241 exhaustive k=2 + 8 400 sampled k=3 across 97/94/92/91/90/89/88 — all "irreducible" | that the certificates are **not** evidence about 87 | `METHODS.md` §10a, `CERTIFICATES.md` §7a, commit `23d80d7` |

### Writeups, ledgers, logs

| label | count | command | note |
|---|---|---|---|
| markdown writeups in the slice | **32** | `find evidence pipeline reproduce docs tests -name "*.md" \| wc -l` | + 5 at root (README, METHODS, and the 3 loose docs) |
| top-level narrative docs | 5 | — | `README.md` 14 K, `METHODS.md` 59 K, `evidence/RESULTS.md` 59 K, `CERTIFICATES.md` 18 K, `pipeline/README.md` 12 K |
| PROVENANCE.md (one per run archive + prior art) | 6 | `ls evidence/*/PROVENANCE.md` | each states derived/own/from-scratch in its **first sentence** |
| CODE_PROVENANCE.md + CONFIG_AS_RUN.md pairs | 7 each | `find evidence -name "CODE_PROVENANCE.md"` | every archive pins the exact code that produced it |
| append-only JSONL ledgers | **23** | `find evidence -name "*.jsonl" \| wc -l` | largest: `family3_sat/tasks_reps_raw.jsonl` 25 K, `family3_sat/results_anchor.jsonl` 24 K, `sat_deep/results.jsonl` 21 K |
| raw logs (`.log`/`.stdout`/`.out`) | **187**, **1.80 MB total** | `find evidence pipeline reproduce \( -name "*.log" -o -name "*.stdout" -o -name "*.out" \) \| wc -l` and `-printf "%s\n" \| awk '{s+=$1} END {print s}'` | largest: `parallel_ladder_run_2026-07-13/coordinator.log` 641 KB |
| dead stray root logs | 6 | `cat w1.nohup wsh*.log d3_b.out` | ≈700 bytes total, all "file not found" |

### Git map (requested)

```
git status --short | wc -l              -> 30 untracked entries
git ls-files | wc -l                    -> 629 tracked files
git status -sb                          -> ## main...origin/main [ahead 1]
git log --oneline origin/main..HEAD     -> 23d80d7
```

**Tracked (629 files) — the public repo:**

| top-level | tracked files |
|---|---|
| `evidence/` | **597** (certificates 201, 88@8 run 117, 88@7 run 79, cascade 60, parallel ladder 58, sub89 20, 88@5 derived 18, 88@6 fs 17, 88@5 fs 14, circuits 9, prior art 3, RESULTS.md 1) |
| `pipeline/` | 15 (4 modules, 2 READMEs, 9 seeds) |
| `reproduce/` | 5 | 
| `docs/` | 4 | 
| `tests/`, `.github/` | 1 each |
| root | `README.md`, `METHODS.md`, `CITATION.cff`, `LICENSE`, `verify_circuit.py`, `.gitignore` |

**Untracked (30 entries) — the entire post-publication campaign:**
`atlas/`, `beat88/`, `bi_mask_requested_evidence/`, `experiments/`,
`fleet1/`…`fleet12/` (12 dirs), `joe_depth3_audit/`, `wrapup/`,
`CHECK_SOLVER.sh`, `FLEET_PLAN.md`, `SESSION_PROMPT.md`, `side_work.md`,
`side_work_REVIEW.md`, `new-representation.md`, `d3_b.out`, `w1.nohup`,
`wshB1.log`, `wshB2.log`, `wshC1.log`, `wshC2.log`.

**Gitignored (present on disk, deliberately excluded):** `__pycache__/`, `*.pyc`,
`*.pyo`, `pipeline/runs_parallel/`, `pipeline/runs_smoke/`, `reproduce/out_*.json`,
`.pytest_cache/`, **`campaign_87/`** (29 GB), `.claude/`. Verified with
`git check-ignore -v`.

**The one unpushed commit — `23d80d7`, "Reprice the neighbourhood certificates:
they are not evidence about 87"** (2026-07-30, +236 lines across `METHODS.md`,
`evidence/RESULTS.md`, `CERTIFICATES.md`; no code, no verdict log, no count
touched). It adds §§10a–10c and the dated scope paragraphs. **This is the single
most consequential unpublished thing in the tree**: the public repo currently
serves certificate claims *without* the scope note that says they carry no
evidence about 87. Pushing it is a correctness fix to the public record, not a
cosmetic one.

---

## 4. KEEP / DELETE proposal

**KEEP — everything tracked (629 files, ~7.5 MB).** It is the published repo:
result circuits, untouched run archives with pinned code, certificate verdicts,
and the narrative. Nothing here is regenerable.

| item | verdict | why | size |
|---|---|---|---|
| `verify_circuit.py` | **KEEP — highest priority** | the oracle; every claim in every slice is defined by it | 4.9 K |
| `evidence/` (all 11 subdirs) | **KEEP** | records, certificates, untouched archives, prior art | 4.9 M |
| `pipeline/` code + `seeds/` | **KEEP** | the engine that found every record; seeds carry per-file provenance that cannot be reconstructed | ~150 K |
| `reproduce/` code | **KEEP** | frozen v1 per-method code — the only surviving statement of what the records were originally obtained with | ~50 K |
| `tests/`, `.github/` | **KEEP** | the differential kernel tests are what make the engine's negatives believable | ~30 K |
| `docs/` generators + SVGs | **KEEP, but regenerate** | encodes the stale 92@4 frontier (LEAD L4); `FRONTIER = [(3,97),(4,92),(5,88)]` at `docs/generate_frontier_svg.py:62` | 108 K |
| `README.md`, `METHODS.md`, `CITATION.cff`, `LICENSE` | **KEEP, edit** | see §5 for the stale claims | 75 K |
| `side_work.md`, `side_work_REVIEW.md`, `new-representation.md` | **KEEP — do not treat as scratch** | two substantial structural analyses + the project's own referee review; the review is reusable methodology | 83 K |
| `FLEET_PLAN.md`, `SESSION_PROMPT.md` | **KEEP** | the campaign's design laws and the standing brief; `FLEET_PLAN.md` §"Design laws" is a distilled measured-negatives list worth publishing | 11 K |
| `CHECK_SOLVER.sh` | **KEEP while laneCUBE runs; DELETE-CANDIDATE after** | operational status script for the live k=14 solve; hardcodes absolute paths | 1.8 K |
| `pipeline/runs_parallel/` (6 folders) | **KEEP + note** | gitignored local re-validation runs from 2026-07-16; small, and they are the on-disk evidence for the "re-validated 2026-07-27" timings quoted in the READMEs. Regenerable in principle, cheap to keep | 1.9 M |
| `reproduce/out_*.json` (5) | **KEEP + note** | gitignored outputs; all oracle-checkable, all regenerable in seconds-to-minutes | ~20 K |
| **`__pycache__/` ×7** (root, pipeline, reproduce, tests, docs, certificates/code, .pytest_cache) | **DELETE-CANDIDATE** | pure build scratch, gitignored, regenerates on first run. Includes stale `cpython-310` and `pypy311` artifacts | **~688 K** |
| **`w1.nohup`, `wshB1.log`, `wshB2.log`, `wshC1.log`, `wshC2.log`, `d3_b.out`** | **DELETE-CANDIDATE — confirmed dead** | each is one line: "file not found" for a script that no longer exists (`worker.sh`, `satfix_hunt.py`, `satfix_hunt2.py`, `deep_extras.py`) | **~700 B** |
| `pipeline/runs_smoke/` | n/a | gitignore entry only; directory does not exist | 0 |

**Total reclaimable from this slice: ~690 KB.** That is the honest number — this
slice is not where the disk is. (`campaign_87/` alone, outside the slice, is
29 GB.)

---

## 5. LEADS (sharp-eye findings)

### L1 — The certificate repricing is the project's most important negative, and it is unpublished. **VERIFIED-IN-LOG.**
Commit `23d80d7` is one commit ahead of `origin/main`. It records that the exact
decider returns "irreducible" on **97 @ 3, 94 @ 4, 92 @ 5, 91 @ 5, 90 @ 5,
89 @ 9 and Jean's 88 @ 7 alike** — 12 241 exhaustive k=2 windows, 8 400 sampled
k=3, zero reducible across all of them. Measured cause: over 45 circuits with a
known-smaller circuit available, the distance to it is **median 42 masks, min 3,
max 48; 44 of 45 need k ≥ 8**, against a certified radius of 3. **Every
"exhaustive, zero reducible" claim anywhere in this tree inherits this**, including
`side_work.md` §§10/18/21/22/26 and `new-representation.md`'s 6.9 M and 2.5 M
mutation sweeps. Implication for phase 2: *a negative at radius ≤ 4 is worth
nothing; the SAT frontier at k = 16 is the only instrument in the slice operating
in the regime where transitions actually live.* Action: push the commit.

### L2 — The single most reusable methodological move in the slice: measure the claim on the population before theorising. **VERIFIED-IN-LOG.**
`side_work_REVIEW.md` §§2.1–2.4 and §4.3 killed four load-bearing claims of a
30-section theory in about a minute of compute, by censusing **58 143 distinct
88-gate value-sets**:
- "the 88 never mixes two absolute bit identities" — **false for 28 % of known
  88s** (41 874 quotient-pure / 14 800 with one mixed mask / 1 469 with two). The
  repo's own from-scratch 88 @ 6 has `g41 = C_1 ⊕ C_2`. So the "quotient-pure
  class" the theory was built to prove things about excludes a quarter of the
  plateau, with no evidence the excluded ones are worse.
- "88 = 24+15+17+32" — the pure-D count is **35 at the mode**; 39 occurs in
  **148 of 58 143 (0.25 %)**. The theory generalises from a rare tail *in exactly
  the coordinate it is built on*. Across the five record 88s the extraction count
  is 23–26 and the D/C split moves by 6 gates.
- the "1D ↔ 1C" balance is the identity `n − 32 = 56`, true at 89, 92 and 97 too.
- the "eerily exact" reuse identity holds in 2 of 4 measurable cases.
**This is a phase-2 discipline, not a one-off**: any structural claim about "the
88" should be quantified over ≈140 000 states first. It is cheap and it has a
100 % hit rate so far.

### L3 — There is no such thing as "the 88", and the least-certified circuit is the most interesting one. **VERIFIED-IN-LOG.**
≈139 878 known distinct 88-gate states, ≥5 families, plain Jaccard as low as
0.285 between the from-scratch 88 @ 5 and the 88 @ 7. `CERTIFICATES.md` §4 states
it against itself: **all 47 exhaustively-certified canonical circuits lie in
Jean's lineage**, and *the one circuit independent of that lineage — the project's
own 88 @ 7 — is precisely the least certified*: not among the 47, no exhaustive
k ≤ 3 sweep ever run, 9 exact k=4 windows and 8 SAT cone windows total. The gap
narrowed (88@6 and 88@5fs got exhaustive k ≤ 3 shells, from-scratch lineage) but
**the 88 @ 7 still has no exhaustive shell at any radius**, and the derived 88 @ 5
has only a k=2 log (`campaign87_run_2026-07-29_got_88at5_derived/certificates/`
contains `k2_shell_88at5.log` and no k3). Under L1 this matters less than it once
did, but it is the cleanest remaining asymmetry in the certificate corpus.

### L4 — README, RESULTS, the frontier SVG and CI all state a stale depth-4 record. **VERIFIED-IN-LOG (I re-ran the oracle).**
`README.md:9` and `evidence/RESULTS.md:1` publish "**verified frontier: 97 @ 3,
92 @ 4, 88 @ 5**". The depth-4 point is wrong by one gate and has been for months:
```
python3 verify_circuit.py campaign_87/cascade6/FRONTIER_91gates_depth4.json 4
python3 verify_circuit.py experiments/e4_depth/out/resched/atlas_compiled_m1_91gates_depth4.json 4
# both -> gates=91 depth=4 outputs_built=32/32  VERDICT: VALID MixColumns circuit
```
`experiments/e4_depth/RESULT.md` reports **15 912 distinct verified-realizable
91-gate depth-4 mask sets** in the repo (plus 214 at 92@4), that all 15 683
census members have exactly 91 *live* gates (no dead-gate defect), and that
**three genuinely distinct lineages** hold 91 @ 4 (cascade6, m3_census, and
`atlas/compiled_m1.json` — which is *filed as depth 5* and reschedules to depth 4
free, Jaccard 0.433 / 0.358 to the other two). `FLEET_PLAN.md` Lane D item 4
lists "E4's 91@4 supersedes 92@4 — records repo/README update" as an outstanding
chore; it was never done. Affected artifacts in **my** slice:
`README.md` (lines 9 and 13, plus the SVG alt-text), `evidence/RESULTS.md`
(title + §2), `docs/generate_frontier_svg.py:62` (`FRONTIER = [(3,97),(4,92),(5,88)]`)
and `docs/frontier.svg`, `evidence/circuits/` (no 91@4 file, no `spectrum.json`
entry), `.github/workflows/verify.yml` (verifies 92@4, not 91@4), and
`tests/test_invariants.py::test_directory_holds_exactly_the_eight_records`
(pins the record set at eight). **This is the highest-priority factual fix in the
slice and it improves a published result.**

### L5 — Both loose root documents' explicit "where I stopped" questions WERE followed up. **VERIFIED-IN-LOG.**
Recording this so nobody re-runs them:
- `new-representation.md` §59 leaves **1 291 pairwise-edge-free backbone triples**
  open under unrestricted 3→3. `atlas/thinktank/phase2_finisher.md` is exactly
  that finisher, and reports "**All 1 540 = C(22,3) backbone triples of this
  geometry are dead**" (1 540 at one plane state, 2 916 tier-1 across all 243 plane
  states, 4 941 tier-2). `FLEET_PLAN.md` design law 2 cites it as settled.
  `atlas/thinktank/enabling_gates.md:198` discusses the 1 291 directly.
- `side_work_REVIEW.md`'s recommendation 1 (**N1: put `t = 1 + y⁻¹` into
  `atlas/ring.py`**, where MixColumns is `[01 02 00 01]` — three terms, unit
  coefficients, **`t²` vanishes**) was followed up in
  `atlas/thinktank/transposed/tring.py` + `atlas/thinktank/transposed_frame.md`
  and `experiments/e14_plateau87/basis/zframe_T.py` + `laneBASIS.md`.
  **Not verified by me whether the vanishing `t²` actually shrank any table** —
  that belongs to the atlas slice.

### L6 — Two of the review's five recommendations appear NOT to have been followed up. **PLAUSIBLE.**
`side_work_REVIEW.md` "Recommended next moves" items **3 and 4** are:
3. *"Re-price gauge choices in gates rather than rank, inside the atlas's σ
   framework"* — the review calls the gauge freedom of §13 "**the one thing here
   the atlas frame does not have an explicit version of — it is aimed at the wrong
   objective, not a bad idea**", and calls "rank is not cost" the best sentence in
   the document. I found no `gauge`-named artifact in `atlas/` (the listing has
   `sigma_*`, `sectors`, `economy.py`, `valuation.py`, no gauge pricing).
4. *"Re-run §23's Pareto rows 3–4 and reconcile with the dual solve in §2.5"* —
   the review's independent dual solve reproduces rows 1–2 exactly (rank 24 → 8
   roots, forced; rank 23 → 10 roots) but reaches only **15** roots where the
   document claims 12 at rank 22, and **never reaches** rank 21 at all. The review
   explicitly says rows 3–4 are "**not refuted — but neither are they
   confirmed**", and asks for the code. There is no reconciliation artifact.
Confidence PLAUSIBLE because I only grepped for names, and both would live in the
atlas/experiments slices. Worth one grep from whoever owns those. Item 3 is a
*positive* lead: an unexplored design variable that the project's most productive
frame does not currently model.

### L7 — The certificate frontiers are all still resumable, and the progress files are on disk. **VERIFIED-IN-LOG.**
`CERTIFICATES.md` "Where the full logs live" lists five resumable frontiers as
being in "the raw 2.8 GB campaign archive … not included in this repository". All
five exist right now under the (gitignored, 29 GB) `campaign_87/`:
```
campaign_87/agents/pop-decider/work/results_pop/pop_progress.jsonl        5.0M   (33 090 states left, ~2.9 h)
campaign_87/agents/pop-decider/work/results_popk3/k3_progress.jsonl       4.0K   (181 selected states left)
campaign_87/agents/family3-exact/work/results_f3/f3_progress.jsonl        5.2M   (closed)
campaign_87/agents/exact-k4/work/results_k4/progress.jsonl                1.4M   (334 605 k=4 windows left on Jean's 88)
campaign_87/agents/family3-exact/work/results_k4_f3/progress.jsonl        896K   (346 858 left on the f3 anchor)
```
Plus 4 + 20 undecided SAT windows in `campaign_87/agents/{loose-sat,family3-sat}/runs/`.
**Do not delete `campaign_87/` without extracting these five files.** Under L1 the
k=2/k=3 continuations are not worth CPU; the **k=4 frontiers and the 24 undecided
SAT windows** are the parts that operate at a useful radius.

### L8 — A timeout that was correctly not counted, and never revisited. **SMELL.**
`new-representation.md` §24: a "572-ish mask global MILP built from the most
universally relevant repair masks became solver-hard and did not produce a
trustworthy global result. **I did not count that timeout as evidence.**" Correct
discipline — and it means a bracket was banked and dropped. The same document
notes the repair searches touched **2 288 distinct arbitrary masks of which 1 905
had never appeared in the original 801-mask proposal universe** — a measured
demonstration that the search language was excluding most of the algebraically
relevant structure. Whether the vocabulary lesson was ever fed back into the
pipeline's rebuild pool I could not determine from this slice.

### L9 — Structure shared by circuits at 88 that the slice actually measures. **VERIFIED-IN-LOG.**
Assembling what this slice contains on "why 88 keeps appearing":
- **the elite basin is 79–81 % ρ²-symmetric**, and its 12 ρ²-fixed masks are
  exactly the (x0^x2)/(x1^x3) sharing trick, *rediscovered by search, not imposed*
  (`METHODS.md` §11). Jean's 88 is 75 % ρ²-symmetric — a second, distinct symmetric
  basin.
- **all five 88s were found in walk chunks, none in an LNS chunk**, and both
  from-scratch ones came from `alt` workers ~19 h into a restart. Descent is not
  what produces an 88; lateral motion plus a depth tie-break is.
- **the symmetric basins are extremely rigid**: all 666 remove-2-orbit-add-≤1
  moves fail on both exactly-symmetric 90s, and "all progress came from union
  crossings" (`CERTIFICATES.md` §8). Crossing beats editing at the frontier — which
  is the same finding as `FLEET_PLAN.md` design law 2 ("no editing/walking lanes").
- **quality correlates with waste, monotonically**: outputs served per gate rises
  97@3 → 88@6 (1.753 → 2.773) and cancellation debt rises with it (max 18 → 106).
  The 97 @ 3's construction trajectory is *completely greedy* in expression mass;
  the from-scratch 88 @ 5 contains **six moves that make it worse**, one by ~6
  occurrences (`new-representation.md` §§5–6). This is the measured version of the
  standing brief's "the score lies", and it is the only *predictive* structural
  signal in the slice.

### L10 — A dangling documentary inconsistency worth one minute. **SMELL.**
`reproduce/README.md` says the pipeline's shipped `hunt87` worker set aims at
"the three 88-gate family anchors this set ships", explicitly *excluding* the two
from-scratch families, and points at
`evidence/circuits/mixcolumns_88gates_depth6.json` and
`..._depth5_fromscratch.json` as the anchors you would have to add by hand. Those
two are the only 88s with **both** exhaustive k ≤ 3 shells **and** Jean-independent
lineage — i.e. the shipped hunting configuration points at the *derived* families
and not at the clean ones. Harmless while nothing is running, but if any phase-2
work reuses `--mode fixed`, this is the wrong default.

---

## 6. HAZARDS

- **`CHECK_SOLVER.sh` is operational, references the LIVE lane, and hardcodes
  absolute paths.** It reads `fleet11/laneCUBE/{found,logs}`, `experiments/STOP`,
  `experiments/FOUND_*.json`, and `verify_circuit.py`, and it `pgrep`s for
  `mono.py` filtered by cwd containing `fleet11`. **Do not move
  `verify_circuit.py` or the repo root while the k=14 solve runs.** (The script
  only reads and never signals — it is safe to run, and it is the sanctioned way
  to check the live solve.)
- **`verify_circuit.py` must not move.** It is referenced by absolute or
  root-relative path from: `.github/workflows/verify.yml`, `tests/test_invariants.py`
  (`ROOT = Path(__file__).resolve().parents[1]`), `pipeline/README.md`,
  `pipeline/seeds/README.md`, `reproduce/README.md`, `evidence/RESULTS.md`,
  `CERTIFICATES.md`, `CHECK_SOLVER.sh`, `SESSION_PROMPT.md`, and — per grep —
  effectively every RESULT.md in every fleet/experiment lane. Moving it breaks
  the definition of "verified" tree-wide.
- **`evidence/*/` run archives are declared UNTOUCHED evidence.** `README.md`
  states the logs/statuses/bests/`code/` are never edited or regenerated and stay
  byte-identical to what the run produced; only `PROVENANCE.md` (commentary) is
  maintained, and only with a dated note. Any reorganisation must preserve them
  byte-for-byte.
- **`reproduce/mixcolumns_core.py` is byte-identical to `pipeline/mixcolumns_core.py`
  by design**, and `reproduce/README.md` publishes the `diff` as a claim. Do not
  deduplicate them into a shared module without updating that claim.
- **`campaign_87/` (29 GB, gitignored) holds the only copies of the five resumable
  certificate frontiers** (paths in L7) and of `cert_audit/` (the scripts behind
  `METHODS.md` §§10a–10c) and `cascade6/FRONTIER_91gates_depth4.json` (a record
  circuit not in `evidence/`). Extract before any deletion.
- **`docs/*.svg` are generated**, not hand-drawn — edit the generators, not the SVGs.
- **`.gitignore` excludes `campaign_87/` and `.claude/`** — anything a
  reorganisation moves *into* those paths silently leaves the repo.
- Nothing in this slice is written by a running process. `pipeline/runs_parallel/`
  is dormant (last write 2026-07-29).

---

## 7. GAPS

- **No CPU spent on re-verification.** I ran `verify_circuit.py` on exactly 3
  files (two 91 @ 4 candidates and one control). The 8 record circuits, 9 seeds
  and 9 certificate circuits are reported as VALID **on the authority of
  `evidence/RESULTS.md`, `CERTIFICATES.md` and the CI workflow**, not from my own
  run. Bulk re-verification is cheap (< 1 min for all 26) but the brief forbids it.
- **`METHODS.md` read partially.** I read its section index and §§6, 8, 9, 11 in
  full. §§1–5, 7, 10–10c, 12–13 I have only via the derived documents
  (`CERTIFICATES.md`, `pipeline/README.md`, commit `23d80d7`). If a stale claim
  hides in §§1–5 or §§12–13 I would not have seen it.
- **`evidence/RESULTS.md` read partially** — head (78 lines) plus its section
  index. Sections 3–8 (per-record lineage narratives) were sampled through the
  `PROVENANCE.md` heads rather than read.
- **L6 is a grep-level finding only.** I did not read `atlas/` or `experiments/`
  contents (other slices). "Gauge pricing was never done" rests on the absence of
  a gauge-named artifact in an `ls` of `atlas/`, which is weak evidence.
- **Track record of the *campaign-era* fleet is under-measured.** The two
  from-scratch 88s came from "restart 18, 18.96 h in" and "session 5, restart 16,
  19.22 h in" of a 16-process fleet. I could not recover from this slice how many
  restarts/sessions ran in total, so **the hit rate of the from-scratch method is
  unknown** — I have two successes and no denominator. The denominators are in the
  raw campaign archive.
- **Windowed-SAT and orbit-engine code are not in this slice**, so their method
  entries are written from their logs and from `CERTIFICATES.md` / `METHODS.md`
  §11. Their generality assessments are inferences from the descriptions.
- **I did not price the k=4 / undecided-SAT continuations in CPU-hours**; L7 gives
  the remaining window counts but the per-window cost varies by two orders of
  magnitude (28 s to 1 509 s) and I did not sample the progress files.
- **`side_work.md` §14 (the 26-XOR reduction star) cannot be checked** — the
  review says the target set is never specified, so neither the 28 nor the 26 is
  verifiable from the document. It remains an unverified claim of a real
  submap improvement.
