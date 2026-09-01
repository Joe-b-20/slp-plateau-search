# CERT — the corpus-wide single-mask deletion-realisability certificate

**Additive file, 2026-08-30.** Executes LEAD-1 of `atlas/corner/ANALYSIS_20260829.md`
§8: extend the §7 deletion certificate from the 498 atlas corner 88s to the
whole indexed corpus. Nothing outside `wrapup/day2/deletion_cert/` was written;
no live directory was touched; all compute `nice -n 19`, at most two threads.

---

## 1. The statement

> **THE CERTIFICATE.** Let `M` be any of the **1,575,516** distinct verified
> 88-gate MixColumns mask sets indexed by `CORPUS88.md` — the corpus **entire** —
> and let `m` be any of its 56 non-target masks. Then `M \ {m}` — an 87-mask set
> that still contains all 32 MixColumns target masks — is **not realisable as an
> XOR-SLP over the 32 inputs**. **88,228,896 / 88,228,896 candidate 87-mask sets
> closed, machine-checked, 0 realisable.**

Equivalently: **no 87-gate MixColumns circuit is obtainable from any of
1,575,516 distinct known 88s by deleting one gate, even with unrestricted
rewiring of the surviving 87 masks.**

This is strictly stronger than the `B = 56` test of `CORPUS88.md`, which only
asks whether a middle gate has *a consumer*; it does not ask whether that
consumer has an **alternative derivation** in the remainder. This does, and it
allows the remaining 87 masks to be rebuilt in any order whatsoever.

| | before (ANALYSIS §7) | now |
|---|---|---|
| mask sets under the deletion test | 498 | **1,575,516 (100 % of the corpus)** |
| candidate 87-mask sets closed | 27,888 | **88,228,896** |
| pass the local necessary condition | 10,833 (38.8 %) | **35,323,820 (40.0 %)** |
| realisable | 0 | **0** |

Confidence: **VERIFIED (negative)**. Exhaustive over the stated population,
using the project's own realisability check, with a positive control that fires.

---

## 2. Population covered

`wrapup/corpus88_index.jsonl` indexes **1,575,516** distinct verified 88-gate
mask sets (`CORPUS88.md`; identity = sorted mask multiset, sha256-16). The mask
sets themselves are **not** in the index — it carries hashes and provenance
only — so they were re-streamed from the incarnation sources by
`tools/producer.py`, which **imports `wrapup/tools/corpus88.py` and calls that
module's own readers** (`plats`, `basin_laterals`, `census_pkl`, `bank_jsonl`,
`bank_glob`, `walk_files`) with a drop-in sink. Admission (88 masks, all 32
targets present) and identity (`corpus88.canon`) are corpus88's, unchanged, so
the stream **is** the index population, in a re-ordered but identical set.

The readers were re-ordered so the six bulk banks run first and the
half-million-file `walk_files` tail runs last, so that a prefix of `masks.bin`
would be a complete citable population if the run were cut short. It was not
cut short. Coverage:

| | sets |
|---|---|
| indexed in `corpus88_index.jsonl` | 1,575,516 |
| **streamed and certified** | **1,575,516 (100.00 %)** |
| not reached | **0** |

**The population is not merely the same size as the index, it is the same
set.** The 1,575,516 `canon` ids in `canon.tsv` were sorted and compared against
the 1,575,516 in `corpus88_index.jsonl`:

```
$ comm -3 <(cut -f1 canon.tsv | sort -u) <(jq -r .canon ../../corpus88_index.jsonl | sort -u) | wc -l
0          # only-in-stream 0, only-in-index 0, common 1,575,516
```

`tools/aggregate.py` separately proves the certified index intervals tile
`[0, 1575516)` with **no gap and no overlap** (it exits non-zero otherwise).

Two byproducts, over all 1,575,516 sets:

* `sets_not_32_targets = 0` — every set carries exactly 32 targets and therefore
  exactly **56** deletable non-target masks. `deletions_per_set` came out at
  exactly `56.000000`, an independent set-wise re-confirmation of the `B = 56`
  bookkeeping across **the whole corpus** — 1,575,516 sets, against the 28,796
  that had ever been through even the weaker test.
* `sets_local_allfail = 0` — no set was degenerate (every mask retained at
  least one derivation pair in `inputs ∪ M`).

---

## 3. The test, and why the fast version is the same test

Per mask set `M` and non-target mask `m`, with `A = inputs ∪ M`:

1. **Local necessary condition** (`near87.py` part 2): after deleting `m`, every
   remaining mask must still have at least one derivation pair `{a,b} ⊆ A \ {m}`
   with `a ^ b = x`. Cheap; a filter only.
2. **Full greedy closure** (`corpus88.py:realisable`) on the survivors: start
   from the 32 inputs and repeatedly add any remaining mask that is the XOR of
   two already-available masks. The closure is **order-free and monotone**, so
   it succeeds iff the set is realisable — exact for this question, not a
   heuristic.

`tools/delcert.c` is a literal port. Three port facts make it ~300× faster
without changing the answer:

* Every mask the greedy can ever hold lies in `A`. So
  *"∃ s ∈ avail with x^s ∈ avail"* is exactly *"∃ pair (a,b) with a^b = x and
  a,b ∈ avail"*. The pair lists `P(x)` over `A` — the same `deriv` table
  `near87.py` builds — are computed **once per set** and reused by the filter
  and by all 56 greedy runs. `avail` is a 128-bit bitset.
* `crit(x)` = intersection of the element sets of `x`'s pairs (at most 2
  elements). `m` fails the filter iff `m ∈ crit(x)` for some `x`. This is
  `near87.py`'s condition rearranged, evaluated in `O(Σ|P(x)|)` instead of
  `O(56 · 88)`.
* `near87.py`'s `x != m` guard is **vacuous** and is not ported: `a ^ b = x`
  with `a = x` forces `b = 0`, which is not in `A`, so `x ∉ crit(x)` always.

The port claim is not argued, it is **measured** — see the controls.

---

## 4. Controls (run before the certificate; transcripts in `logs/CONTROLS.txt`)

**(a) Positive control that CAN fail.** `tools/build_controls.py` takes each of
the 498 and plants a redundant mask `e = a ^ b` (`a,b ∈ M`, `e ∉ M ∪ inputs`),
giving an 89-mask realisable set whose deletion of `e` returns the original,
realisable 88. Same binary, same filter, same greedy, only the record length
differs. A `k = 90` variant plants two.

```
ctrl_pos89 : tested 28386, local_pass 10812, realisable 498   (= 1 x 498) FIRES
ctrl_pos90 : tested 28884, local_pass 11218, realisable 996   (= 2 x 498) FIRES
```

Exactly one (resp. two) firing per record, no more and no fewer. The tool can
fire, the local filter does not swallow a real firing, and the count is right.

**(b) Agreement control — reproduce `near87.json` exactly.** The same 498 mask
sets, decoded from the `.plat` rows the way `near87.py` decodes them:

```
ctrl498    : tested 27888, local_pass 10833, realisable 0
ANALYSIS §7: tested 27888, local_pass 10833, realisable 0
```

All three aggregates identical, including the 10,833 local-pass count that no
JSON file records (it appears only in `ANALYSIS_20260829.md` §7 and
`CASE_FOR_88.md`).

**(c) Agreement on corpus records, Python vs C.** Control (b) exercises `.plat`
decodes; this one exercises the JSONL-bank records that make up the corpus.
`tools/pycheck.py` runs `near87.py`'s Python verbatim on `masks.bin` records
0–299:

```
PYTHON  : tested 16800, local_pass 6620, realisable 0   (41.2 s)
delcert : tested 16800, local_pass 6620, realisable 0   ( 0.14 s)
```

---

## 5. The exact commands

```bash
cd /home/joebachir20/xor_ui/slp-plateau-search/wrapup/day2/deletion_cert
gcc -O2 -Wall -o tools/delcert tools/delcert.c
python3 -c "import sys;sys.path.insert(0,'../../..');\
from verify_circuit import mixcolumns_target_masks as t;\
open('targets.txt','w').write('\n'.join('%08x'%m for m in t())+'\n')"

# 1. stream the corpus mask sets  (bulk banks first, loose-.json walk last)
setsid nohup nice -n 19 python3 -u tools/producer.py > logs/producer.log 2>&1 &

# 2. controls
nice -n 19 python3 tools/build_controls.py
nice -n 19 tools/delcert --bin ctrl_atlas498.bin --targets targets.txt --k 88 --tag ctrl498  --every 0
nice -n 19 tools/delcert --bin ctrl_pos89.bin     --targets targets.txt --k 89 --tag ctrlpos89 --every 0
nice -n 19 tools/delcert --bin ctrl_pos90.bin     --targets targets.txt --k 90 --tag ctrlpos90 --every 0
nice -n 19 python3 tools/pycheck.py 0 300

# 3. the certificate, two shards, second one chasing the producer
setsid nohup nice -n 19 tools/delcert --bin masks.bin --targets targets.txt --k 88 \
      --start 0 --count 178000 --tag A --every 20000 --out shardA.jsonl &
setsid nohup nice -n 19 tools/chase.sh 178000 &      # shard B: 178000 -> EOF

# 4. read the verdict (also checks the shard intervals tile [0,N) with no gap)
nice -n 19 python3 tools/aggregate.py
```

Throughput: **2,571 sets/s** per `nice -n 19` thread on this box under load 27
(88 masks, 56 deletions and ~22 full greedy closures per set). The whole corpus
took **612.9 s of CPU — 10.2 minutes** (sum of the `secs` fields of the shard
`DONE` lines). Streaming the mask sets out of the sources cost 1,457.9 s (24.3 min), i.e.
**fetching** the corpus costs more than **certifying** it. LEAD-1 priced this at
"~2 CPU-days in pure Python, minutes in C"; the C figure was right.

---

## 6. Reading the verdict from the banked shards

Everything is banked as it is produced; nothing is held in memory.

| file | what it holds |
|---|---|
| `RESULT.json` | the aggregate — regenerate any time with `python3 tools/aggregate.py` |
| `COVERED.txt` | one line per certified block: `covered <records> <timestamp>` |
| `shardA.jsonl`, `shardB.jsonl` | per-block progress and `DONE` lines |
| `FIRINGS.jsonl` | **created only if something fires** — one JSON object per realisable 87-mask set, carrying the record index, the deleted mask, and all 88 masks |
| `logs/CONTROLS.txt` | the three control transcripts |
| `masks.bin`, `canon.tsv` | the streamed population; line *i* of `canon.tsv` is the `canon`, source and provenance path of record *i* of `masks.bin` |

`masks.bin` (554 MB) and `canon.tsv` (158 MB) are **regenerable** — one
`tools/producer.py` run, 24.3 min — and need not be committed. Everything needed
to re-derive and re-check the certificate is in `tools/` plus the two source
documents; the small files (`CERT.md`, `RESULT.json`, `COVERED.txt`,
`shard*.jsonl`, `logs/`, `targets.txt`, and the three `ctrl_*.bin` fixtures at
under 180 KB each) are the durable record.

**The run completed.** `COVERED.txt` ends with
`PRODUCER DONE, coverage complete at 1575516`, and `RESULT.json` reads
`coverage_pct_of_index: 100.0`, `gaps: []`, `overlaps: []`,
`realisable_87_mask_sets: 0`. `python3 tools/aggregate.py` recomputes every
number in §1 and §2 from the banked shards and re-verifies the tiling; it is the
canonical way to re-read the verdict, and it exits non-zero on any gap.

**A firing would be an 87 by construction.** `FIRINGS.jsonl` carries the full
mask set; `canon.tsv` line *record+1* gives its provenance; the witness is then
an 87-gate circuit obtainable by re-running the greedy closure to recover a
build order and handing the result to `verify_circuit.py`. **No firing
occurred**, and no `STOP` file was created.

---

## 7. What this does and does not close

**Closes.** The single-deletion route out of the known 88 plateau, over the
entire indexed corpus rather than five circuits or 498. `CASE_FOR_88.md` row C3
can be repriced from "27,888 deletions over 498 88s" to
**"88,228,896 deletions over 1,575,516 88s — every distinct verified 88-gate
mask set held on this machine"**. Paste-ready replacement for the C3 row of
`CASE_FOR_88.md`'s route table (line ~1671):

```
| C3 | **Single-mask deletion + arbitrary rewiring** | **88,228,896** deletions over **all 1,575,516** distinct verified 88s (35,323,820 pass the local filter) | **0 realisable** | `wrapup/day2/deletion_cert/CERT.md`; `RESULT.json` |
```

**Does not close.** Two-mask deletion (`88 → 86` plus one new gate), any route
that leaves the mask sets of known 88s, and of course the existence of an 87
unrelated to any known 88. The prior stated in LEAD-1 was low and the outcome
matches it; the value is the size of the population now closed, not surprise.

**The structural reading, at 3,000× the sample.** ANALYSIS §7 observed that a
39 % local pass rate against a 0 % global pass rate separates the deletion
barrier into a *local* component (availability of a re-derivation) and a
*topological* one (ordering / acyclicity), and that the barrier is topological.
That separation now holds at **40.0 % local pass vs 0 % global over 88 million
deletions** — the local obstruction is genuinely weak and genuinely not what
stops an 87, across every corpus and lineage on this machine.
