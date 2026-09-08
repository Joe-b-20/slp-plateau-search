# RUN.md — every command as typed, with the output it produced

Every command below is typed from the **pack root**. Every block of output is
pasted from a real run, unedited; none of it is illustrative. What the runs
establish, and what they do not, is [`STATEMENT.md`](STATEMENT.md).

To repeat the whole thing in one go:

```bash
sh run_all.sh
```

That is the script whose output this page reproduces. It re-runs the three cheap
levels and both legs of the positive control; it never starts k = 12, 13 or 14.

**Environment for the numbers below.** Linux, Python 3.12, `python-sat` with
**CaDiCaL 1.9.5**, one solver at a time, single-threaded, `nice -n 19`, on a
20-core machine that was carrying an unrelated long-running load throughout.
Timing is `time.monotonic` around the solve call. No standalone solver binary
was installed, so every solve went through `code/solve_dimacs.py`, which parses
the shipped DIMACS file and hands the solver **the clauses out of the file**.

Because of the background load these times move. The same three levels were
solved twice while this pack was assembled and came out at 2.84 / 24.67 /
119.49 s on the first pass and 0.98 / 9.13 / 72.82 s on the second. Read them as
evidence that the shipped files return the banked verdicts, not as a benchmark.

---

## 0. Instance facts

```
$ python3 code/instance_facts.py
```
```json
{
 "instance": {
  "file": "instance_joint_W3U4.json",
  "file_sha256": "d00504cbb8f19dc494d9edd93ee724d7075e262e82d76626e01d3f2f39de2d5b",
  "canonical_sha256": "d00504cbb8f19dc494d9edd93ee724d7075e262e82d76626e01d3f2f39de2d5b",
  "dim": 16,
  "lines": [2, 3, 4, 7],
  "n_inputs": 33,
  "n_targets": 8,
  "depth": null,
  "canonical_sha256_matches_pin": true,
  "instance_key": "f04dcb3ecf180a30204434a0bd32453e7635e8b6"
 },
 "rank_r": 16,
 "free_signals_m": 33,
 "targets_unrealised": 8,
 "lower_bound_L2": 9,
 "greedy_upper_bound": 16,
 "greedy_verify_slp": true,
 "greedy_why": "ok"
}
```

`lower_bound_L2: 9` is the proved floor the ladder starts from. `greedy_upper_bound: 16`
with `greedy_verify_slp: true` is the sanity control: a program for this instance
exists, was replayed, and does compute all 8 targets.

## 1. Every shipped CNF is the encoder's formula

```
$ for k in 9 10 11 12 13 14; do \
      python3 code/check_cnf.py cnf/k${k}_joint_W3U4.cnf --k $k \
              --json results/identity_k${k}.json; done
```
```
k=9   IDENTICAL  nv=12848  clauses=145670  roundtrip=True digests=True
k=10  IDENTICAL  nv=14739  clauses=169830  roundtrip=True digests=True
k=11  IDENTICAL  nv=16730  clauses=195823  roundtrip=True digests=True
k=12  IDENTICAL  nv=18823  clauses=223717  roundtrip=True digests=True
k=13  IDENTICAL  nv=21020  clauses=253580  roundtrip=True digests=True
k=14  IDENTICAL  nv=23323  clauses=285480  roundtrip=True digests=True
```

`roundtrip=True` means the file, parsed back, is literal-for-literal and in
order the same clause list a fresh `build_cnf(...)` produces. Full reports in
`results/identity_k*.json`.

## 2 – 4. The three cheap levels, re-run

```
$ python3 code/solve_dimacs.py cnf/k9_joint_W3U4.cnf  --json results/solve_k9.json
s UNSATISFIABLE
c solver cadical195  status UNSAT  seconds 0.98

$ python3 code/solve_dimacs.py cnf/k10_joint_W3U4.cnf --json results/solve_k10.json
s UNSATISFIABLE
c solver cadical195  status UNSAT  seconds 9.13

$ python3 code/solve_dimacs.py cnf/k11_joint_W3U4.cnf --json results/solve_k11.json
s UNSATISFIABLE
c solver cadical195  status UNSAT  seconds 72.82
```

### Measured against the record

| k | verdict re-run here | measured here | historical, encoding A, 1 core | historical, encoding B, 8 cores |
|---|---|---|---|---|
| 9 | **UNSAT** ✔ | 0.98 s (first pass 2.84 s) | — | 23.68 s |
| 10 | **UNSAT** ✔ | 9.13 s (first pass 24.67 s) | — | 123.82 s |
| 11 | **UNSAT** ✔ | 72.82 s (first pass 119.49 s) | 218.45 s | 785.29 s |

Three for three, verdicts agree. The measured times come in under the historical
ones; the historical runs were contended and, for encoding B, a different CNF
and a different generator, so the comparison is one of *verdicts*, not of speed.

### The three levels NOT re-run

| k | verdict | cost when it was paid | evidence |
|---|---|---|---|
| 12 | **UNSAT** | 5 761.73 core-s (1 core, encoding A); 5 202.15 s (8 cores, encoding B) | [`logs/BANKED_LOGS.md`](logs/BANKED_LOGS.md) §L2, §L3 |
| 13 | **UNSAT** | 105 083.40 s on 8 cores ≈ **233.5 core-hours** (encoding B) | [`logs/BANKED_LOGS.md`](logs/BANKED_LOGS.md) §L3 |
| 14 | **UNSAT** | 356 321.63 core-s ≈ **99.0 core-hours**, one process, kissat 4.0.4 (encoding A); independently confirmed by CaDiCaL 3.0.0 on the same hash-pinned CNF, 468 159.51 core-s ≈ **130 core-hours** | [`logs/BANKED_LOGS.md`](logs/BANKED_LOGS.md) §L1, and the two terminal lines in `logs/` |

k = 13 and k = 14 together are over 330 core-hours. They are documented, not
repeated. k = 14 is the decisive level. Each verdict there came from a complete
solver running the whole formula in one process, not from a partial cube sweep;
two engines on one CNF rule out an engine bug and leave an encoding bug open,
and there is no DRAT proof at k = 14. The scope of that is
[`STATEMENT.md`](STATEMENT.md) §4 and §5.

## 5. The positive control: identity and facts

```
$ python3 code/check_cnf.py positive_control/k7_SUB_U4tgts.cnf --k 7 --no-pin \
          --instance positive_control/instance_SUB_U4tgts.json
$ python3 code/instance_facts.py \
          --instance positive_control/instance_SUB_U4tgts.json --no-pin
```
```
control k=7 IDENTICAL nv=9330 clauses=102115 roundtrip=True
control: r=16 m=33 targets=4  proved lower bound=5  greedy=7 verified=True
```

Same encoder, same 33 free signals, same rank 16, same file format — one block's
4 targets instead of the merged block's 8. Its optimum is 7.

## 6. Positive control, negative leg — k = 6 must be UNSAT

```
$ python3 code/emit_cnf.py --k 6 --no-pin \
          --instance positive_control/instance_SUB_U4tgts.json \
          --out positive_control/k6_SUB_U4tgts.cnf
$ python3 code/solve_dimacs.py positive_control/k6_SUB_U4tgts.cnf
s UNSATISFIABLE
c solver cadical195  status UNSAT  seconds 0.58
```

## 7. Positive control, positive leg — k = 7 must be SAT

```
$ python3 code/solve_dimacs.py positive_control/k7_SUB_U4tgts.cnf \
          --model positive_control/k7_SUB_U4tgts.model
s SATISFIABLE
c model written to positive_control/k7_SUB_U4tgts.model
c solver cadical195  status SAT  seconds 1.19
```

**This is the run that matters most in the pack.** The same encoding, the same
supply, the same dimension, the same solver and the same file path that returns
UNSAT six times on the ladder returns SAT here. The ladder's UNSATs are
therefore about the instances, not about a formula that cannot say yes.

## 8. Decode the model into a program, and check it

```
$ python3 code/decode_model.py positive_control/k7_SUB_U4tgts.model --k 7 \
          --instance positive_control/instance_SUB_U4tgts.json --no-pin
```
```
model_check: 9330/9330 vars assigned, 102115 clauses checked, 0 unsatisfied
gates: [[8,17],[13,19],[11,23],[12,33],[33,34],[9,35],[34,35]]
verify_slp: ok  (33 inputs, 4 targets)
VERDICT: VALID 7-gate program for the block
```

All 102 115 clauses were re-evaluated under the model by the decoder itself —
the solver's word was not taken for it. The 7 gates were then replayed and all
4 target values found.

## 9. The decoded program vs an independently found witness

```
independently banked witness: [[8,17],[13,19],[11,23],[12,33],[33,34],[9,35],[34,35]]
decoded from the SAT model  : [[8,17],[13,19],[11,23],[12,33],[33,34],[9,35],[34,35]]
GATE-FOR-GATE IDENTICAL: True
```

The banked witness in `positive_control/expected_witness.json` was found by a
completely different route — a 528-way split on gate 0's input pair, hit at cube
144 — and verified there. Two unrelated routes, the same seven gates.

## 10. The decoder must reject a corrupted model

One literal of the verified model is flipped, and the decoder is run on it:

```
decoder exit code = 2   (2 = model does not satisfy the formula)
VERDICT: MODEL DOES NOT SATISFY THE FORMULA
unsatisfied clauses named: [3887, 33761, 44548, 60214, 79386, 97551]
```

A decoder that accepts anything proves nothing. This one names the clauses that
break and refuses to emit a program.

## 11. The oracle, on a complete MixColumns circuit

```
$ python3 code/verify_circuit.py positive_control/mixcolumns_88gates_depth7.json 7
```
```json
{
 "cmd": "python3 verify_circuit.py positive_control/mixcolumns_88gates_depth7.json 7",
 "returncode": 0,
 "stdout_tail": [
  "gates=88 depth=7 outputs_built=32/32 problems=0",
  "depth<= 7: OK",
  "VERDICT: VALID MixColumns circuit"
 ],
 "VALID": true,
 "circuit": "mixcolumns_88gates_depth7.json",
 "gates": 88
}
```

That circuit is the output of the programme's rehearsal of the SAT branch: the
constructive 15-gate program for the merged block was given to the circuit
generator, which emitted 88 gates at depth 7, and the oracle accepted it twice
in fresh processes. Depth is *computed* from the gate list, never read from the
file. This is what makes **88 − 15 + 14 = 87** an end-to-end fact rather than
arithmetic on paper: had k = 14 answered SAT, this same path would have emitted
an 87-gate circuit and verified it the same way.

## 12. Checksums

```
$ sh code/make_checksums.sh
$ sha256sum -c SHA256SUMS
```
```
files checksummed: 44
```

`sha256sum -c` then prints one `OK` line per file and exits 0.

`SHA256SUMS` covers the shipped artifacts. It deliberately excludes `results/`
and the files `run_all.sh` derives (`*.model`, `*_gates.json`,
`k6_SUB_U4tgts.cnf`), which a reader who re-runs the pack will overwrite.

## 13. DRAT proofs for every level this pack can afford to prove

```
$ sh run_proofs.sh
```

Proof logging turns each UNSAT into a certificate a checker can replay without
trusting the solver. Run separately from `run_all.sh` because it is heavier.

```
$ python3 code/emit_proof.py positive_control/k6_SUB_U4tgts.cnf --out proofs/k6_SUB_U4tgts.drat
s UNSATISFIABLE
c proof written to proofs/k6_SUB_U4tgts.drat  (52505 lines, 7848148 bytes)
c solver cadical195  status UNSAT  seconds 0.98

$ python3 code/emit_proof.py cnf/k9_joint_W3U4.cnf  --out proofs/k9_joint_W3U4.drat
s UNSATISFIABLE
c proof written to proofs/k9_joint_W3U4.drat  (65505 lines, 9182138 bytes)
c solver cadical195  status UNSAT  seconds 1.45

$ python3 code/emit_proof.py cnf/k10_joint_W3U4.cnf --out proofs/k10_joint_W3U4.drat
s UNSATISFIABLE
c proof written to proofs/k10_joint_W3U4.drat  (355058 lines, 135064503 bytes)
c solver cadical195  status UNSAT  seconds 15.96

$ python3 code/emit_proof.py cnf/k11_joint_W3U4.cnf --out proofs/k11_joint_W3U4.drat
s UNSATISFIABLE
c proof written to proofs/k11_joint_W3U4.drat  (1283970 lines, 845830878 bytes)
c solver cadical195  status UNSAT  seconds 110.39
```

All four levels carry proofs: the emission budget allowed 30 minutes per level,
and the slowest, k = 11, finished proof logging in 110 s. Proof logging costs
roughly 1.5× the plain solve (0.58 → 0.98 s, 0.98 → 1.45 s, 9.13 → 15.96 s,
72.82 → 110.39 s).

**Three of the four `.drat.xz` files ship; k = 11's does not.** Its compressed
refutation is 40 MB — larger than the rest of this repository combined — and it
takes 110 s to remake from the shipped CNF. `sh run_proofs.sh` emits it, and
[`proofs/README.md`](proofs/README.md) gives the one-command form and the
digests recorded when it was emitted here. The shipped `SHA256SUMS` does not
list it, so the §12 check passes on a fresh clone.

Structural validation of each — well-formedness, **not** a proof check:

```
$ python3 code/check_proof_format.py proofs/k9_joint_W3U4.drat --cnf cnf/k9_joint_W3U4.cnf
```
```
k6_SUB_U4tgts.drat       WELL-FORMED DRAT   lemmas=18711   deletions=33794   maxvar=7731  <= nv=7731   ends in empty clause=True
k9_joint_W3U4.drat       WELL-FORMED DRAT   lemmas=23230   deletions=42275   maxvar=12848 <= nv=12848  ends in empty clause=True
k10_joint_W3U4.drat      WELL-FORMED DRAT   lemmas=148849  deletions=206209  maxvar=14739 <= nv=14739  ends in empty clause=True
k11_joint_W3U4.drat      WELL-FORMED DRAT   lemmas=640177  deletions=643793  maxvar=16730 <= nv=16730  ends in empty clause=True
```

Every proof parses, mentions no variable outside its CNF, and ends in the empty
clause. **That is well-formedness, not verification.** No DRAT checker is
installed on this machine, so these proofs were emitted and validated here but
**not checked** here. Checking is one command:

```bash
xz -dk proofs/k9_joint_W3U4.drat.xz
drat-trim cnf/k9_joint_W3U4.cnf proofs/k9_joint_W3U4.drat     # expect: s VERIFIED
```

Sizes, sha256s of both the compressed and the uncompressed form, and the full
checking recipe are in [`proofs/README.md`](proofs/README.md).

---

## Summary of this pack's own runs

| step | what | outcome |
|---|---|---|
| 1 | 6 shipped CNFs vs a fresh build | 6/6 IDENTICAL |
| 2 | k = 9 re-solved from the file | **UNSAT**, 0.98 s ✔ matches banked |
| 3 | k = 10 re-solved from the file | **UNSAT**, 9.13 s ✔ matches banked |
| 4 | k = 11 re-solved from the file | **UNSAT**, 72.82 s ✔ matches banked |
| 5 | control CNF vs a fresh build | **IDENTICAL** |
| 6 | control at k = 6 | **UNSAT**, 0.58 s ✔ as required |
| 7 | control at k = 7 | **SAT**, 1.19 s ✔ the encoding can say yes |
| 8 | model decoded, all clauses re-checked, program replayed | **VALID 7-gate program** |
| 9 | decoded program vs independently found witness | **gate-for-gate identical** |
| 10 | corrupted model | **rejected**, exit 2, clauses named |
| 11 | 88-gate circuit through the standalone oracle | **VALID**, 32/32 outputs, depth 7 |
| 12 | checksums | all shipped files verified |
| 13 | DRAT proofs emitted for k = 6, 9, 10, 11 | 4/4 **WELL-FORMED**, emitted here, **not checked here**; 3 shipped, k = 11 regenerated on demand (110 s) |
| — | k = 12, 13, 14 | **not re-run** and **no proof**; banked UNSAT, see [`logs/BANKED_LOGS.md`](logs/BANKED_LOGS.md) |
