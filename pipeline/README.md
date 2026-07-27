# pipeline — the record-hunting pipeline

Everything needed to hunt for smaller/shallower AES-MixColumns XOR circuits.
Four modules + seeds:

| file | role |
|---|---|
| `ladder_parallel.py` | the entry point + all config at the top; the coordinator |
| `worker.py` | one search worker: runs in chunks forever, verify-before-claim, adopts reseeds, harvests plateau states; `alt` mode alternates walk and lns chunks |
| `engines.py` | the search engines: `lns`, `walk`, `anneal3` + depth machinery |
| `mixcolumns_core.py` | MixColumns spec from GF(2^8), the verifier, seed loader, from-scratch builder |
| `seeds/` | the warm-start circuits used by the shipped fixed-mode worker sets (`seeds/README.md` has the provenance table) |

Run it:

```
python3 ladder_parallel.py [--mode cascade|fixed] [--workers hunt87|sub89]
                           [--stop-gates N] [--stop-depth D]

# hunt 87 from the three known 88-gate families (the shipped configuration):
python3 ladder_parallel.py --mode fixed

# replicate the earlier records:
python3 ladder_parallel.py --mode fixed --workers sub89 --stop-gates 89 --stop-depth 5
python3 ladder_parallel.py --mode cascade --stop-gates 92 --stop-depth 4
```

`--stop-gates`/`--stop-depth` shut everything down cleanly once a verified
global best satisfies both given bounds; without them the run continues until
Ctrl-C.

Output goes to `runs_parallel/<timestamp>/` (created at run time; not code):
`coordinator.log`, `config.json`, and per worker `<label>_best.json`,
`<label>_status.json`, `<label>.log`, `<label>.pop.jsonl` (the harvested
plateau population — this one grows fast, a few MB per worker-minute), plus
`best_overall.json` (the global best) and `reseed_<label>.json` (what the
coordinator offered each worker). Stop with Ctrl-C; every best is already on
disk. Every run self-archives the exact code that produced it into its own
`code/` folder.

## The shipped configurations

- **`MODE = "cascade"` (the default)** — the from-scratch depth ladder: rung
  d3 starts from nothing with `anneal3`; each time the frontier rung beats its
  baseline (or times out) the next deeper rung launches, seeded from it; all
  rungs keep running and reseed each other. This is the configuration shape of
  the run that produced **92 @ depth 4** (and independently re-derived the
  from-scratch 97 @ depth 3). Expect hours.
- **`--mode fixed --workers hunt87`** — the current hunt for 87: one uncapped
  `alt` worker on each of the three known 88-gate families (ours 88@7, the
  third-family 88@8, and Jean's published 88@7), plus a depth-6-capped `lns`
  worker on our 89@depth5. The family workers run with `reseed=False`: an
  equal-size shallower circuit counts as Pareto-better, so a single reseed pass
  would collapse all three onto one circuit and destroy the diversity that is
  the whole point. Mind the provenance: two of the three family workers stand on
  Jean's published circuit (see `seeds/README.md`), so anything they produce is
  *derived from published work*.
- **`--mode fixed --workers sub89`** — the historic two-worker configuration
  of the run that produced **89 @ depth 5**: an uncapped `lns` worker seeded
  with the 89@depth6 circuit, and a depth-5-capped `lns` worker seeded with
  the 90@depth5 circuit, reseeding each other. In the archived run the
  uncapped worker surfaced 89 @ depth 5 after ~10 minutes — with that run's
  engine, which is not this one; to replay the run itself use its `code/`.

## Engines

- `lns` — destroy-and-rebuild (the main hunter), depth-capped, seedable.
- `walk` — value-set remove-1 / remove-2-add-1 hub moves, seedable. Fast and
  exploratory; the plateau sprayer.
- `anneal3` — depth-3 partition annealer, from scratch (the cascade's depth-3
  rung). Unchanged since v1.
- `alt` — not an engine but a worker mode: alternate a 300 s `walk` chunk with
  a 600 s `lns` chunk from the worker's own best. The walk sprays across the
  plateau, the lns punches down from wherever it ended up.

## How the pipeline evolved (four chapters)

### 1–3. The three record runs (v1)

The three archived runs in `../evidence/` were produced by **two code
flavors**; each archive contains the exact code in its `code/` folder with a
`CODE_PROVENANCE.md`, so every statement here can be checked by diffing.

1. **`parallel_ladder_run_2026-07-13`** (found the from-scratch **97 @ depth
   3**, and reached 89 @ depth 6 at rung d10) ran the *old-style* coordinator:
   no reseeding between workers, and `improve()` accepted **strictly fewer
   gates only**. That acceptance rule silently discards a circuit with equal
   gates at lower depth — which is exactly what was later discovered sitting
   next to 89@depth6.
2. **`cascade_run_2026-07-14_from_scratch_newlogic`** (found **92 @ depth
   4**) ran the rewritten coordinator/worker: the **Pareto tie-break**
   (accept fewer gates, OR equal gates at strictly lower depth — and the
   engines were changed to *surface* such candidates rather than drop them)
   and **continuous reseeding** (the coordinator offers every worker the best
   circuit feasible at its depth cap; workers adopt offers between chunks).
   The 92@depth4 was found by the depth-8 rung searching with slack and kept
   only because of the tie-break.
3. **`sub89_run_2026-07-14_got_89at5`** (found **89 @ depth 5**) ran
   **byte-identical code** to the cascade run — only the configuration
   differs (the fixed two-worker setup above, pointed at the frontier
   circuits the earlier runs had produced).

So the records could not have come from one run: the first run's code could
not even *accept* an 89@depth5 while holding 89@depth6, and the third run's
seeds are outputs of the earlier runs. The evolution — old acceptance rule →
Pareto tie-break + reseeding → same code re-aimed at the frontier — is itself
part of the method story (see `../METHODS.md`).

### 4. The 88-gate campaign (v2, the engine you are running)

A 24-agent campaign took the v1 engine apart, measured every piece separately,
and rebuilt `lns` and `walk` around what survived measurement. The curated run
archives are `../evidence/campaign87_*`; the raw campaign archive is not part of
this repository.

The changes, each with its measured effect, are tabulated in
[`../METHODS.md`](../METHODS.md) §5 (the kernel) and §6 (the engines): level-BFS
`relax` with realizability-only `feasible_at` when uncapped, worklist closure
with incremental removal queries, the improve-only-on-change fix, victim
repooling, the `coneinj`/`biginj` destroy mix, peel-before-accept, exact complete
repair enumeration, scored hot pools with a peel cache, SA-with-reheat
acceptance, plateau harvesting, and the `champ_fast` knob values that are now the
defaults. End to end, on a loaded box, the merged engine walked at 480–640 it/s
against ~70–110 before, and ran LNS at ~100–180 against ~60–100 with much richer
neighbourhoods.

Three things were tried, measured, and **left out**: an extra `useful` reuse
score in the rebuild's tie-break and per-victim `restarts` (marginal, and
diversity-negative), and a kick-restart acceptance schedule (no better than SA
with reheat, and it clashes with the victim cost classes).

Two new 88-gate circuits came out of the campaign, both oracle-verified and both
found by this engine. **88 @ depth 7** is of our own lineage with no imported
material; it matches the published 88-gate record (Jean, ePrint 2026/1481) with
an independent circuit — 61 of 88 masks in common — and does not beat it.
**88 @ depth 8** is a third distinct family whose *lineage passes through Jean's
published 88* (its ρ²-symmetric 90 seed was built partly by symmetrizing that
circuit), so it is a derived construction, and it is dominated by the 88@7
anyway. 87 was not found. Both are in `seeds/`, with their provenance in
`seeds/README.md`.

The knob sweep is worth knowing as a negative result: 0 improvements in 101 runs
across a broad range of settings around the v1 values. Knobs buy throughput; they
do not buy gate counts. What moved the frontier was the mechanisms above and
*where the workers were pointed*.

## Knobs

All knobs live at the top of `ladder_parallel.py` (`LNS_KNOBS`, `WALK_KNOBS`,
`ANNEAL_KNOBS`), each with a one-line comment; a worker dict can override any
of them with `knobs=` (for an `alt` worker, keyed by engine:
`knobs={"lns": {...}, "walk": {...}}`). The defaults ARE the campaign's
measured-good configuration. The run's full resolved knob set is written to
`runs_parallel/<timestamp>/config.json` and echoed into each worker log, so an
archived run always states its own configuration.

Two switches matter:

- `harvest` (on) — writes `<label>.pop.jsonl`. Cheap, and the population it
  produces is what the exact irreducibility certificates were run over. It is
  also the file that fills your disk on a long run.
- `cross_pollinate` (off) — merges sibling workers' harvested masks into this
  worker's rebuild pool every `pop_period_s`. Measured as a good diversifier in
  the campaign, but it mixes the mask provenance of every worker in the run: a
  circuit found in a pool that contains masks derived from an imported circuit
  is *derived from published work*. Turn it on deliberately, for a run whose
  seeds are all our own.

## Verify anything independently

Each `_best.json` / `best_overall.json` is an index-pair circuit. Check it
with the standalone oracle one folder up:

```
python3 ../verify_circuit.py runs_parallel/<timestamp>/best_overall.json
```
