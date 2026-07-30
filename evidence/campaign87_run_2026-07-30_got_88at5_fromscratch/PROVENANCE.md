# Provenance — 87-hunt fleet, worker `c_naive` (2026-07-30, produced 88 @ depth 5 from scratch)

The run that produced **88 gates @ depth 5 from scratch**: the search that
reached it began at a freshly generated random construction, not at any earlier
circuit of ours and not at any published one.

**It is not a gate-count record.** 88 is the published best-known count, held by
Jean (ePrint 2026/1481, posted 2026-07-23), and **Jean has priority**. What
changed here is that the **(88, depth 5)** point is now reached by a circuit
found from scratch, rather than only by
`../campaign87_run_2026-07-29_got_88at5_derived/`, whose seed chain runs through
Jean's published work. **That removes this project's dependence on that circuit
at the depth-5 point; it does not beat it.**

Same worker, same fleet and byte-identical code as the 88 @ depth 6 of
`../campaign87_run_2026-07-28_got_88at6_fromscratch/` — a different session, a
different root, and a different basin.

## Read this first: the lineage contains no seeded circuit at all

| step | circuit | how | when (run-time / wall) |
|---|---|---|---|
| root | **146 gates @ d3** | `constructors.build("naive", 1958)` — randomized balanced XOR trees over the 32 raw inputs, with opportunistic reuse. **No seed circuit.** | session 5, restart 16 opened at t = 65 349.0 s / 07-30 09:44:09 |
| ↓ | 93 → 91 → 90 → 89 | `alt` chunks (walk 120 s / LNS 420 s) inside restart 16; the local bests are the `cur=/best=` fields of the chunk lines | 09:45:13 → 10:38:47 |
| ↓ | **88 @ d6** | walk, iteration 33 873 | **t = 69 192.7 s / 07-30 10:48:12** |
| ↓ | **88 @ d5** | same walk, Pareto depth tie-break, iteration 37 155 | **t = 69 198.8 s / 07-30 10:48:19** — 6.1 s later |

Root, 64 minutes, no imported and no inherited material. Both 88-gate states came
out of a **walk** chunk (the `[walk]` line closing at 10:48:24), and `engine_walk`
has no candidate pool and no disk read path at all.

Say **"session 5, restart 16"**, not bare "restart 16": this log holds five
worker sessions and 58 restarts, and the run-times restart at 0 with each
session.

The root re-derives from the archived root constructors — which this archive
**hash-pins rather than copies**, because they are byte-identical to the 88 @
depth 6 archive's (see `code/CODE_PROVENANCE.md`). Seed 1958 rebuilds to
146 gates at depth 3, exactly as logged (re-validated 2026-07-30):

```
python3 -c "import sys; sys.path.insert(0,'../campaign87_run_2026-07-28_got_88at6_fromscratch/code'); \
            import constructors; print(constructors.build('naive',1958)[2])"
{'gates': 146, 'depth': 3, 'outputs': 32, 'ok': True, 'problems': []}
```

## The contamination vectors, checked in the code rather than asserted

Ordered deliberately: vector 0 is the root, and it is the one that carries the
argument. The rest close routes the run happened to leave shut.

0. **The root reads nothing.** This worker's root spec was `constructor:naive`.
   In `hunt_worker.py` the `constructor:` branch of `Roots.next` calls only
   `constructors.build(name, seed)` and returns — **there is no file-reading path
   in that branch at all**. Every branch of `Roots` that can open a circuit off
   disk (`pool89`, `file:`, `glob:`) is a *different* branch, unreachable under
   this spec. Every restart in all five sessions of `runs_hunt/c_naive.log` opens
   on a `naive#<seed>` root; restart 16 of session 5 opens on `naive#1958`, which
   re-derives to exactly the logged 146 gates at depth 3.
1. **Cross-pollination could not have fired anywhere in this fleet.** This is a
   five-part structural argument, not a configuration check:
   1. `_Harvester.merge_into` — the only routine that reads another worker's
      harvest — has **exactly one call site** in `engines.py`, inside
      `engine_lns`, and it is guarded by `if harv.glob_pat`;
   2. `glob_pat` is `k.get("pop_glob")` (`engines.py`, `_harvester`);
   3. `pop_glob` has **exactly one writer in the whole fleet tree**,
      `worker.py:wire_harvest`, which translates a `cross_pollinate` switch into
      the glob;
   4. `hunt_worker.py` **never calls `wire_harvest`** — it imports only
      `WorkerCtx` and `pareto_better` from `worker`, and sets `harvest_path`
      directly on both engines; and `supervisor.py` **never launches `worker.py`
      at all** (the only scripts it spawns are `hunt_worker.py`,
      `orbit_runner.py`, `explorer.py` and `detector.py`);
   5. independently of all of that, `engine_lns` emits an
      `[lns] cross-pollinated N masks (pool=…)` line on every merge that brings
      in new material, and `runs_hunt/c_naive.log` contains **zero** such lines
      over its whole 1 941-line life.

   So no worker in this fleet had cross-pollination on, and this one could not
   have had it on even if a configuration had asked for it. (This is stronger
   than the argument published with the 88 @ depth 6, which rested on `pop_glob`
   never being *set* for that worker. Both conclusions are the same; this one is
   closed by construction. Note that the *earlier* wave-2 and wave-3 fleets ran a
   **different** `hunt_worker.py` that set `pop_glob` directly, and there
   cross-pollination genuinely was live — see `../RESULTS.md` §4 and §5. The two
   files share a name and nothing else on this point.)
2. The worker ran with `repel=False` (the session's first log line, 07-29
   15:35:00), so `repel_masks.json` — which holds masks of the older families —
   was never loaded.
3. Each restart builds a fresh `LocalCtx` and sets `cur = seed_masks`. This is
   directly observable rather than merely asserted: restart 16 opens at
   `cur=93 best=93`, **worse** than restart 15's `best=92`. Nothing carried over.
4. No `reseed_*.json` file, no `ctx.adopt` call and no `archive` import exists in
   `hunt_worker.py`; the producing engine, `engine_walk`, has no candidate pool
   and only ever adds masks derived from its own value set's closure.

## Four corroborations a sceptic can check

**(a) The code predates the run and is already published.** All five code files
are byte-identical to those in
`../campaign87_run_2026-07-28_got_88at6_fromscratch/code/`, which were released
in v3.0.0 on 2026-07-29 and carry modification times of 2026-07-27 — two days
before this find. `code/CODE_PROVENANCE.md` pins their sha256s.

**(b) The published log is a byte-exact prefix of this one.** The copy of
`c_naive.log` released with the 88 @ depth 6 in v3.0.0 (123 197 B, 1 505 lines) is
byte-for-byte the first 123 197 bytes of the log archived here (158 747 B, 1 941
lines):

```
$ head -c 123197 runs_hunt/c_naive.log | sha256sum
2ef567a080dc4e21a12138a01f19db921a2c87fea487c50abc676dc4ebd33cac  -
$ sha256sum ../campaign87_run_2026-07-28_got_88at6_fromscratch/runs_hunt/c_naive.log
2ef567a080dc4e21a12138a01f19db921a2c87fea487c50abc676dc4ebd33cac  ...
```

That prefix already ends at t = 18 407.5 s **of session 5** — the very session
that produced this circuit — and already contains that session's
`repel=False` start line. So the configuration of the producing session was
committed to a public repository roughly **twelve hours** before the find — commit
`391f427`, 2026-07-29 22:51:58 −0400, against the find at 2026-07-30 10:48:19,
a gap of **11.94 h** — by an agent that did not know it was going to matter. (The
published log's *content* stops earlier still: its last line is timestamped
20:41:47, 14.11 h before the find. Two different events; the commit is the one
that makes this public.) This is the strongest single
piece of evidence in the archive, because it is the one thing here that could not
have been arranged after the fact.

**(c) The mask set is this worker's own and nobody else's.** The record's exact
88-mask value set is line **35 285** of `c_naive`'s own harvest file
`campaign_87/hunt87/runs/c_naive.pop.jsonl`, and it appears in **zero** of the
fleet's other fifteen harvest files (sixteen in total, ≈ 1.1 GB, searched
line-exact on 2026-07-30). **Scope this one honestly:** unlike (a), (b) and (d),
the *absence* half rests on harvest files that are not shipped here, are still
growing, and carry no command you can run against this repository. Take it as
reported, not as checked.

**The line number itself, however, is checkable from the published log**, and it
is worth doing because it ties the record's position in the harvest to the
minute it was found. The `harv=` counter resets each session. Sessions 1–3
harvested nothing (`harv=0` throughout); session 4 ends at **harv=22 489** and
session 5 at **harv=14 816**, and

```
22 489 + 14 816 = 37 305
```

is exactly the harvest file's line count and the distinct-state count the pocket
scan reports (`certificates/pocket_depth5_scan.log`, first two lines). So line
35 285 is session 5's harvest entry number **35 285 − 22 489 = 12 796** — and the
two `[walk]` lines that straddle the find report `harv=12631` (t = 69 164.4 s,
10:47:44) and `harv=12939` (t = 69 204.2 s, 10:48:24). 12 796 falls strictly
between them. The record's harvest line is where the log says the record was
found, to within one 40-second walk chunk, using nothing but the log archived in
this folder.

**(d) The RNG seed is arithmetically forced by the clock.** `hunt_worker.py`
advances the seed by `+1` per engine chunk and `+101` per restart from
`--seed 201`, so seed 1958 at restart 16 implies exactly
1958 − 201 − 101 × 15 = **242 prior chunks**. The `alt` cycle is a 120 s walk
chunk and a 420 s LNS chunk, i.e. 270 s per chunk on average, predicting
242 × 270 = **65 340 s** for the restart-16 opening against the **65 349.0 s**
logged — **0.014 % off**. A restart inserted or removed anywhere in the session
would break this.

## Not a lone point: the depth-5 pocket

The find is not a single lucky state. Scanning all 37 305 distinct 88-gate
target-covering value sets in `c_naive`'s own harvest and computing each one's
ASAP (least-fixpoint) depth with `pipeline/engines.py:relax` gives

```
ASAP min-depth histogram: 5: 135, 6: 5 829, 7: 13 315, 8: 4 955, 9: 6 637, 10: 5 571, 11: 863
```

— **135 distinct own-lineage value sets realizable at depth 5**, all
oracle-verified, every one of them first appearing at or after line 35 285. The
record is one of the 135. Across the whole pocket the maximum weighted Jaccard to
Jean's 88 is **0.0602**, and to the derived 88 @ depth 5 **0.0651** (both maximised
over the four byte rotations). Verdict log: `certificates/pocket_depth5_scan.log`.

## Exact neighbourhood certificates for this circuit

Run with the repo's own archived decider (`shell_sweep.py` over
`../campaign87_certificates/code/exact_window.py`); verdict logs in
`certificates/`.

| radius | windows | verdict | wall |
|---|---|---|---|
| k = 2 (remove 2, restore with ≤ 1) | all **1 540** = C(56,2) | **all irreducible, shell exhaustively empty** | 6 s, 1 process |
| k = 3 (remove 3, restore with ≤ 2) | 3 × 9 240 = **27 720** = C(56,3) | **all irreducible, shell exhaustively empty** | 952–983 s, 3 processes |

Both budgets are exhaustive (complete by the proof in that module's docstring),
so these are proofs for exactly those radii: **any 87-gate circuit differs from
this one by ≥ 4 masks.** Nothing here bounds 87 away globally.

## Depth obstruction — a third distinct pattern

The masks whose minimum build depth equals the circuit depth are, for this
circuit, output rows **1, 7, 12, 13, 17, 18, 21, 25, 27, 28 and 31** — six
weight-7 targets (rows 1, 12, 17, 25, 27, 28) and five weight-5 ones (rows 7,
13, 18, 21, 31). That is a **third** distinct obstruction
pattern at 88 gates: the old plateau's 88 @ depth 7 is held by rows **3 and 27**
only, and the family-4 88 @ depth 6 by rows **1, 11, 17 and 25**. Eleven
simultaneously critical rows is what a circuit that has been pushed to its own
depth floor looks like. (Recomputable with `pipeline/engines.py:relax`.)

## How far it is from everything else

Plain Jaccard on mask sets, and the campaign's calibrated weighted Jaccard
(periphery-only, neutral-corpus IDF weights) maximised over all four byte
rotations ρ^k. The plain columns recompute from the circuit JSONs shipped in this
repository; **the weighted column does not** — that metric's implementation, its
IDF weight vector and its calibration corpus are all in the raw campaign tree,
not here. Read `wj` as reported, plain J as checkable:

| against | shared | plain J | periphery J | max wj over ρ^k |
|---|---|---|---|---|
| Jean's 88 (ePrint 2026/1481) | 42 / 88 | 0.313 | 0.098 | **0.0598** |
| our 88 @ d7 (family 1) | 39 | 0.285 | 0.067 | 0.0417 |
| our 88 @ d8 (family 3) | 41 | 0.304 | 0.087 | 0.0514 |
| our 88 @ d6 (family 4) | 43 | 0.323 | 0.109 | **0.1025** |
| the derived 88 @ d5 | 42 | 0.313 | 0.098 | 0.0642 |
| our 89 @ d5 | 42 | 0.311 | 0.097 | 0.0644 |
| Sun–Yang–Li's 89 (ePrint 2025/1493) | 43 | 0.321 | 0.108 | 0.0467 |

Every weighted figure is at most **0.1025** — a factor of three below the
metric's 0.32 "distinct" floor, and below 0.07 against everything except the
other from-scratch circuit — so this is a distinct family under the calibrated
metric as well as under the repository's plain-Jaccard 0.7 rule. It is likewise
outside every family of the campaign's completed census (11 proven-distinct
families in 14 same-linked groups over 410 222 distinct 88-gate states, in the
raw campaign tree, not in this repository): across its 100 archived group
representatives the largest weighted Jaccard reached is **0.293** (G05/F10),
still under the 0.32 distinct floor, while the group that actually holds Jean's
circuit sits at **0.0668** and the group holding this project's derived 88s at
**0.0626**.

**The number to quote for novelty is the rotated maximum, not the unrotated one.**
Unrotated, plain Jaccard to everything above is 0.285–0.323; over all four
rotations the largest value reached is **0.386 (0.179 on the periphery), attained
at ρ³ of Jean's 88**. That is the honest ceiling, and it is not even large in
context: this circuit's similarity to its own rotations sits at
**0.333–0.375**, so the 0.386 it reaches against everything else is only
marginally above what it scores against a rotated copy of itself.

It shares 42 of Jean's 88 masks, but **32 of those are the obligatory output
targets**, so only **10 of the 56 freely chosen masks** coincide.

## What is in this archive

- `FOUND_88gates_depth5_fromscratch.json` — the record, exactly as saved by the
  worker (sha256 `582ddd087ecf197a…`). Canonical copy:
  `../circuits/mixcolumns_88gates_depth5_fromscratch.json` (byte-identical gate
  list).
- `runs_hunt/c_naive.log` — the worker's **untouched** log, all five sessions and
  all 58 restarts, cut at 2026-07-30 11:19:00 (t = 71 039.9 s of session 5). The
  find is the two `NEW BEST 88 gates depth 6/5` lines at t = 69 192.7 s and
  t = 69 198.8 s; session 5 restart 16 opens at t = 65 349.0 s.
- `code/` — `CODE_PROVENANCE.md` and `CONFIG_AS_RUN.md` only. The five source
  files are **byte-identical** to
  `../campaign87_run_2026-07-28_got_88at6_fromscratch/code/`, so they are
  hash-pinned there rather than duplicated.
- `certificates/` — the k = 2 and k = 3 shell verdict logs (and the drivers'
  stdout), plus the depth-5 pocket scan.

## What is NOT in this archive

- The worker's status file (`runs/c_naive_status.json`): the worker is still
  running, so that file describes the present, not the find.
- The harvest `campaign_87/hunt87/runs/c_naive.pop.jsonl` — 34 290 830 B when
  this archive was cut, of which line 35 285 is this record. It is **still being
  appended to**, so no stable sha256 is quoted for it; the rest of the fleet's
  harvest is likewise live.
- `supervisor.py`, the fleet launcher. Unlike the 88 @ depth 6 archive, the
  as-run version *is* still on disk here (last edited 2026-07-29 15:34, one
  minute before session 5 started, and untouched since), and the structural
  cross-pollination argument above was checked against it. It is not copied in
  because nothing in it is load-bearing for the record beyond the worker command
  line, which is in `code/CONFIG_AS_RUN.md` and in the log's first line.

## Re-verify

```
python3 ../../verify_circuit.py FOUND_88gates_depth5_fromscratch.json 5   # VALID
python3 ../../verify_circuit.py FOUND_88gates_depth5_fromscratch.json 4   # INVALID: depth 5 is tight
```

Outputs at the time of archiving:

```
gates=88 depth=5 outputs_built=32/32 problems=0 ; depth<= 5: OK ; VERDICT: VALID MixColumns circuit
gates=88 depth=5 outputs_built=32/32 problems=0 ; depth<= 4: VIOLATED ; VERDICT: INVALID
```

Independently recomputed from the raw JSON against a locally rebuilt GF(2⁸)
spec: 88 gates, depth 5, 32/32 outputs, **0 dead gates**, 0 duplicate masks, no
gate mask colliding with an input.
