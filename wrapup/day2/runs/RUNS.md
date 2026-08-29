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

See the launch block appended below.

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

**Status:** RUNNING as of 11:55.
