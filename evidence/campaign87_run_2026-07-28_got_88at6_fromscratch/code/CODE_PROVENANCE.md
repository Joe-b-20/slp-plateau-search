# The code that produced the 88 @ depth 6

Copied verbatim from `campaign_87/hunt87/` (the raw 87-hunt tree, not in this
repository). The fleet instance that produced the record launched **2026-07-27
22:22:27**; every file here has a modification time *before* that, so each is
the version the worker imported:

| file | mtime | role |
|---|---|---|
| `engines.py` | 2026-07-27 20:48 | the v2 merged engine (`engine_walk`, `engine_lns`, `_Harvester`) |
| `hunt_worker.py` | 2026-07-27 20:49 | one uncapped worker: root selection, `alt` chunk cycle, per-restart `LocalCtx` |
| `constructors.py` | 2026-07-27 21:06 | the four from-scratch root constructors; `build("naive", 2163)` is this record's root |
| `mixcolumns_core.py` | 2026-07-27 20:27 | the GF(2⁸) spec and in-process oracle |
| `verify_circuit.py` | 2026-07-27 20:27 | the standalone oracle the worker's saves were re-checked with |

`engines.py` here is the **shipped** `pipeline/engines.py` plus exactly three
additions (`diff pipeline/engines.py` against this file is 82 lines, 2 of them a
comment the shipped copy updated later):

1. `_harvester(k)` — one `_Harvester` per output path, reused across chunks, so a
   worker's harvest stays deduplicated for its whole life instead of per chunk;
2. `harvest_max` — states larger than 88 masks are not written, which is what
   keeps a multi-day fleet's harvest at hundreds of MB instead of tens of GB;
3. knob-gated family repulsion (`repel_file`, `repel_pen`, `repel_up_p`) —
   **off** for this worker (`repel=False`), so it is inert here.

`run_engine(...)` is unchanged. None of the three touches the moves, the
acceptance rule or the kernel, so the search that found this circuit is the
shipped engine's search.

**Root reproduction (the strongest check available here).** `constructors.py` was
edited 44 minutes before the fleet launched, so its mtime alone does not settle
whether it is the as-run version. It re-derives the logged roots exactly:

```
$ python3 -c "import sys; sys.path.insert(0,'.'); import constructors; \
  [print('naive#%d -> %dg d%d' % (s, constructors.build('naive',s)[2]['gates'], \
   constructors.build('naive',s)[2]['depth'])) for s in (201,2050,2163,2282)]"
naive#201 -> 142g d3
naive#2050 -> 142g d3
naive#2163 -> 139g d3
naive#2282 -> 138g d3
```

Each matches the corresponding `--- restart N from naive#S (Ng dD) ---` line in
`../runs_hunt/c_naive.log` (restarts 1, 17, **18**, 19). Re-validated 2026-07-29.

## Not archived here

`supervisor.py`, the fleet launcher, was edited on 2026-07-29 (shrinking the
fleet from 15 search workers to 5) and so is **not** the version that ran. What
it contributed is the worker's command line, which is recorded verbatim in
`CONFIG_AS_RUN.md` and in the first line of the worker log. `detector.py`,
`explorer.py`, `archive.py`, `orbit_*.py` and the other lanes of the fleet played
no part in this record: `c_naive` reads no file produced by any of them.
