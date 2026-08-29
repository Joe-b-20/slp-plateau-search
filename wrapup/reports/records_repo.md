# Slice report: records_repo (`~/xor_ui/aes_mc_records`)

Agent model: Opus 5 (1M). Date: 2026-08-29. Slice read-only; one file written (this one).

**Summary.** `~/xor_ui/aes_mc_records` is the small (956 KB, 68 tracked files, 30
commits) outward-facing DOI'd artifact repository for this problem. It ships
**11 verified circuit JSON files** (5 of them 88-gate), each mirrored as a plain-text
listing, a Verilog netlist and a Verilog testbench, plus `bounds.json` (11 annotated
entries, 5 with full provenance strings), two independent Python verifiers, a
12-test regression suite, a CI workflow, and an ePrint note in Markdown and LaTeX/PDF.
I re-ran `python3 verify.py`: **all 11 circuits pass, `ALL CIRCUITS VERIFIED`, rc 0**.
The prose is heavy — README 295 lines / 2,686 words, PAPER.md 252 / 2,770,
PRIOR_ART.md 488 / 4,873, `bounds.json` carrying paragraph-long `claim` and
`provenance` strings (the from-scratch 88 @ 5 alone has a ~1,400-word provenance
plus a ~600-word claim). Everything is dated **2026-07-30 / v3.1.0**, and there is
**one unpushed commit (`73ad7ee`)** — so the public GitHub copy is one commit
*behind* even this state. The repository's substantive content is accurate as of
2026-07-30 and nothing in it is *false* except one figure: **it states the depth-4
frontier point as 92 when this project holds three verified 91 @ 4 circuits** (a
patch with exact line numbers already exists, written 2026-08-24). Beyond that
single error, the whole August body of work — the unconditional lower bound
`56 <= L(M)`, the joint-level UNSATs k=9..13, the B=56 tripwire theorem swept over
17,283/17,283 distinct 88s, the closed free-move orbits, the Anatomy Theorem, the
certificate-LP cap 91.4098776 — is **absent, not contradicted**. This is a repo
whose claims are narrower than the project's current knowledge, in every direction
but one.

---

## 1. INVENTORY

`du -sh --exclude=.git .` → **956K**. Per subdir (`du -sh <dir>`):

| path | size | what it IS | documented? |
|---|---|---|---|
| `circuits/` | 48K | 11 circuit JSON files, the primary artifacts. 8-key schema: `id, model, inputCount, gateCount, depth, gates, outputSignals, outputConvention`. No provenance in the JSON by design (it lives in `bounds.json`) | described in README + `bounds.json` |
| `listings/` | 48K | 11 `.txt` human-readable listings (`s32 = s15 ^ s23`, one gate per line). **Generated** by `scripts/generate_listings.py` | header comment + README |
| `verilog/` | 148K | 11 netlists + 11 testbenches, **generated** by `scripts/generate_verilog.py` (has a `--check` drift mode). Plus `sim.vvp`, a 50K gitignored iverilog build output | README §Hardware |
| `audit/` | 188K | `cleanroom_verify.py` (716 lines, independent verifier), `recomputed_metrics.json` (60K, generated), `MATHEMATICAL_VERIFICATION.md` (239 lines, generated). 80K of that is `__pycache__` | self-describing; generated headers say so |
| `paper/` | 212K | `mixcolumns_note.tex` (537 lines, 6 `\section`s), `appendix_circuits.tex` (812 lines, auto-generated), `generate_appendix.py` (126), `mixcolumns_note.pdf` (135K, dated 30 July 2026, "version 3.1") | yes |
| `scripts/` | 60K | 4 generators: `generate_listings.py` (70), `generate_verilog.py` (123), `generate_frontier_svg.py` (239), `reproduce_canonical_hashes.py` (88) | yes |
| `tests/` | 44K | one file, `test_verification.py`, 12 tests (`grep -c 'def test'`) — 4 happy-path, 8 rejection/drift | yes |
| `docs/` | 16K | `frontier.svg` only — the depth–count Pareto chart, **generated**, with a long embedded accessible description that restates the frontier claim in prose | generated |
| `.github/` | 12K | one workflow, `verify.yml` (24 lines) | — |
| root | — | `README.md` 295 L, `PAPER.md` 252 L, `PRIOR_ART.md` 488 L, `bounds.json` 209 L, `CITATION.cff` 30 L, `LICENSE`, `verify.py` 178 L, `verify_all.py` 51 L, `verify_verilog.py` 94 L | heavily |

**The 11 circuits** (from `bounds.json` + filenames; all re-verified by me today):

| file | gates | depth | family / lineage | verified how |
|---|---|---|---|---|
| `mixcolumns_97gates_depth3.json` | 97 | 3 | own, from scratch | `verify.py` (GF(2⁸) rebuild) + `cleanroom_verify.py` (independent byte-level ref, 100,000 deterministic random trials, symbolic output comparison) + Verilog testbench (32 basis vectors) + 2 SHA-256 fields |
| `mixcolumns_92gates_depth4.json` | 92 | 4 | own, from scratch | same |
| `mixcolumns_89gates_depth5.json` | 89 | 5 | own lineage (rooted in the from-scratch 97 @ 3) | same |
| `mixcolumns_88gates_depth5_fromscratch.json` | 88 | 5 | own, from scratch — root `constructors.build("naive", 1958)` | same |
| `mixcolumns_88gates_depth5.json` | 88 | 5 | **DERIVED from Jean's 88** (chain in `bounds.json`) | same |
| `mixcolumns_88gates_depth6.json` | 88 | 6 | own, from scratch — root `naive#2163` | same |
| `mixcolumns_88gates_depth7.json` | 88 | 7 | own lineage; independent match of Jean's point | same |
| `mixcolumns_88gates_depth8.json` | 88 | 8 | **DERIVED from Jean's 88** | same |
| `mixcolumns_98gates_depth3.json` | 98 | 3 | v1 archival, provenance not fully reconstructable | same |
| `mixcolumns_91gates_depth6.json` | 91 | 6 | v1 archival | same |
| `mixcolumns_89gates_depth10.json` | 89 | 10 | v1 archival | same |

**What the prose currently CLAIMS.** All four documents agree, deliberately:

- **Frontier: 97 @ 3, 92 @ 4, 88 @ 5** — "one line, entirely this project's own
  lineage, with no imported material". README:18, PAPER.md:26 and :97,
  PRIOR_ART.md:55 and :420, `docs/frontier.svg` (drawn *and* in its alt text),
  `CITATION.cff` title string, the note's LaTeX title.
- **88 is Jean's count and Jean has priority** — repeated in every document,
  many times over. Nothing here claims a new gate count.
- **Improvement margins vs published**: 97 @ 3 by 2 (vs Shi–Feng–Xu 99),
  92 @ 4 by 5 (vs Osvik–Canright 97), 88 @ 5 by 6 (vs Osvik–Canright 94),
  88 @ 6 by 4 (vs Maximov 92).
- **Published depths for Jean (7) and Sun–Yang–Li (9) are this project's own
  measurements of its own transcriptions**, and are **forced** — the ASAP
  least-fixpoint schedule over each published mask set still returns 7 and 9
  (PRIOR_ART.md:205–221). This caveat is spelled out once and cross-referenced
  everywhere.
- **No lower bound is stated anywhere.** The only lower-bound statement in the
  repository is the *depth* bound: depth 3 is minimum because outputs have
  weight 7 (`audit/MATHEMATICAL_VERIFICATION.md` §Depth lower bound; README:142).
  On gate count the repo says only "SLP is NP-hard; we prove nothing minimal".
- **"87 was not found" is scoped as a statement about a search** — README claim 6,
  PRIOR_ART.md Corrections 2026-07-30, PAPER.md §2 closing. That scoping (commit
  `73ad7ee`) is the newest content in the repo and is *still correct*.
- **Certificate claims** (PAPER.md:137–151): 47 canonical 88s with exhaustively
  empty remove-≤3 shells; both from-scratch 88s likewise (all 1,540 k=2 and all
  27,720 k=3 windows); the **derived** 88 @ 5's k=3 shell **never swept**;
  105,801 of ≈139,878 harvested distinct 88-gate mask sets irreducible at k=2;
  ≈165 million exact window decisions, zero reducible; windowed SAT UNSAT to
  k=16 / k=15 on two family anchors.
- **Literature-search cutoff: 2026-07-23** (PRIOR_ART.md:10), with an explicit
  standing invitation to open an issue if anything published beats
  "97 at depth 3, 92 at depth 4, 88 at depth 5, 88 at depth 6, or fewer than 88
  at any depth".
- `bounds.json` per circuit: `inputCount, gateCount, depth, outputCount,
  outputConvention, sha256_canonical_gates, sha256_circuit_json, verified{},
  claim`, plus `provenance` on the 5 88-gate entries only. Superseded claims are
  **appended to, never rewritten** ("Updated 2026-07-29: …", "Updated 2026-07-30: …").

**Opaque vs documented.** Nothing here is opaque. Every generated file names its
generator in a header; every claim in `bounds.json` carries its own supersession
log; `PRIOR_ART.md` is a dated corrections ledger. If anything, the ratio is
inverted from the rest of the tree: this slice is ~10,300 words of prose guarding
11 small JSON files.

---

## 2. METHODS

This slice contains no search method. It contains **verification, integrity and
comparison** methods, all of which are directly reusable for `aes_inv_mixcolumns`.

### spec-rebuild-verify
- **Family:** verification / artifact checking.
- **What it does:** rebuilds the 32×32 GF(2) MixColumns target from the GF(2⁸)
  definition (polynomial `0x11b`, column `[2,3,1,1]`, FIPS-197 §5.1.3 Eq. 5.6),
  then evaluates the circuit on the 32 unit-input vectors and compares. Because
  the map is linear, agreement on the basis is a complete correctness check.
  Also rechecks declared gate count, declared depth, DAG order, and both SHA-256
  fields against `bounds.json`.
- **Twist vs siblings:** it is the *lightweight* path — one file, no dependencies,
  178 lines; the specification is executable rather than prose.
- **Measured performance:** run today, 11/11 pass, `ALL CIRCUITS VERIFIED`, rc 0,
  under a second. It is also the gate for CI (`.github/workflows/verify.yml`).
- **Cost:** negligible (sub-second, one core).
- **Code:** `verify.py`.
- **Logs/results:** none persisted; `bounds.json:verified{}` is the banked form.
- **Generality:** MIXED. The circuit machinery is CIRCUIT-GENERIC; the target
  generator is MC-HARDCODED. To aim it at `aes_inv_mixcolumns`, replace the
  `[2,3,1,1]` column with `[14,11,13,9]` — one constant.
- **Phase-2 verdict:** keeper. This is the cheapest correct oracle in the whole
  project and the template every public artifact should ship with.

### cleanroom-verify
- **Family:** verification / adversarial checking.
- **What it does:** a second, independently written verifier that never calls
  `verify.py`. Rebuilds MixColumns from a *byte-level* reference (not a mask
  table), does a symbolic output comparison, executes 100,000 deterministic
  random inputs against the byte reference, recomputes gate/depth/fanout/layer
  metrics, and runs a suite of adversarial mutations that must be rejected.
- **Twist vs siblings:** the adversarial suite. 14 planted-defect cases, each
  confirmed rejected: reversed byte order, reversed bit order, transposed matrix,
  *inverse* MixColumns matrix, corrupted target mask, permuted output bindings,
  removed gate, modified parent pair, duplicated intermediate + dead gate,
  appended dead gate, wrong depth metadata, wrong gateCount metadata, missing
  field, forward reference. This is the only place in the project I saw a
  verifier's *negative* capability certified rather than assumed.
- **Measured performance:** 11/11 circuits clean, "Issues: none" on every one;
  14/14 adversarial cases rejected as expected
  (`audit/MATHEMATICAL_VERIFICATION.md` §Adversarial tests).
- **Cost:** 100,000 trials × 11 circuits; seconds to low minutes. Not re-run by me
  (CPU is scarce).
- **Code:** `audit/cleanroom_verify.py` (716 lines).
- **Logs/results:** `audit/recomputed_metrics.json` (60K, keys
  `generated_utc, reference_convention, depth_lower_bound, circuits,
  adversarial_tests, tool_availability`), `audit/MATHEMATICAL_VERIFICATION.md`.
  Both are generated, diffed against the tracked copies on every run, and only
  rewritten under `--update-artifacts` — so verifying leaves the tree clean.
- **Generality:** MIXED, same one-constant change as above. The adversarial
  suite is fully CIRCUIT-GENERIC.
- **Phase-2 verdict:** keeper — and the adversarial-rejection idea is the part
  worth porting first, since it is what makes a "VALID" verdict mean something.

### verilog-simulation-crosscheck
- **Family:** verification / third path.
- **What it does:** emits a Verilog netlist and a testbench per circuit; the
  testbench drives each unit input `e_i` and compares the output word against
  **column** `i` of the MixColumns matrix (not row `T[j]` — the matrix is not
  symmetric, and an early commit `5ecfdb5` records this exact bug being fixed).
  Expected responses come from the GF(2⁸) spec, not from the circuit.
- **Twist vs siblings:** a different language and a different simulator, so it
  catches Python-side convention errors that both Python verifiers would share.
- **Measured performance:** "Icarus Verilog was available; the testbenches are
  exercised separately" (`MATHEMATICAL_VERIFICATION.md` §Tool availability);
  `tests/test_verification.py::test_verilog_path` gates it in CI when present.
- **Cost:** seconds. Not re-run by me.
- **Code:** `scripts/generate_verilog.py` (generator, with `--check` drift mode),
  `verify_verilog.py` (runner).
- **Logs/results:** `verilog/` (22 tracked files), `verilog/sim.vvp` (build output).
- **Generality:** MIXED — same target-constant change.
- **Phase-2 verdict:** keeper, low priority. Its value is convention insurance,
  not throughput.

### canonical-gate-hash
- **Family:** artifact integrity / identity.
- **What it does:** defines a circuit's identity as SHA-256 over the UTF-8 bytes
  of the compact JSON string `{"inputCount":32,"gates":[...]}` with keys in that
  order — a formatting-independent fingerprint — alongside a plain file-bytes
  hash. Both are recorded in `bounds.json` and rechecked by both verifiers.
- **Twist vs siblings:** the *two-hash* discipline. The canonical hash survives
  re-formatting; the file hash does not. `RECORDS_REPO_PATCH.md` §1 shows this
  earning its keep: the 92 @ 4's canonical hash matches byte-for-byte between the
  two repositories while its file hash does not, because the repos hold
  differently pretty-printed copies of the same circuit.
- **Measured performance:** 11/11 hash fields match on today's run.
- **Cost:** negligible.
- **Code:** `scripts/reproduce_canonical_hashes.py` (`--check-bounds` mode).
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** keeper. Adopt the convention verbatim for any new repo.

### generated-artifact-drift-check
- **Family:** repository hygiene.
- **What it does:** every derived file (listings, Verilog, audit reports) has a
  `--check` mode that fails if the file on disk has drifted from the JSON
  artifact it was generated from; `tests/test_verification.py` asserts all of
  them.
- **Twist vs siblings:** it makes hand-editing a generated file a *test failure*
  rather than a silent inconsistency — the exact failure mode a rewrite of this
  repo is most likely to hit.
- **Measured performance:** 12 tests, 4 happy-path + 8 rejection/drift
  (`test_rejects_wrong_gatecount`, `_missing_output_signals`, `_forward_reference`,
  `_dead_gate`, `_wrong_depth`, `_permuted_outputs`, `test_listings_match_artifacts`,
  `test_verilog_matches_artifacts`). Not re-run by me.
- **Code:** `tests/test_verification.py`, plus `--check` in the two generators.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** keeper.

### asap-depth-forcing (claim lives here; implementation is in the method repo)
- **Family:** structural analysis.
- **What it does:** computes the ASAP (least-fixpoint) schedule over a *mask set*
  — the shallowest depth any circuit on that mask set can have, independent of
  the order gates happen to be written in. Applied to published circuits it turns
  "the depth we measured on our transcription" into "the depth that mask set is
  forced to have".
- **Twist vs siblings:** it converts a transcription-dependent observation into a
  transcription-independent one. This is what lets the repo claim its 88 @ 5
  *dominates* Jean's 88 without that claim resting on how the repo transcribed
  Jean's listing.
- **Measured performance:** Jean's mask set → depth 7 forced (3 of 32 output bits
  at 7); Sun–Yang–Li's → 9 forced; this repo's from-scratch 88 @ 5 → depth 5
  forced (11 of 32 output bits, rows 1,7,12,13,17,18,21,25,27,28,31); the 88 @ 6
  → rows 1/11/17/25. Three distinct depth-obstruction patterns.
  (PRIOR_ART.md:205–221, :424–426; PAPER.md:128–135.)
- **Cost:** trivial; it is a fixpoint over a mask set.
- **Code:** `engines.py:relax` in `slp-plateau-search`; run recorded in that
  repo's `evidence/campaign87_imported_prior_art/PROVENANCE.md`. Not implemented
  in this slice.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** keeper. It is cheap, it is the only depth argument here
  that is a theorem rather than a measurement, and it was contributed by an
  *external first-reader* — worth remembering as evidence that publishing early
  bought a real result.

### mask-jaccard-family-test
- **Family:** structural analysis / distinctness.
- **What it does:** measures the overlap of two circuits' internal mask sets and
  reports shared count + Jaccard; a threshold of **0.7** is used repo-wide for
  "same family".
- **Twist vs siblings:** it is used *calibrated*: PRIOR_ART.md:310–315 measures
  Jean's 88 against Sun–Yang–Li's 89 — two independently published circuits — and
  gets Jaccard 0.553, *more* overlap than this repo's 88 @ 7 has with Jean's
  (0.530). The calibration is what licenses "an overlap of this size is what
  independent constructions for this map look like".
- **Measured performance:** every pairwise number the repo quotes — 0.735
  (derived 88 @ 5 vs 89 @ 5, the highest here), 0.530, 0.544, 0.455, 0.386,
  0.362, 0.323, 0.319.
- **Cost:** negligible.
- **Code:** in the method repo, not here; only the outputs live in this slice.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** superseded-for-distinctness by the free-move **orbit /
  component-membership** instrument (e14/e16) and by `D_fine` — but keep it for
  *communication*, since it is far cheaper to explain to a reader. See §3A item 7.

### dated-corrections-ledger (editorial method)
- **Family:** documentation discipline.
- **What it does:** never rewrites a superseded claim. `PRIOR_ART.md` opens with a
  reverse-chronological `## Corrections` log (5 dated entries: 2026-07-23, -27,
  -29, -30, and the 2026-07-30 scope entry); `bounds.json` `claim` strings gain
  "Updated <date>: …" sentences appended to the original text; `PAPER.md` carries
  its own `## Corrections` section with note versions 2, 3, 3.1.
- **Twist vs siblings:** it distinguishes *scope* entries from *correction*
  entries. Commit `73ad7ee` is explicitly filed as scope ("Nothing here is
  withdrawn and no figure changes") — it narrows how a true statement may be read
  rather than retracting it.
- **Measured performance:** it caught and recorded one genuinely false statement
  (PRIOR_ART.md:64–66: the 89 @ 5 "remains the depth-5 point of the
  no-imported-material frontier" → "It does not") without disturbing anything
  around it.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** keeper in *substance*, but see §3A/§1 on verbosity — the
  method is right and the current execution is 10,300 words long. A rewrite should
  keep the ledger and shrink the prose around it.

---

## 3. ARTIFACTS (counts + labels)

Every command below was run from `/home/joebachir20/xor_ui/aes_mc_records/`.

| label | count | command | path |
|---|---|---|---|
| verified circuit JSONs | **11** | `ls circuits/*.json \| wc -l` | `circuits/` |
| …of which 88-gate | **5** | `ls circuits/mixcolumns_88gates_*.json \| wc -l` | `circuits/` |
| …by depth | 3:2, 4:1, 5:3, 6:2, 7:1, 8:1, 10:1 | `python3 -c` over `bounds.json` | — |
| …by lineage | 6 own-from-scratch-or-own-lineage current + 2 derived-from-Jean + 3 v1 archival | `bounds.json` `provenance`/`claim` | — |
| plain-text listings | **11** | `ls listings/*.txt \| wc -l` | `listings/` |
| Verilog netlists | **11** | `ls verilog/*.v \| grep -vc '_tb.v$'` | `verilog/` |
| Verilog testbenches | **11** | `ls verilog/*_tb.v \| wc -l` | `verilog/` |
| `bounds.json` circuit entries | **11** | `python3 -c "import json;print(len(json.load(open('bounds.json'))['circuits']))"` | `bounds.json` |
| …with a `provenance` string | **5** (the 88s only) | same, filtered on `'provenance' in c` | `bounds.json` |
| regression tests | **12** | `grep -c 'def test' tests/test_verification.py` | `tests/` |
| adversarial rejection cases certified | **14** | `MATHEMATICAL_VERIFICATION.md` §Adversarial tests | `audit/` |
| generator scripts | **4** | `find scripts -name '*.py' \| wc -l` | `scripts/` |
| tracked files | **68** | `git ls-files \| wc -l` | — |
| commits | **30** | `git rev-list --count HEAD` | — |
| local git tags | **1** (`v1.0.0` only) | `git tag` | — |
| figures | **1** | `ls docs/` | `docs/frontier.svg` |
| writeups | **4** prose + 1 PDF + 1 LaTeX source | — | `README.md`, `PAPER.md`, `PRIOR_ART.md`, `audit/MATHEMATICAL_VERIFICATION.md`, `paper/mixcolumns_note.{pdf,tex}` |
| raw logs | **0** | — | this repo keeps none by design; run archives live in `slp-plateau-search/evidence/` |

**Bound/UNSAT certificates in this slice: none.** No certificate file is shipped
here. The certificate *claims* are narrative only, in `PAPER.md:137–151` and the
`bounds.json` claim strings, and they point at `slp-plateau-search`.

**Prose volume**, since a rewrite is planned (`wc -l` / `wc -w`):
`README.md` 295 L / 2,686 w, 11 headings; `PAPER.md` 252 L / 2,770 w, 8 headings;
`PRIOR_ART.md` 488 L / 4,873 w, 14 headings (5 dated Corrections entries + 7
numbered Claim sections); `bounds.json` 209 L but with single `provenance` strings
of ~1,400 words and `claim` strings of ~600. Total public prose ≈ **10,300 words +
the 209-line JSON + a 537-line LaTeX note**. Section titles are declarative
sentences ("Claim 5: 88 gates at depth 6 — improves the frontier at that depth,
not the count"), and near-identical caveat paragraphs are restated in README,
PAPER.md, PRIOR_ART.md, `bounds.json` and the SVG alt text — the Jean-priority
disclaimer appears, by my count while reading, in **five** documents and more than
a dozen distinct sentences. **Recording this factually as requested: it is not a
template.**

---

## 3A. STALENESS AUDIT

Baseline: everything in the repo is dated **2026-07-30 / v3.1.0**; `HEAD` is
`73ad7ee`, 2026-07-30 23:57. The August campaigns (e12–e17, fleets 1–12) are
entirely outside it. Below, **current claim → current knowledge**. I am mapping,
not recommending publication.

**A. One outright wrong figure.**

1. **The depth-4 frontier point: repo says 92, the project holds 91.**
   Stated as `92 @ 4` at README:8, README:18, README:87 (table row), PAPER.md:14,
   :26, :44, :89 (table row), :97, :182, PRIOR_ART.md:12 (the standing invitation
   — so the public bar is set one gate too high), :225, :254 (section heading),
   :266, `bounds.json:93` ("uses five fewer"), `docs/frontier.svg` (drawn point
   **and** its accessible description), `CITATION.cff` title string, and the LaTeX
   note's title/abstract. Current knowledge: **three independent oracle-verified
   91-gate depth-4 circuits from three distinct lineages** (pairwise Jaccard
   0.556 / 0.433 / 0.358), 15,912 distinct verified-realizable 91 @ 4 mask sets,
   no dead-gate defect, and 91 exactly optimal inside the whole measured depth-4
   vocabulary by RC2 MaxSAT. So the margin at depth 4 is **six**, not five.
   A ready-made patch with line numbers re-derived against **this exact commit**
   exists: `slp-plateau-search/fleet7/laneCONSOLIDATE/RECORDS_REPO_PATCH.md`
   (2026-08-24, advisory only, nothing edited). Evidence:
   `experiments/e4_depth/RESULT.md` §1–2. Confirmed again by the user's own
   2026-08-27 correction in the session plan: "the depth frontier is UNCHANGED at
   97@3, **91@4**, 88@5".
   **Guard that must travel with it:** 90 @ 4 is **undecided, not refuted** —
   e4's exactness is relative to a fixed 227/300-mask vocabulary, and
   `fleet4/laneDEPTH` §3.2 left "exactly 90 iff W3(D=4) ≤ 11" in flight. Never
   write "optimal at depth 4".
   **Second guard:** the same session note contains a retracted item — a sentence
   proposing the patch "also carry 108@3" is corrected two lines later ("the
   strips improved individual ARTIFACTS' gate counts, never the frontier — do not
   repeat the '108@3 frontier' error"). 108 @ 3 is worse than the shipped 97 @ 3
   and must not enter this repo as a frontier point.

**B. Claims that are true but now much weaker than what is known.**

2. **No lower bound is stated at all.** The repo says only "SLP is NP-hard; we
   prove no count minimal" (README claim 1, PAPER.md §3). Current knowledge:
   **`56 <= L(M) <= 88`, unconditional and refereed** — described in
   `RECORDS_REPO_PATCH.md` §6 as "the first improvement over 54 in the project's
   history", and reaffirmed as the standing bracket through e15/e16/e17. Also
   unstated: **`L_cf(M) >= 92` with a solver-free certificate** (cancellation-free
   complexity is *four above the record*), and the fact that **no published
   MixColumns lower bound exists anywhere** — so a 56 would be the only one in the
   literature. Nothing in the repo hints any of this exists.

3. **"87 was not found is a statement about a search, and stays one."**
   (README claim 6; PRIOR_ART.md Corrections 2026-07-30; commit `73ad7ee`.)
   Still *correct* and should not be reverted — but as of 2026-07-30 it was the
   whole story, and it no longer is. Absent from the repo:
   - **Joint-level UNSAT k=9..13** — no 87 whose top two levels merge to k ≤ 13.
     Banked in `fleet8/unified/results/joint_levels.jsonl` and re-derived by
     `fleet11/laneCUBE` through an **independent CNF encoding**, 528/528 cubes
     agreeing at k=9/10/11, 0 disagreements. The 528-cube partition is
     machine-checked exhaustive, and the **positive control fired** (SAT at cube
     144 with a verify_slp-checked witness) — i.e. the test can fail.
   - **k=14 undecided and still running** (the frontier; 73/528 cubes refuted, 0
     SAT at last tally). A bracket, not a refutation.
   - **The B=56 tripwire theorem**: any valid irreducible 88 with B ≠ 56 yields an
     87 by deletion. Run over the **full population, 17,283/17,283 distinct 88s,
     zero alarms** (e15 run A, complete 2026-08-28) — "the strongest
     population-scale negative in the project" — plus 13/13 anchors at d3,
     27,720 triples each, 0 compressible, B=56 on all 13.
   - **15,099,957 windows swept, 0 compressible, 0 shared-helper wins** (e15
     stage 1); the earlier `≈165 million exact window decisions` figure in
     `PAPER.md:148` counts a different thing and the two must be reconciled before
     either is quoted again (see item 6).
   - **Free-move orbits closed by exhaustion**: 333,396 states across all 8
     F-point components, zero sub-88 (e16 laneFPOINT).
   - **The Anatomy Theorem** (e17, referee-confirmed): 14 proved conjuncts about
     any 87, including A8′ (|A*|=2 impossible at n ≤ 86) and **A11, the first
     gate-count-asymmetric fact in the project's history** — a property that is
     forced on any 87 with |A*|=2 and is **false at n=88** (7,362/19,490).
   - **The certificate LP is capped at 91.4098776 exactly**, proven below both
     upgrade thresholds — that whole family of arguments is proven unable to buy
     the next step.

4. **"87 was not found" as the only negative-space statement, vs. the shape of
   what has been ruled out.** The repo has no notion of *where* 87 has been
   excluded. August has a map: by deletion (population-wide), by free move (13
   closed orbits), by joint level (k ≤ 13), by window (d1/d2 everywhere on
   anchors, d3 on 13), by class pricing, by composition (96,520 splices,
   25.6 × 10⁹ mixes, min 88). None of that structure exists in the public text.

5. **Certificate scoping.** `PAPER.md:143–145` says the derived 88 @ 5 "has an
   empty k = 2 shell but its k = 3 shell was **never swept**, so with the 88 @ 7
   it is one of the two least-certified circuits here." e15's d3 anchor pass
   closed **13/13 anchors at 27,720 triples each**. Whether those two circuits are
   among the 13 anchors I could not determine from this slice — if they are, this
   sentence is stale; if not, it stands. **Check before rewriting** (§7).

6. **Corpus size figures are inconsistent across the two repos' vintages.**
   `PAPER.md:145–148`: "105,801 of the ≈ 139,878 harvested distinct 88-gate mask
   sets are proven irreducible at k = 2". August population figures: **18,355
   valid on-disk 88s / 17,283 distinct mask multisets** (e14 census, e15 run A).
   These are almost certainly different counting bases (harvested mask sets ever
   seen vs. distinct *valid* multisets on disk), and e15's own audit caught six
   discrepancies of exactly this species inside one campaign. **Do not quote
   either number in a rewrite without re-deriving what set it counts.**
   Confidence: SMELL, high-value.

7. **Distinctness instrument superseded.** All inter-circuit distinctness claims
   here are mask-Jaccard with a 0.7 same-family threshold. e14 established that
   the five records are **five pairwise-distinct closed free-move orbits**
   (44,793 states, all 10 pairs measured by direct set intersection, four of five
   perfectly rigid), and e16 extended it to **thirteen studied 88s = thirteen
   pairwise-distinct orbits** over 333,396 states. That is a strictly stronger and
   different notion of "different circuit" than Jaccard, and it is absent.
   Two cautions that must travel with it if it is ever published: e14's own guard
   — free moves preserve gate count, so *the orbit tables partition the 88
   plateau and are not evidence about 87* — and e14's finding that **distinct
   orbit does not imply distinct frame**.

8. **DAG statistics as structure.** `audit/MATHEMATICAL_VERIFICATION.md` publishes
   per-circuit fanout maxima, layer histograms and cancellation counts. e14
   declared **all DAG statistics dead as frame invariants** (mask-identical
   circuits can disagree on them; only opening-pairs and widest-gate are
   frame-legitimate, and even those are not cost-relevant; "no cost-relevant
   invariant is known"). The numbers are fine as *verification output*; they must
   not be presented as structural facts about the circuits. Also retired by e14:
   "max width ≤ 8" and "no <20 opening pairs" were never universal.

9. **The SAT evidence quoted is the old kind.** `PAPER.md:148–150` cites "windowed
   SAT (UNSAT to k=16 and k=15 on two family anchors, 0 SAT anywhere)" and
   correctly calls it evidence relative to the encoding's fixed slot order. The
   joint-level ladder is a cleaner, stronger, independently cross-checked object
   and predates nothing in the repo — it simply is not there.

**C. Dates, versions and process.**

10. **Literature-search cutoff 2026-07-23** (PRIOR_ART.md:10) is now **five weeks
    old**, and PRIOR_ART's own closing paragraph documents that these sweeps have
    a demonstrated failure mode (they corroborated a 91 floor while ePrint
    2025/1493's 89 sat unseen). No new sweep has been run. Separately, **Jean
    replied on 2026-08-10**: he holds *more unpublished 88s*, his intuition is
    that 88 is the lower bound, and proving it "seems extremely hard". Nothing
    published has moved the frontier as far as this project knows — but the
    cutoff line is a dated promise that has aged.

11. **`CITATION.cff` is stale in three ways**: `version: "3.1.0"`,
    `date-released: 2026-07-30`, and a title string that hardcodes
    "97 gates at depth 3; **92 at depth 4**". It also carries a placeholder:
    the v3.0.0 identifier is described as historical because v3.1.0's "own version
    DOI is minted when the v3.1.0 release is published" — and locally
    **`git tag` shows only `v1.0.0`**, so I cannot confirm from this slice that
    v2/v3 releases were ever tagged here (§7).

12. **The unpushed commit.** `73ad7ee` — "Scope the certificate claims: rigidity
    results, not evidence about 87" — is **ahead of `origin/main` by 1** and
    touches `PRIOR_ART.md`, `README.md`, `paper/mixcolumns_note.tex`. The public
    GitHub copy therefore still juxtaposes the empty neighbourhoods with "87 was
    not found" in precisely the way the author wrote that commit to prevent, and
    the published PDF (`paper/mixcolumns_note.pdf`, dated 30 July, 135K) may or
    may not have been rebuilt from the amended `.tex` — its mtime (Jul 30 13:39)
    is **earlier** than the commit (Jul 30 23:57), which suggests **it was not**.
    Confidence: VERIFIED-IN-LOG for the mtime ordering; PLAUSIBLE for the
    inference. Worth checking before any release.

13. **Reproducibility claims not re-measured.** PAPER.md:192 says the published
    method "reproduces 97 @ 3, 92 @ 4 and 89 @ 5"; `RECORDS_REPO_PATCH.md` §3.2
    flags that e4 measured the 92 anchor ending at 92 in **9 of 9** restarts and
    never reaching 91 — so if a 91 ships, this sentence must either stay
    describing the 92 or be re-measured. Also PAPER.md:194 "neither from-scratch
    88 has a single-command reproduction" — the August **working generator**
    (`fleet8/unified/generate.py`, emits oracle-VALID circuits at 88 and 91–107
    plus 116 in closed form, deriving the architecture from GF(2⁸) + 0x11B +
    FIPS-197) may change what that sentence should say. I did not verify the
    generator; flagging the interaction only.

**D. Things that are NOT stale — do not "fix" them.**

- Every **Jean-priority** statement. Confirmed by Jean himself in August.
- The **88 count floor**, the **97 @ 3** and **88 @ 5 / 88 @ 6** claims and margins.
- The **forced-depth** argument for Jean (7) and Sun–Yang–Li (9).
- The **2026-07-30 scope entry** on the remove-≤3 certificates. It remains exactly
  right, and August strengthened rather than weakened its core point: e17's
  laneDELTA showed the neighbouring δ(mc)=2 anomaly to be **circular** ("no 87 was
  found by this move, counted twice") with the standing instruction *do not cite
  δ(mc)=2 as evidence* — the same class of error the scope entry guards against.
- The **dated-corrections policy** itself.

---

## 4. KEEP / DELETE proposal

The whole tracked tree is a **DOI'd public artifact** — 956 KB total. Nothing
tracked should be deleted under any circumstances, and superseded circuits in
particular are referenced by archived Zenodo version DOIs.

| item | verdict | reason | size |
|---|---|---|---|
| `circuits/`, `listings/`, `verilog/*.v`, `bounds.json`, `docs/`, `paper/`, all root `.md` and `.py`, `tests/`, `audit/*.py`, `audit/*.json`, `audit/*.md`, `.github/`, `LICENSE`, `CITATION.cff` | **KEEP** | published artifact, DOI'd, 68 tracked files | 956K total |
| the 3 v1 archival circuits (98@3, 91@6, 89@10) | **KEEP** | explicitly retained "for the archival record"; the v1.0.0 version DOI resolves to them | 8K |
| the 2 Jean-derived 88s (depth 5, depth 8) | **KEEP** | dominated but disclosed; withdrawing them would break the corrections ledger | 5K |
| `__pycache__/` × 5 (`root, audit/, scripts/, tests/, paper/`) | **DELETE-CANDIDATE** | regenerable bytecode, already gitignored, includes stale 3.10 *and* 3.12 pycs | ~180K |
| `.pytest_cache/` | **DELETE-CANDIDATE** | regenerable, gitignored | 28K |
| `verilog/sim.vvp` | **DELETE-CANDIDATE** | iverilog build output, gitignored (`*.vvp`), regenerated by one `iverilog` call | 50K |

Total reclaimable: **~258 KB**. This is a rounding error; the only reason to
remove them is tidiness before a rewrite, and `git clean -Xd` would do it safely
since all three classes are already gitignored. **When in doubt here, keep** — the
cost of over-deleting in a DOI'd repo is a broken citation.

---

## 5. LEADS (sharp-eye findings)

**L1. The depth-4 patch has been sitting written and unexecuted for five days.**
`fleet7/laneCONSOLIDATE/RECORDS_REPO_PATCH.md` (2026-08-24) is a complete,
line-numbered patch against this exact commit, and it names a decision the user
owes. It is also listed as decision #1 in the session plan. Nothing has moved.
Confidence: **VERIFIED-IN-LOG**. Not an 87 lead — an execution gap.

**L2. Three 91 @ 4 circuits from three lineages, and 15,912 distinct 91 @ 4 mask
sets, are unpublished data with an open question attached.** The interesting part
is not the frontier point, it is that **90 @ 4 did not fall** in 49 depth-capped
restarts (4.9 core-hours, endpoints `{(91,4): 40, (92,4): 9}`, 0 at ≤ 90) while
`fleet4/laneDEPTH` §3.2 leaves the block-model rung at "**exactly 90 iff
W3(D=4) ≤ 11**" — a single named, decidable question that was left in flight and
would move a frontier point if answered. Confidence: **VERIFIED-IN-LOG** that it
was left in flight; **PLAUSIBLE** that it is cheap. This is the clearest
"decision left hanging" I found touching this slice.

**L3. The k=3 shell of the derived 88 @ 5 (and the 88 @ 7).** The public paper
names these two as "the two least-certified circuits here" with the derived 88 @
5's k=3 shell **never swept**. e15 then swept 13 anchors at d3 exhaustively. If
those two are in the 13, a published gap has silently closed and nobody has said
so; if they are not, they are the two named uncertified circuits in the whole
public record and sweeping them is a bounded, already-tooled job (27,720 windows
each — hours, not days). Either way the answer is cheap. Confidence: **SMELL**,
cheap to resolve.

**L4. The 139,878 vs 17,283 corpus discrepancy.** Two published/banked figures for
"how many distinct 88-gate mask sets this project has" differ by 8×. Almost
certainly different counting bases — but e15's audit caught six discrepancies of
exactly this species inside a single campaign, and one of them (a "~16,800"
figure that silently priced in a run that was approved, drawn and **never run**)
is the same failure mode. If the larger number is real, then the population sweep
that returned "17,283/17,283 tripwire-silent" covered an eighth of the corpus, not
all of it — and the strongest population-scale negative in the project is weaker
than stated. **This is worth an hour of somebody's time before anything is
published.** Confidence: **SMELL**, high value.

**L5. Structure shared by all 88s — what this slice actually contributes.** Three
independent *forced-depth obstruction patterns* are recorded here and, as far as I
can see, never compared to each other or to anything else: the old plateau's rows
{3,27}, the 88 @ 6's rows {1,11,17,25}, the from-scratch 88 @ 5's rows
{1,7,12,13,17,18,21,25,27,28,31}, and Jean's three output bits at depth 7. Rows
1, 17 and 25 appear in two of the three patterns; 27 in two. Nobody in this slice
asks whether the *set of forced-late output rows* is an invariant of the 88
plateau, and it is computed by a cheap fixpoint (`engines.py:relax`) that already
exists. Note the standing caution: e14 killed every DAG statistic as a frame
invariant, but ASAP depth over a **mask set** is not a DAG statistic — it is
exactly the kind of object that survived. Confidence: **PLAUSIBLE**, cheap to test
on the whole 88 corpus.

**L6. `cleanroom_verify.py` records a cancellation statistic nobody uses.**
Per-circuit "total canceled basis terms" / "total canceled input occurrences":
the derived 88 @ 5 shows 33/66, the from-scratch 88 @ 5 shows **44/88**. Given
that the whole optimality question has been reframed by `L_cf(M) >= 92` as "what
does cancellation buy?" — the cancellation-free complexity being *four above the
record* — a per-circuit cancellation count sitting in a generated audit file for a
month, unread, is exactly the "data generated but never examined" the brief asks
about. It is 11 numbers, already computed, in `audit/recomputed_metrics.json`.
Confidence: **PLAUSIBLE**.

**L7. Jean's unpublished 88s are the named antidote to the one selection-bias
caveat, and the repo update is the gating item.** e14: all local anchors came from
one solver fleet. Jean (2026-08-10) holds more 88s from a genuinely foreign
lineage (his method: "AI, most specifically models from OpenAI under codex"), and
the follow-up email is planned *after* the repos are updated (~2026-08-30). Every
foreign 88 is a fresh cheap shot at an 87 through the B=56 tripwire, and B=56
holding on foreign circuits would be real new evidence for the floor. **The
staleness of this repo is on the critical path to that email.** Confidence:
**VERIFIED-IN-LOG**.

**L8. A latent inconsistency the repo cannot see.** README:11 and the SVG alt text
both assert the depth-6 88 "is dominated by the depth-5 one and so sits behind
it", while `bounds.json` keeps it as a *different family* (Jaccard 0.323). e14/e16
then established the two are in **different closed orbits** — a stronger statement
than either. The public text's weakest available justification for keeping the
depth-6 circuit ("kept as a different family") is the one that has since been
upgraded, and the upgrade is unpublished. Confidence: **VERIFIED-IN-LOG**, minor.

---

## 6. HAZARDS

- **This repo is outward-facing, DOI'd, and CI-gated.** `.github/workflows/verify.yml`
  runs the verifier on push; a broken artifact fails publicly. Per the session
  plan: *do not edit, commit or push without explicit user approval.*
- **One unpushed commit (`73ad7ee`).** Any reorganization must preserve it. Do not
  reset, rebase or force-push. See §3A item 12 — the published PDF may predate it.
- **Seven file classes are GENERATED and must never be hand-edited**: `listings/*.txt`,
  `verilog/*.v`, `verilog/*_tb.v`, `docs/frontier.svg`, `audit/recomputed_metrics.json`,
  `audit/MATHEMATICAL_VERIFICATION.md`, `paper/appendix_circuits.tex`. Each has a
  generator with a `--check` mode and `tests/test_verification.py` asserts the
  match — hand-editing turns into a test failure, not a silent drift, which is
  good, but it will block a release.
- **`sha256_circuit_json` is over the file bytes as they land in *this* repo.**
  A pretty-printer changes it. `RECORDS_REPO_PATCH.md` §1 documents that the same
  92 @ 4 circuit has different file hashes in the two repositories while its
  canonical hash matches. Any circuit copied in must have its file hash
  **recomputed after the copy**.
- **`CITATION.cff` carries live DOIs** (concept 10.5281/zenodo.21299092, plus
  version DOIs for v3.0.0, v2.0.0, v1.0.0). Do not edit the identifier list
  casually; the DOIs resolve to Zenodo depositions that include the superseded
  circuits.
- **Deleting a superseded circuit breaks an archived DOI.** The v1.0.0 deposition
  contains 98 @ 3, 91 @ 6, 89 @ 10; the v2.0.0 one the 88s at depths 7 and 8.
  The patch note says this explicitly: "Do not delete it — the archived DOIs refer
  to it."
- No absolute paths, no symlinks, no running processes in this slice. Nothing here
  is touched by `fleet11/laneCUBE`.

---

## 7. GAPS

- **Whether the derived 88 @ 5 and the 88 @ 7 are among e15's 13 d3 anchors**
  (§3A item 5, L3). Determining it needs `experiments/e15_campaign3/` —
  outside this slice.
- **Whether `v2.0.0` / `v3.0.0` / `v3.1.0` were ever tagged or released.**
  `git tag` locally returns only `v1.0.0`. Checking origin needs network; I did
  not run `git ls-remote`. `CITATION.cff` itself says the v3.1.0 version DOI is
  minted "when the v3.1.0 release is published", which reads as *not yet done*.
- **Whether `paper/mixcolumns_note.pdf` was rebuilt after `73ad7ee` amended the
  `.tex`.** The mtime ordering says no (PDF 13:39, commit 23:57, same day) but I
  did not diff the PDF text against the `.tex`.
- **The 139,878 vs 17,283 reconciliation** (L4) — needs the harvest ledgers in
  `slp-plateau-search`, not this slice.
- **Did not re-run `audit/cleanroom_verify.py`, `verify_verilog.py`, or the
  pytest suite** — CPU is scarce and the solvers own the box. Only `verify.py`
  was run (11/11 pass, sub-second). The clean-room and Verilog results quoted
  above are from the repository's own generated reports, dated 2026-07-30T15:59Z.
- **Did not verify the three candidate 91 @ 4 circuits myself**, nor check whether
  the recommended `cascade6/FRONTIER_91gates_depth4.json` carries the
  `provenance`/`depth`/`verified` fields this repo's schema and bar would require.
  `RECORDS_REPO_PATCH.md` §2 says it does and the other two do not; that is
  second-hand here.
- **The k=14 verdict is unknown and outside this campaign** by the brief's own
  framing.
