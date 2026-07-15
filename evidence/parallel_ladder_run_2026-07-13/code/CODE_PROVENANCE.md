# Code provenance -- 21h ladder run (2026-07-13)

- `worker.py`, `ladder_parallel.py`, `hunt.py`, `mixcolumns_core.py` are the
  EXACT files from `method_reconstruction/record_hunter/` that launched this run
  (old-style cascade coordinator: no reseeding, no Pareto tie-break; the worker's
  `improve()` accepted strictly-fewer-gates only).
- `engines.py` is the current `record_hunter/engines.py`, which received ONE
  later patch after this run: the "no depth cap" sentinel was changed from
  INF=40 to INF=1_000_000 and the feasibility/emit checks tightened, fixing a
  crash in unconstrained-depth (`final` rung) circuit emission. That patch does
  NOT affect any circuit this run produced -- every rung was re-verified
  independently (see ../HARVEST.md). The exact pre-patch engines.py was edited
  in place and is not separately preserved.
