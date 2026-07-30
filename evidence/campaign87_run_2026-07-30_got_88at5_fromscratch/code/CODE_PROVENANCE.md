# The code that produced the from-scratch 88 @ depth 5

**Nothing is copied into this folder, on purpose.** The five files that produced
this circuit are **byte-identical** to the ones already archived — and already
published, in v3.0.0 on 2026-07-29 — with the 88 @ depth 6 in
`../../campaign87_run_2026-07-28_got_88at6_fromscratch/code/`. Duplicating them
would add ~88 kB to the repository and, worse, would create a second copy that
could drift. They are pinned here instead:

| file | sha256 | bytes | mtime | role |
|---|---|---|---|---|
| `engines.py` | `8e05f83a18c20238d37b98f3a37d7fffbb4c7c50756d42a187e3706e51334e29` | 52 522 | 2026-07-27 20:48 | the v2 merged engine (`engine_walk`, `engine_lns`, `_Harvester`) |
| `hunt_worker.py` | `e71a3cbcc09348de776d4bd5a32206cd6786ccade517f2677f6060e78397a089` | 13 030 | 2026-07-27 20:49 | one uncapped worker: root selection, `alt` chunk cycle, per-restart `LocalCtx` |
| `constructors.py` | `5561801b69466a76be44bc7af712d1bea1d0253e61889e78162aaaaa3201eb8f` | 11 884 | 2026-07-27 21:06 | the from-scratch root constructors; `build("naive", 1958)` is this record's root |
| `mixcolumns_core.py` | `d1659287f64217e31a47b14e5baf145997fb6867e9bb27c86873bfdcc9765d46` | 5 524 | 2026-07-27 20:27 | the GF(2⁸) spec and in-process oracle |
| `verify_circuit.py` | `5feaf4d5ec8bde0f7130e75ec6d7a4301905528c958f80499efca46a83cdc120` | 4 927 | 2026-07-27 20:27 | the standalone oracle the worker's saves were re-checked with |

Check the pin:

```
cd ../../campaign87_run_2026-07-28_got_88at6_fromscratch/code
sha256sum engines.py hunt_worker.py constructors.py mixcolumns_core.py verify_circuit.py
```

**Why this is evidence and not just tidiness.** Those files were committed to a
public repository on 2026-07-29, and their modification times are 2026-07-27 —
**two days before** this circuit was found (2026-07-30 10:48:19). The code that
produced this record was therefore fixed, archived and published before the run
that produced it reached its result. `../PROVENANCE.md` corroboration (b) makes
the same point about the log.

`engines.py` is the shipped `pipeline/engines.py` plus exactly three additions
(harvester reuse across chunks, a harvest size cap, and knob-gated family
repulsion, which was **off** here); `run_engine(...)` is unchanged and none of
the three touches the moves, the acceptance rule or the kernel. The full
comparison is in the 88 @ depth 6 archive's own `CODE_PROVENANCE.md`.

**Root reproduction.** `constructors.py` re-derives this record's root exactly:

```
$ python3 -c "import sys; sys.path.insert(0,'.'); import constructors; \
  [print('naive#%d -> %dg d%d' % (s, constructors.build('naive',s)[2]['gates'], \
   constructors.build('naive',s)[2]['depth'])) for s in (201,1843,1958)]"
naive#201 -> 142g d3
naive#1843 -> 143g d3
naive#1958 -> 146g d3
```

Each matches the corresponding
`--- restart N from naive#S (Ng dD) ---` line of session 5 in
`../runs_hunt/c_naive.log` (restarts 1, 15 and **16**; the log is cut inside
restart 16, so there is no restart 17 in this session to check).
Re-validated 2026-07-30.

## Certificate code

The k ≤ 3 shell sweep used the same two files as the 88 @ depth 6's, also
unchanged and already in the repository:

| file | sha256 |
|---|---|
| `../../campaign87_run_2026-07-28_got_88at6_fromscratch/certificates/shell_sweep.py` | `02067b36b27f3ac88667c0d8582ae287c8d3d21dbcc8e2dcc9fd0db375582333` |
| `../../campaign87_certificates/code/exact_window.py` | `9af714b775a4cc30da5de38db4e803c7904d32ea8f9a9f5172eb340f70caa88d` |

## Not archived here

`supervisor.py`, the fleet launcher. It is not load-bearing: what it contributed
is the worker's command line, recorded verbatim in `CONFIG_AS_RUN.md` and in the
first line of each session in the worker log. Unlike the 88 @ depth 6 archive,
the as-run copy of it does still exist (last edited 2026-07-29 15:34, one minute
before session 5 began, untouched since), and it was read when checking that no
worker in this fleet could reach the cross-pollination code path — see
`../PROVENANCE.md`, vector 1.

`detector.py`, `explorer.py`, `archive.py`, `orbit_*.py` and the other lanes of
the fleet played no part in this record: `c_naive` reads no file produced by any
of them, and `hunt_worker.py` does not import `archive` at all.
