#!/usr/bin/env python3
"""
orbit_runner.py -- one orbit-space (rho^2-equivariant) worker of the fleet.

Runs orbit_search.py's ladder in-process, forever, rotating over (seed, rng,
mode) so a single OS process covers the whole orbit lane.  Two things matter
for the 87-hunt:

  * 87 has the natural symmetric shape 43*2 + 1, so the symmetric subspace is
    exactly half the dimension and IS reachable in principle -- the orbit
    record is 90 and every orbit 90 is certified locally optimal, which is
    why this lane runs `mixed` (a small loose-mask budget) as often as `sym`;
  * every circuit it saves is a plain mask set on disk.  Loading one with
    mixcolumns_core.load_circuit_masks throws the symmetry away, so the
    polish worker (root=glob:runs/orb*_*g.json) IS the desymmetrise-and-
    polish handoff: the v2 engine takes the symmetric circuit apart with no
    equivariance constraint and its harvest flows to the 87-detector.

Roots: seeds/orbit/*.json (the two rho^2-symmetric 90s and the symmetric 94)
plus, every third cycle, a random DIVERSE 89 from the fleet's 89 pool --
symmetrising a 89 from another basin lands in an orbit basin nobody has run.

Usage: orbit_runner.py --label o1 --dir D --seed 1 [--tlim 900]
"""
import os, sys, glob, time, json, random, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mixcolumns_core as core
import orbit_search


def pick_seed(d, rng, cycle):
    """Return a path to a circuit to symmetrise."""
    orb = sorted(glob.glob(os.path.join(d, "seeds", "orbit", "*.json")))
    if cycle % 3 == 2:
        div = sorted(glob.glob(os.path.join(d, "seeds", "div89", "*.json")))
        if div:
            return rng.choice(div)
    if orb:
        # NOTE (2026-07-29): `orb[cycle % len(orb)]` made index 2 unreachable --
        # that index is only selected when cycle%3==2, which the div89 branch
        # above already consumed. With 3 orbit seeds that permanently hid
        # sym94.json, the ONLY from-scratch (own-lineage) orbit seed: every
        # orbit cycle started from sym90_a/sym90_b, both of which descend from
        # Jean's imported 88 (see seeds/orbit/PROVENANCE.md). That is how the
        # 88@5 came out derived. Count only the cycles that reach here, so all
        # seeds rotate: cycles 0,1,3,4,6,7,... -> indices 0,1,2,0,1,2,...
        return orb[(cycle - cycle // 3) % len(orb)]
    raise SystemExit("no orbit seeds under seeds/orbit/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--dir", default=HERE)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--tlim", type=float, default=900.0)
    ap.add_argument("--modes", default="mixed,sym")
    args = ap.parse_args()

    out = os.path.join(args.dir, "runs")
    os.makedirs(out, exist_ok=True)
    logp = os.path.join(args.dir, "runs", "%s.log" % args.label)
    lf = open(logp, "a", buffering=1)
    status_path = os.path.join(out, "%s_status.json" % args.label)
    stop_path = os.path.join(args.dir, "STOP")
    t0 = time.time()
    modes = args.modes.split(",")
    rng = random.Random(args.seed)

    def log(m):
        line = "[%8.1fs %s] %s" % (time.time() - t0, time.strftime("%H:%M:%S"), m)
        print(line, flush=True)
        lf.write(line + "\n")

    best = {"g": None, "d": None}

    def flush_status(extra=None):
        st = {"label": args.label, "cap": None, "pid": os.getpid(),
              "best_gates": best["g"], "best_depth": best["d"],
              "started": t0, "updated": time.time(), "alive": True,
              "kind": "orbit"}
        if extra:
            st.update(extra)
        tmp = status_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(st, f)
        os.replace(tmp, status_path)

    def scan_best():
        for p in glob.glob(os.path.join(out, "%s_*g.json" % args.label)):
            try:
                obj = json.load(open(p))
            except Exception:
                continue
            g = obj.get("gateCount"); d = obj.get("depth")
            if g is not None and (best["g"] is None or g < best["g"]):
                best["g"] = g; best["d"] = d

    log("orbit worker start: label=%s tlim=%.0fs modes=%s" % (args.label, args.tlim, modes))
    flush_status()
    cycle = 0
    try:
        while not os.path.exists(stop_path):
            seedp = pick_seed(args.dir, rng, cycle)
            mode = modes[cycle % len(modes)]
            rngi = args.seed * 1000 + cycle
            tag = "%s_c%d" % (args.label, cycle)
            log("--- cycle %d: seed=%s mode=%s rng=%d ---"
                % (cycle, os.path.basename(seedp), mode, rngi))
            try:
                orbit_search.main(["--seed", seedp, "--mode", mode,
                                   "--rng", str(rngi), "--tlim", str(args.tlim),
                                   "--loose", "3", "--out", tag,
                                   "--outdir", out, "--phase", "90"])
            except SystemExit as e:
                log("orbit_search exited: %s" % e)
            except Exception as e:
                log("orbit_search raised %r -- next cycle" % e)
                time.sleep(5)
            scan_best()
            flush_status({"cycle": cycle})
            cycle += 1
    except KeyboardInterrupt:
        pass
    finally:
        flush_status({"alive": False})
        log("orbit worker stopped")


if __name__ == "__main__":
    main()
