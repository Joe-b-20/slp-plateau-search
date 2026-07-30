# Verified results and their lineage — 97@depth3, 92@depth4, 89@depth5, 88@depth5 (×2), 88@depth6/7/8

Eight verified AES-MixColumns 2-input-XOR circuits, at gate counts 97, 92, 89 and
88 (five times: twice at depth 5, and once each at depths 6, 7 and 8). One
frontier comes out of them:

> **Verified frontier: 97 @ 3, 92 @ 4, 88 @ 5 — one line, entirely this
> project's own lineage, with no imported material.**

**87 was not found**, and none of the eight is claimed optimal (SLP minimization
is NP-hard).

**Provenance up front.** 88 is the published best-known gate count, held by Jean
(ePrint 2026/1481, posted 2026-07-23) — **Jean has priority and nothing here
beats it.** Of our five 88s: the from-scratch **88 @ depth 5** (§7) is the
frontier point, found by a search rooted in a randomized XOR tree over the 32 raw
inputs; the 88 @ depth 7 (§4) **matches** that count with an independent circuit;
the 88 @ depth 6 (§6) is another distinct family found **from scratch**; and the
88 @ depth 8 (§5) and the derived 88 @ depth 5 (§8) both have seed chains that
pass through Jean's published circuit, so both are reported as derived work and
say so in their first sentence. Everything else here is this project's own
lineage, rooted in a from-scratch construction.

**What the frontier statement claims, and what it does not.** Until 2026-07-30
the (88, depth 5) point was held only by the derived circuit of §8, so this
repository published two frontiers — an own-lineage one and a combined one that
depended on Jean's circuit. §7 collapses them into one. **This is a statement
about our provenance, not about his result:** the count is still Jean's, the
priority is still Jean's, and the change is that *we* no longer need his circuit
to reach depth 5. "No imported material" means that no circuit file, no published
mask set and no other worker's harvested mask entered that search process — the
root is a pure function of an integer seed and the producing engine reads nothing
from disk. It does **not** claim method independence (the engines and knobs were
tuned over a campaign that did read published circuits), disjointness (§7 shares
42 of 88 masks with Jean's, 32 of them the forced targets), landscape
independence, optimality, any bound on 87, or bit-reproducibility of the descent.

Each section below gives what the circuit is, where it is, the exact code that
produced it, and its **full lineage** with the run-time and wall-clock at which
every step appeared. All eight were re-verified against MixColumns rebuilt from
GF(2^8) (`../verify_circuit.py`), live in `circuits/` with SHA-256 in
`circuits/spectrum.json`, and are hash-pinned in the artifact repository
[aes-mixcolumns-xor-circuits](https://github.com/Joe-b-20/aes-mixcolumns-xor-circuits)
with listings, Verilog and self-contained verifiers (the 88 @ depth 8 ships
there as `mixcolumns_88gates_depth8.json`, labelled derived and non-frontier).
Every run referenced below is archived untouched in this folder, each with a
`code/` subfolder holding — or hash-pinning — the exact code that produced it.

```
python3 ../verify_circuit.py circuits/mixcolumns_89gates_depth5.json 5   # etc.
python3 ../verify_circuit.py circuits/mixcolumns_88gates_depth5_fromscratch.json 5
```

Oracle output for all eight at archiving time — and, since every stated depth is
the true depth, the same run one level tighter must fail:

```
mixcolumns_97gates_depth3.json 3              gates=97 depth=3 outputs_built=32/32 VALID
mixcolumns_92gates_depth4.json 4              gates=92 depth=4 outputs_built=32/32 VALID
mixcolumns_89gates_depth5.json 5              gates=89 depth=5 outputs_built=32/32 VALID
mixcolumns_88gates_depth5_fromscratch.json 5  gates=88 depth=5 outputs_built=32/32 VALID
mixcolumns_88gates_depth5.json 5              gates=88 depth=5 outputs_built=32/32 VALID
mixcolumns_88gates_depth6.json 6              gates=88 depth=6 outputs_built=32/32 VALID
mixcolumns_88gates_depth7.json 7              gates=88 depth=7 outputs_built=32/32 VALID
mixcolumns_88gates_depth8_thirdfamily.json 8  gates=88 depth=8 outputs_built=32/32 VALID

mixcolumns_88gates_depth5_fromscratch.json 4  depth<= 4: VIOLATED   VERDICT: INVALID
mixcolumns_88gates_depth5.json 4              depth<= 4: VIOLATED   VERDICT: INVALID
mixcolumns_88gates_depth6.json 5              depth<= 5: VIOLATED   VERDICT: INVALID
```

Two circuits now sit at **(88 gates, depth 5)** — the from-scratch one of §7 and
the derived one of §8. They are different value sets (plain Jaccard 0.313), and
nothing in this repository keys a record on the (gates, depth) pair.

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

## 3. 89 gates @ depth 5 — lineage spans two runs

- **What:** 89-gate depth-5 circuit — until 2026-07-29 the best point this
  project held at depth 5, and the basin the derived 88 @ depth 5 of §8 later
  came out of. It
  is now **dominated by this project's own from-scratch 88 @ depth 5** (§7, same
  depth, one gate fewer), so it is no longer a frontier point; it is kept because
  it is a link in the lineage of the 88 @ depth 7 and because it is what the
  published depth-5 point was first improved on by. Beats the
  published depth-5 point (94 gates: Osvik–Canright, ePrint 2024/1076,
  Appendix F) by five gates; the
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

## 4. 88 gates @ depth 7 — matches the published record with an independent circuit

- **What:** 88-gate depth-7 circuit — the first 88-gate circuit found by this
  project's own search, and the result that takes the project record from 89 to
  88. It **matches the published record** (Jean, ePrint 2026/1481, 88 gates;
  depth 7 is our measurement — the paper states no depth) **with an independent
  circuit**: the two share 61 of 88 masks (Jaccard 0.530). It does **not** beat
  it. Jean's circuit, transcribed and oracle-verified, is archived and credited
  in `campaign87_imported_prior_art/`.
- **How:** the engine rebuilt during campaign 87 (`../METHODS.md` §5–§6). Worker
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
  | ↓ | **88 @ d7** | `merged-engine` worker `w10_sym94`, walk drift, it = 45 614 (88-gate size, at depth 11) → 47 436 (depth-7 tie-break, 5.3 s later) | **1 973 s (32.9 min) / 07-26 22:08:19** |

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

  Point 2 is what closes the route, and the reason it closes it is in the chunk
  loop of the archived `code/hunt_worker.py`: between chunks the worker reseeds
  with `seed_masks = set(ctx.best_masks)` — the **best**, never the current
  state. So a `cur` that an LNS chunk had cross-pollinated is discarded at the
  chunk boundary unless it improved the best, and no LNS chunk on this worker
  ever did. Cross-pollinated material had no path into the next walk chunk. This
  matters here more than anywhere else in this file: unlike the hunt87 fleet of
  §6 and §7, **this fleet genuinely did cross-pollinate** — five of its workers
  were seeded on the imported circuit and its `hunt_worker.py` sets `pop_glob`
  directly — so the argument cannot lean on the knob being off, only on where
  the merged masks could and could not go.
- **How it sits relative to the other known circuits** (Jaccard on mask sets,
  all re-measured): 0.530 to Jean's 88 (61 shared, symdiff 54), 0.526 to
  Sun–Yang–Li's 89 (ePrint 2025/1493), 0.539 to our own 89@d5. The threshold
  used throughout the campaign is J ≥ 0.7 for "same family".
- **The baseline that 61/88 has to be read against:** Jean (ePrint 2026/1481)
  and Sun–Yang–Li (ePrint 2025/1493) are two indisputably independent published
  works, and their circuits share **63 masks (J = 0.553) with each other** —
  *more* than ours shares with Jean's (61, J = 0.530). At this problem size a
  ~60-mask overlap is what independence looks like; the independence claim here
  rests on the logged lineage above, and the overlap figure agrees with it.

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
- **How:** the `hunt-deeper` run, 12 workers. Record worker
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

## 6. 88 gates @ depth 6 — a new family, found from scratch

**Standing after 2026-07-30:** the from-scratch 88 @ depth 5 of §7 dominates this
circuit (same count, one level shallower), so it is no longer a frontier point.
It keeps its own standing for two reasons that the newer circuit does not
displace: it is a **different family** — plain Jaccard 0.323 between them, well
under this repository's 0.7 rule, and weighted Jaccard 0.1025, the largest such
figure the new circuit reaches against anything — and it remains the
**first 88 this project found from scratch**. Its k ≤ 3 shell certificate and its
basin survey stand unchanged.

- **What:** an 88-gate depth-6 circuit. It is **not a new gate-count record** —
  88 is the existing best-known count, held by Jean (ePrint 2026/1481, posted
  2026-07-23, and Jean has priority) and independently matched by our own 88 @
  depth 7. What it does is **strictly improve the published depth–count Pareto
  frontier**: it **dominates Jean's 88 @ depth 7** (equal count, one level
  shallower) and **improves on the published depth-6 point of 92 gates (Maximov)
  by four gates**. That paper states no depth, so the 7 is this project's
  measurement of its own transcription — but it is **forced, not merely
  observed**: the ASAP (least-fixpoint) schedule over Jean's own mask set, via
  `pipeline/engines.py:relax`, is the shallowest schedule that mask set admits
  and it still puts three of Jean's output masks at depth 7. Jean's circuit
  cannot be rescheduled shallower, so the domination does not rest on any
  transcription or scheduling choice of ours.
  It was also the **fourth
  distinct 88-gate family** this project identified, at Jaccard 0.313 to Jean's
  88, 0.323 to our 88 @ 7, 0.313 to our 88 @ 8, 0.313 to the derived 88 @ 5 and
  0.323 to the from-scratch 88 @ 5 of §7 — and **0.098–0.109** on the periphery
  alone, so outside
  the 32 obligatory targets it shares almost nothing with anything previously
  known. Not a relabelling either: over all four byte rotations ρ^k of every
  *other* 88- and 89-gate circuit this project holds or has transcribed, the
  largest Jaccard it reaches is **0.375 (0.167 on the periphery), at ρ¹ of the
  from-scratch 88 @ depth 5**. **Recomputed 2026-07-30, and the recomputation
  merged two figures into one:** before that circuit existed this maximum was
  0.362/0.153 over the seven-circuit set that includes the superseded 89 @
  depth 10 (which the artifact repository still ships, attained by it unrotated),
  and 0.351/0.141 over the six circuits this repository itself held — the table
  in `campaign87_run_2026-07-28_got_88at6_fromscratch/PROVENANCE.md` — at ρ² of
  our 89 @ depth 5. The new circuit is in *both* sets and exceeds both figures,
  so the two scopes now give the same answer. The older numbers were correct for
  their sets when written and are not withdrawn. One warning for a reader
  recomputing: **0.375 (0.167) also appears here as something else entirely** —
  it is this circuit's Jaccard to its own ρ² image (both pairings happen to share
  48 masks, 16 of them off-target), which measures how far it is from being
  ρ²-symmetric (it is the least symmetric 88 here, 0.545 by mask count), not a
  similarity to anything. The two readings are unrelated.
- **Provenance: from scratch.** The search that reached it began at a freshly
  generated random construction — not at any earlier circuit of ours and not at
  any published one. This is the first 88 this project has found that way; the
  88 @ depth 7 of §4 is own-lineage but warm-started from the project's own
  record chain.
- **How:** the multi-day **87-hunt** fleet (15 search workers + the k=2 detector,
  one shared harvest directory), worker **`c_naive`** — the from-scratch cascade:
  `constructors.build("naive", seed)` builds randomized balanced XOR trees over
  the 32 raw inputs, and the uncapped `alt` worker (120 s walk chunk / 420 s LNS
  chunk) reduces from there. On **restart 18** the root was `naive#2163`, 139
  gates at depth 3; 37 minutes later the walk was at 88.
- **Circuit:** `circuits/mixcolumns_88gates_depth6.json` (sha256
  `799440d7578809b4…`). Source of record:
  `campaign87_run_2026-07-28_got_88at6_fromscratch/FOUND_88gates_depth6.json`
  (byte-identical gate list).
- **Code that produced it:**
  `campaign87_run_2026-07-28_got_88at6_fromscratch/code/` — the engine, worker and
  root constructors, with `CODE_PROVENANCE.md` and `CONFIG_AS_RUN.md`. That
  `engines.py` is the shipped `pipeline/engines.py` plus three additions (harvester
  reuse across chunks, a harvest size cap, and knob-gated family repulsion which
  was **off** here), none of which touch the moves or the kernel.
- **Lineage** — no seed circuit at all, ours or anyone's:

  | step | circuit | how | when it appeared (run-time / wall 2026-07-28) |
  |---|---|---|---|
  | root | **139 @ d3** | `constructors.build("naive", 2163)`, **from scratch** | restart 18 opened at 66 009.5 s / 16:42:36 |
  | ↓ | 95 → 92 → 90 → 89 | `alt` chunks inside restart 18 (the chunk lines' local `best=`) | 16:43:29 → 16:52:12 |
  | ↓ | **88 @ d7** | walk, it = 37 270 | **68 238.2 s (18.96 h) / 17:19:45** |
  | ↓ | **88 @ d6** | same walk, Pareto depth tie-break, it = 37 501 | **68 238.7 s / 17:19:45** — 0.5 s later |

  The root re-derives from the archived `code/constructors.py`: seed 2163 gives
  139 gates at depth 3, exactly as logged (re-validated 2026-07-29).
- **Why no material from anywhere else is in this chain.** The argument starts at
  the **root**, which is where it is strongest, and only then reaches the knobs:
  0. **The root reads nothing.** The worker's root spec was `constructor:naive`,
     and the `constructor:` branch of `Roots.next` in the archived
     `code/hunt_worker.py` calls only `constructors.build(name, seed)` — it has
     **no file-reading path at all**. Every branch of that class that can open a
     circuit (`pool89`, `file:`, `glob:`) is a different branch and was
     unreachable under this spec. All **38** restarts logged in the session that
     produced this circuit opened on a `naive#<seed>` root, and restart 18 opened
     on `naive#2163`, which rebuilds to exactly the logged 139 gates at depth 3.
     Nothing can enter through a root that reads nothing. (The derived 88 @ depth
     5 of §8 is the reason to say this first: the knobs below were identical for
     the worker that found it, and material still reached it — through its
     **root**.)
  1. **Cross-pollination could not have fired for this worker, argued in two
     parts because `supervisor.py` as run is not archived** — it is in neither
     repository, and the archive records that the surviving copy was edited on
     2026-07-29 and is therefore not the version that ran. (a) *From archived
     material alone*: in the archived `code/hunt_worker.py` the engine knob dicts
     are given only `harvest_path`, the string `pop_glob` does not appear in that
     file at all, so this worker's `_Harvester` had `glob_pat=None` and its
     `merge_into` — whose one call site, inside `engine_lns`, is guarded by
     `if harv.glob_pat` — was never called. (b) *From the wider fleet tree, which
     is not published here*: `pop_glob` has exactly one writer anywhere in it,
     `worker.py:wire_harvest`, which the archived `hunt_worker.py` never calls
     (it imports only `WorkerCtx` and `pareto_better` from `worker`) and which
     `supervisor.py` never reaches, because it launches only `hunt_worker.py`,
     `orbit_runner.py`, `explorer.py` and `detector.py` — never `worker.py`.
     Part (b) generalises the result from this worker to the whole fleet; part
     (a) is the half a reader can check from what ships here, and it is enough
     for this circuit. Independently of both, `engine_lns` logs
     `[lns] cross-pollinated N masks (pool=…)` on every merge that brings in new
     material, and the untouched `runs_hunt/c_naive.log` contains **zero** such
     lines. Code and log agree. (The *earlier* wave-2 and wave-3 fleets of §4 and
     §5 ran a different `hunt_worker.py` that set `pop_glob` directly, and there
     cross-pollination genuinely was live and is logged; the two files share a
     name and nothing else on this point.)
  2. the worker ran `repel=False` (first line of the log), so `repel_masks.json`
     — which holds masks of the three older families — was never loaded;
  3. every restart builds a fresh `LocalCtx` and sets `cur = seed_masks`. The
     worker had already reached an 88 @ depth 8 on restart 17 from a *different*
     root, and that circuit did not seed restart 18: nothing but the global Pareto
     bookkeeping crosses a restart boundary;
  4. `engine_walk` has no pool at all and only adds masks derived from its own
     value set's closure; the 89 and both 88-gate states came from walk chunks. One
     LNS chunk of restart 18 did improve the best (92 → 90) — with `pop_glob`
     unset, its rebuild pool holds only that worker's own masks, their pairwise
     sums and its own accumulated hot list, so that step imported nothing either.
- **Its own shell is exhaustively empty:** all 1 540 k=2 windows and all 27 720
  k=3 windows, zero reducible (§9; verdict logs in the archive's
  `certificates/`). The basin around it is large and uniformly shallow: 8 993
  distinct 88-gate states at J > 0.7 to it, **4 420 of them realizable at depth
  6**, none deeper than 7, all proven k=2 irreducible.
- **Negative result: nothing in this basin reaches depth 5.** The obvious
  follow-up question — whether any of the 4 420 depth-6 states could be
  rescheduled at depth 5, which would give a Jean-independent 88 @ depth 5 and
  supersede the derived one of §8 — is answered no by the evidence already in
  hand. The basin screen computed each member's ASAP (least-fixpoint) depth with
  `pipeline/engines.py:relax`, i.e. the shallowest depth that mask set admits at
  all, and the histogram over all 8 993 members is exactly **4 420 at depth 6 and
  4 573 at depth 7, with no bucket below 6** (re-derived independently 2026-07-29
  from the campaign's own 8 993-state pool). Depth 6 is therefore *minimal* for
  every member of this basin, not merely achieved. The complementary search for a
  new mask set was run too: a depth-capped-5 SAT sweep over 27 windows carved out
  of this circuit returned **22 UNSAT and 0 SAT**, with 5 windows — all at the
  widest radius (r = 9) — left undecided by a 150 s timeout. So no 88 @ depth 5
  exists in this family's basin, and none was found near it; a Jean-independent
  88 @ depth 5, if one exists, lives somewhere else. (Sweep logs and the pool are
  in the raw campaign archive, `campaign_87/hunt87_basin4/`, which is not part of
  this repository; `results.json` there carries the totals.)

  **This prediction held, and a day later it paid out.** On 2026-07-30 the same
  worker found an 88 @ depth 5 from scratch (§7) — and it is indeed *somewhere
  else*: not in this basin, not in this family, at weighted Jaccard 0.1025 to
  this circuit. The negative result was correctly scoped; nothing in it has to be
  withdrawn.

---

## 7. 88 gates @ depth 5, found from scratch — the frontier point

- **What, and what it is not.** An 88-gate circuit at **depth 5**, found by a
  search whose root was a randomized XOR tree over the 32 raw inputs. It is
  **not a new gate-count record.** 88 is the published best-known count, held by
  Jean (ePrint 2026/1481, posted 2026-07-23), and **Jean has priority**. What
  changed on 2026-07-30 is that the (88, depth 5) point is now reached by a
  circuit found from scratch — root `constructors.build("naive", 1958)` — rather
  than only by a circuit whose seed chain runs through Jean's published work
  (§8). **This removes this project's dependence on that circuit at the depth-5
  point; it does not beat it.** That framing is the point of the section: the
  collapse of this repository's two frontiers into one is about *our* provenance,
  not about his result.

  Against the rest of the field it **dominates Jean's 88 @ depth 7** (equal
  count, two levels shallower — with the standing caveat that depth 7 is our own
  measurement of our transcription, since that note states no depth), **improves
  on the published 94 @ depth 5** (Osvik–Canright, ePrint 2024/1076, Appendix F)
  by six gates, and dominates this project's own **88 @ 6, 88 @ 7, 88 @ 8 and
  89 @ 5**. It supersedes the derived 88 @ depth 5 of §8 as the circuit
  establishing that Pareto point. **87 was not found**; nothing is claimed
  optimal.

  Independently recomputed from the raw JSON against a locally rebuilt GF(2⁸)
  spec: 88 gates, depth 5, 32/32 outputs, **0 dead gates**, 0 duplicate masks, no
  gate mask colliding with an input.
- **Provenance: from scratch.** Same worker, same fleet and byte-identical code
  as the 88 @ depth 6 of §6 — a different session, a different root, a different
  basin. Worker **`c_naive`**, **session 5, restart 16** (quote the session: the
  log holds five worker sessions and 58 restarts, and each session's run-time
  clock restarts at 0). Root `constructors.build("naive", 1958)` = 146 gates at
  depth 3, rebuilt from the archived constructors and confirmed. Both 88-gate
  states came out of a **walk** chunk, and `engine_walk` has no candidate pool
  and no disk read path.
- **How:** the multi-day **87-hunt** fleet, uncapped `alt` worker (120 s walk
  chunk / 420 s LNS chunk), `repel=False`. From the root, 64 minutes: the LNS
  chunks carried the local best 93 → 91 and 90 → 89, a walk chunk carried
  91 → 90, and a walk chunk reached **88 @ depth 6 at iteration 33 873**, which
  the Pareto depth tie-break carried to **88 @ depth 5 at iteration 37 155**,
  6.1 s later.
- **Circuit:** `circuits/mixcolumns_88gates_depth5_fromscratch.json`. Source of
  record: `campaign87_run_2026-07-30_got_88at5_fromscratch/FOUND_88gates_depth5_fromscratch.json`
  (sha256 `582ddd087ecf197a…`, byte-identical gate list).
- **Code that produced it:** `campaign87_run_2026-07-30_got_88at5_fromscratch/code/`
  — which contains **no source files**, deliberately. All five are
  **byte-identical** to
  `campaign87_run_2026-07-28_got_88at6_fromscratch/code/`, published in v3.0.0 on
  2026-07-29 with modification times of 2026-07-27, so they are hash-pinned in
  `CODE_PROVENANCE.md` rather than duplicated. That the producing code was fixed,
  archived and published two days before the find is itself part of the
  provenance.
- **Lineage** — no seed circuit at all, ours or anyone's:

  | step | circuit | how | when it appeared (run-time of session 5 / wall) |
  |---|---|---|---|
  | root | **146 @ d3** | `constructors.build("naive", 1958)`, **from scratch** | session 5, restart 16 opened at 65 349.0 s / 07-30 09:44:09 |
  | ↓ | 93 → 91 → 90 → 89 | `alt` chunks inside restart 16 (the chunk lines' local `best=`) | 09:45:13 → 10:38:47 |
  | ↓ | **88 @ d6** | walk, it = 33 873 | **69 192.7 s (19.22 h) / 07-30 10:48:12** |
  | ↓ | **88 @ d5** | same walk, Pareto depth tie-break, it = 37 155 | **69 198.8 s / 07-30 10:48:19** — 6.1 s later |

  The 88 @ d6 in the second-to-last row is an intermediate of *this* descent, not
  the family-4 circuit of §6; it was superseded 6.1 s later and is not separately
  archived. The root re-derives from the archived root constructors — the
  `code/constructors.py` of the 88 @ depth 6 archive, hash-pinned by this one:
  seed 1958 gives 146 gates at depth 3, exactly as logged (re-validated
  2026-07-30).
- **Why no material from anywhere else is in this chain.** Five parts, all
  checkable in the archived code and log:
  0. **The root reads nothing.** The `constructor:` branch of `Roots.next` calls
     only `constructors.build(name, seed)` and has **no file-reading path at
     all**; every branch that can open a circuit off disk (`pool89`, `file:`,
     `glob:`) is a different branch, unreachable under this spec. Every restart
     in all five sessions opens on a `naive#<seed>` root.
  1. **Cross-pollination could not have fired for this worker**, argued in the
     same two parts as §6 because `supervisor.py` as run is archived in neither
     repository. (a) *From published material*: the hash-pinned `hunt_worker.py`
     never mentions `pop_glob`, so this worker's `_Harvester` had
     `glob_pat=None`, and `merge_into`'s one call site inside `engine_lns` is
     guarded by `if harv.glob_pat`. (b) *From the unpublished fleet tree*:
     `pop_glob` has exactly one writer anywhere in it,
     `worker.py:wire_harvest`, which `hunt_worker.py` never calls and which
     `supervisor.py` never reaches, because it launches only `hunt_worker.py`,
     `orbit_runner.py`, `explorer.py` and `detector.py` — never `worker.py`;
     that part extends the conclusion to the whole fleet. And the log carries
     **zero** `[lns] cross-pollinated …` lines over its whole 1 941-line life.
  2. `repel=False` on the session's first line, so `repel_masks.json` was never
     opened.
  3. Every restart builds a fresh `LocalCtx` and sets `cur = seed_masks` — here
     *observably*, not just by code reading: restart 16 opens at `cur=93 best=93`,
     **worse** than restart 15's `best=92`. Nothing carried over.
  4. No `reseed_*.json`, no `ctx.adopt`, and `hunt_worker.py` does not import
     `archive` at all; the producing engine, `engine_walk`, has no pool and only
     adds masks derived from its own value set's closure.
- **Four corroborations a sceptic can check** (all four are spelled out with
  commands in the archive's `PROVENANCE.md`):
  1. **The code predates the find and is already public** — byte-identical to
     v3.0.0's copies, mtimes 2026-07-27, find 2026-07-30.
  2. **The published log is a byte-exact prefix of the archived one.** The
     `c_naive.log` released with the 88 @ depth 6 in v3.0.0 (123 197 B, 1 505
     lines) is byte-for-byte the first 123 197 bytes of the 158 747-byte log
     archived with this record, and that prefix already contains **session 5's own
     `repel=False` start line**. The configuration of the producing session was
     committed to a public repository roughly **twelve hours** before the find
     (commit `391f427`, 2026-07-29 22:51:58 −0400; find 2026-07-30 10:48:19 —
     11.94 h). The published log's *content* stops earlier still, its last line
     at 20:41:47, 14.11 h before the find. It is the one thing in this archive
     that could not have been arranged afterwards.
  3. **The mask set is this worker's own** — line **35 285** of `c_naive`'s
     harvest file, appearing in **zero** of the fleet's other fifteen harvest
     files (sixteen in total, ≈ 1.1 GB, searched line-exact 2026-07-30). The
     absence half is *reported, not checkable here*: those harvest files are not
     shipped, are still growing, and no command in the archive runs against them.
     The line number is checkable, though, from the published log alone: the
     `harv=` counter resets per session, sessions 1–3 harvested nothing, session
     4 ends at `harv=22489` and session 5 at `harv=14816`, and
     22 489 + 14 816 = **37 305** — exactly the harvest's line count and the
     pocket scan's distinct-state count. That puts the record at session-5
     harvest entry 35 285 − 22 489 = **12 796**, and the two `[walk]` lines
     straddling the find report `harv=12631` (10:47:44) and `harv=12939`
     (10:48:24). It falls strictly between them.
  4. **The RNG seed is arithmetically forced by the clock.** The worker advances
     its seed by +1 per chunk and +101 per restart from `--seed 201`, so seed
     1958 at restart 16 implies exactly 242 prior chunks; at the `alt` cycle's
     120 s + 420 s that predicts 65 340 s for the restart-16 opening against the
     **65 349.0 s** logged — 0.014 % off. Inserting or removing a restart anywhere
     in the session breaks this.
- **Not a lone point — a 135-member depth-5 pocket.** Replaying every distinct
  88-gate target-covering value set in `c_naive`'s own harvest (37 305 of them)
  and giving each its ASAP depth with `pipeline/engines.py:relax` gives
  **135 distinct own-lineage value sets realizable at depth 5**, all
  oracle-verified, every one of them first appearing at or after line 35 285. The
  record is one of the 135. Across the whole pocket the maximum weighted Jaccard
  is **0.0602** to Jean's 88 and **0.0651** to the derived 88 @ depth 5.
  `certificates/pocket_depth5_scan.log` in the archive holds the scan itself —
  the ASAP depth histogram and the first twenty line numbers, from which the
  135 and the "at or after 35 285" both read directly. It is **not** a
  certificate, as its own `certificates/README.md` says, and it does **not**
  contain the oracle output or the weighted-Jaccard figures: those were computed
  in the raw campaign tree with the calibrated metric described below, which is
  not in this repository.
- **Certificates: its k ≤ 3 shell is exhaustively empty.** All 1 540 k=2 windows
  and all 27 720 k=3 windows irreducible, zero hits, run with the repository's own
  archived decider — so **any 87 differs from it by ≥ 4 masks** (§9). Together
  with the 88 @ depth 6, it is one of only two circuits here that have an
  exhaustive k ≤ 3 shell *and* a lineage independent of Jean's.
- **A third distinct depth obstruction.** The masks whose minimum build depth
  equals the circuit depth are output rows **1, 7, 12, 13, 17, 18, 21, 25, 27, 28
  and 31** — six weight-7 targets (1, 12, 17, 25, 27, 28) and five weight-5
  ones (7, 13, 18, 21, 31). That is a **third**
  structurally distinct way to hit a depth wall at 88 gates, against rows 3 and 27
  for our 88 @ depth 7 and rows 1, 11, 17 and 25 for the 88 @ depth 6. Eleven
  simultaneously critical rows is what a circuit pushed to its own depth floor
  looks like. (Recomputable with `pipeline/engines.py:relax`.)
- **How far it is from everything else.** Plain Jaccard on mask sets, and the
  campaign's calibrated weighted Jaccard (periphery-only, neutral-corpus IDF
  weights) maximised over all four byte rotations ρ^k. **The plain columns
  recompute from the circuit JSONs in this repository; the weighted column does
  not** — that metric's implementation, its IDF weight vector and the corpus it
  was calibrated on all live in the raw campaign tree, so read the `wj` figures
  as reported and the plain ones as checkable. Nothing claimed here rests on the
  weighted column alone:

  | against | shared | plain J | periphery J | max wj over ρ^k |
  |---|---|---|---|---|
  | Jean's 88 (ePrint 2026/1481) | 42 / 88 | 0.313 | 0.098 | **0.0598** |
  | our 88 @ d7 (family 1) | 39 | 0.285 | 0.067 | 0.0417 |
  | our 88 @ d8 (family 3) | 41 | 0.304 | 0.087 | 0.0514 |
  | our 88 @ d6 (family 4) | 43 | 0.323 | 0.109 | **0.1025** |
  | the derived 88 @ d5 (§8) | 42 | 0.313 | 0.098 | 0.0642 |
  | our 89 @ d5 | 42 | 0.311 | 0.097 | 0.0644 |
  | Sun–Yang–Li's 89 (ePrint 2025/1493) | 43 | 0.321 | 0.108 | 0.0467 |

  Every weighted figure is at most **0.1025** — a factor of three below the
  metric's 0.32 "distinct" floor, and below 0.07 against everything except the
  other from-scratch circuit — so this is a distinct family under the
  calibrated metric as well as under this repository's plain-Jaccard 0.7 rule.
  It is also outside every family of the campaign's completed census, which
  certifies **11 proven-distinct families in 14 same-linked groups** over
  **410 222** distinct 88-gate states: across the 100 archived group
  representatives this circuit's largest weighted Jaccard is **0.293** (groups
  G05/F10), still under the 0.32 distinct floor. For scale, the group that
  actually holds Jean's circuit sits at **0.0668** and the group holding this
  project's derived 88s at **0.0626**. (The census, its 410 222 states, the 11
  families and the 100 group representatives all live in the raw campaign tree,
  which is not part of this repository, and so do the weighted metric and its
  calibration corpus. None of these figures can be re-derived from what ships
  here; the plain-Jaccard ones can.)

  **The number to quote for novelty is the rotated maximum, not the unrotated
  one.** Unrotated, plain Jaccard to everything above is 0.285–0.323; over all
  four rotations the largest value reached is **0.386 (0.179 on the periphery),
  attained at ρ³ of Jean's 88**. That is the honest ceiling, and it is not large
  in context: this circuit's similarity to its own rotations sits at
  **0.333–0.375**, so 0.386 against everything else is only marginally above what
  it scores against a rotated copy of itself. It shares 42 of Jean's 88
  masks — but **32 of those are the obligatory output targets**, so only **10 of
  the 56 freely chosen masks** coincide.

---

## 8. 88 gates @ depth 5, derived — the record-89 basin at 88 gates, seeded through Jean's circuit

- **Superseded at its Pareto point, retained as documented derived work.** Since
  2026-07-30 the (88, depth 5) point is established by the from-scratch circuit of
  §7; this one is kept, unchanged and undeleted, because a documented derived
  result is worth more than a deleted one — it is the record of how the project
  first reached depth 5 at 88 gates, and of the seeding bug that made the route
  derived. Its first-sentence derived disclosure below stands.
- **Read this first — provenance:** our engine found this circuit, but **its seed
  chain passes through Jean's published 88** (ePrint 2026/1481), so it is **not**
  an independent construction: it is a "derived from published work" result in the
  sense of [`METHODS.md`](../METHODS.md) §9, and the sibling of the 88 @ depth 8
  in §5 — same seed, same root cause. The chain, every link checked by mask
  identity:

  ```
  Jean's 88 (IMPORTED_88.json)
    -> symmetrized + peeled to 95, orbit-walked to 92        (sym88_92g.json)
    -> unioned with a 91 of our own lineage                  (union_A88.json)
    -> rho^2-symmetric 90 @ d9, "basin 1"                    (uA88_90g.json)
       == hunt87 seeds/orbit/sym90_a.json, byte-identical (sha256 8642ae8702987dc4...)
          to campaign87_certificates/rho2_symmetric_90s/BEST_90gates_depth9_rho2symmetric.json
    -> orbit worker o1, cycle 129, mode sym                  (o1_c129_90g.json, J = 1.000)
    -> worker o_polish restart 71 -> 88 @ d6 -> 88 @ d5
  ```

  The 90 @ depth 9, its union files and the orbit-walk logs were already archived
  in this repository with the 88 @ depth 8, so the whole chain re-checks from this
  repository alone. **Root cause, since fixed:** `orbit_runner.pick_seed` used
  `orb[cycle % len(orb)]`, and index 2 is only reached on the cycle the `div89`
  branch above it already consumes — so `seeds/orbit/sym94.json`, the *only*
  own-lineage orbit seed (byte-identical to the ρ²-symmetric 94 that produced the
  clean 88 @ 7), was unreachable. Counted over both orbit workers' logs: **345
  cycles, 233 on an orbit seed — 119 on `sym90_a`, 114 on `sym90_b`, 0 ever on
  `sym94.json`.** Fixed 2026-07-29, 28 minutes after this find.
- **What:** an 88-gate circuit at **depth 5** — two levels shallower than the
  published 88 @ depth 7, and six gates better than the published depth-5 point
  (94 gates: Osvik–Canright, ePrint 2024/1076, Appendix F). It is joint-shallowest
  with the from-scratch 88 @ depth 5 of §7, which supersedes it as the circuit
  establishing that Pareto point. Independently recomputed from the raw JSON against a
  locally rebuilt GF(2⁸) spec: 88 gates, depth 5, 32/32 outputs, **0 dead gates**,
  0 duplicate masks; 71 of its 88 masks are ρ²-symmetric (80.7 %).
- **It is not a new family.** At Jaccard **0.735 to this project's record 89 @
  depth 5** (75 shared masks, 0.614 on the periphery) it is *above* the 0.7
  same-family threshold used throughout, and closer to that 89 than to any 88
  (best 0.615, our own 88 @ 8; 0.544 to Jean's 88; 0.313 to the 88 @ 6 of §6, and
  0.313 to the from-scratch 88 @ 5 of §7 — the two circuits at (88, depth 5) are
  as far apart as any two 88s here). The right description is **the record-89
  basin reached at 88 gates**, not a family of its own.
- **How:** the same 87-hunt fleet, two workers in series. **`o1`**, a
  ρ²-equivariant orbit ladder, ran cycle 129 on the derived 90 @ depth 9 and saved
  a mask-identical 90. **`o_polish`** — which reads the orbit workers' saved
  circuits as plain mask sets and runs the unconstrained engine on them — took
  that file as the root of its restart 71 and walked 90 → 88 in 85 s.
- **Circuit:** `circuits/mixcolumns_88gates_depth5.json` (sha256
  `9bd2019d7d033def…`). Source of record:
  `campaign87_run_2026-07-29_got_88at5_derived/FOUND_88gates_depth5.json`, which
  is byte-identical (sha256 `bff7b927269f2b59…`) to `runs/o_polish_best.json` as
  the worker saved it.
- **Code that produced it:** `campaign87_run_2026-07-29_got_88at5_derived/code/`.
  One caveat recorded there: `orbit_runner.py` is the **post-fix** version, edited
  28 minutes after the find; everything else is as-run. The descent replays from
  the archived seed without that file.
- **Lineage** (the derived part above, then the descent):

  | step | circuit | how | when it appeared (run-time / wall 2026-07-29) |
  |---|---|---|---|
  | seed | **90 @ d9, ρ²-symmetric** | **derived from Jean's published 88**, as above | o1 cycle 129 at 116 106.2 s / 06:37:36 |
  | ↓ | (root adopted) | `o_polish` restart 71, rng seed 9841 | 126 918.0 s / 09:37:48 |
  | ↓ | **88 @ d6** | walk, it = 38 447 | **127 003.3 s / 09:39:14** — 85.3 s into the restart |
  | ↓ | **88 @ d5** | same walk, Pareto depth tie-break, it = 40 419 | **127 007.5 s (35.3 h) / 09:39:18** — 4.2 s later |

  The 88 @ d6 in the second-to-last row is an intermediate of *this* descent, not
  the family-4 circuit of §6; it was superseded 4.2 s later and is not separately
  archived. The worker ran a further 5 h 51 min without finding an 87.
- **Certificates:** its k=2 shell is exhaustively empty (all 1 540 windows), so
  any 87 differs from it by ≥ 3 masks. Its **k=3 shell was never swept**. Together
  with our own 88 @ depth 7 — which has no exhaustive shell at any radius, only
  9 exact k=4 windows and 8 windowed-SAT cone windows — it is one of the two least
  certified circuits here (§9).

---

## 9. Machine-checked certificates for the 88-gate plateau

No 87-gate circuit was found anywhere in the campaign. Where a search cannot
settle the question, a decision procedure was run over *neighbourhoods* of the
known 88s instead; the full write-up, with the archived per-run verdict
summaries, is in
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
- **The three 88s of §6–§8 — two from scratch, one derived — swept with this
  repository's own decider**
  (verdict logs and the driver in each run archive's `certificates/`):
  the **from-scratch 88 @ depth 5** (§7) has all 1 540 k=2 windows *and* all
  27 720 k=3 windows irreducible — shell exhaustively empty, so any 87 differs
  from it by ≥ 4 masks (swept 2026-07-30); the **88 @ depth 6** likewise, at both
  radii (re-validated 2026-07-29); the **derived 88 @ depth 5** (§8) has its
  1 540 k=2 windows irreducible (≥ 3 masks) and its **k=3 shell was not swept**.
  Around the 88 @ depth 6, all 8 993 known states of its basin are proven k=2
  irreducible as well, plus 1 200 states beyond the harvest.
- **The exhaustive shells and the independent lineages now overlap.** The point
  made below — that all 47 of the certified canonical circuits lie in Jean's
  lineage while our own independent 88 @ depth 7 is the least certified — was the
  honest shape of the negative result in v3.0.0. Two circuits now sit in both
  sets: the 88 @ depth 6 and the from-scratch 88 @ depth 5 each have an
  exhaustively empty k ≤ 3 shell *and* a lineage independent of Jean's. The gap is
  narrower than it was; it is not closed, because the 88 @ depth 7 still has no
  exhaustive shell at any radius.
- **Depth obstructions differ by basin — three patterns now.** The masks whose
  minimum build depth equals the circuit depth are, for our 88 @ depth 7, output
  rows **3 and 27**; for the 88 @ depth 6 of §6, rows **1, 11, 17 and 25** — four
  weight-7 targets; and for the from-scratch 88 @ depth 5 of §7, rows **1, 7, 12,
  13, 17, 18, 21, 25, 27, 28 and 31** — six weight-7 and five weight-5 targets
  at once. So MixColumns has at least three structurally distinct ways to hit a
  depth wall at 88 gates, the depth-6 point was not reachable by pushing on the
  old plateau, and the depth-5 point was not reachable by pushing on the depth-6
  basin either (§6's negative result); each needed a different basin.
  (Recomputable with `pipeline/engines.py:relax`.)
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

- **Provenance in one line:** 97@d3, 92@d4, 88@d6 and the frontier 88@d5 of §7
  are from scratch — each rooted in a fresh construction that reads nothing;
  89@d5 and 88@d7 continue the same own-lineage chain, seeded on the project's
  prior output rather than rediscovered cold; 88@d8 (§5) and the derived 88@d5
  (§8) are the derived ones, both through Jean's published 88.
- **Literature status** (corrected 2026-07-23; full dated audit in the artifact
  repository's PRIOR_ART.md, including its Corrections section): the published
  depth–count frontier is 99@3 (Shi–Feng–Xu, ToSC 2023), 97@4 and 94@5
  (Osvik–Canright, ePrint 2024/1076), 92@6 (Maximov), and 88@7 (Jean, ePrint
  2026/1481), with 89 at unstated depth from Sun–Yang–Li (ePrint 2025/1493).
  Against that: **97@3 and 92@4 improve the frontier** at their depths and remain
  on it; **89@5 improved the published depth-5 point by five gates** and is now
  superseded there by our own 88@5; **88@7 ties the published gate-count floor
  with an independent circuit** rather than lowering it; **88@5 (from scratch),
  88@6 (from scratch) and the derived 88@5 lower the depth at which 88 gates is
  reached**, dominating both Jean's 88@7 and Maximov's 92@6 — but not the count,
  which stays Jean's; and **88@8 (derived) is dominated** by our own 88@7, as are
  the 88@6 and the derived 88@5 by the from-scratch 88@5.
- **Nothing here beats 88 or is proven optimal.** Every campaign that produced
  these 88s searched for an 87 and did not find one, and the certificates in §9
  bound only local neighbourhoods. The from-scratch 88@5 does not lower the count
  either: it changes *whose lineage* reaches (88, depth 5), not what 88 is.
- Every timestamp above is recoverable from the `coordinator.log` and per-worker
  `*.log` files in each run archive; every circuit from its `*_best.json`.
