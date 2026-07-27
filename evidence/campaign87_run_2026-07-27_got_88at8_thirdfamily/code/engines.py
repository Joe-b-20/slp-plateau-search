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
import time, math, random, itertools, json, glob, os
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
def relax_reference(avail):
    """Original O(passes * n^2) fixpoint (kept verbatim for the rare
    duplicate-mask case).  Returns (dep list, pos dict)."""
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


def relax(avail):
    """Minimum XOR build-depth of every mask in `avail` (inputs depth 0).
    Level-BFS rewrite (relax-kernel agent): same least-fixpoint values as
    relax_reference; falls back to the reference on duplicate masks."""
    na = len(avail)
    pos = {m: i for i, m in enumerate(avail)}
    if len(pos) != na:                       # duplicate masks: rare, exact legacy path
        return relax_reference(avail)
    dep = [0] * 32 + [INF] * (na - 32)
    if na <= 32:
        return dep, pos
    resolved = set(avail[:32])
    frontier = avail[:32]
    unresolved = range(32, na)
    d = 1
    if avail[:32] == INPUTS:
        # level-1 shortcut: with the standard input singletons at depth 0, a
        # mask resolves at depth 1 iff wt==2 (a^b, two inputs) or it is 0.
        still = []; newly = []
        for i in unresolved:
            S = avail[i]
            t = S & (S - 1)
            if S == 0 or (t != 0 and t & (t - 1) == 0):
                dep[i] = 1
                newly.append(S)
            else:
                still.append(i)
        if not still:
            return dep, pos
        resolved.update(newly)
        frontier = newly
        unresolved = still
        d = 2
    while frontier:
        still = []; newly = []
        for i in unresolved:
            S = avail[i]
            for a in frontier:
                if S ^ a in resolved:
                    dep[i] = d
                    newly.append(S)
                    break
            else:
                still.append(i)
        if not still:
            break
        resolved.update(newly)
        frontier = newly
        unresolved = still
        d += 1
    return dep, pos


def feasible_at(mask_set, cap):
    """True iff every mask in the set is realizable AND (if cap given) builds at
    depth <= cap.  With cap=None only realizability matters (relax-kernel
    agent): the depth bookkeeping is dropped and the closure exits False as
    soon as a round resolves nothing."""
    if cap is not None or not ISET.isdisjoint(mask_set):
        avail = list(INPUTS) + list(mask_set)
        dep, _ = relax(avail)
        for i in range(32, len(avail)):
            if dep[i] >= INF:
                return False
            if cap is not None and dep[i] > cap:
                return False
        return True
    resolved = set(INPUTS)
    pending = []; frontier = []
    for S in mask_set:                       # round 1: wt==2 (or 0) resolves
        t = S & (S - 1)
        if S == 0 or (t != 0 and t & (t - 1) == 0):
            frontier.append(S)
        else:
            pending.append(S)
    if pending and not frontier:
        return False
    resolved.update(frontier)
    while pending:
        still = []; newly = []
        for S in pending:
            for a in frontier:
                if S ^ a in resolved:
                    newly.append(S)
                    break
            else:
                still.append(S)
        if not newly:
            return False
        resolved.update(newly)
        frontier = newly
        pending = still
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
def _closure_core(S, stop_at_targets=False):
    """Worklist closure (closure-kernel agent): same least fixpoint as the
    original fixpoint loop, O(|S|^2) instead of O(passes * |S| * |avail|).
    Returns (avail, order, parents, remaining) with remaining = S - realized.
    If stop_at_targets, stops as soon as all 32 targets are available."""
    avail = set(INPUTS)
    order = []; parents = {}
    remaining = set(S) - avail
    tleft = len(TSET & remaining) if stop_at_targets else -1
    newly = []
    # seed: masks realizable from the inputs alone (= weight-2 masks; 0 is the
    # degenerate a^a case the naive loop also admits)
    for v in list(remaining):
        w = wt(v)
        if w == 2:
            lo = v & -v
            avail.add(v); remaining.discard(v)
            order.append(v); parents[v] = (lo, v ^ lo); newly.append(v)
        elif v == 0:
            avail.add(v); remaining.discard(v)
            order.append(v); parents[v] = (INPUTS[0], INPUTS[0]); newly.append(v)
    qi = 0
    while qi < len(newly) and remaining:
        u = newly[qi]; qi += 1
        hits = [v for v in remaining if (v ^ u) in avail]
        for v in hits:
            avail.add(v); remaining.discard(v)
            order.append(v); parents[v] = (u, v ^ u); newly.append(v)
            if tleft >= 0 and v in TSET:
                tleft -= 1
                if tleft == 0:
                    return avail, order, parents, remaining
    return avail, order, parents, remaining


def closure(S):
    avail, order, parents, _ = _closure_core(S)
    return avail, order, parents


def realizable(S):
    Sset = S if isinstance(S, (set, frozenset)) else set(S)
    if not TSET <= Sset:   # targets have weight 5/7, never inputs: must be in S
        return False
    avail, _, _, _ = _closure_core(Sset, stop_at_targets=True)
    return TSET <= avail


def trim_masks(S):
    """Keep only masks needed to reach the 32 targets."""
    avail, order, parents, _ = _closure_core(S, stop_at_targets=True)
    if not (TSET <= avail):
        return set(S)
    needed = set(); stack = list(TSET)
    while stack:
        v = stack.pop()
        if v in needed or v in ISET:
            continue
        needed.add(v); a, b = parents[v]; stack.append(a); stack.append(b)
    return needed


class _WalkState:
    """Incremental closure over the walk's current (realizable) mask set
    (closure-kernel agent).  On a removal query, re-derives only the masks
    whose recorded derivation transitively used a removed mask.  The result is
    the exact least fixpoint of S - D."""
    __slots__ = ("S", "avail", "order", "parents")

    def __init__(self, cur):
        self.reset(cur)

    def reset(self, cur):
        self.S = set(cur)
        avail, order, parents, _ = _closure_core(self.S)
        self.avail = avail; self.order = order; self.parents = parents

    def remove_query(self, D):
        """Exact closure info for S - D.
        Returns (ok, avail2, unrealized):
          avail2     == closure(S - D)[0]
          unrealized == (S - D) - avail2
          ok         == TSET <= avail2."""
        aff = set(D)
        parents = self.parents
        for u in self.order:                     # topological, so one pass
            if u in aff:
                continue
            a, b = parents[u]
            if a in aff or b in aff:
                aff.add(u)
        avail2 = self.avail - aff
        remaining = aff.difference(D)
        newly = []
        base = list(avail2)
        for v in list(remaining):
            for a in base:
                if (v ^ a) in avail2:
                    avail2.add(v); remaining.discard(v); newly.append(v)
                    break
        qi = 0
        while qi < len(newly) and remaining:
            u = newly[qi]; qi += 1
            hits = [v for v in remaining if (v ^ u) in avail2]
            for v in hits:
                avail2.add(v); remaining.discard(v); newly.append(v)
        return TSET <= avail2, avail2, remaining


# ==========================================================================
# ENGINE  "lns"  --  depth-capped destroy & rebuild
# ==========================================================================
def _extract(avail, dep, pos, preferred, rng, cap, noise=True, useful=None):
    """Greedy top-down rebuild of all targets from the candidate pool.

    preferred: per-index pull-in cost class (lns-extract agent).  Backward
    compatible: a bool list (True -> cost 1, False -> cost 2) or an int list
    giving the pull-in cost directly (1=kept, 2=sampled, 3=destroyed-victim).
    useful: optional per-index reuse score used as a small tie-break."""
    na = len(avail)
    for t in T:
        i = pos.get(t)
        if i is None or dep[i] >= INF or (cap is not None and dep[i] > cap):
            return None
    cost_of = preferred
    if preferred and isinstance(preferred[0] if len(preferred) else False, bool):
        cost_of = [1 if p else 2 for p in preferred]
    inU = [False] * na; processed = [i < 32 for i in range(na)]
    SCALE = 64
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
        bestc = 9 * SCALE; bi = bj = -1; nties = 0
        for j in range(na):
            if dep[j] >= ds:
                continue
            B = S ^ avail[j]; k = pos.get(B)
            if k is None or dep[k] >= ds or avail[j] > B:
                continue
            cst = 0
            if j >= 32 and not inU[j]:
                cst += cost_of[j] * SCALE
                if useful is not None:
                    cst -= useful[j]
            if k >= 32 and not inU[k]:
                cst += cost_of[k] * SCALE
                if useful is not None:
                    cst -= useful[k]
            if noise and rng.randrange(8) == 0:
                cst += rng.randrange(2) * SCALE
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


def dag_info(Ucur):
    """depth, canonical parents, fanout (refcount as parent), children
    (lns-destroy agent)."""
    avail = list(INPUTS) + list(Ucur)
    dep, pos = relax(avail)
    parents = {}
    for i in range(32, len(avail)):
        S = avail[i]; d = dep[i]
        for j in range(len(avail)):
            if dep[j] >= d:
                continue
            B = S ^ avail[j]
            kb = pos.get(B)
            if kb is None or dep[kb] >= d:
                continue
            parents[S] = (avail[j], B)
            break
    fan = {m: 0 for m in Ucur}
    children = {m: [] for m in Ucur}
    for m, (a, b) in parents.items():
        for p in (a, b):
            if p in fan:
                fan[p] += 1
                children[p].append(m)
    depth = {avail[i]: dep[i] for i in range(32, len(avail))}
    return depth, parents, fan, children


def _inject(victims, kept, rng, per_victim=6):
    """Victim-aware repair candidates: shifted copies v^u, v^input, and victim
    pairwise sums (lns-destroy agent)."""
    ex = []
    nk = len(kept)
    for v in victims:
        for _ in range(per_victim):
            m = v ^ kept[rng.randrange(nk)]
            if m and wt(m) > 1:
                ex.append(m)
        for _ in range(2):
            m = v ^ (1 << rng.randrange(32))
            if wt(m) > 1:
                ex.append(m)
    vl = list(victims)
    for i in range(len(vl)):
        for j in range(i + 1, len(vl)):
            m = vl[i] ^ vl[j]
            if m and wt(m) > 1:
                ex.append(m)
    return ex


def _cone_pick(nontarget, rng, info, kk):
    """Grow a connected victim set: children of victims + parents that only
    feed the victim set (lns-destroy agent)."""
    depth, parents, fan, children = info
    nts = set(nontarget)
    v = rng.choice(nontarget)
    vict = {v}
    for _ in range(kk * 3):
        if len(vict) >= kk:
            break
        cand = set()
        for u in vict:
            a, b = parents.get(u, (0, 0))
            for p in (a, b):
                if p in nts and p not in vict and \
                   all(c in vict for c in children.get(p, [])):
                    cand.add(p)                       # parent only feeding vict
            for c in children.get(u, []):
                if c in nts and c not in vict:
                    cand.add(c)                       # child of a victim
        cand -= vict
        if not cand:
            break
        vict.add(rng.choice(sorted(cand)))
    return list(vict)


def engine_lns(start_masks, cap, target, time_limit, seeds, k, ctx):
    """MERGED LNS (wave-2 merged-engine): destroy / rebuild with

      * level-BFS relax + realizability-only feasible_at   (relax-kernel, 17.5x)
      * victim-repool at cost class 3                      (lns-extract, ~34x accepts)
      * coneinj destroy op mix + injected candidates       (lns-destroy, ~12x improves)
      * PEEL-BEFORE-ACCEPT for near-miss rebuilds          (lns-destroy next-step)
      * scored hot-multiset pool sampling + peel cache     (lns-pool, ~11x)
      * SA acceptance with reheat                          (acceptance-schedule)
      * plateau harvesting of every distinct best-size set (knob-sweep next-step)
      * periodic cross-pollination from sibling harvests   (wave-2 brief)

    Extra knobs (all with safe defaults): op_mix, vic_cost, hot_frac, sa_T0,
    sa_cool, sa_reheat, peel_window, harvest_path, pop_glob, pop_period_s.
    """
    rng = random.Random(seeds[0] if seeds else 1)
    if start_masks is None:
        start_masks = core.naive_masks()
    start = set(start_masks)
    if not feasible_at(start, cap):
        ctx.log("[lns] start circuit is NOT feasible at depth cap %s -- aborting stage"
                % (cap,))
        return
    # ---- knobs ----
    vic_cost = k.get("vic_cost", 3)
    op_mix = k.get("op_mix", {"small": 0.35, "coneinj": 0.45, "biginj": 0.20})
    ops, opw = list(op_mix.keys()), list(op_mix.values())
    hot_frac = k.get("hot_frac", 0.5)
    use_sa = k.get("accept", "sa") == "sa"
    sa_T0 = k.get("sa_T0", 1.2); sa_cool = k.get("sa_cool", 0.9997)
    sa_reheat = k.get("sa_reheat", 4000)
    peel_window = k.get("peel_window", 6)
    harvest_path = k.get("harvest_path")
    pop_glob = k.get("pop_glob")
    pop_period_s = k.get("pop_period_s", 60.0)
    biginj_lo = k.get("biginj_lo", 8); biginj_hi = k.get("biginj_hi", 16)
    cone_lo = k.get("cone_lo", 2); cone_hi = k.get("cone_hi", 4)
    # ---- family repulsion (wave-3 hunt-deeper; default OFF) ----
    repel = set()
    if k.get("repel_file"):
        try:
            repel = set(json.load(open(k["repel_file"])))
        except (OSError, ValueError):
            pass
    repel_pen = k.get("repel_pen", 2)
    repel_up_p = k.get("repel_up_p", 0.25)

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
    hot = []                    # multiset for scored sampling
    peel_seen = set()           # frozensets already peel-processed
    harvested = set()           # frozensets already written to harvest file
    pop_offsets = {}            # cross-pollination file offsets
    next_pop = pop_period_s

    def harvest(mset):
        if harvest_path is None:
            return
        fz = frozenset(mset)
        if fz in harvested or len(harvested) >= 300000:
            return
        harvested.add(fz)
        try:
            with open(harvest_path, "a") as f:
                f.write(json.dumps(sorted(mset)) + "\n")
        except OSError:
            pass

    def cross_pollinate():
        """Merge sibling workers' harvested plateau masks into the pool."""
        n_new = 0
        for path in glob.glob(pop_glob):
            if harvest_path and os.path.abspath(path) == os.path.abspath(harvest_path):
                continue
            try:
                off = pop_offsets.get(path, 0)
                with open(path) as f:
                    f.seek(off)
                    for line in f:
                        try:
                            ms = json.loads(line)
                        except ValueError:
                            continue
                        for m in ms:
                            if m and wt(m) > 1 and m not in accumulate:
                                accumulate.add(m); pool.append(m); n_new += 1
                    pop_offsets[path] = f.tell()
            except OSError:
                continue
        return n_new

    def _small_kk():
        r = rng.random()
        if r < 0.45:
            return 1
        if r < 0.75:
            return 2
        if r < 0.90:
            return 3
        return 4

    info_cache = {"key": None, "info": None}

    def get_info():
        key = hash(frozenset(Ucur))
        if info_cache["key"] != key:
            info_cache["key"] = key
            info_cache["info"] = dag_info(Ucur)
        return info_cache["info"]

    Ucur = _peel(list(start), rng, cap)
    Ubest = list(Ucur)
    ctx.improve(indexpairs_from_masks(Ubest, cap), set(Ubest))
    harvest(Ubest)
    t0 = time.time(); iters = 0
    Temp = sa_T0; last_record_it = 0
    n_peeled_gain = 0
    while (time_limit is None or time.time() - t0 < time_limit) and \
          (target is None or len(Ubest) > target):
        iters += 1
        nu = len(Ucur)
        nontarget = [m for m in Ucur if m not in TSET]
        if not nontarget:
            break

        # ---------------- destroy (operator mix) ----------------
        extra_cand = []
        if iters % 997 == 0:
            kk = min(k["kshake"] + rng.randrange(5), len(nontarget))
            victims = rng.sample(nontarget, kk)
        else:
            op = rng.choices(ops, weights=opw)[0]
            if op == "small":
                kk = min(_small_kk(), len(nontarget))
                victims = rng.sample(nontarget, kk)
            elif op == "uniform":
                kk = min(1 + rng.randrange(k["kmax"]), len(nontarget))
                victims = rng.sample(nontarget, kk)
            elif op == "coneinj":
                kk = min(cone_lo + rng.randrange(cone_hi - cone_lo + 1),
                         len(nontarget))
                victims = _cone_pick(nontarget, rng, get_info(), kk)
                kept0 = [m for m in Ucur if m not in set(victims)]
                extra_cand = _inject(victims, kept0, rng)
            else:  # biginj: big destroy + injection (peel-before-accept saves it)
                kk = min(biginj_lo + rng.randrange(biginj_hi - biginj_lo + 1),
                         len(nontarget))
                victims = rng.sample(nontarget, kk)
                kept0 = [m for m in Ucur if m not in set(victims)]
                extra_cand = _inject(victims, kept0, rng, per_victim=8)
        vset = set(victims)
        kept = [m for m in Ucur if m not in vset]; nkeep = len(kept)
        if nkeep == 0:
            continue

        # ---------------- rebuild candidates ----------------
        cand = list(kept)
        for _ in range(k["nsamp"][0] + rng.randrange(k["nsamp"][1])):
            if hot and rng.random() < hot_frac:
                cand.append(hot[rng.randrange(len(hot))])
            else:
                cand.append(pool[rng.randrange(len(pool))])
        for _ in range(k["nsamp"][0] + rng.randrange(k["nsamp"][1])):
            m = kept[rng.randrange(nkeep)] ^ kept[rng.randrange(nkeep)]
            if m:
                cand.append(m)
        cand.extend(extra_cand)
        cand.extend(victims)          # victim-repool: always feasible rebuild
        seen = set(); C2 = []
        for m in cand:
            if m not in seen and wt(m) > 1:
                seen.add(m); C2.append(m)
        avail = list(INPUTS) + C2
        dep, pos = relax(avail)
        keptset = set(kept)
        costc = [0] * len(avail)
        for i in range(32, len(avail)):
            m = avail[i]
            if m in keptset:
                costc[i] = 1
            elif m in vset:
                costc[i] = vic_cost
            else:
                costc[i] = 2
            if repel and m in repel and m not in keptset:
                costc[i] += repel_pen
        res = _extract(avail, dep, pos, costc, rng, cap)
        if res is None:
            continue
        r = len(res)

        # ---------------- peel-before-accept (near-miss rebuilds) ----------
        if r > nu and r <= nu + peel_window:
            fz = frozenset(res)
            if fz not in peel_seen:
                if len(peel_seen) < 200000:
                    peel_seen.add(fz)
                res2 = _peel(res, rng, cap)
                if len(res2) < r:
                    n_peeled_gain += 1
                    res = res2; r = len(res)

        # ---------------- acceptance ----------------
        d = r - nu
        if use_sa:
            accept = d <= 0 or rng.random() < math.exp(-d / max(Temp, 1e-6))
            Temp *= sa_cool
            if iters - last_record_it > sa_reheat:
                Temp = sa_T0; last_record_it = iters
        else:
            accept = (d <= 0) or (d <= k["up_slack"] and
                                  rng.random() < k["up_prob"])
        if accept and repel and d >= 0:
            # plateau/uphill moves must not drift back toward the known
            # families: reject overlap-increasing moves most of the time
            dov = len(repel.intersection(res)) - len(repel.intersection(Ucur))
            if dov > 0 and rng.random() > repel_up_p:
                accept = False
        if accept:
            resset = set(res)
            for m in res:
                if m not in accumulate:
                    accumulate.add(m); pool.append(m)
                if m not in keptset:          # reintroduced: score it hot
                    if len(hot) < 200000:
                        hot.append(m)
            Ucur = res
            if len(Ucur) <= len(Ubest):
                fz = frozenset(Ucur)
                if fz in peel_seen:
                    cand2 = list(Ucur)
                else:
                    if len(peel_seen) < 200000:
                        peel_seen.add(fz)
                    cand2 = _peel(Ucur, rng, cap)
                    Ucur = cand2
                if len(cand2) < len(Ubest):
                    Ubest = list(cand2)
                    last_record_it = iters
                    ctx.improve(indexpairs_from_masks(cand2, cap), set(cand2),
                                note="it=%d" % iters)
                    harvest(cand2)
                elif len(cand2) == len(Ubest):
                    harvest(cand2)
                    if ctx.improve(indexpairs_from_masks(cand2, cap), set(cand2),
                                   note="depth-tiebreak it=%d" % iters):
                        Ubest = list(cand2)
        if len(Ucur) > len(Ubest) + k["snapback"]:
            Ucur = list(Ubest)
        if pop_glob and time.time() - t0 >= next_pop:
            next_pop += pop_period_s
            n_new = cross_pollinate()
            if n_new:
                ctx.log("[lns] cross-pollinated %d masks (pool=%d)" %
                        (n_new, len(pool)))
        if iters % 20000 == 0:
            ctx.log("[lns] %.0fs iters=%d cur=%d best=%d pool=%d hot=%d "
                    "harv=%d peelgain=%d" %
                    (time.time() - t0, iters, len(Ucur), len(Ubest),
                     len(pool), len(hot), len(harvested), n_peeled_gain))
    ctx.iters = iters


# ==========================================================================
# ENGINE  "walk"  --  value-set remove-1 / remove-2-add-1 hub moves
# ==========================================================================
def _repair(S2, rng, tries, avail=None, forbid=()):
    """EXACT single-mask repair (repair-move agent: complete enumeration, no
    random guessing).  Let A = closure(S2) and stuck = (S2 | TSET) - A.  A
    mask w repairs S2 iff (1) w is a pair-sum of A and (2) the incremental
    closure of A|{w} over `stuck` reaches every stuck target.  Every valid w
    lies in C = {v ^ a : v in stuck, a in A}, so enumerating C ∩ P2 is
    complete.  When several repairs exist, pick the one minimizing the
    trimmed set size, tie-broken by low weight then reuse potential."""
    if avail is None:
        avail, _, _ = closure(S2)
    if TSET <= avail:
        return S2
    stuck = (set(S2) | TSET) - avail
    al = list(avail); na = len(al)
    P2 = set()                             # all pair-sums of A, O(1) membership
    for i in range(na):
        a = al[i]
        for b in al[i + 1:]:
            P2.add(a ^ b)
    cands = set()                          # C ∩ P2 (complete; stuck ∩ P2 = ∅)
    for v in stuck:
        for a in al:
            w = v ^ a
            if w in P2:
                cands.add(w)
    valid = []
    av = set(avail)                        # shared, rolled back per candidate
    for w in cands:
        if w in av or w in forbid:         # forbid = just-removed masks: re-
            continue                       # adding them is a no-op ping-pong
        added = [w]; av.add(w)
        rem = set(stuck); qi = 0
        while qi < len(added):
            x = added[qi]; qi += 1
            for v in list(rem):
                if (v ^ x) in av:
                    av.add(v); rem.discard(v); added.append(v)
        ok = not (rem & TSET)
        for x in added:
            av.discard(x)
        if ok:
            valid.append(w)
    if not valid:
        return None
    if len(valid) == 1:
        return set(S2) | {valid[0]}
    reuse = {w: sum(1 for p in al if (w ^ p) in avail) for w in valid}
    rng.shuffle(valid)
    valid.sort(key=lambda w: (wt(w), -reuse[w]))
    scored = []
    for w in valid[:4]:
        scored.append((len(trim_masks(set(S2) | {w})), w))
    tmin = min(s for s, _ in scored)
    return set(S2) | {rng.choice([w for s, w in scored if s == tmin])}


def _walk_gates(mask_set, cap):
    """Index-pair gates for a mask set (closure-kernel agent).  With cap=None
    any topological witness from the closure is valid and ~50x cheaper than
    the min-depth relax ordering; every candidate is still oracle-verified."""
    if cap is not None:
        return indexpairs_from_masks(mask_set, cap)
    avail, order, parents, remaining = _closure_core(set(mask_set))
    if remaining:
        raise RuntimeError("value-set not realizable")
    idx = {1 << i: i for i in range(32)}
    gates = []
    for m in order:
        a, b = parents[m]
        gates.append([idx[a], idx[b]])
        idx[m] = 32 + len(gates) - 1
    return gates


def engine_walk(start_masks, cap, target, time_limit, seeds, k, ctx):
    """MERGED walk: remove-1 / remove-2-add-1 with

      * incremental closure removal queries (_WalkState; closure-kernel, 21.9x)
      * improve() surfaced only on iterations that changed cur (closure-kernel)
      * EXACT complete _repair + forbid-just-removed (repair-move, ~7x mobility)
      * plateau harvesting of every distinct best-size set (knob-sweep)"""
    rng = random.Random(seeds[0] if seeds else 1)
    if start_masks is None:
        start_masks = core.naive_masks()
    if cap is not None and not feasible_at(start_masks, cap):
        ctx.log("[walk] start not feasible at depth cap %s -- aborting stage" % cap)
        return

    def ok_cap(mset):
        return cap is None or feasible_at(mset, cap)

    harvest_path = k.get("harvest_path")
    harvested = set()

    def harvest(mset):
        if harvest_path is None:
            return
        fz = frozenset(mset)
        if fz in harvested or len(harvested) >= 300000:
            return
        harvested.add(fz)
        try:
            with open(harvest_path, "a") as f:
                f.write(json.dumps(sorted(mset)) + "\n")
        except OSError:
            pass

    # ---- family repulsion (wave-3 hunt-deeper; default OFF) ----
    repel = set()
    if k.get("repel_file"):
        try:
            repel = set(json.load(open(k["repel_file"])))
        except (OSError, ValueError):
            pass
    repel_up_p = k.get("repel_up_p", 0.25)

    cur = trim_masks(start_masks)
    if not ok_cap(cur):
        ctx.log("[walk] trimmed start exceeds depth cap -- aborting"); return
    best = set(cur)
    ctx.improve(_walk_gates(best, cap), set(best))
    harvest(best)
    st = _WalkState(cur)

    def rep_ok(nxt):
        """Repulsion gate: shrinking moves always pass; plateau moves that
        increase overlap with the known families pass only with prob
        repel_up_p."""
        if not repel or len(nxt) < len(cur):
            return True
        dov = len(repel.intersection(nxt)) - len(repel.intersection(cur))
        return dov <= 0 or rng.random() < repel_up_p

    t0 = time.time(); iters = 0
    while (time_limit is None or time.time() - t0 < time_limit) and \
          (target is None or len(best) > target):
        iters += 1
        nont = [v for v in cur if v not in TSET]
        if len(nont) < 2:
            break
        moved = False
        if rng.random() < k["hub_move_p"]:                 # remove-2-add-1
            v1 = rng.choice(nont)
            if rng.random() < 0.5:
                cand = [u for u in nont if u != v1 and wt(u ^ v1) <= k["close_hamming"]]
                v2 = rng.choice(cand) if cand else rng.choice([u for u in nont if u != v1])
            else:
                v2 = rng.choice([u for u in nont if u != v1])
            S2 = cur - {v1, v2}
            ok, avail2, unreal = st.remove_query((v1, v2))
            if ok:
                nxt = trim_masks(S2)
                if ok_cap(nxt):
                    cur = nxt; moved = True
            else:
                fixed = _repair(S2, rng, k["repair_hub"], avail2, forbid=(v1, v2))
                if fixed is not None:
                    nxt = trim_masks(fixed)
                    if len(nxt) < len(cur) and ok_cap(nxt):
                        cur = nxt; moved = True
        else:                                              # remove-1
            v = rng.choice(nont); S2 = cur - {v}
            ok, avail2, unreal = st.remove_query((v,))
            if ok:
                nxt = trim_masks(S2)
                if ok_cap(nxt):
                    cur = nxt; moved = True
            else:
                fixed = _repair(S2, rng, k["repair_one"], avail2, forbid=(v,))
                if fixed is not None:
                    nxt = trim_masks(fixed)
                    slack = 1 if (rng.random() < k["plateau_slack_p"]
                                  and len(cur) < len(best) + 2) else 0
                    if len(nxt) <= len(cur) + slack and ok_cap(nxt) \
                            and rep_ok(nxt):
                        cur = nxt; moved = True
        if moved:
            st.reset(cur)
            # Pareto tie-break: surface fewer-gate OR equal-gate-shallower.
            if len(cur) < len(best):
                best = set(cur)
                ctx.improve(_walk_gates(best, cap), set(best), note="it=%d" % iters)
                harvest(best)
            elif len(cur) == len(best):
                harvest(cur)
                if ctx.improve(_walk_gates(cur, cap), set(cur),
                               note="depth-tiebreak it=%d" % iters):
                    best = set(cur)
        if iters % 20000 == 0:
            ctx.log("[walk] %.0fs iters=%d cur=%d best=%d harv=%d" %
                    (time.time() - t0, iters, len(cur), len(best),
                     len(harvested)))
    ctx.iters = iters


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
