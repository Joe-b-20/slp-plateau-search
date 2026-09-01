# THE CASE THAT 88 IS OPTIMAL

## The complete evidence that `L(M) = 88` for AES MixColumns — and everything that cuts against it

**Compiled 2026-08-29, wrap-up wave 4 (`wrapup/day2`), for a researcher who has
never read this repository.** Repository root for every path below is
`/home/joebachir20/xor_ui/slp-plateau-search/`; paths prefixed
`aes_mc_records/` are the separate public artifact repository
(`~/xor_ui/aes_mc_records`).

This is the master evidence document. The short "Opinion" sections of the two
public repositories cite it; it is also intended as the skeleton of a possible
ePrint note, *Evidence on the optimality of 88*. It is deliberately longer than
anything meant to be read start to finish: it is a reference, and §6 is its
index.

**UPDATE 2026-09-01 — the one open machine decision closed.** `k = 14` on the
merged `W3 ∪ U4` block is **UNSAT** (kissat-4.0.4, one monolithic solve,
356,321.63 core-seconds ≈ 99 core-hours; `fleet11/laneCUBE/RESULT.md` §7.1). The
ladder `k = 9..14` is complete and all UNSAT, so `merged(W3 ∪ U4) = 15` exactly —
merging buys nothing — and **no 87 exists that shares the block structure of
every known 88**. This is **not** a proof that no 87 exists: an 87 outside that
block decomposition is not excluded, and the claim's status below is unchanged.
Affected: §2.4, §2.4.2, §3.5, §4.3 A14, §5 item 3, §6.2 C21/C22, §7.

---

> # THE GUARD
>
> **The refereed state of the problem is `56 ≤ L(M) ≤ 88`, and nothing in this
> document narrows it.** `L(M) = 88` is an *opinion*, held for the reasons in
> §2 and against the reasons in §3. No circuit below 88 gates has ever been
> produced by this project or by anyone else, and no argument below is a proof.
> Where a result *would* move an endpoint if a named hypothesis were proved, the
> hypothesis is named and the price is stated.
>
> Source: `experiments/e17_pure/DOSSIER.md` (THE GUARD);
> `atlas/NOTEBOOK.md` ~725–728.

---

## 0. How to read this document

### 0.1 The problem

AES MixColumns is a fixed `32 × 32` matrix `M` over `GF(2)`: byte-level
multiplication by the circulant `(2,3,1,1)` over `GF(2⁸)/0x11B`, written out
bitwise (FIPS-197). The task is to compute all 32 output bits from the 32 input
bits with as few **2-input XOR gates** as possible — a straight-line program
(SLP) over XOR only. `L(M)` is that minimum. `L_cf(M)` is the minimum over
*cancellation-free* SLPs (every gate's two operand masks have disjoint support).

Facts about `M` used throughout, each machine-checked at least three times
independently (`experiments/e17_pure/REF_ALGEBRA/VERDICT.md` §1;
`experiments/e17_pure/laneY/RESULT.md` §1;
`experiments/e17_pure/laneCHAIN/RESULT.md` §0):

* 32 rows: **20 of weight 5, 12 of weight 7**; 184 support incidences.
* Column weights `28 × 5 + 4 × 11`; the four weight-11 columns `{7,15,23,31}`
  are the **hub**.
* Rank 32 over `GF(2)`; rows pairwise distinct; minimum pairwise Hamming
  distance 4; **no row is a submask of another**; all 496 pairwise row-XORs
  distinct; columns non-zero and pairwise distinct.
* `Aut(M) = {ρ⁰, ρ¹, ρ², ρ³} ≅ Z/4`, where `ρ` is byte rotation
  `(icol, ibit) ↦ ((icol+1) mod 4, ibit)`. `|Aut(M)| = 4` is **proved** by
  complete backtracking over bit-permutations
  (`experiments/e3b_fresh/code/symgf.py`). `ρ` acts on the 32 rows as eight
  four-cycles.

### 0.2 Grades

Every claim below carries one of five labels. The first four are the project's
own grading discipline
(`fleet7/laneCONSOLIDATE/STATE_OF_THE_PROBLEM.md` §2); the fifth is added here.

| grade | meaning |
|---|---|
| **THEOREM (refereed)** | survived an adversarial from-scratch rebuild by a second agent forbidden to read the claimant's code |
| **THEOREM (unrefereed)** | derivation plus machine checks; no second party has rebuilt it |
| **CERTIFICATE** | a machine-checked exhaustive computation over a **stated, finite** population — the scope is part of the claim |
| **MEASUREMENT** | a statistic over a sampled or otherwise incomplete population |
| **OBSERVATION** | a regularity noticed but neither exhaustive nor controlled |

Where a lane report and its referee disagree on a numeral, **the referee's
numeral is what appears here**. Where a source's own status word was weaker than
the claim it supported, **the weaker word is what appears**.

### 0.3 Four standing fences that travel with every citation

These are not caveats to be read once and forgotten. Each one has already caused
a published error in this project.

**F1 — the radius fence (`wrapup/CORRECTIONS.md` C-42;
`wrapup/CONFLICTS_RESOLVED.md` §C10).**

> *"A negative at radius ≤ 4 carries no information about whether an 87 exists.
> These are locality theorems — rigidity statements about small, completely
> enumerated neighbourhoods — not bounds. By this instrument an optimal circuit
> and a four-gates-too-big circuit are indistinguishable: derivation richness and
> dead-gate count are identical to four significant figures at 88, 89, 90, 91 and
> 92 gates. The honest bracket is `56 ≤ L(M) ≤ 88`."*

The measurement behind it
(`campaign_87/wave5_2026-08-04/metareview/optimality/differential_by_length.json`,
1,200 sampled states per length, re-read 2026-08-29):

| gates | 88 | 89 | 90 | 91 | 92 |
|---|---|---|---|---|---|
| `options_per_gate_mean` | 2.3236 | 2.3238 | 2.3262 | 2.3205 | 2.3123 |
| `dead_gate_states` | 0 | 0 | 0 | 0 | 0 |

What F1 covers: every *negative / rigidity / "nothing better nearby"* instrument
used as evidence about whether an 87 exists — empty `k ≤ 4` shells, empty
move-class neighbourhoods, derivation-rigidity and dead-gate statistics, the
mutation sweeps. What it does **not** cover, and where it must not be
over-applied: the certificates remain *true* (an exhaustively empty shell is
still an exhaustively empty shell); **lower bounds are proofs and are untouched**
(`L(M) ≥ 56`, `L_cf(M) ≥ 92`, `N_depth3 ≥ 80`); **upper bounds are witnesses and
are untouched**; and the **`B = 56` tripwire is a theorem with a decision rule,
not a rigidity statistic, and is not repriced.**

One inversion must be fixed wherever it appears: against a proper null, real 88s
are **4.7× more derivation-RICH, not rigid**. The "2.3 vs 64 options/gate"
rigidity framing quoted in older documents is **backwards**.

**F2 — the `N`-independence fence
(`experiments/e17_pure/DOSSIER.md` §5.7).** The single most common way a true
result in this project has failed to bear on 87 is that its derivation never
mentions the gate count, so **its instance at `n = 87` and its instance at
`n = 88` are the same sentence**. The test is not "does the derivation mention
`n`"; it is:

> **Instantiate the statement at `n = 87` and at `n = 88` and ask whether the
> two instances differ.**

By that test, exactly one fact in the entire programme passes: **conjunct A11**
(§4.3). Everything else in §2.5 and §4 is `N`-independent and constrains an 87
exactly as much as it constrains an 88 — which is to say, it describes the shape
an 87 would have, not whether one exists.

**F3 — the population fence (`wrapup/CORPUS88.md` §3, §10).** Six mutually
incompatible counting bases for "the known 88s" are in circulation. Never quote a
population size without naming its object and its dedup rule. In particular the
e15 Run-A census is **not** "every distinct 88 mask multiset on disk": it is
17,283 of 1,575,516 = **1.1 %**, and **92 % of it came from a single method**
(NRPA).

**F4 — the standing prohibition (`experiments/e17_pure/REF_DELTA/VERDICT.md`
§7).** **Never cite `δ(mc) = 2`, or the count "0 / 111,940", as evidence about
87 — on either side of the question.** The deleted-side half (57,379 masks) is
*logically equivalent* to the conclusion it was offered as evidence for; the
surviving-side half (54,561 masks) is not circular but is weak (`p ≈ 0.015–0.25`)
and was confounded on the one variable that defines the observation. §2.5.1
reports what happened when that confound was finally tested.

---

## 1. The claim and its status

### 1.1 The claim

> **`L(M) = 88`.** The minimum number of 2-input XOR gates computing AES
> MixColumns is 88.

**Status: opinion.** It is the stated intuition of the holder of the 88-gate
record — J. Jean, ePrint 2026/1481: *"my intuition tells me 88 is the lower
bound, but proving it seems extremely hard"* — and it is this project's opinion
after three campaigns explicitly aimed at 87.

### 1.2 The only theorem

**THEOREM (refereed).** `56 ≤ L(M) ≤ 88`.

*Upper end.* Explicit oracle-verified 88-gate circuits.
`evidence/circuits/` holds eight hash-pinned canonical records
(`evidence/circuits/spectrum.json`), five of them at 88 gates, at depths 5, 5, 6,
7 and 8; the arbiter is `verify_circuit.py` at the repository root.
Independently, `wrapup/CORPUS88.md` indexes **1,575,516 distinct verified
88-gate mask sets** (§2.2 below).

*Lower end.* `L(M) ≥ 56`, unconditional and refereed, by **adaptive gate
elimination**. Sources: `atlas/thinktank/lower_bound.md` §4;
`atlas/thinktank/referee_55.md` (full report + Addendum);
`atlas/NOTEBOOK.md` ~725–728; restated
`experiments/e17_pure/DOSSIER.md` §1.3. The bound decomposes as

> **`56 = 1 + 18 + 32 + 5`**

| term | value | what it is |
|---|---|---|
| `m` | 1 | the covering bonus — one adaptive Lemma-F stage pays 2 gates instead of 1 |
| `32 − \|K\|` | 18 | the 18 columns outside the keep-set, each zeroed at ≥ 1 gate |
| `32` | 32 | the 32 distinct target rows of `M\|_K`, each of weight ≥ 2, hence each a gate |
| `e_K` | 5 | `minE(cert 5) ≥ 5` — the certified extras |

Cert 5 is `K = {2,4,7,9,15,18,20,21,22,24,25,29,30,31}`, `|K| = 14`. Twelve
covering certificates were tested at depth 4; **eleven die (`minE = 4` exactly,
with explicit witnesses), one survives.** Cert 5's `minE ≥ 5` was established by
**two independent implementations, both exhausted**: the referee's unpruned C
searcher (`9.43e10` nodes, 511/511 root branches, 114/114 shards) and the lane's
pruned Python searcher (`4.75e9` nodes, 511/511, 114/114). Both report the
identical root state; every shard file ends `SHARD-DONE … NO-COMPLETION`.

**The gap is entirely about middles.** In a minimum-size SLP all 32 targets are
distinct masks of weight ≥ 5, so exactly 32 gates are *finals* (gates carrying a
target mask) and the rest are *middles*. Hence `88 = 32 + 56`, a hypothetical
`87 = 32 + 55`, and the bound `56 = 32 + 24`. **The `+32` is free**; three years
of proof effort have bought 24 middles against the record's 56.

### 1.3 The other proved quantities

| statement | grade | source |
|---|---|---|
| `L_cf(M) ≥ 92` — cancellation-free lower bound, solver-free certificate, two independent implementations | THEOREM (refereed) | `beat88/understanding/CANON.md` §U6-2 |
| `L_cf(M) ≤ 102` — explicit oracle-verified 102-gate cancellation-free circuit (`κ = 0`, 32/32 targets, depth 5), replayed from raw JSON 2026-08-29 | THEOREM (witness) | `beat88/understanding/v2_no_vocab/data/cf_incumbent.json`; `wrapup/CONFLICTS_RESOLVED.md` B1. **Do not quote 103, 104 or 133.** |
| `N_depth3 ≥ 80` — every depth-≤3 MixColumns circuit has ≥ 80 gates; exact rational weak-duality certificate over 72,830 rows × 29,180 variables, `u ≥ 0`, `Aᵀu ≤ c` checked in integer arithmetic, `exact_dual_value = 47597998171620/10¹² = 47.597998`. Re-verified 2026-08-29 | THEOREM (refereed) | `campaign_87/wave6_2026-08-11/lower_bound/cert_depth3.json` + `THEOREM.md`; re-check `python3 certify.py --check cert_depth3.json`; `wrapup/day2/STEWARD.md` §S1 |
| Verified depth frontier **97 @ 3 / 91 @ 4 / 88 @ 5** | THEOREM (witnesses) | `experiments/e4_depth/RESULT.md`; `wrapup/CONFLICTS_RESOLVED.md` B7 |

`L_cf(M) ≥ 92` is **the only proved quantity anywhere in the programme that is
above the record.** Everything else in §1.2–§1.3 is below 88, and §3.6 lists the
proved ceilings that keep it there.

⚠ **A public-record correction that travels with this document.** The depth-4
point is **91**, not the published 92. Three mutually distinct lineages are
oracle-verified at `gates=91 depth=4 outputs_built=32/32`
(`campaign_87/cascade6/FRONTIER_91gates_depth4.json`,
`experiments/e4_depth/out/resched/atlas_compiled_m1_91gates_depth4.json`,
`fleet2/laneG_generator/referee/results/ref_91g_d4.json`; pairwise Jaccards
0.556 / 0.433 / 0.358), and the published 92 is *not* a dead-gate strip of a 91
(its target cone is 92 gates, 92 live, 0 dead). Every document still saying
92 @ 4 — including `README.md` and `aes_mc_records/PAPER.md` — is stale.
Source: `wrapup/CONFLICTS_RESOLVED.md` B7, C2, C3.

---

## 2. The positive evidence, ordered by strength

Nothing in this section is a proof. The ordering is by how much each item would
have to be explained away by someone who believed `L(M) ≤ 87`.

### 2.1 Independent convergence on 88 — the strongest item

**Grade: OBSERVATION, but over independent parties.** This is the only evidence
in the document that is not an artifact of this repository's own methods, and it
is therefore the item least vulnerable to F1 and F2.

**(a) The published record was reached independently, twice, from different
directions.** J. Jean reached 88 (ePrint 2026/1481, posted 2026-07-23) and holds
priority; this project reached 88 independently. The two circuits are genuinely
different objects — this project's 88 @ depth 7 **shares 61 of its 88 masks**
with Jean's, i.e. 27 masks differ (`README.md`). This project subsequently found
88 **from scratch** at depth 5 and depth 6 — from root
`constructors.build("naive", 1958)`, a randomised XOR tree over the 32 raw
inputs, with a producing engine that reads nothing from disk. Neither party has
found 87.

**(b) The published literature has approached 88 monotonically from above and
stopped.** (`experiments/e17_pure/DOSSIER.md` §1.2; `README.md`;
`aes_mc_records/PRIOR_ART.md`.)

| depth | published best known | this project |
|---|---|---|
| 3 | 99 (Shi–Feng–Xu, ToSC 2023) | 97 |
| 4 | 97 (Osvik–Canright, ePrint 2024/1076) | **91** |
| 5 | 94 (Osvik–Canright) | 88 |
| 6 | 92 (Maximov, ePrint 2019/833) | 88 |
| 7 | **88 (J. Jean, ePrint 2026/1481 — priority is Jean's)** | 88, independently found |
| unconstrained | 89 (Sun–Yang–Li, ePrint 2025/1493) | 88 |

**87 has never been found by anything, anywhere.**

**(c) The clean-room calibration: from-scratch effort lands at 93, not 88.**
`fleet10/RESULT.md`, written post-hoc 2026-08-29 entirely from on-disk evidence.
`fleet10/cleanroom/spec/` contains exactly two files — the 32 target masks and a
byte-identical copy of `verify_circuit.py` (`md5 682053357d0d873b6dee527e74b83826`,
re-checked 2026-08-29) — and machine-checked self-containment: no fleet10 file
reads anything outside `fleet10/cleanroom/`.

```
$ python3 verify_circuit.py fleet10/cleanroom/work/FINAL.json
gates=93 depth=7 outputs_built=32/32 problems=0
VERDICT: VALID MixColumns circuit
```

Achieved in ~7.5 wall-hours on one day, writing its own randomised
Boyar–Peralta search in C (five generations), a SAT window-repair instrument, an
island portfolio with migration, and a symmetry-quotient SAT search. The
measured curve: **one unaided worker, ~2 minutes: 95–101 gates**; the deepest
logged BP descent alone reaches **94**; the full portfolio reaches **93**, and
five distinct 93s exist. **It never reached 92.**

That is a *calibration, not a search result*: the five-gate gap 93 → 88 is the
measured value of everything this repository accumulated. Two reusable secondary
numbers from the same lane: **ρ-symmetry costs 12–13 gates** in a greedy search
(matched A/B: 108 @ 4 symmetric vs 95 @ 8 asymmetric), and **SAT window repair
near an optimum succeeds 1 time in 1,924** — plentiful improvements descending
from 124, exactly one at 94, **none at all from 93**.

**Why this is the strongest item.** F1 and F2 attack *this project's own
negative instruments*. They do not touch the fact that two independent parties,
a published literature spanning 2019–2026, and a knowledge-free clean-room run
all stop at or above 88, and that the two parties who reached 88 did so with
circuits sharing only 61 of 88 masks.

**Honest counterweight.** Convergence of searches is convergence of *searches*.
The forcedness study (§3.4) shows that at miniature scale a true optimum admits a
median of 10 structurally distinct realisations and that uniqueness collapses as
instances get harder — so the plateau's width is not evidence against 88, but
neither is the convergence evidence *for* it in any quantifiable sense. It is
what it is: nobody has found 87.

### 2.2 The tripwire record — universal `B = 56`, and the stronger deletion certificate

**Grade: THEOREM (unrefereed) + CERTIFICATE.** This is the second-strongest
item because, uniquely among the negatives, it is **explicitly exempted from the
radius fence F1**: it is a theorem with a decision rule, not a rigidity
statistic.

#### 2.2.1 The `B = 56` theorem and its 87 detector

**THEOREM (unrefereed; identity, measured 1500/1500).**
`experiments/e15_campaign3/AUDIT.md` §11.4; restated
`experiments/e17_pure/DOSSIER.md` §3.4; detector code
`experiments/e15_campaign3/tools/sweep.py:296` (`count_B`), wired at 525–532,
alarm path 730–738.

> Let `C` be a valid 88-gate circuit **not already reducible to 87**. Then all 88
> gate masks are distinct, exactly 32 carry target masks, exactly 56 carry
> non-target masks, and **every one of the 56 non-output gates has at least one
> consumer** — `B = 56`.

*Proof.* Two gates with the same mask ⇒ delete the later and rewire ⇒ an 87. A
non-output gate with no consumer ⇒ delete ⇒ an 87. ∎

**The contrapositive is a live 87 detector: `B ≠ 56` on a valid 88 ⇒ an 87 is
available immediately, by deletion.** Generality: `B = n − q` for any irreducible
SLP with distinct masks and outputs on distinct gates.

#### 2.2.2 The record: zero alarms over 1.58 million mask sets

**CERTIFICATE.** `wrapup/CORPUS88.md` §2, §4.

| check | population | result |
|---|---:|---|
| full `count_B` (e15's function, unmodified) | 28,796 sets with a banked build order | **28,796 / 28,796 have `B = 56`. Zero alarms.** |
| 88 **distinct** masks | all **1,575,516** distinct verified mask sets | **1,575,516 / 1,575,516 pass.** No duplicated mask anywhere |
| all 32 targets present | all 1,575,516 | 1,575,516 / 1,575,516 (it is the admission criterion) |

**No B-alarm. No 87 by deletion anywhere in the corpus.** No file named
`ALARM_B_*.json` exists anywhere on disk. The detector is fail-able and has been
shown to fail correctly: `count_B` reads **57** on both 89-gate controls.

The corpus itself, reported in tiers because they mean different things:

| tier | distinct 88s | what it is |
|---|---:|---|
| **A — materialised circuits** | **28,892** | one circuit file / one `.plat` row / one reconstructible basin row per set; 28,796 have a banked build order, hence depth and `B` |
| **B — + four curated population banks** | **198,977** | adds beat88's `pop88_worklist`, campaign_87's two 2026-07 harvests, `found88_layer89` |
| **C — + the NRPA sub-92 harvest** | **1,575,516** | adds `campaign_87/wave5_2026-08-04/nrpa/out/sub92.jsonl` — 1,400,343 valid 88 rows, all pairwise distinct |

**1,575,516 is a floor**, not a ceiling: 2,840,868 further 88-mask rows in the
bulk `.pop.jsonl` harvest and 1,530,095 88-gate records in beat88's export tree
are counted but not hashed. The honest project-wide range is **1.6 M – 4.4 M
distinct**. **92 of the 28,796 are realisable at depth 5**, the record depth.

Verification of the index: 21 circuits spread across every gate-list source were
run through the oracle — **21/21 `VERDICT: VALID MixColumns circuit`, all at 88
gates** — and 438 random rows from the five mask-only banks were checked for 88
distinct masks, all 32 targets, and greedy realisability: **438/438 pass**.

**The plateau is vast and multi-basin.** Three independent plateau harvests, run
weeks apart, are **mutually disjoint**: NRPA ∩ merged-engine = 0,
NRPA ∩ population88_new = 0, merged-engine ∩ population88_new = 0 — **1,540,221
distinct 88s with zero collisions between them**. Each search samples a different
part of the level set.

#### 2.2.3 The deletion-realisability certificate — strictly stronger than `B = 56`

**CERTIFICATE, new 2026-08-29.**
`atlas/corner/ANALYSIS_20260829.md` §7; artifact
`wrapup/day2/atlas498/near87.json`; tool
`wrapup/day2/atlas498/tools/near87.py` (`nice -n 19`, 55.6 s, single thread).

`B = 56` says every middle gate has a consumer, so no gate is *unused*. It does
**not** ask whether the consumers of a deleted gate have an **alternative
derivation** inside the remaining mask set. The new test does, and it allows
**arbitrary rewiring of the surviving 87 masks**.

The construction: every valid 88 contains all 32 target masks, so deleting one
non-target mask leaves an **87-mask set that still contains all 32 targets**. The
only thing between such a set and an 87-gate MixColumns circuit is
realisability — whether every member is the XOR of two earlier members-or-inputs.
Run exhaustively over the 498 distinct 88s of the atlas corner sweep:

```json
{"pairs_overlap87": 35,
 "pairs_overlap87_all_contain_targets": true,
 "pairs_overlap87_realisable": 0,
 "deletions_tested": 27888,
 "deletions_realisable": 0}
```

* All 35 pairs of the 498 that overlap in 87 masks: **35/35 contain the 32
  targets** (asserted, not assumed), **0/35 realisable.**
* All single-mask deletions: `498 × 56 = 27,888` candidate 87-mask sets — the
  count being exactly 56 per circuit independently re-confirms `B = 56`. A cheap
  necessary condition first (after deleting `m`, every remaining mask must retain
  a derivation pair inside `inputs ∪ M \ {m}`): **10,833 of 27,888 pass it** —
  39 %. All 10,833 survivors then went through the project's own
  `wrapup/tools/corpus88.py:realisable` greedy closure, which is **exact** for
  this question (the closure is order-free and monotone, so it succeeds iff the
  set is realisable). **0 of 10,833 realisable.**

> **No 87-gate MixColumns circuit is obtainable from any of the 498 atlas corner
> 88s by deleting one mask, even with unrestricted rewiring of the remainder.
> 27,888 / 27,888 closed, machine-checked.**

**A structural by-product worth more than the certificate.** The 39 % pass rate
on the local condition against a 0 % global pass rate separates the deletion
barrier into two components for the first time: **the obstruction to deletion is
topological (ordering / acyclicity), not local (availability of a
re-derivation).**

**Scope, stated exactly.** 498 circuits, not 1.58 M. The test needs only mask
sets, not build orders, so extending it corpus-wide is the project's single
cheapest unfired certificate (`atlas/corner/ANALYSIS_20260829.md` LEAD-1: the
fast filter is `O(120²)` per circuit, ~11 G integer ops over the full index,
**~2 CPU-days in pure Python, minutes in C**, no solver). If it returned
negative corpus-wide it would be **the strongest deletion certificate the project
could publish**: *"no 87 by one deletion from 1.58 M distinct 88s."* It has not
been run.

### 2.3 Exhaustive negative space

**Grade: CERTIFICATE throughout — and the radius fence F1 applies to every item
in this subsection.** It is stated here, inside the section, rather than hidden
in a footnote:

> **Everything in §2.3 is a locality theorem, not a bound.** The measured
> distance from a circuit to a known better circuit is **median 42 masks, min 3,
> max 48; 44 of 45 transitions need `k ≥ 8`** — against a certified radius of 3
> (`wrapup/CORRECTIONS.md` C-42). The exact decider returns "irreducible" about
> 97 @ 3, 94 @ 4, 92 @ 5, 91 @ 5, 90 @ 5, 89 @ 9 and Jean's 88 @ 7 **alike**
> (12,241 exhaustive `k=2` windows, 8,400 sampled `k=3`, zero reducible on all of
> them). An instrument that says the same thing about an optimal circuit and a
> nine-gates-too-big one has likelihood ratio ≈ 1 about optimality.
>
> These certificates are still *true*, and they are cited here for what they
> legitimately say: **an 87, if one exists, is nowhere near any circuit anyone
> has ever built.**

#### 2.3.1 Move-closed orbits

**CERTIFICATE.** `experiments/e16_lastwish/laneFPOINT/RESULT.md`;
`experiments/e14_plateau87/`; scope statement is conjunct A13 of
`experiments/e17_pure/DOSSIER.md` §4.3.

| object | states | status |
|---|---:|---|
| e14's five known-88 orbits (wirings, under re-association + re-parenting) | 44,793 | closed; **zero free 87s** |
| e16's eight F-point orbits F1..F8 | **333,396** | **all eight CLOSED by exhaustion**, no cap hit, no timeout; **zero states below 88** |
| **combined, thirteen studied anchors** | **378,189** | all closed, **zero sub-88 states** |

Inside those states: **4,856,598 re-association sites examined, 0 collisions**;
436,914 re-parent probes; three collapse tests (free-87 move, dead-gate,
re-association collision) return `0/0/0` at every F-point; **minimum reachable
gate count is 88 at every one of them.** For scale, F1 alone (91,368 states) is
larger than e14's five orbits combined.

Under a *different* move set — the complete neutral remove-1-add-1 move on
**mask sets** rather than wirings — the same five records lie in closed
components of **729 / 2,187 / 10,935 / 112,833 / 59,697** states, 186,381 in
total (`beat88/methods/shared/gauge.py:209 orbit_bfs`). The two numbers,
44,793 and 186,381, are **not competing measurements of one thing**; they are
different objects under different moves, and must never be presented as
revisions of each other (`wrapup/CONFLICTS_RESOLVED.md` B4).

**Scope (A13).** Both move sets are **count-preserving components of known 88s**.
An 87 not reachable from a known 88 by these moves is outside these objects **by
construction**. And e14 measured **90.1 % of on-disk 88s as far from all studied
frames**. *These closures constrain such an 87 not at all.*

#### 2.3.2 The `k`-window sweeps

**CERTIFICATE.** All figures re-tallied 2026-08-29 from append-only ledgers
(`wrapup/CONFLICTS_RESOLVED.md` §S7, §S8, §S5).

> *"All 139,878 distinct harvested 88-gate mask sets are proven irreducible at
> `k = 2` — **215,412,120** exact window decisions, 1,540 windows each, zero
> reducible, re-tallied 2026-08-29 from three append-only progress ledgers whose
> key sets are pairwise disjoint. The figure 139,878 is exact, not
> approximate."*

The `k = 3` queue is **empty, not partial**: 200 rows, all `irreducible_k3`, each
at 27,720 triples. Exact `k = 4` (remove-4 / restore-≤3) coverage, likewise
re-tallied:

| population | windows decided | of a space of | coverage |
|---|---:|---:|---:|
| Jean's 88 | 56,489 | 367,290 | 15.4 % |
| the family-3 anchor | 39,034 | 367,290 | 10.6 % |
| this project's own 88 @ depth 7 | 34,599 | 367,290 | 9.4 % |

**Every window irreducible; zero reducible.** ⚠ Do not quote the stale
32,685 / 20,432 / 9 from `campaign_87/FACTS.md` §6a; and do not quote the
campaign-wide "≈165 M window decisions" total, which the `k = 2` half alone now
exceeds and which has not been re-derived (`wrapup/CONFLICTS_RESOLVED.md` R2).

A separate, later instrument (e15, 2026-08): **15,099,957 `d(S)=1` windows over
22 distinct circuits, 0 compressible, 0 shared helpers** (ledger-exact). Quote it
with its campaign; it must never be summed with the campaign-87 figures.

The decider behind the archived campaign-87 verdicts was validated on **4,200
planted YES windows (4,200/4,200 correct, every witness oracle-verified)** and
**462/462 with the first proof branch deleted**; every archived sweep used
non-target windows only, confirmed by the window counts matching `C(56,k)`
exactly. ⚠ The decider is **unsound on windows containing a target mask** — an
input class no archived sweep ever used, and one that cannot arise for a real 87
(any valid circuit contains all 32 targets, so `S \ T` is automatically
target-free). It must not be reused on raw mask sets without that guard
(`wrapup/CONFLICTS_RESOLVED.md` B6).

#### 2.3.3 Drop-4: no four output rows can be resynthesised cheaper

**CERTIFICATE.** `experiments/e5_readd/ledger.jsonl` (`kind: screen_hist`,
`screen_done`); `wrapup/CONFLICTS_RESOLVED.md` §S11 (residue R3);
`experiments/e5_readd/ADDENDUM_20260829.md`.

> *"For the verified 88 at depth 5, all 35,960 four-target drop sets were
> refuted at `k = W − 1` — no set of 4 output rows can be resynthesised from the
> rest of the circuit using even one gate fewer."*

The same screen has since **run to completion on a second, structurally
different family** — the 88 at depth 5 from scratch — at **35,960 / 35,960
four-target drop sets, zero timeouts**, answering the family-independence
question e5 left open.

⚠ **Precision required.** The word **"refuted"** is banked for `88d5` only. For
`88fs5` the correct wording is **"all 35,960 drop-4 sets screened"**: its
W-histogram contains 15 sets at `W = 0` and 430 at `W = 1`, where "refuted at
`k = W − 1`" is vacuous or ill-posed. A re-tallier should also know that the
`88d5` drop-4 stream holds 35,959 distinct subsets, not 35,960 — the missing one,
`[3,11,19,27]`, is the unique `W = 10` set, excluded by the screen's `wmax = 9`
cap and decided instead in the `cube` stream (121 rows). **There is no hole; a
naive re-tally invents one.**

#### 2.3.4 The move-class walls

**CERTIFICATE.** `beat88/methods/m2_oracle/LEDGER.md` (§Theorems banked),
`STATE.md`; `beat88/methods/m4_inverse/analysis/landscape.md`.

* **No 87 within remove-2-add-1 of all 33,010 known 88 gauge orbits.**
* **No 87 within remove-3-add-1 of all 64 known 89s.**
* **6,832,408 genomes swept**: no 87 within one operand edit of any one-gate
  truncation of the five records and the 89.
* **44,249 `FOUND_*` alarm files** across beat88; gate-count distribution
  89 : 12,704 · 90 : 30,856 · 91 : 16 · 92 : 673. **No `FOUND_*` below 89 gates
  anywhere.**
* The four files named `*87gates*` in `campaign_87` are **deliberate tripwire
  fakes** (`fake87`, `badfail`, `FAILED_87`); none was ever promoted.

#### 2.3.5 The site rebuilds

**CERTIFICATE.** `experiments/e16_lastwish/lane536/RESULT.md` §D.

At a *site* (a non-output gate `u` with exactly two consumers, whose side
operands include a non-output fanout-1 gate), deleting `u` and the once-used side
operand and rewiring the two consumers gives `gates = 84 + G`, where `G` is the
minimum size of an SLP over the surviving signals producing **both** consumer
masks. So **87 iff `G ≤ 3`**, and 86 iff `G ≤ 2`.

| test | population | result |
|---|---:|---|
| **D2** — complete 3-gate test, all shapes, at the 536 records | 536 | **`G > 3` on 536/536** |
| **D3** — the same test on the whole corpus | **55,970 candidate sites** across **18,355 circuits** (k=1: 54,561; k=2: 1,409), 1,686 s | **0 sites with `G ≤ 3`**; 0 oracle-VALID below 88 |
| **D4** — the `k=2` (2-mint / 3-orphan) regime, where 87 iff `G ≤ 4` | **1,409 sites** | **1,409 / 1,409 decided `G > 4`** (1,309 fast, 100 by brute force) — the charter's core case is **CLOSED, not bracketed** |

Fail-able controls: the 3-gate decider was attacked with **8,000 randomly
generated 3-gate SLPs of every topology**, any 2 of 3 gates designated as
outputs — **0 missed**, every returned program replayed gate by gate; the 4-gate
decider's positive control found **400/400 planted instances**.

⚠ **Self-correction that must ship with this item.** The "536 barrier" that
originally motivated the lane **dissolved**: the 536 is **268 sites doubled**
(each contributes an A/B mirror pair), and at every one of them the headline
finding was **forced by an identity and could not have come out otherwise** —
`δ(W) ≥ max(δ(mc₁), δ(mc₂)) − 1` with `max(…) = 4` on 536/536, so `δ(W) ≥ 3` and
"buildable" (`δ(W) = 2`) was arithmetically impossible **before the scan ran**.
Stated at its sharpest, `max(δ) ≥ 4` holds at **99.47 % of all `k=1` candidate
sites in the corpus**. D3 and D4 above are the parts that survive as
computations; the "barrier" framing does not.

### 2.4 Relaxation pricing — every way of taking the problem apart returns 88

**Grade: CERTIFICATE (each item over its own stated class) + MEASUREMENT.**
The common shape: build a relaxation or a re-parameterisation of the synthesis
problem, price it exactly, and see what number comes out. **Nothing has ever come
out below 88.** The one exception that was still open at compile time, `k = 14`,
was **decided UNSAT on 2026-09-01** and came out at 15 (§2.4.2).

#### 2.4.1 The mutation sweeps

**MEASUREMENT.** `fleet12/lane*/results.jsonl`; `wrapup/MANIFEST.md` §3.

> **Every one of ~200 mutations across six lanes returned exactly 88**, each with
> an identified mechanism. The sweep also corrected one published number
> **89 → 88** (see `wrapup/CONFLICTS_RESOLVED.md` B11 — an internal generator
> config price, not a public record).

Two independent, exactly-solved instances landed on 2026-08-29 that make the same
point *by returning zero*:

* **`W3_noshare = 11` exact** (verified, 33,876.6 s) makes `(rank 1, no sharing)
  = 12`, so **the rank cut buys ZERO** and the whole 3-gate gap sits in the
  `D37 → W3` sharing edge. Lane F4's own §3.2 claim that "both ingredients are
  needed" is **false**, exactly as its referee said
  (`fleet3/laneF4_rule/ADDENDUM_20260829.md`).
* **`U3(tier1) = 10` exact** (`k = 9` exhaustively UNSAT), so
  `(U27, U3) = 2 + 10 = 12` — **identical to `4 + 8 = 12`**. The hoped-for move
  "from 12 towards 11" **moves nowhere**; R34 stays at 25
  (`fleet2/laneG_generator/ADDENDUM_20260829.md`).

Two solves on different cells, both returning **zero** for the reduction they
were built to price. *One gate in, one gate out, every time.*

#### 2.4.2 The merged-block ladder — and the door that closed (UPDATED 2026-09-01)

**CERTIFICATE.** `fleet8/unified/results/joint_levels.jsonl` (30 hours of
solver time); cross-checked on a second CNF encoding by `fleet11/laneCUBE`, which
also **decided the last rung, `k = 14`, on 2026-09-01**
(`fleet11/laneCUBE/RESULT.md` §7.1); scope statement is conjunct A14 of
`experiments/e17_pure/DOSSIER.md` §4.3, §8.3.

`k = 9, 10, 11, 12, 13, 14` are **all exhaustively UNSAT** for the merged dimension-16
`W3 ∪ U4` block — 8 targets, lines `{2,3,4,7}`, 33 free values, at the `88@7`
cell, with the `D37` plane and `Q27` held at their configured values,
`PREFLIGHT_OK`. `k = 9/10/11` were **independently re-proved** by a different
encoding at **528/528 cubes UNSAT at each level, 0 disagreements**, with a
positive control firing (SAT at cube 144, verified witness).

With the replay bound `W3 + U4 = 8 + 7 = 15`, the ladder up to `k = 13` bracketed
the merged block at `{14, 15}` (`fleet8/unified/ADDENDUM_20260829.md`; ⚠ that
lane's own `RESULT.md` logs the joint job as `DONE` with **no `k = 14` row and no
verdict file** — "DONE" there means "timed out", `wrapup/CORRECTIONS.md` C-20).
**That bracket is now collapsed:**

**`merged(W3 ∪ U4) = 15` exactly** — the split total. Merging the two largest
levels buys nothing.

> **The honest reading (A14): `UNSAT` at `k ≤ 13` was strictly weaker than what
> the block model already assumes. Only `SAT at k = 14` would have produced an
> 87.** The two-gate saving was already dead; the one-gate question is now
> answered in the negative.

**The verdict, dated (`fleet11/laneCUBE/RESULT.md` §7.1):**

> *"`k = 14` is UNSAT — decided 2026-09-01 by the monolithic route. The
> kissat-4.0.4 member of the monolithic portfolio completed the whole instance
> in one process in 356,321.63 core-seconds (≈ 99 core-hours); log
> `fleet11/laneCUBE/logs/mono_14_kissat404.log`, `{"kind": "mono_level", "k": 14,
> "status": "UNSAT"}`. With the banked `k = 9..13` UNSATs the ladder `k = 9..14`
> is complete, all UNSAT, and the bracket `{14, 15}` collapses to 15."*

A monolithic solve is a complete decision of the level — the same path that
decided `k = 11` and `k = 12`. The 528-cube sweep, which was never finished, is
**consistent and not the basis of the verdict**: it stood at 90/528 decided, all
UNSAT, 0 SAT, when the verdict was banked. Three further monolithic solvers
(`slp_opt` CDCL, cadical-3.0.0, glucose-4.2 — same CNF, different engines) were
still running as engine-level confirmations; a fully independent cross-encoding
check (fleet8's `dslp` CNF at `k = 14`) is optional and has not been run, priced
at roughly 10× the `k = 13` cost. **Do not quote any partial cube coverage
("51/528", "73/528", "87/528") as the status of this level** — those are samples
of an unfinished sweep that the monolithic verdict superseded.

The instance is packaged as a single CNF,
`experiments/sat_package/k14_joint_W3U4.cnf` (4.2 MB): **SAT ⟺ an 87-gate
MixColumns circuit exists in that class** — and it is now decided **UNSAT**.

**What this does and does not say.** It says: **no 87 exists that shares the
block structure of every known 88** — precisely, none whose `W3 ∪ U4` blocks at
that cell are built jointly in ≤ 14 gates. It is **not** a proof that no 87
exists. Its scope, from the same lane's referee: the ladder says nothing about an
87 that does not respect the block strata at that cell — **the load-bearing
unproved assumption of the whole block programme** (§3.5). The honest bracket
remains `56 ≤ L(M) ≤ 88`.

#### 2.4.3 The menu, cell and merge-lattice bounds

**CERTIFICATE, each over its own class.**

| certificate | statement | scale | source |
|---|---|---:|---|
| **all-menu bound** | `price(C) ≥ 87` over **1.41 × 10²⁶** menu configurations, nine of ten block bounds exactly tight, the single loose gate localised at the hub | 10 block bounds | `fleet5/laneMENU/results/bound.json` |
| **cell sweep** | every known cell prices **≥ 88** | 20 distinct cells | `fleet5/laneMENU/results/cellprice.json` |
| **merge lattice** | each dissolved block boundary prices **exactly the split total** — 19 boundaries dissolved, 19 times exactly the split; 7 dissolved simultaneously still landing at exactly 88 | 21 rows: 19 FREE, 2 UNDECIDED | `fleet5/laneMERGE/results/FINAL_TALLY.txt` §B |
| **no-solver merge bounds** | admissible lower bound already equals the split | 131 | `fleet5/laneMERGE/results/bounds.json` |
| **containment + generality** | the replay bound holds and the merge is strictly more general | 349 / 349 | `fleet5/laneMERGE/results/containment.json` |
| **RC2 exact union floors** | exact minimum over a two-circuit mask union; **best floor anywhere = 88** | 749,150 OPTIMAL / 125 timeout | `campaign_87/wave5/burn/union_sat/*.jsonl` |
| **DOOR-SHUT sweep** | `U07(M) ≥ 11` for every minimal committed set with `U1 ≤ 7`, hence `core(Q1) ≥ 18` for **every** `Q1` at the flagship cell | 740 decided, 0 timeouts, 11.85 core-h | `fleet3/laneCB_completeness/` + `REFEREE.md` |
| **dim-12 tap-region optimality** | `min_gates = |B| = 11`, all cubes UNSAT below 11, each with a **positive control** (a verified 11-gate in-region program) | **4** regions — R4 of 88@5, of 88@5fs, of **Jean's 88**, and R3 of `p88_05` | `experiments/e7_push/ledger.jsonl` |
| **buy-one-save-two refutations** | no block of any of the 14 known 88s can be rebuilt in `|B| − 2` gates even given one free extra in-sector mask | 4,926 | `experiments/e3a_exploit/ledger.jsonl` |

One of the four decided dim-12 regions sits on **Jean's foreign-lineage 88** —
an independent-lineage test obtained free and never previously claimed
(`experiments/e7_push/ADDENDUM_20260829.md`; `wrapup/CONFLICTS_RESOLVED.md`
§S12: four decided regions, not the one the write-up reports).

**One 87 branch closed on 2026-08-29.** `MB27B373 = 13` **exactly**
(`k = 12` UNSAT in 19,458 s, plus the replay bound 13). The boundary is FREE,
`laneMERGE` closes **20-for-20**, and **the branch in which 12 would have priced
the class at 87 is foreclosed** (`fleet6/door/ADDENDUM_20260829.md`;
`wrapup/CORRECTIONS.md` C-14 — `fleet5/laneMERGE/RESULT.md` and its
`FINAL_TALLY.txt` still record `[12,13] UNDECIDED` in two places).

#### 2.4.4 The currency plateau and its measured cliff

**CERTIFICATE + MEASUREMENT.** `fleet9/laneENUM/RESULT.md`;
`fleet12/laneF1/ADDENDUM_20260829.md`.

The 88 sits on a **five-wide flat plateau in the currency axis**: menus with
`|M| = 19 … 23` currency shapes all price **88**, with a **−1.00 exchange rate**
(one currency gate bought, one block gate saved) and cliffs at both ends.

The upper cliff was previously *argued* by crossing to a different (uniform)
menu family. It is now **measured inside the record-derived family**, from 13
rows that landed after the lane's write-up:

| `\|M\|` | prices observed | blocks observed |
|---|---|---|
| 17 | 91, 97, 98 | 74, 80, 81 |
| 18 | 91 | 73 |
| **19** | **88** | 69 |
| **20** | **88**, 89, 90 | 68, 69, 70 |
| **21** | **88**, 89, 97 | 67, 68, 76 |
| **23** | **88**, 89 | 65, 66 |
| 24 | 89, 105 | 65, 81 |
| 25 | 89 | 64 |
| 32 / 48 / 56 | 106 / 112 / 120 | 74 / 64 / 64 |

> **`|M| = 23` is the largest currency-shape count at which any menu in the file
> prices at 88.** The −1.00 rate breaks at 23 → 24: the 24th shape buys back
> **zero** block gates (`blocks` stays at 65), so the total goes **88 → 89**. The
> 25th shape does buy one back (65 → 64) but only restores the rate, leaving the
> total at 89. **The plateau stops at `|M| = 23`, measured rather than argued,
> and it stops one gate above the record, not below it.** Nothing ≤ 87 anywhere
> in the 64 rows.

#### 2.4.5 The composition identity — why "one more clever exchange" cannot work

**THEOREM (unrefereed; identity).**
`experiments/e15_campaign3/laneCOMPOSE.md` §1, `laneCOMPOSE_STALL.md` §1.

`88 = 32 finals + 56 middles` is forced. Every decoded mechanism in the block
programme moves a gate between the currency pile and the helper pile; **every
measured cross-frame exchange is 1:1 as a consequence, not a coincidence** — any
two 88s are joined by substitutions that must net zero because both endpoints
cost 88. *A composition of wash-mechanisms is a wash.*

⚠ **This is `N`-independent (F2, conjunct A2′).** `88 = 32 + 56` and
`87 = 32 + 55` are **the same identity**. It explains why no *rearrangement* of a
known 88 will produce an 87; it says nothing about an 87 that is not a
rearrangement of a known 88.

### 2.5 Structural rigidity — what the 88s are, measured

**Grade: MEASUREMENT + CERTIFICATE.** Weakest of the four positive sections,
because every item here is measured **on 88s**, and F2 applies in full: these are
facts about where 88s live, not theorems about where 87s cannot.

#### 2.5.1 The wiring of an 88 is forced by its mask set

**MEASUREMENT, new 2026-08-29.** `wrapup/day2/STEWARD.md` §S3; tool
`wrapup/day2/tools/wiring_null.py`.

This began as a null control, not as a result: `experiments/e17_pure/laneDELTA`
refused to price the surviving-side observation (F4) on the ground that *"a site
is a property of the wiring, and the corpus's wirings are not sampled —
`_closure_core` fixes every parent by one deterministic rule."* The prescribed
experiment holds the mask set fixed and varies **only** the parent choice. Two
independent measurements:

1. **Sampling.** 30 random topological wirings per circuit, 3 circuits: at the
   moment each of the 88 gate masks was built there was **exactly one legal
   parent pair — 1,320 / 1,320 observations** — and it was always the as-found
   parent (masks whose as-found parent was never sampled: **0**).
2. **Census.** 25 circuits, 2,200 gate masks, acyclic-legal parent pairs computed
   directly: **2,197 masks with exactly 1**, 2 with 2, 1 with 3. **Forced
   fraction 0.9986.**

Consequences observed: site counts **identical** across all 20 wirings of each of
6 circuits; fanout histograms identical; the side split was `del_4 / surv_3` in
**100 % of 280 site-sides**. For contrast, *ignoring acyclicity* there is
apparent freedom — pairs `{a,b}` with `a ^ b = m` anywhere in the signal set run
`{1:314, 2:161, 3:521, 4:43, 5:7, 6:10}` over 1,056 masks. **Acyclicity kills
essentially all of it.**

> **For an 88-gate MixColumns circuit, the mask set determines the wiring. The
> DAG is not a free parameter at 88 gates.**

Three things this buys, precisely:

* It **discharges the stated confound.** laneDELTA's reason for refusing to price
  the surviving-side zero is *true but inert*: any wiring rule produces the same
  wiring, so `_closure_core` introduces no bias whatsoever.
* It **cannot produce a p-value.** The null distribution is a point mass, so
  laneDELTA's ruling that the surviving-side zero is **UNPRICED survives** — on
  one fewer leg. F4 stands.
* It **retroactively justifies the whole repository's methodology**: every method
  here that treats an 88 as a mask set loses nothing by doing so.

#### 2.5.2 Fan-out ≥ 8 is unreachable at 88 — proved over all build orders

**CERTIFICATE (exact, exhaustive), new 2026-08-29.**
`experiments/e_upstream/RESULT.md` §7 class C4; model and output
`wrapup/day2/e_upstream/c4_fanout_cpsat.py` / `.json`.

This is the companion to §2.5.1 and it went the other way from what the
reconnaissance predicted, which is why it belongs here rather than in §3.

Define, for a signal `s` of a mask set `S`,
`potential(s) = |{ x ∈ SIG, x ≠ s : s ^ x ∈ S }|` — how many masks of `S` *could*
be produced by a gate consuming `s`. Every build order realises
`fanout(s) ≤ potential(s)`. The reconnaissance found **potential 8 on every one
of the six record 88s** (e.g. `0x00808000` in `mixcolumns_88gates_depth5`), while
no scheduler in the project ever realised more than 3–5. That made the corpus's
apparent "max fan-out ≤ 5" look like a **scheduling artifact**: the mask sets are
not combinatorially barred from fan-out 8, so the open question was exactly
*"does a record 88's mask set admit a valid acyclic build order realising
fan-out 8?"*

Answered by CP-SAT rather than by heuristics — `y[m,p] ∈ {0,1}` selecting one
producing pair per mask, `pos[m]` an order variable, `y[m,{a,b}] = 1 ⇒
pos[a] < pos[m] ∧ pos[b] < pos[m]` for acyclicity, maximise
`Σ_{(m,p) : s ∈ p} y[m,p]`. Sweeping signals in decreasing `potential` and
stopping once the incumbent reaches the next signal's potential makes each answer
**exhaustive over all signals as well as all build orders**, so each row is the
exact maximum fan-out of that mask set, full stop.

| mask set | max potential | **exact max fan-out over all build orders** |
|---|---:|---:|
| `mixcolumns_88gates_depth5` | 8 | **4** |
| `mixcolumns_88gates_depth5_fromscratch` | 8 | **4** |
| `mixcolumns_88gates_depth6` | 8 | **4** |
| `mixcolumns_88gates_depth7` | 8 | **4** |
| `mixcolumns_88gates_depth8_thirdfamily` | 8 | **3** |
| `jean_88gates_depth7_eprint_2026-1481` | 8 | **5** |
| the 33 e_upstream floors (89–94 gates) | 6–11 | 3 ×4, 4 ×20, 5 ×8, **6 ×1** (`S92_36`, at 92 gates) |

```
39 / 39 sweeps exhaustive · 0 timeouts · every solve returned OPTIMAL
record 88s : exact max fan-out = 5   (max potential was 8)
all 39 sets: exact max fan-out = 6   (at 92 gates)
fan-out >= 8 realisable at 88 gates:  NO
```

> **`e_oddlane3`'s "max fan-out ≤ 5" is not an artifact of how this project's
> engines schedule. On these mask sets it is a theorem, over every valid build
> order.** The gap between potential 8 and the true optimum 3–5 is real:
> acyclicity forces most of a signal's eight candidate consumers to be built
> before the shared signal is available. The best fan-out seen anywhere in the
> banked material is **6, and it costs 4 gates** (`S92_36_00204004`, 92 gates) —
> the only price this class has.

Cost of the answer: **~5 minutes of one `nice -n 19` core**, against the ~50
core-hours a pinned-descent campaign would have burned. Pinning a mask was always
the wrong instrument for a property of the *wiring*.

⚠ **Scope, exactly.** This closes the question for **39 mask sets — the six
record 88s and the 33 e_upstream floors.** It does **not** decide fan-out ≥ 8
over the 1.93 M corpus 88s. A stratified sample of 150 further corpus 88s from
three banks is running under the identical exact model
(`wrapup/day2/e_upstream/c4_corpus_sample.py` / `.json`); **it had completed
1 of 150 at the time of writing** (first row: `nrpa_sub92 L49865`,
`maxpot = 9`, `EXACT = 4`). Read that file for the widened histogram.

**Read together with §2.5.1**, this is the second wiring-side rigidity result of
the day and it points the same way: at 88 gates the mask set determines the
wiring almost completely (0.9986 forced), and the one wiring degree of freedom
anyone proposed as slack — fan-out — is **provably not available**. ⚠ Fence F2
still applies: both are facts about 88-gate mask sets, and neither instance
differs at `n = 87`.

#### 2.5.3 Multiplicity-1 blocks — 28 of every 88 gates are forced

**CERTIFICATE.** `fleet9/laneENUM/RESULT.md`; `fleet9/laneENUM/ADDENDUM_20260829.md`.

**13 of 17 accounting blocks have a unique optimum at every one of 70 tested
cells** — no exception — and never vary across 54,889 wild circuits. **28 of
every 88 gates are forced once the menus are chosen.** Widening what a block
*may* use changes nothing, because it does not change what the block is
*minimising*: `W3` handed a whole extra line kept all eight witness gates inside
the original three. Under the forced dependency edges the supply graph is
saturated, so **all 75 legal emission orders produce the byte-identical
circuit**.

Supporting exhaustive material: **82/82 dim-8 block optimality proofs**
(exhaustive DFS at `k−1` returning empty, `optimum_proved = True`); a
**forcedness certificate** — *"every 9-gate optimum of the unprompted merged
`{2,3,7}` block builds `δ₃(0xc)`"*, UNSAT with that value banned, 3,668 s, all
300/300 cubes, positive control fired.

⚠ The `U3` sub-queue has since drained: **all 14 U3 cells** now bank ≥ 1 optimal
set, but all are still `timeout`, so **U3 stays UNDECIDED**; the §4 floors are
numerically unchanged but are now floors on the *full* product. **84.4 core-hours
of SAT enumeration landed after the write-up and produced no new distinct 88s.**

#### 2.5.4 The measured floors: `κ ≥ 20`, `|A*| ≥ 18`, glue `≥ 2`

**MEASUREMENT, new 2026-08-29.** `atlas/corner/ANALYSIS_20260829.md` §3.2, §3.4,
LEAD-3, LEAD-4; artifacts `wrapup/day2/atlas498/{profiles.jsonl,control.json}`.

Measured with `experiments/e17_pure/laneY/code/ylib.py:Analysis` — the e17
ledger — over **1,303 valid 88s** from three independent populations: the 498
atlas corner circuits, a seeded random 800 of the 17,283 e15 census circuits
(seed 20260829), and the five published records.

| statistic | 498 corner (min/med/max) | 800 census sample | five records |
|---|---|---|---|
| depth | 5 / 8 / 11 | 5 / 8 / 14 | 5 … 8 |
| depth ≤ 6 | **87 of 498 (17.5 %)** | 4 of 800 (0.5 %) | 2 of 5 |
| `l3` (socle skeleton) | 64 / 74 / 79 | 62 / 71 / 77 | 67 … 77 |
| **`κ`** | **20** / 26 / 35 | 24 / 29 / 35 | 22 … 28 |
| **`\|A*\|`** | **18** / 21 / 29 | 20 / 23 / 28 | 20 … 25 |
| **glue gates** | 2 / 6 / 12 | 2 / 10 / 12 | 3 … 9 |
| sector-confined gates | 57 / 64 / 67 | 58 / 60 / 67 | 62 … 65 |

> **Over 1,303 88s from three independent populations: `|A*| ≥ 18` and
> `κ ≥ 20`, with no tail.** The minima are attained by 90 and 31 circuits
> respectively — these are not sampling edges. And **every 88 measured has at
> least 2 glue gates** (masks in no sector); the minimum 2 is attained 5 times,
> never 0 or 1, while the compiled M1 all-σ7 circuit reaches **zero glue at 91
> gates** (`atlas/compiled_all7.json`). *Glue is what the last three gates buy,
> and no 88 has ever bought them for less than 2.*

Two free corroborations from the same battery, over 498 circuits the e17
machinery had never been pointed at: **`n = κ + |counted| + Y` holds exactly in
498/498**, the maximal-clean-tree sub-lemma holds in **498/498**, and every mask
in `A*` has weight ≤ 7 across the whole population (`wt 3: 2 · wt 4: 324 ·
wt 5: 6,186 · wt 6: 177 · wt 7: 3,886`) — consistent with `A* ⊆ U`, the e17
invariant, on data it was never tested against.

**Why this matters and exactly how far it goes.** Branch 3 of the Anatomy Theorem
(§4.4) describes an 87 with **`|A*| = 2`**. The measured floor across three
populations is **18** — sixteen away — and the floor looks hard rather than soft.
If a *lower bound* `|A*| ≥ c` could be **proved** for minimum-size SLPs at any
`c > 2`, **branch 3 collapses and the whole case analysis reduces to two cases.**
⚠ But every measurement here is on **88s**, and the target statement is about
**87s** — and conjunct A11 is the standing warning that these statistics are
**gate-count-asymmetric**. This is a smell, not a bound.

#### 2.5.5 The 88 plateau is structurally ordinary and internally sound

**CERTIFICATE.** `atlas/corner/ANALYSIS_20260829.md` §3.1.

Over the 498 corner circuits: **0 duplicate masks, 0 dead gates, `B = 56` in
498/498, exact `κ + |counted| + Y` partition in 498/498, valid maximal-clean-tree
structure in 498/498**, and **`ρ`-equivariant gate-mask multiset in 0/498** — a
**universal negative, not a discriminator** (also 0 in the 800-circuit census
sample and in all five records). No gate anywhere exceeds F-span dimension 3
across all `498 × 88 = 43,824` gates (`dim 1: 14,458 · dim 2: 28,584 ·
dim 3: 782`).

#### 2.5.6 Efficiency inverts, and the plateau has a two-mode attractor

**OBSERVATION.** `wrapup/LEADS.md` §B items 1 and 8; the counterweight list in
the same section.

* **The best circuits carry the most waste.** The greedy-108 sits *exactly* on
  the `L = 152` floor with debt 0 at every cut and is the **worst** circuit
  measured; `W = L − 152` runs 0 → 18 → 52 → 60 → 92 as one descends to 88. At
  fixed depth 8, AUC(89 > 88) is 0.78 for service and **0.87 for `V`**; service
  correlates with gate count at **+0.26 — the wrong sign**. 97 → 88 sheds ~19
  light gates and *buys* ~10 heavy ones. Drop-0 "useless" gates are **5× more
  common in 88s than in 97s**, and placed later. **Any constructor that optimises
  a legible efficiency metric is walking uphill.**
* **88 is a strong attractor, non-monotonically.** Cone-ILS restarts land
  `{88: 15537, 89: 2270, 90: 2529, 91: 3907, 92: 2548, 93: 1578}` — **88 hit
  6.8× more often than 89**, with a trough between two piles at 91 and 88. ⚠
  **This two-mode structure is unexplained and no document addresses it**
  (`wrapup/LEADS.md` §B counterweights). It is recorded as an anomaly, not
  claimed as evidence.
* **Symmetric basins, rediscovered rather than imposed.** The elite basin is
  79–81 % `ρ²`-symmetric and its 12 `ρ²`-fixed masks are exactly the
  `(x0^x2)/(x1^x3)` sharing trick — **found by search, not built in**. Jean's 88
  is 75 % `ρ²`-symmetric: a second, distinct symmetric basin. All five 88s were
  found in **walk** chunks, none in an LNS chunk. *Descent is not what produces
  an 88; lateral motion plus a depth tie-break is.*

---

## 3. The counter-evidence and the gaps

Held to the same standard as §2. This section exists because the project's own
history is that **every over-read claim was eventually corrected by the project
itself**, and the corrections ran in both directions.

### 3.1 The vocabulary is NOT forced — an 89 sits one gate outside it

**THEOREM (witness) + CERTIFICATE.** `experiments/e_upstream/RESULT.md`
(written 2026-08-29 over searches from 2026-08-21/22); artifacts in
`wrapup/day2/e_upstream/`.

**This is the single most "an 87 could hide here"-shaped result in the project.**

The strongest structural argument for 88-optimality one could make from this
corpus runs: *1.9–3.3 million independently found 88s, across every engine and
family this project has, all draw from one dictionary of 1,778 (or 3,172) words;
that dictionary must be forced.* **It is not forced.**

Define, for a 32-bit mask `m` with `LANE[j] = 0x01010101 << j`:
`odd(m) = { j : popcount(m & LANE[j]) is odd }`. Every input singleton and all 32
MixColumns targets have `|odd| = 1`. The feature is `|odd(m)| ≥ 3`.

**The zero-occurrence claim, re-checked independently and target-checked**
(`wrapup/day2/e_upstream/recensus.py`, one `nice -n 19` worker, 805 s; population
named explicitly as the five mask-bearing 88-gate banks of `wrapup/CORPUS88.md`
§2.1 plus the record circuits; a row admitted only with 88 masks **and all 32
targets present**):

| | |
|---|---:|
| rows accepted | **1,925,065** |
| rows rejected, missing a target | **0** |
| non-target mask slots | **107,803,640** (= 1,925,065 × 56, exactly) |
| distinct non-target masks — the vocabulary | **1,778** |
| circuits containing a `\|odd\| ≥ 3` mask | **0** |
| circuits containing a `\|odd\| ≥ 4` mask | **0** |

And yet:

```
$ python3 verify_circuit.py wrapup/day2/e_upstream/circuits/S89_41_00000098.json
gates=89 depth=10 outputs_built=32/32 problems=0
VERDICT: VALID MixColumns circuit
```

**An oracle-verified 89-gate MixColumns circuit carrying the mask `0x00000098`
(`|odd| = 3`), a feature with 0 occurrences in 107,803,640 non-target mask slots
across 1,925,065 valid 88-gate circuits.** And it is not a disguised 88:

| certificate on `S89_41_00000098` | result |
|---|---|
| reducible by deleting 1 non-target mask | **0 of 57** |
| reducible by deleting 2 non-target masks | **0 of 1,596 pairs** |
| deleting the pinned mask `0x98` alone | leaves **6 masks unbuildable, 4 of them MixColumns target rows** — `0x10109888`, `0x10988810`, `0x88101098`, `0x98881010`, one complete `ρ`-orbit |
| emitted build order depth-optimal? | yes — 10 is the **exact minimum depth** of that mask set |

**The out-of-vocabulary word is load-bearing.** The circuit is built *around* it.
And the price is **1 gate — an upper bound, so the true price is 0 or 1.**

*Provenance and cost.* Root `campaign_87/novelty/roots/root_41_randset_wide_g149_d12.json`
(149 gates, depth 12, created 2026-07-29 by a search not trying to make `0x98`).
Phase 1: 192 jobs × 1,200 s; phase 2: 33 jobs × 3,600 s;
**349,200 core-seconds = 97.0 core-hours, exact, not estimated**. 192/192 and
33/33 ran to a reported floor; 0 `UNREALIZABLE`, 0 `ERR`. All 33 floors converted
to oracle format and run: **33/33 `VERDICT: VALID`**. Floor distribution, phase 2:
89 ×1, 90 ×3, 91 ×6, 92 ×12, 93 ×6, 94 ×5.

**What this establishes.** The vocabulary is a **funnel artifact of descent,
priced at ≤ 1 gate, not a law.** Any argument of the form "the corpus never does
X, therefore X is impossible at 88" is dead in general, and must be replaced by
an argument that prices X.

**What this does NOT establish — plainly, because the exciting reading is the
wrong one:**

1. **It does not lower any bound on 87. Not by a fraction of a gate.** Nothing in
   that directory constrains 87; everything is a search upper bound.
2. **It is not evidence that an 87 exists.** The chain "vocabulary not forced ⇒
   searches missed a region ⇒ an 87 lives there" has a false step: exiting the
   vocabulary costs **≥ 0 and ≤ 1 gate**, and an 87 needs a gate *back*. The
   honest reading is the opposite of the exciting one — this experiment tried
   hard, from 225 independent starts and 97 core-hours, to carry a novel word
   down, and **the best it ever reached was 89. It never touched 88, let alone
   87.**
3. **No 88 outside the vocabulary has ever been exhibited** — not here, not by
   `e_oddlane3`, not anywhere on this machine. The four corpus rows that do carry
   the feature are surrogate/transposed states with `targets=False,
   realizable=False`; they are not circuits.
4. **The pinned-descent method cannot refute anything.** "Floor 89" means "89 was
   the best reached in 3,600 s from this root".
5. **The obvious follow-up had never been run.** `deep.py` breaks at
   `bestn ≤ 88` and spends its whole budget on the 149 → 89 stretch; every one of
   its 225 jobs started at 100–173 gates. **No run had ever started from the 89
   and pushed at 88** — see immediately below.

**The 89 → 88 question, in flight at the time of writing.**
`wrapup/day2/runs/RUNS.md` R1; ledger
`wrapup/day2/e_upstream/seed89_ledger.jsonl`. A pinned descent seeded from
`S89_41_00000098`'s own 89 masks, pin `0x98` held alive, **target 88**, launched
2026-08-29 11:36 with a 10,000 s budget, single thread, `nice -n 19`. Its
question is structural, not a sub-record hunt — the engine target is 88, which
*is* the record, and it stops there:

> **Does an 88-gate MixColumns circuit exist outside the corpus vocabulary?**
> Reaching 88 would produce the **first such circuit ever exhibited** — a new
> structural object and the entrance to unsampled plateau. Failing repeatedly is
> the sharpest available evidence that the 88 plateau really is confined to its
> 1,778-word dictionary.

**Result pending at time of writing** — the long run has banked a `start` row and
no `done` row. A 45-second pilot at 11:35 banked
`{"ev":"done","floor":89,"v_alive":true,"rounds":1,"hits":0,"verdict":"no 88
reached from the 89 in this budget (upper bound; search, not proof)"}`. ⚠ Whatever
it returns, it is a **search upper bound in one direction only**: reaching 88
would be a positive existence result; not reaching 88 proves nothing, exactly as
in item 4 above. Read the ledger, not this paragraph, for the outcome.

**Four of the five never-priced feature classes are now closed** — three for
free by counting, and the fourth (C4) by an exact CP-SAT sweep on 2026-08-29.
⚠ The three counting closures went **against** the "the corpus avoids it" story;
the fourth went **for** it. Only **C1** remains a genuine unpriced class:

| class | verdict | price |
|---|---|---|
| C3 — mask weight ≥ 12 | **CLOSED. Not out-of-vocabulary and never was** — 254 valid 88-gate circuits already carry a weight-12 mask | **0 gates** |
| C5 — the column-parity hubs `T_j = 0x01010101 << j` | **CLOSED. All eight hubs, including all four "absent from every record 88", occur in valid 88s** — `T_0` in 6 circuits, `T_7` in 1,429,688 (74 %) | **0 gates** |
| C2 — the 388 weight-2 "never seen" masks | **the candidate list is wrong**: `0x00001800` and `0x08008000` occur in valid 88s (price 0); 40 further candidates priced at ≤ 2 by the banked floors; ~344 open | partial |
| C1 — `\|odd\| ≥ 4` | **the only genuine unpriced feature class left**; 22 usable roots, 153 candidate pins; ≈ 51 + 33 core-hours | unknown |
| C4 — fan-out ≥ 8 | **CLOSED, exactly, 2026-08-29 — and it closed *against* the "artifact" reading.** Exact max fan-out over **all** valid build orders is 3–5 on the six record 88s and 6 anywhere (at 92 gates), despite potential 8; 39/39 sweeps exhaustive, 0 timeouts, every solve OPTIMAL. **Fan-out ≥ 8 is not realisable at 88 gates.** See §2.5.2 — this row moved from counter-evidence to evidence | **unreachable at 88**; best anywhere is 6, and it costs 4 gates |

C5's closure also corrects the source notebook: the hubs absent from every record
88 are `T_0, T_3, **T_5**, T_7` — not `T_4`, which is present in two of them.

### 3.2 Every negative is radius-limited, and the radius is tiny

**MEASUREMENT.** `wrapup/CORRECTIONS.md` C-42; `wrapup/CONFLICTS_RESOLVED.md`
§C10; `wrapup/LEADS.md` standing caveat; commit `23d80d7`.

This is fence F1, restated as counter-evidence rather than as a caveat.

* The exact decider returns **"irreducible" about 97 @ 3, 94 @ 4, 92 @ 5,
  91 @ 5, 90 @ 5, 89 @ 9 and Jean's 88 @ 7 alike** — 12,241 exhaustive `k = 2`
  windows, 8,400 sampled `k = 3`, zero reducible on **all** of them. The
  instrument cannot tell an optimum from a nine-gates-too-big circuit.
* Over 45 circuits with a known-smaller circuit available, the distance to it is
  **median 42 masks, min 3, max 48; 44 of 45 need `k ≥ 8`** — against a certified
  radius of **3**.
* `fence_sat`'s positive control: **0 SAT in 30 windows across slack 1–9**.
* `metareview/optimality`: dead-gate count and derivation richness **identical to
  four significant figures at 88 / 89 / 90 / 91 / 92**.

**Consequence for §2.3 in one sentence:** every orbit closure, every empty shell,
every empty move class in this project has a radius of at most 4, and the honest
step size between a circuit and a better circuit is ~42. **The searches have
proved that no 87 is *near* a known 88. They have not searched the space where an
87 would have to live.**

An honest counter-example to the rigidity story **inside** the project, landed
2026-08-29: `fleet1/laneD_completions`' two basin sweeps completed 27,720 triples
each and found **99 lateral escapes (42 + 57), not 1**. The lane's published
rigidity headline is wrong as stated: **`88@5fs` is not rigid; `88@5`'s basin is
the anomalous one.** All 99 escapes are distinct valid 88s, **94 of them exist
nowhere else in the 1.58 M-row corpus**, and only the 5 with a build order have
had the `B = 56` tripwire fired on them
(`fleet1/laneD_completions/ADDENDUM_20260829.md`; `wrapup/CORRECTIONS.md` C-18).

### 3.3 The census is 1.1 % of the corpus and 92 % one engine

**CERTIFICATE.** `wrapup/CORPUS88.md` §2.2, §3; `wrapup/CONFLICTS_RESOLVED.md`
Part D.

The e15 Run-A census — the population behind the project's largest *complete*
population sweep, and the base for the `B = 56` full-DAG check and much of §2.5 —
is described in its own campaign as certifying *"every distinct 88 mask-multiset
on disk"*. Measured against the deduplicated index:

* **17,283 of 1,575,516 = 1.1 %** (8.7 % excluding the NRPA dump).
* **15,884 of the 17,283 are NRPA sets — 92 %.** The certified population is not
  a cross-section of the project's 88s; it is mostly one method's output.
* The other **1,558,233** distinct 88s were never in that sweep.

Nothing Run A proved is wrong. But "every" must become "every one exported as a
`*88gates*.json` file", and every statistic derived from that census inherits a
**single-method sampling bias of unmeasured size**.

Three further population caveats that must travel
(`experiments/e17_pure/DOSSIER.md` §8.5):

* Three different "known 88s" populations are used interchangeably in the older
  literature of this repository and **are not the same object**: ~139,878
  harvested mask-set states; 3,254 distinct wired census circuits; 18,355 corpus
  files; 14 V2-decomposed representatives.
* The Lemma-R tripwire on 1,200 + 600 corpus 88s covers **6.5 % and 3.3 %** of
  the 18,355. The corpus-wide *site-frame* version is banked (D3); the strictly
  larger private-operand population is **sampled**.
* **Rigidity is basin-dependent** — see the 99 lateral escapes above.

### 3.4 The structural facts hold at 89–97 too

**MEASUREMENT.** `wrapup/LEADS.md` §B counterweights (`fleet1_4` L8);
`experiments/e16_lastwish/laneFORCED/RESULT.md`;
`experiments/e17_pure/DOSSIER.md` §5.7, §8.4.

This is fence F2 as counter-evidence. **The same structural properties that §2.5
reports for 88s hold for 97 @ 3, 92 @ 4 and 89 @ 5.** They are facts about
MixColumns SLPs in this basis, **not a signature of the 88 plateau.** The
`N`-independence table from the dossier, verbatim in substance:

| fact | why it cannot filter an 87 |
|---|---|
| `Y ≥ κ − 6` | measured on 88s; a hypothetical 87 is free to do worse, and that is precisely the regime the bound is about |
| the `s₀` prohibition (`s₀` never a signal, 0/18,355) | the derivation that finally explained it is gate-count-free; e15's own verdict: *"DISQUALIFIES NOTHING"* |
| the `N6` operand-counting identity | exact 13/13, `N`-independent by inspection; banned as a filter at source |
| `88 = 32 + 56` | true at every gate count (A2′) |
| the demand algebra `OUT[col,j] = K_j(m) + T_j(x)` | an identity about `M`; applies to an 87 exactly as to an 88 |
| `slack = d − 1` | pure window combinatorics, no gate count in it |
| Theorem T2 / Lemma R / Corollary R* | hypothesis is `\|C\| = L(M)`; no `n` anywhere |
| e16 F-point orbits, 2-mint/3-orphan closure | count-preserving moves from *known 88s* only |
| lane FORCED's growth law | `n = 4..7` miniatures, random/circulant targets, not `M` |

**And the natural "88 must be optimal because it is so well-explained" intuition
is refuted in this problem class.** The forcedness study tested *"a truly optimal
circuit should be forced — there won't be many variations"* over **99 instances
whose true optimum is certified exactly** (`n = 4..7`, `L* = 3..11`; each
certified by the enumerator returning zero irredundant programs at `L* − 1` with
its node budget intact):

| statistic | value |
|---|---|
| families at the TRUE optimum | min 1, **median 10**, mean 121, max 2,813 |
| optima that are actually unique | **22 / 99 = 22 %** |
| optima admitting ≥ 5 distinct families | 64 / 99 = 65 % |
| … among the hardest tier (`L* ≥ 8`) | 23 / 29 = 79 % |
| ratio families(`L*+1`) / families(`L*`) | min 8, **median 65**, max 829 |

**Forcedness *collapses* as instances get harder**: fraction unique runs
100 % → 50 % → 41 % → 22 % → 13 % → 23 % → 0 % → 0 % → 0 % as `L*` runs 3 → 11.

> **Multiplicity of structurally distinct optimal programs at level `L` is NOT
> evidence that `L` is above the true optimum.** Rarity shows up as a *count
> drop* from `L*+1` to `L*` (median factor 65), not as uniqueness.

This cuts both ways and is listed here for honesty: it neutralises the *strongest
argument against* 88 (the plateau's enormous width), but it equally neutralises
any argument *for* 88 built on how forced the 88s look. **Scope:** miniatures
with random/circulant targets, not `M`; the lane says in its own words that
nothing there bears on `56 ≤ L(M) ≤ 88`.

### 3.5 The class-conditional problem

**MEASUREMENT + named defect.** `wrapup/LEADS.md` §B counterweights (`fleet5_8`
L7, `fleet9_12`); `experiments/e17_pure/DOSSIER.md` §8.3.

Most of §2.4 prices 88 *within a modelled class*. The classes are not proved to
contain an 87.

* **Every "88 is the class optimum" statement is class-conditional**, and the
  class's own load-bearing assumption — lane A's wiring condition, flag F3 — is
  **measured on 22 circuits with one exception and never proved**.
* The block-strata evidence is a **14-for-14 regularity among 88-gate
  circuits** — *exactly the population that would look regular if 87 lived
  somewhere else.*
* **All of the block reasoning lives inside a block partition that was never
  measured on any circuit** (defect D22, LIVE), and `91@6` gate 70 is an
  existing circuit that **no fleet8 block can represent**. **An 87 that crosses a
  block boundary is exactly as possible today as it was before fleet12 started.**
* The `k = 14` decision (§2.4.2) **returned UNSAT on 2026-09-01**, and it says
  nothing about an 87 that does not respect the block strata at that cell. What
  it excludes is an 87 sharing the block structure of every known 88; what it
  leaves untouched is everything outside that decomposition.

### 3.6 What a proof would minimally require

**THEOREM (refereed) throughout — these are proved or measured ceilings, not
opinions.** `experiments/e17_pure/DOSSIER.md` §5.8, §5.5, §6, §7, §9;
`wrapup/LEADS.md` §C.

#### 3.6.1 Every unconditional family in the repository has a ceiling below 88

| family | ceiling / verdict |
|---|---|
| Linear counting / LP over the measured basis | best possible bound **46.2** against a target of 88; reproduces at region scale |
| Tower rungs | `L3 ≤ 51` and `L2 ≤ 26` are *verified circuits* and the tower is monotone ⇒ **every bound from a tower rung is capped at 51 / 26** — both below the refereed 56. Exact `L2`, `L3` cannot improve `L(M)` at all |
| Lemma P (projection / visibility) | capped at `32 + minE_φ`, measured 36–40 |
| Generalised heavy-corner rank ledger | **52** |
| Edge counting | 33, and refuted by the records |
| The `C_c` family | **73** even at `c = 0`; on `M`'s own rung **71**; under the coarse hypothesis **67** |
| Reductions as a proof shape | **cannot see re-optimisation value by construction** — zeroing a column deletes exactly `fanout` gates in all five 88s, cascade exactly zero, mean 1.91, but the truth is 2.83 per column. The ~0.9 gate/column difference is invisible to **every** reduction, however clever |
| Charges as a proof shape | cannot exceed the target count |
| Quotient composition | proved there is **no theorem to find** (Route-2 exactness) |
| Sector localization | *there is no sector-localization lemma, and the record circuits are the proof that none can exist* |
| The backward identity `F = 64 + a − c − 2d` | **circular as stated**; a change of variables carrying zero information |
| The ≥5-plane tier | **unbuildable, not merely unused** — buildable rate 0.0000 at `p = 5..8`; 0 of 7,755 offered masks ever selected across 89,003 floors |

> **Every unconditional family in the repository has a proved or measured ceiling
> strictly below 88, except one.** The exception is `L_cf(M) ≥ 92` — and that
> route has a **proved ceiling of 83.000** on a verified 88-gate circuit
> (`88@5fs`), refereed in exact `Fraction` arithmetic. **The ceiling is not the
> LP's fault**, which means the prescribed fix does not exist.

Two historic routes to `57+` turned out to be **their own conclusions in
disguise**, and this is a theorem, not a failure of effort:

* **`C_c` telescopes to the `minE` question** it was proposed as an alternative
  to. Via `L(M|_Λ) = 32 + minE_Λ`, `C_c` *is* the statement that `minE` grows by
  ≥ 2 per column along the nested chain. The stages it needs at small `c` are
  literally the `minE` purchases at `|K| = 15, 16, …` that lane C priced at
  **pod-months**.
* **Slope-2 `Y`-lemmas are equivalent to the conclusion.** By Theorem Y2 at
  `α = 2, c = 4`: *"`Y ≥ 2κ − 4` for every SLP with `n ≤ 87`" is **equivalent**
  to `L(M) ≥ 88`.* Any proposal of the form "a slope-2 `Y`-lemma buys 88" should
  be struck on sight.

#### 3.6.2 The certificate LP is capped at 91.41 — a dead end, precisely located

**THEOREM (refereed).** `experiments/e17_pure/REF_CONTRA/VERDICT.md` V14, V14b,
V14c, V6c; `fleet7/laneUNCOND/RESULT.md` §4.2; table
`fleet7/laneUNCOND/results/bstar/nostop_lp_cert_4_1.json`.

The referee loaded the banked price table and ran **its own** Check 1 and **its
own** DP, using no code from either lane:

```
priced masks outside supp(t) : 0        negative prices : 0
Check 1 max column sum = 10000000 / 10000000 = 1.0000000   FEASIBLE, exactly tight
B = 914098776 / 10^7 = 91.4098776
```

`ceil(B) = 92`, re-deriving `L_cf(M) ≥ 92`. The LP **optimum** is
`B* = 91.409884` (GLOP; grade: unrefereed; its solver-free lower half
`91.4098776` is what the referee rebuilt).

Two upgrades were proposed and **both are refuted**:

* `B > 92` (giving `L_cf ≥ 93`, and the cancellation budget at 87 rising 5 → 6)
  and `B > 91.9738 = 87 + 2·δ₇` (giving `|A*| ≥ 3` for every 87 unconditionally)
  **both lie above the LP optimum 91.409884. Neither is reachable by optimising
  this LP at all, symmetric or not.**
* **The symmetry lever is worth nothing at the optimum**: symmetrising the banked
  table gains `91.4098776 → 91.4098779`, i.e. **`+0.0000003`**. The LP optimum is
  already `ρ`-symmetric to seven places. The `+0.177` measured elsewhere is the
  distance from one non-optimal table to a partially re-symmetrised version of
  itself.
* The "0.79 of `B` away" framing is **unsound in kind**: `δ₇` is a functional of
  the *same* table, so the threshold moves with `B` — measured,
  `B: 90.9545 → 91.1793 → 91.4099` moved `δ₇: 2.4708 → 2.4869 → 2.5044`.

> **Do not fund a `ρ`-symmetric price optimisation.** The one open item on that
> line is a **certified rational dual** to close `B*`'s upper half, scoped at ~1
> session.

#### 3.6.3 The two live conjectures, and what they are worth together

**Grade: CONJECTURED.** `experiments/e17_pure/DOSSIER.md` §6.

1. **`H_min`: every *minimal* SLP for `M` satisfies `Y ≥ κ − 6`.**
   Price: `L(M) ≥ G(2) − 6 = 58`, one line, using no P1/P2/chain. **Unrefuted.**
   Corpus-consistent and **tight if `L(M) = 88`**: over the 3,254-circuit census
   the minimum of `Y − κ` is exactly **−6**, attained by **43 explicit
   witnesses** (the eight disk circuits alone give only −5, so `c ≤ 4` dies
   without the census). ⚠ The price 58 needs `G(2) = 64`; if `G(2) = 63` it is
   57. ⚠ The quantifier is load-bearing: the version quantified over *all* SLPs
   is **refuted** by Theorem Y4 with six oracle-VALID trim witnesses reaching
   `Y − κ = −399`.

2. **`G_int(3) ≥ 92` ⟹ `κ ≥ 3` and `|A*| ≥ 3` for every 87** — and therefore
   **branch 3 of the Anatomy Theorem does not exist.** This is the cheapest
   single number on the board.

> **Under the most generous simultaneous grant** — `C_0` proved, `Y ≥ κ` proved
> (`c = 0`), `δ(mc) ≥ 3` proved `N`-dependently — **the conjunction yields
> `L(M) ≥ 73`. `H87` survives all three.** No combination of the currently-live
> conjectures reaches 88.

#### 3.6.4 The wall, named

**`Sub-lemma CONF` (confinement).** The only relaxation that is **exact on all
nine circuits tested**, `88@5fs` included, is laneTOOL2's Theorem T4
(`|C| ≥ |A_all| + Φ_D(A_all)`). Its unconditional form — **Lemma OP**: minimise
`|A| + Φ_D(A)` over mask sets *and* over a choice of cancelling operand pair for
each, and show the minimum is ≥ 88 — **would refute `H87` outright.** The gap is
`64 → 88`, twenty-four gates (the degenerate configuration `A = T` prices at 64).

The named obstruction: **operand masks are not confined to `U`, so the
optimisation is not a finite computation as posed.** The concrete first step is

> **Sub-lemma CONF: in a minimum-size SLP for `M`, every cancelling gate's
> operand masks lie in an explicit finite universe `V ⊇ U`.**

With CONF, Lemma OP becomes a finite optimisation of exactly the shape `G(λ)`
already has code for. **Without CONF the problem is not even finitely posed.
Nobody has a candidate `V`. It is the honest name of the wall.**

#### 3.6.5 Three numerals a proof would rest on, and their actual status

**These are the places a successor could build on sand.**
`experiments/e17_pure/DOSSIER.md` §7; `wrapup/day2/STEWARD.md` §S2.

| numeral | what rests on it | actual status |
|---|---|---|
| **`G_int(3) ≥ 92`** | `κ ≥ 3` at `n ≤ 87`; `\|A*\| ≥ 3` for every 87; `κ ≥ 18` at `n ≤ 57`; **the deletion of branch 3** | **Single source, never re-verified by anyone.** It is `BestObjectiveBound() = 92` reported at status **FEASIBLE** after 1,200 s on 4 cores with incumbent 94 — a solver's dual bound *at the moment the clock ran out*, bracket [92, 94], with no status backing it. **The only inherited numeral in the programme that currently changes a conclusion.** The referee-checkable form is one CP-SAT run: `obj ≤ 91` **INFEASIBLE**. Measured cost 2026-08-29: 3–12 h at 1 worker, **with a material chance of returning UNKNOWN and banking nothing**; a ladder driver that banks every rung permanently is drafted at `wrapup/day2/tools/gint3_recert.py` (verified working: `B = 31 → INFEASIBLE in 3.4 s ⇒ G_int(3) ≥ 32`). A free 4× is available by breaking the `Z/4` gauge, which the `G_int` encodings use **not at all**. |
| **`G_int(2) = 64`** | the price `L(M) ≥ 58` for `H_min`; everything numerical in laneY §4.1/§4.2 | **UNPROVEN-AS-STATED.** One 4-core log line is the entire positive evidence; **two independent re-verifications failed** (laneY's own encoding, 900 s, 1 core → FEASIBLE, best bound 32.0; the referee's decision-form encoding → UNKNOWN after 600 s). The three encodings were verified to agree **structurally**, so the gap is solver behaviour, not modelling. `G(1) = 32` **was** independently reproduced and has a two-line hand proof. |
| **A11's numerals 7,362 / 19,490** | the only gate-count-asymmetric fact in the programme | **Computed under `pbar`, not the banked table.** The `n = 87` branch is airtight under both tables (738 and 475 pairs, both at 100 % forcing), so the asymmetry is robust — but the `n = 88` recount under the banked table **has never been run**, and it costs seconds (`wrapup/CORRECTIONS.md` C-48a). |

A fourth, for the record: the covering bonus `m = 1` is included in the refereed
`56 = m + 18 + 37` but **omitted** from the quoted `C_c` ceiling `73 = 2·18 + 37`
and from `67 = 2·12 + 1·6 + 37`. If `m` survives a 2-payment upgrade the figures
are **74 and 68**. Nothing depends on the resolution, but a successor quoting
"the `C_c` family stops at 73" should know the figure is convention-dependent by
exactly one gate.

### 3.7 Named artifacts that must not be over-cited

Collected so that nobody rebuilds a claim on them.

* **E6's flagship 88 does not exist on disk.** `cpk.oracle()` writes the circuit
  to `tempfile.mkstemp` and the caller never persists it; the circuit exists only
  as an oracle **verdict string** in one ledger row. **It must not be cited as an
  on-disk verified circuit**, and reconstructing it is a ~3,762 s CP-SAT run
  (`experiments/e6_cancelplan/ADDENDUM_20260829.md`).
* **The "22 + 5 backbone" picture is falsified** and must never appear in a
  public structural claim (`wrapup/CORRECTIONS.md` C-37).
* **DAG statistics are dead as frame invariants** — mask-identical circuits can
  disagree on them. They are fine as verification output; they are not structural
  facts. "Max width ≤ 8" and "no < 20 opening pairs" were never universal
  (C-43).
* **Three atlas claims about the socle plane are refuted by atlas's own unread
  output**, and the refutation is much larger than first reported (§3.8).
* **fleet12 holds 135 88-gate circuit files but only 21 distinct mask sets**; all
  75 files in `laneORDER/out` are byte-identical. **Never publish a file count as
  a population size** (`wrapup/CONFLICTS_RESOLVED.md` §S9).
* **`fleet8/unified`'s 25 timeout rows collapse to 20 distinct instances** —
  byte-identical block subproblems generated by different lean menus. Counting
  rows overstates coverage by 25 %.
* **The atlas V1.5 corpus is ~14 % complete** (34,112 of ~236,000 instances).
  The word "exhaustive" must never be applied to it (§S14).
* **The vacuity ledger** (`fleet7/laneCONSOLIDATE/STATE_OF_THE_PROBLEM.md` §3.2)
  lists published negatives later withdrawn as carrying no information because
  their controls never fired. **Anyone mining this repository for "X was ruled
  out" must check that list first.**

### 3.8 The two cheap 87 routes point in opposite directions

**MEASUREMENT, new 2026-08-29.** `atlas/corner/ANALYSIS_20260829.md` LEAD-2,
§4.4, §6.

Two independent structural routes to an 87 have been proposed in this project:
`atlas/thinktank/phase2_tower.md` §7.1 and `third_frame.md` C2 want an 87
anchored at **low `l3`** (small socle skeleton); `experiments/e17_pure` branch 3
wants one at **`|A*| = 2`**. Measured across two independent corpora:

* `l3` vs `|A*|`: **`r = −0.854`** over the 498 corner circuits, **`r = −0.553`**
  over 800 census circuits. `l3` vs `κ`: `−0.781` / `−0.256`.
* Concretely, over the 498: `κ ≤ 23 ⇒ l3 ∈ [74, 79]`; `κ = 33 ⇒ l3 ∈ [64, 66]`.
  All ten census 88s at `l3 ≤ 60` have `κ = 33`, `|A*| = 29`.

> **Driving one route's target down drives the other's up. A search that tries to
> satisfy both is aiming at a region no observed 88 occupies, and a search
> anchored at the record `l3 = 57` is anchoring at `|A*| = 29` — the opposite end
> of the branch-3 region.**

*Caveat, stated by the source:* correlation over 88s need not extend to 87s. It
is evidence about where 88s live, not a theorem, and must not be published as a
bound.

The same pass also corrected the socle-plane literature outright, and the
corrections are safe to publish as written:

* **There is no `l3 ≥ 67` floor for 88.** Over the corner sweep `l3` runs
  **continuously 64 → 79 with every integer occupied**; over the 17,283-circuit
  e15 census it reaches **`l3 = 57`** (attained by three distinct circuits), with
  **570 circuits at `l3 ≤ 66`**. The 67 was a sample-size artifact of nine
  circuits.
* **The "empty band `l3 ∈ 69..72`" is the most densely populated part of the 88
  level set** — 70 corner circuits and **7,867** census circuits.
* **There is no "real 2-gate ridge."** The smoking gun is inside the session that
  claimed it: the walk launched from `SH_l70_90.txt`, the very 90-gate circuit
  used to price the band at 90, **descended to 88 in that same session**,
  emitting seven 88-gate rows at `l3 = 64, 65, 65, 66, 66, 66, 66`.
* **The left shoulder of the socle-plane envelope is at 88, not 89.**
  `corner/envelope.py` as published understates the envelope over the whole range
  `l3 ∈ [57, 66]`, because it reads only `out/*.txt` and `work/*.BEST.*.txt` and
  explicitly skips `.plat`.

And one honest deflation of a headline claim: the 498 corner 88s are **not the
best socle anchors known**. The census beats them at every depth but 6. What
survives is narrower and true: **`l3 = 64` at depth 6 is a genuine repository
record for its depth**, and the `sh.l70` family is the only low-`l3` set that is
simultaneously far (overlap ≤ 50 of 88 masks) from every published 88.

### 3.9 The never-searched region is also never-populated

**MEASUREMENT.** `atlas/corner/ANALYSIS_20260829.md` §3.4;
`wrapup/LEADS.md` §10.

The `{p,q}` tap-profile region that `wrapup/LEADS.md` §10 and
`experiments/e17_pure/DOSSIER.md` §4.5 branch 3 identify as never searched
requires `|A*| = 2`, `κ = 2`, `Y = 0`. Measured over the 498:

* `|A*|` histogram `18:90, 19:97, 20:14, 21:88, 22:30, 23:79, 24:17, 25:73,
  27:8, 29:2` — **minimum 18, nothing within 16 of the region**.
* `κ` histogram minimum **20**.

> **None of the 498 falls in a never-searched profile region.** What they do is
> push the observed `κ` floor for 88s from 22 (records) / 24 (census sample) down
> to **20** — a 2-gate move in the right direction and **18 gates short** of the
> region.

This cuts both ways and both readings should be stated. **For 88:** the branch-3
region is empty of 88s across every population ever measured. **Against:** it is
also *unsearched*, and the reason nothing has been found there is that nothing
has looked. `L(M) = 88` does not follow from "nobody looked in the one place
where the arithmetic still permits an 87".

---

## 4. The shape of an 87, if one exists

This is the material an optimality proof would open with, and it is also the
target specification for anyone still hunting. **Every property below is a
necessary condition on a hypothetical 87, with its exact precondition stated.**

Source: `experiments/e17_pure/laneCONTRA/RESULT.md` §1–§3 **as corrected by**
`experiments/e17_pure/REF_CONTRA/VERDICT.md` (V9, V11, V14d, V6c, V14c),
compiled at `experiments/e17_pure/DOSSIER.md` §4, plus the measured floors of
§2.5.4 above. Grade: **THEOREM (refereed)** throughout §4.1–§4.3.

### 4.1 The frame — and why it is stated this way

Everything below is about the hypothesis

> **`H87`: there exists an XOR-SLP for `M` with at most 87 gates.**

We do **not** reason about "an 87" as a free-floating object, because
irreducibility would then have to be *assumed* — the circular failure this
project has been burned by before. Under `H87` take `C` a **minimum-size** SLP;
`|C| = L(M) ≤ 87`. Two reductions make the frame legitimate, both refereed:

* **R1 (no zero mask).** If a signal has mask `0`, its two operands carry equal
  masks; delete the gate and rewire every consumer to either operand. Strictly
  smaller. So a minimum SLP satisfies **H0**, discharging the load-bearing
  hypothesis of Theorems P1 and P2. (H0 is genuinely load-bearing: an independent
  agent exhibited SLPs where dropping it breaks the sub-lemma.)
* **R2 (distinct masks, irreducibility).** If two gates carry the same mask, keep
  the earlier and rewire; if a non-output gate has no consumer, delete it. Either
  move is strictly smaller. This is §2.2.1's `B = 56` argument run at 87, giving
  `B = 55`.

> **Every conjunct below must be read with the word "minimum" in front of it.**
> An 87-gate SLP with a duplicated mask is covered by *no* conjunct here — and
> correctly so, because it contains an 86.

*The honest cost of the frame:* `H87` gives a minimum SLP of size `L(M)`, which
may be 86 or less. Each conjunct is stated at `n = |C|` and evaluated at
`n = 87`; each is monotone in the right direction, so a conjunct proved at 87
holds a fortiori at `n ≤ 87` **unless the arithmetic changes the case split** —
and where it does (the `|A*| = 2` analysis), the `n ≤ 86` branch is handled
explicitly by A8′.

### 4.2 The constants

Under the banked price table
`fleet7/laneUNCOND/results/bstar/nostop_lp_cert_4_1.json` (**use this table, not
`pbar`** — successor instruction, verbatim from the referee):

| quantity | value |
|---|---|
| `B` | **91.4098776** |
| requirement `B − n` at `n = 87` | **4.4098776** |
| `δ_w := max{ D(m) − 1 : m ∈ U, wt(m) = w }`, `w = 2..7` | **0, 0.9999998, 1.9912788, 1.5872092, 2.0429066, 2.5044082** |

Two properties of the `δ` vector, both surviving an **8-table control**:

* **`δ₂ = 0` exactly, 8/8.** A weight-2 cancelling leaf contributes **nothing**
  to the budget. ⚠ This is a statement about a *tight Check-1 column* — about the
  certificate, not about `M`. Whether a feasible table with `δ₂ > 0` exists is
  **an LP question nobody has asked**.
* **`δ₅ < δ₄`, 8/8 — the constants are NOT monotone in `w`.** A weight-5
  cancelling leaf is worth less budget than a weight-4 one, though the crude
  weight form prices it at 3 against 2. **Any successor writing an integer
  program over the cancellation budget must use this table, not `wt − 2`.**

### 4.3 The forced properties, each with its precondition

Let `C` be a **minimum-size** SLP for `M` under `H87`, `n = |C| ≤ 87`.

| # | forced property of any 87 | precondition it needs | grade |
|---|---|---|---|
| **A1** | All `n` gate masks pairwise **distinct**, nonzero, not input singletons; **every non-output gate has a consumer** | minimality (R1, R2) | refereed |
| **A2** | Exactly **32 finals** (gates carrying target masks); the remaining `n − 32` are **middles**. At `n = 87`: **55 middles** | targets have weight 5 or 7, so none is an input; all 32 distinct; A1 gives one gate each | refereed |
| **A2′** | ⚠ **A2 filters nothing by itself** — `88 = 32+56` and `87 = 32+55` are the same identity | — (recorded so no successor re-derives it as content) | refereed |
| **A3** | **No final's two operands are both targets**; every final consumes at least one non-target signal | `M` has rank 32, so no row is the sum of two rows | refereed |
| **A4** | **`κ ≥ 2`** — at least two cancelling gates | Theorem P2 + Lemma D, via `κ ≥ (B − n + Y)/δ₇` | refereed |
| **A5** | `A* ⊆ U`; every member of `A*` is a cancelling gate's mask and a submask of some target row; **cancellation weight budget `Σ_{m∈A*}(wt(m) − 2) ≥ 92 − n`, i.e. ≥ 5 at `n = 87`** | Theorem P1 with the refereed `L_cf(M) ≥ 92`, and hypothesis **H0** | refereed |
| **A6** | **Every weight-7 member of `A*` is one of the 12 weight-7 MixColumns rows**, and the gate carrying it is a cancelling gate whose output *is* that row | `m ⊆ supp(t)`, `wt(m) = 7`, `wt(t) ∈ {5,7}`; `\|U₇\| = 12` verified | refereed |
| **A7** | **The weight-profile inequality.** With `a_w = #{m ∈ A* : wt(m) = w}`: **`Σ_w a_w·δ_w ≥ B − n + Y`** | Lemma D + P2 + `κ ≥ \|A*\|`; **table-dependent** (use §4.2's) | refereed |
| **A8** | **`\|A*\| ≥ 2`; and if no member of `A*` has weight 7 then `\|A*\| ≥ 3`** | A7 at `n=87, Y=0` needs ≥ 4.4098776, while `2·δ₆ = 4.0858132` | refereed |
| **A8′** | `\|A*\| ≥ ⌈(B − n)/δ₇⌉`. In particular **`\|A*\| = 2` is arithmetically impossible at `n ≤ 86`** (there `≥ 3`); `≥ 4` at `n ≤ 83`; `≥ 5` at `n ≤ 81` | `2·δ₇ = 5.0088164 < 5.4098776 = B − 86` | refereed |
| **A9** | **`Y ≤ δ₇·κ − (B − n)`**; in particular **`κ = 2` forces `Y = 0`**, and **`\|A*\| = 2` forces `κ = 2` and `Y = 0`** | rearrangement of A4's chain; uses `κ ≥ \|A*\|` | refereed |
| **A10** | **If `\|A*\| = 2` then one of the twelve weight-7 MixColumns rows is produced by a cancelling gate.** Under the banked table exactly **475** weight-admissible pairs exist at `n = 87` — profiles `{4,7}` 63, `{6,7}` 346, `{7,7}` 66 — and **475/475 contain a weight-7 target row** | A7 admits only those three profiles at `n=87`; A6 identifies weight-7 members. ⚠ **table-contingent**: holds on 5 of 8 feasible tables, including failing on one with a *strictly larger* `B` than a table it passes. Under the banked table the margin roughly **doubles** (`+0.3582982` vs `pbar`'s `+0.1781170`) — not a knife edge, but **anyone who re-optimises the table must re-run this check** | refereed, table-contingent |
| **A11** | ⚠ **A10 is gate-count-ASYMMETRIC — the only such fact in the programme.** At `n = 88` the same computation admits ten profiles and only **7,362 of 19,490** admissible pairs contain a weight-7 target row: **the statement is false at 88** | ⚠ the `n = 88` numerals are computed under `pbar`; the banked-table recount has never been run (§3.6.5) | refereed |
| **A13** | e16's 2-mint/3-orphan closure and the thirteen closed F-point orbits constrain an 87 not free-move-connected to a known 88: **not at all** | both move sets are count-preserving | refereed, as a scope statement |
| **A14** | The joint-level ladder `k = 9..13 UNSAT` constrains an 87: **not at all** | only `SAT at k = 14` would have produced one — and `k = 14` came back **UNSAT, 2026-09-01** (§2.4.2), so the completed ladder `k = 9..14` still constrains an 87 outside the block decomposition **not at all** | refereed, as a scope statement |

**Measured floors that are NOT theorems but constrain the search** (§2.5.4;
grade: MEASUREMENT over 1,303 88s):

| observed floor | population | precondition to promote it |
|---|---|---|
| `\|A*\| ≥ 18` | 498 corner + 800 census + 5 records = 1,303 valid **88s**; minimum attained by **90** circuits | a proof for **minimum-size SLPs**, not for 88s. If any `\|A*\| ≥ c` with `c > 2` were proved, **branch 3 collapses** |
| `κ ≥ 20` | same 1,303; minimum attained by **31** circuits | same |
| glue `≥ 2` | same 1,303; minimum attained 5 times, never 0 or 1; 0 glue is reachable at **91** gates | a pricing lemma: *"an 88 needs ≥ 2 glue gates and glue costs ≥ x"* |
| every valid 88 is **non-deletable** | 27,888/27,888 single-mask deletions over 498 circuits (§2.2.3) | corpus-wide extension (LEAD-1, ~2 CPU-days Python / minutes in C) |

⚠ **The gate-count-asymmetry warning applies to all four rows.** They are
measured on 88s and the target statement is about 87s. A11 is the standing proof
that such statistics *can* differ between 87 and 88.

### 4.4 The complete case analysis under `H87`

By A8′, `|A*| = 2` cannot occur at `n ≤ 86`. So **exactly one** of:

1. **`L(M) ≤ 86`**, and then `|A*| ≥ 3` (≥ 4 at ≤ 83, ≥ 5 at ≤ 81);
2. **`L(M) = 87` and `|A*| ≥ 3`**;
3. **`L(M) = 87` and `|A*| = 2`**, and then `κ = 2`, `Y = 0`, the weight profile
   of `A*` is one of `{4,7}` (63 pairs), `{6,7}` (346), `{7,7}` (66), and **one
   of the twelve weight-7 MixColumns output rows is produced by a cancelling
   gate.**

**Branch 3 is the one an adversarial search should be pointed at.** It describes
a circuit with **exactly two cancelling gates and eighty-five clean ones** —
nothing like any of the eleven wired circuits on disk (`κ = 9..28`), nor like any
of the 1,303 88s measured in §2.5.4 (`κ ≥ 20`). **The `{4,7}` profile — 63 of the
475 — is the branch nothing has pressure on.**

**One CP-SAT run deletes branch 3.** `G_int(3) ≥ 92`, re-certified as an
infeasibility at `obj ≤ 91`, gives `κ ≥ 3` at `n ≤ 87`; with A9 (`|A*| = 2 ⇒
κ = 2`) and A8 (`|A*| ≥ 2`), **every 87 would have `|A*| ≥ 3` and branch 3 would
not exist.** Status of that numeral: §3.6.5.

### 4.5 In one sentence

> Any **minimum-size** 87-gate SLP for MixColumns has 32 finals and 55 middles
> with pairwise distinct masks, no dead gate, no final built from two targets, at
> least two cancelling gates, at least two distinct cancelling-gate masks
> appearing as leaves of maximal clean trees, a cancellation weight budget of at
> least 5 spread over a weight profile satisfying `Σ_w a_w·δ_w ≥ 4.4098776`,
> **no budget contribution at all from weight-2 cancelling leaves**,
> `Y ≤ 2.5044082·κ − 4.4098776`, and — if its cancelling apparatus is as small as
> the arithmetic permits (`|A*| = 2`, forcing `κ = 2` and `Y = 0`) — **a
> cancelling gate whose output *is* one of the twelve weight-7 MixColumns rows.**

---

## 5. What would settle it

Ordered by value per unit of compute. Nothing below is scheduled; the search
phase is over and these are recorded for a successor.

| # | item | what it decides | price |
|---|---|---|---|
| **1** | **Re-certify `G_int(3) ≥ 92` as an infeasibility at `obj ≤ 91`** | **Deletes branch 3 of the case analysis** — the only branch describing an 87 unlike anything ever built. The only inherited numeral that currently changes a conclusion | one CP-SAT run; measured 3–12 h at 1 worker with a real chance of UNKNOWN. **Break the `Z/4` gauge first** — a free 4×, unexploited by these encodings. Buy `G_int(2) = 64` (`--lam 2 --bounds 63`) on the way past: minutes, and it fixes a second flagged foundation |
| **2** | **Run the deletion-realisability test corpus-wide** (§2.2.3) | If any 88 in the 1,575,516 admits a realisable single-mask deletion, that is **an 87 by construction**, immediately oracle-verifiable. If none does, it is the strongest deletion certificate the project could publish | needs only mask sets, no solver; `O(120²)` filter per circuit, ~11 G integer ops — **~2 CPU-days pure Python, minutes in C**, shardable and `nice`-able. Working implementation exists |
| **3** | ~~**Decide `k = 14`** on the merged `W3 ∪ U4` block~~ — **SETTLED 2026-09-01: UNSAT** (§2.4.2; `fleet11/laneCUBE/RESULT.md` §7.1) | It was the only place in the project where a single machine decision could still produce an 87 within a modelled class. It produced none: `merged = 15`, the class closes, **no 87 exists that shares the block structure of every known 88**. **Remaining, and both optional:** (a) the fully independent **cross-encoding re-decision** at `k = 14` on fleet8's `dslp` CNF — the only check that would make the verdict encoding-independent; (b) letting the three other monolithic engines finish as engine-level confirmations. Neither can produce an 87; neither touches an 87 outside the block decomposition | (a) ~10× the `k = 13` cost — hundreds of core-hours, **not recommended**; (b) free, already running. The decisive solve cost **356,321.63 core-seconds (≈ 99 core-hours)**, kissat-4.0.4, well under the 653–1113 forecast |
| **4** | **Re-seed the descent at the 89** (§3.1) — **launched 2026-08-29 11:36, result pending** | Reaching 88 gives the **first 88-gate MixColumns circuit outside the corpus vocabulary** — a new structural object and the entrance to unsampled plateau. Failing repeatedly is the sharpest available evidence that the plateau really is confined to its dictionary | **~1 core-hour for a first answer**; ~20 core-h for all 20 non-appendix floors. Two-line seed change to an existing harness. Cheapest by an order of magnitude. Ledger: `wrapup/day2/e_upstream/seed89_ledger.jsonl` |
| **5** | **A certified rational dual for `B*`**, closing `91.4098776 ≤ B* ≤ 91.409884` | The only remaining purchase on the certificate-LP line | ~1 session |
| **6** | **Prove `\|A*\| ≥ c` for some `c > 2`** for minimum-size SLPs | Collapses branch 3 unconditionally; reduces the case analysis to two cases | unknown — a question for the e17 `Φ`/`B(A)` DP machinery, not a search |
| **7** | **Sub-lemma CONF** — a finite universe `V ⊇ U` confining cancelling operands | Makes **Lemma OP** finitely posed; Lemma OP proved ≥ 88 **refutes `H87` outright** | **Nobody has a candidate `V`.** This is the wall (§3.6.4) |
| **8** | `minE_K` at the newly-found admissible `\|K\| = 13` keep-sets | Needs `minE_K ≥ 4` to *match* 56, `≥ 5` to *beat* it | **unpriced — nobody has computed it.** Two explicit keep-sets are given in `experiments/e17_pure/DOSSIER.md` §5.4 |
| **9** | ~~Exact max-fan-out re-scheduling (class C4)~~ — **DONE 2026-08-29**: structural, not an artifact (§2.5.2). Remaining: widen it past the 39 mask sets | Whether fan-out ≥ 8 is unreachable across the whole corpus, not just the records and the e_upstream floors | the identical exact model over a stratified 150-circuit sample is **running**; `wrapup/day2/e_upstream/c4_corpus_sample.json` |
| — | ~~`ρ`-symmetric price-table optimisation~~ | — | **DO NOT FUND** (§3.6.2): both thresholds lie above the LP optimum, and the symmetry lever is worth `+0.0000003` |
| — | ~~More `k ≤ 3` shell completion~~ | — | **DO NOT FUND**: radius-≤4 negatives are worth ~nothing (F1) |
| — | ~~The depth-3 `d3bound` ladder~~ | — | **NO-GO** (`wrapup/day2/STEWARD.md` §S1): realistic ceiling ≈ 66–70, against an independently certified `N_depth3 ≥ 80` already on disk. The route's own hard ceiling is 65 in `pq` units, and `pq ≥ 56` would be needed for "no 87 at depth 3" |

---

## 6. The evidence table

Every item, its type, the population it covers, and where to find it. **Type**
uses the §0.2 grades. **Bears on 87?** answers fence F2: does the statement's
instance at `n = 87` differ from its instance at `n = 88`?

### 6.1 Theorems

| # | statement | type | population / scope | bears on 87? | citation |
|---|---|---|---|---|---|
| T1 | `L(M) ≥ 56` | THEOREM (refereed) | unconditional | **yes** (it is a bound) | `atlas/thinktank/{lower_bound.md §4, referee_55.md}`; `atlas/NOTEBOOK.md` ~725–728 |
| T2 | `L(M) ≤ 88` | THEOREM (witness) | 8 hash-pinned records + 1,575,516 mask sets | yes | `evidence/circuits/spectrum.json`; `wrapup/CORPUS88.md` |
| T3 | `L_cf(M) ≥ 92`, solver-free certificate | THEOREM (refereed) | unconditional | yes — **the only proved quantity above 88** | `beat88/understanding/CANON.md` §U6-2 |
| T4 | `L_cf(M) ≤ 102`, explicit witness (`κ = 0`, depth 5) | THEOREM (witness) | one circuit | yes | `beat88/understanding/v2_no_vocab/data/cf_incumbent.json`; `wrapup/CONFLICTS_RESOLVED.md` B1 |
| T5 | `N_depth3 ≥ 80` — exact rational dual, 72,830 × 29,180 | THEOREM (refereed) | all depth-≤3 circuits | yes | `campaign_87/wave6_2026-08-11/lower_bound/cert_depth3.json` |
| T6 | Depth frontier **97@3 / 91@4 / 88@5** | THEOREM (witnesses) | 3 oracle-verified lineages at 91@4 | yes | `wrapup/CONFLICTS_RESOLVED.md` B7 |
| T7 | **`B = 56`** on any irreducible valid 88; contrapositive is an 87 detector | THEOREM (unrefereed) | all valid 88s | **no** by itself (`B = n − q` at every `n`) — but its **contrapositive is a decision rule**, exempt from F1 | `experiments/e15_campaign3/AUDIT.md` §11.4 |
| T8 | **THE ANATOMY THEOREM**, conjuncts A1–A14 | THEOREM (refereed) | any minimum-size SLP with `n ≤ 87` | **A11 only**; A1–A10 are `N`-independent shape facts | `experiments/e17_pure/DOSSIER.md` §4 |
| T9 | Theorem P1 — cancellation weight budget `Σ(wt−2) ≥ 92 − \|C\|` | THEOREM (refereed) | any SLP with H0 | yes (`n` appears) | `fleet2/laneP_proof/RESULT.md` §1.2 |
| T10 | Theorem P2 — `\|C\| ≥ κ + Y + B(A)`; **exactly 88.000 on `88@7`** | THEOREM (refereed) | any SLP with H0 | yes | `fleet2/laneP_proof/RESULT.md` §1.3 |
| T11 | Theorem T2 — private-cone tree theorem; `minrep = \|D(c)\|+2` exactly | THEOREM (refereed) | any SLP with `\|C\| = L(M)`; confirmed over **57,139 optimal SLPs / 181 matrices**, 0 violations | **no** (no `n` anywhere) | `experiments/e17_pure/laneDELTA/RESULT.md` §2; `REF_DELTA/VERDICT.md` §2 |
| T12 | Route ceiling **83.000** on `88@5fs` for the whole residual family | THEOREM (refereed) | the P1/P2 relaxation family | yes (it is a ceiling on a proof route) | `fleet2/laneP_proof/RESULT.md`; `experiments/e17_pure/DOSSIER.md` §5.1 |
| T13 | Theorem Y3 — the `(E1,E2,E3,Y-EX)` family's unconditional value is exactly **32** | THEOREM (refereed) | that inequality family | yes (route closure) | `experiments/e17_pure/laneY/RESULT.md` |
| T14 | Theorem Y2 — *"`Y ≥ 2κ − 4` for every SLP with `n ≤ 87`" is **equivalent** to `L(M) ≥ 88`* | THEOREM (refereed) | slope-2 `Y`-lemmas | yes (route closure) | `experiments/e17_pure/DOSSIER.md` §5.2 |
| T15 | Theorem Y4 — `Y ≥ ακ − c` is **false for every `α > 0`, `c`** over all SLPs; six oracle-VALID witnesses to `Y − κ = −399` | THEOREM (refereed) | all SLPs (not minimal ones) | yes (kills the unrestricted form) | `experiments/e17_pure/laneY/RESULT.md` §3.8 |
| T16 | `\|Aut(M)\| = 4`, by complete backtracking | THEOREM (proved) | `M` | n/a | `experiments/e3b_fresh/code/symgf.py` |
| T17 | The merge refinement is worth **exactly zero**; keep-set admissibility is the optimum of the family | THEOREM (refereed) | Theorem-N family | yes (route closure) | `experiments/e17_pure/laneCHAIN/RESULT.md` §2 |
| T18 | `C_c` telescopes to the `minE` question | THEOREM (refereed) | the `C_c` route | yes (route closure) | `experiments/e17_pure/DOSSIER.md` §5.3 |
| T19 | `core(Q1) ≥ 18` for **every** `Q1` at the flagship cell — the flagship-cell 87 door | THEOREM (refereed) | one cell | class-conditional | `fleet3/laneCB_completeness/RESULT.md` + `REFEREE.md` |

### 6.2 Certificates (exhaustive over a stated finite population)

| # | statement | population | result | citation |
|---|---|---|---|---|
| C1 | `B = 56` full-DAG check | **28,796** build-order-bearing 88s | 28,796/28,796; **0 alarms** | `wrapup/CORPUS88.md` §4 |
| C2 | 88 distinct masks, all 32 targets | **1,575,516** distinct 88 mask sets | 1,575,516/1,575,516 | `wrapup/CORPUS88.md` §2 |
| C3 | **Single-mask deletion + arbitrary rewiring** | **88,228,896** deletions over **all 1,575,516** distinct verified 88s (35,323,820 pass the local filter) | **0 realisable** | `wrapup/day2/deletion_cert/CERT.md`; `RESULT.json` (supersedes the 498-circuit pilot: `atlas/corner/ANALYSIS_20260829.md` §7) |
| C4 | overlap-87 intersections of distinct 88s | 35 pairs, all containing the 32 targets | **0 realisable** | same |
| C5 | `k = 2` irreducibility | **139,878/139,878** harvested mask sets; **215,412,120** window decisions, 1,540 each; three disjoint ledgers | 0 reducible | `wrapup/CONFLICTS_RESOLVED.md` §S7 |
| C6 | `k = 3` irreducibility | 200 states × 27,720 triples | 0 reducible; **queue empty** | `wrapup/CONFLICTS_RESOLVED.md` §S7 |
| C7 | `k = 4` (remove-4/restore-≤3) | 56,489 / 39,034 / 34,599 of 367,290 windows on three anchors | 0 reducible | `wrapup/CONFLICTS_RESOLVED.md` §S8 |
| C8 | `d(S) = 1` windows | **15,099,957** over 22 distinct circuits | 0 compressible, 0 shared helpers | `wrapup/CONFLICTS_RESOLVED.md` §S5 |
| C9 | e15 Run-A full-population sweep | **17,283/17,283** — ⚠ **1.1 % of the corpus, 92 % one method** | 0 alarms | `experiments/e15_campaign3/sweep_A_fullpop.jsonl`; F3 |
| C10 | drop-4 refutation at `k = W−1` | **35,960** four-target drop sets on `88@5` | all refuted | `experiments/e5_readd/ledger.jsonl` |
| C11 | drop-4 **screen** (not "refuted") | **35,960/35,960** on `88@5fs`, second family | complete, 0 timeouts | `experiments/e5_readd/ADDENDUM_20260829.md`; residue R3 |
| C12 | free-move orbits (wirings) | **44,793** states, five records | closed; **0 sub-88** | `experiments/e14_plateau87/` |
| C13 | F-point orbits | **333,396** states, eight anchors; combined with C12 = **378,189** | all closed; **0 sub-88**; 4,856,598 re-association sites, 0 collisions | `experiments/e16_lastwish/laneFPOINT/RESULT.md` |
| C14 | remove-1-add-1 components (mask sets) | 729 / 2,187 / 10,935 / 112,833 / 59,697 = **186,381** | closed | `beat88/methods/shared/gauge.py`; `wrapup/CONFLICTS_RESOLVED.md` B4 |
| C15 | site rebuild `G ≤ 3` | **55,970 sites over 18,355 circuits** | **0 sites**; controls 8,000/8,000 | `experiments/e16_lastwish/lane536/RESULT.md` D3 |
| C16 | site rebuild `G ≤ 4` (2-mint/3-orphan) | **1,409 sites** | **1,409/1,409 `G > 4`**; control 400/400 | same, D4 |
| C17 | remove-2-add-1 wall | **33,010** known 88 gauge orbits | no 87 | `beat88/methods/m2_oracle/LEDGER.md` |
| C18 | remove-3-add-1 wall | 64 known 89s | no 87 | same |
| C19 | genome sweep | **6,832,408** genomes | no 87 within one operand edit of any one-gate truncation | `beat88/methods/m4_inverse/analysis/landscape.md` |
| C20 | `FOUND_*` alarms | **44,249** files | **none below 89 gates** | `beat88/` |
| C21 | joint-level ladder | merged `W3 ∪ U4`, `k = 9..14` | **complete, all UNSAT** ⇒ **merged = 15 exactly** (the split total; merging buys nothing); `k=9/10/11` re-proved 528/528 on a second encoding, positive control fired | `fleet8/unified/results/joint_levels.jsonl`; `fleet11/laneCUBE/RESULT.md` §7.1 |
| C22 | **`k = 14` — DECIDED UNSAT 2026-09-01** | the whole level, one monolithic solve (kissat-4.0.4, 356,321.63 core-s ≈ 99 core-h) | **UNSAT.** No 87 shares the block structure of every known 88. The unfinished 528-cube sweep stood at **90/528 decided, all UNSAT, 0 SAT** — consistent, not the basis of the verdict. ⚠ **Not** a proof that no 87 exists: an 87 outside this decomposition is untouched | `fleet11/laneCUBE/RESULT.md` §7.1; `fleet11/laneCUBE/logs/mono_14_kissat404.log` |
| C23 | all-menu bound | **1.41 × 10²⁶** menu configurations | `price ≥ 87`; 9 of 10 block bounds tight | `fleet5/laneMENU/results/bound.json` |
| C24 | cell sweep | 20 distinct cells | every one prices **≥ 88** | `fleet5/laneMENU/results/cellprice.json` |
| C25 | merge lattice | 21 boundaries | 19 FREE, each pricing **exactly the split total**; 7 dissolved simultaneously still land at 88 | `fleet5/laneMERGE/results/FINAL_TALLY.txt` |
| C26 | **`MB27B373 = 13` exactly** | one block | `k = 12` UNSAT in 19,458 s + replay 13; **laneMERGE closes 20-for-20; the 12 ⇒ 87 branch is foreclosed** | `fleet6/door/ADDENDUM_20260829.md` |
| C27 | RC2 exact union floors | **749,150 OPTIMAL** (125 timeouts) | best floor anywhere = **88** | `campaign_87/wave5/burn/union_sat/` |
| C28 | dim-12 tap-region optimality | **4** regions incl. one on **Jean's 88** | `min_gates = \|B\| = 11`, each with a positive control | `experiments/e7_push/ledger.jsonl` |
| C29 | buy-one-save-two | **4,926** blocks over 14 known 88s | none rebuildable in `\|B\|−2` even with a free extra mask | `experiments/e3a_exploit/ledger.jsonl` |
| C30 | dim-8 block optimality | **82/82** cells | `optimum_proved = True` | `fleet9/laneENUM/results/v2_counts.jsonl` |
| C31 | DOOR-SHUT sweep | 740 decided, 0 timeouts | `U07 ≥ 11` for every minimal committed set with `U1 ≤ 7` | `fleet3/laneCB_completeness/` |
| C32 | `W3_noshare = 11` exact | one cell, 33,876.6 s | **the rank cut buys ZERO** | `fleet3/laneF4_rule/ADDENDUM_20260829.md` |
| C33 | `U3(tier1) = 10` exact | one cell, `k=9` UNSAT | `2 + 10 = 12` — **identical** to `4 + 8` | `fleet2/laneG_generator/ADDENDUM_20260829.md` |
| C34 | e_upstream vocabulary re-census | **1,925,065** target-checked 88s, **107,803,640** slots | **1,778-word vocabulary; 0 circuits with `\|odd\| ≥ 3`** | `wrapup/day2/e_upstream/recensus.json` |
| C35 | the 89's irreducibility | 57 single deletions + 1,596 pairs on `S89_41_00000098` | **0 and 0** — not a mislabelled 88 or 87 | `experiments/e_upstream/RESULT.md` §6 |
| C36 | 33 e_upstream floors through the oracle | 33 | **33/33 VALID**, depths exact-minimum | `experiments/e_upstream/RESULT.md` §5 |
| C36b | **Exact max fan-out over ALL valid build orders** | **39 mask sets** — the six record 88s + the 33 e_upstream floors | records **3–5** (potential 8); **6 anywhere**, at 92 gates. **Fan-out ≥ 8 unreachable at 88.** 39/39 exhaustive, 0 timeouts, all OPTIMAL. A 150-circuit corpus widening is **running** | `experiments/e_upstream/RESULT.md` §7 C4; `wrapup/day2/e_upstream/c4_fanout_cpsat.json` |
| C37 | 498-circuit structural battery | 498 corner 88s | 0 dup masks, 0 dead gates, `B = 56` 498/498, `n = κ+\|counted\|+Y` 498/498, `ρ`-equivariance **0/498** | `atlas/corner/ANALYSIS_20260829.md` §3.1 |
| C38 | forcedness at certified optima | **99** miniature instances, `L* = 3..11` | median **10** families at the true optimum; only 22 % unique | `experiments/e16_lastwish/laneFORCED/RESULT.md` |
| C39 | exact-window decider validation | 4,200 planted YES + 462 branch-deleted | 4,200/4,200 and 462/462 correct | `wrapup/CONFLICTS_RESOLVED.md` B6 |
| C40 | corpus `l3` sweep, first ever | **17,283** e15 census 88s | `l3` min **57**; 570 at `l3 ≤ 66`; **no floor at 67, no empty band, no ridge** | `atlas/corner/ANALYSIS_20260829.md` §4.4, §6 |

### 6.3 Measurements and observations

| # | statement | population | citation |
|---|---|---|---|
| M1 | **Clean-room from scratch reaches 93 @ 7 in ~7.5 h**; unaided worker 95–101 in ~2 min; BP alone 94; five distinct 93s; never 92 | one clean-room lane, 151 files, machine-checked self-containment | `fleet10/RESULT.md` |
| M2 | **The wiring of an 88 is forced by its mask set** — 2,197/2,200 masks have exactly one legal acyclic parent pair; **forced fraction 0.9986**; 1,320/1,320 sampled observations forced | 25 circuits census + 3 × 30 wirings | `wrapup/day2/STEWARD.md` §S3 |
| M3 | **`\|A*\| ≥ 18`, `κ ≥ 20`, glue `≥ 2`** with no tail | **1,303** 88s from three populations | `atlas/corner/ANALYSIS_20260829.md` §3.2, LEAD-3, LEAD-4 |
| M4 | **13 of 17 blocks have a unique optimum at all 70 cells**; 28 of 88 gates forced; all 75 legal orders emit the byte-identical circuit | 70 cells; 54,889 wild circuits | `fleet9/laneENUM/RESULT.md` |
| M5 | **The currency plateau is `\|M\| = 19..23`, exchange rate −1.00, upper cliff measured at 23 → 24** | 64 rows | `fleet12/laneF1/ADDENDUM_20260829.md` |
| M6 | **~200 mutations across six lanes all return exactly 88** | ~200 | `fleet12/lane*/results.jsonl` |
| M7 | **Efficiency inverts six ways** — the best circuits carry the most waste; service correlates with gate count at **+0.26**, the wrong sign | multiple | `wrapup/LEADS.md` §B item 1 |
| M8 | **Three independent plateau harvests are mutually disjoint** — 1,540,221 distinct 88s, zero collisions | 3 harvests | `wrapup/CORPUS88.md` §2.2 |
| M9 | ⚠ **LR ≈ 1.00**: `options_per_gate_mean` identical to 4 s.f. at 88/89/90/91/92; median distance to a better circuit **42 masks**, 44 of 45 need `k ≥ 8`, against radius 3 | 1,200 states/length; 45 circuits | `wrapup/CORRECTIONS.md` C-42; `wrapup/CONFLICTS_RESOLVED.md` §C10 |
| M10 | ⚠ **90.1 % of on-disk 88s are far from all studied frames** | on-disk 88s | `experiments/e14_plateau87/`; `experiments/e17_pure/DOSSIER.md` §8.1 |
| M11 | ⚠ **99 lateral escapes, not 1** — `88@5fs` is not rigid; 94 of the 99 exist nowhere else in the 1.58 M corpus | 2 × 27,720 triples | `fleet1/laneD_completions/ADDENDUM_20260829.md` |
| M12 | ⚠ **`l3` and `\|A*\|` are strongly anti-correlated** (`r = −0.854` / `−0.553`) — the two cheap 87 routes pull in opposite directions | 498 + 800 | `atlas/corner/ANALYSIS_20260829.md` LEAD-2 |
| M13 | ⚠ **The branch-3 region is unsearched AND unpopulated** — `\|A*\|` minimum 18 against a required 2 | 498 | `atlas/corner/ANALYSIS_20260829.md` §3.4 |
| M14 | 88 is a strong non-monotone attractor: `{88: 15537, 89: 2270, 90: 2529, 91: 3907, 92: 2548, 93: 1578}` — **6.8× more often than 89. Unexplained; no document addresses it** | cone-ILS restarts | `wrapup/LEADS.md` §B counterweights |
| M15 | Elite basin **79–81 % `ρ²`-symmetric**, the sharing trick rediscovered by search; Jean's 88 is a second, distinct symmetric basin at 75 % | 5 records + basin | `wrapup/LEADS.md` §B item 8 |
| M16 | ρ-symmetry costs **12–13 gates** in a greedy search; SAT window repair near an optimum succeeds **1 in 1,924** | clean-room lane | `fleet10/RESULT.md` §2.2, §3.1 |
| M17 | ⚠ **The vocabulary price is ≤ 1 gate** and the out-of-vocabulary word is load-bearing in the 89 | 225 jobs, 97.0 core-h | `experiments/e_upstream/RESULT.md` |
| M18 | ⚠ Feature classes C3 (weight ≥ 12) and C5 (the eight hubs `T_j`) price at **0 gates** — they were never out of vocabulary. **C4 (fan-out ≥ 8) is CLOSED the other way: unreachable at 88** (see C36b). Only **C1** (`\|odd\| ≥ 4`) is still a genuine unpriced class | 1.93 M circuits; 39 mask sets | `experiments/e_upstream/RESULT.md` §7 |
| M21 | **IN FLIGHT** — pinned descent seeded at the out-of-vocabulary 89, target 88: *does an 88 exist outside the 1,778-word vocabulary?* Launched 11:36, 10,000 s budget. **No `done` row at time of writing**; a 45 s pilot returned floor **89**, no 88 | one seed circuit | `wrapup/day2/runs/RUNS.md` R1; `wrapup/day2/e_upstream/seed89_ledger.jsonl` |
| M19 | ⚠ **The block partition was never measured on any circuit** (defect D22, LIVE); `91@6` gate 70 is representable by **no** fleet8 block | — | `wrapup/LEADS.md` §B counterweights |
| M20 | ⚠ **Class-conditionality**: lane A's wiring condition (flag F3) is measured on 22 circuits with one exception and **never proved** | 22 circuits | `wrapup/LEADS.md` §B counterweights |

### 6.4 The proved ceilings (§3.6.1), for reference

| route | ceiling | citation |
|---|---:|---|
| Linear counting / LP over the measured basis | 46.2 | `fleet7/laneCONSOLIDATE/STATE_OF_THE_PROBLEM.md` §6.2 |
| Tower rungs (level 3 / level 2) | 51 / 26 | same |
| Lemma P (projection / visibility) | 36–40 | same |
| Generalised heavy-corner rank ledger | 52 | same |
| Edge counting | 33 | same |
| `C_c` family (`c = 0` / `M`'s own rung / coarse hypothesis) | 73 / 71 / 67 | `experiments/e17_pure/DOSSIER.md` §5.3 |
| **The residual (P1/P2) family, on a verified 88** | **83.000** | `fleet2/laneP_proof/RESULT.md` |
| **The certificate LP** | **91.4098776** (`B* = 91.409884`) | `experiments/e17_pure/DOSSIER.md` §3.11, §5.5 |
| The `G_int` / exchange-rate family | dies at `κ ≥ 22`, below the records' own `κ = 18..28` | `fleet7/laneUNCOND` §7.4 |
| Reductions / charges / quotient composition / sector localization | proved incapable in kind | `experiments/e17_pure/DOSSIER.md` §5.8 |

---

## 7. The bottom line

**For 88.** Two independent parties and a seven-year published literature stop at
88; a knowledge-free clean-room run stops at 93. Across 1,575,516 distinct
verified 88-gate mask sets there is not one duplicated mask and not one
consumer-less middle gate — **zero alarms on a fail-able detector whose
contrapositive would hand over an 87 on the spot** — and over 27,888 exhaustive
single-mask deletions with unrestricted rewiring, **not one 87-mask set is even
realisable**. Every exact relaxation of the synthesis problem this project has
built — 1.41 × 10²⁶ menus, 20 cells, 21 merge boundaries, 749,150 union floors,
4,926 block rebuilds, ~200 mutations — returns 88 or worse, and the one ladder
that could have returned 87 needed `SAT at k = 14`, which was **decided UNSAT on
2026-09-01** (99 core-hours, kissat-4.0.4): the merged block costs exactly 15,
merging buys nothing, and **no 87 exists that shares the block structure of every
known 88**. At 88 gates the wiring is **not a free parameter**:
the mask set forces it (0.9986 of gate masks have exactly one legal acyclic
parent pair), and the one wiring slack anyone nominated — fan-out — is
**provably unavailable**, exact over every valid build order of 39 mask sets.
**And 87 has never been found by anything, anywhere.**

**Against 88.** Not one of those negatives is a bound. The project's own control
prices its neighbourhood certificates at **likelihood ratio ≈ 1.00**: the exact
decider calls a 97-gate circuit irreducible in exactly the tone it calls Jean's
88 irreducible, and the real distance between a circuit and a better circuit is a
**median 42 masks** against a certified radius of 3. The most-replicated
structural regularity in the corpus — that 1.9 million 88s all draw on one
1,778-word dictionary — **is not forced**: an oracle-verified 89 sits one gate
outside it, irreducible by 1- and 2-deletion, built *around* the novel word. The
census behind much of the structural evidence is **1.1 % of the corpus and 92 %
one engine**. And the arithmetic still permits an 87 shaped unlike anything ever
built — **branch 3: `|A*| = 2`, `κ = 2`, `Y = 0`, a weight-7 MixColumns row
produced by a cancelling gate** — in a region that is unpopulated **and
unsearched**, which is exactly the pair of facts that cannot be told apart.

**The honest statement remains `56 ≤ L(M) ≤ 88`.** The gap is 32 gates. Every
unconditional proof family in this repository has a ceiling below 88 except one,
and that one has a ceiling of 83 on a circuit that exists. The one relaxation
exact on the records is not finitely posed, and nobody has a candidate for the
finite universe that would pose it.

---

*Compiled 2026-08-29 by the CASE-FOR-88 synthesis agent, wrap-up day 2. Every
number is traceable to a named file. Where a source and its referee disagreed on
a numeral, the referee's numeral appears. Where a source's own status word was
weaker than the claim it supported, the weaker word appears. Where a figure was
resolved in `wrapup/CONFLICTS_RESOLVED.md`, that verdict governs; figures listed
in `wrapup/CORRECTIONS.md` as stale do not appear.*
