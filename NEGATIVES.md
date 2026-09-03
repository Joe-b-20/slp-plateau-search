# What has already been tried

Every negative result this project holds, in one table, with the thing each
one does **not** show written next to it. `negatives.jsonl` is the same
content, one JSON object per line, for anyone who would rather filter it
than read it.

The point of this file is to save you time. If you are considering an
attack on the 87-gate question, look here first: the odds are it is already
in the table, and if it is, the `does_not_imply` field tells you where the
previous attempt stopped being informative - which is usually the more
useful half.

## The three strengths

Every row carries exactly one, and they are not interchangeable.

- `theorem` - proved, unconditional within its stated hypothesis
- `exhaustive` - every case in a stated finite population was decided
- `searched` - looked and did not find; coverage stated, not complete

A `searched` row is not weak evidence for the same claim a `theorem` row
makes; it is evidence about a different and much smaller claim. The
distinction is the whole reason this file exists.

## Read the `does_not_imply` column

It is mandatory on every row and it is not boilerplate. Several of these
results are exhaustive over populations in the hundreds of millions and
still carry almost no information about whether an 87-gate circuit exists,
for reasons stated in the row. That assessment is this project's own, from
its own audit of its own work - see the last row.

## Artifact paths — and the `shipped` flag

**Every row is marked shipped or not shipped, and the machine-readable
`negatives.jsonl` carries the same mark as a boolean `shipped` field.** Honest
beats pretty: most of this project's evidence is too large to host.

- **`shipped: true`** (7 of 25 rows) — the artifact is a path *in this
  repository*. Open it now. The row's `artifact` field lists those paths, and
  every one of them was checked to be a tracked file at build time.
- **`shipped: false`** (18 of 25 rows) — the artifact is held in the project's
  working tree, which is much larger than this repository and is not published
  wholesale. For these rows `artifact` is a **plain-English description** of
  what is held, in the form `not-shipped: <what it is>; available on request
  (INVENTORY.md)` — not a path, because a path you cannot open is worse than a
  sentence you can read. `INVENTORY.md` says what is held, how big it is, and
  how to ask for it.

Below, each row's artifact line is prefixed **(shipped)** or **(not shipped)**.
For the not-shipped rows the historical working-tree path is given after the
description as an internal citation: directory names there are historical and
mean nothing, and the file at the end of the path is the evidence.

## The table

| # | claim | strength | scope |
|---|---|---|---|
| 1 | Every XOR circuit computing AES MixColumns uses at least 56 two-input XOR gates. | `theorem` | Unconditional. All straight-line XOR programs over GF(2) computing the 32x32 MixColumns matrix, any depth, any... |
| 2 | A circuit in which no gate's two inputs share a term - so no bit is ever computed and then cancelled - needs at least 92 gates. The best such circuit ... | `theorem` | Unconditional over cancellation-free straight-line programs for this matrix. Solver-free certificate. |
| 3 | Any MixColumns circuit of depth 3 or less needs at least 80 gates. | `theorem` | All depth-<=3 circuits. An exact rational LP dual over a 72,830 x 29,180 system, refereed. |
| 4 | In any valid circuit for a q-output map, the number of gates that are not outputs and do feed something is at most n - q, and any smaller value hands ... | `theorem` | Theorem is unconditional. The record: 28,796 circuits carrying a build order fully checked; 1,575,516 distinct... |
| 5 | Take any known 88-gate circuit, delete any one of its 56 working gates, and rebuild the wiring from scratch however you like: the remaining set of val... | `exhaustive` | 88,228,896 deletions = 1,575,516 mask sets x 56 working gates. 35,323,820 survived the local filter; 0 were re... |
| 6 | No two-gate rewrite improves any known 88: delete any two gates and resynthesise the hole optimally, and you never get below 88. | `exhaustive` | 139,878 of 139,878 mask sets, 1,540 windows each = 215,412,120 exact window decisions, logged in three disjoin... |
| 7 | No three-gate rewrite improves any known 88 either. The queue is empty, not partial. | `exhaustive` | 200 circuits x 27,720 triples, every one decided. |
| 8 | A partial four-gate sweep on three circuits found nothing. | `searched` | 56,489 / 39,034 / 34,599 windows out of 367,290 each - 15.4%, 10.6% and 9.4% coverage. |
| 9 | Across 22 circuits, no single shared helper value rewrites any window to a smaller circuit, and no helper is shared between them. | `exhaustive` | 15,099,957 one-helper rewrite windows, ledger-exact. |
| 10 | No four of the 32 output rows can be rebuilt more cheaply than the record circuit builds them. | `exhaustive` | All 35,960 four-row subsets refuted at one gate below cost for the depth-5 record; all 35,960 screened on a se... |
| 11 | Starting from thirteen 88-gate circuits and applying every gate-count-preserving rewiring and re-association move until the orbit closes, you reach 37... | `exhaustive` | 44,793 states across 5 wiring orbits plus 333,396 across 8 further orbits; 4,856,598 re-association sites with... |
| 12 | At every site in the corpus where deleting a pair of gates could have produced an 87, the replacement it would need provably does not exist. | `exhaustive` | 55,970 candidate sites across 18,355 circuits need a 3-gate replacement: 0 have one. 1,409 need a 4-gate repla... |
| 13 | No 87 within remove-two-add-one of 33,010 circuits, none within remove-three-add-one of 64 89-gate circuits, none within one operand edit of 6,832,408... | `exhaustive` | As stated. The alarms distribute 89: 12,704, 90: 30,856, 91: 16, 92: 673. |
| 14 | The two largest sub-blocks of every known 88, built jointly rather than separately, provably cost 15 gates - exactly what they cost apart. Merging the... | `exhaustive` | Sizes 9 through 14 all exhaustively UNSAT for the merged block: dimension 16, 8 targets, at one decomposition ... |
| 15 | The one remaining undecided sub-block whose cost of 12 would have priced its whole class at 87 costs 13. | `exhaustive` | One block. Size 12 proved UNSAT, with an inherited upper bound of 13. |
| 16 | Pricing the circuit exhaustively over every way of budgeting its shared sub-expressions - 1.41e26 configurations - never returns less than 87. | `exhaustive` | All menu configurations; 9 of the 10 component bounds are exactly tight. |
| 17 | 749,150 exact optimisation runs over restricted alphabets all returned OPTIMAL, and the best floor found anywhere among them is 88. | `exhaustive` | 749,150 solved to optimality, 125 timeouts. |
| 18 | Every dimension-8 block cell in the decomposition is proved exactly optimal, each with a positive control that fires. | `exhaustive` | 82 of 82 cells with optimum_proved true; four further dimension-12 regions decided at their split total. |
| 19 | A gate feeding eight later gates - the one wiring freedom anyone nominated as slack - is not achievable by ANY build order of the record 88s, even tho... | `exhaustive` | 39 mask sets: six record 88s plus 33 further floors. All 39 exact, 0 timeouts, every solve optimal. |
| 20 | Across 1,925,065 verified 88-gate circuits and 107,803,640 non-output gate slots, only 1,778 distinct intermediate values ever appear - and yet a veri... | `exhaustive` | Census exhaustive over 1,925,065 rows, 0 rejected. The counterexample is one circuit, found by search. |
| 21 | A proposed lower-bound route based on a linear invariant was closed by one hand computation: a verified greedy witness caps the bound the route could ... | `theorem` | The whole route family. |
| 22 | Nine named lower-bound proof families are provably incapable of reaching 88 for this matrix, each with an exact computed ceiling: 46.2, 51, 26, 36-40,... | `theorem` | Each ceiling is proved for its own family; together they cover every unconditional technique tried here. |
| 23 | The linear-programming certificate family that produced the 56 bound cannot be pushed past 91.41 for this matrix; its optimum is 91.409884, below both... | `theorem` | The certificate LP family, exactly. |
| 24 | This project audited its own negative results and found most of them near information-free about the question they were run to answer. | `searched` | The audit covers the local-search negatives above: bounded-radius irreducibility, the move-class walls, the or... |
| 25 | An 88-gate circuit you already have cannot be made shallower by rescheduling it. The wiring of an 88 is forced by its mask set, and every circuit ship... | `exhaustive` | Exhaustive and exact where it counts. (i) The ASAP least-fixpoint schedule - the shallowest schedule ANY circu... |
## The rows in full

### 1. lb-56

**Claim.** Every XOR circuit computing AES MixColumns uses at least 56 two-input XOR gates.

**Strength.** **theorem** - proved, unconditional within its stated hypothesis

**Scope.** Unconditional. All straight-line XOR programs over GF(2) computing the 32x32 MixColumns matrix, any depth, any fan-out.

**Cost.** Pen and paper; refereed in-repo.

**Artifact (shipped).** `bounds/gte56/STATEMENT.md`, `bounds/gte56/cert56.json`, `bounds/gte56/check_gte56.py`, `bounds/gte56/mine.c`

**What it does NOT imply.** It is 32 gates below the best circuit anyone has. The statement it supports is 56 <= L(M) <= 88, and the gap is 32 gates. Nothing in this repository narrows it.

### 2. lb-92-cancellation-free

**Claim.** A circuit in which no gate's two inputs share a term - so no bit is ever computed and then cancelled - needs at least 92 gates. The best such circuit known has 102.

**Strength.** **theorem** - proved, unconditional within its stated hypothesis

**Scope.** Unconditional over cancellation-free straight-line programs for this matrix. Solver-free certificate.

**Cost.** Solver-free.

**Artifact (shipped).** `bounds/cf_gte92/STATEMENT.md`, `bounds/cf_gte92/cert_cf92.json`, `bounds/cf_gte92/cert_cf92_sharper.json`, `bounds/cf_gte92/cf_102gates_depth5.json`

**What it does NOT imply.** It bounds nothing about circuits that DO cancel, and every record circuit here cancels. It only reframes the question as 'how much does cancellation buy?' - the records answer 'at least 4'; an 87 would answer 'at least 5'. It is not a lower bound on L(M).

### 3. lb-80-depth3

**Claim.** Any MixColumns circuit of depth 3 or less needs at least 80 gates.

**Strength.** **theorem** - proved, unconditional within its stated hypothesis

**Scope.** All depth-<=3 circuits. An exact rational LP dual over a 72,830 x 29,180 system, refereed.

**Cost.** Not separately priced.

**Artifact (shipped).** `bounds/depth3_gte81/STATEMENT.md`, `bounds/depth3_gte81/cert_depth3.json`, `bounds/depth3_gte81/mip3_result_L1.json`, `bounds/depth3_gte81/mip3_L1_run.log`

**What it does NOT imply.** 80 < 87, so this does NOT exclude a depth-3 87-gate circuit. The technique's own ceiling on this problem is estimated at 66-70, so strengthening it to 88 is a route that has been closed, not a route that is open.

### 4. tripwire-b-never-fired

**Claim.** In any valid circuit for a q-output map, the number of gates that are not outputs and do feed something is at most n - q, and any smaller value hands you an (n-1)-gate circuit by deleting one gate. For 88-gate MixColumns circuits that number is 56, and across every circuit ever tested here it has been 56, with no exception.

**Strength.** **theorem** - proved, unconditional within its stated hypothesis

**Scope.** Theorem is unconditional. The record: 28,796 circuits carrying a build order fully checked; 1,575,516 distinct mask sets checked for the distinctness and target conditions.

**Cost.** Seconds per circuit.

**Reproduce.**

```
python3 tools/tripwire.py <your_circuit.json>
```

**Artifact (not shipped).** The sweep ledger recording the tripwire's verdict on each of the 28,796 circuits with a build order and each of the 1,575,516 distinct mask sets, plus the sweep driver that produced it; the instrument itself ships as tools/tripwire.py (with tools/HOW.md) and the 520-record stratified draw as corpus/sample/, so the check is runnable here on any circuit - only the population is not. Available on request — see `INVENTORY.md`. Working-tree citation: `wrapup/CORPUS88.md`, `experiments/e15_campaign3/tools/sweep.py`, `experiments/e15_campaign3/AUDIT.md`

**What it does NOT imply.** The arrow only runs one way. B != n-q gives you a deletion; a clean B does NOT mean no gate is deletable - two gates duplicating a non-target value both count as working, so B stays clean while a gate is still deletable (tripwire.py demonstrates exactly this case). And the identity holds at every n, so a silent tripwire on 88-gate circuits says nothing whatever about whether an 87 exists.

### 5. no-87-one-deletion

**Claim.** Take any known 88-gate circuit, delete any one of its 56 working gates, and rebuild the wiring from scratch however you like: the remaining set of values cannot be built at all. No 87 is one deletion away from anything we have.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** 88,228,896 deletions = 1,575,516 mask sets x 56 working gates. 35,323,820 survived the local filter; 0 were realisable. Plus 35 overlapping-87 pairs, 0 realisable. 100% of the index.

**Cost.** 612.9 s CPU in the C kernel plus 1,457.9 s streaming; 2,571 mask sets/s on one nice -19 thread.

**Reproduce.**

```
cd corpus/deletion_certificate
gcc -O2 -o tools/delcert tools/delcert.c
nice -n 19 tools/delcert --bin ../sample/corpus88_sample.bin --targets targets.txt --k 88 --tag sample --every 0
nice -n 19 python3 tools/aggregate.py   # re-derives the full-corpus verdict from banked/
```

**Artifact (shipped).** `corpus/deletion_certificate/CERT.md`, `corpus/deletion_certificate/banked/RESULT.json`, `corpus/deletion_certificate/tools/delcert.c`, `corpus/sample/corpus88_sample.jsonl`

**What it does NOT imply.** Radius 1. The measured distance from one of these circuits to a genuinely different optimum is a median of 42 values, and 44 of 45 measured cases need at least 8 changes. A radius-1 result is therefore about 1/42 of the way to the object it would have to exclude.

### 6. irreducible-radius-2

**Claim.** No two-gate rewrite improves any known 88: delete any two gates and resynthesise the hole optimally, and you never get below 88.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** 139,878 of 139,878 mask sets, 1,540 windows each = 215,412,120 exact window decisions, logged in three disjoint append-only ledgers.

**Cost.** Not separately priced; the ledgers carry per-window time.

**Artifact (not shipped).** The two-gate window ledgers - 139,878 mask sets x 1,540 windows, logged in three disjoint shards with their reconciliation. Available on request — see `INVENTORY.md`. Working-tree citation: `wrapup/CONFLICTS_RESOLVED.md`

**What it does NOT imply.** This is the single clearest example of a negative that looks strong and is not. The same exact decider returns 'irreducible' about 97-, 94-, 92-, 91-, 90- and 89-gate circuits too, so its verdict discriminates 88 from 87 at a likelihood ratio of about 1.00. It is evidence that local search is exhausted, not evidence about L(M).

### 7. irreducible-radius-3

**Claim.** No three-gate rewrite improves any known 88 either. The queue is empty, not partial.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** 200 circuits x 27,720 triples, every one decided.

**Cost.** Not separately priced.

**Artifact (not shipped).** The three-gate window ledger - 200 circuits x 27,720 triples, every decision recorded. Available on request — see `INVENTORY.md`. Working-tree citation: `wrapup/CONFLICTS_RESOLVED.md`

**What it does NOT imply.** Same as radius 2, and the project's own guidance is not to fund more of it: negatives at radius <= 4 are worth close to nothing against a true distance of ~42.

### 8. radius-4-partial

**Claim.** A partial four-gate sweep on three circuits found nothing.

**Strength.** **searched** - looked and did not find; coverage stated, not complete

**Scope.** 56,489 / 39,034 / 34,599 windows out of 367,290 each - 15.4%, 10.6% and 9.4% coverage.

**Cost.** Not separately priced.

**Artifact (not shipped).** The partial four-gate sweep ledgers for the three circuits, with their per-circuit coverage counts. Available on request — see `INVENTORY.md`. Working-tree citation: `wrapup/CONFLICTS_RESOLVED.md`

**What it does NOT imply.** Under 16% coverage on three circuits. This is listed so that nobody quotes it as exhaustive; it is not, and the older figures for it circulating in this repository are stale.

### 9. one-helper-windows

**Claim.** Across 22 circuits, no single shared helper value rewrites any window to a smaller circuit, and no helper is shared between them.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** 15,099,957 one-helper rewrite windows, ledger-exact.

**Cost.** The unfinished remainder is priced at ~1,200 CPU-hours; the harder variant stands at 17 of 17,283 circuits even attempted.

**Artifact (not shipped).** The one-helper rewrite ledger - 15,099,957 windows over 22 circuits, decision-exact. Available on request — see `INVENTORY.md`. Working-tree citation: `wrapup/CONFLICTS_RESOLVED.md`

**What it does NOT imply.** 22 circuits, not the corpus. These window counts must never be added to the radius-2/3 counts - they overlap and are not one population. Two of the frames in this family are, by the project's own estimate, unclosable at any budget it had.

### 10. drop-4-outputs

**Claim.** No four of the 32 output rows can be rebuilt more cheaply than the record circuit builds them.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** All 35,960 four-row subsets refuted at one gate below cost for the depth-5 record; all 35,960 screened on a second, structurally different 88. Zero timeouts.

**Cost.** Not separately priced.

**Artifact (not shipped).** The drop-and-readd experiment's append-only ledger and its dated addendum. Available on request — see `INVENTORY.md`. Working-tree citation: `experiments/e5_readd/ledger.jsonl`, `experiments/e5_readd/ADDENDUM_20260829.md`

**What it does NOT imply.** 'Refuted' is banked only for the first circuit. On the second, the correct word is 'screened': 15 subsets cost 0 and 430 cost 1, which makes 'refuted at cost-1' vacuous or ill-posed for those. Four output rows out of 32 is also a small window.

### 11. neutral-orbits-closed

**Claim.** Starting from thirteen 88-gate circuits and applying every gate-count-preserving rewiring and re-association move until the orbit closes, you reach 378,189 circuits and never once drop below 88 gates.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** 44,793 states across 5 wiring orbits plus 333,396 across 8 further orbits; 4,856,598 re-association sites with 0 collisions; 436,914 re-parent probes. Separately 186,381 states under remove-one-add-one.

**Cost.** Not separately priced.

**Artifact (not shipped).** The neutral-orbit enumeration result and the gauge-equivalence module it ran on. Available on request — see `INVENTORY.md`. Working-tree citation: `experiments/e16_lastwish/laneFPOINT/RESULT.md`, `beat88/methods/shared/gauge.py`

**What it does NOT imply.** Both move sets preserve gate count and start from known 88s, so an 87 not reachable from a known 88 by these moves is outside these objects BY CONSTRUCTION - the closure constrains it not at all. And 90.1% of the 88s on disk were measured to be far from every circuit studied this way. The two headline counts are also not measurements of the same thing and must not be compared.

### 12. two-consumer-site-rebuild

**Claim.** At every site in the corpus where deleting a pair of gates could have produced an 87, the replacement it would need provably does not exist.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** 55,970 candidate sites across 18,355 circuits need a 3-gate replacement: 0 have one. 1,409 need a 4-gate replacement: all 1,409 decided negative. Positive controls: 8,000/8,000 planted 3-gate programs found, 400/400 4-gate.

**Cost.** 1,686 s for the 3-gate half.

**Artifact (not shipped).** The two-consumer site-rebuild result write-up, including the correction that dissolved the anomaly which motivated it. Available on request — see `INVENTORY.md`. Working-tree citation: `experiments/e16_lastwish/lane536/RESULT.md`

**What it does NOT imply.** The structural anomaly that motivated this whole lane turned out to be an artifact: the count that looked significant was one set of sites counted twice, and the headline was forced by an identity and could not have come out any other way. The computations above survive; the story around them does not, and a related anomaly from the same lane is closed as circular with a standing instruction not to cite it.

### 13. move-class-walls

**Claim.** No 87 within remove-two-add-one of 33,010 circuits, none within remove-three-add-one of 64 89-gate circuits, none within one operand edit of 6,832,408 circuits, and not one of 44,249 solver alarm files is below 89 gates.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** As stated. The alarms distribute 89: 12,704, 90: 30,856, 91: 16, 92: 673.

**Cost.** Not separately priced.

**Artifact (not shipped).** The move-class oracle's ledger and the inverse-move landscape analysis. Available on request — see `INVENTORY.md`. Working-tree citation: `beat88/methods/m2_oracle/LEDGER.md`, `beat88/methods/m4_inverse/analysis/landscape.md`

**What it does NOT imply.** Every one of these is a bounded-radius negative around known 88s and inherits the same fence. Note also that this repository contains four files with '87gates' in the name; all four are deliberate tripwire fakes planted to test the alarm path, and none is a circuit.

### 14. merged-block-15

**Claim.** Under our block decomposition, the two largest sub-blocks of every known 88, built jointly rather than separately, provably cost 15 gates - exactly what they cost apart. Merging them buys nothing, so no 87 exists that has the same block structure as the known 88s read through that decomposition.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** Sizes 9 through 14 all exhaustively UNSAT for the merged block: dimension 16, 8 targets, at one decomposition cell. The decomposition is a choice of ours; whether every known 88 respects it was not verified, and there is no DRAT proof at k = 14 - the level rests on two complete solvers agreeing on one CNF.

**Cost.** 356,321 core-seconds (about 99 core-hours) for the last size alone, kissat 4.0.4, one monolithic solve; about 30 hours of solver time for the ladder below it.

**Reproduce.**

```
Hand encodings/cnf/k14_joint_W3U4.cnf to any SAT solver. SAT means an 87-gate
MixColumns circuit exists in that class; it came back UNSAT.
The cheap end of the ladder re-runs here:
cd encodings && python3 code/solve_dimacs.py cnf/k9_joint_W3U4.cnf
```

**Artifact (shipped).** `encodings/cnf/k14_joint_W3U4.cnf`, `encodings/STATEMENT.md`, `encodings/logs/BANKED_LOGS.md`, `encodings/logs/mono_14_kissat404.log`, `encodings/logs/mono_14_cadical300.log`, `encodings/positive_control/mixcolumns_88gates_depth7.json`

**What it does NOT imply.** Not a proof that no 87 exists - an 87 outside this decomposition is untouched. The decomposition all of this reasoning lives inside was chosen rather than measured off the circuits, whether every known 88 respects it was not verified, and the companion records repository ships a verified 91-gate depth-6 circuit whose gate 70 (line support {2,3,4,7}) fits no single block of it. There is no DRAT proof at k = 14. Partial cube-coverage fractions from this lane must not be quoted.

### 15. last-door-13

**Claim.** The one remaining undecided sub-block whose cost of 12 would have priced its whole class at 87 costs 13.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** One block. Size 12 proved UNSAT, with an inherited upper bound of 13.

**Cost.** 19,458 s for the deciding solve.

**Artifact (not shipped).** The last-door run's dated addendum and its raw solver output. Available on request — see `INVENTORY.md`. Working-tree citation: `fleet6/door/ADDENDUM_20260829.md`, `fleet6/door/logs/door.out`

**What it does NOT imply.** Class-conditional. It forecloses one branch of one pricing argument. It says nothing about an 87 outside that class.

### 16. menu-price-87

**Claim.** Pricing the circuit exhaustively over every way of budgeting its shared sub-expressions - 1.41e26 configurations - never returns less than 87.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** All menu configurations; 9 of the 10 component bounds are exactly tight.

**Cost.** About 33,000 s spent; the one open sub-problem is priced at a further ~150,000 s.

**Artifact (not shipped).** The menu-pricing bound and per-cell price files, plus the merge tally that combined them. Available on request — see `INVENTORY.md`. Working-tree citation: `fleet5/laneMENU/results/bound.json`, `fleet5/laneMENU/results/cellprice.json`, `fleet5/laneMERGE/results/FINAL_TALLY.txt`

**What it does NOT imply.** The bound is 87, not 88 - it does not by itself exclude an 87, and closing the last gate is an OPEN lead, not a result. The pricing is also class-conditional: it prices 88 within a modelled class that is not proved to contain an 87, and the class's load-bearing wiring assumption was measured on 22 circuits with one exception and never proved.

### 17. rc2-floors

**Claim.** 749,150 exact optimisation runs over restricted alphabets all returned OPTIMAL, and the best floor found anywhere among them is 88.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** 749,150 solved to optimality, 125 timeouts.

**Cost.** Not separately priced.

**Artifact (not shipped).** The RC2 union-SAT burn directory and the exploit run's ledger. Available on request — see `INVENTORY.md`. Working-tree citation: `campaign_87/wave5_2026-08-04/burn/union_sat`, `experiments/e3a_exploit/ledger.jsonl`

**What it does NOT imply.** Every one of these prices a restricted problem. The restriction is exactly the thing that would have to be wrong for an 87 to exist, so agreement among them is close to circular: the regularity is measured across 88-gate circuits, which is precisely the population that would look regular if an 87 lived elsewhere.

### 18. block-cells-optimal

**Claim.** Every dimension-8 block cell in the decomposition is proved exactly optimal, each with a positive control that fires.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** 82 of 82 cells with optimum_proved true; four further dimension-12 regions decided at their split total.

**Cost.** Six comparable regions remain, priced at 2,000-5,500 s each.

**Artifact (not shipped).** The block-cell enumeration counts and the push run's ledger and analysis note. Available on request — see `INVENTORY.md`. Working-tree citation: `fleet9/laneENUM/results/v2_counts.jsonl`, `experiments/e7_push/ledger.jsonl`, `experiments/e7_push/ATLAS_NOTE.md`

**What it does NOT imply.** Cell-conditional. This lane also had to correct an earlier claim from a different lane: 3 of 23 of that lane's negatives were vacuous, their controls having never fired.

### 19. fanout-8-unreachable

**Claim.** A gate feeding eight later gates - the one wiring freedom anyone nominated as slack - is not achievable by ANY build order of the record 88s, even though their value sets combinatorially permit it. The exact maximum at 88 gates is 3 to 5; the best seen anywhere is 6, at 92 gates.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** 39 mask sets: six record 88s plus 33 further floors. All 39 exact, 0 timeouts, every solve optimal.

**Cost.** About 5 minutes of one nice -19 core, against the ~50 core-hours a search campaign for the same question would have cost.

**Artifact (not shipped).** The fan-out CP-SAT model, its result file and the upstream run's write-up. Available on request — see `INVENTORY.md`. Working-tree citation: `experiments/e_upstream/RESULT.md`, `wrapup/day2/e_upstream/c4_fanout_cpsat.py`, `wrapup/day2/e_upstream/c4_fanout_cpsat.json`

**What it does NOT imply.** 39 mask sets, not the corpus; the widening run had completed 1 of 150 at the time of writing. And this is a fact about 88-gate value sets whose instance does not differ at 87 - it constrains what an 87 could look like only if the 87 shares those value sets, which is the assumption at issue.

### 20. vocabulary-not-forced

**Claim.** Across 1,925,065 verified 88-gate circuits and 107,803,640 non-output gate slots, only 1,778 distinct intermediate values ever appear - and yet a verified 89-gate circuit exists that is built around a value outside that list. The dictionary is a search artifact, not a law.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** Census exhaustive over 1,925,065 rows, 0 rejected. The counterexample is one circuit, found by search.

**Cost.** 805 s for the census on one nice -19 worker; 97.0 core-hours (measured, not estimated) for the search that produced the counterexample.

**Reproduce.**

```
python3 verify_circuit.py corpus/vocabulary/S89_out_of_vocabulary_89gates.json
python3 corpus/vocabulary/tools/oov_check.py corpus/vocabulary/vocab.json \
        corpus/vocabulary/S89_out_of_vocabulary_89gates.json
```

**Artifact (shipped).** `corpus/vocabulary/vocab.json`, `corpus/vocabulary/recensus_stats.json`, `corpus/vocabulary/S89_out_of_vocabulary_89gates.json`, `corpus/vocabulary/tools/oov_check.py`

**What it does NOT imply.** It lowers no bound on 87 by any fraction of a gate, and it is not evidence that an 87 exists: leaving the dictionary costs between 0 and 1 gate, and an 87 needs a gate BACK. No 88 outside the dictionary has ever been exhibited; the best this line ever reached was 89.

### 21. route-closed-linear-invariant

**Claim.** A proposed lower-bound route based on a linear invariant was closed by one hand computation: a verified greedy witness caps the bound the route could ever prove at about 53, against the 89 it would have had to decide.

**Strength.** **theorem** - proved, unconditional within its stated hypothesis

**Scope.** The whole route family.

**Cost.** One measurement. No solver time.

**Artifact (not shipped).** The leads ledger entry closing this route, with the invariant it turned on. Available on request — see `INVENTORY.md`. Working-tree citation: `wrapup/LEADS.md`

**What it does NOT imply.** Nothing beyond that route. The transferable lesson is the method: compute an upper bound on your prospective lower bound before building any machinery for it.

### 22. proof-family-ceilings

**Claim.** Nine named lower-bound proof families are provably incapable of reaching 88 for this matrix, each with an exact computed ceiling: 46.2, 51, 26, 36-40, 52, 33, 73/71/67, 83.000, and 91.41.

**Strength.** **theorem** - proved, unconditional within its stated hypothesis

**Scope.** Each ceiling is proved for its own family; together they cover every unconditional technique tried here.

**Cost.** Various; each is a small exact computation.

**Artifact (not shipped).** The consolidated state-of-the-problem write-up and the pure-proof dossier behind these ceilings. Available on request — see `INVENTORY.md`. Working-tree citation: `fleet7/laneCONSOLIDATE/STATE_OF_THE_PROBLEM.md`, `experiments/e17_pure/DOSSIER.md`, `fleet2/laneP_proof/RESULT.md`

**What it does NOT imply.** It does not say 88 is unprovable - it says these techniques cannot prove it. Every unconditional family here has a ceiling below 88 except one, and that one's ceiling is 83 on a circuit that exists.

### 23. certificate-lp-capped

**Claim.** The linear-programming certificate family that produced the 56 bound cannot be pushed past 91.41 for this matrix; its optimum is 91.409884, below both thresholds that would have made it worth upgrading.

**Strength.** **theorem** - proved, unconditional within its stated hypothesis

**Scope.** The certificate LP family, exactly.

**Cost.** Not separately priced.

**Artifact (not shipped).** The pure-proof dossier section recording the certificate LP's cap. Available on request — see `INVENTORY.md`. Working-tree citation: `experiments/e17_pure/DOSSIER.md`

**What it does NOT imply.** 91.41 is above 88, so the cap is not what kills the route - what kills it is that reaching the cap requires assumptions the family cannot certify. Do not read '91.41' as a lower bound of any kind.

### 24. own-audit-repriced-negatives

**Claim.** This project audited its own negative results and found most of them near information-free about the question they were run to answer.

**Strength.** **searched** - looked and did not find; coverage stated, not complete

**Scope.** The audit covers the local-search negatives above: bounded-radius irreducibility, the move-class walls, the orbit closures.

**Cost.** The audit itself is cheap; it is reading, not computing.

**Artifact (not shipped).** The consolidated state-of-the-problem write-up, the corrections ledger and the case write-up this repricing came out of. Available on request — see `INVENTORY.md`. Working-tree citation: `fleet7/laneCONSOLIDATE/STATE_OF_THE_PROBLEM.md`, `wrapup/CORRECTIONS.md`, `wrapup/CASE_FOR_88.md`

**What it does NOT imply.** It does not withdraw the computations - they ran, and their counts are correct. It withdraws the INFERENCE. Specific casualties: a structural backbone picture that turned out to be falsified; a rigidity headline that reported 1 escape where two sweeps find 99; a file count published as a population size where 135 files held 21 distinct circuits; a corpus called exhaustive that is 14% complete; and a list of published negatives whose controls never fired. Anyone mining this repository for 'X was ruled out' must read that list first.

### 25. depth-not-reschedulable

**Claim.** An 88-gate circuit you already have cannot be made shallower by rescheduling it. The wiring of an 88 is forced by its mask set, and every circuit shipped here already sits at the shallowest depth its own mask set admits - so depth is a property of the value set, not of the build order. Size-preserving moves that DO change the value set did not get there either: no transposed 88 ever came out shallower than its seed, and the 88 at depth 6's entire depth-<=6 plateau component contains no depth-5 circuit.

**Strength.** **exhaustive** - every case in a stated finite population was decided

**Scope.** Exhaustive and exact where it counts. (i) The ASAP least-fixpoint schedule - the shallowest schedule ANY circuit on a given mask set admits - computed for all 9 shipped circuits: measured depth equals ASAP depth in 9 of 9. (ii) The 88 at depth 6's depth-<=6 equal-size plateau component under remove-1 plus every valid single-mask repair, enumerated to closure: 5,427 states, frontier 0, all at depth 6, zero at depth 5. (iii) The wiring-forcedness measurement behind (i): 1,320/1,320 sampled gate slots had exactly one legal parent pair, census forced fraction 0.9986. The transposition result is a SEARCH, not exhaustive: 400 double-transposition round-trips from each of the 88s at depths 6, 7 and 8, reaching 727 distinct 88s, none shallower than its seed.

**Cost.** About one second for the ASAP check over all 9 circuits, stdlib only. 251 s on one nice -19 core for the 5,427-state plateau closure; a few minutes for the 1,200 transposition round-trips.

**Reproduce.**

```
python3 corpus/depth_forced/asap_depth.py
```

**Artifact (shipped).** `corpus/depth_forced/DEPTH_FORCED.md`, `corpus/depth_forced/asap_depth.py`, `corpus/depth_forced/HOW.md`

**What it does NOT imply.** It says NOTHING about whether more depth-5 pockets exist to be found directly - almost certainly they do. 92 of the 28,796 corpus 88s carrying a build order are already at depth 5 (0.32%), and only two of those pockets have been enumerated to closure (27 and 135 states). This row does not bound how many depth-5 88s there are, does not claim the known pockets are the only ones, and says nothing about whether a depth-4 88 exists. It rules out exactly one shortcut: taking an 88 you already have and rescheduling, transposing or depth-preservingly walking it to a lower depth. Finding a shallow 88 by searching for one directly is untouched by this row - it is how both depth-5 records were actually made.
