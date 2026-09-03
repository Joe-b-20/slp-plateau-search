# `bounds/depth3_gte81/` — how to run it

Typed from the **pack root** (`bounds/`).

**The `--check` path is Python 3 standard library only.** `numpy` and `scipy`
are imported lazily and are needed only to *generate* a new certificate, never
to verify one. That separation is deliberate: checking the proof must not
depend on a solver stack.

## Files

| file | what it is |
|---|---|
| `STATEMENT.md` | the claims, the technique, the two controls, the honest split |
| `cert_depth3.json` | the exact rational dual certificate (23,450 nonzero duals) |
| `certify.py` | the checker (`--check`) and the generator (needs numpy/scipy) |
| `mcmatrix.py` | the only place the matrix enters; reads `../matrix.txt` |
| `model3.py`, `cuts.py`, `build_lp.py` | the complete depth-3 model and its valid inequalities |
| `control_primal.py`, `control_cuts.py`, `control_lp.py` | the three mandatory soundness controls |
| `mixcolumns_97gates_depth3.json` | the verified 97-gate depth-3 circuit the controls use |
| `mip3.py`, `mip3_result_L1.json`, `mip3_L1_run.log` | the `>= 81` MIP run, its result and its solver log |

---

## 1. `N_depth3 >= 80` — the certificate (THIS IS THE CHECKABLE ONE)

```
python3 depth3_gte81/certify.py --check depth3_gte81/cert_depth3.json
```

Expected output, verbatim:

```
rows 72830  vars 29180  nonzero duals 23450
exact dual value = 47597998171620/1000000000000 = 47.597998
=> |L1|+|L2| >= 48  =>  N_depth3 >= 80
```

| | |
|---|---|
| **measured wall time (re-run 2026-09-01)** | **0.29 s** |
| same check against the original in-repo copy, same day | 2.21 s (the difference is a `numpy` import this port no longer performs; the numbers are identical) |
| historical cost to *generate* the certificate | minutes (an LP solve with a slack margin, then exact integer re-verification) |

Every digit above is integer arithmetic. `47597998171620/10^12` is the exact
value of `u·b`; `ceil` of it is 48; `32 + 48 = 80`.

## 2. The three mandatory controls

A bound from a model is vacuous if the model is unsound, so run these.

```
python3 depth3_gte81/control_primal.py
python3 depth3_gte81/control_cuts.py
python3 depth3_gte81/control_lp.py
```

Expected output, verbatim:

```
gates 97  depth 3
 level 1 : 27 gates, weights [2]
 level 2 : 38 gates, weights [3, 4]
 level 3 : 32 gates, weights [5, 7]
 level-3 masks == targets: True 32
 level-1 masks outside edge candidate set: 0
 level-2 masks outside L2 candidate set  : 0
 model objective realised (|L1|+|L2|) = 65  -> total 97
 CONTROL PASS
```
```
 C1/C2 building          22564 cuts, 0 violated
 C3 target-L2               32 cuts, 0 violated
 C4/C5 w7 matching         768 cuts, 0 violated
 C6 w5 edges                40 cuts, 0 violated
 C7 aggregate                1 cuts, 0 violated
 CONTROL PASS
```
```
rows 72830  vars 29180
row tags: {'cover': 32, 'zparent': 12140, 'build3': 3008, 'wbuild': 4889, 'wedge': 29334, 'C1': 22564, 'C3': 32, 'C4C5': 768, 'C6': 40, 'C7': 1, 'C7b': 2, 'C8': 20}
control objective |L1|+|L2| = 65  (total 97 gates)
violated rows: NONE
CONTROL PASS
```

| | |
|---|---|
| **measured wall times (re-run 2026-09-01)** | `control_primal` **0.05 s**, `control_cuts` **0.12 s**, `control_lp` **0.31 s** |
| historical cost | the same, seconds; these were always cheap and were always mandatory |

Note that the certified dual value 47.598 is comfortably below the control's
realised objective 65 — as it must be, since 65 is achieved by a real circuit.

## 3. `N_depth3 >= 81` — the solver run (NOT a certificate)

The artifacts are shipped and readable; the run is **not** re-run here.

```
cat depth3_gte81/mip3_result_L1.json
cat depth3_gte81/mip3_L1_run.log
```

`mip3_result_L1.json`:

```json
{
 "model": "depth3_strong_highs_mip",
 "level": 1,
 "status": 1,
 "message": "Time limit reached. (HiGHS Status 13: Time limit reached)",
 "wall_monotonic": 1369.951837534958,
 "primal": 148.0,
 "mip_dual_bound": 49.0,
 "mip_gap": 0.668918918918919,
 "N_depth3_lower_bound": 81
}
```

The load-bearing lines of `mip3_L1_run.log`:

```
MIP: 72830 rows x 29180 cols, nnz 259914, level 1 (uncapped)
Running HiGHS 1.2.0 [date: 2021-07-09, git hash: n/a]
...
         0       0         0   0.00%   47.59824561     148               67.84%        0      0      0     14874   135.6s
         0       0         0   0.00%   48.85118809     148               66.99%     2291     24     77     20574 25075.1s
         0       0         0   0.00%   48.85118809     148               66.99%     2298     27     77     20574 60391.9s
Solving report
  Status            Time limit reached
  Dual bound        49
  Timing            60391.94 (total)
  Gap               66.89%
```

**Two gap figures appear in that log and both are real.** The branch-and-cut
progress rows print `66.99%`, computed against the last *displayed* bound
`48.85118809`; the solving report's own final `Gap` is **66.89 %**, computed
against the reported dual bound `49` — `(148 − 49) / 148 = 66.89 %`, which is
also the `mip_gap: 0.668918918918919` recorded in `mip3_result_L1.json`.
**66.89 % is the run's terminal gap** and is the figure quoted everywhere in
this repository.

To reproduce it (needs `highspy`; expect hours, single-threaded, and set your
own time limit):

```
python3 depth3_gte81/mip3.py
```

| | |
|---|---|
| **measured wall time** | **not re-run.** The historical run took 60,391.94 s (≈16.8 h) and still hit its time limit, so re-running it inside a session was not possible and would not have added information. |
| historical cost | 60,391.94 s of HiGHS time, single-threaded, `nice -n 19`, terminated by its own time limit with a **66.89 %** gap remaining |

**Two things to read carefully in that run.**

1. **It never closed.** Status is *Time limit reached*, terminal gap 66.89 %. The `81` is
   HiGHS's **dual bound** (49), which is a valid lower bound at any point during
   branch-and-cut — that part is sound — but the run proves nothing more than 81
   and did not converge. The primal value 148 is just an incumbent, not the
   optimum, and must not be quoted as one.
2. **The result file's own timing field is inconsistent with its log.**
   `wall_monotonic` reads 1369.95 s while HiGHS reports `Timing 60391.94 (total)`
   and the process ran from 11:35 to 04:22. Trust the solver log; the JSON field
   is wrong. It is left in the file unmodified rather than silently patched.

The first LP row of that log, `47.59824561`, is the same LP value the
certificate in §1 pins exactly — an independent confirmation, through HiGHS's
own code path, that the certified 47.597998 is the root relaxation.
