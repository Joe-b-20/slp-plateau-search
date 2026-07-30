#!/usr/bin/env python3
"""rho^2-equivariant orbit-space search runner.

Modes
  sym    exactly sigma-symmetric ladder: alternate orbit-walk (remove 1-2
         orbits + COMPLETE single-addition repair enumeration) and orbit-LNS
         (destroy k orbits, closure+trim+lift rebuild, victim repool).
  mixed  same walk but with a loose-mask budget (<= --loose unpaired masks):
         repairs may add a single loose mask (+1 instead of +2), orbits may
         be demoted to a single half (-1).
  cert   exhaustive orbit-space certificate on the symmetrized seed:
         every remove-1-orbit and every remove-2-orbits-add-(<=1) move.

Usage: orbit_search.py --seed f.json [--mode sym] [--rng 1] [--tlim 600]
                       [--loose 0] [--out prefix]
Every improvement is oracle-verified before being saved; <=88 gates also
writes ../BREAKTHROUGH_<g>gates_depth<d>.json.
"""
import argparse, itertools, os, random, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import mixcolumns_core as core
import engines_closure as EC
from orbit_engine import (sig, orep, osize, oset, TARGET_OREPS, flatten,
                          cost_of, state_from_masks, trim_lift, orbit_peel,
                          demote_pass, repair_candidates, verify_and_save)

TSET = core.TARGET_SET


def add_ok(avail2, unre, addmasks):
    """Exact: can every unrealized mask (and the additions) be derived once
    `addmasks` join the set?  Small worklist over rem only."""
    avail = set(avail2)
    rem = (set(unre) | set(addmasks)) - avail
    progress = True
    while progress and rem:
        progress = False
        for v in list(rem):
            for a in avail:
                if (v ^ a) in avail:
                    avail.add(v); rem.discard(v); progress = True
                    break
    return not rem


class Ladder:
    def __init__(self, args, log):
        self.args = args
        self.log = log
        self.rng = random.Random(args.rng)
        self.best_reps = None
        self.best_loose = set()
        self.best_cost = 10 ** 9
        self.saved = {}

    def on_best(self, reps, loose, note):
        c = cost_of(reps, loose)
        if c >= self.best_cost:
            return False
        reps, loose = orbit_peel(reps, loose, self.rng)
        c = cost_of(reps, loose)
        if c >= self.best_cost:
            return False
        path = os.path.join(self.args.outdir, "%s_best.json" % self.args.out)
        res = verify_and_save(reps, loose, path, note, self.log)
        if res is None:
            return False
        g, d = res
        self.best_reps = set(reps); self.best_loose = set(loose)
        self.best_cost = c
        assert g == c, "cost accounting mismatch %d vs %d" % (c, g)
        arch = os.path.join(self.args.outdir, "%s_%dg.json" % (self.args.out, g))
        if g not in self.saved:
            self.saved[g] = True
            verify_and_save(reps, loose, arch, note, self.log)
        if g <= 88:
            bt = os.path.join(self.args.outdir,
                              "ORBITHIT_%dgates_depth%d.json" % (g, d))
            verify_and_save(reps, loose, bt, note, self.log)
            self.log("*** BREAKTHROUGH: %d gates depth %d ***" % (g, d))
        return True


# ---------------------------------------------------------------- walk phase
def walk_phase(L, reps, loose, tlim, mixed):
    rng = L.rng; log = L.log; args = L.args
    reps = set(reps); loose = set(loose)
    F = flatten(reps, loose)
    W = EC._WalkState(F)
    cost = len(F)
    t0 = time.time(); it = acc = 0
    plateau_p = 0.85
    while time.time() - t0 < tlim:
        it += 1
        items = [(0, r) for r in reps if r not in TARGET_OREPS] + \
                [(1, m) for m in loose]
        if len(items) < 2:
            break
        # ---- occasional demote move (mixed): drop one half of an orbit, -1
        if mixed and len(loose) < args.loose and rng.random() < 0.15:
            r = rng.choice([x for k, x in items if k == 0 and osize(x) == 2]
                           or [None])
            if r is not None:
                drop = rng.choice((r, sig(r)))
                keep = sig(r) if drop == r else r
                ok, _, _ = W.remove_query({drop})
                if ok:
                    reps.discard(r); loose.add(keep)
                    F.discard(drop); W.reset(F); cost -= 1; acc += 1
                    if cost < L.best_cost:
                        L.on_best(reps, loose, "walk-demote it=%d" % it)
                    continue
        # ---- pick 1 or 2 victims
        nv = 2 if rng.random() < 0.45 else 1
        vict = rng.sample(items, min(nv, len(items)))
        D = set()
        for k, x in vict:
            D |= oset(x) if k == 0 else {x}
        ok, avail2, unre = W.remove_query(D)
        addw = None; addkind = "none"; addmasks = set()
        if not ok:
            cands = repair_candidates(unre, avail2, rng)
            rng.shuffle(cands)
            F2 = F - D
            found = None; tests = 0
            for w in cands:
                if w in F2:
                    continue
                sw = sig(w)
                if mixed and len(loose) < args.loose:
                    tests += 1
                    if add_ok(avail2, unre, {w}):
                        found = (w, "loose", {w}); break
                if sw == w:
                    tests += 1
                    if add_ok(avail2, unre, {w}):
                        found = (w, "fixed", {w}); break
                else:
                    if found is None:
                        am = {w, sw} - F2
                        tests += 1
                        if add_ok(avail2, unre, am):
                            found = (w, "orbit", am)
                            if len(D) > 2:
                                break   # already improving
                if tests >= 160:
                    break
            if found is None:
                continue
            addw, addkind, addmasks = found
        newcost = cost - len(D) + len(addmasks)
        accept = (newcost < cost) or (newcost == cost and
                                      rng.random() < plateau_p)
        if not accept:
            continue
        # ---- apply
        for k, x in vict:
            if k == 0:
                reps.discard(x)
            else:
                loose.discard(x)
        F -= D
        F |= addmasks
        if addkind == "loose":
            loose.add(addw)
        elif addkind in ("fixed", "orbit"):
            loose -= {addw, sig(addw)}      # pairing a loose half is legal
            reps.add(orep(addw))
        W.reset(F); cost = len(F); acc += 1
        if cost < L.best_cost:
            if L.on_best(reps, loose, "walk it=%d" % it):
                reps = set(L.best_reps); loose = set(L.best_loose)
                F = flatten(reps, loose); W.reset(F); cost = len(F)
        if cost > L.best_cost + 6:
            reps = set(L.best_reps); loose = set(L.best_loose)
            F = flatten(reps, loose); W.reset(F); cost = len(F)
        if it % 4000 == 0:
            log("[walk] %.0fs it=%d acc=%d cur=%d best=%d loose=%d"
                % (time.time() - t0, it, acc, cost, L.best_cost, len(loose)))
    log("[walk] done %.0fs it=%d acc=%d cur=%d best=%d"
        % (time.time() - t0, it, acc, cost, L.best_cost))
    return reps, loose


# ----------------------------------------------------------------- lns phase
def lns_phase(L, reps, tlim):
    """Symmetric-only orbit LNS: destroy k orbits, rebuild by closure+trim+
    lift from kept + pool samples + victims (repool), orbit-peel, accept."""
    rng = L.rng; log = L.log
    reps = set(reps)
    cur = set(reps)

    def build_pool(rs):
        Fl = sorted(flatten(rs))
        P = set()
        for i in range(len(Fl)):
            for j in range(i + 1, len(Fl)):
                m = Fl[i] ^ Fl[j]
                if m and core.wt(m) > 1:
                    P.add(orep(m))
        return sorted(P)

    pool = build_pool(cur)
    t0 = time.time(); it = acc = 0
    while time.time() - t0 < tlim:
        it += 1
        nont = [r for r in cur if r not in TARGET_OREPS]
        k = 1 + rng.randrange(3)
        if it % 293 == 0:
            k = 5 + rng.randrange(4)
        k = min(k, len(nont))
        vict = set(rng.sample(nont, k))
        kept = cur - vict
        cands = set(kept)
        for _ in range(3 + rng.randrange(7)):
            cands.add(pool[rng.randrange(len(pool))])
        Kl = sorted(flatten(kept))
        for _ in range(3 + rng.randrange(7)):
            m = Kl[rng.randrange(len(Kl))] ^ Kl[rng.randrange(len(Kl))]
            if m and core.wt(m) > 1:
                cands.add(orep(m))
        cands |= vict                       # victim repool
        lift = trim_lift(flatten(cands))
        if lift is None:
            continue
        c = cost_of(lift)
        if c <= cost_of(cur) + 2:
            lift, _ = orbit_peel(lift, set(), rng)
            c = cost_of(lift)
        accept = c <= cost_of(cur) or (c <= cost_of(cur) + 2 and
                                       rng.random() < 0.08)
        if accept:
            for r in lift:
                if r not in cands:
                    pool.append(r)
            cur = set(lift); acc += 1
            if c < L.best_cost:
                L.on_best(cur, set(), "lns it=%d" % it)
        if cost_of(cur) > L.best_cost + 8:
            cur = set(L.best_reps)
        if it % 2000 == 0:
            log("[lns] %.0fs it=%d acc=%d cur=%d best=%d"
                % (time.time() - t0, it, acc, cost_of(cur), L.best_cost))
    log("[lns] done %.0fs it=%d acc=%d cur=%d best=%d"
        % (time.time() - t0, it, acc, cost_of(cur), L.best_cost))
    return cur


# ------------------------------------------------------------ cert mode
def certificate(L, reps):
    """Exhaustive orbit-space remove-1 and remove-2-add-(<=1) on `reps`."""
    rng = L.rng; log = L.log
    reps = sorted(reps)
    F = flatten(reps)
    W = EC._WalkState(F)
    nont = [r for r in reps if r not in TARGET_OREPS]
    log("[cert] %d orbits (%d non-target), %d gates"
        % (len(reps), len(nont), len(F)))
    free1 = 0
    for r in nont:
        ok, _, _ = W.remove_query(oset(r))
        if ok:
            log("[cert] FREE remove-1: orbit %08x (-%d)" % (r, osize(r)))
            free1 += 1
    log("[cert] remove-1: %d free of %d" % (free1, len(nont)))
    improving = equal = 0
    pairs = list(itertools.combinations(nont, 2))
    t0 = time.time()
    for pi, (r1, r2) in enumerate(pairs):
        D = oset(r1) | oset(r2)
        gain = len(D)
        ok, avail2, unre = W.remove_query(D)
        if ok:
            log("[cert] FREE remove-2: %08x %08x (-%d)" % (r1, r2, gain))
            improving += 1
            continue
        cands = repair_candidates(unre, avail2, rng, max_u=64, max_c=100000)
        found_best = 0
        for w in cands:
            sw = sig(w)
            addn = 1 if sw == w else 2
            if gain - addn <= 0:
                if gain - addn == 0 and found_best == 0 and equal < 10**9:
                    if add_ok(avail2, unre, oset(w)):
                        equal += 1; found_best = -1
                continue
            if add_ok(avail2, unre, {w} if sw == w else {w, sw}):
                log("[cert] IMPROVING remove-2-add-1: rm %08x %08x add %08x "
                    "(net -%d)" % (r1, r2, w, gain - addn))
                improving += 1; found_best = 1
                S3 = (F - D) | oset(w)
                lift = {orep(m) for m in S3 if m not in core.INPUT_SET}
                L.on_best(lift, set(), "cert rm2add1")
                break
        if (pi + 1) % 100 == 0:
            log("[cert] %d/%d pairs, %.0fs, improving=%d equalswap=%d"
                % (pi + 1, len(pairs), time.time() - t0, improving, equal))
    log("[cert] DONE: %d pairs, improving=%d, equal-cost swaps=%d"
        % (len(pairs), improving, equal))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", required=True)
    ap.add_argument("--mode", default="sym", choices=["sym", "mixed", "cert"])
    ap.add_argument("--rng", type=int, default=1)
    ap.add_argument("--tlim", type=float, default=600)
    ap.add_argument("--loose", type=int, default=3)
    ap.add_argument("--out", default="orbit")
    ap.add_argument("--outdir", default=HERE)
    ap.add_argument("--phase", type=float, default=90,
                    help="seconds per walk/lns phase")
    args = ap.parse_args(argv)
    os.makedirs(args.outdir, exist_ok=True)

    def log(m):
        print("[%s rng%d] %s" % (args.out, args.rng, m), flush=True)

    L = Ladder(args, log)
    masks = core.load_circuit_masks(os.path.join(HERE, args.seed)
                                    if not os.path.isabs(args.seed)
                                    else args.seed)
    log("seed %s: %d masks" % (os.path.basename(args.seed), len(masks)))
    reps = state_from_masks(set(masks) | TSET)
    F = flatten(reps)
    if not EC.realizable(F):
        log("symmetrized seed NOT realizable -- aborting"); return
    reps = trim_lift(F) or reps
    reps, _ = orbit_peel(reps, set(), L.rng)
    log("symmetrized+peeled: %d orbits, %d gates" % (len(reps), cost_of(reps)))
    L.on_best(reps, set(), "start")
    reps = set(L.best_reps)

    if args.mode == "cert":
        certificate(L, reps)
        return

    loose = set()
    mixed = args.mode == "mixed"
    t0 = time.time()
    while time.time() - t0 < args.tlim:
        left = args.tlim - (time.time() - t0)
        reps, loose = walk_phase(L, reps, loose, min(args.phase, left), mixed)
        left = args.tlim - (time.time() - t0)
        if left <= 0:
            break
        if not mixed or not loose:
            reps = lns_phase(L, reps, min(args.phase * 0.5, left))
        else:
            reps, loose = walk_phase(L, reps, loose, min(args.phase, left),
                                     mixed)
        if mixed and L.rng.random() < 0.5:
            reps, loose = demote_pass(reps, loose, args.loose, L.rng)
    log("FINAL best %d gates" % L.best_cost)


if __name__ == "__main__":
    main()
