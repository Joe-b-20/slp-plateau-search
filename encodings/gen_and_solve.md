# Generating and solving a level

This pack ships the formulas as plain DIMACS CNF. **Any** SAT solver decides
them; nothing about the encoding is solver-specific. This page gives the command
lines, says exactly what was run to produce the numbers in `RUN.md`, and
explains how to check that a shipped file really is the formula it claims to be.

---

## 1. Requirements

| to do this | you need |
|---|---|
| solve a shipped `.cnf` | any DIMACS solver, or Python 3 + `python-sat` |
| check a file *is* the encoder's formula | Python 3, `python-sat`, NumPy |
| regenerate a `.cnf` from the instance | Python 3, `python-sat`, NumPy |
| decode a SAT model into a program | Python 3, `python-sat`, NumPy |
| verify a finished MixColumns circuit | Python 3 only |

```bash
python3 -m pip install python-sat numpy
```

The encoder (`code/slp_opt.py`) and the MixColumns oracle
(`code/verify_circuit.py`) ship inside this pack. Nothing here reaches outside
the pack directory, and every path in every command below is relative to the
pack root.

## 2. Solving a level with a solver binary

The files are ordinary DIMACS. Pick a level and run it. All of these are
correct; none needs a flag.

```bash
# Kissat  (https://github.com/arminbiere/kissat)
kissat cnf/k9_joint_W3U4.cnf

# CaDiCaL (https://github.com/arminbiere/cadical)
cadical cnf/k9_joint_W3U4.cnf

# MiniSat (any 2.2-compatible build; writes the model to a file)
minisat cnf/k9_joint_W3U4.cnf /tmp/k9.model

# Glucose
glucose cnf/k9_joint_W3U4.cnf
```

Exit codes follow the SAT competition convention: **10 = SATISFIABLE**,
**20 = UNSATISFIABLE**, 0 = no answer within the limits you set. Kissat and
CaDiCaL print `s UNSATISFIABLE` for every ladder file in `cnf/`.

**Single-thread, one process.** Every cost in this pack is a one-core number and
the levels are not parallelised. If you hand a level to a portfolio, report
which member answered.

### Proof logging

An UNSAT verdict is a solver's word for it. A **DRAT proof** is a certificate: a
checker replays it against the CNF and has to trust nothing about the solver
that produced it. This pack ships DRAT refutations for **every level it can
afford to prove** — k = 9, k = 10, k = 11, and the control's negative leg
k = 6 — in `proofs/`, with the sha256 of each. See `proofs/README.md` for the
manifest, the sizes, and the checking command.

Emit one yourself, with a binary:

```bash
cadical --no-binary cnf/k9_joint_W3U4.cnf /tmp/k9.drat
kissat --no-binary cnf/k9_joint_W3U4.cnf /tmp/k9.drat
```

or, with no binary installed, exactly as this pack did it:

```bash
python3 code/emit_proof.py cnf/k9_joint_W3U4.cnf --out proofs/k9_joint_W3U4.drat
sh run_proofs.sh          # all four levels, then compress
```

`code/emit_proof.py` parses the clauses **out of the shipped DIMACS file** and
solves with proof logging on, so the certificate refutes the shipped artifact.
Proof logging roughly doubles the solve time; the measured cost of all four
proofs is under four minutes of one core.

**Checking a proof.** The standard checker is
[`drat-trim`](https://github.com/marijnheule/drat-trim) — one C file, `make`,
no dependencies:

```bash
xz -dk proofs/k9_joint_W3U4.drat.xz          # -> proofs/k9_joint_W3U4.drat
drat-trim cnf/k9_joint_W3U4.cnf proofs/k9_joint_W3U4.drat
# expect: s VERIFIED
```

`cake_lpr` and `lrat-check` work the same way once the proof is converted to
LRAT (`drat-trim ... -L out.lrat`).

> **Stated plainly: emission happened here, checking did not.** No DRAT checker
> is installed on the machine that assembled this pack, so these proofs were
> *emitted and structurally validated*, not *verified*. What was checked is
> well-formedness — every line parses, every variable is within the CNF's
> variable count, and the file ends in the empty clause — by
> `code/check_proof_format.py`, which says so about itself in its own docstring.
> Checking is one `make` and one command away for anyone who wants it, and the
> sha256 of each proof is published so that what they check is what was emitted.

**k = 12, 13 and 14 carry no proof.** k = 14's solve alone was ~99 core-hours and
a proof of it would be enormous; producing and checking one is the single most
valuable thing anyone could add to this pack.

## 3. Solving a level without a solver binary

If you have no compiled solver, `code/solve_dimacs.py` runs one from the `pysat`
library. It parses the DIMACS file and hands the solver **the clauses out of the
file** — never a formula rebuilt in memory — so it is a measurement of the
shipped artifact.

```bash
python3 code/solve_dimacs.py cnf/k9_joint_W3U4.cnf
python3 code/solve_dimacs.py cnf/k9_joint_W3U4.cnf --solver kissat404
python3 code/solve_dimacs.py positive_control/k7_SUB_U4tgts.cnf \
        --model positive_control/k7_SUB_U4tgts.model
```

Solver names it accepts include `cadical195`, `cadical300`, `kissat404`,
`glucose42`, `minisat22`.

> **Which route produced this pack's numbers.** No standalone solver binary was
> available on the machine that assembled this pack, so every re-run in `RUN.md`
> went through `code/solve_dimacs.py` with **CaDiCaL 1.9.5** (`cadical195`) via
> `python-sat`. That is a real CaDiCaL deciding the real file; what it is not is
> a clean benchmark measurement, because the machine was carrying an unrelated
> long-running load throughout and every run was `nice -n 19`. Treat the times
> as evidence of *agreement with the banked verdicts*, not as a benchmark.

## 4. Checking that a file is the formula

The interesting claim about a shipped CNF is not its byte count, it is that it
is *the encoder's formula for the pinned instance*. `code/check_cnf.py` proves
that rather than asserting it: it parses the file back into a clause list and
compares it with a fresh `build_cnf(...)` call **literal for literal, in order**.

```bash
python3 code/check_cnf.py cnf/k14_joint_W3U4.cnf --k 14
python3 code/check_cnf.py cnf/k9_joint_W3U4.cnf  --k 9 --solve   # and solve it
python3 code/check_cnf.py positive_control/k7_SUB_U4tgts.cnf --k 7 --no-pin \
        --instance positive_control/instance_SUB_U4tgts.json
```

It prints `"VERDICT": "IDENTICAL"` and exits 0 on success. The reports for all
six ladder levels are banked in `results/identity_k*.json`.

The instance itself is hash-pinned: `code/instance_io.py` carries the canonical
sha256 of the merged-block instance, and every script that reads that file
refuses to run if the digest moves. `--no-pin` is for the control instance,
which is a different object on purpose.

## 5. Regenerating a level

```bash
python3 code/emit_cnf.py --k 9 --out /tmp/k9.cnf
python3 code/emit_cnf.py --k 6 --no-pin \
        --instance positive_control/instance_SUB_U4tgts.json \
        --out /tmp/k6_control.cnf
```

`emit_cnf.py` adds no clause and no variable of its own: it calls
`slp_opt.build_cnf(r, in_vals, tgt_vals, k, symmetry=True)` and serialises
`cnf.clauses` verbatim and in order. It builds the formula twice and refuses to
write if the two differ, so the emission is checked to be deterministic.

**Compare the clause body, not the bytes.** The shipped files carry `c` header
comments that `emit_cnf.py` does not reproduce. Comments are not part of the
formula and no solver reads them. The identity that matters is the one
`check_cnf.py` checks, and it is recorded in each file's header as the
**clause-order sha256**.

## 6. Decoding a SAT answer

Only the control instance is satisfiable — every ladder level is UNSAT — but the
decode path is the one that would matter if a level ever answered SAT, so it
ships and it has been exercised.

```bash
python3 code/decode_model.py positive_control/k7_SUB_U4tgts.model --k 7 \
        --instance positive_control/instance_SUB_U4tgts.json --no-pin
```

The decoder accepts DIMACS `s`/`v` lines, a bare list of signed integers, or a
JSON integer array. It then, in order:

1. rebuilds the CNF with the same call the file was written from, recovering the
   variable blocks;
2. **re-evaluates every clause under your model** — it does not take the
   solver's word for it, and it exits 2 if any clause is unsatisfied, naming the
   clause indices;
3. reads the one-hot `Z[i]` block of each gate and emits the program
   `{"gates": [[a, b], ...]}` — signal *a* XOR signal *b*, where signals
   `0 … 32` are the block's free input signals and signal `33 + i` is gate *i*;
4. replays that program and checks that every target value appears. **This is
   the decisive check**, and it exits 3 if it fails.

The variable layout, block by block with every index range, is in each level's
`*_meta.json` under `var_blocks`. Summarised for k = 14:

| block | variables | meaning |
|---|---|---|
| `V[i][b]` | 1 – 224 | bit *b* of the GF(2)^16 value carried by gate *i*; variable = `i*16 + b + 1` |
| `Z[i][j]` | 225 – 10983 | one-hot pair selection: gate *i* reads the signal pair (p, q) with key `q(q−1)/2 + p` over the `33 + i` signals available to it. `Z[0]` is 225 – 752, exactly C(33,2) = 528 literals |
| `S[i][j]` | interleaved | sequential at-most-one prefix variables for each `Z[i]` |
| `dif[i,j]` | interleaved | (N1) witness bits: gate *i*'s value differs from gate *j*'s |
| `uses[i]` | 23199 – 23211 | (N3) gate *i* reads a signal produced by gate *i−1* |
| `W[t][i]` | 23212 – 23323 | target *t* is carried by gate *i* |

## 7. Verifying a finished circuit

The end of the chain is the standalone oracle. It takes a JSON circuit
`{"gates": [[a, b], ...]}` over 32 inputs, **rebuilds MixColumns from GF(2^8)
arithmetic** — the specification is that code, not a matrix file — replays the
circuit, and reports gate count, computed depth, and how many of the 32 outputs
are right.

```bash
python3 code/verify_circuit.py positive_control/mixcolumns_88gates_depth7.json 7
# gates=88 depth=7 outputs_built=32/32 problems=0
# depth<= 7: OK
# VERDICT: VALID MixColumns circuit
```

Exit 0 iff all 32 outputs are correct (and, when a depth argument is given, iff
the *measured* depth is within it — depth is computed from the gate list, never
read from the file that claims it).

Checking 32 basis inputs is a proof, not a sample: the map is linear over GF(2),
so its values on a basis determine it on all 2^32 inputs.

## 8. A note on cube-and-conquer

`Z[0]` (variables 225 – 752 at k = 14) is an exactly-one block of 528 literals,
one per choice of gate 0's input pair, and it partitions the models exactly.
That fact is machine-checked on the real CNF — including by *asking the solver*
that forcing two cubes at once is UNSAT and that forcing none is UNSAT — and the
check is quoted in `logs/BANKED_LOGS.md` §L4. It is the natural first split.

Be warned that it was measured to cost **26× to 85× more total work** than one
monolithic solve of the same level: each cube re-derives from scratch what one
global solve learns once. It buys parallelism and resumability, not throughput.

## 9. Cost, before you start one

| level | expect |
|---|---|
| k = 9, 10, 11 | seconds to a couple of minutes on one core |
| k = 12 | of order an hour and a half on one core |
| k = 13 | of order a day; ≈ 233 core-hours was paid for it once |
| k = 14 | ≈ 99 core-hours by the fastest route seen (kissat 4.0.4, one process) |
| k = 15 | do not. The 15-gate program exists and is verified; there is nothing to decide |

Level-to-level growth is roughly 20–26×, measured rather than guessed.
