# Slice report: fleet9 / fleet10 / fleet11 / fleet12

Agent model: Opus 5 (1M). Date: 2026-08-29. All paths absolute-from-repo-root
`/home/joebachir20/xor_ui/slp-plateau-search/`; commands are run from there
unless a `cd` is shown.

**Summary.** This slice is 10.5 MB and 1 579 files across four fleets, and it is
the most *document-dense* part of the repository: 32 markdown files totalling
1.05 MB, of which `fleet12/laneAUDIT/AUDIT.md` (188 K, 244 audited rows, 22
registered defects) and `fleet12/laneALGO/ALGORITHM.md` (88 K, certified by four
independent naive-reader reviews) are the two documents the public repo pages
should be distilled from. Three of the four fleets are exceptionally
well-documented; **fleet10 is completely opaque** — an undocumented from-scratch
clean-room reimplementation that reached 93 gates with no RESULT.md anywhere in
the tree, and it is the single most valuable *calibration* datum in the slice
("an independent effort with no project knowledge reaches 93; the project's
record is 88"). fleet9/laneENUM measured the 88-plateau's shape and produced the
slice's sharpest structural fact — **the 88s are a population of interfaces, 13
of 17 blocks have a unique optimum, and the record is a depth record disguised as
a gate record**. fleet11/laneCUBE is LIVE (20 processes) and holds the k=14 joint
SAT test with its cost inversion (monolithic solving is 7.2× *cheaper* than
cubing) and its four-part correctness audit. fleet12 was the audit-and-mutate
campaign: every one of ~200 mutations across six lanes returned exactly 88, with
mechanisms, and it corrected one published number (89 → 88) downward.
**26 distinct methods catalogued. 6 leads.** Three of the leads are live stale
tallies — banked compute that landed *after* its lane's RESULT.md was written and
has never been folded in (fleet9: 72 extra ledger rows and ~84 wall-hours of U3
enumeration; fleet11: k=14 coverage is now **87/528**, not the documented 51;
fleet12/laneF1: 13 extra result rows that measure the plateau's upper cliff
directly instead of by inference).

---

## 1. INVENTORY

```
fleet9    3.3M   1 lane, 573 files   — laneENUM: how big is the 88 class, and what shape is it?
fleet10   832K   1 lane, 151 files   — cleanroom: from-scratch reimplementation. NO WRITEUP.
fleet11   880K   1 lane,  56 files   — laneCUBE: the k=14 joint SAT test. LIVE.
fleet12   5.5M   8 lanes, 799 files  — the audit + one-mutation-per-run campaign
```
`du -sh fleet9 fleet10 fleet11 fleet12` · `find fleet9 fleet10 fleet11 fleet12 -type f | wc -l`

### fleet9/laneENUM — 3.3 M — **well-documented** (`RESULT.md`, 33 K)

| subdir | size | what it is |
|---|---|---|
| `code/` | 276 K | 28 files: the two independent set-enumerators (`enumlib.py` DFS, `satenum.py` SAT set-blocking), the ban instrument (`satban.py`), five controls, three instance builders, the census (`census.py`, `census2.py`, `condrig.py`, `shape.py`), the ρ-symmetry proof (`rho_equivariance.py`), the oracle path (`materialise.py`, `sample.py`), and `tally.py` which re-derives every number in `RESULT.md` |
| `code/imported/` | — | the **historical** k≤3 irreducibility instrument (`exact_window.py`, `exact_driver.py`, `pop_scan.py`) byte-copied read-only from `campaign_87/agents/exact-k4/work/` so the equivariance test runs against the real thing |
| `inst/` | 84 K | three instance files (`v2_records.json` = the 14 known 88s' configurations) |
| `logs/` | 64 K | 13 run logs |
| `results/` | 2.1 M | `TALLY.txt` (the frozen tally), 4 census JSONs, 5 control JSONs, `v2_counts.jsonl` (111 rows), `sat_counts.jsonl` (116 rows), `sample.json`, `circuits/` (223 verified 88s), `sets/` (233 per-cell enumerated mask-set banks, 852 K) |
| `snapshot/` | 720 K | a frozen copy of `fleet8/unified` taken before any work, with its `REPO` constants patched — **the only copy of that code state anywhere; nothing under fleet8–12 is git-tracked** |
| `ledger.jsonl` | 112 K | 270 rows, hash-chained, 26 distinct `kind`s |

### fleet10/cleanroom — 832 K — **OPAQUE: no RESULT.md, no README, no reference anywhere in the tree**

| subdir | size | what it is |
|---|---|---|
| `spec/` | 8 K | `targets.json` (the 32 MixColumns masks as hex) and `verify.py` — **byte-identical to the repo's `verify_circuit.py`** (`md5 682053357d0d873b6dee527e74b83826`), i.e. a copy for self-containment, *not* an independent verifier |
| `work/` | 824 K | 5 C sources + 6 compiled binaries (`bp` … `bp5s`, randomized Boyar–Peralta search), 8 Python SAT-repair scripts, 2 shell drivers (`migrate.sh` island migration, `collect.sh` best-of harvest), 63 circuit JSONs, **67 logs (104 K)** |

The C targets were spot-checked against the spec (`TGT[0] = 16875904 = 0x01018180`
= `targets[0]`), so the search really did aim at MixColumns. `work/FINAL.json`
verifies: `gates=93 depth=7 outputs_built=32/32 VERDICT: VALID`.

### fleet11/laneCUBE — 880 K — **well-documented** (`RESULT.md`, 21 K) — **LIVE, READ-ONLY**

| subdir | size | what it is |
|---|---|---|
| `code/` | 9 files | `cube16.py` (the retargeted e7 cube driver), `inst16.py` (instance assertions), `mono.py` (monolithic solve), `sat_compile.py` (the SAT-branch rehearsal), `report.py`/`mkresult.py` (re-tally), `controls.py`, `agree.py`, `probe.py`, 4 phase shell scripts |
| `cubes/` | 508 K | 6 append-only cube banks + 6 `.DONE` markers |
| `inst/`, `found/`, `results/` | 2 K | the pinned instance, the C2 positive-control hit, `laneCUBE_88gates_d7.json` (the C7 rehearsal's verified 88) |
| `logs/` | 8 K | 16 files, four of them the **currently-open** monolithic portfolio logs (0 bytes — the solvers have not finished) |
| `ledger.jsonl` | 26 K | append-only, includes the pre-registration |

### fleet12 — 5.5 M — **well-documented throughout**; every lane has PREREG + RESULT + PATCHES

| lane | size | what it is |
|---|---|---|
| `LIBRARY.md` | 34 K | **the catalogue of 25 swappable axes** with mechanism, tractability guard, verdict and cost each. Its scoreboard predates laneKNOBS and laneF1 and is therefore stale (see LEADS L4) |
| `laneAUDIT/` | 424 K | 6 documents. `AUDIT.md` is the merged refereed audit: **244 rows**, 47 ABSOLUTE FACT / 116 MUTABLE load-bearing / 81 inert, a **22-entry defect register** (5 at severity 1), and a 17-item ranked successor list. `AUDIT_{CORE,DATA,ENGINE}.md` are the three source audits; `SFLAGS_VERIFIED.md` re-checks five standing claims; `TEMPLATE.md` is the audit schema |
| `laneALGO/` | 220 K | `ALGORITHM.md` (88 K, 1 496 lines) — the certified plain-language algorithm — plus **four rounds of independent naive-reader review** (`NAIVE_READER_REPORT{,_v2,_v3,_v4}.md`); round 4 verdict: PASS with two errata, after the reviewer reimplemented the document's mathematics from the prose alone and every stated value matched |
| `laneHINTS/` | 240 K | audit ranks 2+3 bought: the ten inherited floors re-solved unhinted. 43 result rows, 5 emitted circuits, 4 pristine backups |
| `laneHALO/` | 528 K | axis 3: 12 block-boundary widenings. 118 result rows, 11 emitted circuits, 25 logs. Two **deadlocked-but-not-killed** generator PIDs still hold log handles here |
| `laneORDER/` | 1.3 M | axis 4: all **75** legal block orders. 75 result rows, 75 emitted circuits (**all one md5**), 79 logs, a supply-provenance probe |
| `laneKNOBS/` | 1008 K | axes 6/7/8/9/14/15: 65 pre-registered runs, 57 emitted circuits, 80 logs, 5 solve-cache banks, `derive_out/` |
| `laneF1/` | 1.5 M | axis 12 (the currency menus, flag F1): 64 result rows, 51 emitted circuits, 109 menu JSONs, 72 logs, two no-solver instruments (`diffcheck.py`, `famcheck.py`) |
| `laneLIB/` | 412 K | the six permanent instrument fixes B1–B6 + `LIBRARY.md` itself; `pristine/` holds 13 pre-edit copies of fleet8 files |

File-type breakdown for the slice: 32 `.md` (1.05 M) · 374 logs (`.log`/`.out`/`.nohup`, 923 K) · 5 pycache dirs (252 K) · 6 compiled C binaries (143 K).

---

## 2. METHODS

### sat-cube-and-conquer-on-gate-0
- **Family:** SAT-joint-levels.
- **What it does:** Decides whether a merged 16-dimensional block can be built in
  exactly *k* XOR gates, by splitting the one SAT question into 528 independent
  ones — one for each possible choice of which two inputs the circuit's *first*
  gate reads. Each piece is solved separately and its answer written to disk
  immediately, so a crash or reboot loses only the pieces in flight. The level is
  declared impossible only when all 528 pieces come back impossible.
- **Twist vs siblings:** It is the plain monolithic SAT solve (`sat-monolithic-portfolio`)
  cut into resumable slices. The partition is taken from *the CNF's own variables*
  (`_pairs_upto(m)` = C(33,2) = 528), not from an external idea of which pairs are
  allowed, and the exhaustiveness of the partition is **machine-checked before
  every dispatch** — including asking the solver, not assuming, that forcing two
  cubes at once is UNSAT and forcing none is UNSAT.
- **Measured performance:** k=9, 10, 11 swept 528/528 UNSAT, agreeing with fleet8's
  independent CNF encoding at every level either has decided. **k=14: 51/528 UNSAT
  at write-up, 87/528 UNSAT as of 2026-08-29 (re-counted, see LEADS L1), 0 SAT,
  UNDECIDED.** k=15: 23/528 UNSAT under a 60 s budget — reported as nothing. The
  headline measurement is the **cost inversion**: 528 cubes cost 18 540 core-s at
  k=11 against **218 core-s** for one monolithic solve — **85×** — and against
  fleet8's banked runs 2–3×. Grouping 33 cubes per solver recovers 2.3× of that
  (12 902 → 5 631 core-s, validated 528 compared / 0 disagreements). Extrapolated
  true price of k=14: **653–1 113 core-hours, and the cheapest route does not
  parallelise.**
- **Cost:** 16.68 core-hours banked in cube files (`RESULT.md` §7.4), plus 5 980
  core-s of monolithic solves, plus ~288 core-hours currently burning in the live
  portfolio (4 processes × ~72 h). Inherited free and never re-run: k=12 (11.6
  core-h) and k=13 (**233.5 core-h**).
- **Code:** `fleet11/laneCUBE/code/cube16.py` (a retarget of `experiments/e7_push/code/cube.py`), `code/inst16.py`, `code/report.py`, `code/mkresult.py`, `code/phase*.sh`.
- **Logs/results:** `fleet11/laneCUBE/cubes/*.jsonl` (508 K), `logs/` (16 files), `ledger.jsonl` (26 K), `RESULT.md`.
- **Generality:** **CIRCUIT-GENERIC.** The driver reads an *instance file* rather than building one; pointing it at `aes_inv_mixcolumns` means writing a pre-flight that emits the same `{r, in_vals, tgt_vals}` object. Everything else (`slp_opt.Instance`, `build_cnf`, `_sat_worker`) is imported unchanged.
- **Phase-2 verdict:** **keeper, with the price tag attached.** It is the right instrument when you need resumability or a per-cube SAT lottery; it is the wrong one if you just want the verdict — §7.3/§8 say so in numbers.

### sat-monolithic-portfolio
- **Family:** SAT-joint-levels.
- **What it does:** Hands the *identical* CNF to four different complete SAT
  solvers, one core each, and takes whichever finishes first. Because all four are
  complete, whichever answers first gives a sound verdict.
- **Twist vs siblings:** No decomposition at all — the opposite bet from cubing.
  It buys the measured 7.2×–28.8× cost advantage over cubing, and pays for it by
  losing everything if killed.
- **Measured performance:** k=11 UNSAT in 218 core-s; k=12 UNSAT in 5 762 core-s
  (26.4× growth). Four k=14 processes have been running **3 days** with no verdict
  and **zero bytes of log output**.
- **Cost:** cadical195 / cadical300 / kissat404 / glucose42, 1 core each, ~288 core-hours spent so far.
- **Code:** `fleet11/laneCUBE/code/mono.py`.
- **Logs/results:** `fleet11/laneCUBE/logs/mono_14*.log` (all 0 bytes — a solver that has not spoken).
- **Generality:** CIRCUIT-GENERIC (same instance-file interface as above).
- **Phase-2 verdict:** **keeper.** Cheapest known route to a hard level; the honest framing is "buy it as a portfolio and expect weeks".

### sat-witness-compile (the SAT-branch rehearsal)
- **Family:** SAT-joint-levels / plumbing control.
- **What it does:** Takes a block-level SAT witness and pushes it all the way
  through the production generator to a full 32-output circuit, verified twice by
  the repo oracle — so that if the decisive solve ever *does* say SAT, the path
  from "witness" to "verified circuit" is already known to work.
- **Twist vs siblings:** It is a **control on the success branch**, which almost
  nothing else in the repository has. It was run on a real 15-gate witness
  (constructed from the replay bound) and emitted a verified **88 at depth 7**,
  confirming the arithmetic 88 − 15 + 14 = 87 end to end.
- **Measured performance:** handover checks passed, model price 88, 88 gates at
  depth 7, `verify_circuit.py` VALID twice (rc 0/0).
- **Cost:** minutes.
- **Code:** `fleet11/laneCUBE/code/sat_compile.py`.
- **Logs/results:** `fleet11/laneCUBE/results/laneCUBE_88gates_d7.json`.
- **Generality:** MC-HARDCODED (it routes through `fleet8/unified`'s generator).
- **Phase-2 verdict:** **keeper as a discipline** — rehearse the success branch before you need it.

### cnf-partition-machine-check
- **Family:** SAT correctness control.
- **What it does:** Before any cube is dispatched, checks *on the real CNF* that
  the 528 cubes really do partition its models: the count is C(33,2); the
  enumerated pairs are exactly the input pairs in the solver's own key order; the
  at-least-one clause is literally present in `cnf.clauses`; and — asked of the
  solver rather than assumed — forcing two cubes is UNSAT and forcing none is UNSAT.
- **Twist vs siblings:** Most decomposition arguments in this repository are prose.
  This one aborts the run if it fails, and re-runs at every k.
- **Measured performance:** passed at every level the lane ran; the check output is
  banked in the ledger under `kind="cube_start" → partition_check`.
- **Cost:** seconds per level.
- **Code:** `partition_check()` inside `fleet11/laneCUBE/code/cube16.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.** Cheapest possible insurance against the classic decomposition bug.

### canonical-dfs-set-enumeration
- **Family:** exhaustive enumeration / structural analysis.
- **What it does:** For a small sub-problem, lists **every distinct set of
  intermediate values** of a given size that can be built from the inputs and
  covers the targets — not every program, every *set*, so two orderings of the same
  values count once. Duplicate-freeness comes from a canonical order (repeatedly
  take the numerically smallest currently-buildable value), which gives exactly one
  search path per set.
- **Twist vs siblings:** counts *sets*, not programs, and prunes with the
  Boyar–Peralta δ bound, which is a relaxation and therefore removes no solution.
- **Measured performance:** 82/82 record blocks decided; **the record's own block
  value-set was found in every one** ("RECORD BLOCKS NOT REACHABLE: []"). Passed
  five controls including exhaustive agreement with an unpruned brute-force
  enumerator on 60 random instances (179 sets) and with an independent layered-BFS
  enumerator on 40 instances (778 sets), identical *sets* not merely identical counts.
- **Cost:** `results/block_counts.jsonl` 5 943 s; `v2_counts.jsonl` 130 806 s wall (36.3 h).
- **Code:** `fleet9/laneENUM/code/enumlib.py`, drivers `countdrv.py`, `run_v2.py`, `run_f4.py`; controls `validate.py`, `validate2.py`.
- **Logs/results:** `fleet9/laneENUM/results/{block_counts,v2_counts}.jsonl`, `results/sets/` (233 banks), `results/TALLY.txt`.
- **Generality:** **CIRCUIT-GENERIC** at the instance level (takes r, inputs, targets, k); the *instances* are MC-specific and come from `v2inst.py`/`f4inst.py`.
- **Phase-2 verdict:** **keeper.** This is the instrument that turns "the optimum is 8" into "the optimum is 8 and there is exactly one way to reach it", which is a far stronger statement.

### sat-set-blocking-enumeration
- **Family:** exhaustive enumeration (SAT).
- **What it does:** Same job as the DFS — enumerate all optimal value sets — but by
  asking a SAT solver repeatedly and adding one clause after each answer that
  forbids exactly that *set*, until the solver says UNSAT.
- **Twist vs siblings:** ~100× faster than the DFS at dimension 12, and terminates
  in a machine-checked UNSAT rather than an exhausted search tree. Used wherever
  the DFS could not finish.
- **Measured performance:** agreed with the DFS on all 8 blocks the DFS could
  finish (control F, sets identical, not just counts); independently reproduced the
  U07 counts (3, 3, 12, 18, 3, 10, 3, 1, 1) on nine record blocks; `record_set_found`
  true across 99 cells. **Erratum caught by control F:** the first version of the
  blocking clause had inverted polarity, so the block never bit and the enumerator
  looped on one solution forever — no number from that version reached the report.
- **Cost:** 306 903 s wall over 116 rows (85.3 h), including single cells of 32 h and 16 h.
- **Code:** `fleet9/laneENUM/code/satenum.py`, control `satenum_ctrl.py`, driver `run_sat.py`.
- **Logs/results:** `fleet9/laneENUM/results/sat_counts.jsonl`, `results/sets/`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper** — the fast half of the enumeration pair; keep the DFS as its cross-check.

### sat-with-banned-or-required-values (forcedness test)
- **Family:** structural analysis (SAT).
- **What it does:** Asks for an optimal program **with a specific intermediate
  value forbidden**. If the answer is UNSAT, that value is not merely *usable* —
  every optimum must build it.
- **Twist vs siblings:** turns "the solver reached for X" into "the solver cannot
  do otherwise". It is the only instrument here that can promote a MATCHED /
  hand-picked constant to DERIVED.
- **Measured performance:** control E fired in both directions on real blocks
  (ban a value the unique optimum uses → UNSAT; ban one it does not → SAT; require
  used → SAT; require unused → UNSAT; 10/10). Headline result: banning
  `delta_3(0xc)` on the unprompted merged `{2,3,7}` block at k=9 returned **UNSAT in
  3 668 s over all 300/300 cubes**, so **every** 9-gate optimum builds it — with a
  fired positive control (9 distinct optima enumerated, all building exactly that
  one tap-3 value, rank exactly 1).
- **Cost:** 3 668 s for the decisive ban; controls seconds.
- **Code:** `fleet9/laneENUM/code/satban.py`, `q27force.py`, `q27enum.py`, control `satban_ctrl.py`.
- **Logs/results:** `fleet9/laneENUM/results/{q27_force.jsonl,q27_enum.json,ctrlE_satban.json}`, `logs/q27force.out`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper, and under-used.** It is the cheapest way to retire a "we picked this because the record had it" tag anywhere in a future package.

### symmetry-equivariance-proof-and-sensitivity-control
- **Family:** structural analysis.
- **What it does:** Establishes that the byte-rotation ρ is a genuine automorphism
  of the problem (GF(2)-linear, order 4, permutes the 32 inputs, permutes the 32
  targets), and therefore that gate count, validity, minimum depth and
  neighbourhood structure are all ρ-invariant — so checking one representative per
  orbit is **complete**, and any exhaustive sweep over 88-states can divide its
  work by 4.
- **Twist vs siblings:** it does not stop at the algebra. It **re-runs the actual
  historical irreducibility instrument** (byte-copied read-only into
  `code/imported/`) on C and on ρC window-by-window, requiring every intermediate
  to correspond, and it carries a **sensitivity control that can fail**: the same
  comparison with two *non*-automorphisms (`rot 1`, `rot 4` — linear, permute the
  inputs but not the targets) returns **300/300 mismatches**, so the zero is a
  measurement rather than a tautology.
- **Measured performance:** 4 580 windows compared, **0 mismatches**; 50 000 random
  linearity/order checks; 300/300 mismatches for both non-automorphisms and 0/300
  for both automorphisms. Consequence: the historical "105 801 states k≤2-swept"
  figure certifies **423 204** circuits, and the project's 88-census is exactly one
  representative per orbit (0 ρ-fixed circuits in 54 889).
- **Cost:** minutes.
- **Code:** `fleet9/laneENUM/code/rho_equivariance.py`, control `rho_equiv_ctrl.py`, `code/imported/exact_window.py`.
- **Logs/results:** `fleet9/laneENUM/results/{rho_equivariance.json,ctrlG_equivariance.json}`, `logs/rho_equiv.out`.
- **Generality:** **MIXED.** The *method* (find the symmetry group, prove the instrument equivariant, then quotient) is fully generic and is exactly what should be done first on `aes_inv_mixcolumns`; the specific ρ is MC-specific but the inverse matrix also commutes with byte rotation, so it should transfer directly.
- **Phase-2 verdict:** **keeper — top of the list.** A free 4× on every exhaustive sweep, and it retroactively quadrupled the value of work already done.

### population-census-by-block-decomposition
- **Family:** structural analysis.
- **What it does:** Takes the project's whole harvest of known 88-gate circuits and
  splits each one into the same fixed blocks, then asks which blocks ever differ
  between circuits.
- **Twist vs siblings:** works in a frame that needs no committed interface sets —
  fix the currency menus and the blocks are determined — so it can decompose
  circuits that were never generated by the block model at all.
- **Measured performance:** **54 889** distinct 88-gate mask sets decomposed;
  **0** with any out-of-class value (100 % in class); **37** distinct currency
  configurations; the largest holds 14 359 circuits; **only two blocks ever vary
  inside a configuration** (R01 and R34); the eight currency blocks and all four
  clean sectors vary in **0 of 37** configurations, ever. It also found the first
  counterexample to a standing "law": 2 of 296 census currency blocks violate the
  per-line purity rule C2 — *"a measured regularity with exceptions, not a law"*.
- **Cost:** minutes (no solver).
- **Code:** `fleet9/laneENUM/code/census.py`, `census2.py`, `condrig.py`, `shape.py`.
- **Logs/results:** `fleet9/laneENUM/results/{census.json,census2.json,census2_rows.json,census_cfgs.jsonl,condrig.json,shape.json,population_table.json}`.
- **Generality:** MC-HARDCODED (needs a block decomposition to exist first).
- **Phase-2 verdict:** **keeper.** Cheapest way to learn where a plateau's freedom actually lives before spending solver time.

### minimum-depth-schedule-sampling
- **Family:** structural analysis.
- **What it does:** For a sample of circuits from the plateau, computes the
  provably shallowest schedule of its fixed value set (level BFS) and histograms
  the result.
- **Twist vs siblings:** measures the plateau's **depth** distribution rather than
  its size, which is what produced the slice's most actionable single sentence.
- **Measured performance:** 1 200 uniformly sampled harvest circuits give depths
  {7:1, 8:111, 9:490, 10:543, 11:55} — **mode 10, and depth 5 occurs zero times**.
  The 14 known records sit at {5:2, 6:1, 7:3, 8:6, 9:2}. **The record is a depth
  record disguised as a gate record**; a successor sampling the 88-plateau for an 87
  is sampling a depth-9-to-10 population.
- **Cost:** minutes.
- **Code:** `fleet9/laneENUM/code/sample.py`, `materialise.py`.
- **Logs/results:** `fleet9/laneENUM/results/sample.json` (118 K), `results/circuits/` (223 files), `logs/sample.out`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.** Cheap, and it reframes what "the record" is.

### cleanroom-randomized-boyar-peralta
- **Family:** plateau-search (greedy/randomized).
- **What it does:** Grows a set of XOR results from the 32 inputs. At each step it
  scores every possible new pair-XOR by how much it reduces the total remaining
  distance to the 32 targets, picks the best (random among ties), and repeats;
  restarts from scratch on a timer, keeping the best circuit found. Written in C
  from scratch with its own hash sets and bounded distance queries.
- **Twist vs siblings:** a **clean-room** implementation with no project knowledge,
  no record data, no menus and no block decomposition — which makes its result a
  calibration point rather than a search result. It also carries a **symmetric
  mode**: pick a value and add all four byte-rotations of it at once, scoring by
  the minimum over the four rotations.
- **Measured performance:** best BP-only asymmetric result **94** (`w5C_1.log`);
  typical per-worker best 95–101; **symmetric mode is much worse — 106–108**
  (`islandS.json` 106, `test_sym.json` 108), i.e. forcing ρ-symmetry costs ~12 gates
  in this search. Naive baseline 124. **The whole clean-room effort's best is 93 —
  five gates above the record.**
- **Cost:** 14 logged BP workers, restarts of order 10²–10³ in 13–375 s each,
  across ~6 waves (`w0…w7`, `w2_*`, `w3_*`, `w4_*`, `w5A/B/C/D_*`).
- **Code:** `fleet10/cleanroom/work/bp.c` … `bp5.c` (+ compiled `bp` … `bp5s`).
- **Logs/results:** `fleet10/cleanroom/work/w*.log` (67 logs total, 104 K), `island*.json`, `b*_w*.json`, `t*.json`, `test_{sym,asym}.json`.
- **Generality:** **MC-HARDCODED but trivially retargetable** — a single `TGT[32]` array at the top of each `.c` file is the only problem-specific content.
- **Phase-2 verdict:** **keeper as a baseline generator**, dead as a route to a record. Its value is the number 93/94: it prices what "no project knowledge" is worth.

### sat-window-repair
- **Family:** plateau-search (local improvement, SAT).
- **What it does:** Takes an existing circuit, deletes a random dependency-closed
  set of *m* gates, freezes the rest as constants, and asks a SAT solver whether
  *m−1* (or *m−2*) fresh gates can restore all 32 outputs. On SAT it rebuilds,
  verifies and publishes; on UNSAT that window is proved un-improvable.
- **Twist vs siblings:** the *window* is dependency-closed, and both the "save one
  gate" and "save two gates" asks are tried; UNSAT results are a real (if tiny)
  local certificate.
- **Measured performance:** **2 623 window attempts logged; exactly one
  improvement: `[hunt3] attempt 4: 94 -> 93 gates`** — a hit rate of ~0.04 %. Every
  attempt at m ≥ 8 timed out at 230–285 s; the decided windows are all m ≤ 7.
- **Cost:** ~70 335 s (19.5 h) of solver time across the `wsh*/wsw*/ws*/wsdeep` logs.
- **Code:** `fleet10/cleanroom/work/satfix.py`, `satfix_deep.py`, `satfix_hunt.py`, `satfix_hunt2.py`, `satfix_walk.py`.
- **Logs/results:** `fleet10/cleanroom/work/ws*.log`, `wsh*.log`, `wsw*.log`, `satbest_*.json`, `satinc*.json`.
- **Generality:** **CIRCUIT-GENERIC** — it reads targets from `spec/targets.json` and an arbitrary incumbent circuit.
- **Phase-2 verdict:** **keeper for the descent from a bad circuit; dead near an optimum.** The measured curve — plentiful improvements from 124 down, exactly one at 94 — is itself the useful result.

### island-portfolio-with-migration
- **Family:** plateau-search (search control).
- **What it does:** Runs several independent searches ("islands") in parallel, and
  every 12 minutes copies the best island's circuit over any island that is more
  than 5 gates behind.
- **Twist vs siblings:** a coarse genetic-style migration schedule over whole
  circuits, with a separate `collect.sh` that verifies every candidate before
  crowning a global best.
- **Measured performance:** islands landed at 94/94/94/97; the migration logs
  (`migrate*.log`) are **0 bytes**, i.e. **no migration ever fired** — the islands
  never diverged by more than 5 gates. So this method contributed nothing measurable.
- **Cost:** 5 400 s of wall per driver, negligible CPU.
- **Code:** `fleet10/cleanroom/work/migrate.sh`, `collect.sh`.
- **Logs/results:** `migrate.log`, `migrate2.log`, `migrate3.log` (all empty), `island[A-D,S].json`, `shared_best.json`.
- **Generality:** CIRCUIT-GENERIC (shell only).
- **Phase-2 verdict:** **dead-end as configured** — the 5-gate migration threshold was never reached. Keep the pattern, drop the threshold.

### symmetry-quotient-sat
- **Family:** SAT / symmetry.
- **What it does:** Searches directly for a **rotation-symmetric** circuit by
  solving in the quotient: pick *k* "orbit gates", each of which costs 4 real XOR
  gates when materialised, and require each of the 8 target orbits to be some
  rotation of some orbit gate.
- **Twist vs siblings:** searches a space 4× smaller than the real one, at the cost
  of only finding circuits whose gate count is a multiple of 4 and which are
  ρ-symmetric.
- **Measured performance:** **no result on disk** — no `symsol_k.json` exists in
  the tree, and no log names it. This is an *unfinished* method (see LEADS L6).
  Its sibling measurement in the same directory says why it is unpromising:
  BP's symmetric mode costs ~12 gates over asymmetric, and fleet9 found **zero**
  ρ-fixed circuits among 54 889 88s.
- **Cost:** unknown; no logs.
- **Code:** `fleet10/cleanroom/work/satquot.py`.
- **Generality:** MC-HARDCODED (reads `spec/targets.json`, assumes the rot8 symmetry).
- **Phase-2 verdict:** **unfinished; low expected value but genuinely never answered.** fleet9 §12 item 5 independently asks the same question ("look for a ρ-symmetric 88").

### fact-vs-mutable-code-audit
- **Family:** structural analysis (no solver).
- **What it does:** Walks a generator line by line and classifies every part as
  **ABSOLUTE FACT** (forced by the problem specification — a hypothetical better
  circuit could not violate it) or **MUTABLE** (a choice someone made, which a
  better circuit is free to ignore), and for every mutable part asks what it would
  cost to swap it. Three independent auditors, then an adversarial referee who
  re-verifies by recomputation and merges.
- **Twist vs siblings:** it is the only method in the repository that measures
  **how much of a "result" is actually a modelling assumption**. The referee layer
  is what makes it work: 68 rows were claimed ABSOLUTE FACT and **22 were
  downgraded**, twenty of them from one systematic error (auditors invented classes
  the template does not contain — "ABSOLUTE FACT (as methodology)").
- **Measured performance:** **244 rows** · 47 FACT / 116 MUTABLE-load-bearing / 81
  inert · **22-entry defect register**, 5 at severity 1, 2 of those live in
  artefacts on disk · a 17-item ranked successor list. Headline finding: **the
  shipped-88 run proved no per-block minimum at all** — all ten blocks returned SAT
  at their first tested k, which was the inherited hint, so 18 gate-levels were
  never tested and the instrument's own machine-checked floor was **70, not 88**.
  Second: **"if U1 is 5, the model prices 87"**, a single dim-12 solve away.
- **Cost:** read-only; every check a `python3 -c` one-liner under 90 s. No solver run.
- **Code:** none (documents). Schema at `fleet12/laneAUDIT/TEMPLATE.md`.
- **Logs/results:** `fleet12/laneAUDIT/AUDIT.md` (188 K), `AUDIT_CORE.md`, `AUDIT_DATA.md`, `AUDIT_ENGINE.md`, `SFLAGS_VERIFIED.md`.
- **Generality:** **CIRCUIT-GENERIC** — it is a methodology, and the template transfers unchanged.
- **Phase-2 verdict:** **keeper, and the single highest-leverage method in the slice.** It generated everything fleet12 then went and bought, and it found real 87-shaped openings (two of which were closed by ~4 core-hours of solving).

### naive-reader-certification
- **Family:** documentation / verification.
- **What it does:** Writes the algorithm in plain language, then hands it to a
  reader with **no** prior exposure to the repository, the problem, or any earlier
  round, who may read that one file and nothing else, and must restate the
  algorithm end to end and independently re-derive its mathematics.
- **Twist vs siblings:** the reviewer reimplements from the prose alone — in round
  4 they rebuilt GF(2⁸), the trace-dual basis, the τ coefficients, the shape algebra
  and all 32 target masks from the document, and every stated value matched.
- **Measured performance:** four rounds; round 4 = **PASS with two errata**, 38-step
  restatement, 4 gaps none on the main line. The process also surfaced **seven
  code-versus-documentation disagreements** (§18), including that the repo's own
  `RESULT.md` states the `MATCHED` tag is retired while `cells.py` still carries it.
- **Cost:** documentation time only.
- **Code:** none.
- **Logs/results:** `fleet12/laneALGO/ALGORITHM.md` + `NAIVE_READER_REPORT{,_v2,_v3,_v4}.md`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.** This is the method that produces the public writeup, and it has a pass/fail criterion.

### env-gated-one-mutation-per-run sweeps (the library machinery)
- **Family:** experiment control (meta-method used by five fleet12 lanes).
- **What it does:** Every axis is swapped by an **environment variable that is inert
  when unset** — with the variable unset the patched file behaves byte-identically
  to the shipped one, demonstrated before each lane's first solve. One mutation per
  run; a fresh solve-cache bank per experiment so a changed thing the cache key does
  not capture can never be served a stale answer.
- **Twist vs siblings:** it is what lets one repository hold four mutations at once
  without contaminating the default path, and it is why the lanes' *negatives* mean
  something.
- **Measured performance:** eight mechanisms catalogued (`SLP_SOLVE_CACHE`,
  `SLP_SUPPRESS_HINTS`, `LANE_HALO`, `LANE_ORDER`, `LANE_KNOBS_COMMIT`,
  `SLP_REGRESS_OUTDIR`, `SLP_REVERIFY_OUT`, `SLP_USE_POOL`), each with a documented
  inertness check. A hard **tractability guard** is enforced *inside the patch*
  (`plan._halo` refuses a fifth line: dim 16 is the solver ceiling) rather than in a
  shell script, so it cannot be forgotten.
- **Cost:** negligible.
- **Code:** catalogued in `fleet12/LIBRARY.md` §1; patch records in each lane's `PATCHES.md`; pristine originals in `laneLIB/pristine/`, `laneKNOBS/pristine/`, `laneF1/pristine/`, `laneHALO/plan.py.pre_laneHALO`, `laneHINTS/*.pre_laneHINTS`, `laneORDER/laws.py.pre_laneORDER`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper. Adopt as the default experiment protocol.**

### hint-suppression-resolve
- **Family:** SAT bound verification.
- **What it does:** The generator was being handed ten hard-coded lower bounds
  ("this block needs at least N gates"), read off an earlier lane, which made it
  start searching at N and therefore **never test anything below N**. This method
  drops the floors and re-solves every block from its own counting bound upward.
- **Twist vs siblings:** it does not look for a better circuit; it looks for
  whether the claimed floor was ever *proved*. It is the cheapest possible attack on
  a bound that is inherited rather than earned.
- **Measured performance:** **all ten blocks return exactly their hint**, and the
  **57 gate-levels that had never been tested in this repository's history are now
  proved UNSAT.** `U1 = 6` proved twice from two different mask sets (k=4 UNSAT
  15.75 s, k=5 UNSAT 20.08 s) — which **closes the audit's rank-1 "if U1 is 5 the
  model prices 87"**, negatively. The instrument's machine-checked floor for the
  shipped configuration rises **70 → 88**. And the *hint's key* is measurably wrong:
  at `rec_88at7` (a three-value commitment) `B37` prices **3**, not the hinted 4, so
  **that configuration's price is 88, not the published 89** — with a verified
  circuit on disk to prove it; the same test at `f4_basis` is refuted (k=3 UNSAT).
- **Cost:** **3 513 wall-seconds / 14 053 core-seconds ≈ 3.90 core-hours**, 4 cores peak.
- **Code:** `SLP_SUPPRESS_HINTS` patch (`fleet12/laneHINTS/PATCHES.md`), `bank.py`, `tally.py`, `run_step*.sh`.
- **Logs/results:** `fleet12/laneHINTS/{RESULT.md,results.jsonl (43 rows),logs/,out/ (5 circuits),cache/}`.
- **Generality:** CIRCUIT-GENERIC as a discipline (never inherit a floor you have not proved).
- **Phase-2 verdict:** **keeper.** Four core-hours converted a claimed floor into a proved one and corrected a published number.

### block-boundary-halo-widening
- **Family:** structural mutation.
- **What it does:** A block is only allowed to use values living on its own small
  set of coordinate "lines". This method **widens** one block's line set by a halo
  and re-prices, testing whether the partition the model enforces is costing gates.
- **Twist vs siblings:** it widens the *admissible set* without touching the
  predicate, so nothing else in the model moves; and the tractability guard (≤4
  lines / dim 16) is enforced inside the patch.
- **Measured performance:** **twelve mutations, eleven complete, every one prices
  exactly 88, not one block moved a single gate** — including the D22 falsifier's
  own home (`U4 → {2,3,4,7}`), both ring-adjacent widenings of the largest block,
  and all four hub blocks widened at once. It is not vacuous: `U4`'s supply grew
  25 → 41 with **nine of the sixteen new values genuinely straddling the invented
  boundary**, and k=6 was then proved UNSAT in 104 s at dim 16 with all 41
  available. **The mechanism found is worth more than the negative: a halo enlarges
  what a block MAY use; it does not change what the block is MINIMISING.** In the
  pair mutation, `W3` was handed a whole extra line and used it for nothing.
- **Cost:** minutes to ~340 s per mutation; ten mutations on a budget written for five.
- **Code:** `LANE_HALO` in `plan.py:_halo`; `fleet12/laneHALO/{run_halo.sh,run_chain*.{sh,py},run_b3.py,run_b4.py,run_pairs.py,run_u07.py,bank.py,tally.py}`.
- **Logs/results:** `fleet12/laneHALO/{RESULT.md,results.jsonl (118 rows),logs/ (25),out/ (11 circuits),cache/}`.
- **Generality:** MC-HARDCODED (needs a line-set decomposition), but the *mechanism finding* generalises to any decomposed search.
- **Phase-2 verdict:** **closed, do not re-buy.** The mechanism predicts all further widenings dead; only the *un-split* block (a merge, not a widening) survives, and that is priced at k≥14.

### block-order-permutation-sweep
- **Family:** structural mutation.
- **What it does:** The blocks are solved in some order, and each block is handed
  everything already built that it is allowed to use — so the order decides each
  block's free supply and therefore, in principle, its price. This method enumerates
  **all** legal orders and prices every one.
- **Twist vs siblings:** full coverage rather than a sample (75 of 75), and it
  refuses any order violating a *derived* dependency edge, checked against the
  dependency dictionary the code itself just built (no second copy to drift).
- **Measured performance:** **75/75 price 88, and far sharper than that** — every
  block in every order was handed a **byte-identical instance** (740 of 740
  post-control block solves were cache hits on a key containing the free supply and
  its arrival levels), and **all 75 emitted files share one md5**
  (`eba1f6a998f5a9b30770b0651bb20396`, verified here), VALID ×75. **The 75 orders
  are not 75 classes with a common optimum — they are one class.** Mechanism: under
  the four forced edges the supply graph is *saturated*, so a permutation has
  nothing left to move.
- **Cost:** **215.1 core-seconds = 0.060 core-hours** for the whole sweep (all of it
  the control); the other 74 orders cost 9.85 s each of cache replay. ~16 minutes wall.
- **Code:** `LANE_ORDER` in `laws.py:_lane_order`; `fleet12/laneORDER/{enum_orders.py,sweep.py,bank.py,census.py,tally.py,probe/supply_probe.py}`.
- **Logs/results:** `fleet12/laneORDER/{RESULT.md,results.jsonl (75),logs/ (79),out/ (75),orders.json,diversity.json,probe/seed_shipped.jsonl}`.
- **Generality:** CIRCUIT-GENERIC as a pattern (enumerate the legal orders of any staged pipeline).
- **Phase-2 verdict:** **closed.** 0.06 core-hours bought full coverage of an axis the audit ranked 5th; the *saturation* mechanism tells a successor when to bother re-running it (a configuration where some block builds a mask on a proper subset of its lines).

### commitment-grammar-knob-sweep
- **Family:** structural mutation.
- **What it does:** Three "interface commitments" were hand-written dictionary
  literals. This method introduces a tiny closed grammar so a commitment can be
  specified as one environment variable, and sweeps the alternatives — with an
  unparseable term a hard error rather than a silent fall-through to the shipped value.
- **Twist vs siblings:** the grammar is what makes the sweep *auditable at scale*;
  hand-writing one config literal per candidate is not.
- **Measured performance:** 65 pre-registered runs, **nothing ≤ 87**. Best results
  88 uncapped, **88 @ depth 5 (ties the record)**, 90 @ depth 5, 92 @ depth 4.
  Five pre-registered predictions **refuted**, and the refutations carry the lane:
  (i) the `Q27` `MATCHED` tag is overstated — **six of sixteen tap-3 settings reach a
  verified 88**, not one, and none of the winners is in the menu heuristic that was
  supposed to predict them; (ii) the `Q1` derive, widened from `max_cost 1` to 2,
  stops being vacuous **and selects the configured triple exactly** (predicted not
  to); (iii) the two depth parameters `LIBRARY.md` called the cheapest open axes and
  the obvious attack on the depth-5 gap are **inert** — every interface constraint
  switched off at D=5, both configurations, 13 rows, price unchanged. One
  pre-registered control **failed and was right to**: it exposed that the depth-4
  record is a *ladder* circuit, so the axis was never testable against it.
- **Cost:** **38 120 core-seconds ≈ 10.6 core-hours**, ≤4 concurrent, `--cores 1` each.
- **Code:** `LANE_KNOBS_COMMIT` in `cells.py:164-230`; `SLP_DERIVE_MAX_COST`/`SLP_DERIVE_OUTDIR` in `derive.py`/`annotate_derive.py`; `fleet12/laneKNOBS/scripts/`.
- **Logs/results:** `fleet12/laneKNOBS/{RESULT.md,results.jsonl (65),logs/ (80),out/ (57 circuits),derive_out/ (5),cache/ (5 banks)}`.
- **Generality:** MC-HARDCODED.
- **Phase-2 verdict:** **closed.** "The cheap axes were cheap because there was very little in them, and what there was, was a correction rather than a circuit."

### menu-derivability-diff (no solver)
- **Family:** structural analysis / provenance.
- **What it does:** The deepest record-dependency in the package is a set of eight
  per-line "currency menus" read off known record circuits. Before spending any
  solver time, this method enumerates every menu that a *rule* could produce and
  diffs them against the shipped one — because if the menu were some rule's output,
  the dependency would close by derivation at zero cost.
- **Twist vs siblings:** it is a **proof, not a survey**, in its decisive test:
  derive the eight lines' attributes from the theory alone, observe that three lines
  the theory cannot tell apart carry three *different* shape sets (one of them
  empty), and conclude that **no rule that is a function of the derived line
  attributes can emit this menu.**
- **Measured performance:** 3 879 enumerated rule instances vs all 22 cells →
  **0/22 matched**; the per-role family exhaustive over 57³ = **185 193** instances →
  **0** reproduce the shipped menu; the 22 record cells hold **21 distinct menus**,
  with currency prices from 20 to 28. Verdict: **the menu is a property of the
  circuit it was read off, not of MixColumns.**
- **Cost:** minutes, no solver (189 072 rule instances diffed).
- **Code:** `fleet12/laneF1/diffcheck.py`, `menu_rules.py`.
- **Logs/results:** `fleet12/laneF1/RESULT.md` §1, `menus/` (109 menu JSONs, each carrying the rule that made it).
- **Generality:** **CIRCUIT-GENERIC as a discipline** — before mutating an inherited constant, first ask whether it is derivable, exhaustively, without a solver.
- **Phase-2 verdict:** **keeper.** The cheapest hard result in fleet12.

### menu-neighbourhood-and-tradeoff-sweep
- **Family:** structural mutation / cost-curve measurement.
- **What it does:** Mutates the currency menu one shape at a time (add / drop /
  double-drop / triple-drop, plus whole rule-generated families) and measures how
  the circuit total responds — i.e. it measures the *cross-term* between what you
  spend on shared reusable values and what the blocks then cost.
- **Twist vs siblings:** the deliverable is a **curve**, not a best-of. It is the
  only method in the slice that measures a trade-off rather than testing a hypothesis.
- **Measured performance:** 49 distinct runs, **25 at exactly 88, none below**. The
  cross-term is **exactly −1.00 block gate per +1 currency gate across |M| ∈ [19,23]**
  — spending more on currency buys back exactly what it costs, never more — so
  **88 is a five-wide flat plateau in the menu axis with cliffs on both sides**
  (the fourth drop costs four block gates, 88 → 91; the uniform family above pays
  −0.88, −0.62, then **0.00**). Mechanism: **19 of the 25 88-gate runs emit the
  byte-identical gate list** (md5 `edf56fcc3641`) — dropping a shape does not delete
  a gate, it changes which phase builds the same mask. Best *rule-generated* menu
  prices **97**; the record menu beats it by **nine gates**. It also refuted its own
  pre-registration: the pipeline total is **not** monotone in the menu, because one
  block's supply includes whatever witness an upstream block happened to return.
- **Cost:** **11.99 core-hours**, `--cores 1` each, ≤4 concurrent.
- **Code:** `LANE_F1_MENU` (`cells.py`), `SLP_CURRENCY_KMAX` (`algebra.py`); `fleet12/laneF1/scripts/{run.py,queue.sh,mkmenus.py,descend.py,tally.py,curve.py}`.
- **Logs/results:** `fleet12/laneF1/{RESULT.md,results.jsonl (64 rows),results_{tally,curve,distinct,famcheck}.txt,logs/ (72),out/ (51),menus/ (109),cache/}`.
- **Generality:** MC-HARDCODED.
- **Phase-2 verdict:** **keeper as a template** — "measure the cross-term before assuming a knob is load-bearing" is the transferable lesson. Coverage was tiny (5 of 64, 6 of 128, **0 of 262 144**) and the RESULT says so.

### derive-family-vacuity-audit
- **Family:** structural analysis (no solver).
- **What it does:** When a package claims a constant is "derived", this checks
  whether the constant was even **inside the family the derivation searched**. If it
  was not, the derivation is vacuous — it proved nothing about the thing it is cited for.
- **Twist vs siblings:** it is a guard on *other people's* results, and the audited
  code was more honest than any summary of it (`algebra.py`: *"Always check
  `family_contains_configured` before reading a derive result"*).
- **Measured performance:** REF-V11 found **three of four derive runs vacuous by
  construction** — all three `Q1` values and `D37`'s `δ₄(4)` cost 2 and lay outside a
  family searched at `max_cost=1`. laneKNOBS then widened to `max_cost=2`: `Q1`
  goes 0/3 → **3/3**, `D37` 3/4 → **4/4**, and the widened derive **selects the
  configured triple exactly**. laneF1's `famcheck.py` then showed this is
  **menu-robust**: the configured commitments lie inside the widened family for
  **every one of 40 menus, including the empty menu**, though the offered family
  itself swings 28 → 129 (4.6×).
- **Cost:** minutes (no solver for the check; 3 free-supply solves for the widened derive).
- **Code:** `fleet12/laneF1/famcheck.py`; `SLP_DERIVE_MAX_COST` patch in laneKNOBS.
- **Logs/results:** `fleet12/laneF1/results_famcheck.txt`, `fleet12/laneKNOBS/derive_out/`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.** "The project's best epistemic device" (audit D18).

### instrument-repair-with-regression-separation
- **Family:** tooling / soundness.
- **What it does:** Six minimal, separately-verified, separately-revertible fixes to
  the search instrument itself, each closing a path by which a *non-result* could be
  published as a *result*: a crash or an exhausted loop bound can no longer be
  reported as "provably infeasible"; the solve-cache key now contains the hint and
  the gate cap so an unhinted control can no longer be served the hinted answer; the
  dead-gate strip is on by default; and — crucially — the regression suite's
  pass condition is split into "the circuit verifies 32/32" (still asserted) and
  "the emitted count is exactly N" (a recorded observation).
- **Twist vs siblings:** the regression split is the part nobody asks for: a suite
  that pins current behaviour is a suite that **red-flags its own corrections**
  (four of nine rows would have gone red for being right).
- **Measured performance:** all six applied and verified; all nine regression rows
  VALID and at their corrected counts; the default configuration still emits **88,
  VALID, 66 + 22** from a clean environment **with the entire shipped cache orphaned
  by the key fix** — i.e. every one of the ten block prices was re-solved, not served.
  The naive regime now emits **108 @ depth 3** where it emitted 116. The serial
  solver path turned out to be **1.2×–31× faster** than the multiprocessing pool
  with byte-identical level logs, and the pool **deadlocks** (two live examples, ~0
  CPU, four defunct workers, and the per-block timeout cannot fire because the
  parent is blocked rather than counting) — so serial became the default.
- **Cost:** hours of engineering; one full re-solve.
- **Code:** `fleet12/laneLIB/PATCHES.md` (B1–B6), `pristine/*.pre_laneLIB` (13 files).
- **Logs/results:** `fleet12/laneLIB/{RESULT.md,logs/,out/ (6),out/regress/ (10),out/regress2/ (7)}`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.** These are the fixes that make every later negative believable.

### swappable-parts-catalogue
- **Family:** meta / planning.
- **What it does:** Turns the audit's row-by-row classification into an operational
  catalogue: for every part that is a real axis, where it lives, the mechanism that
  swaps it, the **tractability guard** that stops the swap becoming the original
  intractable problem, the verdict so far, and the cost of buying it if unbought.
- **Twist vs siblings:** it prices the *unbought* axes, and it states three hard
  limits that have each already been paid for in core-hours ("never widen a block
  past dim 16"; "merges at k ≥ 14 are the priced-dead frontier"; "one mutation per run").
- **Measured performance:** **25 axes** catalogued — 6 CLOSED, 4 MEASURED above 88,
  11 OPEN with costs, 1 FRONTIER, 2 INTRACTABLE, 1 needing new machinery. Its
  honest paragraph is the best one-paragraph summary of the whole campaign:
  *"every mutation measured so far returns exactly 88 … everything cheap enough to
  have been swept has been swept, and every one of those sweeps returned 88."*
- **Cost:** documentation only.
- **Code:** none. `fleet12/LIBRARY.md`.
- **Generality:** CIRCUIT-GENERIC as a template.
- **Phase-2 verdict:** **keeper — this is the phase-2 planning document**, subject to the staleness noted in LEADS L4.

### conditional-rigidity-measurement
- **Family:** structural analysis.
- **What it does:** Asks whether fixing one block's value set pins down the next
  one, by grouping the census by upstream block and counting distinct downstream sets.
- **Twist vs siblings:** measures *conditional* rather than marginal variety, which
  is what tells you whether the population is generated by the interface.
- **Measured performance:** `U1 | U07`: 1 015 groups, 409 unique, max 32; `U4 | U27,U3`:
  623 groups, 325 unique, max 2. So conditioning narrows but does not close —
  because a value *set* does not record which members were committed across the
  interface nor how the gate budget was split.
- **Cost:** minutes.
- **Code:** `fleet9/laneENUM/code/condrig.py`.
- **Logs/results:** `fleet9/laneENUM/results/condrig.json`.
- **Generality:** MC-HARDCODED.
- **Phase-2 verdict:** superseded-by-`population-census-by-block-decomposition` as a headline, but keep it — it is what makes the "population of interfaces" claim precise.

### greedy-upper-bound-control
- **Family:** control.
- **What it does:** On every single solve invocation, re-runs a cheap greedy
  constructor on **the instance actually being solved** and verifies its output. If
  that fails, the driver refuses to report any negative.
- **Twist vs siblings:** it is a *liveness* check on the instrument attached to
  every negative, not a one-off self-test.
- **Measured performance:** greedy program of 16 gates, `verify_slp` True, re-run
  and re-logged at the top of every laneCUBE solve; plus a positive control on a
  sub-instance whose optimum was known monolithically (UNSAT 5, UNSAT 6, SAT 7) —
  the cube driver found the SAT at cube 144 with a verified witness, proving the
  instrument finds programs when they exist, at dim 16, through this harness.
- **Cost:** ~3 s per invocation.
- **Code:** `fleet11/laneCUBE/code/controls.py`, `probe.py`, `agree.py`.
- **Logs/results:** `fleet11/laneCUBE/found/HIT_SUB_U4tgts_k7.json`, `cubes/SUB_U4tgts_k{6,7}.jsonl`, `ledger.jsonl`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.** "Positive control C2 is what makes any negative non-vacuous."

---

## 3. ARTIFACTS (counts + labels)

### Verified circuits

| label | count | where | command |
|---|---|---|---|
| **88-gate MixColumns circuits, fleet9 sample** | **223** (216 sampled from the census + 6 ρ-images of the two records + 1 self-test) — every file `gateCount: 88` | `fleet9/laneENUM/results/circuits/` | `ls fleet9/laneENUM/results/circuits/*.json \| wc -l`; gate counts via the python histogram in §3 note below |
| — of which **not in the project's census and not a record** | **60** | same dir (the `s*.json` sample) | `fleet9/laneENUM/RESULT.md` §9, re-derivable by `python3 fleet9/laneENUM/code/tally.py` |
| — of which **88 @ depth 5** (ties the record depth) | **2** (`rho1_88at5`, `rho2_88at5`, `rho3_88at5` are 3 ρ-images at depth 5; spot-verified `rho1_88at5` → `gates=88 depth=5 VALID`) | `fleet9/laneENUM/results/circuits/rho*_88at5.json` | `python3 verify_circuit.py fleet9/laneENUM/results/circuits/rho1_88at5.json` |
| **fleet12 emitted circuits, all lanes** | **224 files**: 88×**135**, 89×36, 90×11, 91×10, 92×8, 93×3, 95×2, 97×2, 98×2, 100, 102, 105, 108×4, + 5 non-circuit JSONs | `fleet12/*/out/`, `fleet12/laneLIB/out/regress{,2}/`, `fleet12/laneKNOBS/derive_out/` | see the python one-liner in §3 note |
| — of which **byte-identical duplicates** | **74 of the 75** laneORDER files share one md5 `eba1f6a998f5a9b30770b0651bb20396` | `fleet12/laneORDER/out/` | `md5sum fleet12/laneORDER/out/*.json \| awk '{print $1}' \| sort \| uniq -c` |
| — **88 @ depth 5** (record-tying) | **8 runs, 2 distinct gate lists** (`md5 c49d7ea2…` ×6, `md5 2ebaa8d8…` ×2) | `fleet12/laneKNOBS/out/k2d5*rec*.json` | `md5sum fleet12/laneKNOBS/out/k2d5*rec*.json` ; verified: `python3 verify_circuit.py fleet12/laneKNOBS/out/k2d5_rec_ctrl.json` → `gates=88 depth=5 VALID` |
| — **the corrected `rec_88at7` 88** (the circuit that reprices a published 89) | **1** | `fleet12/laneHINTS/out/step2b_rec88at7.json` | verified here: `gates=88 depth=8 outputs_built=32/32 VALID` |
| **laneCUBE's rehearsal 88** | 1 | `fleet11/laneCUBE/results/laneCUBE_88gates_d7.json` | (do not re-verify; lane is live) |
| **fleet10 clean-room best** | **93 gates, depth 7, VALID** | `fleet10/cleanroom/work/FINAL.json` | `python3 verify_circuit.py fleet10/cleanroom/work/FINAL.json` |
| fleet10 intermediate circuits | 63 JSONs, 93–124 gates | `fleet10/cleanroom/work/*.json` | histogram command in §1 working notes |

*(§3 note — the histogram command used:* `python3 - <<'EOF'` *loading each JSON and taking* `len(d['gates'])` *or* `d['gateCount']`*; run over* `fleet12/*/out/*.json`, `fleet12/*/out/*/*.json`, `fleet12/laneKNOBS/derive_out/*.json`*.)*

### Bound / UNSAT certificates

| label | what exactly it certifies | count | where |
|---|---|---|---|
| **k=14 cube refutations (partial)** | each row: "no 14-gate normal-form SLP for the merged W3\|U4 dim-16 block exists **with gate 0 reading input pair j**". **87 of 528** as of 2026-08-29 (51 at write-up); the level is UNSAT only when all 528 are | 87 UNSAT rows / 528 cubes | `fleet11/laneCUBE/cubes/joint_W3U4_k14.jsonl` |
| k=15 cube rows | same, under a 60 s budget — **reported as nothing**, since a budget refutes nothing | 23 UNSAT / 168 timeout | `fleet11/laneCUBE/cubes/joint_W3U4_k15.jsonl` |
| k=9/10/11 full sweeps | complete: **all 528 cubes UNSAT** at each level, cross-checked against fleet8's independent CNF encoding | 3 levels × 528 | `fleet11/laneCUBE/cubes/joint_W3U4_k{9,10,11}.jsonl` |
| positive/negative control sweeps | sub-instance `SUB_U4tgts`: k=6 all 528 UNSAT (agrees with monolithic), k=7 SAT at cube 144 with verified witness | 736 rows | `fleet11/laneCUBE/cubes/SUB_U4tgts_k{6,7}.jsonl`, `found/HIT_SUB_U4tgts_k7.json` |
| **57 newly-proved gate levels** | for each: "block B has no program at k gates" at a level **never tested before in this repository's history** — 18 at `f4_88_D4`, 18 at `rec_88at7`, 18 at `f4_88_noQ27`, 2 independent re-proofs of `U1` k=4/5, 1 at `f4_basis` | 57 | `fleet12/laneHINTS/results.jsonl` (43 rows), `fleet12/laneHINTS/cache/*.jsonl`, tabulated in `laneHINTS/RESULT.md` §5 |
| halo-widened UNSAT levels | e.g. `U4` at k=6 UNSAT in 104 s **at dim 16 with all 41 free values available** — a genuinely wider refutation than the un-haloed one | in 118 rows | `fleet12/laneHALO/results.jsonl`, `cache/` |
| block enumeration completions | for each cell: "the set of optimal value sets is exactly this list" (`complete: true`) or a floor (`complete: false`) | 111 v2 rows + 116 sat rows + 10 block rows | `fleet9/laneENUM/results/{v2_counts,sat_counts,block_counts}.jsonl` |
| forcedness certificate | "every 9-gate optimum of the unprompted merged {2,3,7} block builds `delta_3(0xc)`" — UNSAT with that value banned, 3 668 s, all 300/300 cubes, with a fired positive control | 1 | `fleet9/laneENUM/results/q27_force.jsonl`, `q27_enum.json` |
| dim-8 block optimality proofs | exhaustive DFS at k−1 returning empty, `optimum_proved=True` | 82/82 cells | `fleet9/laneENUM/results/v2_counts.jsonl` |
| SAT-window UNSAT certificates | "this dependency-closed window of m gates cannot be rebuilt in m−1" — local, tiny, but real | ~2 622 of 2 623 attempts | `fleet10/cleanroom/work/ws*.log`, `wsh*.log`, `wsw*.log` |

### Writeups and ledgers

| label | count | size | where |
|---|---|---|---|
| markdown documents | **32** | 1.05 M | `find fleet9 fleet10 fleet11 fleet12 -name '*.md'` |
| — RESULT.md files | 8 | 210 K | fleet9/laneENUM, fleet11/laneCUBE, fleet12/lane{F1,HALO,HINTS,KNOBS,LIB,ORDER} |
| — PREREG.md / PATCHES.md pairs | 6 + 6 | 190 K | one per fleet12 lane (laneLIB has PATCHES only) |
| — audit documents | 6 | 424 K | `fleet12/laneAUDIT/` |
| — algorithm + reviews | 5 | 220 K | `fleet12/laneALGO/` |
| **hash-chained ledgers** | 3 | 235 K | `fleet9/laneENUM/ledger.jsonl` (**270 rows**, 26 kinds), `fleet9/laneENUM/snapshot/ledger.jsonl`, `fleet11/laneCUBE/ledger.jsonl` |
| append-only result banks | 6 | 396 K | `fleet12/lane{F1,HALO,HINTS,KNOBS,ORDER}/results.jsonl` (64/118/43/65/75 rows) |
| solve-cache banks | 22 | ~600 K | `fleet12/*/cache/*.jsonl`, `fleet12/laneLIB/out/regress2/solve_cache.jsonl`, `fleet9/laneENUM/snapshot/results/solve_cache.jsonl` |
| raw logs | **374** files | 923 K | `find fleet9 fleet10 fleet11 fleet12 -type f \( -name '*.log' -o -name '*.out' -o -name '*.nohup' \)` |
| menu/instance JSONs | 109 + 3 + 2 | 530 K | `fleet12/laneF1/menus/`, `fleet9/laneENUM/inst/`, `fleet11/laneCUBE/inst/` |
| enumerated mask-set banks | 233 | 852 K | `fleet9/laneENUM/results/sets/` |

### Headline measured numbers this slice can supply to a public page

- 88-gate class: **≥ 219 608 distinct valid 88-gate circuits** provably exist (54 889 harvested, all in class, all pairwise ρ-inequivalent, × 4 for the free ρ-orbit, + 13 records not in the harvest); the project holds 54 902 on disk.
- **13 of 17 accounting blocks have multiplicity exactly 1** at every configuration tested (70 cells, no exception). 28 of every 88 gates are *forced* once the menus are chosen.
- Plateau depth distribution (1 200 draws): mode **10**; **depth 5 never occurs**.
- The 88 is a **five-wide flat plateau in the currency axis** (|M| = 19…23 all price 88), with a −1.00 exchange rate and cliffs at both ends.
- The true price of deciding k=14: **653–1 113 core-hours, and the cheapest route does not parallelise.**
- A from-scratch clean-room effort reaches **93**; the best rule-generated currency menu reaches **97**; the record menu is worth **nine gates** over the best rule anyone here could write.

---

## 4. KEEP / DELETE proposal

**KEEP (unreservedly):**

- `fleet12/laneAUDIT/`, `fleet12/laneALGO/`, `fleet12/LIBRARY.md` (676 K) — the campaign's intellectual output and the source material for the public pages.
- Every `RESULT.md`, `PREREG.md`, `PATCHES.md` (8 + 6 + 6 files, 400 K) — the pre-registrations are only worth anything as a set with their results.
- Every `results.jsonl` / `ledger.jsonl` / `cubes/*.jsonl` (630 K) — append-only, hash-chained, and every RESULT.md is re-tallied *from these*, not from prose. Deleting a bank silently invalidates its document.
- Every `cache/*.jsonl` solve bank (~600 K) — these are not scratch: they hold the actual UNSAT level records (the 57 newly-proved levels live here), and regenerating them costs the 3.9 / 10.6 / 12.0 core-hours the lanes spent.
- All `pristine/`, `*.pre_lane*`, `*.orig` (250 K) — the revert path for every patch to shipped code. Without them the mutations are irreversible.
- `fleet9/laneENUM/snapshot/` (720 K) — **KEEP despite looking like a duplicate.** It is a frozen copy of `fleet8/unified` taken before any fleet9 work, and **nothing under fleet8–fleet12 is git-tracked** (`git ls-files fleet9 fleet10 fleet11 fleet12 | wc -l` → 0; same for fleet8), so this is the only record of that code state.
- `fleet9/laneENUM/code/imported/` — byte-copies of the historical irreducibility instrument; the equivariance result is only meaningful because it ran against *these* bytes.
- `fleet9/laneENUM/results/circuits/` (223 files) — 60 are 88-gate MixColumns circuits the project's census does not contain.
- `fleet12/laneF1/menus/` (109 files, 440 K) — each carries the rule that made it; they are the provenance of the derivability verdict.
- All of `fleet11/laneCUBE/` — **frozen, live** (see HAZARDS).
- **All of `fleet10/cleanroom/`** — it is the only clean-room calibration in the repository and has no writeup; deleting it would destroy the "93 from scratch" datum. See LEADS L5: it needs a RESULT.md written *before* anyone considers pruning it.

**DELETE-CANDIDATE:**

| item | size reclaimed | why |
|---|---|---|
| `fleet12/laneORDER/out/order_*.json` — **74 of 75** | ~300 K | Byte-identical duplicates, one md5 verified across all 75. Keep one file plus the md5 manifest already in `RESULT.md`. *(Mild note: the 75-way identity IS the result, so keep the `md5sum` output in the RESULT if the files go.)* |
| `__pycache__/` in fleet9 (3 dirs) and `fleet12/laneF1/` | 216 K | Regenerable byte-code. **Do NOT touch `fleet11/laneCUBE/code/__pycache__/` (36 K)** — live processes. |
| `fleet10/cleanroom/work/{bp,bp2,bp3,bp4,bp5,bp5s}` compiled binaries | 143 K | Regenerable from the `.c` sources beside them with a one-line `gcc`. |
| `fleet10/cleanroom/work/migrate.log`, `migrate2.log`, `migrate3.log` | 0 K | Empty; the migration never fired. Keep the *fact* (it is a method result — see §2 `island-portfolio-with-migration`) but the files carry nothing. |
| `fleet10/cleanroom/work/` superseded intermediates: `b3_w*.json`, `b4_w*.json`, `b5*_*.json`, `t2..t6.json`, `diag_*.json` (~30 files) | ~25 K | Per-worker snapshots dominated by `island*.json` / `FINAL.json`. **Uncertain → I recommend KEEP**: 25 K is nothing and the wave structure is the only record of how the search progressed. |

**Uncertain, therefore KEEP + note:**

- `fleet12/laneF1/cache/s{1,4,5}.jsonl` (212 K) and the other lanes' caches are per-family banks whose keys were deliberately fresh; they cannot be merged into the shipped bank and should not be.
- `fleet12/laneHALO/out/{b_W3plus4,b3_W3plus4}.json` do **not** exist (the deadlocked runs never wrote them) — but `fleet12/laneHALO/logs/b_W3plus4.log` and `b3_W3plus4.log` are **currently held open** by two live-but-deadlocked PIDs. Do not move them while those PIDs exist.

Total confidently reclaimable: **~660 K** of 10.5 M — this slice is documents and banks, not bulk. There is no multi-GB scratch here.

---

## 5. LEADS (sharp-eye findings)

### L1 — `fleet11/laneCUBE`'s headline number is stale: k=14 is at **87/528**, not 51 — **VERIFIED-IN-LOG**
`RESULT.md` §7.1 and every downstream citation (including `LIBRARY.md` §2.2 and
axis 21) say *"51 of 528 cubes decided"*. Re-counted from the append-only bank
just now: **564 rows, 87 distinct cubes decided, all 87 UNSAT, 0 SAT, 477 open**.
```
python3 -c "import json,collections;rows=[json.loads(l) for l in open('fleet11/laneCUBE/cubes/joint_W3U4_k14.jsonl') if l.strip()];seen={r['cube']:r['status'] for r in rows if r['status'] in ('SAT','UNSAT')};print(len(rows),len(seen),collections.Counter(seen.values()))"
```
The verdict does not change (UNDECIDED, a bracket) but every "51" in the wrap-up
should be re-derived from the bank at write time, not copied. Note also that
**four monolithic solvers have now run 3 days each (~288 core-hours) with
zero bytes of log output** — consistent with the lane's own 653–1 113 core-hour
estimate, and the strongest available evidence that the estimate was honest.

### L2 — fleet9's tally is 5 days stale, and ~84 wall-hours of U3 enumeration landed after the writeup and was never read — **VERIFIED-IN-LOG**
`RESULT.md` is dated 2026-08-24 and says explicitly *"the U3 counting queue was
still draining at write-up and banks per cell, so re-running the tally can only
RAISE floors"*. Nobody re-ran it. Evidence: `results/TALLY.txt` is dated Aug 24
16:20, but `results/v2_counts.jsonl` is Aug 25 04:35, `results/sets/` is Aug 25
06:58 and `results/sat_counts.jsonl` is **Aug 26 04:18**; the ledger has grown
from the documented 198 rows to **270**. What landed: **all 14 U3 cells now have
SAT-enumeration rows**, 13 of them finding ≥1 optimal set (p88_05 found 7),
including single cells that ran **116 049 s (32 h)**, **59 932 s (16.6 h)** and
**53 165 s (14.8 h)**. Total banked enumeration wall across the lane is now
**443 651 s = 123.2 core-hours**, of which 85.3 h is the SAT enumerator.
```
cd fleet9/laneENUM && ls -la results/ && wc -l ledger.jsonl
python3 -c "import json;rows=[json.loads(l) for l in open('results/sat_counts.jsonl')];u3=[r for r in rows if r['block']=='U3'];print(len(u3));[print(r['tag'],r['k'],r['n_sets'],r['complete'],round(r['wall'])) for r in u3]"
```
**Confidence: the data is real; the impact is probably small.** Every new row is
`complete: false, status: timeout`, so U3 stays UNDECIDED and the per-configuration
population floors in §4 only firm up from "UNDEC" to "≥1". But `python3
fleet9/laneENUM/code/tally.py` (verified read-only — it opens files only for
reading and prints) has never been re-run against it, and the lane's own §4
promises that doing so is the correct way to read the table. **Cheap: one command.**

### L3 — `fleet12/laneF1`'s result table is missing 13 rows that measure the plateau's **upper** cliff directly — **VERIFIED-IN-LOG**
`RESULT.md` states a cut-off at 51 rows / 49 distinct runs with *"eight runs still
solving"*. `results.jsonl` now holds **64 rows**. The 13 late arrivals include the
data points the document could only *infer*: `s5a_add046` (|M|=24, blocks 65) → **89**,
`s5a_add04c` (24, 65) → **89**, `s5a_add02a` (24, 65) → **89**, `s5a_add06e` (24, 65) → **89**,
and `s5a_add046e` (**|M|=25, blocks 64**) → **89**. That is the upper cliff measured
rather than argued — the plateau really does stop at |M|=23, and **blocks = 64**
(the lane's "lowest block total measured", previously only reached by a 56-shape
uniform menu) is now also reached by a 25-shape record-derived menu at total 89.
Six further rows are lean-menu `exit 5 UNDECIDED` truncations. **Nothing ≤ 87.**
```
python3 -c "import json;rows=[json.loads(l) for l in open('fleet12/laneF1/results.jsonl')];print(len(rows));[print(r['id'],r.get('currency_shapes'),r.get('blocks_total'),r.get('emitted'),r.get('exit_name')) for r in rows[51:]]"
```
Fix: re-run `fleet12/laneF1/scripts/tally.py` and `curve.py` before quoting §4a.

### L4 — `LIBRARY.md`'s scoreboard predates two of its own lanes — **VERIFIED-IN-LOG**
`LIBRARY.md` says of laneKNOBS *"started after this file was written and is
running now; its verdicts are not yet in §3"*, and axis 12 (the menus, flag F1) is
still listed **OPEN** at *"~100 configs × the affected block solves — days"*. Both
lanes have since finished. So the scoreboard's "11 OPEN" is wrong by at least six
axes: **6, 7, 8, 9, 14, 15 were bought by laneKNOBS** and **12 was bought and
repriced by laneF1** (which supplies its own replacement row in its §8). Anyone
writing the public "what remains open" section from `LIBRARY.md` §4/§5 as it
stands will overstate the open frontier substantially. The corrected picture:
essentially everything cheap is now CLOSED or MEASURED; what genuinely remains is
**axis 13** (currency per-line independence — *"the only untried attack on the 22
rather than the 66"*), **axis 20b** (the symmetry/normalisation rules N1–N3, which
**every UNSAT this repository has ever emitted rests on, and which no one has
re-refereed, including the audit referee**), **axis 24** (L5's forward-only rule —
a fixpoint over blocks, which no ordering of the current loop can express, and
laneORDER's 75/75 negative is precisely the evidence that permuting is exhausted),
and **axis 21** (the un-split block, priced dead at k≥14).

### L5 — `fleet10/cleanroom` is undocumented and unreferenced anywhere in the tree — **VERIFIED-IN-LOG**
`grep -rln "cleanroom\|fleet10" --include='*.md' .` returns only two `atlas/thinktank/`
files, and both are about a *different* `cleanroom_verify.py` in `aes_mc_records/`.
fleet10 has no RESULT.md, no README, no PREREG, and no mention in any campaign
document. It nonetheless contains: a from-scratch C reimplementation of
Boyar–Peralta that reached **94** unaided (**93** after SAT window repair, VALID),
a measured **~12-gate penalty for forcing ρ-symmetry** in the greedy search
(106–108 symmetric vs 94 asymmetric), a SAT window-repair hit rate of **1 in 2 623**,
and an unfinished symmetry-quotient SAT search. **This is the repo's only honest
answer to "how hard is 88 if you start from nothing", and it is the number a
public page most needs.** Recommend: write it a short RESULT.md *before* the
reorganisation wave, from the numbers in this report.

### L6 — `satquot.py` (the symmetry-quotient SAT search) was written and apparently never run to a conclusion — **SMELL**
`fleet10/cleanroom/work/satquot.py` searches for a rot8-symmetric circuit in the
quotient (k orbit gates, 4 real gates each, so only multiples of 4 are reachable).
Its documented output file `symsol_k.json` **does not exist anywhere in the repo**
and no log mentions it. Two independent lines in this slice bear on the same
question and both say it is unpromising — fleet10's own BP symmetric mode is
~12 gates worse, and fleet9 found **zero ρ-fixed circuits among 54 889** 88s — but
fleet9's `RESULT.md` §12 item 5 *independently asks for exactly this search*
(*"Look for a ρ-symmetric 88 … the known parity fact (a ρ-closed 87 needs an odd
number of ρ-fixed masks) makes the absence of ρ-fixed masks at 88 worth a direct
question rather than a sampling observation"*). So a written instrument and a
written request for it exist in the same repository and were never joined up. The
honest framing: **88 is not divisible by 4, so a fully ρ-symmetric 88 is impossible
in this encoding — but 88 = 4×22 exactly**, which means the quotient search at
k=22 is *precisely* the question, and it is cheap. Confidence: PLAUSIBLE that it
is worth one run; the two negative signals above make it low expected value.

### Not a lead, but the strongest structural evidence in the slice about **why 88 keeps appearing**
Three independent measurements converge, and the wrap-up should state them together:
1. **Rigidity** (fleet9): 13 of 17 blocks have a unique optimum at every one of 70
   tested cells, and the same blocks never vary across 54 889 wild circuits.
   **28 of every 88 gates are forced once the menus are chosen** — 32 % of every
   circuit that every local search in this project has been proposing moves on.
2. **Halo mechanism** (fleet12/laneHALO): widening what a block *may* use changes
   nothing, because it does not change what the block is *minimising* — each piece
   was already optimal inside its narrow line set. Demonstrated, not assumed: `W3`
   was handed a whole extra line and every one of its eight witness gates stayed
   inside the original three.
3. **Saturation** (fleet12/laneORDER): under the forced dependency edges the supply
   graph is already saturated, so all 75 legal orders present every block a
   byte-identical instance and emit the byte-identical circuit.

Together: the model is not "an 88 that happens to be found repeatedly"; it is a
structure in which almost everything is pinned, and the only unpinned parts (`U07`,
the R34 core, and one currency line) have been measured and are worth zero. The
counterweight, stated equally plainly by the audit, is that **all of this is inside
a block partition that was never measured on any circuit** (defect D22, severity 1,
LIVE — and `91@6` gate 70 is an existing circuit that no fleet8 block can
represent). An 87 that crosses a block boundary is exactly as possible today as it
was before fleet12 started.

---

## 6. HAZARDS

### 6.1 `fleet11/laneCUBE/` — LIVE. **THE ENTIRE DIRECTORY IS FROZEN.**

20 processes are running in it right now (`ps -eo pid,etime,args`):

| PIDs | age | what |
|---|---|---|
| 333371, 345293, 345295, 345297 | 3d 01–02h | `python3 -u code/mono.py 14` — four monolithic solvers, ~90 % CPU each |
| 443496 | 2d 13h | `python3 -u code/cube16.py --k 14 --cores 16 --group 33 --cube-timeout 0 --tlim 259200 --retry-timeouts` (parent, 0 % CPU) |
| 443570–443584 | 2d 13h | 15 group workers, ~90 % CPU each |

**Do not move, rename, delete, chmod or `git add` anything under
`fleet11/laneCUBE/`. Do not create `experiments/STOP`. Never `pkill`.**
The full set the live processes depend on:

- `fleet11/laneCUBE/code/` — **all 9 `.py` files** (`cube16.py`, `inst16.py`, `mono.py`, `report.py`, `mkresult.py`, `sat_compile.py`, `controls.py`, `agree.py`, `probe.py`) and `code/__pycache__/` (3 `.pyc`). Workers are `fork`ed, but the parent may still import.
- `fleet11/laneCUBE/code/phase.sh`, `phase2.sh`, `phase3.sh`, `phase4.sh` — the detached phase drivers.
- `fleet11/laneCUBE/logs/` — **currently open for append**: `mono_14.log`, `mono_14_cadical300.log`, `mono_14_glucose42.log`, `mono_14_kissat404.log` (all 0 bytes, all held), plus `phase2.pid`, `phase3.pid`, `phase4.pid` (the kill handles named in `RESULT.md` §9).
- `fleet11/laneCUBE/cubes/` — **actively appended and fsynced**: `joint_W3U4_k14.jsonl` above all, plus `tmp/`. A truncated or moved bank loses banked core-hours permanently.
- `fleet11/laneCUBE/ledger.jsonl` — appended per solve.
- `fleet11/laneCUBE/inst/joint_W3U4.json`, `inst/SUB_U4tgts.json` — asserted byte-identical at process start.
- `fleet11/laneCUBE/found/`, `results/` — the SAT-branch write targets.
- **Outside the lane but load-bearing for it:** `atlas/slp_opt.py` (every search primitive is imported from it, unchanged), `fleet8/unified/code/solver.py` (`key_of` imported, not re-implemented), `fleet8/unified/results/joint_W3U4_preflight.json` (the pinned instance, sha256 `d4916aef…`), and `fleet8/unified/results/joint_levels.jsonl` (the inherited k=9–13 ladder, 233.5 core-hours at k=13 alone — **never re-run it**). None of these may move either.

### 6.2 Two live but **deadlocked** generator processes write into fleet12

```
487378  2d10h  python3 -u generate.py ... --tag laneHALO_b_W3plus4  --out .../fleet12/laneHALO/out/b_W3plus4.json
499379  2d09h  python3 -u generate.py ... --tag laneHALO_b3_W3plus4 --out .../fleet12/laneHALO/out/b3_W3plus4.json
```
Both have cwd `fleet8/unified`, four `<defunct>` children each, 0 % CPU — they are
the `dslp._run_pool` deadlock documented in `laneHALO/RESULT.md` §1.2/§5.1 and were
deliberately **left detached, not killed**. Each holds an **open write handle** on
`fleet12/laneHALO/logs/b_W3plus4.log` / `b3_W3plus4.log` respectively (confirmed via
`/proc/<pid>/fd`). They will never write again, but do not move those two log files
while the PIDs exist, and do not `pkill python3` for any reason. Their intended
outputs (`out/b_W3plus4.json`, `out/b3_W3plus4.json`) were never created and their
verdict was superseded by `out/b4_W3plus4.json`.

### 6.3 A key mismatch that will bite the **next** laneCUBE launch (not the running one)

`fleet11/laneCUBE/code/inst16.py:47-48` pins
`EXPECT_KEY = f04dcb3ecf180a30204434a0bd32453e7635e8b6`, imported from fleet8's own
`key_of`. **laneLIB fix B1 changed that key function**, so the digest is now
`56abd9cb90099824eafda21b81f241bf64fb7eba`. The running processes are safe (the
assertion runs once at start, and workers are forked), but **any fresh launch of
`cube16.py` or `mono.py` will refuse to start**, loudly, naming
`key_matches_recorded`. It fails closed, which is the correct direction. The remedy
is one line in `fleet11/laneCUBE/code/inst16.py`, and `solver.legacy_key_u1(inst)`
reproduces the old digest for confirmation. Documented in full at
`fleet12/laneLIB/RESULT.md` §7 — **the reorganisation wave must carry this note
forward, because the lane cannot be restarted without it.**

### 6.4 Hardcoded absolute paths that a reorganisation would break

Every one of these hardcodes `/home/joebachir20/xor_ui/slp-plateau-search/...`:
- `fleet10/cleanroom/work/satfix*.py` — `SPEC` and `WORK` constants.
- `fleet10/cleanroom/work/collect.sh`, `migrate.sh` — `cd` to an absolute path.
- `fleet11/laneCUBE/RESULT.md` §9's resume commands (documentation, but it is the resume procedure).
- `fleet12/laneHALO/run_chain*.sh`, `run_halo.sh` and the `--out` arguments of the two deadlocked PIDs.
- `fleet9/laneENUM/code/tally.py`, `v2inst.py` and friends resolve `LANE` and `REPO` relative to the repo root; `snapshot/code/*` has its `REPO` constants **patched for relocation and marked in-file** — a second relocation needs the same treatment.

### 6.5 Cross-fleet reads that must not be broken

- `fleet9/laneENUM` reads `campaign_87/agents/hunt-deeper/population88_new.jsonl` (the 54 889-circuit harvest) and byte-copies from `campaign_87/agents/exact-k4/work/`.
- `fleet12/*` all read `fleet8/unified/` and, through it,
  `fleet1/laneA_v2pricing/results/configs.json` — **loaded at module import time on
  every invocation of the generator, including `naive` and `--selftest`** (flag F1).
- `fleet12/laneORDER` appends to the **shared, hash-chained**
  `fleet8/unified/results/prereg.jsonl` (153 entries, chain verified). Two
  concurrent writers break the chain; that is why the whole 75-order sweep ran on
  one core.

---

## 7. GAPS

1. **I did not re-run `fleet9/laneENUM/code/tally.py`.** It is verified read-only
   (it opens files only for reading and prints to stdout), and running it is the
   correct next step for LEAD L2 — but the brief makes this wave read-only and
   "prints a table" is close enough to "produces a new number" that I left it to
   the wave that owns the decision. Same for `fleet12/laneF1/scripts/tally.py` and
   `curve.py` (LEAD L3).
2. **I did not open `fleet12/laneAUDIT/AUDIT_{CORE,DATA,ENGINE}.md` (200 K) beyond
   greps.** The merged `AUDIT.md` supersedes them by construction and its referee
   log states where it diverges; if the public writeup wants the pre-merge
   pre-registrations, those three files hold them.
3. **fleet10's total CPU cost is an estimate, not a measurement.** The BP logs
   record per-restart seconds but no wall totals and there is no ledger; I recovered
   19.5 h of SAT-repair time exactly (`grep -ho 'in [0-9.]*s'`) but the BP side is
   only bounded by log timestamps and restart counters. No ledger exists to fix it.
4. **I could not determine why `fleet10/cleanroom` exists or when it was
   commissioned.** No PREREG, no ledger, no mention in any campaign document, and
   the directory mtime (Aug 24) is all the provenance there is.
5. **`fleet10/cleanroom/work/satquot.py`'s run history is unrecoverable** — no log,
   no output file, no ledger row. I can say it produced nothing that is on disk; I
   cannot say whether it was ever run.
6. **I did not verify circuits in bulk.** Five were verified individually with
   `python3 verify_circuit.py` (all VALID): `fleet10/.../FINAL.json` (93@7),
   `fleet12/laneKNOBS/out/k2d5_rec_ctrl.json` (88@5),
   `fleet9/.../circuits/rho1_88at5.json` (88@5), and all five
   `fleet12/laneHINTS/out/*.json`. The 442 remaining circuit files in the slice are
   reported at the gate counts recorded in their own JSON and their lanes' banks;
   bulk re-verification would need the CPU the solvers own.
7. **The k=14 coverage figure in LEAD L1 is a moving target.** 87/528 was true at
   the moment I counted. Anyone quoting it must re-count from
   `fleet11/laneCUBE/cubes/joint_W3U4_k14.jsonl` at write time.
8. **Whether the 74 duplicate `laneORDER` circuit files may be deleted depends on a
   policy call I cannot make**: their byte-identity *is* the lane's result, so the
   evidence must survive even if the files do not (the `md5sum` output in
   `laneORDER/RESULT.md` already records it, which is why I proposed the deletion at
   all).
9. **Repo-root strays touching this slice:** `wshB1.log`, `wshB2.log`, `wshC1.log`,
   `wshC2.log` at the repository root are **not** duplicates of fleet10's
   identically-named files (md5s all differ; the root ones are 123–124 bytes and
   pair up two-by-two). They look like fleet10-style satfix runs launched from the
   wrong directory. They are outside my slice; flagging so whoever owns the root
   does not assume they are copies.
