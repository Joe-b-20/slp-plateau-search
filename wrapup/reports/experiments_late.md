# Slice report: experiments_late (e10, e11, e12, e13, e14, e15, e16, e17)

Agent model: Opus 5 (1M context). Date: 2026-08-29.

**Summary.** This slice holds eight campaigns spanning 2026-08-18 to 2026-08-29,
totalling **302 MB** across 8 directories, and it contains the project's densest
and freshest material. Two of them (e10, e11) are subset-pricing experiments on
sub-instances of MixColumns; the other six are the "late campaigns" — the
hand-reasoning reconstruction of the record 88 (e13), the plateau geometry and
free-move orbit work (e14), the population window sweep and the **B = 56
tripwire theorem** (e15), the 536-autopsy / F-point-orbit / forcedness campaign
(e16), and the pure-reason proof campaign whose product is **the Anatomy
Theorem** and the **Lower-Bound Dossier** (e17). Every campaign ends in the same
verdict: **no 87, `56 <= L(M) <= 88` untouched**. The three headline facts the
task asked me to locate all check out and their exact statements, proofs and
running code are cited below. **Operational status: everything in this slice is
FINISHED.** e15's population sweep completed 2026-08-28 22:38, its d3 anchor
pass completed 2026-08-29 04:12, and its RESULT.md passed a cross-desk audit at
2026-08-29 08:57 — no process in this slice is alive (the only live processes on
the box are `fleet11/laneCUBE`'s `mono.py`/`cube16.py` and `fleet12/laneHALO`'s
`generate.py`; nothing under `experiments/` is running). laneDELTA is likewise
complete (RESULT.md written 2026-08-28 12:18); its Lemma-R corpus tripwire ran
and returned **0 hits on 1,200 valid 88s** and **66 hits on non-88s**. I found
**24 leads**, the sharpest being e17's own successor map (one CP-SAT run is the
highest value-per-hour item on the whole board), e15's approved-but-never-run
"run C", and e11's single open level `k = 12` priced at ~38 CPU-hours.

---

## 1. INVENTORY

Sizes from `du -sh experiments/<dir>` (2026-08-29):

| dir | size | what it IS | documented? |
|---|---|---|---|
| `e10_crossfam` | 1.3M | Cross-family **subset pricing**: does cancellation ever strictly beat cancellation-free cost on output subsets of MixColumns? | YES — `RESULT.md` (18.7K), `report_snapshot.txt`, append-only `ledger.jsonl` (201 rows) |
| `e11_quad10` | 23M | Successor to e10: the two **dim-10 cross-family quads** driven to `12 <= cost <= 13`, plus a dimension-stratified matched control | YES — `RESULT.md` (29.7K), `ledger.jsonl` (110 rows), `shards/` |
| `e12_legibility` | 384K | Do global optima look **locally senseless**? Certified-optimal miniature instances vs greedy | YES — `RESULT.md` (5.9K) + `PLAN.md`, `ledger.jsonl` (65 rows) |
| `e13_hand87` | 900K | The **hand/cluster campaign**: four reasoning lanes reconstructing a record circuit from scratch; plus window/cut, transposition, and from-scratch-algebra lanes | YES — 5 RESULT.md files + `AUDIT.md`, `LEDGER.md`, per-lane `NOTES.md` |
| `e14_plateau87` | 848K | **Campaign 2**: free-move orbits of the 88 plateau, the `D_fine` metric, the F-point extraction, the death of the anatomy census | YES — `RESULT.md`, `AUDIT.md` (212K), `LEDGER.md`, 3 lane files |
| `e15_campaign3` | 45M | **Campaign 3**: population window sweep (17,283 circuits), the B=56 tripwire, mechanism decode, composition/ILP, five excursion probes | YES, heavily — `RESULT.md` (57K, audited), `AUDIT.md` (223K), `AUDIT_FINAL.md`, `LEDGER.md` (259K), 5 lane files |
| `e16_lastwish` | 231M | **Final-wish campaign**, three lanes: the 536 autopsy, the F-point orbit enumeration (the 224M state bank), the forcedness study | PARTIAL — three lane `RESULT.md` files, but **no campaign-level RESULT.md** (see LEADS L20) |
| `e17_pure` | 1.1M | **Pure-reason proof campaign**: 4 lanes + 3 adversarial referees, output = the **`DOSSIER.md`** lower-bound map (92K) | YES, exceptionally — `DOSSIER.md`, 4 lane RESULT.md, 3 REF VERDICT.md, 7 LEDGER.md |

**File-type breakdown** (`find <dir> -name '*.EXT' | wc -l`):

| dir | .json | .jsonl | .py | .md | .log | .txt |
|---|---|---|---|---|---|---|
| e10_crossfam | 57 | 1 | 26 | 1 | 17 | 1 |
| e11_quad10 | 6 | 7 | 28 | 1 | 23 | 1 |
| e12_legibility | 43 | 2 | 3 | 2 | 9 | 0 |
| e13_hand87 | 39 | 0 | 27 | 15 | 5 | 14 |
| e14_plateau87 | 21 | 0 | 40 | 8 | 4 | 1 |
| e15_campaign3 | 39 | 7 | 88 | 18 | 30 | 29 |
| e16_lastwish | 16 | 29 | 28 | 8 | 18 | 1 |
| e17_pure | 24 | 0 | 33 | 16 | 7 | 0 |

**Where the bytes are** (`find ... -size +500k | sort -rn | head`):
`e16_lastwish/laneFPOINT/bank/F8.states.bin` 134M, `.../F1.states.bin` 61M,
`e11_quad10/shards/ctl10_cf12_31_107_617_920_k11.jsonl` 17M,
`.../F2.states.bin` 13M, `e15_campaign3/sweep_A_fullpop.jsonl` 12M,
`.../F6.states.bin` 12M, `e15_campaign3/tools/pop88.pkl` 10M,
`e15_campaign3/n3_results/joint_pop.jsonl` 4.8M,
`e16_lastwish/lane536/corpus_le3.jsonl` 3.7M,
`e15_campaign3/n3_results/corpus_scan.jsonl` 2.9M.
Raw logs are trivial in size everywhere: 118 `.log/.out/.nohup` files, **2.2 MB
total**, of which 2.0 MB is e11's two `shardcontrol*.log`.

**Opaque subdirs (no README/RESULT of their own):** `e15_campaign3/compose/`
(59 python files + JSON — but every one is named in `laneCOMPOSE.md`),
`e15_campaign3/probes/` (7 JSON, named in RESULT §Stage 3),
`e15_campaign3/n3_results/` (10 files, named in `N3_ILP_SPEC.md`),
`e14_plateau87/basis/` (documented inside `laneBASIS.md`),
`e12_legibility/data/` (43 `*.witnesses.json`, described in RESULT §Ground truth).
Nothing in this slice is genuinely undocumented.

**18 `__pycache__` directories, 548 KB total.**

---

## 2. METHODS

### crossfam-subset-pricing
- **Family:** exact-subset pricing / exhaustive SLP search.
- **What it does:** For a subset `S` of MixColumns output rows, compute the exact
  cancellation-free cost `cost_cf(S)` by MILP (constructive, so it is a
  machine-checked upper bound), then run an exhaustive unrestricted XOR-SLP
  search at the single budget `k = cost_cf - 1`. UNSAT-exhaustive decides `gap =
  0`; SAT exhibits a strict cancellation gain; an aborted budget is recorded as a
  bracket and never as a bound.
- **Twist vs siblings:** spends the whole budget on the one hardest level instead
  of climbing a ladder — sound because a gap is cheap to find (first-solution
  DFS) and only its absence is expensive.
- **Measured performance:** `cost(S) = cost_cf(S)` on **54 of 54** subsets
  decided, 9 of them cross-family, **zero gaps**. Cross-family decided classes:
  n=2 at dim 8/9/10, n=3 at dim 9/10. 6 subsets left UNDECIDED as brackets.
  `e10_crossfam/RESULT.md` §1, §2; `ledger.jsonl` kind `gaphunt` 62 rows.
- **Cost:** minutes-to-hours per subset; escalation runs of 293–308 s closed two
  dim-10 n=3 classes at ~1.4e8 nodes each.
- **Code:** `e10_crossfam/code/gaphunt.py`, `code/qsearch.c` (E8's searcher,
  copied verbatim), `code/xrun.py`, `code/escalate.py`, `code/enum.py`.
- **Logs/results:** `e10_crossfam/ledger.jsonl` (181K, 201 rows),
  `report_snapshot.txt`, `found/` (54 JSON witnesses).
- **Generality:** MIXED. `qsearch` is circuit-generic over a bit-mask target set;
  `enum.py`/`classes.json` encode MixColumns' row structure and the ρ-orbit Venn
  isomorphism. Aiming at `aes_inv_mixcolumns` needs a new target-row table and a
  new orbit/isomorphism enumeration; the searcher is unchanged.
- **Phase-2 verdict:** **keeper as an instrument, dead end as a programme** —
  §1(c) proves the question is identically empty below 4 targets.

### shape-matched-random-control
- **Family:** control / calibration methodology.
- **What it does:** For each real MixColumns subset shape (dim, target count,
  target weights, support union), generates random instances of exactly that
  shape and runs the same exhaustive both-ways decision, to establish whether the
  measured quantity can be non-zero *at that shape at all*.
- **Twist vs siblings:** it prices the *null*, not the instance. It is the method
  that retroactively voided a whole campaign's worth of negatives.
- **Measured performance:** **0 / 400** at every MixColumns shape with `n <= 3`
  — so the E2/E8/E10 nulls at `n <= 3` "carry no information about MixColumns
  whatsoever". At `n = 4` dim 8 it fires: **5/16 (31%)**, all 16 exhaustive.
  Reproduced E8's original 48/400 control exactly.
- **Cost:** ~400 exhaustive instances, hours.
- **Code:** `e10_crossfam/code/matched.py`, `code/density.py`, `code/pivot.py`.
- **Logs/results:** `matched.log`, `pivot.log`, `pivot_dim9.log`, ledger kinds
  `control_shape_matched_random`, `pivot_density_cell`, `density_map`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper — the highest-leverage methodological item in the
  slice.** "A null is worthless unless the matched control fires" is a rule that
  should be applied to any new circuit before spending search budget.

### dim10-quad-ladder
- **Family:** exhaustive SLP search with cube sharding.
- **What it does:** Exhaustively refutes successive gate budgets `k` for the two
  dim-10 cross-family quads `{0,7,8,24}` and `{0,7,8,16}`, sharding the search by
  depth-3 root cubes so that a level is resumable to the cube.
- **Twist vs siblings:** the k=11 levels that e10 never tried — they cost only
  ~45 CPU-min each and collapsed the entire question to a single open level.
- **Measured performance:** **`12 <= cost <= 13` for both quads**, both ends
  machine-checked. k = 8, 9, 10, **11** all `exhaustive: true`. k=11 =
  6,043,276,712 nodes (2,726 CPU-s) / 5,846,598,421 nodes (2,669 CPU-s). k=12
  measured-projected at **~1.92e11 nodes ≈ 38 CPU-hours per quad**; **276 of
  34,080 root cubes (0.81%) closed and banked, no bound claimed**.
- **Cost:** ~2 CPU-hours banked at k=11 plus 0.60 CPU-hours of k=12 cubes.
- **Code:** `e11_quad10/code/qsearch_shard2.c`, `code/shard.py`,
  `code/shardcontrol.py`, `code/decide.py`, `code/finalize.py`.
- **Logs/results:** `k11_q24.log`, `k11_q16.log`,
  `shards/q0_7_8_24_k12.jsonl` (276 closed cubes, resumable),
  `shardcontrol.log`/`shardcontrol2.log` (2.0M), `ledger.jsonl` (110 rows).
- **Generality:** CIRCUIT-GENERIC (the searcher takes an arbitrary target mask
  set); the two quads are MC-specific inputs.
- **Phase-2 verdict:** **keeper.** The only exhaustive-ladder instrument in the
  slice with a measured, resumable price at its open level.

### search-free-gap-hunt (planted-program screen)
- **Family:** one-sided existence screen.
- **What it does:** Plants verified `s`-gate programs whose outputs are four
  weight-5 targets at the real shape, computes `cost_cf` exactly by MILP, and
  certifies a strict cancellation gap wherever `cost_cf > s` — no search at all.
- **Twist vs siblings:** finds gaps without any exhaustive refutation; it can
  never rule one out.
- **Measured performance:** 150 planted 12-gate programs (`cost_cf` histogram
  `{9:18, 10:77, 11:51, 12:4}`) and 600 with `>= 2` cancelling target gates —
  **0 of 750 with `cost_cf >= 13`**, i.e. a 12-vs-13 gap at the real quads' level
  is rare enough not to appear in 750 directed plants. Uniform planting produces
  the shape 0 of 4,000 times, which is why the planter directs its last 4 gates.
- **Code:** `e11_quad10/code/hunt13.py`, `code/plantgap.py`, `code/planted10.py`.
- **Logs/results:** `hunt13_s12_fc2.log`, ledger kind `gap_existence_hunt`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper** — cheap directed evidence where exhaustion is
  unaffordable, provided the one-sidedness is stated.

### partial-budget-worthlessness-calibration
- **Family:** instrument diagnostics.
- **What it does:** Plants instances that *provably* have a `k`-gate program and
  asks the sharded canonical-order DFS for SAT at that `k`, measuring how much of
  the level must be consumed before the solution is reached.
- **Measured performance:** one instance SAT in **6.1 s**; a second consumed
  **1,583,819,419 nodes (0.82% of the level) without reaching any solution**,
  though one is guaranteed to exist. Conclusion: *"no SAT found" at dim 10, k=12
  under any partial budget carries almost no information* — which retro-voided
  e10's 90-second k=12 probes (0.02% of the level).
- **Code:** `e11_quad10/code/planted10.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper — should be run before any new partial-budget
  search programme is funded.**

### legibility-profiling (D-instrument, progress vs investment gates)
- **Family:** structural analysis of optima.
- **What it does:** Defines `D(S) = Σ_targets (δ_S(t) − 1)` with exact δ, splits
  every gate into "progress" (`dD < 0`) and "investment" (`dD = 0`), and compares
  four quantities per instance: `k*` (SAT-certified optimum), `k_strict` (min over
  all-progress circuits), `k_cf` (min cancellation-free), `k_greedy` (best of 2000
  BP restarts).
- **Twist vs siblings:** it does not search for circuits — it measures whether a
  legible search *could* have found the optimum.
- **Measured performance:** **`k_strict = k*` on 39/39 decided instances** (0
  counterexamples, 4 UNDECIDED timeouts) — optima never need locally-senseless
  gates, so the 88s' legibility is not evidence against optimality. But greedy
  misses the optimum **6 of 7** times on MC-density-matched instances (by 1–2
  gates in 13–16). GF(4) mini-MixColumns: `k* = 14` vs greedy 15, and only 6/14
  of the optimum's gates are greedy-top — *"optima are not senseless; they are
  patient."* All five 88s carry 0–2 investment gates out of 88, D0 = 152.
- **Cost:** ~2 h per dim-8 ρ-orbit `k=11` UNSAT certificate; three dim-12 orbits
  left UNDECIDED after 3 h/level.
- **Code:** `e12_legibility/code/smallscale.py`, `code/lib12.py`,
  `code/records.py`.
- **Logs/results:** `ledger.jsonl` (65 rows), `records_profiles.jsonl`,
  `data/*.witnesses.json` (43 files), `logs/` (11 logs).
- **Generality:** CIRCUIT-GENERIC (families are parameterised); the `records.py`
  half is MC-hardcoded.
- **Phase-2 verdict:** **keeper** — it is the only method here that prices what a
  heuristic search is structurally blind to.

### cluster-currency-hand-reasoning (e13's four-lane composition)
- **Family:** hand reasoning, refereed.
- **What it does:** Partitions the 32 outputs into clusters and planes, develops a
  "currency" algebra of shared sub-masks, prices every mechanism as an explicit
  gate list, and composes cluster blocks into a full circuit; an adversarial audit
  lane recounts every claim and every assembly is oracle-verified before banking.
- **Twist vs siblings:** no solver anywhere in the loop. The ledger law is *"no
  count without a gate list"*.
- **Measured performance — THE HEADLINE:** the trajectory
  **106 → 97 → 91 → 90 → 88** (flat+F1 at 106; C012's HBC frame at 97; three
  independent 91 witnesses; `corner90`; then the composition at 88), and the
  composed 88 is **gate-for-gate the known record**: *"all 88 operand-mask pairs
  coincide; the two circuits differ only in topological ordering"*
  (`e13_hand87/cluster_campaign/RESULT.md` §Verdict, lines 5–16). I re-verified
  `assembly_stage5.json`: `gates=88 depth=5 outputs_built=32/32 problems=0 —
  VALID`. It reconstructed the optimum from scratch by reasoning; it did **not**
  find a new 88 and did not reach 87.
- **Cost:** one multi-agent session; every claim single-core seconds-to-minutes.
- **Code:** `e13_hand87/cluster_campaign/assemble.py` plus lane scratchpads.
- **Logs/results:** `cluster_campaign/RESULT.md` (14K), `AUDIT.md`, `LEDGER.md`
  (73K), `C012.md`/`C34.md`/`C567.md`, `RECORD_TAPWORLD.txt`, and the stage
  ladder `assembly_stage0..5.json` (108/97/…/90/88).
- **Generality:** MC-HARDCODED in its content (planes, taps, Fano interfaces), but
  the *method* (cluster/currency frame + adversarial pricing) is transferable.
- **Phase-2 verdict:** **keeper — the single most transferable methodology in the
  slice**, and the proof that a reasoning fleet can reach a SAT-derived record.

### window-cut-compressibility (laneCUT / `d(S)` split)
- **Family:** local-surgery exhaustive search.
- **What it does:** For a window `S` of gates, splits the compressibility question
  on `d(S)` = number of internal gates, because budget − interface = `d(S) − 1` is
  exactly the number of free intermediate masks a replacement may use. `d(S)=1`
  can be searched to exhaustion by BFS over windows; `d(S)>=2` adds one free
  helper; `d(S)>=3` adds triples.
- **Twist vs siblings:** the `d(S)` decomposition is what turns "look for a
  smaller re-implementation of a sub-circuit" from a heuristic into a complete
  search with a stated budget.
- **Measured performance:** `d(S)=1` BFS **closed on its own** (ran out of
  windows, not budget) on 88@5 (6,848 windows), 88@5fs (18,564), 88@6 (26,498),
  88@7 (386,922) — **0 compressible everywhere**. Two errata are recorded in
  place by e15's re-run: the published 14,564 was a transcription error for
  18,564; the published 387,395 **does not reproduce** (386,922), and the row's
  result is untouched. The 88@8 row never finished here (e15 later closed it at
  2,220,037 windows).
- **Code:** `e13_hand87/laneCUT/adopt.py`, `slack.py`, `triple.py`, `cut.py`,
  `cut2.py`, `anatomy.py`; controls `mkcontrol.py`, `mkcontrol2.py`.
- **Logs/results:** `laneCUT/RESULT.md`, `NOTES.md`, `d7.log`, `d8.log`,
  `slack_d5_a2.log`, `control_89.json`, `control_89b.json`.
- **Generality:** MIXED — the window/`d(S)` machinery is circuit-generic; the
  oracle and target masks are MC-hardcoded.
- **Phase-2 verdict:** **keeper — this is the workhorse.** It is the direct
  ancestor of e15's `sweep.py` and of the whole population sweep.

### transposition-principle
- **Family:** structural theorem + artifact transfer.
- **What it does:** Applies the transposition principle to a MixColumns SLP to
  obtain an SLP for `M^T`, and measures whether the transposed circuit can be
  cheaper (the hope was that reused outputs would develop slack).
- **Measured performance:** **it cannot, ever.**
  `gates(T) = Σ_v (f_v + e_v − 1) = a + n − m`, so for `m = n = 32`,
  `gates(T) = a` identically — the handshake lemma forces `Σ f_v = 2a` and
  distinct outputs force `Σ e_v = n`. Verified on all five 88s (reused-output
  count varies 2→6, every feeding column constant). Produced 5 new artifacts:
  `T_mixcolumns_88gates_depth{5,5fs,6,7,8}.json`, oracle-VALID against its own
  `M^T` oracle, plus two hand 107s.
- **Code:** `e13_hand87/laneT/transpose.py`, `accounting.py`, `verify_T.py`,
  `fromscratch_T.py`.
- **Logs/results:** `laneT/RESULT.md` (10K), `k4.log`, `k4T_patched.log`.
- **Generality:** CIRCUIT-GENERIC (the identity holds for any XOR SLP).
- **Phase-2 verdict:** **dead end, and valuably so** — it closes the whole
  transposition direction by identity, one line, for any target circuit.

### topdown-algebra-plus-peephole (laneFRESH)
- **Family:** from-scratch construction + local improvement.
- **What it does:** Derives MixColumns from the pair/triple plane algebra
  (`OUT_k = X(m_k) + T_k`, TAPS = {1,3,4}), builds several structurally unrelated
  from-scratch designs, then applies a strict peephole loop and a plateau walk.
- **Measured performance:** a **hard 108 attractor — four structurally unrelated
  from-scratch designs land on exactly 108**. Only two one-off cancellations get
  below it by reason (worth 4 gates together: 108 → 106 → 104). Best by
  reason+peephole: **99 @ depth 5**; best at all: **95** by an illegible machine
  plateau walk. 15 oracle-verified artifacts spanning 95–121 gates.
- **Cost:** seconds to 300 s per walk.
- **Code:** `e13_hand87/laneFRESH/d1_flat.py`, `hand.py`, `improve.py`,
  `walk.py`, `rebuild2.py`, `rebuild3.py`, `d3_loop.py`, `d5_wshape.py`.
- **Generality:** MC-HARDCODED (the plane/tap algebra); the peephole/walk half is
  circuit-generic.
- **Phase-2 verdict:** **superseded-by-cluster-currency-hand-reasoning** for
  reaching a record; keep as the calibration of what naive top-down algebra costs.

### free-move-orbit-closure (e14 `closure.py`)
- **Family:** plateau geometry / exhaustive enumeration.
- **What it does:** Defines two gate-count-preserving "free moves" —
  **re-association** (changes exactly one gate mask) and **re-parenting** (changes
  none) — and enumerates the closed connected component of a given 88 under them,
  checking every state for a duplicate mask (which would be an 87 by deletion).
- **Twist vs siblings:** it is the only method that *partitions* the plateau
  rather than sampling it.
- **Measured performance — HEADLINE:** the five studied 88s (record@d5, fs@d5,
  88@d6, 88@d7, 88@d8) lie in **five pairwise-distinct CLOSED components of
  729 / 2,187 / 10,935 / 26,730 / 4,212 states = 44,793**, all five closures
  independently re-enumerated by the audit lane; pairwise distinctness settled by
  **direct set intersection on all ten pairs**, with union cardinality = sum of
  cardinalities over the 44,793 states. **Zero free 87s** (no duplicate mask, no
  dead gate) in any of them (`e14_plateau87/RESULT.md` items 1 and §The
  87-negatives).
- **Cost:** hours; the d7 intersection completed inside its cap after being
  wrongly projected as unaffordable.
- **Code:** `e14_plateau87/closure.py`, `control.py`, `basis/component.py`,
  `basis/orbits5.py`, `basis/lipschitz.py`.
- **Logs/results:** `RESULT.md`, `laneBASIS.md`, `AUDIT.md` §19.6/§26,
  `basis/orbits5.log`, `basis/dupscan.log`.
- **Generality:** CIRCUIT-GENERIC — both moves are defined on any XOR DAG; only
  the validity oracle is MC-specific.
- **Phase-2 verdict:** **keeper**, but carrying its own binding guard: both moves
  preserve gate count, **so if an 87 exists it lies in none of these components by
  construction. These tables describe the 88 plateau; they are not evidence about
  87.**

### dfine-metric-and-farthest-point-extraction
- **Family:** structural metric / population census.
- **What it does:** `D_fine` = half-L1 distance between gate-mask multisets,
  minimised over the four byte rotations; re-association is Lipschitz-1 under it
  and re-parenting is exactly invariant, so `D_fine` values are **certified lower
  bounds on free-move distance**. Farthest-point extraction then picks the
  on-disk 88s maximally remote from everything already studied.
- **Measured performance:** of 18,355 valid 88s in the repo `*88gates*.json`
  corpus (17,283 distinct mask multisets), **16,536 — 90.1% — sit at
  `D_fine >= 21` from all five studied circuits.** Extraction names eight points
  F1–F8, all oracle-VALID. The full 13×13 matrix: minimum pairwise over all 13 =
  **21**, attained at (record, d8) — a **known-known** pair; minimum among the
  eight F-points = 38; minimum from every known = 39. *"The eight new points are
  further from each other and from the knowns than the knowns are from one
  another."*
- **Code:** `e14_plateau87/basis/dfine.py`, `topmetric.py`, `census_filter.py`;
  scratchpad `dfine_pop.py`, `mass_pop.py`, `cache_pop.py`;
  `e15_campaign3/tools/dfine_pop.py`, `farpoints.py`, `dfine_scan.py`.
- **Logs/results:** `e14_plateau87/RESULT.md` §6, `LEDGER.md` §5.3/§5.6,
  `e15_campaign3/dmin.tsv` (2.9M), `probes/DECODE_TARGETS_dfine.json`.
- **Generality:** CIRCUIT-GENERIC apart from the rotation group (which is
  `Aut(M)`-specific and would need recomputing for another matrix).
- **Phase-2 verdict:** **keeper — the only frame instrument of e14 that survived
  attack.** Everything else (8 anatomy rows, 4 DAG statistics) died.

### wl-plane-isolation-symmetry-proof (laneFS88)
- **Family:** exact symmetry computation.
- **What it does:** 1-WL colour refinement to isolate planes, then a complete
  pruned DFS over input-bit permutations, to compute the stabiliser of the target
  mask set exactly.
- **Measured performance:** **the stabiliser has order EXACTLY 4** — the byte
  rotations, nothing more. There is no hidden symmetry, so the project's `σ` test
  is tight. Also produced the chimeras `chimA`/`chimE` (oracle-VALID 88s outside
  their parents' closed components — new *circuits*, not new *designs*), and the
  single-gate-removal negative on all five knowns.
- **Code:** `e14_plateau87/sym.py`, `edgesym.py`, `splice.py`, `splice2.py`.
- **Logs/results:** `laneFS88.md` (80K), `FS88_DECODE.md`, `FS88_listing.txt`,
  `laneFS88_chimA_record_x_sig2.json` (I re-verified: **VALID**, 88 gates,
  depth 5), `laneFS88_chimE_d8_x_sig2.json`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper** — computing `Aut` exactly is the first thing to
  do on a new circuit.

### local-surgery-pricing (laneBEND)
- **Family:** priced local moves.
- **What it does:** Attempts count-preserving or count-reducing surgeries on known
  88s — output chaining add/remove, one-rotation collisions, mint-and-chain
  detours through 89 — and prices each in gates.
- **Measured performance:** output chaining is **+1 in both directions** (209 add
  constructions, 12 removals, all landing at 89); **74 rotations across five
  knowns + stage5, 0 collisions**; mint-and-chain detours through 89 re-entered
  the known components 6/6. Rigidity: alternative wirings at fixed masks number
  **0/0/0/0/2** across the five knowns — four of five are perfectly rigid.
- **Code:** `e14_plateau87/reparent2.py`, `rigid.py`, `seams.py`, `blocks.py`,
  `orbit.py`.
- **Logs/results:** `laneBEND.md` (56K) plus 12 `laneBEND_*.json` artifacts
  (including two explicitly `REJECTED`).
- **Generality:** MIXED.
- **Phase-2 verdict:** **superseded-by-e15's PC001–PC005 / e16's lane536**, which
  run the same species of move exhaustively over the whole corpus.

### algebraic-frame-derivation (laneBASIS)
- **Family:** ladder/atlas-style algebraic construction.
- **What it does:** Derives MixColumns from a single-frame algebraic form
  (`M = 1 + Xz + z^3`, unipotent) and from a fully-decomposed Jordan form, to
  measure what a purely algebraic derivation costs.
- **Measured performance:** `basis/zframe_105.json` — **VALID 105**, the best
  single-frame algebraic derivation; `basis/jordan_140.json` — **VALID 140**, the
  fully-decomposed design "priced honestly: conjugation moves cost".
  Also produced the Lipschitz lemma that made `D_fine` load-bearing.
- **Code:** `e14_plateau87/basis/zframe.py`, `jordan.py`, `zcoords.py`,
  `flat108.py`, `ringcheck.py`, `tight.py`, `wide.py`.
- **Generality:** CIRCUIT-GENERIC in method (any matrix with a polynomial form).
- **Phase-2 verdict:** **keeper as a baseline generator** for a new circuit — it
  gives a legal starting circuit and an honest algebraic ceiling in minutes.

### free-gate-scan
- **Family:** cheap exhaustive negative.
- **What it does:** Scans a valid 88 for a duplicated gate mask or a
  consumer-less non-output gate; either one *is* an 87 by deletion.
- **Measured performance:** **ZERO across all five closed orbits (~45k circuits,
  three independent measurements) and ZERO across the 18,355 valid 88s of the
  repo corpus** — two independent loaders, zero duplicated masks, zero dead
  gates. Explicit scope: it rules out only an 87 obtainable by deleting a
  redundant gate from an 88 already on disk or free-move-reachable from the five
  knowns. **No positive control is constructible — exhibiting one would be the
  prize.**
- **Code:** `e14_plateau87/audit_tools.py`, `e15_campaign3/tools/free87_all.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper** — it costs nothing and it is the cheapest
  possible tripwire. It is also the ancestor of the B=56 tripwire below.

### population-window-sweep (e15 `sweep.py`, tiers B / FH / D3)
- **Family:** plateau search at population scale.
- **What it does:** Runs laneCUT's window/`d(S)` compressibility search over the
  whole on-disk 88 population instead of a handful of reference circuits. Tier B
  = `d(S)=1` window BFS + `d(S)>=2`; tier FH = the free-helper `d(S)>=2` regime
  only; tier D3 = the triple-seeded `d(S)>=3` regime. One compressible window
  anywhere is an 87 on the spot.
- **Twist vs siblings:** it is the first time anything of the kind was run past
  the five knowns, and every row carries its own truncation boundary as a field
  (`{why, maxwin, at_base, bases_done, bases_total}`) so a capped row can never be
  read as a closed one.
- **Measured performance:**
  * **13-anchor pass (tier B), COMPLETE 2026-08-28 00:12:** `d(S)=1` CLOSED on
    11 of 13, **CAPPED on 2 (F3 at 10 of 88 bases, F7 at 41 of 88)**;
    `d(S)>=2` COMPLETE 13/13; **12,073,707 windows, 0 compressible, 0 shared
    helpers, 0 B-alarms.**
  * **Run A (tier FH), COMPLETE 2026-08-28 22:38:** **17,283 rows = the entire
    distinct-mask-multiset population**, all VALID88, all `d2.tested = d2.seeds =
    1,540`, `compressible_total = 0` on every row, 0 duplicate rows, and the
    swept-path set equals `popfull.txt` exactly. Reproduced here:
    `wc -l experiments/e15_campaign3/sweep_A_fullpop.jsonl` → **17283**;
    `wc -l .../popfull.txt` → **17283**.
  * **d3 anchor pass, COMPLETE 2026-08-29 04:12:** 13 rows × 27,720 triples =
    **360,360 triples, all tested, 0 skipped, 0 compressible**, 19,845.6 s.
    (`wc -l .../sweep_D3_anchors.jsonl` → **13**.)
  * **Six shared-helper rows found** (four carrying 1, two carrying 3) — the
    first ever recorded on valid 88s, **falsifying e13's inherited universal**
    "no mask finishes more than one window; all helpers are distinct". None
    compresses, but `d(S)>=3` on the population is therefore **not** closed by
    e13's argument.
- **Cost:** run A ≈ 19 CPU-hours (2 shards, 77,860 s and ~78,000 s wall); d3
  ≈ 5.5 CPU-hours; the unbought `d(S)=1` population pass prices at **~1,200
  CPU-hours** (255 CPU-s/circuit vs 4 CPU-s for free-helper).
- **Code:** `e15_campaign3/tools/sweep.py` (the driver), `tools/adopt.py`,
  `tools/slack.py`, `tools/triple.py`, `tools/cut.py`.
- **Logs/results:** `sweep_A_fullpop.jsonl` (12M), `sweep_D3_anchors.jsonl`,
  `sweep_ledger.jsonl` (32 tier-B rows, **15,099,957** `d1.windows` summed),
  `logs_A_shuf00.log`/`_01.log`, `logs_D3_anchors.log`, `laneSWEEP.md` (68K).
- **Generality:** MIXED — the window machinery is circuit-generic, the oracle and
  the target set are MC-hardcoded, and the corpus is MC-specific.
- **Phase-2 verdict:** **keeper — the single most reusable search method in the
  slice**, with two declared sub-gaps carried forward (below).

### b56-tripwire  ★ TOP-PRIORITY CATALOG ITEM
- **Family:** proved-theorem-turned-live-detector.
- **What it does:** Counts `B` = the number of non-output gates that have a
  consumer, on every circuit the sweep touches. On a valid 88 this must be 56;
  anything else means an 87 is available *by deletion*.
- **THE THEOREM, verbatim** (`e15_campaign3/laneSWEEP.md` §11, lines 1250–1258;
  attribution "AUDIT3, proof verified at ARCH3's desk; ARCH3 R53, binding"):

  > On any valid 88-gate MixColumns circuit *not already reducible to 87*,
  > `B = 56` exactly, where `B` = the number of non-output gates that have a
  > consumer.
  > Sketch: validity puts all 32 targets on gates; two gates with the same mask
  > make the later deletable (an 87); a non-output gate with no consumer is
  > deletable (an 87). So 88 distinct masks, exactly 32 output gates, 56
  > non-output gates, all with consumers.

  **The contrapositive is the 87 detector:** `B != 56` on a valid 88 means a
  duplicated mask or a consumer-less non-output gate, and in *either* case an 87
  is immediately available by deletion. Generalised in `e17_pure/DOSSIER.md`
  §3.4 as the `87 = 32 + 55` split.
- **Proof location:** `e15_campaign3/laneSWEEP.md` §11 (statement + sketch +
  fail-ability check); `e15_campaign3/AUDIT.md` §11.4 (the proof as banked by
  the referee); restated in `e15_campaign3/RESULT.md` §"durable list" item 2 and
  in `e17_pure/DOSSIER.md` §3.4.
- **Code that RUNS the tripwire:** `e15_campaign3/tools/sweep.py` —
  `count_B(c)` at **line 296** (`return sum(1 for g in range(c.n) if not
  c.isout[g] and c.cons[g])`), wired into every row at **lines 525–532**
  (`rec['B'] = count_B(c)`, `rec['B_theorem_ok'] = (rec['B'] == 56)`, and an
  `ALARM` string on failure), with the loud path at **lines 730–738** (writes
  `ALARM_B_<ts>.json` and prints `*** B-THEOREM ALARM (87 AVAILABLE)`).
- **Measured performance:** fired **ZERO** times on **17,283 / 17,283** run-A
  circuits and **13 / 13** d3 anchors. **No `ALARM_B_*.json` exists anywhere on
  disk** (`find experiments/e1[0-7]* -name 'ALARM*' -o -name 'STOP' | wc -l` →
  **0**). `B = 56` established two ways because 906 stale-build rows lack the `B`
  field: the explicit `B` reads 56 on all 16,377 rows carrying it with
  `B_theorem_ok: true`, and on all 17,283 rows `helpers.bases = 56` and
  `d2.seeds = 1,540 = C(56,2)`; zero mismatches where both are present. The d3
  seed count `27,720 = C(56,3)` is the same theorem arriving a fourth way, and
  the 89-gate controls carry `29,260 = C(57,3)` — the theorem read from the
  failing side. **Fail-ability check: `count_B` reads 57 on both 89-gate
  controls and 56 on the 88s**, so the detector can and does report the alarm
  value. A retroactive scan of every row the lane ever banked (230 valid-88 rows,
  including two superseded files) found 0 with `seeds != 1540`.
- **Cost:** ~free — one pass over the gate list per circuit.
- **Generality:** **MC-HARDCODED only in the constant.** The theorem is
  `B = n − (#outputs)` for any irreducible SLP with distinct masks and all
  outputs on distinct gates; for a new circuit with `q` outputs at size `n` the
  tripwire is `B == n − q`. **This is the item to port first when aiming at
  `aes_inv_mixcolumns`** — it is a free, always-on, provably-sound
  one-gate-improvement detector.
- **Phase-2 verdict:** **keeper, highest priority.** It is the campaign's only
  live 87 detector and it is exactly the artifact the Jean follow-up wants: feed
  a foreign 88 to it and it either confirms `B = 56` or hands you an 87.

### mechanism-decode-and-library
- **Family:** structural analysis / vocabulary.
- **What it does:** Decodes an unfamiliar 88 gate-by-gate into named mechanisms
  (currency keying, helper fusion, Σ-fusion, corner mechanisms, plane drops) and
  banks them in a schema-conformant library with an incompatibility map.
- **Measured performance:** 13/13 anchors examined (F1 gate-for-gate; F2/F3 at
  full mechanism level); `MECHANISM_LIBRARY.md` v2.7 = **15 entries + 6 notes**,
  six errata struck in place. **Its scope measurement travels with it: the named
  objects cover 21.1% of the plateau's vocabulary (280 of 1,330 masks), 36.5%
  weighted by occurrence.** Population-scale structural facts that survived: the
  `s_0` prohibition (0 of 18,355, and *derived*, not merely observed — but
  labelled gate-count-free, so it can never filter an 87), the doubled-sum law,
  the complementary-Fano identity, `priv4 ⇒ not-s_7` at 952/952.
- **Code:** `e15_campaign3/attrib.py`, `roles.py`, `vocab.py`, `plane7.py`,
  `dfine.py`, `lineage.py`, `compose/frame.py`, `compose/demand.py`.
- **Logs/results:** `MECHANISM_LIBRARY.md` (68K) + `_v1.2_superseded.md`,
  `INCOMPATIBILITY_MAP.md`, `laneDECODE.md` (46K), `F1_DECODE.md`,
  `F2_F3_DECODE.md`, `F5_F8_DECODE.md`, `F1..F8_attrib.txt`.
- **Generality:** MC-HARDCODED.
- **Phase-2 verdict:** **keeper as a record**, but note the campaign's own
  conclusion: **the composition thesis is dead by an identity** — `88 = 32 + 56`
  is forced, every mechanism moves a gate between the currency and helper piles,
  and *"a composition of wash-mechanisms is a wash."*

### composition-and-splice-search (N1 / N2 / N2')
- **Family:** recombination search.
- **What it does:** Splices cluster blocks or per-output cones between known 88s
  and minimises the resulting gate count.
- **Measured performance:** N1 (two-frame cluster splice, 20×19×254 = **96,520**
  subsets) — **min 88, EXHAUSTIVE at cluster granularity**. N2 (`20^8` =
  25.6 billion free per-cluster mixes, 18.9M nodes, 81 s) — **min 88, exhaustive
  on that space**. N2' (per-output splice over `20^32`, hill-climb from 80
  starts) — min 88, local. N1's optimal splice **rebuilt d7 exactly** (record and
  d7 share their C567 block) — an identity check, not a new circuit.
- **Code:** `e15_campaign3/compose/splice.py`, `build_splice.py`,
  `outmix.py`, `outclimb.py`, `absorb.py`, `cover.py`, `mixmin.py`.
- **Logs/results:** `laneCOMPOSE.md` (97K), `laneCOMPOSE_STALL.md`,
  `laneCOMPOSE_splice_d7C0-4_recordC5-7.json`, `compose/splice_top.json`,
  `compose/outmix_result.json`, `compose/outclimb_result.json`.
- **Generality:** CIRCUIT-GENERIC given a corpus of circuits to splice.
- **Phase-2 verdict:** **dead-end for gate count** (the wash identity), keeper as
  a *diversity generator* for a new circuit's corpus.

### vocabulary-restricted-ILP (N3)
- **Family:** exact solver encoding.
- **What it does:** Asks `Q(V, n)`: is there an `n`-gate circuit using only masks
  from a fixed vocabulary `V`? Encoded as an ILP/CP-SAT model with acyclicity.
- **Measured performance:** validated in both directions (C2 INFEASIBLE path with
  0 conflicts, reproducing laneFS88's no-gate-removable result by a second
  unrelated method; C3 FEASIBLE path with an oracle-VALID witness);
  `Q(V_K1, 87)` INFEASIBLE at two desks. **Then a ceiling, not a curve:** a
  three-point probe at `V = 134` found **no recovery at 11× budget** — rounds
  flat (+11%) while seconds grew 11.2×. The rank encoder was retired by
  measurement (24.8M branches, no close at 805). **`Q(V*, 87)` — "is there an 87
  using only masks some known 88 already uses?" — WAS NOT REACHED. IT WAS NOT
  ANSWERED NEGATIVELY.** `V*` is 1,393; no current encoder reaches above ~100–134
  masks.
- **Code:** `e15_campaign3/compose/n3_ilp.py`, `n3_lazy.py`, `n3_lazy_ladder.py`,
  `n3_run.py`, `n3_run87.py`, `ilp_size.py`, `completeness.py`.
- **Logs/results:** `N3_ILP_SPEC.md`, `n3_results/` (10 files incl.
  `joint_pop.jsonl` 4.8M, `corpus_scan.jsonl` 2.9M), `n3_session1.log`,
  `joint_pass.log`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper with a named blocker — "what is needed is a
  different instrument, not a bigger budget for this one."**

### excursion-probes PC001–PC005
- **Family:** single-move surgery, corpus-wide.
- **What it does:** Five probes, each a single count-preserving-or-reducing move
  with a fail-able control: PC001 re-parent an orphan; PC002 rotation collisions;
  PC003 marginal-object excursion; PC004 the 1-mint/2-orphan funnel on 13
  anchors; PC005 the same funnel on the **full corpus**.
- **Measured performance:** PC001 **0 orphanable / 728 gates** (control 56/56);
  PC002 **0 collisions in 172 legal rotations** (calibration 6/6, planted 12/12);
  PC003 negative by derivation with the closure enumerated; PC004 587 → 37 → **0**;
  **PC005: 800,994 two-consumer gates → 55,970 candidate sites → 536
  non-trivial → 0.** PC001/PC002 were the first time the F-points were ever probed
  — **scope: POINTS, not ORBITS** (closed later by e16).
- **Code:** `e15_campaign3/compose/orphan_fpoints.py`, `rot_fpoints.py`,
  `rot_control.py`, `orphan_control.py`, `funnel.py`, `scan_1m2o.py`,
  `scan2_1m2o.py`, `corpus_scan.py`, `plant_1m2o.py`, `verify_hit.py`.
- **Logs/results:** `probes/PC001..PC004*.json`,
  `n3_results/corpus_scan.jsonl`, `corpus_scan.log`.
- **Generality:** CIRCUIT-GENERIC given a corpus.
- **Phase-2 verdict:** **keeper** — PC005 is the template for a cheap
  corpus-wide one-move negative on any new circuit.

### ops-harness (slot-guard / chain / identity-based process census)
- **Family:** operational discipline (not a search method, but a reusable one).
- **What it does:** A start-only, cap-respecting resume script that recomputes
  remaining work *from the ledgers on disk* rather than the process table; a
  chain that launches the next stage when a slot frees; and a guard that ALARMs
  (but never acts) when startable work exists and a slot is idle. Process
  identity is established by `/proc/<pid>/cwd`, never by pattern — `pkill` is
  banned across every campaign in this slice.
- **Measured performance:** the guard correctly detected shard 0 down with its
  restart budget spent and ALARM-ONLY'd rather than restarting; it exited cleanly
  at `no startable work (runA 0 unswept, d3 0/13, d3 running=yes; partition OK
  17283 rows)`. Run A completion was **verified from the ledger, not the process
  table**.
- **Code:** `e15_campaign3/tools/slot_guard.sh`, `resume_all.sh`, `procid.sh`,
  `launch_shard1_then_d3.sh`, `freshcheck.sh`.
- **Logs/results:** `logs_slot_guard.log`, `logs_chain.log`,
  `.slot_guard_restarts`, `.start.lock`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper** — this is the harness that let a saturated
  20-core box run a 3-day sweep alongside four untouchable solvers.

### maskspace-free-move-closure-with-tripwires (e16 `fpclose.py`)
- **Family:** plateau geometry, second generation.
- **What it does:** A mask-space re-implementation of e14's free-move closure,
  ~8× faster (≈27 states/s → the run reports ~180 states/s aggregate), plus
  **three collapse tripwires**: T1 duplicate mask, **T2 dead gate** (re-parenting
  orphans an operand), **T3 re-association collision** (the minted mask already
  exists). T2 and T3 are the two routes e14's code never tested and silently
  dropped respectively.
- **Twist vs siblings:** the argument that T1/T2/T3 are the *only* ways a
  count-preserving move can yield a sub-88 circuit is written out and declared as
  sub-gap SG4.
- **Measured performance — HEADLINE:** **333,396 states across the eight F-point
  components, all eight CLOSED by exhaustion** (F1 91,368 / F2 19,683 / F3 729 /
  F4 2,187 / F5 2,916 / F6 17,496 / F7 243 / F8 198,774), 4,856,598
  re-association sites and 436,914 re-parentings probed, **T1 = T2 = T3 = 0
  everywhere, minimum reachable gate count 88 at every one**. Added to e14's five
  orbits: **378,189 enumerated states across thirteen closed orbits, zero sub-88
  states.** No component contains any other anchor at any rotation → **the
  thirteen studied 88s lie in thirteen pairwise-distinct closed orbits.**
  *(I re-derived the state counts from the bank sizes at 8 bytes/gate × 88 gates:
  the eight files sum to exactly 333,396 — reproduces the reported number.)*
  Free by-product: running T2/T3 over e14's own 44,793 states gives 0 and 0.
- **Controls — five, one of which failed first:** CONTROL 1 reproduced all five
  of e14's banked cardinalities exactly (729/2187/10935/26730/4212, sum 44,793);
  CONTROL 2 showed broken engines fail (B2 no-re-association → 1 state vs 729;
  B3 no acyclicity guard → 378 CLOSED=False); CONTROL 3 is pointwise identity
  with e14's `closure.py` **imported verbatim**, 8/8 states identical on five
  components **including F1**; CONTROL 4 fired both tripwires on planted 89-gate
  structure end-to-end through the root oracle (rebuilt 88s oracle-VALID);
  CONTROL 5 wrote 12 random banked states per component to disk and oracled them
  — **96/96 VALID, gate counts seen `[88]`**. The first version of CONTROL 2 was
  *worthless and said so* (B1 reproduced 729 because re-parenting is inert on
  record@d5) and is kept in the ledger because it is the informative part.
- **Cost:** 2,336 s wall total across eight components, 2 processes, `nice -n 15`.
- **Code:** `e16_lastwish/laneFPOINT/fpclose.py` (engine), `fprun.py` (run),
  `control_fp.py`, `xval.py`, `tripwire_control.py`, `bankcheck.py`.
- **Logs/results:** `laneFPOINT/RESULT.md`, `LEDGER.md`, `RESULT_F1..F8.json`,
  `bank/F*.states.bin` (**224 MB**), `bank/F*.progress.jsonl`,
  `bank/F*.alarms.jsonl` (**all eight are 0 bytes**), `CONTROL_partAB.log`,
  `CONTROL_partC.log`.
- **Generality:** CIRCUIT-GENERIC (moves are defined on any XOR DAG).
- **Phase-2 verdict:** **keeper, and it supersedes e14's `closure.py`** — same
  results, 8× faster, two extra collapse tests, five controls.

### exhaustive-small-SLP-decision (`slp3.py` / `le4_k2.py`)
- **Family:** exact micro-search with a closed case list.
- **What it does:** Decides, exhaustively, whether there is a straight-line
  program of `G <= 3` (resp. `G <= 4`) gates over a given available-signal pool
  producing **both** of two required masks. This converts a local rebuild
  question into an arithmetic one: at a k=1 site `gates = 84 + G`, so **87 iff
  `G <= 3`**; at a k=2 (three-orphan) site `gates = 83 + G`, so **87 iff
  `G <= 4`**.
- **Twist vs siblings:** it is **shape-free**. It replaces the specific "W-shape"
  the earlier instrument invented with the complete question, and is therefore
  ~100× wider.
- **Measured performance:** whole corpus, `corpus_le3.py`, 18,355 circuits,
  1,686 s: **55,970 candidate sites (k=1: 54,561, k=2: 1,409), sites with
  `G <= 3`: 0, oracle-VALID below 88: 0.** k=2 regime: 1,409 sites, 1,309 decided
  `G > 4` by the fast procedure and the **100 UNDECIDED closed by brute force,
  100/100 `G > 4`** — so **the 2-mint/3-orphan regime is CLOSED on this corpus**,
  not bracketed. Completeness attacked adversarially: `slp3.py` survived **8,000
  randomly-generated 3-gate SLPs of every topology with any 2 of 3 gates
  designated outputs — 0 missed**, plus 0/3,000 false positives and every
  returned program replayed.
- **Cost:** 1,686 s for the corpus `G<=3` run; ~11 CPU-hours would be needed to
  brute-force all 1,409 k=2 sites (not spent).
- **Code:** `e16_lastwish/lane536/slp3.py`, `le4_k2.py`, `le4_undecided.py`,
  `corpus_le3.py`, `completeD.py`, `completeD2.py`.
- **Logs/results:** `corpus_le3.jsonl` (3.7M, **18,355 rows**),
  `le4_k2.jsonl`, `le4_undecided_s*.jsonl`, `completionD2.jsonl`,
  `sites_536.jsonl` (**536 rows**).
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper** — the cleanest "is this circuit one gate from
  smaller?" decision procedure the project owns.

### identity-first-autopsy (the 536)
- **Family:** structural derivation replacing a measurement.
- **What it does:** Takes a headline measurement and asks whether it was
  *arithmetically forced*, before treating it as evidence.
- **Measured performance:** **"the 536" DISSOLVED.** It is **268 sites doubled**
  (each contributes an A/B mirror pair; 268/268 are exact mirror pairs), i.e. any
  reading of "536 opportunities" over-counts by 2×. The instrument's headline
  ("the mint is never buildable") is an **identity**: `delta(W) >= max(delta(mc1),
  delta(mc2)) − 1`, and `max(...) = 4` on **536/536**, so `delta(W) >= 3` and
  "buildable" (`= 2`) was impossible before the scan ran. Sharpest form:
  `max(delta) >= 4` holds at **99.47% of all k=1 candidate sites in the corpus**.
  Also established as an *equality*: `d(W) = minrep(W | S) − 1` exactly (a DAG of
  `k` XOR gates has at most `k+1` leaves; an `m`-term XOR costs `m−1`).
  The mints are ordinary: **97.6% (523/536) are masks some known 88 already
  builds**, 0/536 are target masks.
- **Code:** `e16_lastwish/lane536/extract536.py`, `charBC.py`, `quantE.py`,
  `jointE.py`, `ksplit.py`.
- **Logs/results:** `lane536/RESULT.md` (16K), `PREREG.md` (pre-registered
  predictions timestamped 13:04:17Z before any completion code existed),
  `mints_BC.jsonl`, `LEDGER.md`.
- **Generality:** CIRCUIT-GENERIC as a *method*; the identities are generic XOR
  facts.
- **Phase-2 verdict:** **keeper — this is the repricing discipline.** Its own
  summary: *"the number was real, the evidence it carried about 87 was much
  smaller than its size suggested."*

### forcedness-enumeration (`forced.c`)
- **Family:** exhaustive counting of optimal families at miniature scale.
- **What it does:** Exhaustive DFS with an admissible lower bound and **exact
  structural canonicalisation** (one representative per DAG, lex-min linear
  extension) that counts how many structurally distinct optimal programs an
  instance has at `L*`, `L*+1`, `L*+2`, with irredundance enforced.
- **Twist vs siblings:** it answers a *methodological* question — "does the
  existence of several distinct 88s tell us 88 is not optimal?" — rather than
  searching for a circuit.
- **Measured performance:** **99 certified-optimal instances** (n = 4..7,
  `L*` = 3..11). Families at the true optimum: min 1, **median 10**, mean 121,
  max 2,813; only **22/99 = 22%** of true optima are unique; **65%** admit ≥ 5
  families, rising to **79%** among `L* >= 8`. Forcedness collapses with
  hardness: `log10(families) = 0.324·L* − 1.09`, i.e. **×2.11 families per extra
  optimal gate**, Spearman ρ = 0.60. No cliff at the optimum (×33 from `L*` to
  `L*+1` vs ×20 from `L*+1` to `L*+2`). **Circulant miniatures — the MixColumns
  analogue — are the least forced of all: median 309 families, zero unique.**
  Verdict: the user's "a true optimum should be forced" hypothesis is **refuted**
  in this problem class; five distinct 88s discriminate nothing.
- **Controls:** hand-computable n=3 case exact; an independently written
  brute-force enumerator agrees on **40/40 comparisons** of (dags, valuesets,
  raw) across 9 instances and every level.
- **Cost:** 1 core, `nice -n 15`; ~25 min per dense n=6 instance.
- **Code:** `e16_lastwish/laneFORCED/forced.c` (+ `forced`), `runner.py`,
  `n7probe.py`, `growth.py`, `bruteforce_check.py`, `analyse.py`.
- **Logs/results:** `rows.jsonl` (91), `n7.jsonl` (8), `growth.jsonl` (20),
  `SUMMARY.txt`, `RESULT.md` (14K), `LEDGER.md` (with the pre-registration).
- **Generality:** **CIRCUIT-GENERIC and instance-generic** — it takes any target
  mask set. Scale-limited to n ≤ 7.
- **Phase-2 verdict:** **keeper** — it settles a recurring interpretive question
  cheaply, and the same code answers it for any new circuit family.

### pure-reason-theorem-lanes (e17 laneCHAIN / laneY / laneCONTRA / laneDELTA)
- **Family:** proof by hand, no SAT and no search.
- **What it does:** Four parallel lanes each attack one route to a lower bound —
  the `C_c` conjecture chain, the `kappa`/`Y` ledger, the assume-87 program, and
  the derivation of e16's `delta(mc)=2` anomaly — with every claim graded
  (a) proved / (b) proved-modulo-a-named-lemma / (c) conjectured, and with the
  standing rule that **a corpus fact can never filter a hypothetical 87**.
- **Measured performance:** see the next four entries; nothing narrows
  `56 <= L(M) <= 88`, and the campaign's own summary is that
  **`H87` survives every currently-live conjecture** — even under "the most
  generous simultaneous grant" the conjunction yields only `L(M) >= 73`.
- **Cost:** 1 core, `nice -n 15`, seconds-to-minutes per numeric check; the
  fleet was not touched.
- **Code:** `e17_pure/lane{CHAIN,Y,CONTRA,DELTA}/code/`.
- **Logs/results:** four `RESULT.md` (24K/38K/35K/39K) + four `LEDGER.md`.
- **Generality:** MC-HARDCODED in content, CIRCUIT-GENERIC in method.
- **Phase-2 verdict:** **keeper.** This is the only family in the whole project
  that produces statements about a circuit that does not exist.

### anatomy-theorem (laneCONTRA)  ★ TOP-PRIORITY CATALOG ITEM
- **Family:** assume-87 structural derivation.
- **What it does:** Assumes `H87` (a minimum-size SLP of `n <= 87` gates exists)
  and derives a conjunction of forced properties, each conjunct labelled with its
  hypotheses and its grade.
- **The theorem, in the dossier's own one sentence** (`e17_pure/DOSSIER.md` §4.4):
  > Any **minimum-size** 87-gate SLP for MixColumns has 32 finals and 55 middles
  > with pairwise distinct masks, no dead gate, no final built from two targets,
  > at least two cancelling gates, at least two distinct cancelling-gate masks
  > appearing as leaves of maximal clean trees, a cancellation weight budget of at
  > least 5 spread over a weight profile satisfying
  > `Σ_w a_w · delta_w >= 4.4098776`, no budget contribution at all from weight-2
  > cancelling leaves, `Y <= 2.5044082·kappa − 4.4098776`, and — if its cancelling
  > apparatus is as small as the arithmetic permits (`|A*| = 2`, forcing
  > `kappa = 2` and `Y = 0`) — **a cancelling gate whose output *is* one of the
  > twelve weight-7 MixColumns rows.**

  Conjuncts A1–A14 with grades are tabulated at `DOSSIER.md` §4.3
  (lines 633–655); the complete case analysis is §4.5; the three caveats a
  successor must carry are §4.6.
- **The referee-confirmed asymmetric fact (A11):** *"A10 is gate-count-
  ASYMMETRIC. At `n = 88` the same computation admits ten profiles and only
  7,362 of 19,490 admissible pairs contain a weight-7 target row — the statement
  is false at 88."* Grade **(a)**, REF_CONTRA V9, exhaustive recount. At `n = 87`
  it is **475/475 = 100%** under the banked table (profiles `{4,7}` 63, `{6,7}`
  346, `{7,7}` 66). **This is the first gate-count-asymmetric fact in the
  programme** — the first statement that distinguishes 87 from 88 rather than
  describing the plateau. Its caveat is equally load-bearing: it is *not* an 87
  detector, and dropping the `|A*| = 2` hypothesis repeats the project's `U1`
  error.
- **Cost:** seconds per script, 1 core.
- **Code:** `e17_pure/laneCONTRA/code/spectrum.py`, `perweight.py`, `close.py`,
  `final.py` (they import lane P's refereed `cflib.py` and rebuild nothing);
  referee rebuild in `e17_pure/REF_CONTRA/code/ref1..ref5*.py`.
- **Logs/results:** `laneCONTRA/RESULT.md` (35K), `results_perweight.json`,
  `results_spectrum.json`, `results_symmetrised.json`,
  `REF_CONTRA/VERDICT.md`, `REF_CONTRA/ref5_uncond.log`.
- **Generality:** MC-HARDCODED (it is a theorem about `M`), but the *shape*
  (certificate table → weight-profile inequality → forced anatomy) ports.
- **Phase-2 verdict:** **keeper — the spine of the lower-bound dossier**, and the
  thing to show Jean.

### certificate-price-LP (`B = 91.4098776`)  ★ the 91.41 cap
- **Family:** LP/certificate lower-bound machinery.
- **What it does:** Prices each (target, mask) pair in a table `p`, subject to
  **Check 1** (`max_m Σ_t p[t][m] <= 1`), and computes `B` by a subset DP; `B` is
  a lower bound on the cancellation-free cost `L_cf(M)`, and the per-weight
  constants `delta_w := max{D(m) − 1 : m ∈ U, wt(m) = w}` feed the Anatomy
  Theorem.
- **Measured performance:** the banked table
  (`fleet7/laneUNCOND/results/bstar/nostop_lp_cert_4_1.json`) gives, rebuilt
  independently by REF_CONTRA with its own Check 1 and its own DP:
  `Check 1 max column sum = 1.0000000 (exactly tight, FEASIBLE)`,
  **`B = 914098776 / 10^7 = 91.4098776`**, grade **(a) REFEREED**. It dominates
  the published U6-2 table (91.0019782) by 0.4079 and laneCONTRA's
  ρ-symmetrised table (91.1792575) by 0.2306201. `ceil(B) = 92`, re-deriving
  `L_cf(M) >= 92`. The constants:
  `delta_{2..7} = 0, 0.9999998, 1.9912788, 1.5872092, 2.0429066, 2.5044082`.
- **THE CAP — why this line is closed** (`DOSSIER.md` §5.5, grade (a) REFEREED):
  the LP **optimum** is `B* = 91.409884`. The two thresholds anyone wanted —
  `B > 92` (which would give `L_cf >= 93`) and `B > 91.9738 = 87 + 2·delta_7`
  (which would give `|A*| >= 3` for every 87 unconditionally) — **both lie above
  the LP optimum and are therefore unreachable by optimising this LP at all,
  symmetric or not.** The symmetry lever is worth `+0.0000003`: the optimum is
  already ρ-symmetric to seven places. *"Do not fund a ρ-symmetric price
  optimisation."* The one remaining purchase on the line is a **certified
  rational dual** closing `91.4098776 <= B* <= 91.409884`, scoped at ~1 session.
- **Code:** `e17_pure/REF_CONTRA/code/ref2_bound.py`, `ref3_pairs.py`,
  `ref4_controls.py`, `ref5_uncond.py`; source table under `fleet7/laneUNCOND/`.
- **Generality:** CIRCUIT-GENERIC in form (any target matrix admits the same LP);
  every constant is MC-specific.
- **Phase-2 verdict:** **keeper as a bound generator, dead-end as an upgrade
  path.**

### y-ledger-impossibility (laneY)
- **Family:** proof by counterexample + self-defeat.
- **What it does:** Attacks `Y >= kappa − c`, the only conjecture on the board
  with a measured constant and a price (`c = 6` pays `L(M) >= 58`).
- **Measured performance:** **there is no such `c`.** As stated over every SLP,
  `Y >= alpha·kappa − c` is **false for every `alpha > 0` and every `c`**, and
  stays false for *trim* SLPs — six explicit oracle-VALID witnesses reaching
  `Y − kappa = −399`. Narrowed to the size regime where the pricing needs it, the
  hypothesis is **logically equivalent to its own conclusion**: the inequality
  that converts a Y-lemma of slope `alpha` into `L(M) >= G(1+alpha) − c` is the
  same inequality that proves `Y − alpha·kappa <= n − G(1+alpha)` unconditionally.
  What replaces it is Theorem Y1, the **first upper bound on `Y`** in the
  programme, plus a general impossibility theorem at every slope. Referee
  (REF_ALGEBRA) CONFIRMED Y1–Y5 and the arithmetic, but **REFUTED as stated**
  laneY's own recommendation to strike `Y >= kappa − 6` from the board.
- **Code:** `e17_pure/laneY/code/` (+ `ylib.py`), referee rebuild
  `e17_pure/REF_ALGEBRA/code/`.
- **Logs/results:** `laneY/RESULT.md` (38K), `laneY/results/`, `laneY/logs/`,
  `REF_ALGEBRA/VERDICT.md`.
- **Generality:** MC-HARDCODED.
- **Phase-2 verdict:** **dead-end, definitively closed** — with the important
  by-product that the closure is itself a theorem.

### lemma-R / T2 corpus tripwire (laneDELTA)
- **Family:** theorem-turned-detector, second instance.
- **What it does:** **Lemma R / Corollary R\***: in an optimal SLP, for every
  (gate, private-operand) pair, `minrep(mask | available) = 3` exactly — never 1,
  never 2. A `minrep = 2` hit *is* a valid circuit with one gate fewer, produced
  constructively. **Theorem T2** (the private-cone tree theorem): `minrep(mask(c)
  | Avail(c)) = |D(c)| + 2` exactly, the cone is a tree with distinct leaves.
- **Twist vs siblings:** it is strictly wider than lane536's site frame — it drops
  the requirement that the other operand have exactly two consumers.
- **Measured performance (the tripwire actually ran, 2026-08-28):**
  * `witness.py corpus 1200`: **1,200 valid 88s, 9,100 private-operand pairs
    (7.6/circuit), minrep=1: 0, minrep=2: 0, minrep=3: 9,100 — LEMMA R HITS: 0.**
    (`laneDELTA/witness_corpus.log`; `lemmaR_hits_corpus.json` is the empty file.)
  * `witness.py nonsample`: **667 valid non-88 circuits, 11,944 pairs
    (17.9/circuit), minrep=2: 66 — LEMMA R HITS: 66 on 26 distinct circuits**,
    and five were compressed and oracled: **89→88 VALID (×3), 90→88 VALID,
    90→89 VALID** (`witness_nonsample.log`, `lemmaR_hits_nonsample.json`).
  * `cone_theorem.py corpus 150`: **T2 VIOLATIONS: 0** on 150 corpus 88s
    (13,200 gates, tree/distinct 13,200/13,200).
  * `cone_theorem.py non 90 91`: **T2 VIOLATIONS: 1**, at `n = 89`, gate 80,
    `D = [32,67]` — file
    `campaign_87/agents/frontier-d6sat/found/p1_002f1a7337e999c916e670db_r4_plus1_89gates_depth6.json`.
  * `pern.py`: the per-`n` table (88: 60 circuits/359 pairs/0 minrep2; 89: 228
    circuits/2,057 pairs/3 minrep2; 90: 63/763/5; 91: 25/348/0; 88corpus:
    600/4,564/0).
  * **Optimal circuits carry less than half the private-operand structure of
    non-optimal ones (7.6 vs 17.9 pairs per circuit)** — itself a consequence of
    Lemma R being enforced.
  * Referee (REF_DELTA) CONFIRMED T2 and its proof, and it *survived exhaustive
    enumeration of 57,139 optimal SLPs over 181 matrices*, including `|D| = 3`, a
    regime the corpus never reached — but noted it is **not new mathematics**.
- **Cost:** 71 s (1,200 88s), 173 s (667 non-88s), 281 s + 189 s (T2).
  Whole corpus would be ~80 CPU-minutes at 1 core — **not spent**.
- **Code:** `e17_pure/laneDELTA/witness.py`, `cone_theorem.py`, `nat_witness.py`,
  `pern.py`, `lemmaR_sweep.py` (superseded first cut, kept).
- **Logs/results:** `laneDELTA/RESULT.md` (39K), `LEDGER.md`,
  `witness_corpus.log`, `witness_nonsample.log`, `T2_corpus.log`, `T2_non.log`,
  `pern.log`, `lemmaR_hits_*.json`, `nat_hits.json`, `T2_witness_89to88.json`.
- **Generality:** **CIRCUIT-GENERIC** — Lemma R and T2 are statements about
  optimal XOR SLPs, not about MixColumns.
- **Phase-2 verdict:** **keeper, second only to the B=56 tripwire.** Same shape:
  a proved theorem whose violation hands you a smaller circuit, running as a
  cheap always-on scan.

### adversarial-cross-desk-referee
- **Family:** verification methodology.
- **What it does:** A referee seat rebuilds every load-bearing object **from
  source with no code shared with the claimant** — REF_ALGEBRA constructed the
  MixColumns matrix a *third* way (byte-level 8×8 GF(2) multiply matrices
  composed per coefficient) and asserted it equal row-for-row to the repo oracle's
  own targets; REF_CONTRA re-implemented Check 1 / the subset DP as a memoised
  recursion rather than the shared bottom-up loop, and read the claimant's code
  only *after* its own numbers were fixed.
- **Measured performance across this slice:** e13 — 5 errors caught before
  publication, 5 produced by the referee itself, all caught by other lanes.
  e14 — AUDIT2's final ledger: 10 catches / 10 self-errors / 10 withdrawn, seven
  of the ten caught by lanes; the referee's own worst call (`U1` promoted to "the
  strongest wall in the corpus") **fails in 660 circuits that were already on
  disk when the sentence was written**. e15 — a cross-desk audit returned
  **FAIL** on 2026-08-29 against a document whose figures all reproduced, because
  three figures had been carried from partial-run running totals rather than
  re-derived; all three were corrected in place and the document then passed.
  e17 — three VERDICT.md files, each with confirmed *and* refuted rows (e.g.
  laneCONTRA's `n=88` numeral 8,562 corrected to **7,362**, an error that ran
  *against* the claimant and made the asymmetry stronger).
- **Code:** `e17_pure/REF_*/code/`, `e15_campaign3/audit3_tools.py`,
  `e14_plateau87/audit_tools.py`, `e14_plateau87/selfaudit.py`.
- **Logs/results:** `e13_hand87/cluster_campaign/AUDIT.md`,
  `e14_plateau87/AUDIT.md` (212K), `e15_campaign3/AUDIT.md` (223K) +
  `AUDIT_FINAL.md` (29K), `e17_pure/REF_*/VERDICT.md`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2 verdict:** **keeper — arguably the most valuable transferable asset
  in the whole tree.** The recurring named failure modes (RELAY, SELF-EXCLUDING
  INSTRUMENT, FALSE CONFLICT, "a true statement carrying an unearned
  conclusion") are a ready-made checklist.

---

## 3. ARTIFACTS (counts + labels)

All commands run from `/home/joebachir20/xor_ui/slp-plateau-search/`.

### 3.1 Verified MixColumns circuits (full 32×32 instance)

Heuristic scan of every `.json` under the slice that parses as a gate list of
30–300 gates (`python3` walk, one-off; script not banked):

| gate count | files | where |
|---|---|---|
| **88** | **28** | e13 (8), e14 (16), e15 (3), e17 (1) |
| 89 | 7 | e13 (2), e15 (5 — planted controls) |
| 90 | 3 | e13 (2), e15 (1) |
| 91 | 5 | e13 (4), e17 (1) |
| 92 | 3 | e13 (2), e17 (1) |
| 95–108 | ~23 | e13 laneFRESH ladder, e14 `basis/` (105 ×3, 108) |
| 109–215 | ~11 | e13 (113/114/121), e14 `jordan_140`, e17 tables |

Caveat: a handful of the e17 and e10/e11 rows are result tables, not circuits;
the e13/e14/e15 rows are all genuine circuit files. **Total circuit-like JSON in
the slice: 86.** I oracle-verified two by hand
(`python3 verify_circuit.py <file>`):
`experiments/e13_hand87/cluster_campaign/assembly_stage5.json` → `gates=88
depth=5 outputs_built=32/32 problems=0 — VALID`, and
`experiments/e14_plateau87/laneFS88_chimA_record_x_sig2.json` → same, **VALID**.

Named, distinctive circuit artifacts worth quoting publicly:
- `e13_hand87/cluster_campaign/assembly_stage{0,1,3,4,5}.json` — the
  **106 → 97 → 91 → 90 → 88 reasoning ladder**, every rung oracle-VALID; stage5
  is gate-for-gate the record.
- `e13_hand87/laneT/T_mixcolumns_88gates_depth{5,5fs,6,7,8}.json` — **five
  88-gate circuits for `M^T`** (new artifacts, VALID against the `M^T` oracle).
- `e14_plateau87/laneFS88_chim{A,E}*.json` — VALID 88s outside their parents'
  closed components (new **circuits**, not new **designs**).
- `e14_plateau87/basis/zframe_105.json` (VALID 105, best single-frame algebraic
  derivation) and `basis/jordan_140.json` (VALID 140).
- `e13_hand87/laneFRESH/*.json` — 15 VALID circuits spanning **95 to 121** gates,
  the from-scratch/peephole/plateau-walk ladder.

### 3.2 Tripwires and their (empty) alarm files

- **`find experiments/e1[0-7]* -name 'ALARM*' -o -name 'STOP' | wc -l` → `0`.**
  No alarm was ever written anywhere in this slice.
- `e16_lastwish/laneFPOINT/bank/F{1..8}.alarms.jsonl` — **eight files, all
  0 bytes** (`ls -la`), the T1/T2/T3 tripwire outputs.
- `e17_pure/laneDELTA/lemmaR_hits_corpus.json` — 2 bytes (`[]`), the Lemma-R
  tripwire on 1,200 valid 88s; `T2_viol_corpus.json` — 2 bytes.
- `e17_pure/laneDELTA/lemmaR_hits_nonsample.json` — 15,850 bytes, **66 hits on
  26 non-88 circuits** (these *are* compressions, and five were oracled).

### 3.3 Exhaustive / bound certificates (what each certifies)

| certificate | certifies | where | command |
|---|---|---|---|
| Run A bank, 17,283 rows | every distinct 88 mask-multiset on disk has **no compressible window in the `d(S)>=2` free-helper regime**, and `B = 56` | `e15_campaign3/sweep_A_fullpop.jsonl` | `wc -l` → 17283 |
| d3 anchor bank, 13 rows | 13 anchors × 27,720 triples = **360,360 triples enumerated, 0 compressible**, with a declared aimed-helper sub-gap | `e15_campaign3/sweep_D3_anchors.jsonl` | `wc -l` → 13 |
| Tier-B bank, 32 rows | **15,099,957 `d(S)=1` windows**, `d1.closed` true on 27 / false on 5, 0 compressible, 0 shared helpers | `e15_campaign3/sweep_ledger.jsonl` | `wc -l` → 32 |
| Eight closed F-point components | **333,396 states, all CLOSED by exhaustion, min gate count 88 at every one** | `e16_lastwish/laneFPOINT/bank/F*.states.bin` + `RESULT_F*.json` | `python3 -c "sum(getsize(f)//(8*88))"` → 333396 |
| Five e14 orbits | 44,793 states, five pairwise-distinct closed components, zero free 87s | `e14_plateau87/RESULT.md` item 1; reproduced in `laneFPOINT/CONTROL_partAB.log` | — |
| Corpus `G<=3` decision | **55,970 sites over 18,355 circuits, 0 with `G <= 3`** | `e16_lastwish/lane536/corpus_le3.jsonl` | `wc -l` → 18355 |
| k=2 (3-orphan) closure | **1,409 / 1,409 sites decided `G > 4`** — the 2-mint/3-orphan regime CLOSED on this corpus | `lane536/le4_k2.jsonl`, `le4_undecided_s*.jsonl` | — |
| `12 <= cost <= 13` for both dim-10 quads | k = 8,9,10,11 exhaustively refuted; 13-gate cf programs constructive | `e11_quad10/k11_q{24,16}.log`, `found/quad_*_cf13.json` | — |
| 54 cross-family subset decisions | `cost = cost_cf`, gap exactly 0 | `e10_crossfam/found/` (54 JSON) | `ls e10_crossfam/found \| wc -l` → 54 |
| 43 certified small optima | `k*` UNSAT-certified, witnesses replayed | `e12_legibility/data/*.witnesses.json` | `ls \| wc -l` → 43 |
| 99 certified-optimal forcedness instances | zero irredundant programs at `L*−1` with budget intact | `e16_lastwish/laneFORCED/rows.jsonl` (91) + `n7.jsonl` (8) | `wc -l` |
| `B = 91.4098776` price table | Check-1-feasible, exactly tight; `ceil(B) = 92` ⟹ `L_cf(M) >= 92` | table lives at `fleet7/laneUNCOND/...`; rebuild + verdict in `e17_pure/REF_CONTRA/VERDICT.md` V14 | — |

### 3.4 Writeups / reports

`find <slice> -name 'RESULT*.md' -o -name 'BRIEF*.md' ...` → **13 RESULT.md**
(e10, e11, e12, e13×4, e14, e15, e16×3, e17 lanes ×4 — plus 8 `RESULT_F*.json`),
**3 referee VERDICT.md**, **1 DOSSIER.md (92K)**, **6 BRIEF/PLAN files**,
**5 AUDIT files** (e13, e14 212K, e15 223K, e15 AUDIT_FINAL 29K),
**16 LEDGER files**. Total markdown in the slice: **69 files**.

### 3.5 Ledgers / append-only result files

`find ... \( -name 'LEDGER*.md' -o -name 'ledger.jsonl' \) -printf '%s\t%p\n'`:

| ledger | size | rows |
|---|---|---|
| `e10_crossfam/ledger.jsonl` | 181K | 201 |
| `e11_quad10/ledger.jsonl` | 61K | 110 |
| `e12_legibility/ledger.jsonl` | 67K | 65 |
| `e13_hand87/cluster_campaign/LEDGER.md` | 73K | — |
| `e14_plateau87/LEDGER.md` | 34K | — |
| `e15_campaign3/LEDGER.md` | **259K** | R0–R90 |
| `e16_lastwish/{lane536,laneFORCED,laneFPOINT}/LEDGER.md` | 16K/9K/14K | — |
| `e17_pure/{6 lanes+refs}/LEDGER.md` | 9K–22K each | — |

Append-only JSONL banks: **53 files, 46 MB** across the slice (e11 20.0M, e15
19.6M, e16 6.3M, rest <0.5M).

### 3.6 Raw logs

**118 files (`*.log`, `*.out`, `*.nohup`), 2.2 MB total.** Per slice:
e10 17, e11 23 (2.0M — dominated by `shardcontrol*.log`), e12 11, e13 5, e14 4,
e15 31, e16 18, e17 9. Command:
`find <dir> \( -name '*.log' -o -name '*.out' -o -name '*.nohup' \) -type f -printf '%s\n' | awk '{t+=$1}END{print t}'`.

---

## 4. KEEP / DELETE proposal

**Default posture: KEEP.** This slice is 302 MB total; the only item above 20 MB
is one state bank. Nothing here is worth risking.

### KEEP — unconditionally
- **Every `RESULT.md`, `AUDIT*.md`, `LEDGER*.md`, `VERDICT.md`, `BRIEF*.md`,
  `NOTES.md`, `PREREG.md`, `DOSSIER.md`, and every lane `.md`.** These are the
  campaign record and the source of every number in the public repos.
- **Every `.jsonl` ledger/bank** (46 MB). `sweep_A_fullpop.jsonl`,
  `sweep_D3_anchors.jsonl`, `sweep_ledger.jsonl`, `corpus_le3.jsonl`,
  `le4_k2.jsonl`, `sites_536.jsonl`, `rows.jsonl`, `ledger.jsonl` ×3 — these are
  the *authority* for every published count and the campaigns explicitly re-derive
  from them rather than from prose.
- **Every `.py`/`.c` and every compiled binary** (`qsearch`, `qsearch_shard2`,
  `forced`). Small, and the method catalog above is worthless without them.
- **Every circuit `.json`** (86 files). Irreplaceable without re-running search.
- **All 118 log files (2.2 MB).** Several carry calibration lines that exist
  nowhere else (e.g. `logs_D3_anchors.log`'s two planted-89 control readings,
  which are what license the d3 zero).
- **`e11_quad10/shards/q0_7_8_24_k12.jsonl`** — 276 closed k=12 cubes, explicitly
  **resumable to the cube**. Deleting it throws away 0.60 CPU-hours *and* the
  resume point of the slice's one open exhaustive level.
- **`e15_campaign3/sample500.txt`** — the drawn-but-never-swept run C sample.
  It is the work list for a purchase that was approved and never made.
- **Superseded files kept deliberately in place and named as such**
  (`MECHANISM_LIBRARY_v1.2_superseded.md`, `RESULT_DRAFT.md`,
  `sweep_A_fullpop_ABORTED_sortedorder.jsonl`,
  `sweep_ledger_round0_slowcode.jsonl`, `launch_*.sh.SUPERSEDED`,
  `code/matched10.py` "the **misdesigned** first control, kept for the record",
  `lemmaR_sweep.py`). The campaigns' own discipline is *"original figure struck,
  never silently overwritten"* — deleting these breaks that.

### DELETE-CANDIDATE (safe, small)
- **18 `__pycache__` directories — 548 KB.** Pure build artifact.
  `find experiments/e1[0-7]* -name '__pycache__' -type d`. **Reclaims 0.5 MB.**
- **`e15_campaign3/RUN_B.log`** (143 bytes) — a mis-launched command; its entire
  content is `python3: can't open file '.../e15_campaign3/fprun.py': [Errno 2]
  No such file or directory` (`fprun.py` belongs to e16's laneFPOINT). Harmless
  either way; flagging it only because it looks like a missing artifact and is
  not. **KEEP is also fine.**
- **`e15_campaign3/.start.lock` (0 bytes) and `.slot_guard_restarts` (22 bytes)**
  — stale run-control state from a finished run. Trivial size; delete only if
  tidying, and note the guard's own log records why the restart budget was spent.

### DELETE-CANDIDATE (large, but **I recommend KEEP**)
- **`e16_lastwish/laneFPOINT/bank/F*.states.bin` — 224 MB, 74% of this whole
  slice.** These are the 333,396 enumerated 88-gate states, 8 bytes per gate.
  *Argument for deletion:* they are regenerable — the engine is banked
  (`fpclose.py`), the run took only 2,336 s wall, and every derived number is
  already in `RESULT.md` and `RESULT_F1..F8.json`.
  *Argument for keeping (mine):* the bank **is** the certificate. CONTROL 5
  (`bankcheck.py`) sampled 96 states out of it and oracled them 96/96 VALID; the
  on-disk sizes are the reported counts (I re-derived 333,396 from the file sizes
  alone). It is also the object e16's own SG2 names as the input to a
  corpus-wide orbit census. **Proposal: KEEP; if disk pressure demands, compress
  (`zstd -19`, likely 5–10×) rather than delete, and never delete
  `F*.progress.jsonl` / `RESULT_F*.json` / the empty `alarms.jsonl` files, which
  are tiny.** Reclaimable by deletion: **224 MB**; by compression: ~180–200 MB.
- **`e11_quad10/shards/ctl10_cf12_31_107_617_920_k11.jsonl` — 17 MB.** A control
  instance's per-cube record. Regenerable but it is append-only ledger data and
  the control it belongs to is the one that *fired* (it produced the dim-10 gap).
  **KEEP.**
- **`e15_campaign3/tools/pop88.pkl` — 10 MB.** A cache of the parsed 88
  population. Genuinely regenerable from the corpus in minutes.
  **DELETE-CANDIDATE, reclaims 10 MB** — but only once someone confirms nothing
  in `tools/` loads it lazily at import; `cache_pop.py` writes it.
- **`e15_campaign3/popfull_shuffled.txt`, `popshard_0{0,1}.txt`,
  `popshuf_0{0,1}.txt`, `popshuf_01_remaining.txt`, `popshuf_00_remaining.txt`
  — 6.4 MB of derived work lists**, all regenerable from `popfull.txt` (2.1 MB,
  KEEP — it is the denominator of the headline count and the partition check).
  **DELETE-CANDIDATE, reclaims ~6.4 MB.** Caveat: `RESULT.md` cites
  `popshuf_00.txt` (8,639) and `popshuf_01.txt` (8,644) as the disjointness/sum
  check, so keeping those two is cheap honesty. Recommend deleting only
  `popfull_shuffled.txt`, `popshard_*` and `*_remaining.txt` (~4.3 MB).

**Total safely reclaimable without touching evidence: ~15 MB** (pycache + pkl +
derived work lists). The only large win is the 224 MB state bank, and I recommend
compressing rather than deleting it.

---

## 5. LEADS (sharp-eye findings)

Confidence labels: **VERIFIED-IN-LOG** / **PLAUSIBLE** / **SMELL**.

**L1 — `G_int(3) >= 92` has never been re-verified, and it is the only inherited
numeral that currently changes a conclusion. VERIFIED-IN-LOG.**
`e17_pure/DOSSIER.md` §7.2 and §9.5: the value is *"a solver's best objective
bound"*, bracket `[92, 94]`, never re-certified. If it holds, `kappa >= 3` and
`|A*| >= 3` for every 87. The dossier calls re-certifying it *as an infeasibility
at `obj <= 91`* — **one CP-SAT run** — *"the highest value-per-hour item on the
board."* Everything that dies if `G_int(3) <= 91`: `kappa >= 3` at `n <= 87`,
`|A*| >= 3`, and the §6.2 conditional chain. Companion item: `G_int(2) = 64` has
**two failed independent reproduction attempts against one log** (§7.1) —
that is a SMELL on an inherited constant that laneY's headline recommendation
depends on exactly.

**L2 — e15's "run C" was approved, its sample was drawn and banked, and it never
ran. VERIFIED-IN-LOG.** `RESULT.md` §Coverage-map correction: *"RUN C WAS
APPROVED, ITS SAMPLE WAS DRAWN AND BANKED (`sample500.txt`, 500 rows), AND IT
NEVER RAN. There is no `sweep_C_sample.jsonl` anywhere in the repository."* It
was a stratified 500-circuit `d(S)=1` sample at a 200,000-window cap. This is the
cheapest slice of the 1,200-CPU-hour `d(S)=1` population gap, the work list is on
disk, and the instrument is complete and twice-validated. **A ready-to-run
purchase.**

**L3 — the `t = h1 ^ h2` both-helpers-new sub-gap: inherited verbatim from e13,
declared by e15, closed by nobody. VERIFIED-IN-LOG.** Every d3 row carries
`aimed_helper_only: true`. *"A d3 zero means 'no compressible window found by the
aimed-helper search on this enumeration'. It does NOT mean 'none exists'."* The
13 anchors are ENUMERATED-WITH-A-DECLARED-SUB-GAP, never CLOSED. This is a
genuine hole in the strongest local negative the project owns, and e15 lists
building the complete instrument as its lead #2.

**L4 — `Q(V*, 87)` was NOT REACHED and was NOT answered negatively.
VERIFIED-IN-LOG.** "Is there an 87 using only masks some known 88 already uses?"
`V*` = 1,393 masks; no encoder reaches above ~100–134. The instrument ceiling was
*measured* (11× budget bought +11% rounds while seconds grew 11.2×), so it is a
ceiling, not a curve. e15 calls it *"the sharpest unanswered question the
campaign owns"* and explicitly says the fix is a different instrument.

**L5 — e11's k = 12: one open level, priced, and 0.81% already banked and
resumable. VERIFIED-IN-LOG.** `12 <= cost <= 13` for both dim-10 quads; k = 12
is the *only* remaining level for either. **~1.92e11 nodes ≈ 38 CPU-hours per
quad**, "roughly one overnight run on four cores"; 276 of 34,080 root cubes
already closed in `shards/q0_7_8_24_k12.jsonl`, resumable with `--tag`. The
matched control now fires at dim 10 (§L6), so the answer would mean something.
Note the counter-evidence: 750 directed plants produced **0** instances with
`cost <= 12` and `cost_cf >= 13`, which is the best current reason to expect the
answer is 13.

**L6 — the one verified strict cancellation gap at dim 10, and the stratum
nobody sampled. VERIFIED-IN-LOG.** `e11_quad10/found/gap_dim10_n4_w5_31_283_465_809.json`
— an 11-gate program with 2 cancelling gates against `cost_cf = 12`. But the
*real quads have `cost_cf = 13`*, the highest well-populated dim-10 stratum
(17.5%), and **e11 has zero instances there**, because a cf=13 control costs the
same 38 CPU-hours as the real question. The help-rate rises with `cost_cf` within
a dimension (dim 8: 0/1 at cf=8 → 8/16 at cf=10 → 3/8 at cf=11). *"At dim 10,
'measure the control first' cannot be satisfied more cheaply than answering the
question."* An honest structural limit worth stating publicly.

**L7 — the `{4,7}` profile: 63 of 475 admissible pairs, "the branch nothing has
pressure on." VERIFIED-IN-LOG.** `DOSSIER.md` §4.5 branch 3 and §9.5: if an 87
exists with `|A*| = 2` it has **exactly two cancelling gates and eighty-five
clean ones** — *"nothing like any of the eleven wired circuits on disk
(`kappa = 9..28`)"* — and one of the twelve weight-7 MixColumns rows is produced
by a cancelling gate. **This is a concrete, never-searched target region for an
adversarial search.** It is the sharpest positive lead in the whole slice.

**L8 — A11's `n = 88` branch was never recounted under the banked table.
VERIFIED-IN-LOG.** `DOSSIER.md` §4.6 caveat 1: the numerals 7,362 / 19,490 are
computed under `pbar`, not the banked table; *"a successor restating A11 should
re-run the `n = 88` branch under the banked table."* Cheap (seconds), and A11 is
the first gate-count-asymmetric fact in the programme, so its numbers should be
airtight before anyone publishes it.

**L9 — A10 is table-contingent and holds on only 5 of 8 feasible tables.
VERIFIED-IN-LOG.** `DOSSIER.md` §4.6 caveat 2, a caveat the lane itself does not
state. Including one table with a *strictly larger* `B` than a table it fails on.
Under the banked table the margin roughly doubles (`+0.3582982` vs `+0.1781170`),
so it is not on a knife edge — but **anyone who re-optimises the price table must
re-run this check.**

**L10 — "is there a feasible Check-1 table with `delta_2 > 0`?" — an LP question
nobody has asked. VERIFIED-IN-LOG.** `DOSSIER.md` §9.5. `delta_2 = 0` (a weight-2
cancelling leaf buys nothing) is a statement about a *tight Check-1 column*, i.e.
about the certificate rather than about `M`. Cheap, and it would change a
conjunct of the Anatomy Theorem.

**L11 — the wiring-randomised null: named, cheap, unrun, and it is the one
genuinely unexplained observation left. VERIFIED-IN-LOG.** `DOSSIER.md` §9.2 +
`REF_DELTA/VERDICT.md` F5. The surviving-side zero (54,561 masks) is not
circular; it is weak and confounded, currently `p ≈ 0.015–0.25`. Every null run
for it is confounded *in the same direction* because a "site" is a property of
the wiring and the corpus's wirings are not sampled (`_closure_core` fixes every
parent by one deterministic rule). **The experiment:** hold each corpus 88's mask
set fixed, re-wire it many ways — `fleet1/laneC_proofside/code/rewire.py` already
does this — and measure the surviving-side rate across wirings of the same
circuit. *"It is cheap. It is the null this quantity has always needed. Nobody
has run it."*

**L12 — the instance-shrinking question for T2: the sharpest open structural
question, and laneDELTA's obituary for the whole direction is NOT established.
VERIFIED-IN-LOG.** `DOSSIER.md` §9.1 / `REF_DELTA` §6. The right criterion for
whether a local-optimality theorem aggregates into a lower bound is not "how rare
is the coincidence" but **"does the local theorem license a step that SHRINKS the
instance?"** Lemma F has one (that is why the refereed 55/56 bound exists);
Lemma R and T2 do not. The referee explicitly rules that laneDELTA's §8 ("the
whole local-optimality direction is closed; this file is its obituary") is **not
established** — the restriction-and-recurse sub-direction is live.

**L13 — Lemma OP / Sub-lemma CONF: "the honest name of the wall."
VERIFIED-IN-LOG.** `DOSSIER.md` §9.5. laneTOOL2's Theorem T4 is the only
relaxation exact on all nine circuits tested; its unconditional form (Lemma OP)
would refute `H87` outright. The gap is **64 → 88, twenty-four gates**, and the
named obstruction is that cancelling-gate operand masks are not confined to `U`,
so the optimisation is not even finitely posed. **Sub-lemma CONF** (confinement
to an explicit finite universe `V ⊇ U`) is the concrete first step, and *"nobody
has a candidate `V`."*

**L14 — the Lemma-R tripwire covered only 6.5% of the corpus; the full run is
~80 CPU-minutes. VERIFIED-IN-LOG.** `laneDELTA/RESULT.md` §8b sub-gap 1: ran on
1,200 + 600 of 18,355 corpus 88s (two non-nested samples). The private-operand
population it scans is *strictly larger* than lane536's site frame, so the
corpus-wide version is genuinely new coverage, not a repeat. **One CPU-hour of
free, always-on 87 detection nobody bought.**

**L15 — there is a live T2 violation on disk, at n = 89. VERIFIED-IN-LOG.**
`laneDELTA/T2_non.log`: `T2 VIOLATIONS: 1`, file
`campaign_87/agents/frontier-d6sat/found/p1_002f1a7337e999c916e670db_r4_plus1_89gates_depth6.json`,
gate 80, `D = [32,67]`, `d = 2`, `r = 3`. Expected (T2 must fail on non-optimal
circuits) but it was never followed up: T2 on non-88s covered `n <= 91` only, and
the larger circuits were skipped after a first run was killed (LEDGER L14).
**PLAUSIBLE lead:** the same scan over the whole non-88 population may surface
more compressible circuits.

**L16 — 66 Lemma-R hits on 26 non-88 circuits means the on-disk corpus contains
reducible circuits, and five were already compressed. VERIFIED-IN-LOG.**
`witness_nonsample.log`: 89→88 VALID ×3, 90→88 VALID, 90→89 VALID. Most hits sit
in `campaign_87/wave5_2026-08-04/burn/mutant_cluster/quarantine_misplaced/`.
**Consequence for goal 3 of this wrap-up:** any public statement of the form "N
verified circuits at k gates" should note that some non-88 files on disk are
*not* irreducible, and the exact count of genuinely-irreducible non-88s has never
been computed. Cheap to fix with the same tripwire.

**L17 — F3 and F7 are permanently bracketed at `d(S)=1`. VERIFIED-IN-LOG.**
`RESULT.md` Stage 1(a): F3 reached **10 of 88 bases** with 3,000,000 windows
(full space ~2.7e7), F7 reached **41 of 88**. *"UNCLOSABLE at any budget this
campaign was going to have."* These are the only two of the thirteen anchors with
an open `d(S)=1` regime, and both are extreme-depth circuits (10 and 11). The
cost model is explicitly a *description*, not a predictor — depth was ruled out
twice as the driver (F1 at depth 7 has 563,008 windows vs 58,872 and 99,923 for
two population depth-7 circuits, a 6–9× spread at identical depth).
**SMELL: nobody explained what actually drives `d(S)=1` cost.** That unexplained
6–9× spread at fixed depth is a structural signal about the plateau that was
measured and dropped.

**L18 — the shared-helper falsification is a live hole, not a closed one.
VERIFIED-IN-LOG.** e13 closed the `d(S)>=3` regime by *argument*, whose
load-bearing clause was "no mask finishes more than one window; all helpers are
distinct". Run A found **six circuits with shared helpers** (four with 1, two
with 3), and **the same mask `0x2818302` recurs across three unrelated
circuits** — so this is a repeating population feature, not an artifact. None of
the six compresses, but **`d(S)>=3` on the population is not closed**, and the
recurring mask is an unexplained structural coincidence nobody decoded.

**L19 — SG1: the count-increasing excursion is the real ceiling on all thirteen
orbit closures. VERIFIED-IN-LOG.** `laneFPOINT/RESULT.md` §6: both free moves
preserve gate count, so *"an 87 reachable only by passing through an 89 is
outside this object entirely."* 378,189 states of evidence say nothing about it.
The natural next object is the component under a move set admitting a temporary
89 (mint two, orphan three) — which lane536 decided **only at single sites**, not
as a connected move set. **This is the largest structural gap in the search side
of the slice.**

**L20 — e16_lastwish has no campaign-level RESULT.md. VERIFIED-IN-LOG.** It has
`BRIEF.md` and three excellent lane RESULT.md files, but nothing integrates them,
and e15's own RESULT explicitly notes the absence. Three headline results (the
536 dissolution, 333,396 F-point states, the forcedness refutation) currently
have no single citable document. **Cheap and high-value for the public repo
pages.**

**L21 — the 3-smooth structure of the orbit sizes, noticed and undecoded.
PLAUSIBLE.** `laneFPOINT/RESULT.md` §5: F7 243 = 3^5, F3 729 = 3^6, F4 2187 =
3^7, F2 19683 = 3^9, F5 2916 = 2²·3^6, F6 17496 = 2³·3^7, F1 91368 = 2³·3^5·47,
F8 198774 = 2·3^5·409, alongside e14's 10935 = 3^7·5 and 4212 = 2²·3^4·13.
Independent re-association sites contribute three states apiece; the pure powers
of three are components that are exactly a product of independent sites. *"The
residues 47, 409, 13, 5 are where the sites interact, and nobody has decoded
them."* Also: **re-parenting is inert on half the components** (F2, F3, F4, F7
and e14's record@d5 admit zero legal re-parentings anywhere), while F8 is
dominated by them (412,128 probes, 17× all others combined). A structural
dichotomy in the plateau that was recorded as "not load-bearing" and dropped.

**L22 — the `le4` fast path is under-attacked by its own author's grading.
VERIFIED-IN-LOG.** `lane536/RESULT.md` sub-gap 4: `slp3.py`'s completeness
survived 8,000 random-topology plantings; `le4`'s fast path has only 428 planted
instances, of which just 28 came from a random topology. So **1,309 of the 1,409
k=2 negatives rest more on the argument than on adversarial testing.** Closing it
by brute force costs ~11 CPU-hours. The 2-mint/3-orphan closure is one of the
campaign's headline claims, so this is the weakest load-bearing joint in it.

**L23 — e12's dim-12 orbits banked partial bounds from timeouts that nobody
used. VERIFIED-IN-LOG.** `e12_legibility/RESULT.md` ground-truth table:
`mc_orbit12` (ρ-orbits 1, 3, 4) — all UNDECIDED, but **proven `>= 12` with greedy
at 16**, i.e. three live brackets `[12,16]` on dim-12 sub-instances. Similarly
e10's dim-9 `n = 4` cell is a **lower bound only** (`>= 1/5`, 4 of 5 samples
unresolved at a 90 s cap). A timeout is a bracket; these three brackets are the
only dim-12 information the slice holds and no successor picked them up.

**L24 — e10's own "what I would do next" item 2 was never done, and e11 did item
1 instead. PLAUSIBLE.** `e10_crossfam/RESULT.md` §7 item 2: *change the object
being priced* — for a cancelling gate `g` of a verified 88 serving rows `R`, let
`W` be the masks available just before `g` and ask for the exact minimum cost of
`R` **from `W`**, with and without cancellation. §1(b) is the reason: every
cancelling gate lives in a cone at least 2 gates *above* the standalone optimum,
so *"the cancellation is not a local saving; it is the repair bill for reusing a
wire built for other outputs"* — the payoff is realised in the complement of the
cone, precisely where subset pricing cannot see. The implementation cost was
stated as **one new flag on `qsearch` (`--avail`)**. It is *"the first
formulation in which cancellation can show a gain"* and nobody built it.

*(Bonus observation, filed here because it is the closest thing in the slice to
an explanation of why 88 keeps appearing: e15's composition identity. `88 = 32
finals + 56 middles` is forced; every decoded mechanism moves a gate between the
currency and helper piles; every measured cross-frame exchange is 1:1 as a
**consequence, not a coincidence** — any two 88s are joined by substitutions that
must net zero because both endpoints cost 88. So **"a composition of
wash-mechanisms is a wash"**, reached independently by two lanes. Combined with
e16's forcedness result — that a true optimum of this size would be expected to
have hundreds of structurally distinct realisations — the plateau's width stops
being evidence of looseness. That pairing is, in my reading, the strongest
"why 88" story the slice contains, and it is currently split across two
campaigns' documents with nothing joining them.)*

---

## 6. HAZARDS

1. **Nothing in this slice is live.** I checked `ps -eo pid,etime,stat,args`:
   the only running processes on the box are `fleet11/laneCUBE`'s
   `python3 -u code/mono.py 14` (×4) and
   `python3 -u code/cube16.py --k 14 --cores 16 --group 33 ...` (×17), plus two
   `fleet12/laneHALO` `generate.py` runs. **No process has a cwd or argument
   under `experiments/`.** e15's last process exited 2026-08-29 04:12.
2. **`e15_campaign3/.start.lock` and `.slot_guard_restarts`** are run-control
   state read by `tools/slot_guard.sh` and `tools/resume_all.sh`. If anyone ever
   resumes e15, these must be present or absent deliberately. Harmless now.
3. **Hardcoded absolute paths.** Reorganisation will break things:
   `e13_hand87/laneFRESH/RESULT.md` and every lane's Law-1 procedure invoke
   `python3 /home/joebachir20/xor_ui/slp-plateau-search/verify_circuit.py`;
   `e17_pure/DOSSIER.md` declares *"Repository root for every path in this
   document is `/home/joebachir20/xor_ui/slp-plateau-search/`"*;
   `e17_pure/laneDELTA/lemmaR_hits_nonsample.json` and `nat_hits.json` record
   absolute paths into `campaign_87/` and `experiments/e3a_exploit/`.
   **The dossier and the laneDELTA hit files reference files OUTSIDE this slice**
   — `fleet7/laneUNCOND/results/bstar/nostop_lp_cert_4_1.json` (the banked price
   table, explicitly "use this, not `pbar`"),
   `fleet2/laneP_proof/RESULT.md`, `fleet1/laneC_proofside/code/rewire.py`,
   `fleet6/laneTOOL2/RESULT.md`, `beat88/understanding/CANON.md`,
   `atlas/thinktank/lower_bound.md`, `atlas/thinktank/referee_55.md`,
   `fleet7/laneCONSOLIDATE/STATE_OF_THE_PROBLEM.md`. **Deleting or moving any of
   those breaks the dossier's citation chain.**
4. **`e15_campaign3/tools/sweep.py` is the code that the B=56 tripwire lives in,
   and `e13_hand87/laneCUT/adopt.py` is the code e15's audit re-ran to produce
   the two errata.** Both are load-bearing for published numbers; neither should
   be edited in place.
5. **`e16_lastwish/laneFPOINT/bank/F*.alarms.jsonl` are 0-byte files that are
   evidence.** A tidy-up pass that deletes empty files would destroy the
   artifact that certifies the tripwires fired zero times.
6. **`e15_campaign3/popfull.txt` is the denominator** of the 17,283 headline and
   the partition check in `RESULT.md`. Do not delete it with the other work
   lists.

---

## 7. GAPS

1. **Gate counts in §3.1 are from a heuristic JSON scan**, not from the oracle.
   I verified only two circuits by hand (both VALID) per the CPU budget. A
   definitive by-gate-count census would need `verify_circuit.py` on all 86
   files — a few minutes of CPU, but the brief forbids bulk re-verification.
   Some e17/e10/e11 rows in that table are certainly result tables misread as
   gate lists; the e13/e14/e15 rows are reliable.
2. **I did not read `e15_campaign3/AUDIT.md` (223K), `LEDGER.md` (259K),
   `laneCOMPOSE.md` (97K), `laneDECODE.md` (46K), `e14_plateau87/AUDIT.md`
   (212K), or `laneFS88.md` (80K) in full** — only the sections `RESULT.md`
   points at. There may be further dropped anomalies inside them. Budget.
3. **CPU costs are recoverable only where a log printed them.** I have exact
   figures for run A (77,860 s per shard), d3 (19,845.6 s), laneFPOINT (2,336 s),
   the lane536 corpus run (1,686 s), laneDELTA's four scans (71/173/281/189 s),
   e11's k=11 levels (2,726 / 2,669 CPU-s). For e10, e12, e13 and e14 the logs
   record per-run times but no campaign total, so I have not given one.
4. **I could not determine whether `e15_campaign3/tools/pop88.pkl` is still
   imported by anything.** `cache_pop.py` writes it; I did not trace every reader,
   so my delete recommendation for it is conditional.
5. **`e16_lastwish` has no campaign-level RESULT.md**, so its cross-lane
   integration (what the three lanes jointly establish) exists nowhere and I have
   had to assemble it from three lane files. Anything a missing integration
   document would have caught — a contradiction between lanes — I would not have
   seen.
6. **The `.states.bin` banks were not parsed**, only sized. I confirmed the
   reported state counts arithmetically (size ÷ (8 bytes × 88 gates) reproduces
   333,396 exactly), which is strong but is not the same as reading them.
7. **I did not check whether e10's and e11's `found/` witnesses re-verify.**
   Both campaigns claim fresh-subprocess verification (55 VALID / 0 INVALID and
   2 VALID / 0 INVALID respectively) and I took those at face value.
