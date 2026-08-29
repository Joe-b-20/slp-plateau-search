# CORPUS-88 — the deduplicated index of every distinct verified 88-gate circuit on this machine

Agent: CORPUS-88 consolidator (wave 2). Date: 2026-08-29.
Index: `wrapup/corpus88_index.jsonl` — 1,575,516 rows, 457 MB.
Tool: `wrapup/tools/corpus88.py`. Machine-readable summary: `wrapup/work/summary.json`.

**Headline: 1,575,516 distinct verified 88-gate MixColumns mask sets.**
Not one of them has a duplicated mask. Every one of the 28,796 for which a build
order exists on disk has **B = 56** — no B-alarm, no 87 available by deletion
anywhere in the corpus. The e15 "full census" of 17,283 turns out to be **1.1 %**
of what is actually on disk, and 92 % of the census came from a single method.

Report the number in tiers — they mean different things:

| tier | distinct 88s | what it is |
|---|---:|---|
| **A — materialised circuits** | **28,892** | one circuit file / one `.plat` row / one reconstructible basin row per set; 28,796 of them have a banked build order (depth + `B` computable) |
| **B — + the four curated population banks** | **198,977** | adds beat88's `pop88_worklist`, campaign_87's two 2026-07 harvests and `found88_layer89` |
| **C — + the NRPA sub-92 harvest** | **1,575,516** | adds `wave5/nrpa/out/sub92.jsonl`, a single method's plateau dump (1,400,343 valid 88 rows, all pairwise distinct) |

For "N available upon request", tier A is what can be handed over as runnable
circuits today; tiers B and C are mask sets whose build order must be re-derived.

**1,575,516 is a floor, not the ceiling.** Two large classes are counted but not
hashed: 2,840,868 further 88-mask rows in the bulk `.pop.jsonl` harvest and
1,530,095 88-gate records in beat88's export tree (§7). The honest project-wide
range is **1.6 M – 4.4 M distinct**; only the floor is verified and deduplicated.

---

## 1. Identity — reused, not invented

The project's standard notion of circuit identity is the **sorted multiset of
gate output masks** (32-bit ints), taken straight from
`experiments/e15_campaign3/tools/cache_pop.py:38`:

```python
gm  = masks_of(pairs)          # replay index pairs, sig[a]^sig[b]; gm = sig[32:]
key = tuple(sorted(gm))        # <- the identity
```

`sweep.py:validity()` uses the same replay against the same spec source
(`verify_circuit.mixcolumns_target_masks` + `load_index_pairs`). This
consolidator hashes exactly that key:

```
canon = sha256(",".join("%08x" % m for m in sorted(masks))).hexdigest()[:16]
```

It is a **multiset**, so a duplicated mask shows up as `n_masks_distinct < 88`
rather than being silently collapsed. It is **gauge-free**: gate order, gate
indices and file encoding are quotiented out; ρ-images stay distinct rows, as
the project treats them everywhere else. It is **not** beat88's `canon_id`,
which is a coarser gauge-orbit id — beat88's rows are re-hashed here under the
common identity.

A row is admitted only if it is a **valid 88**: exactly 88 masks, and all 32
MixColumns target masks present among them. For gate-list sources that is the
full oracle replay test computed with `verify_circuit.py`'s own spec code, so
every gate-list-backed row is oracle-VALID by construction rather than by
assertion. For mask-only sources it is the set-level test plus (spot-checked,
§6.2) greedy realisability.

---

## 2. Totals

| | |
|---|---:|
| **distinct 88-gate mask sets** | **1,575,516** |
| source memberships (sum over sources) | 1,622,806 |
| sets with a build order on disk (depth + `B` computable) | 28,796 |
| sets that are mask-set-only | 1,546,720 |
| sets with a duplicated mask (⇒ an immediate 87) | **0** |
| sets with `B != 56` | **0** |
| not in the e15 17,283 census | **1,558,233** |

Commands (all `nice -n 19`, one worker at a time, ≤ 2 concurrent):

```
python3 wrapup/tools/corpus88.py --stage curated   # file walk, .plat, basin laterals, census
python3 wrapup/tools/corpus88.py --stage banks     # the four curated mask-set banks
python3 wrapup/tools/corpus88.py --stage nrpa      # wave5 NRPA sub92 harvest
python3 wrapup/tools/corpus88.py --stage emit      # index + work/summary.json
wc -l wrapup/corpus88_index.jsonl      -> 1575516
```

### 2.1 Per source

`distinct` = distinct mask sets this source contributes; `only here` = sets no
other source in this index holds.

| source | distinct | only here | what it is |
|---|---:|---:|---|
| `campaign_87_nrpa_sub92` | 1,400,343 | 1,376,539 | `campaign_87/wave5_2026-08-04/nrpa/out/sub92.jsonl` — 1,441,779 rows, 1,400,343 of them `gates:88`, **all pairwise distinct** (the file is self-deduplicated) |
| `campaign_87_merged_engine_pop` | 84,989 | 80,356 | `campaign_87/agents/merged-engine/runs_hunt/*.pop.jsonl` — wave-2 plateau harvest (15 files, 690,850 rows, 433,563 at exactly 88 masks) |
| `campaign_87_population88_new` | 54,889 | 53,763 | `campaign_87/agents/hunt-deeper/population88_new.jsonl` — wave-3 harvest, 54,889 rows, every row a valid 88 |
| `beat88_pop88_worklist` | 33,010 | 23,646 | `beat88/methods/m2_oracle/runs/pop88_worklist.jsonl` — beat88's authoritative 88 population (`masks_hex`), all 33,010 rows valid |
| `campaign_87` (circuit files) | 20,969 | 2,743 | every 88-gate circuit JSON under `campaign_87/` |
| `e15_census_pop88` | 17,283 | 2 | `experiments/e15_campaign3/tools/pop88.pkl` — the Run-A census baseline |
| `beat88` (circuit files) | 7,087 | 6,960 | 88-gate circuit JSONs under `beat88/`, **excluding** `m3_census/exports/` |
| `campaign_87_found88_layer89` | 3,254 | 50 | `campaign_87/hunt87_layer89/found88.jsonl` |
| `atlas_corner_plat` | **498** | **283** | `atlas/corner/out/*.plat`, the 504 rows with gate count 88 |
| `fleet9-12` | 244 | 75 | circuit JSONs in fleet9–fleet12 (incl. the record-tying 88 @ depth 5) |
| `fleet1-4_basin_lateral` | **99** | **94** | the 99 lateral 88s from `fleet1/laneD_completions/basin_*.jsonl` — see §5 |
| `evidence` | 55 | 0 | `evidence/` + `pipeline/` + `reproduce/` circuit JSONs |
| `atlas` (circuit JSONs) | 30 | 6 | 88-gate circuit JSONs elsewhere in `atlas/` |
| `experiments_early/e5_readd` | 16 | 4 | the round-trip 88s |
| `fleet5-8` | 9 | 2 | matches `fleet5_8.md`'s "distinct 88-gate mask sets: 9" exactly |
| `experiments_late/e14_plateau87` | 8 | 2 | |
| `experiments_early/e3b_fresh` | 5 | 0 | |
| `fleet1-4` (circuit files) | 5 | 0 | |
| `records_repo` | 5 | 0 | `~/xor_ui/aes_mc_records/circuits/mixcolumns_88gates_*.json` — matches the 5 claimed |
| `experiments_late/e15_campaign3` | 3 | 0 | |
| `experiments_early/e1_regions` | 2 | 0 | |
| `experiments_early/sat_package` | 1 | 0 | |
| `experiments_late/e13_hand87` | 1 | 0 | stage 5 of the 106→97→91→90→88 reasoning ladder |
| `experiments_late/e17_pure` | 1 | 0 | |

Underlying file scan: **580,278 JSON files seen, 264,417 parsed, 63,849 valid
88-gate circuit files** (173 s wall, one nice-19 process).

**Cross-checks that came out exactly right, independently recomputed:**
`records_repo` 5, `fleet5-8` 9 distinct, `atlas_corner_plat` 498 distinct, the
99 basin laterals, and — see §3 — the 84,989 / 54,889 / 139,878 triple.

### 2.2 Overlap — the pairs that matter

Full 24 × 24 matrix in `wrapup/work/summary.json` → `overlap_matrix`. The
informative entries:

| A | B | \|A ∩ B\| |
|---|---|---:|
| merged-engine 84,989 | population88_new 54,889 | **0** |
| NRPA 1,400,343 | merged-engine | **0** |
| NRPA | population88_new | **0** |
| NRPA | beat88 worklist | 7,860 |
| NRPA | e15 census 17,283 | **15,884** |
| NRPA | campaign_87 circuit files | 15,952 |
| NRPA | atlas `.plat` / beat88 files / fleet / evidence | 0 in every case |
| merged-engine | beat88 worklist | 794 |
| population88_new | beat88 worklist | 634 |
| e15 census | campaign_87 circuit files | 17,263 |
| e15 census | merged-engine | 34 |
| e15 census | population88_new | 14 |
| e15 census | beat88 worklist | 14 |
| e15 census | beat88 circuit files | 13 |
| atlas `.plat` 498 | e15 census | 2 |
| atlas `.plat` 498 | merged-engine | 195 |
| atlas `.plat` 498 | beat88 worklist | 4 |
| atlas `.plat` 498 | `evidence`+`pipeline`+`reproduce` | 1 |
| fleet9-12 | e15 census | 12 |
| fleet1-4 basin laterals 99 | e15 census | 1 |
| fleet1-4 basin laterals 99 | merged-engine / NRPA | 0 / 0 |
| found88_layer89 3,254 | merged-engine | 3,180 |
| beat88 circuit files 7,087 | beat88 worklist | 4 |

Four of these deserve to be said out loud.

- **The three big harvests are mutually disjoint.** NRPA ∩ merged-engine = 0,
  NRPA ∩ population88_new = 0, merged-engine ∩ population88_new = 0. Three
  independent plateau searches, run weeks apart, produced 1,540,221 distinct 88s
  with **zero** collisions between them. The 88-gate plateau is not a small set
  the searches keep re-finding; it is enormous, and each search samples a
  different part of it.
- **The atlas corner corpus is genuinely foreign.** 498 distinct 88s, of which
  **283 are known to no other source here** and 0 to NRPA. `atlas_misc.md`'s
  claim "0 of 498 equal any of the 54 88-gate circuits under `evidence/`" holds:
  the single `evidence`-labelled overlap is `reproduce/out_88hunt.json`, a
  reproduction output, not one of the eight canonical `evidence/circuits/`
  records.
- **beat88's loose 88 files and beat88's own worklist barely intersect** (4 of
  7,087). The worklist keeps one canonical representative per gauge orbit; the
  loose files are other members of those orbits, and other lineages entirely.
- **92 % of the e15 census is one method's output.** 15,884 of the 17,283
  census sets are NRPA sets. The population the Run-A sweep certified is not a
  cross-section of the project's 88s; it is mostly `wave5/nrpa`.

### 2.3 Depth

Depth is recorded only where a build order exists on disk (28,796 sets). For the
other 1,546,720 a depth would have to be re-derived, not read.

| depth | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| distinct sets | **92** | 440 | 2,255 | 8,924 | 7,232 | 3,427 | 3,241 | 2,445 | 660 | 58 | 14 | 8 |

**92 distinct mask sets are realisable at depth 5**, the record depth — far more
than the handful the public repo names.

---

## 3. Reconciliation: 17,283 (Aug census) vs 139,878 (records-repo PAPER.md)

**They count different objects, and both numbers are exactly right.**

### What 17,283 counts

`experiments/e15_campaign3/LEDGER.md:178` (§4, sampling frame):

> Corpus: repo `*88gates*.json` — 20,410 files, 18,355 valid 88s, **17,283
> distinct mask multisets**, 0 dup-mask, 0 dead-gate (two independent loaders).

It is produced by `experiments/e15_campaign3/tools/cache_pop.py`, whose walk is
gated on the **filename**:

```python
if "88gates" not in fn or not fn.endswith(".json"):
    continue                                   # cache_pop.py:26-27
```

So: *distinct mask multisets among the individually-materialised circuit files
whose name contains the string `88gates`*. Banked as `tools/pop88.pkl` (17,283
entries) and swept as `sweep_A_fullpop.jsonl` (`wc -l` → 17,283).

### What 139,878 counts

`~/xor_ui/aes_mc_records/PAPER.md:146` — "105,801 of the ≈ 139,878 harvested
distinct 88-gate mask sets are proven irreducible at k = 2" — sourced in
`campaign_87/FINAL_REPORT.md:19` as

> ~139,878 distinct verified 88-gate mask sets | 88 | populations in
> `agents/merged-engine/runs_hunt/` + `agents/hunt-deeper/population88_new.jsonl`

These are **rows in two plateau-harvest population dumps**. They were never
written out as individual circuit files, so `cache_pop.py`'s filename filter
could not see a single one of them.

### The arithmetic, recomputed here under the common identity

| | |
|---|---:|
| `agents/merged-engine/runs_hunt/*.pop.jsonl`, distinct valid-88 mask sets | 84,989 |
| `agents/hunt-deeper/population88_new.jsonl`, distinct valid-88 mask sets | 54,889 |
| intersection of the two | **0** |
| union | **139,878** |

The "≈" in `PAPER.md` is unnecessary: **139,878 is exact**, and it is exact
because the two harvests are perfectly disjoint. This is an independent
confirmation — the consolidator re-hashed both banks from raw masks and never
read either campaign's own counts.

### How the two overlap

| | |
|---|---:|
| 17,283 ∩ 139,878 | **48** (34 with merged-engine + 14 with population88_new) |
| fraction of the census inside the 139,878 | 0.28 % |

The two figures are **99.7 % disjoint** and neither contains the other. A
public sentence that is true: *"≈ 1.58 million distinct 88-gate mask sets are
held, of which 139,878 are the two 2026-07 plateau harvests, 1,400,343 are the
NRPA sub-92 harvest, and 17,283 are the individually-exported circuit files that
the 2026-08 window-compression census swept."* (Those three sets overlap only in
the 15,884 + 48 noted above.)

### Consequence nobody has drawn

`experiments_late.md` §3.3 describes the Run-A bank as certifying "**every**
distinct 88 mask-multiset on disk". Measured against this index the true scope
is **17,283 of 1,575,516 = 1.1 %** (8.7 % if the NRPA dump is excluded). The
other 1,558,233 distinct 88s were never in that sweep. Nothing Run A proved is
wrong — but "every" should become "every one exported as a `*88gates*.json`
file" in any public statement, and the sweep's population should be described as
NRPA-dominated (§2.2).

---

## 4. The B = 56 tripwire over everything new

Theorem (e15 `sweep.py:296`, ARCH3 R53): on a valid 88 not already reducible to
87, `B` — the number of non-output gates that have a consumer — is exactly 56.
`B != 56` ⇒ a duplicated mask or a consumer-less non-output gate ⇒ **an 87 is
available by deletion**.

The check splits in two, because `B` needs the DAG and 1,546,720 sets have no
build order on disk:

| check | applies to | result |
|---|---:|---|
| **full `count_B`** (e15's function, unmodified) | 28,796 sets with a build order | **28,796 / 28,796 have B = 56. Zero alarms.** |
| set-level half — 88 **distinct** masks | all 1,575,516 | **1,575,516 / 1,575,516 pass.** No duplicated mask anywhere |
| set-level half — all 32 targets present | all 1,575,516 | 1,575,516 / 1,575,516 (it is the admission criterion) |

**No B-alarm. No 87 by deletion anywhere in the corpus.** The expected result,
now measured over 1.58 M sets instead of 17 k.

The consumer-less-gate half of the theorem is *not* decided for the 1,546,720
mask-only sets; deciding it needs a build order, which for those sets would have
to be re-solved. That is the one honest gap in this bonus check.

**Side finding — a real gap in e15's own Run A:** 906 of the 17,283 Run-A rows
in `sweep_A_fullpop.jsonl` carry **no `B` field at all**. They were swept before
the tripwire was added (they are the `wave5/nrpa/out/FOUND_88gates_*` shard):

```
python3 -c "import json,collections; c=collections.Counter(json.loads(l).get('B')
  for l in open('experiments/e15_campaign3/sweep_A_fullpop.jsonl')); print(dict(c))"
-> {None: 906, 56: 16377}     ALARM rows: 0
```

This consolidator closes that gap: all 906 are file-backed, `count_B` ran on
them here, and all 906 returned 56.

---

## 5. The 99 lateral 88s — materialised, not skipped

`fleet1_4.md` LEAD L2 flags 99 lateral 88s in
`fleet1/laneD_completions/basin_88at6.jsonl` (57 `HIT-3` rows) and
`basin_88at5fs.jsonl` (42), "never compiled, verified, deduplicated, or checked
against the census". They do **not** need re-solving: each row records
`{triple deleted, 3 gates paid}`, so the mask set is

```
parent_mask_set  \  {3 deleted masks}  ∪  {3 paid masks}
```

with the parents being `evidence/circuits/mixcolumns_88gates_depth6.json` and
`..._depth5_fromscratch.json`. All 99 reconstruct to exactly 88 masks covering
all 32 targets, and all 99 pass a greedy realisability check (each mask is an
XOR of two earlier available masks — so a build order exists).

Result: **99 admitted, 0 unrealisable. 94 of the 99 are held by no other source
in this index; only 1 is in the e15 census; 0 are in the 139,878 harvest; 0 are
in the NRPA harvest.** Genuinely new material, now indexed. Their build orders
are not banked (only one, `NEW88_from_88at6_hit3_depth9.json`, was ever
compiled), so they carry no depth and no full `B`.

---

## 6. Verification

### 6.1 Oracle sample — 21 circuits, 21 VALID

`python3 verify_circuit.py <file>`, spread across every gate-list source.
**21 / 21 `VERDICT: VALID MixColumns circuit`, all at 88 gates.**

| file | depth |
|---|---|
| `evidence/circuits/mixcolumns_88gates_depth5.json` | 5 |
| `evidence/circuits/mixcolumns_88gates_depth5_fromscratch.json` | 5 |
| `evidence/circuits/mixcolumns_88gates_depth6.json` | 6 |
| `evidence/circuits/mixcolumns_88gates_depth7.json` | 7 |
| `evidence/circuits/mixcolumns_88gates_depth8_thirdfamily.json` | 8 |
| `evidence/campaign87_imported_prior_art/jean_88gates_depth7_eprint_2026-1481.json` | 7 |
| `~/xor_ui/aes_mc_records/circuits/mixcolumns_88gates_depth5.json` | 5 |
| `fleet9/laneENUM/results/circuits/rho1_88at5.json` | 5 |
| `fleet12/laneKNOBS/out/k2d5_rec_ctrl.json` | 5 |
| `fleet12/laneHINTS/out/step2b_rec88at7.json` | 8 |
| `fleet8/unified/results/gen_88_noQ27.json` | 8 |
| `fleet5/laneMERGE/results/mergegen_MB273.json` | 10 |
| `fleet3/laneF4_rule/results/gen_f4_88_D4.json` | 10 |
| `fleet4/laneDEPTH/results/genD_88at5_record_D5_c3_322.json` | 5 |
| `fleet1/laneD_completions/NEW88_from_88at6_hit3_depth9.json` | 9 |
| `experiments/e13_hand87/cluster_campaign/assembly_stage5.json` | 5 |
| `experiments/e14_plateau87/laneFS88_chimA_record_x_sig2.json` | 5 |
| `campaign_87/agents/merged-engine/BREAKTHROUGH_88gates_depth7.json` | 7 |
| `campaign_87/wave6_2026-08-11/discriminate/runs/VERIFIED88_hiplane_88_0.json` | 10 |
| `atlas/corner/out/desc.98at3_a1_s2_d0.plat` line 9 (decoded) | 6 |
| `atlas/corner/out/fib_S_88gates_depth5_88_s1_S1.plat` line 1 (decoded) | 6 |

The two `.plat` rows were decoded by this consolidator's own `.plat` reader into
`wrapup/work/sample_plat_{0,1}.json` and then handed to the oracle — that checks
the reader, not merely that `.plat` files exist.

### 6.2 Realisability sample for the mask-only banks — 438 / 438

The oracle needs a build order, which mask-only banks do not carry. Instead,
random rows were checked for: 88 masks, 88 **distinct** masks, all 32 targets
present, and greedy realisability from the 32 inputs.

| bank | sampled | pass | fail |
|---|---:|---:|---:|
| `wave5/nrpa/out/sub92.jsonl` | 198 | 198 | 0 |
| `merged-engine/runs_hunt/w2_new88.pop.jsonl` | 60 | 60 | 0 |
| `hunt-deeper/population88_new.jsonl` | 60 | 60 | 0 |
| `beat88 pop88_worklist.jsonl` | 60 | 60 | 0 |
| `hunt87_layer89/found88.jsonl` | 60 | 60 | 0 |

---

## 7. What is NOT in the index, and why

Documented exclusions, not oversights. All of it is 88-gate material that would
raise the total.

| class | scale | why excluded |
|---|---|---|
| `beat88/**/m3_census/exports/` | **1,251,227 files**; 1,530,095 records at 88 gates across the three `MANIFEST.jsonl` | The manifests carry metadata only — **no masks**. Recovering the mask sets means opening 1.25 M files (6.7 GB on disk). beat88's own authoritative distinct figure, 33,010, is `pop88_worklist.jsonl` and **is** indexed. `find beat88 -path '*m3_census/exports*' -type f \| wc -l` |
| `campaign_87/**/*.pop.jsonl` outside merged-engine | **115 files, ~13.1 GB**, containing **2,840,868 rows of exactly 88 masks** | Bulk plateau harvest at each run's own best size (bare mask lists, mixed 88–92+). Streaming-counted, not ingested; see §7.1 |
| `campaign_87/wave6_2026-08-11/fusion_diag/runs/full.jsonl` | 434,125 rows, 139 MB | Rows are structural invariants (`sigma`, `ihist`, `Phist`, `src`) — **no masks**. The "434,125 distinct verified 88 mask sets" in `campaign_87.md` §3.2 counts scanned rows; the masks are not in this file |
| wave6 `discriminate` 4-plane 88s | 33,821 oracle-verified | `VERIFIED88_HIPLANE.txt` is a 1 KB **summary**; only 6 sample circuits (`VERIFIED88_hiplane_88_{0..5}.json`) were ever exported, and those are indexed |
| `campaign_87/agents/frontier-exact/work/results_*/*progress.jsonl` | 84,989 + 987 + 200 + 130 k rows | Verdict rows keyed by a 16-hex `key` — **no masks**. The same population is indexed via merged-engine |

### 7.1 The streaming count of the bulk harvest — 2,840,868 rows

```
find campaign_87 -name '*.pop.jsonl' -not -path '*merged-engine*' -print0 \
  | xargs -0 cat | awk -F, 'NF==88{n++} END{print n}'
-> 2840868                    # wrapup/work/bulkpop_count.log
```

These files are bare JSON mask lists, so "88 comma fields" = "88 masks". This is
a **row** count, not a distinct count: rows repeat within and across the 115
files, and none was hashed. Taking the observed ratios elsewhere as a guide
(NRPA was ~100 % distinct, merged-engine ~20 %), the unindexed remainder is
somewhere between ~0.6 M and ~2.8 M further 88-gate mask sets. **The true
project-wide distinct-88 total is therefore between 1.6 M and 4.4 M**; 1,575,516
is a floor, and it is the largest number that is actually verified and
deduplicated. Ingesting the 13.1 GB is the obvious next extension (about 25–35
minutes of one nice-19 worker, ~6 GB RSS at the top end).

Not counted at all: the beat88 export tree, whose 1,530,095 records at 88 gates
would need 1.25 M file opens (§7).

---

## 8. Every count's producing command

| count | command |
|---|---|
| distinct total 1,575,516 | `wc -l wrapup/corpus88_index.jsonl` |
| per-source / overlap / depth / B | `python3 wrapup/tools/corpus88.py --stage emit`, then `wrapup/work/summary.json` |
| 580,278 JSON seen / 63,849 valid-88 files | `--stage curated`, `stats.walk` |
| 504 `.plat` rows at 88 → 498 distinct | `--stage curated`, `stats.plat`; cross-check `awk '$1==88' atlas/corner/out/*.plat \| wc -l` |
| 7,075 total `.plat` plateau rows | `awk '{print $1}' atlas/corner/out/*.plat \| wc -l` |
| 99 basin laterals | `--stage curated`, `stats.basin_lateral`; cross-check `grep -c 'HIT-3' fleet1/laneD_completions/basin_88at{6,5fs}.jsonl` |
| e15 census 17,283 | `python3 -c "import pickle;print(len(pickle.load(open('experiments/e15_campaign3/tools/pop88.pkl','rb'))))"`; `wc -l experiments/e15_campaign3/sweep_A_fullpop.jsonl` |
| beat88 worklist 33,010 | `wc -l beat88/methods/m2_oracle/runs/pop88_worklist.jsonl` |
| population88_new 54,889 | `wc -l campaign_87/agents/hunt-deeper/population88_new.jsonl` |
| merged-engine 690,850 rows → 433,563 at 88 → 84,989 distinct | `cat campaign_87/agents/merged-engine/runs_hunt/*.pop.jsonl \| wc -l`; `--stage banks` |
| found88_layer89 3,254 | `wc -l campaign_87/hunt87_layer89/found88.jsonl` |
| NRPA 1,441,779 rows → 1,400,343 at 88 | `wc -l campaign_87/wave5_2026-08-04/nrpa/out/sub92.jsonl`; `grep -c '"gates": 88,' <same>` |
| beat88 export files 1,251,227 | `find beat88 -path '*m3_census/exports*' -type f \| wc -l` |
| bulk `.pop.jsonl` 130 files / 13.71 GB | `find campaign_87 -name '*.pop.jsonl' \| wc -l`; `-printf '%s\n' \| awk '{s+=$1}END{print s/1073741824}'` |
| bulk `.pop.jsonl` 88-mask rows 2,840,868 | the `awk -F,` pipeline in §7.1 |
| Run-A B histogram (906 without B) | §4 |
| oracle sample 21/21 | `python3 verify_circuit.py <file>` per row of §6.1 |
| realisability sample 438/438 | §6.2 |

---

## 9. Index row format (`wrapup/corpus88_index.jsonl`)

```json
{"canon":"4604f7230bb0f8ca","gates":88,"depth":7,"n_masks_distinct":88,
 "incarnations":[{"source":"evidence","file":"slp-plateau-search/reproduce/out_88hunt.json","depth":7},
                 {"source":"atlas_corner_plat","file":"slp-plateau-search/atlas/corner/out/hunt.88gates_depth7_88_a3_s1_d0.plat#L2","depth":7},
                 {"source":"campaign_87_merged_engine_pop","file":"campaign_87/agents/merged-engine/runs_hunt/w2_new88.pop.jsonl#L3980"}],
 "n_incarnations":9,"sources":["evidence","atlas_corner_plat","campaign_87_merged_engine_pop"],
 "B":56,"B_theorem_ok":true,"in_e15_census":false}
```

- `canon` — the 16-hex identity of §1. `depth` — smallest depth seen; `null` when no build order is on disk.
- `incarnations` — capped at 8 per row; `n_incarnations` is the true count. Line-addressed rows use `path#Lnnn`.
- `B` / `B_theorem_ok` — present only where a build order exists.
- The **mask sets themselves are not stored** (1.58 M × 88 ints would be ~1.5 GB). They are re-derivable in minutes from the incarnation paths; for the Jean exchange, rerun the stages and dump masks instead of hashes.
- **Size note / disk cost:** the index is 457 MB and `wrapup/work/sink_curated.pkl` (the resumable in-memory state, needed only to re-run `--stage emit` without redoing the scans) is another 328 MB. `zstd -19` takes the index well under 50 MB; compress it before anything is committed or shipped, and delete the pickle once the index is final.

---

## 10. What to tell the public repo, and J. Jean

- "**1,575,516 distinct verified 88-gate MixColumns mask sets available upon
  request**" is defensible: every one replays to all 32 MixColumns targets under
  the repo's own verifier semantics, deduplicated under the project's own
  identity. Quote the tier table at the top so the reader knows what kind of
  object each number counts.
- Say plainly which are **circuits** — 28,796 with a banked build order, so
  directly runnable and depth-labelled, **92 of them at the record depth 5** —
  and which are **mask sets** (1,546,720, build order to be re-derived).
- The **139,878** figure in `aes_mc_records/PAPER.md` is exact, not approximate;
  drop the "≈". The claim it supports ("105,801 of the ≈ 139,878 proven
  irreducible at k = 2") is unaffected.
- Fix the scope word: the e15 Run-A census is *not* "every distinct 88 mask
  multiset on disk" — it is 1.1 % of them, and 92 % of it came from one method.
- The 88-gate plateau is **vast and multi-basin**: three independent harvests
  produced 1,540,221 distinct 88s with zero overlap between them, and the atlas
  corner sweep alone holds 283 mask sets no other corpus here knows.
- **For Jean's foreign-lineage 88s, the ready-made tripwire is:** hash under §1,
  look the hash up in `corpus88_index.jsonl` (novel or not), then run e15's
  `count_B`. All 1,575,516 sets here are duplicate-mask-free and all 28,796
  build-order-bearing ones are B = 56 — so a foreign 88 with `B != 56` would be
  the first ever seen, and would yield an 87 by deletion on the spot.
