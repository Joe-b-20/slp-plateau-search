# The corpus-wide single-gate deletion certificate

## 1. The statement

> **THE CERTIFICATE.** Let `M` be any of the **1,575,516** distinct verified
> 88-gate MixColumns mask sets in the corpus — the corpus **entire** — and let
> `m` be any of its 56 non-target masks. Then `M \ {m}` — an 87-mask set that
> still contains all 32 MixColumns target masks — is **not realisable as an
> XOR straight-line program over the 32 inputs**.
> **88,228,896 / 88,228,896 candidate 87-mask sets closed, machine-checked,
> 0 realisable.**

Equivalently: **no 87-gate MixColumns circuit is obtainable from any of
1,575,516 distinct known 88-gate circuits by deleting one gate, even with
unrestricted rewiring of the surviving 87 masks.**

This is strictly stronger than the `B = 56` tripwire (see `../tripwire_demo/`),
which only asks whether a middle gate has *a consumer*. It does not ask whether
that consumer has an **alternative derivation** in the remainder. This does, and
it allows the remaining 87 masks to be rebuilt in any order whatsoever.

| | earlier result | this certificate |
|---|---|---|
| mask sets under the deletion test | 498 | **1,575,516 (100 % of the corpus)** |
| candidate 87-mask sets closed | 27,888 | **88,228,896** |
| pass the local necessary condition | 10,833 (38.8 %) | **35,323,820 (40.0 %)** |
| realisable | 0 | **0** |

Confidence: **VERIFIED (negative)**. Exhaustive over the stated population,
using the project's own realisability check, with a positive control that fires.

---

## 2. Population covered

The corpus index holds **1,575,516** distinct verified 88-gate mask sets.
Identity is the sorted mask multiset, hashed: `canon = sha256(",".join("%08x" %
m for m in sorted(masks)))[:16]`. Admission requires exactly 88 masks with all
32 MixColumns target masks present among them.

The index carries hashes and provenance only, not the mask sets themselves, so
the sets were re-streamed from their sources by `tools/producer.py`, which
imports the corpus consolidator and calls **that module's own readers** with a
drop-in sink. Admission and identity are the consolidator's, unchanged, so the
stream **is** the index population — a re-ordered but identical set.

| | sets |
|---|---|
| indexed in the corpus index | 1,575,516 |
| **streamed and certified** | **1,575,516 (100.00 %)** |
| not reached | **0** |

**The population is not merely the same size as the index, it is the same
set.** The 1,575,516 `canon` ids in the streamed provenance table were sorted
and compared against the 1,575,516 in the corpus index; the symmetric
difference was empty — only-in-stream 0, only-in-index 0, common 1,575,516.
`tools/aggregate.py` separately proves the certified index intervals tile
`[0, 1575516)` with **no gap and no overlap** (it exits non-zero otherwise).

Two byproducts, over all 1,575,516 sets:

* `sets_not_32_targets = 0` — every set carries exactly 32 targets and therefore
  exactly **56** deletable non-target masks. `deletions_per_set` came out at
  exactly `56.000000`: an independent, set-wise re-confirmation of the `B = 56`
  bookkeeping across the whole corpus.
* `sets_local_allfail = 0` — no set was degenerate; every mask retained at least
  one derivation pair.

---

## 3. The test, and why the fast version is the same test

Per mask set `M` and non-target mask `m`, with `A = inputs ∪ M`:

1. **Local necessary condition.** After deleting `m`, every remaining mask must
   still have at least one derivation pair `{a,b} ⊆ A \ {m}` with `a ^ b = x`.
   Cheap; a filter only.
2. **Full greedy closure.** On the survivors: start from the 32 inputs and
   repeatedly add any remaining mask that is the XOR of two already-available
   masks. The closure is **order-free and monotone**, so it succeeds iff the set
   is realisable — exact for this question, not a heuristic.

`tools/delcert.c` is a literal port of both. Three port facts make it ~300×
faster without changing the answer:

* Every mask the greedy can ever hold lies in `A`. So *"∃ s ∈ avail with
  x^s ∈ avail"* is exactly *"∃ pair (a,b) with a^b = x and a,b ∈ avail"*. The
  pair lists `P(x)` over `A` are computed **once per set** and reused by the
  filter and by all 56 greedy runs. `avail` is a 128-bit bitset.
* `crit(x)` = intersection of the element sets of `x`'s pairs (at most 2
  elements). `m` fails the filter iff `m ∈ crit(x)` for some `x` — the same
  condition rearranged, evaluated in `O(Σ|P(x)|)` instead of `O(56 · 88)`.
* The Python's `x != m` guard is **vacuous** and is not ported: `a ^ b = x` with
  `a = x` forces `b = 0`, which is not in `A`, so `x ∉ crit(x)` always.

The port claim is not argued, it is **measured** — see the controls, which
include the original Python run against the C on the same records.

---

## 4. Controls

An instrument that cannot fire is not evidence. All three controls are
re-runnable from this pack in under a second; see `RUN.md`.

**(a) Positive control that CAN fail.** Each of 498 mask sets gets a redundant
mask `e = a ^ b` planted (`a,b ∈ M`, `e ∉ M ∪ inputs`), giving an 89-mask
realisable set whose deletion of `e` returns the original, realisable 88. Same
binary, same filter, same greedy — only the record length differs. A `k = 90`
variant plants two.

```
ctrl_pos89 : tested 28386, local_pass 10812, realisable 498   (= 1 x 498) FIRES
ctrl_pos90 : tested 28884, local_pass 11218, realisable 996   (= 2 x 498) FIRES
```

Exactly one (resp. two) firing per record, no more and no fewer. The tool can
fire, the local filter does not swallow a real firing, and the count is right.

**(b) Agreement control against the earlier 498-set result.** The same 498 mask
sets, decoded from their original source rows:

```
ctrl498    : tested 27888, local_pass 10833, realisable 0
expected   : tested 27888, local_pass 10833, realisable 0
```

All three aggregates identical, including the 10,833 local-pass count.

**(c) Agreement on corpus records, Python vs C.** Control (b) exercises one
decode path; this one exercises the bulk records that make up the corpus.
`tools/pycheck.py` carries the original Python — the local condition and the
greedy closure — transcribed verbatim, with no import from the project, and
prints the same three aggregates. Run over the shipped 520-set sample:

```
PYTHON  : tested 29120, local_pass 11875, realisable 0   (14.2 s)
delcert : tested 29120, local_pass 11875, realisable 0   ( 0.1 s)
```

---

## 5. Cost

Throughput: **2,571 sets/s** per `nice -n 19` thread (88 masks, 56 deletions and
~22 full greedy closures per set). The whole corpus took **612.9 s of CPU —
10.2 minutes**. Streaming the mask sets out of their sources cost 1,457.9 s
(24.3 min): **fetching** the corpus costs more than **certifying** it.

---

## 6. Reading the verdict

Everything is banked as it is produced; nothing is held in memory. The banked
full-corpus record is in `banked/`:

| file | what it holds |
|---|---|
| `banked/RESULT.json` | the aggregate; regenerate with `tools/aggregate.py` |
| `banked/COVERED.txt` | one line per certified block |
| `banked/shardA.jsonl`, `banked/shardB.jsonl` | per-block progress and `DONE` lines |
| `banked/producer_stats.json` | per-source admission counts for the stream |
| `banked/CONTROLS.txt` | the original control transcripts |

`FIRINGS.jsonl` is **created only if something fires** — one JSON object per
realisable 87-mask set, carrying the record index, the deleted mask, and all 88
masks. **No firing occurred**, and `n_FIRING_lines` in `RESULT.json` is 0.

**A firing would be an 87 by construction.** The full mask set is banked; the
witness is then an 87-gate circuit obtained by re-running the greedy closure to
recover a build order and handing the result to the verifier.

The two large intermediates — the streamed mask file (554 MB) and its
provenance table (158 MB) — are **regenerable in one 24-minute producer run**
and do not ship. What ships instead is a documented 520-set sample of the same
population (`../sample/`), over which the certificate re-runs in 0.1 s.

---

## 7. What this does and does not close

**Closes.** The single-deletion route out of the known 88 plateau, over the
entire corpus rather than five circuits or 498: **88,228,896 deletions over
1,575,516 distinct verified 88s, 0 realisable.**

**Does not close.** Two-mask deletion (`88 → 86` plus one new gate); any route
that leaves the mask sets of known 88s; and of course the existence of an 87
unrelated to any known 88. The prior on this firing was low and the outcome
matches it — the value is the size of the population now closed, not surprise.

**The structural reading.** A 40.0 % local pass rate against a 0 % global pass
rate separates the deletion barrier into a *local* component (availability of a
re-derivation) and a *topological* one (ordering / acyclicity), and says the
barrier is **topological**. That separation now holds over 88 million deletions,
across every corpus and lineage held: the local obstruction is genuinely weak
and genuinely not what stops an 87.

**What it is not.** This is a statement about the *known* 88s. It is not a lower
bound. The honest bracket on the MixColumns XOR complexity remains
`56 ≤ L(M) ≤ 88`.
