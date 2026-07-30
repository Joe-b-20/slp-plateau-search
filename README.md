# slp-plateau-search

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21402996.svg)](https://doi.org/10.5281/zenodo.21402996)
[![verify](https://github.com/Joe-b-20/slp-plateau-search/actions/workflows/verify.yml/badge.svg)](https://github.com/Joe-b-20/slp-plateau-search/actions/workflows/verify.yml)

The search method and evidence behind this project's small 2-input XOR circuits
for AES MixColumns. Eight verified circuits, one frontier:

- **verified frontier: 97 @ 3, 92 @ 4, 88 @ 5 — one line, entirely this project's
  own lineage, with no imported material.**

**87 was not found**, and nothing here is claimed optimal.

- **97 @ 3 and 92 @ 4** improve the published depth–count Pareto frontier at
  their depth (99 @ 3, Shi–Feng–Xu ToSC 2023; 97 @ 4, Osvik–Canright ePrint
  2024/1076), and the depth-5 point improves the published 94 @ 5 (Osvik–Canright)
  by six gates. Our own **89 @ 5** improved it by five and is now superseded there
  by the 88 @ 5 below.
- **88 is not our count.** It is the published best-known count, held by Jean
  (ePrint 2026/1481, posted 2026-07-23), and **Jean has priority**. Our **88 @ 7**
  reaches it from a different direction — it **matches** that circuit with an
  independent one, the two sharing 61 of their 88 masks — rather than beating it.
  (Depth 7 is our measurement of our transcription; the paper states no depth.)
- What is new here is **depth at 88 gates, reached from scratch**. Until
  2026-07-30 the depth-5 point was held only by a circuit whose seed chain ran
  through Jean's published work. It is now held by **88 @ depth 5 found from
  scratch** — root `constructors.build("naive", 1958)`, a randomized XOR tree over
  the 32 raw inputs, with a producing engine that reads nothing from disk. **This
  removes this project's dependence on that circuit at the depth-5 point; it does
  not beat it.** The collapse of the two frontiers into one is about our
  provenance, not about his result. That circuit dominates Jean's 88 @ 7 (equal
  count, two levels shallower — and that depth 7 is *forced*: the shallowest
  schedule Jean's own mask set admits is still 7), improves on the published
  94 @ 5 by six gates, and dominates our own **88 @ 6** (also from scratch, a
  different family, and still the first 88 this project found that way),
  **88 @ 7**, **88 @ 8** and **89 @ 5**. The **derived 88 @ depth 5** and the
  **derived 88 @ depth 8** are retained, not deleted, and keep their
  first-sentence derived disclosure.
- Also published at unconstrained depth: 89 at unstated depth (Sun–Yang–Li,
  ePrint 2025/1493). Neither published point dominates any point of the frontier
  above — see the artifact repository's `PRIOR_ART.md`, including its Corrections
  section.

![The published depth–count Pareto frontier for AES MixColumns vs this work: 97 at depth 3, 92 at depth 4 and an 88 at depth 5 found from scratch, which is the depth-5 point; a derived 88 at the same depth-5 point, an 89 at depth 5, an 88 at depth 6 also found from scratch, the 88 at depth 7 that ties the published record with an independent circuit, and the derived 88 at depth 8, all dominated](docs/frontier.svg)

All eight verified circuits are in `evidence/circuits/`, hash-pinned in
`evidence/circuits/spectrum.json`; all eight also live, **gate-for-gate
identical**, in the artifact repository —
**[aes-mixcolumns-xor-circuits](https://github.com/Joe-b-20/aes-mixcolumns-xor-circuits)**
— as static, machine-checkable files with self-contained verifiers. That
repository ships eleven circuits in all: these eight, plus three superseded
earlier results of this project (98 @ 3, 91 @ 6, 89 @ 10) kept there for the
archival record and not carried here. This
repository is the other half: the **method** (a value-set
shortest-linear-program search with plateau walking and destroy-rebuild moves —
see [`METHODS.md`](METHODS.md); the remove-2-add-1 "hub" move that named this
repository is retained but **measured dead at the frontier**, METHODS.md §8),
the **pipeline** that ran it, and the **evidence** of the runs that produced
the records, archived untouched with their exact code and logs.

Everything is dependency-free Python 3 (stdlib only).

## Quickstart

Reproduce the records (all searches are stochastic — times are what the
archived and re-validation runs took, not guarantees):

```text
# 97 gates @ depth 3 -- from scratch, single core, single file. Took 60-156 s
# across our runs (RNG seed 6), 81 s re-validated 2026-07-27; it restarts on
# further seeds until it hits 97 or its 15 min budget:
cd reproduce && python3 reproduce.py

# 88 gates @ depth 7 -- one worker of the shipped pipeline on the record's own
# ρ²-symmetric 94-gate seed, stopping itself at 88 @ depth <= 7. 19.4 min
# re-validated 2026-07-27 with the shipped stop rule; 32.9 min in the
# archived run:
cd reproduce && python3 hunt_88.py

# 89 gates @ depth 5 -- the two-worker sub-89 configuration, warm-started from
# this project's 89@depth6 and 90@depth5 circuits. 592 s (~10 min) in the
# archived run on the v1 engine; the shipped v2 engine re-found it 0.3 s into
# its first chunk, the command returning in 19-22 s (re-validated 2026-07-27):
cd pipeline && python3 ladder_parallel.py --mode fixed --workers sub89 --stop-gates 89 --stop-depth 5

# 92 gates @ depth 4 -- the from-scratch cascade ladder (the archived run
# reached 92@4 after ~2.7 h; expect hours):
cd pipeline && python3 ladder_parallel.py --mode cascade --stop-gates 92 --stop-depth 4
```

[`reproduce/README.md`](reproduce/README.md) says what does and does not
reproduce. Four circuits have no single reproduction command: the **88 @ depth 8**
and the **derived 88 @ depth 5**, for the provenance reason above (neither should
be handed out as a recipe), and the two from-scratch circuits — the **88 @ depth
6** and the **88 @ depth 5** — which came out of a multi-day 16-process fleet, on
restart 18 and on session 5 restart 16 of the same worker. Their roots are exactly
reproducible (`constructors.build("naive", 2163)` and `…, 1958)`); their descents
are not, and what those took is archived, not promised. The lineage and the exact
worker, seed, iteration and wall-clock of
every record are in [`evidence/RESULTS.md`](evidence/RESULTS.md); the runs
themselves are archived under `evidence/campaign87_run_*/` with their code.

Verify any circuit against MixColumns rebuilt from GF(2⁸) — pass a path to a
circuit JSON (`{"gates": [[a,b], ...]}` index pairs, signals 0..31 = inputs,
gate k → signal 32+k; run with no arguments for all accepted encodings), plus
an optional depth bound:

```text
python3 verify_circuit.py evidence/circuits/mixcolumns_88gates_depth5_fromscratch.json 5
python3 verify_circuit.py evidence/circuits/mixcolumns_88gates_depth5_fromscratch.json 4   # INVALID: the depth is tight
python3 verify_circuit.py evidence/circuits/mixcolumns_89gates_depth5.json 5
python3 verify_circuit.py evidence/circuits/mixcolumns_88gates_depth6.json 6
python3 verify_circuit.py reproduce/out_97.json 3   # after running reproduce/reproduce.py
```

## Layout

| path | what it is |
|---|---|
| [`METHODS.md`](METHODS.md) | the method: value-set representation, moves, engines, kernel, pipeline, exact neighbourhood certificates, symmetry, provenance |
| `reproduce/` | single-command reproductions: the from-scratch depth-3 record (97 gates, single core) and a single-worker re-run of the 88 @ depth 7 (`hunt_88.py`), plus opt-in legacy demonstrations of the moves with per-method seed provenance |
| `pipeline/` | the record hunter: coordinator (`ladder_parallel.py`), workers, engines, the record-producing configurations — including the `--workers hunt87` set that puts an uncapped worker on each of the three 88-gate family anchors it ships (**two of those three anchors stand on Jean's published circuit**, so anything those workers produce is derived work — see `pipeline/README.md` and `pipeline/seeds/README.md`) — and the code-evolution history across the record runs |
| `evidence/` | `RESULTS.md` (the records + full lineage), `circuits/` (all eight verified circuits, SHA-256 in `spectrum.json`), and the record-producing run archives, untouched: logs, statuses, every verified best, and the exact `code/` that produced each. **What "untouched" covers** is that run material — the logs, statuses, bests and `code/` are never edited or regenerated, and each stays byte-identical to what the run produced. An archive's own `PROVENANCE.md` is its commentary, not run data, and is maintained: a later result can add a **dated** supersession note, strengthen an argument, repair a `RESULTS.md` cross-reference, or correct a sentence that has since become false. Every such change is recorded in a dated note at the top of the file it touches, and no claim is withdrawn without saying so |
| `evidence/campaign87_run_2026-07-26_got_88at7/` | the run that found the 88 @ depth 7: `PROVENANCE.md`, the record and its ρ²-symmetric 94 seed, every worker's log and best, the diverse-88 portfolio, and the exact `code/` |
| `evidence/campaign87_run_2026-07-27_got_88at8_thirdfamily/` | the run that found the 88 @ depth 8: same shape, plus the third-family representatives and census references; its `PROVENANCE.md` opens with the derived lineage |
| `evidence/campaign87_run_2026-07-28_got_88at6_fromscratch/` | the run that found the 88 @ depth 6 **from scratch**: `PROVENANCE.md` (leading with the root, which reads nothing, then the contamination vectors checked in the archived code), the record, the worker's untouched log, the exact `code/` including the root constructors, and `certificates/` — its exhaustively empty k ≤ 3 shell |
| `evidence/campaign87_run_2026-07-29_got_88at5_derived/` | the run that found the **derived** 88 @ depth 5: same shape; its `PROVENANCE.md` **opens with the derived lineage** through Jean's published 88, the seed is archived beside the record, and `certificates/` holds its k = 2 shell. Superseded at its Pareto point by the row below, and kept |
| `evidence/campaign87_run_2026-07-30_got_88at5_fromscratch/` | the run that found the **frontier** 88 @ depth 5 **from scratch**: `PROVENANCE.md` (the root, the five closed contamination vectors, and four corroborations a sceptic can check — including that the published 88 @ depth 6 log is a *byte-exact prefix* of this one), the record, the worker's untouched log, `certificates/` (exhaustively empty k ≤ 3 shell + the 135-member depth-5 pocket), and a `code/` that **hash-pins** rather than duplicates: its five source files are byte-identical to the 88 @ depth 6 archive's |
| `evidence/campaign87_certificates/` | `CERTIFICATES.md` and the machine-checked verdict summaries behind it: exhaustive k ≤ 3 shells for 47 canonical 88s, the population sweeps, the windowed-SAT runs (evidence, not proof), and the two exactly ρ²-symmetric 90-gate circuits |
| `evidence/campaign87_imported_prior_art/` | the published circuits, transcribed, oracle-verified and credited — **never ours**: Jean's 88 @ depth 7 (ePrint 2026/1481) and Sun–Yang–Li's 89 (ePrint 2025/1493) |
| `verify_circuit.py` | standalone GF(2⁸) oracle: `python3 verify_circuit.py <circuit.json> [max_depth]` |

## The three own-lineage chains

![Three lineages: the from-scratch 97-gate depth-3 circuit laddered down to the 89 @ depth 5 and on to the 88 @ depth 7; a second, independent chain from a random 139-gate construction to the 88 @ depth 6; and a third, also independent, from a random 146-gate construction to the frontier 88 @ depth 5](docs/lineage.svg)

All three chains above are this project's own, and the lower two start from
nothing but a random construction — the third of them is the frontier's depth-5
point. Full lineage tables for every record — each step with the run-time and
wall-clock at which it appeared, and the derived chains of the 88 @ depth 8 and
the derived 88 @ depth 5 spelled out link by link — are in
[`evidence/RESULTS.md`](evidence/RESULTS.md).

## Verification chain

Nothing in this repository asks to be trusted. Every claimed circuit is a
JSON gate list; `verify_circuit.py` rebuilds the AES MixColumns specification
from the GF(2⁸) definition (FIPS 197, polynomial `0x11b`, column `[2,3,1,1]`)
and replays the circuit against it. The engines themselves never claim a
count — every candidate passes the oracle before it is saved or logged
(verify-before-claim), and the run archives in `evidence/` let you re-check
every intermediate best ever recorded.

The same discipline applies to provenance: circuits from the literature are
kept apart from ours, credited by author and ePrint number, and a result whose
seed chain runs through published work says so in its first sentence. Negative
results are graded the same way — the exact window enumerations in
`evidence/campaign87_certificates/` are proofs for exactly the radius they
cover, while the windowed-SAT UNSATs are evidence only, holding relative to the
encoding's fixed slot order. Nothing here bounds an 87-gate circuit away.

## License / citation

MIT. Release **v3.1.0** (2026-07-30) adds an eighth circuit — an **88 @ depth 5
found from scratch**, with its run archive and its exhaustively empty k ≤ 3 shell
— which collapses the two frontiers of v3.0.0 into one that carries no imported
material. v3.0.0 (2026-07-29) added the 88 @ depth 6 found from scratch and the
derived 88 @ depth 5 to the 97/92/89/88@7/88@8 of v2. If you use the method or
the circuits, please cite this
repository and the artifact repository (see `CITATION.cff`). The accompanying
note is published with the artifacts:
[`paper/mixcolumns_note.pdf`](https://github.com/Joe-b-20/aes-mixcolumns-xor-circuits/blob/main/paper/mixcolumns_note.pdf),
archived under DOI
[10.5281/zenodo.21299092](https://doi.org/10.5281/zenodo.21299092).
