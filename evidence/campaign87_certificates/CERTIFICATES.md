# Machine-checked certificates — campaign 87

Every result below is a **negative** result: a decision procedure was run to
completion (or a SAT solver returned UNSAT) over a precisely defined
neighbourhood of a verified circuit, and nothing smaller was found. No 87-gate
circuit was found anywhere.

Two different kinds of certificate live here, and they carry different weight:

- **Exact window certificates** (`exact_window/`, `exact_k4/`, `pop_decider/`,
  `family3_exact/`) — a provably complete enumeration. A "no" from these
  procedures *is* a proof for the neighbourhood it covers, with completeness
  proofs in the producing modules' docstrings and validation against independent
  brute force (25/25, 12/12 at budgets 1–2; 1 257 instances incl. 122 genuine
  NOs at budget 3). **Those two modules ship here**, verbatim as archived:
  `code/exact_window.py` (budgets 1–2) and `code/exact_k4.py` (budget 3). Every
  verdict log in this folder was produced by them, and the case analysis that
  makes the proof is in their docstrings — the certificates are not asked to be
  taken on trust.
- **Windowed SAT certificates** (`sat_deep/`, `loose_sat/`, `family3_sat/`) —
  UNSAT **relative to the encoding's fixed slot order** (broken kept masks pinned
  at their original positions, free slots at the removed masks' positions). This
  is strong evidence, **not** a completeness proof, and is cited as such
  throughout.

The files here are the small per-run verdict summaries and per-window verdict
logs. The multi-MB resumable progress logs are not included in this repository;
they are listed at the end by path in the raw campaign archive.

---

## 1. `exact_window/` — the first exact decision procedure

"Remove a window of k masks; can k−1 or fewer new masks restore all 32 targets?"
Frontier-cascade closure with rollback; exact at budget 1 (k=2) and budget 2
(k=3); honest partial DFS above that (those runs are recorded as `nosol`, never
as irreducible). ~113 000 windows decided in total.

| subject | k=2 (budget 1) | k=3 (budget 2) | file |
|---|---|---|---|
| Jean's 88 (`IMPORTED_88`) | **1 540 / 1 540 exhaustive, all irreducible** | **27 720 / 27 720 exhaustive, all irreducible** | `k2_IMPORTED_88.json`, `k3_IMPORTED_88.json` |
| 89@5 (repo record) | 1 596 / 1 596 exhaustive | **29 260 / 29 260 exhaustive** (in two parts) | `k2_mixcolumns_89gates_depth5.json`, `k3_d5_all*.json` |
| 89@6 | 1 596 / 1 596 exhaustive | **29 260 / 29 260 exhaustive** | `k2_seed_89_at_depth6.json`, `k3_d6_all.json` |
| 89 (sub89 rerun), 89@7, 89@10 (`out_89`) | 1 596 / 1 596 exhaustive each | 4 000 structural windows each | `k2_*`, `k3_smart_*` |

**Theorem (k ≤ 3, Jean's 88):** no 87-gate circuit exists within "remove ≤ 3
masks, re-add fewer" of it — any 87 differs from it by **≥ 4 masks**.
**Theorem (89 seeds):** the remove-2-add-1 "hub move" neighbourhood of all five
89 seeds is exactly empty; both record 89s are ≥ 4 masks from any 88 in this
move class.

The k=4/k=5 entries in this folder (`k4_*`, `k5_*`) are **partial** searches —
their stats show `nosol`, not `irreducible`. They prove nothing on their own.

---

## 2. `exact_k4/` — exact budget-3, the 12 siblings, and the first population sweep

Exact budget-3 ("remove 4, restore with ≤ 3") with the completeness proof in
`code/exact_k4.py`'s module docstring (shipped here); validated on **1 257 instances against an
independent complete brute force, 100 % agreement including 122 genuine NOs**,
identically under CPython 3.10 and PyPy 3.11 (`full_test_cpython.log`,
`full_test_pypy.log`).

- **12 sibling 88s** (the syl-move plateau siblings of Jean's 88): each swept
  **k=2 exhaustively (1 540) and k=3 exhaustively (27 720)** — 18 480 + 332 640
  windows, all irreducible (`sib_88g_j85_*_k[23].json`, `sib00_k2.json`).
  With Jean's own point this is the "**all 13 canonical circuits of families 1–2
  have exactly empty k ≤ 3 shells**" theorem.
- **k=4 on Jean's 88:** 32 677 of the 367 290 windows decided exactly (8.9 %),
  all irreducible, prioritised so that every all-diff quad (2 380) and every
  structural window is covered (`summary_*.json`).
- **Population k=2, first pass:** 10 617 of the 84 989 harvested 88-gate states
  fully swept (16.35 M exact window decisions), all irreducible
  (`pop_scan_run.log`).

---

## 3. `pop_decider/` — the population sweep continued

- **Population k=2 (families 1–2): 51 899 / 84 989 states (61.1 %) fully swept,
  every one irreducible** — 79 924 460 exact window decisions in the log
  (10 617 inherited + 41 282 decided here). Order was most-distant-from-Jean
  first, so the **entire symdiff ≥ 55 band is closed** — the least-covered half
  of the population is the swept half. 33 090 states remain (~2.9 h uncontended,
  resumable). Session log: `pop_scan_phase1.log`.
- **First k=3 theorems on population states:** the 19 most theorem-starved states
  (minimum symdiff 54–56 to *all* 13 canonical 88s, farthest-point diversified)
  closed exhaustively — **19 × 27 720 = 526 680 exact decisions, all
  irreducible_k3** (`sum_*.json`, `k3_progress.jsonl`; 181 of the 200 selected
  states remain).
- **k=4 continuation:** Jean's 88 advanced 32 677 → 32 685 windows;
  **the independent 88@7 got its first 9 exact k=4 windows**, all irreducible
  (`k4_independent88_progress.jsonl`).
- Sanity gate: 12/12 randomly sampled population states rebuilt into full
  circuits and passed the standalone oracle at 88 gates.

---

## 4. `family3_exact/` — the third family decided

- **34 circuits** (the 88@8 anchor + the 25 census representatives + the 8
  portfolio_family3 representatives): **all 1 540 k=2 windows AND all 27 720 k=3
  windows exhaustive for every one of them** = 52 360 + 942 480 = **994 840
  exact decisions, all irreducible**, zero nosol, zero timeouts
  (`sum_<hash>_k2.json`, `sum_<hash>_k3.json`, 34 pairs; `phase1.out`).
- **The whole family at k=2:** **53 902 / 53 902 states (100 %) swept, all
  irreducible_k2** = **83 009 080 exact decisions** in 10 841 s (`f3_scan.out`).
  Unlike families 1–2, this family is **closed** at k=2.
- **k=4 on the anchor:** 20 432 / 367 290 windows (5.6 %), all irreducible,
  highest-priority classes first (`k4_f3.out`).

**Theorem:** any 87 differs from every one of the 53 902 known third-family
states by ≥ 3 masks, and from the anchor + 33 diverse representatives by
≥ 4 masks.

### Canonical-circuit tally (the "47")

k ≤ 3 shells are exhaustively empty for **47 canonical 88-gate circuits**:
Jean's 88 (1) + its 12 syl-move siblings (12) + the third-family anchor and its
33 representatives (34).

**What that population is, stated plainly.** All 47 lie in Jean's-lineage
families: families 1–2 are Jean's circuit and its syl-move siblings, and the
family-3 anchor's seed chain passes through Jean's circuit (§8, and
`../../METHODS.md` §9). The theorem is therefore a **rigidity statement about
that neighbourhood**, not about the 88-gate plateau as a whole — and the one
circuit here that is independent of Jean's lineage, **the project's own 88@7,
is precisely the least-certified**: it is *not* among the 47, its exhaustive
k ≤ 3 sweep was never run, and all it has is 9 exact k=4 windows (§3) and 8 SAT
cone windows (§6). The best-certified shell and the independent shell are
disjoint, and that gap is the honest shape of the negative result.

Population coverage at k=2: **105 801 of the ≈ 139 878 known 88-gate states**
(51 899 of families 1–2 + all 53 902 of family 3).

### Total exact decisions

| producer | exact window decisions |
|---|---|
| `exact_window/` | ~113 000 windows |
| `exact_k4/` | ~16.8 M |
| `pop_decider/` | ~64.1 M |
| `family3_exact/` | ~84.0 M |
| **total, no double counting** | **≈ 165 M** |

---

## 5. `sat_deep/` — windowed SAT on Jean's 88

Sound windowed Fuhs–Schneider–Kamp CNF; any model is a whole realizable circuit,
and every model found is re-verified through the oracle. CaDiCaL in killable
child processes; every window's removal set `R` is logged with its verdict, so
every run resumes.

- **48 windows on Jean's 88 at budget 87 (r = k−1), k = 9–16: 34 UNSAT,
  14 timeout, 0 SAT** (`results.jsonl`; phase logs `phaseA/B/C.log`).
- **Max window size proven UNSAT: k = 16** (the earlier frontier was k = 12).
- Hardness anti-correlates with nB (broken kept masks), not k: every window with
  nB ≥ 19 was decided.
- Pipeline self-test: a planted r=k window came back SAT in 1.6 s and decoded to
  an oracle-VALID 88@7 (`selftest.jsonl`).

## 6. `loose_sat/` — Kissat + symmetry breaking

Two knob-gated, soundness-proved symmetry-breaking layers (SB-P parent
commutativity; SB-F guarded lex on adjacent free slots) plus Kissat 4.0.4.
Clauses are only added, so an UNSAT can never be manufactured; SAT preservation
was checked by 7/7 planted selftests that all decoded to verified 88s
(`selftest.jsonl`). Benchmark: the three slowest CaDiCaL UNSATs (960/1 000/
1 509 s) re-decided in 28/45/106 s — **14–34× faster** (`bench_kissat_pf.jsonl`).

- **Jean's 88, the 14 survivors of §5 re-adjudicated: 10 UNSAT, 4 still
  undecided, 0 SAT** (`results.jsonl`). The two loosest windows (nB = 3 and
  nB = 5) fell. Final standing on Jean's 88 across §5 and §6: **48 windows →
  44 UNSAT, 4 undecided, 0 SAT, frontier k = 16.**
- **This project's independent 88@7, 8 loosest cone windows: 5 UNSAT,
  3 undecided, 0 SAT** (`results_indep.jsonl`) — including an nB = 1 window
  (near-pure synthesis) in 34 s. This is the only SAT coverage the independent
  88 has.
- `results_satdeep.jsonl` is sat-deep's log copied in for comparability
  (same window ids).

## 7. `family3_sat/` — the third family's first SAT attack

Same toolchain as §6, unchanged, on the 88@8 anchor + the 8 portfolio reps.

- **Anchor: 50 cone windows k = 9–16 → 37 UNSAT, 13 undecided, 0 SAT.
  The entire k ≤ 12 regime is UNSAT (28/28); max-k UNSAT frontier = 15**
  (`results_anchor.jsonl`).
- **8 reps: 32 windows → 25 UNSAT, 7 undecided, 0 SAT** (`results_reps.jsonl`).
- Self-test on this anchor: planted k=10 window SAT in 9.1 s, decoded to an
  oracle-VALID 88@8 (`selftest.jsonl`).
- With sb=pf the survivors are no longer the low-nB windows — raw window size is
  the limit now. The dominant remaining gap for **all three families** is the
  fixed slot order in the encoding.

---

## 8. `rho2_symmetric_90s/` — the best known exactly ρ²-symmetric circuits

Not 88-related, but certificate-bearing and load-bearing for the 88@8's
provenance.

- `BEST_90gates_depth9_rho2symmetric.json` (basin 1) and
  `BEST_90gates_depth7_rho2symmetric_basin2.json` (basin 2): two **exactly
  ρ²-symmetric 90-gate** circuits, oracle-VALID at depths 9 and 7, Jaccard 0.463
  apart. They improve the best known exactly-symmetric circuit from 94 to 90.
- `cert90_90g.json`, `cert90_best.json`: orbit-space local-optimality
  certificates — both 90s (and the 91) are machine-certified locally optimal
  under **all** remove-1-orbit and **all 666** remove-2-orbits-add-≤1 moves, with
  zero equal-cost remove-2 swaps. These symmetric basins are extremely rigid; all
  progress came from union crossings.
- **Provenance chain of basin 1** (this is what makes the 88@8 a derived result —
  the logs to check it are all here):
  `union_A88.json` (`"union_of": ["symA_91g.json", "sym88_92g.json"]`) →
  `uA88.log` → 90@9. `symA.log` shows `symA_91g` came from our own ρ²-symmetric
  94; `sym88.log` shows `sym88_92g` came from `IMPORTED_88.json`, i.e. **Jean's
  published 88** (ePrint 2026/1481), symmetrized+peeled to 95 and walked to 92.
  `make_union.py` is the (three-line) union tool.
  Basin 2 (`union_90A.json`) is a further cross of that same 90 with a 91 of our
  own lineage, so it inherits the same derived status.

---

## Where the full logs live

The multi-MB resumable progress logs are not included in this repository. They
are in the raw 2.8 GB campaign archive at the paths below; each frontier here is
resumable from its own progress file.

| what | path |
|---|---|
| population k=2 (families 1–2), 33 090 states left | `campaign_87/agents/pop-decider/work/results_pop/pop_progress.jsonl` |
| population k=3, 181 selected states left | `campaign_87/agents/pop-decider/work/results_popk3/k3_progress.jsonl` |
| family-3 k=2 (closed) | `campaign_87/agents/family3-exact/work/results_f3/f3_progress.jsonl` |
| k=4 on Jean's 88 (334 605 windows left) | `campaign_87/agents/exact-k4/work/results_k4/progress.jsonl` |
| k=4 on the family-3 anchor (346 858 left) | `campaign_87/agents/family3-exact/work/results_k4_f3/progress.jsonl` |
| the 4 + 20 undecided SAT windows | `campaign_87/agents/{loose-sat,family3-sat}/runs/` |

## Re-verification

The 9 circuit JSONs in this folder (the two ρ²-symmetric 90s, the orbit-space
certificate circuits, the union seeds and their ancestors) were re-checked with
`../../verify_circuit.py`: **all VALID**, at the gate counts and depths stated
in their filenames.
