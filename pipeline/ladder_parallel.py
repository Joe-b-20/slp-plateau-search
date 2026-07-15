#!/usr/bin/env python3
"""
ladder_parallel.py  --  the record-hunting pipeline (parallel, reseeding).

    python3 ladder_parallel.py [--mode cascade|fixed]
                               [--stop-gates N] [--stop-depth D]

Two modes (--mode overrides the MODE default below):

  "cascade"  the depth ladder: start depth 3 from scratch, and each time the
             frontier rung beats its baseline (or times out) launch the next
             deeper rung seeded from it -- all rungs keep running, all reseed.

  "fixed"    launch a fixed set of workers at once (each with its own depth cap
             and seed) and let them run in parallel, continuously re-seeding
             each other. Shipped as the exact sub-89 configuration that
             produced 89@depth5.

--stop-gates / --stop-depth make the coordinator shut everything down cleanly
as soon as a verified global best satisfies BOTH given bounds (an omitted
bound is a don't-care), e.g. to replicate the records:

    python3 ladder_parallel.py --mode fixed   --stop-gates 89 --stop-depth 5
    python3 ladder_parallel.py --mode cascade --stop-gates 92 --stop-depth 4

Without stop bounds the run continues until Ctrl-C; either way every best is
already on disk.

Every worker is its own OS process (real parallelism). Every worker
verifies-before-claim and uses a PARETO tie-break (accept fewer gates, or
equal gates at lower depth) so shallow equal-gate circuits are not lost. The
coordinator maintains best_overall.json and offers each worker the best circuit
that is feasible at its depth cap (reseed_<label>.json), which the worker adopts
between chunks.
"""
import argparse
import os, sys, json, time, shutil, subprocess

# ==========================================================================
# CONFIG  --  edit everything here
# ==========================================================================
OUT_ROOT = "runs_parallel"
MODE = "cascade"                # "cascade" or "fixed"
#   cascade = the from-scratch depth ladder (d3 anneal3, deeper rungs seeded
#             from the frontier). This is the configuration shape of the run
#             that produced 92@depth4 (see ../evidence/
#             cascade_run_2026-07-14_from_scratch_newlogic/).
#   fixed   = the FIXED_WORKERS set below, shipped as the EXACT two-worker
#             configuration of the sub-89 run that produced 89@depth5 (see
#             ../evidence/sub89_run_2026-07-14_got_89at5/code/CONFIG_AS_RUN.md).

# ---- fixed-mode workers: the sub-89 configuration -------------------------
# Two reseeding workers warm-started at the frontier: an uncapped hunter on the
# 89@depth6 circuit (chasing 88, and free to surface equal-gate-shallower
# circuits via the Pareto tie-break -- this is the worker that found 89@depth5
# in ~10 minutes), and a depth-5-capped hunter on the 90@depth5 circuit.
FIXED_WORKERS = [
    dict(label="uncapped_sub89", engine="lns", depth=None,
         start="seeds/seed_89_at_depth6.json"),
    dict(label="depth5_sub90", engine="lns", depth=5,
         start="seeds/seed_90_at_depth5.json"),
]

# ---- cascade-mode ladder ---------------------------------------------------
DEPTHS = [3, 4, 5, 6, 7, 8, 9, 10, 11]
FINAL_UNCAPPED_DEPTH = True
MAX_WAIT_S = 2 * 3600           # a rung triggers the next after this long even without a hit
IMPROVE_BY = 1                  # ...or as soon as it beats its baseline by this many gates
DEPTH3_BASELINE = 97
ENGINE_D3 = "anneal3"
ENGINE_DEEP = "lns"

# ---- shared ---------------------------------------------------------------
SEEDS_PER_WORKER = [1, 2, 3]    # default RNG seeds (a worker dict may override)
POLL_S = 20                     # coordinator status cadence
CHUNK_S = 600                   # worker chunk length (each worker continues from its OWN best)
RESEED = True                   # coordinator offers each worker the best circuit
                                # feasible at its depth cap (as in both record runs)

LNS_KNOBS = dict(kmax=6, kshake=12, snapback=8, nsamp=(24, 24), up_prob=0.5, up_slack=4)
WALK_KNOBS = dict(hub_move_p=0.35, close_hamming=4, repair_hub=40, repair_one=24, plateau_slack_p=0.02)
ANNEAL_KNOBS = dict(anneal_iters=150000, ils_rounds=2500, sa_T0=2.0, sa_T1=0.05)
# ==========================================================================
# END CONFIG
# ==========================================================================

HERE = os.path.dirname(os.path.abspath(__file__))

# Optional stop bounds, set from the command line in main(). The coordinator
# stops cleanly once a verified global best satisfies every given bound.
STOP_GATES = None
STOP_DEPTH = None


def target_reached(state):
    if state["gb"] is None or (STOP_GATES is None and STOP_DEPTH is None):
        return False
    g, d = state["gb"]
    return (STOP_GATES is None or g <= STOP_GATES) and \
           (STOP_DEPTH is None or d <= STOP_DEPTH)


def pareto_better(g2, d2, g1, d1):
    if g1 is None:
        return True
    return g2 < g1 or (g2 == g1 and d2 < d1)


def read_status(path):
    try:
        return json.load(open(path))
    except Exception:
        return None


def launch(label, engine, depth, start, out_dir, log, seeds=None):
    seeds = ",".join(str(s) for s in (seeds or SEEDS_PER_WORKER))
    depth_arg = "none" if depth is None else str(depth)
    start_abs = "scratch" if start == "scratch" else os.path.join(HERE, start) \
        if not os.path.isabs(start) else start
    cmd = [sys.executable, os.path.join(HERE, "worker.py"),
           label, engine, depth_arg, start_abs, out_dir, seeds]
    logf = open(os.path.join(out_dir, "%s.stdout" % label), "a")
    proc = subprocess.Popen(cmd, cwd=HERE, stdout=logf, stderr=subprocess.STDOUT)
    log("LAUNCH %-16s engine=%s depth=%s start=%s pid=%d"
        % (label, engine, depth_arg,
           os.path.basename(start) if start != "scratch" else "scratch", proc.pid))
    return proc


def gather_bests(meta):
    """label -> (gates, depth, best_path) for every worker with a verified best."""
    out = {}
    for lbl, m in meta.items():
        st = read_status(m["status_path"])
        if st and st.get("best_gates") is not None:
            out[lbl] = (st["best_gates"], st["best_depth"], m["best_path"])
    return out


def do_reseed(meta, procs, out_dir, log, state):
    """Update best_overall.json and offer each live worker the best circuit that
    is feasible at its depth cap (and Pareto-beats its own best)."""
    bests = gather_bests(meta)
    if not bests:
        return
    gb_lbl = min(bests, key=lambda l: (bests[l][0], bests[l][1]))
    gg, gd, gp = bests[gb_lbl]
    if state["gb"] is None or pareto_better(gg, gd, state["gb"][0], state["gb"][1]):
        state["gb"] = (gg, gd)
        shutil.copy(gp, os.path.join(out_dir, "best_overall.json"))
        log("GLOBAL BEST %d gates depth %d (%s) -> best_overall.json" % (gg, gd, gb_lbl))
    if not RESEED:
        return
    for lbl, m in meta.items():
        if procs[lbl].poll() is not None:
            continue
        cap = m["cap"]
        own = bests.get(lbl)
        own_g, own_d = (own[0], own[1]) if own else (None, None)
        cands = [(g, d, p) for l2, (g, d, p) in bests.items()
                 if l2 != lbl and (cap is None or d <= cap)]
        if not cands:
            continue
        cg, cd, cp = min(cands, key=lambda t: (t[0], t[1]))
        if pareto_better(cg, cd, own_g, own_d) and state["offer"].get(lbl) != (cg, cd, cp):
            shutil.copy(cp, os.path.join(out_dir, "reseed_%s.json" % lbl))
            state["offer"][lbl] = (cg, cd, cp)
            log("  reseed offer -> %-16s : %d gates depth %d (from %s)"
                % (lbl, cg, cd, os.path.basename(cp)))


def status_row(meta, procs):
    row = []
    for lbl, m in meta.items():
        st = read_status(m["status_path"])
        bg = st["best_gates"] if st else None
        bd = st["best_depth"] if st else None
        up = "up" if procs[lbl].poll() is None else "DOWN"
        row.append("%s=%s/%s(%s)" % (lbl, bg, bd, up))
    return "  ".join(row)


def cleanup(procs, meta, out_dir, log, state):
    for p in procs.values():
        if p.poll() is None:
            p.terminate()
    time.sleep(2)
    for p in procs.values():
        if p.poll() is None:
            p.kill()
    log("==================== FINAL BESTS ====================")
    for lbl in procs:
        st = read_status(meta[lbl]["status_path"])
        if st:
            log("%-16s depth_cap=%s  best=%s gates @ depth %s"
                % (lbl, st["cap"], st["best_gates"], st["best_depth"]))
    if state["gb"]:
        log("BEST OVERALL: %d gates @ depth %d  -> best_overall.json" % state["gb"])
    log("all circuits + logs in: %s" % out_dir)


def make_run():
    stamp = time.strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(HERE, OUT_ROOT, stamp)
    os.makedirs(out_dir, exist_ok=True)
    # self-archive the EXACT code producing this run (so results are always
    # reproducible from their own folder -- no more in-place-edit ambiguity).
    code_dir = os.path.join(out_dir, "code")
    os.makedirs(code_dir, exist_ok=True)
    for fn in ("mixcolumns_core.py", "engines.py", "worker.py", "ladder_parallel.py"):
        try:
            shutil.copy(os.path.join(HERE, fn), os.path.join(code_dir, fn))
        except Exception:
            pass
    worker_knobs = {w["label"]: w["knobs"] for w in FIXED_WORKERS if w.get("knobs")}
    json.dump({"chunk_s": CHUNK_S, "reseed": RESEED,
               "knobs": {"lns": LNS_KNOBS, "walk": WALK_KNOBS, "anneal3": ANNEAL_KNOBS},
               "worker_knobs": worker_knobs},
              open(os.path.join(out_dir, "config.json"), "w"), indent=2)
    return out_dir


def run_fixed():
    out_dir = make_run()
    masterlog = open(os.path.join(out_dir, "coordinator.log"), "a", buffering=1)
    t0 = time.time()
    def log(msg):
        line = "[%8.1fs %s] %s" % (time.time() - t0, time.strftime("%H:%M:%S"), msg)
        print(line, flush=True); masterlog.write(line + "\n")
    log("FIXED-mode pipeline -> %s" % out_dir)
    log("workers: %s" % [(w["label"], w["engine"], w["depth"]) for w in FIXED_WORKERS])

    procs, meta = {}, {}
    for w in FIXED_WORKERS:
        lbl = w["label"]
        procs[lbl] = launch(lbl, w["engine"], w["depth"], w["start"], out_dir, log,
                            seeds=w.get("seeds"))
        meta[lbl] = {"cap": w["depth"],
                     "status_path": os.path.join(out_dir, "%s_status.json" % lbl),
                     "best_path": os.path.join(out_dir, "%s_best.json" % lbl)}
    state = {"gb": None, "offer": {}}
    try:
        while True:
            time.sleep(POLL_S)
            log("status: " + status_row(meta, procs))
            do_reseed(meta, procs, out_dir, log, state)
            if target_reached(state):
                log("STOP TARGET reached: %d gates @ depth %d -> shutting down" % state["gb"])
                break
    except KeyboardInterrupt:
        log("Ctrl-C: stopping all workers")
    finally:
        cleanup(procs, meta, out_dir, log, state)


def run_cascade():
    out_dir = make_run()
    masterlog = open(os.path.join(out_dir, "coordinator.log"), "a", buffering=1)
    t0 = time.time()
    def log(msg):
        line = "[%8.1fs %s] %s" % (time.time() - t0, time.strftime("%H:%M:%S"), msg)
        print(line, flush=True); masterlog.write(line + "\n")
    log("CASCADE-mode pipeline -> %s" % out_dir)

    procs, meta = {}, {}
    started_at, baseline = {}, {}
    def rl(d): return "d%d" % d

    d0 = DEPTHS[0]; lbl = rl(d0)
    procs[lbl] = launch(lbl, ENGINE_D3 if d0 == 3 else ENGINE_DEEP, d0, "scratch", out_dir, log)
    meta[lbl] = {"cap": d0, "status_path": os.path.join(out_dir, "%s_status.json" % lbl),
                 "best_path": os.path.join(out_dir, "%s_best.json" % lbl)}
    started_at[lbl] = time.time(); baseline[lbl] = DEPTH3_BASELINE
    frontier_idx = 0; final_launched = False
    state = {"gb": None, "offer": {}}
    try:
        while True:
            time.sleep(POLL_S)
            log("status: " + status_row(meta, procs))
            do_reseed(meta, procs, out_dir, log, state)
            if target_reached(state):
                log("STOP TARGET reached: %d gates @ depth %d -> shutting down" % state["gb"])
                break
            if final_launched:
                continue
            fd = DEPTHS[frontier_idx]; flbl = rl(fd)
            st = read_status(meta[flbl]["status_path"])
            best = st["best_gates"] if st and st.get("best_gates") is not None else None
            target = baseline[flbl] - IMPROVE_BY
            elapsed = time.time() - started_at[flbl]
            if not ((best is not None and best <= target) or elapsed >= MAX_WAIT_S):
                continue
            why = ("hit %d<=%d" % (best, target)) if (best is not None and best <= target) \
                else ("timeout %.0fs" % elapsed)
            if not os.path.exists(meta[flbl]["best_path"]):
                started_at[flbl] = time.time(); continue
            seed_file = os.path.join(out_dir, "seed_from_%s.json" % flbl)
            shutil.copy(meta[flbl]["best_path"], seed_file)
            seed_count = best if best is not None else baseline[flbl]
            if frontier_idx + 1 < len(DEPTHS):
                nd = DEPTHS[frontier_idx + 1]; nlbl = rl(nd)
                log("TRIGGER %s (%s, seed=%d) -> launch %s at depth %d" % (flbl, why, seed_count, nlbl, nd))
                procs[nlbl] = launch(nlbl, ENGINE_DEEP, nd, seed_file, out_dir, log)
                meta[nlbl] = {"cap": nd, "status_path": os.path.join(out_dir, "%s_status.json" % nlbl),
                              "best_path": os.path.join(out_dir, "%s_best.json" % nlbl)}
                started_at[nlbl] = time.time(); baseline[nlbl] = seed_count
                frontier_idx += 1
            elif FINAL_UNCAPPED_DEPTH:
                log("TRIGGER %s (%s, seed=%d) -> launch FINAL (uncapped depth)" % (flbl, why, seed_count))
                procs["final"] = launch("final", ENGINE_DEEP, None, seed_file, out_dir, log)
                meta["final"] = {"cap": None, "status_path": os.path.join(out_dir, "final_status.json"),
                                 "best_path": os.path.join(out_dir, "final_best.json")}
                started_at["final"] = time.time(); baseline["final"] = seed_count
                final_launched = True
            else:
                final_launched = True
    except KeyboardInterrupt:
        log("Ctrl-C: stopping all workers")
    finally:
        cleanup(procs, meta, out_dir, log, state)


def main():
    global STOP_GATES, STOP_DEPTH
    parser = argparse.ArgumentParser(
        description="Record-hunting pipeline for AES MixColumns XOR circuits.")
    parser.add_argument("--mode", choices=("cascade", "fixed"), default=MODE,
                        help="cascade = from-scratch depth ladder (default); "
                             "fixed = the shipped sub-89 worker set")
    parser.add_argument("--stop-gates", type=int, default=None, metavar="N",
                        help="stop cleanly once a verified best has <= N gates")
    parser.add_argument("--stop-depth", type=int, default=None, metavar="D",
                        help="stop cleanly once the verified best also has depth <= D")
    args = parser.parse_args()
    STOP_GATES, STOP_DEPTH = args.stop_gates, args.stop_depth

    os.makedirs(os.path.join(HERE, OUT_ROOT), exist_ok=True)
    if args.mode == "fixed":
        run_fixed()
    else:
        run_cascade()


if __name__ == "__main__":
    main()
