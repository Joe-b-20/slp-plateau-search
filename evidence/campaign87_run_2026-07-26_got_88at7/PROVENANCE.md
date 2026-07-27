# Provenance — campaign-87 merged-engine hunt (2026-07-26, produced 88 @ depth 7)

The run that produced **88 gates @ depth 7**, the first 88-gate circuit found by
this project's own search. It matches the published world record (Jean, ePrint
2026/1481, 88@7) with a **different circuit** — the two share 61 of 88 masks
(Jaccard 0.530). It does not beat the published record.

This directory is the untouched archive of the run's small artifacts plus a
`code/` folder with the exact code that produced them. The multi-hundred-MB
plateau population files are **not** in the repo; they are listed by path, size
and SHA-256 below.

## The run

| | |
|---|---|
| what | campaign-87 wave-2 "merged engine" long hunt, 10 workers, one shared harvest directory (cross-pollination between LNS workers) |
| launched | 2026-07-26 **21:35:25**, budget 8 400 s (2 h 20 min), clean shutdown 23:55:25 |
| launcher | `code/launch_hunt.sh 8400` (verbatim as run) |
| engine | `code/engines.py` — the merged engine (all seven wave-1 improvements integrated) |
| record worker | **`w10_sym94`** — `alt` mode (alternating 300 s walk chunks and 600 s LNS chunks), rng 1010, seed = the ρ²-symmetric 94@5 (`seed_rho2sym_94gates_depth5.json`) |
| the record | `BREAKTHROUGH_88gates_depth7.json` (= `runs_hunt/w10_sym94_best.json` = `runs_hunt/ALERT_w10_sym94_88gates.json`; identical mask sets) |

## How the 88 appeared (verbatim from `runs_hunt/w10_sym94.log`)

```
[     0.0s 21:35:25] hunt worker start: engine=alt seed=symlns_94gates_seed44.json rng=1010 total=8400s
[     2.2s 21:35:28]   NEW BEST 90 gates depth 5 VERIFIED depth-tiebreak it=723
[   202.4s 21:38:48]   NEW BEST 89 gates depth 8 VERIFIED it=58504
[   204.1s 21:38:50]   NEW BEST 89 gates depth 7 VERIFIED depth-tiebreak it=58795
[  1973.3s 22:08:19]   NEW BEST 88 gates depth 11 VERIFIED it=45614
[  1978.6s 22:08:24]   NEW BEST 88 gates depth 7 VERIFIED depth-tiebreak it=47436
[  8400.0s 23:55:25] hunt worker done: best=88@7 iters(last chunk)=151040
```

94 → 90@5 in 2.2 s, 90 → 89@7 in 3.4 min, 89 → 88 at **t = 1 973 s (32.9 min)**,
walk iteration 45 614 of that chunk; the walk's Pareto depth tie-break then took
the same-size circuit from depth 11 to **depth 7 in 5.3 s** (it = 47 436). The
remaining 6 400 s of the worker never found an 87.

## Lineage of the 88@7 — this project's own, no imported circuit in the chain

| step | circuit | how | when |
|---|---|---|---|
| root | 97 @ d3 | `anneal3`, **from scratch** (no seed) | 2026-07-13, `../parallel_ladder_run_2026-07-13/` |
| ↓ | 89 @ d5 | the 21 h ladder → 89@d6, then one reroute in the sub-89 run | 2026-07-14, `../sub89_run_2026-07-14_got_89at5/` |
| ↓ | **94 @ d5, exactly ρ²-symmetric** | ρ²-symmetrize + orbit-peel + orbit-LNS of the trimmed 89@5 (campaign-87 `structure-algebra` agent; 41 size-2 orbits + 12 fixed masks; shares 82/94 masks with the 89@5) | 2026-07-26, `seed_rho2sym_94gates_depth5.json` |
| ↓ | **88 @ d7** | worker `w10_sym94` walk drift, it = 45 614 | 2026-07-26 22:08 |

**No material from Jean's published 88 (or Sun–Yang–Li's 89) is in this chain.**
The worker ran in `alt` mode, so its LNS chunks did cross-pollinate masks from
sibling workers (five of which were seeded on Jean's 88). That path is closed for
this record for two independent reasons, both checkable in the log:

1. cross-pollination is an **LNS-only** knob (`pop_glob`); `engine_walk` has no
   pool and only ever adds masks derived from its own value set's closure
   (`code/engines.py`, `engine_lns` vs `engine_walk`), and every improvement on
   this worker came from a walk chunk;
2. the worker's 89@7 (t = 204 s) predates the first cross-pollination event
   (t = 424 s), and **no LNS chunk on this worker ever improved the best** — every
   `[lns]` line ends at `cur=91…98, best=89/88`. The 88 descends from the walk's
   own 89.

## What is in this archive

- `BREAKTHROUGH_88gates_depth7.json` — the record, exactly as the run saved it.
  Canonical copy: `../circuits/mixcolumns_88gates_depth7.json` (sha256 in
  `../circuits/spectrum.json`).
- `seed_rho2sym_94gates_depth5.json` — the ρ²-symmetric 94 seed (verified).
- `runs_hunt/` — every worker's `.log`, `_best.json`, `_status.json`,
  `ALERT_*.json` and the mid-hunt reseed circuit `distant88_seed.json`.
  **Untouched.**
- `portfolio88/` — the run's 8 maximally-diverse verified 88s + manifest
  (k-centre picks over the harvest; J to Jean 0.517–0.796).
- `REPORT.md` — the agent's own report on the merge and the hunt (copied
  verbatim; its numbers are the source for `../../campaign_87/FACTS.md`).
- `code/` — the exact engine and worker scripts, with `CODE_PROVENANCE.md`
  and `CONFIG_AS_RUN.md`.

## What is NOT in this archive (campaign archive, not in repo)

The harvested plateau populations are far too large for the repository. They live
in the gitignored campaign folder:

| file | size | sha256 | lines |
|---|---|---|---|
| `campaign_87/agents/merged-engine/runs_hunt/w10_sym94.pop.jsonl` | 62 779 694 B (60 MB) | `dab6b554573fd9b360e982a2a3060910ff678b29e69adf66ce9b30463976e59b` | 67 380 |
| `campaign_87/agents/merged-engine/runs_hunt/*.pop.jsonl` (all 10 workers) | 639 541 881 B total (610 MB) | — | 690 850 raw lines → **84 989 distinct verified 88-gate mask sets** |

Those populations are what the exact-certificate agents swept; their verdict
summaries are archived in `../campaign87_certificates/`.

## Re-verify

```
python3 ../../verify_circuit.py BREAKTHROUGH_88gates_depth7.json 7
python3 ../../verify_circuit.py seed_rho2sym_94gates_depth5.json 5
```

Outputs at the time of archiving:

```
gates=88 depth=7 outputs_built=32/32 problems=0 ; depth<= 7: OK ; VERDICT: VALID MixColumns circuit
gates=94 depth=5 outputs_built=32/32 problems=0 ; depth<= 5: OK ; VERDICT: VALID MixColumns circuit
```

All 36 circuit JSONs in this directory (record, seed, per-worker bests, alerts,
portfolio) were re-verified against the oracle: **all VALID**.
