# INVENTORY

What exists, how big it is, and how to get the parts that are too large to
host. Nothing here is offered as "available on request" without a size and a
count next to it.

## What ships in this repository

| class | count | size | identity |
|---|---:|---:|---|
| lower-bound certificates + checkers (`bounds/`) | 38 files | 788 KB | the matrix is `bounds/matrix.txt`, sha256 `9c337107cba5b0b434fc580ccb1d0323ac51ce17a5fe99da91b97aa8fbc7b620` |
| SAT encodings, instances, controls, proofs (`encodings/`) | 82 files | 28 MB | `encodings/SHA256SUMS`, 41 entries, `sha256sum -c` |
| corpus-scale results and samples (`corpus/`) | 56 files | 1.7 MB | per-section `RUN.md` + `SAMPLE.sha256` |
| record and working circuits (`evidence/`) | 598 files | 4.7 MB | `evidence/circuits/spectrum.json` |
| search pipeline and reproduction harness | 20 files | 248 KB | — |
| instruments (`tools/tripwire.py`, `scripts/overlap.py`) | 2 files | 40 KB | standard library, Python 3.6+ |

Named data files a reader may want to pin:

```
9c337107cba5b0b434fc580ccb1d0323ac51ce17a5fe99da91b97aa8fbc7b620  bounds/matrix.txt                     1 KB
db7e7a5922b49045461fb5bde81b77d07050ad417f833503383648735c221b74  corpus/sample/corpus88_sample.jsonl   640,943 B
3f20018a4a20cf9215a85ded36182d4f0a69b644287b83e0a592dd22cab424b7  corpus/sample/corpus88_sample.bin     183,040 B
169a1ee5283d1462265b6341099af24646155c3699cf43bbcd1dc36f29144a1b  corpus/vocabulary/vocab.json          18,937 B
69639f9be8864aa9142ff49775881dbaa33ac8119cb68bf2e9296a9164161e0a  negatives.jsonl                       25 rows
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
| distinct 88-gate mask sets, canonicalised | **1,575,516** | 554 MB as raw masks (`88 × uint32` per record) | **too large to host** |
| provenance index, one row per mask set | 1,575,516 | **478,728,370 B** (457 MB), sha256 `acd1cdc811504d33435a8530cf053de9b6ed2ef9c919921e9506f135dd8d1b8a` | **too large to host** |
| canonical-form table | 1,575,516 | 158 MB | too large to host |
| **the shipped sample** | **520** distinct mask sets, stratified across 18 lineages, all five published record 88s included | 824 KB | **in this repository**, `corpus/sample/` |
| the certificate's own output, banked | 15 shard intervals tiling `[0, 1575516)` | 12 KB | in this repository, `corpus/deletion_certificate/banked/` |

The sample is drawn deterministically (evenly spaced indices inside each
stratum, no RNG, no seed) and every result in
`corpus/deletion_certificate/` re-runs over it unchanged. Its
`SAMPLE.sha256` pins the full index it was drawn from, so the draw is
auditable by anyone who obtains that index.

Two further counts, kept deliberately distinct because they count different
things: **1,575,516** mask sets were collected and pass set-level checks;
**28,796** of them carry complete build recipes and were put through the full
structural test. Neither number is the other.

## The re-census the vocabulary came from

| | |
|---:|---|
| circuit rows accepted (88 masks, all 32 targets) | **1,925,065** |
| rows rejected, wrong length | 257,291 |
| non-target gate slots examined | **107,803,640** |
| distinct non-target masks — *the vocabulary* | **1,778** |

The vocabulary itself, the per-mask statistics, and a verified 89-gate circuit
using six masks that appear in **none** of those 107.8 million slots all ship
in `corpus/vocabulary/` (64 KB).

## Held locally, available on request

A long search campaign produced far more than a repository should carry. Sizes
are measured, not estimated. Ask by opening an issue naming the class you want;
individual files and filtered extracts are easy to send, whole classes are not.

| class | count | size |
|---|---:|---:|
| oracle-checkable exported circuit records | **1,549,319** (1,530,095 of them 88-gate, including 167 at depth 5) | 1.8 GB of manifests |
| the same, as individual circuit files | 1,251,130 files | 1.1 GB apparent, 6.7 GB on disk |
| distinct gauge orbits over the known 88 population | **33,010** | — |
| search-engine telemetry (each row a bit-exact replay tuple) | 127 archives | **31.4 GB** |
| population harvest, compressed ~150:1, nothing pruned | 1,083 segments | 337 MB (≈50 GB raw) |
| population harvest dumps, uncompressed | 130 files | 13.71 GB |
| ledgers, labels, worklists, window banks | 566 files | 3.48 GB |
| CNF dumps from the search campaign | — | 5.53 GB |
| packed state pools (`.bin`) | — | 1.51 GB |
| regenerable solver instance files | — | 967 MB |
| raw run logs | **~9,793** files | **~3.8 GB** (3.4 GB of it one campaign's logs, ~1.7 GB byte-identical duplicate pairs) |
| append-only result ledgers, several hash-chained | **161** | — |
| write-ups: per-lane results, referee reports, a 244-row audit with 22 registered defects, a full paper draft, a 12-item retraction ledger | **774** | — |

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
