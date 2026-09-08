# Depth is a property of the value set

**The negative:** you cannot make an existing 88 shallower by rescheduling it.
There is no rewiring, no Tellegen transposition, no topological-order trick that
takes a known 88 down to depth 5. If you want a shallower circuit you have to
change *which values it computes*, and that is a search, not a rewrite.

This matters because it closes an attractive-looking shortcut: *"get any 88
cheaply from scratch, then convert it to depth 5."* Step two does not exist.

---

## 1. The wiring of an 88 is forced by its value set

Measured in the project's working tree (`wrapup/day2/STEWARD.md`), by sampling
random topological realisations of known 88s and counting, at each gate, how
many legal parent pairs were available:

| measurement | result |
|---|---|
| 30 random wirings × 3 circuits, per-gate legal parent pairs | **1 320 / 1 320 observations had exactly one** |
| masks whose as-found parent was never sampled | **0** |
| census, 25 circuits, 2 200 gate masks | 2 197 with exactly 1, 2 with 2, 1 with 3 — **forced fraction 0.9986** |

Ignoring acyclicity there *is* apparent freedom (pairs `{a,b}` with `a^b = m`
anywhere in the signal set run 1–6 per mask). Acyclicity removes essentially all
of it. **At 88 gates the DAG is not a free parameter.**

So depth is a function of the value set. The question "can I reschedule this
circuit shallower?" has a computable answer, and it is the same answer for every
circuit on that value set.

## 2. Every shipped circuit is already at its minimum possible depth

The **ASAP least-fixpoint schedule** over a value set is the shallowest schedule
any circuit on that value set admits. Computed here for all nine shipped
circuits, against the depth the standalone verifier measures:

| circuit | gates | measured depth | ASAP depth | reschedulable? |
|---|---:|---:|---:|---|
| `mixcolumns_88gates_depth5.json` | 88 | 5 | **5** | no |
| `mixcolumns_88gates_depth5_fromscratch.json` | 88 | 5 | **5** | no |
| `mixcolumns_88gates_depth6.json` | 88 | 6 | **6** | no |
| `mixcolumns_88gates_depth7.json` | 88 | 7 | **7** | no |
| `mixcolumns_88gates_depth8_thirdfamily.json` | 88 | 8 | **8** | no |
| `mixcolumns_89gates_depth5.json` | 89 | 5 | **5** | no |
| `mixcolumns_91gates_depth4.json` | 91 | 4 | **4** | no |
| `mixcolumns_92gates_depth4.json` | 92 | 4 | **4** | no |
| `mixcolumns_97gates_depth3.json` | 97 | 3 | **3** | no |

**Measured depth equals ASAP depth in all nine cases.** The 88 @ 6 cannot be
rewired to depth 5; neither can the 88 @ 7 or the 88 @ 8.

### Reproduce

Run from the repository root:

```
python3 corpus/depth_forced/asap_depth.py
```

Standard library only, about a second, exit 0 if and only if every circuit is
already minimal. It prints, per circuit, the measured depth, the ASAP depth, the
level histogram and the output rows pinned at the deepest level — those rows are
*why* the depth cannot come down without changing the value set. The mechanism
is in [`HOW.md`](HOW.md).

## 3. Size-preserving moves that DO change the value set still do not get there

Two independent measurements, 2026-09-02, one core, `nice -n 19`.

**(a) Double transposition (Tellegen round-trip).** The DAG over an 88-gate
value set is unique, but its topological orders are not and the transpose is
order-sensitive, so `M → Mᵀ → M` is a cost-preserving map that need not be the
identity. 400 round-trips from each of the three non-depth-5 88s:

| seed | distinct 88s reached | ASAP depths of everything reached | max symmetric difference |
|---|---:|---|---:|
| 88 @ 6 | 354 | `{6: 196, 7: 157}` | 16 masks |
| 88 @ 7 | 145 | `{7: 50, 8: 94}` | 10 masks |
| 88 @ 8 | 228 | `{8: 8, 9: 101, 10: 118}` | 12 masks |

**Across 727 distinct 88s, transposition never once produced a circuit shallower
than its seed.** It preserves depth or deepens it. (Consistent with the
transposition principle: `gates(Mᵀ) = gates(M)` identically, so transposition is
cost-preserving by identity, and it was depth-non-improving in practice here
too.)

**(b) Exhaustive plateau enumeration from the 88 @ 6.** Remove-1 plus every
valid single-mask repair, keeping every neighbour whose ASAP depth is ≤ 6, run
to closure (251 s):

```
expanded=5427  seen=5427  frontier=0  exhausted=True
depth tally over the whole component: [(6, 5427)]
states at depth 5: 0
```

The 88 @ 6's **entire** depth-≤6 equal-size plateau component is 5 427 circuits,
every one of them at depth 6. This is a complete enumeration of that component,
not a sampling miss.

## 4. Why — and why the records' own route is not a counterexample

- **92 of 28 796** corpus 88s carrying a build order are at depth 5: **0.32 %**.
- The depth-5 88s live in **small closed pockets**. The depth-≤5 component
  around the derived 88 @ 5 is **27 states, exhausted**; around the from-scratch
  88 @ 5 it is **135 states, exhausted**. The two are far apart (Jaccard 0.313)
  — separate pockets, not one.
- A depth-non-increasing size-88 move therefore cannot *enter* a depth-5 pocket
  starting from a depth-6-or-deeper 88. The only ways in are to go up in depth
  or to change gate count — that is, to run the search.

Both depth-5 records were made that way, and neither is a conversion. In each
case a walk reached 88 gates *already inside* a depth-5 pocket, and the Pareto
depth tie-break then walked at fixed size to depth 5 within seconds:

| circuit | 88 gates first appear | tie-break reaches | elapsed |
|---|---|---|---:|
| 88 @ 7 | depth 11, it = 45 614 | 7, it = 47 436 | 5.3 s |
| 88 @ 8 | depth 10, it = 99 444 | 8, it = 100 049 | 1.2 s |
| 88 @ 6 (from scratch) | depth 7, it = 37 270 | 6, it = 37 501 | 0.5 s |
| 88 @ 5 (derived) | depth 6, it = 38 447 | **5**, it = 40 419 | 4.2 s |
| 88 @ 5 (from scratch) | depth 6, it = 33 873 | **5**, it = 37 155 | 6.1 s |

The tie-break costs no extra search and runs automatically, but **where it stops
is set by the region of the search space the walk is already in**, not by any
transformation applied afterwards. Two of the five reached depth 5. It is not a
conversion step and cannot be aimed at a chosen depth.

---

## What this does not show

It says nothing about whether **more** depth-5 pockets exist to be found
directly — almost certainly they do; 92 are already indexed and only two have
been enumerated to closure. It does not bound the number of depth-5 88s, and it
does not say a depth-4 88 is impossible. What it rules out is exactly one thing:
taking an 88 you already have and rescheduling, transposing or
depth-preservingly walking it to a lower depth.

**Working-tree sources.** `wrapup/day2/STEWARD.md` (the wiring-null measurement),
`wrapup/day2/conversion_check.md` (the full check this doc is drawn from),
`wrapup/CORPUS88.md` (the corpus depth histogram),
`beat88/analysis/scratch/value-set-representation/transpose_walk.py` and
`beat88/analysis/scratch/pareto-depth-tiebreak/bfs_capped.py` (the two searches
in §3). Paths name files in the project's working tree, which is larger than
this repository; see `INVENTORY.md`.
