# Lower bounds, as arguments you can run

Three lower bounds on the cost of AES MixColumns as an XOR circuit. Each one is
packaged the same way: the claim, the technique named, a proof sketch you can
read in a page, the certificate or data as a file, a checker that runs on it,
and a `RUN.md` giving the exact command, the real expected output, and a
measured wall time.

The matrix is `matrix.txt` — 32 rows, 32 columns, one character per entry — and
its sha256 is in `matrix.sha256`. Every checker reads it; none of them has the
matrix baked in.

```
9c337107cba5b0b434fc580ccb1d0323ac51ce17a5fe99da91b97aa8fbc7b620  matrix.txt
```

## The three bounds

| directory | claim | kind of evidence | check cost |
|---|---|---|---|
| [`cf_gte92/`](cf_gte92/) | `L_cf(M) >= 92` (cancellation-free), and `<= 102` | price certificate, solver-free; derived twice independently; plus an explicit witness | **0.03 s** |
| [`gte56/`](gte56/) | `L(M) >= 56`, unconditional | Theorem-N hypotheses checkable in closed form, plus an exhaustion that is shipped and re-runnable | **0.11 s** + **166 s** to re-run the exhaustion |
| [`depth3_gte81/`](depth3_gte81/) | `N_depth3 >= 80` certified, `>= 81` by solver | exact rational dual certificate, plus three mandatory soundness controls | **0.29 s** + **0.5 s** of controls |

Read `cf_gte92/` first. It is the strongest thing here, and the only proved
quantity in the whole programme that lies **above** the 88-gate record: every
XOR circuit for MixColumns with at most 91 gates must contain a cancelling gate.

Each directory also has a `HOW.md`: the counting argument's shape, what the
searcher or the checker actually does, and the entry-point command —
[`cf_gte92/HOW.md`](cf_gte92/HOW.md), [`gte56/HOW.md`](gte56/HOW.md),
[`depth3_gte81/HOW.md`](depth3_gte81/HOW.md),
[`validation/HOW.md`](validation/HOW.md).

## Where the bounds actually sit

    L(M)         56  <=  L(M)  <= 88          (88 = the best known circuit)
    L_cf(M)      92  <=  L_cf  <= 102         (cancellation-free only)
    N_depth3     81  <=  N_d3  <= 97          (depth <= 3 only)

`L(M) <= 88` and the two upper bounds are witnesses — explicit circuits — and
are not re-argued here. **`L(M) = 88` is not claimed and is not proved.** The
gap 56..88 is entirely about *middle* gates: in a minimum SLP exactly 32 gates
carry target masks and the rest are middles, so `88 = 32 + 56` and the bound is
`56 = 32 + 24`. The `+32` is free; the proof work has bought 24 middles against
the record's 56.

## The control

[`validation/`](validation/) is the credibility control the rest of this
directory rests on. A lower-bound method is only worth reading if it cannot
return a number above the truth, so the `gte56/` machinery — the same Theorem-N
formula and the same searcher — is run on small matrices whose exact optimum was
proved by a completely unrelated method (iterated SAT, with the level below the
optimum recorded UNSAT).

It does three things: it checks no bound exceeds a known optimum; it checks the
searcher's own exact answers agree with the SAT optima, which is a real
cross-check of two unrelated code paths; and it includes a deliberate **negative
control** — a matrix with an unused input — showing that if you skip the
precondition `check_gte56.py` enforces, the machinery *does* overclaim. That
instance is in the suite because it makes the precondition visible rather than
decorative.

## What you need

Python 3, standard library only, for every checker. One C compiler, once, if you
want to re-run the `gte56/` exhaustion:

```
cc -O2 -o gte56/mine gte56/mine.c
```

`numpy`/`scipy` and `highspy` appear only in the *generation* paths of
`depth3_gte81/`, never in a check. That separation is deliberate: verifying a
proof must not depend on a solver stack.

## Honest labelling

Two things in here are runs, not certificates, and are marked as such wherever
they appear:

* **`N_depth3 >= 81`** is a HiGHS dual bound from a branch-and-cut run that hit
  its time limit with a 67 % gap. The bound is valid; the run proves nothing
  further and did not converge. The certified, independently checkable number at
  depth 3 is **80**.
* **`e_K = 5`** in `gte56/` is an exhaustion, not a short certificate. It is
  shipped and re-runnable here in 166 s single-core — but the run reproduced
  here uses two (sound, documented) prunings, whereas the historical
  `9.43e10`-node run used none, and that unpruned run is what makes the result
  prune-independent. It is cited, not reproduced.
