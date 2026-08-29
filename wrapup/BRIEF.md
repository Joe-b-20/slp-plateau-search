# WRAP-UP CAMPAIGN BRIEF — wave 1 (digest)

Date: 2026-08-29. Read this whole file before touching anything.

## Context

This repo holds a concluded research campaign: computing AES MixColumns (32x32
over GF(2), FIPS-197) in as few 2-input XOR gates as possible. Final state:
record = 88 gates (refereed bracket 56 <= L(M) <= 88), no 87 ever found, the
last live computation (the k=14 joint SAT test) is still running and is NOT
part of this campaign. The search phase is OVER.

This wrap-up campaign has four end goals:
1. Organize the local tree (label everything, propose deletions of scratch).
2. A METHOD CATALOG — every search/analysis method ever run here, with its
   measured track record from its own logs. This is the single most valuable
   deliverable: it is the toolkit for the next phase (other circuits, e.g.
   aes_inv_mixcolumns).
3. Counts + labels of every artifact class, so the public repos can say
   "N of X available upon request" with honest, reproducible numbers.
4. Distilled material from which short, plain-language public repo pages
   will be written.

Your report is raw material for goals 2-4 and the deletion decision in 1.

## HARD RULES

- **This wave is READ-ONLY.** You write exactly ONE file: your report at the
  path given in your task. You do not move, rename, delete, or modify
  anything else, anywhere.
- **`fleet11/laneCUBE/` is LIVE.** Four SAT solvers + a cube sweep run there
  right now. Never write inside it, never create `experiments/STOP`, never
  kill or signal any process, never use pkill. Reading inside laneCUBE is
  allowed but keep it light.
- **Big files:** parts of this tree are tens of GB. Never cat/read a large
  file whole. Use `du -sh`, `find ... | wc -l`, `ls -lS | head`, `head`,
  `tail`, `grep -c`, sampling. Budget your reading.
- **CPU is scarce** (the solvers own ~18 of 20 cores). No heavy computation.
  Verifying a handful of circuits with `python3 verify_circuit.py <file>`
  (repo root; prints VALID) is fine; bulk re-verification is not.
- **Counts must be reproducible.** Every count you report comes with the
  exact command that produced it.
- **When in doubt, KEEP.** Deletion recommendations are proposals only;
  over-deleting loses data forever, under-deleting costs disk.

## SHARP EYE (standing order from the user)

The route to 87 — or to a proof that 88 is optimal — might be hiding in this
project's data. While digesting your slice, actively look for:
- results nobody followed up on (a RESULT.md ending in "next step" that has
  no successor; logs whose final lines were never analyzed)
- anomalies mentioned once and dropped; contradictions between files
- data that was generated but never examined (large result files with no
  corresponding analysis/writeup)
- partial bounds from timed-out solves (a timeout is a bracket, not a
  refutation — timed-out runs often banked proven partial bounds)
- anything in your slice that looks like evidence about WHY 88 keeps
  appearing (structure shared by all 88s, obstructions at 87)
Everything of this kind goes in your LEADS section, even if speculative.
Label confidence honestly (VERIFIED-IN-LOG / PLAUSIBLE / SMELL).

## REPORT FORMAT (use exactly these sections)

```
# Slice report: <slice-name>
Agent model: <model>. Date. One-paragraph summary at top.

## 1. INVENTORY
Directory map of the slice with sizes (du -sh per subdir), what each subdir
IS (one line each), file-type breakdown where relevant. Note which subdirs
are already well-documented (have a RESULT.md / README) vs opaque.

## 2. METHODS
One catalog entry per distinct method found in this slice (schema below).
A "method" = any distinct way of searching for circuits, proving bounds,
or analyzing circuit structure. Small twists on a sibling method get their
own entry with the twist named.

## 3. ARTIFACTS (counts + labels)
Countable classes, e.g.:
- verified circuits by gate count / depth / family (count + where + command)
- UNSAT/bound certificates (what exactly each certifies)
- writeups/reports (RESULT.md files etc.)
- ledgers / append-only result files
- raw logs (count, total size)
Each: label, count, command used, path.

## 4. KEEP / DELETE proposal
Per subdir or file-class: KEEP (and why — result, ledger, unique data) or
DELETE-CANDIDATE (and why — regenerable scratch, CNF dumps, duplicate state,
dead intermediate) with size reclaimed. Anything uncertain: KEEP + a note.

## 5. LEADS (sharp-eye findings)
As described above. If none: say "none found" explicitly.

## 6. HAZARDS
Anything in your slice that must not be moved/deleted for operational
reasons (live process files, files referenced by running code, symlinks,
absolute paths hardcoded in scripts that reorganization would break).

## 7. GAPS
What you could not determine and why (log missing, file unreadable, would
need compute). Honest > complete.
```

## METHOD CATALOG ENTRY SCHEMA

```
### <method-name (short, kebab-case)>
- Family: <e.g. SAT-joint-levels | plateau-search | class-pricing-generator |
  ladder/atlas | hand-reasoning | structural-analysis | ...>
- What it does: 2-3 sentences, plain language, no project jargon.
- Twist vs siblings: what distinguishes it from the nearest other method.
- Measured performance: what its logs actually show (best gate count reached,
  what it proved/refuted, hit rates). Cite the log/result files.
- Cost: CPU time / wall time if recoverable from logs.
- Code: path(s) to the implementation.
- Logs/results: path(s), sizes.
- Generality: CIRCUIT-GENERIC / MC-HARDCODED / MIXED — and what would need
  changing to aim it at a different circuit (e.g. aes_inv_mixcolumns).
- Phase-2 verdict: keeper / superseded-by-<method> / dead-end, one line why.
```

## Final-message rule

Your report file is the deliverable. Your final text message: 5-10 lines —
slice name, report path, method count, headline artifact counts, number of
leads, anything urgent. No file dumps.
