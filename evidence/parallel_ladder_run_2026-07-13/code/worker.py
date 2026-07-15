#!/usr/bin/env python3
"""
worker.py  --  one depth-stage of the parallel ladder, run FOREVER.

Launched by ladder_parallel.py as its own OS process (true parallelism). It runs
a single engine at a fixed depth cap with no time limit and no target, and it
continuously:
  * saves the best VERIFIED circuit so far to  <out_dir>/<label>_best.json
  * writes live status to                      <out_dir>/<label>_status.json
  * appends a log to                           <out_dir>/<label>.log

It never stops on its own; the coordinator reads the status file to decide when
to launch the next-deeper worker, and leaves this one running.

Usage (normally only the coordinator calls this):
  python3 worker.py <label> <engine> <depth|none> <scratch|seedfile> <out_dir> <seeds_csv>
"""
import os, sys, json, time
import mixcolumns_core as core
import engines


def atomic_write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f)
    os.replace(tmp, path)


class WorkerCtx:
    def __init__(self, label, cap, out_dir):
        self.label = label
        self.cap = cap
        self.best_path = os.path.join(out_dir, "%s_best.json" % label)
        self.status_path = os.path.join(out_dir, "%s_status.json" % label)
        self.logf = open(os.path.join(out_dir, "%s.log" % label), "a", buffering=1)
        self.t0 = time.time()
        self.best_n = 10 ** 9
        self.best_depth = None
        self.status = {"label": label, "cap": cap, "pid": os.getpid(),
                       "best_gates": None, "best_depth": None,
                       "started": self.t0, "updated": self.t0, "alive": True}
        self._flush_status()

    def _flush_status(self):
        self.status["updated"] = time.time()
        atomic_write_json(self.status_path, self.status)

    def log(self, msg):
        line = "[%7.1fs %s] %s" % (time.time() - self.t0,
                                   time.strftime("%H:%M:%S"), msg)
        print(line, flush=True)
        self.logf.write(line + "\n")
        self._flush_status()                      # heartbeat

    def improve(self, gates, masks, note=""):
        v = core.verify(gates, max_depth=self.cap)
        if not v["ok"]:
            self.log("  WARNING candidate REJECTED (outputs=%d/32 depth=%d) -- not claimed"
                     % (v["outputs"], v["depth"]))
            return False
        if v["gates"] >= self.best_n:
            return False
        self.best_n = v["gates"]; self.best_depth = v["depth"]
        core.save(gates, self.best_path,
                  extra={"depth": v["depth"], "verified": True, "cap": self.cap})
        self.status["best_gates"] = v["gates"]; self.status["best_depth"] = v["depth"]
        self._flush_status()
        self.log("  NEW BEST %d gates depth %d VERIFIED %s -> %s"
                 % (v["gates"], v["depth"], note, os.path.basename(self.best_path)))
        return True


def main():
    label = sys.argv[1]
    engine = sys.argv[2]
    depth_arg = sys.argv[3]
    start_arg = sys.argv[4]
    out_dir = sys.argv[5]
    seeds = [int(x) for x in sys.argv[6].split(",")] if len(sys.argv) > 6 and sys.argv[6] else [1]

    cap = None if depth_arg.lower() in ("none", "free", "-1") else int(depth_arg)
    if start_arg == "scratch":
        start_masks = None
    else:
        start_masks = core.load_circuit_masks(start_arg)

    ctx = WorkerCtx(label, cap, out_dir)
    ctx.log("worker start: engine=%s depth=%s start=%s seeds=%s"
            % (engine, cap, start_arg, seeds))

    # engine knob defaults (same values as hunt.py); tuned a bit hotter for a
    # long unattended run.
    knobs = {
        "lns": dict(kmax=6, kshake=12, snapback=8, nsamp=(24, 24),
                    up_prob=0.5, up_slack=4),
        "walk": dict(hub_move_p=0.35, close_hamming=4, repair_hub=40,
                     repair_one=24, plateau_slack_p=0.02),
        "anneal3": dict(anneal_iters=150000, ils_rounds=2500, sa_T0=2.0, sa_T1=0.05),
    }[engine]

    try:
        engines.run_engine(engine, start_masks, cap, None, None, seeds, knobs, ctx)
        # lns/walk return when they run out of moves; keep the process alive so
        # the coordinator's view stays stable, and re-seed to keep searching.
        while True:
            ctx.log("engine returned; restarting search from current best")
            sm = core.load_circuit_masks(ctx.best_path) if os.path.exists(ctx.best_path) else start_masks
            engines.run_engine(engine, sm, cap, None, None,
                               [s + 1000 for s in seeds], knobs, ctx)
    except KeyboardInterrupt:
        pass
    finally:
        ctx.status["alive"] = False
        ctx._flush_status()
        ctx.log("worker stopped")


if __name__ == "__main__":
    main()
