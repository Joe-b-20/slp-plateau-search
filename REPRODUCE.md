# REPRODUCE

Every claim in the [evidence ladder](README.md#the-evidence-ladder), with the
command that checks it, the line of output that means it passed, and what it
cost. Nothing below is illustrative: every command was typed from the root of
this repository and every time is a real measurement, either from the
reproduction pack the command lives in, from this repository's own assembly
run on 2026-09-01, or — for Tier R — from the re-runs of 2026-09-02.

**Four tiers.**

| tier | budget | what it is |
|---|---|---|
| **[A](#tier-a--seconds)** | seconds | the oracle, the tripwire, the three bound checkers, the corpus certificates over the shipped sample. Python 3 standard library only. **Start here.** |
| **[B](#tier-b--minutes)** | minutes | the SAT ladder at k = 9, 10, 11 with its positive control and DRAT emission; the Python-vs-C agreement control; the self-contained `>= 56` exhaustion; the bound-machinery validation suite. Needs a C compiler and, for the SAT rows, `python-sat`. |
| **[R](#tier-r--the-records-rebuilt)** | a minute to hours | **the records, rebuilt** — not verified from a file, *produced again from nothing*, by the fastest honest method the project has for each. Six of the nine verified circuits have a command; three do not, and the table says why for each. Python 3 standard library only. |
| **[C](#tier-c--documented-not-re-run)** | hours to core-weeks | banked. k = 12/13/14, the `>= 81` solver run, the full-corpus deletion run, the prune-free exhaustion, the radius sweeps. Each row names its cost, its artifact, and why re-running it here would add nothing. |

Tier A's record row checks that the shipped circuits *are* what they claim.
Tier R is the different and larger claim: that the machinery which produces them
runs, on one core, from GF(2⁸) and nothing else, and gets there again.

**Environment for the measured times.** Linux, Python 3.12, one core,
`nice -n 19`, on a 20-core machine carrying an unrelated load throughout. Wall
times move with that load — two runs of the same command in Tier B differ by
10 %. Read them as orders of magnitude and as evidence that the shipped files
return the banked verdicts, not as a benchmark. Where a pack measured the same
command twice, both numbers are given.

**Nothing here needs the network.** No downloads, no solver service, no
account. `python-sat` (Tier B, SAT rows only) and a C compiler (Tier B) are the
only things that are not already in a stock Python 3.

---

## Tier A — seconds

All of Tier A runs in **under two seconds in total**, plus one `gcc`.

### Ladder row 1 — *any circuit needs >= 56 gates* (**proved**)

| | |
|---|---|
| command | `cd bounds && python3 gte56/check_gte56.py` |
| expected | `RESULT: every closed-form hypothesis of Theorem N holds for this matrix.` … `With e_K = 5 (cited exhaustion) :  L(M) >= 56` |
| measured | **0.03 s** (0.11 s on a cold page cache) |
| historical | the closed-form hypotheses were hand-checked, then machine-checked, at negligible cost — they were never the expensive half. The expensive half is `e_K`; see [B9](#b9) and [C6](#c6). |

The checker reads `bounds/matrix.txt` and the certificate; it has no matrix
baked in. `--matrix`/`--cert` point it at any other 0/1 matrix.

### Ladder row 2 — *any depth-3 circuit needs >= 81 gates* (**proved**)

The **certified, independently checkable** number is **80**. The step to 81 is
a solver dual bound, banked in [C4](#c4) and labelled as a run, not a
certificate, everywhere it appears.

| | |
|---|---|
| command | `cd bounds && python3 depth3_gte81/certify.py --check depth3_gte81/cert_depth3.json` |
| expected | `exact dual value = 47597998171620/1000000000000 = 47.597998` / `=> \|L1\|+\|L2\| >= 48  =>  N_depth3 >= 80` |
| measured | **0.29 s** (0.27 s in this repository's assembly run) |
| historical | minutes to *generate* the certificate — an LP solve with a slack margin, then exact integer re-verification. Checking it is all-integer arithmetic and needs no solver stack. |

A bound from a model is vacuous if the model is unsound, so the three
soundness controls are not optional:

| | |
|---|---|
| command | `cd bounds && python3 depth3_gte81/control_primal.py && python3 depth3_gte81/control_cuts.py && python3 depth3_gte81/control_lp.py` |
| expected | `CONTROL PASS` three times; `model objective realised (\|L1\|+\|L2\|) = 65  -> total 97`; `violated rows: NONE` |
| measured | **0.05 s + 0.12 s + 0.31 s** |
| historical | the same — seconds, and always mandatory |

### Ladder row 3 — *cancellation-free circuits need >= 92; best known 102* (**proved** / verified circuit)

| | |
|---|---|
| command | `cd bounds && python3 cf_gte92/check_cf_cert.py --aes-crosscheck` |
| expected | `RESULT: certificate VALID.` / `B = 910019782/10000000 = 91.0019782` / `=> L_cf(M) >= 92` |
| measured | **0.03 s** |
| historical | ~25 minutes of projected subgradient ascent to *generate* the table. The published check cost was quoted as "~2 s, solver-free" — conservative by a factor of sixty. |

`--aes-crosscheck` adds `CHECK A`: the script rebuilds MixColumns from
GF(2^8)/0x11B out of the specification and confirms `bounds/matrix.txt` is that
map, row for row. Drop the flag and the checker is matrix-agnostic.

The **second, independent derivation** — a different lane, a different route,
a better constant, the same integer conclusion:

| | |
|---|---|
| command | `cd bounds && python3 cf_gte92/check_cf_cert.py --cert cf_gte92/cert_cf92_sharper.json` |
| expected | `numerator = 914098776,  B = 914098776/10000000 = 91.4098776` / `=> L_cf(M) >= 92` |
| measured | **0.03 s** |
| historical | 60–120 s per multiplier value on 8 threads, 19 values, plus exactification |

The **witness** at 102, and the checker's negative control — a checker that
cannot say no is worthless:

| | |
|---|---|
| command | `cd bounds && python3 cf_gte92/check_cancellation_free.py cf_gte92/cf_102gates_depth5.json --require-cancellation-free` |
| expected | `RESULT: VALID and CANCELLATION-FREE.` — 102 gates, 32/32 targets, `kappa = 0`, depth 5, all four **computed** |
| measured | **0.02 s** |
| | |
| control | `python3 bounds/cf_gte92/check_cancellation_free.py corpus/tripwire_demo/circuits/mixcolumns_88gates_depth5.json` |
| expected | `RESULT: VALID, but NOT cancellation-free (kappa = 22).` |
| measured | **0.03 s** |

The same 102-gate circuit ships in the records repository from v3.2.0 as
`circuits/mixcolumns_102gates_cf.json`, with a `bounds.json` entry, a listing
and a Verilog netlist.

### Ladder row 4 — *the records: 97 @ depth 3, 91 @ depth 4, 88 @ depth 5* (**verified circuits**)

The circuits live in the records repository; this repository carries the
standalone oracle and its own copies under `evidence/circuits/`.

| | |
|---|---|
| command | `python3 verify_circuit.py evidence/circuits/mixcolumns_88gates_depth5_fromscratch.json 5` |
| expected | `gates=88 depth=5 outputs_built=32/32 problems=0` / `depth<= 5: OK` / `VERDICT: VALID MixColumns circuit`, exit 0 |
| measured | **0.02 s** |
| historical | n/a — verification has always been instantaneous |

Depth is **computed**, not read from the file, and the claim is tight — the
same circuit must be rejected one level down:

| | |
|---|---|
| command | `python3 verify_circuit.py evidence/circuits/mixcolumns_88gates_depth5_fromscratch.json 4` |
| expected | `depth<= 4: VIOLATED` / `VERDICT: INVALID`, **exit 1** |
| measured | **0.02 s** |

The full 13-circuit sweep with the adversarial suite is in the records
repository: [B10](#b10).

### Ladder row 6 — *no 87 is one gate-deletion away from any known 88* (**exhaustive**), and the B = 56 tripwire

The instrument first, on the five published record 88s **and** the published
88 from an independent author:

| | |
|---|---|
| command | `cd corpus/tripwire_demo && python3 ../../tools/tripwire.py --quiet circuits/mixcolumns_88gates_depth*.json circuits/foreign_88gates_depth7_eprint_2026-1481.json` |
| expected | six lines `n=88   B=56   expect=56   silent`, then `6 file(s) examined, none has a deletable gate.`, exit 0 |
| measured | **0.3 s** (0.03 s in this repository's assembly run) |

An instrument that cannot fire is not evidence, so the positive controls are
mandatory:

| | |
|---|---|
| command | `cd corpus/tripwire_demo && python3 ../../tools/tripwire.py --selftest circuits/mixcolumns_88gates_depth5_fromscratch.json` |
| expected | `1. the clean circuit as given -> silent` / `2. … + one duplicated gate -> FIRED` / `3. … + one gate nobody reads -> FIRED` / `SELF-TEST: PASS` |
| measured | **0.1 s** |
| | |
| command | `cd corpus/tripwire_demo && python3 tools/make_planted.py circuits/mixcolumns_88gates_depth6.json circuits && python3 ../../tools/tripwire.py circuits/planted_dup.json` |
| expected | `RESULT: *** A GATE CAN BE DELETED. ***`, `gate 20 and gate 21 both compute 0x02020002`, **exit 1** |
| measured | **0.1 s** |
| note | in this control `B` reads its *expected* 57 and the tripwire fires anyway, on the duplicate check. `B != n - q => a deletable gate` is sound; **its converse is false**, and this is the demonstration. |

`tools/tripwire.py` and `corpus/tripwire_demo/tripwire.py` are the same file,
byte for byte. Run either on your own circuit.

Then the deletion certificate itself. Build once:

| | |
|---|---|
| command | `cd corpus/deletion_certificate && gcc -O2 -Wall -o tools/delcert tools/delcert.c` |
| expected | silent |
| measured | **0.4 s** (0.14 s here) |

The controls, which must fire exactly as many times as there are planted
redundancies and no more:

| | |
|---|---|
| command | `cd corpus/deletion_certificate && tools/delcert --bin fixtures/ctrl_pos89.bin --targets targets.txt --k 89 --tag ctrlpos89 --every 0` |
| expected | `"realisable":498` — one planted deletion per record, found, no more |
| measured | **0.04 s** |
| | |
| command | `… --bin fixtures/ctrl_pos90.bin … --k 90 --tag ctrlpos90 --every 0` |
| expected | `"realisable":996` |
| measured | **0.04 s** |
| | |
| command | `… --bin fixtures/ctrl_neg498.bin … --k 88 --tag ctrl498 --every 0` |
| expected | `"realisable":0` **and** `"local_pass":10833` — a count independently recorded before the C tool existed |
| measured | **0.03 s** |

The certificate over the shipped 520-set sample, and the re-derivation of the
full-corpus verdict from the banked shards:

| | |
|---|---|
| command | `cd corpus/deletion_certificate && tools/delcert --bin ../sample/corpus88_sample.bin --targets targets.txt --k 88 --tag sample --every 0` |
| expected | `"tested":29120,"local_pass":11875,"realisable":0` — 520 sets × 56 working gates, 40.8 % pass the cheap filter, 0 survive the closure |
| measured | **0.03 s** |
| | |
| command | `cd corpus/deletion_certificate && python3 tools/aggregate.py` |
| expected | `"deletions_tested": 88228896` / `"realisable_87_mask_sets": 0` / `"coverage_pct_of_index": 100.0` / `OK: the certified intervals tile [0, 1575516) with no gap and no overlap.` |
| measured | **0.05 s** |
| historical | the run those shards came from: [C5](#c5) |

The full-scale run is [C5](#c5). What `aggregate.py` proves here is that the
banked intervals tile the whole index — that is what the "100 % of the corpus"
claim rests on, and it exits non-zero on any gap.

The sample the certificate ran over, re-checked from nothing but this pack:

| | |
|---|---|
| command | `cd corpus/sample && python3 tools/check_sample.py` |
| expected | `checked 520 rows: 520 distinct mask sets, each 88 distinct masks with all 32 targets` / `failures: 0` / `VERDICT: ALL ROWS PASS` |
| measured | **0.04 s** (0.05 s here) |

### Ladder row 9 — *the known 88s' shared vocabulary is not forced* (**verified counterexample**)

| | |
|---|---|
| command | `cd corpus/vocabulary && python3 tools/verify_circuit.py S89_out_of_vocabulary_89gates.json` |
| expected | `gates=89 depth=10 outputs_built=32/32 problems=0` / `VERDICT: VALID MixColumns circuit` |
| measured | **0.05 s** (0.02 s here) |
| | |
| command | `cd corpus/vocabulary && python3 tools/oov_check.py vocab.json S89_out_of_vocabulary_89gates.json` |
| expected | `OUT of the vocabulary: 6` / `VERDICT: OUT OF VOCABULARY.` — six masks occurring in none of 107,803,640 gate slots across 1,925,065 circuits |
| measured | **0.05 s** |
| | |
| control | `cd corpus/vocabulary && python3 tools/oov_check.py vocab.json ../tripwire_demo/circuits/mixcolumns_88gates_depth5.json` |
| expected | `IN  the vocabulary  : 56` / `OUT of the vocabulary: 0` / `VERDICT: entirely inside the corpus vocabulary.` |
| measured | **0.05 s** |
| historical | the re-census the vocabulary came from: 1,925,065 rows, 107,803,640 gate slots (banked in `recensus_stats.json`) |

### Ladder row 10 — *a from-scratch attempt reaches 93* (**measurement**)

| | |
|---|---|
| command | `cd corpus/calibration && python3 verify_circuit.py cleanroom_93gates.json` |
| expected | `gates=93 depth=7 outputs_built=32/32 problems=0` / `VERDICT: VALID MixColumns circuit` |
| measured | **0.05 s** (0.02 s here) |
| historical | the clean-room search that produced it: [C9](#c9) |

### The independence statistic (records README §"Credit and independence")

| | |
|---|---|
| command | `python3 scripts/overlap.py evidence/circuits/mixcolumns_88gates_depth7.json evidence/campaign87_imported_prior_art/jean_88gates_depth7_eprint_2026-1481.json` |
| expected | `shared      61` / `Jaccard        = 61/115 = 0.530` |
| measured | **0.03 s** |
| calibration | the same script on two circuits nobody disputes are independent — Jean's 88 against Sun–Yang–Li's published 89 — gives `shared 63`, `Jaccard 0.553`. Two independent circuits overlap *more* than ours does with Jean's. That is what independence looks like for this map. |

---

## Tier B — minutes

### The SAT ladder — ladder row 5 (*no 87 shares the block structure of the known 88s*)

The theorem is: the merged pair of the two largest blocks of every known 88
takes **exactly 15** gates; 9 through 14 are UNSAT. This tier re-proves the
cheap end of that ladder from the shipped DIMACS files. The expensive end is
[C1–C3](#c1).

**B1. Every shipped CNF is the encoder's own formula.** A ladder over files
somebody could have edited proves nothing.

| | |
|---|---|
| command | `cd encodings && for k in 9 10 11 12 13 14; do python3 code/check_cnf.py cnf/k${k}_joint_W3U4.cnf --k $k --json results/identity_k${k}.json; done` |
| expected | six lines `IDENTICAL … roundtrip=True digests=True` |
| measured | **3.6 s** for all six |

`roundtrip=True` means the file, parsed back, is literal-for-literal and in
order the clause list a fresh `build_cnf(...)` produces.

**B2. Instance facts** — the floor the ladder starts from, and a sanity control
that a program for the instance exists at all.

| | |
|---|---|
| command | `cd encodings && python3 code/instance_facts.py` |
| expected | `"lower_bound_L2": 9`, `"greedy_upper_bound": 16`, `"greedy_verify_slp": true` |
| measured | **1.2 s** |

**B3. The three cheap levels, re-solved from the shipped files.**

| | |
|---|---|
| command | `cd encodings && python3 code/solve_dimacs.py cnf/k9_joint_W3U4.cnf --json results/solve_k9.json` |
| expected | `s UNSATISFIABLE` / `c solver cadical195  status UNSAT` |
| measured | **0.98 s** (first pass 2.84 s; 0.89 s here) |
| historical | 23.68 s, encoding B, 8 cores |
| | |
| command | `… cnf/k10_joint_W3U4.cnf --json results/solve_k10.json` |
| expected | `s UNSATISFIABLE` |
| measured | **9.13 s** (first pass 24.67 s) |
| historical | 123.82 s, encoding B, 8 cores |
| | |
| command | `… cnf/k11_joint_W3U4.cnf --json results/solve_k11.json` |
| expected | `s UNSATISFIABLE` |
| measured | **72.82 s** (first pass 119.49 s) |
| historical | 218.45 s (encoding A, 1 core); 785.29 s (encoding B, 8 cores) |

The historical runs used a different CNF from a different generator on a
contended machine, so the comparison is one of **verdicts**, not of speed.
Three for three, the verdicts agree.

<a id="b4"></a>
**B4. The positive control — the row that matters most in the pack.** The same
encoder, the same 33 free signals, the same rank 16, the same solver, the same
code path that returns UNSAT six times on the ladder, on an instance whose
optimum is 7.

| | |
|---|---|
| command | `cd encodings && python3 code/solve_dimacs.py positive_control/k6_SUB_U4tgts.cnf` |
| expected | `s UNSATISFIABLE` — the negative leg |
| measured | **0.58 s** |
| | |
| command | `cd encodings && python3 code/solve_dimacs.py positive_control/k7_SUB_U4tgts.cnf --model positive_control/k7_SUB_U4tgts.model` |
| expected | **`s SATISFIABLE`** — the encoding can say yes |
| measured | **1.19 s** |
| | |
| command | `cd encodings && python3 code/decode_model.py positive_control/k7_SUB_U4tgts.model --k 7 --instance positive_control/instance_SUB_U4tgts.json --no-pin` |
| expected | `model_check: 9330/9330 vars assigned, 102115 clauses checked, 0 unsatisfied` / `verify_slp: ok` / `VERDICT: VALID 7-gate program for the block` |
| measured | seconds |
| | |
| cross-check | the decoded gates are **gate-for-gate identical** to `positive_control/expected_witness.json`, banked from a completely different route (a 528-way split on gate 0's input pair, hit at cube 144) |
| | |
| negative | one literal of the verified model flipped → decoder **exit 2**, `MODEL DOES NOT SATISFY THE FORMULA`, unsatisfied clauses named. A decoder that accepts anything proves nothing. |

**B5. The end-to-end rehearsal.** The constructive 15-gate program for the
merged block was handed to the circuit generator, which emitted 88 gates at
depth 7, and the standalone oracle accepted it in a fresh process. This is what
makes `88 - 15 + 14 = 87` an end-to-end fact rather than arithmetic on paper:
had k = 14 answered SAT, this same path would have emitted an 87-gate circuit
and verified it the same way.

| | |
|---|---|
| command | `cd encodings && python3 code/verify_circuit.py positive_control/mixcolumns_88gates_depth7.json 7` |
| expected | `gates=88 depth=7 outputs_built=32/32 problems=0` / `VERDICT: VALID MixColumns circuit` |
| measured | seconds |

**B6. DRAT proofs.** An UNSAT verdict is a solver's word for it; a DRAT
refutation is a certificate a checker replays without trusting the solver.

| | |
|---|---|
| command | `cd encodings && sh run_proofs.sh` |
| expected | four proofs emitted and validated: `WELL-FORMED DRAT … ends in empty clause=True` for k = 6, 9, 10, 11 |
| measured | **0.98 + 1.45 + 15.96 + 110.39 s ≈ 129 s** of proof logging (roughly 1.5× the plain solve) |

Three of the four `.drat.xz` files ship (k = 6, 9, 10). **k = 11's does not** —
40 MB compressed, larger than the rest of this repository put together, and
110 s to remake from the shipped CNF. `proofs/README.md` has the one-command
form, the digests recorded when it was emitted here, and the `drat-trim`
recipe.

**These proofs were emitted and structurally validated here; they were not
checked here** — no DRAT checker is installed on the assembly machine. Do not
read "well-formed" as "verified". Checking one is two commands:

```bash
xz -dk proofs/k9_joint_W3U4.drat.xz
drat-trim cnf/k9_joint_W3U4.cnf proofs/k9_joint_W3U4.drat     # expect: s VERIFIED
```

**B7. Checksums.**

| | |
|---|---|
| command | `cd encodings && sha256sum -c SHA256SUMS` |
| expected | 41 lines of `OK`, no failures |
| measured | **under a second** |
| note | `SHA256SUMS` deliberately excludes `results/` and the files `run_all.sh` derives, which a reader who re-runs the pack will overwrite. It is regenerated by `sh code/make_checksums.sh`. |

Everything above except the DRAT step is what `sh run_all.sh` does in one go.
It never starts k = 12, 13 or 14.

<a id="b8"></a>
**B8. Deletion certificate — Python vs C agreement** (ladder row 6). A ~300×
port is worth nothing unless it is diffed against what it ports.

| | |
|---|---|
| command | `cd corpus/deletion_certificate && python3 tools/pycheck.py ../sample/corpus88_sample.bin 0 520` |
| expected | `"tested":29120,"local_pass":11875,"realisable":0` — identical on all three aggregates to the C tool's output in Tier A |
| measured | **6.1 s** Python (5.6 s here) vs **0.0 s** C — below the timer's resolution |
| historical | the same control on 300 corpus records: 41.2 s vs 0.14 s, both 16,800 / 6,620 / 0 |

`tools/pycheck.py` carries the original Python — the local necessary condition
and the greedy closure — transcribed verbatim, importing nothing from the
project.

<a id="b9"></a>
**B9. The `>= 56` exhaustion, self-contained** (ladder row 1). `e_K` is the one
term of the bound that is not a closed-form check. It ships and it re-runs.

| | |
|---|---|
| build | `cd bounds && cc -O2 -o gte56/mine gte56/mine.c` |
| command | `cd bounds && python3 gte56/check_gte56.py --minE-depth 3` |
| expected | `k=14 depth=3 jam=8 shard=0/1 nodes=5784927 result=NONE` / `[PASS] H1 depth-3 exhaustion finds no completion => minE >= 4` → `L(M) >= 55` |
| measured | **0.47 s** and **0.9 s** on two runs; node count byte-identical both times |
| | |
| command | `cd bounds && python3 gte56/check_gte56.py --minE-depth 4` |
| expected | `k=14 depth=4 jam=8 shard=0/1 nodes=1895523772 result=NONE` / `[PASS] H1 … => minE >= 5` → **`L(M) >= 56`** |
| measured | **166.0 s** and **156.8 s** on two runs, one core; **1,895,523,772 nodes**, identical both times |
| historical | 200–730 s per certificate in the originating lane's Python searcher; ~15 s in the referee's C searcher; and the prune-free run in [C6](#c6) |

The searcher is deterministic, so the node count is a reproducible fingerprint
even when the wall time is not. **Read the difference honestly:** this run uses
two prunings, both proved sound in `mine.c`'s header. The historical run that
makes the result *prune-independent* used none — [C6](#c6).

<a id="b10"></a>
**B10. The bound machinery on instances with known optima.** A lower-bound
method is only worth reading if it cannot return a number above the truth.

| | |
|---|---|
| command | `cd bounds && python3 validation/run_validation.py` |
| expected | `RESULT: PASS on 3 instance(s).` — no bound exceeds a known optimum at any covering level or keep-set size; the searcher independently reproduces every SAT-proved optimum; the precondition negative control overclaims exactly as documented when its gate is ignored, and becomes sound once reduced |
| measured | **170.5 s** and **156.2 s** on two runs; identical verdicts and node counts |
| one instance | `python3 validation/run_validation.py --instance L5_tap_pairQ3` — **0.2 s**, exercises every code path except the deep exhaustion |
| historical | the reference optima cost 4,511 s of SAT for `L1_clean_iso` (4,236 s of it in one `k = 11` UNSAT call) plus a 72,000 s hardening run with all symmetry-breaking clauses stripped; 42.45 s for `tap_P__Q1_2_4_a` |

**B11. The records, all of them, with the adversarial suite** (ladder row 4).
This one runs in the **records repository**, not here.

| | |
|---|---|
| command | `python3 verify_all.py` (in `aes-mixcolumns-xor-circuits`) |
| expected | every circuit `[ OK ]`, `ALL CIRCUITS VERIFIED`, `Adversarial tests passed: 14 of 14`, `Overall result: PASS`, exit 0 |
| measured | **20.6 s** |
| note | compare-only mode: it writes nothing, so verifying never dirties the working tree |

**B12. This repository's own tests.**

| | |
|---|---|
| command | `python3 -m unittest discover -s tests` |
| expected | `Ran 35 tests` / `OK` |
| measured | **12.5 s** |

---

## Tier R — the records, rebuilt

The asset this project has that a circuit file does not carry: **the machinery
that produces the records**, packaged so it can be run again from nothing. Each
row offers the *fastest honest* route to its circuit — which is usually, but not
always, the tool that historically found it; where it differs, the row says so.
Every command below is stdlib-only Python 3 and verifies
its own output against MixColumns rebuilt from GF(2⁸) before it reports
anything. The four `reproduce/` commands each run on **one core**; the two
`pipeline/` rows are coordinators that launch worker processes — two for the
89 @ 5, one per depth rung for the 92 @ 4 cascade. All of them are documented in
[`reproduce/`](reproduce/), whose README
carries the full method notes, the provenance argument for each, and the times
from every earlier re-run.

One row per verified circuit. Where there is no command the row says so and
prices the archived run instead — **no row here is illustrative and no command
here is aspirational**.

| circuit | command | cost |
|---|---|---|
| **97 @ 3** — *frontier*, from scratch | `cd reproduce && python3 reproduce.py` | **57.4 s and 51.8 s** in two runs, measured 2026-09-02 (RNG seed 6, its first seed, both times); 81 s on 2026-07-27; 60–156 s across earlier runs |
| **91 @ 4** — *frontier*, from scratch | **none here yet.** The cascade fleet that found it is a separate codebase, published in neither repository — but the fastest route is not that search: an exact **construction** in the project's unpublished tree emits an independent 91 @ 4 from GF(2⁸) alone. `reproduce/README.md` gives the command, the provenance tests and the packaging blocker | **2 s** measured 2026-09-02, one core, cold cache — the fastest reproduction of any record here. The historical search cost **54.4 min** of one core from its from-scratch root `naive#40426`, inside a ~74 process-hour run |
| **88 @ 5** — *frontier*, from scratch | `cd reproduce && python3 hunt_88at5.py` | archived: **64 min** of one core from its root `naive#1958`, then 6.1 s to depth 5 via the Pareto tie-break. Two re-runs 2026-09-02 reproduced the descent to **89 gates in 558 s** against the archived 3 072 s, and **did not reach 88 within 164 min** — the last gate is a single lucky walk chunk. Read the archived 64 min as one sample, not a promise; `reproduce/README.md` has both runs in full |
| **88 @ 6**, from scratch | `cd reproduce && python3 hunt_88at5.py --rng 2163 --target-depth 6` | archived: **37 min** of one core from its root `naive#2163`. Same script and same archived worker as the row above; not re-measured on 2026-09-02 |
| **88 @ 7**, matching the published count with an independent circuit | `cd reproduce && python3 hunt_88.py` | **19.4 min** measured 2026-07-27 under the shipped stop rule; archived 32.9 min |
| **88 @ 5, derived** | **none, by choice** — its seed chain runs through published work, so it is reported as derived and not offered as a recipe | archive: `evidence/campaign87_run_2026-07-29_got_88at5_derived/`, with the code, the seed and the untouched logs |
| **88 @ 8**, third family | **none, by choice** — same reason | archive: `evidence/campaign87_run_2026-07-27_got_88at8_thirdfamily/`; the seed also ships as `pipeline/seeds/seed_88_at_depth8_thirdfamily.json` |
| **89 @ 5** — *superseded by the 88 @ 5, kept* | `cd pipeline && python3 ladder_parallel.py --mode fixed --workers sub89 --stop-gates 89 --stop-depth 5` | **20 s** measured 2026-09-02 (verified at the coordinator's first status poll, t = 17.5 s); 19 s and 22 s on 2026-07-27; archived 592 s on the v1 engine |
| **92 @ 4** — *superseded by the 91 @ 4, kept*, from scratch | `cd pipeline && python3 ladder_parallel.py --mode cascade --stop-gates 92 --stop-depth 4` | archived: **9 610 s (2.67 h)**. Not re-measured. Do **not** retarget it at 91 — it reaches 92, and its stop condition latches shut once the cascade goes below 91 gates at any depth |

**What Tier R does not claim.** Every one of these is a stochastic search. The
times are what a run took, not what a run will take; a re-run can be faster,
much slower, or miss inside its budget. The two `hunt_*` scripts start from the
record run's own root and RNG, so each reproduces its first chunk exactly — but
chunk boundaries are wall-clock, so a machine of a different speed parts company
with the archived trajectory from the second chunk on, and what comes back is
another point in the same basin rather than the record circuit. That is the
honest thing a re-run establishes: the shipped engine, seed and knobs are the
ones that produced the record, and they run.

**Sometimes they miss, and the tier says so.** The 88 @ 5's own re-runs on
2026-09-02 reproduced its descent to 89 gates five times faster than the archived
run and then did not find the last gate inside 164 minutes, where the archive
took 64. Nothing was adjusted to hide that: it is what a stochastic search does,
and a tier that only ever reported its wins would not be worth running.

**A row's command need not be the tool that historically found the circuit.**
Where a faster honest route exists, it is the one offered, labelled as a
different method. "From scratch" means one thing throughout: **no record circuit
and no record-derived data as input — targets from GF(2⁸) and FIPS-197 only.**

**Two of the three frontier points reproduce from nothing with a command in this
repository** — the 97 @ 3 computes its targets from GF(2⁸); the 88 @ 5's root is
a randomized XOR tree that is a pure function of the integer 1958. The 91 @ 4 is
the gap, and it is a packaging gap rather than a scientific one: it can be
*constructed* from GF(2⁸) in two seconds by a generator this project has and has
not published. That the route clears the from-scratch bar was tested rather than
assumed — an audit hook shows no record circuit is opened, and replacing the one
record-derived table it loads with garbage leaves the emitted circuit
byte-identical. What blocks publication is the tool's `numpy` and SAT-solver
dependencies against this folder's stdlib-only contract, not its provenance. It
is filed in [`leads.md`](leads.md).

---

## Tier C — documented, not re-run

Every row here was paid for once. Each names what it cost, where the evidence
sits, and why re-running it inside a session would add nothing.

<a id="c1"></a>
### C1–C3. The expensive end of the SAT ladder — ladder row 5

| level | verdict | cost when it was paid | artifact | why not re-run |
|---|---|---|---|---|
| **k = 12** | UNSAT | **5,761.73 core-s** (1 core, encoding A); **5,202.15 s** on 8 cores (encoding B) | `encodings/logs/BANKED_LOGS.md` §L2, §L3; CNF `encodings/cnf/k12_joint_W3U4.cnf`, identity-checked in [B1](#tier-b--minutes) | ~1.6 core-hours, twice over; the CNF ships and anyone with the budget can repeat it |
| **k = 13** | UNSAT | **105,083.40 s on 8 cores ≈ 233.5 core-hours** (encoding B) | `encodings/logs/BANKED_LOGS.md` §L3; CNF ships | 233 core-hours |
| **k = 14** | UNSAT | **356,321.63 core-s ≈ 99.0 core-hours**, one process, kissat 4.0.4 (encoding A) | `encodings/logs/BANKED_LOGS.md` §L1; CNF `encodings/cnf/k14_joint_W3U4.cnf` ships | 99 core-hours. **This is the decisive level** and it was decided by a single complete solver running the whole formula — not by a partial cube sweep. |

k = 13 and k = 14 together are over 330 core-hours. **None of the three carries
a DRAT proof**, so the decisive level of this theorem rests on complete solvers
being correct rather than on a checked certificate. That is the honest boundary
of this repository's evidence, and it is why the cheap levels ship proofs and
why the positive control in [B4](#b4) exists.

Hand `encodings/cnf/k14_joint_W3U4.cnf` to any SAT solver you trust. SAT there
would mean an 87-gate MixColumns circuit exists in that block class.

<a id="c4"></a>
### C4. The `>= 81` solver run — ladder row 2

| | |
|---|---|
| what | HiGHS branch-and-cut on the full depth-3 model, 72,830 rows × 29,180 columns |
| cost | **60,391.94 s ≈ 16.8 h**, single-threaded, `nice -n 19` |
| artifact | `bounds/depth3_gte81/mip3_result_L1.json`, `bounds/depth3_gte81/mip3_L1_run.log` — both shipped and readable |
| result | `Status: Time limit reached`, `Dual bound 49`, gap **66.99 %** → `N_depth3 >= 81` |
| to repeat | `cd bounds && python3 depth3_gte81/mip3.py` (needs `highspy`; expect hours; set your own limit) |
| why not re-run | **it never closed.** The run hit its own time limit with two thirds of the gap open, so re-running it inside a session was not possible and would not have added information. The 81 is HiGHS's *dual* bound, which is valid at any point in branch-and-cut — that part is sound — but the primal 148 is an incumbent, not an optimum, and must never be quoted as one. |

Two things to read carefully in that log. First, the result file's own
`wall_monotonic` field says 1,369.95 s while HiGHS reports
`Timing 60391.94 (total)`; **trust the solver log**, the JSON field is wrong,
and it is left unpatched rather than silently corrected. Second, the log's
first LP row, `47.59824561`, is the same value the exact certificate in
[ladder row 2](#ladder-row-2--any-depth-3-circuit-needs--81-gates-proved) pins
to the digit — an independent confirmation, through HiGHS's own code path,
that the certified 47.597998 is the root relaxation.

<a id="c5"></a>
### C5. The full-corpus deletion run — ladder row 6

| stage | cost |
|---|---|
| producer — streaming 1,575,516 distinct mask sets out of ~40 GB of raw run output into `masks.bin` (554 MB) and `canon.tsv` (158 MB) | **1,457.9 s = 24.3 min** |
| certificate — **88,228,896 deletions**, two shards | **612.9 s CPU = 10.2 min** |
| throughput | **2,571 sets/s** per `nice -n 19` thread |

**Banked result** (`corpus/deletion_certificate/banked/RESULT.json`): 1,575,516
mask sets, 100.00 % of the index, 88,228,896 deletions tested, 35,323,820 pass
the local filter, **0 realisable**, 0 firings, 0 gaps, 0 overlaps, 56.000000
deletions per set.

**Why not re-run.** The 554 MB mask file and the ~40 GB of source banks it was
streamed from do not ship — the honest sizes are in `INVENTORY.md`. What does
ship is better than a re-run of the same numbers: the 520-set sample the same
binary processes unchanged, the positive and negative controls, and
`tools/aggregate.py`, which re-derives every headline figure from the banked
shards **and proves the certified intervals tile `[0, 1575516)` with no gap and
no overlap** in 0.05 s. Fetching the corpus costs more than certifying it.

The commands that produced the banked result are recorded verbatim in
`corpus/deletion_certificate/RUN.md` §5, with a `tools/sources.example.json`
template, so the full-scale run is reproducible by anyone holding the sources.

<a id="c6"></a>
### C6. The prune-free `e_K` exhaustion — ladder row 1

| | |
|---|---|
| what | the depth-4 exhaustion behind `e_K = 5`, run with **no prunings at all** |
| cost | 16 workers, 114 shards per certificate, run twice: **9.43e10 nodes** (unpruned C) and **4.75e9 nodes** (pruned Python), both `NO COMPLETION` on all 511/511 root branches |
| artifact | cited in `bounds/gte56/STATEMENT.md` and `RUN.md`; the shipped searcher is `bounds/gte56/mine.c` |
| why not re-run | 9.43e10 nodes. [B9](#b9) reproduces the *verdict* single-core in 166 s using two prunings that are proved sound in `mine.c`'s header comment. The value of the unpruned run is precisely that it does **not** depend on those two arguments being correct — so it is cited, not reproduced. |

<a id="c7"></a>
### C7. The radius sweeps — ladder row 7 (*no 87 within any change of <= 4 gates of a known 88*)

| radius | scale | strength |
|---|---|---|
| remove-2-add-1 | 139,878 of 139,878 mask sets × 1,540 windows = **215,412,120 exact window decisions**, in three disjoint ledgers | exhaustive |
| remove-3-add-2 | 200 circuits × 27,720 triples, every one decided | exhaustive |
| remove-4 | 56,489 / 39,034 / 34,599 windows of 367,290 on three circuits — **15.4 %, 10.6 %, 9.4 %** | searched, coverage stated |
| one operand edit of any one-gate truncation | 6,832,408 genomes over 529 base circuits | exhaustive |

Campaign-wide: **≈165 million exact window decisions**, zero timeouts, zero
reducible. Artifact: `NEGATIVES.md` rows 6–13 and the matching
`negatives.jsonl` entries, each with its `does_not_imply` field.

**Why not re-run.** Hundreds of core-hours, over a population that does not
ship. And — stated here rather than left for a reader to find — **this
repository's own control audit prices these near information-free about
whether an 87 exists**: the same tests return "nothing better nearby" for
89-to-97-gate circuits that demonstrably have an 88 below them. See
`corpus/calibration/CONTROL_AUDIT.md`. They are exhaustive statements, honestly
scoped, about neighbourhoods; they are not evidence of optimality.

<a id="c8"></a>
### C8. The relaxations — ladder row 8 (*~200 relaxations all price back to 88*)

| what | scale |
|---|---|
| menu pricing over every way of budgeting shared sub-expressions | **1.41e26** configurations, never below 87; 9 of 10 component bounds exactly tight |
| exact optimisation over restricted alphabets | **749,150** runs returned OPTIMAL, 125 timeouts; best floor anywhere = 88 |
| dimension-8 block cells proved exactly optimal | **82 of 82**, each with a positive control that fires |
| the fan-out-8 freedom | 39 mask sets, all exact, 0 timeouts |

Artifact: `NEGATIVES.md` rows 14–19, `negatives.jsonl`. **Why not re-run:**
campaign-scale solver time over blocks and populations that do not ship.

<a id="c9"></a>
### C9. The clean-room search — ladder row 10

| | |
|---|---|
| what | an independent from-scratch effort with none of this project's accumulated structure |
| cost | **19.54 hours** of measured solver time |
| result | **93 gates at depth 7**, verified — the last five gates are where all the difficulty lives |
| artifact | `corpus/calibration/cleanroom_93gates.json`, `corpus/calibration/CALIBRATION.md`; the circuit re-verifies in 0.05 s in Tier A |
| why not re-run | 19.5 h, and the measurement it produced is a single number that the shipped circuit already witnesses |

### Ladder row 11 — *88 is optimal* (**believed**)

No command. It is an opinion, fenced as one in the README, and the README also
names the tension: two of its three pillars lean on exactly the local negatives
[C7](#c7) discounts.

---

## Coverage

Every row of the README's evidence ladder, and where it is checked:

| ladder row | tier |
|---|---|
| any circuit needs >= 56 | **A** (certificate) + **B9** (exhaustion, 166 s) + **C6** (prune-free, cited) |
| any depth-3 circuit needs >= 81 | **A** (certified 80 + three controls) + **C4** (the step to 81, a solver run) |
| cancellation-free >= 92, best known 102 | **A** (both derivations, the witness, the negative control) |
| the records 97/91/88 | **A** (oracle + depth tightness) + **B11** (all 13, adversarial suite) + **[R](#tier-r--the-records-rebuilt)** (produced again from nothing, by the fastest honest method for each: 6 of 9 circuits have a command, 3 do not and say why) |
| no 87 shares the block structure of the known 88s | **B1–B7** (k = 9,10,11 + positive control + DRAT) + **C1–C3** (k = 12,13,14) |
| no 87 one deletion away from any known 88 | **A** (controls, sample, banked re-derivation) + **B8** (Python/C agreement) + **C5** (the full run) |
| no 87 within <= 4 gates of a known 88 | **C7** — and read the calibration caveat with it |
| ~200 relaxations price back to 88 | **C8** |
| the vocabulary is not forced | **A** (the 89, its 6 out-of-vocabulary masks, the negative control) |
| from-scratch reaches 93 | **A** (the circuit) + **C9** (the search) |
| 88 is optimal | **believed** — no command exists, and none is claimed |

If a command in Tier A or B does not produce the output stated next to it, that
is a real failure and nothing in this repository should be believed until it is
explained. Open an issue with your Python version and the full output.
