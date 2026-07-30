# The code that produced the 88 @ depth 5

Copied verbatim from `campaign_87/hunt87/` (the raw 87-hunt tree, not in this
repository). The fleet instance launched **2026-07-27 22:22:30** and the find is
at 2026-07-29 09:39:18.

| file | mtime | as run? | role |
|---|---|---|---|
| `engines.py` | 2026-07-27 20:48 | **yes** | the v2 merged engine; `o_polish`'s walk chunk found the circuit |
| `hunt_worker.py` | 2026-07-27 20:49 | **yes** | `o_polish`: root selection by glob, `alt` chunk cycle, per-restart `LocalCtx` |
| `orbit_engine.py` | 2026-07-27 20:29 | **yes** | ρ²-equivariant moves in orbit space |
| `orbit_search.py` | 2026-07-27 20:30 | **yes** | the orbit ladder `o1` ran |
| `orbit_runner.py` | 2026-07-29 10:07 | **no — post-fix** | picks each orbit cycle's seed |
| `mixcolumns_core.py` | 2026-07-27 20:27 | **yes** | the GF(2⁸) spec and in-process oracle |
| `verify_circuit.py` | 2026-07-27 20:27 | **yes** | the standalone oracle |

`engines.py` is the **shipped** `pipeline/engines.py` plus exactly three
additions (an 82-line diff, 2 lines of it a comment the shipped copy updated
later): a per-path `_Harvester` reused across chunks, the
`harvest_max` size cap, and knob-gated family repulsion — **off** for this worker
(`repel=False`), hence inert. `run_engine(...)` is unchanged.

## `orbit_runner.py` is the fixed version, not the version that ran

It was edited **2026-07-29 10:07, 28 minutes after this find**. The as-run
`pick_seed` chose `orb[cycle % len(orb)]`; the archived version chooses
`orb[(cycle - cycle // 3) % len(orb)]` and carries the reason as a comment. The
difference is exactly why this circuit is derived work: under the old expression
index 2 — `seeds/orbit/sym94.json`, the only own-lineage orbit seed — was
unreachable, so all 233 orbit-seeded cycles in this fleet started from the two
Jean-descended 90s. See `../PROVENANCE.md`.

Nothing else about the descent depends on this file: it chose the seed, and the
seed it chose is archived beside the record as
`../seed_orbit_90gates_depth9_derived.json`, so the descent itself replays from
that file without `orbit_runner.py` at all.

## Not archived here

`supervisor.py` (edited 2026-07-29 for a fleet shrink, so not as-run — the two
workers' command lines are in `CONFIG_AS_RUN.md` and in the first line of each
log), and the fleet's other lanes, none of which fed these two workers:
`o_polish` reads only `runs/o?_c*_*g.json`, i.e. the orbit workers' own output.
