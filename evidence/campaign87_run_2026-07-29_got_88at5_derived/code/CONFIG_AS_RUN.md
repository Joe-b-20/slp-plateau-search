# Configuration as run — workers `o1` and `o_polish`

Two workers, in series: the orbit ladder produced the 90 @ depth 9 file, the
polish worker descended it.

## `o1` — ρ²-equivariant orbit ladder

Launched by the fleet supervisor as:

```
python3 orbit_runner.py --label o1 --dir <hunt87> --seed 2101 --tlim 900
```

Log echo: `orbit worker start: label=o1 tlim=900s modes=['mixed', 'sym']`.
Each cycle picks a seed (`pick_seed`), then runs
`orbit_search.main(--seed <file> --mode <mixed|sym> --rng <2101000+cycle>
--tlim 900 --loose 3 --phase 90)` and saves the result as
`runs/o1_c<cycle>_<gates>g.json`.

The cycle that matters:

```
[116106.2s 06:37:36] --- cycle 129: seed=sym90_a.json mode=sym rng=2101129 ---
```

→ `runs/o1_c129_90g.json`, 90 gates at depth 9, mask-identical to its
Jean-descended seed (see `../PROVENANCE.md`).

## `o_polish` — desymmetrise and polish

```
python3 hunt_worker.py --label o_polish --dir <hunt87> \
        --root "glob:runs/o?_c*_*g.json" --seed 2301 \
        --restart-s 3600 --stall-s 1200
```

Log echo:

```
[     0.0s 22:22:30] hunt worker start: root=glob:runs/o?_c*_*g.json engines=alt
                     repel=False seed=2301 restart=3600s stall=1200s
```

| setting | value |
|---|---|
| depth cap | **none** (`cap=None`) — the depth 5 came from the Pareto tie-break, not from a cap |
| mode | `alt` — 120 s walk chunk then 420 s LNS chunk |
| new root when | no improvement for 1 200 s, or 3 600 s on one root |
| root source | the orbit workers' saved circuits, least-gates-first, each used once |
| harvest | `runs/o_polish.pop.jsonl`, states of ≤ 88 masks only |
| cross-pollination | **never set** (`pop_glob` absent; `hunt_worker.py` sets only `harvest_path`) |
| repulsion | off |
| rng | 2301, `+1` per chunk, `+101` per restart → restart 71 ran at seed 9841 |

Walk knobs (`WALK_KNOBS`): `hub_move_p 0.5   close_hamming 6
plateau_slack_p 0.35`.

LNS knobs (`LNS_KNOBS`):

```
op_mix {"small": 0.35, "coneinj": 0.45, "biginj": 0.20}
kmax 4   cone_lo 2   cone_hi 4   biginj_lo 8   biginj_hi 16
kshake 12   nsamp [12, 12]   hot_frac 0.5   vic_cost 3   peel_window 6
accept "sa"   sa_T0 1.2   sa_cool 0.9997   sa_reheat 4000
up_prob 0.35   up_slack 1   snapback 12
```

The record came out of the **first walk chunk** of restart 71 — 85.3 s in, before
any LNS chunk of that restart ran at all.
