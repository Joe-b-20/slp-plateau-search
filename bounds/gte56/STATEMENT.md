# `L(M) >= 56` — unconditional

## The claim

Let `M` be the 32x32 GF(2) matrix of AES MixColumns (`../matrix.txt`; sha256 in
`../matrix.sha256`). Let `L(M)` be the minimum number of 2-input XOR gates in
any straight-line program computing all 32 output bits from the 32 input bits.

> **Every XOR circuit for MixColumns uses at least 56 gates.**

No assumption about depth, structure, wiring, fan-out or search history. The
best known circuit uses 88 gates, so the honest bracket is `56 <= L(M) <= 88`.

## The technique: adaptive gate elimination

Two ingredients, combined.

**Lemma F (fan-out).** Let `A` be a 32-row GF(2) matrix whose zero columns form
a set `Z`, whose non-zero columns are pairwise distinct, and all of whose rows
have weight `>= 2`. Then any *optimal* SLP `C` for `A`

  (i) uses no input of `Z` as an operand. Substituting `x := 0` for `x in Z`
  changes no row of `A`; if such an `x` were an operand, deleting it yields a
  strictly smaller SLP for `A`, contradicting optimality.

  (ii) has some live input of fan-out `>= 2`. The first gate of `C` takes two
  input operands, live by (i). If both, `x_i` and `x_k`, had fan-out 1, that
  gate is the unique consumer of both, and then every gate mask has equal `i,k`
  coordinates (induction: the shared consumer does; any other gate's operands
  are other inputs, with coordinates `0,0`, or gates, equal by induction).
  Every row of `A` has weight `>= 2`, hence is a gate mask, hence columns `i`
  and `k` of `A` are equal — contradiction.

**Zeroing (Lemma 1).** Setting an input to zero and deleting the gates it feeds
gives an SLP for the matrix with that column zeroed. If the zeroed input has
fan-out `>= 2` we lose at least 2 gates; otherwise at least 1.

**Theorem N.** Let `F` be a family of column sets, each `K in F` having the 32
rows of `M|_K` pairwise distinct of weight `>= 2` (*admissible*) and
`minE_K >= e_K`. If for every `m`-subset `A` of the columns there is a `K in F`
with `A ∩ K = {}` (the *level-m covering hypothesis*), then

> `L(M) >= m + min_{K in F} [ (32 - |K|) + 32 + e_K ]`.

*Proof.* Run the zeroing chain **adaptively**. At stage `k` let `C_k` be an
optimal SLP for `A^(k)` (`M` with the already-chosen columns zeroed). The
hypotheses of Lemma F hold at every stage: live columns are columns of `M` and
pairwise distinct, and every row still has weight `>= 2` because the zeroed set
is always inside the complement of some `K in F`, whose `M|_K` has all row
weights `>= 2` (weights are monotone along the chain). So Lemma F gives a live
input `y_k` of fan-out `>= 2` in `C_k`. For the first `m` stages, zero `y_k`
itself: the covering hypothesis guarantees a `K in F` avoiding everything zeroed
so far, so the plan stays completable, and each such stage is worth `>= 2`. Then
fix a `K in F` disjoint from the `m` zeroed columns and zero the remaining
`32 - |K| - m` columns outside `K`, each worth `>= 1`. Finally
`L(M|_K) >= 32 + minE_K`: in a minimal SLP the 32 restricted target masks are
distinct and of weight `>= 2`, so each is a distinct gate, and `minE_K` counts
the minimum number of further gate masks needed to realise them. Summing gives
the claim. ∎

The adaptivity is the point. A fixed keep-set lets an adversary park all the
high fan-out on the kept columns; choosing `K` *after* seeing where the fan-out
is, using the symmetry group to have enough keep-sets to choose from, removes
that escape.

## The certificate

`cert56.json` instantiates Theorem N at `m = 1` with the family `F` = the four
`sigma`-conjugates of one keep-set (`sigma` = the byte rotation of the signal
indices, an order-4 automorphism of `M`):

    K = {2, 4, 7, 9, 15, 18, 20, 21, 22, 24, 25, 29, 30, 31},   |K| = 14

    L(M)  >=   m  +  (32 - |K|)  +  32  +  e_K
          >=   1  +      18      +  32  +   5    =   56
               |          |          |        |
        covering    columns outside  the 32   certified
          bonus      the keep-set   targets    extras

## What is checkable in closed form, and what is not

`check_gte56.py` verifies, against `../matrix.txt`, every term but `e_K`:

* the matrix hypotheses (columns nonzero and pairwise distinct; rows of weight
  `>= 2`) that Lemma F needs;
* that the certificate's `sigma` really is an automorphism of the supplied
  matrix, entry by entry, and has order 4;
* Theorem-N admissibility of `K` and of all four of its conjugates;
* the level-1 covering hypothesis: the four conjugates have empty intersection,
  so every column is avoided by one of them;
* the screen `e_K <= jam(K)` — `jam(K)` is the number of restricted targets not
  reachable by free closure, and `minE <= jam` always, so a certificate claiming
  more extras than the jam would refute itself. Here `jam(K) = 8`;
* the arithmetic;
* a positive control on the realizability predicate: a recorded 4-extra witness
  for a *different, failing* keep-set really does complete it.

**`e_K = 5` is not a short certificate — it is an exhaustion.** `minE(K) >= 5`
— no set of four or fewer extra masks completes `M|_K` — is the output of a
depth-4 exhaustion of the extras tree, run to completion by **two independent
implementations**:

| implementation | root branches | shards | nodes | result |
|---|---|---|---|---|
| unpruned C searcher (independent referee's own code) | 511/511 | 114/114 | 9.43e10 | NO COMPLETION |
| pruned searcher (originating lane's code) | 511/511 | 114/114 | 4.75e9 | NO COMPLETION |

Both report the identical root state (free closure 24/32, `|avail| = 38`, 511
root candidates); each covers every branch index 0..510 exactly once; all 228
shard files end `SHARD-DONE ... NO-COMPLETION`.

**The exhaustion is shipped and it is cheap.** `mine.c` (single file, no
dependencies, takes an arbitrary target list) is the searcher, and
`--minE-depth D` re-runs it in-band:

| depth | what it certifies | bound | measured here |
|---|---|---|---|
| 3 | `minE >= 4` | `L(M) >= 55` | 5,784,927 nodes, **0.8 s**, one core |
| 4 | `minE >= 5` | `L(M) >= 56` | 1,895,523,772 nodes, **166 s**, one core |

So the whole of `L(M) >= 56` is reproducible inside this directory in under
three minutes on one core — the historical run needed 16 workers because it was
sharded and, on one of the two code paths, deliberately unpruned. Note the
distinction honestly: the run reproduced here is the **pruned** code path (the
last-level and canonical-order prunings, both proved sound in `mine.c`'s header
comment). The 9.43e10-node **unpruned** exhaustion is what makes the result
prune-independent, and that one is cited, not re-run. See `RUN.md`.

## Honest scope

* This is the *only* unconditional lower bound on `L(M)` in the programme, and
  56 is where its family stops, not where it was abandoned. The whole `|K| = 14`
  layer is exhausted: of twelve covering certificates tested at depth 4, eleven
  have `minE = 4` **exactly** (explicit 4-extra witnesses; one is shipped here as
  the control), and one — this one — survives.
* The next rung, `minE >= 6` at depth 5 giving 57, is estimated at ~500x the
  depth-4 cost.
* The gap 56..88 is entirely about *middle* gates. In a minimum SLP all 32
  targets are distinct masks of weight `>= 5`, so exactly 32 gates carry target
  masks and the rest are middles: `88 = 32 + 56`, and the bound is `56 = 32 + 24`.
  The `+32` is free; the proof effort has bought 24 middles against the record's
  56.
* Theorem N is stated for any GF(2) matrix with distinct non-zero columns and an
  automorphism group; `check_gte56.py` and `mine.c` both take an arbitrary
  matrix. `../validation/` runs exactly this machinery on small instances whose
  optimum is known exactly.
