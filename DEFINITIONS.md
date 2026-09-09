# Definitions

Every term this project uses that a reader could not guess, defined once, in
plain words. Where the term names something a program can decide, the command
that decides it is given underneath. If a term is used anywhere in these
repositories and is not on this page, that is a bug — please report it.

Terms are ordered so that each one only uses terms above it.

**Every command on this page is written to be run from the root of this
repository, unchanged, against files that ship here.** Where a command takes a
`<placeholder>`, substitute your own file.

---

## straight-line program (SLP)

A list of instructions with no branches and no loops: every line combines two
values computed on earlier lines (or two inputs) and names the result. That is
all a circuit is here — the repository name abbreviates it.

Concretely, our circuits are straight-line programs whose only operation is
2-input XOR, over 32 input bits.

---

## gate

One line of the program: `signal k = signal a XOR signal b`, with `a` and `b`
strictly earlier. Signals `0..31` are the circuit's inputs; gate number `k`
(counting from 0) produces signal `32 + k`. **Gate count** is the number of
lines. That is the quantity being minimised.

---

## value — also called a *mask*, or an *intermediate value*

Every gate XORs together some subset of the 32 circuit inputs. Write that
subset as a 32-bit number, one bit per input. That number is the gate's
**value**: bit `j` is 1 if and only if input signal `j` is among the inputs
XORed together.

A value says *what* a gate computes and says nothing about *how* — two circuits
can reach the same value by different routes. Almost every structural statement
in this project is a statement about values.

**Value is the word used throughout these pages.** *Mask* is the same thing and
is what the code, the file formats and some command output call it; the two are
interchangeable. We avoid the word "word"; AES already uses it for something
else.

```
# print the value of every gate in a circuit, and how two circuits' values overlap
python3 scripts/overlap.py evidence/circuits/mixcolumns_88gates_depth7.json <other.json> --list-shared
```

---

## output value / target

MixColumns is a fixed 32×32 matrix over GF(2). Row `r` of that matrix, read as
a 32-bit number, is the value output bit `r` must have. Those 32 numbers are the
**targets**. A circuit is correct exactly when all 32 appear as values somewhere
in it — nothing else is required, and no test vectors are needed.

The matrix is shipped as `matrix.txt` with its sha256, and is rebuilt from the
GF(2^8) field arithmetic by the verifier, never read from a file.

```
python3 verify_circuit.py <circuit.json>
# prints: gates=<n> depth=<d> outputs_built=32/32 ... VERDICT: VALID
# e.g.  python3 verify_circuit.py evidence/circuits/mixcolumns_88gates_depth5.json
```

---

## why 32 basis vectors is a proof and not a sample

The map is linear over GF(2). A linear map is completely determined by its
values on a basis, so checking the 32 unit inputs checks the map on all 2^32
inputs at once. The verifier does not even do that much work: it compares value
sets, which is the same statement in one step.

---

## depth, and level

The **depth** of a gate is the length of the longest chain of gates from an
input to it: an input has depth 0, and a gate has depth one more than the
deeper of its two parents. The **depth of a circuit** is the largest depth of
any gate. It is the critical path in gate delays.

A **level** is a depth class: level `d` is the set of gates at depth exactly
`d`. "The two largest levels" means the two depth classes containing the most
gates. Levels partition the gates; they have nothing to do with outputs.

Depth is always *computed* from the gate list in this project, never asserted
by the file that claims it.

```
python3 verify_circuit.py <circuit.json> <max_depth>
# exits non-zero if the measured depth exceeds max_depth
# e.g.  python3 verify_circuit.py evidence/circuits/mixcolumns_88gates_depth5.json 5   # exit 0
#       python3 verify_circuit.py evidence/circuits/mixcolumns_88gates_depth5.json 4   # exit 1
```

**Why depth 3 is the minimum for MixColumns.** Twelve of the 32 output bits
depend on 7 input bits. A tree of 2-input gates of depth `d` has at most `2^d`
leaves, so producing a value depending on 7 inputs needs depth at least
`ceil(log2(7)) = 3`. Hence no MixColumns circuit has depth 2, and the shipped
97-gate depth-3 circuit is at the minimum possible depth.

---

## fan-out

The number of later gates that read a given signal. **Maximum fan-out** is the
largest such number over all signals in the circuit; it is the metric a
hardware integrator cares about, because a high-fan-out net needs buffering.

Fan-out is computed from the gate list alone, so any shipped circuit can be
measured directly; the tripwire prints the per-signal user counts it derives on
the way to `B`. The project's per-circuit fan-out histograms over the full
corpus are held locally and are not shipped (`INVENTORY.md`).

---

## output gate, working gate, and B

A gate is an **output gate** if its value is one of the 32 targets. Everything
else is an intermediate. An intermediate gate is **working** if some later gate
reads it, and **dead** if nothing does.

**B** is the number of working gates: gates that are not outputs and do feed
something.

**Why B has a forced value.** A valid circuit puts all 32 targets on gates, so
at least 32 of its `n` gates are output gates, so at most `n − 32` are not, so
`B ≤ n − 32`. If `B` is smaller than that, some intermediate gate was left out
of the count, and there are only two ways that happens: the gate is dead
(delete it), or two gates carry the same target so fewer than `n − 32` gates
are left over (delete the later one). Either way you have an `(n−1)`-gate
circuit, constructively, with no search.

So for an 88-gate MixColumns circuit `B = 56`, and `B ≠ 56` **is** an 87.

This is a two-line counting argument and a sanity screen, not a deep theorem,
and it should not be cited as one. Note also that the arrow only runs one way:
`B = 56` does **not** mean no gate is deletable.

```
python3 tools/tripwire.py <circuit.json>          # reports B, its expected value,
python3 tools/tripwire.py --selftest <known.json> # duplicates and dead gates
# e.g.  python3 tools/tripwire.py evidence/circuits/mixcolumns_88gates_depth5.json
#       -> n=88 B=56 expect=56 ... silent
```

---

## irreducible

Used in two different senses in this project, and they must not be confused.

1. **Irreducible (the tripwire sense).** No gate is deletable by the two
   mechanisms above: no two gates carry the same value, and no intermediate
   gate is dead. This is the hypothesis under which `B = n − 32`. It is
   decidable in milliseconds — `tripwire.py` decides it.

2. **Irreducible at radius k (the search sense).** No way of deleting `k`
   gates and optimally resynthesising the hole produces a smaller circuit.
   This is expensive, it is relative to `k`, and `k` is always stated.

Sense 1 is cheap and weak. Sense 2 is expensive and, per this project's own
audit, still weak — see `NEGATIVES.md`.

---

## cancellation-free

A gate **cancels** if its two input values share a set bit: that bit appears
twice in the XOR and vanishes. A circuit is **cancellation-free** if no gate
does this — formally, if `popcount(mask(a) & mask(b)) == 0` at every gate.

Cancellation-free circuits are the easy case: without cancellation the problem
is a covering problem and admits a lower-bound argument. That argument gives
**92** for MixColumns, and the best cancellation-free circuit known has 102.
Every record circuit here cancels, so 92 is *not* a lower bound on the real
problem — it is a measurement of how much cancellation is worth, which is at
least 4 gates.

```python
# the predicate, in full
def cancels(mask_a, mask_b):
    return bin(mask_a & mask_b).count("1") > 0
```

---

## block structure

Partition the 32 output bits into groups, and partition the gates by which
group of outputs they serve. The resulting shape — which groups exist, how many
gates each needs, which gates are shared between groups — is a circuit's
**block structure**.

It is a property of a chosen decomposition rather than an intrinsic invariant
of the circuit: change the partition and you change the block structure.
Statements of the form "no 87 shares the block structure of the known 88s" are
therefore conditional on the decomposition, which is why every one of them in
these repositories is scoped *under our block decomposition* and names it. The
decomposition this project's block reasoning uses is a choice, and which
circuits respect it has been measured: 5 of the 5 published 88s, and 23,456 of
the 28,796 corpus 88s with a build order on disk — 81.5 %. The check can fail,
and does: the companion records repository ships a verified 91-gate depth-6
circuit whose gate 70 has line support `{2, 3, 4, 7}` and so fits no single
block of it. The 18.5 % that violate almost all carry one value spanning lines 0
and 2, which no block holds together. So a block-structure statement covers that
81.5 % class and the five published 88s, and says nothing outside it.
Measurement to be published with the toolkit. The decisive level of the theorem
stated over this decomposition also carries no DRAT proof.

---

## vocabulary

The union of all values appearing in a collection of circuits. Across 1,925,065
verified 88-gate circuits and 107,803,640 gate slots, only **1,778** distinct
non-target values ever appear; that set is "the vocabulary".

It is an observation about a corpus, not a constraint on circuits. A verified
89-gate circuit exists that is built around a value outside it, which is what
tells us leaving the vocabulary costs at most one gate.

```
python3 verify_circuit.py corpus/vocabulary/S89_out_of_vocabulary_89gates.json
# gates=89 depth=10 outputs_built=32/32 problems=0 -> VERDICT: VALID
python3 corpus/vocabulary/tools/oov_check.py   # -> 6 out-of-vocabulary values
```

---

## distance, and radius

The **distance** between two circuits is the number of values in one that are
not in the other — the size of the symmetric difference of their value sets,
usually reported as the count on one side. In plain words: **how many of the
gates' values you would have to change** to turn one into the other.

The **radius** of a search is the largest distance it looked out to. "Radius 2"
means every circuit within 2 changed values was examined.

The number that matters when reading any radius-limited negative: the measured
distance between two genuinely different optima for this map is a **median of
42**, and searches in this project reach 3 or 4.

```
python3 scripts/overlap.py A.json B.json
# "only in A" and "only in B" are the two one-sided distances
# e.g.  python3 scripts/overlap.py evidence/circuits/mixcolumns_88gates_depth7.json \
#           evidence/circuits/mixcolumns_88gates_depth5.json
```

---

## orbit

Fix a set of rewriting moves that do not change the gate count — re-associating
an XOR chain, re-parenting a gate onto a different pair that computes the same
value. Start from one circuit and apply moves until nothing new appears. The set
you reach is that circuit's **orbit** under those moves.

An orbit is closed by construction against the moves that generated it, and
says nothing about circuits those moves cannot reach.

---

## counting certificate

A lower-bound argument of the form: assign a numeric weight to each value, show
that one gate can increase the total weight by at most some amount, and
conclude that reaching the targets from the inputs takes at least
`(target weight − input weight) / (gain per gate)` gates. The **certificate**
is the file of weights: checking it is arithmetic, and needs no solver and no
trust in the program that found it.

This is what produces the unconditional bound of **56**. The certificate for it
is a file you can check by hand.

The family has a proved ceiling: no assignment of weights in this family can
push the bound past 91.41 for this matrix, so it is not a route to 88.

---

## pricing, and a pricing bound

Take the circuit apart along some structural line — by output group, by depth
level, by which shared sub-expressions are allowed — solve each piece exactly,
and add up the costs. The total is a **price**. If the decomposition is valid
for every circuit in a class, the price is a lower bound *for that class*.

"Prices back to exactly 88" means: this way of taking the problem apart, solved
exactly, gives 88 and not less. Two hundred such decompositions do this.

Every one of them is **class-conditional**. The class is defined by the
decomposition, and none of these classes is proved to contain an 87. A price of
88 across many classes is evidence about the classes, not about `L(M)`.

---

## realisable / non-realisable

Given a set of values (no wiring), ask whether *some* circuit of the stated size
builds exactly that set, with every gate free to take any two earlier signals.
"Allowing arbitrary rewiring" means exactly that: the wiring is not inherited
from the circuit the value set came from; it is re-derived from scratch, over
all possible wirings.

A value set is **non-realisable at size k** if no such circuit exists. This is a
decidable question about the value set alone, and it is what the single-deletion
certificate decides 88 million times.

---

## verified, certified, known

Three tiers, and they are not interchangeable:

- **verified** — the circuit file exists and passes `verify_circuit.py`.
- **certified** — verified, *and* the specific structural computation being
  cited was run on it and banked with its ledger row.
- **known** — appears somewhere in this project's corpus of value sets. Most
  known 88s have no build order on disk and are therefore not verified as
  circuits; they are verified as value sets.

Never read "known" as "verified". The counts differ by more than an order of
magnitude.

---

## lineage, and foreign lineage

A circuit's **lineage** is the chain of circuits its search descended from.
Two circuits share a lineage if one's search was seeded, directly or
transitively, by the other.

**Foreign lineage** means: produced by somebody else's search, with no seed
from ours. It matters because every circuit in this project's corpus came from
one family of search engines, so corpus-wide regularities may be properties of
the engine rather than of the problem. Circuits from another author's search
are the cheapest available test of that.

We use "another author's search" in preference to "foreign lineage" in public
text; the term is listed here because it appears in older files.

---

## the 89–97 control group

Circuits at 89, 91, 92, 94 and 97 gates that are known **not** to be optimal,
used as a control: any test claiming to detect optimality must behave
differently on them than on the 88s. Several of this project's structural tests
do not, which is why those tests are reported as near information-free. Running
a test on the control group before believing its verdict on the 88s is the
single most useful habit in this repository.
