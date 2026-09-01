# The positive control

**An UNSAT ladder with no positive control is worth nothing.** A formula that is
subtly over-constrained — one bug that forbids a legal gate, one off-by-one in
the target coverage — is UNSAT at every k and looks exactly like a theorem. The
only way to tell the two apart is to make the same machinery answer **SAT** on a
question whose answer is already known by other means.

That is what this directory is. It is the non-negotiable half of the evidence in
`../STATEMENT.md`.

---

## The control instance

`instance_SUB_U4tgts.json` is a sub-instance of the merged block:

| | merged block (the theorem) | control |
|---|---|---|
| rank | 16 | 16 |
| free signals | 33 | **the same 33** |
| lines | {2, 3, 4, 7} | {2, 3, 4, 7} |
| targets | 8 (both blocks') | **4** (one block's) |
| optimum | 15 — the thing proved | **7** — known independently |
| proved lower bound | 9 | 5 |

Same encoder, same supply, same dimension, same DIMACS format, same solver, same
decode path. The only difference is which targets are asked for — and therefore
whether the answer is yes or no.

## Both legs are run

| leg | k | must be | measured |
|---|---|---|---|
| negative | 6 | UNSAT | UNSAT, 0.58 s |
| positive | 7 | SAT | **SAT, 1.19 s** |

A control that only ever says SAT would show nothing either. The k = 6 leg is
what shows the encoding is still capable of a negative on this very instance,
one gate below its optimum.

## The expected answer, from an unrelated route

`expected_witness.json` holds a 7-gate program for this instance found by a
completely different method: the level was split 528 ways on gate 0's input
pair, and cube 144 came back SAT. That witness was verified where it was found.

The model this pack solves decodes to **the same seven gates, in the same
order**:

```
[[8,17],[13,19],[11,23],[12,33],[33,34],[9,35],[34,35]]
```

Two unrelated searches, one answer.

## The decode, checked rather than trusted

`../code/decode_model.py` re-evaluates **all 102 115 clauses** of the control CNF
under the model before it decodes anything, then replays the decoded program and
confirms every one of the 4 targets appears. It exits non-zero if either check
fails — and it does: a copy of the model with a single literal flipped is
rejected with exit 2 and the offending clause indices named.

## The verifier leg — a real, finished circuit

A program for one block is not yet a MixColumns circuit, so the last leg runs
the standalone oracle on a complete one.

`mixcolumns_88gates_depth7.json` is the 88-gate, depth-7 MixColumns circuit that
the programme produced when it rehearsed the SAT branch end to end: the
constructive 15-gate program for the merged block was handed to the circuit
generator, which emitted a whole 32-in/32-out circuit, and the oracle accepted it
twice in fresh processes.

```bash
python3 ../code/verify_circuit.py mixcolumns_88gates_depth7.json 7
# gates=88 depth=7 outputs_built=32/32 problems=0
# depth<= 7: OK
# VERDICT: VALID MixColumns circuit
```

The oracle rebuilds MixColumns from GF(2^8) arithmetic — the specification is
that code, not a matrix file — and computes the depth from the gate list rather
than reading the number the file claims. Checking 32 basis inputs is a proof and
not a sample, because the map is linear over GF(2).

This is what makes **88 − 15 + 14 = 87** an end-to-end fact: the path that would
have turned a SAT at k = 14 into a record circuit exists, has been run on a real
witness, and ends in a verified circuit.

## Files

```
README.md                        this file
instance_SUB_U4tgts.json         the control instance, verbatim
k7_SUB_U4tgts.cnf                the positive leg, k = 7  (expect SAT)
k7_SUB_U4tgts_meta.json          variable map and digests
expected_witness.json            the independently found 7-gate answer
mixcolumns_88gates_depth7.json   a complete, oracle-verified MixColumns circuit
```

The negative leg's CNF (`k6_SUB_U4tgts.cnf`), the solver's model and the decoded
gate list are **derived**, not shipped: `sh ../run_all.sh` regenerates all three
(steps 6–10) so that a reader sees them produced rather than handed over.
