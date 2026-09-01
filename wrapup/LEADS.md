# LEADS — merged, deduplicated, ranked register

Compiled 2026-08-29 from the ten wave-1 slice reports in `wrapup/reports/`.
All paths are relative to the repo root `/home/joebachir20/xor_ui/slp-plateau-search/`
unless prefixed `aes_mc_records/` (= `~/xor_ui/aes_mc_records`).

## What this file is, and is not

**The search phase is OVER.** The user has ended it. This register exists for two
purposes only:

1. material for a public repo section addressed **to future 87-hunters** — "here is
   what we did not finish, and what we would look at first";
2. the **user's own discretion**, if any compute is ever spent on this problem again.

It is **not a work queue**, and nothing in it is scheduled. No entry below has been
run, and no entry should be read as a commitment.

**Standing caveat that outranks every SEARCH lead here** (`campaign_87` L1,
`root_infra` L1, commit `23d80d7`): the project's own controls price its
neighbourhood negatives at likelihood-ratio ≈ 1.00. The exact decider returns
"irreducible" on 97@3, 94@4, 92@5, 91@5, 90@5, 89@9 and Jean's 88@7 alike (12,241
exhaustive k=2 windows, 8,400 sampled k=3, zero reducible), while the measured
distance from a circuit to a known better one is **median 42 masks, min 3**, against
a certified radius of 3. *A negative at radius ≤ 4 carries essentially no information
about whether an 87 exists.* Leads that only extend such radii are ranked low here
for exactly that reason.

## Intake

| | count |
|---|---|
| Numbered lead items across the 10 reports | **140** |
| Merged as duplicates of another lead | 14 |
| Closed by later work → Appendix A | 27 |
| Reclassified as stale-figure fixes → `CORRECTIONS.md` (56 entries) | 31 |
| Reclassified as evidence (§B) or guardrails (§C) | 18 |
| **Surviving actionable leads, ranked below** | **54** |

(The categories overlap: a lane result that *landed* after its write-up is both a closure
and a correction, and is listed in both places. The four such items are lane B's `R01 ≥ 15`,
lane F4's `W3_noshare`, lane D's basin sweeps, and the frontier-exact ledgers.)

## Labels

- **SEARCH** — could yield an 87. **PROOF** — evidence toward 88-optimality.
  **BOTH** — a positive answer is an 87, a negative is a proof-side fact.
- Confidence is **the source report's own label**, carried verbatim:
  VERIFIED(-IN-LOG) / PLAUSIBLE / SMELL.
- Cost is **as stated in the source report**; `UNKNOWN` where the report gives none.
  Costs are not re-estimated here.
- Rank = (decisiveness for 87-or-optimality) × (cheapness). Ties broken toward
  "a machine-checkable verdict" over "a measurement".

---

# A. RANKED LEADS

## Tier 1 — decisive and cheap (1–12)

### 1. `m_S7W_B27_c7` at k = 11 — the one row that closes a flag
**PROOF (SAT would be SEARCH). VERIFIED-IN-LOG.**
`fleet5/laneMENU` proves `price ≥ 87` over 1.41e26 currency menus with nine of ten
bounds exactly tight, and localises the single loose gate at the hub. The deciding
instrument reached k = 6,7,8,9,10 **all exhaustively UNSAT** (37.1 / 57.1 / 208.1 /
1144.8 / 13140.2 s), proving `bound ≥ 11`. The ledger row reads
`status: stopped_by_operator, lower_bound: 11, lb_kind: bracket, predicted: 12` — it
was **stopped by the operator, not refuted**.
*Why it matters:* **k = 11 UNSAT ⇒ merged = 12 ⇒ the all-menu bound rises 87 → 88 and
flag F1 closes outright.** k = 11 SAT ⇒ the loose hub gate is real.
*Cost:* ~1.5e5 s against ~3.3e4 s already spent; the lane notes the asymmetry — SAT
is found far faster than UNSAT is proved, so silence favours the UNSAT branch.
*Files:* `fleet5/laneMENU/inst/m_S7W_B27_c7_3b1c8975975d.json`,
`fleet5/laneMENU/code/queue_merge.py`, lane ledger.
*Source:* `fleet5_8` L3.

### 2. The 28 order-free fence windows **at budget 87** that never ran
**BOTH. VERIFIED-IN-LOG (re-verified independently in the slice session).**
`wave5/fence_sat/STATUS_NOVEL.md` records an audit finding that all 16 decided
windows in the novel-89 queue sat at total budget **88**, and that the 28 budget-**87**
windows — *"the only ones in this queue whose SAT would be a world record"* — had
never run. It set `prio = -1` so they run first on resume; campaign compute stopped
five days later. Re-verified: `totals Counter({88: 210, 87: 28})`, budget-87 windows
with any result: **0**. `windows_novel.jsonl` mtime Aug 6 14:18 (the fix);
`results_novel.jsonl` mtime Aug 6 12:20 — *before* the fix, never written again.
*Why it matters:* **fence is the only certificate class in the project with no
slot-order caveat.** The ideation round rated it the top unrun lead.
*Cost:* resume is idempotent — `bash wave5/fence_sat/launch_novel.sh <procs>`. k,n on
the 28: (16,14) (18,16) (20,18) (22,20); 7 novel-region anchors.
*Files:* `campaign_87/wave5_2026-08-04/fence_sat/{STATUS_NOVEL.md,launch_novel.sh,runs/windows_novel.jsonl,runs/results_novel.jsonl}`.
*Source:* `campaign_87` L3.

### 3. 498 never-analysed distinct 88-gate mask-sets in `atlas/corner/out`
**BOTH. VERIFIED (measured and oracle-checked in the slice session).**
`ideas_strange_corners.md` §7 lists three job files (`hunt.jobs` 160 walks, `sh2.jobs`
76, `fib.jobs` 32) as "still running at write-up, results not included"; no successor
exists anywhere in the repo. The output was never analysed. Measured now: **498
distinct 88-gate mask-sets**, socle-skeleton `l3` running **continuously 64 → 79**
(histogram 64:2 65:8 66:17 67:7 68:24 69:36 70:16 71:6 72:12 73:50 74:85 75:42 76:59
77:65 78:57 79:12), and **0 of the 498 equals any of the 54 distinct 88s under
`evidence/`**. 13 were converted and run through `verify_circuit.py`: **13/13 VALID**.
*Why it matters:* (a) it **refutes three published atlas claims** — the `l3 ≥ 67`
floor, the "empty band 69–72", the "real 2-gate ridge" (→ `CORRECTIONS.md` C-15);
(b) `phase2_tower.md` argues an 87 should be sought skeleton-anchored at **low** `l3`,
and the lowest known 88 was 67 — there are now verified 88s at **64**, three gates
further into the corner where the tower argument places an 87. Anchoring a
skeleton-anchored SAT at `l3 = 64` is strictly cheaper and strictly closer to the
`bp_L3_51.json` witness.
*Cost:* converting all 498 and verifying = minutes; socle-plane envelope recompute =
seconds. Anchored SAT: UNKNOWN.
*Files:* `atlas/corner/out/*.plat`, `atlas/corner/socle.py::l3_of`,
`atlas/thinktank/{ideas_strange_corners.md,phase2_tower.md,third_frame.md,audit_inference.md}`.
*Source:* `atlas_misc` L1. Confidence VERIFIED for the circuits and `l3` values,
PLAUSIBLE for the 87 relevance.

### 4. Three unfinished routes to "every 87-gate MixColumns circuit has depth ≥ 4"
**PROOF. VERIFIED-IN-LOG.**
The certified depth-3 bound stands at `N_depth3 ≥ 80`. Reaching rung K = 55 on route
(c) gives `N_depth3 ≥ 88` — i.e. a **publishable theorem** that no 87 is shallow.
Three routes, none refuted, all abandoned:
(a) `wave6/lower_bound/THEOREM.md` §6 proves the LP saturated at 47.598 across cut
levels 1–4; only branches E ∈ {19,20} can reach 48 and both sit at LP value exactly
48.0, so everything above 80 is **integer** reasoning. The prepared next command
(`node_probe.py 19 29 0 29`) was never run (`ls logs/ | grep node` → only
`node_19_29.log`).
(b) The **killed** capped MIP already banked a better bound: `logs/mip3_L1.log` ends
mid-run at 599.5 s with `BestBound 48.44982378` ⇒ **N_depth3 ≥ 81**, still climbing;
the uncapped run reached 49.478 ⇒ **≥ 82**. `mip3_result_L1.json`, which THEOREM.md
tells the reader to consult, **does not exist**. Solver-claim class, but the
certificate machinery to convert them exists.
(c) The orphaned route: `d3_model/d3bound.py` lifts exact MILP solutions on target
subsets into global bounds and, in **17 minutes on one core**, climbed
32 → 52 → 53 → 59 → **63**, every rung `PROVEN OPTIMAL`, rungs getting *better*, each
solving in ≤ 155 s. `logs/d3bound.log` ends at k=10 with no k=12 attempt and no note.
The campaign's own correction chain reads 57 → 66 → 80 and **never mentions 63**.
*Cost:* (c) is minutes per rung at the point of abandonment; scaling to K = 55 is
UNKNOWN.
*Files:* `campaign_87/wave6_2026-08-11/lower_bound/{THEOREM.md,logs/mip3_L1.log,logs/mip3_L1_uncapped.log}`,
`campaign_87/d3_model/{d3bound.py,logs/d3bound.log}`.
*Source:* `campaign_87` L4.

### 5. Re-certify `G_int(3) ≥ 92` — one CP-SAT run
**PROOF. VERIFIED-IN-LOG.**
`e17_pure/DOSSIER.md` §7.2/§9.5: the value is *"a solver's best objective bound"*,
bracket `[92,94]`, never re-certified. Re-certifying it **as an infeasibility at
`obj ≤ 91`** is *"the highest value-per-hour item on the board."* If it fails,
`kappa ≥ 3` at `n ≤ 87`, `|A*| ≥ 3` and the §6.2 conditional chain all die.
Companion SMELL: `G_int(2) = 64` has **two failed independent reproduction attempts
against one log** (§7.1) — an inherited constant that laneY's headline recommendation
depends on exactly.
*Ceiling that must travel with it* (`fleet5_8` L6): `G_int(3) ≥ 92` moves the
dichotomy from `kappa ≥ 16` to `kappa ≥ 18`; `≥ 94` gives 19; **no larger value is
reachable** — laneUNCOND's ceiling applies verbatim, so the route still dies at
`kappa ≥ 22`, below the records' own `kappa = 18..28`. Fund it knowing that.
*Cost:* one CP-SAT run.
*Files:* `experiments/e17_pure/DOSSIER.md` §7.1–7.2, §9.5;
`fleet6/laneTOOL2` §7.4; `fleet7/laneUNCOND` §7.4.
*Source:* `experiments_late` L1 + `fleet5_8` L6.

### 6. Run the Lemma-R tripwire over the whole 88 corpus — ~80 CPU-minutes
**SEARCH. VERIFIED-IN-LOG.**
`laneDELTA/RESULT.md` §8b sub-gap 1: the tripwire ran on 1,200 + 600 of **18,355**
corpus 88s (two non-nested samples) = 6.5 % coverage, returning 0 hits on valid 88s
and 66 hits on non-88s. The private-operand population it scans is *strictly larger*
than lane536's site frame, so the corpus-wide version is genuinely new coverage, not
a repeat. **One CPU-hour of free, always-on 87 detection nobody bought.**
*Cost:* ~80 CPU-minutes.
*Files:* `experiments/e17_pure/laneDELTA/RESULT.md` §8b; lane code + `witness_nonsample.log`.
*Source:* `experiments_late` L14.

### 7. Jean's unpublished foreign-lineage 88s through the B = 56 tripwire
**SEARCH. VERIFIED-IN-LOG.**
Every local anchor came from one solver fleet (e14's own selection-bias caveat). Jean
(letter 2026-08-10) holds **more unpublished 88s from a genuinely foreign lineage**
(his method: "AI, most specifically models from OpenAI under codex"), and his stated
intuition is that 88 is the floor. Each foreign 88 is a free shot at an 87 through the
B = 56 tripwire — *any valid irreducible 88 with B ≠ 56 yields an 87 by deletion* —
which has fired **zero** times on 17,283/17,283 local distinct 88s. **B = 56 holding
on foreign circuits would be real new evidence for the floor; B ≠ 56 would be an 87.**
*Gating item:* the follow-up email is planned *after* the public repos are updated
(~2026-08-30), and `aes_mc_records` is stale (→ `CORRECTIONS.md` C-02).
*Cost:* minutes per circuit once the circuits are in hand.
*Files:* `experiments/e15_campaign3/RESULT.md` (tripwire theorem + run A),
`aes_mc_records/` (the gating update).
*Source:* `records_repo` L7 (+ project memory: Jean correspondence).

### 8. The 16 unclaimed `rc2_floor` jobs on glue-conditioned alphabets
**BOTH. VERIFIED-IN-LOG.**
`wave6/modular_syl/` established, as a theorem rather than a hope, that the
glue-conditioned mask population (**11,778 masks, generated without ever reading a
circuit**) contains **all 88 gate masks of three separate record 88s** and 87/88 of
two more. Since a record's gate-mask set is a closed feasible set,
`floor(population) ≤ 88` follows. The remaining gap is fully localised — module search
0 gates, decomposition 0, coverage 0, glue ≤ 4 — to **selection under the RC2 solver's
~280-mask alphabet cap**. The direct test is 16 `rc2_floor` jobs on the conditioned
alphabets (|A| = 299 … 11,778). All 16 sit **unclaimed** in the queue; the rented pod
ran the low-priority `A7b_B` batch instead and then died.
*Why it matters:* this is *"the cleanest statement anywhere in the slice that 88 is a
**solver-capacity artifact of the instruments** rather than a measured optimum."*
*Cost:* one RC2 call per alphabet.
*Files:* `campaign_87/wave6_2026-08-11/pod_jobs/queue/` (16 files, all `A7b_R_*`),
`campaign_87/wave6_2026-08-11/modular_syl/`.
*Source:* `campaign_87` L10.

### 9. A possible **90 @ depth 4**, one capped SAT call away
**Frontier move (not an 87). VERIFIED-IN-LOG that it was left in flight.**
`fleet4/laneDEPTH` §3.2/§3.3 prices the depth-4 rung at the 88@5 cell as
`79 + W3(D=4) ≥ 90`, **exactly 90 iff `W3(D=4) ≤ 11`**. Collected from the logs: both
runs timed out at 10 h — `DECIDE_W3_D4_le11` (no bound banked) and
`..._le11_c2` (`lower_bound_proven = 11`; k=6 UNSAT 39.7 s, k=7 66.3, k=8 250.8,
k=9 1243.3, k=10 7973.7). So the honest state is `W3(D=4) ≥ 11` machine-checked, rung
`≥ 90`, endpoint **UNDECIDED — never a refutation**. The question is *exactly one
capped SAT call* (`max_gates = 11`, so UNSAT is a machine-checked negative rather than
a timeout), and the payoff is a repo frontier point. Corroborating partial bounds sit
in fleet8's ledger: `W3` at D=3 exhaustively UNSAT below k=11, `U1` at D=4 below k=9.
*Counter-prior:* the lane's positive-only repair probe shifts toward 12 (three targets
each needing to lose a level), which would leave the frontier at 91; and 49
depth-capped restarts produced `{(91,4): 40, (92,4): 9}`, 0 at ≤ 90.
*Files:* `fleet4/laneDEPTH/{RESULT.md,logs/queue4.out,results/dcache.jsonl}`,
`fleet8/unified/ledger.jsonl`, `experiments/e4_depth/RESULT.md`.
*Source:* `fleet1_4` L5 + `records_repo` L2 + `fleet5_8` L5 (same lead, three reports).

### 10. The `{4,7}` profile region — "the branch nothing has pressure on"
**SEARCH. VERIFIED-IN-LOG.**
`e17_pure/DOSSIER.md` §4.5 branch 3 and §9.5: **63 of 475 admissible pairs**. If an 87
exists with `|A*| = 2` it has **exactly two cancelling gates and eighty-five clean
ones** — *"nothing like any of the eleven wired circuits on disk (`kappa = 9..28`)"* —
and one of the twelve weight-7 MixColumns rows is produced by a cancelling gate.
*Why it matters:* a concrete, fully-specified, **never-searched target region** for an
adversarial search, and it is exactly the shape no instrument in the project has ever
aimed at. The slice calls it *"the sharpest positive lead"* it holds.
*Cost:* UNKNOWN (no instrument exists for it).
*Files:* `experiments/e17_pure/DOSSIER.md` §4.5, §9.5.
*Source:* `experiments_late` L7.

### 11. The CF MILP has already seen ≥ 93 and nobody extracted it
**PROOF. VERIFIED-IN-LOG (SMELL on the extraction).**
`understanding/u6_spec87/cfree.log`: the exact CF MILP (HiGHS, 14,456 binaries)
reached **dual bound 92.63 at 790 s / 2,038 nodes and was still running when
stopped**. The refereed certificate gives 92. **So the relaxation has already proved
≥ 93 and it was never banked.** With V2's oracle-verified 102 upper end, the live
bracket is `[93 on HiGHS trust, 102 verified]`, gap 9, and `PROGRAM_STATE.md` names
closing the CF MILP as **the only live lower-bound route**.
*Cautionary companion, same lane:* U3 declared the cancellation-free route dead at
`CF ≥ 47 < 51`; U6 revived the same object with target-dependent prices and column
constraints and got **92**. *The difference between 47 and 92 was the choice of
relaxation, not the object* — a standing warning to re-ask every route this project
declared dead on one weak relaxation.
*Cost:* re-run to termination; UNKNOWN.
*Files:* `beat88/understanding/u6_spec87/cfree.log`, `.../PROGRAM_STATE.md`.
*Source:* `beat88` U-9 (+ `beat88` L15 for the bracket framing).

### 12. The reducible-88 layer — where an 87 would actually certify, and nothing searched it
**PROOF-scoping (decides what every negative in the project means). VERIFIED-IN-LOG.**
CANON's **U1-17 is labelled "Load-bearing"**: the equivalence "87 ⟺ some 88-mask set's
core admits a `k−1` completion" runs through **reducible** 88-mask sets, and every
corpus in this repo holds only **irreducible** ones. Therefore *"no irreducible 88
family admits a `k−1` completion" would NOT prove `C_AES ≥ 88`.* U7 §4 records that
the reducible-88 layer was **killed before staffing as circular**.
*Why it matters:* if an 87 exists, U1-16 says it certifies as a `k−1` completion of a
**reducible** 88 — and **every negative in both halves of the beat88 slice is scoped
away from exactly that region.** Any public claim about coverage must say this.
*Cost:* UNKNOWN — no corpus of reducible 88s exists.
*Files:* `beat88/understanding/CANON.md` U1-16/U1-17, `.../u7_representation/` §4.
*Source:* `beat88` U-11.

---

## Tier 2 — strong, with a real price or a real caveat (13–32)

### 13. The instrument cap that matters is 3 → 4 planes, and 31,016 four-plane 88s were already on disk
**BOTH. VERIFIED-IN-LOG for the measurements, PLAUSIBLE for the inference.**
Wave 6's plane-cage discriminator measured that ≤3-bit-plane confinement — assumed by
every campaign instrument — is **not a property of optima**: a ≥4-plane gate is **free
at the plateau** (88 gates on 120/120 matched descents, price 0.00) while an equally
rare ≤3-plane quota costs ≈ +0.87 gates. **31,016 distinct oracle-verified 88-gate
circuits containing a 4-plane gate were already on this project's disk** across 13 run
files from four independent tracks, unseen. Meanwhile `nplanes ≤ 3` is 195,420 of 2³²
masks = **0.0045 % of the space**, and the SYL pattern class, the skeleton-pool cross
generator and the plane-local/cross decomposition all live inside it.
*Honest counterweight, on record:* the ≥5-plane tier is not merely unused but
**unbuildable** (buildable rate 0.0000 at p = 5..8; 0 of 7,755 offered masks ever
selected across 89,003 floors), and the down-1 question was asked 626 times on the
high-plane family with UNSAT every time it answered.
*The reconciliation nobody wrote:* **the cap that matters is 3 → 4, not 4 → 5, and no
≤3-plane instrument was ever re-run with a 4-plane alphabet.** Concrete and cheap.
*Source:* `campaign_87` L2 (+ L9 for the ineffective patch, → `CORRECTIONS.md` C-33).

### 14. The 99 lateral 88s that were generated and never compiled
**SEARCH (census) + a headline correction. VERIFIED-IN-LOG.**
Lane D's basin sweeps ran to completion after its RESULT.md was written:
`basin_88at5fs.jsonl` and `basin_88at6.jsonl`, 27,720 rows each — **42 HIT-3 escapes
in the 88@5fs basin, 57 in 88@6, 99 in total**, against the 1 the write-up knows about.
**99 oracle-VALID-shaped 88-gate mask sets exist as data and have never been compiled,
verified, deduplicated, or checked against the 88 census.** The one that *was* compiled
verified VALID first time (re-verified in the slice session). Free by-product:
**zero completions at `k ≤ 2` across all 55,440 triples** — a stronger no-87 statement
than the write-up claims.
*Cost:* compile-and-verify is cheap; the report calls it the largest block of
generated-but-unexamined data in the slice.
*Files:* `fleet1/laneD_completions/{basin_88at5fs.jsonl,basin_88at6.jsonl,RESULT.md}`.
*Source:* `fleet1_4` L2. (Headline correction → `CORRECTIONS.md` C-18.)

### 15. 182 of 204 families undecided — and the eight best frames are among them
**SEARCH. VERIFIED-IN-LOG, found independently by two lanes.**
M5's Phase-B queue was ordered by `Δ = n_components − k` ascending so the most compound
frames would run first, but `imap_unordered` writes results as they *finish* — **so the
22 rows that exist are the fast ones.** Seven of the eight compound-obligation frames
are undecided, **including both `Δ = −2` frames** (`m3k|d11` n=6, `m3l|d10` n=15), which
appear in no earlier sample. `Δ < 0` means the family spends more gates than it has
independent obligations, so a merged repair is **not excluded by counting** — these are
the only frames where the campaign's own structural argument does not rule out an 87.
U1's independent census found the same 8 of 204 (`f91b_7|d8`, `mix_6|d12`, `rho_2|d14`,
`rho_2|d7`, `m3a|d6`, `m3b|d14`, `m3k|d11`, `m3l|d10`).
Also here: **`f91b_7|d8`'s budget-7 search was still running when killed**, positive
control passed (`k=8` discharges all 7 obligations), `k−1 = 7` open, 13,003 siblings —
a bracket, not a refutation, and not counted in the 22.
*Cost:* `phaseB_remaining.json` holds all 182 in order; `verify/shot87.py` runs one
family at a time on a single local box. The lane's STATE.md says *"a successor should
start here."*
*Caveat the lane binds to it (U1 Cor. 7.2):* a `k−1` completion is **sufficient** for
an 87; its absence is **not necessary** for `C_AES ≥ 88`.
*Files:* `beat88/methods/m5_backbone/verify/{STATE.md,PHASE2.md,phaseB_run.log,phaseB_remaining.json,shot87.py}`.
*Source:* `beat88` L1 + L3 + U-1 (merged).

### 16. `e_upstream`'s 89 carrying a mask feature extinct in all 3.28 M known 88s
**BOTH. VERIFIED-IN-LOG. No write-up exists at all.**
`e_oddlane3/census.py` measured `|odd(m)| ≥ 3` at **0 occurrences in ~184 M mask slots
over 3,280,541 distinct 88-gate circuits**. `e_upstream` pinned such masks into
from-scratch roots and descended, banked **33 survival floors**, and stopped.
**`S89_41_00000098.json` is 89 gates and carries `0x98` with `|odd| = 3`.** All 33 were
checked in-process: realizable from the 32 singletons, 0 unbuildable masks, all 32
targets present, pin present in every one. Floor distribution: 89×1, 90×3, 91×6, 92×12,
93×6, 94×5.
*Why it matters:* **the price of leaving the corpus's 3,172-word vocabulary is measured
at ≤ 1 gate**, and the notebook's own reading table says a floor of 89 means "the
feature costs 1 gate — a real, quotable number". Nobody quoted it.
*Two named follow-ups, neither run:* (a) convert the 33 to oracle format and verify —
they are stored as `{"masks": [...]}` and **none has ever been through the oracle**;
(b) the general machine — five more feature classes listed and **not one priced**
(`|odd| ≥ 4`; the 388 never-seen weight-2 masks in `e_w2novel/candidates.json`;
weight ≥ 12; fan-out ≥ 8; the column-parity hubs `T_0,T_3,T_4,T_7` absent from every
record 88).
*Companion (`experiments_early` L5):* the four corpus 88-mask sets that do carry the
feature are **surrogate/transposed states, not MixColumns circuits**; and a radius-1
pin probe from an 88 returned 89 on every one of ~76 × 14 candidates. Together:
**reachable at 89 from upstream, unreachable at 88 by editing — construct into the
region, do not edit toward it.** Nobody drew that conclusion.
*Files:* `experiments/e_upstream/S*.json`, `experiments/e_oddlane3/{census.py,hunt.out}`,
`experiments/e_w2novel/candidates.json`.
*Source:* `experiments_early` L4 + L5.

### 17. The cheapest remaining +1 on the unconditional lower bound
**PROOF. VERIFIED-IN-LOG.**
U7's `cfE` ceiling instrument settled `minE_{K′} = 4` exactly (that rung exhausted at
54) but left the other keep-set bracketed at `minE_K ∈ [4,6]`. U3 §7: depth 4 →
`minE ≥ 5` → **`L(M) ≥ 55`**, ~10⁹–10¹⁰ nodes, *"plausible in C, ~hours on 2 cores"*.
U7's own FINAL STATUS labels this *"gift to U3, unused"*. Cheaper still: **only 3
keep-sets per size were ever swept and only 2 taken to depth 3**; enumerating all
`|K| = 14` sets with `q = 32` needs no new solver. And the `cfE` ceiling curve keeps
rising to **81 at `|K| = 24`**, so Theorem B is *not* information-starved —
contradicting U3's own "realistic ceiling mid-to-high 50s".
*Note:* the refereed bound is already 56, so a 55 is not itself news — the value is the
*method* reaching further, and the 81-at-24 curve saying the family has headroom.
*Files:* `beat88/understanding/u7_representation/`, `.../u3_lowerbound/RESULT.md`.
*Source:* `beat88` U-7.

### 18. Lane P handed lane B a strictly stronger tool and it was never used
**PROOF. VERIFIED-IN-LOG for the theorem, PLAUSIBLE-high-value for the payoff.**
Lane P §4.3 proves `N ≥ m_W + z_W + col_W` and measures it on lane B's own 22-gate R01
witness: **21 of 22**, against the 14 lane B was transferring. It states the actionable
form — add `z_W + col_W ≤ k − m_W` for **every kernel simultaneously** to the fortified
CNF, which at k = 15 forces `z+col ≤ 1, ≤2, ≤2, ≤3` under qk4/qk2/qk6/qk7 at once while
the record spends 2, 8, 0, 2 — and says *"Lane B can add them in an afternoon."* Lane B
had already finalized the same day; `grep -c fortify fleet1/laneB_regionbounds/ledger.jsonl`
shows the fortify arm stopped at k = 13. **This is the one mechanism in the projection
family lane P believes can push R01 past 15, it is proved, it is cheap, and it was never
run.**
*Files:* `fleet2/laneP_*/RESULT.md` §4.3, `fleet1/laneB_regionbounds/ledger.jsonl`.
*Source:* `fleet1_4` L4.

### 19. `R01 ≥ 16` — the quotient ladder's k = 15 level, started and abandoned 1/1008 in
**PROOF. VERIFIED-IN-LOG.**
Lane B's k = 14 landed after the write-up: `{"tag":"R01_qk4_s2","k":14,"status":"UNSAT",
"cubes":1008,"ran":1008,"wall":101990.2,"cpu_secs":484560.6}` ⇒ `m_qk4 ≥ 15` ⇒ the
quotient ladder **independently certifies R01 ≥ 15**, the pod floor reproduced by a
different method at a fraction of the cost. And `cubes/R01_qk4_s2_k15.jsonl` contains
**exactly one row** (cube 0:0, UNSAT, 0.09 s) — the k = 15 level, whose completion gives
**R01 ≥ 16, the first floor past the pods**. Fully specified, resumable, already
launched, never collected, never mentioned by a later wave.
*Also uncollected:* `R34_qk1_8_9` k = 14 finished UNSAT (28/28 cubes, 13,118 CPU-s),
verdict `bracket, lower_bound_proven: 15, ub 18`.
*Cost:* lane B priced k = 15 at ~2–9 Ms local CPU / **1–4 pod-days**.
*Files:* `fleet1/laneB_regionbounds/{ledger.jsonl,cubes/R01_qk4_s2_k15.jsonl}`.
*Source:* `fleet1_4` L1.

### 20. SG1 — the count-increasing excursion, the largest structural gap on the search side
**SEARCH. VERIFIED-IN-LOG.**
`laneFPOINT/RESULT.md` §6: both free moves preserve gate count, so *"an 87 reachable
only by passing through an 89 is outside this object entirely."* **378,189 states of
evidence say nothing about it.** The natural next object is the component under a move
set admitting a temporary 89 (mint two, orphan three) — which lane536 decided **only at
single sites**, never as a connected move set.
*Files:* `experiments/e16_lastwish/laneFPOINT/RESULT.md` §6, `.../lane536/RESULT.md`.
*Source:* `experiments_late` L19.

### 21. The parity-hub law and the P7 block re-synthesis that was specified and never run
**BOTH. PLAUSIBLE.**
`wave5/burn/handreduce/WAVE2_INSIGHTS.md` (48 KB of hand analysis, no code) identifies a
**parity-hub law**: the 88/89 separator is exactly "materialize ≥1 plane parity as a
cross-orbit hub", each hub costs one gate and serves ~3 targets in two orbits, and
89/90/92/96/97-gate circuits have none. Corpus-wide: **all observed hubs lie in
{P1,P2,P4,P6} — precisely the parities usable without touching P7 — while P7 is the
unique quadruple-duty mask**, appearing in all four carry-orbit terms; every circuit
instead re-buys P7 fragments per letter, and *"the invariant 21-gate xtime-carry toll is
exactly the cost of refusing to materialize P7 once."* Uniform across all eleven
circuits examined. It ends with a concrete instruction: **exact SAT/ILP re-synthesis of
just the carry-orbit block** (16 targets, frozen non-carry interface and pair layer)
over a basis extended with a materialized P7, asking for ≤ current block cost − 1, with
the prediction that the hub-free version returns UNSAT and *"the hub-extended instance
is where 87 lives if it exists."* **Never run.**
*Companion in the same lead:* the one improving window whose shape the project holds is
**disconnected** (four pairwise non-adjacent masks) and every generator ever run samples
connected sets (`cluster` 0/197,000, `cone` 0/118,000). Wave 6 built the disconnected
generator — ~3,600× enrichment, 872 theorem-grade decisions, 0 SAT — but killed it at
n ≤ 9 while the new encoder reaches n = 14–16. **The predicate and the encoder were
never combined.**
*Source:* `campaign_87` L17.

### 22. The plane-locality theorem test — one solver call on a 12,946-mask space
**PROOF (a real theorem if UNSAT). PLAUSIBLE.**
E1 §8.4: every one of the 1,136 masks of every verified circuit on disk, and every valid
single-mask repair of the 88@5 / 89@5 / 92@4 anchors, lies inside a **12,946-element**
subset of the 2³² mask space. Its own proposed decisive test is one sentence: *"hand
`atlas/slp_opt.py` an 87-gate instance restricted to plane-local masks: UNSAT there
would be a real theorem about a 12,946-mask space instead of a 2³² one."* Never run.
*The report calls it the cheapest route in its slice from a corpus regularity to an
actual theorem.* Read it against Tier-2 #13: the plane-local restriction is exactly the
kind of instrument cap that the plane-cage work says is not a property of optima — so
an UNSAT here is a theorem **about the restricted space**, and must be stated that way.
*Companion:* E2 §8.3's **bit-7 carry-gate prefix** — the only genuinely high-order
sharing in all nine verified circuits is 2–3 weight-2 masks on bit 7, forced by `0x11B`,
present even in the 97@3. Fixing them as a forced prefix and searching the remainder is
*"a legitimate, never-tried restriction, and unlike most restrictions it has direct
evidence of being satisfied by every known optimum."*
*Source:* `experiments_early` L9.

### 23. `n_components ≥ k`: re-run the five exclusions through `close_core.py`
**PROOF. VERIFIED-IN-LOG. "The clearest unfinished path toward a real obstruction
argument in the slice."**
`n_components ≥ k` holds in **60 of 62** profiled families (196 of 204 in the full
Phase-A profile). PHASE2.md §1b: *"That is the structural reason 87 is hard here — the
obligations are already nearly in bijection with the gates."* §1c found **four distinct
gauge orbits** where `k−1` provably cannot finish the core — *"the most lower-bound-shaped
result in this phase"*. The caveat is explicit: those 5 exclusions used a relaxation that
does **not** cover the gate-pair (E3) channel, so they are "not yet sound". §2 built the
sound version (`close_core.py`) and ran it to completion **only for the derived 88@5's
frame**. *"Re-running the 5 exclusions through `close_core.py` is the immediate
follow-up"* — and it never happened; `close_core.py` was killed as "superseded by the
physical searcher", which then decided only 22 families.
*Source:* `beat88` L7.

### 24. `f91b_7|d8`'s double-hit dead mask — the sharpest single anomaly in the corpus
**SEARCH. VERIFIED-IN-LOG.**
`u1_obligations/NOTEBOOK.md` §5 check 3: for `f91b_7|d8` the two E3 gates satisfy
`00010203 ⊕ 83800001 = 83810202`, which **is** the singleton dead mask of comp6 — *"and,
remarkably, a second pair of that family's repair gates hits the same dead mask:
`00810283 ⊕ 83000081 = 83810202`."* **Two independent gate pairs in one family XOR to
the same obligation.** Nothing anywhere in the tree explains, generalises or exploits it.
It is exactly the shape of redundancy an 87 could exploit, **and it sits in the one frame
the campaign named as its best remaining lead** (see #15).
*Source:* `beat88` U-2.

### 25. "An 87 must buy a gate that serves nothing" — a priced theory with no instrument
**BOTH. VERIFIED-IN-LOG.**
U1-15 prices the only known escape exactly: `γ(U) = 3` for the 87-mask state
`U = exterior61 ∪ n16`, cheapest schedule `enabler → trigger → bridge`, **the middle gate
not constructible from `A`**. U7 §8.7(f) supplies mechanism and price: a full-class (Λ)
mask is cheap to build but **every consumer of it toward a target must cancel**, because
no target has heavy pattern `H`. So "buy a gate that appears useless" is a
theorem-shaped requirement with a price tag. **And every search instrument in the
campaign — tier-3, novocab, all the deciders — buys only from `cons(A)` and therefore
cannot reproduce the one completion the canon has priced.** The most coherent positive
theory of where an 87 lives that the project produced, and nothing was ever aimed at it.
*Corroborating from another slice (`root_infra` L9, `beat88` U-5):* drop-0 "useless"
gates are **5× more common in 88s than 97s and placed later**; the from-scratch 88@5
contains **six moves that make it worse**.
*Source:* `beat88` U-3.

### 26. Search *inside* a `c`-fibre — mapped, enumerated, abandoned at shutdown
**SEARCH. VERIFIED-IN-LOG.**
There are exactly **11 non-zero non-singleton heavy classes**, so `c ∈ [8,11]` and
**nothing else exists**. Known 88s occupy {9,10,11} (11/89/104 of 204); `c = 8` is the
97; and `c` slides `|Z|` against `|cf|` **at constant sum 88** (`c = 9 → 23+65`,
`c = 11 → 33+55`). So **an 87 must move *within* a `c`-fibre** — precisely what U5's
`plans8` (4,510) and `plans9` (336,484) enumerations parameterise. **Nobody ever searched
inside a fibre.** A concrete, finite, fully-enumerated space, mapped and then dropped.
*Files:* `beat88/understanding/u5_heavycorner/heavy_corner_library.json` (1.3 MB).
*Source:* `beat88` U-6.

### 27. e15's "run C" — approved, sampled, banked, never run
**SEARCH. VERIFIED-IN-LOG.**
`e15_campaign3/RESULT.md`: *"RUN C WAS APPROVED, ITS SAMPLE WAS DRAWN AND BANKED
(`sample500.txt`, 500 rows), AND IT NEVER RAN. There is no `sweep_C_sample.jsonl`
anywhere in the repository."* A stratified 500-circuit `d(S) = 1` sample at a 200,000-window
cap. **The cheapest slice of the 1,200-CPU-hour `d(S)=1` population gap** — work list on
disk, instrument complete and twice-validated. `d(S)=1` currently stands at **17 of
17,283 population circuits attempted at all**.
*Files:* `experiments/e15_campaign3/{sample500.txt,RESULT.md}`.
*Source:* `experiments_late` L2.

### 28. Axis 20b — the symmetry/normalisation rules N1–N3 have never been re-refereed
**PROOF-hygiene. VERIFIED-IN-LOG.**
`LIBRARY.md`'s corrected picture names four genuinely-open axes, and this is the one with
teeth: **every UNSAT this repository has ever emitted rests on N1–N3, and no one has
re-refereed them, including the audit referee.** If they are wrong, an unknown share of
the project's negative results are wrong with them. The other three genuinely-open axes:
**13** (currency per-line independence — *"the only untried attack on the 22 rather than
the 66"*), **24** (L5's forward-only rule — a fixpoint over blocks that no ordering of
the current loop can express; laneORDER's 75/75 negative is the evidence that permuting
is exhausted), and **21** (the un-split block, priced dead at k ≥ 14).
*Files:* `fleet12/LIBRARY.md` §4/§5 (stale scoreboard → `CORRECTIONS.md` C-07).
*Source:* `fleet9_12` L4.

### 29. The complete `C(57,5)` shell of the record 89 stopped at 19 %
**PROOF. VERIFIED-IN-LOG.**
`m2_oracle/STATE.md`: 789,584 of 4,187,106 windows. A zero-win *completion* would prove,
via removal monotonicity, that **no sub-88 circuit adds ≤ 3 new masks relative to the
shipped 89@5** — closing core-5 for the record circuit, the single question M2 names as
"the last open question for the record circuit". Resume command written out verbatim.
*Cost:* ~1.7 pod-days under PyPy, **~2 h with the C kernel**.
*Caveat:* this is a radius-≤4-class result — see the standing caveat at the top.
*Source:* `beat88` L4.

### 30. `e11`'s `k = 12` — one open level, priced, 0.81 % banked and resumable
**PROOF (sub-instance pricing). VERIFIED-IN-LOG.**
`12 ≤ cost ≤ 13` for both dim-10 quads; k = 12 is the *only* remaining level for either.
**~1.92e11 nodes ≈ 38 CPU-hours per quad**, "roughly one overnight run on four cores";
276 of 34,080 root cubes already closed in `shards/q0_7_8_24_k12.jsonl`, resumable with
`--tag`. The matched control now fires at dim 10, so the answer would mean something.
*Counter-evidence:* 750 directed plants produced **0** instances with `cost ≤ 12` and
`cost_cf ≥ 13` — the best current reason to expect 13.
*Source:* `experiments_late` L5 (+ L6 for the unsampled `cf = 13` stratum).

### 31. `--avail`: the first formulation in which cancellation can show a gain
**BOTH. PLAUSIBLE.**
`e10_crossfam/RESULT.md` §7 item 2: for a cancelling gate `g` of a verified 88 serving
rows `R`, let `W` be the masks available just before `g`, and ask for the exact minimum
cost of `R` **from `W`**, with and without cancellation. §1(b) is the reason: every
cancelling gate lives in a cone **at least 2 gates above** the standalone optimum, so
*"the cancellation is not a local saving; it is the repair bill for reusing a wire built
for other outputs"* — the payoff is realised in the complement of the cone, exactly where
subset pricing cannot see. Implementation cost stated as **one new flag on `qsearch`**.
e11 did item 1 instead; item 2 was never built.
*Source:* `experiments_late` L24.

### 32. The ρ-class asymmetry: `≤86` trims occur only in ρ-classes {0,1,3}
**PROOF (theorem-shaped). VERIFIED-IN-LOG, never attacked.**
Measured over **170,921 states** in `wave5/burn/simple/execute/`, and it **survives a
DAG-randomization control** (wave-6 A1 audit: *"the absence of class 4 is the
theorem-shaped fact"*). It reached `wave6/TRIAGE.md` as a live item and was never given a
dedicated attempt. If the absence of class 4 has a proof, it is a structural obstruction
of exactly the kind the obstruction hunt concluded must exist — **an invariant of a single
circuit, not a count of circuits.**
*Source:* `campaign_87` L6.

---

## Tier 3 — real but expensive, speculative, or narrow (33–54)

| # | Lead | Tag | Conf. | Cost | Files / source |
|---|---|---|---|---|---|
| 33 | **Odd-`a` sector.** `OBSTRUCTIONS.md` §1b proves (P1/P2) any 87 whose mask set is exactly ρ- or ρ²-closed contains an **odd** number of fixed masks; at 88 the constraint is vacuous. *"The orbit engine has never walked odd-a configurations"* — both symmetric basins (a=10, a=16) and the 12-mask trick are even-`a`. P2 was never encoded. Corroborating: the natural trimmed hub set {P7,P2,P3} has odd size 3 while all known 88s carry an even hub count. | BOTH | VERIFIED (stmt) | UNKNOWN | `campaign_87/wave5.../burn/obstruction/OBSTRUCTIONS.md` §1b — `campaign_87` L7a |
| 34 | **The `v·(1,1,1,1)` marker.** Every known 88 — five families, all 134,889 sampled plateau points — contains ≥1 mask `v·(1,1,1,1)` with `v` a single bit; our 89@5, 89@6, the 90s, the 92@4 and the 97@3 contain **none** (Sun–Yang–Li's 89 carries one). Correctly flagged "do not cite as evidence" and kept out of the publication draft — but as a **falsifiable prediction about any future 87** it is the sharpest structural regularity measured, and no proof route was attempted. | PROOF | VERIFIED | UNKNOWN | §5c, same file — `campaign_87` L7b |
| 35 | **`|W| = 2` instrument never built** — remove-3-add-2 discharging a compound obligation two-for-one. U1 and U2 both name it as the open door; Theorem 4 says it is exactly where a compound obligation's marginal cost could drop. Natural inputs = the `Δ<0` frames of #15. | SEARCH | VERIFIED | UNKNOWN | `beat88/methods/m5_backbone/verify/STATE.md` §6.3 — `beat88` L2 |
| 36 | **The routing constructor, unfinished at 99.** 108 → 99 by rerouting alone with `A` frozen (`fiber_best_99gates.json`, oracle-VALID depth 4); **the recursive descent past 99 was never run.** PHASE2.md §5.5 calls the routing axis "real and unexploited": same masks, ≥5 gates apart. Orthogonal to every other method in the campaign. | SEARCH | VERIFIED | UNKNOWN | STATE.md §6.5 — `beat88` L6 |
| 37 | **`vac(w) ≥ 3` ⟺ remove-3-add-1 ⟺ an 87 from an 89**, never run on the 46,318-orbit 89 census (only on the 64 known anchors). Sized at ~77 core-hours by the shell route, "a small job" by the `vac` route. ⚠ The equivalence is a **conjecture**: a positive is an 87 unconditionally, a negative needs a control against complete k=3/b=1 shells first. Adjacent: U2's own #1 next step — *"91 of 221 adjacent served pairs still collide; what distinguishes those?"* — the only obstruction between 4,600 high-mobility rigid 89s and an 88, stopping 53 % of them alone. | SEARCH | VERIFIED | ~77 core-h | `beat88` U-12 |
| 38 | **1.4 M distinct 88s in `sub92.jsonl` were never mined.** 1.45 GB, 1,441,779 lines, every distinct ≤92-gate mask set NRPA produced including **1,400,343 distinct 88s**; exactly **five** circuits were ever extracted and nothing else reads it. Given `union_sat`'s measured control (unions of two remote circuits hit floor 88 at 0.7 %), this is unmined pair material. Also unread: `d3_model/harvest/*.dist.jsonl` (115 MB, no reader), `agents/frontier-d6sat/` (94 MB, zero prose), and `hunt87`'s **64,421 states dropped on backlog overflow** (recoverable by re-running the detector from offset 0). | SEARCH | SMELL | UNKNOWN | `campaign_87` L13 |
| 39 | **Still-open SAT windows at budget 87, with resume state:** 4 on Jean's 88 (k=13–15), 3 on the independent 88 (k=12–13), 20 on family 3 (k=13–16), plus **18 in the unreported `frontier-sat`** given only 2,700 s. Compute mistake on record: `loose-sat`'s four survivors had already timed out at 4,800 s each and were re-run at **2,700 s** — 44 % *less* compute than they had survived — while the recommended `--timeout 21600` overnight run never happened. ⚠ Wave-1 `sat-window`'s 25 timed-out windows are **not reconstructible** (removal sets never logged) and must not be cited as a resumable frontier. | SEARCH | VERIFIED | UNKNOWN | `campaign_87` L14, `root_infra` L7 |
| 40 | **Six `|B| = 11` dim-12 tap regions remain**, each a measured ~2,000–5,500 s job on a resumable driver (`88@6 R4`, `88@7 R4`, `p88_00/03/05/07 R4`) — after four were decided at `min_gates = 11` with positive controls, incl. one on Jean's foreign-lineage 88. | PROOF | VERIFIED | ~2–5.5 ks each | `experiments/e7_push/` — `experiments_early` L2 |
| 41 | **Search in the transposed frame — proposed, never run.** `transposed_frame.md` establishes `L(M) = L(Mᵀ)`, gives a verified transpose-and-back path (11/11), and measures `r(mask weight, co-mask weight) = −0.62..−0.73` — so the existing instruments, run unmodified on `Mᵀ`, would explore a slice ranked by a nearly opposite statistic. The transposed *bound* lane was exhausted and closed; the transposed *search* (§3.1) never ran. Tooling exists and the plateau walkers are circuit-generic. | SEARCH | PLAUSIBLE | UNKNOWN | `atlas/thinktank/transposed/` — `atlas_misc` L3 |
| 42 | **A bracket-aware DP for the 32 timed-out strata.** 32 instances timed out at the 900 s cap, each banking `lower_bound_proven = 10` with no upper bound, and **none is in `m1_sigma.json` at all** (verified: 0 present by canonical `(kind,P,Q)` key). In exact/pessimist mode they price `INF`; in optimist mode they are filled at the floor **7**, far below their proven **≥ 10**. Folding the banked brackets in as genuine lower bounds can only *raise* the optimist floor — a small edit to `solve2`, and the cheapest available strengthening of the class result. Sharpens the standing caveat that **M1 = 91 is an upper bound plus a witness, not a floor**. | PROOF | VERIFIED | small edit | `atlas/{m1_sigma.json,m1_wide_results/,m1_v15_results/}` — `atlas_misc` L5 |
| 43 | **Two structural identities nobody built a search around.** (a) `F = 64 + a − c − 2d`, verified 67/67 — so an 87 requires exactly `a − c − 2d = 23`; §9.3 marks the lower-bound use (*"bounding `c` above and `a` below"*) **never attempted**, and it is a shape this project has not tried. (b) The **rank-3 manufacture question** (`tri_search.md` §8.2.5) — "make an open node a 3-fold XOR of closed masks" is, in the ring frame, an **algebraic** question, not a search, and it is the exact bottleneck the market measured at probability 2.6e-4. Explicitly never attempted. | PROOF / BOTH | PLAUSIBLE | UNKNOWN | `atlas/thinktank/{backward_search.md,tri_search.md}` — `atlas_misc` L6 |
| 44 | **Banked, resumable timeouts across the theory lanes.** (a) U5's `E ≥ 8`: budget 6 refuted in 1 node, budget-7 run **stopped after ~10 CPU-min** on memoisation memory — *"rerun with a node cap or a support-size prune"*; if `E ≥ 8` held, the heavy floor becomes 28 (and even then only the `z = 1` sub-branch; `z ≥ 2` untouched). (b) **11 undecided tier-2 dropscan elements on the 88@6** — ~44 s each at 4 CP-SAT workers closes tier-2 on a second family. (c) **`cfsynth cfm` never finished** — `CF(M) ∈ [79,103]` and closing, now interacting with V2's verified 102, so `CF(M)`'s exact value in [79,102] is genuinely open with the machinery on disk. ⚠ Systematic caveat → `CORRECTIONS.md` C-39. | PROOF | VERIFIED | (b) ~8 min | `beat88` U-8 |
| 45 | **The `Z/4` byte-lane gauge is completely unbroken — a free 4× on every solve.** Verified in V2's model: rotation maps `TARGETS` onto `TARGETS` and permutes the 1,648-mask `IN` universe onto itself for all three `k`, so **every solution comes in orbits of up to 4**. Breaking it is a lex-leader constraint on the `IN`-indicator vector. *"Not done here."* Related: **ρ-symmetry breaking over the 8 `Z/4` orbits is the named unexploited lever** for the `G_int(3)` / exact-`L_cf` encodings, which use it not at all. | enabler | VERIFIED | one constraint | `beat88` U-10, `fleet5_8` L6 |
| 46 | **A2 has never been asked the right way.** The 223-mask union question at budget 87 has timed out three times (SAT 2,013.6 s; PB 3,601 s) — but the **pinned control now SATs in 1 s** (the admissibility control the question never had), and V2's own measured law says PB should be run in **optimisation mode, never as a budget ladder**. A2 has only ever been run as a decision at a fixed budget, and now has a validated model attached. | SEARCH | VERIFIED | UNKNOWN | `beat88` U-14 |
| 47 | **The rewiring null for the surviving-side zero.** `DOSSIER.md` §9.2 + `REF_DELTA/VERDICT.md` F5: the 54,561-mask surviving-side zero is not circular but is weak and confounded (`p ≈ 0.015–0.25`), and **every null ever run for it is confounded in the same direction**, because a "site" is a property of the wiring and the corpus's wirings are not sampled (`_closure_core` fixes every parent by one deterministic rule). The experiment: hold each corpus 88's mask set fixed and re-wire it many ways — **`fleet1/laneC_proofside/code/rewire.py` already does this** — measuring the surviving-side rate across wirings of the same circuit. *"It is cheap. It is the null this quantity has always needed. Nobody has run it."* | PROOF | VERIFIED | cheap | `experiments_late` L11 |
| 48 | **The instance-shrinking criterion, and laneDELTA's obituary that is NOT established.** `DOSSIER.md` §9.1 / `REF_DELTA` §6: the right criterion for whether a local-optimality theorem aggregates into a lower bound is not "how rare is the coincidence" but **"does the local theorem license a step that SHRINKS the instance?"** Lemma F has one — that is why the refereed 55/56 exists; Lemma R and T2 do not. **The referee explicitly rules that laneDELTA §8 ("the whole local-optimality direction is closed; this file is its obituary") is not established** — the restriction-and-recurse sub-direction is live. | PROOF | VERIFIED | UNKNOWN | `experiments_late` L12 |
| 49 | **`t = h1 ^ h2`, the both-helpers-new sub-gap**, inherited verbatim from e13, declared by e15, closed by nobody. Every d3 row carries `aimed_helper_only: true`: *"A d3 zero means 'no compressible window found by the aimed-helper search on this enumeration'. It does NOT mean 'none exists'."* The 13 anchors are ENUMERATED-WITH-A-DECLARED-SUB-GAP, never CLOSED — **a genuine hole in the strongest local negative the project owns.** e15 lists building the complete instrument as its lead #2. Adjacent (L18): run A found **six circuits with shared helpers** and the same mask **`0x2818302` recurs across three unrelated circuits**, so `d(S) ≥ 3` on the population is not closed and the recurring mask is undecoded. | PROOF | VERIFIED | UNKNOWN | `experiments_late` L3, L18 |
| 50 | **`Q(V*, 87)` was NOT REACHED and NOT answered negatively** — "is there an 87 using only masks some known 88 already uses?", `V*` = 1,393 masks, no encoder reaches above ~100–134. The ceiling was *measured* (11× budget bought +11 % rounds while seconds grew 11.2×), so it is a ceiling, not a curve. e15 calls it *"the sharpest unanswered question the campaign owns"* and says the fix is **a different instrument**. | SEARCH | VERIFIED | new instrument | `experiments_late` L4 |
| 51 | **`le4`'s fast path is the weakest load-bearing joint in the 2-mint/3-orphan closure.** `slp3.py`'s completeness survived 8,000 random-topology plantings; `le4`'s fast path has only 428 planted instances, of which **28** came from a random topology — so **1,309 of the 1,409 k=2 negatives rest more on the argument than on adversarial testing.** Brute-force closure ≈ **11 CPU-hours**. | PROOF-hygiene | VERIFIED | ~11 CPU-h | `experiments_late` L22 |
| 52 | **Cell and gate axes never swept.** Every lane-level theorem in waves 3–4 is **cell-conditional at one cell** (88@7 or 88@5), and the other cells were never touched. Named and unrun: (a) the interface-level curve at *every* tap at *both* cells — "the whole depth premium is one number per interface", 3-parameter, minute-scale solves; (b) **sweep the CELL against depth** — *"ten cells at ~1 h each would answer which cells support 88@5? — and that question has never been asked in this repo"*; the 19 cells' currency curves are already computed and free; (c) **sweep `C_3` alone** — "the cheapest genuinely new axis in the whole configuration space, and it is how 88@5fs buys `B = 19`"; (d) re-run the stratified attribution at the other five R34 cells. | PROOF | VERIFIED (unrun) | ~1 h/cell | `fleet1_4` L7 |
| 53 | **Two cheap named experiments in the proof-side lanes.** (a) **Re-point the y1 census at `\|Cl \ U\|`** — 3,254 circuits × 16 wirings in **132.5 s** — to find the true worst case of `kappa − \|Cl \ U\|`. `\|Cl \ U\|` is **13–22 on every circuit from 88 to 92 gates** and is *invisible to every price certificate in the program* (U6-2, U6-3, Lane P's `B`, laneTOOL2's `Phi` all live on `U`); the strengthened chain reads **78–85 against n = 88..92** versus 65–73. The lane calls it "the cheapest identified place to look for the missing increasing-in-kappa term", and it is a **falsification first**. (b) **A certified rational upper bound on `B*`** — the LP dual is already computed and only needs exactifying; it would prove the U6-2 certificate form can never reach `L_cf ≥ 93` and make the family ceiling rigorous at `kappa ≥ 20`. Priced at ~1 session. | PROOF | PLAUSIBLE | 132.5 s / ~1 session | `fleet7/laneUNCOND` §7.3, §7.5 — `fleet5_8` L6 |
| 54 | **Small, cheap, uncollected.** (a) **Forced-late output rows as a plateau invariant** — three independent forced-depth obstruction patterns are on record and never compared (old plateau {3,27}; 88@6 {1,11,17,25}; 88@5fs {1,7,12,13,17,18,21,25,27,28,31}; Jean's three bits at depth 7); rows 1, 17, 25 appear in two patterns, 27 in two. Computed by a cheap existing fixpoint (`engines.py:relax`); ASAP depth over a **mask set** is not a DAG statistic, so it survives e14's cull (`records_repo` L5). (b) **Canon the 15,650 depth-4 91s in `pod2`'s MANIFEST** and count distinct orbits — the record file says 34 circuits / 32 orbits; if it is more, the depth-4 frontier is wider than the record suggests and a depth-4 census is a new publishable object. **Nothing has ever attacked 96@3** on the same Pareto frontier `{3:97, 4:91, 5:88, 6:88}` (`beat88` L5). (c) **Mine the 31.4 GB of descriptor telemetry before it is compressed or deleted** — it carries `deg_max` for every visited state (M2 recorded 118 orbits at `deg_max = 13`, above both canonical families) and the neutral out-degree of every 88 the fleet ever touched (25 of 29 certified 88s sit at exactly 16; **the four outliers at 12, 14, 20, 21 were never identified**) (`beat88` L9). (d) **A third distinct 88 @ depth 7 sits unregistered in a scratch directory** — `found_88at7_walkonly_seed1011.json`, oracle-VALID, J = 0.833 to the record, matching no file in `evidence/circuits/`, produced by a one-word change (`ENGINE="walk"`) in 18.5 min vs 34.4 (`beat88` L11). (e) **The k=5 escape operator has never been fired at volume** — `remove1_add2` + trim is a complete k=5 descent operator that reached 89s no k ≤ 2 shell contains (9 of 36 hits carry its signature); 2,274 firings at retirement points only, *"the cheapest possible sampling and also the thinnest"* (`beat88` L12). (f) **The corrected ruler's own fitted target was never built** — heavy-mask emission is 1.11/1000 (popcount arm), 18.27 (corrected-W), 14.80 (uniform), and the fourteen known 88s sit at **7.31, between the two arms**; a ruler or temperature tuned to 7.3 is a one-line change to `corner/walk.c` and the §4.6 temperature sweep is exactly the dial (`atlas_misc` L2). (g) **`atlas/soclecurrency/` is the one undocumented lane** — 1,048 solved sector instances and a full DP whose docstring implements the **dcost over-charge fix** flagged as possibly pricing real 88s at 91, with **no writeup**; read `dp.py`'s output before the tree is reorganised (`atlas_misc` L7). (h) **Two truncated relaxation runs** — `fjb.log` reached 90 in MODE=junction and the log ends with no optimum line; `eft.log` stopped at 800 of 3,249 frames in MODE=both, on a script advertising "seconds instead of hours". Expected outcome is a sixth confirmation of 91, but it is the one M1 computation *started and abandoned* rather than decided (`atlas_misc` L4). (i) **The 92-gate waypoint calibration is finished analysis waiting to be written** (`analysis/waypoint_census_92.{jsonl,txt}`) (`beat88` L10). (j) **`satquot.py`, the symmetry-quotient SAT search, was written and never run to a conclusion** — 88 = 4 × 22, so the quotient search at **k = 22** is precisely fleet9's own written request, and the instrument and the request sit in the same repo unjoined; two negative signals (fleet10's symmetric mode is ~12 gates worse; **zero ρ-fixed circuits among 54,889** 88s) make it low expected value (`fleet9_12` L6). (k) **Re-price gauge choices in gates rather than rank inside the atlas σ framework** — the review calls gauge freedom *"the one thing here the atlas frame does not have an explicit version of — it is aimed at the wrong objective, not a bad idea"*, and no `gauge`-named artifact exists in `atlas/`; also §23's Pareto rows 3–4 were never reconciled (the review's dual reproduces rows 1–2 exactly but reaches 15 roots where the document claims 12, and never reaches rank 21) (`root_infra` L6). (l) **Is there a feasible Check-1 table with `delta_2 > 0`?** — an LP question nobody has asked; `delta_2 = 0` is a statement about a *tight Check-1 column*, i.e. about the certificate rather than about `M`, and answering it would change a conjunct of the Anatomy Theorem (`experiments_late` L10). (m) **The `MIX_d4pop300_pop88_400` rung** — 554 masks, **175 of which no depth-4 circuit on disk uses**, TIMEOUT at 1,792 s; the direct test of E4's own constructive instruction, named as *"the run to re-launch first on an uncontended box"*; alphabets on disk (`experiments_early` L11). (n) **Drop sets of size 2, 3, 5, 6, 8 are untouched and now cheap** — a `W`-for-`W−1` refutation at `W = 12` would be a **radius-23 local-optimality certificate**, far beyond anything in the corpus; measured at ~4 s at k=6, ~400 s at k=8, ~1 h per circuit screen (`experiments_early` L13). (o) **The odd σ-half contains only odd costs** — below 91 the next value is **89**, a *two-gate* move this project has never made at that scale (5,728 σ-closed states, 10 arms, not one even cost); and the complete single-orbit repair walk at **47 it/s** is the only instrument that ever descended two gates inside the half, against destroy/rebuild LNS at 1.2 it/s which descended not at all (`experiments_early` L14). (p) **E8's named fix for the dim-12 wall** — replace the `2^dim` `dist[]`/delta pass with a lazily evaluated bound over the ≤20 available masks; the single change that would open orbits 1, 3, 4, which currently sit as live brackets `[12,16]` (`experiments_early` L7, `experiments_late` L23). (q) **Untried alternative universes** — `U₁` as the named universe (38,240 masks, 665,024 CF-split literals, containing 84/88 of the 88@5's masks), intrinsic and complete for its index, untried; and V1-2(b)'s successor tier-3 model, fully specified and sized with both mandatory control gates written down, never built (`beat88` U-13). (r) **What do the diagonal-class heavy gates buy?** — classes {7,23} and {15,31} hold **no target at all**, are seeded by 168 and 173 of 204 families, carry 3–5 gates each; every known 88 pays for at least one target-free class and *nothing in the lane explains what they buy*; listed as **unassigned**. Sibling: the **cashing law should be provable outright** (425/425 measured, proof route stated), upgrading u2's cuttability criterion from a 299/300 empirical rule to a theorem (`beat88` U-15). (s) **Data generated and never analysed:** `boundprobe_{7,42,99}.{json,log}` (three completed seeded runs, no discussion anywhere) and `u2_walls/data/mask_enrichment.json` (no mask-enrichment claim in the notebook) — pointed given that **92.2 % of every cut ever found adds one of two masks** (`beat88` U-17); the U5 × U6 join was never made because U6 wrote its spec believing U5 did not exist (`beat88` U-19). (t) **The 572-mask global MILP timeout** was correctly not counted as evidence — and therefore a bracket was banked and dropped; the same document notes the repair searches touched **2,288 distinct masks of which 1,905 had never appeared in the 801-mask proposal universe**, a measured demonstration that the search language excluded most of the algebraically relevant structure (`root_infra` L8). (u) **The 88@7 has no exhaustive shell at any radius** — all 47 exhaustively-certified canonical circuits lie in Jean's lineage, and *the one circuit independent of that lineage is precisely the least certified*; the derived 88@5 has only a k=2 log (`root_infra` L3, `records_repo` L3). (v) **11 unread cancellation numbers** — `cleanroom_verify.py` records per-circuit "canceled basis terms / canceled input occurrences" (derived 88@5: 33/66; from-scratch 88@5: **44/88**), sitting unread in `audit/recomputed_metrics.json` for a month, while the whole optimality question has been reframed by `L_cf ≥ 92` as "what does cancellation buy?" (`records_repo` L6). (w) **The 92@4 anchor is a trap nobody resolved** — 0 of 9 depth-capped restarts reached 91 (E4), independently reproduced 0/3 by E9, while the inventory records that step as a four-minute result; the citation chase shows `TOPOLOGY.md`'s "91@4 in four minutes" describes a *from-scratch* descent, not a one-gate improvement. E4 priced resolution at **30 minutes**. E9's framing is the strongest strategic signal in that slice: **cold restarts reach the frontier, local search cannot cross it** — and the comparison nobody has run is N core-hours of `ladder_parallel` cold roots against N core-hours of frontier-local search, scored on distinct frontier circuits found (`experiments_early` L10). | mixed | mixed | mixed | as cited |

---

# B. EVIDENCE ABOUT *WHY* 88 — not leads, but the public-page material

These are not actions. They are the project's accumulated answer to "why does 88 keep
appearing", assembled from five reports. Each carries its own honest counterweight, and
the counterweights are load-bearing.

1. **Efficiency inverts, six independent ways** (`beat88` U-5). The greedy-108 sits
   *exactly* on the `L = 152` floor with debt 0 at every cut and is the **worst** circuit
   measured; `W = L − 152` runs 0 → 18 → 52 → 60 → 92 down to 88. At fixed depth 8,
   AUC(89 > 88) is 0.78 for service and **0.87 for `V`**, and service correlates with gate
   count at **+0.26 — the wrong sign**. 97 → 88 sheds ~19 light gates and *buys* ~10 heavy
   ones. Drop-0 "useless" gates are **5× more common in 88s than 97s** and placed later.
   **The best circuits carry the most waste. Any constructor that optimises a legible
   efficiency metric is walking uphill.** Corroborated independently by `root_infra` L9
   (outputs served per gate rises 97@3 → 88@6, 1.753 → 2.773, with cancellation debt rising
   alongside; the from-scratch 88@5 contains six moves that make it worse).
2. **The frontier-tightening triple** (`beat88` U-4), measured over **9.5 M cancelling
   gates**, largest stratum giving the tightest bound: `cover(O) ≤ 2` at 88 vs ≤ 3 at
   89/90; `max wt(O) = 7` at 88 vs 9 at 89/90 (**and 7 is exactly the heaviest target
   weight**); `max wt(σ) = 14` against a proved ambient 32. V1's reading: *"If it is a law
   rather than sampling, an 87 would have `cover(O) = 1` throughout."* **Nobody tested it,
   and the obvious test is the lineage control u2 already built.** Cite as *"the proved
   ambient bound is 2.3× the largest span anyone has observed"*, never as *"a factor of
   2.3 remains"*.
3. **Conservation laws, proved tight, at four scales** (`fleet1_4` L8, `fleet5_8` L7).
   `B37 + U4 = 11` invariant over every configuration measured, with the replay bound
   proving it a **floor**; `costT(C_0) + U07 = 12` constant across seven distinct menus —
   each gate spent on line-0 currency buys back exactly one gate of `U07`, **never two**;
   **19 block boundaries dissolved, 19 times exactly the split total**, and 7 dissolved
   simultaneously still landing at exactly 88; the cost-2 shared-plane family drops the
   consumer floor 8 → 7 and raises the supplier's price to 89. *One gate in, one gate out,
   every time.*
4. **Rigidity, halo, saturation** (`fleet9_12`). 13 of 17 blocks have a unique optimum at
   every one of 70 tested cells and never vary across 54,889 wild circuits — **28 of every
   88 gates are forced once the menus are chosen**. Widening what a block *may* use changes
   nothing, because it does not change what the block is *minimising* (`W3` handed a whole
   extra line kept all eight witness gates inside the original three). Under the forced
   dependency edges the supply graph is already saturated, so all 75 legal orders emit the
   byte-identical circuit.
5. **The composition identity** (`experiments_late`, bonus). `88 = 32 finals + 56 middles`
   is forced; every decoded mechanism moves a gate between the currency and helper piles;
   every measured cross-frame exchange is 1:1 as a **consequence, not a coincidence** — any
   two 88s are joined by substitutions that must net zero because both endpoints cost 88.
   **"A composition of wash-mechanisms is a wash."** Paired with e16's forcedness result —
   that a true optimum of this size would be expected to have hundreds of structurally
   distinct realisations — **the plateau's width stops being evidence of looseness.** The
   two halves currently sit in different campaigns' documents with nothing joining them.
6. **`c` is exhausted** (`beat88` U-6): exactly 11 heavy classes ⇒ `c ∈ [8,11]` and nothing
   else exists; 88s occupy {9,10,11}, the 97 is `c = 8`. **An 87 must move within a fibre.**
7. **`L_cf(M) ≥ 92`** (`fleet1_4` L8): the only proved quantity above 88, so the whole
   question is literally *"how much do cancelling gates buy?"* — the records answer "at
   least 4", an 87 would answer "at least 5". And `κ` is monotone against `n` across the
   spectrum (9,10 → 18,18,19 → 21 → 22..28 as `n` goes 97 → 91/92 → 89 → 88), with the cone
   union at **53–56 clean gates for every circuit from 88 to 92** and 33–35 for the 97s.
   Lane P: *"A lemma that explains that number is the lemma."*
8. **Symmetric basins** (`root_infra` L9): the elite basin is **79–81 % ρ²-symmetric** and
   its 12 ρ²-fixed masks are exactly the (x0^x2)/(x1^x3) sharing trick, **rediscovered by
   search, not imposed**; Jean's 88 is 75 % ρ²-symmetric — a second, distinct symmetric
   basin. All five 88s were found in **walk** chunks, none in an LNS chunk; both
   from-scratch ones came from `alt` workers ~19 h into a restart. *Descent is not what
   produces an 88; lateral motion plus a depth tie-break is,* and crossing beats editing.

**The counterweights that must ship with all of the above:**

- The same structural properties hold for **97@3, 92@4 and 89@5** — they are facts about
  MixColumns SLPs in this basis, **not a signature of the 88 plateau** (`fleet1_4` L8).
- Every "88 is the class optimum" statement is **class-conditional**; the class's own
  load-bearing assumption (lane A's wiring condition, flag F3) is **measured on 22 circuits
  with one exception and never proved**; and the block-strata evidence is a 14-for-14
  regularity among **88**-gate circuits — *exactly the population that would look regular
  if 87 lived somewhere else* (`fleet5_8` L7).
- All of the block reasoning lives inside a **block partition that was never measured on
  any circuit** (defect D22, LIVE) — and `91@6` gate 70 is an existing circuit no fleet8
  block can represent. **An 87 that crosses a block boundary is exactly as possible today
  as it was before fleet12 started** (`fleet9_12`).
- The "22 + 5 backbone" story is **falsified** and must never appear in a public structural
  claim (→ `CORRECTIONS.md` C-37).
- Two-mode structure in the optimum landscape is **unexplained**: cone-ILS restarts give
  `{88: 15537, 89: 2270, 90: 2529, 91: 3907, 92: 2548, 93: 1578}` — 88 hit **6.8× more
  often than 89**, non-monotone with a trough between two piles at 91 and 88 — while
  fresh_fleet's endpoint law has its own mode at 90. No document addresses it
  (`campaign_87` L5).
- The `d(S)=1` cost driver is unexplained: **a 6–9× spread at identical depth** (F1 at
  depth 7 has 563,008 windows against 58,872 and 99,923 for two population depth-7
  circuits). Depth was ruled out twice as the driver (`experiments_late` L17).

---

# C. GUARDRAILS — routes with proved ceilings (do not fund expecting more)

Surfaced together because each kills a plan someone would otherwise pay for.

1. **Route ceiling 83** — no Lagrangian certificate of the residual family can push
   `κ + Y + B(A*)` above **83.000** on `88@5fs`, referee-confirmed in exact rationals. The
   program needs an *integral* residual bound as well as the span-cone lemma, and
   `PROGRAM_STATE.md` names only the latter. (`fleet1_4` L9a)
2. **No quotient-composition theorem exists** — for `W1 ∩ W2 = 0` the pair map is
   injective, so the joint relaxation **is** the original problem. (`fleet1_4` L9b)
3. **Tower rungs are capped below the refereed 56** (51 at level 3, 26 at level 2), so
   exact `L2`/`L3` cannot improve `L(M)` at all. (`fleet1_4` L9c)
4. **Lane C's arithmetic erratum** — the predecessor's "next purchase `k(6)` at `|K| = 15`,
   expected value +1" is **wrong by its own formula** (`1 + 17 + 32 + 6 = 56`, no gain); the
   real route costs pod-months at low probability. (`fleet1_4` L9)
5. **The exchange-rate / `G_int` family dies at `kappa ≥ 22`**, below the records' own
   `kappa = 18..28` — laneUNCOND's ceiling applies to `G_int` verbatim. (`fleet5_8` L6)
6. **The certificate LP is capped at 91.4098776 exactly**, proven below both upgrade
   thresholds — that whole family of arguments cannot buy the next step. (`records_repo`
   staleness §3, e17)
7. **The ≥5-plane tier is unbuildable, not merely unused** — buildable rate 0.0000 at
   p = 5..8; 0 of 7,755 offered masks ever selected across 89,003 floors. Do not fund a
   ≥5-plane search on the strength of Tier-2 #13, which is about 3 → 4. (`campaign_87` L2)
8. **Radius ≤ 4 negatives are worth ~nothing** — the standing caveat at the top of this
   file. Do not fund more k ≤ 3 shell completion.
9. **The dim-10 `cf = 13` control cannot be bought more cheaply than the question**
   (38 CPU-hours either way) — *"at dim 10, 'measure the control first' cannot be
   satisfied."* An honest structural limit worth stating publicly. (`experiments_late` L6)
10. **`d(S)=1` on F3 and F7 is UNCLOSABLE at any budget this project had** — F3 reached
    10 of 88 bases with 3,000,000 windows against a ~2.7e7 space; F7 reached 41 of 88.
    (`experiments_late` L17)

---

# Appendix A — CLOSED / WITHDRAWN (do not re-run)

Every lead dropped from the ranked register, with its closure citation. Nothing is
dropped silently.

## A.1 — The eight atlas "unfinished" items, closed downstream
Source: `atlas_misc` §5 closure table (checked against `fleet*/` and `experiments/`).

| Atlas item | Closure |
|---|---|
| Sector-block re-optimisation (`basin/b9b_*`), incl. *"88@6 S2 in 8 gates = an 87 outright"* | **CLOSED** by `experiments/e7_push/`: 70 of 112 blocks decided exactly optimal with a live control, **0 hits**; 3 of the atlas run's 23 negatives were vacuous and are corrected in `experiments/e7_push/ATLAS_NOTE.md` (the correction was never pasted into atlas → `CORRECTIONS.md` C-16) |
| `bwd9.py` two-step hop (coded in atlas, never run there) | **RUN** in `fleet1/laneD_completions/` (`bwd_frontier_bwd9.log`, `ledger_bwd9.jsonl`) |
| V1.5 corpus completion → theorem-grade class bound | **CLOSED NEGATIVE** by `fleet1/laneD_completions/`: the optimist shortcut returns **58**, and the flat-floor family is refuted by the 553 measured σ=6 cells |
| Width-5/6 σ entries; V2 region pricing | picked up in `fleet1/laneA_v2pricing/`, `fleet1/laneB_regionbounds/` |
| Skeleton-anchored / `l = 51` | picked up in `fleet1/laneC_proofside/` |
| R56 landmark and its wrong `compare_to` | picked up in `fleet12/laneAUDIT/`, `experiments/e15_campaign3/` |
| `C_c` conjecture | **CLOSED** by identity (e17 campaign) |
| `phase2_alt` disjoint-basin sweeps | referenced and superseded in `fleet1/laneD_completions/RESULT.md` |

## A.2 — Other closures

| Lead | Closure citation |
|---|---|
| `new-representation.md` §59's **1,291 pairwise-edge-free backbone triples** | **CLOSED**: `atlas/thinktank/phase2_finisher.md` — *"All 1,540 = C(22,3) backbone triples of this geometry are dead"* (1,540 at one plane state, 2,916 tier-1 across all 243 plane states, 4,941 tier-2); `FLEET_PLAN.md` design law 2 cites it as settled; `atlas/thinktank/enabling_gates.md:198` discusses the 1,291 directly. (`root_infra` L5) |
| `side_work_REVIEW.md` rec. 1 — put `t = 1 + y⁻¹` into `atlas/ring.py` | **FOLLOWED UP** in `atlas/thinktank/transposed/tring.py` + `transposed_frame.md`, and `experiments/e14_plateau87/basis/zframe_T.py` + `laneBASIS.md`. (Whether the vanishing `t²` shrank any table is unverified.) (`root_infra` L5) |
| fleet8's **cost-2 shared-plane family** as a route to 87 | **CLOSED NEGATIVE**: `fleet12/laneKNOBS/RESULT.md` §6 costed it — the derive-nominated `D37` **prices 89**; the consumer saves a gate and the supplier pays it back. The floors genuinely moved (8 → 6/7/7) but there is no 87. (`fleet5_8` L1) |
| `MB27B373 ∈ [12,13]` — the last undecided in-class 87 lead | **CLOSED**: `fleet6/door/logs/door.out` line 5, `[sat] k=12: UNSAT (19458.32 s)`, with the inherited replay bound 13 ⇒ **MB27B373 = 13 exactly**; forecloses the branch where 12 would have priced the class at 87. (`fleet5_8` L4) |
| The two-gate saving on `merged(W3 ∪ U4)` | **CLOSED**: k = 9..13 all exhaustively UNSAT ⇒ `merged ≥ 14`, and with the replay bound `merged ∈ {14,15}`. **The remaining one-gate question (k = 14) is also CLOSED as of 2026-09-01: UNSAT**, by one monolithic kissat-4.0.4 solve (356,321.63 core-s ≈ 99 core-h) — `merged(W3 ∪ U4) = 15` exactly, merging buys nothing, and **no 87 exists that shares the block structure of every known 88** (`fleet11/laneCUBE/RESULT.md` §7.1). ⚠ Not a proof that no 87 exists — an 87 outside that block decomposition is not excluded. (`fleet5_8` L2) |
| E5's drop-4 screen on `88fs5` "left running" | **COMPLETED**: 35,960 four-target drop sets refuted at `k = W−1`, zero improvements, zero timeouts → the project holds **two** complete drop-4 certificates, not one. (`experiments_early` L1) |
| E3a's `buyone` / `blockpop` / `k3shell` "still accumulating" | **COMPLETED EMPTY**: 4,926 `buyone` rows all `UNSAT_at_nB_minus_2`, 0 hits; 586 decided blocks, 0 HIT; and **two complete exhaustive remove-3-add-2 certificates** banked (88@7 and 88fs, 27,720 windows each). (`experiments_early` L3) |
| E7's dim-12 tap-region queue "84 of 231 cubes done" | **COMPLETED**: four regions decided at `min_gates = 11` with positive controls (88@5 R4, 88@5fs R4, **JEAN88 R4**, p88_05 R3). Six `|B| = 11` regions remain → ranked at #40. (`experiments_early` L2) |
| The k=2 / k=3 population and residue frontiers listed as resumable in `CERTIFICATES.md` and `FACTS.md` | **ALREADY FINISHED** in the unreported `agents/frontier-exact/`: 84,989 + 987 rows all `irreducible_k2`; k=3 queue empty (200/200 `irreducible_k3`). Do not re-run. → `CORRECTIONS.md` C-11. (`campaign_87` L11, superseding `root_infra` L7's "33,090 states left, ~2.9 h") |
| lane F4's `W3_noshare` "≥ 10 PROVEN, exact UNDECIDED" | **LANDED at 11 EXACT** (`results/cache.jsonl`, wall 33,876.6 s, `verified=true`), and lane G's parallel `U3` solve landed at **10 exact**. The lane's "both ingredients are needed" is refuted by its own late solve. → `CORRECTIONS.md` C-17. (`fleet1_4` L3) |
| lane B's `R01 ≥ 15` "k=14 in flight" | **LANDED UNSAT** (1008/1008 cubes, 484,560.6 CPU-s). The *k = 15* level remains open → ranked at #19. (`fleet1_4` L1) |
| The Y-lemma route | **CLOSED by self-defeat** (e17 campaign; project memory) |
| The `wave6/hp_strike` shape hypothesis (*"windows at n = 12,13,14 with `\|req\|/n ≥ 0.85` should decide FAST"*) | **REFUTED by its own lane** — 8/8 timeouts at n = 14 with passing controls, against a pre-registered decision rule. The STATUS still records it CONFIRMED → `CORRECTIONS.md` C-26. (`campaign_87` L12) |
| The `PLANE_CAP = 8` patch for the ≥5-plane blind spot | **APPLIED AND MEASURED INEFFECTIVE** within 24 h: `hp_patchcheck.py` shows `clean_and_repair` deletes two thirds (324 proposed → 107 surviving, 0.69 % of pool content), i.e. the patch draws exactly the unbuildable kind. The scoreboard still lists ≥5-plane as an open frontier → `CORRECTIONS.md` C-33. (`campaign_87` L9) |
| The `δ` linear-invariant lower-bound route (`δ(m) = hi(m) ⊕ lo(m)`) | **CLOSED BY ONE MEASUREMENT, no solver time**: a verified greedy witness gives `SLPmin₁₆ ≤ 26`, so `2·SLPmin₁₆ + 1` can never certify more than ≈53 against the 89 it would have to decide. Logged as `kind: route_closed`. *The pattern — compute an upper bound on your prospective lower bound before building the machinery — is worth copying.* (`experiments_early` L15) |
| E5's three bounded-but-unpinned orbit values (`[10,16]`, `[9,15]`, `[9,13]`) | **NOTHING DEPENDS ON THEM** — their 87 questions are all closed. Recorded only so the timeouts are not mistaken for refutations. (`experiments_early` L12) |
| The δ(mc) = 2 neighbourhood anomaly | **CLOSED as circular** ("no 87 was found by this move, counted twice"), with a standing instruction *do not cite δ(mc)=2 as evidence*. (e17 laneDELTA; `records_repo` §3D) |
| The forcedness hypothesis at small scale | **REFUTED** (e16; project memory) |
| The 536 anomaly | **DISSOLVED** — identity artifact (e16 lane536; project memory) |
| 2-mint / 3-orphan | **CLOSED** at single sites (e16 lane536) — but *not* as a connected move set, which is ranked at #20. |

---

# Appendix B — leads reclassified as stale-figure fixes

These arrived in the reports' LEADS sections but are corrections, not investigations.
All are registered in `wrapup/CORRECTIONS.md` with document paths and correct figures:

`fleet9_12` L1 (laneCUBE 51 → 87/528), L2 (fleet9's 72 post-writeup rows), L3 (laneF1's
13 late rows), L4 (LIBRARY.md open-axes count), L5 (fleet10 undocumented);
`fleet5_8` L1 (fleet8 floors + STATE_OF_THE_PROBLEM §5.3), L2 (joint verdict never
written back), L4 (MB27B373), L5 (20 untabulated partial bounds);
`fleet1_4` L2 (basin rigidity headline), L3 (W3_noshare attribution), L11 (records
update note);
`campaign_87` L1 (LR ≈ 1.00 repricing), L8 (unrecorded B=16/17 UNSATs and the n=12
splice frontier), L11 (139,878), L12, L15 (seven separate contradictions), L16
(wall-clock contamination), L18 (misleading small artifacts);
`experiments_early` L1, L2, L3, L5, L6, L7 (coverage table), L8 (E6's lost artifact);
`experiments_late` L8 (A11 recount), L9 (A10 table-contingency), L16 (reducible non-88s
on disk), L20 (e16 has no RESULT.md);
`beat88` L8 (22+5 falsified), L13 (possible pod1 data gap), L14 (census inbox), L15
(bound provenance), U-8 caveat (1–2 worker UNKNOWNs), U-16 (four population counts),
U-18 (QUARANTINE path);
`records_repo` L1, L3, L4, L8 + the whole §3A staleness audit;
`root_infra` L1 (unpushed commit), L4 (stale depth-4), L10 (hunt87 anchors).
