# pipeline — the record-hunting search engine

Everything needed to hunt for smaller or shallower AES-MixColumns XOR circuits.
Stdlib Python 3, one OS process per search worker.

**How it works** — the representation, the three engines, the coordinator, with
diagrams: [`HOW.md`](HOW.md).
**Where each record actually came from** — run by run, with its archive:
[`../evidence/RESULTS.md`](../evidence/RESULTS.md).

| file | role |
|---|---|
| `ladder_parallel.py` | the entry point, the coordinator, and all config at the top |
| `worker.py` | one search worker: time-boxed chunks forever, verify-before-claim, adopts reseeds, harvests plateau states |
| `engines.py` | the search engines `lns`, `walk`, `anneal3`, plus the depth machinery |
| `mixcolumns_core.py` | MixColumns from GF(2⁸), the verifier, the seed loader, the from-scratch start |
| `seeds/` | the warm-start circuits the fixed worker sets use — provenance table in `seeds/README.md` |

## Run it

```
python3 ladder_parallel.py [--mode cascade|fixed] [--workers hunt87|sub89]
                           [--stop-gates N] [--stop-depth D]
```

```
# from-scratch depth ladder (hours):
python3 ladder_parallel.py --mode cascade --stop-gates 92 --stop-depth 4

# the fixed 87-hunting set; no stop bound, runs until Ctrl-C:
python3 ladder_parallel.py --mode fixed

# the two-worker set that reaches 89 @ depth 5 (seconds):
python3 ladder_parallel.py --mode fixed --workers sub89 --stop-gates 89 --stop-depth 5
```

`--stop-gates` / `--stop-depth` shut everything down cleanly once a verified
global best satisfies both bounds; an omitted bound is a don't-care. Without
them the run continues until Ctrl-C. Either way every best is already on disk.

One caveat before scripting a run: the stop test is applied to one Pareto
*global* best across all workers, and that best never regresses. A worker that
reaches a small gate count at a depth above your `--stop-depth` can make the
pair unsatisfiable for the rest of the run.

## The shipped configurations

- **`--mode cascade` (the default)** — the from-scratch depth ladder: the
  depth-3 rung starts from nothing with `anneal3`, and each time the frontier
  rung beats its baseline (or times out) the next deeper rung launches seeded
  from it. All rungs keep running and reseed each other. This shape produced
  **92 @ depth 4** from nothing, at t = 9 610 s. Expect hours.
- **`--mode fixed --workers hunt87`** — the 87 hunt: one uncapped `alt` worker
  on each of three 88-gate families, plus a depth-6-capped `lns` worker on the
  89 @ depth 5 circuit. The family workers run with `reseed=False` on purpose —
  an equal-size shallower offer counts as Pareto-better, so one reseed pass
  would collapse all three onto one circuit and destroy the diversity that is
  the point of the set. **Provenance: two of the three family seeds descend from
  published work** (see `seeds/README.md`), so anything those workers produce is
  derived work and must be reported that way.
- **`--mode fixed --workers sub89`** — the two-worker set that reached
  **89 @ depth 5**: an uncapped `lns` worker on the 89 @ depth 6 circuit and a
  depth-5-capped `lns` worker on the 90 @ depth 5 circuit, reseeding each other.
  Re-run 2026-09-02: 20 s end to end. Note it runs *today's* engines, not the
  engine of the archived run; to replay that run itself, use its own `code/`
  folder in `../evidence/`.

## Engines

| name | move | use |
|---|---|---|
| `lns` | destroy part of the circuit and re-synthesise it | the main hunter; pushes a warm-started circuit down |
| `walk` | remove one mask (or two) and repair by complete enumeration | fast sideways motion across the equal-size plateau |
| `anneal3` | anneal a model in which depth 3 holds by construction | reaching a low count at depth exactly 3, from nothing |
| `alt` | not an engine: alternate a `walk` chunk with a longer `lns` chunk | how all five 88-gate circuits were reached |

Mechanism, acceptance rules and every knob's effect: [`HOW.md`](HOW.md).

## Knobs

All knobs live at the top of `ladder_parallel.py` (`LNS_KNOBS`, `WALK_KNOBS`,
`ANNEAL_KNOBS`), each with a one-line comment; a worker dict overrides any of
them with `knobs=` (for an `alt` worker, keyed by engine). **The defaults are
the measured-good configuration** — a sweep of 101 runs across a broad range of
settings produced 0 gate-count improvements, so knobs buy throughput, not
records. Each run writes its fully resolved knob set to `config.json`.

Two switches change what a run *means*, not just how fast it is:

- `harvest` (on) — append every distinct plateau state to `<label>.pop.jsonl`.
  Cheap, and that population is what the exact irreducibility certificates were
  run over. It also fills a disk: a few MB per worker-minute.
- `cross_pollinate` (off) — merge sibling workers' harvested masks into this
  worker's rebuild pool. A measured-good diversifier, but it mixes the mask
  provenance of every worker in the run: a circuit found in a pool containing
  masks from an imported circuit is derived from published work. Turn it on
  deliberately, for a run whose seeds are all your own.

## Output

`runs_parallel/<timestamp>/` (created at run time): `coordinator.log`,
`config.json`, and per worker `<label>_best.json`, `<label>_status.json`,
`<label>.log`, `<label>.pop.jsonl`, plus `best_overall.json` and
`reseed_<label>.json`. Every run self-archives the exact code that produced it
into its own `code/` folder.

## Verify anything independently

Every `_best.json` is an index-pair circuit. Check it with the standalone oracle
one folder up, which shares no code with the engines:

```
python3 ../verify_circuit.py runs_parallel/<timestamp>/best_overall.json
```
