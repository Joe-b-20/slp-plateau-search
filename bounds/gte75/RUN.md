# `bounds/gte75/` — how to run it

Typed from this directory (`bounds/gte75/`). Python 3 standard library only, except `checks/lp_regen.py`
(numpy + scipy; optional). No solver is needed to check anything; solvers were used only to find the
certificates. Times measured 2026-10-01 on one core.

## Files

| file | what it is |
|---|---|
| `STATEMENT.md`, `HOW.md` | the claim and status; the map of the argument |
| `PROOF_NOTE_75.md`, `.pdf` | the standalone proof note (identical to the records repository's copy, tag v4.0.0) |
| `checks/finite_facts.py` | recomputes every finite fact F1-F14 of the note from the GF(2^8) definition of MixColumns |
| `checks/check72.py`, `check73.py` | the enumerations of Propositions 8.4 and 9.2 (69-72 gates) |
| `checks/check_dark_source.py` (+ `check73_drift.py`, `check_short_boundary.py`, `short_code.json`) | the weight <= 12 zero-sum subsets behind fact F13 |
| `checks/certify74.py` + `CERTIFICATES74.json`, `checks/independent74.py` | 73 gates: 262 profiles, 524 claims, 484 exact certificates; two implementations |
| `checks/certify75.py` + `CERTIFICATES75.json`, `checks/independent75.py` | 74 gates: 1,102 profiles, 2,204 claims, 4,057 exact certificates; two implementations |
| `checks/stress.py`, `checks/lp_regen.py` | optional cross-checks: every identity and row on the shipped circuits; an LP that regenerates all 2,204 claims |
| `checks/run_all.sh`, `checks/EXPECTED_RESULTS.md` | runs everything and prints the last lines; the recorded transcript |
| `bound_76/README.md` | the facts about the certified, less reviewed extension to 76 |

## 1. Everything at once (about 2 minutes)

```
sh checks/run_all.sh
```

Expected: `finite_facts.py` ends with `ALL FINITE PREMISES RECOMPUTED AND MATCH`; the four certificate checkers
and `check_dark_source.py` end with `"all_checks_passed": true`; `stress.py` reports `"failures": []`;
`lp_regen.py` reports `survivors 0` and `claims identical 2204`. The full transcript is
`checks/EXPECTED_RESULTS.md`.

## 2. One by one

| command | the line that matters | time |
|---|---|---|
| `python3 checks/finite_facts.py` | `ALL FINITE PREMISES RECOMPUTED AND MATCH` | 35 s |
| `python3 checks/check72.py` | `"minimum_two_step_increment": 3` (and positive increments at 69, 70) | < 1 s |
| `python3 checks/check73.py` | the unique zero-drift tuple a = b = 24, Y = Z = 0; `"rank": 28` | < 1 s |
| `python3 checks/check_dark_source.py` | `"rank_R10": 29`, `"complete_nonzero_quotient_word_count": 736`, `"all_checks_passed": true` | 10 s |
| `python3 checks/certify74.py` / `independent74.py` | `"all_checks_passed": true`, 484 certificates, largest right side -1 | 3 s each |
| `python3 checks/certify75.py` / `independent75.py` | `"all_checks_passed": true`, 4,057 certificates, 9,604 references, 927 direct, largest right side -1 | 30 s / 10 s |
| `python3 checks/stress.py` | `"failures": []` on the circuits in `evidence/circuits/` | 2 s |
| `python3 checks/lp_regen.py` | `survivors 0`, `claims identical 2204` | 20 s (numpy, scipy) |
| `python3 ../../verify_circuit.py ../../evidence/circuits/mixcolumns_88gates_depth5_fromscratch.json` | `VERDICT: VALID MixColumns circuit` (the upper bound) | < 1 s |

The note's section 14 lists the same commands in the records repository's layout (`lower_bounds/checks/`).

## 3. What a failure would mean

A failed assertion in `finite_facts.py` means a finite fact of the note is wrong as stated. A rejected
certificate or an uncovered case in the certificate checkers means the computation does not prove what section
11 says. A nonempty `"failures"` list in `stress.py` means a real circuit violates an inequality the note claims
is necessary, which would refute the argument. None of these has happened.
