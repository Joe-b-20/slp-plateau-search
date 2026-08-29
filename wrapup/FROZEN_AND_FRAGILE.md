# FROZEN AND FRAGILE — reorganization hazard map

Consolidated 2026-08-29 from the §6 HAZARDS and §7 GAPS sections of the ten slice
reports in `wrapup/reports/`. Companion to `wrapup/KEEP_DELETE.md` (which covers
*deletion*; this file covers *moving and renaming*).

**Purpose.** Before the later move/reorganize wave touches any path, check it
against this file. §0 is the lookup procedure; §1–§4 are things that **cannot
move**; §5–§12 are things that **break when moved** and how; §13 is the move-order
checklist.

**Headline numbers**
- **~700+ files hardcode the absolute repo root** `/home/joebachir20/xor_ui/slp-plateau-search`
  (campaign_87 466 · fleet1–4 75 · experiments/e1–e9 ~60 · atlas 41 across 20 files
  · plus enumerated sets in fleet5–8, fleet9–12, experiments/e10–e17, root).
- **39 symlinks in the whole repo, every one inside `campaign_87/`** — re-verified
  this session (`find . -type l`). Zero in `beat88/`, `atlas/`, `experiments/`,
  `fleet*/`, `evidence/`, `pipeline/`.
- **22 live processes** hold the frozen set of §1.
- **18 STOP sentinels** whose removal relaunches detached compute.
- The published-repo tree, `evidence/`, and `experiments/sat_package/` are pinned
  by DOI, by a byte-untouched declaration, and by SHA256 respectively.

**Naming correction every mover needs.** The slice reports abbreviate two
directories. The real names on disk are:
```
campaign_87/wave5_2026-08-04/     (reports write "wave5/")
campaign_87/wave6_2026-08-11/     (reports write "wave6/")
```
Verified this session with `ls -1 campaign_87/`.

---

## 0. How to check a path in 30 seconds

1. Is it under `fleet11/laneCUBE/`, or is it one of the four files in §1.2? →
   **STOP. Frozen. Do not touch until the k=14 solve ends.**
2. Is it `fleet8/unified/…`, or `fleet12/laneHALO/logs/b{,3}_W3plus4.log`? →
   **§1.3. Frozen for the same reason.**
3. Does its basename start with `STOP`? → **§2. Never delete, never omit from a
   copy.**
4. Is it in `evidence/`, `~/xor_ui/aes_mc_records`, or
   `experiments/sat_package/`? → **§3. Pinned; byte-identity is the contract.**
5. Is it a `.py` or `.sh`? → grep it for `/home/joebachir20` (**§5**) and for
   sibling-directory reads (**§6**).
6. Is it a `.jsonl` / `.json` / `.md`? → **§9**: absolute paths are baked into
   *data* and *prose* here, not only into code.
7. Is it a directory you are about to change the **depth** of? → **§7**. Several
   scripts resolve the repo root by walking a fixed number of parents.
8. None of the above → probably safe, but run the §13 checklist.

Fast greps:
```bash
# code-level absolute paths in a candidate subtree
grep -rln '/home/joebachir20/xor_ui/slp-plateau-search' --include='*.py' --include='*.sh' <dir>
# data/prose-level absolute paths (the ones people forget)
grep -rl  '/home/joebachir20/xor_ui/slp-plateau-search' --include='*.jsonl' --include='*.json' --include='*.md' <dir>
# who reads a file you are about to move
grep -rn '<basename>' --include='*.py' --include='*.sh' --include='*.md' .
# symlinks (all 39 are in campaign_87)
find <dir> -type l
```

---

## 1. CANNOT MOVE — live process dependencies

**22 PIDs, re-verified by `ps -eo pid,etime,args` on 2026-08-29.**
Never `pkill`. Never signal. Never create `experiments/STOP`.

| PIDs | age | process |
|---|---|---|
| 333371, 345293, 345295, 345297 | 3d 01–02 h | `python3 -u code/mono.py 14` — four monolithic solvers, ~90 % CPU each |
| 443496 | 2d 13 h | `python3 -u code/cube16.py --k 14 --cores 16 --group 33 --cube-timeout 0 --tlim 259200 --retry-timeouts` (parent) |
| 443570–443584 | 2d 13 h | 15 group workers, ~90 % CPU each |
| 487378, 499379 | 2d 09–10 h | two **deadlocked** `generate.py`, cwd `fleet8/unified` |

### 1.1 `fleet11/laneCUBE/` — the entire directory is frozen

Enumerated dependency set (`reports/fleet9_12.md` §6.1):

| path | why frozen |
|---|---|
| `code/` — all 9 `.py`: `cube16.py`, `inst16.py`, `mono.py`, `report.py`, `mkresult.py`, `sat_compile.py`, `controls.py`, `agree.py`, `probe.py` | workers are `fork`ed, but the parent may still import |
| `code/__pycache__/` (3 `.pyc`, 36 K) | same |
| `code/phase.sh`, `phase2.sh`, `phase3.sh`, `phase4.sh` | detached phase drivers |
| `logs/mono_14.log`, `mono_14_cadical300.log`, `mono_14_glucose42.log`, `mono_14_kissat404.log` | **open for append right now** (all 0 bytes, all held) |
| `logs/phase2.pid`, `phase3.pid`, `phase4.pid` | the kill handles named in `RESULT.md` §9 |
| `cubes/joint_W3U4_k14.jsonl` and `cubes/tmp/` | **actively appended and fsynced.** A truncated or moved bank loses banked core-hours permanently |
| `ledger.jsonl` | appended per solve |
| `inst/joint_W3U4.json`, `inst/SUB_U4tgts.json` | asserted byte-identical at process start |
| `found/`, `results/` | the SAT-branch write targets |

### 1.2 Outside the lane, load-bearing for it — four files (all re-verified to exist)

| path | role | note |
|---|---|---|
| `atlas/slp_opt.py` | every search primitive imported from it, unchanged | also imported by `fleet5/laneGLUE/code/gmodel.py:27,268` and by the exact experiments |
| `fleet8/unified/code/solver.py` | `key_of` imported, not re-implemented | see §8 for the key-pin hazard |
| `fleet8/unified/results/joint_W3U4_preflight.json` | the **pinned instance**, sha256 `d4916aef…` | also opened by `fleet11/laneCUBE/code/probe.py` **by absolute path** |
| `fleet8/unified/results/joint_levels.jsonl` | 381 B — the inherited k=9–13 ladder | **233.5 core-hours at k=13 alone. Never re-run it.** |

### 1.3 `fleet8/unified/` — live shared infrastructure, not a finished lane

Must not be moved, renamed, or have its `code/` edited (`reports/fleet5_8.md` H1).

- `fleet11/laneCUBE/code/inst16.py` reads the preflight and imports `key_of`;
  `probe.py` opens the preflight by absolute path; `sat_compile.py` imports
  fleet8's modules read-only and redirects every write.
- **~10 fleet12 scripts `cd` into it or `sys.path.insert` it by absolute path:**
  `fleet12/laneHINTS/run_step2.sh`, `run_step2b_rec88at7.sh`, `run_step3a_U1.sh`,
  `run_step3b_all.sh`, `run_step3c_noQ27.sh`; `fleet12/laneHALO/run_halo.sh`,
  `run_pairs.py:54`, `run_b4.py:67`, `run_u07.py:61`;
  `fleet12/laneORDER/run_order.sh:30`, `enum_orders.py:13`,
  `probe/supply_probe.py:20,24`.
- `fleet9/laneENUM/code/f4inst.py` runs a **snapshot copy** of fleet8's plan+engine.
- `fleet8/unified/ledger.jsonl` and `results/prereg.jsonl` are **shared writable
  hash-chained state** — `laneORDER/sweep.py:10` and `run_order.sh:15` warn the
  chain is *only safe under a single writer*. Rows appended as recently as
  **2026-08-27T18:23**. Do not truncate, rewrite or reformat.
- `fleet8/unified/results/joint.lock` (26 B, `82529 2026-08-25T03:42:14`) — the
  single-instance lock. Deleting it invites a second concurrent joint run.

### 1.4 The two deadlocked generators

`fleet12/laneHALO/logs/b_W3plus4.log` and `b3_W3plus4.log` are held open by PIDs
487378 / 499379 (confirmed via `/proc/<pid>/fd`). Four `<defunct>` children each,
0 % CPU — the `dslp._run_pool` deadlock documented in `laneHALO/RESULT.md`
§1.2/§5.1, **deliberately left detached, not killed.** They will never write again.
**Do not move those two log files while the PIDs exist. Do not `pkill python3`
for any reason.** Their intended outputs (`out/b_W3plus4.json`,
`out/b3_W3plus4.json`) were never created; the verdict was superseded by
`out/b4_W3plus4.json`.

### 1.5 The oracle and the repo root

`verify_circuit.py` **must not move**, and neither must the repo root, while
anything above runs. It is referenced by absolute or root-relative path from
`.github/workflows/verify.yml`, `tests/test_invariants.py`, `pipeline/README.md`,
`pipeline/seeds/README.md`, `reproduce/README.md`, `evidence/RESULTS.md`,
`CERTIFICATES.md`, `CHECK_SOLVER.sh`, `SESSION_PROMPT.md`, and — per grep —
**effectively every `RESULT.md` in every fleet and experiment lane.** Moving it
breaks the definition of "verified" tree-wide.

`CHECK_SOLVER.sh` (repo root) hardcodes absolute paths and reads
`fleet11/laneCUBE/{found,logs}`, `experiments/STOP`, `experiments/FOUND_*.json`,
`verify_circuit.py`, and `pgrep`s for `mono.py` filtered by cwd containing
`fleet11`. It only reads and never signals — safe to run, and it is the sanctioned
way to check the live solve.

---

## 2. CANNOT MOVE (or omit from a copy) — STOP sentinels

Removing one, or copying a tree **without** it, **relaunches detached compute.**
All are zero-byte or near-zero-byte, so any "delete empty files" or size-filtered
`rsync` will strip them.

Full enumeration (`find . -name 'STOP*'`, run this session — 18 sentinels):

```
campaign_87/hunt87/STOP
campaign_87/hunt87/selftest_run/STOP
campaign_87/tri_hunt/STOP
campaign_87/prior_basins/derived/engine/STOP
campaign_87/wave5_2026-08-04/fresh_fleet/STOP          <-- RESTARTS on `rm -f STOP`
campaign_87/wave5_2026-08-04/evolve/STOP               <-- RESTARTS on `rm -f STOP`
campaign_87/wave5_2026-08-04/mine_89only/STOP
campaign_87/wave5_2026-08-04/burn/union_sat/STOP
campaign_87/wave5_2026-08-04/burn/simple/execute/STOP
campaign_87/wave5_2026-08-04/burn/simple/executor/STOP
campaign_87/wave5_2026-08-04/nrpa/out/STOP
beat88/methods/m3_census/runs/local/STOP
beat88/methods/m3_census/runs/local/STOP_SHIPPER
beat88/methods/m3_census/runs/local_prev/STOP_SHIPPER
beat88/pod_salvage/pod1/beat88/methods/m3_census/runs/pod1/STOP
beat88/pod_salvage/pod1/beat88/methods/m3_census/runs/pod1/STOP_SHIPPER
beat88/pod_salvage/pod2/beat88/methods/m3_census/runs/pod2/STOP
beat88/pod_salvage/pod2/beat88/methods/m3_census/runs/pod2/STOP_SHIPPER
```
(`campaign_87/wave5_2026-08-04/burn/simple/execute/logs/STOPPED_procs_snapshot.txt`
also matches the glob but is a log, not a sentinel.)

Related: `campaign_87/agents/hunt-88at6/launch.sh` does `rm -f ../STOP_BREAKTHROUGH`
as its second action. And **`experiments/STOP` must never be created** — it is the
live campaign's kill switch.

**52 stale PID files** — `campaign_87/hunt87_layer89/pids/`, `families16/pids/`,
`hunt87_basin4/pids/`, `novelty/descent/pids`, `d3_model/runs/pids.txt`. The
launchers read them to decide whether a shard is already running; after a move a
fresh launch could refuse to start or **signal a recycled PID**.
(`hunt87`/`tri_hunt`/`cascade6` are safe — their `Fleet._owned()` verifies
`/proc/<pid>/cmdline`.)

---

## 3. CANNOT MOVE — checksum-, DOI- and byte-pinned

| # | scope | pin | what breaks on a move |
|---|---|---|---|
| 3.1 | `experiments/sat_package/` (24 MB, 51 files) | `SHA256SUMS`, currently 51/51 OK | Moving, renaming, recompressing or regenerating **any** file breaks the manifest. `code/{sat_compile,inst16,cube16}.py` and `verify_circuit.py` inside it are unmodified `cp -p` copies taken 2026-08-28, **deliberately pinned so later drift is visible — do not de-duplicate them against their originals.** `sat_package/code/sat_compile.py` resolves its working directory from its own location; **moving that file relative to the package lets it write into the running campaign's directories.** Do not touch until k=14 is settled. |
| 3.2 | `evidence/*/` run archives (4.9 MB, 11 subdirs) | `README.md` declares logs/statuses/bests/`code/` **never edited or regenerated**, byte-identical to what the run produced | Any reorganisation must preserve them **byte-for-byte**. Only `PROVENANCE.md` is maintained, and only with a dated note. |
| 3.3 | `~/xor_ui/aes_mc_records` (956 K tracked) | DOI'd (concept 10.5281/zenodo.21299092 + version DOIs), CI-gated, one **unpushed commit `73ad7ee`** | `sha256_circuit_json` is over the file bytes **as they land in that repo** — a pretty-printer changes it; recompute after any copy. Deleting a superseded circuit breaks an archived DOI. Do not reset, rebase or force-push. Seven file classes are generated and must never be hand-edited: `listings/*.txt`, `verilog/*.v`, `verilog/*_tb.v`, `docs/frontier.svg`, `audit/recomputed_metrics.json`, `audit/MATHEMATICAL_VERIFICATION.md`, `paper/appendix_circuits.tex`. |
| 3.4 | `bi_mask_requested_evidence/` | `SHA256SUMS.txt` | Hash-manifested preservation bundle answering an explicit request; only surviving copy of the n16 near-26 module and the 36-mask defect vocabulary; input to `phase2_e3.py`. *(The `*:Zone.Identifier` ADS files are **not** in the manifest, so removing them is safe.)* |
| 3.5 | `atlas/v15_partial.tgz`, `atlas/wide_results.tgz` | become the **sole copies** if their expansions are deleted | Never delete both a tarball and its expansion in the same pass. SHA-verify `wide_results.tgz` before acting on it — that pair was checked by entry count only. |
| 3.6 | `fleet2/laneP_proof/referee/results/verify1_ledger_snapshot_20260820.jsonl` | sha256 `bc77f0fd…`, the **refereed reference**, frozen while the live file kept growing | Its sibling `fleet2/laneP_proof/verify1/ledger.jsonl` (8,074 rows, sha256 `497b8da7…`) is the final file. Lane P §6 quotes the snapshot with the final in parentheses. Treating them as duplicates and deduplicating **corrupts the referee's record.** |
| 3.7 | `beat88/pod_salvage/` | sources destroyed | Both pods (38.80.152.147:41863, 213.173.105.99:42056) terminated 2026-08-15/16. Only copies of ~18 GB + ~21 GB of run data, 1,020,241 exported circuits, two 715 MB manifests, 854 harvest segments. |
| 3.8 | `atlas/pod_evidence/` | sources destroyed | Only local copy of the L ≥ 56 depth-4 exhaustion (`d4out.tgz`) and the 28/28 cube verdict. Backs the project's headline lower bound. |

---

## 4. CANNOT MOVE — no version control safety net

| tree | `git ls-files … | wc -l` | consequence |
|---|---|---|
| `beat88/` (47 GB, 1,463,947 files) | **0** | `git status --porcelain beat88` → `?? beat88/`. Not one write-up, certificate, `CANON.md` or export is tracked. **A botched move is unrecoverable.** |
| `fleet8/` … `fleet12/` | **0** | Which is why `fleet9/laneENUM/snapshot/` (720 K, a frozen pre-fleet9 copy of `fleet8/unified`) and the five `fleet8/unified/code/*.{bak,prelive}` are the **only** record of those code states. |
| `campaign_87/` (29 GB) | gitignored | `.gitignore` excludes `campaign_87/` **and** `.claude/` — anything a reorganisation moves *into* those paths **silently leaves the repo.** |

Before any move of these three: copy the prose/certificate layer (~15 MB for
beat88, plus fleet8–12's `.md`/`.py`) off the box or commit it.

---

## 5. FRAGILE — hardcoded absolute paths in CODE

The root string is `/home/joebachir20/xor_ui/slp-plateau-search`. **Every
documented resume command in the project is an absolute `cd`.**

| region | count | reproduction command | concentration |
|---|---|---|---|
| `campaign_87/` | **466** `.py`/`.sh` files | `grep -rl '/home/joebachir20/xor_ui/slp-plateau-search' campaign_87 \| grep -v site-packages \| wc -l` | `wave5_2026-08-04` **227** · `wave6_2026-08-11` **106** · `agents/` **24** · mid-campaign dirs **43**. The rented pod solved this with a **symlink on the remote box**, not by fixing the files. |
| `fleet1`–`fleet4` | **75** hardcodes in **30** files | `grep -rln '/home/joebachir20' --include=*.py --include=*.sh fleet1 fleet2 fleet3 fleet4 \| wc -l` | `laneB/code/*.sh` (nanny chains, launchers) · `laneCB/code/launch_*.sh`, `ctrl_rank2.sh` · `laneD/code/run_bwd.sh` · `v2lib.py`, `price.py`, `resttab.py`, `quotients.py`, `qsolve.py`, `fortify.py`, `rtheory.py`, `u07.py` |
| `experiments/e1`–`e9` | **~60** files | `grep -rl '/home/joebachir20/xor_ui/slp-plateau-search' experiments` | `e5_readd/code/kern.py` (`ROOT = "…"`) · `e3a_exploit/code/{blocks,blockpop,buyone,k3shell,kern,orbit_odd,plansize,spread}.py` · `e6_cancelplan/code/cpk.py` · `e7_push/code/{convex,cube,kern,orbit_odd,sigma_odd}.py` · `e8_quad/code/{assemble,decode,familycurve,firstgates,instances,runquad,validate}.py` · `e4_depth/code/{d4decide,d4floor}.py` · `e_oddlane3/census.py` · ~15 `.sh` drivers |
| `atlas/` | **41** occurrences across **20** files | `grep -rln '/home/joebachir20/xor_ui/slp-plateau-search' --include=*.py --include=*.sh atlas` | `run_ef.sh` · `socleplane/{build,sweep,core,readoff,recskel}.py` · `tower/{analyze,lift,quotient,extract,structure}.py` · `thinktank/{phase2_depth_driver,phase2_alt_chain,phase2_chain,phase2_chain2}.sh` · `thinktank/{compile_config_v3,v15_dp,v15b_gen}.py` · `thinktank/proofside_code/{z_census.py,run_hi.sh}` |
| `fleet5`–`fleet8` | enumerated, not counted | see §6 | shell drivers with hardcoded `cd`: `fleet5/laneMERGE/code/queue{1,3,5}.sh` · `fleet6/laneTOOL2/code/run_wave{,2,3}.sh`, `run_final.sh`. Plus `fleet7/laneUNCOND/referee/h0.py:15,17` |
| `fleet9`–`fleet12` | enumerated | | `fleet10/cleanroom/work/satfix*.py` (`SPEC`, `WORK` constants) · `fleet10/cleanroom/work/{collect,migrate}.sh` (absolute `cd`) · `fleet12/laneHALO/run_chain*.sh`, `run_halo.sh` and the `--out` args of the two deadlocked PIDs · the ~10 fleet12 scripts of §1.3 |
| `experiments/e10`–`e17` | enumerated | | every lane's Law-1 procedure invokes `python3 /home/…/verify_circuit.py`; see §9 for the data/prose side |
| repo root | 1 | | `CHECK_SOLVER.sh` |
| `beat88/` | **0 in code** | | Uses `kernel.repo_root()` (finds the checkout from either the local or the pod layout, overridable with `SLP_ROOT`) and `sys.path.insert(0, "<repo>/beat88/methods/shared")`. **The hazard here is in the documented resume commands, not the code** — see §9. |
| `~/xor_ui/aes_mc_records` | **0** | | no absolute paths, no symlinks, no running processes |

---

## 6. FRAGILE — cross-directory reads (dependency edges)

Reorganising the **producer** breaks the **consumer**, even when the consumer's own
directory is untouched. This is the table a mover most needs.

| consumer | reads / imports | edge |
|---|---|---|
| `fleet5/laneMENU/code/cells_all.py:18`, `queue1.py`, `derive_menu.py`, `queue_main.py`, `rho.py`, `menuspace.py` (via `M.F4`) | `fleet1/laneA_v2pricing/results/configs.json`; `fleet3/laneF4_rule/code` | **7-call-site hub** |
| `fleet5/laneMERGE/code/cells.py` | `fleet1/laneA_v2pricing/results/configs.json` | |
| `fleet8/unified/code/cells.py:33` | `fleet1/laneA_v2pricing/results/configs.json` | loaded **at module import on every invocation**, incl. `naive` and `--selftest` |
| `fleet8/unified/code/cells.py:170` | `fleet2/laneG_generator/results/` (the ladder spectrum) | moving it kills every `f4`- and `ladder`-regime run |
| `fleet8/unified/code/check_l5.py:13` | `fleet3/laneF4_rule/code` | |
| `fleet9/laneENUM/code/v2inst.py:32`, `snapshot/code/cells.py:33` | `fleet1/laneA_v2pricing/results/configs.json` | |
| `fleet12/laneF1/diffcheck.py:28` | `fleet1/laneA_v2pricing/results/configs.json` | `fleet12/laneALGO/ALGORITHM.md:33` calls it *"the algorithm's one external data dependency"* — the audit docs cite the path **verbatim** |
| `fleet3/laneCB_completeness/code/crosscheck.py` (+ 2 sandbox copies) | `fleet1/laneA_v2pricing/inst/g01full_88at7_f8cd1048a1b76bf2d5a6.json` · `fleet2/laneG_generator/inst/free_U1_diag_flag_a246c12491b9.json` · `fleet2/laneG_generator/referee/inst/refU1_diag_49f138ea64.json` | **the evidence that no encoding disagreement exists between the three lanes** |
| `fleet5/laneGLUE/code/gmodel.py:27,268` | `atlas/slp_opt.py`; `fleet3/laneF4_rule/code` | |
| `fleet7/laneUNCOND/code/dich2.py:31` | `beat88/understanding/u6_spec87` (8 CANON price tables) | **cross-slice, fleet → beat88** |
| `fleet7/laneUNCOND/referee/h0.py:15,17` | hardcoded repo root + `evidence/circuits/mixcolumns_88gates_depth5.json` | |
| `fleet9/laneENUM` | `campaign_87/agents/hunt-deeper/population88_new.jsonl` (54,889-circuit harvest); byte-copies from `campaign_87/agents/exact-k4/work/` | **cross-slice, fleet → campaign_87** |
| `fleet12/*` | `fleet8/unified/` and through it `fleet1/laneA_v2pricing/results/configs.json` | |
| `fleet12/laneORDER` | **appends** to `fleet8/unified/results/prereg.jsonl` (hash-chained, 153 entries) | two concurrent writers break the chain — the whole 75-order sweep ran on one core for this reason |
| `campaign_87/hunt87/supervisor.py:86`, `tri_hunt/supervisor.py:99`, `cascade6/supervisor.py:107` | `campaign_87/agents/exact-k4/tools/pypy3.11-v7.3.23-linux64/bin/pypy3` | **silent** 5× slowdown if the tree moves (falls back to CPython, no error) |
| `campaign_87/hunt87_layer89/harvest89.py`, `families16/harvest.py`, `d3_exact/screen.py`, `wave6_2026-08-11/discriminate/scan_hiplane.py` | glob `hunt87/runs`, `hunt87_basin4`, `hunt87_depth5`, `agents/*/runs*` | harvest-globbers reach across the whole campaign |
| every `experiments/e*/code/` | `sys.path.insert` `pipeline/` → imports `engines` / `mixcolumns_core`; exact experiments import `atlas/slp_opt.py`; E5/E6/E7 resolve circuits through `evidence/circuits/*.json` **by name** | **Reorganising `pipeline/`, `atlas/`, `evidence/`, `beat88/` or `campaign_87/` breaks the experiments slice even if it is untouched.** |
| `atlas/periscope/{engine,census,shapes,shell_probe,harvest_check}.py`, `atlas/corner/{socle,census,envelope}.py`, `atlas/tri/{tri_control,tri_c3,tri_c4}.py`, `atlas/tower/extract.py`, `atlas/thinktank/{phase2_probe,phase2_controls,phase2_fin}.py` | `evidence/circuits/`, `pipeline/`, `beat88/`, and **`~/xor_ui/aes_mc_records` — a different repo** | ~15 files |
| `joe_depth3_audit/*.py` | `evidence/circuits/...` **by relative path** | only run from the repo root; moving them into a subdir **silently breaks them** |
| `beat88/methods/m5_backbone/verify/shot87.py` | `beat88/methods/m3_census/exports/<FILE>.json` **directly** | the 182-family resume in `phaseB_remaining.json` breaks if `exports/` is repacked into a tarball |
| `atlas/explainer.html`, `atlas/workbench.html` | `atlas/viz_data.json`, `atlas/editor_data.json` | **no generator exists in the repo** (audit ISSUE 5.5) — unregenerable |
| `beat88/methods/shared/kernel.py` | rebuilds `shared/lib/libslpkernel.so` on import if missing/stale | deleting the `.so` is safe; **deleting `csrc/` is not** |
| `experiments/sat_package/README.md` §9 | `fleet11/laneCUBE/cubes/joint_W3U4_k14.jsonl` | the package's honesty note is only correct while that lane is untouched |

---

## 7. FRAGILE — depth-sensitive path resolution

Several scripts find the repo root by **walking a fixed number of parents**.
Changing the *depth* of a lane directory silently redirects them — no error.

- `fleet8/unified/code/generate.py:50-61`, `fleet5/laneMERGE/code/mergegen.py:114,155`,
  `fleet5/laneGLUE/code/reassoc.py:135`, `fleet8/unified/code/joint.py:169-185` all
  resolve `REPO/verify_circuit.py` and `REPO/experiments/` by walking **two
  directories up from the lane**. *"Changing the depth of any lane directory
  silently redirects the FOUND/STOP protocol."* (`reports/fleet5_8.md` H3.)
- `tests/test_invariants.py`: `ROOT = Path(__file__).resolve().parents[1]`.
- `fleet9/laneENUM/code/tally.py`, `v2inst.py` resolve `LANE` and `REPO` relative to
  the repo root. `fleet9/laneENUM/snapshot/code/*` has its `REPO` constants
  **already patched for relocation and marked in-file — a second relocation needs
  the same treatment.**
- `experiments/sat_package/code/sat_compile.py` resolves its working directory from
  its own location (this is a *safety* feature — see §3.1).
- `beat88` `kernel.repo_root()` finds the checkout from either the local or the pod
  layout, and honours `SLP_ROOT`. **beat88 is the only slice designed to be moved.**

---

## 8. FRAGILE — code-level pins that fail on the *next* launch

**`fleet11/laneCUBE/code/inst16.py:47-48` — the laneCUBE cache-key pin.**
```
EXPECT_KEY = f04dcb3ecf180a30204434a0bd32453e7635e8b6
```
imported from fleet8's own `key_of`. **laneLIB fix B1 changed that key function**,
so the digest is now `56abd9cb90099824eafda21b81f241bf64fb7eba`.

- The **running** processes are safe: the assertion runs once at start and workers
  are forked.
- **Any fresh launch of `cube16.py` or `mono.py` will refuse to start**, loudly,
  naming `key_matches_recorded`. It fails closed, which is the correct direction.
- The remedy is one line in `fleet11/laneCUBE/code/inst16.py`;
  `solver.legacy_key_u1(inst)` reproduces the old digest for confirmation.
- Documented in full at `fleet12/laneLIB/RESULT.md` §7. **The reorganisation wave
  must carry this note forward — the lane cannot be restarted without it.**

Related: **env-gated behaviour switches inside `fleet8/unified`** —
`SLP_SUPPRESS_HINTS` (`generate.py:78`), `SLP_DERIVE_MAX_COST`, `SLP_USE_POOL`,
plus env-gated menu and commitment overrides at `code/cells.py:39,213` and
`code/plan.py:48` (`LANE_HALO`). **A run's numbers depend on the environment it was
launched in, and the artefacts do not always record which.** Also `--pool` is
documented as deadlocking (`generate.py:409-417`); the serial path is the default
and is 1.2×–31× faster.

---

## 9. FRAGILE — absolute paths baked into DATA and PROSE (not just code)

These cannot be fixed by a `sed` over `*.py`, and several of them are
**append-only by convention, so they cannot be rewritten at all.**

| location | what is baked in |
|---|---|
| `campaign_87/wave5_2026-08-04/burn/oddparity/ledger.jsonl` | alphabet paths recorded **inside ledger lines**; append-only, cannot be rewritten |
| campaign_87 ledgers generally | absolute paths embedded in result rows |
| `experiments/e17_pure/DOSSIER.md` | declares *"Repository root for every path in this document is `/home/joebachir20/xor_ui/slp-plateau-search/`"*, then cites `fleet7/laneUNCOND/results/bstar/nostop_lp_cert_4_1.json`, `fleet2/laneP_proof/RESULT.md`, `fleet1/laneC_proofside/code/rewire.py`, `fleet6/laneTOOL2/RESULT.md`, `beat88/understanding/CANON.md`, `atlas/thinktank/lower_bound.md`, `atlas/thinktank/referee_55.md`, `fleet7/laneCONSOLIDATE/STATE_OF_THE_PROBLEM.md`. **Moving any of those breaks the dossier's citation chain.** |
| `experiments/e17_pure/laneDELTA/lemmaR_hits_nonsample.json`, `nat_hits.json` | record absolute paths into `campaign_87/` and `experiments/e3a_exploit/` |
| `experiments/e13_hand87/laneFRESH/RESULT.md` and every lane's Law-1 procedure | `python3 /home/joebachir20/xor_ui/slp-plateau-search/verify_circuit.py` |
| `beat88/methods/m2_oracle/STATE.md`, `m5_backbone/verify/STATE.md` §5, `m3_census/FINAL.md` §6 | **documented resume commands** written against `beat88/methods/<lane>/code` as cwd, and against pod paths `/root/slp87`, `/root/slp87_pod2`. **Reorganising the lane directories breaks every documented resume path** even though the code itself is relocatable. |
| pod2-origin logs throughout `beat88/pod_salvage/pod2` | contain `/root/slp87` paths that were really pod2 (pod2's repo relied on `/root/slp87 -> /root/slp87_pod2`) |
| `fleet11/laneCUBE/RESULT.md` §9 | absolute resume commands — documentation, but it **is** the resume procedure |
| `fleet12` audit documents | cite `fleet1/laneA_v2pricing/results/configs.json` **verbatim** |
| `campaign_87` `wave6_2026-08-11/audit` and every resume note | absolute `cd` |
| `~/xor_ui/aes_mc_records/audit/` generated reports | none — but `sha256_circuit_json` is over file bytes, so any reformat during a move invalidates them |

---

## 10. FRAGILE — symlinks

**39 symlinks in the entire repo, all inside `campaign_87/`** (`find . -type l`,
re-run this session). Zero in `beat88/` (confirmed by that slice too), `atlas/`,
`experiments/`, `fleet*/`, `evidence/`, `pipeline/`, `reproduce/`, `tests/`,
`docs/`, `bi_mask_requested_evidence/`, `joe_depth3_audit/`, or the records repo.

| symlink | target | hazard |
|---|---|---|
| `campaign_87/agents/frontier-sat/kissat/src/makefile` | `/home/joebachir20/xor_ui/slp-plateau-search/campaign_87/agents/loose-sat/kissat/makefile` | **absolute, cross-agent.** Deleting or relocating `agents/loose-sat/` silently breaks `frontier-sat`'s solver rebuild. |
| 5 × `agents/{frontier-sat,family3-sat,sat-window,lit-88,sat-deep,loose-sat}/venv/bin/python{,3,3.10}` + `venv/lib64` (20 links) | `/home/joebachir20/anaconda3/bin/python3` | absolute bootstrap — **the venvs are not relocatable.** Rebuild rather than move. |
| `campaign_87/agents/exact-k4/tools/pypy3.11-v7.3.23-linux64/bin/{python,python3,python3.11,pypy,pypy3}` | internal | the target of the three-detector dependency (§6) |
| `campaign_87/agents/{frontier-sat,loose-sat}/kissat/{src,test}/configure`, `kissat/test/cnf/hard.cnf` | internal to each kissat tree | move the tree whole or not at all |
| `campaign_87/wave6_2026-08-11/sat_boost/tools/cms/scripts/{fuzz/final_check.py,output_parser/helper.py}` | internal to the CryptoMiniSat vendor tree | |

---

## 11. FRAGILE — filename- and position-coupled data

Renaming these files, or reordering their contents, breaks a parser or a resume
with **no error**.

- `atlas/corner/out/*.plat` — filenames encode arm/seed/config and are parsed by
  `corner/analyze.py`. Renaming breaks the A/B analysis.
- `campaign_87/wave5_2026-08-04/burn/downstep/runs/{A..H}.done` hold **line numbers
  positionally coupled** to `jobs_[A-H].txt`. Editing a jobs file invalidates the
  done file silently.
- **Append-only ledgers with skip-by-id resume** — splitting, sorting,
  deduplicating or reformatting causes **silent re-decision or silent skipping**:
  campaign_87's `fence_sat`, `burn/union_sat`, `burn/downstep`, `alphabet_ladder`,
  `steinberg`, `mine_89only`, `skeleton_pools`, `band_hunt`, `hp_strike`, all
  `progress.jsonl`, all `*/detector/swept.jsonl`, `rung_ledger.jsonl`,
  `endpoints.jsonl`, `psweep*.jsonl`; every fleet `ledger.jsonl` / `results.jsonl`
  / `cubes/*.jsonl` / `cache/*.jsonl`; every experiment `ledger.jsonl`;
  `fleet8/unified/{ledger.jsonl, results/prereg.jsonl}` (hash-chained).
- **`fleet1/laneA_v2pricing/solve_cache.jsonl` references each `inst/` and `logs/`
  file by name** — archiving those trees invalidates the cache.
- **Checkpoint stubs that look like checkpoints:**
  `campaign_87/wave6_2026-08-11/dfs_par/ck/SIGMA7_B17_41-42-…-97.ck` is a **134-byte
  stub** next to the real 2.2 MB checkpoint; `runpod/synced/ck_rescue/ck/fromscratch_B16_35-47-…-110.ck`
  is **0 bytes**. Resume B=18 from `ck_rescue/ck/`, not from `dfs_par/ck/`.
- **Filename-based record detection produces false positives:**
  `campaign_87/wave5_2026-08-04/burn/mutant_cluster/quarantine_misplaced/` (98 files
  named `BREAKTHROUGH_88gates_*`) and `.../burn/mutant_satrepair/selftest_work/`
  (`BREAKTHROUGH_{101..126}gates_*`). **Gate on `gateCount` and on
  `verify_circuit.py`, never on the filename.**

---

## 12. FRAGILE — deliberate duplicates that must NOT be de-duplicated

A reorganisation that "tidies up copies" will destroy four independence claims.

| pair | why they are separate |
|---|---|
| `reproduce/mixcolumns_core.py` ↔ `pipeline/mixcolumns_core.py` | byte-identical **by design**; `reproduce/README.md` publishes the `diff` as a claim |
| `fleet2/laneG_generator/code/theory.py`, `build.py` ↔ `fleet3/laneF4_rule/code/…` ↔ `fleet3/laneDEPTH/code/f4/` | **copies, not imports** (lane F4 §7 and lane DEPTH say so explicitly, with cache and ledger paths re-pointed). Merging them breaks the provenance claim that each lane's algebra was independently instantiated, and silently couples three currently independent lanes. |
| `fleet9/laneENUM/snapshot/` ↔ `fleet8/unified/` | the snapshot is a **frozen pre-fleet9 copy**, and since fleet8–12 are untracked it is the only record of that code state |
| `experiments/sat_package/code/{sat_compile,inst16,cube16}.py`, `verify_circuit.py` ↔ their live originals | `cp -p` copies pinned 2026-08-28 **so later drift is visible** |
| `fleet2/laneP_proof/verify1/ledger.jsonl` ↔ `.../referee/results/verify1_ledger_snapshot_20260820.jsonl` | see §3.6 |
| `fleet9/laneENUM/code/imported/` ↔ `campaign_87/agents/exact-k4/work/` | byte-copies of the historical irreducibility instrument; the equivariance result is only meaningful because it ran against **those bytes** |

And the reverse trap — **things that look like duplicates but are not:**
`wshB1.log` / `wshB2.log` / `wshC1.log` / `wshC2.log` at the repo root have md5s
that all differ from `fleet10`'s identically-named files.

---

## 13. Move-order checklist

1. **Do not move anything in §1 until the k=14 solve finishes.** That is
   `fleet11/laneCUBE/`, `fleet8/unified/`, `atlas/slp_opt.py`,
   `fleet12/laneHALO/logs/b{,3}_W3plus4.log`, `verify_circuit.py`, and the repo
   root itself. Check with `ps -eo pid,etime,args | grep -E 'mono\.py|cube16\.py'`.
2. **Back up first.** `beat88/` and `fleet8`–`fleet12` are untracked; `campaign_87/`
   is gitignored (§4). A botched move there is unrecoverable.
3. **Copy with `-a` / `--links` and no size filter**, so the 18 STOP sentinels (§2),
   the 39 symlinks (§10) and the zero-byte evidence files survive.
4. **Never run `pkill`, and never create `experiments/STOP`.**
5. For each moved directory, run the four greps in §0 over it **and over the whole
   repo for its basename** — the consumer is usually in a different slice (§6).
6. Fix code paths, then **re-read §9**: the data and prose layers hold absolute
   paths that no code `sed` will reach, and the append-only ledgers among them
   cannot be rewritten at all.
7. If any lane directory changes **depth**, re-check §7 — those failures are silent.
8. Carry the §8 `EXPECT_KEY` note forward in writing. laneCUBE cannot be restarted
   without it.
9. Re-verify the pins in §3 afterwards: `sha256sum -c` in `sat_package/` (expect
   51/51 OK) and in `bi_mask_requested_evidence/`; confirm `evidence/` is
   byte-identical; confirm `git status` in `~/xor_ui/aes_mc_records` still shows the
   single unpushed commit `73ad7ee`.
10. Do not de-duplicate anything in §12.

### Ops traps that survive any reorganisation

Recorded across the reports; they bite whoever re-runs this code, wherever it lives.

- `atlas/slp_opt.py` defaults to **all cores** and will spawn ~21 workers — always
  pass `--cores` (a load-176 incident is documented).
- `subprocess.run(capture_output=True, timeout=…)` **hangs forever** on `slp_opt`
  because grandchildren hold the pipe — use file redirection + `start_new_session`
  + `killpg`.
- `slp_opt --timeout` is **wall-clock**, and **this box's clock steps backwards** —
  use a monotonic deadline. beat88 moved to `time.monotonic`; anything resurrected
  from an older tree must be checked. **Any timestamp comparison across files in
  this tree is unreliable.**
- `slp_opt` **block-buffers stdout** under redirection — use `python3 -u`.
- `pysat`'s `Cadical195.interrupt()` raises `NotImplementedError` in the installed
  build and `solve()` does not release the GIL, so **an in-process wall clock on a
  pysat CaDiCaL solve silently never fires.** One worker ran 47 minutes past a
  3,600 s "timeout".
- **`nice` is fatal on this box, not polite:** at `nice -n 10` under load ~39 a
  worker received 1.4 % of one core. Use `/proc` CPU-seconds, not wall clock.
- **Trim-backend split:** beat88's C `trim` disagrees with Python on 14.5 % of
  states *above* 88 masks (0/1,671 at exactly 88). Never switch trim backends
  mid-stream when re-processing `*.cells.jsonl` or the harvest.
- `zstd` is **not installed** and Python has no `zstandard` module — a prerequisite
  for every compression proposal in `KEEP_DELETE.md` §3.
