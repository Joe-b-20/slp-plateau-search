# slp-plateau-search

The search for the fewest 2-input XOR gates computing AES MixColumns, and the
evidence it produced. The circuits themselves are published in
[aes-mixcolumns-xor-circuits](https://github.com/Joe-b-20/aes-mixcolumns-xor-circuits);
this repository holds the proofs, the negative results, the instruments, and the
open problems.

**Where it stands: `56 ≤ minimum ≤ 88`. No 87 was found. 88 is not proven
optimal.**

One author, Joe, working with AI agents he directed; "we" on these pages means
that collaboration. The choices behind the work, in his words:
[`DECISIONS.md`](DECISIONS.md).

**Start here — three commands, all stdlib Python 3, all under a minute:**

```bash
sh bounds/gte75/checks/run_all.sh                    # the >= 75 bound: finite facts + exact certificates (about 2 min)
python3 tools/tripwire.py YOURCIRCUIT.json           # a fired tripwire on an 88 IS an 87
python3 verify_circuit.py evidence/circuits/mixcolumns_88gates_depth5_fromscratch.json 5
```

Everything else, with the line of output that means it passed and what it cost,
is in [`REPRODUCE.md`](REPRODUCE.md).

## The evidence ladder

Every claim this project makes, each in exactly one row:

| claim | status |
|---|---|
| any circuit needs ≥ 75 gates | **computer-assisted proof, review draft** — a standalone proof note, fourteen finite facts recomputed by script, exact Farkas certificates with two independent checkers; reviewed only by machine so far: `bounds/gte75/` (supersedes the ≥ 56 pack, which stays checkable). A certified but less reviewed extension to ≥ 76 is described in the same pack |
| any depth-3 circuit needs ≥ 80 gates | **proved** — rational certificate, re-checks in under a second: `bounds/depth3_gte81/` |
| …and ≥ 81 gates | **solver run, not a certificate** — a sound dual bound from a time-limited run; see [The lower bounds](#the-lower-bounds) |
| cancellation-free circuits need ≥ 96 (best known: 102) | **proved** — split-price certificate + two checkers, refereed; supersedes the earlier 92: `bounds/cf_gte96/` / verified circuit |
| the records: 97 @ depth 3, 91 @ depth 4, 88 @ depth 5 | **verified circuits** — each rebuilds from scratch with one command (`reproduce/`); the 88 @ 5 search is randomized and its recorded re-runs missed, see `REPRODUCE.md` Tier R |
| **under our block decomposition**, no 87 shares the internal block structure of the known 88s (its merged top block needs exactly 15 gates; 9–14 all impossible) | **proved** — SAT with a positive control; k = 14 decided by two independent solver engines on one encoding, no DRAT proof at that level; the decomposition is our choice, measured as respected by 5/5 published 88s and 81.5 % of the corpus, and an 87 outside that class is not excluded; a decomposition found by search reaches 90.75 % at the same price — see [The block-structure theorem](#the-block-structure-theorem) |
| no 87 is one gate-deletion away from any known 88, even with free rewiring of the rest | **exhaustive** — 88,228,896 deletions over all 1,575,516 distinct verified 88-gate value sets (28,796 of them also carry a full build order), 0 realisable |
| every design rule shared by the known 88s, loosened one at a time and the loosened problem solved exactly, still costs 88 | **exhaustive within each variant** — ~200 variants, none below 88 |
| no 87 within any change of ≤ 4 gates of a known 88 | **exhaustive at that radius**; weak evidence beyond it — see calibration |
| the known 88s' shared value-vocabulary is *not* forced by smallness | **verified counterexample** — see below |
| 88 is optimal | **believed** — see Opinion |

![The published depth-versus-gate-count frontier for AES MixColumns, with this
project's own frontier drawn against it](docs/frontier.svg)

*The published frontier (dashed grey) against this project's (solid blue): 97
gates at depth 3, 91 at depth 4, 88 at depth 5, every point of it this
project's own lineage. **No gate-count record is claimed here**: 88 is
J. Jean's published count and Jean has priority; what changed is the depth at
which 88 is reached. The figure regenerates byte-identically with
`python3 docs/generate_frontier_svg.py`.*

Terms with precise meanings (value, block structure, irreducible, B,
cancellation-free, vocabulary, radius) are defined with runnable checks in
[`DEFINITIONS.md`](DEFINITIONS.md).

## What is NOT claimed

Optimality. The 56–88 gap is real and 32 wide. The small-edit negatives above
prove exactly their stated radius and no more: genuinely different solutions
are about 42 gate-changes apart, far beyond any radius exhausted here. The
corpus is one search lineage: **1,575,516 distinct verified 88-gate value
sets** — each a set of 88 intermediate values known to be realisable —
collected and set-checked, of which **28,796** carry full build orders and
support the tests that need the wiring. These are different quantities
counting different things, kept distinct on purpose:
[`INVENTORY.md`](INVENTORY.md) tabulates both of them and the 17,283-file
census beside them.

## The lower bounds

Each with its statement, a ≤ 1-page writeup of the technique, the certificate,
and a checker that runs on any 32×32 matrix — validated against small
instances with known optima (`bounds/README.md`):

- **≥ 75, unconditional (computer-assisted, review draft)** — parity classes of
  the signals, an odd-signal graph, exact transposition and a bounded potential
  over repeated transposition, then a linear system on helper types whose
  infeasibility at 73 and 74 gates is certified by integer multipliers; every
  finite fact about the matrix re-computes in 35 s and every certificate
  re-checks in 30 s (`bounds/gte75/`). Reviewed by programs and by independent
  machine reviews, by no human yet. A certified extension to **≥ 76** exists
  but is not yet in citable form (`bounds/gte75/bound_76/README.md`).
- **≥ 56, unconditional** — the earlier counting argument over reachable value
  sets, superseded by the 75 but kept checkable; the full exhaustion re-runs
  inside `bounds/` in ~3 minutes on one core.
- **≥ 80 at depth 3, certified; ≥ 81 from a solver run** — enumerate a complete
  structural model of every depth-3 circuit, add proved-valid inequalities, and
  certify an exact *rational LP dual* over the resulting 72,830 × 29,180 system.
  That yields **80**, and the certificate re-checks in under a second from a
  JSON file with no solver and no floating point. The step to **81** is
  something else: the dual bound of a HiGHS branch-and-cut run on the same
  model, valid at any point in branch-and-cut (so the 81 is sound) but reached
  when the run hit its 16.8-hour time limit with a 66.89 % gap. It is a
  documented run rather than a certificate; it improves with compute and was
  still rising when stopped. `bounds/depth3_gte81/STATEMENT.md` states both and
  says to cite them differently.
- **≥ 96 cancellation-free** — a split-price certificate (prices keyed by target,
  mask *and* split), derived twice independently and refereed shared-nothing; with
  the shipped 102-gate cancellation-free circuit: `96 ≤ optimum_cf ≤ 102`. It
  supersedes the mask-only 92 (`bounds/cf_gte92/`, kept as the published value).
  The split family's own optimum is 95.85, so it cannot reach 97; an exact solver
  run reached a dual bound of 99 (a run, not a certificate).

## The block-structure theorem

The known 88s are *read* through one block layout, and this theorem is a
statement about that layout. Statement: building the merged pair of its two
largest blocks takes exactly 15 gates — 9 through 14 are UNSAT.

**What decided k = 14, exactly.** kissat 4.0.4, one core, 356,321.63 s ≈ 99
core-hours, 2026-09-01 — and, independently, CaDiCaL 3.0.0 on the *same
hash-pinned CNF*, 468,159.51 s ≈ 130 core-hours, the same day. Both terminal
lines ship verbatim as `encodings/logs/mono_14_kissat404.log` and
`encodings/logs/mono_14_cadical300.log`. That is **two independent engines on
one encoding.** It rules out a bug in either engine and leaves a bug in the
encoding open, because a wrong CNF comes back UNSAT for reasons that have
nothing to do with circuits. There is **no DRAT refutation at k = 14** — the
pack ships proofs only for k = 9, k = 10 and the k = 6 control. A third engine,
or a reproduction under a different encoding, remains open and is `leads.md` #2.

Two further cross-checks do exist, one rung lower: levels 9–13 also hold under
a second, independently written SAT encoding, and levels 9–11 were additionally
re-decided as 528 independent sub-cases each (all UNSAT, zero disagreements).
The encoding's positive control produces and verifies a real circuit at a
satisfiable setting — proof it can say yes.

**The scope, in full.** The block decomposition this argument is stated over
was chosen, not measured off the circuits. It has now been measured:

| known 88-gate circuits | respect the decomposition |
|---|---|
| the five published 88s | **5 / 5**, zero violating gates |
| the 28,796 corpus 88s with a build order on disk | **23,456 = 81.5 %** |

The test can fail, and does: it flags gate 70 of the companion records
repository's verified `mixcolumns_91gates_depth6`, line support `{2, 3, 4, 7}`
— inside the merged block, but inside neither W3 `{2, 3, 7}` nor U4
`{3, 4, 7}` on its own. The 18.5 % that do not respect it almost all carry one
value spanning lines 0 and 2, which no block of this decomposition holds
together. Ours is also not the best that can be priced exactly. A search over
decompositions found a better one automatically:

| decomposition | respected by | priced exactly |
|---|---|---|
| ours | **81.5 %** | yes, total 88 |
| the one the search found | **90.75 %** = 26,132 | yes, total 88 |
| one that holds lines 0 and 2 together | **99.2 %** | no — one block of dimension 16 |
| the ceiling over decompositions that can be priced exactly | **91.1 %** | — |

The one the search found holds 2,676 more circuits than ours, and every one of
its blocks pays for the values it holds — none of them absorbs circuits for
free. Measurement to be published
with the toolkit.

The consequence is unchanged in substance and now quantified: the theorem covers
the 81.5 % class and the five published 88s, and an 87 outside that class is not
excluded. The block prices still sum to an *upper* bound on the class rather
than a lower bound on circuits — reading them downwards would need each block
priced against every value whose support lies inside it at any level, because a
respecting circuit may build its operands in any order, and what is priced here
is the smaller supply that one build order realises. Turning the sum into a
lower bound is the open step. The same scope is recorded
in `DEFINITIONS.md`, `encodings/STATEMENT.md` §7.2 and `leads.md` #2, and it is
why the theorem is quoted with "under our block decomposition" everywhere it
appears. Encodings, instances, DRAT proofs for the cheap levels, the banked
k = 14 logs, and the control are in `encodings/`.

## A hypothesis that died

Every known 88 draws its values from one shared pool of 1,778. It was
tempting to conclude the pool is forced — that any circuit this small must use
it, so searching inside it would suffice. A verified 89 built around a value
from **outside** the pool killed that inference: leaving the pool costs at most
one gate, so an 87 owes the pool nothing. Other conjectured regularities fell
the same way; each is a row in [`negatives.jsonl`](negatives.jsonl) with what
it does *not* imply.

## Calibration — why we distrust our own negatives

The control audit: our local-search negatives cannot distinguish an optimal
88 from a non-optimal 89–97, so a clean sweep at radius 3–4 says almost
nothing about 87's existence. That is why the ladder labels those rows the way
it does. One companion number: a from-scratch attempt carrying none of this
project's accumulated knowledge stops at 93. The last five gates are the hard
part, and they are where the accumulated knowledge goes — which is the argument
for reading `NEGATIVES.md` before searching blind.

## Instruments you can run on your own circuit

- [`tools/tripwire.py`](tools/tripwire.py) — stdlib, seconds. It replays the
  circuit and reports dead gates, duplicate values, and B, the number of gates
  that feed later gates without being outputs. Neither a dead gate nor a
  duplicate can occur in a minimal circuit, and a short lemma forces
  B = 88 − 32 = 56 on any irreducible 88, so **B ≠ 56 on an 88 from any source
  means an 87 is one deletion away**. Sound in that direction only; the tool
  ships a counterexample to the converse, and `REPRODUCE.md` Tier A runs it.
- `verify_circuit.py` — the oracle; rebuilds MixColumns from FIPS-197, proves
  correctness on the 32 unit inputs, and measures depth rather than reading it.
- [`scripts/overlap.py`](scripts/overlap.py) — shared-value count between two
  circuits (the independence statistic).

Every shipped method — search engines, bound checkers, the SAT encoding, the
corpus instruments — has a HOW doc giving the idea, the algorithm as a diagram,
what it measured, and its command:
[`METHODS_INDEX.md`](METHODS_INDEX.md).

## How to reproduce, and what exists beyond this repository

[`REPRODUCE.md`](REPRODUCE.md) is the manifest: every claim above, the command
that checks it, the line of output that means it passed, and what it cost. It
has four tiers:

| tier | budget | contents |
|---|---|---|
| **A** | seconds | the oracle, the tripwire, the three bound checkers, the corpus certificates over the shipped sample |
| **B** | minutes | the SAT ladder at k = 9/10/11 with its positive control and DRAT emission, the `≥ 56` exhaustion, the validation suite |
| **R** | seconds to hours | the records themselves — [`reproduce/`](reproduce/) rebuilds them from scratch, one command per record with its measured time, for seven of the nine verified circuits, by the fastest route the project has rather than necessarily the one that historically found it; the other two say plainly why they have none |
| **C** | hours to core-weeks | banked and documented rather than re-run, each with its cost and its artifact |

[`INVENTORY.md`](INVENTORY.md) lists what exists beyond this repository —
corpora, certificates, instances, logs — with exact counts, sizes, and hashes.
Samples ship here. The pieces genuinely too large to host are stated as such,
with how to request them; the largest is the index of the 1,575,516 distinct
88-gate **value sets**, at 457 MB.

## Why the search stopped, what it cost, and where the instruments go next

**Why it stopped.** k = 14, the last decisive computation, returned UNSAT on
2026-09-01; every remaining lead was then priced rather than run, in
[`leads.md`](leads.md).

**What it cost.** The runs itemised in `REPRODUCE.md` and the STATEMENTs come
to **at least 610 core-hours** — 233 at k = 13, 229 at k = 14 across two
engines, 97 for the out-of-vocabulary 89's search, 20 for the clean-room
control, 17 for the depth-3 solver bound, 13 at k = 12. Three further lines
carry no core-hour figure, so 610 is a floor.

**Where the instruments go next.** Oracle, tripwire, bound checkers and the
exact-SLP encoding read a target list and nothing else, and are already pointed
at AES **InvMixColumns**: matrix derived from FIPS-197 and GF(2⁸) under four
passing controls, tripwire reading B = 56 on all five published forward 88s,
day-0 baselines of a naive XOR tree at 440 gates and a greedy at 164 @ depth 9.
The only printed count for that matrix is 92 (Xiang et al., ToSC 2020), and
91 follows directly from Yuan et al.'s in-place 91 for MixColumns (ToSC 2024),
since an in-place program inverts gate for gate; so the bar is 91. We have
found no published gate count at a stated depth and no non-trivial lower
bound for it.

## Opinion

*This section is opinion; nothing in it is proved.* We think 88 is the answer,
for two reasons that survive the calibration section. First, every time we
loosened one of the rules the known 88s obey and solved the loosened problem
exactly, the answer came back 88 — about two hundred times in a row — and a
tripwire that would have produced an 87 immediately stayed silent over 1.58
million circuits. Second, everywhere we could afford an exact answer, the
optimum turned out *tight*: merging the two largest blocks saves nothing, a
circuit's wiring is forced by its values, and the depth of every shipped
circuit is already its minimum. Structures that rigid are usually optimal.

We hold it loosely all the same. The two places an 87 must live — outside the
known block structure, possibly outside the shared vocabulary — are exactly
the places no instrument of ours ever covered, and silence in an unsearched
region is not evidence. If an 87 exists, we expect it to look unlike anything
here: no known 88's block layout, at least 4 values away from everything
certified, probably depth 4 or more — and found by construction, a genuinely
different decomposition of the matrix, rather than by searching near known 88s.
One falsifiable expectation either way: B = 56 will hold on every 88 from
another author's search that anyone ever tests. We would like to be wrong; the
leads below are where we would look first.

## Already refuted, and still open

- [`NEGATIVES.md`](NEGATIVES.md) + [`negatives.jsonl`](negatives.jsonl) —
  everything already refuted, machine-readable: scope, strength
  (theorem / exhaustive / searched), artifact, repro command where one
  exists, and what each result does NOT imply. Read before spending compute.
  Every row carries a boolean `shipped` field: `true` means its artifact is a
  path in this repository you can open right now, `false` means the artifact is
  held locally and the row says so in words — see `INVENTORY.md` for what is
  available on request.
- [`leads.md`](leads.md) — the open attacks, ranked by payoff/cost, priced in
  core-hours, with a startable command where the inputs are public. Cheapest
  decisive items: any 88 from another author's search through the tripwire
  (lead 1, seconds, runnable now); a possible 90 @ depth 4 one capped solver
  call away (lead 7); and the single ~42 core-hour solve (150,000 s) that would
  raise lead 5's exhaustive pricing bound from 87 to 88 — the last two need the
  corpus, which is not public.

MIT. Cite via `CITATION.cff`.
