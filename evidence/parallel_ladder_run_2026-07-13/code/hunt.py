#!/usr/bin/env python3
"""
hunt.py  --  record-hunting pipeline for AES-MixColumns XOR circuits.

    python3 hunt.py

Runs the experiments defined in the CONFIG block below.  An experiment is a
list of STAGES run in order; each stage searches for the smallest circuit it
can at a chosen depth cap, starting from scratch, from a file, or from the
previous stage's best.  Everything is logged to the console AND to a log file,
every improvement is verified against the GF(2^8) oracle before it is claimed,
and the best circuit of each stage is saved to disk as it shrinks so you can
watch and inspect it live.

Nothing here ever reports a gate count it has not verified.
"""
import os, sys, json, time, traceback
import mixcolumns_core as core
import engines

# ==========================================================================
# CONFIG  --  edit everything here
# ==========================================================================

OUT_ROOT = "runs"        # experiments are written to runs/<name>_<timestamp>/

# ---- Default search knobs per engine -------------------------------------
# A stage uses its engine's knobs here, unless the stage supplies its own
# "knobs" dict (which is merged over these).  Every knob is explained inline.

LNS_KNOBS = dict(
    kmax     = 6,        # DESTROY SIZE.  Each step rips out 1..kmax non-output
                         #   masks and rebuilds.  Bigger = bolder moves (escapes
                         #   ruts, but each step is slower and noisier).
    kshake   = 12,       # Every ~1000 steps do a BIG destroy of this many masks
                         #   to jump to a far part of the space.  Bigger = wilder
                         #   occasional shake-ups.
    snapback = 8,        # If the working circuit drifts more than this many gates
                         #   above the best, snap back to the best.  Bigger =
                         #   wander further before giving up (more exploration).
    nsamp    = (24, 24), # How many candidate masks to throw into each rebuild:
                         #   (base, extra-random).  Bigger = richer rebuilds,
                         #   more likely to find a cut, but slower per step.
    up_prob  = 0.5,      # Chance of accepting a rebuild that is up to up_slack
                         #   gates WORSE (uphill).  Higher = explores more,
                         #   converges slower.
    up_slack = 4,        # How many gates worse an accepted uphill move may be.
)

WALK_KNOBS = dict(
    hub_move_p      = 0.35,  # Chance of a remove-2-add-1 "hub" move (the move
                             #   that actually cuts a gate) vs a plain remove-1.
    close_hamming   = 4,     # Bias hub pairs whose masks differ in <= this many
                             #   bits (structurally close -> likelier to merge).
    repair_hub      = 40,    # Repair attempts after a hub move before giving up.
    repair_one      = 24,    # Repair attempts after a remove-1 move.
    plateau_slack_p = 0.02,  # Chance of accepting a +1 sideways step to escape
                             #   a local rut.  Higher = wanders more.
)

ANNEAL_KNOBS = dict(
    anneal_iters = 150_000,  # Simulated-annealing moves per restart.  More =
                             #   deeper cooling per restart (slower, better).
    ils_rounds   = 2_500,    # Iterated-local-search kicks per restart.
    sa_T0        = 2.0,      # Start "temperature": higher = accepts more bad
                             #   moves early (explores wildly at first).
    sa_T1        = 0.05,     # End temperature: how greedy it becomes at the end.
)

# ---- The experiments to run ----------------------------------------------
# Each stage field:
#   name        label used for files and log lines
#   engine      "anneal3" (depth-3 from scratch) | "lns" | "walk"
#   start       "scratch" | "prev" (previous stage's best) | a path to a .json
#   depth       an int depth cap, or None for UNCONSTRAINED depth
#   target      stop when a verified circuit this small is found, or None to
#               keep going until time_limit_s (or forever if that is None too)
#   time_limit_s seconds for this stage, or None to run until target / Ctrl-C
#   seeds       list of RNG seeds to try (more seeds = more independent restarts)
#   knobs       optional per-stage overrides of the engine's knobs
#
# THEORY of the default experiment (the "depth ladder"): find the tightest
# circuit at depth 3, then relax the cap one notch and WARM-START from that
# circuit.  Relaxing the cap can only keep or lower the gate count, and starting
# from the tightest lower-depth circuit may guide the looser search into a
# better basin than searching the looser depth cold.  We climb 3 -> 4 -> 5 ->
# 6 -> unconstrained and watch the count fall.

DEPTH_LADDER = dict(
    name="depth_ladder",
    stages=[
        dict(name="d3_scratch", engine="anneal3", start="scratch",
             depth=3,    target=None, time_limit_s=300, seeds=[6, 1, 2, 3]),
        dict(name="d4_from_d3", engine="lns",     start="prev",
             depth=4,    target=None, time_limit_s=300, seeds=[1]),
        dict(name="d5_from_d4", engine="lns",     start="prev",
             depth=5,    target=None, time_limit_s=300, seeds=[1]),
        dict(name="d6_from_d5", engine="lns",     start="prev",
             depth=6,    target=None, time_limit_s=300, seeds=[1]),
        dict(name="dfree_from_d6", engine="lns",  start="prev",
             depth=None, target=None, time_limit_s=300, seeds=[1]),
    ],
)

# The list of experiments main() will run, in order.  Add your own dicts here.
EXPERIMENTS = [DEPTH_LADDER]

# ==========================================================================
# END CONFIG  --  machinery below
# ==========================================================================

KNOBS_FOR = {"lns": LNS_KNOBS, "walk": WALK_KNOBS, "anneal3": ANNEAL_KNOBS}


class Logger:
    """Tee log lines to the console and a file, with elapsed + wall time."""
    def __init__(self, path):
        self.f = open(path, "a", buffering=1)
        self.t0 = time.time()
    def __call__(self, msg):
        line = "[%7.1fs %s] %s" % (time.time() - self.t0,
                                   time.strftime("%H:%M:%S"), msg)
        print(line, flush=True)
        self.f.write(line + "\n")
    def close(self):
        self.f.close()


class Ctx:
    """Passed to an engine.  Holds the depth cap, does verify-before-claim, and
    saves + logs every genuine improvement."""
    def __init__(self, log, cap, best_path, stage_result):
        self.log = log
        self.cap = cap
        self.best_path = best_path
        self.result = stage_result
        self.best_n = 10 ** 9
        self.best_gates = None
        self.best_masks = None

    def improve(self, gates, masks, note=""):
        v = core.verify(gates, max_depth=self.cap)
        if not v["ok"]:
            self.log("  WARNING candidate REJECTED (outputs=%d/32, depth=%d, %s) -- not claimed"
                     % (v["outputs"], v["depth"], (v["problems"][:1] or ["depth>cap"])[0]))
            return False
        if v["gates"] >= self.best_n:
            return False
        self.best_n = v["gates"]; self.best_gates = gates; self.best_masks = masks
        core.save(gates, self.best_path,
                  extra={"depth": v["depth"], "verified": True, "cap": self.cap})
        self.result["gates"] = v["gates"]; self.result["depth"] = v["depth"]
        self.result["verified"] = True
        self.log("  NEW BEST %d gates, depth %d, VERIFIED  %s  -> %s"
                 % (v["gates"], v["depth"], note, os.path.basename(self.best_path)))
        return True


def resolve_start(start, prev_masks, log):
    if start == "scratch":
        log("  start: from scratch (balanced-tree naive circuit)")
        return None
    if start == "prev":
        if prev_masks is None:
            log("  start: 'prev' requested but no previous stage -- using scratch")
            return None
        log("  start: warm from previous stage (%d masks)" % len(prev_masks))
        return set(prev_masks)
    masks = core.load_circuit_masks(start)
    log("  start: seed file %s (%d masks)" % (start, len(masks)))
    return set(masks)


def run_stage(stage, prev_masks, exp_dir, log):
    name = stage["name"]; engine = stage["engine"]
    cap = stage.get("depth"); target = stage.get("target")
    tlimit = stage.get("time_limit_s"); seeds = stage.get("seeds", [1])
    knobs = dict(KNOBS_FOR[engine]); knobs.update(stage.get("knobs", {}))

    log("")
    log("=== STAGE %s | engine=%s depth=%s target=%s time=%s seeds=%s ==="
        % (name, engine, cap, target, tlimit, seeds))
    start_masks = resolve_start(stage.get("start", "scratch"), prev_masks, log)

    best_path = os.path.join(exp_dir, "%s_best.json" % name)
    result = {"stage": name, "engine": engine, "depth_cap": cap,
              "gates": None, "depth": None, "verified": False}
    ctx = Ctx(log, cap, best_path, result)
    t0 = time.time()
    try:
        engines.run_engine(engine, start_masks, cap, target, tlimit, seeds, knobs, ctx)
    except KeyboardInterrupt:
        log("  interrupted -- keeping best so far")
    except Exception:
        log("  ERROR in engine:\n" + traceback.format_exc())
    result["time_s"] = round(time.time() - t0, 1)
    if ctx.best_gates is None:
        log("  stage produced no verified circuit")
        return prev_masks, result
    log("  stage %s done: best %d gates, depth %d (%.1fs)"
        % (name, result["gates"], result["depth"], result["time_s"]))
    return ctx.best_masks, result


def run_experiment(exp, log_root):
    stamp = time.strftime("%Y%m%d_%H%M%S")
    exp_dir = os.path.join(log_root, "%s_%s" % (exp["name"], stamp))
    os.makedirs(exp_dir, exist_ok=True)
    log = Logger(os.path.join(exp_dir, "run.log"))
    log("EXPERIMENT %s -> %s" % (exp["name"], exp_dir))

    manifest = {"experiment": exp["name"], "started": stamp,
                "dir": exp_dir, "stages": []}
    prev = None
    for stage in exp["stages"]:
        prev, result = run_stage(stage, prev, exp_dir, log)
        manifest["stages"].append(result)
        with open(os.path.join(exp_dir, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=2)

    log("")
    log("==================== SUMMARY: %s ====================" % exp["name"])
    log("%-16s %-8s %6s %6s %10s" % ("stage", "engine", "gates", "depth", "time"))
    for r in manifest["stages"]:
        log("%-16s %-8s %6s %6s %9ss"
            % (r["stage"], r["engine"], r["gates"], r["depth"], r.get("time_s")))
    log("manifest + per-stage circuits in: %s" % exp_dir)
    log.close()
    return manifest


def main():
    os.makedirs(OUT_ROOT, exist_ok=True)
    for exp in EXPERIMENTS:
        run_experiment(exp, OUT_ROOT)


if __name__ == "__main__":
    main()
