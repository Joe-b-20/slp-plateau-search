# Configuration as run — worker `c_naive`, session 5

Identical to the configuration that produced the 88 @ depth 6 two days earlier —
same worker, same command line, same defaults. The fleet supervisor launched it
with exactly this argument list (`supervisor.py`,
`hw("c_naive", "constructor:naive", 201, restart_s=7200, stall_s=2400)`):

```
python3 hunt_worker.py --label c_naive --dir <hunt87> \
        --root constructor:naive --seed 201 --restart-s 7200 --stall-s 2400
```

Everything else is a `hunt_worker.py` default. The first line of session 5 in
`../runs_hunt/c_naive.log` echoes the effective configuration:

```
[     0.0s 15:35:00] hunt worker start: root=constructor:naive engines=alt
                     repel=False seed=201 restart=7200s stall=2400s
```

That line is 2026-07-29 15:35:00, and it is **already present in the copy of this
log published with the 88 @ depth 6 in v3.0.0** — see `../PROVENANCE.md`
corroboration (b).

| setting | value | where from |
|---|---|---|
| depth cap | **none** (`cap=None`, uncapped hunt) | `WorkerCtx(args.label, None, out)` |
| mode | `alt` — walk chunk then LNS chunk, forever | `--engines` default |
| walk / LNS chunk | 120 s / 420 s | `--walk-chunk-s` / `--lns-chunk-s` defaults |
| new root when | no improvement for 2 400 s, or 7 200 s on one root | `--stall-s` / `--restart-s` |
| harvest | `runs/c_naive.pop.jsonl`, states of ≤ 88 masks only | `--harvest-max` default 88 |
| cross-pollination | **unreachable in this fleet** (`pop_glob` is written only by `worker.py:wire_harvest`, which `hunt_worker.py` never calls and `supervisor.py` never launches) | `../PROVENANCE.md` vector 1 |
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

Both 88-gate states of this record came out of a **walk** chunk — the chunk that
closes with `[walk] 75s iters=40000 cur=88 best=88` at 10:48:24. `engine_walk`
has no candidate pool and no disk read path; it only adds masks derived from its
own value set's closure. Restart 16's LNS chunks improved the local best on the
way down (93 → 91, 90 → 89) but never produced an 88, and with `pop_glob`
unreachable an LNS rebuild pool holds only that worker's own masks, their
pairwise sums and its own accumulated hot list.

The record's own restart is **session 5, restart 16**, opened at t = 65 349.0 s
with rng seed 1958
(`--- restart 16 from naive#1958 (146g d3) (rng seed 1958) ---`). Quote the
session number: the log holds five sessions and 58 restarts, and each session's
run-time clock restarts at 0.
