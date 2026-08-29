# DELETION LOG — Tier 1 execution

Executor: CLEANUP agent. Scope: **TIER 1 ONLY** of `wrapup/KEEP_DELETE.md`, as approved by the user.
Tier 2 and Tier 3 are NOT approved and were not touched.

## Baseline — 2026-08-29T10:21:40-04:00

```
$ df -h .
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdd       1007G  638G  318G  67% /
```

Top-level `du -sh` (pod_salvage excluded from the beat88 figure to keep the scan cheap):

```
29G   campaign_87        1.3G  atlas          18M  fleet2      4.0M  fleet5
9.4G  beat88 (-pods)     787M  wrapup         15M  fleet1      3.3M  fleet9
379M  experiments        5.5M  fleet12        11M  fleet3      3.1M  fleet8
4.9M  evidence           2.3M  pipeline      880K  fleet11    832K  fleet10
2.2M  fleet7             628K  fleet4        584K  fleet6     404K  bi_mask_requested_evidence
```

Live processes re-verified at start: 4x `mono.py 14` (333371, 345293/5/7) and
1+15 `cube16.py` (443496, 443570-443584), all in `fleet11/laneCUBE`. Untouched.
No signal was ever sent to any process during this pass.

## Actions

### 1.1 campaign_87 — CNF dumps (solver input)

`2026-08-29T10:2x` — Scoped to the named directories only, per C16 (never a repo-wide
`find -name '*.cnf' -delete`; `experiments/sat_package/**/*.cnf` is SHA-pinned). Within each
directory only `*.cnf` was matched — these dirs also hold `.spec.json` instance specs and
solver `.out` logs, which were **kept** (logs are TIER 3 compress-not-delete, §3.4).

| path | before | .cnf deleted | action |
|---|---|---|---|
| `campaign_87/wave5_2026-08-04/burn/simple/execute/cnf` | 3.3 G | 69 files / 3303 MB | DELETED |
| `campaign_87/wave5_2026-08-04/alphabet_ladder/cnf` | 1.5 G | 86 files / 1496 MB | DELETED (100 `.spec.json` kept) |
| `campaign_87/wave5_2026-08-04/metareview/optimality/cnf` | 327 M | 16 files / 326 MB | DELETED (16 `.spec.json` kept) |
| `campaign_87/wave6_2026-08-11/sat_boost/cnf` | 28 M | 8 files / 27 MB | DELETED (`.icnf` cube file + specs kept) |
| `campaign_87/wave6_2026-08-11/band_hunt/cnf` | 25 M | 26 files / 24 MB | DELETED (26 `.out` kept) |
| `campaign_87/hunt87_depth4/runs/cnf` | 18 M | 12 files / 16 MB | DELETED (12 `.out` kept) |
| `campaign_87/d3_sat/runs/cnf` | 125 M | **0 files** | **SKIPPED** — content mismatch |

**SKIPPED `d3_sat/runs/cnf` (125 M):** the proposal calls it a CNF dump; it contains **zero**
`.cnf` files. All 41 files are solver `.out` logs (`lad_k18_r2_B64_ctl.out`, `split_B64_n1_19.out`, …).
Per procedure rule 4 (content does not match description) and §3.4 (campaign_87 logs are
TIER 3 — "compression would be reasonable; deletion would not"), it was left alone.

**Also skipped:** the "remainder" of the CNF row. 10 further `cnf/` directories exist in
campaign_87 (`wave6/xor_encoding`, `skeleton_pools`, `pattern_class`, `hp_strike`,
`agents/frontier-sat`, `agents/family3-sat`, `agents/frontier-d6sat`, `band_hunt/scratch`,
`frontier-sat/kissat/test` (symlinked `hard.cnf`, D12), `burn/oddparity`). None is named in the
proposal, and C16 forbids widening the pattern. Not touched.

**Reclaimed: 5.07 GB** (proposal claimed 5.53 GB for this row incl. d3_sat + remainder).

### 1.1 campaign_87 — venvs and vendored builds

| path | size | action |
|---|---|---|
| `wave5_2026-08-04/lp_closure/build/abc` | 595 M | DELETED (commit banked below) |
| `wave5_2026-08-04/lp_closure/build/mockturtle` | 87 M | DELETED (commit banked below) |
| `agents/lit-88/venv` | 210 M | DELETED |
| `agents/frontier-sat/venv` | 35 M | DELETED |
| `agents/family3-sat/venv` | 35 M | DELETED |
| `agents/sat-deep/venv` | 35 M | DELETED |
| `agents/loose-sat/venv` | 35 M | DELETED |
| `wave6_2026-08-11/sat_boost/tools` (CnC, cms, march-sat) | 20 M | DELETED |
| `agents/sat-window/venv` | 108 M | **SKIPPED** — not in the proposal |
| `agents/exact-k4/tools` | 187 M | **NOT TOUCHED** — C1 carve-out, DO-NOT-TOUCH D11 |
| `agents/loose-sat/kissat/` | — | **NOT TOUCHED** — C2 carve-out, D12 symlink target |

**Correction to the proposal — provenance banked here.** The proposal justified deleting the
ABC and mockturtle trees with *"commits recorded in `clone_abc.log` / `clone_mt.log`"*. Those
logs are 37 and 43 bytes and contain only `Cloning into 'abc'... / ABC CLONE RC=0` — **no commit,
no tag, no version.** Both trees were clean checkouts (`git status --porcelain` → 0 paths), so the
identifiers were recovered from their `.git` before deletion and are recorded here, which is what
makes this row genuinely zero-information-loss:

```
abc         https://github.com/berkeley-abc/abc.git
            8e224cd794a10e578d6dc3ee76e504c5c3edbdbe  2026-08-01T15:27:17-07:00
            "Update mapped delay computation."
mockturtle  https://github.com/lsils/mockturtle.git
            852605f5ad0f8f4c90b6e1dc8cabff11e0a3c75e  2026-08-07T18:38:06+08:00
            "fix: the bug of genlib_reader parser (#698)"
rebuild:    git clone <origin> && git -C <dir> checkout <sha>
```

`build/{clone_abc.log,clone_mt.log,pip_cmake.log,mt_linsyn/}` were kept.

**SKIPPED `agents/sat-window/venv` (108 M):** the proposal enumerates "`lit-88/venv` 210 M + 4
further venvs ~35 M each" — arithmetic that accounts for five venvs, not six. sat-window's venv is
the only one carrying `z3` in addition to `pysat`, i.e. it is not the same object as the four. Not
named, so not deleted (procedure rule 4).

The five deleted venvs were verified to contain only `pysat`+`six` (four of them, byte-for-byte the
same package set) and a scraping stack (`playwright`/`requests`/`rich`) for `lit-88` — one `pip install`
each. `agents/{loose-sat,family3-sat}/runs/` — which hold the 4 + 20 undecided SAT windows of D20 —
were **not** touched; only their interpreters went. The cross-agent symlink of D12 was re-verified to
resolve after the pass.

**Reclaimed: 1.03 GB.**

### 1.1 campaign_87 — remaining TIER 1 rows

| item | path | size | action |
|---|---|---|---|
| `.npy` posting index | `wave5_2026-08-04/alphabet_ladder/work/corpus_index/post.npy` | 400 M | DELETED (`offs/sizes/vocab.npy` kept) |
| plane-census re-scan | `wave6_2026-08-11/discriminate/runs/hiplane_states_{0..3}.jsonl` | 539 M | DELETED (6 `verify88_*.json` kept) |
| window enumeration | `wave6_2026-08-11/hp_strike/runs/windows.jsonl` | 85 M | DELETED |
| window enumeration | `wave6_2026-08-11/band_hunt/runs/windows_splice{,2,_all}.jsonl` | 56 M | DELETED |
| per-window scratch | `wave6_2026-08-11/pattern_class/runs/tmp_D{0,1}/` — 20,800 files | 84 M | DELETED |
| `.dist.jsonl` telemetry | `d3_model/harvest/{lns97,lnslib,smoke_lns,walk97,walklib}.dist.jsonl` | 114 M | DELETED (3 `.pop.jsonl` kept) |
| byte-verified duplicate | `wave6_2026-08-11/lower_bound/branch_certificates.json` | 5.0 M | DELETED |
| byte-verified duplicate | `wave6_2026-08-11/lower_bound/branch_summary.json` | 6.5 K | DELETED |
| `__pycache__` | campaign-wide, 110 dirs | 7.4 M | DELETED |
| claimed duplicate | `wave6_2026-08-11/pattern_class/runs/diverse88_shuf.jsonl` | 22 M | **SKIPPED** — not a duplicate |

**Verification notes.**

- `tmp_D{0,1}`: the proposal says these are "superseded by `ledger.jsonl`". No `ledger.jsonl` exists in
  `pattern_class/runs/`, but the lane's ledger is one level up at `pattern_class/ledger.jsonl`
  (1,616,944 B, mtime 2026-08-12 04:26 — *later* than the scratch it supersedes). Confirmed present
  before deleting. Counted 20,800 files, not the 21,076 quoted; 84 M, not ~50 M — inside the 2x bound.
- `.dist.jsonl`: re-confirmed no reader. `grep -rln 'dist\.jsonl' --include='*.py' --include='*.sh'` over
  the whole repo returns only `wrapup/` prose. The `.pop.jsonl` siblings were not globbed.
- `branch_certificates.json` / `branch_summary.json`: `cmp` re-run this session — both **byte-identical**
  to their `_E18_48` snapshots, which `THEOREM.md` names as the preserved copies and which survive.
  Only the un-suffixed (re-run-overwritable, §6 H6) copies went.
- `__pycache__`: the proposal counted 722 dirs / 66 M campaign-wide. Most of that mass was inside the
  venv and vendored trees already removed in the row above; 110 dirs / 7.4 M remained and were swept.
  Excluded from the sweep: `agents/exact-k4/tools/` (PyPy, D11) and `agents/sat-window/venv/` — 104
  `__pycache__` dirs inside those were left untouched.

**SKIPPED `diverse88_shuf.jsonl` (22 M) — the proposal's claim is incorrect.** It is listed under
"byte-verified duplicates … `cmp`-confirmed byte-identical by the slice agent". It is not:

```
diverse88.jsonl       5b7a2e1f270427ead16cc776085ab42d2b7e1c2f10e64e5880f13c3f02a3e000
diverse88_shuf.jsonl  adf8d7ffa102359458a0d4b25c33a26a7618e0639f4afa22b492982421e26473
```

Same length (22,096,547 B both), different bytes — which is exactly what a *shuffle* is. The two
`branch_*` pairs in the same row really are identical, so the slice agent's `cmp` result appears to
have been carried across rows. A shuffled work list's **ordering can be load-bearing** (it determines
which items a truncated run processed), so this was left in place. Not a byte-duplicate ⇒ not TIER 1.

**Post-pass safety checks:** all 11 campaign_87 STOP sentinels present; all five D20 certificate
frontiers present at full size; the D12 symlink resolves; `agents/exact-k4/tools` at 187 M.

**campaign_87: 29 G → 21 G. Reclaimed in this slice: ~8.0 GB.**

### 1.2 beat88 (100 % untracked — every deletion here is permanent, D19)

No `.md`, `.py`, certificate or export file was deleted anywhere in beat88. The D19 recommendation
to commit/copy the prose layer off the box first was **not performed** (out of scope for this pass);
it remains outstanding, and this pass was confined to formats that cannot carry prose.

| item | size | action |
|---|---|---|
| 113 byte-identical `.nohup` copies | **1.61 G** | DELETED |
| 8 differing `.nohup` + 4 orphans | — | KEPT (listed below) |
| `u2_walls/data/{census,u4_gates,cuts,cuts_typed}.jsonl` | 289 M | DELETED (C7 precondition checked) |
| `analysis/scratch/**/*.pop.jsonl` — 9 files | 64 M | DELETED |
| `analysis/scratch/relax-depth/*.pkl` — 5 files | 3.2 M | DELETED |
| `u4_economy/prof.jsonl` | 8.3 M | DELETED |
| `**/__pycache__/` — 44 dirs | 2.4 M | DELETED |
| `**/*.stale` — 26 files | 40 K | DELETED |
| `methods/shared/lib/libslpkernel.so` | 29 K | DELETED |
| `u4_economy/sw_rows.jsonl` | 9.0 M | **SKIPPED** — no producer found |
| `u1_obligations/identity_rows.jsonl` + retracted lanes' logs | ~0.5 M | **SKIPPED** — NOTEBOOK says keep |
| `analysis/scratch` `.log`/`.out`/`.stdout`/`.err` — 88 files | ~80 K | **SKIPPED** — nil reclaim |
| `analysis/scratch/exact-repair/m7_out_*.pkl` | 13 K | **SKIPPED** — a result, not work state |

**`.nohup` verification.** Every pair was re-`cmp`'d this session rather than trusted: 113 identical,
8 differing, 4 with no `.log` partner — reproducing the slice agent's split exactly. Only the 113
identical were removed. Kept:

```
DIFFER  m3_census/runs/local_prev/{m3d4,m3g,m3b}.nohup
DIFFER  m3_census/runs/local/{local_f91c_11,local_rbasis_4,local_f91a_3,local_xown_10,local_f91b_7}.nohup
ORPHAN  m3_census/runs/{local_prev,local}/shipper.nohup
ORPHAN  pod_salvage/pod{1,2}/beat88/methods/m3_census/runs/pod{1,2}/shipper.nohup
```
The 8 differing pairs were **never diffed** (the proposal's own GAP 4) and still have not been.

**C7 sequencing, discharged.** `u2_walls/data/*` was deleted only after confirming its regeneration
source survives: `methods/m2_oracle/runs/` = 263 M, 65 files, present and on the KEEP list; the
rebuilder `u2_walls/code/build_dataset.py` present; and `data/.gitignore` itself declares the four
files derived ("rebuildable from m2_oracle/runs … ~30 s"). The `.gitignore` was preserved, so the
declaration outlives the data. The other 18 files in `data/` (collision, factored, lambda, repair,
why_collide, `u4_gates.txt`, …) were not touched.

**SKIPPED `sw_rows.jsonl` (9.0 M).** The proposal calls it "regenerable by the exact commands in
`u4_economy/NOTEBOOK.md` §8". `grep -rl sw_rows --include='*.py' --include='*.sh' --include='*.md'` over
**all of beat88** returns nothing — the string does not occur in any script or notebook. Its sibling
`prof.jsonl` *is* documented (`profile.py corpus.txt prof.jsonl`) and was deleted. With no producer
on disk and beat88 untracked, `sw_rows.jsonl` is not reproducible and so is not TIER 1.

**SKIPPED `u1_obligations` (~0.5 M).** `u1_obligations/NOTEBOOK.md:1222` reads *"RETRACTED PROGRAMS
(kept for the record, do not cite their logs)"*. The tree's own instruction is to keep the logs and
not cite them — the opposite of deleting them. Half a megabyte does not buy overriding that.

`libslpkernel.so` was deleted only after verifying `kernel.py:44-46` rebuilds it when missing or
older than `csrc/slp_kernel.c`, that `csrc/{build.sh,slp_kernel.c}` are present, and that `gcc` exists.
`csrc/` was not touched.

**beat88 reclaimed: ~1.97 GB.**

### 1.3 atlas + misc

| item | size | action |
|---|---|---|
| `atlas/m1_v15_results/` — 34,112 files | **135 M** | DELETED |
| `atlas/**/__pycache__/` — 14 dirs | 760 K | DELETED |
| `bi_mask_requested_evidence/**/*:Zone.Identifier` — 36 files | 144 K | DELETED |
| `d3_b.out` (repo root) | 123 B | DELETED |
| `atlas/userscheme_pricing.log` | 0 B | **SKIPPED** — D31 |

**`m1_v15_results` — verified in full, not sampled.** This deletion makes `atlas/v15_partial.tgz`
(1,853,913 B) the sole copy (D22/D34), so the slice agent's two-file SHA sample was not relied on.
The tarball was extracted to scratch and compared with `diff -r` across the **entire** tree:
34,112 files on each side, **0 differing** (`diff` exit 0, empty output). The tarball was left in
place and re-stat'd afterwards. Its expansion is fully recoverable with `tar xzf`.

**`*:Zone.Identifier`** — re-confirmed absent from the manifest (`grep -c Zone.Identifier
SHA256SUMS.txt` → 0) before deleting. `sha256sum -c SHA256SUMS.txt` was run **before and after**:
35/35 OK both times, zero failures. The hash-manifested bundle of D34/§3.4 is intact.

**SKIPPED `atlas/userscheme_pricing.log` (0 B) — internal contradiction in the proposal.** §1.3 lists
it as a TIER 1 "empty log"; **D31 names this exact file** as one of the zero-byte files that *are*
evidence and must survive a tidy-up. DO-NOT-TOUCH outranks TIER 1, C17 says never sweep by size, and
the hard exclusions for this pass forbid deleting empty files. Kept. Reclaim forgone: 0 bytes.

**atlas: 1.3 G → 1.2 G. Reclaimed: ~136 MB.**

### 1.4 experiments

| item | size | action |
|---|---|---|
| `__pycache__` — 29 dirs (e1–e17) | 1008 K | DELETED |
| `e15_campaign3/RUN_B.log` | 143 B | DELETED |
| `e3a_exploit/inst/` — 5,705 files | **23 M** | **SKIPPED** — C20 not dischargeable |
| `e15_campaign3/.start.lock` | 0 B | **SKIPPED** — empty-file exclusion |
| `e15_campaign3/.slot_guard_restarts` | 22 B | **SKIPPED** — resume input |
| `e2_outputcost/kill_manifest.txt` | 4.5 K | **SKIPPED** — proposal offers KEEP |

`RUN_B.log` was deleted as the same object as `d3_b.out`: a one-line `[Errno 2]` for a script that
does not exist (`e15_campaign3/fprun.py`, which belongs to e16). C14/C15 resolve that class as
deletable. `experiments/sat_package/` was excluded from the `__pycache__` sweep by path (it holds
none anyway); its `SHA256SUMS` re-verifies **51/51 OK** after the pass.

**SKIPPED `e3a_exploit/inst/` (23 M) — C20's condition was checked and only half of it clears.**

1. *Which files does `nat_hits.json` name?* — **Clear.** `e17_pure/laneDELTA/nat_hits.json` contains
   exactly 2 references to e3a, both to `e3a_exploit/found`, **none to `inst/`**. No dangling citation
   would be created.
2. *Is it actually regenerable?* — **No, not as described.** C20 flags that regenerability was
   "inferred from naming, not regeneration-tested". Reading `code/blocks.py` settles it: `ask()`
   (line ~96) writes `inst/<tag>.json` and **in the same function immediately shells out to
   `slp_opt.py --cores N --timeout T`**. There is no instance-only mode and no `--emit` flag; the
   instances are a side effect of the search. "Regenerating" them means re-running the whole E3a
   solver campaign — thousands of optimizer invocations — not "one command".

That call would also be actively unsafe right now: `blocks.py` uses
`subprocess.run(capture_output=True, timeout=…)` against `atlas/slp_opt.py`, which is the exact
combination `FROZEN_AND_FRAGILE.md` records as **hanging forever** (grandchildren hold the pipe), and
`slp_opt.py` defaults to **all cores** while 20 solver processes are live. So the regeneration could
not be tested without endangering the k=14 solve, and an untested regeneration claim is not TIER 1.
23 MB of solver input left in place; the decision is cheap to revisit once the box is idle.

D21 resumable state re-verified untouched: `e7_push/cubes/` 21 `.jsonl`, `e11_quad10` shard,
`e15_campaign3/sample500.txt`. The e16 F-point bank (224 M) is TIER 3 and was not touched.

**experiments: 379 M → 378 M. Reclaimed: ~1 MB.**

### 1.5–1.7 fleet1–fleet12

| item | size | action |
|---|---|---|
| `__pycache__` — 19 dirs, fleet1–fleet4 | 808 K | DELETED |
| `fleet2/laneP_proof/ledger.jsonl.prev` | 24 K | DELETED |
| `fleet1/laneC_proofside/_tmp_inst.txt` | 35 B | DELETED |
| `__pycache__` — 7 dirs, fleet5/6/7 | ~320 K | DELETED |
| `__pycache__` — 4 dirs, fleet9 (x3) + fleet12/laneF1 | ~216 K | DELETED |
| `fleet8/unified/__pycache__`, `fleet8/unified/code/__pycache__` | 236 K | **SKIPPED** — C10 + hard exclusion |
| `fleet11/laneCUBE/code/__pycache__` (3 `.pyc`) | 36 K | **SKIPPED** — live process |
| `fleet10/cleanroom/work/{bp,bp2,bp3,bp4,bp5,bp5s}` | 143 K | **SKIPPED** — not regenerable as claimed |
| `fleet10/cleanroom/work/migrate{,2,3}.log` | 0 B | **SKIPPED** — D31/C17, and the emptiness *is* the result |
| `fleet8/unified/code/*.{bak,prelive}` | 58 K | **NOT A TIER 1 ITEM** — withdrawn by C9 |

`ledger.jsonl.prev` was deleted only after confirming its regenerator `laneP_proof/code/mkledger.py`
is present **and** that both D26 ledgers survive untouched — `verify1/ledger.jsonl` (1,866,304 B) and
the refereed `referee/results/verify1_ledger_snapshot_20260820.jsonl` (1,859,789 B). The two were not
compared, deduplicated or reformatted. `_tmp_inst.txt` went with `l2_inst.txt` (97 B) confirmed present.

**SKIPPED the six cleanroom binaries (143 K) — the stated regeneration is not available.** The proposal
says "regenerable from the `.c` sources beside them with a one-line `gcc`". Three problems, checked:
there are **five** `.c` files and **six** binaries — **`bp5s` has no source** and is not mentioned in any
script or document in the tree; `grep -rn 'gcc\|cc -O'` across every `.sh`/`.md`/`.txt` in `cleanroom/`
returns **nothing**, so no compile flags are recorded for any of the six; and D29 states `fleet10/cleanroom/`
is the only clean-room calibration in the repo, has **no writeup**, and "needs a `RESULT.md` written
*before* anyone considers pruning it" — confirmed, there is no `.md` in `cleanroom/`. 143 KB is not worth
spending the "93 from scratch" datum's only build artefacts on.

### 1.8 repo root / infra

| item | size | action |
|---|---|---|
| `__pycache__` ×5 + `.pytest_cache` (root, `tests/`, `docs/`, `pipeline/`, `reproduce/`) | 660 K | DELETED |
| `w1.nohup`, `wshB1.log`, `wshB2.log`, `wshC1.log`, `wshC2.log` | 537 B | DELETED (C14) |
| `d3_b.out` | 123 B | DELETED (logged in §1.3; C15 — counted once) |

Each of the five root logs was **read** before deletion, not matched by name (C14/GAP 9 warns they must
not be assumed to be copies of fleet10's identically-named files). Contents: `w1.nohup` = `bash: worker.sh:
No such file or directory`; `wshB{1,2}.log` = `[Errno 2]` for `satfix_hunt.py`; `wshC{1,2}.log` = same for
`satfix_hunt2.py`. All dead one-liners for scripts that do not exist. `fleet10/cleanroom/work/wsh*.log`
were left untouched and are visibly different objects (1,183–2,176 B vs 123–124 B), as GAP 9 says.

No `certificates/code/__pycache__` exists; the proposal's count of 7 resolved to 6 on disk.

### 1.9 `~/xor_ui/aes_mc_records` — **SKIPPED IN FULL**

258 KB (`__pycache__` ×5, `.pytest_cache/`, `verilog/sim.vvp`). The records repo is a **hard exclusion**
for this pass regardless of tier, so `git clean -Xd` was not run. Verified untouched afterwards: working
tree clean, the single unpushed commit `73ad7ee` still present, 5 `__pycache__` dirs still in place.

---

## Final state — 2026-08-29

```
$ df -h .   (before / after)
/dev/sdd  1007G  638G used  318G avail  67%   <- before
/dev/sdd  1007G  629G used  328G avail  66%   <- after
```

| directory | before | after | reclaimed |
|---|---|---|---|
| `campaign_87/` | 29 G | **21 G** | ~8.0 GB |
| `beat88/` | 47 G | **45 G** | ~2.0 GB |
| `atlas/` | 1.3 G | **1.2 G** | ~136 MB |
| `experiments/` | 379 M | **378 M** | ~1 MB |
| `fleet1`–`fleet12` | 44.6 M + 9.8 M + 10.5 M | unchanged to the MB | ~1.4 MB |
| repo root | 7.5 M | — | ~660 KB |
| **repo total** | **77 G** | **69 G** | **≈ 10.2 GB** |

### Post-pass safety verification (all green)

| check | result |
|---|---|
| 4 x `mono.py 14` + 16 x `cube16.py` still running | **20 processes, uninterrupted** (3d 04h / 2d 14h) |
| signals sent to any process | **none** — no `pkill`, no `kill`, no `experiments/STOP` |
| STOP sentinels (D9) | **18/18 present** |
| broken symlinks repo-wide | **0** |
| D12 cross-agent symlink | resolves to `loose-sat/kissat/makefile` |
| `experiments/sat_package/SHA256SUMS` | **51/51 OK** |
| `bi_mask_requested_evidence/SHA256SUMS.txt` | **35/35 OK** (before and after) |
| D20 five certificate frontiers | present, full size |
| D21 resumable state (e7 cubes, e11 shard, sample500) | present |
| `~/xor_ui/aes_mc_records` | untouched; tree clean; unpushed `73ad7ee` intact |
| `evidence/`, `fleet11/laneCUBE/`, `fleet8/unified/`, `fleet12/laneHALO/`, PyPy tree | untouched |
| `fleet1/laneA_v2pricing/results/configs.json` (D23) | 42,128 B, present |
| `verify_circuit.py` (D8) | present, unmoved |

**Note on the two deadlocked `generate.py` (PIDs 487378 / 499379, D7).** They are **no longer running.**
They were **already absent at baseline**: the start-of-pass `ps -eo pid,etime,args | grep -E
'mono\.py|cube16\.py|generate\.py'`, run before the first deletion, returned only the 20 solver
processes. So they exited or were reaped before this pass began — nothing here signalled them. Their
held-open logs `fleet12/laneHALO/logs/b{,3}_W3plus4.log` were not touched regardless and remain at
327 B / 114 B. The live-process count is therefore **20, not the 22 recorded on 2026-08-29 morning.**

### Scope discipline

TIER 2 and TIER 3 were **not touched**. Specifically still on disk, untouched: the 13.7 GB of
campaign_87 `.pop.jsonl` harvests, `global_vocab/states_uniq.bin` (C4), `hunt87_layer89/pool/` (C3),
beat88's 31.4 GB of `.cells.jsonl` and 44,249 `FOUND_*` files, `exports/`, `atlas/m1_v15/` +
`m1_wide{,_results}/` + `tri/market/`, `e16_lastwish/laneFPOINT/bank/`, `e15_campaign3/tools/pop88.pkl`,
and `fleet12/laneORDER/out/order_*.json`.

**Outstanding, deliberately not done here:** the D19 backup of beat88's untracked prose/certificate
layer (~15 MB) and of `fleet8`–`fleet12`. It is step 1 of the proposal's recommended order and should
happen before any TIER 2/3 pass in those trees. No `.md`, `.py` or certificate file was deleted in this
pass, so nothing of that layer was lost — but it is still the only copy, and still unbacked.

