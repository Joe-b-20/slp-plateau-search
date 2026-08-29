# Slice report: fleet5 / fleet6 / fleet7 / fleet8

Agent model: Opus 5 (1M context). Date: 2026-08-29. Read-only pass; this file is
the only thing written.

**Summary.** This slice is 9.8 MB across seven lanes and is the *dense* end of the
campaign: it holds almost no bulk data and almost all of the project's
consolidated reasoning. Its centre of gravity is `fleet8/unified/generate.py` — a
working, oracle-verified MixColumns generator that emits 88 and 91–107 and 116
from a *derived* architecture (GF(2^8) + 0x11B + FIPS-197), with depth as a real
constraint, honest count accounting, a hash-chained pre-registration ledger and a
137-cell reachability map. That tool is the single highest-value phase-2 asset in
the slice and probably in the repo. Around it: `fleet5` closed three whole
parameter axes (line-set glue = free by theorem; currency menus ≥ 87 over
1.41e26 configurations; nineteen block boundaries dissolved at exactly zero),
`fleet6/door` decided the campaign's last in-class 87 lead by direct computation
(`MB27B373 = 13`, no 87 through it), `fleet6/laneTOOL2` built and then killed the
integral-residual chain it was built for, `fleet7/laneUNCOND` proved that "make T4
unconditional" *is* the original problem (Theorem U1, refereed) and that the whole
exchange-rate family has a proved ceiling below the record's own regime, and
`fleet7/laneCONSOLIDATE` wrote the two documents the repo-update phase actually
needs (`STATE_OF_THE_PROBLEM.md`, `RECORDS_REPO_PATCH.md`). 26 distinct methods
catalogued, 135 circuit files (9 distinct 88 mask sets), 7 leads. Nothing in the
slice is a deletion candidate beyond 0.6 MB of `__pycache__` and 5 backup files —
**but `fleet8/unified/` is a live dependency of the running `fleet11/laneCUBE` job
and of ~10 fleet12 scripts with hardcoded absolute paths, and must not be moved.**

---

## 1. INVENTORY

Slice total: **9.8 MB, 988 files** (`du -sc fleet5 fleet6 fleet7 fleet8`;
`find fleet5 fleet6 fleet7 fleet8 -type f | wc -l`).

```
fleet5              4.0M   three parameter-relaxation lanes (wave 5)
  laneGLUE           756K  is the block model's LINE-SET confinement costing gates? (no)
  laneMENU           2.3M  is the record-provenanced CURRENCY MENU costing gates? (at most one)
  laneMERGE          1.1M  are the block BOUNDARIES costing gates? (no, 19/21 decided free)
fleet6               584K
  door                24K  a single 24 h solve that decided laneMERGE's last undecided row
  laneTOOL2          556K  the integral residual bound Phi; Theorem T4; L_cf upper bound
fleet7               2.2M
  laneCONSOLIDATE    152K  no compute: the cross-lane state-of-the-problem + records patch
  laneUNCOND         2.1M  proof side: T4's unconditional form; the exchange-rate LP, solved exactly
fleet8               3.1M
  unified            3.1M  THE GENERATOR — one tool replacing three, plus its ledger and maps
```

Per-subdir file-type breakdown (`find <dir> -type f | wc -l`, `du -sh`):

| lane | code | inst | logs | results | ledger | writeup |
|---|---|---|---|---|---|---|
| laneGLUE | 25 f / 208K | 35 f / 144K | 43 f / 180K | 22 f / 152K | 70 rows / 35K | `RESULT.md` 27.7K |
| laneMENU | 15 f / 116K | 140 f / 572K | 149 f / 764K | 6 f / 104K | **2801 rows / 692K** | `RESULT.md` 25.5K |
| laneMERGE | 29 f / 220K | 51 f / 208K | 52 f / 208K | 9 f / 324K | 110 rows / 46K | `RESULT.md` 24.5K |
| laneTOOL2 | 20 f + `verify1/` 22 f | — | 8 f / 36K | 28 f / 132K | 89 rows / 40K | `RESULT.md` 49.5K |
| door | — | 1 f | 1 f | — | — | `README.md` 1.2K |
| laneUNCOND | 11 f + `referee/` 17 f | — | 5 f / 24K | 32 f (19 lpcerts, 1.5M) | 110 + 108 (referee) | `RESULT.md` 69.5K |
| laneCONSOLIDATE | — | — | — | — | 62 rows / 20K | `STATE_OF_THE_PROBLEM.md` 104K, `RECORDS_REPO_PATCH.md` 21.9K |
| unified | 29 f / 352K | 10 f / 44K | 28 f / 124K | 20 f + `reach/` 108 f | **1948 rows / 1.15M** | `RESULT.md` 53.8K, `REACHABILITY.md` 16.3K |

**Documentation status.** Every subdir is well documented — this is the
best-documented slice I would expect in the repo. All seven have a `RESULT.md` or
`README.md`, all seven have an append-only `ledger.jsonl`, and five of the seven
ship a `tally.py`-style re-derivation script so the prose can be regenerated from
the ledger. **Nothing here is opaque.** The one *stale* document is
`fleet8/unified/RESULT.md` (see LEADS L1).

Largest files in the slice, for reference:
`fleet8/unified/ledger.jsonl` 1.15 M · `fleet5/laneMENU/ledger.jsonl` 686 K ·
`fleet8/unified/results/solve_cache.jsonl` 324 K ·
`fleet5/laneMERGE/results/containment.json` 140 K ·
`fleet7/laneCONSOLIDATE/STATE_OF_THE_PROBLEM.md` 101 K ·
19 × `fleet7/laneUNCOND/results/lpcerts/lp_cert_*.json` at ~78 K each.
(`find fleet5 fleet6 fleet7 fleet8 -type f -printf '%s\t%p\n' | sort -rn | head`)

---

## 2. METHODS

26 entries. The unified generator (M1) gets the deepest treatment per the task
brief; M2–M6 are its sub-instruments and are listed separately because each is
independently reusable.

### unified-generator
- **Family:** class-pricing-generator / block-decomposition assembler.
- **What it does:** Emits a complete, oracle-valid MixColumns XOR circuit at a
  requested gate count and depth. It derives a ten-block decomposition of the
  32×32 problem from the field and the matrix alone, solves each block to a
  *proven* minimum with an exact SAT oracle, assembles the union of gate masks,
  schedules them at minimum depth by level-BFS, and verifies the result twice
  (in-process against targets rebuilt from FIPS-197, and by a fresh
  `verify_circuit.py` subprocess). It refuses to emit a circuit that misses the
  request: infeasibility, timeout and solver failure are three distinct exit codes
  (4 / 5 / 7) and none of them is ever reported as the others.
- **Twist vs siblings:** It replaces three earlier generators
  (`fleet2/laneG_generator/generate.py` = recipes only, could not reach 88, and
  `--depth` was a post-hoc *check* that let it emit depth-5 for a depth-4 request;
  `fleet3/laneF4_rule/code/gen.py` = reached 88 but had no depth parameter at all;
  `fleet4/laneDEPTH/code/genD.py` = depth-capped but two configurations and no
  count interface). The three shared no code except a byte-identical `theory.py`
  (md5 `90889a780e1179c5b93a8fff2b5ab3c2`); there is now one copy. Four things are
  genuinely new here: (a) the architecture is *derived* by `code/laws.py` rather
  than tabulated; (b) depth reaches the model in four places rather than being
  read off afterwards; (c) `--count` is checked against the **emitted** count with
  the delta's cause named (mask collisions + dead-gate strip); (d) pre-registration
  is hash-chained and written *before* the solve.
- **Measured performance:** Regression 9/9 rows hit their asked count and verified
  VALID: 116@3, 91@5, 92@4, 93@5, 94@5, 88 (uncapped, emitted at depth 7), 88@5,
  89, 90@5 (`RESULT.md` §6, `results/regression.json`, rebuilt from the ledger by
  `code/regress.py`). Reachability map: 137 cells probed, **33 VALID, 17
  INFEASIBLE, 75 ELSEWHERE, 12 UNDECIDED** (`RESULT.md` §7; the live
  `results/reach_grid.jsonl` now has 138 rows / 13 UNDECIDED — one row of drift).
  Verified (gates, min depth) pairs emitted: 88@5, 89@6, 90@5, 91@4, 92@4, 93@4,
  94@4, 95@4, 96@5, 97@4, 98@5, 99@5, 100@4, 101@4, 102@4, 103@5, 104@4, 105@4,
  108@4, 116@3. Cap-off control **10/10** against `atlas/slp_opt.py` on the ten
  real blocks (`RESULT.md` §3, `logs/capoff.log`). Integrity at hand-off:
  pre-registration chain OK / 55 entries, 12/12 circuits re-verify VALID, ledger
  375 solves + 137 reach cells (`RESULT.md` Appendix). Ledger has since grown to
  **1948 rows / 1028 solves** because fleet12 lanes drive this tool.
- **Cost:** Cheap warm (0.19–0.54 s per regression row from cache); expensive cold
  — 88@5 cold was 4916 s, 90@5 cold 611 s, 89 cold 167 s. The `--map` sweep (stage
  J) ran 2026-08-24 16:45 → 2026-08-25 00:28, ~7.7 h (`logs/phase.log`).
- **Code:** `fleet8/unified/generate.py` (the CLI), `fleet8/unified/code/` —
  `theory.py` (algebra core), `laws.py` (the derivation), `plan.py` (one model
  layer, three plan builders), `dslp.py` (CNF core, optional depth cap),
  `solver.py`, `engine.py`, `assemble.py`, `cells.py`, `ledger.py`, `live.py`.
- **Logs/results:** `fleet8/unified/ledger.jsonl` (1.15 M),
  `results/solve_cache.jsonl` (324 K, 433 rows), `results/prereg.jsonl` (118 K,
  320 rows), `results/reach_grid.jsonl` (44 K, 138 rows), `results/reach/` (108
  circuit files, 436 K), `REACHABILITY.md`, `logs/` (28 files, 124 K).
- **Generality: MIXED — and this is the important paragraph for phase 2.**
  * **CIRCUIT-GENERIC (no change needed):** the whole SAT layer (`dslp.py` —
    gate-position encoding, one-hot pair selection, N1/N2/N3 symmetry breaking, L1
    cone bound, optional level variables, `reach_levels` exact reachability),
    `solver.py` (cache keying, cap-off control, never serving an `error` row),
    `assemble.py` (mask set with collision accounting, `min_depth_schedule`
    level-BFS, `strip_dead_gates`, `verify_inprocess`), `engine.py`, `ledger.py`
    (hash-chained pre-registration), `regress.py`, `reach.py`/`render.py`,
    `capoff.py`, `live.py`. These are a general exact-SLP toolkit and would work on
    any GF(2) linear map.
  * **FIELD-HARDCODED but shared with the inverse:** `code/theory.py:30`
    `AES = 0x11B`. Everything derived from the *field* — the dual basis
    (`build_duals`), the dual xtime chain `xtime_dual_coords`, and therefore
    `QLINES`, `TAPS = {1,3,4}`, `CLEAN`, `PARENT` — comes from 0x11B alone and is
    **unchanged for `aes_inv_mixcolumns`**, which uses the same field. So L0
    (taps), L2 (planes `{k−1,7}`), L3 (shared/unshared ⇒ *tap 3 is the unique
    unshared interface*) and L4 (supplier) all transfer verbatim.
  * **MIXCOLUMNS-HARDCODED (what must change):** three things, all in
    `code/theory.py`:
    1. `mixcolumns_target_masks()` (lines 88–119) — the 32 target rows, from the
       `[2,3,1,1]` circulant. For inv-MixColumns this becomes the `[e,b,d,9]`
       circulant. Mechanical.
    2. `W = 0x7` (line 200), documented as *"the unit factor of c"*, and
       `SECTOR_TARGETS = [(tmul(ypow(j+1), W), tmul(tmul(0x2, ypow(j)), W)) …]`
       (lines 254–257). This is the load-bearing one: it encodes that a
       MixColumns sector target factors as a **p-part on line j plus a q-part on
       `QLINES[j]`** with `c = 3 = 1 + y` and a single unit factor `w = 1+v+v²`.
       The inverse matrix's coefficients do not have this two-part shape, so this
       decomposition — and with it `laws.workset` (L1: `{j} ∪ QLINES[j]`), the
       block line-sets, and the whole ten-block architecture — has to be
       **re-derived, not re-typed**. Expect the inverse's worksets to be wider and
       the block count/dimensions to change.
    3. `sector_value_lines` / `sector_of` (lines 243–274), which assume the same
       (p, q) coordinate shape.
  * **RECORD-PROVENANCED (external, not derivable):** `code/cells.py:32` reads
    `REPO/fleet1/laneA_v2pricing/results/configs.json` for the currency menus and
    the 22 cell definitions, and `code/cells.py:170` reads
    `REPO/fleet2/laneG_generator/results/…` for the ladder spectrum. This is flag
    **F1** and it is live: *every* `f4`-regime price is conditional on a menu read
    off a record circuit. For a new circuit there is no record to read, so
    **phase 2 must either derive menus (lane MENU's `code/derive_menu.py` already
    reads a record-free menu out of a charged witness — this is the wiring job
    fleet8's own §10 item 2 names as the highest-value remaining move) or run the
    `ladder`/`naive` regimes, which are record-free but price 91+.**
  * `code/check_l5.py:13` also `sys.path.insert`s `fleet3/laneF4_rule/code` for the
    L5 comparison control.
- **Phase-2 verdict:** **KEEPER — the crown jewel.** Port order for another
  circuit: (1) swap the target matrix; (2) re-derive the sector (p, q)
  decomposition and `workset` from the new coefficients, keeping `laws.py`'s L2–L5
  reasoning intact; (3) run `--regime naive` for a closed-form baseline, then
  `--regime ladder`; (4) solve the menu problem before attempting the `f4` regime.

### law-derivation (`--explain` / `laws.py`)
- **Family:** structural-analysis, solver-free.
- **What it does:** Derives, as executable code rather than tables, the block
  architecture: which lines each block works on, where each tap's carrier plane
  sits, which planes pay for themselves, which need a dedicated supplier block,
  which already-built values are free to which blocks, and the topological block
  order. `python3 generate.py --explain` prints the whole chain.
- **Twist vs siblings:** Replaces `rule.py`, `prescribe.py` and three lanes'
  hardcoded `ORDER`/`LINES` tables. The headline is that lane F4's hand-written
  "shared-plane RULE" — the one marked edge worth the three gates between 91 and
  88 — is not a rule but a *consequence* of one predicate (L5: a built value is
  free to every block whose workset contains its support).
- **Measured performance:** Against lane F4's hand-written supply at the 88@7
  cell: supply superset **10/10**, prices agree **10/10**, model price 88
  (`results/check_l5.json`, re-derivable by `code/check_l5.py`). W3's supply under
  L5 is *exactly* lane F4's 26 values, D37 included, with no `if name == "W3"`
  anywhere. Also derives the corrected one-gate interface families — **64** on
  {3,7} and **71** on {2,7}, against `planeenum.py`'s 24 and 56.
- **Cost:** milliseconds, no solver.
- **Code:** `fleet8/unified/code/laws.py`, `code/theory.py`, `code/check_l5.py`.
- **Logs/results:** `results/check_l5.json` (3 K); the `--explain` output is
  reproduced in `RESULT.md` §2.
- **Generality:** MIXED — L0/L2/L3/L4/L5 are field-generic (0x11B), L1 is
  MixColumns-specific (see above).
- **Phase-2 verdict:** **keeper.** This is the part that makes the generator
  legible instead of configured, and it is the template for deriving *any*
  circuit's block architecture from its algebra.

### merged-derive (interface derivation by boundary deletion)
- **Family:** SAT / free-supply-derivation.
- **What it does:** To test whether a committed interface value between two blocks
  is real or an artefact of the split, delete the boundary and solve supplier and
  consumer as ONE block. The interface appears neither as a target nor as a free
  input, so the instrument is never told it exists; read the commitment off
  whatever the unconstrained optimum builds.
- **Twist vs siblings:** Unlike free-supply derivation (next entry), it posits no
  candidate family at all, so the vacuity failure mode cannot arise. This is why
  its result stands and the free-supply ones (as originally run) did not.
- **Measured performance:** Merged solve of B27 ∪ W3 on lines [2,3,7]: **exact,
  optimum 9 gates, 572 s**. Among the nine gates exactly one is supported on the
  tap-3 plane, and it is `δ₃(0xc)` — bit-identical to the value lane F4
  configured by hand. Derived rank 1. **This closed the fleet3 referee's
  provenance finding on Q27** and retired the `MATCHED` tag. It also proves 9 is a
  lower bound over *every* commitment of every rank, so the split model does not
  over-price that boundary. `results/derive_merged_Q27.json`, `logs/derive_Q27.log`.
- **Cost:** 572 s at 8 cores.
- **Code:** `fleet8/unified/code/derive.py` (`--derive Q27`).
- **Generality:** CIRCUIT-GENERIC in shape; the block names are MC-specific.
- **Phase-2 verdict:** **keeper — this is the shape to reach for.** The project's
  own conclusion (`RESULT.md` §2b) is that MERGED beats FREE-SUPPLY as a
  derivation method because it cannot be mis-specified.

### free-supply-derive (+ the vacuity guard)
- **Family:** SAT / one-solve-bounds-a-whole-family.
- **What it does:** Offer a block an entire candidate family of interface values at
  *zero* gate cost. Because the family is free, the optimum is a machine-checked
  lower bound for every subset of it simultaneously, and the witness hands back a
  concrete choice. `code/annotate_derive.py` then re-checks every artefact and
  stamps whether the configured commitment was even *inside* the offered family —
  if not, the run is marked VACUOUS as a test.
- **Twist vs siblings:** The vacuity guard is the twist and it is a genuinely
  transferable methodological instrument: it is a machine check against the
  project's own recurring failure mode (a negative that was never given the chance
  to be positive).
- **Measured performance:** At `max_cost = 1` (the shipped default): D37 at W3
  floor 8 over 64 values, D37 at U4 floor 8 (witness took *exactly* the three
  configured values it was offered, 3/3), Q1 at U1 floor 8 over 45 values —
  **3 of 3 stamped VACUOUS**, because the configured values cost 2 gates on their
  planes, not 1. At `max_cost = 2` (re-run 2026-08-27 by fleet12/laneKNOBS through
  this same code): family 200 / 241 / 241, floors **6 / 7 / 7**, **0 of 3
  vacuous**, and the Q1 derive **selects the configured triple exactly, 3/3**.
  Ledger rows `kind=derive_free` and `kind=vacuity_guard` in
  `fleet8/unified/ledger.jsonl`; `results/vacuity_guard.json`.
- **Cost:** cost-1 runs 3169 s / 5312 s / 6925 s; cost-2 runs 551 s / 2076 s /
  2018 s (much cheaper — the wider family makes the instance *easier*).
- **Code:** `fleet8/unified/code/derive.py`, `code/algebra.py`
  (`one_gate_family`, `plane_family(lines, menu, max_cost)`),
  `code/annotate_derive.py`. Env gates: `SLP_DERIVE_MAX_COST`.
- **Generality:** CIRCUIT-GENERIC as a technique. `STATE_OF_THE_PROBLEM.md` §6.1
  W1 calls it *"the single highest-leverage technique in the project"* — it
  replaced a 2^24 point-probe sweep with one solve, and an instance that timed out
  at 4 h twice with a 170 s one.
- **Phase-2 verdict:** **keeper, with the guard mandatory.** Never run a
  free-supply derive without `annotate_derive`'s in-family check.

### rank-curve measurement
- **Family:** SAT / parameter sweep.
- **What it does:** Instead of assuming a law about how many values an interface
  should carry, price supplier + consumer at each rank 0,1,2,3 over the derived
  family and read the optimum off the curve.
- **Twist vs siblings:** It measures a law the charter *states*, and it revised it.
- **Measured performance:** rank 0 → 9, rank 1 → 9, rank 2 → 10, rank 3 → 11. So
  **rank 0 and rank 1 TIE**; the first gate at B27 buys back one gate gross (W3
  9→8), net zero — not the two the charter's law claimed. The merged solve's exact
  9 proves the tie is the floor. `results/derive_rank.json`, `results/rank_Q27.json`,
  `logs/derive_rank*.log`. (`results/rank_Q27.BAD_candidates.json` is the
  self-caught bad first run, retained.)
- **Cost:** ~1600 s total (`logs/phase.log` stage D, 13:38 → 14:05).
- **Code:** `fleet8/unified/code/derive.py --derive rank`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.** Cheap, and it caught a prescribed law being
  wrong.

### capoff-control (two-implementation equivalence)
- **Family:** control / instrument validation.
- **What it does:** Runs the depth-capped solver with the cap switched off on the
  **ten real blocks** of the architecture and checks it reproduces the independent
  plain oracle `atlas/slp_opt.py` gate-for-gate.
- **Twist vs siblings:** It is a genuine two-implementation control, not a
  tautology: `dslp.py` re-implements the base CNF rather than importing it, and
  with `depth=None` no level variable is emitted at all. It runs on real
  instances, not toys.
- **Measured performance:** **10/10 AGREE** (B27 1, B37 4, U07 12, U1 6, S2W 7,
  W3 8, U4 7, S5W/S6W/S7W 7). `dslp` is also 2–7× faster than `slp_opt` on every
  row. `logs/capoff.log`, `logs/ctrl_*.out` (10 files).
- **Cost:** ~6 min total (`logs/phase.log` stage A).
- **Code:** `fleet8/unified/code/capoff.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper — run this first on any new circuit.** It is the
  cheapest possible proof that the fast instrument has not silently diverged.

### reachability-map sweep
- **Family:** systematic probe / measurement.
- **What it does:** Asks the generator for every (count, depth) pair in a grid,
  banks one append-only row per cell, and renders a map distinguishing four
  verdicts: VALID at the asked count; ELSEWHERE (valid but a different count,
  because the mask set de-duplicated); INFEASIBLE (with the *reason* —
  machine-checked depth-unreachability vs. no configuration at that price);
  UNDECIDED (a timeout, never a refutation).
- **Twist vs siblings:** Nothing in the project had this before; the three
  superseded tools reported only the pairs they happened to emit. The
  INFEASIBLE/UNDECIDED separation is the honest part.
- **Measured performance:** 137 cells in `RESULT.md` §7 (33/17/75/12); 138 rows
  and 13 UNDECIDED in the live `results/reach_grid.jsonl`. Standing warning
  recorded in `REACHABILITY.md`: an `infeasible_depth` verdict is a statement
  about *this decomposition*, not about circuits — the repo's own 97@3 is a
  circuit this model cannot express.
- **Cost:** ~7.7 h (stage J, `logs/reach.log` 7 K).
- **Code:** `fleet8/unified/code/reach.py`, `code/render.py`.
- **Logs/results:** `results/reach_grid.jsonl`, `results/reach/` (108 files).
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.** This is the deliverable shape for "what can the
  generator actually do on circuit X".

### regression-suite (subprocess-isolated, thrice-verified)
- **Family:** control / reproducibility.
- **What it does:** Each row is a fresh `generate.py` subprocess run twice (cold,
  then warm) and then verified a *third* time by a separately launched
  `verify_circuit.py`. Rows are rebuilt from the append-only ledger, not from prose.
- **Measured performance:** 9/9 rows hit their asked count and verified VALID
  (table in METHODS entry 1). Notable rows: the 88 uncapped emits at depth **7**,
  not the depth 10 lane F4 reported — same configuration, same block prices,
  different minimal witness, and depth is a property of the mask *set*; the 89
  control must and does honestly report 89.
- **Cost:** warm ~2 s total; cold dominated by 88@5 (4916 s).
- **Code:** `fleet8/unified/code/regress.py`. `results/regression.json`,
  `results/reg_*.json` (8 circuits), `logs/regress*.log`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.**

### joint-block-boundary-test (dim-16 merged ladder)
- **Family:** SAT-joint-levels.
- **What it does:** Takes two adjacent blocks, builds ONE block carrying both
  their targets on the union of their working lines, and climbs the gate ladder
  k = lb, lb+1, … A pre-flight asserts the instance is exactly the union (no
  fabricated free values) *before* any compute is spent. SAT at the decisive level
  means the split model over-prices the boundary and the class drops a gate;
  UNSAT means the boundary is free; a timeout is a bracket.
- **Twist vs siblings:** The pre-flight is the twist and it earned its keep: its
  first run **FAILED**, catching eight fabricated masks that scaffolding had minted
  with `add_chain` and that would have made a day-long dim-16 SAT result worthless.
- **Measured performance:** W3|U4 at the 88@7 cell, dim 16, 8 targets, 33 free
  values = exactly W3's 26 ∪ U4's 25, split total 15, decisive k = 14.
  **k = 9/10/11/12/13 all exhaustively UNSAT** at 23.7 / 123.8 / 785.3 / 5202.2 /
  **105 083.4** s. So `merged ≥ 14`, and with the replay bound `merged ∈ {14, 15}`.
  `results/joint_levels.jsonl` (5 rows), `logs/joint.log`,
  `results/joint_W3U4_preflight.json` (key `f04dcb3e…`).
- **Cost:** 2026-08-25T03:42 → 2026-08-26T11:01, ~31 h on 8 cores; ~16.6× per
  gate level.
- **Code:** `fleet8/unified/code/joint.py` (`preflight()` / `run()`),
  `code/joint_launch.sh`.
- **Generality:** CIRCUIT-GENERIC in shape.
- **Phase-2 verdict:** **keeper**, with the caveat that the level cost multiplier
  (~16.6×/level at dim 16) makes it affordable only for a boundary you have
  already priced. See LEADS L2 — the decisive k = 14 is **not** in this folder.

### conservation-replay-bound
- **Family:** structural-analysis + one exact solve.
- **What it does:** Re-derives the *argument* for a conservation law rather than
  the constant: because the supplier's program can be replayed inside the
  consumer, `B37 + consumer(with commitment) ≥ consumer(with no commitment)`, and
  one exact solve of the right-hand side pins the floor.
- **Measured performance:** U4 with no D37 = **11** (exact, 5263 s); W3 with no
  D37 = **11** (exact, 5856 s). So `B37 + U4 ≥ 11` and `B37 + W3 ≥ 11`, matching
  lane F4's measured invariant and turning it into a proven floor with every
  measured point sitting on it. `results/conservation_D37.json`,
  `logs/derive_cons.log`.
- **Cost:** ~3.1 core-hours.
- **Code:** `fleet8/unified/code/derive.py --derive conservation`, `laws.conservation_statement`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.** The replay bound is the cheapest sound lower
  bound in the toolkit and it is why "one gate in, one gate out" keeps showing up.

### dead-gate-strip + honest-count accounting
- **Family:** circuit post-processing / measurement hygiene.
- **What it does:** (a) removes gates whose output is neither a target nor
  consumed — free and sound; (b) records every mask collision between two blocks
  with both block tags, so the gap between model price and emitted count always
  has a *named* cause. `--count` is checked against the emitted count.
- **Twist vs siblings:** Lane G measured asked-97 → emitted-95 and asked-107 →
  emitted-103 and reported the gap **with no cause**. This names it.
- **Measured performance:** At the 88@7 cell, delta +0 (price 88 = emitted 88, no
  de-duplication). fleet12/laneKNOBS later measured that **five of its 88s exist
  only because the strip runs**, so the strip is not cosmetic.
- **Code:** `code/assemble.py` (`MaskSet.collisions`, `strip_dead_gates`),
  `generate.py:88-119`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper — mandatory.** Any count reported without this is
  unreliable in both directions.

### exact-currency-vs-depth curve (BFS, no solver)
- **Family:** exhaustive enumeration.
- **What it does:** Computes the exact minimum gate count to build a set of
  single-line "currency" values at each depth, by exhaustive BFS over the value
  space — so a currency value's *arrival level* is chosen, not discovered.
- **Twist vs siblings:** No solver at all, and it is what makes depth a constraint
  at the first of four places rather than a post-hoc check.
- **Measured performance:** `algebra.t_min_gates`; exhaustive. Guarded by
  `CurrencyUndecided` — a `kmax` truncation is exit 5, never "impossible" (this is
  fleet12/lane LIB audit defect D5, honoured in `code/algebra.py:95,115,194,207`).
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.**

### min-depth-schedule (level-BFS)
- **Family:** exact scheduling.
- **What it does:** Given a set of gate masks, computes the provably minimum depth
  schedule by level-BFS and returns it.
- **Measured performance:** Used on every emitted circuit; produces the depth
  reported in every regression row. Its soundness argument is stated in
  `RESULT.md` §4: block programs respect the cap at *witness* levels, which
  upper-bound the final BFS levels, so a schedule of depth ≤ D exists and the BFS
  returns the minimum. The tool still hard-traps `depth > D` after emission.
- **Code:** `code/assemble.py:min_depth_schedule`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.**

### hash-chained pre-registration ledger
- **Family:** discipline / methodology.
- **What it does:** Writes the prediction to an append-only file with a sha256
  chain over prior entries **before** the solve runs, and re-verifies the chain on
  demand.
- **Twist vs siblings:** Three earlier lanes had a `ledger.py` that wrote
  predictions at solve *completion* — which is not pre-registration. This one
  cannot be back-dated.
- **Measured performance:** chain OK, 55 entries at hand-off; `results/prereg.jsonl`
  now 320 rows. Across the slice pre-registration converted misses into findings:
  laneMERGE 17 met / 2 MISSED / 3 withdrawn; laneUNCOND 5/5 confirmed with an
  honest note about a mistyped verdict constant; laneMENU's whole 87 theorem was
  pre-registered at 2026-08-22T22:22:08 and came in exactly; laneGLUE had **two of
  its own predictions refuted** and reported both.
- **Code:** `fleet8/unified/code/ledger.py`; sibling implementations in every lane.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper — adopt as the default.**

### glue-census (line-set confinement)
- **Family:** structural-analysis.
- **What it does:** For every gate of every decomposed known circuit, computes the
  value's *line support* and asks whether it lies inside any block's line-set
  ("value-glue") and whether the two operands' joint support does ("joint-glue").
- **Twist vs siblings:** It derives line coordinates by a route using **no field
  arithmetic** (trace duality: `support(m) = {k : m & (0x01010101 << k) ≠ 0}`),
  and cross-checks against lane F4's `build_duals` route on 2000 random masks —
  so agreement is a real independent check, not a shared bug.
- **Measured performance:** 22 circuits, **1970 gates**. The 14 record 88s: 1232
  gates, **0 value-glue, 1 joint-glue**. All 22: 1 value-glue, 2 joint-glue. The
  only value-glue gate anywhere is `91@6` gate 70 on `{2,3,4,7}` and it is
  **removable at zero cost by re-association**. The single genuine violation among
  1232 record-88 gates is `88@6` gate 79, and analysis shows it buys **line-1
  currency, not arithmetic**. This *refuted the charter's premise*: atlas's "3–9
  glue gates per 88" measures sector-confinement, which is strictly finer and does
  not transfer.
- **Cost:** minutes; no solver for the census itself.
- **Code:** `fleet5/laneGLUE/code/glue.py`, `code/census.py`, `code/anat79.py`.
- **Logs/results:** `results/census.json` (11 K), `results/census_gates.jsonl`.
- **Generality:** MIXED — the census is generic; the ladder/line-sets are derived
  by *measuring* each rho-orbit's support-union, which is a technique that
  transfers.
- **Phase-2 verdict:** **keeper.** "Measure the orbit support-unions and see if
  they reproduce your block line-sets" is a cheap first structural probe on any
  new circuit.

### widening-theorem + byproduct-impossibility (G1, G4)
- **Family:** hand-reasoning / theorem, solver-free, with SAT falsification tests.
- **What it does:** G1 proves that letting a block form gate values on *any*
  line-set, up to all eight lines, is exactly free — the value-level
  expressiveness gap is worth zero gates. G4 proves a block running at its base
  price can never emit a value with a component outside its own line-set, closing
  the sharing route the census pointed at.
- **Twist vs siblings:** Both are proofs; the SAT runs afterwards are
  *falsification tests of the proof*, not the evidence for it.
- **Measured performance:** G1 confirmed by 4 widening controls (two at dim 16),
  all at exactly the base price. G4 confirmed on **48/48** exact dim-12 instances
  run *after* the proof, all `capped_unsat`. Two results outside G4's reach were
  measured separately: `D37` minted by `S7W` on `{3,6,7}` ≥ 11 = base; `Q1`
  relocated to `S7W` on `{0,6,7}` ≥ 9 against a budget of 8.
- **Cost:** `results/byproduct.json` is 17.9 K of 48 exact dim-12 solves.
- **Code:** `fleet5/laneGLUE/code/theorems.py`, `code/queue1.py`, `code/queue3.py`.
- **Generality:** the *argument shape* is CIRCUIT-GENERIC; the constants are MC.
- **Phase-2 verdict:** **keeper as a pattern** (prove it, then run the SAT sweep
  as a falsification test — not the other way round). The axis itself is
  **closed** for MixColumns and does not need re-running.

### free-supply single-value and pair census
- **Family:** SAT / exhaustive free-supply.
- **What it does:** For each block, offer every candidate value free, one at a
  time, and record which values are *helpful* and by how much; then repeat for
  pairs.
- **Measured performance:** ~1200 exact solves, **0 timeouts**, across five dim-8
  blocks. **42 genuinely helpful values, every one worth exactly one gate, every
  one of full two-line support.** `B37` closed outright. 241 pair instances: **99
  pairs save two, none saves three.** `results/helpful_*.json`,
  `results/pairs_helpful_*.json`, `results/allhelpful.json`.
- **Cost:** ~9 s per capped dim-8 solve on 4 cores.
- **Code:** `fleet5/laneGLUE/code/queue2.py`, `code/queue4.py`, `code/queue5.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.** "No single free value is worth more than one
  gate, and no pair is worth more than two" is exactly the kind of local-tightness
  fact worth establishing early on a new circuit.

### zero-cost re-association
- **Family:** circuit rewriting.
- **What it does:** Expands a gate's cone to leaves and searches for a
  line-disciplined bracketing of the same value; if one exists using masks already
  present, the offending gate is removed at zero cost.
- **Measured performance:** Removed the corpus's only value-glue gate and emitted
  `results/91at6_glue_free.json` — **91 gates, depth 7, `VERDICT: VALID`**, zero
  value-glue and zero joint-glue. **Re-verified in this pass:** `python3
  verify_circuit.py fleet5/laneGLUE/results/91at6_glue_free.json` → `gates=91
  depth=7 outputs_built=32/32 problems=0 / VERDICT: VALID MixColumns circuit`.
  Applied to `88@6` gate 79 it *fails* and says why: every disciplined bracketing
  needs two intermediates the circuit does not contain, so the disciplined route
  costs two extra gates.
- **Code:** `fleet5/laneGLUE/code/reassoc.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.** Cheap normaliser; also a diagnostic (a
  *failure* to re-associate localises what a gate is really buying).

### menu-space formalisation + rho theorem (solver-free)
- **Family:** structural-analysis / exhaustive enumeration.
- **What it does:** Formalises the currency-menu parameter (the per-line shopping
  list of T-shapes), enumerates it exactly (**1857 buildable shape-sets per line,
  1857⁸ = 1.41 × 10²⁶ configurations**), and proves the menu space carries a
  price-preserving `Z/4` action from byte rotation.
- **Twist vs siblings:** No solver anywhere. It converts an unswept, unflagged
  parameter into a finite object with a known size and a symmetry.
- **Measured performance:** `results/menuspace.json`, `results/rho.json`,
  `results/cells_currency.json` (10 K).
- **Code:** `fleet5/laneMENU/code/menuspace.py`, `code/rho.py`, `code/cells_all.py`.
- **Generality:** MIXED — the *move* (formalise the free parameter, size it, find
  its symmetry) is CIRCUIT-GENERIC and is the right first step for any new
  circuit. The 1857 and the `Z/4` are MC.
- **Phase-2 verdict:** **keeper.**

### charged-group bound (the all-menu theorem)
- **Family:** SAT + concatenation argument.
- **What it does:** Bounds the model price over *every* menu configuration at
  once, by charging each line's currency to exactly one block and summing exact
  per-block free-supply floors over disjoint charged lines.
- **Twist vs siblings:** It is a bound over a 1.41e26-element space obtained from
  ten machine-checked solves, not a sample. And it says *where* the slack is.
- **Measured performance:** **price(C) ≥ 87 for every menu**, against
  price(MENU_88at7) = 88. **Nine of the ten bounds are exactly tight.** The one
  loose gate is the hub: line 7 is read by seven of ten blocks but charged to one,
  and `bound(S7W,{7}) = 10` against a record charge of 11. 87 is the *exact
  ceiling of the one-block-per-group scheme*, not a compute limit. Four blocks
  (U1, B27, B37, W3) are additionally proved **menu-proof** — already at their
  floor at 88@7, so no menu anywhere makes them cheaper. Pre-registered in full
  (assignment, every bound, the total) before the deciding solves ran, and it came
  in exactly. `results/bound.json`.
- **Cost:** ten exact block solves plus 31104 assignment evaluations
  (`code/bound_opt.py`).
- **Code:** `fleet5/laneMENU/code/mmodel.py`, `code/bound_opt.py`, `code/queue_main.py`.
- **Generality:** CIRCUIT-GENERIC as an argument shape (charge disjoint resources
  to single blocks, sum exact floors).
- **Phase-2 verdict:** **keeper — one of the two strongest arguments in the
  slice.**

### cell sweep (price every known menu exactly)
- **Family:** systematic SAT measurement.
- **What it does:** Prices all 21 known cells block by block at the fixed
  interface commitment, cheap blocks first so expensive ones are only spent on
  cells that can still reach 87.
- **Measured performance:** The pre-registered null ("the menu does not matter")
  is **refuted 41 times out of 168** — the menu moves individual blocks by up to 3
  gates (S2W 6..9, U07 9..12, B27 1..3, B37 4..6, U1 6..8, U4 6..8) — **but no
  cell's blocks move together.** **Every one of the 20 distinct known cells prices
  ≥ 88**; nine are pinned at exactly 88, eleven are ≥ 91. The `p88_0x` family
  exhibits perfect break-even seven different ways: `costT(C_0) + U07 = 12`
  constant across seven distinct menus. `results/cellprice.json`.
- **Cost:** 134 solve rows / 1328 result rows in a 2801-row ledger.
- **Code:** `fleet5/laneMENU/code/cellprice.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.** The break-even table is the clearest single
  picture in the slice of *why* 88 keeps appearing.

### derive-menu-from-witness
- **Family:** derivation / provenance removal.
- **What it does:** Reads a **record-free** currency menu out of any charged-group
  optimal witness.
- **Measured performance:** At the 88@7 `U07` control it returns `C_0 = {2,4,7,b}`.
  Written, tested, and **never wired into the generator.**
- **Code:** `fleet5/laneMENU/code/derive_menu.py`.
- **Generality:** CIRCUIT-GENERIC — and this is the piece phase 2 needs most,
  because a new circuit has no record to read menus off.
- **Phase-2 verdict:** **keeper — highest-value unfinished item in the slice.**
  `fleet8/unified/RESULT.md` §10 item 2 and its S1 row both name wiring this into
  `--derive` as the single move that would make the whole `f4` regime record-free.

### merged-group probe (the hub instrument)
- **Family:** SAT-joint-levels.
- **What it does:** Generalises the charged-group bound from one block to a *set*
  of blocks, so a group can share currency internally. Deciding it decides whether
  the all-menu theorem's 87 is real or an artefact of the one-block-per-group
  restriction.
- **Measured performance:** `m_S7W_B27_c7` — group {S7W, B27} on lines {2,6,7},
  dim 12, 34 inputs, 5 targets, line 7 charged. **k = 6,7,8,9,10 all exhaustively
  UNSAT** at 37.1 / 57.1 / 208.1 / 1144.8 / **13140.2** s, so `bound ≥ 11` is
  proven. `k = 11` is the deciding level and was **stopped by the operator**, not
  refuted: ledger `kind=result, tag=m_S7W_B27_c7, status=stopped_by_operator,
  lower_bound=11, lb_kind=bracket, predicted=12`.
- **Cost:** level cost growing ~11×; an UNSAT at k=11 was estimated at ~1.5e5 s
  against ~3.3e4 s remaining.
- **Code:** `fleet5/laneMENU/code/queue_merge.py`;
  `inst/m_S7W_B27_c7_3b1c8975975d.json`, `logs/m_S7W_B27_c7_3b1c8975975d.out`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.** See LEADS L3 — this is an open, priced,
  decisive row.

### block-merge relaxation (the merge lattice)
- **Family:** SAT / relaxation test.
- **What it does:** Dissolves a block boundary by solving two or three blocks as
  ONE exact instance. This relaxes **three** modelling choices simultaneously —
  boundary placement, one-way information flow, and the interface commitment
  (which becomes internal and may be replaced by anything or nothing). A null is
  therefore a theorem about a strictly larger class.
- **Twist vs siblings:** Two properties are machine-checked for every candidate
  before any solve: the **replay bound** (`merged ≤ split`, by concatenating the
  members' own optimal programs) and **strict generality** (an explicit witness of
  one of three kinds — W1 boundary, W2 order, W3 commitment). 349/349 on both.
- **Measured performance:** **Nineteen boundaries dissolved, nineteen times
  exactly the split total.** Plus **131 further candidates settled FREE with no
  solver at all** by admissible bounds. **Seven boundaries dissolved
  simultaneously — 14 of 18 blocks merged into 7 — and the class optimum is still
  exactly 88.** Two undecided: `MB27B373` `[12,13]` (since closed, next entry) and
  `MU07U1` `[10,18]` (timed out at k=17 after 11 879 s, exactly as pre-registered).
  Sharpest rows: `MB273` (deletes the Q27 commitment entirely) = **exact 9**, and
  its unconstrained 9-gate witness's **first gate is `δ₃(0xc)`** — the committed
  interface value, chosen freely. `MB373` = 12 exactly, closed by three
  instruments agreeing. Full table `results/FINAL_TALLY.txt`,
  `results/merge_table.json`, `results/containment.json` (140 K),
  `results/bounds.json` (113 K).
- **Cost:** ladder decisions from 0.7 s to 6674 s; the two undecided rows consumed
  11 766 + 31 681 + 11 879 s of timeout.
- **Code:** `fleet5/laneMERGE/code/mergemodel.py`, `code/enumerate_merges.py`,
  `code/containment.py`, `code/bounds.py`, `code/tally.py`.
- **Generality:** CIRCUIT-GENERIC — this is one of the most transferable methods
  in the slice.
- **Phase-2 verdict:** **keeper.** "Enumerate every boundary, machine-check the
  replay bound and strict generality, then dissolve them" is a complete recipe.

### uncapped-ladder deep-level decision (fleet6/door)
- **Family:** SAT, brute allocation.
- **What it does:** Takes one undecided merge row, hands the *uncapped* instance
  12 cores and a 24 h budget, and lets the ladder re-derive the cheap levels
  before spending everything on the decisive one.
- **Twist vs siblings:** No cleverness — it is the deliberate purchase of one
  decision that two earlier capped attempts (11 766 s and 31 681 s on 4 cores)
  could not afford. It is in the slice as the model of *when to just buy it*.
- **Measured performance:** `MB27B373` (tap-3 interface + shared plane + sector-3
  work as ONE block, dim 12, 21 inputs, 8 targets): **k = 8/9/10/11/12 all
  exhaustively UNSAT** at 2.63 / 10.11 / 96.36 / 994.88 / **19 458.32** s. With
  the replay upper bound of 13 that forces **`MB27B373 = 13` exactly = the split
  total.** The triple boundary is FREE; **12 would have priced the class at 87**,
  and it does not. Verified here independently from
  `fleet6/door/logs/door.out` and `fleet6/door/inst/MB27B373_uncapped.json`.
- **Cost:** ~5.4 h for the decisive level; ~24 h wall.
- **Code:** driven by `atlas/slp_opt.py`; the lane is instance + log + README only.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper as a pattern.** Note `fleet6/door` has **no
  `RESULT.md`** — its decisive result lives in a 170-byte log (see LEADS L4).

### integral residual bound Phi (built, calibrated, and it killed its own chain)
- **Family:** proof-side / CP-SAT + reductions.
- **What it does:** Computes an integral residual quantity `Phi(A)` — a minimum
  cancellation-free program covering a demand set — exactly by CP-SAT, with two
  reductions (R1, R2) that make it seconds instead of hours, and feeds it into the
  chain `|C| ≥ kappa + Y + Phi(A)`.
- **Measured performance:** Calibration test 1 PASSED; **calibration test 2
  FAILED, and the failure is a theorem** — `Phi(A*) ≤ 34` on 88@5fs proves the
  P2/T1 chain cannot reach `L(M) ≥ 84`. It also showed the previously refereed
  "integrality gap ≥ 5" was a **misattribution** (true gap ≤ 0.5351). The tool
  changes no number on any record: `Phi(A*) = ⌈B(A*)⌉` on all five record 88s.
  Replacement chain **T4 is exact `= n` on 9 of 9 circuits**. The load-bearing
  negative was independently rebuilt three ways in `verify1/` (own fixpoint
  checker, explicit hierarchies, separate HiGHS MILP).
- **Cost:** minutes per calibration row after R1/R2.
- **Code:** `fleet6/laneTOOL2/code/` (`t2lib.py`, `phi2.py`, `c2b_calibrate.py`,
  `w1_witness.py`, `x2_repaired.py`), `verify1/` (22 files, independent rebuild).
- **Logs/results:** `results/` 28 files, 132 K; `ledger.jsonl` 89 rows.
- **Generality:** CIRCUIT-GENERIC (it is a statement about SLPs, not about MC).
- **Phase-2 verdict:** **dead-end for bounds, keeper as a calibrated
  instrument.** Its own §7 says "do not fund the integral residual bound"; but
  `phi2.py` + R1/R2 is the machinery `G_int(3)` needs (below).

### adversarial re-wiring census (y1)
- **Family:** falsification by census.
- **What it does:** Takes a large census of known circuits and re-wires each many
  ways, recomputing a claimed invariant, to find the true worst case.
- **Measured performance:** **Refuted Lane P's Y3 (`Y ≥ kappa − 5`)**:
  `min(Y − kappa) = −6` over **3254 census circuits, 43 witnesses**. Pre-registered
  (PRED-10). The corrected constant `Y ≥ kappa − 6` prices at `L(M) ≥ 58`, beating
  the refereed 56 — but it is a measurement over 88s, not a theorem, and one
  further `−7` costs a gate off the 58. 3254 circuits × 16 wirings ran in **132.5 s**.
- **Code:** `fleet6/laneTOOL2/code/y1_census.py`; `results/y1_census.json`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper — the cheapest falsification instrument in the
  slice.** Both laneTOOL2 §7.3 and laneUNCOND §7.3 recommend re-pointing it at a
  different statistic (`|Cl \ U|`) as the next cheap experiment; nobody did.

### L_cf reuse-greedy + CP-SAT upper bound
- **Family:** constructive search.
- **What it does:** A randomised-restart reuse-greedy builds cancellation-free
  programs (each intermediate pool closure-checked), then CP-SAT is seeded with it.
- **Measured performance:** greedy 110 → CP-SAT **103**, closure-verified, no
  optimality in 900 s; a second 1500 s warm start moved nothing.
  `results/lcf_cpsat.json`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **superseded.** The project already held an oracle-verified
  **102** with an artefact on disk (`beat88/.../v2_no_vocab/data/cf_incumbent.json`),
  so the "first upper bound on L_cf" headline is both not first and a regression —
  `STATE_OF_THE_PROBLEM.md` records this as discrepancies D1/D10/D11 and it is
  **uncorrected in `fleet6/laneTOOL2/RESULT.md`**.

### U1 construction (configuration → circuit, oracle-verified)
- **Family:** hand-reasoning / theorem with a machine-checked constructive half.
- **What it does:** Proves that the "unconditional form" of the T4 bound, once
  written with the acyclicity constraint a real circuit forces, is an **equality**
  with `L(M)` — by exhibiting a construction that turns any admissible stratified
  configuration into a circuit of that size.
- **Twist vs siblings:** It is a *retirement* method: it converts "this bound might
  be improvable" into "improving this bound is the original problem".
- **Measured performance:** **REFEREED — CONFIRMED, both halves**, by an
  adversarial agent barred from reading `code/` that wrote its own MixColumns
  rebuild, extractor, rebuilder and exact-`L` solver. The construction ran through
  the repo oracle **10/10 `VERDICT: VALID`** (`results/recon/*.json`, 8 files).
  One real defect found and fixed: the construction needs an explicit
  **earliest-stratum tie-break**. The referee also tested anti-circularity: 68
  MixColumns circuits from **88 to 4621 gates**, and 20 small instances whose
  optimal circuits have `L = 3..8` — the optimal configuration has value exactly
  `L` in all 20, and 500 random admissible configurations produced **zero** with
  value `< L`.
- **Cost:** minutes.
- **Code:** `fleet7/laneUNCOND/code/u1_reconstruct.py`, `code/ulib.py`;
  `referee/` (17 files, its own 108-row ledger).
- **Generality:** CIRCUIT-GENERIC (it is a statement about XOR-SLPs).
- **Phase-2 verdict:** **keeper — a route retired with a reason.** Do not fund
  "make T4 unconditional" for any circuit; it is that circuit's own problem.

### U2 collapse witness (solver-free negative)
- **Family:** explicit-object refutation.
- **What it does:** Refutes a claim by *building the object*, not by failing to
  find one: a perfect matching of the 32 targets into 16 pairs with all three
  overlap conditions, giving `|A| = 48` and an empty demand set.
- **Measured performance:** value **48 < 88**, **11/11 definitional checks, no
  solver**, PRED-1 pre-registered. **REFEREED — CONFIRMED and STRENGTHENED** (the
  referee proved 48 *optimal* in that family by a forest argument).
  `results/collapse48.json`. Corrects `fleet6/laneTOOL2` headline item 8, which is
  **false as a global statement**.
- **Code:** `fleet7/laneUNCOND/code/u2_collapse.py`; `referee/u2.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper.** The template: a negative that is an explicit
  positive object cannot be vacuous.

### exchange-rate LP solved exactly (+ the family ceiling)
- **Family:** LP / certificate.
- **What it does:** The price-table family behind the project's best
  cancellation-free bound had only ever been attacked by subgradient ascent. This
  recognises it as a **finite LP** (~5.9 k variables, ~18.6 k constraints), solves
  it with GLOP, and re-certifies every value with an exactified rational price
  table and a `Fraction` DP.
- **Twist vs siblings:** Exact optimum instead of ascent; and then it proves a
  **ceiling for the whole family**, which is the rarer and more valuable move.
- **Measured performance:** `G*(lam)` at 19 values of lam, all `OPTIMAL`; every
  value **beats** the corresponding CANON table on disk (gains +0.179 to +0.413).
  `G*` is piecewise linear: `= 32·lam` for lam ≤ 5/2, then slope 12, saturating at
  **`B* = 91.409884`** from lam = 7/2. CANON U6-2's certified constant improves
  from `91.0019782` to **`91.4098776`** (exact rational `114262347/1250000`,
  solver-free re-check). Yields the **unconditional, solver-free dichotomy: for
  every XOR-SLP for M, `|C| ≥ 58` or `kappa ≥ 16`** — eight times stronger, in the
  regime that matters, than the standing refereed `kappa ≥ 2`. And the ceiling:
  **no price table and no lam can ever prove `n ≥ 57` for a circuit with
  `kappa ≥ 22`** (rigorous), or `kappa ≥ 20` given the LP optimum — and the
  records have `kappa = 18..28`, so **the exchange rate is capped below the
  record's own regime, by proof.** Bonus: `H_p(lam) = G*(lam)` to the last digit at
  five values of lam, so the `A`-choice integrality is worth **exactly zero**.
- **Cost:** GLOP 60–120 s per lam on 8 threads; 19 lam values.
- **Code:** `fleet7/laneUNCOND/code/lp_g.py`, `code/bstar.py`, `code/dich.py`,
  `code/dich2.py`, `code/hp.py`.
- **Logs/results:** `results/lpcerts/` (19 files, 1.5 M), `results/bstar/`,
  `results/dichotomy*.json`, `logs/lp_*.log`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper as a technique, dead-end as a route.** "Recognise
  the family as an LP, solve it exactly, then bound the whole family" is
  transferable and it is what turned a hope into a closed route.

### provenance audit (DERIVED / MEASURED / ASSUMED template)
- **Family:** methodology / anti-circularity discipline.
- **What it does:** Tabulates **every ingredient** of a lane's chain with four
  columns: where it is used, its provenance (DERIVED from definitions / INHERITED
  / MEASURED on circuits / EXPLICIT WITNESS), *can a hypothetical 87 violate it*,
  and *what breaks if it does*. Circuit-calibrated statements are then explicitly
  **quarantined** — named, and shown to appear in no proof.
- **Twist vs siblings:** It states the **soundness asymmetry** explicitly: for a
  `min over admissible configurations` to be a valid lower bound, the admissible
  set must be a *superset* of every circuit's configuration, so *over*-constraining
  is the circular failure mode and *under*-constraining is merely lossy.
- **Measured performance:** 16 ingredients tabulated (`fleet7/laneUNCOND/RESULT.md`
  §1.3). Result: **not one constraint on admissible configurations is calibrated on
  a known circuit**; the three circuit-calibrated statements (rows m, n, o) are all
  measured on circuits of ≥ 88 gates, an 87 can violate every one, and none is used
  in U1, U2, the dichotomy or the ceiling. The referee's row-1b check was declared
  "the highest-value thing to attack". The sibling table in
  `fleet8/unified/RESULT.md` §8 (DERIVED / MEASURED / ASSUMED / STILL STATIC S1–S5
  / RECORD-PROVENANCED) is the same discipline applied to a generator.
- **Generality:** CIRCUIT-GENERIC — it is pure methodology.
- **Phase-2 verdict:** **keeper — adopt as the required section of every phase-2
  writeup.** This is the direct antidote to the failure mode
  `STATE_OF_THE_PROBLEM.md` identifies as the project's real one: *a regularity
  observed on 88-gate circuits being used to describe circuits that are not 88
  gates.*

### adversarial-referee rebuild
- **Family:** control / independent verification.
- **What it does:** A second agent, **barred from reading the lane's `code/`**,
  rebuilds the definitions, the target matrix, the extractor and an exact solver
  from scratch, and attacks the claims — including with anti-circularity tests on
  circuits and instances *outside* the claimed regime.
- **Measured performance across the slice:** In four referee reports project-wide,
  **no claim marked PROVED was refuted, but several were narrowed and several
  sentences around them were false.** In this slice: laneUNCOND's referee confirmed
  U1 and U2, strengthened U2 to optimality, and found one real construction defect
  (the tie-break). laneTOOL2 has `verify1/` — an independent rebuild with its own
  fixpoint checker, its own hierarchies and a separate HiGHS MILP, three ways on the
  load-bearing negative. Referee code: `fleet7/laneUNCOND/referee/` (17 files, 108
  ledger rows); `fleet6/laneTOOL2/verify1/` (22 files, 28 ledger rows).
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper — mandatory for anything that will be published.**

### cross-lane consolidation / discrepancy audit
- **Family:** documentation / audit, no compute.
- **What it does:** Reads every lane's `RESULT.md` and the public repos, re-derives
  the line numbers and hashes against the *current* checkouts, and produces (a) a
  tiered state-of-the-problem with an evidence hierarchy REFEREED / PROVED /
  MEASURED / CONJECTURED, (b) a costed open-problems table, (c) a
  measured-dead-with-mechanism table, and (d) an explicit **DISCREPANCIES** section
  recording contradictions between files that nobody had caught.
- **Measured performance:** 46 `source_read` rows, **11 `discrepancy` rows**, 2
  verifications, 2 deliverables (`fleet7/laneCONSOLIDATE/ledger.jsonl`, 62 rows).
  Found 11 live contradictions, including: `L_cf`'s upper bound quoted at four
  different values across current documents (D1/D10/D11); the orchestration brief
  carrying three stale figures (D2); three different "known 88s" populations
  (139 878 / 3254 / 14) used interchangeably, with the 139 878 itself corrected to
  105 801 in two other files (D3); the BRIEF still teaching the "radius is the
  failing dimension" diagnosis its own campaign refuted (D8); the known-cell count
  off by one, 20 vs 21 (D9); and a decisive result banked in a log and written up
  nowhere (D7 — `fleet6/door`).
- **Cost:** zero compute.
- **Code:** none; the deliverables are the documents.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper — and this wrap-up campaign is its successor.**
  `STATE_OF_THE_PROBLEM.md` §6 is already 80 % of the method catalog goal 2 asks
  for, at project scale. See ARTIFACTS and LEADS for its staleness.

---

## 3. ARTIFACTS (counts + labels)

### Verified circuits

**135 circuit JSON files** in the slice (files with a `gates` list of pairs).
Command:
```
python3 - <<'EOF'   # counts files whose JSON has a gates list of index pairs
import json,os
n=0
for root in ['fleet5','fleet6','fleet7','fleet8']:
  for dp,_,fn in os.walk(root):
    for f in fn:
      if not f.endswith('.json'): continue
      p=os.path.join(dp,f)
      try: d=json.load(open(p))
      except Exception: continue
      if isinstance(d,dict) and isinstance(d.get('gates'),list) and d['gates'] \
         and isinstance(d['gates'][0],(list,tuple)): n+=1; print(len(d['gates']),p)
print(n)
EOF
```

By gate count (files): **88 × 13**, 89 × 8, 90 × 8, 91 × 12, 92 × 6, 93 × 6,
94 × 10, 95 × 7, 96 × 6, 97 × 3, 98 × 10, 99 × 4, 100 × 5, 101 × 6, 102 × 9,
103 × 6, 104 × 5, 105 × 2, 108 × 1, 116 × 7.

**Distinct 88-gate mask sets: 9** (13 files de-duplicated by mask set). Command:
the script in LEADS-adjacent verification below; the nine are

| label | mask-set hash | file | what it is |
|---|---|---|---|
| split-model 88 | `465fdd759909` | `fleet5/laneMERGE/results/gen_f4_88_D4.json` | laneMERGE's own end-to-end baseline control |
| merged-model 88 | `f651f252e09b` | `fleet5/laneMERGE/results/mergegen_MB273.json` | the merged model's 88, one mask each way from the split's (Jaccard 0.978) |
| unified 88 | `95d6ff65f523` | `fleet8/unified/results/reg_88.json` (+ `reg_88at10`, `reach/f4_f4_88_D4_None`) | fleet8's `f4_88_D4` emission, depth 7 |
| **no-Q27 88** | `21ef55e7f66c` | `fleet8/unified/results/gen_88_noQ27.json` | **the tap-3 interface deleted entirely**; Jaccard 0.978 to the unified 88 — exactly one mask differs |
| 88@5 re-derivation | `8cd07d870dc1` | `fleet8/unified/results/reg_88at5.json`, `reach/f4_rec_88at5_5`, `laneUNCOND/recon_88at5` | a re-derivation of record 88@5 (Jaccard 1.000 measured by lane DEPTH), not a discovery |
| 88@5fs / 88@6 / 88@7 / 88@8 | `68d8…`, `643e…`, `7f45…`, `0525…` | `fleet7/laneUNCOND/results/recon/recon_88at*.json` | **U1-construction rebuilds of known records** — evidence about the theorem, not new circuits |

**Spot re-verification done in this pass** (2 circuits, per BRIEF budget):
```
python3 verify_circuit.py fleet8/unified/results/gen_88_noQ27.json
  -> gates=88 depth=8 outputs_built=32/32 problems=0 / VERDICT: VALID MixColumns circuit
python3 verify_circuit.py fleet5/laneGLUE/results/91at6_glue_free.json
  -> gates=91 depth=7 outputs_built=32/32 problems=0 / VERDICT: VALID MixColumns circuit
```

**Publishable-candidate circuits already flagged by laneCONSOLIDATE §6** (all
oracle-verified, all with a mandatory caveat): `fleet5/laneMERGE/results/mergegen_MB273.json`
(88 @ depth 10) and `fleet5/laneGLUE/results/91at6_glue_free.json` (91 @ depth 7).

### UNSAT / bound certificates

| label | count | what exactly it certifies | path | command |
|---|---|---|---|---|
| joint W3\|U4 level ledger | **5 rows** (k = 9,10,11,12,13 UNSAT) | the merged dim-16 W3∪U4 block needs **≥ 14** gates; with the replay bound, merged ∈ {14,15} | `fleet8/unified/results/joint_levels.jsonl` | `cat fleet8/unified/results/joint_levels.jsonl` |
| `MB27B373` decision | 5 levels (k = 8..12 UNSAT) | the triple merge = **13 exactly** = split; **no 87 through it from either side** | `fleet6/door/logs/door.out` | `cat fleet6/door/logs/door.out` |
| hub merged-group bracket | 5 levels (k = 6..10 UNSAT) | `bound({S7W,B27},{7}) ≥ 11`; k = 11 undecided (operator stop) | `fleet5/laneMENU/logs/m_S7W_B27_c7_3b1c8975975d.out` | `cat` that file |
| merge lattice | **21 rows**: 19 FREE, 2 UNDECIDED | each dissolved boundary prices exactly the split total | `fleet5/laneMERGE/results/FINAL_TALLY.txt` §B | `cat` |
| no-solver merge bounds | **131** | admissible lower bound already equals split | `fleet5/laneMERGE/results/bounds.json` | `python3 fleet5/laneMERGE/code/tally.py` |
| containment + generality | **349 / 349** | replay bound holds and the merge is strictly more general (W1/W2/W3 witness each) | `fleet5/laneMERGE/results/containment.json` | `python3 fleet5/laneMERGE/code/containment.py` |
| G4 byproduct falsification | **48 / 48** `capped_unsat` | no block at base price emits a foreign-line value | `fleet5/laneGLUE/results/byproduct.json` | — |
| all-menu bound | **10** block bounds, 9 tight | `price(C) ≥ 87` over **1.41e26** menu configurations | `fleet5/laneMENU/results/bound.json` | `python3 fleet5/laneMENU/code/bound_opt.py` |
| cell sweep | **20 distinct cells** (21 named) | every known cell prices ≥ 88 | `fleet5/laneMENU/results/cellprice.json` | `python3 fleet5/laneMENU/code/cellprice.py` |
| exchange-rate LP certificates | **19** `lp_cert_*.json` (1.5 M) + 1 `nostop_lp_cert` | exact `G*(lam)` at 19 lam values; `B_p = 114262347/1250000 ≥` ⇒ `L_cf(M) ≥ 92` | `fleet7/laneUNCOND/results/lpcerts/`, `results/bstar/` | `ls fleet7/laneUNCOND/results/lpcerts \| wc -l` |
| dichotomy tables | 27 exact price tables (8 CANON + 19) | `\|C\| ≥ 58` **or** `kappa ≥ 16`, unconditional and solver-free | `fleet7/laneUNCOND/results/dichotomy*.json` | `python3 fleet7/laneUNCOND/code/dich.py` |
| U2 collapse witness | 1 | T4's unconditional form as stated by laneTOOL2 §5.3 has value ≤ 48 | `fleet7/laneUNCOND/results/collapse48.json` | `python3 .../code/u2_collapse.py` |
| conservation floors | 2 exact solves | `B37 + U4 ≥ 11`, `B37 + W3 ≥ 11` | `fleet8/unified/results/conservation_D37.json` | `cat` |
| cap-off control | **10 / 10** | `dslp(cap off) ≡ atlas/slp_opt.py` on the ten real blocks | `fleet8/unified/logs/capoff.log` | `cat` |
| banked partial bounds from timeouts | **20 rows** | each names a `lower_bound_proven` under a timeout — a bracket, never a refutation | `fleet8/unified/ledger.jsonl` | see LEADS L5 for the extraction command |

### Writeups

**10 markdown documents, 394 KB.** Command:
`find fleet5 fleet6 fleet7 fleet8 -name "*.md" -printf "%s %p\n" | sort -rn`

`STATE_OF_THE_PROBLEM.md` 104 K · `laneUNCOND/RESULT.md` 69.5 K ·
`unified/RESULT.md` 53.8 K · `laneTOOL2/RESULT.md` 49.5 K · `laneGLUE/RESULT.md`
27.7 K · `laneMENU/RESULT.md` 25.5 K · `laneMERGE/RESULT.md` 24.5 K ·
`RECORDS_REPO_PATCH.md` 21.9 K · `unified/REACHABILITY.md` 16.3 K ·
`door/README.md` 1.2 K.

### Ledgers (append-only)

**9 ledgers, 5326 rows total.** Command:
`for f in fleet5/*/ledger.jsonl fleet6/*/ledger.jsonl fleet6/laneTOOL2/verify1/ledger.jsonl fleet7/*/ledger.jsonl fleet7/laneUNCOND/referee/ledger.jsonl fleet8/unified/ledger.jsonl; do echo "$f $(wc -l < $f)"; done`

| ledger | rows | dominant kinds |
|---|---|---|
| `fleet8/unified/ledger.jsonl` | **1948** | solve 1028, prereg 320, generate 270, reach_cell 138, vacuity_guard 65 |
| `fleet5/laneMENU/ledger.jsonl` | **2801** | predict 1330, result 1328, solve 134 |
| `fleet5/laneMERGE/ledger.jsonl` | 110 | solve 42, merge 24, prereg 22, satprobe 8 |
| `fleet7/laneUNCOND/ledger.jsonl` | 110 | Bp_exact 33, lp_G_star 19, u1_reconstruct 10 |
| `fleet7/laneUNCOND/referee/ledger.jsonl` | 108 | the referee's own independent ledger |
| `fleet6/laneTOOL2/ledger.jsonl` | 89 | circuit_measure 11, prereg 11, T4_repaired_chain 11 |
| `fleet5/laneGLUE/ledger.jsonl` | 70 | solve 35, prereg 12, result 11 |
| `fleet7/laneCONSOLIDATE/ledger.jsonl` | 62 | source_read 46, **discrepancy 11** |
| `fleet6/laneTOOL2/verify1/ledger.jsonl` | 28 | the independent rebuild's ledger |

Plus 4 solve caches: `fleet8/unified/results/solve_cache.jsonl` 433 rows,
`fleet5/laneMENU/results/cache.jsonl` 134, `fleet5/laneMERGE/.../cache.jsonl` 42,
`fleet5/laneGLUE/.../cache.jsonl` 35. And `fleet8/unified/results/prereg.jsonl`
320 rows (hash-chained).

### Raw logs and instances

**286 log files / 1.34 MB**; **237 instance files / 968 KB**. Command:
`for d in fleet5/lane* fleet6/* fleet7/laneUNCOND fleet8/unified; do find $d/logs $d/inst -type f 2>/dev/null; done | wc -l` and `du -sh` per dir (table in §1).
Largest: `fleet5/laneMENU/logs/queue_main*.out` (6 files, 27–34 K each — the
sequential queue transcripts).

---

## 4. KEEP / DELETE proposal

**Headline: keep essentially everything.** The whole slice is 9.8 MB and there is
no bulk regenerable data in it — no CNF dumps, no cube files, no large scratch.
Total reclaimable is **~0.6 MB**, which is not worth the risk.

| item | size | verdict |
|---|---|---|
| All `RESULT.md` / `README.md` / `REACHABILITY.md` / `STATE_OF_THE_PROBLEM.md` / `RECORDS_REPO_PATCH.md` | 394 K | **KEEP.** Primary results; two of them are the repo-update phase's raw material. |
| All 9 `ledger.jsonl` + 4 `cache.jsonl` + `prereg.jsonl` | ~2.4 M | **KEEP.** Append-only sources of truth; every `RESULT.md` number re-derives from them and several `tally.py` scripts depend on them. `fleet8/unified/ledger.jsonl` additionally holds results that exist **nowhere else** (LEADS L1, L5). |
| All `code/`, `verify1/`, `referee/` directories | ~1.3 M | **KEEP.** This is the method catalog's substance and phase 2's toolkit. |
| All 135 circuit JSON files | ~130 K | **KEEP.** Cheap, oracle-verified, and 9 distinct 88 mask sets is real data. |
| `fleet7/laneUNCOND/results/lpcerts/` (19 files) + `bstar/` | 1.5 M | **KEEP.** These are the *certificates* behind `L_cf(M) ≥ 92`, the dichotomy and the family ceiling. Regenerating needs GLOP + ~20 min/cert and the exactified rationals. Largest single block in the slice and still worth keeping. |
| `fleet5/laneMERGE/results/containment.json` + `bounds.json` | 253 K | **KEEP.** The 349/349 machine-check and the 131 no-solver rows; regenerable but slow and load-bearing for the "strictly more general class" claim. |
| All `inst/` (237 files, 968 K) | 968 K | **KEEP.** Instances are hashed into cache keys; `fleet8/unified/results/joint_W3U4_preflight.json` in particular is **read by the running fleet11/laneCUBE job**. |
| All `logs/` (286 files, 1.34 M) | 1.34 M | **KEEP.** Several decisive results exist ONLY in a log — `fleet6/door/logs/door.out` (170 bytes, decides `MB27B373`) and `fleet5/laneMENU/logs/m_S7W_B27_c7_*.out` (the hub bracket). |
| `fleet8/unified/results/reach/` (108 circuit files) | 436 K | **KEEP.** Each is an emitted, verified circuit backing one reachability cell. |
| **`__pycache__/` — 9 directories** | **556 K** | **DELETE-CANDIDATE.** Pure build artefacts, regenerated on import. Command: `find fleet5 fleet6 fleet7 fleet8 -name __pycache__ -type d`. **Caveat: `fleet8/unified/code/__pycache__` (236 K) belongs to code the LIVE fleet11/laneCUBE job imports** — deleting it is harmless (Python regenerates it) but do it when nothing is mid-import. |
| **`.bak` / `.prelive` backups — 5 files** | **58 K** | **DELETE-CANDIDATE, with a note.** `fleet8/unified/code/derive.py.bak`, `generate.py.prelive`, `code/assemble.py.prelive`, `code/engine.py.prelive`, `code/solver.py.prelive`. These are pre-`--live`-instrumentation snapshots; git holds the history. **KEEP if the repo does not actually have these files committed** — check `git log --oneline -- fleet8/unified/code/solver.py` first. |
| `fleet8/unified/results/rank_Q27.BAD_candidates.json` | 850 B | **KEEP.** A self-caught bad run, deliberately retained; it is evidence of the discipline. |
| `fleet8/unified/logs/joint_launch_stdout.log`, `verify1/sat.log`, `verify1/sat2.log` | 0 B | **KEEP** (zero-cost; their existence records that a stage was launched). |
| `fleet8/unified/results/joint.lock` | 26 B | **KEEP** — see HAZARDS. |
| `fleet6/laneTOOL2/verify1/` | 112 K | **KEEP.** Independent rebuild of a load-bearing negative; deleting it would delete the second party. |

---

## 5. LEADS

Seven. Confidence labelled per the BRIEF.

### L1 — `fleet8/unified/RESULT.md` is STALE, and the fix it recommends was already run with the numbers moving. **[VERIFIED-IN-LOG]**

`RESULT.md` §2b reports all three free-supply derivations as **VACUOUS**, floors
**8 / 8 / 8**, over the `max_cost = 1` families of 64 / 64 / 45 values, and its §10
item 3 lists *"re-run the free-supply derives over `plane_family(..., max_cost=2)`
— only the compute was missing"* as future work. **That re-run happened on
2026-08-27** through this same code, and the numbers are in this folder's ledger:

```
python3 -c "
import json
for l in open('fleet8/unified/ledger.jsonl'):
  d=json.loads(l)
  if d.get('kind') in ('derive_free','vacuity_guard'):
    print(d.get('t'),d.get('kind'),d.get('iface'),d.get('consumer'),
          d.get('family_size'),d.get('min_gates') or d.get('floor'),d.get('vacuous'))"
```

| derivation | family | floor | in-family | agrees | vacuous |
|---|---|---|---|---|---|
| Q1 at U1 | **200** (`plane_family(max_cost=2)`) | **6** (was 8) | 3/3 | **3/3 — all of them** | **false** |
| D37 at U4 | **241** | **7** (was 8) | 4/4 | 2/4 | **false** |
| D37 at W3 | **241** | **7** (was 8) | 4/4 | 0/4 | **false** |

Three consequences, in decreasing certainty:

1. **The `Q1` derive is repaired and it selects the configured triple exactly.**
   That is a real provenance gain that `fleet8/unified/RESULT.md` does not record.
2. **`STATE_OF_THE_PROBLEM.md` §5.3 is now wrong.** It lists as *open and
   untouched*: *"The multi-gate shared-plane family. Lane F4's `W3 ≥ 8` is closed
   for all 64 one-gate values; a `D37` containing 2-gate values could in principle
   drive `W3` to 7. Untouched."* It is no longer untouched — **W3's floor over all
   241 ≤2-gate `{3,7}` commitments is measured at 7**, and U4's likewise.
3. **It does not yield an 87** — `fleet12/laneKNOBS/RESULT.md` §6 costed it and
   reports the derive-nominated `D37` **prices 89**: the consumer saves a gate and
   the supplier pays it back. This is another instance of the slice's dominant
   pattern (see L7). So the lead is *closed*, but the closure is recorded in
   fleet12 and **not** in fleet8, and three documents in this slice still state the
   superseded numbers.

**Also inconsistent within the folder:** `results/derive_free_*.json` (mtime
2026-08-25) still hold the OLD `family_size: 64/45, floor 8, VACUOUS: true` rows,
while `results/vacuity_guard.json` (mtime 2026-08-27) holds the NEW `floor 7/7/6,
vacuous: false` stamps. **The artefacts and their own guard disagree.** Anyone
re-running `code/annotate_derive.py` without the env variables set will silently
flip them back. *Action for the wrap-up: fold the cost-2 rows into
`fleet8/unified/RESULT.md` §2b and §10, and correct `STATE_OF_THE_PROBLEM.md` §5.3.*

### L2 — the joint W3|U4 test's decisive level k = 14 is NOT in this folder, and the job reported DONE without writing a verdict. **[VERIFIED-IN-LOG]**

`logs/joint_status.log` reads `JOINT DONE 2026-08-26T11:01:14`. But
`results/joint_levels.jsonl` stops at **k = 13**, `logs/joint.log` stops at k = 13,
and **`results/joint_W3U4_result.json` — the file `RESULT.md` §10 names as the
final verdict — does not exist.** The k = 13 UNSAT landed at 09:52:29, so roughly
69 minutes of k = 14 ran and produced nothing. (`results/joint.lock` still holds
pid `82529` from 03:42:14.)

What IS banked and is a real, permanent result: **k = 9..13 all exhaustively
UNSAT** ⇒ `merged(W3∪U4) ≥ 14`, and with the replay bound `merged ∈ {14, 15}`.
That already kills the two-gate saving. Only the one-gate question is open, and
the BRIEF says the k = 14 test is now running in `fleet11/laneCUBE` (which reads
`fleet8/unified/results/joint_W3U4_preflight.json` and imports fleet8's own
`key_of` — confirmed at `fleet11/laneCUBE/code/inst16.py:4-12`).

*Action: when laneCUBE finishes, the verdict must be written back into
`fleet8/unified/results/joint_W3U4_result.json` or the ledger, or this folder will
permanently read "DONE, no answer".* Note also that `results/joint_levels.jsonl`
is the **only** record of the 105 083 s k = 13 UNSAT — 29 core-hours in one 381-byte
file. Back it up before any reorganisation.

### L3 — the all-menu theorem's last gate is an open, priced, decisive row that was stopped by the operator, not refuted. **[VERIFIED-IN-LOG]**

`fleet5/laneMENU` proves `price ≥ 87` over 1.41e26 menus, with **nine of ten bounds
exactly tight**, and localises the single loose gate at the hub. The deciding
instrument `m_S7W_B27_c7` reached **k = 6,7,8,9,10 all exhaustively UNSAT** (37.1 /
57.1 / 208.1 / 1144.8 / 13140.2 s), proving `bound ≥ 11`. The ledger row reads
`status: stopped_by_operator, lower_bound: 11, lb_kind: bracket, predicted: 12`.

**k = 11 UNSAT ⇒ merged = 12 ⇒ the total bound rises 87 → 88 and flag F1 closes
outright.** k = 11 SAT ⇒ the loose hub gate is real. Estimated ~1.5e5 s against
~3.3e4 s remaining when it was stopped, and the lane states the asymmetry
explicitly: SAT is found far faster than UNSAT is proved, so *the row is much more
likely to report if the answer is the disappointing one.* Instance
`inst/m_S7W_B27_c7_3b1c8975975d.json`, driver `code/queue_merge.py`.

This is, together with L2, the **only unpurchased decisive computation in the
slice**, and it is the cheaper of the two. If any compute is ever spent on this
project again, this row is the one that closes a flag.

### L4 — `fleet6/door` has no `RESULT.md`; its decisive answer lives in a 170-byte log. **[VERIFIED-IN-LOG]**

`fleet6/door/logs/door.out` is five lines. Line 5 — `[sat] k=12: UNSAT
(19458.32s)` — combined with the inherited replay bound of 13, **decides
`MB27B373 = 13` exactly**, closes `fleet5/laneMERGE`'s last undecided in-class 87
lead, and forecloses the branch where **12 would have priced the class at 87**.
`laneCONSOLIDATE` flagged this as discrepancy D7; `fleet8/unified/RESULT.md` §10
item 5 picked it up and independently re-derived it from the log and the instance.
But `fleet5/laneMERGE/RESULT.md` §2a still reads `[12,13] UNDECIDED` and
`results/FINAL_TALLY.txt` still reads `MB27B373 ... UNDECIDED`. *Action: this is
the cheapest correction in the slice — one row of one table, plus a three-line
`RESULT.md` in `fleet6/door`.*

### L5 — 20 banked partial bounds from timed-out solves, sitting in one ledger, never tabulated. **[VERIFIED-IN-LOG]**

Every one of these is a proven `lower_bound_proven` under a timeout — a bracket,
never a refutation — and no document in the slice collects them.

```
python3 -c "
import json
for l in open('fleet8/unified/ledger.jsonl'):
  d=json.loads(l)
  if d.get('status')=='timeout':
    print(d['t'],d['block'],'tag=',d.get('tag'),'cap=',d.get('depth'),
          'lb=',d['lower_bound_proven'],'wall=',d['wall'])"
```

The ones fleet8 itself banked, which `RESULT.md` §10 item 4 partly reports:
**`W3` at D = 3 is exhaustively UNSAT below k = 11**; **`U1` at D = 4 below k = 9**
(both 900 s); `W3` uncapped below k = 10 at the reach cells. These are two fresh
partial bounds on the *depth-4 rung wall* — `W3` at D = 4 on the 88@5 cell is the
single solve between the repo and a verified **90 @ 4**, and lane DEPTH's attempts
timed out at 36 000 s with `k ≤ 10` exhaustively UNSAT.

The later rows (2026-08-27, `laneF1_*` / `laneKNOBS_*` / `laneHINTS_*` tags) are
fleet12's, but the data lives here: `U07` uncapped with a record-free menu is
**≥ 14** (30 565 s), against 12 at the record menu; `S2W` uncapped is **≥ 11** at
two record-free menus (19 185 s, 18 014 s), against 7 at the record menu.
**Off-record menus cost real gates and the brackets prove it.** That is a
quantitative statement about flag F1 that neither `laneMENU/RESULT.md` nor
`unified/RESULT.md` contains. *Action for goal 3: this is a countable artifact
class ("N proven partial bounds banked from timeouts") worth publishing honestly.*

### L6 — the two cheapest named-and-never-run experiments in the slice. **[PLAUSIBLE]**

Both are named by their own lanes as the next thing to do, both are cheap, and
neither has a successor anywhere in the repo:

1. **Re-point the y1 census at `|Cl \ U|`.** `fleet7/laneUNCOND` §7.3: run
   `fleet6/laneTOOL2/code/y1_census.py` (3254 circuits, **132.5 s** for 3254 × 16
   wirings) with `|Cl \ U|` as the statistic instead of `Y`, and find the true
   worst case of `kappa − |Cl \ U|`. `|Cl \ U|` is **13–22 on every circuit from 88
   to 92 gates** and is *invisible to every price certificate in the program* —
   U6-2, U6-3, Lane P's `B`, laneTOOL2's `Phi` all live on `U`. The strengthened
   chain reads **78–85 against n = 88..92**, versus 65–73 for `kappa + |counted|`.
   The lane calls this "the cheapest identified place to look for the missing
   increasing-in-kappa term", and it is a *falsification* first: if it degrades the
   way `Y − kappa` did, the route dies for a day of compute.
2. **A certified rational upper bound on `B*`.** `fleet7/laneUNCOND` §7.5: the LP
   dual is **already computed**; it only needs exactifying. It would prove the U6-2
   certificate form can never reach `L_cf ≥ 93`, resolve CANON U6-2's own flagged
   inconsistency about the HiGHS dual bounds 92.60 / 92.30, and make the family
   ceiling rigorous at `kappa ≥ 20` instead of 22. Priced at ~1 session.

Also unbought and priced: `G_int(3)` to a referee-grade lower bound
(`laneTOOL2` §7.4 / `laneUNCOND` §7.4). Payoff exactly: `G_int(3) ≥ 92` moves the
dichotomy from `kappa ≥ 16` to **`kappa ≥ 18`**; `≥ 94` gives 19. **No larger value
is reachable** — laneUNCOND's ceiling applies to `G_int` verbatim, so the route
still dies at `kappa ≥ 22`, below the records' own `kappa = 18..28`. The named
unexploited lever is **rho-symmetry breaking over the 8 `Z/4` orbits**, which
neither the `G_int(3)` nor the exact-`L_cf` encoding uses at all. *This is a lead
with a known ceiling — worth flagging precisely because someone might otherwise
fund it expecting more.*

### L7 — the structural evidence about WHY 88 keeps appearing, from four independent instruments in this slice. **[VERIFIED-IN-LOG]**

This is the slice's contribution to the optimality question, and it is worth
stating as one paragraph because four unrelated methods produced the same shape:

* **Merges: 19 boundaries dissolved, 19 times exactly the split total**, plus 131
  no-solver FREE rows, plus 7 boundaries dissolved *simultaneously* (14 of 18
  blocks into 7) still landing at exactly 88.
* **Menus: `costT(C_0) + U07 = 12` constant across seven distinct menus.** Each
  gate spent on line-0 currency buys back exactly one gate of `U07`, **never two** —
  the same conservation, realised seven independent ways
  (`fleet5/laneMENU` §4.1).
* **The shared plane: `B37 + U4 ≥ 11` and `B37 + W3 ≥ 11`** as proven floors, with
  every measured point sitting on them (`fleet8/unified/results/conservation_D37.json`);
  and the tap-3 rank curve where rank 0 and rank 1 **tie** at 9, the merged solve
  proves 9 is the floor over every commitment of every rank, and there is a valid
  **88 with no tap-3 interface at all** differing from the configured 88 by exactly
  one mask. *A rank-1 unshared interface relocates one gate; it does not save one.*
* **The cost-2 shared-plane family (L1 above): consumer floor drops 8 → 7 and the
  supplier's price rises to 89.** One gate in, one gate out, again.

Two instruments at different scales — fleet8's merged B27∪W3 returning exactly 9,
and fleet6/door's triple merge returning exactly 13 — agree that **the split block
model does not over-price the R34 boundary anywhere.** Against that,
`STATE_OF_THE_PROBLEM.md` §7.2's honest counterweight stands unchanged and is the
right place to point a successor: every "88 is the class optimum" statement is
class-conditional; the class's own load-bearing assumption (lane A's wiring
condition, flag F3) is **measured on 22 circuits with one exception and never
proved**; and the only evidence for the block strata is a 14-for-14 regularity
among **88**-gate circuits — *exactly the population that would look regular if 87
lived somewhere else.* Nothing in this slice touches that.

---

## 6. HAZARDS

**H1 — `fleet8/unified/` MUST NOT BE MOVED, RENAMED OR HAVE ITS `code/` EDITED.**
It is live shared infrastructure, not a finished lane.
* The **running** `fleet11/laneCUBE` job depends on it:
  `fleet11/laneCUBE/code/inst16.py` reads
  `fleet8/unified/results/joint_W3U4_preflight.json` and *imports* `key_of` from
  `fleet8/unified/code/solver.py`; `fleet11/laneCUBE/code/probe.py` opens the same
  preflight by **absolute path**; `fleet11/laneCUBE/code/sat_compile.py` imports
  fleet8's modules read-only and redirects every write.
* ~10 fleet12 scripts `cd` into it or `sys.path.insert` it by **absolute path**:
  `fleet12/laneHINTS/run_step2.sh`, `run_step2b_rec88at7.sh`, `run_step3a_U1.sh`,
  `run_step3b_all.sh`, `run_step3c_noQ27.sh`; `fleet12/laneHALO/run_halo.sh`,
  `run_pairs.py:54`, `run_b4.py:67`, `run_u07.py:61`;
  `fleet12/laneORDER/run_order.sh:30`, `enum_orders.py:13`,
  `probe/supply_probe.py:20,24`.
* `fleet9/laneENUM/code/f4inst.py` runs a **snapshot copy** of fleet8's plan+engine.
* Its `ledger.jsonl` and `results/prereg.jsonl` are **shared writable state**:
  `fleet12/laneORDER/sweep.py:10` and `run_order.sh:15` warn that the hash chain is
  *only safe under a single writer*. Rows were appended as recently as
  **2026-08-27T18:23**. Do not truncate, rewrite or reformat either file.

**H2 — `fleet8/unified/results/joint.lock`** (26 bytes, `82529 2026-08-25T03:42:14`)
is the single-instance lock for the joint solve. Leave it; deleting it invites a
second concurrent joint run.

**H3 — outbound absolute/relative path dependencies from the slice.** Reorganising
*other* directories breaks code in mine:
* `fleet8/unified/code/cells.py:32` → `fleet1/laneA_v2pricing/results/configs.json`
  (the menus and 22 cell definitions — **flag F1's physical location**);
  `cells.py:170` → `fleet2/laneG_generator/results/` (the ladder spectrum).
  Moving either kills every `f4`- and `ladder`-regime run.
* `fleet8/unified/code/check_l5.py:13` → `fleet3/laneF4_rule/code`.
* `fleet5/laneMENU/code/cells_all.py:12,17` → `fleet3/laneF4_rule/code` and
  `fleet1/laneA_v2pricing/results/configs.json`; same for `laneMENU/code/queue1.py`,
  `derive_menu.py`, `queue_main.py`, `rho.py`, `menuspace.py` via `M.F4`.
* `fleet5/laneGLUE/code/gmodel.py:27,268` → `atlas/slp_opt.py` and
  `fleet3/laneF4_rule/code`.
* `fleet7/laneUNCOND/code/dich2.py:31` → `beat88/understanding/u6_spec87` (the
  8 CANON price tables the dichotomy consumes).
* `fleet7/laneUNCOND/referee/h0.py:15,17` → hardcoded
  `/home/joebachir20/xor_ui/slp-plateau-search` and
  `evidence/circuits/mixcolumns_88gates_depth5.json`.
* Every generator/emitter resolves `REPO/verify_circuit.py` and `REPO/experiments/`
  by walking two directories up from the lane (`generate.py:50-61`,
  `fleet5/laneMERGE/code/mergegen.py:114,155`, `fleet5/laneGLUE/code/reassoc.py:135`,
  `fleet8/unified/code/joint.py:169-185`). **Changing the depth of any lane
  directory silently redirects the FOUND/STOP protocol.**
* Shell drivers with hardcoded `cd`: `fleet5/laneMERGE/code/queue1.sh`,
  `queue3.sh`, `queue5.sh`; `fleet6/laneTOOL2/code/run_wave{,2,3}.sh`,
  `run_final.sh`.

**H4 — decisive results that exist in exactly one small file.** Losing any of
these loses a bought computation:
* `fleet6/door/logs/door.out` — 170 bytes, 24 core-hours, decides `MB27B373 = 13`.
* `fleet8/unified/results/joint_levels.jsonl` — 381 bytes, ~31 h / 29 core-hours,
  the only record of k = 9..13 UNSAT for the dim-16 joint block.
* `fleet5/laneMENU/logs/m_S7W_B27_c7_3b1c8975975d.out` — 171 bytes, the hub
  bracket (k = 6..10 UNSAT, 13 140 s at the top level).
* The cost-2 derive rows in `fleet8/unified/ledger.jsonl` (LEADS L1) — the only
  place those numbers exist inside this slice.

**H5 — `fleet7/laneCONSOLIDATE/RECORDS_REPO_PATCH.md` is ADVISORY ONLY.** It
describes edits to `~/xor_ui/aes_mc_records`, a DOI'd outward-facing artifact.
Nothing has been edited, committed or pushed, and the file says so in its second
line. Do not let a wrap-up pass mistake it for a completed change.

**H6 — env-gated behaviour switches inside `fleet8/unified`.** `SLP_SUPPRESS_HINTS`
(`generate.py:78`), `SLP_DERIVE_MAX_COST`, `SLP_USE_POOL`, plus env-gated menu and
commitment overrides at `code/cells.py:39,213` and `code/plan.py:48`
(`LANE_HALO`). **A run's numbers depend on the environment it was launched in**,
and the artefacts do not always record which. This is the mechanism behind the L1
inconsistency. Also: `--pool` is documented as deadlocking
(`generate.py:409-417`) — the serial path is the default and is 1.2×–31× faster.

---

## 7. GAPS

1. **The k = 14 joint verdict.** Not determinable from this slice — the job
   reported DONE with no k = 14 row and no result file, and the successor run is in
   `fleet11/laneCUBE`, which the BRIEF forbids me to probe beyond light reading.
   Whether k = 14 was killed, crashed, or was deliberately handed off is not
   recoverable from anything in fleet8. (L2.)
2. **I did not re-run any tally.** Every `tally.py` / `bound_opt.py` /
   `cellprice.py` re-derivation was left un-run per the CPU rule, so every number
   I quote from a `RESULT.md` is that lane's own claim, cross-checked against the
   ledger only where the ledger made it cheap. The numbers I *independently*
   derived are: the artifact counts and file sizes, the ledger row/kind counts,
   the 9 distinct 88 mask sets and their pairwise Jaccards, the timeout/partial-bound
   table, the vacuity-guard history, and two circuit verifications.
3. **The exact core-hours consumed by the slice** are not recoverable. `wall` is
   recorded per solve but the core counts vary (4, 8, 12) and are not always in the
   row. I quote wall seconds as logged, not core-seconds.
4. **`fleet5/laneMENU`'s 2801-row ledger** I sampled by `kind` only. Its 1330
   predict / 1328 result pairs encode a per-row pre-registration record I did not
   audit for hit rate; the lane's own §6 discipline-checks section reports it.
5. **Whether the `.prelive` / `.bak` files are redundant with git** — I did not run
   `git log` on them, so my DELETE-CANDIDATE label there is conditional.
6. **`fleet7/laneUNCOND/results/lpcerts/`** — I read the directory listing and the
   `RESULT.md` table, not the 1.5 MB of certificate contents. I have not
   independently checked that the 19 files correspond to the 19 lam values in the
   table.
7. **`STATE_OF_THE_PROBLEM.md`'s staleness beyond my slice.** It is dated
   2026-08-24 and is authoritative for everything up to fleet7. I verified that it
   is stale on `MB27B373` (its own D7 predicted it), on §5.3's "multi-gate
   shared-plane family — untouched" (L1), and on the joint W3|U4 row O7 ("not
   attempted; bracket [9,15]" — it is now [14,15]). **I did not audit it against
   fleet9–fleet12 or e13–e17**, which is a substantial body of later work; someone
   holding those slices should. Its §6.1/§6.2 method tables are nevertheless the
   best existing draft of goal 2 at project scale and should be the wrap-up
   catalog's backbone, with a staleness pass.
