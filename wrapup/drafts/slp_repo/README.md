# MixColumns in as few XOR gates as possible

AES MixColumns is a 32×32 matrix over GF(2) (FIPS-197). This repo is a search
for the smallest circuit that computes it using only 2-input XOR gates.

**Result: 56 ≤ minimum ≤ 88.** The record is 88 gates. We never found an 87.
The search concluded in August 2026.

Check any circuit in this repo yourself:

```
python3 verify_circuit.py evidence/circuits/mixcolumns_88gates_depth5.json
```

It prints gate count, depth, how many of the 32 outputs are built, and a verdict.
It rebuilds MixColumns from the field arithmetic, so it trusts nothing else here.

## What we did and what we found

**The record is 88 gates.** We published five distinct 88-gate circuits, at
depths 5, 5, 6, 7 and 8. J. Jean found an 88 independently, by a different method, and
holds further unpublished ones.

**Fewest gates at each depth limit: 97 at depth 3, 91 at depth 4, 88 at depth 5.**
All verified. The 91 at depth 4 exists in three independent lineages.

**Lower bound: 56 gates.** Refereed, unconditional, with a certificate. A
separate certificate shows every depth-3 circuit needs at least 80 gates.

**The SAT test.** Take the two largest intermediate levels of a circuit and ask
whether they can be built together with *k* gates. At k = 9, 10, 11, 12, 13 —
and, decided 2026-09-01 after ~99 core-hours of solving — **14**, the answer is
proven no. A solution at 14 would have been an 87; there is none. So the merged
block costs exactly 15, merging the two largest levels saves nothing, and no 87
exists that is built the way every known 88 is built. The test assumes the
circuit splits into the same blocks, which an 87 need not do — that is the one
door this result leaves open.

**The census.** We hold 1,575,516 distinct verified 88-gate solutions. 28,796 of
them carry a build order and are directly runnable; 92 of those are at depth 5.
Every one passes a cheap check that would have handed us an 87 for free if it
failed: on the 28,796 with a build order, exactly 56 middle gates have a
consumer — the value forced on any 88 that cannot be shrunk by deleting a gate.
On all 1,575,516, no mask appears twice. Zero alarms in either half. The check
is one-way. Failing it gives an 87; passing it does not prove the circuit is
minimal.

**The negative space is large and empty.** All 139,878 harvested 88s are proven
irreducible when any two gates are swapped for one — 215,412,120 exact
decisions, zero reducible. Thirteen neighbourhoods around known 88s are closed
by exhaustion: 378,189 states, nothing below 88 gates in any of them. On the
depth-5 record, all 35,960 ways of dropping four output rows and rebuilding them
cheaper are refuted.

**And the honest caveat.** Our own control audit prices those negatives at
roughly nothing. The same test returns "irreducible" for 97-, 92-, 90- and
89-gate circuits alike. The measured distance from a circuit to a better one is
a median of 42 masks, against a search radius of 3 or 4. **A negative at radius 4
carries essentially no information about whether an 87 exists.**

**Calibration.** One from-scratch attempt with none of this project's knowledge
reached 93 gates. This project's methods reach 88.

## Opinion

This section is opinion, not proof.

We think 88 is optimal.

Four things push us that way. Jean reached 88 by a completely different method
and stopped there too. A free, always-on detector for one-gate improvements has
now run over 1.5 million distinct 88s and never fired once. Every relaxation we
could price came back at 88: 749,150 exactly-solved block floors with 88 as the
best anywhere, and a class-pricing bound covering 1.41×10²⁶ configurations, none
below 87. Loosening one block's budget buys a gate somewhere and gives one back
somewhere else, every time we measured it. And thirteen neighbourhoods of known
88s are closed by exhaustion with 88 as the floor in every one.

Against that: the same structural regularities hold for our 97-, 92- and 89-gate
circuits, so they may be facts about this problem rather than about 88. And the
width of the 88 plateau is not evidence either way — we tested that on small
instances with a certified optimum, and having many distinct optimal solutions
does not mean the optimum is too high.

An 87 would have to look unlike anything we hold. Outside the shared vocabulary
of every known 88. Not splitting into the block structure every known 88 shares
— the merged-levels route through that structure is now proven empty. Almost
certainly not shallow: the depth-3 floor is
already 80 and still climbing. And if its cancelling apparatus is as small as
the arithmetic allows — two cancelling gates against 85 clean ones — then one of
the twelve heaviest output rows must be produced by a cancelling gate. Our
circuits have between 9 and 28 cancelling gates. Nothing on disk is that shape.

## If you want to find an 87 (or prove 88 optimal)

**The last live case is now closed.** The k = 14 SAT test finished on
2026-09-01: UNSAT, in ~99 core-hours by a single solver on one core. The class
it covered — any 87 sharing the known 88s' block structure — is empty. What
remains open is only what the test never covered: an 87 with a different block
structure. One optional confirmation is priced and not run: re-deciding k = 14
under our second, independent SAT encoding (roughly 10× the cost of its k = 13
run).

**Already refuted — do not repeat.**

- Local search around known 88s out to radius 4. Exhausted, empty, and by our
  own audit worth close to nothing.
- Dropping up to four output rows and rebuilding them cheaper. Refuted.
- Free-move neighbourhoods of thirteen known 88s. Closed. Nothing below 88.
- One family of proof certificates is capped at exactly 91.41. It cannot reach
  the next step. Do not fund it.
- The cancellation-free route: proved between 92 and 102, and the exchange-rate
  arguments built on it die below where the real circuits sit.
- Searches restricted to symmetric circuits: about 12 gates worse.
- Searches over five or more planes: unbuildable, not merely unused. Zero of
  7,755 offered masks were ever selected.

**Best open leads, cheapest first.**

1. One SAT run at 11 gates on a single block. It closes the last loose gate in a
   bound covering 1.41×10²⁶ configurations, raising it from 87 to 88. Roughly 40
   core-hours; the levels below it are already done.
2. 28 search windows at budget 87 that were queued, prioritised, and never ran
   before compute stopped. This is the only certificate class here with no
   ordering caveat, and a solution would be a record. Resume is one command.
3. 498 verified 88-gate solutions from an independent algebraic frame that
   nobody ever analysed. They sit three steps further into the region where the
   theory places an 87 than any circuit we studied. Minutes to extract; the
   anchored search after that is unpriced.
4. Three unfinished routes to "every 87-gate circuit has depth 4 or more". One
   of them climbed the depth-3 floor from 32 to 63 in 17 minutes on one core,
   every rung proven, and was abandoned while still improving. Reaching 88 would
   be a publishable theorem.
5. Re-certify one inherited constant as a proof of infeasibility rather than a
   solver's best guess. One run. It is the only borrowed number that currently
   changes a conclusion, and several conclusions die if it fails.
6. The two-cancelling-gate region described above. Fully specified, never
   searched, and no instrument exists that aims at it. Cost unknown.

Our full method catalogue, corpora and certificates are available on request.

## Available on request

This repo ships the record circuits and their certificates. A much larger body
of working material is kept locally and is available on request.

- **1,575,516 distinct verified 88-gate solutions.** 28,796 carry a build order
  and run directly, 92 of those at depth 5; the rest are mask sets whose build
  order would need re-deriving. Two further large classes are counted but not
  deduplicated, so the true figure is between 1.6 and 4.4 million.
- **8 record circuits** (97 at depth 3, 91 at depth 4, 89 at depth 5, and five
  88s at depths 5, 5, 6, 7, 8) with a SHA-256 manifest, plus 11 fully packaged
  circuits with Verilog and testbenches.
- **A 93-gate circuit from an independent from-scratch effort** with no access
  to this project's methods — our calibration for how hard the last five gates
  are.
- **The lower bound `≥ 56`** with its certificate, and a certified depth-3 bound
  of 80 gates re-checkable in seconds.
- **A cancellation-free bound `≥ 92`**, derived twice independently, with 19
  exact certificates.
- **Proofs that the two largest levels cannot merge at 9, 10, 11, 12 or 13
  gates**, cross-checked at the cheap end by a second, independent encoding over
  an exhaustive 528-piece partition with a working positive control. The 14-gate
  case is packaged as a single 4.2 MB CNF and is open.
- **215,412,120 exact window decisions**, zero reducible, covering all 139,878
  harvested 88s.
- **378,189 fully enumerated neighbourhood states** across thirteen closed
  components, minimum 88 gates throughout.
- **749,150 exactly-solved block floors** (best anywhere: 88), 47,948 solved
  8-dimensional sector instances with replayable witnesses, and a class-pricing
  bound over 1.41×10²⁶ configurations.
- **Five theorems with checked proofs**, including the one-gate-improvement
  detector and a list of 14 properties forced on any 87-gate minimum circuit.
- **~160 append-only result ledgers**, ~770 write-ups, and ~9,800 raw run logs.

No circuit smaller than 88 gates was ever found. Everything above is checkable
with the verifier in this repo.

To ask for any of it, open an issue.
