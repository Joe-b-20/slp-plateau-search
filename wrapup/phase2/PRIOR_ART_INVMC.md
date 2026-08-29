# Prior-art audit: AES **InvMixColumns** as a 2-input-XOR-count problem

**Dossier date: 2026-08-29. Literature-search cutoff: 2026-08-29.**

Target map: the AES inverse MixColumns transformation — multiplication of a
4-byte column by the circulant matrix with first row `[0E, 0B, 0D, 09]` over
GF(2⁸) with `q(x) = x⁸+x⁴+x³+x+1`, viewed as a **32 × 32 invertible matrix over
GF(2)** and implemented as a straight-line program of free-standing 2-input XOR
gates. This is the exact analogue of the MixColumns problem audited in the
records repository (`~/xor_ui/aes_mc_records/PRIOR_ART.md`), and this file
follows that file's format and citation discipline: every figure is tied to a
specific paper, table and page; the cost model is stated for each; s-XOR and
g-XOR are never conflated; and anything not read at the primary source is listed
as UNCONFIRMED.

**Headline, stated once and precisely.** The InvMixColumns XOR-count problem is
**almost entirely unstudied as a problem in its own right.** Exactly **one**
published paper reports a 2-input-XOR count for this matrix
(Xiang–Zeng–Lin–Bao–Zhang, ToSC 2020(2), **92 s-XOR**, full listing in their
Table 4, p. 137). Every other count in this dossier is either (a) an
*implication* of a published MixColumns result under a published invariance
theorem — nobody has written the number down — or (b) from the hardware-area
literature, which uses a different cost function. **No depth is published for
InvMixColumns by anyone.** **No lower bound beyond the trivial ones is published
by anyone.**

---

## 1. The cost model, and which published numbers are comparable

Same model as the records repository, restated for this target:

- **g-XOR / SLP**: an ordered list of free-standing 2-input XOR gates over
  GF(2); cost = number of gates; depth = longest input-to-output gate path.
- **s-XOR (in-place)**: a sequence of instructions `x[i] <- x[i] XOR x[j]` on 32
  registers initialised with the inputs, such that at the end every output
  resides in a register.

**s-XOR → g-XOR (count and depth preserved).** The records repository's SSA
unrolling proposition applies verbatim: a k-instruction s-XOR program unrolls to
a k-gate 2-input XOR circuit *of the same depth*. So a published k-instruction
s-XOR program for InvMixColumns means a published k-gate 2-input XOR circuit for
InvMixColumns.

### 1a. The InvMixColumns-specific twist: s-XOR is inversion-invariant, g-XOR is not

This is the single most important fact in this dossier, and it is why
InvMixColumns has almost no literature of its own.

> **Beierle, Kranz, Leander, CRYPTO 2016 — Corollary 1** (ePrint
> [2016/119](https://eprint.iacr.org/2016/119), §3, immediately after Lemma 1;
> read at the primary source): *"If wt⊕(A) = t, then also wt⊕(A⁻¹) = t."* The
> paper states the setting explicitly one paragraph earlier: *"naturally in the
> setting **not allowing temporary registers**, the XOR-count is invariant under
> taking the inverse."*

Mechanically: an in-place program is a product of type-3 elementary matrices
`I + E_{i,j}`, each of which is its own inverse over GF(2); running the
instruction list **in reverse order** computes the inverse map with **exactly
the same number of instructions**. Xiang et al. spell this out for AES and use
it to produce their InvMixColumns circuit (§5.3, p. 133; see §3.1 below).

Three consequences that govern everything downstream:

1. **Every s-XOR MixColumns record transfers to InvMixColumns at the same
   count, for free.** The best s-XOR MixColumns result therefore *is* the best
   InvMixColumns result, whether or not anyone has said so.
2. **No g-XOR MixColumns record transfers.** Free straight-line programs may use
   temporary wires and are not reversible instruction-by-instruction. In
   particular **Jean's 88 (ePrint 2026/1481) and Sun–Yang–Li's 89 (ePrint
   2025/1493) say nothing about InvMixColumns.** Neither paper mentions the
   inverse; neither count transfers.
3. **Depth does not transfer.** Reversing an instruction list preserves the
   count but rearranges the data-dependency graph, so the depth of the reversed
   program is unrelated to the depth of the forward one. Nobody has measured or
   published the depth of any InvMixColumns circuit. This is an open,
   *cheap-to-close* measurement (see §8).

**Not comparable** (different cost functions; §6 and §7 below): technology-mapped
gate-equivalent (GE) area, FPGA LUT counts, `A_XOR`/`T_XOR` unit-area models,
multi-input XOR gates (XOR3/XOR4), and in-place quantum CNOT circuits.

---

## 2. The published depth–count frontier for InvMixColumns

Every (depth, count) point for the AES InvMixColumns 32 × 32 matrix in a
comparable model that this sweep found. Contrast this with the MixColumns table
in the records repository, which has thirteen rows.

| Depth | Count | Source | Model | Status |
|---|---|---|---|---|
| not stated | **92** | Xiang, Zeng, Lin, Bao, Zhang, ToSC 2020(2), **Table 4, p. 137**; text at §1 p. 122 and §5.3 p. 133. DOI: [10.13154/tosc.v2020.i2.120-145](https://doi.org/10.13154/tosc.v2020.i2.120-145); ePrint [2020/903](https://eprint.iacr.org/2020/903) | s-XOR (⇒ 92-gate 2-input XOR circuit) | **PUBLISHED**, full 92-instruction listing printed in the paper. Verified at the primary source in *both* the ToSC and ePrint versions. |
| not stated | **91** | *Implied*, not published: Yuan, Wu, Shi, Zhang, Zhang, ToSC 2024(2), **Table 2 p. 337 and Table 4 p. 340** (AES MixColumns, 91 **s-XOR**, full in-place listing) + Beierle–Kranz–Leander Corollary 1 | s-XOR (⇒ 91-gate 2-input XOR circuit) | **IMPLIED — no paper states this number for InvMixColumns.** The two ingredients are both published and both verified here at their primary sources; the one-line inference is ours. |
| ≥ 5 | — | minimum achievable depth; **computed for this dossier**, not published | — | See §5. |

**That is the entire comparable-model frontier: one published point and one
implied point.** No depth-constrained record exists at any depth. No published
work reports a g-XOR (free straight-line) search targeted at this matrix.

For scale, the same sweep's MixColumns frontier (records repo, cutoff
2026-07-23) runs 99 @ 3, 97 @ 4, 94 @ 5, 92 @ 6, 88 @ 7 — five Pareto points
from six research groups. InvMixColumns has attracted, in the SLP literature,
**one table**.

---

## 3. Source by source

### 3.1 Xiang, Zeng, Lin, Bao, Zhang — ToSC 2020(2), pp. 120–145 — **92 s-XOR. The only published number.**

Read at the primary source (ToSC published PDF and ePrint 2020/903; both
carry the same text and table numbering).

- **§1, p. 122** (Our Contributions): *"since an invertible matrix and its
  inverse share the same matrix decomposition length (in terms of the number of
  type-3 elementary matrices) [BKL16, Köl19], they have the same implementation
  cost under s-Xor metric. As a direct application, the inverse MixColumns
  matrix used in AES can be implemented with 92 Xor's."*
- **§5.3 "On Inverse Matrices", p. 133**: *"the inverse matrix of AES
  MixColumns is much more complex, and it is often expected to be less
  efficient. Note that Paar's and Boyar-Peralta's heuristics deal with a matrix
  and its inverse independently, and this will result in different
  implementations. However, our heuristic is based on matrix decomposition …
  A direct application of this property is that the AES inverse MixColumns can
  be implemented using only 92 Xor operations (see Table 4)."*
- **Table 4, p. 137**: *"An implementation of AES inverse MixColumns with 92 Xor
  operations."* A full 92-line in-place listing (`u27 = u27 + u3`, …), with
  output positions annotated `[v_i]`. **This is the artefact.** Its companion,
  Table 3 on p. 136, is the corresponding 92-instruction MixColumns program.
- **No depth is stated** for either table.
- Their MixColumns 92 s-XOR matches Maximov's 92 g-XOR (ePrint 2019/833) at the
  time; the InvMixColumns 92 is obtained by the inversion argument, not by a
  separate search.
- Source code and the per-matrix implementations are at
  <https://github.com/xiangzejun/Optimizing_Implementations_of_Linear_Layers>
  (`Implementations/AES.txt`; checked 2026-08-29 — the repository ships the
  forward AES program only, consistent with the inverse being obtained by
  reversal rather than stored separately).

### 3.2 Yuan, Wu, Shi, Zhang, Zhang — ToSC 2024(2), pp. 322–347 — **91 s-XOR for MixColumns; the 91 for InvMixColumns follows but is never stated**

Read at the primary source (ToSC published PDF). DOI:
[10.46586/tosc.v2024.i2.322-347](https://doi.org/10.46586/tosc.v2024.i2.322-347).

- **Abstract, p. 322**: *"For the AES MixColumn operation, we get two
  implementations with 91 XOR counts and depth 13 of in-place quantum
  implementation, respectively."*
- **§1.1, p. 324**: *"we have obtained a new implementation of the AES linear
  layer with **91 XORs under the s-XOR counts metric**, which is equivalent to
  the result obtained under the g-XOR metric [LXZZ21]."*
- **Table 2, p. 337** (row `AES [JV02]`): `97 | 95 | 94 | 91 | 92 | 91*`, the
  first four columns g-XOR ([KLSW17], [BFI19], [TP20], [LXZZ21]) and the last
  two s-XOR ([XZL+20], this paper). The footnote reads: *"Results with (\*)
  indicates that they are also the state-of-the-art known to us under g-XOR
  counting."*
- **Table 4, p. 340**: *"The implementation of AES MixColumn with 91 XORs."* A
  full 91-line in-place listing (`x[15] = x[15] + x[23]`, … with output
  annotations `y[i]`).
- **The word "inverse" does not appear in this paper.** They do not apply
  Corollary 1, and they do not mention InvMixColumns.

**The inference (ours, not theirs).** Table 4 is a 91-instruction s-XOR program
for MixColumns. Reversing it is a 91-instruction s-XOR program for
InvMixColumns (BKL16 Corollary 1 / Xiang et al. §5.3). Unrolling that is a
91-gate 2-input XOR circuit for InvMixColumns. **The best count for
InvMixColumns supportable from the literature is therefore 91, one better than
the only number anyone has published, and it is available by transcribing a
published table backwards.** No paper claims it.

### 3.3 Alexander Maximov — ePrint 2019/833 — **does NOT cover InvMixColumns** (correcting a common assumption)

Read at the primary source, full text. The paper is a four-page note. Its
result is *"a short linear program for AES MixColumn with 92 XOR gates and depth
6"* (abstract, p. 1). **The strings "inverse", "InvMixColumn", "decryption" do
not occur anywhere in the paper**, and it contains exactly one circuit listing,
for the forward matrix. Any claim that Maximov gives an InvMixColumns count is
wrong. (Its §1 does give the classical MixColumns baseline of 108 2-input XOR
gates; there is no inverse counterpart.)

### 3.4 Jérémy Jean — ePrint [2026/1481](https://eprint.iacr.org/2026/1481) — 88 g-XOR, **MixColumns only**; the AI-search precedent

Read at the primary source; the note is two pages.

- *"We give in this short note a circuit implementing the matrix-vector product
  with the 32x32 binary matrix of the AES MixColumns using 88 XOR gates."*
  Algorithm 1, p. 2, is the full 88-line listing.
- History given: 94 [TP19], 92 [Max19], 91 [LXZZ21], 89 [SYL25].
- **Acknowledgements, p. 1**: *"This result has been found with the help of AI,
  most specifically models from OpenAI under codex."* This is the only
  AI-search result in this problem family, and it is the single most relevant
  precedent for a phase-2 InvMixColumns programme.
- **Nothing in the note concerns InvMixColumns**, and the 88 is a free
  straight-line program, so it does **not** transfer under Corollary 1. As of
  the cutoff, **no AI-assisted (or any other) result has been published for the
  inverse matrix.**

### 3.5 Sun, Yang, Li — ePrint [2025/1493](https://eprint.iacr.org/2025/1493) — 89 g-XOR, **MixColumns only**

Read at the primary source (version last updated 2025-11-13). Abstract: *"we
achieve the first implementation requiring only 89 g-Xor operations, improving
upon the previous best result of 91 g-Xor operations."* §5.2, Tables 2–4, are
all the forward matrix; **the string "inverse" does not occur in the paper.**
Their structural observation (a row permutation of the MixColumns matrix
grouping targets into eight patterns, Table 3) is MixColumns-specific and has no
published InvMixColumns analogue.

### 3.6 Osvik, Canright — ePrint [2024/1076](https://eprint.iacr.org/2024/1076) — 94 @ depth 5, 97 @ depth 4, **explicitly excludes decryption**

Read at the primary source. §2, p. 2: *"(We will not consider decryption
here.)"* §1, p. 2: *"our two new results are 94-XOR depth 5 (see Appendix F) and
97-XOR depth 4 (see Appendix G)."* Appendix F is headed *"AES MixColumns with 94
XORs and depth 5"*, Appendix G *"AES MixColumns with 97 XORs and depth 4"*.
These are the *only* depth-annotated free straight-line AES-linear-layer
circuits at depths 4–5 in the literature, and **they have no inverse
counterpart.**

### 3.7 Shi, Feng, Xu — ToSC 2023(4), pp. 489–510 — depth-constrained, **MixColumns only**

Read at the primary source. Their result: *"the framework BPBS is capable of
finding an implementation of depth 3 with only 99 XOR gates"* (§5.1, p. 502;
listing in Table 4, p. 503). **Table 3, p. 502** is the depth-annotated
MixColumns comparison table — `[KLSW17] 97/8, [TP20] 94/6, [XZL+20] 92/6,
[Max19] 92/6, [LXZZ21] 91/7, [LSL+19] 105/3, [BFI21] 103/3, [LWF+22] 103/3,
[LZW23] 102/3, IBPD 101/3, IBPD-MD 100/3, BPBS 99/3` — and **every entry is the
forward matrix.** The word "inverse" appears in this paper only in the sense of
"involutory" matrices (self-inverse MDS matrices designed to be their own
inverse — a *different* target, not AES's). **This is the depth-constrained
literature, and InvMixColumns is absent from it.**

### 3.8 Everything else checked, with no InvMixColumns result

All read at the primary source and searched full-text for
`inverse` / `InvMixColumn` / `MC⁻¹`:

| Source | AES MixColumns result | InvMixColumns? |
|---|---|---|
| Kranz, Leander, Stoffelen, Wiemer, ToSC 2017(4); ePrint [2017/1151](https://eprint.iacr.org/2017/1151) | 97 | **No.** "Involutory" hits only, a different target. |
| Banik, Funabiki, Isobe, IWSEC 2019; ePrint [2019/856](https://eprint.iacr.org/2019/856) | 95 | **No.** "Involutary" hits only. |
| Tan, Peyrin, TCHES 2020(1); ePrint [2019/847](https://eprint.iacr.org/2019/847) | 94 | **No.** |
| Lin, Xiang, Zeng, Zhang, CT-RSA 2021, LNCS 12704 | 91 (g-XOR per Yuan Table 2; 91/7 per SFX23 Table 3) | **Not verifiable — paywalled.** See UNCONFIRMED. |
| Liu, Zhao, Wang et al., ePrint [2023/174](https://eprint.iacr.org/2023/174) (LZW23) | 102 @ depth 3 | **No.** |
| HILL, ToSC 2026(1) ([view/12794](https://tosc.iacr.org/index.php/ToSC/article/view/12794)) | 79 "h-XOR" @ depth 3 (mixed XOR2/XOR3) | **No.** One "inverse" hit, unrelated (a rewrite rule). |
| Zhang et al., "More Inputs Makes Difference", ToSC ([view/9724](https://tosc.iacr.org/index.php/ToSC/article/view/9724)) | 243 with XOR4 gates | **No.** |
| "Utilizing Circulant Structure…", ToSC 2026 ([view/13012](https://tosc.iacr.org/index.php/ToSC/article/view/13012); arXiv [2511.18226](https://arxiv.org/abs/2511.18226)) | quantum CNOT depth 10 / 107 gates | **No.** |
| Shi, Feng, ASIACRYPT 2024; ePrint [2024/381](https://eprint.iacr.org/2024/381) | quantum, depth-10 linear layer | **No.** |
| Yu, Liu, "Multiple Rows Mixers and Hsilu", ToSC; ePrint [2025/1960](https://eprint.iacr.org/2025/1960) | new linear-layer family | **No.** |
| Pehlivanoğlu, Demir, PeerJ CS ([PMC10807753](https://pmc.ncbi.nlm.nih.gov/articles/PMC10807753/)) | 44 gates @ depth 3 (5×XOR2 + 7×XOR3 + 32×XOR4), Table 5 | **No.** Confirmed by targeted read. |

**Archive-level negative check (2026-08-29).** The IACR Cryptology ePrint
Archive full-text-of-metadata search (titles, authors, abstracts, keywords) for
`InvMixColumns` returns **"No results"**. The search for `inverse MixColumns`
returns exactly four papers — 2016/592, 2017/118, 2019/107, 2024/381 — none of
which is an implementation-cost paper for this matrix. `title:MixColumns`
returns five papers, of which only Jean's 2026/1481 is an implementation paper.
`"s-XOR"` returns four papers: 2025/1493, 2024/1171 (unrelated, a DDH result),
2020/903, 2019/856.

---

## 4. Structural facts that constrain the problem

These are algebraic facts about the matrix, published in the hardware
literature, that any InvMixColumns search programme has to reckon with. Each is
sourced; the arithmetic verifications noted as "checked here" are ours.

- **InvMC = MC³, i.e. the AES MixColumns matrix has multiplicative order 4.**
  Banik, Bogdanov, Regazzoni, *Compact Circuits for Combined AES
  Encryption/Decryption* (author PDF via EPFL Infoscience), §"Combined
  Mixcolumn": *"we take advantage of the fact that the Inverse Mixcolumn matrix
  used in AES is the cube of the Forward Mixcolumn matrix"*, printed with the
  matrix identity `[[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]] =
  [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]³`. **Checked here** by direct
  GF(2⁸) computation: MC² = circ(05,00,04,00), MC³ = circ(0E,0B,0D,09) = InvMC,
  MC⁴ = I.
- **Hence InvMC = MC ∘ MC², with MC² = circ(05,00,04,00).** This is the
  classical decryption-reuse factorisation used throughout the AES hardware
  literature (Fischer, Drutarovský, Chodowiec, Gramain, *InvMixColumn
  decomposition and multilevel resource sharing in AES implementations*, IEEE
  TVLSI 13(8), 2005, DOI [10.1109/TVLSI.2005.853606](https://doi.org/10.1109/TVLSI.2005.853606)).
  It gives the trivial upper bound cost(InvMC) ≤ cost(MC) + cost(MC²), which at
  the 88-gate MixColumns record is far above 91 and is therefore **not** a route
  to a record — but it *is* a route to a structured seed circuit.
- **The matrix is much denser than MixColumns.** Computed here from the 32 × 32
  binary matrix: MixColumns has 184 ones, row weights {5 (×20), 7 (×12)};
  **InvMixColumns has 472 ones, row weights {11 (×8), 13 (×8), 15 (×4), 17 (×4),
  19 (×8)}** — 2.57× the density. Xiang et al. anticipate the consequence at
  §5.3, p. 133: *"the inverse matrix of AES MixColumns is much more complex, and
  it is often expected to be less efficient."* The empirical surprise of their
  §5.3 is that under s-XOR it is **not** less efficient — it costs exactly the
  same.

---

## 5. Depth: nothing published, and a computable floor

**No depth figure for any InvMixColumns circuit appears in any source found by
this sweep.** Xiang et al.'s Table 4 and Yuan et al.'s Table 4 both print
instruction lists with no depth annotation, and the reversal that produces the
inverse program does not preserve the forward program's depth (§1a).

**Minimum achievable depth = 5** (computed for this dossier from the matrix, not
taken from any paper). The standard argument — an output depending on `w` inputs
needs depth at least `⌈log₂ w⌉`, stated for MixColumns in Shi–Feng–Xu ToSC
2023(4) — applied to InvMixColumns's maximum row weight of 19 gives
`⌈log₂ 19⌉ = 5`. For contrast the same argument gives 3 for MixColumns (maximum
row weight 7), which is the known and attained MixColumns minimum.

So the depth-constrained frontier for InvMixColumns is **entirely empty from
depth 5 upward**, and depths 1–4 are impossible. Any circuit at depth 5, 6 or 7
with any gate count would be the first published point at that depth.

---

## 6. MixColumns + InvMixColumns sharing — one short section

Implementations that compute *both* directions with shared gates constrain what
"optimal InvMixColumns alone" is worth in practice. This is a large, old, and
methodologically separate literature: it measures **area** (GE, LUTs, or
unit-`A_XOR` models), not SLP length, and it optimises the *combined* circuit
including multiplexers and control.

- **Fischer, Drutarovský, Chodowiec, Gramain**, IEEE TVLSI 13(8), 2005 — the
  canonical InvMixColumn decomposition paper; serial and parallel decompositions
  with word-, byte- and bit-level resource sharing; reported reduction of
  reconfigurable logic area of the complete cipher by up to 20%. (Abstract read;
  full text paywalled — see UNCONFIRMED.)
- **Banik, Bogdanov, Regazzoni**, *Compact Circuits for Combined AES
  Encryption/Decryption* (JCEN; author PDF read at EPFL Infoscience). The
  MC³ trick removes the InvMixColumns circuit entirely at the cost of running
  MixColumns three times: *"a Forward Mixcolumn circuit which occupies 108 xor
  gates is sufficient for both purposes. This saves us area equal to 58 xor
  gates and one 32 bit multiplexer, which amounts to around 130 GE."* Their
  full combined enc/dec core is 2227 GE. **Note the asymmetry this creates:** in
  a serial architecture the *cheapest* InvMixColumns is not a circuit at all —
  it is three passes through the MixColumns circuit. A better standalone
  InvMixColumns circuit only pays off in a round-parallel or latency-bound
  design.
- **Zhang, Yang, Zheng, Zhang, Wu**, *A full matrix joint optimization method
  for hardware implementation of AES MixColumns/InvMixColumns*, IEICE
  Electronics Express 17(24), 2020, DOI
  [10.1587/elex.17.20200391](https://doi.org/10.1587/elex.17.20200391) (full
  text read). Measures in `A_XOR` (unit 2-input-XOR area) and `T_XOR`. §3.2:
  MixColumns direct implementation **152 A_XOR @ 3 T_XOR**; InvMixColumns direct
  implementation **440 A_XOR @ 5 T_XOR**; whole-matrix joint optimisation gives
  an area reduction *"up to 56.14% at min CPD constraint and up to 61.59% at min
  area constraint"* for InvMixColumns. The absolute optimised figures live in
  their Table II, which is a vector graphic that text extraction cannot read —
  the implied values (≈193 and ≈169 A_XOR) are our arithmetic and are listed as
  UNCONFIRMED. **Either way, the CSE/hardware line is ~2× off the 92 that the
  SLP line reached in the same year**, because it shares subexpressions inside a
  byte-level coefficient structure rather than searching the 32 × 32 matrix.
- **Later FPGA line** (e.g. *Efficient Fine-Grained LuT-Based Optimization of
  AES MixColumns and InvMixColumns for FPGA Implementation*, Electronics
  14(24):4912, 2025, DOI
  [10.3390/electronics14244912](https://doi.org/10.3390/electronics14244912))
  targets LUT6 primitives rather than XOR gates. Not comparable in either
  direction; publisher blocked automated retrieval (UNCONFIRMED).

**What this section means for phase 2.** Nothing in the sharing literature
competes with 92/91 as an XOR count, and nothing in it would be improved by a
better standalone InvMixColumns SLP in a byte-serial design. The market for a
record InvMixColumns circuit is the same market as for a record MixColumns
circuit: round-unrolled hardware, bitsliced software, masking/threshold
implementations where every gate is multiplied by the share count, and quantum
circuit synthesis where the s-XOR form maps to in-place CNOTs.

---

## 7. Lower bounds

**Confirmed: nothing published for InvMixColumns beyond the trivial bounds.**
The sweep found no lower-bound statement of any kind for this matrix. For
completeness, the trivial bounds and what is known for the sibling problem:

- **Trivial gate bound: ≥ 32.** Every one of the 32 outputs has row weight ≥ 11,
  so no output is an input or a copy, so each needs at least one gate of its own.
  (Not published; stated here as folklore.)
- **Trivial depth bound: ≥ 5.** §5 above.
- **No published bound for MixColumns either.** The records repository's audit
  found none, and this sweep found none: the whole family's "records" are upper
  bounds from heuristic search. The SLP problem is NP-hard, and the literature's
  only general negative results are hardness and approximation-ratio statements,
  not instance bounds.
- The `slp-plateau-search` project's own MixColumns lower-bound work
  (certificate LP capped at 91.41; the outstanding purchasable lemma
  G_int(3) ≥ 92; see the e17 dossier) has **no InvMixColumns analogue anywhere
  in the literature**, and would be a first if ported.

---

## 8. Cost-model caveats

Read these before quoting any number above.

1. **s-XOR vs g-XOR is the load-bearing distinction here, more than for
   MixColumns.** Both InvMixColumns counts in §2 are s-XOR results. They are
   valid 2-input-XOR gate counts (the SSA-unrolling proposition), but they were
   *not* produced by a free straight-line search of the inverse matrix. Nobody
   has run a g-XOR search on InvMixColumns. Given that free search beat
   in-place search by 3 gates on MixColumns (88 g-XOR vs 91 s-XOR), the g-XOR
   optimum for InvMixColumns is plausibly well below 91 — but **that is a
   conjecture with zero published evidence, and this dossier does not assert
   it.**
2. **Depths in §2 are absent, not zero.** Neither published table states a
   depth, and the reversal that yields InvMixColumns does not preserve the
   forward depth. Any depth attached to an InvMixColumns circuit must be
   measured on a concrete transcription and labelled as a measurement — exactly
   the discipline the records repository applies to Jean's and Sun–Yang–Li's
   circuits. **This is the cheapest open item in the whole dossier**: transcribe
   Xiang Table 4 (p. 137) and the reversal of Yuan Table 4 (p. 340), run the
   ASAP least-fixpoint schedule, and the depth-constrained frontier acquires its
   first two points.
3. **Bit and byte conventions.** Gate counts and depths are invariant under
   input/output relabelling, so column-order, byte-order and MSB/LSB conventions
   do not affect any comparison. The row-weight figures in §4 were computed
   MSB-first; the multiset of row weights is convention-independent.
4. **`A_XOR` is not a gate count in the SLP sense.** The IEICE figures in §6
   count 2-input XOR gates in a *fixed structural decomposition* (coefficient
   multipliers plus adder trees), not in an unrestricted straight-line program.
   They are legitimately comparable in units and not comparable in kind.
5. **GE, LUT and quantum CNOT figures are excluded** for the same reasons as in
   the records repository.
6. **Multi-input XOR figures are excluded.** No InvMixColumns figure exists in
   that model anyway.

---

## 9. UNCONFIRMED list

Numbers or statements this dossier could not verify at the primary source, with
the secondary source used.

1. **Lin, Xiang, Zeng, Zhang, CT-RSA 2021 — "91 XOR for AES MixColumns", metric
   and any inverse content.** Springer/ACM paywalled; no ePrint or author PDF
   found. Two independent secondaries agree on the count: Yuan et al. ToSC
   2024(2) **Table 2, p. 337** places `[LXZZ21] 91` in its **g-XOR** sub-table,
   and Shi–Feng–Xu ToSC 2023(4) **Table 3, p. 502** lists it as **91/7**
   (count/depth). Jean's note also lists *"91 XOR in [LXZZ21]"*. **Note for the
   records repository:** its own frontier table labels Lin et al.'s 91 as
   *s-XOR*; both secondaries here say **g-XOR**. If g-XOR is right, the 91 does
   **not** transfer to InvMixColumns under Corollary 1 — and the 91 for
   InvMixColumns rests on Yuan et al.'s s-XOR 91 alone, which *is* verified.
   Neither secondary shows any InvMixColumns entry for Lin et al., but absence
   from a citing table is not absence from the paper. **Flagged as a discrepancy
   worth resolving in the records repo independently of this dossier.**
2. **Zhang et al., IEICE ELEX 2020 — absolute optimised InvMixColumns area.**
   The in-text figures (152 and 440 `A_XOR`, and the 56.14% / 61.59% reductions)
   are verified; the resulting ≈193 and ≈169 `A_XOR` are **our arithmetic**, and
   their Table II could not be extracted (vector-drawn table).
3. **Fischer, Drutarovský, Chodowiec, Gramain, IEEE TVLSI 2005 — full text.**
   IEEE paywalled. Abstract and the "up to 20% area reduction" figure taken from
   the IEEE/Semantic Scholar abstract. The InvMixColumn-decomposition *fact* is
   independently confirmed by our own GF(2⁸) computation (§4) and by
   Banik–Bogdanov–Regazzoni's printed identity.
4. **Electronics 14(24):4912, 2025 (MDPI LUT paper) — all figures.** Publisher
   returned HTTP 403 to automated retrieval; only a search-engine summary was
   available. No number from it is quoted as a value in this dossier.
5. **Banik–Bogdanov–Regazzoni's "58 xor gates" saving.** Quoted verbatim from
   the author PDF, but the paper does not state what standalone InvMixColumns
   circuit those 58 gates belonged to, so the figure should not be read as an
   InvMixColumns gate count.
6. **Completeness of the negative claims.** §3.8's "no InvMixColumns result" was
   established by full-text search of downloaded PDFs for `inverse`,
   `InvMixColumn`, `MC⁻¹` and `decryption`. Text extraction can silently fail on
   vector-drawn tables (as it did for the IEICE Table II), so a count hidden in
   a graphic table would be missed. Treat every negative here as best-effort
   with a date. The records repository's own July sweeps are the cautionary
   precedent: they corroborated a 91-XOR MixColumns floor against every
   2024–2026 comparison table while ePrint 2025/1493's 89 sat unnoticed.

---

## 10. State of the problem

**Best known count: 91 two-input XOR gates — and nobody has published it.** The
only *published* InvMixColumns count is **92 s-XOR** (Xiang et al., ToSC 2020(2),
Table 4, p. 137), which is also the only complete InvMixColumns circuit listing
in the literature. One gate better is available for the price of transcribing
Yuan et al.'s 91-instruction s-XOR MixColumns program (ToSC 2024(2), Table 4,
p. 340) backwards, under a CRYPTO 2016 corollary that Xiang et al. already
applied to this exact matrix — but no paper takes that step, so 91 is an
*implied* record with no claimant. **Best depth-constrained record: none exists
at any depth.** No InvMixColumns circuit anywhere has a published depth; the
minimum possible depth is 5 (computed here; ⌈log₂ 19⌉ from the matrix's maximum
row weight), so the entire depth-constrained frontier is unclaimed. **Gap to any
bound: unmeasurable** — no lower bound beyond ≥32 gates and ≥5 depth exists for
this matrix, and none exists for MixColumns either.

**How active is the area?** For MixColumns: very. Five groups moved the count
between 2017 and 2026 (97 → 95 → 94 → 92 → 91 → 89 → 88), the last two steps
inside thirteen months, and the depth-3 line moved 105 → 99 over the same
period. For InvMixColumns: **inactive to the point of vacancy.** One table in
2020, obtained as a corollary rather than by search, and nothing since. The
ePrint archive has never carried a paper with "InvMixColumns" in its title,
abstract or keywords. The most recent and most sophisticated tools — Sun–Yang–Li's
linear-combination Boyar–Peralta, Shi–Feng–Xu's depth-constrained BPBS, Jean's
AI-assisted search — have every one of them been pointed at the forward matrix
and never at the inverse. Jean's note is the only AI-search result in the family
and it is MixColumns-only; **applying AI search to InvMixColumns is, as of
2026-08-29, an entirely open move that no one has made.** The asymmetry has a
clear cause: MixColumns is on the encryption hot path everyone benchmarks, and
the sharing literature (§6) taught hardware designers that InvMixColumns is
free-ish via MC³ — so the incentive to search it hard never formed.

**Obvious analogy targets after InvMixColumns.** Only targets the literature
actually optimises as 2-input XOR counts:

- **Other ciphers' MDS matrices, forward direction.** The standard benchmark
  suite carried in every paper's Table 1/2 (Xiang et al. ToSC 2020(2) Table 1;
  Yuan et al. ToSC 2024(2) Table 2): Anubis 98, Clefia M0 97 / M1 103, Twofish
  110, Fox mu4 130, Khazad 366, Whirlwind M0 173 / M1 181, Joltik 44,
  SmallScale AES 42, Grøstl/Whirlpool at 64×64. Every one of these is
  *actively* contested and every one has the same inverse blind spot — Xiang
  et al.'s Corollary-1 argument applies verbatim to all of them, and no paper
  reports the inverse count for any of them either.
- **Involutory MDS matrices** (SS16, LW16, SKOP15, JPST17 rows in the same
  tables) are optimised as XOR counts but are *self-inverse by construction*, so
  they are the degenerate case of this dossier's question and not an analogy
  target.
- **The AES S-box's linear layers** — the top and bottom linear parts of the
  Boyar–Peralta S-box decomposition — are optimised as XOR counts in the S-box
  literature (Maximov–Ekdahl, ePrint 2019/802 and the "Smashing the
  Implementation Records of AES S-box" line), but as *sub-blocks of a nonlinear
  circuit* under a mixed AND/XOR objective, not as a clean 32×32 SLP problem.
  A different game; noted, not recommended.
- **Not a target: quantum CNOT synthesis** (ToSC 2026 circulant paper,
  Shi–Feng ASIACRYPT 2024). Same matrices, different resource model, already
  crowded.

---

## 11. How this audit was compiled

One sweep, 2026-08-29, over: IACR ePrint (including three direct archive
metadata searches — `InvMixColumns`, `inverse MixColumns`, `title:MixColumns`,
`"s-XOR"` — whose result counts are recorded verbatim in §3.8), ToSC/FSE (six
papers downloaded and full-text searched), CT-RSA and Springer LNCS, arXiv,
PeerJ CS / PMC, IEEE Xplore and J-STAGE abstracts, MDPI, EPFL Infoscience,
Semantic Scholar, and GitHub artefact repositories. Sixteen PDFs were retrieved
and searched at full text; two primary sources (Lin et al. CT-RSA 2021; Fischer
et al. TVLSI 2005) were paywalled and are recorded in §9.

Where a number appears above without an UNCONFIRMED tag, it was read in the
paper's own text or table, with the page recorded. Where a number is an
implication rather than a claim (the 91), it is labelled as such at every
occurrence. The matrix-level computations (row weights, MC⁴ = I,
MC² = circ(05,00,04,00), the depth floor of 5) were performed for this dossier
and are labelled as ours everywhere they appear; they are one-line GF(2⁸)
calculations and are independently reproducible.

Negative claims here — "no depth is published", "no lower bound exists", "no AI
search has been applied" — rest on targeted searches and full-text greps, not on
exhaustive enumeration of the literature. They are best-effort statements with a
date, not proofs of absence.
