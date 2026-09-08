# `bounds/validation/` — how to run it

Typed from the **pack root** (`bounds/`). Python 3 standard library only, plus
the searcher from [`../gte56/`](../gte56/), which must be compiled once:

```
cc -O2 -o gte56/mine gte56/mine.c
```

## Files

| file | what it is |
|---|---|
| `STATEMENT.md` | why the control exists, what it tests, and what it caught |
| `HOW.md` | the mechanism: what is enumerated, how each optimum is obtained, what each assertion would catch |
| `known_optima.json` | the instances, their proved optima, and the evidence for each |
| `instances/*.txt` | the matrices, same format as `../matrix.txt` |
| `run_validation.py` | the suite |

## The command

```
python3 validation/run_validation.py
```

Expected output — the real transcript from the re-run, abridged only where
marked:

```
control: the bound machinery of ../gte56/ must never exceed a known optimum
searcher: gte56/mine

--------------------------------------------------------------------------
instance L1_clean_iso   (4 targets over 8 columns)   role: positive
  known optimum         : 12   [PROVED EXACT]
  proved by             : iterated SAT (CaDiCaL) over an SLP encoding
  ladder                : k=7 UNSAT (0.46 s), k=8 UNSAT (2.00 s), k=9 UNSAT (16.55 s), k=10 UNSAT (255.15 s), k=11 UNSAT (4235.96 s), k=12 SAT (1.19 s)
  searcher exact answer : 4 targets + minE 8 = 12   [AGREES]  (169.5 s)
  preconditions         : columns nonzero and pairwise distinct -- OK

  [as given] admissible keep-sets : 143

    level  bound    optimum  slack    verdict
    m=0    12       12       0        sound
    m=1    12       12       0        sound
    m=2    12       12       0        sound

    |K| capped at  best m=1 optimum  verdict
    3              10       12       sound
    4              10       12       sound
    5              10       12       sound
    6              11       12       sound
    7              12       12       sound
    8              12       12       sound

  searcher work for this instance: 2.7e+09 nodes, 170.1 s

--------------------------------------------------------------------------
instance L5_tap_pairQ3   (4 targets over 7 columns)   role: positive
  known optimum         : 10   [PROVED EXACT]
  proved by             : iterated SAT over the same encoding
  ladder                : G=4 UNSAT, G=5 UNSAT, G=6 UNSAT, G=7 UNSAT, G=8 UNSAT, G=9 UNSAT, G=10 SAT
  searcher exact answer : 4 targets + minE 6 = 10   [AGREES]  (0.1 s)
  preconditions         : columns nonzero and pairwise distinct -- OK

  [as given] admissible keep-sets : 60

    level  bound    optimum  slack    verdict
    m=0    10       10       0        sound
    m=1    10       10       0        sound
    m=2    10       10       0        sound

    |K| capped at  best m=1 optimum  verdict
    3              9        10       sound
    4              9        10       sound
    5              9        10       sound
    6              10       10       sound
    7              10       10       sound

  searcher work for this instance: 7.97e+05 nodes, 0.1 s

--------------------------------------------------------------------------
instance tap_P__Q1_2_4_a   (4 targets over 8 columns)   role: precondition_negative_control
  known optimum         : 10   [PROVED EXACT]
  proved by             : iterated SAT over the same encoding
  ladder                : not itemised in the banked row; the solver reports exhaustive proof of optimality
  searcher exact answer : 4 targets + minE 6 = 10   [AGREES]  (0.1 s)
  preconditions         : VIOLATED: zero columns [4], duplicate column pairs []

  This instance is in the suite to show that the precondition is
  LOAD-BEARING.  Applying Theorem N anyway, ignoring the gate:

  [precondition IGNORED] admissible keep-sets : 116

    level  bound    optimum  slack    verdict
    m=0    11       10       -1       OVERCLAIM
    m=1    11       10       -1       OVERCLAIM
    m=2    11       10       -1       OVERCLAIM

    |K| capped at  best m=1 optimum  verdict
    3              10       10       sound
    4              10       10       sound
    5              10       10       sound
    6              11       10       OVERCLAIM
    7              11       10       OVERCLAIM
    8              11       10       OVERCLAIM

  => it OVERCLAIMS: 11 against a true optimum of 10.  That is
     the documented behaviour, and it is why check_gte56.py
     checks A2 (columns nonzero) and A3 (columns distinct)
     before it reports anything.

  Now the same matrix with its 1 zero column(s) dropped -- an
  input no target uses cannot change the optimum, so the known
  optimum 10 still applies, and now the machinery must be sound:

  [reduced, 7 columns] admissible keep-sets : 58

    level  bound    optimum  slack    verdict
    m=0    10       10       0        sound
    m=1    10       10       0        sound
    m=2    10       10       0        sound

    |K| capped at  best m=1 optimum  verdict
    3              9        10       sound
    4              9        10       sound
    5              9        10       sound
    6              10       10       sound
    7              10       10       sound

  searcher work for this instance: 2.9e+06 nodes, 0.3 s

==========================================================================
RESULT: PASS on 3 instance(s).
  * The searcher independently reproduced every SAT-proved optimum exactly.
  * No Theorem-N bound exceeded a known optimum on any instance whose
    preconditions hold, at any covering level or keep-set size.
  * The precondition negative control overclaimed exactly as documented
    when its gate was ignored, and became sound once reduced.
```

| | |
|---|---|
| **measured wall time (re-run 2026-09-01, twice)** | **170.5 s** and **156.2 s**, one core, `nice -n 19`; identical verdicts and identical node counts both times |
| where the time goes | essentially all of it is `L1_clean_iso`, whose full-instance `minE = 8` needs a depth-7 exhaustion (2.7e9 nodes): 170.1 s / 155.2 s on the two runs. The other two instances together take 0.4 s. |
| historical cost of the reference optima | `L1_clean_iso` **4,511 s** of SAT (4,236 s of it in the single `k = 11` UNSAT call), plus a 72,000 s hardening run with all symmetry-breaking clauses stripped; `L5_tap_pairQ3` minutes; `tap_P__Q1_2_4_a` 42.45 s |

To run one instance only:

```
python3 validation/run_validation.py --instance L5_tap_pairQ3
```

That takes **0.2 s** and exercises every code path except the deep exhaustion.

## Reading the exit status

Exit 0 means: every bound was `<=` the known optimum on every instance whose
preconditions hold; the searcher agreed with every SAT optimum; and the negative
control overclaimed exactly as documented when its gate was ignored, then became
sound once reduced. Anything else is a real failure and the pack should not be
believed until it is explained.
