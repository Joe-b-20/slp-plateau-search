# CONFLICTS RESOLVED — referee pass over METHOD_CATALOG Appendix B and MANIFEST §9

Agent: CONFLICT REFEREE (wrap-up wave 3). Date: **2026-08-29**.
Method: every verdict below is re-derived from a **primary source** — an
append-only ledger, a raw artefact, or a computation I ran myself in this
session — never from a slice report or from another wrap-up document. Where a
slice report and a ledger disagree, the ledger wins. Where a claim could be
re-measured cheaply, it was re-measured rather than read.

Scope: 11 Appendix B conflicts + 14 MANIFEST §9 count families + 10 load-bearing
`CORRECTIONS.md` spot-checks. Read-only everywhere; this file is the only write.
`fleet11/laneCUBE`, `fleet8/unified`, `fleet12/laneHALO` were opened read-only.

**Tally: 22 resolved · 4 both-right-different-objects · 3 partially resolved
(named residue below) · 0 fully unresolved.**

**POSTSCRIPT 2026-09-01: k=14 decided UNSAT — see `fleet11/laneCUBE/RESULT.md`
§7.1.** The tallies in §B8 (and the rows citing it, §C4 and the summary tables)
are left exactly as measured on 2026-08-29; they are a correct record of an
unfinished sweep, not the status of the level.

---

# ⚠ READ FIRST — what could NOT be fully closed, and what it would take

| # | residue | why it is open | what would close it |
|---|---|---|---|
| **R1** | Appendix B #4 (gauge components). Verdict is *both right, different objects* — but the two instruments agree **exactly** at 88@5 (729), 88@5fs (2,187) and 88@6 (10,935) and then diverge 4.2× and 14.2× at 88@7 and 88@8. Under "different objects" the agreement at three of five anchors is a coincidence I did not explain. | Explaining it needs the mask-set projection of e14's wiring orbit, which is not banked. | Re-run `experiments/e14_plateau87/basis/d7only.py` with the state key changed from `key()` (operand-mask pairs) to `tuple(sorted(masks))`, and check the projected set against `beat88/methods/shared/gauge.py:orbit_bfs`. ~5 min of one core at d5/d6; ~15 min at d7. **Predicted: e14's projection ⊆ m1's component, strictly at d7/d8.** Until run, do not assert set-containment in public. |
| **R2** | The **≈165 M** window-decision total. The k=2 half is now re-tallied at **215,412,120** from three append-only ledgers (below, §B5/§S7), which already exceeds the published campaign-wide total. But the published 165 M is described as "no double counting" across four producers, and I did not re-derive the `exact_window/` (~113 k) and `exact_k4/` (~16.8 M) components. | I can prove the published total is a **stale under-count**; I cannot yet certify a replacement grand total. | Re-tally `exact_window/` and `exact_k4/` from their own ledgers and check for key overlap with `results_pop`/`results_f3`. Until then quote the **k=2 figure alone** (215,412,120, ledger-exact) and drop "≈165 M" rather than replacing it. |
| **R3** | MANIFEST §9.11 (e5 drop-4). The **screen** is complete on **both** circuits — `screen_done` rows exist for `88d5` (8,205 screened + 27,754 counting) and `88fs5` (13,315 + 22,645 = 35,960 exactly). But only `88d5` has a banked **refutation** statement, and `88fs5`'s W-histogram contains 15 sets at `W = 0` and 430 at `W = 1`, where "refuted at `k = W−1`" is vacuous or ill-posed. | The ledger banks coverage, not a per-circuit verdict, for `88fs5`. | Quote the complete-refutation claim for `88d5` only. `88fs5` may be quoted as "all 35,960 drop-4 sets screened", not "refuted". |
| **R4** *(minor)* | MANIFEST §9.10's breakdown of fleet9's 223 — "6 ρ-images, 1 self-test, only 60 both non-census and non-record" — was **not** re-derived. The **223** itself is confirmed exactly (§S9). | Needs a census join I did not run. | Join fleet9's 223 canon hashes against `wrapup/corpus88_index.jsonl` (`in_e15_census`, `sources`). Minutes. |

Everything else below is closed.

---

# PART A — METHOD_CATALOG.md Appendix B, conflicts 1–11

---

## B1 — `L_cf(M)` upper bound: **103** vs **102** vs 104 vs 133

**Claim A.** `L_cf(M) ≤ 103`, CP-SAT, closure-verified, "the first upper bound
on `L_cf` in this project" — `fleet6/laneTOOL2/RESULT.md:152, 738–758`, artefact
`fleet6/laneTOOL2/results/lcf_cpsat.json`.
**Claim B.** `L_cf(M) ≤ 102`, oracle-verified explicit witness —
`beat88/understanding/v2_no_vocab/data/cf_incumbent.json`, re-verified by
`fleet7/laneUNCOND/RESULT.md:129, 1006` ("laneTOOL2's 103 is a one-gate
regression, not a first").

**Primary evidence I checked.** I replayed the 102-gate witness myself from raw
JSON — not through anyone's wrapper:

```
python3 -c "... json.load('beat88/understanding/v2_no_vocab/data/cf_incumbent.json') ...
            replay sig, count gates with sig[a] & sig[b] != 0, check targets"
-> gates 102
-> targets covered 32 of 32
-> cancelling gates kappa = 0
-> depth 5
```

A cancellation-free SLP is exactly one where every gate's two operand masks have
disjoint support; `kappa = 0` is that condition, measured directly. The witness
is real, complete and cancellation-free.

**Verdict.** **102 is right. 103 is a one-gate regression, not a competing
bound.** laneTOOL2 ran a fresh CP-SAT search unaware of the standing incumbent
and reported its own (worse) feasible solution as a first upper bound; the
incumbent predates it. 104 (an unextracted incumbent) and 133 (a referee's
circuit) are older and weaker still. The lower end `L_cf(M) ≥ 92` (CANON U6-2)
is used as given by both lanes and is not touched by this.

**Uncorrected at source:** `fleet6/laneTOOL2/RESULT.md:152, 750, 792, 829`.

> **PUBLIC-SAFE:** `92 ≤ L_cf(M) ≤ 102`. The upper bound is an explicit
> 102-gate cancellation-free circuit (`kappa = 0`, all 32 MixColumns targets,
> depth 5), independently re-verified 2026-08-29. Do not quote 103, 104 or 133.

---

## B2 — residual-LP integrality gap: **"≥ 5"** vs **"≤ 0.5351"** *(catalog said UNRESOLVED — it is resolvable)*

**Claim A.** Proven integrality gap `≥ 5` on `88@5fs`, route ceiling 83.000 —
`fleet2/laneP_proof/RESULT.md:113, 450–480, 678`, with a referee's exact
`Fraction` dual of **exactly 34** against `|counted| = 39`.
**Claim B.** That is a misattribution; true gap `≤ 0.5351` —
`fleet6/laneTOOL2/RESULT.md:102–107, 461–481`.

**Primary evidence I checked.** `fleet6/laneTOOL2/ledger.jsonl`, `kind:
phi_calibration` rows (append-only, 10 rows) — not the prose:

| circuit | `phi_lower` | `phi_upper` | `exact` | `counted` | `laneP_B` (LP dual) | `gain_over_LP` |
|---|---:|---:|---|---:|---:|---:|
| 88@7 | 35 | 35 | true | 35 | 35.000 | 0.000 |
| **88@5fs** | **34** | **34** | **true** | **39** | **33.462** | **0.538** |
| 88@5 | 43 | 43 | true | 43 | 42.666 | 0.334 |
| 88@6 | 30 | 30 | true | 31 | 29.666 | 0.334 |
| 88@8 | 38 | 38 | true | 39 | 37.666 | 0.334 |
| 89@5 | 47 | 47 | true | 47 | 46.666 | 0.334 |
| 91@4a | 52 | 52 | true | 52 | 50.979 | 1.021 |
| 91@4b | 47 | 47 | true | 48 | 45.767 | 1.233 |
| 92@4 | 50 | 50 | true | 54 | 48.866 | 1.134 |

and the controls, `kind: planted_control` (7 rows): on the referee's **own**
planted 5-bit integrality-gap instance the tool returns `Phi = 8` by CP-SAT
(status `OPTIMAL`, `verified: true`) **and** by independent brute force, against
an exact LP dual of `15/2` — `two_methods_agree: true`, `verdict: FIRED`. The
control can fail and did not.

**Verdict.** **Claim B is right; Claim A mislabels a real quantity.** Both lanes
agree the exact LP dual on `88@5fs` is **34**. The disagreement is over what the
*integral* optimum `Phi(A*)` is:

- Lane P **assumed** `Phi(A*) = |counted| = 39` (via Lane C's "the
  cancellation-free layer is exactly optimal for its own required outputs") and
  therefore read `39 − 34 = 5` as an integrality gap.
- laneTOOL2 **measured** `Phi(A*) = 34`, exactly, with matching lower and upper
  bounds and a positive control. So the integrality gap is `34 − LP ∈ [0, 0.5351]`.

The number 5 is real but is `|counted| − Phi(A*)` — the record circuit's clean-layer
**suboptimality**, not an LP–IP gap.

**Two consequences neither lane's headline states.**
1. **Lane P's 83.000 ceiling STANDS and is strengthened** — it survives replacing
   the dual by the exact integral optimum (`88 − (39 − 34) = 83`).
2. **Lane C's claim is falsified on 3 of 5 canonical 88s.** `phi_equals_counted`
   is `false` for 88@5fs (34 vs 39), 88@8 (38 vs 39) and 88@6 (30 vs 31).

> **PUBLIC-SAFE:** The residual covering LP is essentially integral: the exact
> integral optimum exceeds the LP by less than 1.15 on all nine measured
> circuits, and by at most 0.5351 on `88@5fs`. The separately-reported "gap ≥ 5"
> is the record circuit's clean-layer suboptimality (`|counted| − Φ(A*) = 39 − 34`),
> not an integrality gap. The 83.000 route ceiling on `88@5fs` is unaffected.

---

## B3 — reachability grid: **137 cells** vs **138 rows**

**Claim A.** 137 cells: 33 VALID / 17 INFEASIBLE / 75 ELSEWHERE / 12 UNDECIDED —
`fleet8/unified/RESULT.md:530–534`.
**Claim B.** 138 rows / 13 UNDECIDED — the live `results/reach_grid.jsonl`.

**Primary evidence I checked.** `wc -l fleet8/unified/results/reach_grid.jsonl`
→ **138**; re-tally of the `status` field →
`{VALID: 33, INFEASIBLE: 17, ELSEWHERE: 75, UNDECIDED: 13}`. File mtime
2026-08-25 00:28.

**Verdict.** **The ledger is right: 138 / 13 UNDECIDED.** Exactly one UNDECIDED
row was appended after the write-up; the other three counts are byte-identical
between the two sources, which is what a one-row append predicts and is itself a
control on the reading.

> **PUBLIC-SAFE:** 138 reachability cells probed: 33 VALID, 17 INFEASIBLE,
> 75 ELSEWHERE, 13 UNDECIDED (`fleet8/unified/results/reach_grid.jsonl`,
> re-tallied 2026-08-29).

---

## B4 — gauge-component sizes for 88@7 and 88@8 — **BOTH RIGHT, DIFFERENT OBJECTS** *(see R1)*

**Claim A.** "True gauge component" 88@7 = **112,833**, 88@8 = **59,697**, both
closed — `beat88/methods/m1_cartography/LEDGER.md:62`, log
`runs/escape_recheck.log`.
**Claim B.** Free-move closures **26,730** and **4,212**, both CLOSED —
`experiments/e14_plateau87/laneBASIS.md:311, 314`, `RESULT.md:44`, reproduced
independently in `basis/d7only.py` (26,730, 32 BFS levels, 261 s).

**Primary evidence I checked** — the two move definitions in code, and the
anchors:

- Both use the **same five anchor files** (`m1_cartography/bin/t_escape_recheck.py:60–66`
  `ANCHORS`; e14's `CASES`/laneBASIS) — `evidence/circuits/mixcolumns_88gates_depth{5,5_fromscratch,6,7,8_thirdfamily}.json`.
- **m1's component** is `beat88/methods/shared/gauge.py:209 orbit_bfs`, docstring:
  *"The complete neutral **remove-1-add-1** component of `state`"*, states are
  sorted **mask tuples**.
- **e14's component** is `experiments/e14_plateau87/basis/component.py:76 neighbours`
  — **re-association** and **re-parenting** only; state identity at
  `component.py:44–46` is `frozenset(frozenset((s[a], s[b])) for a,b in gates)`,
  i.e. the set of unordered operand-**mask pairs** — a **wiring/DAG**, not a mask set.

**Verdict.** **Both correct for their own object.** They differ on *two* axes,
not one:

| | m1_cartography | e14/e16 |
|---|---|---|
| state = | 88-mask **set** | **wiring** (operand-mask-pair set) |
| move = | any neutral **remove-1-add-1** | re-association + re-parenting |
| sizes (d5/d5fs/d6/d7/d8) | 729 / 2,187 / 10,935 / **112,833** / **59,697** | 729 / 2,187 / 10,935 / **26,730** / **4,212** |
| total over the five | **186,381** | **44,793** |

Re-association is a *restricted* remove-1-add-1 (it requires the removed mask's
consumer to be unique) and re-parenting is mask-set-identity, so the direction of
the divergence (m1 ≥ e14) is what the definitions predict.

**Correction to Appendix B itself:** the catalog attributes m1's component to
"union crossing, double transposition, and remove-1-add-2 / remove-2-add-1".
That is wrong — those are the **escape-test probe classes** (MC-B / MC-C), which
`t_escape_recheck.py` classifies *against* the component; they do not build it.
The component move is remove-1-add-1.

> **PUBLIC-SAFE:** Never write "the closed component" without its move set and
> its state object. Two correct forms:
> *"Under the complete neutral remove-1-add-1 move on mask sets, the five record
> 88s lie in closed components of 729 / 2,187 / 10,935 / 112,833 / 59,697 states."*
> *"Under the two free moves (re-association, re-parenting) on wirings, they lie
> in closed components of 729 / 2,187 / 10,935 / 26,730 / 4,212 wirings —
> 44,793 in total, containing zero 87s."*
> Do not present 44,793 and 186,381 as competing measurements of one thing.

---

## B5 — `n_components ≥ k`: **"60 of 62"** vs **"FALSE, 8 of 204"**

**Claim A.** Holds in 60 of 62 profiled families —
`beat88/methods/m5_backbone` (PHASE2 §1b).
**Claim B.** FALSE — 8 of 204 violate —
`beat88/understanding/u1_obligations/NOTEBOOK.md:357–380`.

**Primary evidence I checked.** `u1_obligations/NOTEBOOK.md:335–345`, the
measured distribution over the 204-family corpus:

```
families 204
identity (all obligations)     ok = 204 / 204
identity (needed obligations)  ok = 204 / 204
n_components − k : −2:2  −1:6  0:40  +1:53  +2:37  +3:36  +4:20  +5:8  +6:2
```

I re-added it: `2+6+40+53+37+36+20+8+2 = 204` ✓, and the negative bins are
`2 + 6 = 8` ✓ — the violator count is the histogram's own left tail, not a
separate assertion. All eight are named individually with mechanism
(`NOTEBOOK.md:363–372`), and three independent artifact-checks are recorded
(`n_needed` recount gives 9 violators, not 0; slot-degeneracy excluded; the
mechanism exhibited gate-by-gate, e.g. `00010203 ⊕ 83800001 = 83810202`).

**Verdict.** **The conjecture is FALSE.** Both counts are correct for their own
corpus — 2 of 62 in PHASE2's smaller corpus, 8 of 204 in the full one — so 60/62
was never evidence *for* the invariant; it was 2 counterexamples already.
The surviving statements, both verified in the primary source:

- `k = Σ m_j` and `k − n = surplus − free`: **204/204**, no fitted parameter.
- `n_expensive ≥ 1`: **203/204** (`PROOFCHECK.md:653–655`).
- `n_expensive ≥ 1 ∨ cover ≥ k`: **204/204** (`NOTEBOOK.md:674`).

**Scope word that must travel with it** (`PROOFCHECK.md:553, 665`): these are
**route closures, not obstructions** — they say a particular attack does not
work, not that 87 is blocked.

> **PUBLIC-SAFE:** The conjecture "local completability requires
> `n_components ≥ k`" is false: 8 of 204 profiled families violate it, all eight
> named with mechanism. What survives is the identity `k − n_components =
> surplus − free`, exact on 204/204 families, and the disjunction
> `n_expensive ≥ 1 ∨ cover ≥ k`, 204/204 — a route closure, not an obstruction
> to an 87.

---

## B6 — exact-window decider: **"no completeness bug"** vs **"414/450 false irreducible"** — **BOTH RIGHT, DIFFERENT INPUTS**

**Claim A.** 4,200/4,200 planted YES windows answered correctly, branch-deletion
validated (462/462 with case 1a deleted); no completeness bug; the ≈165 M
verdicts stand — `campaign_87/cert_audit`, restated
`evidence/campaign87_certificates/CERTIFICATES.md:256–261`.
**Claim B.** Defect: 414 of 450 target-containing windows returned a false
"irreducible" — `beat88/analysis/code/exact-window-code.md:149–161`.

**Primary evidence I checked.** The Claim-B source **reconciles this itself**,
in the same paragraph. `exact-window-code.md:148–161`:

> "The docstring restricts windows to *non-target* masks (l.6), but nothing in
> the code enforces it. … on 450 windows containing one target mask … the
> decider returned **414 false 'irreducible'** (92 %). Two saving graces: every
> archived sweep used non-target windows only (**window counts match `C(56,k)`
> exactly**), and the ≥ 4-mask theorem is unaffected — any valid circuit contains
> all 32 target masks, so `S \ T` for a real 87 is automatically target-free. So
> **no archived verdict is impugned**."

**Verdict.** **Both correct, disjoint inputs, and already reconciled at source.**
Claim A is about the archived input class (non-target windows); Claim B is about
an input class no archived sweep ever fed it. The `C(56,k)` window-count identity
is the check that the archived sweeps really were target-free — a control that
could have failed.

**Correction to Appendix B itself:** "no document reconciles them explicitly" is
wrong; `exact-window-code.md` §4.5 does, in the sentence quoted above.

**Live hazard that IS real (do not lose it):** the module has no
`assert not (window & TSET)`, so any *reuse* over raw mask sets — move generation
over non-circuit sets — will get confidently wrong proofs. Same section also
flags `solve2`/`solve_deep` overloading `None` for both "proved empty" and
"deadline expired", resolved by re-reading `time.time()` on a box whose clock is
known to step backwards; archived sweeps report zero timeouts, so nothing archived
is impugned, but any rerun must use `time.monotonic()`.

> **PUBLIC-SAFE:** The archived exact-window verdicts stand: the decider was
> validated on 4,200 planted YES windows (4,200/4,200 correct, every witness
> oracle-verified; 462/462 with the first proof branch deleted), and every
> archived sweep used non-target windows only, confirmed by the window counts
> matching `C(56,k)` exactly. The decider is **unsound on windows containing a
> target mask** — an input class no archived sweep used — and must not be reused
> on raw mask sets without that guard.

---

## B7 — the published depth-4 record: **92 @ 4** vs **91 @ 4** — **91 IS RIGHT; HEADLINE CHANGE**

**Claim A.** 92 @ depth 4 — `README.md:44, 86`; `evidence/RESULTS.md:1, 59, 98–122, 866`;
`evidence/circuits/spectrum.json:11`; `~/xor_ui/aes_mc_records/PAPER.md:26, 44, 89, 97, 167, 182, 192`;
`pipeline/README.md`; `reproduce/README.md:17`.
**Claim B.** 91 @ depth 4, three independent lineages.

**Primary evidence I checked — I ran the repo's own oracle on all three:**

```
python3 verify_circuit.py campaign_87/cascade6/FRONTIER_91gates_depth4.json
  -> gates=91 depth=4 outputs_built=32/32 problems=0   VERDICT: VALID MixColumns circuit
python3 verify_circuit.py experiments/e4_depth/out/resched/atlas_compiled_m1_91gates_depth4.json
  -> gates=91 depth=4 outputs_built=32/32 problems=0   VERDICT: VALID MixColumns circuit
python3 verify_circuit.py fleet2/laneG_generator/referee/results/ref_91g_d4.json
  -> gates=91 depth=4 outputs_built=32/32 problems=0   VERDICT: VALID MixColumns circuit
```

Three further independent corroborations I checked:

1. **The published 92@4 is not itself a stripped 91.** I computed the transitive
   cone of the 32 target masks over `evidence/circuits/mixcolumns_92gates_depth4.json`:
   **92 gates, 92 live, 0 dead.** So the 91 is a genuinely better circuit, not a
   dead-gate strip of the published one. (`fleet12/laneAUDIT`'s `92@4 → 91@4`
   strip applies to `fleet8/unified/results/reg_92at4.json`, a different artefact.)
2. **A fourth and fifth lineage exist and were priced independently.**
   `fleet6/laneTOOL2/ledger.jsonl` carries `phi_calibration` rows for **`91@4a`**
   and **`91@4b`** as ordinary measured circuits (`n: 91`).
3. **Bulk siblings.** Re-tallied the four beat88 export manifests myself:
   **15,684 records at gates=91, depth=4** (15,650 in `pod_salvage/pod2`, 34 in
   `methods/m3_census/exports`). ⚠ These manifests carry **metadata only, no
   masks** (`CORPUS88.md` §7) — they are records, not independently checkable
   circuits, and must be described that way.

**Verdict.** **The public claim is understated by a gate.** 91 @ depth 4 is held
in at least three oracle-verified, mutually distinct lineages (pairwise Jaccards
0.556 / 0.433 / 0.358). A patch with exact line numbers already exists at
`fleet7/laneCONSOLIDATE/RECORDS_REPO_PATCH.md` (2026-08-24) and has not been applied.

> **PUBLIC-SAFE:** The verified depth frontier is **97 @ 3 / 91 @ 4 / 88 @ 5**.
> The depth-4 point is a 91-gate circuit at depth 4, oracle-verified
> (`gates=91 depth=4 outputs_built=32/32`), held in three independent lineages;
> it improves the published depth-4 point (97, Osvik & Canright, ePrint
> 2024/1076 App. G) by six gates. Every document still stating 92 @ 4 is stale.

---

## B8 — k=14 cube coverage: **51/528** vs **73/528** vs **87/528** — LIVE, quote with a timestamp

**Primary evidence I checked (READ-ONLY; no writes, no process touched):**

- `fleet11/laneCUBE/cubes/joint_W3U4_k14.DONE` (2026-08-26 12:21:25): the
  write-up snapshot — `unsat_cubes: 51, sat_cubes: 0, open_cubes: 477,
  coverage "51/528", status "UNDECIDED"`.
- `fleet11/laneCUBE/cubes/joint_W3U4_k14.jsonl`, **mtime 2026-08-29 08:27:05 −0400**,
  564 rows. Re-tallied by distinct cube id:

```
distinct cubes seen        : 528
distinct UNSAT cubes       : 87
distinct SAT cubes         : 0
still open (never UNSAT)   : 441
```

- The lane **is still running**: `ps` shows 1 supervisor + 16 workers,
  `code/cube16.py --k 14 --cores 16 --group 33 --cube-timeout 0 --tlim 259200
  --retry-timeouts`, started Aug 26, ~90 % CPU each.

**Verdict.** No conflict — **one monotone live run sampled at three times.**
51 (2026-08-26 12:21) → 73 (`rec` tally, undated) → **87 (2026-08-29 08:27)**.
The lane's own pre-registration binds the reading: `"partial_coverage":
"BRACKET only: 'X of 528 cubes UNSAT' -- UNDECIDED, never a refutation"`.

> **PUBLIC-SAFE:** *"As of 2026-08-29 08:27 −0400, 87 of the 528 cubes of the
> decisive k = 14 level are proven UNSAT, 0 SAT, 441 open. The level is
> UNDECIDED; this is a coverage bracket, not a refutation. The run is live."*
> Any figure quoted must carry that timestamp. Do not write "51/528" or "73/528"
> without one.

**POSTSCRIPT 2026-09-01: k=14 decided UNSAT — see `fleet11/laneCUBE/RESULT.md`
§7.1** (one monolithic kissat-4.0.4 solve, 356,321.63 core-s). The cube-coverage
figures above remain a correct record of the unfinished sweep, but they are no
longer the status of the level and must not be quoted as it.

---

## B9 — laneCUT window counts: **14,564→18,564** and **387,395→386,922**

**Primary evidence I checked.** Both errata are already applied in place, struck
but visible, with sources:

- `experiments/e13_hand87/laneCUT/RESULT.md:24–32` — `~~14,564~~ 18,564`, marked
  a one-digit transcription error, per-level table `114+216+…+11+1 = 18,564`.
  (`18,564 = C(18,6)`, arithmetically consistent.)
- `experiments/e13_hand87/laneCUT/RESULT.md:35–45` — `~~387,395~~ 386,922`.
- `experiments/e15_campaign3/laneSWEEP.md:383–400` — **three independent
  measurements against 387,395**: laneSWEEP's re-run of e13's *own unmodified*
  `adopt.py`, AUDIT3's independent catch #5, and ARCH3's prior strike.
- `experiments/e15_campaign3/LEDGER.md:211` (append-only) — R16 row banking
  386,922 with `audit3_K4_closure.json`.

**Verdict.** Both errata correct and already applied. **Neither changes a
result** — every affected row is still CLOSED with **0 compressible**.

**Refinement Appendix B lacks — the 88@7 figure has a convention:**

```
e13 adopt.py per-level sum (seed bases excluded) : 386,922
  + the 56 seed bases (laneSWEEP's counter)      : 386,978
laneSWEEP sweep.py K4 row                        : 386,978   <- exact agreement
e13 RESULT.md table                              : 387,395   <- wrong by 473
```

> **PUBLIC-SAFE:** For the 88 @ depth 7 remove-window closure: **386,922
> generated windows** excluding seed bases, or **386,978** including the 56 seed
> bases — name the convention. Closed, **0 compressible**. For the 88 @ depth 5
> from-scratch closure: **18,564** windows, closed, 0 compressible. The published
> 14,564 and 387,395 are errata, corrected in place; neither touches a conclusion.

---

## B10 — "known 88s" population sizes — **RESOLVED BY `CORPUS88.md`**

Superseded by `wrapup/CORPUS88.md`, which re-hashed every source under one
identity (sorted mask multiset). I did not re-do that work; I ran **four
independent controls** on it, and all four came out exact:

| control I computed here | corpus88 says | mine |
|---|---:|---:|
| distinct 88 mask sets, `fleet9`+`fleet10`+`fleet11`+`fleet12` | 244 | **244** ✓ |
| distinct 88 mask sets, `evidence/`+`pipeline/`+`reproduce/` | 55 | **55** ✓ |
| 88-gate rows in `atlas/corner/out/*.plat` | 504 → 498 distinct | **504** ✓ |
| `139,878 = 84,989 ⊎ 54,889`, intersection 0 | exact | **exact** ✓ (§S7) |

**Verdict.** Quote the `CORPUS88.md` tier table. The headline is **1,575,516
distinct verified 88-gate mask sets**, of which **28,796** carry a banked build
order and **92** of those are at the record depth 5. It is a **floor**: the
honest project-wide range is **1.6 M – 4.4 M** distinct.

> **PUBLIC-SAFE:** *"1,575,516 distinct verified 88-gate MixColumns mask sets
> available upon request; 28,796 of them carry a banked build order and are
> directly runnable, 92 of those at the record depth 5. This is a verified,
> deduplicated floor — two further large classes are counted but not hashed, so
> the project-wide range is 1.6 M – 4.4 M."*
> Never quote a population size without naming its object and dedup rule.

---

## B11 — `B37` price **3** vs the published **89** — B37=3 is right, and it is **not** a record change

**Claim.** `fleet12/laneHINTS` (H47) measures `B37` at 3, not the hinted 4, at
the `rec_88at7` commitment, so that configuration prices **88, not 89**.

**Primary evidence I checked.** I ran the repo oracle on the emitted circuit:

```
python3 verify_circuit.py fleet12/laneHINTS/out/step2b_rec88at7.json
  -> gates=88 depth=8 outputs_built=32/32 problems=0   VERDICT: VALID MixColumns circuit
```

`fleet12/laneHINTS/RESULT.md:123, 211` records `B37` at `|D37| = 3`: k3 SAT in
0.15 s, "BELOW — the hint was an unsound floor here". The same test at
`f4_basis` is **refuted** (k=3 UNSAT, `B37` = 4) — `RESULT.md:161, 309`.

**Verdict.** **Confirmed at one configuration, refuted at another** — the hint is
config-dependent, not globally wrong. The "89" is an **internal generator
config price**, not a public record. And Appendix B's "the published figure has
not been corrected" is **wrong**: it *is* corrected in two places —
`fleet8/unified/REACHABILITY.md:236` ("Line 111 … is stale: the true uncapped
price is 88") and `fleet12/LIBRARY.md:310` ("`rec_88at7` **88** (was published 89
— corrected by axis 2)"). What remains stale is the data row itself,
`REACHABILITY.md:111`.

**No public frontier moves:** 88 @ depth 8 is already held
(`evidence/circuits/mixcolumns_88gates_depth8_thirdfamily.json`).

> **PUBLIC-SAFE:** Do **not** put this in a public repo as a result. Internally:
> *"The `rec_88at7` configuration prices at 88, not the tabulated 89 — the `B37`
> block hint of 4 is an unsound floor at that commitment (k=3 SAT). The emitted
> 88-gate circuit is oracle-verified at depth 8. The same test at `f4_basis` is
> refuted (k=3 UNSAT), so the hint is config-dependent. `REACHABILITY.md:111` is
> still stale."*

---

# PART B — MANIFEST.md §9, the 14 conflicting count families

Items 1–4 duplicate Appendix B and are cross-referenced; 5–14 are resolved here.

| §9 item | verdict | see |
|---|---|---|
| 1. 88-gate counts across 25 sources | **RESOLVED** — `CORPUS88.md` tier table; four independent controls exact | B10 |
| 2. 17,283 vs 139,878 corpus base | **RESOLVED — both right, different objects**; 99.7 % disjoint | B10, S7 |
| 3. k=14 cube coverage | **RESOLVED** — live run, three timestamps; current **87/528**, 2026-08-29 08:27 | B8 |
| 4. depth-4 frontier | **RESOLVED — 91 @ 4**, three oracle-verified lineages; published 92 is stale | B7 |

---

## S5 — **≈165 M** window decisions vs **15,099,957** windows — different campaigns

**Primary evidence.**
`evidence/campaign87_certificates/CERTIFICATES.md:167–173` — the ≈165 M is a
2026-07 `campaign_87` total across four producers (`exact_window/` ~113 k,
`exact_k4/` ~16.8 M, `pop_decider/` ~64.1 M, `family3_exact/` ~84.0 M),
"no double counting".
`experiments/e15_campaign3/RESULT.md:154, 1020` — 15,099,957 is e15's 2026-08
`d1` window count. I re-tallied it from the append-only ledger:

```
python3 -c "sum(json.loads(l)['d1']['windows'] for l in open('sweep_ledger.jsonl'))"
-> rows 32, rows with d1.windows 32, sum 15099957     (exact)
```

**Verdict.** **Both right, different objects, different campaigns, one year
apart in method.** ≈165 M counts *k-window irreducibility decisions* over the
2026-07 population sweeps; 15,099,957 counts *`d1` windows* over 32 tier-B rows
(22 distinct circuits) in the 2026-08 e15 sweep. They must never be summed,
compared, or presented as revisions of each other. See **R2** — the ≈165 M is
additionally stale.

> **PUBLIC-SAFE:** *"15,099,957 `d(S)=1` windows over 22 distinct circuits,
> 0 compressible, 0 shared helpers"* (e15, ledger-exact) — a separate, later
> instrument from the campaign-87 window sweeps. Quote each with its campaign.

---

## S6 — **"54 known 88s under `evidence/`"** vs **"8 canonical record circuits"** — both exactly right

**Primary evidence — I counted both myself:**

```
evidence/circuits/*.json                                 -> 9 files
   = 8 circuit JSONs + spectrum.json
   the 8: 88@5, 88@5fs, 88@6, 88@7, 88@8_thirdfamily, 89@5, 92@4, 97@3
   of which 88-gate: 5

88-gate circuit JSONs anywhere under evidence/            -> 87 files
distinct 88-gate MASK SETS under evidence/                -> 54
distinct 88-gate MASK SETS, evidence/+pipeline/+reproduce/ -> 55   (= CORPUS88's figure)
```

**Verdict.** **Both right, different objects.** **8** = canonical record circuits
in `evidence/circuits/` (all gate counts; 5 are 88s). **54** = distinct 88-gate
mask sets across the whole `evidence/` subtree, most of them inside the untouched
run archives. The atlas's comparison base was the 54; `root`'s 8 is the record
set. The atlas claim *"0 of 498 corner mask-sets equal any of the 54"* holds
(`CORPUS88.md` §2.2: the single `evidence`-labelled overlap is
`reproduce/out_88hunt.json`, a reproduction output, not a record).

> **PUBLIC-SAFE:** *"8 canonical record circuits in `evidence/circuits/`
> (97@3, 92@4→91@4, 89@5, and five 88s at depths 5, 5, 6, 7, 8); 54 distinct
> 88-gate mask sets across the whole `evidence/` tree once the run archives are
> included."*

---

## S7 — campaign_87 population k=2: **finished or partial?** — **FINISHED. HEADLINE CHANGE.**

Three figures circulate for one population: **51,899 of 84,989** (`FACTS.md` §6a),
**105,801 of ≈139,878** (`root` §3, `CERTIFICATES.md:162`, and the public
`aes_mc_records/PAPER.md:146`), and **finished** (`c87` §3.3).

**Primary evidence — I re-tallied the three append-only progress ledgers
directly, including a disjointness check that could have failed:**

| ledger | rows | verdicts | distinct keys | windows (`tested`) |
|---|---:|---|---:|---:|
| `agents/frontier-exact/work/results_pop/pop_progress.jsonl` | 84,989 | `{irreducible_k2: 84989}` | 84,989 | 84,989 × 1,540 = 130,883,060 |
| `agents/frontier-exact/work/results_residue/residue_progress.jsonl` | 987 | `{irreducible_k2: 987}` | 987 | 1,519,980 |
| `agents/family3-exact/work/results_f3/f3_progress.jsonl` | 53,902 | `{irreducible_k2: 53902}` | 53,902 | 83,009,080 |
| **union** | **139,878** | **all `irreducible_k2`** | **139,878** | **215,412,120** |

```
pairwise key overlaps : 0, 0, 0
union of key sets     : 139,878
every row's `tested`  : 1540 (no other value in any of the three files)
```

Also: `results_popk3/k3_progress.jsonl` — **200 rows, all `irreducible_k3`**,
each `stats.irreducible = 27,720`; the k=3 queue is **empty**, not "181 selected
states remain".

**Verdict.** **The k=2 population sweep is FINISHED, and every circulating public
figure understates it.** 139,878 of 139,878 (100 %) of the known 88-gate
population is proven `irreducible_k2`. `51,899 / 84,989` and `105,801 / ≈139,878`
are stale mid-run snapshots. This independently reproduces `CORRECTIONS.md` C-11
row for row, and cross-confirms `CORPUS88.md` §3 (`84,989 ⊎ 54,889 = 139,878`,
intersection 0) from a completely different file set — the progress ledgers, not
the mask banks.

**Both decompositions of 139,878 are correct:**
`84,989 + 54,889` (by harvest bank) `= 84,989 + 987 + 53,902` (by sweep ledger),
since `987 + 53,902 = 54,889`.

> **PUBLIC-SAFE:** *"All 139,878 distinct harvested 88-gate mask sets are proven
> irreducible at k = 2 — 215,412,120 exact window decisions, 1,540 windows each,
> zero reducible, re-tallied 2026-08-29 from three append-only progress ledgers
> whose key sets are pairwise disjoint. The figure 139,878 is exact, not
> approximate."*
> `aes_mc_records/PAPER.md:146` ("105,801 of the ≈ 139,878") must be corrected
> **upward** to 139,878 of 139,878, and the "≈" dropped.
> ⚠ Pair it with the C-42 scope sentence (§C10) — a negative at radius ≤ 4
> carries no information about whether an 87 exists.

---

## S8 — `FACTS.md` stale k=4 tallies — **ledger figures are right**

**Primary evidence — I re-tallied every k=4 progress ledger by distinct window
index `r` and by verdict `s`:**

| ledger | published (`FACTS.md:236–238`) | ledger rows | distinct windows | verdicts | of a space of |
|---|---:|---:|---:|---|---:|
| `frontier-exact/…/results_k4/progress.jsonl` (Jean's 88) | 32,685 | **56,489** | 56,489 | `{irreducible: 56489}` | 367,290 (15.4 %) |
| `frontier-exact/…/results_k4_f3/progress.jsonl` (family-3 anchor) | 20,432 | **39,034** | 39,034 | `{irreducible: 39034}` | 367,290 (10.6 %) |
| `frontier-exact/…/results_k4_indep/progress.jsonl` (this project's 88@7) | **9** | **34,599** | 34,599 | `{irreducible: 34599}` | 367,290 (9.4 %) |

**The 39,034 vs 20,432 sub-conflict is a containment, not a disagreement.** Two
agents ran family-3 k=4 into identically-named paths. I intersected the window
index sets:

```
frontier-exact f3 : 39,034
family3-exact  f3 : 20,432
overlap           : 20,432      <- a strict subset
union             : 39,034
```

So 20,432 is an earlier snapshot of the *same* sweep in the *same* index space
(max `r` = 367,283), and 39,034 supersedes it. `results_k4_indep`'s own summary
confirms the space: `{"covered_total": 34599, "space": 367290, "coverage_pct": 9.42}`.

**Verdict.** **`FACTS.md` §6a is stale in all three cells.** Zero reducible
windows anywhere; the direction of every correction is *more* coverage.

> **PUBLIC-SAFE:** *"Exact k = 4 (remove-4/restore-≤3) coverage, re-tallied
> 2026-08-29 from the append-only ledgers: Jean's 88, 56,489 of 367,290 windows
> (15.4 %); the family-3 anchor, 39,034 (10.6 %); this project's own 88 @ depth 7,
> 34,599 (9.4 %). Every window irreducible; zero reducible."*
> Do not quote 32,685 / 20,432 / 9.

---

## S9 — fleet12's 135 88s include byte-identical duplicates — **CONFIRMED and worse than stated**

**Primary evidence — I hashed every 88-gate JSON in `fleet9`–`fleet12` and
replayed each to its mask set:**

| tree | files | distinct md5 | distinct mask sets |
|---|---:|---:|---:|
| `fleet9` | 225 | 223 | **223** |
| `fleet10` | 0 | 0 | 0 |
| `fleet11` | 1 | 1 | 1 |
| `fleet12` | **135** | **24** | **21** |
| combined | 361 | — | **244** (= `CORPUS88.md`'s fleet9-12 figure, exact) |

Per-directory inside fleet12:

```
laneF1/out       25 files -> 8 distinct md5
laneHALO/out     11 files -> 6
laneKNOBS/out    17 files -> 9
laneHINTS/out     4 files -> 3
laneLIB/out       3 files -> 3
laneORDER/out    75 files -> 1        <- all 75 byte-identical
```

**Verdict.** **Confirmed, and MANIFEST understates it twice.** (a) `laneORDER/out`
is **75 of 75** byte-identical, not "74 of the 75". (b) The gap is not "~55 %":
135 files collapse to **24** byte-distinct and **21** distinct mask sets — a
factor of **6.4**, not 1.8.

> **PUBLIC-SAFE:** *"fleet12 holds 135 88-gate circuit files but only 21 distinct
> 88-gate mask sets; all 75 files in `laneORDER/out` are byte-identical. Across
> fleet9–fleet12 there are 244 distinct 88-gate mask sets."* Never publish a
> fleet12 file count as a population size.

---

## S10 — fleet9's 223 — **223 confirmed; the 6/1/60 breakdown NOT re-derived** *(see R4)*

225 files → **223 distinct by md5 and by mask set** (identical, so the two
duplicates are exact file copies). The claimed composition — 6 ρ-images, 1
self-test, only 60 both non-census and non-record — was not re-derived here.

> **PUBLIC-SAFE:** *"223 distinct 88-gate mask sets under `fleet9`."* Do not
> publish the 6 / 1 / 60 breakdown until it is re-derived from
> `corpus88_index.jsonl`.

---

## S11 — e5 drop-4 screen: RESULT.md's one family vs "2 circuits × 35,960" — *(see R3)*

**Primary evidence.** `experiments/e5_readd/ledger.jsonl`, `kind: screen_hist`
and `kind: screen_done`:

```
screen_hist 88d5   n=35960  W-hist {2:360, 3:6372, 4:21799, 5:5376, 6:1755, 7:254, 8:42, 9:1, 10:1}
screen_hist 88fs5  n=35960  W-hist {0:15, 1:430, 2:3485, 3:10572, 4:12785, 5:6385, 6:1682, 7:527, 8:73, 9:6}
screen_done 88d5   screened 8205  + trivial_counting 27754  (= 35,959; +1 = the W=10 set, decided by the §1 cube run)
screen_done 88fs5  screened 13315 + trivial_counting 22645  (= 35,960 exactly)
```

**Verdict.** **The screen is complete on both circuits** (RESULT.md predates the
second). **But the refutation claim is banked for `88d5` only** — see R3.

**Minor discrepancy noted, not load-bearing:** `RESULT.md:73` splits `88d5` as
"8,487 by the SAT engine … 27,472 by counting"; the ledger's `screen_done` row
splits it 8,205 / 27,754. Both sum to 35,959 and neither changes the verdict —
almost certainly the two `screen_hist` rows (two runs) with different screen/count
cut-points.

> **PUBLIC-SAFE:** *"For the verified 88 at depth 5, all 35,960 four-target drop
> sets were refuted at `k = W−1` — no set of 4 output rows can be resynthesised
> from the rest of the circuit using even one gate fewer. The same screen was
> also run to completion on the 88 at depth 5 from scratch."* Do not extend the
> word "refuted" to the second circuit.

---

## S12 — e7 dim-12 tap regions: RESULT.md's **one** vs the ledger's **four** — **FOUR**

**Primary evidence.** `experiments/e7_push/ledger.jsonl`, all four
`kind: cube_verdict` rows in full:

| arm | circuit | idx | `nB` | `lower_bound_proven` | `min_gates` | verdict | control | timestamp |
|---|---|---:|---:|---:|---:|---|---|---|
| `R_88at5_R4` | 88@5 | 4 | 11 | 11 | 11 | `DECIDED_no_saving` | POSITIVE (verified 11-gate program) | 2026-08-18T22:05 |
| `R_88at5fs_R4` | 88@5fs | 4 | 11 | 11 | 11 | `DECIDED_no_saving` | POSITIVE | 2026-08-18T22:59 |
| `R_JEAN88_R4` | JEAN88 | 4 | 11 | 11 | 11 | `DECIDED_no_saving` | POSITIVE | 2026-08-18T23:40 |
| `R_p88_05_R3` | p88_05 | 3 | 11 | 11 | 11 | `DECIDED_no_saving` | POSITIVE | 2026-08-19T01:22 |

`RESULT.md` mtime **2026-08-18 22:36**; `ledger.jsonl` mtime **2026-08-19 01:22**.
The write-up predates three of the four verdicts, and `RESULT.md:378, 423` shows
the other three were *queued* in exactly the order the ledger records them
completing (`code/regionq.sh '88@5fs:4' 'JEAN88:4' 'p88_05:3'`). The queue
finished; nobody updated the document.

**Verdict.** **Four decided regions, not one.** Each carries its own positive
control (a verified 11-gate in-region program), so the "exactly optimal" reading
is controlled in all four.

> **PUBLIC-SAFE:** *"Four dimension-12 tap regions are decided exactly optimal:
> `min_gates = |B| = 11` in each, all cubes UNSAT below 11, each with a positive
> control (a verified 11-gate in-region program) — regions R4 of the 88 @ depth 5,
> the 88 @ depth 5 from-scratch, and Jean's 88, plus R3 of `p88_05`."*
> Do not write "the first one" or "one decided region".

---

## S13 — atlas's own 88-structure claims vs its own corner output — **REFUTED, reproduced here**

**Claims under test** (`atlas/thinktank/ideas_strange_corners.md:76–79, 244, 412`;
`audit_inference.md:352`; `ideas_basin_atlas.md:167`; `NOTEBOOK.md:795`):
an `l3 ≥ 67` floor · the band `l3 ∈ 69..72` empty of known circuits · a "real
2-gate ridge" separating two basins.

**Primary evidence — I computed `l3` myself** over every 88-gate row of
`atlas/corner/out/*.plat`, using atlas's **own** `corner/socle.py:l3_of`
(unmodified) so the definition is theirs, not mine:

```
88-gate plat rows processed: 504          (matches CORPUS88's 504 -> 498 distinct)
l3 range: 64 -> 79
l3 histogram: {64:2, 65:9, 66:17, 67:8, 68:24, 69:36, 70:16, 71:6, 72:12,
               73:51, 74:86, 75:42, 76:59, 77:67, 78:57, 79:12}
gaps in 64..79: []      (every integer value is occupied)
```

**Verdict.** **All three claims are refuted by atlas's own unanalysed output.**

- `l3 ≥ 67` floor: **false** — 28 rows sit below 67 (2 at 64, 9 at 65, 17 at 66).
- band `l3 ∈ 69..72` empty: **false** — **70 rows** occupy it (36/16/6/12).
- the "2-gate ridge": there is **no gap** to be a ridge; `l3` runs continuously
  64 → 79 with every value occupied.

> **PUBLIC-SAFE:** Publish **none** of the `l3 ≥ 67` floor, the empty
> `l3 ∈ 69..72` band, or the "real 2-gate ridge". Publishable instead:
> *"Over 504 88-gate circuits from the corner sweep, the socle-skeleton size
> `l3` runs continuously from 64 to 79 with every integer value occupied —
> the previously reported floor and empty band were artefacts of a ~15-point
> sample drawn only from record circuits."*

---

## S14 — atlas V1.5 corpus incompleteness — **CONFIRMED by atlas's own notebook**

`atlas/NOTEBOOK.md:954`: `m1_v15_results/: 34,112 of ~242k (corpus INCOMPLETE; …)`.
`NOTEBOOK.md:735` describes the launched corpus as "236k instances".

**Verdict.** **Confirmed: the V1.5 corpus is ~14 % complete.** The two
denominators (236,088 vs "~242k") are the launched-corpus size versus a rounded
notebook restatement; the numerator 34,112 and the INCOMPLETE flag are atlas's own.

> **PUBLIC-SAFE:** *"The V1.5 (triple/unit currency) corpus is incomplete —
> 34,112 of ~236,000 instances solved."* The word "exhaustive" must never be
> applied to it. The separate result **"V1.5 class optimum = 91"**
> (`NOTEBOOK.md:762`) is a statement about the solved class, not the corpus, and
> is unaffected.

---

# PART C — `CORRECTIONS.md` spot-verification, the 10 most load-bearing

| # | correction | verification | verdict |
|---|---|---|---|
| C1 | **C-11**, campaign_87 population understated | re-tallied all six progress ledgers independently (§S7, §S8); every row of C-11's table reproduces exactly | **CONFIRMED, row for row** |
| C2 | depth frontier **91 @ 4** | ran the oracle on all three circuits; 3/3 VALID at gates=91 depth=4 (§B7) | **CONFIRMED** |
| C3 | published 92 @ 4 is not a stripped 91 | computed the target cone of `evidence/circuits/mixcolumns_92gates_depth4.json`: **92 gates, 92 live, 0 dead** | **CONFIRMED — the 91 is a better circuit, not a strip** |
| C4 | **k=14 coverage 87/528** | re-tallied `joint_W3U4_k14.jsonl` by distinct cube id; 87 UNSAT / 0 SAT / 441 open, mtime 2026-08-29 08:27:05, 17 live processes (§B8) | **CONFIRMED, timestamped** |
| C5 | population numbers (`CORPUS88.md`) | four independent controls, all exact: 244 · 55 · 504 · `84,989 ⊎ 54,889 = 139,878` (§B10) | **CONFIRMED** |
| C6 | **C-42**, the LR ≈ 1.00 repricing — **scope** | see §C10 below | **CONFIRMED, with a scope fence** |
| C7 | **C-25 item 1**, "shared-helper rows: one → SIX" | re-tallied `shared_helpers` over all 17,283 rows of `sweep_A_fullpop.jsonl`: `{0: 17277, 1: 4, 3: 2}`, and the six filenames match C-25's list exactly | **CONFIRMED exactly** |
| C8 | **C-25 item 2**, "`d(S)=1` uncovered ~16,800 → 17,266" | re-derived from `sweep_ledger.jsonl`: 32 rows → **22 distinct paths** → **5** under `aes_mc_records/circuits/` → **17** population circuits ⇒ `17,283 − 17 = 17,266`; `compressible_total` sums to **0**, all 32 `VALID88` | **CONFIRMED exactly** |
| C9 | **C-25 item 3**, depth-14 provenance 12 of 13 | not re-derived (lowest public value of the ten) | **not checked** |
| C10 | `CORPUS88.md`'s "e15 Run A is 1.1 %, not every 88" | `wc -l wrapup/corpus88_index.jsonl` → **1,575,516**; `17,283 / 1,575,516 = 1.1 %` | **CONFIRMED** |

## C10 (detail) — the exact scope of the **LR ≈ 1.00** repricing

This is the single most dangerous number to over- or under-apply, so its scope is
fenced explicitly.

**What I verified.** `campaign_87/wave5_2026-08-04/metareview/optimality/differential_by_length.json`,
1,200 sampled states per length:

| gates | `options_per_gate_mean` | `dead_gate_states` |
|---:|---:|---:|
| 88 | 2.3236 | 0 |
| 89 | 2.3238 | 0 |
| 90 | 2.3262 | 0 |
| 91 | 2.3205 | 0 |
| 92 | 2.3123 | 0 |

Identical to ~4 significant figures across 88–92. An instrument that returns the
same value on an optimal circuit and a four-gates-too-big one has likelihood
ratio ≈ 1 about optimality. Corroborated by the second instrument
(`experiments/e17_pure/laneDELTA/RESULT.md:58, 376`; `LEDGER.md:275`) and by the
control audit already published in
`evidence/campaign87_certificates/CERTIFICATES.md:236–248` (the same decider says
"irreducible" about 97-, 94-, 92-, 91-, 90-, 89- and 88-gate circuits alike;
real improvements need **median 42** masks, **44 of 45** transitions need `k ≥ 8`,
against a certified radius of 3).

**What LR ≈ 1.00 DOES cover** — every *negative / rigidity / "nothing better
nearby"* instrument used as evidence about whether an 87 exists: empty k ≤ 4
shells, empty move-class neighbourhoods, derivation-rigidity and dead-gate
statistics, the mutation sweeps.

**What it does NOT cover — do not let the repricing over-reach:**
- The certificates themselves remain **true**; only the inference from them is
  repriced. An exhaustively empty shell is still an exhaustively empty shell.
- **Lower bounds are proofs, not evidence**, and are untouched: `L(M) ≥ 56`
  (refereed, unconditional), `L_cf(M) ≥ 92` (CANON U6-2, solver-free), the
  depth-3 floor `≥ 80`.
- **Upper bounds are witnesses**, and are untouched: every verified circuit.
- The **B = 56 tripwire** is a theorem with a decision rule, not a rigidity
  statistic; it is not repriced.

> **PUBLIC-SAFE (use verbatim wherever a certificate is quoted):**
> *"A negative at radius ≤ 4 carries no information about whether an 87 exists.
> These are locality theorems — rigidity statements about small, completely
> enumerated neighbourhoods — not bounds. By this instrument an optimal circuit
> and a four-gates-too-big circuit are indistinguishable: derivation richness and
> dead-gate count are identical to four significant figures at 88, 89, 90, 91 and
> 92 gates. The honest bracket is `56 ≤ L(M) ≤ 88`."*
> Additional inversion to fix wherever it appears: against a proper null, real
> 88s are **4.7× more derivation-RICH, not rigid** — the "2.3 vs 64 options/gate"
> rigidity framing is backwards.

---

# PART D — resolutions that CHANGE a headline number the MANIFEST currently carries

| MANIFEST §0 row | currently says | after this pass |
|---|---|---|
| **Biggest sweep — window decisions** | "≈165 M exact window decisions campaign-wide" | **STALE UNDER-COUNT.** The k = 2 half alone is **215,412,120**, ledger-exact and disjointness-checked (§S7). Replace with the k=2 figure; do not state a new grand total until R2 is closed. |
| **Biggest sweep — population** | "17,283 / 17,283 distinct 88 mask-multisets swept" | **Correct for its object, wrong as framed.** 17,283 is *the individually-exported `*88gates*.json` files*, = **1.1 %** of the 1,575,516 corpus, and **92 % of it is one method's output** (NRPA). The project's largest population sweep is the k=2 sweep at **139,878 states / 100 %** (§S7). |
| **k = 14 still running** | "51/528 · 73/528 · 87/528 — disagree" | **Not a disagreement**: one live run, three timestamps. Current **87/528 UNSAT, 0 SAT, 441 open, UNDECIDED, as of 2026-08-29 08:27 −0400** (§B8). |
| **Depth frontier / depth-4 point** | frontier row already says 91 @ 4; a second row says "public repos still state 92 @ 4" | **91 @ 4 confirmed by oracle, 3/3**, and the published 92 @ 4 is *not* a dead-gate artefact (0 dead gates). Delete the hedge; the public repos are simply a gate behind (§B7). |
| **Biggest export corpus** | "1,549,319 records across **three** hosts (1,530,095 at 88 gates, incl. 167 at depth 5)" | **Right for three manifests; there are four.** All four: **1,549,415 rows / 1,530,179 at 88 gates / 167 at depth 5 / 15,684 at 91 @ 4**. The fourth (`exports/from_pod/MANIFEST.jsonl`) holds exactly 96 rows (84 at 88, 12 at 89) — `1,549,319 + 96` and `1,530,095 + 84` reconcile to the digit. ⚠ These rows carry **metadata only, no masks**. |
| §9 conflict list | 14 families "DEDUP PENDING / recorded, not resolved" | **All 14 now have a verdict** (Part B). Four are *both right, different objects*; the rest resolve to one number. |

---

## Appendix — every command this referee ran

All read-only, all `nice -n 19` where they did real work, no process started, no
file written outside `wrapup/CONFLICTS_RESOLVED.md`.

```
# B1  cancellation-free witness, replayed from raw JSON
python3 -c "... cf_incumbent.json -> 102 gates, kappa=0, 32/32 targets, depth 5"

# B2  banked exact integral optima and their controls
python3 -c "... fleet6/laneTOOL2/ledger.jsonl kind in {phi_calibration, planted_control}"

# B3  reachability grid
wc -l fleet8/unified/results/reach_grid.jsonl                 -> 138
python3 -c "... Counter(status) -> VALID 33 INFEASIBLE 17 ELSEWHERE 75 UNDECIDED 13"

# B4  move definitions read in code
beat88/methods/shared/gauge.py:209   orbit_bfs  (remove-1-add-1, mask sets)
experiments/e14_plateau87/basis/component.py:44,76  key/neighbours (wirings)

# B7  the depth-4 frontier
python3 verify_circuit.py {campaign_87/cascade6/FRONTIER_91gates_depth4.json,
   experiments/e4_depth/out/resched/atlas_compiled_m1_91gates_depth4.json,
   fleet2/laneG_generator/referee/results/ref_91g_d4.json}     -> 3/3 VALID 91@4
python3 -c "... target cone of evidence/circuits/mixcolumns_92gates_depth4.json -> 0 dead"

# B8  laneCUBE, READ-ONLY
ls -la --time-style=full-iso fleet11/laneCUBE/cubes/joint_W3U4_k14.jsonl
python3 -c "... distinct cube ids -> 528 seen / 87 UNSAT / 0 SAT / 441 open"
ps aux | grep cube16.py                                        -> 17 live processes

# B10/S6/S9  independent controls on CORPUS88
python3 -c "... distinct 88 mask sets: fleet9-12 -> 244 ; evidence+pipeline+reproduce -> 55
                ; evidence alone -> 54 ; fleet12 135 files -> 24 md5 -> 21 mask sets"

# S5   e15 d1 windows
python3 -c "... sum(d1.windows) over sweep_ledger.jsonl -> 15,099,957"

# S7   the k=2 population, from the append-only ledgers
python3 -c "... pop 84,989 / residue 987 / family3 53,902, all irreducible_k2,
                pairwise key overlaps 0/0/0, union 139,878, tested==1540 everywhere,
                windows 215,412,120"

# S8   k=4 coverage and the family-3 containment
python3 -c "... results_k4 56,489 ; results_k4_f3 39,034 ; results_k4_indep 34,599, all irreducible
                ; family3-exact f3 20,432 is a strict SUBSET of frontier-exact's 39,034"

# S12  e7 cube verdicts
python3 -c "... e7_push/ledger.jsonl kind=cube_verdict -> 4 rows, all DECIDED_no_saving"

# S13  l3 recomputed with atlas's own socle.py
python3 -c "from socle import l3_of ; 504 rows at 88 gates ; l3 64..79, no gaps"

# C7/C8  e15 audit figures
python3 -c "... shared_helpers over 17,283 Run-A rows -> {0:17277, 1:4, 3:2}"
python3 -c "... sweep_ledger 32 rows / 22 paths / 5 records-repo -> 17,283-17 = 17,266"

# C10  the LR instrument
python3 -m json.tool campaign_87/wave5_2026-08-04/metareview/optimality/differential_by_length.json

# Part D  beat88 export manifests
python3 -c "... 4 MANIFEST.jsonl -> 1,549,415 rows / 1,530,179 at 88 / 167 at 88@5 / 15,684 at 91@4"
```

*End. Written 2026-08-29 by the CONFLICT REFEREE. Every number above was
re-derived in this session from a primary artefact; where I could not re-derive
one, it is named in R1–R4 or marked "not checked" in Part C.*
