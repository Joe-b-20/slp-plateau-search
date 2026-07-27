# Provenance — campaign-87 hunt-deeper run (2026-07-27, produced 88 @ depth 8)

The run that produced **88 gates @ depth 8**, a third distinct 88-gate family
(Jaccard 0.455 to Jean's published 88, 0.544 to this project's 88@7). It does
**not** improve the frontier — it is dominated by our own 88@7 — and is kept as a
documented distinct construction.

## Read this first: the lineage passes through Jean's published 88

The seed of this descent is orbit-ladder's ρ²-symmetric **90 @ depth 9**
(`seed_rho2sym_90gates_depth9_basin1.json`, "basin 1"). That 90 was produced by a
**union of two symmetrized circuits**, and one of them is derived from Jean's
circuit:

```
campaign_87/agents/orbit-ladder/work/union_A88.json
    "union_of": ["symA_91g.json", "sym88_92g.json"]

symA_91g.json  ← symA.log:  "seed symlns_94gates_seed44.json: 94 masks"
                            (our ρ²-symmetric 94, own lineage) → 91 gates
sym88_92g.json ← sym88.log: "seed IMPORTED_88.json: 88 masks"
                            "symmetrized+peeled: 53 orbits, 95 gates" → 92 gates
                            (IMPORTED_88.json = Jean, ePrint 2026/1481)
```

and `work/uA88_90g.json` — the 90@9 that seeded this run — is byte-identical to
`BEST_90gates_depth9_rho2symmetric.json` (sha256
`8642ae8702987dc4…`), produced from `union_A88.json` at walk it = 10 336.

**So: the 88@8 is NOT an independent from-scratch construction. Its ancestry
contains masks derived from Jean's published 88** (via symmetrisation, union,
peeling and 25 000+ orbit-walk moves). This is a "derived from published work"
lineage in the sense of METHODS.md §9, and must always be stated as such.
The 88@7 in `../campaign87_run_2026-07-26_got_88at7/` is the one with a clean
own-lineage claim; the two are different circuits with different provenance.

(The relevant orbit-ladder logs and union files are archived in
`../campaign87_certificates/rho2_symmetric_90s/` so the chain above can be
re-checked without the campaign folder.)

## The run

| | |
|---|---|
| what | campaign-87 wave-3 "hunt-deeper" fleet, 12 workers, shared harvest directory |
| launched | 2026-07-27 **00:57:08**, budget 15 300 s (4 h 15 min), finished 05:12:08 |
| launcher | `code/launch_hunt.sh 15300` (verbatim as run) |
| engine | `code/engines.py` — the merged engine plus knob-gated family repulsion; `code/hunt_worker.py` adds drift-mode reseeding |
| record worker | **`d3_orb90a`** — `alt` mode, rng 3303, knobs `'{}'` (**no repulsion, no drift mode**), seed = the ρ²-symmetric 90@9 |
| the record | `BREAKTHROUGH_88gates_depth8_THIRDFAMILY.json` (= `runs_hunt/d3_orb90a_best.json` = `runs_hunt/ALERT_d3_orb90a_88gates.json`; identical mask sets) |

## The descent (verbatim from `runs_hunt/d3_orb90a.log`)

```
[     0.0s 00:57:08] hunt worker start: engine=alt seed=BEST_90gates_depth9_rho2symmetric.json rng=3303 total=15300s
[   189.4s 01:00:17]   NEW BEST 90 gates depth 5 VERIFIED depth-tiebreak it=83299
[  3793.4s 02:00:21]   NEW BEST 89 gates depth 7 VERIFIED it=75097
[  4548.4s 02:12:56]   NEW BEST 89 gates depth 6 VERIFIED depth-tiebreak it=17640
[  7452.8s 03:01:21]   NEW BEST 88 gates depth 10 VERIFIED it=99444
[  7454.0s 03:01:22]   NEW BEST 88 gates depth 8 VERIFIED depth-tiebreak it=100049
[ 15300.1s 05:12:08] hunt worker done: best=88@8 iters(last chunk)=39653
```

90@9 → 90@5 in 3.2 min; 90 → 89@7 at **t = 3 793 s (63 min)**; 89@7 → 89@6 at
t = 4 548 s (76 min); 89 → 88 at **t = 7 453 s (124 min)**, walk iteration 99 444,
depth-tiebroken to depth 8 within 1.2 s. The remaining 2 h 11 min of the worker
found no 87.

Every improvement on this worker came from a **walk** chunk. The LNS chunks did
cross-pollinate sibling masks (`[lns] cross-pollinated …` lines) but never
improved the best — every `[lns]` line ends `cur=91…98, best=90/89/88`. The walk
engine has no pool and does not read sibling harvests.

## What is in this archive

- `BREAKTHROUGH_88gates_depth8_THIRDFAMILY.json` — the record, exactly as saved.
  Canonical copy: `../circuits/mixcolumns_88gates_depth8_thirdfamily.json`.
- `seed_rho2sym_90gates_depth9_basin1.json` — the seed (verified 90@9).
- `runs_hunt/` — every worker's `.log`, `_best.json`, `_status.json`,
  `ALERT_*.json` and the mid-run reseed circuits (`remote_seed_[ab].json`,
  `frontier88_seed.json`, `n3edge_seed.json`). **Untouched.**
- `newfamily_reps/` — the 25 early third-family representatives the online census
  saved (`NEWFAMILY_88_00..24_*.json`), all verified 88s.
- `portfolio_family3/` — 8 k-centre-diverse third-family reps + manifest.
- `family_refs.json` — the three family anchor mask sets (jean / new88 / orb88)
  used by the census; `repel_masks.json` — the 57-mask family core used by the
  *other* (repulsion) workers of this fleet.
- `REPORT.md` — the agent's own report (verbatim).
- `code/` — the exact engine, worker, census and launcher, with
  `CODE_PROVENANCE.md` and `CONFIG_AS_RUN.md`.

## What is NOT in this archive (campaign archive, not in repo)

| file | size | sha256 | lines |
|---|---|---|---|
| `campaign_87/agents/hunt-deeper/runs_hunt/d3_orb90a.pop.jsonl` | 169 241 720 B (161 MB) | `b37f8fb2bde3d73bcb034658451fdff7fd0570016a0fe98a17858aa30fdb5f0f` | 179 950 |
| `campaign_87/agents/hunt-deeper/population88_new.jsonl` | 50 678 244 B (48 MB) | `a1f67ab4fe733031ede68147e556d162e4e3c36190436ee2a969debe4c01029d` | **54 889 distinct new 88-gate mask sets** (53 902 of them third-family) |
| `campaign_87/agents/hunt-deeper/runs_hunt/*.pop.jsonl` (all 12 workers) | 1 526 810 645 B total (1.4 GB) | — | raw harvest |
| `campaign_87/agents/hunt-deeper/census/` | 9.3 MB | — | dedupe state of the online census |

`population88_new.jsonl` is the file `family3-exact` swept exhaustively at k = 2
(all 53 902 family-3 states, all irreducible); its verdict summaries are in
`../campaign87_certificates/family3_exact/`.

## Re-verify

```
python3 ../../verify_circuit.py BREAKTHROUGH_88gates_depth8_THIRDFAMILY.json 8
python3 ../../verify_circuit.py seed_rho2sym_90gates_depth9_basin1.json 9
```

Outputs at the time of archiving:

```
gates=88 depth=8 outputs_built=32/32 problems=0 ; depth<= 8: OK ; VERDICT: VALID MixColumns circuit
gates=90 depth=9 outputs_built=32/32 problems=0 ; depth<= 9: OK ; VERDICT: VALID MixColumns circuit
```

All 64 circuit JSONs in this directory (record, seed, per-worker bests, alerts,
reseed points, 25 census reps, 8 portfolio reps) were re-verified against the
oracle: **all VALID**.
