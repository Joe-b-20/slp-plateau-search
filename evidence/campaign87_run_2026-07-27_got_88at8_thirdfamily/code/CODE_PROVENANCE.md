# Code provenance — campaign-87 hunt-deeper run (2026-07-27, produced 88@d8)

Every file here is the **exact producing version**, copied unmodified from
`campaign_87/agents/hunt-deeper/` after the run:

| file | source | role |
|---|---|---|
| `engines.py` | `work/engines.py` | the merged engine (see the 88@7 archive's `CODE_PROVENANCE.md` for the merge itself) **plus family repulsion** |
| `hunt_worker.py` | `work/hunt_worker.py` | merged-engine's worker **plus drift-mode reseeding** |
| `mixcolumns_core.py` | `work/mixcolumns_core.py` | spec + GF(2⁸) oracle |
| `worker.py`, `ladder_parallel.py` | `work/` | repo pipeline worker/orchestrator, carried along unchanged (unused by this hunt) |
| `verify_circuit.py` | `work/verify_circuit.py` | standalone oracle, byte-identical to the repo root copy |
| `launch_hunt.sh`, `monitor_pass.sh` | agent folder | the launcher as run, and its monitor |
| `census.py` | agent folder | incremental dedupe of harvested 88s + online Jaccard family detector |

Dependency-free Python 3 standard library only.

## Delta versus the 88@7 run's `engines.py`

Exactly two additions, both knob-gated and **off by default** (`diff` against
`campaign_87/agents/merged-engine/work/engines.py` is 30 lines):

- **Family repulsion** — new knobs `repel_file`, `repel_pen` (LNS only),
  `repel_up_p`. In `engine_lns` a repel mask's pull-in cost class is bumped by
  `repel_pen`; in both engines a plateau/uphill move that *increases* overlap
  with the repel set is rejected with probability `1 − repel_up_p`
  (`rep_ok` in `engine_walk`).
- **Drift-mode reseeding** — `hunt_worker.py` knob `drift_refs`: instead of
  reseeding each chunk from the frozen Pareto best (which discarded all plateau
  drift), reseed from the most family-distant best-size state harvested in the
  previous chunk, with a +0.05 slack ratchet.

**Neither was active for the record worker `d3_orb90a`** — it was launched with
`'{}'`, so both `repel_file` and `drift_refs` are unset (verifiable on line 1 of
`../runs_hunt/d3_orb90a.log`). They were used by this fleet's *other* workers
(tracks P and F), whose logs are archived alongside.

Verify-before-claim is unchanged: engines propose, `ctx.improve` verifies against
the GF(2⁸) oracle before anything is saved or logged.
