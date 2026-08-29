# PORT_NOTES.md — what must be RE-DERIVED for AES InvMixColumns

Companion to `wrapup/METHOD_CATALOG.md` §(a) *Phase-2 starter kit* and
`wrapup/reports/fleet5_8.md` §`unified-generator` → **Generality**.

This file is about the *generator chain* (`fleet8/unified/`), the one keeper in
the catalog whose port cost is **not** "swap a constant". Everything asserted
here that carries a number was computed today by
`wrapup/phase2/spec/sector_probe.py`; the transcript is
`wrapup/phase2/controls/S1_sector_probe.txt`.

Nothing in this file was executed against the generator. It specifies the
re-derivation; it does not perform it.

---

## 0. What is already done (this kit)

| deliverable | file | status |
|---|---|---|
| InvMixColumns spec, from FIPS-197 + GF(2⁸) | `spec/derive_invmc.py` → `spec/invmc_matrix.json`, `spec/invmc_target_masks.json` | derived, 4 controls pass |
| forward control + GF(2) inverse + M³ identity | `controls/C1-C4_spec_derivation.txt` | all PASS |
| oracle, arbitrary target | `tools/verify_slp_generic.py` | 5 controls pass (`controls/O1-O5_oracle.txt`) |
| B = n − q tripwire, arbitrary target | `tools/tripwire_B.py` | calibrated; all five published 88s read B = 56 (`controls/B1_tripwire.txt`) |
| day-0 baselines | `tools/baseline_naive.py` | `controls/N1_baselines.txt`, `N2_baseline_oracled.txt`, `N3_composition_bound.txt` |

---

## 1. The three tiers of port cost (from fleet5_8.md, verified against the code)

**CIRCUIT-GENERIC — no change at all.** The entire exact-SLP layer:
`dslp.py` (gate-position CNF, one-hot pair selection, N1/N2/N3 symmetry
breaking, L1 cone bound, level variables, `reach_levels`), `solver.py`,
`assemble.py` (`min_depth_schedule`, `strip_dead_gates`, `verify_inprocess`),
`engine.py`, `ledger.py`, `regress.py`, `reach.py`, `render.py`, `capoff.py`,
`live.py`. These read a target list and nothing else.

**FIELD-ONLY — unchanged, because the inverse lives in the same field.**
`theory.py:30 AES = 0x11B` and everything derived from it alone:
`build_duals()` → `DUALS`, `xtime_dual_coords()` → `QLINES`, and hence
`TAPS = [1,3,4]`, `CLEAN = [0,2,5,6,7]`, `PARENT`. Confirmed today: the probe
imports `theory.py` untouched and these constants are the same objects for the
inverse. Laws **L0** (taps), **L2** (planes `{k−1,7}`), **L3** (tap 3 is the
unique unshared interface) and **L4** (supplier) therefore transfer verbatim.

**MIXCOLUMNS-HARDCODED — must be re-derived.** Three items, all in
`fleet8/unified/code/theory.py`.

---

## 2. Item 1 — `mixcolumns_target_masks()` (theory.py:88–119). MECHANICAL.

The `[2,3,1,1]` circulant becomes `[0x0e,0x0b,0x0d,0x09]`. **Already done and
controlled**: `spec/derive_invmc.py` emits exactly these rows and proves them
three ways (identical forward derivation vs `verify_circuit.py` *and* vs
`theory.TARGET_MASKS`; `M_fwd·M_inv = I`; `M_fwd³ = M_inv`).

Drop-in: replace the function body with a load of
`wrapup/phase2/spec/invmc_target_masks.json`, or better, keep the from-scratch
derivation and only change the coefficient list — the trust-nothing property of
this project is that the spec *is* code.

---

## 3. Item 2 — `W = 0x7` and `SECTOR_TARGETS` (theory.py:200, 254–257). THE LOAD-BEARING ONE.

### What computation produced them

`theory.py` states `W = 0x7 # w = 1 + v + v^2 (the unit factor of c)` with no
derivation beside it. Reconstructed and verified today:

1. Work in `T = F2[v]/(v⁴)` (nibbles, bit *i* = vⁱ), `v = y+1`, `y` = the byte
   rotation. A 32-bit mask becomes a line vector `(t_0..t_7)` via
   `mask_to_lines` (trace-dual basis `DUALS`).
2. The dual xtime chain `2·d_k = d_{k−1} + τ_k·d_7` gives `QLINES[k]`, so
   **sector** `S_k = span{d_k, 2·d_k} ⊗ T` — a **two-coordinate** frame
   `(p on line k, q on QLINES[k])`.
3. **Measure** the 32 forward targets in that frame: `k = sector_of(L)`,
   `p = L[k]`, `q = L[PARENT[k]]`. Result (verified, all 8 sectors agree):

   | output byte `col` | ring exponent `a = (4−col) mod 4` | (p, q) |
   |---|---|---|
   | 0 | 0 | (0x9, 0xe) |
   | 3 | 1 | (0xb, 0x2) |
   | 2 | 2 | (0xd, 0x6) |
   | 1 | 3 | (0x7, 0xa) |

   (The index reversal is `theory.YBYTE`: trace duality reverses byte order.)
4. The four pairs are `yᵃ`-shifts of one another, so **solve** for the unit:
   `W := y⁻¹ · p(a=0) = 0xf · 0x9 = 0x7`. Then the closed form
   `SECTOR_TARGETS[a] = (y^{a+1}·W, v·yᵃ·W)` reproduces all four — verified PASS.

So `W` is *solved for*, not chosen, and the whole two-coordinate frame exists
**only because `c_fwd`'s GF(2)-scalars are `{x⁰, x¹}`**:

```
c_fwd(y) = 02 + 03y + 01y² + 01y³      c_inv(y) = 0e + 0by + 0dy² + 09y³
  in the v-basis (y = 1+v):
c_fwd    = 01 + 02v +      01v³        c_inv    = 01 + 02v + 04v² + 09v³
  x-powers used:  forward {x⁰, x¹}              inverse {x⁰, x¹, x², x³}
```

### What that means for the inverse, measured

* `theory.sector_of()` returns a sector for **32/32** forward targets and
  **0/32** inverse targets. The forward `(p,q)` readout does not parse at all.
* Forward line-support sizes: `{2: 20, 3: 12}`, mean 2.38.
  Inverse: `{4: 8, 5: 12, 6: 4, 7: 8}`, mean 5.38.

### The re-derived frame (computed today; **not** yet wired into the generator)

Widen the sector to the full four-tap chain,
`S'_k = span{d_k, 2·d_k, 4·d_k, 8·d_k} ⊗ T`, matching `c_inv`'s scalar set
`{x⁰..x³}`. Then, verified:

* **32/32** inverse targets are expressible as
  `p·d_k + q·2d_k + r·4d_k + s·8d_k` for a *single* `k` — the inverse has a
  universal sector problem too, on a **four**-coordinate frame.
* The universal quadruple at `a = 0` is **`(0x9, 0xe, 0x4, 0x8)`**, i.e.
  `(y·W, v·W, v², v³)` with the *same* `W = 0x7`, and the same column-shift law
  holds: `SECTOR_TARGETS_inv[a] = yᵃ · (0x9, 0xe, 0x4, 0x8)` — verified PASS for
  all four columns.
* Per-line-`k` support of `S'_k`: `[4, 5, 5, 7, 7, 6, 5, 4]` — which is exactly
  the per-output-bit union of the four inverse column targets. The frame is
  tight, not slack.

**Consequence for `laws.workset` (L1).** The forward workset is
`{j} ∪ QLINES[j]`, of sizes `[2,3,2,3,3,2,2,2]`. The inverse workset is the
4-tap line set, of sizes `[4,5,5,7,7,6,5,4]` — **roughly doubled**. Every block
line-set, the block count, and the block dimensions in the ten-block
architecture are downstream of this and must be recomputed by re-running
`laws.py`'s derivation against the new worksets. `laws.py`'s *reasoning*
(L2–L5) is untouched; its *inputs* change.

Expect: wider worksets ⇒ larger per-block dimensions ⇒ the exact SAT solves
inside the generator get materially more expensive. Price this with L13
(cost-curve pricing, `fleet1/laneB_regionbounds/code/pricing.py`) **before**
committing solver time.

---

## 4. Item 3 — `sector_value_lines` / `sector_of` (theory.py:243–274). FOLLOWS FROM §3.

Both hard-code the two-coordinate shape (`t[k] ^= p`, then `q` onto
`QLINES[k]`; and `sector_of`'s `lines[par] == lines[7]` tap test). Rewrite
against the four-tap chain: `t += Σ_i c_i·(2ⁱ d_k)`, with membership decided by
solving the 8×4 F2 incidence system per T-bit-plane (the routine
`solve_chain()` in `spec/sector_probe.py` is a working reference
implementation).

---

## 5. Not in theory.py, but blocking: the RECORD-PROVENANCED menus (flag F1)

`fleet8/unified/code/cells.py:32` reads
`fleet1/laneA_v2pricing/results/configs.json` (currency menus, 22 cell
definitions) and `cells.py:170` reads `fleet2/laneG_generator/results/…` (the
ladder spectrum). **These were read off record MixColumns circuits.** For the
inverse there is no record to read, so every `f4`-regime price is unavailable
until one of:

* wire `fleet5/laneMENU/code/derive_menu.py` (already reads a record-free menu
  out of a charged witness — fleet8's own RESULT.md §10 item 2 names this as the
  highest-value remaining move), or
* run only the `ladder` / `naive` regimes, which are record-free.

This is the single biggest non-algebraic blocker and it is independent of §3.

---

## 6. Port order (supersedes the catalog's four-step, with today's results folded in)

1. ~~Swap the target matrix~~ — **done** (`spec/invmc_matrix.json`).
2. ~~Point the oracle and the B-tripwire at it~~ — **done and calibrated**.
3. Re-derive `SECTOR_TARGETS_inv` and `workset` from §3's four-tap frame; keep
   `laws.py`'s L2–L5 reasoning intact. The constants are computed above;
   **wiring them in and re-running `laws.py` is the actual work.**
4. Recompute `Aut` for the inverse (catalog J6, `e3b_fresh/code/symgf.py`) — the
   inverse is circulant in the same way, so the Z/4 byte rotation is expected to
   survive, but *measure* it, do not assume it.
5. Run `--regime naive`, then `--regime ladder`, for record-free baselines.
6. Solve the menu problem (§5) before attempting `f4`.

---

## 7. Structural facts: inverse vs forward

Measured (`controls/C1-C4_spec_derivation.txt`):

| | forward `[2,3,1,1]` | inverse `[14,11,13,9]` | ratio |
|---|---|---|---|
| coefficient popcounts | 1, 2, 1, 1 (**5**) | 3, 3, 3, 2 (**11**) | 2.20× |
| matrix density (ones in 32×32) | **184** | **472** | 2.57× |
| mean row weight | 5.75 | 14.75 | 2.57× |
| row-weight histogram | {5: 20, 7: 12} | {11: 8, 13: 8, 15: 4, 17: 4, 19: 8} | — |
| GF(2) rank | 32 | 32 | — |
| line-support (theory frame) | {2: 20, 3: 12} | {4: 8, 5: 12, 6: 4, 7: 8} | 2.26× mean |

The density ratio is not the coefficient-popcount ratio: `2.57 ≠ 2.20`. The
extra comes from the reduction — the heavy inverse coefficients push more terms
through `x⁸ ↦ 0x1B`, and the row-weight *spread* opens from `{5,7}` (two values)
to `{11,…,19}` (five values). The forward matrix's near-uniform rows are a real
structural asymmetry, and the project's whole "20 rows of weight 5, 12 of
weight 7" self-check has no inverse analogue.

### Upper bounds, both ways

| bound | forward | inverse | note |
|---|---|---|---|
| naive XOR tree (density − q) | **152** | **440** | zero sharing; the day-0 number |
| Paar1 greedy (20 restarts) | **108** @ depth 5 | **164** @ depth 9 | `tools/baseline_naive.py`, both oracled VALID |
| via composition `M_inv = M³` | — | **264** @ depth 15 | three chained copies of the record 88; oracled VALID (`circuits/invmc_from_mc_cubed_264.json`) |
| project record | **88** @ depth 5 | — | five published circuits, all B = 56 |

Two things to note. First, the composition bound is *free* and it is a genuine
theorem — any n-gate MixColumns circuit yields a 3n-gate InvMixColumns circuit —
but at 264 it is already beaten by a 1997 greedy run in seconds. Second, the
forward Paar1 number **108** independently reproduces the catalog's B6
observation that "four unrelated designs land on exactly 108", which is a free
cross-check that `baseline_naive.py` is not lying.

Ratio of best-known to naive: forward `88/152 = 0.58`; inverse, today,
`164/440 = 0.37`. The inverse has far more room, because its rows share far
more: a denser matrix over the same 32-dimensional space is *more*
compressible, not less, in relative terms. Whether the inverse's absolute
optimum lands above or below 88 is exactly the open question, and this kit does
not answer it.

### Lower bounds — likely *better* on the inverse

Catalog **I5/I7** (gate-elimination chain, `atlas/thinktank/proofside_code/`):
`L ≥ 51` by a one-line construction, `L ≥ 56` refereed. The argument nowhere
uses the fact that the matrix is MixColumns; the catalog's own entry says
retargeting is a one-line change and "would likely give a **better** bound,
since inv-MixColumns rows are denser". That is the cheapest first proof-side
move on the inverse and it is *not* done here.

### Prior art

Deliberately not asserted in this file. Published XOR-count figures for
InvMixColumns are task **T1f**'s (`DAY2_PLAN.md`) job and require the web;
nothing in this repository states one. What *is* true and stated here: the
project's forward record is 88, and this kit's best inverse circuit today is
164 from a greedy that takes seconds. Do not quote a comparison until T1f lands.

---

## 8. Anything the kit refuses to do

`tools/verify_slp_generic.py` refuses a target file that has no `provenance`
header (exit 3), whose `rows_sha256` does not match, whose stated mask list
disagrees with the rows, whose rows do not match a from-scratch GF(2⁸)
re-derivation from the declared `mds_column`, or that is rank-deficient. All
five refusals are exercised in `controls/O1-O5_oracle.txt`. This is the
property that makes "VALID" mean something; keep it when the kit is copied into
the next repo.
