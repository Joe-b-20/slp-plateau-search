#!/usr/bin/env python3
"""
hunt_worker.py -- one search process of the 87-hunt fleet.

Same shape as pipeline/worker.py (chunked engine loop, verify-before-claim,
per-worker best/status/log files, plateau harvesting into <label>.pop.jsonl)
with the two things this campaign needs added:

  * a ROOT SOURCE per restart instead of a single fixed seed, so a worker that
    has stopped moving abandons its basin instead of grinding it:
        constructor:<name>  a fresh from-scratch root (constructors.py)
        engine:anneal3      the depth-3 partition annealer, run as the root
        pool89              a random diverse 89 (seeds/div89 + the 4,861-state
                            89@depth6 pool)
        file:a.json,b.json  cycle these circuits
        glob:runs/orb*_*g.json   newest/smallest unprocessed match (this is
                            the orbit-space handoff: symmetric circuits get
                            desymmetrised the moment they are loaded as a
                            plain mask set, then polished by the v2 engine)
  * a per-restart best, so "no local improvement for --stall-s" can trigger
    the next restart.  The worker's GLOBAL best (what STATUS.md reports) is
    still the Pareto best over every restart.

Nothing self-stops: the supervisor owns the lifetime of this process.

Usage:
  hunt_worker.py --label L --dir D --root R [--engines alt] [--repel]
                 [--restart-s 5400] [--stall-s 2400] [--seed 1]
"""
import os, sys, json, time, glob, random, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mixcolumns_core as core
import engines
import constructors
from worker import WorkerCtx, pareto_better


# ==========================================================================
# knobs -- the shipped v2 configuration, uncapped (the 88-hunt regime)
# ==========================================================================
LNS_KNOBS = {
    "op_mix": {"small": 0.35, "coneinj": 0.45, "biginj": 0.20},
    "kmax": 4, "cone_lo": 2, "cone_hi": 4, "biginj_lo": 8, "biginj_hi": 16,
    "kshake": 12, "nsamp": [12, 12], "hot_frac": 0.5, "vic_cost": 3,
    "peel_window": 6, "accept": "sa", "sa_T0": 1.2, "sa_cool": 0.9997,
    "sa_reheat": 4000, "up_prob": 0.35, "up_slack": 1, "snapback": 12,
}
WALK_KNOBS = {"hub_move_p": 0.5, "close_hamming": 6, "plateau_slack_p": 0.35}
ANNEAL3_KNOBS = {"anneal_iters": 150000, "ils_rounds": 2500,
                 "sa_T0": 2.0, "sa_T1": 0.05}


class RootCtx(object):
    """Throwaway context used only to capture the best circuit an engine
    produces while it is acting as a ROOT CONSTRUCTOR (anneal3)."""

    def __init__(self, cap, log):
        self.cap = cap
        self.log = log
        self.best_n = None
        self.best_depth = None
        self.best_masks = None

    def improve(self, circuit, masks, note=""):
        v = core.verify(circuit, max_depth=self.cap)
        if not v["ok"]:
            return False
        if not pareto_better(v["gates"], v["depth"], self.best_n, self.best_depth):
            return False
        self.best_n = v["gates"]; self.best_depth = v["depth"]
        self.best_masks = set(masks)
        return True


class LocalCtx(object):
    """Per-restart view of the worker: tracks THIS restart's best (so stalls
    are detectable) and forwards every verified improvement to the global
    WorkerCtx, which applies the campaign Pareto rule across restarts."""

    def __init__(self, ctx):
        self.ctx = ctx
        self.cap = ctx.cap
        self.best_n = None
        self.best_depth = None
        self.best_masks = None
        self.last_improve = time.time()

    def log(self, m):
        self.ctx.log(m)

    def improve(self, circuit, masks, note=""):
        v = core.verify(circuit, max_depth=self.cap)
        if not v["ok"]:
            self.ctx.log("  WARNING candidate REJECTED (outputs=%d/32 depth=%d)"
                         % (v["outputs"], v["depth"]))
            return False
        if not pareto_better(v["gates"], v["depth"], self.best_n, self.best_depth):
            return False
        self.best_n = v["gates"]; self.best_depth = v["depth"]
        self.best_masks = set(masks)
        self.last_improve = time.time()
        self.ctx.improve(circuit, masks, note=note)   # global, may be a no-op
        return True


# ==========================================================================
# root sources
# ==========================================================================
class Roots(object):
    def __init__(self, spec, d, rng, log=None, anneal_s=600.0):
        self.spec = spec
        self.d = d
        self.rng = rng
        self.log = log or (lambda m: None)
        self.anneal_s = anneal_s
        self.n = 0
        self.used = set()
        self.files = []
        if spec.startswith("file:"):
            self.files = [p if os.path.isabs(p) else os.path.join(d, p)
                          for p in spec[5:].split(",")]

    # -- helpers -------------------------------------------------------
    def _pool89(self):
        cands = sorted(glob.glob(os.path.join(self.d, "seeds", "div89", "*.json")))
        if cands and self.rng.random() < 0.35:
            p = self.rng.choice(cands)
            return set(core.load_circuit_masks(p)), os.path.basename(p)
        jl = os.path.join(self.d, "seeds", "pop89_depth6.jsonl")
        if os.path.exists(jl):
            sz = os.path.getsize(jl)
            with open(jl) as f:
                f.seek(self.rng.randrange(max(1, sz - 2)))
                f.readline()                      # drop the partial line
                line = f.readline()
                if not line.startswith("["):
                    f.seek(0); line = f.readline()
            try:
                return set(json.loads(line)), "pop89_depth6"
            except ValueError:
                pass
        if cands:
            p = self.rng.choice(cands)
            return set(core.load_circuit_masks(p)), os.path.basename(p)
        return None, "none"

    def _glob(self, pattern):
        """Least-gates unprocessed match; falls back to re-using the best."""
        pats = os.path.join(self.d, pattern) if not os.path.isabs(pattern) else pattern
        best = None
        for p in sorted(glob.glob(pats)):
            try:
                ms = set(core.load_circuit_masks(p))
            except Exception:
                continue
            key = (p in self.used, len(ms), p)
            if best is None or key < best[0]:
                best = (key, ms, p)
        if best is None:
            return None, "none"
        self.used.add(best[2])
        return best[1], os.path.basename(best[2])

    # -- next root -----------------------------------------------------
    def next(self, seed):
        self.n += 1
        s = self.spec
        if s.startswith("constructor:"):
            name = s.split(":", 1)[1]
            masks, gates, rep = constructors.build(name, seed)
            return masks, "%s#%d (%dg d%d)" % (name, seed, rep["gates"], rep["depth"])
        if s == "engine:anneal3":
            # anneal3 IS the root constructor here: run it depth-capped at 3
            # for a bounded slice, then hand its value-set to the uncapped
            # reduction engines (a depth-3 circuit is a legal start for any cap).
            rc = RootCtx(3, self.log)
            engines.run_engine("anneal3", None, 3, None, self.anneal_s,
                               [seed], dict(ANNEAL3_KNOBS), rc)
            if rc.best_masks is None:
                return core.naive_masks(), "anneal3-failed->naive"
            return set(rc.best_masks), "anneal3#%d (%dg d%d)" % (
                seed, rc.best_n, rc.best_depth)
        if s == "pool89":
            return self._pool89()
        if s.startswith("file:"):
            p = self.files[(self.n - 1) % len(self.files)]
            return set(core.load_circuit_masks(p)), os.path.basename(p)
        if s.startswith("glob:"):
            return self._glob(s[5:])
        raise SystemExit("unknown root spec %r" % s)


# ==========================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--dir", default=HERE)
    ap.add_argument("--root", required=True)
    ap.add_argument("--engines", default="alt",
                    help="'alt' (walk+lns), 'lns', 'walk', or 'anneal3'")
    ap.add_argument("--repel", action="store_true")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--restart-s", type=float, default=5400.0)
    ap.add_argument("--stall-s", type=float, default=2400.0)
    ap.add_argument("--walk-chunk-s", type=float, default=120.0)
    ap.add_argument("--lns-chunk-s", type=float, default=420.0)
    ap.add_argument("--harvest-max", type=int, default=88,
                    help="largest plateau state size written to the harvest")
    ap.add_argument("--anneal-s", type=float, default=600.0,
                    help="seconds of depth-3 annealing per root (root=engine:anneal3)")
    args = ap.parse_args()

    out = os.path.join(args.dir, "runs")
    os.makedirs(out, exist_ok=True)
    stop_path = os.path.join(args.dir, "STOP")

    lns = dict(LNS_KNOBS); walk = dict(WALK_KNOBS)
    lns["harvest_path"] = os.path.join(out, "%s.pop.jsonl" % args.label)
    walk["harvest_path"] = lns["harvest_path"]
    # only sizes the 87-detector consumes are written to disk (see engines.
    # _Harvester): a multi-day fleet that logged every plateau on the way down
    # would burn ~30 GB/day, of which 80% is 89..135-gate states nothing reads.
    lns["harvest_max"] = args.harvest_max
    walk["harvest_max"] = args.harvest_max
    if args.repel:
        rp = os.path.join(args.dir, "repel_masks.json")
        lns["repel_file"] = rp; walk["repel_file"] = rp
        lns["repel_pen"] = 2; lns["repel_up_p"] = 0.25
        walk["repel_up_p"] = 0.25
    knobs = {"lns": lns, "walk": walk, "anneal3": dict(ANNEAL3_KNOBS)}
    cycle = ("walk", "lns") if args.engines == "alt" else (args.engines,)

    ctx = WorkerCtx(args.label, None, out)        # cap=None: uncapped hunt
    ctx.status["root"] = args.root
    ctx.status["repel"] = bool(args.repel)
    ctx.log("hunt worker start: root=%s engines=%s repel=%s seed=%d "
            "restart=%.0fs stall=%.0fs"
            % (args.root, args.engines, args.repel, args.seed,
               args.restart_s, args.stall_s))

    rng = random.Random(args.seed)
    roots = Roots(args.root, args.dir, rng, ctx.log, args.anneal_s)
    seed = args.seed
    restart = 0
    try:
        while not os.path.exists(stop_path):
            restart += 1
            try:
                seed_masks, tag = roots.next(seed)
            except Exception as e:
                ctx.log("  root build FAILED (%s) -- retrying in 20s" % e)
                time.sleep(20); seed = seed + 1013; restart -= 1; continue
            if seed_masks is None:
                # e.g. the orbit handoff before the orbit workers have saved
                # anything yet: wait for material rather than silently falling
                # back to a from-scratch start.
                ctx.log("  no root available from %s yet -- waiting 60s" % args.root)
                ctx.status["root_tag"] = "waiting for %s" % args.root
                ctx._flush_status()
                time.sleep(60); restart -= 1; continue
            ctx.status["restart"] = restart
            ctx.status["root_tag"] = tag
            ctx.log("--- restart %d from %s (rng seed %d) ---" % (restart, tag, seed))
            local = LocalCtx(ctx)
            t_start = time.time()
            chunk = 0
            cur = seed_masks
            while not os.path.exists(stop_path):
                if time.time() - t_start > args.restart_s:
                    ctx.log("  restart budget reached (best %s@%s) -- new root"
                            % (local.best_n, local.best_depth))
                    break
                if time.time() - local.last_improve > args.stall_s:
                    ctx.log("  stalled %.0fs at %s gates -- new root"
                            % (args.stall_s, local.best_n))
                    break
                eng = cycle[chunk % len(cycle)]
                secs = args.walk_chunk_s if eng == "walk" else args.lns_chunk_s
                try:
                    engines.run_engine(eng, cur, None, None, secs, [seed],
                                       knobs[eng], local)
                except Exception as e:
                    ctx.log("  engine %s raised %r -- next chunk" % (eng, e))
                    time.sleep(2)
                if local.best_masks is not None:
                    cur = set(local.best_masks)
                seed += 1
                chunk += 1
            seed += 101
    except KeyboardInterrupt:
        pass
    finally:
        ctx.status["alive"] = False
        ctx._flush_status()
        ctx.log("hunt worker stopped")


if __name__ == "__main__":
    main()
