# Code provenance -- sub-89 run (2026-07-14, produced 89@depth5)

- `mixcolumns_core.py` and `engines.py` are the EXACT producing versions
  (unchanged since; these carry the Pareto-tie-break surfacing in the engines).
- `worker.py` and `ladder_parallel.py` are the current pipeline versions. They
  gained per-worker seed/knob support AFTER this run; those additions are inert
  when a worker supplies no `seeds`/`knobs` field (this run's workers did not), so
  this code reproduces this run's behaviour identically. Run with the config in
  CONFIG_AS_RUN.md + the config.json here. The byte-identical pre-addition
  orchestration was edited in place and is not separately preserved.
