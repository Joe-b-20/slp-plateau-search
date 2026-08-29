# Slice report: experiments_early

Agent model: Opus 5 (1M context). Date: 2026-08-29.

**Summary.** This slice is the 2026-08-18 five-agent experiment campaign (E1–E9, run
under `_shared/BRIEF.md`) plus three small solo probes from 2026-08-21/22
(`e_oddlane3`, `e_upstream`, `e_w2novel`) and the 2026-08-28 SAT-competition
benchmark package (`sat_package`). It is 77 MB, 6,563 files, 10 `RESULT.md`
write-ups, 10 append-only ledgers totalling 83,252 rows / 19 MB, and ~238
circuit-or-mask-set artifacts. It is the **best-documented part of the tree**: every
E-directory carries a re-tallied RESULT.md with explicit control status, and the
campaign's house rules (oracle-or-it-didn't-happen, every negative needs a fired
positive control, timeout ≠ refutation) are visibly enforced. The methodological
yield is high: I catalogue **31 distinct methods**, of which ~10 are strong phase-2
keepers and 3 are close to circuit-generic. The three biggest *unbanked* findings
are all "the run finished after the write-up and nobody re-tallied": E5's drop-4
local-optimality screen **completed on a second 88 family**, E7's dim-12 tap-region
queue **decided three more regions** (including Jean's foreign-lineage 88), and E3a's
buy-one-save-two sweep **completed empty at 4,926 instances**. A fourth lead is
`e_upstream`, which has no write-up at all and holds an **89-gate circuit carrying a
mask feature that is extinct in all 3.28 M known 88s** — i.e. a measured price of
exactly 1 gate for leaving the corpus vocabulary.

---

## 1. INVENTORY

Sizes: `du -sh <dir>`; file counts: `find <dir> -type f | wc -l`. Slice total
`du -shc e1_regions e2_outputcost e3a_exploit e3b_fresh e4_depth e5_readd e6_cancelplan e7_push e8_quad e9_radius e_oddlane3 e_upstream e_w2novel _shared sat_package` = **77 M**.

| dir | size | files | what it IS | documented? |
|---|---|---|---|---|
| `_shared` | 16 K | 1 | `BRIEF.md` — the campaign charter: problem statement, hard rules, the "already measured dead" list, target structure, reference circuits. The single most reusable document in the slice. | n/a (is the doc) |
| `e1_regions` | 1.2 M | 130 | Multi-instance search on **one** circuit in disjoint mask-space regions, with/without coordination. Coordinator + barrier + 3 message channels. | **RESULT.md** (796 lines) + generated `out/report.md` |
| `e2_outputcost` | 1.1 M | 79 | The output-subset **cost curve** `U(n)`: exact cost of every small subset of the 32 output rows, by SAT oracle + a cancellation-free MILP, reduced by an isomorphism argument. | **RESULT.md** (679 lines) |
| `e3a_exploit` | 25 M | 5,761 | "Exploit the known openings": plateau-cage measurement, exact sector-block re-optimisation at scale, buy-one-save-two, odd-parity sigma sector, k=3 shell, plan-space sizing. Largest ledger except E5. | **RESULT.md** (649 lines) + `TALLY.txt` |
| `e3b_fresh` | 884 K | 65 | Fresh-angle portfolio (13 arms declared up front, 5 run): FIXN fixed-size infeasible search, demand-flow (A,B) pricing, SYMGF automorphism proof, orbit-drop. | **RESULT.md** (367 lines) |
| `e4_depth` | 6.6 M | 73 | **The depth axis.** Disk-wide min-depth sweep of 38,711 distinct mask sets + exact depth-capped MaxSAT floors over mask alphabets. **Headline artifact: the refereed depth frontier 97@3 / 91@4 / 88@5.** | **RESULT.md** (366 lines) |
| `e5_readd` | 16 M | 88 | Exact minimum **re-add cost** of a dropped rho-orbit, by SAT + independent DFS + cube-and-conquer; then the complete drop-4 screen. Ledger is 72,805 rows / 16 M. | **RESULT.md** (279 lines) |
| `e6_cancelplan` | 484 K | 48 | The cancellation-plan CP-SAT instrument: per-child candidate sets, optional cancellation, the first non-vacuous decision that lane ever produced. | **RESULT.md** (548 lines) + `TALLY.txt` |
| `e7_push` | 780 K | 73 | Finishes three things E3a left in reach: resumable cube-level dim-12 region decisions, the convex-closure repair of the sector-0 block spec, the odd sigma half. | **RESULT.md** (429 lines) + `ATLAS_NOTE.md` + `TALLY.txt` |
| `e8_quad` | 372 K | 39 | A purpose-built C searcher (`qsearch.c`) that closed `cost(rho-orbit quad) = 12` exactly, ~4 orders of magnitude faster than the generic oracle. | **RESULT.md** (357 lines) |
| `e9_radius` | 1.1 M | 65 | The radius hypothesis tested with a firing control; CPU-second budgeting from `/proc`; chained shake-and-recover displacement operator. | **RESULT.md** (509 lines) |
| `e_oddlane3` | 84 K | 19 | Corpus-wide degeneracy census (3.28 M 88-gate circuits, 460 files, 3.9 GB streamed) + a radius-1 pin probe. | `NOTEBOOK.md` only — **no RESULT.md**, probe output unanalysed |
| `e_upstream` | 416 K | 53 | "Cultivate novelty upstream": pin an extinct mask feature into a 100–173-gate root and descend; read the **survival floor** = the feature's price. | `NOTEBOOK.md` only — **no RESULT.md**; 33 result artifacts never written up |
| `e_w2novel` | 16 K | 2 | 388 weight-2 masks that appear in **no** circuit of the corpus, + an unrun probe. | opaque (candidates + script, no notes) |
| `sat_package` | 24 M | 52 | Self-contained SAT-competition benchmark: `k14_joint_W3U4.cnf` (SAT ⟺ 87 gates), the k=9..13 UNSAT ladder, generator, decoder, verifier, demos. | **README.md** (405 lines) + `SUBMISSION_NOTES.md` |

**File-type breakdown (whole slice).** 147 `.py`, 25 `.sh`, 1 `.c`; 10 `ledger.jsonl`
(83,252 rows total, 19 M: `wc -l */ledger.jsonl`); 7 `.cnf` (22 M, all in
`sat_package`); ~5,900 small `.json` (5,705 of them are E3a solver instances); 11
`__pycache__` dirs (460 K).

**Opaque vs documented.** Everything E1–E9 is documented to an unusually high
standard. The three genuinely opaque spots are `e_w2novel` (no notes at all),
`e_oddlane3`'s `hunt.out` (a completed corpus scan whose result line was never
folded into any write-up), and `e_upstream`'s 33 `S<n>_*.json` floor files (no
write-up, and not in oracle format — see §5).

---

## 2. METHODS

31 entries. Grouped loosely; each is a distinct method or a named twist.

### exact-alphabet-floor-maxsat
- Family: exact-optimisation / SAT-MaxSAT
- What it does: fixes a finite alphabet `A` of candidate gate masks and a depth cap `L`, then asks RC2 core-guided MaxSAT for the **minimum** number of gates from `A` that builds all 32 outputs at depth ≤ `L`. The optimum is decoded, re-scheduled depth-optimally, and handed to the oracle in the same run.
- Twist vs siblings: it *minimises* instead of *deciding*. The returned optimum is its own oracle-verified positive control, so it structurally cannot produce a vacuous negative — unlike `d4decide.py`, its own sibling.
- Measured performance: floor = **91 at depth ≤ 4** over 5 independent vocabularies (91, 91, 92, 117, 155, 189, 195, **227** masks) and over the 300 most-frequent masks of the whole 15,912-circuit depth-4 population. 1.3 s at 227 masks; 23.4 s at 300; TIMEOUT/UNDECIDED at 400, 554, 600, 688. The decide form (`d4decide.py`) on the same 227-mask instance did not return in >500 s — a **≥400×** gap. (`e4_depth/RESULT.md` §3–4 and the verbatim `tally.py` appendix.)
- Cost: seconds to ~40 min per rung; 6 rungs logged `floor_timeout`.
- Code: `e4_depth/code/d4floor.py` (minimise), `e4_depth/code/d4decide.py` (decide, kept as the negative control), `e4_depth/code/harvest.py` (alphabet construction).
- Logs/results: `e4_depth/ledger.jsonl` (82 rows), `e4_depth/out/floor/` (13 witnesses, 56 K), `e4_depth/out/alph/` (22 alphabets, 208 K).
- Generality: **CIRCUIT-GENERIC** in form, MC-hardcoded in the target list only. Point it at another matrix by swapping the target masks and re-harvesting an alphabet from that matrix's own circuit population.
- Phase-2 verdict: **keeper, top tier.** "Minimise, never decide" is the single most transferable methodological result in this slice.

### mindepth-reschedule-sweep
- Family: structural-analysis / disk audit
- What it does: for a mask set, computes the minimum depth at which it can be scheduled (max of the `relax` level over the set) and compares it to the depth the file was written at. Run over the whole disk.
- Twist vs siblings: it is an audit, not a search — it asks whether stated depths are real or just un-optimised scheduling.
- Measured performance: **2 of 38,711 distinct mask sets reschedule shallower**, and one of those two is a genuine frontier point (`atlas/compiled_m1.json`, 5 → 4, a *third* independent 91@4 lineage). Maximum observed rescheduling gain across the whole sweep is exactly **1 level** — which is what licenses excluding the 1.16 M depth-≥7 88s from the frontier claim.
- Cost: enumerated 1,820,576 JSON files; two passes producing 6.2 M of JSONL.
- Code: `e4_depth/code/mindepth.py`, `e4_depth/code/analyze.py`
- Logs/results: `e4_depth/out/mindepth_scan.jsonl` (2.9 M, 17,518 circuits), `e4_depth/out/mindepth_scan_pass1.jsonl` (3.3 M, 22,636 circuits), `e4_depth/out/resched/` (2 circuits).
- Generality: **CIRCUIT-GENERIC** (pure DAG scheduling over mask sets).
- Phase-2 verdict: **keeper** as a one-shot audit run once per corpus. The well is dry here, but a new circuit's corpus should get the same audit on day one.

### depth-capped-restart-hunt
- Family: plateau-search
- What it does: repeatedly restarts the shipped `walk`+`lns` alternation under a hard depth cap from a fixed anchor, oracle-verifying every record.
- Twist vs siblings: depth cap + Pareto tie-break, and the instrument re-derives and verifies its own anchor on every restart so the control is per-run.
- Measured performance: **0 of 49 restarts** reached ≤ 90 gates at depth ≤ 4, 4.9 core-hours. Endpoints `{(91,4): 40, (92,4): 9}`. Note the trap: 0/9 restarts from the shipped 92@4 reached 91, though the project inventory records that step as a four-minute result.
- Cost: 17,649 s worker time, contended box.
- Code: `e4_depth/code/hunt.py`
- Logs/results: `e4_depth/ledger.jsonl` (49 `restart_end` rows), `e4_depth/logs/`.
- Generality: MC-HARDCODED (drives `pipeline/engines`).
- Phase-2 verdict: superseded-by-`exact-alphabet-floor-maxsat` for deciding a depth level; still fine as a cheap upper-bound producer.

### region-partitioned-concurrent-search
- Family: plateau-search / parallel coordination
- What it does: partitions **one** circuit's mask space into disjoint linear subspaces (rho-orbit plane sets), gives each worker a region, and serialises their edits through a revalidating coordinator barrier.
- Twist vs siblings: the region is a **mask-space predicate**, not a lookup table — required, because the repair step invents masks no table owns.
- Measured performance: **worse than one instance**, at every plateau anchor, by 1.4–2.6× in distinct states per core-second (`p_mw ≈ 0.002–0.005`). `par-indep` (N instances, no regions) matches solo within 2%, so the loss is caused by the regions, not by concurrency. It does buy one thing: write-conflict rate falls 76–78% → 31–35%.
- Cost: 23,325 worker core-seconds, 180 runs in the arm matrix.
- Code: `e1_regions/code/e1.py`, `regions.py`, `run_e1.py`, `test_barrier.py`, `test_live.py`
- Logs/results: `e1_regions/ledger.jsonl` (267 K, 1,063 rows), `e1_regions/out/report.md`, 72 `IMPROVE_*.json`.
- Generality: MIXED — the coordinator/barrier is circuit-generic; the orbit subspaces are MC-specific.
- Phase-2 verdict: **dead-end as stated**, but the *diagnosis* is a keeper (see `exact-move-census` below). Its own recommendation — partition by MOVE, not by area — was never tested.

### talk-channel-ablation (M1/M2/M3)
- Family: parallel coordination
- What it does: three independently switchable inter-worker messages — PROTECT (publish what my construction hangs off), DEMAND (ask a neighbour to build a mask I cannot, paying +1), TOKEN (mutex on boundary masks) — each ablated separately.
- Twist vs siblings: DEMAND with a gift-credit economy (grant, TTL, trim protection, revoke-by-restore) is new to the project.
- Measured performance: **M1 PROTECT is the only channel that pays** (+8% distinct/core-s, commit rate 0.648 → 0.745, p=0.0022). M2 DEMAND −26%, M3 TOKEN n.s. alone but it delayed a *provable* improvement 5–14× in the control. All three together −53%: destructive interaction. The demand economy did work mechanically — 50 demander-attributed gate reductions on the naive start — and delivered **zero** at all four frontier anchors.
- Cost: inside the 23,325 core-second budget above.
- Code: `e1_regions/code/e1.py`
- Generality: CIRCUIT-GENERIC (it is a coordination protocol).
- Phase-2 verdict: keeper for M1 only; M2/M3 dead-end at frontier radius.

### exact-move-census
- Family: structural-analysis
- What it does: enumerates the **complete** remove-1 + single-mask-repair move set of a state, then scores any proposed partition by what fraction of that move set stays region-local. No search needed.
- Twist vs siblings: it evaluates a search design *before* running it.
- Measured performance: the number that explains the whole E1 result — the complete remove-1 move set of the record 88@5 is **12 moves**, distributing 3/6/1/0 across four balanced regions (one worker has no legal move at all). Orbit partitions keep 74–98% of moves local; DAG-mincut and random partitions score **exactly 0.000**, structurally.
- Cost: seconds.
- Code: `e1_regions/code/move_census.py`
- Logs/results: `e1_regions/out/move_census.json`
- Generality: **CIRCUIT-GENERIC.**
- Phase-2 verdict: **keeper, top tier** — the cheapest way to kill a bad parallel/decomposition design before spending compute.

### plane-locality-measurement
- Family: structural-analysis
- What it does: measures whether a mask's plane signature is contained in a single rho-orbit's plane set, over the whole mask universe and over every circuit on disk.
- Measured performance: exactly **12,946 of 2^32 masks are plane-local (3.0e-6)**, and **all 1,136 masks** of the 11 verified circuits plus `naive_masks()` are inside that set, 0 exceptions. Stronger: every valid single-mask repair of the 88@5 / 89@5 / 92@4 anchors is plane-local (12/12, 36/36, 82/82), 91% at the naive start. A ~330,000× candidate-universe reduction, apparently free at the frontier.
- Caveat recorded in-source: every circuit on disk descends from one engine lineage, so this may be a property of the search trajectory, not of optimal circuits.
- Code: `e1_regions/code/regions.py`
- Logs/results: `e1_regions/out/plane_locality.json`, `out/planelocal_repairs.json`
- Generality: MC-HARDCODED (rho-orbit planes), but the *idea* — measure a cheap structural predicate over the whole known population and check every repair against it — is generic.
- Phase-2 verdict: **keeper.** Its own proposed decisive test (hand `slp_opt.py` an 87 instance restricted to plane-local masks) was never run — see LEADS.

### gauge-inflation-check
- Family: structural-analysis / measurement hygiene
- What it does: canonicalises sampled states under the project's gauge group and reports how many "distinct" frozensets collapse to one canonical orbit.
- Measured performance: at the 88@5, **~75× inflation** — 668 distinct frozensets collapsed to 1 canon in a 75-state sample. At the 89@5, inflation ~1.02. So every "N distinct states visited" claim at the record is a rotation count, not an exploration count.
- Code: `e1_regions/code/gauge_check.py`, `gauge_check88.py`
- Generality: MIXED (needs a gauge group for the target circuit).
- Phase-2 verdict: **keeper** — a mandatory sanity filter on any exploration-rate claim.

### output-subset-exact-pricing
- Family: exact-optimisation
- What it does: for a subset `S` of output rows, restricts to the support union of `S`, remaps to a low-dimensional instance, and gets the exact minimal SLP length from `atlas/slp_opt.py`; every returned program is lifted back to 32 bits and re-evaluated.
- Twist vs siblings: the round-trip lift is what makes the dimensional restriction safe rather than assumed.
- Measured performance: `U(1) = 152` exact (32/32 rows, each `w−1`); `U(2) = 114`; 127/127 round-trips passed; 127/127 `exhaustive`; 15/15 planted positives.
- Cost: 87 oracle decisions plus timeouts up to 5,489 s each.
- Code: `e2_outputcost/code/{runner,common,construct,report}.py`
- Logs/results: `e2_outputcost/ledger.jsonl` (914 rows, 348 K).
- Generality: **CIRCUIT-GENERIC** given a target matrix.
- Phase-2 verdict: **keeper, top tier** — this is how you get a defensible cost curve for a *new* matrix cheaply.

### venn-isomorphism-class-reduction
- Family: structural-analysis / combinatorial reduction
- What it does: two output-subsets are isomorphic instances iff a bijection of the support union matches all Venn-region sizes; one oracle run then decides the whole class, with an explicit machine-verified bit-permutation certificate.
- Measured performance: **496 pairs → 13 classes; 4,960 triples → 121; 35,960 quads → 1,264; the 8 rho-orbits → 2 classes.** 319 propagation rows, **0 certificate failures**. It turned "finish all 496 pairs" from 410 runs into 8.
- Cost: negligible (pure combinatorics).
- Code: `e2_outputcost/code/classes.py`, `cones.py`, `propagate.py`
- Generality: **CIRCUIT-GENERIC.** This is the highest-leverage reusable trick in the slice.
- Phase-2 verdict: **keeper, top tier.** Run it first on any new matrix; it prices the whole exact-subset programme before a single solver call.

### cancellation-free-milp
- Family: exact-optimisation (restricted)
- What it does: in a cancellation-free program masks add disjointly up the DAG, so candidate gates are exactly the size-≥2 subsets of the targets and minimising the built set is an exact integer program (scipy/HiGHS).
- Twist vs siblings: answers a *restricted* question exactly, so it is a cross-check rather than a substitute — and it is the only instrument in E2 that reaches dim 12–13 blocks at all.
- Measured performance: agrees with the true optimum **90/90** where both are known; **0** instances where cancellation strictly helps; 145/145 witnesses round-trip verified.
- Cost: 900 s hard cap, hit on both dim-12 weight-7 family reps.
- Code: `e2_outputcost/code/cfopt.py`, `cf_batch.py`, `cf_report.py`
- Generality: **CIRCUIT-GENERIC.**
- Phase-2 verdict: **keeper** — cheap upper bound plus a strong independent cross-check on any SAT result.

### order-of-sharing-cone-analysis
- Family: structural-analysis
- What it does: for each gate of a verified circuit, counts how many distinct output families its output cone spans.
- Measured performance: identical profile across **nine** verified circuits at four depths — ~2/3 of gates serve one rho-orbit, 20–30 serve exactly two, 0–1 serve three or four, and a constant tail of **2–3 gates serves five orbits**. Those 2–3 are always weight-2 masks on **bit 7** — the footprint of the reduction polynomial `0x11B`. Nothing anywhere shares across ≥6 orbits.
- Code: `e2_outputcost/code/section7.py`
- Logs/results: `e2_outputcost/artifacts/order_of_sharing.json`
- Generality: MIXED (needs a family decomposition; the method is generic, the rho-orbits are not).
- Phase-2 verdict: **keeper** — the sharpest structural description of *where* an optimum's sharing lives, and it directly generated the "fix the carry gates as a forced prefix" proposal (never run).

### partition-assemble-and-dedup
- Family: constructive
- What it does: solves blocks independently, glues them into a full 32-output circuit, and lets coincident masks deduplicate at glue time.
- Measured performance: this is the correction that matters — **Σ block costs is not the realisable count.** Order-1: Σ=152 assembles to 146 as chains, **139** as balanced trees. Order-4 family-optimal: Σ=114 assembles to a verified **105 @ depth 5**. So "optimise each family exactly and glue" has a hard ceiling of 105, seventeen gates above the record.
- Code: `e2_outputcost/code/construct.py`, `e8_quad/code/assemble.py`
- Logs/results: `e2_outputcost/artifacts/partition_*.json` (11), `e8_quad/artifact_family_optimal_circuit.json` (I re-verified: `gates=105 depth=5 outputs_built=32/32 VERDICT: VALID`).
- Generality: **CIRCUIT-GENERIC.**
- Phase-2 verdict: **keeper** — always the right first upper bound for a new matrix.

### plateau-drift-with-tabu-and-away-bias
- Family: plateau-search
- What it does: walks the equal-cost plateau with the shipped remove-1 + complete repair, adding a **tabu tenure** on just-removed masks and an **"away" bias** that picks, among all valid repairs, one not in the origin set (ballistic instead of diffusive).
- Twist vs siblings: both additions are absent from the shipped engines.
- Measured performance: raises distinct plateau states visited from **64 to 726** (11×) at matched compute — and moves the reach ceiling by **exactly zero masks**. Radius never exceeds **12** at the 88@5 across tabu 0/30/150 and a doubled step radius, over 1.04 M steps; **16** at the 88@6. `free_remove1` events: 0 in every arm. The 12→16 difference is entirely the **basin**, not the operator (de-confounded by running the missing cell).
- Cost: 1,500 s per arm × 6 arms.
- Code: `e3a_exploit/code/drift.py`, validated by `code/selftest.py` (56/56 agreement with shipped `engines._repair`, 0 disagreements)
- Generality: MIXED.
- Phase-2 verdict: **dead-end for finding gates, keeper as a diagnostic** — it measures the basin diameter, which is the number that closed the whole plateau-walking route.

### population-spread-measurement
- Family: structural-analysis
- What it does: reads every 88-gate harvest on disk, dedupes to distinct mask states, and measures pairwise symmetric difference over a sample.
- Measured performance: **78,281 distinct 88-mask states**, pairwise distance median 86 / p99 170 / max 172 (of a possible 176) — yet built from a union of only **916 distinct masks**. Combined with the cage result: the search *covers* a wide region by destroy-and-rebuild but cannot *move* through it at constant gate count.
- Code: `e3a_exploit/code/spread.py`
- Generality: **CIRCUIT-GENERIC.**
- Phase-2 verdict: keeper.

### self-controlling-block-reoptimisation
- Family: exact-optimisation
- What it does: takes a block `B` of a known circuit, defines NEEDED/AVAIL from the rest, and asks the exact oracle for the minimum in-block program at `max_gates = |B|`. One solve returns either a decoded witness at `|B|` — the positive control, **inside the same solve** — or a program below `|B|`, which is an 87 outright.
- Twist vs siblings: the atlas's `b9b_sweep.py` asked at `|B|−1`, a decision whose only outcomes are UNSAT or nothing. Asking at `|B|` costs the same and is strictly more informative — and it is what exposed three vacuous published negatives.
- Measured performance: whole 112-block dim-8 sweep in **1,291 s**. 67 `OPTIMAL_AT_nB`, 35 `NOT_COVERED`, 10 `CONTROL_FAILED`, **0 HIT**. Hit-path control: 4/4 spliced witnesses re-verified by the oracle.
- Cost: 21.5 CPU-minutes for the whole sweep the atlas had left unfinished.
- Code: `e3a_exploit/code/blocks.py`, `kern.py`
- Logs/results: `e3a_exploit/ledger.jsonl` `kind:"block"` rows (140).
- Generality: MIXED — the framing is generic; the sector geometry is MC-specific.
- Phase-2 verdict: **keeper, top tier.** "Ask at the known-achievable length so the control is the answer" is the single most reusable control-design idea here.

### population-scale-block-reoptimisation (blockpop)
- Family: exact-optimisation, scaled
- What it does: the same self-controlling question, but re-derives BLOCK/NEEDED/AVAIL for an **arbitrary replayed circuit** instead of the 14 named ones, so it can be pointed at the 78,281 harvested states.
- Twist vs siblings: address-by-content, not by `PATH[name]`; ~9 s per block.
- Measured performance (re-tallied by me from the ledger, **the RESULT.md numbers are stale**): **586 blocks decided — 324 `OPTIMAL_AT_nB`, 198 `NOT_COVERED`, 64 `CONTROL_FAILED`, 0 HIT.**
- Cost: shards ran past the write-up.
- Code: `e3a_exploit/code/blockpop.py`
- Generality: MIXED.
- Phase-2 verdict: **keeper** — the highest-coverage exact 87-detector in the project, and it is still nowhere near saturated (586 of 78,281).
- Trap recorded in-source and worth carrying: `campaign_87/*/runs/mtA.pop.jsonl` is a **transposed-matrix** harvest whose states are not MixColumns circuits; it silently filled 268 of a 400-state sample. Any harvest-wide sweep needs a validate-before-admit loader.

### buy-one-save-two
- Family: exact-optimisation
- What it does: adds ONE new in-sector mask `x` buildable in one gate from signals the block may use, then asks for the block in `|B|−2`. Net −1 ⇒ 87.
- Twist vs siblings: two-layer control — a per-block solve at `|B|` with `x` free, plus the sibling `blocks.py` witness at `|B|` without `x`.
- Measured performance (re-tallied by me; the RESULT.md says "still accumulating"): **4,926 candidate instances, verdict `UNSAT_at_nB_minus_2` on every one. 0 hits. The sweep is COMPLETE and empty.**
- Cost: ~1.2 s per instance.
- Code: `e3a_exploit/code/buyone.py`
- Logs/results: `e3a_exploit/ledger.jsonl` (4,926 `buyone` rows), `e3a_exploit/inst/` (5,705 generated instances).
- Generality: MIXED.
- Phase-2 verdict: **keeper as a template, closed as a question** for this matrix.

### complete-k3-shell (remove-3-add-2)
- Family: exhaustive neighbourhood
- What it does: complete enumeration of every remove-3 window with a budget-2 repair, per circuit, with a planted-positive control (pad with a redundant mask, remove a window containing it, the routine must find the 2-mask repair).
- Measured performance (re-tallied; **RESULT.md predates two of these**): control POSITIVE on 88d5, 88d7, 88fs. **Two complete exhaustive certificates now exist — 88@7 and 88fs, 27,720 windows each, "EXHAUSTIVE: no remove-3-add-2 improvement"** — plus 88@5 stopped INCOMPLETE at 25,064/27,720 (90%). Previously only 88@6 had one.
- Cost: 1,758–2,700 s per circuit.
- Code: `e3a_exploit/code/k3shell.py`
- Generality: **CIRCUIT-GENERIC** in principle.
- Phase-2 verdict: **keeper** — a bounded, cheap, exhaustive local-optimality certificate.

### parity-pinned-orbit-walk (sigma sector)
- Family: symmetry-sector search
- What it does: in the sigma = rho² symmetric sector a closed set costs `2a + b` with `b` = number of sigma-fixed masks, so cost is odd iff `b` is odd. The walk **completely enumerates** the one-gate-buildable sigma-fixed injection pool, injects each in turn to reach odd `b`, then rejects every move that flips `b mod 2`.
- Twist vs siblings: the shipped orbit engine can change `b` but is never pinned, so it drifts back into the even half — which is exactly what its 166 cycles at `cur=90 best=90` look like.
- Measured performance: 2 seeds, 2 independently enumerated pools (130 and 78), 56 injections, **every one settles at 91, none reaches 89**; 54,596+ moves rejected purely for parity. Sector state: even half 90 (`b`=16), odd half **91** — two independent points, `b`=15@d5 and `b`=13@d7. E7 then showed the crucial re-pricing: below 91 the next odd value is **89**, so this is a **two-gate** move, not one.
- Cost: minutes per arm; pinned walk runs at 47 it/s vs 1.2 it/s for a destroy/rebuild LNS in the same sector.
- Code: `e3a_exploit/code/orbit_odd.py`, `e7_push/code/pinprobe.py`, `e7_push/code/sigma_odd.py`
- Logs/results: 3 + 2 verified sigma-closed circuits in `found/` (I re-verified `sigma_91gates_depth7_fixed13.json`: `gates=91 depth=7 VERDICT: VALID`).
- Generality: MC-HARDCODED (needs a symmetry of the matrix).
- Phase-2 verdict: keeper as a **method template** (symmetry sector + parity invariant + pinned search); dead-end for 87 here.
- **Control correction worth carrying:** E3a called its odd-half negative controlled on the strength of a 94→93→92→91 descent. Those costs alternate parity, so that descent works by crossing between halves — it controls the sector, not the half. E7 built the matched control (93 → 91 with the pin on, two gates, same parity class) and it fired.

### plan-space-sizing
- Family: pre-measurement (no solver)
- What it does: counts the model size `|W|` a cancellation-plan configuration would cost, before anyone builds the model.
- Measured performance: the per-child form is buildable at every `c ≤ 6` (`|W|` = 11,209 → 42,603) against tier3c's unbuildable 87,897. Seconds, no solver, and it retired a blocking argument that had killed a whole lane.
- Code: `e3a_exploit/code/plansize.py`, `e6_cancelplan/code/size.py`, `vocabsize.py`, `popsize.py`
- Generality: **CIRCUIT-GENERIC.**
- Phase-2 verdict: **keeper, top tier.** Cheapest possible way to kill or unblock a formulation.

### fixed-size-infeasible-search (FIXN)
- Family: relaxation search
- What it does: pins `|S| = N` exactly and lets the state be an **invalid** circuit for the whole run, minimising a graded potential `Φ = Σ_t c(t)` where `c(t)` is the *exact* minimum extra masks needed to build target `t` (exact for 0,1,2; capped at 3). Metropolis acceptance, so coverage may decrease.
- Twist vs siblings: the intersection of two prior dead ends — `walk87.py` never let coverage decrease; `m4_inverse` searched program space and failed its control. FIXN is mask-set space + fixed size + decreasing coverage + the r2 gradient.
- Measured performance: **control fires 203× at the record** — 768 materialisations, **767 independently oracle-verified 88s** from infeasible fixed-size states at N=84/85/86. At N=87: 0 materialisations, best total 89, 18,683 iterations. A **controlled null**, not a vacuum.
- Radius by-product: minimum Jaccard to seed 0.130 at N=87 — 87% of the mask set replaced at constant cost. But the hot setting reached Jaccard 0.13 with a Φ floor of 6, the cold setting held Φ at 2 but stayed above Jaccard 0.52: **far travel and low objective never co-occurred.**
- Cost: ~71,000 iterations over 9 runs.
- Code: `e3b_fresh/code/fixn.py`, `common.py`
- Generality: **CIRCUIT-GENERIC** (the potential is defined from any target set).
- Phase-2 verdict: **keeper** — one of very few instruments here whose control fires 200+ times at the record.

### demand-flow-(A,B)-neutral-neighbourhood-pricing
- Family: representational search
- What it does: at a verified circuit's prefix `n`, enumerates the **complete** structured free-routing neighbourhood (zero-gate moves that change routing `B` behind an identical mask set `A`) and rolls out every member.
- Twist vs siblings: it *prices* a lever the project called "the strongest proof-of-concept result" and never measured.
- Measured performance: the rollout is exact from prefix ≥46 (a sharp cliff at 45 — the first calibration in the project's history). At every calibrated prefix from 47 to 86, across three 88 families and the 89: **0 improving, 0 even-neutral** among 8–162 moves; best child uniformly parent+1. Two working controls: (a) the estimator returns the parent's true gate count; (b) the same instrument *does* find 10 and 15 improving moves on rows where the rollout is wrong. `dfattack` beam search over 240 windows: `best_found` histogram `{88: 240}`.
- Cost: cheap.
- Code: `e3b_fresh/code/df/{dfcal,dffreedom,dfneutral,dfattack}.py`
- Generality: MIXED.
- Phase-2 verdict: **dead-end at the frontier, keeper as a cautionary result** — it explains seven earlier routing "search failures" with one mechanism instead of seven budgets, and it retired a recommended architecture (per-mask-set routing archive) before it was built.

### automorphism-group-proof (SYMGF)
- Family: structural proof
- What it does: complete backtracking over bit-permutations `π` of the 32 input coordinates with `π(TARGETS) = TARGETS`.
- Measured performance: **|Aut| = 4, proved in 0.1 s** — exactly `{ρ⁰,ρ¹,ρ²,ρ³}`. The real centraliser in GL(32,2) is ≥255× larger (bytewise GF(2^8) multiplication commutes with M, verified), but **zero** of the 254 non-trivial scalars is a coordinate permutation, and only a coordinate permutation can be imposed as mask-set invariance. Consequence: the tempting "87 ≡ 0 mod 3, 88 ≡ 1 mod 3" order-3 sector **does not exist** — closed by proof, not by search.
- Cost: 0.1 s.
- Code: `e3b_fresh/code/symgf.py`, `symgf_check.py`
- Generality: **CIRCUIT-GENERIC.** This is the first thing to run on a new matrix — it tells you the whole symmetry budget in a second.
- Phase-2 verdict: **keeper, top tier.**

### orbit-drop-and-readd (heuristic beam)
- Family: relaxation search
- What it does: drops a whole rho-orbit (4 targets), re-optimises the 28-target relaxed instance with retargeted engines, then re-adds the orbit with a beam search.
- Measured performance: the relaxation does bite (weight-7 orbits give a 28-target set 1–2 masks smaller than the 88's own), **but the re-add gives it all back and more.** Best total 89. Honest control failure recorded: for orbit 3 the relaxed set is byte-identical to the 88's own sub-circuit, so the true re-add cost is ≤10 and the beam returned 11 ⇒ the beam is ≥1 gate loose and every "total" is an inflated upper bound.
- Code: `e3b_fresh/code/orbitdrop.py`, `readd_beam.py`, `retarget.py`, `tdrop.py`
- Generality: MIXED.
- Phase-2 verdict: superseded-by-`free-gate-reduction-exact-readd`.
- **Reusable gotcha:** `mixcolumns_core.verify` hardcodes `outputs == 32`, so it can never pass a target-*subset* instance; anyone retargeting `pipeline/engines.py` will silently get "0 improvements".

### free-gate-reduction-exact-readd
- Family: exact-optimisation
- What it does: the reduction that makes a dim-32 question exhaustible. The dropped targets are absent from the available set `A`, so **each of them must BE a gate**; a `k`-gate completion is `G = T ⊎ F` with only `|F| = k−4` free gates. Build order never has to be searched because reachability from `A` is a **confluent closure**.
- Twist vs siblings: it converts "synthesise 4 outputs at dim 32" (impossible for `slp_opt.py`, whose delta table is 4 GB at dim 32) into "find at most 5 extra masks".
- Measured performance: **exact minimum re-add cost = 10** for E3b's open 87 question (9 would have been 87). And across **41 decided instances** — all 8 rho-orbits of all five verified 88s, plus E3b's relaxed sets — `exact_readd = 88 − |remaining|` in **41 of 41**, total 88 every time, never 87 and never 89.
- Cost: ~4 s at k=6, ~400 s at k=8, 3,980 solver-seconds for the k=9 cube run.
- Code: `e5_readd/code/{kern,satx,dfs,cube,mkinst,runner}.py`
- Generality: **CIRCUIT-GENERIC.** The reduction only needs "the dropped targets are absent from `A`", which holds for any circuit and any target subset.
- Phase-2 verdict: **keeper, top tier.** This is the most transferable exact technique in the slice.

### position-cube-and-conquer (E5 flavour)
- Family: SAT decomposition
- What it does: values are distinct and every target must be carried, so exactly one gate carries each target; enumerating the set `P` of target-carrying positions partitions all solutions into 56 cubes. The hardest cube got one further split by *which* target sits last.
- Measured performance: monolithic k=9 did not finish in 3,600 s; the split finished with **56/56 cubes UNSAT and none left undecided**. Discipline recorded: a single undecided cube would make the run UNDECIDED.
- Code: `e5_readd/code/cube.py`
- Generality: **CIRCUIT-GENERIC.**
- Phase-2 verdict: keeper. (Note the tension with the campaign-wide finding that cubing on gate-0 pairs *multiplies* work — cubing on **semantic** positions is a different and better split than cubing on gate 0.)

### all-drop-k local-optimality screen
- Family: exhaustive certification
- What it does: enumerates **every** k-target drop set of a circuit, scores each by `W = 88 − |trim|` (the gates the circuit spends privately on that set), and refutes `k = W−1` on each — by SAT where needed and by an exhaustive counting argument where the arithmetic suffices.
- Measured performance (re-tallied by me; the RESULT.md reports only the first family): **88@5: 35,960/35,960 refuted** (8,487 by SAT in 3,875 solver-seconds, 27,472 by counting, 1 by the cube run). **88fs5: 35,960/35,960 refuted — `screen_done` logged, 13,315 screened + 22,645 by counting.** Zero improvements, zero timeouts, zero non-`unsat` verdicts in either. A `W`-for-`W−1` swap moves up to `2W−1 = 19` masks, so this is a local-optimality certificate at radius up to 19, against the corpus's previous best of "the whole k≤3 neighbourhood is empty".
- Cost: ~1 hour per circuit.
- Code: `e5_readd/code/screen.py`, `report.py`
- Logs/results: `e5_readd/ledger.jsonl` — 72,201 `drop4` rows, all `unsat`.
- Generality: **CIRCUIT-GENERIC.**
- Phase-2 verdict: **keeper, top tier** — the strongest local-optimality statement in the whole slice, and now doubled.

### five-control-stack (E5)
- Family: verification discipline
- What it does: five independent controls on one exact campaign — witness replay (45/45), escalation SAT (41/41 `sat` at the exact value after exhaustive `unsat` below), matched seeded control at the *same free-gate budget* (39/39 fired), two-engine agreement SAT vs DFS (131/131, 0 disagreements), symmetry-free recheck of the intricate value-lex rule (6/6 reproduce), and oracle round-trip (39/39 assembled 32-output circuits VALID at exactly `n+k = 88`). Plus `selftest_dfs.py`: 3,972 random instances against a brute force over gate *sequences* sharing no code, 0 mismatches.
- Phase-2 verdict: **keeper as the template.** This is what a defensible exact negative looks like; copy the stack wholesale.

### per-child-candidate-set CP-SAT plan model
- Family: constraint programming
- What it does: models a cancelling gate as a triple `(child z, overlap O, split A)`; each child carries its own candidate overlap list; `y_i ∈ {0,1}` makes cancellation **optional**; integer times on a measured `NEEDT` cone let a cancel output feed a disjoint gate.
- Twist vs siblings: optional cancellation is the structural fix for the failure that voided 143 prior decisions — the model *contains* the pure cancellation-free solution, so plan incoherence cannot exist, and one solve decides all `2^n` sub-plans.
- Measured performance: **the lane's first non-vacuous decision** — `W1w1_orbit1` INFEASIBLE at budget 87 in 188 s, exhaustive over its overlap class. 7 configurations run at 87, **1 decided, 6 UNKNOWN**. Flagship arm POPUNION synthesised a **verified 88-gate depth-5 circuit (66 CF + 22 cancelling)** from a 796-pair vocabulary with the child↔overlap assignment FREE — and drove the dual bound only to 46 of 88 in 3,762 s. Bound-gain rate measured at **0.02–0.03 gates/second**, and it *falls* as the candidate set grows (57 at 122 pairs, 46 at 796).
- Cost: 188 s – 3,762 s per configuration at 4 CP-SAT workers.
- Code: `e6_cancelplan/code/cpk.py`, `sweep.py`, `popcfg.py`, `vocabcfg.py`
- Generality: MC-HARDCODED (the V1-2(b) formulation is specific to this analysis).
- Phase-2 verdict: keeper as a **formulation lesson** (make the hard structure optional so the model contains a trivially feasible point); the decision form is superseded — its own conclusion is "stop deciding, start bounding, and not with CP-SAT".

### four-control-suite (E6: C0/C1a/C1b/C2/C3)
- Family: verification discipline
- What it does: C0 model sanity with cancellation forbidden; C1a **solver-free** representability of 9 real circuits (problems = 0 on all 9); C1b representation *with* the solver on 8 donors at six depths, each hit exactly on its own gate count; C2 the sampler control whose absence voided 143 configurations; C3 a per-configuration control run on the very configuration that produced the negative.
- Measured performance: 9/9, 16/16, PASS, and 6 of 6 stage-B controls green. The one recorded FAIL is C0's first unhinted run — kept in the ledger on purpose because its diagnosis (no incumbent in 622 s, dual bound 93.0) is what produced the greedy hint.
- Phase-2 verdict: **keeper** — C1a in particular (check by hand that a real solution satisfies every constraint before trusting any INFEASIBLE) is nearly free and catches encoding incompleteness.

### candidate-class naming-rate measurement
- Family: pre-measurement
- What it does: scores a candidate class by what fraction of **real** cancelling gates it names, over 41,067 gates from 1,500 circuits, alongside the model size it costs.
- Measured performance: `W1` names 0.413 at `|W|`=38,240; `W2` names 0.702 at 211,936; `W3` 0.772. Since a configuration decides only circuits *all* of whose cancelling gates it names, the useful quantity is the naming rate raised to the power κ: `0.41^27 ≈ 10^-10.6`. The economically-motivated `TDIFF` class names **12.9%** — worse than a plain weight cap. **The classes wide enough to contain a good circuit are exactly the classes too large to build.**
- Code: `e6_cancelplan/code/classes.py`, `lean.py`, `scope.py`, `popclass.py`
- Generality: **CIRCUIT-GENERIC** in method.
- Phase-2 verdict: **keeper, top tier** — prices a whole strategy in seconds. Its sibling `lean.py` killed the obvious escape (only 16.6% of 82,578 real cancel parents are built as `A ⊕ O`) before anyone spent a week on it.

### vocabulary-saturation measurement
- Family: structural-analysis
- What it does: reads circuits until the `(child, overlap)` vocabulary stops growing.
- Measured performance: **4,120 pairs over 1,469 children, saturated** — 2,000 → 12,000 circuits grows it by 1.3%. That repairs an earlier diagnosis: in `(z,O)` coordinates the population is essentially self-covering, so the coordinate change was right and the corpus was never the problem; the problem is that the faithful set costs 1.81× the size at which the previous instrument returned UNKNOWN.
- Code: `e6_cancelplan/code/satur.py`; data in `e6_cancelplan/data/pop_vocab.json` (107 K)
- Generality: **CIRCUIT-GENERIC.**
- Phase-2 verdict: keeper.

### resumable cube-level exact decision
- Family: SAT decomposition / engineering
- What it does: partitions a level into one task per choice of gate 0's input pair (an exact partition, since gate 0's pair selector is exactly-one), runs cubes in parallel, and **writes every finished cube to an append-only file**, so a deadline miss costs only the cubes in flight and `--resume` picks up where it stopped. It asks at `|B|−1` with the control taken from a verified greedy witness at `|B|`, and refuses to report a negative if that control does not verify.
- Twist vs siblings: pure resumability. `slp_opt.py` as a subprocess throws away every finished cube when its deadline expires, which is why a 12-CPU-hour level looked unschedulable.
- Measured performance: E3a projected ~12 CPU-hours for the last level; it cost **5,689 CPU-seconds** — a 7× pessimistic projection. Per-level CPU: k=7 → 42 s, k=8 → 83, k=9 → 788, k=10 → **5,689**; the ~16.6×-per-level rule of thumb overshoots here (2.0×, 9.5×, 7.2×). Validated against the monolithic path on the same instance (identical UNSAT at k=7,8,9).
- Cost: ~2,000–5,500 s wall on 3 cores per region.
- Code: `e7_push/code/cube.py`; state in `e7_push/cubes/*.jsonl` (21 files, 4,083 cube records, 320 K)
- Generality: **CIRCUIT-GENERIC** (it wraps `slp_opt` unchanged).
- Phase-2 verdict: **keeper, top tier.** Any long exact solve should be built this way.

### topologically-convex block closure
- Family: instance repair / structural proof
- What it does: fixes a specification bug. A gate `o` can simultaneously be a *descendant* of one block gate and an *operand* of another (no cycle — `o` just sits between them in topological order), and `AVAIL` excludes descendants, so the instance cannot express the circuit's own program. The repair is the interval closure `B* = B ∪ {g : g is a descendant of B and an ancestor of B}`, with a written proof of sufficiency.
- Measured performance: diagnostic over all 112 blocks, no solver, seconds: sector 0 has 10 blocks with a descendant-operand and 10 uncovered raw → **0 uncovered after the closure**. All 14 sector-0 blocks then decided `OPTIMAL_AT_nB` with the control firing in 14/14, total cost 1,315 s. In sectors 1/3/4 the coverage failure survives the closure, confirming those need dimension 12 — a genuinely different failure.
- Code: `e7_push/code/convex.py`
- Generality: **CIRCUIT-GENERIC** (it is a DAG property).
- Phase-2 verdict: **keeper.** And a general lesson: a "free structural control" that tests the wrong predicate is worse than no control.

### exact canonical-set DFS (qsearch)
- Family: exact-optimisation, purpose-built
- What it does: iterative-deepening DFS over **sets** of gates in canonical lex-minimal build order, with an admissible non-counting lower bound and an exact end-game. Four ideas, each with its soundness proof written into the source header.
  - (a) enumerate sets not sequences: buildability is monotone so the greedy closure is confluent, giving each buildable set a unique canonical order — removes the `k!` orderings;
  - (b) bound `b ≥ max_i(d_(i) + i − 1)` over sorted per-target distances — gives 7 at the root against 4 for every counting bound tried. **Two tempting stronger forms are false and are documented as such**, which is exactly the shape of error the repo already recorded as a near-miss false negative;
  - (c) exact end-game: when remaining budget equals unbuilt targets, every remaining gate must *be* a target, decided exactly by greedy — removes the last levels where nearly all the cost lives;
  - (d) `dist[]` maintained in one pass, 256 byte-ops per node at dim 8.
- Measured performance: refuted k ≤ 9 in **2.2 s** where the generic SAT oracle needed 1,200 s; k=11 refuted at 698,949,645 nodes in 959 s; k=12 SAT with decoded witness. **`cost(rho-orbit quad) = 12` exactly.** Turned a 14-day estimate into 16 minutes.
- Controls: 121/121 agreement with the generic oracle, 300/300 against a deliberately prune-free reference searcher, 25/25 planted positives at k=10/11/12, 2000/2000 independent completeness audit of every prune, and — the one that matters — **it demonstrably can see cancellation pay** (strict gains on 48 of 400 random instances, smallest at dim 5).
- Cost: single-threaded C, `gcc -O2`. Wall: 959 s for the hardest refutation.
- Code: `e8_quad/code/qsearch.c` (+ `instances.py`, `refsearch.py`, `differential.py`, `planted.py`, `audit_path.py`, `cancelscan.py`)
- Generality: **CIRCUIT-GENERIC for small dim** — it takes `dim`, singleton inputs, and an arbitrary target set. Hard wall: the `dist[]` pass is `2^dim`, so dim 12 is 16× dim 8 per node (the dim-12 orbit class is bracketed `[11,18]`, UNDECIDED). Removing that wall (a lazily evaluated bound over the ≤20 available masks) is the named next step.
- Phase-2 verdict: **keeper, top tier.** Ideas (a) and (c) are general and, per its own write-up, nothing in `pipeline/` or `beat88/` uses them.

### CPU-second budgeting from /proc
- Family: measurement instrumentation
- What it does: drives the shipped `pipeline/worker.py` unmodified but budgets in the worker's own `utime+stime` read from `/proc/<pid>/stat`, with a deliberately loose wall safety net.
- Why it matters: at `nice -n 10` on this box at load ~39, a worker got **3 CPU-seconds in 238 wall-seconds — 1.4% of one core**. The first calibration gave every worker a "480-second" budget worth ~7 CPU-seconds and everything timed out. **Wall clock is not a budget on this machine.**
- Measured performance: with it, the step-1 gate passed — 90@5 → 89@5 in a median **16.6 CPU-s, 8/8 restarts**.
- Code: `e9_radius/code/harness.py`, `calib.py`
- Generality: **CIRCUIT-GENERIC** (pure ops).
- Phase-2 verdict: **keeper, mandatory.** Every future experiment on this box should budget this way.

### chained shake-and-recover displacement
- Family: large-neighbourhood operator
- What it does: buys radius in *cycles* — shake by a modest step, descend back to `n0`, repeat until achieved radius reaches the target. Every cycle ends at the anchor's own gate count, which is what "constant gate count" has to mean.
- Twist vs siblings: it pins gate count **per state**, not per arm. That is the fix for a general reporting defect (E1(c) reported a displacement statistic and a quality statistic from two different states in the same table).
- Measured performance — the headline number: radius at constant gate count costs **0.8 CPU-s per mask two gates above the frontier and 5.2–11.1 at it**, a 6–14× price rise, with reach capped at ~1/4 of what is requested. **Half of all shake-and-recover cycles at an 88 fail to restore 88 gates** (32/64 and 24/46). Because reach is bought *by descending*, it fails wherever descent fails — reach and descent are not two independent dimensions.
- Cost: 3.13 core-hours over 122 trials, 11 calibrations, 14 interleaved controls.
- Code: `e9_radius/code/chain.py`, `shake.py`, `trial.py`
- Generality: MIXED.
- Phase-2 verdict: **keeper** — it is the only operator measured here that moves a circuit a long way while pinning its gate count at every step, and it is ~5 lines of glue over the shipped rebuild.

### radius-hypothesis significance test
- Family: experimental design
- What it does: matched TEST budgets and matched descent seeds per trial index, arms analysed by **achieved** rather than requested radius, an r=0 paired null that is simultaneously a live positive control, and controls interleaved every 8–10 trials rather than front-loaded.
- Measured performance: on the one anchor whose control fires (n=70, 33 descents), P(descend) is **flat** — 0.43 at r=0, 0.67 at r=15–26, 0.32 at r=27–45; permutation p=0.35 with a *negative* effect direction; every Fisher p ≥ 0.19. Interleaved control **14/14 fired**. The other five anchors' nulls never fired and their arms are reported as **VACUOUS**, explicitly.
- Code: `e9_radius/code/trial.py`, `tally.py --trend --fisher --disp`
- Generality: **CIRCUIT-GENERIC** (it is a design, not a search).
- Phase-2 verdict: **keeper, top tier.** The best-designed experiment in the slice; reuse the design wholesale.

### corpus-wide degeneracy census
- Family: structural-analysis
- What it does: streams **every** 88-gate population file in the repo (460 files, 3.9 GB) and measures structural coordinates of every non-target mask.
- Measured performance: **3,280,541 distinct 88-gate circuits are built from 3,172 distinct words.** Families, basins, Jaccard distance and depth are all rewiring of one small dictionary. Degeneracy scan: mask weight ranges 2–18 (not degenerate), lanes 1–5 (not degenerate), but **`|odd(m)| ∈ {0,1,2}, never 3** — 0 occurrences in ~184 M mask slots. Histogram: `0: 113,366,654 / 1: 67,470,645 / 2: 3,881,285 / 3+: 0`.
- Cost: 393 s.
- Code: `e_oddlane3/census.py`
- Logs/results: `e_oddlane3/NOTEBOOK.md`, `hunt.out`
- Generality: **CIRCUIT-GENERIC** in method (find the corpus's degenerate coordinates), MC-specific in the coordinate definitions.
- Phase-2 verdict: **keeper, top tier.** "Measure what no circuit we ever found does, then force a search into that region" is the most original framing in the slice, and it is cheap.

### feature-pinning survival floor (upstream cultivation)
- Family: constructive / feature pricing
- What it does: pins a structurally novel mask `v` by adding it to the target set (**both `engines.TSET` and `engines.T`** — `_extract` iterates the list, so pinning only the set lets LNS silently drop it) and descends from a 100–173-gate from-scratch root. The smallest size reached with `v` still alive is the feature's **price**.
- Twist vs siblings: a novelty *bias* does not survive descent (`trim_masks` keeps only what the targets need); a *pin* does. And it starts upstream, where the feature is abundant and free, instead of at 88 where it is provably extinct.
- Measured performance: floors banked across 33 runs at 89–94 gates. **The best is 89 gates, carrying mask `0x98` with `|odd| = 3`** — a feature with zero occurrences in 184 M mask slots of the 88 corpus. I re-checked all 33: every mask set is realizable from the 32 input singletons with 0 unbuildable masks, contains all 32 targets, and contains its pinned mask. So the measured price of leaving the corpus vocabulary is **≤ 1 gate**, not "expensive". Never written up.
- Cost: 16 workers × ~190 jobs × 1200 s.
- Code: `e_upstream/deep.py`, `probe.py`
- Logs/results: `e_upstream/S*.json` (33), `w00..w15.log`
- Generality: **CIRCUIT-GENERIC in method** — it prices *any* structural feature against *any* target set.
- Phase-2 verdict: **keeper, top tier, and unfinished.** See LEADS.

### SAT benchmark packaging + semantic-identity proof
- Family: reproducibility engineering
- What it does: the live campaign never writes a DIMACS file (it hands `cnf.clauses` straight to a solver), so the shipped benchmark's identity had to be *established*: same instance object (pinned SHA256, re-derived through the running lane's own assertion module), same encoder call, clause-for-clause round trip (`clause-order sha256` identical both ways), and behavioural agreement (three lower levels solved **from the shipped files** returning the verdicts the campaign banked with a *different* encoder).
- Decoder discipline: the decoder re-evaluates all 285,480 clauses under the model rather than trusting the solver, and has four demonstrations — a real solver model decoded gate-for-gate identical to an independently banked witness; a corrupted model correctly rejected with exit 2; a full-scale k=14 planted model decoded identically; and the `verify_circuit.py` leg exercised on a real 88-gate circuit.
- Measured performance: I ran `sha256sum -c SHA256SUMS` — **51/51 OK**. The k-ladder difficulty gradient is measured, not guessed: 12.1 s (k=9) → 130 s → 708 s → 5,762 core-s → 105,083 s on 8 cores (k=13); growth 26.4× then 20.2×, pricing k=14 at ≈650–1,100 core-hours.
- Code: `sat_package/code/{gen_cnf,check_cnf,make_planted,plant_model}.py`, `decode_solution.py`
- Generality: **CIRCUIT-GENERIC as a template.** The instance is MC-specific; the identity-proof pattern transfers to any campaign that solves in-memory.
- Phase-2 verdict: **keeper, top tier.** This is the model for how to publish an artifact from an in-memory campaign.

---

## 3. ARTIFACTS (counts + labels)

### Write-ups
| label | count | command | path |
|---|---|---|---|
| `RESULT.md` experiment reports | 10 | `ls e*/RESULT.md \| wc -l` | `e1_regions`, `e2_outputcost`, `e3a_exploit`, `e3b_fresh`, `e4_depth`, `e5_readd`, `e6_cancelplan`, `e7_push`, `e8_quad`, `e9_radius` |
| generated tally snapshots | 4 | `ls e*/TALLY.txt e*/report_snapshot.txt e*/out/TALLY.txt` | e3a, e6, e7 (`TALLY.txt`), e8 (`report_snapshot.txt`), e4 (`out/TALLY.txt`) |
| notebooks (no RESULT) | 2 | — | `e_oddlane3/NOTEBOOK.md`, `e_upstream/NOTEBOOK.md` |
| maintainer notes / charters | 3 | — | `_shared/BRIEF.md`, `e7_push/ATLAS_NOTE.md`, `sat_package/SUBMISSION_NOTES.md` |
| package README | 1 | — | `sat_package/README.md` |
| generated report fragments | 10 | `ls e1_regions/out/*.md e1_regions/out/parts/*.md` | `e1_regions/out/report.md`, `RESULT_draft_notes.md`, `parts/sec1-8.md` |

### Ledgers (append-only, one object per decision)
`wc -l e*/ledger.jsonl` → **83,252 rows total**; `du -ch e*/ledger.jsonl` → **19 M**.

| ledger | rows | size | dominant row kinds |
|---|---|---|---|
| `e5_readd/ledger.jsonl` | 72,805 | 16 M | `drop4` 72,201 (all `unsat`), `decision` 304, `cube` 121, `exact` 41, `roundtrip` 39 |
| `e3a_exploit/ledger.jsonl` | 6,051 | 1.3 M | `buyone` 4,926, `blockpop` 586, `block` 140 |
| `e3b_fresh/ledger.jsonl` | 1,632 | 464 K | FIXN iterations, df arms |
| `e1_regions/ledger.jsonl` | 1,063 | 268 K | 193 `ev="run"`, plus `new_best`/`improvement`/`batch_*` |
| `e2_outputcost/ledger.jsonl` | 914 | 348 K | `cost_by_isomorphism` 319, `gap` 239, `cost` 194, `cancellation_free_optimum` 145, `planted_positive` 15 |
| `e7_push/ledger.jsonl` | 221 | 95 K | `diagnose` 112, `cube_level` 24, `convex_block` 19 |
| `e9_radius/ledger.jsonl` | 189 | 119 K | trials, controls, hits |
| `e8_quad/ledger.jsonl` | 171 | 99 K | `control_vs_e2` 121, `quad_level` 37 |
| `e6_cancelplan/ledger.jsonl` | 124 | 58 K | `cfg`, `sizing`, `spancheck`, controls |
| `e4_depth/ledger.jsonl` | 82 | 28 K | `restart_end` 49, `d4floor` 11, `anchor_check` 6, `floor_timeout` 6 |

### Verified / checked circuits and mask sets — 238 files
`ls e1_regions/out/IMPROVE_*.json e1_regions/anchors/*.json e2_outputcost/artifacts/*.json e3a_exploit/found/*.json e3b_fresh/found/*.json e3b_fresh/relaxed/*.json e4_depth/out/records/*.json e4_depth/out/resched/*.json e4_depth/out/floor/*.json* e5_readd/found/*.json e7_push/found/*.json e8_quad/artifact_*.json e9_radius/hits/*.json e_upstream/S*.json | wc -l` → **238**

| label | count | gate counts | path | note |
|---|---|---|---|---|
| E1 improvement circuits, all oracle-verified | 72 | 89–100 | `e1_regions/out/IMPROVE_*.json` | all 72 beat their anchor and all 72 passed the oracle; smallest 89 |
| E1 anchors (incl. the constructed 90-gate power control) | 8 | 88–127 | `e1_regions/anchors/` | `c90.json` is provably one shipped move from an 89 |
| E2 assembled partition circuits, oracle-VALID | 11 | 105–146 | `e2_outputcost/artifacts/partition_*.json`, `naive.json` | includes `partition_U2.json` at 114 |
| E8 family-optimal assembled circuit | 1 | **105 @ d5** | `e8_quad/artifact_family_optimal_circuit.json` | I re-verified: `VERDICT: VALID`. Exact ceiling of the per-family strategy |
| E8 decoded 12-gate quad optima | 2 | 12-gate blocks | `e8_quad/artifact_orbit{0,2}_12gates.json` | one contains 2 cancelling gates |
| E5 round-trip 88-gate circuits | 39 | **88** | `e5_readd/found/` | 11 of them are NOT the seed circuit — genuinely distinct exactly-optimal completions (min Jaccard 0.934, same family) |
| E9 verified 89@5 circuits | 35 | **89 @ d5** | `e9_radius/hits/` | 35 distinct canonical states, each oracle-verified twice; the first population at 89 |
| E3b FIXN/READD circuits | 7 | 88, 89, 91 | `e3b_fresh/found/` | 5 of them are 88s at depths 5–9 |
| E3b relaxed 28-target mask sets | 4 | 78–80 masks | `e3b_fresh/relaxed/` | the inputs to E5's exact question |
| sigma-closed sector circuits | 5 | 91, 91, 92, 93 | `e3a_exploit/found/` (3), `e7_push/found/` (2) | best odd-parity sigma point = 91, in two distinct `(gates, b)` classes |
| E4 depth-4 records + reschedules | 8 | 91–92 @ d4, 89 @ d5 | `e4_depth/out/records/`, `out/resched/` | `atlas_compiled_m1_91gates_depth4.json` is the **third independent 91@4 lineage** |
| E4 MaxSAT floor witnesses | 13 | 91–92 | `e4_depth/out/floor/` | each oracle-verified at its cap; one `.ORACLE_REJECTED` kept deliberately as the record of a borrowed-code defect |
| `e_upstream` pinned survival floors | 33 | 89, 90×3, 91×6, 92×12, 93×6, 94×5 | `e_upstream/S*.json` | **mask-set format, not oracle format, never verified.** I checked all 33 in-process: realizable, all 32 targets present, pin present |

### Bound / decision certificates (what each certifies)
| label | count | certifies | path |
|---|---|---|---|
| drop-4 local-optimality, complete | **2 circuits × 35,960 sets** | no 4 output rows of that 88 can be resynthesised from the rest using even one gate fewer — a local-optimality certificate at radius up to 19 | `e5_readd/ledger.jsonl` (`kind:"drop4"`, all `unsat`; two `screen_done` rows) |
| exact rho-orbit re-add costs | 41 | `exact_readd = 88 − |remaining|`, total 88, in 41/41 (circuit, orbit) instances | `e5_readd/ledger.jsonl` (`kind:"exact"`) |
| dim-8 sector-block optimality | 67 + 14 (convex) + 324 (population) | the block's own gate count is the exact in-sector optimum, with a decoded witness in the same solve | `e3a_exploit/ledger.jsonl`, `e7_push/ledger.jsonl` |
| dim-12 tap-region optimality | **4** | `min_gates = 11 = |B|`, `lower_bound_proven = 11`, every cube reporting | `e7_push/ledger.jsonl` (`kind:"cube_verdict"`), `e7_push/cubes/*.jsonl` (4,083 cube records) |
| buy-one-save-two refutations | 4,926 | no block of any of the 14 known 88s can be rebuilt in `|B|−2` gates even given one free extra in-sector mask | `e3a_exploit/ledger.jsonl` (`kind:"buyone"`) |
| complete remove-3-add-2 shells | 2 complete + 1 at 90% | no remove-3-add-2 improvement exists for 88@7 or 88fs (27,720 windows each) | `e3a_exploit/ledger.jsonl` (`kind:"k3_sweep"`) |
| cancellation-plan INFEASIBLE at 87 | 1 | no ≤87-gate circuit in which every cancelling gate has a weight-1 overlap producing AES target row 0 | `e6_cancelplan/ledger.jsonl` (`W1w1_orbit1`) |
| depth-4 exact floors | 11 | 91 is exactly optimal at depth ≤ 4 inside each of 11 named mask alphabets, up to 300 masks | `e4_depth/ledger.jsonl` (`kind:"d4floor"`) |
| `\|Aut\| = 4` proof | 1 | the permutation automorphism group of the MixColumns target set is exactly ρ, order 4 | `e3b_fresh/code/symgf.py` + ledger |
| SAT ladder UNSAT levels | 5 | the joint W3\|U4 block costs > k, for k = 9..13 | `sat_package/ladder/*.cnf` + README table |
| the open instance | 1 | SAT ⟺ 87-gate MixColumns; **status unknown** | `sat_package/k14_joint_W3U4.cnf` (4.2 M) |
| documented UNDECIDED / timeouts | 6 (E4) + 4 (E2) + 2 (E5) + 1 (E8) | brackets, never negatives | the respective ledgers |

### Raw logs
`find <dirs> \( -name '*.log' -o -name '*.out' \)` → ~200 files, **~450 KB total** across the E-dirs (`e_upstream` alone is 210 KB of worker logs). Plus `e9_radius/runs_archive.tar.gz` (592 K, 537 per-run scratch dirs) and 12 zero-byte logs (`find ... -name '*.log' -size 0`) that are the record of deliberately killed or preempted arms.

### Solver instances / model files (regenerable)
| label | count | size | path |
|---|---|---|---|
| E3a dim-8 SAT instances | 5,705 | 23 M | `e3a_exploit/inst/` (`buy_*`, `region_*`, `sector_p88*`) |
| E7 solver instances | 19 | small | `e7_push/inst/` |
| E5 instance bundle | 4 files | 70 K | `e5_readd/inst/` |
| benchmark CNFs (ladder + k14) | 6 | 18 M | `sat_package/`, `sat_package/ladder/` |
| demo CNFs + models | 4 | 5.9 M | `sat_package/demo/` |
| `__pycache__` | 11 dirs | 460 K | across the E-dirs |

---

## 4. KEEP / DELETE proposal

**KEEP — no question**

| item | size | why |
|---|---|---|
| all 10 `RESULT.md` + `_shared/BRIEF.md` + both `NOTEBOOK.md` + `ATLAS_NOTE.md` | ~300 K | the method catalog's primary sources; `BRIEF.md` is the reusable charter |
| all 10 `ledger.jsonl` | 19 M | append-only certificates; every number in every write-up is re-derived from them, and three of them contain results the write-ups do not (§5) |
| all `code/` trees (147 `.py`, 25 `.sh`, `qsearch.c`) | ~2 M | the phase-2 toolkit. `qsearch.c` in particular is a one-file exact searcher with its soundness proofs in the header |
| all 238 circuit/mask-set artifacts | ~600 K | verified or checkable; several are unique (the 105@5, the third 91@4, the 35 89s, the 39 exact-completion 88s, the odd-parity sigma points, the 89 carrying an extinct feature) |
| `e4_depth/out/mindepth_scan*.jsonl` | 6.2 M | the min-depth of 38,711 distinct mask sets — a corpus-wide dataset that cost a 1.8 M-file enumeration and cannot be cheaply reproduced |
| `e4_depth/out/alph/` | 208 K | the 688-mask depth-4 vocabulary with usage counts over 15,912 circuits, and the 2,050-mask 88 vocabulary over 20,854 — inputs to the one live depth lead |
| `e7_push/cubes/*.jsonl` | 320 K | exact-search state: 4,083 finished cubes. This is what makes the region results resumable and auditable per-cube |
| `e6_cancelplan/data/pop_vocab.json` | 107 K | the 4,120-pair saturated cancellation vocabulary — a measured, saturated object |
| `e1_regions/out/*.json` (census, plane-locality, selftests, gauge) | ~200 K | the pre-search measurements that are the actual findings |
| `e9_radius/runs_archive.tar.gz` | 592 K | already compressed; 537 run dirs |
| `sat_package/` entire | 24 M | a submission-ready, checksum-verified package (51/51 OK) for a live open question. **Do not touch until the k=14 question is settled.** |
| all logs, including the 12 empty ones | ~450 K | tiny, and the empty ones are the record of which arms were killed (E6 documents this explicitly so "nobody reads a launch as a result") |

**DELETE-CANDIDATE**

| item | size reclaimed | why | risk |
|---|---|---|---|
| `e3a_exploit/inst/` (5,705 generated dim-8 instances) | **23 M** | pure solver input, regenerated deterministically by `code/buyone.py` / `blocks.py` / `blockpop.py` from the circuits on disk. Every verdict is already in `ledger.jsonl`. This is 92% of E3a's footprint | low — but keep ~5 files as format exemplars, and note that regenerating needs the same circuit set present |
| 11 `__pycache__` dirs | 460 K | build artifacts, and they contain hardcoded absolute paths | none |
| `e2_outputcost/kill_manifest.txt` | 4.5 K | a process-management scratch file from a single session | low; KEEP if the wrap-up wants a record of process discipline |

**KEEP with a note (uncertain)**

- `sat_package/demo/k14_PLANT14.cnf` + `k7_SUB_U4tgts.cnf` (5.7 M): regenerable by `code/make_planted.py` / `gen_cnf.py`, but they are part of a checksummed package. Deleting them breaks `SHA256SUMS`. **KEEP** unless the package is repackaged.
- `sat_package/ladder/*.cnf` (14 M): regenerable from `instance_joint_W3U4.json` via `gen_cnf.py --k N`, but they are the shipped benchmark family and their whole point is being byte-pinned. **KEEP.**
- `e5_readd/ledger.jsonl` (16 M): 72,201 of its rows are one-line-per-drop-set `unsat` records. It could be compressed to a histogram — but it *is* the certificate, and the two `screen_done`/`screen_hist` rows are only meaningful against the full row set. **KEEP; compress with `xz` if disk matters (it will shrink ~20×).**
- `e1_regions/out/parts/sec1-8.md` + `RESULT_draft_notes.md`: superseded drafts of `RESULT.md`. Harmless at 40 K. **KEEP** (they document how the report was assembled) or delete if tidiness matters.

Net easy reclaim: **~23.5 M of 77 M**, all of it regenerable solver input and bytecode.

---

## 5. LEADS (sharp-eye findings)

### L1. E5's drop-4 local-optimality screen COMPLETED on a second 88 family and nobody re-tallied — VERIFIED-IN-LOG
`e5_readd/RESULT.md` §7 says: *"`88fs5` was **left running** … do not quote the `88fs5` numbers in this file, re-tally them."* Nobody did. The ledger says it finished:
```
python3 -c "import json,collections;c=collections.Counter();[c.update([(json.loads(l).get('circuit'),json.loads(l).get('verdict'))]) for l in open('experiments/e5_readd/ledger.jsonl') if '\"drop4\"' in l]; print(c)"
→ {('88d5','unsat'): 36241, ('88fs5','unsat'): 35960}
```
plus `{"circuit":"88fs5","kind":"screen_done","screened":13315,"trivial_counting":22645,"wmax":9}` and its `screen_hist` over all 35,960 sets. **All 35,960 four-target drop sets of the 88-from-scratch@5 are refuted at `k = W−1`, zero improvements, zero timeouts.** The project therefore holds **two** complete drop-4 certificates, not one — and E5 explicitly flagged that `88fs5`'s W-profile is visibly different from `88d5`'s (six `W=9` sets versus one), so family-independence was an open question and is now answered on a second family. This is a publishable upgrade to the strongest local-optimality statement in the corpus, sitting unbanked in a ledger.

### L2. E7's dim-12 tap-region queue COMPLETED — four regions decided, not one — VERIFIED-IN-LOG
`e7_push/RESULT.md` reports **one** decided dim-12 region (88@5 R4) and says region 2 is at "84 of 231 cubes done". The ledger contains **four** `cube_verdict` rows, each `min_gates = 11`, `lower_bound_proven = 11`, `control: POSITIVE`:

| region | cubes | k=10 wall | verdict |
|---|---|---|---|
| `88@5 R4` | 210 | 1,898 s | min_gates = 11 (in RESULT) |
| `88@5fs R4` | 231 | 2,852 s | **min_gates = 11 — not in RESULT** |
| `JEAN88 R4` | 190 | 1,979 s | **min_gates = 11 — not in RESULT** |
| `p88_05 R3` | 210 | 5,549 s | **min_gates = 11 — not in RESULT** |

`region_JEAN88_4_k10.jsonl` has 190/190 cube records; `region_88at5fs_4_k10.jsonl` 231/231; `region_p88_05_3_k10.jsonl` 210/210. So the headline "the first decided dim-12 region in this project" is now four decided dim-12 regions, **including one on Jean's foreign-lineage 88** — which is exactly the independent-lineage test the project wanted. Six of the ten `|B| = 11` regions remain (`88@6 R4`, `88@7 R4`, `p88_00 R4`, `p88_03 R4`, `p88_05 R4`, `p88_07 R4`), each now a measured ~2,000–5,500 s job on a resumable driver.

### L3. E3a's buy-one-save-two sweep completed empty at 4,926 instances — VERIFIED-IN-LOG
RESULT.md lists `buyone` as "still accumulating" with controls fired on "all 8 blocks reached". The ledger holds **4,926 `buyone` rows, verdict `UNSAT_at_nB_minus_2` on every single one, 0 hits**, across all 14 known 88s. Same for `blockpop`: 586 decided blocks (324 `OPTIMAL_AT_nB`, 198 `NOT_COVERED`, 64 `CONTROL_FAILED`, **0 HIT**) against the "counts in the tally" placeholder. And `k3shell` banked **two complete exhaustive remove-3-add-2 certificates** (88@7 and 88fs, 27,720 windows each, verdict `"EXHAUSTIVE: no remove-3-add-2 improvement"`), where RESULT.md records only that the control fired. Three closed questions reported as open.

### L4. `e_upstream` has no write-up, and it holds an 89-gate circuit carrying a feature extinct in all 3.28 M known 88s — VERIFIED-IN-LOG
`e_oddlane3/census.py` measured `|odd(m)| ≥ 3` at **0 occurrences in ~184 M mask slots over 3,280,541 distinct 88-gate circuits**. `e_upstream` then pinned such masks into from-scratch roots and descended. It banked 33 survival floors and stopped. **`S89_41_00000098.json` is 89 gates and carries `0x98` with `|odd| = 3`.** I checked all 33 in-process (realizable from the 32 singletons with 0 unbuildable masks, all 32 targets present, pin present in every one):

```
python3 - <<'EOF'   # from repo root
import json,sys,glob; sys.path.insert(0,'.')
from verify_circuit import mixcolumns_target_masks
T=set(mixcolumns_target_masks())
for fn in sorted(glob.glob('experiments/e_upstream/S*.json')):
    S=set(json.load(open(fn))['masks']); av={1<<i for i in range(32)}; rem=S-av; p=True
    while p:
        p=False
        for m in list(rem):
            if any((m^a) in av for a in av): av.add(m); rem.discard(m); p=True
    print(fn, len(S), len(rem), T.issubset(av))
EOF
→ every file: 0 unbuildable, all targets present
```
Floor distribution: 89×1, 90×3, 91×6, 92×12, 93×6, 94×5. **So the price of leaving the 3,172-word vocabulary is measured at ≤ 1 gate, and the notebook's own reading table says a floor of 89 means "the feature costs 1 gate — a real, quotable number".** Nobody quoted it. Two follow-ups the notebook itself names and nobody ran: (a) convert these to oracle format and verify them — they are stored as `{"masks": [...]}` and `verify_circuit.py` takes gate lists, so **none of the 33 has ever been through the oracle**; (b) the general machine — the notebook lists five more feature classes to price (`|odd| ≥ 4`, the 388 never-seen weight-2 masks in `e_w2novel/candidates.json`, weight ≥ 12, fan-out ≥ 8, the column-parity hubs `T_0,T_3,T_4,T_7` absent from every record 88) and **not one of them was priced**. `e_w2novel` is 2 files: the candidate list and an unrun probe.

### L5. The `e_oddlane3` probe's final log line was never analysed, and it refines the census — VERIFIED-IN-LOG
`e_oddlane3/hunt.out` ends: `DONE. total 88-gate sets with a >=3-odd-lane mask: 4` — four 88-mask sets in the corpus *do* carry the feature. But each is logged `targets=False realizable=False`, i.e. they are **surrogate/transposed states from `campaign_87/wave6.../surrogates_88.jsonl`, not MixColumns circuits**. So the census claim survives intact — but the refinement (the only 88-mask sets carrying the feature are non-circuits) is written nowhere, and the radius-1 pin probe's own result (14 workers × ~76 candidates, **every one → 89**) is also unwritten. The notebook itself predicted this: a radius-1 probe from an 88 "can only ever answer 89". Combined with L4: the region is reachable at 89 from upstream and unreachable at 88 by editing, which is precisely the "construct into it rather than edit toward it" conclusion nobody drew.

### L6. Three published atlas negatives are still standing, uncorrected — VERIFIED-IN-LOG
E3a found and E7 independently reproduced (with two exact engines cross-checked) that `atlas/thinktank/basin/b9b_sweep.py`'s "free structural control" tests the wrong predicate, so three of its 23 published `ctl=OK exhaustive` lines (88@5 S0, 88@7 S0, 88@8 S0) are vacuous negatives. E7 wrote a paste-ready correction with a proof of the convex-closure repair. **It was never pasted:** `atlas/thinktank/ideas_basin_atlas.md` is dated Aug 18 01:05 — before E7 ran — and `command grep -c convex atlas/thinktank/ideas_basin_atlas.md` returns **0**. The correction is a five-minute edit; the sharpened statement is that all three blocks land on exactly `|B| + 1`, so "the scoped space is one gate too poor to reproduce the circuit that already exists".

### L7. E2's post-write-up campaign2 burned 16.7 hours for zero decisions, and it is the same wall E8 hit — VERIFIED-IN-LOG
`e2_outputcost/campaign2.log` ran to `CAMPAIGN2 DONE 06:07:03`: **40 of 40 dim-12 quad classes returned `status=timeout` at ~1,565 s each, 60,010 s elapsed, cost=None on every one.** No new n=4 exact costs. Coverage did grow slightly (my re-tally: n=2 decided 274 → 278, n=3 140 → 165), so the RESULT.md coverage table is stale, but the headline is a measured negative: **dim 12 at k≈24 is out of reach of the generic SAT oracle**, exactly as E8 §6 reported for its own dim-12 orbit (bracket `[11,18]`, k=11 budget-expired at 122.7 M nodes). Two instruments, same wall, same cause (`dist[]`/delta table is `2^dim`). E8 names the fix — replace the `2^dim` pass with a lazily evaluated bound over the ≤20 available masks — and it is the single change that would open orbits 1, 3, 4.

### L8. E6's headline artifact was never saved to disk — SMELL (artifact loss)
E6's flagship result is a **verified 88-gate depth-5 circuit (66 CF + 22 cancelling) synthesised from a 796-pair vocabulary with the child↔overlap assignment free**. `e6_cancelplan/found/` is **empty**. The circuit exists only as the string `A_oracle: "gates=88 depth=5 outputs_built=32/32 problems=0\nVERDICT: VALID MixColumns circuit"` inside one ledger row. The same is true of every stage-B control circuit (111 g, 110 g, 109 g, 112 g, 108 g). Regenerable in principle (`code/popcfg.py run --modeA merged --budget 88 --hint-circuit ...`) at ~3,762 s, but nobody knows it is missing.

### L9. Two named, cheap, decisive tests that were designed and never run — PLAUSIBLE
- **The plane-locality theorem test.** E1 §8.4: every one of the 1,136 masks of every verified circuit on disk, and every valid single-mask repair of the 88@5/89@5/92@4 anchors, is inside a **12,946-element** subset of the 2^32 mask space. Its own proposed decisive test is one sentence long — *"hand `atlas/slp_opt.py` an 87-gate instance restricted to plane-local masks: UNSAT there would be a real theorem about a 12,946-mask space instead of a 2^32 one."* Never run. It is the cheapest route in the slice from a corpus regularity to an actual theorem.
- **The bit-7 carry-gate prefix.** E2 §8.3: the only genuinely high-order sharing in every one of nine verified circuits is 2–3 weight-2 masks on bit 7, forced by the reduction polynomial `0x11B`, present even in the 97@3. Fixing them as a forced prefix and searching the remainder is "a legitimate, never-tried restriction, and unlike most restrictions it has direct evidence of being satisfied by every known optimum". Never run.

### L10. The 92@4 anchor is a trap nobody resolved — VERIFIED-IN-LOG, mechanism unknown
E4: **0 of 9** depth-capped restarts from `evidence/circuits/mixcolumns_92gates_depth4.json` reached 91, while the project inventory records that exact step as a four-minute result. E9 independently reproduced it: `CAL1_92to91_d4`, **0/3 descents at 300 CPU-seconds each**, and chased the citation — `TOPOLOGY.md`'s "91@4 in four minutes" describes a **from-scratch `naive+anneal3` descent to the frontier**, not a one-gate improvement of the 92 on disk. So the "depth is soft" premise rests on a step that two independent instruments cannot reproduce. E4 priced resolving it at 30 minutes and nobody spent them. E9's version of the same observation is arguably the strongest surviving strategic signal in the slice: **cold restarts reach the frontier, local search cannot cross it**, and the comparison nobody has run is N core-hours of `ladder_parallel` cold roots against N core-hours of frontier-local search, scored on distinct frontier circuits found.

### L11. The most informative undecided rung in the depth lane — PLAUSIBLE
E4's `MIX_d4pop300_pop88_400`: 554 masks, **175 of which no depth-4 circuit on disk uses**, TIMEOUT at 1,792 s. That is the direct test of E4's own constructive instruction ("a 90 @ 4 needs a mask outside the measured vocabulary — inject masks the depth-4 population has never used and re-run the exact floor"), and E4 names it as *"the run to re-launch first on an uncontended box"*. The decidable frontier of the ladder was measured at 300–600 masks on a contended box; this rung is at 554. Alphabets are on disk (`e4_depth/out/alph/`).

### L12. Three exact values bounded but not pinned, and one open bracket — VERIFIED-IN-LOG
E5 §7: `orbit4_seed9_78_rlx ∈ [10,16]`, `orbit1_seed9_79_rlx ∈ [9,15]`, `orbit5_seed9_80_rlx ∈ [9,13]` — witness searches timed out at 5,141 s each, logged `timeout`. Their 87 questions are all closed, so nothing depends on them; noted only so they are not mistaken for refutations. E5 also records a **solver-free lower-bound idea it never used**: projecting the available set `A` onto the orbit's support coordinates is a linear map, so the exact cost of the projected dim-8/12 instance is a valid *lower bound* on the real dim-32 re-add cost. That would give bounds for drop sets currently out of reach, for free.

### L13. Drop sets of size 2, 3, 5, 6, 8 are untouched and now cheap — PLAUSIBLE
E5's free-gate reduction works for **any** target subset, and E5 names the next rung explicitly: a `W`-for-`W−1` refutation at `W = 12` (two orbits) would be a **radius-23 local-optimality certificate, far beyond anything in the corpus**. Cost is measured (~4 s at k=6, ~400 s at k=8, ~1 hour for a whole circuit's screen). Nobody ran it.

### L14. The odd sigma half was re-priced and the re-pricing changes the strategy — VERIFIED-IN-LOG
E3a pushed the odd half to 91 and read it as "one gate short". E7 showed a σ-closed cost is `2a + b`, so the odd half contains **only odd costs** — below 91 the next value is **89**, a *two-gate* move, and this project has never made a one-gate move at this scale. Measured over 5,728 σ-closed states across 10 arms: **not one even cost appears**, 0 rebuild failures. E7 also found that "use a wider neighbourhood" is measurably wrong here — the complete single-orbit repair walk runs at **47 it/s** and is the only instrument that has ever descended two gates inside the half, while a destroy/rebuild LNS runs at **1.2 it/s** and did not descend at all.

### L15. One lower-bound route was closed cheaply, and the closing is worth copying — VERIFIED-IN-LOG
E7 §3(f): `δ(m) = hi(m) ⊕ lo(m)` is linear and σ-invariant, so the distinct nonzero δ-values of a σ-closed circuit form a valid **dim-16** SLP for `δ(targets)`, giving `cost = 2a + b ≥ 2·SLPmin₁₆ + 1`. It looked like the first real lower-bound handle on a sector with no theorem — and a verified greedy witness gives `SLPmin₁₆ ≤ 26`, so the argument can never certify more than ≈53 against the 89 it would have to decide. **Dead on arrival, closed by one measurement, no solver time, logged as `kind: route_closed`.** That pattern — compute an upper bound on your prospective lower bound before building the machinery — is the cheapest method in the whole slice.

---

## 6. HAZARDS

1. **`fleet11/laneCUBE/` is live and `sat_package` points at it.** `sat_package/README.md` §9 says the k=14 cube count "moves as the sweep runs; re-tally `fleet11/laneCUBE/cubes/joint_W3U4_k14.jsonl` before quoting it". Nothing in my slice writes there, but the package's honesty note is only correct while that lane is untouched. Also `SUBMISSION_NOTES.md` §4.9: **if the live campaign returns a verdict on k=14, the package's §3 description goes out of date, and a SAT verdict turns it from a benchmark submission into a result announcement.**
2. **`sat_package/` is checksum-pinned.** `SHA256SUMS` covers 51 files and currently verifies clean (`sha256sum -c SHA256SUMS` → 51/51 OK). Moving, renaming, recompressing or regenerating any file inside it breaks the manifest. `code/{sat_compile,inst16,cube16}.py` and `verify_circuit.py` are **unmodified `cp -p` copies** of live-campaign files taken 2026-08-28, deliberately pinned so later drift is visible — do not "de-duplicate" them against their originals.
3. **`sat_package/code/sat_compile.py` resolves its working directory from its own location** so the copy writes only inside the package. Moving that file relative to the package would let it write into the running campaign's directories.
4. **Hardcoded absolute repo paths are pervasive.** `command grep -rl '/home/joebachir20/xor_ui/slp-plateau-search' <slice>` matches **~60 files**, including `e5_readd/code/kern.py` (`ROOT = "/home/joebachir20/xor_ui/slp-plateau-search"`), `e3a_exploit/code/{blocks,blockpop,buyone,k3shell,kern,orbit_odd,plansize,spread}.py`, `e6_cancelplan/code/cpk.py`, `e7_push/code/{convex,cube,kern,orbit_odd,sigma_odd}.py`, `e8_quad/code/{assemble,decode,familycurve,firstgates,instances,runquad,validate}.py`, `e4_depth/code/{d4decide,d4floor}.py`, `e_oddlane3/census.py`, and ~15 `.sh` drivers. **Moving the repo root, or any of these directories, breaks all of them.** The ledgers also embed absolute paths.
5. **Everything in `code/` reaches sideways into `pipeline/`, `atlas/`, `evidence/`, `beat88/`, `campaign_87/`.** Every experiment `sys.path.insert`s `pipeline/` and imports `engines` / `mixcolumns_core`; the exact experiments import `atlas/slp_opt.py`; E5/E6/E7 resolve circuits through `evidence/circuits/*.json` by name. Reorganising *those* directories breaks this slice even if the slice itself is untouched.
6. **`e7_push/cubes/*.jsonl` is live search state, not a log.** The cube driver resumes from it. Deleting or truncating any of the 21 files silently discards up to 5,549 s of CPU per level and would make a re-run report a *different* completed-cube count.
7. **Ledgers are the source of truth and several disagree with their own RESULT.md** (§5, L1–L3, L7). Any wrap-up text quoting a RESULT.md number for E2/E3a/E5/E7 must re-tally first. Each directory ships the re-tally script (`code/tally.py` or `code/report.py`).
8. **`e6_cancelplan/code/orbitcfg.py` is written but never run** (RESULT.md §7 says so explicitly, "ready for the next session"). Do not read its existence as a completed arm.
9. **`e_oddlane3/census.py` streams 460 files / 3.9 GB.** Re-running it is a 393-second I/O-heavy job — do not fire it casually on a loaded box.
10. **`e5_readd` hazard note that applies repo-wide:** `pysat`'s `Cadical195.interrupt()` raises `NotImplementedError` in the installed build and `solve()` does not release the GIL, so **an in-process wall clock on a pysat CaDiCaL solve silently never fires**. One worker ran 47 minutes past a 3,600 s "timeout". Any experiment reusing `atlas/`-style in-process timeouts should treat its own timeouts as unenforced until checked.
11. **`nice` is fatal on this box, not polite** (E9): at `nice -n 10` under load ~39 a worker received 1.4% of one core. Wall clock is not a budget here; use `/proc` CPU-seconds.

---

## 7. GAPS

- **I did not re-run any `tally.py` / `report.py`.** All my re-tallies (L1, L3, L7, and the E7 cube counts) are direct `json.loads` scans of the ledgers, which is why I quoted the exact commands. The official scripts might slice differently — in particular E3a's `tally.py` may exclude arms I counted.
- **I could not oracle-verify the 33 `e_upstream` floor circuits.** They are stored as `{"masks": [...]}` and `verify_circuit.py` accepts gate lists (index pairs or mask triples). My in-process check (realizable from the 32 singletons, all 32 targets present, pin present) is sound but is **not** the independent oracle. Converting them is a few lines; I did not, because this wave is read-only.
- **I spot-verified only three circuits** with `verify_circuit.py` (`e8_quad/artifact_family_optimal_circuit.json` → 105@5 VALID; `e5_readd/found/E5_88d5_orb0_sub_k5.json` → 88@5 VALID; `e7_push/found/sigma_91gates_depth7_fixed13.json` → 91@7 VALID). The other 235 artifacts are taken on the strength of their ledger `oracle_ok` / `oracle` fields; bulk re-verification is out of budget.
- **I did not determine whether `e_upstream`'s job list ran to completion.** `deep_jobs.json` describes ~190 jobs; 16 worker logs exist and end with `worker N done`, and 33 floors were banked. Whether 33 is the full yield or a partial one I cannot tell from the logs, which do not carry a job counter.
- **I did not measure how much of E3a's `blockpop` coverage is redundant.** 586 blocks decided over a sampled population of 78,281 states; the ledger does not obviously record which states were sampled, so I cannot say how many distinct circuits those 586 blocks came from.
- **The `e3a_exploit/inst/` deletion recommendation is not regeneration-tested.** I inferred regenerability from the file naming and the generating scripts; I did not re-run a generator to confirm byte-identical output.
- **E6's missing circuits (L8) may exist elsewhere.** I searched only `e6_cancelplan/`. If a sibling directory or a `fleet*` lane captured them, the artifact is not actually lost.
- **`e_w2novel` I could not assess at all beyond its file list** — 388 candidate weight-2 masks and an unrun probe, with no notes, no log, and no ledger. Whether the candidate list was ever validated against the corpus I cannot tell.
- **I did not read `sat_package/code/cube16.py` or `sat_compile.py` in full** (25 K and 13 K of live-campaign code copied verbatim). My generality assessment of the package rests on the README's own account plus the checksum verification, not on reading those two files.
