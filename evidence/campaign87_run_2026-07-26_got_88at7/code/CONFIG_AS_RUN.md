# Config as run — campaign-87 merged-engine hunt (2026-07-26)

Launched exactly as `./launch_hunt.sh 8400` from the agent's `work/` directory
(`launch_hunt.sh` is archived here verbatim), i.e. 10 workers × 8 400 s writing
into one shared harvest directory `runs_hunt/`.

The record worker:

```
python3 hunt_worker.py w10_sym94 alt \
    ../../structure-algebra/symlns_94gates_seed44.json \
    ../runs_hunt 1010 8400 '{}'
```

`'{}'` = default knobs, i.e. exactly the values logged on the worker's first
line:

```
lns  = {'kmax': 4, 'kshake': 12, 'snapback': 12, 'nsamp': (12, 12),
        'up_prob': 0.5, 'up_slack': 4,
        'harvest_path': '../runs_hunt/w10_sym94.pop.jsonl',
        'pop_glob': '../runs_hunt/*.pop.jsonl', 'pop_period_s': 120.0}
walk = {'hub_move_p': 0.3, 'close_hamming': 8, 'repair_one': 40,
        'repair_hub': 24, 'plateau_slack_p': 0.15,
        'harvest_path': '../runs_hunt/w10_sym94.pop.jsonl'}
```

Defaults inside `engines.py` that these do not override: `op_mix`
{small 0.35, coneinj 0.45, biginj 0.20}, `vic_cost` 3, `hot_frac` 0.5,
SA acceptance (`sa_T0` 1.2, `sa_cool` 0.9997, `sa_reheat` 4000),
`peel_window` 6, `cone_lo/hi` 2/4, `biginj_lo/hi` 8/16.

`alt` mode: chunk 0, 2, 4 … = 300 s `walk`; chunk 1, 3, 5 … = 600 s `lns`; each
chunk reseeds from the worker's own Pareto best and bumps the rng by one.
Depth cap `None` throughout (uncapped); stop target 87 (never reached).

The other nine workers of the same launch are listed in `launch_hunt.sh`; five
were seeded on the imported Jean 88, one on the imported Sun–Yang–Li 89, three on
portfolio circuits. Their logs are in `../runs_hunt/`; the mid-hunt reseeds
(w2, w6, w7, w8, w9) and where each track ended are summarised in
`../PROVENANCE.md`.
