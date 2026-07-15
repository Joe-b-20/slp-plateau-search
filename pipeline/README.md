# pipeline — the record-hunting pipeline

Everything needed to hunt for smaller/shallower AES-MixColumns XOR circuits.
Four modules + seeds:

| file | role |
|---|---|
| `ladder_parallel.py` | the entry point + all config at the top; the coordinator |
| `worker.py` | one search worker: runs in chunks forever, verify-before-claim, adopts reseeds |
| `engines.py` | the search engines: `lns`, `walk`, `anneal3` + depth machinery |
| `mixcolumns_core.py` | MixColumns spec from GF(2^8), the verifier, seed loader, from-scratch builder |
| `seeds/` | the warm-start circuits used by the shipped fixed-mode config |

Run it:

```
python3 ladder_parallel.py [--mode cascade|fixed] [--stop-gates N] [--stop-depth D]

# replicate the records:
python3 ladder_parallel.py --mode fixed   --stop-gates 89 --stop-depth 5
python3 ladder_parallel.py --mode cascade --stop-gates 92 --stop-depth 4
```

`--stop-gates`/`--stop-depth` shut everything down cleanly once a verified
global best satisfies both given bounds; without them the run continues until
Ctrl-C.

Output goes to `runs_parallel/<timestamp>/` (created at run time; not code):
`coordinator.log`, `config.json`, and per worker `<label>_best.json`,
`<label>_status.json`, `<label>.log`, plus `best_overall.json` (the global
best) and `reseed_<label>.json` (what the coordinator offered each worker).
Stop with Ctrl-C; every best is already on disk. Every run self-archives the
exact code that produced it into its own `code/` folder.

## The two shipped configurations

- **`MODE = "cascade"` (the default)** — the from-scratch depth ladder: rung
  d3 starts from nothing with `anneal3`; each time the frontier rung beats its
  baseline (or times out) the next deeper rung launches, seeded from it; all
  rungs keep running and reseed each other. This is the configuration shape of
  the run that produced **92 @ depth 4** (and independently re-derived the
  from-scratch 97 @ depth 3). Expect hours.
- **`MODE = "fixed"`** — shipped as the exact two-worker configuration of the
  sub-89 run that produced **89 @ depth 5**: an uncapped `lns` worker seeded
  with the 89@depth6 circuit, and a depth-5-capped `lns` worker seeded with
  the 90@depth5 circuit, reseeding each other. In the archived run the
  uncapped worker surfaced 89 @ depth 5 after ~10 minutes.

## How the pipeline evolved across the three record runs (and why three runs)

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

The `pipeline/` code here is the newest flavor (the cascade/sub-89 code, plus
inert support for per-worker RNG-seed/knob overrides added afterwards); for
any archived run, the authoritative code is the one inside that run's
`code/` folder.

## Engines

- `lns` — depth-capped destroy-and-rebuild (the main hunter), seedable.
- `walk` — value-set remove-1 / remove-2-add-1 hub moves, seedable.
- `anneal3` — depth-3 partition annealer, from scratch (the cascade's
  depth-3 rung).

## Verify anything independently

Each `_best.json` / `best_overall.json` is an index-pair circuit. Check it
with the standalone oracle one folder up:

```
python3 ../verify_circuit.py runs_parallel/<timestamp>/best_overall.json
```
