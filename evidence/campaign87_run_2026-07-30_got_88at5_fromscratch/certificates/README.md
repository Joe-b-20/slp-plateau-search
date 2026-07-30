# Exhaustive k ≤ 3 shell of the from-scratch 88 @ depth 5, and its depth-5 pocket

Run on **2026-07-30** with the repository's own archived decider — the same two
files as the 88 @ depth 6's sweep, unchanged and hash-pinned in
`../code/CODE_PROVENANCE.md`:
`../../campaign87_run_2026-07-28_got_88at6_fromscratch/certificates/shell_sweep.py`
over `../../campaign87_certificates/code/exact_window.py`.

| log | radius | windows | verdict | wall |
|---|---|---|---|---|
| `k2_shell_88at5fs.log` | k = 2, budget 1 | 1 540 = C(56,2) | **1 540 irreducible, 0 hits** | 6 s, 1 process |
| `k3_shell_88at5fs_shard[0-2].log` | k = 3, budget 2 | 3 × 9 240 = 27 720 = C(56,3) | **27 720 irreducible, 0 hits** | 952–983 s, 3 processes |

`k3_s[0-2].out` are the drivers' stdout lines for the same three shards.
Sharding is by window index and is only for wall-clock; the union of the shards
is the full enumeration.

Both budgets are exhaustive (complete by the first-unlock case analysis proved in
`exact_window.py`'s docstring), so this is a proof for exactly those radii: **any
87-gate circuit differs from this one by ≥ 4 masks.** It bounds nothing globally,
and no 87-gate circuit was found anywhere in the campaign.

```
python3 ../../campaign87_run_2026-07-28_got_88at6_fromscratch/certificates/shell_sweep.py \
        ../FOUND_88gates_depth5_fromscratch.json 2 k2_shell_88at5fs.log
for s in 0 1 2; do
  python3 ../../campaign87_run_2026-07-28_got_88at6_fromscratch/certificates/shell_sweep.py \
          ../FOUND_88gates_depth5_fromscratch.json 3 k3_shell_88at5fs_shard$s.log $s 3 &
done
```

The input was `../FOUND_88gates_depth5_fromscratch.json`, whose gate list is
byte-identical to the canonical
`../../circuits/mixcolumns_88gates_depth5_fromscratch.json`.

## `pocket_depth5_scan.log` — the 135-member depth-5 pocket

Not a certificate: a scan. Every distinct 88-gate target-covering value set in
`c_naive`'s own harvest file was replayed and given its ASAP (least-fixpoint)
depth by `pipeline/engines.py:relax`, i.e. the shallowest depth that mask set
admits at all. Of 37 305 distinct states, **135 realize at depth 5** — the record
is one of them, and every one of the 135 first appears at or after line 35 285,
the record's own line. The harvest itself is live and stays in the raw campaign
tree (`campaign_87/hunt87/runs/c_naive.pop.jsonl`), which is not part of this
repository.
