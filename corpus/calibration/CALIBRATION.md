# The clean-room calibration: 93 gates from nothing

## The experiment

One capable agent was given a specification directory containing **two files,
8 KB total**: the 32 MixColumns target masks, and a verifier. Nothing else. No
seed circuit, no record data, no gate menus, no block decomposition, no import
of any of the project's search code. It was asked to build a MixColumns XOR
circuit from first principles against that spec.

It wrote its own randomised Boyar–Peralta implementation in C — its own hash
sets, its own RNG, no library beyond libc — across five generations, then a SAT
window-repair loop and an island portfolio with migration.

**It reached 93 gates, depth 7, valid, in about 7.5 hours of wall time on one
day.**

## RE-RUN — verify it

```
$ nice -n 19 python3 verify_circuit.py cleanroom_93gates.json
gates=93 depth=7 outputs_built=32/32 problems=0
VERDICT: VALID MixColumns circuit
  exit status: 0
```

**Measured 2026-09-01: 0.05 s wall.** The file's md5 is
`6bb8a324ed9ab61eb6e094d94e4324bf`, matching the value recorded when the lane
was written up. Transcript: `out/VERIFY.txt`.

## What it means

This project's record is **88**. A from-scratch effort with no project
knowledge lands at **93**.

That gap — **five gates** — is the measured value of everything the project
accumulated: the block decomposition, the currency menus, the SAT ladders, the
symmetry normalisation, the plateau census, the seed lineages, every campaign in
the tree. It is not an estimate. It is one clean-room run against one record.

Placed against the published literature, the calibration reads:

| circuit | gates | depth |
|---|---:|---:|
| **clean-room, one day, no project knowledge** | **93** | 7 |
| published (Osvik–Canright) | 94 | 5 |
| published (Sun–Yang–Li) | 89 | — |
| the record | 88 | 7 |

A day of competent from-scratch work gets you to roughly the state of the
published art. It does not get you near 88. **That is the finding.**

Two supporting numbers make the shape clearer:

* **One worker, unaided, ~2 minutes: 95–101 gates.** Eight independent workers
  landed at 99, 95, 101, 98, 96, 101, 99, 95. The first 90 % of the descent is
  cheap; the last few gates are not.
* **93 is where the lane stopped, and it stopped against a wall, not a clock.**
  The SAT repair loop made **2,623 window attempts, 1,924 of them gate-saving
  asks, and got exactly one hit** — a single 57.7-second solve that took 94 to
  93. The descent from 93 was then attempted roughly 2,200 more times and never
  once succeeded. Measured solver time: **19.54 hours**. The lane also produced
  32 distinct circuits at 94 against 5 at 93, a shape consistent with 93 being
  a genuine local wall for the method.

## Caveats, stated plainly

* **n = 1.** One clean-room run, one agent, one day. One data point is one data
  point. The useful experiment for sharpening this is a second clean-room run by
  a different agent.
* **The write-up is post-hoc.** The lane shipped with no plan, no ledger and no
  commissioning note. Its record was reconstructed afterwards entirely from
  on-disk evidence. Nothing was witnessed.
* **"No project knowledge" is inferred, not documented.** The evidence is
  circumstantial but machine-checked: the spec directory's contents, the
  verified absence of seeds or menus, and the fact that no file in the lane
  reads anything outside its own directory. That is strong evidence of the
  *condition*; it is not documentation of the *intent*.
* **The verifier in the spec was a copy** of the project's own verifier, byte
  for byte. It is a copy for self-containment, not a second independent oracle.
  No claim of "two independent checks" would be true of this lane.
* **CPU cost is only partly grounded.** Solver time is measured at 19.54 h. The
  Boyar–Peralta side was never instrumented, and the 7.5-hour figure is a *wall*
  span across an unknown number of concurrent workers, not a CPU total. No
  core-hour figure for the lane as a whole is defensible.
* **The lane's product is a number, not a circuit.** 93 at depth 7 dominates
  nothing: the published 94 is at depth 5. No 88, no 87, and nothing here bears
  on either.

## Files

| path | what it is |
|---|---|
| `cleanroom_93gates.json` | the circuit, as index pairs; 93 gates, depth 7 |
| `verify_circuit.py` | independent MixColumns verifier, rebuilt from GF(2^8) |
| `out/VERIFY.txt` | transcript of the 2026-09-01 verification |
