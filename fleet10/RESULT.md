# fleet10 / cleanroom — what an independent effort with no project knowledge reaches

> **Written post-hoc, 2026-08-29, during the wrap-up wave, entirely from on-disk
> evidence.** fleet10 shipped with no `RESULT.md`, no `README`, no `PREREG` and no
> ledger, and was referenced nowhere in the tree (`wrapup/reports/fleet9_12.md`
> LEAD L5). Nothing below was witnessed; every number is re-derived from the files
> in `fleet10/cleanroom/` and each is cited to the file it came from. Where a claim
> cannot be grounded in a file it is marked **UNGROUNDED** or **INFERRED** and left
> as a claim, not a fact. §10 lists everything in that category.

**One job — reconstructed from what is on disk:** build a MixColumns XOR circuit
from nothing. `spec/` contains the 32 target masks and a verifier, and *nothing
else*. No seed circuit, no record data, no menus, no block decomposition, no
import of `atlas/slp_opt.py` or `fleet8/unified`. The whole of `work/` is written
from first principles against that spec.

That makes fleet10's number a **calibration, not a search result**: it prices what
the project's accumulated knowledge is worth. **A from-scratch effort lands at 93
gates. The project's record is 88.** See §8.

**Headline, verified 2026-08-29:**

```
$ python3 verify_circuit.py fleet10/cleanroom/work/FINAL.json
gates=93 depth=7 outputs_built=32/32 problems=0
VERDICT: VALID MixColumns circuit
```

---

## 1. The spec — everything the effort was given

`fleet10/cleanroom/spec/` is 2 files, 8 K:

| file | what it is |
|---|---|
| `targets.json` | `n_inputs: 32`, `targets` (32 hex masks), `targets_int` (the same as ints), and a one-line `note`: *"Each target is a subset of the 32 input bits, given as a bitmask. Target i must be produced as the XOR of the input bits its mask selects."* |
| `verify.py` | **byte-identical to the repository's `verify_circuit.py`** — `md5sum` on both gives `682053357d0d873b6dee527e74b83826` (re-checked 2026-08-29). It is a *copy for self-containment*, **not** an independent verifier. Any claim of "two independent checks" would be false. |

The search really did aim at MixColumns: the C sources hardcode
`TGT[0] = 16875904u` (`work/bp.c:27-32`), and
`json.load(spec/targets.json)['targets_int'][0]` is `16875904` = `0x01018180` =
`targets[0]` = `"0x01018180"`. Re-checked 2026-08-29.

**Self-containment, machine-checked.** Every absolute path mentioned in any `.c`,
`.py` or `.sh` file under `fleet10/` is one of:

```
/home/joebachir20/xor_ui/slp-plateau-search/fleet10/cleanroom/spec
/home/joebachir20/xor_ui/slp-plateau-search/fleet10/cleanroom/spec/targets.json
/home/joebachir20/xor_ui/slp-plateau-search/fleet10/cleanroom/work
/home/joebachir20/xor_ui/slp-plateau-search/fleet10/cleanroom/work/symsol_
```
(`grep -rhno '/home/[a-zA-Z0-9_./-]*' --include='*.py' --include='*.c' --include='*.sh' fleet10 | sort -u`,
2026-08-29). **No fleet10 file reads anything outside `fleet10/cleanroom/`.** That
is the evidence for the clean-room framing; the *intent* is inferred, not
documented (§10).

**Wall span.** Directory and file mtimes run `Aug 24 14:23` (`cleanroom/`,
`spec/`) to `Aug 24 21:56` (`work/wshD1.log`, `wshD2.log`) — about **7.5 hours on
one day**. That is the only provenance on disk.

---

## 2. Method A — randomized Boyar–Peralta, written from scratch in C

`work/bp.c` (9 708 B) and four successors. Its own docstring (`bp.c:1-17`):

> State: base S of 32-bit masks (starts as the 32 unit vectors). `d[t]` = exact
> minimum number of S-elements whose XOR is target t. Step: consider every pair sum
> `u = S_i ^ S_j` not already in S; score by the total of new distances
> `sum_t min(d[t], dist_S(t^u)+1)`; pick the best (random among ties, optional norm
> tie-break). **In symmetric mode the pick also adds rot8/16/24 of `u`** … and
> scoring uses min over the 4 rotations. Distance queries are bounded … Runs
> restarts until the monotonic deadline; writes best circuit … whenever improved.

CLI (`bp.c:14`): `./bp seed mode(0=asym,1=sym) norm_mode(0=none,1=max,2=min) time_s out.json`.
Its own open-addressing hash sets, its own xorshift RNG, its own bounded
distance query — no library beyond libc.

**Five generations, each a real change** (diffs re-run 2026-08-29):

| source | mtime | what it adds over its predecessor |
|---|---|---|
| `bp.c` | 14:30 | the base search |
| `bp2.c` | 14:32 | `load_circ()` / `publish()` — warm-start a restart from a **shared best** file (`argv[6]`), and publish improvements back to it |
| `bp3.c` | 14:33 | accepts **equal-cost** circuits (`cur==cnt && (rnd()&1)`, `bp3.c:128`), prunes at `ns-32>best` instead of `>=best` (*"allow equal (plateau)"*, `bp3.c:195`), and only prints `BEST` on a **strict** improvement (`bp3.c:270`) |
| `bp4.c` | 14:35 | an **in-memory annealing incumbent**: accepts `cnt==ninc+1` with probability 15/100 (`bp4.c:261-271`) and allows a `+1` uphill cap (`bp4.c:200`) |
| `bp5.c` | 14:45 | an **exact iterative-deepening DFS endgame** (`eg_lb()`, `eg_dfs()`, `endgame()`, `bp5.c:107-202`) with a 150 000-node cap, falling back to greedy when capped |

Compiled binaries `bp bp2 bp3 bp4 bp5 bp5s` sit beside them (143 K; regenerable —
`wrapup/KEEP_DELETE.md:126`).

### 2.1 What BP measured

**Wave 1 — 8 independent workers, no sharing** (`work/w0.log` … `w7.log`,
`best_w0.json` … `best_w7.json`; all 8 re-verified VALID 2026-08-29):

| worker | log's last `BEST` line | verified |
|---|---|---|
| w0 | `BEST 99 gates (restart 11, 13s)` | 99 @ 5 |
| w1 | `BEST 95 gates (restart 54, 76s)` | 95 @ 7 |
| w2 | `BEST 101 gates (restart 43, 44s)` | 101 @ 6 |
| w3 | `BEST 98 gates (restart 94, 108s)` | 98 @ 5 |
| w4 | `BEST 96 gates (restart 31, 48s)` | 96 @ 7 |
| w5 | `BEST 101 gates (restart 90, 89s)` | 101 @ 5 |
| w6 | `BEST 99 gates (restart 74, 84s)` | 99 @ 6 |
| w7 | `BEST 95 gates (restart 45, 66s)` | 95 @ 6 |

So **unaided, one worker, ~2 minutes: 95–101 gates.**

**The deepest logged BP descent** is `work/w5C_1.log`, which walks
`100 → 99 → 97 → 95 → 94` and ends:

```
BEST 94 gates (restart 352, 375s)
```

**94 is the best gate count BP reached on its own.** `work/b5C_1.json` verifies
`gates=94 depth=8 … VALID` (2026-08-29). 32 distinct 94-gate circuits are on
disk across 37 files (§7.3).

**Later waves' logs are mostly empty and this is explained by the code, not by a
failure:** `w2_*`, `w3_*`, `w4_*`, `w5A_*`, `w5B_*` are 0 bytes except
`w2_4.log` and `w3_4.log` (each one line, `BEST 98 gates (restart 1, 0s)`).
From `bp3.c:270` onward `BEST` prints only on a **strict** improvement over the
worker's running best, and those waves were started from a shared incumbent
already at 94, so a silent worker is a worker that never beat its seed. Their
results are in the JSONs, not the logs: all sixteen of `b3_w0..7.json` and
`b4_w0..7.json` hold 94 gates.

### 2.2 The ρ-symmetry penalty — the second reusable number

`bp.c` mode 1 forces the circuit to be closed under byte-rotation: every pick
adds `rot8/16/24` of the chosen value at once, and scoring is the min over the
four rotations (`bp.c:1-17`). The two sides were run as a matched pair at the same
minute (both files mtime `Aug 24 14:30`, immediately after `bp` was compiled at
14:30) and both re-verified VALID 2026-08-29:

| file | mode | verified |
|---|---|---|
| `work/test_asym.json` | asymmetric | **95 gates**, depth 8 |
| `work/test_sym.json` | **symmetric** | **108 gates**, depth 4 |

and the best symmetric circuit anywhere in the lane is 106:

| file | verified | note |
|---|---|---|
| `work/islandS.json` | **106 gates**, depth 5 | the symmetric island |
| `work/t6.json` | 106 gates | **byte-identical circuit** to `islandS.json` (same md5 over the gate list) |

**Measured penalty for forcing ρ-symmetry in this search: 12–13 gates.**
13 on the matched same-minute pair (108 vs 95); **12** against the lane's best
asymmetric result (106 vs 94). Symmetric mode buys depth (4–5 vs 7–9) and pays
for it heavily in count.

This is one of only two direct measurements in the repository on that question.
The other is fleet9's: *"No ρ-fixed 88 exists in 54,889 circuits"*
(`fleet9/laneENUM/RESULT.md:347`, and line 40: *"not one circuit is ρ-fixed"*).
They agree in direction and are methodologically independent — fleet10 priced
symmetry in a *greedy search*, fleet9 counted it in a *census*.

### 2.3 The naive baseline

`work/baseline.json` — **124 gates, depth 5, VALID** (2026-08-29). mtime `14:26`,
which is *before* any `bp` binary exists (`bp`, `14:30`). No script under
`fleet10/` contains the string `baseline`, so **how it was produced is not
recoverable from disk** (§10). What it is good for is the span it brackets:
**124 → 93 is the whole distance this lane travelled.**

---

## 3. Method B — SAT window repair

`work/satfix.py` (8 250 B) and four parameter variants. Its docstring
(`satfix.py:2-10`):

> Loop: load incumbent circuit; delete a random **dependency-closed** set of *m*
> gates; keep the rest as **constant signals**; ask **CryptoMiniSat** whether
> `f = m-1` (or `m-2`) new free gates can restore all 32 targets. On SAT, rebuild,
> verify, publish.

Read from the code (`satfix.py:56-216`), the two asks it actually issues are:

* **shrink** (`satfix.py:234-235`) — `f = m-1`. A genuine gate saving. UNSAT here
  is a real, if local, certificate: *this dependency-closed window of m gates
  cannot be rebuilt in m−1*.
* **plateau** (`satfix.py:231-232`) — `f = m`, with `force_diff=True`, which forbids
  one specific mask of the deleted window (`satfix.py:104-107, 172-177`). A lateral
  move that must land somewhere new.

The window is grown by upward dependency closure with a cap of `m_want + 2`
(`satfix.py:85`), so a "plateau" ask can arrive with `m = m_want + 2` while `f` was
fixed at `m_want` — which is where the `m − f = 2` rows in the logs come from. There
is **no separate "save two gates" mode in the code**; the m−2 asks are a side
effect of over-deletion.

The five scripts are the same instrument at five settings (diffs re-run 2026-08-29;
`satfix.py` vs each is 2–5 changed lines):

| script | window size | plateau probability | per-window budget | note |
|---|---|---|---|---|
| `satfix.py` | `randint(4, 9)` | 0.35 | 40 s | the base |
| `satfix_walk.py` | `randint(4, 7)` | **0.60** | 30 s | plateau-heavy: a neutral walk |
| `satfix_hunt.py` | `randint(7, 10)` | 0.10 | 150 s | shrink-heavy |
| `satfix_hunt2.py` | `randint(9, 12)` | 0.10 | 240 s | bigger windows |
| `satfix_deep.py` | `randint(10, 14)` | 0.15 | **300 s** | **and it drops the `a < b` operand-ordering clauses** (`satfix.py:131-133` are absent), i.e. a weaker symmetry break — sound for UNSAT, just slower |

### 3.1 The full tally — 2 623 windows

Counted 2026-08-29 over the 24 SAT logs
(`cat work/ws[0-9].log work/wsdeep.log work/wsh*.log work/wsw*.log | grep -c '^  window m='`;
the naive glob `ws*.log` double-counts and gives 5 219 — do not use it):

| | attempts | SAT | UNSAT | TIMEOUT |
|---|---|---|---|---|
| **shrink** (`f < m`) | **1 924** | **1** | **1 314** | 609 |
| **plateau** (`f = m`) | 699 | 468 | 122 | 109 |
| **total** | **2 623** | 469 | 1 436 | 718 |

**Exactly one line in the entire 24-log corpus records a gate improvement**
(`grep -h` over the same 24 files):

```
work/wsh3.log:4    window m=9 f=8 miss=5: SAT in 57.7s
work/wsh3.log:5  [hunt3] attempt 4: 94 -> 93 gates
```

**Hit rate: 1 in 2 623 windows, or 1 in 1 924 gate-saving asks (0.05 %).** That
single 57.7-second solve is the only reason this lane's number is 93 and not 94.

Per-tag attempt counts, from each log's own closing line
(`[tag] done after N attempts`), which agree with the window counts:

| tag | attempts | log |
|---|---|---|
| `walk1` / `walkB` / `walkC` / `walkD` | 543 / 569 / 555 / 572 | `wsw1.log`, `wswB.log`, `wswC.log`, `wswD.log` |
| `hunt2` / `hunt3` | 57 / 53 | `wsh2.log`, `wsh3.log` |
| `huntB1` / `huntB2` | 50 / 50 | `wshB1.log`, `wshB2.log` |
| `huntC1` / `huntC2` | 26 / 27 | `wshC1.log`, `wshC2.log` |
| `huntD1` / `huntD2` | 28 / 28 | `wshD1.log`, `wshD2.log` |
| `deep` | 14 | `wsdeep.log` |
| (untagged wave) | 3+4+4+4+3+6+3 = 27 | `ws1.log` … `ws7.log` |
| (started, no window) | 1 / 0 | `wsh1.log`, `wsh4.log` |

**Solver time: 70 334.7 s = 19.54 h**, summed exactly from the logs' own
`in <x>s` fields (`grep -o 'in [0-9.]*s'` over the 24 files, 2026-08-29).

### 3.2 Where the solver's wall is

Window size decides everything. Counted 2026-08-29:

| m | decided (SAT+UNSAT) | timed out |
|---|---|---|
| 4 | 271 | 0 |
| 5 | 452 | 1 |
| 6 | 549 | 26 |
| 7 | 473 | 159 |
| 8 | 120 | 186 |
| 9 | 37 | 140 |
| 10 | 3 | 79 |
| 11–14 | **0** | 127 |

**This corrects `wrapup/reports/fleet9_12.md`**, which states *"Every attempt at
m ≥ 8 timed out … the decided windows are all m ≤ 7."* Not so: **160 windows at
m ≥ 8 were decided** (120 at m=8, 37 at m=9, 3 at m=10). The true cliff is at
**m = 11**: `satfix_deep.py`'s entire 14-attempt run at m ∈ [10,14] timed out,
every one, at 56–334 s (`work/wsdeep.log`, all 14 lines).

**The 1 314 UNSATs are the lane's only certificates.** Each says: *this particular
dependency-closed window of m ≤ 10 gates in this particular circuit cannot be
rebuilt in m−1.* Local, tiny, and true — and worth nothing about 87.

---

## 4. Method C — island portfolio with migration

`work/migrate.sh` (709 B). Four islands `A B C D`; every 720 s take the best
island file and copy it over any island **more than 5 gates behind**
(`migrate.sh:16`: `if [ $((n-best)) -gt 5 ]`), for `5400` s of wall.

**Result: the migration never fired.** `work/migrate.log`, `migrate2.log`,
`migrate3.log` are all **0 bytes**, and the reason is visible in the island files
(all re-verified VALID 2026-08-29):

| island | verified |
|---|---|
| `islandA.json` | 94 gates, depth 9 |
| `islandB.json` | 94 gates, depth 9 |
| `islandC.json` | 94 gates, depth 7 |
| `islandD.json` | 97 gates, depth 6 |
| `islandS.json` | 106 gates, depth 5 (the *symmetric* island, not in the A–D migration set) |

The maximum spread over A–D is **97 − 94 = 3**, and the threshold is **> 5**. The
method contributed nothing measurable **because the threshold was never reached**,
not because migration is a bad idea. ⚠ The three empty logs are a *result*; never
sweep them by size (`wrapup/KEEP_DELETE.md:127`, conflict C17).

`work/collect.sh` is the harvest: it walks `island*.json b*_*.json shared_best.json
t*.json test_*.json satinc.json satbest_*.json`, takes the smallest gate count, and
**crowns it only after `python3 ../spec/verify.py` passes** (`collect.sh:4-13`),
then copies it to `FINAL.json`. `FINAL.json` and `satbest_walk1.json` are
byte-identical (`md5 6bb8a324ed9ab61eb6e094d94e4324bf`), so the published best came
from the `walk1` neutral-walk run.

---

## 5. Method D — symmetry-quotient SAT: written, never concluded

`work/satquot.py` (5 275 B), docstring (`satquot.py:2-17`):

> A symmetric circuit is generated by k 'orbit gates' `w_1..w_k`, where
> `w_i = v_a ^ rot8r(v_b)` … Materializing every orbit costs **4 real XOR gates per
> `w_i` ⇒ 4k total**. Each of the 8 target orbits (reps = `targets[0..7]`) must equal
> some `rot8r(w_i)`. … Usage: `python3 satquot.py k [seed] [timeout_s]`. Prints SAT +
> the orbit gates and **writes `symsol_k.json`** … on success.

**No `symsol_*.json` exists anywhere in the repository**
(`find / -name 'symsol*'` over the repo root, 2026-08-29, returns nothing) and no
log names it. Whether it was ever run is **unrecoverable** (§10).

Two facts about it that are grounded and worth carrying forward:

1. Only gate counts that are **multiples of 4** are reachable in this encoding. A
   fully ρ-symmetric **88 is therefore not excluded** — 88 = 4 × 22 — so **k = 22 is
   exactly the question**, and it is one cheap run.
2. Both independent signals say it is unpromising: this lane's own symmetric mode
   costs 12–13 gates (§2.2), and fleet9 found **zero** ρ-fixed circuits among
   54 889 88s (`fleet9/laneENUM/RESULT.md:347`). But
   `fleet9/laneENUM/RESULT.md:542-543` *asks for precisely this search*. An
   instrument and a written request for it sit in the same repository and were
   never joined up (`wrapup/reports/fleet9_12.md` LEAD L6).

---

## 6. Verification — done fresh for this document

Every circuit named in this file was re-run through the repository oracle on
**2026-08-29** with `python3 verify_circuit.py <file>` from the repo root.
**All 20 returned `VERDICT: VALID MixColumns circuit` with `outputs_built=32/32
problems=0`.**

The headline:

```
$ python3 verify_circuit.py fleet10/cleanroom/work/FINAL.json
gates=93 depth=7 outputs_built=32/32 problems=0
VERDICT: VALID MixColumns circuit
```

The rest: `baseline` (124@5), `test_sym` (108@4), `test_asym` (95@8), `islandS`
(106@5), `islandA` (94@9), `islandB` (94@9), `islandC` (94@7), `islandD` (97@6),
`b5C_1` (94@8), `b5D_0` (97@8), `best_w0..7` (99@5, 95@7, 101@6, 98@5, 96@7,
101@5, 99@6, 95@6), and all eight 93-gate files (§7.2).

---

## 7. Result

### 7.1 Verdict

**93 gates, depth 7, VALID — reached from a bare spec in ~7.5 hours on one day,
by a two-stage pipeline: a from-scratch C Boyar–Peralta search to 94, then one
successful SAT window repair to 93.** No 88, no 87, and nothing here bears on
either. The lane's product is a **number**, not a circuit.

Route, with each step cited:

```
 124  baseline.json                      (provenance not on disk — §10)
   ↓  bp.c, 8 workers, ~2 min each
95–101  best_w0..7.json / w0..w7.log
   ↓  bp2..bp5.c, shared incumbent, plateau + annealing + exact endgame
  94  b5C_1.json  ← w5C_1.log "BEST 94 gates (restart 352, 375s)"
   ↓  satfix_hunt.py — 1 hit in 2 623 windows
  93  wsh3.log:5  "[hunt3] attempt 4: 94 -> 93 gates"
   ↓  collect.sh, verified before crowning
  93  FINAL.json  (== satbest_walk1.json, md5 6bb8a324ed9ab61eb6e094d94e4324bf)
```

### 7.2 The 93s — five distinct circuits, not one

Eight files hold 93 gates; over their gate lists there are **five distinct
circuits** (md5 over the canonical gate list, 2026-08-29):

| circuit | files | verified depth |
|---|---|---|
| `d489e5a1` | `FINAL.json`, `satbest_walk1.json` | **7** |
| `b8ed5e9f` | `satbest_hunt3.json`, `satinc2.json` | 8 |
| `720658e6` | `satbest_walkB.json` | 8 |
| `87b1867e` | `satbest_walkC.json` | 9 |
| `0387241b` | `satbest_walkD.json`, `satinc.json` | 7 |

The four `walk*` runs each started from the 93 and spent 543–572 windows moving
laterally without ever reaching 92. **93 is where this lane stopped, and it stopped
against a wall, not against a clock**: 1 924 gate-saving asks, one hit, and that hit
was at 94 — the descent from 93 was attempted ~2 200 times and never once succeeded.

### 7.3 The whole circuit population

62 JSONs in `work/`, all with a single `gates` key. Gate-count histogram and
distinct-circuit count (2026-08-29):

| gates | files | distinct circuits |
|---|---|---|
| 93 | 8 | **5** |
| 94 | 37 | **32** |
| 95 | 3 | 3 |
| 96 | 1 | 1 |
| 97 | 3 | 3 |
| 98 | 2 | 2 |
| 99 | 2 | 2 |
| 101 | 2 | 2 |
| 106 | 2 | **1** (`islandS.json` = `t6.json`) |
| 108 | 1 | 1 |
| 124 | 1 | 1 |

The 94-level is broad — **32 distinct circuits** — and the 93-level is thin. That
shape is consistent with 93 being a genuine local wall for this method, and it is
the only thing in the lane that even resembles a structural observation.

### 7.4 Cost

**Solver time: 19.54 h, measured** (§3.1). **BP time: not measured.** The BP logs
record per-restart seconds but no wall totals, there is no ledger, and the only
bound is file mtimes. The `~7.5 h` span in §1 is a *wall* span across an unknown
number of concurrent workers, not a CPU figure. Any CPU number for the BP side
would be **UNGROUNDED**.

---

## 8. What the calibration means — stated plainly

**A capable agent, given only the 32 target masks and a verifier, and no project
knowledge whatsoever, reaches 93 gates in one working day. This project's record is
88.**

That gap — **five gates** — is the measured value of everything this repository
accumulated: the block decomposition, the currency menus, the SAT ladders, the
symmetry normalisation, the plateau census, the seed lineages, every campaign in
`experiments/`, `atlas/`, `campaign_87/` and `fleet1`–`fleet12`. Not an estimate;
one clean-room run against one record.

Read against the published frontier
(`README.md:8-9`, `README.md:14-21`):

| point | count | depth | source |
|---|---|---|---|
| this lane, clean-room | **93** | 7 | `fleet10/cleanroom/work/FINAL.json` |
| published, Osvik–Canright | 94 | 5 | `README.md:14-16` |
| published, Sun–Yang–Li | 89 | unstated | `README.md:39-40` |
| published record, Jean | 88 | (7, forced) | `README.md:19-21`, `README.md:31-33` |
| this project's frontier | 97 / 92 / **88** | 3 / 4 / 5 | `README.md:8-9` |

So the clean-room result is **one gate below the published 94** — at a worse depth,
so it dominates nothing — and **five above the record**. A day of competent
from-scratch work gets you to roughly the state of the published art of 2024. It
does not get you near 88. **That is the finding.**

**This is the only calibration of its kind in the repository.** No other lane was
run without project context; every other search in the tree inherits seeds, menus,
banked levels or a block decomposition. `INDEX.md:55` and
`wrapup/KEEP_DELETE.md:564-566` both record it as such — the latter as a
never-delete: *"the only clean-room calibration in the repository … Deleting it
destroys the '93 from scratch' datum."* This document is the writeup that entry
asked for.

Two secondary numbers are reusable and are cited nowhere else:

* **ρ-symmetry costs 12–13 gates** in a greedy search (§2.2) — the only *search-side*
  price for the symmetry that fleet9 studied census-side.
* **SAT window repair near an optimum hits 1 in 1 924** (§3.1) — the measured death
  curve of the method: plentiful improvements on the way down from 124, exactly one
  at 94, none at all from 93.

---

## 9. File map

```
fleet10/
├── RESULT.md                     ← this file (written 2026-08-29, post-hoc)
└── cleanroom/                    832 K, 151 files, all mtime Aug 24
    ├── spec/                     8 K — everything the effort was given
    │   ├── targets.json          32 MixColumns masks (hex + int) + a one-line note
    │   └── verify.py             byte-identical copy of the repo's verify_circuit.py
    └── work/                     824 K — 14 sources, 6 binaries, 62 JSONs, 67 logs
```

**`work/` — sources (14)**

| file | what it is |
|---|---|
| `bp.c` `bp2.c` `bp3.c` `bp4.c` `bp5.c` | the five generations of the C Boyar–Peralta search (§2) |
| `bp` `bp2` `bp3` `bp4` `bp5` `bp5s` | their compiled binaries, 143 K. **Regenerable**; `bp5s` is a second compile of `bp5.c` |
| `satfix.py` | the SAT window-repair instrument (§3) |
| `satfix_walk.py` `satfix_hunt.py` `satfix_hunt2.py` `satfix_deep.py` | the same instrument at four other window/budget settings; `_deep` also drops the `a<b` operand-ordering clauses |
| `satquot.py` | the symmetry-quotient SAT search. **Never concluded** (§5) |
| `migrate.sh` | the 4-island, 720 s, >5-gate migration driver (§4) |
| `collect.sh` | best-of harvest; verifies before crowning; writes `FINAL.json` |
| `seedpatch.py` | 187 B; despite the name, it only prints the last line of each `w*.log` — a progress peek, not a patcher |

**`work/` — results (62 JSONs)**

| file(s) | what it is |
|---|---|
| **`FINAL.json`** | **the lane's answer: 93 gates, depth 7, VALID.** Byte-identical to `satbest_walk1.json` |
| `baseline.json` | 124 @ 5 — the pre-search starting point; no generator on disk |
| `test_sym.json` / `test_asym.json` | the matched ρ-symmetry A/B: 108 @ 4 vs 95 @ 8 |
| `best_w0..7.json` | wave-1 per-worker bests (95–101), unaided `bp` |
| `b2_w4.json` | the one wave-2 (`bp2`) output, 98 |
| `b3_w0..7.json`, `b4_w0..7.json` | waves 3 and 4 (`bp3`, `bp4`), all 94 |
| `b5A_0/1`, `b5B_0/1`, `b5C_0/1`, `b5D_0/1.json` | wave 5 (`bp5`): 94 ×6, 97 ×2 |
| `islandA/B/C/D.json` | the migration portfolio: 94, 94, 94, 97 |
| `islandS.json` | the symmetric island: 106 @ 5. Same circuit as `t6.json` |
| `shared_best.json` | the warm-start file `bp2`+ read and published into (94) |
| `t2..t6.json`, `diag_seed/out/out2.json` | per-wave snapshots and diagnostics, 94 (and `t6` = 106) |
| `satbest_t3/s4/s7/walk2.json` | SAT-repair bests that stalled at 94 |
| `satbest_hunt3/walk1/walkB/walkC/walkD.json`, `satinc.json`, `satinc2.json` | the seven other 93-gate files — five distinct circuits (§7.2) |

**`work/` — logs (67)**

| file(s) | what it is |
|---|---|
| `w0..w7.log` | wave-1 BP descent traces — the only BP logs with a full curve |
| `w2_*.log`, `w3_*.log`, `w4_*.log`, `w5A_*.log`, `w5B_*.log` | later BP waves; **empty by design** (`bp3.c:270` prints only on strict improvement), except `w2_4` and `w3_4` |
| `w5C_0/1.log`, `w5D_0/1.log` | the wave-5 workers that did improve; **`w5C_1.log` is where 94 was reached** |
| `ws1..ws7.log` | the first `satfix.py` wave, 27 windows |
| `wsdeep.log` | `satfix_deep.py`: 14 windows at m ∈ [10,14], **all timeout** |
| `wsh1..wsh4.log`, `wshB1/B2`, `wshC1/C2`, `wshD1/D2.log` | the `hunt` runs. **`wsh3.log:5` is the single improvement line in the lane** |
| `wsw1..wsw3.log`, `wswB/C/D.log` | the `walk` runs, 543–572 windows each; the four big ones are the bulk of the 2 623 |
| `migrate.log`, `migrate2.log`, `migrate3.log` | **0 bytes — and that is the result** (§4). Never sweep by size |

⚠ **Do not confuse with repo-root strays.** `wshB1.log`, `wshB2.log`, `wshC1.log`,
`wshC2.log` also exist at the repository root. They are **not** copies — md5s all
differ and the root files are 123–124 bytes
(`wrapup/reports/fleet9_12.md` §7 item 9).

---

## 10. What is not grounded

Listed so no one downstream mistakes any of it for a measurement.

1. **INFERRED — "no project knowledge".** No `PREREG`, brief or commissioning note
   exists. The clean-room framing rests on (a) `spec/` containing only targets and a
   verifier, (b) the machine-checked fact that no fleet10 source reads any path
   outside `fleet10/cleanroom/` (§1), and (c) the absence of any seed, menu, block
   decomposition or import of project code. That is strong circumstantial evidence
   of the *condition*, not documentation of the *intent*.
2. **UNGROUNDED — why fleet10 exists and who commissioned it.** No PREREG, no
   ledger, no mention in any campaign document. Directory mtime `Aug 24 14:23` is
   the entire provenance.
3. **UNGROUNDED — `baseline.json`'s provenance.** 124 @ 5, VALID, written at 14:26,
   four minutes before `bp` was compiled. No script under `fleet10/` mentions it.
4. **UNGROUNDED — BP CPU cost.** §7.4. Only the SAT side (19.54 h) is measured.
5. **UNRECOVERABLE — whether `satquot.py` was ever run.** No output, no log, no
   ledger row. All that can be said is that it produced nothing on disk.
6. **INFERRED — the wave↔binary mapping** (`wN_*.log` ↔ `bN_w*.json` ↔ `bpN`). It
   follows from filenames, mtime ordering and the `strictly`-print change in
   `bp3.c:270`; no launcher script survives to confirm it. No number in this
   document depends on it.
7. **Corrected here, from the files:** `wrapup/reports/fleet9_12.md` states that
   every m ≥ 8 window timed out and all decided windows were m ≤ 7. **160 windows at
   m ≥ 8 were decided** (§3.2). The same report describes a *"save two gates"* ask as
   designed; the code has no such mode (§3).

---

## 11. How to continue this (everything needed is on disk)

The lane is fully self-contained and needs nothing outside `fleet10/cleanroom/`.

```bash
cd /home/joebachir20/xor_ui/slp-plateau-search/fleet10/cleanroom/work

# rebuild the search (the binaries are regenerable):
gcc -O2 -o bp5 bp5.c

# a fresh clean-room run: seed, mode(0=asym,1=sym), norm(0/1/2), seconds, out
./bp5 12345 0 0 600 fresh.json

# push an incumbent with SAT window repair: circuit, seed, minutes, tag
python3 satfix_hunt.py FINAL.json 7 60 mytag     # needs pycryptosat

# the one question this lane wrote an instrument for and never answered (§5):
python3 satquot.py 22          # 88 = 4 x 22, so k=22 is exactly the question

# re-verify anything, with the repo oracle rather than the local copy:
cd /home/joebachir20/xor_ui/slp-plateau-search
python3 verify_circuit.py fleet10/cleanroom/work/FINAL.json
```

* **The calibration is already banked.** Re-running BP will not change what fleet10
  is for. If anyone wants to *sharpen* the calibration, the useful experiment is a
  second clean-room run by a different agent — one data point is one data point.
* **Do not delete `migrate*.log`** (0 bytes) or the `b*_w*.json` intermediates. The
  empty logs are the migration result; the wave structure is the only record of how
  the search progressed (`wrapup/KEEP_DELETE.md:127`).
* **`satquot.py` at k = 22 is the one cheap open item**, and fleet9 independently
  asked for it (`fleet9/laneENUM/RESULT.md:542-543`). Both available signals say it
  will fail. It has still never been asked.
