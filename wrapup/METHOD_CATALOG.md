# METHOD CATALOG — the master toolkit

**Total distinct methods catalogued: 309** (in 14 families), distilled from ~350
raw entries across the ten slice reports in `wrapup/reports/`. **At least 36
entries are merges** of two or more slice entries describing the same method
under different names — 20 of them carry an explicit **Incarnations** line naming
every version and the order they evolved in; the rest name their sources inline.
**11 numeric conflicts** between reports are collected in Appendix B; **six of
them** (Appendix B #1–#6) also carry an inline `CONFLICT` marker in their entry —
#7–#11 do not, and one inline marker (E13's "243 = 3⁵") is a conflict that is
*not* in Appendix B. *(Corrected 2026-08-29 by `wrapup/day2/CATALOG_AUDIT.md` §4;
the original text claimed all eleven were flagged inline.)* **9 entries** were too
thin in their source report to fill the schema; **all nine have since been
completed** — see Appendix A.

This catalog is the backbone of phase 2 (aiming the toolkit at another circuit,
e.g. `aes_inv_mixcolumns`). Read §Starter kit first if you want the short list.

> ⚠ **Audit caveat (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`).** A 62-entry
> adversarial sample against primary sources returned **37 PASS / 24 FAIL / 1
> UNVERIFIABLE**. Two document-wide defects survive this edit and you must read
> around them: **(1) 130 of the 309 entries carry no `Generality` line at all**
> — absence of a label is not evidence of portability, and in nine audited cases
> where a label *was* present the code contradicted it. **(2) Numbers in this
> file were copied from the slice reports, not re-derived**; where an audited
> figure did not reproduce, the entry now carries an `AUDIT` note. Entries
> audited PASS are marked in §(b)'s index; unaudited entries carry no warranty.

---

## How to read an entry

Every entry keeps the brief's schema:

- **Family** — which of the 14 groups below.
- **What it does** — plain language, no project jargon. A reader who has never
  seen this repo should understand it.
- **Twist** — what distinguishes it from its nearest sibling.
- **Measured** — what its own logs show. Numbers are copied verbatim from the
  slice reports; nothing is averaged, rounded or invented. Where two reports give
  different numbers for the same thing, both are kept and marked `CONFLICT`.
- **Cost** — CPU/wall time where the logs recorded it.
- **Code** / **Logs** — paths, as the slice reports gave them.
- **Generality** — `CIRCUIT-GENERIC` (works on any target matrix as written) /
  `MC-HARDCODED` (specific to AES MixColumns) / `MIXED` (generic machinery,
  MixColumns constants), plus what would have to change for a new circuit.
- **Incarnations** — for merged entries only: every place this method lives.
- **Phase-2** — keeper / superseded-by-X / dead-end, one line why.

### The problem, in one paragraph (context for a new reader)

AES MixColumns is a fixed 32×32 matrix over GF(2). Computing it means building
each of 32 output bits as an XOR of input bits, using only 2-input XOR gates and
reusing intermediate results. Fewer gates = better. Every signal in such a
circuit is fully described by a 32-bit **mask** (which inputs it XORs), so a
circuit is essentially a *set of masks* that is closed under "each mask is the
XOR of two earlier ones" and contains all 32 targets. The record here is **88
gates**; the refereed bracket is **56 ≤ L(M) ≤ 88**; no 87 was ever found.

### The 14 families

| | family | what it is for | entries |
|---|---|---|---|
| **A** | Verification, oracles and artifact integrity | deciding whether a circuit is real | 11 |
| **B** | From-scratch construction and baselines | getting a first legal circuit with no prior data | 14 |
| **C** | Plateau / local search: engines and move classes | improving a circuit you already have | 27 |
| **D** | Orchestration, fleets, diversity and ops | running many searches without wasting the box | 18 |
| **E** | Exact local certificates (window / shell deciders) | proving "no smaller circuit within radius k" | 19 |
| **F** | SAT / MaxSAT / PB / CP-SAT decision procedures | asking a solver an exact yes/no | 31 |
| **G** | Exhaustive exact searchers, DP and enumeration | solver-free exact answers on small instances | 19 |
| **H** | Class-pricing, block decomposition and generators | deriving a circuit's price from the algebra | 51 |
| **I** | Lower-bound machinery | proving a floor on the gate count | 33 |
| **J** | Structural analysis of circuits and populations | understanding what the circuits are made of | 41 |
| **K** | Tripwires and live detectors | always-on "an improvement is available" alarms | 5 |
| **L** | Controls, calibration and audit instruments | making a negative result mean something | 30 |
| **M** | Hand reasoning and theorem lanes | proofs, no solver | 4 |
| **N** | Documentation, planning and provenance | keeping the record honest | 6 |
| | **total** | | **309** |

**If you read only three things:** the phase-2 starter kit (§a), family **K**
(two free, provably sound "a smaller circuit is available" detectors), and **L2**
(the measurement that repriced most of this project's negative results).

---

# Family A — Verification, oracles and artifact integrity

Nothing downstream in this project is trustworthy without these. On a new
circuit, **port A1 first**.

### A1 · spec-oracle (`verify_circuit.py` / `verify.py`)
- **Family:** verification / ground truth.
- **What it does:** Rebuilds the 32×32 MixColumns matrix from GF(2⁸) arithmetic
  (the code *is* the specification — `xtime`, `gf_mul`, coefficients `[2,3,1,1]`,
  FIPS-197 §5.1.3), then replays a candidate circuit gate by gate over 32-bit
  masks and reports gate count, depth, how many of the 32 target masks appear
  among the built signals, and structural problems (non-2-input gates, forward
  references). Exits 0 iff all 32 outputs are built with no problems and
  (optionally) depth ≤ a cap. Because the map is linear, agreement on the 32 unit
  inputs is a *complete* correctness check.
- **Twist:** it shares no code with anything it checks. It carries a built-in
  spec self-check (`wts.count(5)==20 and wts.count(7)==12`) that fails loudly if
  the rebuilt matrix is wrong, and accepts four circuit encodings (index pairs,
  mask triples, kit format, bare list).
- **Measured:** every circuit claim in the entire tree is defined as "this
  printed VALID". CI runs it on all 8 records at their depth and asserts each
  FAILS one level tighter. In the records repo, 11/11 pass, `ALL CIRCUITS
  VERIFIED`, rc 0, under a second. Campaign-wide: **zero false claims ever**
  (`beat88/analysis/code/spec-oracle.md`).
- **Cost:** milliseconds per circuit.
- **Code:** `verify_circuit.py` (129 LOC, repo root); `verify.py` (178 lines,
  records repo).
- **Logs:** `evidence/RESULTS.md` (output for all 8 records);
  `bounds.json:verified{}`.
- **Generality:** **MIXED, ~30 lines from CIRCUIT-GENERIC.** Only
  `mixcolumns_target_masks()` (lines 37–55) and the weight self-check (line 99)
  are MixColumns-specific. For `aes_inv_mixcolumns`, change the coefficient row
  `[2,3,1,1]` → `[14,11,13,9]` and recompute the expected weight profile.
- **Incarnations:** `root_infra:oracle-verify-circuit` · `records_repo:spec-rebuild-verify` ·
  `campaign_87:spec-oracle` · used unchanged by every other slice.
- **Phase-2:** **keeper, first thing to port.** Nothing downstream is
  trustworthy without it.

### A2 · cleanroom-adversarial-verifier
- **Family:** verification / adversarial checking.
- **What it does:** A second, independently written verifier that never calls
  `verify.py`. Rebuilds MixColumns from a *byte-level* reference (not a mask
  table), does a symbolic output comparison, executes 100,000 deterministic
  random inputs against the byte reference, recomputes gate/depth/fanout/layer
  metrics, and runs a suite of planted defects that must be rejected.
- **Twist:** the adversarial suite. 14 planted-defect cases, each confirmed
  rejected: reversed byte order, reversed bit order, transposed matrix,
  **inverse** MixColumns matrix, corrupted target mask, permuted output bindings,
  removed gate, modified parent pair, duplicated intermediate + dead gate,
  appended dead gate, wrong depth metadata, wrong gateCount metadata, missing
  field, forward reference. This is the only place in the project where a
  verifier's *negative* capability is certified rather than assumed.
- **Measured:** 11/11 circuits clean, "Issues: none" on every one; **14/14
  adversarial cases rejected as expected**.
- **Cost:** 100,000 trials × 11 circuits; seconds to low minutes.
- **Code:** `audit/cleanroom_verify.py` (716 lines).
- **Logs:** `audit/recomputed_metrics.json` (60K), `audit/MATHEMATICAL_VERIFICATION.md`.
- **Generality:** MIXED (same one-constant change). The adversarial suite is
  fully CIRCUIT-GENERIC.
- **Phase-2:** **keeper — port the adversarial-rejection idea first**, since it
  is what makes a "VALID" verdict mean anything.

### A3 · verilog-simulation-crosscheck
- **Family:** verification / third path.
- **What it does:** Emits a Verilog netlist and testbench per circuit; the
  testbench drives each unit input `e_i` and compares the output word against
  **column** `i` of the matrix (not row `T[j]` — the matrix is not symmetric; an
  early commit `5ecfdb5` records this exact bug being fixed). Expected responses
  come from the GF(2⁸) spec, not from the circuit.
- **Twist:** a different language and simulator, so it catches Python-side
  convention errors that both Python verifiers would share.
- **Measured:** Icarus Verilog available; `tests/test_verification.py::test_verilog_path`
  gates it in CI when present.
- **Code:** `scripts/generate_verilog.py` (with `--check` drift mode),
  `verify_verilog.py`. **Logs:** `verilog/` (22 tracked files).
- **Generality:** MIXED — same target-constant change.
- **Phase-2:** keeper, low priority. Value is convention insurance, not throughput.

### A4 · canonical-gate-hash (two-hash discipline)
- **Family:** artifact integrity / identity.
- **What it does:** Defines a circuit's identity as SHA-256 over the UTF-8 bytes
  of the compact JSON `{"inputCount":32,"gates":[...]}` with keys in that order —
  a formatting-independent fingerprint — alongside a plain file-bytes hash.
- **Twist:** the *two-hash* discipline. The canonical hash survives re-formatting;
  the file hash does not. `RECORDS_REPO_PATCH.md` §1 shows the 92 @ 4's canonical
  hash matching byte-for-byte between two repositories while its file hash does
  not, because the repos hold differently pretty-printed copies.
- **Measured:** 11/11 hash fields match.
- **Code:** `scripts/reproduce_canonical_hashes.py --check-bounds`.
- **Generality:** CIRCUIT-GENERIC. **Phase-2:** keeper — adopt verbatim.

### A5 · generated-artifact-drift-check
- **Family:** repository hygiene.
- **What it does:** Every derived file (listings, Verilog, audit reports) has a
  `--check` mode that fails if the on-disk file has drifted from the JSON it was
  generated from; the test suite asserts all of them.
- **Twist:** makes hand-editing a generated file a *test failure* rather than a
  silent inconsistency.
- **Measured:** 12 tests, 4 happy-path + 8 rejection/drift.
- **Code:** `tests/test_verification.py` + `--check` in the two generators.
- **Generality:** CIRCUIT-GENERIC. **Phase-2:** keeper.

### A6 · depth-tightness-CI + reference-differential unit tests
- **Family:** verification hygiene.
- **What it does:** (a) CI verifies all 8 records at their stated depth **and
  asserts each FAILS one level tighter**, keyed on the *file* never on the
  (gates, depth) pair (two records share (88,5)). (b) 24 unit tests check the
  spec's weight profile, oracle rejection of forward references / truncation /
  depth violations, the eight records against `spectrum.json` SHA-256s, and — the
  valuable part — the fast kernels (`relax`, incremental closure, `remove_query`,
  exact `_repair`) against **plain reference implementations written out in the
  same file**.
- **Twist:** differential testing of a fast kernel against a slow obvious one,
  in-file, is what makes the engine's negatives believable.
- **Measured:** whole module runs "well under two minutes", stdlib-only.
- **Code:** `tests/test_invariants.py` (541 LOC), `.github/workflows/verify.yml`.
- **Generality:** MIXED — record list and weight profile hardcoded; the
  differential-testing pattern is generic.
- **Phase-2:** **keeper, and copy the pattern** for any new target's kernels.

### A7 · batched-numpy verifier (shared B2)
- **Family:** verification infrastructure.
- **What it does:** Verifies whole batches of circuits at once with numpy,
  reporting live-gate counts, at ~**400 k circuits/s**.
- **Twist:** it is fast enough to be used *inside* a search loop rather than at
  the end of one.
- **Measured:** M4's 25 checks + a **100,009-circuit fuzz, 0 failures**.
- **Code:** `beat88/methods/shared/verifier.py` (adopted from
  `beat88/methods/m4_inverse/verifier.py`).
- **Generality:** CIRCUIT-GENERIC except the target set. **Phase-2:** keeper.

### A8 · realize-completion (value-set → program → oracle in one call)
- **Family:** verification infrastructure.
- **What it does:** Takes a *mask set* (which is all most instruments produce),
  synthesises an actual gate list for it, and pushes it through the oracle — in
  one function call.
- **Twist:** it closes the gap between "the search says it found something" and
  "a verified circuit exists on disk"; it is what turned 12 completion candidates
  into **12/12 VALID at 88 gates**.
- **Code:** `beat88/methods/m4_inverse/realize_completion.py`.
- **Generality:** CIRCUIT-GENERIC. **Phase-2:** keeper.

### A9 · dead-gate-strip + honest-count accounting
- **Family:** circuit post-processing / measurement hygiene.
- **What it does:** (a) removes gates whose output is neither a target nor
  consumed — free and sound; (b) records every mask collision between two blocks
  with both block tags, so the gap between a model's price and the emitted count
  always has a *named* cause. The requested `--count` is checked against the
  **emitted** count.
- **Twist:** predecessors reported asked-97 → emitted-95 and asked-107 →
  emitted-103 **with no cause**. This names it.
- **Measured:** at the 88@7 cell, delta +0. `fleet12/laneKNOBS` later measured
  that **five of its 88s exist only because the strip runs** — the strip is not
  cosmetic.
- **Code:** `fleet8/unified/code/assemble.py` (`MaskSet.collisions`,
  `strip_dead_gates`), `generate.py:88-119`.
- **Generality:** CIRCUIT-GENERIC. **Phase-2:** **keeper — mandatory.** Any count
  reported without this is unreliable in both directions.

### A10 · validated primitive kernel suite (shared B1–B5)
- **Family:** infrastructure.
- **What it does:** Five validated primitives every lane imports: a C
  closure/feasibility/trim/complete-repair/complete-neighbourhood kernel (B1), the
  batched numpy verifier (B2, = A7), a streaming population index (B3), intrinsic
  circuit descriptors (B4), and a gauge canonicaliser (B5, = J5).
- **Measured:** B1 — 60,001 randomised states vs `pipeline/engines.py`,
  **885,634 comparisons, 0 mismatches**. B3 — 850,784 states brute-force
  cross-checked, **0 mismatches, 33 MB RAM**. B4 — 0 mismatches vs three
  independent references. B5 — both closed 88@5 components collapse (2,187 → 1
  core; 729 → 1 core). Speeds: `feasible()` 8 µs, `trim()` ~25 µs,
  `repair_degrees()` ~5 ms, complete `neighbours()` 7–20 ms. Passes on gcc 13 and
  gcc 11.4, ctypes only.
- **⚠ Recorded hazard:** the C `trim` is witness-dependent — **14.5 % mismatch vs
  Python (327/2,253), concentrated entirely above 88 masks, 0/1,671 at exactly
  88**. Never swap trim backends mid-stream in a structure that records trimmed
  states.
- **Code:** `beat88/methods/shared/{kernel.py,gauge.py,verifier.py,popindex.py,descriptors.py,fixes.py,csrc/,lib/,tests/}`.
- **Data:** `shared/index/pop88/` (460 MB).
- **Generality:** CIRCUIT-GENERIC except the target set in `kernel.load_circuit`.
- **Phase-2:** **keeper, port-first.** Cheapest thing to carry to a new circuit:
  swap the target matrix and the suite runs.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — Generality label wrong, and it names the wrong file.** `kernel.load_circuit` is a JSON loader containing no target set; the 32 MixColumns targets are rebuilt **inside the C kernel** (`csrc/slp_kernel.c:34` `TARGETS[32]`, `:38` `xtime_` with `0x11B`, `:47` `coef[4]={2,3,1,1}`), and the whole kernel is uint32 / 32-input width-locked. Correct label **MIXED**; the port is not "swap the target matrix" but edit and rebuild the C. Two further defects: "B3 — 850,784 states brute-force cross-checked" misstates the scope by five orders of magnitude (850,784 is the number *indexed*; the brute-force check was 6+6 queries plus 300 sampled ids); and the B5 validation log's own final line is `=== B5 gauge canonicaliser: FAIL ===` (the 88@6 component gives 15 distinct cores), which this entry omits.
- **COMPLETED (2026-08-29):** the three `beat88/analysis` descriptor rows that became this suite's **B4** (`shared/descriptors.py`) were Appendix A item 7; they are now written up as a single full entry at **Appendix A §A·7**.

### A11 · SAT-benchmark packaging + semantic-identity proof
- **Family:** reproducibility engineering.
- **What it does:** The live campaign never writes a DIMACS file (it hands
  `cnf.clauses` straight to a solver), so a shipped benchmark's identity had to be
  *established*: same instance object (pinned SHA-256, re-derived through the
  running lane's own assertion module), same encoder call, clause-for-clause round
  trip (clause-order sha256 identical both ways), and behavioural agreement (three
  lower levels solved **from the shipped files** returning the verdicts the
  campaign banked with a *different* encoder). The decoder re-evaluates all
  **285,480 clauses** under the model rather than trusting the solver.
- **Measured:** `sha256sum -c SHA256SUMS` → **51/51 OK**. Difficulty gradient
  measured, not guessed: 12.1 s (k=9) → 130 s → 708 s → 5,762 core-s → 105,083 s
  on 8 cores (k=13); growth 26.4× then 20.2×, pricing k=14 at ≈**650–1,100
  core-hours**.
- **Code:** `experiments/sat_package/code/{gen_cnf,check_cnf,make_planted,plant_model}.py`,
  `decode_solution.py`.
- **Generality:** CIRCUIT-GENERIC as a template; the instance is MC-specific.
- **Phase-2:** **keeper, top tier** — the model for publishing an artifact from an
  in-memory campaign.

---

# Family B — From-scratch construction and baselines

How a new circuit gets a first legal answer, and how you price "what does no
project knowledge buy?"

### B1 · anneal3 (depth-3 partition annealer)
- **Family:** from-scratch construction, depth-first.
- **What it does:** Models each of the 32 outputs as `A ⊕ B` where A and B
  partition its target bits into depth-≤2 parts; auxiliary signals are
  refcount-costed so a shared part is paid once. Simulated annealing over the
  per-output split choices, then greedy descent and iterated local search with
  random kicks. Depth ≤ 3 holds by construction.
- **Twist:** the only from-scratch constructor that is *depth-first* rather than
  gate-count-first.
- **Measured:** **97 @ depth 3 from scratch**, beating the published 99 @ 3
  (Shi–Feng–Xu ToSC 2023). Re-validated 2026-07-27: cost 97 on its first RNG seed
  after **81.1 s** on one core (23.5 s annealing, then ILS); 60–156 s across
  earlier runs. Never below 97 in 16 seeds nor in 21 core-hours; CP-SAT on the
  exact ILP reaches only 101 with the dual bound frozen at 32. Independently
  re-derived gate-for-gate by the demand-flow work. In `beat88`'s depth-capped
  lane it was run as **pure ILS with no SA phase at all** and became half of the
  91@4 recipe (see C24).
- **Cost:** ~81 s, one core; roots ~25–37 s each in pure Python.
- **Code:** `pipeline/engines.py:engine_anneal3`; frozen v1 in
  `reproduce/reproduce.py`; `beat88/methods/m3_census/code/anneal3.py`.
- **Logs:** `evidence/parallel_ladder_run_2026-07-13/d3.log`, `reproduce/out_97.json`.
- **Generality:** **MIXED.** The A⊕B partition model is generic for any GF(2)
  linear map; targets come from `mixcolumns_core.py`. `beat88`'s copy is
  **MC-HARDCODED and depth-3-only** (its emitter cannot express depth ≥ 4; target
  weights 5/7 baked in).
- **Incarnations:** `root_infra:anneal3-depth3-annealer` → `beat88:2B anneal3` →
  `beat88:m3-depth-capped-lane` (as pure ILS).
- **Phase-2:** **keeper.** Cheapest known way to get a good shallow root for a new
  target, and the root of the project's entire own-lineage chain.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** The Generality line contrasts the root copy (MIXED) with beat88's (MC-HARDCODED) as if they differed. They are the same code — `05-depth-capped-lane.md:49-50` records anneal3.py copied *verbatim* — and the root carries the identical weight-5/7 branch (`pipeline/engines.py:975`) and `range(32)`. Treat both as MIXED with the 5/7 split enumeration as the porting hazard.

### B2 · naive-random-xor-tree root (seedless root generator)
- **Family:** from-scratch construction / provenance.
- **What it does:** `constructors.build("naive", <int>)` generates randomized
  balanced XOR trees over the 32 raw inputs with opportunistic reuse, producing a
  valid but large depth-3 circuit (139 and 146 gates for the two recorded seeds)
  as a pure function of one integer.
- **Twist:** unlike anneal3 it makes no attempt at quality — its entire value is
  *provenance*: the root reads nothing from disk, so everything descended from it
  is certifiably free of imported material.
- **Measured:** roots of **both** from-scratch 88s. `naive#2163` → 139 @ d3 → 88 @
  d6 (restart 18, 18.96 h in). `naive#1958` → 146 @ d3 → 93 → 91 → 90 → 89 → **88
  @ d6 at t = 69 192.7 s** → **88 @ d5** (session 5, restart 16, 19.22 h in). Both
  reproduce their logged roots exactly from the integer. Yield per lane across
  constructors: naive **8.6 CPU-h/88**, anneal3 10.2, paar 20.5, bp 39.9. The root
  shares 8/56 periphery masks with its own 88 — **the same as an unrelated root**,
  i.e. roots are RNG seeds, not structural donors.
- **Code:** `evidence/campaign87_run_2026-07-28_got_88at6_fromscratch/code/`;
  `beat88/methods/m3_census/code/roots.py`.
- **Generality:** **CIRCUIT-GENERIC** apart from the input count.
- **Phase-2:** **keeper** — how a new target gets a clean-provenance start in one line.

### B3 · anti-vocabulary root construction
- **Family:** root supply / diversity.
- **What it does:** Constructs starting circuits deliberately biased *away* from
  the project's own harvested mask vocabulary (`avpaar`, `avsplit`, `avtree`,
  `randset`), on the principle that "a step that saves 6 gates loses to a step
  that saves 4 with a mask the project has never built".
- **Measured:** the from-scratch constructors are the **only** lanes producing
  genuinely off-family material (`c_anneal3` max-wJ 0.063, `c_bp` 0.078, `c_paar`
  0.091, vs `o_polish` 0.830 and `free_own` 0.697); their vocabulary bias is
  *negative* (−0.55, −0.73) while every other lane is +1.2 to +3.1 bits into the
  house dialect.
- **Code:** `campaign_87/novelty/roots/constructors_ext.py`, `MANIFEST.json`.
- **Generality:** CIRCUIT-GENERIC. **Phase-2:** keeper — the only measured
  antidote to the house-dialect effect.

### B4 · randomized Boyar–Peralta greedy (clean-room)
- **Family:** greedy construction / calibration baseline.
- **What it does:** Grows a set of XOR results from the 32 inputs. At each step it
  scores every possible new pair-XOR by how much it reduces the total remaining
  distance to the 32 targets, picks the best (random among ties), and repeats;
  restarts from scratch on a timer, keeping the best. Written in C from scratch
  with its own hash sets and bounded distance queries.
- **Twist:** **clean-room** — no project knowledge, no record data, no menus, no
  block decomposition — so its result is a *calibration point*, not a search
  result. Also carries a symmetric mode (add all four byte-rotations at once).
- **Measured:** best BP-only asymmetric **94**; typical per-worker best 95–101;
  **symmetric mode much worse — 106–108**, i.e. forcing ρ-symmetry costs ~12 gates.
  Naive baseline 124. **The whole clean-room effort's best is 93 — five gates above
  the record.** In the quotient tower (atlas), BP run with an **exact** subset-sum
  distance table (full BFS over the quotient space) gave `L2 ≤ 26` and `L3 ≤ 51`
  — 16 below the earlier 67. Separately, e12 measured BP-style greedy missing the
  optimum **6 of 7 times** on MC-density-matched instances (by 1–2 gates in 13–16).
- **Cost:** 14 logged BP workers, restarts of order 10²–10³ in 13–375 s each.
- **Code:** `fleet10/cleanroom/work/bp.c` … `bp5.c`; `atlas/tower/bp.c`, `bp2.c`.
- **Generality:** **MC-HARDCODED but trivially retargetable** — a single `TGT[32]`
  array at the top of each `.c` file is the only problem-specific content.
- **Incarnations:** `fleet9_12:cleanroom-randomized-boyar-peralta` ·
  `atlas_misc:quotient-tower` (BP with exact distance table) ·
  `experiments_late:legibility-profiling` (as `k_greedy` baseline).
- **Phase-2:** **keeper as a baseline generator**, dead as a route to a record.
  Its value is the number 93/94: it prices what "no project knowledge" is worth.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** Two Generality defects. (a) "restarts of order 10²–10³" — no log reaches 10³; observed winning restart indices are 1…352, and the "13–375 s" bracket has a floor of 0 s. (b) "a single `TGT[32]` array at the top of **each** `.c` file is the only problem-specific content" is false in both directions: `atlas/tower/bp.c` has **no** TGT at all (it reads the instance from stdin, so that file is fully CIRCUIT-GENERIC), while `fleet10/cleanroom/work/bp5.c:292` bakes ρ-symmetry (`rotl(u,8*r)`) beyond any target list.

### B5 · partition-assemble-and-dedup
- **Family:** constructive upper bound.
- **What it does:** Solves blocks of outputs independently, glues them into a full
  32-output circuit, and lets coincident masks deduplicate at glue time.
- **Twist:** it is the correction that matters — **Σ block costs is not the
  realisable count.**
- **Measured:** Order-1: Σ=152 assembles to 146 as chains, **139** as balanced
  trees. Order-4 family-optimal: Σ=114 assembles to a verified **105 @ depth 5**.
  So "optimise each family exactly and glue" has a hard ceiling of 105 — seventeen
  gates above the record.
- **Code:** `experiments/e2_outputcost/code/construct.py`,
  `experiments/e8_quad/code/assemble.py`.
- **Generality:** **CIRCUIT-GENERIC.** **Phase-2:** keeper — always the right
  first upper bound for a new matrix.

### B6 · top-down algebra + peephole (laneFRESH)
- **Family:** from-scratch construction + local improvement.
- **What it does:** Derives MixColumns from the pair/triple plane algebra
  (`OUT_k = X(m_k) + T_k`, TAPS = {1,3,4}), builds several structurally unrelated
  from-scratch designs, then applies a strict peephole loop and a plateau walk.
- **Measured:** a **hard 108 attractor — four structurally unrelated designs land
  on exactly 108**. Only two one-off cancellations get below it by reason (worth 4
  gates: 108 → 106 → 104). Best by reason+peephole: **99 @ depth 5**; best at all:
  **95** by an illegible machine plateau walk. 15 oracle-verified artifacts 95–121.
- **Code:** `experiments/e13_hand87/laneFRESH/{d1_flat,hand,improve,walk,rebuild2,rebuild3,d3_loop,d5_wshape}.py`.
- **Generality:** MC-HARDCODED (plane/tap algebra); peephole/walk half is generic.
- **Phase-2:** superseded-by-M1 (cluster-currency hand reasoning) for reaching a
  record; keep as the calibration of what naive top-down algebra costs.

### B7 · algebraic-frame derivation (laneBASIS)
- **Family:** ladder/atlas-style algebraic construction.
- **What it does:** Derives MixColumns from a single-frame algebraic form
  (`M = 1 + Xz + z³`, unipotent) and from a fully-decomposed Jordan form, to
  measure what a purely algebraic derivation costs.
- **Measured:** `basis/zframe_105.json` — **VALID 105**, best single-frame
  algebraic derivation; `basis/jordan_140.json` — **VALID 140**, "priced honestly:
  conjugation moves cost". Also produced the Lipschitz lemma that made `D_fine`
  (J4) load-bearing.
- **Code:** `experiments/e14_plateau87/basis/{zframe,jordan,zcoords,flat108,ringcheck,tight,wide}.py`.
- **Generality:** CIRCUIT-GENERIC in method (any matrix with a polynomial form).
- **Phase-2:** **keeper as a baseline generator** for a new circuit — a legal
  starting circuit and an honest algebraic ceiling in minutes.

### B8 · backward-frontier search
- **Family:** randomized constructive search (backward from targets).
- **What it does:** Saturates backwards from the targets under a scored candidate
  order, with a *safe closure* engine (the previous engine "free-split through open
  children" stranded 2–4 nodes on a realizable 88).
- **Measured:** **the published 96 does not survive the fix.** Mandatory plumbing
  control fired first: planted 88 node sets on three basins come back oracle-VALID
  with **0 stranded**. 400 runs in the published regime: **best 104, median 112**.
  Control arm with the *old* policy on the *new* saturator: **106 — worse**. The
  two-step hop scorer `bwd9`: best 107 at n=64, **20–40× more expensive per run**,
  trips a cycle defect at ~3–6 %.
- **New instrument defect (reported, not fixed):** `risky_close_one` can reach a
  state whose χ relation contains a cycle — 0/400, 1/100, 2/64. Always caught by
  `dag_to_gates`, but it aborts sweeps.
- **Code:** `fleet1/laneD_completions/code/{bwd_frontier,run_bwd}.{py,sh}`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **dead-end at this budget** (frontier 104 vs record 88). Keep the
  fix and the plumbing control.

### B9 · backward-factorization search (+ the F identity)
- **Family:** search from targets toward inputs, with an exact accounting identity.
- **What it does:** Searches by repeatedly factoring an unresolved mask
  `m = a ⊕ b`; cost `F` = number of distinct internal factors. Proved equal to
  minimum gate count in both directions; a "free-split confluence lemma" means you
  never branch on a free split, so a run is a sequence of *introductions* and an 88
  is exactly 56 introductions.
- **Measured:** an exact identity **`F = 64 + a − c − 2d`** (a = pure-supply
  introductions, c = yield-3, d = yield-4), verified on all 32 circuits it touched,
  later 67/67. So **88 ⟺ `a − c − 2d = 24` and 87 ⟺ 23.** Mean closure yield is
  monotone across the frontier (1.571 for the 88s down to 1.485 for 98@3). Best
  cold circuit **96 VALID**; nothing below 89 in 1,281 runs. The engine ties records
  on supply (a = 32 vs 33–36) and loses **solely** on yield-3 (c = 0 vs 7–10).
- **⚠ Caveat:** `tri_search.md` later proved the saturator used for *all* these
  counts can strand nodes, so the 96 and everything in that section came from a
  partially broken instrument. Repaired in `atlas/tri/`; **never re-measured**.
- **Code:** `atlas/thinktank/backward/{bwd_core,bwd_equiv,bwd_audit,bwd_profile,bwd5..bwd9,bwd_beam,bwd_identity}.py`.
- **Generality:** **CIRCUIT-GENERIC** — the formulation, identity and yield
  statistics are stated for an arbitrary XOR target set.
- **Phase-2:** keeper (the identity especially); re-measure before quoting the 96.

### B10 · tri-search market (forward × backward × middle)
- **Family:** three coupled searches with an on-disk market.
- **What it does:** Runs forward, backward and a middle pool **simultaneously**,
  coupled through a shared market. Backward posts *constructive* bundle demands
  (the second partner of a yield-3 pair is forced: `u2 = d ⊕ u1`, so the demand
  list is complete with no search); the middle prices and builds; forward verifies.
- **Measured:** mechanism works as designed (`c: 0→6` cold, `0→9` planted; identity
  held 67/67) but **the economics are refuted**: measured exchange rate **5–8
  supply gates per yield-3 rebate against a break-even of 1**, so `F` *rises*
  across rounds (107 → 176). Diagnosis, the deepest result in the lane: **a yield-3
  move needs an open node of closed-rank exactly 3, and those occur 0–1 per step,
  matching pure chance (≈2.6e-4, ~0.4 expected per run)** — records do not *find*
  their yield-3 moves, they **manufacture** them. **99.1 % of yield-3 opportunities
  cost two masks** (34,067 of 34,368). The demand book **recalls 64–86 % of the
  records' own supply masks but ranks them ~200–800 of 25k**, with the economically
  *derived* criterion ranking them WORST of nine statistics (4.4 % vs shape-weight's
  0.8 %).
- **Code:** `atlas/tri/{tri_engine,tri_market,tri_loop,tri_control,tri_c3,tri_c4,sweep_base}.py`.
- **Generality:** **CIRCUIT-GENERIC.**
- **Phase-2:** keeper as a *negative result with a mechanism* — it tells the next
  phase not to try to buy coincidences. Its plumbing control caught a real bug in a
  sibling method (B9).

### B11 · NRPA (nested rollout policy adaptation)
- **Family:** constructive stochastic tree search.
- **What it does:** The only *constructive* paradigm in the campaign — builds
  circuits gate by gate under a learned 9-feature linear policy over candidate
  masks, rather than repairing complete circuits.
- **Measured:** 476,017 episodes at 37.1 rollouts/s, **best verified 88**,
  1,441,779 distinct ≤92-gate sets, 1,400,343 distinct 88s all at min depth 7.
  Crucially: with an unrestricted vocabulary (`free`/`open` modes) it only reached
  **101 and 99** — the learned policy needs the harvested V88 prior.
- **Cost:** 161,740 s = **44.9 core-hours** on one core.
- **Code:** `campaign_87/wave5_2026-08-04/nrpa/nrpa.py` (40K, single file).
  **Logs:** `campaign_87/wave5_2026-08-04/nrpa/out/sub92.jsonl` (1.45 GB / 1,441,779 lines).
- **Generality:** CIRCUIT-GENERIC in form, MC-HARDCODED in its prior.
- **Phase-2:** keeper for a new circuit — the only method that can start from
  nothing, but it must be given a vocabulary.

### B12 · evolve (LLM-authored operator population)
- **Family:** meta-search.
- **What it does:** A population of ~27 search-operator *programs*, each a Python
  file, evaluated by the mean endpoint of the descents it produces, with new
  individuals authored as mutations of the winners.
- **Measured:** 407 valid descents; endpoint distribution 88:9 89:74 90:183 91:115
  92:19 93:4 94:3; best individual `j_alg_99272` at **P(≤88) = 0.04**.
  Independently refuted the root-cancellation hypothesis at n=180.
- **Code:** `campaign_87/wave5_2026-08-04/evolve/evolve_loop.py`, `pop/*.py`.
- **Generality:** CIRCUIT-GENERIC. **Phase-2:** keeper — it was right about roots
  when a hand-run experiment was wrong.

### B13 · modular / glue-conditioned synthesis
- **Family:** constructive decomposition.
- **What it does:** Builds MixColumns as 7 small SLPs on 8–12 variables glued
  through single-residue masks, and generates the candidate mask population from
  the glue structure **without ever reading a circuit**.
- **Measured:** best from-scratch modular result is an **exact floor of 96** with a
  decoded RC2 witness; ladder: empty-glue 106 → locally-optimal modules 103 →
  greedy 103 → hill-climb 101 → block-coordinate descent 96 → exact floor 96.
  Boyar–Peralta is **exactly optimal given a glue** (gap 0 on 30/30); decomposition
  costs **0**; column generation is a **trap** (37 rounds never moved off 96); RC2
  cost is driven by alphabet *density*, not size, cap ~230 masks.
  **The result that matters:** the glue-conditioned population — 11,778 masks,
  generated without reading any circuit — **contains all 88 gate masks of three
  separate record 88s** and 87/88 of two more. Since a record's gate-mask set is a
  closed feasible set, `floor(population) ≤ 88` is a **theorem, not a hope**. The
  remaining gap localises entirely to selection under the solver's ~280-mask cap.
- **Code:** `campaign_87/wave6_2026-08-11/modular_syl/{galph,genall,flinc,asearch,p0exact,gfloor}.py`.
- **Generality:** MC-HARDCODED (the 7-pattern residue decomposition is from
  Sun–Yang–Li for this matrix).
- **Phase-2:** **keeper — the single most promising unfinished line** in the
  campaign_87 slice.

### B14 · L_cf reuse-greedy + CP-SAT upper bound
- **Family:** constructive search for the cancellation-free optimum.
- **What it does:** A randomised-restart reuse-greedy builds cancellation-free
  programs (each intermediate pool closure-checked), then CP-SAT is seeded with it.
- **Measured:** greedy 110 → CP-SAT **103**, closure-verified, no optimality in
  900 s; a second 1500 s warm start moved nothing.
- **`CONFLICT`:** the project already held an oracle-verified **102** on disk
  (`beat88/.../v2_no_vocab/data/cf_incumbent.json`), so this "first upper bound on
  L_cf" headline is both not-first and a regression. `STATE_OF_THE_PROBLEM.md`
  records this as discrepancies D1/D10/D11; it is **uncorrected** in
  `fleet6/laneTOOL2/RESULT.md`. See Appendix B #1.
- **Code:** `fleet6/laneTOOL2/` (`results/lcf_cpsat.json`).
- **Phase-2:** **superseded** by F27's CF incumbent (102, depth 5, zero cancelling
  gates), which with I12 gives `92 ≤ L_cf(M) ≤ 102` with both ends solid.

---
- **COMPLETED (2026-08-29):** this entry was one of the nine Appendix A skeletons. The full schema-conformant entry, written from primary sources by `wrapup/day2/CATALOG_AUDIT.md` §3, is **Appendix A §A·9**.
# Family C — Plateau / local search: engines and move classes

The workhorses. Read the C1/C2/C4 verdicts together: they are excellent far from
the frontier and provably inert at it.

### C1 · walk (value-set plateau walk)
- **Family:** plateau-search / neutral walking.
- **What it does:** Remove-1 and hub moves over the incremental closure of a value
  set, with exact complete repair enumeration; walks *sideways* across equal-size
  circuits rather than descending. The Pareto tie-break (accept equal gates at
  strictly lower depth) is what converts lateral motion into depth wins.
- **Twist:** it is the *plateau sprayer* — it does not try to improve, it tries to
  move.
- **Measured:** **480–640 it/s** on a loaded box (v1: ~70–110). Both campaign-era
  88s and both from-scratch 88s were surfaced by walk chunks; NEW-BEST attribution
  across the archive is **walk 736 vs LNS 22**. In the 88@7 run the walk found the
  88 masks at depth 11 and the tie-break carried the same mask set to depth 7 **5.3
  s later**. At the frontier its improvement probability is measured **zero**
  (0/324,815 free removals), and the walk is **provably monotone non-increasing**
  (`plateau_slack_p` is arithmetically inert).
- **Code:** `pipeline/engines.py:engine_walk`; `campaign_87/agents/merged-engine/work/engines.py`.
- **Logs:** `evidence/campaign87_run_2026-07-26_got_88at7/runs_hunt/w10_sym94.log`.
- **Generality:** MIXED (value-sets of 32-bit masks, fixed 32-target set).
- **Incarnations:** `root_infra:walk-valueset-plateau` · `campaign_87:merged-engine` ·
  `beat88:2B plateau-walk-neutral-swap`.
- **Phase-2:** **keeper — the only engine that has ever produced an 88.**
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** The headline `480–640 it/s` is repriced in a primary this catalog cites elsewhere and should carry a `CONFLICT` flag: `beat88/analysis/code/engine-walk.md:230-239` measures **451 / 660 / 546 it/s** sustained over 300 s across three RNG seeds, with first-minute decay 866 → 346, and notes "the band is narrower than the seed-to-seed spread, so it cannot have been measured with replication."

### C2 · LNS (destroy-and-rebuild large-neighbourhood search)
- **Family:** plateau-search / large neighbourhood.
- **What it does:** Repeatedly destroys a connected cone (or a large injected
  block) of the current value set and rebuilds it from a scored pool, accepting on
  a simulated-annealing schedule with reheat. Rebuilds are peeled before being
  judged; victims are re-pooled at a higher cost class so a rebuild can never
  dead-end; the depth cap is enforced by a level-BFS `relax`.
- **Twist vs v1:** five separately measured mechanisms — victim repooling (~34×
  accepted moves/s; feasible iterations 1.2 % → 100 %), scored hot pools (~11×
  accepted moves, 16–18× pool hit rate), peel-before-accept (2,630 near-miss
  rebuilds recovered in a 2-min probe), SA-with-reheat (~2× drift), and the
  `coneinj`/`biginj` destroy mix (uniform destroys measured dead: **0 accepts in
  5,633**).
- **Measured:** ~100–180 it/s on a loaded box (v1: 60–100). Re-found **89 @ depth 5
  at t = 0.3 s of its first chunk** (LNS iteration 18), twice, on a seed the v1
  engine needed 592 s for. All five 88s were found inside runs of this engine
  (though the 88s themselves came from *walk* chunks). At the frontier the
  measurement is brutal: **effective radius 0.24 masks**; 84–85 % of accepted moves
  are literal no-ops; 4 distinct 88-states in 300 s vs the walk's 10,124.
- **Code:** `pipeline/engines.py:engine_lns` (1,204 LOC file).
- **Generality:** MIXED, as C1.
- **Incarnations:** `root_infra:lns-destroy-rebuild` · `campaign_87:merged-engine` ·
  `beat88:2B lns-destroy-and-greedy-rebuild`.
- **Phase-2:** **keeper — the workhorse**, with measured-good knob defaults; but
  superseded/dead at the frontier.

### C3 · merged-engine wave-1 improvement bundle (seven measured A/Bs)
- **Family:** plateau-search engineering.
- **What it does:** Seven separately measured engine improvements, each with its
  own A/B, cross-checked for bit-identical trajectories or oracle-verified
  equivalence, then merged into one production engine.
- **Measured (each row from `campaign_87/agents/<name>/REPORT.md`):**

  | improvement | measured effect |
  |---|---|
  | **relax-kernel** (level-BFS depth relaxation, realizability-only closure) | **17.5× end-to-end LNS** (42.3 → 739 it/s); bit-identical 1,500-iteration trajectories |
  | **closure-kernel** (worklist/BFS closure, incremental `remove_query`, improve-only-on-change) | **21.9× walk** (12.3 → 269 it/s); root cause was an improve-spam bug costing 78 % of runtime |
  | **victim-repool** | **~34× accepted moves/s**; 100 % of iterations feasible (was 1.2 %) |
  | **coneinj destroy** | **~12× improvements/s**; the only operator making destroy size 3–4 productive |
  | **exact `_repair`** (complete enumeration of `{v^a : a ∈ closure(S2)}`, \|C\|≈7) | **~7× plateau mobility** (1.9 → 13.6–16.3 distinct states/s); complete enumeration is *cheaper* than 24–40 random tries |
  | **scored hot-multiset pool + peel cache** | **~11× accepted moves**, 16–18× pool hit rate |
  | **SA-with-reheat acceptance** | **~2× drift** (best of SA/RRT/LAHC/kicks; LAHC provably inert) |

  Net: walk went from ~70–110 to 480–640 it/s. C closure alone is **3.1 µs =
  65–110×**; `relax` decremental 2.62× end-to-end; **numpy and GPU are measured
  traps**.
- **Code:** `campaign_87/agents/{relax-kernel,closure-kernel,lns-extract,lns-destroy,repair-move,lns-pool,acceptance-schedule}/`;
  merged in `campaign_87/agents/merged-engine/work/engines.py`; C kernels became `beat88` B1.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper** — this table is the tuning guide for any new engine.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — Generality label wrong and internally inconsistent.** Labelled bare `CIRCUIT-GENERIC` with no port clause, but the merged artefact is MixColumns-bound at the top of the file: `campaign_87/agents/merged-engine/work/engines.py:28-31` (`import mixcolumns_core as core; T = core.TARGETS; TSET = core.TARGET_SET`), `work/mixcolumns_core.py:21,36,53-54` (`0x11B`, `coef=[2,3,1,1]`, asserts 20 weight-5 / 12 weight-7), and the engine leans on it at `:256`. **C1 and C2 label this same file MIXED.** Correct label **MIXED**, port cost = swap `mixcolumns_core` and de-hardcode the 32-bit width. The seven A/B rows are correct to the digit and the phase-2 verdict stands. Separately, the "Net" sentence mixes eras: the seven rows are campaign_87 wave-1, while `3.1 µs = 65–110×`, `2.62×` and the numpy/GPU verdict are beat88-era C-kernel results.

### C4 · hub move (remove-2-add-1)
- **Family:** plateau-search / local move class.
- **What it does:** Removes two masks from a value set and adds one, using the
  complete repair machinery to enumerate every legal single replacement. It is the
  one move class that can strictly reduce gate count by one in a single step.
- **Measured:** **DEAD at the frontier, exactly and repeatedly.** 0 successes in
  ~**2.24 M** repair samples across all seeds; then proven exactly — the
  remove-2-add-1 neighbourhood of *every one of the five 89 seeds* is empty (1,596
  windows each, exhaustive), and empty inside every certified k ≤ 3 shell.
  Independently re-confirmed by the demand-flow work (1,596 cases, 0 moves). But
  historically it cut **90 → 89 in 150 s**.
- **Code:** `pipeline/engines.py` (inside `engine_walk`); `reproduce/reproduce.py`
  method `"89"`; `campaign_87/agents/hub-moves/work/moves2.py`.
- **Generality:** **CIRCUIT-GENERIC.**
- **Incarnations:** `root_infra:hub-move-remove2add1` ·
  `campaign_87:hub-move exact enumeration`.
- **Phase-2:** **dead-end at the frontier, keeper as a first probe** on a new
  target where the frontier is far away.

### C5 · exact single-mask repair (complete enumeration)
- **Family:** local-search kernel.
- **What it does:** Given a mask removed from a circuit, enumerates *every* legal
  single-mask replacement rather than sampling candidates.
- **Twist:** completeness makes a "no repair exists" answer meaningful; and it is
  measurably *cheaper* than sampling.
- **Measured:** completeness re-verified **0 misses on 362 breaking removals**;
  ~7× plateau mobility. **Defect found:** the `valid[:4]` prescreen (sorting by
  `(hamming_wt, -reuse)` and keeping four) **deletes 30–37 % of true plateau
  edges**.
- **Code:** `pipeline/engines.py:_repair`; analysis in
  `beat88/analysis/code/repair-code.md`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper; delete the selection rule.**

### C6 · complete remove-1-add-2
- **Family:** exhaustive local neighbourhood.
- **What it does:** Remove one mask, allow two replacements — a strictly larger
  neighbourhood than the shipped move.
- **Measured:** 126 s/state → **3,070 distinct 89s + 79 88s, 63 of them
  unreachable by the shipped move.**
- **Code:** `beat88/analysis/code/repair-code.md` (implementation in `pipeline/`).
- **Generality:** CIRCUIT-GENERIC. **Phase-2:** keeper.

### C7 · BFS plateau enumeration
- **Family:** local-search / exact.
- **What it does:** Instead of walking randomly on the plateau, enumerate the
  plateau breadth-first.
- **Measured:** full neighbourhood of an 88 in **0.1 s**; **2,465 expanded / 6,324
  discovered in 300 s at 0 % revisit** vs the walk's 22–68 % revisit rate.
- **Phase-2:** **keeper — dominates the walk as an instrument.**

### C8 · syl-move (out-degree-1 subsequence replacement)
- **Family:** literature-derived move (Sun–Yang–Li).
- **What it does:** Finds a maximal chain of signals each used exactly once,
  deletes it, and exactly re-synthesizes it; generalized here to closed cones over
  out-degree ≤2/≤3.
- **Measured:** produced the **first-ever drift on Jean's 88 plateau** — 26 distinct
  verified 88-gate mask sets (symdiff 2–6 from Jean's), plus 183 distinct 89 sets.
  No improvement to any seed. Its predecessor filter (out-degree **1** windows) is
  **provably inert on an 88** — every component is a singleton on all six circuits
  tested; out-degree ≤2 is the version with structure at this size (see F7/E-band).
- **Code:** `campaign_87/agents/syl-move/work/syl_move.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** keeper — the only move that unfroze a plateau the standard move set
  could not touch.

### C9 · plateau drift with tabu + "away" bias
- **Family:** plateau-search, diffusion vs ballistics.
- **What it does:** Walks the equal-cost plateau with the shipped remove-1 +
  complete repair, adding a **tabu tenure** on just-removed masks and an **"away"
  bias** that picks, among all valid repairs, one not in the origin set.
- **Measured:** raises distinct plateau states visited from **64 to 726 (11×)** at
  matched compute — and moves the reach ceiling by **exactly zero masks**. Radius
  never exceeds **12** at the 88@5 across tabu 0/30/150 and a doubled step radius,
  over 1.04 M steps; **16** at the 88@6. `free_remove1` events: **0 in every arm**.
  The 12→16 difference is entirely the **basin**, not the operator.
- **Cost:** 1,500 s per arm × 6 arms.
- **Code:** `experiments/e3a_exploit/code/drift.py` (self-test 56/56 vs shipped `_repair`).
- **Phase-2:** **dead-end for finding gates, keeper as a diagnostic** — it measures
  the basin diameter, the number that closed the plateau-walking route.

### C10 · chained shake-and-recover displacement
- **Family:** large-neighbourhood operator.
- **What it does:** Buys radius in *cycles* — shake by a modest step, descend back
  to `n0`, repeat until achieved radius reaches the target. Every cycle ends at the
  anchor's own gate count, which is what "constant gate count" has to mean.
- **Twist:** it pins gate count **per state**, not per arm — the fix for a general
  reporting defect (reporting a displacement statistic and a quality statistic from
  two different states).
- **Measured:** radius at constant gate count costs **0.8 CPU-s per mask two gates
  above the frontier and 5.2–11.1 at it**, a 6–14× price rise, with reach capped at
  ~1/4 of what is requested. **Half of all shake-and-recover cycles at an 88 fail to
  restore 88 gates** (32/64 and 24/46). Because reach is bought *by descending*, it
  fails wherever descent fails.
- **Cost:** 3.13 core-hours over 122 trials, 11 calibrations, 14 interleaved controls.
- **Code:** `experiments/e9_radius/code/{chain,shake,trial}.py`.
- **Phase-2:** **keeper** — the only operator measured that moves a circuit a long
  way while pinning its gate count at every step, ~5 lines of glue over the rebuild.

### C11 · periscope plateau walk (non-monotone injection)
- **Family:** plateau-search.
- **What it does:** Enumerates the **complete** valid-repair set (the shipped
  engine truncated to 4), adds **tap-vocabulary injection** — with p ≈ 0.1 inject a
  protected extra gate from the excluded vocabulary, i.e. a deliberate
  89-excursion, so later repairs can reroute through it. Plus victim retry, tabu
  deques, and a descent alarm.
- **Twist:** the shipped walk was **provably monotone** — no uphill at all. This is
  the only walker in the project with a non-monotone move.
- **Measured:** planted positive passed — from a naive 116-gate seed, **31 cascaded
  descents to a VALID 90-gate circuit in 150 s**. Its night fleet reached best 90
  (186 emitted circuits, 2,741 harvest rows). **No sub-88.**
- **Code:** `atlas/periscope/{engine,shapes,census,pop_census,harvest_check,shell_probe}.py`.
- **Generality:** **CIRCUIT-GENERIC** engine; only `shapes.build_dictionary` is
  frame-specific.
- **Phase-2:** keeper.

### C12 · zero-cost re-association
- **Family:** circuit rewriting / normaliser.
- **What it does:** Expands a gate's cone to leaves and searches for a
  line-disciplined bracketing of the same value; if one exists using masks already
  present, the offending gate is removed at zero cost.
- **Measured:** removed the corpus's only value-glue gate and emitted
  `fleet5/laneGLUE/results/91at6_glue_free.json` — **91 gates, depth 7, VALID**,
  zero value-glue and zero joint-glue (re-verified in the slice pass). Applied to
  `88@6` gate 79 it *fails and says why*: every disciplined bracketing needs two
  intermediates the circuit does not contain.
- **Code:** `fleet5/laneGLUE/code/reassoc.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper.** Cheap normaliser; a *failure* to re-associate localises
  what a gate is really buying.

### C13 · SAT window repair (delete a cone, ask SAT to rebuild it smaller)
- **Family:** plateau-search / local improvement driven by SAT.
- **What it does:** Deletes a random dependency-closed set of *m* gates, freezes
  the rest as constants, and asks a SAT solver whether *m−1* (or *m−2*) fresh gates
  can restore all 32 outputs. On SAT it rebuilds, verifies and publishes; on UNSAT
  the window is proved un-improvable.
- **Measured:** **2,623 window attempts logged; exactly one improvement:
  `[hunt3] attempt 4: 94 → 93 gates`** — a hit rate of ~0.04 %. Every attempt at
  m ≥ 8 timed out at 230–285 s; all decided windows are m ≤ 7.
- **Cost:** ~70,335 s (19.5 h) of solver time.
- **Code:** `fleet10/cleanroom/work/satfix*.py`.
- **Generality:** **CIRCUIT-GENERIC** — reads targets from `spec/targets.json` and
  an arbitrary incumbent.
- **Phase-2:** **keeper for the descent from a bad circuit; dead near an optimum.**
  The measured curve — plentiful improvements from 124 down, exactly one at 94 — is
  itself the useful result.

### C14 · demand-flow search (F, B bi-mask routing)
- **Family:** representation change / search.
- **What it does:** Gives every signal a forward mask F (which inputs it XORs) and
  a **backward demand mask** B (which of the 32 outputs currently depend on it).
  The circuit becomes a sequence of rank-one factorizations `M = ⊕ B_v F_vᵀ`. A
  *routing* move rewrites B through an existing XOR triangle at **zero gate cost**;
  a *materialization* move buys `c = a⊕b` for one gate and simultaneously buys a
  new routing direction.
- **Twist:** it separates two things the value-set representation fuses. Two states
  with identical materialized masks can have different B and therefore different
  continuation costs.
- **Measured:** the controlled experiment is the result — **same first ten masks,
  different routing: completion cost 108 vs 100 gates**, and the better routing was
  *uglier* by the naive expression metric (L: 146 → 156). Descent 108 → 100 → 99 →
  98 @ depth 4; a saved artifact reached **the project's known 97 @ 3 gate-for-gate**
  from a weak greedy basin. Demand-intersection greedy alone stalls at 108; a
  one-step exact fiber oracle reaches only ~105. Diagnostics: average outputs served
  per gate rises monotonically with quality (97@3: 1.753 → 88@6: 2.773);
  "cancellation debt" `V − 184` rises too (97@3 max 18 → 88s 74–106). The
  independent `m5-routing-constructor` re-derivation reached **108 → 99 gates by
  rerouting alone**, oracle-VALID at depth 4, same masks, ≥5 gates apart — **the
  recursive descent past 99 was never run.**
- **Code:** described in `new-representation.md` §§1–14; implemented as
  `beat88/methods/m5_backbone/routing.py`, `verify/fiber10.py`.
- **Generality:** **CIRCUIT-GENERIC** — B is defined for any target matrix.
- **Incarnations:** `root_infra:demand-flow-search` (documented) ·
  `beat88:m5-routing-constructor` (implemented) · falsified at the frontier by C15.
- **Phase-2:** **keeper, and the strongest single idea in the documents** — the only
  method with a *positive* control that the ordinary representation provably fails.
  Unfinished: the routing axis past 99.

### C15 · demand-flow neutral-neighbourhood pricing (the frontier falsification of C14)
- **Family:** representational search, priced.
- **What it does:** At a verified circuit's prefix `n`, enumerates the **complete**
  structured free-routing neighbourhood (zero-gate moves that change routing `B`
  behind an identical mask set `A`) and rolls out every member.
- **Twist:** it *prices* the lever C14 called "the strongest proof-of-concept
  result" and never measured.
- **Measured:** the rollout is exact from prefix ≥46 (a sharp cliff at 45 — the
  first calibration in the project's history). At every calibrated prefix from 47 to
  86, across three 88 families and the 89: **0 improving, 0 even-neutral** among
  8–162 moves; best child uniformly parent+1. Two working controls: the estimator
  returns the parent's true gate count, and the same instrument *does* find 10 and 15
  improving moves on rows where the rollout is wrong. `dfattack` beam search over 240
  windows: `best_found` histogram **{88: 240}**.
- **Code:** `experiments/e3b_fresh/code/df/{dfcal,dffreedom,dfneutral,dfattack}.py`.
- **Phase-2:** **dead-end at the frontier, keeper as a cautionary result** — it
  explains seven earlier routing "search failures" with one mechanism and retired a
  recommended architecture before it was built.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — schema violation: this entry has no `Generality`, no `Cost` and no `Logs` field.** The measurements are exact. The correct label is **MIXED**: `experiments/e3b_fresh/code/df/dfcal.py:29` does `from bi_mask_probe import TARGETS`, and `bi_mask_probe.py:36-61` defines `xtime`/`gf_mul` and builds the AES targets; `:81,:90` and `demand_flow_search.py:39,137,202` hardcode 32-bit width. Port cost = replace `bi_mask_probe.target_masks()` and de-hardcode the width.

### C16 · ρ²-symmetric orbit search (symmetrize → orbit-peel → orbit-LNS → union-cross)
- **Family:** symmetry-reduced search.
- **What it does:** Byte rotation ρ (order 4) commutes with MixColumns, so it acts
  on value-sets. The half-rotation ρ² is used to search in orbit space, where a move
  adds or removes a whole orbit at once; existing circuits are symmetrized and
  peeled into the symmetric subspace; progress is made by **union crossings** of two
  symmetric circuits rather than by local moves.
- **Twist:** full ρ-symmetry costs about **+19 gates** (best fully symmetric ≈108),
  so the method uses only the *half* rotation, where the elite basin is already
  79–81 % symmetric. The 12 ρ²-fixed masks turn out to be the classic
  (x0^x2)/(x1^x3) sharing trick, rediscovered rather than imposed.
- **Measured:** ~90–120 walk it/s vs ~5 for naive orbit search (`campaign_87` reports
  ~100 it/s ≈ 20× naive). Two **exactly ρ²-symmetric 90-gate circuits** (depth 9 and
  depth 7, Jaccard 0.463 apart) — previous best exactly symmetric was 94; both
  machine-certified locally optimal in orbit space (every remove-1-orbit and all
  **666** remove-2-orbits-add-≤1 moves fail). As a *seeding device*: the ρ²-symmetric
  94 @ 5 is the seed the 88 @ 7 came from, and the ρ²-symmetric 90 @ 9 is the seed of
  the 88 @ 8. Stopped with formal cause: "structurally confined to a region no record
  circuit occupies" — the symmetric sector floors at 90, and **every known 88 has
  asymmetry defect u ∈ {17,…,40} while the engine's budget was u ≤ 3.**
- **Cost:** the 90 → 89 @ 5 descent from a symmetric basin took ~15 min.
- **Code:** `campaign_87/agents/orbit-ladder/work/engines_{closure,relax}.py`;
  `evidence/campaign87_certificates/rho2_symmetric_90s/make_union.py`.
- **Generality:** **MIXED — the *method* is CIRCUIT-GENERIC.** What a new target
  needs is its automorphism group. `aes_inv_mixcolumns` has the same Z/4 byte
  rotation, so this ports essentially unchanged.
- **Incarnations:** `root_infra:rho2-symmetric-orbit-search` ·
  `campaign_87:ρ²-equivariant orbit search` · `beat88:2B ρ²-orbit search`.
- **Phase-2:** **keeper as a seed generator, dead as a search space.** Two of the
  five 88s trace to it; it is the only method that made progress by *crossing*.

### C17 · parity-pinned orbit walk (sigma sector)
- **Family:** symmetry-sector search with an invariant pin.
- **What it does:** In the σ = ρ² symmetric sector a closed set costs `2a + b` with
  `b` = number of σ-fixed masks, so cost is odd iff `b` is odd. The walk
  **completely enumerates** the one-gate-buildable σ-fixed injection pool, injects
  each in turn to reach odd `b`, then rejects every move that flips `b mod 2`.
- **Twist:** the shipped orbit engine can change `b` but is never pinned, so it
  drifts back into the even half — which is exactly what its 166 cycles at
  `cur=90 best=90` look like.
- **Measured:** 2 seeds, 2 independently enumerated pools (130 and 78), 56
  injections, **every one settles at 91, none reaches 89**; 54,596+ moves rejected
  purely for parity. Pinned walk runs at **47 it/s vs 1.2 it/s** for a
  destroy/rebuild LNS in the same sector. Sector state: even half 90 (`b`=16), odd
  half **91** (`b`=15@d5 and `b`=13@d7). Re-pricing: below 91 the next odd value is
  **89**, so this is a **two-gate** move, not one.
- **Control correction worth carrying:** e3a called its odd-half negative controlled
  on a 94→93→92→91 descent — but those costs alternate parity, so that descent
  controls the *sector*, not the *half*. e7 built the matched control (93 → 91 with
  the pin on, two gates, same parity class) and it fired.
- **Code:** `experiments/e3a_exploit/code/orbit_odd.py`,
  `experiments/e7_push/code/{pinprobe,sigma_odd}.py`.
- **Generality:** MC-HARDCODED (needs a symmetry of the matrix).
- **Phase-2:** keeper as a **method template** (symmetry sector + parity invariant +
  pinned search); dead-end for 87 here.

### C18 · orbit-drop-and-readd (heuristic beam)
- **Family:** relaxation search.
- **What it does:** Drops a whole ρ-orbit (4 targets), re-optimises the 28-target
  relaxed instance with retargeted engines, then re-adds the orbit with a beam search.
- **Measured:** the relaxation does bite (weight-7 orbits give a 28-target set 1–2
  masks smaller than the 88's own), **but the re-add gives it all back and more.**
  Best total 89. Honest control failure recorded: for orbit 3 the relaxed set is
  byte-identical to the 88's own sub-circuit, so the true re-add cost is ≤10 and the
  beam returned 11 ⇒ the beam is **≥1 gate loose** and every "total" is inflated.
- **Reusable gotcha:** `mixcolumns_core.verify` hardcodes `outputs == 32`, so it can
  never pass a target-*subset* instance; anyone retargeting `pipeline/engines.py`
  will silently get "0 improvements".
- **Code:** `experiments/e3b_fresh/code/{orbitdrop,readd_beam,retarget,tdrop}.py`.
- **Phase-2:** superseded-by-G10 (`free-gate-reduction-exact-readd`).

### C19 · fixed-size infeasible search (FIXN)
- **Family:** relaxation search over infeasible states.
- **What it does:** Pins `|S| = N` exactly and lets the state be an **invalid**
  circuit for the whole run, minimising a graded potential `Φ = Σ_t c(t)` where
  `c(t)` is the *exact* minimum extra masks needed to build target `t` (exact for
  0,1,2; capped at 3). Metropolis acceptance, so coverage may decrease.
- **Twist:** the intersection of two prior dead ends — `walk87.py` never let coverage
  decrease; `m4_inverse` searched program space and failed its control. FIXN is
  mask-set space + fixed size + decreasing coverage + the r2 gradient.
- **Measured:** **control fires 203× at the record** — 768 materialisations, **767
  independently oracle-verified 88s** from infeasible fixed-size states at
  N=84/85/86. At N=87: 0 materialisations, best total 89, 18,683 iterations. A
  **controlled null**, not a vacuum. Radius by-product: minimum Jaccard to seed
  **0.130 at N=87** — 87 % of the mask set replaced at constant cost. But the hot
  setting reached Jaccard 0.13 with a Φ floor of 6, the cold setting held Φ at 2 but
  stayed above Jaccard 0.52: **far travel and low objective never co-occurred.**
- **Cost:** ~71,000 iterations over 9 runs.
- **Code:** `experiments/e3b_fresh/code/{fixn,common}.py`.
- **Generality:** **CIRCUIT-GENERIC** (the potential is defined from any target set).
- **Phase-2:** **keeper** — one of very few instruments whose control fires 200+
  times at the record.

### C20 · fixed-87 infeasible population search over program genomes
- **Family:** evolutionary / quality-diversity over derivations.
- **What it does:** Fixes the program length at exactly 87 gates — almost always
  infeasible — and scores by how many of the 32 targets it builds, over a batched
  numpy verifier at ~400 k circuits/s. The genome is the *derivation* (a gate list),
  a representation the value-set frame quotients away.
- **Measured:** **dropped on day 1 by its own pre-registered kill test, harder than
  written.** `32 − built` has no signal outside balls of radius ≈8–10 operand edits
  around circuits already owned: **99.91 % of random 87-gate genomes score 0;
  99.996 % of all local moves are neutral**; the *complete* one-edit shell of *every*
  one-gate truncation of all five known 88s and the 89 (529 base genomes,
  **6,832,408 genomes, exhaustive**) contains **zero** genomes at 32/32 with live
  ≤ 87, best score 31. **Control B fails**: at fixed length 89, seeded from 3-gate
  truncations of the 92@4, the search reaches only 30 of 32 (steepest ascent) / 29
  (QD, 203,770 evaluations) even though a valid 89 provably exists — so the 87
  hunt's failure (31/32 over 208,329 evaluations) **carries no information**.
- **Cost:** ~1 day, 2 local cores; the 87 hunt itself 420 s.
- **Code:** `beat88/methods/m4_inverse/{verifier,genome,search}.py`.
- **Generality:** CIRCUIT-GENERIC (the failure mode is about XOR having no metric).
- **Phase-2:** **dead-end**, cleanly and cheaply killed. Left three keepers: A7, A8,
  and one open door — use **`r2` (targets within one pair-sum), not `32 − built`**,
  the only relaxation measured with real gradient.

### C21 · latent-interface (gauge) climb
- **Family:** search in a transformed space.
- **What it does:** Writes a circuit as `B·A + D = M` and walks the *latent
  interface* rather than the circuit itself, splicing back and oracle-verifying.
- **Measured:** round trip exact (`B·A + D == M`, 40/40 per anchor). **Phase-1 power
  control passes**: 97→91, 92→90, 91→90, 90→89, all oracle-VALID. Attribution
  measured: random-gauge operators are a *handicap* (+1.4 … +2.3 gates paired); the
  chain operator is what descends. Phases 2–3 ran seven 88-anchors to ~13,000+
  interface iterations each — **all pinned at `best 88/88`**; because the walk runs
  *at* the anchor's own gate count, any single accepted improvement would have been
  an 87.
- **Code:** `campaign_87/wave6_2026-08-11/gauge/{climb,latent,analyze}.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** keeper — it passes its power control, which most instruments do not.

### C22 · Steinberg / transvection word search
- **Family:** group-theoretic search.
- **What it does:** Represents the circuit as a word in the Steinberg presentation
  of SL(32+r, 2) and rewrites it using the group relations, so the move set is
  defined by algebra rather than mask arithmetic.
- **Measured:** **killed by a cross-instrument control.** From the *identical*
  97-gate anchor the repo's own walk descends 97 → 92 in **83 s**, while the
  Steinberg search returns **+0** after 250k–400k iterations across three move
  classes and multiple seeds. Power floor confirmed (`mixed` recovers all 8 planted
  dead gates, 96 → 88). Theory: under the projection `w ↦ V(w)` the entire
  cost-neutral part of the move set collapses to a point.
- **Code:** `campaign_87/wave5_2026-08-04/steinberg/{steinberg,moves,hunt,xcontrol}.py`.
- **Phase-2:** **dead-end — and cleanly so. Do not re-propose it.**

### C23 · depth-capped worker / depth-capped restart hunt
- **Family:** plateau-search under a hard depth constraint.
- **What it does:** The same walk/LNS engines with a hard depth cap threaded into
  both the engine and the worker context, so the search only ever visits circuits
  realizable at depth ≤ D. The cap flows into the *depth fixpoint*, not just a
  post-filter, plus a root-feasibility guard. The e4 variant restarts repeatedly
  from a fixed anchor and re-derives and verifies its own anchor per restart.
- **Measured:** cap-4 workers hold 92@d4 and cap-5 holds 88@d5 while uncapped
  siblings on the same seed drift to depth 5–7. `campaign_87/agents/hunt-88at6` ran a cap=6
  fleet for 13,500 s × 6 workers and never reached 88 at depth ≤ 6 (≈22 core-hours).
  e4: **0 of 49 restarts** reached ≤ 90 gates at depth ≤ 4 in 4.9 core-hours;
  endpoints `{(91,4): 40, (92,4): 9}`. **Trap noted:** 0/9 restarts from the shipped
  92@4 reached 91, though the project inventory records that step as a four-minute
  result.
- **Code:** `campaign_87/tri_hunt/hunt_worker.py --cap`,
  `campaign_87/agents/hunt-88at6/work/cap_worker.py`, `experiments/e4_depth/code/hunt.py`.
- **Generality:** CIRCUIT-GENERIC engine, MC-HARDCODED driver.
- **Phase-2:** keeper for frontier/Pareto work; superseded by F17 for *deciding* a
  depth level; dead for the 87 hunt.

### C24 · depth-capped lane recipe (how 91 @ depth 4 was actually made)
- **Family:** composition — from-scratch constructive root + hard depth cap.
- **What it does:** Composes two things neither of which works alone: a
  partition/pairing annealer (B1, run as **pure ILS with no SA phase at all**) that
  builds a depth-3 root from the spec itself reading no file, then a `--cap 4` walk
  that refuses any state whose ASAP depth exceeds 4. Depth is a *constraint*, never
  a tie-break, and the lane is restart-heavy because depth-capped components are
  measured cages (**644 distinct states at cap 3**, then nothing).
- **Measured:** **91 gates at depth 4**, re-verified in the slice pass
  (`gates=91 depth=4 outputs_built=32/32 problems=0 / VALID`). 34 distinct verified
  91@4 circuits locally, 32 distinct gauge orbits; **pod2's manifest holds 15,650
  further 91@4 records**. Against the archived 92@4: plain J 0.346, periphery J
  0.144, row-depth Hamming 11 — a different circuit. Replayable bit-for-bit
  (`replay.py --spec 'anneal3' --root-seed 6130 --walk-seed 6137 --iters 363964`).
  **Neither half would have done it**: the annealer stops at 97–99, and a generic
  capped walk from a naive root stalls at 96 under cap 4 (and at **111** under cap 3).
- **Cost:** the 92→91 step took **four minutes of one core**.
- **Code:** `beat88/methods/m3_census/code/{descent.py (--cap/--claim-max),anneal3.py,roots.py,replay.py}`.
- **Logs:** `exports/RECORD_mixcolumns_91gates_depth4.json`, `exports/FRONTIER.json`.
- **Generality:** MIXED — cap machinery generic; anneal3 MC-HARDCODED, depth-3-only.
- **Phase-2:** **keeper — the highest measured return-per-core in the whole tree**,
  and the one that produced a publishable record. Pareto frontier left behind:
  `{3:97, 4:91, 5:88, 6:88, …, 16:88}`.

### C25 · composition, splice and union crossing
- **Family:** recombination search.
- **What it does:** Splices cluster blocks or per-output cones between known 88s,
  or takes the union of two circuits' mask sets and re-minimises, and minimises the
  resulting gate count.
- **Measured:** N1 (two-frame cluster splice, 20×19×254 = **96,520** subsets) —
  **min 88, EXHAUSTIVE at cluster granularity**. N2 (`20^8` = 25.6 billion free
  per-cluster mixes, 18.9 M nodes, 81 s) — **min 88, exhaustive on that space**. N2′
  (per-output splice over `20^32`, hill-climb from 80 starts) — min 88, local. N1's
  optimal splice **rebuilt d7 exactly** (record and d7 share their C567 block) — an
  identity check, not a new circuit. Plain union crossing: **13 of 15 pairwise
  crossings beat the symmetrize-first path by ~4.6 gates**; two land at 89/90 from
  cold — but M1's cartography later measured the class as gauge-confined and
  anti-correlated with parent distance (0 escapes in 3,293 products).
- **Code:** `experiments/e15_campaign3/compose/{splice,build_splice,outmix,outclimb,absorb,cover,mixmin}.py`;
  `evidence/campaign87_certificates/rho2_symmetric_90s/make_union.py`.
- **Generality:** CIRCUIT-GENERIC given a corpus of circuits to splice.
- **Phase-2:** **dead-end for gate count** (the "wash identity": `88 = 32 + 56` is
  forced, every mechanism moves a gate between the currency and helper piles, *"a
  composition of wash-mechanisms is a wash"*); **keeper as a diversity generator.**

### C26 · local-surgery pricing (laneBEND)
- **Family:** priced local moves.
- **What it does:** Attempts count-preserving or count-reducing surgeries on known
  88s — output chaining add/remove, one-rotation collisions, mint-and-chain detours
  through 89 — and prices each in gates.
- **Measured:** output chaining is **+1 in both directions** (209 add constructions,
  12 removals, all landing at 89); **74 rotations across five knowns + stage5, 0
  collisions**; mint-and-chain detours through 89 re-entered the known components
  6/6. Rigidity: alternative wirings at fixed masks number **0/0/0/0/2** across the
  five knowns — four of five are perfectly rigid.
- **Code:** `experiments/e14_plateau87/{reparent2,rigid,seams,blocks,orbit}.py`.
- **Phase-2:** **superseded-by-C27 / E15-lane536**, which run the same species of
  move exhaustively over the whole corpus.

### C27 · excursion probes PC001–PC005 (corpus-wide single-move surgery)
- **Family:** single-move surgery at corpus scale.
- **What it does:** Five probes, each a single count-preserving-or-reducing move
  with a fail-able control: PC001 re-parent an orphan; PC002 rotation collisions;
  PC003 marginal-object excursion; PC004 the 1-mint/2-orphan funnel on 13 anchors;
  PC005 the same funnel on the **full corpus**.
- **Measured:** PC001 **0 orphanable / 728 gates** (control 56/56); PC002 **0
  collisions in 172 legal rotations** (calibration 6/6, planted 12/12); PC003
  negative by derivation with the closure enumerated; PC004 587 → 37 → **0**;
  **PC005: 800,994 two-consumer gates → 55,970 candidate sites → 536 non-trivial →
  0.** PC001/PC002 were the first time the F-points were probed — **scope: POINTS,
  not ORBITS** (closed later by e16's J3). The "536" was subsequently **dissolved**
  by L24 (it is 268 sites doubled).
- **Code:** `experiments/e15_campaign3/compose/{orphan_fpoints,rot_fpoints,rot_control,orphan_control,funnel,scan_1m2o,scan2_1m2o,corpus_scan,plant_1m2o,verify_hit}.py`.
- **Generality:** CIRCUIT-GENERIC given a corpus.
- **Phase-2:** **keeper** — PC005 is the template for a cheap corpus-wide one-move
  negative on any new circuit.

---

# Family D — Orchestration, fleets, diversity and ops

### D1 · cascade depth ladder
- **Family:** search orchestration.
- **What it does:** Rung d3 starts from nothing with B1; each time the frontier rung
  beats its baseline (or times out) the next deeper rung launches seeded from it;
  all rungs keep running and reseed one another. Depth is the *schedule variable*,
  not a constraint — the ladder buys depth slack to find gate count, then lets the
  Pareto tie-break pull the result back down.
- **Measured:** produced **92 @ depth 4 from scratch** at t = 9,610 s (2.67 h). Full
  cascade timeline: d3 97 → d4 96 → d5 95 → d6 94 → d7 93 → d8 92 → … The v1 version
  (21 h) gave the per-rung table 97/94/92/91/89/90/90/89/90/90.
- **Code:** `pipeline/ladder_parallel.py --mode cascade` (459 LOC).
- **Logs:** `evidence/cascade_run_2026-07-14_from_scratch_newlogic/coordinator.log`,
  `evidence/parallel_ladder_run_2026-07-13/HARVEST.md`.
- **Generality:** **CIRCUIT-GENERIC** orchestration over a MIXED engine set.
- **Phase-2:** **keeper — the canonical "point it at a new circuit and walk away"
  recipe**, and the only one with a from-scratch Pareto frontier to show.

### D2 · Pareto tie-break + continuous reseeding
- **Family:** acceptance rule (a coordinator twist, separately load-bearing).
- **What it does:** The improve rule accepts fewer gates **or** equal gates at
  strictly lower depth, and the engines were changed to *surface* equal-size
  shallower candidates instead of dropping them; the coordinator continuously offers
  every worker the best circuit feasible at that worker's depth cap.
- **Twist:** the v1 rule accepted strictly-fewer-gates only. That rule provably
  could not have produced any depth record — it would have discarded an 89 @ depth 5
  while holding an 89 @ depth 6, which is exactly what the archive shows.
- **Measured:** the 92 @ 4 exists *only* because of it (found by the depth-8 rung
  searching with slack). The 88 @ 7 reached depth 7 from depth 11 in **5.3 s**
  through it. `reproduce/README.md` documents that stopping on gate count alone
  yields 88 @ depth 8–11 instead.
- **Cost:** free.
- **Code:** `pipeline/ladder_parallel.py`, `pipeline/worker.py`.
- **Generality:** **CIRCUIT-GENERIC.**
- **Phase-2:** **keeper, non-negotiable.** The single cheapest mechanism in the repo
  per record produced.

### D3 · alt worker mode (walk/LNS alternation)
- **Family:** worker schedule.
- **What it does:** Alternates a 300 s `walk` chunk with a 600 s `lns` chunk from
  the worker's own best — the walk sprays across the plateau, the LNS punches down
  from wherever it landed. Not an engine; a schedule. It exists because walk and lns
  fail differently (walk cannot descend, lns cannot diversify).
- **Measured:** the mode of the record worker `w10_sym94` that found **88 @ depth 7**
  at t = 1,973 s, and of `c_naive` that found **88 @ d6 and 88 @ d5 from scratch**.
  Single-worker re-run 2026-07-27 reached 88 @ depth ≤ 7 in **19.4 min**, with the
  first chunk reproducing the archived worker's iteration numbers to the digit
  (92 @ it=27, 91 @ it=32, 90 @ it=603/622/670/723, 89 @ it=58 504, 89 @ 7 @ it=58 795).
- **Code:** `pipeline/worker.py`; aimed by `reproduce/hunt_88.py` (198 LOC).
- **Generality:** **CIRCUIT-GENERIC.**
- **Phase-2:** **keeper — the highest hit-rate configuration in the repo.**
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** "the record worker `w10_sym94` … found 88 @ depth 7 at t = 1,973 s" conflates two events. The log gives 88 @ depth **11** at 1973.3 s and 88 @ depth **7** at 1978.6 s — the same 5.3 s gap that C1 and D2 both state explicitly.

### D4 · hunt fleet supervisor
- **Family:** fleet infrastructure.
- **What it does:** One supervisor launches 6–16 heterogeneous workers, each on its
  own seed circuit and knob profile, restarts them with a rotated RNG seed when they
  die, regenerates a `STATUS.md` every 10 minutes, and shuts the fleet down when a
  `STOP` file appears. Every worker appends the distinct equal-best mask sets it
  visits to its own `.pop.jsonl`.
- **Twist:** PID-file process control that verifies `/proc/<pid>/cmdline` mentions
  the directory before signalling — **`pkill` is banned by name** in the README
  because it destroyed sibling work twice on this box.
- **Measured:** `hunt87` — 19.74 h, 16 workers, best 88@5, **148,347 new distinct
  88 states**, 198/198 MAP-Elites cells occupied, no 87. `tri_hunt` — 5.27 h, 10
  workers, best 88@5, 15,897 new 88 states, no 87.
- **Cost:** ~14 of 20 cores.
- **Code:** `campaign_87/{hunt87,tri_hunt,cascade6}/supervisor.py`.
- **Generality:** CIRCUIT-GENERIC. **Phase-2:** keeper — the harness every later
  fleet inherits.

### D5 · fleet restart loop
- **Family:** orchestration.
- **What it does:** Restarts a worker from a fresh root rather than continuing a
  long walk.
- **Measured:** 169 restarts, **14 reached 88 (8.3 %), 14/14 opened a never-seen
  pocket, zero repeats**, yield curve flat.
- **Phase-2:** **keeper — the only demonstrated novelty mechanism** in the old codebase.

### D6 · chunked reseed-from-best
- **Family:** orchestration.
- **What it does:** Periodically resets the worker's state to its own best rather
  than continuing, and (in the coordinator variant) offers the global best.
- **Measured:** chunk reset wins on every axis (**23.3 % vs 5.6 %** of ≥10-mask
  changes); coordinator reseed **offers: 17 in the entire archive**.
- **Phase-2:** keeper (the reset), superseded (the shared-memory half).

### D7 · plateau harvesting
- **Family:** data generation attached to a search.
- **What it does:** Appends every distinct equal-best mask set the search walks over
  to a `<label>.pop.jsonl` population file, instead of discarding siblings. It costs
  nothing and turns a search into a census.
- **Measured:** produced the **≈139,878 distinct known 88-gate states** (84,989
  families 1–2 + 53,902 family 3) that every certificate sweep and family census has
  been run over. Corpus at beat88 scale: 15,461,215 raw lines → **836,598 distinct
  88-gate states**, vocabulary 1,979 masks. Storage: **919 B/state vs 13–16 B as
  deltas (57–72×)**. All five 88s were found inside harvesting runs. But it is
  **provably causally inert** — the 10⁵–10⁶ verified plateau states per fleet went to
  files nothing read back during the search.
- **Cost:** disk — "a few MB per worker-minute"; it is the file that fills a disk.
- **Code:** `pipeline/engines.py:_Harvester`; knob `harvest` (on by default).
- **Generality:** **CIRCUIT-GENERIC.**
- **Incarnations:** `root_infra:plateau-harvesting` · `beat88:2B plateau-harvester`.
- **Phase-2:** **keeper, and arguably the most underrated method here** — on a new
  target, turn it on from day one; the population is worth more than the record.
  Store deltas, and read it back.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — the headline decomposition does not add up.** "≈139,878 distinct known 88-gate states (84,989 families 1–2 + 53,902 family 3)": both components verify individually, but **84,989 + 53,902 = 138,891**, off by 987. The 139,878 is a real but *different, earlier* measurement — `beat88/analysis/SYNTHESIS.md:154` files it as "three-old-anchor harvest, late July, **historical**" — and `SYNTHESIS.md:45-47` reprices it as counting orbit points of a handful of components **~100× over** ("volume was mistaken for exploration"). Neither is flagged `CONFLICT`. Quote **138,891** for the two-component sum, or cite 139,878 with its own provenance. Everything else in this entry is sound; `_Harvester` is genuinely CIRCUIT-GENERIC (read end to end; its only filter is `wt(m) > 1`).

### D8 · cross-pollination (sibling harvest merge)
- **Family:** population sharing.
- **What it does:** Every LNS worker periodically globs its siblings' harvests and
  merges their masks into its own rebuild candidate pool.
- **Twist:** it is **provenance-contaminating** — `hunt87` deliberately ran it OFF
  because two anchors descend from a published circuit; `tri_hunt` ran it ON.
- **Measured:** 3,651 merges pulling 1,072,997 masks; raising the shallow lanes'
  harvest cap took merge traffic from 280 masks/10 min to 927 per event across 14
  sources. **In both record events the LNS chunks never improved the best** — every
  improvement came from walk chunks — so cross-pollination's measured contribution
  to a record is **zero**. A self-test later found `campaign_87/hunt87/hunt_worker.py` never
  called `wire_harvest`, so cross-pollination was **silently dead** there and nothing
  in the logs said so.
- **Phase-2:** **superseded** — high provenance cost, no measured record contribution.

### D9 · MAP-Elites structural novelty archive
- **Family:** diversity.
- **What it does:** A 2,500-cell archive indexed by (3 family-distance axes ×
  ρ²-symmetry × gate band) computed on the *periphery* (non-target, non-input masks).
  An empty cell will buy a circuit up to **+6 gates worse** than the archive best —
  and the +6 is not arbitrary: it is exactly what the ρ²-symmetric 94 cost over the
  88 it eventually produced.
- **Measured:** 198/198 cells occupied, 4,375 expansions, 387 improved in place,
  best elite 88. In the wider audit: 24,473 submissions → 585 accepted, 198/2500
  cells, **0 new families** — structurally blind, because barren and productive
  basins share far bins.
- **Code:** `campaign_87/hunt87/{archive,explorer}.py`.
- **Phase-2:** keeper as the cheapest diversity mechanism; **dead-end as built**
  (distance-to-known coordinates); superseded by D12's intrinsic descriptors.

### D10 · basin-diversity harvesting (repel knob)
- **Family:** diversity.
- **What it does:** Adds a repulsion penalty against a reference mask set so the
  walk is pushed away from known basins, then harvests everything it visits.
- **Measured:** **356 distinct new 89 mask sets** (vs 4 previously known), min
  Jaccard to known 89s down to 0.107; recombination produced a verified hybrid 90@7
  in no known basin. Also: the **universal core of all ≤91 circuits is the 32 targets
  plus exactly one mask** (`0x40400000`).
- **Code:** `campaign_87/agents/basin-diversity/work/`; `repel_file`/`repel_pen` knobs.
- **Phase-2:** keeper.

### D11 · island portfolio with migration
- **Family:** search control.
- **What it does:** Runs several independent searches ("islands") in parallel, and
  every 12 minutes copies the best island's circuit over any island more than 5
  gates behind; a separate `collect.sh` verifies every candidate before crowning a
  global best.
- **Measured:** islands landed at 94/94/94/97; the migration logs are **0 bytes** —
  **no migration ever fired**, because the islands never diverged by more than 5
  gates. The method contributed nothing measurable.
- **Phase-2:** **dead-end as configured.** Keep the pattern, drop the threshold.

### D12 · mass basin census under intrinsic coordinates (the m3 fleet)
- **Family:** plateau-search at fleet scale, archived by intrinsic descriptors.
- **What it does:** Runs thousands of cheap descents from freshly constructed roots
  that read no existing circuit, and archives every state by an *intrinsic*
  descriptor (per-output ASAP depth profile, ρ²-defect band, gauge canon) rather
  than by distance to known circuits. The archive is the objective: descents whose
  descriptor is already known get killed at the ~100-gate waypoint.
- **Twist:** earlier archives measured "distance to known families", which is
  provably blind to productive-vs-barren *unknown*.
- **Measured:** **6,304 descents, 747 core-hours, 1,546,597 oracle-verified ≤88
  claims, 2,722 new families, 12,596 novel 88-orbits handed to the labeller, 5,268
  labelled exhaustively, 0 cuttable, 1 depth record (91@4), 0 eighty-sevens.**
  3,679 descents killed at the waypoint by triage; 15.2 M archive cells suppressed
  as gauge duplicates; 12.0 M equal-gate elite swaps; **2,274 firings of the k=5
  escape hatch, 0 hits**; 462 roots rejected as depth-illegal.
  Five things it proved: (1) reaching 88 is cheap and the supply of 88-families is
  large (2,722 in 747 core-hours vs the old campaign's 13 CPU-hours per family,
  marginal rate never saturating); (2) **the 88 plateau is rigid at the shape we can
  decide exhaustively** — 7,125 orbits across structurally independent generators,
  every one proved to admit no remove-2-add-1 net −1 cut; (3) the depth axis is
  softer than the gate axis; (4) **roots are RNG seeds, not structural donors** —
  all four arms statistically indistinguishable at the waypoint; (5) determinism is
  worth building for — iteration-denominated budgets made every descent bit-replayable
  and turned engine changes into same-trajectory A/Bs, which is how a pure-C kernel
  was caught landing **two gates worse at equal iterations while looking 5.5× faster
  on the clock**.
  Honest limits: the row-depth descriptor has **no resolution at the 100-gate
  waypoint**; triage is worth **1.31×, not an order of magnitude**; 4,732 orbits
  still unlabelled at close.
- **Cost:** 747 core-hours over ~70 lanes on three hosts.
- **Code:** `beat88/methods/m3_census/code/` (14 modules), `fleet.sh`, `run_*.sh`.
- **Generality:** MIXED. Engine, archive, descriptors, replay are circuit-generic;
  the target set and ρ² symmetry are MixColumns.
- **Phase-2:** **keeper as a corpus generator, dead-end as an 87 hunt.** Its own
  words: *"searching harder in the same shape has a well-measured expected value now,
  and it is zero."*

### D13 · fresh-fleet from-scratch descent (a power measurement, not a hunt)
- **Family:** plateau-search run as a statistical experiment.
- **What it does:** 8 lanes generating random roots and descending them to a local
  optimum, logging every endpoint, until a pre-registered sample size is reached.
- **Measured:** **1,500 from-scratch descents; endpoint law 88:52 89:375 90:575
  91:359 92:101 93:21 94:12 95:5; 0 reached ≤ 87.** P(87 per descent) < **2.00e-3**
  at 95 %; **P(87 | reached 88) < 0.056** at 95 %; a continuing-decay model needs 31
  88-arrivals and 52 were observed, so decay is **rejected at 99 %** — the operator
  class has a wall at 88.
- **Cost:** 4 days, most of the box; 5.06 GB of harvest.
- **Code:** `campaign_87/wave5_2026-08-04/fresh_fleet/{supervisor,engines,e1_analysis}.py`.
- **Generality:** CIRCUIT-GENERIC — **the single most reusable experimental design**
  in the campaign_87 slice.
- **Phase-2:** keeper (as methodology). It is what let the campaign price its own
  search class instead of guessing.

### D14 · region-partitioned concurrent search
- **Family:** parallel coordination.
- **What it does:** Partitions **one** circuit's mask space into disjoint linear
  subspaces (ρ-orbit plane sets), gives each worker a region, and serialises their
  edits through a revalidating coordinator barrier. The region is a **mask-space
  predicate**, not a lookup table — required, because the repair step invents masks
  no table owns.
- **Measured:** **worse than one instance**, at every plateau anchor, by 1.4–2.6× in
  distinct states per core-second (`p_mw ≈ 0.002–0.005`). `par-indep` (N instances,
  no regions) matches solo within 2 %, so the loss is caused by the regions, not by
  concurrency. It buys one thing: write-conflict rate falls 76–78 % → 31–35 %.
- **Cost:** 23,325 worker core-seconds, 180 runs.
- **Code:** `experiments/e1_regions/code/{e1,regions,run_e1,test_barrier,test_live}.py`.
- **Phase-2:** **dead-end as stated**, but the *diagnosis* is a keeper (see J42
  `exact-move-census`). Its own recommendation — **partition by MOVE, not by area** —
  was never tested.

### D15 · talk-channel ablation (M1/M2/M3)
- **Family:** parallel coordination protocol.
- **What it does:** Three independently switchable inter-worker messages — PROTECT
  (publish what my construction hangs off), DEMAND (ask a neighbour to build a mask
  I cannot, paying +1), TOKEN (mutex on boundary masks) — each ablated separately.
  DEMAND carries a gift-credit economy (grant, TTL, trim protection, revoke-by-restore).
- **Measured:** **M1 PROTECT is the only channel that pays** (+8 % distinct/core-s,
  commit rate 0.648 → 0.745, p=0.0022). M2 DEMAND **−26 %**; M3 TOKEN n.s. alone but
  it delayed a *provable* improvement 5–14× in the control. All three together
  **−53 %**: destructive interaction. The demand economy worked mechanically — 50
  demander-attributed gate reductions on the naive start — and delivered **zero** at
  all four frontier anchors.
- **Code:** `experiments/e1_regions/code/e1.py`.
- **Generality:** CIRCUIT-GENERIC (it is a protocol).
- **Phase-2:** keeper for M1 only; M2/M3 dead-end at frontier radius.

### D16 · ops harness (slot-guard / chain / identity-based process census)
- **Family:** operational discipline.
- **What it does:** A start-only, cap-respecting resume script that recomputes
  remaining work *from the ledgers on disk* rather than from the process table; a
  chain that launches the next stage when a slot frees; and a guard that ALARMs (but
  never acts) when startable work exists and a slot is idle. Process identity is
  established by `/proc/<pid>/cwd`, **never by pattern** — `pkill` is banned across
  every campaign.
- **Measured:** the guard correctly detected shard 0 down with its restart budget
  spent and **ALARM-ONLY'd rather than restarting**; it exited cleanly at
  `no startable work (runA 0 unswept, d3 0/13, d3 running=yes; partition OK 17283
  rows)`. Run A completion was verified **from the ledger, not the process table**.
- **Code:** `experiments/e15_campaign3/tools/{slot_guard.sh,resume_all.sh,procid.sh,launch_shard1_then_d3.sh,freshcheck.sh}`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper** — this is the harness that let a saturated 20-core box run
  a 3-day sweep alongside four untouchable solvers.

### D17 · CPU-second budgeting from /proc
- **Family:** measurement instrumentation.
- **What it does:** Drives the shipped worker unmodified but budgets in the worker's
  own `utime+stime` read from `/proc/<pid>/stat`, with a deliberately loose wall
  safety net.
- **Why it matters:** at `nice -n 10` on this box at load ~39, a worker got **3
  CPU-seconds in 238 wall-seconds — 1.4 % of one core**. The first calibration gave
  every worker a "480-second" budget worth ~7 CPU-seconds and everything timed out.
  **Wall clock is not a budget on this machine.**
- **Measured:** with it, the step-1 gate passed — 90@5 → 89@5 in a median **16.6
  CPU-s, 8/8 restarts**.
- **Code:** `experiments/e9_radius/code/{harness,calib}.py`.
- **Generality:** **CIRCUIT-GENERIC** (pure ops).
- **Phase-2:** **keeper, mandatory.** Every future experiment on this box should
  budget this way.

### D18 · env-gated, one-mutation-per-run experiment protocol
- **Family:** experiment control (meta-method used by five fleet12 lanes).
- **What it does:** Every axis is swapped by an **environment variable that is inert
  when unset** — with the variable unset the patched file behaves byte-identically to
  the shipped one, demonstrated before each lane's first solve. One mutation per run;
  a fresh solve-cache bank per experiment so a changed thing the cache key does not
  capture can never be served a stale answer.
- **Measured:** eight mechanisms catalogued (`SLP_SOLVE_CACHE`, `SLP_SUPPRESS_HINTS`,
  `LANE_HALO`, `LANE_ORDER`, `LANE_KNOBS_COMMIT`, `SLP_REGRESS_OUTDIR`,
  `SLP_REVERIFY_OUT`, `SLP_USE_POOL`), each with a documented inertness check. A hard
  **tractability guard** is enforced *inside the patch* (`plan._halo` refuses a fifth
  line: dim 16 is the solver ceiling) rather than in a shell script, so it cannot be
  forgotten.
- **Code:** catalogued in `fleet12/LIBRARY.md` §1; pristine originals in each lane's
  `pristine/`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper. Adopt as the default experiment protocol.**

---
# Family E — Exact local certificates (window and shell deciders)

These answer: *"remove k gates from this circuit — can fewer than k gates put it
back?"* A "no" here is a theorem about a ball of radius k. **Read E1's caveat and
L2 before quoting any of these as evidence about optimality.**

### E1 · exact window decider (budgets 1–2, k ≤ 3)
- **Family:** exact local certificate.
- **What it does:** "Remove a window of k masks from a verified circuit; can k−1 or
  fewer new masks restore all 32 targets?" Frontier-cascade closure with rollback,
  microsecond cost per test. A `None` answer is a *proof* for that window, backed by
  a first-unlock case analysis in the module docstring. Exact at k=2 and k=3; above
  that it does an honest partial DFS whose runs are recorded as `nosol`, never as
  irreducible.
- **Twist:** the completeness proof is what separates it from the SAT certificates —
  a "no" here is a theorem, a "no" there is evidence.
- **Measured:** **≈165 million exact window decisions campaign-wide, zero timeouts,
  zero reducible windows.** ~113,000 windows decided in the certificate archive.
  **All 1,540 k=2 and all 27,720 k=3 windows of the reference 88 exhaustive, all
  irreducible** ⇒ any 87 differs from it by ≥4 masks. The remove-2-add-1
  neighbourhood of all five 89 seeds is exactly empty. Validated 25/25 and 12/12
  against independent brute force; then branch-validated on **4,200 planted YES
  windows over 74 circuits, 4,200/4,200 correct**, cases 1b and 2a in isolation
  (462/462 and 33/33). Throughput 2.9–5.0 states/s on 4 procs (~6,900 windows/s);
  one k=2 shell ≈ 1.2 s, one k=3 shell ≈ 70–136 s.
  **`CONFLICT`:** `beat88/analysis/code/exact-window-code.md` records a defect —
  **414/450 false "irreducible" on *target* windows** — against the campaign's
  "no completeness bug, the ~165 M verdicts stand". The scopes differ (target-mask
  windows vs free-mask windows); see Appendix B #6.
- **Cost:** hours per circuit at k=3 (27,720 windows).
- **Code:** `evidence/campaign87_certificates/code/exact_window.py` (358 LOC,
  stdlib-only); `campaign_87/agents/exact-window/work/exact_window.py`;
  read-only copies in `fleet9/laneENUM/code/imported/`,
  `beat88/methods/m2_oracle/code/exact_window.py`.
- **Generality:** **MIXED.** The decider is generic over a target mask set; it
  imports `mixcolumns_core` and (inside `rebuild_circuit()` only) `engines`.
- **Incarnations:** `campaign_87:exact-window cascade` → `root_infra:exact-window-decider`
  (archived, shipped verbatim) → `beat88:m2-exact-window-decider-at-net-minus-2`
  (aimed at 89s/90s so a YES is the goal) → `fleet9` (imported as an equivariance test).
- **Phase-2:** **keeper — but read L2 first.** The same procedure finds zero
  reducible windows on a **97-gate circuit that is nine gates from optimal**, so an
  empty shell is not evidence of optimality.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** Two scope notes. (a) The `~165 M` total is faithfully copied but is now ruled a **stale under-count** by `wrapup/CONFLICTS_RESOLVED.md` Part D: the k=2 half alone re-tallies to **215,412,120** from three append-only ledgers. Quote the k=2 figure alone until residue R2 closes. (b) The `CONFLICT` note's claim that "no document reconciles them explicitly" is **false** — `beat88/analysis/code/exact-window-code.md` §4.5 reconciles them in the same paragraph, and the `C(56,k)` window-count identity is the control proving every archived sweep was target-free. **Live reuse hazard to carry forward:** the module has no `assert not (window & TSET)`, so any reuse over raw mask sets will get confidently wrong proofs; and `solve2`/`solve_deep` overload `None` for both "proved empty" and "deadline expired" using `time.time()` on a box whose clock steps backwards — any rerun must use `time.monotonic()`. Minor: "stdlib-only" is inaccurate (it imports `mixcolumns_core`).

### E2 · exact k=4 decider (budget 3)
- **Family:** exact local certificate (the k=4 sibling of E1).
- **What it does:** The same question at "remove 4, restore with ≤ 3", with its own
  completeness proof and a different case analysis.
- **Twist:** at k=4 the window count (**367,290 per circuit**) makes exhaustion
  infeasible, so it runs *prioritised* — every all-diff quad and every structural
  window first.
- **Measured:** validated on **1,257 instances against independent complete brute
  force, 100 % agreement including 122 genuine NOs**, identically under CPython 3.10
  and PyPy 3.11. On the reference 88: **32,685 / 367,290 windows (8.9 %)** decided
  exactly, all irreducible. On the family-3 anchor: 20,432 / 367,290 (5.6 %). On the
  project's independent 88 @ 7: **9 windows** — the least-certified circuit in the
  corpus. ~**16.8 M** exact decisions logged from this module; 53,126 budget-3
  decisions, 0 wins. **Removal monotonicity proved** (297 planted, 1,630 sub-windows,
  0 violations). Cost is **nearly flat in k** — 1.295 s at k=4 → 2.370 s at k=12.
- **Code:** `evidence/campaign87_certificates/code/exact_k4.py` (342 LOC);
  `campaign_87/agents/exact-k4/work/{exact_k4,exact_driver3}.py`.
- **Generality:** MIXED, as E1.
- **Phase-2:** **keeper — the most under-used instrument in the project** (its cost
  barely grows with k and nobody pushed it).

### E3 · complete small-core shells (the "88 wall" and "89 wall")
- **Family:** exact-window, completeness rather than coverage.
- **What it does:** Instead of sampling windows, enumerates the *complete* remove-k
  shell of a circuit at budget k−1 and decides every window. A completed zero-win
  shell is a theorem: no smaller circuit exists within that radius.
- **Measured (all with planted controls; every negative a theorem):**

  | theorem | scope | scale |
  |---|---|---|
  | **88 wall, core-2** — no 87 within remove-2-add-1 | 36,810 orbits incl. **all 33,010** of the complete known 88 population | 11,004+11,003+11,003 rows, **0 cuttable** |
  | **88 wall, core-3** — no 87 within remove-3-add-2 | six canonical families + 506 random + 1,137 descent-reached 88s | `runs/k3b2_*.jsonl` |
  | **89 wall, core-3** — no 87 within remove-3-add-1 | **64/64** known 89 anchors | 1,872,640 windows |
  | **89 wall, core-4** — no 87 within remove-4-add-2 | 13/64 anchors complete | 395,010 windows on the shipped 89 alone, 790/790 controls |

  Structural finding that outlives the arms: **tightness, not gate count, governs
  local reducibility** — every *tight* circuit from 89 to 97 has exactly zero core-3
  descents; the only circuits that descend carry dead gates. A 97 nine gates above
  the record is as locally rigid as an 89.
- **Cost:** a complete k=3/b=1 shell of an 89 = **6 seconds**. The complete `C(57,5)`
  shell of the record 89 is 4,187,106 windows and **reached 789,584 (19 %) before
  shutdown — still open.**
- **Code:** `beat88/methods/m2_oracle/code/{census_cut,gen_k3_shell,a1_shell_driver}.py`.
- **Generality:** MIXED — needs a new target set and an anchor corpus.
- **Phase-2:** **keeper, the strongest instrument in the beat88 slice.** It
  supersedes sampled window tiers, which spent ~230 core-hours to say less.

### E4 · population-scale shell sweeping (pop-decider / family3 / layer89)
- **Family:** E1/E2 deployed over a whole harvested population, not hand-picked
  circuits.
- **What it does:** Runs the exact deciders over the harvested population, ordered
  most-distant-from-the-reference-circuit first so the least-covered half is the
  swept half; fully resumable from an append-only progress JSONL.
- **Measured:** families 1–2: **51,899 / 84,989 states (61.1 %) fully swept at k=2,
  every one irreducible — 79,924,460 exact decisions**; the entire symdiff ≥ 55 band
  is closed; 33,090 states remain (~2.9 h uncontended). Family 3: **53,902 / 53,902
  (100 %), 83,009,080 exact decisions in 10,841 s — the family is CLOSED at k=2.**
  First k=3 theorems on 19 theorem-starved states: 526,680 exact decisions, all
  irreducible. Sanity gate: 12/12 sampled states rebuilt and passed the oracle at 88.
  The **layer-sweep** variant streams *every* population file, extracts every
  distinct 89-gate state into a packed binary layer, then runs complete k=2 shells on
  a provenance- and depth-stratified round-robin sample: **4,002,869 lines streamed →
  1,309,223 distinct 89-gate states; 9,693 complete shells.** Reductions occur in
  **exactly one source** (982/1,501 hits, ~67 %) and **0/7,568 everywhere else**;
  within that pocket 948 `win` (89→88), **0 `free` (89→87)** in 1,428 states.
  Round-robin over (source, min-depth) buckets was necessary: a naive
  most-distant-first sort put 60,000 states at the head that were all one basin.
- **Cost:** ~64.1 M + ~84.0 M decisions; the f3 k=2 pass alone 10,841 s.
- **Code:** the two deciders driven from `campaign_87/hunt87_layer89/{layerlib,harvest89,sweep_k2_layer,sweep_k3_layer}.py`.
- **Logs:** `evidence/campaign87_certificates/pop_decider/`, `family3_exact/`;
  **resumable frontiers all present on disk.**
- **Phase-2:** **keeper as an instrument, superseded as an argument** — L2 shows
  population coverage does not buy evidence about 87.

### E5 · family census + irreducibility certificates
- **Family:** structural clustering + exact certification.
- **What it does:** Clusters the whole 88-gate harvest under a calibrated weighted-
  Jaccard periphery metric, takes connected components as proven-distinct families,
  picks 3 representatives per family (most central + two most distant), and produces
  a machine-checkable JSON certificate for each representative's complete k=2 and k=3
  shell.
- **Measured:** **44,610 states clustered, 995,003,745 pairs scored, 10
  proven-distinct families** at the G32 threshold (13 groups at G46), max inter-family
  wJ 0.2827. Certificates: **76 × complete k=2 (1,540 windows) + 76 × complete k=3
  (27,720 windows) = 2,223,760 exhaustive decisions, every shell EMPTY**, plus 10
  partial k=4 at ~1 % coverage.
- **Cost:** k=3 certs ~564 s each ≈ 12 core-hours; the abandoned k=4 attempts cost
  ~15 core-hours for ~1 % coverage.
- **Code:** `campaign_87/families16/{reps,harvest,assign}.py`.
  **Logs:** `families16/certs/` (172 files, 700K).
- **Phase-2:** keeper — certificates are self-describing and re-checkable.

### E6 · cuttability census (exact labels + pre-registered signature analysis)
- **Family:** structural analysis over exact labels.
- **What it does:** Labels each gauge-orbit of a circuit population with a single
  exhaustive bit — "does its complete remove-2-add-1 shell contain a descent?" — then
  runs a *pre-registered* statistical analysis for which structural features predict
  that bit.
- **Twist:** the analysis plan was written and committed **before any label was
  computed**, and every negative carries a planted-positive control at the same
  budget; a control miss aborts the run.
- **Measured:** **85,446 gauge-orbits labelled, 1,076 cuttable.** Signature surviving
  Bonferroni + ≥2-strata replication: **neutral repair richness** — `deg_max` (AUC
  0.913, median 8 cuttable vs 5 rigid), `deg_mean`, `sh_out_neutral`,
  `sh_out_repairs` — all four measuring one quantity. Explicitly rejected as
  source-confounded / non-replicating: `sh_fixed_masks` (AUC 0.935 but fails
  cross-stratum), depth, ρ²-fraction. Excluded as label-leaky: `sh_out_improving`,
  `sh_out_total`. Corpus lesson: **line counts are not corpus size** — a "107k
  89-cluster" is 42 gauge orbits, and one file's 19.7 % cuttability is an artifact of
  its ordering (first 60k records; 0.03 % thereafter).
- **Cost:** ~5,800 orbits/hour on a 6-way local pool.
- **Code:** `beat88/methods/m2_oracle/code/census_*.py`, `cuttable_breakdown.py`.
- **Generality:** CIRCUIT-GENERIC given a decider and a gauge canonicaliser.
- **Phase-2:** **keeper.** It is the campaign's alarm system (a cut on an 88 *is* an
  87) and its retention-bias oracle for any future fleet. See L23 — its four named
  descriptors half-die under a lineage control.

### E7 · window-cut compressibility, split on `d(S)` (laneCUT)
- **Family:** local-surgery exhaustive search.
- **What it does:** For a window `S` of gates, splits the compressibility question on
  `d(S)` = number of internal gates, because budget − interface = `d(S) − 1` is
  exactly the number of free intermediate masks a replacement may use. `d(S)=1` can
  be searched to exhaustion by BFS over windows; `d(S)≥2` adds one free helper;
  `d(S)≥3` adds triples.
- **Twist:** the `d(S)` decomposition turns "look for a smaller re-implementation of a
  sub-circuit" from a heuristic into a complete search with a stated budget.
- **Measured:** `d(S)=1` BFS **closed on its own** (ran out of windows, not budget) on
  88@5 (6,848 windows), 88@5fs (18,564), 88@6 (26,498), 88@7 (386,922) — **0
  compressible everywhere.** Two errata recorded in place by the e15 re-run: the
  published 14,564 was a transcription error for 18,564; the published 387,395 **does
  not reproduce** (386,922). The 88@8 row never finished here (e15 later closed it at
  2,220,037 windows).
- **Code:** `experiments/e13_hand87/laneCUT/{adopt,slack,triple,cut,cut2,anatomy}.py`;
  controls `mkcontrol.py`, `mkcontrol2.py`.
- **Generality:** MIXED — window/`d(S)` machinery generic; oracle and targets MC.
- **Phase-2:** **keeper — this is the workhorse.** Direct ancestor of E8.

### E8 · population window sweep (tiers B / FH / D3)
- **Family:** E7 at population scale.
- **What it does:** Runs the `d(S)` compressibility search over the whole on-disk 88
  population instead of a handful of reference circuits. Tier B = `d(S)=1` window BFS
  + `d(S)≥2`; tier FH = the free-helper `d(S)≥2` regime only; tier D3 = triple-seeded
  `d(S)≥3`. One compressible window anywhere is an 87 on the spot. Every row carries
  its own truncation boundary as a field (`{why, maxwin, at_base, bases_done,
  bases_total}`) so a capped row can never be read as a closed one.
- **Measured:**
  * **13-anchor pass (tier B), complete 2026-08-28:** `d(S)=1` CLOSED on 11 of 13,
    **CAPPED on 2** (F3 at 10 of 88 bases, F7 at 41 of 88); `d(S)≥2` COMPLETE 13/13;
    **12,073,707 windows, 0 compressible, 0 shared helpers, 0 B-alarms.**
  * **Run A (tier FH), complete 2026-08-28:** **17,283 rows = the entire
    distinct-mask-multiset population**, all VALID88, all `d2.tested = d2.seeds =
    1,540`, `compressible_total = 0` on every row, 0 duplicate rows, swept-path set
    equals `popfull.txt` exactly.
  * **d3 anchor pass, complete 2026-08-29:** 13 rows × 27,720 triples = **360,360
    triples, all tested, 0 skipped, 0 compressible**, 19,845.6 s.
  * **Six shared-helper rows found** (four carrying 1, two carrying 3) — the first
    ever recorded on valid 88s, **falsifying e13's inherited universal** "no mask
    finishes more than one window; all helpers are distinct". None compresses, but
    `d(S)≥3` on the population is therefore **not** closed by e13's argument.
- **Cost:** run A ≈ **19 CPU-hours**; d3 ≈ 5.5 CPU-hours; the unbought `d(S)=1`
  population pass prices at **~1,200 CPU-hours** (255 CPU-s/circuit vs 4 CPU-s for
  free-helper).
- **Code:** `experiments/e15_campaign3/tools/sweep.py` + `{adopt,slack,triple,cut}.py`.
- **Logs:** `sweep_A_fullpop.jsonl` (12M), `sweep_D3_anchors.jsonl`,
  `sweep_ledger.jsonl` (32 tier-B rows, **15,099,957** `d1.windows` summed),
  `laneSWEEP.md` (68K).
- **Generality:** MIXED.
- **Phase-2:** **keeper — the single most reusable search method in the experiments
  slice**, with two declared sub-gaps carried forward.

### E9 · complete k=3 shell (remove-3-add-2)
- **Family:** exhaustive neighbourhood.
- **What it does:** Complete enumeration of every remove-3 window with a budget-2
  repair, per circuit, with a planted-positive control (pad with a redundant mask,
  remove a window containing it, the routine must find the 2-mask repair).
- **Measured:** control POSITIVE on 88d5, 88d7, 88fs. **Two complete exhaustive
  certificates — 88@7 and 88fs, 27,720 windows each, "EXHAUSTIVE: no
  remove-3-add-2 improvement"** — plus 88@5 stopped INCOMPLETE at 25,064/27,720
  (90 %). Previously only 88@6 had one.
- **Cost:** 1,758–2,700 s per circuit.
- **Code:** `experiments/e3a_exploit/code/k3shell.py`.
- **Generality:** **CIRCUIT-GENERIC** in principle. **Phase-2:** keeper — a bounded,
  cheap, exhaustive local-optimality certificate.

### E10 · basin edit closure sweep (delete k, **forbid** them, re-complete)
- **Family:** plateau-search / neighbourhood exhaustion with a forbid step.
- **What it does:** For a known circuit, deletes `k` non-target masks, **forbids**
  them, and asks whether the targets can be re-completed for ≤ `k` gates. A `k−1`
  completion is a descent (an 87); a `k` completion is a lateral move.
- **Twist:** the forbid step is what makes a `none` verdict mean something — the
  instrument cannot re-derive what it deleted.
- **Measured:** controls re-fired in-session on both geometries before any negative
  was banked: AU0 0 violations / AU2 0 mismatches / AU3 0 of 143 & 0 of 120 /
  **PC-PLANT 40/40** / **PC-BYPASS 22 completions, 22 oracle-VALID**. Both sweeps ran
  to completion: **27,720 / 27,720 triples each. Zero completions at k ≤ 2, i.e. zero
  87 candidates.**
- **Cost:** ~13,000–40,000 s per geometry on 2 workers.
- **Code:** `atlas/thinktank/phase2_alt_run.py` driven from `fleet1/laneD_completions/`;
  ledgers `basin_88at5fs.jsonl`, `basin_88at6.jsonl` (2.9 MB, 27,720 rows each).
- **Generality:** CIRCUIT-GENERIC given a verified circuit to sit on.
- **Phase-2:** **keeper** — the only method in fleet1–4 that generated *new verified
  circuits at the record gate count*, and its negatives are the strongest
  local-rigidity statements available there.

### E11 · all-drop-k local-optimality screen
- **Family:** exhaustive certification at large effective radius.
- **What it does:** Enumerates **every** k-target drop set of a circuit, scores each
  by `W = 88 − |trim|` (the gates the circuit spends privately on that set), and
  refutes `k = W−1` on each — by SAT where needed and by an exhaustive counting
  argument where the arithmetic suffices.
- **Measured:** **88@5: 35,960/35,960 refuted** (8,487 by SAT in 3,875
  solver-seconds, 27,472 by counting, 1 by a cube run). **88fs5: 35,960/35,960
  refuted** — 13,315 screened + 22,645 by counting. Zero improvements, zero timeouts,
  zero non-`unsat` verdicts in either. A `W`-for-`W−1` swap moves up to **`2W−1 = 19`
  masks**, so this is a local-optimality certificate at radius up to 19, against the
  corpus's previous best of "the whole k≤3 neighbourhood is empty".
- **Cost:** ~1 hour per circuit. **Logs:** `experiments/e5_readd/ledger.jsonl` — 72,201 `drop4`
  rows, all `unsat`.
- **Code:** `experiments/e5_readd/code/{screen,report}.py`.
- **Generality:** **CIRCUIT-GENERIC.**
- **Phase-2:** **keeper, top tier — the strongest local-optimality statement
  available**, and now doubled.

### E12 · exact 3-gate finisher (frozen exterior, arbitrary replacement gates)
- **Family:** exhaustive local closure with a proved-complete move set.
- **What it does:** Freezes a circuit's "exterior", deletes a triple of module masks,
  and asks exactly whether ≤ k arbitrary XOR gates can complete all 32 targets with
  the deleted triple forbidden. `k = 3` ⇒ a new 88 geometry; `k = 2` ⇒ an **87**.
- **Twist:** the move set is **proved complete for k ≤ 3** (four-shape case analysis +
  a role argument), strictly stronger than the previous campaign's `fourgate.py`,
  which excluded deep enabler chains by fiat.
- **Measured:** **all 1,540 = C(22,3) triples of the 88@5 geometry are dead** — 869
  cross-cluster + 422 confined + 249 edgeful, zero completions at plane choice #73,
  845 s wall on 7 workers. Tier 1 (the 12 maximal-span triples) also dead on **all
  243/243 plane choices** (2,916 instances). Control discipline: PC1 19/19 over 4,617
  instances; PC3 60/60 — **and PC3 caught a real false-negative bug** (an unsound
  pruning rule) before any negative was banked. Key scoping discovery: **the backbone
  and the 3^k manifold are basin-dependent** — 88@6's manifold is only 3,645/6,561
  valid, so porting the recipe verbatim would have swept an almost-empty set.
- **Cost:** ~36–75 s per (triple, choice); full coverage = 211,167 instances ≈ **2,000
  core-hours**.
- **Code:** `atlas/thinktank/phase2_{geom,fin,controls,run,gen_rest,alt_run,summary}.py`.
- **Generality:** MC-HARDCODED (consumes a frozen geometry). The **control
  discipline** is the transferable part.
- **Phase-2:** superseded in scope by the basin work; keep the control pattern.

### E13 · frozen-exterior module search (backbone + ternary repair planes + defect graph)
- **Family:** structural analysis via exact finite decision.
- **What it does:** Freezes 61 of an 88's masks and treats the remaining 27 as a
  variable *module*; an 87 in that exterior is exactly a 26-mask module. Then
  exhaustively decides small module rewrites with arbitrary (not
  vocabulary-restricted) replacement gates.
- **Measured:** the 88 modules collapse to a **22-mask backbone plus five disjoint
  GF(2) repair planes**, giving exactly **3⁵ = 243** optimal modules; the 15 plane
  masks are provably *exactly* the complete one-step repair frontier of the backbone
  (**15 of 4,459** constructible next gates make progress, and they are precisely
  those 15). Exact finite optimum over the 37-mask quotient = 27 (primal = dual).
  Negatives, all exhaustive within scope: 22-backbone + any four arbitrary XOR gates
  cannot complete (all four first-progress branches closed); **85,293** arbitrary
  2→1 descents from all 243 modules — zero; 5,346 backbone deletions + one arbitrary
  restore — zero; 8,910 and 56,133 deduplicated 2→2 cases — zero; 5,940
  one-backbone+two-plane 87 shells — zero; **6,918,660** 3→3 combinations in the
  36-mask defect language — zero; 249/249 edge-containing arbitrary 3→3 backbone
  triples — zero. Positives: verified **new 88 @ depth 6 circuits using masks outside
  the original 801-mask vocabulary**, an uphill 26→27→28→29 escape where the first
  gate made zero progress, real cross-defect sharing (a verified 89 @ 6 with two
  backbone masks absent), and 4 valid double-backbone 89 modules.
  **`CONFLICT`/correction:** an independent re-implementation found the "243 = 3⁵
  manifold" is actually **729 = 3⁶** once the sixth coordinate is unfrozen (729/729
  oracle-VALID), and that the manifold is a *known* gauge orbit. Also: the "22+5
  backbone" picture is **family-local, not a property of 88-gate circuits** — only 17
  of 62 families have all slots ternary; cores run 78–83, so "the" 22-mask backbone
  is anywhere from 18 to 26, and **no lower bound can be built on it.**
- **Code:** described in `new-representation.md` §§15–64; re-checked in
  `beat88/methods/m5_backbone/verify/VERIFICATION.md`.
- **Generality:** **CIRCUIT-GENERIC method, instance-specific results.**
- **Phase-2:** **keeper as a method, superseded as an argument** — every negative is
  a small-radius statement.

### E14 · exhaustive small-SLP decision (`slp3.py` / `le4_k2.py`)
- **Family:** exact micro-search with a closed case list.
- **What it does:** Decides, exhaustively, whether there is a straight-line program of
  `G ≤ 3` (resp. `G ≤ 4`) gates over a given available-signal pool producing **both**
  of two required masks. This converts a local rebuild question into arithmetic: at a
  k=1 site `gates = 84 + G`, so **87 iff `G ≤ 3`**; at a k=2 (three-orphan) site
  `gates = 83 + G`, so **87 iff `G ≤ 4`**.
- **Twist:** it is **shape-free** — it replaces the specific "W-shape" an earlier
  instrument invented with the complete question, and is therefore ~100× wider.
- **Measured:** whole corpus, 18,355 circuits, 1,686 s: **55,970 candidate sites
  (k=1: 54,561, k=2: 1,409), sites with `G ≤ 3`: 0, oracle-VALID below 88: 0.** k=2
  regime: 1,409 sites, 1,309 decided `G > 4` by the fast procedure and the **100
  UNDECIDED closed by brute force, 100/100 `G > 4`** — so the **2-mint/3-orphan
  regime is CLOSED on this corpus**, not bracketed. Completeness attacked
  adversarially: `slp3.py` survived **8,000 randomly-generated 3-gate SLPs of every
  topology with any 2 of 3 gates designated outputs — 0 missed**, plus 0/3,000 false
  positives and every returned program replayed.
- **Cost:** 1,686 s for the corpus run; ~11 CPU-hours would brute-force all 1,409 k=2
  sites (not spent).
- **Code:** `experiments/e16_lastwish/lane536/{slp3,le4_k2,le4_undecided,corpus_le3,completeD,completeD2}.py`.
- **Generality:** **CIRCUIT-GENERIC.**
- **Phase-2:** **keeper — the cleanest "is this circuit one gate from smaller?"
  decision procedure the project owns.**
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** Generality is over-broad for 3 of the 6 files named. `slp3.le3` and `le4_k2.le4` are genuinely circuit-generic, but `completeD.py:38` (`INPUTS = {1 << i: i for i in range(32)}`), `:79,120` and `:184,187` (`== 88`) are 32/88-bound. The entry prices no port cost; a real port needs a new site-finder and oracle.

### E15 · one-target-short exhaustive completion probe
- **Family:** exact decision at population scale.
- **What it does:** For every harvested 88-gate state and every one of its 32 targets,
  delete that target's gate, trim, and exhaustively probe every closure pair for a
  completion at ≤86 or ≤85.
- **Measured:** **1,119,399 distinct 88-states × 32 targets → 1,630,797 objects
  trimming to ≤86 (23,864 to 85), all probed exhaustively, 0 completions**, 1,611 s
  wall across 3 shards. A relaxed-threshold self-test found **1,703 real
  completions**, so the instrument has power.
- **Code:** `campaign_87/wave5_2026-08-04/burn/simple/execute/{scan86,scan87}.py`.
- **Phase-2:** keeper — cheap, powered, and it produced a ρ-class asymmetry finding.

### E16 · thinker_c exhaustive completion scan (closing a pre-existing population)
- **Family:** exact enumeration over a relaxed population.
- **What it does:** Uses the sound reduction "an 87 exists ⟺ some 86-mask, 31-target
  state completes", and exhaustively re-bases and scans the entire 31-target
  population a previous campaign had generated and **never analysed**.
- **Twist:** it *closes* a whole pre-existing population rather than searching a new one.
- **Measured:** **629,274 states scanned, 282,970 at |S| = 86, 0 completions, 6,487
  positive controls at |S| = 87.** The completion predicate was validated by the only
  authority that counts: A8 turned 12 of them into circuits, **12/12 VALID at 88
  gates.** Net effect: the thinker_c population (612,949 distinct sub-88 states,
  never censused) is **CLOSED**.
  ⚠ The 6,487 verified-88 completions are **counts only — not materialised on disk**;
  using them as donors needs the scan re-run with a dump.
- **Code:** `beat88/methods/m4_inverse/{scan_thinker_c,realize_completion}.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper** — "find a sound relaxation whose population already exists,
  then close it exhaustively" is cheap and produced a real theorem-shaped negative.

### E17 · down-step / reduction-lemma analysis
- **Family:** exact decision + theory.
- **What it does:** Asks "remove k masks, restore with k−d" for d ≥ 2 (a double or
  triple step) rather than the usual d = 1, then proves the whole family reduces to
  one coordinate.
- **Twist:** it produced a **theorem that retires a whole family of ideas**: every
  "remove k, add k−d" question reduces to a single coordinate `m` = the size of the
  target-free window; the step depth d is bookkeeping. Down-1 and down-2 are equally
  dead at equal m. **Reachable m ≈ 4–5; historical improvements sit at m ≈ 42.**
- **Measured:** 77,195 ledger lines, **82,786 UNSAT / 748 partial-nosol / 197
  timeout**; 20,893 down-step window decisions, 0 SAT, 99.0 % theorem-grade; **9
  exhaustive theorems**; 88→86 does not fire. One completed m=4 exhaustive theorem on
  a 90-gate anchor cost **16.0 core-hours** (424,270 target-free windows, 0 hits).
- **Code:** `campaign_87/wave5_2026-08-04/burn/downstep/{downstep,exhaustive3,exhaustive4,reach}.py`.
- **Phase-2:** keeper as a *theorem*; the search itself is retired by its own lemma.

### E18 · exact k−1 shell over all 2³² (|W| = 1 and |W| = 2)
- **Family:** exhaustive completeness search over the entire mask universe.
- **What it does:** Asks whether any `k−1`-set of the form `(R∖{r₁,r₂}) ∪ {g}` — or
  `(R∖{r₁,r₂,r₃}) ∪ {g₁,g₂}` — completes an 88's core, for **arbitrary masks over the
  whole 2³² universe**, not a vocabulary. Completeness comes from an *unlock-event
  argument* (the first unlock must be E1 or E3), which restricts candidates to a
  provably sufficient finite set.
- **Twist:** the only 87-hunting instrument whose negatives are exact over all 2³²
  **and** reached by an argument rather than by enumeration. The |W|=2 version adds a
  three-branch exhaustive case split, one of which (B3, "enabler-first") is the
  *deception-door* shape — a gate that unlocks nothing and exists only to make the
  next gate derivable.
- **Measured:** **U1-14** — 4,127 pairs, 28,167 exact states, **0 completions**.
  **U1-23** — 7,223 triples, 464,522 B1 pairs, 2,159,283 B3 pairs, 474,511 B2/kernel
  tests, **0 completions**. Certified on 4,127 *true positives* with all three
  branches firing; screen accepts 4,127/4,127. Closed region: *delete ≤3 repair gates,
  add ANY ≤2 masks, all 204 families.* Instrument certificate U1-24:
  `Repair.fast_unlock` validated on **815,974 cases, 0 mismatches**.
- **Code:** `beat88/understanding/u1_obligations/{pc_km1_exact,km2_exact,run_km2}.py`.
- **Generality:** MIXED — the completeness argument is CIRCUIT-GENERIC (it uses only
  the E1/E3 event taxonomy); retargeting needs a new target set, a corpus of
  near-optimal circuits, and a re-audit of `fast_unlock`.
- **Phase-2:** **keeper — the best exact instrument in the understanding half.**

### E19 · certifier inverted into a move generator
- **Family:** exact → local search.
- **What it does:** Runs the window certifier not to certify but to *enumerate* the
  complete radius-2 exchange neighbourhood, producing new circuits rather than
  verdicts.
- **Measured:** complete radius-2 exchange neighbourhood of an 89 in **56 s
  single-core, 521 distinct sibling 89s**.
- **Phase-2:** keeper. (Sibling: `depth-capped component enumeration` — an 88@5's
  depth-5 component is **exactly 135 states in 18 s**, the same 135 a multi-day fleet
  found by replaying 37,305 states over 20 h.)

---

# Family F — SAT / MaxSAT / PB / CP-SAT decision procedures

Thirty-one entries. The two structural lessons of the whole family, both measured:
**minimise, never decide** (F17), and **an UNSAT is only as strong as the encoding
choice you did not vary** (L11).

### F1 · windowed FSK SAT (fixed slot order)
- **Family:** SAT bounded synthesis — the original SAT instrument.
- **What it does:** Freezes all but k of a circuit's gates and emits a CNF asking
  "can this window be resynthesized with k−1 gates?" in a Fuhs–Schneider–Kamp-style
  encoding where any model decodes to a whole realizable circuit. Every window's
  removal set is logged with its verdict so runs resume; every model found is
  re-verified through the oracle.
- **Twist:** it reaches window sizes the exact deciders cannot (k = 9–16 vs k ≤ 4), at
  the cost of being **UNSAT relative to the encoding's fixed slot order** — strong
  evidence, not a completeness proof.
- **Measured:** first generation — 137 windows (0 SAT / 88 UNSAT / 49 timeout), max
  UNSAT window k=12; found and worked around a pysat bug
  (`Cadical153.interrupt()` raises `NotImplementedError`, so timeouts were silently
  ignored). Archived generation — **48 windows on the reference 88 at k = 9–16: 34
  UNSAT, 14 timeout, 0 SAT.** Max window proven UNSAT: **k = 16** (previous frontier
  12). Hardness anti-correlates with **nB (broken kept masks), not k**: every window
  with nB ≥ 19 was decided. Pipeline self-test: a planted r=k window came back SAT in
  1.6 s and decoded to an oracle-VALID 88 @ 7.
- **Cost:** individual UNSATs up to 1,509 s.
- **Code:** `campaign_87/agents/sat-window/sat_window.py`.
  **Logs:** `evidence/campaign87_certificates/sat_deep/`.
- **Generality:** **CIRCUIT-GENERIC encoding, MIXED harness.**
- **Incarnations:** `campaign_87:windowed FSK SAT` → `root_infra:windowed-sat-fsk`
  (archived) → superseded by F6/F8.
- **Phase-2:** **superseded** by the order-free lift (F6) and the GF(2) encoder (F8),
  but it is the only method that reached radius 16.

### F2 · killable-subprocess SAT driver
- **Family:** SAT infrastructure.
- **What it does:** Runs CaDiCaL/Kissat in a child process killed by the OS at the
  deadline, sidestepping the pysat interrupt bug, with resumable JSONL task ledgers
  keyed by window id.
- **Measured:** moved the max proven-UNSAT window from **k=12 to k=16**; six wave-1
  timeouts became UNSAT at 212–1,509 s.
- **Code:** `campaign_87/agents/sat-deep/{sat_deep,solve_child}.py`.
- **Phase-2:** keeper (infrastructure).

### F3 · symmetry-broken SAT (SB-P + SB-F)
- **Family:** SAT + sound symmetry breaking.
- **What it does:** Adds two soundness-proved clause layers — SB-P (parent
  commutativity, lexicographic order within a gate) and SB-F (conditional
  lexicographic order on adjacent *free* slots). Clauses are only added, so an UNSAT
  can never be manufactured; SAT-preservation is what needs proving, and it was
  measured (7/7 planted self-tests decoded to verified 88s).
- **Measured:** known UNSATs re-decided **14–34× faster** (960/1,000/1,509 s →
  28/45/106 s). Re-adjudicated the 14 survivors of the deep sweep: **10 UNSAT, 4
  undecided, 0 SAT**, including the two loosest windows (nB = 3, nB = 5). Final
  standing on the reference 88: **48 windows → 44 UNSAT, 4 undecided, 0 SAT, frontier
  k = 16.** On the project's independent 88 @ 7: 8 cone windows → 5 UNSAT, 3
  undecided, 0 SAT, including an nB = 1 window in 34 s — *the only SAT coverage that
  circuit has.* Third-family application: anchor 50 windows → 37 UNSAT / 13
  undecided, **entire k ≤ 12 regime UNSAT, 28/28**.
- **Code:** `campaign_87/agents/frontier-sat/frontier_sat.py` (implementation),
  `campaign_87/agents/loose-sat/loose_sat.py` (runs).
- **Generality:** **CIRCUIT-GENERIC.**
- **Incarnations:** `campaign_87:symmetry-broken SAT` · `root_infra:windowed-sat-kissat-symbreak`.
- **Phase-2:** **keeper — the best cost/coverage instrument in the certificate
  archive.** Its residual gap (fixed slot order) is quantified, not hand-waved.

### F4 · SB-D depth-sorted symmetry break
- **Family:** SAT symmetry breaking, for depth-capped encoders.
- **What it does:** Sorts slots by non-decreasing depth, tie-breaking equal-depth
  neighbours by mask lex. Sound and complete; mutually exclusive with SB-F.
- **Measured:** **19.6 s vs 222.7 s head-to-head (11×) ≈ +3 slots of reach** on cone
  geometry. **Important negative on its transfer:** ported to the order-free window
  encoder it is **1.21× SLOWER** (SB-F 26.2 s vs SB-D 31.8 s over 9 decisive pairs),
  because that lane runs `cap=None` and SB-D must pay for a depth ladder it does not
  need. The head-to-head harness *first printed "SB-D DISAGREES — UNSOUND"* and was
  wrong — it compared a `timeout` against an `unsat`; fixed to classify only
  sat-vs-unsat as unsound. Recorded as a near-miss false alarm.
  Second finding from the same lane: **the depth cap is a major cost driver**, so
  gate-count-only questions should run at loose caps.
- **Code:** `beat88/methods/m2_oracle/code/gsat_sbd.py`.
- **Phase-2:** **keeper for any depth-capped encoder.**

### F5 · fence / topology-family SAT (order-free by construction)
- **Family:** SAT with symmetry eliminated by construction.
- **What it does:** Enumerates *fences* — ordered partitions of the free gates into
  levels — and solves one CNF per fence with the level structure pinned. Every DAG
  conforms to exactly one fence, so the family is complete and slot-permutation
  symmetry is eliminated **by construction, not by clauses**. An UNSAT sweep over all
  fences of a window is a real theorem with no ordering caveat.
- **Twist:** **the only certificate class in the entire project without the slot-order
  caveat.** Ported from Haaswijk et al. (TCAD 2020) onto the existing encoder because
  `percy` itself cannot run here (truth-table based, ≤8 inputs).
- **Measured:** validated 11/11 planted, 94/94 against the exact decider, adversarial
  soundness probe 8/8. Sweeps: round-1 9 order-free UNSAT / 931 units; family 10 UNSAT
  / 9 open-hard / 18,294 units / **215.1 h solver time**; novel-89 16 UNSAT / 5,238
  units / 41.9 h. Whole-track ledger: **29,125 unsat, 433 trivial-unsat, 78 timeout,
  24 open-hard, 13 sat (all planted/validation)**. **But its own positive control
  killed it**: 30 windows across slack 1–9, `{open-hard: 13, unsat: 17}`, **0 SAT** —
  including a control where nine gates of slack provably exist. A k=13 window cannot
  see a one-gate improvement that is provably one gate away.
- **Code:** `campaign_87/wave5_2026-08-04/fence_sat/{fence_sat,sweep,validate}.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper for certification, dead as a discovery instrument at k ≤ 13.**
  Its 28 highest-value windows were never run.

### F6 · slot-order-free window SAT (A3)
- **Family:** SAT, order-free by encoding.
- **What it does:** Encodes a window as "these kept masks must each equal *some* free
  slot's value", removing the arbitrary slot ordering. The CNF is a function of the
  kept *set*, so an UNSAT is a real theorem.
- **Measured:** **408-job run at maxslots 12 → 399 UNSAT, 0 SAT.** Cost curve measured
  on real windows: 9 slots 4.4 s, 11 slots 9.7 s, 12 slots **76.0 s** — ~7.8× per
  slot, extrapolating to ~600 s at 13 and ~4,700 s at 14. **Recommendation recorded:
  do not run the 13–14 escalation** (order 10⁴ core-hours). Its predecessor produced
  the **first caveat-free UNSAT** in the project and bracketed the practical cut-off
  at `nB + r ≈ 12`.
- **Code:** `beat88/methods/m2_oracle/code/a3_window_sat.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper, but blocked on encoding** — a slot bump is not affordable;
  the next gain needs an encoding improvement (incremental SAT / cube-and-conquer were
  never installed here).

### F7 · cone-window exact synthesis (A4) and the convex-block band
- **Family:** exact-window / SAT, window chosen by circuit structure.
- **What it does:** Cuts a window by *output cone* (pick 16 of 32 outputs, delete every
  mask private to them) and exactly re-synthesizes that sub-circuit with one fewer
  gate. Every deleted slot is free by construction, so there is no slot-order caveat.
  The sibling **convex-block / band splice** variant instead cuts out **out-degree ≤2
  connected components** of the DAG (size 9–28) and asks the down-1 question.
- **Measured:** cone form — **kill test met.** The frontier is ~10–12 free slots; the
  literal |O| = 16 cone problem needs **31–34 slots**. **7 genuine cone UNSAT theorems
  banked** (the driver declined to ask the real question on any cone whose control had
  not resolved; controls 8/8 then 4/6 + 2 timeouts, **0 refuted**).
  Band form — 290 rows, controls OK 274 / VACUOUS 16: n≤9 15 unsat, n=10 70 unsat + 28
  timeout, n=11 30 unsat + 65 timeout, **n=12 2 UNSAT** + 34 timeout, n=13/14 timeout
  only. **Zero SAT anywhere.** Its predecessor filter (out-degree-1 windows) is
  **provably inert on an 88** — every component is a singleton on all six circuits
  tested.
- **Code:** `beat88/methods/m2_oracle/code/a4_cone.py`;
  `campaign_87/wave6_2026-08-11/band_hunt/band.py` (37K — the wave's most reused module).
- **Phase-2:** **cone form dead-end as specified** (frontier 10–12 vs 31–34 slots);
  band form keeper; **F4 (SB-D) is the keeper that came out of it.**

### F8 · GF(2)-explicit (XOR-native) SAT encoding
- **Family:** SAT encoding — the production window instrument from 2026-08-11.
- **What it does:** Replaces the Tseitin-triple window encoding with one selector row
  and one XOR row per bit, keeping the GF(2) structure explicit so only
  free-slot→free-slot fan-in is bilinear.
- **Twist:** it is the *encoding*, not the solver, that moves the ceiling — a positive
  test that also **refutes** the Gauss-Jordan hypothesis (the 5 GJ matrices engage and
  buy nothing measurable).
- **Measured:** CNF at n=12 is **19.7 k clauses vs 106.7 k (5.4× smaller)**;
  head-to-head over 64 solves, new-only wins 4, old-only 0, **median 9.3×**; at n=16
  old 0/2, new 2/2. **Ceiling moved n=12 → n=14.** Validation V1–V6 pass, including V6
  54/54 against a brute-force oracle with no SAT solver.
- **Self-reported defect (quarantined, honest):** `_exactly_two` initially asserted
  only one half of the sequential counter, so a free slot could degenerate into a copy.
  All UNSATs stayed sound and every SAT was oracle-verified, but the first head-to-head
  was biased in the new encoder's favour, and **all six validation gates passed with
  the bug present.** Superseded rows are quarantined on disk.
- **Code:** `campaign_87/wave6_2026-08-11/xor_encoding/{xorenc,bench,hunt}.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper — this is the SAT instrument to carry forward.**
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — the headline size ratio is computed from quarantined, superseded data, and one control claim is contradicted by its own log.** (a) "19.7 k clauses vs 106.7 k (**5.4×** smaller)": 19,666 appears **only** in `runs/relaxed_encoder_SUPERSEDED/ceilingA.jsonl`, i.e. runs made with the `_exactly_two` bug this entry itself quarantines. The current post-fix encoder at n=12 gives **26,428 clauses + 384 XOR rows** (`runs/ceilingB.jsonl`), so the true ratio is **4.04×, not 5.4×**. (b) **"V6 54/54" is unbacked** — the only validation log on disk reads `[FAIL] V6 new encoder matches the proven-complete exact decider agree=0 (UNSAT=0 SAT=0) disagree=0` / `VALIDATION FAILED` (`runs/validate2.log:32,34`); 54/54 exists only in prose. (c) Generality **MIXED**, not CIRCUIT-GENERIC: `bench.py:55` imports `mixcolumns_core`, `:313` loads a MixColumns 88, `hunt.py:65-69` hardcodes five MixColumns circuits; `xorenc.py` is width-locked to 32. Verified and standing: 64 solves, median **9.3×**, ceiling n=12 → n=14. Minor: "at n=16 old 0/2, new 2/2" is a stale mid-run snapshot; the completed `ceilingC.jsonl` has three pairs (old 0/3, new 3/3).

### F9 · depth-capped exact SLP oracle (`dslp`)
- **Family:** SAT-based exact decision; a genuinely new instrument.
- **What it does:** Decides *minimum gates subject to a depth cap*, with **levelled
  inputs** (a block's inputs are not free — currency arrives at level 1/2/3, an
  interface value arrives wherever its producer put it) and **per-target caps** (one
  block must deliver its own targets by level `D` but its exported interface several
  levels earlier). Order-encoded level variables `a[i][l]` = "level(gate i) ≤ l" plus
  `z → level(i) ≥ level(operand)+1`; each normalisation rule argued depth-safe in the
  docstring. An exact reachability precheck over the whole `2^r` value space reports
  `infeasible_depth` rather than letting a solver grind.
- **Twist:** the base CNF is **re-implemented rather than imported**, so "cap off
  reproduces `slp_opt`" is a two-implementation control and not a tautology.
- **Measured / controls, all three fired:** (A) cap-off vs `slp_opt` **10/10** on real
  block instances, plus at full scale (`U07` uncapped = 12, `W3` uncapped = 8);
  (B) exhaustive brute force **40/40** uniform caps and **60/60** per-target caps
  against a BFS enumeration sharing no code with the SAT path — and it certifies every
  UNSAT level, not just the value; (C) planted positive found at 5 gates and replaying
  at depth 3, with the same targets at cap 2 correctly `infeasible_depth`. `dslp` is
  also **2–7× faster than `slp_opt`** on every capoff row.
- **Cost:** **91 exact depth-capped block decisions, 5 timeouts, 13,215 s** of solver
  wall at `--cores 6`, plus 80 exhaustive currency curves with no solver at all.
- **Code:** `fleet4/laneDEPTH/code/{dslp,selftest_dslp,model,genD}.py`; single copy now
  in `fleet8/unified/code/dslp.py`.
- **Generality:** **CIRCUIT-GENERIC.** The instrument knows nothing about MixColumns.
- **Phase-2:** **keeper — the most reusable new tool of fleet1–4**, and the only
  oracle in the repo that can price depth.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — the Cost line does not reproduce from its own stated source.** "91 exact depth-capped block decisions, 5 timeouts, 13,215 s of solver wall" is sourced to `code/tally.py` §D over `results/dcache.jsonl`; that file today holds **97 rows — 81 exact + 7 infeasible_depth + 9 timeouts, wall 157,413 s**, and no prefix of it reproduces 91/5/13,215 (last-wins dedup by key gives 73/7/6 and 82,311 s). `RESULT.md` hedges with "Tally **at write-up**"; this entry dropped the hedge — restore it or re-tally. Second: "**2–7×** faster than `slp_opt` on **every** capoff row" — the actual range is **1.96×–7.45×**, two of ten rows outside the band. Third: "single copy now in `fleet8/unified/code/dslp.py`" is false — `fleet4/laneDEPTH/code/dslp.py` (608 lines) still exists and differs from the fleet8 copy (671 lines). The CIRCUIT-GENERIC label **is** correct: zero MixColumns constants and zero 32-bit assumptions in either copy.

### F10 · joint-block boundary test (dim-16 merged ladder)
- **Family:** SAT joint levels.
- **What it does:** Takes two adjacent blocks, builds ONE block carrying both their
  targets on the union of their working lines, and climbs the gate ladder
  k = lb, lb+1, …. A pre-flight asserts the instance is exactly the union (no
  fabricated free values) *before* any compute is spent. SAT at the decisive level
  means the split model over-prices the boundary; UNSAT means the boundary is free; a
  timeout is a bracket.
- **Twist:** the pre-flight earned its keep — its first run **FAILED**, catching eight
  fabricated masks that scaffolding had minted with `add_chain` and that would have
  made a day-long dim-16 SAT result worthless.
- **Measured:** W3|U4 at the 88@7 cell, dim 16, 8 targets, 33 free values = exactly
  W3's 26 ∪ U4's 25, split total 15, decisive k = 14. **k = 9/10/11/12/13 all
  exhaustively UNSAT** at 23.7 / 123.8 / 785.3 / 5,202.2 / **105,083.4 s.** So
  `merged ≥ 14`, and with the replay bound `merged ∈ {14, 15}`.
- **Cost:** 2026-08-25T03:42 → 2026-08-26T11:01, ~31 h on 8 cores; **~16.6× per gate
  level**.
- **Code:** `fleet8/unified/code/joint.py` (`preflight()` / `run()`).
- **Generality:** CIRCUIT-GENERIC in shape.
- **Phase-2:** **keeper**, with the caveat that ~16.6×/level at dim 16 makes it
  affordable only for a boundary you have already priced. **The decisive k = 14 is
  still open** (see F11/F12).

### F11 · monolithic SAT portfolio
- **Family:** SAT joint levels — the opposite bet from cubing.
- **What it does:** Hands the *identical* CNF to four different complete SAT solvers,
  one core each, and takes whichever finishes first. Because all four are complete,
  whichever answers first gives a sound verdict.
- **Measured:** k=11 UNSAT in **218 core-s**; k=12 UNSAT in **5,762 core-s** (26.4×
  growth). Four k=14 processes ran **3 days** with no verdict and **zero bytes of log
  output**. It buys a measured **7.2×–28.8× cost advantage over cubing**, and pays for
  it by losing everything if killed.
- **Cost:** cadical195 / cadical300 / kissat404 / glucose42, 1 core each, ~288
  core-hours spent.
- **Code:** `fleet11/laneCUBE/code/mono.py`. *(Directory is LIVE — do not touch.)*
- **Generality:** CIRCUIT-GENERIC (instance-file interface).
- **Phase-2:** **keeper.** Cheapest known route to a hard level; the honest framing is
  "buy it as a portfolio and expect weeks".

### F12 · resumable cube-and-conquer (banked cubes)
- **Family:** SAT decomposition + engineering.
- **What it does:** Splits a level-`k` decision into independent cubes, solves each
  separately, and **writes every finished cube to an append-only file**, so a crash or
  deadline costs only the cubes in flight and `--resume` picks up where it stopped. A
  level is proven only at full cube coverage; a single undecided cube makes the run
  UNDECIDED.
- **Three partition choices were measured, and they are not equivalent:**
  * **on gate 0's input pair** (an exact partition since the pair selector is
    exactly-one): fleet11's 528-cube split cost **18,540 core-s at k=11 against 218
    core-s for one monolithic solve — 85× worse**, and 2–3× worse than banked runs
    elsewhere. Grouping 33 cubes per solver recovers 2.3× (12,902 → 5,631 core-s,
    validated 528 compared / 0 disagreements). Extrapolated true price of k=14:
    **653–1,113 core-hours, and the cheapest route does not parallelise.**
  * **on semantic positions** (which gate carries each target — exactly one must):
    e5's 56-cube split finished a k=9 level the monolithic solve could not do in
    3,600 s, **56/56 cubes UNSAT, none undecided.**
  * **on depth-3 root cubes** (e11): k=11 levels closed at 6,043,276,712 nodes
    (2,726 CPU-s) / 5,846,598,421 nodes (2,669 CPU-s).
  * `march_cu` generic cubing on a 34,062-var / 355,842-clause rung: `-d 8` gives 256
    cubes in 9.5 s and **0 of 256 decided in 9 minutes**; verbatim, *"the ×20–100 of
    the plan is NOT there. Measured multiplier ≈ 1."*
- **Also measured (e7):** a projected ~12 CPU-hours for a level cost **5,689
  CPU-seconds** — a 7× pessimistic projection. Per-level CPU: k=7 → 42 s, k=8 → 83,
  k=9 → 788, k=10 → **5,689**.
- **Code:** `experiments/e7_push/code/cube.py` (the ancestor),
  `experiments/e5_readd/code/cube.py`, `fleet1/laneB_regionbounds/code/qsolve.py`
  (`--shard`, split2 → 1008 cells), `experiments/e11_quad10/code/shard.py`,
  `fleet11/laneCUBE/code/cube16.py`.
- **Generality:** **CIRCUIT-GENERIC** (wraps `slp_opt` / an instance file unchanged).
- **Incarnations:** `experiments_early:resumable cube-level exact decision` +
  `position-cube-and-conquer` → `fleet1:cube-banked-resumable-exact-search` →
  `experiments_late:dim10-quad-ladder` → `fleet9_12:sat-cube-and-conquer-on-gate-0`.
- **Phase-2:** **keeper, with the partition choice as the load-bearing decision.**
  Cube on *semantics*, not on gate 0. Any long exact solve should be built this way.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — the phase-2 verdict inverts what the primary concluded.** This entry makes the *partition choice* load-bearing ("cube on semantics, never on gate 0"). `fleet11/laneCUBE/RESULT.md` says the opposite about the cause: *"The 59×–131× multiplier above is **not the partition's fault, it is the process granularity**: one solver per cube throws away every clause the previous cube learned"* — and grouping recovers **2.3×** on the **identical** gate-0 partition. So the 85× prices process granularity, not gate-0-vs-semantics. Keep the method; reword the recommendation as "group cubes into one solver process", with the partition choice secondary. Every measured figure verifies. Path nits: `qsolve.py` has no `--shard` flag (it has `--split2`), and the march_cu code (`campaign_87/wave6_2026-08-11/sat_boost/cnc.py`) is missing from the Code list.

### F13 · CNF partition machine-check
- **Family:** SAT correctness control.
- **What it does:** Before any cube is dispatched, checks *on the real CNF* that the
  cubes really do partition its models: the count is C(33,2) = 528; the enumerated
  pairs are exactly the input pairs in the solver's own key order; the at-least-one
  clause is literally present in `cnf.clauses`; and — asked of the solver rather than
  assumed — forcing two cubes is UNSAT and forcing none is UNSAT.
- **Twist:** most decomposition arguments in this repository are prose. This one aborts
  the run if it fails, and re-runs at every k.
- **Code:** `partition_check()` inside `fleet11/laneCUBE/code/cube16.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper.** Cheapest possible insurance against the classic
  decomposition bug.

### F14 · SAT set-blocking enumeration (enumerate all optimal value sets)
- **Family:** exhaustive enumeration by SAT.
- **What it does:** Enumerates all optimal value sets by asking a SAT solver
  repeatedly and adding one clause after each answer that forbids exactly that *set*,
  until the solver says UNSAT.
- **Twist:** ~**100× faster** than the DFS equivalent (G5) at dimension 12, and it
  terminates in a machine-checked UNSAT rather than an exhausted search tree.
- **Measured:** agreed with the DFS on all 8 blocks the DFS could finish (sets
  identical, not just counts); independently reproduced the U07 counts
  (3, 3, 12, 18, 3, 10, 3, 1, 1) on nine record blocks; `record_set_found` true across
  99 cells. **Erratum caught by its own control:** the first blocking clause had
  inverted polarity, so the block never bit and the enumerator looped on one solution
  forever — **no number from that version reached the report.**
- **Cost:** 306,903 s wall over 116 rows (85.3 h), including single cells of 32 h and 16 h.
- **Code:** `fleet9/laneENUM/code/satenum.py`, control `satenum_ctrl.py`.
- **Phase-2:** **keeper** — the fast half of the enumeration pair; keep G5 as its
  cross-check.

### F15 · SAT with banned or required values (forcedness test)
- **Family:** structural analysis by SAT.
- **What it does:** Asks for an optimal program **with a specific intermediate value
  forbidden**. If the answer is UNSAT, that value is not merely *usable* — every
  optimum must build it.
- **Twist:** it turns "the solver reached for X" into "the solver cannot do
  otherwise". It is the only instrument that can promote a hand-picked constant to
  DERIVED.
- **Measured:** control fired in both directions on real blocks (ban a value the
  unique optimum uses → UNSAT; ban one it does not → SAT; require used → SAT; require
  unused → UNSAT; **10/10**). Headline: banning `δ₃(0xc)` on the unprompted merged
  `{2,3,7}` block at k=9 returned **UNSAT in 3,668 s over all 300/300 cubes**, so
  **every** 9-gate optimum builds it — with a fired positive control (9 distinct optima
  enumerated, all building exactly that one tap-3 value, rank exactly 1).
- **Code:** `fleet9/laneENUM/code/satban.py`, `q27force.py`, control `satban_ctrl.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper, and under-used.** The cheapest way to retire a "we picked this
  because the record had it" tag anywhere in a future package.

### F16 · RC2 MaxSAT alphabet floors (union / per-region)
- **Family:** exact MaxSAT over a restricted mask alphabet.
- **What it does:** Takes the union of two verified circuits' mask sets as the
  alphabet and asks RC2 for the *exact* minimum-size circuit realizable inside it.
- **Twist:** exact, not a bound; and the union always contains a complete 88 by
  construction, so no separate vacuity control is needed.
- **Measured:** **347,525 pairs decided, floor distribution {88: 347,509, TIMEOUT: 16},
  best floor anywhere 88**, mean 2.45 s/pair (≈**236 core-hours**); ledger tally
  749,150 OPTIMAL / 125 TIMEOUT. **Its own power control is the whole story:**
  union(89_a, 89_b) from different lanes hits floor 88 in **4 of 600 pairs (0.7 %)** —
  so the instrument *can* find a −1, at a measured rate, and never did at 88. Four
  named cross-region 88s were produced this way and oracle-verified.
- **Code:** `campaign_87/wave5_2026-08-04/burn/union_sat/work/*.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper — with its own control, the best-calibrated negative in the
  campaign_87 slice.**

### F17 · exact alphabet-floor MaxSAT ("minimise, never decide")
- **Family:** exact optimisation / MaxSAT.
- **What it does:** Fixes a finite alphabet `A` of candidate gate masks and a depth cap
  `L`, then asks RC2 core-guided MaxSAT for the **minimum** number of gates from `A`
  that builds all 32 outputs at depth ≤ `L`. The optimum is decoded, re-scheduled
  depth-optimally, and handed to the oracle in the same run.
- **Twist — the most transferable methodological result in its slice:** it *minimises*
  instead of *deciding*. The returned optimum is its own oracle-verified positive
  control, so it structurally cannot produce a vacuous negative — unlike its own
  sibling `d4decide.py`.
- **Measured:** floor = **91 at depth ≤ 4** over 5 independent vocabularies (91, 91,
  92, 117, 155, 189, 195, **227** masks) and over the 300 most-frequent masks of the
  whole 15,912-circuit depth-4 population. **1.3 s at 227 masks; 23.4 s at 300;
  TIMEOUT at 400, 554, 600, 688.** The decide form on the same 227-mask instance did
  not return in >500 s — a **≥400× gap.**
- **Code:** `experiments/e4_depth/code/{d4floor,d4decide,harvest}.py`.
- **Generality:** **CIRCUIT-GENERIC** in form, MC-hardcoded in the target list only.
- **Phase-2:** **keeper, top tier.** "Minimise, never decide" should be the default.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — one wrong figure.** "floor = **91** at depth ≤ 4 over 5 independent vocabularies (91, 91, **92**, 117, 155, 189, 195, 227 masks)": the 92-mask vocabulary `C92` has floor **92, not 91** — it is the one alphabet in the table that does not give 91 (`experiments/e4_depth/RESULT.md:309-330`, row `C92 92 4 92 0.0 True`). The list also drops `A_plus_88d5` (138 masks, floor 91) and double-counts 189. Everything else stands, and the ≥400× gap is real and conservative. Note for reuse: the two decide-form rows are banked with `control False` — their positive control never fired, which is exactly the vacuity this entry's Twist claims for `d4decide.py`.

### F18 · skeleton pools + RC2 exact-floor generator
- **Family:** generate-and-decide at scale.
- **What it does:** Generates mask alphabets by closure and lattice construction and
  asks RC2 for each one's exact minimum, so a floor ≥ 88 *is* the K=87 UNSAT and ships
  its own decoded 88-gate witness.
- **Measured:** **88,908 pools decided by exact floor** at 4,818/h, mean 1.00 s per
  floor, 10.4 h uptime. Floor distribution 88 → 16,941 (19.05 %), 89–91 → 7,095,
  92–95 → 19,691, 96–100 → 26,143, 101+ → 19,026. Positive-control chain
  **25,074/25,074**. Elite archive of 300, **all floor 88**. Stopped when its kill
  criterion fired: the `nov` family scored **0/4,440 at floor 88** (min 89) — every
  measured step away from an anchor costs at least a gate.
  ⚠ An audit found its cross generator **silently capped at 4 bit-planes**.
- **Code:** `campaign_87/wave6_2026-08-11/skeleton_pools/{gen,loop,sp_core,worker}.py`.
- **Phase-2:** keeper, with the plane cap noted (see L37).

### F19 · pattern-class exact window floors (Sun–Yang–Li residue classes)
- **Family:** exact MaxSAT over a literature-derived alphabet.
- **What it does:** Restricts the alphabet to Sun–Yang–Li's seven maximal residue
  patterns (**12,945 masks = 3.0 × 10⁻⁶ of 2³²**) and computes exact class-window
  floors by RC2.
- **Measured:** **177 exact floors, zero improvements**, 0.1–230 s each (median ≈7 s)
  on windows where a bit-vector K−1 rung will not close in 120 s. Every verdict carries
  its own RC2 witness, so none can be vacuous. D0/D1 lanes swept 20,800 verified
  distinct 88 mask-sets. Information-rate finding: 3,259 harvest shots yield only **47
  distinct sub-problems (0.17/circuit)** versus a diverse lane's 3.9/circuit — a
  **23× difference in information per solve.** The import itself is the durable part:
  the pattern class contains **32/32 targets and 100 % of the gates of all ten
  reference circuits**, with coverage monotone in circuit quality (V88 99.10 %, V89
  92.05 %, V90 85.99 %, Vall 78.73 %).
- **Code:** `campaign_87/wave6_2026-08-11/pattern_class/{cwlib,cwpair,cwfloor}.py`.
- **Generality:** MC-HARDCODED.
- **Phase-2:** keeper — but the class **implies** ≤3 bit-planes, so L37's plane-cage
  finding applies to every negative it produced.

### F20 · union-subset and PB covering SAT (A2)
- **Family:** SAT / pseudo-Boolean, radius-unbounded.
- **What it does:** Instead of bounding the radius around one circuit, bounds the
  *universe*: "is there a realizable ≤87-mask subset of the union of these known
  circuits' masks?" A YES anywhere in the pool is an 87.
- **Twist:** the only exact question in the campaign that is not local to some anchor.
- **Measured:** **427 UNSAT verdicts, 0 SAT**, across CP-SAT, the fast band, and the PB
  escalation. Fast band: **118 pools, 118 UNSAT, max 5.6 s.** The **PB/covering encoder
  is "the single biggest capability gain"** of the lane — it decided in seconds pools a
  pre-registered "pair-density law" had predicted were impossible. That law is itself a
  first-rate methodological negative: it pre-registered, went **6/6 out-of-sample**, and
  was still **an artifact of the CP-SAT encoding, not a fact about the problem** —
  *out-of-sample replication tests the law, not its subject.* Earlier form: union of
  two known 88s = 109–137 masks; all six = 223; `XV190_K87` UNSAT in 13,023 s. The
  depth-3 layer UNSATs come in 1–4 s each; the global instance blew to **35 M clauses
  purely from the cardinality encoding** — size was never the obstacle.
- **Code:** `beat88/methods/m2_oracle/code/{a2_union_sat,a2_pb_union,a2_pb_escalate,a2_fastband,a2_pair_density}.py`.
- **Generality:** **CIRCUIT-GENERIC** — needs only a mask universe and a target set.
- **Phase-2:** **keeper**, and its escalation ladder (pairwise unions → cross-lane core
  ∪ basin vocab → the full 1,979-mask vocabulary) was never climbed to the top.

### F21 · free-closer (one unrestricted mask over all 2³²)
- **Family:** SAT, vocabulary-relaxed by exactly one mask.
- **What it does:** Fixes a region's core and asks the "last step" question with the
  closing gate mask **unrestricted over all 2³²** rather than drawn from a harvested
  alphabet.
- **Twist:** the only instrument that escapes vocabulary conditioning — but it escapes
  it by exactly **one mask**. A roll-up overstated this as "not conditioned on
  harvested vocabulary" and was formally corrected.
- **Measured:** positive control 4/4 (recovers a deleted mask from ~6,350 candidates in
  0.7–2.4 s). Rungs `FC_K87_{A,B,D,E}`, `FCS_K87_SIGMA{5,7}`, `FCR_K87_cls{0,1}` all
  UNSAT at L=13; `FC87_K87_{A,B,D,E}` UNSAT depth-unconditional (L=87) at 472–2,689 s
  each. **Control audit: 23 CONTROLLED, 3 UNCONTROLLED, 2 VACUOUS.** Undecided: region
  C (3 timeouts), class-0-grown, `V88pref240`, the n85 object.
- **Cost:** ≈44 core-hours, ~28 h of it on TIMEOUT/UNKNOWN rows.
- **Code:** `campaign_87/wave5_2026-08-04/burn/simple/execute/{freecloser,audit_controls,summarize}.py`.
- **Phase-2:** keeper — the strongest scoped instrument in wave 5, **provided the scope
  sentence travels with every number.**

### F22 · alphabet-restricted SAT ladder
- **Family:** SAT over a fixed alphabet, rung by rung.
- **Measured:** **self-refuted in its own STATUS.md, in capitals.** The per-region test
  returns K=96 **UNSAT in 0.4 s on a 97-gate region that has a verified 88 nine gates
  below it**; RC2 floors return each region's own count exactly (97→97, 92→92, 90→90,
  88→88). Ledger: SAT 164 / UNSAT 50 / TIMEOUT-UNKNOWN 37 / OPTIMAL 5. Verbatim:
  *"Therefore the nine K=87 UNSATs below are NOT evidence that no 87 exists."*
- **Code:** `campaign_87/wave5_2026-08-04/alphabet_ladder/work/alphabet_ladder.py`.
- **Phase-2:** **dead-end — and the way it died** (a control, run late, that
  invalidated the track's own headline) is the most valuable thing in it.

### F23 · global CP-SAT / min-union set cover
- **Family:** ILP / CP-SAT global bound attempt.
- **What it does:** Harvests a global vocabulary of masks and cones from every run,
  then asks a single global model for a ≤87-gate solution, or for a certified lower
  bound via min-union-of-cones.
- **Measured:** **negative on every axis, and diagnosed.** The 88-gate vocabulary
  saturates at **1,112 masks** (an independent Chao1 estimate predicted exactly 1,112).
  Min-union ILS: 814 restarts, ~43,500 local optima, **23,906 landings at exactly 88,
  zero below**, and all 872 distinct 88s produced were already in the harvest. Global
  CP-SAT ≤87: **UNKNOWN after 11,989 / 17,988 / 17,990 s.** `subset_bound.log` is two
  lines and reports a **certified bound of 2**. The LP relaxation is **provably
  vacuous** (aggregated 0.175, disaggregated ≤ 4.496 by an explicit feasible point).
  **A later audit found the historical CP-SAT UNKNOWNs all ran with
  `lp_iterations: 0`** — only `linearization_level=2` engages the LP, and with it a
  historically-UNKNOWN instance became **INFEASIBLE in 0.5 s.**
- **Code:** `campaign_87/global_vocab/{min_union_cpsat,lp_bound,subset_bound,run_B}.py`.
- **Phase-2:** **dead-end as a bound; keeper as a vocabulary harvester** (`V88.json`,
  `vocab_counts.json`). The `linearization_level` finding is a live re-run lead.

### F24 · cone-vocabulary ILS (set-cover local search)
- **Family:** set-cover local search over a cone library.
- **Measured:** 529 restarts, best 88, cost histogram
  `{88: 15537, 89: 2270, 90: 2529, 91: 3907, 92: 2548, 93: 1578, …}` over a
  92,208-cone library. A completely different search paradigm lands on 88 **6.8× more
  often than on 89**, with a non-monotone dip at 89–90 — independent evidence that 88
  is a genuine attractor.
- **Code:** `campaign_87/global_vocab/{cone_ils,cone_ils88}.py`.
- **Phase-2:** keeper as an *evidence* instrument.

### F25 · vocabulary-restricted ILP `Q(V, n)`
- **Family:** exact solver encoding.
- **What it does:** Asks: is there an `n`-gate circuit using only masks from a fixed
  vocabulary `V`? Encoded as an ILP/CP-SAT model with acyclicity.
- **Measured:** validated in both directions (C2 INFEASIBLE path with 0 conflicts,
  reproducing an independent lane's no-gate-removable result by a second unrelated
  method; C3 FEASIBLE path with an oracle-VALID witness); `Q(V_K1, 87)` INFEASIBLE at
  two desks. **Then a ceiling, not a curve:** a three-point probe at `V = 134` found
  **no recovery at 11× budget** — rounds flat (+11 %) while seconds grew 11.2×. The
  rank encoder was retired by measurement (24.8 M branches, no close at 805).
  **`Q(V*, 87)` — "is there an 87 using only masks some known 88 already uses?" — WAS
  NOT REACHED. IT WAS NOT ANSWERED NEGATIVELY.** `V*` is 1,393; no current encoder
  reaches above ~100–134 masks.
- **Code:** `experiments/e15_campaign3/compose/{n3_ilp,n3_lazy,n3_lazy_ladder,n3_run,n3_run87,ilp_size,completeness}.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper with a named blocker** — *"what is needed is a different
  instrument, not a bigger budget for this one."*

### F26 · cancellation-plan CP-SAT (per-child candidate sets)
- **Family:** constraint programming over cancellation plans.
- **What it does:** Models a cancelling gate as a triple `(child z, overlap O, split
  A)`; each child carries its own candidate overlap list; `y_i ∈ {0,1}` makes
  cancellation **optional**; integer times on a measured `NEEDT` cone let a cancel
  output feed a disjoint gate. One solve decides all `2^n` sub-plans.
- **Twist:** optional cancellation is the structural fix for the failure that voided
  143 prior decisions — the model *contains* the pure cancellation-free solution, so
  plan incoherence cannot exist.
- **Measured:** **the lane's first non-vacuous decision** — `W1w1_orbit1` INFEASIBLE at
  budget 87 in 188 s, exhaustive over its overlap class. 7 configurations run at 87,
  **1 decided, 6 UNKNOWN**. Flagship arm POPUNION synthesised a **verified 88-gate
  depth-5 circuit (66 CF + 22 cancelling)** from a 796-pair vocabulary with the
  child↔overlap assignment FREE — and drove the dual bound only to 46 of 88 in 3,762 s.
  Bound-gain rate **0.02–0.03 gates/second, and it *falls* as the candidate set grows**
  (57 at 122 pairs, 46 at 796).
- **Its predecessor (`tier3`) is a recorded triple failure worth keeping:** the planted
  positive PASSED (21 s) but only because the donor was one of the five circuits the
  vocabulary was built from — **a circular control**; all five real runs at budget 87
  returned UNKNOWN at ~5,944 s. A 143-config sweep was **VOID**: a follow-up re-solve
  found **three of four sampled INFEASIBLE-at-87 configs are provably INFEASIBLE at
  budget 115 — twenty-seven gates above the record.** They were not expensive plans,
  they were *impossible* ones. **Rule earned: a negative from a sampled instance
  requires a positive control on a SAMPLED instance.** A third redesign (4,036,311 CF
  literals) returned UNKNOWN at 1,020 s with its control FAILING: a real plan has 1.05
  children per overlap, so faithfulness needs `p ≈ K`, which is exactly what explodes
  the universe — **"there is no pool size that is both faithful and buildable."**
- **Code:** `experiments/e6_cancelplan/code/{cpk,sweep,popcfg,vocabcfg}.py`;
  predecessor in `beat88/understanding/u7_*` tier3.
- **Incarnations:** `beat88:u7-tier3-plan-substitution` (VOID) → design spec V1-2(b) →
  `experiments_early:per-child-candidate-set CP-SAT plan model` (built, first
  non-vacuous decision).
- **Generality:** MC-HARDCODED formulation.
- **Phase-2:** keeper as a **formulation lesson** (make the hard structure optional so
  the model contains a trivially feasible point); the decision form is superseded — its
  own conclusion is *"stop deciding, start bounding, and not with CP-SAT."*

### F27 · vocabulary-free IN/OUT formulation + pseudo-Boolean optimisation
- **Family:** encoding design + PB cutting planes.
- **What it does:** Partitions signals into `IN` (theorem-named, 1,648 masks by U6's
  Lemma 1) and everything else as **free 32-bit vectors over all 2³²**. The scope of a
  verdict becomes **two integers `(S, E)`**, both functions of `M`, with a *complete*
  limit `(S = 55, E = 87)`.
- **Twist:** the coordinates are not distances to anything known, so it passes the
  blindness test tier3 fails. The complete 87 instance is a **176,474-variable /
  53,762-constraint model that builds in 9 s**, and the `S!`/`E!` symmetry is
  **completely** broken.
- **Measured:**
  * **The tiny-exact ground-truth control — the best control artifact in the
    campaign:** on small random GF(2) matrices, **14/14 exact optima reproduced with
    no vocabulary** (INFEASIBLE at `L−1`, OPTIMAL at `L`, every time). Three of the 14
    are load-bearing: their optimum **cannot** be reached cancellation-free, so the
    free machinery is what finds it. It runs on random matrices by construction, so it
    is **fully CIRCUIT-GENERIC.**
  * Calibration: `S = 0, E = 0` *is* CF synthesis, where I12 says every budget ≤ 91
    must be UNSAT. CP-SAT is INFEASIBLE at 33 (0 s) and 36 (2 s), then **UNKNOWN at
    40, 45, 50, 55 and 60 (> 659 s)** — **the engine is ~53 gates short on the easiest
    slice the instrument has.** Diagnosis: the formulation is correct, complete and
    cheap to build; **CP-SAT is simply a poor infeasibility prover for a
    covering/cardinality problem.**
  * **Pseudo-Boolean (Exact 2.2.1), pre-registered before any run, and it held:**
    budget 60 — where CP-SAT burned 659 s and returned nothing — **falls to cutting
    planes in 1 second.** Positive control at MixColumns scale passes (pinned at 146:
    SAT 0 s; at 145: UNSAT 0 s). **The reusable law: Exact's *optimisation* mode (dual
    bound 88) is far stronger than its own *decision* ladder (stuck between 60 and
    70) — any future PB work should run in optimisation mode, never as a budget
    ladder.** Known limit recorded before it bit: order-encoded acyclicity levels cost
    `O(P·L)` per parent and are **not encodable as written** at MixColumns scale —
    *"this is the wall the 87 rung will hit, and it needs a level-free acyclicity
    argument, not a bigger machine."*
  * **The CF incumbent:** optimisation mode on the `S = E = 0` slice produced an
    oracle-verified **102-gate, depth-5, zero-cancelling-gate circuit**, giving
    **`92 ≤ L_cf(M) ≤ 102` with both ends solid.** Every previously reported upper
    number is superseded (104 was an unextracted incumbent, 103 a `best:` line from a
    log cut off mid-solve, 133 a referee's circuit).
  * **A retracted theorem ladder, recorded in full:** the first `horizon87` S-sweep was
    **wrong** — it swept `S` as a cap, silently excluding circuits with `s < S` needing
    more events. The referee demonstrated it on three small instances. **Nothing was
    banked**; the repaired version pins `S` exactly.
- **Code:** `beat88/understanding/v2_no_vocab/`.
- **Generality:** **CIRCUIT-GENERIC** — `IN` is derived from the target set by theorem.
- **Phase-2:** **keeper — the best-scoped instrument and the best-measured engine work
  in the whole tree.**
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — Generality label wrong.** Labelled `CIRCUIT-GENERIC` on the grounds that "`IN` is derived from the target set by theorem", but the flagship model hardcodes MixColumns: `code/novocab.py:50` `from mixcolumns_core import TARGETS, INPUTS`, `:53` `NOT32 = 0xFFFFFFFF`, `range(32)` at `:59,72,105`; **15 of the 24 files** under `code/` import `mixcolumns_core`. Correct label **MIXED** — the generic part is real but narrow (`tiny.py`/`pbtiny.py` are among the nine that do not import it, which is precisely why the tiny-exact control is fully generic). Every measured number verifies. Minor: "UNKNOWN at 40, 45, 50, 55 and 60 (> 659 s)" — only budget 60 ran 659 s; 40/45/50/55 are recorded at > 264 s.

### F28 · cancellation-free exact synthesis over a *proved* universe (CANC)
- **Family:** representation design + exact CP-SAT synthesis.
- **What it does:** Splits any circuit as `n = |cfcl(S)| + |Dcf(S)|` — the
  cancellation-free closure plus "the masks cancellation cannot avoid" — then minimises
  a cancellation-free family exactly, over a universe **proved complete**.
- **Twist:** two structural facts do all the work and both are proved — (i) **no
  acyclicity encoding is needed**, because parts of a CF gate are strictly smaller
  subsets, so any derivation is well-founded by `|S|`, killing every level/order
  variable; (ii) **the universe is proved** — in a minimal CF family every member is
  contained in some required output, giving exactly **1,648 masks** for the 32 AES
  targets. Model: 1,648 booleans / 12,604 split literals; a weight-w mask has
  `2^{w−1}−1 ≤ 63` splits against the ~4,000–6,500 pairs a general XOR encoding carries.
- **Measured:** **the greedy-108 is cancellation-free (`|Dcf| = 0`); the 88s destroy
  23–33 masks. So the entire 108 → 88 gap *is* the cancellation layer.** Exact
  synthesis reached `CF(M) ≤ 103` with a lower bound of 79 and **was still closing when
  the run was stopped**. End-to-end planted positive: the 88@5-derived plan
  re-synthesised at budget 65 and decoded to `gates=88 depth=5 VALID`. Pre-registered
  dead: **`|Dcf|` as a quality score inverts at the frontier.**
- **Generality:** **CIRCUIT-GENERIC** — the 1,648-mask universe is *derived* from the
  target set by the lemma. (It will be much larger for inv-MixColumns; that is the cost
  question.)
- **Phase-2:** **keeper, and unfinished.**

### F29 · tier-1 CF-layer reoptimization (freeze the plan, minimise the rest)
- **Family:** exact CP-SAT applied to record circuits.
- **What it does:** For each of the five canonical 88 donors, freeze the cancellation
  plan `Z` with the donor's own parent pairs, and **exactly minimise the
  cancellation-free layer over all 2³²**.
- **Measured** (each run < 1 s): 88@5 derived (|Z| = 23, own CF 65) → **65, OPTIMAL**;
  88@5 scratch (27, 61) → **61, OPTIMAL**; 88@6 (30, 58) → **INFEASIBLE at 57**; 88@7
  (27, 61) → **INFEASIBLE at 60**; 88@8 third (33, 55) → **INFEASIBLE at 54**.
  > In all five canonical 88 families the cancellation-free layer is already exactly
  > optimal for its own required-output list, over the whole 2³² mask universe. **An 87
  > cannot come from building better.**
  Strictly sharper than irreducibility. Scope stated plainly: conditional on freezing
  `Z` *and* the donor's exact parent pairs.
  **Companion tier-2 dropscan** (delete one element of `Z`, re-minimise): 88@7 —
  **27/27 attempted, 26 proven necessary, 1 undecided, 0 droppable**; 88@6 — 30/30
  attempted, 19 necessary, **11 undecided (timeout)**, 0 droppable. **The 88s are tight
  in BOTH layers simultaneously.**
- **Phase-2:** **keeper — the single best "why 88" result in the project.**

### F30 · symmetry-quotient SAT (rotation-symmetric circuits)
- **Family:** SAT / symmetry.
- **What it does:** Searches directly for a **rotation-symmetric** circuit by solving
  in the quotient: pick *k* "orbit gates", each costing 4 real XOR gates when
  materialised, and require each of the 8 target orbits to be some rotation of some
  orbit gate. The space is 4× smaller, at the cost of only finding ρ-symmetric circuits
  whose gate count is a multiple of 4.
- **Measured:** **no result on disk** — no solution file exists and no log names it.
  This is an *unfinished* method. Sibling measurements say why it is unpromising: BP's
  symmetric mode costs ~12 gates over asymmetric (B4), and fleet9 found **zero ρ-fixed
  circuits among 54,889 88s**.
- **Code:** `fleet10/cleanroom/work/satquot.py`.
- **Phase-2:** **unfinished; low expected value but genuinely never answered.**
- **COMPLETED (2026-08-29):** this entry was one of the nine Appendix A skeletons. The full schema-conformant entry, written from primary sources by `wrapup/day2/CATALOG_AUDIT.md` §3, is **Appendix A §A·1**.

### F31 · CryptoMiniSat / Gauss-Jordan native XOR (measured worthless here)
- **Family:** SAT scaling attempt.
- **Measured:** an XOR scan of the CNF recovers **6 XORs, all of length 2**, and CMS is
  **1.1×–4.3× slower than kissat** — the GF(2) structure is consumed at encoding time.
  The lever that does exist is RC2 floors (≥40× / ≥19× / ≥15× / ≥11× on 200–216-mask
  alphabets).
- **Phase-2:** **dead-end — do not re-propose native-XOR SAT on this encoding without
  first re-running this measurement.**

---
# Family G — Exhaustive exact searchers, DP and enumeration

Solver-free (or solver-light) exact answers on instances small enough to exhaust.
The recurring lesson: **check whether the target count makes the problem SAT-free
before reaching for a solver** (G8 measured a ~4-orders-of-magnitude speedup).

### G1 · exact small-SLP oracle (`slp_opt.py`)
- **Family:** exact oracle — the most directly portable tool in the tree.
- **What it does:** Takes a JSON instance `{dim, inputs, targets}` and returns the
  exact minimum-length straight-line XOR program, by iterative-deepening SAT (UNSAT at
  k, SAT at k+1).
- **Twist:** three independent solver lineages exist and were cross-checked
  (`sigma_sat.py`, `slp_opt.py`, and a from-scratch bitmask checker `chk.py`).
- **Measured:** self-test **2,406/2,406**. It is the engine under the σ tables (H2),
  every block price in fleet1–12, `output-subset-exact-pricing` (G18), the cube runs
  (F12), and the sector-tightness theorem (H45). Measured limits: it **cannot decide a
  263-input dim-12 instance** (three independent lanes, ~5 h wasted, see H12); a
  generic SAT climb is **not** a route to exact `L2` (50 min on 3 cores did not close
  even k=17).
- **Code:** `atlas/slp_opt.py` (41 KB) + `slp_opt_selftest.py`.
- **Generality:** **CIRCUIT-GENERIC.** Point it at any small linear problem.
- **Phase-2:** **keeper. Reusable as-is for any new circuit's sub-problems.**
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** Two sourcing gaps. The self-test **2,406/2,406** is recorded only in the lane notebook (`atlas/NOTEBOOK.md:400`) with **no run log on disk**, so the count is prose-only. And the "three lineages" twist cites a from-scratch checker **`chk.py` that does not exist anywhere in the repo**. The CIRCUIT-GENERIC label is confirmed by reading the file (no MixColumns constants, no 32-bit assumptions).

### G2 · exact canonical-set DFS (`qsearch`)
- **Family:** exact optimisation, purpose-built C searcher.
- **What it does:** Iterative-deepening DFS over **sets** of gates in canonical
  lex-minimal build order, with an admissible non-counting lower bound and an exact
  end-game. Four ideas, each with its soundness proof in the source header:
  (a) enumerate sets not sequences — buildability is monotone so the greedy closure is
  confluent, giving each buildable set a unique canonical order, removing the `k!`
  orderings; (b) bound `b ≥ max_i(d_(i) + i − 1)` over sorted per-target distances —
  gives 7 at the root against 4 for every counting bound tried, and **two tempting
  stronger forms are false and are documented as such**; (c) exact end-game — when
  remaining budget equals unbuilt targets, every remaining gate must *be* a target,
  decided exactly by greedy; (d) `dist[]` maintained in one pass, 256 byte-ops per node
  at dim 8.
- **Measured:** refuted k ≤ 9 in **2.2 s** where the generic SAT oracle needed 1,200 s;
  k=11 refuted at **698,949,645 nodes in 959 s**; k=12 SAT with decoded witness.
  **`cost(ρ-orbit quad) = 12` exactly.** Turned a 14-day estimate into 16 minutes.
- **Controls:** 121/121 agreement with the generic oracle, 300/300 against a
  deliberately prune-free reference searcher, 25/25 planted positives at k=10/11/12,
  2000/2000 independent completeness audit of every prune, and — the one that matters —
  **it demonstrably can see cancellation pay** (strict gains on 48 of 400 random
  instances).
- **Hard wall:** the `dist[]` pass is `2^dim`, so dim 12 is 16× dim 8 per node (the
  dim-12 orbit class is bracketed `[11,18]`, UNDECIDED). Removing that wall (a lazily
  evaluated bound over the ≤20 available masks) is the named next step.
- **Code:** `experiments/e8_quad/code/qsearch.c` + `{instances,refsearch,differential,planted,audit_path,cancelscan}.py`.
- **Generality:** **CIRCUIT-GENERIC for small dim.**
- **Phase-2:** **keeper, top tier.** Ideas (a) and (c) are general and **nothing in
  `pipeline/` or `beat88/` uses them.**

### G3 · dim-10 quad ladder (sharded `qsearch`)
- **Family:** exhaustive SLP search with cube sharding.
- **What it does:** Exhaustively refutes successive gate budgets `k` for two dim-10
  cross-family quads, sharding by depth-3 root cubes so a level is resumable to the cube.
- **Measured:** **`12 ≤ cost ≤ 13` for both quads**, both ends machine-checked.
  k = 8, 9, 10, **11** all `exhaustive: true`. k=11 = **6,043,276,712 nodes (2,726
  CPU-s)** / 5,846,598,421 nodes (2,669 CPU-s). k=12 measured-projected at **~1.92e11
  nodes ≈ 38 CPU-hours per quad**; **276 of 34,080 root cubes (0.81 %) closed and
  banked, no bound claimed.**
- **Cost:** ~2 CPU-hours banked at k=11 plus 0.60 CPU-hours of k=12 cubes.
- **Code:** `experiments/e11_quad10/code/{qsearch_shard2.c,shard,shardcontrol,decide,finalize}.py`.
- **Phase-2:** **keeper.** The only exhaustive-ladder instrument with a measured,
  resumable price at its open level.

### G4 · parallel DFS over derivation DAGs (no CNF at all)
- **Family:** exhaustive branch-and-bound in C.
- **What it does:** Searches directly over derivation DAGs with a lockless shared
  transposition table, root-splitting into tasks with adaptive re-splitting. Relies on
  a monotone-improvability lemma: a SAT at any block **is** the 87, and a full UNSAT
  sweep certifies the whole convex **down-set** of that block.
- **Twist:** it beats the SAT route on exactly the instances SAT cannot do — **40 rows
  where kissat timed out at 90–155 s were decided in 0.1–25 s.**
- **Measured:** validation V1 504 decisions / 145,752 re-splits / **0 mismatches**, V2
  632 decisions 0 mismatches, **398/398 planted controls**, 373/373 agreement with the
  single-threaded ledger. Scaling on B=15: 376.5 s (1 thread) → 33.1 s (16 threads),
  4.31e7 nodes/s. Pruning median log₁₀ −5.03 at n=8 → **−6.90 at n=12**. Two
  corrections it forced: the projected 10⁸ nodes/s/core was never achievable (real
  ~2×10⁶, memory-bound, 69 % TT hits), and the planned distance prune was **unsound**
  and would have manufactured false UNSATs.
- **Results never written into any summary:** **B=16, 7 of 8 anchors UNSAT**
  (fromscratch 2.95e11 nodes, depth5, depth6, depth7 1.22e11, thirdfamily, SIGMA5
  1.39e11, alg2; SIGMA7 hit CAP at 5.82e11 nodes) and **B=17 UNSAT on SIGMA7 (2.05e11
  nodes, 12,678 s) and alg2 (2.33e11 nodes, 14,905 s)**, both with
  `planted_control: "planted ok (17 gates)"`. Independently cross-validated on a second
  machine — three B=18-ladder rungs agree to 3 significant figures.
- **Code:** `campaign_87/wave6_2026-08-11/dfs_par/{par.c,psweep.py,xpar.py}`; single-threaded
  ancestor `campaign_87/wave6_2026-08-11/dfs_spike/dfs.c`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper — the strongest exhaustive engine the project ever built, and
  it was still climbing when the campaign stopped.**
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — one overstated cross-validation claim.** "Independently cross-validated on a second machine — three B=18-ladder rungs **agree to 3 significant figures**." Three rungs on the pod is right; the agreement is to **two** significant figures at best — 7.389e6 vs 7.44e6/7.51e6; 2.1509e8 vs 2.1367e8; and **2.2020e8 vs 2.1367e8, ~3.1 % apart**. The primary claims only that node counts "differ **only by the usual parallel-dedup jitter**"; the "3 significant figures" gloss is this catalog's own addition and is false. Everything else verifies. Attribution caveat: the 40-row kissat comparison, 398/398, 373/373 and the −5.03 → −6.90 pruning medians are **dfs_spike** (the single-threaded ancestor) measurements, presented here under the parallel engine.

### G5 · canonical DFS set enumeration (count sets, not programs)
- **Family:** exhaustive enumeration / structural analysis.
- **What it does:** For a small sub-problem, lists **every distinct set of intermediate
  values** of a given size that can be built from the inputs and covers the targets —
  not every program, every *set*, so two orderings of the same values count once.
  Duplicate-freeness comes from a canonical order (repeatedly take the numerically
  smallest currently-buildable value), giving exactly one search path per set. Prunes
  with the Boyar–Peralta δ bound, a relaxation, so it removes no solution.
- **Measured:** 82/82 record blocks decided; **the record's own block value-set was
  found in every one** ("RECORD BLOCKS NOT REACHABLE: []"). Passed five controls
  including exhaustive agreement with an unpruned brute-force enumerator on 60 random
  instances (179 sets) and with an independent layered-BFS enumerator on 40 instances
  (778 sets), **identical *sets*, not merely identical counts**.
- **Cost:** 5,943 s for one results file; 130,806 s wall (36.3 h) for the larger one.
- **Code:** `fleet9/laneENUM/code/enumlib.py` + drivers + `validate.py`, `validate2.py`.
- **Generality:** **CIRCUIT-GENERIC** at the instance level.
- **Phase-2:** **keeper.** It turns "the optimum is 8" into "the optimum is 8 and there
  is exactly one way to reach it".

### G6 · program census (enumerate every optimum, then read off what it consumes)
- **Family:** complete enumeration of optima.
- **What it does:** Enumerates **every** `k`-gate program of an instance, then for each
  surviving value set enumerates every build order and every operand choice and reads
  off which interface values it consumes.
- **Measured:** census6 — 4.8 M states in **68 s** → 4 distinct extra-pairs →
  **exactly TWO optimal committed sets**, both tap-diagonal bases: `{4,6,a}` (= record
  88@7's own set) and `{4,6,e}` (= an independent lane's derived set). *There are
  exactly two optima and the two lanes found one each* — which retires a "witness luck"
  caveat in both directions and answers the open necessity question: at the optimum a
  `vT` basis is **necessary**, not merely sufficient. census7 — **21,872 seven-gate
  programs**, complete, banked — and it produced a real **negative about a cheap
  route**: the value union covers **243 of 243** admissible values, so the filter
  "`Q1 ⊆ U`" is vacuous.
- **Cost:** 68 s + 3 × ~1,415 s.
- **Code:** `fleet3/laneCB_completeness/code/{census6,census7}.py`.
- **Phase-2:** **keeper.** Enumerating *all* optima, not one, is what turned an ansatz
  into a derivation.

### G7 · minE exhaustion by orderly generation
- **Family:** certificate over a combinatorial characterisation.
- **What it does:** A minimal circuit and a minimal *realizable mask set* containing the
  targets are the same object (dedup and stripping weight-<2 masks never grow a set), so
  **`L = #targets + minE` exactly** for the right instances. Exhausting the "extra
  masks" search to depth `k` then proves `L ≥ #targets + 1 + k`. Two prunings, each with
  a proof: P1 (last-level candidates must close a target) and P2 (orderly generation —
  skip `c < prev` if `c` was already a candidate).
- **Measured:** `L2` bracket **`[17,26] → [22,26]`**. Depth 5 exhausted **three times**:
  pruned (294,188,302 nodes), **pruning-free (80,092,627,410 nodes, 8/8 shards NONE,
  4 h 26 m)**, and by an independent from-scratch implementation (1,795,955,245 nodes).
  The two *unpruned* trees are node-for-node identical (425,649,382 vs 425,649,383 at
  k=4 — a root-counting offset). Nodes ×~50 per level.
- **Code:** `fleet1/laneC_proofside/code/{mine2.c,l2_build.py,validate.py}`; independent
  implementation in `verify1/`.
- **Generality:** **CIRCUIT-GENERIC** — the `L = n + minE` identity needs only "targets
  distinct, weight ≥ 2, none an input, inputs a basis".
- **Phase-2:** **keeper.** But note the strategic caveat: **every bound from a tower
  rung is capped at 51 (level 3) or 26 (level 2), both below the refereed 56** — so
  exact `L2`/`L3` cannot improve `L(M)` at all. Use it for calibration, never as a bound
  route.

### G8 · greedy-schedule lemma enumeration (SAT-free exact engines)
- **Family:** exact combinatorial search without a solver.
- **What it does:** Proves that a valid program can always be reordered as "build every
  currently-buildable target, then introduce the next extra", so a `k`-gate program with
  `t` targets has exactly `k − t` extras and the search is over that many values. With 4
  targets, deciding `k = 5` is a search over **one** value.
- **Measured:** three independent engines, all exhaustive, all agreeing:
  `min_gates_naive` (**0.16 s**), `AmbientFast` (**0.03 s / 20 s**), and the **relaxed
  sweep** which iterates the *whole 4096-value 12-bit space* handing each value over
  free — proving the strictly stronger "there is no value at all, buildable or not" — in
  **0.39 s**. This is where a SAT solver had burned **4 h + 66 min + 240 s across three
  lanes and produced nothing.**
- **Controls:** CTRL-A (reproduces two other lanes' oracle value 6), CTRL-B (UNSAT at 5
  as their solver logged), CTRL-C (empty supply UNSAT at 6), **CTRL-D planted positive,
  shape-matched** — the ambient instance plus one free value taken from the interior of
  a real 6-gate program returns **5** on both engines.
- **Code:** `fleet3/laneCB_completeness/code/{enum_exact,check_relaxed,decide}.py`.
- **Generality:** CIRCUIT-GENERIC for small-target-count blocks.
- **Phase-2:** **keeper — check whether the target count makes the problem SAT-free
  before reaching for a solver.** Speedup here was ~4 orders of magnitude.

### G9 · exhaustive currency-vs-depth curve (BFS, no solver)
- **Family:** complete enumeration.
- **What it does:** Breadth-first enumeration over a line's value space giving the exact
  gates-vs-depth curve for a set of single-line "currency" values — so `None` means
  **provably impossible**, not "not found", and a value's arrival level is *chosen*, not
  discovered.
- **Measured:** over all 19 cells on record, **every cell's whole currency is buildable
  at depth 2 for 0–2 gates over the gate-minimum, and depth 1 is infeasible at every
  cell.** At the 88@7 cell: 22 gates at depth ≥ 3, 23 at depth 2 — forcing all currency
  to level ≤ 2 costs exactly one gate. So supply chains are nearly free and were never
  the depth problem. Guarded by `CurrencyUndecided` — a `kmax` truncation is exit 5,
  never "impossible".
- **Code:** `fleet4/laneDEPTH/code/currency.py`; `fleet8/unified/code/algebra.py:t_min_gates`.
- **Generality:** CIRCUIT-GENERIC. **Phase-2:** keeper.

### G10 · free-gate-reduction exact re-add
- **Family:** exact optimisation — the reduction that makes a dim-32 question
  exhaustible.
- **What it does:** The dropped targets are absent from the available set `A`, so **each
  of them must BE a gate**; a `k`-gate completion is `G = T ⊎ F` with only `|F| = k − 4`
  free gates. Build order never has to be searched because reachability from `A` is a
  **confluent closure**.
- **Twist:** it converts "synthesise 4 outputs at dim 32" (impossible for `slp_opt.py`,
  whose delta table is 4 GB at dim 32) into "find at most 5 extra masks".
- **Measured:** **exact minimum re-add cost = 10** for the open 87 question (9 would
  have been 87). Across **41 decided instances** — all 8 ρ-orbits of all five verified
  88s, plus the relaxed sets — `exact_readd = 88 − |remaining|` in **41 of 41**, total
  88 every time, never 87 and never 89.
- **Cost:** ~4 s at k=6, ~400 s at k=8, 3,980 solver-seconds for the k=9 cube run.
- **Code:** `experiments/e5_readd/code/{kern,satx,dfs,cube,mkinst,runner}.py`.
- **Generality:** **CIRCUIT-GENERIC.** The reduction only needs "the dropped targets are
  absent from `A`", which holds for any circuit and any target subset.
- **Phase-2:** **keeper, top tier — the most transferable exact technique** in the
  experiments slice.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** Scope overstatement in "all 8 ρ-orbits of all five verified 88s, **plus the relaxed sets**": 5 × 8 = 40, and only **one** relaxed set is inside the 41 (byte-identical to `88d5_orb3_sub`). The other three relaxed sets are explicitly *not* pinned (§7: `[10,16]`, `[9,15]`, `[9,13]`, witness searches timed out at 5,141 s) and one of them has total **≥ 89**, not 88. The CIRCUIT-GENERIC label is defensible — `satx.py:36` takes `dim=DIM` as a parameter; only the harness `kern.py:11-22` is MixColumns-bound.

### G11 · forcedness enumeration (`forced.c`)
- **Family:** exhaustive counting of optimal families at miniature scale.
- **What it does:** Exhaustive DFS with an admissible lower bound and **exact structural
  canonicalisation** (one representative per DAG, lex-min linear extension) that counts
  how many structurally distinct optimal programs an instance has at `L*`, `L*+1`,
  `L*+2`, with irredundance enforced. It answers a *methodological* question — "does the
  existence of several distinct 88s tell us 88 is not optimal?" — rather than searching.
- **Measured:** **99 certified-optimal instances** (n = 4..7, `L*` = 3..11). Families at
  the true optimum: min 1, **median 10**, mean 121, max 2,813; only **22/99 = 22 %** of
  true optima are unique; **65 %** admit ≥ 5 families, rising to **79 %** among `L* ≥ 8`.
  Forcedness collapses with hardness: `log10(families) = 0.324·L* − 1.09`, i.e. **×2.11
  families per extra optimal gate**, Spearman ρ = 0.60. No cliff at the optimum (×33
  from `L*` to `L*+1` vs ×20 from `L*+1` to `L*+2`). **Circulant miniatures — the
  MixColumns analogue — are the least forced of all: median 309 families, zero unique.**
  Verdict: "a true optimum should be forced" is **refuted** in this problem class; five
  distinct 88s discriminate nothing.
- **Controls:** hand-computable n=3 case exact; an independently written brute-force
  enumerator agrees on **40/40 comparisons** across 9 instances and every level.
- **Cost:** 1 core, `nice -n 15`; ~25 min per dense n=6 instance. Scale-limited to n ≤ 7.
- **Code:** `experiments/e16_lastwish/laneFORCED/{forced.c,runner,n7probe,growth,bruteforce_check,analyse}.py`.
- **Generality:** **CIRCUIT-GENERIC and instance-generic.**
- **Phase-2:** **keeper** — it settles a recurring interpretive question cheaply, and the
  same code answers it for any new circuit family.

### G12 · quotient tower (solve mod `v^k`)
- **Family:** structural analysis + exact search on genuinely smaller problems.
- **What it does:** Solves MixColumns modulo `v^k` — a smaller standalone circuit
  problem at each rung — with Boyar–Peralta using an **exact** subset-sum distance table
  (full BFS over the whole quotient space).
- **Measured:** `L2 ≤ 26`, `L3 ≤ 51` — **16 below** the earlier 67. Lower bounds
  `L2 ≥ 17`, `L3 ≥ 33`. Tower `0 → 26 → 51 → 88`, steps **26, 25, 37** — so **the socle
  rung is the expensive one**, inverting the earlier reading. Search-free constructions
  verified at 27 and 54. Measured verdict: **a generic SAT climb is not a route to exact
  L2.**
- **Code:** `atlas/tower/{quotient,extract,structure,lb,lift,analyze,verify_all}.py`,
  `bp.c`, `bp2.c`.
- **Generality:** **CIRCUIT-GENERIC** for any linear circuit over a filtered ring;
  BP-with-exact-distance-table is generic outright.
- **Phase-2:** keeper.

### G13 · exhaustive wiring enumeration (rigidity)
- **Family:** exhaustive structural census.
- **What it does:** Enumerates the *entire* wiring space of a mask set (an SLP is a mask
  set **plus** a parent-pair choice) and computes the exact minimum of a structural
  quantity over all valid wirings.
- **Measured:** over 10 named circuits, the exact minimum equals the shipped value on
  **10/10**, from code sharing nothing with the lane's. **Four of the five record 88s
  have a UNIQUE valid wiring** (88@8 has 4; 92@4 has 64; 97@3 has 16). Census re-run
  over **3,254 known 88s**: minimum budget 78 against a requirement of 4, 0 violations;
  **2,509 with a unique valid wiring, 745 with more than one.**
- **Code:** `fleet2/laneP_proof/verify1/rigidity.py`.
- **Phase-2:** **keeper.** Uniqueness of wiring is what makes per-circuit structural
  claims about a *mask set* legitimate.

### G14 · heavy-corner exhaustive library
- **Family:** linear projection + complete BFS.
- **What it does:** Projects onto the four weight-11 columns {7,15,23,31} — the GF(2⁸)
  reduction bits. π is linear, so a gate's heavy class is the XOR of its parents': **the
  heavy world of *any* circuit is an SLP over a 16-element universe**, small enough to
  exhaust.
- **Measured:** exact cost-to-go over **all 1,857 reachable states**; **all 1,857 can
  still finish — the heavy corner never traps a constructor, it only prices one.**
  **4,510** plans at `c = 8` and **336,484** at `c = 9` fully enumerated. Cost law:
  heavy gates ≥ 19 + c. Census over 204 families: heavy gates 43–51 (mean 47.6) against
  a floor of 27; classes realised `c ∈ {9: 11, 10: 89, 11: 104}` — **never 8** — and
  **not one of the 4,510 `c=8` plans is used by any known 88** (nor by 1,200 further
  sampled 88s: `c ≥ 9` in **1,404/1,404**).
  **The load-bearing negative:** the `c = 8` region is not unexplored — **the archived
  97-gate depth-3 ladder lives there.** Across 97 → 92 → 89 → 88 the heavy corner
  *grows* 38 → 42 → 46 → 47.6 while light shrinks 59 → 50 → 43 → 40.2. **A constructor
  that minimises heavy activity walks toward the 97, not toward an 87.**
- **Artifact:** `beat88/understanding/u5_heavycorner/heavy_corner_library.json` (1.3 MB)
  — self-contained, a function of the AES matrix alone.
- **Generality:** MC-HARDCODED constants, CIRCUIT-GENERIC technique. For
  `aes_inv_mixcolumns` the analogue is "project onto the anomalously heavy columns" —
  but the inverse matrix's column weights are uniformly dense, so the projection would
  be larger and probably less useful. **That is the main porting question.**
- **⚠** This lane has **no PROOFCHECK.md**, so its results are not in the project's canon.
- **Phase-2:** keeper.

### G15 · cross-family subset pricing (`gaphunt`)
- **Family:** exact-subset pricing / exhaustive SLP search.
- **What it does:** For a subset `S` of output rows, computes the exact
  cancellation-free cost `cost_cf(S)` by MILP (constructive, so a machine-checked upper
  bound), then runs an exhaustive unrestricted XOR-SLP search at the single budget
  `k = cost_cf − 1`. UNSAT-exhaustive decides `gap = 0`; SAT exhibits a strict
  cancellation gain; an aborted budget is recorded as a bracket and never as a bound.
- **Twist:** spends the whole budget on the one hardest level instead of climbing a
  ladder — sound because a gap is cheap to find (first-solution DFS) and only its
  absence is expensive.
- **Measured:** `cost(S) = cost_cf(S)` on **54 of 54** subsets decided, 9 of them
  cross-family, **zero gaps**. Cross-family decided classes: n=2 at dim 8/9/10, n=3 at
  dim 9/10. 6 subsets left UNDECIDED as brackets. Escalation runs of 293–308 s closed
  two dim-10 n=3 classes at ~1.4e8 nodes each.
- **Code:** `experiments/e10_crossfam/code/{gaphunt,xrun,escalate,enum}.py` + `qsearch.c`.
- **Phase-2:** **keeper as an instrument, dead end as a programme** — the question is
  identically empty below 4 targets.

### G16 · search-free gap hunt (planted-program screen)
- **Family:** one-sided existence screen.
- **What it does:** Plants verified `s`-gate programs whose outputs are four weight-5
  targets at the real shape, computes `cost_cf` exactly by MILP, and certifies a strict
  cancellation gap wherever `cost_cf > s` — **no search at all**.
- **Twist:** finds gaps without any exhaustive refutation; it can never rule one out.
- **Measured:** 150 planted 12-gate programs (`cost_cf` histogram
  `{9:18, 10:77, 11:51, 12:4}`) and 600 with ≥2 cancelling target gates — **0 of 750
  with `cost_cf ≥ 13`**, i.e. a 12-vs-13 gap at the real quads' level is rare enough not
  to appear in 750 directed plants. Uniform planting produces the shape **0 of 4,000**
  times, which is why the planter directs its last 4 gates.
- **Code:** `experiments/e11_quad10/code/{hunt13,plantgap,planted10}.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper** — cheap directed evidence where exhaustion is unaffordable,
  provided the one-sidedness is stated.

### G17 · cancellation-free MILP
- **Family:** exact optimisation, restricted question.
- **What it does:** In a cancellation-free program masks add disjointly up the DAG, so
  candidate gates are exactly the size-≥2 subsets of the targets and minimising the built
  set is an exact integer program (scipy/HiGHS).
- **Twist:** it answers a *restricted* question exactly, so it is a cross-check rather
  than a substitute — and it is the only instrument in its lane that reaches dim 12–13
  blocks at all.
- **Measured:** agrees with the true optimum **90/90** where both are known; **0**
  instances where cancellation strictly helps; 145/145 witnesses round-trip verified.
- **Cost:** 900 s hard cap, hit on both dim-12 weight-7 family reps.
- **Code:** `experiments/e2_outputcost/code/{cfopt,cf_batch,cf_report}.py`.
- **Generality:** **CIRCUIT-GENERIC.**
- **Phase-2:** **keeper** — cheap upper bound plus a strong independent cross-check on
  any SAT result.

### G18 · output-subset exact pricing (with a round-trip lift)
- **Family:** exact optimisation.
- **What it does:** For a subset `S` of output rows, restricts to the support union of
  `S`, remaps to a low-dimensional instance, and gets the exact minimal SLP length from
  G1; every returned program is lifted back to 32 bits and re-evaluated.
- **Twist:** the round-trip lift is what makes the dimensional restriction safe rather
  than assumed.
- **Measured:** `U(1) = 152` exact (32/32 rows, each `w−1`); `U(2) = 114`; **127/127
  round-trips passed; 127/127 `exhaustive`; 15/15 planted positives.**
- **Cost:** 87 oracle decisions plus timeouts up to 5,489 s each.
- **Code:** `experiments/e2_outputcost/code/{runner,common,construct,report}.py`.
- **Generality:** **CIRCUIT-GENERIC** given a target matrix.
- **Phase-2:** **keeper, top tier** — how to get a defensible cost curve for a *new*
  matrix cheaply.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — a conditional bound presented as exact.** This entry writes "`U(1) = 152` exact …; **`U(2) = 114`**" as parallel exact facts. The primary says the opposite: *"`U(2) <= 114` is certain, and `U(2) = 114` holds **unless** one of those 7 classes beats its cancellation-free value"* (`RESULT.md:266-267`), and 222 of the 496 pairs carry only a cancellation-free upper-bound cost, not an oracle cost. Write `U(2) ≤ 114`, exact only under the stated law. Second: "Cost: **87 oracle decisions**" is a stale earlier tally — the coverage table gives 89 for pairs and **127** oracle decisions overall, which is what the 127/127 controls count. Third: "timeouts up to 5,489 s **each**" misdescribes four distinct timeouts (1201 / 5328 / 5489 / 2400 s). `U(1) = 152`, 127/127 round-trips and 15/15 planted positives are exact.

### G19 · Venn isomorphism class reduction
- **Family:** combinatorial reduction (pure, no solver).
- **What it does:** Two output-subsets are isomorphic instances iff a bijection of the
  support union matches all Venn-region sizes; one oracle run then decides the whole
  class, with an explicit machine-verified bit-permutation certificate.
- **Measured:** **496 pairs → 13 classes; 4,960 triples → 121; 35,960 quads → 1,264; the
  8 ρ-orbits → 2 classes.** 319 propagation rows, **0 certificate failures.** It turned
  "finish all 496 pairs" from 410 runs into **8**.
- **Cost:** negligible.
- **Code:** `experiments/e2_outputcost/code/{classes,cones,propagate}.py`.
- **Generality:** **CIRCUIT-GENERIC — the highest-leverage reusable trick in its slice.**
- **Phase-2:** **keeper, top tier.** Run it first on any new matrix; it prices the whole
  exact-subset programme before a single solver call.

---

# Family H — Class-pricing, block decomposition and generators

The largest family: 51 entries. This is the "derive the circuit's price from the
algebra instead of searching for it" programme. It produced a generator that emits
a verified 88 from theory, and it is where the phase-2 crown jewel lives (H26).

### H1 · ring / ladder frame
- **Family:** structural frame — everything in this family sits inside it.
- **What it does:** Rewrites the 32×32 GF(2) problem as arithmetic in
  `R = F256[v]/(v⁴)`. Input bits and output rows both become units of a rank-1 R-module
  under the trace pairing; the whole matrix is one formula
  `M_T = (1+v+v²)(y·I8 + v·Xᵀ)`. The 32-dim problem splits into 8 coupled 8-dim "sector"
  problems (one per bit position) that are all **the same** problem, glued in a ladder,
  with four "taps" coupling sectors to a hub.
- **Twist:** unlike every earlier representation it is *graded* by the nilpotent
  `v = y+1`, so it explains rather than describes.
- **Measured:** decomposition verified constructively; all 8 sectors carry the same 4
  targets; `assemble.py` compiles abstract sector programs into real mask circuits
  (naive scheme → 116 gates, VALID). Re-derived from scratch by an adversarial auditor
  with zero shared code: **duality 3000/3000 pairings, z-iso 1000/1000, all 32
  `c·z(bit_i) == z(row_i)`, tensor rank of c = 2, socle identity 8/8, zero convention
  slips.**
- **Code:** `atlas/{ring,sectors,lines,sector_view,anatomy,valuation,economy,assemble}.py`.
- **Generality:** MC-HARDCODED in constants, **CIRCUIT-GENERIC in method** for any
  circuit that is multiplication by a fixed element of a local ring — **inverse
  MixColumns is exactly that: same R, different `c = 14+11v+13v²+9v³`.** Porting =
  recompute `c`, the dual basis, and the tap set; everything downstream is parameterised.
- **Phase-2:** **keeper — the single most reusable asset in the atlas slice.**

### H2 · exact sector oracle (σ tables)
- **Family:** exact-oracle deployment at table scale.
- **What it does:** Solves the 8-dimensional sector problem exactly — minimum XOR gates
  to reach 4 fixed targets from a raw set plus a purchased "currency menu" `(P,Q)` — and
  banks the whole table.
- **Measured:** `m1_results` **5,623 instances, 3,124 exact + 2,499 infeasible, zero
  timeouts**; `m1_wide_results` 8,313 (26 timeouts); `m1_v15_results` 34,112 (6
  timeouts). Value histogram `{7:222, 8:1475, 9:1049, 10:329, 11:44, 12:5}`. Floor law
  `σ_floor(|P|,|Q|) = 12 − min(|P|,3) − h(|Q|)`, verified 33/35 cells.
  **σ(0,0) = 12 exact** (k=11 UNSAT cost 4,236 s single-lineage, later closed
  multi-lineage by a 28-way cube split, 28/28 UNSAT). **σ_tap ≡ σ_clean on all 466
  shared (P,Q)** — the "tap premium" is entirely dcost + span. Integrity: 604/604
  witnesses re-replayed shared-nothing; 1,002/1,002 infeasibility verdicts re-derived by
  independent rank test; 12,637 monotonicity extensions, 0 violations.
- **Code:** `atlas/sigma_sat.py`, `atlas/slp_opt.py`, `m1_search.py::gen()`.
  **Logs:** `m1_results/`, `m1_wide_results/`, `m1_v15_results/` → `m1_sigma.json`
  (13,153 rows).
- **Phase-2:** **keeper. Reusable as-is for any new circuit's sector subproblems.**

### H3 · M1 chain DP (price an architecture class exactly, then compile the winner)
- **Family:** class-pricing / DP.
- **What it does:** Prices the whole line-disciplined ("M1") architecture class exactly:
  choose a currency menu per column, pay `Σ_k σ(P_k,Q_k)` from the oracle table plus the
  supply bill, minimise over all menu assignments by a chain DP. Runs in `optimist`
  (missing entries priced maximally favourably) and `pessimist`/`exact` modes to bracket.
- **Twist:** the cost function is *exact table lookup*, not a heuristic — so the optimum
  is a real class optimum, and it **compiles**: `compile_config.py` turns the winning
  config into a verifiable circuit.
- **Measured:** bracket `[75,92]` → `[85,92]` → **exactly 91** on the complete table.
  Compiled witness `compiled_m1.json` = **91 gates, VALID**; `compiled_all7.json` = **91
  gates, VALID, depth 5, ZERO glue**. Records are 88, so **the records' out-of-class
  mechanism is worth exactly 3 gates.** Re-priced **six** times (shared constituents,
  junctions at real cost, free tap-1 passengers, σ⁺-exact free sets, width-uncapped,
  V1.5 vocabulary) and returned 91 every time.
- **Code:** `atlas/{m1_search,m1_search_v2,m1_search_wide,m1_batch,compile_config,compile_config_v2}.py`.
- **Generality:** MIXED. The DP + table lookup + compile-and-verify pipeline is generic.
- **Phase-2:** **keeper — the template for "price an architecture class exactly and
  compile the winner".** ⚠ 91 is an **upper bound + witness** for the class, not yet a
  floor.

### H4 · V1.5 exotic-currency DP
- **Family:** class-pricing (twist on H3).
- **Twist:** adds *exotic* column currency — triples, units, and the socle `v³` — that
  M1 forbids, priced at true build cost via exhaustive BFS over the 4-dim currency space
  (487 menus per column).
- **Measured:** **class optimum still exactly 91.** The mechanism is real
  (**σ = 6 exists, first ever measured**: `σ(clean; P={6,7,8,a}, Q={2,a,c}) = 6`, k=5
  UNSAT / k=6 SAT, witness verified) but **wash-priced**: the "q-face tax" makes the
  neighbouring sector pay exactly +1, on all six decider rows. σ = 6 requires width-4
  p-menus with ≥2 exotic levels: 45/54 such classes give 6; **0/26** width-3 perfect
  chains and **0/43** width-4 1-exotic ever do; and **no σ = 5 has appeared anywhere in
  2,600+ exact V1.5 entries.** First verified socle-currency circuit: 91 gates, VALID.
- **Cost:** 236,088-instance corpus on 28 pod workers; only 34,112 landed.
- **Phase-2:** keeper as a *pricing pattern* ("give the model the vocabulary the records
  actually use, then see if it still can't reach them").

### H5 · shape-law mining (`pred7`)
- **Family:** oracle-table data mining.
- **What it does:** Treats the complete exact table as a dataset and derives a
  **closed-form 3-rule predicate** deciding `σ = 7`, then uses the predicate to extend
  the DP past the table's coverage.
- **Measured:** **pred7 has 0 errors on all 3,124 feasible entries** and agrees with an
  independent constructive search on all 4,096 `(P,Q)` pairs. The `σ=7` up-set has
  exactly **24 minimal patterns = 7 rotation classes**, all `(3,3)`. Mechanism census of
  all 222 optimal 7-gate witnesses: **antipodal target pairing is impossible 0/222;
  cyclic-adjacent pairing finds all 222.** And the reason for 91:
  **`91 = 8×7 + 24 + 9 + 2`**, the `+2` a **misalignment tax from a fixed-point-free
  4-cycle of menus**.
- **Generality:** **CIRCUIT-GENERIC technique** — "mine your exact oracle for a
  closed-form predicate, then price beyond the table with it."
- **Phase-2:** **keeper — the highest leverage-per-CPU method in the atlas slice.**

### H6 · junction capacity sweep
- **Family:** exact-oracle probe (twist on H2).
- **What it does:** Asks whether a sector program can emit a "junction" (`3d_k·t`) for
  free, in two dual forms: hand it in as a *free input* and ask for `σ−1`/`σ−2`, or add
  it as an *extra target* and ask for `σ`. Monotonicity lets one call decide 21 pairs.
- **Measured:** **capacity is exactly 1, proven** — over all 222 σ=7 classes, 0 admit two
  free junctions; 1,332 asks, **1,313 UNSAT, 78 SAT, 0 unresolved.** Capacity-**2** does
  exist off the floor (12 instances in the σ=8 stratum, all tap, all `(|P|,|Q|)=(4,4)`),
  refuting an earlier "capacity ≤ 1" law; capacity 3 is 0/13. The double-diagonal
  junction routing **works and saves exactly 1 gate** (94-gate VALID vs 95-gate VALID) —
  but the flat basin re-absorbs it and the junction-enabled DP is still 91.
- **Code:** `atlas/thinktank/{capacity_sweep,junction_dp2,junction_assemble}.py`,
  `atlas/sigma_plus_sweep.py`; bank `atlas/spbank/*.jsonl` (11,248 records).
- **Generality:** **CIRCUIT-GENERIC probe shape** — "add candidates as free inputs vs as
  extra targets, batch by monotonicity" is reusable anywhere.
- **Phase-2:** keeper (the probe); the specific junction question is settled.

### H7 · free-junction relaxation bound (decide whether a sweep is worth running)
- **Family:** class-pricing, deliberate over-relaxation.
- **What it does:** Instead of running 1,332 exact asks, *assume the answer is yes
  everywhere* subject only to capacity 1, and see what the DP can then reach. If the
  bound is ≥ 91, no sweep outcome can change the verdict.
- **Measured:** MODE=none → **91** (complete). MODE=tap1 → **89** (complete).
  MODE=junction → best 90, **run truncated, no optimum line.** So the shortcut did
  **not** discharge the sweep. The cheap exact follow-up pinned MODE=tap1 back at **91**;
  MODE=both **stopped at 800 of 3,249 frames**, best 91.
- **Cost:** seconds–minutes (the whole point).
- **Code:** `atlas/{free_junction_bound,exact_free_targeted}.py`, `run_ef.sh`.
- **Generality:** CIRCUIT-GENERIC pattern.
- **Phase-2:** keeper as a pattern; the specific run is **unfinished**.

### H8 · transposed chain DP / split-q / sigma-aug / lazy-oracle loop
- **Family:** class-pricing — four escalating twists on H3, all closed.
- **Measured, in order:** transposed V1 optimum **92** (optimist also 92; forward control
  reproduces 91 on the same code path). Split-q sector-7 oracle: `σ_split ≥ 9` everywhere
  machine-proven, `K = 80` exact ⇒ model optimum in `[89,92]`. `σ_aug` (supply
  obligations folded in as extra targets, removing a double-count): drops to **83** —
  *excludes nothing and exhibits nothing*. Lazy oracle loop: diagnosed
  **non-convergent** (surrogate slack is uniform, not concentrated; plateau at 83); the
  sole rescue (additive premium ≥ 4) refuted by an exact counterexample (measured gap
  +2); additive ceiling 85.
- **Code:** `atlas/thinktank/transposed/{transposed_dp,splitq,splitq_dp,aug,aug_dp,lazy_dp}.py`.
- **Generality:** MIXED. The **"add the supply elements as extra targets to remove
  double-counting"** trick and the lazy-oracle loop are fully general.
- **Phase-2:** **dead-end, and explicitly declared settled** — a model built to host the
  records' own routing still does not price an 88. Valuable precisely because it is a
  *closed* lane.

### H9 · v2 region pricing (the fleet-1 backbone)
- **Family:** class-pricing / exact block decomposition.
- **What it does:** Changes coordinates so a 32-bit mask becomes 8 nibbles on "lines";
  partitions a circuit's gates by the line support of each gate's *value* into ~10 blocks
  (currency per line, plus region blocks); prices each block by an exact minimum-gates
  decision given a committed interface. The sum is a true lower bound for any circuit in
  the class realizing that configuration.
- **Twist:** the first model that contains the records' *joint* region economy — currency,
  sector work, tap supply and hosting priced **together** (folded `W07`/`W3` blocks).
- **Measured:** all 14 known 88s decompose with zero residue and price at **exactly 88**;
  89@5/89@10 → 89; two compiled M1-optima → 91. **~50 exact block decisions, 18 heavy
  probes + full control tier, ALL TIGHT** — every decision the solver finished returned
  exactly the record's own block size; zero sub-witness blocks in the whole campaign.
  In-cell R01 core values exactly constant across records (18,18,18,19,19,19); R34 core
  (22×10, 23×4).
- **Cost:** `ledger.jsonl` 667 rows, 26 `exact`, 9 `crash_or_timeout`; overnight campaigns
  across 2 days on 6 cores. Undecided brackets: `U3` at nb=11–13 (2–8 h timeouts each).
- **Code:** `fleet1/laneA_v2pricing/code/{v2lib,decompose,subblocks,extract_configs,price,control,probes}.py`.
- **Generality:** MC-HARDCODED in its coordinates (trace-dual basis and tap ladder come
  from the AES field), CIRCUIT-GENERIC in method. For `aes_inv_mixcolumns` the ladder
  `2·d_k = d_{k-1} + τ_k d_7` re-derives mechanically from the same reduction polynomial;
  the block list and the sector target `(p_j,q_j)` must be recomputed.
- **Phase-2:** **keeper — the backbone.** Every downstream lane (G, CB, F4, DEPTH, and
  fleet5/8/9/12) reads its `configs.json`.

### H10 · joint-block probe (folded blocks)
- **Family:** class-pricing, twist on H9.
- **What it does:** Instead of pricing two blocks separately, folds them into one and asks
  the exact oracle for the joint minimum, so the solver may spend a gate that serves two
  roles — which a per-block model structurally cannot see.
- **Measured:** **18 folded probes, 18 tight.** Mechanism read off an optimal witness
  (88@5fs `U07`, exact 8): **7 of its 8 gates ARE instance targets** — the supply exported
  downstream *is* the sector work.
- **Cost:** minutes to 8 h per probe.
- **Phase-2:** **keeper** — the cheapest way to detect that a decomposition is losing
  gates at a seam.

### H11 · singleton committed-value exhaustion (`g01`)
- **Family:** exhaustive committed-value sweep.
- **What it does:** For a fixed cell, asks for every single candidate interface value `w`
  whether committing it lets the downstream block come in under the record, each an exact
  capped UNSAT.
- **Measured:** **240/240 candidate values individually useless, 0 timeouts** (504 ledger
  rows / 480 `useless` across two arms). Hence `G01 = 18` against every `|Q'| = 1`
  configuration.
- **Cost:** ~a day of a 6-core arm.
- **Phase-2:** **superseded-by-H13 (`ambient-relaxation`)**, which decides all sizes at
  once, SAT-free, in **0.4 s** — but it stands as the independent computational leg.

### H12 · full-span closure solve (a negative methodological result)
- **Family:** monolithic exact solve.
- **What it does:** Offers the downstream block the entire 255-value span free and asks
  for the optimum at the improving level — one solve deciding all committed sizes at once.
- **Measured:** **failed, three times, in three lanes.** Lane A: 4 h,
  `status=crash_or_timeout`, **0-byte solver log** (a redirection hazard) — no lower bound
  at all. Lane G reproduced the failure (263 inputs, timeout at 240 s, bracket only). Lane
  CB: 66 min without completing even `k=4`, logged `aborted_no_level`, explicitly **not** a
  negative.
- **Cost:** ~5 h wasted across three lanes.
- **Phase-2:** **dead-end.** Three independent measurements say `slp_opt.py` cannot decide
  a 263-input dim-12 instance. **The reusable lesson:** *push constraints into the instance
  rather than sweeping loose ones — a 4-element `Q` decides in 24–70 s where a singleton
  does not decide in 3,100 s.*

### H13 · ambient relaxation single solve
- **Family:** exhaustive decision by relaxation.
- **What it does:** Instead of sweeping committed sets, hands the block **the whole ambient
  value space free, simultaneously**, so one decision ranges over every set of every size at
  once. The honest cap is then on *gates*, not on `|Q|`.
- **Measured:** **`U1(Q1) ≥ 6` for every committed set of every size from the whole
  255-value span — diagonal, skew, pure-hub, anything — and 6 is attained.** So an earlier
  15-diagonal narrowing loses **nothing** at this cell: its ansatz becomes a **derivation**,
  and `= 5` is refuted. Correction banked with no compute: the bracket was already `[5,6]`
  before the lane ran anything, because an exact `U1(15 diagonals) = 6` is an upper bound
  for the ambient instance.
- **Code:** `fleet3/laneCB_completeness/code/{cbtheory,decide}.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper — supersedes singleton sweeps outright.**

### H14 · minimal-set extraction + monotone upstream sweep
- **Family:** complete case split via monotonicity.
- **What it does:** Inverts a badly-priced sweep. Rather than pricing 240 loose singletons
  (measured **>3,100 s each** for the UNSAT half → ~150+ core-hours), it enumerates the
  *minimal* committed sets from the complete program census, then prices those —
  multi-element instances are far more constrained and decide in **24–147 s**.
  Monotonicity then lifts each decision to all supersets.
- **Measured:** **740 minimal committed sets** (92 of size 3, 648 of size 4). Swept to
  completion: **720 exhaustive UNSATs at cap 10 + 20 audited monotonicity prunes, 0 leads,
  0 timeouts, 11.85 core-hours.** With the census this is a **complete case split**, and
  yields: at the flagship cell, `core(Q1) = U07(Q1) + U1(Q1) ≥ 18` for **every** committed
  set — any subset of the 255-value span, any size, no cap — and 18 is attained. **The
  in-class 87 door at this cell is SHUT.** Non-trivially so: every single `vT` diagonal is
  upstream-**free** (`U07({w}) = 10` exactly), so the obstruction is joint and rank-driven
  and **no singleton filter could ever have found it.**
- **Controls:** CTRL-E (`U1({4,6,e})` = 6 SAT in 62.7 s on the same harness and cap where
  28 rank-≤2 sets return exhaustive UNSAT); **CTRL-F planted positive** (three values from a
  real optimal 10-gate upstream program → 10 SAT, 18.0 s).
- **Code:** `fleet3/laneCB_completeness/code/{extract_L,sweepL}.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper — the single best "how to price an interface" recipe** in the
  fleet slices.

### H15 · theory-first generator (derive the algebra, price the blocks, compile)
- **Family:** class-pricing generator — the inverse of search.
- **What it does:** Derives the algebra from GF(2⁸) and FIPS-197 alone (absolute trace,
  trace-dual basis by inverting the trace Gram matrix, mask↔line dictionary, the dual
  xtime chain **computed rather than tabulated**), decomposes the 32-target problem into
  ~10 blocks of dimension 8–16, asks the exact oracle for each block's provable minimum,
  replays the block programs into one global mask set, and verifies twice. **No search
  over circuits; no record circuit read at run time.**
- **Twist:** it constructs rather than searches, so a "miss" is loud (non-zero exit)
  instead of a silent claim.
- **Measured:** emitted and oracle-VALID: **116@3** (0 oracle calls), **91@5**, **92@4**,
  **94@5**, plus 95/99/103 where the model price was an *upper* bound and the mask set
  de-duplicated below it. Referee re-ran all four with its own fresh subprocess. Derived
  dual basis `29 b0 58 05 a6 53 a4 52` matches `atlas/ring.py` independently.
- **Code:** `fleet2/laneG_generator/generate.py`, `code/{theory,build,recipes,modules}.py`.
- **Generality:** **MIXED, and the most portable asset in fleet1–4.** The ladder derives
  from the reduction polynomial (`τ_k`), so `aes_inv_mixcolumns` needs: a new target list,
  a re-run of the module sweep, and a new currency-menu source (flag F1 — see H34/H39).
- **Phase-2:** **keeper** — superseded in implementation by H26 but the derivation chain
  is the thing.

### H16 · module sweep (capped σ predicate)
- **Family:** exhaustive table building.
- **What it does:** Generates the canonical sector interfaces from theory and asks the
  exact oracle the *capped* question `σ ≤ 7?` for each — cheap because a capped UNSAT
  terminates early.
- **Measured:** **1,383 canonical classes, 3,022 s wall, ZERO timeouts.** 92 YES (σ = 7
  with a 7-gate witness), 1,291 NO (exhaustive capped UNSAT, σ ≥ 8). **Independent
  cross-check:** all six `(kind,|P|,|Q|)` σ-7 counts equal those from `atlas/m1_sigma.json`
  (13,153 rows, different session, different generator, different solver invocations);
  the referee extended it to **466 shared decided classes, 0 disagreements.**
- **Code:** `fleet2/laneG_generator/code/{modules,sweep}.py`.
- **Phase-2:** **keeper.** Two independently produced tables agreeing cell-by-cell is the
  strongest control in that slice.

### H17 · ladder chain DP (keep the whole price spectrum)
- **Family:** exact DP over configurations.
- **What it does:** Outer loop over the hub menu, inner chain over the column menus, taps
  reading the hub; keeps a witness configuration for **every** achievable price, not only
  the minimum.
- **Measured:** achievable prices **91…107**, optimum **91**, and the optimal configuration
  independently re-derives `atlas/all7_config.json` — a genuine cross-lane agreement, not
  an import. Referee precision note: there are **exactly 2** configs at 91 and they are
  global `y`-rotations of each other.
- **Phase-2:** **keeper.** Keeping the whole spectrum (not just the argmin) is what made
  H18 and the 92@4 emission possible.

### H18 · depthscan (min-depth configuration search)
- **Family:** search over the *model's* configuration space; twist on H17.
- **Measured:** the all-σ-7 family contains exactly 2 configurations priced 91 and **both
  schedule to depth 5**. A 91@4 configuration does exist but its `C_2` carries only 2
  levels and so has σ = 8, putting it **outside** the swept family. **UNDECIDED: does an
  all-σ-7 91@4 exist?**
- **Phase-2:** **superseded-by-F9** (`dslp`), which puts depth inside the block decision
  instead of filtering afterwards.

### H19 · free-supply derivation (one solve bounds a whole family) + vacuity guard
- **Family:** exact-oracle instrument. **The single most re-used method in fleet waves 2–8.**
- **What it does:** Offers a downstream block a supply set `S` at **zero gate cost** and
  asks for the exact minimum. Because `S` is free, `U(S) ≤ U(Q)` for every `Q ⊆ S`: the
  answer is a machine-checked **lower bound for the whole family at once**, *and* the
  optimal witness hands back a concrete committed set. One solve replaces `2^{|S|}` point
  probes, and the witness is a derivation rather than a fit.
  The **vacuity guard** re-checks every artefact and stamps whether the configured
  commitment was even *inside* the offered family — if not, the run is marked VACUOUS.
- **Measured:** with the entire 255-value span it **timed out at 4 h**. Narrowing the
  candidate family *from theory* (240 → 15 tap diagonals) dropped the instance from 263
  inputs to 35, solving in **170 s** with **`U1 = 6` EXACT** and derived set
  `Q1 = {(d0+d7)⊗4, ⊗6, ⊗e}`. Pricing the upstream block with it:
  `COL0 0 + U07 12 + U1 6 = 18` — **exactly the R01 core of every record at this cell**,
  reached without ever looking at a record. **5 of 5 derived committed sets are bases of
  `vT` realised as tap diagonals**, every one a different basis. Family-wide (Test F):
  offered all 24 one-gate shared-plane values, got `W3 = 8` EXACT in **1,505 s**, and the
  witness **independently selected `u(5,4)` — record 88@7's own stepping stone**, with no
  record read at any step.
  **Vacuity guard results:** at `max_cost = 1` (shipped default) — D37 at W3 floor 8 over
  64 values, D37 at U4 floor 8 (witness took *exactly* the three configured values, 3/3),
  Q1 at U1 floor 8 over 45 values — **3 of 3 stamped VACUOUS**, because the configured
  values cost 2 gates on their planes, not 1. At `max_cost = 2` — family 200/241/241,
  floors **6/7/7, 0 of 3 vacuous**, and the Q1 derive **selects the configured triple
  exactly, 3/3**.
  **Single-value and pair census** (a full deployment): ~1,200 exact solves, **0 timeouts**,
  across five dim-8 blocks — **42 genuinely helpful values, every one worth exactly one
  gate, every one of full two-line support**; `B37` closed outright; 241 pair instances:
  **99 pairs save two, none saves three.**
- **Cost:** 2 s – 1,505 s per solve depending on family width; cost-1 runs 3,169 / 5,312 /
  6,925 s; cost-2 runs 551 / 2,076 / 2,018 s (**the wider family makes the instance
  easier**).
- **Code:** `fleet2/laneG_generator/code/freesupply.py`; `fleet3/laneF4_rule/code/f4model.py`;
  `fleet8/unified/code/{derive.py,algebra.py,annotate_derive.py}`;
  `fleet5/laneGLUE/code/queue2.py`, `queue4.py`, `queue5.py`.
- **Generality:** **CIRCUIT-GENERIC.**
- **Incarnations:** `fleet1_4:free-supply-derivation` → `fleet5_8:free-supply-derive (+ the
  vacuity guard)` → `fleet9_12:derive-family-vacuity-audit` (the guard as an audit).
- **Phase-2:** **keeper, with the guard mandatory.** *"The single highest-leverage
  technique in the project"* — it replaced a 2^24 point-probe sweep with one solve, and an
  instance that timed out at 4 h twice with a 170 s one. **Never run a free-supply derive
  without the in-family check.**
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — Generality under-declared, and one "all" has since been refuted.** Labelled `CIRCUIT-GENERIC` with no port cost, but all three cited paths run on the MixColumns sector algebra: `fleet2/laneG_generator/code/freesupply.py:42-43` imports `sector_value_lines, SECTOR_TARGETS`; `fleet3/laneF4_rule/code/f4model.py:30-31,84` builds its targets from them; `fleet8/unified/code/derive.py:44-45` imports `PARENT, QLINES, TAPS`. **H26 in this same catalog declares exactly this object load-bearing and non-portable** ("has to be re-derived, not re-typed"). Correct label **MIXED**, port cost = H26's port item (2). Second: "offered *all* 24 one-gate shared-plane values" was refuted — the true one-gate family is **64**, not 24 nor 48 (`fleet3/laneF4_rule/referee/REFEREE.md:56`: "The enumeration was wrong; the conclusion it supported survives"). The floor was re-established over the true family; the "all 24" has not been, and H27 carries the correction while this entry did not. Third: the `max_cost = 2` figures live in `fleet12/laneKNOBS/derive_out/`, which the Code field omits. Every other number is exact.

### H20 · merged-derive (interface derivation by boundary deletion)
- **Family:** SAT derivation, mis-specification-proof.
- **What it does:** To test whether a committed interface value between two blocks is real
  or an artefact of the split, **delete the boundary** and solve supplier and consumer as
  ONE block. The interface appears neither as a target nor as a free input, so the
  instrument is never told it exists; read the commitment off whatever the unconstrained
  optimum builds.
- **Twist:** unlike H19 it posits no candidate family at all, so **the vacuity failure mode
  cannot arise.** This is why its result stands and the free-supply ones (as originally run)
  did not.
- **Measured:** merged solve of B27 ∪ W3 on lines [2,3,7]: **exact, optimum 9 gates, 572 s.**
  Among the nine gates exactly one is supported on the tap-3 plane, and it is `δ₃(0xc)` —
  bit-identical to the value an earlier lane configured by hand. Derived rank 1. **This
  closed a referee's provenance finding and retired the `MATCHED` tag.** It also proves 9 is
  a lower bound over *every* commitment of every rank.
- **Code:** `fleet8/unified/code/derive.py --derive Q27`.
- **Phase-2:** **keeper — this is the shape to reach for.** The project's own conclusion is
  that MERGED beats FREE-SUPPLY as a derivation method because it cannot be mis-specified.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** Two pointer defects, and **this entry carries no `Generality` label**. (a) The Code line reads `fleet8/unified/code/derive.py --derive Q27`, but `code/derive.py` has **no argparse at all** — the flag is on `generate.py:422-423`, i.e. `python3 generate.py --derive Q27`. (b) Correct label is **MIXED**: `derive_merged` is built on `laws.architecture()`, `TAPS`, `plane_of` and the 8-line ring frame, so a bare port is not available; the starter kit's "block names" port cost understates it. The results JSON matches this entry field-for-field.

### H21 · rank-curve measurement
- **Family:** SAT parameter sweep.
- **What it does:** Instead of assuming a law about how many values an interface should
  carry, price supplier + consumer at each rank 0,1,2,3 over the derived family and read the
  optimum off the curve.
- **Measured:** rank 0 → 9, rank 1 → 9, rank 2 → 10, rank 3 → 11. So **rank 0 and rank 1
  TIE**; the first gate at B27 buys back one gate gross (W3 9→8), net zero — **not the two
  the charter's law claimed.** The merged solve's exact 9 proves the tie is the floor.
- **Cost:** ~1,600 s total.
- **Phase-2:** **keeper.** Cheap, and it caught a prescribed law being wrong.

### H22 · replay bound / conservation (a lower bound for the price of one solve)
- **Family:** free lower bound by program replay.
- **What it does:** If a producer block's inputs are all available to its consumer, the
  consumer can simply replay the producer's whole program verbatim. Hence
  `B37 + U4(D37) ≥ U4(no D37)` for **any** commitment whatsoever — costing one solve of the
  consumer *with no supply at all*.
- **Measured:** `U4(no D37)` = **11 EXACT** (k=6..10 exhaustively UNSAT, k=11 SAT; 17,199 s),
  independently re-solved by a referee on a differently packed instance at 23,673 s. In
  fleet8: U4 with no D37 = **11** (exact, 5,263 s); W3 with no D37 = **11** (exact,
  5,856 s). Consequences: (1) the measured "conservation law" `B37 + U4 = 11` becomes a
  **proven, tight floor** — every configuration measured sits exactly on it, so **no
  re-choice of the tap-4 interface can ever gain a gate**; (2) with `W3 ≥ 8` family-wide,
  `B ≥ 12 + W3 ≥ 20` — **no 87 at the 88@7 cell** in the derived family; (3) it resolved a
  referee UNDECIDED (the merged `U347` bracketed `{10,11}`; the answer is 11, so **the split
  costs exactly 0**). The referee then walked `W3 ≥ 8` out to the **complete 64-value
  one-gate family** (48-value solve: k=7 UNSAT 3,944 s, k=8 SAT).
- **Cost:** ~3.1 core-hours in fleet8.
- **Code:** `fleet3/laneF4_rule/code/f4model.py` (no-supply instances);
  `fleet8/unified/code/derive.py --derive conservation`.
- **Generality:** **CIRCUIT-GENERIC** wherever a block model has nested input sets.
- **Incarnations:** `fleet1_4:replay-bound` · `fleet5_8:conservation-replay-bound`.
- **Phase-2:** **keeper — the cheapest sound lower bound in the toolkit**, and why "one
  gate in, one gate out" keeps showing up.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** Same invocation error as H20 — `--derive conservation` is a `generate.py` flag, not a `derive.py` one (and "conservation" is not in its help string `"Q1|Q27|D37|all"`, though `derive.main` accepts it). Also the closing parenthetical splices two different referee runs: the 3,944 s belongs to the **48**-value solve, while the complete **64**-value repair solve is a separate run (k=5,6,7 UNSAT / k=8 SAT). The CIRCUIT-GENERIC label is defensible *because* the entry states its proviso.

### H23 · defect-calculus rule derivation (RULE F4)
- **Family:** hand-derivation + exhaustive machine checking.
- **What it does:** Defines a per-sector "defect" `Δ_k = t_{k−1} + t_7` (zero exactly on
  sector-k values), tabulates how each elementary move changes `(p_k, Δ_k)` and who else can
  use it, and reads off the rule. Every identity is then machine-checked exhaustively over
  `T × T`.
- **The rule:** a tap's interface plane pays for itself **exactly when the tap sits
  immediately above another tap (or above the root)**. From the reduction polynomial alone:
  AES taps `{1,3,4}`; `1−1 = 0` (root) → shared; `4−1 = 3 ∈ TAPS` → shared; `3−1 = 2 ∉ TAPS`
  → **unshared**. So this field has exactly ONE unshared tap interface, at tap 3 — **which
  is precisely where all 3 gates of the model's gap sit and precisely where every record
  keeps the interface rank at ≤ 1.** That is content beyond a fit: it names, from the
  polynomial, which interface must not be greedily filled.
- **Measured:** identities I1–I5 all PROVED exhaustively (256/256, 240/240). Prescription
  measured against all 14 records: tap 1 rank ≥ 2 always; tap 4 rank ≥ 2 in 13/14; **tap 3
  rank ≤ 1 in 14/14**, and **every one of the 14 records' `D27` values is a one-gate value.**
- **Code:** `fleet3/laneF4_rule/code/{rule,prescribe,planeenum}.py`.
- **Generality:** **CIRCUIT-GENERIC over any field with a reduction polynomial** — the rule
  is stated in terms of `τ_k`, so it transfers to `aes_inv_mixcolumns` and to other MDS
  matrices directly. **The most transferable *idea* in fleet1–4.**
- **Phase-2:** **keeper — the one modelling rule that closed 91 → 88.** Under the previous
  F4-restricted model the same cell prices 91; with the rule it prices 88 and **builds a
  VALID 88-gate circuit** (`results/gen_f4_88_D4.json`, re-verified: `gates=88 depth=10
  32/32 VALID`).

### H24 · stratified attribution (find out *where* a model is wrong)
- **Family:** structural analysis of a price gap.
- **What it does:** Takes a modelled price that is loose by `n` gates and re-stratifies both
  sides by *exact* line support until the gap localises to one stratum, with a per-gate
  assertion that each gate's value is the XOR of its operands' values in line coordinates.
- **Measured:** **corrected the referee's own diagnosis.** The referee had localised "the
  bulk" of a 3-gate gap to a line restriction. Re-stratified:
  `COL3 0 / Q27 +3 / D37 +1 / W3 0 / U4 −1` — **all of it sits at the tap-3 interface.** And
  the line restriction is *empirically free*: across all 14 known 88s, **0 of 107 `U4` gates
  carry line 2 in their value AND 0 carry it in an operand.** What the model actually
  deleted was the **export edge** `D37 → W3`: of the 52 `{3,7}`-stratum gates across the 14
  records, **46 feed the sector-3 work and 27 are consumed by BOTH blocks; 14/14 circuits
  have ≥ 1 dual-role gate.** Control: an independent re-implementation of the block
  classification reproduces the per-block sizes on **22/22 circuits exactly.**
- **Code:** `fleet3/laneF4_rule/code/{blocks,r34anat,strata,attrib,walk88at7}.py`.
- **Phase-2:** **keeper — this is how you find out *where* a model is wrong.**

### H25 · stepping-stone non-interchangeability (Test G)
- **Family:** falsification of a derivation rule; twist on H19.
- **What it does:** When a derived family has few members, prices *each* member rather than
  assuming the choice is immaterial.
- **Measured:** the derived family of one-gate stepping stones has **exactly two** members;
  record 88@7 uses `u(5,4)` and record 88@8 uses `u(1,4)`, so the lane predicted the choice
  was immaterial and priced the other to prove it. **MISS:** `W3` = 8 with `u(5,4)`, **9**
  with `u(1,4)`. Assembling the alternative end to end emits a **VALID 89** — reported as
  the 89 it is, not the 88 it was aimed at. **So "pick any member of the derived family" is
  REFUTED as a derivation rule; the family-wide free-supply solve is not.**
- **Phase-2:** **keeper — the methodological lesson of fleet wave 3.** *That distinction is
  the difference between a derivation and a fit.*

### H26 · unified generator ★
- **Family:** class-pricing generator / block-decomposition assembler. **The crown jewel.**
- **What it does:** Emits a complete, oracle-valid MixColumns XOR circuit at a **requested
  gate count and depth**. It derives a ten-block decomposition of the 32×32 problem from the
  field and the matrix alone, solves each block to a *proven* minimum with an exact SAT
  oracle, assembles the union of gate masks, schedules them at minimum depth by level-BFS,
  and verifies twice (in-process against targets rebuilt from FIPS-197, and by a fresh
  `verify_circuit.py` subprocess). It refuses to emit a circuit that misses the request:
  infeasibility, timeout and solver failure are three distinct exit codes (4 / 5 / 7) and
  none is ever reported as the others.
- **Twist:** it replaces three earlier generators (H15 = recipes only, could not reach 88,
  and `--depth` was a post-hoc *check*; `fleet3/laneF4_rule/code/gen.py` = reached 88 but had
  no depth parameter; `fleet4/laneDEPTH/code/genD.py` = depth-capped but two configurations
  and no count interface). Four things are genuinely new: (a) the architecture is *derived*
  by `code/laws.py` rather than tabulated; (b) depth reaches the model in four places rather
  than being read off afterwards; (c) `--count` is checked against the **emitted** count with
  the delta's cause named; (d) pre-registration is hash-chained and written *before* the
  solve.
- **Measured:** regression **9/9 rows hit their asked count and verified VALID**: 116@3,
  91@5, 92@4, 93@5, 94@5, 88 (uncapped, emitted at depth 7), 88@5, 89, 90@5. Reachability
  map: **137 cells probed, 33 VALID, 17 INFEASIBLE, 75 ELSEWHERE, 12 UNDECIDED**
  (`CONFLICT`: the live `results/reach_grid.jsonl` now has **138 rows / 13 UNDECIDED** — one
  row of drift; Appendix B #3). Verified (gates, min depth) pairs emitted: 88@5, 89@6, 90@5,
  91@4, 92@4, 93@4, 94@4, 95@4, 96@5, 97@4, 98@5, 99@5, 100@4, 101@4, 102@4, 103@5, 104@4,
  105@4, 108@4, 116@3. Cap-off control **10/10** against `atlas/slp_opt.py` on the ten real
  blocks. Integrity at hand-off: pre-registration chain OK / 55 entries, 12/12 circuits
  re-verify VALID, ledger 375 solves + 137 reach cells; **ledger has since grown to 1,948
  rows / 1,028 solves** because fleet12 lanes drive this tool.
- **Cost:** cheap warm (0.19–0.54 s per regression row from cache); expensive cold — **88@5
  cold was 4,916 s**, 90@5 cold 611 s, 89 cold 167 s. The `--map` sweep ran ~7.7 h.
- **Code:** `fleet8/unified/generate.py` + `code/{theory,laws,plan,dslp,solver,engine,assemble,cells,ledger,live}.py`.
  *(Do not touch `fleet8/unified` per campaign rules — read only.)*
- **Generality: MIXED — this is the important paragraph for phase 2.**
  * **CIRCUIT-GENERIC (no change needed):** the whole SAT layer (`dslp.py` —
    gate-position encoding, one-hot pair selection, N1/N2/N3 symmetry breaking, L1 cone
    bound, optional level variables, `reach_levels` exact reachability), `solver.py`,
    `assemble.py` (mask set with collision accounting, `min_depth_schedule`,
    `strip_dead_gates`, `verify_inprocess`), `engine.py`, `ledger.py`, `regress.py`,
    `reach.py`/`render.py`, `capoff.py`, `live.py`. These are a general exact-SLP toolkit
    and would work on any GF(2) linear map.
  * **FIELD-HARDCODED but shared with the inverse:** `code/theory.py:30 AES = 0x11B`.
    Everything derived from the *field* — the dual basis, the dual xtime chain, and
    therefore `QLINES`, `TAPS = {1,3,4}`, `CLEAN`, `PARENT` — comes from 0x11B alone and is
    **unchanged for `aes_inv_mixcolumns`**, which uses the same field. So L0, L2, L3
    (*tap 3 is the unique unshared interface*) and L4 all transfer verbatim.
  * **MIXCOLUMNS-HARDCODED (what must change):** three things, all in `code/theory.py`:
    1. `mixcolumns_target_masks()` (lines 88–119) — the 32 target rows from the `[2,3,1,1]`
       circulant. For inv-MixColumns this becomes the `[e,b,d,9]` circulant. Mechanical.
    2. `W = 0x7` (line 200) and `SECTOR_TARGETS` (lines 254–257) — **the load-bearing one.**
       It encodes that a MixColumns sector target factors as a **p-part on line j plus a
       q-part on `QLINES[j]`** with `c = 3 = 1 + y` and a single unit factor `w = 1+v+v²`.
       The inverse matrix's coefficients **do not have this two-part shape**, so this
       decomposition — and with it `laws.workset`, the block line-sets, and the whole
       ten-block architecture — has to be **re-derived, not re-typed.** Expect the inverse's
       worksets to be wider and the block count/dimensions to change.
    3. `sector_value_lines` / `sector_of` (lines 243–274), which assume the same (p, q) shape.
  * **RECORD-PROVENANCED (external, not derivable):** `code/cells.py:32` reads
    `fleet1/laneA_v2pricing/results/configs.json` for the currency menus and the 22 cell
    definitions, and `cells.py:170` reads the ladder spectrum. This is **flag F1** and it is
    live: *every* `f4`-regime price is conditional on a menu read off a record circuit. For a
    new circuit there is no record to read, so **phase 2 must either derive menus (H34 already
    reads a record-free menu out of a charged witness — the highest-value remaining wiring
    job) or run the `ladder`/`naive` regimes, which are record-free but price 91+.**
- **Phase-2:** **KEEPER — the crown jewel.** Port order for another circuit: (1) swap the
  target matrix; (2) re-derive the sector (p, q) decomposition and `workset` from the new
  coefficients, keeping `laws.py`'s L2–L5 reasoning intact; (3) run `--regime naive` for a
  closed-form baseline, then `--regime ladder`; (4) **solve the menu problem before
  attempting the `f4` regime.**
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** Two wording defects inside the Generality block; everything else in this entry survived the hardest check in the audit, including every line citation and the (p,q) claim. (a) "So **L0, L2, L3 … and L4 all transfer verbatim**" is false as code: `laws.py:92-96 plane_is_shared` and `laws.py:132-138 supplier_of` both compute through `workset()` — which *is* L1, the one the next bullet concedes must be re-derived — and L4 additionally hardcodes MixColumns block-name tables (`laws.py:121`, `:127-129`). Only **L0, L2 and L5** are genuinely field-or-support-only. (b) The ladder spectrum is filed under "RECORD-PROVENANCED (external, not derivable)", but `cells.py:174-181` states the opposite — *"the DP is theory-generated (**no record circuit is involved at any point**)"* — and this entry contradicts itself two sentences later by naming `ladder` as a record-free escape. Flag F1 covers `cells.py:32` (configs.json) only.

### H27 · law derivation (`--explain` / `laws.py`)
- **Family:** structural analysis, solver-free.
- **What it does:** Derives, **as executable code rather than tables**, the block
  architecture: which lines each block works on, where each tap's carrier plane sits, which
  planes pay for themselves, which need a dedicated supplier block, which already-built
  values are free to which blocks, and the topological block order.
- **Twist:** it replaces three lanes' hardcoded `ORDER`/`LINES` tables. The headline is that
  the hand-written "shared-plane RULE" (H23) — the one edge worth the three gates between 91
  and 88 — **is not a rule but a *consequence* of one predicate** (L5: a built value is free
  to every block whose workset contains its support).
- **Measured:** against the hand-written supply at the 88@7 cell: supply superset **10/10**,
  prices agree **10/10**, model price 88. W3's supply under L5 is *exactly* the hand-written
  26 values, D37 included, with no `if name == "W3"` anywhere. Also derives the corrected
  one-gate interface families — **64** on {3,7} and **71** on {2,7}, against `planeenum.py`'s
  24 and 56.
- **Cost:** milliseconds, no solver.
- **Generality:** MIXED — L0/L2/L3/L4/L5 are field-generic (0x11B), L1 is MixColumns-specific.
- **Phase-2:** **keeper.** This is what makes the generator legible instead of configured,
  and it is the template for deriving *any* circuit's block architecture from its algebra.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — the Generality line is self-contradictory, and one claim is literally false.** (a) "L0/L2/L3/L4/L5 are field-generic (0x11B), L1 is MixColumns-specific" cannot hold: L3 (`plane_is_shared`, `laws.py:92-96`) and L4 (`supplier_of`, `laws.py:132-138`) are *computed by calling* `workset()` — the L1 the same sentence concedes is MixColumns-specific, and whose docstring gives the reason (`laws.py:17-19`); L4 also hardcodes the MixColumns block/interface name tables at `:121` and `:127-129`. Correct: **L0, L2, L5** generic; **L1, L3, L4** MixColumns-derived. (b) "with no `if name == \"W3\"` anywhere" is **literally false** — `fleet8/unified/code/plan.py:279: if not share and name == "W3":`. The primary is careful where this entry is not: `RESULT.md:33-34` says "no `if name == W3` anywhere **in the model**", and `laws.py:49-50` names that branch as the deliberate `--no-share` labelled control. Dropping three words turns a true claim into a false one. (c) This entry has **no `Code:` field**; `laws.py` and `--explain` appear only in the heading. The measured block is clean (10/10, model price 88).

### H28 · reachability map sweep
- **Family:** systematic probe / measurement.
- **What it does:** Asks the generator for every (count, depth) pair in a grid, banks one
  append-only row per cell, and renders a map distinguishing four verdicts: **VALID** at the
  asked count; **ELSEWHERE** (valid but a different count, because the mask set
  de-duplicated); **INFEASIBLE** with the *reason* (machine-checked depth-unreachability vs
  no configuration at that price); **UNDECIDED** (a timeout, never a refutation).
- **Twist:** nothing in the project had this before; the INFEASIBLE/UNDECIDED separation is
  the honest part.
- **Measured:** 137 cells (33/17/75/12) — see the `CONFLICT` note in H26. Standing warning
  recorded: an `infeasible_depth` verdict is a statement about *this decomposition*, not
  about circuits — the repo's own 97@3 is a circuit this model cannot express.
- **Cost:** ~7.7 h.
- **Phase-2:** **keeper.** This is the deliverable shape for "what can the generator actually
  do on circuit X".

### H29 · block-merge relaxation (the merge lattice)
- **Family:** SAT relaxation test at boundary scale.
- **What it does:** Dissolves a block boundary by solving two or three blocks as ONE exact
  instance. This relaxes **three** modelling choices simultaneously — boundary placement,
  one-way information flow, and the interface commitment (which becomes internal and may be
  replaced by anything or nothing). A null is therefore a theorem about a strictly larger
  class.
- **Twist:** two properties are machine-checked for **every** candidate before any solve:
  the **replay bound** (`merged ≤ split`, by concatenating the members' own optimal programs)
  and **strict generality** (an explicit witness of one of three kinds — W1 boundary, W2
  order, W3 commitment). **349/349 on both.**
- **Measured:** **nineteen boundaries dissolved, nineteen times exactly the split total.**
  Plus **131 further candidates settled FREE with no solver at all** by admissible bounds.
  **Seven boundaries dissolved simultaneously — 14 of 18 blocks merged into 7 — and the class
  optimum is still exactly 88.** Two undecided: `MB27B373` `[12,13]` (since closed, see H30)
  and `MU07U1` `[10,18]` (timed out at k=17 after 11,879 s, exactly as pre-registered).
  Sharpest rows: `MB273` (deletes the Q27 commitment entirely) = **exact 9**, and its
  unconstrained 9-gate witness's **first gate is `δ₃(0xc)`** — the committed interface value,
  chosen freely. `MB373` = 12 exactly, closed by three instruments agreeing.
- **Cost:** ladder decisions from 0.7 s to 6,674 s; the two undecided rows consumed
  11,766 + 31,681 + 11,879 s of timeout.
- **Code:** `fleet5/laneMERGE/code/{mergemodel,enumerate_merges,containment,bounds,tally}.py`.
- **Generality:** **CIRCUIT-GENERIC — one of the most transferable methods in fleet5–8.**
- **Phase-2:** **keeper.** "Enumerate every boundary, machine-check the replay bound and
  strict generality, then dissolve them" is a complete recipe.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — Generality under-declared.** Every measured number verifies exactly (I had the 19 decided rows counted from the table). But it is labelled `CIRCUIT-GENERIC` while `fleet5/laneMERGE/code/mergemodel.py:66` wires in the MixColumns ring frame's line map (`LINES = {"U07": [0,7], "U1": [0,1,7], "B27": [2,7], …}`), `:63` the 8 column blocks, and `:94` a **record cell** (`CURRENCY = … # = 22 at the 88@7 cell`). Correct label **MIXED** — which H33 in this same file already says for the same object. The recipe ports; this code does not, and the starter kit's "block model" port cost is the honest one.

### H30 · uncapped-ladder deep-level decision (when to just buy it)
- **Family:** SAT, brute allocation.
- **What it does:** Takes one undecided merge row, hands the *uncapped* instance 12 cores and
  a 24 h budget, and lets the ladder re-derive the cheap levels before spending everything on
  the decisive one. No cleverness — it is the deliberate purchase of one decision that two
  earlier capped attempts (11,766 s and 31,681 s on 4 cores) could not afford.
- **Measured:** `MB27B373` (tap-3 interface + shared plane + sector-3 work as ONE block, dim
  12, 21 inputs, 8 targets): **k = 8/9/10/11/12 all exhaustively UNSAT** at 2.63 / 10.11 /
  96.36 / 994.88 / **19,458.32 s.** With the replay upper bound of 13 that forces
  **`MB27B373 = 13` exactly = the split total.** The triple boundary is FREE; **12 would have
  priced the class at 87, and it does not.**
- **Cost:** ~5.4 h for the decisive level; ~24 h wall.
- **⚠** `fleet6/door` has **no `RESULT.md`** — its decisive result lives in a 170-byte log.
- **Phase-2:** **keeper as a pattern.**

### H31 · charged-group bound (the all-menu theorem)
- **Family:** SAT + concatenation argument.
- **What it does:** Bounds the model price over *every* menu configuration at once, by
  charging each line's currency to exactly one block and summing exact per-block free-supply
  floors over disjoint charged lines.
- **Twist:** a bound over a **1.41e26-element space** obtained from ten machine-checked
  solves, not a sample. And it says *where* the slack is.
- **Measured:** **price(C) ≥ 87 for every menu**, against price(MENU_88at7) = 88. **Nine of
  the ten bounds are exactly tight.** The one loose gate is the hub: line 7 is read by seven
  of ten blocks but charged to one, and `bound(S7W,{7}) = 10` against a record charge of 11.
  **87 is the exact ceiling of the one-block-per-group scheme, not a compute limit.** Four
  blocks (U1, B27, B37, W3) are additionally proved **menu-proof** — already at their floor
  at 88@7. Pre-registered in full (assignment, every bound, the total) before the deciding
  solves ran, and it came in exactly.
- **Cost:** ten exact block solves plus 31,104 assignment evaluations.
- **Code:** `fleet5/laneMENU/code/{mmodel,bound_opt,queue_main}.py`.
- **Generality:** CIRCUIT-GENERIC as an argument shape (charge disjoint resources to single
  blocks, sum exact floors).
- **Phase-2:** **keeper — one of the two strongest arguments in fleet5–8.**

### H32 · cell sweep (price every known menu exactly)
- **Family:** systematic SAT measurement.
- **What it does:** Prices all 21 known cells block by block at the fixed interface
  commitment, cheap blocks first so expensive ones are only spent on cells that can still
  reach 87.
- **Measured:** the pre-registered null ("the menu does not matter") is **refuted 41 times
  out of 168** — the menu moves individual blocks by up to 3 gates (S2W 6..9, U07 9..12, B27
  1..3, B37 4..6, U1 6..8, U4 6..8) — **but no cell's blocks move together.** **Every one of
  the 20 distinct known cells prices ≥ 88**; nine are pinned at exactly 88, eleven are ≥ 91.
  The `p88_0x` family exhibits perfect break-even seven different ways: `costT(C_0) + U07 =
  12` constant across seven distinct menus.
- **Cost:** 134 solve rows / 1,328 result rows in a 2,801-row ledger.
- **Phase-2:** **keeper.** The break-even table is the clearest single picture in fleet5–8 of
  *why* 88 keeps appearing.

### H33 · menu-space formalisation + ρ theorem (solver-free)
- **Family:** structural analysis / exhaustive enumeration.
- **What it does:** Formalises the currency-menu parameter (the per-line shopping list of
  T-shapes), enumerates it exactly (**1,857 buildable shape-sets per line, 1,857⁸ = 1.41 ×
  10²⁶ configurations**), and proves the menu space carries a price-preserving `Z/4` action
  from byte rotation.
- **Twist:** no solver anywhere. It converts an unswept, unflagged parameter into a finite
  object with a known size and a symmetry.
- **Generality:** MIXED — the *move* (formalise the free parameter, size it, find its
  symmetry) is CIRCUIT-GENERIC and is the right first step for any new circuit.
- **Phase-2:** **keeper.**

### H34 · derive-menu-from-witness ★ (the highest-value unfinished item)
- **Family:** derivation / provenance removal.
- **What it does:** Reads a **record-free** currency menu out of any charged-group optimal
  witness.
- **Measured:** at the 88@7 `U07` control it returns `C_0 = {2,4,7,b}`. **Written, tested,
  and never wired into the generator.**
- **Code:** `fleet5/laneMENU/code/derive_menu.py`.
- **Generality:** CIRCUIT-GENERIC — **and this is the piece phase 2 needs most, because a new
  circuit has no record to read menus off.**
- **Phase-2:** **keeper — highest-value unfinished item in fleet5–8.** Wiring it into
  `--derive` is the single move that would make the whole `f4` regime record-free.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — Generality label wrong; but the method is real, not vapour.** I had `fleet5/laneMENU/code/derive_menu.py` (85 lines) run once under `nice -n 19`: it prints `DERIVED MENU (single-line gates): {0: ['0x2','0x4','0x7','0xb']}` — exactly the claimed `C_0` — while the record's own 88@7 menu is `[]`, so the derived menu is genuinely not read off the record. "Never wired into the generator" is confirmed by grep. But `derive_menu.py:26-28` hardcodes `BLOCK_LINES` for the ten MixColumns blocks and runs on `theory.support` and the 8-line ring frame. Correct label **MIXED**. This matters because the entry's whole phase-2 pitch is "a new circuit has no record to read menus off" — a new circuit also has no `BLOCK_LINES`.

### H35 · merged-group probe (the hub instrument)
- **Family:** SAT joint levels.
- **What it does:** Generalises H31 from one block to a *set* of blocks, so a group can share
  currency internally. Deciding it decides whether the all-menu theorem's 87 is real or an
  artefact of the one-block-per-group restriction.
- **Measured:** group {S7W, B27} on lines {2,6,7}, dim 12, 34 inputs, 5 targets, line 7
  charged. **k = 6,7,8,9,10 all exhaustively UNSAT** at 37.1 / 57.1 / 208.1 / 1,144.8 /
  **13,140.2 s**, so `bound ≥ 11` is proven. **`k = 11` is the deciding level and was stopped
  by the operator, not refuted** (`status=stopped_by_operator, lower_bound=11,
  lb_kind=bracket, predicted=12`).
- **Cost:** level cost growing ~11×; an UNSAT at k=11 estimated at ~1.5e5 s against ~3.3e4 s
  remaining.
- **Phase-2:** **keeper — an open, priced, decisive row.**

### H36 · block-boundary halo widening
- **Family:** structural mutation.
- **What it does:** A block is only allowed to use values on its own small set of coordinate
  "lines". This **widens** one block's line set by a halo and re-prices, testing whether the
  partition the model enforces is costing gates. It widens the *admissible set* without
  touching the predicate; the tractability guard (≤4 lines / dim 16) is enforced inside the
  patch.
- **Measured:** **twelve mutations, eleven complete, every one prices exactly 88, not one
  block moved a single gate** — including the falsifier's own home, both ring-adjacent
  widenings of the largest block, and all four hub blocks widened at once. **It is not
  vacuous:** `U4`'s supply grew 25 → 41 with **nine of the sixteen new values genuinely
  straddling the invented boundary**, and k=6 was then proved UNSAT in 104 s at dim 16 with
  all 41 available. **The mechanism found is worth more than the negative: a halo enlarges
  what a block MAY use; it does not change what the block is MINIMISING.**
- **Cost:** minutes to ~340 s per mutation.
- **Phase-2:** **closed, do not re-buy.** The mechanism predicts all further widenings dead;
  only the *un-split* block (a merge, not a widening) survives, priced at k ≥ 14.

### H37 · block-order permutation sweep
- **Family:** structural mutation, full coverage.
- **What it does:** The blocks are solved in some order, and each is handed everything already
  built that it is allowed to use — so the order decides each block's free supply and
  therefore, in principle, its price. This enumerates **all** legal orders and prices every
  one, refusing any order violating a *derived* dependency edge.
- **Measured:** **75/75 price 88, and far sharper than that** — every block in every order was
  handed a **byte-identical instance** (740 of 740 post-control block solves were cache hits
  on a key containing the free supply and its arrival levels), and **all 75 emitted files
  share one md5** (`eba1f6a998f5a9b30770b0651bb20396`), VALID ×75. **The 75 orders are not 75
  classes with a common optimum — they are one class.** Mechanism: under the four forced
  edges the supply graph is *saturated*, so a permutation has nothing left to move.
- **Cost:** **215.1 core-seconds = 0.060 core-hours** for the whole sweep (all of it the
  control); the other 74 orders cost 9.85 s each of cache replay.
- **Phase-2:** **closed.** The *saturation* mechanism tells a successor when to bother
  re-running it (a configuration where some block builds a mask on a proper subset of its
  lines).

### H38 · commitment-grammar knob sweep
- **Family:** structural mutation.
- **What it does:** Three "interface commitments" were hand-written dictionary literals. This
  introduces a tiny closed grammar so a commitment can be specified as one environment
  variable, and sweeps the alternatives — with an unparseable term a **hard error** rather
  than a silent fall-through.
- **Measured:** 65 pre-registered runs, **nothing ≤ 87**. Best results 88 uncapped, **88 @
  depth 5 (ties the record)**, 90 @ depth 5, 92 @ depth 4. Five pre-registered predictions
  **refuted**, and the refutations carry the lane: (i) the `Q27` `MATCHED` tag is overstated —
  **six of sixteen tap-3 settings reach a verified 88**, not one, and none of the winners is
  in the menu heuristic supposed to predict them; (ii) the `Q1` derive, widened from
  `max_cost 1` to 2, stops being vacuous **and selects the configured triple exactly**
  (predicted not to); (iii) the two depth parameters called the cheapest open axes are
  **inert** — every interface constraint switched off at D=5, both configurations, 13 rows,
  price unchanged. One pre-registered control **failed and was right to**: it exposed that the
  depth-4 record is a *ladder* circuit, so the axis was never testable against it.
- **Cost:** **38,120 core-seconds ≈ 10.6 core-hours.**
- **Phase-2:** **closed.** *"The cheap axes were cheap because there was very little in them,
  and what there was, was a correction rather than a circuit."*

### H39 · menu-derivability diff (is this inherited constant derivable at all?)
- **Family:** structural analysis / provenance, no solver.
- **What it does:** The deepest record-dependency in the package is a set of eight per-line
  "currency menus" read off known record circuits. Before spending any solver time, this
  enumerates every menu that a *rule* could produce and diffs them against the shipped one —
  because if the menu were some rule's output, the dependency would close by derivation at
  zero cost.
- **Twist:** it is a **proof, not a survey**, in its decisive test: derive the eight lines'
  attributes from the theory alone, observe that three lines the theory cannot tell apart
  carry three *different* shape sets (one of them empty), and conclude that **no rule that is
  a function of the derived line attributes can emit this menu.**
- **Measured:** 3,879 enumerated rule instances vs all 22 cells → **0/22 matched**; the
  per-role family exhaustive over 57³ = **185,193** instances → **0** reproduce the shipped
  menu; the 22 record cells hold **21 distinct menus**, with currency prices from 20 to 28.
  Verdict: **the menu is a property of the circuit it was read off, not of MixColumns.**
- **Cost:** minutes, no solver (189,072 rule instances diffed).
- **Code:** `fleet12/laneF1/{diffcheck,menu_rules}.py`.
- **Generality:** **CIRCUIT-GENERIC as a discipline** — before mutating an inherited constant,
  first ask whether it is derivable, exhaustively, without a solver.
- **Phase-2:** **keeper. The cheapest hard result in fleet12.**

### H40 · menu neighbourhood + trade-off sweep (measure the cross-term)
- **Family:** structural mutation / cost-curve measurement.
- **What it does:** Mutates the currency menu one shape at a time (add / drop / double-drop /
  triple-drop, plus whole rule-generated families) and measures how the circuit total
  responds — i.e. it measures the *cross-term* between what you spend on shared reusable
  values and what the blocks then cost. The deliverable is a **curve**, not a best-of.
- **Measured:** 49 distinct runs, **25 at exactly 88, none below.** The cross-term is
  **exactly −1.00 block gate per +1 currency gate across |M| ∈ [19,23]** — spending more on
  currency buys back exactly what it costs, never more — so **88 is a five-wide flat plateau
  in the menu axis with cliffs on both sides** (the fourth drop costs four block gates,
  88 → 91). Mechanism: **19 of the 25 88-gate runs emit the byte-identical gate list**
  (md5 `edf56fcc3641`) — dropping a shape does not delete a gate, it changes which phase
  builds the same mask. Best *rule-generated* menu prices **97**; the record menu beats it by
  **nine gates**. It also refuted its own pre-registration: the pipeline total is **not**
  monotone in the menu.
- **Cost:** **11.99 core-hours.** Coverage was tiny (5 of 64, 6 of 128, **0 of 262,144**) and
  the RESULT says so.
- **Phase-2:** **keeper as a template** — "measure the cross-term before assuming a knob is
  load-bearing".

### H41 · self-controlling block reoptimisation (ask at the known-achievable length)
- **Family:** exact optimisation with the control inside the answer.
- **What it does:** Takes a block `B` of a known circuit, defines NEEDED/AVAIL from the rest,
  and asks the exact oracle for the minimum in-block program at `max_gates = |B|`. One solve
  returns either a decoded witness at `|B|` — **the positive control, inside the same solve** —
  or a program below `|B|`, which is an 87 outright.
- **Twist:** the predecessor asked at `|B|−1`, a decision whose only outcomes are UNSAT or
  nothing. Asking at `|B|` costs the same and is strictly more informative — and it is what
  exposed **three vacuous published negatives**.
- **Measured:** whole 112-block dim-8 sweep in **1,291 s**. 67 `OPTIMAL_AT_nB`, 35
  `NOT_COVERED`, 10 `CONTROL_FAILED`, **0 HIT**. Hit-path control: 4/4 spliced witnesses
  re-verified by the oracle.
- **Cost:** 21.5 CPU-minutes for a sweep an earlier campaign had left unfinished.
- **Code:** `experiments/e3a_exploit/code/{blocks,kern}.py`.
- **Phase-2:** **keeper, top tier.** *"Ask at the known-achievable length so the control is
  the answer"* is the single most reusable control-design idea in the experiments slice.

### H42 · population-scale block reoptimisation (`blockpop`)
- **Family:** H41 scaled to an arbitrary replayed circuit.
- **What it does:** The same self-controlling question, but re-derives BLOCK/NEEDED/AVAIL for
  an **arbitrary replayed circuit** instead of named ones, so it can be pointed at the whole
  harvested population. Address-by-content, not by name; ~9 s per block.
- **Measured (re-tallied from the ledger; the RESULT.md numbers are stale):** **586 blocks
  decided — 324 `OPTIMAL_AT_nB`, 198 `NOT_COVERED`, 64 `CONTROL_FAILED`, 0 HIT.**
- **Trap recorded in-source and worth carrying:** one harvest file is a **transposed-matrix**
  harvest whose states are not MixColumns circuits; it silently filled **268 of a 400-state
  sample**. Any harvest-wide sweep needs a validate-before-admit loader.
- **Phase-2:** **keeper** — the highest-coverage exact 87-detector in the experiments slice,
  and **still nowhere near saturated (586 of 78,281).**

### H43 · buy-one-save-two
- **Family:** exact optimisation with a two-layer control.
- **What it does:** Adds ONE new in-sector mask `x` buildable in one gate from signals the
  block may use, then asks for the block in `|B|−2`. Net −1 ⇒ 87.
- **Twist:** two-layer control — a per-block solve at `|B|` with `x` free, plus the sibling
  witness at `|B|` without `x`.
- **Measured (re-tallied; the RESULT.md says "still accumulating"):** **4,926 candidate
  instances, verdict `UNSAT_at_nB_minus_2` on every one. 0 hits. The sweep is COMPLETE and
  empty.**
- **Cost:** ~1.2 s per instance.
- **Phase-2:** **keeper as a template, closed as a question** for this matrix.

### H44 · topologically-convex block closure (a specification-bug fix)
- **Family:** instance repair / structural proof.
- **What it does:** Fixes a specification bug. A gate `o` can simultaneously be a *descendant*
  of one block gate and an *operand* of another (no cycle — `o` just sits between them in
  topological order), and `AVAIL` excludes descendants, so the instance cannot express the
  circuit's own program. The repair is the interval closure
  `B* = B ∪ {g : g is a descendant of B and an ancestor of B}`, with a written proof of
  sufficiency.
- **Measured:** diagnostic over all 112 blocks, no solver, seconds: sector 0 has 10 blocks
  with a descendant-operand and 10 uncovered raw → **0 uncovered after the closure.** All 14
  sector-0 blocks then decided `OPTIMAL_AT_nB` with the control firing **14/14**, total cost
  1,315 s. In sectors 1/3/4 the coverage failure survives the closure, confirming those need
  dimension 12.
- **Code:** `experiments/e7_push/code/convex.py`.
- **Generality:** **CIRCUIT-GENERIC** (it is a DAG property).
- **Phase-2:** **keeper.** General lesson: *a "free structural control" that tests the wrong
  predicate is worse than no control.*

### H45 · sector tightness theorem
- **Family:** exact oracle applied to records.
- **What it does:** For every (record, sector), reconstructs the sector's exact interface
  (inputs it consumes from outside, values it exports) and asks the oracle for `w_k − 1`.
- **Measured:** **48/48 UNSAT.** Every sector program of every record is exactly minimal for
  its interface ⇒ **an 87 requires renegotiating *interfaces*, not improving programs.** The
  cleanest "nothing is stackable in place" statement in the corpus.
- **Phase-2:** keeper.
- **COMPLETED (2026-08-29):** this entry was one of the nine Appendix A skeletons. The full schema-conformant entry, written from primary sources by `wrapup/day2/CATALOG_AUDIT.md` §3, is **Appendix A §A·6**.

### H46 · sector block reoptimisation (the superseded predecessor)
- **Family:** exact oracle applied to records.
- **Measured here:** **58 of 112 blocks run** (23 `ctl=OK` exhaustive negatives, 35
  `NOT-COVERED`); coverage by sector `S0:3, S1:14, S2:3, S3:14, S4:14, S5:3, S6:3, S7:4`; one
  log is **0 bytes**.
- **Closed downstream:** **3 of the 23 negatives were *vacuous*** (in-sector optimum strictly
  exceeds `|B|`); after H44's convex-closure repair, **70 of 112 blocks are decided exactly
  optimal with a live control, 0 hits**, and the surviving surface is 35 blocks in sectors
  1/3/4 needing dimension 12.
- **Phase-2:** **superseded-by-H41/H44. Do not re-run.**

### H47 · hint-suppression resolve (never inherit a floor you have not proved)
- **Family:** SAT bound verification.
- **What it does:** The generator was being handed ten hard-coded lower bounds ("this block
  needs at least N gates"), read off an earlier lane, which made it start searching at N and
  therefore **never test anything below N**. This drops the floors and re-solves every block
  from its own counting bound upward. It does not look for a better circuit; it looks for
  whether the claimed floor was ever *proved*.
- **Measured:** **all ten blocks return exactly their hint**, and the **57 gate-levels that
  had never been tested in this repository's history are now proved UNSAT.** `U1 = 6` proved
  twice from two different mask sets (k=4 UNSAT 15.75 s, k=5 UNSAT 20.08 s) — which **closes
  the audit's rank-1 "if U1 is 5 the model prices 87"**, negatively. The instrument's
  machine-checked floor for the shipped configuration rises **70 → 88**. And the *hint's key*
  is measurably wrong: at `rec_88at7` (a three-value commitment) `B37` prices **3, not the
  hinted 4**, so **that configuration's price is 88, not the published 89** — with a verified
  circuit on disk to prove it.
- **Cost:** **3,513 wall-seconds / 14,053 core-seconds ≈ 3.90 core-hours**, 4 cores peak.
- **Generality:** CIRCUIT-GENERIC as a discipline.
- **Phase-2:** **keeper.** Four core-hours converted a claimed floor into a proved one and
  corrected a published number.

### H48 · optimist / pessimist bound DP + floor sensitivity sweep
- **Family:** class lower bound over a partial corpus.
- **What it does:** Runs the class DP twice — once with each unpriced cell at its proven
  *upper* bound (pessimist: reproduces the published class optimum, the control) and once at
  its proven *lower* bound (optimist: a valid class lower bound). Adds a floor-sensitivity
  sweep to see how far the family can go.
- **Measured:** **the optimist shortcut is DEAD, and not narrowly.** Pessimist returns
  **exactly 91** with a σ table 11× larger than the original — the control fires. Optimist
  returns **58**. Floor sweep: 4→58, 5→66, 6→74, 7→82, 8→90, 9→91 — **exactly +8 per unit of
  floor** (one per sector), so ≥ 88 needs a universal per-sector floor of 8, and **553
  measured exact cells sit at σ = 6**, so floor 8 is refuted *by measurement*. Honest bracket:
  class optimum ∈ **[58, 91]**, not "= 91". Corpus completion priced at **≥ 2,000 CPU-h**
  (201,976 instances).
- **Generality:** MIXED (corpus MC-specific; the two-mode + sensitivity pattern is generic).
- **Phase-2:** **keeper as a pattern** (run the DP in both modes and sweep the floor *before*
  buying corpus); the specific route is a **dead-end**.

### H49 · targeted cell pricing (lazy / cutting-plane)
- **Family:** partial exact pricing; twist on H48.
- **What it does:** Identifies which unpriced cells the optimist chain actually leans on and
  solves exactly just those, then re-runs the DP.
- **Measured:** five cells priced at 9 / 9 / 10 / ≥10 / ≥10 against a floor of 4 —
  **individual cells are cheap to lift, and even a timed-out `slp_opt` run pays** (the UNSAT
  ladder it completed is a machine-checked lower bound). **But installing all five moves the
  bound 58 → 58**: the argmin simply relocates to another of the 271,109 unpriced cells.
  **~2,900 solver-seconds bought zero gates.**
- **Phase-2:** **dead-end for this corpus** — but *"a timeout is a bracket, not a
  refutation"* is a keeper and is applied everywhere else.

### H50 · interface-level curve (separate the interface cap from the depth cap)
- **Family:** parametric exact sweep. **The sharpest finding of fleet wave 4.**
- **What it does:** Separates two effects everything else conflates — sweeps the *arrival
  level of the committed interface value* independently of the total depth cap, for producer
  and consumer separately, and finds where the two curves cross.
- **Measured:** **`U07`'s price is a function of the INTERFACE cap alone; the total depth cap
  does not enter it.** `Q1` at level 2 → 14 gates, level 3 → 13, level ≥ 4 → 12 — and **13 is
  13 at `D=5`, `D=6` and `D=7` alike.** The consumer runs the other way: `U1 = 6` with `Q1` at
  level ≤ 3, **≥ 9 at level 4**. So the R01 depth-5 optimum is `l1=3: 13+6 = 19` against `18`
  uncapped — **the whole depth-5 premium of the region is +1 gate and it sits entirely at the
  tap-1 interface level.** The depth-axis analogue of H23's gate-axis conservation law.
- **Consequence:** *depth is substantially a property of the CELL.* The identical model, code
  and depth cap give **88 at the 88@5 cell and 90 at the 88@7 cell** — the sharpest available
  statement of why the five known 88s sit at five different depths.
- **Code:** `fleet4/laneDEPTH/code/{curves,frontier}.py`.
- **Phase-2:** **keeper, and UNFINISHED** — the lane's own #2 next step ("run the interface-
  level curve at every tap, at both cells") is a 3-parameter search with minute-scale solves
  and was never run.

### H51 · regression suite (subprocess-isolated, thrice-verified)
- **Family:** control / reproducibility for a generator.
- **What it does:** Each row is a fresh `generate.py` subprocess run twice (cold, then warm)
  and then verified a *third* time by a separately launched `verify_circuit.py`. Rows are
  rebuilt from the append-only ledger, not from prose.
- **Measured:** 9/9 rows hit their asked count and verified VALID. Notable rows: the 88
  uncapped emits at depth **7**, not the depth 10 an earlier lane reported — same
  configuration, same block prices, different minimal witness, and depth is a property of the
  mask *set*; the 89 control must and does honestly report 89.
- **Phase-2:** **keeper.**

---
# Family I — Lower-bound machinery

Proving a *floor*. The refereed state at close is **56 ≤ L(M) ≤ 88**. Exactly one
technique family in the whole project clears 88, and it bounds the
cancellation-free cost only (I12).

### I1 · depth-3 structure theorem + complete model
- **Family:** exact structural enumeration.
- **What it does:** Proves that in any depth-≤3 circuit every target sits at level exactly 3
  (weight 5 or 7 > 2² = 4), no target feeds another gate, level-1 gates have weight exactly 2,
  and level-2 gates weight 3 or 4 — hence `N_depth3 = 32 + min(|L1| + |L2|)` over a **finite**
  space: **7,897 candidate level-2 masks, 496 candidate edges, 6,120 decompositions.**
- **Twist:** the only place in the project where the search space is finite and completely
  enumerable.
- **Measured:** the three counts were derived twice independently and agree exactly.
- **Code:** `campaign_87/d3_model/{d3_theory,d3model}.py`, `campaign_87/wave6_2026-08-11/lower_bound/model3.py`.
- **Generality:** **MC-HARDCODED but mechanically portable** — the theorem needs only the
  target weight profile; for another matrix, recompute the weight bound `2^ℓ` and re-enumerate.
- **Phase-2:** keeper — the foundation of the campaign's only unconditional theorem.

### I2 · certified LP dual bound with valid inequalities (`N_depth3 ≥ 80`)
- **Family:** LP relaxation + exact rational certificate.
- **What it does:** Writes an integer-coefficient system `A p ≥ b` whose every row is a proved
  theorem about depth-3 circuits (cuts C1–C10), obtains a dual vector `u ≥ 0` with `Aᵀu ≤ c`
  from HiGHS, **rounds it to denominator 10¹² and re-verifies feasibility in exact integer
  arithmetic** before reporting. Weak duality then gives the bound with nothing floating-point
  in the claim.
- **Twist:** the certificate (`cert_depth3.json`, **23,450 nonzero duals**) is re-checkable in
  one command independently of the solver, of scipy, and of the session.
- **Measured:** `u·b = 47.597998… ⇒ |L1|+|L2| ≥ 48 ⇒ **N_depth3 ≥ 80**`. Bracket
  `80 ≤ N_depth3 ≤ 97`. Without the cuts the LP is 29.19 (⇒62); an earlier uncertified CP-SAT
  dual was 34 (⇒66). C8 alone is worth +1.05. **Three mandatory controls all PASS** (the
  verified 97@3 circuit maps into the model at cost exactly 65; none of the 23,405 cuts is
  violated by it; none of the 72,830 LP rows is violated). By-products, also certified: every
  depth-3 circuit has ≥18 level-1 gates; only `E ∈ {19, 20}` can reach 48, and both sit at LP
  value **exactly 48.0**, so no further cutting can raise the bound — everything above is
  integer reasoning. SCIP 10 reproduces the root LP to 7 digits through a different code path.
- **Cost:** minutes for the certificate; the branch profile is 42–45 s per E.
- **Code:** `campaign_87/wave6_2026-08-11/lower_bound/{model3,cuts,build_lp,certify,branch_certify,node_probe,control_primal,control_cuts,control_lp}.py`.
- **Generality:** MC-HARDCODED (the cuts are theorems about *this* weight profile) — but the
  *recipe* (complete structural model → valid inequalities → exact rational dual → mandatory
  primal control) is fully generic.
- **Phase-2:** **keeper — the single most valuable artifact in the campaign_87 slice.** It is
  the only unconditional result that campaign owns.

### I3 · target-subset exact MILP lifting (the abandoned ≥63 ladder)
- **Family:** lower bound by relaxation, **integer** reasoning not LP.
- **What it does:** Picks a subset of k targets, solves the exact depth-3 model restricted to
  them to proven optimality, and lifts `min|P|+|Q| + 32` into a global bound (dropping targets
  is a valid relaxation).
- **Measured:** whole run **17 minutes on one core**: 32 (trivial) → **52** (k=6, 19 s) → 53 →
  **59** (k=8, 129 s) → **63** (k=10, 155 s), every rung `PROVEN OPTIMAL`. **The log ends there
  with no k=12 attempt and no explanatory note.**
- **Code:** `campaign_87/d3_model/d3bound.py`.
- **Phase-2:** **keeper — a live, cheap, unfinished route** (it is exactly the integer
  reasoning wave 6 concluded is the only way past 80).

### I4 · edge-floor relaxation + ladder
- **Family:** lower bound sub-relaxation.
- **What it does:** Drops the level-2 counting entirely and bounds only the edge structure
  (**496 real variables instead of 29,180**), then composes an edge floor F with the certified
  per-E profile: `N_depth3 ≥ 32 + min_{E≥F} LP_E`.
- **Measured:** F=21→81, 23→82, 25→84, **27→85 (its ceiling, since the verified 97@3 uses 27
  edges)**. Status: cap 20 undecided at 1,200 s (CP-SAT); cap 19 UNKNOWN after 10,800 s.
  Established floor F = 18 ⇒ `N_depth3 ≥ 80`.
- **Phase-2:** keeper but **capped** — it cannot on its own reach the 56 needed for the
  depth-4 theorem.

### I5 · column-zeroing bound (Theorem A) → `L(M) ≥ 51`
- **Family:** gate-elimination combinatorics, entirely solver-free.
- **What it does:** Picks a column set `K` such that `M|_K` has 32 pairwise-distinct rows of
  weight ≥ 2; zeroing each of the `32−|K|` outside columns provably kills ≥ 1 gate, and the
  surviving matrix still needs 32. Bound = `(32−|K|) + 32`.
- **Twist:** thirteen integers and a five-line argument.
- **Measured:** **`L(M) ≥ 51`** with `K = [2,8,10,13,15,18,20,21,22,23,24,29,31]`. **51 is the
  EXACT optimum of the technique**, upgraded from MILP-asserted to exhaustively proved: **all
  462,411,532 subsets of [32] of size ≤ 12 enumerated in C.** On **Mᵀ the same technique gives
  only 49**, so the transposed frame is *worse* as a proof frame.
- **Cost:** verification is instant (`python3 verify_bound.py`, stdlib, 1 s).
- **Generality:** **CIRCUIT-GENERIC and explicitly so — which is its own stated ceiling.** The
  argument nowhere uses the fact that this matrix is MixColumns; on a random invertible 32×32
  it would give a *larger* number. Retargeting to `aes_inv_mixcolumns` is a **one-line change**
  and would likely give a **better** bound, since inv-MixColumns rows are denser.
- **Phase-2:** **keeper — publishable, unpublished.**
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** Two defects, neither numerical (every figure verifies, and `sum(C(32,k), k=1..12) = 462,411,532` checks exactly). (a) This entry has **no `Code:` field** — it names `verify_bound.py` bare; the path is `beat88/understanding/u3_lowerbound/verify_bound.py`. (b) "Retargeting to `aes_inv_mixcolumns` is a **one-line change**" is not supported by that file: `:51` `for k, c in enumerate([2,3,1,1])` is the one line, but `:86-88` are unconditional tripwires (`assert rw.count(5)==20 and rw.count(7)==12`, `assert sum(rw)==184`) that abort on any other matrix, and `:22-24` hardcode MixColumns certificates. The script only *checks* a given `K` and does no search, so a new bound needs the ≤12-subset enumeration (`maxq.c`) re-run — four lines plus a 4.6 × 10⁸-subset enumeration.

### I6 · minE forced-extras (Theorem B) → `L(M) ≥ 54`
- **Family:** bounded exhaustive realizability search.
- **What it does:** At a keep-set `K`, computes `minE_K` = the fewest extra masks that must be
  adjoined to the restricted rows to make them realizable over the kept inputs. Bound =
  `(32−|K|) + 32 + minE_K`.
- **Twist vs I5:** the only place in either bound lane where **more compute buys more bound.**
- **Measured:** `L(M) ≥ 54` at `|K| = 14`; a second, largely-disjoint keep-set gives 54
  independently. **The phase transition is sharp:** `minE = 0` at `|K| ≤ 13` and `≥ 4` at
  `|K| = 14` — and `minE = 0` was verified on **all 72** `|K|=13` keep-sets with `q = 32`, so
  **Theorem B provably adds nothing at the Theorem-A optimum.** Verified by **three independent
  implementations** (pruned Python, unpruned Python, a referee's C searcher validated against
  brute force on 700 random small instances).
- **Cost:** depth 3 = **7.0 M nodes / 286 s** on one core in Python (a 30k-node / 1.2 s variant
  already gives ≥ 53). Depth 4 (→ 55) is ~10⁹–10¹⁰ nodes: out of reach in Python, *"plausible in
  C, ~hours on 2 cores"*.
- **Context number worth carrying:** the *counting* bound for this dimension is **73–74** —
  almost every invertible 32×32 needs ≥ 74 — and the record 88 sits above it. **That is why
  "prove 88 optimal" is not reachable by counting.**
- **Phase-2:** **keeper** — by its lane's own assessment, the highest bound-per-hour work left.

### I7 · adaptive gate elimination (Lemma F + Theorem N) → `L(M) ≥ 56` (refereed)
- **Family:** proof-side lower bound — the project's hardest currency.
- **What it does:** `L(M) ≥ m + min_K [(32−|K|) + 32 + e_K]` over a family of keep-sets covering
  every m-subset, run **adaptively** with a fresh optimal SLP at every stage; `e_K` = minimum
  extra values ("minE") by unpruned exhaustive search.
- **Measured:** **L(M) ≥ 55, then L(M) ≥ 56 unconditional and refereed** — the first improvement
  over 54 in project history. Cert 5 gives `minE ≥ 5` by **two** independent exhaustions
  (**9.43e10 and 4.75e9 nodes, 511/511 branches each**). 11 of 12 certificates die at depth 4
  (`minE = 4` exactly, with witnesses). Searcher validation **400/400** against brute force;
  determinism across reboot node-for-node.
  **Refereed state of the problem: `56 ≤ L(M) ≤ 88`.**
- **Cost:** depth-3 ≈ 2e8 nodes / 15 s in C; depth-4 = pod-scale; depth-5 estimated **40–80
  pod-days** unpruned.
- **Code:** `atlas/thinktank/proofside_code/{mc.py,mine.c,ub.c,checkwit.py,admis.py,enum14.py,exact80.sh}`.
- **Generality:** **CIRCUIT-GENERIC** — stated for any 0/1 matrix with distinct non-zero columns
  and a symmetry group.
- **Incarnations:** `beat88:u3-column-zeroing` (51) → `beat88:u3-minE-forced-extras` (54) →
  `atlas_misc:adaptive-gate-elimination` (56, refereed).
- **Phase-2:** **keeper. This is the slice's hardest currency.**

### I8 · keep-set layer enumeration (why the elimination family stops)
- **Family:** proof-side — enumerate the *whole layer* instead of sampling certificates.
- **Measured:** minimum admissible `|K| = 13` exactly, exactly **72** admissible 13-sets, all
  with `minE = 0`. **The entire `|K| = 14` layer is CLOSED at 56**: all **33,548** admissible
  14-sets enumerated, `minE ≤ 5` for 33,542 of them, the six exceptions resolved exactly. The
  `m = 2` branch is dead by complete census (caps at 54) — and the regularity is *explained*:
  all 640 keep-sets with jam ≥ 12 contain the full hub orbit.
- **The sharpest diagnostic in the atlas slice:** `L(M) − L(M|_K) = 88 − 37 = 51` gates for 18
  columns = **2.83 per column**, while the bound pays 19 — and **51 − 19 = 32 = 88 − 56.**
  Cascade is *exactly zero* in all five 88s. **So the entire remaining gap is the price of a
  column, and the missing 0.9 per column is re-optimisation value — untouched by any elimination
  lemma.**
- **Phase-2:** **keeper — it says exactly why the elimination family stops at 56.**

### I9 · quotient counting lemma (floor transfer by projection)
- **Family:** structural lower bound.
- **What it does:** For a region module `M = lines ⊗ T` and any subspace `W` of the line space,
  projecting along `W⊗T` maps any valid program for the region to a valid program for the
  quotient instance (delete zero and duplicate projections). So `L(region) ≥ L(π_W-instance)`
  unconditionally, and the quotient instances are dimension 4 or 8 — decidable — where the
  region is 12 or 16 and is not.
- **Twist:** it is a *floor transfer*, not a search accelerant; all its solves are one or two
  dimensions below the cost wall.
- **Measured:** R01 (floor to beat 15): `qk2 = 13`, `qk3 = 11`, `qk5 = 10` EXACT;
  `qk4 (kill-d7) ≥ 14`. **Reading: killing the d7 line — deleting the C7 import currency — is
  what makes the region expensive.** Honest ceiling stated in the lane: `max_W L(π_W)` — no LP
  combination beats the max, because a full-line-support gate is visible to every quotient.
  Measured level curve for `qk4`: k=11: 58 s, k=12: 689 s, k=13: 17,469 s — **×10–25 per level**;
  k=14 landed after write-up at **1008/1008 cubes, 484,561 CPU-s.**
- **Code:** `fleet1/laneB_regionbounds/code/{quotients,qsolve,mklemmas,pricing}.py`.
- **Generality:** **CIRCUIT-GENERIC** wherever the target module has a tensor structure
  `lines ⊗ T`. **The most portable lower-bound tool in fleet1–4.**
- **Phase-2:** **keeper** — it certifies `R01 ≥ 14` at ~1/10 the compute of the direct route.

### I10 · quotient exact form (a strict strengthening of I9)
- **Family:** structural theorem.
- **What it does:** Partitions the gates by their value under the projection:
  `N = #{v ∈ W⊗T} + #{distinct nonzero projections} + #{collisions} ≥ z_W + m_W + col_W`. Also
  proves there is **no composition theorem to find**: for `W1 ∩ W2 = 0` the pair map is
  injective on values, so the joint relaxation *is* the original problem.
- **Measured:** on lane B's own record-universal 22-gate R01 witness the exact form is worth
  **21 of 22** (at `W = span{d1}`) against lane B's transferred **14**. Control fired:
  `z_{qk2} = 4` independently reproduces lane B's own line-support profile "4 gates pure d1".
- **Actionable hand-off (never executed):** add `z_W + col_W ≤ k − m_W` for **every** kernel
  simultaneously to the fortified region CNF. At `k = 15` that forces `z+col ≤ 1` under qk4,
  `≤ 2` under qk2, `≤ 2` under qk6, `≤ 3` under qk7 *at the same time*, while the record spends
  2, 8, 0, 2 there. Lane B's "tight mode" (I11) is the special case `z_W + col_W = 0` for one
  `W`. **Refereed — CONFIRMED.**
- **Phase-2:** **keeper, and UNSPENT.**

### I11 · lemma-fortified CNF (tight mode)
- **Family:** SAT encoding augmentation; twist on I9.
- **What it does:** Injects "at least `m` of the `k` gates project nonzero under `π_W`" as
  cardinality clauses into the region CNF — a proven consequence, so UNSAT stays a theorem and
  every witness survives. **Tight mode:** when the level being decided equals a lemma bound,
  every gate's projection must be nonzero, distinct and new, so the projected program is itself
  minimal.
- **Measured:** **SOUND but MARGINAL as an accelerant.** Matched-cube measurement at k=13, same
  host: fortified/plain = **0.82× (~1.2× faster)**. Static soundness control: the verified
  22-gate witness satisfies every lemma. Dynamic planted control: SAT with verified witness at
  `k = bound`. Two instrument bugs found in review and logged (vacuous cardinality counter —
  never unsound; an EXACT-overclaim at capped kmax — erratum).
- **Phase-2:** **keeper with the honest caveat** — the value is arithmetic floor transfer, not
  solver speed. I10 is the strictly stronger version that was never run.

### I12 · laminar price certificate → `L_cf(M) ≥ 92`, and its LP ceiling ★
- **Family:** Lagrangian dual → exact-integer, solver-free certificate. **The only bound family
  in the project above 88.**
- **What it does:** In a cancellation-free SLP every target is built as a *laminar hierarchy*
  over its support. Assign integer prices `n[t][m] ≥ 0` over a denominator `D`, with the column
  constraint `Σ_t n[t][m] ≤ D` (a mask is one gate however many targets want it). Then
  `B = (1/D)·Σ_t min_H Σ_{S∈H} n[t][mask(S)]`, each inner term a `2^{w_t}`-state subset DP over
  ≤ 128 states.
- **Twist — why it is the only bound that clears 88:** soundness needs three lines and **no
  optimality of the price table**, and it is the **only quantity in the programme whose endpoint
  values are not fixed by `184 → 32`** — exactly the escape I20 demanded.
- **Measured, as a lineage:**
  * `cert_exact.json` (D = 10⁶) → `B = 90.80458` → **`L_cf ≥ 91`**.
  * `cert_exact_v2.json` (D = 10⁷) → `B = **91.0019782**` → **`L_cf ≥ 92`**, refereed. The
    improvement came from replacing a proportional rescale with a **true Euclidean projection**
    onto `{x ≥ 0, Σ_t x ≤ 1}` plus a Polyak step with the exactly-constant subgradient norm
    `‖g‖² = Σ_t(w_t − 1) = 152`.
  * **Recognised as a finite LP** (~5.9 k variables, ~18.6 k constraints), solved with GLOP and
    re-certified with an exactified rational table and a `Fraction` DP: `G*(λ)` at 19 values of
    λ, all `OPTIMAL`; every value **beats** the corresponding table on disk (gains +0.179 to
    +0.413). `G*` is piecewise linear: `= 32·λ` for λ ≤ 5/2, then slope 12, saturating at
    **`B* = 91.409884`** from λ = 7/2. The certified constant improves to **`B = 91.4098776`**
    (exact rational `114262347/1250000`, solver-free re-check), independently rebuilt by a
    referee with its own Check 1 and its own DP (`Check 1 max column sum = 1.0000000, exactly
    tight, FEASIBLE`). Per-weight constants:
    `δ_{2..7} = 0, 0.9999998, 1.9912788, 1.5872092, 2.0429066, 2.5044082` — these feed I30.
  * **THE CAP — why this line is closed:** the LP **optimum** is `B* = 91.409884`. The two
    thresholds anyone wanted — `B > 92` (⇒ `L_cf ≥ 93`) and `B > 91.9738 = 87 + 2·δ₇` (⇒
    `|A*| ≥ 3` for every 87 unconditionally) — **both lie above the LP optimum and are therefore
    unreachable by optimising this LP at all, symmetric or not.** The symmetry lever is worth
    **+0.0000003**: the optimum is already ρ-symmetric to seven places. *"Do not fund a
    ρ-symmetric price optimisation."* The one remaining purchase is a **certified rational dual**
    closing `91.4098776 ≤ B* ≤ 91.409884`, scoped at ~1 session.
  * Bonus results from the LP form: the **unconditional, solver-free dichotomy — for every
    XOR-SLP for M, `|C| ≥ 58` or `κ ≥ 16`** (eight times stronger, in the regime that matters,
    than the standing refereed `κ ≥ 2`); and a family ceiling — **no price table and no λ can
    ever prove `n ≥ 57` for a circuit with `κ ≥ 22`** (rigorous), or `κ ≥ 20` given the LP
    optimum — and the records have `κ = 18..28`, so **the exchange rate is capped below the
    record's own regime, by proof.** `H_p(λ) = G*(λ)` to the last digit at five values of λ, so
    the `A`-choice integrality is worth **exactly zero**.
- **Cost:** verify in **~2 s, stdlib only, solver-free**. Generation: `push.py 20000 10000000`
  ≈ 25 min. GLOP 60–120 s per λ on 8 threads; 19 λ values.
- **Code:** `beat88/understanding/u6_*/push.py` (ascent);
  `fleet7/laneUNCOND/code/{lp_g,bstar,dich,dich2,hp}.py` (exact LP);
  `experiments/e17_pure/REF_CONTRA/code/{ref2_bound,ref3_pairs,ref4_controls,ref5_uncond}.py`
  (independent rebuild); banked table `fleet7/laneUNCOND/results/bstar/nostop_lp_cert_4_1.json`.
- **Generality:** **CIRCUIT-GENERIC machinery, MC-HARDCODED certificate.** The hierarchy lemma,
  the DP and the pricing all take an arbitrary target set; the mask universe (1,648 masks here)
  is *derived* per matrix by Lemma 1, not assumed. Retargeting: rebuild `TARGETS`, re-run the
  ascent, re-verify. **The most portable high-value method in the campaign.**
- **Incarnations:** `beat88:u6-laminar-price-certificate` (91.0019782) →
  `fleet5_8:exchange-rate LP solved exactly` (91.4098776, `B* = 91.409884`) →
  `experiments_late:certificate-price-LP` (refereed, the cap).
- **Phase-2:** **keeper as a bound generator, dead-end as an upgrade path.** Refereed,
  publishable, unpublished.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** Two defects, neither load-bearing; the verdict stands and I had the verifier re-run (`CHECK 1 ok` / `CHECK 2 ok: numerator = 910019782  B = 91.0019782` / `=> L_cfree(M) >= 92`, **wall 0.18 s**, so "~2 s" is conservative and true). (a) Arithmetic: the entry writes "`B > 91.9738 = 87 + 2·δ₇`" three lines after listing `δ₇ = 2.5044082` — under the listed constants that sum is **92.0088164**. The 91.9738 comes from the *superseded* `pbar` table's `δ₇ = 2.4868874`. Both thresholds sit above 91.409884, so no verdict changes, but the identity as printed is false. (b) The Code list omits the actual Tier-1 verifier, `beat88/understanding/u6_spec87/verify_cert.py` — which is also **not** stdlib-only: `:19-21` hardcodes an absolute path into this box's repo (`sys.path.insert(0,'/home/joebachir20/…/pipeline')`), so the "solver-free 2 s check" aborts on any other machine. Fix that line before porting.

### I13 · two-price λ lift → `U ≥ 2` cancelling gates
- **Family:** certificate arithmetic on top of I12.
- **What it does:** Two price families and a rational multiplier give
  `U ≥ (G(λ) − n)/(λ − 1)`, where `U` is the number of cancelling gates.
- **Measured:** `G(7/2) = 90.996546` → **`U ≥ 2` at n = 87 and at n = 88**; `U ≥ 1` at n = 90.
  All eight certificate numerators re-derived to the digit by an independent exact-integer
  checker over a separately rebuilt `M`. **The lane originally left this in floating point and
  the referee caught it.**
  **An exact NEGATIVE recorded so the compute is not spent again:** `U ≥ 3` is **not reachable
  by this instrument.** The measured curve `G(λ)` over λ = 2.85 … 3.75 tops the ratio
  `(G−87)/(λ−1)` out at **1.599**. Cause of death: per-target hierarchy costs **cannot be
  equalised** because the masks targets buy are shared, and the column constraints bind long
  before costs level. *"`U ≥ 3` needs a structurally better relaxation, not a better λ and not
  more ascent."*
- **Phase-2:** **keeper**, and the `U ≥ 3` negative is a **keeper as a dead-end certificate.**

### I14 · cancellation weight budget (Theorem P1)
- **Family:** structural theorem linking two complexity measures.
- **What it does:** For each target, unrolls its cone stopping at inputs and at cancelling gates
  ("maximal clean tree"); the leaf supports partition the target's support and the internal
  nodes are distinct clean gates. Refining each non-singleton leaf by a fixed hierarchy turns
  any SLP into a hierarchy family, so `|C| ≥ L_cf(M) − Σ_{m∈A*}(wt(m) − 2)`.
- **Twist:** the first theorem in the programme that makes `L_cf(M) ≥ 92` a bound on `L(M)` at
  all — previously it was explicitly fenced off.
- **Measured:** every 88 must spend a cancellation weight budget of **≥ 4**, every 87 **≥ 5**.
  Verified on all 11 wired circuits on disk; the records **overspend by a factor of ~19–22**
  (75/83/90/86/83 against a required 4) — the honest measure of how lossy the crude refinement
  is. **Refereed — CONFIRMED** (proof rebuilt from scratch, non-circular against `L_cf ≥ 92`).
- **Code:** `fleet2/laneP_proof/code/{cflib,measure}.py`.
- **Generality:** **CIRCUIT-GENERIC** — needs only `L_cf` for the target matrix.
- **Phase-2:** **keeper.**

### I15 · residual hierarchy certificate (Theorem P2 + exactification)
- **Family:** certificate / LP over hierarchies.
- **What it does:** Splits every gate three ways — `n = κ + |counted| + Y` (κ = cancelling,
  counted = clean gates with an all-clean path to a target, Y = "dedicated" clean gates that
  exist only to feed cancellation) — then prices `counted` by a partial-hierarchy DP with the
  cancelling masks as free leaves. Re-optimises the price table *per circuit* by projected
  subgradient ascent, then **exactifies** it into integers over `D = 10⁷` so a standalone
  verifier can re-check it.
- **Measured:** instrument control reproduces the published table **to the digit** (numerator
  `910019782`, universe 1648, `c`-distribution `{1:1396,2:204,3:44,6:4}`); an independent ascent
  from scratch reaches 91.02172 vs the published 91.0019782. **On `88@7` the chain evaluates to
  exactly 88.000 (κ=26, Y=27, B=35.000 = |counted| — the residual LP is integral there).** For
  `88@7` and `88@5` the chain proves `n ≥ 88` **in exact integers, solver-free** — *"this
  circuit cannot be improved to 87 without changing its cancellation apparatus"* is now
  machine-checkable. **The first optimality-strength statement about a record circuit in this
  programme.**
- **Cost:** 6,000 subgradient iterations per circuit, minutes.
- **Code:** `fleet2/laneP_proof/code/{resid,exactify,verify_exact,localize}.py`.
- **Generality:** CIRCUIT-GENERIC given a cancellation-free certificate.
- **Phase-2:** **keeper.**

### I16 · LP dual-gap recovery (settle a gap without more iterations)
- **Family:** obstruction proof from the dual side.
- **What it does:** Settles "is this gap a true integrality gap or an undertrained ascent?"
  **without more iterations**: the LP's dual is combinatorial (a distribution over each target's
  partial hierarchies), so averaging the ascent's argmin hierarchies over its last quarter yields
  a *feasible dual* and hence an upper bound on the LP value.
- **Measured:** on `88@5fs`, `|counted| = 39` but the recovered dual evaluates to **34.0000** →
  **proven gap ≥ 5** → **no certificate of this family can push the chain above 83.000**,
  whatever the missing lemma says. A referee recomputed its own mixture dual in exact `Fraction`
  arithmetic: **exactly 34.** **Control fired:** the same instrument returns ~0 gap on four
  circuits and pins `88@7` at exactly 35.00 = `|counted|`.
- **`CONFLICT`:** `fleet6/laneTOOL2` later reports the "integrality gap ≥ 5" as a
  **misattribution** with true gap ≤ 0.5351. Both stand in their own reports; see Appendix B #2.
- **Consequence (a correction to the whole programme's standing plan):** the route needs **two**
  new tools, not one — the named span-cone-union lemma *and* an **integral** (non-LP) bound for
  the residual hierarchy-union problem. Two planning documents name only the first.
- **Phase-2:** **keeper — the highest-value negative in fleet1–4.** It stops a pod-scale
  certificate campaign that could not have worked.

### I17 · integral residual bound Φ (built, calibrated, and it killed its own chain)
- **Family:** proof-side / CP-SAT + reductions.
- **What it does:** Computes an integral residual quantity `Φ(A)` — a minimum cancellation-free
  program covering a demand set — exactly by CP-SAT, with two reductions (R1, R2) that make it
  seconds instead of hours, and feeds it into the chain `|C| ≥ κ + Y + Φ(A)`.
- **Measured:** calibration test 1 PASSED; **calibration test 2 FAILED, and the failure is a
  theorem** — `Φ(A*) ≤ 34` on 88@5fs proves the P2/T1 chain cannot reach `L(M) ≥ 84`. It also
  showed the previously refereed "integrality gap ≥ 5" was a **misattribution** (true gap ≤
  0.5351). The tool changes no number on any record: `Φ(A*) = ⌈B(A*)⌉` on all five record 88s.
  Replacement chain **T4 is exact `= n` on 9 of 9 circuits**. The load-bearing negative was
  independently rebuilt three ways (own fixpoint checker, explicit hierarchies, separate HiGHS
  MILP).
- **Code:** `fleet6/laneTOOL2/code/{t2lib,phi2,c2b_calibrate,w1_witness,x2_repaired}.py`,
  `verify1/` (22 files).
- **Generality:** CIRCUIT-GENERIC (it is a statement about SLPs, not about MC).
- **Phase-2:** **dead-end for bounds, keeper as a calibrated instrument.** Its own §7 says "do
  not fund the integral residual bound"; but `phi2.py` + R1/R2 is the machinery a `G_int(3)`
  attempt would need.

### I18 · U1 construction (retiring a bound by proving it is the original problem)
- **Family:** hand-reasoning theorem with a machine-checked constructive half.
- **What it does:** Proves that the "unconditional form" of the T4 bound, once written with the
  acyclicity constraint a real circuit forces, is an **equality** with `L(M)` — by exhibiting a
  construction that turns any admissible stratified configuration into a circuit of that size.
- **Twist:** it is a *retirement* method — it converts "this bound might be improvable" into
  "improving this bound is the original problem".
- **Measured:** **REFEREED — CONFIRMED, both halves**, by an adversarial agent barred from
  reading `code/` that wrote its own MixColumns rebuild, extractor, rebuilder and exact-`L`
  solver. The construction ran through the repo oracle **10/10 `VERDICT: VALID`**. One real
  defect found and fixed: the construction needs an explicit **earliest-stratum tie-break**. The
  referee also tested anti-circularity: 68 MixColumns circuits from **88 to 4,621 gates**, and 20
  small instances whose optimal circuits have `L = 3..8` — the optimal configuration has value
  exactly `L` in all 20, and 500 random admissible configurations produced **zero** with value
  `< L`.
- **Generality:** CIRCUIT-GENERIC (a statement about XOR-SLPs).
- **Phase-2:** **keeper — a route retired with a reason.** Do not fund "make T4 unconditional"
  for any circuit; it is that circuit's own problem.

### I19 · U2 collapse witness (a negative that is an explicit positive object)
- **Family:** explicit-object refutation.
- **What it does:** Refutes a claim by *building the object*, not by failing to find one: a
  perfect matching of the 32 targets into 16 pairs with all three overlap conditions, giving
  `|A| = 48` and an empty demand set.
- **Measured:** value **48 < 88**, **11/11 definitional checks, no solver**, pre-registered.
  **REFEREED — CONFIRMED and STRENGTHENED** (the referee proved 48 *optimal* in that family by a
  forest argument). Corrects another lane's headline, which is **false as a global statement.**
- **Phase-2:** **keeper.** The template: **a negative that is an explicit positive object cannot
  be vacuous.**

### I20 · counting-LP as a method ceiling (the uniformity theorem)
- **Family:** LP duality over a basis of cut functionals. **The only instrument that prices a
  whole class of proof techniques instead of trying one.**
- **What it does:** Builds a basis of symmetric cut functionals and solves
  `max ⟨u, swing⟩ s.t. ⟨u, Δφ_k⟩ ≤ 1` over every observed per-gate increment vector. The optimum
  is the best bound *any* linear counting argument over that basis could ever give.
- **Measured:** 23-functional basis over **44,738 distinct increment vectors** of 2.32 M gates →
  **n ≥ 37.85.** The control recovers the trivial bound exactly. An enriched 86-dimensional basis
  over 43,947 increment vectors → **n ≥ 46.21.** *"Multiplying the basis by 3.7× bought 18 %,
  against a factor of 1.9 still needed."*
- **The uniformity theorem (why this matters):** any cut functional whose endpoints are fixed by
  `M` yields a bound of exactly `88 · (mean Δφ / max Δφ)` — **hence never above 88**, and equal
  to 88 only if the increment is constant on every gate of every 88. Measured uniformity ratio:
  **0.43–0.53.** **Design consequence, the single most actionable sentence in the understanding
  half:** *introduce a quantity whose endpoint values are NOT determined by `184 → 32`.* I12's
  price certificate is the one such quantity in the whole programme, and it is the only one that
  clears 88.
- **Generality:** CIRCUIT-GENERIC machinery (a theorem about the shape of counting arguments).
- **Phase-2:** **keeper — the most transferable idea in the understanding half.**

### I21 · cut-trajectory economy (conservation laws over telescoping functionals)
- **Family:** conservation laws.
- **What it does:** Defines the cut `A_k = inputs ∪ {g₀…g_{k−1}}`, runs a backward demand pass
  over the suffix, and checks the cut identity at every one of the `n+1` cuts; then measures
  expression mass `L`, factorisation area `V`, and cancellation debt `D = V − 184` along the
  whole trajectory.
- **Measured:** corpus **26,222 verified circuits / 2.32 M gates.** Laws verified with **0
  violations**: `L₀ = 184`, `Lₙ = 32`, `V₀ = Vₙ = 184`, `D_k ≥ 0` at every cut, `L ≥ 152`. **The
  one genuine conservation law is `V`** — area returns to 184, an invariant of the AES matrix
  rather than of the circuit. **The efficiency inversion:** the greedy-108 sits *exactly on the
  floor* `L = 152` with debt 0 at every cut — and is the **worst** circuit measured; `W = L − 152`
  runs 0 → 18 → 52 → 60 → **92** down the 108 → 97 → 92 → 89 → 88 ladder. At *fixed depth* the
  premise inverts outright: 89-gate circuits serve as many or more outputs per gate as 88s from
  depth 7 up (AUC(89>88) = 0.78 for `s̄`, **0.87 for `V`**), and the correlation of `s̄` with gate
  count at depth 8 is **+0.26 — the wrong sign for the whole premise.**
- **Phase-2:** **keeper.**

### I22 · heavy-corner rank floors (U5-2 / U5-3)
- **Family:** rank-based lower bound from a linear projection.
- **Measured:** every circuit contains **≥ 19 route-A heavy gates**, hence **≥ 27 gates with
  nonzero heavy part** — stated for arbitrary SLPs, checked **204/204, 0 violations**, measured
  slack 13–22. **Explicit non-compounding result, recorded so nobody re-derives it:**
  `27 + 12 = 39 < 54`, and it does **not** add to Theorem B, because in a 14-column projection
  `rank(P₀) = 23` collapses to ≤ 14. Also: the matrix's only heavy-world identity
  `t₇ ⊕ t₁₅ ⊕ t₂₃ ⊕ t₃₁ = Λ = 0x80808080` — unique, established exhaustively (536,154 subsets of
  size ≤ 7 tested; `rank(P₀) = 23`, kernel 1-dimensional); all 276 pairwise XORs of `P₀` are
  distinct (a Sidon set); **no heavy target is the XOR of two free masks.**
- **Phase-2:** keeper (the identity especially — it mechanically explains Λ's measured frozenness,
  J33).

### I23 · cap-table analysis (classify every bound technique and give each a ceiling)
- **Family:** structural survey of the whole lower-bound programme.
- **What it does:** Classifies every unconditional lower-bound technique in the repository as a
  *reduction*, a *charge*, or a *certificate*, and gives each family a proved or measured ceiling.
- **Measured:** Lemma P ~40; class-rank 32; heavy-corner ledger 52; edge counting 33 (**refuted by
  the records**, which evaluate to 31–33); linear-counting LP 46.2; Theorem-N chain 56 today,
  ≤ 73 under `C_0`; tower rung 51; backward identity **circular** (`a = F − 64 + c + 2d`
  identically — a change of variables carrying zero information). **Exactly one family is above
  88: `L_cf(M) ≥ 92`.** Plus a proved payment-budget theorem: every adaptive chain from `M` to
  `M|_{K5}` pays ≤ 51 total, so a uniform per-stage payment of 3 is **refuted unconditionally by
  the record circuit**, and the `C_c` family stops at 73 even at `c = 0`.
- **Phase-2:** **keeper — read this before funding any bound work.** Its conclusion ("the whole
  optimality question is exactly *what does cancellation buy?*") is what the next wave executed.
- **COMPLETED (2026-08-29):** this entry was one of the nine Appendix A skeletons. The full schema-conformant entry, written from primary sources by `wrapup/day2/CATALOG_AUDIT.md` §3, is **Appendix A §A·5**.

### I24 · obstruction hunt (parity / counting / invariant arguments, systematically killed)
- **Family:** lower-bound theory, executed and mostly refuted.
- **What it does:** Enumerates the candidate classes of obstruction against an 87 and kills or
  scopes each with a machine check.
- **Measured, all machine-checked:**
  * **T0 (PROVEN):** orbit counting on the *set* of circuits can prove *existence* but never
    *non-existence* — the empty set satisfies every Burnside congruence. **Any obstruction must
    be an invariant of a *single* circuit.**
  * **P1/P2 (PROVEN, conditional):** any 87 whose mask set is exactly ρ²-closed contains an
    **odd** number of ρ²-fixed masks; the ρ version has a mod-4 refinement. At 88 both are vacuous.
  * **Weight/cancellation accounting (REFUTED constructively):** the weight-flow identity
    `w(t) = P(t) − 2Σμ_h(t)c_h` is exactly true, machine-verified on all 8 evidence circuits —
    and *scale-free*. A verified **87-gate circuit with MixColumns' exact weight profile (20×5 +
    12×7 = 184), 32 independent outputs, all gates alive, 41 cancelling** exists on disk (it is
    **not** a MixColumns circuit, by design) — so **no weight-accounting invariant can exclude 87.**
  * **Rank/matroid (KILLED):** the target matroid is the free matroid on 32 elements, identical
    for the identity matrix. The odd-weight-forest bound caps near 35.
  * **Symmetry group (COMPUTED, KILLED):** `Aut(M) = {(σ,τ) : PMQ = M}` has order **exactly 4 =
    ⟨ρ⟩**; the transpose-twisted part is **empty** (M is not permutation-equivalent to Mᵀ). Full
    count-preserving symmetry is `⟨ρ⟩ × {id, trace-dual}`, order 8.
  * **Move-invariant homomorphisms (KILLED empirically):** six candidate Z/2–Z/4 invariants tested
    against **380,034 pairs** of harvested 88s at symmetric difference exactly 2 — every one is
    flipped by a single ±0 move (46,260 to 277,921 flips each).
- **Code:** `campaign_87/wave5_2026-08-04/burn/obstruction/t1_equivariance.py … t5_plateau_scan.py`.
- **Phase-2:** **keeper — the highest theory-per-byte directory in the campaign_87 slice (80 KB).**
  It tells a successor exactly which lower-bound ideas not to re-propose, with a machine-checked
  reason for each.

### I25 · class-rank localization + edge-counting bound (two families, both capped)
- **Family:** proof-side.
- **Measured:** class-rank localization **exists and provably caps at exactly 32** (8 target
  classes × 4). Edge counting `Σφ − |U|` is **refuted by the records themselves** — it evaluates
  to 31–33 on the very circuits it must bound, because every 88 has 3–6 inputs of fanout exactly 1.
- **Phase-2:** **dead-end, and valuable as such** — two whole families provably capped below 56.
- **COMPLETED (2026-08-29):** this entry was one of the nine Appendix A skeletons. The full schema-conformant entry, written from primary sources by `wrapup/day2/CATALOG_AUDIT.md` §3, is **Appendix A §A·4**.

### I26 · `C_c` fanout-1 conjecture + census
- **Family:** proof-side conjecture with its parameter measured on real optima first.
- **What it does:** Conjectures that any optimal SLP has ≤ c live inputs of fanout 1; payoff
  `L(M) ≥ 73 − c`.
- **Measured:** census over **1,197 distinct verified circuits including 94 distinct 88-states**:
  `z ≤ 11` over all 1,197 and `z ≤ 8` over all 94 optima. `c ≤ 16` alone would beat the trivial
  record bound. **z is largest exactly at the frontier** (mean 5.47 at 88, 1.93 at 91). The
  class-level form was **killed** by an explicit counterexample family (M5), and the whole route
  was later **closed by identity/self-defeat** in the e17 campaign.
- **Generality:** stated matrix-agnostically — **CIRCUIT-GENERIC.**
- **Phase-2:** closed; but the *census technique* and the discipline "**measure the conjecture's
  parameter on real optima before funding the proof**" are keepers.

### I27 · candidate-lemma falsification (cheap refutation before proof)
- **Family:** cheap refutation.
- **What it does:** States the natural candidate lemmas and tests each against every wired circuit
  on disk. Seconds of compute.
- **Measured:** **four dead on arrival**, each with an explicit witness: Y1 "every cancelling gate
  has an off-hierarchy operand" fails on 9 of 11 (**the one most people would try first**); Y2
  `Y ≥ κ` fails on 4; Y4 fails on 9; Y5 fails on 5. Y3 `Y ≥ κ − 5` survives 11/11 but yields a
  vacuous bound. **Each failure names the next candidate**: the surviving shape is a *counting*
  lemma over the union of cones, not a *charging* lemma over individual gates.
- **Code:** `fleet2/laneP_proof/code/ycand.py`.
- **Phase-2:** **keeper — run this before any proof attempt.** Cost: seconds. Value: months.

### I28 · adversarial re-wiring census (the cheapest falsification instrument)
- **Family:** falsification by census.
- **What it does:** Takes a large census of known circuits and re-wires each many ways,
  recomputing a claimed invariant, to find the true worst case.
- **Measured:** **refuted Y3 (`Y ≥ κ − 5`)**: `min(Y − κ) = −6` over **3,254 census circuits, 43
  witnesses**. Pre-registered. The corrected constant `Y ≥ κ − 6` prices at `L(M) ≥ 58`, beating
  the refereed 56 — but it is a measurement over 88s, not a theorem, and one further `−7` costs a
  gate off the 58. **3,254 circuits × 16 wirings ran in 132.5 s.**
- **Code:** `fleet6/laneTOOL2/code/y1_census.py`.
- **Phase-2:** **keeper — the cheapest falsification instrument in fleet5–8.** Both lanes
  recommend re-pointing it at a different statistic (`|Cl \ U|`) as the next cheap experiment;
  **nobody did.**

### I29 · Y-ledger impossibility (closing a conjecture by self-defeat)
- **Family:** proof by counterexample + self-defeat.
- **What it does:** Attacks `Y ≥ κ − c`, the only conjecture on the board with a measured constant
  and a price (`c = 6` pays `L(M) ≥ 58`).
- **Measured:** **there is no such `c`.** As stated over every SLP, `Y ≥ α·κ − c` is **false for
  every `α > 0` and every `c`**, and stays false for *trim* SLPs — six explicit oracle-VALID
  witnesses reaching `Y − κ = −399`. Narrowed to the size regime where the pricing needs it, the
  hypothesis is **logically equivalent to its own conclusion**: the inequality that converts a
  Y-lemma of slope `α` into `L(M) ≥ G(1+α) − c` is the same inequality that proves
  `Y − α·κ ≤ n − G(1+α)` unconditionally. What replaces it is Theorem Y1, the **first upper bound
  on `Y`** in the programme, plus a general impossibility theorem at every slope. A referee
  CONFIRMED Y1–Y5 and the arithmetic, but **REFUTED as stated** the lane's own recommendation to
  strike `Y ≥ κ − 6` from the board.
- **Code:** `experiments/e17_pure/laneY/code/` + `ylib.py`; referee `REF_ALGEBRA/code/`.
- **Phase-2:** **dead-end, definitively closed** — with the by-product that the closure is itself
  a theorem.

### I30 · anatomy theorem (assume-87 structural derivation) ★
- **Family:** assume-87 structural derivation.
- **What it does:** Assumes `H87` (a minimum-size SLP of `n ≤ 87` gates exists) and derives a
  conjunction of forced properties, each conjunct labelled with its hypotheses and its grade
  (a = proved / b = proved-modulo-a-named-lemma / c = conjectured).
- **The theorem, in one sentence:**
  > Any **minimum-size** 87-gate SLP for MixColumns has 32 finals and 55 middles with pairwise
  > distinct masks, no dead gate, no final built from two targets, at least two cancelling gates,
  > at least two distinct cancelling-gate masks appearing as leaves of maximal clean trees, a
  > cancellation weight budget of at least 5 spread over a weight profile satisfying
  > `Σ_w a_w · δ_w ≥ 4.4098776`, no budget contribution at all from weight-2 cancelling leaves,
  > `Y ≤ 2.5044082·κ − 4.4098776`, and — if its cancelling apparatus is as small as the arithmetic
  > permits (`|A*| = 2`, forcing `κ = 2` and `Y = 0`) — **a cancelling gate whose output *is* one
  > of the twelve weight-7 MixColumns rows.**
- **The referee-confirmed asymmetric fact (A11):** *"A10 is gate-count-ASYMMETRIC. At `n = 88` the
  same computation admits ten profiles and only **7,362 of 19,490** admissible pairs contain a
  weight-7 target row — the statement is false at 88."* Grade **(a)**, exhaustive recount. At
  `n = 87` it is **475/475 = 100 %** under the banked table (profiles `{4,7}` 63, `{6,7}` 346,
  `{7,7}` 66). **This is the first gate-count-asymmetric fact in the programme** — the first
  statement that distinguishes 87 from 88 rather than describing the plateau. Its caveat is equally
  load-bearing: it is **not** an 87 detector, and dropping the `|A*| = 2` hypothesis repeats the
  project's `U1` error.
  (An earlier draft of the `n=88` numeral was 8,562, corrected by the referee to **7,362** — an
  error that ran *against* the claimant and made the asymmetry stronger.)
- **Cost:** seconds per script, 1 core.
- **Code:** `experiments/e17_pure/laneCONTRA/code/{spectrum,perweight,close,final}.py`; referee
  rebuild `experiments/e17_pure/REF_CONTRA/code/ref1..ref5*.py`.
- **Generality:** MC-HARDCODED (a theorem about `M`), but the *shape* (certificate table →
  weight-profile inequality → forced anatomy) ports.
- **Phase-2:** **keeper — the spine of the lower-bound dossier**, and the thing to show an
  external correspondent.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — the starred asymmetry drops its own load-bearing caveat.** Every number verifies (n=88: 19,490 pairs / 7,362 weight-7 / 8,562 any-target, with the 8,562→7,362 correction recorded; n=87: 475 admissible pairs = 63+346+66, all with a weight-7 row). But `experiments/e17_pure/DOSSIER.md:651` states A11 **with** a caveat this entry deletes: *"These two numerals are computed under `pbar`; the referee did not publish an `n = 88` recount under the banked table. At `n = 87` the two tables give 738 and 475 pairs respectively … a successor restating A11 should re-run the `n = 88` branch under the banked table."* This entry restates A11 as "**the same computation**" at n=88 versus "475/475 = 100 % **under the banked table**" at n=87 — two different price tables presented as one computation. For the fact this file calls "the first gate-count-asymmetric fact", that conditionality must travel with it. **Fix: restore the caveat, or fund the n=88 recount under the banked table.**

### I31 · spec-87 joint satisfiability (why "prove 88 optimal" was abandoned)
- **Family:** consistency check on a whole proof programme.
- **What it does:** Takes every proven constraint on an 87 and asks whether they jointly pinch.
- **Measured:** **the certified joint floor of the entire proven hard spec is 54, not 88 — slack
  33 gates. There is no pinch and no optimality proof.** `Σ drop = 152`, `Σ ρ = 152` and
  `Σ serve ≥ 152` are all the *same* `152 = wt(M) − 32` in three coordinates, and the third is an
  **inequality**, never an equality (measured `Σ serve = 218` on the 88@5, 244 on the 88@6; only
  the greedy-108 sits at 152). The containment law caps **only the first gate.**
- **Phase-2:** **keeper** — this is the document that closed the optimality route.

### I32 · Boyar–Peralta drop profile (a bound route superseded by its by-products)
- **Family:** rigorous potential accounting.
- **Measured:** `max drop ≤ 6` is **FALSE** — **27 gates in the corpus at drop 7/8/9**,
  re-verified by an independent non-incremental second pass. Drop-9 witness: gate 43 buying
  `0x80808080`, Φ 71 → 62. **Of the 27 gates with drop ≥ 7, 25 buy `0x80808080`; only three
  distinct masks in the whole corpus can push a gate past 6.** Bound arithmetic: universal caps
  degrade monotonically with corpus size (88 → 82 → 76 → 66 → 62); provable today is
  `⌈152/9⌉ = 17`, below trivial. Standing instruction: *"do not re-derive maxdrop ≤ 6. It is
  false."*
- **Phase-2:** **superseded as a bound route** but **keeper for its by-products** — the Λ
  discovery and the drop-0 gate population both came out of it.

### I33 · transposition principle (a whole direction closed by an identity)
- **Family:** structural theorem + artifact transfer.
- **What it does:** Applies the transposition principle to a MixColumns SLP to obtain an SLP for
  `Mᵀ`, and measures whether the transposed circuit can be cheaper (the hope was that reused
  outputs would develop slack).
- **Measured:** **it cannot, ever.** `gates(T) = Σ_v (f_v + e_v − 1) = a + n − m`, so for
  `m = n = 32`, **`gates(T) = a` identically** — the handshake lemma forces `Σ f_v = 2a` and
  distinct outputs force `Σ e_v = n`. Verified on all five 88s (reused-output count varies 2→6,
  every feeding column constant). Produced 5 new artifacts
  `T_mixcolumns_88gates_depth{5,5fs,6,7,8}.json`, oracle-VALID against a `Mᵀ` oracle, plus two
  hand 107s.
- **Code:** `experiments/e13_hand87/laneT/{transpose,accounting,verify_T,fromscratch_T}.py`.
- **Generality:** **CIRCUIT-GENERIC** (the identity holds for any XOR SLP).
- **Phase-2:** **dead end, and valuably so** — it closes the whole transposition *cost* direction
  by identity, one line, for any target circuit. (The transposed *frame* is still useful: see J7.)

---

# Family J — Structural analysis of circuits and populations

What the circuits are actually made of, and what the population of 88s looks like.

### J1 · min-depth schedule (level-BFS / ASAP) and its deployments
- **Family:** scheduling — no search.
- **What it does:** Depth is a property of the *schedule*, not the mask set. Level-BFS (level `L`
  = exactly the masks that are an XOR of two masks of level `< L`) gives the provable minimum
  level of every mask, hence the depth-optimal schedule for a fixed set. Applied to a *mask set*
  it turns "the depth we measured on our transcription" into "the depth that mask set is forced
  to have".
- **Measured, across four deployments:**
  * **Control fires the right way:** the eight record circuits are already depth-optimal for
    their own mask sets and come back unchanged. It *does* find a full level of slack in the
    theory-compiled 91: **5 → 4**, verified `gates=91 depth=4 32/32 VALID` — equal to the best
    91@4 on disk. A naive 116-mask scheme: 4 → 3.
  * **Disk-wide audit:** **2 of 38,711 distinct mask sets reschedule shallower**, and one of the
    two is a genuine frontier point (a *third* independent 91@4 lineage). **Maximum observed
    rescheduling gain across the whole sweep is exactly 1 level** — which is what licenses
    excluding 1.16 M depth-≥7 88s from the frontier claim. (Enumerated 1,820,576 JSON files.)
  * **Forced-depth on published circuits:** one external 88's mask set → depth **7** forced (3 of
    32 output bits at 7); another published circuit → **9** forced; this repo's from-scratch 88 @
    5 → depth **5** forced (11 of 32 output bits, rows 1,7,12,13,17,18,21,25,27,28,31); the 88 @
    6 → rows 1/11/17/25. **Three distinct depth-obstruction patterns.**
  * **Plateau depth sampling:** 1,200 uniformly sampled harvest circuits give depths
    `{7:1, 8:111, 9:490, 10:543, 11:55}` — **mode 10, and depth 5 occurs zero times.** The 14
    known records sit at `{5:2, 6:1, 7:3, 8:6, 9:2}`. **The record is a depth record disguised as
    a gate record**; a successor sampling the 88-plateau for an 87 is sampling a depth-9-to-10
    population.
  * Assembly order is worth **exactly zero** — for all 12 circuits measured, as-written depth
    equals the level-BFS minimum of the same mask set.
- **Code:** `pipeline/engines.py:relax`; `fleet2/laneG_generator/code/build.py::min_depth_schedule`
  (copied into laneF4 and laneDEPTH); `fleet8/unified/code/assemble.py:min_depth_schedule`;
  `experiments/e4_depth/code/{mindepth,analyze}.py`; `fleet9/laneENUM/code/sample.py`.
- **Generality:** **CIRCUIT-GENERIC, zero adaptation needed.**
- **Incarnations:** `records_repo:asap-depth-forcing` · `fleet1_4:min-depth-rescheduler` ·
  `fleet5_8:min-depth-schedule` · `experiments_early:mindepth-reschedule-sweep` ·
  `fleet9_12:minimum-depth-schedule-sampling`.
- **Phase-2:** **keeper — free gates-for-nothing at depth**, and the only depth argument in the
  project that is a theorem rather than a measurement. Run the disk-wide audit once per corpus.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** Minor over-claim on "**zero adaptation needed**": `pipeline/engines.py:99` (`dep = [0]*32 + [INF]*(na-32)`) and `fleet8/unified/code/assemble.py:94` (`inputs = [1 << i for i in range(32)]`) both hardcode 32 inputs. Generic across circuits on 32 inputs; not across dimensions. (This entry's own three code citations are correct and all exist; the broken path is in starter-kit row 14, corrected there.)

### J2 · level-BFS depth diagnosis (attribute the critical path to blocks)
- **Family:** structural analysis, no solver.
- **What it does:** Level-BFS gives the provable minimum level of every mask; each mask is
  attributed to a block by the line support of its value, so the critical path is annotated block
  by block.
- **Measured:** **every critical path crosses at most three block tags and is dominated by ONE
  block's internal span.** A theory-generated 88 burns levels 2..8 on a nine-mask `U07`; `88@7`
  has `U3` spanning six; shallow circuits have no block spanning more than four. **Diagnosis: the
  depth is burnt inside block programs**, because the exact oracle minimises gates and depth never
  enters its objective.
- **Code:** `fleet4/laneDEPTH/code/diag.py`.
- **Phase-2:** **keeper.** Cheap, solver-free, and it aimed the whole lane.

### J3 · free-move orbit closure (and its second-generation tripwired rewrite)
- **Family:** plateau geometry / exhaustive enumeration.
- **What it does:** Defines two gate-count-preserving "free moves" — **re-association** (changes
  exactly one gate mask) and **re-parenting** (changes none) — and enumerates the closed connected
  component of a given 88 under them, checking every state for a collapse (a duplicate mask, a
  dead gate, or a minted mask that already exists — each of which would be an 87). It is the only
  method that *partitions* the plateau rather than sampling it.
- **Measured, gen 1 (e14):** the five studied 88s lie in **five pairwise-distinct CLOSED
  components of 729 / 2,187 / 10,935 / 26,730 / 4,212 states = 44,793**, all five closures
  independently re-enumerated by an audit lane; pairwise distinctness settled by **direct set
  intersection on all ten pairs**. **Zero free 87s** in any of them.
- **Measured, gen 2 (e16, mask-space, ~8× faster, with three tripwires T1 duplicate / T2 dead gate
  / T3 re-association collision):** **333,396 states across the eight F-point components, all
  eight CLOSED by exhaustion** (F1 91,368 / F2 19,683 / F3 729 / F4 2,187 / F5 2,916 / F6 17,496 /
  F7 243 / F8 198,774), **4,856,598 re-association sites and 436,914 re-parentings probed, T1 = T2
  = T3 = 0 everywhere**, minimum reachable gate count 88 at every one. Added to gen 1:
  **378,189 enumerated states across thirteen closed orbits, zero sub-88 states.** No component
  contains any other anchor at any rotation → **the thirteen studied 88s lie in thirteen
  pairwise-distinct closed orbits.** Free by-product: running T2/T3 over gen 1's own 44,793 states
  gives 0 and 0.
- **Five controls, one of which failed first:** CONTROL 1 reproduced all five banked cardinalities
  exactly; CONTROL 2 showed broken engines fail (no-re-association → 1 state vs 729; no acyclicity
  guard → 378 CLOSED=False); CONTROL 3 is pointwise identity with gen 1's code **imported
  verbatim**, 8/8 states identical on five components including F1; CONTROL 4 fired both tripwires
  on planted 89-gate structure end-to-end through the oracle; CONTROL 5 wrote 12 random banked
  states per component and oracled them — **96/96 VALID, gate counts seen `[88]`.** The first
  version of CONTROL 2 was *worthless and said so* and is kept in the ledger because that is the
  informative part.
- **Cost:** gen 2 — **2,336 s wall** across eight components, 2 processes, `nice -n 15`.
- **`CONFLICT`:** a separate quotient-graph cartography lane reports "true gauge-component" sizes
  of **112,833 for 88@7 and 59,697 for the third family**, against 26,730 and 4,212 here. The move
  classes differ; see Appendix B #4.
- **Code:** `experiments/e14_plateau87/closure.py`;
  `experiments/e16_lastwish/laneFPOINT/{fpclose,fprun,control_fp,xval,tripwire_control,bankcheck}.py`.
- **Generality:** **CIRCUIT-GENERIC** — both moves are defined on any XOR DAG; only the validity
  oracle is MC-specific.
- **Phase-2:** **keeper (gen 2 supersedes gen 1)** — but carrying its own binding guard: **both
  moves preserve gate count, so if an 87 exists it lies in none of these components by
  construction. These tables describe the 88 plateau; they are not evidence about 87.**

### J4 · `D_fine` metric + farthest-point extraction
- **Family:** structural metric / population census.
- **What it does:** `D_fine` = half-L1 distance between gate-mask multisets, minimised over the
  four byte rotations; re-association is Lipschitz-1 under it and re-parenting is exactly
  invariant, so `D_fine` values are **certified lower bounds on free-move distance**.
  Farthest-point extraction then picks the on-disk 88s maximally remote from everything already
  studied.
- **Measured:** of **18,355 valid 88s** in the repo corpus (17,283 distinct mask multisets),
  **16,536 — 90.1 % — sit at `D_fine ≥ 21` from all five studied circuits.** Extraction names
  eight points F1–F8, all oracle-VALID. The full 13×13 matrix: minimum pairwise over all 13 =
  **21**, attained at a **known-known** pair; minimum among the eight F-points = 38; minimum from
  every known = 39. *"The eight new points are further from each other and from the knowns than
  the knowns are from one another."*
- **Code:** `experiments/e14_plateau87/basis/{dfine,topmetric,census_filter}.py`;
  `experiments/e15_campaign3/tools/{dfine_pop,farpoints,dfine_scan}.py`.
- **Generality:** CIRCUIT-GENERIC apart from the rotation group (`Aut(M)`-specific).
- **Phase-2:** **keeper — the only frame instrument of e14 that survived attack.** Everything else
  (8 anatomy rows, 4 DAG statistics) died.

### J5 · gauge canonicalisation + inflation check
- **Family:** measurement hygiene, mandatory.
- **What it does:** Canonicalises sampled states under the project's gauge group and reports how
  many "distinct" frozensets collapse to one canonical orbit.
- **Measured:** at the 88@5, **~75× inflation** — 668 distinct frozensets collapsed to 1 canon in
  a 75-state sample. At the 89@5, inflation ~1.02. So **every "N distinct states visited" claim at
  the record is a rotation count, not an exploration count.** At larger scale: the plateau closes
  at **2,187 = 3⁷** / **729 = 3⁶**, and one harvest file of 518,253 lines collapses to **≤ 9 gauge
  components (~100× overcount)**. **Standing rule adopted:** `canon` is a dedup bucket key only;
  any distinctness/escape claim must classify against the component BFS, and membership is
  `PopIndex.find()`, never a truncated core hash (a real bug: a 128-bit core hash stored in a
  `uint64` array silently kept the low 64 bits, and a "1,137 novel orbits" claim was really **1**).
- **Code:** `experiments/e1_regions/code/{gauge_check,gauge_check88}.py`;
  `beat88/methods/shared/gauge.py`.
- **Generality:** MIXED (needs a gauge group for the target circuit).
- **Phase-2:** **keeper — a mandatory sanity filter on any exploration-rate claim.**

### J6 · exact automorphism computation + equivariance proof
- **Family:** structural proof — the first thing to run on a new matrix.
- **What it does:** Three independent routes to the same object: (a) complete backtracking over
  bit-permutations `π` of the 32 input coordinates with `π(TARGETS) = TARGETS`; (b) 1-WL colour
  refinement to isolate planes then a complete pruned DFS over input-bit permutations; (c)
  proving the byte-rotation ρ is a genuine automorphism (GF(2)-linear, order 4, permutes inputs
  and targets) and therefore that gate count, validity, minimum depth and neighbourhood structure
  are all ρ-invariant — so checking one representative per orbit is **complete** and any
  exhaustive sweep can divide its work by 4.
- **Measured:** **|Aut| = 4, proved in 0.1 s** — exactly `{ρ⁰,ρ¹,ρ²,ρ³}`; the WL route confirms
  the stabiliser has order **EXACTLY 4**. The real centraliser in GL(32,2) is ≥255× larger
  (bytewise GF(2⁸) multiplication commutes with M, verified), but **zero** of the 254 non-trivial
  scalars is a coordinate permutation, and only a coordinate permutation can be imposed as
  mask-set invariance. **Consequence: the tempting "87 ≡ 0 mod 3, 88 ≡ 1 mod 3" order-3 sector
  does not exist — closed by proof, not by search.**
  **The equivariance half does not stop at algebra:** it re-runs the actual historical
  irreducibility instrument (byte-copied read-only) on C and on ρC window by window, requiring
  every intermediate to correspond — **4,580 windows compared, 0 mismatches**; 50,000 random
  linearity/order checks; and it carries a **sensitivity control that can fail**: the same
  comparison with two *non*-automorphisms returns **300/300 mismatches**, so the zero is a
  measurement rather than a tautology. Consequence: a historical "105,801 states k≤2-swept" figure
  certifies **423,204** circuits, and the 88-census is exactly one representative per orbit (**0
  ρ-fixed circuits in 54,889**).
- **Cost:** 0.1 s for `Aut`; minutes for the equivariance run.
- **Code:** `experiments/e3b_fresh/code/{symgf,symgf_check}.py`;
  `experiments/e14_plateau87/{sym,edgesym,splice,splice2}.py`;
  `fleet9/laneENUM/code/rho_equivariance.py` + `rho_equiv_ctrl.py`.
- **Generality:** **CIRCUIT-GENERIC** as a method; the inverse matrix also commutes with byte
  rotation, so it should transfer directly.
- **Incarnations:** `experiments_early:automorphism-group-proof (SYMGF)` ·
  `experiments_late:wl-plane-isolation-symmetry-proof` ·
  `fleet9_12:symmetry-equivariance-proof-and-sensitivity-control` ·
  `campaign_87:obstruction hunt` (symmetry-group row).
- **Phase-2:** **keeper, top of the list.** A free 4× on every exhaustive sweep, and it
  retroactively quadrupled the value of work already done. (Its by-products include the chimeric
  88s `chimA`/`chimE` — oracle-VALID 88s outside their parents' closed components.)
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — the cited code does not contain the WL route.** Every figure verifies. But route (b) is cited to `experiments/e14_plateau87/{sym,edgesym,splice,splice2}.py` and **none of those contains 1-WL or the DFS**: `sym.py` is a 34-line mask/rotation comparison, `edgesym.py` a 23-line generator edge-symmetry probe, `splice*.py` the chimera builders. The real code is **`experiments/e14_plateau87/auto.py`** (`# 1-WL colour refinement on the bipartite graph`, `def refine(ci,co)`) and **`experiments/e14_plateau87/auto2.py`** (plane-wise `24^8` DFS), written up at `FS88_DECODE.md:525-538`. Route (a) is correctly cited. Second: `sym.py:20-21` and `edgesym.py:7` hardcode `/home/joebachir20/xor_ui/aes_mc_records/circuits/` — a path **outside this repo** — so neither is reproducible from a clone.

### J7 · transpose duality and the transposed frame
- **Family:** structural identity + a change of frame.
- **What it does:** Reverses every edge of the SLP DAG. `XOR-count(M) = XOR-count(Mᵀ)` — reversing
  a dead-gate-free 2-input-XOR DAG computes the transpose at exactly the same gate count. Reading
  masks in the bit basis instead of the trace-dual basis gives a *different* ladder with better
  structure.
- **Measured:** verified 88→88→88 round trips on all five known 88 families, both 89s, the 92 and
  the 97; 300 perturbed circuits, 0 failures; all 11 repository circuits transpose to same-count
  VALID `Mᵀ` circuits and back. **Depth is NOT preserved** (5→6, 5→7, 4→8, 3→5, 8→11).
  Structurally `Mᵀ = (I₄⊗B)·PMP·(I₄⊗B)⁻¹` with B the Gram matrix of the trace form — a genuine
  basis change, not a permutation, which is why the optimum is identical but the landscape is not.
  Only **11.1 % of periphery masks** are shared between a circuit and its transpose, so k=2 window
  collections are ~89 % disjoint. Result: **8,481 Mᵀ states, 13,705,916 exact window decisions, 22
  complete k≤3 shells, zero reducible.** Frame structure: the transposed ladder is a **connected
  path 0-1-…-7** with one exotic element, versus the forward frame's broken path plus three
  diagonals; seven of eight transposed sectors are raw-free; **zero diagonals in any transposed
  record**; glue 65/65 in one mechanism; off-ladder bill drops from 9–17 to 4–8;
  `r(mask weight, co-mask weight) = −0.62..−0.73` — **old search instruments rank `Mᵀ` by a nearly
  opposite statistic.**
- **Scientific value:** it **kills the "primal neighbourhoods were the problem" hypothesis** — the
  barrier is structural, not an artifact of move shape. Wave 6 also *hunted* in `Mᵀ` and measured
  the null at n=27 and n=14 per arm — no reachability advantage; and `Mᵀ` **descends significantly
  worse (p = 1.2 × 10⁻⁴)**.
- **⚠ Hazard:** with k dead gates the transpose is *smaller by exactly k*, so an untrimmed 89
  appears to become an 88. **Trim first, always.**
- **Code:** `campaign_87/dual_transpose/{transpose,verify_duality}.py`, `campaign_87/wave6_2026-08-11/transpose/`;
  `atlas/thinktank/transposed/{tframe,tring,census,bias,localize,verify_mt,run_transpose}.py`.
- **Generality:** **CIRCUIT-GENERIC — Tellegen applies to every linear circuit.**
- **Phase-2:** keeper — cheap, proved, doubles the neighbourhood supply for free. **Note: nobody
  ever ran a proper *search* on `Mᵀ` despite the measured r ≈ −0.7.**

### J8 · mask-Jaccard family test (calibrated)
- **Family:** structural analysis / distinctness.
- **What it does:** Measures the overlap of two circuits' internal mask sets and reports shared
  count + Jaccard; a threshold of **0.7** is used repo-wide for "same family".
- **Twist:** it is used *calibrated* — two independently published circuits by different authors
  score Jaccard **0.553**, *more* overlap than this repo's 88 @ 7 has with one of them (0.530).
  The calibration is what licenses "an overlap of this size is what independent constructions for
  this map look like".
- **Measured:** every pairwise number the repo quotes — 0.735 (the highest here), 0.530, 0.544,
  0.455, 0.386, 0.362, 0.323, 0.319.
- **Phase-2:** **superseded-for-distinctness by J3/J4**, but keep it for *communication* — it is
  far cheaper to explain to a reader.

### J9 · novelty ruler (neutral-baseline weighted Jaccard)
- **Family:** measurement.
- **What it does:** Builds a *neutral* corpus of MixColumns constructions (**6,171 documents
  across 7 strata**: BP, tree, reuse, Paar, Paar-soft, published, anneal3 roots) and contrasts
  mask document-frequency there against the project's own harvest, producing an IDF weight table
  so "how novel is this circuit" is measured against constructions **the project did not make**.
- **Measured:** **402 of 911 harvest periphery masks (44.1 %) are never produced by any neutral
  construction.** Family threshold calibrated at wJ ≥ 0.46 (error 0.0, margin 0.144) and plain
  J ≥ 0.60. Then the finding that matters: **76.4 % of 42,763 harvested 88s sit inside a known
  family**, and the only lanes producing off-family material are the from-scratch constructors.
- **Code:** `campaign_87/novelty/{novelty,measure}.py`, `baseline/{gen_baseline,calibrate}.py`.
- **Phase-2:** **keeper — without it, "new family" claims are unfalsifiable.**

### J10 · population spread measurement
- **Family:** structural analysis.
- **What it does:** Reads every 88-gate harvest on disk, dedupes to distinct mask states, and
  measures pairwise symmetric difference over a sample.
- **Measured:** **78,281 distinct 88-mask states**, pairwise distance median 86 / p99 170 / max
  172 (of a possible 176) — yet built from a union of only **916 distinct masks**. Combined with
  the cage result: the search *covers* a wide region by destroy-and-rebuild but cannot *move*
  through it at constant gate count.
- **Phase-2:** keeper.

### J11 · corpus-wide degeneracy census (find the coordinate nothing occupies)
- **Family:** structural analysis at full corpus scale.
- **What it does:** Streams **every** 88-gate population file in the repo (460 files, 3.9 GB) and
  measures structural coordinates of every non-target mask.
- **Measured:** **3,280,541 distinct 88-gate circuits are built from 3,172 distinct words.**
  Families, basins, Jaccard distance and depth are all rewiring of one small dictionary.
  Degeneracy scan: mask weight ranges 2–18 (not degenerate), lanes 1–5 (not degenerate), but
  **`|odd(m)| ∈ {0,1,2}, never 3** — 0 occurrences in ~184 M mask slots. Histogram:
  `0: 113,366,654 / 1: 67,470,645 / 2: 3,881,285 / 3+: 0`.
- **Cost:** 393 s.
- **Code:** `experiments/e_oddlane3/census.py`.
- **Generality:** CIRCUIT-GENERIC in method, MC-specific in the coordinate definitions.
- **Phase-2:** **keeper, top tier.** *"Measure what no circuit we ever found does, then force a
  search into that region"* is the most original framing in the experiments slice, and it is
  cheap. Its follow-through is J14b (feature pinning).

### J12 · fusion-surplus / plane-abstraction census
- **Family:** structural analysis at population scale.
- **What it does:** Computes a plane-level "fusion surplus" for every harvested 88 and asks
  whether the plateau is one structure.
- **Measured:** over **434,125 distinct verified 88 mask-sets**, surplus spans **16..30** (mean
  21.68) across **13,132 distinct type-histograms**, and is realization-invariant. **"The 88
  plateau is one fusion pattern" is refuted**, and the plane-counting floor (Σ ≥ 64) is loose by
  16–30, so **no plane-level counting argument can bound 87.** Also: 9,391 sets (2.16 %) carry a
  signal touching 4 planes — always exactly one, consumed exactly once, always built from two
  disjoint-plane 2-plane parents; **0 sets reach 5 planes.**
- **Phase-2:** keeper (it closed a whole abstraction level as too coarse).

### J13 · plane-locality measurement (a ~330,000× candidate reduction, and its caveat)
- **Family:** structural analysis.
- **What it does:** Measures whether a mask's plane signature is contained in a single ρ-orbit's
  plane set, over the whole mask universe and over every circuit on disk.
- **Measured:** exactly **12,946 of 2³² masks are plane-local (3.0e-6)**, and **all 1,136 masks**
  of the 11 verified circuits plus the naive constructor's masks are inside that set, 0
  exceptions. Stronger: every valid single-mask repair of the 88@5 / 89@5 / 92@4 anchors is
  plane-local (**12/12, 36/36, 82/82**), 91 % at the naive start. A ~**330,000×**
  candidate-universe reduction, apparently free at the frontier.
- **Caveat recorded in-source:** every circuit on disk descends from one engine lineage, so this
  may be a property of the search trajectory, not of optimal circuits.
- **Generality:** MC-HARDCODED (ρ-orbit planes), but the *idea* — measure a cheap structural
  predicate over the whole known population and check every repair against it — is generic.
- **Phase-2:** **keeper.** Its own proposed decisive test (hand the exact oracle an 87 instance
  restricted to plane-local masks) **was never run.**
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **UNVERIFIABLE.** This entry has **no `Code:` and no `Logs:` field**, and its headline — "exactly **12,946** of 2³² masks are plane-local" — is not locatable in any primary source. A repo-wide search over `.md`/`.json`/`.py` returns only `beat88/understanding/v1_vocab_theory/data/harvest.json`'s `"bad_p": 12946`, an unrelated vocabulary-harvest statistic sitting beside `bad_O` in a dict about accepted/dup/violating circuits. The derived figure checks arithmetically (2³² / 12,946 = 331,720 ≈ "330,000×") but arithmetic on an unsourced number is not verification. **Do not quote the 330,000× reduction until the 12,946 is re-derived and banked.**

### J14 · feature-pinning survival floor (price a structural feature upstream)
- **Family:** constructive / feature pricing.
- **What it does:** Pins a structurally novel mask `v` by adding it to the target set (**both
  `engines.TSET` and `engines.T`** — `_extract` iterates the list, so pinning only the set lets
  LNS silently drop it) and descends from a 100–173-gate from-scratch root. The smallest size
  reached with `v` still alive is the feature's **price**.
- **Twist:** a novelty *bias* does not survive descent (`trim_masks` keeps only what the targets
  need); a *pin* does. And it starts upstream, where the feature is abundant and free, instead of
  at 88 where it is provably extinct.
- **Measured:** floors banked across 33 runs at 89–94 gates. **The best is 89 gates, carrying mask
  `0x98` with `|odd| = 3`** — a feature with **zero occurrences in 184 M mask slots** of the 88
  corpus (J11). Re-checked: every one of the 33 mask sets is realizable from the 32 input
  singletons with 0 unbuildable masks, contains all 32 targets, and contains its pinned mask. So
  **the measured price of leaving the corpus vocabulary is ≤ 1 gate, not "expensive". Never
  written up.**
- **Cost:** 16 workers × ~190 jobs × 1,200 s.
- **Code:** `experiments/e_upstream/{deep,probe}.py`.
- **Generality:** **CIRCUIT-GENERIC in method** — it prices *any* structural feature against *any*
  target set.
- **Phase-2:** **keeper, top tier, and unfinished.**

### J15 · order-of-sharing cone analysis
- **Family:** structural analysis.
- **What it does:** For each gate of a verified circuit, counts how many distinct output families
  its output cone spans.
- **Measured:** identical profile across **nine** verified circuits at four depths — ~2/3 of gates
  serve one ρ-orbit, 20–30 serve exactly two, 0–1 serve three or four, and a constant tail of
  **2–3 gates serves five orbits**. Those 2–3 are always weight-2 masks on **bit 7** — the
  footprint of the reduction polynomial `0x11B`. **Nothing anywhere shares across ≥6 orbits.**
- **Phase-2:** **keeper** — the sharpest structural description of *where* an optimum's sharing
  lives; it directly generated the "fix the carry gates as a forced prefix" proposal (never run).

### J16 · glue census (line-set confinement)
- **Family:** structural analysis.
- **What it does:** For every gate of every decomposed known circuit, computes the value's *line
  support* and asks whether it lies inside any block's line-set ("value-glue") and whether the two
  operands' joint support does ("joint-glue").
- **Twist:** it derives line coordinates by a route using **no field arithmetic** (trace duality:
  `support(m) = {k : m & (0x01010101 << k) ≠ 0}`), and cross-checks against the field route on
  2,000 random masks — so agreement is a real independent check, not a shared bug.
- **Measured:** 22 circuits, **1,970 gates.** The 14 record 88s: 1,232 gates, **0 value-glue, 1
  joint-glue.** All 22: 1 value-glue, 2 joint-glue. The only value-glue gate anywhere is `91@6`
  gate 70 on `{2,3,4,7}` and it is **removable at zero cost by re-association** (C12). The single
  genuine violation among 1,232 record-88 gates is `88@6` gate 79, and analysis shows it buys
  **line-1 currency, not arithmetic.** This **refuted the charter's premise**: the atlas's "3–9
  glue gates per 88" measures sector-confinement, which is strictly finer and does not transfer.
- **Phase-2:** **keeper.** "Measure the orbit support-unions and see if they reproduce your block
  line-sets" is a cheap first structural probe on any new circuit.

### J17 · economy census (column-pure / diagonal / mixed / glue typing)
- **Family:** structural analysis.
- **What it does:** Classifies every gate of a circuit by its dual-basis support and tabulates
  per-circuit budgets. The classifier's well-definedness is a *theorem* (all 28 pairwise sector
  intersections computed; exactly six are non-zero and each is 1-dimensional), not a test.
- **Measured:** ~80 of 88 gates live in the 8 sectors; glue 3–9 in the 88s vs 15 in 92@4 and 24 in
  97@3. **The glue law:** across all 74 off-line gates of eight frontier circuits, *every one* lies
  in a tap triple, 0 violations — against a null-model baseline of 0.150–0.189. **But** a later
  audit showed the law is **non-discriminating** (97@3 satisfies it 24/24) and **FALSE under
  operand-accounting** (88@6 gate 79 has support {1,2,7}).
- **Phase-2:** keeper as an instrument; its "better ⇒ more disciplined" reading is **refuted**
  (98@3, the worst circuit in the repo, has 6 off-line gates — fewer than three of the five 88s).

### J18 · socle fibration
- **Family:** structural analysis in a graded frame.
- **What it does:** Every circuit splits **exactly** as `|C| = l3 + s3` (skeleton mod socle +
  socle-level fibre); `L = min_Q |Q| + ρ(Q)`. Gives a 2-D "socle plane" in which every circuit is
  a point.
- **Measured:** `(l2,l3,s3)` for 9 circuits; the five 88s spread over `l3 ∈ {67,68,73,74,77}`.
  **Honest self-falsification recorded:** glue does *not* die in the quotient, so "the trick is 3
  socle gates" is wrong. A later audit correctly noted `l + s = 88` is an **identity**, not a
  measured tradeoff line. A third independent implementation reproduces the published `l3` table
  9/9.
- **Generality:** CIRCUIT-GENERIC for any local ring with a socle.
- **Phase-2:** keeper.

### J19 · carrier-difference census (the circle / C-D frame)
- **Family:** structural analysis / algebraic representation.
- **What it does:** Places the 32 inputs on a circle so byte rotation is a 90° turn; defines
  `Δ = I + R`; classifies every signal as a **carrier** `C_j` (still carries one absolute bit-lane
  identity) or a **difference** `D` (pure rotational information); and censuses each circuit as
  counts of `C+C→D`, `D+D→D`, `C+D→C` gates. It is a *typing discipline* over masks, cheap to
  compute, and — used as a **population statistic** — it falsifies single-circuit theories in
  about a minute.
- **Measured (from the review, which re-derived everything):** exact and confirmed —
  `o_{r+8} = R(o_r)` for all 32 outputs; the 32 outputs form **5** rotation orbits (sizes
  4/4/**16**/4/4); `Δ⁴ = 0` with ranks 32→24→16→8→0; **`M = I + LΔ + Δ³`** verified on all 32
  basis vectors; the first 20 gates of the from-scratch 88 @ 5 are exactly **15 quarter-chords +
  5 diameters**; exactly 24 extraction events, 3 per lane, 20 immediate + 4 delayed; the four
  delayed lanes are exactly 0, 3, 4, 6; internal carriers per lane `(2,2,2,3,2,2,2,2)` = 17;
  exactly two cross-lane extraction vectors.
- **Cost:** ~1 minute over a 58,143-circuit corpus.
- **Code:** review scripts described as throwaway but each result restated in full; `atlas/ring.py`
  holds the correct ring.
- **Generality:** MIXED — the C/D typing needs the target's lane structure; for
  `aes_inv_mixcolumns` the same circle and the same Δ apply (same Z/4).
- **Phase-2:** **keeper as an instrument, dead-end as a theory** — the review shows the theory
  generalises from a 0.25 % tail circuit.

### J20 · mechanism decode and library
- **Family:** structural analysis / vocabulary.
- **What it does:** Decodes an unfamiliar 88 gate-by-gate into named mechanisms (currency keying,
  helper fusion, Σ-fusion, corner mechanisms, plane drops) and banks them in a schema-conformant
  library with an incompatibility map.
- **Measured:** 13/13 anchors examined; `MECHANISM_LIBRARY.md` v2.7 = **15 entries + 6 notes**,
  six errata struck in place. **Its scope measurement travels with it: the named objects cover
  21.1 % of the plateau's vocabulary (280 of 1,330 masks), 36.5 % weighted by occurrence.**
  Population-scale structural facts that survived: the `s_0` prohibition (0 of 18,355, and
  *derived*, not merely observed — but labelled gate-count-free, so it can never filter an 87), the
  doubled-sum law, the complementary-Fano identity, `priv4 ⇒ not-s_7` at 952/952.
- **Generality:** MC-HARDCODED.
- **Phase-2:** **keeper as a record**, but note the campaign's own conclusion: **the composition
  thesis is dead by an identity** — `88 = 32 + 56` is forced, every mechanism moves a gate between
  the currency and helper piles, and *"a composition of wash-mechanisms is a wash."*

### J21 · population census by block decomposition
- **Family:** structural analysis.
- **What it does:** Takes the whole harvest of known 88-gate circuits and splits each one into the
  same fixed blocks, then asks which blocks ever differ between circuits. It works in a frame that
  needs no committed interface sets — fix the currency menus and the blocks are determined — so it
  can decompose circuits that were never generated by the block model at all.
- **Measured:** **54,889** distinct 88-gate mask sets decomposed; **0** with any out-of-class value
  (100 % in class); **37** distinct currency configurations; the largest holds 14,359 circuits;
  **only two blocks ever vary inside a configuration** (R01 and R34); the eight currency blocks and
  all four clean sectors vary in **0 of 37** configurations, ever. It also found the first
  counterexample to a standing "law": 2 of 296 census currency blocks violate the per-line purity
  rule — *"a measured regularity with exceptions, not a law"*.
- **Cost:** minutes (no solver).
- **Phase-2:** **keeper.** Cheapest way to learn where a plateau's freedom actually lives before
  spending solver time.

### J22 · conditional rigidity measurement
- **Family:** structural analysis.
- **What it does:** Asks whether fixing one block's value set pins down the next one, by grouping
  the census by upstream block and counting distinct downstream sets.
- **Measured:** `U1 | U07`: 1,015 groups, 409 unique, max 32; `U4 | U27,U3`: 623 groups, 325
  unique, max 2. So conditioning narrows but does not close — because a value *set* does not record
  which members were committed across the interface nor how the gate budget was split.
- **Phase-2:** superseded-by-J21 as a headline, but keep it — it is what makes the "population of
  interfaces" claim precise.

### J23 · forced-fanout rewiring (separate mask-set properties from wiring artefacts)
- **Family:** structural measurement.
- **What it does:** An SLP is a mask set *plus* a parent-pair choice; this separates what is a
  property of the set from what is a wiring artefact. "Forced" = the number of live inputs `x`
  having at most one available mask `m` with `m ⊕ x` also available — such an `x` has fanout 1 in
  *every* wiring.
- **Measured:** `88@5: z=3 (forced 3)`, `88@5fs: 5 (4)`, `88@6: 5 (5)`, `88@7: 6 (3)`, `88@8: 6
  (3)`, `89@5: 1 (1)`, `92@4: 3 (3)`, `97@3: 0 (0)`. Every re-wiring quoted was replayed and
  produces all 32 rows.
- **Phase-2:** **keeper.** G13 later *exhausted* the wiring space and found four of the five record
  88s have a UNIQUE valid wiring — which is what makes any per-circuit structural claim meaningful.

### J24 · transvection sibling matrix
- **Family:** structural analysis / exact accounting.
- **What it does:** From the `z` fanout-1 live inputs of a circuit builds an explicit invertible
  `Q` (invertible **by triangularity in program order**, not by composing transvections), forms
  `M' = M·Q⁻¹`, emits the shortened program and replays it. Gives
  `L(A) − Σ wt(m_x) ≤ L(A·Q⁻¹) ≤ L(A) − z`.
- **Measured:** `88@5 → 85`, `88@5fs → 83`, `88@6 → 83`, `88@7 → 82`, `88@8 → 82`, `89 → 88`,
  `92 → 89`, `97 → 97`, `91@4 → 89`. Sharp form on 88@5 and 88@6 (every `u_x` is an input):
  `L(M·Q⁻¹) = L(M) − 3` and `− 5` **exactly**, for two explicit matrices in `M`'s column-operation
  orbit. Referee re-executed on six record 88s with row-by-row verification.
- **Phase-2:** **keeper as accounting; the obstruction reading was WITHDRAWN in the lane itself**
  (rigidity implies `C_c`, not conversely; "for all invertible `E`" is vacuous since `E = M⁻¹`
  gives `L = 0`).

### J25 · provably-optimal census (`c0_census`)
- **Family:** structural measurement on objects proved optimal.
- **What it does:** Samples admissible keep-sets `K` where `minE_K` is known exactly *with no
  search at all* (`minE = 0`: the free target closure completes; `minE = 1`: one extra completes),
  giving provably optimal mask sets, then measures a structural quantity on them.
- **Twist:** every prior measurement of the same quantity in this project was taken on circuits
  nobody had proved optimal.
- **Measured:** 8,000 sampled 14-sets → **527 provably optimal mask sets** (181 + 346). Best
  wiring: `z = 0` in 485, `z = 1` in 42, **max z = 1**. At cert 5, `L(M|_K5) = 37` exactly and its
  37-mask optimum can be wired so **every one of the 14 live inputs has fanout ≥ 2**.
- **Phase-2:** **keeper** — this is how you get evidence about optimal objects without being able
  to find optimal objects.

### J26 · basin atlas (14-circuit census + relabelling-invariant ledger)
- **Family:** structural analysis / out-of-sample validation. **The best de-biasing instrument in
  the atlas slice.**
- **What it does:** Two independent clustering metrics (mask-set Jaccard and a 22-component ladder
  fingerprint) over all 14 known 88s, plus a **relabelling-invariant ledger** that attributes each
  supply gate to the sector accounts it actually serves.
- **Measured, and several of these overturn earlier headlines:**
  * Two metrics, one partition, **three basins**: `{twelve}` | `{88@6}` | `{88@5fs}`; effective
    independent origins = **four**, not one and not five.
  * **The central localization is measurably backwards**: no 88 ever runs a tap sector *below* the
    floor; all fourteen run the tap cluster *above* it, sector 3 by ≥2 in 14/14. The only
    sub-floor sectors in the dataset are **clean** ones.
  * The "two mechanisms" story is a **bookkeeping artifact** — 6 work + 1 supply = 7 = the model
    price, in every case.
  * **The universal mask core of all fourteen 88s is TWO gates.** There is no shared backbone.
  * **The three-account test is saturated**: values serving ≥3 distinct accounts number 2–4 in
    *every* 88 **and 3 in the 91-gate M1 optimum and 4 in the 97**. "Find a triple-role value"
    cannot be the 87 programme.
  * `(CLEAN, TAPS, SHARED)` runs on **one line, 1-for-1** across all 14.
- **Phase-2:** **keeper.**

### J27 · monster anatomy (a lore correction about mask weight)
- **Family:** structural analysis / instrument-bias diagnosis.
- **Measured:** exactly **three** "monster" (high-mask-weight) gates across 11 record circuits, and
  the weight statistic is a **measurement artifact**: an exact formula
  `mask weight = Σ_j |tv(μ_j)|` (0 mismatches over every signal of all 11 circuits) shows the same
  element weighs 6 on a light line and 10–11 on a tap line. Of the three, one is removable at **0
  gates and 0 depth**, one at 0 gates and +1 depth, one costs exactly +1. Latent census: 17 of 896
  sector-pure gates *would* be weight ≥ 8 on a heavy line.
- **Phase-2:** the lore correction is a keeper; the lead it opened (search with a corrected ruler)
  was executed (J28) and is null on the plateau.

### J28 · corrected ruler (line-normalised shape weight)
- **Family:** search heuristic / instrument repair, with an unusually good A/B harness.
- **What it does:** Replaces `popcount(mask)` — which every search in this project's history used
  to rank and cap candidates — with a **line-normalised shape weight** `W`: decompose into
  v-coordinates and count minimal atoms over the redundant generator set. O(1) per mask via a
  256-entry BFS table.
- **Twist:** it is the *fix* for a proven bias: the same abstract element weighs ~1.5× more on a
  "tap line", so popcount structurally excluded the exact vocabulary the last 3 gates are made of
  (the excluded vocabulary is **exactly 1,516 elements**).
- **Measured:** `W` halves the artificial cross-line spread (512 → 256). It **orders the frontier
  where popcount anti-orders it**: `Σ popcount` is *lowest* for 97@3 (370) and 98@3 (365) and
  highest for the 88s (372–394); `Σ W` reverses it — 88s 297–319 < 92@4 331 < 98@3 342 < 97@3 360.
  On **descent** it wins (mean best 90.33 vs popcount's 91.67 from a 97@3 start, equal CPU, 42
  runs) and is the only arm besides its sibling to reach 89. On **plateau walking** it is null (753
  distinct states vs popcount's 756 — while *no* preference gives 3,784, a 5.0× effect that is
  about having a tie-break at all). It confirms its own prediction and then kills it: heavy-mask
  emission rate is 1.11/1000 (popcount arm) vs 18.27/1000 (`W` arm) — but the 14 known 88s sit at
  **7.31/1000, between the two**, so **neither ruler points where 88s live.**
  **Also killed: "the best circuits destroy the most information."** y-basis cancellation spans
  9–33 and separates the frontier; in the v-basis it is **flat at 46–56 for every circuit from 88
  to 98.**
- **Cost:** 166 walks, equal-CPU accounting via `clock()`, 60–300 CPU-s/cell.
- **Generality:** the ruler is dual-basis-specific; **the seven-arm equal-CPU A/B with two null and
  two *inverted* control arms, plus a temperature sweep, is fully general and unusually
  well-designed. Port that harness.**
- **Phase-2:** **keeper, and under-exploited.**

### J29 · E3 triple classification / backbone recovery
- **Family:** structural analysis on a previous campaign's data.
- **What it does:** Recovers the 22-mask backbone from four double-defect bridge JSONs
  (over-determined four ways) and classifies all C(22,3) triples by span.
- **Measured:** the three previously-unnamed backbone masks identified — `00800080`, `00808000`,
  `80000080`, all pure `d7` columns (which is why they admit no +1 bypass). Independently
  reproduces the prior campaign's counts: exactly 13 edges, exactly 249 edge-containing triples,
  1,291 edge-free. **E3 is not empty**: 869 genuinely cross clusters, 157 fully spread, 12 with the
  maximal span. Three clean-territory defect masks are exactly XOR differences of cross-cluster
  backbone pairs — **the E3 shape exists, is buildable, and costs +1.**
- **Phase-2:** the finding survives; the search it launched is closed.

### J30 · enabler / midpoint theory (why glue exists)
- **Family:** structural analysis / theory.
- **What it does:** Every tapped-sector target is a 3-leg sum; its three midpoints XOR to zero. Two
  of the three lie off every ladder line, so **every per-sector score gives them zero** — that is
  what an "enabling gate" is, and it explains the five ternary repair planes as midpoint triples.
- **Measured:** cluster law 74/74 (later 87/87). Of the 30 off-line gates in the five 88s only 8
  are order-1; **22 are deeper (glue+glue→target)** — so pairwise-invisible mechanisms are the
  norm. Records achieve midpoint profit 3; an in-architecture 87 needs 4.
- **Generality:** generalises to any circuit whose targets are ≥3-leg sums.
- **Phase-2:** keeper as *understanding*; **its search directive was never executed.**
- **COMPLETED (2026-08-29):** this entry was one of the nine Appendix A skeletons. The full schema-conformant entry, written from primary sources by `wrapup/day2/CATALOG_AUDIT.md` §3, is **Appendix A §A·2**.

### J31 · backbone obligation calculus + the physical k−1 search (`shot87`)
- **Family:** structural analysis → exact search over gate constructions.
- **What it does:** Decomposes an 88 into a *core* (masks constant across its local neutral
  component) plus `k` repair coordinates, computes the core's pending **components** (= repair
  obligations), and then asks physically whether the core can be finished with `k−1` gates — which
  would be an 87. The unit of analysis is a *family/core*, not a circuit or a window; the search is
  over gate-constructions from the live closure with a set-cover lower-bound prune.
- **Measured:** Phase A profiled **all 204 families, 0 errors**: `k ∈ {4:2, 5:29, 6:60, 7:59, 8:39,
  9:9, 10:6}`; `all-ternary` **54 yes / 150 no**; `comps − k ∈ {−2:2, −1:6, 0:40, 1:53, 2:37, 3:36,
  4:20, 5:8, 6:2}`. Phase B decided **22 of 204: 15 sound NO-87, 7 INCONCLUSIVE at the 25 M node
  cap, 22/22 planted controls PASS.** Node counts 25,190 → 20,901,823.
  **The headline structural fact:** `n_components ≥ k` in **60 of 62** profiled families — *"that
  is the structural reason 87 is hard here: the obligations are already nearly in bijection with
  the gates."* **Four distinct gauge orbits** are provably unable to finish with `k−1` gates.
  **`CONFLICT` / correction:** a later lane found `n_components ≥ k` is **FALSE — 8 of 204 violate**
  (see J32 and Appendix B #5).
- **A soundness bug caught before it shipped:** an early prune (`|R| > gates_left + free`) returned
  "NO COMPLETION, 5,990 nodes" in 6 s for the campaign's top 87 lead — **a confident false
  negative**, because one mask can serve several components. Replaced with an exact set-cover DP
  bound over all `2^ncomp` subsets. **The 6-second runtime was itself the tell.**
- **Cost:** Phase A ~10 min on 30 procs; Phase B ~1 h/family at the 25 M cap.
- **Code:** `beat88/methods/m5_backbone/{m5,pending,abstract4,e3fix,routing,cash}.py` and
  `verify/{shot87,census,run_census,sweep87,close42,close_core,fiber10,fourgate,neg39,m5lib}.py`.
- **Generality:** **CIRCUIT-GENERIC** — the decomposition is exterior-parameterised and runs on any
  circuit; obligations are a closure property.
- **Phase-2:** **keeper, and the most under-finished method in the beat88 slice** — 182 of 204
  families never decided, including 7 of the 8 compound-obligation frames that are the best leads.

### J32 · obligation calculus with a witness-free cost (the repaired version)
- **Family:** combinatorial accounting.
- **What it does:** Formalises "an 88 = gauge core `C` + `k` repair gates", defines an *obligation*
  as a connected component of the dead set, and asks exactly when `k−1` gates could finish the core.
- **Measured:** the counting identity `k = Σ_j m_j` holds **204/204** (+5,100 witnesses). The
  conjecture `n_components ≥ k` is **FALSE — 8 of 204 violate** (J31 had found 2 of 62).
  **Self-refutation, referee-forced:** marginal cost is **witness-dependent**, so every
  compound/free/surplus column of the first census is a witness artifact — **the whole line is
  retracted.** Repaired by a **canonical-cost census**: a witness-free cost ρ, under which
  `n_expensive ≥ 1` holds 203/204 and the disjunction `n_expensive ≥ 1 ∨ cover ≥ k` holds
  **204/204**; the cash law is exact **425/425**.
- **Generality:** the definitions are CIRCUIT-GENERIC; the instrument is MC-HARDCODED through the
  204-family census.
- **Phase-2:** **keeper (the ρ version); the witness-dependent version is explicitly RETRACTED.**

### J33 · walls-as-a-dataset (treat millions of exact labels as data)
- **Family:** structural analysis over the exact labels the search lanes produced. **The highest
  density of transferable methodology in the beat88 slice.**
- **What it does:** Treats the campaign's millions of exact negatives and ~1,100 positives
  (cuttable 89s) as a *dataset* and asks what smaller object separates cuttable from rigid.
- **Measured:**
  * **Dataset:** 90,110 rows → **89,744 unique orbits, 0 label disagreements**; 1,076 cuttable
    (89: 1,063 · 90: 8 · 91: 5 · **88: 0**); 1,143 distinct cuts, 1,140 aligned at ρ-rotation k=0.
  * **The lineage-independence control — the lane's most important result.** At Jaccard ≥ 0.90 the
    1,063 cuttable orbits collapse to **13 clusters** (largest 686, then 295; two basins hold
    92 %), while a size-matched rigid null gives 850 clusters. **Every statistic computed over
    "1,076 cuttable orbits" has effective n ≈ 13.** (See L23.)
  * **Cut factorization: 1,121 / 1,121 cuts factor in BOTH orderings, zero exceptions, in 6.1 s.**
    A cut is *not* a two-gate rearrangement — it is **one mask `c` whose addition kills two gates
    at once**. The added mask takes only **49 distinct values (29 up to ρ)**, and **92.2 % of all
    cuts ever found add one of just two masks** (`08808c0c` 47.8 %, `0808848c` 44.4 %).
  * **Repair-relation marginals:** cuttability of a tight circuit ⟺ `max_w vac(w) ≥ 2`, **299/300**
    against the exhaustive label; **`deg_max ≤ 4 ⟹ rigid`, 0 / 22,247**, screening 48 % of the
    tight-89 corpus. **And it refutes the campaign's own retention advice:** `P(cuttable | deg_max)`
    is **non-monotone** — peak 29.7 % at `deg_max = 10`, **0 % at 12 and 14** — so "prefer
    `deg_max ≥ 13`" is wrong.
  * **Collision mechanism:** "collision = self-dependence" is **dead** — the repair is still
    constructible in **480/480**. What separates cashing from colliding is **adjacency of the served
    pair** (`m₁⊕m₂ ∈ S ∪ INPUTS`): 58.8 % vs 10.4 %, a **5.6× rate ratio**, neither necessary nor
    sufficient. Among high-mobility *rigid* circuits, **53 of 100 already have a doubly-serving
    repair and are stopped purely by collision.**
  * **Within-lineage descriptor control:** `deg_max` AUC **0.823 naive → 0.662 within-lineage**
    (half the signal is lineage confound); `sh_out_neutral` **dies** (0.555) despite being one of
    the four named signature descriptors; `sh_fixed_masks` **survives** at 0.660 — the campaign had
    rejected it using cross-*source* replication, **the wrong control**.
  * **Per-gate re-sweep:** 3,441 circuits, **307,694 gates.** Population A (27 extreme-sharing
    gates): **25 of 27 buy the single mask Λ = 0x80808080**, none in a 91/92/97. Population B
    (drop-0 "useless" gates) **enable nothing** — and the placement hypothesis *inverts*: 88s carry
    **1.99 drop-0 gates each vs 0.41 for 97s (5×)** and place them **later**.
  * **Λ probe:** `deg(Λ) = 0` in **100/100** circuits containing it (baseline P = 0.834, so all-100
    by chance ≈ 1.3 × 10⁻⁸); Λ is never a valid repair column where absent. Λ-containing tight 89s
    cut at **0.02 % vs 2.76 % — 138× less** — but the lineage control shows none of the 2,205 orbits
    in any *mixed* basin contains Λ, so it is a basin marker, usable as a screen, **not** as evidence.
  * **Dead in this lane, with cause of death recorded:** an algebraic cut-type ladder (its T3/T4
    split is an artifact of the ladder's own ordering); and a Φ-drop parity lemma, **refuted by its
    own checker** with drop-30–32 witnesses in every parity class, because 4 of the 32 inputs are
    themselves φ-odd.
- **⚠** This is the **only unrefereed lane** in the understanding programme, and the one part of it
  that was refereed was refuted.
- **Phase-2:** **keeper — apply the lineage-independence control to every corpus-wide statistic the
  campaign published.**

### J34 · overlap parameterisation + vocabulary-blindness audit (V1)
- **Family:** structure theorem + whole-corpus census.
- **What it does:** Proves the cancellation layer's vocabulary has exactly one unknown, and it is
  not a set of masks — it is the **overlaps**. V1-1: every mask of a circuit is a subset of a target
  or of a cancel-parent. V1-2: a cancelling gate is *exactly* a triple `(child z, overlap O, split
  A)` with parents `A|O` and `(z∖A)|O`. Feedstock is not free-floating: it is `z ⊔ O` cut in two.
- **Measured:**
  * **Frontier anatomy** over 8 oracle-VALID circuits: **178 cancelling gates, 80 distinct overlaps,
    80/80 with `cover = 1`** — null probability ≈ **4 × 10⁻³¹**. **176 of 178 cancelling gates are
    `split`**; the intuitive "build a superset, strip it" nested shape occurs **twice**.
  * **Corpus census:** **381,613 JSON files → 324,121 distinct live-trimmed circuits, 9,557,026
    cancelling gates, in ~200 s.** At live size 88: 242,974 circuits, 7,158,511 cancelling gates,
    `cover(O) = 1` in **99.917 %**, `cover(O) = 2` in 5,941, **`cover(O) ≥ 3` in ZERO**; only **546
    distinct overlaps and 2,228 distinct cancel-parents** across a quarter of a million circuits.
    *Every mask of every one of the 242,974 known 88s lies in `V₂`* (subsets of 3-target unions);
    97.6 % lie in `V₁`.
  * **The audit that voided the programme's main line:** the entire known 88 population uses
    **2,646 distinct masks; tier-3's 3,961-mask vocabulary `W` contains 1,113 of them — 42 %.** At
    89 it is 30 %, at 90 it is 23 %. Good news attached: **`W ⊂ V₁` entirely (3,961/3,961)** — the
    corpus-derived vocabulary is a *sample* of a set writable from the matrix alone. Sizes:
    `|V₀| = 1,648`, `|V₁| = 532,457`, `|V₂| ≤ 2.13 × 10⁸`.
  * **Span cone bound (V1-6):** `|cone(u) ∪ cone(v)| ≥ wt(z) + wt(O) − 1`, proved for **arbitrary**
    SLPs (strengthened from CF parents, which matters because feedstock is often itself produced by
    a cancelling gate — measured 45 of 356 parent slots). Consequence: **a cancelling gate costs
    `wt(O) + 1` extra unless the overlap's cone is shared.**
  * **A clean impossibility-of-this-approach (V1-8):** the natural inequality system's least upper
    bound on `cover` is **8 — the ambient one** — so it yields exactly the whole space `F₂³²`.
- **Phase-2:** **keeper**, and V1-2(b) — re-parameterising the cancel mode as `(z, O from 1,680
  theorem-derived masks, A over splits)` so feedstock is *constructed* rather than *inherited* — is
  the design that became F26.

### J35 · heavy-corner × plan join
- **Family:** joint structural finding across two lanes.
- **Measured:** **the cancellation plan `Z` is essentially a choice of which targets to build by
  cancellation** — 24 of 27 `Z` elements are AES targets on the 88@7, 26 of 30 on the 88@6. The
  heavy class count `c` is the coarse coordinate sliding `|Z|` against `|cf|` **along the plateau
  at constant sum 88** (`c=9 → (23,65)`, `c=11 → (33,55)`). `Z` is heavy-enriched in every frontier
  circuit (59–75 %) and **heavy-POOR in the 97 (33 %)** — the cancellation layer *becomes* the heavy
  layer as circuits improve. Two universal heavy-critical plan elements appear in **7 of 7**
  circuits. **And the Λ coupling, priced:** a full-class mask is cheap to build (a disjoint union of
  four heavy inputs, living in the CF layer) but **every consumer of it toward a target must
  cancel**, because no target has heavy pattern `H` — "buy a gate that appears useless", now with a
  proof and a price tag.
- **Phase-2:** **keeper — the sharpest joint finding in the programme.**

### J36 · vocabulary saturation measurement
- **Family:** structural analysis.
- **What it does:** Reads circuits until the `(child, overlap)` vocabulary stops growing.
- **Measured:** **4,120 pairs over 1,469 children, saturated** — 2,000 → 12,000 circuits grows it by
  1.3 %. That repairs an earlier diagnosis: in `(z,O)` coordinates the population is essentially
  self-covering, so **the coordinate change was right and the corpus was never the problem**; the
  problem is that the faithful set costs 1.81× the size at which the previous instrument returned
  UNKNOWN.
- **Phase-2:** keeper.

### J37 · candidate-class naming-rate measurement (price a strategy in seconds)
- **Family:** pre-measurement.
- **What it does:** Scores a candidate class by what fraction of **real** cancelling gates it names,
  over 41,067 gates from 1,500 circuits, alongside the model size it costs.
- **Measured:** `W1` names 0.413 at `|W|`=38,240; `W2` names 0.702 at 211,936; `W3` 0.772. Since a
  configuration decides only circuits *all* of whose cancelling gates it names, the useful quantity
  is the naming rate raised to the power κ: `0.41^27 ≈ 10^-10.6`. The economically-motivated
  `TDIFF` class names **12.9 %** — worse than a plain weight cap. **The classes wide enough to
  contain a good circuit are exactly the classes too large to build.** Its sibling `lean.py` killed
  the obvious escape (**only 16.6 % of 82,578 real cancel parents are built as `A ⊕ O`**) before
  anyone spent a week on it.
- **Phase-2:** **keeper, top tier — prices a whole strategy in seconds.**

### J38 · structure algebra (what symmetry the search discovered on its own)
- **Family:** structural analysis.
- **Measured:** the 32 targets are a **single** column map (no disjoint 4-column decomposition;
  every output byte touches all four input bytes). ρ has order 4 and the targets form 8 free
  ρ-orbits. **Full ρ-symmetry costs +19** (best ≈108); the elite basin is **79–81 % ρ²-symmetric**
  and its 12 ρ²-fixed masks are exactly the classic (x0^x2)/(x1^x3) trick — the search rediscovered
  the order-2 subgroup unaided. One published 88 is 75 % ρ²-symmetric. Best single-byte cone
  standalone is 33 gates, so four independent cones would cost ≥132 against 89 achieved —
  **cross-byte sharing is the whole game (57 of 89 gates shared).**
- **Phase-2:** keeper — it produced the seeds both search-found 88 families descended from.

### J39 · legibility profiling (are optima reachable by legible search?)
- **Family:** structural analysis of optima.
- **What it does:** Defines `D(S) = Σ_targets (δ_S(t) − 1)` with exact δ, splits every gate into
  "progress" (`dD < 0`) and "investment" (`dD = 0`), and compares four quantities per instance:
  `k*` (SAT-certified optimum), `k_strict` (min over all-progress circuits), `k_cf` (min
  cancellation-free), `k_greedy` (best of 2,000 BP restarts). It does not search for circuits — it
  measures whether a legible search *could* have found the optimum.
- **Measured:** **`k_strict = k*` on 39/39 decided instances** (0 counterexamples, 4 UNDECIDED
  timeouts) — **optima never need locally-senseless gates**, so the 88s' legibility is not evidence
  against optimality. But greedy misses the optimum **6 of 7** times on MC-density-matched instances
  (by 1–2 gates in 13–16). GF(4) mini-MixColumns: `k* = 14` vs greedy 15, and only 6/14 of the
  optimum's gates are greedy-top — *"optima are not senseless; they are patient."* All five 88s
  carry 0–2 investment gates out of 88, `D0 = 152`.
- **Cost:** ~2 h per dim-8 ρ-orbit `k=11` UNSAT certificate; three dim-12 orbits left UNDECIDED
  after 3 h/level.
- **Phase-2:** **keeper** — the only method that prices what a heuristic search is structurally
  blind to.

### J40 · exact move census (kill a bad decomposition before you run it)
- **Family:** structural analysis / pre-measurement.
- **What it does:** Enumerates the **complete** remove-1 + single-mask-repair move set of a state,
  then scores any proposed partition by what fraction of that move set stays region-local. No search
  needed — it evaluates a search design *before* running it.
- **Measured:** the number that explains a whole failed parallelisation — **the complete remove-1
  move set of the record 88@5 is 12 moves**, distributing 3/6/1/0 across four balanced regions (one
  worker has **no legal move at all**). Orbit partitions keep 74–98 % of moves local; DAG-mincut and
  random partitions score **exactly 0.000**, structurally.
- **Cost:** seconds.
- **Code:** `experiments/e1_regions/code/move_census.py`.
- **Generality:** **CIRCUIT-GENERIC.**
- **Phase-2:** **keeper, top tier — the cheapest way to kill a bad parallel/decomposition design
  before spending compute.**
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — Generality wrong, and a mis-stated range.** (a) Labelled `CIRCUIT-GENERIC`, but `experiments/e1_regions/code/move_census.py:15-16` does `import mixcolumns_core as core; TSET = core.TARGET_SET` and `:23` reads it directly; the anchor list at `:52` is seven fixed MixColumns circuits. This is the *same* coupling E1 carries, and **E1 is labelled MIXED** — the catalog is internally inconsistent. Correct label **MIXED**. (b) "orbit partitions keep **74–98 %** of moves local" — the primary JSON's minimum orbit `local_frac` is **0.7143** (a88fs under orbit4 and orbit8), so the true range is **71.4–97.7 %**. The lane's own table prints `0.714` two lines above the sentence saying 74 %, so the error was copied upstream rather than introduced here.

### J41 · widening theorem + byproduct impossibility (G1, G4)
- **Family:** hand-reasoning theorem, solver-free, with SAT runs as falsification tests.
- **What it does:** G1 proves that letting a block form gate values on *any* line-set, up to all
  eight lines, is exactly free — the value-level expressiveness gap is worth zero gates. G4 proves
  a block running at its base price can never emit a value with a component outside its own
  line-set, closing the sharing route the glue census pointed at.
- **Twist:** both are proofs; the SAT runs afterwards are *falsification tests of the proof*, not
  the evidence for it.
- **Measured:** G1 confirmed by 4 widening controls (two at dim 16), all at exactly the base price.
  G4 confirmed on **48/48** exact dim-12 instances run *after* the proof, all `capped_unsat`. Two
  results outside G4's reach were measured separately: `D37` minted by `S7W` ≥ 11 = base; `Q1`
  relocated to `S7W` ≥ 9 against a budget of 8.
- **Phase-2:** **keeper as a pattern** (prove it, then run the SAT sweep as a falsification test —
  not the other way round). The axis itself is **closed** for MixColumns.

---
# Family K — Tripwires and live detectors

Always-on, provably sound "an improvement is available right now" alarms. These are
the cheapest things in the whole catalog and two of them are the top phase-2 ports.

### K1 · B = 56 tripwire ★ TOP PRIORITY
- **Family:** proved theorem turned live detector.
- **What it does:** Counts `B` = the number of non-output gates that have a consumer, on every
  circuit any sweep touches. On a valid 88 this must be 56; anything else means an 87 is available
  *by deletion*.
- **THE THEOREM, verbatim** (attribution: proof verified at a referee's desk, binding):
  > On any valid 88-gate MixColumns circuit *not already reducible to 87*, `B = 56` exactly, where
  > `B` = the number of non-output gates that have a consumer.
  > **Sketch:** validity puts all 32 targets on gates; two gates with the same mask make the later
  > deletable (an 87); a non-output gate with no consumer is deletable (an 87). So 88 distinct
  > masks, exactly 32 output gates, 56 non-output gates, all with consumers.

  **The contrapositive is the 87 detector:** `B ≠ 56` on a valid 88 means a duplicated mask or a
  consumer-less non-output gate, and in *either* case an 87 is immediately available by deletion.
  Generalised as the `87 = 32 + 55` split.
- **Proof location:** `experiments/e15_campaign3/laneSWEEP.md` §11 (statement + sketch +
  fail-ability check); `experiments/e15_campaign3/AUDIT.md` §11.4; restated in `experiments/e15_campaign3/RESULT.md` and
  `experiments/e17_pure/DOSSIER.md` §3.4.
- **Code that RUNS it:** `experiments/e15_campaign3/tools/sweep.py` — `count_B(c)` at **line 296**
  (`return sum(1 for g in range(c.n) if not c.isout[g] and c.cons[g])`), wired into every row at
  **lines 525–532** (`rec['B'] = count_B(c)`, `rec['B_theorem_ok'] = (rec['B'] == 56)`, plus an
  `ALARM` string on failure), with the loud path at **lines 730–738** (writes `ALARM_B_<ts>.json`
  and prints `*** B-THEOREM ALARM (87 AVAILABLE)`).
- **Measured:** fired **ZERO** times on **17,283 / 17,283** run-A circuits and **13 / 13** d3
  anchors. **No `ALARM_B_*.json` exists anywhere on disk.** `B = 56` established two ways because
  906 stale-build rows lack the `B` field: the explicit `B` reads 56 on all **16,377** rows carrying
  it with `B_theorem_ok: true`, and on all 17,283 rows `helpers.bases = 56` and
  `d2.seeds = 1,540 = C(56,2)`; zero mismatches where both are present. The d3 seed count
  `27,720 = C(56,3)` is the same theorem arriving a fourth way, and the 89-gate controls carry
  `29,260 = C(57,3)` — the theorem read from the failing side. **Fail-ability check: `count_B` reads
  57 on both 89-gate controls and 56 on the 88s**, so the detector can and does report the alarm
  value. A retroactive scan of every row the lane ever banked (230 valid-88 rows) found 0 with
  `seeds != 1540`.
- **Cost:** ~free — one pass over the gate list per circuit.
- **Generality:** **MC-HARDCODED only in the constant.** The theorem is `B = n − (#outputs)` for
  any irreducible SLP with distinct masks and all outputs on distinct gates; for a new circuit with
  `q` outputs at size `n` the tripwire is `B == n − q`. **This is the item to port first when aiming
  at `aes_inv_mixcolumns`** — free, always-on, provably-sound one-gate-improvement detection.
- **Phase-2:** **keeper, highest priority.** It is the campaign's only live 87 detector and it is
  exactly the artifact an external-correspondent follow-up wants: feed a foreign 88 to it and it
  either confirms `B = 56` or hands you an 87.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — the starter kit's "one constant" port cost is wrong**; every measured number is exact. Recomputed from `sweep_A_fullpop.jsonl`: 17,283 VALID88; `B` present on 16,377, **all 56**, all `B_theorem_ok: true` (906 stale exactly); `helpers.bases = 56` and `d2.seeds = 1540` on 17,283/17,283; **no `ALARM_B_*.json` anywhere on disk**; and the detector demonstrably **can** fail — `count_B` returns **57** on both 89-gate controls and 56 on the 88s. **Port cost:** running this on another circuit needs ≥4 edits across 2 files — `tools/sweep.py:48` (`TARGETS = set(mixcolumns_target_masks())`), `:102` (`n == 88 and built == 32`), `:528` (`rec['B'] == 56`), and `laneCUT/cut.py:22` (`TGT = mixcolumns_target_masks()`, which `Circ.isout` depends on), plus `cut.py:34`'s `range(32)` — **and it cannot run at all until A1 is ported first**. `count_B` itself is genuinely generic; the harness around it is not. Citation nit: the quoted body of `count_B` is at line **310**; 296 is the `def`.

### K2 · Lemma R / Theorem T2 corpus tripwire ★
- **Family:** theorem turned detector, second instance.
- **What it does:** **Lemma R / Corollary R\***: in an optimal SLP, for every (gate,
  private-operand) pair, `minrep(mask | available) = 3` exactly — never 1, never 2. A `minrep = 2`
  hit *is* a valid circuit with one gate fewer, produced constructively. **Theorem T2** (the
  private-cone tree theorem): `minrep(mask(c) | Avail(c)) = |D(c)| + 2` exactly, the cone is a tree
  with distinct leaves.
- **Twist:** strictly wider than the k=1-site frame — it drops the requirement that the other
  operand have exactly two consumers.
- **Measured (the tripwire actually ran, 2026-08-28):**
  * corpus mode: **1,200 valid 88s, 9,100 private-operand pairs (7.6/circuit), minrep=1: 0,
    minrep=2: 0, minrep=3: 9,100 — LEMMA R HITS: 0.**
  * non-88 mode (the power control): **667 valid non-88 circuits, 11,944 pairs (17.9/circuit),
    minrep=2: 66 — LEMMA R HITS: 66 on 26 distinct circuits**, and five were compressed and
    oracled: **89→88 VALID (×3), 90→88 VALID, 90→89 VALID.**
  * T2 on 150 corpus 88s: **0 VIOLATIONS** (13,200 gates, tree/distinct 13,200/13,200).
  * T2 on non-88s: **1 VIOLATION**, at `n = 89`, gate 80, `D = [32,67]`, in a named file.
  * per-`n` table (88: 60 circuits/359 pairs/0 minrep2; 89: 228/2,057/3; 90: 63/763/5; 91:
    25/348/0; 88-corpus: 600/4,564/0).
  * **Optimal circuits carry less than half the private-operand structure of non-optimal ones (7.6
    vs 17.9 pairs per circuit)** — itself a consequence of Lemma R being enforced.
  * A referee CONFIRMED T2 and its proof, and it **survived exhaustive enumeration of 57,139
    optimal SLPs over 181 matrices**, including `|D| = 3`, a regime the corpus never reached — but
    noted it is **not new mathematics**.
- **Cost:** 71 s (1,200 88s), 173 s (667 non-88s), 281 s + 189 s (T2). Whole corpus would be ~80
  CPU-minutes at 1 core — **not spent.**
- **Code:** `experiments/e17_pure/laneDELTA/{witness,cone_theorem,nat_witness,pern,lemmaR_sweep}.py`.
- **Generality:** **CIRCUIT-GENERIC** — Lemma R and T2 are statements about optimal XOR SLPs, not
  about MixColumns.
- **Phase-2:** **keeper, second only to K1.** Same shape: a proved theorem whose violation hands you
  a smaller circuit, running as a cheap always-on scan.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — the starter kit's "port cost: none" is wrong**; every measured number is exact. The theorems are circuit-generic; the code is not. All five cited scripts do `from frame import Frame`, and `experiments/e15_campaign3/compose/frame.py:22` is `return (a^0x11B)&0xFF if (a&0x100) else (a&0xFF)`, `:32` `coef=[2,3,1,1]`, `:42` `TARGET = target_masks()`, with 32-signal assumptions at `:51,73,83`. Each script additionally hard-filters `if f.n != 88` (`witness.py:135`, `cone_theorem.py:147`, `lemmaR_sweep.py:87`, `pern.py:47`). **Port cost: a new target-mask generator plus four `n != 88` guards.**

### K3 · streaming k=2 shell detector (the live 87 tripwire)
- **Family:** exact decision deployed as a live monitor.
- **What it does:** Tails every worker's harvest file by persisted byte offset, dedupes new 88-gate
  states by md5, keeps a **novelty-biased bounded backlog** (picks the state with maximum minimum
  symmetric difference against a reservoir of already-swept states, not FIFO), and runs the complete
  1,540-window k=2 shell on each. Rationale: every known 88 has an exactly empty k≤2 shell, so a new
  88 whose shell is *not* empty is an 87.
- **Twist:** it runs concurrently with the search and raises a `CLAIM_*.json` on a hit; the novelty
  bias is what makes a bounded backlog defensible.
- **Measured:** **197,072 exhaustive k=2 shells decided across the two fleets, all empty, zero
  claims raised.** 1.9 s/state on CPython, 0.65 s under PyPy. One fleet dropped 64,421 states on
  backlog overflow; the other dropped 0.
- **Code:** `campaign_87/{hunt87,tri_hunt}/detector.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** keeper — the cheapest continuous safety net in the project.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — Generality wrong, and the throughput figure is contradicted by the lane's own ledger.** The 197,072 headline is exact (148,893 + 48,179, all `verdict: "irreducible_k2"`, zero non-empty; no `BREAKTHROUGH_87*` file exists). (a) Labelled `CIRCUIT-GENERIC`, but `campaign_87/hunt87/detector.py:39,43` imports `mixcolumns_core` and takes `TARGET_SET`; `hunt87/mixcolumns_core.py:21,36,51` carries `0x11B`, `coef=[2,3,1,1]`, `range(32)`; and the 1,540 window count is itself `C(56,2)` — an 88-gate MixColumns constant. By this catalog's own convention (K1 self-labels MC-HARDCODED for the identical situation) the correct label is **MIXED**. (b) "1.9 s/state on CPython, 0.65 s under PyPy" is sourced to `hunt87/README.md:119-120` but contradicted by the banked ledger: mean/median per-state is **1.152 / 1.205 s** (hunt87) and **1.277 / 1.269 s** (tri_hunt) over all 197,072 rows — and `tri_hunt/REPORT.md:92-93` states that lane ran under PyPy, so its PyPy states cost ~2× the quoted 0.65 s. `detector.py:29` also says 2.05 s CPython, not 1.9.

### K4 · free-gate scan (duplicate mask / dead gate)
- **Family:** cheapest possible exhaustive negative.
- **What it does:** Scans a valid 88 for a duplicated gate mask or a consumer-less non-output gate;
  either one *is* an 87 by deletion.
- **Measured:** **ZERO across all five closed orbits (~45k circuits, three independent measurements)
  and ZERO across the 18,355 valid 88s of the repo corpus** — two independent loaders, zero
  duplicated masks, zero dead gates. Explicit scope: it rules out only an 87 obtainable by deleting
  a redundant gate from an 88 already on disk or free-move-reachable from the knowns. **No positive
  control is constructible — exhibiting one would be the prize.**
- **Code:** `experiments/e14_plateau87/audit_tools.py`,
  `experiments/e15_campaign3/tools/free87_all.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper** — it costs nothing and it is the ancestor of K1.

### K5 · self-test / fake-87 tripwire harness
- **Family:** validation infrastructure.
- **What it does:** Plants a known-solvable instance (a deliberately wasted gate, a fake 87) and
  checks that the pipeline finds it **and** that the export path *rejects* the fake.
- **Measured:** **131 checks, 0 failed**, and it pins three real harness bugs, including the one
  that matters most: *"Cross-pollination was silently dead — `campaign_87/hunt87/hunt_worker.py` never called
  `wire_harvest`, so every hunt87 fleet harvested and never merged, and nothing in the logs said
  so."* The four `"gateCount": 87` files in the whole campaign_87 slice are all tripwire artifacts
  named `fake87`, `badfail` or `FAILED_87` — **the strongest available evidence that no real 87 was
  ever found and lost.**
- **Code:** `campaign_87/cascade6/selftest_cascade.py`, `campaign_87/d3_exact/selftest.py`,
  `campaign_87/hunt87/selftest_archive.py`, `campaign_87/agents/*/selftest*.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper — mandatory.**

---

# Family L — Controls, calibration and audit instruments

**This family is the campaign's real product.** Its single most important finding is
L2: most of the project's negative instruments were measured at likelihood ratio
≈ 1.00 about the existence of an 87. Read L1–L4 before reusing any negative from
this tree.

### L1 · positive-control methodology (the one-gate-above control) ★
- **Family:** methodology — the standing policy.
- **What it does:** Every negative instrument is re-run on an instance that **provably has the
  improvement it claims not to see** — typically a circuit one to nine gates above a verified
  better one.
- **Measured, across four independent instruments:**
  * the exhaustive k=2 decider finds **0 reducible windows** on a 97-gate circuit with a verified
    88 nine gates below it, and on a 94, a 92, a 91, a 90, an 89 and an 88 — **12,241 exhaustive
    k=2 + 8,400 sampled k=3, zero reducible anywhere.** *"A 97-gate circuit is indistinguishable
    from an 88 by this instrument."*
  * a per-region vocabulary ladder returns UNSAT **in 0.4 s** on a 97-gate region with 9 gates of
    slack.
  * fence SAT: 30 windows across slack 1–9, **0 SAT.**
  * a meta-review found dead-gate count and derivation rigidity **identical to four significant
    figures at 88/89/90/91/92** (2.312–2.326 options/gate; 0 dead gates in 1,200 samples per
    length) — **LR = 1.00.** It also *inverts* the campaign's own framing: against a proper null
    (random 88-mask subsets of the vocabulary at 0.495 options/gate), real 88s are **4.7× more
    derivation-rich, not rigid.**
  * completeness control: 4,200 planted-YES windows over 74 circuits, each decider branch tested in
    isolation by deleting the earlier branches — 462/462 and 33/33 recovered, zero oracle
    rejections.
- **Code:** `campaign_87/cert_audit/{plant_probe,control,case_hunt,slot_order_test}.py`,
  `campaign_87/wave5_2026-08-04/burn/simple/execute/audit_controls.py`, `campaign_87/wave5_2026-08-04/fence_sat/validate.py`.
- **Generality:** CIRCUIT-GENERIC — **the most transferable thing in the campaign_87 slice.**
- **Phase-2:** **keeper. Standing policy: no negative is reported without its one-gate-above
  control.**

### L2 · certificate control audit (the repricing) ★
- **Family:** meta-method — the only method in the tree whose subject is another method.
- **What it does:** Runs a negative-result instrument on inputs whose ground truth is *known to be
  positive*, to measure whether the instrument has any discriminating power for the question it is
  being read as answering. Three parts: (1) run the exact decider on circuits known to be
  improvable; (2) branch-validate the completeness proof by deleting earlier cases and checking the
  later ones still recover planted witnesses; (3) measure how much a SAT verdict depends on an
  encoding choice by permuting that choice.
- **Measured:**
  1. **97 @ 3, 94 @ 4, 92 @ 5, 91 @ 5, 90 @ 5, 89 @ 9 and an 88 @ 7 all have exhaustively empty
     k=2 shells (12,241 windows) and no reducible k=3 window in 8,400 sampled.** A 97-gate circuit
     — nine gates above best known — is **indistinguishable from an 88** by this instrument. The
     reason is scale: over 45 circuits with a smaller verified circuit available, the distance to
     that better circuit is **median 42 masks, min 3, max 48; 44 of 45 need k ≥ 8.** Certified
     radius is **3**.
  2. 4,200/4,200 planted YES windows answered correctly; 462/462 and 33/33 with earlier branches
     deleted. **No completeness bug — the ~165 M verdicts stand.**
  3. On provably-SAT windows the encoding returns UNSAT under **123 of 128 arbitrary mask
     orderings**, but under **128/128 legitimate topological reorderings the verdict does not
     move** (and the seed's own gate order is in that class). The depth-capped encoder's CNF is
     byte-identical under every reordering of the kept set.
- **Cost:** one day.
- **Code:** `campaign_87/cert_audit/`.
- **Generality:** **CIRCUIT-GENERIC — it is a discipline, not code.**
- **Phase-2:** **keeper, and it should be a gate on every negative result in phase 2.** The
  cheapest single improvement to method quality in the whole tree — it produced the project's most
  consequential result by *withdrawing* an inference rather than adding one.

### L3 · shape-matched random control (price the null, not the instance) ★
- **Family:** control / calibration methodology.
- **What it does:** For each real subset shape (dim, target count, target weights, support union),
  generates random instances of exactly that shape and runs the same exhaustive both-ways decision,
  to establish whether the measured quantity can be non-zero *at that shape at all*.
- **Twist:** it prices the *null*, not the instance. It is the method that retroactively voided a
  whole campaign's worth of negatives.
- **Measured:** **0 / 400** at every MixColumns shape with `n ≤ 3` — so three lanes' nulls at
  `n ≤ 3` **"carry no information about MixColumns whatsoever"**. At `n = 4` dim 8 it fires: **5/16
  (31 %)**, all 16 exhaustive. Reproduced an earlier lane's 48/400 control exactly.
- **Cost:** ~400 exhaustive instances, hours.
- **Code:** `experiments/e10_crossfam/code/{matched,density,pivot}.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper — the highest-leverage methodological item in the experiments slice.**
  *"A null is worthless unless the matched control fires"* should be applied to any new circuit
  before spending search budget.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — the scope of "0/400" is overstated and the run's own PARTIAL status is dropped.** The count 0/400 is exact, but "0/400 at every MixColumns shape with `n ≤ 3`" is contradicted by the primary log: `matched.py` enumerated **8** distinct shapes at dim ≤ 9 and reported only **5** — the three dim-9 shapes `(9,[5,5])`, `(9,[5,5,5])`, `(9,[5,7])`, all of them n ≤ 3, never ran, and `matched.log` ends with **no final `MATCHED CONTROL:` summary line** because the process was killed. The lane is honest and this entry is not: the ledger row carries `"status": "PARTIAL - process stopped to respect the concurrency cap; per-shape rows below are complete as printed"`. **Correct claim: "0/400 at every shape of dim ≤ 8."** The CIRCUIT-GENERIC label is defensible — `matched.py` is fully dim-generic and shapes are read from the ledger as data.

### L4 · partial-budget worthlessness calibration
- **Family:** instrument diagnostics.
- **What it does:** Plants instances that *provably* have a `k`-gate program and asks the searcher
  for SAT at that `k`, measuring how much of the level must be consumed before the solution is
  reached.
- **Measured:** one instance SAT in **6.1 s**; a second consumed **1,583,819,419 nodes (0.82 % of
  the level) without reaching any solution**, though one is guaranteed to exist. Conclusion:
  *"no SAT found" at dim 10, k=12 under any partial budget carries almost no information* — which
  retro-voided an earlier lane's 90-second k=12 probes (0.02 % of the level).
- **Phase-2:** **keeper — should be run before any new partial-budget search programme is funded.**
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL on entry completeness** (every number is exact against the ledger row). **This entry has no `Code:` field and no `Generality:` field**, breaking the catalog's own template and leaving the reader no path to the instrument. The code is `experiments/e11_quad10/code/planted10.py` (`DIM, NT, W, K = 10, 4, 5, 12`; `plant_directed` / `verify_plant` / `check_witness`, every plant required to contain a cancelling gate) and it is genuinely **CIRCUIT-GENERIC** — no MixColumns anywhere in it. Only the starter-kit cross-reference names the file; the entry did not.

### L5 · brute-force oracle validation (with a vacuity gate)
- **Family:** instrument control.
- **What it does:** Decides random small instances twice — once by the searcher under test, once by
  a definitional brute force over the *full* mask universe — and **requires the batch to contain
  genuine negatives or be declared vacuous and discarded.**
- **Measured:** 120/120 agreement; distribution `0:1, 1:23, 2:42, 3:30, >3:24` (24 genuine
  negatives). **This control caught a real bug**: a first C implementation failed 8/120 (a stale
  candidate-map entry made it *miss* completions, i.e. produce false negatives). And an independent
  verifier's *first* 120-instance batch produced zero genuine negatives — it **declared the batch
  vacuous and regenerated it with a weight-4 target floor, unprompted.**
- **Code:** `fleet1/laneC_proofside/code/validate.py`, `verify1/{oracle,xcheck}.py`.
- **Phase-2:** **keeper — the discipline, not the code.** Every negative in fleet1–4 traces back to
  a control of this shape.

### L6 · five-control stack (what a defensible exact negative looks like)
- **Family:** verification discipline.
- **What it does:** Five independent controls on one exact campaign: witness replay (45/45),
  escalation SAT (41/41 `sat` at the exact value after exhaustive `unsat` below), matched seeded
  control at the *same free-gate budget* (39/39 fired), two-engine agreement SAT vs DFS (131/131, 0
  disagreements), symmetry-free recheck of an intricate value-lex rule (6/6 reproduce), and oracle
  round-trip (39/39 assembled 32-output circuits VALID at exactly `n+k = 88`). Plus a DFS self-test:
  **3,972 random instances against a brute force over gate *sequences* sharing no code, 0
  mismatches.**
- **Phase-2:** **keeper as the template. Copy the stack wholesale.**

### L7 · four-control suite (C0 / C1a / C1b / C2 / C3)
- **Family:** verification discipline for a constraint model.
- **What it does:** C0 model sanity with the hard feature forbidden; C1a **solver-free**
  representability of 9 real circuits (problems = 0 on all 9); C1b representation *with* the solver
  on 8 donors at six depths, each hit exactly on its own gate count; C2 the sampler control whose
  absence voided 143 configurations; C3 a per-configuration control run on the very configuration
  that produced the negative.
- **Measured:** 9/9, 16/16, PASS, and 6 of 6 stage-B controls green. The one recorded FAIL is C0's
  first unhinted run — **kept in the ledger on purpose** because its diagnosis (no incumbent in
  622 s, dual bound 93.0) is what produced the greedy hint.
- **Phase-2:** **keeper** — C1a in particular (check by hand that a real solution satisfies every
  constraint before trusting any INFEASIBLE) is nearly free and catches encoding incompleteness.

### L8 · cap-off control (two-implementation equivalence)
- **Family:** control / instrument validation.
- **What it does:** Runs the depth-capped solver with the cap switched off on the **ten real blocks**
  of the architecture and checks it reproduces the independent plain oracle gate-for-gate.
- **Twist:** a genuine two-implementation control, not a tautology — the fast solver re-implements
  the base CNF rather than importing it, and with `depth=None` no level variable is emitted at all.
  It runs on real instances, not toys.
- **Measured:** **10/10 AGREE** (B27 1, B37 4, U07 12, U1 6, S2W 7, W3 8, U4 7, S5W/S6W/S7W 7). The
  fast solver is also **2–7× faster** on every row.
- **Cost:** ~6 min.
- **Phase-2:** **keeper — run this first on any new circuit.** The cheapest possible proof that the
  fast instrument has not silently diverged.

### L9 · greedy upper-bound control (a liveness check attached to every negative)
- **Family:** control.
- **What it does:** On **every single solve invocation**, re-runs a cheap greedy constructor on
  *the instance actually being solved* and verifies its output. If that fails, the driver refuses
  to report any negative.
- **Twist:** it is a *liveness* check attached to every negative, not a one-off self-test.
- **Measured:** greedy program of 16 gates, `verify_slp` True, re-run and re-logged at the top of
  every solve; plus a positive control on a sub-instance whose optimum was known monolithically
  (UNSAT 5, UNSAT 6, SAT 7) — the cube driver found the SAT at cube 144 with a verified witness,
  **proving the instrument finds programs when they exist, at dim 16, through this harness.**
- **Cost:** ~3 s per invocation.
- **Phase-2:** **keeper.** *"Positive control C2 is what makes any negative non-vacuous."*

### L10 · derive-family vacuity audit ("was the constant even inside the family?")
- **Family:** structural analysis, no solver — a guard on *other people's* results.
- **What it does:** When a package claims a constant is "derived", this checks whether the constant
  was even **inside the family the derivation searched**. If it was not, the derivation is vacuous —
  it proved nothing about the thing it is cited for.
- **Measured:** the audit found **three of four derive runs vacuous by construction** — all three
  `Q1` values and `D37`'s `δ₄(4)` cost 2 and lay outside a family searched at `max_cost=1`.
  Widening to `max_cost=2`: `Q1` goes 0/3 → **3/3**, `D37` 3/4 → **4/4**, and the widened derive
  **selects the configured triple exactly.** A follow-up showed this is **menu-robust**: the
  configured commitments lie inside the widened family for **every one of 40 menus, including the
  empty menu**, though the offered family itself swings 28 → 129 (4.6×).
- **Twist:** the audited code was more honest than any summary of it (*"Always check
  `family_contains_configured` before reading a derive result"*).
- **Code:** `fleet12/laneF1/famcheck.py`; the `SLP_DERIVE_MAX_COST` patch.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper. "The project's best epistemic device."**

### L11 · slot-order sensitivity test (mandatory before quoting any windowed UNSAT)
- **Family:** audit.
- **What it does:** Re-emits the same window CNF under different gate orderings and checks whether
  the verdict survives.
- **Measured:** **arbitrary orderings manufacture UNSAT on 123 of 128 provably satisfiable
  windows** — the caveat is load-bearing and must never be dropped. But **128/128 legitimate
  topological reorderings preserve the verdict**, and the seed's own order is in that class, so the
  campaign's UNSATs are not wrong — **they are correctly scoped.**
- **Code:** `campaign_87/cert_audit/{slot_order_test,d6sat_order_test}.py`.
- **Phase-2:** **keeper (mandatory before quoting any windowed UNSAT).**

### L12 · plan-space sizing (kill or unblock a formulation before building it)
- **Family:** pre-measurement, no solver.
- **What it does:** Counts the model size `|W|` a configuration would cost, **before anyone builds
  the model**.
- **Measured:** the per-child form is buildable at every `c ≤ 6` (`|W|` = 11,209 → 42,603) against
  a predecessor's unbuildable 87,897. **Seconds, no solver, and it retired a blocking argument that
  had killed a whole lane.**
- **Code:** `experiments/e3a_exploit/code/plansize.py`,
  `experiments/e6_cancelplan/code/{size,vocabsize,popsize}.py`.
- **Generality:** **CIRCUIT-GENERIC.**
- **Phase-2:** **keeper, top tier.** Cheapest possible way to kill or unblock a formulation.

### L13 · cost-curve pricing (price the next rung before buying it)
- **Family:** methodology / campaign planning.
- **What it does:** Measures the per-level cost growth of an exact search on real levels, then
  extrapolates to price the next rungs before spending them.
- **Measured:** killed generic climbing with a number: at the measured **10–17.5× per-level
  growth**, certifying `R01 = 22` costs **7.7e10 – 3.7e12 pod-seconds (~2,400 – 117,000
  pod-years)**; `R34` is astronomically worse. **No compute budget certifies the record regions by
  climbing.** The same technique repriced a proof-side ladder (`minE ≥ 7` at `|K| = 15` = 1e15–1e16
  nodes = pod-*months*, not the pod-day a predecessor note had budgeted) and an `L2` exact (a 2e15-node
  problem). Other measured multipliers collected in this catalog: ~16.6×/level at dim 16 (F10),
  ~7.8× per slot (F6), ~11× per level (H35), 26.4× then 20.2× (A11), ×10–25 per level (I9),
  ×~50 per level (G7).
- **Code:** `fleet1/laneB_regionbounds/code/pricing.py`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper — the single highest-leverage habit in fleet1–4.** It saved the project
  pod-months twice in one wave.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** The two proof-side repricings quoted here (`minE ≥ 7` at `|K|=15` ≈ 10¹⁵–10¹⁶ nodes, "pod-months"; L2 exact ≈ 2 × 10¹⁵ nodes) live in `fleet1/laneC_proofside/RESULT.md:613-615,479-481` and are **not** in this entry's Code field.

### L14 · constraint-ratio law (predict window difficulty, and read the caveat)
- **Family:** instrument calibration.
- **What it does:** Predicts window difficulty from `|req|/n` (required-outputs over free-slots)
  rather than from n.
- **Measured:** pooling two independent ledgers at fixed n — ratio 0.5 → 0/15 decided; 0.6 → 26/104
  (605 s); 0.7 → 110/139 (126 s); 0.8 → 178/180 (22 s); 0.9 → 176/176 (6.5 s); 1.0 → 39/39
  (4.1 s). A **~70× spread at fixed n**, and above ratio 0.8 n has no residual effect. It explains
  an apparent inter-track disagreement as a difference in *which windows each generator produced*.
- **Its own closing caveat, the important half:** *"a MORE constrained window is LESS likely to hide
  an 87, so the speed and the 87-hunt point in opposite directions."* **Every instrument that got
  faster in wave 6 got faster on the windows least likely to contain the answer.**
- **Phase-2:** **keeper — use it to *schedule* windows, and read the caveat before quoting a
  throughput number as progress.**
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** Two scope notes. The caveat is carried correctly and verbatim, but the entry's extension ("every instrument that got faster in wave 6 …") is **broader than the source**, which scopes the warning to this track (`STATUS.md:390-391`). And this entry carries **no `Code:` field** — the table is at `campaign_87/wave6_2026-08-11/hp_strike/STATUS.md:304-309`, the code at `compare.py`.

### L15 · prediction scoring + hash-chained pre-registration
- **Family:** methodology / discipline.
- **What it does:** Writes every prediction to an append-only ledger with a sha256 chain over prior
  entries **before** the corresponding solve runs, then scores strictly from the ledger, not from
  prose. Three earlier lanes had a ledger that wrote predictions at solve *completion* — which is
  not pre-registration. This one cannot be back-dated.
- **Measured:** one lane **15 of 18 met**; all three misses turned into structure rather than being
  explained away. Another lane: **MET 3 · MISS 7 · SPLIT 2 · UNDECIDED 2** over 14 predictions —
  and its RESULT.md records that an earlier draft said "MET 4", *"the ledger says 3, and the ledger
  wins"*. The misses are where the findings came from. Chain OK / 55 entries at hand-off; 320 rows
  now. Across the fleet slices pre-registration converted misses into findings: one lane 17 met / 2
  MISSED / 3 withdrawn; another 5/5 confirmed with an honest note about a mistyped verdict constant;
  a whole 87 theorem pre-registered at `2026-08-22T22:22:08` and came in exactly; another lane had
  **two of its own predictions refuted and reported both.**
- **Code:** `fleet8/unified/code/ledger.py`; sibling implementations in every lane.
- **Phase-2:** **keeper — adopt as the default.** *A 7-miss lane produced more than a 15-hit lane
  precisely because the misses were logged.*

### L16 · provenance audit (DERIVED / MEASURED / ASSUMED, with quarantine)
- **Family:** methodology / anti-circularity discipline.
- **What it does:** Tabulates **every ingredient** of a chain with four columns: where it is used,
  its provenance (DERIVED from definitions / INHERITED / MEASURED on circuits / EXPLICIT WITNESS),
  *can a hypothetical 87 violate it*, and *what breaks if it does*. Circuit-calibrated statements
  are then explicitly **quarantined** — named, and shown to appear in no proof.
- **Twist:** it states the **soundness asymmetry** explicitly: for a `min over admissible
  configurations` to be a valid lower bound, the admissible set must be a *superset* of every
  circuit's configuration, so **over-constraining is the circular failure mode and under-constraining
  is merely lossy.**
- **Measured:** 16 ingredients tabulated. Result: **not one constraint on admissible configurations
  is calibrated on a known circuit**; the three circuit-calibrated statements are all measured on
  circuits of ≥ 88 gates, an 87 can violate every one, and none is used in the load-bearing results.
  The sibling table for a generator adds the categories STILL-STATIC and RECORD-PROVENANCED.
- **Generality:** CIRCUIT-GENERIC — pure methodology.
- **Phase-2:** **keeper — adopt as the required section of every phase-2 writeup.** This is the
  direct antidote to the project's real failure mode: *a regularity observed on 88-gate circuits
  being used to describe circuits that are not 88 gates.*

### L17 · adversarial cross-desk referee (rebuild from source, share no code)
- **Family:** verification methodology. **Arguably the most valuable transferable asset in the
  whole tree.**
- **What it does:** A referee seat rebuilds every load-bearing object **from source with no code
  shared with the claimant**, and is barred from reading the claimant's `code/` until its own
  numbers are fixed. One referee constructed the MixColumns matrix a *third* way (byte-level 8×8
  GF(2) multiply matrices composed per coefficient) and asserted it equal row-for-row to the repo
  oracle's targets; another re-implemented a Check-1/subset-DP as a memoised recursion rather than
  the shared bottom-up loop.
- **Measured across the tree:**
  * e13 — 5 errors caught before publication, 5 produced by the referee itself, all caught by other
    lanes.
  * e14 — 10 catches / 10 self-errors / 10 withdrawn, seven of the ten caught by lanes; the
    referee's own worst call (a "strongest wall in the corpus" promotion) **fails in 660 circuits
    that were already on disk when the sentence was written.**
  * e15 — a cross-desk audit returned **FAIL** against a document whose figures all reproduced,
    because three figures had been carried from partial-run running totals rather than re-derived;
    all three corrected in place and the document then passed.
  * e17 — three VERDICT.md files, each with confirmed *and* refuted rows.
  * fleet slices — in four referee reports project-wide, **no claim marked PROVED was refuted, but
    several were narrowed and several sentences around them were false.** One referee confirmed two
    theorems, strengthened one to optimality, and found one real construction defect (a missing
    tie-break). Another lane's `verify1/` rebuilt a load-bearing negative **three ways** (own
    fixpoint checker, explicit hierarchies, separate HiGHS MILP).
  * A sibling protocol rebuilds an *external document's* claims from its **definitions** rather than
    its code: 8 verdicts — reproduced (a bi-mask layer, 184 AES incidences, both side-counts 57/97
    and 28/88 exact; "15 of 4,459" exactly), **corrected** (a "243 = 3⁵ manifold" is actually
    **729 = 3⁶**), **resolved** (the manifold is a *known* gauge orbit), and **FALSIFIED** (two
    "alien" 88s claimed outside the campaign's language are already in the 850,784-state census,
    same gauge orbit as a known one).
- **Code:** `experiments/e17_pure/REF_*/code/`, `fleet7/laneUNCOND/referee/` (17 files, 108-row
  ledger), `fleet6/laneTOOL2/verify1/` (22 files), `beat88/methods/m5_backbone/verify/VERIFICATION.md`.
- **Generality:** CIRCUIT-GENERIC.
- **Phase-2:** **keeper — mandatory for anything that will be published.** The recurring named
  failure modes (RELAY, SELF-EXCLUDING INSTRUMENT, FALSE CONFLICT, "a true statement carrying an
  unearned conclusion") are a ready-made checklist.

### L18 · meta-review (six independent red-team agents, scheduled *before* the spend)
- **Family:** audit.
- **What it does:** Six agents (auditor, framebreaker, forecaster, optimality advocate, outside
  view, explorer) independently attack the campaign's own claims and instruments.
- **Measured:** found **six live bugs on the ≤87 path** — pin-before-size, seen-before-verify, an
  export gate that had silently swallowed **1,821 of its 1,822 distinct 88s**, a gateCount schema
  mismatch, a silent SAT downgrade, and a 300,000-line harvest dedupe cap that froze the three most
  productive lanes for hours (~410k states discarded on one lane alone). **None had produced a false
  claim; several would have silently dropped a future 87.** The framebreaker produced the structural
  finding of the campaign: **the "540,579 distinct 88s" collapse to ~10–15 effective mask
  alphabets**, with 291,771 of them sharing one *set-identical* 113-mask vocabulary.
- **Phase-2:** **keeper — schedule one before, not after, the expensive runs.**

### L19 · fact-vs-mutable code audit ★
- **Family:** structural analysis (no solver) — **the single highest-leverage method in fleet9–12.**
- **What it does:** Walks a generator line by line and classifies every part as **ABSOLUTE FACT**
  (forced by the problem specification — a hypothetical better circuit could not violate it) or
  **MUTABLE** (a choice someone made, which a better circuit is free to ignore), and for every
  mutable part asks what it would cost to swap it. Three independent auditors, then an adversarial
  referee who re-verifies by recomputation and merges.
- **Twist:** it is the only method in the repository that measures **how much of a "result" is
  actually a modelling assumption.** The referee layer is what makes it work: 68 rows were claimed
  ABSOLUTE FACT and **22 were downgraded**, twenty of them from one systematic error (auditors
  invented classes the template does not contain).
- **Measured:** **244 rows** · 47 FACT / 116 MUTABLE-load-bearing / 81 inert · **22-entry defect
  register**, 5 at severity 1, 2 of those live in artefacts on disk · a 17-item ranked successor
  list. Headline finding: **the shipped-88 run proved no per-block minimum at all** — all ten blocks
  returned SAT at their first tested k, which was the inherited hint, so **18 gate-levels were never
  tested** and the instrument's own machine-checked floor was **70, not 88.** Second: **"if U1 is 5,
  the model prices 87"** — a single dim-12 solve away (both closed by H47 with ~4 core-hours).
- **Cost:** read-only; every check a one-liner under 90 s. **No solver run.**
- **Code:** none (documents). Schema at `fleet12/laneAUDIT/TEMPLATE.md`; result
  `fleet12/laneAUDIT/AUDIT.md` (188 K).
- **Generality:** **CIRCUIT-GENERIC — a methodology, and the template transfers unchanged.**
- **Phase-2:** **keeper, and the single highest-leverage method in its slice.** It generated
  everything fleet12 then went and bought, and it found real 87-shaped openings.

### L20 · audit from banked artifacts + the forgery sandbox
- **Family:** referee-facing self-audit, **with a demonstrated limitation.**
- **What it does:** Re-checks a theorem from the banked artefacts only — that the decided rows are
  exactly the claimed set with no duplicates or extras, that every row is a capped UNSAT or a
  well-founded prune, that all 720 solver logs independently report `exhaustive: true`, that all 720
  instances rebuild byte-exactly, and that the named controls fired.
- **Measured:** PASSES every check. **But finding F-6: passing is a *consistency* check, not
  tamper-evidence — it can be defeated by a forged log+instance pair.** The referee built two
  sandboxes to demonstrate this and then **re-executed the oracle itself rather than trusting the
  audit.**
- **Code:** `fleet3/laneCB_completeness/code/audit_door.py`; sandboxes 536 KB.
- **Phase-2:** **keeper, with the caveat shipped alongside it.** *Attack your own audit script and
  keep the attack* is itself worth copying.

### L21 · lineage-independence control (effective n, not raw n)
- **Family:** statistical control on corpus-wide claims.
- **What it does:** Before computing any statistic over a corpus of circuits, clusters that corpus
  by lineage (here at Jaccard ≥ 0.90) and reports the number of *independent* clusters, against a
  size-matched null.
- **Measured:** 1,063 cuttable orbits collapse to **13 clusters** (largest 686, then 295; two basins
  hold 92 %), while a size-matched rigid null gives **850** clusters. **Every statistic computed
  over "1,076 cuttable orbits" has effective n ≈ 13.** Applied as a descriptor control it halves or
  kills the campaign's own signature descriptors (`deg_max` AUC 0.823 → 0.662; `sh_out_neutral`
  dies at 0.555) and *rescues* one the campaign had rejected using the **wrong** control
  (`sh_fixed_masks` survives at 0.660).
- **Phase-2:** **keeper — apply to every corpus-wide statistic before it is published.**

### L22 · identity-first autopsy (was the measurement arithmetically forced?)
- **Family:** repricing discipline — structural derivation replacing a measurement.
- **What it does:** Takes a headline measurement and asks whether it was *arithmetically forced*,
  before treating it as evidence.
- **Measured:** **"the 536" DISSOLVED.** It is **268 sites doubled** (each contributes an A/B mirror
  pair; 268/268 are exact mirror pairs), so any reading of "536 opportunities" over-counts by 2×.
  The instrument's headline ("the mint is never buildable") is an **identity**:
  `δ(W) ≥ max(δ(mc1), δ(mc2)) − 1`, and `max(...) = 4` on **536/536**, so `δ(W) ≥ 3` and "buildable"
  (`= 2`) **was impossible before the scan ran.** Sharpest form: `max(δ) ≥ 4` holds at **99.47 % of
  all k=1 candidate sites in the corpus.** Also established as an *equality*:
  `d(W) = minrep(W | S) − 1` exactly (a DAG of `k` XOR gates has at most `k+1` leaves; an `m`-term
  XOR costs `m−1`). The mints are ordinary: **97.6 % (523/536) are masks some known 88 already
  builds**, 0/536 are target masks.
- **Pre-registration:** predictions timestamped **13:04:17Z before any completion code existed.**
- **Code:** `experiments/e16_lastwish/lane536/{extract536,charBC,quantE,jointE,ksplit}.py`.
- **Generality:** CIRCUIT-GENERIC as a *method*; the identities are generic XOR facts.
- **Phase-2:** **keeper — this is the repricing discipline.** Its own summary: *"the number was
  real, the evidence it carried about 87 was much smaller than its size suggested."*

### L23 · success-branch rehearsal (`sat_compile`)
- **Family:** plumbing control on the branch nothing tests.
- **What it does:** Takes a block-level SAT witness and pushes it all the way through the production
  generator to a full 32-output circuit, verified twice by the oracle — so that if the decisive
  solve ever *does* say SAT, the path from "witness" to "verified circuit" is already known to work.
- **Twist:** it is a **control on the success branch**, which almost nothing else in the repository
  has.
- **Measured:** run on a real 15-gate witness (constructed from the replay bound) and emitted a
  verified **88 at depth 7**, confirming the arithmetic `88 − 15 + 14 = 87` end to end. Handover
  checks passed, `verify_circuit.py` VALID twice (rc 0/0).
- **Code:** `fleet11/laneCUBE/code/sat_compile.py`. *(LIVE directory — read only.)*
- **Phase-2:** **keeper as a discipline — rehearse the success branch before you need it.**

### L24 · instrument repair with regression separation
- **Family:** tooling / soundness.
- **What it does:** Six minimal, separately-verified, separately-revertible fixes to the search
  instrument itself, each closing a path by which a *non-result* could be published as a *result*: a
  crash or an exhausted loop bound can no longer be reported as "provably infeasible"; the
  solve-cache key now contains the hint and the gate cap so an unhinted control can no longer be
  served the hinted answer; the dead-gate strip is on by default; and — crucially — **the regression
  suite's pass condition is split** into "the circuit verifies 32/32" (still asserted) and "the
  emitted count is exactly N" (a recorded observation).
- **Twist:** the regression split is the part nobody asks for: **a suite that pins current behaviour
  is a suite that red-flags its own corrections** (four of nine rows would have gone red for being
  right).
- **Measured:** all six applied and verified; all nine regression rows VALID at their corrected
  counts; the default configuration still emits **88, VALID, 66 + 22** from a clean environment
  **with the entire shipped cache orphaned by the key fix** — every one of the ten block prices was
  re-solved, not served. The naive regime now emits **108 @ depth 3** where it emitted 116. The
  serial solver path turned out to be **1.2×–31× faster** than the multiprocessing pool with
  byte-identical level logs, and **the pool deadlocks** (two live examples, ~0 CPU, four defunct
  workers, and the per-block timeout cannot fire because the parent is blocked rather than counting)
  — so serial became the default.
- **Code:** `fleet12/laneLIB/PATCHES.md` (B1–B6), `pristine/*.pre_laneLIB` (13 files).
- **Phase-2:** **keeper.** These are the fixes that make every later negative believable.

### L25 · radius-hypothesis significance test (the best-designed experiment in the tree)
- **Family:** experimental design.
- **What it does:** Matched TEST budgets and matched descent seeds per trial index, arms analysed by
  **achieved** rather than requested radius, an r=0 paired null that is simultaneously a live
  positive control, and controls **interleaved every 8–10 trials rather than front-loaded**.
- **Measured:** on the one anchor whose control fires (n=70, 33 descents), P(descend) is **flat** —
  0.43 at r=0, 0.67 at r=15–26, 0.32 at r=27–45; permutation **p=0.35 with a *negative* effect
  direction**; every Fisher p ≥ 0.19. Interleaved control **14/14 fired.** The other five anchors'
  nulls never fired and their arms are reported as **VACUOUS**, explicitly.
- **Code:** `experiments/e9_radius/code/trial.py`, `tally.py --trend --fisher --disp`.
- **Generality:** **CIRCUIT-GENERIC** (a design, not a search).
- **Phase-2:** **keeper, top tier. Reuse the design wholesale.**

### L26 · positive-only probe (a miss that carries no information, logged as such)
- **Family:** honest-negative discipline.
- **What it does:** A probe whose miss carries **no** negative information, logged as such so nobody
  later reads it as a refutation.
- **Measured:** on a cached 10-gate depth-5 witness, three of its four targets sit at level 5 and no
  single added mask (of the 227 level-feasible over the whole `2^12` span) brings all three down to
  4. Logged `kind=repair, found=false, note="positive-only probe; a miss carries no negative
  information"`. It legitimately **shifts a prior without becoming evidence.**
- **Phase-2:** **keeper — the cleanest example of the discipline in the tree.**

### L27 · plane-cage discriminator (does my instrument's cage exclude known solutions?) ★
- **Family:** controlled experiment on an instrument's own assumption.
- **What it does:** Tests whether the ≤3-bit-plane confinement that most campaign instruments assume
  is a fact about optima or an artifact of the operator, by running matched-pair descents under a
  quota that forces a ≥4-plane gate versus a rarity-matched **sham** quota.
- **Measured (recomputed from the final 663-row ledger, not the frozen snapshot):** the ≥4-plane
  predicate is **free at the plateau — 88 on 120 of 120 held descents, price 0.00 gates** — while
  the rarity-matched sham quota costs ≈ **+0.87 gates.** Separately, a census of 11.7 M harvested
  state-lines found **31,016 distinct oracle-verified 88-gate MixColumns circuits containing a
  4-plane gate**, across 13 run files from four independent tracks. Price curve: max-planes 4 → min
  88; **5 → min 89** (1,137 circuits); ≥6 unobserved. 0 of 663 descents reached 87.
- **Honest negative in the same track:** a planted-optimum calibration **"CANNOT BE COMPLETED"** —
  the surrogate family is 20–25 gates easier than real MixColumns, so it calibrates nothing.
- **Generality:** CIRCUIT-GENERIC (the "does my instrument's cage exclude known solutions?"
  experiment).
- **Phase-2:** **keeper — the most important result of campaign_87 wave 6.** It invalidates the
  scope of every negative produced by a ≤3-plane-restricted instrument (F19 in particular).

### L28 · high-plane tier probe (close a frontier honestly and cheaply)
- **Family:** instrument-capability measurement.
- **What it does:** Offers the exact floor oracle masks touching ≥5 bit planes and measures whether
  an optimum ever uses one.
- **Measured:** **3,731 pools offering 7,755 ≥5-plane masks; used 0 times**; 95 % upper bound on
  per-pool usage **0.103 %**. The detector's positive control fires (336 injected masks used, plane
  counts `{2:297, 3:9, 4:2, ≥5:0}`). Corroborated with no new compute by rescanning another track's
  89,003 floors: 6,183 buildable ≥5-plane masks, **0 ever selected.** The structural reason:
  buildable rate for a random p-plane mask is **0.0000 at p = 5..8** (0.35 at p=3, 0.003 at p=4, 1.0
  at p=2) — making one buildable needs `k ≥ p−4` extra pool slots. Leave-one-out over 4,572 (pool,
  mask) pairs: removing a 5-plane mask **never** moves the floor (19/19).
- **Phase-2:** keeper — **a model of how to close a frontier honestly and cheaply.**

### L29 · the atlas adversarial-audit family (four instruments, port all four)
- **Family:** audit.
- **What it does:** Four distinct instruments:
  1. **from-scratch frame rebuild** — re-derive every foundational claim in a module importing
     nothing from the codebase. Verdict: frame sound, **zero convention slips**, and the compilers
     reproduce their outputs **byte-identically**.
  2. **independent instance rebuild** — rebuild the whole instance corpus from FIPS-197 with zero
     code reuse and diff bit-for-bit. Verdict: **5,623/5,623 MATCH**, 0 critical findings; landmark
     columns *predicted* from algebra and matched.
  3. **trust-graph audit** — map every claim to the artifact supporting it *today*, labelled MLV /
     single-lineage / weak / no-artifact. Found a genuine internal contradiction (a law withdrawn on
     line 158 and re-invoked as a premise on line 179) and one no-artifact claim shipped in a public
     explainer.
  4. **alternative-reading audit** — never "is this right" but "given it is right, what else is
     consistent, and would any decision change". Includes **null-model construction** and a
     **dependency trace of 'independent' verifications**. Found: nine more valid 88s sitting on disk
     unexamined; "better ⇒ more disciplined" is false; **the finisher's frozen geometry is 88@5's
     mask set exactly, and 13 of 14 known 88s fail the freeze**; the three "independent" solver
     lineages share **one** instance generator; a four-way target-mask agreement is really 2-way; a
     landmark's pass mark was a **numeral collision** that would have manufactured a false positive
     on the null.
- **Generality:** **CIRCUIT-GENERIC and the most transferable material in the atlas slice after the
  oracle.**
- **Phase-2:** **keeper — port all four verbatim.**

### L30 · reproduce-harness (frozen single-move demos as pedagogy and smoke tests)
- **Family:** reproducibility / pedagogy.
- **What it does:** Three self-contained demonstrations of one move each, on *superseded* records:
  method `"91"` (plateau walk over equal-size circuits from a published 92 until one gate becomes
  removable → 91 @ 6, **6.7 s**); method `"89"` (value-set walk, remove-1 + remove-2-add-1 hub,
  cutting 90 → 89 at unconstrained depth, **150 s**); method `"90"` (irreducibility proof of a 91:
  duplicate scan, peel, all-pairs remove-2-add-1, **0.2 s**). Each reads as *one move* rather than a
  tuned kernel; deliberately frozen at v1.
- **Measured:** all re-validated on one core. Honest negative recorded in the README: from nothing,
  method `"89"`'s walk floors near 92 — **the 89 needs its seed.** Separately, the harness
  **reproduced the record 88@d7 gate-for-gate, every iteration index, 18 days and one refactor
  later — the search is deterministic.**
- **Code:** `reproduce/reproduce.py` (996 LOC), `reproduce/seeds.py` (77 LOC), `reproduce/hunt_88.py`.
- **Phase-2:** **keeper as pedagogy / smoke tests**, superseded as search by the v2 engines.

---

# Family M — Hand reasoning and theorem lanes

No solver in the loop. This family contains the project's proof that a reasoning
fleet can reach a SAT-derived record.

### M1 · cluster-currency hand reasoning (a reasoning fleet reconstructs the record) ★
- **Family:** hand reasoning, refereed, no solver anywhere in the loop.
- **What it does:** Partitions the 32 outputs into clusters and planes, develops a "currency"
  algebra of shared sub-masks, prices every mechanism as an explicit gate list, and composes cluster
  blocks into a full circuit; an adversarial audit lane recounts every claim and every assembly is
  oracle-verified before banking. **The ledger law is *"no count without a gate list"*.**
- **Measured — THE HEADLINE:** the trajectory **106 → 97 → 91 → 90 → 88** (flat+F1 at 106; a cluster
  frame at 97; three independent 91 witnesses; `corner90`; then the composition at 88), and the
  composed 88 is **gate-for-gate the known record**: *"all 88 operand-mask pairs coincide; the two
  circuits differ only in topological ordering"*. Re-verified in the slice pass:
  `assembly_stage5.json` → `gates=88 depth=5 outputs_built=32/32 problems=0 — VALID`. **It
  reconstructed the optimum from scratch by reasoning; it did not find a new 88 and did not reach
  87.**
- **Cost:** one multi-agent session; every claim single-core seconds-to-minutes.
- **Code:** `experiments/e13_hand87/cluster_campaign/assemble.py` plus lane scratchpads.
- **Logs:** `cluster_campaign/RESULT.md` (14K), `AUDIT.md`, `LEDGER.md` (73K), `C012.md`/`C34.md`/
  `C567.md`, `RECORD_TAPWORLD.txt`, and the stage ladder `assembly_stage0..5.json`
  (108/97/…/90/88).
- **Generality:** MC-HARDCODED in its content (planes, taps, Fano interfaces), but the *method*
  (cluster/currency frame + adversarial pricing) is transferable.
- **Phase-2:** **keeper — the single most transferable methodology in the experiments-late slice**,
  and the proof that a reasoning fleet can reach a SAT-derived record.
- **AUDIT (2026-08-29, `wrapup/day2/CATALOG_AUDIT.md`):** **FAIL — the 88 is real; "from scratch" is not.** I had the oracle re-run on `experiments/e13_hand87/cluster_campaign/assembly_stage5.json`: `gates=88 depth=5 outputs_built=32/32 problems=0 / VALID`, and the trajectory `106 → 97 → 91 → 90 → 88` is verbatim in the lane. But this entry claims *"it reconstructed the optimum **from scratch** by reasoning"*, and the lane's own ledger records `## 3j. ARCH: the record's tap-world DECODED (RECORD_TAPWORLD.txt, round 1)` followed by the round-2 assignment `C012 mine RECORD_TAPWORLD.txt`. Mtimes fix the order: `RECORD_TAPWORLD.txt` 15:27 → `C012_corner90.json` 15:46 → `C012_composed88.json` 16:03, and `RESULT.md:46` itself says the 90 used "**the record's C0/C1 corner mechanisms**". The **106→97 rungs predate the decode; 91→90→88 do not.** "No solver in the loop" is true; "from scratch" is not. It remains a genuine method (frame + priced gate lists + adversarial recount + oracle-gated banking) — only the independence claim fails.

### M2 · pure-reason theorem lanes (four parallel proof attacks with graded claims)
- **Family:** proof by hand, no SAT and no search.
- **What it does:** Four parallel lanes each attack one route to a lower bound — a conjecture chain,
  a `κ`/`Y` ledger, the assume-87 programme, and the derivation of a live anomaly — with every claim
  graded **(a) proved / (b) proved-modulo-a-named-lemma / (c) conjectured**, and with the standing
  rule that **a corpus fact can never filter a hypothetical 87.**
- **Measured:** the four outcomes are catalogued individually (I29, I30, I12, K2). Nothing narrows
  `56 ≤ L(M) ≤ 88`, and the campaign's own summary is that **`H87` survives every currently-live
  conjecture** — even under "the most generous simultaneous grant" the conjunction yields only
  `L(M) ≥ 73`.
- **Cost:** 1 core, `nice -n 15`, seconds-to-minutes per numeric check.
- **Code:** `experiments/e17_pure/lane{CHAIN,Y,CONTRA,DELTA}/code/`.
- **Generality:** MC-HARDCODED in content, CIRCUIT-GENERIC in method.
- **Phase-2:** **keeper.** This is the only family in the whole project that produces statements
  about a circuit that does not exist.

### M3 · hand-reduction algebra (the parity-hub law)
- **Family:** hand reasoning, no code, no data.
- **What it does:** A human-legible algebraic dissection of what the 88-gate circuits actually
  compute — bit-plane parities `P_i`, the carry structure of xtime, and where each circuit spends its
  gates.
- **Measured:** identifies the **parity-hub law** — the 88/89 separator is exactly "materialize ≥1
  plane parity as a cross-orbit hub"; each hub costs exactly 1 gate and serves ~3 targets in two
  orbits; **89/90/92/96/97-gate circuits have none.** And a corpus-wide blind spot: **all observed
  hubs lie in {P1, P2, P4, P6} — precisely the parities usable without touching P7 — while P7 is the
  unique quadruple-duty mask**, appearing in all four carry-orbit terms. Every known circuit instead
  re-buys P7 fragments per letter, and *"the invariant 21-gate xtime-carry toll is exactly the cost
  of refusing to materialize P7 once."* Uniform across all eleven circuits examined.
- **Code:** none (48 KB of prose analysis).
- **Generality:** MC-HARDCODED.
- **Phase-2:** **keeper — the densest single *unexecuted* hypothesis in the campaign_87 slice.**
- **COMPLETED (2026-08-29):** this entry was one of the nine Appendix A skeletons. The full schema-conformant entry, written from primary sources by `wrapup/day2/CATALOG_AUDIT.md` §3, is **Appendix A §A·3**.

### M4 · counterexample-family construction (kill a conjecture's class-level form)
- **Family:** hand reasoning + exact verification.
- **What it does:** Builds an explicit matrix family `A_k` whose optimum and whose *unique* optimal
  SLP are both provable by hand, then confirms with an exhaustive solver at small `k`.
- **Measured:** `L(A_k) = 5k`, every optimal SLP has exactly `k` fanout-1 inputs. A referee
  re-derived it, ran the exact oracle to exhaustively proven optima (`L(A_2)=10`, `L(A_3)=15`) and
  enumerated **all** optimal SLPs for `k = 1..6` — **exactly one each**. **Kills the class-level form
  of the `C_c` conjecture** — but the referee then bounded what it shows: `A_k` needs
  `#rows/#cols ≥ 1.67` while the chain invokes `C_c` only at `≤ 1.39`, so the missing hypothesis is
  **coarse** ("average row weight ≥ 4"), not fine structure of `M`.
- **Code:** `fleet1/laneC_proofside/verify2/{ak,ak2,claim3}.py`.
- **Phase-2:** **keeper — the cheapest way to kill a conjecture's class-level form**, and the
  referee's regime analysis is the template for not over-reading it.

---

# Family N — Documentation, planning and provenance

### N1 · swappable-parts catalogue (the phase-2 planning document)
- **Family:** meta / planning.
- **What it does:** Turns L19's row-by-row classification into an operational catalogue: for every
  part that is a real axis, where it lives, the mechanism that swaps it, the **tractability guard**
  that stops the swap becoming the original intractable problem, the verdict so far, and the cost of
  buying it if unbought. It prices the *unbought* axes.
- **Measured:** **25 axes** catalogued — 6 CLOSED, 4 MEASURED above 88, 11 OPEN with costs, 1
  FRONTIER, 2 INTRACTABLE, 1 needing new machinery. Three hard limits, each already paid for in
  core-hours: *"never widen a block past dim 16"*; *"merges at k ≥ 14 are the priced-dead
  frontier"*; *"one mutation per run"*. Its honest paragraph is the best one-paragraph summary of the
  whole campaign: *"every mutation measured so far returns exactly 88 … everything cheap enough to
  have been swept has been swept, and every one of those sweeps returned 88."*
- **Code:** none. `fleet12/LIBRARY.md`.
- **Generality:** CIRCUIT-GENERIC as a template.
- **Phase-2:** **keeper — this is the phase-2 planning document** (subject to staleness).

### N2 · cross-lane consolidation / discrepancy audit
- **Family:** documentation audit, no compute.
- **What it does:** Reads every lane's `RESULT.md` and the public repos, re-derives the line numbers
  and hashes against the *current* checkouts, and produces (a) a tiered state-of-the-problem with an
  evidence hierarchy REFEREED / PROVED / MEASURED / CONJECTURED, (b) a costed open-problems table,
  (c) a measured-dead-with-mechanism table, and (d) an explicit **DISCREPANCIES** section recording
  contradictions between files that nobody had caught.
- **Measured:** 46 `source_read` rows, **11 `discrepancy` rows**, 2 verifications, 2 deliverables.
  Found 11 live contradictions, including: `L_cf`'s upper bound quoted at **four different values**
  across current documents; an orchestration brief carrying three stale figures; **three different
  "known 88s" populations (139,878 / 3,254 / 14) used interchangeably**, with the 139,878 itself
  corrected to 105,801 in two other files; a brief still teaching the "radius is the failing
  dimension" diagnosis its own campaign refuted; the known-cell count off by one (20 vs 21); and **a
  decisive result banked in a log and written up nowhere.**
- **Cost:** zero compute.
- **Phase-2:** **keeper — and this wrap-up campaign is its successor.**

### N3 · dated corrections ledger (never rewrite a superseded claim)
- **Family:** documentation discipline.
- **What it does:** Never rewrites a superseded claim. A prior-art document opens with a
  reverse-chronological `## Corrections` log (5 dated entries); `bounds.json` `claim` strings gain
  "Updated <date>: …" sentences appended to the original text; the paper carries its own
  `## Corrections` section with note versions 2, 3, 3.1.
- **Twist:** it distinguishes *scope* entries from *correction* entries. One commit is explicitly
  filed as scope ("Nothing here is withdrawn and no figure changes") — it narrows how a true
  statement may be read rather than retracting it.
- **Measured:** it caught and recorded one genuinely false statement (a "remains the depth-5 point of
  the no-imported-material frontier" claim → "It does not") without disturbing anything around it.
- **Phase-2:** **keeper in substance** — but the current execution is 10,300 words long. A rewrite
  should keep the ledger and shrink the prose around it.
- **COMPLETED (2026-08-29):** this entry was one of the nine Appendix A skeletons. The full schema-conformant entry, written from primary sources by `wrapup/day2/CATALOG_AUDIT.md` §3, is **Appendix A §A·8**.

### N4 · naive-reader certification (a pass/fail criterion for a public writeup)
- **Family:** documentation / verification.
- **What it does:** Writes the algorithm in plain language, then hands it to a reader with **no**
  prior exposure to the repository, the problem, or any earlier round, who may read that one file
  and nothing else, and must restate the algorithm end to end and independently re-derive its
  mathematics.
- **Twist:** the reviewer reimplements from the prose alone — in one round they rebuilt GF(2⁸), the
  trace-dual basis, the τ coefficients, the shape algebra and all 32 target masks from the document,
  and **every stated value matched.**
- **Measured:** four rounds; round 4 = **PASS with two errata**, 38-step restatement, 4 gaps none on
  the main line. The process also surfaced **seven code-versus-documentation disagreements**,
  including that a `RESULT.md` states a tag is retired while the code still carries it.
- **Code:** none. `fleet12/laneALGO/ALGORITHM.md` + `NAIVE_READER_REPORT{,_v2,_v3,_v4}.md`.
- **Phase-2:** **keeper.** This is the method that produces the public writeup, and it has a
  pass/fail criterion.

### N5 · prior-art import + provenance audit
- **Family:** literature.
- **What it does:** Transcribes published circuits from papers, verifies each against the GF(2⁸)
  oracle, measures its depth (papers usually state none), and scores its distance from every project
  circuit.
- **Measured:** **12 circuits imported and all oracle-VALID** — 88@7, 89@9, 91@8, 92@6, 92@6, 94@5,
  97@4, 94@9, 95@6, 97@8, 99@3, 102@3. Feeding eight alien basins to the engine for ~5 h produced
  89s and **no 88s**. **Literature corrections on the record**: one ePrint attribution corrected; a
  91 that is in-place (s-XOR) and must not be cited as a g-XOR 91; **one paper's table says depth 6
  and this project measures depth 9**; one paper could not be obtained at all.
- **Code:** `campaign_87/agents/lit-88/{fetch_jean,import_jean88,import_sun89}.py`,
  `prior_basins/work/import_lib.py`.
- **Phase-2:** keeper — and `fetch_jean.py` (Playwright/cloudscraper against a Cloudflare-blocked
  ePrint) is the reusable part.

### N6 · records-hygiene audit
- **Family:** bookkeeping.
- **What it does:** Re-verifies every claimed record file through the repo oracle today, re-derives
  gate counts from the JSON (not filenames), recomputes both hash conventions, recomputes pairwise
  Jaccards, and writes a maintainer-facing line-by-line change list **without touching any published
  file**.
- **Measured:** found that **the published depth-4 frontier point is understated by a gate**: three
  independent oracle-verified 91@4 circuits exist on disk (cascade ladder / m3 census / atlas-M1
  reschedule; Jaccards 0.556 / 0.433 / 0.358 — **three genuinely distinct lineages**) while
  `README.md`, `spectrum.json`, `PAPER.md` and `PRIOR_ART.md` all still say 92@4. The shipped-92
  file hash reproduces `spectrum.json`'s pin exactly, validating the hash convention.
- **Code/results:** `fleet1/laneD_completions/RECORDS_UPDATE_NOTE.md` (154 lines, advisory).
- **Phase-2:** **keeper — and ACT ON IT.** Direct public-repo material. See Appendix B #7.

---
# (a) PHASE-2 STARTER KIT — the keepers, ordered by expected value on a new circuit

Ordered by what you should do first when aiming this toolkit at another circuit
(e.g. `aes_inv_mixcolumns`). "Port cost" is what has to change.

## Day 1 — nothing is trustworthy without these

| # | method | why first | port cost | code |
|---|---|---|---|---|
| 1 | **A1 spec-oracle** | every claim in this project is defined as "this printed VALID" | swap `[2,3,1,1]` → `[14,11,13,9]` and the weight self-check (~30 lines) | `verify_circuit.py` |
| 2 | **K1 B = n − q tripwire** | free, always-on, provably sound one-gate-improvement detector; feed it any foreign circuit | ⚠ **not "one constant" — ≥4 edits in 2 files, and only after row 1 is done**: `sweep.py:48,102,528` + `laneCUT/cut.py:22,34`. `count_B` itself is generic; the harness is not (AUDIT 2026-08-29) | `experiments/e15_campaign3/tools/sweep.py:296` (def; body at **310**), `:525-532`, `:730-738` |
| 3 | **J6 exact `Aut` + equivariance proof** | tells you the whole symmetry budget in 0.1 s and buys a free 4× on every later sweep | none (it takes a target set) | `experiments/e3b_fresh/code/symgf.py`, `fleet9/laneENUM/code/rho_equivariance.py` |
| 4 | **A10 validated kernel suite (B1–B5)** | closure / trim / repair / neighbourhood / gauge, 885,634 comparisons 0 mismatches | ⚠ **not "swap the target matrix" — edit and rebuild the C**: `csrc/slp_kernel.c:34,38,47` rebuilds the 32 MixColumns targets from `0x11B` and `{2,3,1,1}`, and the kernel is uint32/32-input width-locked (AUDIT 2026-08-29) | `beat88/methods/shared/` |
| 5 | **K2 Lemma R / T2 tripwire** | second free detector; violation *is* a smaller circuit (66 hits on non-optimal circuits, 5 compressed and oracled) | ⚠ **the theorems are generic, the code is not** — not "none": a new target generator plus four `n != 88` guards; all five scripts import `compose/frame.py` (`0x11B`, `coef=[2,3,1,1]`) (AUDIT 2026-08-29) | `experiments/e17_pure/laneDELTA/witness.py`, `cone_theorem.py` |
| 6 | **L1 + L2 positive-control policy** | **no negative is reported without its one-gate-above control**; L2 is why | none — a discipline | `campaign_87/cert_audit/` |
| 7 | **A2 cleanroom adversarial verifier** | 14 planted defects, all rejected — what makes "VALID" mean something | one constant (`INV_MATRIX` is already in the file). ⚠ 5 of the 14 cases are MC-matrix-specific, so the *suite* is not fully generic (AUDIT 2026-08-29) | **⚠ separate repo** `~/xor_ui/aes_mc_records/audit/cleanroom_verify.py` |

## Week 1 — get a circuit, then get a population

| # | method | why | port cost | code |
|---|---|---|---|---|
| 8 | **G1 `slp_opt.py` exact oracle** | exact minimum SLP for any small instance; the engine under half this catalog | none | `atlas/slp_opt.py` |
| 9 | **B2 naive roots + B1 anneal3** | clean-provenance start in one line; 97@3 from scratch in 81 s | swap the spec module | `pipeline/engines.py:engine_anneal3`, `constructors.build("naive", n)` |
| 10 | **D1 cascade ladder + D2 Pareto tie-break + D3 alt-worker** | the "point it at a circuit and walk away" recipe; the tie-break is free and produced every depth record | circuit-generic orchestration | `pipeline/ladder_parallel.py --mode cascade`, `worker.py` |
| 11 | **C1 walk + C2 LNS + C3 tuned knobs** | the only engines that ever produced an 88; C3 is the tuning table | swap the spec module | `pipeline/engines.py` |
| 12 | **D7 plateau harvesting** | turn the search into a census from day one — *the population is worth more than the record* | none | `pipeline/engines.py:_Harvester` |
| 13 | **B4 clean-room Boyar–Peralta** | prices what "no project knowledge" buys (93/94 here) | one `TGT[32]` array | `fleet10/cleanroom/work/bp*.c` |
| 14 | **J1 min-depth schedule (level-BFS/ASAP)** | free gates-at-depth; the only depth argument that is a theorem | none across circuits on 32 inputs; both files hardcode 32 (AUDIT 2026-08-29) | `pipeline/engines.py:relax`, **`fleet8/unified/code/assemble.py:91`**`:min_depth_schedule` (there is no `pipeline/assemble.py` — path corrected 2026-08-29) |
| 15 | **C16 ρ²-symmetric orbit search** | two of five 88s trace to it; the inverse matrix has the same Z/4 | needs the new `Aut` (same here) | orbit engine in the campaign archive |

## Weeks 2–4 — exact certificates and the honest negatives

| # | method | why | port cost | code |
|---|---|---|---|---|
| 16 | **E7/E8 window-cut `d(S)` sweep** | the workhorse local-surgery search; scales from 5 anchors to a whole population | oracle + target set | `experiments/e15_campaign3/tools/sweep.py` |
| 17 | **E1/E2 exact window deciders** | complete at k≤3 (and k=4), ~165 M verdicts *(⚠ now ruled a **stale under-count** — the k=2 half alone is 215,412,120; see `CONFLICTS_RESOLVED.md` Part D)*, cost nearly flat in k | swap the spec module. ⚠ **on reuse, add `assert not (window & TSET)` and switch to `time.monotonic()`** — see E1's AUDIT note | `evidence/campaign87_certificates/code/exact_window.py`, `exact_k4.py` |
| 18 | **E14 exhaustive small-SLP decision** | the cleanest "is this circuit one gate from smaller?" procedure the project owns | none | `experiments/e16_lastwish/lane536/slp3.py`, `le4_k2.py` |
| 19 | **L3 shape-matched random control** | *a null is worthless unless the matched control fires* — it voided a campaign's worth of negatives | none | `experiments/e10_crossfam/code/matched.py` |
| 20 | **L4 partial-budget calibration + L14 constraint-ratio law** | prices whether "no solution found" means anything at all | none | `experiments/e11_quad10/code/planted10.py`, `campaign_87/wave6_2026-08-11/hp_strike/compare.py` |
| 21 | **L13 cost-curve pricing + L12 plan-space sizing** | price the next rung / the next formulation *before* buying it; saved pod-months twice | none | `fleet1/laneB_regionbounds/code/pricing.py`, `experiments/e3a_exploit/code/plansize.py` |
| 22 | **J40 exact move census** | kills a bad parallel/decomposition design in seconds | none | `experiments/e1_regions/code/move_census.py` |
| 23 | **G19 Venn class reduction + G18 output-subset pricing** | prices the whole exact-subset programme before a single solver call (496 pairs → 8 runs) | needs the new target matrix | `experiments/e2_outputcost/code/classes.py`, `runner.py` |
| 24 | **G10 free-gate exact re-add** | converts a dim-32 question into "find ≤5 extra masks"; 41/41 exact | none | `experiments/e5_readd/code/` |
| 25 | **F17 minimise-never-decide MaxSAT** | the returned optimum is its own positive control; ≥400× faster than the decide form | swap the target list | `experiments/e4_depth/code/d4floor.py` |

## Month 2+ — the heavy machinery

| # | method | why | port cost | code |
|---|---|---|---|---|
| 26 | **H26 unified generator ★** | emits a verified circuit at a *requested* (count, depth) from theory | swap the target matrix; **re-derive the sector (p,q) decomposition** — see H26's Generality block | `fleet8/unified/` |
| 27 | **H27 law derivation** | derives the block architecture as code, not tables | L0/L2/L3/L4/L5 transfer (same field); L1 must be re-derived | `fleet8/unified/code/laws.py` |
| 28 | **H19 free-supply derive + vacuity guard** | one solve bounds a whole family; *never run it without the in-family check* | none | `fleet8/unified/code/derive.py`, `annotate_derive.py` |
| 29 | **H20 merged-derive** | cannot be mis-specified — delete the boundary and read the optimum | block names | `fleet8/unified/code/derive.py --derive` |
| 30 | **H22 replay bound** | the cheapest sound lower bound in the toolkit, one solve | none | `fleet3/laneF4_rule/code/f4model.py` |
| 31 | **F9 depth-capped exact oracle (`dslp`)** | the only oracle that can price depth; 2–7× faster than the plain one | none | `fleet8/unified/code/dslp.py` |
| 32 | **F8 GF(2)-explicit SAT encoding** | ~~5.4×~~ **4.04×** smaller CNF *(the 5.4× is computed from quarantined superseded runs — AUDIT 2026-08-29)*, median 9.3× faster, ceiling n=12→14. ⚠ the "V6 54/54" control claim is contradicted by its own log | **MIXED, not none** — `bench.py:55,313` and `hunt.py:65-69` are MC-bound | `campaign_87/wave6_2026-08-11/xor_encoding/xorenc.py` |
| 33 | **F12 resumable cube-and-conquer** | cube on **semantic positions**, never on gate 0 (measured 85× worse) | none | `experiments/e5_readd/code/cube.py`, `experiments/e7_push/code/cube.py` |
| 34 | **G2 `qsearch` + G4 `dfs_par`** | the two strongest exhaustive engines; `dfs_par` beats SAT exactly where SAT times out | target mask set only (dim wall at ~12) | `experiments/e8_quad/code/qsearch.c`, `campaign_87/wave6_2026-08-11/dfs_par/par.c` |
| 35 | **I12 laminar price certificate** | the **only** bound family in the project above 88; verifies in 2 s, stdlib, solver-free | rebuild `TARGETS`, re-run the ascent | `fleet7/laneUNCOND/code/lp_g.py`, `bstar.py` |
| 36 | **I5 + I7 gate-elimination chain** | `L ≥ 51` in one line; `L ≥ 56` refereed; likely **better** on the denser inverse matrix | ⚠ **"one-line target change" is materially false** (AUDIT 2026-08-29). For `L ≥ 51`: four lines plus a 4.6 × 10⁸-subset enumeration (`verify_bound.py:86-88` are unconditional MC tripwires). For `L ≥ 56`: a new keep-set certificate search, a new symmetry group satisfying Theorem N's covering hypothesis, **and a fresh 9.43 × 10¹⁰-node depth-4 exhaustion at pod scale** | `atlas/thinktank/proofside_code/`, `beat88/understanding/u3_lowerbound/verify_bound.py` |
| 37 | **H29 block-merge relaxation** | "enumerate every boundary, machine-check replay + strict generality, dissolve" — a complete recipe | block model | `fleet5/laneMERGE/code/` |
| 38 | **L19 fact-vs-mutable audit + N1 swappable-parts catalogue** | measures how much of a "result" is a modelling assumption; then prices every open axis | template transfers unchanged | `fleet12/laneAUDIT/TEMPLATE.md`, `fleet12/LIBRARY.md` |

## Standing disciplines to adopt on day 1 (no code to port)

**L15** hash-chained pre-registration · **L16** DERIVED/MEASURED/ASSUMED provenance table with
quarantine · **L17** adversarial cross-desk referee (mandatory before publishing) · **L18**
red-team meta-review *before* the expensive runs · **D18** env-gated one-mutation-per-run
protocol · **D17** budget CPU-seconds from `/proc`, never wall clock · **D16** identity-based
process control, `pkill` banned · **L21** lineage-independence control on every corpus statistic ·
**L26** label positive-only probes as such · **A9** dead-gate strip on every emitted count ·
**J5** gauge-canonicalise before quoting any "N distinct states".

---

# (b) FULL INDEX

309 entries. Verdict key: **K** = keeper · **K★** = keeper, top tier · **S** = superseded ·
**D** = dead-end · **U** = unfinished / open.

| id | name | family | one line | verdict |
|---|---|---|---|---|
| A1 | spec-oracle (`verify_circuit.py`) | verification | rebuild the matrix from GF(2⁸) and replay a circuit; the definition of VALID | K★ |
| A2 | cleanroom adversarial verifier | verification | second independent verifier + 14 planted defects, all rejected | K★ |
| A3 | verilog simulation crosscheck | verification | third path in a different language; convention insurance | K |
| A4 | canonical gate hash | integrity | formatting-independent SHA-256 identity, alongside a file hash | K |
| A5 | generated-artifact drift check | hygiene | hand-editing a generated file becomes a test failure | K |
| A6 | depth-tightness CI + differential unit tests | hygiene | verify at depth D and assert failure at D−1; fast kernels vs slow references | K |
| A7 | batched numpy verifier | verification | ~400 k circuits/s, live-gate counts, 100,009-circuit fuzz clean | K |
| A8 | realize-completion | verification | mask set → gate list → oracle in one call | K |
| A9 | dead-gate strip + honest-count accounting | hygiene | every count gap gets a named cause; 5 record 88s exist only because of it | K★ |
| A10 | validated kernel suite (B1–B5) | infrastructure | closure/verifier/index/descriptors/gauge, 885,634 comparisons 0 mismatches | K★ |
| A11 | SAT-benchmark packaging + identity proof | reproducibility | how to publish an artifact from an in-memory campaign; 51/51 hashes OK | K★ |
| B1 | anneal3 depth-3 annealer | construction | 97@3 from scratch in 81 s, beating the published 99@3 | K★ |
| B2 | naive random XOR-tree root | construction | seedless, provenance-clean root; ancestor of both from-scratch 88s | K★ |
| B3 | anti-vocabulary root construction | diversity | the only measured antidote to the house-dialect effect | K |
| B4 | randomized Boyar–Peralta (clean-room) | baseline | prices "no project knowledge" at 93/94 | K |
| B5 | partition-assemble-and-dedup | construction | Σ block costs ≠ realisable count; family-optimal glue ceilings at 105 | K |
| B6 | top-down algebra + peephole | construction | four unrelated designs land on exactly 108; best by reason 99@5 | S |
| B7 | algebraic frame derivation | construction | VALID 105 from a single-frame algebraic form, in minutes | K |
| B8 | backward frontier search | construction | published 96 does not survive the plumbing fix; best 104 | D |
| B9 | backward factorization search + `F` identity | construction | exact identity `F = 64 + a − c − 2d`, 67/67 | K |
| B10 | tri-search market | construction | mechanism works, economics refuted: 5–8 supply gates per rebate | D |
| B11 | NRPA | construction | 476,017 episodes, best 88; needs a vocabulary prior to work | K |
| B12 | evolve (LLM-authored operators) | meta-search | 407 descents, best individual P(≤88) = 0.04 | K |
| B13 | modular / glue-conditioned synthesis | construction | record-free population containing 3 records' full mask sets ⇒ floor ≤ 88 is a theorem | K★U |
| B14 | L_cf reuse-greedy + CP-SAT | construction | 103; superseded by an on-disk 102 | S |
| C1 | walk (value-set plateau) | local search | 480–640 it/s; every 88 came from walk chunks | K★ |
| C2 | LNS destroy-and-rebuild | local search | the workhorse; effective radius 0.24 masks at the frontier | K/D |
| C3 | merged-engine improvement bundle | local search | seven measured A/Bs: 17.5×, 21.9×, 34×, 12×, 7×, 11×, 2× | K★ |
| C4 | hub move (remove-2-add-1) | move class | 0 successes in 2.24 M samples at the frontier; cut 90→89 in 150 s historically | D/K |
| C5 | exact single-mask repair | kernel | complete enumeration beats sampling; the `valid[:4]` prescreen deletes 30–37 % of edges | K |
| C6 | complete remove-1-add-2 | neighbourhood | 3,070 new 89s + 79 88s, 63 unreachable by the shipped move | K |
| C7 | BFS plateau enumeration | local search | full neighbourhood in 0.1 s, 0 % revisit vs the walk's 22–68 % | K★ |
| C8 | syl-move | move class | first-ever drift on a frozen plateau: 26 new 88 mask sets | K |
| C9 | plateau drift with tabu + away bias | local search | 11× more states, exactly 0 more reach; measures the basin diameter | D/K |
| C10 | chained shake-and-recover | operator | radius at constant gate count, priced: 0.8 → 5.2–11.1 CPU-s/mask | K |
| C11 | periscope plateau walk | local search | the only walker with a non-monotone move; 116 → 90 in 150 s | K |
| C12 | zero-cost re-association | rewriting | removed the corpus's only value-glue gate; a failure localises what a gate buys | K |
| C13 | SAT window repair | local search | 2,623 attempts, exactly one improvement (94→93); dead near an optimum | K/D |
| C14 | demand-flow search (F,B bi-mask) | representation | same masks, different routing: 108 vs 100 gates — a positive control | K★U |
| C15 | demand-flow neutral-neighbourhood pricing | representation | 0 improving and 0 neutral moves at every calibrated prefix | D/K |
| C16 | ρ²-symmetric orbit search | symmetry search | two exactly symmetric 90s; seeded two of the five 88s | K |
| C17 | parity-pinned orbit walk | symmetry search | 56 injections all settle at 91; a two-gate move, not one | K |
| C18 | orbit-drop-and-readd | relaxation | relaxation bites, the re-add gives it back; beam is ≥1 gate loose | S |
| C19 | fixed-size infeasible search (FIXN) | relaxation | control fires 203× at the record; 767 oracle-verified 88s from infeasible states | K★ |
| C20 | fixed-87 genome QD search | relaxation | killed day 1 by its own control; 6,832,408 genomes exhaustive, 0 hits | D |
| C21 | latent-interface (gauge) climb | transformed space | passes its power control (97→91, 92→90…); seven 88-anchors pinned | K |
| C22 | Steinberg / transvection word search | group search | +0 after 400k iterations where the walk does 97→92 in 83 s | D |
| C23 | depth-capped worker / restart hunt | local search | cap-4 holds 92@4; 0 of 49 restarts reached ≤90 at depth ≤4 | K/D |
| C24 | depth-capped lane recipe (91@4) | composition | anneal3-as-ILS root + `--cap 4` walk; 92→91 in four minutes of one core | K★ |
| C25 | composition, splice and union crossing | recombination | 96,520 splices exhaustive, min 88; the wash identity | D/K |
| C26 | local-surgery pricing (laneBEND) | priced moves | chaining is +1 both ways; 4 of 5 knowns perfectly rigid | S |
| C27 | excursion probes PC001–PC005 | corpus surgery | 800,994 sites → 55,970 → 536 → 0, with fail-able controls | K |
| D1 | cascade depth ladder | orchestration | 92@4 from scratch in 2.67 h; the walk-away recipe | K★ |
| D2 | Pareto tie-break + continuous reseeding | acceptance rule | free; every depth record exists only because of it | K★ |
| D3 | alt worker mode | schedule | the mode of every record worker; 88@7 in 19.4 min on one core | K★ |
| D4 | hunt fleet supervisor | fleet | 16 workers, 19.74 h, 148,347 new 88 states; `pkill` banned | K |
| D5 | fleet restart loop | orchestration | 169 restarts, 14 reached 88, 14/14 opened a never-seen pocket | K★ |
| D6 | chunked reseed-from-best | orchestration | chunk reset wins on every axis; the shared memory does not | K/S |
| D7 | plateau harvesting | data generation | free; produced the population every certificate sweep ran over | K★ |
| D8 | cross-pollination | population | 3,651 merges, zero measured record contribution, high provenance cost | S |
| D9 | MAP-Elites structural archive | diversity | 198/198 cells, 0 new families — structurally blind | K/D |
| D10 | basin-diversity harvesting (repel) | diversity | 356 new 89 mask sets vs 4 previously known | K |
| D11 | island portfolio with migration | search control | migration never fired (0-byte logs); contributed nothing | D |
| D12 | mass basin census (intrinsic descriptors) | fleet | 6,304 descents, 747 core-h, 2,722 new families, 0 eighty-sevens | K/D |
| D13 | fresh-fleet power measurement | experiment design | 1,500 descents; P(87 per descent) < 2.00e-3; decay rejected at 99 % | K★ |
| D14 | region-partitioned concurrent search | parallel | worse than one instance by 1.4–2.6×; the regions are the cause | D |
| D15 | talk-channel ablation | protocol | PROTECT +8 %, DEMAND −26 %, all three together −53 % | K/D |
| D16 | ops harness (slot-guard / chain / procid) | ops | ALARM-only, never act; completion verified from ledgers not processes | K★ |
| D17 | CPU-second budgeting from /proc | instrumentation | wall clock is not a budget: 3 CPU-s in 238 wall-s at load 39 | K★ |
| D18 | env-gated one-mutation-per-run protocol | experiment control | inert-when-unset patches; tractability guards inside the patch | K★ |
| E1 | exact window decider (k ≤ 3) | certificate | ~165 M verdicts, 0 reducible; complete by proof | K |
| E2 | exact k=4 decider | certificate | 1,257/1,257 vs brute force incl. 122 NOs; cost nearly flat in k | K★ |
| E3 | complete small-core shells | certificate | the 88 wall and 89 wall; a complete k=3 shell of an 89 in 6 s | K★ |
| E4 | population-scale shell sweeping | certificate | family 3 CLOSED at k=2 (83 M decisions); 1,309,223 distinct 89 states | K/S |
| E5 | family census + irreducibility certificates | certificate | 10 proven-distinct families, 2,223,760 exhaustive decisions, all empty | K |
| E6 | cuttability census (pre-registered) | labels | 85,446 orbits labelled, 1,076 cuttable; the signature is repair richness | K |
| E7 | window-cut `d(S)` compressibility | surgery | the workhorse; `d(S)=1` closed by exhaustion on four anchors | K★ |
| E8 | population window sweep (B/FH/D3) | surgery | 17,283 rows = the entire distinct population, 0 compressible | K★ |
| E9 | complete k=3 shell (remove-3-add-2) | certificate | two complete 27,720-window certificates, controls positive | K |
| E10 | basin edit closure sweep (forbid step) | certificate | 27,720/27,720 twice, 0 completions at k ≤ 2; generated new verified 88s | K★ |
| E11 | all-drop-k local-optimality screen | certificate | 35,960/35,960 refuted, twice; radius up to 19 masks | K★ |
| E12 | exact 3-gate finisher | closure | all 1,540 triples dead on 243/243 plane choices; PC3 caught a real bug | S |
| E13 | frozen-exterior module search | structure | 22-mask backbone + five ternary planes; 6,918,660 3→3 combinations, zero | K/S |
| E14 | exhaustive small-SLP decision (`slp3`) | micro-search | shape-free; 2-mint/3-orphan regime CLOSED on the corpus | K★ |
| E15 | one-target-short completion probe | certificate | 1,630,797 objects probed exhaustively, 0 completions, 1,703 in self-test | K |
| E16 | thinker_c exhaustive completion scan | certificate | closes a 629,274-state pre-existing population nobody had analysed | K★ |
| E17 | down-step / reduction-lemma analysis | theory | every "remove k add k−d" reduces to one coordinate; reachable m ≈ 4–5 vs 42 | K |
| E18 | exact k−1 shell over all 2³² | certificate | 0 completions over arbitrary masks, by an unlock-event completeness argument | K★ |
| E19 | certifier inverted into a move generator | exact→local | complete radius-2 neighbourhood of an 89 in 56 s, 521 siblings | K |
| F1 | windowed FSK SAT | SAT | reached k=16; UNSAT relative to a fixed slot order | S |
| F2 | killable-subprocess SAT driver | infrastructure | sidesteps the interrupt bug; moved the frontier k=12 → 16 | K |
| F3 | symmetry-broken SAT (SB-P + SB-F) | SAT | 14–34× faster; 44/48 windows UNSAT, 0 SAT | K★ |
| F4 | SB-D depth-sorted symmetry break | SAT | 11× on cone geometry, +3 slots; 1.21× *slower* where there is no depth ladder | K |
| F5 | fence / topology-family SAT | SAT | the only caveat-free certificate class; killed as a discovery tool by its own control | K/D |
| F6 | slot-order-free window SAT | SAT | 399/408 UNSAT; ~7.8× per slot, the 13–14 escalation priced and declined | K |
| F7 | cone-window synthesis + convex-block band | SAT | frontier 10–12 slots vs 31–34 needed; 7 cone theorems; SB-D came from it | D/K |
| F8 | GF(2)-explicit XOR-native encoding | SAT | 5.4× smaller CNF, median 9.3×, ceiling n=12 → 14 | K★ |
| F9 | depth-capped exact SLP oracle (`dslp`) | SAT | the only oracle that prices depth; three controls all fired | K★ |
| F10 | joint-block boundary test (dim 16) | SAT | k=9..13 exhaustively UNSAT; ~16.6× per level; pre-flight caught 8 fake masks | K |
| F11 | monolithic SAT portfolio | SAT | 7.2–28.8× cheaper than cubing; loses everything if killed | K |
| F12 | resumable cube-and-conquer | SAT | cube on semantics (56/56 UNSAT), never on gate 0 (85× worse) | K★ |
| F13 | CNF partition machine-check | control | asks the solver, not the prose, whether the cubes partition the models | K★ |
| F14 | SAT set-blocking enumeration | enumeration | ~100× faster than the DFS; its own control caught an inverted polarity | K |
| F15 | SAT with banned/required values | forcedness | turns "the solver reached for X" into "it cannot do otherwise"; 10/10 control | K★ |
| F16 | RC2 MaxSAT alphabet floors | MaxSAT | 347,525 pairs, floor 88; power control fires at 0.7 % | K★ |
| F17 | exact alphabet-floor MaxSAT | MaxSAT | *minimise, never decide*: ≥400× the decide form, control built in | K★ |
| F18 | skeleton pools + RC2 floor generator | generate-decide | 88,908 pools at 4,818/h; stopped by its own kill criterion | K |
| F19 | pattern-class exact window floors | MaxSAT | 177 exact floors, 0 improvements; but the class implies ≤3 planes | K/S |
| F20 | union-subset and PB covering SAT | SAT/PB | radius-unbounded; 427 UNSAT, 0 SAT; the PB encoder was the capability gain | K★U |
| F21 | free-closer (one unrestricted mask) | SAT | escapes vocabulary conditioning by exactly one mask; 23/3/2 control audit | K |
| F22 | alphabet-restricted SAT ladder | SAT | self-refuted in capitals: K=96 UNSAT on a 97 with 9 gates of slack | D |
| F23 | global CP-SAT / min-union set cover | ILP | negative on every axis; LP provably vacuous; `linearization_level` finding open | D/K |
| F24 | cone-vocabulary ILS | set cover | a different paradigm lands on 88 6.8× more often than 89 | K |
| F25 | vocabulary-restricted ILP `Q(V,n)` | ILP | `Q(V*,87)` **was not reached and not answered negatively**; ceiling ~134 masks | K U |
| F26 | cancellation-plan CP-SAT (per-child) | CP | first non-vacuous decision; its predecessor is a recorded triple failure | K/S |
| F27 | vocabulary-free IN/OUT + PB optimisation | encoding | 14/14 exact optima with no vocabulary; PB optimisation ≫ PB decision ladder | K★ |
| F28 | CF exact synthesis over a proved universe | CP | no acyclicity needed; the 1,648-mask universe is derived, not assumed | K★U |
| F29 | tier-1 CF-layer reoptimization | CP | all five 88s' CF layer already optimal over all 2³² — *an 87 cannot come from building better* | K★ |
| F30 | symmetry-quotient SAT | SAT | written, never run; no results on disk | U |
| F31 | CryptoMiniSat / native XOR | SAT | 6 XORs recovered, 1.1–4.3× slower than kissat | D |
| G1 | `slp_opt.py` exact oracle | exact | exact minimum SLP for any small instance; self-test 2,406/2,406 | K★ |
| G2 | exact canonical-set DFS (`qsearch`) | exact | sets not sequences; 2.2 s where the generic oracle needed 1,200 s | K★ |
| G3 | dim-10 quad ladder (sharded) | exact | `12 ≤ cost ≤ 13`, both ends machine-checked; open level priced at 38 CPU-h | K |
| G4 | parallel DFS over derivation DAGs | exact | beats SAT where SAT times out; B=17 UNSAT, still climbing at close | K★ |
| G5 | canonical DFS set enumeration | enumeration | counts *sets*; the record's own block set found in 82/82 | K |
| G6 | program census (all optima) | enumeration | exactly TWO optimal committed sets, and two lanes found one each | K★ |
| G7 | minE exhaustion (orderly generation) | exact | 80,092,627,410 nodes pruning-free; two unpruned trees node-identical | K |
| G8 | greedy-schedule lemma enumeration | exact | 0.39 s where three lanes of SAT burned 5 h and produced nothing | K★ |
| G9 | exhaustive currency-vs-depth BFS | enumeration | `None` means provably impossible; depth 1 infeasible at every cell | K |
| G10 | free-gate exact re-add | exact | dim-32 → "find ≤5 extra masks"; 41/41 exact, always 88 | K★ |
| G11 | forcedness enumeration (`forced.c`) | enumeration | only 22 % of true optima are unique — five distinct 88s discriminate nothing | K★ |
| G12 | quotient tower (mod `v^k`) | exact | `L2 ≤ 26`, `L3 ≤ 51`; the socle rung is the expensive one | K |
| G13 | exhaustive wiring enumeration | census | four of five record 88s have a UNIQUE valid wiring | K★ |
| G14 | heavy-corner exhaustive library | projection | all 1,857 states can finish; a heavy-minimising constructor walks toward the 97 | K |
| G15 | cross-family subset pricing | exact | `cost = cost_cf` on 54/54; the question is empty below 4 targets | K/D |
| G16 | search-free gap hunt (planted screen) | screen | 0 of 750 directed plants show a gap; one-sided by construction | K |
| G17 | cancellation-free MILP | exact | 90/90 agreement; 0 instances where cancellation strictly helps | K |
| G18 | output-subset exact pricing | exact | `U(1) = 152`, `U(2) = 114`; 127/127 round-trips | K★ |
| G19 | Venn isomorphism class reduction | reduction | 496 pairs → 13 classes; 410 runs → 8 | K★ |
| H1 | ring / ladder frame | frame | the 32-dim problem as 8 coupled 8-dim sectors in `F256[v]/(v⁴)` | K★ |
| H2 | exact sector oracle (σ tables) | pricing | 5,623 instances, 0 timeouts; σ(0,0)=12 exact | K★ |
| H3 | M1 chain DP | pricing | class optimum exactly 91, compiled to a VALID 91; records beat it by 3 | K★ |
| H4 | V1.5 exotic-currency DP | pricing | σ=6 exists but is wash-priced; class optimum still 91 | K |
| H5 | shape-law mining (`pred7`) | data mining | closed-form 3-rule σ=7 predicate, 0 errors on 3,124 entries | K★ |
| H6 | junction capacity sweep | probe | capacity exactly 1, proven over all 222 σ=7 classes | K |
| H7 | free-junction relaxation bound | planning | relax to decide whether an expensive sweep is worth running | K U |
| H8 | transposed DP / split-q / sigma-aug / lazy loop | pricing | four escalating twists, all closed; the aug trick is general | D |
| H9 | v2 region pricing | pricing | all 14 known 88s price at exactly 88 with zero residue; ~50 exact decisions all tight | K★ |
| H10 | joint-block probe (folded blocks) | pricing | 18 folded probes, 18 tight; detects gates lost at a seam | K |
| H11 | singleton committed-value exhaustion | sweep | 240/240 individually useless; blind to jointly-enabling sets | S |
| H12 | full-span closure solve | monolithic | failed three times in three lanes; ~5 h wasted | D |
| H13 | ambient relaxation single solve | relaxation | one decision over every set of every size; supersedes singleton sweeps | K★ |
| H14 | minimal-set extraction + monotone sweep | case split | 740 minimal sets, 720 exhaustive UNSATs, 11.85 core-h; the door is SHUT | K★ |
| H15 | theory-first generator | generator | 116@3, 91@5, 92@4, 94@5 emitted with no record read at run time | K/S |
| H16 | module sweep (capped σ) | table | 1,383 classes, 3,022 s, 0 timeouts; two independent tables agree cell-by-cell | K★ |
| H17 | ladder chain DP (price spectrum) | DP | keeps every achievable price, not the argmin; 91…107 | K |
| H18 | depthscan | search | both 91-priced configs schedule to depth 5; an all-σ-7 91@4 is UNDECIDED | S |
| H19 | free-supply derivation + vacuity guard | derivation | one solve bounds `2^{|S|}` point probes; 4 h timeout → 170 s | K★ |
| H20 | merged-derive (boundary deletion) | derivation | cannot be mis-specified; exact 9, and it picked the hand-configured value | K★ |
| H21 | rank-curve measurement | sweep | rank 0 and rank 1 tie; caught a prescribed law being wrong | K |
| H22 | replay bound / conservation | lower bound | a proven tight floor for the price of one solve | K★ |
| H23 | defect-calculus rule (RULE F4) | derivation | names, from the reduction polynomial, which interface must not be filled | K★ |
| H24 | stratified attribution | diagnosis | localises a 3-gate model gap to one interface; corrected a referee | K★ |
| H25 | stepping-stone non-interchangeability | falsification | "pick any member of the derived family" REFUTED; the family solve is not | K★ |
| H26 | unified generator | generator | emits a verified circuit at a requested (count, depth); 9/9 regression | K★ |
| H27 | law derivation (`laws.py`) | derivation | the hand-written rule is a *consequence* of one predicate; 10/10 agreement | K★ |
| H28 | reachability map sweep | measurement | 137 cells; INFEASIBLE vs UNDECIDED separated honestly | K |
| H29 | block-merge relaxation | relaxation | 19 boundaries dissolved, 19 times the split total; 7 at once, still 88 | K★ |
| H30 | uncapped-ladder deep-level decision | SAT | buy one decision: k=12 UNSAT in 19,458 s forces the exact value | K |
| H31 | charged-group bound (all-menu theorem) | bound | `price ≥ 87` over a 1.41e26-element space from ten solves; 9/10 tight | K★ |
| H32 | cell sweep | measurement | every one of 20 known cells prices ≥ 88; the break-even table | K★ |
| H33 | menu-space formalisation + ρ theorem | enumeration | turns an unflagged parameter into a finite object with a symmetry | K |
| H34 | derive-menu-from-witness | derivation | reads a **record-free** menu; written, tested, never wired in | K★U |
| H35 | merged-group probe | SAT | k=6..10 UNSAT, `bound ≥ 11`; k=11 stopped by the operator, not refuted | K U |
| H36 | block-boundary halo widening | mutation | 12 mutations, all price 88; a halo widens what a block MAY use, not what it minimises | D |
| H37 | block-order permutation sweep | mutation | 75/75 one md5; the supply graph is saturated | D |
| H38 | commitment-grammar knob sweep | mutation | 65 runs, nothing ≤ 87; five pre-registered predictions refuted | D |
| H39 | menu-derivability diff | provenance | a proof: no rule over derived line attributes can emit the shipped menu | K★ |
| H40 | menu neighbourhood + trade-off sweep | cost curve | cross-term exactly −1.00 per currency gate; 88 is a five-wide flat plateau | K |
| H41 | self-controlling block reoptimisation | exact | ask at `\|B\|` so the control is the answer; exposed three vacuous negatives | K★ |
| H42 | population-scale block reoptimisation | exact | 586 blocks decided, 0 hits; nowhere near saturated (586 of 78,281) | K U |
| H43 | buy-one-save-two | exact | 4,926 instances, complete and empty | K/D |
| H44 | topologically-convex block closure | repair | fixes a spec bug; 10 uncovered → 0; then 14/14 with the control firing | K★ |
| H45 | sector tightness theorem | exact | 48/48 UNSAT — an 87 requires renegotiating interfaces, not programs | K |
| H46 | sector block reoptimisation | exact | 3 of 23 negatives vacuous; closed and superseded downstream | S |
| H47 | hint-suppression resolve | verification | 57 never-tested gate levels proved UNSAT; floor 70 → 88 in 3.9 core-h | K★ |
| H48 | optimist/pessimist DP + floor sweep | bound | the shortcut is dead; class optimum ∈ [58, 91], not "= 91" | K/D |
| H49 | targeted cell pricing | pricing | five cells lifted, bound moves 58 → 58; ~2,900 solver-s bought zero gates | D |
| H50 | interface-level curve | sweep | price depends on the interface cap alone; depth is a property of the CELL | K★U |
| H51 | regression suite (thrice-verified) | control | fresh subprocess ×2 + an independent oracle run; rebuilt from the ledger | K |
| I1 | depth-3 structure theorem + complete model | bound | the only finite, completely enumerable search space in the project | K |
| I2 | certified LP dual bound (`N_depth3 ≥ 80`) | bound | exact rational dual, 23,450 duals, three mandatory controls PASS | K★ |
| I3 | target-subset exact MILP lifting | bound | 32 → 52 → 59 → 63 in 17 minutes, then the log stops with no note | K U |
| I4 | edge-floor relaxation + ladder | bound | 496 variables instead of 29,180; ceiling 85 | K |
| I5 | column-zeroing bound (Theorem A) | bound | `L ≥ 51`; 51 is the exact optimum of the technique, exhaustively proved | K★ |
| I6 | minE forced-extras (Theorem B) | bound | `L ≥ 54`; the only bound lane where more compute buys more bound | K★ |
| I7 | adaptive gate elimination (Theorem N) | bound | `L(M) ≥ 56` unconditional and refereed — the project's hardest currency | K★ |
| I8 | keep-set layer enumeration | bound | the `\|K\|=14` layer CLOSED at 56; explains exactly why the family stops | K★ |
| I9 | quotient counting lemma | bound | floor transfer by projection; `R01 ≥ 14` at ~1/10 the compute | K★ |
| I10 | quotient exact form (Route 2) | bound | strictly stronger than I9 — worth 21 of 22 against a transferred 14 | K★U |
| I11 | lemma-fortified CNF (tight mode) | encoding | sound but only ~1.2× faster; the value is the arithmetic, not the solver | K |
| I12 | laminar price certificate + LP + cap | bound | `L_cf ≥ 92`; the **only** family above 88; `B* = 91.409884` is the ceiling | K★/D |
| I13 | two-price λ lift | bound | `U ≥ 2` at n=87 and 88; `U ≥ 3` provably unreachable by this instrument | K |
| I14 | cancellation weight budget (P1) | theorem | makes `L_cf ≥ 92` a bound on `L(M)` at all; refereed | K |
| I15 | residual hierarchy certificate (P2) | certificate | proves `n ≥ 88` for two records in exact integers, solver-free | K★ |
| I16 | LP dual-gap recovery | negative | proven gap ≥ 5 ⇒ this certificate family caps at 83; stopped a pod-scale campaign | K★ |
| I17 | integral residual bound Φ | bound | calibration test 2 FAILED and the failure is a theorem | D/K |
| I18 | U1 construction | retirement | the bound is an equality with `L(M)`; improving it is the original problem | K★ |
| I19 | U2 collapse witness | refutation | a negative that is an explicit positive object; 48 < 88, no solver | K★ |
| I20 | counting-LP method ceiling (uniformity) | meta-bound | any endpoint-fixed cut functional gives ≤ 88; measured ratio 0.43–0.53 | K★ |
| I21 | cut-trajectory economy | conservation | `V` returns to 184 always; the efficiency premise inverts at fixed depth | K |
| I22 | heavy-corner rank floors | bound | ≥27 gates with nonzero heavy part, 204/204; explicitly non-compounding | K |
| I23 | cap-table analysis | survey | every bound family with its ceiling; exactly one is above 88 | K★ |
| I24 | obstruction hunt | theory | six candidate obstruction classes, each killed or scoped with a machine check | K★ |
| I25 | class-rank localization + edge counting | bound | both provably capped below 56; edge counting refuted by the records | D |
| I26 | `C_c` fanout-1 conjecture + census | conjecture | measure the parameter on real optima first; z largest exactly at the frontier | S/K |
| I27 | candidate-lemma falsification | refutation | four lemmas dead on arrival in seconds; each failure names the next candidate | K★ |
| I28 | adversarial re-wiring census | falsification | 3,254 circuits × 16 wirings in 132.5 s; refuted a surviving lemma | K★ |
| I29 | Y-ledger impossibility | closure | no such constant exists; the hypothesis is equivalent to its own conclusion | D |
| I30 | anatomy theorem (assume-87) | theorem | the first **gate-count-asymmetric** fact: 475/475 at 87, false at 88 | K★ |
| I31 | spec-87 joint satisfiability | consistency | the whole proven hard spec floors at 54, not 88 — slack 33 gates | K★ |
| I32 | Boyar–Peralta drop profile | bound | `max drop ≤ 6` is FALSE; 27 gates at drop 7/8/9 | S/K |
| I33 | transposition principle identity | theorem | `gates(T) = a` identically — the transposed circuit can never be cheaper | D★ |
| J1 | min-depth schedule (level-BFS / ASAP) | scheduling | forced depth as a theorem; max rescheduling gain across 38,711 sets is 1 level | K★ |
| J2 | level-BFS depth diagnosis | analysis | the depth is burnt inside one block's program, not in the assembly order | K |
| J3 | free-move orbit closure (+ tripwires) | geometry | thirteen pairwise-distinct closed orbits, 378,189 states, zero sub-88 | K★ |
| J4 | `D_fine` metric + farthest-point extraction | metric | certified lower bounds on free-move distance; 90.1 % of 88s are far from all knowns | K★ |
| J5 | gauge canonicalisation + inflation check | hygiene | ~75× inflation at the record; "N distinct states" is a rotation count | K★ |
| J6 | exact `Aut` + equivariance proof | symmetry | `\|Aut\| = 4` in 0.1 s; a free 4× on every exhaustive sweep | K★ |
| J7 | transpose duality + transposed frame | identity | `L(M) = L(Mᵀ)`; doubles the neighbourhood supply; trim first, always | K |
| J8 | mask-Jaccard family test | distinctness | calibrated against two independently published circuits (0.553) | S/K |
| J9 | novelty ruler (neutral baseline) | measurement | 44.1 % of harvest masks are made by no neutral construction | K★ |
| J10 | population spread measurement | census | 78,281 states, median distance 86, from a union of 916 masks | K |
| J11 | corpus-wide degeneracy census | census | `\|odd(m)\| ∈ {0,1,2}, never 3` — 0 in ~184 M mask slots | K★ |
| J12 | fusion-surplus / plane census | census | "the plateau is one fusion pattern" refuted; 0 sets reach 5 planes | K |
| J13 | plane-locality measurement | analysis | 12,946 of 2³² masks; a ~330,000× reduction, apparently free at the frontier | K U |
| J14 | feature-pinning survival floor | pricing | leaving the corpus vocabulary costs **≤ 1 gate**, not "expensive"; never written up | K★U |
| J15 | order-of-sharing cone analysis | analysis | a constant tail of 2–3 gates serves five orbits, always weight-2 on bit 7 | K |
| J16 | glue census (line-set confinement) | analysis | 0 value-glue in 1,232 record-88 gates; refuted the charter's premise | K |
| J17 | economy census | analysis | the glue law is non-discriminating and false under operand accounting | K |
| J18 | socle fibration | analysis | `\|C\| = l3 + s3` exactly; the tradeoff reading is an identity | K |
| J19 | carrier-difference census (C-D frame) | representation | `M = I + LΔ + Δ³` verified; a population instrument that kills theories in a minute | K/D |
| J20 | mechanism decode + library | vocabulary | 15 entries covering 21.1 % of the plateau's vocabulary; the composition thesis is dead | K |
| J21 | population census by block decomposition | census | 54,889 sets, 100 % in class, only two blocks ever vary | K★ |
| J22 | conditional rigidity measurement | census | conditioning narrows but does not close | S/K |
| J23 | forced-fanout rewiring | measurement | separates mask-set properties from wiring artefacts | K |
| J24 | transvection sibling matrix | accounting | `L(M·Q⁻¹) = L(M) − 3` exactly for two explicit matrices | K |
| J25 | provably-optimal census | measurement | 527 provably optimal mask sets — evidence about optima without finding optima | K★ |
| J26 | basin atlas + invariant ledger | de-biasing | three basins not five; the universal core of all fourteen 88s is TWO gates | K★ |
| J27 | monster anatomy | lore correction | mask weight is a measurement artifact of the line the element sits on | K |
| J28 | corrected ruler (shape weight) | heuristic | orders the frontier where popcount anti-orders it; neither points where 88s live | K U |
| J29 | E3 triple classification / backbone recovery | analysis | the three unnamed backbone masks identified; E3 exists, is buildable, costs +1 | K |
| J30 | enabler / midpoint theory | theory | explains what an "enabling gate" is; its search directive was never executed | K U |
| J31 | backbone obligation calculus + `shot87` | analysis | obligations are nearly in bijection with gates — the structural reason 87 is hard | K★U |
| J32 | obligation calculus, witness-free cost | accounting | the witness-dependent version is RETRACTED; the ρ version holds 204/204 | K |
| J33 | walls-as-a-dataset | meta-analysis | effective n ≈ 13, not 1,076; a cut is one mask killing two gates | K★ |
| J34 | overlap parameterisation (V1) | theorem | `cover(O) ≥ 3` in ZERO of 242,974 circuits; the vocabulary audit that voided a main line | K★ |
| J35 | heavy-corner × plan join | analysis | the cancellation layer *becomes* the heavy layer as circuits improve | K★ |
| J36 | vocabulary saturation | measurement | 4,120 pairs saturated; the corpus was never the problem | K |
| J37 | candidate-class naming rate | pre-measurement | classes wide enough to contain a good circuit are too large to build | K★ |
| J38 | structure algebra (ρ²) | analysis | full ρ-symmetry costs +19; cross-byte sharing is the whole game | K |
| J39 | legibility profiling | analysis | `k_strict = k*` on 39/39 — optima are not senseless, they are patient | K★ |
| J40 | exact move census | pre-measurement | the complete remove-1 move set of the record is **12 moves** | K★ |
| J41 | widening theorem + byproduct impossibility | theorem | prove first, then run SAT as a falsification test; 48/48 confirm | K |
| K1 | B = 56 tripwire | tripwire | free, always-on, provably sound 87 detector; 0 alarms in 17,283 circuits | K★ |
| K2 | Lemma R / T2 corpus tripwire | tripwire | 66 hits on non-optimal circuits, five compressed and oracled | K★ |
| K3 | streaming k=2 shell detector | tripwire | 197,072 exhaustive shells decided live alongside the search | K |
| K4 | free-gate scan | tripwire | zero duplicated masks and zero dead gates across the whole corpus | K |
| K5 | self-test / fake-87 harness | tripwire | 131 checks, 0 failed; found that cross-pollination was silently dead | K★ |
| L1 | positive-control methodology | control | no negative without a one-gate-above control; LR measured at 1.00 | K★ |
| L2 | certificate control audit (repricing) | meta | a 97 is indistinguishable from an 88 by the k≤3 instrument | K★ |
| L3 | shape-matched random control | control | 0/400 at every shape with n ≤ 3 — those nulls carry no information | K★ |
| L4 | partial-budget worthlessness calibration | diagnostics | 0.82 % of a level consumed without reaching a guaranteed solution | K★ |
| L5 | brute-force oracle validation + vacuity gate | control | caught a real false-negative bug; a batch with no negatives is discarded | K★ |
| L6 | five-control stack | discipline | what a defensible exact negative looks like; copy wholesale | K★ |
| L7 | four-control suite (C0/C1a/C1b/C2/C3) | discipline | C1a is solver-free and catches encoding incompleteness | K★ |
| L8 | cap-off control | control | 10/10 two-implementation agreement on real blocks | K★ |
| L9 | greedy upper-bound control | control | a liveness check attached to every single solve invocation | K★ |
| L10 | derive-family vacuity audit | audit | three of four "derived" constants were outside the searched family | K★ |
| L11 | slot-order sensitivity test | audit | 123/128 arbitrary orderings manufacture UNSAT; 128/128 legitimate ones do not | K★ |
| L12 | plan-space sizing | pre-measurement | kills or unblocks a formulation in seconds, no solver | K★ |
| L13 | cost-curve pricing | planning | 2,400–117,000 pod-years — no budget certifies by climbing | K★ |
| L14 | constraint-ratio law | calibration | ~70× spread at fixed n; the faster windows are the least likely to hide an 87 | K★ |
| L15 | prediction scoring + hash-chained pre-registration | discipline | cannot be back-dated; a 7-miss lane out-produced a 15-hit lane | K★ |
| L16 | provenance audit (DERIVED/MEASURED/ASSUMED) | discipline | over-constraining is the circular failure mode; quarantine what is calibrated | K★ |
| L17 | adversarial cross-desk referee | verification | rebuild from source sharing no code; no PROVED claim refuted, many narrowed | K★ |
| L18 | meta-review (six red-team agents) | audit | six live bugs on the ≤87 path, none of which had yet produced a false claim | K★ |
| L19 | fact-vs-mutable code audit | audit | 244 rows; the shipped run had proved no per-block minimum at all | K★ |
| L20 | audit from banked artifacts + forgery sandbox | audit | passing is consistency, not tamper-evidence — and it proved it | K★ |
| L21 | lineage-independence control | statistics | effective n ≈ 13 against a raw 1,076; half the descriptor signal is confound | K★ |
| L22 | identity-first autopsy | repricing | the 536 dissolved: 268 sites doubled, and the headline was an identity | K★ |
| L23 | success-branch rehearsal | control | rehearse the SAT branch before you need it; emitted a verified 88@7 | K★ |
| L24 | instrument repair with regression separation | soundness | a suite that pins behaviour red-flags its own corrections | K★ |
| L25 | radius-hypothesis significance test | design | matched budgets, achieved-not-requested arms, interleaved controls 14/14 | K★ |
| L26 | positive-only probe | discipline | a miss that carries no information, logged as such | K★ |
| L27 | plane-cage discriminator | control | the ≥4-plane predicate is **free** at the plateau; the sham quota costs +0.87 | K★ |
| L28 | high-plane tier probe | measurement | 7,755 ≥5-plane masks offered, used 0 times; the frontier closed honestly | K |
| L29 | atlas adversarial-audit family (4 instruments) | audit | frame rebuild / instance rebuild / trust graph / alternative reading | K★ |
| L30 | reproduce-harness (frozen single-move demos) | pedagogy | three one-move demos; reproduced the record 88@d7 gate-for-gate 18 days later | K |
| M1 | cluster-currency hand reasoning | hand proof | 106 → 97 → 91 → 90 → 88, gate-for-gate the known record, no solver | K★ |
| M2 | pure-reason theorem lanes | hand proof | graded claims; `H87` survives every currently-live conjecture | K★ |
| M3 | hand-reduction algebra (parity-hub law) | theory | the 88/89 separator is one materialised plane parity; P7 is never bought | K★U |
| M4 | counterexample-family construction | refutation | kills a conjecture's class-level form with a hand-provable family | K★ |
| N1 | swappable-parts catalogue | planning | 25 axes with costs and tractability guards; the phase-2 planning document | K★ |
| N2 | cross-lane consolidation / discrepancy audit | audit | 11 live contradictions found, including a decisive result written up nowhere | K★ |
| N3 | dated corrections ledger | documentation | never rewrite a superseded claim; separate scope from correction | K |
| N4 | naive-reader certification | documentation | a pass/fail criterion for the public writeup; reader reimplements from prose | K★ |
| N5 | prior-art import + provenance audit | literature | 12 published circuits imported and oracle-VALID; four literature corrections | K |
| N6 | records-hygiene audit | bookkeeping | the published depth-4 point is understated by a gate, three distinct lineages | K★ |

---

# Appendix A — thin entries: **ALL NINE NOW COMPLETED** (2026-08-29)

These nine appeared in the slice reports with too little to fill the schema and
were listed here rather than dropped. An adversarial audit
(`wrapup/day2/CATALOG_AUDIT.md` §3) went to the primary sources for each and
**completed all nine — none is a non-method.** Every one had more evidence than
this appendix credited it with; for two of them what the evidence shows is that
the headline is unreproducible (H45) or false (M3), which is itself the finding.
The full entries follow, in the catalog's own schema. The body entries they
complete (`F30`, `J30`, `M3`, `I25`, `I23`, `H45`, `A10`/B4, `N3`, `B14`) are
unchanged in place; the total remains **309**.

---

### A·1 · **F30** symmetry-quotient SAT — *instrument built, never run*
- **What it does:** Searches for a circuit that is **identical under 8-bit rotation**, solving only
  for one rotation-class representative. Instead of 88 individual gates it solves for `k` "orbit
  gates", each one signal XOR a rotated copy of another; materialising each orbit costs exactly 4
  real XOR gates, so reachable gate counts are **multiples of 4**. It hands CryptoMiniSat a CNF with
  one-hot operand/rotation selectors and native XOR clauses per bit, and on success expands the
  quotient solution back into a full 32-input asymmetric circuit.
- **Twist:** its nearest sibling is the same lane's *greedy* symmetric mode, which builds rot8-closed
  circuits and pays 12–13 gates for the privilege. F30 is the only instrument in the repo that asks
  the symmetric question **exhaustively** rather than greedily, collapsing the space 4× by never
  representing the other three rotations at all.
- **Measured:** **none — it was never executed.** The lane's own audit is explicit
  (`fleet10/RESULT.md:557`): *"UNRECOVERABLE — whether `satquot.py` was ever run. No output, no log,
  no ledger row."* The numbers that *price* it: matched A/B `test_asym.json` **95 @ 8** vs
  `test_sym.json` **108 @ 4**; best symmetric circuit in the lane `islandS.json` **106 @ 5**;
  **"measured penalty for forcing ρ-symmetry in this search: 12–13 gates"** (`RESULT.md:142-152`);
  and fleet9's independent **"No ρ-fixed 88 exists in 54,889 circuits"** (`laneENUM/RESULT.md:347`).
  Both available signals say it will fail. **88 = 4 × 22, so `k = 22` is exactly the question.**
- **Cost:** not recorded. *Derived by the audit, not primary:* the k=22 CNF is **40,403 vars /
  204,377 clauses / 704 XOR rows** (k=21: 36,834/186,166; k=23: 44,137/223,568) — a small instance by
  this project's standards, hours not days. ⚠ **`pycryptosat` is not installed on this box**, so the
  script cannot run as written without installing the solver.
- **Code:** `fleet10/cleanroom/work/satquot.py` (156 lines); reads `fleet10/cleanroom/spec/targets.json`.
- **Logs:** **none.** Its only output file (`symsol_k.json`, `satquot.py:154`) does not exist anywhere;
  60+ `.log` files under `fleet10/cleanroom/work/` and none is this.
- **Generality:** **MIXED, leaning MC-HARDCODED.** No `0x11B`, no `[2,3,1,1]`, no `xtime` — targets are
  read from a spec file, which is the generic part. Everything structural is MixColumns-shaped:
  `:25-26` hardcodes that the 32 targets fall into exactly **8** rot8-orbits with reps in positions
  0–7; `:28` fixes the 32-bit word; `:39,53` hardwire the symmetry group as **Z/4 acting by 8-bit
  rotation**, i.e. the AES 4-byte column; `:82-83` the 8×4 byte layout. Port cost: a new orbit
  decomposition of the new target set under the new automorphism group — i.e. J6 first.
- **Phase-2:** **run it once, then catalogue it properly.** `fleet10/RESULT.md:600` calls it *"the one
  cheap open item"* and fleet9 independently asked for exactly this search
  (`fleet9/laneENUM/RESULT.md:542-543`). **An instrument and a written request for it sat in the same
  repository and were never joined up** — that is the transferable lesson, independent of the answer.

### A·2 · **J30** enabler / midpoint theory — *Appendix A understated this badly*
- **What it does:** Explains why some gates in a record circuit look worthless to every scoring
  function yet are necessary. A three-term sum must be computed as two XORs, so one of three possible
  intermediate values ("midpoints") must be bought; two of the three lie off every structural line the
  scoring functions can see, so they score **zero** until the third term arrives and collapses them
  onto a useful value. The theory names these off-line midpoints **enablers**, classifies them by how
  many corrections they need ("order"), and derives five necessary conditions any profitable enabler
  must satisfy — turning "the score lies" into a finite, enumerable move vocabulary.
- **Twist:** its nearest sibling is the previous campaign's *ternary repair planes*, an empirical
  observation that certain mask triples XOR to zero. J30 **derives** that: the three midpoints of any
  3-term sum always XOR to zero, so a repair plane **is** a midpoint triple, and the "3 routings per
  tap constraint, every choice works" freedom is just the choice of bracketing. It converts an
  unexplained coincidence into an identity, and then prices it.
- **Measured** (`atlas/thinktank/enabling_gates.md`): **cluster law — every off-line gate in all 8
  frontier circuits (88@5, 88@5fs, 88@6, 88@7, 88@8, 89@5, 92@4, 97@3), 74 off-line gates total, has
  support inside a tap triple; zero violations** (`:144-146`). The 36 defect/bypass masks of the
  +1-cost 89 bridges decode as **24 in tap clusters, 7 on-line S2, 5 genuinely off-line** (`:162-166`).
  Of the **30** off-line gates in the five 88s, **only 8 are order-1; 22 are deeper** (`:188-189`).
  E1 enumeration: cluster {0,1,7} → 3570/4095 off-line values, **426** E1, **110** y-orbits;
  clusters {2,3,7} and {3,4,7} → 3780/4095, 300, 78 each (`:213-215`); **18** canonical y-orbit
  enabler classes (`:221`). Disciplined class optimum **91** exact vs records at **88 = 91 − 3**, so an
  in-architecture 87 needs midpoint-sharing profit **≥ 4** (`:251-253`). The **243 = 3⁵** optimal
  modules are the 3⁵ bracketing choices of five slots (`:135-138`).
- **The follow-up that ran its own §8 test** (`atlas/thinktank/phase2_e3.md`, same day): of the **1,291**
  pairwise-invisible triples, **0** use a column outside the tap-triple union, **869** are not contained
  in any single tap triple, **859** also carry an off-line exchange value outside every tap triple.
  The cluster law survives **13 new off-line values, 13/13** (`:363`). And the correction, in its own
  words (`:368-371`): *"Correct §8 of `enabling_gates.md`: the discriminating test has been run and
  **does not discriminate in the hoped-for direction**. The V2 localization does not extend to order-3
  moves; the tap-cluster collapse is not established."* Recorded at `atlas/NOTEBOOK.md:451-463,515`.
- **Cost:** not recorded (one think-tank session, 2026-08-17). The follow-up is re-runnable in one
  command and reads only files on disk (`phase2_e3.md:390-393`).
- **Code:** ⚠ the theory's **own** six verification scripts are gone — `decode_specimens.py`,
  `hoptheory.py`, `glue_census.py`, `cluster_law.py`, `defect36.py` exist nowhere in the repo, and the
  `planes.py` that does exist is an unrelated tool. **The follow-up survives:**
  `atlas/thinktank/phase2_e3.py` (20,719 B, self-contained, imports only `atlas/ring.py` +
  `atlas/economy.py`), plus `phase2_gen_rest.py:53-55` and `phase2_fin.py:311`.
- **Logs:** `atlas/thinktank/phase2_e3_candidates.txt` (73,372 B, **869 lines**, one per candidate
  triple with span, spread and clean glue exchange values) — the primary data product. None for
  `enabling_gates.md` itself.
- **Generality:** **MC-HARDCODED.** Every quantity lives in a coordinate system built for this problem
  — the ring `T = F₂[v]/(v⁴)`, the eight sectors, the tap identity `2d_k = d_{k−1} + d_7` verified as
  `fmul(0x05,2) = 0x0a = 0x58^0x52` (`:49-50`), concrete masks throughout. The *abstract* midpoint law
  ("the three midpoints of a 3-term sum XOR to zero") is trivially circuit-generic; nothing else is.
- **Phase-2:** **keeper as a way of seeing, with three honest caveats.** (a) Its own verification
  scripts are lost, so §1–§7 are not re-derivable *in place* — only in principle from
  `atlas/ring.py`/`economy.py` plus the evidence JSONs. (b) Its §5 pricing argument is explicitly
  **not** a machine-checked theorem (`:262-264`, "a local exchange argument"). (c) **Its §8 hope was
  falsified** — the E3 class is populated, not empty. The transferable part is the mechanism: *a gate
  that scores zero under every structural predicate may be the forced midpoint of a multi-leg sum.*

### A·3 · **M3** hand-reduction algebra / the parity-hub law — *FOUND-NOTHING + REFUTED PREDICTION*
- **What it does:** Twenty-one no-tool language-model agents were handed inlined gate lists of the
  record circuits and asked to find a one-gate improvement by pure reasoning. **None did.** What they
  produced instead is an algebraic account of *why* the circuits resist: a difference calculus over the
  four output bytes, and the **parity-hub law** — the two-output differences all contain a doubled full
  column parity, so materialising one column-parity mask as a shared hub discharges ~3 target
  obligations across two byte-orbits for one gate.
- **Twist:** its nearest sibling is any automated rigidity prober, which reports *that* a circuit is
  locally optimal. M3 reports **which algebraic identity makes it so**, and — uniquely — names an
  *unbought* device: `P7 = 0x80808080`, claimed to be the only mask with quadruple duty, appearing in
  all four carry-orbit expressions yet absent from every circuit examined. **That named prediction is
  what makes it falsifiable, and it is what got falsified.**
- **The law** (`campaign_87/wave5_2026-08-04/burn/handreduce/WAVE2_INSIGHTS.md:70`): with `e=a^c`,
  `f=b^d`, `P=a^b^c^d` and plane parities `P_i`, within each bit-orbit `j`,
  `outA_j^outC_j = (2P)_j^e_j` and `outB_j^outD_j = (2P)_j^f_j`; `(2P)_j = P_{j−1}` for non-carry
  `j ∈ {2,5,6,7}`, but `(2P)_0 = P7`, `(2P)_1 = P0^P7`, `(2P)_3 = P2^P7`, `(2P)_4 = P3^P7` at the carry
  positions. **Status: a hand-verified identity wrapped in a heuristic economic reading — neither
  theorem nor machine-checked.** Its own header says so (`:3`): *"nothing here is oracle-verified
  circuit material — these are analyses"*, self-rated *"high on the structural pattern; **medium** on
  the conjecture that the P7-hub carry-block re-synthesis yields 87."*
- **Measured:** wave 1 **9 agents, 0 candidates** (5 of 9 blew the output-token ceiling mid-derivation);
  wave 2 **12 agents, 0 candidates, 12/12 completed** (48,728 B). Hub census over the six records:
  `A,B={P4,P6}, C,E={P1}, D,F={P2}`; 89/90/92/96/97 carry **none**; every hub costs 1 gate and serves
  ~3 targets in 2 orbits (`:70`). Ledger: every circuit = 32 finishers + supports; every 88 = **32+56**;
  an 87 is exactly **55** supports (`:9`).
- **REFUTED — twice, independently, and the campaign pre-registered its own falsifier**
  (`assume87/operations.md:402-407`). (1) **By exhibition**, wave 6
  (`campaign_87/wave6_2026-08-11/ATTEMPTS_SINCE_PUSH.md:686-700`, *"PREMISE REFUTED BY EXHIBITION"*):
  over 93,852 distinct harvested 88-states, **12,039 carry Σ5 and 14,088 carry Σ7**; two oracle-VALID
  88s were produced straight from harvest (`SIGMA5_88_from_harvest.json` 88@7,
  `SIGMA7_88_from_harvest.json` 88@8) — *"No solver was needed."* (2) **By census**, 2026-08-29, over
  **1,925,065** accepted 88-gate mask sets from six banks (804.6 s):
  `hub_count_per_circuit_histogram = {0:7, 1:1909794, 2:9814, 3:4476, 4:960, 5:14}` — **5,450 circuits
  carry ≥3 hubs** and **7 carry zero**, so the strict separator has counterexamples; and
  `hub_j_occurrences` puts **P7 in 1,429,688 of 1,925,065** circuits — **the single most common hub in
  the corpus**, the exact opposite of "the corpus-wide blind spot".
  ✅ **Crucially the conventions agree:** the machine census gives the six records hubs
  `[2], [4,6], [4,6], [1], [2], [1]` — a perfect multiset match to M3's hand census. **M3's arithmetic
  on the six records is right; the extrapolation to the corpus is false.**
- **Cost:** 21 agent-runs across two waves, no tools, no wall-clock recorded. The *falsifications* have
  costs: recensus 804.6 s single-threaded over 1.93 M rows; the wave-6 Σ probes 38.7 s / 60.2 s.
- **Code:** **none for M3 itself** — the two documents contain no code and reference no script.
  Instruments that *test* its claims, all written later by other lanes:
  `wrapup/day2/e_upstream/recensus.py` (hub counting at `:55-56,81,97,186-187`),
  `wrapup/day2/e_upstream/classes.py`.
- **Logs:** for M3, none. For the falsifications: `wrapup/day2/e_upstream/{recensus.json,recensus.log,classes.json}`,
  `campaign_87/global_vocab/vocab_counts.json`, and the two exhibited circuits.
- **Generality:** **MC-HARDCODED, totally.** `a,b,c,d` are the four AES input bytes, `xt` is AES
  `xtime`, and the carry positions `{0,1,3,4}` are exactly the set bits of the reduction polynomial's
  low byte `0x1B`. Nothing here transfers to another circuit family.
- **Phase-2:** **keep as the cleanest example in the repo of a hand-reasoning lane earning its keep by
  being wrong in public** — it made a checkable prediction, the campaign pre-registered a falsifier,
  and machine work broke it. Do **not** carry the parity-hub separator forward as fact. Its proposed
  decisive experiment (P7-extended carry-block re-synthesis over the 16-target carry orbit) **was never
  built**, and the nearest thing that was run found nothing with passing controls (684 RC2 exact-floor
  alphabets, floor 88 on every one; 8/8 seeded descents at 1,800 s, none improving).

### A·4 · **I25** class-rank localization + edge-counting bound — *a ceiling method, not a bound*
- **What it does:** Two attempts to prove a floor by finding a quantity each gate can move by at most 1
  and showing how far it must travel. The first splits every signal's mask into eight algebraic blocks,
  gives each signal a class, and counts the dimension each class must gain. The second counts **wires**:
  every gate has two inputs, so gates ≥ (sum of input fanouts) − (gates nobody consumes). Both are then
  **evaluated on the record circuits they must bound**, and both turn out arithmetically incapable of
  ever reaching 88.
- **Twist:** **it is a self-refutation via the records.** Rather than trying harder, the author reads
  his own bound family's ceiling off circuits that exist. The class-rank cap is proved by algebra; the
  edge-counting cap is proved by the record circuits *themselves* evaluating to 31–33.
- **Measured** (`atlas/thinktank/ideas_proofside.md`): class-rank theorem `:212`, bound `:219`,
  **cap = 32** as 8 target classes × 4 (`:229-239`), singleton classes contribute **zero** because
  inputs `d_k y^j` already span the 4-dim block — *"the whole shared-currency economy is rank-invisible"*
  (`:232-236`); v-filtration refinement sums to **≤ 28**, measures ~19 (`:242-244`). Edge counting
  `L ≥ Σφ_i − |U|`, `|U| ≤ 32` (`:261`), and the 10-circuit table (`:266-277`) — bounds
  **31 / 33 / 33 / 32 / 33 / 32 / 32** on the seven 88s, **35** on 89@5, **38** on 92@4, **45** on 97@3.
  By-products: max input fanout **2–3**, inputs used ~**1.9** times; every 88 has **3–6** inputs of
  fanout exactly 1, refuting "every live input has fanout ≥ 2" (`:286-290`). Own verdict, *"would not
  fund"* (`:415-417`). Re-entered independently into two cap tables
  (`fleet1/laneC_proofside/RESULT.md:675,677`; `experiments/e17_pure/DOSSIER.md:1042,1045`).
- **Cost:** **not recorded** for either family. Cheap by inspection: class-rank is pen-and-paper;
  the edge table is a ~10-circuit fanout tally.
- **Code:** class-rank — **none** (a prose theorem with a two-line proof). Edge-counting — **partial**:
  `atlas/thinktank/proofside_code/price.py` computes per-input `outdeg` (= φ) and the column price,
  with `mc.py` building M. ⚠ **`fanout.py`, named in its own reproduction section
  (`ideas_proofside.md:445`) as a shipped script, does not exist anywhere in the repo** — so the `|U|`
  column, the load-bearing half of the bound, **has no surviving implementation**.
- **Logs:** **none.** `proofside_code/` carries logs for the Theorem-N ladder only.
- **Generality:** **MC-HARDCODED** (the measured half). `mc.py:9-12` `xtime` with `0x11B`; `:28`
  `coef = [2,3,1,1]`; `price.py:22,31,78` `range(32)`. The class-rank *inequality* is generic (charge
  each gate to its class); everything that makes it a number is AES. The edge-counting *inequality* is
  fully generic; `|U| ≤ 32` is the hardcoded target count.
- **Phase-2:** **keeper as a NEGATIVE/ceiling instrument, not as a bound.** ⚠ **The 10-circuit table is
  unreproducible as written** — that must travel with any citation of it. The transferable move is the
  one that killed both families in an afternoon: *evaluate your candidate bound on the circuits it is
  supposed to bound, before funding the proof.*

### A·5 · **I23** cap-table analysis — *the "no Code/Cost/Logs" flag was a category error*
- **What it does:** Instead of trying to prove a better floor, it lists **every** lower-bound technique
  the project has used and asks, for each: what is the largest number this technique could *ever*
  produce, perfected? Each answer is proved algebraically or measured by evaluating the technique on
  circuits known to exist. The result is one table showing essentially every family topping out well
  below 88.
- **Twist:** it converts "we failed to prove 89" into **a proved ceiling per family** — the difference
  between "nobody found it" and "it isn't there". The organizing insight: all techniques are one of
  three shapes (reduction / charge / certificate) and two of the three have *structural* caps — a
  reduction can only see what mutilating a circuit deletes (measured **1.91**/column against a truth of
  **2.83**, so the ~0.9 gap is invisible to every reduction ever written), and a charge cannot exceed
  the target count (**32**). Only certificates survive, and exactly one certificate family has ever
  produced a number above 88.
- **Measured — the table is the artifact.** `fleet1/laneC_proofside/RESULT.md` §3.5, header `:672`,
  rows `:674-682`, **nine families**: Lemma P / projection-visibility `32 + minE_φ` (~40, proved);
  **class-rank 32** (proved, 8 classes × 4); generalised heavy-corner rank ledger **52** (measured max);
  **edge counting 33** (refuted by the records); linear counting / LP **46.2** (measured); Theorem-N
  column-zeroing **56 today, ≤ 73 under `C_0`** (proved); socle tower rung **51** (capped by the
  verified `L3 ≤ 51` witness); backward identity `F = 64+a−c−2d` (**circular**); and
  **cancellation-free `L_cf` ≥ 92** (CANON U6-2, solver-free certificate) — the only row above the
  record. The lane grades it honestly (`:703`): *"cap table (§3.5) | ANALYSIS over cited refereed
  results | each row's citation"*. Taxonomy at `:548-560`; the two shape-caps at `:562-576`.
  **A second, later cap table exists and should be cited alongside:** `experiments/e17_pure/DOSSIER.md`
  §5.8, header `:1036`, **twelve rows** `:1038-1048` — keeps 46.2 / 52 / 33 / (36–40), adds tower rungs
  (51, level 2 capped at 26), `C_c` (73 at c=0, 71 on M's own rung, 67 coarse), quotient composition
  ("no theorem to find"), sector localization ("no such lemma can exist"), and promotes *reductions*
  and *charges as proof shapes* to rows of their own.
- **Two live defects that belong in any citation.** (a) **fleet7 asked for its family to be added and
  it never was**: `fleet7/laneUNCOND/RESULT.md:136` *"It belongs in Lane C's cap table as a closed
  family"*, `:710-711` *"this family's ceiling is `102 − 2.1875·κ`, and it crosses 56 at `κ = 22`"*
  (records have κ ∈ {18,19,21,22,26,27,28}). (b) **The one surviving row has since been given its own
  ceiling of 83**: `DOSSIER.md:1050-1053`, from `experiments/e17_pure/laneCONTRA/RESULT.md:62-66`.
  ⚠ **Neither cap table carries `91.4098776`** — checked directly. Lane C's row still cites the older
  `91.0019782`-era constant `L_cf ≥ 92`; the 91.4098776 lives only in `fleet7/laneUNCOND/RESULT.md`
  (`:21,109,634,1003`). A known inconsistency is already logged against this
  (`STATE_OF_THE_PROBLEM.md:1137-1142`, defect **D11**: three active lanes, three pictures of the same
  `L_cf` bracket).
- **Cost:** not recorded — correctly, since the table is analysis over cited results.
- **Code / Logs:** **none for the table itself**, and that is the right answer for a survey method — its
  artifact *is* the table, at two absolute paths with per-row citations. The lane's `code/` directory
  and `ledger.jsonl` (29 entries, 13 kinds) support the *rows*.
- **Generality:** **MIXED, leaning CIRCUIT-GENERIC.** The three-shapes taxonomy and "charges cannot
  exceed the target count" are generic statements about linear-SLP lower-bound programs. Every *number*
  is MixColumns-specific. **The methodology transfers; the table does not.**
- **Phase-2:** **keeper — one of the strongest entries in this catalog, and the first thing to rebuild
  on a new circuit.** Build the cap table *before* funding any bound work: it is the instrument that
  tells you which proof shapes are arithmetically incapable of reaching your target, and it costs
  nothing but bookkeeping.

### A·6 · **H45** sector tightness theorem — *48 machine checks with zero surviving artifacts*
- **What it does:** The record 88s split into eight sectors, each a sub-program consuming values from
  elsewhere and handing values back. For each of six record circuits and each of its eight sectors, the
  sector is cut out and rebuilt as a standalone exact problem — **imports become inputs, exports become
  targets** — and an exhaustive oracle is asked whether the sector's job can be done with one gate
  fewer. All 48 come back impossible. Conclusion: **no record can be improved by fixing any one sector;
  an 87 must renegotiate the interfaces between sectors, not improve a program inside one.**
- **Twist:** it flips the local-search question. Prior closure sweeps only tried ≤3-gate mask moves;
  this replaces **up to 9 gates at once** and had never been run. It converts "we searched and found
  nothing" into "each piece is provably at its own floor **given its interface**" — which is what
  identifies the *interface economy*, not the programs, as the only remaining place an 87 could live.
- **Measured** (`atlas/thinktank/ideas_two_mechanisms.md`): construction `:141-146`; result `:148`
  **"48/48 UNSAT (machine-proven, `slp_opt.py`, exhaustive). Every sector program of every record is
  exactly minimal for its interface."** 48 = **six frontier records (five 88s + 89@5) × eight sectors**.
  Scope note `:151-153`. Corollary `:155-158`: *"win 3 in supply then add 1 in work" is impossible at
  single-sector scope; any combination must change ≥2 sectors and their shared supply jointly.*
  The `w_k` work counts the queries were built from (`:73-80`): 88@5 `8,7,6,5,7,7,7,6` Σ53 · 88@5fs
  `6,7,7,7,6,7,6,7` Σ53 · 88@6 `8,4,9,6,6,7,6,7` Σ53 · 88@7 `9,6,7,7,7,7,7,6` Σ56 · 88@8
  `9,7,6,5,7,7,7,6` Σ54 · M1 optimum `7,7,7,7,7,7,7,7` Σ56 — ⚠ **89@5's row is absent, so 8 of the 48
  instances have no published `w_k`.** Two σ=6 facts proved from these instances (`:187-190`),
  independently corroborated by the basin atlas (`:264-268`). Restated at `atlas/NOTEBOOK.md:768-769`.
  Reused **as a method** by two later lanes: `fleet1/laneB_regionbounds/RESULT.md:235-238` — *"the
  tightness-theorem pattern ('minimal given imports', 48/48) applied INSIDE the region … the only
  priced-able path to the full certification this lane found"*; same at `fleet2/laneG_generator`.
- **Is it a theorem?** **No — it is 48 machine checks.** The document gives a construction and a solver
  verdict, never a proof. Everything universal about it is a universally-quantified statement over an
  explicitly finite set of 48 exhaustive UNSAT queries. The lane's naming is generous; the entry should
  not repeat it uncritically.
- **Cost:** **not recorded.** No wall time, no node counts, no core-hours for any of the 48. The only
  size datum: the *generous*-variant 88@7 S7 instance had **114 inputs** (`:61`); the tight instances
  are sector-local (`w_k ≈ 4–9`) and much smaller.
- **Code:** ⚠ **the driver is gone.** The oracle survives — `atlas/slp_opt.py` (1,037 lines, dual
  SAT + iterative-deepening DFS, documented soundness proofs for every pruning rule, explicit guarantee
  that a negative is *"EXHAUSTIVELY proven … never heuristic"*), with `atlas/slp_opt_selftest.py`. The
  scripts that **built and ran** the 48 do not: `ideas_two_mechanisms.md:21-23` names
  `tm_dissect.py`, `tm_regions.py`, `tm_straddle.py`, `tm_resolve_gen{,2}.py`, `tm_chaincost.py`,
  `rich_inst*/` and `:16-19` records *"A restart wiped the scratchpad mid-session … **the `tm_*.py`
  scratchpad scripts are gone, their results are recorded here**."* An exhaustive search confirms:
  no `tm_*.py`, no `rich_inst*` anywhere. Sector-classification support **does** survive and is useful:
  `atlas/{sectors,sector_view,ring,anatomy}.py`; the six input circuits are in `evidence/circuits/`.
- **Logs:** **none.** Not one of the 48 instances or verdicts is on disk — no JSONL, no per-instance
  JSON, no solver output. The `48/48` exists only as a sentence in markdown, twice, plus a one-line
  restatement in the notebook.
- **Generality:** **MIXED.** Generic: `slp_opt.py` takes `{dim, inputs, targets, max_gates}` from JSON
  and knows nothing about AES, and **the method — cut a sub-program out, promote imports to inputs and
  exports to targets, ask for one gate fewer — is fully circuit-generic**, as lane B's re-targeting
  proves. Hardcoded: "sector" is AES ring theory (`atlas/ring.py:14 AES = 0x11B`; `atlas/sectors.py:3-7`
  defines sectors as spans fitting an xtime line; `atlas/anatomy.py:47-49,59-60` `0x11B`, `[2,3,1,1]`).
  The "8" in 48 = 6 × 8 is the eight AES sectors.
- **Phase-2:** **port the *recipe*, not the result.** ⚠ **Evidence grade: prose-only / unreproducible.**
  It sits one notch above a non-method purely because the recipe and the oracle are both precise enough
  to rebuild from scratch — and rebuilding is exactly what a new circuit needs anyway.
  ⚠ **Do not confuse with the unrelated 48/48 in `fleet5/laneGLUE`** (dim-12 glue byproducts, theorem
  G4) — that is **J41**. Coincidental count, different experiment.

### A·7 · **B4 descriptors** — the three `beat88/analysis` rows, as **one** entry (folded into A10)
- **What it does:** Three cheap per-circuit numbers that say *which structural basin a circuit came
  from*, needing no reference to any known circuit. (a) **ρ²-defect**: how many of a circuit's chosen
  masks survive a two-byte rotation — one set intersection. (b) **Row-depth profile**: for each of the
  32 output rows, the earliest level at which that row could be built from the circuit's own masks,
  kept in spec row order. (c) **Neutral degeneracy**: delete each mask and exhaustively enumerate every
  single mask that restores all 32 outputs — an exact count of sideways moves at the same size.
- **Twist:** each inverts a standard use. (a) is a *between-basin coordinate*, not a gradient
  (correlation with Jaccard-to-anchors **−0.061**), and it is used to **repel away from** the exhausted
  band — the opposite of the campaign's earlier symmetrize-and-peel use of ρ². (b) carries *direction*,
  not just distance: the maximal-depth rows are that basin's depth walls, so it says *where* a circuit
  is stuck. (c) **reuses the exhaustive-certificate decider positively** — the improving shell is empty
  from 97 down to 88 so it cannot tell a 97 from an 88, but the *neutral* shell measured by the same
  code is monotone in gate count.
- **Measured** (a): found88 n=**3,254**, mean 0.645, sd 0.034, min 0.589, max **0.786**; ils88 n=**872**,
  mean 0.562, min **0.536**, max 0.643 — band **[0.536, 0.786]** over 4,126 states; the two from-scratch
  88s sit at 16/56 = 0.2857, **z = −10.63** (computed, not asserted — `pop2.py:88-97` computes μ and σ
  over the population; the audit reproduced all of this from the raw JSONL). ⚠ n = 3,254 (found88 only)
  is the z-score denominator, despite the "4,126-state range" phrasing.
  (b): within-family Hamming **0–3** (fam4 recomputed `[0,2,2,3,3,2]`), within-basin **8**, remote-89
  cluster **6–8**, cross-family **11–28** (min 11 = 88@7↔89@5, max 28 = SYL89↔88@6). ⚠ **B4's own
  "18–26 across families" is contradicted by the same corpus** — the true cross-family minimum is
  **11**, and the gap is clean but its margin is **3**, not large.
  (c): bands 97 → **68/80/86**, 92 → 55/82, 91 → 32–69, 90 → 26–54, 89 → 14–36, **88 → 12–21**; 0.1 s
  per circuit; tripwire: `improving > 0` at 88 gates **would be** an 87.
  ⚠ **"25 of 29 exactly 16" has no surviving artefact** — a repo-wide grep for out-degree output in
  `*.log/*.txt/*.json/*.jsonl` returns **zero** matches; it exists only as prose. ⚠ The band table's
  corpus counts (3/2/6/6/26/29 = 72) **silently omit the 94-gate row (n=2)** of the 74-circuit seedlist.
- **Cost:** (a) ~50 µs, one set intersection; (b) ~1 ms; (c) 0.1 s, folded version 10–20 ms.
- **Code:** scratch originals `beat88/analysis/scratch/symmetry-orbits/pop2.py` (97 lines),
  `beat88/analysis/scratch/diversity-metrics-and-roots/rowdepth.py` (38 lines),
  `beat88/analysis/scratch/exact-certificates/probe2.py` (50 lines). **Shipped fold: B4 =
  `beat88/methods/shared/descriptors.py`** — `row_depth_profile` `:87-107`, `rho2_defect` `:110-134`,
  `neutral_out_degree` `:136-162`, combined `descriptors()` `:164-186`. The fold is **real in code**:
  `:5-14` names all three scratch sources by path and by finding. Note it took `rowdepth.py`, **not**
  the scratch `descriptors.py`, which holds the D1–D4 *negative* result and was correctly not promoted.
- **Logs:** **none for the scratch scripts** — every headline is a transcription of unsaved stdout.
  Validation of the folded version: `beat88/methods/shared/analysis/b4_validation.log` — 2,009 states,
  8 circuits, 200 states × 3 rotations, **MISMATCHES 0**; tests at `shared/tests/test_descriptors.py`
  (four properties, incl. `neutral_out_degree` vs an independent pure-Python complete enumeration).
- **Generality:** **MIXED.** The descriptor mathematics is circuit-generic (ASAP least-fixpoint over any
  mask set; defect of any set under any permutation; neighbourhood of any value set). The constants are
  MC-hardcoded one layer down: `descriptors.py:37` `RHO = tuple(((c//8 + 1) % 4)*8 + (c%8) …)` — the
  AES 4-byte × 8-bit column — and `range(32)` throughout; `:30-33` `TARGETS = K.TARGETS` from the C
  kernel (`csrc/slp_kernel.c:38`, `0x11B`); and the claim that `⟨ρ⟩ ≅ Z/4` is the *complete*
  automorphism group is MC-specific. **Port cost: swap the C target generator and re-derive the
  symmetry group (J6); the three descriptors themselves need no change.**
- **Phase-2:** **keeper — build all three on day 1 of a new circuit.** They are the cheapest honest
  answer to "is this population one basin or several?", and (c) doubles as a free improvement tripwire.
  ⚠ Re-measure (c)'s mode before quoting it, and quote (b)'s separation as **11–28**, not 18–26.

### A·8 · **N3** dated corrections ledger
- **What it does:** When a published claim turns out wrong or superseded, **nothing already written is
  edited**. A dated entry goes at the top of a Corrections section saying what changed, and the old
  claim stays on the page exactly as it was. A reader sees both what was believed and when it stopped
  being true.
- **Twist:** it separates **scope** entries from **correction** entries. The 2026-07-30 entry is filed
  as scope — *"Nothing here is withdrawn; no comparison figure changes"* (`PRIOR_ART.md:44`) — because
  it narrows how a true statement may be read rather than retracting a figure. Superseded circuits stay
  shipped with their original claim strings intact: *"Their earlier claim statements stand as made"*
  (`:61`).
- **Measured — counts derived by the audit, not copied.** In the separate records repo
  `~/xor_ui/aes_mc_records`: `PRIOR_ART.md` §Corrections (`:15-145`) **5** dated entries,
  reverse-chronological, 2026-07-23 → 2026-07-30; `PAPER.md` §Corrections (`:37-75`) **3**, each tied to
  a note version; `bounds.json` **6** appended `Updated <date>:` sentences (3 × 07-29, 3 × 07-30)
  appended to the original `claim` text. Discipline confirmed by inspection: claim strings retain the
  original and prepend *"Historical claim as of 2026-07-10, superseded (see PRIOR_ART.md Corrections)"*;
  `README.md:104` carries a `| File | Gates | Depth | Superseded by |` table; `PRIOR_ART.md:445` keeps a
  `## Earlier claims from this project (v1, superseded)` section. **It keeps and marks; it does not
  rewrite** — by prose supersession rather than literal strike-through. The outcome reproduces:
  `PRIOR_ART.md:66-68` — *"One statement made here on 2026-07-29 is now **false and is corrected**…
  **It does not**."* **Successor instance:** `wrapup/CORRECTIONS.md`, **56** `### C-nn` entries
  (`C-01` at `:30`, `C-56` at `:794`), dates 2026-07-23 → 2026-08-29, with a stronger explicit rule
  (`:9`): *"This register is read-only — no document has been edited."*
- ⚠ **Figure that does not reproduce as stated:** the source report's *"the current execution is 10,300
  words long"*. `PRIOR_ART.md` alone is **4,873** words; 10,300 is `PRIOR_ART + PAPER + README` =
  **10,329**. The number is right, the noun is wrong.
- ⚠ **Is the rule enforced by anything? No.** `aes_mc_records/.github/workflows/verify.yml` runs the
  verifiers and `unittest discover -s tests`; a grep for `correction` across `tests/`, `verify_all.py`
  and `scripts/` returns **zero** hits. No template, no linter, no CI gate. The discipline is entirely
  human, and git history shows it applied by hand.
- **Cost:** zero compute.
- **Code:** **none** — a pure editorial protocol.
- **Logs:** the ledgers *are* the artifacts: `~/xor_ui/aes_mc_records/{PRIOR_ART.md,PAPER.md,bounds.json,README.md}`
  plus that repo's git history, and `wrapup/CORRECTIONS.md`.
- **Generality:** **CIRCUIT-GENERIC.** Nothing in the protocol references MixColumns, GF(2⁸), `0x11B`,
  `[2,3,1,1]` or 32 targets. The *content* is MC-specific; the method is not. It ports by copying the
  section header and the scope-vs-correction distinction.
- **Phase-2:** **adopt on day 1, and add the enforcement it never had** — a CI check that any change to
  a claim string also appends a dated Corrections entry. That is the one cheap improvement the audit
  can name, and it is the difference between a discipline and a habit.

### A·9 · **B14** `L_cf` reuse-greedy + CP-SAT — *reframed: a method with a superseded result*
- **What it does:** Asks how many XOR gates MixColumns needs if **every gate must have operands with
  disjoint bit support** (no cancellation). It builds an answer greedily — for each output find the
  cheapest tree split, counting anything already built as free, then re-optimise one output at a time
  against the pool of all the others — then hands that to CP-SAT to shrink. It reached 103.
- **Twist:** **every intermediate state of the greedy is itself a valid cancellation-free program,
  closure-checked**, so the run yields a *certified* upper bound at every step rather than only at the
  end, and the witness replays by pure closure with no solver trusted.
- **Measured:** greedy alone **129** (3 rounds) → **113** (60) → **110** (300)
  (`fleet6/laneTOOL2/ledger.jsonl:47,48,49`, ts 23:51:23 → 23:52:53). CP-SAT seeded with the greedy:
  **FEASIBLE 103**, dual bound 92, 900.0 s, 1,648 vars (`:73`); re-run warm-started from the 103:
  **FEASIBLE 103** again, 1,500.2 s, **no movement on either end** (`:86`). Witness is 103 masks. The
  lower end is **not independent** — 92 was fed to the solver as a constraint
  (`lcf_cpsat.json: "used_refereed_lb_92_as_constraint": true`). G(3) bracket moved only
  `[86,94] → [92,94]` in 1,200 s.
- ⚠ **The supersession is worse than "superseded".** `beat88/understanding/v2_no_vocab/data/cf_incumbent.json`
  is dated **2026-08-15 15:35**; laneTOOL2's `L_cf` rows are **2026-08-23/24**. **The 102 predates the
  103 by eight days**, so `RESULT.md:741-742` — *"The project has no upper bound on `L_cf` at all"* —
  **was already false when written**, and the 103 is a **one-gate regression, not a first**. The audit
  re-verified the incumbent from the JSON alone: `gateCount` **102** = `len(gates)` 102; **32/32 targets
  built**; **cancelling gates κ = 0**; 102 distinct masks, no forward references. Its own log:
  *"ORACLE: VERDICT: VALID MixColumns circuit / cancelling gates (must be 0 …): 0 / ⇒ VERIFIED
  L_cf(M) ≤ 102"*.
- ⚠ **Still uncorrected at eight line numbers** in `fleet6/laneTOOL2/RESULT.md`: **152** ("First upper
  bound on `L_cf(M)` in this project"), **741-742**, **747**, **750-751**, **758-759**, **792**,
  **829** (table row 19), **831** (table row 21). Already registered as `wrapup/CORRECTIONS.md` C-19.
- ⚠ **Two further defects found in the primaries by this audit and in no existing report:**
  (1) `code/z1_lcf.py:164` reads `mdl.Add(obj >= 92)   # refereed CANON U6-2 lower bound, as a HINT
  ONLY` — the comment says hint, `mdl.Add` is a **hard constraint** (the JSON and RESULT.md get it
  right; the code comment does not). (2) `ledger.jsonl:85` logs
  `{"kind":"lcf_upper_bound","method":"reuse_greedy",…,"value":103}`, but that 103 came from CP-SAT —
  `z1_lcf.py:112-121` warm-starts the pool from the previous CP-SAT witness *before* the greedy result
  is logged at `:129-131`. **The ledger attributes a solver result to the greedy; the honest
  greedy-only figure is 110.**
- **Cost:** greedy ~**90 s** wall for the 3/60/300 sequence; CP-SAT **900.0 + 1,500.2 = 2,400.2 s at 4
  workers**. The superseding 102 cost **1,980 s** at 4 workers by a different route.
- **Code:** `fleet6/laneTOOL2/code/z1_lcf.py` (197 lines; `weighted_tree` `:38-62`, `greedy` `:65-97`,
  CP-SAT model `:139-176`), with `t2lib.py`, `phi2.py`, `w1_witness.py` (`closure_check`). Superseding
  route: `beat88/understanding/v2_no_vocab/code/cfincumbent.py`.
- **Logs:** `fleet6/laneTOOL2/ledger.jsonl` (89 lines; `L_cf` rows 47,48,49,72,73,85,86,88),
  `logs/final.log`, `results/{lcf_cpsat.json,lcf_upper_witness.json}`. Superseding:
  `beat88/understanding/v2_no_vocab/data/{cfincumbent.log,cfimprove.log,ctrl_lcf91.log}`.
- **Generality:** **MIXED — MC-hardcoded at the interface, generic in the algorithm.** `z1_lcf.py:108`
  `T = L.mixcolumns_targets()`; `t2lib.py:45` `coef = [2,3,1,1]`, `:23` `poly=0x11B`, `:95` `range(32)`;
  `z1_lcf.py:159` forces the 32 targets and `:165` hardwires **this problem's** refereed lower bound
  into the model. The reuse-greedy + coordinate descent over hierarchy trees, and the CP-SAT
  disjoint-split encoding, are generic over any GF(2) linear map. **Port cost: the target generator
  plus dropping the `>= 92` line.**
- **Phase-2:** **keeper as a method; the bound is dead.** Three things survive. (1) **The reuse-greedy is
  the only solver-free `L_cf` constructor in the repo** — 129 → 110 in ~90 s with no solver at all; the
  102 came from a CP-SAT optimisation of a different model and has no solver-free counterpart, so the
  greedy survives its own bound as a warm-starter and as a fallback where CP-SAT is unavailable.
  (2) **Closure-checked-at-every-step** (`z1_lcf.py:65-68`) is the reusable discipline: every
  intermediate is a certificate, so the method never has to trust the solver for the upper end.
  (3) The costed negative is worth keeping — 2,400 s at 4 cores moved neither end, and the diagnosis
  (ρ-symmetry unexploited, 8 orbits of 4 rows) is a concrete next step that applies verbatim to `G(3)`.
  **Never quote `L_cf(M) ≤ 103` again; `≤ 102` is the standing figure.**

---

# Appendix B — conflicts flagged (11)

Where two slice reports give different numbers for what sounds like the same
thing. Both figures are kept, with sources.

> ⚠ **This appendix was overtaken 33 minutes after it was written.**
> `wrapup/CONFLICTS_RESOLVED.md` (2026-08-29 10:47) resolves all eleven from
> primary sources — **22 resolved · 4 both-right-different-objects · 3 partially
> resolved · 0 fully unresolved**. Items #2, #6, #10 and #11 below carried stale
> or refuted text and are corrected in place (AUDIT 2026-08-29,
> `wrapup/day2/CATALOG_AUDIT.md` §5). **Read `CONFLICTS_RESOLVED.md` first.**

1. **`L_cf(M)` upper bound — four different values in current documents.**
   `fleet6/laneTOOL2` reports **103** (CP-SAT, closure-verified) as a first upper bound;
   `beat88/understanding/v2_no_vocab/data/cf_incumbent.json` holds an oracle-verified **102**
   (depth 5, zero cancelling gates); historical figures of **104** (an unextracted incumbent) and
   **133** (a referee's circuit) also circulate. `STATE_OF_THE_PROBLEM.md` records this as
   discrepancies D1/D10/D11 and it is **uncorrected in `fleet6/laneTOOL2/RESULT.md`.**
   *Best current statement:* `92 ≤ L_cf(M) ≤ 102`, both ends solid (I12 + F27).
2. **Integrality gap of the residual LP: "≥ 5" vs "≤ 0.5351".**
   `fleet2/laneP_proof` (I16) reports a **proven gap ≥ 5** on `88@5fs`, with a referee's exact
   `Fraction` recomputation giving **exactly 34** against `|counted| = 39`.
   `fleet6/laneTOOL2` (I17) reports that this refereed gap was a **misattribution**, true gap
   **≤ 0.5351**.
   **✅ RESOLVED** (`CONFLICTS_RESOLVED.md` §B2; corrected here 2026-08-29 — this item
   previously read "Unresolved"). **Claim B is right; Claim A mislabels a real quantity.**
   Both lanes agree the exact LP dual on `88@5fs` is **34**. laneTOOL2 *measured*
   `Φ(A*) = 34` exactly (matching lower and upper bounds, with a positive control that
   fired: on a planted 5-bit gap instance the tool returns `Φ = 8` by CP-SAT **and** by
   independent brute force against an exact dual of `15/2`). Lane P *assumed*
   `Φ(A*) = |counted| = 39` and read `39 − 34 = 5` as an integrality gap. So the residual
   covering LP is essentially integral (gap ≤ **0.5351** on `88@5fs`, < 1.15 on all nine
   measured circuits), and the **5 is the record circuit's clean-layer suboptimality**,
   `|counted| − Φ(A*)`, not an LP–IP gap. Two consequences: **Lane P's 83.000 ceiling
   STANDS and is strengthened** (it survives replacing the dual by the exact integral
   optimum: `88 − (39 − 34) = 83`); and **Lane C's `phi_equals_counted` is falsified on 3 of
   5 canonical 88s** (88@5fs 34 vs 39, 88@8 38 vs 39, 88@6 30 vs 31). The index row for
   I16 still reads "proven gap ≥ 5 ⇒ caps at 83" — the *cap* is right, the *reason* is not.
3. **Reachability grid: 137 cells vs 138 rows.**
   `fleet8/unified/RESULT.md` §7 reports **137 cells (33 VALID / 17 INFEASIBLE / 75 ELSEWHERE / 12
   UNDECIDED)**; the live `results/reach_grid.jsonl` has **138 rows / 13 UNDECIDED**. One row of
   drift after the write-up.
4. **Gauge-component sizes for 88@7 and the third family.**
   `beat88/methods/m1_cartography` reports "true gauge component" sizes **88@7 = 112,833** and
   **88@8 third family = 59,697** (both closed). `experiments/e14_plateau87` reports free-move
   closures of **26,730** and **4,212**. The 88@5 and 88@6 figures agree (729 / 2,187 / 10,935), so
   the discrepancy is in the *move class* (m1 includes union crossing, double transposition, and
   remove-1-add-2 / remove-2-add-1; e14/e16 use only re-association and re-parenting). **Both are
   correct for their own definition** — but the phrase "the closed component" must always name its
   move set.
5. **`n_components ≥ k`: "60 of 62 families" vs "FALSE, 8 of 204 violate".**
   `beat88/methods/m5_backbone` (J31) reports the inequality holding in **60 of 62** profiled
   families and reads it as the structural reason 87 is hard. `beat88/understanding/u1_obligations`
   (J32) reports it **FALSE — 8 of 204 violate**, naming all eight, and notes m5 had found 2 of 62.
   **Resolution: the conjecture is false;** the surviving statement is the disjunction
   `n_expensive ≥ 1 ∨ cover ≥ k`, 204/204, under a witness-free cost.
6. **Exact-window decider: "no completeness bug" vs "414/450 false irreducible".**
   `campaign_87/cert_audit` and `root_infra` report **4,200/4,200 planted YES windows answered
   correctly** with branch-deletion validation, concluding **no completeness bug — the ~165 M
   verdicts stand.** `beat88/analysis/code/exact-window-code.md` records a **defect: 414/450 false
   "irreducible" on *target* windows.** The scopes differ (target-mask windows vs free-mask
   windows). **Do not quote the decider on target windows without re-checking this.**
   **✅ RESOLVED — both right, disjoint inputs** (`CONFLICTS_RESOLVED.md` §B6; corrected here
   2026-08-29 — this item previously said "no document reconciles them explicitly", which is
   **false**). `beat88/analysis/code/exact-window-code.md` §4.5 reconciles them in the same
   paragraph as the defect: the docstring restricts windows to non-target masks but nothing in
   the code enforces it; every archived sweep used non-target windows only, **confirmed by the
   window counts matching `C(56,k)` exactly** — a control that could have failed — and the
   ≥4-mask theorem is unaffected, since any valid circuit contains all 32 target masks, so
   `S \ T` for a real 87 is automatically target-free. **No archived verdict is impugned.**
   ⚠ **Two live reuse hazards to carry into phase 2:** the module has no
   `assert not (window & TSET)`, so any reuse over raw mask sets (move generation over
   non-circuit sets) will get confidently wrong proofs; and `solve2`/`solve_deep` overload
   `None` for both "proved empty" and "deadline expired", resolved by re-reading `time.time()`
   on a box whose clock is known to step backwards — archived sweeps report zero timeouts, so
   nothing archived is impugned, but **any rerun must use `time.monotonic()`**.
7. **The published depth-4 record: 92@4 vs 91@4.**
   `README.md`, `spectrum.json`, `PAPER.md` and `PRIOR_ART.md` all say **92 @ depth 4**. Three
   independent oracle-verified **91 @ depth 4** circuits exist on disk (cascade ladder / m3 census /
   atlas-M1 reschedule; pairwise Jaccards 0.556 / 0.433 / 0.358 — three distinct lineages), plus a
   pod manifest holding **15,650 further 91@4 records**. **The public claim is understated by a
   gate.** (N6, C24, J1.)
8. **k=14 cube coverage: 51/528 vs 87/528.**
   `fleet11/laneCUBE/RESULT.md` reports **51/528 UNSAT at write-up**; a re-count on 2026-08-29 gives
   **87/528 UNSAT, 0 SAT, UNDECIDED**. Same run, different times — the lane is LIVE. Any figure
   quoted must carry its date.
   **✅ RESOLVED — one monotone live run sampled at three times** (`CONFLICTS_RESOLVED.md` §B8):
   51 (2026-08-26 12:21) → 73 (undated) → **87 (2026-08-29 08:27 −0400)**, re-tallied by distinct
   cube id: 528 distinct cubes seen, **87 UNSAT, 0 SAT, 441 open**. The lane's own
   pre-registration binds the reading: *"BRACKET only: 'X of 528 cubes UNSAT' — UNDECIDED, never
   a refutation."* **Never write 51/528, 73/528 or 87/528 without its timestamp.**
9. **laneCUT window counts: two published figures do not reproduce.**
   The published **14,564** was a transcription error for **18,564** (88@5fs). The published
   **387,395** (88@7) **does not reproduce** — the e15 re-run gives **386,922**. Both errata are
   recorded in place and neither changes a result (0 compressible either way).
10. **"Known 88s" population sizes are used interchangeably across documents and count different
    objects.** Figures in circulation, each correct for its own object: **14** (named records) ·
    **3,254** (a wiring census corpus) · **17,283** (distinct mask multisets in the repo corpus) ·
    **18,355** (valid 88 JSON files in the repo corpus) · **33,010** (the complete known 88
    population as gauge orbits) · **44,793 / 378,189** (states in closed free-move orbits) ·
    **54,889** (distinct 88-gate mask sets decomposed) · **78,281** (distinct 88-mask states in one
    harvest) · **105,801 / 139,878** (distinct known 88 states, the second corrected to the first in
    two files) · **242,974** (distinct live-trimmed 88-gate circuits) · **434,125** (distinct
    verified 88 mask-sets) · **836,598 / 850,784** (distinct 88-gate states in the beat88 index) ·
    **3,280,541** (distinct 88-gate circuits across 460 population files). **Never quote a
    population size without naming the object and the dedup rule.** A cross-lane audit already
    flagged three of these as used interchangeably.
    **✅ SUPERSEDED BY `wrapup/CORPUS88.md`** (`CONFLICTS_RESOLVED.md` §B10; added here
    2026-08-29 — none of the figures above is the corpus headline). CORPUS88 re-hashed every
    source under one identity (sorted mask multiset), and four independent controls on it came
    out **exact**. The headline is **1,575,516 distinct verified 88-gate mask sets**, of which
    **28,796** carry a banked build order and **92** of those are at the record depth 5. It is a
    **floor**: the honest project-wide range is **1.6 M – 4.4 M** distinct. Quote the CORPUS88
    tier table, naming the object and the dedup rule.
11. **`B37` price 3 vs the published 89.**
    `fleet12/laneHINTS` (H47) measures `B37` at **3, not the hinted 4**, at the `rec_88at7`
    three-value commitment, so **that configuration's price is 88, not the published 89** — with a
    verified circuit on disk. The same test at a second configuration is **refuted** (k=3 UNSAT).
    ~~The published figure has not been corrected.~~
    **✅ RESOLVED, and the struck sentence was wrong** (`CONFLICTS_RESOLVED.md` §B11; corrected
    here 2026-08-29, re-confirmed independently by this audit). It **is** corrected in two
    places — `fleet8/unified/REACHABILITY.md:236` (*"Line 111 … is stale: the true uncapped price
    is 88"*) and `fleet12/LIBRARY.md:310` (*"`rec_88at7` **88** (was published 89 — corrected by
    axis 2)"*). **What remains stale is only the data row itself, `REACHABILITY.md:111`.** The
    emitted circuit is oracle-verified (`gates=88 depth=8 outputs_built=32/32`). **No public
    frontier moves** — 88 @ depth 8 is already held — and the "89" is an internal generator
    config price, not a public record: do **not** put it in a public repo as a result.

---

*End of catalog. 309 methods, 14 families. Written 2026-08-29 from the ten slice
reports in `wrapup/reports/`; every number was copied from those reports and
every path was as they gave it. **Revised the same day by an adversarial audit
against primary sources** (`wrapup/day2/CATALOG_AUDIT.md`): paths repaired, 41
entries annotated with what did not reproduce, 8 starter-kit rows repriced,
Appendix B reconciled with `CONFLICTS_RESOLVED.md`, and all nine Appendix A
skeletons completed. See the CHANGELOG below for the full list. Nothing outside
`wrapup/` was written or modified.*

---

# CHANGELOG

### 2026-08-29 — adversarial audit pass (`wrapup/day2/CATALOG_AUDIT.md`)

An adversarial referee rebuilt 62 entries from **primary sources** — the actual
code files and the actual logs/ledgers, never the slice reports this catalog was
written from — audited all 38 rows of the phase-2 starter kit, re-derived every
count claim the document makes about itself, cross-checked six Appendix B items
against `wrapup/CONFLICTS_RESOLVED.md`, and closed all nine Appendix A skeletons.
**Result: 37 PASS · 24 FAIL · 1 UNVERIFIABLE.** Edits applied, all of them
additive or corrective in place — no entry was moved, merged, renumbered or
deleted, and the total remains **309 methods in 14 families**:

1. **Paths repaired (51 lines).** Unresolvable path citations fell from **79 to
   30** (the residue is relative continuations within an entry, plus the
   `aes_mc_records` paths now marked as a separate repo). Three systematic
   causes, all mechanical: `wave5/` → `campaign_87/wave5_2026-08-04/` and
   `wave6/` → `campaign_87/wave6_2026-08-11/` (the date suffixes were dropped);
   bare `eNN_*/` → `experiments/eNN_*/`; bare `agents/`, `hunt87/`, `d3_exact/`
   → `campaign_87/…`. Every repaired path was verified to resolve.
2. **41 entries carry a new `AUDIT (2026-08-29)` line** recording what did not
   reproduce, what the code actually says, or what caveat the entry dropped.
   The 24 FAILs are: A10, C3, C15, D7, F8, F9, F12, F17, F27, G4, G18, H19, H27,
   H29, H34, I30, J6, J13, J40, K1, K2, K3, L3, L4, M1 (25 entries; J13 is the
   single UNVERIFIABLE). The rest are PASS entries with a material caveat.
3. **Eight starter-kit rows repriced.** Rows **2 (K1)**, **4 (A10)**, **5 (K2)**,
   **7 (A2)**, **14 (J1)**, **17 (E1/E2)**, **32 (F8)** and **36 (I5+I7)** carried
   port costs the code contradicts ("one constant", "none", "swap the target
   matrix", "one-line target change") or paths that do not resolve. Row 36's
   `L ≥ 56` in particular needs a fresh 9.43 × 10¹⁰-node depth-4 exhaustion at pod
   scale, not one line.
4. **Header corrected.** "13 groups" → 14; the claim that all 11 numeric
   conflicts are flagged inline is replaced by the true correspondence (six are);
   and a standing audit caveat was added — **130 of 309 entries carry no
   `Generality` line at all**, so absence of a label is not evidence of
   portability.
5. **Appendix B updated against `CONFLICTS_RESOLVED.md`** (written 33 minutes
   after this catalog). Item **#2** no longer reads "Unresolved" — the "gap ≥ 5"
   is a misattribution and the 83.000 ceiling is strengthened, not weakened.
   Item **#6**'s "no document reconciles them explicitly" was **false** and is
   struck, with the two live reuse hazards (`assert not (window & TSET)`,
   `time.monotonic()`) promoted into the text. Item **#8** now carries its
   mandatory timestamp. Item **#10** is superseded by `CORPUS88.md`'s
   **1,575,516** headline. Item **#11**'s "the published figure has not been
   corrected" was **false** and is struck.
6. **All nine Appendix A skeletons completed** (§A·1–A·9), each in the catalog's
   own schema and each written from primary sources. **None was a non-method.**
   Two carry findings that outrank their headlines: **H45**'s "48/48 UNSAT" has
   **zero surviving primary artifacts** (the driver was wiped; it is 48 machine
   checks, not a theorem), and **M3**'s parity-hub separator is **false** —
   refuted by exhibition in wave 6 and by a 1,925,065-circuit census that finds
   P7, the claimed corpus-wide blind spot, in **1,429,688** of them.
   **F30** is completed as a zero-result entry: the instrument was built, fleet9
   independently asked for it, and it was never run.

**Not fixed, and named so a successor can price it:** the 130 entries with no
`Generality` label. Filling them needs the same code-opening pass this audit did
for 62 entries, and the audit found the label wrong in **nine of the eleven cases
where one was present and checkable** — so the missing 130 should be assumed
unknown, not assumed generic.
