# Patch plan — `~/xor_ui/aes_mc_records`

**Status: DRAFT FOR REVIEW. Nothing in the records repository has been edited,
committed or pushed.** Everything below was re-read against the current checkout
(`73ad7ee`, v3.1.0, 2026-07-30) on 2026-08-29; every line number quoted was
verified today, not copied forward.

Files staged in this directory, ready to copy in:

| staged file | goes to |
|---|---|
| `mixcolumns_91gates_depth4.json` | `circuits/mixcolumns_91gates_depth4.json` |
| `mixcolumns_91gates_depth4.txt` | `listings/mixcolumns_91gates_depth4.txt` |
| `README.md` | `README.md` (full replacement draft) |
| `stage_91at4.py` | *not shipped* — the staging/verification script, kept for audit |
| `VERIFY_TRANSCRIPT.txt` | *not shipped* — the transcript reproduced in §3 below |

**Sources for every number.** `wrapup/CONFLICTS_RESOLVED.md` PUBLIC-SAFE lines
(cited as `CR §<id>`), `wrapup/CORRECTIONS.md` (`CO C-nn`),
`wrapup/CORPUS88.md` (`CP §n`), `wrapup/MANIFEST.md` (`MF`),
`fleet7/laneCONSOLIDATE/RECORDS_REPO_PATCH.md` (`RP §n`),
`wrapup/reports/records_repo.md` (`BA §n`).

---

## Item 1 — push the unpushed commit

`73ad7ee` "Scope the certificate claims: rigidity results, not evidence about
87" is ahead of `origin/main` by 1 and touches `PRIOR_ART.md`, `README.md`,
`paper/mixcolumns_note.tex`. Until it is pushed, the public GitHub copy still
juxtaposes the empty neighbourhoods with "87 was not found" in exactly the way
that commit was written to prevent. (`CO C-05`, `BA §3A.12`.)

- **Do this first, on its own**, before any of the edits below, so the scope
  correction reaches the public copy even if the rest is deferred.
- **Also check:** `paper/mixcolumns_note.pdf` mtime is Jul 30 13:39, *earlier*
  than the commit at Jul 30 23:57 — the PDF was very likely never rebuilt from
  the amended `.tex`. Rebuild it before any release. (`CO C-05`; mtime ordering
  verified, the inference is an inference.)

---

## Item 2 — the 92 → 91 correction at depth 4

**The fact.** The verified depth frontier is **97 @ 3 / 91 @ 4 / 88 @ 5**. The
depth-4 point is a 91-gate depth-4 circuit, oracle-verified, held in three
independent lineages; it improves the published depth-4 point (97, Osvik &
Canright, ePrint 2024/1076 App. G) by **six** gates, not five. (`CR §B7`.)

**Two guards that must travel with the fix** (`CO C-02`):

1. **90 @ 4 is undecided, not refuted.** The exactness result behind 91 is
   relative to a fixed 227/300-mask vocabulary, and "exactly 90 iff W3(D=4) ≤ 11"
   was left in flight. **Never write "optimal at depth 4."**
2. **Do not add 108 @ 3.** A session note proposing it was retracted two lines
   later; 108 @ 3 is worse than the shipped 97 @ 3 and is not a frontier point.

### 2a. `README.md` — 3 sites

| line | current | change to |
|---|---|---|
| 8 | `possible depth), **92 at depth 4**, **88 at depth 5** — six gates below the` | `**91 at depth 4**` |
| 18 | `**Verified frontier: 97 @ 3, 92 @ 4, 88 @ 5 — one line, entirely this project's` | `97 @ 3, 91 @ 4, 88 @ 5` |
| 87 | table row `mixcolumns_92gates_depth4 \| 92 \| 4 \| 97 (Osvik and Canright…) \| improves it by 5` | **add a row above it** for `circuits/mixcolumns_91gates_depth4.json` \| 91 \| **4** \| same baseline \| `improves it by 6`; **retain** the 92 row, restated as `improves it by 5; superseded at its depth within this repository by the 91 above, and retained` |

Also line 6–7 (`Four are smaller than any published circuit at their own depth`):
the count of listed circuits changes and the sentence must move with it.
*The full-replacement `README.md` draft in this directory already handles all
four; use it instead if the rewrite is adopted.*

### 2b. `PAPER.md` — 6 sites to change, 2 not to

| line | current | change to |
|---|---|---|
| 14 | `**92-gate** circuit at depth **4**, improving the 97-gate depth-4 point of Osvik` | `**91-gate**`, and the margin stated nearby becomes **six** |
| 26 | `and kept for the record. **Verified frontier: 97 @ 3, 92 @ 4, 88 @ 5 — one line,` | `97 @ 3, 91 @ 4, 88 @ 5` |
| 44 | `frontiers reported on 2026-07-29 collapse into one**: 97 @ 3, 92 @ 4, 88 @ 5.` | `97 @ 3, 91 @ 4, 88 @ 5` — **judgement call**: this sentence sits inside a dated narrative about 2026-07-29; annotating may be better than rewriting (`RP §3.2`) |
| 89 | frontier-table row `mixcolumns_92gates_depth4 \| 92 \| 4 \| … \| improves it by 5 \| own` | **add** a `mixcolumns_91gates_depth4` row (`91 \| 4 \| 97 (same) \| improves it by 6 \| own`); keep the 92 row marked superseded |
| 97 | `One frontier follows: **97 @ 3, 92 @ 4, 88 @ 5**, every point of it on this` | `**97 @ 3, 91 @ 4, 88 @ 5**` |
| 182 | `- **Provenance.** 97 @ 3 and 92 @ 4 are from scratch; …` | `97 @ 3 and 91 @ 4 are from scratch` — **true only because the circuit chosen in §3 is the from-scratch cascade one** |

**Do not change:**

- **line 168** — `…92 @ depth 6 (Maximov)…` is the *published baseline* list. The
  92 there is Maximov's number. Editing it would be an error. (`RP §3.2`.)
- **line 192** — `dependency-free Python that reproduces 97 @ 3, 92 @ 4 and 89 @ 5`
  is a *reproducibility* claim about the shipped scripts. The depth-4 anchor was
  measured ending at 92 in **9 of 9** restarts and never reaching 91, so unless
  the shipped pipeline is re-run and shown to reach 91, **leave this line
  describing the 92**. (`CO C-06`, `RP §3.2`.)
- Related, also line 194 (`neither from-scratch 88 has a single-command
  reproduction`): a closed-form generator exists in the method repository that
  may change what this sentence should say. Not verified; flagged only, no edit
  proposed. (`CO C-06`.)

### 2c. `PRIOR_ART.md` — 4 standing claims + 1 new log entry

| line | current | change to |
|---|---|---|
| 12 | `claimed here — fewer than 97 at depth 3, 92 at depth 4, 88 at depth 5, 88 at` | `**91** at depth 4` — this is the **standing public invitation to report a better circuit**, so it currently sets the bar one gate too high |
| 225 | `four points: 97 @ 3 by 2 gates, 92 @ 4 by 5, 88 @ 5 by 6, 88 @ 6 by 4. It does` | `**91 @ 4 by 6**` |
| 254 | heading `## Claim 2: 92 gates at depth 4 improves the published depth-4 point (97)` | `## Claim 2: 91 gates at depth 4 …`, and restate the section body (254–268) for 91, keeping the 92 as its superseded predecessor |
| 266 | `**Conclusion:** circuits/mixcolumns_92gates_depth4.json uses five fewer gates` | `circuits/mixcolumns_91gates_depth4.json uses **six** fewer gates` |

**Leave as history — do not silently rewrite:** lines **55, 67, 90, 91, 98,
123, 142, 420**. Each sits inside a dated Corrections entry that was true when
written; the repository's own policy is to retain and annotate. Instead **add
one new dated Corrections entry at the top of §Corrections** recording the
92 → 91 supersession — which is also what makes those eight lines read correctly
as history. (`RP §3.3`.)

### 2d. `docs/frontier.svg` — regenerate, do not hand-edit

The SVG is generated by `scripts/generate_frontier_svg.py` and
`tests/test_verification.py` fails on drift. Edit the **generator**, then
regenerate:

- `scripts/generate_frontier_svg.py:59` — `(4, 92, "92", -10, 4, "end")` in this
  project's point list → `(4, 91, "91", …)`.
- `scripts/generate_frontier_svg.py:116` — the accessible description string
  `'…97 gates at depth 3, 92 at depth 4, 88 at depth 5…'` → 91.
- `scripts/generate_frontier_svg.py:12, 15, 20` — the header comment restating
  the frontier.
- **Do not touch line 50** — `(6, 92, "92 Max19", …)` is Maximov's published
  point.

Rendered result: `docs/frontier.svg` line 3 (the `<desc>` alt text) and the
drawn/labelled point at lines 12 and 59 must both end up saying 91. The alt text
and the image must not disagree. (`BA §3A.1`; hazard: generated files, `BA §6`.)

### 2e. `CITATION.cff` — see Item 6.

### 2f. `paper/mixcolumns_note.tex` + PDF

- **line 13** — title `97 Gates at Depth 3; 92 at Depth 4; 88 at Depth 5` → 91.
- **abstract (~line 19)** — `\textbf{92} at depth \textbf{4} against 97~\cite{OC24}`
  → 91, and the margin becomes six.
- **line 34** — `the frontier is one line, \textbf{97 @ 3, 92 @ 4, 88 @ 5}` → 91.
- **line 92** — `Our frontier is one line, 97 @ 3, 92 @ 4, 88 @ 5` → 91.
- **line 192** — `One frontier therefore: \textbf{97 @ 3, 92 @ 4, 88 @ 5}` → 91.
- **lines 397, 403** — reproduction timings and "the 92 at depth 4 … reproduced
  by the published method": **the same rule as `PAPER.md:192`** — leave
  describing the 92 unless re-measured.
- **line 462** — the v1 version history (`the 97, 92 and 89`) is **history,
  leave**.
- `paper/appendix_circuits.tex` is generated by `paper/generate_appendix.py` —
  regenerate, do not hand-edit.
- Rebuild `paper/mixcolumns_note.pdf` (see Item 1).

**Total 92 → 91 sites: 16** (README 3, PAPER 6, PRIOR_ART 4, `bounds.json` 1,
SVG generator + rendered alt text 1, CITATION title 1) plus the LaTeX note's
title and abstract, matching the enumeration in `CO C-02`.

---

## Item 3 — the depth-4 record circuit

### 3a. Which 91 was chosen, and why

Three verified 91 @ 4 circuits exist in three distinct lineages, pairwise
Jaccard 0.556 / 0.433 / 0.358 (`CR §B7`, `RP §1`). **Chosen:
`campaign_87/cascade6/FRONTIER_91gates_depth4.json`** from
`~/xor_ui/slp-plateau-search`.

- It is this project's own **from-scratch cascade lineage** — the same family as
  the 92 @ 4 it supersedes — so `PAPER.md:182` ("97 @ 3 and 92 @ 4 are from
  scratch") stays true after substitution with **no new provenance argument**.
- Its own JSON carries a provenance string: *"independent: cascade6, from
  scratch. Every root in this run is `constructors.build(name, seed)` or the
  anneal3 engine — a pure function of an integer. No circuit file, harvest,
  archive, repel mask or population from any other run entered this directory.
  Cross-pollination OFF."* `found_utc 2026-08-01T00:37:38Z`.
- The other two cost more (`RP §2`): the census 91 has **no `provenance`, no
  `depth`, no `verified` field** and would need all three written; the third is a
  reschedule of a depth-5-labelled file and would need its own provenance
  sentence explaining that.

### 3b. Schema conversion

The source file carries `gateCount, gates, depth, verified, cap, found_by_file,
found_utc, provenance` — it does **not** carry the records-repo schema keys
`id, model, inputCount, outputSignals, outputConvention`. `outputSignals` was
**derived**, not copied: `stage_91at4.py` rebuilds the 32 MixColumns target masks
from GF(2⁸) exactly as `verify.py` does, then locates the signal carrying each
target. All 32 were located uniquely.

The staged file is written with `json.dumps(..., indent=1)` and the key order
`id, model, inputCount, gateCount, depth, gates, outputSignals,
outputConvention` — byte-formatting matched to `circuits/mixcolumns_92gates_depth4.json`.

### 3c. Verification transcript

Staging + independent re-check (`python3 stage_91at4.py`, this directory):

~~~text
AES MixColumns rebuilt from GF(2^8): weight profile 20x5 + 12x7  [OK]
outputSignals derived: 32/32 targets located (min 80, max 122)
structural (2-input XOR, parents strictly earlier): OK
gateCount declared 91 == actual 91
depth declared 4 == measured 4
outputs correct: 32/32
live gates (reverse-reachable from outputs): 91/91
distinct gate masks: 91/91

sha256_circuit_json    = 883da457b3224916664f85ec12c1b940cab96c6632586a334709f375cb8cbf3d
sha256_canonical_gates = 9cf029f08ebc36848c94b2d9c8bbd51f2695737a9af4c976fb7c7f016ef283a7

ALL CHECKS PASS.
~~~

**Cross-check.** `9cf029f08ebc36848c94b2d9c8bbd51f2695737a9af4c976fb7c7f016ef283a7`
is byte-for-byte the canonical hash recorded for this circuit in `RP §1`,
computed there from the source file a week earlier by a different script. The
canonical hash survived the schema conversion and the reformatting, as designed.

**91/91 live and 91 distinct masks** together mean this is not a 90 with a dead
gate — the same check that was run over the whole depth-4 census (`CR §B7`).

Then the records repository's **own** `verify.py`, run unmodified over a
sandbox copy of `circuits/` plus the new file, with a `bounds.json` carrying the
new entry (read-only against the real repo; the sandbox is under the session
scratchpad):

~~~text
AES MixColumns rebuilt from GF(2^8): weight profile 20x5 + 12x7  [OK]

[ OK ] mixcolumns_88gates_depth5: 88 gates, depth 5 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_88gates_depth5_fromscratch: 88 gates, depth 5 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_88gates_depth6: 88 gates, depth 6 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_88gates_depth7: 88 gates, depth 7 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_88gates_depth8: 88 gates, depth 8 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_89gates_depth10: 89 gates, depth 10 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_89gates_depth5: 89 gates, depth 5 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_91gates_depth4: 91 gates, depth 4 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_91gates_depth6: 91 gates, depth 6 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_92gates_depth4: 92 gates, depth 4 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_97gates_depth3: 97 gates, depth 3 — all 32 outputs correct, SHA fields match
[ OK ] mixcolumns_98gates_depth3: 98 gates, depth 3 — all 32 outputs correct, SHA fields match

ALL CIRCUITS VERIFIED.
rc=0
~~~

**12/12 pass on the enlarged set.**

### 3d. Still to run before release (not run here — CPU is scarce)

- `python3 audit/cleanroom_verify.py --update-artifacts` — regenerates
  `audit/recomputed_metrics.json` and `audit/MATHEMATICAL_VERIFICATION.md`.
- `python3 scripts/generate_verilog.py` — the new circuit needs a netlist and a
  testbench like every other.
- `python3 scripts/generate_listings.py --check` — the staged
  `mixcolumns_91gates_depth4.txt` was produced by importing that script's own
  `render()`, so it should already match; confirm.
- `python3 scripts/reproduce_canonical_hashes.py --check-bounds`.
- `python3 -m pytest tests/` — 12 tests. Four exercise the happy path, eight are
  rejection/drift checks; `test_listings_match_artifacts` and
  `test_verilog_matches_artifacts` will fail until the two generators above have
  been re-run over the enlarged `circuits/`.
- `README.md:243` says `circuits/    eleven circuit JSON files` — becomes twelve
  (the full-replacement draft already says twelve).
- `python3 verify_all.py`.

**Hazard:** `sha256_circuit_json` is over the file bytes *as they land in the
records repo*. The value above is for the staged bytes in this directory; if
anything reformats the file on the way in, recompute it. (`RP §1`, `BA §6`.)

---

## Item 4 — `bounds.json`

### 4a. Add the 91 @ 4 entry

Insert immediately **before** the `mixcolumns_92gates_depth4` entry, which opens
at `bounds.json:77` (`"id"` on :78, `"claim"` on :93). Same schema, same key
order; the block below is shown at indent 1 — **re-indent to match the file**,
whose `circuits[]` entries are nested deeper.

~~~json
{
 "id": "mixcolumns_91gates_depth4",
 "inputCount": 32,
 "gateCount": 91,
 "depth": 4,
 "outputCount": 32,
 "outputConvention": "output j (j in 0..31) is MixColumns output bit j; bit j = bit (j mod 8) of state byte (j div 8), least-significant-bit-first within each byte. It is produced at internal signal index outputSignals[j].",
 "sha256_canonical_gates": "9cf029f08ebc36848c94b2d9c8bbd51f2695737a9af4c976fb7c7f016ef283a7",
 "sha256_circuit_json": "883da457b3224916664f85ec12c1b940cab96c6632586a334709f375cb8cbf3d",
 "verified": {
  "allOutputsCorrect": true,
  "everyGateIs2InputXOR": true,
  "everyParentIndexSmaller": true,
  "measuredDepth": 4,
  "method": "checked against AES MixColumns rebuilt from GF(2^8) in verify.py, and against 32 basis-vector responses in the Verilog testbench"
 },
 "provenance": "Own lineage, from scratch. Found 2026-08-01T00:37:38Z by the cascade search of the method repository, in a directory whose every root is a pure function of an integer seed; no circuit file, harvest, archive, repel mask or population from any other run entered it, and cross-pollination was off. Supersedes mixcolumns_92gates_depth4 at depth 4 within this repository; that circuit is retained.",
 "claim": "Uses six fewer 2-input XOR gates than the only published depth-4 AES MixColumns circuit we are aware of (97 gates: Osvik and Canright, ePrint 2024/1076, Appendix G); we do not make an optimality claim, and in particular 90 gates at depth 4 is undecided, not refuted."
}
~~~

`sha256_circuit_json` **must be recomputed** if the file bytes change on copy-in.
Re-verify `verified.measuredDepth` with the repo's own verifier after the copy.
Note this would make the 91 the sixth entry carrying a `provenance` string
(currently only the five 88s carry one) — that is a deliberate extension, since
a new frontier point earns one.

### 4b. Amend the 92 @ 4 entry — retain, never delete

`bounds.json:93`, the `claim` string, currently: *"Uses five fewer 2-input XOR
gates than the only published depth-4 AES MixColumns circuit we are aware of
(97 gates: Osvik and Canright, ePrint 2024/1076, Appendix G); we do not make an
optimality claim."*

**Append** a dated sentence, in the style the file already uses for the
superseded 89 and 88s:

> Updated 2026-08-29: superseded at its depth within this repository by
> `mixcolumns_91gates_depth4` (one fewer gate, same depth). It is retained, not
> withdrawn, and its original claim stands as made. It is not a dead-gate strip
> of the 91: all 92 of its gates are live.

(The 0-dead-gate check on the shipped 92 is `CR §B7`.)

### 4c. The lower bound

`bounds.json` has no lower-bound field of any kind today; the only lower bound
anywhere in the repository is the *depth* floor of 3. Two options, user's call:

- **Minimal:** add nothing to `bounds.json`; state `56 ≤ L(M) ≤ 88` in the prose
  only (the README draft does).
- **Fuller:** add a sibling top-level key beside `spec`, `note`, `circuits`:

~~~json
"bounds": {
 "gateCount": {
  "lower": 56,
  "upper": 88,
  "statement": "56 <= L(M) <= 88 for the minimum number of 2-input XOR gates computing AES MixColumns. Lower: an unconditional, refereed counting certificate at depth 4. Upper: the verified 88-gate circuits in this repository. We know of no published lower bound for this matrix.",
  "note": "The upper bound is 88, Jean's count (ePrint 2026/1481), who has priority. No optimality is claimed at either end."
 },
 "depth": {
  "lower": 3,
  "statement": "MixColumns has outputs depending on 7 inputs, so depth >= ceil(log2 7) = 3. Attained by mixcolumns_97gates_depth3."
 }
}
~~~

Source for the bracket: `MF §0` ("The bracket `56 <= L(M) <= 88`", lower from an
unconditional refereed certificate, upper from the verified 88s) and the
verbatim PUBLIC-SAFE certificate-scope line at `CR §C10`. **The certificate
itself is not shipped here** — if the bound is stated, either ship the
certificate or say plainly that it lives in the method repository.

---

## Item 5 — new results for `PAPER.md`

All of these go in `## 2. Results`, in the paragraph beginning *"Beyond the
circuits, the note reports machine-checked local certificates…"*
(`PAPER.md:137–151`). Register: the repo's own, short and factual.

### 5a. Corrections to figures already printed

**`PAPER.md:145–146` currently reads** *"105,801 of the ≈ 139,878 harvested
distinct 88-gate mask sets are proven irreducible at k = 2"*. Both halves are
wrong in the same direction — the sweep finished.

> Replace with: *"All 139,878 harvested distinct 88-gate mask sets are proven
> irreducible at k = 2: 215,412,120 exact window decisions, 1,540 windows each,
> zero reducible."*

Source `CR §S7`, which re-tallied three append-only progress ledgers whose key
sets are pairwise disjoint (84,989 + 987 + 53,902 = 139,878) and states
explicitly that **the "≈" must be dropped — 139,878 is exact** and that the
105,801 figure is a stale mid-run snapshot to be corrected **upward**.

**`PAPER.md:147–148` currently reads** *"≈ 165 million exact window decisions
returned zero reducible windows"*. That figure counts a different object from
the one above and is itself stale. It must **not** be summed with, or presented
as a revision of, the 215,412,120. `CR §D` marks it a stale under-count and says
to replace it with the k=2 figure and not to state a new grand total. Simplest
correct move: **delete the sentence**, since the replacement in 5a already
carries an exact decision count.

### 5b. Joint-level UNSATs

> *"For a merged 16-dimensional block that any 87-gate circuit must contain, no
> program of 9, 10, 11, 12 or 13 gates exists — all five levels UNSAT — so that
> block needs at least 14 gates. The levels at 9, 10 and 11 were re-proved
> independently with a second CNF encoding, 528 of 528 cubes UNSAT at each
> level, zero disagreements, and the encoding's positive control fired (a
> satisfiable cube with a checked witness), so the test can fail. The 14 case is
> undecided and running; as of 2026-08-29 08:27 −0400, 87 of its 528 cubes are
> proven UNSAT, 0 SAT, 441 open. That is a coverage bracket, not a refutation."*

Sources: `MF` rows 33/34 (the five UNSAT levels and the independent
cross-check); `CR §B8` for the k=14 tally, **which must always carry its
timestamp** — do not write a bare "87/528", and do not write "51/528" or
"73/528" at all, those are earlier samples of the same live run.

### 5c. The deletion regularity, and one-gate reduction

> *"Two population-scale negatives. First: deleting a gate from a valid 88-gate
> circuit yields an 87 only if that gate is redundant — a duplicated mask, or a
> non-output gate nothing consumes. Across 1,575,516 distinct verified 88-gate
> mask sets there is no duplicated mask, and all 28,796 that carry a build order
> have exactly 56 consumed non-output gates, the value that certifies neither
> defect. No 87 is available by deletion anywhere in that corpus. Second: for
> the verified 88 at depth 5, all 35,960 four-output-row drop sets were refuted
> at one gate fewer — no four output rows can be resynthesised from the rest of
> the circuit even one gate more cheaply. The same screen ran to completion on
> the from-scratch 88 at depth 5."*

Sources: `CP §4` (1,575,516 / 28,796 / B = 56 / zero alarms, and its own stated
gap — the consumer-less half is undecided for the 1,546,720 mask-only sets, so
do not claim it there); `CR §S11` for the 35,960 drop sets, **including its
explicit instruction not to extend the word "refuted" to the second circuit** —
the wording above says "screen ran to completion", which is what is banked.

### 5d. The scope sentence that must accompany all of it

Use verbatim (`CR §C10`), and keep it adjacent to the certificate paragraph:

> *"A negative at radius ≤ 4 carries no information about whether an 87 exists.
> These are locality theorems — rigidity statements about small, completely
> enumerated neighbourhoods — not bounds. By this instrument an optimal circuit
> and a four-gates-too-big circuit are indistinguishable. The honest bracket is
> 56 ≤ L(M) ≤ 88."*

This **extends**, and does not replace, the 2026-07-30 scope entry already in
the repo (commit `73ad7ee`), which is still exactly right and must not be
reverted (`BA §3A.D`).

### 5e. Two sentences to fix while in there

- **`PAPER.md:143–145`** says the derived 88 @ 5's k = 3 shell was *"never
  swept"* and that with the 88 @ 7 it is one of the two least-certified circuits
  here. A later 13-anchor exhaustive d3 pass may have closed this. **Whether
  those two circuits are among those 13 anchors could not be determined** —
  see §Unsourced below. Do not restate the sentence either way until checked.
- **`PAPER.md:148–150`**, the windowed-SAT sentence ("UNSAT to k = 16 and k = 15
  on two family anchors"), is correct and correctly hedged. Keep it, but the
  joint-level ladder in 5b is the stronger and independently cross-checked
  object; put 5b first.

---

## Item 6 — `CITATION.cff`

Three changes, one line each:

| field | current | proposed |
|---|---|---|
| `title` | `"Small 2-input XOR circuits for AES MixColumns (97 gates at depth 3; 92 at depth 4; …)"` | `92 at depth 4` → **`91 at depth 4`** |
| `version` | `"3.1.0"` | `"3.2.0"` |
| `date-released` | `2026-07-30` | the release date |

A **minor** bump (3.1.0 → 3.2.0) is right: a new verified circuit and a
corrected frontier point are new content, not a breaking reorganisation and not
a bug-fix.

**Identifiers block — needs a decision, not an edit.** The v3.0.0 entry is
described as historical *"because v3.1.0's own version DOI is minted when the
v3.1.0 release is published"*, and locally `git tag` shows **only `v1.0.0`**, so
it cannot be confirmed from here that v2.0.0 / v3.0.0 / v3.1.0 were ever tagged
in this checkout. Resolve before minting a v3.2.0 DOI, or the identifier list
will describe a release history the tags do not have. (`CO C-03`, `BA §3A.11`,
`BA §7`.) **Do not edit the existing DOI values** — they resolve to live Zenodo
depositions.

---

## Item 7 — do NOT touch

- **Any existing DOI value** in `CITATION.cff`. Concept DOI
  `10.5281/zenodo.21299092` and the version DOIs for v3.0.0, v2.0.0, v1.0.0
  resolve to live Zenodo depositions.
- **Any superseded circuit file.** The v1 archival three (98 @ 3, 91 @ 6,
  89 @ 10) are what the v1.0.0 deposition resolves to; the 88s at depths 7 and 8
  are in the v2.0.0 one. `mixcolumns_92gates_depth4.json` stays, amended not
  deleted. **Deleting a superseded circuit breaks an archived DOI.**
- **The two Jean-derived 88s.** Dominated but disclosed; withdrawing them would
  break the corrections ledger.
- **Every Jean-priority statement**, everywhere. Jean confirmed his priority
  directly in August. 88 stays flat and stays his.
- **The 88 count floor, and the 97 @ 3, 88 @ 5 and 88 @ 6 claims and margins.**
  Only depth 4 moves.
- **The forced-depth argument** for Jean (7) and Sun–Yang–Li (9).
- **The 2026-07-30 scope entry** on the remove-≤3 certificates (`73ad7ee`). Still
  exactly right; extend it, never revert it.
- **The dated-corrections policy.** Append entries; do not rewrite superseded
  text.
- **`PRIOR_ART.md` lines 55, 67, 90, 91, 98, 123, 142, 420** — dated history.
- **`PAPER.md:168`** — Maximov's published 92 @ 6.
- **`scripts/generate_frontier_svg.py:50`** — Maximov's published point.
- **Generated files, by hand:** `listings/*.txt`, `verilog/*.v`,
  `verilog/*_tb.v`, `docs/frontier.svg`, `audit/recomputed_metrics.json`,
  `audit/MATHEMATICAL_VERIFICATION.md`, `paper/appendix_circuits.tex`. Each has
  a generator with a `--check` mode and the test suite asserts the match — a
  hand edit becomes a CI failure. (`BA §6`.)
- **Never write "optimal at depth 4"** (Item 2 guard 1) and **never add 108 @ 3**
  (guard 2).

---

## Also on the record, and left out of this patch on purpose

Sourced and true, but not proposed for publication here — each is a decision the
patch does not need to make:

- **The literature-search cutoff (`PRIOR_ART.md:10`, 2026-07-23) is five weeks
  old** and no new sweep has been run. These sweeps have a demonstrated failure
  mode — a previous one corroborated a 91 floor while an 89 sat unseen on
  ePrint. Either re-run the sweep before release or move the date honestly.
  (`CO C-04`.)
- **Private correspondence** received 2026-08-10 bearing on the count floor is
  not cited in the README draft. Publishing another researcher's unpublished
  view needs their permission; that is the user's to seek, not this patch's to
  assume.
- **The stronger distinctness instrument.** All inter-circuit distinctness in
  the repo is mask-Jaccard with a 0.7 threshold; a stronger notion (the studied
  88s are pairwise-distinct closed orbits) exists and is unpublished. If it is
  ever published, two guards travel with it: the orbit tables partition the 88
  plateau and are **not** evidence about 87, and distinct orbit does not imply
  distinct frame. (`BA §3A.7`.)
- **`audit/MATHEMATICAL_VERIFICATION.md`'s per-circuit DAG statistics** (fanout
  maxima, layer histograms) are fine as *verifier output* but must not be
  presented as structural facts about the circuits — they are not invariants.
  (`BA §3A.8`.)

---

## Numeric claims I could not source

- **Whether the derived 88 @ 5 and the 88 @ 7 are among the 13 exhaustively
  swept d3 anchors** — this decides whether `PAPER.md:143–145` ("its k = 3 shell
  was never swept … the two least-certified circuits here") is now stale or
  still stands. Neither `CONFLICTS_RESOLVED.md`, `CORRECTIONS.md`, `CORPUS88.md`
  nor `MANIFEST.md` names the 13 anchors. **Left unedited**; §5e flags it.
- **A total core-hours or wall-clock figure** for the search behind "we think 88
  is optimal". No such figure exists in the sources, so the README draft's
  Opinion section makes no effort claim — it cites the 1.5 M distinct solutions
  instead, which is sourced (`CP` headline).
- **Whether v2.0.0 / v3.0.0 / v3.1.0 were ever tagged or released.** Locally only
  `v1.0.0` exists; confirming needs the remote. Item 6 defers rather than
  guesses.

---

## Post-draft addendum (2026-08-29, day-2 session)

**Item 8 (new, from the InvMixColumns prior-art research —
`wrapup/phase2/PRIOR_ART_INVMC.md`):** our PRIOR_ART.md labels Lin et al.
(CT-RSA 2021, the 91) as **s-XOR**, but two independent secondaries (Yuan et
al. ToSC 2024 Table 2 header; Shi-Feng-Xu ToSC 2023 Table 3) call it
**g-XOR**. The primary is paywalled. Before the next records release, either
resolve against the primary or add a footnote acknowledging the conflicting
secondary labels. This matters beyond bookkeeping: s-XOR programs invert
gate-for-gate (Beierle-Kranz-Leander CRYPTO 2016, Cor. 1), so the label
decides whether Lin's 91 also implies a 91 for InvMixColumns.
