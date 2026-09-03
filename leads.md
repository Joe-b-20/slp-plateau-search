# Open leads

Everything below is unfinished. Each entry says what is open, what winning it
would prove, what it costs, and how to start. Several can be started in the
next five minutes with nothing but this repository and a Python interpreter;
those are first.

Read `NEGATIVES.md` before starting any of these. Most of the obvious attacks
are in that table already, and the `does_not_imply` field on each row is where
the previous attempt stopped being informative.

**Startability.** Each lead is marked:

- **runnable now** — the command is given and the files it needs are in these
  repositories.
- **requires the corpus** — needs the mask-set corpus, the solver harness, or
  the run archives, which are not in the public repositories (see the data
  inventory for exact counts and sizes).

**A note on what "winning" means.** Exactly two outcomes here would be a
genuine result: exhibiting an 87-gate circuit, or proving a lower bound above
56. Everything else on this list narrows a class or improves a depth record.
The list is ranked by payoff over cost, not by importance.

---

## 1. Point the deletion tripwire at other people's 88-gate circuits

**Runnable now.**

**Open.** Every circuit in this project's corpus came out of one family of
search engines. The tripwire — the free check that turns any duplicated or
unread gate into a smaller circuit — has never fired. On any population: the
**17,283** circuit files on disk at the census (the complete screen, file by
file), the **28,796** circuits carrying a full build order (the complete screen
including `B`), and the **1,575,516** distinct verified 88-gate value sets in
the corpus index
(the value-set checks only — `B` is a property of the wiring and cannot be
computed from a value set). Three populations, three different tests, all
silent; `INVENTORY.md` keeps them apart. It has never been run on a circuit somebody else's search
produced, apart from the one published 88 that is public.

**Why it is worth doing.** A hit **is** an 87, immediately, by deleting one
gate. A miss is also worth something: silence on circuits from an unrelated
search is the first evidence for the floor that is not confounded by this
project's own engine.

**Cost.** Seconds per circuit.

```
python3 tools/tripwire.py --selftest their_88.json    # prove the instrument fires
python3 tools/tripwire.py their_88.json               # then read the verdict
python3 verify_circuit.py their_88.json         # check it is a MixColumns
                                                # circuit in the first place
```

**Status of the one foreign circuit that is public.** The published 88-gate
circuit of J. Jean (ePrint 2026/1481) has been run: `B = 56`, no duplicates, no
dead gates, silent. That is one data point, and one is not a sample.

**What it does not settle.** The identity behind the tripwire holds at every
gate count, so a silent tripwire on a collection of 88s is not evidence that no
87 exists. It is a detector, not a bound.

---

## 2. Re-decide the shipped SAT instance on a different encoding

**Runnable now** (you supply the solver).

**Open.** The strongest structural result here is that a particular 16-bit
sub-block of the known 88s cannot be built in 14 gates. `SAT` on the shipped
instance means an 87-gate MixColumns circuit exists in that class; `UNSAT`
means it does not. It was **decided by kissat 4.0.4 and independently confirmed
by CaDiCaL 3.0.0 on the same hash-pinned instance** — two engines, both terminal
lines shipped as `encodings/logs/mono_14_kissat404.log` and
`encodings/logs/mono_14_cadical300.log`. That is engine-level redundancy and
nothing more. **There is no DRAT proof at k = 14**, and both engines read the
*same CNF*, so a **third engine or a cross-encoding reproduction remains open** —
that is what this lead is.

**Why it is worth doing.** Two engines on one file rules out an engine bug; it
does not rule out an encoding bug, and a wrong encoding is UNSAT for free. The
second encoding in this programme currently reaches only k = 13
(`encodings/logs/BANKED_LOGS.md` §L3), so the decisive level has never been
decided twice *independently of the encoding*. A cross-encoding decision either
promotes this from "our formula says so" to a fact about the mathematics, or
finds the bug. A DRAT refutation would settle it outright.

**Cost.** The original solve took 356,321 core-seconds — about 99 core-hours —
with kissat 4.0.4; CaDiCaL 3.0.0's confirmation took 468,160 core-seconds ≈ 130
core-hours. A third engine on the shipped file is priced in that range. A second
*encoding* of the same question is priced at roughly ten times the cost of the
size below it, which is hundreds of core-hours. This is expensive; it is listed
high because the *artifact* is one 4.3 MB file and needs nothing else.

```
<your-solver> encodings/cnf/k14_joint_W3U4.cnf
```

**What it does not settle.** Even a confirmed UNSAT is class-conditional: an 87
outside that decomposition is untouched. The decomposition it lives inside is a
choice of ours; whether every known 88 respects it was not verified, and the
companion records repository ships a verified 91-gate depth-6 circuit whose
gate 70 (line support `{2, 3, 4, 7}`) fits no single block of it. That is a live
defect, and it is the reason this lead is about *reproducing* the result rather
than extending it.

---

## 3. Push the one circuit that breaks the dictionary down to 88 gates

**Runnable now** for the verification; **requires the corpus** for the descent
harness.

**Open.** Across 1,925,065 verified 88-gate circuits and 107,803,640 gate
slots, only 1,778 distinct intermediate values ever appear. A verified 89-gate
circuit exists that is built around a value outside that list — delete it and
six values become unbuildable, four of them outputs. No descent has ever
*started* from that circuit; every previous run burned its budget getting down
from 149 gates and never reached it.

**Why it is worth doing.** Reaching 88 from there would produce the first
88-gate circuit ever exhibited outside the dictionary — a new structural object
and an entrance to a region of the plateau nothing has sampled. Failing
repeatedly is the sharpest available evidence that the 88s really are confined
to those 1,778 values.

**Cost.** About one core-hour for a first answer; about twenty for the full
set. It is a two-line seed change to a harness that already exists — the
cheapest thing on this list by an order of magnitude.

```
python3 verify_circuit.py corpus/vocabulary/S89_out_of_vocabulary_89gates.json
# gates=89 depth=10 outputs_built=32/32 problems=0
# VERDICT: VALID MixColumns circuit
```

**What it does not settle.** Whatever it returns is a search result in one
direction only. Reaching 88 is a positive existence result; not reaching 88
proves nothing at all.

---

## 4. The 28 search windows at record-breaking budget that were never run

**Requires the corpus.**

**Open.** A queue of exact search windows was audited and found to have decided
only the 210 windows priced at the current record. The 28 windows priced one
gate *below* it — the only ones in the queue whose success would be a record —
were reprioritised to run first, and compute stopped five days later. Verified
independently: 210 windows at budget 88 decided, 28 windows at budget 87 with
any result at all: **zero**.

**Why it is worth doing.** A success is an 87-gate circuit. This is the only
window family in the project with no caveat about the order slots were filled
in, and the resume is idempotent — restarting costs nothing already spent.

**Cost.** Not separately priced; the queue and its driver are on disk and the
run resumes where it stopped.

**What it does not settle.** 28 windows over 7 anchor circuits. Emptiness there
is another bounded-radius negative.

---

## 5. Close the last gate in the exhaustive pricing bound: 87 → 88

**Requires the corpus.**

**Open.** An exhaustive price over 1.41 × 10²⁶ ways of budgeting the circuit's
shared sub-expressions returns "at least 87". Nine of its ten component bounds
are exactly tight; all the slack sits in one sub-problem. Deciding that
sub-problem raises the whole bound from 87 to 88 and closes the family.

**Why it is worth doing.** It would make "88 is optimal" a proved statement
*within that class* — over 10²⁶ configurations, unconditionally. That is the
strongest positive result available anywhere on this list.

**Cost.** About 150,000 seconds of solver time against the 33,000 already
spent. The ladder below it is already decided: sizes 6 through 10 are UNSAT at
37, 57, 208, 1,145 and 13,140 seconds respectively. The ledger records the run
as *stopped by the operator*, not refuted.

**What it does not settle.** Class-conditional, like every price in this
project. The class is not proved to contain an 87, and its load-bearing wiring
assumption was measured on 22 circuits with one exception and never proved.

---

## 6. Re-certify the one inherited number that still changes a conclusion

**Requires the corpus.**

**Open.** A bound of 92 on an integer sub-problem is currently only a solver's
best objective bound, bracketed at [92, 94], never re-certified as an
infeasibility proof. Three downstream floors rest on it.

**Why it is worth doing.** It is the only inherited numeral in the project that
still changes a conclusion, and settling it deletes the one branch of the case
analysis that describes an 87 unlike anything ever built. Highest
value-per-hour on the board.

**Cost.** One constraint-programming run; measured at 3–12 hours on one worker,
with a real chance of returning UNKNOWN. There is a symmetry in the problem
worth a free factor of four that no existing encoding exploits — break that
first.

**What it does not settle.** Even if it lands, the proof family it belongs to
has a proved ceiling that sits below the records' own measured range. Fund it
knowing that.

---

## 7. A 90-gate circuit at depth 4 — one capped solver call away

**Requires the corpus.**

**Open.** The depth-4 rung prices as `79 + X`, where `X ≥ 11` is proved, so the
rung is at least 90. It equals exactly 90 if and only if `X = 11`. Two attempts
timed out at ten hours; the ladder below is decided (sizes 6 through 10 UNSAT
at 40, 66, 251, 1,243 and 7,974 seconds).

**Why it is worth doing.** It is not an 87, but it is the most *publishable*
single item on this list: a new point on the public depth-versus-size frontier,
which currently reads 97 at depth 3, 91 at depth 4, 88 at depth 5.

**Cost.** Exactly one capped solver call, with the size cap set so that UNSAT
is a machine-checked negative rather than a timeout.

**What it does not settle.** The counter-prior is real: the lane's own repair
probe shifts toward 12, and 49 depth-capped search restarts produced forty
circuits at 91 gates, nine at 92, and none at 90 or below.

---

## 8. Finish the 87-detector sweep over the larger population

**Requires the corpus.**

**Open.** A detector whose alarm yields an 87 outright has been run on 1,800 of
18,355 corpus circuits — 6.5% coverage — returning zero hits on valid 88s and
66 hits on deliberately broken controls. The population it scans is strictly
larger than the one the corpus-wide deletion certificate covers, so the
remaining 93% is genuinely new coverage, not a re-run.

**Why it is worth doing.** A hit is an 87. A clean sweep is the first
corpus-wide result for this population.

**Cost.** About 80 CPU-minutes. One CPU-hour of always-on 87 detection that
nobody has bought.

**What it does not settle.** Same fence as every corpus-wide negative: it is a
statement about circuits reachable from this project's engines.

---

## 9. Analyse the 498 verified 88-gate circuits nobody has read

**Runnable now** for the verification half; **requires the corpus** for the
search that follows.

**Open.** Three search jobs were still running when the campaign was written
up, and their output was never read. It contains 498 distinct 88-gate circuits,
none of which matches any published circuit, and 13 of the 13 converted so far
verify as valid MixColumns.

**Why it is worth doing.** Two things. First, they already refute three claims
this project published about the structure of the plateau — a supposed floor, a
supposed empty band, and a supposed ridge — and those corrections are banked.
Second, they sit three gates further into the structural corner where one
theory places an 87, which makes an anchored search from them strictly cheaper
and strictly closer to a witness than anything tried.

**Cost.** Converting and verifying all 498: minutes. The anchored search after
that: unknown.

```
python3 verify_circuit.py <converted_circuit.json>
python3 scripts/overlap.py <converted_circuit.json> \
        evidence/circuits/mixcolumns_88gates_depth5_fromscratch.json
```

**What it does not settle.** The two cheap routes to an 87 point in *opposite*
directions — the correlation between the two statistics they optimise is
strongly negative, so driving one down drives the other up. And these 498 are
not the best anchors known for the theory that motivates them.

---

## 10. Decide the 182 structural families that were never reached

**Requires the corpus.**

**Open.** A queue of 204 structural families was ordered hardest-first, but
results were written as they finished — so the 22 rows that exist are the easy
ones. Seven of the eight families in which a circuit spends more gates than it
has independent obligations are undecided, including both extreme cases, which
appear in no earlier sample. Two independent censuses agree on which eight
those are. One family's search was still running, with its positive control
passing, when it was killed.

**Why it is worth doing.** These are the only frames in which this project's
own structural argument does not rule out an 87. A completion in one of them is
an 87.

**Cost.** The remaining work list is on disk in priority order and the runner
takes one family at a time on a single machine.

**What it does not settle.** A completion is sufficient for an 87; its absence
is not necessary for any bound.

---

## 11. The one region the arithmetic still permits, that nothing has ever searched

**No instrument exists.**

**Open.** The case analysis leaves exactly one branch standing: an 87 with
exactly two cancelling gates and eighty-five clean ones, with one of the twelve
heaviest output bits produced by a cancelling gate. That is 63 of 475
admissible parameter pairs, and it looks like nothing on disk.

**Why it is worth doing.** A hit is an 87 of an entirely new shape. This is the
sharpest positive lead the project holds and it has never been aimed at,
because no tool here can aim at it.

**Cost.** Unknown. Building the instrument is the lead.

**What it does not settle, and what must travel with it.** Measured across 498
circuits, the statistic this region requires to be 2 has a minimum of 18;
nothing measured is within 16 of it. So: *for* the floor, the region is empty of
88s in every population ever measured. *Against* the floor, it is also
unsearched, and "empty" and "never looked" cannot be told apart from here. Note
too that the cheapest way to kill this branch is lead 6, not a search.

---

## 12. Publish the cascade search that found the shipped 91 @ depth 4

**Requires the corpus.** This is the one entry here that is **packaging rather
than search**: winning it proves nothing new about MixColumns. Most of it is
now done, and what is left is recorded so that nobody thinks the whole gap
closed.

**Closed on 2026-09-03.** All three frontier points now reproduce from nothing
with one command each: `reproduce/reproduce.py` for the 97 @ 3 (57 s),
`reproduce/construct_91at4.py` for the 91 @ 4 (3.9 s), and
`reproduce/hunt_88at5.py` for the 88 @ 5 (archived 64 min). The 91 @ 4's command
is the exact ladder construction, packaged with the ten generator modules it
needs and one stated exception to `reproduce/`'s stdlib-only contract: it needs
`numpy` and `python-sat`. It emits an independent, oracle-verified 91 @ depth 4
sharing 53 of its 91 values with the shipped circuit, so it is a second witness
rather than a copy, and its provenance was tested rather than assumed — under an
audit hook the run reads no file in the repository but its own modules, and the
module holding the record-read currency menus is not imported at all.

**Still open.** The multi-process cascade *search* that historically produced
the shipped file is unpublished. Archiving it means the worker plus its root
(`constructors.build("naive", 40426)`, chunk seed 40426, depth cap 4, `alt`
mode, cascade handoff off; **54.4 min** of one core, inside a ~74 process-hour
run). It is worth less than the construction it would sit beside — it is slower
by three orders of magnitude and stochastic — which is why it was not the thing
packaged first.

**Cost.** No compute. A worker, its config and its logs, lifted and documented.

**What it does not settle.** Nothing about MixColumns — this buys
reproducibility rather than knowledge. Note also what the shipped construction
is *not*: a blind search finding 91 by luck. It is a construction whose *model
class* prices out at exactly 91 — which is a statement about that class, **not**
a lower bound on MixColumns, and not a claim
that 90 @ 4 is impossible. 90 @ 4 remains undecided; see lead 7. A
blind cap-4 descent to 91 was measured at **3.9 core-hours** in a different lane,
and 9 of 9 restarts from this project's own 92 @ 4 ended at 92 — so do not offer
the pipeline's existing `--mode cascade --stop-gates 92 --stop-depth 4`
retargeted at 91: on the archived evidence its depth-4 rung reaches 92 and no
further. (The stop test itself was fixed on 2026-09-03 and no longer latches
shut when a deeper rung goes below 91 gates.)

---

## Two things this page will not say

**That the unsearched region is empty.** It is unsearched *and* unpopulated,
and nothing in this repository distinguishes those.

**That any negative on this page or in `NEGATIVES.md` is a bound.** Not one of
them is. The local ones return the same verdict about 89-, 91-, 92-, 94- and
97-gate circuits as they do about the 88s, at a likelihood ratio of about 1.00,
against a measured median distance of 42 values between genuinely different
optima.
