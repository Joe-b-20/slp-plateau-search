#!/usr/bin/env python3
"""
hunt_worker.py -- one long-hunt worker for the merged engine (wave-2).

Runs the merged lns (or walk) engine in chunks from a seed circuit, reseeding
each chunk from its own best, bumping the RNG each chunk.  Writes:
  <out>/<label>_best.json    best VERIFIED circuit so far
  <out>/<label>_status.json  live status
  <out>/<label>.log          log
  <out>/<label>.pop.jsonl    harvested plateau population (one mask list/line)
Cross-pollinates from <out>/*.pop.jsonl of sibling workers.

Usage:
  python3 hunt_worker.py <label> <engine> <seedfile> <out_dir> <rng> <total_s> \
      [knobs_json]
"""
import os, sys, json, time
import mixcolumns_core as core
import engines


def atomic_write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f)
    os.replace(tmp, path)


def pareto_better(g2, d2, g1, d1):
    if g1 is None:
        return True
    return g2 < g1 or (g2 == g1 and d2 < d1)


class Ctx:
    def __init__(self, label, out_dir):
        self.label = label
        self.cap = None
        self.best_path = os.path.join(out_dir, "%s_best.json" % label)
        self.status_path = os.path.join(out_dir, "%s_status.json" % label)
        self.logf = open(os.path.join(out_dir, "%s.log" % label), "a", buffering=1)
        self.t0 = time.time()
        self.best_n = None
        self.best_depth = None
        self.best_masks = None
        self.iters = 0

    def _flush_status(self):
        atomic_write_json(self.status_path,
                          {"label": self.label, "pid": os.getpid(),
                           "best_gates": self.best_n,
                           "best_depth": self.best_depth,
                           "updated": time.time(), "t0": self.t0})

    def log(self, msg):
        line = "[%8.1fs %s] %s" % (time.time() - self.t0,
                                   time.strftime("%H:%M:%S"), msg)
        self.logf.write(line + "\n")
        self._flush_status()

    def improve(self, circuit, masks, note=""):
        v = core.verify(circuit, max_depth=None)
        if not v["ok"]:
            self.log("  WARNING candidate REJECTED -- not claimed")
            return False
        if not pareto_better(v["gates"], v["depth"], self.best_n, self.best_depth):
            return False
        self.best_n = v["gates"]; self.best_depth = v["depth"]
        self.best_masks = set(masks)
        core.save(circuit, self.best_path,
                  extra={"depth": v["depth"], "verified": True, "cap": None})
        self.log("  NEW BEST %d gates depth %d VERIFIED %s" %
                 (v["gates"], v["depth"], note))
        if v["gates"] <= 88:
            flag = os.path.join(os.path.dirname(self.best_path),
                                "ALERT_%s_%dgates.json" % (self.label, v["gates"]))
            core.save(circuit, flag, extra={"depth": v["depth"], "verified": True})
        self._flush_status()
        return True


def _jac(A, B):
    return len(A & B) / len(A | B)


def main():
    label, engine, seedfile, out_dir = sys.argv[1:5]
    rng0 = int(sys.argv[5]); total_s = float(sys.argv[6])
    knobs_extra = json.loads(sys.argv[7]) if len(sys.argv) > 7 else {}

    os.makedirs(out_dir, exist_ok=True)
    ctx = Ctx(label, out_dir)

    # drift mode (wave-3 hunt-deeper): reseed each chunk from the most
    # family-DISTANT harvested best-size state instead of the frozen best.
    drift_refs = knobs_extra.pop("drift_refs", None)
    drift = None
    if drift_refs:
        refs = json.load(open(drift_refs))
        drift = {"refs": [set(v) for v in refs.values()],
                 "off": 0, "best": None, "bestJ": 9.9}

    def drift_pick(pop_path, want_n):
        """Chained outward drift: take the most family-distant state of size
        want_n harvested since the LAST call (this chunk's excursion tip);
        accept it if within +0.05 of the global record distance, else fall
        back to the global record state."""
        try:
            f = open(pop_path)
        except OSError:
            return None
        f.seek(drift["off"])
        data = f.read(); f.close()
        end = data.rfind("\n")
        if end < 0:
            return drift["best"]
        drift["off"] += end + 1
        wbest = None; wJ = 9.9
        for line in data[:end].split("\n"):
            try:
                ms = json.loads(line)
            except ValueError:
                continue
            if len(ms) != want_n:
                continue
            S = set(ms)
            jb = max(_jac(S, R) for R in drift["refs"])
            if jb < wJ:
                wJ = jb; wbest = S
        if wbest is not None and wJ <= drift["bestJ"] + 0.05:
            if wJ < drift["bestJ"]:
                drift["bestJ"] = wJ
            drift["best"] = wbest
        return drift["best"]
    lns_knobs = dict(kmax=4, kshake=12, snapback=12, nsamp=(12, 12),
                     up_prob=0.5, up_slack=4,
                     harvest_path=os.path.join(out_dir, "%s.pop.jsonl" % label),
                     pop_glob=os.path.join(out_dir, "*.pop.jsonl"),
                     pop_period_s=120.0)
    walk_knobs = dict(hub_move_p=0.3, close_hamming=8, repair_one=40,
                      repair_hub=24, plateau_slack_p=0.15,
                      harvest_path=os.path.join(out_dir, "%s.pop.jsonl" % label))
    lns_knobs.update(knobs_extra.get("lns", knobs_extra) if engine != "walk" else {})
    walk_knobs.update(knobs_extra.get("walk", {}) if engine == "alt"
                      else (knobs_extra if engine == "walk" else {}))

    seed_masks = core.load_circuit_masks(seedfile)
    ctx.log("hunt worker start: engine=%s seed=%s rng=%d total=%.0fs lns=%s walk=%s"
            % (engine, os.path.basename(seedfile), rng0, total_s,
               lns_knobs, walk_knobs))
    t0 = time.time()
    chunk = 0
    while time.time() - t0 < total_s:
        remain = total_s - (time.time() - t0)
        if engine == "alt":
            eng = "walk" if chunk % 2 == 0 else "lns"
        else:
            eng = engine
        chunk_s = min(300.0 if eng == "walk" and engine == "alt" else 600.0,
                      remain)
        if chunk_s < 30:
            break
        knobs = walk_knobs if eng == "walk" else lns_knobs
        engines.run_engine(eng, seed_masks, None, 87, chunk_s,
                           [rng0 + chunk], knobs, ctx)
        if ctx.best_n is not None and ctx.best_n <= 87:
            ctx.log("TARGET REACHED -- stopping")
            break
        if drift is not None and ctx.best_n is not None:
            pick = drift_pick(os.path.join(out_dir, "%s.pop.jsonl" % label),
                              ctx.best_n)
            if pick is not None:
                seed_masks = set(pick)
                ctx.log("drift reseed: %d gates, maxJ_fam=%.3f" %
                        (len(pick), drift["bestJ"]))
            elif ctx.best_masks is not None:
                seed_masks = set(ctx.best_masks)
        elif ctx.best_masks is not None:
            seed_masks = set(ctx.best_masks)
        chunk += 1
    ctx.log("hunt worker done: best=%s@%s iters(last chunk)=%d"
            % (ctx.best_n, ctx.best_depth, ctx.iters))


if __name__ == "__main__":
    main()
