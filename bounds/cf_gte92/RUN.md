# `bounds/cf_gte92/` — how to run it

Typed from the **pack root** (`bounds/`). Python 3 standard library only. No
solver, no compiler, no network.

## Files

| file | what it is |
|---|---|
| `STATEMENT.md` | the claim, the technique, both derivations, and where the line stops |
| `HOW.md` | the mechanism: what a price table is, what each check asserts, what it costs |
| `cert_cf92.json` | the published price certificate, `B = 91.0019782` |
| `cert_cf92_sharper.json` | the independently derived, stronger table, `B = 91.4098776` |
| `check_cf_cert.py` | the certificate checker |
| `cf_102gates_depth5.json` | the 102-gate cancellation-free witness |
| `check_cancellation_free.py` | replays a circuit and computes gates / targets / `kappa` / depth |

---

## 1. `L_cf(M) >= 92` — the published certificate

```
python3 cf_gte92/check_cf_cert.py --aes-crosscheck
```

Expected output, verbatim:

```
matrix       : matrix.txt
  sha256     : 9c337107cba5b0b434fc580ccb1d0323ac51ce17a5fe99da91b97aa8fbc7b620
  shape      : 32 rows x 32 columns, total row weight 184
certificate  : cf_gte92/cert_cf92.json
  denominator: 10000000, 32 price tables

  [PASS] CHECK A  matrix is AES MixColumns (GF(2^8) rebuild) row-for-row identical
  [PASS] CHECK T  one price table per target                32 tables, 32 targets
  [PASS] CHECK 0  prices non-negative, inside their target support 1960 priced (target,mask) pairs, 0 bad
  [PASS] CHECK 1  column constraint  sum_t n[t][m] <= D     max column sum = 10000000 / 10000000 = 1.0000000  over 1648 distinct masks
  [PASS] CHECK 2  hierarchy DPs evaluated                   numerator = 910019782,  B = 910019782/10000000 = 91.0019782
  [PASS] CHECK 3  computed bound matches the stated bound   computed ceil(B) = 92, certificate states 92

==========================================================================
RESULT: certificate VALID.
  B = 910019782/10000000 = 91.0019782
  => L_cf(M) >= 92
  => every cancellation-free XOR-SLP for this matrix has >= 92 gates;
     equivalently, every SLP with <= 91 gates contains a cancelling gate.
```

| | |
|---|---|
| **measured wall time (re-run 2026-09-01)** | **0.03 s** |
| same check against the original in-repo verifier, same day | 0.06 s, identical numbers (`CHECK 1 ok`, `numerator = 910019782  B = 91.0019782`, `=> L_cfree(M) >= 92`) |
| historical cost to *generate* the table | ~25 minutes of projected subgradient ascent |
| historically quoted check cost | "~2 s, stdlib only, solver-free" — conservative; it is well under a tenth of that |

`--aes-crosscheck` adds `CHECK A`: the script rebuilds MixColumns from
GF(2^8)/0x11B out of the spec and confirms `../matrix.txt` is that map, row for
row. Drop the flag and the checker is matrix-agnostic.

## 2. `L_cf(M) >= 92` — the second, independent derivation

```
python3 cf_gte92/check_cf_cert.py --cert cf_gte92/cert_cf92_sharper.json
```

Expected output (differing lines only):

```
  [PASS] CHECK 0  prices non-negative, inside their target support 1934 priced (target,mask) pairs, 0 bad
  [PASS] CHECK 1  column constraint  sum_t n[t][m] <= D     max column sum = 10000000 / 10000000 = 1.0000000  over 1648 distinct masks
  [PASS] CHECK 2  hierarchy DPs evaluated                   numerator = 914098776,  B = 914098776/10000000 = 91.4098776
  [PASS] CHECK 3  computed bound matches the stated bound   computed ceil(B) = 92, certificate states 92
...
  B = 914098776/10000000 = 91.4098776
  => L_cf(M) >= 92
```

| | |
|---|---|
| **measured wall time (re-run 2026-09-01)** | **0.03 s** |
| historical cost to *generate* the table | 60–120 s per multiplier value on 8 threads, 19 values, plus exactification |

Same integer conclusion, better constant, produced by a different lane through
a different route. `91.4098776` is close to the ceiling of the whole price family
(`B* = 91.409884`) — see [`STATEMENT.md`](STATEMENT.md).

## 3. `L_cf(M) <= 102` — the witness, and the cancellation-freeness check

```
python3 cf_gte92/check_cancellation_free.py cf_gte92/cf_102gates_depth5.json --require-cancellation-free
```

Expected output, verbatim:

```
circuit          : cf_gte92/cf_102gates_depth5.json
matrix           : matrix.txt  (32 rows x 32 columns)

  gates          : 102   (file states gateCount = 102, MATCHES)
  targets built  : 32 of 32
  kappa          : 0   (gates whose two operand masks overlap)
  depth          : 5   (computed from the gate list, not asserted)

==========================================================================
RESULT: VALID and CANCELLATION-FREE.
  All 32 rows are built and no gate cancels, so this circuit is a
  witness for  L_cf(M) <= 102.
```

| | |
|---|---|
| **measured wall time (re-run 2026-09-01)** | **0.02 s** |
| historical cost | the circuit was found by search; replaying and re-verifying it has always been instantaneous, and it was independently replayed from raw JSON on 2026-08-29 with the same four figures |

### The negative control — run this too

The checker is only informative if it can return a negative verdict. Point it at
the 88-gate record (in the records repository,
`circuits/mixcolumns_88gates_depth5.json`):

```
python3 cf_gte92/check_cancellation_free.py PATH/TO/mixcolumns_88gates_depth5.json
```

Measured here, 2026-09-01:

```
  gates          : 88   (file states gateCount = 88, MATCHES)
  targets built  : 32 of 32
  kappa          : 22   (gates whose two operand masks overlap)
  depth          : 5   (computed from the gate list, not asserted)
  cancelling at  : gate indices [44, 49, 50, 51, 52, 53, 58, 63, 64, 69] ...

RESULT: VALID, but NOT cancellation-free (kappa = 22).
  It witnesses L(M) <= 88; it says nothing about L_cf(M).
```

The 88-gate circuit is 4 gates below the cancellation-free floor of 92, and it
cancels 22 times.
The record circuit is not duplicated here — it lives in the records repository
under a stable name.
