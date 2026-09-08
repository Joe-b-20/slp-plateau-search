# The control audit: the project's own negatives price at LR ≈ 1.00

**Document only. Nothing to re-run here** — this page states a result computed
elsewhere and cites its artifacts.

---

## What was audited

The project accumulated a very large stock of negative results of the form
*"nothing better exists nearby"*: exhaustively empty `k ≤ 4` deletion shells,
empty move-class neighbourhoods, derivation-rigidity statistics, dead-gate
counts, mutation sweeps. Roughly **165 million exact window decisions, zero
reducible windows.** These were being read as evidence that 88 is optimal.

The audit ran those same instruments on inputs whose ground truth is known to be
**positive** — circuits that provably *can* be improved, because a smaller
verified circuit exists in the same repository.

## The result

**The instruments return the same answer either way.**

### (a) The exact bounded-radius decider

Run on 7 circuits from 97 gates down to 88, every one of them provably
improvable:

| circuit | gates @ depth | exhaustive k=2 windows | reducible | sampled k=3 | reducible |
|---|---|---:|---:|---:|---:|
| cascade d3 | 97 @ 3 | 2080 | 0 | 1200 | 0 |
| parallel d4 | 94 @ 4 | 1891 | 0 | 1200 | 0 |
| parallel d5 | 92 @ 5 | 1770 | 0 | 1200 | 0 |
| cascade d10 | 91 @ 5 | 1711 | 0 | 1200 | 0 |
| parallel d11 | 90 @ 5 | 1653 | 0 | 1200 | 0 |
| imported 89 | 89 @ 9 | 1596 | 0 | 1200 | 0 |
| imported 88 | 88 @ 7 | 1540 | 0 | 1200 | 0 |

**12,241 exhaustive k=2 windows and 8,400 sampled k=3 windows. Zero reducible,
everywhere.** A 97-gate circuit — nine gates too big — has an exhaustively empty
`k = 2` shell, exactly like the 88.

### (b) The structural rigidity statistics

1,200 reservoir-sampled states per gate-length, drawn from a corpus of ~3.16 M
states:

| gates | options per gate (mean) | dead-gate states |
|---:|---:|---:|
| 88 | 2.3236 | 0 |
| 89 | 2.3238 | 0 |
| 90 | 2.3262 | 0 |
| 91 | 2.3205 | 0 |
| 92 | 2.3123 | 0 |

Identical to four significant figures across 88–92.

### Why that is a likelihood ratio of 1.00

An instrument that returns the same value on an optimal circuit and on a
four-gates-too-big one has **likelihood ratio ≈ 1.00** about optimality: the
ratio of the probability of its output given the circuit is optimal to that
given it is improvable. **LR = 1.00.** The reading carries no information.

The instruments themselves are not broken, and this was checked: a completeness
control planted 4,200 YES windows across 74 circuits and the decider **missed
zero**. It finds what is there. At these radii there is nothing to find, at 97
gates as much as at 88.

The campaign's rigidity framing was also **inverted**. Against a proper null —
random 88-mask subsets, at 0.495 options per gate — real 88s are **4.7× more
derivation-rich, not rigid.**

## What this reprices, and what it leaves alone

**Repriced.** Not the certificates — an exhaustively empty shell is still an
exhaustively empty shell. What is wrong is **the inference drawn from them**.
Every neighbourhood, vocabulary and "nothing better nearby" negative in the
project is true, correctly scoped, and **carries no information about whether an
87 exists**. These are *locality theorems* — rigidity statements about small,
completely enumerated neighbourhoods — **not bounds**.

**Untouched.**

* **Lower bounds.** `L(M) ≥ 56` is refereed. These are proofs, not evidence.
* **Upper bounds.** Every verified circuit is a witness and stands on its own.
* **The `B = 56` tripwire**
  ([`../tripwire_demo/RUN.md`](../tripwire_demo/RUN.md)) — a theorem with a
  decision rule, not a rigidity statistic. It either produces a smaller circuit
  or it does not.
* **The deletion certificate** in this pack. It is a statement about what the
  known 88s admit, exhaustive over its stated population, with a positive
  control that fires. It is not offered as evidence that 87 does not exist, and
  [`../deletion_certificate/CERT.md`](../deletion_certificate/CERT.md) §7 says
  so.

## The public-safe statement

> A negative at radius ≤ 4 carries no information about whether an 87 exists.
> These are locality theorems — rigidity statements about small, completely
> enumerated neighbourhoods — not bounds. By this instrument an optimal circuit
> and a four-gates-too-big circuit are indistinguishable: derivation richness and
> dead-gate count are identical to four significant figures at 88, 89, 90, 91 and
> 92 gates. The bracket is `56 ≤ L(M) ≤ 88`.

## Why the scale of a negative is not its strength

The rest of this pack is negatives, and a reader is entitled to know which of
them the project's own audit has already discounted. The size of a negative and
its informativeness are different quantities: 88 million deletions is a fact
about population size, not about optimality.

## Artifact citations

The primary computed sources are the differential-by-length table and the
script that produced it (reservoir sampling, fixed seed), and the decider
control's summary and per-circuit transcript. Both catalog entries derived from
them were independently re-derived by a referee and passed; for the `k = 3`
figures the per-circuit log is the correct primary, as the summary JSON carries
stale zeros for four circuits. The published statement of the control appears in
the campaign's own certificates document, which was amended to carry it.
