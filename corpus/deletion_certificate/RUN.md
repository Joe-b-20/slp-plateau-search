# RUN — deletion certificate

Every command below is run **from this directory** (`deletion_certificate/`).
All outputs pasted here are real, captured on the dates shown, `nice -n 19`,
at most two threads.

Requirements: a C compiler and Python 3 (standard library only). No solver, no
third-party packages.

---

## 0. Build

```
$ gcc -O2 -Wall -o tools/delcert tools/delcert.c
```

Silent on success. **Measured 2026-09-01: 0.4 s.**

---

## 1. RE-RUN — the positive control (the instrument must be able to fire)

A `0` from a tool that cannot return anything else is worthless. These fixtures
are 498 mask sets each carrying one (`k=89`) or two (`k=90`) **planted**
redundant masks whose deletion provably returns a realisable set. The tool must
find exactly that many and no more.

```
$ nice -n 19 tools/delcert --bin fixtures/ctrl_pos89.bin --targets targets.txt --k 89 --tag ctrlpos89 --every 0
{"DONE":1,"shard":"ctrlpos89","start":0,"count":498,"done":498,"tested":28386,"local_pass":10812,"realisable":498,"sets_not_32_targets":0,"sets_local_allfail":0,"secs":0.0}

$ nice -n 19 tools/delcert --bin fixtures/ctrl_pos90.bin --targets targets.txt --k 90 --tag ctrlpos90 --every 0
{"DONE":1,"shard":"ctrlpos90","start":0,"count":498,"done":498,"tested":28884,"local_pass":11218,"realisable":996,"sets_not_32_targets":0,"sets_local_allfail":0,"secs":0.0}
```

(The `FIRING` lines — 498 and 996 of them — are written to stdout too and are
elided above.)

**PASS condition:** `realisable` is exactly `498` and exactly `996` — one and
two planted deletions per record, no more, no fewer.

**Measured 2026-09-01: 0.04 s wall each.** Historical: 0.1 s and 4.1 s CPU.

### The negative half of the same control

The same binary on the same 498 mask sets *without* the planted masks must
return 0, and must reproduce an independently recorded local-pass count of
10,833 that appears in no machine-generated file:

```
$ nice -n 19 tools/delcert --bin fixtures/ctrl_neg498.bin --targets targets.txt --k 88 --tag ctrl498 --every 0
{"DONE":1,"shard":"ctrl498","start":0,"count":498,"done":498,"tested":27888,"local_pass":10833,"realisable":0,"sets_not_32_targets":0,"sets_local_allfail":0,"secs":0.0}
```

**Measured 2026-09-01: 0.03 s wall.** Full transcript: `out/CONTROLS_rerun.txt`.

---

## 2. RE-RUN — the certificate over the shipped sample

The full corpus (554 MB of mask sets) does not ship. The 520-set sample in
`../sample/` does, and the certificate runs over it unchanged:

```
$ nice -n 19 tools/delcert --bin ../sample/corpus88_sample.bin --targets targets.txt --k 88 --tag sample --every 0
{"DONE":1,"shard":"sample","start":0,"count":520,"done":520,"tested":29120,"local_pass":11875,"realisable":0,"sets_not_32_targets":0,"sets_local_allfail":0,"secs":0.0}
```

**Measured 2026-09-01: 0.03 s wall.**

Read it as: 520 mask sets × 56 non-target masks = **29,120 candidate 87-mask
sets**, 11,875 (40.8 %) survive the cheap local filter, **0** survive the full
greedy closure. The local-pass rate matches the full corpus's 40.0 %.

---

## 3. RE-RUN — Python vs C agreement on the same records

`tools/pycheck.py` carries the original Python — the local necessary condition
and the greedy closure — transcribed verbatim, importing nothing from the
project. A ~300× port is worth nothing unless it is diffed against what it
ports, so run both on the same slice and compare all three aggregates:

```
$ nice -n 19 python3 tools/pycheck.py ../sample/corpus88_sample.bin 0 520
{"PYTHON":1,"start":0,"count":520,"tested":29120,"local_pass":11875,"realisable":0,"secs":6.1}

$ nice -n 19 tools/delcert --bin ../sample/corpus88_sample.bin --targets targets.txt --k 88 --tag sample --every 0
{"DONE":1,"shard":"sample","start":0,"count":520,"done":520,"tested":29120,"local_pass":11875,"realisable":0,"sets_not_32_targets":0,"sets_local_allfail":0,"secs":0.0}
```

**PASS condition:** `tested`, `local_pass` and `realisable` identical.
They are: 29,120 / 11,875 / 0 on both.

**Measured 2026-09-01: 6.1 s (Python) vs 0.0 s (C)** on this
slice — the C tool is below the timer's resolution. Full transcript:
`out/AGREEMENT_sample.txt`. Historically the same
control was run on 300 corpus records: 41.2 s vs 0.14 s, both 16,800 / 6,620 / 0.

---

## 4. RE-RUN — re-derive the full-corpus verdict from the banked shards

The full run's per-block output is banked in `banked/`. This recomputes every
headline number in `CERT.md` from those shards and **proves the certified index
intervals tile `[0, 1575516)` with no gap and no overlap** — the tiling is what
the "100 % of the corpus" claim rests on. It exits non-zero on any gap.

```
$ nice -n 19 python3 tools/aggregate.py
{
 "intervals": 15,
 "covered_contiguous_prefix": 1575516,
 "gaps": [],
 "overlaps": [],
 "rows_in_corpus_index": 1575516,
 "coverage_pct_of_index": 100.0,
 "deletions_tested": 88228896,
 "local_filter_pass": 35323820,
 "local_filter_pass_pct": 40.04,
 "realisable_87_mask_sets": 0,
 "n_FIRING_lines": 0,
 "sets_not_32_targets": 0,
 "sets_local_allfail": 0,
 "deletions_per_set": 56.0
}

OK: the certified intervals tile [0, 1575516) with no gap and no overlap.
```

**Measured 2026-09-01: 0.05 s wall.** Output: `out/AGGREGATE.txt`.

Note `deletions_per_set: 56.0` — exactly 56, over 1,575,516 sets. That is an
independent set-wise re-confirmation of the `B = 56` bookkeeping across the
whole corpus.

---

## 5. FULL SCALE — the commands that produced the banked result

These need the search-campaign source banks (~40 GB of raw run output), which
are not part of this pack, and a `tools/sources.json` naming where they live
(see `tools/sources.example.json`). They are recorded so the full-scale run
is reproducible by anyone holding the sources.

```
# 1. stream every distinct 88-gate mask set out of the sources
#    -> masks.bin (554 MB), canon.tsv (158 MB)
$ CORPUS_ROOT=<tree> CORPUS_OUT=<dir> CORPUS_SOURCES=tools/sources.json \
      nice -n 19 python3 tools/producer.py

# 2. the certificate, two shards, the second chasing the producer
$ nice -n 19 tools/delcert --bin masks.bin --targets targets.txt --k 88 \
      --start 0 --count 178000 --tag A --every 20000 --out shardA.jsonl
$ nice -n 19 tools/delcert --bin masks.bin --targets targets.txt --k 88 \
      --start 178000 --tag B --every 20000 --out shardB.jsonl

# 3. read the verdict (also proves the shard intervals tile [0,N))
$ nice -n 19 python3 tools/aggregate.py
```

**Historical cost, from the run logs:**

| stage | cost |
|---|---|
| producer (streaming 1,575,516 mask sets out of the sources) | **1,457.9 s = 24.3 min** |
| certificate (88,228,896 deletions, 2 shards) | **612.9 s CPU = 10.2 min** |
| throughput | **2,571 sets/s** per `nice -n 19` thread |

Fetching the corpus costs more than certifying it.

**Banked result** (`banked/RESULT.json`, reproduced by step 4 above):

> 1,575,516 mask sets, 100.00 % of the index, **88,228,896 deletions tested,
> 35,323,820 pass the local filter, 0 realisable**, 0 firings, 0 gaps,
> 0 overlaps, 56.000000 deletions per set.

---

## Files

| path | what it is |
|---|---|
| `CERT.md` | the certificate statement, method, controls and scope |
| `tools/delcert.c` | the C tool; a literal port of the two Python checks |
| `tools/pycheck.py` | the original Python, verbatim, for the agreement control |
| `tools/aggregate.py` | re-derives the verdict and proves the interval tiling |
| `tools/producer.py` | reference copy of the full-corpus streamer (needs the sources) |
| `tools/sources.example.json` | the source-bank paths the streamer needs, as a template |
| `targets.txt` | the 32 MixColumns target masks, hex, one per line |
| `fixtures/ctrl_pos89.bin`, `ctrl_pos90.bin` | positive controls; must fire 498 / 996 |
| `fixtures/ctrl_neg498.bin` | negative control; must return 0 with local_pass 10833 |
| `banked/` | the full-corpus run's own output: result, coverage, shards, controls |
| `out/` | transcripts of the 2026-09-01 re-runs above |
