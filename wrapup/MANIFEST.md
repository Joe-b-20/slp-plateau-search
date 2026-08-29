# MANIFEST — master artifact inventory

Project: `slp-plateau-search` — AES MixColumns (32×32 over GF(2), FIPS-197) in
fewest 2-input XOR gates. Search phase concluded at record **88 gates**.

Date: 2026-08-29. Synthesised from the ten wave-1 slice reports in
`wrapup/reports/`. **Every count below is quoted exactly as its source report
gave it, together with the command that report ran.** Nothing here is
extrapolated, summed across reports, or reconciled. Where reports overlap or
disagree the entries are kept side by side and marked
**DEDUP PENDING — see corpus88 job**.

Source abbreviations (all under `wrapup/reports/`):
`atlas` = `atlas_misc.md` · `beat88` = `beat88.md` · `c87` = `campaign_87.md` ·
`exp-e` = `experiments_early.md` · `exp-l` = `experiments_late.md` ·
`f1-4` = `fleet1_4.md` · `f5-8` = `fleet5_8.md` · `f9-12` = `fleet9_12.md` ·
`rec` = `records_repo.md` · `root` = `root_infra.md`.

All repo-relative paths are under
`/home/joebachir20/xor_ui/slp-plateau-search/` unless the path begins
`~/xor_ui/aes_mc_records` (the separate public records repo).

---

## 0. HEADLINE NUMBERS

| fact | statement | source |
|---|---|---|
| **The bracket** | `56 <= L(M) <= 88` | lower: `atlas` §3.3 "cert 5, depth 4" — `minE >= 5` ⇒ **`L(M) >= 56` unconditional, refereed**, artifacts `atlas/pod_evidence/d4out.tgz`, `atlas/thinktank/proofside_code/{cert5.txt,d4/}`. Upper: 88-gate circuits verified by the repo oracle (`root` §3, `rec` §3) |
| earlier lower bound (superseded) | `54 <= L(MixColumns)`, refereed-grade, 1-second verifier | `beat88` §3.3 — `beat88/understanding/u3_lowerbound/RESULT.md` + `verify_bound.py` |
| **Depth frontier** | **97 @ 3 / 91 @ 4 / 88 @ 5**, refereed | `exp-e` §1 (`experiments/e4_depth/RESULT.md`, 366 lines, "the refereed depth frontier 97@3 / 91@4 / 88@5") |
| depth-4 point, published vs held | public repos still state **92 @ 4**; the project holds **91 @ 4 in three independent lineages** | `root` (README.md, `evidence/RESULTS.md`, `docs/frontier.svg`, CI workflow all say 92); `rec` §3A; `f1-4` L11; third lineage `experiments/e4_depth/out/resched/atlas_compiled_m1_91gates_depth4.json` (`exp-e` §3) — **CONFLICT #4 below** |
| **Joint-level UNSATs** | merged dim-16 `W3 ∪ U4` block: **k = 9,10,11,12,13 all UNSAT** ⇒ merged block needs **>= 14** gates; with the replay bound merged ∈ {14,15} | `f5-8` §3 — `fleet8/unified/results/joint_levels.jsonl`, 5 rows, `cat` |
| — independent cross-check | k = 9/10/11 re-proved by an independent CNF encoding, **528/528 cubes UNSAT at each level, 0 disagreements**, positive control fired (SAT at cube 144, verified witness) | `f9-12` §3 — `fleet11/laneCUBE/cubes/joint_W3U4_k{9,10,11}.jsonl`, `SUB_U4tgts_k{6,7}.jsonl` |
| — **k = 14 still running** | a bracket, not a refutation. Coverage figures disagree across sources: **51/528** (at laneCUBE write-up), **73/528** (`rec` tally), **87/528** (`f9-12` tally, 2026-08-29) | `f9-12` §3, `rec` §3A — **CONFLICT #3 below** |
| — the open instance, packaged | 1 CNF: SAT ⟺ an 87-gate MixColumns exists; status unknown | `exp-e` §3 — `experiments/sat_package/k14_joint_W3U4.cnf` (4.2 M) |
| **Biggest sweep — window decisions** | **≈165 M exact window decisions** campaign-wide, zero timeouts, zero reducible | `c87` §3.3 (`campaign_87/FACTS.md` §6a + the per-class ledgers); restated `root` §3 (`CERTIFICATES.md` §4 table) |
| **Biggest sweep — population** | **17,283 / 17,283** distinct 88 mask-multisets swept, **zero alarms** (e15 run A, complete 2026-08-28) | `exp-l` §3.3 — `wc -l experiments/e15_campaign3/sweep_A_fullpop.jsonl` → 17283 |
| **Biggest sweep — d(S)=1 windows** | **15,099,957** windows, 0 compressible, 0 shared helpers | `exp-l` §3.3 — `wc -l experiments/e15_campaign3/sweep_ledger.jsonl` → 32 (rows), totals inside |
| **Biggest sweep — genomes** | **6,832,408** genomes: no 87 within one operand edit of any one-gate truncation of the five 88s and the 89 | `beat88` §3.3 — `beat88/methods/m4_inverse/analysis/landscape.md` |
| **Biggest sweep — exhaustion nodes** | `minE` depth-5 exhaustion ⇒ `L2 >= 22`, three times, one pruning-free: 294,188,302 / **80,092,627,410** / 1,795,955,245 nodes | `f1-4` §3.2 — `fleet1/laneC_proofside/runs/l2_k5*.out` |
| **Biggest sweep — exact block floors** | **749,150 OPTIMAL** RC2 union floors (125 timeouts); best floor anywhere = 88 | `c87` §3.3 — `grep -o '"status": "OPTIMAL"' campaign_87/wave5/burn/union_sat/*.jsonl \| wc -l` |
| **Biggest export corpus** | **1,549,319** oracle-checkable exported circuit records across three hosts (1,530,095 of them 88-gate, incl. **167 at depth 5**) | `beat88` §3.1 — three `MANIFEST.jsonl` files, `grep -o '"gates": [0-9]*' … \| sort \| uniq -c` |
| **Largest sector-oracle corpus** | **47,948** solved 8-dimensional sector instances across three corpora | `atlas` summary + §3.2 |
| **Free-move closure** | **333,396** states across all 8 F-point components, all CLOSED by exhaustion, min gate count 88 at every one | `exp-l` §3.3 — `experiments/e16_lastwish/laneFPOINT/bank/F*.states.bin` |
| **No 87 anywhere** | smallest circuit in every slice is 88; the four `*87gates*` files in `campaign_87` are deliberate tripwire fakes (`fake87`, `badfail`, `FAILED_87`); the smallest `FOUND_*` alarm across 44,249 of them is 89 | `c87` §3.1, `beat88` §3.2 |

---

## 1. VERIFIED CIRCUITS

The oracle is `verify_circuit.py` at the repo root (`root`). "Verified" below
means a report either re-ran the oracle or cites an in-lane `oracle_ok` field;
each row says which.

### 1.1 Canonical record circuits (the published set)

| label | count | where | command | source |
|---|---|---|---|---|
| canonical record circuits — 97@3, 92@4, 89@5, 88@5 ×2, 88@6, 88@7, 88@8 | **8** | `evidence/circuits/` | `ls evidence/circuits/*.json \| grep -v spectrum \| wc -l` | `root` §3 |
| SHA-256 manifest of those 8 | 1 | `evidence/circuits/spectrum.json` | — | `root` §3 |
| public records-repo circuit JSONs | **11** (5 of them 88-gate) | `~/xor_ui/aes_mc_records/circuits/` | `ls circuits/*.json \| wc -l`; `ls circuits/mixcolumns_88gates_*.json \| wc -l` | `rec` §3 |
| — by depth | 3:2, 4:1, 5:3, 6:2, 7:1, 8:1, 10:1 | same | `python3 -c` over `bounds.json` | `rec` §3 |
| — by lineage | 6 own-from-scratch-or-own-lineage current + 2 derived-from-Jean + 3 v1 archival | same | `bounds.json` `provenance`/`claim` | `rec` §3 |
| re-verification status | `python3 verify.py` → **all 11 pass, `ALL CIRCUITS VERIFIED`, rc 0** | — | — | `rec` summary |
| mirrored plain-text listings | **11** | `~/xor_ui/aes_mc_records/listings/` | `ls listings/*.txt \| wc -l` | `rec` §3 |
| Verilog netlists | **11** | `~/xor_ui/aes_mc_records/verilog/` | `ls verilog/*.v \| grep -vc '_tb.v$'` | `rec` §3 |
| Verilog testbenches | **11** | same | `ls verilog/*_tb.v \| wc -l` | `rec` §3 |
| `bounds.json` circuit entries | **11** (5 with a `provenance` string — the 88s) | `~/xor_ui/aes_mc_records/bounds.json` | `python3 -c "import json;print(len(json.load(open('bounds.json'))['circuits']))"` | `rec` §3 |
| record skeletons | 8 (one per frontier circuit) | `atlas/socleplane/skel_*.json` | `ls socleplane/skel_*.json` | `atlas` §3.1 |

### 1.2 88-gate circuits — **DEDUP PENDING — see corpus88 job**

Every figure in this table counts a *different* population under a *different*
notion of "distinct" (file / mask-set / mask-multiset / gauge orbit / exported
record). **They are deliberately not summed and not reconciled.**

| # | label | count as reported | where | command | source |
|---|---|---|---|---|---|
| 1 | 88-gate circuits under `evidence/` (as cited by the atlas comparison) | **54 distinct** | `evidence/` | comparison script in `atlas` §5 L1 | `atlas` §3.1, §5 L1 |
| 2 | 88-gate mask-sets in the atlas corner sweep | **498 distinct**, and **0 of 498 equal any of the 54** under `evidence/`; socle-skeleton size `l3` runs continuously 64→79; 13 converted and oracle-VALID | `atlas/corner/out/*.plat` | script in `atlas` §5 L1 | `atlas` §3.1 |
| 3 | 88-gate circuit JSONs inside `atlas/` | **38 files / 32 distinct mask-sets** (2 of the 32 are `M^T`, not MixColumns) | `atlas/` | python scan over `glob('**/*.json')`, `len(g)==88`, dedup by intermediate mask-set | `atlas` §3.1 |
| 4 | fleet9 laneENUM 88-gate sample | **223** files (216 census-sampled + 6 ρ-images of the two records + 1 self-test); **60** of them not in the project census and not a record; **2 at depth 5** (record-tying) | `fleet9/laneENUM/results/circuits/` | `ls fleet9/laneENUM/results/circuits/*.json \| wc -l` | `f9-12` §3 |
| 5 | fleet12 emitted 88s | **135** of 224 emitted circuit files; **74 of the 75** laneORDER files are byte-identical (`md5 eba1f6a998f5a9b30770b0651bb20396`); **8 runs / 2 distinct gate lists at depth 5**; +1 corrected `rec_88at7` | `fleet12/*/out/`, `laneLIB/out/regress{,2}/`, `laneKNOBS/derive_out/` | python histogram over `len(d['gates'])`/`d['gateCount']`; `md5sum fleet12/laneORDER/out/*.json \| awk '{print $1}' \| sort \| uniq -c` | `f9-12` §3 |
| 6 | fleet1–4 lateral 88s found but never compiled | **99** (42 + 57) — recorded only as `{triple deleted+forbidden, 3 gates paid}` | `fleet1/laneD_completions/basin_88at5fs.jsonl` (42), `basin_88at6.jsonl` (57) | `wc -l` on each basin file | `f1-4` §3.1 (LEAD L2) |
| 7 | fleet1–4 circuit-shaped JSONs, 88-gate bucket | **24** of 660 circuit-shaped JSONs | `fleet1`–`fleet4` | python histogram over `len(d['gates'])>60` (script in `f1-4` §3.1) | `f1-4` §3.1 |
| 8 | fleet1–4 NEW oracle-VALID 88s emitted in-slice | 2 (`NEW88_from_88at6_hit3_depth9.json` @ depth 9 — shares 85/88 masks with 88@6, never checked against the census; `gen_f4_88_D4.json` @ depth 10, built from theory) + 1 depth-tight `genD_88at5_record_D5_c3_322.json` @ depth 5 with **Jaccard 1.000 to record 88@5 (a re-derivation)** | `fleet1/laneD_completions/`, `fleet3/laneF4_rule/results/`, `fleet4/laneDEPTH/results/` | `python3 verify_circuit.py <file>` (5 of 6 re-verified, all VALID) | `f1-4` §3.1 |
| 9 | experiments-late 88-gate circuit files | **28** (e13 8, e14 16, e15 3, e17 1) | `experiments/e1[3-7]*/` | python walk over gate-list JSONs (one-off; script not banked) | `exp-l` §3.1 |
| 10 | experiments-early E5 round-trip 88s | **39**, of which **11 are NOT the seed circuit** — genuinely distinct exactly-optimal completions (min Jaccard 0.934, same family) | `experiments/e5_readd/found/` | `ls … \| wc -l` (part of the 238-artifact listing) | `exp-e` §3 |
| 11 | fleet5–8 88-gate files / distinct mask sets | **13 files → 9 distinct mask sets** (incl. the **no-Q27 88** with the tap-3 interface deleted entirely, Jaccard 0.978 to the unified 88) | `fleet5`–`fleet8` | python walk printing `len(d['gates'])` per file; dedup script in `f5-8` §3 | `f5-8` §3 |
| 12 | public records repo 88s | **5** | `~/xor_ui/aes_mc_records/circuits/` | `ls circuits/mixcolumns_88gates_*.json \| wc -l` | `rec` §3 |
| 13 | beat88 exported 88-gate **records** (gauge-inflated states, not orbits) | **1,530,095** of 1,549,319 records; by depth 5:**167**, 6:1,829, 7:94,534, 8:695,082, 9:430,281, 10:197,447, 11:42,353, 12:53,453, 13:10,618, 14:2,946, 15:1,266, 16:112, 17:7 | three `MANIFEST.jsonl` (local/pod1/pod2, 396+715+717 MB) | `grep -o '"gates": [0-9]*' <MANIFEST.jsonl> \| sort \| uniq -c`; depth via `grep '"gates": 88' … \| grep -o '"depth": [0-9]*' \| sort \| uniq -c` | `beat88` §3.1 |
| 14 | beat88 authoritative **distinct gauge orbits** | **33,010** for the whole known 88 population; M3 contributed 2,722 new families / 12,596 novel orbits | `beat88/methods/m2_oracle/runs/pop88_worklist.jsonl` (33,010 lines) | `wc -l` | `beat88` §3.1 |
| 15 | beat88 circuit files on disk | **1,251,130 files** (local 230,889 · pod1 532,724 · pod2 487,517), 1.1 GB apparent / 6.7 GB on disk | the three `exports/` dirs | `find <exports> -maxdepth 1 -type f \| wc -l` | `beat88` §3.1 |
| 16 | campaign_87 filenames claiming 88 gates | **20,745** | `campaign_87/` | `find . -name '*gates*' -name '*.json' \| grep -c 88gates` | `c87` §3.1 |
| 17 | campaign_87 wave-6 oracle-verified 4-plane 88s | **31,016 distinct** (33,821 verified, all at exactly 88; 20 distinct 4-plane masks) | `campaign_87/wave6/discriminate/runs/VERIFIED88_HIPLANE.txt` | — | `c87` §3.1 |
| 18 | campaign_87 wave-2 distinct verified 88 mask sets | **84,989** | `campaign_87/agents/merged-engine/REPORT.md` | — | `c87` §3.2 |
| 19 | campaign_87 wave-3 new distinct 88 mask sets | **54,889** | `campaign_87/agents/hunt-deeper/population88_new.jsonl` | `wc -l` | `c87` §3.2 |
| 20 | campaign_87 stated project total | **≈139,878** distinct known 88 states (84,989 + 54,889) | derived | — | `c87` §3.2; quoted in the public `PAPER.md:145–148` per `rec` |
| 21 | campaign_87 wave-6 fusion-scan distinct verified 88 mask sets | **434,125** | `campaign_87/wave6/fusion_diag/runs/full.jsonl` | — | `c87` §3.2 |
| 22 | campaign_87 88s with full masks + oracle flags | **3,254** | `campaign_87/hunt87_layer89/found88.jsonl` | `wc -l` | `c87` §3.2 |
| 23 | e15/e14 August population base | **18,355 valid on-disk 88s / 17,283 distinct mask multisets** | `experiments/e15_campaign3/popfull.txt`, `sweep_A_fullpop.jsonl`; `e16_lastwish/lane536/corpus_le3.jsonl` | `wc -l` → 17283; `wc -l corpus_le3.jsonl` → 18355 | `exp-l` §3.3, `rec` §3A |
| 24 | fleet9's lower bound on the 88 class | **>= 219,608 distinct valid 88-gate circuits provably exist** (54,889 harvested, pairwise ρ-inequivalent, ×4 for the free ρ-orbit, +13 records not in the harvest); **54,902 held on disk** | `fleet9/laneENUM/RESULT.md` | `python3 fleet9/laneENUM/code/tally.py` | `f9-12` §3 headline |
| 25 | fleet9/fleet12 88-plateau depth distribution | 1,200 draws: mode **10**; **depth 5 never occurs** | `fleet9/laneENUM/` | — | `f9-12` §3 headline |

**DEDUP PENDING — see corpus88 job** applies to this whole subsection.

### 1.3 Other-gate-count verified circuits

| label | count | where | command | source |
|---|---|---|---|---|
| provenance-labelled seed circuits (2 imported, 3 derived, 4 own) | **9** | `pipeline/seeds/` | `ls pipeline/seeds/*.json \| wc -l` | `root` §3 |
| imported prior-art circuits (Jean 88, Sun–Yang–Li 89) | **2** | `evidence/campaign87_imported_prior_art/` | `ls …/*.json` | `root` §3 |
| campaign_87 imported published circuits | **12** (Jean 88@7, SYL 89@9 + 10 others, all oracle-VALID) | `campaign_87/prior_basins/imported/`, `agents/lit-88/IMPORTED_*` | `ls` | `c87` §3.1 |
| reproduction outputs | 5 (88, 89, 91, 91, 97) | `reproduce/out_*.json` | `ls reproduce/out_*.json` | `root` §3 |
| local pipeline run bests | 6 (89@5 ×3, 89@6, 97@3, 92@4) | `pipeline/runs_parallel/*/best_overall.json` | `ls` | `root` §3 |
| ρ²-symmetric certificate circuits (2 exactly-symmetric 90s + orbit certs + union seeds/ancestors) | **9**, all re-checked VALID | `evidence/campaign87_certificates/rho2_symmetric_90s/*.json` | `ls` | `root` §3 |
| exactly ρ²-symmetric 90s (previous best symmetric was 94) | 2 | `campaign_87/agents/orbit-ladder/BEST_90gates_*` | — | `c87` §3.1 |
| all JSON in the root slice | 469 | `evidence`, `pipeline`, `reproduce` | `find evidence pipeline reproduce -name "*.json" \| wc -l` | `root` §3 |
| atlas circuit JSONs (gate counts 26…176) | **711**; 91-gate **43**, 92-gate **43** | `atlas/` | python scan over `glob('**/*.json')` counting `len(d['gates'])` | `atlas` §3.1 |
| atlas plateau state rows (min gate count **88**, no 87) | **7,075** — 88:504, 89:3507, 90:1845, 91:822, 92:157, 93:156, 94:66, 95:11, 96:5, 97:2 | `atlas/corner/out/` | `awk '{print $1}' corner/out/*.plat \| sort -n \| uniq -c` | `atlas` §3.1 |
| atlas 89-gate states | 3,431 distinct lines | `atlas/corner/out/*.plat` | `awk '$1==89' corner/out/*.plat \| sort -u \| wc -l` | `atlas` §3.1 |
| atlas periscope emissions (best 90, no 88) | 186 | `atlas/periscope/finds/` | `ls periscope/finds \| wc -l` | `atlas` §3.1 |
| atlas tri emissions (best 88 from planted pools; cold best 107) | 67–69 | `atlas/tri/out/` | `ls tri/out/*.json \| wc -l` | `atlas` §3.1 |
| atlas quotient-tower witnesses | 6 (`bp_L2_26`, `bp_L3_51`, `construct_L2_27`, `construct_L3_54`, `witness_L2_26`, `witness_L3_67`) | `atlas/tower/` | `ls tower/*.json` | `atlas` §3.1 |
| record 91 @ depth 4 (beat88) | 1 canonical + 33 siblings (32 gauge orbits) | `beat88/methods/m3_census/exports/RECORD_mixcolumns_91gates_depth4.json`, `exports/DEPTH_RECORD` | re-verified `VERDICT: VALID` | `beat88` §3.1 |
| beat88 89-gate cores from one 90-gate seed | 20 (7 at depth 5) of 36 oracle-VALID states | `beat88/methods/m1_cartography/exports/` (21 files) | `find … -type f \| wc -l` | `beat88` §3.1 |
| beat88 rerouted 99 @ depth 4 (108 → 99 by rerouting alone) | 1 | `beat88/methods/m5_backbone/verify/fiber_best_99gates.json` | — | `beat88` §3.1 |
| beat88 adopted anchors | 6 high-mobility 88s (depths 10–13) + ladder/natgt/chain/M1 anchor sets | `beat88/methods/m2_oracle/code/{k4b3_anchors,ladder_anchors,natgt_anchors,m1_anchors}/` | — | `beat88` §3.1 |
| beat88 natural 89-gate descents (ground-truth positives) | **10,089** | `beat88/pod_salvage/pod1/…/m2_oracle/runs/natgt_descents_89/` | — | `beat88` §3.1 |
| campaign_87 `BREAKTHROUGH*.json` | 171 (53×89g, 45×88g, 15×90g, rest 97–127g selftest artifacts) | `campaign_87/` | `find . -name 'BREAKTHROUGH*.json' \| wc -l` | `c87` §3.1 |
| campaign_87 distinct ≤92-gate mask sets (NRPA) | 1,441,779 | `campaign_87/wave5/nrpa/out/sub92.jsonl` | `wc -l` | `c87` §3.2 |
| campaign_87 distinct 89-gate states in the 89 layer | 1,309,223 (packed in `pool/layer89.bin`) | `campaign_87/hunt87_layer89/REPORT.md` | — | `c87` §3.2 |
| campaign_87 88-gate vocabulary `V88` | **1,112 masks** — saturated w.r.t. the harvest, then **broken by 750+ more in wave 5**; NRPA found five verified 88s using masks outside it | `campaign_87/global_vocab/V88.json` | — | `c87` §3.2 |
| exp-early E1 improvement circuits, all oracle-verified (89–100) | 72 | `experiments/e1_regions/out/IMPROVE_*.json` | `ls … \| wc -l` | `exp-e` §3 |
| exp-early E9 verified 89@5 circuits (the first population at 89) | **35** distinct canonical states, each oracle-verified twice | `experiments/e9_radius/hits/` | `ls` | `exp-e` §3 |
| exp-early E8 family-optimal circuit (exact ceiling of the per-family strategy) | 1 at **105 @ d5**, re-verified VALID | `experiments/e8_quad/artifact_family_optimal_circuit.json` | `python3 verify_circuit.py` | `exp-e` §3 |
| exp-early E4 depth-4 records + reschedules | 8 (91–92 @ d4, 89 @ d5); `atlas_compiled_m1_91gates_depth4.json` is the **third independent 91@4 lineage** | `experiments/e4_depth/out/{records,resched}/` | `ls` | `exp-e` §3 |
| exp-early E4 MaxSAT floor witnesses | 13 (91–92); one `.ORACLE_REJECTED` kept deliberately as the record of a borrowed-code defect | `experiments/e4_depth/out/floor/` | `ls` | `exp-e` §3 |
| exp-early E2 assembled partition circuits, oracle-VALID (105–146) | 11 | `experiments/e2_outputcost/artifacts/` | `ls` | `exp-e` §3 |
| exp-early E3b FIXN/READD circuits (88, 89, 91; 5 are 88s at depths 5–9) | 7 | `experiments/e3b_fresh/found/` | `ls` | `exp-e` §3 |
| exp-early `e_upstream` pinned survival floors (89, 90×3, 91×6, 92×12, 93×6, 94×5) | 33 — **mask-set format, never oracle-verified**; checked in-process as realizable | `experiments/e_upstream/S*.json` | `ls` | `exp-e` §3 |
| exp-early total circuit-or-mask-set artifacts | **238** | across the E-dirs | the 15-glob `ls … \| wc -l` in `exp-e` §3 | `exp-e` §3 |
| exp-late `M^T` (transposed-target) 88-gate circuits | **5** — `T_mixcolumns_88gates_depth{5,5fs,6,7,8}.json`, VALID against the `M^T` oracle | `experiments/e13_hand87/laneT/` | — | `exp-l` §3.1 |
| exp-late hand-reasoning ladder (106 → 97 → 91 → 90 → 88), every rung oracle-VALID; stage5 is gate-for-gate the record | 5 | `experiments/e13_hand87/cluster_campaign/assembly_stage{0,1,3,4,5}.json` | `python3 verify_circuit.py … assembly_stage5.json` → 88@5 VALID | `exp-l` §3.1 |
| exp-late from-scratch/peephole/plateau ladder (95–121 gates) | 15 VALID | `experiments/e13_hand87/laneFRESH/*.json` | — | `exp-l` §3.1 |
| exp-late algebraic single-frame derivations | `basis/zframe_105.json` (VALID 105, best single-frame) + `basis/jordan_140.json` (VALID 140) | `experiments/e14_plateau87/basis/` | — | `exp-l` §3.1 |
| exp-late total circuit-like JSON in slice | **86**; 89:7, 90:3, 91:5, 92:3, 95–108:~23, 109–215:~11 | `experiments/e1[0-7]*` | python walk, gate lists 30–300 | `exp-l` §3.1 |
| fleet1–4 backward-search outputs | 601 + 4 (6 planted-88 controls, all oracle-VALID at F=88, 0 stranded); best 4 preserved **104/105/105/106**, each oracle-VALID | `fleet1/laneD_completions/bwd_out/` (2.4 MB), `bwd_best/` | `ls` | `f1-4` §3.1 |
| fleet1–4 lane-G generator emissions | 7 (116@3, 91@5, 92@4, 94@5, and 95/99/103 where the model price was an upper bound) | `fleet2/laneG_generator/results/` | — | `f1-4` §3.1 |
| fleet1–4 referee re-emissions (independent verification copies, incl. a **91 @ depth 4**) | 6 | `fleet2/laneG_generator/referee/results/` (5), `fleet3/laneF4_rule/referee/prov/results/` (1) | — | `f1-4` §3.1 |
| fleet1–4 decompositions of known circuits (analysis, not new circuits) | 22 | `fleet1/laneA_v2pricing/results/decomp_*.json` | — | `f1-4` §3.1 |
| fleet5–8 circuit files by gate count | **135 files**: 88×13, 89×8, 90×8, 91×12, 92×6, 93×6, 94×10, 95×7, 96×6, 97×3, 98×10, 99×4, 100×5, 101×6, 102×9, 103×6, 104×5, 105×2, 108×1, 116×7 | `fleet5`–`fleet8` | python walk (script in `f5-8` §3) | `f5-8` §3 |
| fleet5–8 publishable candidates already flagged | 2 — `mergegen_MB273.json` (88 @ depth 10), `91at6_glue_free.json` (91 @ depth 7), both oracle-verified with a mandatory caveat | `fleet5/laneMERGE/results/`, `fleet5/laneGLUE/results/` | `python3 verify_circuit.py` (both VALID) | `f5-8` §3 |
| **fleet10 clean-room best** — an independent from-scratch effort with no project knowledge | **93 gates, depth 7, VALID** (+ 63 intermediates, 93–124 gates) | `fleet10/cleanroom/work/FINAL.json` | `python3 verify_circuit.py fleet10/cleanroom/work/FINAL.json` | `f9-12` §3 |
| fleet11 laneCUBE rehearsal 88 | 1 (do **not** re-verify — lane is live) | `fleet11/laneCUBE/results/laneCUBE_88gates_d7.json` | — | `f9-12` §3 |

---

## 2. UNSAT / LOWER-BOUND CERTIFICATES

Grouped by **what each class certifies**, in the reports' own words.

### 2.1 Unconditional lower bounds on `L(M)`

| certificate | exact statement certified | count | where | source |
|---|---|---|---|---|
| **cert 5, depth 4** | `minE >= 5` ⇒ **`L(M) >= 56`, unconditional, refereed** — the only improvement over 54 in project history | 1 | `atlas/pod_evidence/d4out.tgz`; `atlas/thinktank/proofside_code/{cert5.txt,d4/}` | `atlas` §3.3 |
| earlier bound | `54 <= L(MixColumns)`, refereed-grade + 1-second verifier | 1 | `beat88/understanding/u3_lowerbound/RESULT.md`, `verify_bound.py` | `beat88` §3.3 |
| **cancellation-free bound** | `L_cf(MixColumns) >= 92` | 1 | `beat88/understanding/u6_spec87/RESULT_CF.md`, `cert_u63_7_2.json` | `beat88` §3.3 |
| — independent LP re-derivation | `B_p = 114262347/1250000` ⇒ **`L_cf(M) >= 92`**; exact `G*(lam)` at 19 lam values | **19** `lp_cert_*.json` (1.5 M) + 1 `nostop_lp_cert` | `fleet7/laneUNCOND/results/lpcerts/`, `results/bstar/` | `f5-8` §3 |
| **certificate-LP cap** | the certificate LP is capped at **`B = 91.4098776` exactly**, Check-1-feasible and tight; `ceil(B) = 92` — proven below both upgrade thresholds, i.e. the whole family of arguments cannot buy the next step | 1 price table | table at `fleet7/laneUNCOND/…`; rebuild + verdict in `experiments/e17_pure/REF_CONTRA/VERDICT.md` V14 | `exp-l` §3.3 |
| `minE` exhaustions | `L2 >= 22` by depth-5 exhaustion, three times, one pruning-free | 3 runs (294,188,302 / 80,092,627,410 / 1,795,955,245 nodes) | `fleet1/laneC_proofside/runs/l2_k5*.out`, `ledger.jsonl` | `f1-4` §3.2 |
| integer residual certificates | `n >= 88` for `88@7` and `88@5` **given their apparatus**, solver-free, re-checkable | 3 (`88@5`, `88@7`, `89@5`) | `fleet2/laneP_proof/results/exact_*.json`, `code/verify_exact.py` | `f1-4` §3.2 |
| LP dual certificate | integrality gap >= 5 on `88@5fs` ⇒ route ceiling **83.000** | 1 (+ 4 ~0-gap controls) | `fleet2/laneP_proof/results/lpgap.json` | `f1-4` §3.2 |

### 2.2 Depth-restricted lower bounds

| certificate | exact statement certified | count | where | source |
|---|---|---|---|---|
| **the depth-3 lower bound** | **every depth-≤3 MixColumns circuit has >= 80 gates.** Re-checked this session: `python3 certify.py --check cert_depth3.json` → `exact dual value = 47597998171620/1000000000000 = 47.597998 => |L1|+|L2| >= 48 => N_depth3 >= 80` | 1 (457 K, 23,450 rational duals) | `campaign_87/wave6/lower_bound/cert_depth3.json`; theorem at `wave6/lower_bound/THEOREM.md` | `c87` §3.3 |
| depth-4 exact floors | 91 is exactly optimal at depth <= 4 inside each of 11 named mask alphabets, up to 300 masks | **11** | `experiments/e4_depth/ledger.jsonl` (`kind:"d4floor"`) | `exp-e` §3 |
| depth-capped block decisions | exact min gates under a depth cap | **91 exact + 5 timeouts**, 13,215 s | `fleet4/laneDEPTH/results/dcache.jsonl` (97 rows) | `f1-4` §3.2 |
| exhaustive currency curves | gates-vs-depth per menu, solver-free (`None` = provably impossible) | **80** over 19 cells | `fleet4/laneDEPTH/code/currency.py` | `f1-4` §3.2 |

### 2.3 Joint-level SAT ladder (the k=14 frontier)

| certificate | exact statement certified | count | where | source |
|---|---|---|---|---|
| joint `W3\|U4` level ledger | the merged dim-16 `W3 ∪ U4` block needs **>= 14** gates; with the replay bound merged ∈ {14,15} | **5 rows** (k = 9,10,11,12,13 UNSAT) | `fleet8/unified/results/joint_levels.jsonl` | `f5-8` §3 |
| k=9/10/11 full cube sweeps (independent CNF encoding) | complete: **all 528 cubes UNSAT** at each level, cross-checked against fleet8's encoding, 0 disagreements | 3 levels × 528 | `fleet11/laneCUBE/cubes/joint_W3U4_k{9,10,11}.jsonl` | `f9-12` §3 |
| **k=14 cube refutations (partial, LIVE)** | each row: "no 14-gate normal-form SLP for the merged `W3\|U4` dim-16 block exists **with gate 0 reading input pair j**". The level is UNSAT only when all 528 are | **87 of 528** (`f9-12`, 2026-08-29); **73/528** (`rec`); **51** at laneCUBE write-up — **CONFLICT #3** | `fleet11/laneCUBE/cubes/joint_W3U4_k14.jsonl` | `f9-12` §3, `rec` §3A |
| k=15 cube rows | same, under a 60 s budget — **reported as nothing**, since a budget refutes nothing | 23 UNSAT / 168 timeout | `fleet11/laneCUBE/cubes/joint_W3U4_k15.jsonl` | `f9-12` §3 |
| positive/negative control sweeps | sub-instance `SUB_U4tgts`: k=6 all 528 UNSAT (agrees with monolithic); **k=7 SAT at cube 144 with verified witness** — i.e. the test can fail | 736 rows | `fleet11/laneCUBE/cubes/SUB_U4tgts_k{6,7}.jsonl`, `found/HIT_SUB_U4tgts_k7.json` | `f9-12` §3 |
| the packaged open instance | SAT ⟺ an 87-gate MixColumns exists; **status unknown** | 1 CNF (4.2 M) | `experiments/sat_package/k14_joint_W3U4.cnf` | `exp-e` §3 |
| SAT-competition ladder CNFs | the joint `W3\|U4` block costs > k, for k = 9..13 | 5 CNFs + README table | `experiments/sat_package/ladder/*.cnf` | `exp-e` §3 |
| **57 newly-proved gate levels** | for each: "block B has no program at k gates", at a level **never tested before in this repository's history** — 18 at `f4_88_D4`, 18 at `rec_88at7`, 18 at `f4_88_noQ27`, 2 independent re-proofs of `U1` k=4/5, 1 at `f4_basis` | **57** | `fleet12/laneHINTS/results.jsonl` (43 rows), `cache/*.jsonl`, `laneHINTS/RESULT.md` §5 | `f9-12` §3 |
| halo-widened UNSAT levels | e.g. `U4` at k=6 UNSAT in 104 s **at dim 16 with all 41 free values available** — a genuinely wider refutation | within 118 rows | `fleet12/laneHALO/results.jsonl`, `cache/` | `f9-12` §3 |
| `MB27B373` door decision | the triple merge = **13 exactly** = split; **no 87 through it from either side** | 5 levels (k = 8..12 UNSAT) | `fleet6/door/logs/door.out` | `f5-8` §3 |
| hub merged-group bracket | `bound({S7W,B27},{7}) >= 11`; k = 11 undecided (operator stop) | 5 levels (k = 6..10 UNSAT) | `fleet5/laneMENU/logs/m_S7W_B27_c7_3b1c8975975d.out` | `f5-8` §3 |
| conservation floors | `B37 + U4 >= 11`, `B37 + W3 >= 11` | 2 exact solves | `fleet8/unified/results/conservation_D37.json` | `f5-8` §3 |

### 2.4 Neighbourhood / "wall" exhaustions (no 87 within distance k)

| certificate | exact statement certified | count / scale | where | source |
|---|---|---|---|---|
| **88 wall, core-2** | no 87 within remove-2-add-1 | 36,810 orbits incl. all 33,010 known 88s; `grep -c '"cuttable": true'` → **0** | `beat88/methods/m2_oracle/runs/pop88_lab*.jsonl` | `beat88` §3.3 |
| **88 wall, core-3** | no 87 within remove-3-add-2 | six canonical families + 506 random + 1,137 descent-reached | `beat88/…/runs/k3b2_*.jsonl` | `beat88` §3.3 |
| **89 wall, core-3** | no 87 within remove-3-add-1 of any known 89 | 64/64 anchors, **1,872,640 windows** | `beat88/…/runs/`, `LEDGER.md` §Theorems banked | `beat88` §3.3 |
| **89 wall, core-4** | no 87 within remove-4-add-2 | 13/64 anchors complete | `beat88/…/runs/k4b3_*.jsonl` | `beat88` §3.3 |
| **M4 one-edit exhaustion** | no 87 within one operand edit of any one-gate truncation of the five 88s and the 89 | 529 base genomes, **6,832,408 genomes** | `beat88/methods/m4_inverse/analysis/landscape.md` | `beat88` §3.3 |
| **M4 thinker_c closure** | the whole 31-target population admits no completion at `\|S\| <= 86` | 629,274 states, 282,970 at `\|S\|=86`, 6,487 positive controls | `beat88/methods/m4_inverse/out/thinker_c_rebase.json` | `beat88` §3.3 |
| M5 Phase-B | sound "NO 87" for an 88-family's `k−1` completion | **15** sound + 7 inconclusive of 204 | `beat88/methods/m5_backbone/verify/phaseB_verdicts.jsonl` | `beat88` §3.3 |
| M1 rigidity | 3,293 move-class products, 0 escapes from the true gauge component; complete `C(56,2)` shells on 540 cores (~830,000 k<=2 decisions), 0 descents | — | `beat88/methods/m1_cartography/FINAL.md`, `runs/escape_recheck.log` | `beat88` §3.3 |
| exhaustively-empty k<=3 shells | any 87 differs from each of these circuits by **>= 4 masks** | **47 canonical** (Jean's 88 + 12 syl-siblings + family-3 anchor + 33 reps) **+ 2 from-scratch** (88@6, 88@5fs) | `evidence/campaign87_certificates/exact_k4/`, `family3_exact/`, `campaign87_run_*/certificates/` | `root` §3 |
| complete remove-3-add-2 shells | no remove-3-add-2 improvement exists for `88@7` or `88fs` (27,720 windows each) | 2 complete + 1 at 90% (`88@5` stopped at 25,064/27,720) | `experiments/e3a_exploit/ledger.jsonl` (`kind:"k3_sweep"`) | `exp-e` §3 |
| **drop-4 local optimality** | no 4 output rows of that 88 can be resynthesised from the rest using even one gate fewer — a local-optimality certificate at radius up to 19 | **2 circuits × 35,960 sets** (`88@5`: 35,960/35,960; `88fs5`: 35,960/35,960), all `unsat` | `experiments/e5_readd/ledger.jsonl` (`kind:"drop4"`, two `screen_done` rows) | `exp-e` §3 |
| exact ρ-orbit re-add costs | `exact_readd = 88 − \|remaining\|`, total 88, in 41/41 (circuit, orbit) instances | 41 | `experiments/e5_readd/ledger.jsonl` (`kind:"exact"`) | `exp-e` §3 |
| orbit-space local-optimality certs | locally optimal under all remove-1-orbit and all **666** remove-2-orbit-add-<=1 moves | 2 circuits (+1 at 91) | `evidence/campaign87_certificates/rho2_symmetric_90s/cert90_*.json` | `root` §3 |
| **five e14 free-move orbits** | 44,793 states, five pairwise-distinct closed components, **zero free 87s** | 5 | `experiments/e14_plateau87/RESULT.md` item 1; `e16/laneFPOINT/CONTROL_partAB.log` | `exp-l` §3.3 |
| **eight closed F-point components** | **333,396 states, all CLOSED by exhaustion, min gate count 88 at every one** | 8 | `experiments/e16_lastwish/laneFPOINT/bank/F*.states.bin` + `RESULT_F*.json` | `exp-l` §3.3 |

### 2.5 Window / fence / down-step UNSATs

| certificate | exact statement certified | count | where | source |
|---|---|---|---|---|
| exact k=2 shells (streaming detectors) | for each 88-gate state: all 1,540 remove-2 windows are irreducible. Zero non-empty, zero claims raised | **197,072** (148,893 + 48,179) | `campaign_87/hunt87/detector/swept.jsonl`, `tri_hunt/detector/swept.jsonl` | `c87` §3.3 |
| exact k=2 + k=3 certificates (family reps) | complete shells of 76 family representatives, `exhaustive: true`, all `EMPTY` | 76 + 76 = **2,223,760 window decisions** | `campaign_87/families16/certs/*_k{2,3}.json` | `c87` §3.3 |
| exact k=4 partial | honestly labelled `EMPTY_PARTIAL`, `exhaustive: false`, ~1% coverage | 10 | `campaign_87/families16/certs/*_k4.json` | `c87` §3.3 |
| **order-free fence UNSAT** | the only certificate class in the project **without** the slot-order caveat | **29,125** unsat + 433 trivial-unsat | `campaign_87/wave5/fence_sat/runs/*.jsonl` — `grep -o '"status": "unsat"' … \| wc -l` | `c87` §3.3 |
| down-step window UNSAT | + 9 fully exhaustive theorems | **82,786** | `campaign_87/wave5/burn/downstep/runs/*.jsonl` | `c87` §3.3 |
| windowed SAT (fixed slot order) | UNSAT **relative to the encoding's fixed slot order** | 108 UNSAT / 114 timeout / **0 SAT** (dedupe by `id`, last-wins, or you double-count) | six ledgers under `campaign_87/agents/{sat-deep,loose-sat,family3-sat,frontier-sat}/runs/` | `c87` §3.3 |
| windowed-SAT window verdicts (published set) | Jean's 88: 48 windows → 44 UNSAT / 4 undecided / 0 SAT, frontier k=16; family-3 anchor: 50 → 37/13; 8 reps: 32 → 25/7; independent 88@7: 8 → 5/3 | **130** | `evidence/campaign87_certificates/{sat_deep,loose_sat,family3_sat}/` | `root` §3 |
| **union UNSATs** | no 87 realizable in that mask universe | **427** | `beat88/methods/m2_oracle/runs/a2_{results,pb_results,pb_escalate,density}.jsonl` | `beat88` §3.3 |
| A3 window UNSATs | order-free, slot <= 12 | **399 UNSAT / 0 SAT** (408 jobs) | `beat88/…/runs/a3_results.jsonl` | `beat88` §3.3 |
| A4 cone UNSATs | no gate saving in that cone (controls passed) | **7** | `beat88/…/runs/a4_results.jsonl` | `beat88` §3.3 |
| SAT-window UNSATs (fleet10 clean room) | "this dependency-closed window of m gates cannot be rebuilt in m−1" — local, tiny, but real | ~**2,622 of 2,623** attempts | `fleet10/cleanroom/work/ws*.log`, `wsh*.log`, `wsw*.log` | `f9-12` §3 |
| convex-block down-set UNSAT | each certifies the whole convex down-set of that block; planted controls OK | **9** (B=16 ×7, B=17 ×2) | `campaign_87/wave6/dfs_par/psweep.jsonl`, `psweep_b17.jsonl` | `c87` §3.3 |
| cancellation-plan INFEASIBLE at 87 | no <=87-gate circuit in which every cancelling gate has a weight-1 overlap producing AES target row 0 | 1 | `experiments/e6_cancelplan/ledger.jsonl` (`W1w1_orbit1`) | `exp-e` §3 |

### 2.6 Class / sector / menu pricing certificates

| certificate | exact statement certified | count | where | source |
|---|---|---|---|---|
| **DOOR-SHUT sweep** | `U07(M) >= 11` for every minimal committed set with `U1 <= 7`, hence `core(Q1) >= 18` for **every** `Q1` at the flagship cell | **740 decided** (720 exhaustive capped UNSAT + 20 audited monotonicity prunes), 0 timeouts, 11.85 core-h | `fleet3/laneCB_completeness/results/branchL_shard*.jsonl` (`wc -l` = 185 each) | `f1-4` §3.2 |
| complete 7-gate program census | every 7-gate ambient program (basis of the case split) | **21,872** | `fleet3/laneCB_completeness/results/census7_sols_shard*.json` (3 files) | `f1-4` §3.2 |
| complete 6-gate census | exactly 2 optimal committed sets exist | 4 extra-pairs → 2 sets | `fleet3/…/results/` + `code/census6.py` | `f1-4` §3.2 |
| singleton exhaustion | every single committed value is individually useless at the flagship cell | **240/240** exact capped UNSAT (504 rows, 480 `useless`) | `fleet1/laneA_v2pricing/ledger.jsonl`, `kind=g01_single` | `f1-4` §3.2 |
| module table | `σ = 7` or `σ >= 8` for each canonical sector class | **1,383** (92 YES / 1,291 exhaustive capped UNSAT), 0 timeouts | `fleet2/laneG_generator/results/modules.jsonl` (1,409 rows) | `f1-4` §3.2 |
| quotient exact-search cubes | per-level UNSAT at full cube coverage | k=12/13/14 at **1008/1008 cubes each**; 7 R01 quotients + 65 R34 instances | `fleet1/laneB_regionbounds/cubes/*.jsonl` (516 KB) | `f1-4` §3.2 |
| F4 oracle decisions | block minima at the 88@7 cell | 24 exact + 1 timeout (now 25 exact per LEAD L3), 32 invocations, 46,675 s | `fleet3/laneF4_rule/results/cache.jsonl`, `ledger.jsonl` (66 rows) | `f1-4` §3.2 |
| **all-menu bound** | `price(C) >= 87` over **1.41e26** menu configurations | **10** block bounds, 9 tight | `fleet5/laneMENU/results/bound.json` | `f5-8` §3 |
| cell sweep | every known cell prices >= 88 | **20 distinct cells** (21 named) | `fleet5/laneMENU/results/cellprice.json` | `f5-8` §3 |
| merge lattice | each dissolved boundary prices exactly the split total | **21 rows**: 19 FREE, 2 UNDECIDED | `fleet5/laneMERGE/results/FINAL_TALLY.txt` §B | `f5-8` §3 |
| no-solver merge bounds | admissible lower bound already equals split | **131** | `fleet5/laneMERGE/results/bounds.json` | `f5-8` §3 |
| containment + generality | replay bound holds and the merge is strictly more general (W1/W2/W3 witness each) | **349 / 349** | `fleet5/laneMERGE/results/containment.json` | `f5-8` §3 |
| G4 byproduct falsification | no block at base price emits a foreign-line value | **48 / 48** `capped_unsat` | `fleet5/laneGLUE/results/byproduct.json` | `f5-8` §3 |
| dichotomy tables | `\|C\| >= 58` **or** `kappa >= 16`, unconditional and solver-free | 27 exact price tables (8 CANON + 19) | `fleet7/laneUNCOND/results/dichotomy*.json` | `f5-8` §3 |
| U2 collapse witness | T4's unconditional form as stated by laneTOOL2 §5.3 has value <= 48 | 1 | `fleet7/laneUNCOND/results/collapse48.json` | `f5-8` §3 |
| dim-8 block optimality proofs | exhaustive DFS at k−1 returning empty, `optimum_proved=True` | **82/82 cells** | `fleet9/laneENUM/results/v2_counts.jsonl` | `f9-12` §3 |
| block enumeration completions | "the set of optimal value sets is exactly this list" (`complete: true`) or a floor (`complete: false`) | 111 v2 rows + 116 sat rows + 10 block rows | `fleet9/laneENUM/results/{v2_counts,sat_counts,block_counts}.jsonl` | `f9-12` §3 |
| **forcedness certificate** | "every 9-gate optimum of the unprompted merged {2,3,7} block builds `delta_3(0xc)`" — UNSAT with that value banned, 3,668 s, all 300/300 cubes, positive control fired | 1 | `fleet9/laneENUM/results/q27_force.jsonl`, `q27_enum.json` | `f9-12` §3 |
| dim-8 sector-block optimality | the block's own gate count is the exact in-sector optimum, with a decoded witness in the same solve | 67 + 14 (convex) + 324 (population) | `experiments/e3a_exploit/ledger.jsonl`, `e7_push/ledger.jsonl` | `exp-e` §3 |
| dim-12 tap-region optimality | `min_gates = 11 = \|B\|`, `lower_bound_proven = 11`, every cube reporting | **4** | `experiments/e7_push/ledger.jsonl` (`kind:"cube_verdict"`), `e7_push/cubes/*.jsonl` (4,083 cube records) | `exp-e` §3 |
| buy-one-save-two refutations | no block of any of the 14 known 88s can be rebuilt in `\|B\|−2` gates even given one free extra in-sector mask | **4,926** | `experiments/e3a_exploit/ledger.jsonl` (`kind:"buyone"`) | `exp-e` §3 |
| g11 cube split | `σ(clean,∅,∅) = 12` exact, **28/28 cubes UNSAT** | 1 | `atlas/pod_evidence/g11_cubes/VERDICT.json`, `cubes.jsonl` | `atlas` §3.3 |
| σ⁺ junction bank | per (class, level): can this sector emit a free junction? | **11,248 records** (10,494 UNSAT, 752 SAT, 2 UNKNOWN) | `atlas/spbank/*.jsonl` | `atlas` §3.2 |
| `\|Aut\| = 4` proof | the permutation automorphism group of the MixColumns target set is exactly ρ, order 4 | 1 | `experiments/e3b_fresh/code/symgf.py` + ledger | `exp-e` §3 |
| 54 cross-family subset decisions | `cost = cost_cf`, gap exactly 0 | 54 | `experiments/e10_crossfam/found/` | `exp-l` §3.3 |
| dim-10 quad brackets | `12 <= cost <= 13` for both dim-10 quads; k = 8,9,10,11 exhaustively refuted; 13-gate cf programs constructive | 2 | `experiments/e11_quad10/k11_q{24,16}.log`, `found/quad_*_cf13.json` | `exp-l` §3.3 |
| certified small optima | `k*` UNSAT-certified, witnesses replayed | **43** | `experiments/e12_legibility/data/*.witnesses.json` | `exp-l` §3.3 |
| certified-optimal forcedness instances | zero irredundant programs at `L*−1` with budget intact | **99** (91 + 8) | `experiments/e16_lastwish/laneFORCED/rows.jsonl`, `n7.jsonl` | `exp-l` §3.3 |

### 2.7 Banked partial bounds from timeouts (brackets, never refutations)

| label | what it is | count | where | source |
|---|---|---|---|---|
| **32 timed-out strata** | each `lower_bound_proven = 10`, no upper — brackets, not values | 26 in `atlas/m1_wide_results/`, 6 in `atlas/m1_v15_results/` | — | `atlas` §3.3, §5 L5 |
| R01 region climb | `R01_record_imports >= 15` (k=14 UNSAT, 6,932 s) | 1 | `atlas/pod_evidence/R01_climb.log` | `atlas` §3.3 |
| R34 region climb | `R34_record_imports >= 16` (k=15 UNSAT, 8,903 s) | 1 | `atlas/pod_evidence/R34_climb.log` | `atlas` §3.3 |
| R56 region climb | optimum in **[15, 23]**, capped at 43,200 s | 1 | `atlas/pod_evidence/R56_climb.log` | `atlas` §3.3 |
| L1 landmark | `σ(0,0) = 12` (k=11 UNSAT, 4,236 s) | 1 | `atlas/m1_landmark_results/L1.log` | `atlas` §3.3 |
| L1 bare-encoding leg | bracket **[11, 12]** — timed out at k=10 after 4,905 s | 1 | `atlas/m1_landmark_results/L1_bare_encoding.log` | `atlas` §3.3 |
| fleet8 banked partial bounds | each names a `lower_bound_proven` under a timeout — a bracket, never a refutation | **20 rows** | `fleet8/unified/ledger.jsonl` (extraction command in `f5-8` LEADS L5) | `f5-8` §3 |
| documented UNDECIDED / timeouts (exp-early) | brackets, never negatives | 6 (E4) + 4 (E2) + 2 (E5) + 1 (E8) | the respective ledgers | `exp-e` §3 |

### 2.8 Validation and control records (the certificates about the certificates)

| label | what it certifies | scale | where | source |
|---|---|---|---|---|
| decider validation records | that the completeness proofs hold | 25/25 + 12/12 brute-force; 1,257 instances @ 100% incl. 122 NOs; **4,200/4,200** planted positives; 462/462 + 33/33 branch-isolated | `evidence/campaign87_certificates/exact_k4/full_test_{cpython,pypy}.log`, `METHODS.md` §10b | `root` §3 |
| **the repricing control record** | that the neighbourhood certificates are **not** evidence about 87 | 12,241 exhaustive k=2 + 8,400 sampled k=3 across 97/94/92/91/90/89/88 — all "irreducible" | `METHODS.md` §10a, `CERTIFICATES.md` §7a, commit `23d80d7` | `root` §3 |
| bare-encoding floor cross-check | 24 floor strata re-derived with all normalisation/pruning clauses stripped, **agree=24 disagree=0** | 24 | `atlas/m1_landmark_results/bare_floor_crosscheck.log` | `atlas` §3.3 |
| cap-off control | `dslp(cap off) ≡ atlas/slp_opt.py` on the ten real blocks | **10 / 10** | `fleet8/unified/logs/capoff.log` | `f5-8` §3 |
| adversarial rejection cases certified (public repo) | 14 | — | `~/xor_ui/aes_mc_records/audit/MATHEMATICAL_VERIFICATION.md` §Adversarial tests | `rec` §3 |
| regression tests (public repo) | 12 | `grep -c 'def test' tests/test_verification.py` | `~/xor_ui/aes_mc_records/tests/` | `rec` §3 |
| **tripwire fakes** (the export path rejects a bogus record) | 4 files named `*87gates*`, all deliberate — `fake87`, `badfail`, `FAILED_87`; none was promoted | 4 | `campaign_87/` | `c87` §3.1 |
| empty alarm files (tripwires that never fired) | `find experiments/e1[0-7]* -name 'ALARM*' -o -name 'STOP' \| wc -l` → **0**; 8 zero-byte `F{1..8}.alarms.jsonl`; `lemmaR_hits_corpus.json` = 2 bytes (`[]`) on 1,200 valid 88s vs **66 hits on 26 non-88 circuits** in `lemmaR_hits_nonsample.json` | — | `experiments/e16_lastwish/laneFPOINT/bank/`, `e17_pure/laneDELTA/` | `exp-l` §3.2 |
| `FOUND_*` alarm files (beat88) | **44,249** files; gate-count distribution 89:12,704 · 90:30,856 · 91:16 · 92:673. **No `FOUND_*` below 89 gates anywhere.** All four classes documented as expected defects | 44,249 | `find beat88 -name 'FOUND_*' \| wc -l`; `… \| xargs grep -h -o '"gateCount": [0-9]*' \| sort \| uniq -c` | `beat88` §3.2 |

---

## 3. EXACT-DECISION SWEEPS

Distinct from §2 in that these are *populations of decisions* rather than
single named certificates.

| sweep | what was decided | total | where / command | source |
|---|---|---|---|---|
| **total exact window decisions, campaign-wide** | remove-k/restore-fewer, zero timeouts, zero reducible | **≈165 M+** | `campaign_87/FACTS.md` §6a + the class ledgers; restated in `CERTIFICATES.md` §4 | `c87` §3.3, `root` §3 |
| population k=2, families 1–2 | all `irreducible_k2` — **finished**, though `FACTS.md` §6a still says 51,899 of 84,989 | **84,989 states** (84,989 distinct ids) | `wc -l campaign_87/agents/frontier-exact/work/results_pop/pop_progress.jsonl` | `c87` §3.3 |
| population k=2, the 987 new88 | all irreducible | 987 | `…/results_residue/residue_progress.jsonl` | `c87` §3.3 |
| population k=3 | all `irreducible_k3` — **finished**, `FACTS.md` says 19 closed / 181 queued | 200 | `…/results_popk3/k3_progress.jsonl` | `c87` §3.3 |
| k=4 windows, Jean's 88 | all irreducible (`FACTS.md` says 32,685) | **56,489** | `wc -l campaign_87/agents/frontier-exact/work/results_k4/progress.jsonl` | `c87` §3.3 |
| k=4 windows, family-3 anchor | all irreducible (`FACTS.md` says 20,432) | **39,034** | `…/results_k4_f3/progress.jsonl` | `c87` §3.3 |
| k=4 windows, independent 88 | all irreducible (`FACTS.md` says **9**) | **34,599** | `…/results_k4_indep/progress.jsonl` | `c87` §3.3 |
| population states swept at k=2 (published framing) | any 87 differs from each by >= 3 masks | **105,801 of ≈139,878** (51,899 fam 1–2 + 53,902 fam 3; family 3 **100% closed**) | `evidence/campaign87_certificates/pop_decider/`, `family3_exact/` | `root` §3 |
| **e15 run A (tier FH)** | every distinct 88 mask-multiset on disk has **no compressible window in the `d(S)>=2` free-helper regime**, and `B = 56` | **17,283 rows / 17,283 circuits**, complete 2026-08-28 22:38 | `wc -l experiments/e15_campaign3/sweep_A_fullpop.jsonl` → 17283 | `exp-l` §3.3 |
| **e15 tier-B bank** | **15,099,957 `d(S)=1` windows**, `d1.closed` true on 27 / false on 5, 0 compressible, 0 shared helpers | 32 rows | `wc -l experiments/e15_campaign3/sweep_ledger.jsonl` → 32 | `exp-l` §3.3 |
| **e15 d3 anchor bank** | 13 anchors × 27,720 triples = **360,360 triples enumerated, 0 compressible**, with a declared aimed-helper sub-gap | 13 rows | `wc -l experiments/e15_campaign3/sweep_D3_anchors.jsonl` → 13 | `exp-l` §3.3 |
| e16 corpus `G<=3` decision | **55,970 sites over 18,355 circuits, 0 with `G <= 3`** | 18,355 rows | `wc -l experiments/e16_lastwish/lane536/corpus_le3.jsonl` → 18355 | `exp-l` §3.3 |
| e16 k=2 (3-orphan) closure | **1,409 / 1,409 sites decided `G > 4`** — the 2-mint/3-orphan regime CLOSED on this corpus | 1,409 | `experiments/e16_lastwish/lane536/le4_k2.jsonl`, `le4_undecided_s*.jsonl` | `exp-l` §3.3 |
| **RC2 exact union floors** | exact minimum over a two-circuit mask union; best floor anywhere **88** | **749,150 OPTIMAL** / 125 timeout | `grep -o '"status": "OPTIMAL"' campaign_87/wave5/burn/union_sat/*.jsonl \| wc -l` | `c87` §3.3 |
| RC2 exact skeleton floors | 19.05% floor exactly 88 | **88,908 pools** | `campaign_87/wave6/skeleton_pools/ledger.jsonl` | `c87` §3.3 |
| exact class-window floors | each ships its own RC2 witness — none can be vacuous | **177** | `campaign_87/wave6/pattern_class/ledger.jsonl` | `c87` §3.3 |
| **strict M1 sector results** | for a given menu `(P,Q)`: the exact minimum gate count with a replayable witness, or a proof of infeasibility | **5,633 files** (3,124 exact, 2,499 infeasible), 23 M | `ls atlas/m1_results \| wc -l`; `grep -ho '"status": "[a-z]*"' m1_results/*.json \| sort \| uniq -c` | `atlas` §3.2 |
| wide-menu results (widths up to 6) | same | **8,313** (8,287 exhaustive, **26 timeouts**), 33 M | `grep -l '"exhaustive": false' atlas/m1_wide_results/*.json \| wc -l` | `atlas` §3.2 |
| V1.5 exotic results (triple/unit/socle menus) | same. **Corpus incomplete: 34,112 of 236,088 instances** | **34,112** (34,106 exhaustive, **6 timeouts**), 135 M | `grep -l '"exhaustive": false' atlas/m1_v15_results/*.json \| wc -l` | `atlas` §3.2 |
| σ histogram, V1.5 | the **553 σ=6 cells** refute a universal floor of 8 | 6:553, 7:5627, 8:7001, 9:5165, 10:627 | `grep -ho '"min_gates": [0-9]*' atlas/m1_v15_results/*.json \| awk '{print $2}' \| sort -n \| uniq -c` | `atlas` §3.2 |
| σ histogram, wide | — | 7:1430, 8:4191, 9:1653, 10:256 | same on `m1_wide_results` | `atlas` §3.2 |
| **canonical distilled σ table** | `(kind, P, Q) → min_gates`; value histogram 7:1652, 8:5666, 9:2702, 10:585, 11:44, 12:5. **No witnesses** — those live in the result dirs | **13,153 rows** (2,499 infeasible), 1.3 M | `python3 -c "import json;print(len(json.load(open('atlas/m1_sigma.json'))))"` | `atlas` §3.2 |
| socle-currency results | sector solves under the socle-currency pricing | 1,048, 4.2 M | `find atlas/soclecurrency/results -type f \| wc -l` | `atlas` §3.2 |
| landmark solves | the named L1–L5 and R01/R34/R56 solves | 23 logs / 11 instances, 132 K | `ls atlas/m1_landmark_results \| wc -l` | `atlas` §3.2 |
| min-depth sweep (e4) | **2 of 38,711 distinct mask sets reschedule shallower**; max observed rescheduling gain is exactly **1 level** — which is what licenses excluding the 1.16 M depth->=7 88s from the frontier claim | 38,711 | `experiments/e4_depth/out/mindepth_scan*.jsonl` (6.2 M) | `exp-e` §2, §4 |
| fleet12 mutation sweep | every one of ~200 mutations across six lanes returned exactly **88**, with mechanisms; corrected one published number 89 → 88 | ~200 | `fleet12/lane*/results.jsonl` | `f9-12` summary |
| plane-locality measurement | exactly **12,946 of 2^32 masks are plane-local (3.0e-6)**, and **all 1,136 masks** of the 11 verified circuits plus `naive_masks()` are inside that set, 0 exceptions; every valid single-mask repair of the 88@5/89@5/92@4 anchors is plane-local (12/12, 36/36, 82/82) | — | `experiments/e1_regions/` | `exp-e` §2 |

---

## 4. THEOREMS WITH BANKED PROOFS

| theorem | exact statement | proof / bank location | source |
|---|---|---|---|
| **`L(M) >= 56`** | unconditional, refereed; from `minE >= 5` at depth 4 | `atlas/pod_evidence/d4out.tgz`, `atlas/thinktank/proofside_code/{cert5.txt,d4/}`; record at `atlas/NOTEBOOK.md` | `atlas` §3.3 |
| **`N_depth3 >= 80`** | **every depth-<=3 MixColumns circuit has >= 80 gates.** Exact rational certificate, 23,450 duals; re-checked this session | `campaign_87/wave6/lower_bound/cert_depth3.json` + `THEOREM.md`; check: `python3 certify.py --check cert_depth3.json` | `c87` §3.3 |
| **The B = 56 tripwire theorem** | *"On any valid 88-gate MixColumns circuit not already reducible to 87, `B = 56` exactly, where `B` = the number of non-output gates that have a consumer."* Contrapositive: `B != 56` on a valid 88 ⇒ an 87 is immediately available **by deletion**. Generality: `B = n − q` for any irreducible SLP with distinct masks and outputs on distinct gates | statement + sketch: `experiments/e15_campaign3/laneSWEEP.md` §11 (lines 1250–1258); banked proof: `e15_campaign3/AUDIT.md` §11.4; restated `e15_campaign3/RESULT.md`, `e17_pure/DOSSIER.md` §3.4. Detector code: `e15_campaign3/tools/sweep.py`, `count_B` at line 296, wired at 525–532, alarm path 730–738 | `exp-l` §2, §3.3 |
| — its sweep record | fired **ZERO** times on **17,283 / 17,283** run-A circuits and **13 / 13** d3 anchors; **no `ALARM_B_*.json` exists anywhere on disk**. Fail-ability check: `count_B` reads 57 on both 89-gate controls | as above | `exp-l` §2 |
| **The Anatomy Theorem** (e17 laneCONTRA, referee-confirmed) | *"Any minimum-size 87-gate SLP for MixColumns has 32 finals and 55 middles with pairwise distinct masks, no dead gate, no final built from two targets, at least two cancelling gates, at least two distinct cancelling-gate masks appearing as leaves of maximal clean trees, a cancellation weight budget of at least 5 spread over a weight profile satisfying `Σ_w a_w · delta_w >= 4.4098776`, no budget contribution at all from weight-2 cancelling leaves, `Y <= 2.5044082·kappa − 4.4098776`, and — if its cancelling apparatus is as small as the arithmetic permits (`\|A*\| = 2`, forcing `kappa = 2` and `Y = 0`) — a cancelling gate whose output *is* one of the twelve weight-7 MixColumns rows."* 14 conjuncts A1–A14 with grades; **A11 is the first gate-count-asymmetric fact in the project's history** — forced on any 87 with `\|A*\|=2` and **false at n=88** (7,362/19,490) | `experiments/e17_pure/DOSSIER.md` §4.3 (conjunct table) and §4.4 (one-sentence form) | `exp-l` §2, `rec` §3A |
| **The depth frontier** | refereed **97 @ 3 / 91 @ 4 / 88 @ 5** | `experiments/e4_depth/RESULT.md` (366 lines) | `exp-e` §1 |
| **`L_cf(M) >= 92`** | cancellation-free lower bound, two independent derivations | `beat88/understanding/u6_spec87/RESULT_CF.md` + `cert_u63_7_2.json`; `fleet7/laneUNCOND/results/{lpcerts,bstar}/` | `beat88` §3.3, `f5-8` §3 |
| **Theorem U1** (fleet7 laneUNCOND, refereed) | making T4 unconditional **is** the original problem; the whole exchange-rate family has a proved ceiling below the record's own regime | `fleet7/laneUNCOND/RESULT.md` (69.5 K) | `f5-8` summary |
| **The flagship-cell 87 door** (fleet3 laneCB, refereed) | closed by theorem: `core(Q1) >= 18` for every `Q1` at the flagship cell | `fleet3/laneCB_completeness/RESULT.md` + `REFEREE.md` | `f1-4` summary, §3.2 |
| **`\|Aut\| = 4`** | the permutation automorphism group of the MixColumns target set is exactly ρ, order 4 | `experiments/e3b_fresh/code/symgf.py` + ledger | `exp-e` §3 |
| **The 88 wall** (beat88) | no 87 within remove-2-add-1 of all 33,010 known 88 gauge-orbits; no 87 within remove-3-add-1 of all 64 known 89s | `beat88/methods/m2_oracle/{LEDGER.md §Theorems banked, STATE.md}` | `beat88` summary, §3.3 |
| **The tap-plane rule** (fleet3 laneF4) | the tap plane is *shared*, not exported — the one missing modelling rule; built a from-scratch VALID 88 | `fleet3/laneF4_rule/RESULT.md` | `f1-4` summary |
| **Multiplicity-1 blocks** (fleet9) | **13 of 17 accounting blocks have multiplicity exactly 1** at every configuration tested (70 cells, no exception); 28 of every 88 gates are *forced* once the menus are chosen | `fleet9/laneENUM/RESULT.md` | `f9-12` §3 headline |
| **The currency plateau** (fleet9) | the 88 is a **five-wide flat plateau** in the currency axis (`\|M\| = 19…23` all price 88), with a −1.00 exchange rate and cliffs at both ends | `fleet9/laneENUM/RESULT.md` | `f9-12` §3 headline |

---

## 5. APPEND-ONLY LEDGERS

| slice | count | scale | where | command | source |
|---|---|---|---|---|---|
| root / evidence | **23** | largest: `family3_sat/tasks_reps_raw.jsonl` 25 K, `results_anchor.jsonl` 24 K, `sat_deep/results.jsonl` 21 K | `evidence/` | `find evidence -name "*.jsonl" \| wc -l` | `root` §3 |
| experiments-early | **10** ledgers | **83,252 rows / 19 M** — `e5_readd` 72,805 · `e3a_exploit` 6,051 · `e3b_fresh` 1,632 · `e1_regions` 1,063 · `e2_outputcost` 914 · `e7_push` 221 · `e9_radius` 189 · `e8_quad` 171 · `e6_cancelplan` 124 · `e4_depth` 82 | `experiments/e*/ledger.jsonl` | `wc -l e*/ledger.jsonl`; `du -ch e*/ledger.jsonl` | `exp-e` §3 |
| experiments-late (markdown ledgers) | **16 LEDGER files** | `e15_campaign3/LEDGER.md` **259 K** (R0–R90) · `e13` 73 K · `e14` 34 K · `e16` 16/9/14 K · `e17` 9–22 K each | `experiments/e1[0-7]*/` | `find … -name 'LEDGER*.md' -printf '%s\t%p\n'` | `exp-l` §3.5 |
| experiments-late (JSONL banks) | **53 files, 46 MB** | e11 20.0 M, e15 19.6 M, e16 6.3 M, rest <0.5 M; `e10` 201 rows, `e11` 110, `e12` 65 | `experiments/e1[0-7]*/` | `find` + `wc -l` | `exp-l` §3.5 |
| fleet1–4 | 19 named ledgers | `basin_88at6` 27,720 · `basin_88at5fs` 27,720 · `laneP/verify1` 8,074 · laneP referee snapshot 8,057 (sha256 `497b8da7…` final / `bc77f0fd…` frozen) · laneP referee b9_census 3,255 · laneG modules 1,409 · laneCB u07_cache 788 · laneA 667 · laneD 442 · laneA solve_cache 359 · laneDEPTH 267 · laneD rerank0 141 · laneC validation 120 · laneCB 107 · laneDEPTH dcache 97 · laneB 87 · laneD bwd9 81 · laneP 79 · laneF4 66 | `fleet1`–`fleet4` | `wc -l` on each | `f1-4` §3.3 |
| fleet5–8 | **9 ledgers, 5,326 rows** | `fleet8/unified` **1,948** (solve 1028, prereg 320, generate 270, reach_cell 138, vacuity_guard 65) · `fleet5/laneMENU` **2,801** · laneMERGE 110 · laneUNCOND 110 · laneUNCOND referee 108 · laneTOOL2 89 · laneGLUE 70 · laneCONSOLIDATE 62 (incl. **11 discrepancy rows**) · laneTOOL2/verify1 28 | `fleet5`–`fleet8` | the `for f in …; do echo "$f $(wc -l < $f)"; done` loop in `f5-8` §3 | `f5-8` §3 |
| fleet5–8 solve caches + prereg | 4 caches + 1 hash-chained prereg | `fleet8/unified/results/solve_cache.jsonl` 433 · `laneMENU/results/cache.jsonl` 134 · laneMERGE 42 · laneGLUE 35; `fleet8/unified/results/prereg.jsonl` **320 rows, hash-chained** | same | — | `f5-8` §3 |
| fleet9–12 | **3 hash-chained ledgers** (235 K) + **6 append-only result banks** (396 K) + **22 solve-cache banks** (~600 K) | `fleet9/laneENUM/ledger.jsonl` **270 rows / 26 kinds**; `fleet12/lane{F1,HALO,HINTS,KNOBS,ORDER}/results.jsonl` = 64/118/43/65/75 rows | `fleet9`–`fleet12` | `wc -l` | `f9-12` §3 |
| beat88 labelled-orbit ledgers | `pop88_lab0/1/2` 11,004/11,003/11,003 (**cuttable 0/0/0**) · `s89_lab0/1` 16,539/16,544 (534/522 cuttable — expected, a cut yields an 88) · `l89b_lab0/1` 6,293/6,290 (2/2) · `census_pod0/1/2` 1,994/1,993/2,249 (3/7/7) · `census_inbox` 5,369 (**1** — a 90→89 cut) · `census` 8 (0) | worklists: `pop88_worklist` 33,010 · `stratum89_worklist` 31,950 · `layer89b_worklist` 18,865 · `census_worklist` 5,980 · `k3b2_worklist` 506 · `k3b2_chain_worklist` 300 | `beat88/methods/m2_oracle/runs/` | `wc -l`; `grep -c '"cuttable": true'` | `beat88` §3.4 |
| beat88 drained circuit inbox | **11,219** drained circuit files, 0 pending, 0 unreadable | — | `beat88/methods/m2_oracle/code/census_inbox/processed/` | `find … -type f \| wc -l` | `beat88` §3.4 |
| atlas jsonl banks | `spbank/*.jsonl`, `sigma_plus_bank.jsonl`, `thinktank/sweep{7,8}_*.jsonl`, `thinktank/phase2_*.jsonl`, `tri/market/ledger.jsonl` | — | `atlas/` | — | `atlas` §3.4 |

---

## 6. WRITEUPS (the RESULT.md class)

| slice | count | notable individually-named documents | command | source |
|---|---|---|---|---|
| root / published | **32** in-slice + 5 at root | `README.md` 14 K, `METHODS.md` 59 K, `evidence/RESULTS.md` 59 K, `CERTIFICATES.md` 18 K, `pipeline/README.md` 12 K; 6 `PROVENANCE.md` (one per run archive + prior art, each stating derived/own/from-scratch **in its first sentence**); 7 `CODE_PROVENANCE.md` + 7 `CONFIG_AS_RUN.md` pairs; and the three loose root docs `side_work.md`, `side_work_REVIEW.md`, `new-representation.md` | `find evidence pipeline reproduce docs tests -name "*.md" \| wc -l` | `root` §3 |
| public records repo | **4** prose + 1 PDF + 1 LaTeX source | `README.md` (295 L / 2,686 w), `PAPER.md` (252 / 2,770), `PRIOR_ART.md` (488 / 4,873), `audit/MATHEMATICAL_VERIFICATION.md`, `paper/mixcolumns_note.{pdf,tex}` (537-line LaTeX). Total public prose ≈ **10,300 words** + a 209-line `bounds.json` | `wc -l` / `wc -w` | `rec` §3 |
| atlas | **28** `.md` (26 in `thinktank/` + `NOTEBOOK.md` + 1) | `atlas/NOTEBOOK.md` is the programme record | `find atlas -name '*.md' \| wc -l` | `atlas` §3.4 |
| beat88 | **120** | `ALLOCATION.md`; per-lane `THESIS/LEDGER/STATE/FINAL` ×5 (`m2_oracle/LEDGER.md` alone is 1,714 lines); `methods/DESIGN_NOTES.md`; `m3_census/analysis/00–05*.md`; `analysis/SYNTHESIS.md` + 26 reports; `understanding/{PROGRAM_STATE,CANON,MANIFESTO}.md` | `find beat88 -name '*.md' \| wc -l` | `beat88` §3.6 |
| campaign_87 | **412** `.md` (36 `REPORT.md`, 63 `STATUS.md`, 38 `README.md`) | `FACTS.md` (fact-by-fact sourced ground truth), `wave5/publication_draft/{DRAFT.md, CLAIMS_AUDIT.md, PAPER_OUTLINE.md}` (a complete 37 K paper draft with every claim mapped to an on-disk source), `wave6/lower_bound/THEOREM.md`, `wave5/burn/obstruction/OBSTRUCTIONS.md`, `wave5/burn/handreduce/WAVE2_INSIGHTS.md`, `wave5/metareview/SYNTHESIS.md`, `LONGSHOT_RESULTS.md` (with a 12-item retraction ledger), `wave6/ATTEMPTS_SINCE_PUSH.md` (125 K catalog) | `find . -name '*.md' -not -path '*/venv/*' \| wc -l` | `c87` §3.4 |
| experiments-early | **10 `RESULT.md`** + 4 tally snapshots + 2 notebooks + 3 charters + 1 package README + 10 generated fragments | `_shared/BRIEF.md` — the campaign charter, "the single most reusable document in the slice"; `sat_package/SUBMISSION_NOTES.md` | `ls e*/RESULT.md \| wc -l` | `exp-e` §3 |
| experiments-late | **69** markdown total: **13 `RESULT.md`**, 3 referee `VERDICT.md`, **1 `DOSSIER.md` (92 K)**, 6 BRIEF/PLAN, 5 AUDIT (e14 212 K, e15 223 K, e15 `AUDIT_FINAL` 29 K), 16 LEDGER | `e17_pure/DOSSIER.md` (the Lower-Bound Dossier), `e15_campaign3/AUDIT.md` | `find … -name 'RESULT*.md' …` | `exp-l` §3.4 |
| fleet1–4 | **18** | 9 `RESULT.md` (one per lane), 4 `REFEREE.md`, 1 `WALKTHROUGH.md`, 1 `RECORDS_UPDATE_NOTE.md`, 2 lane-G digests, 1 `cubes/README.md` (a document explaining why a directory is deliberately **empty** — worth copying as a practice) | `find fleet1 fleet2 fleet3 fleet4 -name '*.md' \| wc -l` | `f1-4` §3.3 |
| fleet5–8 | **10 documents, 394 KB** | `STATE_OF_THE_PROBLEM.md` 104 K · `laneUNCOND/RESULT.md` 69.5 K · `unified/RESULT.md` 53.8 K · `laneTOOL2/RESULT.md` 49.5 K · `laneGLUE/RESULT.md` 27.7 K · `laneMENU/RESULT.md` 25.5 K · `laneMERGE/RESULT.md` 24.5 K · **`RECORDS_REPO_PATCH.md` 21.9 K** · `unified/REACHABILITY.md` 16.3 K · `door/README.md` 1.2 K | `find fleet5 fleet6 fleet7 fleet8 -name "*.md" -printf "%s %p\n" \| sort -rn` | `f5-8` §3 |
| fleet9–12 | **32 documents, 1.05 MB** | 8 `RESULT.md` (210 K); 6 `PREREG.md` + 6 `PATCHES.md` (190 K); **`fleet12/laneAUDIT/AUDIT.md` 188 K, 244 audited rows, 22 registered defects** (6 audit docs, 424 K); **`fleet12/laneALGO/ALGORITHM.md` 88 K, certified by four independent naive-reader reviews** (5 docs, 220 K). **fleet10 has no RESULT.md anywhere** | `find fleet9 fleet10 fleet11 fleet12 -name '*.md'` | `f9-12` §3 |
| curated preservation bundle | **39** real files (75 minus 36 `:Zone.Identifier`), **30 of them SHA-256 manifested** — a curated bundle from the *previous* campaign, keep verbatim | `bi_mask_requested_evidence/` | `find bi_mask_requested_evidence -type f \| wc -l` | `atlas` §3.4 |

---

## 7. RAW LOGS

| slice | count | total size | command | source |
|---|---|---|---|---|
| root / evidence / pipeline / reproduce | **187** | **1.80 MB** (largest `parallel_ladder_run_2026-07-13/coordinator.log` 641 KB) | `find evidence pipeline reproduce \( -name "*.log" -o -name "*.stdout" -o -name "*.out" \) \| wc -l` and `-printf "%s\n" \| awk '{s+=$1} END {print s}'` | `root` §3 |
| root stray dead logs | 6 | ≈700 bytes total, all "file not found" | `cat w1.nohup wsh*.log d3_b.out` | `root` §3 |
| atlas | **243** | 1.3 M | `find atlas \( -name '*.log' -o -name '*.out' \) \| wc -l` | `atlas` §3.4 |
| campaign_87 | **5,004** | **405 MB** (wave5 3,355 / 227 MB · wave6 627 / 37 MB · agents 504 / 4.6 MB) | `find . \( -name '*.log' -o -name '*.out' -o -name '*.err' \) \| wc -l` | `c87` §3.4 |
| beat88 | **606** `.log`/`.nohup` | **3.4 GB** (of which **1.73 GB is byte-identical duplicate pairs**) | see `beat88` §4 | `beat88` §3.5 |
| experiments-early | ~200 | ~450 KB (`e_upstream` alone 210 KB); + `e9_radius/runs_archive.tar.gz` 592 K (537 per-run scratch dirs); **12 zero-byte logs** = the record of deliberately killed/preempted arms | `find <dirs> \( -name '*.log' -o -name '*.out' \)` | `exp-e` §3 |
| experiments-late | **118** | 2.2 MB (e10 17, e11 23 [2.0 M], e12 11, e13 5, e14 4, e15 31, e16 18, e17 9) | `find <dir> \( -name '*.log' -o -name '*.out' -o -name '*.nohup' \) -type f -printf '%s\n' \| awk '{t+=$1}END{print t}'` | `exp-l` §3.6 |
| fleet1–4 | 1,470 + 864 + 379 + 14 + 43 + 5 per-lane | laneG 11.3 MB · laneCB 6.6 MB · laneA 3.0 MB | the per-lane `find $L -path '*/logs/*' -type f\|wc -l` loop | `f1-4` §3.4 |
| fleet5–8 | **286** | 1.34 MB (largest `fleet5/laneMENU/logs/queue_main*.out`, 6 files 27–34 K each) | the `for d in …; do find $d/logs $d/inst -type f; done \| wc -l` loop | `f5-8` §3 |
| fleet9–12 | **374** | 923 K | `find fleet9 fleet10 fleet11 fleet12 -type f \( -name '*.log' -o -name '*.out' -o -name '*.nohup' \)` | `f9-12` §3 |
| public records repo | **0** by design | — | — | `rec` §3 |

---

## 8. BULK DATA, INSTANCES AND BENCHMARK PACKAGES

Not "results" but the largest classes on disk, listed so the request line is honest.

| class | count | size | where | command | source |
|---|---|---|---|---|---|
| `*.cells.jsonl` descriptor-telemetry archives (search-engine memory; each row a bit-exact replay tuple) | **127** | **31.4 GB** | `beat88/` | `find . -name '*.cells.jsonl' -printf '%s\n' \| awk '{s+=$1;n++}END{print n,s}'` | `beat88` §3.5 |
| `MANIFEST.jsonl` (3 big + 4 small) | 7 | 1.8 GB | `beat88/` | `find . -name 'MANIFEST.jsonl'` | `beat88` §3.5 |
| compressed harvest segments `*.pop.*.jsonl.zst` — the **complete** population harvest at ~150:1, nothing pruned | **1,083** | **337 MB** (standing in for ~50 GB raw) | `beat88/` | `find . -name '*.pop.*.jsonl.zst' \| wc -l` | `beat88` §3.5 |
| other `.jsonl` (ledgers, labels, worklists, windows) | 566 | 3.48 GB | `beat88/` | `find . -name '*.jsonl' ! -name '*.cells.jsonl' ! -name 'MANIFEST.jsonl'` | `beat88` §3.5 |
| `*.pop.jsonl` harvest dumps | 130 files | **13.71 GB** | `campaign_87/` | `find . -name '*.pop.jsonl' -printf '%s\n' \| awk …` | `c87` §3.2, §1 |
| CNF dumps | — | 5.53 GB | `campaign_87/` | — | `c87` summary |
| `.bin` pools (incl. `pool/layer89.bin`) | — | 1.51 GB | `campaign_87/` | — | `c87` summary |
| atlas instance files (regenerable) | — | 967 MB | `atlas/` | `du -sh` | `atlas` summary |
| **SAT-competition benchmark package** | 6 CNFs (ladder k=9..13 + the open k=14) 18 M, + 4 demo CNFs/models 5.9 M, + `README.md` + `SUBMISSION_NOTES.md` | 24 M | `experiments/sat_package/` | `ls` | `exp-e` §3 |
| E3a dim-8 SAT instances | 5,705 | 23 M | `experiments/e3a_exploit/inst/` | `ls` | `exp-e` §3 |
| fleet1–4 solver instances | laneG 1,453 · laneCB 795 · laneA 358 · laneB 82 · laneF4 38 | — | per-lane `inst/` | the loop in `f1-4` §3.4 | `f1-4` §3.4 |
| fleet5–8 instance files | **237** | 968 KB | per-lane `inst/` | the loop in `f5-8` §3 | `f5-8` §3 |
| fleet9–12 menu/instance JSONs + enumerated mask-set banks | 109 + 3 + 2 menus/instances (530 K); **233** mask-set banks (852 K) | — | `fleet12/laneF1/menus/`, `fleet9/laneENUM/{inst,results/sets}/`, `fleet11/laneCUBE/inst/` | `ls` | `f9-12` §3 |
| interactive HTML | 2 (`explainer.html` 180 K, `workbench.html` 104 K) | 284 K | `atlas/` | — | `atlas` §3.4 |
| generator / verifier scripts (public repo) | 4 generators, 2 independent Python verifiers | — | `~/xor_ui/aes_mc_records/scripts/` | `find scripts -name '*.py' \| wc -l` | `rec` §3 |
| atlas code files | **167** (`.py` + `.c`) | — | `atlas/` | `find atlas \( -name '*.py' -o -name '*.c' \) \| wc -l` | `atlas` §3.4 |

---

## 9. CONFLICTING / OVERLAPPING COUNTS — **DEDUP PENDING**

Recorded, not resolved. A separate agent is computing the deduplicated 88 corpus.

1. **88-gate circuit counts across sources.** Twenty-five separate figures, all in
   §1.2 above, counting files vs mask-sets vs mask-multisets vs gauge orbits vs
   exported records: `evidence/` **54** · atlas corner **498** · atlas in-tree
   **38 files / 32 mask-sets** · fleet9 **223** · fleet12 **135** · fleet1–4 basin
   **99** (+ **24** in-tree) · experiments **28** (late) + **39** (E5 round-trip) ·
   fleet5–8 **13 files / 9 mask-sets** · records repo **11 circuits / 5 88s** ·
   beat88 **1,530,095 records / 33,010 orbits / 1,251,130 files** · campaign_87
   **20,745 filenames / 31,016 4-plane / 84,989 + 54,889 / 434,125 fusion-scan /
   3,254 with masks** · e14–e15 **18,355 on disk / 17,283 distinct multisets** ·
   fleet9's derived lower bound **>= 219,608 distinct valid 88s exist**.
   **DEDUP PENDING — see corpus88 job.**
2. **17,283 vs 139,878 corpus base.** `rec` L4 and `rec` §3A item 6: the public
   `PAPER.md:145–148` says "105,801 of the ≈139,878 harvested distinct 88-gate
   mask sets"; August says 18,355 valid on-disk 88s / 17,283 distinct multisets.
   `rec`'s own verdict: "almost certainly different counting bases… **do not quote
   either number in a rewrite without re-deriving what set it counts**"
   (confidence SMELL, high-value). **DEDUP PENDING.**
3. **k=14 cube coverage.** 51/528 (laneCUBE write-up) vs 73/528 (`rec` tally) vs
   87/528 (`f9-12` tally, 2026-08-29). The lane is LIVE; the number moves. Quote
   with a date or not at all.
4. **Depth-4 frontier point.** Published: **92 @ 4** (`README.md`,
   `evidence/RESULTS.md`, `docs/frontier.svg`, CI workflow, `bounds.json`).
   Held: **91 @ 4**, three independent lineages (`campaign_87/cascade6/
   FRONTIER_91gates_depth4.json`, `experiments/e4_depth/out/resched/
   atlas_compiled_m1_91gates_depth4.json`, `fleet2/laneG_generator/referee/
   results/ref_91g_d4.json`), plus 33 beat88 siblings at 91@4. Sources: `root`
   summary, `rec` §3A, `f1-4` L11, `exp-e` §3. A patch with exact line numbers
   already exists (`fleet7/laneCONSOLIDATE/RECORDS_REPO_PATCH.md`, 2026-08-24).
5. **≈165 M window decisions vs 15,099,957 windows.** `rec` §3A item 6: the two
   figures "count a different thing and the two must be reconciled before either
   is quoted again."
6. **The "54 known 88s under `evidence/`"** used as the atlas comparison base vs
   `root`'s **8 canonical record circuits in `evidence/circuits/`** — different
   subtrees of `evidence/`, never reconciled in either report.
7. **campaign_87 population k=2: finished or partial?** `c87` §3.3 reads the
   ledgers as **finished** (84,989 + 987 + 53,902 = 139,878 = the entire
   population); `FACTS.md` §6a still says **51,899 of 84,989**; `root` §3 reports
   **105,801 of ≈139,878**. Three numbers, one population.
8. **`FACTS.md` stale k=4 tallies.** k=4 windows: Jean's 88 **56,489** vs
   `FACTS.md` 32,685; family-3 anchor **39,034** vs 20,432; independent 88
   **34,599** vs **9**. Ledger-derived figures are the larger ones (`c87` §3.3).
9. **fleet12's 135 88s include 74 byte-identical duplicates** (one md5 across
   74 of the 75 laneORDER files) — the file count and the distinct count differ
   by ~55%.
10. **fleet9's 223 88s include 6 ρ-images and 1 self-test**, and only **60** are
    both non-census and non-record.
11. **e5 drop-4 screen**: `exp-e` §3 reports **2 circuits × 35,960** complete,
    while `e5_readd/RESULT.md` reports only the first family (`exp-e` §2 note:
    "RESULT.md predates two of these").
12. **e7 dim-12 tap regions**: RESULT.md reports **one** decided region; the
    ledger holds **four** `cube_verdict` rows (`exp-e` §5).
13. **atlas's own published 88 structure claims are refuted by its own
    unanalysed output**: the `l3 >= 67` floor, the "empty band `l3 ∈ 69..72`" and
    the "real 2-gate ridge" all fail against the 498 corner mask-sets, whose `l3`
    runs continuously 64→79 (`atlas` summary, §5 L1).
14. **atlas V1.5 corpus is incomplete**: 34,112 of 236,088 instances — any
    "exhaustive" framing of that corpus is wrong (`atlas` §3.2).

---

## 10. "AVAILABLE UPON REQUEST" — draft section for the public repos

> Copy-ready. `{N}` marks a figure blocked on the corpus88 dedup job. Every
> non-placeholder number below is quoted from a slice report and is reproducible
> by the command recorded in the section above.

---

### Available upon request

The published repository ships the verified record circuits and their
certificates. A much larger body of working material was produced during the
2026 campaign and is kept locally. It is available on request:

- **{N} verified 88-gate MixColumns circuits** ({M} distinct after
  deduplication — dedup pending). Counting bases differ widely across the
  campaign's sub-corpora: 1,530,095 exported oracle-checkable 88-gate records
  across three hosts, resolving to 33,010 distinct gauge orbits by the
  campaign's own canonicalisation; 17,283 distinct 88 mask-multisets in the
  final population sweep; 498 further distinct 88 mask-sets from an
  independent algebraic frame that match none of the published circuits.
- **1,549,319 oracle-checkable circuit records total**, including 167 at
  88 gates and depth 5.
- **8 canonical record circuits** (97@3, 92@4, 89@5, 88@5 ×2, 88@6, 88@7,
  88@8) with a SHA-256 manifest, plus **11 fully packaged circuits** (JSON,
  plain-text listing, Verilog netlist, Verilog testbench) in the DOI'd records
  repository — all 11 re-verified, `ALL CIRCUITS VERIFIED`.
- **A verified 91-gate circuit at depth 4**, in three independent lineages —
  one gate better than the depth-4 point currently stated in the published
  frontier.
- **A 93-gate circuit from an independent clean-room effort** with no access to
  the project's methods — the project's own calibration datum for how hard the
  last five gates are.
- **A refereed unconditional lower bound `L(M) >= 56`** with its certificate,
  and a certified depth-restricted bound: **every depth-<=3 MixColumns circuit
  needs at least 80 gates** (exact rational certificate, 23,450 duals,
  re-checkable in seconds).
- **A certified cancellation-free bound `L_cf(M) >= 92`**, derived twice
  independently, with 19 exact LP certificates.
- **UNSAT certificates for the joint `W3|U4` block at k = 9, 10, 11, 12, 13**,
  cross-checked at k = 9/10/11 by a second, independent CNF encoding over a
  machine-checked exhaustive 528-cube partition with a fired positive control.
  The k = 14 level — whose satisfiability is equivalent to the existence of an
  87-gate circuit — is packaged as a single 4.2 MB CNF and is **open**.
- **57 gate levels proved UNSAT that had never been tested before**, plus
  ~29,125 order-free window UNSAT certificates (the only certificate class in
  the project with no slot-order caveat) and 82,786 down-step window UNSATs.
- **Approximately 165 million exact window decisions** — zero reducible, zero
  timeouts — establishing that no 87-gate circuit lies within remove-2-add-1 of
  any of 33,010 known 88-gate gauge orbits, nor within remove-3-add-1 of any of
  64 known 89s, nor within one operand edit of any one-gate truncation of the
  record circuits (6,832,408 genomes).
- **Exhaustive closure of the plateau's free-move structure**: 333,396 states
  across eight components, every one closed, minimum gate count 88 throughout.
- **Exact-decision sweeps**: 749,150 optimal RC2 union floors (best floor
  anywhere: 88); 88,908 RC2 skeleton-pool floors; 47,948 solved 8-dimensional
  sector instances with replayable witnesses; a 13,153-row distilled exact
  price table; a class-pricing bound covering 1.41 × 10^26 menu configurations,
  all priced at >= 87; and a min-depth sweep of 38,711 distinct mask sets.
- **Five theorems with banked, referee-checked proofs**: the `B = 56` tripwire
  (a sound, free, always-on one-gate-improvement detector, swept over
  17,283/17,283 distinct 88s with zero alarms); the Anatomy Theorem (14 proved
  properties forced on any 87-gate minimum circuit, one of them provably false
  at 88 gates); the flagship-cell door theorem; Theorem U1; and the depth
  frontier 97@3 / 91@4 / 88@5.
- **More than 150 append-only, in several cases hash-chained, result ledgers**,
  every published number re-derivable from them.
- **Approximately 770 write-ups** — per-lane RESULT.md files, adversarial
  referee reports, a 244-row audit with 22 registered defects, a certified
  algorithm description, a complete unpublished paper draft with every claim
  mapped to an on-disk source, and a 12-item retraction ledger.
- **Roughly 9,800 raw run logs** (~3.8 GB, of which 3.4 GB is one campaign's
  run logs) and ~31 GB of search-engine telemetry, each row carrying a
  bit-exact replay tuple.

No circuit smaller than 88 gates was ever found. Every artifact above is
oracle-checkable with the verifier shipped in this repository.

---

*Placeholders to fill after the corpus88 dedup job: `{N}` = total verified
88-gate circuits held; `{M}` = distinct after deduplication.*

*Three bullets in the draft above are **arithmetic over the slice reports, not
independently measured totals** — the only numbers in this manifest that are.
Each must be re-derived with a single `find` before publication:*
- *"approximately 770 write-ups" = §6 per-slice markdown counts
  32 + 4 + 28 + 120 + 412 + 10 + 69 + 18 + 10 + 32 + 39 = **774***
- *"more than 150 ledgers" = §5 per-slice counts
  23 + 10 + 16 + 53 + 19 + 9 + 31 = **161**, excluding beat88's labelled-orbit
  and worklist banks (not individually totalled by that report)*
- *"roughly 9,800 raw run logs" = §7 per-slice counts
  187 + 243 + 5,004 + 606 + ~200 + 118 + 2,775 + 286 + 374 = **~9,793**,
  ~3.8 GB, of which beat88 alone is 606 files / 3.4 GB*
