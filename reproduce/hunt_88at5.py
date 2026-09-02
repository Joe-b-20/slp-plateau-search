#!/usr/bin/env python3
"""
hunt_88at5.py  --  single-worker, single-core re-run of the FROM-SCRATCH search
that found the 88 @ depth 5, from the same root, with the same code and knobs.

    python3 hunt_88at5.py                  # 180 min budget; archived: 64 min
    python3 hunt_88at5.py --minutes 360    # longer budget
    python3 hunt_88at5.py --target-depth 6 # stop at the intermediate 88 @ 6

There is no seed circuit.  The root is `constructors.build("naive", 1958)` --
a randomized XOR tree over the 32 raw inputs, a pure function of the integer
1958 -- which re-derives the record run's own root, 146 gates at depth 3,
exactly.  From that root the archived worker reached 88 @ depth 6 in 64 minutes
and 88 @ depth 5 six seconds later, by the Pareto depth tie-break.

This file contains NO search code.  It launches ONE process of the ARCHIVED
worker that produced the record --
`../evidence/campaign87_run_2026-07-28_got_88at6_fromscratch/code/hunt_worker.py`,
hash-pinned by the record's own archive and published two days BEFORE the find
-- polls its status file, and stops it as soon as an oracle-verified best
reaches the target.  Nothing is copied and no knob is restated here: the LNS and
walk knobs, the 120 s / 420 s `alt` chunk cycle and the uncapped depth all come
from that archived file, so they cannot drift from the ones that ran.

WHAT REPRODUCES EXACTLY, AND WHAT DOES NOT.  The record's restart is session 5,
restart 16 of a five-session worker, opened on root `naive#1958` with RNG seed
1958 (`--- restart 16 from naive#1958 (146g d3) (rng seed 1958) ---` in
`../evidence/campaign87_run_2026-07-30_got_88at5_fromscratch/runs_hunt/c_naive.log`).
The engines take that integer, not the worker's RNG object, and it advances by
+1 per chunk -- so starting a fresh worker with `--seed 1958` puts restart 1 in
exactly restart 16's state, and the root and the first chunk are reproduced.
Chunk boundaries are WALL-CLOCK (120 s walk / 420 s LNS), so from the second
chunk on a machine of a different speed is at a different iteration and the
trajectories part.  This is a stochastic search: a re-run can be faster, much
slower, or miss inside a budget.

PROVENANCE.  The root reads nothing off disk; cross-pollination and repulsion
are off; the producing engine (`engine_walk`) has no candidate pool and no disk
read path.  Nothing this worker produces is derived from published work.  The
full five-part argument is in the record's `PROVENANCE.md`.
"""

# ==========================================================================
# CONFIG  --  edit everything here
# ==========================================================================

# The archived worker + engines + constructors that produced the record.  They
# are byte-identical to (and hash-pinned by) the from-scratch 88 @ depth 5
# archive's own code manifest; the 88 @ depth 6 archive is where they live.
ARCHIVE = "../evidence/campaign87_run_2026-07-28_got_88at6_fromscratch/code"

ROOT_SPEC    = "constructor:naive"   # a pure function of the integer below
RNG_SEED     = 1958                  # the record restart's root AND chunk seed
TARGET_GATES = 88      # stop as soon as a VERIFIED best has this many gates
TARGET_DEPTH = 5       # ...AND this depth, or better.  Both bounds matter: the
                       # walk reaches the 88 masks at depth 6 first and the
                       # Pareto tie-break carries the same size to depth 5 a few
                       # seconds later (6.1 s, in the archived run).
MINUTES      = 180     # wall-clock budget; the archived descent from this root
                       # took 64 min (69 192.7 s - 65 349.0 s of session 5)
KEEP_ROOT    = True    # hold the record's root for the whole budget.
                       #
                       # WHY THIS IS NOT A DEFAULT OF THE ARCHIVED WORKER.  That
                       # worker rotates roots: --restart-s 5400 abandons a root
                       # after 90 min, and --stall-s 2400 abandons it after 40
                       # min with no local improvement.  Those are right for a
                       # 16-worker fleet mining many roots for days, and WRONG
                       # for this script, whose entire job is to re-run ONE
                       # restart.  Measured here 2026-09-02: on an idle fast
                       # core the walk takes this root to 89 gates in 559 s and
                       # then needs a lucky walk chunk, so the 2400 s stall
                       # clock expired at t = 3240 s (54 min) and the worker
                       # dropped the record's root -- 10 min BEFORE the time the
                       # archived descent took to reach 88 from it.  The
                       # archived run survived its own stall rule only because
                       # it was slower: on a loaded box its improvements were
                       # spread over 3072 s rather than 559 s.
                       #
                       # So both timers are set to the budget, and the root is
                       # held.  Set False to get the archived worker's own
                       # rotation instead, which past ~40-90 min stops being a
                       # re-run of this restart and becomes an open-ended hunt.
KEEP_RUN_DIR = False   # True = keep the run folder (log, status, and the
                       # harvested plateau population)

# ==========================================================================
# END CONFIG  --  implementation below
# ==========================================================================

import argparse, json, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PIPE = os.path.join(ROOT, "pipeline")
ARCH = os.path.abspath(os.path.join(HERE, ARCHIVE))

sys.path.insert(0, HERE)
import mixcolumns_core as core        # byte-identical to the pipeline's copy

LABEL = "c_naive"                     # the record worker's own label


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--minutes", type=float, default=MINUTES,
                    help="wall-clock budget (default %(default)s)")
    ap.add_argument("--target", type=int, default=TARGET_GATES,
                    help="stop at this verified gate count (default %(default)s)")
    ap.add_argument("--target-depth", type=int, default=TARGET_DEPTH,
                    help="...and this depth (default %(default)s; 0 = any depth)")
    ap.add_argument("--rng", type=int, default=RNG_SEED,
                    help="root + chunk seed (default %(default)s, the record restart's)")
    ap.add_argument("--keep", action="store_true", default=KEEP_RUN_DIR,
                    help="keep the run folder (log + harvested population)")
    ap.add_argument("--rotate-roots", action="store_true", default=not KEEP_ROOT,
                    help="use the archived worker's own root rotation "
                         "(--restart-s 5400 / --stall-s 2400) instead of "
                         "holding the record's root for the whole budget")
    args = ap.parse_args()

    worker = os.path.join(ARCH, "hunt_worker.py")
    if not os.path.exists(worker):
        sys.exit("archived worker not found: %s" % worker)

    # The root, re-derived here before anything is launched: a pure function of
    # the integer, and the number the record's log recorded for it.
    sys.path.insert(0, ARCH)
    import constructors
    _, _, rep = constructors.build("naive", args.rng)
    print("root: constructors.build(\"naive\", %d) -> %d gates, depth %d "
          "(no seed circuit; from scratch)" % (args.rng, rep["gates"], rep["depth"]),
          flush=True)
    if args.rng == RNG_SEED and (rep["gates"], rep["depth"]) != (146, 3):
        print("  WARNING: the record's log says 146 gates at depth 3 for this seed",
              flush=True)

    stamp = time.strftime("%Y-%m-%d_%H%M%S")
    out_dir = os.path.join(HERE, "runs_88at5_" + stamp)
    os.makedirs(out_dir, exist_ok=True)
    print("run folder: %s" % os.path.relpath(out_dir, HERE), flush=True)

    env = dict(os.environ)
    # `hunt_worker.py` imports WorkerCtx/pareto_better from the pipeline's
    # `worker.py`; everything else it needs sits beside it in the archive.
    env["PYTHONPATH"] = PIPE + os.pathsep + env.get("PYTHONPATH", "")
    cmd = [sys.executable, worker, "--label", LABEL, "--dir", out_dir,
           "--root", ROOT_SPEC, "--seed", str(args.rng)]
    if not args.rotate_roots:
        # Hold this root for the whole budget: both of the archived worker's
        # root-rotation timers are pushed past the deadline.  See KEEP_ROOT.
        secs = args.minutes * 60.0 + 600.0
        cmd += ["--restart-s", repr(secs), "--stall-s", repr(secs)]
    proc = subprocess.Popen(
        cmd, cwd=ARCH, env=env,
        stdout=open(os.path.join(out_dir, "%s.stdout" % LABEL), "a"),
        stderr=subprocess.STDOUT)
    print("worker pid %d: %s  root=%s seed=%d  target=%d gates @ depth %s  "
          "budget=%.0f min  roots=%s"
          % (proc.pid, os.path.relpath(worker, ROOT), ROOT_SPEC, args.rng,
             args.target, args.target_depth if args.target_depth > 0 else "any",
             args.minutes,
             "rotating (archived defaults)" if args.rotate_roots
             else "this one, held for the budget"), flush=True)

    runs = os.path.join(out_dir, "runs")
    status_path = os.path.join(runs, "%s_status.json" % LABEL)
    best_path = os.path.join(runs, "%s_best.json" % LABEL)
    stop_path = os.path.join(out_dir, "STOP")
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
            print("  [%7.1fs] verified best: %d gates, depth %d"
                  % (time.time() - t0, g, d), flush=True)
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
        open(stop_path, "w").close()          # the worker's own graceful stop
        try:
            proc.wait(timeout=30)
        except Exception:
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
        print("REACHED %d gates at depth %d after %.1f s (%.1f min)"
              % (g, d, secs, secs / 60.0))
        print("archived, from the same root: 88 @ depth 6 at 64.1 min, "
              "88 @ depth 5 at 64.2 min")
    elif seen:
        print("budget spent (%.1f min); best reached: %d gates at depth %d"
              % ((time.time() - t0) / 60.0, seen[0], seen[1]))
        print("the search is stochastic -- a longer budget or another root may get there")
    else:
        print("budget spent (%.1f min); the worker never reported a verified best"
              % ((time.time() - t0) / 60.0))
    if os.path.exists(best_path):
        dest = os.path.join(HERE, "out_88at5.json")
        shutil.copy(best_path, dest)
        v = core.verify(json.load(open(dest))["gates"])
        print("best circuit -> out_88at5.json  (oracle: %d gates, depth %d, "
              "%d/32 outputs, %s)"
              % (v["gates"], v["depth"], v["outputs"], "VALID" if v["ok"] else "INVALID"))
        print("re-check it yourself:  python3 ../verify_circuit.py out_88at5.json %d"
              % v["depth"])
    if args.keep:
        print("run folder kept: %s" % out_dir)
    else:
        shutil.rmtree(out_dir, ignore_errors=True)
    print("=" * 72)


if __name__ == "__main__":
    main()
