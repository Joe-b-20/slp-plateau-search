# RUN — verify the record circuits

The trivial, load-bearing row. Every other result in this pack is a statement
*about* circuits; this is the check that the circuits are what they claim to be.
It takes twenty seconds and it is the first thing a sceptical reader should run.

The record circuits and their verifier live in the public records repository,
not in this pack — this page records the command and its real output.

---

## RE-RUN

```
$ nice -n 19 python3 verify_all.py
```

**Measured 2026-09-01: 20.6 s wall.** Exit 0. The working tree was clean before
and after — verification writes nothing.

```
AES MixColumns rebuilt from GF(2^8): weight profile 20x5 + 12x7  [OK]

[ OK ] mixcolumns_88gates_depth5: 88 gates, depth 5 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_88gates_depth5_fromscratch: 88 gates, depth 5 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_88gates_depth6: 88 gates, depth 6 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_88gates_depth7: 88 gates, depth 7 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_88gates_depth8: 88 gates, depth 8 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_89gates_depth10: 89 gates, depth 10 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_89gates_depth5: 89 gates, depth 5 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_91gates_depth6: 91 gates, depth 6 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_92gates_depth4: 92 gates, depth 4 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_97gates_depth3: 97 gates, depth 3 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_98gates_depth3: 98 gates, depth 3 — all 32 outputs correct, SHA fields match

ALL CIRCUITS VERIFIED.
Clean-room mathematical verification summary
Support histogram: {"5": 20, "7": 12}
- mixcolumns_88gates_depth5: gates=88, depth=5, issues=0
- mixcolumns_88gates_depth5_fromscratch: gates=88, depth=5, issues=0
- mixcolumns_88gates_depth6: gates=88, depth=6, issues=0
- mixcolumns_88gates_depth7: gates=88, depth=7, issues=0
- mixcolumns_88gates_depth8: gates=88, depth=8, issues=0
- mixcolumns_89gates_depth10: gates=89, depth=10, issues=0
- mixcolumns_89gates_depth5: gates=89, depth=5, issues=0
- mixcolumns_91gates_depth6: gates=91, depth=6, issues=0
- mixcolumns_92gates_depth4: gates=92, depth=4, issues=0
- mixcolumns_97gates_depth3: gates=97, depth=3, issues=0
- mixcolumns_98gates_depth3: gates=98, depth=3, issues=0
Adversarial tests passed: 14 of 14
Artifact mode: compare only, nothing written
- audit/recomputed_metrics.json: MATCH (generated_utc and tool_availability excluded as run/environment dependent)
- audit/MATHEMATICAL_VERIFICATION.md: MATCH (Tool availability section excluded as environment dependent)
Warnings: 0
Overall result: PASS

All requested verification paths passed.
```

**PASS condition:** all 11 circuits `[ OK ]`, `ALL CIRCUITS VERIFIED`,
`Adversarial tests passed: 14 of 14`, `Overall result: PASS`, exit 0.

---

## What it actually checks

`verify_all.py` runs two independent entry points:

1. **`verify.py`** — rebuilds AES MixColumns from GF(2^8) arithmetic mod
   `0x11B` (the specification *is* that code, not a table copied from
   somewhere), then replays each circuit gate by gate and compares all 32
   output bits. It also re-derives the target weight profile and asserts it is
   20 masks of Hamming weight 5 and 12 of weight 7 — a self-check on the
   spec itself, so a corrupted spec fails loudly rather than silently
   validating the wrong function.

2. **`audit/cleanroom_verify.py`** — an independent recomputation of every
   published metric, compared against the tracked audit artifacts, plus 14
   adversarial tests. It runs in **compare-only mode: it writes nothing**, so
   verifying never dirties the working tree. Fields that legitimately vary by
   run or environment (timestamps, tool availability) are excluded from the
   comparison; everything else must MATCH.

Optionally, `--with-verilog` also runs the Verilog netlists through Icarus.

## Why this row matters

Every circuit used anywhere in this pack is on that list or verified alongside
it:

* the **five published 88s** are the negative control for the tripwire
  (`../tripwire_demo/`) and five of the 520 rows of the corpus sample
  (`../sample/`);
* the **97 and the 92** are among the seven circuits in the control audit
  (`../calibration/CONTROL_AUDIT.md`) that the exact decider calls
  "irreducible" while a verified 88 sits below them;
* the **89 at depth 10** is the same gate count as the out-of-vocabulary
  circuit in `../vocabulary/`, which is verified separately by the same
  verifier code.

If this command fails, nothing else in the pack means anything. It has not
failed.
