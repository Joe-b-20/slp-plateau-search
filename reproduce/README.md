# reproduce — one command per record, with its measured time

Everything here is dependency-free Python 3 (stdlib only). **Six of the nine
verified circuits have a reproduction command** — four run from this folder, two
are pipeline runs — and the table below carries all six. Three have none: the
**91 @ depth 4**, for which two from-scratch routes exist and neither is
published yet — one of them a **2-second** construction
([why](#the-91--depth-4--no-command-here-and-what-produced-it-instead)) — and the
**derived 88 @ depth 5** and **88 @ depth 8**, which are derived work and are not
offered as recipes ([why](#the-three-circuits-with-no-command-here-and-why)).

Two of the three **current frontier points** — 97 @ 3 and 88 @ 5 — are
reproducible from scratch *with a command in this folder*, no seed circuit of
any provenance. The third, 91 @ 4, has no command here — though a 2-second
from-scratch construction for it exists in the project's unpublished tree and is
measured [below](#a-91--depth-4-in-two-seconds). That gap is stated rather than
papered over.

**A reproduction command need not be the tool that historically found the
record.** Where a faster honest route exists it is named, with what it is, how it
differs from the original finder, and what "from scratch" means for it — the
bar being *no record circuit and no record-derived data as input; targets from
GF(2⁸) and FIPS-197 only*.

Every search is stochastic. Times below are **what a run actually took**, dated
and labelled — a measurement, never a promise.

| what it reproduces | command | measured |
|---|---|---|
| **97 @ depth 3, from scratch** — *frontier* | `python3 reproduce.py` | **57.4 s and 51.8 s** in two runs, one core, re-run 2026-09-02 (RNG seed 6, its first seed, both times); **81 s** on 2026-07-27; 60–156 s across earlier runs |
| **91 @ depth 4** — *frontier* | *none here yet* — but a **2-second** from-scratch construction exists outside this repository, and it is the fastest reproduction of any record this project has: [see below](#a-91--depth-4-in-two-seconds) | **2 s** measured 2026-09-02, cold cache, one core, by exact construction (not the historical finder). The search that actually found the shipped circuit cost 54.4 min of one core, inside a ~74 process-hour run |
| **88 @ depth 5, from scratch** — *frontier* | `python3 hunt_88at5.py` | archived: **64 min** of one core from its root. Two re-runs 2026-09-02 reproduced the descent to **89 gates in 558 s** (archived: 3 072 s) but **did not reach 88 in 164 min** — the last gate is one lucky walk chunk. Stochastic; see [The from-scratch 88 @ depth 5](#the-from-scratch-88--depth-5) |
| **88 @ depth 6, from scratch** | `python3 hunt_88at5.py --rng 2163 --target-depth 6` | archived: **37 min** of one core from its root. Not re-measured here — same script, same code, a different root integer |
| **88 @ depth 7**, from our ρ²-symmetric 94 | `python3 hunt_88.py` | **19.4 min** with the shipped stop rule, re-validated 2026-07-27 (a second re-run reached 88 gates at 31.0 min but stopped at depth 8 under an earlier gate-count-only rule); the archived run took 32.9 min. Stochastic — see [The 88 @ depth 7](#the-88--depth-7) |
| **89 @ depth 5** *(superseded by the 88 @ depth 5, kept)*, from this project's 89@6 + 90@5 circuits | `cd ../pipeline && python3 ladder_parallel.py --mode fixed --workers sub89 --stop-gates 89 --stop-depth 5` | **20 s** end to end, re-run 2026-09-02 (the worker verified 89 @ depth 5 inside its first chunk, at t = 17.5 s of the coordinator's first status poll); **19 s and 22 s** on 2026-07-27; the archived run took 592 s (~10 min), with the v1 engine (see below) |
| **92 @ depth 4, from scratch** *(superseded by the 91 @ depth 4, kept)* | `cd ../pipeline && python3 ladder_parallel.py --mode cascade --stop-gates 92 --stop-depth 4` | hours: the archived run reached it at t = 9 610 s (2.67 h). Not re-measured here. **Do not retarget this command at 91** — [why](#the-91--depth-4--no-command-here-and-what-produced-it-instead) |

Each command verifies its own output against MixColumns rebuilt from GF(2⁸)
before reporting it, and every output file is re-checkable by hand — see
[Verify independently](#verify-independently).

## 97 @ depth 3 — the single-file, single-core reproduction

```
python3 reproduce.py
```

Simulated annealing + iterated local search over a shared depth-1-pairs /
depth-2-parts model. **From scratch**: the targets are computed from GF(2⁸),
there is no seed circuit. The result is checked by the independent verifier and
written to `out_97.json`; a summary table prints at the end.

Re-validated **2026-07-27** with the shipped code on one core (`taskset -c 0`):
the annealer reached cost 97 on its first RNG seed after **81.1 s** (23.5 s
annealing, then ILS), and the standalone oracle re-confirmed
`gates=97 depth=3 outputs_built=32/32 VALID`. Earlier runs of the same script
took 60–156 s. If seed 6 misses, the script keeps restarting on further seeds
until it hits the target or its 900 s budget runs out.

Re-run twice more **2026-09-02** on this repository, one core, `nice -n 19`, on a
loaded 20-core box: **57.4 s** and **51.8 s**, both reaching cost 97 on RNG seed
6 — the same first seed — and both re-confirmed by the oracle at
`gates=97 depth=3 outputs_built=32/32 VALID`. This remains the fastest
from-scratch route to the depth-3 point the project has: the depth-3 annealer is
the only method in the whole roster that reaches 97 at depth 3, and the
closed-form constructions that are faster land at 116 gates.

This method is specific to depth 3 and was **not** touched by the v2 engine
rebuild — it does not share a kernel with the pipeline engines.

## The 91 @ depth 4 — no command here, and what produced it instead

This is the one frontier point with **no reproduction command in this
repository**, and the reason is not that the search is expensive. It is that the
code is not here. Two different pieces of code could give it, and neither is
published yet:

**The fastest way to a 91 @ depth 4 is not a search at all — it is two seconds
of construction.** That is worth stating before the history, because it is the
number a reader actually wants. See
[A 91 @ depth 4 in two seconds](#a-91--depth-4-in-two-seconds) below.

### What produced the shipped circuit

**What produced it.** A from-scratch cascade fleet — seven processes, one per
depth rung, on a 20-core box, started 2026-07-31 and stopped by hand. Its
depth-4 lane ran uncapped-restart, depth-capped-4, `alt` mode (120 s walk / 420 s
LNS chunks), and on its fifth restart opened on the from-scratch root
`constructors.build("naive", 40426)` = 144 gates at depth 3. From that root the
descent went 93 @ 4 → 92 @ 4 → **91 @ 4**, verified, and the coordinator promoted
it at **2026-08-01T00:37:38Z**. Cross-pollination was off; every root in that run
is `constructors.build(name, seed)` or the `anneal3` engine — a pure function of
one integer — so the point is from scratch, as
[`../evidence/RESULTS.md`](../evidence/RESULTS.md) §2 states.

**What it cost**, three ways, because only the first is what a re-run would pay:

| | |
|---|---|
| the descent that found it, from its root | **3 263 s = 54.4 min**, one core |
| that depth-4 lane, start to hit | 37 399 s = 10.4 h, one core |
| the whole fleet to the hit | ~10.6 h wall × 7 processes ≈ 74 process-hours |

**Why no command is offered.** The fleet's supervisor and its depth-capped
worker are a separate codebase from `../pipeline/`, and neither is published
here or in the records repository. Packaging a 91 @ 4 re-run means publishing
that worker as a run archive with the same provenance argument the two
from-scratch 88 archives carry — the shape of it is clear and cheap (the
record's restart is rooted at `naive#40426` with chunk seed 40426, so
`hunt_88at5.py`'s pattern applies verbatim once the capped worker exists here),
but it has not been done, and until it is there is no command. It is filed as a
packaging lead in [`../leads.md`](../leads.md).

**What is *not* a substitute, and must not be presented as one.** The pipeline's
own cascade — `ladder_parallel.py --mode cascade --stop-gates 91 --stop-depth 4`
— parses, has a depth-4 rung, and will run. It does not reproduce the 91, for
two independent reasons:

- **It reaches 92, not 91.** That is not an inference — it is what the archived
  run did. `../evidence/cascade_run_2026-07-14_from_scratch_newlogic/` ends
  `d4 depth_cap=4 best=92 gates @ depth 4`, and the 92 it holds arrived by
  reseeding from another rung rather than from its own descent
  (`d4.log`: `ADOPTED reseed 92 gates depth 4`). Later depth-4 work of this
  project, not published here, re-ran that step from this circuit **nine times
  and reached 91 on none of them**.
- **The stop condition can latch shut.** `target_reached` tests one Pareto
  *global* best across all rungs, and that best never regresses. In the same
  archived run it went to `GLOBAL BEST 91 gates depth 5 (d5)` at t = 11 213 s —
  and from that moment `gates ≤ 91 and depth ≤ 4` was unsatisfiable for the rest
  of the run, which continued to t = 23 368 s and was stopped by hand. Under
  `--stop-gates 91 --stop-depth 4` that run would have burnt 6.5 hours and never
  stopped itself, while its depth-4 rung sat on a 92. A rung holding a genuine
  91 @ 4 would fire the stop, since it dominates (91, 5) — but a deeper rung
  reaching 88 at any depth above 4 latches the test shut first.

The `--stop-gates 92 --stop-depth 4` form in the table above is the one that was
measured, and it is kept pointed at 92 for exactly that reason.

### A 91 @ depth 4 in two seconds

**The reproduction command for a record does not have to be the tool that
historically found it.** For this point the fastest honest route is not the
cascade at all: it is an *exact construction* that never searches over circuits.

A separate line of this project's work — a standalone MixColumns **generator**,
built from GF(2⁸), the FIPS-197 matrix and the trace-dual basis, with exact
minimal-SLP solves of theory-generated 8-dimensional sector instances — has a
`ladder` model whose optimum is exactly 91 gates. (That is the optimum **of that
model class**, not a lower bound on MixColumns: nothing here says 90 @ depth 4 is
impossible, and it remains undecided.) Asked for 91 gates with depth as a hard
constraint, it emits one:

```
python3 generate.py --count 91 --regime ladder --depth 4 --cores 1
```

Measured here **2026-09-02**, one core, `nice -n 19`, **from an empty solve
cache**: **2 seconds**, eight exact sector solves of 7 gates each, then

```
  model price   : 91
  EMITTED count : 91   (delta +0)
  depth         : 4  (asked <= 4)
  verify_circuit.py rc=0:
      gates=91 depth=4 outputs_built=32/32 problems=0
      depth<= 4: OK
      VERDICT: VALID MixColumns circuit
```

The emitted circuit was then carried over to **this** repository and re-checked
with the standalone oracle here, which knows nothing about the generator:
`gates=91 depth=4 outputs_built=32/32 problems=0 / VALID`, and `depth<= 3:
VIOLATED` one level down — so the depth-4 claim is tight, by the same test
[ladder row 4](../REPRODUCE.md) applies to the shipped records.

**It is not the record circuit, and that is the point.** It shares 53 of its 91
masks with the cascade6 circuit (Jaccard 0.411) — an **independent witness** of
the same frontier point, constructed rather than found. What it reproduces is
the *claim* 91 @ depth 4, not the artifact.

**Is it from scratch?** By the strict bar — *no record circuit and no
record-derived data as input; targets from GF(2⁸)/FIPS-197 only* — yes, and it
was tested rather than assumed. Two checks were run here on 2026-09-02:

- **What it opens.** Under a Python audit hook logging every `open`, the whole
  run touches exactly two data files in the tree: the ladder model's price
  spectrum, and the generator's currency-menu table. **No record circuit is
  opened at any point.**
- **The menu table is not load-bearing.** That second file is the project's one
  long-standing record dependency — menus read off record circuits. So the run
  was repeated in a copied tree with **every menu in it replaced by garbage**.
  It emitted a **byte-identical** 91-gate depth-4 gate list. The menus are
  loaded unconditionally at import and never consulted on this path; the
  dependency is real in the code and absent from the result.

What *is* inherited is the price spectrum — the result of an exact DP over the
ladder configuration space. That DP is theory-generated, no circuit of any
provenance enters it, and every configuration it names is **re-solved from
scratch** by the generator's own solver before anything is emitted. Only the
*search over configurations* is inherited, not any circuit.

**Two generators, and why the older one is not enough.** The ladder model came
from an earlier standalone generator, which reads **no** menu table at all — the
audit hook shows it opening only its own module cache and the spectrum. But its
`--depth` is not a constraint: it accepts the flag, never constrains on it, and
then honestly reports the miss. Asked for 91 at depth 4 it emits **91 @ depth 5**
and prints `depth<= 4: VIOLATED / VERDICT: INVALID` (measured here, 0.09 s). The
merged tool is the one that turns the cap into a constraint the model must meet —
four places, block by block, with an `InfeasibleAtDepth` exit and a named reason
if it cannot. That is what makes 91 @ **4** come out, and it is also what drags
in the inert menu import. A packaged version wants the second tool's depth
handling and the first one's clean dependency list.

**Why there is still no command in this folder.** The generator is in the
project's unpublished working tree, not here, and vendoring it is a real
decision rather than a copy: it is roughly a dozen modules, and it needs
`numpy` and a SAT solver — which would break this folder's standing
"dependency-free Python 3, stdlib only" contract. That is a repository
architecture call, and the audit findings still open against the tool should be
closed first. What this session established is that the **provenance** blocker
is not there: the F1 menu dependency, which would have disqualified the route,
is measurably inert on it. The packaging job is filed in
[`../leads.md`](../leads.md).

**A note on the 88s — why this route does not extend to them.** The same
generator emits a verified 88 quickly, but **not from scratch**. Its `f4` regime
genuinely consumes the record-read menus, and its one depth-5-capable
configuration reads all three of its structural commitments off the **derived**
88 @ depth 5. The same garbage-menu experiment settles it, measured here
2026-09-02 on one core from a cold cache:

| `f4`, asking for 88 | result |
|---|---|
| with the real record-read menus | **88 gates @ depth 9, VALID, in 30 s** |
| with every menu replaced by garbage | **no circuit in 15 minutes** — killed at the budget |

Read the second row for exactly what it is: a **timeout, not a verdict**. It does
not prove no 88 is reachable without the menus; it shows the menus are doing
real work on that path, 30 s against >900 s. That is the opposite of what the
ladder did — where the same substitution changed nothing at all, byte for byte —
and it is why the ladder counts as from scratch and `f4` does not. (A separate finding of the lane F4 referee points
the same way: one of that configuration's structural constants is numerically
identical to a record's and load-bearing — swap it and the model prices 89, not
88.) The ladder model cannot reach 88 at all; its optimum is exactly 91. So for
an 88 from nothing, the route in this folder — `hunt_88at5.py` — remains the
honest one, and it is a search, not a construction.

## The from-scratch 88 @ depth 5

```
python3 hunt_88at5.py                    # 180 min budget; archived: 64 min
python3 hunt_88at5.py --minutes 360      # longer budget
python3 hunt_88at5.py --rng 2163 --target-depth 6   # the 88 @ depth 6's root
```

**There is no seed circuit.** The root is
`constructors.build("naive", 1958)` — a randomized balanced XOR tree over the 32
raw inputs, a pure function of the integer 1958 — and it re-derives the record
run's own root, **146 gates at depth 3**, exactly as its log recorded it. That
makes this the second of the three frontier points that reproduces from nothing.

Like `hunt_88.py`, this script contains **no search code**. It launches one
process of the *archived worker that produced the record* —
`../evidence/campaign87_run_2026-07-28_got_88at6_fromscratch/code/hunt_worker.py`,
hash-pinned by the record's own archive and published two days *before* the find
— polls its status file, and stops it as soon as an oracle-verified best reaches
88 gates at depth ≤ 5. Both bounds matter, for the same reason as in the 88 @ 7:
the walk reaches the 88 masks at depth 6 first and the Pareto tie-break carries
the same size to depth 5 seconds later. No knob is restated in this folder: the
LNS and walk knobs, the `alt` chunk cycle and the uncapped depth all come from
the archived file. Its one external import is `WorkerCtx`/`pareto_better` from
`../pipeline/worker.py`, which the script puts on the path.

That the launched code *is* the producing code is checkable in one command, and
was re-checked on **2026-09-02**: all five files match the sha256 pins the record's
own archive published for them.

```
cd ../evidence/campaign87_run_2026-07-28_got_88at6_fromscratch/code
sha256sum engines.py hunt_worker.py constructors.py mixcolumns_core.py verify_circuit.py
# compare with ../../campaign87_run_2026-07-30_got_88at5_fromscratch/code/CODE_PROVENANCE.md
```

**Why `--rng 1958` is the honest default, and what it does and does not buy.**
The record's restart is **session 5, restart 16** of a five-session worker,
opened on `naive#1958` with RNG seed 1958. The engines take that *integer*, not
the worker's RNG object, and it advances by +1 per chunk — so a fresh worker
started with `--seed 1958` begins in exactly restart 16's state, and the root and
the first chunk are reproduced. Chunk boundaries are **wall-clock**, though
(120 s walk / 420 s LNS), so from the second chunk on a machine of a different
speed sits at a different iteration and the trajectories part — the same caveat
as `hunt_88.py`, and it is why a re-run is a re-run and not a replay.

**The root is held, and that is this script's own choice.** The archived worker
rotates roots — it abandons one after 90 minutes (`--restart-s` 5400 s) or after
40 minutes with no local improvement (`--stall-s` 2400 s) — which is right for
one worker of sixteen mining many roots for days, and wrong for a script whose
whole job is to re-run *one* restart. Both timers are therefore pushed past the
budget, so the record's root is kept for the entire run; `--rotate-roots` gives
the archived behaviour back. This was not a precaution: the first re-run here hit
exactly that rule and lost the root. See the run record below.

This is therefore **a re-run of the winning restart, not a blind search**, and
the distinction is the whole cost story:

| | |
|---|---|
| from *this* root (the record's), archived | 88 @ depth 6 at **64.1 min**, 88 @ depth 5 **6.1 s later** |
| from an arbitrary fresh root (`--rng` anything else) | a lottery, and an expensive one. The fleet's own accounting, which is not published here, prices this constructor at **~8.6 CPU-hours per 88** and finds ~3.5 % of from-scratch descents reach 88 at all. That landing at *depth 5* is a further sub-event **is** checkable here: the shipped `c_naive.log` records three independent arrivals at 88 gates over that worker's five sessions (depths 8/7/6, then 10/9/8, then 6/**5**), and exactly one of the three reached depth 5 |

**What re-runs did here, and the packaging bug they caught.** Two re-runs on
**2026-09-02**, one core each, `nice -n 19`, on a loaded 20-core box. Both
re-derived the root at 146 gates / depth 3, and both ran the same descent — the
early chunks are deterministic given the seed, so their timings agree to within a
few seconds — and both were **far ahead of the archived run**:

| | run 1 | run 2 (root held) | archived, same root |
|---|---|---|---|
| 93 @ 5 | 23 s | 22 s | — |
| 91 @ 5 | 46 s | 46 s | 385 s |
| 90 @ 5 | 70 s | 74 s | 1 185 s |
| 89 @ 5 | 559 s | 558 s | 3 072 s |
| **88 @ 6 → 88 @ 5** | root lost at 54 min | **not in 164 min** | 3 843 s / 3 849 s |

Run 1 then sat at 89 and the archived worker's own **stall rule fired at
t = 3 240 s (54 min)** — `stalled 2400s at 89 gates -- new root` — dropping the
record's root **ten minutes before the time the archived descent had needed to
reach 88 from it**.

That is a bug in this script, not in the record: the archived worker rotates
roots because it was one of sixteen mining many roots for days, and a re-run of
*one restart* must not inherit that. Being fast makes it worse, not better — the
walk banks its improvements early, so the 2 400 s no-improvement clock starts
sooner. The archived run survived its own rule only by being slower, spreading
the same improvements over 3 072 s instead of 559 s.

`hunt_88at5.py` therefore now **holds the root for the whole budget**, pushing
both rotation timers past the deadline; `--rotate-roots` restores the archived
behaviour.

**The re-run under the fix, in full.** Launched 10:20:14, one core, `nice -n 19`,
`--minutes 165`. The fix worked — the log opens `restart=10500s stall=10500s`,
and there is **no** `new root` or `stalled` line anywhere in its 259 chunks
(121 walk, 68 LNS): the record's root was held for the entire run. It reached
**89 @ depth 5 at t = 558 s** and then **stayed at 89 for the remaining 154
minutes**, ending at t = 9 837 s (164 min) without an 88.

So the honest result for this row is: **the descent reproduces, the last gate did
not.** Down to 89 gates this re-run was 3–5× faster than the archived one; the
step from 89 to 88 is a single lucky walk chunk, and in 164 minutes on this
machine it did not come, against the archived run's 64 minutes from the same
root. That is not a failure of the packaging — the root, the seed, the code and
the first chunk are all reproduced — it is the stochasticity this page keeps
warning about, and it is why the script ships a 180-minute default and why
nothing here promises a time. A second attempt is a different RNG draw of the
same walk; the archived arrival is one sample, and so is this miss.

**Provenance.** The root reads nothing off disk — the `constructor:` branch of
the worker's root selector has no file-reading path at all. Cross-pollination was
unreachable in the producing fleet and repulsion was off, and the engine that
produced both 88-gate states, `engine_walk`, has no candidate pool and no disk
read path. Nothing this worker produces is derived from published work. The
five-part argument, with the log lines and the hash pins, is in
`../evidence/campaign87_run_2026-07-30_got_88at5_fromscratch/PROVENANCE.md`.

**On the fleet generators.** A separate line of this project's work can emit a
verified 88 @ depth 5 from a block model in ~46 min of one core. It is **not**
offered here and should not be mistaken for this: its cell and all three of its
structural commitments are read off the *derived* 88 @ depth 5 — the circuit
whose seed chain runs through published work — and the circuit it emits is that
one, mask for mask. It is a re-derivation, not a discovery, it needs a SAT solver
and a census file this repository does not carry, and packaging it would publish
a recipe for re-emitting derived work. That is the same line this folder already
declines to cross for the 88 @ 8.

## 89 @ depth 5 — seconds, not minutes, with the v2 engine

```
cd ../pipeline
python3 ladder_parallel.py --mode fixed --workers sub89 --stop-gates 89 --stop-depth 5
```

The historic two-worker sub-89 configuration: an uncapped `lns` worker on this
project's 89 @ depth 6 circuit and a depth-5-capped one on its 90 @ depth 5,
reseeding each other, stopping themselves at the target.

The **archived run** (2026-07-14) surfaced the 89 @ depth 5 at t = 592 s (~10 min).
That run used the v1 engine; the shipped engine is the campaign's rebuilt one,
and it is much faster on this seed. Re-validated **2026-07-27**, twice:

- the uncapped worker verified **89 gates @ depth 5 at t = 0.3 s of its first
  chunk** (LNS iteration 18, via the Pareto depth tie-break), both times;
- the command as a whole took **19 s** and **22 s** end to end — that time is
  the coordinator's 20 s status-poll cadence plus process start/stop, not
  search time.

Re-run again **2026-09-02**, as shipped, `nice -n 19`: **20 s** end to end. The
89 @ depth 5 was already standing at the coordinator's first status poll
(t = 17.5 s), which fired `STOP TARGET reached: 89 gates @ depth 5` and shut both
workers down two seconds later. The other worker, capped at depth 5 on the 90 @ 5
seed, was still at 90 when it was stopped, as before.

## The 88 @ depth 7

```
python3 hunt_88.py                     # 45 min budget, the record worker's RNG
python3 hunt_88.py --minutes 120       # longer budget
python3 hunt_88.py --target 87 --target-depth 0   # don't stop at 88
```

`hunt_88.py` contains no search code: the 88 came out of the pipeline, so this
script only *aims* it. It writes the shipped configuration into a run folder,
launches **one** `../pipeline/worker.py` process (`alt` mode, uncapped, RNG 1010)
on the exact seed the record worker used, polls its status file, and stops it as
soon as an oracle-verified best reaches **88 gates at depth ≤ 7**. Both bounds
matter: the walk finds the 88 masks at some large depth first and the Pareto
tie-break carries that same size down to depth 7 a second or two later, so
stopping on the gate count alone yields an 88 at depth 8–11. The knobs are
imported from `../pipeline/ladder_parallel.py` rather than copied, so they cannot
drift from the shipped ones. The run folder is deleted at the end unless you pass
`--keep`; the best circuit is copied out to `out_88hunt.json`.

**What the archive says.** The 88 @ depth 7 was found by worker `w10_sym94` of a
10-worker, 8 400 s hunt on 2026-07-26 — `alt` mode, RNG 1010, seeded with the
exactly ρ²-symmetric **94 @ depth 5** of our own lineage — at **t = 1 973 s
(32.9 min)**, at depth 11, which the Pareto tie-break took to depth 7 5.3 s
later. Full log, code and provenance:
`../evidence/campaign87_run_2026-07-26_got_88at7/`.

**What a single-worker re-run did here.** Two re-runs on **2026-07-27**, one
worker each, on the defaults above:

| run | 88 gates first verified | at depth ≤ 7 | oracle |
|---|---|---|---|
| 1 (an earlier stop rule: gate count only) | t = 1 858.5 s (31.0 min), at depth 11 → depth 8 within 1.2 s | stopped before the tie-break got there | 88 @ 8, 32/32, VALID |
| 2 (the shipped stop rule, 88 @ depth ≤ 7) | t = 1 161.6 s (19.4 min), at depth 8 | **t = 1 162.6 s (19.4 min)** | **88 @ 7, 32/32, VALID** |

Archived, for comparison: 1 973 s (32.9 min). Run 2's circuit is **not** a copy
of the record — it shares 83 of its 88 masks with it (Jaccard 0.892): the same
plateau basin, a different point in it.

The **first chunk is reproduced exactly**, because the seed circuit and the RNG
seed are the archived worker's: 92 at `it=27`, 91 at `it=32`, 90 @ 9/8/6/5 at
`it=603/622/670/723`, 89 @ 8 at `it=58504`, 89 @ 7 at `it=58795` — the archived
worker's iteration numbers to the digit, reached in 82 s here against its 202 s
(one worker on an idle box walks at ~750 it/s; that one, one of ten on a loaded
box, ran at ~290 it/s). Chunk boundaries are **wall-clock**, though, so from the
second chunk on a faster machine is at a different iteration and the
trajectories part — which is why the two re-runs above diverged (31.0 min to
88 gates under the old stop rule vs 19.4 min to 88 @ depth 7 under the
shipped one).

This is a re-run, not an independent confirmation and not a promise: change the
RNG, the seed, the chunk lengths or the machine and it is an open-ended
stochastic search again. What it establishes is that the shipped engine, seed and
knobs are the ones that produced the record.

**Provenance.** The ρ²-symmetric 94 seed is our own lineage (from-scratch 97 @ 3
→ 89 @ 6 → 89 @ 5 → symmetrized 94), so nothing this worker produces is derived
from published work; cross-pollination stays off, as in the shipped
configuration. Our 88 @ depth 7 **matches** the published 88-gate record
(Jean, ePrint 2026/1481) **with an independent circuit** — 61 of 88 masks in
common — it does not beat it.

## The three circuits with no command here, and why

- The **88 @ depth 8** (a third distinct family) and the **derived 88 @ depth 5**
  both have seed chains that pass through Jean's published
  circuit, so both are reported as derived work and neither is offered as a
  recipe. Their run archives are
  `../evidence/campaign87_run_2026-07-27_got_88at8_thirdfamily/` and
  `../evidence/campaign87_run_2026-07-29_got_88at5_derived/`, each with the exact
  code, the seed and the untouched logs; the 88 @ 8's seed also ships as
  `../pipeline/seeds/seed_88_at_depth8_thirdfamily.json`. This is a choice, not a
  gap: both *could* be re-run from their archives, and are not offered because
  publishing a recipe for derived work is not something this folder does.
- The **91 @ depth 4** is a genuine gap — the code that produced it is not in
  this repository. Its cost, its lineage and what must not be substituted for it
  are [above](#the-91--depth-4--no-command-here-and-what-produced-it-instead).

**What changed on 2026-09-02.** This section used to name four circuits. The two
from-scratch 88s — the **88 @ depth 6** and the **from-scratch 88 @ depth 5** —
were listed here because each came out of one restart of one worker of a
multi-day 16-process fleet (restart 18, 18.96 h in; and session 5 restart 16,
19.22 h in), and no single command reproduced *the fleet*. That was the wrong
thing to ask for. Re-running the **step** is what a reader wants, the archives
already hold everything it needs — the roots
`constructors.build("naive", 2163)` and `constructors.build("naive", 1958)`
re-derive the logged 139-gate and 146-gate depth-3 roots exactly, and the
producing worker is archived beside them — and the engines turned out to be
seeded by the restart's own logged integer, so the step is startable directly.
`hunt_88at5.py` does exactly that, and both are now in the table above. The
from-scratch 88 @ depth 5 is the frontier's depth-5 point; it is **not** a
gate-count record, since 88 is Jean's published count and Jean has priority.

To continue the hunt for 87 from the three 88-gate family anchors the pipeline
ships, use its shipped set: `python3 ladder_parallel.py --mode fixed` (i.e.
`--workers hunt87`), minding the provenance note in `../pipeline/README.md`. The
two from-scratch families' anchors are
`../evidence/circuits/mixcolumns_88gates_depth6.json` and
`../evidence/circuits/mixcolumns_88gates_depth5_fromscratch.json`.

## Legacy demonstrations (opt-in)

Three further methods demonstrate the individual moves on this project's
*superseded* records. Name them on the command line (or add them to `RUN` at
the top of `reproduce.py`):

```
python3 reproduce.py 91          # or: python3 reproduce.py 91 90 89
```

Honest provenance and re-validated times, per method (**2026-07-27**, one core):

| method | seed provenance | what it shows | measured |
|---|---|---|---|
| `"91"` | the **published** 92-gate SLP of Xiang, Zeng, Lin, Bao and Zhang, embedded in `seeds.py` as data | plateau walk over equal-size circuits until one gate becomes removable → 91 @ depth 6 | **6.7 s** (reduced on the first search seed); 5–60 s across runs |
| `"89"` | a 90-gate depth-6 circuit of **our own** earlier lineage (`SEED_90_MASKS`) | the value-set walk (remove-1 + remove-2-add-1 hub moves) cutting 90 → 89 at unconstrained depth | **150 s** — hit 89 (at depth 10) inside its first 150 s RNG seed |
| `"90"` | a 91-gate depth-6 circuit of **our own** earlier lineage (`SEED_91_TRIPLES`) | proves the seed admits no single local cut (duplicate scan, peel, all-pairs remove-2-add-1); with `C90["lns_seconds"] > 0` also runs the pure-Python LNS (reaches ~91) | **0.2 s** for the irreducibility proof |

These reproduce **superseded** results, kept because each is a clean, readable
statement of one move: the current records are in the table at the top and in
`../evidence/RESULTS.md`.
From nothing, method `"89"`'s walk floors near 92 — the 89 needs its seed.

## Which engine is which

`reproduce.py` deliberately carries the **original per-method search code** of
the runs it reproduces, frozen. It is what those results were obtained with, and
each method reads as one move rather than as a tuned kernel. It is *not* the
current engine.

The current engine is `../pipeline/engines.py`, rebuilt in the 2026-07 campaign.
That rebuild is why the 89 @ depth 5 now comes back in seconds and why any of
the five 88s exist at all; `hunt_88.py` here aims it, and `../METHODS.md` §5–§6 documents
each change with its measured effect.

`hunt_88at5.py` aims a **third** copy: the `engines.py` archived with the
from-scratch 88s, which is `../pipeline/engines.py` plus three additions
(harvester reuse across chunks, a harvest size cap, and knob-gated family
repulsion — which was off in the producing run). `run_engine` is unchanged and
none of the three touches the moves, the acceptance rule or the kernel; the
comparison is in that archive's `CODE_PROVENANCE.md`. It is aimed rather than
copied for the same reason as the others: the code that produced a record is the
code a re-run should use.

`mixcolumns_core.py` in this folder is a **byte-identical copy** of
`../pipeline/mixcolumns_core.py` — both halves of the repository verify against
exactly the same oracle, and `diff` proves it:

```
diff ../pipeline/mixcolumns_core.py mixcolumns_core.py && echo identical
```

## Files

| file | what it is | edit it? |
|---|---|---|
| `reproduce.py` | the runnable script: **CONFIG block at the very top** (every knob), then the methods, then the runner | yes — all tuning lives at the top |
| `hunt_88.py` | aims one pipeline worker at the ρ²-symmetric 94 seed and stops it at the target; CONFIG block at the top, overridable with `--minutes/--target/--rng` | yes — same |
| `hunt_88at5.py` | aims one *archived* worker at the from-scratch root `naive#1958` — **no seed circuit** — and stops it at 88 gates @ depth ≤ 5; CONFIG block at the top, overridable with `--minutes/--target/--target-depth/--rng` | yes — same |
| `mixcolumns_core.py` | the MixColumns spec rebuilt from GF(2⁸) + the verifier (byte-identical to the pipeline's copy) | no — this is the trustworthy math |
| `seeds.py` | the embedded seed circuits (data) | no — starting points, not answers |

## Verify independently

Every `out_*.json` is an index-pair circuit (`{"gates":[[a,b],...]}`, signals
0..31 = inputs, gate k → signal 32+k). Re-check any of them with the standalone
verifier one folder up:

```
python3 ../verify_circuit.py out_97.json 3
python3 ../verify_circuit.py out_91.json 6
python3 ../verify_circuit.py out_88hunt.json      # depth bound optional
python3 ../verify_circuit.py out_88at5.json 5
```

## Published circuits, for comparison

Nothing in this folder is claimed optimal, and no published circuit is counted
as a result of this project. The points the records above are measured against:
99 @ depth 3 (Shi–Feng–Xu, ToSC 2023); 97 @ depth 4 and 94 @ depth 5
(Osvik–Canright, ePrint 2024/1076); 92 @ depth 6 (Maximov); 92 gates
(Xiang–Zeng–Lin–Bao–Zhang — the seed of method `"91"`); **88 gates (Jean,
ePrint 2026/1481)**, measured at depth 7 here — the paper states no depth;
and **89 gates at unstated depth (Sun–Yang–Li, ePrint 2025/1493)**, measured
at depth 9 here. Neither of the last two dominates our
88 @ depth 5, so **97 @ 3, 91 @ 4 and 88 @ 5** — this project's current frontier
— all stand against the published points. (The 92 @ 4 and 89 @ 5 in the table
above were frontier points when they were made and are superseded by this
project's own later circuits, not by anyone else's.)
Both imported circuits are transcribed, oracle-verified and credited
under `../evidence/campaign87_imported_prior_art/`; the full record table and
lineage are in `../evidence/RESULTS.md`.
