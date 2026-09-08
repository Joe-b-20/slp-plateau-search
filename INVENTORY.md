# INVENTORY

What exists, how big it is, and how to get the parts that are too large to
host. Nothing here is offered as "available on request" without **either** a
measured size **or** a measured count next to it. Six rows of the request table
carry one and not the other, and each says in words which half is missing: it
was never separately measured.

## What ships in this repository

Counts and sizes below are **content bytes of tracked files**, generated from
`git ls-files` on 2026-09-03. Every tracked file is in exactly one row and the
rows sum to the total, so nothing is unaccounted for. (On-disk usage is larger:
block allocation rounds every small file up.)

| class | count | size | identity |
|---|---:|---:|---|
| lower-bound certificates + checkers (`bounds/`) | 42 files | 715 KB | the matrix is `bounds/matrix.txt`, sha256 `9c337107cba5b0b434fc580ccb1d0323ac51ce17a5fe99da91b97aa8fbc7b620`, pinned by `bounds/matrix.sha256` |
| SAT encodings, instances, controls, proofs (`encodings/`) | 85 files | 27.3 MB | `encodings/SHA256SUMS`, **44 entries**, `sha256sum -c` — re-run by CI |
| corpus-scale results and samples (`corpus/`) | 59 files | 1.5 MB | per-section `RUN.md` + `corpus/sample/SAMPLE.sha256` |
| record and working circuits (`evidence/`) | 598 files | 2.8 MB | `evidence/circuits/spectrum.json` |
| search pipeline and reproduction harness (`pipeline/`, `reproduce/`) | 23 files | 256 KB | provenance per seed file in `pipeline/seeds/README.md` |
| instruments (`tools/`, `scripts/`) | 4 files | 34 KB | standard library, Python 3.6+; 2 programs + their 2 HOW docs |
| figures and their generators (`docs/`) | 4 files | 44 KB | both SVGs regenerate byte-identically from the two scripts beside them |
| unit tests (`tests/`) | 1 file | 23 KB | 35 tests; run by CI |
| CI workflow (`.github/`) | 1 file | 6 KB | `verify.yml` |
| root documents (README, REPRODUCE, NEGATIVES, DEFINITIONS, INVENTORY, METHODS_INDEX, leads, negatives.jsonl, LICENSE, CITATION.cff, verify_circuit.py, .gitignore) | 12 files | 170 KB | `negatives.jsonl` sha256 below |
| **total tracked** | **829 files** | **32.8 MB** | |

Named data files a reader may want to pin:

```
9c337107cba5b0b434fc580ccb1d0323ac51ce17a5fe99da91b97aa8fbc7b620  bounds/matrix.txt                     1 KB
db7e7a5922b49045461fb5bde81b77d07050ad417f833503383648735c221b74  corpus/sample/corpus88_sample.jsonl   640,943 B
3f20018a4a20cf9215a85ded36182d4f0a69b644287b83e0a592dd22cab424b7  corpus/sample/corpus88_sample.bin     183,040 B
169a1ee5283d1462265b6341099af24646155c3699cf43bbcd1dc36f29144a1b  corpus/vocabulary/vocab.json          18,937 B
a6171f30c1b02fe98dc30cd142e2b4d57566a135a1844d5e6911dbf63334b833  negatives.jsonl                       25 rows (7 shipped, 18 not)
```

The six SAT ladder CNFs (k = 9…14) ship in full — 19 MB, 2.0 to 4.3 MB each —
so the decisive instance can be handed to any solver. Three of the four DRAT
refutations ship; k = 11's is 40 MB compressed and is **regenerated instead**
(`cd encodings && sh run_proofs.sh`, 110 s). See `encodings/proofs/README.md`.

## The 88-gate corpus

The headline exhaustive result — 88,228,896 single-gate deletions, 0
realisable — ran over this.

| | count | size | status |
|---|---:|---:|---|
| distinct verified 88-gate **value sets**, canonicalised | **1,575,516** | 554 MB as raw values (`88 × uint32` per record) | **too large to host** |
| provenance index, one row per value set | 1,575,516 | **478,728,370 B** (457 MB), sha256 `acd1cdc811504d33435a8530cf053de9b6ed2ef9c919921e9506f135dd8d1b8a` | **too large to host** |
| canonical-form table | 1,575,516 | 158 MB | too large to host |
| **the shipped sample** | **520** distinct value sets, stratified across 18 lineages, all five published record 88s included | 824 KB | **in this repository**, `corpus/sample/` |
| the certificate's own output, banked | 15 shard intervals tiling `[0, 1575516)` | 12 KB | in this repository, `corpus/deletion_certificate/banked/` |

The sample is drawn deterministically (evenly spaced indices inside each
stratum, no RNG, no seed) and every result in
`corpus/deletion_certificate/` re-runs over it unchanged. Its
`SAMPLE.sha256` pins the full index it was drawn from, so the draw is
auditable by anyone who obtains that index.

**Three counts, kept deliberately distinct because they count different
things.** Quoting any of them as another is the single easiest mistake to make
about this corpus:

| number | what it counts | which checks it supports |
|---:|---|---|
| **1,575,516** | distinct 88-gate **value sets**, canonicalised — the corpus index above | set-level checks only: value distinctness and the 32 targets, and the 88,228,896-deletion certificate, both of which need nothing but the value set |
| **28,796** | of those, the ones carrying a **complete build order**, gate by gate | everything the value sets support, **plus** every structural test that needs the wiring — including `B`, which cannot be computed from a value set at all |
| **17,283** | **circuit files on disk** at the census, the file-level population the tripwire was swept over (the count `leads.md` #1 quotes) | the complete tripwire screen, file by file |

No one of these is another, and none of them counts *circuits proved distinct
as circuits*: 1,575,516 counts value sets, and many circuits can share one.

## The re-census the vocabulary came from

| | |
|---:|---|
| circuit rows accepted (88 values, all 32 targets) | **1,925,065** |
| rows rejected, wrong length | 257,291 |
| non-target gate slots examined | **107,803,640** |
| distinct non-target values — *the vocabulary* | **1,778** |

The vocabulary itself, the per-value statistics, and a verified 89-gate circuit
using six values that appear in **none** of those 107.8 million slots all ship
in `corpus/vocabulary/` (64 KB).

## Held locally, available on request

A long search campaign produced far more than a repository should carry. Sizes
are measured, not estimated. Ask by opening an issue naming the class you want;
individual files and filtered extracts are easy to send, whole classes are not.

| class | count | size |
|---|---:|---:|
| oracle-checkable exported circuit records | **1,549,319** (1,530,095 of them 88-gate, including 167 at depth 5) | 1.8 GB of manifests |
| the same, as individual circuit files | 1,251,130 files | 1.1 GB apparent, 6.7 GB on disk |
| distinct gauge orbits over the known 88 population | **33,010** | *size not separately measured* (orbit representatives, held inside the larger ledger archives below) |
| search-engine telemetry (each row a bit-exact replay tuple) | 127 archives | **31.4 GB** |
| population harvest, compressed ~150:1, nothing pruned | 1,083 segments | 337 MB (≈50 GB raw) |
| population harvest dumps, uncompressed | 130 files | 13.71 GB |
| ledgers, labels, worklists, window banks | 566 files | 3.48 GB |
| CNF dumps from the search campaign | *not separately counted* | **5.53 GB** |
| packed state pools (`.bin`) | *not separately counted* | **1.51 GB** |
| regenerable solver instance files | *not separately counted*; regenerable from the shipped encoder, so the count is not the useful number | **967 MB** |
| raw run logs | **~9,793** files | **~3.8 GB** (3.4 GB of it one campaign's logs, ~1.7 GB byte-identical duplicate pairs) |
| append-only result ledgers, several hash-chained | **161** | *size not separately measured*; counted inside the 3.48 GB ledger row above |
| write-ups: per-run results, review reports, a 244-row audit with 22 registered defects, a full paper draft, a 12-item retraction ledger | **774** | *size not separately measured*; Markdown, a few MB in total |

Certificate classes behind the rows of `NEGATIVES.md`, held in the same place:
≈**165 million** exact window decisions (zero timeouts, zero reducible);
**29,125** order-free window UNSAT certificates — the only certificate class
here with no slot-order caveat — and 82,786 down-step window UNSATs; **749,150**
exact optimisation runs returning OPTIMAL; **47,948** solved 8-dimensional
sector instances with replayable witnesses; **333,396** states across eight
exhaustively closed components; **57** gate levels proved UNSAT that had never
been tested at that level before.

## What is *not* held

No circuit smaller than 88 gates was ever found, in any of the above. The files
whose names claim 87 gates are four deliberate tripwire fakes, and every one of
them was rejected by the export path — that is what they are for.

Every artifact above is oracle-checkable with `verify_circuit.py` in this
repository. Where a class is offered on request, the request is answered with
the files and the command that checks them, not with a summary.
