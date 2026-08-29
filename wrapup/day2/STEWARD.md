# COMPUTE STEWARD — S1 / S2 / S3 feasibility report

Date 2026-08-29. Agent: compute steward (Opus 5). Box at load 19.8/20, 4 mono
SAT solvers + laneCUBE live. **Nothing was launched.** Everything below is
either a read, a `--help`-class import, or a seconds-to-60-seconds test at
`nice -n 19` that wrote only under `wrapup/day2/`. No process was signalled,
no `experiments/STOP` was created, nothing inside `fleet11/laneCUBE` or
`fleet8/unified` was touched or written.

**Calibration for every time estimate below.** Measured today, same box, same
`nice -19`: `d3bound` k=6 took **19 s** on the idle box in July and **>40 s**
now (it hit a 40 s cap mid-solve at gap 4.8%). So the scavenging factor is
**≈2–3× wall per core-second**, i.e. roughly the "0.5 effective core" the
task assumes, slightly worse.

---

## Verdict table

| | item | GO/NO-GO | banks to disk? | 1 thread? | mem | est. wall @ ~0.5 core |
|---|---|---|---|---|---|---|
| S1 | `d3bound.py` resume from 63 | **NO-GO** (cannot reach what matters) | yes, per rung | yes | 176 MB → ~2 GB | 4–9 h for ≤ +7 on a bound already beaten by 80 |
| S1′ | `mip3.py` (same lead, route b) — **substitute** | **GO** | yes, via log line | yes | 359 MB → ~2–3 GB | 12 h for a bound already at 82 and climbing |
| S2 | `G_int(3) ≥ 92` re-certification | **GO, time-boxed** | rung-wise only (drafted) | yes | **145 MB** | 3–12 h, real risk of UNKNOWN |
| S3 | wiring-randomised null | **GO — and it already answered** | yes, jsonl | yes | 58 MB | 3 min (census) / 30 min (full) |

---

## S1. The depth-3 ladder

### What the script is and how a rung is proven

`campaign_87/d3_model/d3bound.py` (99 lines) over
`campaign_87/d3_model/d3model.py::solve_window(..., subset_only=True)`.
Backend: **HiGHS via `scipy.optimize.milp`** (scipy 1.11.4, numpy 1.26.4),
**inherently single-threaded** — `_milp` passes only
`{time_limit, mip_rel_gap, presolve}`, no thread option.

The rung logic: drop every target outside a subset `S`, solve
`min |P| + |Q|` exactly. Any full depth-3 circuit restricted to `S` is feasible
for that program, so `32 + min` is a valid **gate** lower bound (the +32 is one
gate per target, from the structure theorem). A rung is banked **only** when
`res.status == 0` (HiGHS *proven optimal*).

### State on disk

* `campaign_87/d3_model/ckpt/bounds.json` —
  `{"bound": 63, "how": "exact min over 10 targets (heavy[:10])", "subset": [1,3,4,9,11,12,17,19,20,25], "pq": 31}`
* `campaign_87/d3_model/logs/d3bound.log` (1,478 B) — 13 lines, starts 09:09:18,
  **ends 09:25:50 mid-`k=10`**, i.e. after rep 0 of 6 at k=10; k=12/14/16 never
  attempted, no note, no successor.

**Resume is automatic**, not a restart: `main()` re-reads `ckpt/bounds.json` at
startup and only banks strict improvements over 63. Give it only the untried
rungs so nothing is repeated.

### Launch command (for the record — see the NO-GO)

```
cd /home/joebachir20/xor_ui/slp-plateau-search/campaign_87/d3_model && \
setsid nohup nice -n 19 python3 d3bound.py 12,14,16 3600 3 \
  > logs/d3bound_resume.out 2>&1 &
```
(args: `ks`, per-solve `time_limit` seconds, `reps` per k. Writes append-only to
`logs/d3bound.log` + `ckpt/bounds.json` — outside `wrapup/day2/`, so this is the
user's to launch, not mine.)

### Memory, banking, threading

* Peak RSS measured at k=6: **176 MB** (of which ~14 s and most of the baseline
  is the `d3model` import + model build). Extrapolate ~1–2 GB at k=14–16 as the
  B&B tree grows; `ulimit -v 4000000` is cheap insurance.
* Banking: **yes, and reboot-safe.** Every rung is appended to the log at
  completion; every improvement rewrites `ckpt/bounds.json`. Nothing is held in
  memory across rungs.
* **Defect worth a 3-line patch:** a rung that hits the time limit banks
  *nothing*, although `res.mip_dual_bound` is present and is a valid lower
  bound. Verified today: the timed-out k=6 solve carried
  `mip_dual_bound = 20.0` (⇒ bound 52) alongside `status=1`. Patch:
  `if bound is None and res.mip_dual_bound: bound = 32 + ceil(res.mip_dual_bound)`
  and bank it with a `PROVEN DUAL BOUND` tag. This is exactly the trick
  `mip3.py` already uses.

### What `N_depth3 ≥ 80` is, and whether this route is independent

`campaign_87/wave6_2026-08-11/lower_bound/cert_depth3.json` — an **exact
rational weak-duality certificate** over `build_lp.build(True)`: 72,830 rows ×
29,180 variables, `u ≥ 0` with `Aᵀu ≤ c` checked in integer arithmetic,
`exact_dual_value = 47597998171620/10¹² = 47.597998` ⇒ `|L1|+|L2| ≥ 48` ⇒
**`N_depth3 ≥ 80`**. **Re-verified today** (`nice -19 python3 certify.py --check
cert_depth3.json` → `N_depth3 >= 80`). Nothing floating-point enters the claim.

`d3bound` is **genuinely independent** of it: different object (exact MILP on
target subsets, restriction-relaxation) versus an LP dual on the complete row
system. Two different proofs, not two runs of one.

### Is exceeding 80 plausible? **No.**

`bound = 32 + pq`. To beat 80 needs `pq ≥ 49`; the theorem "no 87 at depth 3"
needs `bound ≥ 88`, i.e. **`pq ≥ 56`**.

The all-heavy rungs measured (k = number of targets priced):

| k | 4 | 6 | 8 | 10 |
|---|---|---|---|---|
| `pq` | 15 | 20 | 27 | 31 |
| bound | 47 | 52 | 59 | 63 |
| Δ per 2 targets | — | +5 | +7 | **+4** |

Three facts close this off:

1. **Only 12 weight-7 (heavy) targets exist.** k=12 exhausts them; every rung
   past 12 must add weight-5 targets, which price lower.
2. **The increments are already decelerating** (+7 then +4) at the point of
   abandonment.
3. **The route's own ceiling is 65.** At k=32 the subset program *is* the full
   problem, and the verified 97-gate depth-3 circuit gives `pq_full ≤ 65` —
   `mip3.py` uses exactly that as a hard objective cap. So `pq ≥ 56` means
   pricing a ~26-target subset to within 9 of the global optimum.

At k=10 a rung already costs 155 s idle (≈5 min scavenged). k≈26 is not
reachable. **Realistic ceiling for this route: bound ≈ 66–70** — it will beat
63 and it will not beat the 80 that is already certified by an independent
proof. LEADS.md's framing ("stopped while still improving") is accurate about
the log and misleading about the destination.

If the user wants the k=12 rung purely for the record, it is ~10–25 min:
`python3 d3bound.py 12 1800 1`.

### Substitute: route (b) from the same lead is already past 80

`campaign_87/wave6_2026-08-11/lower_bound/mip3.py` — HiGHS branch-and-cut on
the *complete* strengthened model, and it reports `N_depth3 >= 32 +
ceil(mip_dual_bound)` directly.

* `logs/mip3_L1.log` — capped run, killed at 599.5 s with dual bound
  **48.44982378 ⇒ N_depth3 ≥ 81**, still climbing, still at node 0.
* `logs/mip3_L1_uncapped.log` — reached **49.47825234 ⇒ N_depth3 ≥ 82** at
  538.7 s and was killed at 885.8 s. `mip3_result_L1.json` (which THEOREM.md
  tells the reader to consult) **does not exist** — the run never finished.

Measured today (inline, no writes): model builds in ~2 s, 72,831 × 29,180,
nnz 268,307, **peak RSS 359 MB at 60 s**; the root LP has not produced a dual
bound line by 60 s (the July log shows node 0 still open at 330 s), so the
first useful output is ~5–10 min in and then continuous.

```
cd /home/joebachir20/xor_ui/slp-plateau-search/campaign_87/wave6_2026-08-11/lower_bound && \
setsid nohup nice -n 19 python3 mip3.py 43200 1 > logs/mip3_L1_resume.log 2>&1 &
```

* Banks to disk: **yes, but only via the log** (`disp: True` prints a dual-bound
  line every ~30–60 s; the JSON is written only at the end). A reboot loses the
  tree but every printed dual bound remains a valid, permanent rung — which is
  precisely how 48.4498 was harvested from the previous kill.
* Single-threaded: yes (same scipy/HiGHS path).
* Memory: 359 MB at 60 s, expect 2–3 GB over 12 h of tree growth. **Cap it**
  (`ulimit -v 6000000`) — this is the one item here that could bite a box at
  14/31 GB used.
* This route is the one that can actually move the published number, and it
  needs no new code.

---

## S2. `G_int(3) ≥ 92` re-certification

### What exactly must be solved

`fleet6/laneTOOL2/code/u1_uncond.py::solve_G(targets, lam, cores, timeout, ub)`.
CP-SAT (ortools 9.15.6755). Universe `L.universe(mixcolumns_targets())` =
**1,648 masks**; the model is **17,784 booleans** (3 × 1,648 for `a`/`y`/`b`
plus **12,840** split-indicator vars) and **builds in 0.5 s**.

`G(λ) := min over A ⊆ U of ( λ|A| + Φ(A) )`, encoded as
`min 3·Σa + Σy` subject to buildability of every target.

**The question: is `3|A| + |Y| ≤ 91` feasible? `INFEASIBLE` ⇒ `G_int(3) ≥ 92`.**

### What "re-certify as proof of infeasibility rather than the solver's best guess" means

The number on the board comes from one line of `results/u1_uncond.json`:

```
lam=3  status=FEASIBLE  seconds=1200.07  G=94.0  bound_scaled=92  A_size=15 Y_size=49
```

i.e. **`BestObjectiveBound() = 92` reported at status FEASIBLE** after 1200 s on
4 cores, with incumbent 94 — bracket [92, 94]. That is CP-SAT's *dual bound at
the moment the clock ran out*: a claim about an interrupted run, with no status
backing it and nothing a referee can re-check. (`logs/wave2.log` shows the same
model at 600 s / 4 cores reporting only `[lower 86.0]`, which is what the number
looks like when you stop earlier.)

The referee-checkable forms, in increasing strength:

1. **`INFEASIBLE`** on the model plus `obj ≤ 91` — a *status*, not a bound.
   This is what §7.2 asks for and is what the drafted driver targets.
2. `OPTIMAL` on the unconstrained minimisation — gives the exact value and
   closes the [92, 94] bracket outright.

Note honestly: CP-SAT emits no DRAT/proof log, so (1) is still a solver claim —
it is a *reproducible, status-level* claim rather than a truncated-run bound.
That is the whole of the upgrade, and it is what the dossier asks for.

### Memory — not the problem

**Peak RSS 145 MB** at 1 worker (measured, `/usr/bin/time -v`). CP-SAT is heavy
on some models; this is not one of them. Memory is a non-issue; **time is the
whole risk.**

### Checkpointing — no, and the mitigation

CP-SAT has no resume. A killed run banks nothing; after a reboot you start from
zero. Mitigation, drafted and smoke-tested:
**`wrapup/day2/tools/gint3_recert.py`** runs a *ladder* of decision instances,
appending each verdict to `wrapup/day2/work/gint3_recert.jsonl`, skipping rungs
already decided on restart. Every `INFEASIBLE` rung is a permanent certificate.
Verified working: `B=31 → INFEASIBLE in 3.4 s ⇒ G_int(3) ≥ 32` banked.

The driver keeps `Minimize(obj)` alongside `Add(obj ≤ B)`, because measurement
says dropping it is much worse (below); `--pure-decision` is available but not
recommended.

### Time estimate — and a warning

Measured today, 1 worker, `nice -19`:

| run | result |
|---|---|
| `B=31`, minimize on | **INFEASIBLE 3.4 s** ⇒ `G_int(3) ≥ 32` |
| `B=40`, pure decision, 8 s | UNKNOWN |
| `B=50`, pure decision, 60 s | UNKNOWN |
| `B=50`, minimize on, 60 s | UNKNOWN, `best_bound` still **32.0** |
| `B=91`, minimize on, 60 s | UNKNOWN, `best_bound` still **32.0** |
| `B=50`, `optimize_with_core=True`, 60 s | UNKNOWN, bound 32.0 |

So the bound does not begin to move inside the first minute of core time. The
historical anchor is the only real datum: **4,800 core-seconds (1200 s × 4
cores) to reach bound 92**, with 2,400 core-seconds reaching only 86 — i.e. the
climb is back-loaded.

At ~0.5 effective core that is **≈2.7 h wall if single-worker CP-SAT is as
efficient per core-second as 4-worker.** It usually is not: the 4 workers run
diverse strategies and share clauses, and the objective-bound worker may simply
not be scheduled at `num_search_workers=1`. **Honest estimate: 3–12 h, with a
material chance of returning UNKNOWN and banking nothing.**

### Launch command

```
cd /home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/tools && \
setsid nohup nice -n 19 python3 gint3_recert.py --lam 3 --bounds 91 \
  --timeout 43200 --cores 1 > ../work/gint3.log 2>&1 &
```

### Two things to do before spending 12 h on it

1. **Break the `Z/4` gauge first.** LEADS #45 (`beat88` U-10, `fleet5_8` L6):
   rotation maps `TARGETS` onto `TARGETS` and permutes the 1,648-mask universe
   onto itself, so every solution comes in orbits of up to 4 — **a free 4×** —
   and ρ-symmetry breaking is named as *the* unexploited lever **for the
   `G_int` / exact-`L_cf` encodings specifically**, which use it not at all. A
   lex-leader constraint on the `a`-indicator vector over the 8 ρ-orbits is one
   constraint and would turn a 12 h gamble into a ~3 h one.
2. **Buy `G_int(2) = 64` on the way past.** §7.1: two independent
   reproductions have failed against one log line, and laneY's price
   `L(M) ≥ 58` hangs on it. The same driver does it —
   `--lam 2 --bounds 63` — and the original was `OPTIMAL` in 9.46 s at 4 cores,
   so this rung is minutes, not hours. It is strictly cheaper than S2 proper and
   fixes a second flagged foundation.

### Ceiling that must travel with the purchase

`fleet5_8` L6 / `fleet7/laneUNCOND` §7.4: `G_int(3) ≥ 92` moves the dichotomy
from `κ ≥ 16` to `κ ≥ 18`; `≥ 94` gives 19; **no larger value is reachable**,
and the route still dies at `κ ≥ 22`, below the records' own `κ = 18..28`. Fund
it as "closes the one purchasable lemma and deletes branch 3 of the Anatomy
Theorem", not as "opens a road".

---

## S3. The wiring-randomised null control

### What it tests

`laneDELTA/RESULT.md` §6(e), `DOSSIER.md` §9.2, `REF_DELTA/VERDICT.md` F5.

The surviving-side zero is the one genuinely unexplained observation in the
e16/e17 material: over lane536's site frame, `minrep = 2` never occurs on the
**surviving** consumer of a site in a valid 88 — `0 / 54,561` corpus-wide.
(`witness_corpus.log`, 1,200 88s: `del_3 20, del_4 3739, del_None 24, surv_3
3583, surv_4 19, surv_None 3` — no `surv_2` at all. The non-88 comparator has
`surv_2 = 47`.)

Every null run for it is confounded in the same direction, because **a "site" is
a property of the wiring**, and the corpus's wirings are not sampled:
`_closure_core` fixes every parent by one deterministic rule. The prescribed
experiment holds the mask set fixed and varies **only** the parent choice.

### The tool — drafted, smoke-tested, not run at volume

**`wrapup/day2/tools/wiring_null.py`.** Reuses `frame.Frame`/`TARGET` and
`slp3.pairset`/`minrep_S`; `sites()` and `sidesplit()` are copied **verbatim**
from `laneDELTA/witness.py` rather than imported, because importing that module
runs `os.makedirs` on a scratch path outside `wrapup/day2/`. Adds a
`Wiring` class (a `Frame`-compatible view of an in-memory gate list) and
`random_wiring()` (uniform-random topological realisation; buildability is a
monotone closure so any greedy order terminates). Append-only jsonl, resumable
on `(file, wiring)`, single-threaded, **58 MB peak**.

```
cd /home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/tools && \
nice -n 19 python3 wiring_null.py --census --circuits 500          # ~3 min
nice -n 19 python3 wiring_null.py --circuits 200 --wirings 50 \
    --out ../work/wiring_null.jsonl                                 # ~30 min
```

Smoke tests run (all seconds, all written under `wrapup/day2/work/`):
`--smoke` (3×3) 2 s; `--circuits 8 --wirings 12` 6 s → 104 rows;
`--census --circuits 25` → 2,200 gate masks. Measured ~0.17 s per rewired frame
under load, so 200 circuits × 50 wirings ≈ 30 min. The 30 s `glob` over the
**20,412** `*88gates*.json` files dominates short runs.

### The smoke test already answered the question: the null is degenerate

Two independent measurements:

1. **Sampling.** 30 random topological wirings per circuit, 3 circuits: at the
   moment each of the 88 gate masks was built there was **exactly one** legal
   parent pair — **1,320 / 1,320 observations** — and it was always the
   as-found parent (`masks whose as-found parent never sampled: 0`).
2. **Census** (`--census`, 25 circuits, 2,200 gate masks, acyclic-legal parent
   pairs computed directly): **2,197 masks with exactly 1**, 2 with 2, 1 with 3.
   **Forced fraction 0.9986.**

Consequences observed: site counts were *identical* across all 20 wirings of
each of 6 circuits (2, 3, 2, 3, 3, 1 respectively); fanout histograms identical;
the side split was `del_4 / surv_3` in 100% of 280 site-sides.

(For contrast, ignoring acyclicity there is apparent freedom — pairs `{a,b}`
with `a^b = m` anywhere in the signal set run `{1:314, 2:161, 3:521, 4:43,
5:7, 6:10}` over 1,056 masks. Acyclicity kills essentially all of it.)

**Reading:** for an 88-gate MixColumns circuit, the mask set determines the
wiring. The DAG is not a free parameter at 88 gates.

### What that hardens, precisely

* It **discharges the stated confound.** laneDELTA's reason (3) for refusing to
  price — "the corpus's wirings are not sampled; `_closure_core` fixes every
  parent by one deterministic rule" — is *true but inert*: any wiring rule
  produces the same wiring, so `_closure_core` introduces no bias whatsoever.
  The surviving-side zero is a property of the **mask set**, not of the search's
  parent-choice convention.
* It **cannot produce a p-value.** The null distribution is a point mass, so
  laneDELTA's ruling "the surviving-side zero is UNPRICED" **survives** — but on
  one fewer leg, and REF_DELTA F5's recommendation ("their own recommendation of
  the wiring-randomised null is right and should be run") is now answered rather
  than pending.
* It is a **new structural fact in its own right**, and a cheap one: *the wiring
  of an 88 is forced by its mask set (99.86% of gates; 0 of 88 gates ever had a
  choice across 30 sampled wirings).* That belongs in the "why 88" material, and
  it retroactively justifies every method in this repo that treats an 88 as a
  mask set — mask-set-only canonicalisation loses nothing.

Run the census at 500 circuits to state the number with authority; the full null
is optional confirmation.

---

## Sanity checks (all `nice -n 19`)

| check | result |
|---|---|
| `scipy` / `numpy` import | 1.11.4 / 1.26.4 ✓ |
| `d3model.get_model()` + `solve_window(heavy[:4], subset_only=True)` | `pq=15`, status 0 (proven), 0.9 s ✓ |
| `campaign_87/d3_model/ckpt/bounds.json` | present, `bound=63` ✓ |
| `certify.py --check cert_depth3.json` | `N_depth3 >= 80` ✓ |
| `build_lp.build(True,1)` + 60 s HiGHS MIP | 72,831 × 29,180, nnz 268,307, 359 MB ✓ |
| `ortools` import + `L.universe()` | 9.15.6755, 32 targets, **1,648** masks ✓ |
| CP-SAT model build (`u1_uncond` encoding) | 0.5 s, 17,784 vars, 145 MB ✓ |
| `gint3_recert.py --bounds 31` | INFEASIBLE 3.4 s ⇒ `G_int(3) ≥ 32` ✓ |
| `frame.Frame` / `slp3` / corpus glob | 20,412 `*88gates*.json` files ✓ |
| `wiring_null.py --smoke` | 3 circuits × 3 wirings, 2 s, 58 MB ✓ |

## Files written by this agent (all under `wrapup/day2/`)

* `wrapup/day2/STEWARD.md` — this report
* `wrapup/day2/tools/gint3_recert.py` — S2 ladder driver (drafted, smoke-tested)
* `wrapup/day2/tools/wiring_null.py` — S3 null + wiring-freedom census
* `wrapup/day2/work/{smoke,smoke2,gint3_smoke,gint3_smoke2,gint3_smoke3,gint3_smoke4}.jsonl`
  — smoke-test output, deletable

## Ops notes for whoever launches

* S1′ (`mip3.py`) is the only item with a real memory trajectory. Cap it.
* S2 banks nothing until a rung closes. If the box may reboot, prefer the
  symmetry-broken model first rather than a bare 12 h run.
* S1 and S1′ write inside `campaign_87/…`; S2 and S3 as commanded above write
  only inside `wrapup/day2/work/`.
* All four are single-threaded. Total footprint if all run at once: < 4 GB.
