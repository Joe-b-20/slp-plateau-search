# Configuration as run — worker `c_naive`

The worker was launched by the fleet supervisor with exactly this argument list
(`supervisor.py`, `hw("c_naive", "constructor:naive", 201, restart_s=7200,
stall_s=2400)`):

```
python3 hunt_worker.py --label c_naive --dir <hunt87> \
        --root constructor:naive --seed 201 --restart-s 7200 --stall-s 2400
```

Everything else is a `hunt_worker.py` default, and the first line of
`../runs_hunt/c_naive.log` echoes the effective configuration:

```
[     0.0s 22:22:27] hunt worker start: root=constructor:naive engines=alt
                     repel=False seed=201 restart=7200s stall=2400s
```

| setting | value | where from |
|---|---|---|
| depth cap | **none** (`cap=None`, uncapped hunt) | `WorkerCtx(args.label, None, out)` |
| mode | `alt` — walk chunk then LNS chunk, forever | `--engines` default |
| walk / LNS chunk | 120 s / 420 s | `--walk-chunk-s` / `--lns-chunk-s` defaults |
| new root when | no improvement for 2 400 s, or 7 200 s on one root | `--stall-s` / `--restart-s` |
| harvest | `runs/c_naive.pop.jsonl`, states of ≤ 88 masks only | `--harvest-max` default 88 |
| cross-pollination | **never set** (`pop_glob` absent) | `hunt_worker.py` sets only `harvest_path` |
| repulsion | off | `--repel` not passed |
| rng | 201, `+1` per chunk, `+101` per restart | `--seed`, restart loop |

Walk knobs (`WALK_KNOBS`):

```
hub_move_p 0.5   close_hamming 6   plateau_slack_p 0.35
```

LNS knobs (`LNS_KNOBS`, the campaign's measured-good `champ_fast` values plus the
wave-3 operator mix):

```
op_mix {"small": 0.35, "coneinj": 0.45, "biginj": 0.20}
kmax 4   cone_lo 2   cone_hi 4   biginj_lo 8   biginj_hi 16
kshake 12   nsamp [12, 12]   hot_frac 0.5   vic_cost 3   peel_window 6
accept "sa"   sa_T0 1.2   sa_cool 0.9997   sa_reheat 4000
up_prob 0.35   up_slack 1   snapback 12
```

Both 88-gate states of this record came out of a **walk** chunk, as did the 89.
One LNS chunk of restart 18 did improve the best (the `[lns]` line at 16:48:24,
`best=90`, up from 92); the other nine end `best=89` or `best=88` unchanged. With
`pop_glob` unset, an LNS rebuild pool holds only that worker's own masks, their
pairwise sums and its own accumulated hot list.

The record's own restart is restart 18, opened at t = 66 009.5 s with rng seed
2163 (`--- restart 18 from naive#2163 (139g d3) (rng seed 2163) ---`). The chunk
that found it is the walk chunk beginning at t ≈ 68 200 s.
