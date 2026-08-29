# Slice report: campaign_87

Agent model: Claude Opus 5 (1M context). Date: 2026-08-29.

**Summary.** `campaign_87/` (29 GB, 94,014 files, 25 top-level subdirs, entirely
gitignored) is the *whole* 87-hunt before the fleet campaigns: six waves run
2026-07-26 → 2026-08-13, plus a long-shot ideation round, plus the campaign's
publication draft. It is not one campaign but six stacked ones, and the later
ones repeatedly *retract* the earlier ones — the single most important thing to
carry forward is not any negative result but the **control methodology** that
priced the negatives at likelihood-ratio ≈ 1.00. Best verified anywhere in the
slice: **88 gates**; no 87 was ever found, and four files named `*87gates*` are
all deliberate tripwire fakes (`fake87`, `badfail`, `FAILED_87`) confirming the
export path rejects a bogus record. Disk is dominated by regenerable data:
**13.71 GB of `*.pop.jsonl` harvest dumps, 5.53 GB of CNF, 1.51 GB of `.bin`,
1.39 GB of vendored venvs/PyPy/ABC builds** — roughly **24 GB of the 29 GB is
deletable or re-derivable, and under ~1 GB is genuinely irreplaceable.** The
slice is completely cold (no file modified since 2026-08-13; no live process).
Its highest-value contents are: the certified depth-3 lower bound
**N_depth3 ≥ 80** (wave 6, exact rational certificate), the **order-free fence
encoding** (the only certificate class in the project without the slot-order
caveat), the **obstruction no-go analysis**, the **publication draft +
claims audit**, and a set of **finished-but-never-read exact ledgers** that
silently complete frontiers the campaign's own FACTS.md still lists as open.

---

## 1. INVENTORY

### 1.1 Top level

```
du -sh /home/joebachir20/xor_ui/slp-plateau-search/campaign_87   → 29G
find campaign_87 -type f | wc -l                                 → 94014
```

| subdir | size | what it is | documented? |
|---|---|---|---|
| `wave5_2026-08-04/` | 15G | wave 5: the five-track campaign + six-agent meta-review + `burn/` (20 sub-tracks) + the publication draft | yes, heavily (271 `.md`) |
| `tri_hunt/` | 5.1G | three-seed supervisor/worker hunt (2026-07-30/31) | yes (README/REPORT/STATUS/FINAL_STATUS) |
| `agents/` | 3.2G | waves 1–4: 28 agent dirs, per-agent `REPORT.md`, rolled up in `SYNTHESIS.md` | 24/28 |
| `wave6_2026-08-11/` | 1.5G | wave 6: the final wave (T1–T5, A1–A12), ends at campaign shutdown | yes (83 `.md`) |
| `hunt87_layer89/` | 1.3G | exact shell sweep of the whole 89-gate layer | yes (`REPORT.md`) |
| `hunt87/` | 1.1G | the original multi-day 87 hunt (supervisor + detector) | yes |
| `global_vocab/` | 1.1G | long-shot: global vocabulary harvest + min-union LP/CP-SAT bound attempt | only in `LONGSHOT_RESULTS.md` §2 |
| `d3_sat/` | 126M | depth-3 SAT ladder (early) | opaque |
| `d3_model/` | 115M | depth-3 structural model / harvest | opaque |
| `novelty/` | 94M | vocabulary-diverse ROOT library + descent | partial (`roots/README.md`) |
| `families16/` | 69M | the "16 families" clustering (later retracted as a greedy artifact) | opaque |
| `prior_basins/` | 34M | long-shot: 10 published circuits imported as fresh basins | `LONGSHOT_RESULTS.md` §4 + 2 `PROVENANCE.md` |
| `dual_transpose/` | 30M | long-shot: transpose duality, XOR-count(M)=XOR-count(Mᵀ) | `LONGSHOT_RESULTS.md` §1 + `DUALITY_VERIFICATION.txt` |
| `hunt87_depth4/` | 24M | depth-4-capped hunt | opaque |
| `hunt87_basin4/` | 16M | basin-4 hunt | opaque |
| `d3_exact/` | 3.3M | exact depth-3 enumeration | opaque |
| `hunt87_depth5/` | 2.2M | depth-5-capped hunt | opaque |
| `cascade6/` | 1.1M | independent from-scratch provenance-clean cascade | yes (README/STATUS/PROVENANCE) |
| `cert_audit/` | 516K | long-shot: **the control audit** that reprices every certificate | `LONGSHOT_RESULTS.md` §3 (repo commits 23d80d7, 73ad7ee) |
| `base/` | 236K | shared seeds (`base/seeds/IMPORTED_88.json` etc.) | — |
| `prov_d5fs/`, `hunt87_prov/`, `hunt87_prov5/` | 200K/16K/12K | provenance re-derivations of specific circuits | opaque |

Top-level documents (all worth keeping, all cross-referencing each other):
`FACTS.md` (26K — *the* single source of truth for repo prose, fact-by-fact
sourced), `SYNTHESIS.md` (26K — running roll-up of waves 1–4),
`LONGSHOT_RESULTS.md` (17K — the long-shot round + a **12-item ledger of
retracted claims**), `PUBLICATION_BRIEF.md` (21K), `V3_AUDIT.md` / `V31_AUDIT.md`
(release audits), `FINAL_REPORT.md`, `REPO_BRIEF.md`, `BRIEF.md`.

### 1.2 File-type breakdown (whole slice)

```
find . -type f -printf '%s %p\n' | awk '{n=split($2,a,"."); e=(n>1?a[n]:"NOEXT"); s[e]+=$1} END{...}' | sort -rn
```

| class | count | bytes | note |
|---|---|---|---|
| `*.pop.jsonl` (harvest dumps) | 130 | **13.71 GB** | one circuit state per line; pure stochastic scratch |
| other `*.jsonl` | 2,851 | **4.77 GB** | mixes ledgers (unique) with pools/populations (scratch) |
| `*.cnf` | 871 | **5.53 GB** | solver input dumps, all regenerable |
| `*.bin` | 4 | **1.51 GB** | `global_vocab/states_uniq.bin` 1.10 GB + `hunt87_layer89/pool/layer89.bin` 445 MB |
| `*.npy` | 6 | 0.51 GB | `alphabet_ladder/work/corpus_index/post.npy` 400 MB (rebuildable index) |
| venvs / PyPy / ABC / kissat builds | — | **1.39 GB** | vendored third party |
| `*.json` | 59,485 | 0.18 GB | mostly individual circuit files |
| logs (`.log/.out/.err`) | 5,004 | **405 MB** | wave5 alone: 3,355 files / 227 MB |
| `.md` writeups | 412 | — | 36 `REPORT.md`, 63 `STATUS.md`, 38 `README.md` |
| `__pycache__` / `.pyc` | 722 dirs | 66 MB | |
| project `.py` (non-vendored) | 3,130 | 117 MB | |

Verified circuit files: 20,745 filenames contain `88gates`, 588 `89gates`,
305 `92gates`, 196 `97gates`, 57 `90gates`; **2 contain `87gates` and both are
selftest fakes.** 171 files match `BREAKTHROUGH*.json` (53 × 89, 45 × 88, 15 ×
90, rest are 97–127-gate selftest artifacts).

### 1.3 Headline circuits re-verified in this session

```
python3 verify_circuit.py <path>          # from repo root
```
| path | result |
|---|---|
| `campaign_87/agents/merged-engine/BREAKTHROUGH_88gates_depth7.json` | VALID — first search-found independent 88 (family 2) |
| `campaign_87/agents/hunt-deeper/BREAKTHROUGH_88gates_depth8_THIRDFAMILY.json` | VALID — family 3 |
| `campaign_87/agents/lit-88/IMPORTED_88.json` | VALID — Jean's 88 (family 1) |
| `campaign_87/wave5_2026-08-04/burn/obstruction/counterexample_87_weight184.json` | **INVALID (by design)** — an 87-gate circuit with MixColumns' exact weight/rank profile that is *not* MixColumns; it exists to kill weight-accounting obstructions and must never be reported as a MixColumns circuit |

### 1.4 Prior-art PDFs (explicit ask)

```
/home/joebachir20/xor_ui/slp-plateau-search/campaign_87/agents/lit-88/jean_eprint_2026_1481.pdf
    236,797 bytes — J. Jean, ePrint 2026/1481, the independent published 88
/home/joebachir20/xor_ui/slp-plateau-search/campaign_87/agents/lit-88/sunyangli_eprint_2025_1493.pdf
    318,566 bytes — Sun–Yang–Li, ePrint 2025/1493, the 89
```
These are the only two PDFs anywhere under `lit-88/`. The dir is 212 MB because
`lit-88/venv/` is 210 MB (Playwright's bundled Node binary is 117 MB, plus
`curl_cffi` 29.5 MB and `cloudscraper`) — installed because eprint.iacr.org was
Cloudflare-blocked (`lit-88/fetch_jean.py`). No browser profile, no page cache.
The transcribed circuits are `agents/lit-88/IMPORTED_88.json` (1,367 B, 88@7,
provenance field states explicitly "This is Jean's circuit, NOT a result of this
project's search") and `agents/lit-88/IMPORTED_89_sunyangli.json` (1,302 B),
both copied to `base/seeds/`.


---

## 2. METHODS

44 distinct methods. Paths are relative to `campaign_87/` unless noted. Every
"measured performance" line is from the named log/result file. **Read §5 LEADS
before reusing any negative result from this slice: the campaign's own controls
(cert-audit, alphabet_ladder, fence_sat, metareview/optimality) measured most of
the negative instruments at likelihood ratio ≈ 1.00 about the existence of an
87.** Repo-wide context: the record is 88; no 87 exists anywhere in this slice.

### A. Stochastic search engines (walk / LNS / fleet)

#### hunt-fleet-supervisor
- Family: plateau-search / fleet infrastructure
- What it does: one supervisor process launches 6–16 heterogeneous search workers, each on its own seed circuit and knob profile, restarts them with a rotated RNG seed when they die, regenerates a `STATUS.md` every 10 minutes, and shuts the whole fleet down when a `STOP` file appears. Every worker appends the distinct equal-best mask sets it visits to its own `.pop.jsonl` harvest file.
- Twist vs siblings: PID-file process control that verifies `/proc/<pid>/cmdline` mentions the directory before signalling — `pkill` is banned by name in the README because it destroyed sibling work twice on this box.
- Measured performance: `hunt87/supervisor.out` — 19.74 h, 16 workers, best 88@5, 148,347 new distinct 88 states, 198/198 MAP-Elites cells occupied, no 87. `tri_hunt/supervisor.out` — 5.27 h, 10 workers, best 88@5, 15,897 new 88 states, no 87.
- Cost: ~14 of 20 cores; 19.7 h and 5.3 h respectively.
- Code: `hunt87/supervisor.py`, `hunt87/hunt_worker.py`, `tri_hunt/supervisor.py`, `cascade6/supervisor.py`
- Logs/results: `hunt87/status.log` (478K), `hunt87/supervisor.out` (156K), `tri_hunt/status.log` (178K)
- Generality: CIRCUIT-GENERIC (targets come from `mixcolumns_core.py`)
- Phase-2 verdict: keeper — this is the harness every later fleet inherits.

#### merged-engine (walk + LNS with all wave-1 fixes)
- Family: plateau-search
- What it does: the campaign's production search engine — a neutral-drift walk over equal-size mask sets plus large-neighbourhood search (destroy k masks, greedily rebuild), with a Pareto depth tie-break, plateau harvesting and 120 s cross-pollination between sibling workers.
- Twist vs siblings: it is the *merge* of seven separately measured wave-1 improvements (below), which together took the walk from ~70–110 to 480–640 iterations/s.
- Measured performance: **found the project's first independent 88 @ depth 7** at t = 1,973 s from the ρ²-symmetric 94 seed (`agents/merged-engine/runs_hunt/w10_sym94.log`); an 8,400 s × 10-worker hunt harvested **84,989 distinct verified 88-gate mask sets**; no 87 in the remaining 6,400 s.
- Cost: 8,400 s × 10 workers ≈ 23 core-hours.
- Code: `agents/merged-engine/work/engines.py`
- Logs/results: `agents/merged-engine/runs_hunt/*.pop.jsonl` (611 MB), `BREAKTHROUGH_88gates_depth7.json`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — the reference engine.

The seven measured improvements inside it, each its own method with its own A/B
(all from `agents/<name>/REPORT.md`, all cross-checked for bit-identical
trajectories or oracle-verified equivalence):

| method | code | measured effect |
|---|---|---|
| **relax-kernel** (level-BFS depth relaxation, realizability-only closure) | `agents/relax-kernel/` → `work/engines.py:43-127` | **17.5× end-to-end LNS** (42.3 → 739 it/s); bit-identical 1,500-iteration trajectories vs baseline |
| **closure-kernel** (worklist/BFS closure, incremental `remove_query`, improve-only-on-change) | `agents/closure-kernel/harness.py` | **21.9× walk** (12.3 → 269 it/s); root cause was an improve-spam bug costing 78% of runtime |
| **victim-repool** (destroyed masks stay in the pool at cost class 3) | `agents/lns-extract/` | **~34× accepted moves/s**; makes 100% of iterations feasible (was 1.2%) |
| **coneinj destroy** (connected-cone victims + injected candidates) | `agents/lns-destroy/work/lns_lab.py` | **~12× improvements/s**; the only operator making destroy size 3–4 productive |
| **exact `_repair`** (complete enumeration of `{v^a : a ∈ closure(S2)}`, \|C\|≈7) | `agents/repair-move/` | **~7× plateau mobility** (1.9 → 13.6–16.3 distinct states/s); complete enumeration is *cheaper* than 24–40 random tries |
| **scored hot-multiset pool + peel cache** | `agents/lns-pool/work/engines_pool.py` | **~11× accepted moves**, 16–18× pool hit rate |
| **SA-with-reheat acceptance** | `agents/acceptance-schedule/` | **~2× drift** (best of SA/RRT/LAHC/kicks; LAHC provably inert) |

#### depth-capped-worker
- Family: plateau-search variant
- What it does: the same walk/LNS engines but with a hard depth cap threaded into both the engine and the worker context, so the search only ever visits circuits realizable at depth ≤ D.
- Twist vs siblings: the cap flows into the *depth fixpoint*, not just a post-filter, plus a root-feasibility guard.
- Measured performance: `tri_hunt/REPORT.md` §3.3 — cap-4 workers hold 92@d4 and cap-5 holds 88@d5 while uncapped siblings on the same seed drift to depth 5–7. `agents/hunt-88at6` ran a cap=6 fleet for 13,500 s × 6 workers and never reached 88 at depth ≤6.
- Cost: `hunt-88at6` ≈ 22 core-hours.
- Code: `tri_hunt/hunt_worker.py --cap`, `agents/hunt-88at6/work/cap_worker.py`
- Logs/results: `tri_hunt/runs/c4_*.pop.jsonl`, `agents/hunt-88at6/runs_cap6/`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper for frontier work (a depth-capped record is a separate Pareto point), dead for the 87 hunt.

#### cross-pollination (sibling harvest merge)
- Family: plateau-search / population
- What it does: every LNS worker periodically globs its siblings' `.pop.jsonl` harvests and merges their masks into its own rebuild candidate pool.
- Twist vs siblings: it is **provenance-contaminating** — `hunt87` deliberately ran it OFF because two of its anchors descend from Jean's published circuit; `tri_hunt` ran it ON because all three of its roots are own-lineage.
- Measured performance: `tri_hunt/FINAL_STATUS_2026-07-31.md` — 3,651 merges pulling 1,072,997 masks. Raising the shallow lanes' harvest cap took merge traffic from 280 masks/10 min to 927 masks per event across 14 sources. **In both record events the LNS chunks never improved the best** — every improvement came from walk chunks (`FACTS.md` §2–3), so cross-pollination's measured contribution to a record is zero.
- Code: `_Harvester.merge_into` in `*/engines.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: superseded — high provenance cost, no measured record contribution. `cascade6` turns it off on purpose.

#### map-elites-archive (structural novelty archive)
- Family: plateau-search / diversity
- What it does: a 2,500-cell archive indexed by (3 family-distance axes × ρ²-symmetry × gate band) computed on the *periphery* (non-target, non-input masks). An empty cell will buy a circuit up to **+6 gates worse** than the archive best.
- Twist vs siblings: the +6 exchange rate is not arbitrary — it is exactly what the ρ²-symmetric 94 cost over the 88 it eventually produced.
- Measured performance: `hunt87/STATUS.md` — 198/198 cells occupied, 4,375 expansions, 387 improved in place, best elite 88 gates.
- Code: `hunt87/archive.py`, `hunt87/explorer.py`
- Logs/results: `hunt87/archive/elites.jsonl` (237K — full mask set per occupied cell)
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — the cheapest diversity mechanism in the tree.

#### basin-diversity harvesting (repel knob)
- Family: plateau-search / diversity
- What it does: adds a repulsion penalty against a reference mask set so the walk is pushed away from known basins, then harvests everything it visits.
- Measured performance: `agents/basin-diversity/REPORT.md` — 356 distinct new 89 mask sets (vs 4 previously known), min Jaccard to known 89s down to 0.107; recombination produced a verified hybrid 90@7 in no known basin. Also: the **universal core of all ≤91 circuits is the 32 targets plus exactly one mask** (`0x40400000`).
- Code: `agents/basin-diversity/work/`, later `repel_file`/`repel_pen` knobs in `hunt-deeper`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper.

#### ρ²-equivariant orbit search
- Family: plateau-search in a quotient space
- What it does: searches in the 53-dimensional orbit space of the half-rotation ρ² instead of the 32-dimensional mask space, so every move is symmetric by construction and the dimensionality halves.
- Measured performance: `agents/orbit-ladder/REPORT.md` — ~100 it/s (≈20× the naive orbit search); improved the best *exactly ρ²-symmetric* circuit from 94 to **two independent 90s**; both machine-certified locally optimal in orbit space. Its ρ²-symmetric 94 and 90 seeds are the ancestors of **both** search-found 88 families. But `wave5/CAMPAIGN_VERDICT.md` §5 stopped it with formal cause: "structurally confined to a region no record circuit occupies" (the symmetric sector floors at 90).
- Code: `agents/orbit-ladder/work/engines_closure.py`, `agents/orbit-ladder/work/engines_relax.py`, `wave5/burn/oddparity/o2lib.py`
- Generality: MC-HARDCODED (ρ is a symmetry of *this* matrix); a different circuit needs its own automorphism computed first — and `wave5/burn/obstruction/t4_automorphisms.py` shows how (Aut(M) = ⟨ρ⟩, order exactly 4).
- Phase-2 verdict: keeper as a *seed generator*, dead as a search space.

#### syl-move (out-degree-1 subsequence replacement)
- Family: plateau-search / literature-derived move
- What it does: implements Sun–Yang–Li's move — find a maximal chain of signals each used exactly once, delete it, and exactly re-synthesize it — generalized here to closed cones over out-degree ≤2/≤3.
- Measured performance: `agents/syl-move/REPORT.md` — produced the **first-ever drift on Jean's 88 plateau**: 26 distinct verified 88-gate mask sets (symdiff 2–6 from Jean's), plus 183 distinct 89 sets. No improvement to any seed.
- Code: `agents/syl-move/work/syl_move.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — the only move that unfroze a plateau the standard move set could not touch.

#### nrpa (nested rollout policy adaptation)
- Family: constructive stochastic tree search
- What it does: the only *constructive* paradigm in the campaign — builds circuits gate by gate under a learned 9-feature linear policy over candidate masks, rather than repairing complete circuits.
- Twist vs siblings: every other method here operates on complete circuits.
- Measured performance: `wave5/nrpa/out/STATUS.md` — 476,017 episodes at 37.1 rollouts/s, **best verified 88**, 1,441,779 distinct ≤92-gate sets, 1,400,343 distinct 88s all at min depth 7. Crucially: with an unrestricted vocabulary (`free`/`open` modes) it only reached **101 and 99** — the learned policy needs the harvested V88 prior to get anywhere.
- Cost: 161,740 s = 44.9 core-hours on one core.
- Code: `wave5/nrpa/nrpa.py` (40K, single file)
- Logs/results: `wave5/nrpa/out/sub92.jsonl` (1.45 GB / 1,441,779 lines)
- Generality: CIRCUIT-GENERIC in form, MC-HARDCODED in its prior (`h(m)` weights are hand-tuned for this target set)
- Phase-2 verdict: keeper for a new circuit — it is the only method that can start from nothing, but it must be given a vocabulary.

#### evolve (LLM-authored operator population)
- Family: meta-search
- What it does: a population of ~27 search-operator *programs*, each a Python file, evaluated by the mean endpoint of the descents it produces, with new individuals authored as mutations of the winners.
- Measured performance: `wave5/evolve/STATUS.md` — 407 valid descents, endpoint distribution 88:9 89:74 90:183 91:115 92:19 93:4 94:3; best individual `j_alg_99272` at P(≤88) = 0.04. Independently refuted the root-cancellation hypothesis at n=180.
- Code: `wave5/evolve/evolve_loop.py`, `wave5/evolve/pop/*.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — it was the author's designated survivor, and it was right about roots when a hand-run experiment was wrong.

#### fresh-fleet from-scratch descent (the E1 experiment)
- Family: plateau-search, run as a *statistical experiment*
- What it does: 8 lanes generating random roots and descending them to a local optimum, logging every endpoint, until a pre-registered sample size is reached.
- Twist vs siblings: it is not a hunt, it is a **power measurement** of the whole descent operator class.
- Measured performance: `wave5/fresh_fleet/FINAL_STATE.md` — **1,500 from-scratch descents; endpoint law 88:52 89:375 90:575 91:359 92:101 93:21 94:12 95:5; 0 reached ≤87.** P(87 per descent) < 2.00e-3 at 95%; **P(87 | reached 88) < 0.056 at 95%**; a continuing-decay model needs 31 88-arrivals and 52 were observed, so decay is **rejected at 99%** — the operator class has a wall at 88.
- Cost: 4 days, most of the box; 5.06 GB of harvest.
- Code: `wave5/fresh_fleet/supervisor.py`, `engines.py`, `e1_analysis.py`
- Generality: CIRCUIT-GENERIC — and this is the single most reusable *experimental design* in the slice.
- Phase-2 verdict: keeper (as methodology). It is what let the campaign price its own search class instead of guessing.

#### steinberg / transvection word search
- Family: group-theoretic search
- What it does: represents the circuit as a word in the Steinberg presentation of SL(32+r, 2) and rewrites it using the group relations, so the move set is defined by algebra rather than mask arithmetic.
- Twist vs siblings: this was the ideation round's #1 unrun idea precisely because its failure mode was not already measured.
- Measured performance: **killed by a cross-instrument control.** `wave5/steinberg/STATUS.md` — from the *identical* 97-gate anchor the repo's own walk descends 97 → 92 in 83 s, while the Steinberg search returns **+0** after 250k–400k iterations across three move classes and multiple seeds. Power floor confirmed (`mixed` recovers all 8 planted dead gates, 96 → 88). Theory: under the projection `w ↦ V(w)` the entire cost-neutral part of the move set collapses to a point.
- Code: `wave5/steinberg/steinberg.py`, `moves.py`, `hunt.py`, `xcontrol.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: dead-end — and cleanly so. Do not re-propose it.

#### anti-vocabulary root construction
- Family: root/seed supply
- What it does: constructs starting circuits deliberately biased *away* from the project's own harvested mask vocabulary (`avpaar`, `avsplit`, `avtree`, `randset`), on the principle that "a step that saves 6 gates loses to a step that saves 4 with a mask the project has never built".
- Measured performance: `novelty/results/pop.txt` — the from-scratch constructors are the **only** lanes producing genuinely off-family material (`c_anneal3` max-wJ 0.063, `c_bp` 0.078, `c_paar` 0.091, vs `o_polish` 0.830 and `free_own` 0.697); their vocabulary bias is *negative* (−0.55, −0.73) while every other lane is +1.2 to +3.1 bits into the house dialect.
- Code: `novelty/roots/constructors_ext.py`, `novelty/roots/MANIFEST.json`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — the only measured antidote to the house-dialect effect (§5, L2).

### B. Exact combinatorial decision procedures (the proof engine)

#### exact-window cascade (budget-1 / budget-2 / budget-3)
- Family: exhaustive local search with rollback
- What it does: given a circuit and a set of k masks to remove, decides *exactly and completely* whether the removed masks can be rebuilt with at most k−1 (or k−2, k−3) new gates, by a frontier cascade closure with rollback at microsecond cost per test. A "reducible" window on an 88 would be an 87.
- Twist vs siblings: it is provably complete (proof in the module docstring) and validated against independent brute force — 25/25 and 12/12 for budgets 1 and 2, and **1,257 instances including 122 genuine NOs** for budget 3, identically under CPython and PyPy.
- Measured performance: **≈165 million exact window decisions campaign-wide, zero timeouts, zero reducible windows** — every canonical 88 and 89, every population sweep, every family. Throughput 2.9–5.0 states/s on 4 procs (~6,900 windows/s); one exhaustive k=2 shell ≈ 1.2 s, one k=3 shell ≈ 70–136 s, one k=4 window p50 0.94 s under PyPy.
- Cost: hundreds of core-hours, spread across `exact-window`, `exact-k4`, `pop-decider`, `family3-exact`, `frontier-exact`, the two detectors, `families16`, `hunt87_layer89`, `hunt87_basin4`, `d3_exact`.
- Code: `agents/exact-window/work/exact_window.py`, `agents/exact-k4/work/exact_k4.py`, `agents/exact-k4/work/exact_driver3.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: **keeper, with the cert-audit caveat attached** — see §5 L1: the same procedure finds zero reducible windows on a 97-gate circuit that is nine gates from optimal, so an empty shell is not evidence of optimality.

#### 87-tripwire detector (streaming k=2 shell decider)
- Family: exact decision, deployed as a live monitor
- What it does: tails every worker's harvest file by persisted byte offset, dedupes new 88-gate states by md5, keeps a **novelty-biased bounded backlog** (picks the state with maximum minimum symmetric difference against a reservoir of already-swept states, not FIFO), and runs the complete 1,540-window k=2 shell on each. Rationale: every known 88 has an exactly empty k≤2 shell, so a new 88 whose shell is *not* empty is an 87.
- Twist vs siblings: it runs concurrently with the search and raises a `CLAIM_*.json` on a hit; the novelty bias is what makes a bounded backlog defensible.
- Measured performance: **197,072 exhaustive k=2 shells decided across the two fleets, all empty, zero claims raised.** 1.9 s/state on CPython, 0.65 s under PyPy. `hunt87` dropped 64,421 states on backlog overflow; `tri_hunt` dropped 0.
- Code: `hunt87/detector.py`, `tri_hunt/detector.py`, `tri_hunt/exact_window.py`
- Logs/results: `hunt87/detector/swept.jsonl` (148,893), `tri_hunt/detector/swept.jsonl` (48,179)
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — the cheapest continuous safety net in the project.

#### layer-sweep (exhaustive shell sweep of a whole gate layer)
- Family: exact decision at population scale
- What it does: streams *every* population file the campaign has written, extracts every distinct 89-gate realizable target-covering state into a packed binary layer, then runs complete k=2 shells on a provenance- and depth-stratified round-robin sample of it.
- Twist vs siblings: round-robins across (source, min-depth) buckets rather than sorting by novelty — the REPORT documents that a naive most-distant-first sort put 60,000 states at the head that were all one basin.
- Measured performance: 4,002,869 lines streamed → **1,309,223 distinct 89-gate states**; 9,693 complete shells. Reductions occur in **exactly one source** (`hunt87/seeds/pop89_depth6.jsonl`, 982/1,501 hits, ~67%) and **0/7,568 everywhere else**. Within that pocket: 948 `win` (89→88), **0 `free` (89→87)** in 1,428 states. Min-depth histogram of the layer: d5 105,132 · d6 621,755 · d7 172,735 · … · d15 8.
- Code: `hunt87_layer89/layerlib.py`, `harvest89.py`, `sweep_k2_layer.py`, `sweep_k3_layer.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — the clearest single picture of what a plateau layer looks like.

#### family census + irreducibility certificates
- Family: structural analysis + exact decision
- What it does: clusters the whole 88-gate harvest under a calibrated weighted-Jaccard periphery metric, takes connected components as proven-distinct families, picks 3 representatives per family (most central + two most distant), and produces a machine-checkable JSON certificate for each representative's complete k=2 and k=3 shell.
- Measured performance: `families16/out/manifest.json` — 44,610 states clustered, 995,003,745 pairs scored, **10 proven-distinct families at the G32 threshold** (13 groups at G46), max inter-family wJ 0.2827. Certificates: **76 × complete k=2 (1,540 windows) + 76 × complete k=3 (27,720 windows) = 2,223,760 exhaustive decisions, every shell EMPTY**, plus 10 partial k=4 at ~1% coverage.
- Cost: the k=3 certs are ~564 s each ≈ 12 core-hours; the abandoned k=4 attempts cost ~15 core-hours for ~1% coverage.
- Code: `families16/reps.py`, `families16/harvest.py`, `families16/assign.py`
- Logs/results: `families16/certs/` (172 files, 700K) — **the single largest banked proof object in the mid-campaign region**
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — certificates are self-describing and re-checkable.

#### down-step / reduction-lemma analysis
- Family: exact decision + theory
- What it does: asks "remove k masks, restore with k−d" for d ≥ 2 (a double or triple step) rather than the usual d = 1, then proves the whole family reduces to one coordinate.
- Twist vs siblings: it produced a **theorem that retires a whole family of ideas**: every "remove k, add k−d" question reduces to a single coordinate m = the size of the target-free window; the step depth d is bookkeeping. Down-1 and down-2 are equally dead at equal m. Reachable m ≈ 4–5; historical improvements sit at m ≈ 42.
- Measured performance: `wave5/burn/downstep/` — 77,195 ledger lines, **82,786 UNSAT / 748 partial-nosol / 197 timeout**; 20,893 down-step window decisions, 0 SAT, 99.0% theorem-grade; **9 exhaustive theorems**; 88→86 does not fire. One completed m=4 exhaustive theorem on a 90-gate anchor cost 16.0 core-hours (424,270 target-free windows, 0 hits).
- Code: `wave5/burn/downstep/downstep.py`, `exhaustive3.py`, `exhaustive4.py`, `reach.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper as a *theorem*; the search itself is retired by its own lemma.

#### one-target-short exhaustive completion probe
- Family: exact decision at population scale
- What it does: for every harvested 88-gate state and every one of its 32 targets, delete that target's gate, trim, and exhaustively probe every closure pair for a completion at ≤86 or ≤85.
- Measured performance: `wave5/burn/simple/execute/VERDICTS.md` LANE 3c — **1,119,399 distinct 88-states × 32 targets → 1,630,797 objects trimming to ≤86 (23,864 to 85), all probed exhaustively, 0 completions**, 1,611 s wall across 3 shards. A relaxed-threshold self-test found 1,703 real completions, so the instrument has power.
- Code: `wave5/burn/simple/execute/scan86.py`, `scan87.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — cheap, powered, and it produced the ρ-class asymmetry (§5 L6).

#### hub-move exact enumeration (negative move certificates)
- Family: exact decision on the move set itself
- What it does: instead of sampling moves, enumerates *all* of them — all 1,596 remove-2 pairs, all 29,260 remove-3 triples — and certifies the neighbourhood empty.
- Measured performance: `agents/hub-moves/REPORT.md` — the remove-2-add-1 "hub move" is **dead: 0 successes in ~2.24 M repair samples**, later proven exactly empty on all four 89 seeds; the 89@5 record is provably locally optimal under remove-3-add-1 (a hit would have been an 87). `agents/lns-destroy`: uniform destroy sizes 3–6 gave **0 accepts in 5,633 attempts** — about two-thirds of production LNS compute provably did nothing.
- Code: `agents/hub-moves/work/moves2.py`, `agents/lns-destroy/work/lns_lab.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — the pattern (enumerate the move set before spending months sampling it) is the transferable lesson.

### C. SAT / MaxSAT / ILP decision procedures

#### windowed FSK SAT (fixed slot order)
- Family: SAT bounded synthesis
- What it does: freezes all but k of a circuit's gates and emits a CNF asking "can this window be resynthesized with k−1 gates?" in a Fuhs–Schneider-Kamp-style encoding where any model decodes to a whole realizable circuit.
- Twist vs siblings: the *original* SAT instrument; its UNSAT results are **relative to the encoding's fixed slot order** — a caveat `cert_audit` later measured as load-bearing (123 of 128 provably satisfiable windows are manufactured UNSAT under arbitrary orderings, though all 128 legitimate topological reorderings preserve the verdict).
- Measured performance: 137 windows (0 SAT / 88 UNSAT / 49 timeout); max UNSAT window k=12. Found and worked around a pysat bug: `Cadical153.interrupt()` raises `NotImplementedError`, so timeouts were silently ignored.
- Code: `agents/sat-window/sat_window.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: superseded-by wave-6's GF(2)-explicit encoder and by fence_sat.

#### killable-subprocess SAT driver
- Family: SAT infrastructure
- What it does: runs CaDiCaL/Kissat in a child process killed by the OS at the deadline, sidestepping the pysat interrupt bug, with resumable JSONL task ledgers keyed by window id.
- Measured performance: `agents/sat-deep/REPORT.md` — moved the max proven-UNSAT window from k=12 to **k=16**; six wave-1 timeouts became UNSAT at 212–1509 s. Insight: hardness anti-correlates with nB (broken-kept count), not k.
- Code: `agents/sat-deep/sat_deep.py`, `agents/sat-deep/solve_child.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper (infrastructure).

#### symmetry-broken SAT (SB-P + SB-F, `sb=pf`)
- Family: SAT + sound symmetry breaking
- What it does: adds two soundness-proved clause layers — SB-P (parent commutativity, lexicographic order within a gate) and SB-F (conditional lexicographic order on adjacent *free* slots).
- Measured performance: `agents/loose-sat/REPORT.md` — known UNSATs re-decided **14–34× faster** (960/1000/1509 s → 28/45/106 s); **10 of the 14 previously undecided "loose" windows on Jean's 88 fell to UNSAT**, including the two loosest. Verdict shift: with `sb=pf` the binding limit is no longer solver power but the fixed slot order.
- Code: `agents/frontier-sat/frontier_sat.py` (the implementation), `agents/loose-sat/loose_sat.py` (the runs)
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper.

#### fence / topology-family SAT (order-free)
- Family: SAT with symmetry eliminated by construction
- What it does: enumerates *fences* — ordered partitions of the free gates into levels — and solves one CNF per fence with the level structure pinned. Every DAG conforms to exactly one fence, so the family is complete and slot-permutation symmetry is eliminated **by construction, not by clauses**. An UNSAT sweep over all fences of a window is a real theorem with no ordering caveat.
- Twist vs siblings: **the only certificate class in the entire project without the slot-order caveat.** Ported from Haaswijk et al. (TCAD 2020) onto the existing encoder because `percy` itself cannot run here (truth-table based, ≤8 inputs).
- Measured performance: validated 11/11 planted, 94/94 against the exact decider, adversarial soundness probe 8/8. Sweeps: round-1 9 order-free UNSAT / 931 units; family 10 UNSAT / 9 open-hard / 18,294 units / **215.1 h solver time**; novel-89 16 UNSAT / 5,238 units / 41.9 h. Whole-track ledger tally: **29,125 unsat, 433 trivial-unsat, 78 timeout, 24 open-hard, 13 sat (all planted/validation)**. **But its own positive control killed it**: 30 windows across slack 1–9, `{open-hard: 13, unsat: 17}`, **0 SAT** — including `ctl_s9_97to96`, where nine gates of slack provably exist. A k=13 window cannot see a one-gate improvement that is provably one gate away.
- Code: `wave5/fence_sat/fence_sat.py`, `sweep.py`, `validate.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: **keeper for certification, dead as a discovery instrument at k≤13** — and see §5 L3: its 28 highest-value windows were never run.

#### free-closer (one unrestricted mask over all 2³²)
- Family: SAT, vocabulary-relaxed
- What it does: fixes a region's core and asks the "last step" question with the closing gate mask **unrestricted over all 2³²** rather than drawn from a harvested alphabet.
- Twist vs siblings: it is the only instrument that escapes vocabulary conditioning — but it escapes it by exactly **one mask**. The wave-5 roll-up overstated this as "not conditioned on harvested vocabulary" and was formally corrected.
- Measured performance: positive control 4/4 (recovers a deleted mask from ~6,350 candidates in 0.7–2.4 s). Rungs: `FC_K87_{A,B,D,E}` and `FCS_K87_SIGMA{5,7}` and `FCR_K87_cls{0,1}` all UNSAT at L=13; `FC87_K87_{A,B,D,E}` UNSAT depth-unconditional (L=87) at 472–2,689 s each. **Control audit: 23 CONTROLLED, 3 UNCONTROLLED, 2 VACUOUS.** Undecided: region C (3 timeouts), class-0-grown, `V88pref240`, the n85 object.
- Cost: ≈44 core-hours in that table alone, ~28 h of it on TIMEOUT/UNKNOWN rows.
- Code: `wave5/burn/simple/execute/freecloser.py`, `audit_controls.py`, `summarize.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — the strongest scoped instrument in wave 5, provided the scope sentence travels with every number.

#### RC2 MaxSAT alphabet floors (union / per-region)
- Family: exact MaxSAT over a restricted mask alphabet
- What it does: takes the union of two verified circuits' mask sets as the alphabet and asks RC2 for the *exact* minimum-size circuit realizable inside it.
- Twist vs siblings: exact, not a bound; and the union always contains a complete 88 by construction, so no separate vacuity control is needed.
- Measured performance: `wave5/burn/union_sat/STATUS.md` — **347,525 pairs decided, floor distribution {88: 347,509, TIMEOUT: 16}, best floor anywhere 88**, mean 2.45 s/pair (≈236 core-hours); ledger tally 749,150 OPTIMAL / 125 TIMEOUT. **Its own power control is the whole story: union(89_a, 89_b) from different lanes hits floor 88 in 4 of 600 pairs (0.7%)** — so the instrument *can* find a −1, at a measured rate, and never did at 88. Four named cross-region 88s were produced this way and oracle-verified.
- Code: `wave5/burn/union_sat/work/*.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — with union_sat's own control, this is the best-calibrated negative in the slice.

#### alphabet-restricted SAT ladder
- Family: SAT over a fixed alphabet, rung by rung
- What it does: fixes an empirically universal core and frees the rest over the harvested vocabulary, asking K = 87 rung by rung.
- Measured performance: **self-refuted in its own STATUS.md, in capitals.** The per-region test returns K=96 **UNSAT in 0.4 s on a 97-gate region that has a verified 88 nine gates below it**; RC2 floors return each region's own count exactly (97→97, 92→92, 90→90, 88→88). Ledger: SAT 164 / UNSAT 50 / TIMEOUT-UNKNOWN 37 / OPTIMAL 5. Verbatim: *"Therefore the nine K=87 UNSATs below are NOT evidence that no 87 exists."*
- Code: `wave5/alphabet_ladder/work/alphabet_ladder.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: dead-end — and the way it died (a control, run late, that invalidated the track's own headline) is the most valuable thing in it.

#### depth-capped window SAT (kissat, caps 4 and 5)
- Family: SAT with a depth constraint
- What it does: freezes all but r masks and asks for a resynthesis at ≤ the same gate count **and depth ≤ cap**.
- Measured performance: `hunt87_depth4/runs/*.jsonl` — **2,275 UNSAT / 61 timeout / 22 SAT, and every SAT is a calibration self-test**; i.e. every genuine depth-4 push is UNSAT. `hunt87_depth5`: `sib_sweep.out` 32/32 unsat, `sib_sweep2.out` 119 unsat / 2 timeout. Runs cost 31,179 s and 38,966 s wall.
- Code: `hunt87_depth4/work/d4run.py`, `hunt87_depth5/work/d5run.py`, bundled `bin/kissat_d4`, `work/kissat_d5push`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper for Pareto-frontier work.

#### global CP-SAT / min-union set cover
- Family: ILP / CP-SAT global bound attempt
- What it does: harvests a global vocabulary of masks and cones from every run, then asks a single global model for a ≤87-gate solution, or for a certified lower bound via min-union-of-cones.
- Measured performance: **negative on every axis, and diagnosed.** The 88-gate vocabulary saturates at **1,112 masks** (an independent Chao1 estimate predicted exactly 1,112). Min-union ILS: 814 restarts, ~43,500 local optima, **23,906 landings at exactly 88, zero below**, and all 872 distinct 88s produced were already in the harvest. Global CP-SAT ≤87: **UNKNOWN after 11,989 s / 17,988 s / 17,990 s**. `subset_bound.log` is two lines and reports a **certified bound of 2**. The LP relaxation is **provably vacuous** (aggregated 0.175, disaggregated ≤ 4.496 by an explicit feasible point). A later audit found the historical CP-SAT UNKNOWNs all ran with `lp_iterations: 0` — only `linearization_level=2` engages the LP, and with it a historically-UNKNOWN instance became **INFEASIBLE in 0.5 s**.
- Code: `global_vocab/min_union_cpsat.py`, `lp_bound.py`, `subset_bound.py`, `run_B.py`; `wave5/lp_closure/`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: dead-end as a bound; **keeper as a vocabulary harvester** (`V88.json`, `vocab_counts.json`).

#### cone-vocabulary ILS
- Family: set-cover local search
- What it does: iterated local search over min-union-of-cones assignments across a 92,208-cone library.
- Measured performance: `global_vocab/cone_ils.log` — 529 restarts, best 88, cost histogram `{88: 15537, 89: 2270, 90: 2529, 91: 3907, 92: 2548, 93: 1578, …}`. A completely different search paradigm lands on 88 **6.8× more often than on 89**, with a non-monotone dip at 89–90 — independent evidence that 88 is a genuine attractor.
- Code: `global_vocab/cone_ils.py`, `cone_ils88.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper as an *evidence* instrument (§5 L5).

### D. Lower bounds and structure theory

#### depth-3 structure theorem + complete model
- Family: exact structural enumeration
- What it does: proves that in any depth-≤3 circuit every target sits at level exactly 3 (weight 5 or 7 > 2² = 4), no target feeds another gate, level-1 gates have weight exactly 2, and level-2 gates weight 3 or 4 — hence `N_depth3 = 32 + min(|L1| + |L2|)` over a **finite** space: 7,897 candidate level-2 masks, 496 candidate edges, 6,120 decompositions.
- Twist vs siblings: this is the only place in the project where the search space is finite and completely enumerable.
- Measured performance: the three counts were derived twice independently (wave-5 `metareview/optimality/depth3_exact.py`, wave-6 `lower_bound/model3.py`) and agree exactly.
- Code: `d3_model/d3_theory.py`, `d3_model/d3model.py`, `wave6/lower_bound/model3.py`
- Generality: **MC-HARDCODED but mechanically portable** — the theorem only needs the target weight profile; for another matrix, recompute the weight bound 2^ℓ and re-enumerate.
- Phase-2 verdict: keeper — the foundation of the campaign's only unconditional theorem.

#### certified LP dual bound with valid inequalities (**N_depth3 ≥ 80**)
- Family: LP relaxation + exact rational certificate
- What it does: writes an integer-coefficient system `A p ≥ b` whose every row is a proved theorem about depth-3 circuits (cuts C1–C10), obtains a dual vector `u ≥ 0` with `Aᵀu ≤ c` from HiGHS, **rounds it to denominator 10¹² and re-verifies feasibility in exact integer arithmetic** before reporting. Weak duality then gives the bound with nothing floating-point in the claim.
- Twist vs siblings: the certificate (`cert_depth3.json`, 23,450 nonzero duals) is re-checkable in one command independently of the solver, of scipy, and of the session.
- Measured performance: `u·b = 47.597998… ⇒ |L1|+|L2| ≥ 48 ⇒ **N_depth3 ≥ 80**`. Bracket 80 ≤ N_depth3 ≤ 97. Without the cuts the LP is 29.19 (⇒62); wave-5's uncertified CP-SAT dual was 34 (⇒66). C8 alone is worth +1.05. **Three mandatory controls all PASS** (the verified 97@3 circuit maps into the model at cost exactly 65; none of the 23,405 cuts is violated by it; none of the 72,830 LP rows is violated). By-products, also certified: every depth-3 circuit has ≥18 level-1 gates; only E ∈ {19, 20} can reach 48, and both sit at LP value **exactly 48.0**, so no further cutting can raise the bound — everything above is integer reasoning. SCIP 10 reproduces the root LP to 7 digits through a different code path.
- Cost: minutes for the certificate; the branch profile is 42–45 s per E.
- Code: `wave6/lower_bound/{model3,cuts,build_lp,certify,branch_certify,node_probe,control_primal,control_cuts,control_lp}.py`
- Logs/results: `wave6/lower_bound/THEOREM.md`, `cert_depth3.json`, `branch_summary_E18_48.json`
- Generality: MC-HARDCODED (the cuts are theorems about *this* weight profile) — but the *recipe* (complete structural model → valid inequalities → exact rational dual → mandatory primal control) is fully generic.
- Phase-2 verdict: **keeper — the single most valuable artifact in the slice.** It is the only unconditional result the campaign owns.

#### target-subset exact MILP lifting (the abandoned ≥63 ladder)
- Family: lower bound by relaxation
- What it does: picks a subset of k targets, solves the exact depth-3 model restricted to them to proven optimality, and lifts `min|P|+|Q| + 32` into a global bound (dropping targets is a valid relaxation).
- Twist vs siblings: it is **integer reasoning**, not LP — exactly the thing wave 6 concluded is the only route past 80.
- Measured performance: `d3_model/logs/d3bound.log`, whole run 17 minutes on one core: 32 (trivial) → **52** (k=6, 19 s) → 53 → **59** (k=8, 129 s) → **63** (k=10, 155 s), every rung `PROVEN OPTIMAL`. **The log ends there with no k=12 attempt and no explanatory note.**
- Code: `d3_model/d3bound.py`
- Generality: MC-HARDCODED, same as the model
- Phase-2 verdict: keeper — see §5 L4; this is a live, cheap, unfinished route.

#### edge-floor relaxation + ladder
- Family: lower bound sub-relaxation
- What it does: drops the level-2 counting entirely and bounds only the edge structure (496 real variables instead of 29,180), then composes an edge floor F with the certified per-E profile: `N_depth3 ≥ 32 + min_{E≥F} LP_E`.
- Measured performance: F=21→81, 23→82, 25→84, **27→85 (its ceiling, since the verified 97@3 uses 27 edges)**. Status: cap 20 undecided at 1,200 s (CP-SAT); cap 19 UNKNOWN after 10,800 s (`edge_ladder.log`). Established floor F = 18 ⇒ N_depth3 ≥ 80.
- Code: `wave6/lower_bound/edge_floor.py`, `edge_floor_sat.py` (CNF + kissat with DRAT), `edge_ladder.py`
- Generality: MC-HARDCODED
- Phase-2 verdict: keeper but capped — it cannot on its own reach the 56 needed for the depth-4 theorem.

#### obstruction hunt (parity / counting / invariant arguments)
- Family: lower-bound theory, systematically executed and mostly refuted
- What it does: enumerates the candidate classes of obstruction against an 87 and kills or scopes each with a machine check.
- Results, all machine-checked (`wave5/burn/obstruction/OBSTRUCTIONS.md`):
  - **T0 (PROVEN):** orbit counting on the set of circuits can prove *existence* but never *non-existence* — the empty set satisfies every Burnside congruence. Any obstruction must be an invariant of a *single* circuit.
  - **P1/P2 (PROVEN, conditional):** any 87 whose mask set is exactly ρ²-closed contains an **odd** number of ρ²-fixed masks; the ρ version has a mod-4 refinement. At 88 both are vacuous.
  - **Weight/cancellation accounting (REFUTED constructively):** the weight-flow identity `w(t) = P(t) − 2Σμ_h(t)c_h` is exactly true and machine-verified on all 8 evidence circuits — and *scale-free*. `counterexample_87_weight184.json` is a verified **87-gate circuit with MixColumns' exact weight profile (20×5 + 12×7 = 184), 32 independent outputs, all gates alive, 41 cancelling** — so no weight-accounting invariant can exclude 87. (Re-verified this session: the file is **not** a MixColumns circuit, by design.)
  - **Rank/matroid (KILLED):** the target matroid is the free matroid on 32 elements, identical for the identity matrix. The odd-weight-forest bound (every odd gate has one odd parent and one even gate parent ⇒ ≥32 odd gates, ≥1 even gate) caps near 35.
  - **Symmetry group (COMPUTED, KILLED):** `Aut(M) = {(σ,τ) : PMQ = M}` has order **exactly 4 = ⟨ρ⟩`; the transpose-twisted part is **empty** (M is not permutation-equivalent to Mᵀ). Full count-preserving symmetry is ⟨ρ⟩ × {id, trace-dual}, order 8.
  - **Move-invariant homomorphisms (KILLED empirically):** six candidate Z/2–Z/4 invariants tested against 380,034 pairs of harvested 88s at symmetric difference exactly 2 — every one is flipped by a single ±0 move (46,260 to 277,921 flips each). No connectivity assumption needed.
- Code: `wave5/burn/obstruction/t1_equivariance.py … t5_plateau_scan.py`
- Generality: MIXED — T0, the weight identity and the odd-forest argument are CIRCUIT-GENERIC; the ρ analysis is MC-HARDCODED.
- Phase-2 verdict: **keeper — the highest theory-per-byte directory in the slice (80 KB).** It tells a successor exactly which lower-bound ideas not to re-propose, with a machine-checked reason for each.

#### transpose duality
- Family: structural identity
- What it does: proves and exploits `XOR-count(M) = XOR-count(Mᵀ)` — reversing a dead-gate-free 2-input-XOR DAG computes the transpose at exactly the same gate count.
- Measured performance: verified 88→88→88 round trips on all five known 88 families, both 89s, the 92 and the 97; 300 perturbed circuits, 0 failures. **Depth is NOT preserved** (5→6, 5→7, 4→8, 3→5, 8→11). Structurally `Mᵀ = (I₄⊗B)·PMP·(I₄⊗B)⁻¹` with B the Gram matrix of the GF(2⁸) trace form — a genuine basis change, not a permutation, which is why the optimum is identical but the landscape is not. Only **11.1% of periphery masks** are shared between a circuit and its transpose, so k=2 window collections are ~89% disjoint. Result: **8,481 Mᵀ states, 13,705,916 exact window decisions, 22 complete k≤3 shells, zero reducible.** Wave 6 additionally *hunted* in Mᵀ and measured the null at n=27 and n=14 per arm — no reachability advantage.
- Scientific value: **kills the "primal neighbourhoods were the problem" hypothesis** — the barrier is structural, not an artifact of move shape.
- Hazard: with k dead gates the transpose is *smaller by exactly k*, so an untrimmed 89 appears to become an 88. Trim first, always.
- Code: `dual_transpose/transpose.py`, `verify_duality.py`; `wave6/transpose/`
- Generality: CIRCUIT-GENERIC (any linear map)
- Phase-2 verdict: keeper — cheap, proved, and it doubles the neighbourhood supply for free.

#### structure-algebra (ρ² symmetry analysis)
- Family: structural analysis
- What it does: measures which symmetries of the target set the search has discovered on its own.
- Measured performance: the 32 targets are a **single** column map (no disjoint 4-column decomposition; every output byte touches all four input bytes). ρ has order 4 and the targets form 8 free ρ-orbits. **Full ρ-symmetry costs +19** (best ≈108); the elite basin is **79–81% ρ²-symmetric** and its 12 ρ²-fixed masks are exactly the classic (x0^x2)/(x1^x3) trick — the search rediscovered the order-2 subgroup unaided. Jean's 88 is 75% ρ²-symmetric. Best single-byte cone standalone is 33 gates, so four independent cones would cost ≥132 against 89 achieved — cross-byte sharing is the whole game (57 of 89 gates shared).
- Code: `agents/structure-algebra/{sym_search,sym_lns,analysis}.py`
- Generality: MC-HARDCODED
- Phase-2 verdict: keeper — it produced the seeds both search-found 88 families descended from.

#### hand-reduction algebra (the plane / parity-hub law)
- Family: hand reasoning
- What it does: a human-legible algebraic dissection of what the 88-gate circuits actually compute — bit-plane parities `P_i`, the carry structure of xtime, and where each circuit spends its gates.
- Measured performance (`wave5/burn/handreduce/WAVE2_INSIGHTS.md`, 48 KB of prose, no code, no data): identifies the **parity-hub law** — the 88/89 separator is exactly "materialize ≥1 plane parity as a cross-orbit hub"; each hub costs exactly 1 gate and serves ~3 targets in two orbits; 89/90/92/96/97-gate circuits have none. And a corpus-wide blind spot: **all observed hubs lie in {P1, P2, P4, P6} — precisely the parities usable without touching P7 — while P7 is the unique quadruple-duty mask**, appearing in all four carry-orbit terms. Every known circuit instead re-buys P7 fragments per letter, and "the invariant 21-gate xtime-carry toll is exactly the cost of refusing to materialize P7 once." Uniform across all eleven circuits examined.
- Code: none (analysis only)
- Generality: MC-HARDCODED (it is about AES MixColumns' specific algebra)
- Phase-2 verdict: **keeper — the densest single unexecuted hypothesis in the slice** (§5 L7).

### E. Measurement, control, and audit instruments

#### positive-control methodology (the campaign's real product)
- Family: methodology
- What it does: every negative instrument is re-run on an instance that provably has the improvement it claims not to see — typically a circuit one to nine gates above a verified better one.
- Measured performance, across four independent instruments:
  - `cert_audit/`: the exhaustive k=2 decider finds **0 reducible windows** on a 97-gate circuit with a verified 88 nine gates below, on a 94, a 92, a 91, a 90, an 89 and Jean's 88 — **12,241 exhaustive k=2 + 8,400 sampled k=3, zero reducible anywhere.** *"A 97-gate circuit is indistinguishable from Jean's 88 by this instrument."* Transition distance over 45 circuits with a known better one: min 3, **median 42**, max 48 — against a certified radius of 3.
  - `wave5/alphabet_ladder/`: per-region vocabulary UNSAT in 0.4 s on a 97-gate region with 9 gates of slack.
  - `wave5/fence_sat/STATUS_CONTROL.md`: 30 windows across slack 1–9, **0 SAT**.
  - `wave5/metareview/optimality/`: dead-gate count and derivation rigidity are identical to four significant figures at 88/89/90/91/92 (2.312–2.326 options/gate; 0 dead gates in 1,200 samples per length). **LR = 1.00.** It also *inverts* the campaign's own framing: against a proper null (random 88-mask subsets of V88 at 0.495 options/gate), real 88s are **4.7× more derivation-rich**, not rigid.
  - Completeness control: 4,200 planted-YES windows over 74 circuits, each decider branch tested in isolation by deleting the earlier branches — 462/462 and 33/33 recovered, zero oracle rejections.
- Code: `cert_audit/{plant_probe,control,case_hunt,slot_order_test}.py`, `wave5/burn/simple/execute/audit_controls.py`, `wave5/fence_sat/validate.py`
- Generality: CIRCUIT-GENERIC — **this is the most transferable thing in the slice.**
- Phase-2 verdict: **keeper. Standing policy from `CAMPAIGN_VERDICT.md`: no negative is reported without its one-gate-above control.**

#### novelty ruler (neutral-baseline weighted Jaccard)
- Family: measurement
- What it does: builds a *neutral* corpus of MixColumns constructions (6,171 documents across 7 strata: BP, tree, reuse, Paar, Paar-soft, published, anneal3 roots) and contrasts mask document-frequency there against the project's own harvest, producing an IDF weight table so "how novel is this circuit" is measured against constructions the project did not make.
- Measured performance: 402 of 911 harvest periphery masks (44.1%) are **never produced by any neutral construction**. Family threshold calibrated at wJ ≥ 0.46 (error 0.0, margin 0.144) and plain J ≥ 0.60. Then the finding that matters: **76.4% of 42,763 harvested 88s sit inside a known family**, and the only lanes producing off-family material are the from-scratch constructors.
- Code: `novelty/novelty.py`, `measure.py`, `baseline/gen_baseline.py`, `baseline/calibrate.py`
- Logs/results: `novelty/baseline/weights.json` (357K — the table the whole campaign's `wj` metric depends on)
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — without it, "new family" claims are unfalsifiable.

#### slot-order sensitivity test
- Family: audit
- What it does: re-emits the same window CNF under different gate orderings and checks whether the verdict survives.
- Measured performance: **arbitrary orderings manufacture UNSAT on 123 of 128 provably satisfiable windows** — the caveat is load-bearing and must never be dropped. But **128/128 legitimate topological reorderings preserve the verdict**, and the seed's own order is in that class, so the campaign's UNSATs are not wrong — they are correctly scoped.
- Code: `cert_audit/slot_order_test.py`, `cert_audit/d6sat_order_test.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper (mandatory before quoting any windowed UNSAT).

#### prior-art import + provenance audit
- Family: literature
- What it does: transcribes published circuits from papers, verifies each against the GF(2⁸) oracle, measures its depth (papers usually state none), and scores its distance from every project circuit.
- Measured performance: 12 circuits imported and all oracle-VALID — Jean 88@7, Sun–Yang–Li 89@9, Yuan 91@8, Maximov 92@6, Xiang 92@6, Osvik–Canright 94@5 and 97@4, Tan–Peyrin 94@9, Banik 95@6, Boyar–Peralta 97@8, Shi–Feng–Xu 99@3, Liu–Zhao–Wang 102@3. Feeding eight alien basins to the engine for ~5 h produced 89s and no 88s. **Literature corrections on the record**: ePrint 2020/903 is Xiang et al., not Lin et al.; the Yuan 91 is in-place (s-XOR) and must not be cited as Lin's g-XOR 91; **Tan–Peyrin's table says depth 6 and this project measures depth 9**; Lin–Xiang–Zeng–Zhang (CT-RSA 2021) could not be obtained at all.
- Code: `agents/lit-88/{fetch_jean,import_jean88,import_sun89}.py`, `prior_basins/work/import_lib.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — and `fetch_jean.py` (Playwright/cloudscraper against a Cloudflare-blocked ePrint) is the reusable part.

#### self-test / tripwire harness
- Family: validation infrastructure
- What it does: plants a known-solvable instance (a deliberately wasted gate, a fake 87) and checks that the pipeline finds it and that the export path *rejects* the fake.
- Measured performance: `cascade6/selftest_cascade.py` — **131 checks, 0 failed**, and it pins three real harness bugs, including the one that matters most: *"Cross-pollination was silently dead — `hunt87/hunt_worker.py` never called `wire_harvest`, so every hunt87 fleet harvested and never merged, and nothing in the logs said so."* The four `"gateCount": 87` files in the whole slice are all tripwire artifacts named `fake87`, `badfail` or `FAILED_87` — the strongest available evidence that no real 87 was ever found and lost.
- Code: `cascade6/selftest_cascade.py`, `d3_exact/selftest.py`, `hunt87/selftest_archive.py`, `agents/*/selftest*.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — mandatory.

#### meta-review (six independent red-team agents)
- Family: audit
- What it does: six agents (auditor, framebreaker, forecaster, optimality advocate, outside view, explorer) independently attack the campaign's own claims and instruments.
- Measured performance: found **six live bugs on the ≤87 path** — pin-before-size, seen-before-verify, an NRPA export gate that had silently swallowed **1,821 of its 1,822 distinct 88s**, a gateCount schema mismatch, a silent SAT downgrade, and a 300,000-line harvest dedupe cap that froze the three most productive lanes for hours (~410k states discarded on one lane alone). None had produced a false claim; several would have silently dropped a future 87. The framebreaker produced the structural finding of the campaign: **the "540,579 distinct 88s" collapse to ~10–15 effective mask alphabets**, with 291,771 of them sharing one *set-identical* 113-mask vocabulary.
- Code/results: `wave5/metareview/{auditor,framebreaker,forecaster,optimality,outside,explorer}/REPORT.md` + `SYNTHESIS.md`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: **keeper — schedule one before, not after, the expensive runs.**

### F. Wave-6 methods (the last wave — mostly undocumented in any roll-up)

#### GF(2)-explicit (XOR-native) SAT encoding
- Family: SAT encoding
- What it does: replaces the Tseitin-triple window encoding with one selector row and one XOR row per bit, keeping the GF(2) structure explicit so only free-slot→free-slot fan-in is bilinear.
- Twist vs siblings: it is the *encoding*, not the solver, that moves the ceiling — a positive test that also **refutes** the Gauss-Jordan hypothesis (the 5 GJ matrices engage and buy nothing measurable).
- Measured performance: CNF at n=12 is **19.7 k clauses vs 106.7 k (5.4× smaller)**; head-to-head over 64 solves, new-only wins 4, old-only 0, **median 9.3×**; at n=16 old 0/2, new 2/2. **Ceiling moved n=12 → n=14** (2/2 at n=16). Validation V1–V6 pass, including V6 54/54 against a brute-force oracle with no SAT solver. Adopted campaign-wide as the production window instrument on 2026-08-11.
- Self-reported defect (quarantined, honest): `_exactly_two` initially asserted only one half of the sequential counter, so a free slot could degenerate into a copy. All UNSATs stayed sound and every SAT was oracle-verified, but the first head-to-head was biased in the new encoder's favour, and **all six validation gates passed with the bug present**. Superseded rows are in `xor_encoding/runs/relaxed_encoder_SUPERSEDED/`.
- Code: `wave6/xor_encoding/xorenc.py`, `bench.py`, `hunt.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: **keeper — this is the SAT instrument to carry forward.**

#### parallel DFS over derivation DAGs with a shared transposition table
- Family: exhaustive branch-and-bound, no CNF at all
- What it does: searches directly over derivation DAGs in C with a lockless shared transposition table, root-splitting into tasks with adaptive re-splitting. Relies on a monotone-improvability lemma: a SAT at any block **is** the 87, and a full UNSAT sweep certifies the whole convex **down-set** of that block.
- Twist vs siblings: it beats the SAT route on exactly the instances SAT cannot do — **40 rows where kissat timed out at 90–155 s were decided in 0.1–25 s**.
- Measured performance: validation V1 504 decisions / 145,752 re-splits / **0 mismatches**, V2 632 decisions 0 mismatches, 398/398 planted controls, and 373/373 agreement with the single-threaded ledger. Scaling on B=15: 376.5 s (1 thread) → 33.1 s (16 threads), 4.31e7 nodes/s. Pruning median log₁₀ −5.03 at n=8 → **−6.90 at n=12**. Two corrections it forced on the campaign plan: the projected 10⁸ nodes/s/core was never achievable (real ~2×10⁶, memory-bound, 69% TT hits), and the planned distance prune was **unsound** and would have manufactured false UNSATs.
- Results (see §5 L8 — these were never written into any summary): **B=16, 7 of 8 anchors UNSAT** (fromscratch 2.95e11 nodes, depth5, depth6, depth7 1.22e11, thirdfamily, SIGMA5 1.39e11, alg2; SIGMA7 hit CAP at 5.82e11 nodes) and **B=17 UNSAT on SIGMA7 (2.05e11 nodes, 12,678 s) and alg2 (2.33e11 nodes, 14,905 s)**, both with `planted_control: "planted ok (17 gates)"`. Independently cross-validated on a second machine (a rented pod) — three B=18-ladder rungs agree to 3 significant figures.
- Code: `wave6/dfs_par/par.c`, `psweep.py`, `xpar.py`; single-threaded ancestor `wave6/dfs_spike/dfs.c`
- Logs/results: `wave6/dfs_par/psweep.jsonl`, `psweep_b17.jsonl`, `ck/` (16 MB of checkpoints), `runpod/synced/ck_rescue/ck/` (5.6 MB, including the live B=18 checkpoint)
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: **keeper — the strongest exhaustive engine the project ever built, and it was still climbing when the campaign stopped.**

#### convex-block / band splice deciding (out-degree ≤2 components)
- Family: SAT window generation
- What it does: instead of cones or random removals, cuts out **out-degree ≤2 connected components** of the DAG (size 9–28) and asks the down-1 question over the GF(2) encoder.
- Twist vs siblings: it decides a band nobody had ever decided. Its predecessor filter — SYL §4.2's out-degree-**1** window rule — is **provably inert on an 88** (every component is a singleton on all six circuits tested); out-degree ≤2 is the version that has structure at this size.
- Measured performance: `band_hunt/runs/ledger.jsonl`, 290 rows, controls OK 274 / VACUOUS 16: n≤9 15 unsat, n=10 70 unsat + 28 timeout, n=11 30 unsat + 65 timeout, **n=12 2 UNSAT** + 34 timeout, n=13/14 timeout only. Zero SAT anywhere.
- Code: `wave6/band_hunt/band.py` (37 K — the wave's most reused module), `wave6/pattern_class/SPEC_for_disc_windows.md` (the spec)
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper.

#### the constraint-ratio law (window difficulty prediction)
- Family: instrument calibration
- What it does: predicts window difficulty from `|req|/n` (required-outputs over free-slots) rather than from n.
- Measured performance: pooling two independent ledgers at fixed n — ratio 0.5 → 0/15 decided; 0.6 → 26/104 (605 s); 0.7 → 110/139 (126 s); 0.8 → 178/180 (22 s); 0.9 → 176/176 (6.5 s); 1.0 → 39/39 (4.1 s). A **~70× spread at fixed n**, and above ratio 0.8 n has no residual effect. It explains an apparent inter-track disagreement as a difference in *which windows each generator produced*.
- Its own closing caveat, which is the important half: *"a MORE constrained window is LESS likely to hide an 87, so the speed and the 87-hunt point in opposite directions."* Every instrument that got faster in wave 6 got faster on the windows least likely to contain the answer.
- Code: `wave6/hp_strike/compare.py`, `hp.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: **keeper — use it to *schedule* windows, and read the caveat before quoting a throughput number as progress.**

#### co-parent / rebracket-pair disconnected-window predicate
- Family: window generation, targeting a measured blind spot
- What it does: generates **disconnected** removal windows using a witness-free co-parent predicate, closing a blind spot that wave 5 measured: every window generator the project had ever run samples *connected* sets, and the one improving window whose shape is known is four pairwise non-adjacent masks.
- Measured performance: hit rate **1 in 81** at m=4 versus `disjrand` 1 in 292,449 and uniform C(58,4) = 424,270 — a **~3,600× enrichment**; a class that took 16 h to exhaust closes in **3.6 s**. Blind spot re-confirmed: `cluster` 0/197,000, `cone` 0/118,000, wave-5 `sibling` 0/74,000. **872 window decisions, all theorem-grade, 0 SAT.** Killed by triage because the exact deciders cap at n≤9 while the new encoder reaches n=14–16.
- Code: `wave6/disc_windows/disc.py`, `discsweep.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper (the predicate), superseded (the decider).

#### skeleton pools + RC2 exact-floor generator
- Family: generate-and-decide
- What it does: generates mask alphabets by closure and lattice construction and asks RC2 for each one's exact minimum, so a floor ≥ 88 *is* the K=87 UNSAT and ships its own decoded 88-gate witness.
- Measured performance: **88,908 pools decided by exact floor** at 4,818/h, mean 1.00 s per floor, 10.4 h uptime. Floor distribution 88 → 16,941 (19.05%), 89–91 → 7,095, 92–95 → 19,691, 96–100 → 26,143, 101+ → 19,026. Positive-control chain 25,074/25,074. Elite archive of 300, **all floor 88**. Stopped when its kill criterion fired: the `nov` family scored **0/4,440 at floor 88** (min 89) — every measured step away from an anchor costs at least a gate.
- Code: `wave6/skeleton_pools/{gen,loop,sp_core,worker}.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper, but see §5 L9 — an audit found its cross generator silently capped at 4 bit-planes.

#### plane-cage discriminator (matched-pair quota descent)
- Family: controlled experiment on an instrument's own assumption
- What it does: tests whether the ≤3-bit-plane confinement that most campaign instruments assume is a fact about optima or an artifact of the operator, by running matched-pair descents under a quota that forces a ≥4-plane gate versus a rarity-matched **sham** quota.
- Measured performance (recomputed from the final 663-row ledger, not the frozen snapshot): the ≥4-plane predicate is **free at the plateau — 88 on 120 of 120 held descents, price 0.00 gates** — while the rarity-matched sham quota costs ≈ **+0.87 gates**. Separately, a census of 11.7 M harvested state-lines found **31,016 distinct oracle-verified 88-gate MixColumns circuits containing a 4-plane gate**, across 13 run files from four independent tracks. Price curve: max-planes 4 → min 88; **5 → min 89** (1,137 circuits); ≥6 unobserved. 0 of 663 descents reached 87.
- Honest negative in the same track: the planted-optimum calibration E2 "CANNOT BE COMPLETED" — the surrogate family is 20–25 gates easier than real MixColumns, so it calibrates nothing.
- Code: `wave6/discriminate/{scan_hiplane,verify88,quota_walk,plane5,plant,surrogate_run}.py`
- Generality: CIRCUIT-GENERIC (the "does my instrument's cage exclude known solutions?" experiment)
- Phase-2 verdict: **keeper — this is the wave's most important result** (§5 L9).

#### high-plane tier probe (does the oracle ever *take* a wide mask?)
- Family: instrument-capability measurement
- What it does: offers the exact floor oracle masks touching ≥5 bit planes and measures whether an optimum ever uses one.
- Measured performance: **3,731 pools offering 7,755 ≥5-plane masks; used 0 times**; 95% upper bound on per-pool usage 0.103%. The detector's positive control fires (336 injected masks used, plane counts {2:297, 3:9, 4:2, ≥5:0}). Corroborated with no new compute by rescanning another track's 89,003 floors: 6,183 buildable ≥5-plane masks, **0 ever selected**. The structural reason: buildable rate for a random p-plane mask is **0.0000 at p = 5..8** (0.35 at p=3, 0.003 at p=4, 1.0 at p=2) — making one buildable needs `k ≥ p−4` extra pool slots. Leave-one-out over 4,572 (pool, mask) pairs: removing a 5-plane mask never moves the floor (19/19).
- Code: `wave6/highplane/{hp_lib,hp_worker,hp_report,hp_ledgerscan,hp_patchcheck}.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — a model of how to close a frontier honestly and cheaply.

#### fusion-surplus / plane-abstraction census
- Family: structural analysis at population scale
- What it does: computes a plane-level "fusion surplus" for every harvested 88 and asks whether the plateau is one structure.
- Measured performance: over **434,125 distinct verified 88 mask-sets**, surplus spans **16..30** (mean 21.68) across **13,132 distinct type-histograms**, and is realization-invariant. **"The 88 plateau is one fusion pattern" is refuted**, and the plane-counting floor (Σ ≥ 64) is loose by 16–30, so no plane-level counting argument can bound 87. Also: 9,391 sets (2.16%) carry a signal touching 4 planes — always exactly one, consumed exactly once, always built from two disjoint-plane 2-plane parents; **0 sets reach 5 planes**.
- Code: `wave6/fusion_diag/plane_scan.py`, `precond.py`
- Generality: MC-HARDCODED (bit planes are specific to this byte structure)
- Phase-2 verdict: keeper (it closed a whole abstraction level as too coarse).

#### modular / glue-conditioned synthesis
- Family: constructive decomposition
- What it does: builds MixColumns as 7 small SLPs on 8–12 variables glued through single-residue masks, and — crucially — generates the candidate mask population from the glue structure **without ever reading a circuit**.
- Measured performance: best from-scratch modular result is an **exact floor of 96** with a decoded RC2 witness; the ladder on the same objective runs empty-glue 106 → locally-optimal modules 103 → greedy 103 → hill-climb 101 → block-coordinate descent 96 → exact floor 96. Findings, each measured: Boyar–Peralta is **exactly optimal given a glue** (gap 0 on 30/30 instances), so module search is not the constraint; decomposition costs **0**; frequency filtering saturates instantly; column generation is a **trap** (setting the core to the previous witness pins the incumbent — 37 rounds never moved off 96); RC2 cost is driven by alphabet *density*, not size, with a practical cap around 230 masks.
- **The result that matters** (§5 L10): the glue-conditioned population — 11,778 masks, generated without reading any circuit — **contains all 88 gate masks of three separate record 88s** and 87/88 of two more. Since a record's gate-mask set is a closed feasible set, `floor(population) ≤ 88` is a **theorem, not a hope**. The whole remaining gap localises to selection under the solver's ~280-mask cap: module search 0 gates, decomposition 0, coverage 0, glue ≤ 4.
- Code: `wave6/modular_syl/{galph,genall,flinc,asearch,p0exact,gfloor}.py`
- Generality: MC-HARDCODED (the 7-pattern residue decomposition is from Sun–Yang–Li for this matrix)
- Phase-2 verdict: **keeper — the single most promising unfinished line in the slice.**

#### latent-interface (gauge) climb
- Family: search in a transformed space
- What it does: writes a circuit as `B·A + D = M` and walks the *latent interface* rather than the circuit itself, splicing back and oracle-verifying.
- Measured performance: round trip exact (`B·A + D == M`, 40/40 per anchor). **Phase-1 power control passes**: 97→91, 92→90, 91→90, 90→89, all oracle-VALID. Attribution measured: random-gauge operators are a *handicap* (+1.4 … +2.3 gates paired); the chain operator is what descends. Phase 2 and the undocumented Phase 3 ran seven 88-anchors to ~13,000+ interface iterations each — **all pinned at `best 88/88`**, and because the walk runs *at* the anchor's own gate count, any single accepted improvement would have been an 87.
- Code: `wave6/gauge/{climb,latent,analyze}.py`
- Generality: CIRCUIT-GENERIC
- Phase-2 verdict: keeper — it passes its power control, which most instruments in this slice do not.

#### pattern-class exact window floors (Sun–Yang–Li residue classes)
- Family: exact MaxSAT over a literature-derived alphabet
- What it does: restricts the alphabet to Sun–Yang–Li's seven maximal residue patterns (12,945 masks = 3.0 × 10⁻⁶ of 2³²) and computes exact class-window floors by RC2.
- Measured performance: **177 exact floors, zero improvements**, 0.1–230 s each (median ≈7 s) on windows where a bit-vector K−1 rung will not close in 120 s. Every verdict carries its own RC2 witness, so none can be vacuous. D0/D1 lanes swept 20,800 verified distinct 88 mask-sets. Information-rate finding: 3,259 harvest shots yield only **47 distinct sub-problems (0.17/circuit)** versus a diverse lane's 3.9/circuit — a **23× difference in information per solve**.
- The import itself is the durable part: the pattern class contains **32/32 targets and 100% of the gates of all ten reference circuits**, with coverage monotone in circuit quality (V88 99.10%, V89 92.05%, V90 85.99%, Vall 78.73%). Decomposition: our 88@5 = 63 private + 25 shareable; Jean's = 64 + 24.
- Code: `wave6/pattern_class/{cwlib,cwpair,cwfloor}.py`; import in `wave6/literature/`
- Generality: MC-HARDCODED
- Phase-2 verdict: keeper — but note the class **implies** ≤3 planes, so §5 L9 applies to every negative it produced.

#### cube-and-conquer + CryptoMiniSat/Gauss (both measured worthless here)
- Family: SAT scaling attempts
- Measured performance: `march_cu` on a 34,062-var / 355,842-clause rung — `-d 8` gives 256 cubes in 9.5 s and **0 of 256 decided in 9 minutes**; `-d 13` gives 8,192 cubes and cube #0 alone is undecided at 599 s. Verbatim: *"the ×20–100 of the plan is NOT there. Measured multiplier ≈ 1."* CryptoMiniSat with Gauss-Jordan: an XOR scan recovers **6 XORs, all of length 2**, and CMS is **1.1×–4.3× slower than kissat** — the GF(2) structure is consumed at encoding time. The lever that does exist is RC2 floors (≥40×/≥19×/≥15×/≥11× on 200–216-mask alphabets).
- Code: `wave6/sat_boost/cnc.py`, `wave6/sat_boost/tools/cms/`
- Phase-2 verdict: dead-end — do not re-propose cube-and-conquer or native-XOR SAT on this encoding without first re-running these two measurements.

---

## 3. ARTIFACTS (counts + labels)

All commands run from `campaign_87/` unless a path says otherwise.

### 3.1 Circuits

| label | count | command | notes |
|---|---|---|---|
| all `.json` files | 59,485 | `find . -name '*.json' \| wc -l` | mostly individual circuits |
| filenames claiming 88 gates | 20,745 | `find . -name '*gates*' -name '*.json' \| grep -c 88gates` | |
| filenames claiming 87 gates | **2** (+2 by `gateCount`) | `find . -iname '*87gates*'` | **all four are tripwire fakes** — `fake87`, `badfail`, `FAILED_87`; none was promoted |
| `BREAKTHROUGH*.json` | 171 | `find . -name 'BREAKTHROUGH*.json' \| wc -l` | 53×89g, 45×88g, 15×90g, rest 97–127g selftest artifacts |
| the three canonical 88s | 3 | see §1.3 | all re-verified VALID this session |
| imported published circuits | 12 | `ls prior_basins/imported/ agents/lit-88/IMPORTED_*` | Jean 88@7, SYL 89@9, + 10 others, all oracle-VALID |
| oracle-verified 4-plane 88s (wave 6) | **31,016 distinct** | `wave6/discriminate/runs/VERIFIED88_HIPLANE.txt` | 33,821 verified, all at exactly 88; 20 distinct 4-plane masks |
| exactly ρ²-symmetric 90s | 2 | `agents/orbit-ladder/BEST_90gates_*` | previous best symmetric was 94 |

### 3.2 Population / plateau data

| label | count | command |
|---|---|---|
| distinct verified 88 mask sets (wave 2) | 84,989 | `agents/merged-engine/REPORT.md` |
| new distinct 88 mask sets (wave 3) | 54,889 | `wc -l agents/hunt-deeper/population88_new.jsonl` |
| **project total known distinct 88 states** | **≈139,878** | 84,989 + 54,889 |
| distinct verified 88 mask sets (wave-6 fusion scan) | 434,125 | `wave6/fusion_diag/runs/full.jsonl` |
| distinct ≤92-gate mask sets (NRPA) | 1,441,779 | `wc -l wave5/nrpa/out/sub92.jsonl` |
| distinct 89-gate states in the 89 layer | 1,309,223 | `hunt87_layer89/REPORT.md`; packed in `pool/layer89.bin` |
| 88-gate circuits with full masks + oracle flags | 3,254 | `wc -l hunt87_layer89/found88.jsonl` |
| harvest lines across `.pop.jsonl` | 130 files / 13.71 GB | `find . -name '*.pop.jsonl' -printf '%s\n' \| awk ...` |
| the 88-gate vocabulary V88 | **1,112 masks** | `global_vocab/V88.json` — saturated w.r.t. the harvest; **broken by 750+ more in wave 5**, and NRPA found five verified 88s using masks outside it |

### 3.3 Certificates — what each class actually certifies

| class | count | where | certifies |
|---|---|---|---|
| exact k=2 shells (streaming detectors) | **197,072** | `hunt87/detector/swept.jsonl` (148,893) + `tri_hunt/detector/swept.jsonl` (48,179) | for each 88-gate state: all 1,540 remove-2 windows are irreducible. Zero non-empty, zero claims raised |
| exact k=2 + k=3 certificates (family reps) | 76 + 76 = **2,223,760 window decisions** | `families16/certs/*_k{2,3}.json` | complete shells of 76 family representatives, `exhaustive: true`, all `EMPTY` |
| exact k=4 partial | 10 | `families16/certs/*_k4.json` | honestly labelled `EMPTY_PARTIAL`, `exhaustive: false`, ~1% coverage |
| population k=2 (families 1–2) | **84,989 states, all `irreducible_k2`** | `wc -l agents/frontier-exact/work/results_pop/pop_progress.jsonl` → 84989, 84,989 distinct ids | **finished** — see §5 L11; `FACTS.md` §6a still says 51,899 of 84,989 |
| population k=2 (the 987 new88) | 987, all irreducible | `agents/frontier-exact/work/results_residue/residue_progress.jsonl` | |
| population k=3 | 200, all `irreducible_k3` | `agents/frontier-exact/work/results_popk3/k3_progress.jsonl` | **finished** — `FACTS.md` says 19 closed / 181 queued |
| k=4 windows, Jean's 88 | **56,489**, all irreducible | `wc -l agents/frontier-exact/work/results_k4/progress.jsonl` | `FACTS.md` says 32,685 |
| k=4 windows, family-3 anchor | **39,034**, all irreducible | `.../results_k4_f3/progress.jsonl` | `FACTS.md` says 20,432 |
| k=4 windows, independent 88 | **34,599**, all irreducible | `.../results_k4_indep/progress.jsonl` | `FACTS.md` says **9** |
| **total exact window decisions campaign-wide** | ≈165 M+ | `FACTS.md` §6a, plus the above | zero timeouts, zero reducible |
| windowed SAT UNSAT (fixed slot order) | 108 UNSAT / 114 timeout / **0 SAT** | six ledgers under `agents/{sat-deep,loose-sat,family3-sat,frontier-sat}/runs/` | dedupe by `id`, last-wins, or you double-count |
| **order-free** fence UNSAT | **29,125** unsat + 433 trivial-unsat | `grep -o '"status": "unsat"' wave5/fence_sat/runs/*.jsonl \| wc -l` | the only class with **no** slot-order caveat |
| down-step window UNSAT | 82,786 | `grep -o '"status": "unsat"' wave5/burn/downstep/runs/*.jsonl \| wc -l` | + 9 fully exhaustive theorems |
| RC2 exact union floors | **749,150 OPTIMAL** / 125 timeout | `grep -o '"status": "OPTIMAL"' wave5/burn/union_sat/*.jsonl \| wc -l` | exact minimum over a two-circuit mask union; best floor anywhere 88 |
| RC2 exact skeleton floors | 88,908 pools | `wave6/skeleton_pools/ledger.jsonl` | 19.05% floor exactly 88 |
| exact class-window floors | 177 | `wave6/pattern_class/ledger.jsonl` | each ships its own RC2 witness — none can be vacuous |
| convex-block down-set UNSAT | **9** (B=16 ×7, B=17 ×2) | `wave6/dfs_par/psweep.jsonl`, `psweep_b17.jsonl` | each certifies the whole convex down-set of that block; planted controls OK |
| the depth-3 lower bound | 1 | `wave6/lower_bound/cert_depth3.json` (457 K, 23,450 rational duals) | **every depth-≤3 MixColumns circuit has ≥ 80 gates**. **Re-checked in this session**: `python3 certify.py --check cert_depth3.json` → `exact dual value = 47597998171620/1000000000000 = 47.597998 => |L1|+|L2| >= 48 => N_depth3 >= 80` |

### 3.4 Writeups and logs

```
find . -name '*.md' -not -path '*/venv/*' | wc -l   → 412
find . -name 'REPORT.md' | wc -l                    → 36
find . -name 'STATUS.md' | wc -l                    → 63
find . -name 'README.md' -not -path '*/venv/*' | wc -l → 38
find . \( -name '*.log' -o -name '*.out' -o -name '*.err' \) | wc -l → 5004   (405 MB)
```
By region: wave5 271 `.md` / 3,355 logs / 227 MB · wave6 83 `.md` / 627 logs / 37 MB ·
agents 46 `.md` (24 `REPORT.md`) / 504 logs / 4.6 MB · everything else 12 `.md`.

**Documents worth naming individually:** `FACTS.md` (the fact-by-fact sourced
ground truth), `wave5/publication_draft/{DRAFT.md, CLAIMS_AUDIT.md,
PAPER_OUTLINE.md}` (a complete 37 K paper draft with every claim mapped to an
on-disk source), `wave6/lower_bound/THEOREM.md`, `wave5/burn/obstruction/
OBSTRUCTIONS.md`, `wave5/burn/handreduce/WAVE2_INSIGHTS.md`,
`wave5/metareview/SYNTHESIS.md`, `LONGSHOT_RESULTS.md` (including its 12-item
retraction ledger), `wave6/ATTEMPTS_SINCE_PUSH.md` (125 K catalog).

---

## 4. KEEP / DELETE proposal

Everything here is a **proposal**. Nothing was moved or deleted. The slice is
cold — no file has been modified since 2026-08-13 and no process has a working
directory inside it.

### 4.1 DELETE-CANDIDATE — regenerable, no information loss (~9.6 GB)

| class | size | where | why safe |
|---|---|---|---|
| CNF dumps | **5.53 GB** | `wave5/burn/simple/execute/cnf` 3.3 G · `wave5/alphabet_ladder/cnf` 1.5 G · `wave5/metareview/optimality/cnf` 327 M · `d3_sat/runs/cnf` 125 M · `wave6/sat_boost/cnf` 28 M · `wave6/band_hunt/cnf` 25 M · `hunt87_depth4/runs/cnf` 18 M · rest | solver *input*, regenerated by one command; the verdicts are in the ledgers |
| vendored builds and venvs | **1.39 GB** | `wave5/lp_closure/build/abc` 595 M (+mockturtle 87 M) · `agents/lit-88/venv` 210 M · `agents/exact-k4/tools` 187 M (incl. `pypy.tar.bz2` 35 M kept next to its own extraction) · 4 more venvs 35 M each · `wave6/sat_boost/tools` 20 M | rebuildable; ABC/mockturtle commits are recorded in `clone_abc.log` / `clone_mt.log`. **Caveat: see §6 H2 and H3 before deleting `agents/exact-k4/tools` or `agents/loose-sat/kissat`** |
| derived index / packed pools | **1.51 GB** | `global_vocab/states_uniq.bin` 1.10 G · `hunt87_layer89/pool/layer89.bin` 445 M | rebuildable from the harvests (expensive: re-streams 2.9 GB) |
| `.npy` posting index | 0.40 GB | `wave5/alphabet_ladder/work/corpus_index/post.npy` | rebuildable index |
| plane-census re-scan dumps | 0.57 GB | `wave6/discriminate/runs/hiplane_states_{0..3}.jsonl` | a re-scan of `**/*.pop.jsonl`; the 36 MB of `verify88_*.json` is the result and must stay |
| window enumerations | 0.15 GB | `wave6/hp_strike/runs/windows.jsonl` 89 M (`python3 hp.py enum`, ~2 min) · `wave6/band_hunt/runs/windows_splice*.jsonl` 59 M | regenerated deterministically |
| per-window scratch JSONs | ~0.05 GB / 21,076 files | `wave6/pattern_class/runs/tmp_D{0,1}/` | superseded by `ledger.jsonl` |
| `__pycache__` / `.pyc` | 66 MB / 722 dirs | everywhere | |
| exact duplicates | ~27 MB | `wave6/pattern_class/runs/diverse88_shuf.jsonl` (a shuffle of `diverse88.jsonl`) · `wave6/lower_bound/branch_certificates.json` vs `branch_certificates_E18_48.json`, and `branch_summary.json` vs `branch_summary_E18_48.json` — **`cmp`-confirmed byte-identical in this session** | delete the un-suffixed copies only: `THEOREM.md` names the `_E18_48` files as the preserved snapshots, and any `branch_certify.py` re-run overwrites the un-suffixed ones |
| `.dist.jsonl` telemetry with no reader | 0.11 GB | `d3_model/harvest/*.dist.jsonl` | no script in the tree references the `.dist.jsonl` suffix; the sibling `.pop.jsonl` files *are* consumed |

**Subtotal ≈ 9.6 GB reclaimable with zero information loss.**

### 4.2 DELETE-CANDIDATE (second tier) — replaceable but not reproducible (~13 GB)

The `*.pop.jsonl` harvest dumps: **130 files, 13.71 GB.** Each line is one
distinct plateau mask set found by a stochastic search. Re-running the same
search with the same seed does *not* reproduce them (RNG state, load, restart
timing), so they are not "regenerable" — but a fresh run of comparable length
would produce a statistically equivalent population, and the *analyses* that
consumed them (`population88_new.jsonl`, the census files, `found88.jsonl`,
`verify88_*.json`, `fusion_diag/runs/full.jsonl`, all the ledgers) are small and
already on disk.

Biggest single files: `wave5/nrpa/out/sub92.jsonl` 1.45 G · `tri_hunt/runs/`
5.06 G (of which the four cap-4/uncapped-d4 files are 2.8 G of single-basin
92-gate states — a documented "one-directional flood") ·
`wave5/fresh_fleet/runs/` 4.71 G · `agents/hunt-deeper/runs_hunt/` 1.47 G ·
`agents/merged-engine/runs_hunt/` 0.60 G · `hunt87/runs/` 1.01 G.

**Recommendation: keep a representative slice, delete the bulk.** Concretely,
keep (a) `agents/hunt-deeper/population88_new.jsonl` (48 MB, the deduped result),
(b) one `.pop.jsonl` per distinct search *mode* as a format/provenance exemplar
(~10 files, ~1 GB), and (c) everything under 50 MB. That reclaims ~12 GB.
Two cautions: `wave5/nrpa/out/sub92.jsonl` (1.45 GB, 1,441,779 lines) is
**unmined** — exactly five circuits were ever extracted from it, and union_sat's
control shows that pairs of remote circuits hit floor 88 at a measured 0.7% rate,
so it is live pair material (§5 L13). And `hunt87_layer89/pool/` (1.3 GB) is
cheap to keep and expensive to rebuild.

### 4.3 KEEP — unconditionally

- **Every `.md`** (412 files). The prose *is* the result in this slice; several
  directories' entire scientific output is one `STATUS.md`.
- **Every ledger** — `*/ledger.jsonl`, `*/detector/swept.jsonl`,
  `*/runs/results*.jsonl`, `*/progress.jsonl`, `rung_ledger.jsonl`,
  `endpoints.jsonl`, `psweep*.jsonl`. These are append-only and resume by
  skipping ids already present; splitting, sorting, deduplicating or reformatting
  any of them causes silent re-decision or silent skipping.
- **`wave6/lower_bound/`** (12 MB) — the certified theorem, its controls, and its
  audit path.
- **`wave6/dfs_par/ck/`** (16 MB) and **`wave6/runpod/synced/ck_rescue/ck/`**
  (5.6 MB) — accumulated exhaustive-proof checkpoints, including the only
  surviving B=18 work. Resume from `ck_rescue/`, not from `dfs_par/ck/` (§6 H6).
- **`families16/certs/`** (172 files, 700 KB) — self-describing, re-checkable
  irreducibility certificates.
- **`wave5/publication_draft/`** (72 KB) and **`wave5/burn/obstruction/`** (80 KB)
  and **`wave5/burn/handreduce/`** (64 KB) — the highest value-per-byte in the
  whole slice.
- **`agents/lit-88/*.pdf`** (544 KB) and **`base/seeds/`** and
  **`prior_basins/imported/`** — prior art. `base/seeds/` contains the *imported*
  published circuits and must never be flattened into a shared seed pool (§6 H5).
- **All 5,004 log files (405 MB).** Several of this report's findings exist only
  in a log tail. Compression would be reasonable; deletion would not.
- **`novelty/baseline/weights.json`** (357 KB) — the IDF table every "new family"
  claim in the project depends on.
- Every `*gates_depth*.json`, every `BREAKTHROUGH*`, every `FOUND_*`,
  `hunt87/archive/elites.jsonl`, `wave6/discriminate/runs/verify88_*.json` and
  `hp88_anchors.json`, `modular_syl/alph/`.
- **`tri_hunt/supervisor.py.bak-thin`** and **`hunt87/supervisor.py.bak-2026-07-29`**
  — despite the `.bak` extension these are the only record of the fleet
  configurations whose logs are on disk.

### 4.4 KEEP with a note

- `wave6/pod_jobs/queue/` (16 unclaimed jobs) — do not tidy these away; they are
  the highest-value resumable work in the slice (§5 L10).
- `wave5/burn/mutant_cluster/quarantine_misplaced/` (98 files with
  `BREAKTHROUGH_` name prefixes at 88 gates) and
  `wave5/burn/mutant_satrepair/selftest_work/` (101–126-gate selftest artifacts)
  — keep, but see §6 H8: any future `find -name 'BREAKTHROUGH_*'` record detector
  will match them.
- The four `"gateCount": 87` tripwire fakes — keep. They are the evidence that
  the export path rejects a bogus record.

---

## 5. LEADS (sharp-eye findings)

Ordered by value. Confidence labels are per the brief.

**L1 — The campaign's own controls price most of its negatives at LR ≈ 1.00.
[VERIFIED-IN-LOG]** This is the finding that reframes everything else. The same
exhaustive k=2 decider that produced ~165 M "irreducible" verdicts finds **zero
reducible windows on a 97-gate circuit that has a verified 88 nine gates below
it** (`cert_audit/`, 12,241 exhaustive k=2 + 8,400 sampled k=3, zero reducible on
circuits at 97, 94, 92, 91, 90, 89 and 88). Transition distance across 45
circuits with a known better one: min 3, **median 42** — against a certified
radius of 3. The alphabet-ladder track reaches the same conclusion in capitals in
its own `STATUS.md`; fence_sat's positive control goes **0 SAT in 30 windows
across slack 1–9**; `metareview/optimality` measures dead-gate count and
derivation rigidity as identical to four significant figures at 88/89/90/91/92.
*Consequence for phase 2:* every neighbourhood/vocabulary negative in this slice
is true, correctly scoped, and **carries no information about whether an 87
exists.** Also note the inversion `metareview/optimality` found: against a proper
null, real 88s are 4.7× more derivation-**rich**, not rigid — the "2.3 vs 64
options/gate" framing quoted elsewhere is backwards.

**L2 — Why 88 keeps appearing: the instrument stack searched 0.0045% of mask
space, and the answer may be outside it. [VERIFIED-IN-LOG for the measurements,
PLAUSIBLE for the inference]** Wave 6's plane-cage discriminator found that the
≤3-bit-plane confinement every campaign instrument assumes is **not** a property
of optima: a ≥4-plane gate is **free at the plateau** (88 gates on 120 of 120
matched descents, price 0.00) while an equally-rare ≤3-plane quota costs ≈ +0.87
gates — and **31,016 distinct oracle-verified 88-gate MixColumns circuits
containing a 4-plane gate were already on this project's disk**, across 13 run
files from four independent tracks, unseen. Meanwhile `nplanes ≤ 3` is
**195,420 of 2³² masks = 0.0045% of the space**, and the SYL pattern class
(which *implies* nplanes ≤ 3), the skeleton-pool cross generator (an undeclared
4-plane cap in three places) and the plane-local/cross decomposition all live
inside it. Independent corroboration from `novelty/`: 76.4% of 42,763 harvested
88s sit inside a known family, and the only lanes producing off-family material
are the from-scratch constructors; and from `metareview`: the "540,579 distinct
88s" collapse to **~10–15 effective mask alphabets**, with 291,771 sharing one
*set-identical* 113-mask vocabulary. The honest counterweight is also on record:
the ≥5-plane tier is not merely unused but **unbuildable** (buildable rate 0.0000
at p = 5..8, 0 of 7,755 offered masks ever selected across 89,003 floors), and
the down-1 question was asked 626 times on the high-plane family with UNSAT every
time it got an answer. **The reconciliation nobody wrote: the instrument cap that
matters is 3 → 4, not 4 → 5, and no ≤3-plane instrument was ever re-run with a
4-plane alphabet.** That is a concrete, cheap phase-2 experiment.

**L3 — 28 order-free fence windows at budget 87 were prioritised to run first and
never ran. [VERIFIED-IN-LOG, re-verified independently in this session]**
`wave5/fence_sat/STATUS_NOVEL.md` records an audit finding that all 16 decided
windows in the novel-89 queue were at total budget **88**, and that the 28
budget-**87** windows — *"the only ones in this queue whose SAT would be a world
record"* — had never run; it sets `prio = -1` so they run first on resume.
Verified directly:
```
python3 -c "...json.loads over runs/windows_novel.jsonl / results_novel.jsonl..."
totals: Counter({88: 210, 87: 28});  budget-87 windows: 28, with any result: 0
k,n on the 28: (16,14) (18,16) (20,18) (22,20);  7 novel-region anchors
```
`windows_novel.jsonl` mtime Aug 6 14:18 (the fix); `results_novel.jsonl` mtime
Aug 6 12:20 — *before* the fix, never written again. Campaign compute stopped
Aug 11. **Fence is the only certificate class in the project with no slot-order
caveat**, and the ideation round rated it the top unrun lead. Resume:
`bash wave5/fence_sat/launch_novel.sh <procs>` (idempotent).

**L4 — Two independent, cheap, unfinished routes to push the depth-3 bound past
80 toward the "every 87 has depth ≥ 4" theorem. [VERIFIED-IN-LOG]**
(a) `wave6/lower_bound/THEOREM.md` §6 proves the LP is **saturated at 47.598
across cut levels 1–4** and that only branches E ∈ {19, 20} can reach 48, both
sitting at LP value **exactly 48.0** — so everything above 80 is integer
reasoning, and the prepared next command (`node_probe.py 19 29 0 29`, branching
on Σ_{wt=4} y_m) was never run; `ls logs/ | grep node` returns only
`node_19_29.log`.
(b) The **killed** capped MIP had already banked a better bound. `logs/mip3_L1.log`
ends mid-run at 599.5 s with `BestBound 48.44982378` — ⌈48.4498⌉ = 49 ⇒
**N_depth3 ≥ 81** — and it was still climbing (47.598 → 48.450 in 600 s). The
uncapped run reached 49.478 ⇒ **N_depth3 ≥ 82** (`mip3_L1_uncapped.log`, quoted
in §7 of THEOREM.md). `mip3_result_L1.json`, which THEOREM.md tells the reader to
consult for the final number, **does not exist**. Both are solver-claim class,
not certificates — but the certificate machinery exists to convert them.
(c) A *third*, older and completely orphaned route: `d3_model/d3bound.py` lifts
exact MILP solutions on **target subsets** into global bounds, and in **17 minutes
on one core** climbed 32 → 52 → 53 → 59 → **63**, every rung `PROVEN OPTIMAL`,
with rungs getting *better* and each solving in ≤155 s. `logs/d3bound.log` ends
at k=10 with no k=12 attempt and no explanatory note. This is exactly the
integer reasoning wave 6 says is the only way forward, and it was abandoned at
its steepest point before wave 5 or 6 ever knew it existed (the campaign's own
correction chain reads 57 → 66 → 80 and never mentions 63).
Reaching rung K = 55 gives N_depth3 ≥ 88, i.e. **"every 87-gate MixColumns
circuit has depth ≥ 4"** — a publishable theorem.

**L5 — 88 is a genuine attractor across paradigms, and the shape of the
distribution is odd. [VERIFIED-IN-LOG]** `global_vocab/cone_ils.log` — a
cone-vocabulary ILS with no relation to the walk/LNS engine — 529 restarts, cost
histogram `{88: 15537, 89: 2270, 90: 2529, 91: 3907, 92: 2548, 93: 1578, ...}`:
88 is hit **6.8× more often than 89**, and the distribution is **non-monotone**
(89 < 90 < 91 > 92). Local optima pile up at 91 *and* at 88 with a trough
between. The same shape appears in `cone_ils88.log` (285 restarts). Nobody
analysed this. Combined with fresh_fleet's endpoint law (88:52 89:375 90:575
91:359 92:101) — which has its *own* mode at 90 and a secondary structure at 88 —
there is an unexplained two-mode structure in the optimum landscape that no
document addresses.

**L6 — The ρ-class asymmetry: ≤86 trims occur only in ρ-classes {0, 1, 3}, never
in {2, 4, 5, 6, 7}. [VERIFIED-IN-LOG, theorem-shaped, never attacked]** Measured
over 170,921 states in `wave5/burn/simple/execute/`, and it **survives a
DAG-randomization control** (wave-6 A1 audit: "the absence of class 4 is the
theorem-shaped fact"). It reached `wave6/TRIAGE.md` as a live item and was never
given a dedicated attempt. If the absence of class 4 has a proof, it is a
structural obstruction of exactly the kind §5-L7's obstruction hunt concluded
must exist (an invariant of a single circuit, not a count of circuits).

**L7 — Two live obstruction leads left explicitly unexplored.
[VERIFIED-IN-LOG for the statements, OPEN for the payoff]**
(a) **The odd-`a` sector.** `wave5/burn/obstruction/OBSTRUCTIONS.md` §1b proves
(P1/P2) that any 87 whose mask set is exactly ρ- or ρ²-closed must contain an
**odd** number of fixed masks; at 88 the constraint is vacuous. Its own closing
sentence: *"the orbit engine has never walked odd-a configurations"* — both known
symmetric basins (a = 10, a = 16) and the classic 12-mask trick are even-`a`.
Nobody encoded P2 before shutdown. Note the corroborating hint from the
hand-reduction analysis: the natural trimmed hub set {P7, P2, P3} has **odd size
3**, while all known 88s carry an even hub count.
(b) **The v·(1,1,1,1) marker.** §5c: every known 88 — five families and all
134,889 sampled plateau points — contains at least one mask of the form
`v·(1,1,1,1)` with `v` a single bit, while our 89@5, 89@6, the 90s, the 92@4 and
the 97@3 contain **none** (Sun–Yang–Li's 89 carries one). It is flagged
"do not cite as evidence" and correctly kept out of the publication draft — but
as a **falsifiable prediction about any future 87** it is the sharpest structural
regularity anyone measured, and no proof route was ever attempted.

**L8 — Theorem-grade B=16 and B=17 UNSATs that appear in no summary document.
[VERIFIED-IN-LOG, re-verified in this session]** `wave6/dfs_par/psweep.jsonl`
holds **B=16 UNSAT on 7 of 8 anchors** (fromscratch 2.95e11 nodes, depth5,
depth6, depth7 1.22e11, thirdfamily, SIGMA5 1.39e11, alg2; SIGMA7 hit CAP at
5.82e11) and `psweep_b17.jsonl` (written 2026-08-13 09:45) holds **B=17 UNSAT on
SIGMA7 (2.05e11 nodes, 12,678 s) and alg2 (2.33e11 nodes, 14,905 s)**, both with
`"planted_control": "planted ok (17 gates)"`. Under the monotone-improvability
lemma each certifies the whole convex **down-set** of that block. Large convex
blocks were the campaign's own #1 open frontier, and it was partially closed on
the last day with nobody recording it. Related and equally unrecorded:
`wave6/band_hunt/runs/ledger.jsonl` holds **two n=12 UNSATs with controls OK**
(1,491 s and 1,046 s) that push the decided splice frontier from n=11 to n=12,
contradicting three documents that still say "the frontier sits at n=11"; and
`wave6/hp_strike/runs/ledger.jsonl` holds **two more n=12 UNSATs** in 685 rows
where the STATUS reports 626. The B=18 proof work also survives, in
`wave6/runpod/synced/ck_rescue/ck/SIGMA7_B18_*.ck` (36,077 bytes, larger than the
local copy) — resume from there.

**L9 — The wave-6 audit found a blind spot with a measured removal cost of zero,
and the fix was never validated. [VERIFIED-IN-LOG]** The skeleton-pool cross
generator was capped at 4 bit planes in **three undeclared places**; over ten
families it proposed 15,299 masks with plane histogram {2: 11,954, 3: 2,725,
4: 620, **≥5: 0**}. In the auditor's words: *"an 87 with ANY gate mask touching
≥5 planes escapes every T1 query past and future — structurally, not
probabilistically."* Removal cost measured at **zero**. A patch was applied
(`PLANE_CAP=8`) — and `wave6/highplane/hp_patchcheck.py` then showed the patch
*draws exactly the unbuildable kind*: `clean_and_repair` deletes two thirds
(324 proposed → 107 surviving, 0.69% of pool content). So the hole was found,
patched, and the patch was measured ineffective, all within 24 hours, and the
track's own scoreboard still lists the ≥5-plane tier as an open frontier.

**L10 — The declared milestone job was queued, flagged "run FIRST" in two
documents, and never executed. [VERIFIED-IN-LOG, re-verified in this session]**
`wave6/modular_syl/` established a result that is stated as a theorem, not a
hope: the **glue-conditioned mask population (11,778 masks, generated without
ever reading a circuit) contains all 88 gate masks of three separate record 88s**
and 87/88 of two more. Since a record's gate-mask set is a closed feasible set,
`floor(population) ≤ 88` follows. The entire remaining gap is localised —
module search 0 gates, decomposition 0, coverage 0, glue ≤ 4 — to **selection
under the RC2 solver's ~280-mask alphabet cap**. The direct test is 16 `rc2_floor`
jobs on the conditioned alphabets (|A| = 299 … 11,778):
```
ls wave6/pod_jobs/queue → 16 files, all A7b_R_*   (queue_done 78, deferred 20, results 78)
```
All 16 are **still unclaimed**; the rented pod ran the low-priority `A7b_B` batch
instead and then died. This is one RC2 call per alphabet and it is the cleanest
statement anywhere in the slice that 88 is a **solver-capacity artifact of the
instruments rather than a measured optimum**.

**L11 — Frontiers the campaign lists as open are actually finished, in an
unreported directory. [VERIFIED-IN-LOG, measured in this session]** The
undocumented `agents/frontier-exact/` ran the k=4 closure and the population
sweeps that `exact-k4`, `pop-decider` and `family3-exact` all listed as their
"next step", and nobody ever tabulated the ledgers:
```
wc -l agents/frontier-exact/work/results_pop/pop_progress.jsonl   → 84989  (84,989 distinct ids)
   all verdicts irreducible_k2      FACTS.md §6a says 51,899 of 84,989, "33,090 remain, ~2.9 h"
wc -l .../results_residue/residue_progress.jsonl → 987   all irreducible_k2
wc -l .../results_popk3/k3_progress.jsonl        → 200   all irreducible_k3
   FACTS.md says "19 closed exhaustively, 181 selected states remain"  (19 + 181 = 200)
wc -l .../results_k4/progress.jsonl        → 56489  all "irreducible"  (FACTS.md: 32,685)
wc -l .../results_k4_f3/progress.jsonl     → 39034  all "irreducible"  (FACTS.md: 20,432)
wc -l .../results_k4_indep/progress.jsonl  → 34599  all "irreducible"  (FACTS.md: 9)
```
So: **84,989 + 987 + 53,902 (family 3, already closed) = 139,878 = the entire
known 88 population is proven k=2-irreducible**, not the 105,801 on record; the
k=3 queue is empty; and k=4 coverage on the three anchors is roughly double what
is published. Two consequences. First, `FACTS.md` §6a and `FINAL_REPORT.md` should
be corrected upward before any public statement quotes them. Second — and this is
the sharper point — **L1 applies to all of it**: more irreducibility at radius ≤4
is exactly the evidence class the controls measured at LR ≈ 1.

**L12 — A pre-registered prediction was refuted by its own lane and the STATUS
still records it as confirmed. [VERIFIED-IN-LOG, re-verified in this session]**
`wave6/hp_strike/STATUS.md` registers: *"if the frontier is really about shape,
then windows at n = 12, 13, 14 with |req|/n ≥ 0.85 should decide FAST"*, records
the first two rows as *"Consistent with CONFIRMED"*, and states the decision rule
— *"REFUTED if they time out anyway."* `logs/laneR.log` then runs on: the last
eight rows are all `"n87": 14, "nreq": 13` (ratio 0.929), `"status": "timeout"`,
`"t": 600.03`, `"control": "OK"`, `ctl_gates: 88`. **8/8 timeouts with passing
controls — the hypothesis is refuted at n = 14** and n does impose a real cost the
ratio cannot buy back. `python3 hp.py report && python3 compare.py` settles it in
seconds.

**L13 — Large generated data that was never examined. [SMELL]**
`wave5/nrpa/out/sub92.jsonl` — 1.45 GB, 1,441,779 lines, every distinct ≤92-gate
mask set NRPA produced including 1,400,343 distinct 88s. Exactly **five** circuits
were ever extracted from it (`NOTES.md`), and nothing else in the campaign reads
it. Given `union_sat`'s measured control (unions of two remote circuits hit floor
88 at 0.7%), this is unmined pair material. Similarly:
`d3_model/harvest/*.dist.jsonl` (115 MB) has no reader anywhere in the tree;
`hunt87`'s detector **dropped 64,421 states** on backlog overflow that were never
decided (recoverable by re-running the detector from offset 0);
`agents/frontier-d6sat/` (94 MB, including a 43 MB `grow_a800.jsonl`) has zero
prose anywhere.

**L14 — Solver runs that were fully encoded and then died unnoticed. [VERIFIED-IN-LOG]**
Three `hand_surgeon` jobs — `conemix_dec87.log` (232 B), `conemix_exact.log`
(131 B), `conemix_exact32.log` (239 B) — each ends on its encoding line
(2,083,417 clauses in one case) with no verdict, ever; the STATUS says "jobs left
running detached" at session end. `global_vocab`'s three most expensive CP-SAT
logs (`B_v88_k87.log`, `B_v88cut.log`, `B_v89cut.log`) end mid-banner with the
model built and no result — **including the K=87 decision instance**. The
`wave6/literature` pattern-class K=87 rung on the best-conditioned alphabet the
project ever had ran with a **passing SAT control** (3,143 s) and then timed out
after **28,800 s** with verdict UNDECIDED, recorded nowhere. Wave-1 `sat-window`'s
25 timed-out windows are **not reconstructible** — their removal sets were never
logged, so they cannot be cited as a resumable frontier.
Still-open SAT windows at budget 87, with resume state: **4** on Jean's 88
(k=13–15), **3** on the independent 88 (k=12–13), **20** on family 3 (k=13–16),
plus **18** in the unreported `frontier-sat` at k=13–16 that were only ever given
2,700 s. Note the compute mistake in that last group: `loose-sat`'s four survivors
had already timed out at 4,800 s each and were re-run at **2,700 s** — 44% less
compute than they had already survived — while the recommended `--timeout 21600`
overnight run never happened.

**L15 — Contradictions and stale summaries to reconcile before publishing.
[VERIFIED-IN-LOG]**
- The "symmetric sector floor = 90" cited campaign-wide is **not a theorem**: the
  best reached in `wave5/burn/oddparity/` is 91, every UNSAT there is alphabet-
  and depth-conditioned, and the one sector-scale run (`symmat`, 1,517 masks)
  returned **UNKNOWN at K = 89, 88 and 87** after 2,455 s each. The sector is
  undecided below 90.
- "ρ-symmetry costs ≈108, so the ρ sector is expensive" carries no information:
  `wave6/fresheyes_a/equiv.py` prints `plain greedy CSE: 108` and
  `equivariant greedy CSE: 108` — 108 is simply what unrestricted greedy gets.
  The correction was never propagated into `OBSTRUCTIONS.md`.
- `wave5/STATE_2026-08-11.md` §2's free-closer paragraph is retracted by its own
  §CORRECTION 100 lines later; the retracted text is the first thing a reader
  hits. Anyone quoting §2 without scrolling will publish a false claim.
- `LONGSHOT_RESULTS.md` carries a **12-item retraction ledger**, and **all 24
  wave-1..4 agent REPORTs predate all 12 corrections.** Check any pre-2026-07-30
  number against it — including #8 ("139,878 proven k=2-irreducible" — only
  105,801 were, though L11 now makes the original claim true for a different
  reason), #11 (16 families → 11 proven-distinct) and #12 (11 distinct 88@5s →
  one value set in 7 gate orderings).
- The append-only ledgers re-log ids across phases, so a raw
  `grep -c '"unsat"'` double-counts. Always dedupe by id, last-wins.
- All 72 returned `A7b_B` pod rungs are **vacuous by the project's own rule** —
  in every one of the 18 families the top (control) rung is UNSAT or TIMEOUT,
  never SAT; 12 families have a *failed* positive control, which says the claimed
  module size `b` was itself wrong. Nobody ran this check.
- `SHUTDOWN_PLAN.md`'s final step was to write `CAMPAIGN_FINAL.md`.
  **It does not exist.** Nine wave-6 subdirs created on Aug 12–13 (`discriminate`,
  `fusion_diag`, `hp_strike`, `highplane`, `gauge`, `modular_syl`, `fresheyes_a`,
  `fresheyes_b`, `pod_jobs`, `runpod`) appear nowhere in `ATTEMPTS_SINCE_PUSH.md`,
  which stops on Aug 12 morning. **That is where the unfinished threads are.**

**L16 — Wall-clock contamination in archived certificates. [VERIFIED-IN-LOG,
unresolved]** `wave5/STATE_2026-08-11.md` lines 100–102: *"this box's clock steps
backwards and the ARCHIVED exact-decider certificates use wall-clock deadlines
(burn deciders were immunized; archived ones were not) — audit before
submitting."* Corroborated by a negative wall time in a ledger
(`burn/oddparity/ledger.jsonl`: `"wall": -8.5`) and by a whole segregated
`ledger_preclockfix.jsonl` (1.5 MB). Wave-6's `COMMON_BRIEF.md` repeats the
warning as a standing rule. **Any archived certificate whose completeness
depended on a wall-clock deadline is suspect, and the publication package depends
on them.** Never resolved.

**L17 — Two unexecuted, fully specified structural hypotheses. [PLAUSIBLE]**
(a) `wave5/burn/handreduce/WAVE2_INSIGHTS.md` (48 KB of hand analysis, no code)
identifies a **parity-hub law** — the 88/89 separator is exactly "materialize ≥1
plane parity as a cross-orbit hub", each hub costs exactly one gate and serves
~3 targets in two orbits, and 89/90/92/96/97-gate circuits have none. Its
corpus-wide observation: **all observed hubs lie in {P1, P2, P4, P6} — precisely
the parities usable without touching P7 — while P7 is the unique quadruple-duty
mask**, appearing in all four carry-orbit terms; every circuit instead re-buys P7
fragments per letter, and "the invariant 21-gate xtime-carry toll is exactly the
cost of refusing to materialize P7 once." It ends with a concrete instruction:
*exact SAT/ILP re-synthesis of just the carry-orbit block (16 targets, frozen
non-carry interface and pair layer) over a basis extended with a materialized P7,
asking for ≤ current block cost − 1*, with the prediction that the hub-free
version returns UNSAT and *"the hub-extended instance is where 87 lives if it
exists."* Uniform across all eleven circuits examined. This block re-synthesis was
never run.
(b) `wave5/STATE_2026-08-11.md` §2 and `wave5/burn/downstep/` measured that the
**one improving window whose shape the project holds is disconnected**
(four pairwise non-adjacent masks), and that every generator ever run samples
connected sets (`cluster` 0/197,000, `cone` 0/118,000). Wave 6 *did* build the
disconnected generator and it worked spectacularly as an enrichment device
(~3,600×, 872 theorem-grade decisions, 0 SAT) — but it was killed at n ≤ 9 while
the new encoder reaches n = 14–16. **The predicate and the encoder were never
combined.**

**L18 — Small things worth one command each. [SMELL]**
`agents/hunt-88at6/shallow_pool/prepool_d6.pop.jsonl` is **6 lines** (verified)
where the launcher's own comment describes it as the shared shallow mask universe
for six workers — which would explain why four cap-6 workers produced 14, 16, 66
and 264 harvest lines after a 13,500 s budget while a sibling produced 93,621.
`d3_sat/runs/splitR1.log` is a wall of `NameError: name 'lemma' is not defined`
at `work/d3exact.py:318`, repeated for every instance, with the driver never
checking the exit code. `d3_sat/runs/split_B64.jsonl` covers `n1 ∈ 0..18 ∪
45..64` only — **the 26 hardest middle cases (n1 = 19..44) were never run**, so
the "depth-3 ≤96 is UNSAT" reading of `splitL2.log` is not supported.
`wave5/alphabet_ladder/CUBE_p250_K87.cubes.jsonl` is **0 bytes**.
`wave6/dfs_par/ck/SIGMA7_B17_41-42-...-97.ck` is a **134-byte stub** whose S-list
differs by one element from the real 2.2 MB checkpoint — easy to mistake for
resumable state.

---

## 6. HAZARDS

**H1 — Absolute paths everywhere.** 466 project `.py`/`.sh` files hard-code
`/home/joebachir20/xor_ui/slp-plateau-search` (`grep -rl ... | grep -v
site-packages | wc -l`). Per region: wave5 227, wave6 106 (the rented pod solved
this with a **symlink on the remote box**, not by fixing the files), agents 24,
mid-campaign 43. **Every documented resume command is an absolute `cd`.** Worse,
absolute paths are baked into *result data*, not just code —
`wave5/burn/oddparity/ledger.jsonl` records alphabet paths inside ledger lines,
and the ledgers are append-only by convention, so they cannot be rewritten.
Moving `campaign_87/` breaks essentially every resume path in it.

**H2 — A cross-agent symlink by absolute path.**
`agents/frontier-sat/kissat/src/makefile → /home/.../agents/loose-sat/kissat/makefile`.
Deleting or relocating `agents/loose-sat/` silently breaks `frontier-sat`'s
solver rebuild. Five venvs also bootstrap off `/home/joebachir20/anaconda3/bin/python3`
by absolute symlink and are not relocatable.

**H3 — Three detectors depend on a PyPy tree inside another agent's directory.**
`hunt87/supervisor.py:86`, `tri_hunt/supervisor.py:99` and
`cascade6/supervisor.py:107` all construct a path ending
`pypy3.11-v7.3.23-linux64/bin/pypy3`, resolving to
`agents/exact-k4/tools/`. Pruning that 187 MB toolchain (listed as a delete
candidate in §4.1) silently drops all three detectors from ~2.5 sweeps/s to
~0.5 (they fall back to CPython) with no error.

**H4 — Harvest-globbing scripts reach across the whole campaign.**
`hunt87_layer89/harvest89.py`, `families16/harvest.py`, `d3_exact/screen.py` and
`wave6/discriminate/scan_hiplane.py` all glob `hunt87/runs`, `hunt87_basin4`,
`hunt87_depth5` and `agents/*/runs*`. Deleting the `.pop.jsonl` bulk (§4.2) makes
the layer89 pool, the families16 census and the plane census non-reproducible —
their *outputs* survive, their derivations do not.

**H5 — `base/seeds/` contains the imported published circuits.**
`base/seeds/IMPORTED_88.json` and `IMPORTED_89_sunyangli.json` sit alongside
own-lineage seeds. `tri_hunt/README.md` is explicit that imported material must
never enter a search directory's pool, and the whole clean-lineage argument in
`PUBLICATION_BRIEF.md` §2 depends on it. **Do not flatten `base/seeds/` into a
shared seed directory.**

**H6 — Checkpoint traps.** Resume B=18 from
`wave6/runpod/synced/ck_rescue/ck/` (36,077 B, 2026-08-13 19:07), **not** from
`wave6/dfs_par/ck/` (7,590 B). `wave6/dfs_par/ck/SIGMA7_B17_41-42-...-97.ck` is a
134-byte stub next to the real 2.2 MB checkpoint;
`ck_rescue/ck/fromscratch_B16_35-47-...-110.ck` is 0 bytes.
`wave6/lower_bound/branch_certificates.json` is overwritten by any
`branch_certify.py` re-run — `branch_summary_E18_48.json` and
`branch_certificates_E18_48.json` are the preserved copies.

**H7 — Append-only ledgers with skip-by-id resume.** `fence_sat`,
`burn/union_sat`, `burn/downstep`, `alphabet_ladder`, `steinberg`, `mine_89only`,
`skeleton_pools`, `band_hunt`, `hp_strike`, all `progress.jsonl` files — every
one resumes by skipping ids already present in its own ledger. Splitting,
sorting, deduplicating or reformatting any of them causes silent re-decision or
silent skipping. `burn/downstep/runs/{A..H}.done` hold *line numbers* positionally
coupled to `jobs_[A-H].txt`; editing a jobs file invalidates the done file with
no error.

**H8 — Filename-based record detection will produce false positives.**
`wave5/burn/mutant_cluster/quarantine_misplaced/` holds 98 files named
`BREAKTHROUGH_88gates_*`, and `wave5/burn/mutant_satrepair/selftest_work/` holds
`BREAKTHROUGH_{101..126}gates_*`. Any successor script that globs
`BREAKTHROUGH_*` to detect a record will match them. **Gate on `gateCount` and
on `verify_circuit.py`, never on the filename.** Note also
`agents/frontier-sat/runs/cnf/9f3c9acebff6_fearly.out` is a **zero-byte** result
file from a killed run — a naive "did it produce output?" check passes.

**H9 — Stale STOP files and PID files.** Live `STOP` sentinels exist in
`hunt87/`, `tri_hunt/`, `wave5/fresh_fleet/`, `wave5/mine_89only/`,
`wave5/evolve/`, `hunt87/selftest_run/`. **`fresh_fleet` and `evolve` restart on
`rm -f STOP`** — copying the tree without the STOP file, or a cleanup step that
removes zero-byte files, would relaunch detached compute. `agents/hunt-88at6/
launch.sh` does `rm -f ../STOP_BREAKTHROUGH` as its second action. 52 stale PID
files sit in `hunt87_layer89/pids/`, `families16/pids/`, `hunt87_basin4/pids/`,
`novelty/descent/pids`, `d3_model/runs/pids.txt`; the launchers read them to
decide whether a shard is already running, so a fresh launch could refuse to
start or signal a recycled PID. (`hunt87`/`tri_hunt`/`cascade6` are safe — their
`Fleet._owned()` verifies `/proc/<pid>/cmdline`.)

**H10 — Backups that do not look like backups.**
`tri_hunt/supervisor.py.bak-thin` is the only record of the original 15-worker
fleet configuration whose logs are on disk (the fleet was thinned mid-run to give
cores to `global_vocab`, and README/REPORT were never updated — so any throughput
computed from `STATUS.md` is wrong by ~4×). `hunt87/supervisor.py.bak-2026-07-29`
is the same kind of artifact. `wave6/audit/{gen,loop,worker}.py.new` are patched
sources kept beside their patch — verify they match what actually ran before
trusting either.

**H11 — Bundled binaries with no build script.** `d3_sat/bin/kissat_d3`,
`hunt87_depth4/bin/kissat_d4`, `hunt87_depth5/work/kissat_d5push` (554–567 KB
each). No version string is recorded in any log; they cannot be rebuilt from this
tree.

**H12 — The clock.** This box's wall clock steps backwards (see L16). Any
timestamp comparison across files in this tree is unreliable, and archived
certificates that used wall-clock deadlines were never audited.

---

## 7. GAPS

1. **I did not re-verify the ~165 M exact window decisions or any SAT UNSAT.**
   Every certificate count in §3.3 is a line count or a ledger tally, not an
   independent re-check. **The one exception is the depth-3 certificate, which I
   did re-check in this session** — `python3 certify.py --check cert_depth3.json`
   returns `exact dual value = 47597998171620/1000000000000 = 47.597998 =>
   |L1|+|L2| >= 48 => N_depth3 >= 80`. The campaign's only unconditional theorem
   stands, independently of the session that produced it.
2. **I verified four circuits, not thousands.** Bulk re-verification is exactly
   what the brief forbids. The 20,745 files named `*88gates*` are *claimed*, not
   confirmed, by this report; the campaign's own verify-before-claim discipline
   and the four tripwire fakes are the evidence that the claim is sound.
3. **The `.pop.jsonl` bulk (13.71 GB) was line-counted, not read.** Whether the
   populations contain anything the analyses missed — L13's unmined
   `sub92.jsonl` in particular — cannot be settled without compute.
4. **`agents/frontier-d6sat/` (94 MB) and `agents/hunt-88at6/`'s 266 MB remain
   under-analysed.** Both have zero prose; I tabulated their ledgers but did not
   reconstruct what their `grow`/`ext`/`rigid` passes were testing.
5. *(closed)* The duplicate `branch_certificates` / `branch_summary` pairs in
   `wave6/lower_bound/` are `cmp`-confirmed **byte-identical** — see §4.1.
6. **The `wave6/fresheyes_a` / `fresheyes_b` verdicts exist only as three `.txt`
   dumps.** They were inputs to the `CAMPAIGN_FINAL.md` that was never written,
   and `fresheyes_b`'s central conclusion (≤3-plane confinement is a fixed point)
   was refuted the same afternoon by `discriminate` — a reconciliation nobody
   wrote and I could only reconstruct, not confirm from a primary document.
7. **Provenance of two mid-campaign audits is unrecoverable.**
   `hunt87_prov/` and `hunt87_prov5/` kept **no output at all** — no log, no
   JSON. Their conclusions (independence of the family-4 88@6; the lineage chain
   of the derived 88@5 through Jean's circuit) survive only as prose in
   `hunt87/README.md`. `prov_d5fs/` did keep its outputs and is the model.
8. **`d3_model/runs/results.json` has an mtime of 2026-08-18 18:05** — three
   weeks after every other file in that directory, i.e. *after* the campaign
   ended. Something in a later fleet rewrote it. I did not trace what.
9. **I could not determine whether the k=4 ledgers in `frontier-exact` are
   complete or merely large.** They contain 56,489 / 39,034 / 34,599 rows, all
   `"s": "irreducible"`, but the driver logs no completion marker, so I can state
   the count and the verdict but not "the closure is finished".
10. **Disk figures are `du`/`find` measurements at one instant** and include
    ~1.4 GB of vendored third-party trees that a `du -sh` on a fresh checkout
    would not reproduce.
