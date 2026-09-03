# Banked solver logs — excerpts

The three expensive levels (k = 12, 13, 14) were **not** re-run for this pack.
Re-running them costs hours to weeks of a core; see the cost column in
`../STATEMENT.md`. What follows are the verbatim lines the campaign banked when
it decided them, with two edits and no others: an absolute filesystem path was
replaced by a relative one, and an internal lane label was dropped. Every
number is untouched.

Each log is append-only JSON Lines. `core_seconds` is `time.monotonic`
end-to-start around one solver call in one process on one core.

---

## L1 — k = 14, the decisive level (verdict UNSAT)

Source: the monolithic solver portfolio, one process and one core per solver, on
the same formula as `cnf/k14_joint_W3U4.cnf`.

**The two terminal lines ship in this directory, verbatim:**
`mono_14_kissat404.log` and `mono_14_cadical300.log`. They are the raw
append-only terminal records, copied byte-for-byte from the campaign's log
directory — no edit at all, including the internal run label `"lane": "CUBE"`
(the campaign's name for the monolithic-solver route; it carries no
mathematical content and is kept only so the shipped files are byte-identical
to the originals). The trailing `MONO TERMINAL LINE` marker is the writer's
end-of-run sentinel.

```json
{"kind": "mono_level", "lane": "CUBE", "k": 14, "status": "UNSAT", "core_seconds": 356321.63, "cores": 1, "solver": "kissat404"}
{"kind": "mono_level", "lane": "CUBE", "k": 14, "status": "UNSAT", "core_seconds": 468159.51, "cores": 1, "solver": "cadical300"}
```

kissat 4.0.4: 356 321.63 core-seconds ≈ **99.0 core-hours**. Decided 2026-09-01.
CaDiCaL 3.0.0: 468 159.51 core-seconds ≈ **130.0 core-hours**. Landed
2026-09-01, independently, on the same hash-pinned instance.

Two independent complete solver engines therefore returned UNSAT on the same
formula. Only one is needed for the verdict — one complete solver returning
UNSAT decides the level — so the second is redundancy against an engine bug,
not against an encoding bug: **both solved the same CNF, so a wrong encoding
would still be UNSAT for free.** What is still open is a cross-*encoding*
reproduction at k = 14 (levels 9–13 have one; see §L3) and a DRAT refutation at
k = 14 (none exists; the pack ships refutations only for k = 9 and k = 10, plus the k = 6 control).

*History of this entry.* When the pack was first assembled this section read:
“Three further complete solvers (CaDiCaL 1.9.5, CaDiCaL 3.0.0, Glucose 4.2)
were still running the identical formula … each is an independent engine-level
confirmation **if and when it lands**.” One of the three landed — CaDiCaL 3.0.0,
2026-09-01, the line above. CaDiCaL 1.9.5 and Glucose 4.2 were still running
when the campaign ended and are recorded here as never having landed. Section
updated 2026-09-03.

## L2 — k = 11 and k = 12, monolithic

Same code path, same encoder, one core each.

```json
{"kind": "mono_level", "k": 11, "status": "UNSAT", "core_seconds": 218.45, "cores": 1}
{"kind": "mono_level", "k": 12, "status": "UNSAT", "core_seconds": 5761.73, "cores": 1}
```

## L3 — the second encoding's ladder, k = 9 … 13

A different CNF for the same mathematical question, written by a different
generator, solved on 8 cores. This is the cross-check described in
`../STATEMENT.md` §5.

```json
{"k": 9,  "result": "UNSAT", "seconds": 23.68}
{"k": 10, "result": "UNSAT", "seconds": 123.82}
{"k": 11, "result": "UNSAT", "seconds": 785.29}
{"k": 12, "result": "UNSAT", "seconds": 5202.15}
{"k": 13, "result": "UNSAT", "seconds": 105083.40}
```

k = 13 alone is 105 083.4 s of 8-core wall ≈ **233.5 core-hours**. It is the
reason k = 13 is inherited rather than re-run anywhere.

## L4 — the partition check the cube route ran before dispatching anything

The cube route splits the level on gate 0's input pair. Before a single cube is
solved it machine-checks, on the real CNF, that the 528 cubes partition the
models exactly — including by *asking the solver* that forcing two cubes at once
is UNSAT and that forcing none is UNSAT.

```json
{"tag": "joint_W3U4", "k": 14, "m": 33, "r": 16, "cubes": 528, "lb": 9,
 "control": {"greedy_ub": 16, "verified": true, "secs": 1.73},
 "partition": {"n_cubes": 528, "n_cubes_is_C_m_2": true,
   "pairs_are_all_input_pairs": true, "pairs_in_key_order": true,
   "gate0_pairs_use_only_inputs": true, "at_least_one_clause_present": true,
   "two_cubes_at_once_UNSAT": true, "no_cube_at_all_UNSAT": true,
   "exactly_one_cube_per_model": true}}
```

The cube sweep at k = 14 reached 90 of 528 cubes decided, all UNSAT, none SAT,
and was reported as **UNDECIDED** — never as a refutation:

```json
{"kind": "cube_level", "k": 14, "n_cubes": 528, "unsat_cubes": 90,
 "sat_cubes": 0, "open_cubes": 438, "coverage": "90/528",
 "status": "UNDECIDED",
 "claim": "90 of 528 cubes decided UNSAT; 438 still open -- UNDECIDED, NOT a refutation"}
```

The verdict in L1 came from the monolithic route, which is a complete decision
of the level. The partial sweep is consistent with it and adds nothing to it.

## L5 — the SAT branch, rehearsed on a real witness before it was needed

The 15-gate program for the merged block is constructive: run the first block's
8-gate program, then the second's 7-gate program. That witness was pushed all
the way through the circuit generator and the standalone oracle, so the path
that must fire on a SAT is tested rather than trusted.

```json
{"witness_gates": 15, "verify_slp": true, "why": "ok",
 "prov": {"source": "replay bound: block A then block B", "parts": {"A": 8, "B": 7}}}
```

```json
{"kind": "sat_compile", "witness_gates": 15,
 "handover": {"block_free": 33, "witness_free": 33, "supply_superset": true,
              "targets_match": true},
 "model_price": 88, "emitted_gates": 88, "depth": 7, "inprocess_built": 32,
 "verify_rc": [0, 0], "verify_tail": ["VERDICT: VALID MixColumns circuit"],
 "verified_twice": true, "circuit": "mixcolumns_88gates_depth7.json"}
```

That circuit ships in this pack as
`positive_control/mixcolumns_88gates_depth7.json`, and `RUN.md` step 6 re-runs
the oracle on it. It is what makes the arithmetic **88 − 15 + 14 = 87**
end-to-end rather than a promise: had k = 14 come back SAT, this path would have
emitted an 87.
