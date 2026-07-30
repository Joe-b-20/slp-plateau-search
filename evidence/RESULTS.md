# Verified results and their lineage — 97@depth3, 92@depth4, 89@depth5, 88@depth5/6/7/8

Seven verified AES-MixColumns 2-input-XOR circuits, at gate counts 97, 92, 89 and
88 (four times, at depths 5, 6, 7 and 8). Two frontiers come out of them:

- **combined verified frontier: 97 @ 3, 92 @ 4, 88 @ 5**;
- **own-lineage frontier, no imported material anywhere in the chain:
  97 @ 3, 92 @ 4, 89 @ 5, 88 @ 6**.

**87 was not found**, and none of the seven is claimed optimal (SLP minimization
is NP-hard).

**Provenance up front.** 88 is the published best-known gate count, held by Jean
(ePrint 2026/1481, posted 2026-07-23) — **Jean has priority and nothing here
beats it.** Of our four 88s: the 88 @ depth 7 (§4) **matches** that count with an
independent circuit; the 88 @ depth 6 (§6) is a fourth distinct family found
**from scratch**; the 88 @ depth 8 (§5) and the 88 @ depth 5 (§7) both have seed
chains that pass through Jean's published circuit, so both are reported as
derived work and say so in their first sentence. Everything else here is this
project's own lineage, rooted in a from-scratch construction.

Each section below gives what the circuit is, where it is, the exact code that
produced it, and its **full lineage** with the run-time and wall-clock at which
every step appeared. All seven were re-verified against MixColumns rebuilt from
GF(2^8) (`../verify_circuit.py`), live in `circuits/` with SHA-256 in
`circuits/spectrum.json`, and are hash-pinned in the artifact repository
[aes-mixcolumns-xor-circuits](https://github.com/Joe-b-20/aes-mixcolumns-xor-circuits)
with listings, Verilog and self-contained verifiers (the 88 @ depth 8 ships
there as `mixcolumns_88gates_depth8.json`, labelled derived and non-frontier).
Every run referenced below is archived untouched in this folder, each with a
`code/` subfolder holding the exact code that produced it.

```
python3 ../verify_circuit.py circuits/mixcolumns_89gates_depth5.json 5   # etc.
python3 ../verify_circuit.py circuits/mixcolumns_88gates_depth6.json 6
```

Oracle output for all seven at archiving time — and, since every stated depth is
the true depth, the same run one level tighter must fail:

```
mixcolumns_97gates_depth3.json 3             gates=97 depth=3 outputs_built=32/32 VALID
mixcolumns_92gates_depth4.json 4             gates=92 depth=4 outputs_built=32/32 VALID
mixcolumns_89gates_depth5.json 5             gates=89 depth=5 outputs_built=32/32 VALID
mixcolumns_88gates_depth5.json 5             gates=88 depth=5 outputs_built=32/32 VALID
mixcolumns_88gates_depth6.json 6             gates=88 depth=6 outputs_built=32/32 VALID
mixcolumns_88gates_depth7.json 7             gates=88 depth=7 outputs_built=32/32 VALID
mixcolumns_88gates_depth8_thirdfamily.json 8 gates=88 depth=8 outputs_built=32/32 VALID

mixcolumns_88gates_depth5.json 4             depth<= 4: VIOLATED   VERDICT: INVALID
mixcolumns_88gates_depth6.json 5             depth<= 5: VIOLATED   VERDICT: INVALID
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

## 3. 89 gates @ depth 5 — lineage spans two runs

- **What:** 89-gate depth-5 circuit — the best **own-lineage** point at depth 5,
  and the basin the derived 88 @ depth 5 of §7 later came out of. Beats the
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

## 6. 88 gates @ depth 6 — a fourth family, found from scratch

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
  It is also a **fourth
  distinct 88-gate family**, at Jaccard 0.313 to Jean's 88, 0.323 to our 88 @ 7
  and 0.313 to our 88 @ 8 — and **0.098–0.109** on the periphery alone, so outside
  the 32 obligatory targets it shares almost nothing with anything previously
  known. Not a relabelling either: over all four byte rotations ρ^k of every
  *other* 88- and 89-gate circuit this project holds or has transcribed, the
  largest Jaccard it reaches is 0.362 (0.153 on the periphery). **Scope matters
  for that number and is the only reason two figures circulate:** 0.362/0.153
  is the maximum over the *seven*-circuit comparison set that includes the
  superseded 89 @ depth 10 (which the artifact repository still ships), and it
  is attained by that circuit unrotated. Restricted to the six circuits this
  repository itself holds — the table in
  `campaign87_run_2026-07-28_got_88at6_fromscratch/PROVENANCE.md`, which does
  not list the 89 @ depth 10 — the maximum is **0.351 (0.141)**, at ρ² of our
  89 @ depth 5. One more scope note, so that a reader recomputing the
  unqualified maximum is not surprised: both figures exclude the circuit's
  comparison against *itself*, whose own ρ² image sits at J = 0.375 — that is a
  measure of how far this circuit is from being ρ²-symmetric (it is the least
  symmetric 88 here, 0.545 by mask count), not a similarity to anything else.
  Both figures are correct for their stated set; neither is a
  correction of the other.
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
     5 of §7 is the reason to say this first: the knobs below were identical for
     the worker that found it, and material still reached it — through its
     **root**.)
  1. **Cross-pollination, argued in two parts** because `supervisor.py` as run is
     not archived: (a) the archived `hunt_worker.py` sets only `harvest_path` on
     both engines and **never mentions `pop_glob` anywhere**, so no sibling
     worker's harvest could be merged into this one's rebuild pool; and (b)
     independently of the code, `engine_lns` logs
     `[lns] cross-pollinated N masks (pool=…)` on every merge that brings in new
     material, and the untouched `runs_hunt/c_naive.log` contains **zero** such
     lines. Code and log agree.
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
  k=3 windows, zero reducible (§8; verdict logs in the archive's
  `certificates/`). The basin around it is large and uniformly shallow: 8 993
  distinct 88-gate states at J > 0.7 to it, **4 420 of them realizable at depth
  6**, none deeper than 7, all proven k=2 irreducible.
- **Negative result: nothing in this basin reaches depth 5.** The obvious
  follow-up question — whether any of the 4 420 depth-6 states could be
  rescheduled at depth 5, which would give a Jean-independent 88 @ depth 5 and
  supersede the derived one of §7 — is answered no by the evidence already in
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

---

## 7. 88 gates @ depth 5 — the record-89 basin at 88 gates, seeded through Jean's circuit

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
  (94 gates: Osvik–Canright, ePrint 2024/1076, Appendix F). It is the shallowest
  88 this project holds. Independently recomputed from the raw JSON against a
  locally rebuilt GF(2⁸) spec: 88 gates, depth 5, 32/32 outputs, **0 dead gates**,
  0 duplicate masks; 71 of its 88 masks are ρ²-symmetric (80.7 %).
- **It is not a new family.** At Jaccard **0.735 to this project's record 89 @
  depth 5** (75 shared masks, 0.614 on the periphery) it is *above* the 0.7
  same-family threshold used throughout, and closer to that 89 than to any 88
  (best 0.615, our own 88 @ 8; 0.544 to Jean's 88; 0.313 to the 88 @ 6 of §6).
  The right description is **the record-89 basin reached at 88 gates**, not a
  fifth family.
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
  certified circuits here (§8).

---

## 8. Machine-checked certificates for the 88-gate plateau

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
- **The two new 88s, swept with this repository's own decider** (verdict logs and
  the driver in each run archive's `certificates/`; re-validated 2026-07-29):
  the **88 @ depth 6** has all 1 540 k=2 windows *and* all 27 720 k=3 windows
  irreducible — shell exhaustively empty, so any 87 differs from it by ≥ 4 masks;
  the **88 @ depth 5** has its 1 540 k=2 windows irreducible (≥ 3 masks) and its
  **k=3 shell was not swept**. Around the 88 @ depth 6, all 8 993 known states of
  its basin are proven k=2 irreducible as well, plus 1 200 states beyond the
  harvest.
- **Depth obstructions differ by basin.** The masks whose minimum build depth
  equals the circuit depth are, for our 88 @ depth 7, output rows **3 and 27**;
  for the 88 @ depth 6 of §6 they are rows **1, 11, 17 and 25** — four weight-7
  targets. So MixColumns has at least two structurally distinct ways to hit a
  depth wall at 88 gates, and the depth-6 point was not reachable by pushing on
  the old plateau — it needed a different basin. (Recomputable with
  `pipeline/engines.py:relax`.)
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

- **Provenance in one line:** 97@d3 and 92@d4 are from scratch, and 88@d6 is too —
  its root is a fresh random construction; 89@d5 and 88@d7 continue that same
  own-lineage chain, seeded on the project's prior output rather than rediscovered
  cold; 88@d8 (§5) and 88@d5 (§7) are the derived ones, both through Jean's
  published 88.
- **Literature status** (corrected 2026-07-23; full dated audit in the artifact
  repository's PRIOR_ART.md, including its Corrections section): the published
  depth–count frontier is 99@3 (Shi–Feng–Xu, ToSC 2023), 97@4 and 94@5
  (Osvik–Canright, ePrint 2024/1076), 92@6 (Maximov), and 88@7 (Jean, ePrint
  2026/1481), with 89 at unstated depth from Sun–Yang–Li (ePrint 2025/1493).
  Against that: **97@3, 92@4 and 89@5 improve the frontier** at their depths and
  remain on it (neither newer point dominates 89@5); **88@7 ties the published
  gate-count floor with an independent circuit** rather than lowering it;
  **88@6 (from scratch) and 88@5 (derived from Jean's published circuit) lower
  the depth at which 88 gates is reached**, dominating both Jean's 88@7 and
  Maximov's 92@6 — but not the count, and in the 88@5's case not as an
  independent construction; and **88@8 (also derived) is dominated** by our own
  88@7.
- **Nothing here beats 88 or is proven optimal.** Every campaign that produced
  these 88s searched for an 87 and did not find one, and the certificates in §8
  bound only local neighbourhoods.
- Every timestamp above is recoverable from the `coordinator.log` and per-worker
  `*.log` files in each run archive; every circuit from its `*_best.json`.
