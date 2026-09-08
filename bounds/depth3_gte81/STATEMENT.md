# Depth-3 circuits: `N_depth3 >= 80` (certified) and `>= 81` (solver run)

## The claims, and the difference between them

Let `N_depth3` be the minimum number of 2-input XOR gates in a circuit for
MixColumns (`../matrix.txt`) of **depth at most 3**.

> **(1) `N_depth3 >= 80`.** An exact rational weak-duality certificate. Checkable
> in **under a second**, from a JSON file, with nothing but the Python standard
> library. No solver, no floating point, no trust in the session that produced it.

> **(2) `N_depth3 >= 81`.** The dual bound of a branch-and-cut MIP run on the same
> model. Reproducible, but it is a **solver result, not a certificate**: to
> believe it you must re-run HiGHS for hours and trust its dual bound, or take
> the run log at its word.

These are not the same kind of object and this directory does not pretend they
are. (1) is packaged as a checkable certificate; (2) is packaged as a
documented solver run with its log. The known upper bound is 97 (an explicit
verified depth-3 circuit, shipped here as the positive control), so the honest
depth-3 bracket is `81 <= N_depth3 <= 97`.

For context: the best circuit at any depth uses 88 gates, so depth 3 costs
gates — but 81 is still below 88, so this line does not by itself rule out an
87-gate depth-3 circuit.

## The technique

**Step 1 — a complete finite structural model.** For depth `<= 3` the problem
becomes finite and completely enumerable, which happens nowhere else in this
programme. Every MixColumns target has weight 5 or 7, and `5 > 2^2 = 4`, so no
target can be produced at level `<= 2`; every target therefore lies at level
exactly 3, and no target feeds another gate. Hence there are exactly 32 level-3
gates, one per target, and

    N_depth3 = 32 + min ( |L1| + |L2| )

over level-1 gates (weight exactly 2 — "edges") and level-2 gates (weight 3 or
4; weight `<= 2` would be realisable at level 1). A weight-4 level-2 mask is the
XOR of two disjoint edges; a weight-3 one is an input XOR a disjoint edge. Every
level-2 gate feeds only level-3 gates, so it appears in some target
decomposition. Enumerating gives **7,897 candidate level-2 masks, 496 candidate
edges, 6,120 decompositions** — all three counts derived twice independently.

**Step 2 — valid inequalities.** `cuts.py` adds families C1–C10, each a
*theorem* about depth-3 circuits (a level-2 mask forces the edges inside it;
weight-7 targets force a matching; aggregate degree bounds; …). Adding them
cannot change the integer optimum; they only tighten the relaxation.

**Step 3 — an exact rational dual certificate.** The LP is
`min c·p  s.t.  A p >= b, p >= 0` with all-integer `A`, `b`, `c`. Weak duality:
for **any** vector `u >= 0` with `Aᵀu <= c`,

    c·p  >=  u·A·p  >=  u·b     for every feasible p.

So a rational `u` with those two properties is a self-contained, machine-
checkable proof of `|L1| + |L2| >= ceil(u·b)`. `certify.py` obtains such a `u`
from an LP solver *with a slack margin*, rounds it to denominator `10^12`, and
then **re-verifies `u >= 0` and `Aᵀu <= c` in exact integer arithmetic** before
reporting anything. Nothing floating-point survives into the claim, and the
check does not need the solver — or scipy, or numpy — at all.

The certificate is `cert_depth3.json`: **23,450 nonzero duals** over 72,830 rows
and 29,180 variables, with

    exact dual value = 47597998171620 / 10^12 = 47.597998...
    => |L1| + |L2| >= 48
    => N_depth3 >= 32 + 48 = 80

For scale, the same model at three stages:

| dual or LP value used | value | resulting bound on `N_depth3` |
|---|---|---|
| the relaxation without any cuts | 29.19 | 62 |
| an earlier, uncertified CP-SAT dual | 34 | 66 |
| the certified dual shipped here | 47.597998 | 80 |

One cut family alone (C8) accounts for `+1.05` of that.

**Step 4 — where the LP stops, and why 81 needs a MIP.** Only `E ∈ {19, 20}` can
reach 48, and both have LP value **exactly 48.0**, so no further cutting can
raise the LP bound: everything above 80 has to come from integer reasoning.
`mip3.py` runs the same model as a MIP; HiGHS's dual bound reached **49**,
giving `N_depth3 >= 32 + 49 = 81`. That number is real but it is the solver's,
not a certificate's.

## The three mandatory positive controls

A lower bound from a model is worthless if the model is unsound — an over-tight
"valid inequality" would give an arbitrarily large, entirely fake bound. So the
verified **97-gate depth-3 circuit** (shipped here) is mapped into the model and
must satisfy everything:

| control | what it rules out | result |
|---|---|---|
| `control_primal.py` | the structure theorem is wrong | the circuit maps in: 27 edges + 38 level-2 + 32 targets, objective exactly 65 (→ 97) |
| `control_cuts.py` | some cut is not a theorem | 23,405 cuts checked, **0 violated** |
| `control_lp.py` | some LP row is not valid | 72,830 rows checked, **0 violated**, objective 65 |

If any of these failed, every bound in this directory would be vacuous. They are
not optional, and together they run in under a second — see [`RUN.md`](RUN.md).

An independent cross-check on the LP itself: SCIP 10 reproduces the root LP
value to 7 digits through a completely different code path.

## Honest scope

* The model is specific to *this* weight profile: the cuts are theorems about
  targets of weight 5 and 7. The **recipe** — complete structural model →
  valid inequalities → exact rational dual → mandatory primal control — is
  generic, and `mcmatrix.py` is the single place the matrix enters, but pointing
  it at a different matrix requires re-deriving the structure theorem first.
* `>= 80` is a certificate. `>= 81` is a run. Cite them differently.
* Depth 3 is a *restricted* class: none of this bears on `L(M)`, whose refereed
  bracket is `56 <= L(M) <= 88` (see [`../gte56/`](../gte56/)).
