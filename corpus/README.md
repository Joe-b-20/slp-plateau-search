# Corpus-scale results — reproduction pack

Seven self-contained sections. Each has a `RUN.md` carrying the exact command to
run from that directory, the real pasted output, the time it took when it was
last re-run, and — where the full-scale version takes more than a minute — the
historical cost of the full run and its banked result.

Everything here concerns **AES MixColumns as an XOR straight-line program**: 32
inputs, 32 outputs, 2-input XOR gates, minimise the gate count. The best known
circuit uses **88** gates. The refereed bracket is `56 ≤ L(M) ≤ 88`.

A circuit's **value set** is the set of intermediate values its gates compute:
one value per gate, written as the 32-bit mask of which inputs that gate is the
XOR of. Identity, populations and most results in this pack are stated over
value sets rather than over circuits. See
[`../DEFINITIONS.md`](../DEFINITIONS.md).

## What is in the pack

| section | what it is | re-runs in |
|---|---|---|
| [`deletion_certificate/`](deletion_certificate/RUN.md) | **the main result.** 88,228,896 single-gate deletions over all 1,575,516 distinct verified 88-gate **value sets** — 0 realisable | < 1 s (controls + sample), 15 s (Python agreement) |
| [`sample/`](sample/RUN.md) | a documented 520-set sample of the corpus, drawn across every lineage, all five published 88s included | 0.04 s |
| [`tripwire_demo/`](tripwire_demo/RUN.md) | the `B = 56` instrument: point it at a stranger's circuit, learn in seconds whether a gate is deletable | < 1 s |
| [`vocabulary/`](vocabulary/RUN.md) | the 1,778-value corpus vocabulary, and a verified 89-gate circuit that uses six values outside it | 0.15 s |
| [`calibration/`](calibration/CALIBRATION.md) | what a from-scratch clean-room search reaches (93), and the audit that prices the project's own negatives at LR ≈ 1.00 | 0.05 s |
| [`records_check/`](records_check/RUN.md) | verify every record circuit against a from-first-principles MixColumns implementation | 21 s |
| [`depth_forced/`](depth_forced/DEPTH_FORCED.md) | depth is a property of the **value set**: every shipped circuit is already at the shallowest depth its own value set admits, so no 88 can be rescheduled shallower | 0.02 s |

The three instruments in the pack have a `HOW.md` explaining the mechanism with
diagrams: [`deletion_certificate/HOW.md`](deletion_certificate/HOW.md),
[`sample/HOW.md`](sample/HOW.md), [`depth_forced/HOW.md`](depth_forced/HOW.md),
and the tripwire's is [`../tools/HOW.md`](../tools/HOW.md).

## Suggested order

1. **`records_check/`** first. If the circuits are not what they claim to be,
   nothing else matters. 21 seconds.
2. **`tripwire_demo/`** — the fastest real instrument in the pack, with its
   positive controls. Shows what a *constructive* negative looks like.
3. **`deletion_certificate/`** — the main result. Run the positive control
   before the certificate: a tool that cannot report a realisable deletion says
   nothing when it reports none.
4. **`sample/`** — what the certificate ran over, and how it was drawn.
5. **`vocabulary/`** — why the corpus-scale negatives are scoped to *the
   corpus* and not to *the problem*.
6. **`calibration/`** — how hard the problem is from cold, and which of this
   project's negatives its own audit has already discounted.
7. **`depth_forced/`** — 0.02 s, and it rules out one route a reader is likely
   to propose: you cannot take an 88 you already have and reschedule it down to
   the record depth.

## Requirements

Python 3 (**standard library only** — no packages) and a C compiler for the one
C tool. No SAT solver, no network, nothing to install.

## Two things this pack will not claim

**It does not claim 88 is optimal.** The deletion certificate is exhaustive over
1,575,516 known 88-gate value sets. It says nothing about 87-gate circuits
unrelated to any of them, and
[`deletion_certificate/CERT.md`](deletion_certificate/CERT.md) §7 states that
scope explicitly.

**It does not offer neighbourhood emptiness as evidence of optimality.** The
project's own control audit found that its exact decider returns "irreducible"
about a 97-gate circuit that has a verified 88 nine gates below it — a
likelihood ratio of about 1.00 about optimality. That audit is reproduced in
[`calibration/CONTROL_AUDIT.md`](calibration/CONTROL_AUDIT.md) rather than
omitted, because a reader is entitled to know which negatives have already been
discounted.

The results that survive that repricing are the ones stated here: constructive
tripwires, exhaustive statements correctly scoped to their population, and
verified circuits.

## Conventions

* All commands are `nice -n 19` and use at most two threads.
* All pasted outputs are real, captured on the dates shown, on one machine
  under load. Timings are wall-clock and will vary.
* All paths in `RUN.md` files are relative to the directory the `RUN.md` is in.
* Circuit files are index pairs: signals `0..31` are the 32 inputs, gate *k*
  produces signal `32+k` as the XOR of two earlier signals.
* Value sets are identified by
  `canon = sha256(",".join("%08x" % m for m in sorted(masks)))[:16]` — the
  sorted multiset of gate output masks. Two circuits with the same `canon`
  compute the same values whatever order they were built in.
