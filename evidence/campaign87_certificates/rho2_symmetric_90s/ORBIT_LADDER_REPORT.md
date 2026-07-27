# orbit-ladder — REPORT (wave 2)

## Mission
Build and run a rho^2-equivariant search seeded from structure-algebra's
exactly-symmetric 94, descend in orbit space (each orbit move = 2 real
gates), try a mixed mode with a small asymmetric budget.

## 1. Orbit-space formulation (work/orbit_engine.py, work/orbit_search.py)

sigma = rho^2 maps input bit b -> (b+16) mod 32, so on 32-bit masks
**sigma(m) is a 16-bit rotation** — one shift-or per application. Verified:
sigma commutes with MixColumns and TARGET_SET is sigma-closed (16 orbit
pairs, no fixed targets).

- Orbit variable = rep r = min(m, sigma(m)); size-2 orbit {r, sigma(r)}
  costs 2 gates, fixed mask (sigma(r)==r, byte pattern ABAB) costs 1.
- A sigma-closed value-set costs 2a + b; mixed mode adds <= L unpaired
  "loose" masks (cost 2a + b + u, u <= 3).
- Realizability is always decided on the FULL flattened mask set with the
  fast kernels copied from closure-kernel (worklist closure, early-stop
  `realizable`, incremental `_WalkState.remove_query`) and relax-kernel
  (level-BFS `relax` for emission). Files copied as work/engines_closure.py
  and work/engines_relax.py (originals untouched).
- **Walk move**: remove 1-2 orbits (or loose masks); if realizability breaks,
  enumerate the COMPLETE single-addition repair set — by repair-move's
  characterization every valid single addition w satisfies w = u ^ a
  (u unrealized, a available) AND w in pairwise-sums(avail2); candidates are
  tested with a tiny worklist cascade (`add_ok`). Repair may add a fixed
  mask (+1), an orbit (+2), or (mixed) a loose mask (+1). Plateau drift on
  equal cost (p=0.85), snapback at best+6.
- **Orbit-LNS**: destroy k orbits (1-3, periodic 5-8), rebuild by
  closure+trim+lift-to-orbits from kept + orbit-rep pool + victims
  (victim-repool per lns-extract), orbit-peel, accept <= cur.
- **Mixed extras**: demote move (drop ONE half of a size-2 orbit -> loose,
  -1 gate), loose repairs, pairing a loose half back into an orbit.
- **cert mode**: exhaustive remove-1-orbit and remove-2-orbits-add-(<=1)
  over all C(nontarget,2) pairs with the complete repair enumeration —
  machine-checked local-optimality certificates in orbit space.

## 2. Validation
- Every improvement is emitted as an index-pair circuit and passes
  mixcolumns_core.verify (GF(2^8) oracle) BEFORE being saved; the runner
  asserts emitted gate count == 2a+b+u accounting on every save. All final
  artifacts re-verified with work/verify_circuit.py: VALID.
- Engine throughput: ~90-120 walk it/s on 90-mask sets with full exact
  repair enumeration (vs ~5 it/s for structure-algebra's naive-closure
  orbit LNS), ~30 lns it/s.

## 3. New symmetry facts (work/analyze_sym.py, 0.3 s for all seeds)
| circuit | sigma-overlap | fixed | symmetrize+trim+peel |
|---|---|---|---|
| 89@5 record | 70/89 (78%) | 12 | 94 (= known symmetric best) |
| 89@6 | 72/89 (80%) | 12 | 94 |
| **Jean IMPORTED_88** | **66/88 (75%)** | 12 | **95 — a second symmetric basin** |
| SYL IMPORTED_89 | 64/89 (71%) | 16 | 98 |
| 89@7 / out_89 / 92@4 | 64/56/61% | 9-10 | 99 / 102 / 101 |

## 4. Descent trajectory (all oracle-verified)
- 94 (structure-algebra's hard plateau) -> **93 -> 92 -> 91 in 80 s** of
  orbit walk (their 8-min runs never left 94; the complete repair
  enumeration + fixed-mask repairs make the difference).
- Jean-88 symmetrized 95 -> 92; SYL symmetrized 100 -> 92 (mixed).
- Basin crossing (make_union.py: union of symmetrized orbit sets, trim,
  peel, re-descend): symA-91 U sym88-92 (J=0.63) -> **90 gates, exactly
  rho^2-symmetric** (37 pairs + 16 fixed, depth 9). VALID.
- Second cross (90 U mixA-91-with-loose) -> an INDEPENDENT 90 (depth 7,
  J=0.47 to the first 90 — two distinct symmetric 90 basins).
- 90 U 90 cross -> only 91; mixed mode from 90 -> 90 (loose budget used at
  91 level but never produced 89).
- **Certificates**: the 91 and the 90 are both PROVABLY locally optimal in
  orbit space under all remove-1 and all 666 remove-2-add-1 moves, with
  ZERO equal-cost remove-2 swaps — these basins are extremely rigid.
- No <= 88; no BREAKTHROUGH file.

## 5. Best verified circuits (agent folder top; also work/*_90g.json)
- **BEST_90gates_depth7_rho2symmetric_basin2.json — 90 gates @ depth 7,
  exactly rho^2-symmetric.** VALID.
- BEST_90gates_depth9_rho2symmetric.json — 90 @ 9, distinct basin. VALID.
- Improves the best known exactly-symmetric circuit 94 -> 90 (-4); now only
  +1 over the repo's asymmetric 89 and +2 over Jean's 88. Half-symmetry
  premium collapsed from +5 to +1/+2.

## 6. Mishaps
Two `pkill -f`/`pgrep -f` calls matched my own wrapper shell's command line
(exit 144, same failure class as the wave-1 lns-pool incident); no other
agent's processes were touched (patterns contained only my own file names).
Killed by explicit PID afterwards.

## 7. Single most promising next step
The two 90s are rigid (certified) but sit in DIFFERENT basins, and loose
masks let the walk hover at 90 with u=3. Desymmetrize both 90s and hand
them to the merged-engine asymmetric polish (a symmetric 90 one basin away
from 88's symmetrization is a better asymmetric warm start than any 89),
and run windowed SAT (sat-deep's encoding) IN ORBIT SPACE on the 90s:
k=10-14 orbit cone windows have half the variables of mask-space windows,
and one improving window at r=k-1 there is -2 real gates (89 symmetric
would need b odd, e.g. 40x2+9; 88 = 40x2+8 or 36x2+16).
