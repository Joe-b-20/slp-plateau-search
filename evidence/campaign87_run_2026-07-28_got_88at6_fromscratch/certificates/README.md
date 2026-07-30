# Exhaustive k ≤ 3 shell of the 88 @ depth 6

Re-run from this repository on **2026-07-29** with `shell_sweep.py`, which uses
the repo's own archived decider
`../../campaign87_certificates/code/exact_window.py` (byte-identical to the copy
the 87-hunt used).

| log | radius | windows | verdict | wall |
|---|---|---|---|---|
| `k2_shell_88at6.log` | k = 2, budget 1 | 1 540 = C(56,2) | **1 540 irreducible, 0 hits** | 5 s, 1 process |
| `k3_shell_88at6_shard[0-3].log` | k = 3, budget 2 | 4 × 6 930 = 27 720 = C(56,3) | **27 720 irreducible, 0 hits** | 432–454 s, 4 processes (CPython, on a loaded box) |

Both budgets are exhaustive, so this is a proof for those radii: **any 87-gate
circuit differs from this one by ≥ 4 masks.** It bounds nothing globally.

The input was `../FOUND_88gates_depth6.json`, whose gate list is byte-identical to
the canonical `../../circuits/mixcolumns_88gates_depth6.json`.

```
python3 shell_sweep.py ../FOUND_88gates_depth6.json 2 k2.log
for s in 0 1 2 3; do python3 shell_sweep.py ../FOUND_88gates_depth6.json 3 k3_$s.log $s 4 & done
```
