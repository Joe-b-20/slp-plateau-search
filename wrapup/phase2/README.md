# phase2 — the verified starting kit for AES InvMixColumns

Built 2026-08-29 (day-2 session, task T1e). Everything here is derived from
FIPS-197 and GF(2⁸) or ported from a named file in this repo; every claim has a
banked control transcript under `controls/`.

This directory is meant to be **copied out** as the seed of the next repo.

## Layout

```
spec/    derive_invmc.py      the derivation (run it; it re-emits everything)
         sector_probe.py      the fleet8 algebraic frame, measured on the inverse
         invmc_matrix.json            32x32 GF(2) matrix + provenance header
         invmc_target_masks.json      the 32 masks, corpus mask convention
         mixcolumns_matrix.json       the forward control, same format
         mixcolumns_target_masks.json
         derivation_transcript.txt
tools/   verify_slp_generic.py  the oracle, arbitrary target matrix
         tripwire_B.py          the B = n - q one-gate-improvement detector
         baseline_naive.py      naive XOR tree + Paar1 greedy, day-0 numbers
circuits/  invmc_paar1.json                164 gates @ depth 9   (VALID)
           invmc_from_mc_cubed_264.json    264 gates @ depth 15  (VALID)
           mixcolumns_paar1.json           108 gates @ depth 5   (VALID)
controls/  every transcript; run_all.sh reproduces the lot
PORT_NOTES.md   what must be RE-DERIVED for the fleet8 generator chain
```

## The convention (read this before touching a mask)

Taken from `verify_circuit.py:37-55`, not from memory:

```
out row index = 8*out_byte + out_bit      in col index = 8*in_byte + in_bit
bit i of a byte is the coefficient of x^i           -> LSB-FIRST in the byte
mask(r) = OR_c M[r][c] << c                         -> bit c = input index c
out_byte[col] = XOR_k coef[k] * in_byte[(col+k) % 4]
```

## Quick start

```bash
python3 spec/derive_invmc.py                       # re-derive + all 4 controls
python3 tools/verify_slp_generic.py --target spec/invmc_matrix.json C.json [depth]
python3 tools/tripwire_B.py --target spec/invmc_matrix.json --calibrate BASE.json C.json
python3 tools/baseline_naive.py --target spec/invmc_matrix.json --emit out.json
bash controls/run_all.sh                           # everything, from scratch
```

## Numbers, as of the build

| | forward `[2,3,1,1]` | inverse `[14,11,13,9]` |
|---|---|---|
| matrix density | 184 | 472 |
| naive XOR tree | 152 | 440 |
| Paar1 greedy | 108 @ d5 | 164 @ d9 |
| via `M_inv = M³` | — | 264 @ d15 |
| project record | 88 @ d5 (B = 56) | — |

See `PORT_NOTES.md` §7 for what these mean and §3 for the one piece of the
generator chain that is real work.
