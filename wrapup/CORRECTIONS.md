# CORRECTIONS — the stale-numbers register

Compiled 2026-08-29 from the ten wave-1 slice reports in `wrapup/reports/`.
Paths are relative to `/home/joebachir20/xor_ui/slp-plateau-search/` unless prefixed
`aes_mc_records/` (= `~/xor_ui/aes_mc_records`).

**Purpose: nothing public gets written from a stale number.** Every document below
carries a figure that later work moved, refuted, or completed. This register is
read-only — no document has been edited. Each entry gives: the document, the claim as
it currently stands, the correct figure, and the citation that establishes it.

**56 corrections registered.**

## Numbers that must NEVER be quoted without re-deriving them at write time

| Figure | Why |
|---|---|
| Any depth-4 frontier point | 92 is wrong everywhere; it is **91** (C-01, C-02) |
| Any "N of the known 88s" population count | at least **six** incompatible counting bases in circulation (C-11, C-38, C-45) |
| Any laneCUBE cube count | it moves while the lane runs (C-08) |
| Any "exhaustive, zero reducible" certificate claim | repriced at LR ≈ 1.00 (C-42) |
| Any pre-2026-07-30 wave-1..4 campaign_87 number | 12-item retraction ledger postdates all of them (C-30) |
| Any `grep -c` over an append-only ledger | ids are re-logged across phases; dedupe by id, last-wins (C-31) |
| Any UNKNOWN from a u7/v2 timed-out run | run at 1–2 workers, where contention manufactures UNKNOWNs (C-39) |

---

# 1. The two public repositories

### C-01 — `slp-plateau-search` public repo publishes a stale depth-4 record
**Documents:** `README.md:9` and `:13` (plus the SVG alt-text), `evidence/RESULTS.md:1`
and §2, `docs/generate_frontier_svg.py:62` (`FRONTIER = [(3,97),(4,92),(5,88)]`),
`docs/frontier.svg`, `.github/workflows/verify.yml` (verifies 92@4),
`tests/test_invariants.py::test_directory_holds_exactly_the_eight_records`,
`evidence/circuits/` (no 91@4 file, no `spectrum.json` entry).
**Wrong claim:** "verified frontier: 97 @ 3, **92 @ 4**, 88 @ 5".
**Correct figure:** **91 @ 4**, verified — `python3 verify_circuit.py
campaign_87/cascade6/FRONTIER_91gates_depth4.json 4` and
`experiments/e4_depth/out/resched/atlas_compiled_m1_91gates_depth4.json` both return
`gates=91 depth=4 outputs_built=32/32 VERDICT: VALID`. `experiments/e4_depth/RESULT.md`
reports **15,912 distinct verified-realizable 91@4 mask sets** (plus 214 at 92@4), all
15,683 census members with exactly 91 *live* gates (no dead-gate defect), and **three
genuinely distinct lineages** (cascade6, m3_census, `atlas/compiled_m1.json` — filed as
depth 5, reschedules to depth 4 free; Jaccard 0.433 / 0.358).
**Source:** `root_infra` L4 (oracle re-run in-session); `experiments_early`/`fleet1_4`
concur. `FLEET_PLAN.md` Lane D item 4 lists this as an outstanding chore, never done.

### C-02 — `aes_mc_records` publishes the same stale depth-4 record, in 16 places
**Documents:** `README.md:8`, `:18`, `:87` (table row); `PAPER.md:14`, `:26`, `:44`,
`:89` (table row), `:97`, `:182`; `PRIOR_ART.md:12` (**the standing public invitation —
so the bar is set one gate too high**), `:225`, `:254` (section heading), `:266`;
`bounds.json:93` ("uses five fewer"); `docs/frontier.svg` (drawn point **and** its
accessible description); `CITATION.cff` title string; the LaTeX note's title and
abstract.
**Wrong claim:** 92 @ depth 4; margin at depth 4 stated as five.
**Correct figure:** **91 @ 4**; the margin is **six**. A ready-made patch with line
numbers re-derived against this exact commit exists and has been unexecuted for five
days: `fleet7/laneCONSOLIDATE/RECORDS_REPO_PATCH.md` (2026-08-24, advisory only).
**Two guards that must travel with the fix:**
1. **90 @ 4 is undecided, not refuted** — e4's exactness is relative to a fixed
   227/300-mask vocabulary, and `fleet4/laneDEPTH` §3.2 left "exactly 90 iff
   `W3(D=4) ≤ 11`" in flight. **Never write "optimal at depth 4."**
2. **Do not add 108 @ 3.** A session note proposing it is retracted two lines later —
   the strips improved individual artifacts' gate counts, never the frontier; 108@3 is
   worse than the shipped 97@3.
**Source:** `records_repo` §3A item 1; `fleet1_4` L11; `root_infra` L4.

### C-03 — `aes_mc_records/CITATION.cff` is stale in three ways
**Wrong:** `version: "3.1.0"`; `date-released: 2026-07-30`; a title string that
hardcodes "97 gates at depth 3; **92 at depth 4**". It also carries a placeholder: the
v3.0.0 identifier is described as historical because v3.1.0's own version DOI "is minted
when the v3.1.0 release is published".
**Correct:** the title must say 91 at depth 4 (C-02). **Unverifiable from the slice:**
locally `git tag` shows only `v1.0.0`, so it could not be confirmed that v2/v3 releases
were ever tagged in this checkout.
**Source:** `records_repo` §3A item 11.

### C-04 — the literature-search cutoff is a dated promise that has aged
**Document:** `aes_mc_records/PRIOR_ART.md:10`.
**Wrong claim:** literature cutoff **2026-07-23** — now five weeks old.
**Correct:** no new sweep has been run. PRIOR_ART's own closing paragraph documents that
these sweeps have a **demonstrated failure mode** (they corroborated a 91 floor while
ePrint 2025/1493's 89 sat unseen). Separately, **Jean replied 2026-08-10**: he holds more
unpublished 88s, his intuition is that 88 is the lower bound, and proving it "seems
extremely hard".
**Source:** `records_repo` §3A item 10.

### C-05 — two unpushed commits, and a PDF that was probably never rebuilt
**`slp-plateau-search` commit `23d80d7`** is one ahead of `origin/main` and is *"the most
important commit in the repo's history"* — the one that **withdraws the inference
"certificates ⇒ 87 is unlikely"**. Until it is pushed, the public copy still carries the
withdrawn inference.
**`aes_mc_records` commit `73ad7ee`** ("Scope the certificate claims: rigidity results,
not evidence about 87") is likewise **ahead of `origin/main` by 1**, touching
`PRIOR_ART.md`, `README.md`, `paper/mixcolumns_note.tex`. So the public GitHub copy still
juxtaposes the empty neighbourhoods with "87 was not found" in precisely the way that
commit was written to prevent.
**And:** `paper/mixcolumns_note.pdf` mtime (Jul 30 13:39) is **earlier** than the commit
(Jul 30 23:57) — the PDF was very likely **not rebuilt from the amended `.tex`**.
VERIFIED for the mtime ordering, PLAUSIBLE for the inference. Check before any release.
**Source:** `root_infra` L1; `records_repo` §3A item 12.

### C-06 — `aes_mc_records/PAPER.md` reproducibility sentences interact with August work
**`PAPER.md:192`** — "the published method reproduces 97 @ 3, 92 @ 4 and 89 @ 5". E4
measured the 92 anchor **ending at 92 in 9 of 9 restarts, never reaching 91**, so if a 91
ships this sentence must either stay describing the 92 or be re-measured.
**`PAPER.md:194`** — "neither from-scratch 88 has a single-command reproduction". The
August working generator (`fleet8/unified/generate.py`, emitting oracle-VALID circuits at
88 and 91–107 plus 116 in closed form, deriving the architecture from GF(2⁸) + 0x11B +
FIPS-197) may change what this should say. The generator was not verified in-slice; the
interaction is flagged only.
**Source:** `records_repo` §3A item 13 via `RECORDS_REPO_PATCH.md` §3.2.

---

# 2. Live tallies made stale by compute that landed after the write-up

### C-07 — `fleet12/LIBRARY.md`'s open-axes scoreboard predates two of its own lanes
**Document:** `fleet12/LIBRARY.md` §4/§5 (and its note *"laneKNOBS started after this file
was written and is running now; its verdicts are not yet in §3"*).
**Wrong claim:** **11 axes OPEN**, with axis 12 (the menus, flag F1) listed OPEN at
"~100 configs × the affected block solves — days".
**Correct figure:** wrong by **at least seven axes** — **6, 7, 8, 9, 14, 15 were bought by
laneKNOBS**, and **12 was bought and repriced by laneF1** (which supplies its own
replacement row in its §8). The corrected picture: essentially everything cheap is now
CLOSED or MEASURED. What genuinely remains open is **axis 13** (currency per-line
independence), **axis 20b** (the symmetry/normalisation rules N1–N3 — *every UNSAT this
repository has ever emitted rests on them, and nobody, including the audit referee, has
re-refereed them*), **axis 24** (L5's forward-only rule), and **axis 21** (the un-split
block, priced dead at k ≥ 14).
**Consequence:** anyone writing the public "what remains open" section from §4/§5 as it
stands **will overstate the open frontier substantially.**
**Source:** `fleet9_12` L4.

### C-08 — `fleet11/laneCUBE`'s headline cube count is stale
**Documents:** `fleet11/laneCUBE/RESULT.md` §7.1 and every downstream citation, including
`fleet12/LIBRARY.md` §2.2 and axis 21.
**Wrong claim:** "51 of 528 cubes decided".
**Correct figure:** **564 rows, 87 distinct cubes decided, all 87 UNSAT, 0 SAT, 477
open** — re-counted from the append-only bank
`fleet11/laneCUBE/cubes/joint_W3U4_k14.jsonl`. The verdict is unchanged (**UNDECIDED, a
bracket**), but **every "51" must be re-derived from the bank at write time, not copied**,
and the number moves while the lane runs. Related honest datum: four monolithic solvers
have now run 3 days each (~288 core-hours) with zero bytes of log output, consistent with
the lane's own 653–1,113 core-hour estimate.
⚠ `experiments/sat_package/README.md` §9 already carries the right instruction ("re-tally
before quoting"); its honesty note is only correct while the lane is untouched.
**Source:** `fleet9_12` L1; `experiments_early` H1.

### C-09 — `fleet9/laneENUM`'s tally is five days stale; ~84 wall-hours were never read
**Documents:** `fleet9/laneENUM/RESULT.md` (dated 2026-08-24) and
`fleet9/laneENUM/results/TALLY.txt` (Aug 24 16:20).
**Wrong claim:** the documented state, with the lane's own note that *"the U3 counting
queue was still draining at write-up and banks per cell, so re-running the tally can only
RAISE floors"*. Nobody re-ran it.
**Correct figures:** the ledger has grown **198 → 270 rows** (**72 post-write-up rows**);
`results/v2_counts.jsonl` is Aug 25 04:35, `results/sets/` Aug 25 06:58,
`results/sat_counts.jsonl` **Aug 26 04:18**. What landed: **all 14 U3 cells now have
SAT-enumeration rows**, 13 of them finding ≥ 1 optimal set (p88_05 found 7), including
single cells that ran **116,049 s (32 h)**, **59,932 s (16.6 h)** and **53,165 s (14.8 h)**.
Total banked enumeration wall is now **443,651 s = 123.2 core-hours**, of which 85.3 h is
the SAT enumerator.
**Impact:** small — every new row is `complete: false, status: timeout`, so U3 stays
UNDECIDED and the §4 population floors only firm from "UNDEC" to "≥ 1". But
`python3 fleet9/laneENUM/code/tally.py` (read-only) has never been re-run, and the lane's
§4 says doing so is the correct way to read the table. **One command.**
**Source:** `fleet9_12` L2.

### C-10 — `fleet12/laneF1`'s result table is missing 13 rows
**Document:** `fleet12/laneF1/RESULT.md` §4a.
**Wrong claim:** a cut-off at **51 rows / 49 distinct runs**, with "eight runs still
solving".
**Correct figure:** `fleet12/laneF1/results.jsonl` now holds **64 rows**. The 13 late
arrivals include the data points the document could only *infer*: `s5a_add046`,
`s5a_add04c`, `s5a_add02a`, `s5a_add06e` (all |M| = 24, blocks 65) → **89**, and
`s5a_add046e` (**|M| = 25, blocks 64**) → **89**. **That is the plateau's upper cliff
measured rather than argued** — the plateau really does stop at |M| = 23, and blocks = 64
(previously reached only by a 56-shape uniform menu) is now also reached by a 25-shape
record-derived menu at total 89. Six further rows are lean-menu `exit 5 UNDECIDED`
truncations. **Nothing ≤ 87.**
**Fix:** re-run `fleet12/laneF1/scripts/tally.py` and `curve.py` before quoting §4a.
**Source:** `fleet9_12` L3.

### C-11 — `campaign_87` population figures are understated; the frontiers listed as open are finished
**Documents:** `campaign_87/FACTS.md` §6a and `campaign_87/FINAL_REPORT.md`; also
`CERTIFICATES.md`'s "resumable frontiers" list.
**Wrong claims:** "51,899 of 84,989 … 33,090 remain, ~2.9 h"; "**105,801** of the
≈139,878 harvested distinct 88-gate mask sets are proven irreducible at k = 2"; "19 closed
exhaustively, 181 selected states remain"; k=4 coverage 32,685 / 20,432 / 9.
**Correct figures** — measured in the unreported, untabulated `agents/frontier-exact/`:
```
results_pop/pop_progress.jsonl      84,989 rows, all irreducible_k2
results_residue/residue_progress.jsonl  987 rows, all irreducible_k2
results_popk3/k3_progress.jsonl        200 rows, all irreducible_k3   (queue EMPTY)
results_k4/progress.jsonl           56,489 rows, all "irreducible"    (published: 32,685)
results_k4_f3/progress.jsonl        39,034 rows, all "irreducible"    (published: 20,432)
results_k4_indep/progress.jsonl     34,599 rows, all "irreducible"    (published: 9)
```
⇒ **84,989 + 987 + 53,902 (family 3, already closed) = 139,878 = the entire known 88
population is proven k=2-irreducible**, the k=3 queue is empty, and k=4 coverage on the
three anchors is roughly double what is published.
**Two consequences.** (1) `FACTS.md` §6a and `FINAL_REPORT.md` must be corrected
**upward**. (2) **C-42 applies to all of it** — more irreducibility at radius ≤ 4 is
exactly the evidence class the controls measured at LR ≈ 1, so the correction makes the
numbers right without making them mean more.
**Source:** `campaign_87` L11 (measured in-session), superseding `root_infra` L7's
"33,090 states left".

### C-12 — `fleet8/unified/RESULT.md` reports floors that its own ledger has already moved
**Documents:** `fleet8/unified/RESULT.md` §2b and §10 item 3; and, inconsistently,
`fleet8/unified/results/derive_free_*.json` (mtime 2026-08-25) vs
`fleet8/unified/results/vacuity_guard.json` (mtime 2026-08-27).
**Wrong claim:** all three free-supply derivations **VACUOUS**, floors **8 / 8 / 8**, over
the `max_cost = 1` families of 64 / 64 / 45 values — and §10 item 3 lists *"re-run the
free-supply derives over `plane_family(..., max_cost=2)` — only the compute was missing"*
as **future work**.
**Correct figures:** that re-run **happened on 2026-08-27** through this same code:

| derivation | family | floor | in-family | agrees | vacuous |
|---|---|---|---|---|---|
| Q1 at U1 | **200** | **6** (was 8) | 3/3 | **3/3** | **false** |
| D37 at U4 | **241** | **7** (was 8) | 4/4 | 2/4 | **false** |
| D37 at W3 | **241** | **7** (was 8) | 4/4 | 0/4 | **false** |

The `Q1` derive is repaired and selects the configured triple exactly — a provenance gain
`RESULT.md` does not record.
⚠ **The artefacts and their own guard disagree:** `results/derive_free_*.json` still hold
the OLD `family_size 64/45, floor 8, VACUOUS: true` rows. Anyone re-running
`code/annotate_derive.py` without the env variables set **will silently flip them back**.
**Does not yield an 87** — see Appendix A of `LEADS.md`: `fleet12/laneKNOBS/RESULT.md` §6
costed the derive-nominated `D37` at **89**.
**Source:** `fleet5_8` L1.

---

# 3. Superseded verdicts and attributions

### C-13 — `STATE_OF_THE_PROBLEM.md` §5.3 says "untouched" about something already measured
**Document:** `fleet7/laneCONSOLIDATE/STATE_OF_THE_PROBLEM.md` §5.3.
**Wrong claim:** *"The multi-gate shared-plane family. Lane F4's `W3 ≥ 8` is closed for all
64 one-gate values; a `D37` containing 2-gate values could in principle drive `W3` to 7.
**Untouched.**"*
**Correct figure:** **W3's floor over all 241 ≤2-gate `{3,7}` commitments is measured at
7**, and U4's likewise (C-12) — and the route is closed negative at 89 by
`fleet12/laneKNOBS/RESULT.md` §6.
**Also stale in the same document:** `MB27B373` (C-14), and its own D7 predicted it.
**Source:** `fleet5_8` L1, H7.

### C-14 — `MB27B373` is still recorded as UNDECIDED in two places
**Documents:** `fleet5/laneMERGE/RESULT.md` §2a and `fleet5/laneMERGE/results/FINAL_TALLY.txt`.
**Wrong claim:** `MB27B373 [12,13] UNDECIDED`.
**Correct figure:** **`MB27B373 = 13` exactly.** `fleet6/door/logs/door.out` line 5 —
`[sat] k=12: UNSAT (19458.32 s)` — combined with the inherited replay bound of 13 decides
it, closes `fleet5/laneMERGE`'s last undecided in-class 87 lead, and **forecloses the
branch where 12 would have priced the class at 87**. `laneCONSOLIDATE` flagged it as
discrepancy D7 and `fleet8/unified/RESULT.md` §10 item 5 independently re-derived it.
**The cheapest correction in the repository: one row of one table.** (`fleet6/door` also
has no `RESULT.md` — C-52.)
**Source:** `fleet5_8` L4.

### C-15 — three published atlas claims about the socle plane are refuted by atlas's own unread output
**Documents:** `atlas/thinktank/ideas_strange_corners.md` §4.5, `atlas/NOTEBOOK.md`,
`atlas/thinktank/audit_inference.md` §3.3.
**Wrong claims:**
1. *"the band `l3 ∈ 69..72` … is now populated — and costs 90–91 gates, so the two 88 bands
   `{67,68}` and `[73,78]` are separated by a **real 2-gate ridge**"*;
2. the published 88 floor **`l3 ≥ 67`**;
3. *"real content = bimodal `l3` by lineage, gap 69–72 empty"*.
**Correct figures**, measured from `atlas/corner/out/*.plat` (498 distinct 88-gate
mask-sets, 13 verified VALID in-session): **70 of the 498 sit at 88 gates with
`l3 ∈ 69..72`** (verified at each of 69, 70, 71, 72) — **there is no ridge; the 88 level
set is continuous from 64 to 79**. **27 circuits sit at `l3 ∈ {64,65,66}`** (verified at
64, 65, 66) — the floor is not 67. The 69–72 gap is an artifact of the **9-circuit sample**
placed on the plane, not of the plane. `corner/socle.py::l3_of` was confirmed to reproduce
the published table exactly (88@5→77, 88@5fs→67, 88@6→68, 88@7→74), so the discrepancy is
in the claims, not the instrument.
**Source:** `atlas_misc` L1 (measured and oracle-verified in-session). See `LEADS.md` #3.

### C-16 — a proved correction to three atlas negatives was written and never pasted
**Document:** `atlas/thinktank/ideas_basin_atlas.md` (dated Aug 18 01:05 — *before* the
correcting run).
**Wrong claim:** three of `basin/b9b_sweep.py`'s 23 published `ctl=OK exhaustive` lines
(**88@5 S0, 88@7 S0, 88@8 S0**) are presented as sound negatives.
**Correct:** they are **vacuous** — the "free structural control" tests the wrong
predicate. Found by E3a, independently reproduced by E7 with two exact engines
cross-checked, and E7 wrote a paste-ready correction with a proof of the convex-closure
repair (`experiments/e7_push/ATLAS_NOTE.md`). It was never pasted:
`grep -c convex atlas/thinktank/ideas_basin_atlas.md` returns **0**. The sharpened
statement is that all three blocks land on exactly `|B| + 1` — *"the scoped space is one
gate too poor to reproduce the circuit that already exists."*
**Cost of the fix: five minutes.**
**Source:** `experiments_early` L6; `atlas_misc` §5 closure table.

### C-17 — lane F4's attribution of its own 3-gate gap is refuted by its own late solve
**Documents:** `fleet3/laneF4_rule/RESULT.md` §3.2 (and, by inheritance, `WALKTHROUGH.md`
§4).
**Wrong claim:** `W3_noshare(Q27={δ₃(c)})` is `≥ 10 PROVEN; exact value UNDECIDED`, with
the 3-gate gap decomposed as *"the rank cut alone buys ≤ 1, the edge buys the other ≥ 2 —
both ingredients are needed; neither alone accounts for 3."*
**Correct figures:** the re-queued solve finished — `results/cache.jsonl`
`name=bW3_noshare_2dd8cbb10c3d status=exact min_gates=11 wall=33876.6 verified=true`. With
`W3_noshare = 11` the four measured points are `(rank3, no share) = 12`,
`(rank1, no share) = 12`, `(rank1, share) = 9`, `(rank0, share) = 10` ⇒ **the rank cut
alone buys ZERO and the sharing edge buys all 3.**
**Independent confirmation, also uncollected:** lane G's §7b in-flight solve (`U3` with
tier-1 rank-2 supply) finished at **10 exact**, not the hoped-for 9
(`logs/free_U3_tier1_t1_09d4d5136dea.out`: k=9 UNSAT 3552 s, k=10 SAT), so `(U27,U3)`
stays at 12 and lane G's §4.4(b) "moves from 12 towards 11" **moves nowhere**.
**Note:** the lane F4 referee spotted this and lists it as refutation (ii) in its BOTTOM
LINE — `RESULT.md` was never corrected, so **the two documents now disagree.**
**Source:** `fleet1_4` L3.

### C-18 — lane D's rigidity headline is wrong as stated; 99 escapes, not 1
**Document:** `fleet1/laneD_completions/RESULT.md`.
**Wrong claim:** the basin sweeps are "RESTARTED, PRODUCING, RUNNING" with
`{88@5fs: 4,944 banked, 0 escapes}` and `{88@6: 4,480 banked, 1 HIT-3}`, concluding
*"edit-closure rigidity is basin-dependent, since 88@5's basin gave 0 escapes in >10,000
triples"* and *"88@5fs 4,944 so far, 0"*.
**Correct figures:** both sweeps ran to completion — `basin_88at5fs.jsonl` and
`basin_88at6.jsonl`, **27,720 rows each**; tallies **88@5fs {none: 27,678, HIT-3: 42}** and
**88@6 {none: 27,663, HIT-3: 57}** = **99 escapes total**. **88@5fs is not rigid either**;
the true statement is that **88@5's basin is the anomalous one** (0 escapes in 10,266
triples) and the other two are not. Free by-product the write-up does not claim: **zero
completions at `k ≤ 2` across all 55,440 triples.**
**Source:** `fleet1_4` L2. (The 99 uncompiled mask sets are ranked at `LEADS.md` #14.)

### C-19 — `fleet6/laneTOOL2/RESULT.md` carries a superseded `L_cf` headline and a refuted constant
**Document:** `fleet6/laneTOOL2/RESULT.md`.
**Wrong claim (a):** its CP-SAT **103** is presented as the "first upper bound on `L_cf`".
**Correct:** it is neither first nor an improvement — the project already held an
**oracle-verified 102** with an artefact on disk
(`beat88/.../v2_no_vocab/data/cf_incumbent.json`), so the headline is a **regression**.
`STATE_OF_THE_PROBLEM.md` records this as discrepancies **D1/D10/D11** (the `L_cf` upper
bound is quoted at **four different values** across current documents) and it remains
**uncorrected in laneTOOL2's own RESULT.md**.
**Wrong claim (b), inherited from lane P:** `Y3: Y ≥ kappa − 5`.
**Correct:** **refuted** — `min(Y − kappa) = −6` over 3,254 census circuits, 43 witnesses,
pre-registered (PRED-10). The corrected constant `Y ≥ kappa − 6` prices at `L(M) ≥ 58`,
beating the refereed 56 — **but it is a measurement over 88s, not a theorem**, and one
further `−7` costs a gate off the 58. (3,254 circuits × 16 wirings ran in **132.5 s**.)
**Source:** `fleet5_8` §2 (method entries), L6.

### C-20 — `fleet8/unified` reports the joint test DONE without ever writing a verdict
**Documents:** `fleet8/unified/logs/joint_status.log` (`JOINT DONE 2026-08-26T11:01:14`)
and `fleet8/unified/RESULT.md` §10, which names
`results/joint_W3U4_result.json` as the final verdict.
**Wrong claim:** DONE.
**Correct:** `results/joint_levels.jsonl` stops at **k = 13**, `logs/joint.log` stops at
k = 13, and **`results/joint_W3U4_result.json` does not exist**. The k = 13 UNSAT landed at
09:52:29, so roughly 69 minutes of k = 14 ran and produced nothing.
(`results/joint.lock` still holds pid 82529.)
**What IS banked and permanent:** **k = 9..13 all exhaustively UNSAT** ⇒
`merged(W3 ∪ U4) ≥ 14`, and with the replay bound `merged ∈ {14, 15}` — which already
kills the two-gate saving. Only the one-gate question is open, and it is the live
`fleet11/laneCUBE` job.
⚠ **`results/joint_levels.jsonl` is the ONLY record of the 105,083 s k = 13 UNSAT — 29
core-hours in one 381-byte file.** Back it up before any reorganisation, and write the
laneCUBE verdict back here when it lands, or this folder will permanently read "DONE, no
answer".
**Source:** `fleet5_8` L2.

---

# 4. Experiments-campaign tallies (results that landed after their RESULT.md)

### C-21 — `e5_readd/RESULT.md` §7 tells the reader not to quote figures that have since completed
**Wrong claim:** *"`88fs5` was **left running** … do not quote the `88fs5` numbers in this
file, re-tally them."* Nobody did.
**Correct figures:** the drop-4 ledger reads `{('88d5','unsat'): 36241,
('88fs5','unsat'): 35960}`, plus
`{"circuit":"88fs5","kind":"screen_done","screened":13315,"trivial_counting":22645,"wmax":9}`
and its `screen_hist` over all 35,960 sets. **All 35,960 four-target drop sets of the
88-from-scratch@5 are refuted at `k = W−1`: zero improvements, zero timeouts.** The project
therefore holds **two** complete drop-4 certificates, not one — and E5 had explicitly
flagged that `88fs5`'s W-profile differs visibly from `88d5`'s (six `W=9` sets vs one), so
**family-independence was an open question and is now answered on a second family**.
**Source:** `experiments_early` L1.

### C-22 — `e7_push/RESULT.md` reports one decided dim-12 region; there are four
**Wrong claim:** one decided dim-12 region (88@5 R4), with region 2 at "84 of 231 cubes
done".
**Correct figures:** the ledger holds **four** `cube_verdict` rows, each `min_gates = 11`,
`lower_bound_proven = 11`, `control: POSITIVE`:

| region | cubes | k=10 wall | in RESULT.md? |
|---|---|---|---|
| `88@5 R4` | 210 | 1,898 s | yes |
| `88@5fs R4` | 231 | 2,852 s | **no** |
| `JEAN88 R4` | 190 | 1,979 s | **no** |
| `p88_05 R3` | 210 | 5,549 s | **no** |

with 190/190, 231/231 and 210/210 cube records on disk. So "the first decided dim-12
region in this project" is now **four**, **including one on Jean's foreign-lineage 88** —
exactly the independent-lineage test the project wanted.
**Source:** `experiments_early` L2.

### C-23 — `e3a/RESULT.md` reports three closed questions as open
**Wrong claims:** `buyone` "still accumulating"; `blockpop` "counts in the tally"
placeholder; `k3shell` recorded only as "the control fired".
**Correct figures:** **4,926 `buyone` rows, verdict `UNSAT_at_nB_minus_2` on every one, 0
hits, across all 14 known 88s**; **586 decided blocks** (324 `OPTIMAL_AT_nB`, 198
`NOT_COVERED`, 64 `CONTROL_FAILED`, **0 HIT**); and **two complete exhaustive
remove-3-add-2 certificates** banked (88@7 and 88fs, **27,720 windows each**, verdict
`"EXHAUSTIVE: no remove-3-add-2 improvement"`).
**Source:** `experiments_early` L3.

### C-24 — `e2_outputcost/RESULT.md`'s coverage table is stale
**Wrong claim:** the coverage counts as of the write-up.
**Correct figures:** `campaign2.log` ran to `CAMPAIGN2 DONE 06:07:03` — **40 of 40 dim-12
quad classes returned `status=timeout` at ~1,565 s each, 60,010 s elapsed, `cost=None` on
every one**; no new n=4 exact costs. Coverage did grow: **n=2 decided 274 → 278, n=3
140 → 165**. The headline is a measured negative — **dim 12 at k ≈ 24 is out of reach of the
generic SAT oracle** — matching E8's own dim-12 wall (bracket `[11,18]`, k=11 budget-expired
at 122.7 M nodes) with the same cause (`dist[]`/delta table is `2^dim`).
**Source:** `experiments_early` L7.

### C-25 — e15's cross-desk audit returned FAIL and corrected three carried figures
**Documents:** `experiments/e15_campaign3/RESULT.md` (**corrected in place**, then passed)
and `experiments/e15_campaign3/AUDIT_FINAL.md` §6–§7. **Still uncorrected at source:**
`experiments/e15_campaign3/laneSWEEP.md` §10.2b line 336.
**Verdict:** **FAIL, 2026-08-29** — the document's own BINDING claim, that every closing
figure was re-derived from the append-only sources, was false; figures had been carried
from **partial-run lane running-totals**. *Everything the desk could independently
re-derive reproduced exactly; `56 ≤ L(M) ≤ 88` is untouched and no negative weakens.*
**The three corrected figures:**
1. **Shared-helper rows: "one" → SIX** (four at 1, two at 3). The cited row is
   `cand_floor_PL2_E_…_053310_88g.json` (`0x81010180`); the other five are
   `sol_GEN89_w2_066923…`, `sol_GEN89_w2_001387…`, `union_PAIR_SIGMA5_h5c90652d…` (all
   `0x2818302`), and `union_TRI_S5_h963cb3_ha2a173…`, `union_TRI_S5_h1bf647_h6ef0b8…`
   (both 3 helpers). **Provenance of the error:** `laneSWEEP.md` §10.2b line 336,
   `shared-helper rows 1` — **a 610-row running total** carried into the final document as
   a completed-run figure. Direction: harmless to every conclusion and it *strengthens*
   one (e13's helper-distinctness universal is falsified a fortiori); all six are VALID88,
   d2 complete 1,540/1,540, `compressible_total = 0`, `bases = 56`, tripwire clean.
2. **`d(S)=1` uncovered: "~16,800" → 17,266**, in both required places. Decomposition:
   32 tier-B rows → 22 distinct circuits → 5 of them are K1–K5 under
   `aes_mc_records/circuits/`, outside the population list → **17** population circuits
   with `d(S)=1` attempted at all ⇒ `17,283 − 17 = 17,266`. The `~16,800` **silently priced
   in run C, which was approved, drawn and never run** — the correction now names that
   explicitly.
3. **Depth-14 provenance: 12 of 13** in `campaign_87/wave6_2026-08-11/discriminate/runs/`
   (7 `q0`, 5 `q1`), the 13th in
   `campaign_87/wave5_2026-08-04/burn/union_sat/found/sol_GEN89_w0_035873_alg_1_fs_1_88gates.json`.
**Source:** `experiments/e15_campaign3/AUDIT_FINAL.md` §6 D1, §7 items 1–4;
`experiments_late` §2 (referee-desk method entry); `records_repo` L4.

---

# 5. `campaign_87` contradictions and unrecorded results

### C-26 — a pre-registered prediction was refuted and the STATUS still records it CONFIRMED
**Document:** `campaign_87/wave6_2026-08-11/hp_strike/STATUS.md`.
**Wrong claim:** registers *"if the frontier is really about shape, then windows at
n = 12, 13, 14 with `|req|/n ≥ 0.85` should decide FAST"*, records the first two rows as
*"Consistent with CONFIRMED"*, and states the decision rule *"REFUTED if they time out
anyway."*
**Correct:** `logs/laneR.log` runs on — the last **eight** rows are all `"n87": 14,
"nreq": 13` (ratio 0.929), `"status": "timeout"`, `"t": 600.03`, `"control": "OK"`,
`ctl_gates: 88`. **8/8 timeouts with passing controls ⇒ the hypothesis is REFUTED at
n = 14**, and n does impose a real cost the ratio cannot buy back.
**Settles in seconds:** `python3 hp.py report && python3 compare.py`.
**Source:** `campaign_87` L12.

### C-27 — "the symmetric sector floor = 90" is cited campaign-wide and is not a theorem
**Correct:** the best reached in `campaign_87/wave5_2026-08-04/burn/oddparity/` is **91**;
every UNSAT there is **alphabet- and depth-conditioned**; and the one sector-scale run
(`symmat`, 1,517 masks) returned **UNKNOWN at K = 89, 88 and 87** after 2,455 s each.
**The sector is undecided below 90.**
**Source:** `campaign_87` L15.

### C-28 — "ρ-symmetry costs ≈108, so the ρ sector is expensive" carries no information
**Document:** `campaign_87/wave5.../burn/obstruction/OBSTRUCTIONS.md` (the correction was
never propagated into it).
**Correct:** `wave6/fresheyes_a/equiv.py` prints `plain greedy CSE: 108` **and**
`equivariant greedy CSE: 108` — **108 is simply what unrestricted greedy gets.** The
comparison is uninformative.
**Source:** `campaign_87` L15.

### C-29 — a retracted paragraph is the first thing a reader hits
**Document:** `campaign_87/wave5_2026-08-04/STATE_2026-08-11.md` §2.
**Wrong claim:** the free-closer paragraph in §2.
**Correct:** it is **retracted by its own §CORRECTION 100 lines later**. Anyone quoting §2
without scrolling **will publish a false claim.**
**Source:** `campaign_87` L15.

### C-30 — a 12-item retraction ledger postdates every wave-1..4 report
**Document:** `campaign_87/LONGSHOT_RESULTS.md` vs the 24 wave-1..4 agent `REPORT`s.
**Correct:** **all 24 reports predate all 12 corrections.** Any pre-2026-07-30 number must
be checked against the ledger — including **#8** ("139,878 proven k=2-irreducible" — only
105,801 were at the time, though C-11 now makes the original claim true *for a different
reason*), **#11** (16 families → **11** proven-distinct), and **#12** (11 distinct 88@5s →
**one value set in 7 gate orderings**).
**Source:** `campaign_87` L15.

### C-31 — raw `grep -c` over the append-only ledgers double-counts
**Correct:** the ledgers re-log ids across phases, so `grep -c '"unsat"'` overcounts.
**Always dedupe by id, last-wins.** This affects every ledger-derived count in the
campaign_87 tree.
**Source:** `campaign_87` L15.

### C-32 — all 72 returned `A7b_B` pod rungs are vacuous by the project's own rule
**Correct:** in **every one of the 18 families** the top (control) rung is UNSAT or
TIMEOUT, **never SAT**; and **12 families have a *failed* positive control**, which says
the claimed module size `b` was itself wrong. **Nobody ran this check.** These rungs must
not be counted as decided results.
**Source:** `campaign_87` L15.

### C-33 — the ≥5-plane blind spot was found, patched, and the patch was measured ineffective — and the scoreboard still says "open frontier"
**Documents:** the wave-6 highplane track scoreboard.
**Facts, all within 24 hours:** the skeleton-pool cross generator was capped at 4 bit
planes in **three undeclared places**; over ten families it proposed 15,299 masks with
plane histogram {2: 11,954, 3: 2,725, 4: 620, **≥5: 0**}. Auditor: *"an 87 with ANY gate
mask touching ≥5 planes escapes every T1 query past and future — structurally, not
probabilistically."* Removal cost measured at **zero**. A patch was applied
(`PLANE_CAP=8`) — and `wave6/highplane/hp_patchcheck.py` then showed **the patch draws
exactly the unbuildable kind**: `clean_and_repair` deletes two thirds (324 proposed → 107
surviving, **0.69 % of pool content**).
**Correct framing:** the hole is real, the patch does not close it, and the ≥5-plane tier
is separately measured **unbuildable** (buildable rate 0.0000 at p = 5..8). The scoreboard
must not list ≥5-plane as an open frontier awaiting compute.
**Source:** `campaign_87` L9, L2.

### C-34 — three documents say the decided splice frontier sits at n = 11; it is n = 12
**Correct:** `wave6/band_hunt/runs/ledger.jsonl` holds **two n = 12 UNSATs with controls
OK** (1,491 s and 1,046 s), and `wave6/hp_strike/runs/ledger.jsonl` holds **two more n = 12
UNSATs**. Additionally `hp_strike`'s STATUS reports **626** rows where the ledger holds
**685**.
**Source:** `campaign_87` L8.

### C-35 — theorem-grade B = 16 and B = 17 UNSATs appear in no summary document
**Correct (record incomplete, not wrong):** `wave6/dfs_par/psweep.jsonl` holds **B = 16
UNSAT on 7 of 8 anchors** (fromscratch 2.95e11 nodes, depth5, depth6, depth7 1.22e11,
thirdfamily, SIGMA5 1.39e11, alg2; SIGMA7 hit CAP at 5.82e11), and `psweep_b17.jsonl`
(written 2026-08-13 09:45) holds **B = 17 UNSAT on SIGMA7** (2.05e11 nodes, 12,678 s) **and
alg2** (2.33e11 nodes, 14,905 s), both with `"planted_control": "planted ok (17 gates)"`.
**Under the monotone-improvability lemma each certifies the whole convex down-set of that
block** — and large convex blocks were the campaign's own #1 open frontier, partially
closed on the last day with nobody recording it. The B = 18 proof work also survives in
`wave6/runpod/synced/ck_rescue/ck/SIGMA7_B18_*.ck` (36,077 bytes, **larger than the local
copy** — resume from there).
**Source:** `campaign_87` L8.

### C-36 — the campaign's own final document does not exist, and its activity log stops a day early
**Correct:** `SHUTDOWN_PLAN.md`'s final step was to write `CAMPAIGN_FINAL.md`. **It does
not exist.** And `ATTEMPTS_SINCE_PUSH.md` stops on Aug 12 morning, so **nine wave-6
subdirs created Aug 12–13 appear in it nowhere**: `discriminate`, `fusion_diag`,
`hp_strike`, `highplane`, `gauge`, `modular_syl`, `fresheyes_a`, `fresheyes_b`,
`pod_jobs`, `runpod`. **That is where the unfinished threads are** — several of this
register's and `LEADS.md`'s best entries come from exactly those directories.
**Source:** `campaign_87` L15.

---

# 6. `beat88`

### C-37 — the "22 + 5 backbone" picture is falsified and must not appear in any public structural claim
**Document:** `beat88/methods/m5_backbone/verify/PHASE2.md` §1a and anything downstream
that repeats it.
**Correct:** only **17 of 62** families have all repair slots ternary; slot sizes run to
**11**; cores run **78–83** so the "22-mask backbone" actually ranges **18–26**; and in
**7 families `k ≠ n_slots`**, including the archived 88@7 (`core=81, n_slots=6, k=7` — two
masks in the same gauge slot, the exact failure mode `b5-gauge.md` warns about, in the
wild). *"So the 22+5 decomposition is not lower-bound material. Any argument of the shape
'every 88 has this backbone, and this backbone needs 5 repairs' is dead at the first
clause."*
**Source:** `beat88` L8.

### C-38 — four different counts of the same 88 population are in circulation, unreconciled
**Documents / figures:** **33,010** (`pop88_worklist.jsonl`) / **35,999**
(`PROGRAM_STATE.md`) / **36,810** (`m2_oracle/LEDGER.md`) / **41,108** (u2's deduplicated
census). U6's notebook flags the last two as *"unreconciled and an open item"*; it was
never resolved.
**Aggravating factor:** u2 demonstrated that `cores.npy` **calls known-old 88s novel** (a
128-bit / 64-bit truncation bug).
**Consequence:** **any public claim of the form "we covered the entire known 88
population" inherits this ambiguity and must be reconciled first.** Combine with C-11 and
C-45 — the project has at least six counting bases for "how many 88s do we have".
**Source:** `beat88` U-16.

### C-39 — every timed-out result in u7 and v2 was produced at 1–2 solver workers
**Correct:** at 1–2 workers **contention manufactures UNKNOWNs**. The lane's standing
warning: **never trust an UNKNOWN from those runs in either direction.** Applies to the 11
undecided tier-2 dropscan elements, the `E ≥ 8` budget-7 run, and every other u7/v2
timeout.
**Source:** `beat88` U-8.

### C-40 — `m3_census/FINAL.md` says 4,732 orbits are unlabelled; the queue drained afterwards
**Wrong claim:** *"4,732 of my orbits are still unlabelled at close. The labelling loop
stays alive; a cut in that queue is still an 87."*
**Correct:** `code/census_inbox/` now has **0 pending, 11,219 in `processed/`, 0
unreadable**, and `census_watch.log`'s last lines read `batch: 2 labeled (102 pending)` →
`labeled 2 new; positives 1076 -> 1076`. The loop drained the queue after FINAL.md was
written and then stopped with the box. The 4,732 either got labelled (and the "12,596
novel orbits" figure was never reconciled against the 5,369 rows in `census_inbox.jsonl`)
or were never enqueued. **Reconcile `census_inbox.jsonl` (5,369 rows, dedup by `canon_id`)
against M3's 12,596 before quoting either.**
**Source:** `beat88` L14.

### C-41 — a path in the record points at a directory that does not exist locally
**Document:** `beat88/understanding/u7_representation/NOTEBOOK.md`, FINAL STATUS.
**Wrong path:** `u7_representation/data/QUARANTINE_unvalidated/` (143 decided
configurations).
**Correct path:**
`beat88/pod_salvage/pod2/u7/beat88/understanding/u7_representation/data/QUARANTINE_unvalidated`.
Harmless (the data is *void*) but anyone reading the notebook alone will conclude the data
was lost.
**Source:** `beat88` U-18.

---

# 7. Claims that are true but mean less than they read

### C-42 — the certificate repricing: every "exhaustive, zero reducible" claim in the tree inherits it
**Document:** commit `23d80d7` (unpushed, C-05); affected text includes `side_work.md`
§§10/18/21/22/26, `new-representation.md`'s 6.9 M and 2.5 M mutation sweeps,
`CERTIFICATES.md`, `campaign_87/cert_audit/`, and every lane RESULT.md quoting an empty
neighbourhood.
**What is wrong:** not the certificates — **the inference drawn from them.** The exact
decider returns "irreducible" on **97@3, 94@4, 92@5, 91@5, 90@5, 89@9 and Jean's 88@7
alike** (12,241 exhaustive k=2 windows, 8,400 sampled k=3, **zero reducible on all of
them**), while over 45 circuits with a known-smaller circuit available the distance to it
is **median 42 masks, min 3, max 48; 44 of 45 need k ≥ 8** — against a certified radius
of 3. Corroborated four independent ways: the alphabet-ladder track's own STATUS.md;
fence_sat's positive control at **0 SAT in 30 windows across slack 1–9**; and
`metareview/optimality` measuring dead-gate count and derivation rigidity as **identical to
four significant figures at 88 / 89 / 90 / 91 / 92**.
**Correct framing for any public text:** *a negative at radius ≤ 4 carries no information
about whether an 87 exists.* Search-side methods produced **locality theorems** (the 88/89
walls), **not bounds**; the honest bracket to state is the refereed `56 ≤ L(M) ≤ 88`.
**Additional inversion to fix:** `metareview/optimality` found that against a proper null,
real 88s are **4.7× more derivation-RICH, not rigid** — **the "2.3 vs 64 options/gate"
rigidity framing quoted elsewhere is backwards.**
**Source:** `root_infra` L1; `campaign_87` L1; `beat88` L15.

### C-43 — DAG statistics are published as structure and are dead as frame invariants
**Document:** `aes_mc_records/audit/MATHEMATICAL_VERIFICATION.md` (per-circuit fanout
maxima, layer histograms, cancellation counts).
**Correct:** e14 declared **all DAG statistics dead as frame invariants** — mask-identical
circuits can disagree on them; only opening-pairs and widest-gate are frame-legitimate,
and even those are not cost-relevant; *"no cost-relevant invariant is known"*. The numbers
are fine as **verification output**; they must not be presented as structural facts about
the circuits. **Also retired by e14:** "max width ≤ 8" and "no < 20 opening pairs" were
never universal.
**Source:** `records_repo` §3A item 8.

### C-44 — the distinctness instrument is superseded, and one README sentence contradicts `bounds.json`
**Documents:** `aes_mc_records/README.md:11` + the SVG alt text; `aes_mc_records/bounds.json`;
all inter-circuit distinctness claims (mask-Jaccard, 0.7 same-family threshold).
**Wrong/weak claims:** README says the depth-6 88 *"is dominated by the depth-5 one and so
sits behind it"*, while `bounds.json` keeps it as a **different family** (Jaccard 0.323).
**Correct:** e14 established the five records are **five pairwise-distinct closed
free-move orbits** (44,793 states, all 10 pairs measured by direct set intersection, four
of five perfectly rigid), and e16 extended it to **thirteen studied 88s = thirteen
pairwise-distinct orbits** over 333,396 states — a strictly stronger notion of "different
circuit" than Jaccard, and absent from the repo. So the public text's **weakest**
justification for keeping the depth-6 circuit is the one that has since been upgraded.
**Two cautions that must travel with any publication of the orbits:** free moves preserve
gate count, so **the orbit tables partition the 88 plateau and are not evidence about 87**;
and **distinct orbit does not imply distinct frame**.
**Source:** `records_repo` §3A item 7 + L8.

### C-45 — two "window" counts measure different things and must be reconciled before either is quoted
**Documents:** `aes_mc_records/PAPER.md:148` ("≈165 million exact window decisions") vs
e15 stage 1 (**15,099,957 windows swept, 0 compressible, 0 shared-helper wins**).
**Correct:** they count different objects. **Reconcile before quoting either.** Same
species of error as C-11/C-38 — and e15's own audit caught six discrepancies of exactly
this species inside one campaign (C-25).
**Source:** `records_repo` §3A items 3 and 6.

### C-46 — `PAPER.md`'s "least-certified circuits" sentence may already be stale
**Document:** `aes_mc_records/PAPER.md:143–145` — the derived 88@5 "has an empty k = 2
shell but its k = 3 shell was **never swept**, so with the 88@7 it is one of the two
least-certified circuits here."
**Correct, pending one check:** e15's d3 anchor pass closed **13/13 anchors at 27,720
triples each**. **Whether those two circuits are among the 13 anchors was not determined.**
If they are, a published gap has silently closed; if not, they remain the two named
uncertified circuits in the public record and sweeping them is a bounded, already-tooled
job. **Check before rewriting.** Related and still true (`root_infra` L3): **the 88@7 has
no exhaustive shell at any radius**, and all 47 exhaustively-certified canonical circuits
lie in Jean's lineage.
**Source:** `records_repo` §3A item 5 + L3.

### C-47 — "N verified circuits at k gates" needs a caveat: some on-disk non-88s are reducible
**Correct:** the Lemma-R tripwire returned **66 hits on 26 non-88 circuits**, and five
were already compressed with VALID witnesses: **89 → 88 ×3, 90 → 88, 90 → 89**. Most hits
sit in `campaign_87/wave5_2026-08-04/burn/mutant_cluster/quarantine_misplaced/`. **The
exact count of genuinely-irreducible non-88s has never been computed** — cheap to fix with
the same tripwire. Any public artifact count must say this.
**Source:** `experiments_late` L16.

### C-48 — two Anatomy-Theorem numerals carry caveats the lane itself does not state
**Document:** `experiments/e17_pure/DOSSIER.md` §4.6.
**(a) A11** — the numerals **7,362 / 19,490** are computed under `pbar`, **not the banked
table**; *"a successor restating A11 should re-run the `n = 88` branch under the banked
table."* Cheap (seconds), and A11 is **the first gate-count-asymmetric fact in the
programme**, so its numbers should be airtight before publication. (Note the referee
history: laneCONTRA's `n = 88` numeral **8,562 was corrected to 7,362** — an error that ran
*against* the claimant and made the asymmetry stronger.)
**(b) A10** — is **table-contingent and holds on only 5 of 8 feasible tables**, including
one table with a *strictly larger* `B` than a table it fails on. Under the banked table the
margin roughly doubles (`+0.3582982` vs `+0.1781170`), so it is not on a knife edge — but
**anyone who re-optimises the price table must re-run this check.**
**Source:** `experiments_late` L8, L9.

---

# 8. Records that do not exist, or that mislead a reader

### C-49 — 20 proven partial bounds sit in one ledger and no document collects them
**Document:** `fleet8/unified/ledger.jsonl`; partly reported in `RESULT.md` §10 item 4.
**Correct:** each is a proven `lower_bound_proven` under a timeout — **a bracket, never a
refutation** — and no document tabulates them. Notable rows: **`W3` at D = 3 exhaustively
UNSAT below k = 11**; **`U1` at D = 4 below k = 9** (both 900 s); `W3` uncapped below k = 10
at the reach cells; `U07` uncapped with a record-free menu **≥ 14** (30,565 s) against 12
at the record menu; `S2W` uncapped **≥ 11** at two record-free menus (19,185 s, 18,014 s)
against 7 at the record menu. **Off-record menus cost real gates and the brackets prove
it** — a quantitative statement about flag F1 that neither `laneMENU/RESULT.md` nor
`unified/RESULT.md` contains. Also a countable artifact class worth publishing honestly:
*"N proven partial bounds banked from timeouts."*
**Source:** `fleet5_8` L5.

### C-50 — `e16_lastwish` has no campaign-level RESULT.md
**Correct:** it has `BRIEF.md` and three excellent lane RESULT.md files, but nothing
integrates them, and e15's own RESULT explicitly notes the absence. **Three headline
results have no single citable document**: the 536 dissolution, the 333,396 F-point
states, and the forcedness refutation. Cheap and high-value for the public pages.
**Source:** `experiments_late` L20.

### C-51 — `fleet10/cleanroom` is undocumented and unreferenced anywhere in the tree
**Correct:** `grep -rln "cleanroom\|fleet10" --include='*.md' .` returns only two
`atlas/thinktank/` files, both about a *different* `cleanroom_verify.py`. fleet10 has no
RESULT.md, no README, no PREREG, no mention in any campaign document. It nonetheless holds
a from-scratch C reimplementation of Boyar–Peralta that reached **94** unaided (**93**
after SAT window repair, VALID), a measured **~12-gate penalty for forcing ρ-symmetry**
(106–108 symmetric vs 94 asymmetric), and a SAT window-repair hit rate of **1 in 2,623**.
**This is the repo's only honest answer to "how hard is 88 if you start from nothing", and
it is the number a public page most needs.** Write it a short RESULT.md before any
reorganisation.
**Source:** `fleet9_12` L5.

### C-52 — `fleet6/door` has no RESULT.md; its decisive answer lives in a 170-byte log
**Correct:** `fleet6/door/logs/door.out` is five lines, and line 5 decides `MB27B373 = 13`
(C-14). A three-line `RESULT.md` would stop the answer from being invisible.
**Source:** `fleet5_8` L4.

### C-53 — archived certificates may be wall-clock contaminated, and it was never resolved
**Documents:** `campaign_87/wave5_2026-08-04/STATE_2026-08-11.md` lines 100–102; repeated
as a standing rule in wave-6's `COMMON_BRIEF.md`.
**The warning:** *"this box's clock steps backwards and the ARCHIVED exact-decider
certificates use wall-clock deadlines (burn deciders were immunized; archived ones were
not) — audit before submitting."* Corroborated by a **negative wall time** in a ledger
(`burn/oddparity/ledger.jsonl`: `"wall": -8.5`) and by a whole segregated
`ledger_preclockfix.jsonl` (1.5 MB).
**Status: UNRESOLVED.** **Any archived certificate whose completeness depended on a
wall-clock deadline is suspect, and the publication package depends on them.**
**Source:** `campaign_87` L16.

### C-54 — small artifacts that will mislead the next reader
- `campaign_87/agents/hunt-88at6/shallow_pool/prepool_d6.pop.jsonl` is **6 lines**
  (verified) where the launcher's comment describes it as the shared shallow mask universe
  for six workers — which would explain why four cap-6 workers produced 14, 16, 66 and 264
  harvest lines after a 13,500 s budget while a sibling produced 93,621.
- `campaign_87/d3_sat/runs/splitR1.log` is a wall of
  `NameError: name 'lemma' is not defined` at `work/d3exact.py:318`, repeated for every
  instance, **with the driver never checking the exit code**.
- `campaign_87/d3_sat/runs/split_B64.jsonl` covers `n1 ∈ 0..18 ∪ 45..64` only — **the 26
  hardest middle cases (n1 = 19..44) were never run**, so the "depth-3 ≤ 96 is UNSAT"
  reading of `splitL2.log` **is not supported**.
- `campaign_87/wave5.../alphabet_ladder/CUBE_p250_K87.cubes.jsonl` is **0 bytes**.
- `campaign_87/wave6.../dfs_par/ck/SIGMA7_B17_41-42-...-97.ck` is a **134-byte stub** whose
  S-list differs by one element from the real 2.2 MB checkpoint — **easy to mistake for
  resumable state**.
- `campaign_87/wave6.../lower_bound/mip3_result_L1.json`, which `THEOREM.md` tells the
  reader to consult for the final number, **does not exist** (C-01 sibling; see
  `LEADS.md` #4).
**Source:** `campaign_87` L18, L4.

### C-55 — the atlas canonical σ table silently omits 32 bracketed strata
**Document:** `atlas/m1_sigma.json`, and every claim reading "M1 = 91" off it.
**Correct:** **32 instances timed out at the 900 s cap**, each banking
`lower_bound_proven = 10` with no upper bound (26 in `m1_wide_results/`, 6 in
`m1_v15_results/`; all `tap` with an empty or width-1 `P`). `NOTEBOOK.md` says *"Timeout
strata land as brackets … the bound-DP consumes them as-is; a timeout is never a false
exact"* — **but they are not in `m1_sigma.json` at all**, neither by instance name nor by
canonical `(kind,P,Q)` key (verified: 0 present). In **exact/pessimist** mode the DP prices
them `INF`; in **optimist** mode they are filled at the floor **7**, far below their proven
**≥ 10**.
**Consequence:** **M1 = 91 is an upper bound plus a witness, not a floor** — a point
`audit_foundations.md` §4 made and `fleet1/laneD_completions/RESULT.md` confirmed brutally
(the optimist DP over the incomplete V1.5 corpus returns **58**, not 89–91). Folding the
banked `≥ 10` brackets in can only raise the optimist floor.
**Source:** `atlas_misc` L5.

### C-56 — two documents point at artifacts that are missing or wrong
**(a) E6's headline artifact was never saved.** E6's flagship result is a **verified
88-gate depth-5 circuit** (66 CF + 22 cancelling) synthesised from a 796-pair vocabulary
with the child↔overlap assignment free. `experiments/e6_cancelplan/found/` is **empty** —
the circuit exists only as the string
`A_oracle: "gates=88 depth=5 outputs_built=32/32 problems=0\nVERDICT: VALID MixColumns
circuit"` inside one ledger row. The same is true of every stage-B control circuit
(111 g, 110 g, 109 g, 112 g, 108 g). Regenerable in principle
(`code/popcfg.py run --modeA merged --budget 88 --hint-circuit ...`, ~3,762 s), but
**nobody knows it is missing.** (`experiments_early` L8)
**(b) The shipped hunting configuration points at the wrong anchors.**
`reproduce/README.md` says the shipped `hunt87` worker set aims at "the three 88-gate
family anchors this set ships", explicitly *excluding* the two from-scratch families —
i.e. it points at the **derived** families and not at the two 88s that have **both**
exhaustive k ≤ 3 shells **and** Jean-independent lineage
(`evidence/circuits/mixcolumns_88gates_depth6.json`, `..._depth5_fromscratch.json`).
Harmless while nothing runs; the wrong default if any phase-2 work reuses `--mode fixed`.
(`root_infra` L10)
