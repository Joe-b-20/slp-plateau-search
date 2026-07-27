# Code provenance — campaign-87 merged-engine hunt (2026-07-26, produced 88@d7)

Every file here is the **exact producing version**, copied unmodified from
`campaign_87/agents/merged-engine/` after the run:

| file | source | role |
|---|---|---|
| `engines.py` | `work/engines.py` | the merged engine — `engine_lns`, `engine_walk`, `engine_anneal3`, `run_engine` |
| `hunt_worker.py` | `work/hunt_worker.py` | one long-hunt worker: chunked runs, reseed-from-own-best, harvest file, verify-before-claim `ctx.improve` |
| `mixcolumns_core.py` | `work/mixcolumns_core.py` | spec + GF(2⁸) oracle (`verify`) |
| `worker.py`, `ladder_parallel.py` | `work/` | the repo pipeline's worker/orchestrator, carried along unchanged (the hunt used `hunt_worker.py`, not these) |
| `verify_circuit.py` | `work/verify_circuit.py` | the standalone oracle, byte-identical to the repo root copy |
| `launch_hunt.sh`, `status.sh` | agent folder | the launcher as run, and its monitor |

Dependency-free Python 3 standard library only, as everywhere in this repo.

## What changed in the engine relative to the repo pipeline of 2026-07-16

The merge integrates the seven measured wave-1 improvements; `run_engine`'s
signature is unchanged, so this file is a drop-in replacement for
`pipeline/engines.py`.

- `relax()` rewritten as level-BFS (+ `relax_reference` kept verbatim as the
  duplicate-mask fallback); `feasible_at` does realizability-only closure with
  early exit when `cap=None`.
- New worklist closure core `_closure_core` (stop-at-targets), new
  `_WalkState.remove_query` incremental removal closure; `improve()` is now
  called only on iterations that changed `cur` (this was 78 % of walk runtime).
- `_extract` takes an integer **cost-class** list instead of a bool `preferred`
  (bool still accepted); destroyed victims stay in the candidate pool at cost 3
  ("victim-repool"), which makes every LNS iteration feasible by construction.
- New destroy operators `coneinj` / `biginj` with injected rebuild candidates
  (`dag_info`, `_inject`, `_cone_pick`), knob-selected via `op_mix`;
  **peel-before-accept** for near-miss rebuilds.
- `_repair` is now the exact complete enumeration (C ∩ P2) with
  forbid-just-removed and min-trim choice.
- Scored hot-multiset pool sampling + peel cache.
- SA-with-reheat acceptance by default.
- New: plateau **harvesting** (`harvest_path` — every distinct equal-best-size
  mask set appended to a `.pop.jsonl`) and **cross-pollination** (`pop_glob`,
  `pop_period_s`) — LNS only.

New knobs, all defaulted so old configs behave as before: `op_mix`, `vic_cost`,
`hot_frac`, `accept`, `sa_T0`, `sa_cool`, `sa_reheat`, `peel_window`,
`biginj_lo/hi`, `cone_lo/hi`, `harvest_path`, `pop_glob`, `pop_period_s`.

Nothing in the engine ever claims a gate count: candidates go to `ctx.improve`,
which verifies against the GF(2⁸) oracle before anything is saved or logged.
