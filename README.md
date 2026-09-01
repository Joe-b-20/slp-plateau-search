# slp-plateau-search

The search for the fewest 2-input XOR gates computing AES MixColumns, and the
evidence it produced. The circuits themselves are published in
[aes-mixcolumns-xor-circuits](https://github.com/Joe-b-20/aes-mixcolumns-xor-circuits);
this repo holds the proofs, the negative results, the instruments, and the
open problems. If you just want to try to beat 88, start there — come here
when you want to know what has already been tried and what is actually proven.

**Where it stands: `56 ≤ minimum ≤ 88`. No 87 was found. 88 is not proven
optimal.**

## The evidence ladder

Every claim this project makes, each in exactly one row:

| claim | status |
|---|---|
| any circuit needs ≥ 56 gates | **proved** — certificate + checker: `bounds/` |
| any depth-3 circuit needs ≥ 81 gates | **proved** — `bounds/` |
| cancellation-free circuits need ≥ 92 (best known: 102) | **proved** / verified circuit |
| the records: 97 @ depth 3, 91 @ depth 4, 88 @ depth 5 | **verified circuits** (the verifier is a proof — see the circuits repo) |
| no 87 shares the internal block structure of the known 88s (its merged top block needs exactly 15 gates; 9–14 all impossible) | **proved** — SAT with a positive control; scope: an 87 with *different* structure is not excluded |
| no 87 is one gate-deletion away from any known 88, even with free rewiring of the rest | **exhaustive** — 88,228,896 deletions over all 1,575,516 distinct known 88s, 0 realisable |
| no 87 within any change of ≤ 4 gates of a known 88 | **exhaustive within that radius** — and near information-free globally (see calibration) |
| ~200 relaxations of the known 88s' structure all price back to exactly 88 | **exhaustive within each stated class** |
| the known 88s' shared vocabulary is *not* forced | **verified counterexample** — an 89 exists using a value no known 88 uses |
| a from-scratch attempt with none of this knowledge reaches 93 | **measurement** |
| 88 is optimal | **believed** — see Opinion |

## What is NOT claimed

Optimality is not proven; the 56–88 gap is real and 32 wide. The exhaustive
local negatives above are weak evidence about whether an 87 exists globally —
our own control audit showed the same tests return "nothing better nearby"
for 89–97-gate circuits too, and genuinely different solutions sit ~42 gate
changes apart while the searches reach 3–4. The 1.58M-circuit corpus is one
search lineage and statistically biased toward it; 1,575,516 were collected
and pass set-level checks, while the full structural test ran on the 28,796
that carry complete build recipes — different quantities, kept distinct on
purpose.

Terms with precise meanings (mask, block structure, irreducible, B,
cancellation-free, vocabulary, radius) are defined with runnable checks in
[`DEFINITIONS.md`](DEFINITIONS.md).

## Instruments you can run on your own circuit

- [`tools/tripwire.py`](tools/tripwire.py) — stdlib, seconds: finds duplicate
  values and dead gates (either one = a free smaller circuit), and reports the
  count B that must equal gates−32 in any irreducible solution. If you hold an
  88 from any source: B ≠ 56 means you are holding an 87 after one deletion.
  (Sound in that direction only; the tool documents the counterexample to the
  converse.)
- `verify_circuit.py` — the oracle; rebuilds MixColumns from FIPS-197, proof
  by the 32 unit inputs.
- [`scripts/overlap.py`](scripts/overlap.py) — shared-value count between two
  circuits (the independence statistic).

## The bounds, as arguments

Each with its statement, a ≤ 1-page writeup of the technique, the certificate,
and a checker that runs on any 32×32 matrix — validated against small
instances with known optima (`bounds/README.md`):

- **≥ 56, unconditional** — a counting argument over reachable value sets.
- **≥ 81 at depth 3** — exhaustive frontier enumeration per level; this bound
  improves with compute and was still climbing when stopped.
- **≥ 92 cancellation-free** — derived twice independently; with the shipped
  102-gate cancellation-free circuit: `92 ≤ optimum_cf ≤ 102`.

## The block-structure theorem

Every known 88 organizes its intermediate values into the same block layout.
Statement: building the merged pair of its two largest blocks takes exactly
15 gates — 9 through 14 are UNSAT (the 14-level: ~99 core-hours, single
solver, instance hash pinned; 9–11 re-proved under a second independent
encoding, 528/528 subcases each, with a positive control that produced and
verified a real solution at a satisfiable setting). Consequence: an 87, if it
exists, is built differently from every 88 anyone has found. Encodings,
instances, and the control are in `encodings/`.

## Calibration — why we distrust our own negatives

Two results in this repo exist to limit what the others may claim. The
control audit: the local-search negatives cannot distinguish an optimal 88
from a non-optimal 89–97, so they carry almost no information about 87's
existence. The from-scratch baseline: with none of this project's accumulated
structure, honest effort reaches 93 — the last five gates are where all the
difficulty lives. Both are first-class results here, not appendix caveats.

## Hypotheses that died

The strongest structural regularity — all 1.58M known 88s draw their values
from one shared 1,778-value vocabulary — is **not** a law: a verified 89
exists using a value outside it, so leaving the vocabulary costs at most one
gate. Several other conjectured invariants fell the same way; each is a row
in [`negatives.jsonl`](negatives.jsonl) with what it does *not* imply.

## Opinion

*Belief, not proof.* We think 88 is optimal: two unrelated search programs
(ours and Jean's AI-based one) stopped at exactly 88; the deletion tripwire
stayed silent over 1.58 million circuits; every relaxation priced back to 88.
Named tension: the second and third of those lean on local negatives — the
very kind the calibration section weakens. The first does not, which is why
independent convergence is the evidence we weight most. If an 87 exists it
must differ from every certified 88 by ≥ 4 values, share no known 88's block
structure, and (likely) have depth ≥ 4.

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
k = 9/10/11 with its positive control and DRAT emission, the `>= 56`
exhaustion, the validation suite), **C** banked and documented rather than
re-run, each with its cost and its artifact. [`INVENTORY.md`](INVENTORY.md) lists
what exists beyond this repo — corpora, certificates, instances, logs — with
exact counts, sizes, and hashes; samples ship here, and the pieces genuinely
too large to host (the 1.58M-circuit index is 457 MB) are stated as such with
how to request them.

MIT. Cite via `CITATION.cff`.
