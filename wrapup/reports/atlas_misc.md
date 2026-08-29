# Slice report: atlas + joe_depth3_audit + bi_mask_requested_evidence + d3_b.out

Agent model: Opus 5 (1M). Date: 2026-08-29.

**Summary.** `atlas/` is a self-contained three-day research programme
(2026-08-16 → 2026-08-18) that re-derived the whole MixColumns problem in a new
algebraic frame — a ring/ladder/sector decomposition — and then priced it
exactly. It is by far the densest methodological deposit in the repository:
**28 writeups, 167 code files, 26 distinct methods, and three exact-oracle
corpora totalling 47,948 solved 8-dimensional sector instances.** Its headline
results are (a) the refereed unconditional bound **L(M) ≥ 56** (the only
improvement over 54 in project history), (b) the **M1/V1.5 class optimum = 91**
under six independent re-pricings with a compiled VALID 91-gate witness, and
(c) a large body of measured structure laws about why 88 keeps appearing. The
1.3 GB is almost entirely **instance files (967 MB, regenerable) and expanded
result dirs that are byte-identically duplicated by two small tarballs already
on disk** — about **1.20 GB is reclaimable with zero information loss**. The
distilled science lives in ~15 MB of `.md` + `m1_sigma.json` + code.
`bi_mask_requested_evidence/` is a curated, hash-manifested preservation bundle
from the *previous* campaign and must be kept verbatim. `joe_depth3_audit/` is
three throwaway scripts. `d3_b.out` is a Python "file not found" traceback.

**One live finding.** Section 5 lead L1: `atlas/corner/out/*.plat` contains
**498 distinct 88-gate mask-sets, none of which is any of the 54 known 88-gate
circuits under `evidence/`**, and their socle-skeleton size `l3` runs
**continuously from 64 to 79**. I converted and verified 13 of them with
`verify_circuit.py` (all VALID). This **refutes**, from the atlas session's own
unanalysed output, three claims the session itself published: the 88 floor
`l3 ≥ 67`, the "empty band `l3 ∈ 69..72`", and the "real 2-gate ridge"
separating two 88 families.

---

## 1. INVENTORY

### 1.1 Top level of the slice

| path | size | what it is |
|---|---|---|
| `atlas/` | 1.3 G | the ladder/atlas programme, 2026-08-16..18 (concluded) |
| `bi_mask_requested_evidence/` | 404 K | curated preservation bundle from the *previous* (demand-flow / bi-mask) campaign |
| `joe_depth3_audit/` | 16 K | three ad-hoc scripts auditing depth-3 circuits |
| `d3_b.out` | 123 B | a Python traceback: `can't open file '.../deep_extras.py'` |

Commands: `du -sh atlas joe_depth3_audit bi_mask_requested_evidence d3_b.out`

### 1.2 `atlas/` directory map

```
du -sh atlas/* | sort -rh
```

| subdir | size | files | what it IS | documented? |
|---|---|---|---|---|
| `m1_v15/` | 934 M | 236,088 | **V1.5 sector INSTANCES** (exotic-shape menus). Generated, not solved. | via NOTEBOOK + `thinktank/v15b_gen.py` |
| `m1_v15_results/` | 135 M | 34,112 | V1.5 **solved** instances (SAT witness + full per-level UNSAT log each). Corpus is **incomplete** (34,112 of ~242k). | yes |
| `tri/` | 80 M | 105 | tri-directional (forward+backward+middle) market search workspace; 80 M is `tri/market/round_00*/demands.jsonl` | `thinktank/tri_search.md` |
| `m1_wide_results/` | 33 M | 8,313 | wide-menu (width ≤ 6) sector results, **COMPLETE** | yes |
| `m1_wide/` | 33 M | 8,313 | the matching instances | yes |
| `m1_results/` | 23 M | 5,633 | the original strict M1 sector results, **COMPLETE** (3,124 exact + 2,499 infeasible + 10 landmark/shim files) | yes |
| `m1_instances/` | 23 M | 5,623 | the matching instances (audited bit-for-bit against an independent FIPS-197 derivation) | yes |
| `thinktank/` | 13 M | 635 | **the science**: 26 agent writeups + their code + logs + sub-workspaces (`basin/`, `backward/`, `transposed/`, `proofside_code/`) | yes, heavily |
| `corner/` | 11 M | 1,757 | corrected-ruler plateau-walk lab (C engine `walk*.c` + driver + 1,589 `.plat` state dumps) | `thinktank/ideas_strange_corners.md` |
| `soclecurrency/` | 4.4 M | 1,072 | ladder DP with **socle** currency + over-charge-free supply pricing | code docstrings only — **opaque, no RESULT.md** |
| `periscope/` | 3.7 M | 235 | second plateau walker (shape-weight softmax + tap-vocabulary injection) with logs/harvest/finds | `thinktank/ideas_open.md` |
| `spbank/` | 2.5 M | 50 | σ⁺ (junction-capacity) sweep bank: 11,248 verdict records | yes |
| `v15_partial.tgz` | 1.8 M | — | **byte-identical archive of all 34,112 files of `m1_v15_results/`** (verified) | no |
| `m1_sigma.json` | 1.3 M | — | **the canonical distilled sigma table**: 13,153 `(kind,P,Q) → min_gates` rows | yes |
| `wide_results.tgz` | 548 K | — | **byte-identical archive of `m1_wide_results/`** (8,313 files) | no |
| `tower/` | 200 K | 34 | quotient-tower lane (L1/L2/L3 sub-problems, C branch-and-prune, witnesses) | `thinktank/phase2_tower.md` |
| `socleplane/` | 188 K | 26 | socle fibration: skeletons of every record, `phi(l)` completion machinery | `thinktank/third_frame.md` |
| `explainer.html` / `workbench.html` | 286 K | 2 | interactive explainer + workbench (audited; explainer's "15/16" panel was a forecast, later made true) | yes |
| `pod_evidence/` | 96 K | 8 | drained pod artifacts: 28/28 g11 cubes UNSAT, R01/R34/R56 climb logs, `d4out.tgz` (cert-5 depth-4 exhaustion) | yes |
| `m1_landmark_results/` | 84 K | 23 | the named landmark solves (L1..L5, R01/R34/R56, bare-encoding cross-check) | yes |
| `m1_landmarks/` | 48 K | 11 | their instances | yes |
| `viz_data.json`,`editor_data.json` | 72 K | 2 | data behind the HTML; **no generator exists in the repo** (audit finding) | flagged |
| root `*.py` / `*.log` | ~250 K | 40 + 12 | the frame toolkit (`ring/anatomy/valuation/sectors/lines/economy/sector_view`), the solvers (`sigma_sat.py`, `slp_opt.py`), the DPs (`m1_search*.py`), the compilers (`assemble.py`, `compile_config*.py`), the relaxation bounds (`free_junction_bound.py`, `exact_free_targeted.py`) | `NOTEBOOK.md` |
| `__pycache__/` (7 dirs) | 696 K | — | build artifacts | — |

`atlas/NOTEBOOK.md` (970 lines, 57 KB) is the chronological record and the
entry point. It is unusually good: it carries its own **ERRATA** section
(E1–E5) and marks claims (M)easured / (D)erived.

**Documented vs opaque.** `thinktank/` is exhaustively documented (26 `.md`).
`corner/`, `periscope/`, `tower/`, `socleplane/`, `tri/`, `spbank/` are each
covered by exactly one thinktank writeup. **`soclecurrency/` (4.4 M, 1,072
files) is the one subdir with no writeup at all** — only `dp.py`'s docstring
explains it (a ladder DP with socle currency and the dcost over-charge fix).

### 1.3 The small directories

**`joe_depth3_audit/`** — 3 scripts, ~2.2 KB total, dated 2026-08-14:
- `mc_weights.py` — builds the 32×32 MixColumns GF(2) matrix from scratch and
  prints row weights (`20×5 + 12×7`).
- `decompose.py` — per-depth gate histogram of the 97-gate depth-3 circuit,
  reporting `32 + E + P` where E/P are depth-1/2 populations.
- `scan.py` — scans `evidence/`, `reproduce/`, `beat88/` for all depth-3
  circuits and tallies `(N, E, P)` profiles.

All three use **relative** paths and only run from the repo root. Nothing writes
output; results were read off the terminal and are not preserved.

**`bi_mask_requested_evidence/`** — 75 files, 3 numbered sections, plus
`README.md` and `SHA256SUMS.txt` (30 hashed files). It is a *response to a
preservation request* about the previous campaign, and it is scrupulous about
what was lost:
- `01_near26/` — 1 of 18 near-miss 26-mask modules, **losslessly recovered**
  from the preserved uphill-29 witness. The other 17 raw files are gone and
  were deliberately **not** regenerated.
- `02_backbone_defects/` — the 22-mask backbone's defect layer: 36-mask defect
  vocabulary, 19 backbone bypasses (CSV + raw), 4 double-defect bridge JSONs,
  `BACKBONE_DEFECT_FINDINGS.md`.
- `03_trajectories_and_metrics/` — the original bi-mask/demand-flow analyzer,
  aggregate metric CSV, demand-flow + routing-LNS search code, and the
  deterministic 108→100→99→98 repro chain. The specific 97@3 LNS output is
  **not preserved**.
- **36 `*:Zone.Identifier` files (144 K)** — Windows alternate-data-stream junk
  from a WSL copy; not in `SHA256SUMS.txt`.

This bundle is the direct input to `thinktank/phase2_e3.py` and the whole
finisher lane — the 22-mask backbone, the 13 edges, the 1,291 edge-free triples
were all recovered from `02_backbone_defects/`.

---

## 2. METHODS

26 catalogue entries. Ordered by family. "Generality" answers: what would have
to change to aim it at `aes_inv_mixcolumns`?

### ring-ladder-frame
- **Family:** structural-analysis (the frame everything else sits in).
- **What it does:** Rewrites the 32×32 GF(2) problem as arithmetic in
  `R = F256[v]/(v^4)`. Input bits and output rows both become units of a rank-1
  R-module under the trace pairing; the whole matrix is one formula
  `M_T = (1+v+v^2)(y·I8 + v·X^T)`. The 32-dim problem splits into 8 coupled
  8-dim "sector" problems (one per bit position) that are all **the same**
  problem, glued in a ladder, with four "taps" coupling sectors to a hub.
- **Twist vs siblings:** unlike every earlier representation, it is *graded* by
  the nilpotent `v = y+1`, so it explains rather than describes.
- **Measured:** decomposition verified constructively; all 8 sectors carry the
  same 4 targets; `assemble.py` compiles abstract sector programs into real
  mask circuits (naive scheme → 116 gates, VALID). Re-derived from scratch by
  an adversarial auditor with zero shared code: **duality 3000/3000 pairings,
  z-iso 1000/1000, all 32 `c·z(bit_i) == z(row_i)`, tensor rank of c = 2,
  socle identity 8/8, zero convention slips.**
- **Cost:** hours of derivation; all checks seconds.
- **Code:** `atlas/ring.py`, `sectors.py`, `lines.py`, `sector_view.py`,
  `anatomy.py`, `valuation.py`, `economy.py`, `assemble.py`.
- **Logs/results:** `NOTEBOOK.md` §1–8; `thinktank/audit_foundations.md`.
- **Generality:** MC-HARDCODED in its constants, **CIRCUIT-GENERIC in method**
  for any circuit that is multiplication by a fixed element of a local ring
  (inverse MixColumns is exactly that: same R, different `c = 14+11v+13v²+9v³`
  in the standard basis). Porting = recompute `c`, the dual basis, and the tap
  set; everything downstream is parameterised.
- **Phase-2 verdict:** **keeper — the single most reusable asset in the slice.**

### economy-census
- **Family:** structural-analysis.
- **What it does:** Classifies every gate of a circuit as column-pure /
  diagonal / mixed / glue by its dual-basis support, and tabulates per-circuit
  budgets.
- **Twist:** the classifier's well-definedness is a *theorem* (all 28 pairwise
  sector intersections computed; exactly six are non-zero and each is
  1-dimensional), not a test.
- **Measured:** ~80 of 88 gates live in the 8 sectors; glue 3–9 in the 88s vs
  15 in 92@4 and 24 in 97@3. **The glue law:** across all 74 off-line gates of
  eight frontier circuits, *every one* lies in a tap triple, 0 violations —
  and a null model puts the chance baseline at 0.150–0.189. **But** a later
  audit showed the law is non-discriminating (97@3 satisfies it 24/24) and
  FALSE under operand-accounting (88@6 gate 79 has support {1,2,7}).
- **Code:** `atlas/economy.py`, `lines.py`; audit in
  `thinktank/audit_foundations_code/`.
- **Generality:** CIRCUIT-GENERIC given a frame.
- **Phase-2 verdict:** keeper as an instrument; its "better ⇒ more disciplined"
  reading is **refuted** (`audit_inference.md` §2.2: 98@3, the worst circuit in
  the repo, has 6 off-line gates — fewer than three of the five 88s).

### exact-sector-oracle (σ tables)
- **Family:** exact-oracle / SAT.
- **What it does:** Solves the 8-dimensional sector problem exactly — minimum
  XOR gates to reach 4 fixed targets from a raw set plus a purchased "currency
  menu" `(P,Q)` — by iterative-deepening SAT (UNSAT at k, SAT at k+1).
- **Twist:** three independent solver lineages (`sigma_sat.py`, `slp_opt.py`,
  and a from-scratch bitmask checker `chk.py`), cross-checked.
- **Measured:** `m1_results` 5,623 instances, **3,124 exact + 2,499 infeasible,
  zero timeouts**; `m1_wide_results` 8,313 (26 timeouts); `m1_v15_results`
  34,112 (6 timeouts). Value histogram over the strict corpus
  `{7:222, 8:1475, 9:1049, 10:329, 11:44, 12:5}`. Floor law
  `σ_floor(|P|,|Q|) = 12 − min(|P|,3) − h(|Q|)`, verified 33/35 cells.
  **σ(0,0) = 12 exact** (k=11 UNSAT cost 4,236 s single-lineage, later closed
  multi-lineage by a 28-way cube split, 28/28 UNSAT). **σ_tap ≡ σ_clean on all
  466 shared (P,Q)** — the "tap premium" is entirely dcost + span.
  Integrity: 604/604 witnesses re-replayed shared-nothing; 1,002/1,002
  infeasibility verdicts re-derived by independent rank test; 12,637
  monotonicity extensions, 0 violations.
- **Cost:** the corpora took pod-days; per-instance seconds to ~1 h, 900 s cap.
- **Code:** `atlas/sigma_sat.py`, `atlas/slp_opt.py` (41 KB, with
  `slp_opt_selftest.py`, 2406/2406), `m1_search.py::gen()`.
- **Logs/results:** `m1_results/`, `m1_wide_results/`, `m1_v15_results/`,
  distilled into `m1_sigma.json` (13,153 rows).
- **Generality:** **CIRCUIT-GENERIC.** `slp_opt.py` takes a JSON instance
  `{dim, inputs, targets}` and returns the exact minimum SLP. It is the single
  most directly portable tool here — point it at any small linear problem.
- **Phase-2 verdict:** **keeper. Reusable as-is for any new circuit's sector
  subproblems.**

### m1-chain-dp
- **Family:** class-pricing / DP.
- **What it does:** Prices the whole line-disciplined ("M1") architecture class
  exactly: choose a currency menu per column, pay `Σ_k σ(P_k,Q_k)` from the
  oracle table plus the supply bill, minimise over all menu assignments by a
  chain DP. Runs in `optimist` (missing entries priced maximally favourably)
  and `pessimist`/`exact` modes to bracket.
- **Twist vs siblings:** the cost function is *exact table lookup*, not a
  heuristic — so the optimum is a real class optimum, and it **compiles**:
  `compile_config.py` turns the winning config into a verifiable circuit.
- **Measured:** bracket `[75,92]` → `[85,92]` → **exactly 91** on the complete
  table. Compiled witness `compiled_m1.json` = **91 gates, VALID**. Later
  `compiled_all7.json` = **91 gates, VALID, depth 5, ZERO glue**. Records are
  88, so **the records' out-of-class mechanism is worth exactly 3 gates**.
  Re-priced **six** times (shared constituents, junctions at real cost,
  free tap-1 passengers, σ⁺-exact free sets, width-uncapped, V1.5 vocabulary)
  and returned 91 every time. Width-uncapped confirmed on 8,313 wide instances,
  zero timeouts.
- **Cost:** DP itself minutes; the table behind it is the expensive part.
- **Code:** `atlas/m1_search.py`, `m1_search_v2.py`, `m1_search_wide.py`,
  `m1_batch.py`, `compile_config.py`, `compile_config_v2.py`,
  `thinktank/v15_dp.py`, `thinktank/compile_config_v3.py`,
  `soclecurrency/dp.py`.
- **Generality:** MIXED. The chain topology is the ladder's; the DP + table
  lookup + compile-and-verify pipeline is generic.
- **Phase-2 verdict:** **keeper — the template for "price an architecture class
  exactly and compile the winner".** Caveat: 91 is an **upper bound + witness**
  for the class, not yet a floor (see §5, L5).

### v15-exotic-currency-dp
- **Family:** class-pricing (twist on `m1-chain-dp`).
- **Twist:** adds *exotic* column currency — triples, units, and the socle `v³`
  — that M1 forbids, priced at true build cost via exhaustive BFS over the
  4-dim currency space (487 menus per column).
- **Measured:** **class optimum still exactly 91.** The mechanism is real
  (σ = 6 exists, first ever measured: `σ(clean; P={6,7,8,a}, Q={2,a,c}) = 6`,
  k=5 UNSAT / k=6 SAT, witness verified) but **wash-priced**: the "q-face tax"
  makes the neighbouring sector pay exactly +1, on all six decider rows.
  σ = 6 requires width-4 p-menus with ≥2 exotic levels: 45/54 such classes give
  6; **0/26** width-3 perfect chains and **0/43** width-4 1-exotic ever do; and
  **no σ = 5 has appeared anywhere in 2,600+ exact V1.5 entries.**
  First verified socle-currency circuit: `thinktank/v15_rich91_circuit.json`,
  91 gates, VALID.
- **Cost:** 236,088-instance corpus on 28 pod workers; only 34,112 landed.
- **Code:** `thinktank/v15_dp.py`, `v15b_gen.py`, `compile_config_v3.py`.
- **Generality:** MIXED, same as its parent.
- **Phase-2 verdict:** keeper as a *pricing pattern* ("give the model the
  vocabulary the records actually use, then see if it still can't reach them").

### junction-capacity-sweep
- **Family:** exact-oracle probe (twist on `exact-sector-oracle`).
- **What it does:** Asks whether a sector program can emit a "junction"
  (`3d_k·t`) for free, in two dual forms: hand it in as a *free input* and ask
  for `σ−1`/`σ−2`, or add it as an *extra target* and ask for `σ`. Monotonicity
  lets one call decide 21 pairs.
- **Measured:** **capacity is exactly 1, proven** — over all 222 σ=7 classes,
  0 admit two free junctions; 1,332 asks, 1,313 UNSAT, 78 SAT, 0 unresolved.
  Capacity-**2** does exist off the floor (12 instances in the σ=8 stratum, all
  tap, all `(|P|,|Q|)=(4,4)`), refuting an earlier "capacity ≤ 1" law; capacity
  3 is 0/13. The double-diagonal junction routing **works and saves exactly 1
  gate** (94-gate VALID vs 95-gate VALID) — but the flat basin re-absorbs it
  and the junction-enabled DP is still 91.
- **Code:** `thinktank/capacity_sweep.py`, `junction_dp2.py`,
  `junction_assemble.py`, `atlas/sigma_plus_sweep.py`; bank
  `atlas/spbank/*.jsonl` (11,248 records: 10,494 UNSAT / 752 SAT / 2 UNKNOWN).
- **Generality:** **CIRCUIT-GENERIC probe shape** — "add candidates as free
  inputs vs as extra targets, batch by monotonicity" is reusable anywhere.
- **Phase-2 verdict:** keeper (the probe); the specific junction question is
  settled.

### free-junction-relaxation-bound
- **Family:** class-pricing (deliberate over-relaxation).
- **What it does:** Instead of running 1,332 exact asks, *assume the answer is
  yes everywhere* subject only to capacity 1, and see what the DP can then
  reach. If the bound is ≥ 91, no sweep outcome can change the verdict.
- **Measured:** MODE=none → **91** (complete). MODE=tap1 → **89** (complete).
  MODE=junction → best 90, **run truncated, no optimum line**. So the shortcut
  did **not** discharge the sweep. The cheap exact follow-up
  (`exact_free_targeted.py`) pinned MODE=tap1 back at **91**; MODE=both
  **stopped at 800 of 3,249 frames**, best 91.
- **Cost:** seconds–minutes (the whole point).
- **Code:** `atlas/free_junction_bound.py`, `atlas/exact_free_targeted.py`,
  `atlas/run_ef.sh`. Logs `atlas/fjb.log`, `atlas/eft.log`,
  `exact_free{,_slow,_partial}.log`.
- **Generality:** CIRCUIT-GENERIC pattern (relax to decide whether an expensive
  sweep is worth running).
- **Phase-2 verdict:** keeper as a pattern; the specific run is **unfinished**
  (§5, L4).

### transposed-frame (Tellegen)
- **Family:** structural-analysis.
- **What it does:** Reverses every edge of the SLP DAG. `L(M) = L(M^T)` exactly;
  reading masks in the bit basis instead of the trace-dual basis gives a
  *different* ladder with better structure.
- **Twist:** the transposed ladder is a **connected path** 0-1-…-7 with one
  exotic element, versus the forward frame's broken path plus three diagonals.
- **Measured:** all 11 repository circuits transpose to same-count VALID `M^T`
  circuits and back (banked:
  `thinktank/transposed/mixcolumns_T_88gates_from_88at{5,7}.json`). Depth is
  *not* preserved (88@5 → 88@7). Seven of eight transposed sectors are
  raw-free; **zero diagonals in any transposed record**; glue 65/65 in one
  mechanism, no exceptions (null probability ≈ 1e-60). Off-ladder bill drops
  from 9–17 to 4–8. `r(mask weight, co-mask weight) = −0.62..−0.73` — old
  search instruments rank `M^T` by a nearly opposite statistic.
- **Code:** `thinktank/transposed/{tframe,tring,census,bias,localize,
  verify_mt,run_transpose}.py`.
- **Generality:** **CIRCUIT-GENERIC — Tellegen applies to every linear
  circuit.** The most portable single idea in the slice.
- **Phase-2 verdict:** **keeper.** Note (§5, L3): nobody ever ran a *search* on
  `M^T`, despite the measured r ≈ −0.7.

### transposed-chain-dp / split-q / sigma-aug / lazy-oracle-loop
- **Family:** class-pricing (four escalating twists on `m1-chain-dp`).
- **Measured, in order:** transposed V1 optimum **92** (optimist also 92;
  forward control reproduces 91 on the same code path). Split-q sector-7 oracle:
  `σ_split ≥ 9` everywhere machine-proven, `K = 80` exact ⇒ model optimum in
  `[89,92]`. `σ_aug` (supply obligations folded in as extra targets, removing a
  double-count): drops to **83** — *excludes nothing and exhibits nothing*.
  Lazy oracle loop: diagnosed **non-convergent** (surrogate slack is uniform,
  not concentrated; plateau at 83); the sole rescue (additive premium ≥ 4)
  refuted by an exact counterexample (measured gap +2); additive ceiling 85.
- **Code:** `thinktank/transposed/{transposed_dp,splitq,splitq_dp,aug,aug_dp,
  lazy_dp}.py`.
- **Generality:** MIXED. The **"add the supply elements as extra targets to
  remove double-counting"** trick and the lazy-oracle-loop are fully general.
- **Phase-2 verdict:** **dead-end, and explicitly declared settled** — a model
  built to host the records' own routing still does not price an 88. Valuable
  precisely because it is a *closed* lane.

### quotient-tower (L1/L2/L3)
- **Family:** structural-analysis + exact search.
- **What it does:** Solves MixColumns modulo `v^k` — a genuinely smaller
  standalone circuit problem at each rung — with Boyar–Peralta using an
  **exact** subset-sum distance table (full BFS over the whole quotient space).
- **Measured:** `L2 ≤ 26` (`tower/bp_L2_26.json`), `L3 ≤ 51`
  (`tower/bp_L3_51.json`) — **16 below** the earlier 67. Lower bounds
  `L2 ≥ 17`, `L3 ≥ 33`. Tower `0 → 26 → 51 → 88`, steps **26, 25, 37** — so
  **the socle rung is the expensive one**, inverting the earlier reading.
  Search-free constructions verified at 27 and 54. **Measured verdict: a
  generic SAT climb is not a route to exact L2** (50 min on 3 cores did not
  close even k=17, its first level).
- **Code:** `atlas/tower/{quotient,extract,structure,lb,lift,analyze,
  verify_all}.py`, `bp.c`, `bp2.c`, `run_bp.py`.
- **Generality:** **CIRCUIT-GENERIC** for any linear circuit over a filtered
  ring; the BP-with-exact-distance-table is generic outright.
- **Phase-2 verdict:** keeper.

### socle-fibration
- **Family:** structural-analysis.
- **What it does:** Every circuit splits **exactly** as `|C| = l3 + s3`
  (skeleton mod socle + socle-level fibre); `L = min_Q |Q| + rho(Q)`. Gives a
  2-D "socle plane" in which every circuit is a point.
- **Measured:** `(l2,l3,s3)` for 9 circuits; the five 88s spread over
  `l3 ∈ {67,68,73,74,77}`. **Honest self-falsification recorded**: glue does
  *not* die in the quotient, so "the trick is 3 socle gates" is wrong.
  A later audit correctly noted `l + s = 88` is an **identity**, not a measured
  tradeoff line.
- **Code:** `atlas/socleplane/{core,build,cover,moves,mu,phi,recskel,readoff,
  bitcost,sweep}.py`; third independent implementation in `corner/socle.py`
  (reproduces the published `l3` table 9/9).
- **Generality:** CIRCUIT-GENERIC for any local ring with a socle.
- **Phase-2 verdict:** keeper — and see §5 L1: the socle plane is where my
  slice's live finding lives.

### corrected-ruler (line-normalised shape weight)
- **Family:** search-heuristic / instrument repair.
- **What it does:** Replaces `popcount(mask)` — which every search in this
  project's history used to rank and cap candidates — with a **line-normalised
  shape weight** `W`: decompose into v-coordinates and count minimal atoms over
  the redundant generator set. O(1) per mask via a 256-entry BFS table.
- **Twist:** it is the *fix* for a proven bias: the same abstract element weighs
  ~1.5× more on a "tap line", so popcount structurally excluded the exact
  vocabulary the last 3 gates are made of (the excluded vocabulary is **exactly
  1,516 elements**).
- **Measured:** `W` halves the artificial cross-line spread (512 → 256).
  It **orders the frontier where popcount anti-orders it**:
  `Σ popcount` is *lowest* for 97@3 (370) and 98@3 (365) and highest for the
  88s (372–394); `Σ W` reverses it — 88s 297–319 < 92@4 331 < 98@3 342 <
  97@3 360. On **descent** it wins (mean best 90.33 vs popcount's 91.67 from a
  97@3 start, equal CPU, 42 runs) and is the only arm besides its sibling to
  reach 89. On **plateau walking** it is null (753 distinct states vs
  popcount's 756 — while *no* preference gives 3,784, a 5.0× effect that is
  about having a tie-break at all). It confirms its own prediction and then
  kills it: heavy-mask emission rate is 1.11/1000 (popcount arm) vs 18.27/1000
  (`W` arm) — but the 14 known 88s sit at **7.31/1000, between the two**, so
  neither ruler points where 88s live.
  **Also killed: "the best circuits destroy the most information."** y-basis
  cancellation spans 9–33 and separates the frontier; in the v-basis it is
  **flat at 46–56 for every circuit from 88 to 98**.
- **Cost:** 166 walks, equal-CPU accounting via `clock()`, 60–300 CPU-s/cell.
- **Code:** `atlas/corner/{ruler,census,census2,socle,envelope,driver,
  analyze}.py`, `walk.c`, `walk3.c`, `walk4.c`, `walk5.c`, `*.jobs`.
- **Generality:** the ruler is dual-basis-specific; the **seven-arm equal-CPU
  A/B with two null and two *inverted* control arms, plus a temperature sweep**
  is fully general and unusually well-designed. Port that harness.
- **Phase-2 verdict:** **keeper, and under-exploited** — see §5, L1 and L2.

### periscope-plateau-walk
- **Family:** plateau-search (sibling of the corrected-ruler walker).
- **Twist vs `corrected-ruler`:** enumerates the **complete** valid-repair set
  (the shipped engine truncated to 4 by `(hamming_wt, -reuse)`), adds
  **tap-vocabulary injection** — with p ≈ 0.1 inject a protected extra gate from
  the excluded vocabulary, i.e. a deliberate 89-excursion, so later repairs can
  reroute through it (the shipped walk was **provably monotone**: no uphill at
  all). Plus victim retry, tabu deques, and a descent alarm.
- **Measured:** planted positive passed — from a naive 116-gate seed, **31
  cascaded descents to a VALID 90-gate circuit in 150 s**. Its own night fleet
  reached best 90 (186 emitted circuits in `periscope/finds/`, 2,741 harvest
  rows). **No sub-88.**
- **Code:** `atlas/periscope/{engine,shapes,census,pop_census,harvest_check,
  shell_probe}.py`, `run_night.sh`.
- **Generality:** **CIRCUIT-GENERIC** engine; only `shapes.build_dictionary` is
  frame-specific.
- **Phase-2 verdict:** keeper — the only walker in the project with a
  non-monotone move.

### exact-3-gate-finisher
- **Family:** exhaustive local closure.
- **What it does:** Freezes a circuit's "exterior", deletes a triple of module
  masks, and asks exactly whether ≤ k arbitrary XOR gates can complete all 32
  targets with the deleted triple forbidden. `k = 3` ⇒ a new 88 geometry;
  `k = 2` ⇒ an **87**.
- **Twist:** the move set is **proved complete for k ≤ 3** (four-shape case
  analysis + a role argument), strictly stronger than the previous campaign's
  `fourgate.py`, which excluded deep enabler chains by fiat.
- **Measured:** **all 1,540 = C(22,3) triples of the 88@5 geometry are dead** —
  869 cross-cluster + 422 confined + 249 edgeful, zero completions at plane
  choice #73, 845 s wall on 7 workers. Tier 1 (the 12 maximal-span triples) also
  dead on **all 243/243 plane choices** (2,916 instances). Control discipline is
  exemplary: PC1 19/19 over 4,617 instances; PC3 60/60 — **and PC3 caught a real
  false-negative bug** (an unsound pruning rule) before any negative was banked.
  Key scoping discovery: **the backbone and the 3^k manifold are
  basin-dependent** — 88@6's manifold is only 3,645/6,561 valid, and the
  intrinsic backbones of the from-scratch 88s are target-heavy, so porting the
  recipe verbatim would have swept an almost-empty set.
- **Cost:** ~36–75 s per (triple, choice); full coverage = 211,167 instances
  ≈ 2,000 core-hours.
- **Code:** `thinktank/phase2_{geom,fin,controls,run,gen_rest,alt_run,summary}.py`,
  `phase2_*.jsonl`, `phase2_tier{1..5}.txt`.
- **Generality:** MC-HARDCODED (it consumes this campaign's frozen geometry).
  The **control discipline** is the transferable part.
- **Phase-2 verdict:** superseded in scope by the basin work; keep the control
  pattern.

### e3-triple-classification / backbone-recovery
- **Family:** structural-analysis on the previous campaign's data.
- **What it does:** Recovers the 22-mask backbone from four double-defect bridge
  JSONs (over-determined four ways) and classifies all C(22,3) triples by span.
- **Measured:** the three previously-unnamed backbone masks identified —
  `00800080`, `00808000`, `80000080`, all pure `d7` columns (which is why they
  admit no +1 bypass). Independently reproduces the prior campaign's counts:
  exactly 13 edges, exactly 249 edge-containing triples, 1,291 edge-free.
  **E3 is not empty**: 869 genuinely cross clusters, 157 fully spread, 12 with
  the maximal span. Three clean-territory defect masks are exactly XOR
  differences of cross-cluster backbone pairs — **the E3 shape exists, is
  buildable, and costs +1.**
- **Code:** `thinktank/phase2_e3.py`, `phase2_e3_candidates.txt` (869 lines);
  input `bi_mask_requested_evidence/02_backbone_defects/`.
- **Generality:** MC-HARDCODED.
- **Phase-2 verdict:** the finding survives; the search it launched is closed.

### enabler/midpoint theory
- **Family:** structural-analysis (theory of *why* glue exists).
- **What it does:** Every tapped-sector target is a 3-leg sum; its three
  midpoints XOR to zero. Two of the three lie off every ladder line, so **every
  per-sector score gives them zero** — that is what an "enabling gate" is, and
  it explains the previous campaign's five ternary repair planes as midpoint
  triples.
- **Measured:** cluster law 74/74 (later 87/87). Of the 30 off-line gates in the
  five 88s only 8 are order-1; **22 are deeper (glue+glue→target)** — so
  pairwise-invisible mechanisms are the norm. Records achieve midpoint profit 3;
  an in-architecture 87 needs 4.
- **Code:** `thinktank/enabling_gates.md` (scripts were in a volatile scratchpad).
- **Generality:** generalises to any circuit whose targets are ≥3-leg sums.
- **Phase-2 verdict:** keeper as *understanding*; its search directive was never
  executed.

### backward-factorization-search
- **Family:** search (from targets toward inputs).
- **What it does:** Searches by repeatedly factoring an unresolved mask
  `m = a ⊕ b`; cost `F` = number of distinct internal factors. Proved equal to
  minimum gate count in both directions; a "free-split confluence lemma" means
  you never branch on a free split, so a run is a sequence of *introductions*
  and an 88 is exactly 56 introductions.
- **Measured:** **an exact identity: `F = 64 + a − c − 2d`** (a = pure-supply
  introductions, c = yield-3, d = yield-4), verified on all 32 circuits it
  touched, later 67/67. So **88 ⟺ `a − c − 2d = 24` and 87 ⟺ 23.** Mean closure
  yield is monotone across the whole frontier (1.571 for the 88s down to 1.485
  for 98@3). Best cold circuit **96 VALID**; nothing below 89 in 1,281 runs.
  The engine ties records on supply (a = 32 vs 33–36) and loses **solely** on
  yield-3 (c = 0 vs 7–10).
- **Code:** `thinktank/backward/{bwd_core,bwd_equiv,bwd_audit,bwd_profile,
  bwd5..bwd9,bwd_beam,bwd_identity}.py`, `finds/`, `logs/`.
- **Generality:** **CIRCUIT-GENERIC.** The formulation, the identity and the
  yield statistics are stated for an arbitrary XOR target set.
- **Phase-2 verdict:** **keeper**, with a caveat: `tri_search.md` later proved
  the saturator used for *all* of these counts can strand nodes, so the 96 and
  everything in that section came from a partially broken instrument. Repaired
  in `tri/`; **never re-measured here** (picked up downstream — see §5).

### tri-search-market
- **Family:** search (three coupled searches).
- **What it does:** Runs forward, backward and a middle pool **simultaneously**,
  coupled through a shared market on disk. Backward posts *constructive* bundle
  demands (the second partner of a yield-3 pair is forced: `u2 = d ⊕ u1`, so the
  demand list is complete with no search); the middle prices and builds; forward
  verifies.
- **Measured:** market mechanism works exactly as designed (`c: 0→6` cold,
  `0→9` planted; identity held 67/67) but **the economics are refuted**:
  measured exchange rate **5–8 supply gates per yield-3 rebate against a
  break-even of 1**, so `F` *rises* across rounds (107 → 176). Diagnosis, and
  it is the deepest result in the lane: **a yield-3 move needs an open node of
  closed-rank exactly 3, and those occur 0–1 per step, matching pure chance
  (≈2.6e-4, ~0.4 expected per run).** So records do not *find* their yield-3
  moves, they **manufacture** them — role-multiplicity ≥ 2 is necessary, not
  decorative. **99.1% of yield-3 opportunities cost two masks** (34,067 of
  34,368). And the demand book **recalls 64–86% of the records' own supply
  masks but ranks them ~200–800 of 25k, with the economically *derived*
  criterion ranking them WORST of nine statistics** (4.4% vs shape-weight's
  0.8%).
- **Cost:** every round re-runs backward; `tri/market/` is 80 M of demand books.
- **Code:** `atlas/tri/{tri_engine,tri_market,tri_loop,tri_control,tri_c3,
  tri_c4,sweep_base}.py`.
- **Generality:** **CIRCUIT-GENERIC.**
- **Phase-2 verdict:** keeper as a *negative result with a mechanism* — it tells
  the next phase not to try to buy coincidences. Its plumbing control caught a
  real bug in a sibling method, which is the strongest argument in the slice for
  mandatory plumbing controls.

### adaptive-gate-elimination (Lemma F + Theorem N)
- **Family:** proof-side lower bound.
- **What it does:** `L(M) ≥ m + min_K [(32−|K|) + 32 + e_K]` over a family of
  keep-sets covering every m-subset, run **adaptively** with a fresh optimal SLP
  at every stage; `e_K` = minimum extra values ("minE") by unpruned exhaustive
  search.
- **Measured:** **L(M) ≥ 55**, then **L(M) ≥ 56 unconditional and refereed** —
  the first improvement over 54 in project history. Cert 5 gives `minE ≥ 5` by
  **two** independent exhaustions (9.43e10 and 4.75e9 nodes, 511/511 branches
  each). 11 of 12 certificates die at depth 4 (`minE = 4` exactly, with
  witnesses). Searcher validation 400/400 against brute force; determinism
  across reboot node-for-node.
  **Refereed state of the problem: 56 ≤ L(M) ≤ 88.**
- **Cost:** depth-3 ≈ 2e8 nodes / 15 s in C; depth-4 = pod-scale;
  depth-5 estimated **40–80 pod-days** unpruned.
- **Code:** `thinktank/proofside_code/{mc.py,mine.c,ub.c,checkwit.py,admis.py,
  enum14.py,exact80.sh}`, `pod_evidence/d4out.tgz`.
- **Generality:** **CIRCUIT-GENERIC** — stated for any 0/1 matrix with distinct
  non-zero columns and a symmetry group.
- **Phase-2 verdict:** **keeper. This is the slice's hardest currency.**

### keepset-layer-enumeration
- **Family:** proof-side (twist on the above: enumerate the *whole layer*
  instead of sampling certificates).
- **Measured:** minimum admissible `|K| = 13` exactly, exactly **72** admissible
  13-sets, all with `minE = 0`. **The entire `|K| = 14` layer is CLOSED at 56**:
  all **33,548** admissible 14-sets enumerated, `minE ≤ 5` for 33,542 of them,
  the six exceptions resolved exactly. The `m = 2` branch is dead by complete
  census (caps at 54, strictly worse than 56) — and the regularity is
  *explained*: all 640 keep-sets with jam ≥ 12 contain the full hub orbit.
- **Also measured, and it is the sharpest diagnostic in the slice:**
  `L(M) − L(M|_K) = 88 − 37 = 51` gates for 18 columns = **2.83 per column**,
  while the bound pays 19 — and **51 − 19 = 32 = 88 − 56**. Cascade is *exactly
  zero* in all five 88s. **So the entire remaining gap is the price of a column,
  and the missing 0.9 per column is re-optimisation value — untouched by any
  elimination lemma.**
- **Code:** as above.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper — it says exactly why the elimination family
  stops at 56.**

### class-rank-localization + edge-counting bound
- **Family:** proof-side (two families, both closed).
- **Measured:** class-rank localization **exists and provably caps at exactly
  32** (8 target classes × 4). Edge counting `Σφ − |U|` is **refuted by the
  records themselves** — it evaluates to 31–33 on the very circuits it must
  bound, because every 88 has 3–6 inputs of fanout exactly 1.
- **Phase-2 verdict:** **dead-end, and valuable as such** — two whole families
  of lower-bound argument are provably capped below 56.

### C_c fanout-1 conjecture
- **Family:** proof-side conjecture + census.
- **What it does:** Conjectures that any optimal SLP has ≤ c live inputs of
  fanout 1; payoff `L(M) ≥ 73 − c`.
- **Measured:** census over **1,197 distinct verified circuits including 94
  distinct 88-states**: `z ≤ 11` over all 1,197 and `z ≤ 8` over all 94 optima.
  `c ≤ 16` alone would beat the trivial record bound. **z is largest exactly at
  the frontier** (mean 5.47 at 88, 1.93 at 91).
- **Generality:** stated matrix-agnostically — **CIRCUIT-GENERIC.**
- **Phase-2 verdict:** closed downstream (per project memory, the e17 campaign
  records `C_c` as closed by identity/self-defeat) — but the *census technique*
  and the "measure the conjecture's parameter on real optima first" discipline
  are keepers.

### basin-atlas (14-circuit census + invariant ledger)
- **Family:** structural-analysis / out-of-sample validation.
- **What it does:** Two independent clustering metrics (mask-set Jaccard and a
  22-component ladder fingerprint) over all 14 known 88s, plus a
  **relabelling-invariant ledger** that attributes each supply gate to the
  sector accounts it actually serves.
- **Measured, and several of these overturn earlier headlines:**
  - Two metrics, one partition, **three basins**: `{twelve}` | `{88@6}` |
    `{88@5fs}`; effective independent origins = **four**, not one and not five.
  - **The central localization is measurably backwards**: no 88 ever runs a tap
    sector *below* the floor; all fourteen run the tap cluster *above* it,
    sector 3 by ≥2 in 14/14. The only sub-floor sectors in the dataset are
    **clean** ones.
  - The "two mechanisms" story is a **bookkeeping artifact** — one diagonal
    bought as supply with two S7 consumers; 6 work + 1 supply = 7 = the model
    price, in every case.
  - **The universal mask core of all fourteen 88s is TWO gates.** There is no
    shared backbone.
  - **The three-account test is saturated**: values serving ≥3 distinct accounts
    number 2–4 in *every* 88 **and 3 in the 91-gate M1 optimum and 4 in the
    97**. "Find a triple-role value" cannot be the 87 programme — this kills the
    session's own four-way "fleet convergence".
  - `(CLEAN, TAPS, SHARED)` runs on **one line, 1-for-1** across all 14.
- **Code:** `thinktank/basin/b{0..12}_*.py` + logs.
- **Generality:** the invariant-ledger construction and the two-metric agreement
  test are **CIRCUIT-GENERIC.**
- **Phase-2 verdict:** **keeper — the best de-biasing instrument here.**

### sector-tightness-theorem
- **Family:** exact-oracle applied to records.
- **What it does:** For every (record, sector), reconstruct the sector's exact
  interface (inputs it consumes from outside, values it exports) and ask the
  oracle for `w_k − 1`.
- **Measured:** **48/48 UNSAT.** Every sector program of every record is exactly
  minimal for its interface. ⇒ an 87 requires renegotiating **interfaces**, not
  improving programs. This is the cleanest "nothing is stackable in place"
  statement in the corpus.
- **Phase-2 verdict:** keeper.

### sector-block-reoptimisation
- **Family:** exact-oracle applied to records (twist: replace a whole gate block
  by one fewer gate, confined to the sector's 8-dim span, with a structural
  NOT-COVERED control).
- **Measured here:** **58 of 112 blocks run** (23 `ctl=OK` exhaustive negatives,
  35 `NOT-COVERED`); coverage by sector is `S0:3, S1:14, S2:3, S3:14, S4:14,
  S5:3, S6:3, S7:4`. `basin/b9_88at6.log` is **0 bytes**.
- **Closed downstream** (`experiments/e7_push/`): 3 of the 23 negatives were
  *vacuous* (in-sector optimum strictly exceeds `|B|`); after a convex-closure
  repair, **70 of 112 blocks are decided exactly optimal with a live control,
  0 hits**, and the surviving surface is 35 blocks in sectors 1/3/4 needing
  dimension 12.
- **Code:** `thinktank/basin/b9_blockopt.py`, `b9b_sweep.py`, `b9b_*.log`.
- **Phase-2 verdict:** **superseded-by e7_push. Do not re-run.**

### shape-law mining (pred7)
- **Family:** oracle-table data mining.
- **What it does:** Treats the complete exact table as a dataset and derives a
  **closed-form 3-rule predicate** deciding `σ = 7`, then uses the predicate to
  extend the DP past the table's coverage.
- **Measured:** **pred7 has 0 errors on all 3,124 feasible entries** and agrees
  with an independent constructive search on all 4,096 `(P,Q)` pairs. The `σ=7`
  up-set has exactly **24 minimal patterns = 7 rotation classes**, all `(3,3)`.
  Mechanism census of all 222 optimal 7-gate witnesses: **antipodal target
  pairing is impossible 0/222; cyclic-adjacent pairing finds all 222.**
  And the reason for 91: `91 = 8×7 + 24 + 9 + 2`, the `+2` a **misalignment tax
  from a fixed-point-free 4-cycle of menus**.
- **Generality:** **CIRCUIT-GENERIC technique** — "mine your exact oracle for a
  closed-form predicate, then price beyond the table with it."
- **Phase-2 verdict:** **keeper — the highest leverage-per-CPU method here.**

### adversarial-audit family (4 methods)
- **Family:** audit. Four distinct instruments, all worth porting:
  1. **from-scratch frame rebuild** (`audit_foundations`) — re-derive every
     foundational claim in a module importing nothing from the codebase.
     Verdict: frame sound, zero convention slips, and `assemble.py` /
     `compile_config*.py` reproduce their outputs **byte-identically**.
  2. **independent instance rebuild** (`audit_generator`) — rebuild the whole
     instance corpus from FIPS-197 with zero code reuse and diff bit-for-bit.
     Verdict: **5,623/5,623 MATCH**, 0 critical findings; V2 landmark columns
     *predicted* from algebra and matched.
  3. **trust-graph audit** (`audit_trust`) — map every claim to the artifact
     supporting it *today*, labelled MLV / single-lineage / weak / no-artifact.
     Found a genuine internal contradiction (a law withdrawn on line 158 and
     re-invoked as a premise on line 179) and one no-artifact claim shipped in
     the HTML explainer.
  4. **alternative-reading audit** (`audit_inference`) — never "is this right"
     but "given it is right, what else is consistent, and would any decision
     change". Includes **null-model construction** and a **dependency trace of
     'independent' verifications**. Found: nine more valid 88s sitting on disk
     unexamined; "better ⇒ more disciplined" is false; **the finisher's frozen
     geometry is 88@5's mask set exactly, and 13 of 14 known 88s fail the
     freeze**; the three "independent" solver lineages share **one** instance
     generator; the four-way target-mask agreement is really 2-way; the R56
     landmark's pass mark was a **numeral collision** that would have
     manufactured a false positive on the null.
- **Generality:** **CIRCUIT-GENERIC and the most transferable material in the
  slice after the oracle.**
- **Phase-2 verdict:** **keeper — port all four verbatim.**

### monster-anatomy
- **Family:** structural-analysis (instrument-bias diagnosis).
- **Measured:** exactly **three** "monster" (high-mask-weight) gates across 11
  record circuits, and the weight statistic is a **measurement artifact**: an
  exact formula `mask weight = Σ_j |tv(μ_j)|` (0 mismatches over every signal of
  all 11 circuits) shows the same element weighs 6 on a light line and 10–11 on
  a tap line. Of the three, one is removable at **0 gates and 0 depth**, one at
  0 gates and +1 depth, one costs exactly +1. Latent census: 17 of 896
  sector-pure gates *would* be weight ≥ 8 on a heavy line.
- **Phase-2 verdict:** the lore correction is a keeper; the lead it opened
  (search with a corrected ruler) was executed and is null on the plateau.

---

## 3. ARTIFACTS (counts + labels)

All counts run from `/home/joebachir20/xor_ui/slp-plateau-search/atlas` unless
stated.

### 3.1 Verified circuits

| label | count | command | notes |
|---|---|---|---|
| circuit JSONs in `atlas/` (files with a 2-column `gates` list) | **711** | python scan over `glob('**/*.json')` counting `len(d['gates'])` | gate counts 26 … 176 |
| — of which 88-gate | **38 files / 32 distinct mask-sets** | same scan, `len(g)==88`, dedup by intermediate mask-set | 2 of the 32 are `M^T` circuits (`thinktank/transposed/`), not MixColumns |
| — 91-gate | 43 | same | includes `compiled_m1.json`, `compiled_all7.json`, `v15_rich91_circuit.json` |
| — 92-gate | 43 | same | |
| **88-gate mask-sets in `corner/out/*.plat`** | **498 distinct** | see §5 L1 for the exact script | **0 of 498 equal any of the 54 88-gate circuits under `evidence/`** |
| 89-gate states in `corner/out/*.plat` | 3,431 distinct lines | `awk '$1==89' corner/out/*.plat \| sort -u \| wc -l` | |
| all plateau state rows in `corner/out/` | 7,075 (min gate count **88**, no 87) | `awk '{print $1}' corner/out/*.plat \| sort -n \| uniq -c` | distribution: 88:504, 89:3507, 90:1845, 91:822, 92:157, 93:156, 94:66, 95:11, 96:5, 97:2 |
| circuits emitted by `periscope/finds/` | 186 | `ls periscope/finds \| wc -l` | best **90**; no 88 |
| circuits emitted by `tri/out/` | 67–69 | `ls tri/out/*.json \| wc -l` | best 88 (from planted pools), cold best 107 |
| quotient-tower witnesses | 6 | `ls tower/*.json` | `bp_L2_26.json` (26), `bp_L3_51.json` (51), `construct_L2_27.json`, `construct_L3_54.json`, `witness_L2_26.json`, `witness_L3_67.json` |
| skeletons of records | 8 | `ls socleplane/skel_*.json` | one per frontier circuit |

**Spot verification** (this session, `python3 verify_circuit.py`): 4 records
plus 13 plateau-derived circuits, **17/17 VALID**.

### 3.2 Exact-oracle corpora (the bulk of the value)

| label | count | size | command | what each entry certifies |
|---|---|---|---|---|
| strict M1 sector results | **5,633 files** (3,124 exact, 2,499 infeasible) | 23 M | `ls m1_results \| wc -l`; `grep -ho '"status": "[a-z]*"' m1_results/*.json \| sort \| uniq -c` | for a given menu `(P,Q)`: the exact minimum gate count with a replayable witness, or a proof of infeasibility |
| wide-menu results | **8,313** (8,287 exhaustive, **26 timeouts**) | 33 M | `grep -l '"exhaustive": false' m1_wide_results/*.json \| wc -l` | same, widths up to 6 |
| V1.5 exotic results | **34,112** (34,106 exhaustive, **6 timeouts**) | 135 M | `grep -l '"exhaustive": false' m1_v15_results/*.json \| wc -l` | same, exotic (triple/unit/socle) menus. **Corpus incomplete: 34,112 of 236,088 instances.** |
| σ value histogram, V1.5 | 6:**553**, 7:5627, 8:7001, 9:5165, 10:627 | — | `grep -ho '"min_gates": [0-9]*' m1_v15_results/*.json \| awk '{print $2}' \| sort -n \| uniq -c` | the 553 σ=6 cells are the measurement that refutes a universal floor of 8 |
| σ value histogram, wide | 7:1430, 8:4191, 9:1653, 10:256 | — | same on `m1_wide_results` | |
| **canonical distilled table** | **13,153 rows** (2,499 infeasible) | 1.3 M | `python3 -c "import json;print(len(json.load(open('m1_sigma.json'))))"` | `(kind, P, Q) → min_gates`. Value histogram 7:1652, 8:5666, 9:2702, 10:585, 11:44, 12:5. **No witnesses** — those live in the result dirs. |
| σ⁺ junction bank | **11,248 records** (10,494 UNSAT, 752 SAT, 2 UNKNOWN) | 2.5 M | `cat spbank/*.jsonl \| wc -l`; `grep -ho '"verdict": "[A-Z]*"' spbank/*.jsonl \| sort \| uniq -c` | per (class, level): can this sector emit a free junction? |
| socle-currency results | 1,048 | 4.2 M | `find soclecurrency/results -type f \| wc -l` | sector solves under the socle-currency pricing |
| landmark solves | 23 logs / 11 instances | 132 K | `ls m1_landmark_results \| wc -l` | the named L1–L5 and R01/R34/R56 solves |

### 3.3 Bound certificates

| certificate | what it certifies | artifact |
|---|---|---|
| **cert 5, depth 4** | `minE ≥ 5` ⇒ **`L(M) ≥ 56` unconditional, refereed** | `pod_evidence/d4out.tgz`; `thinktank/proofside_code/{cert5.txt,d4/}` |
| g11 cube split | `σ(clean,∅,∅) = 12` exact, **28/28 cubes UNSAT** | `pod_evidence/g11_cubes/VERDICT.json`, `cubes.jsonl` |
| R01 region climb | `R01_record_imports ≥ 15` (k=14 UNSAT, 6,932 s) | `pod_evidence/R01_climb.log` |
| R34 region climb | `R34_record_imports ≥ 16` (k=15 UNSAT, 8,903 s) | `pod_evidence/R34_climb.log` |
| R56 region climb | optimum in **[15, 23]**, capped at 43,200 s | `pod_evidence/R56_climb.log` |
| L1 landmark | `σ(0,0) = 12` (k=11 UNSAT, 4,236 s) | `m1_landmark_results/L1.log` |
| L1 bare-encoding leg | bracket **[11, 12]** — timed out at k=10 after 4,905 s | `m1_landmark_results/L1_bare_encoding.log` |
| bare-encoding floor cross-check | 24 floor strata re-derived with all normalisation/pruning clauses stripped, **agree=24 disagree=0** | `m1_landmark_results/bare_floor_crosscheck.log` |
| **32 timed-out strata** | each `lower_bound_proven = 10`, no upper — **brackets, not values** | 26 in `m1_wide_results/`, 6 in `m1_v15_results/`; see §5 L5 |

### 3.4 Writeups, ledgers, logs

| label | count | command |
|---|---|---|
| `.md` writeups in `atlas/` | **28** (26 in `thinktank/` + `NOTEBOOK.md` + 1) | `find atlas -name '*.md' \| wc -l` |
| code files (`.py` + `.c`) | **167** | `find atlas \( -name '*.py' -o -name '*.c' \) \| wc -l` |
| log/out files | **243**, 1.3 M total | `find atlas \( -name '*.log' -o -name '*.out' \) \| wc -l` |
| append-only jsonl banks | `spbank/*.jsonl`, `sigma_plus_bank.jsonl`, `thinktank/sweep{7,8}_*.jsonl`, `thinktank/phase2_*.jsonl`, `tri/market/ledger.jsonl` | — |
| interactive HTML | 2 (`explainer.html` 180 K, `workbench.html` 104 K) | — |
| `bi_mask_requested_evidence/` real files | **39** (75 minus 36 `:Zone.Identifier`), 30 of them SHA-256 manifested | `find bi_mask_requested_evidence -type f \| wc -l` |

---

## 4. KEEP / DELETE proposal

Total slice 1.3 GB. **Reclaimable with zero information loss: ~1.20 GB.**

### 4.1 DELETE-CANDIDATE — provably redundant (verified this session)

| path | reclaims | why |
|---|---|---|
| `atlas/m1_v15_results/` (the expanded dir) | **133 M** | `atlas/v15_partial.tgz` (1.8 M) is a **byte-identical, complete** archive of it. Verified: file lists diff to 0 lines; two sampled files SHA-256 identical. **Keep the tarball, delete the expansion.** |
| `atlas/m1_wide_results/` (the expanded dir) | **32.5 M** | `atlas/wide_results.tgz` (548 K) is the same archive relationship (8,313 files + dir = 8,314 entries). *Recommend the same SHA spot-check before deleting.* |

Reproduce the check:
```
tar tzf atlas/v15_partial.tgz | sed 's|m1_v15_results/||' | grep -v '^$' | sort > /tmp/a
ls atlas/m1_v15_results | sort > /tmp/b; diff /tmp/a /tmp/b   # 0 lines
```

### 4.2 DELETE-CANDIDATE — regenerable inputs

| path | reclaims | why |
|---|---|---|
| `atlas/m1_v15/` | **934 M** | 236,088 *instance* files, deterministically regenerable by `thinktank/v15b_gen.py` (+ the pod generator). Only 34,112 were ever solved, and which ones is recorded by the result filenames. **Note before deleting:** `v15b_gen.py` covers the "complement family"; confirm the pod-side generator for the `≥1 exotic in P` family is also in-repo, else regenerate-and-tar first. |
| `atlas/m1_wide/` | **33 M** | 8,313 instances from `m1_search_wide.py::gen()` (a 2-line diff from `m1_search.py`). |
| `atlas/tri/market/` | **80 M** | Market state (`demands.jsonl` per round). Regenerable by `tri_loop.py`; the *finding* (exchange rate 5–8 vs break-even 1) is fully written up in `tri_search.md`. Keep `tri/market/ledger.jsonl` (5 K) and `tri/out/`. |
| `atlas/**/__pycache__/` | 696 K | build artifacts |
| `bi_mask_requested_evidence/**/*:Zone.Identifier` | 144 K | Windows ADS junk; none appear in `SHA256SUMS.txt`, so removing them does not invalidate the manifest. |
| `d3_b.out` | 123 B | a traceback for a script that no longer exists |
| `atlas/userscheme_pricing.log` | 0 B | empty |

**Sub-total: ~1.05 GB regenerable + 165 MB redundant = ~1.21 GB.**

### 4.3 KEEP — do not delete

| path | why |
|---|---|
| `atlas/NOTEBOOK.md` + `thinktank/*.md` (28 files) | **the deliverable.** Every number in this report traces here. |
| `atlas/m1_sigma.json` | the canonical 13,153-row exact table — the distilled product of ~48k CPU-heavy solves |
| `atlas/m1_results/` + `m1_instances/` | the strict corpus **with witnesses**, bit-for-bit audited against an independent FIPS-197 derivation. 46 M; small enough to keep expanded. |
| `atlas/v15_partial.tgz`, `wide_results.tgz` | after 4.1, these become the only copies |
| `atlas/spbank/`, `sigma_plus_bank.jsonl` | append-only verdict banks |
| `atlas/pod_evidence/` | **the only local copy of the L ≥ 56 depth-4 exhaustion and the 28/28 cube verdict.** Irreplaceable. |
| `atlas/m1_landmarks/`, `m1_landmark_results/` | the named landmark solves incl. the bare-encoding cross-check |
| `atlas/corner/out/*.plat` (4.6 M) | **498 distinct 88-gate states, none matching a known circuit** — see §5 L1. Unmined data; keep. |
| `atlas/corner/work/`, `corner/*.py`, `walk*.c`, `*.jobs` | the seven-arm A/B harness — reusable |
| `atlas/periscope/`, `tower/`, `socleplane/`, `soclecurrency/`, `tri/{out,*.py}`, `thinktank/{basin,backward,transposed,proofside_code}/` | lane workspaces with unique results; total ~28 M |
| all `*.py`, `*.c`, `*.sh` (167 files) | the method catalogue's implementations |
| `atlas/explainer.html`, `workbench.html`, `viz_data.json`, `editor_data.json` | **KEEP + NOTE**: no generator for the two JSONs exists in the repo (audit ISSUE 5.5), so they are unregenerable |
| `bi_mask_requested_evidence/` (all real files) | a hash-manifested preservation bundle answering an explicit request, containing the **only surviving copy** of the n16 near-26 module and the 36-mask defect vocabulary. Input to `phase2_e3.py`. |
| `joe_depth3_audit/` | 16 K, three scripts; trivially small, mildly useful (`mc_weights.py` builds the matrix from scratch in 20 lines). KEEP by the "when in doubt" rule. |

---

## 5. LEADS

### L1 — VERIFIED (by me, this session). 498 unrecorded 88-gate circuits, and the socle plane's "2-gate ridge" does not exist.

`atlas/corner/out/*.plat` holds the plateau states emitted by the
corrected-ruler walker. `ideas_strange_corners.md` §7 lists three job files
(`hunt.jobs` 160 walks, `sh2.jobs` 76, `fib.jobs` 32) as **"still running at
write-up, results not included"**, and no successor exists anywhere — I grepped
the whole repo: `"corrected ruler"` / `"line-normalis"` have **zero** matches
outside `atlas/`. The output was never analysed.

Measured now:

```
# 498 distinct 88-gate mask-sets, l3 histogram, novelty vs evidence/
cd atlas/corner && python3 - <<'EOF'
import sys,glob; sys.path.insert(0,'.'); sys.path.insert(0,'..')
from socle import l3_of
from anatomy import load_gates
from collections import Counter
def masks(g):
    f=[1<<i for i in range(32)]
    for a,b in g: f.append(f[a]^f[b])
    return frozenset(f[32:])
seen={}
for p in glob.glob('out/*.plat'):
    for ln in open(p):
        t=ln.split()
        if not t or int(t[0])!=88: continue
        n=list(map(int,t[1:])); g=[(n[2*i],n[2*i+1]) for i in range(len(n)//2)]
        seen.setdefault(masks(g),(l3_of(g),p))
print(len(seen), sorted(Counter(l for l,_ in seen.values()).items()))
EOF
```

- **498 distinct 88-gate mask-sets.**
- **`l3` histogram: 64:2, 65:8, 66:17, 67:7, 68:24, 69:36, 70:16, 71:6, 72:12,
  73:50, 74:85, 75:42, 76:59, 77:65, 78:57, 79:12.**
- **0 of the 498 equal any of the 54 distinct 88-gate circuits under
  `evidence/`.**

I converted 13 of them to JSON (in my scratchpad, nothing written to the repo)
and ran `python3 verify_circuit.py`: **13/13 VALID MixColumns, 88 gates,
32/32 outputs.** I also confirmed `corner/socle.py::l3_of` reproduces the
published table exactly (88@5→77, 88@5fs→67, 88@6→68, 88@7→74).

This contradicts three published claims from this very session:

1. `ideas_strange_corners.md` §4.5 and `NOTEBOOK.md`: *"the band `l3 ∈ 69..72`
   … is now populated — and costs 90–91 gates, so the two 88 bands `{67,68}`
   and `[73,78]` are separated by a real 2-gate ridge."* — **70 of the 498 sit
   at 88 gates with `l3 ∈ 69..72`**; I verified one at each of 69, 70, 71, 72.
   There is no ridge; the 88 level set is **continuous from 64 to 79**.
2. The published 88 floor `l3 ≥ 67`: **27 circuits at `l3 ∈ {64,65,66}`**,
   verified at 64, 65, 66.
3. `audit_inference.md` §3.3: *"real content = bimodal `l3` by lineage, gap
   69–72 empty."* — the gap is an artifact of the tiny sample (9 circuits) that
   was placed on the plane, not of the plane.

**Why it might matter for 87.** `audit_inference.md` §4 flags "(80,7)-type 87
skeletons are excluded by nothing measured", and `phase2_tower.md` argues an 87
should be sought skeleton-anchored at low `l3`. The lowest-`l3` 88s known before
today were 67; there are now **verified 88s at 64**, i.e. 3 gates further into
the corner where the tower argument says an 87 would live. Anchoring a
skeleton-anchored SAT (`third_frame.md` C2 / `phase2_tower.md` §7.1) at
`l3 = 64` instead of 67 is strictly cheaper and strictly closer to the
`bp_L3_51.json` witness. **Cost to act: converting the 498 to JSON and
verifying is minutes; the socle-plane envelope recomputation is seconds.**

Confidence: **VERIFIED** for the circuits and the `l3` values; **PLAUSIBLE**
for the 87 relevance.

### L2 — PLAUSIBLE. The corrected ruler's own calibration target was never used.

`ideas_strange_corners.md` §4.8 measured heavy-mask emission per 1000 gates:
popcount arm **1.11**, corrected-`W` arm **18.27**, uniform 14.80 — and the
fourteen known 88s at **7.31, between the two arms**. The report's conclusion
was "neither ruler points where 88s live", and the lane stopped. But the
measurement hands you a **fitted target**: a ruler (or a temperature) tuned to
emit heavy masks at ≈7.3/1000 was never built or tested, even though the harness
(`corner/walk.c`, 7 pluggable arms + a temperature sweep) supports it as a
one-line change. The temperature sweep in §4.6 is exactly the dial. Zero
downstream pickup anywhere in `fleet*/` or `experiments/`.

### L3 — PLAUSIBLE. Nobody ever ran a *search* in the transposed frame.

`transposed_frame.md` establishes `L(M) = L(M^T)`, gives a verified
transpose-and-transpose-back path (11/11 circuits), and measures
`r(mask weight, co-mask weight) = −0.62..−0.73` — meaning **the existing search
instruments, run unmodified on `M^T`, would explore a slice of the space ranked
by a nearly opposite statistic**. The transposed *bound* lane was pursued to
exhaustion and closed. The transposed *search* was proposed in §3.1 and never
run. The tooling exists (`thinktank/transposed/run_transpose.py`,
`verify_mt.py`) and the plateau walkers are circuit-generic.

### L4 — SMELL (cheap to close). Two truncated relaxation runs.

`atlas/fjb.log`: the free-junction bound is a deliberate over-relaxation whose
own docstring says *"If it is ≥ 91 … the verdict stands unconditionally; if it
is ≤ 90, the configurations it names are exactly the instances the sweep must
then be run on."* It returned **89** in MODE=tap1 (complete) and reached **90**
in MODE=junction — where **the log ends with no optimum line**, i.e. the run was
killed. The cheap exact follow-up `eft.log` closed MODE=tap1 at 91 but **stopped
at 800 of 3,249 frames** in MODE=both (`NOTEBOOK.md` lists
`exact_free_targeted` among "possibly-live local stragglers to kill or ignore …
non-decisive"). The script advertises "seconds instead of hours". Expected
outcome is a sixth confirmation of 91 — but it is the one M1 computation that
was *started and abandoned* rather than decided.

### L5 — VERIFIED-IN-LOG. 32 bracketed strata are silently absent from the canonical table.

32 instances timed out at the 900 s cap, each banking
`lower_bound_proven = 10` with no upper bound (26 in `m1_wide_results/`, 6 in
`m1_v15_results/`; all `tap` with an empty or width-1 `P`). `NOTEBOOK.md` says
*"Timeout strata land as brackets … the bound-DP consumes them as-is; a timeout
is never a false exact."* But they are **not in `m1_sigma.json` at all** —
neither by instance name nor by canonical `(kind,P,Q)` key:

```
cd atlas && python3 -c "
import json,glob,sys; sys.path.insert(0,'.')
from m1_search import canon_PQ
tab={(r['kind'],)+canon_PQ(tuple(r['P']),tuple(r['Q'])) for r in json.load(open('m1_sigma.json'))}
n=0
for p in glob.glob('m1_wide_results/*.json')+glob.glob('m1_v15_results/*.json'):
    s=open(p).read()
    if '\"exhaustive\": false' in s:
        d=json.loads(s); n+= ((d['kind'],)+canon_PQ(tuple(d['P']),tuple(d['Q'])) in tab)
print(n)"   # -> 0
```

Consequence: in **exact/pessimist** mode the DP prices them `INF` (safe for an
upper-bound reading of 91, but it means 91 is a minimum over a *restricted* set
of configs); in **optimist** mode they are filled at the floor 7, which is far
below their **proven ≥ 10**. Folding the banked `≥10` brackets in as genuine
lower bounds can only *raise* the optimist floor — a bracket-aware DP is a small
edit to `solve2` and is the cheapest available strengthening of the class
result. This also sharpens the caveat that **M1 = 91 is an upper bound plus a
witness, not a floor** — a point `audit_foundations.md` §4 made and
`fleet1/laneD_completions/RESULT.md` later confirmed brutally (the optimist DP
over the incomplete V1.5 corpus returns **58**, not 89–91).

### L6 — PLAUSIBLE. Two structural facts nobody built a search around.

Both are stated as measurements, neither was converted into a move:

- **`F = 64 + a − c − 2d`** (`backward_search.md`, verified 67/67). So an 87
  requires exactly `a − c − 2d = 23`. §9.3 says *"bounding `c` above and `a`
  below would be a bound of a shape the elimination lemmas do not produce"* and
  marks it **never attempted**. It is a *lower-bound* use of a search identity —
  a shape this project has not tried.
- **The rank-3 manufacture question** (`tri_search.md` §8.2.5): "make an open
  node a 3-fold XOR of closed masks" is, in the ring frame, an **algebraic**
  question, not a search — and it is the exact bottleneck the market measured at
  probability 2.6e-4. Explicitly never attempted.

### L7 — SMELL. `atlas/soclecurrency/` is the one undocumented lane.

4.4 M, 1,072 files, 1,048 solved sector instances, a full DP (`dp.py`) whose
docstring says it implements the **dcost over-charge fix** that
`phase2_capacity.md` flagged as possibly pricing real 88s at 91 — and there is
**no writeup**. `sweep_clean7.log` and the floor JSONs are the only narrative.
Someone should read `dp.py`'s output before the tree is reorganised; if it
produced a number below 91 it never reached the notebook.

### Leads that are CLOSED downstream — do not re-run

I checked each against `fleet*/` and `experiments/`:

| atlas "unfinished" item | status |
|---|---|
| sector-block re-optimisation (`basin/b9b_*`, incl. "88@6 S2 in 8 gates = an 87 outright") | **CLOSED** by `experiments/e7_push/`: 70 of 112 blocks decided exactly optimal with a live control, **0 hits**; 3 of the atlas run's 23 negatives were vacuous and are corrected in `experiments/e7_push/ATLAS_NOTE.md` |
| `bwd9.py` two-step hop (coded here, never run here) | **RUN** in `fleet1/laneD_completions/` (`bwd_frontier_bwd9.log`, `ledger_bwd9.jsonl`) |
| V1.5 corpus completion → theorem-grade class bound | **CLOSED NEGATIVE** by `fleet1/laneD_completions/`: the optimist shortcut returns 58, and the flat-floor family is refuted by the 553 measured σ=6 cells |
| width-5/6 σ entries; V2 region pricing | picked up in `fleet1/laneA_v2pricing/`, `laneB_regionbounds/` |
| skeleton-anchored / `l = 51` | picked up in `fleet1/laneC_proofside/` |
| R56 landmark and its wrong `compare_to` | picked up in `fleet12/laneAUDIT/`, `experiments/e15_campaign3/` |
| `C_c` conjecture | closed per project memory (e17 campaign) |
| `phase2_alt` disjoint-basin sweeps | referenced in `fleet1/laneD_completions/RESULT.md` |

**No 87 exists anywhere in this slice.** The minimum over all 711 circuit JSONs
and all 7,075 plateau state rows is **88**.

---

## 6. HAZARDS

1. **Hardcoded absolute paths.** 41 occurrences of
   `/home/joebachir20/xor_ui/slp-plateau-search` across 20 files in `atlas/`
   (`run_ef.sh`, `socleplane/{build,sweep,core,readoff,recskel}.py`,
   `tower/{analyze,lift,quotient,extract,structure}.py`,
   `thinktank/{phase2_depth_driver.sh,phase2_alt_chain.sh,phase2_chain.sh,
   phase2_chain2.sh,compile_config_v3.py,v15_dp.py,v15b_gen.py}`,
   `thinktank/proofside_code/{z_census.py,run_hi.sh}`). Any move of the repo
   breaks these. Command:
   `grep -rln "/home/joebachir20/xor_ui/slp-plateau-search" --include=*.py --include=*.sh atlas`
2. **Cross-directory reads.** ~15 files read from sibling directories
   (`evidence/circuits/`, `pipeline/`, `beat88/`, and `~/xor_ui/aes_mc_records/`
   — a **different repo**): `periscope/{engine,census,shapes,shell_probe,
   harvest_check}.py`, `corner/{socle,census,envelope}.py`,
   `tri/{tri_control,tri_c3,tri_c4}.py`, `tower/extract.py`,
   `thinktank/{phase2_probe,phase2_controls,phase2_fin}.py`. Moving
   `evidence/` or `beat88/` breaks the atlas instruments.
3. **`joe_depth3_audit/*.py` use relative paths** (`evidence/circuits/...`) and
   only run from the repo root. Moving them into a subdir silently breaks them.
4. **`atlas/viz_data.json` and `editor_data.json` have no generator in the
   repo** (audit ISSUE 5.5). They are unregenerable; `explainer.html` and
   `workbench.html` depend on them.
5. **`atlas/v15_partial.tgz` and `wide_results.tgz` become the sole copies** if
   §4.1 is executed. Verify SHA before deleting the expansions, and never delete
   both a tarball and its expansion in the same pass.
6. **`pod_evidence/` is the only local copy** of the depth-4 cert-5 exhaustion
   (`d4out.tgz`) and the 28/28 cube verdict. The pods are gone. This directory
   backs the project's headline lower bound.
7. **Ops traps recorded in `transposed_dp.md`, still live in the code:**
   (a) `slp_opt.py` defaults to **all cores** and will spawn ~21 workers —
   always pass `--cores` (a load-176 incident is documented);
   (b) `subprocess.run(capture_output=True, timeout=...)` **hangs forever** on
   `slp_opt` because grandchildren hold the pipe — use file redirection +
   `start_new_session` + `killpg`;
   (c) `slp_opt --timeout` is **wall-clock** and this box's backwards-stepping
   clock defeats it — use a monotonic deadline;
   (d) `slp_opt` **block-buffers stdout** under redirection, so a supervisor
   sees an empty file — use `python3 -u`.
   These matter if any phase-2 work re-runs the oracle. Nothing in my slice is
   currently running (`atlas/` last modified 2026-08-18); I started and signalled
   no processes.
8. `atlas/corner/out/*.plat` filenames encode the arm/seed/config and are read
   by `corner/analyze.py`'s parser — renaming them breaks the A/B analysis.

---

## 7. GAPS

1. **I did not verify all 498 plateau 88s** — only 13, spanning `l3` ∈ {64, 65,
   66, 69, 70, 71, 72, 79}. Verifying all 498 is a few CPU-minutes but the brief
   forbids bulk verification while the solvers hold the cores. The 498 count is
   a count of *distinct intermediate-mask sets among 88-gate plateau rows*; the
   walker only accepts valid states and my sample was 13/13 VALID, but the
   full-corpus claim is inferential.
2. **Novelty of the 498 is measured against `evidence/` only** (54 distinct
   88-gate circuits, 0 matches). My repo-wide comparison — including
   `campaign_87/`, `beat88/`, `experiments/`, `fleet*/` — timed out at 2
   minutes and I did not retry, to stay inside the CPU budget. The stronger
   claim ("novel repo-wide") is therefore **not established**; and
   `~/xor_ui/aes_mc_records/` is a separate repo I did not read at all.
3. **`atlas/soclecurrency/` (4.4 M, 1,048 results) is undigested.** No writeup
   exists and I read only `dp.py`'s docstring. Its DP implements the dcost
   over-charge fix; whether it ever produced a number is unknown to me.
4. **`atlas/tower/bp3_*.out` and `corner/work/` were not opened.** I inferred
   the tower's results from `phase2_tower.md` rather than from the raw outputs.
5. **Whether `m1_v15/`'s 236,088 instances are fully regenerable in-repo.**
   `thinktank/v15b_gen.py` generates the "complement family"; the main pod
   generator (which required ≥1 exotic shape in `P`) is referenced as
   `/root/atlas/...` and I did not confirm an in-repo equivalent. My
   delete-recommendation for `m1_v15/` is conditional on that check.
6. **The `wide_results.tgz` ↔ `m1_wide_results/` identity is asserted from
   entry counts only** (8,314 entries vs 8,313 files + dir). I SHA-verified the
   v15 pair, not this one. Do the same check before deleting.
7. **Timings.** Most thinktank writeups do not state wall-clock cost, so the
   "Cost" fields in §2 are sparse and come from the few logs that carry
   `seconds`.
8. **I did not read `explainer.html` or `workbench.html`** (286 K of HTML); the
   audit reports say the explainer once shipped an unsupported "15/16" panel
   that later became true via `pod_evidence/`. Whether the file was ever edited
   is unknown to me.
