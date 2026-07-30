# Provenance — 87-hunt fleet, workers `o1` → `o_polish` (2026-07-29, produced 88 @ depth 5)

## Read this first: this circuit is DERIVED FROM PUBLISHED WORK

Our engine found it, but **its seed chain passes through Jean's published 88**
(ePrint 2026/1481), so it is **not** an independent construction. It is a
"derived from published work" result in the sense of
[`METHODS.md`](../../METHODS.md) §9 — ours to report, never ours to claim, and
Jean is credited at every step. It is also **not** a gate-count record: 88 is
the published best-known count and Jean has priority.

The chain, every link checked by mask identity (`J→prev` is the Jaccard to the
previous stage; re-measured 2026-07-29):

| stage | masks | J→prev | what it is |
|---|---|---|---|
| `IMPORTED_88.json` | 88 | — | **Jean's published 88, ePrint 2026/1481** |
| `sym88_92g.json` | 92 | 0.636 | Jean's 88 ρ²-symmetrized and peeled to 95, orbit-walked to 92 |
| `symA_91g.json` | 91 | — | a 91 of *our own* lineage (from the ρ²-symmetric 94) |
| `union_A88.json` | 113 | 0.805 | the union of the two — this is where Jean's material enters |
| `uA88_90g.json` | 90 | 0.504 | orbit-walked to a ρ²-symmetric **90 @ depth 9** ("basin 1") |
| `seeds/orbit/sym90_a.json` | 90 | **1.000** | the hunt's copy of that 90 — **byte-identical**, sha256 `8642ae8702987dc4…`, to this repo's `../campaign87_certificates/rho2_symmetric_90s/BEST_90gates_depth9_rho2symmetric.json` |
| `runs/o1_c129_90g.json` | 90 | **1.000** | what orbit worker `o1` returned from cycle 129 on that seed: 90 @ depth 9, mask-identical to it. Archived here as `seed_orbit_90gates_depth9_derived.json`. |
| **`FOUND_88gates_depth5.json`** | 88 | 0.589 | this circuit, from `o_polish` restart 71 on the file above |

The 90 @ depth 9, its union files and the orbit-walk logs proving the chain were
already archived in this repository with the 88 @ depth 8 (which is the 88 @ d5's
sibling: same seed, same root cause), so the whole chain re-checks from this
repository alone.

**Root cause, since fixed.** `orbit_runner.pick_seed` selected the orbit seed with
`orb[cycle % len(orb)]`, and index 2 is only reached when `cycle % 3 == 2` — the
cycle the `div89` branch above it already consumes. With three files in
`seeds/orbit/`, that permanently hid index 2 — `sym94.json`, the **only**
own-lineage orbit seed, byte-identical (sha256 `89416f51be37f427…`) to
`../campaign87_run_2026-07-26_got_88at7/seed_rho2sym_94gates_depth5.json`, the
seed the clean 88 @ depth 7 came from. Counted over both orbit workers' logs:
**345 cycles, 233 of them on an orbit seed — 119 on `sym90_a`, 114 on `sym90_b`,
and 0 ever on `sym94.json`.** Every orbit-seeded descent in this fleet therefore
started from Jean-descended material. Fixed 2026-07-29 10:07, 28 minutes after
this find; see the note in `code/orbit_runner.py`.

## What the circuit is

88 gates at **depth 5** — two levels shallower than the published 88 @ depth 7
and, at 88 gates, six fewer than the published depth-5 point (94 gates,
Osvik–Canright, ePrint 2024/1076). Independently recomputed from the raw JSON
against a locally rebuilt GF(2⁸) spec: 88 gates, depth 5, 32/32 outputs,
**0 dead gates**, 0 duplicate masks, 0 forward references. 71 of its 88 masks are
ρ²-symmetric (80.7 %; periphery 39/56 = 69.6 %).

**It is not a new family.** Jaccard on mask sets (threshold J ≥ 0.7 = same
family):

| against | shared | Jaccard | periphery-only J |
|---|---|---|---|
| our record **89 @ d5** | 75 / 89 | **0.735** | 0.614 |
| our ρ²-symmetric 94 @ d5 | 76 | 0.717 | — |
| our 88 @ d8 (family 3) | 67 | 0.615 | 0.455 |
| our 88 @ d7 (family 1) | 63 | 0.558 | 0.383 |
| Jean's 88 (family 2) | 62 | 0.544 | 0.366 |
| Sun–Yang–Li's 89 | 61 | 0.526 | 0.345 |
| our 88 @ d6 (family 4) | 42 | 0.313 | 0.098 |

At 0.735 to the record 89 @ depth 5 it sits **above** the same-family threshold,
and closer to that 89 than to any 88. The honest description is therefore: **the
record-89 basin reached at 88 gates, and the shallowest 88 this project holds** —
not a fifth family.

## The run

| | |
|---|---|
| what | the multi-day **87-hunt** fleet (`campaign_87/hunt87/supervisor.py`): 15 search workers + the k=2 detector, one shared harvest directory |
| this instance | launched 2026-07-27 **22:22:30**; the find is 35.3 h in |
| producing workers | **`o1`** (ρ²-equivariant orbit ladder) then **`o_polish`** (desymmetrise-and-polish: it reads the orbit workers' saved circuits as plain mask sets and runs the unconstrained engine on them) |
| the record | `FOUND_88gates_depth5.json` — **byte-identical** (sha256 `bff7b927269f2b59…`) to `runs/o_polish_best.json` as saved by the worker. Canonical copy: `../circuits/mixcolumns_88gates_depth5.json`. |
| harvest cross-check | the record's exact mask set is line 81 of `campaign_87/hunt87/runs/o_polish.pop.jsonl` (re-checked 2026-07-29) |

The descent, verbatim from the two worker logs:

```
runs_hunt/o1.log
[116106.2s 06:37:36] --- cycle 129: seed=sym90_a.json mode=sym rng=2101129 ---

runs_hunt/o_polish.log
[126918.0s 09:37:48] --- restart 71 from o1_c129_90g.json (rng seed 9841) ---
[126964.1s 09:38:34] [walk] 46s iters=20000 cur=90 best=90 harv=0
[127003.3s 09:39:14]   NEW BEST 88 gates depth 6 VERIFIED it=38447 -> o_polish_best.json
[127007.5s 09:39:18]   NEW BEST 88 gates depth 5 VERIFIED depth-tiebreak it=40419 -> o_polish_best.json
```

90 → 88 in **85.3 s** of walk from the restart, then the Pareto depth tie-break
carried the same size from depth 6 to **depth 5 4.2 s later**. Both came from a
**walk** chunk. The 88 at depth 6 in the second-to-last line is an intermediate of
*this* descent, not the family-4 circuit of
`../campaign87_run_2026-07-28_got_88at6_fromscratch/`; it was superseded 4.2 s
later and is not separately archived. The worker went on for a further 5 h 51 min
(twelve more roots, best 88 → 89) without finding an 87, until the 2026-07-29
15:35 fleet shrink retired it.

## Exact neighbourhood certificates for this circuit

| radius | windows | verdict |
|---|---|---|
| k = 2 (remove 2, restore with ≤ 1) | all **1 540** = C(56,2) | **all irreducible, shell exhaustively empty** |
| k = 3 | **not swept** | — |

The k = 2 sweep (verdict log in `certificates/`) used the repo's own archived
decider, `../campaign87_certificates/code/exact_window.py`, whose budget-1 search
is exhaustive by the proof in its docstring — so it is a proof for that radius:
**any 87 differs from this circuit by ≥ 3 masks.** Nothing here bounds 87 away
globally.

Its k = 3 shell was never run; together with this project's 88 @ depth 7 — which
has no exhaustive shell at any radius — it is one of the two least certified
circuits in the repository. The sweep is a few minutes of CPU (see
`certificates/README.md`).

## Depth obstruction

The masks whose minimum build depth equals the circuit depth are output rows
**1, 3, 8, 17, 19, 25 and 27** — the same kind of wall the record 89 @ depth 5
runs into (rows 1, 4, 11, 17, 19, 20, 25), which is consistent with the two
sharing a basin.

## What is in this archive

- `FOUND_88gates_depth5.json` — the record, exactly as saved by the worker.
- `seed_orbit_90gates_depth9_derived.json` — the seed handed to `o_polish`
  restart 71 (= `runs/o1_c129_90g.json`, oracle-verified 90 @ depth 9). **Derived
  from published work**, as above.
- `runs_hunt/o_polish.log`, `runs_hunt/o1.log` — both producing workers'
  **untouched** logs.
- `runs_hunt/o2.log` — the fleet's **second** orbit ladder, untouched. It produced
  nothing on this chain and is kept only so the seed-rotation count below re-derives
  from this archive alone: across `o1.log` + `o2.log` there are 345 cycles, 233 of
  them on an orbit seed (119 `sym90_a`, 114 `sym90_b`, **0** ever on `sym94.json`).
- `code/` — the engine, the hunt worker and the orbit machinery, with
  `CODE_PROVENANCE.md` and `CONFIG_AS_RUN.md`.
- `certificates/` — the k = 2 shell verdict log and the sweep driver.

## What is NOT in this archive

The harvest files and the 1 275 per-cycle orbit circuits under
`campaign_87/hunt87/runs/o?_c*_*g.json`, of which only cycle 129's is kept here.
Referenced instead:

| file | size | sha256 | lines |
|---|---|---|---|
| `campaign_87/hunt87/runs/o_polish.pop.jsonl` | 669 708 B | `30797164505dfdd8777d6be8b98eb74a389e2a12e52dfd2dfefd4301eee5932d` | 729 (this record's mask set is line 81) |
| `campaign_87/hunt87/runs/*.pop.jsonl` (all 16 workers) | 868 MB total | — | the fleet's whole harvest, still growing |

## Re-verify

```
python3 ../../verify_circuit.py FOUND_88gates_depth5.json 5   # VALID
python3 ../../verify_circuit.py FOUND_88gates_depth5.json 4   # INVALID: depth 5 is tight
python3 ../../verify_circuit.py seed_orbit_90gates_depth9_derived.json 9
```

Outputs at the time of archiving:

```
gates=88 depth=5 outputs_built=32/32 problems=0 ; depth<= 5: OK ; VERDICT: VALID MixColumns circuit
gates=88 depth=5 outputs_built=32/32 problems=0 ; depth<= 4: VIOLATED ; VERDICT: INVALID
gates=90 depth=9 outputs_built=32/32 problems=0 ; depth<= 9: OK ; VERDICT: VALID MixColumns circuit
```
