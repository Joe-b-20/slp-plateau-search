# The control: does the bound machinery overclaim?

## Why this directory exists

A lower-bound argument is only worth reading if it cannot return a number above
the truth. That is not something a reader can take on trust from prose, and it
is not something the MixColumns instance can settle — nobody knows `L(M)`, so
there is nothing there to compare a bound against.

So the machinery is run on **small matrices whose exact optimum is known**, by a
method that shares no code, no encoding and no idea with it.

## What is tested

The instrument under test is `../gte56/` — the Theorem-N bound

    L(M) >= m + min_{K in F} [ (n - |K|) + T + minE_K ]

and the extras-tree searcher `mine.c` that supplies `minE_K`. Not a
reimplementation: the same formula, the same compiled binary.

The reference answers come from an **iterated SAT decision procedure** over an
SLP encoding: it asks "is there a circuit with `k` gates?" for increasing `k`,
and the first satisfiable `k` is the optimum *because the level below it is
recorded UNSAT*. That oracle carries its own controls — it was required to agree
exactly, including on the negative side, with a deliberately naive breadth-first
enumeration sharing no code with it, on random instances small enough to
enumerate; a second, independent CNF implementation of the same decision problem
agreed 10/10 on an unrelated block set. That class of control is not decorative:
an earlier searcher in this programme failed a 120-instance brute-force control
8/120 and had to be fixed.

## The three checks

**0. Preconditions are checked, not assumed.** Lemma F and Theorem N need the
matrix's columns to be non-zero and pairwise distinct. The suite verifies this
before applying anything, and includes an instance that deliberately fails it.

**1. Soundness.** Every Theorem-N bound — at covering levels `m = 0, 1, 2`, and
at every cap on the keep-set size — must be `<=` the known optimum.

**2. Agreement.** `mine` can also compute the optimum outright, because in a
minimum SLP no gate mask repeats and every target of weight `>= 2` is itself a
gate mask, so the gate set is exactly (targets) ∪ (extras) and

    L(M)  =  T + minE(all columns).

The suite computes that and compares it with the SAT optimum. Agreement is a
genuine cross-check of *both* instruments: a C extras-tree exhaustion and a
CNF/CaDiCaL decision procedure, arriving at the same integer from opposite
directions.

**3. Slack.** How much the bound loses when the keep-set is forced to be small —
which is the regime the MixColumns certificate is actually in, since there
`|K| = 14` out of 32 and the exhaustion is what limits it.

## The result, and the one thing it caught

All three instances pass, and the searcher reproduces all three SAT optima
exactly. But the suite did not pass on the first attempt, and the reason is the
most useful thing in this directory.

`tap_P__Q1_2_4_a` has an **entirely zero column**: the instance hands the circuit
a free input that no target uses. Theorem N charges `>= 1` gate for every column
outside the keep-set — that charge is Lemma 1 applied to a *live* column, and a
zero column costs nothing to zero. Applied to that matrix without the
precondition gate, the machinery returns **11 against a true optimum of 10**.

That instance is now a permanent **negative control**. The suite deliberately
runs it with the gate ignored, requires the overclaim to appear, and then drops
the zero column — which cannot change the optimum, since it is an input nothing
uses — and requires the machinery to be sound on the reduced matrix. It is.

This is why `check_gte56.py` reports checks A2 (columns non-zero) and A3
(columns pairwise distinct) before it reports a bound, and why they are not
presented as boilerplate. On MixColumns all 32 columns are non-zero and pairwise
distinct, so the `>= 56` is unaffected — but the precondition is doing real work,
and now there is an instance that proves it.

## How tight is it?

On both clean instances the `m = 1` covering bound is **exactly tight** — 12
against an optimum of 12, and 10 against an optimum of 10 — once the keep-set is
allowed to be large enough for the exhaustion to see the whole instance. Cap the
keep-set below that and the bound degrades gracefully and stays sound:

| instance | optimum | `|K| <= 3` | `<= 5` | `<= 6` | `<= 7` | `<= 8` |
|---|---|---|---|---|---|---|
| `L1_clean_iso` | 12 | 10 | 10 | 11 | 12 | 12 |
| `L5_tap_pairQ3` | 10 | 9 | 9 | 10 | 10 | — |

Read that as the honest picture of the method: it is *capable* of being tight,
and what costs it on MixColumns is not the theorem but the price of the
exhaustion — `|K| = 14` of 32 columns is deep in the left-hand columns of that
table.

## Scope of the control

* Three instances, 4 targets each, over 7–8 columns. They are small because
  proving an optimum is expensive: the reference proof for `L1_clean_iso` alone
  cost 4,511 s of SAT, most of it in the single UNSAT call at `k = 11`.
* They are MixColumns-derived blocks re-expressed in their own input basis, not
  random matrices. A random-matrix sweep would be a stronger control and is not
  claimed here.
* The control tests the `gte56/` machinery. The `depth3_gte81/` and `cf_gte92/`
  bounds carry their own controls in their own directories: three mandatory
  primal controls against a verified 97-gate circuit, and a witness plus a
  cancelling-circuit negative control, respectively.
