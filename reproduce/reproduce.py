#!/usr/bin/env python3
"""
reproduce.py  --  single-command, single-core, stdlib-only reproduction of the
from-scratch depth-3 record for AES MixColumns (97 gates at depth 3), plus
optional legacy demonstrations of the search moves.

    python3 reproduce.py

Edit the CONFIG block just below to choose which methods run and to tune every
search parameter.  The math and the verifier live in mixcolumns_core.py; the
seed circuits live in seeds.py.  Each method writes out_<method>.json and is
checked by the independent GF(2^8) verifier before it is reported.

The methods, and what each really is:

  "97"  CURRENT RECORD, depth-3, FROM SCRATCH.  Simulated-annealing +
        iterated-local-search over a "shared depth-1 pairs / depth-2 parts"
        model.  Reaches 97 gates at depth 3 -- the current record count at the
        minimum possible depth -- from nothing, in minutes.
        (The other current records need the multi-worker pipeline:
         92@depth4 via ../pipeline MODE="cascade"; 89@depth5 via
         ../pipeline MODE="fixed".  See ../pipeline/README.md.)

  "91"  LEGACY demo.  Value-set reduction of the PUBLISHED 92-gate circuit of
        Xiang-Zeng-Lin-Bao-Zhang: walk the plateau of equal-size circuits
        until one gate becomes removable -> 91 @ depth 6.
  "89"  LEGACY demo.  The value-set walk (remove-1 + remove-2-add-1 hub moves)
        reducing a 90-gate seed to 89 at unconstrained depth.  From nothing
        this method floors near 92; the 89 needs the 90-gate seed.
  "90"  LEGACY demo.  Proves a 91-gate seed admits no single local cut, and
        optionally runs the pure-Python LNS (reaches ~91, not the elite 90).
"""

# ==========================================================================
# CONFIG  --  edit everything here
# ==========================================================================

# Which methods to run.  Default: just "97" -- the from-scratch reproduction
# of the CURRENT depth-3 record (97 gates at depth 3, ~1-3 min single core).
#
# The other two current records need the multi-worker pipeline, not this file:
#   92 @ depth 4  ->  ../pipeline/ MODE="cascade"   (hours, from scratch)
#   89 @ depth 5  ->  ../pipeline/ MODE="fixed"     (~10-15 min from the
#                     shipped 89@depth6 seed; see ../pipeline/README.md)
#
# The remaining methods here are LEGACY demonstrations of the moves on this
# project's superseded records ("91" ~5-60s, "89" ~1-4min, "90" ~10-30s);
# add them to RUN if you want to see the walk cut real circuits step by step.
RUN = ["97"]

OUT_DIR = "."          # folder for out_<record>.json files
VERBOSE = True         # print per-method progress

# ---- record 97 : depth-3 from-scratch annealer ---------------------------
C97 = dict(
    target_gates = 97,       # stop as soon as a circuit this small (or smaller) is found
    time_limit_s = 900,      # overall wall-clock budget across restarts
    anneal_iters = 150_000,  # simulated-annealing moves per restart
    ils_rounds   = 2_500,    # iterated-local-search kicks per restart
    sa_T0        = 2.0,      # SA start "temperature" (higher = wilder early moves)
    sa_T1        = 0.05,     # SA end temperature
    # RNG restart seeds, tried in order.  Seed 6 reliably hits 97 in ~1-2 min;
    # the rest are fallbacks so a plain run keeps trying until it beats target.
    seeds        = [6] + [s for s in range(1, 200) if s != 6],
    max_depth    = 3,        # hard depth cap (do not change for this record)
)

# ---- record 91 : depth-6, reduce a published 92 by one gate --------------
C91 = dict(
    max_depth    = 6,        # depth cap enforced at acceptance
    time_limit_s = 240,      # total budget across search-seeds
    slice_s      = 25,       # budget per search-seed before moving to the next
    swap_tries   = 60,       # neutral-swap attempts per plateau step
)

# ---- record 89 : reduce a 90-gate seed via the value-set walk ------------
C89 = dict(
    target_gates = 89,       # stop once the walk reaches this size
    per_seed_s   = 150,      # budget per RNG seed (two phases share this)
    total_s      = 2_400,    # overall budget; loops seeds until target hit
    phase1_frac  = 0.35,     # fraction of per-seed time spent in phase-1 swap_walk
    hub_move_p   = 0.35,     # P(remove-2-add-1 "hub" move) in phase 2 (the move that cuts)
    close_hamming= 4,        # bias hub pairs whose XOR has popcount <= this
    repair_hub   = 40,       # repair attempts after a hub move
    repair_one   = 24,       # repair attempts after a remove-1 move
    plateau_slack_p = 0.02,  # P(accept a size+1 plateau step to escape a rut)
)

# ---- record 90 : depth-6 LNS re-synthesis --------------------------------
C90 = dict(
    max_depth    = 6,
    lns_seconds  = 0,        # 0 = verify seed + prove irreducibility only (fast);
                             # >0 = also run the pure-Python LNS (reaches ~91, not 90)
    target_gates = 90,
    kmax         = 6,        # destroy 1..kmax non-target masks per LNS step
    kshake       = 12,       # occasional big destroy size
    snapback     = 8,        # reset current->best when current > best+snapback
    nsamp        = (24, 24), # (base, extra) pool + pairwise-sum sample sizes
    up_prob      = 0.5,      # P(accept a rebuild up to +up_slack larger)
    up_slack     = 4,
    rng_seed     = 1,
    show_irreducibility = True,  # print the "this seed has no local cut" proof
)

# ==========================================================================
# END CONFIG  --  implementation below
# ==========================================================================

import os, sys, json, time, math, random
from itertools import combinations

import mixcolumns_core as core
import seeds

T = core.TARGETS
TSET = core.TARGET_SET
INPUTS = core.INPUTS
ISET = core.INPUT_SET
bits_of = core.bits_of
wt = core.wt


def _log(msg):
    if VERBOSE:
        print(msg, flush=True)


# --------------------------------------------------------------------------
# METHOD  record 97  --  depth-3 from-scratch annealer
# --------------------------------------------------------------------------
def method_97(cfg, out_path):
    """SA + greedy descent + ILS over a shared-part model; every gate depth<=3
    by construction.  Returns index-pair gates."""
    maxd = cfg["max_depth"]

    def gen_splits(t):
        """Candidate ways to split output t into two depth-<=2 parts A,B
        (A ^ B == t).  weight-7 -> quad(4)+triple(3); weight-5 -> several."""
        bs = bits_of(t)
        S = set()
        if len(bs) == 7:
            for c in combinations(bs, 4):
                A = sum(1 << b for b in c)
                S.add((A, t ^ A))
        else:                                   # weight 5
            for c in combinations(bs, 4):
                A = sum(1 << b for b in c); S.add((A, t ^ A))
            for c in combinations(bs, 3):
                A = sum(1 << b for b in c); S.add((A, t ^ A))
            ext = [e for e in range(32) if not (t >> e) & 1]
            for c in combinations(bs, 3):
                base = sum(1 << b for b in c)
                for e in ext:
                    A = base | (1 << e)
                    S.add((A, t ^ A))
        return sorted(S)

    SPLITS = [gen_splits(t) for t in T]

    PAIRINGS = {}
    def get_pairings(m):
        """Ways to build a weight-3/4 part from depth-1 pairs."""
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
        """Reference-counted circuit: cost = 32 + #distinct pairs + #distinct parts."""
        __slots__ = ('rng', 'choice', 'big', 'pairs', 'pairing', 'cost')
        def __init__(s, seed):
            s.rng = random.Random(seed)
            s.choice = [None] * 32
            s.big = {}; s.pairs = {}; s.pairing = {}
            s.cost = 32
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
            best = None; bestnew = 99
            opts = get_pairings(m); n = len(opts)
            start = s.rng.randrange(n)
            for k in range(n):
                pr = opts[(start + k) % n]
                new = sum(1 for p in pr if s.pairs.get(p, 0) == 0)
                if new < bestnew: bestnew = new; best = pr
            return best
        def part_add(s, m):
            w = wt(m)
            if w == 1: return
            if w == 2: s.pair_add(m); return
            c = s.big.get(m, 0); s.big[m] = c + 1
            if c == 0:
                s.cost += 1
                best = s._best_pairing(m); s.pairing[m] = best
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
        def _part_add_forced(s, m, pg):
            w = wt(m)
            if w == 1: return
            if w == 2: s.pair_add(m); return
            c = s.big.get(m, 0); s.big[m] = c + 1
            if c == 0:
                s.cost += 1
                best = pg.get(m) or get_pairings(m)[0]
                s.pairing[m] = best
                for p in best: s.pair_add(p)
        def restore(s, snap):
            ch, pg, _ = snap
            for o in range(32): s.set_choice(o, None)
            s.pairing = {}
            for o in range(32):
                idx = ch[o]; s.choice[o] = idx
                A, B = SPLITS[o][idx]
                s._part_add_forced(A, pg); s._part_add_forced(B, pg)

    def descend(s):
        improved = True
        while improved:
            improved = False
            order = list(range(32)); s.rng.shuffle(order)
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
            temp = T0 * (T1 / T0) ** (it / iters)
            r = rng.random()
            if r < 0.60:
                o = rng.randrange(32); old = s.choice[o]; c0 = s.cost
                idx = rng.randrange(len(SPLITS[o]))
                if idx == old: continue
                s.set_choice(o, idx); d = s.cost - c0
                if d > 0 and rng.random() > math.exp(-d / temp):
                    s.set_choice(o, old)
            elif r < 0.85:
                if s.big:
                    s.repair(rng.choice(list(s.big.keys())))
            else:
                s.greedy_rechoice(rng.randrange(32))
            if s.cost < best[2]: best = s.snapshot()
        return best

    def kick(s, k):
        for _ in range(k):
            o = s.rng.randrange(32)
            s.set_choice(o, s.rng.randrange(len(SPLITS[o])))

    def solve_one(seed, label, deadline):
        _log("  [97] %6.1fs seed %d: annealing (%d moves, T %.2f -> %.2f)..."
             % (time.time() - t0, label, cfg["anneal_iters"], cfg["sa_T0"], cfg["sa_T1"]))
        s = State(seed)
        b = anneal(s, cfg["anneal_iters"], cfg["sa_T0"], cfg["sa_T1"])
        s.restore(b); descend(s); cur = s.snapshot()
        _log("  [97] %6.1fs seed %d: anneal + descent -> cost %d; iterated local search..."
             % (time.time() - t0, label, cur[2]))
        for r in range(cfg["ils_rounds"]):
            if (r & 63) == 0 and time.time() > deadline: break
            if cur[2] <= cfg["target_gates"]: break
            if r and r % 512 == 0:
                _log("  [97] %6.1fs seed %d: ILS round %d/%d, best this seed %d"
                     % (time.time() - t0, label, r, cfg["ils_rounds"], cur[2]))
            s.restore(cur); kick(s, s.rng.randrange(2, 7)); descend(s)
            if s.cost <= cur[2]: cur = s.snapshot()
        return cur

    def emit_index_pairs(snap):
        choices, pairing, _ = snap
        pairing = {int(k): tuple(v) for k, v in pairing.items()}
        bigs = {}; pairs = set(); finals = []
        for o in range(32):
            A, B = SPLITS[o][choices[o]]
            finals.append((T[o], A, B))
            for m in (A, B):
                w = wt(m)
                if w == 2: pairs.add(m)
                elif w >= 3 and m not in bigs:
                    bigs[m] = pairing.get(m) or get_pairings(m)[0]
        for m, pg in bigs.items():
            for p in pg: pairs.add(p)
        sig_index = {(1 << b): b for b in range(32)}
        gates = []
        def add_gate(mask, amask, bmask):
            gates.append([sig_index[amask], sig_index[bmask]])
            sig_index[mask] = 32 + len(gates) - 1
        for p in sorted(pairs):                       # depth 1
            i, j = bits_of(p); add_gate(p, 1 << i, 1 << j)
        for m in sorted(bigs):                         # depth 2
            pg = bigs[m]
            if wt(m) == 3:
                p = pg[0]; add_gate(m, p, m ^ p)
            else:
                p1, p2 = pg; add_gate(m, p1, p2)
        for t, A, B in finals:                         # depth 3
            add_gate(t, A, B)
        return gates

    t0 = time.time(); deadline = t0 + cfg["time_limit_s"]
    gbest = None
    for seed in cfg["seeds"]:
        if time.time() > deadline: break
        snap = solve_one(seed * 100003 + 17, seed, deadline)
        if gbest is None or snap[2] < gbest[2]: gbest = snap
        _log("  [97] %6.1fs seed %d: finished at cost %d (best overall %d, target %d)"
             % (time.time() - t0, seed, snap[2], gbest[2], cfg["target_gates"]))
        if gbest[2] <= cfg["target_gates"]: break
    return emit_index_pairs(gbest)


# --------------------------------------------------------------------------
# METHOD  record 91  --  reduce a published 92-gate circuit by one gate
# --------------------------------------------------------------------------
def method_91(cfg, out_path):
    """Value-set neutral-swap plateau walk: reduce the published 92 to 91 at
    depth<=6.  Returns index-pair gates."""
    maxd = cfg["max_depth"]
    OUT = TSET

    def seed_value_set():
        """Run the published in-place SLP; collect the non-input masks produced."""
        reg = {i: 1 << i for i in range(32)}
        V = set()
        for (i, j) in seeds.PUBLISHED_92_SLP:
            nv = reg[i] ^ reg[j]; reg[i] = nv
            if nv not in ISET: V.add(nv)
        return V

    def unbuilt(S):
        """Subset of S NOT buildable by XOR-closure from the inputs, plus the
        buildable 'built' set."""
        built = set(INPUTS); ub = set(S) - built; frontier = list(built)
        while frontier:
            a = frontier.pop()
            newly = [v for v in ub if (v ^ a) in built]
            for v in newly:
                ub.discard(v); built.add(v); frontier.append(v)
        return ub, built

    def realizable(S):
        return not unbuilt(S)[0]

    def min_depth(S):
        universe = set(S) | set(INPUTS)
        dep = {v: 0 for v in INPUTS}; changed = True
        while changed:
            changed = False
            for v in S:
                if v in ISET: continue
                best = None
                for a in universe:
                    b = v ^ a
                    if a != b and b in dep and a in dep:
                        d = 1 + max(dep[a], dep[b])
                        if best is None or d < best: best = d
                if best is not None and best < dep.get(v, 1 << 30):
                    dep[v] = best; changed = True
        return dep

    def depth_ok(S):
        dep = min_depth(S)
        return all(v in dep for v in S) and max(dep[v] for v in S) <= maxd

    def repair_candidates(S):
        ub, built = unbuilt(S)
        if not ub: return []
        cands = set()
        for u in ub:
            for c in built:
                v = u ^ c
                if v and v not in S and v not in ISET: cands.add(v)
        good = []
        for v in cands:
            if not any((v ^ a) in built and (v ^ a) != v for a in built): continue
            if realizable(S | {v}): good.append(v)
        return good

    def reduce_one(V, seed, budget):
        rnd = random.Random(seed); V = set(V); t0 = time.time()
        while time.time() - t0 < budget:
            removable = sorted(w for w in V if w not in OUT)
            rnd.shuffle(removable)
            for w in removable:                       # probe a real remove-1
                S = V - {w}
                if realizable(S) and depth_ok(S):
                    return S
            for _ in range(cfg["swap_tries"]):        # else a neutral swap
                w = rnd.choice(removable); S = V - {w}
                good = [v for v in repair_candidates(S) if v != w]
                if not good: continue
                V = S | {rnd.choice(good)}; break
        return None

    def reconstruct(S):
        dep = min_depth(S)
        order = sorted((v for v in S if v not in ISET), key=lambda v: dep[v])
        have = set(INPUTS); idx = {1 << i: i for i in range(32)}; pairs = []
        for v in order:
            best = None
            for a in have:
                b = v ^ a
                if a != b and b in have:
                    key = max(dep[a], dep[b])
                    if best is None or key < best[0]: best = (key, a, b)
            if best is None: raise RuntimeError("unbuildable value")
            _, a, b = best
            pairs.append([idx[a], idx[b]]); idx[v] = 32 + len(pairs) - 1; have.add(v)
        return pairs

    V = seed_value_set()
    assert realizable(V) and all(t in V for t in T) and depth_ok(V), "bad seed"
    _log("  [91] seed: %d gates (depth<=%d, all 32 outputs)" % (len(V), maxd))
    t0 = time.time(); reduced = None; sd = 0
    while reduced is None and time.time() - t0 < cfg["time_limit_s"]:
        sd += 1
        remaining = cfg["time_limit_s"] - (time.time() - t0)
        reduced = reduce_one(V, sd, min(cfg["slice_s"], remaining))
        if reduced is None:
            _log("  [91] seed %d: no reduction within slice, retrying" % sd)
    if reduced is None:
        _log("  [91] FAILED to reduce within budget"); return None
    _log("  [91] reduced to %d gates on search-seed %d (%.1fs)"
         % (len(reduced), sd, time.time() - t0))
    return reconstruct(reduced)


# --------------------------------------------------------------------------
# METHOD  record 89  --  value-set walk reducing a 90-gate seed to 89
# --------------------------------------------------------------------------
def method_89(cfg, out_path):
    """Two-phase value-set local search (swap_walk then hub-move walk) that cuts
    a 90-gate seed to 89.  Returns index-pair gates."""

    def closure(S):
        avail = set(INPUTS); order = []; parents = {}
        remaining = set(S) - avail; progress = True
        while progress and remaining:
            progress = False
            for v in list(remaining):
                for a in avail:
                    b = v ^ a
                    if b in avail:
                        avail.add(v); remaining.discard(v)
                        order.append(v); parents[v] = (a, b)
                        progress = True; break
        return avail, order, parents

    def realizable(S):
        avail, _, _ = closure(S); return TSET <= avail

    def trim(S):
        avail, order, parents = closure(S)
        assert TSET <= avail
        needed = set(); stack = list(TSET)
        while stack:
            v = stack.pop()
            if v in needed or v in ISET: continue
            needed.add(v); a, b = parents[v]; stack.append(a); stack.append(b)
        return [v for v in order if v in needed], parents

    def trimmed_set(S):
        topo, _ = trim(S); return set(topo)

    def repair_candidates(S2, rng, tries):
        avail, order, parents = closure(S2)
        if TSET <= avail: return S2
        wanted = list((set(S2) | TSET) - avail); avail_list = list(avail)
        for _ in range(tries):
            c = rng.choice(wanted); a = rng.choice(avail_list); w = c ^ a
            if w == 0 or w in avail or w in ISET: continue
            if not any((w ^ p) in avail for p in avail_list): continue
            S3 = set(S2) | {w}
            av3, _, _ = closure(S3)
            if TSET <= av3: return S3
        return None

    def swap_walk(S, seconds, rng):
        """Phase 1: remove-1, else repair-add-1; greedily keep any reduction."""
        cur = trimmed_set(S); best = set(cur); t0 = time.time()
        while time.time() - t0 < seconds:
            nont = [v for v in cur if v not in TSET]
            if not nont: break
            v = rng.choice(nont); S2 = cur - {v}
            avail, order, parents = closure(S2)
            if TSET <= avail:
                cur = trimmed_set(S2)
                if len(cur) < len(best): best = set(cur)
                continue
            wanted = (set(S2) | TSET) - avail; avail_list = list(avail)
            for _ in range(cfg["repair_one"]):
                if not wanted: break
                c = rng.choice(list(wanted)); a = rng.choice(avail_list); w = c ^ a
                if w == 0 or w in avail or w in ISET: continue
                if not any((w ^ p) in avail for p in avail_list): continue
                S3 = S2 | {w}; av3, _, _ = closure(S3)
                if TSET <= av3:
                    nxt = trimmed_set(S3)
                    if len(nxt) <= len(cur): cur = nxt; break
            if len(cur) < len(best): best = set(cur)
        return best

    def walk(S, seconds, rng):
        """Phase 2: 65% remove-1, 35% remove-2-add-1 hub move; the hub move is
        what actually cuts a gate.  Rare +1 plateau slack to escape ruts."""
        cur = trimmed_set(S); best = set(cur); t0 = time.time()
        while time.time() - t0 < seconds:
            nont = [v for v in cur if v not in TSET]
            if len(nont) < 2: break
            if rng.random() < cfg["hub_move_p"]:
                v1 = rng.choice(nont)
                if rng.random() < 0.5:
                    cand = [u for u in nont if u != v1
                            and bin(u ^ v1).count("1") <= cfg["close_hamming"]]
                    v2 = rng.choice(cand) if cand else rng.choice([u for u in nont if u != v1])
                else:
                    v2 = rng.choice([u for u in nont if u != v1])
                S2 = cur - {v1, v2}; av, _, _ = closure(S2)
                if TSET <= av:
                    cur = trimmed_set(S2)
                else:
                    fixed = repair_candidates(S2, rng, cfg["repair_hub"])
                    if fixed is not None:
                        nxt = trimmed_set(fixed)
                        if len(nxt) < len(cur): cur = nxt
            else:
                v = rng.choice(nont); S2 = cur - {v}; av, _, _ = closure(S2)
                if TSET <= av:
                    cur = trimmed_set(S2)
                else:
                    fixed = repair_candidates(S2, rng, cfg["repair_one"])
                    if fixed is not None:
                        nxt = trimmed_set(fixed)
                        slack = 1 if (rng.random() < cfg["plateau_slack_p"]
                                      and len(cur) < len(best) + 2) else 0
                        if len(nxt) <= len(cur) + slack: cur = nxt
            if len(cur) < len(best): best = set(cur)
        return best

    def to_index_pairs(S):
        topo, parents = trim(S); idx = {1 << i: i for i in range(32)}; gates = []
        for k, v in enumerate(topo):
            a, b = parents[v]; gates.append([idx[a], idx[b]]); idx[v] = 32 + k
        return gates

    def run_once(seed, seconds):
        rng = random.Random(seed)
        S = set(seeds.SEED_90_MASKS)
        assert realizable(S), "seed not realizable"
        half = seconds * cfg["phase1_frac"]
        b1 = swap_walk(S, half, rng)
        best = walk(b1, seconds - half, rng)
        return best

    t0 = time.time(); seed = 0; best_set = None; best_n = 10 ** 9
    while time.time() - t0 < cfg["total_s"]:
        seed += 1
        cand = run_once(seed, cfg["per_seed_s"]); n = len(cand)
        if n < best_n:
            best_n = n; best_set = cand
            _log("  [89] new best %d (seed %d, %.0fs)" % (n, seed, time.time() - t0))
        if best_n <= cfg["target_gates"]:
            _log("  [89] reached target %d at seed %d" % (best_n, seed)); break
    return to_index_pairs(best_set)


# --------------------------------------------------------------------------
# METHOD  record 90  --  depth-6 large-neighbourhood re-synthesis
# --------------------------------------------------------------------------
def method_90(cfg, out_path):
    """Depth-limited LNS (destroy-and-rebuild) seeded from the 91-gate circuit.
    In pure Python this reaches ~91; also proves the seed has no single local
    cut.  Returns index-pair gates for the best circuit obtained."""
    from collections import defaultdict, deque
    MAXD = cfg["max_depth"]; INF = 99
    TLIST = T; TSETL = TSET

    # ---- id-based model over the 91-gate seed --------------------------
    def load_seed_gates():
        id_of = {1 << k: k for k in range(32)}; gates = []
        for i, (m, am, bm) in enumerate(seeds.SEED_91_TRIPLES):
            gates.append((m, id_of[am], id_of[bm])); id_of[m] = 32 + i
        return gates

    def build_masks(gates):
        return [1 << i for i in range(32)] + [g[0] for g in gates]

    def valid(gates):
        d = [0] * 32; masks = [1 << i for i in range(32)]
        for gi, (m, a, b) in enumerate(gates):
            sid = 32 + gi
            if a >= sid or b >= sid or masks[a] ^ masks[b] != m: return False
            nd = 1 + max(d[a], d[b])
            if nd > MAXD: return False
            d.append(nd); masks.append(m)
        return TSETL <= set(masks)

    def max_depth_of(gates):
        d = [0] * 32
        for (m, a, b) in gates: d.append(1 + max(d[a], d[b]))
        return max(d[32:], default=0)

    def topo_fix(gates):
        n = len(gates); indeg = [0] * n; dep = [[] for _ in range(n)]
        for i, (m, a, b) in enumerate(gates):
            for p in (a, b):
                if p >= 32: dep[p - 32].append(i); indeg[i] += 1
        q = deque(i for i in range(n) if indeg[i] == 0); order = []
        while q:
            i = q.popleft(); order.append(i)
            for j in dep[i]:
                indeg[j] -= 1
                if indeg[j] == 0: q.append(j)
        if len(order) != n: return None
        newid = {32 + i: 32 + pos for pos, i in enumerate(order)}
        return [(m, a if a < 32 else newid[a], b if b < 32 else newid[b])
                for (m, a, b) in (gates[i] for i in order)]

    def gc(gates):
        changed = True
        while changed:
            changed = False; used = set()
            for (m, a, b) in gates: used.add(a); used.add(b)
            keep, remap = [], {}
            for i, (m, a, b) in enumerate(gates):
                sid = 32 + i
                if sid not in used and m not in TSETL: changed = True; continue
                remap[sid] = 32 + len(keep); keep.append((m, a, b))
            if changed:
                gates = [(m, a if a < 32 else remap[a], b if b < 32 else remap[b])
                         for (m, a, b) in keep]
        return gates

    def ancestors(gates):
        anc = [set() for _ in range(32 + len(gates))]
        for gi, (m, a, b) in enumerate(gates):
            anc[32 + gi] = {a, b} | anc[a] | anc[b]
        return anc

    def alt_pairs_for(gates, masks, mask2ids, ci, anc):
        sid = 32 + ci; m, pa, pb = gates[ci]; res, seen = [], set()
        for u in range(32 + len(gates)):
            if u == sid: continue
            for v in mask2ids.get(masks[u] ^ m, ()):
                if v == sid or v <= u or (u, v) in seen: continue
                seen.add((u, v))
                if {u, v} == {pa, pb} or sid in anc[u] or sid in anc[v]: continue
                res.append((u, v))
        return res

    def variant_A_cut(base):
        masks = build_masks(base)
        mask2ids = defaultdict(list)
        for i, mm in enumerate(masks): mask2ids[mm].append(i)
        anc = ancestors(base); d = [0] * 32
        for (m, a, b) in base: d.append(1 + max(d[a], d[b]))
        cons = defaultdict(list)
        for gi, (m, a, b) in enumerate(base):
            cons[a].append(32 + gi); cons[b].append(32 + gi)
        for gi, (m, a, b) in enumerate(base):
            G = 32 + gi
            if m in TSETL: continue
            cand = list(base); ok = True
            for C in cons.get(G, []):
                ci = C - 32; Cmask = base[ci][0]; picked = None
                for (u, v) in alt_pairs_for(base, masks, mask2ids, ci, anc):
                    if u == G or v == G: continue
                    if 1 + max(d[u], d[v]) <= MAXD: picked = (u, v); break
                if picked is None: ok = False; break
                cand[ci] = (Cmask, picked[0], picked[1])
            if not ok: continue
            c2 = gc(topo_fix(cand) or cand)
            if len(c2) < len(base) and valid(c2): return c2
        return None

    # ---- dls relax/extract/peel/lns (faithful port of dls.c) -----------
    def relax(avail):
        na = len(avail); pos = {m: i for i, m in enumerate(avail)}
        dep = [0] * 32 + [INF] * (na - 32); changed = True
        while changed:
            changed = False
            for i in range(32, na):
                cur = dep[i]
                if cur == 1: continue
                S = avail[i]; best = cur
                for j in range(na):
                    dA = dep[j]
                    if dA + 1 >= best: continue
                    B = S ^ avail[j]
                    if B == 0 or B == S: continue
                    bi = pos.get(B)
                    if bi is None: continue
                    nd = 1 + (dA if dA > dep[bi] else dep[bi])
                    if nd < best:
                        best = nd
                        if best == 1: break
                if best < cur: dep[i] = best; changed = True
        return dep, pos

    def feasible_set(mset):
        avail = [1 << i for i in range(32)] + list(mset)
        dep, _ = relax(avail)
        return all(dep[i] <= MAXD for i in range(32, len(avail)))

    def extract(avail, dep, pos, preferred, rng, noise=True):
        na = len(avail)
        for t in TLIST:
            i = pos.get(t)
            if i is None or dep[i] > MAXD: return None
        inU = [False] * na; processed = [i < 32 for i in range(na)]
        for t in TLIST: inU[pos[t]] = True
        while True:
            pick = -1; pd = -1
            for i in range(32, na):
                if inU[i] and not processed[i] and dep[i] > pd: pd = dep[i]; pick = i
            if pick < 0: break
            processed[pick] = True; S = avail[pick]; ds = dep[pick]
            bestc = 9; bi = bj = -1; nties = 0
            for j in range(na):
                if dep[j] >= ds: continue
                B = S ^ avail[j]; k = pos.get(B)
                if k is None or dep[k] >= ds: continue
                if avail[j] > B: continue
                c = 0
                if j >= 32 and not inU[j]: c += 1 if preferred[j] else 2
                if k >= 32 and not inU[k]: c += 1 if preferred[k] else 2
                if noise and rng.randrange(8) == 0: c += rng.randrange(2)
                if c < bestc: bestc = c; bi = j; bj = k; nties = 1
                elif c == bestc:
                    nties += 1
                    if rng.randrange(nties) == 0: bi = j; bj = k
            if bi < 0: return None
            if bi >= 32: inU[bi] = True
            if bj >= 32: inU[bj] = True
        return [avail[i] for i in range(32, na) if inU[i]]

    def peel(mset, rng):
        s = list(mset); improved = True
        while improved:
            improved = False; idx = list(range(len(s))); rng.shuffle(idx)
            for i in idx:
                if i >= len(s) or s[i] in TSETL: continue
                tmp = s[:i] + s[i + 1:]
                if feasible_set(tmp): s = tmp; improved = True; break
        return s

    def order_by_depth(mset):
        avail = [1 << i for i in range(32)] + list(mset)
        dep, pos = relax(avail); out = []
        for lvl in range(1, MAXD + 1):
            for i in range(32, len(avail)):
                if dep[i] != lvl: continue
                S = avail[i]; done = False
                for j in range(len(avail)):
                    if dep[j] >= lvl: continue
                    B = S ^ avail[j]; k = pos.get(B)
                    if k is None or dep[k] >= lvl: continue
                    out.append((S, avail[j], B)); done = True; break
                if not done: raise RuntimeError("cannot realize mask")
        return out

    def lns(seed_masks, pool, seconds, rng_seed, target, kmax, kshake,
            snapback, nsamp, up_prob, up_slack, accumulate, start_masks):
        rng = random.Random(rng_seed); t0 = time.time()
        init = start_masks if start_masks is not None else seed_masks
        assert feasible_set(init), "start infeasible"
        Ucur = peel(init, rng); Ubest = list(Ucur); iters = 0
        while time.time() - t0 < seconds:
            iters += 1; nu = len(Ucur)
            k = 1 + rng.randrange(kmax)
            if iters % 997 == 0: k = kshake + rng.randrange(5)
            nontarget = [i for i in range(nu) if Ucur[i] not in TSETL]
            rng.shuffle(nontarget); vict = set(nontarget[:k])
            kept = [Ucur[i] for i in range(nu) if i not in vict]; nkeep = len(kept)
            Tm = list(kept)
            for _ in range(nsamp[0] + rng.randrange(nsamp[1])):
                Tm.append(pool[rng.randrange(len(pool))])
            for _ in range(nsamp[0] + rng.randrange(nsamp[1])):
                m = kept[rng.randrange(nkeep)] ^ kept[rng.randrange(nkeep)]
                if m: Tm.append(m)
            seen = set(); T2 = []
            for m in Tm:
                if m not in seen and bin(m).count("1") > 1: seen.add(m); T2.append(m)
            avail = [1 << i for i in range(32)] + T2
            dep, pos = relax(avail); preferred = [False] * len(avail)
            keptset = set(kept)
            for i in range(32, len(avail)):
                if avail[i] in keptset: preferred[i] = True
            res = extract(avail, dep, pos, preferred, rng)
            if res is None: continue
            r = len(res)
            accept = (r <= nu) or (r <= nu + up_slack and rng.random() < up_prob)
            if accept:
                if accumulate is not None:
                    for m in res:
                        if m not in accumulate: accumulate.add(m); pool.append(m)
                Ucur = res
                if len(Ucur) < len(Ubest):
                    Ucur = peel(Ucur, rng); Ubest = list(Ucur)
                    _log("  [90] %6.1fs best=%d (it %d)" % (time.time() - t0, len(Ubest), iters))
                    if len(Ubest) <= target: return Ubest, iters
            if len(Ucur) > len(Ubest) + snapback: Ucur = list(Ubest)
            if iters % 5000 == 0:
                Ucur = peel(Ucur, rng)
                if len(Ucur) < len(Ubest):
                    Ubest = list(Ucur)
                    if len(Ubest) <= target: return Ubest, iters
        return Ubest, iters

    def triples_to_index_pairs(gates):
        masks = build_masks(gates)
        return [[a, b] for (m, a, b) in gates]

    def set_to_gates(mask_set):
        trip = order_by_depth(mask_set); idof = {1 << k: k for k in range(32)}; g = []
        for i, (m, a, b) in enumerate(trip):
            g.append((m, idof[a], idof[b])); idof[m] = 32 + i
        return gc(g)

    # ---- run -----------------------------------------------------------
    base = gc(load_seed_gates())
    assert valid(base), "seed did not verify"
    _log("  [90] seed: gates=%d depth=%d outputs=32/32" % (len(base), max_depth_of(base)))

    if cfg["show_irreducibility"]:
        sol = [g[0] for g in base]
        dup = len(sol) - len(set(sol))
        peeled = peel(sol, random.Random(0))
        ra = variant_A_cut(base)
        _log("  [90] irreducibility of this seed: duplicate masks=%d, "
             "peel remove-1=%d, single-gate cut=%s"
             % (dup, len(sol) - len(peeled), "none" if ra is None else len(ra)))
        _log("  [90] => no single local cut; the elite 90 is a global re-synthesis, "
             "not a one-gate cut of this seed.")

    best_gates = base
    if cfg["lns_seconds"] > 0:
        sol = [g[0] for g in base]; S = set(sol)
        for a in sol:
            for b in sol:
                m = a ^ b
                if m and bin(m).count("1") > 1: S.add(m)
        pool = sorted(S); rng = random.Random(cfg["rng_seed"])
        avail = [1 << i for i in range(32)] + pool
        dep, pos = relax(avail); pref = [False] * len(avail); start = None
        for _ in range(40):
            r = extract(avail, dep, pos, pref, rng, noise=True)
            if r and (start is None or len(r) < len(start)): start = r
        start = peel(list(start), rng)
        _log("  [90] running LNS for %ds (pure Python reaches ~91)..." % cfg["lns_seconds"])
        bestset, iters = lns(sol, list(pool), cfg["lns_seconds"], cfg["rng_seed"],
                             cfg["target_gates"], cfg["kmax"], cfg["kshake"],
                             cfg["snapback"], cfg["nsamp"], cfg["up_prob"],
                             cfg["up_slack"], set(pool), start)
        g = set_to_gates(bestset)
        if valid(g) and len(g) < len(best_gates): best_gates = g

    return triples_to_index_pairs(best_gates)


# --------------------------------------------------------------------------
# Runner
# --------------------------------------------------------------------------
METHODS = {
    "97": (method_97, C97, 3),
    "91": (method_91, C91, 6),
    "89": (method_89, C89, None),
    "90": (method_90, C90, 6),
}

LABELS = {
    "97": "from scratch -> 97 gates @ depth 3: ties the CURRENT depth-3 record",
    "91": "legacy demo: published 92-gate circuit -> 91 @ depth 6 (record superseded by 89 @ depth 5)",
    "89": "legacy demo: 90-gate seed -> 89 gates, unconstrained depth (superseded by 89 @ depth 5)",
    "90": "legacy demo: local-irreducibility proof of a 91-gate seed (optional LNS)",
}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    results = []
    for rec in RUN:
        if rec not in METHODS:
            print("unknown record %r (choose from %s)" % (rec, list(METHODS)))
            continue
        fn, cfg, depth_cap = METHODS[rec]
        out_path = os.path.join(OUT_DIR, "out_%s.json" % rec)
        _log("\n=== method %s: %s ===" % (rec, LABELS[rec]))
        t0 = time.time()
        gates = fn(cfg, out_path)
        dt = time.time() - t0
        if gates is None:
            results.append((rec, "FAILED", 0, 0, dt)); continue
        v = core.verify(gates, max_depth=depth_cap)
        core.save(gates, out_path, extra={"depth": v["depth"], "verified": v["ok"]})
        status = "VERIFIED" if v["ok"] else "INVALID(%s)" % (v["problems"][:1] or v["outputs"])
        results.append((rec, status, v["gates"], v["depth"], dt))
        _log("  -> %s: %d gates, depth %d, %s  (%.1fs) -> %s"
             % (rec, v["gates"], v["depth"], status, dt, out_path))

    print("\n" + "=" * 72)
    print("%-8s %-10s %6s %6s %8s   %s" % ("method", "status", "gates", "depth", "time", "what it was"))
    print("-" * 72)
    for rec, status, g, d, dt in results:
        print("%-8s %-10s %6s %6s %7.1fs   %s" % (rec, status, g, d, dt, LABELS[rec]))
    print("=" * 72)
    print("Every out_<method>.json is independently checkable:")
    print("  python3 ../verify_circuit.py out_97.json 3")
    print("The current 92@depth4 and 89@depth5 records reproduce with the")
    print("pipeline, not this file -- see ../pipeline/README.md.")


if __name__ == "__main__":
    main()
