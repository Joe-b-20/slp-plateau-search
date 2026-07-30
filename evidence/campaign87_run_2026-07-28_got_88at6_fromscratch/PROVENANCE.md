# Provenance — 87-hunt fleet, worker `c_naive` (2026-07-28, produced 88 @ depth 6)

The run that produced **88 gates @ depth 6** — a fourth distinct 88-gate family,
and the first 88 this project has found **from scratch**: the search that reached
it started from a freshly generated random construction, not from any earlier
circuit of ours and not from any published one.

It is **not a gate-count record.** 88 is the published best-known count, held by
Jean (ePrint 2026/1481, posted 2026-07-23, and Jean has priority) and
independently matched by this project's own 88 @ depth 7. What this circuit does
is improve the published depth–count Pareto frontier: it dominates Jean's 88 @
depth 7 (equal count, one level shallower — depth 7 being our own measurement of
our transcription, since that note states no depth) and improves on the published
depth-6 point of 92 gates (Maximov) by four gates.

## Read this first: the lineage contains no seeded circuit at all

| step | circuit | how | when (run-time / wall) |
|---|---|---|---|
| root | **139 gates @ d3** | `constructors.build("naive", 2163)` — randomized balanced XOR trees over the 32 raw inputs, with opportunistic reuse. **No seed circuit.** | restart 18 opened at t = 66 009.5 s / 07-28 16:42:36 |
| ↓ | 95 → 92 → 90 → 89 | `alt` chunks (walk 120 s / LNS 420 s) inside restart 18; the local bests are the `cur=/best=` fields of the chunk lines | 16:43:29 → 16:52:12 |
| ↓ | **88 @ d7** | walk, iteration 37 270 | **t = 68 238.2 s / 07-28 17:19:45** |
| ↓ | **88 @ d6** | same walk, Pareto depth tie-break, iteration 37 501 | **t = 68 238.7 s / 07-28 17:19:45** — 0.5 s later |

Root, 37 minutes, no imported and no inherited material. The root is
re-derivable from the archived `code/constructors.py`: seed 2163 rebuilds to
139 gates at depth 3, exactly as logged (re-validated 2026-07-29).

```
python3 -c "import sys; sys.path.insert(0,'code'); import constructors; \
            print(constructors.build('naive',2163)[2])"
```

**The contamination vectors, checked in the archived code rather than asserted.**
They are ordered deliberately: vector 0 is the root, and it is the one that
carries the argument. The others close routes that the run happened to leave
shut — necessary, but not what makes this circuit from scratch. (The *derived*
88 @ depth 5 of `../campaign87_run_2026-07-29_got_88at5_derived/` had vectors 1–4
in exactly the same state; what differed was its root.)

0. **The root reads nothing.** This worker's root spec was `constructor:naive`
   (its command line, above). In `code/hunt_worker.py` the `constructor:` branch
   of `Roots.next` calls only `constructors.build(name, seed)` and returns —
   **there is no file-reading path in that branch at all**. Every branch of
   `Roots` that can open a circuit off disk (`pool89` via `_pool89`, `file:`,
   `glob:` via `_glob`) is a *different* branch, unreachable under this spec.
   Consistently with that, **all 38 restarts** logged in the worker session that
   produced this circuit (`runs_hunt/c_naive.log` from the `22:22:27` start
   onward) open on a `naive#<seed>` root, restart 18 on `naive#2163`, which
   re-derives to exactly the logged 139 gates at depth 3 by the command above.
   A search whose root reads nothing cannot inherit anything through its root.
1. **Cross-pollination — two independent parts.** `supervisor.py` as run is *not*
   archived (see "What is NOT in this archive"), so this is stated as the
   two-part argument it is rather than as one check. (a) In the archived
   `code/hunt_worker.py`, the engine knob dicts are given only `harvest_path`;
   the string `pop_glob` **does not appear anywhere in that file**, so the
   `_Harvester` this worker built had `glob_pat=None` and its `merge_into` was
   never called. (b) Independently of the code: in `code/engines.py`, `engine_lns`
   logs `[lns] cross-pollinated N masks (pool=…)` for every merge that brings in
   new material, and `runs_hunt/c_naive.log` contains **zero** such lines over
   its whole life. Code and log agree, from two directions.
2. The worker ran with `repel=False` (first line of `runs_hunt/c_naive.log`), so
   `repel_masks.json` — which contains masks of the three older families — was
   never loaded.
3. Each restart builds a fresh `LocalCtx` and sets `cur = seed_masks`
   (`code/hunt_worker.py`, the restart loop). The worker had already reached an
   88 @ depth 8 on restart 17 from a *different* root (15:58:20), and that
   circuit did **not** seed restart 18: the only carry-over across restarts is
   the global Pareto bookkeeping that decides what gets logged and saved, never
   the search state.
4. `engine_walk` has no candidate pool at all and only adds masks derived from
   its own value set's closure; the 89 and both 88-gate states of this restart came
   from walk chunks. One LNS chunk *did* improve the best here (92 → 90, the
   `[lns]` line at 16:48:24) — with `pop_glob` unset its rebuild pool is built only
   from its own current masks, their pairwise sums and its own accumulated hot
   list, so that step imported nothing either.

## A fourth distinct family

Jaccard on mask sets (re-measured 2026-07-29; the campaign's threshold is
J ≥ 0.7 for "same family"):

| against | shared | Jaccard | periphery-only J |
|---|---|---|---|
| Jean's 88 (ePrint 2026/1481) | 42 / 88 | **0.313** | **0.098** |
| our 88 @ d7 (family 1) | 43 | **0.323** | **0.109** |
| our 88 @ d8 (family 3) | 42 | **0.313** | **0.098** |
| our 88 @ d5 | 42 | **0.313** | **0.098** |
| our record 89 @ d5 | 44 | 0.331 | 0.119 |
| Sun–Yang–Li's 89 (ePrint 2025/1493) | 41 | 0.301 | 0.087 |

The periphery column is the one that matters: every valid circuit contains the
same 32 target masks, so full Jaccard has a floor near 0.22 for two 88s that
share nothing else. On the 56 masks this circuit actually chose it agrees with
the other three families on about a tenth — outside the obligatory targets it
shares almost nothing with anything previously known. It is not a relabelling
either: over all four byte rotations ρ^k of every circuit **in the table above**,
the largest Jaccard reached is **0.351**, and **0.141** on the periphery (both ρ²
of our 89 @ d5).

**Scope of that maximum.** The table above is the six circuits this repository
holds or has transcribed; it deliberately does not include the project's
**superseded 89 @ depth 10**, which is retired here but still shipped by the
artifact repository. `../RESULTS.md` §6 quotes the maximum over that wider
seven-circuit set, where it is **0.362 (0.153)** — attained by the 89 @ depth 10
unrotated. Both numbers are correct for their own comparison set; the difference
is scope, not a disagreement.

## The run

| | |
|---|---|
| what | the multi-day **87-hunt** fleet (`campaign_87/hunt87/supervisor.py`): 15 search workers + the k=2 detector, one shared harvest directory |
| this instance | launched 2026-07-27 **22:22:27**, still running when this archive was cut; the find is 18.96 h in |
| worker | **`c_naive`** — `hunt_worker.py --label c_naive --root constructor:naive --seed 201 --restart-s 7200 --stall-s 2400`, `alt` mode, **uncapped** (`cap=None`), `repel=False` |
| the record | `FOUND_88gates_depth6.json`. Canonical copy: `../circuits/mixcolumns_88gates_depth6.json` (byte-identical gate list). |
| harvest cross-check | the record's exact 88-mask set is line 2 199 of **`c_naive`'s own harvest file** `campaign_87/hunt87/runs/c_naive.pop.jsonl` (re-checked 2026-07-29). Of the fleet's 16 harvest files it appears in five others, all of them workers pointed *at this basin after the find*: `f4_a`, `f4_b` (seeded from `seeds/fam4/`, added 2026-07-29 01:17) and the three explorers that draw the archive cells those seeds improved. |

## Exact neighbourhood certificates for this circuit

Both sweeps were run with the repo's own archived decider
(`../campaign87_certificates/code/exact_window.py`, byte-identical to the copy
the hunt used) and are re-runnable from this repository alone; verdict logs in
`certificates/`.

| radius | windows | verdict |
|---|---|---|
| k = 2 (remove 2, restore with ≤ 1) | all **1 540** = C(56,2) | **all irreducible, shell exhaustively empty** |
| k = 3 (remove 3, restore with ≤ 2) | all **27 720** = C(56,3) | **all irreducible, shell exhaustively empty** |

Both budgets are exhaustive (complete by the proof in that module's docstring),
so these are proofs for exactly those radii: **any 87-gate circuit differs from
this one by ≥ 4 masks.** Nothing here bounds 87 away globally.

The basin around it was swept too, by the `hunt87_basin4` agent: **8 993**
distinct 88-gate states at J > 0.7 to this circuit, all oracle-valid, **4 420 of
them realizable at depth 6** and none deeper than 7; all 8 993 proven k=2
irreducible, plus 1 200 further states beyond the harvest. Those sweep logs stay
in the raw campaign archive (`campaign_87/hunt87_basin4/`).

## Depth obstruction

The masks whose minimum build depth equals the circuit depth are, for this
circuit, output rows **1, 11, 17 and 25** — four weight-7 targets. The old
88-plateau's wall is elsewhere: our 88 @ depth 7 is held at depth 7 by rows
**3 and 27** only. Two structurally different ways to hit a depth wall at 88
gates (`../RESULTS.md` §8, reproducible with `pipeline/engines.py:relax`).

## What is in this archive

- `FOUND_88gates_depth6.json` — the record, exactly as saved by the worker.
- `runs_hunt/c_naive.log` — the worker's **untouched** log, all restarts. The
  find is the two `NEW BEST 88 gates depth 7/6` lines at t = 68 238 s; restart 18
  opens at t = 66 009.5 s.
- `code/` — the engine, worker and root constructors as run, with
  `CODE_PROVENANCE.md` and `CONFIG_AS_RUN.md`.
- `certificates/` — the k = 2 and k = 3 shell verdict logs and the sweep driver.

## What is NOT in this archive

- The worker's status file (`runs/c_naive_status.json`) — it was overwritten by a
  later respawn of the same worker and no longer describes the find.
- The harvest `campaign_87/hunt87/runs/c_naive.pop.jsonl` — 29 631 670 B and
  32 200 lines when this archive was cut, of which line 2 199 is this record. It is
  **still being appended to** by the respawned worker, so no stable sha256 is
  quoted for it; the rest of the fleet's harvest is 868 MB across 16 files and is
  likewise live.
- `supervisor.py`, the fleet launcher: it was edited on 2026-07-29 (a fleet
  shrink from 15 search workers to 5) and is therefore **not** the version that
  ran. The worker's own command line, which is what matters, is in
  `code/CONFIG_AS_RUN.md` and in the first line of the worker log.

## Re-verify

```
python3 ../../verify_circuit.py FOUND_88gates_depth6.json 6   # VALID
python3 ../../verify_circuit.py FOUND_88gates_depth6.json 5   # INVALID: depth 6 is tight
```

Outputs at the time of archiving:

```
gates=88 depth=6 outputs_built=32/32 problems=0 ; depth<= 6: OK ; VERDICT: VALID MixColumns circuit
gates=88 depth=6 outputs_built=32/32 problems=0 ; depth<= 5: VIOLATED ; VERDICT: INVALID
```
