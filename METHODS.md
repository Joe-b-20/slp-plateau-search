# The method: value-set SLP search, plateau walking, and exact local certificates

This document specifies the search method behind this project's AES MixColumns
XOR circuits: 97 gates at depth 3, 92 at depth 4 and 89 at depth 5 — the three
that improve the *published* depth–count frontier at their depths — plus
four 88-gate circuits: an independent 88 at depth 7 that *ties* the
published gate-count floor without beating it, an 88 at depth 6 found **from
scratch**, and two whose seed chains pass through published work (88 at depth 5,
88 at depth 8). Combined verified frontier: 97 @ 3, 92 @ 4, 88 @ 5. Own-lineage
frontier: 97 @ 3, 92 @ 4, 89 @ 5, 88 @ 6. See `evidence/RESULTS.md` and the
artifact repository
[aes-mixcolumns-xor-circuits](https://github.com/Joe-b-20/aes-mixcolumns-xor-circuits).
Everything here is implemented in dependency-free Python in this repository.
Three of those circuits — **97 @ 3, 92 @ 4 and 89 @ 5** — are reproduced by that
code with no AI system in the loop, as is a single-worker re-run of the 88 @ 7.
The v2 engine of Sections 4–6, the certificates of Section 10 and **all four**
88-gate circuits came out of author-directed LLM-agent campaigns (Section 13) —
the 88 @ 7 and 88 @ 8 from the 24-agent campaign of 2026-07-26/27, the 88 @ 6 and
88 @ 5 from the later multi-day fleet of 2026-07-28/29 — and the 88 @ 6 in
particular has no single-command reproduction (`reproduce/README.md` says why).
Every circuit any of it produced is machine-verified against MixColumns rebuilt
from GF(2⁸).

## 1. Problem and model

Implement the AES MixColumns map — a 32×32 matrix over GF(2) — as a circuit
of 2-input XOR gates, minimizing the gate count (the Shortest Linear Program
problem, NP-hard), optionally under a depth cap. The specification is rebuilt
from the GF(2⁸) definition in `*/mixcolumns_core.py`; an independent oracle
(`verify_circuit.py`) checks every claimed circuit. Nothing here is claimed
optimal: the negative results of Section 10 are local, and none of them bounds
87 away globally.

## 2. The representation: circuits as value-sets

A circuit is represented not as an ordered gate list but as a **set of GF(2)
bit-masks** over the 32 inputs (one mask per gate output). A set is a valid
circuit iff it is *realizable* — starting from the 32 input singletons, every
mask in the set equals the XOR of two already-available masks — and contains
all 32 MixColumns output masks. Gate count = |set|. Three things follow:

- "delete a gate and see if the circuit still works" becomes a set operation;
- two circuits are comparable by mask overlap regardless of gate ordering (the
  Jaccard index used for families in Section 11);
- a *neighbourhood* — "remove these k masks, add at most k−1 others" — is a
  finite object that can be enumerated exhaustively (Section 10).

## 3. The motivating observation

Good circuits at this size *look* locally efficient — every gate reads as an
optimal step. That was true of the naive construction this project started
from and of every circuit it produced up to the 89, and it is exactly what
makes them hard to improve: such circuits sit at local optima, so any further
reduction has to pass through intermediate circuits that contain locally
*suboptimal* steps. (No claim is made here about how anyone else's circuit was
constructed.) The method is therefore built around moves that are individually
neutral or worse but globally productive, and acceptance rules that let the
search traverse them.

At 88 gates that reading is now measured rather than assumed: on every 88 whose
shell has actually been swept — 47 canonical circuits and the 88 @ depth 6
exhaustively at k ≤ 3, the 88 @ depth 5 at k = 2, and 105 801 harvested
population states at k = 2 — the enumerated move classes come back **empty**,
every time (Section 10; this project's own 88 @ 7 is not among the 47).
Nothing is gained by searching harder for one clever step; what produced all four
88-gate circuits was the opposite — making the *equal-size* plateau cheap to
walk, and walking a very large amount of it, from as many different starting
basins as possible.

## 4. The moves

- **remove-1**: drop a non-output mask; keep the smaller set if it is still
  realizable. (A genuine −1 cut; rarely available on good circuits.)
- **neutral swap (plateau walk) with exact repair**: remove one mask and add
  one *repair* mask that restores realizability — size unchanged. The repair set
  is now enumerated completely rather than sampled. After the removal let
  `A = closure(S₂)` and `stuck = (S₂ ∪ T) − A`. A mask `w` can repair `S₂` only
  if (a) it is buildable now, i.e. `w ∈ P₂(A)`, the pair-sums of `A`, and (b) it
  unlocks something, i.e. `w = u ^ a` for some `u ∈ stuck`, `a ∈ A`. So
  `C = {u ^ a} ∩ P₂(A)` **contains every possible single-mask repair**, and
  iterating over it decides the move (`pipeline/engines.py:_repair`). Measured
  `|C| ≈ 7` — complete enumeration is *cheaper* than the 24–40 random candidates
  the previous engine tried, which missed 81–82 % of the repairs that existed.
  Exact repair gave ~7× plateau mobility (1.9 → 13.6–16.3 distinct states/s) —
  time-to-89 from the 90 @ depth 5 seed went from 0 of 6 runs to 3 of 4 — and is
  how every 88 here was reached. The just-removed masks are passed as `forbid`:
  re-adding one is a ping-pong no-op.
- **remove-2-add-1 ("hub" move)**: remove two masks, add one repair mask. Kept
  in the walk (`hub_move_p`) as a diversifier, but at the 88/89 frontier it is
  **provably dead** — Section 8.
- **destroy-and-rebuild (LNS)**: remove a group of masks and re-synthesize from
  a candidate pool. Three operators are mixed (`op_mix`): `small` (1–4 random
  masks), `coneinj` (a *connected* cone of the circuit DAG plus injected local
  candidates), `biginj` (a large random destroy plus injection). Removing a cone
  leaves a hole the rebuild can genuinely re-plan; k unrelated masks usually just
  get re-derived — `coneinj` measured ~12× improvements/s and is the only
  operator that makes destroy sizes 3–4 productive.
- **depth-aware reconstruction**: `relax` gives each mask's minimum build depth
  over the set; candidates over the cap are rejected and gate lists emitted in
  depth order (`order_by_depth`), turning any realizable set into an explicit
  circuit respecting the cap. Uncapped, any topological witness from the closure
  is already a valid circuit (`_walk_gates`) at ~50× less cost.

```mermaid
flowchart TD
    A["S := value-set of a starting circuit"] --> B{"pick a move:<br/>remove ONE non-output mask,<br/>or TWO with prob. hub_move_p"}
    B --> E{"incremental closure query:<br/>is S - D still realizable?"}
    E -->|no| F["EXACT repair: enumerate<br/>C = (stuck ^ avail) ∩ pairsums(avail),<br/>minus the just-removed masks"]
    F -->|"C admits none"| G["undo the move"] --> B
    F -->|"repair found"| H
    E -->|yes| H["trim S to what the 32 outputs need"]
    H --> I{"depth-capped and<br/>min-build-depth > cap?"}
    I -->|yes| G
    I -->|no| J{"did cur actually change?"}
    J -->|no| B
    J -->|yes| K["harvest this distinct mask set"]
    K --> L{"fewer gates, or equal<br/>gates at lower depth?"}
    L -->|no| B
    L -->|yes| M["verify against the GF(2^8) spec"]
    M -->|correct| N["best := S"] --> B
    M -->|rejected| B
```

## 5. The kernel: closure, relax, and the improve-spam fix

Both search engines spend nearly all their time answering two questions — "what
can this mask set build?" and "at what depth?" — so the kernel is where
throughput lives. Three rewrites, each checked against the function it replaced,
plus one bug that dominated everything else:

| change | what it does | measured |
|---|---|---|
| `relax`, level-BFS | resolves build depth one level at a time, so a mask is tested only against the level that could lower it; same least fixpoint, bit-identical 1 500-iteration trajectories | **17.5×** end-to-end LNS (42.3 → 739 it/s); 18.9× per call |
| `_closure_core`, worklist BFS | re-tests a mask only when a *new* mask it could pair with appears, with a `stop_at_targets` early exit for feasibility and trim | O(\|S\|²) instead of repeated full re-scans |
| `_WalkState.remove_query` | marks only the masks whose derivation transitively used a removed mask and re-derives those; still the exact least fixpoint of `S − D` | part of the 21.9× below |
| improve-spam fix | the Pareto tie-break called `ctx.improve` (full relax + oracle verify) on *every* plateau iteration, including rejected moves where `cur` never changed — **78 % of walk runtime** | **21.9×** walk (12.3 → 269 it/s; ~395–430 on 4 procs) |

`relax_reference` is kept verbatim as ground truth and as the duplicate-mask
fallback. End to end the merged engine walks at **480–640 it/s** against ~70–110
before, and runs LNS at ~100–180 against ~60–100, with much richer
neighbourhoods — 289 k walk iterations in one 600 s chunk under full fleet load.
Smoke gate: from `pipeline/seeds/seed_90_at_depth5.json` the walk reached a
verified 89 @ depth 5 in 42 s in the archived run.

## 6. The engines

Three engines share the moves and the verify-before-claim contract (an engine
never claims a count; it proposes candidates, and a candidate becomes "best"
only after the GF(2⁸) oracle verifies it at the active depth cap):

- **`walk`** (`pipeline/engines.py:engine_walk`) — remove-1 and hub moves over
  the incremental closure, with exact repair. Both new 88s came from walk chunks.
- **`lns`** (`engine_lns`) — destroy and rebuild, with the mechanisms below.
- **`anneal3`** (`engine_anneal3`) — a from-scratch depth-3 constructor. Each
  output is modelled as A ⊕ B where A, B partition its bits into depth-≤2 parts;
  auxiliary signals are refcount-costed, so shared parts are paid once.
  Simulated annealing over the per-output split choices, plus greedy descent and
  iterated local search with random kicks. Depth ≤ 3 holds by construction.

| LNS mechanism | why | measured |
|---|---|---|
| **victim-repool** (`_extract` cost classes: 1 kept, 2 sampled/injected, 3 just-destroyed victim) | victims stay available instead of being excluded, so a rebuild never dead-ends, while the higher cost still pushes it elsewhere. Before, 98.8 % of iterations bailed at `_extract`'s up-front check *after* paying for `relax` | **~34×** accepted moves/s, 6.4× distinct sets/min; 100 % feasible iterations |
| **scored pools** (current masks + pairwise sums + accumulated masks; a "hot" list of masks a rebuild actually reintroduced, drawn `hot_frac` of the time) | concentrates candidates on what has already proved useful here | **~11×** accepted moves; 16–18× pool hit rate |
| **peel-before-accept** (`peel_window`) | a rebuild a few masks too big is usually redundant, not wrong; peeling before judging it is also what makes the large `biginj` destroys viable | **2 630** near-miss rebuilds recovered in a 2-minute probe |
| **SA with reheat** (`sa_T0`, `sa_cool`, `sa_reheat`) | uphill rebuilds on a cooling schedule that resets when no new best has appeared for `sa_reheat` iterations; the old threshold rule stays selectable | **~2×** drift, best simple schedule tested |

**Plateau harvesting** (`_Harvester`, shared by both search engines) is the
second half. Only a strictly better — or equal-size but shallower — circuit is
ever exported, yet the search constantly walks over sibling circuits of the same
size and used to discard them. Harvesting appends every distinct equal-best mask
set to a `.pop.jsonl` population file; that population is the ≈ 139 878 distinct
known 88-gate states, and all four 88s were found inside harvesting runs. With
`pop_glob` a worker also merges **sibling** workers' harvests into its rebuild
pool (cross-pollination) — an LNS-only knob, **off in the shipped
configuration**, because it mixes the mask provenance of every worker in a run
(Section 9).

## 7. The pipeline

`pipeline/ladder_parallel.py` orchestrates OS-process workers (`worker.py`),
each running one engine at one depth cap in fixed-length chunks. The engine name
`alt` is a worker *mode*, not an engine: it alternates a short walk chunk (300 s)
with a longer LNS chunk (600 s), and that is what the best-performing hunt
workers ran, including every one that found an 88. Crucially, a chunk does **not**
continue from wherever the previous chunk drifted to: after every chunk the
worker reseeds from its own Pareto best (`seed_masks = set(ctx.best_masks)`,
`pipeline/worker.py`, and identically in the archived
`evidence/campaign87_run_2026-07-26_got_88at7/code/hunt_worker.py`), and
`ctx.best_masks` only moves on an oracle-verified Pareto improvement. So an LNS
chunk that fails to improve the best is a **no-op on the state the next walk
chunk sees** — so a non-improving LNS chunk cannot smuggle pooled masks into the
walk's lineage at all, and this is the mechanical half of the 88 @ 7
independence argument of Section 9 (there, *no* LNS chunk on that worker ever
improved its best). Two facts belong together here: the archived record run had
cross-pollination *enabled* (`pop_glob` set for its LNS chunks), while the
shipped configuration defaults it off (`cross_pollinate=False`,
`pipeline/ladder_parallel.py`) — the record is independent not because the knob
was off but because no LNS chunk on that worker ever improved its best. The
multi-day fleet that later produced the 88 @ 6 and the 88 @ 5 never set `pop_glob`
at all: its `hunt_worker.py` passes only `harvest_path`, so those workers write
harvests and never read a sibling's.

- **Pareto tie-break**: a worker's `improve()` accepts a candidate with fewer
  gates, **or equal gates at strictly lower depth**. Equal-gate-shallower
  circuits are surfaced rather than discarded — this is how 89 @ depth 6 became
  89 @ depth 5 within minutes of being offered as a seed, and how all four 88s
  were tie-broken one to three levels shallower within seconds of first being
  seen: depth 11 → 7, depth 10 → 8, depth 7 → 6 and depth 6 → 5.
- **Reseeding / the ladder**: the coordinator tracks the global best and offers
  each worker the best circuit feasible at its depth cap; workers adopt offers
  that Pareto-beat their own best between chunks. In cascade mode rung d3 starts
  from scratch (`anneal3`) and each deeper rung is seeded from the rung above —
  the from-scratch lineage in `evidence/RESULTS.md` came from this ladder.
- **Family workers**: the shipped `hunt87` set runs one uncapped worker on each of
  the three 88-gate family anchors it ships (families 1–3 of Section 11) with
  `reseed=False`, plus one depth-capped worker on the depth frontier. Opting out
  of reseeding is deliberate — an equal-size shallower offer would collapse all
  three family workers onto one circuit and throw away the diversity the set
  exists for. The fourth family (Section 11) was found later, by a separate
  multi-day fleet whose workers each hold their own root; its anchor is
  `evidence/circuits/mixcolumns_88gates_depth6.json`.

Every run self-archives its exact code into its output folder, so archived
results are always reproducible from their own directory.

```mermaid
flowchart LR
    W1["d3: anneal3<br/>from scratch"] -- "verified bests" --> BO["best_overall.json<br/>(global Pareto best)"]
    W2["d4: lns<br/>seeded from d3"] -- "verified bests" --> BO
    W3["d5..d11: lns / alt<br/>or the hunt87 family workers"] -- "verified bests" --> BO
    BO --> RS["reseed offer: best circuit<br/>feasible at that worker's cap"]
    RS -- "adopted between chunks iff Pareto-better,<br/>cap-feasible, and reseed is on" --> W2
    RS --> W3
```

## 8. What was measured and rejected

Negative results are part of the evidence, and several of them redirected the
search:

| finding | evidence |
|---|---|
| **the hub move is dead at the frontier** | 0 successes in ~2.24 M repair samples across all seeds, then proven exactly: the remove-2-add-1 neighbourhood of every one of the five 89 seeds is *empty*, and likewise inside the certified k ≤ 3 shells of Section 10 |
| **knobs are not the lever** | a wide grid sweep gave **0 improvements in 101 runs**; the shipped values are measured-good, but throughput and neighbourhood *shape* are what move the search |
| **LAHC is inert** in this acceptance role | **measured** inert: 0 uphill acceptances (up% 0.00, zero excursions) at both L = 200 and L = 2 000 in the instrumented 3-seed schedule comparison, because uphill proposals are near-nonexistent — it degenerates to hill climbing. SA-with-reheat replaced it |
| **uniform destroys do not rebuild** | uniform sizes 3…6 gave 0 accepts in 5 633 attempts, the periodic `kshake` destroy 0 in 293 — which motivated the connected-cone operator and injection |
| **random repair is worse than exhaustive** | missed 81–82 % of existing repairs at higher cost than enumerating all ≈ 7 (Section 4) |

The shipped `champ_fast` values (`nsamp=(12,12)`, `kmax=4`, `snapback=12`) buy
+30–80 % throughput at equal drift acceptance. Near-dead knobs are documented
rather than silently kept: `up_prob` is a binary drift switch, `nsamp=(48,48)` is
3× slower for no benefit, `kmax ≥ 10` is wasted.

## 9. Provenance: what is ours, what is derived, what is imported

Every circuit is reported in one of three classes: **from scratch** (no seed at
all); **own lineage** (seeded from this project's own prior output, transitively
back to a from-scratch root); **derived from published work** (the seed chain
passes through someone else's circuit, however far back — ours to *report*,
never ours to *claim*, and always credited).

The four 88-gate circuits fall in three different classes, and the difference is
stated wherever any of them appears:

```mermaid
flowchart TD
    R["97 @ d3 — FROM SCRATCH<br/>(anneal3, 2026-07-13)"] --> S89["89 @ d6 → 89 @ d5<br/>(own lineage)"]
    S89 --> S94["ρ²-symmetric 94 @ d5<br/>(symmetrize + orbit-peel + orbit-LNS)"]
    S94 --> N88["88 @ d7 — OURS, own lineage,<br/>no imported material"]
    S94 --> O91["a 91 of our own lineage"]
    R2["139 @ d3 — FROM SCRATCH<br/>(random XOR trees, naive#2163, 2026-07-28)"] --> F88["88 @ d6 — OURS, from scratch,<br/>fourth family"]
    J["Jean's published 88 @ d7<br/>ePrint 2026/1481 — IMPORTED"] --> J92["symmetrized + peeled to 95,<br/>orbit-walked to 92"]
    J92 --> U["union → ρ²-symmetric 90 @ d9"]
    O91 --> U
    U --> T88["88 @ d8 — found by our engine,<br/>DERIVED FROM PUBLISHED WORK"]
    U --> D88["88 @ d5 — found by our engine,<br/>DERIVED FROM PUBLISHED WORK"]
```

- The **88 @ depth 7** is own lineage, rooted in the from-scratch 97 @ depth 3.
  No imported mask enters the chain: the walk engine has no pool and only adds
  masks derived from its own value set's closure, cross-pollination is an
  LNS-only knob, and in the archived run every improvement on that worker came
  from a walk chunk — its 89 @ 7 predates the worker's first cross-pollination
  event, and no LNS chunk there ever improved the best. It **matches** the
  published record (Jean, ePrint 2026/1481) **with an independent circuit** —
  61 of 88 masks shared, Jaccard 0.530. It does not beat it.
- The **88 @ depth 6** is **from scratch**, and the load-bearing fact is the
  **root**, not any knob. That worker's root spec was `constructor:naive`, and the
  `constructor:` branch of `Roots.next` in the archived `hunt_worker.py` calls
  only `constructors.build(name, seed)`: it has **no file-reading path at all**.
  Every branch of that class that can read a circuit off disk — `pool89`, `file:`,
  `glob:` — is a different branch, and none of them was reachable under this
  spec. All **38** restarts logged in the worker session that produced this
  circuit opened on a `naive#<seed>` root, and the one that produced it, restart
  18, opened on `naive#2163`, which rebuilds from the archived `constructors.py`
  to exactly the logged 139 gates at depth 3 — randomized balanced XOR trees over
  the 32 raw inputs. A search that starts from a root reading nothing cannot
  inherit anything through its root; 37 minutes later it was at 88.

  Two further routes are closed by the *run* rather than by the root, and they
  are worth stating separately, because the derived 88 @ depth 5 below is proof
  that the knobs are not the whole story — material reached *that* circuit
  through its **root**. (i) Cross-pollination. `supervisor.py` as run is not
  archived (it was edited before the archive was cut), so this is an explicit
  two-part argument rather than a single check: the archived `hunt_worker.py`
  sets only `harvest_path` on both engines and **never mentions `pop_glob`
  anywhere**, and independently, `engine_lns` emits an
  `[lns] cross-pollinated N masks` line every time a merge brings in new
  material — of which the worker's untouched log contains **zero**. Code and log
  agree. (ii) Repulsion: `repel=False` on the log's first line, so
  `repel_masks.json`, which holds the three older families' masks, was never
  opened. Beyond those, each restart builds a fresh `LocalCtx` and resets `cur`
  to the new root, so the 88 @ 8 the same worker had found on the *previous*
  restart from a different root did not seed this one. (One LNS chunk of restart
  18 did improve the best, 92 → 90; with `pop_glob` unset its pool is built only
  from its own masks and their pairwise sums. The 89 and both 88-gate states came
  from walk chunks.) It is a **fourth distinct family** (Section 11), and its own
  k ≤ 3 shell is exhaustively empty — the only circuit here for which that is
  true *and* whose lineage is independent of Jean's, since the 88 @ 8 is the
  family-3 anchor among the 47 (Section 10).
- The **88 @ depth 8 and the 88 @ depth 5** were both found by our engine, but
  **both seed chains pass through Jean's published circuit**, at the same place:
  Jean's 88 was ρ²-symmetrized and peeled to 95, orbit-walked to 92, unioned with
  a 91 of our own lineage to give the ρ²-symmetric 90 @ 9. The 88 @ 8 descends
  from that 90 directly; the 88 @ 5 descends from it through one ρ²-equivariant
  orbit cycle that returned a mask-identical 90. Both are reported as **derived
  work** — the 88 @ 8 as a third distinct family (dominated by our own 88 @ 7,
  so not a frontier point), the 88 @ 5 as the shallowest 88 here and, at Jaccard
  0.735, a member of our record 89 @ 5's basin rather than a new family. The
  common cause was a seed-rotation bug that made the one own-lineage orbit seed
  unreachable; it is fixed, and `evidence/campaign87_run_2026-07-29_got_88at5_derived/`
  documents it.
- **Imported circuits are always credited, never counted as results**: Jean,
  ePrint 2026/1481 (88 gates) and Sun–Yang–Li, ePrint 2025/1493 (89 gates).
  Neither paper states a depth; the depths quoted here — 7 and 9 — are this
  repo's measurements of its own transcriptions. Those depths are **forced, not
  merely observed**: running `pipeline/engines.py:relax` over each transcribed
  mask set gives the ASAP (least-fixpoint) schedule, the shallowest schedule any
  circuit on that mask set can have, and it still puts three of Jean's output
  masks at depth 7 and one of Sun–Yang–Li's at depth 9. Neither circuit can be
  rescheduled shallower without changing its mask set, so the depth-6 88's
  domination of Jean's point does not rest on a scheduling choice of ours. This
  check was suggested and independently run by an external first-reader before
  being reproduced here. Both circuits are oracle-verified and kept under
  `evidence/campaign87_imported_prior_art/` and `pipeline/seeds/` with
  `_imported` in the filename.

### The earlier (v1) circuits

The project's first three circuits — 98 @ depth 3, 91 @ depth 6, and 89 @
depth 10, released 2026-07-10 and now superseded — were found by earlier, more
primitive versions of the same search. **The exact code state that produced them
was not preserved**: it was edited in place before being archived. That mistake
is the direct reason the pipeline now self-archives its exact code into every
run folder, and why every later record has a complete code-and-log trail while
these three do not. What is reconstructable:

- **91 @ depth 6** — the neutral-swap plateau walk applied to the published
  92-gate circuit of Xiang, Zeng, Lin, Bao, and Zhang; that reduction replays in
  `reproduce/reproduce.py` (method `"91"`).
- **89 @ depth 10** — seeded value-set walks. The original discovery path is not
  cleanly reconstructable; the equivalent 90→89 reduction replays as method
  `"89"`.
- **98 @ depth 3** — an early version of the depth-3 constructor of Section 6.

No current claim depends on them; the later records dominate all three. They
remain in the artifact repository as verified artifacts, correctness being
machine-checkable regardless of provenance.

## 10. Exact neighbourhood certificates

A search can only report what it found. To say anything about what is *not*
there, the repo uses a decision procedure instead.

**The question.** Given a verified 88-gate circuit and a *window* of k masks
removed from it, can at most k−1 new masks — each buildable at the moment it is
added, with cascade unlocks in between — restore all 32 targets? A "yes" is an
87-gate circuit; a "no", run to completion, is a proof for that window.

**The procedure.** Frontier-cascade closure with rollback, decided by budget:
budget 1 (k = 2), budget 2 (k = 3), budget 3 (k = 4). Completeness is proved by
first-unlock case analysis in the producing modules' docstrings — the first
unlock must have the newest added mask as a parent, which pins each added mask
to a finite, enumerable shape — so a `None` answer with no deadline expiry is a
machine-checked proof, not a failed search. **Both deciders ship with that
proof**: `evidence/campaign87_certificates/code/exact_window.py` (budgets 1–2)
and `exact_k4.py` (budget 3), verbatim as archived, are the modules that
produced every verdict log in `evidence/campaign87_certificates/`. Runs above the proved budget are
recorded as `nosol`, never as `irreducible`. Validation: budgets 1 and 2 agree
with an independent brute force 25/25 and 12/12; budget 3 agrees on **1 257
instances including 122 genuine NOs**, identically under CPython 3.10 and
PyPy 3.11.

**What is proven** (full write-up and archived verdict summaries:
`evidence/campaign87_certificates/CERTIFICATES.md`):

- **47 canonical 88-gate circuits have exhaustively empty k ≤ 3 shells** — all
  1 540 k=2 windows and all 27 720 k=3 windows each, zero reducible: Jean's 88,
  its 12 plateau siblings, and the third-family anchor with 33 representatives.
  Consequence: **any 87-gate circuit differs from each of them by ≥ 4 masks.**
  State the scope plainly: **all 47 lie in Jean's-lineage families** — families
  1–2 *are* Jean's circuit and its siblings, and the family-3 anchor's seed chain
  runs through Jean's circuit (Section 9) — so what those 47 certify is the
  rigidity of *that* neighbourhood.
- **The 88 @ depth 6 closes an independent one.** Its k ≤ 3 shell is exhaustively
  empty too — all 1 540 k=2 and all 27 720 k=3 windows irreducible, re-run from
  this repository on 2026-07-29 with the archived decider, verdict logs in
  `evidence/campaign87_run_2026-07-28_got_88at6_fromscratch/certificates/` — and
  it is a from-scratch fourth family, at Jaccard ≤ 0.323 to every circuit in the
  47. All 8 993 known states of its basin are k=2 irreducible as well. So the
  "88 is locally rigid" evidence is no longer confined to one lineage. The
  **88 @ depth 5** has its k=2 shell closed (1 540 windows) and its k=3 shell
  **unswept**; this project's own **88 @ depth 7** is still **not** among the 47 —
  its exhaustive k ≤ 3 sweep was never run, and all it has is 9 exact k=4 windows
  and 8 SAT cone windows. Those two are the least-certified circuits here, and
  "all our 88s" remains a claim this evidence does not support.
- **Population sweeps.** 105 801 of the ≈ 139 878 known distinct 88-gate states
  are proven irreducible at k=2: 51 899 of families 1–2 (61.1 %, ordered
  most-distant-first, so the entire symmetric-difference ≥ 55 band is closed;
  33 090 remain, resumable) plus **all 53 902 of family 3 (100 %, closed)**. At
  k=3 the 19 most theorem-starved population states were closed exhaustively
  (526 680 decisions, all irreducible).
- **k=4** (remove 4, restore with ≤ 3), partial but prioritised and all
  irreducible: 32 685 of 367 290 windows on Jean's 88 (8.9 %, covering every
  all-diff quad and every structural window), 20 432 on the family-3 anchor
  (5.6 %), 9 on our 88 @ 7.
- **The 89 seeds.** All five have exhaustively empty k=2 shells (1 596 windows
  each); k=3 is exhaustive for the 89 @ 5 and 89 @ 6 (29 260 each).
- **Total: ≈ 165 M exact window decisions, zero timeouts, zero reducible
  windows.**

**Windowed SAT — evidence, not proof.** The same windows were also attacked with
a sound windowed Fuhs–Schneider–Kamp CNF encoding, solved by Kissat 4.0.4 in
killable child processes, with two soundness-proved symmetry-breaking layers
(SB-P, parent commutativity; SB-F, guarded lex on adjacent free slots). Clauses
are only added, so UNSAT cannot be manufactured, and planted-SAT self-tests
decoded to oracle-verified 88s at every stage; the symmetry breaking re-decided
the three slowest previous UNSATs 14–34× faster.

| anchor | windows | UNSAT | undecided | SAT | max-k UNSAT |
|---|---|---|---|---|---|
| Jean's 88 | 48 | 44 | 4 | 0 | k = 16 |
| our 88 @ 7 | 8 | 5 | 3 | 0 | k = 13 |
| family-3 anchor (88 @ 8) | 50 | 37 | 13 | 0 | k = 15 (all 28 windows with k ≤ 12 UNSAT) |
| family-3 representatives | 32 | 25 | 7 | 0 | — |

**0 SAT anywhere.** The caveat that must travel with these numbers: UNSAT here
is **relative to the encoding's fixed slot order** (broken kept masks pinned at
their original positions, free slots at the removed masks' positions). That is
strong evidence, not a completeness proof, and the fixed slot order is the
dominant remaining gap for the three families it covers. Undecided windows are
undecided, not UNSAT.

## 11. Symmetry and the family structure of the 88 plateau

**The symmetry.** Byte rotation ρ (order 4) commutes with MixColumns, so it acts
on value-sets: the 32 targets fall into 8 ρ-orbits of size 4, and a
ρ-equivariant circuit can be searched in *orbit space*, where a move adds or
removes a whole orbit at once. That collapses the search but costs size —
demanding full ρ-symmetry costs about +19 gates (best fully symmetric ≈ 108 =
27 orbits). The half-rotation ρ² is where the structure actually is:

- **The elite basin is 79–81 % ρ²-symmetric**, and its 12 ρ²-fixed masks are
  exactly the classic (x0^x2)/(x1^x3) sharing trick — rediscovered by the
  search, not imposed. Jean's 88 is 75 % ρ²-symmetric (66 of 88) and
  symmetrizes-and-peels to 95: a *second*, distinct symmetric basin.
- A ρ²-equivariant orbit engine (~90–120 walk it/s, against ~5 for the naive
  orbit search) produced **two exactly ρ²-symmetric 90-gate circuits** (depth 9
  and depth 7, Jaccard 0.463 apart) — the best exactly symmetric circuits known
  here, the previous best being 94. Both are **derived from published work** in
  the sense above: basin 1 (depth 9) unions a 91 of our own lineage with a 92
  symmetrized from Jean's published 88, and basin 2 crosses that same 90 with
  another 91 of ours. Both are machine-certified locally optimal in orbit space:
  every remove-1-orbit move and all 666 remove-2-orbits-add-≤1 moves fail. These
  basins are extremely rigid; further progress came from *union crossings*, not
  local moves.
- Symmetry is also a seeding device. The ρ²-symmetric 94 @ 5 (41 size-2 orbits +
  12 fixed masks, 82 masks shared with our 89 @ 5) costs only +5 over the record
  and is the seed from which the 88 @ 7 was found — 32.9 minutes into that
  worker in the archived run.

**The families.** Two circuits count as the same family when their mask sets
have Jaccard ≥ 0.7. On that threshold there are **four** known 88-gate
families, all mutually far apart:

| pair | shared masks | Jaccard |
|---|---|---|
| Jean's 88 ↔ our 88 @ 7 | 61 / 88 | 0.530 |
| Jean's 88 ↔ our 88 @ 8 | 55 | 0.455 |
| our 88 @ 7 ↔ our 88 @ 8 | 62 | 0.544 |
| **our 88 @ 6 ↔ Jean's 88** | **42** | **0.313** |
| **our 88 @ 6 ↔ our 88 @ 7** | **43** | **0.323** |
| **our 88 @ 6 ↔ our 88 @ 8** | **42** | **0.313** |
| *baseline*: Jean's 88 ↔ Sun–Yang–Li's 89 | *63* | *0.553* |

The fourth family — the from-scratch 88 @ depth 6 — is far outside the range the
first three span: **0.313–0.323** to all of them, and **0.098–0.109** on the
periphery alone. That second figure is the informative one: every valid circuit
contains the same 32 target masks, so full Jaccard has a floor near 0.22 for two
88s that share nothing else, and on the 56 masks this circuit actually chose it
agrees with the other families on about a tenth. Nor is it a relabelling: over
all four byte rotations ρ^k of every *other* 88- and 89-gate circuit this project
holds or has transcribed — including the superseded 89 @ depth 10 — the largest
Jaccard it reaches is 0.362 (and 0.153 on the periphery).

The 0.7 cutoff is a working threshold, not a derived one, and it is now known to
be load-bearing in one place. For the 88-gate families it is not: the largest
inter-family overlap measured is 0.544, so any cutoff in 0.6–0.7 assigns the four
families identically. But **the derived 88 @ depth 5 sits at 0.735 to this
project's record 89 @ depth 5** (75 shared masks; 0.614 on the periphery) — above
the threshold, and closer to that 89 than to any 88 (best 0.615). It is therefore
reported as *the record-89 basin reached at 88 gates*, not as a fifth family, and
a cutoff moved even slightly upward would flip that call. Any statement of the
form "these are the *only* families" is a statement about what has been
searched, not about the problem.

The Sun–Yang–Li row is the baseline the 61/88 figure needs. Jean (ePrint
2026/1481) and Sun–Yang–Li (ePrint 2025/1493) are two indisputably independent
published works, and they share **more** masks with each other (63, J = 0.553)
than our 88 @ 7 shares with Jean's (61, J = 0.530). At this problem size a
60-mask overlap is what independence looks like, not evidence against it.

Around the first three anchors, harvesting mapped a population of **≈ 139 878
distinct 88-gate mask sets** (84 989 from the first hunt, 54 889 new from the
second). Of the 54 889: 53 902 in the third family, 987 in the frontier family,
and 0 unaffiliated — **that population contained no fourth family**. The fourth
family did not come from it: it came from a from-scratch worker starting nowhere
near any of them, which is the finding. Its own basin is large and uniformly
shallow — 8 993 distinct 88-gate states at J > 0.7 to it, **4 420 of them
realizable at depth 6**, none deeper than 7, all k=2 irreducible. Four structural
findings shape where to look next:

- **The universal core is almost empty.** Across all known ≤ 91-gate circuits
  the intersection is the 32 targets plus a single mask, and the known 89s share
  only ten non-target masks between them. Nearly everything outside that core is
  basin-specific, so the −1 has far more freedom than any one lineage explores —
  the argument for many independent basins over one deep descent.
- **Sharing across output cones is essential and already near-total.** The best
  standalone cone for one output byte is 33 gates, so four independent cones
  would cost ≥ ~132; the 89 shares 57 of its 89 gates between byte cones. There
  is no disjoint 4-column decomposition to exploit — the 32 targets are a single
  column map and every target touches all four input bytes.
- **Distance alone is not a direction.** A remote 89-cluster of over 107 000
  distinct states sits at maximum Jaccard 0.331 to all of the first three 88
  families, and three hours of LNS punching at it produced no 88.
- **Different basins hit the depth wall on different rows.** The masks whose
  minimum build depth equals the circuit depth — the obstruction to going one
  level shallower — are, for our 88 @ depth 7, output rows **3 and 27**; for the
  88 @ depth 6 they are rows **1, 11, 17 and 25**, four weight-7 targets. There
  is no single structural bottleneck at 88 gates: the depth-6 point was not
  reachable by pushing harder on the old plateau, it needed a different basin.
  (Both figures recompute from `pipeline/engines.py:relax`.)

## 12. Reproducing the records

`reproduce/README.md` is the authority on commands, configurations and runtimes.
Which mechanism produces which record:

- **97 @ depth 3**: `reproduce/reproduce.py` — single command, single core,
  from scratch, minutes.
- **92 @ depth 4**: `pipeline/` with `MODE="cascade"` — the from-scratch ladder.
- **89 @ depth 5**: `pipeline/` with `MODE="fixed"`, worker set `sub89` — the
  two-worker configuration of the run that found it, warm-started from the
  shipped 89 @ depth 6 and 90 @ depth 5 circuits.
- **The four 88s**: all came out of uncapped `alt` workers (walk + LNS chunks)
  with harvesting on, and every one of them was first seen one to three levels
  deeper and carried down by the Pareto depth tie-break within seconds. Two were
  seeded from ρ²-symmetric circuits — the 88 @ 7 from the ρ²-symmetric 94, the
  88 @ 8 from the ρ²-symmetric 90 basin 1 — and both seeds ship in
  `pipeline/seeds/`; the `hunt87` worker set continues that hunt. The **88 @ 6**
  had no seed at all: it came from `constructors.build("naive", 2163)` on restart
  18 of one worker of a multi-day fleet, and only its run archive reproduces it.
  The **88 @ 5** deliberately ships no reproduction command — its seed chain runs
  through published work (Section 9). These are stochastic multi-worker searches:
  what they took is recorded in `evidence/campaign87_run_*/` — exact code, config,
  logs and every verified best — not promised.

`reproduce/reproduce.py` also carries opt-in legacy demonstrations of the
individual moves on superseded records, with seed provenance stated per method.
`pipeline/README.md` documents how the code evolved between record runs.

## 13. History

The search programs were originally written and executed by LLM coding agents,
used as programming tools under the author's direction; the moves and acceptance
rules of Sections 3–4 were designed by the author. The method was then
reimplemented as the dependency-free Python in this repository, which reproduces
97 @ 3, 92 @ 4 and 89 @ 5 with no AI in the loop — that is the claim the opening
of this document makes, and it does **not** extend to any of the four 88s, which
the campaigns below *found*. That includes the two newest, and the own-lineage
frontier's depth-6 point among them: **88 @ 6 and 88 @ 5 were found on
2026-07-28 and 2026-07-29 by the third chapter's fleet, not by the 24-agent
campaign**, and the AI involvement is the same in kind for them as for the
older results. Every circuit ever claimed — here
or in the artifact repository, whatever produced it — is machine-verified
against MixColumns rebuilt from GF(2⁸).

The kernel, the operator set, the certificates and the symmetry analysis in this
document come from a second chapter: over **2026-07-26/27** a 24-agent campaign,
again directed by the author, was pointed at the method itself rather than at
the circuits. It profiled and rewrote the kernel, replaced sampled repair with
the exact enumeration of Section 4, added the destroy operators, acceptance
schedule and harvesting of Section 6, killed several move classes on measurement
(Section 8), built the decision procedures of Section 10, and found the 88 @
depth 7 and the 88 @ depth 8.

A third chapter, from **2026-07-27** onward, ran the same engine as a multi-day
fleet instead of a wave of agents: sixteen processes — fifteen search workers
plus one detector deciding the k=2 shell of every unseen harvested 88. The fifteen
were four from-scratch cascades on four different root constructors, repelled
hunters seeded from diverse 89s, two ρ²-equivariant orbit ladders and a
desymmetrising polish worker downstream of them, a free control on the project's
own 88 anchors, hunters on the fourth family's basin once it existed, and three
MAP-Elites novelty explorers over a structural archive — all aimed at 87. It has
not found one. What it did find is that starting *nowhere near* a known circuit is
what produces new structure: the from-scratch cascade `c_naive` opened the fourth
family and with it the 88 @ depth 6, while the orbit-ladder lane produced the
**derived** 88 @ depth 5.

The raw archives of both are not included in this repository (2.8 GB and ~900 MB
of harvest respectively); the curated results — all four 88s, an untouched run
archive with its code for each, the certificate summaries, the ρ²-symmetric
circuits and the credited imported prior art — are in `evidence/campaign87_*`.
The shipped `pipeline/engines.py` is the merged engine of the second chapter with
`run_engine(...)` unchanged, so it drops in for the code that produced the earlier
records; the fleet's copy adds only harvest bookkeeping and an off-by-default
repulsion knob on top of it.
