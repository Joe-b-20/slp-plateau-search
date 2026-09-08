# How the validation suite works

[`STATEMENT.md`](STATEMENT.md) says why this directory exists and what it caught;
[`RUN.md`](RUN.md) gives the command and the transcript. This file explains the
mechanism: what is enumerated, how the exact optimum of a small instance is
obtained, and what each assertion would catch.

## 1. What is under test

The machinery of [`../gte56/`](../gte56/) — the same formula and the *same
compiled binary*, not a reimplementation — is run on small matrices whose exact
optimum was proved by an unrelated method (iterated SAT, with the level below the
optimum recorded UNSAT), and every bound it produces is compared against that
optimum.

Three instances ship, and one of them is designed to fail:

| instance | role | columns | targets | known optimum |
|---|---|---|---|---|
| `L1_clean_iso` | positive | 8 | 4 | 12 |
| `L5_tap_pairQ3` | positive | 7 | 4 | 10 |
| `tap_P__Q1_2_4_a` | precondition negative control | 8 | 4 | 10 |

They are MixColumns-derived blocks re-expressed in their own input basis, not
random matrices, so they exercise the machinery on the kind of structure it is
aimed at.

## 2. What the suite computes for each instance

```mermaid
flowchart TD
    A["instance matrix and its SAT-proved optimum"] --> B["preconditions: any zero column? any duplicate columns?"]
    B --> C["exact answer: climb the extras ladder d = 0, 1, 2, ... until the searcher says COMPLETION"]
    C --> D["optimum equals targets plus that d, compared with the SAT optimum"]
    A --> E["enumerate EVERY admissible keep set of the columns"]
    E --> F["for each, run the same ladder on the restricted targets"]
    F --> G["value of a keep set = live columns outside it + targets + its extras"]
    G --> H["for each threshold, take the family of keep sets scoring at least it"]
    H --> I{"does that family miss every choice of m columns?"}
    I -->|"no"| H
    I -->|"yes"| J["bound at level m = m + threshold"]
    J --> K{"role"}
    K -->|"positive"| L["every bound at every level must be at most the optimum"]
    K -->|"negative control"| M["the bound must EXCEED the optimum, by the amount recorded"]
```

Three mechanisms need naming precisely.

**The exact optimum, from the same searcher.** For `d = 0, 1, 2, …` the suite
invokes `mine` on the instance's full target list at depth `d` and returns the
first `d` that reports `COMPLETION`. That `d` is exactly the minimum number of
extra masks, so the optimum is `targets + d`. This works because in a minimum
XOR straight-line program no gate mask repeats and every target of weight ≥ 2 is
itself a gate mask, so the gate set is exactly the targets plus the extras.
Since the SAT optima came from unrelated code, agreement here is a genuine
cross-check of two independent paths, not a self-consistency test.

**The full bound table, by brute force.** Every subset of the columns of size
2..n is enumerated, filtered to the admissible ones, and priced by the same
ladder. This is why the suite only handles 7–8 column instances: the table is
exponential in the number of columns and every cell is a subprocess ladder.

**The best covering family, by descending threshold.** Distinct table values are
walked from the top; at each threshold the family of keep sets scoring at least
that much is tested for whether it misses every `m`-subset of columns. The first
threshold that covers gives the bound `m + threshold`, and it is the maximum
because the family only grows as the threshold falls. The suite reports this at
levels `m = 0, 1, 2`, and then repeats the `m = 1` computation with the table
restricted to keep sets of size at most a cap, for every cap — which shows how
much of the bound depends on being allowed large keep sets.

## 3. How the negative control is enforced

`tap_P__Q1_2_4_a` has an entirely **zero column**, and applying Theorem N to it
without the precondition returns **11 against a true optimum of 10**;
[`STATEMENT.md`](STATEMENT.md) gives the reason and what it caught.

The suite's role dispatch is what turns that into a test: a positive instance
must pass its preconditions and produce only sound bounds; the control must
**fail** its preconditions, must overclaim by the exact recorded amount, and must
become sound once reduced. Exit status is 0 only if every one of those holds.

## 4. What it established

- **Agreement:** the searcher reproduced all three SAT optima exactly —
  `4 + 8 = 12`, `4 + 6 = 10`, `4 + 6 = 10`. The two instruments share no code.
- **Soundness:** no bound above a known optimum on either clean instance, at any
  level or cap. On both, the level-1 bound is exactly *tight* — 12 against 12
  and 10 against 10 — once the keep set is allowed to be large enough, so the
  formula is not merely safe but sharp on this kind of instance.
- **The limitation:** with the keep set capped small the bound loses up to two
  gates (the cap-by-cap table is in [`STATEMENT.md`](STATEMENT.md)). On
  MixColumns the certificate uses a keep set of 14 of 32 columns, so it is in
  the region where the bound is not yet tight.
- Almost all the run time is one deep exhaustion (2.7e9 nodes) on
  `L1_clean_iso`; the other two instances together take **0.4 s**. Wall times,
  node counts and the provenance of the reference optima are in
  [`RUN.md`](RUN.md).

## 5. Run it

From the `bounds/` directory:

```
cc -O2 -o gte56/mine gte56/mine.c                              # once

python3 validation/run_validation.py                            # ~160 s
python3 validation/run_validation.py --instance L5_tap_pairQ3   # 0.2 s
```

The short form exercises every code path except the deep exhaustion, which makes
it the smoke test to run after changing anything in [`../gte56/`](../gte56/).
Also accepted: `--mine PATH` and `--max-depth D`. [`RUN.md`](RUN.md) gives the
full expected transcript.
