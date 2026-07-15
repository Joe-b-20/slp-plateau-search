#!/usr/bin/env python3
"""
engines.py  --  the search engines used by the record hunter.

All engines minimise the number of 2-input XOR gates for AES MixColumns, with
an optional depth cap.  They share one interface (run_engine) and talk to the
run through a small `ctx` object:

    ctx.log(msg)                 -> write a line to console + log file
    ctx.improve(gates, masks)    -> verify the candidate; if valid AND smaller
                                    than the best so far, save it and log it.
                                    Returns True if it became the new best.

An engine never "claims" a gate count; it only ever proposes candidates to
ctx.improve, which verifies against the GF(2^8) oracle before anything is saved
or reported.

Engines
    "lns"     depth-capped large-neighbourhood re-synthesis (destroy & rebuild).
              General purpose; seedable; the main hunter for depth >= 4 and for
              reducing a warm-started circuit.
    "walk"    value-set local search (remove-1 + remove-2-add-1 hub moves).
              Seedable; good for unconstrained / high-depth reduction.
    "anneal3" depth-3 partition annealer (from scratch, depth fixed at 3).
              The reliable way to reach a low count at depth 3 from nothing.
"""
import time, math, random, itertools
from collections import defaultdict, deque
import mixcolumns_core as core

T = core.TARGETS
TSET = core.TARGET_SET
INPUTS = core.INPUTS
ISET = core.INPUT_SET
bits_of = core.bits_of
wt = core.wt

INF = 1_000_000                # sentinel: mask not (yet) realizable from the set


# ==========================================================================
# Depth machinery shared by the lns/walk engines (min-depth + reconstruction)
# ==========================================================================
def relax(avail):
    """Minimum XOR build-depth of every mask in `avail` (inputs depth 0),
    computed as a fixpoint over pairs.  Returns (dep list, pos dict)."""
    na = len(avail)
    pos = {m: i for i, m in enumerate(avail)}
    dep = [0] * 32 + [INF] * (na - 32)
    changed = True
    while changed:
        changed = False
        for i in range(32, na):
            cur = dep[i]
            if cur == 1:
                continue
            S = avail[i]; best = cur
            for j in range(na):
                dA = dep[j]
                if dA + 1 >= best:
                    continue
                B = S ^ avail[j]
                if B == 0 or B == S:
                    continue
                bi = pos.get(B)
                if bi is None:
                    continue
                nd = 1 + (dA if dA > dep[bi] else dep[bi])
                if nd < best:
                    best = nd
                    if best == 1:
                        break
            if best < cur:
                dep[i] = best; changed = True
    return dep, pos


def feasible_at(mask_set, cap):
    """True iff every mask in the set is realizable AND (if cap given) builds at
    depth <= cap.  cap=None means 'no depth limit' but the set must still be
    realizable (dep < INF)."""
    avail = list(INPUTS) + list(mask_set)
    dep, _ = relax(avail)
    for i in range(32, len(avail)):
        if dep[i] >= INF:                    # not realizable from this set at all
            return False
        if cap is not None and dep[i] > cap:
            return False
    return True


def order_by_depth(mask_set, cap):
    """Emit (mask, parentA, parentB) triples in depth order so the circuit
    respects the cap.  Requires feasible_at(mask_set, cap)."""
    avail = list(INPUTS) + list(mask_set)
    dep, pos = relax(avail)
    real = [dep[i] for i in range(32, len(avail))]
    if any(d >= INF for d in real):
        raise RuntimeError("value-set not realizable")
    top = cap if cap is not None else (max(real) if real else 0)
    out = []
    for lvl in range(1, top + 1):
        for i in range(32, len(avail)):
            if dep[i] != lvl:
                continue
            S = avail[i]; done = False
            for j in range(len(avail)):
                if dep[j] >= lvl:
                    continue
                B = S ^ avail[j]
                k = pos.get(B)
                if k is None or dep[k] >= lvl:
                    continue
                out.append((S, avail[j], B)); done = True; break
            if not done:
                raise RuntimeError("cannot realize mask %08x within depth" % S)
    return out


def indexpairs_from_masks(mask_set, cap):
    """Turn a value-set into index-pair gates the verifier accepts."""
    trip = order_by_depth(mask_set, cap)
    idx = {1 << i: i for i in range(32)}
    gates = []
    for (m, a, b) in trip:
        gates.append([idx[a], idx[b]])
        idx[m] = 32 + len(gates) - 1
    return gates


# ==========================================================================
# Value-set closure/trim shared by the walk engine
# ==========================================================================
def closure(S):
    avail = set(INPUTS); order = []; parents = {}
    remaining = set(S) - avail; progress = True
    while progress and remaining:
        progress = False
        for v in list(remaining):
            for a in avail:
                if (v ^ a) in avail:
                    avail.add(v); remaining.discard(v)
                    order.append(v); parents[v] = (a, v ^ a); progress = True; break
    return avail, order, parents


def realizable(S):
    avail, _, _ = closure(S)
    return TSET <= avail


def trim_masks(S):
    """Keep only masks needed to reach the 32 targets."""
    avail, order, parents = closure(S)
    if not (TSET <= avail):
        return set(S)
    needed = set(); stack = list(TSET)
    while stack:
        v = stack.pop()
        if v in needed or v in ISET:
            continue
        needed.add(v); a, b = parents[v]; stack.append(a); stack.append(b)
    return needed


# ==========================================================================
# ENGINE  "lns"  --  depth-capped destroy & rebuild
# ==========================================================================
def _extract(avail, dep, pos, preferred, rng, cap, noise=True):
    na = len(avail)
    for t in T:
        i = pos.get(t)
        if i is None or dep[i] >= INF or (cap is not None and dep[i] > cap):
            return None
    inU = [False] * na; processed = [i < 32 for i in range(na)]
    for t in T:
        inU[pos[t]] = True
    while True:
        pick = -1; pd = -1
        for i in range(32, na):
            if inU[i] and not processed[i] and dep[i] > pd:
                pd = dep[i]; pick = i
        if pick < 0:
            break
        processed[pick] = True; S = avail[pick]; ds = dep[pick]
        bestc = 9; bi = bj = -1; nties = 0
        for j in range(na):
            if dep[j] >= ds:
                continue
            B = S ^ avail[j]; k = pos.get(B)
            if k is None or dep[k] >= ds or avail[j] > B:
                continue
            cst = 0
            if j >= 32 and not inU[j]:
                cst += 1 if preferred[j] else 2
            if k >= 32 and not inU[k]:
                cst += 1 if preferred[k] else 2
            if noise and rng.randrange(8) == 0:
                cst += rng.randrange(2)
            if cst < bestc:
                bestc = cst; bi = j; bj = k; nties = 1
            elif cst == bestc:
                nties += 1
                if rng.randrange(nties) == 0:
                    bi = j; bj = k
        if bi < 0:
            return None
        if bi >= 32:
            inU[bi] = True
        if bj >= 32:
            inU[bj] = True
    return [avail[i] for i in range(32, na) if inU[i]]


def _peel(mset, rng, cap):
    s = list(mset); improved = True
    while improved:
        improved = False; idx = list(range(len(s))); rng.shuffle(idx)
        for i in idx:
            if i >= len(s) or s[i] in TSET:
                continue
            tmp = s[:i] + s[i + 1:]
            if feasible_at(tmp, cap):
                s = tmp; improved = True; break
    return s


def engine_lns(start_masks, cap, target, time_limit, seeds, k, ctx):
    """Destroy k non-target masks, rebuild from a pool of samples + pairwise
    sums, keep if not larger; periodically peel; report every improvement."""
    rng = random.Random(seeds[0] if seeds else 1)
    if start_masks is None:
        start_masks = core.naive_masks()
    start = set(start_masks)
    if not feasible_at(start, cap):
        ctx.log("[lns] start circuit is NOT feasible at depth cap %s -- aborting stage"
                % (cap,))
        return
    # pool = current masks + all pairwise sums (weight>1)
    sol = list(start)
    S = set(sol)
    for a in sol:
        for b in sol:
            m = a ^ b
            if m and wt(m) > 1:
                S.add(m)
    pool = sorted(S)
    accumulate = set(pool)
    Ucur = _peel(list(start), rng, cap)
    Ubest = list(Ucur)
    ctx.improve(indexpairs_from_masks(Ubest, cap), set(Ubest))
    t0 = time.time(); iters = 0
    while (time_limit is None or time.time() - t0 < time_limit) and \
          (target is None or len(Ubest) > target):
        iters += 1
        nu = len(Ucur)
        kk = 1 + rng.randrange(k["kmax"])
        if iters % 997 == 0:
            kk = k["kshake"] + rng.randrange(5)
        nontarget = [i for i in range(nu) if Ucur[i] not in TSET]
        if len(nontarget) < kk:
            kk = max(1, len(nontarget))
        rng.shuffle(nontarget); vict = set(nontarget[:kk])
        kept = [Ucur[i] for i in range(nu) if i not in vict]; nkeep = len(kept)
        if nkeep == 0:
            continue
        cand = list(kept)
        for _ in range(k["nsamp"][0] + rng.randrange(k["nsamp"][1])):
            cand.append(pool[rng.randrange(len(pool))])
        for _ in range(k["nsamp"][0] + rng.randrange(k["nsamp"][1])):
            m = kept[rng.randrange(nkeep)] ^ kept[rng.randrange(nkeep)]
            if m:
                cand.append(m)
        seen = set(); C2 = []
        for m in cand:
            if m not in seen and wt(m) > 1:
                seen.add(m); C2.append(m)
        avail = list(INPUTS) + C2
        dep, pos = relax(avail)
        preferred = [False] * len(avail); keptset = set(kept)
        for i in range(32, len(avail)):
            if avail[i] in keptset:
                preferred[i] = True
        res = _extract(avail, dep, pos, preferred, rng, cap)
        if res is None:
            continue
        r = len(res)
        accept = (r <= nu) or (r <= nu + k["up_slack"] and rng.random() < k["up_prob"])
        if accept:
            for m in res:
                if m not in accumulate:
                    accumulate.add(m); pool.append(m)
            Ucur = res
            if len(Ucur) < len(Ubest):
                Ucur = _peel(Ucur, rng, cap); Ubest = list(Ucur)
                ctx.improve(indexpairs_from_masks(Ubest, cap), set(Ubest),
                            note="it=%d" % iters)
        if len(Ucur) > len(Ubest) + k["snapback"]:
            Ucur = list(Ubest)
        if iters % 20000 == 0:
            ctx.log("[lns] %.0fs iters=%d cur=%d best=%d" %
                    (time.time() - t0, iters, len(Ucur), len(Ubest)))


# ==========================================================================
# ENGINE  "walk"  --  value-set remove-1 / remove-2-add-1 hub moves
# ==========================================================================
def _repair(S2, rng, tries):
    avail, _, _ = closure(S2)
    if TSET <= avail:
        return S2
    wanted = list((set(S2) | TSET) - avail); avail_list = list(avail)
    for _ in range(tries):
        c = rng.choice(wanted); a = rng.choice(avail_list); w = c ^ a
        if w == 0 or w in avail or w in ISET:
            continue
        if not any((w ^ p) in avail for p in avail_list):
            continue
        S3 = set(S2) | {w}
        av3, _, _ = closure(S3)
        if TSET <= av3:
            return S3
    return None


def engine_walk(start_masks, cap, target, time_limit, seeds, k, ctx):
    """Remove a mask (or two) and repair; keep any reduction that still builds
    all targets and (if a cap is set) stays within depth."""
    rng = random.Random(seeds[0] if seeds else 1)
    if start_masks is None:
        start_masks = core.naive_masks()
    if cap is not None and not feasible_at(start_masks, cap):
        ctx.log("[walk] start not feasible at depth cap %s -- aborting stage" % cap)
        return

    def ok_cap(mset):
        return cap is None or feasible_at(mset, cap)

    cur = trim_masks(start_masks)
    if not ok_cap(cur):
        ctx.log("[walk] trimmed start exceeds depth cap -- aborting"); return
    best = set(cur)
    ctx.improve(indexpairs_from_masks(best, cap), set(best))
    t0 = time.time(); iters = 0
    while (time_limit is None or time.time() - t0 < time_limit) and \
          (target is None or len(best) > target):
        iters += 1
        nont = [v for v in cur if v not in TSET]
        if len(nont) < 2:
            break
        if rng.random() < k["hub_move_p"]:                 # remove-2-add-1
            v1 = rng.choice(nont)
            if rng.random() < 0.5:
                cand = [u for u in nont if u != v1 and wt(u ^ v1) <= k["close_hamming"]]
                v2 = rng.choice(cand) if cand else rng.choice([u for u in nont if u != v1])
            else:
                v2 = rng.choice([u for u in nont if u != v1])
            S2 = cur - {v1, v2}
            if TSET <= closure(S2)[0]:
                nxt = trim_masks(S2)
                if ok_cap(nxt):
                    cur = nxt
            else:
                fixed = _repair(S2, rng, k["repair_hub"])
                if fixed is not None:
                    nxt = trim_masks(fixed)
                    if len(nxt) < len(cur) and ok_cap(nxt):
                        cur = nxt
        else:                                              # remove-1
            v = rng.choice(nont); S2 = cur - {v}
            if TSET <= closure(S2)[0]:
                nxt = trim_masks(S2)
                if ok_cap(nxt):
                    cur = nxt
            else:
                fixed = _repair(S2, rng, k["repair_one"])
                if fixed is not None:
                    nxt = trim_masks(fixed)
                    slack = 1 if (rng.random() < k["plateau_slack_p"]
                                  and len(cur) < len(best) + 2) else 0
                    if len(nxt) <= len(cur) + slack and ok_cap(nxt):
                        cur = nxt
        if len(cur) < len(best):
            best = set(cur)
            ctx.improve(indexpairs_from_masks(best, cap), set(best), note="it=%d" % iters)
        if iters % 20000 == 0:
            ctx.log("[walk] %.0fs iters=%d cur=%d best=%d" %
                    (time.time() - t0, iters, len(cur), len(best)))


# ==========================================================================
# ENGINE  "anneal3"  --  depth-3 partition annealer (from scratch)
# ==========================================================================
def engine_anneal3(start_masks, cap, target, time_limit, seeds, k, ctx):
    if cap not in (3, None):
        ctx.log("[anneal3] note: this engine only produces depth-3 circuits "
                "(ignoring cap=%s)" % cap)
    from itertools import combinations

    def gen_splits(t):
        bs = bits_of(t); S = set()
        if len(bs) == 7:
            for c in combinations(bs, 4):
                A = sum(1 << b for b in c); S.add((A, t ^ A))
        else:
            for c in combinations(bs, 4):
                A = sum(1 << b for b in c); S.add((A, t ^ A))
            for c in combinations(bs, 3):
                A = sum(1 << b for b in c); S.add((A, t ^ A))
            ext = [e for e in range(32) if not (t >> e) & 1]
            for c in combinations(bs, 3):
                base = sum(1 << b for b in c)
                for e in ext:
                    A = base | (1 << e); S.add((A, t ^ A))
        return sorted(S)

    SPLITS = [gen_splits(t) for t in T]
    PAIRINGS = {}

    def get_pairings(m):
        pr = PAIRINGS.get(m)
        if pr is None:
            bs = bits_of(m)
            if len(bs) == 3:
                pr = []
                for i in range(3):
                    r = [bs[j] for j in range(3) if j != i]
                    pr.append(((1 << r[0]) | (1 << r[1]),))
            else:
                a, b, c, d = bs
                pr = [((1 << a) | (1 << b), (1 << c) | (1 << d)),
                      ((1 << a) | (1 << c), (1 << b) | (1 << d)),
                      ((1 << a) | (1 << d), (1 << b) | (1 << c))]
            PAIRINGS[m] = pr
        return pr

    class State:
        __slots__ = ('rng', 'choice', 'big', 'pairs', 'pairing', 'cost')
        def __init__(s, seed):
            s.rng = random.Random(seed); s.choice = [None] * 32
            s.big = {}; s.pairs = {}; s.pairing = {}; s.cost = 32
            for o in range(32):
                s.set_choice(o, s.rng.randrange(len(SPLITS[o])))
        def pair_add(s, p):
            c = s.pairs.get(p, 0); s.pairs[p] = c + 1
            if c == 0: s.cost += 1
        def pair_del(s, p):
            c = s.pairs[p]
            if c == 1: del s.pairs[p]; s.cost -= 1
            else: s.pairs[p] = c - 1
        def _best_pairing(s, m):
            best = None; bestnew = 99; opts = get_pairings(m); n = len(opts)
            start = s.rng.randrange(n)
            for kk in range(n):
                pr = opts[(start + kk) % n]
                new = sum(1 for p in pr if s.pairs.get(p, 0) == 0)
                if new < bestnew: bestnew = new; best = pr
            return best
        def part_add(s, m):
            w = wt(m)
            if w == 1: return
            if w == 2: s.pair_add(m); return
            c = s.big.get(m, 0); s.big[m] = c + 1
            if c == 0:
                s.cost += 1; best = s._best_pairing(m); s.pairing[m] = best
                for p in best: s.pair_add(p)
        def part_del(s, m):
            w = wt(m)
            if w == 1: return
            if w == 2: s.pair_del(m); return
            c = s.big[m]
            if c == 1:
                del s.big[m]; s.cost -= 1
                for p in s.pairing[m]: s.pair_del(p)
                del s.pairing[m]
            else: s.big[m] = c - 1
        def set_choice(s, o, idx):
            old = s.choice[o]
            if old is not None:
                A, B = SPLITS[o][old]; s.part_del(A); s.part_del(B)
            s.choice[o] = idx
            if idx is not None:
                A, B = SPLITS[o][idx]; s.part_add(A); s.part_add(B)
        def repair(s, m):
            if m not in s.big: return
            for p in s.pairing[m]: s.pair_del(p)
            best = s._best_pairing(m); s.pairing[m] = best
            for p in best: s.pair_add(p)
        def delta_add(s, m):
            w = wt(m)
            if w == 1: return 0
            if w == 2: return 0 if s.pairs.get(m, 0) > 0 else 1
            if s.big.get(m, 0) > 0: return 0
            best = 3
            for pr in get_pairings(m):
                n = sum(1 for p in pr if s.pairs.get(p, 0) == 0)
                if n < best: best = n
            return 1 + best
        def greedy_rechoice(s, o):
            old = s.choice[o]; A, B = SPLITS[o][old]
            s.choice[o] = None; s.part_del(A); s.part_del(B)
            best = []; bestd = 999
            for idx, (A2, B2) in enumerate(SPLITS[o]):
                d = s.delta_add(A2) + s.delta_add(B2)
                if d < bestd: bestd = d; best = [idx]
                elif d == bestd: best.append(idx)
            idx = s.rng.choice(best); s.choice[o] = idx
            A2, B2 = SPLITS[o][idx]; s.part_add(A2); s.part_add(B2)
        def snapshot(s):
            return (list(s.choice), dict(s.pairing), s.cost)
        def _forced(s, m, pg):
            w = wt(m)
            if w == 1: return
            if w == 2: s.pair_add(m); return
            c = s.big.get(m, 0); s.big[m] = c + 1
            if c == 0:
                s.cost += 1; best = pg.get(m) or get_pairings(m)[0]; s.pairing[m] = best
                for p in best: s.pair_add(p)
        def restore(s, snap):
            ch, pg, _ = snap
            for o in range(32): s.set_choice(o, None)
            s.pairing = {}
            for o in range(32):
                idx = ch[o]; s.choice[o] = idx
                A, B = SPLITS[o][idx]; s._forced(A, pg); s._forced(B, pg)

    def descend(s):
        improved = True
        while improved:
            improved = False; order = list(range(32)); s.rng.shuffle(order)
            for o in order:
                c0 = s.cost; s.greedy_rechoice(o)
                if s.cost < c0: improved = True
            for m in list(s.big.keys()):
                if m in s.big:
                    c0 = s.cost; s.repair(m)
                    if s.cost < c0: improved = True

    def anneal(s, iters, T0, T1):
        rng = s.rng; best = s.snapshot()
        for it in range(iters):
            temp = T0 * (T1 / T0) ** (it / iters); r = rng.random()
            if r < 0.60:
                o = rng.randrange(32); old = s.choice[o]; c0 = s.cost
                idx = rng.randrange(len(SPLITS[o]))
                if idx == old: continue
                s.set_choice(o, idx); d = s.cost - c0
                if d > 0 and rng.random() > math.exp(-d / temp):
                    s.set_choice(o, old)
            elif r < 0.85:
                if s.big: s.repair(rng.choice(list(s.big.keys())))
            else:
                s.greedy_rechoice(rng.randrange(32))
            if s.cost < best[2]: best = s.snapshot()
        return best

    def kick(s, kk):
        for _ in range(kk):
            o = s.rng.randrange(32); s.set_choice(o, s.rng.randrange(len(SPLITS[o])))

    def emit(snap):
        choices, pairing, _ = snap
        pairing = {int(x): tuple(v) for x, v in pairing.items()}
        bigs = {}; pairs = set(); finals = []
        for o in range(32):
            A, B = SPLITS[o][choices[o]]; finals.append((T[o], A, B))
            for m in (A, B):
                w = wt(m)
                if w == 2: pairs.add(m)
                elif w >= 3 and m not in bigs:
                    bigs[m] = pairing.get(m) or get_pairings(m)[0]
        for m, pg in bigs.items():
            for p in pg: pairs.add(p)
        si = {(1 << b): b for b in range(32)}; gates = []
        def add(mask, am, bm):
            gates.append([si[am], si[bm]]); si[mask] = 32 + len(gates) - 1
        for p in sorted(pairs):
            i, j = bits_of(p); add(p, 1 << i, 1 << j)
        for m in sorted(bigs):
            pg = bigs[m]
            if wt(m) == 3:
                p = pg[0]; add(m, p, m ^ p)
            else:
                p1, p2 = pg; add(m, p1, p2)
        for t, A, B in finals:
            add(t, A, B)
        return gates

    def seed_stream():
        yielded = set()
        for sd in (seeds or [6]):
            yielded.add(sd); yield sd
        for sd in itertools.count(1):
            if sd not in yielded:
                yield sd

    t0 = time.time(); gbest = None
    for sd in seed_stream():
        if time_limit is not None and time.time() - t0 >= time_limit:
            break
        if target is not None and gbest is not None and gbest[2] <= target:
            break
        s = State(sd * 100003 + 17)
        b = anneal(s, k["anneal_iters"], k["sa_T0"], k["sa_T1"])
        s.restore(b); descend(s); cur = s.snapshot()
        deadline = INF if time_limit is None else t0 + time_limit
        for r in range(k["ils_rounds"]):
            if (r & 63) == 0 and time.time() > deadline: break
            if target is not None and cur[2] <= target: break
            s.restore(cur); kick(s, s.rng.randrange(2, 7)); descend(s)
            if s.cost <= cur[2]: cur = s.snapshot()
        if gbest is None or cur[2] < gbest[2]:
            gbest = cur
            gates = emit(gbest)
            sig = [1 << i for i in range(32)]
            for a, bb in gates: sig.append(sig[a] ^ sig[bb])
            ctx.improve(gates, set(sig[32:]), note="seed=%d" % sd)


ENGINES = {
    "lns": engine_lns,
    "walk": engine_walk,
    "anneal3": engine_anneal3,
}


def run_engine(name, start_masks, cap, target, time_limit, seeds, knobs, ctx):
    if name not in ENGINES:
        raise SystemExit("unknown engine %r (choose from %s)" % (name, list(ENGINES)))
    ENGINES[name](start_masks, cap, target, time_limit, seeds, knobs, ctx)
