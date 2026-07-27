# Imported prior-art circuits — NOT this project's results

These two circuits were **published by other people**. They are archived here
because campaign 87 used them (as search seeds, as certificate subjects, and as
the comparison baseline), and because several of this project's own results must
be described relative to them. They are always to be credited to their authors.

| file | gates @ depth | author / source | how it got here |
|---|---|---|---|
| `jean_88gates_depth7_eprint_2026-1481.json` | **88 @ 7\*** | **Jean, ePrint 2026/1481**, Algorithm 1 (88-XOR AES MixColumns), posted 2026-07-23 | transcribed from the paper, input bits relabelled to this repo's convention, then oracle-verified; \*the paper states no depth — depth 7 is what this repo's oracle measures for the transcribed circuit, exactly as for the 89 below |
| `sunyangli_89gates_eprint_2025-1493.json` | **89 @ 9** | **Sun–Yang–Li, ePrint 2025/1493**, Table 4 (89 g-XOR AES MixColumns), 2025-08 | same route; the paper states no depth — depth 9 is what this repo's oracle measures for the transcribed circuit |

Both files keep their original `provenance` / `source` /
`input_permutation_paper_to_repo` fields exactly as written at import time.
Neither is the product of any search in this repository.

## Verification (this repo's standalone oracle)

```
python3 ../../verify_circuit.py jean_88gates_depth7_eprint_2026-1481.json 7
    gates=88 depth=7 outputs_built=32/32 problems=0 ; depth<= 7: OK ; VERDICT: VALID MixColumns circuit

python3 ../../verify_circuit.py sunyangli_89gates_eprint_2025-1493.json
    gates=89 depth=9 outputs_built=32/32 problems=0 ; VERDICT: VALID MixColumns circuit
```

Jean's paper credits the discovery to a search run "with the help of OpenAI
codex" and gives no method and no depth claim; the depth 7 above is this repo's
measurement. Sun–Yang–Li describe their method (LCB-BP voting variant + MILP +
graph-based local optimisation replacing out-degree-1 subsequences).

## How they relate to this project's circuits

Mask overlap (mask set = the circuit's non-input signal values), measured with
this repo's oracle:

| pair | shared masks | Jaccard |
|---|---|---|
| **Jean 88 ↔ Sun–Yang–Li 89** *(baseline: two independent published works)* | **63** | **0.553** |
| Jean 88 ↔ **our 88@7** | 61 / 88 | 0.530 |
| Jean 88 ↔ **our 88@8 (third family)** | 55 | 0.455 |
| Jean 88 ↔ our 89@5 record | 61 | 0.526 |
| Sun–Yang–Li 89 ↔ our 89@5 record | 59 | 0.496 |
| Sun–Yang–Li 89 ↔ our 88@7 | 61 | 0.526 |
| our 88@7 ↔ our 88@8 | 62 | 0.544 |

**Read the first row before judging the second.** Jean and Sun–Yang–Li are two
indisputably independent published works — different authors, different
methods, a year apart, neither derived from the other — and they share **63**
masks (J = 0.553), *more* than our 88@7 shares with Jean's (61, J = 0.530). A
~60-mask overlap is simply what two independently found circuits for this map
look like at this size; it is the baseline, not a red flag. Our 88@7's
independence rests on its logged lineage
(`../campaign87_run_2026-07-26_got_88at7/PROVENANCE.md`), and the overlap figure
is consistent with it rather than merely tolerated by it.

So our 88@7 **matches** the published 88-gate record with an independent
circuit — it does not beat it. Our 88@8 is a third distinct family, but its
*lineage* runs through Jean's circuit (see
`../campaign87_run_2026-07-27_got_88at8_thirdfamily/PROVENANCE.md`), so it is a
derived, not independent, construction.

## Certificate subjects

Jean's 88 is the most heavily certified circuit in the project: exhaustive exact
k = 2 and k = 3 shells (empty), 32 685 exact k = 4 windows (all irreducible), and
48 windowed-SAT cone windows of which 44 are UNSAT (frontier k = 16, 4
undecided). See `../campaign87_certificates/CERTIFICATES.md`.
