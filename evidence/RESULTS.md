# Results that matter — 97@depth3, 92@depth4, 89@depth5, 88@depth7

Five verified AES-MixColumns 2-input-XOR circuits. Four of them are the best we
found at their depth; the fifth (88 @ depth 8, §5) is a same-size circuit from a
third distinct family — dominated by the 88 @ depth 7, so not a frontier point,
kept as a documented distinct construction. All five were re-verified
independently against MixColumns rebuilt from GF(2^8) (`../verify_circuit.py`);
none is claimed optimal (SLP minimization is NP-hard). For each: what it is,
where the circuit is, the exact code that produced it, and its **full lineage**
with the run-time and wall-clock at which every step appeared — back to a
from-scratch construction where there is one, and said plainly where there is
not (the 88 @ depth 8's seed chain passes through Jean's published circuit).

The project record improves 89 → 88. **87 was not found.**

Hash-pinned copies of the first three circuits (with listings, Verilog, and self-contained verifiers) live in the artifact repository, [aes-mixcolumns-xor-circuits](https://github.com/Joe-b-20/aes-mixcolumns-xor-circuits). All five circuits are in `circuits/`, with SHA-256 for each in
`circuits/spectrum.json`. Every run referenced below is archived untouched in
this folder, and each run archive contains a `code/` subfolder with the exact
code that produced it.

```
python3 ../verify_circuit.py circuits/mixcolumns_89gates_depth5.json 5   # etc.
python3 ../verify_circuit.py circuits/mixcolumns_88gates_depth7.json 7
```

Oracle output for all five at archiving time:

```
mixcolumns_97gates_depth3.json 3             gates=97 depth=3 outputs_built=32/32 VALID
mixcolumns_92gates_depth4.json 4             gates=92 depth=4 outputs_built=32/32 VALID
mixcolumns_89gates_depth5.json 5             gates=89 depth=5 outputs_built=32/32 VALID
mixcolumns_88gates_depth7.json 7             gates=88 depth=7 outputs_built=32/32 VALID
mixcolumns_88gates_depth8_thirdfamily.json 8 gates=88 depth=8 outputs_built=32/32 VALID
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
  gates: Osvik–Canright, ePrint 2024/1076, Appendix F) by five gates; the
  original 89-gate circuit needed depth 9–10. (Later literature check,
  2026-07-23: Sun–Yang–Li, ePrint 2025/1493, had 89 g-XOR at unstated depth
  since 2025-08, and Jean, ePrint 2026/1481, posted 88 at depth 7 after these
  runs; neither dominates 89 at depth 5 — see the artifact repository
  PRIOR_ART.md Corrections.)
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

## 4. 88 gates @ depth 7 — the new headline; ties the published record

- **What:** 88-gate depth-7 circuit — the first 88-gate circuit found by this
  project's own search, and the result that takes the project record from 89 to
  88 (87 was not found). It **matches the published record** (Jean, ePrint
  2026/1481, 88 gates; depth 7 is our measurement — the paper states no depth)
  **with an independent circuit**: the two share 61 of 88 masks (Jaccard
  0.530). It does **not** beat it. Jean's circuit, transcribed and
  oracle-verified, is archived and credited in
  `campaign87_imported_prior_art/`.
- **How:** the engine rebuilt during campaign 87 (level-BFS relax, incremental
  worklist closure, exact complete repair enumeration, victim repool, coneinj
  destroy, peel-before-accept, SA-with-reheat, plateau harvesting). Worker
  `w10_sym94` of a 10-worker hunt, `alt` mode (alternating walk and LNS
  chunks), rng 1010, walk drift, seeded with an exactly ρ²-symmetric 94 @
  depth 5. From that seed: 94 → 90@d5 at t = 2.2 s (it = 723), 90 → 89@d8 at
  t = 202.4 s (it = 58 504) and 89@d7 at t = 204.1 s, then **88 gates at
  t = 1 973.3 s (32.9 min), walk iteration 45 614** — at depth 11; the walk's
  Pareto depth tie-break carried the same size to **depth 7 5.3 s later**
  (t = 1 978.6 s, it = 47 436). The worker's remaining ~6 400 s found no 87.
- **Circuit:** `circuits/mixcolumns_88gates_depth7.json` (sha256
  `d87f6ed982518d93…`). Source of record:
  `campaign87_run_2026-07-26_got_88at7/BREAKTHROUGH_88gates_depth7.json`
  (identical mask set to that run's `w10_sym94_best.json` and its
  `ALERT_w10_sym94_88gates.json`).
- **Code that produced it:** `campaign87_run_2026-07-26_got_88at7/code/` — the
  merged `engines.py`, worker and launcher, with `CODE_PROVENANCE.md` and
  `CONFIG_AS_RUN.md`. The run was launched 2026-07-26 **21:35:25** on a budget
  of 8 400 s and shut down cleanly at 23:55:25; all ten workers shared one
  harvest directory.
- **Lineage** — this project's own; no imported circuit is in the chain:

  | step | circuit | how | when it appeared (run-time / wall) |
  |---|---|---|---|
  | root | **97 @ d3** | scratch (`anneal3`), no seed | 235 s / 07-13 14:02:25 |
  | ↓ | **89 @ d6** | 21 h ladder, rung d10 | 39 725 s (11.03 h) / 07-14 01:00:34 |
  | ↓ | **89 @ d5** | sub-89 run, one reroute (`uncapped_sub89`) | 592 s (0.16 h) / 07-14 14:26:31 |
  | ↓ | **94 @ d5, exactly ρ²-symmetric** | ρ²-symmetrize + orbit-peel + orbit-LNS of the trimmed 89@d5 — 41 size-2 orbits + 12 fixed masks, sharing 82/94 masks with the 89@d5; it costs only +5 over the record | 07-26 ~20:33 wall (file mtime; that run's log carries no timestamps) |
  | ↓ | **88 @ d7** | `merged-engine` worker `w10_sym94`, walk drift, it = 45 614 | **1 973 s (32.9 min) / 07-26 22:08:19** |

  The seed circuit is archived beside the record as
  `campaign87_run_2026-07-26_got_88at7/seed_rho2sym_94gates_depth5.json`
  (oracle-verified 94 @ depth 5).

- **Why no imported material is in this chain** — both points are checkable in
  the archived worker log:
  1. cross-pollination between workers is an **LNS-only** knob (`pop_glob`);
     `engine_walk` has no pool and only ever adds masks derived from its own
     value set's closure — and every improvement on this worker came from a
     walk chunk;
  2. the worker's 89@d7 (t = 204 s) predates its first cross-pollination event
     (t = 424.2 s), and no LNS chunk on this worker ever improved the best
     (every `[lns]` line ends `cur=91…98, best=89/88`).
- **How it sits relative to the other known circuits** (Jaccard on mask sets,
  all re-measured): 0.530 to Jean's 88 (61 shared, symdiff 54), 0.526 to
  Sun–Yang–Li's 89 (ePrint 2025/1493), 0.539 to our own 89@d5. The threshold
  used throughout the campaign is J ≥ 0.7 for "same family".

---

## 5. 88 gates @ depth 8 — a third distinct family, seeded through Jean's circuit

- **Read this first — provenance:** this circuit was found by our engine, but
  **its seed chain passes through Jean's published 88** (ePrint 2026/1481), so
  it is **not** an independent construction; it is a "derived from published
  work" result in the sense of [`METHODS.md`](../METHODS.md) §9. The seed was
  an exactly ρ²-symmetric 90 @ depth 9 built as a **union** of two symmetrized
  circuits, and one of the two came from Jean's circuit:

  ```
  union_A88.json   "union_of": ["symA_91g.json", "sym88_92g.json"]
  symA_91g.json  ← seed symlns_94gates_seed44.json (our ρ²-symmetric 94)  → 91
  sym88_92g.json ← seed IMPORTED_88.json (JEAN, ePrint 2026/1481),
                   "symmetrized+peeled: 53 orbits, 95 gates"              → 92
  union → 90 @ d9 (basin 1) at walk it = 10 336 → descended here to 88 @ d8
  ```

  The union files and the logs proving the chain are archived in
  `campaign87_certificates/rho2_symmetric_90s/`; the 90@d9 that seeded the run
  is byte-identical to that folder's
  `BEST_90gates_depth9_rho2symmetric.json` (sha256 `8642ae8702987dc4…`).
  The 88 @ depth 7 in §4 is the one with a clean own-lineage claim.
- **What:** an 88-gate depth-8 circuit, verified, and a **third distinct
  88-gate family**: Jaccard 0.455 to Jean's 88 (55 shared masks) and 0.544 to
  our own 88@d7 (62 shared) — both well below the 0.7 family threshold. It is
  **dominated by the 88 @ depth 7** (same size, greater depth), so it does not
  improve the frontier; it is documented because a genuinely third construction
  of the same size is the interesting object, not a new record.
- **How:** the wave-3 `hunt-deeper` fleet, 12 workers. Record worker
  `d3_orb90a`, `alt` mode, rng 3303, knobs `'{}'` — family repulsion and drift
  mode **off** for this worker (other workers of the fleet used them). From the
  90@d9 seed: 90@d5 at t = 189.4 s (it = 83 299), **89@d7 at t = 3 793.4 s
  (63 min, it = 75 097)**, 89@d6 at t = 4 548.4 s (76 min), then **88 gates at
  t = 7 452.8 s (124 min, it = 99 444)** at depth 10, depth-tiebroken to
  **depth 8 1.2 s later** (t = 7 454.0 s, it = 100 049). No 87 in the worker's
  remaining 2 h 11 min. Every improvement came from a **walk** chunk; the LNS
  chunks did cross-pollinate sibling masks but never improved the best.
- **Circuit:** `circuits/mixcolumns_88gates_depth8_thirdfamily.json` (sha256
  `e692dfc6a5a3eaa1…`). Source of record:
  `campaign87_run_2026-07-27_got_88at8_thirdfamily/BREAKTHROUGH_88gates_depth8_THIRDFAMILY.json`.
- **Code that produced it:**
  `campaign87_run_2026-07-27_got_88at8_thirdfamily/code/` — the merged engine
  plus knob-gated family repulsion, the drift-mode worker, census and launcher.
  The run was launched 2026-07-27 **00:57:08** on a budget of 15 300 s
  (4 h 15 min) and finished 05:12:08.
- **Lineage:**

  | step | circuit | how | provenance / when |
  |---|---|---|---|
  | a | 91 gates, ρ²-symmetric | orbit-walked from our own ρ²-symmetric 94 (§4) | ours |
  | b | 92 gates, ρ²-symmetric | **Jean's published 88** symmetrized + peeled to 95, orbit-walked to 92 | **published work, credited** |
  | ↓ | **90 @ d9, ρ²-symmetric** | union of a and b, orbit walk, it = 10 336 | derived |
  | ↓ | **88 @ d8** | `hunt-deeper` worker `d3_orb90a`, walk, it = 99 444 | **7 453 s (124 min) / 07-27 03:01:21**, depth-tiebroken to d8 at 03:01:22 |

---

## 6. Machine-checked certificates for the 88-gate plateau

No 87-gate circuit was found anywhere in the campaign, and a large amount of
compute went into deciding *neighbourhoods* of the known 88s exactly. The full
write-up, with the archived per-run verdict summaries, is in
[`campaign87_certificates/CERTIFICATES.md`](campaign87_certificates/CERTIFICATES.md).
The scope, stated exactly:

- **47 canonical 88-gate circuits have exhaustively empty k ≤ 3 shells** — all
  1 540 k=2 windows and all 27 720 k=3 windows for each, none reducible. Those
  47 are Jean's 88 (1) + its 12 syl-move plateau siblings (12) + the
  third-family anchor and its 33 representatives (34). Consequence: **any 87
  differs from each of those 47 by ≥ 4 masks.**
- **This project's own 88 @ depth 7 is *not* one of the 47.** Its exhaustive
  k ≤ 3 sweep was never run; what it has is 9 exact k=4 windows (all
  irreducible) and 8 windowed-SAT cone windows (5 UNSAT, 3 undecided, 0 SAT).
  "All our 88s" is not a claim this evidence supports.
- **Population sweeps:** 105 801 of the ≈ 139 878 known distinct 88-gate mask
  sets proven irreducible at k=2 — 51 899 of families 1–2 (61.1 %, closing the
  whole symdiff ≥ 55 band) plus **all 53 902 states of family 3 (100 %,
  closed)**.
- **≈ 165 M exact window decisions in total**, zero timeouts, zero reducible
  windows (exact-window ~113 k windows + exact-k4 ~16.8 M + pop-decider
  ~64.1 M + family3-exact ~84.0 M). The procedures were validated against an
  independent brute force: 25/25 and 12/12 at budgets 1–2, and 1 257 instances
  including 122 genuine NOs at budget 3, identically under CPython 3.10 and
  PyPy 3.11.
- **Windowed SAT is evidence, not proof:** UNSAT there is relative to the
  encoding's fixed slot order. 0 SAT anywhere; max-k UNSAT frontier k = 16 on
  Jean's 88 and k = 15 on the family-3 anchor (whose entire k ≤ 12 regime is
  UNSAT, 28/28). The undecided windows are undecided, not UNSAT.
- Nothing above bounds 87 away globally. Every exact result is merely
  consistent with 88 being locally rigid.

Also certificate-bearing, and archived in the same folder: two exactly
ρ²-symmetric **90-gate** circuits (depths 9 and 7, Jaccard 0.463 apart),
machine-certified locally optimal in orbit space under all remove-1-orbit and
all 666 remove-2-orbits-add-≤1 moves. They improve the best known exactly
symmetric circuit from 94 to 90. Both are **derived work**, not independent
results: basin 1 (depth 9) is the union of §5 — a 91 of our own lineage with a
92 symmetrized from Jean's published 88 — and basin 2 crosses that same 90 with
another 91 of ours, so it inherits the same status.

---

## Notes

- **Provenance in one line:** 97@d3 is genuinely from scratch; 92@d4 is from
  scratch too (down the cascade ladder); 89@d5 descends from a from-scratch 97 via
  the 21h ladder to 89@d6, then a one-gate-depth reroute — i.e. seeded on the
  project's own prior output, not an independent from-scratch discovery. 88@d7
  continues that same own-lineage chain through the ρ²-symmetric 94. 88@d8 is
  the one exception: **its seed chain passes through Jean's published 88**
  (§5), and it is labelled derived work everywhere it appears.
- **Not proven optimal.** Literature status (corrected 2026-07-23; full dated
  audit in the artifact repository PRIOR_ART.md, incl. its Corrections
  section): the published depth–count frontier is 99@3 (Shi–Feng–Xu, ToSC
  2023), 97@4 and 94@5 (Osvik–Canright, ePrint 2024/1076), 92@6 (Maximov),
  and 88@7 (Jean, ePrint 2026/1481), with 89 at unstated depth from
  Sun–Yang–Li (ePrint 2025/1493). Against that: **97@3, 92@4 and 89@5 improve
  the frontier** at their depths and remain on it (neither newer point
  dominates 89@5); **88@7 ties the published gate-count floor with an
  independent circuit** rather than lowering it; and **88@8 is dominated** by
  our own 88@7, so it is documented but is not a frontier point.
- **Nothing here beats 88.** The campaign that produced the two 88s searched
  for an 87 and did not find one, and the certificates in §6 bound only local
  neighbourhoods — they say nothing about whether an 87 exists.
- Every timestamp above is recoverable from the `coordinator.log` and per-worker
  `*.log` files in each run archive; every circuit from its `*_best.json`.
