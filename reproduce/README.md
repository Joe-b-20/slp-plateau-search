# reproduce — one command per record, with its measured time

Everything here is dependency-free Python 3 (stdlib only). Four of the eight
verified circuits have a reproduction command: two run from this folder, two are
pipeline runs, and all four are in one table. The other four — the from-scratch
88 @ depth 5, the 88 @ depth 6, the derived 88 @ depth 5 and the 88 @ depth 8 —
have none, for the reasons below.

Every search is stochastic. Times below are **what a run actually took**, dated
and labelled — a measurement, never a promise.

| what it reproduces | command | measured |
|---|---|---|
| **97 @ depth 3, from scratch** | `python3 reproduce.py` | **81 s**, one core, re-validated 2026-07-27 (RNG seed 6); 60–156 s across earlier runs |
| **89 @ depth 5**, from this project's 89@6 + 90@5 circuits | `cd ../pipeline && python3 ladder_parallel.py --mode fixed --workers sub89 --stop-gates 89 --stop-depth 5` | **19 s and 22 s** in two runs, re-validated 2026-07-27; the archived run took 592 s (~10 min), with the v1 engine (see below) |
| **88 @ depth 7**, from our ρ²-symmetric 94 | `python3 hunt_88.py` | **19.4 min** with the shipped stop rule, re-validated 2026-07-27 (a second re-run reached 88 gates at 31.0 min but stopped at depth 8 under an earlier gate-count-only rule); the archived run took 32.9 min. Stochastic — see [The 88 @ depth 7](#the-88--depth-7) |
| **92 @ depth 4**, from scratch | `cd ../pipeline && python3 ladder_parallel.py --mode cascade --stop-gates 92 --stop-depth 4` | hours: the archived run reached it at t = 9 610 s (2.67 h). Not re-measured here |

Each command verifies its own output against MixColumns rebuilt from GF(2⁸)
before reporting it, and every output file is re-checkable by hand — see
[Verify independently](#verify-independently).

## 97 @ depth 3 — the single-file, single-core reproduction

```
python3 reproduce.py
```

Simulated annealing + iterated local search over a shared depth-1-pairs /
depth-2-parts model. **From scratch**: the targets are computed from GF(2⁸),
there is no seed circuit. The result is checked by the independent verifier and
written to `out_97.json`; a summary table prints at the end.

Re-validated **2026-07-27** with the shipped code on one core (`taskset -c 0`):
the annealer reached cost 97 on its first RNG seed after **81.1 s** (23.5 s
annealing, then ILS), and the standalone oracle re-confirmed
`gates=97 depth=3 outputs_built=32/32 VALID`. Earlier runs of the same script
took 60–156 s. If seed 6 misses, the script keeps restarting on further seeds
until it hits the target or its 900 s budget runs out.

This method is specific to depth 3 and was **not** touched by the v2 engine
rebuild — it does not share a kernel with the pipeline engines.

## 89 @ depth 5 — seconds, not minutes, with the v2 engine

```
cd ../pipeline
python3 ladder_parallel.py --mode fixed --workers sub89 --stop-gates 89 --stop-depth 5
```

The historic two-worker sub-89 configuration: an uncapped `lns` worker on this
project's 89 @ depth 6 circuit and a depth-5-capped one on its 90 @ depth 5,
reseeding each other, stopping themselves at the target.

The **archived run** (2026-07-14) surfaced the 89 @ depth 5 at t = 592 s (~10 min).
That run used the v1 engine; the shipped engine is the campaign's rebuilt one,
and it is much faster on this seed. Re-validated **2026-07-27**, twice:

- the uncapped worker verified **89 gates @ depth 5 at t = 0.3 s of its first
  chunk** (LNS iteration 18, via the Pareto depth tie-break), both times;
- the command as a whole took **19 s** and **22 s** end to end — that time is
  the coordinator's 20 s status-poll cadence plus process start/stop, not
  search time.

## The 88 @ depth 7

```
python3 hunt_88.py                     # 45 min budget, the record worker's RNG
python3 hunt_88.py --minutes 120       # longer budget
python3 hunt_88.py --target 87 --target-depth 0   # don't stop at 88
```

`hunt_88.py` contains no search code: the 88 came out of the pipeline, so this
script only *aims* it. It writes the shipped configuration into a run folder,
launches **one** `../pipeline/worker.py` process (`alt` mode, uncapped, RNG 1010)
on the exact seed the record worker used, polls its status file, and stops it as
soon as an oracle-verified best reaches **88 gates at depth ≤ 7**. Both bounds
matter: the walk finds the 88 masks at some large depth first and the Pareto
tie-break carries that same size down to depth 7 a second or two later, so
stopping on the gate count alone yields an 88 at depth 8–11. The knobs are
imported from `../pipeline/ladder_parallel.py` rather than copied, so they cannot
drift from the shipped ones. The run folder is deleted at the end unless you pass
`--keep`; the best circuit is copied out to `out_88hunt.json`.

**What the archive says.** The 88 @ depth 7 was found by worker `w10_sym94` of a
10-worker, 8 400 s hunt on 2026-07-26 — `alt` mode, RNG 1010, seeded with the
exactly ρ²-symmetric **94 @ depth 5** of our own lineage — at **t = 1 973 s
(32.9 min)**, at depth 11, which the Pareto tie-break took to depth 7 5.3 s
later. Full log, code and provenance:
`../evidence/campaign87_run_2026-07-26_got_88at7/`.

**What a single-worker re-run did here.** Two re-runs on **2026-07-27**, one
worker each, on the defaults above:

| run | 88 gates first verified | at depth ≤ 7 | oracle |
|---|---|---|---|
| 1 (an earlier stop rule: gate count only) | t = 1 858.5 s (31.0 min), at depth 11 → depth 8 within 1.2 s | stopped before the tie-break got there | 88 @ 8, 32/32, VALID |
| 2 (the shipped stop rule, 88 @ depth ≤ 7) | t = 1 161.6 s (19.4 min), at depth 8 | **t = 1 162.6 s (19.4 min)** | **88 @ 7, 32/32, VALID** |

Archived, for comparison: 1 973 s (32.9 min). Run 2's circuit is **not** a copy
of the record — it shares 83 of its 88 masks with it (Jaccard 0.892): the same
plateau basin, a different point in it.

The **first chunk is reproduced exactly**, because the seed circuit and the RNG
seed are the archived worker's: 92 at `it=27`, 91 at `it=32`, 90 @ 9/8/6/5 at
`it=603/622/670/723`, 89 @ 8 at `it=58504`, 89 @ 7 at `it=58795` — the archived
worker's iteration numbers to the digit, reached in 82 s here against its 202 s
(one worker on an idle box walks at ~750 it/s; that one, one of ten on a loaded
box, ran at ~290 it/s). Chunk boundaries are **wall-clock**, though, so from the
second chunk on a faster machine is at a different iteration and the
trajectories part — which is why the two re-runs above diverged (31.0 min to
88 gates under the old stop rule vs 19.4 min to 88 @ depth 7 under the
shipped one).

This is a re-run, not an independent confirmation and not a promise: change the
RNG, the seed, the chunk lengths or the machine and it is an open-ended
stochastic search again. What it establishes is that the shipped engine, seed and
knobs are the ones that produced the record.

**Provenance.** The ρ²-symmetric 94 seed is our own lineage (from-scratch 97 @ 3
→ 89 @ 6 → 89 @ 5 → symmetrized 94), so nothing this worker produces is derived
from published work; cross-pollination stays off, as in the shipped
configuration. Our 88 @ depth 7 **matches** the published 88-gate record
(Jean, ePrint 2026/1481) **with an independent circuit** — 61 of 88 masks in
common — it does not beat it.

## The four circuits with no command here, and why

- The **88 @ depth 8** (a third distinct family) and the **derived 88 @ depth 5**
  both have seed chains that pass through Jean's published
  circuit, so both are reported as derived work and neither is offered as a
  recipe. Their run archives are
  `../evidence/campaign87_run_2026-07-27_got_88at8_thirdfamily/` and
  `../evidence/campaign87_run_2026-07-29_got_88at5_derived/`, each with the exact
  code, the seed and the untouched logs; the 88 @ 8's seed also ships as
  `../pipeline/seeds/seed_88_at_depth8_thirdfamily.json`.
- The **88 @ depth 6** and the **from-scratch 88 @ depth 5** are clean — both
  found from scratch — but each came out of one restart of one worker of a
  multi-day 16-process fleet (restart 18, 18.96 h in; and session 5 restart 16,
  19.22 h in), and no single
  command reproduces that. What is archived instead is everything needed to
  re-run the *step*: the roots are `constructors.build("naive", 2163)` and
  `constructors.build("naive", 1958)`, both in
  `../evidence/campaign87_run_2026-07-28_got_88at6_fromscratch/code/` (the later
  run's archive hash-pins that same code rather than duplicating it), which
  re-derive the logged 139-gate and 146-gate depth-3 roots exactly, and the
  worker logs record every chunk from there to 88 gates. The from-scratch
  88 @ depth 5 is the frontier's depth-5 point; it is **not** a gate-count
  record, since 88 is Jean's published count and Jean has priority.

To continue the hunt for 87 from the three 88-gate family anchors the pipeline
ships, use its shipped set: `python3 ladder_parallel.py --mode fixed` (i.e.
`--workers hunt87`), minding the provenance note in `../pipeline/README.md`. The
two from-scratch families' anchors are
`../evidence/circuits/mixcolumns_88gates_depth6.json` and
`../evidence/circuits/mixcolumns_88gates_depth5_fromscratch.json`.

## Legacy demonstrations (opt-in)

Three further methods demonstrate the individual moves on this project's
*superseded* records. Name them on the command line (or add them to `RUN` at
the top of `reproduce.py`):

```
python3 reproduce.py 91          # or: python3 reproduce.py 91 90 89
```

Honest provenance and re-validated times, per method (**2026-07-27**, one core):

| method | seed provenance | what it shows | measured |
|---|---|---|---|
| `"91"` | the **published** 92-gate SLP of Xiang, Zeng, Lin, Bao and Zhang, embedded in `seeds.py` as data | plateau walk over equal-size circuits until one gate becomes removable → 91 @ depth 6 | **6.7 s** (reduced on the first search seed); 5–60 s across runs |
| `"89"` | a 90-gate depth-6 circuit of **our own** earlier lineage (`SEED_90_MASKS`) | the value-set walk (remove-1 + remove-2-add-1 hub moves) cutting 90 → 89 at unconstrained depth | **150 s** — hit 89 (at depth 10) inside its first 150 s RNG seed |
| `"90"` | a 91-gate depth-6 circuit of **our own** earlier lineage (`SEED_91_TRIPLES`) | proves the seed admits no single local cut (duplicate scan, peel, all-pairs remove-2-add-1); with `C90["lns_seconds"] > 0` also runs the pure-Python LNS (reaches ~91) | **0.2 s** for the irreducibility proof |

These reproduce **superseded** results, kept because each is a clean, readable
statement of one move: the current records are in the table at the top and in
`../evidence/RESULTS.md`.
From nothing, method `"89"`'s walk floors near 92 — the 89 needs its seed.

## Which engine is which

`reproduce.py` deliberately carries the **original per-method search code** of
the runs it reproduces, frozen. It is what those results were obtained with, and
each method reads as one move rather than as a tuned kernel. It is *not* the
current engine.

The current engine is `../pipeline/engines.py`, rebuilt in the 2026-07 campaign.
That rebuild is why the 89 @ depth 5 now comes back in seconds and why any of
the five 88s exist at all; `hunt_88.py` here aims it, and `../METHODS.md` §5–§6 documents
each change with its measured effect.

`mixcolumns_core.py` in this folder is a **byte-identical copy** of
`../pipeline/mixcolumns_core.py` — both halves of the repository verify against
exactly the same oracle, and `diff` proves it:

```
diff ../pipeline/mixcolumns_core.py mixcolumns_core.py && echo identical
```

## Files

| file | what it is | edit it? |
|---|---|---|
| `reproduce.py` | the runnable script: **CONFIG block at the very top** (every knob), then the methods, then the runner | yes — all tuning lives at the top |
| `hunt_88.py` | aims one pipeline worker at the ρ²-symmetric 94 seed and stops it at the target; CONFIG block at the top, overridable with `--minutes/--target/--rng` | yes — same |
| `mixcolumns_core.py` | the MixColumns spec rebuilt from GF(2⁸) + the verifier (byte-identical to the pipeline's copy) | no — this is the trustworthy math |
| `seeds.py` | the embedded seed circuits (data) | no — starting points, not answers |

## Verify independently

Every `out_*.json` is an index-pair circuit (`{"gates":[[a,b],...]}`, signals
0..31 = inputs, gate k → signal 32+k). Re-check any of them with the standalone
verifier one folder up:

```
python3 ../verify_circuit.py out_97.json 3
python3 ../verify_circuit.py out_91.json 6
python3 ../verify_circuit.py out_88hunt.json      # depth bound optional
```

## Published circuits, for comparison

Nothing in this folder is claimed optimal, and no published circuit is counted
as a result of this project. The points the records above are measured against:
99 @ depth 3 (Shi–Feng–Xu, ToSC 2023); 97 @ depth 4 and 94 @ depth 5
(Osvik–Canright, ePrint 2024/1076); 92 @ depth 6 (Maximov); 92 gates
(Xiang–Zeng–Lin–Bao–Zhang — the seed of method `"91"`); **88 gates (Jean,
ePrint 2026/1481)**, measured at depth 7 here — the paper states no depth;
and **89 gates at unstated depth (Sun–Yang–Li, ePrint 2025/1493)**, measured
at depth 9 here. Neither of the last two dominates our
89 @ depth 5, so the 97 @ 3, 92 @ 4 and 89 @ 5 all remain on the published
frontier. Both imported circuits are transcribed, oracle-verified and credited
under `../evidence/campaign87_imported_prior_art/`; the full record table and
lineage are in `../evidence/RESULTS.md`.
