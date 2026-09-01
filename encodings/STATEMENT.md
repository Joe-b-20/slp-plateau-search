# The block-structure theorem

**AES MixColumns, straight-line XOR circuits. The merged pair of the two blocks
that had not yet been priced together costs exactly 15 gates — not 14.**

Everything on this page is either a definition, a number taken from a solver
log that ships with this pack, or a run you can repeat from `RUN.md`. Nothing is
asserted that a script here cannot re-derive.

---

## 1. The problem, in plain words

AES MixColumns is a fixed 32 × 32 matrix over GF(2). It takes 32 input bits to
32 output bits, and every output bit is the XOR of some subset of the input
bits. To *implement* it is to write a **straight-line program**: a list of
two-input XOR gates, each combining two signals already available (an input, or
an earlier gate's output), such that all 32 output bits appear somewhere in the
list. Fewer gates is better. The fewest is unknown.

Two things about that:

* the best circuit anyone has published uses **88** gates, and nothing has ever
  reached 87;
* nobody has published a lower bound for this matrix at all.

So the interval between what is proved and what is built is enormous, and any
*exact* statement inside it — a level of a subproblem decided rather than
searched — is worth having. This pack contains one.

## 2. The decomposition, defined

Direct exact minimisation of a 32-output circuit is far out of reach. The
programme this pack comes from therefore **decomposes** the matrix and prices
each piece exactly.

**Lines.** The 32 output bits are read as 8 groups of 4, indexed 0 … 7. Call
each group a *line*. Every target of the matrix has its weight concentrated on a
small set of lines.

**Blocks.** For each line *j* there is a set of other lines that line *j*'s
outputs unavoidably depend on. A **block** is the subproblem of building line
*j*'s four output values while working only inside the lines it touches — its
**workset**. Two blocks are *adjacent* when their worksets overlap: they can
share intermediate values, so pricing them separately might over-charge for what
they have in common.

The two blocks this pack is about are the ones the programme labels **W3** and
**U4**:

| block | workset (lines) | dimension | targets | price, solved alone |
|---|---|---|---|---|
| W3 | {2, 3, 7} | 12 | 4 | **8 gates** (exact) |
| U4 | {3, 4, 7} | 12 | 4 | **7 gates** (exact) |
| **merged W3 \| U4** | **{2, 3, 4, 7}** | **16** | **8** | **the question** |

Their worksets **overlap in lines {3, 7}**. That overlap is what makes the pair
interesting: it is the last boundary in the decomposition that had not been
priced by a merged solve, and it was also the largest such boundary anyone could
afford to decide — 8 + 7 = 15 gates split, so the decisive question sits at
k = 14. (Earlier boundaries in the decomposition were closed the same way, by
merged solves; those that were decided returned "the boundary is free". The next
boundary up — absorbing a third block — splits as 4 + 8 + 7 = 19, is decisive at
k = 18, and prices out at roughly 10^7 core-seconds. It was not affordable and
was not attempted.)

**"The merged pair", precisely.** Delete the interface between W3 and U4
entirely. Do not posit any shared value, do not hand either side a value the
other built, do not charge for a handover. Instead pose ONE subproblem: given
the 33 signals that are genuinely free at that point in the circuit — which is
exactly the union of W3's 26 and U4's 25 — build **all 8** of the two blocks'
target values, in as few XOR gates as possible, working inside GF(2)^16 on lines
{2, 3, 4, 7}. That single subproblem is the object this pack ships, in
`instance/instance_joint_W3U4.json`.

**Two bounds bracket it before any solver runs.**

* **≤ 15, constructively.** Run W3's 8-gate program, then U4's 7-gate program.
  Both are programs over signals the merged block also has, so their
  concatenation is a valid 15-gate program for the merged block. This is the
  *replay bound*, and it is not a hand-wave: that 15-gate witness was built,
  replayed and checked, and then pushed all the way through the circuit
  generator to a complete, oracle-verified 88-gate MixColumns circuit — see
  `logs/BANKED_LOGS.md` §L5 and `positive_control/`.
* **≥ 9, by a proved counting argument.** Distinct target values must be
  produced by distinct gates, and a target whose value needs *d* inputs cannot
  sit earlier than position *d*. Maximising over the targets gives 9 for this
  instance. The bound and its proof are the (L2) paragraph in `code/slp_opt.py`;
  `code/instance_facts.py` computes it for the shipped instance and prints **9**.

  This bound is load-bearing, and not a formality. The CNF carries
  symmetry-breaking clauses, so it is not by itself monotone in *k*: a
  formula could in principle be UNSAT at k while a shorter program exists. The
  ladder therefore has to start at a floor it did **not** solve for, and 9 is
  that floor.

So the merged block costs somewhere in 9 … 15, and the interesting question is
whether it costs **14** — because 14 would mean the split pricing over-charges
by one gate, the whole circuit drops from 88 to 87, and a record falls.

## 3. The theorem

> **Theorem (block structure).** For the merged W3 | U4 block — 33 free signals,
> 8 targets, rank 16, pinned by the canonical sha256
> `d00504cbb8f19dc494d9edd93ee724d7075e262e82d76626e01d3f2f39de2d5b`
> and the instance key `f04dcb3ecf180a30204434a0bd32453e7635e8b6` — the decision problem
> "is there a k-gate XOR straight-line program producing all 8 targets" is
> **UNSATISFIABLE for every k = 9, 10, 11, 12, 13, 14**.
>
> With the proved lower bound of 9 and the constructive 15-gate program, the
> optimum of the merged block is therefore **exactly 15**.
>
> **Consequence.** Merging the two blocks buys nothing. The boundary between
> them is *free*: 15 merged = 8 + 7 split. In particular **no 87-gate
> MixColumns circuit exists whose W3 and U4 blocks are built jointly in 14
> gates.**

The soundness of reading UNSAT off a symmetry-broken formula rests on the three
normal forms the encoder adds — (N1) all signal values distinct and non-zero,
(N2) every gate is used, (N3) an adjacent-independence ordering — each of which
is proved in `code/slp_opt.py`'s docstring to preserve at least one **optimal**
solution. So if a 14-gate program existed, the k = 14 formula would be
satisfiable. It is not.

## 4. The ladder

Every level of the ladder, with the cost that was actually paid. "Encoding A" is
the encoder shipped here (`code/slp_opt.py`); "encoding B" is a second,
independently written CNF for the same mathematical question, from the same
programme. Times are wall-clock seconds on the stated number of cores.

| k | verdict | encoding A, 1 core | encoding B, 8 cores | re-run in this pack |
|---|---|---|---|---|
| 9 | **UNSAT** | — | 23.68 s | **2.84 s** ✔ |
| 10 | **UNSAT** | — | 123.82 s | **24.67 s** ✔ |
| 11 | **UNSAT** | 218.45 s | 785.29 s | **119.49 s** ✔ |
| 12 | **UNSAT** | 5 761.73 s | 5 202.15 s | not re-run (≈ 1.6 h) |
| 13 | **UNSAT** | — | 105 083.40 s ≈ **233.5 core-hours** | not re-run (≈ 29 h × 8) |
| 14 | **UNSAT** | **356 321.63 s ≈ 99.0 core-hours** (kissat 4.0.4) | — | not re-run (≈ 4 days) |

The three cheap levels were re-solved for this pack, **from the shipped DIMACS
files**, with an off-the-shelf solver and no access to the programme's own
harness; measured times and verdicts are in `RUN.md` and `results/`. The three
expensive levels are documented from their banked logs
(`logs/BANKED_LOGS.md`) and were deliberately not repeated: k = 13 and k = 14
together are over 330 core-hours.

k = 14, the decisive level, was decided by a single complete solver running the
whole formula in one process — not by a partial cube sweep. A separate cube
sweep on the same level had reached 90 of 528 cubes, all UNSAT, and was reported
as UNDECIDED throughout; it is consistent with the verdict and contributes
nothing to it.

**Growth, for anyone pricing a follow-up.** Level to level the cost multiplies
by roughly 20–26×. That is why the ladder stops here: k = 15 is not a
refutation anyone can afford, and does not need to be — the 15-gate program
exists and has been verified.

## 5. Two encodings, and why that matters

An UNSAT is a statement about a formula. It becomes a statement about
mathematics only if the formula is the right one. This ladder was decided twice,
by two CNFs written independently of each other for the same question:

* **Encoding A** — the encoder in `code/slp_opt.py`. Value variables `V[i][b]`,
  a one-hot pair-selector `Z[i][j]` per gate with a sequential at-most-one
  chain, target-coverage variables, and the (N1)–(N3) normal-form clauses. The
  DIMACS files in `cnf/` are its output, serialised clause for clause and in
  order.
* **Encoding B** — a different generator, from the programme's block-pricing
  tool, with its own variable layout. It decided k = 9 … 13.

They agree at **every level either has decided** — five levels, both UNSAT each
time.

Within encoding A there is a second agreement, of a different kind. Each of
k = 9, 10, 11 was decided two ways on the *same* formula: monolithically (one
solver, whole formula — this pack's own re-runs, `RUN.md` steps 2–4) and by a
528-way split on gate 0's input pair, which reported **528/528 cubes UNSAT** at
each of those levels. Same verdict both ways, three times. At k = 11 the two
solve *paths* inside the split route were also compared cube by cube: 528
compared, 0 disagreements.

Independently of all that, this pack's `code/check_cnf.py` re-derives each
shipped DIMACS file from the pinned instance and compares it to the file
literal-for-literal, in order. All six ladder files check out IDENTICAL; the
report for each is in `results/identity_k*.json`.

### Certificates, where they are affordable

Two solvers agreeing is still two solvers being trusted. A **DRAT proof** removes
that trust: an independent checker replays the refutation against the CNF and
needs to know nothing about the solver that wrote it.

This pack ships DRAT refutations for every level it can afford to prove —
**k = 9, k = 10, k = 11**, and the control's negative leg **k = 6** — in
`proofs/`, each with its sha256. All four were emitted from the shipped DIMACS
files (under four minutes of one core in total) and structurally validated:
every line parses, no variable falls outside the CNF, and each file ends in the
empty clause.

**They were emitted here and not checked here** — no DRAT checker is installed
on the machine that assembled the pack. Checking is one command
(`drat-trim cnf/k9_joint_W3U4.cnf proofs/k9_joint_W3U4.drat`), the recipe is in
`proofs/README.md`, and the published digests fix exactly what a checker would
be checking.

**k = 12, 13 and 14 carry no proof.** k = 14's solve alone was ~99 core-hours,
and its refutation would be very large. So the decisive level of the theorem
currently rests on complete solvers being correct, not on a checked certificate.
That is the honest boundary of this pack's evidence, and closing it is the most
valuable thing anyone could add.

## 6. The positive control — the encoding can say yes

**An UNSAT ladder with no positive control is worth nothing.** A formula that is
subtly over-constrained — a bug that forbids some legal gate, an off-by-one in
the target coverage — is UNSAT at every k, and looks exactly like a theorem.

So the same encoder, on the same free supply, at the same dimension, through the
same file format and the same solver, is made to answer **SAT** on a question
whose answer is independently known:

| | |
|---|---|
| instance | `positive_control/instance_SUB_U4tgts.json` — the identical 33 free signals of the merged block, but only **one** block's 4 targets |
| known optimum | **7** gates |
| the negative leg | at k = 6 the formula must be UNSAT |
| the positive leg | at k = 7 it must be SAT, and the model must decode to a real 7-gate program |
| independent answer to check against | the programme's own search found this witness by a completely different route (a 528-cube sweep, hit at cube 144) and banked it in `positive_control/expected_witness.json` |

Both legs were run for this pack. k = 6: **UNSAT** in 0.58 s. k = 7: **SAT** in
1.19 s; the model was decoded, every one of the 102 115 clauses re-checked under
it, the 7-gate program replayed, all 4 targets confirmed present — and the
decoded program is **gate-for-gate identical** to the banked witness. A
deliberately corrupted copy of the same model is **rejected**, with the
offending clauses named.

Finally, the leg that turns a block program into a circuit: the standalone
oracle `code/verify_circuit.py` — which rebuilds MixColumns from GF(2^8)
arithmetic and does not read the matrix from any file — is run on the complete
88-gate depth-7 circuit that the programme produced when it rehearsed this exact
compile path on the 15-gate witness. It returns `VERDICT: VALID MixColumns
circuit`, 32/32 outputs, depth 7. That is the arithmetic 88 − 15 + 14 = 87
confirmed end to end: had k = 14 answered SAT, this path would have emitted an
87-gate circuit and verified it.

Commands and pasted output: `RUN.md` steps 5–8.

## 7. Scope — what this does NOT say

Read this before quoting the theorem.

1. **It is not a lower bound on MixColumns.** It says the *merged block* costs
   15. It does not say the whole matrix costs 88, and it does not exclude an
   87-gate circuit that is not built this way.
2. **Block structure is a property of a chosen partition, not of a circuit.**
   Change the decomposition and the blocks change. "No 87 shares this block
   structure" is conditional on this partition, and the partition is named
   above so that the condition is checkable. Whether the known 88-gate circuits
   themselves respect this partition is a separate question, and this pack does
   not answer it.
3. **It closes one class, not the problem.** The honest statement is: *no 87
   exists whose W3 and U4 blocks are built jointly in ≤ 14 gates.* An 87 could
   still exist that re-cuts the matrix somewhere else entirely.
4. **The 88 record is not this programme's.** It was published independently;
   this programme reached 88 separately, from a different direction.
5. **Nothing here is claimed optimal for MixColumns.** The true minimum remains
   unknown.

## 8. Files

```
STATEMENT.md            this file — the theorem, the definitions, the scope
RUN.md                  every command as typed, with real pasted output
gen_and_solve.md        how to reproduce a level with any DIMACS solver
PROVENANCE.md           what was checked, what was edited, and the digests
run_all.sh              one command that reproduces every runnable step
run_proofs.sh           re-emit the DRAT refutations (heavier; separate on purpose)
SHA256SUMS              sha256 over the shipped artifacts

instance/               the instance, byte-for-byte, hash-pinned
cnf/                    the ladder k = 9 … 14 as DIMACS, with variable maps
proofs/                 DRAT refutations for k = 6, 9, 10, 11 — start at its README.md
positive_control/       the SAT control — start at its README.md
code/                   encoder, solver runner, identity checker, decoder, oracle
results/                every measurement made while assembling this pack
logs/                   excerpts of the banked logs for the levels not re-run
```

Read in that order. If you only read two things, read the theorem in §3 and the
positive control in §6.
