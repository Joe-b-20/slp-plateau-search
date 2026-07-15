# Results that matter — 97@depth3, 92@depth4, 89@depth5

Three verified AES-MixColumns 2-input-XOR circuits, each the best we found at its
depth. All three were re-verified independently against MixColumns rebuilt from
GF(2^8) (`../verify_circuit.py`); none is claimed optimal (SLP minimization is
NP-hard). For each: what it is, where the circuit is, the exact code that
produced it, and its **full lineage back to a from-scratch construction** with
the run-time and wall-clock at which every step appeared.

The canonical, hash-pinned copies of the record circuits (with listings, Verilog, and self-contained verifiers) live in the artifact repository, [aes-mixcolumns-xor-circuits](https://github.com/Joe-b-20/aes-mixcolumns-xor-circuits). The three circuits are in `circuits/` (one file per depth, with SHA-256 in
`circuits/spectrum.json`). Every run referenced below is archived untouched in
this folder, and each run archive contains a `code/` subfolder with the exact
pipeline code that produced it.

```
python3 ../verify_circuit.py circuits/mixcolumns_89gates_depth5.json 5   # etc.
```

---

## 1. 97 gates @ depth 3 — the from-scratch root

- **What:** 97-gate depth-3 circuit. Beats the published 99 (Shi–Feng–Xu, ToSC
  2023) and this project's earlier 98.
- **How:** the `anneal3` engine — simulated annealing + iterated local search over
  a model of shared depth-1 pairs / depth-2 parts. **Pure from scratch:** targets
  computed from GF(2^8), no seed. This is the root that every other result
  ultimately descends from.
- **Circuit:** `circuits/mixcolumns_97gates_depth3.json` (sha256 `d7289a99cad19573…`).
  Source of record: `parallel_ladder_run_2026-07-13/d3_best.json`.
- **Code that produced it:** `parallel_ladder_run_2026-07-13/code/` (`engines.py` →
  `engine_anneal3`). Also reproducible standalone: `../reproduce/reproduce.py`
  reaches 97 from scratch in pure Python (~1–3 min).
- **Lineage:** none — it is from scratch.
- **Appeared:** in the 21h ladder run at **t = 235 s (0.07 h), 2026-07-13 14:02:25**.
  (Independently reproduced from scratch by the cascade run's own d3 rung at
  t = 267 s, 2026-07-14 15:04:59 — so this depth-3 result is reproducible cold.)

---

## 2. 92 gates @ depth 4 — from scratch, down the depth ladder

- **What:** 92-gate depth-4 circuit. Beats the published depth-4 point (97 gates:
  Osvik–Canright, ePrint 2024/1076, Appendix G) by five gates.
- **How:** the `lns` engine (destroy-and-rebuild). In the **from-scratch cascade
  run** (2026-07-14, the run with the Pareto tie-break + reseeding), the depth-8
  worker `d8` — searching with slack under its loose cap — landed on a circuit that
  is only depth 4; the Pareto tie-break kept it and reseeding copied it to the
  depth-4 rung. The whole chain is rooted in that run's own from-scratch 97.
- **Circuit:** `circuits/mixcolumns_92gates_depth4.json` (sha256 `3615c132cae7e4fb…`).
  Source of record: `cascade_run_2026-07-14_from_scratch_newlogic/d4_best.json`
  (found by `d8`, held by `d4` via reseeding).
- **Code that produced it:** `cascade_run_2026-07-14_from_scratch_newlogic/code/`.
- **Lineage** (all in the cascade run, rooted in from scratch; each rung was
  seeded from the previous rung's best at its trigger — the `seed_from_dN.json`
  files in that archive):

  | step | circuit | rung | seeded from | when it appeared (run-time / wall 2026-07-14) |
  |---|---|---|---|---|
  | root | **97 @ d3** | d3 | scratch (`anneal3`) | 267 s / 15:04:59 |
  | ↓ | 96 @ d4 | d4 | 97@d3 | 7 299 s / 17:02:11 |
  | ↓ | 95 @ d4 | d5 | 96@d4 | 7 899 s / 17:12:10 |
  | ↓ | 94 @ d5 | d6 | 95@d4 | 7 990 s / 17:13:42 |
  | ↓ | 93 @ d5 | d7 | 94@d5 | 8 210 s / 17:17:21 |
  | ↓ | **92 @ d4** | d8 | 93@d5 | **9 610 s (2.67 h) / 17:40:41** |

---

## 3. 89 gates @ depth 5 — the headline; lineage spans two runs

- **What:** 89-gate depth-5 circuit. The fewest gates we know (89), at the
  shallowest depth we've reached them (5). Beats the published depth-5 point (94
  gates: Osvik–Canright, ePrint 2024/1076, Appendix F) by five gates and the
  smallest published count at any depth (91, Lin et al., CT-RSA 2021, s-XOR)
  by two; the original 89-gate circuit needed depth 9–10.
- **How:** the `lns` engine. In the **sub-89 run** the `uncapped_sub89` worker was
  seeded with the 89@depth6 circuit and, one reroute later, found an equal-gate
  circuit at **depth 5**. The log line is `NEW BEST 89 gates depth 5 VERIFIED
  depth-tiebreak` — it survived only because of the two fixes (Pareto tie-break:
  accept equal gates at lower depth; and the engines surfacing such candidates).
  It shares 84/89 internal masks with its 89@depth6 parent — a genuine ~5-gate
  reroute that shed one depth level.
- **Circuit:** `circuits/mixcolumns_89gates_depth5.json` (sha256 `209f74d5717112f8…`).
  Source of record: `sub89_run_2026-07-14_got_89at5/best_overall.json`
  (= `…/RECORD_89_at_depth5.json`).
- **Code that produced it:** `sub89_run_2026-07-14_got_89at5/code/` (the pipeline
  carrying the Pareto tie-break + reseeding — the fixes that made 89@5 catchable).
  Its parent 89@6 was produced by the older code in
  `parallel_ladder_run_2026-07-13/code/`.
- **Lineage** — rooted in the 21h run's from-scratch 97, laddered down to 89@d6,
  then one reroute to 89@d5 in the sub-89 run:

  | step | circuit | run / rung | seeded from | when it appeared (run-time / wall) |
  |---|---|---|---|---|
  | root | **97 @ d3** | 21h / d3 | scratch (`anneal3`) | 235 s / 07-13 14:02:25 |
  | ↓ | 96 @ d4 | 21h / d4 | 97@d3 | 11 594 s / 07-13 17:11:43 |
  | ↓ | 95 @ d5 | 21h / d5 | 96@d4 | 11 731 s / 07-13 17:14:01 |
  | ↓ | 94 @ d4 | 21h / d6 | 95@d5 | 11 907 s / 07-13 17:16:57 |
  | ↓ | 93 @ d7 | 21h / d7 | 94@d4 | 12 709 s / 07-13 17:30:19 |
  | ↓ | 92 @ d7 | 21h / d8 | 93@d7 | 16 980 s / 07-13 18:41:29 |
  | ↓ | 92 @ d7 | 21h / d9 | 92@d7 | 24 181 s / 07-13 20:41:31 |
  | ↓ | **89 @ d6** | 21h / d10 | 92@d7 | **39 725 s (11.03 h) / 07-14 01:00:34** |
  | ↓ | **89 @ d5** | sub-89 / uncapped_sub89 | 89@d6 (d10's circuit) | **592 s (0.16 h) / 07-14 14:26:31** |

  (Within d10 the descent was 92@d7 → 91@d5 @ 27 038 s → 90@d5 @ 27 378 s → 89@d6
  @ 39 725 s. The 89@d6 parent circuit is
  `parallel_ladder_run_2026-07-13/d10_best.json`.)

---

## Notes

- **Provenance in one line:** 97@d3 is genuinely from scratch; 92@d4 is from
  scratch too (down the cascade ladder); 89@d5 descends from a from-scratch 97 via
  the 21h ladder to 89@d6, then a one-gate-depth reroute — i.e. seeded on the
  project's own prior output, not an independent from-scratch discovery.
- **Not proven optimal.** Literature check completed 2026-07-15: the published
  depth–count frontier is 99@3 (Shi–Feng–Xu, ToSC 2023), 97@4 and 94@5
  (Osvik–Canright, ePrint 2024/1076), 92@6 (Maximov), 91@7 (Lin et al., CT-RSA
  2021, s-XOR); the three circuits above improve it at every depth from 3 to 5
  and 89@5 dominates the deeper points. Full audit: PRIOR_ART.md in the
  artifact repository.
- Every timestamp above is recoverable from the `coordinator.log` and per-worker
  `*.log` files in each run archive; every circuit from its `*_best.json`.
