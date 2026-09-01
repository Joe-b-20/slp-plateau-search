# LAUNCH RECORD — day-2 steward runs

All runs: `setsid nohup`, `nice -n 19`, **single thread**, detached from this
session, banking to disk continuously, all state under `wrapup/day2/runs/`.
Nothing was written inside `campaign_87/`; nothing inside `fleet11/laneCUBE`
or `fleet8/unified` was read-locked, written, or signalled; no `experiments/STOP`;
no `pkill`. Box measurement used for planning: a `nice -19` single thread gets
**~43% of a core**.

**Hard deadline: 2026-08-30 01:30 local.** Both long runs carry an internal
wall-clock limit that lands well before it and exit cleanly on their own,
writing their result file. Neither needs to be killed.

---

## RUN 1 — S1′: `mip3.py` depth-3 dual-bound climber

**What it is.** HiGHS branch-and-cut on the complete strengthened depth-3
model; every row of `build_lp` is a theorem about depth-3 circuits, so
`N_depth3 >= 32 + ceil(mip_dual_bound)` at any moment. This is the route that
had already banked **N_depth3 >= 82** (`mip_dual_bound = 49.47825234` at
538.7 s) before being killed at 885.8 s in August.

**Copy, not original.** The whole 25-file `.py` set of
`campaign_87/wave6_2026-08-11/lower_bound/` was copied to
`wrapup/day2/runs/mip3/` and every hardcoded
`.../campaign_87/wave6_2026-08-11/lower_bound` path in the **copies** was
rewritten to `.../wrapup/day2/runs/mip3`. The originals are byte-identical to
before (verified: the original `mip3.py` still carries 2 references to its own
path). Reads of `/pipeline` (for `mixcolumns_core`) are unchanged and read-only.

**One patch to the copy** (`wrapup/day2/runs/mip3/mip3.py`): the objective cap
`|L1|+|L2| <= 65` is now conditional on `argv[3] == 'capped'`. Rationale — the
banked 82 trajectory came from the *uncapped* variant
(`logs/mip3_L1_uncapped.log`: 72830 rows, nnz 259914, bound 49.478); the capped
variant reached only 48.4498 in 599.5 s. Both are sound; we reproduce the better
one. **Verified before launch that the copy builds exactly that model:**
`rows 72830, nvar 29180, base 8393, nnz 259914` — an exact match to the
uncapped log's header.

**Launch (executed 2026-08-29 11:36:16):**
```
cd /home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/runs/mip3
setsid nohup bash -c 'ulimit -v 6000000; exec nice -n 19 python3 mip3.py 45000 1' \
    > mip3_L1_run.log 2>&1 < /dev/null &
```

| | |
|---|---|
| **PID** | **1372748** |
| log | `wrapup/day2/runs/mip3/mip3_L1_run.log` |
| result file | `wrapup/day2/runs/mip3/mip3_result_L1.json` (+ `mip3_primal_L1.json`) written at exit |
| internal limit | 45,000 s (12.5 h) — HiGHS wall clock, started at solve start |
| expected completion | **~2026-08-30 00:15**, i.e. 1 h 15 m before the deadline |
| memory | `ulimit -v 6000000` (6 GB address space) as specified |
| threads | 1 (scipy's HiGHS is single-threaded; no thread option is passed) |

**Banking.** `disp: True` prints a dual-bound line every ~30–100 s; **every
printed `BestBound` is a permanent, valid rung** (`N_depth3 >= 32 + ceil(bound)`)
and survives a reboot in the log even though the JSON is written only at exit.
This is exactly how 48.4498 was harvested from the previous kill.

**First-dual-bound confirmation (required check):** the first bound line
appeared at **135.6 s** — `R 0 0 0 0.00% 47.59824561 148 67.84% ... 135.6s` —
and by 234.5 s it had moved to **47.97730668** with 1,009 cuts in play. The
climb is live and on the same shape as the August log (48.3476 at 330.9 s).

**Kill instructions (only if needed):** `kill 1372748` — a plain SIGTERM. The
log keeps every bound already printed, so nothing is lost. Do **not** `pkill`;
there are unrelated live SAT solvers on this box.

**Bound-to-beat:** 49.47825234 ⇒ `N_depth3 >= 82`. Anything above
`ceil(bound) = 50` is new; `bound > 55` would give `N_depth3 >= 88` and the
theorem "no 87 at depth 3" — not expected, but it is the same run either way.

⚠ **Environment note for the writeup:** the August logs were produced under
**HiGHS 1.8.0**; this box's scipy 1.11.4 bundles **HiGHS 1.2.0**. Same model,
older cut generators. If the bound lands below 49.478 that is a plausible
explanation and not a contradiction of the banked number.

---

## RUN 2 — S2: `G_int` re-certification ladder

Driver: `wrapup/day2/tools/gint3_recert.py` (mine). Model: laneTOOL2's own
encoding (`u1_uncond.solve_G`), universe 1,648 masks, 17,784 booleans.
All verdicts append to `wrapup/day2/runs/gint/gint_ladder.jsonl`; the driver
skips `(lam, B, gauge)` triples already decided there, so a reboot resumes.

### 2a. Waypoint — `G_int(2)`, ungauged (model validation)

```
cd /home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/tools
setsid nohup nice -n 19 python3 gint3_recert.py --lam 2 --bounds 63 \
    --timeout 1800 --cores 1 --out ../runs/gint/gint_ladder.jsonl \
    > ../runs/gint/gint2_waypoint.log 2>&1 < /dev/null &
```
PID 1373707, launched 11:36:5x, hard cap 1,800 s. `INFEASIBLE` certifies
`G_int(2) >= 64` — the constant DOSSIER §7.1 flags as having **two failed
independent reproductions against one log line**, and on which laneY's
`L(M) >= 58` depends. Verdict recorded below.

### 2b. The Z/4 gauge break and its soundness control

`rho` = rotate the four state bytes by one. Implemented in the driver as a
**lex-leader cut for the single generator**: `v >=_lex rho.v` on the
concatenated `a`/`y` indicator vector over `sorted(U)`.

*Soundness argument.* `rho` induces a bijection of the feasible set that
preserves the objective, so every orbit has a lex-maximum, and that lex-maximum
satisfies `v >=_lex g.v` for **every** `g` in the group — in particular for the
generator. So at least one representative of every feasible orbit survives.
(Truncating the comparison to a prefix only weakens the cut, so it stays sound
at any length; the run uses the full vector.)

```
python3 gint3_recert.py --control ../runs/gint/gauge_control.json --cores 1 --timeout 600
```
→ `wrapup/day2/runs/gint/{gauge_control.json,gauge_control.log}`

**CONTROL A — arithmetic prerequisites (no solver):**

| check | result |
|---|---|
| `rho^4 == id` | **True** |
| `rho(TARGETS) == TARGETS` | **True** |
| `rho(U) == U` | **True** |
| `rho` preserves popcount | **True** |
| `split_pairs` equivariant, all **1,648** masks | **True** |
| orbit sizes present | `[2, 4]` |

**CONTROL B — planted known-feasible assignment:** the published `G(3)`
incumbent from `fleet6/laneTOOL2/results/u1_uncond.json` (`|A|=15, |Y|=49`,
obj **94**). Its four rotations were computed; **2 of the 4 survive the
lex-leader cut** (so the cut is doing work but is not emptying the orbit).
Planting the surviving rotation into the **gauge-broken** model at `B=94` →
**OPTIMAL (feasible), 2.3 s**; the same witness in the **ungauged** model →
**OPTIMAL, 2.7 s**. A real feasible orbit is preserved.

**CONTROL C — end-to-end on the validated constant:** `--lam 2 --bounds 64
--gauge` must stay feasible (the optimum `A = TARGETS, Y = {}` is `rho`-fixed,
hence a guaranteed survivor of the cut), and `--lam 2 --bounds 63` must return
the same verdict gauged and ungauged. Logs:
`runs/gint/gint2_gauged_b64.log`.

**VERDICT: `PASS`** (written to `runs/gint/gauge_control.json`). The driver
additionally re-runs Control A automatically on every `--gauge` invocation and
**refuses to launch** if it fails.

### 2c. The real run — `G_int(3) >= 92` as an infeasibility

```
cd /home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/tools
setsid nohup nice -n 19 python3 gint3_recert.py --lam 3 --bounds 91 \
    --timeout 47243 --cores 1 --gauge --out ../runs/gint/gint_ladder.jsonl \
    > ../runs/gint/gint3_b91_gauged.log 2>&1 < /dev/null &
```
PID 1384125, launched 2026-08-29 11:52:37, budget computed at launch as
`date -d "2026-08-30 01:00:00" +%s` minus now = 47,243 s (13 h 7 m), i.e.
30 min inside the deadline.

---

# OUTCOMES (written 2026-08-30 16:14, after the fact)

## ⚠ The dominant fact: the host suspended for essentially the whole window

`uptime` advanced by **4 minutes between 2026-08-29 18:34 and 2026-08-30 16:14**
— 21 h 40 m of wall clock, 4 minutes of awake machine. An earlier suspend ate
~6.6 h between 11:53 and 18:34 (uptime went 5d 3:19 → 5d 4:14 across 7.5 h of
wall time).

**Operational lesson, and it is the important deliverable of this run:**
*solver time limits on this box are not suspend-safe.* HiGHS's `time_limit` and
CP-SAT's `max_time_in_seconds` both kept counting while the machine was asleep,
so each job "used up" a 12–13 h budget while doing **~20 minutes of real work**,
then stopped at its limit. `time.monotonic()` does *not* advance across suspend
here (mip3 recorded `wall_monotonic = 1369.95` against a HiGHS-reported total of
`60391.94`), so the two clocks disagree by a factor of 44.

Any future long run on this box must be governed by a **`time.monotonic()` or
CPU-time watchdog that re-arms the solver limit**, not by a single solver-side
wall limit. Nothing was left running past the deadline: both jobs exited on
their own limits and no process of mine survives.

## RUN 1 result — S1′ `mip3.py`: **`N_depth3 >= 81` banked, run completed cleanly**

`wrapup/day2/runs/mip3/mip3_result_L1.json`:
```json
{"model": "depth3_strong_highs_mip", "level": 1, "status": 1,
 "message": "Time limit reached. (HiGHS Status 13: Time limit reached)",
 "wall_monotonic": 1369.95, "primal": 148.0, "mip_dual_bound": 49.0,
 "mip_gap": 0.6689, "N_depth3_lower_bound": 81}
```
* **Result: `mip_dual_bound = 49.0` ⇒ `N_depth3 >= 81`.** The JSON was written
  (this is the file THEOREM.md tells the reader to consult and which had never
  existed — it exists now, for the copy).
* Trajectory in `mip3_L1_run.log`: 47.598 @ 135.6 s → 47.977 @ 234.5 s →
  48.142 @ 333.8 s → 48.594 @ 799.3 s → 48.626 @ 974.9 s → 48.756 @ 1108.9 s →
  best printed 48.851, final reported bound 49.0. Node 0 was never left; the
  whole climb is root cuts.
* **One short of the previously banked 82** (`49.47825234`, August). Two
  sufficient explanations, both recorded before launch: it got **1,370 s of real
  compute instead of 45,000 s** because of the suspend, and this box's scipy
  1.11.4 bundles **HiGHS 1.2.0** where the August log was **HiGHS 1.8.0**.
  Nothing here contradicts the banked 82; it under-reproduces it.
* Re-running this with a suspend-safe watchdog is cheap and is the obvious next
  step: the August curve reached 49.478 in 538.7 s, so ~20 min of *real* awake
  compute should clear 82.

## RUN 2 results — S2 `G_int`

| run | verdict | seconds (wall, suspend-inflated) | banked |
|---|---|---|---|
| `lam=2 B=63` ungauged (waypoint) | **UNKNOWN**, `best_bound = 32.0` | 23,341.6 | nothing |
| `lam=2 B=64` gauged (control C, search form) | **UNKNOWN**, `best_bound = 32.0` | 23,123.8 | nothing |
| `lam=3 B=91` gauged (the real run) | **UNKNOWN**, `best_bound = 32.0` | 37,215.3 | nothing |

* **The `G_int(2) = 64` waypoint did not reproduce.** This is now a **third**
  failed independent reproduction, joining the two DOSSIER §7.1 already records
  (laneY's `g2.py` at 900 s / 1 core → FEASIBLE with bound 32.0; REF_ALGEBRA's
  decision encoding → UNKNOWN at 600 s / 1 core). Our failure has the **same
  signature as laneY's**: bound stuck at exactly **32.0**. The pattern across
  four attempts is unambiguous — *the 4-core bound climb does not happen at
  1 core on this model*, and `G_int(2) = 64` still rests on the single
  `logs/wave2.log` line. It should stay flagged UNPROVEN-AS-STATED.
* **`G_int(3) >= 92` is not purchased.** `best_bound` never left 32.0. The
  bracket `[92, 94]` remains exactly as §7.2 describes it, and the conditional
  chain (`kappa >= 3` at `n <= 87`, `|A*| >= 3`, deletion of Anatomy branch 3)
  remains conditional.
* The only `G_int` rung this session actually banked is the trivial
  `lam=3 B=31 -> INFEASIBLE (3.4 s) ⇒ G_int(3) >= 32`
  (`wrapup/day2/work/gint3_smoke2.jsonl`), which is not news.

## Gauge-break control — **PASS**, on three independent checks

`wrapup/day2/runs/gint/{gauge_control.json,gauge_control.log}`

* **A (arithmetic, no solver):** `rho^4 = id`; `rho(TARGETS) = TARGETS`;
  `rho(U) = U`; popcount preserved; **`split_pairs` equivariant on all 1,648
  masks**; orbit sizes `{2, 4}`. All True. Together with the standard lex-leader
  argument (every orbit has a lex-max, and the lex-max satisfies `v >=_lex g.v`
  for every `g`), this *proves* the cut sound.
* **B (planted, lam=3):** the published `G(3)` incumbent (`|A|=15, |Y|=49`,
  obj 94). 2 of its 4 rotations survive the cut; planting a survivor into the
  **gauge-broken** model at `B=94` → **OPTIMAL (feasible) in 2.3 s**, matching
  the ungauged model's 2.7 s.
* **C (planted, lam=2):** the known optimum `A = TARGETS, Y = {}` (obj 64) is
  `rho`-fixed, satisfies the cut in the Python mirror, and the **gauge-broken**
  model accepts it — **OPTIMAL in 0.6 s** vs ungauged 0.3 s.
  *(The search-form version of this control, `--lam 2 --bounds 64 --gauge` run
  as a solve rather than a planting, returned UNKNOWN — it never found the
  trivial solution in the compute the suspend left it. That is a statement about
  the solver's search on this box, not about the cut: the planted form settles
  the question directly and decisively.)*

**Conclusion: the Z/4 lex-leader cut is sound and was correctly used.** It is not
why the run failed — the run failed for lack of awake CPU.

## Side effects outside `wrapup/day2/`

`__pycache__/*.pyc` byte-compilation artifacts under `campaign_87/d3_model/`,
`campaign_87/wave6_2026-08-11/lower_bound/` and `fleet6/laneTOOL2/code/`,
created by Python on import during the read-only sanity checks. Regenerable,
harmless, deletable. **No source file outside `wrapup/day2/` was modified**;
`campaign_87/.../mip3.py`, `fleet6/laneTOOL2/code/u1_uncond.py` and
`campaign_87/d3_model/d3bound.py` are untouched. `fleet11/laneCUBE` was never
written to; the k=14 `cube16.py` solvers are still running; no
`experiments/STOP` exists.

---

## Standing rules for anyone touching these

* Both runs are `nice -19` single-thread; together they use well under one core
  and under 6.5 GB.
* Neither needs killing before the deadline; both exit on their own.
* If the box must be quiesced anyway: `kill <PID>` by the PIDs above, one at a
  time. **Never `pkill`** — the k=14 mono solvers and `fleet11/laneCUBE` are
  live and unrelated.
* Nothing here writes outside `wrapup/day2/runs/`.

---

## R1 — `seed89` : the pinned descent RE-SEEDED AT THE 89, target 88

**Launched** 2026-08-29 11:36 local. **PID 1372715.** *(This entry was lost when RUNS.md
was rewritten at 16:14; restored 2026-08-30 16:58 with its outcome.)*

```
setsid nohup nice -n 19 python3 wrapup/day2/e_upstream/seed89.py 10000 \
  > wrapup/day2/e_upstream/seed89.nohup 2>&1 < /dev/null &
```

| | |
|---|---|
| script | `wrapup/day2/e_upstream/seed89.py` — a **patched copy** of `experiments/e_upstream/deep.py`; the originals in `experiments/e_upstream/` were never modified |
| seed | `experiments/e_upstream/S89_41_00000098.json` — 89 masks, oracle-VALID, depth 10 |
| pin | `0x00000098` (\|odd\| = 3), patched into **both** `engines.T` and `engines.TSET` |
| engine target | **88** (the record). LNS 120 s / walk 60 s alternating, `LP.LNS_KNOBS` / `LP.WALK_KNOBS` unchanged |
| budget | 10,000 s **monotonic** |
| log / ledger / stdout | `wrapup/day2/e_upstream/seed89.log` · `seed89_ledger.jsonl` · `seed89.nohup` |
| hits would land as | `wrapup/day2/e_upstream/HIT88_00000098_<k>.json` + `..._circuit.json`, written the instant a ≤ 88-mask state appeared |

**Purpose (verbatim in the ledger's `start` row).** Every one of e_upstream's 225 pinned
descents started at a 100–173-gate root and spent its whole budget on the 149 → 89
stretch; the **89 → 88 gap had never received a single dedicated second**. This job asked:
*does an out-of-vocabulary 88 exist one step below the 89?* That is a **structural question
about the record level** — 88 **is** the record — **not a sub-record search**. The engine's
target was 88 and it stops there. No STOP file was to be created on a hit, and none was.

### Outcome — CLOSED 2026-08-30 16:57, NO 88 REACHED (partial negative)

| | |
|---|---|
| improvements below the 89 seed | **0** (`ev:"improve"` rows: 0) |
| `HIT88_*` files banked | **0** |
| floor | **89**, pin alive |
| monotonic elapsed / CPU used | **3,967 s / 1,581 s ≈ 0.44 core-hours** of the ~1.2 budgeted |
| how it ended | terminated at the authorised deadline; it exited **without** writing its own `stop`/`done` row, so the closing record in the ledger is `ev:"closed_by_operator"` and is explicitly marked as operator-written, not process-written |

**Verdict: no out-of-vocabulary 88 was found one step below the 89. This is a PARTIAL
NEGATIVE and an upper bound from search — not a proof that 88 is unreachable with this
pin.** The question stays OPEN. `seed89.py` is stateless; re-launching it with a fresh
budget resumes from the same seed.

**Operational lesson (worth carrying).** The budget never expired because **the host was
suspended**: machine uptime advanced ~1.6 h while the wall clock advanced ~29 h, and
`time.monotonic()` does not tick while suspended. A monotonic deadline is right for
*interruptibility* but is **not** a wall-clock guarantee on a laptop-class box — a job that
must respect a wall-clock deadline needs an absolute `time.time()` check too.

**Status:** CLOSED.

---

## R2 — `c4_corpus_sample` : C4's exact fan-out verdict, widened to sampled corpus 88s

**Launched** 2026-08-29 11:53 local. **PID 1376420.**

```
C4_N=150 C4_WALL=2400 setsid nohup nice -n 19 \
  python3 wrapup/day2/e_upstream/c4_corpus_sample.py \
  > wrapup/day2/e_upstream/c4_corpus_sample.log 2>&1 < /dev/null &
```

| | |
|---|---|
| script | `wrapup/day2/e_upstream/c4_corpus_sample.py` — same CP-SAT model as `c4_fanout_cpsat.py`, 1 solver worker |
| population | 150 valid 88-gate mask sets, stratified (every *k*th row) across `nrpa/out/sub92.jsonl`, `beat88 pop88_worklist.jsonl`, `hunt-deeper/population88_new.jsonl` |
| budget | self-limiting: `C4_WALL=2400` s, checked before each set, so it **stops cleanly** and banks whatever it has |
| output | `wrapup/day2/e_upstream/c4_corpus_sample.json`, rewritten after **every** mask set |
| log | `wrapup/day2/e_upstream/c4_corpus_sample.log` |

**Purpose.** `c4_fanout_cpsat.py` already closed C4 exactly on 39 mask sets (6 record 88s
+ the 33 e_upstream floors): exact max fan-out over **all** build orders is 3–5 on the
record 88s, 6 across all 39, so **fan-out ≥ 8 is not realisable at 88**. This widens the
base so the verdict is not an artifact of six hand-picked circuits. Per-set answers are
exact and the per-set signal sweep is exhaustive (branch-and-bound on `potential`, since
`fanout(s) ≤ potential(s)`).

**Kill instructions.** Safe at any moment; results are on disk after each set.

```
kill 1376420
pkill -f 'c4_corpus_sample.py'
```

### Outcome — COMPLETED (wall-capped) 2026-08-29, verdict NO

| | |
|---|---|
| corpus 88s solved | **103** of the 150 sampled (50 `nrpa_sub92`, 50 `beat88_worklist`, 3 `population88_new`) |
| exact max fan-out histogram | **3 ×15 · 4 ×80 · 5 ×8** |
| max over the sample | **5** |
| sets reaching fan-out >= 8 | **0** |
| sweeps exhaustive | **102 / 103** (one set had a solve hit the 120 s cap; its 4 is a lower bound on its own maximum) |
| their `max potential` | 6 ×7 · 7 ×13 · **8 ×39 · 9 ×33 · 10 ×11** |

**83 of the 103 have a signal with potential >= 8 and none realises more than 5.** Together
with the 39 exact record/floor sets this is **142 mask sets, max fan-out 3-6, never 8** —
see `experiments/e_upstream/RESULT.md` C4.

**Operational lesson.** The wall cap is checked only *between* mask sets, and one set took
22,266 s (a hard CP-SAT instance re-solved across ~27 signals at the 120 s cap). The job
still stopped cleanly and banked everything, but a per-set cap is needed as well as a
per-solve cap.

**Status:** CLOSED.
