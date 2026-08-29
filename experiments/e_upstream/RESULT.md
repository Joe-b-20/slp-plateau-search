# e_upstream — the price of leaving the 88 corpus's vocabulary is exactly 1 gate

> **Written post-hoc on 2026-08-29, during the wrap-up.** The searches are from
> 2026-08-21/22 and were never written up. Nothing here re-runs a search. Everything
> below is either (a) quoted from the on-disk logs with the log line named, or (b) new
> analysis performed on 2026-08-29 over the banked artifacts — the oracle verification,
> the deletion certificates, the independent re-census, and the pricing of the five
> feature classes are all new work of that date. New-work scripts and outputs live in
> `wrapup/day2/e_upstream/`. Items I could not ground are labelled **UNGROUNDED**.

## The number

**There is an oracle-verified 89-gate MixColumns circuit that carries a mask with
`|odd(m)| = 3` — a structural feature with 0 occurrences in 107,803,640 non-target
mask slots across 1,925,065 valid 88-gate circuits (and 0 in the older, wider
184,718,584-slot census).**

```
$ python3 verify_circuit.py wrapup/day2/e_upstream/circuits/S89_41_00000098.json
gates=89 depth=10 outputs_built=32/32 problems=0
VERDICT: VALID MixColumns circuit
```

And it is not a disguised 88:

| certificate on `S89_41_00000098` | result |
|---|---|
| 88 masks distinct, all 32 targets present | yes (89 distinct masks, 32 targets, 57 non-target) |
| reducible by deleting 1 non-target mask | **0 of 57** |
| reducible by deleting 2 non-target masks | **0 of 1,596 pairs** |
| deleting the pinned mask `0x98` alone | leaves **6 masks unbuildable, 4 of them MixColumns target rows** |

So the headline is sharper than "≤ 1 gate". The 89 is **exactly one gate above the
record**, it is **irreducible by 1- and 2-deletion**, and the out-of-vocabulary word is
**load-bearing** — remove it and four of the 32 outputs (`0x10109888`, `0x10988810`,
`0x88101098`, `0x98881010`, one full ρ-orbit) can no longer be built from what remains.

**Price of the feature: 1 gate. Upper bound, from search — the true price is 0 or 1.**

---

## 1. What was asked

`NOTEBOOK.md`, opened 2026-08-21 at Joe's redirect: *why dig at 88/89 for novelty
instead of upstream, where it is easy to grow?*

The premise came from `e_oddlane3`: 3.28 M known 88-gate circuits are built from one
small dictionary, and one structural coordinate is stuck at a value no circuit ever
leaves. A *bias* toward novelty does not survive descent (`trim_masks` keeps only what
the 32 targets need). A **pin** does: add the novel mask `v` to both `engines.TSET` and
`engines.T` — `_extract` iterates the list, so patching only the set lets LNS silently
drop the pin — then descend from an upstream root where `v` is already free. The best
size reached with `v` still alive is `v`'s **survival floor**, and

```
floor - 88  =  the price, in gates, of carrying the feature      (a search upper bound)
```

`NOTEBOOK.md` §3 fixes the reading in advance: floor 88 = the region is inhabited at the
record; 89–92 = the feature costs `floor − 88` gates, "a real, quotable number"; > 92 =
expensive, and we know by how much.

## 2. The feature, defined exactly

Bit `8b + j` of a 32-bit mask is input bit `j` of input byte `b`, `b ∈ {0,1,2,3}`,
`j ∈ {0..7}`. Define the **lane mask** `LANE[j] = Σ_b 1 << (8b+j) = 0x01010101 << j`, and

* `lanes(m) = { j : m & LANE[j] ≠ 0 }` — the bit positions the mask touches
* `odd(m)  = { j : popcount(m & LANE[j]) is odd }` — the bit positions where it carries
  odd byte-parity

The feature is **`|odd(m)| ≥ 3`**. Every input singleton and all 32 MixColumns target
masks have `|odd| = 1`. Code: `probe.py:28-29`, `deep.py:28-29`,
`e_oddlane3/census.py:5-12` — three copies, identical.

The pin that reached 89 is **`0x00000098`** (decimal 152): bits 3, 4 and 7 of byte 0, so
`lanes = {3,4,7}`, each with popcount 1, so `|odd| = 3`, `|lanes| = 3`, weight 3. It is
a perfectly ordinary XOR of three input bits — nothing forbids it. It costs at least
2 gates to build from inputs, and it is **not** one of the 1,778 words in the re-census
vocabulary (§4).

## 3. What was run

Two phases, both 2026-08-21/22, 16 workers, logs `w00.log`..`w15.log` (append mode, so
both phases are in the same 16 files; phase 2 starts at the second `worker N/16:` line).

| | phase 1 — `probe.py` | phase 2 — `deep.py` |
|---|---|---|
| job list | 65 of the 72 `campaign_87/novelty/roots/*.json` carry a `\|odd\|≥3` mask; up to 3 pins per root | `deep_jobs.json` — the 33 best (root, pin) pairs from phase 1 |
| jobs | **192** | **33** |
| budget / job | 1,200 s | 3,600 s |
| `UNREALIZABLE` | 0 | 0 |
| `ERR` | 0 | 0 |
| `FLOOR` lines | 192 | 33 |
| pin alive at the floor | **192 / 192** | **33 / 33** |
| banked | 0 (`probe.py` banks only `n ≤ 89`) | **33** |

Job accounting commands (`experiments/e_upstream/`):

```
grep -h "jobs, 1200s" w*.log | awk '{s+=$3}END{print s}'   -> 192
grep -h "jobs, 3600s" w*.log | awk '{s+=$3}END{print s}'   ->  33
grep -hc "FLOOR"        w*.log | awk '{s+=$1}END{print s}' -> 225   (= 192 + 33)
grep -hc "banked"       w*.log | awk '{s+=$1}END{print s}' ->  33
grep -hc "UNREALIZABLE" w*.log | awk '{s+=$1}END{print s}' ->   0
grep -h  "ERR "         w*.log                             -> (empty)
```

**This closes the gap `wrapup/reports/experiments_early.md` §7 flagged** ("I did not
determine whether e_upstream's job list ran to completion"): 192/192 and 33/33 ran to a
reported floor. Nothing was preempted.

**Cost: 192 × 1,200 + 33 × 3,600 = 349,200 core-seconds ≈ 97.0 core-hours.** Exact, not
estimated: the only early exit in both scripts is `if ctx.bestn <= 88: break`, which
never fired.

### Floor distributions

| floor | 89 | 90 | 91 | 92 | 93 | 94 | 95 | 96 | 97 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| phase 1 (192 jobs, 1,200 s) | 0 | 3 | 30 | 57 | 53 | 27 | 15 | 6 | 1 |
| phase 2 (33 jobs, 3,600 s) | **1** | 3 | 6 | 12 | 6 | 5 | — | — | — |

Phase 2 re-ran only jobs whose phase-1 floor was 90 or 91 (`deep_jobs.json`: 3 at 90,
30 at 91) and tripled their budget. Tripling the budget moved the best floor 91 → 89.

### Provenance of the 89

* **Root:** `campaign_87/novelty/roots/root_41_randset_wide_g149_d12.json` — 149 gates,
  depth 12, `constructor: randset_wide`, dated 2026-07-29. `0x98` is one of its 149
  masks, created for free by a search that was not trying to make it.
* **Phase 1** floor for this (root, pin): **91** (`deep_jobs.json`, `prev_floor: 91`).
* **Phase 2**, `w00.log:458-506`, one worker, 3,600 s:

```
  root_41_randset_wide_g149_d12.json  pin 0x00000098 nodd=3 nlane=3  from 149 gates
    148  (v alive: True)
    146  (v alive: True)
    ...  (57 improvement lines, v alive: True on every one)
     91  (v alive: True)
     90  (v alive: True)
     89  (v alive: True)
    FLOOR 89  v_alive=True
    *** banked ***
```

149 → 89 in one 3,600 s LNS+walk loop, the pin alive at every single improvement.

## 4. The zero-occurrence claim, stated precisely and re-checked

### 4.1 What the original "184 M mask slots" covers

`e_oddlane3/census.py`, run 2026-08-21, 393 s. Its population is defined by a **first-line
sniff**: every `*.jsonl` in the repo of size ≥ 2,000 bytes **whose first line parses to a
list of 88 masks** — 460 files, 3.9 GB. A row is admitted if its mask list has length 88
and integer entries. Reported:

```
88-gate circuits scanned:            3,280,541
distinct non-target masks:               3,172
#odd-lanes histogram:   0: 113,366,654   1: 67,470,645   2: 3,881,285   3+: 0
```

Three things a reader must know about that population, none of them stated in the
notebook:

1. It counts **rows, not distinct circuits**. Nothing was deduplicated.
2. `census.py:40` admits a row on `len(ms)==88` alone — it **never checks that the 32
   targets are present**. The histogram sums to **184,718,584** slots, i.e.
   184,718,584 / 3,280,541 = **56.31** non-target masks per row, where a valid 88 has
   exactly 56. About **1.0 M of the 184.7 M slots therefore come from rows that are not
   valid MixColumns circuits.**
3. The first-line sniff **skips mixed-size files.** The project caught this itself
   (`e_oddlane3/hunt.py` docstring) and re-swept every `.jsonl` (3,891 files, cap 60,000
   rows each). `hunt.out` ends `DONE. total 88-gate sets with a >=3-odd-lane mask: 4` —
   and all four are logged `targets=False realizable=False`, all four from
   `campaign_87/wave6_2026-08-11/discriminate/runs/surrogates_88.jsonl`. They are
   **surrogate / transposed states, not MixColumns circuits.** The census claim survives.

`wrapup/corpus88_index.jsonl` **cannot** be used to re-check this: by design it stores
hashes, not masks (`wrapup/CORPUS88.md` §9).

### 4.2 Independent re-census, 2026-08-29 — the claim holds

`wrapup/day2/e_upstream/recensus.py`, one `nice -n 19` worker, 805 s. Population named
explicitly and **target-checked**: the five mask-bearing 88-gate banks of
`wrapup/CORPUS88.md` §2.1, plus the `evidence/` record circuits. A row is admitted only
if it has exactly 88 masks **and all 32 target masks present**.

| | |
|---|---:|
| rows accepted (88 masks + all 32 targets) | **1,925,065** |
| rows rejected, wrong length | 257,291 |
| rows rejected, missing a target | **0** |
| non-target mask slots | **107,803,640** (= 1,925,065 × 56, exactly) |
| distinct non-target masks (the vocabulary) | **1,778** |
| circuits containing a `\|odd\| ≥ 3` mask | **0** |
| circuits containing a `\|odd\| ≥ 4` mask | **0** |

```
#odd-lanes histogram:   0: 64,099,791   1: 39,307,442   2: 4,396,407   3+: 0
per source: nrpa_sub92 1,400,343 | merged_engine 433,563 | population88_new 54,889
            beat88_worklist 33,010 | found88_layer89 3,254 | evidence_records 6
```

Two independent cross-checks came out exactly right: `nrpa_sub92` = **1,400,343** rows at
88 gates, matching `wrapup/CORPUS88.md` §2.1 to the unit; and the slot count is exactly
56 × rows, which the original census's was not.

**`0x98` is not in the 1,778-word vocabulary.** Neither is any `|odd| ≥ 3` mask.

This population is *smaller* than the original census's (1.93 M target-checked rows vs
3.28 M unchecked rows) and its vocabulary is *smaller* (1,778 vs 3,172), because it is
the clean subset. Quote whichever you like; the `|odd| ≥ 3` count is 0 in both.

**UNGROUNDED:** `e_w2novel/probe.py`'s docstring cites a third, earlier count — "2.65 M
distinct 88-gate circuits ... 2,063 distinct values" from a "bigcensus" of 2026-08-21.
No script or log by that name is on disk. Treat 3,172 (census.py) and 1,778 (recensus.py)
as the two grounded vocabulary sizes and ignore 2,063.

## 5. Verification — 33 / 33 through the oracle

`experiments_early.md` §7 recorded that **none of the 33 floors had ever been through
`verify_circuit.py`**, because they are stored as `{"masks": [...]}` and the oracle takes
gate lists. Done on 2026-08-29.

`wrapup/day2/e_upstream/tomake.py` recovers a build order by greedy topological
construction (emit any unbuilt mask that is the XOR of two already-available signals) and
writes `{"gates": [[a,b],...]}`.

| | |
|---|---:|
| floors converted | 33 / 33, **0 unbuildable masks** in any of them |
| mask counts | 89 ×1, 90 ×3, 91 ×6, 92 ×12, 93 ×6, 94 ×5 — matching the filenames |
| all masks distinct | 33 / 33 |
| all 32 targets present | 33 / 33 |
| pinned mask present | 33 / 33 |
| `verify_circuit.py` verdict | **33 / 33 `VERDICT: VALID MixColumns circuit`** |

```
for f in wrapup/day2/e_upstream/circuits/S*.json; do python3 verify_circuit.py "$f"; done
```

The emitted orders are also **depth-optimal**: an exact layered-BFS minimum depth over
each mask set returns the same depth `verify_circuit.py` reports for the emitted order,
in all 33 cases. The 89 is **89 gates at depth 10, and 10 is the exact minimum depth of
that mask set**.

## 6. Deletion certificates — and a distinction the notebook missed

New, 2026-08-29, pure counting over the 33 verified circuits. This is the mask-set
analogue of e15's `B = 56` tripwire (`wrapup/CORPUS88.md` §4): if some non-target mask
`m` can be dropped with the remaining set still realizable, the circuit is secretly one
gate cheaper.

**Single deletion — 33 floors, every non-target mask tested:**

| | |
|---|---:|
| floors reducible by one deletion | **13 of 33** |
| deletable masks found | 13 |
| of those, deletions that **preserve the pin** | **0** |
| **in every one of the 13, the only deletable mask is the pin itself** | ✔ |

That is a clean, self-consistent confirmation of the whole method — and a distinction
worth drawing:

* In **13 floors** the novel word is an **appendix**: a dangling gate that computes it and
  feeds nothing. Those floors measure the price of *having the word present* (trivially 1)
  and their true novelty-free optimum is one gate lower.
* In the other **20 floors, including the 89**, the novel word is **woven in**. For
  `S89_41_00000098`, deleting `0x98` leaves six masks unbuildable — `0x00008898`,
  `0x10009898`, and the four target rows `0x10109888`, `0x10988810`, `0x88101098`,
  `0x98881010` (one complete ρ-orbit). The circuit is *built around* the out-of-vocabulary
  word.

**Pair deletion — 58,496 pairs tested across the 33 floors:**

| | |
|---|---:|
| pairs tested | **58,496** |
| pairs whose removal leaves a realizable set | **3** |
| of those, pin-preserving | **0** — every hit includes the pin |
| pairs tested on `S89_41_00000098` | **1,596**, hits **0** |

So `S89_41_00000098` is **irreducible by 1-deletion and by 2-deletion**: it is not a
mislabelled 88, and it is not a mislabelled 87. The 3 pair hits are in the 92/93-gate
floors (`S92_36`, `S92_47`, `S93_56`) and each drops the pin plus one more mask, i.e.
they are the appendix case one level deeper.

## 7. The five never-priced feature classes

`NOTEBOOK.md` §5 lists five further classes for the same machine and prices none of them.
Each is defined precisely below, with what it would take to price it, and with whatever
pricing is available from **counting alone** over the artifacts that already exist:
the 33 verified floors, the 72 from-scratch roots, the six record 88s, and the 1.93 M-row
re-census. **Three of the five are now priced without a solver. Two remain open leads.**

### C1 — `|odd(m)| ≥ 4`

*Definition:* the same coordinate as the main feature, one notch further out — a mask
carrying odd byte-parity in four or more of the eight bit lanes.

*Why it was designed:* if `|odd| ≥ 3` costs 1 gate, the natural question is whether the
price is a step or a slope. `|odd| ≥ 4` is the next rung and tells you which.

| measurement | value |
|---|---:|
| occurrences in the re-census (107.8 M slots, 1.93 M circuits) | **0** |
| occurrences in the 33 e_upstream floors (89–94 gates) | **0** |
| roots (of 72) carrying an `\|odd\| ≥ 4` mask, free | **22**, 153 occurrences |
| roots carrying an `\|odd\| ≥ 5` mask | 12, 27 occurrences |

**Verdict: NOT PRICED. Open lead, and the cheapest of the five to run.** It needs a
solver/search run — the existing harness, unmodified: `deep.py` with the candidate filter
`nodd(m) >= 4`. There are 22 usable roots with 153 candidate pins. Calibrating on phase 1
(1,200 s got 65 roots to 90–97; 3,600 s got the best to 89), a first pass of 153 jobs ×
1,200 s = **51 core-hours** would bracket it, and a 33-job second pass at 3,600 s adds 33.
**Not run** — far past the ≤ 5-minute single-core budget for this session.
*Prediction worth recording before it runs:* the phase-1 floor distribution for `|odd|≥3`
peaked at 92 and only 3 of 192 jobs reached 90; a class that is strictly rarer upstream
(153 occurrences vs 780) should land 1–3 gates worse, i.e. a floor of 90–92.

### C2 — the weight-2 masks that appear in no circuit of the corpus

*Definition:* a weight-2 mask is `(1<<i) | (1<<j)`, the output of a single XOR of two raw
input bits. There are `C(32,2) = 496`. `e_w2novel/candidates.json` lists **388** of them
as appearing in **no** circuit of the 3.28 M corpus — implying 108 do appear.

*Why it was designed:* it is the *exhaustive* novelty class. Deciding all 388 decides the
entire single-gate novelty question, with no sampling.

| measurement | value |
|---|---:|
| weight-2 masks in the re-census vocabulary (1.93 M circuits) | **85** |
| of those 85, masks `e_w2novel` lists as never seen | **2** — `0x00001800`, `0x08008000` |
| the 33 e_upstream floors containing at least one candidate | **28 of 33** |
| distinct candidates realised across the 33 floors | **40** |
| cheapest floor carrying one | **90 gates** (`S90_01_00088010`, `S90_54_08008400`, 2 each) |

**Verdict: PARTIALLY PRICED BY COUNTING — and the candidate list is wrong.**

1. **`0x00001800` and `0x08008000` are not novel at all.** They occur in valid 88-gate
   circuits in the re-census population, so their price is **0 gates**. The candidate list
   is at most 386, not 388. (This direction of error is one-way: a mask I observe present
   is definitively present. Whether more of the 388 fall is unknown — my population is a
   subset of theirs.)
2. **40 further candidates are priced at ≤ 2 gates for free**, by the floors this
   experiment already banked: 28 of the 33 verified circuits happen to contain one, the
   cheapest at 90 gates. Nobody had to run anything; the answer was sitting in the
   artifacts. The full 40-mask list is in `wrapup/day2/e_upstream/classes.json`
   (`aggregate.w2novel_seen`).
3. The remaining ~344 are unpriced. `e_w2novel/probe.py` exists and has **never been run**
   (no logs, no ledger, no `HIT_*.json`). It is a radius-1 pin probe from the four record
   88s, which `NOTEBOOK.md` §3 itself argues can only ever return 89 — so running it as
   written is not worth 388 × 900 s ≈ **97 core-hours**. Re-pointing it at the upstream
   roots (all 72 of which carry candidates — 1,890 occurrences) is the version worth
   running.

### C3 — mask weight ≥ 12

*Definition:* `popcount(m) ≥ 12` — a very heavy signal, an XOR of 12+ input bits.

*Why it was designed:* to test whether the corpus avoids *big* objects generally, or
specifically avoids odd-parity structure. `e_oddlane3` reported corpus weights ranging
2…18 and called the coordinate "not degenerate".

| measurement | value |
|---|---:|
| re-census weight histogram | 2: 33,345,151 · 3: 21,550,464 · 4: 27,215,653 · 5: 13,544,246 · 6: 7,767,197 · 7: 3,757,561 · 8: 108,947 · 9: 88,594 · 10: 58,996 · 11: 366,577 · **12: 254** |
| valid 88-gate circuits carrying a weight-12 mask | **254** |
| the 33 e_upstream floors carrying one | 0 (max weight over the 33 is 11) |
| roots (of 72) carrying one, free | 1 |

**Verdict: PRICED AT 0 GATES. The class is not out-of-vocabulary and never was.** 254
oracle-admissible 88-gate circuits in the re-census population already contain a
weight-12 mask. There is nothing to buy. (`e_oddlane3`'s wider census saw weights up to
18, so the statement is only stronger there.) Pinning a weight-≥12 mask and descending
would burn ~50 core-hours to re-derive a floor of 88 that counting gives in 805 s.
This class should be struck from the list.

### C4 — fan-out ≥ 8 on one mask

*Definition:* some signal is consumed as an operand by 8 or more gates. `e_oddlane3`
measured max fan-out ≤ 5 across the corpus and 3–4 in the record 88s.

*Why it was designed:* every other class is a property of a *mask*; this one is a property
of the *wiring*. If the corpus's fan-out ceiling is real it is a completely different kind
of constraint from the vocabulary.

*The catch, which the notebook does not note:* **fan-out is not a property of a mask set.**
The same 88 masks admit many build orders with different fan-outs, so this class cannot be
priced by pinning a mask at all — the harness in this directory is the wrong instrument.

New measurement (`wrapup/day2/e_upstream/fanout.py`). For a signal `s`, define
`potential(s) = |{ x ∈ SIG, x ≠ s : s ^ x ∈ S }|` — how many masks of `S` *could* be
produced by a gate consuming `s`. Every build order realises `fanout(s) ≤ potential(s)`.

| circuit set | max potential | best fan-out any *heuristic* scheduler here realised |
|---|---:|---:|
| the six record 88s | **8 on every one** (e.g. `0x00808000` in `mixcolumns_88gates_depth5`) | 3–5 |
| the 33 e_upstream floors | 6–11 | 2–6 |
| the 72 upstream roots (as built) | — | **53 of 72 roots already have fan-out ≥ 8**, max 11 |

Potential 8 on every record 88 means the mask sets are *not* combinatorially barred from
fan-out 8 — so the open question was exactly: **does the record 88's mask set admit a
valid acyclic build order realising fan-out 8?**

#### C4 — CLOSED, exactly, 2026-08-29

Answered by CP-SAT, not by heuristics. `wrapup/day2/e_upstream/c4_fanout_cpsat.py`,
one `nice -n 19` thread, **total 39 mask sets, ~5 minutes**:

```
SIG   = the 32 input singletons + S
y[m,p] in {0,1} for each producing pair p = {a,b} of each mask m in S,  sum_p y[m,p] = 1
pos[m] in [0, |S|-1]
y[m,{a,b}] = 1  =>  pos[a] < pos[m]  and  pos[b] < pos[m]        (acyclicity)
maximise  fanout(s) = sum over (m,p) with s in p of y[m,p]
```

The optimum is the **exact maximum fan-out on signal `s` over every valid build order of
that mask set**. Sweeping signals in decreasing `potential` and stopping once the
incumbent reaches the next signal's potential makes the per-circuit answer **exhaustive
over all signals too** (`fanout(s) ≤ potential(s)` always), so each row below is the exact
maximum fan-out of that mask set, full stop.

| mask set | max potential | **exact max fan-out over all build orders** |
|---|---:|---:|
| `mixcolumns_88gates_depth5` | 8 | **4** |
| `mixcolumns_88gates_depth5_fromscratch` | 8 | **4** |
| `mixcolumns_88gates_depth6` | 8 | **4** |
| `mixcolumns_88gates_depth7` | 8 | **4** |
| `mixcolumns_88gates_depth8_thirdfamily` | 8 | **3** |
| `jean_88gates_depth7_eprint_2026-1481` | 8 | **5** |
| the 33 e_upstream floors (89–94 gates) | 6–11 | 3 ×4, 4 ×20, 5 ×8, **6 ×1** (`S92_36`, at 92 gates) |

```
39 / 39 sweeps exhaustive · 0 timeouts · every solve returned OPTIMAL
record 88s : exact max fan-out = 5   (max potential was 8)
all 39 sets: exact max fan-out = 6   (at 92 gates)
fan-out >= 8 realisable at 88 gates:  NO
```

**Verdict: NO. Fan-out ≥ 8 is not realisable at 88 gates on any record-88 mask set, and
this is a proof over all build orders, not a search result.** The gap between potential 8
and the true optimum 3–5 is real: the eight candidate consumers of a signal can never all
be scheduled, because acyclicity forces most of those masks to be built before the shared
signal is available. So `e_oddlane3`'s "max fan-out ≤ 5" is **not** an artifact of how the
project's engines schedule — on these mask sets it is a theorem. The best fan-out seen
anywhere in the banked material is **6, and it costs 4 gates** (`S92_36_00204004`, 92
gates), which is the only price this class has.

*Scope, honestly:* this closes the question **for the six record 88s and the 33
e_upstream floors — 39 mask sets, exactly**. It does not decide fan-out ≥ 8 over all
1.93 M corpus 88s. A stratified sample of 150 further corpus 88s from three banks is
running under the identical exact model (`c4_corpus_sample.py`,
`c4_corpus_sample.json`); read that file for the widened histogram.
*What is now certain:* pinning a mask was always the wrong instrument for this class, and
no synthesis run should ever be spent on it. Cost of the answer: **~5 minutes of one
nice-19 core**, versus the ~50 core-hours a pinned campaign would have burned.

### C5 — the column-parity hubs `T_j` absent from every record 88

*Definition:* **UNGROUNDED as to the original author's intent** — the term is used in
`e_oddlane3/NOTEBOOK.md` and `e_upstream/NOTEBOOK.md` and defined in neither. The only
reading consistent with both notebooks is `T_j = LANE[j] = 0x01010101 << j`, the XOR of
input bit `j` across all four bytes. Corroboration: under this reading the six record 88s
carry 1, 2, 2, 1, 1, 1 of them, matching `e_oddlane3`'s "1–2 of the 8 per circuit" exactly.
Note `|odd(T_j)| = 0` and `weight(T_j) = 4` for every `j`.

*Why it was designed:* they are the natural "hub" signals of the matrix, and the record
circuits use only a couple of them.

**First, a correction.** `NOTEBOOK.md` §5 names `T_0, T_3, T_4, T_7` as absent from every
record 88. Recomputed over all six record circuits:

| circuit | hubs present |
|---|---|
| `mixcolumns_88gates_depth5.json` | `T_2` |
| `mixcolumns_88gates_depth5_fromscratch.json` | `T_4, T_6` |
| `mixcolumns_88gates_depth6.json` | `T_4, T_6` |
| `mixcolumns_88gates_depth7.json` | `T_1` |
| `mixcolumns_88gates_depth8_thirdfamily.json` | `T_2` |
| `jean_88gates_depth7_eprint_2026-1481.json` | `T_1` |

Present in ≥ 1 record 88: **`T_1, T_2, T_4, T_6`**. Absent from every one: **`T_0, T_3,
T_5, T_7`**. `T_4` is present (twice); the notebook's list should read **`T_5`, not
`T_4`**.

**And then the class dissolves.** Over the 1.93 M-circuit re-census:

| hub | `T_0` | `T_1` | `T_2` | `T_3` | `T_4` | `T_5` | `T_6` | `T_7` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| occurrences in valid 88s | **6** | 448,206 | 56,016 | **2,744** | 6,579 | **3,355** | 166 | **1,429,688** |

**Verdict: PRICED AT 0 GATES. All eight hubs — including all four "absent" ones — occur
in valid 88-gate MixColumns circuits.** `T_0` is rare (6 circuits in 1.93 M) and `T_7` is
near-universal (74 %), but none is extinct. "Absent from every record 88" was a statement
about six hand-picked circuits, not about the corpus. Nothing to buy here either.

(Bonus refinement: hubs per circuit ranges **0–5**, not "1–2" — histogram
`{0: 7, 1: 1,909,794, 2: 9,814, 3: 4,476, 4: 960, 5: 14}`. And the 33 e_upstream floors
between them carry `T_1..T_7`, cheapest `T_5` and `T_7` at 90 gates, `T_3` at 91 — which
would have priced the class at ≤ 2 even without the re-census.)

### Summary of the five

| class | status after 2026-08-29 | price | what would settle it |
|---|---|---|---|
| C1 `\|odd\| ≥ 4` | **open lead** | unknown | `deep.py` with `nodd ≥ 4`; 153 pins × 1,200 s ≈ **51 core-h** + 33 core-h refine |
| C2 the 388 weight-2 masks | **partly priced; list is wrong** | 2 masks at **0**, 40 masks at **≤ 2**, ~344 open | re-point `e_w2novel/probe.py` at the roots, not the record 88s (≈ 97 core-h as written) |
| C3 weight ≥ 12 | **CLOSED** | **0 gates** (254 circuits) | — nothing; strike from the list |
| C4 fan-out ≥ 8 | **CLOSED, exactly** | **unreachable at 88** on all 39 mask sets tested; best anywhere is fan-out 6 at 92 gates | — nothing; the CP-SAT answer took ~5 min and is exact over all build orders |
| C5 the hubs `T_j` | **CLOSED** | **0 gates** (all 8 occur) | — nothing; and fix `T_4` → `T_5` in the notebook |

**Three of the five classes are now closed at a cost of about ten minutes of one core**,
against the ~200 core-hours a pinned campaign over all five would have consumed. Two of
the three (C3, C5) turned out never to have been out-of-vocabulary at all, and the third
(C4) was never a mask-pinning question. Only **C1** is a genuine unpriced feature class,
and C2 is genuine but its candidate list needs rebuilding first.

## 8. What the 89 does and does not say about 87

This is the most "an 87 could hide here"-shaped result in the project, because it is the
only measured *cheap exit* from the shared vocabulary. Being precise about it matters.

### What it does establish

1. **A structural argument for 88-optimality is dead.** The strongest form of "the corpus
   proves 88 is special" runs: *1.9–3.3 million independently-found 88s, across every
   engine and family this project has, all use one dictionary of 1,778 (or 3,172) words;
   that dictionary must be forced.* It is not forced. It costs **1 gate** to step outside
   it, and the step is not marginal — the 89 is irreducible by 1- and 2-deletion and four
   of its target rows depend on the novel word. The vocabulary is a **funnel artifact of
   descent**, priced at ≤ 1 gate, not a law.
2. **The direction of the error is known and one-way.** Both quantities here are upper
   bounds: the floor is an upper bound on the true minimum for a pinned feature, and the
   price `floor − 88` is therefore an upper bound on the true price. Measurement can only
   **overstate** the price. So "≤ 1 gate" is safe; "= 1 gate" would not be.
3. **Reachable at 89 from upstream, unreachable at 88 by editing.** `e_oddlane3`'s radius-1
   probe pinned `|odd| ≥ 3` candidates one edit away from a record 88 and got **89 on every
   completed pin**. e_upstream constructed *into* the region and got 89. The two agree, and
   the operational lesson is the notebook's own: **construct into the region, do not edit
   toward it.**

### What it does not establish — plainly

1. **It does not lower any bound on 87. Not by a fraction of a gate.** No proof-side object
   in this directory constrains 87 at all. Everything here is a search upper bound.
2. **It is not evidence that an 87 exists.** The chain "vocabulary is not forced ⇒ maybe
   the searches missed a region ⇒ maybe an 87 lives there" has a false step: exiting the
   vocabulary costs **at least 0 and at most 1 gate**, and an 87 needs a gate *back*. The
   honest reading is the opposite of the exciting one — this experiment tried hard, from
   192 + 33 independent starts and 97 core-hours, to carry a novel word down, and the best
   it ever reached was **89**. It never touched 88, let alone 87.
3. **No 88 outside the vocabulary has ever been exhibited.** Not by this experiment, not by
   `e_oddlane3`, not anywhere on this machine. The four corpus 88-mask sets that do carry
   the feature (`hunt.out`) are surrogate/transposed states with `targets=False`,
   `realizable=False` — not circuits.
4. **The pinned-descent method cannot refute anything.** A floor of 89 means "89 was the
   best reached in 3,600 s from this root". It does not mean 88 is unreachable with that
   pin. `NOTEBOOK.md` says this ("Every number here is an upper bound on the true floor —
   search, not proof") and it is worth repeating in a document someone might cite.
5. **The obvious follow-up was never run.** `deep.py`'s loop breaks at `bestn <= 88` and
   spends its whole budget descending from 149 gates. **No run has ever started from the
   89 and pushed at 88.** The 89 → 88 gap has received zero dedicated seconds.

### The cheapest decisive next computation, with an honest price

Ranked by value per core-hour. All three are for the record; the 87 search stays ended and
nothing below was run in this session.

| # | computation | what it decides | honest price |
|---|---|---|---|
| **1** | **Re-seed the descent at the 89.** Pin `0x98`, seed from `S89_41_00000098`'s 89 masks, target 88, LNS+walk. This is the one thing e_upstream never did: every one of its 225 jobs started at 100–173 gates and spent its budget on the 149→89 stretch. | Reaching 88 gives the **first 88-gate MixColumns circuit outside the corpus vocabulary** — a genuinely new structural object and the entrance to unsampled plateau. Failing repeatedly is the sharpest available evidence that the 88 plateau really is confined to its dictionary. | **1 core-hour for a first answer**; ~20 core-hours to do all 20 non-appendix floors, ~33 to do all 33. The harness exists and needs a two-line seed change. **Cheapest by an order of magnitude.** |
| 2 | **Exact fan-out re-scheduling** (C4 above) on one record 88's mask set. | Whether "fan-out ≤ 5" is structural or a scheduling artifact — the only one of the five classes that is about wiring rather than vocabulary. | **Minutes** of CP-SAT, once a ~50-line model is written. |
| 3 | `deep.py` with `nodd ≥ 4` (C1 above). | Whether the price of leaving the vocabulary is a step or a slope. Only meaningful *after* #1: if #1 reaches 88, the whole price scale shifts down by one. | **51 + 33 core-hours.** |

Note what is *not* on this list: nothing here is an 87 hunt. #1 asks for an **88**, and its
value is structural — it would be the first evidence that the plateau extends past the
dictionary, or the first real evidence that it does not.

### Status of #1 and #2 as of 2026-08-29 12:00

* **#2 is done.** Answer: **NO** — see C4 above. Exact, exhaustive over all build orders
  on 39 mask sets, ~5 minutes. `e_oddlane3`'s fan-out ceiling is structural, not a
  scheduling artifact.
* **#1 is RUNNING.** `wrapup/day2/e_upstream/seed89.py` (a patched **copy** of `deep.py`;
  the originals in this directory are untouched), launched 11:36 local, PID 1372715,
  budget 10,000 s wall ≈ 1.2 core-hours at the measured ~43 % of a core. Registered in
  `wrapup/day2/runs/RUNS.md` §R1 with kill instructions. Live log
  `wrapup/day2/e_upstream/seed89.log`, ledger `seed89_ledger.jsonl`; any ≤ 88-mask state
  is written to disk the instant it appears, as `HIT88_00000098_*.json` plus a decoded
  oracle-format circuit. **Read the ledger's final `ev:"done"` row for the verdict.**
  Reminder for whoever reads it: a floor of 89 there is an upper bound from search, not a
  proof that 88 is unreachable with this pin.

## 9. Corrections this write-up makes to other documents

| document | claim | correction |
|---|---|---|
| `e_upstream/NOTEBOOK.md` §5 | hubs `T_0, T_3, T_4, T_7` absent from every record 88 | `T_4` is present in two of them; the absent set is `T_0, T_3, **T_5**, T_7` — and all eight occur in the corpus, so the class prices at 0 |
| `e_upstream/NOTEBOOK.md` §4 | "65 roots × up to 3 pins each (~190 jobs)" | exactly **192** jobs ran in phase 1, plus **33** in phase 2 |
| `e_oddlane3/NOTEBOOK.md` §2 | column-parity hubs "1–2 of the 8 per circuit" | 0–5 over 1.93 M circuits; `{0:7, 1:1909794, 2:9814, 3:4476, 4:960, 5:14}` |
| `e_w2novel/candidates.json` | 388 weight-2 masks appear in **no** circuit | at least 2 of them do (`0x00001800`, `0x08008000`); the list is ≤ 386 |
| `wrapup/LEADS.md` §16 | the e_oddlane3 radius-1 probe returned 89 "on every one of ~76 × 14 candidates" | 76 jobs were **declared** across 14 workers; **28 pins started, 14 reported a result**, all 14 → 89, and no worker logged `done`. `e_upstream/NOTEBOOK.md` §3 already says "stopped at 14/76"; LEADS overstates it |
| `wrapup/reports/experiments_early.md` §7 | "I could not oracle-verify the 33 e_upstream floor circuits" / "did not determine whether the job list ran to completion" | both closed: **33/33 oracle-VALID**, **192/192 + 33/33 jobs completed** |
| `wrapup/reports/experiments_early.md` §2 | "the measured price of leaving the corpus vocabulary is **≤ 1 gate**" | correct, and now sharper: the 89 is irreducible by 1- and 2-deletion and the novel word is load-bearing for four target rows |

## 10. File map

### In this directory (the 2026-08-21/22 run — unchanged)

| file | what it is |
|---|---|
| `NOTEBOOK.md` | the design note: premise, the pin trick, the reading table, the five classes |
| `probe.py` | phase 1 — 192 jobs, 1,200 s each; banks only `FLOOR<n>_*.json` for `n ≤ 89` (none) |
| `deep.py` | phase 2 — 33 jobs, 3,600 s each; banks every alive floor as `S<n>_<root>_<pin>.json` |
| `deep_jobs.json` | the 33 (root, pin, prev_floor) records phase 2 re-ran |
| `S89_41_00000098.json` | **the result.** 89 masks, pin `0x98`, root `root_41_randset_wide_g149_d12` |
| `S9[0-4]_*.json` (32 more) | the other floors: 90 ×3, 91 ×6, 92 ×12, 93 ×6, 94 ×5 |
| `w00.log` … `w15.log` | 16 worker logs, both phases appended; the 89's trace is `w00.log:458-506` |

### New, 2026-08-29 (`wrapup/day2/e_upstream/`)

| file | what it is |
|---|---|
| `tomake.py` | mask set → oracle-format gate list, by greedy topological build |
| `circuits/S*.json` | **the 33 floors in oracle format** — all 33 `VERDICT: VALID` |
| `convert.json` | per-floor conversion record: mask counts, targets, pin, `|odd|≥3` masks |
| `recensus.py` | the independent, target-checked re-census over a named population |
| `recensus.json` | its output: 1,925,065 rows, 107,803,640 slots, 1,778 words, 0 at `\|odd\|≥3` |
| `recensus.log` | the run log with per-source timings (805 s, one `nice -n 19` worker) |
| `vocab.json` | the 1,778-word vocabulary, sorted |
| `deletions.py` / `deletions.json` | the single-deletion certificates + the pin-removal cascades (§6) |
| `deletion_pairs.log` | the pair-deletion sweep: 58,496 pairs, 3 hits, 0 pin-preserving (265 s) |
| `classes.py` / `classes.json` | the five-class pricing over floors, roots and record 88s |
| `fanout.py` / `fanout.json` | fan-out *potential* vs heuristically realised — the reconnaissance for C4 |
| `c4_fanout_cpsat.py` / `.json` | **C4 closed:** exact max fan-out over all build orders, 39 mask sets, exhaustive |
| `c4_corpus_sample.py` / `.json` / `.log` | the same exact model over a stratified sample of corpus 88s (widening C4's base) |
| `seed89.py` | **the patched copy of `deep.py`** that re-seeds the descent at the 89, target 88 (§8 #1) |
| `seed89.log` / `seed89_ledger.jsonl` / `seed89.nohup` | that run's live log, ledger and stdout; hits land as `HIT88_00000098_*.json` |
| `../runs/RUNS.md` | the launch register: command, PID, budget, purpose, kill instructions |

### Read alongside

| file | why |
|---|---|
| `experiments/e_oddlane3/NOTEBOOK.md`, `census.py`, `hunt.py`, `hunt.out` | where the feature and the "zero occurrences" claim come from, and the self-correction |
| `experiments/e_w2novel/candidates.json`, `probe.py` | class C2's candidate list (≤ 386, not 388) and its never-run probe |
| `wrapup/CORPUS88.md` | the corpus this is measured against; §9 explains why the index holds no masks |
| `wrapup/LEADS.md` §16 | the lead entry this write-up closes |

## 11. UNGROUNDED items, listed

* **`T_j` is never defined in any primary source.** `T_j = 0x01010101 << j` is my
  reconstruction. It reproduces `e_oddlane3`'s "1–2 hubs per record 88" exactly, which is
  good corroboration, but it is a reconstruction.
* **The "bigcensus" cited in `e_w2novel/probe.py`** (2.65 M circuits, 2,063 masks) has no
  script and no log on disk.
* **Whether more than 2 of the 388 weight-2 candidates are actually present.** My
  re-census population is a subset of `census.py`'s; masks I found are definitively
  present, masks I did not find may still be.
* **Whether phase 1's 192 jobs are the intended complete list.** `probe.py` builds its job
  list from `roots()` at run time; the count 192 is what the logs report, and the
  notebook's "~190" agrees, but no manifest was banked for phase 1 (unlike phase 2's
  `deep_jobs.json`).
* **Whether the 33 floors' mask sets are novel against `wrapup/corpus88_index.jsonl`.**
  They are 89–94 gates, so they are outside that index by construction; no equivalent
  index exists at 89+.
* **The C1 prediction in §7 (floor 90–92) is a guess**, recorded so it can be scored, not
  a measurement.
