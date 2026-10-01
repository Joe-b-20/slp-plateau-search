# `bounds/cf_gte96/` — how to run it

Typed from the **pack root** (`bounds/`). Python 3 standard library only. No solver, no
compiler, no network. Times measured 2026-09-26 on one core.

## Files

| file | what it is |
|---|---|
| `STATEMENT.md` | the claim, the technique, both derivations, where the line stops, controls |
| `HOW.md` | what is new relative to `../cf_gte92/`: the split-keyed price and the checks |
| `cert_cf96_split.json` | the split-price certificate, `B = 95.8521517` |
| `cert_cf96_split_referee.json` | the referee's independently derived table, `B = 95.8521565` |
| `cert_cf92_sharper_as_split.json` | **control**: the old mask-only table `../cf_gte92/cert_cf92_sharper.json` embedded in the split family; must give the old constant |
| `check_split_cert.py` | the certificate checker |
| `check_split_cert_independent.py` | the referee's checker, written from the statement without sight of the other; brute-forces every hierarchy as well |

The upper-bound witness (102 gates) and its replay checker stay in `../cf_gte92/`.

---

## 1. `L_cf(M) >= 96` — the certificate

```
python3 cf_gte96/check_split_cert.py --aes-crosscheck
```

Expected output, verbatim:

```
matrix       : matrix.txt
  sha256     : 9c337107cba5b0b434fc580ccb1d0323ac51ce17a5fe99da91b97aa8fbc7b620
  shape      : 32 rows x 32 columns, total row weight 184
certificate  : cf_gte96/cert_cf96_split.json
  denominator: 10000000, 32 price tables

  [PASS] CHECK A  matrix is AES MixColumns (GF(2^8) rebuild)     row-for-row identical
  [PASS] CHECK T  one price table per target                     32 tables, 32 targets
  [PASS] CHECK 0  keys well formed, prices non-negative integers 13293 priced (target,mask,split) triples, 0 bad
  [PASS] CHECK 1  column constraint  sum_t n[t][(S,A)] <= D      max column sum = 9999999 / 10000000 = 0.9999999  over 12840 distinct (mask,split) columns
  [PASS] CHECK 2  hierarchy DPs evaluated                        numerator = 958521517,  B = 958521517/10000000 = 95.8521517
  [PASS] CHECK 3  computed bound matches the stated bound        computed ceil(B) = 96, certificate states 96

==========================================================================
RESULT: certificate VALID.
  B = 958521517/10000000 = 95.8521517
  => L_cf(M) >= 96
  => every cancellation-free XOR-SLP for this matrix has >= 96 gates;
     equivalently, every SLP with <= 95 gates contains a cancelling gate.
```

| | |
|---|---|
| **measured wall time** | **0.04 s** |
| historical cost to *generate* the table | one exact LP over 13,293 variables and 12,840 constraints, then exactification to integers over `10^7` |

## 2. `L_cf(M) >= 96` — the second, independent derivation

```
python3 cf_gte96/check_split_cert.py --cert cf_gte96/cert_cf96_split_referee.json
```

Expected output (differing lines only):

```
  [PASS] CHECK 0  keys well formed, prices non-negative integers 13298 priced (target,mask,split) triples, 0 bad
  [PASS] CHECK 1  column constraint  sum_t n[t][(S,A)] <= D      max column sum = 10000000 / 10000000 = 1.0000000  over 12840 distinct (mask,split) columns
  [PASS] CHECK 2  hierarchy DPs evaluated                        numerator = 958521565,  B = 958521565/10000000 = 95.8521565
  [PASS] CHECK 3  computed bound matches the stated bound        computed ceil(B) = 96, certificate states 96
...
  => L_cf(M) >= 96
```

**Measured wall time: 0.04 s.** Same integer conclusion, produced by the referee from the
statement alone, through its own LP.

## 3. Control — the old table must give the old constant

```
python3 cf_gte96/check_split_cert.py --cert cf_gte96/cert_cf92_sharper_as_split.json
```

Expected output (differing lines only):

```
  [PASS] CHECK 0  keys well formed, prices non-negative integers 13366 priced (target,mask,split) triples, 0 bad
  [PASS] CHECK 2  hierarchy DPs evaluated                        numerator = 914098776,  B = 914098776/10000000 = 91.4098776
  [PASS] CHECK 3  computed bound matches the stated bound        computed ceil(B) = 92, certificate states 92
...
  => L_cf(M) >= 92
```

**Measured wall time: 0.04 s.** `91.4098776` is exactly the constant `../cf_gte92/RUN.md`
reports for the same table, so the split family contains the old one and the checker prices
it identically.

## 4. The independent checker

```
python3 cf_gte96/check_split_cert_independent.py --matrix matrix.txt --cert cf_gte96/cert_cf96_split.json --claim 96 --aes-crosscheck
```

Expected output, verbatim:

```
matrix : matrix.txt  (32 rows x 32 columns, row weights [5, 7])
  [PASS] A  matrix equals FIPS-197 MixColumns rebuilt here, row for row
  [PASS] K  13293 priced entries parsed strictly; bad syntax 0, bad value 0, malformed key 0, duplicate JSON keys 0
  [INFO] K  keys spelt with A NOT holding lowbit(S): 0 (normalised); two spellings of one split inside one table: 0; zero prices: 0
  [PASS] C  (C') 12840 distinct (S,split) columns, 409 priced by >= 2 rows; max column sum 9999999 / D=10000000; columns over D: 0; tight columns: 0
  [PASS] D  per-row minima: DP over all submasks == brute force over all 126840 hierarchies; argmin hierarchies re-validated and re-priced
  [INFO] B  numerator 958521517, D 10000000, B = 958521517/10000000 = 95.8521517, ceil(B) = 96
  [PASS] B  ceil(B) = 96  >= claim 96
RESULT: certificate VALID  (B = 95.8521517, ceil = 96)
```

| | |
|---|---|
| **measured wall time** | **0.38 s** (brute force over all 126,840 hierarchies included); `--no-bruteforce --quiet`: 0.05 s |

## 5. Negative control — a broken certificate must be rejected

Add the denominator to any one price (so one column exceeds `D`) and re-run the checker: it
prints `[FAIL] CHECK 1` and `RESULT: certificate INVALID`, exit code 1. Measured 2026-09-26.
