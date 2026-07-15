#!/usr/bin/env python3
"""
ladder_parallel.py  --  the record-hunting pipeline (parallel, reseeding).

    python3 ladder_parallel.py

Two modes (set MODE below):

  "fixed"    launch a fixed set of workers at once (each with its own depth cap
             and seed) and let them run in parallel forever, continuously
             re-seeding each other with the best circuits as they appear.
             This is the targeted sub-89 / 89@depth5 attempt.

  "cascade"  the depth ladder: start depth 3 from scratch, and each time the
             frontier rung beats its baseline (or times out) launch the next
             deeper rung seeded from it -- all rungs keep running, all reseed.

Every worker is its own OS process (real parallelism). Every worker
verifies-before-claim and now uses a PARETO tie-break (accept fewer gates, or
equal gates at lower depth) so shallow equal-gate circuits are not lost. The
coordinator maintains best_overall.json and offers each worker the best circuit
that is feasible at its depth cap (reseed_<label>.json), which the worker adopts
between chunks. Stop with Ctrl-C; every best is already on disk.
"""
import os, sys, json, time, shutil, subprocess

# ==========================================================================
# CONFIG  --  edit everything here
# ==========================================================================
import os as _os
OUT_ROOT = "runs_parallel"
MODE = "fixed"                  # "fixed" or "cascade"
#   fixed   = the FIXED_WORKERS set below.
#   cascade = the from-scratch depth ladder (d3 anneal3 up to d11 + uncapped).

# ---- fixed-mode workers: OVERNIGHT DIVERSITY RUN -------------------------
# N independent LNS explorers, all FROM SCRATCH, all UNCAPPED depth, each with a
# DISTINCT RNG seed AND distinct search knobs (kmax / up_prob / snapback) so no
# two settle in the same basin. RESEED is OFF (below) so they never converge --
# this is pure exploration: N independent walks, keep the best of all of them.
# Depth is unconstrained on purpose: once we have a low gate count we can shave
# depth cheaply afterwards (as the seeded short run showed: 89@6 -> 89@5 in 10m).
#
# N_EXPLORERS = one worker per PHYSICAL core, so no two workers share a core and
# each walk runs at full speed. This machine (i7-13700H) has 14 physical cores
# (6 P + 8 E) / 20 logical threads; 14 avoids hyperthreading contention on the
# fast P-cores. Raise toward 16 for more basins (mild HT contention); do NOT use
# 20 (pure oversubscription). os.cpu_count() reports 20 LOGICAL, so we don't use it.
N_EXPLORERS = 14
_KMAX = [4, 6, 8, 10, 5, 7, 9, 6, 8, 10, 4, 12, 6, 8, 5, 9]     # destroy size
_UPP  = [0.3, 0.5, 0.7, 0.4, 0.6, 0.35, 0.55, 0.7, 0.45, 0.5, 0.65, 0.3, 0.6, 0.4, 0.7, 0.5]  # uphill accept
_SNAP = [6, 10, 16, 8, 12, 6, 14, 10, 8, 16, 12, 6, 10, 14, 8, 12]  # wander tolerance
FIXED_WORKERS = [
    dict(label="scratch_%02d" % i, engine="lns", depth=None, start="scratch",
         seeds=[100003 * i + 7],                       # a distinct RNG basin per worker
         knobs=dict(kmax=_KMAX[i % len(_KMAX)],
                    up_prob=_UPP[i % len(_UPP)],
                    snapback=_SNAP[i % len(_SNAP)]))
    for i in range(N_EXPLORERS)
]

# ---- cascade-mode ladder (for a future full run) -------------------------
DEPTHS = [3, 4, 5, 6, 7, 8, 9, 10, 11]
FINAL_UNCAPPED_DEPTH = True
MAX_WAIT_S = 2 * 3600
IMPROVE_BY = 1
DEPTH3_BASELINE = 97
ENGINE_D3 = "anneal3"
ENGINE_DEEP = "lns"

# ---- shared ---------------------------------------------------------------
SEEDS_PER_WORKER = [1, 2, 3]    # default RNG seeds (overridden per-worker above)
POLL_S = 20                     # coordinator status cadence
CHUNK_S = 600                   # worker chunk length (each worker continues from its OWN best)
RESEED = False                  # OFF for the diversity run: explorers stay independent.
                                #   The coordinator still tracks best_overall.json across them.

LNS_KNOBS = dict(kmax=6, kshake=12, snapback=8, nsamp=(24, 24), up_prob=0.5, up_slack=4)
WALK_KNOBS = dict(hub_move_p=0.35, close_hamming=4, repair_hub=40, repair_one=24, plateau_slack_p=0.02)
ANNEAL_KNOBS = dict(anneal_iters=150000, ils_rounds=2500, sa_T0=2.0, sa_T1=0.05)
# ==========================================================================
# END CONFIG
# ==========================================================================

HERE = os.path.dirname(os.path.abspath(__file__))


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
    os.makedirs(os.path.join(HERE, OUT_ROOT), exist_ok=True)
    if MODE == "fixed":
        run_fixed()
    elif MODE == "cascade":
        run_cascade()
    else:
        raise SystemExit("MODE must be 'fixed' or 'cascade'")


if __name__ == "__main__":
    main()
