#!/usr/bin/env python3
"""seed89.py -- a PATCHED COPY of experiments/e_upstream/deep.py (originals untouched).

THE TWO-LINE CHANGE, and the whole point of this run
====================================================
Every one of e_upstream's 225 pinned descents started at a 100-173-gate root and
spent its entire budget on the 149 -> 89 stretch.  The 89 -> 88 gap has never
received a single dedicated second.  This job seeds the descent AT the banked
89 (`experiments/e_upstream/S89_41_00000098.json`, oracle-VALID, 89 gates,
depth 10) with the same pin 0x00000098 (|odd|=3) and the same target 88, so the
whole budget goes into the one gate that matters.

QUESTION IT ASKS (for the record, verbatim in the ledger):
  Does an out-of-vocabulary 88 exist one step below the 89?
This is a STRUCTURAL question about the RECORD level -- 88 is the record, not a
sub-record.  It is not an 87 hunt: the target is 88 and the engine stops there.
A hit would be the first 88-gate MixColumns circuit containing a mask outside
the 1,778-word corpus vocabulary; repeated failure is the sharpest available
evidence that the 88 plateau really is confined to its dictionary.

Everything else -- the pin mechanism (patch BOTH engines.T and engines.TSET,
since _extract iterates the list), the LNS/walk alternation, the knobs -- is
deep.py unchanged.

Banks to disk as it lands: every improvement appends to seed89_ledger.jsonl;
any state at <= 88 masks is written out immediately (masks + oracle-format gate
list) BEFORE the loop continues, so a kill at any moment loses nothing.
Interruptible at any time: kill the PID; the ledger and any hit are already on
disk.  Honours an absolute monotonic deadline and an optional STOP file.
"""
import sys, os, json, time, random

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'pipeline')); sys.path.insert(0, REPO)
import engines, ladder_parallel as LP
from verify_circuit import mixcolumns_target_masks

TARGETS = set(mixcolumns_target_masks())
BASE_T = frozenset(engines.TSET)
BASE_L = list(engines.T)
LANE = [sum(1 << (8 * b + j) for b in range(4)) for j in range(8)]
def nodd(m): return sum(1 for j in range(8) if bin(m & LANE[j]).count("1") & 1)
def nlane(m): return sum(1 for j in range(8) if m & LANE[j])

WALK = dict(LP.WALK_KNOBS); WALK["harvest_path"] = None
LNS = dict(LP.LNS_KNOBS); LNS["harvest"] = False; LNS["harvest_path"] = None

SEED = os.path.join(REPO, 'experiments/e_upstream/S89_41_00000098.json')
LOG = os.path.join(HERE, 'seed89.log')
LEDGER = os.path.join(HERE, 'seed89_ledger.jsonl')
STOP = os.path.join(HERE, 'STOP_seed89')

fh = open(LOG, "a", buffering=1)
lg = open(LEDGER, "a", buffering=1)
def log(m):
    fh.write("%s %s\n" % (time.strftime("%H:%M:%S"), m))
def led(**kw):
    kw["t"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    lg.write(json.dumps(kw) + "\n")


def build_order(masks):
    """Greedy topological build -> oracle-format index pairs, or None."""
    idx = {1 << i: i for i in range(32)}
    rem = [m for m in masks if m not in idx]
    pairs = []
    prog = True
    while rem and prog:
        prog = False
        nxt = []
        for m in rem:
            got = None
            for a in idx:
                b = m ^ a
                if b in idx and b != m:
                    got = (idx[a], idx[b]); break
            if got:
                pairs.append([got[0], got[1]]); idx[m] = 32 + len(pairs) - 1; prog = True
            else:
                nxt.append(m)
        rem = nxt
    return None if rem else pairs


class Ctx:
    def __init__(s, v):
        s.best = None; s.bestn = 10 ** 9; s.v = v; s.nhit = 0
    def log(s, m):
        pass
    def improve(s, circ, masks, note=""):
        if len(masks) >= s.bestn:
            return
        s.bestn = len(masks); s.best = set(masks)
        alive = s.v in s.best
        log("    %d  (v alive: %s)" % (len(masks), alive))
        led(ev="improve", n=len(masks), v_alive=alive)
        if len(masks) <= 88:
            s.nhit += 1
            ok_t = TARGETS <= s.best
            pairs = build_order(sorted(s.best))
            base = "HIT%d_%08x_%d" % (len(masks), s.v, s.nhit)
            json.dump({"pinned": s.v, "nodd": nodd(s.v), "gates_reached": len(masks),
                       "v_alive": alive, "all_targets": ok_t,
                       "seed": "experiments/e_upstream/S89_41_00000098.json",
                       "masks": sorted(s.best)},
                      open(os.path.join(HERE, base + ".json"), "w"))
            if pairs is not None:
                json.dump({"gates": pairs}, open(os.path.join(HERE, base + "_circuit.json"), "w"))
            log("*** HIT %d MASKS  v_alive=%s all_targets=%s realizable=%s -> %s ***"
                % (len(masks), alive, ok_t, pairs is not None, base))
            led(ev="HIT", n=len(masks), v_alive=alive, all_targets=ok_t,
                realizable=pairs is not None, file=base + ".json")


def main():
    secs = float(sys.argv[1]) if len(sys.argv) > 1 else 10000.0
    v = 152                                     # 0x00000098, |odd| = 3
    d = json.load(open(SEED))
    M = set(d["masks"])
    assert len(M) == 89 and v in M and TARGETS <= M, "seed is not the banked 89"
    rng = random.Random(89152)

    engines.TSET = frozenset(BASE_T | {v}); engines.T = BASE_L + [v]
    ok = engines.realizable(M)
    log("=" * 78)
    log("seed89: seed=%s |M|=%d pin=0x%08x nodd=%d nlane=%d realizable=%s target=88 budget=%.0fs"
        % (os.path.basename(SEED), len(M), v, nodd(v), nlane(v), ok, secs))
    log("question: does an out-of-vocabulary 88 exist one step below the 89?"
        " (structural question about the RECORD level; not a sub-record search)")
    led(ev="start", seed=os.path.basename(SEED), n_seed=len(M), pin="0x%08x" % v,
        nodd=nodd(v), realizable=ok, target=88, budget_s=secs, pid=os.getpid(),
        purpose="Does an out-of-vocabulary 88 exist one step below the 89? "
                "Structural question about the record level (88 IS the record); "
                "not a sub-record / 87 search -- the engine target is 88 and it stops there.")
    if not ok:
        log("UNREALIZABLE seed -- abort"); led(ev="abort", why="unrealizable"); return

    ctx = Ctx(v)
    ctx.bestn = len(M); ctx.best = set(M)
    t0 = time.monotonic()
    deadline = t0 + secs
    rounds = 0
    try:
        while time.monotonic() < deadline:
            if os.path.exists(STOP):
                log("STOP file present -- stopping"); led(ev="stop", why="STOP file"); break
            rounds += 1
            left = deadline - time.monotonic()
            cur = ctx.best
            engines.run_engine("lns", cur, None, 88, min(120, max(5, left)),
                               [rng.randrange(10 ** 6)], LNS, ctx)
            if time.monotonic() >= deadline or ctx.bestn <= 88:
                break
            cur = ctx.best
            engines.run_engine("walk", cur, None, 88, min(60, max(5, deadline - time.monotonic())),
                               [rng.randrange(10 ** 6)], WALK, ctx)
            if ctx.bestn <= 88:
                break
            if rounds % 10 == 0:
                log("  ... round %d, %.0fs left, best=%d" % (rounds, deadline - time.monotonic(), ctx.bestn))
                led(ev="progress", rounds=rounds, best=ctx.bestn,
                    elapsed_s=round(time.monotonic() - t0))
    except Exception as e:
        log("ERR %s" % e); led(ev="err", msg=str(e))
    finally:
        engines.TSET = BASE_T; engines.T = BASE_L

    alive = ctx.best is not None and v in ctx.best
    log("FLOOR %d  v_alive=%s  rounds=%d  wall=%.0fs  hits=%d"
        % (ctx.bestn, alive, rounds, time.monotonic() - t0, ctx.nhit))
    led(ev="done", floor=ctx.bestn, v_alive=alive, rounds=rounds,
        wall_s=round(time.monotonic() - t0), hits=ctx.nhit,
        verdict=("REACHED 88" if ctx.bestn <= 88 else
                 "no 88 reached from the 89 in this budget (upper bound; search, not proof)"))


main()
