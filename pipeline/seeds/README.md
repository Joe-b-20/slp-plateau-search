# seeds — warm-start circuits for the fixed-mode worker sets

Every file is an index-pair circuit (`{"gateCount", "gates": [[a,b],...]}`) plus
a `provenance` field. All nine were re-verified with the standalone oracle
before being committed:

```
cd ..            # pipeline/
for f in seeds/*.json; do python3 ../verify_circuit.py "$f"; done
```

**Provenance is per file, and the table below is the authority.** Three classes
(`../../METHODS.md` §9): our own lineage; published work, imported and credited;
and our search output whose *lineage passes through* published work. Of the nine
files, two are imported and three are derived. Anything a worker produces
inherits the status of its seed.

| file | gates @ depth | provenance |
|---|---|---|
| `seed_88_at_depth7_ours.json` | 88 @ 7 | **ours, own lineage, no imported material** — found by this pipeline (campaign 87, worker `w10_sym94`) from our own ρ²-symmetric 94, itself from our 89@5. Independent of Jean's 88 (Jaccard 0.530). Matches the published record with a different circuit; does not beat it. |
| `seed_88_at_depth8_thirdfamily.json` | 88 @ 8 | found by this pipeline, but **DERIVED — its lineage passes through Jean's circuit** (its seed is the ρ²-symmetric 90@9 below). A third distinct 88-gate family (J 0.455 / 0.544 to the other two); dominated by 88@7, kept as a distinct construction. |
| `seed_88_at_depth7_jean_imported.json` | 88 @ 7* | **IMPORTED** — Jean, ePrint 2026/1481, Algorithm 1. Not our result. *The paper states no depth; the 7 is our oracle's measurement of our transcription. |
| `seed_89_sunyangli_imported.json` | 89 @ 9* | **IMPORTED** — Sun–Yang–Li, ePrint 2025/1493, Table 4. Not our result. *The paper states no depth; the 9 is our oracle's measurement of our transcription. |
| `seed_89_at_depth5.json` | 89 @ 5 | **ours, own lineage** — the project's depth-5 record circuit (lineage in `../../evidence/RESULTS.md`). |
| `seed_89_at_depth6.json` | 89 @ 6 | **ours, own lineage** — the frontier circuit the historic sub-89 run started from. |
| `seed_90_at_depth5.json` | 90 @ 5 | **ours, own lineage** — the depth-5 circuit the historic sub-89 run's capped worker started from. |
| `seed_90_at_depth7_rho2sym_basin2.json` | 90 @ 7 | exactly ρ²-symmetric (basin 2); with basin 1 the best exactly symmetric circuits we know of (previous best symmetric: 94). **DERIVED — lineage passes through Jean's circuit** (basin 1 ∪ a 91 of our lineage). |
| `seed_90_at_depth9_rho2sym_basin1.json` | 90 @ 9 | exactly ρ²-symmetric (basin 1) = a 91 of our lineage ∪ a 92 symmetrized from Jean's 88. **DERIVED — lineage passes through Jean's circuit.** The basin whose descent produced the third-family 88@8. |

Who uses them: the `hunt87` worker set starts from the three 88s and the 89@5,
the `sub89` set from the 89@6 and the 90@5 (`../ladder_parallel.py`,
`WORKER_SETS`). The two ρ²-symmetric 90s are not in a shipped set — they are
the fastest-descending young basins we have (90 → 89@5 in ~15 min in the
archived run) and are there to be pointed at.

Each file's `source` field names the exact path it came from: for the record
circuits the curated copy in `../../evidence/circuits/`, otherwise the raw
campaign archive, which is not part of this repository.
