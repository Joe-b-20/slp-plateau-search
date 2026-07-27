#!/usr/bin/env python3
"""
exact_window.py -- EXACT window resynthesis for AES MixColumns SLP mask sets.

Question answered exactly (for small budgets): given a verified 89-mask set S,
remove a window V of k non-target masks (K = S \ V); does there exist a set W
of <= k-1 new masks such that all 32 targets are XOR-reachable from
inputs + K + W?  One YES = an 88-gate circuit (trim can only shrink further).

Realizability model
    avail = closure(inputs + K): repeatedly add any kept mask expressible as
    the XOR of two available masks.  rem = K \ avail (locked kept masks).
    KEY INVARIANT: at the fixpoint no locked mask is a pair-sum of avail, so
    every future unlock must have a NEWLY added mask as one parent.  This makes
    cascade propagation frontier-driven and O(#new * |rem|) per test.

Exactness (proved by first-unlock case analysis on any valid build order):
  budget 1 (k=2): the added mask w causes a first unlock r = w ^ a with
    a in avail, hence w in {r ^ a} and w in P = pairsums(avail).  COMPLETE.
  budget 2 (k=3): for any working pair {x,y} some ordering falls in one of:
    (1a) first mask w1 is unlock-shaped AND buildable: w1 in D0 = {r^a} & P;
         then the second mask is found by the (complete) budget-1 search on
         the child state.
    (1b) no single mask unlocks anything; first unlock r1 = w2 ^ a with
         w2 NOT in P, so w2 = w1 ^ a' (built from w1), i.e.
         w1 = r1 ^ a ^ a' in P and w2 = r1 ^ a.
    (2a) no single mask unlocks anything; first unlock r1 = w1 ^ w2 with both
         w1, w2 in P  (meet-in-the-middle over P: w2 = w1 ^ r1).
    (the case w2 = w1 ^ a inside 2a forces r1 = a in avail: contradiction.)
    COMPLETE.
  budget >= 3 (k>=4): DFS whose first level(s) use unlock-anchored candidates
    D0 (optionally + random buildable "block" masks), with the LAST TWO levels
    handled by the complete budget-2 routine.  NOT a completeness proof for
    the whole space; results are flagged status="partial" unless a solution
    is found.

All searches also apply the trivial deficiency prune: if rem/U is empty the
window is already free gates (immediate win), and every candidate mask must be
buildable at the moment it is added.
"""
import sys, os, time, random, itertools, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mixcolumns_core as core

INPUTS = core.INPUTS
TSET = set(core.TARGET_SET)


# --------------------------------------------------------------------------
# closure + pair-sum machinery
# --------------------------------------------------------------------------
def fast_closure(masks):
    """avail = inputs + every mask of `masks` reachable as iterated pair-XORs.
    Returns (avail_set, locked_set)."""
    avail = set(INPUTS)
    rem = set(masks) - avail
    progress = True
    while progress and rem:
        progress = False
        for v in list(rem):
            for a in avail:
                if (v ^ a) in avail:
                    avail.add(v)
                    rem.discard(v)
                    progress = True
                    break
    return avail, rem


def pairsums(avail):
    """All non-zero XORs of two distinct avail masks, minus avail itself."""
    av = list(avail)
    P = set()
    n = len(av)
    for i in range(n):
        ai = av[i]
        for j in range(i + 1, n):
            P.add(ai ^ av[j])
    P -= avail
    return P


class WinState(object):
    """Mutable search state for one window. avail is modified in place with
    rollback; news tracks masks added since the root (for buildability)."""
    __slots__ = ("avail", "rem", "P", "news", "u_left", "tests", "deadline")

    def __init__(self, kept_masks):
        self.avail, locked = fast_closure(kept_masks)
        self.rem = sorted(locked)              # locked kept masks (fixed list)
        self.P = pairsums(self.avail)
        self.news = []
        self.u_left = sum(1 for t in TSET if t not in self.avail)
        self.tests = 0
        self.deadline = None

    # -- cascade add / rollback ------------------------------------------
    def try_add(self, w):
        """Add buildable mask w (not in avail) + cascade unlocks.
        Returns (added_list, new_u_left)."""
        avail = self.avail
        rem = self.rem
        added = [w]
        avail.add(w)
        u = self.u_left - (1 if w in TSET else 0)
        qi = 0
        while qi < len(added):
            n = added[qi]
            qi += 1
            for r in rem:
                if r not in avail and (r ^ n) in avail:
                    avail.add(r)
                    added.append(r)
                    if r in TSET:
                        u -= 1
        return added, u

    def rollback(self, added):
        for m in added:
            self.avail.remove(m)

    # -- buildability ----------------------------------------------------
    def pfull(self):
        """Pair-sum set of the CURRENT avail (root P extended by news and
        cascaded unlocks, which were not in the root avail)."""
        if not self.news:
            return self.P
        ext = set()
        for n in self.news:
            for a in self.avail:
                if a != n:
                    ext.add(n ^ a)
        return self.P | ext

    def d0(self, Pf):
        """Unlock-shaped AND currently-buildable candidates."""
        avail = self.avail
        D = set()
        for r in self.rem:
            if r in avail:
                continue
            D |= ({r ^ a for a in avail} & Pf)
        D -= avail
        D.discard(0)
        return D


# --------------------------------------------------------------------------
# exact budget-1 and budget-2 searches
# --------------------------------------------------------------------------
def solve1(st, Pf=None):
    """EXACT: return [w] if a single buildable mask completes all targets."""
    if st.u_left == 0:
        return []
    if Pf is None:
        Pf = st.pfull()
    for w in st.d0(Pf):
        added, u2 = st.try_add(w)
        st.tests += 1
        st.rollback(added)
        if u2 == 0:
            return [w]
    return None


def solve2(st):
    """EXACT: return W (|W|<=2) completing all targets, or None."""
    if st.u_left == 0:
        return []
    avail = st.avail
    Pf = st.pfull()
    D0 = st.d0(Pf)
    # ---- case 1a: w1 in D0, then exact budget-1 on the child ----
    for w1 in D0:
        added, u2 = st.try_add(w1)
        st.tests += 1
        if u2 == 0:
            st.rollback(added)
            return [w1]
        saved_u = st.u_left
        st.u_left = u2
        st.news.extend(added)
        res = solve1(st)
        del st.news[len(st.news) - len(added):]
        st.u_left = saved_u
        st.rollback(added)
        if res is not None:
            return [w1] + res
        if st.deadline and time.time() > st.deadline:
            return None
    av_list = list(avail)
    # ---- case 1b: w2 = r ^ a not buildable; w1 = w2 ^ a' in P ----
    seen_pairs = set()
    for r in st.rem:
        if r in avail:
            continue
        for a in av_list:
            w2 = r ^ a
            if w2 in avail or w2 in Pf:      # buildable-now w2 covered by 1a
                continue
            for a2 in av_list:
                w1 = w2 ^ a2
                if w1 == w2 or w1 in avail or w1 not in Pf or w1 in D0:
                    continue
                key = (w1, w2)
                if key in seen_pairs:
                    continue
                seen_pairs.add(key)
                added1, u1 = st.try_add(w1)
                added2, u2 = st.try_add(w2)      # buildable: w2 = w1 ^ a2
                st.tests += 1
                st.rollback(added2)
                st.rollback(added1)
                if u2 == 0:
                    return [w1, w2]
        if st.deadline and time.time() > st.deadline:
            return None
    # ---- case 2a: w1 ^ w2 = r, both in P (meet-in-the-middle) ----
    for r in st.rem:
        if r in avail:
            continue
        for w1 in Pf:
            w2 = w1 ^ r
            if w2 not in Pf or w1 >= w2 or w1 in D0 or w2 in D0:
                continue
            if w1 in avail or w2 in avail:
                continue
            added1, u1 = st.try_add(w1)
            added2, u2 = st.try_add(w2)
            st.tests += 1
            st.rollback(added2)
            st.rollback(added1)
            if u2 == 0:
                return [w1, w2]
    return None


# --------------------------------------------------------------------------
# budget >= 3: unlock-anchored DFS (partial), last two levels exact
# --------------------------------------------------------------------------
def solve_deep(st, budget, rng=None, block_samples=0, branch_cap=None):
    """Return W (|W| <= budget) or None. EXACT for budget<=2; for budget>=3
    the first budget-2 levels branch on D0 (+ random buildable blocks), so a
    None is NOT a proof."""
    if st.u_left == 0:
        return []
    if budget <= 0:
        return None
    if budget == 1:
        return solve1(st)
    if budget == 2:
        return solve2(st)
    Pf = st.pfull()
    cands = st.d0(Pf)
    if block_samples and rng is not None:
        Pl = list(Pf)
        for _ in range(block_samples):
            w = Pl[rng.randrange(len(Pl))]
            if w not in st.avail:
                cands.add(w)
    # rank candidates: most immediate unlock progress first
    scored = []
    for w in cands:
        added, u2 = st.try_add(w)
        st.rollback(added)
        scored.append((u2, -len(added), w))
    scored.sort()
    if branch_cap:
        scored = scored[:branch_cap]
    for _, _, w in scored:
        added, u2 = st.try_add(w)
        st.tests += 1
        if u2 == 0:
            st.rollback(added)
            return [w]
        saved_u = st.u_left
        st.u_left = u2
        st.news.extend(added)
        res = solve_deep(st, budget - 1, rng, block_samples, branch_cap)
        del st.news[len(st.news) - len(added):]
        st.u_left = saved_u
        st.rollback(added)
        if res is not None:
            return [w] + res
        if st.deadline and time.time() > st.deadline:
            return None
    return None


# --------------------------------------------------------------------------
# window-level driver
# --------------------------------------------------------------------------
def solve_window(full_set, window, budget, rng=None, block_samples=0,
                 branch_cap=None, time_cap=None):
    """Remove `window` from full_set; search for <=budget new masks restoring
    all targets.  Returns dict with status:
       'win'        -> solution W found (masks list)
       'free'       -> window already redundant (0 new masks needed!)
       'irreducible'-> exhaustively proven no solution (budget<=2 only)
       'nosol'      -> nothing found, search was partial
    """
    kept = [m for m in full_set if m not in window]
    t0 = time.time()
    st = WinState(kept)
    if time_cap:
        st.deadline = t0 + time_cap
    if st.u_left == 0:
        return {"status": "free", "W": [], "tests": 0, "rem": len(st.rem),
                "time": time.time() - t0}
    if budget >= 3 and rng is None:
        rng = random.Random(12345)
    W = solve_deep(st, budget, rng, block_samples, branch_cap)
    el = time.time() - t0
    timed_out = st.deadline is not None and time.time() > st.deadline
    if W is not None:
        return {"status": "win", "W": W, "tests": st.tests,
                "rem": len(st.rem), "time": el}
    exact = (budget <= 2) and not timed_out and not block_samples
    return {"status": "irreducible" if exact else "nosol",
            "W": None, "tests": st.tests, "rem": len(st.rem), "time": el}


# --------------------------------------------------------------------------
# brute-force reference (for validating solve2's completeness) -------------
# --------------------------------------------------------------------------
def solve2_brute(full_set, window):
    """Reference: w1 over ALL of P(avail), then exact solve1. Complete because
    WLOG the first-built mask is in P(avail) and the last is unlock-shaped."""
    kept = [m for m in full_set if m not in window]
    st = WinState(kept)
    if st.u_left == 0:
        return []
    r = solve1(st)
    if r is not None:
        return r
    for w1 in sorted(st.P):
        added, u2 = st.try_add(w1)
        saved_u = st.u_left
        st.u_left = u2
        st.news.extend(added)
        res = solve1(st) if u2 else []
        del st.news[len(st.news) - len(added):]
        st.u_left = saved_u
        st.rollback(added)
        if res is not None:
            return [w1] + res
    return None


def rebuild_circuit(full_set, window, W):
    """Turn (seed \\ window) + W into verified index-pair gates."""
    import engines
    masks = set(m for m in full_set if m not in window) | set(W)
    masks = engines.trim_masks(masks)
    gates = engines.indexpairs_from_masks(masks, None)
    rep = core.verify(gates)
    return gates, masks, rep
