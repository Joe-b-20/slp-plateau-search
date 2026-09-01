# Corpus-scale results — reproduction pack

Six self-contained sections. Each has a `RUN.md` carrying the exact command to
run from that directory, the real pasted output, the time it took when it was
last re-run, and — where the full-scale version does not fit in a coffee break —
the historical cost of the full run and its banked result.

Everything here concerns **AES MixColumns as an XOR straight-line program**: 32
inputs, 32 outputs, 2-input XOR gates, minimise the gate count. The best known
circuit uses **88** gates. The refereed bracket is `56 ≤ L(M) ≤ 88`.

## What is in the pack

| section | what it is | re-runs in |
|---|---|---|
| [`deletion_certificate/`](deletion_certificate/RUN.md) | **the headline result.** 88,228,896 single-gate deletions over all 1,575,516 distinct verified 88s — 0 realisable | < 1 s (controls + sample), 15 s (Python agreement) |
| [`sample/`](sample/RUN.md) | a documented 520-set sample of the corpus, drawn across every lineage, all five published 88s included | 0.04 s |
| [`tripwire_demo/`](tripwire_demo/RUN.md) | the `B = 56` instrument: point it at a stranger's circuit, learn in seconds whether a gate is deletable | < 1 s |
| [`vocabulary/`](vocabulary/RUN.md) | the 1,778-value corpus mask vocabulary, and a verified 89-gate circuit that speaks six words outside it | 0.15 s |
| [`calibration/`](calibration/CALIBRATION.md) | what a from-scratch clean-room search reaches (93), and the audit that prices the project's own negatives at LR ≈ 1.00 | 0.05 s |
| [`records_check/`](records_check/RUN.md) | verify every record circuit against a from-first-principles MixColumns implementation | 21 s |

## Suggested order

1. **`records_check/`** first. If the circuits are not what they claim to be,
   nothing else matters. 21 seconds.
2. **`tripwire_demo/`** — the cheapest real instrument in the pack, with its
   positive controls. Shows what a *constructive* negative looks like.
3. **`deletion_certificate/`** — the headline. Run the positive control before
   the certificate; a `0` from a tool that cannot return anything else is
   worthless.
4. **`sample/`** — what the certificate ran over, and how it was drawn.
5. **`vocabulary/`** — why the corpus-scale negatives are scoped to *the
   corpus* and not to *the problem*.
6. **`calibration/`** — how hard the problem is from cold, and which of this
   project's negatives its own audit has already discounted.

## Requirements

Python 3 (**standard library only** — no packages) and a C compiler for the one
C tool. No SAT solver, no network, nothing to install.

## Two things this pack will not claim

**It does not claim 88 is optimal.** The deletion certificate is exhaustive over
1,575,516 known 88s. It says nothing about 87-gate circuits unrelated to any of
them, and `deletion_certificate/CERT.md` §7 states that scope explicitly.

**It does not offer neighbourhood emptiness as evidence of optimality.** The
project's own control audit found that its exact decider returns "irreducible"
about a 97-gate circuit that has a verified 88 nine gates below it — a
likelihood ratio of about 1.00 about optimality. That audit is reproduced in
`calibration/CONTROL_AUDIT.md` rather than omitted, because a reader is entitled
to know which negatives have already been discounted.

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
* Mask sets are identified by
  `canon = sha256(",".join("%08x" % m for m in sorted(masks)))[:16]` — the
  sorted multiset of gate output masks. Two circuits with the same `canon`
  compute the same values whatever order they were built in.
