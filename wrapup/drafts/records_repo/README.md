# Small XOR circuits for AES MixColumns

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21299092.svg)](https://doi.org/10.5281/zenodo.21299092)
[![verify](https://github.com/Joe-b-20/aes-mixcolumns-xor-circuits/actions/workflows/verify.yml/badge.svg)](https://github.com/Joe-b-20/aes-mixcolumns-xor-circuits/actions/workflows/verify.yml)

Verified 2-input XOR circuits for AES MixColumns, with a verifier that rebuilds
the specification from scratch. Nothing here is claimed optimal.

## The records

**Frontier: 97 gates at depth 3, 91 at depth 4, 88 at depth 5.** One line, all of
it on this project's own lineage, no imported circuits.

| File | Gates | Depth | Best published at that depth | |
|---|---|---|---|---|
| `circuits/mixcolumns_97gates_depth3.json` | 97 | 3 | 99 (Shi, Feng, Xu, ToSC 2023) | 2 fewer |
| `circuits/mixcolumns_91gates_depth4.json` | 91 | 4 | 97 (Osvik, Canright, ePrint 2024/1076 App. G) | 6 fewer |
| `circuits/mixcolumns_88gates_depth5_fromscratch.json` | 88 | 5 | 94 (Osvik, Canright, App. F) | 6 fewer |
| `circuits/mixcolumns_88gates_depth6.json` | 88 | 6 | 92 (Maximov, ePrint 2019/833) | 4 fewer |

Depth 3 is the minimum possible depth: MixColumns has outputs depending on 7
inputs, so no circuit can be shallower.

**88 is flat.** 88 is the smallest gate count anyone has, at any depth. It is
**Jean's count** (ePrint 2026/1481, 2026-07-23) and **Jean has priority**. This
repository holds five 88s and none of them lowers that floor — what they change
is the *depth* at which 88 is reached. Two of the five are derived from Jean's
circuit and labelled so everywhere.

Also shipped, none of them a frontier point: `mixcolumns_88gates_depth5.json`
(derived from Jean's), `mixcolumns_88gates_depth7.json` (an independent circuit
matching Jean's point, 61 of 88 masks shared), `mixcolumns_88gates_depth8.json`
(derived), `mixcolumns_89gates_depth5.json`, and three earlier circuits kept for
the archival record (98 @ 3, 91 @ 6, 89 @ 10). The 92 @ 4 that was the depth-4
record until 2026-08 is retained too, superseded by the 91 above.

Each circuit is also a plain-text listing in `listings/`, a Verilog netlist and
testbench in `verilog/`, and an entry in `bounds.json` with its hashes,
provenance and exact claim. All of those are generated from `circuits/`.

## The bracket

**56 ≤ L(M) ≤ 88** for the minimum 2-input XOR count of MixColumns.

- **Upper: 88.** A verified 88-gate circuit exists; several are in `circuits/`.
- **Lower: 56.** An unconditional, refereed counting certificate at depth 4.
  It is the only lower bound we know of for this matrix in the literature.

The gap is 32 gates wide. Nobody has closed it.

## Verify

Pure Python 3, no dependencies:

~~~text
python3 verify.py            # fast single path
python3 verify_all.py        # adds the independent clean-room verifier
~~~

`verify.py` rebuilds MixColumns in GF(2⁸) from `0x11b` and the column
`[2,3,1,1]` (FIPS 197-upd1 §5.1.3 Eq. 5.6), simulates each circuit on the 32
unit inputs, and compares. The map is linear, so agreement on the basis is a
complete correctness check. It also rechecks declared gate count, declared
depth, DAG order and both SHA-256 fields. A passing run ends
`ALL CIRCUITS VERIFIED.`

`audit/cleanroom_verify.py` is a second verifier written independently against a
byte-level reference, with 100,000 deterministic random tests and 14 adversarial
mutations it must reject. With Icarus Verilog installed,
`python3 verify_all.py --with-verilog` adds a simulation path.

The convention is in the verifier, not in prose. If yours differs — a different
bit order, a transposed matrix — regenerate the target masks under it before
comparing counts.

## Prior art

Published depth–count frontier, source-checked circuit by circuit in
[`PRIOR_ART.md`](PRIOR_ART.md):

| Depth | Gates | Source |
|---|---|---|
| 3 | 99 | Shi, Feng, Xu, ToSC 2023 |
| 4 | 97 | Osvik, Canright, ePrint 2024/1076 App. G |
| 5 | 94 | Osvik, Canright, App. F |
| 6 | 92 | Maximov, ePrint 2019/833; also Xiang et al., ToSC 2020 |
| 7 | 88 | Jean, ePrint 2026/1481 |

Sun, Yang and Li (ePrint 2025/1493) publish an 89 at unconstrained depth.
Neither Jean nor Sun–Yang–Li states a depth; the 7 and the 9 used here are this
project's own measurements of its own transcriptions, and both are *forced* —
the shallowest schedule either mask set admits still gives 7 and 9.

`PRIOR_ART.md` has the full audit, including a dated corrections log. If
something published beats 97 at depth 3, 91 at depth 4, 88 at depth 5, 88 at
depth 6, or uses fewer than 88 gates at any depth, please open an issue.

## Opinion

*This section is opinion, not proof. Nothing below is claimed as a result.*

**We think 88 is optimal.** Several independent search methods have between them
produced over 1.5 million distinct verified 88-gate solutions and not one 87.
The 88 plateau is enormous and the level below it looks empty. That is a belief
about a search, not a theorem; the honest bracket stays 56 ≤ L(M) ≤ 88.

**If an 87 exists, here is what we can say about its shape.** These are results,
not opinion:

- It is not one gate away from anything we hold. Deleting a gate from an 88
  gives an 87 only if that gate is redundant — a duplicated mask, or a
  non-output gate nothing consumes. Across 1,575,516 distinct verified 88-gate
  solutions there is no duplicated mask, and all 28,796 that carry a build order
  have exactly 56 consumed non-output gates, the value that says no such gate
  exists. No 87 by deletion anywhere in the corpus.
- It differs from every certified 88 here by at least 4 masks. Removing up to 3
  masks from those circuits and rebuilding cheaper is exhaustively impossible.
- It cannot resynthesise 4 output rows cheaply. For the depth-5 88, all 35,960
  four-row drop sets were refuted at one gate fewer.
- It is not built the way every known 88 is built. For the merged block in our
  standard decomposition, 9 through 14 gates are all proven UNSAT (the 14 case
  decided 2026-09-01, ~99 core-hours), so that block costs exactly 15 and
  merging the two largest levels saves nothing. An 87 that does not split into
  these blocks escapes this test entirely; none of our circuits is such an
  exception.

Read together, an 87 would have to be structurally unlike every 88 we have ever
seen, not a local repair of one. **That is the opinion. It is not evidence that
87 does not exist** — a negative inside a radius-4 neighbourhood carries no
information about whether an 87 exists, and we say so wherever a certificate is
quoted.

## For 87-hunters and optimality-provers

Four directions, one line each. Methods, code and run archives are in
[`slp-plateau-search`](https://github.com/Joe-b-20/slp-plateau-search); this
repository is circuits only.

- **The block-structure route is closed.** The SAT instance that asked whether
  an 87 with our block decomposition exists returned UNSAT (2026-09-01). What
  no test covers: an 87 with a different block structure. That is now the
  sharpest open question.
- **Lift the lower bound.** 56 comes from one counting certificate at depth 4.
  Nothing rules out a much better bound by the same route; we know of no
  published attempt to try.
- **Cancellation.** Without cancellation the count is provably at least 92 —
  four *above* the record. So every 88 spends cancellation to get there, and
  what cancellation buys is, we think, the real question behind optimality.
- **Foreign lineages.** Every 88 we hold came from our own solvers. An 88 built
  by an unrelated method is the cheapest thing anyone could contribute: run the
  deletion check above on it, and a solution with a different structure would be
  new evidence either way.

## Available on request

Not shipped here because of size; email or open an issue and we will send them.

- **1,575,516 distinct verified 88-gate mask sets**, deduplicated. 28,796 carry
  a build order and are directly runnable; 92 of those are at depth 5. This is a
  verified floor — two further large classes are counted but not hashed, so the
  true figure is somewhere between 1.6 and 4.4 million.
- **The k = 2 irreducibility sweep**: all 139,878 harvested distinct 88-gate mask
  sets proven irreducible, 215,412,120 exact window decisions, zero reducible.
- **UNSAT certificates** for the merged block at 9, 10, 11, 12 and 13 gates, and
  the packaged open instance at 14.
- **The three depth-4 lineages.** The published 91 is one of three independent
  91-gate depth-4 circuits we hold, plus 15,912 distinct realizable 91 @ 4 mask
  sets.
- **Verilog, listings and audit reports** for anything above, generated by the
  same scripts as the shipped ones.

## The exact model

- A circuit is a list of **2-input XOR gates over GF(2)**.
- Signals are indexed from 0. Signals 0..31 are the 32 input bits.
- Gate `k` produces signal `32 + k` = `signal[gates[k][0]] XOR
  signal[gates[k][1]]`. Both parents have strictly smaller index, so the circuit
  is a DAG in list order.
- Depth of a signal is the longest path in gates from any input; inputs have
  depth 0. Circuit depth is the maximum over all gates.
- `outputSignals[j]` names the signal carrying MixColumns output bit `j`.
- Bit `i` in 0..31 means bit `(i mod 8)` of byte `(i div 8)`,
  least-significant-bit first.
- `sha256_canonical_gates` is SHA-256 over the compact JSON
  `{"inputCount":32,"gates":[...]}` — a formatting-independent fingerprint.
  `sha256_circuit_json` is over the file bytes.

Every `k`-instruction in-place (s-XOR) program gives a `k`-gate 2-input XOR
circuit, so s-XOR counts are comparable and the earlier 91s (Lin et al.,
CT-RSA 2021; Yuan et al., ToSC 2024) are in scope. Multi-input XOR gates,
gate-equivalent area and quantum CNOT are different cost models and are not
claimed against.

## Contents

~~~
circuits/     twelve circuit JSON files
listings/     the same circuits as plain text (generated)
verilog/      one netlist + one testbench per circuit (generated)
docs/         the depth-count frontier figure (generated)
bounds.json   per-circuit hashes, provenance and exact claims
PRIOR_ART.md  source-by-source audit of every comparison
PAPER.md      short write-up; paper/ holds the LaTeX and PDF
audit/        clean-room verifier and its generated reports
scripts/      the generators
tests/        regression tests for shipped and malformed artifacts
~~~

## References

- NIST, *Advanced Encryption Standard (AES)*, FIPS 197-upd1, 2023.
  <https://doi.org/10.6028/NIST.FIPS.197-upd1>
- A. Maximov, *AES MixColumn with 92 XOR Gates*, ePrint 2019/833.
- Z. Xiang, X. Zeng, D. Lin, Z. Bao, S. Zhang, *Optimizing Implementations of
  Linear Layers*, ToSC 2020(2):120-145.
- D. Lin, Z. Xiang, X. Zeng, S. Zhang, *A Framework to Optimize Implementations
  of Matrices*, CT-RSA 2021, LNCS 12704.
- H. Shi, X. Feng, S. Xu, *A Framework with Improved Heuristics to Optimize
  Low-Latency Implementations of Linear Layers*, ToSC 2023(4):489-510.
- Y. Yuan, W. Wu, T. Shi, L. Zhang, Y. Zhang, *A Framework to Improve the
  Implementations of Linear Layers*, ToSC 2024(2):322-347.
- D. A. Osvik, D. Canright, *A More Compact AES, and More*, ePrint 2024/1076.
- Y. Sun, R. Yang, T. Li, *Revisit the Boyar-Peralta Algorithm to Solve the
  Shortest Linear Program Problem*, ePrint 2025/1493.
- J. Jean, *88-XOR Implementation of the AES MixColumns Matrix*, ePrint
  2026/1481.

## License / citation

MIT. Cite the note (`paper/mixcolumns_note.pdf`, or `PAPER.md`) and this
repository via <https://doi.org/10.5281/zenodo.21299092> — see `CITATION.cff`.
