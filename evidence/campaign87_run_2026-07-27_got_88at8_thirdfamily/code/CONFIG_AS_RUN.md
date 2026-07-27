# Config as run — campaign-87 hunt-deeper fleet (2026-07-27)

Launched exactly as `./launch_hunt.sh 15300` from the agent's `work/` directory
(`launch_hunt.sh` archived here verbatim): 12 workers × 15 300 s into one shared
harvest directory `runs_hunt/`, in three tracks — D (continue the young,
never-converged basins, 5 workers, plain knobs), P (third-family prospecting with
repulsion from both known 88 families, 6 workers), F (push the distant-88
frontier, 1 worker, soft repulsion).

The record worker (track D, plain knobs):

```
python3 hunt_worker.py d3_orb90a alt \
    ../../orbit-ladder/BEST_90gates_depth9_rho2symmetric.json \
    ../runs_hunt 3303 15300 '{}'
```

`'{}'` = default knobs, exactly as logged on the worker's first line:

```
lns  = {'kmax': 4, 'kshake': 12, 'snapback': 12, 'nsamp': (12, 12),
        'up_prob': 0.5, 'up_slack': 4,
        'harvest_path': '../runs_hunt/d3_orb90a.pop.jsonl',
        'pop_glob': '../runs_hunt/*.pop.jsonl', 'pop_period_s': 120.0}
walk = {'hub_move_p': 0.3, 'close_hamming': 8, 'repair_one': 40,
        'repair_hub': 24, 'plateau_slack_p': 0.15,
        'harvest_path': '../runs_hunt/d3_orb90a.pop.jsonl'}
```

No `repel_file`, no `drift_refs` → **family repulsion and drift mode were OFF for
this worker**. `alt` mode as before: 300 s walk chunks alternating with 600 s LNS
chunks, each chunk reseeded from the worker's own Pareto best with the rng bumped
by one. Depth cap `None`; stop target 87 (never reached).

The repulsion configuration used by the other workers (for reference, from
`launch_hunt.sh`):

```
REPEL     = {"lns": {"repel_file": "../repel_masks.json", "repel_pen": 2, "repel_up_p": 0.25},
             "walk": {"repel_file": "../repel_masks.json", "repel_up_p": 0.25}}
REPELSOFT = {"lns": {"repel_file": "../repel_masks.json", "repel_pen": 1, "repel_up_p": 0.4},
             "walk": {"repel_file": "../repel_masks.json", "repel_up_p": 0.4}}
```

`repel_masks.json` (archived one level up) is the 57-mask "family core": the
union of both then-known 88 anchors plus masks present in ≥ 30 % of the wave-2
88-harvest, minus targets and weight-2 masks.
