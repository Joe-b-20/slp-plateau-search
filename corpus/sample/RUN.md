# RUN — the corpus sample

A shippable, documented sample of the 88-gate MixColumns mask corpus:
**520 distinct verified 88-gate mask sets**, drawn across every lineage the
corpus holds, including all five published record 88s.

The full corpus is 1,575,516 distinct mask sets — 554 MB as raw masks, with a
478 MB provenance index. Neither ships. This does, and every result in
`../deletion_certificate/` re-runs over it unchanged.

---

## What a row looks like

`corpus88_sample.jsonl`, one JSON object per line:

```json
{"canon": "…16 hex…",
 "source": "atlas_corner_jean",
 "lineage": "atlas corner enumeration seeded from the independently-authored (foreign-lineage) published 88",
 "n_masks_distinct": 88,
 "n_targets_present": 32,
 "masks": ["01018180", "02028381", …88 of them…]}
```

Rows drawn from the five published record circuits carry an extra
`"record_circuit"` field naming which one.

`corpus88_sample.bin` carries the same masks as `88 × uint32` little-endian per
record, sorted ascending, in the same row order — the format the C certificate
tool reads.

**Identity.** `canon` is the project's standard circuit identity: the sorted
multiset of gate output masks, hashed.

```
canon = sha256(",".join("%08x" % m for m in sorted(masks))).hexdigest()[:16]
```

Two circuits with the same `canon` compute the same 88 values, whatever build
order they were found in. Every row of this sample has a distinct `canon`.

---

## RE-RUN — check every sampled set

Standard library Python 3, no arguments, nothing outside this pack. It rebuilds
the 32 MixColumns target masks from GF(2^8) arithmetic and re-checks all 520
rows: 88 distinct masks, all 32 targets present, `canon` matches the masks, and
the `.jsonl` and `.bin` agree bit for bit.

```
$ nice -n 19 python3 tools/check_sample.py
MixColumns target masks rebuilt from GF(2^8) mod 0x11B: 32 masks, weight profile 20x5 + 12x7  [OK]

checked 520 rows: 520 distinct mask sets, each 88 distinct masks with all 32 targets
failures: 0

stratum composition
  nrpa                    100
  merged_engine            60
  census                   59
  oracle_worklist          50
  deep_hunt                50
  atlas_corner             40
  atlas_corner_jean        40
  oracle_misc              30
  basin_lateral            20
  layer89_descent          20
  campaign_misc            20
  fleet_late               10
  atlas_misc                6
  published_record          5
  experiment_readd          5
  fleet_mid                 2
  experiment_plateau        2
  fleet_early               1
  TOTAL                   520

the five published record 88s are present:
  mixcolumns_88gates_depth5
  mixcolumns_88gates_depth5_fromscratch
  mixcolumns_88gates_depth6
  mixcolumns_88gates_depth7
  mixcolumns_88gates_depth8

file hashes
  db7e7a5922b49045461fb5bde81b77d07050ad417f833503383648735c221b74  corpus88_sample.jsonl
  3f20018a4a20cf9215a85ded36182d4f0a69b644287b83e0a592dd22cab424b7  corpus88_sample.bin

VERDICT: ALL ROWS PASS
```

**Measured 2026-09-01: 0.04 s wall.** Transcript: `out/CHECK.txt`.

Every row was re-checked the same way at build time, before it was written.

---

## Composition, and why these strata

The corpus is not a uniform population; it is the union of everything a long
campaign produced. The sample is **stratified, not proportional** — a
proportional draw would be 87 % one search method and would tell you nothing
about the rest. Small and structurally interesting lineages are deliberately
over-represented relative to their corpus share.

| stratum | n | what it is |
|---|---:|---|
| `nrpa` | 100 | nested rollout policy adaptation search, sub-92 pool |
| `merged_engine` | 60 | merged multi-heuristic engine hunt populations |
| `census` | 59 | exhaustive-population census of 88s at fixed depth |
| `oracle_worklist` | 50 | SAT/oracle-driven worklist descent to 88 |
| `deep_hunt` | 50 | deep-hunt 88 population |
| `atlas_corner` | 40 | atlas corner enumeration, own-lineage seeds |
| `atlas_corner_jean` | 40 | atlas corner enumeration seeded from the **independently-authored** published 88 |
| `oracle_misc` | 30 | assorted oracle-guided descent runs |
| `basin_lateral` | 20 | lateral moves inside a basin around a known 88 |
| `layer89_descent` | 20 | 88s found by descending from an 89-gate layer |
| `campaign_misc` | 20 | assorted search-campaign outputs |
| `fleet_late` | 10 | late-wave distributed fleet runs |
| `atlas_misc` | 6 | assorted atlas ladder/ring outputs |
| `published_record` | 5 | **the five published record 88-gate circuits** |
| `experiment_readd` | 5 | gate re-addition experiment |
| `fleet_mid` | 2 | mid-wave distributed fleet runs |
| `experiment_plateau` | 2 | plateau-87 experiment outputs |
| `fleet_early` | 1 | early-wave distributed fleet runs |
| **total** | **520** | |

Three things worth reading off this table:

* **The foreign lineage is in.** `atlas_corner_jean` is 40 sets descending from
  the one published 88 this project did not produce. Any claim of the form
  "every 88 we can find has property P" is worth much less if every 88 shares
  an ancestor; these do not.
* **The published records are in.** All five are present, and — a fact worth
  stating — all five were already in the corpus from the search banks before the
  published files were read. The published circuits are not a separate
  population; the search rediscovered them.
* **`census` is 59, not the 60 requested.** One census pick collided with a
  published record 88 (they are the same mask set), and the sample keeps one
  row per distinct `canon`. That collision is real corpus structure, not a
  build error.

---

## Provenance

`SAMPLE.sha256`:

```
db7e7a5922b49045461fb5bde81b77d07050ad417f833503383648735c221b74  corpus88_sample.jsonl
3f20018a4a20cf9215a85ded36182d4f0a69b644287b83e0a592dd22cab424b7  corpus88_sample.bin
# The FULL index this sample was drawn from -- NOT shipped, 478728370 bytes.
# Commented out so `sha256sum -c SAMPLE.sha256` passes clean on what does ship;
# uncomment the line below if you obtain the index, to audit the draw.
# acd1cdc811504d33435a8530cf053de9b6ed2ef9c919921e9506f135dd8d1b8a  corpus88_index.jsonl
```

```
cd corpus/sample && sha256sum -c SAMPLE.sha256
# corpus88_sample.jsonl: OK
# corpus88_sample.bin: OK
```

The commented third hash pins the exact full index this sample was drawn from,
so the draw can be audited by anyone who obtains it. It is a comment rather
than a live entry because `sha256sum -c` cannot open a file that does not ship,
and a manifest that always reports a failure teaches a reader to ignore it.

---

## How the draw was made

`tools/build_sample.py` is the build script. It is shipped as the provenance
record, not as a public entry point — it reads the two large intermediates of
the full-corpus run, which do not ship.

The selection is **deterministic: evenly spaced indices inside each stratum, no
RNG, no seed**. Anyone who regenerates the intermediates regenerates this exact
sample. Every drawn row is re-checked (88 distinct masks, all 32 targets, canon
agreement) before it is written, and the build asserts on any failure.

```
$ nice -n 19 python3 tools/build_sample.py <masks.bin> <canon.tsv> <corpus_index.jsonl> <record_circuits_dir>
```

**Measured 2026-09-01: 5.4 s wall, 188 MB peak RSS.**

---

## Files

| path | what it is |
|---|---|
| `corpus88_sample.jsonl` | the sample: 520 rows, masks + source label + lineage |
| `corpus88_sample.bin` | the same masks, 88 × uint32 LE per record |
| `SAMPLE.sha256` | hashes of both, plus of the full index it was drawn from |
| `tools/check_sample.py` | **re-checks every row; needs nothing but this pack** |
| `tools/build_sample.py` | the build script, for provenance |
| `out/CHECK.txt` | transcript of the 2026-09-01 re-run |
