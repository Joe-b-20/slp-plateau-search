# Imported prior-art circuits — NOT this project's results

These two circuits were **published by other people**. They are archived here
because campaign 87 used them (as search seeds, as certificate subjects, and as
the comparison baseline), and because several of this project's own results must
be described relative to them. They are always to be credited to their authors.

| file | gates @ depth | author / source | how it got here |
|---|---|---|---|
| `jean_88gates_depth7_eprint_2026-1481.json` | **88 @ 7\*** | **Jean, ePrint 2026/1481**, Algorithm 1 (88-XOR AES MixColumns), posted 2026-07-23 | transcribed from the paper, input bits relabelled to this repo's convention, then oracle-verified; \*the paper states no depth — depth 7 is what this repo's oracle measures for the transcribed circuit, exactly as for the 89 below |
| `sunyangli_89gates_eprint_2025-1493.json` | **89 @ 9\*** | **Sun–Yang–Li, ePrint 2025/1493**, Table 4 (89 "g-XOR" AES MixColumns — the same model as Jean's, and as this repo's) | same route; \*the paper states no depth — depth 9 is what this repo's oracle measures for the transcribed circuit, exactly as for the 88 above |

Both files keep their **gate lists** and their original `gateCount` / `depth` /
`provenance` / `source` / `input_permutation_paper_to_repo` fields exactly as
written at import time. Neither is the product of any search in this repository.

**One documented, non-substantive addition (2026-07-29).** Both files gained two
derived keys, `outputSignals` and `outputConvention`, so that a reader comparing
them against the papers does not have to infer which internal signal carries
which output bit. `outputSignals[j]` is the index of the signal whose mask equals
MixColumns output bit `j` under this repository's convention (signals 0..31 are
the inputs, gate `k` produces signal `32+k`) — exactly the two keys the artifact
repository's `circuits/` format carries, added here for the same reason. They are
*computed from the unchanged gate list*, they change no count and no depth, and
this repository's oracle ignores them (`verify_circuit.py` re-derives the outputs
from the GF(2⁸) spec and checks the mask set, so it re-verifies both files
byte-for-byte the same as before). The artifact repository's clean-room verifier,
which enforces an exact 8-key schema, scans only *its own* `circuits/` directory
and ships no copy of either imported circuit, so it is not affected.

## Verification (this repo's standalone oracle)

```
python3 ../../verify_circuit.py jean_88gates_depth7_eprint_2026-1481.json 7
    gates=88 depth=7 outputs_built=32/32 problems=0 ; depth<= 7: OK ; VERDICT: VALID MixColumns circuit

python3 ../../verify_circuit.py sunyangli_89gates_eprint_2025-1493.json
    gates=89 depth=9 outputs_built=32/32 problems=0 ; VERDICT: VALID MixColumns circuit
```

Jean's paper credits the discovery to a search run "with the help of OpenAI
codex" and gives no method and no depth claim. Sun–Yang–Li describe their method
(LCB-BP voting variant + MILP + graph-based local optimisation replacing
out-degree-1 subsequences).

## How they relate to this project's circuits

**Updated 2026-07-29** for the v3 release, which adds two more 88-gate circuits
of this project's own — the from-scratch **88 @ depth 6** and the **derived
88 @ depth 5** — both of which belong here. Every figure in the table was
recomputed on that date.

Mask overlap (mask set = the circuit's non-input signal values), measured with
this repo's oracle; the periphery column excludes the 32 obligatory target masks
that every valid circuit must contain:

| pair | shared masks | Jaccard | periphery-only J |
|---|---|---|---|
| **Jean 88 ↔ Sun–Yang–Li 89** *(baseline: two independent published works)* | **63** | **0.553** | 0.378 |
| Jean 88 ↔ **our 88@6** *(from scratch — the headline v3 circuit)* | **42 / 88** | **0.313** | **0.098** |
| Jean 88 ↔ **our 88@5** *(**derived**: its seed chain passes through this very circuit)* | 62 | 0.544 | 0.366 |
| Jean 88 ↔ **our 88@7** | 61 / 88 | 0.530 | 0.349 |
| Jean 88 ↔ **our 88@8 (third family, derived)** | 55 | 0.455 | 0.258 |
| Jean 88 ↔ our 89@5 record | 61 | 0.526 | 0.345 |
| Sun–Yang–Li 89 ↔ our 88@6 | 41 | 0.301 | 0.087 |
| Sun–Yang–Li 89 ↔ our 88@5 | 61 | 0.526 | 0.345 |
| Sun–Yang–Li 89 ↔ our 89@5 record | 59 | 0.496 | 0.310 |
| Sun–Yang–Li 89 ↔ our 88@7 | 61 | 0.526 | 0.345 |
| our 88@7 ↔ our 88@8 | 62 | 0.544 | 0.366 |

**The two v3 rows read in opposite directions, and that is the point.** The
88 @ depth 6 is the *least* similar circuit this project has ever produced to
either published one — 42 shared masks, and only **10 of the 56** off-target
masks it actually chose — which is what "from scratch" looks like when measured.
The 88 @ depth 5's 62 / 0.544 is not evidence of independence in the other
direction and is not offered as such: that circuit's seed chain *passes through
Jean's 88* (`../campaign87_run_2026-07-29_got_88at5_derived/PROVENANCE.md`), so
its overlap with Jean's circuit is expected, and it is reported as derived work
everywhere it appears.

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
circuit — it does not beat it. **As of the v3 release the 88@7 is itself
dominated**, not by anything published but by this project's own from-scratch
**88 @ depth 6**: same count, one level shallower. Jean's 88 @ depth 7 is
correspondingly no longer on this project's reported frontier either. Neither
statement touches the count: 88 is still Jean's, Jean still has priority, and
nothing here goes below it. Our 88@8 is a third distinct family, but its
*lineage* runs through Jean's circuit (see
`../campaign87_run_2026-07-27_got_88at8_thirdfamily/PROVENANCE.md`), so it is a
derived, not independent, construction.

## The measured depths are forced, not just observed

Both papers state a count and no depth, so the 7 and the 9 above are this
repository's measurements of *its own* transcriptions. That is the weakest form
of the claim, and it is worth stating the stronger one, because the 88 @ depth
6's domination of Jean's point depends on it: **neither circuit can be
rescheduled shallower.** Running `pipeline/engines.py:relax` over a transcribed
mask set returns the ASAP (least-fixpoint) build depth of every mask — the
shallowest depth *any* circuit on that mask set can achieve, independent of the
gate order in which it happens to be written down. On Jean's mask set three
output masks come out at depth 7; on Sun–Yang–Li's, one comes out at depth 9.

```
python3 -c "
import sys; sys.path[:0]=['../../pipeline','../..']
import mixcolumns_core as core, engines as E
from verify_circuit import mixcolumns_target_masks
T=set(mixcolumns_target_masks())
for f in ('jean_88gates_depth7_eprint_2026-1481.json',
          'sunyangli_89gates_eprint_2025-1493.json'):
    a=core.INPUTS+sorted(core.load_circuit_masks(f)-set(core.INPUTS))
    d,p=E.relax(a); print(f, 'ASAP depth =', max(d[p[m]] for m in T))"

jean_88gates_depth7_eprint_2026-1481.json ASAP depth = 7
sunyangli_89gates_eprint_2025-1493.json ASAP depth = 9
```

So the depths are properties of the published mask sets, not of our
transcription order: there is no shallower schedule to find. This check was
suggested and independently run by an external first-reader of the v3 release
and is reproduced here from this repository's own `relax`.

## Certificate subjects

Jean's 88 is the most heavily certified circuit in the project: exhaustive exact
k = 2 and k = 3 shells (empty), 32 685 exact k = 4 windows (all irreducible), and
48 windowed-SAT cone windows of which 44 are UNSAT (frontier k = 16, 4
undecided). See `../campaign87_certificates/CERTIFICATES.md`.
