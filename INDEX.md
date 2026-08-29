# INDEX — map of this repository

**What this is.** A search for the smallest circuit that computes the AES MixColumns
matrix (32 bits in, 32 bits out) using only 2-input XOR gates. The search phase is
**over**. The best circuit anyone here built is **88 gates**; the best proof anyone here
has is that **at least 56 gates are needed**, so the answer L(M) sits somewhere in
`56 <= L(M) <= 88`. **No 87-gate circuit was ever found** — every claim to the contrary in
this tree is a deliberate tripwire fake. One test is still running: `fleet11/laneCUBE`
is solving a SAT instance (`k = 14`) whose "yes" answer would be an 87; it is a bracket,
not a refutation, and its coverage figure moves daily. Everything below is raw campaign
material kept at its original path. **The distilled layer is `wrapup/` — start there.**

---

## Start here

| read | for |
|---|---|
| `wrapup/METHOD_CATALOG.md` | the **methods** — 309 of them in 14 families, with a "what to port first" ladder at the tail |
| `wrapup/MANIFEST.md` | **what exists**: headline numbers, every circuit, every corpus, every count with the command that produced it |
| `wrapup/CORPUS88.md` | the **88-gate corpus** — one identity, one dedup rule, the reconciliation of the competing population sizes (index: `wrapup/corpus88_index.jsonl`) |
| `wrapup/LEADS.md` | the **54 open leads**, ranked, for future 87-hunters. Not a work queue |
| `wrapup/KEEP_DELETE.md` + `wrapup/DELETION_LOG.md` | what was cleaned up, what must never be touched (34 do-not-touch entries) |
| `wrapup/CORRECTIONS.md` | the **stale-number register** — 56 figures in this tree that are wrong or superseded. Check a number here before quoting it |
| `wrapup/FROZEN_AND_FRAGILE.md` | files that break something if moved |
| `fleet11/laneCUBE/RESULT.md` + `CHECK_SOLVER.sh` (repo root) | the **live k = 14 test** and the one-command status check |
| `wrapup/reports/` | the ten long slice reports everything above was distilled from |

**The oracle.** `verify_circuit.py` at the root is the only thing that makes a claim true
here. `python3 verify_circuit.py <circuit.json>` must print `VALID`.

---

## Directories and root files

Sizes are **pre-cleanup**, quoted from the wave-1 slice reports (2026-08-29).
Flags: **LIVE** = processes running · **FROZEN-DEP** = something live imports it ·
**ARCHIVE** = finished, read-only · **TOOLING** = code you would reuse.

| path | what it is | dates | size | entry point | flag |
|---|---|---|---|---|---|
| `campaign_87/` | the original 87 hunt: six stacked waves, gitignored | Jul 26 – Aug 13 | 29 G | `FACTS.md`, then `FINAL_REPORT.md`, `LONGSHOT_RESULTS.md` | ARCHIVE |
| `beat88/` | the "beat 88" campaign: 5 method lanes, 9 understanding lanes, 26-report retrospective, 38 G of salvaged rented-machine data | Aug 13 – 16 | 47 G | `ALLOCATION.md`, then per-lane `FINAL.md` / `RESULT.md` | ARCHIVE |
| `atlas/` | the ring/ladder re-derivation of the problem; source of the `L(M) >= 56` bound | Aug 16 – 18 | 1.3 G | `NOTEBOOK.md` (+ `thinktank/` = the science) | FROZEN-DEP |
| `experiments/` | 22 numbered campaigns e1–e17 plus solo probes and the SAT benchmark package | Aug 18 – 29 | ~380 M | per-dir `RESULT.md`; best single doc `e17_pure/DOSSIER.md` | ARCHIVE |
| `fleet1/` | wave 1: region pricing (laneA), quotient-counting floors (laneB), proof side (laneC), hygiene (laneD) | Aug 19 – 20 | 15 M | per-lane `RESULT.md` | ARCHIVE |
| `fleet2/` | wave 2: the theory-first generator (laneG), the cancellation budget (laneP) | Aug 20 | 18 M | per-lane `RESULT.md` + `referee/REFEREE.md` | ARCHIVE |
| `fleet3/` | wave 3: completeness / the flagship 87 door (laneCB), the shared-plane rule + a from-scratch 88 (laneF4) | Aug 20 – 22 | 11 M | `laneF4_rule/WALKTHROUGH.md`, per-lane `RESULT.md` | ARCHIVE |
| `fleet4/` | wave 4: exact minimum-gates-under-a-depth-cap oracle | Aug 22 | 628 K | `laneDEPTH/RESULT.md` | ARCHIVE |
| `fleet5/` | wave 5: three parameter axes closed (glue, currency menus, block boundaries) | Aug 22 – 23 | 4.0 M | per-lane `RESULT.md` | ARCHIVE |
| `fleet6/` | the last in-class 87 lead decided (`door`); the integral-residual chain (laneTOOL2) | Aug 23 – 24 | 584 K | `laneTOOL2/RESULT.md`, `door/README.md` | ARCHIVE |
| `fleet7/` | Theorem U1 (making the bound unconditional *is* the original problem); the cross-lane state-of-the-problem write-up | Aug 24 | 2.2 M | `laneCONSOLIDATE/STATE_OF_THE_PROBLEM.md` | ARCHIVE |
| `fleet8/` | **the generator** — one tool that emits verified 88 and 91–116 circuits from derived structure | Aug 24 | 3.1 M | `unified/RESULT.md` (stale in places), `unified/REACHABILITY.md` | TOOLING / FROZEN-DEP |
| `fleet9/` | how big and what shape the 88 class is; two independent enumerators | Aug 24 | 3.3 M | `laneENUM/RESULT.md` | ARCHIVE |
| `fleet10/` | clean-room from-scratch calibration: self-contained search reached 93 gates VALID vs the record 88 — the measured value of project knowledge | Aug 24 | 832 K | `fleet10/RESULT.md` (written post-hoc Aug 29) | ARCHIVE |
| `fleet11/` | **the k = 14 joint SAT test.** 20+ processes running; entire directory frozen | Aug 26 – now | 880 K | `laneCUBE/RESULT.md` | **LIVE** |
| `fleet12/` | the audit-and-mutate campaign: ~200 mutations, all returned 88; 244-row audit | Aug 27 | 5.5 M | `laneALGO/ALGORITHM.md`, `laneAUDIT/AUDIT.md` | ARCHIVE (`laneHALO` FROZEN-DEP) |
| `evidence/` | the published archive: 8 record circuits, 7 untouched run archives, the certificate corpus, imported prior art | Jul 13 – 30 | 4.9 M | `RESULTS.md`, `CERTIFICATES.md` | ARCHIVE |
| `pipeline/` | the v2 record-hunting engine that found every record here, incl. all five 88s | Jul | 2.3 M | `pipeline/README.md` | TOOLING |
| `reproduce/` | one command per record, with the frozen v1 per-method code | Jul | 284 K | `reproduce/README.md` | TOOLING |
| `tests/` | 24 invariant tests, 541 lines | Jul | 128 K | `test_invariants.py` | TOOLING |
| `docs/` | `frontier.svg`, `lineage.svg` and their generators | Jul | 108 K | the scripts' docstrings | TOOLING |
| `.github/` | CI that re-verifies all 8 records | Jul | 12 K | `workflows/verify.yml` | TOOLING |
| `bi_mask_requested_evidence/` | curated, hash-manifested preservation bundle from the demand-flow campaign. Keep verbatim | Aug 15 | 404 K | its manifest | ARCHIVE |
| `joe_depth3_audit/` | three throwaway depth-3 audit scripts | Aug 14 | 16 K | none | ARCHIVE |
| `wrapup/` | **the distilled layer** — see "Start here" | Aug 29 | ~470 M | `wrapup/MANIFEST.md` | ARCHIVE |

### Root files

| file | what it is |
|---|---|
| `verify_circuit.py` | **the oracle.** Every claim in the project is defined as "this printed VALID" |
| `README.md`, `METHODS.md` | the public-facing description. Both still state the depth-4 record as 92; three verified 91 @ depth 4 circuits exist here (`wrapup/CORRECTIONS.md` #7) |
| `CHECK_SOLVER.sh` | one-command status of the live `laneCUBE` k = 14 run |
| `CITATION.cff`, `LICENSE` | DOI metadata; MIT |
| `FLEET_PLAN.md`, `SESSION_PROMPT.md` | operating instructions for the fleet campaigns |
| `side_work.md` + `side_work_REVIEW.md` | an external structural analysis and this project's adversarial review of it — the review is among the most useful method documents here |
| `new-representation.md` | a second external record: the forward/backward bi-mask representation |
| `d3_b.out`, `w1.nohup`, `wsh*.log` | dead one-line error logs from launches whose scripts no longer exist |

---

## Chronology

| when | campaign | outcome |
|---|---|---|
| Jul 26 – Aug 13 | `campaign_87` | Six stacked waves hunting an 87. None found; best is 88. Yielded a certified depth-3 floor (>= 80 gates) and — more importantly — the control audit showing the project's "nothing better nearby" results carry almost no information (likelihood ratio ~ 1.00). |
| Aug 13 – 16 | `beat88` | No 87. Produced a verified 91 @ depth 4, ~1.53 M exported oracle-checkable 88-gate records, the "88 wall" theorems (no 87 within small edits of any known 88 or 89), and two refereed lower bounds. |
| Aug 16 – 18 | `atlas` | Re-derived the whole problem in a ring/ladder frame and priced it exactly: the unconditional, refereed **L(M) >= 56** — the only lower-bound improvement in project history — plus a class optimum of 91 with a compiled witness. |
| Aug 18 (+ Aug 21/22, Aug 28) | `experiments` e1–e9, solo probes, `sat_package` | Five-agent experiment campaign under strict house rules. Headline: the refereed depth frontier **97 @ 3 / 91 @ 4 / 88 @ 5**; also the output-subset cost curve and exact re-add costs. |
| Aug 19 – 22 | `fleet1`–`fleet4` | Built the region-pricing model and its floors; closed the flagship-cell 87 door by refereed theorem; found the one missing modelling rule and used it to build a **VALID 88 from theory with no circuit search**; added a depth-capped exact oracle. |
| Aug 22 – 24 | `fleet5`–`fleet8` | Closed three whole parameter axes as free (line-set glue, currency menus over 1.4e26 configurations, 19 of 21 block boundaries); proved Theorem U1 (removing the bound's last assumption is equivalent to the original problem); shipped the unified generator. |
| Aug 24 – 27 | `fleet9`–`fleet12` | Measured the 88 plateau's shape (the record is a depth record disguised as a gate record); an independent clean-room effort reached only 93; started the live k = 14 test; ran ~200 audited one-at-a-time mutations, **every one returned exactly 88**. |
| Aug 18 – 29 | `experiments` e10–e17 | Subset pricing, hand-reconstruction of the record 88 by reasoning alone, free-move orbit closure, the **B = 56 tripwire theorem** swept clean over all 17,283 distinct 88s, and the **Anatomy Theorem** + lower-bound dossier. Every campaign ends: no 87, `56 <= L(M) <= 88` untouched. |
| Aug 29 | wrap-up | Ten slice reports written, then distilled into `wrapup/`; Tier-1 scratch deleted; this index written. |

---

*Written 2026-08-29 from the ten slice reports in `wrapup/reports/` and the
distilled files in `wrapup/`. Sizes are pre-cleanup. No number here is new: if a
figure matters, check it against `wrapup/CORRECTIONS.md` first.*
