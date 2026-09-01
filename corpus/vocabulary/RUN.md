# RUN — the corpus vocabulary, and a circuit outside it

## What the vocabulary is

`vocab.json` is **every distinct non-target gate mask that occurs anywhere in
the 88-gate corpus re-census** — the complete set of intermediate values the
accumulated search has ever produced.

| | |
|---|---|
| circuit rows accepted (88 masks, all 32 targets) | **1,925,065** |
| rows rejected, wrong length | 257,291 |
| rows rejected, missing targets | 0 |
| non-target gate slots examined | **107,803,640** |
| **distinct non-target masks — the vocabulary** | **1,778** |

107.8 million gate slots. **1,778 distinct values.** Every 88-gate circuit the
campaign ever produced was assembled out of that fixed alphabet, and roughly
99.998 % of the slots are repeats.

Per-mask statistics accompany it in `recensus_stats.json`: weight histogram
(mask Hamming weights 2–12, mode 2 at 33.3 M slots), lane histogram, hub
occurrence counts, and the 85 weight-2 masks present.

The obvious question is whether 1,778 is a property of **the problem** or a
property of **the search**. The circuit below settles it.

---

## RE-RUN (1) — verify the 89-gate circuit

`S89_out_of_vocabulary_89gates.json` is a valid 89-gate MixColumns circuit.
`tools/verify_circuit.py` rebuilds MixColumns from GF(2^8) field arithmetic —
the spec *is* that code — replays the circuit, and checks all 32 output bits.

```
$ nice -n 19 python3 tools/verify_circuit.py S89_out_of_vocabulary_89gates.json
gates=89 depth=10 outputs_built=32/32 problems=0
VERDICT: VALID MixColumns circuit
  exit status: 0  (0 = VALID)
```

**PASS condition:** `outputs_built=32/32`, `problems=0`, `VALID`.
**Measured 2026-09-01: 0.05 s wall.**

---

## RE-RUN (2) — the one-command out-of-vocabulary check

Replay the circuit, subtract the 32 target masks, and ask which of the
remaining masks appear in **no** entry of the 1,778-value vocabulary:

```
$ nice -n 19 python3 tools/oov_check.py vocab.json S89_out_of_vocabulary_89gates.json
vocabulary            : 1778 distinct non-target masks
circuit               : 89 gates, 89 distinct masks
  of which targets    : 32 / 32
  non-target masks    : 57
  IN  the vocabulary  : 51
  OUT of the vocabulary: 6
    0x00000088  (decimal 136, Hamming weight 2)
    0x00000098  (decimal 152, Hamming weight 3)
    0x0080048c  (decimal 8389772, Hamming weight 5)
    0x10009898  (decimal 268474520, Hamming weight 7)
    0x8488888c  (decimal 2223540364, Hamming weight 9)
    0x8c88888c  (decimal 2357758092, Hamming weight 10)

VERDICT: OUT OF VOCABULARY. 6 mask(s) in this circuit occur in no
         entry of the 1,778-value corpus vocabulary.
  exit status: 0  (0 = at least one out-of-vocabulary mask)
```

**Measured 2026-09-01: 0.05 s wall.**

Six of its 57 non-target masks — including `0x00000098`, the value the circuit
was pinned on — occur **nowhere** in 107,803,640 gate slots across 1,925,065
circuits. Note their Hamming weights: 2, 3, 5, 7, 9, 10. These are not exotic
in any structural sense. The corpus simply never produced them.

---

## RE-RUN (3) — the negative control

The same check on a published record 88 must come back empty, or the tool would
be finding "out-of-vocabulary" masks everywhere and the result above would be
meaningless:

```
$ nice -n 19 python3 tools/oov_check.py vocab.json ../tripwire_demo/circuits/mixcolumns_88gates_depth5.json
vocabulary            : 1778 distinct non-target masks
circuit               : 88 gates, 88 distinct masks
  of which targets    : 32 / 32
  non-target masks    : 56
  IN  the vocabulary  : 56
  OUT of the vocabulary: 0

VERDICT: entirely inside the corpus vocabulary.
  exit status: 1  (1 = wholly in-vocabulary, as expected)
```

**PASS condition:** 56 of 56 in vocabulary, 0 out.
**Measured 2026-09-01: 0.05 s wall.** Full transcript: `out/VOCAB.txt`.

---

## What this shows, and what it does not

**Shows.** The 1,778-value vocabulary is a property of **the search**, not of
**the problem**. A valid MixColumns circuit exists that speaks six words the
corpus has never once used, and it was found without difficulty once something
deliberately looked outside the alphabet. Any argument of the form "we have
examined 1.9 million circuits and the structure is always X" is bounded by the
alphabet those circuits were built from — and that alphabet is demonstrably not
forced.

This is the concrete reason the corpus-wide negatives in this pack are scoped
the way they are. They are exhaustive over *the corpus*. The corpus is not
exhaustive over *the problem*.

**Does not show.** This circuit is an **89**, not an 88 and not an 87. It costs
one gate more than the record. A search seeded from it, targeting 88, reached no
88: zero improvements in roughly 0.44 core-hours of a budgeted ~1.2, so the run
is a **partial negative and an upper bound from search, not a proof**. The
question of whether an out-of-vocabulary 88 exists one step below it is **open**.

Nothing here bears on the existence of an 87.

---

## Files

| path | what it is |
|---|---|
| `vocab.json` | the 1,778 distinct non-target masks, as a JSON array of ints |
| `recensus_stats.json` | the re-census statistics the vocabulary came from |
| `S89_out_of_vocabulary_89gates.json` | the verified 89-gate circuit, as index pairs |
| `tools/verify_circuit.py` | independent MixColumns verifier, rebuilt from GF(2^8) |
| `tools/oov_check.py` | the one-command vocabulary membership check |
| `out/VOCAB.txt` | transcript of the 2026-09-01 re-runs |
