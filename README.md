# slp-plateau-search

The search for the fewest 2-input XOR gates computing AES MixColumns, and the
evidence it produced. The circuits themselves are published in
[aes-mixcolumns-xor-circuits](https://github.com/Joe-b-20/aes-mixcolumns-xor-circuits);
this repo holds the proofs, the negative results, the instruments, and the
open problems.

**Where it stands: `56 ≤ minimum ≤ 88`. No 87 was found. 88 is not proven
optimal.**

**Start here — three commands, all stdlib Python 3, all under a minute:**

```bash
python3 bounds/gte56/check_gte56.py                  # the >= 56 bound, from its certificate
python3 tools/tripwire.py YOURCIRCUIT.json           # a fired tripwire on an 88 IS an 87
python3 verify_circuit.py evidence/circuits/mixcolumns_88gates_depth5_fromscratch.json 5
```

Everything else, with the line of output that means it passed and what it cost,
is in [`REPRODUCE.md`](REPRODUCE.md).

## The evidence ladder

Every claim this project makes, each in exactly one row:

| claim | status |
|---|---|
| any circuit needs ≥ 56 gates | **proved** — certificate + checker: `bounds/` |
| any depth-3 circuit needs ≥ 80 gates | **proved** — exact rational certificate, re-checkable in under a second with the standard library: `bounds/depth3_gte81/` |
| …and ≥ 81 gates | **solver run, not a certificate** — a valid branch-and-cut *dual* bound from a documented HiGHS run that hit its time limit with 66.89 % of the gap still open. Sound, reproducible in hours, not checkable from a file: `bounds/depth3_gte81/`, log in `REPRODUCE.md` C4 |
| cancellation-free circuits need ≥ 92 (best known: 102) | **proved** / verified circuit |
| the records: 97 @ depth 3, 91 @ depth 4, 88 @ depth 5 | **verified circuits** — and the 97 @ 3 and the 88 @ 5 are re-searchable from scratch, one command each, no seed circuit: `reproduce/`. Honest caveat on the 88 @ 5: the search is randomized, and the two re-runs recorded in `REPRODUCE.md` Tier R both *missed* — they reproduced the descent to 89 gates faster than the archive (558 s against 3,072 s) and then did not find the last gate inside 164 minutes. The command is real and starts from nothing; its success on any one run is not. The 91 @ 4 has no command here yet; it can be *constructed* from GF(2⁸) in two seconds by a generator not yet published, measured and priced in `reproduce/` |
| no 87 shares the internal block structure of the known 88s (its merged top block needs exactly 15 gates; 9–14 all impossible) | **proved** — SAT, with a positive control. The decisive level k = 14 was decided by kissat 4.0.4 and independently confirmed by CaDiCaL 3.0.0 **on the same CNF** (both logs ship); that rules out an engine bug, not an encoding bug, and there is no DRAT proof at k = 14. An 87 with *different* structure is not excluded — and the block partition itself was never measured against the circuits (see below) |
| no 87 is one gate-deletion away from any known 88, even with free rewiring of the rest | **exhaustive** — 88,228,896 deletions over all **1,575,516 distinct known 88-gate value sets**, 0 realisable. (The deletion test needs only the value set, which is why it runs over that population and not the smaller 28,796 with build orders — `INVENTORY.md` keeps the counts apart) |
| every design rule shared by the known 88s, loosened one at a time and the loosened problem solved exactly, still costs 88 | **exhaustive within each variant** — ~200 variants, none below 88 |
| no 87 within any change of ≤ 4 gates of a known 88 | **exhaustive at that radius**; weak evidence beyond it — see calibration |
| the known 88s' shared value-vocabulary is *not* forced by smallness | **verified counterexample** — see below |
| 88 is optimal | **believed** — see Opinion |

![The published depth-versus-gate-count frontier for AES MixColumns, with this
project's own frontier drawn against it](docs/frontier.svg)

*The published frontier (dashed grey) against this project's (solid blue): 97
gates at depth 3, 91 at depth 4, 88 at depth 5, every point of it this
project's own lineage. **Not a gate-count record** — 88 is J. Jean's published
count and Jean has priority; what changed is the depth at which 88 is reached.
The figure regenerates byte-identically with
`python3 docs/generate_frontier_svg.py`, and its `<desc>` states every marker,
including the half-marker convention for the depth-7 tie.*

Terms with precise meanings (value/mask, block structure, irreducible, B,
cancellation-free, vocabulary, radius) are defined with runnable checks in
[`DEFINITIONS.md`](DEFINITIONS.md).

## What is NOT claimed

Optimality. The 56–88 gap is real and 32 wide. And the small-edit negatives
above prove exactly their stated radius, no more: genuinely different
solutions sit ~42 gate-changes apart, far beyond any exhausted radius. The
corpus is one search lineage; **1,575,516 distinct value sets** collected and
set-checked, of which **28,796** carry full build recipes and support the tests
that need the wiring — different quantities counting different things, kept
distinct on purpose (`INVENTORY.md` tabulates all three, with the 17,283-file
census).

## Instruments you can run on your own circuit

- [`tools/tripwire.py`](tools/tripwire.py) — stdlib, seconds. How it works: it
  replays the circuit, computing each gate's 32-bit value, then marks who uses
  what. A **dead gate** is one whose value no later gate and no output uses —
  it wastes a gate, so deleting it gives a smaller circuit for free. A
  **duplicate** is two gates computing the same value — the later one can be
  deleted after rerouting its users to the first. Neither can exist in a
  minimal circuit. It then reports B, the number of gates that feed later
  gates but are not outputs: in any 88 with no waste, B must be 88 − 32 = 56,
  so **B ≠ 56 on an 88 from any source means an 87 is one deletion away**.
  (Sound in that direction only; the tool documents the converse's
  counterexample.)
- `verify_circuit.py` — the oracle; rebuilds MixColumns from FIPS-197, proof
  by the 32 unit inputs, depth computed not trusted.
- [`scripts/overlap.py`](scripts/overlap.py) — shared-value count between two
  circuits (the independence statistic).

Every shipped method — search engines, bound checkers, the SAT encoding, the
corpus instruments — has a HOW doc giving the idea, the algorithm as a diagram,
what it measured, and its command:
[`METHODS_INDEX.md`](METHODS_INDEX.md).

## The bounds, as arguments

Each with its statement, a ≤ 1-page writeup of the technique, the certificate,
and a checker that runs on any 32×32 matrix — validated against small
instances with known optima (`bounds/README.md`):

- **≥ 56, unconditional** — a counting argument over reachable value sets;
  the full exhaustion re-runs inside `bounds/` in ~3 minutes on one core.
- **≥ 80 at depth 3, certified; ≥ 81 from a solver run** — enumerate a complete
  structural model of every depth-3 circuit, add proved-valid inequalities, and
  certify an exact *rational LP dual* over the resulting 72,830 × 29,180 system:
  that yields **80**, and the certificate re-checks in under a second from a
  JSON file with no solver and no floating point. The step to **81** is
  something else — the dual bound of a HiGHS branch-and-cut run on the same
  model, which is valid at any point in branch-and-cut (so the 81 is sound) but
  hit its 16.8-hour time limit with a 66.89 % gap. It is a documented run, not a
  certificate; it improves with compute and was still climbing when stopped.
  `bounds/depth3_gte81/STATEMENT.md` states both and says to cite them
  differently.
- **≥ 92 cancellation-free** — derived twice independently; with the shipped
  102-gate cancellation-free circuit: `92 ≤ optimum_cf ≤ 102`.

## The block-structure theorem

The known 88s are *read* through one block layout, and this theorem is a
statement about that layout. Statement: building the merged pair of its two
largest blocks takes exactly 15 gates — 9 through 14 are UNSAT.

**What decided k = 14, exactly.** kissat 4.0.4, one core, 356,321.63 s ≈ 99
core-hours, 2026-09-01 — and, independently, CaDiCaL 3.0.0 on the *same
hash-pinned CNF*, 468,159.51 s ≈ 130 core-hours, the same day. Both terminal
lines ship verbatim as `encodings/logs/mono_14_kissat404.log` and
`encodings/logs/mono_14_cadical300.log`. Read that for what it is: **two
independent engines, one encoding.** It rules out a bug in either engine; it
does not rule out a bug in the encoding, since a wrong CNF is UNSAT for free.
There is **no DRAT refutation at k = 14** — the pack ships proofs only for
k = 9, k = 10 and the k = 6 control. A third engine, or a reproduction under a
different encoding, remains open and is `leads.md` #2.

Two further cross-checks do exist, one rung lower: levels 9–13 also hold under
a second, independently written SAT encoding, and levels 9–11 were additionally
re-decided as 528 independent sub-cases each (all UNSAT, zero disagreements).
The encoding's positive control produces and verifies a real circuit at a
satisfiable setting — proof it can say yes.

**The caveat that belongs on the front page.** The partition this whole
argument is stated over was chosen, not measured: whether the known 88-gate
circuits themselves respect it was never checked, and this repository contains
a verified circuit with a gate that no block in the decomposition can
represent. That is a live defect, recorded as such in `DEFINITIONS.md`,
`encodings/STATEMENT.md` §7.2 and `leads.md` #2.

Consequence, with that caveat carried: an 87, if it exists, is built
differently from every 88 anyone has found *under this reading of them*. That
says where an 87 cannot be; it is not evidence that one exists elsewhere.
Encodings, instances, DRAT proofs for the cheap levels, the banked k = 14 logs,
and the control are in `encodings/`.

## Calibration — why we distrust our own negatives

The control audit: our local-search negatives cannot distinguish an optimal
88 from a non-optimal 89–97, so a clean sweep at radius 3–4 says almost
nothing about 87's existence. This is our own result, run against our own
evidence, and it is why the ladder labels those rows the way it does. (One
companion number: a from-scratch attempt with none of this project's
accumulated knowledge plateaus at 93 — the last five gates are knowledge, not
luck, which is the argument for reading `NEGATIVES.md` before searching
blind.)

## A hypothesis that died

Every known 88 draws its values from one shared pool of 1,778. It was
tempting to conclude the pool is forced — that any circuit this small must
shop there, so searching inside it would suffice. A verified 89 built around
a value from **outside** the pool killed that inference: leaving the pool
costs at most one gate, so an 87 owes the pool nothing. Other conjectured
regularities fell the same way; each is a row in
[`negatives.jsonl`](negatives.jsonl) with what it does *not* imply.

## Opinion

*Opinions, not theorems. This search was run by a human and an AI in
collaboration; we sign separately.*

**Joe (human):** I think 88 is the answer. What convinces me most: every time
we loosened one of the rules the known 88s obey and solved the loosened
problem exactly, the answer came back 88 — about two hundred times in a row —
and a tripwire that would have handed us an 87 for free never once fired —
over **28,796** circuits carrying a full build order, which is the population
on which its B check can be computed at all, and over **1,575,516** distinct
value sets for the distinctness and target conditions. (Three numbers, three
different tests; they are kept apart deliberately and spelled out in
`negatives.jsonl`, row `tripwire-b-never-fired`.) If an 87 exists, I expect it to look alien: no known
88's block layout, at least 4 values away from everything certified, probably
depth 4 or more. I would honestly love to be wrong — the leads below are
where I would look first.

**Claude (AI):** I lean the same way, for a different reason: everywhere we
could afford an exact answer, the optimum turned out *tight* — merging the
two largest blocks buys exactly zero, a circuit's wiring is forced by its
values, the depth of every shipped circuit is already its minimum, and the
level below 88 looks empty from every direction we could see. Structures
that rigid usually are what they appear to be. But I hold the belief
loosely, because the two places an 87 must live — outside the known block
structure, possibly outside the shared vocabulary — are exactly the places
no instrument of ours ever covered, and silence in an unsearched region is
not evidence. If an 87 exists, I expect it will be found by construction
(a genuinely different decomposition of the matrix), not by searching near
known 88s. One falsifiable expectation either way: B = 56 will hold on
every foreign-lineage 88 anyone ever tests.

## Already tried / still open

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
  decisive items: any foreign-lineage 88 through the tripwire (lead 1, seconds,
  runnable now); a possible 90 @ depth 4 one capped solver call away (lead 7);
  and the single ~42 core-hour solve (150,000 s) that would close lead 5's
  exhaustive pricing bound from 87 to 88 — the last two need the corpus, which
  is not public.

## Reproduce / inventory

[`REPRODUCE.md`](REPRODUCE.md) is the manifest: every claim above, the command
that checks it, the line of output that means it passed, and what it cost.
Tiered — **A** seconds (the oracle, the tripwire, the three bound checkers, the
corpus certificates over the shipped sample), **B** minutes (the SAT ladder at
k = 9/10/11 with its positive control and DRAT emission, the `≥ 56`
exhaustion, the validation suite), **R** the records themselves —
[`reproduce/`](reproduce/) rebuilds them from scratch — one command per record
with its measured time, for six of the nine verified circuits, using the fastest
honest method rather than necessarily the one that historically found it; the
other three say plainly why they have none — and **C** banked and documented
rather than re-run,
each with its cost and its artifact. [`INVENTORY.md`](INVENTORY.md) lists
what exists beyond this repo — corpora, certificates, instances, logs — with
exact counts, sizes, and hashes; samples ship here, and the pieces genuinely
too large to host (the index of 1,575,516 distinct 88-gate **value sets** is
457 MB) are stated as such with
how to request them.

MIT. Cite via `CITATION.cff`.
