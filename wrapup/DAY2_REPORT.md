# Day-2 autonomous session — final report

Session: 2026-08-29 11:00 → 2026-08-30 16:20 (wall). **Real awake time was far
shorter: the host suspended repeatedly** — uptime advanced ~90 minutes across
the whole window. Everything below accounts for that. Hard rule held: **nothing
was pushed, sent, or published**; the k=14 solvers ran (and slept) untouched —
still alive, no SAT hit, no STOP.

## New science (all banked, all verified)

1. **A new negative certificate, stronger than B=56** — every single-mask
   deletion of the 498 atlas 88s (27,888 candidate 87-mask sets, each still
   containing all 32 targets) is **non-realisable even with unrestricted
   rewiring**. By-product: the deletion barrier is *topological, not local*
   (39% pass the local test, 0% the global one).
   → atlas/corner/ANALYSIS_20260829.md §7. A corpus-wide extension to all
   1.58M distinct 88s is in flight (wrapup/day2/deletion_cert/).
2. **N_depth3 ≥ 81** — the depth-3 gate floor rose from the certified 80
   (MIP dual bound 49.0, banked, wrapup/day2/runs/mip3/mip3_result_L1.json).
3. **Fan-out ≥ 8 is unrealisable at 88** — exhaustive CP-SAT over all build
   orders per mask set; record 88s max at 3–5 despite potential-8 signals.
   "Max fan-out ≤ 5" is structural. → experiments/e_upstream/RESULT.md (C4).
4. **An 88's wiring is forced by its mask set** (99.86% of masks have exactly
   one legal parent pair) — the planned wiring-null control is degenerate, and
   the forcedness is itself a why-88 fact. → wrapup/day2/STEWARD.md.
5. **The skeleton record moved twice**: the atlas 498's l3=64 anchors verified,
   then beaten by a first-ever census sweep — **l3=57** (9 anchors extracted,
   9/9 VALID). Fourth refuted atlas claim found (envelope shoulder at 88, not
   89). **The two proposed 87 routes (low-l3 vs low-|A*|) are anti-aligned,
   r=−0.854** — a search satisfying both aims where no 88 lives.
6. **The out-of-vocabulary 89 is real and load-bearing** (verified, irreducible
   to 2 deletions; leaving the 88s' shared dictionary costs ≤ 1 gate). Three of
   its five feature classes closed for ~10 min of CPU. The decisive 89→88
   pinned descent (asks for an 88, not an 87) is running — banks any hit
   instantly (wrapup/day2/e_upstream/seed89_ledger.jsonl).
7. **Negative reproductions, honestly banked**: G_int(3) ≥ 92 was NOT purchased
   (UNKNOWN; and G_int(2)=64 failed to reproduce a third time — stays
   UNPROVEN-AS-STATED). The d3-ladder lead was killed by pricing (route
   ceiling < certified 80). MB27B373=13 (harvested, not new compute) closes
   another 87 branch.

## Deliverables

- **wrapup/CASE_FOR_88.md** — the master evidence dossier (1,799 lines, 81
  cited items: 19 theorems / 41 certificates / 21 measurements), including
  today's results and the honest counter-evidence. The skeleton of a possible
  ePrint note.
- **wrapup/METHOD_CATALOG.md — now audited**: 62 entries verified against
  primary sources, 24 defects found and FIXED in place (changelog appended);
  9 thin entries completed; generality labels corrected (audit:
  wrapup/day2/CATALOG_AUDIT.md).
- **Phase 2 is ready to start** (wrapup/phase2/): InvMixColumns spec derived
  with three passing controls; the oracle and B-tripwire ported to
  arbitrary-matrix form and control-tested; day-0 baselines (naive 440, greedy
  164@9, M³ 264); the inverse's sector structure derived (four-tap chain, same
  W); prior-art dossier (published best 92 — one paper ever; implied 91;
  **depth frontier completely unclaimed; no lower bounds; no AI-search
  attempts**); and PHASE2_PLAN.md (first target: the depth frontier; then the
  virgin lower-bound side).
- **11 harvest addenda** beside stale RESULT.md files (wrapup/day2/HARVEST.md),
  incl. the measured |M|=23 plateau cliff and the corrected rank-cut story.
- **Both repos staged on local branches** — `repo-update-2026-08`
  (slp-plateau-search) and `v3.2.0-staging` (aes_mc_records): the README
  rewrites, the 92→91@4 fix, the new 91@4 circuit, all tests run. The staging
  agent may still be finishing when you read this — see wrapup/day2/STAGING.md
  for its record. **Nothing pushed; main untouched in both repos.** Approving
  tomorrow = merge + push + send the Jean email (kept as a local working draft
  only — `wrapup/drafts/` is deliberately not part of the public set, since it
  holds correspondence with a named third party; the draft needs the current
  k=14 cube count refreshed before sending).

## Operational findings

- **Solver wall-limits are not suspend-safe on this box**: HiGHS/CP-SAT budgets
  burned 12h of "time" on ~20 min of awake compute while the host slept. Any
  future long run needs a monotonic/CPU-time watchdog. NOTE: the live
  cube16 sweep's --tlim may have the same exposure — worth checking before
  relying on its 3-day budget.
- The wall clock jumped forward hours during suspends (known hazard, forward
  direction confirmed). All my runs bank continuously, so nothing was lost.

## Still running when this report was written

- k=14: 4 monolithic solvers + cube sweep (87/528 UNSAT, 0 SAT at last tally).
- seed89 89→88 descent (R1) and the fan-out survey (R2) — self-limiting,
  banked, kill instructions in wrapup/day2/runs/RUNS.md.
- The corpus-wide deletion certificate and the repo-staging agent (their
  outputs land in wrapup/day2/deletion_cert/ and wrapup/day2/STAGING.md).

## Post-report update: staging finished

Both branches are fully staged and tested (wrapup/day2/STAGING.md):
`repo-update-2026-08` — 4 commits, 34/34 tests, CI green;
`v3.2.0-staging` — 5 commits, verify 12/12, pytest 12/12. Nothing pushed.

**One decision for review before merging:** on the slp branch the old 92@4
circuit was REMOVED from evidence/ (per CHANGES.md, "91 in place of 92"),
while the records repo retains its superseded 92 beside the new 91. If you
prefer keep-beside in both (the records-repo convention), it is a one-commit
amend on the branch. Also still open: the records PRIOR_ART literature cutoff
refresh and the untagged v2/v3 DOI history.

## Post-report update 2: the corpus-wide deletion certificate CLOSED

**Verdict: negative, at 100% coverage.** All 88,228,896 single-gate deletions
across ALL 1,575,516 distinct verified 88s are non-realisable, even with
unrestricted rewiring (35,323,820 pass the local filter; 0 pass globally).
Coverage proven set-identical to the corpus index (0 symmetric difference).
Controls: positive control fired exactly as planted; the 498-circuit pilot
reproduced to the digit; Python-vs-C agreement on 300 corpus records.
This is now the strongest deletion certificate the project holds — "no 87 by
one-gate deletion from any distinct verified 88 on this machine" — and row C3
of CASE_FOR_88.md has been repriced accordingly. By-product: B=56 bookkeeping
re-confirmed set-wise over the whole corpus (deletions_per_set = 56.000000).
Full record: wrapup/day2/deletion_cert/CERT.md. The 712 MB of regenerable
stream files (masks.bin, canon.tsv) are kept on disk, not committed.

## Post-report update 3: R1 and R2 closed — session fully quiescent

- **R1 (seed89, the 89→88 pinned descent): partial negative.** No 88 reached,
  pin alive, in 0.44 of the budgeted ~1.2 core-hours before the operator stop
  (host suspends meant the monotonic budget never expired — a monotonic
  deadline gives interruptibility, not a wall-clock guarantee; lesson banked).
  This is a search upper bound from one-third of one seed's budget, NOT an
  answer. The priced next step stands: ~20 core-hours across all 20
  non-appendix floors (experiments/e_upstream/RESULT.md §8).
- **R2 (fan-out widening): verdict NO on a real base.** 142 mask sets total
  (103 stratified corpus + 39 exact), max fan-out 3-6, never 8 — even though
  83 of the 103 carry signals with potential >= 8. Acyclicity, not the mask
  alphabet, caps fan-out.
- All launch records in wrapup/day2/runs/RUNS.md are CLOSED. The only
  processes alive in this tree are the k=14 solvers.

## Post-report update 4 (2026-09-01): k=14 is DECIDED — UNSAT

The one open machine decision this report left running has landed.

- **`k = 14` on the merged `W3|U4` dim-16 block: UNSAT**, decided 2026-09-01 by
  the monolithic route — kissat-4.0.4 completed the whole instance in one
  process, **356,321.63 core-seconds (~99 core-hours, 1 core)**, well under the
  653-1113 core-hour forecast. Log: `fleet11/laneCUBE/logs/mono_14_kissat404.log`
  (`{"kind": "mono_level", "k": 14, "status": "UNSAT"}`). Authoritative
  statement: `fleet11/laneCUBE/RESULT.md` §7.1.
- **Consequence.** The ladder `k = 9..14` is complete, all UNSAT; the bracket
  {14, 15} collapses. **merged(W3 u U4) = 15 exactly = the split total, so
  merging buys nothing**, and **no 87 exists that shares the block structure of
  every known 88**.
- **Scope, unchanged.** This is NOT a proof that no 87 exists. An 87 outside the
  standard block decomposition is not excluded, and `56 <= L(M) <= 88` stands.
- **Confirmation status.** The 528-cube sweep was never finished and is not the
  basis of the verdict: it stood at 90/528 decided, all UNSAT, 0 SAT —
  consistent. The three other monolithic engines (`slp_opt` CDCL, cadical-3.0.0,
  glucose-4.2, same CNF) were still running as engine-level confirmations. The
  fully independent cross-encoding check (fleet8's `dslp` CNF at k = 14) has not
  been run; priced at roughly 10x the k = 13 cost, and optional.
- Body of this report above is unedited; the "still running" tallies in it are
  correct as of the date they were written.
