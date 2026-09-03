# slp-plateau-search

The search for the fewest 2-input XOR gates computing AES MixColumns, and the
evidence it produced. The circuits themselves are published in
[aes-mixcolumns-xor-circuits](https://github.com/Joe-b-20/aes-mixcolumns-xor-circuits);
this repo holds the proofs, the negative results, the instruments, and the
open problems.

**Where it stands: `56 ≤ minimum ≤ 88`. No 87 was found. 88 is not proven
optimal.**

## The evidence ladder

Every claim this project makes, each in exactly one row:

| claim | status |
|---|---|
| any circuit needs ≥ 56 gates | **proved** — certificate + checker: `bounds/` |
| any depth-3 circuit needs ≥ 81 gates | **proved** — `bounds/` |
| cancellation-free circuits need ≥ 92 (best known: 102) | **proved** / verified circuit |
| the records: 97 @ depth 3, 91 @ depth 4, 88 @ depth 5 | **verified circuits** — and the 97 @ 3 and the 88 @ 5 are re-searchable from scratch, one command each, no seed circuit: `reproduce/`. The 91 @ 4 has no command here yet; it can be *constructed* from GF(2⁸) in two seconds by a generator not yet published, measured and priced in `reproduce/` |
| no 87 shares the internal block structure of the known 88s (its merged top block needs exactly 15 gates; 9–14 all impossible) | **proved** — SAT, independently confirmed by two solver engines, with a positive control; an 87 with *different* structure is not excluded |
| no 87 is one gate-deletion away from any known 88, even with free rewiring of the rest | **exhaustive** — 88,228,896 deletions over all 1,575,516 distinct known 88s, 0 realisable |
| every design rule shared by the known 88s, loosened one at a time and the loosened problem solved exactly, still costs 88 | **exhaustive within each variant** — ~200 variants, none below 88 |
| no 87 within any change of ≤ 4 gates of a known 88 | **exhaustive at that radius**; weak evidence beyond it — see calibration |
| the known 88s' shared value-vocabulary is *not* forced by smallness | **verified counterexample** — see below |
| 88 is optimal | **believed** — see Opinion |

Terms with precise meanings (value/mask, block structure, irreducible, B,
cancellation-free, vocabulary, radius) are defined with runnable checks in
[`DEFINITIONS.md`](DEFINITIONS.md).

## What is NOT claimed

Optimality. The 56–88 gap is real and 32 wide. And the small-edit negatives
above prove exactly their stated radius, no more: genuinely different
solutions sit ~42 gate-changes apart, far beyond any exhausted radius. The
corpus is one search lineage; 1,575,516 collected and set-checked, 28,796
carrying full build recipes for the deeper tests — different quantities, kept
distinct on purpose.

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

## The bounds, as arguments

Each with its statement, a ≤ 1-page writeup of the technique, the certificate,
and a checker that runs on any 32×32 matrix — validated against small
instances with known optima (`bounds/README.md`):

- **≥ 56, unconditional** — a counting argument over reachable value sets;
  the full exhaustion re-runs inside `bounds/` in ~3 minutes on one core.
- **≥ 81 at depth 3** — exhaustive frontier enumeration per level; this bound
  improves with compute and was still climbing when stopped.
- **≥ 92 cancellation-free** — derived twice independently; with the shipped
  102-gate cancellation-free circuit: `92 ≤ optimum_cf ≤ 102`.

## The block-structure theorem

Every known 88 organizes its intermediate values into the same block layout.
Statement: building the merged pair of its two largest blocks takes exactly
15 gates — 9 through 14 are UNSAT. The 14-level was decided by one solver in
~99 core-hours and independently confirmed by a second solver engine
(~130 core-hours) on the same hash-pinned instance; levels 9–11 also hold
under a second, independent encoding (528/528 subcases each), and the
encoding's positive control produces and verifies a real circuit at a
satisfiable setting — proof it can say yes. Consequence: an 87, if it exists,
is built differently from every 88 anyone has found. That says where an 87
cannot be; it is not evidence that one exists elsewhere. Encodings,
instances, DRAT proofs for the cheap levels, and the control are in
`encodings/`.

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
and a tripwire that would have handed us an 87 for free stayed silent over
1.58 million circuits. If an 87 exists, I expect it to look alien: no known
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
- [`leads.md`](leads.md) — the open attacks, ranked by payoff/cost, priced in
  core-hours, with a startable command where the inputs are public. Cheapest
  decisive items: a single ~40 core-hour SAT solve; a possible 90 @ depth 4
  one solve away; any foreign-lineage 88 through the tripwire (seconds).

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
too large to host (the 1.58M-circuit index is 457 MB) are stated as such with
how to request them.

MIT. Cite via `CITATION.cff`.
