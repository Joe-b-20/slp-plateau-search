#!/usr/bin/env python3
"""
ladder_parallel.py  --  parallel depth-cascade record hunt.

    python3 ladder_parallel.py

Idea (your experiment):
  * Start a depth-3 search from scratch, running FOREVER (uncapped time).
  * As soon as that search either beats its baseline by a gate OR hits its time
    cap, launch a depth-4 search -- seeded with depth-3's BEST-SO-FAR at that
    moment -- WITHOUT stopping the depth-3 search.
  * Cascade the same rule up depths 4,5,6,7,8,9,10,11, each new depth seeded
    from the previous depth's best at its cutoff, all running in parallel.
  * After depth 11 triggers, launch a FINAL search with uncapped depth AND
    uncapped time.

Every worker is its own OS process (real parallelism, uses your cores). Every
worker verifies before it claims a count and streams its best circuit + status
to disk. The coordinator only watches those status files and launches the next
worker; it never stops a running one.

Theory: climbing depth-by-depth and always warm-starting the looser search from
the tightest circuit found one depth below may guide it into better basins than
searching each depth cold -- and running them in parallel means the deeper
searches get a long head start instead of waiting in series.

Stop the whole thing with Ctrl-C; every worker's best is already on disk.
"""
import os, sys, json, time, subprocess, signal

# ==========================================================================
# CONFIG  --  edit everything here
# ==========================================================================
OUT_ROOT = "runs_parallel"      # results go to runs_parallel/<timestamp>/

DEPTHS = [3, 4, 5, 6, 7, 8, 9, 10, 11]   # ladder rungs, in order
FINAL_UNCAPPED_DEPTH = True     # after the last rung, add an uncapped-depth stage

MAX_WAIT_S = 2 * 3600           # per-rung time cap: advance to the next depth
                                #   after this many seconds even if the gate
                                #   target was not hit. (2 hours.)
IMPROVE_BY = 1                  # advance early once a rung reaches
                                #   (its seed count - IMPROVE_BY) gates, verified.
DEPTH3_BASELINE = 97            # the depth-3 count to beat: rung 3 advances when
                                #   it hits 97 - IMPROVE_BY = 96 (or after MAX_WAIT_S).

SEEDS_PER_WORKER = [1, 2, 3]    # RNG seeds each worker uses (more = more tries,
                                #   more CPU per worker).
POLL_S = 20                     # how often the coordinator checks worker status.

# engine per rung: depth-3 from scratch uses the depth-3 annealer; deeper rungs
# and the final use the general LNS engine, seeded from the previous rung.
ENGINE_D3 = "anneal3"
ENGINE_DEEP = "lns"
# ==========================================================================
# END CONFIG
# ==========================================================================

HERE = os.path.dirname(os.path.abspath(__file__))


def read_status(path):
    try:
        return json.load(open(path))
    except Exception:
        return None


def launch(label, engine, depth, start, out_dir, log):
    seeds = ",".join(str(s) for s in SEEDS_PER_WORKER)
    depth_arg = "none" if depth is None else str(depth)
    cmd = [sys.executable, os.path.join(HERE, "worker.py"),
           label, engine, depth_arg, start, out_dir, seeds]
    logf = open(os.path.join(out_dir, "%s.stdout" % label), "a")
    proc = subprocess.Popen(cmd, cwd=HERE, stdout=logf, stderr=subprocess.STDOUT)
    log("LAUNCH %-8s engine=%s depth=%s start=%s pid=%d"
        % (label, engine, depth_arg, os.path.basename(start) if start != "scratch" else "scratch", proc.pid))
    return proc


def main():
    stamp = time.strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.join(HERE, OUT_ROOT, stamp)
    os.makedirs(out_dir, exist_ok=True)
    masterlog = open(os.path.join(out_dir, "coordinator.log"), "a", buffering=1)
    t0 = time.time()

    def log(msg):
        line = "[%8.1fs %s] %s" % (time.time() - t0, time.strftime("%H:%M:%S"), msg)
        print(line, flush=True)
        masterlog.write(line + "\n")

    log("PARALLEL LADDER -> %s" % out_dir)
    log("depths=%s  final_uncapped=%s  max_wait=%ds  improve_by=%d"
        % (DEPTHS, FINAL_UNCAPPED_DEPTH, MAX_WAIT_S, IMPROVE_BY))

    procs = {}                      # label -> Popen
    started_at = {}                 # label -> launch time
    baseline = {}                   # label -> seed gate count (target = baseline - IMPROVE_BY)
    status_path = {}                # label -> status.json path
    best_path = {}                  # label -> best.json path

    def rung_label(d):
        return "d%d" % d

    # --- launch the first rung (depth 3, from scratch) ---
    d0 = DEPTHS[0]
    lbl = rung_label(d0)
    procs[lbl] = launch(lbl, ENGINE_D3 if d0 == 3 else ENGINE_DEEP, d0, "scratch", out_dir, log)
    started_at[lbl] = time.time()
    baseline[lbl] = DEPTH3_BASELINE
    status_path[lbl] = os.path.join(out_dir, "%s_status.json" % lbl)
    best_path[lbl] = os.path.join(out_dir, "%s_best.json" % lbl)

    frontier_idx = 0                # index into DEPTHS of the deepest launched rung
    final_launched = False

    try:
        while True:
            time.sleep(POLL_S)

            # periodic snapshot of every worker
            row = []
            for lbl in procs:
                st = read_status(status_path.get(lbl, ""))
                bg = st["best_gates"] if st else None
                bd = st["best_depth"] if st else None
                alive = "up" if procs[lbl].poll() is None else "DOWN"
                row.append("%s=%s/%s(%s)" % (lbl, bg, bd, alive))
            log("status: " + "  ".join(row))

            if final_launched:
                continue            # everything is launched; just keep watching

            # is the current frontier rung ready to trigger the next?
            fd = DEPTHS[frontier_idx]
            flbl = rung_label(fd)
            st = read_status(status_path[flbl])
            best = st["best_gates"] if st and st["best_gates"] is not None else None
            target = baseline[flbl] - IMPROVE_BY
            elapsed = time.time() - started_at[flbl]
            hit = best is not None and best <= target
            timed = elapsed >= MAX_WAIT_S
            if not (hit or timed):
                continue

            why = ("hit %d<=%d" % (best, target)) if hit else ("timeout %.0fs" % elapsed)
            seed_count = best if best is not None else baseline[flbl]

            # snapshot the frontier's current best as the seed for the next rung
            if not os.path.exists(best_path[flbl]):
                log("frontier %s has no verified circuit yet; waiting" % flbl)
                started_at[flbl] = time.time()   # reset its clock; try again
                continue
            seed_file = os.path.join(out_dir, "seed_from_%s.json" % flbl)
            with open(best_path[flbl]) as f:
                seed_data = f.read()
            with open(seed_file, "w") as f:
                f.write(seed_data)

            if frontier_idx + 1 < len(DEPTHS):
                nd = DEPTHS[frontier_idx + 1]
                nlbl = rung_label(nd)
                log("TRIGGER %s (%s, seed=%d) -> launch %s at depth %d"
                    % (flbl, why, seed_count, nlbl, nd))
                procs[nlbl] = launch(nlbl, ENGINE_DEEP, nd, seed_file, out_dir, log)
                started_at[nlbl] = time.time()
                baseline[nlbl] = seed_count
                status_path[nlbl] = os.path.join(out_dir, "%s_status.json" % nlbl)
                best_path[nlbl] = os.path.join(out_dir, "%s_best.json" % nlbl)
                frontier_idx += 1
            elif FINAL_UNCAPPED_DEPTH:
                log("TRIGGER %s (%s, seed=%d) -> launch FINAL (uncapped depth)"
                    % (flbl, why, seed_count))
                procs["final"] = launch("final", ENGINE_DEEP, None, seed_file, out_dir, log)
                started_at["final"] = time.time()
                baseline["final"] = seed_count
                status_path["final"] = os.path.join(out_dir, "final_status.json")
                best_path["final"] = os.path.join(out_dir, "final_best.json")
                final_launched = True
            else:
                log("ladder complete (no final stage configured)")
                final_launched = True
    except KeyboardInterrupt:
        log("Ctrl-C: stopping all workers")
    finally:
        for lbl, p in procs.items():
            if p.poll() is None:
                p.terminate()
        time.sleep(2)
        for lbl, p in procs.items():
            if p.poll() is None:
                p.kill()
        # final summary
        log("==================== FINAL BESTS ====================")
        for lbl in procs:
            st = read_status(status_path.get(lbl, ""))
            if st:
                log("%-8s depth_cap=%s  best=%s gates @ depth %s"
                    % (lbl, st["cap"], st["best_gates"], st["best_depth"]))
        log("all circuits + logs in: %s" % out_dir)


if __name__ == "__main__":
    main()
