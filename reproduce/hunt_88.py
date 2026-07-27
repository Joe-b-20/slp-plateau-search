#!/usr/bin/env python3
"""
hunt_88.py  --  single-worker, single-core re-run of the search that found the
88 @ depth 7, from the same seed, with the same engine and the same knobs.

    python3 hunt_88.py                 # 45 min budget, the record worker's RNG
    python3 hunt_88.py --minutes 120   # longer budget
    python3 hunt_88.py --target 87     # don't stop at 88 (the real 87 hunt is
                                       # ../pipeline --mode fixed --workers hunt87)

This is NOT a copy of the search code.  The 88 came out of the pipeline, so
this file only *aims* the pipeline: it writes the shipped configuration into a
run folder and launches ONE `../pipeline/worker.py` process on the exact seed
the record worker used, then polls its status file and stops it as soon as the
oracle-verified best reaches the target (or the budget runs out).  The knobs
come from `../pipeline/ladder_parallel.py` by import, so they cannot drift from
the shipped ones.

What it reproduces, honestly (see ../evidence/RESULTS.md for the full lineage):
the archived 88 @ depth 7 was found by worker `w10_sym94` of a 10-worker,
8 400 s hunt on 2026-07-26 -- `alt` mode (alternating walk and lns chunks),
RNG 1010, seeded with the exactly rho^2-symmetric 94 @ depth 5 circuit -- at
t = 1 973 s (32.9 min), and the walk's Pareto tie-break took the same 88 masks
down to depth 7 five seconds later.  Every improvement on that worker came out
of its own walk chunks, so a single worker is a fair re-run of it; what a
single worker does NOT reproduce is the other nine workers' share of the luck.
This is a stochastic search: a re-run can take much longer than the archived
one, or not get there at all inside a budget.  Two re-runs on 2026-07-27 took
19.4 and 31.0 minutes; the details, and what does and does not reproduce
iteration-for-iteration, are in README.md.

The seed circuit is our own lineage (89@5 -> rho^2-symmetrized 94), so nothing
this worker produces is derived from published work -- cross-pollination is off
here, as in the shipped configuration.
"""

# ==========================================================================
# CONFIG  --  edit everything here
# ==========================================================================

# The seed: the exactly rho^2-symmetric 94 @ depth 5 of our own lineage, kept
# with the run archive of the record it produced.  It is not in
# ../pipeline/seeds/ because it is not part of a shipped worker set.
SEED = "../evidence/campaign87_run_2026-07-26_got_88at7/seed_rho2sym_94gates_depth5.json"

TARGET_GATES = 88      # stop as soon as a VERIFIED best has this many gates
TARGET_DEPTH = 7       # ...AND this depth, or better.  Both bounds matter: the
                       # walk finds the 88 masks at some large depth first and
                       # the Pareto tie-break walks the same size down to depth
                       # 7 a few seconds later, so stopping on the gate count
                       # alone hands back an 88 at depth 8-11.
MINUTES      = 45      # wall-clock budget; the archived worker took 32.9 min
                       # of an 8 400 s (140 min) budget
ENGINE       = "alt"   # the record worker's mode: 300 s walk / 600 s lns chunks
DEPTH_CAP    = None    # uncapped, as the record worker ran (the 88 first
                       # appeared at depth 11 and was tie-broken to depth 7)
RNG_SEEDS    = [1010]  # the record worker's RNG seeds
KEEP_RUN_DIR = False   # True = keep the run folder (logs + the harvested
                       # plateau population, which grows by MBs per minute)

# ==========================================================================
# END CONFIG  --  implementation below
# ==========================================================================

import argparse, json, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.join(os.path.dirname(HERE), "pipeline")
sys.path.insert(0, PIPE)

import ladder_parallel as L          # the shipped knobs, by import (no copy)
import mixcolumns_core as core       # the pipeline's copy -- byte-identical to
                                     # this folder's, so the oracle is the same

LABEL = "repro88_sym94"


def make_run_dir():
    """A run folder shaped exactly like a pipeline run: config.json + code/."""
    stamp = time.strftime("%Y-%m-%d_%H%M%S")
    out_dir = os.path.join(PIPE, "runs_parallel", "repro88_" + stamp)
    os.makedirs(os.path.join(out_dir, "code"), exist_ok=True)
    for fn in ("mixcolumns_core.py", "engines.py", "worker.py", "ladder_parallel.py"):
        shutil.copy(os.path.join(PIPE, fn), os.path.join(out_dir, "code", fn))
    shutil.copy(os.path.abspath(__file__), os.path.join(out_dir, "code", "hunt_88.py"))
    with open(os.path.join(out_dir, "config.json"), "w") as f:
        json.dump({"chunk_s": L.CHUNK_S, "walk_chunk_s": L.WALK_CHUNK_S,
                   "reseed": False,      # one worker: nobody to reseed from
                   "knobs": {"lns": L.LNS_KNOBS, "walk": L.WALK_KNOBS,
                             "anneal3": L.ANNEAL_KNOBS},
                   "worker_knobs": {}}, f, indent=2)
    return out_dir


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--minutes", type=float, default=MINUTES,
                    help="wall-clock budget (default %(default)s)")
    ap.add_argument("--target", type=int, default=TARGET_GATES,
                    help="stop at this verified gate count (default %(default)s)")
    ap.add_argument("--target-depth", type=int, default=TARGET_DEPTH,
                    help="...and this depth (default %(default)s; 0 = any depth)")
    ap.add_argument("--seed-circuit", default=SEED,
                    help="circuit JSON to start from (default: the record's rho^2-symmetric 94)")
    ap.add_argument("--rng", default=",".join(str(s) for s in RNG_SEEDS),
                    help="comma-separated RNG seeds (default %(default)s, the record worker's)")
    ap.add_argument("--keep", action="store_true", default=KEEP_RUN_DIR,
                    help="keep the run folder (logs + harvested population)")
    args = ap.parse_args()

    start = os.path.abspath(os.path.join(HERE, args.seed_circuit)) \
        if not os.path.isabs(args.seed_circuit) else args.seed_circuit
    if not os.path.exists(start):
        sys.exit("seed circuit not found: %s" % start)
    sv = core.verify(json.load(open(start))["gates"])
    print("seed: %s\n      %d gates, depth %d, outputs %d/32"
          % (os.path.relpath(start, HERE), sv["gates"], sv["depth"], sv["outputs"]),
          flush=True)

    out_dir = make_run_dir()
    print("run folder: %s" % os.path.relpath(out_dir, HERE), flush=True)
    proc = subprocess.Popen(
        [sys.executable, os.path.join(PIPE, "worker.py"), LABEL, ENGINE,
         "none" if DEPTH_CAP is None else str(DEPTH_CAP), start, out_dir, args.rng],
        cwd=PIPE, stdout=open(os.path.join(out_dir, "%s.stdout" % LABEL), "a"),
        stderr=subprocess.STDOUT)
    print("worker pid %d: engine=%s depth=%s rng=%s target=%d gates @ depth %s "
          "budget=%.0f min"
          % (proc.pid, ENGINE, DEPTH_CAP, args.rng, args.target,
             args.target_depth if args.target_depth > 0 else "any", args.minutes),
          flush=True)

    status_path = os.path.join(out_dir, "%s_status.json" % LABEL)
    best_path = os.path.join(out_dir, "%s_best.json" % LABEL)
    t0 = time.time(); deadline = t0 + args.minutes * 60.0
    seen = None; hit = None; first_size = None
    try:
        while time.time() < deadline and proc.poll() is None:
            time.sleep(1.0)
            try:
                with open(status_path) as f:
                    st = json.load(f)
            except Exception:
                continue
            g, d = st.get("best_gates"), st.get("best_depth")
            if g is None or (g, d) == seen:
                continue
            seen = (g, d)
            print("  [%7.1fs] verified best: %d gates, depth %d" % (time.time() - t0, g, d),
                  flush=True)
            if g > args.target:
                continue
            if first_size is None:
                first_size = (time.time() - t0, g, d)
            if args.target_depth <= 0 or d <= args.target_depth:
                hit = (time.time() - t0, g, d)
                break
    except KeyboardInterrupt:
        print("  interrupted", flush=True)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=30)
        except Exception:
            proc.kill()

    print("=" * 72)
    if first_size:
        secs, g, d = first_size
        print("%d gates first reached at depth %d after %.1f s (%.1f min)"
              % (g, d, secs, secs / 60.0))
    if hit:
        secs, g, d = hit
        print("REACHED %d gates at depth %d after %.1f s (%.1f min)" % (g, d, secs, secs / 60.0))
    elif seen:
        print("budget spent (%.1f min); best reached: %d gates at depth %d"
              % ((time.time() - t0) / 60.0, seen[0], seen[1]))
        print("the search is stochastic -- a longer budget or another RNG may get there")
    else:
        print("budget spent (%.1f min); the worker never improved on its seed"
              % ((time.time() - t0) / 60.0))
    if os.path.exists(best_path):
        dest = os.path.join(HERE, "out_88hunt.json")
        shutil.copy(best_path, dest)
        v = core.verify(json.load(open(dest))["gates"])
        print("best circuit -> out_88hunt.json  (oracle: %d gates, depth %d, %d/32 outputs, %s)"
              % (v["gates"], v["depth"], v["outputs"], "VALID" if v["ok"] else "INVALID"))
        print("re-check it yourself:  python3 ../verify_circuit.py out_88hunt.json %d" % v["depth"])
    if args.keep:
        print("run folder kept: %s" % out_dir)
    else:
        shutil.rmtree(out_dir, ignore_errors=True)
    print("=" * 72)


if __name__ == "__main__":
    main()
