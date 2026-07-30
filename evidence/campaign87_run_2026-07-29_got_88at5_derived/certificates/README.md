# Exhaustive k = 2 shell of the 88 @ depth 5

Re-run from this repository on **2026-07-29** with `shell_sweep.py`, which uses
the repo's own archived decider
`../../campaign87_certificates/code/exact_window.py`.

| log | radius | windows | verdict | wall |
|---|---|---|---|---|
| `k2_shell_88at5.log` | k = 2, budget 1 | 1 540 = C(56,2) | **1 540 irreducible, 0 hits** | 5 s, 1 process |

Budget 1 is exhaustive, so this is a proof for that radius: **any 87-gate circuit
differs from this one by ≥ 3 masks.** It bounds nothing globally.

**The k = 3 shell of this circuit was not swept** — unlike the 88 @ depth 6, whose
k ≤ 3 shell is closed. Together with this project's 88 @ depth 7, which has no
exhaustive shell at any radius, this is one of the two least certified circuits in
the repository. The sweep is a few minutes of CPU if anyone wants it:

```
python3 shell_sweep.py ../FOUND_88gates_depth5.json 2 k2.log
for s in 0 1 2 3; do python3 shell_sweep.py ../FOUND_88gates_depth5.json 3 k3_$s.log $s 4 & done
```
