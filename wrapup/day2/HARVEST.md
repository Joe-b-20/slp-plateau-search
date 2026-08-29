# HARVEST — results that landed after their write-up, collected 2026-08-29

Day-2 task T1c. **Read-mostly**: the only files written are the eleven
`ADDENDUM_20260829.md` files listed below and this summary. No existing file
was modified, no `atlas/` or `thinktank` file was touched, and no live
directory was written to (the k = 14 solvers in `fleet11/laneCUBE` were read
only). Every figure below is re-derived from an **append-only ledger, log or
cube bank**, never from a derived tally, `RESULT.md` or `TALLY.txt`.

## Addenda written

| # | file | the one-line correction it carries |
|---|---|---|
| 1 | `fleet9/laneENUM/ADDENDUM_20260829.md` | The U3 queue drained: **all 14 U3 cells** now bank ≥ 1 optimal set (13 at 1, `p88_05` at 7) — still all `timeout`, so U3 stays UNDECIDED, the §4 floors are numerically unchanged but are now floors on the *full* product; **84.4 core-hours of SAT enumeration landed after the write-up** (U3 alone cost 84.2 core-h against a published estimate of 8,400 s), and **no new distinct 88s** were produced. |
| 2 | `fleet12/laneF1/ADDENDUM_20260829.md` | The 13 late rows (6 priced, 7 `exit 5 UNDECIDED`) **measure the plateau's upper cliff instead of arguing it: `\|M\| = 23` is the last currency-shape count that prices at 88**; the 24th shape buys back **zero** block gates (65 → 65) so the total goes 88 → 89, and a 25-shape record-derived menu reaches `blocks = 64` at 89. Nothing ≤ 87 in 64 rows. |
| 3 | `fleet1/laneB_regionbounds/ADDENDUM_20260829.md` | `R01_qk4_s2` **k = 14 UNSAT, 1008/1008 cubes, 484.6 ks CPU** ⇒ `m_qk4 ≥ 15` ⇒ **the quotient route independently certifies `R01 ≥ 15`**; `R34_qk1_8_9` moves to bracket [15,18]; k = 15 is launched and abandoned **1 cube of 1008** in. |
| 4 | `fleet1/laneD_completions/ADDENDUM_20260829.md` | Both basin sweeps completed 27,720 triples each: **99 lateral escapes (42 + 57), not 1** — `88@5fs` is not rigid, `88@5`'s basin is the anomalous one. All 99 are in `corpus88` and distinct; **94 exist nowhere else in the 1.58 M-row corpus**, and only the 5 with a build order have had the B = 56 tripwire fired on them (all B = 56). |
| 5 | `fleet3/laneF4_rule/ADDENDUM_20260829.md` | `W3_noshare = 11` exact (verified, 33,876.6 s) makes `(rank 1, no sharing) = 12`, so **the rank cut buys ZERO and the `D37 → W3` sharing edge buys all 3 gates** — §3.2's "both ingredients are needed" is false, exactly as the lane's own referee said. No bound moves. |
| 6 | `fleet2/laneG_generator/ADDENDUM_20260829.md` | `U3(tier1) = 10` exact (k = 9 exhaustively UNSAT), so `(U27,U3) = 2 + 10 = 12` — **identical to `4 + 8 = 12`**; §4.4(b)'s "moves from 12 towards 11" **moves nowhere**, R34 stays at 25, and the hoped-for evidence against the greedy criterion does not exist. |
| 7 | `fleet8/unified/ADDENDUM_20260829.md` | (a) The **20 banked timeout brackets tabulated** (25 rows → 20 distinct instances, 32.4 core-hours) — headline: *off-record menus cost real gates* (`U07 ≥ 14` vs 12, `S2W ≥ 11` vs 7 at the record menu). (b) The joint job logged `DONE` with **no k = 14 row** and no verdict file: **`merged(W3 ∪ U4) ∈ {14, 15}`** — k = 9…13 exhaustively UNSAT for the lower end, replay `W3 + U4 = 8 + 7 = 15` for the upper. |
| 8 | `experiments/e5_readd/ADDENDUM_20260829.md` | The second-family screen completed: **`88fs5` 35,960 / 35,960 four-target drop sets, all refuted at `k = W−1`, zero timeouts** — so the project holds **two** complete drop-4 certificates on two structurally different families, answering the family-independence question E5 left open. |
| 9 | `experiments/e6_cancelplan/ADDENDUM_20260829.md` | **The extraction is impossible and this is the proof:** `cpk.oracle()` writes the circuit to `tempfile.mkstemp` and the caller never persists it, so E6's flagship 88 exists only as an oracle *verdict string* in one ledger row. Nothing was written to `wrapup/day2/harvest/`. The claim must not be cited as an on-disk verified circuit. |
| 10 | `experiments/e7_push/ADDENDUM_20260829.md` | **Four** decided dim-12 regions, not one — all `min_gates = 11`, `DECIDED_no_saving`, **including one on Jean's foreign-lineage 88** (the independent-lineage test, obtained free and never claimed). Plus the never-pasted atlas correction reproduced in full: three `b9b_0.log` `ctl=OK` negatives are **vacuous**, and the convex-closure repair **closes sector 0 at 14/14**. |
| 11 | `fleet6/door/ADDENDUM_20260829.md` | **`MB27B373` = 13 exactly** (k = 12 UNSAT in 19,458 s + replay bound 13) — the boundary is FREE, `laneMERGE` closes 20-for-20, and the branch in which 12 would have priced the class at **87** is foreclosed. `laneMERGE` still records `[12,13] UNDECIDED` in two places. |

Eleven addenda covering the seven briefed harvest items: item 3 spans four lanes
(3, 4, 5, 6), items 4 and 5 both land in `fleet8/unified` (7), and item 6 spans
three experiments (8, 9, 10).

## The three corrections that matter most

1. **`fleet6/door`: `MB27B373` = 13.** The only one of these that closes an
   87 branch. It has sat in a 170-byte log since 2026-08-24 while
   `fleet5/laneMERGE/RESULT.md` and its `FINAL_TALLY.txt` still say
   `[12,13] UNDECIDED`. One row of one table.
2. **The rank cut buys nothing, twice.** `W3_noshare = 11` (lane F4) and
   `U3(tier1) = 10` (lane G) are independent solves on different cells that
   both return **zero** for the rank/basis reduction, putting the whole 3-gate
   gap in the `D37 → W3` sharing edge. Two `RESULT.md` files currently claim the
   opposite; the merged statement is stronger than either.
3. **`merged(W3 ∪ U4) ∈ {14, 15}` with `DONE` meaning "timed out".**
   `fleet8/unified` reads `JOINT DONE` with no verdict file, and the only record
   of its 105,083 s k = 13 UNSAT is one 381-byte file. The two-gate saving is
   dead; the one-gate question is live in `fleet11/laneCUBE` at 87/528 cubes.

## Things a re-tallier should not get wrong

* **`fleet9/laneENUM` U07:** three cells were run twice and the *later* row
  banks a **lower** count than the earlier `killed_for_queue_reorder` row
  (20→16, 28→16, 19→13). Both are floors — take the **max**, not the last.
* **`e5_readd` 88d5:** the `drop4` stream holds 35,959 distinct subsets, not
  35,960. The missing one, `[3,11,19,27]`, is the unique `W = 10` set, excluded
  by the screen's `wmax = 9` cap and decided instead in the **`cube`** stream
  (121 rows, label `88d5_orb3_sub`). There is no hole; a naive re-tally invents
  one.
* **`fleet8/unified` timeouts:** 25 rows collapse to **20** distinct instances —
  different lean menus generate byte-identical block subproblems
  (`s4_ifc2a`/`s4_ifc6e`/`s4_ifcc`, `s7_c7`/`s7_c6`, `s4_if`/`s4_ifc6`).
  Counting rows overstates coverage by 25 %.
* **`fleet9/laneENUM` row counts:** the ledger holds 270 rows; the RESULT's
  erratum counts 198, but **228** rows existed at the RESULT's 16:20 mtime.
  "+72" is against the RESULT's own number, "+42" is against the clock.

## What was not harvestable

`wrapup/day2/harvest/` was **not created**: the one artifact it was to hold —
E6's ledger-only 88 — does not exist on disk and cannot be reconstructed from
banked data (see addendum 9). Regenerating it is a ~3,762 s CP-SAT run and was
out of scope for a read-mostly pass.
