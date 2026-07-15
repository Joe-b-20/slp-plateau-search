# reproduce — the from-scratch depth-3 record in pure Python

One command reproduces the current depth-3 record for AES MixColumns — **97
gates at depth 3, from scratch** — in minutes, on one core, stdlib only:

```
python3 reproduce.py
```

The method searches (simulated annealing + iterated local search over a
shared depth-1-pairs / depth-2-parts model; targets computed from GF(2⁸), no
seed), then the result is checked by an independent GF(2⁸) verifier and
written to `out_97.json`. A summary table prints at the end.

The other two current records are pipeline runs, not single-file scripts:

| record | how to reproduce | time |
|---|---|---|
| 89 @ depth 5 | `../pipeline/` with `MODE="fixed"` (the exact sub-89 run config, shipped) | ~10–15 min |
| 92 @ depth 4 | `../pipeline/` with `MODE="cascade"` (the from-scratch ladder) | hours |

See `../pipeline/README.md` for both, including the code-evolution history of
the runs that found them.

## Legacy demonstrations (opt-in)

Three further methods demonstrate the individual moves on this project's
*superseded* records; add them to `RUN` at the top of `reproduce.py` to run
them. Honest provenance, per method:

- **`"91"`** — starts from the *published* 92-gate SLP of Xiang, Zeng, Lin,
  Bao, and Zhang (embedded in `seeds.py` as data) and walks the plateau of
  equal-size circuits until one gate becomes removable → 91 @ depth 6
  (~5–60 s).
- **`"89"`** — the value-set walk (remove-1 + remove-2-add-1 hub moves) cuts
  a 90-gate seed to 89 at unconstrained depth (~1–4 min). From nothing this
  method floors near 92; the 89 needs the seed.
- **`"90"`** — proves a 91-gate seed admits no single local cut (duplicate
  scan, peel, all-pairs remove-2-add-1), and with `C90["lns_seconds"] > 0`
  runs the pure-Python LNS re-synthesis (reaches ~91).

## Files

| file | what it is | edit it? |
|---|---|---|
| `reproduce.py` | the runnable script: **CONFIG block at the very top** (every knob), then the methods, then the runner | yes — all tuning lives at the top |
| `mixcolumns_core.py` | the MixColumns spec rebuilt from GF(2^8) + the verifier | no — this is the trustworthy math |
| `seeds.py` | the embedded seed circuits (data) | no — starting points, not answers |

## Verify independently

Every `out_<method>.json` is an index-pair circuit (`{"gates":[[a,b],...]}`,
signals 0..31 = inputs, gate k → signal 32+k). Re-check any of them with the
standalone verifier one folder up:

```
python3 ../verify_circuit.py out_97.json 3
python3 ../verify_circuit.py out_91.json 6
```
