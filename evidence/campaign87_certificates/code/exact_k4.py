#!/usr/bin/env python3
"""
exact_k4.py -- EXACT budget-3 window resynthesis (k=4 windows -> the 87 hunt).

Extends exact_window.py's first-unlock case analysis by one level.

THEOREM (completeness of solve3).  Let (avail, rem) be the root closure
fixpoint of the kept masks (invariant: no locked mask is a pair-sum of avail),
Pf = pairsums(avail).  If there is a set W of <= 3 new masks, each buildable
(XOR of two currently-available masks) at the moment it is added in some
order, interleaved with automatic cascade unlocks, that makes all targets
available, then solve3 returns some such W' with |W'| <= 3.

Proof.  All missing targets are locked, so any solution triggers at least one
unlock.  Fix a valid build order (w1[, w2[, w3]]) and let j in {1,2,3} be the
number of W-masks added strictly BEFORE the first unlock r.  When the i-th
mask is added, avail is still exactly root-avail + earlier w's (no unlock
yet), so buildability enumerates exhaustively:
    w1 in Pf;   w2 in Pf or w2 = w1^a;   w3 in Pf, w1^b, w2^b, or w1^w2
(a, b, c, a2 always range over root avail; r over locked masks).
The first unlock r must have the newest mask as a parent: r = w_j ^ z with
z in avail + {earlier w's} (r a pair-sum of older masks contradicts the
fixpoint invariant / the "no earlier unlock" assumption).

j=1:  r = w1 ^ a and w1 in Pf  =>  w1 in D0 (unlock-shaped & buildable).
      The remaining <=2 masks are a budget-2 problem on the child fixpoint,
      decided by the (already proven exact) solve2.               [Case A]

j=2:  by the budget-2 analysis (exact_window.py) the pair (w1, w2) can be
      assumed, after reordering scenarios covered by j=1 into Case A, of one
      of two shapes:
        1b: w2 = r ^ a not in Pf|avail, w1 = w2 ^ a2 in Pf
        2a: r = w1 ^ w2, w1, w2 in Pf (neither in D0)
      The third mask is a budget-1 problem on the grandchild fixpoint,
      decided by the exact solve1.                                [Case B]

j=3:  the cascade after w3 must finish ALL targets: a plain u==0 test, no
      recursion.  Exhausting (buildability of w2) x (buildability of w3) x
      (z in avail | {w1, w2}) and discarding
        - contradictions with the fixpoint invariant
          (e.g. w3 = w1^b & z = w1  =>  r = b in avail), and
        - scenarios that reorder into j<=2 (e.g. w3 in Pf & r = w3^a
          =>  w3 in D0, Case A;  w3 = w2^b & w2 in Pf & r = w3^a  =>
          pair (w2, w3) is shape 1b, Case B),
      exactly three irreducible triple shapes remain:
        T1: x, y in Pf; z = y ^ c not in Pf|avail; r = x ^ z
            (covers r = w3^w1 with w3 = w2^b;  r = w3^w2 with w3 in Pf,
             w2 = w1^a2;  and r = w3^w2 with w3 = w1^b, w2 in Pf)
        T2: x in Pf; y = x ^ a2 not in Pf|avail; z = y ^ b not in Pf|avail;
            r = z ^ a                                  (the 3-chain)
        T3: x, y in Pf; z = x ^ y not in Pf|avail; r = z ^ a
      Case C enumerates a superset of each shape and tests u==0.  [Case C]

Every remaining scenario is impossible or covered, so a None answer with no
deadline expiry is a machine-checked proof of irreducibility.        QED

(Enumerating supersets is always sound: any tested triple that reaches u==0
is a genuine solution regardless of which case suggested it.)
"""
import sys, os, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exact_window as xw


# --------------------------------------------------------------------------
# helpers: add a pair then exact budget-1; test a triple
# --------------------------------------------------------------------------
def _pair_then_one(st, x, y):
    """Add buildable masks x then y (cascading), then exact solve1.
    Returns solution list or None.  State fully restored."""
    saved_u = st.u_left
    n0 = len(st.news)
    added1, u1 = st.try_add(x)
    st.u_left = u1
    st.news.extend(added1)
    if y in st.avail:                       # cascade already produced y
        added2 = []
        u2 = u1
    else:
        added2, u2 = st.try_add(y)
        st.u_left = u2
        st.news.extend(added2)
    st.tests += 1
    res = [] if u2 == 0 else xw.solve1(st)
    del st.news[n0:]
    st.u_left = saved_u
    st.rollback(added2)
    st.rollback(added1)
    if res is not None:
        return [x, y] + res
    return None


def _try_triple(st, seq):
    """Add the (buildable, in this order) masks of seq; True iff u hits 0.
    State fully restored."""
    saved_u = st.u_left
    stack = []
    for w in seq:
        if w in st.avail:
            continue
        added, u = st.try_add(w)
        st.u_left = u
        stack.append(added)
        if u == 0:
            break
    st.tests += 1
    ok = st.u_left == 0
    for added in reversed(stack):
        st.rollback(added)
    st.u_left = saved_u
    return ok


# --------------------------------------------------------------------------
# EXACT budget-3
# --------------------------------------------------------------------------
ALL_CASES = ("A", "B1b", "B2a", "T1", "T2", "T3")


def solve3(st, stats=None, cases=None):
    """EXACT: return W (|W|<=3) completing all targets, or None.
    None is a proof of impossibility unless st.deadline expired.
    `cases` restricts which branches run (TESTING ONLY -- restricting cases
    forfeits the completeness guarantee)."""
    if cases is None:
        cases = ALL_CASES
    if st.u_left == 0:
        return []
    avail = st.avail
    deadline = st.deadline
    Pf = st.pfull()
    D0 = st.d0(Pf)

    def tag(name):
        if stats is not None:
            stats[name] = stats.get(name, 0) + 1

    # ---------------- Case A: w1 in D0, then exact budget-2 ----------------
    if "A" in cases:
        scored = []
        for w in D0:
            added, u2 = st.try_add(w)
            st.rollback(added)
            scored.append((u2, -len(added), w))
        scored.sort()
        for _, _, w1 in scored:
            added, u2 = st.try_add(w1)
            st.tests += 1
            if u2 == 0:
                st.rollback(added)
                tag("A")
                return [w1]
            saved_u = st.u_left
            st.u_left = u2
            st.news.extend(added)
            res = xw.solve2(st)
            del st.news[len(st.news) - len(added):]
            st.u_left = saved_u
            st.rollback(added)
            if res is not None:
                tag("A")
                return [w1] + res
            if deadline and time.time() > deadline:
                return None
    av_list = list(avail)

    # ---------------- Case B: first-unlock pair, then exact budget-1 -------
    # B-1b: w2 = r ^ a not buildable now; w1 = w2 ^ a2 in Pf
    if "B1b" in cases:
        seen = set()
        for r in st.rem:
            if r in avail:
                continue
            for a in av_list:
                y = r ^ a
                if y in avail or y in Pf:
                    continue
                for a2 in av_list:
                    x = y ^ a2
                    if x == y or x in avail or x not in Pf or x in D0:
                        continue
                    key = (x, y)
                    if key in seen:
                        continue
                    seen.add(key)
                    res = _pair_then_one(st, x, y)
                    if res is not None:
                        tag("B1b")
                        return res
            if deadline and time.time() > deadline:
                return None
    # B-2a: r = w1 ^ w2, both in Pf, neither in D0
    if "B2a" in cases:
        seen2 = set()
        for r in st.rem:
            if r in avail:
                continue
            for x in Pf:
                y = x ^ r
                if y not in Pf or x >= y or x in D0 or y in D0:
                    continue
                if x in avail or y in avail:
                    continue
                key = (x, y)
                if key in seen2:
                    continue
                seen2.add(key)
                res = _pair_then_one(st, x, y)
                if res is not None:
                    tag("B2a")
                    return res
            if deadline and time.time() > deadline:
                return None

    # ---------------- Case C: all three before the first unlock ------------
    if not ("T1" in cases or "T2" in cases or "T3" in cases):
        return None
    rem_locked = [r for r in st.rem if r not in avail]
    PfL = [p for p in Pf if p not in avail]
    # A1 = masks one buildable step beyond Pf (via one avail mask)
    A1 = set()
    for p in PfL:
        for c in av_list:
            A1.add(p ^ c)
    A1 -= Pf
    A1 -= avail
    A1.discard(0)

    # T2 (3-chain): x in Pf, y = x^a2, z = y^b, r = z^a  (y,z outside Pf|avail)
    if "T2" in cases:
        for r in rem_locked:
            for a in av_list:
                z = r ^ a
                if z in avail or z in Pf:
                    continue
                for b in av_list:
                    y = z ^ b
                    if y == z or y in avail or y in Pf or y not in A1:
                        continue
                    for c in av_list:
                        x = y ^ c
                        if x == y or x in avail or x not in Pf:
                            continue
                        if _try_triple(st, (x, y, z)):
                            tag("T2")
                            return [x, y, z]
            if deadline and time.time() > deadline:
                return None

    # T1: x, y in Pf, z = y^c, r = x^z  (z outside Pf|avail)
    if "T1" in cases:
        for r in rem_locked:
            for x in PfL:
                z = r ^ x
                if z not in A1:
                    continue
                for c in av_list:
                    y = z ^ c
                    if y == x or y in avail or y not in Pf:
                        continue
                    if _try_triple(st, (x, y, z)):
                        tag("T1")
                        return [x, y, z]
            if deadline and time.time() > deadline:
                return None

    # T3: x, y in Pf, z = x^y, r = z^a  (z outside Pf|avail)
    if "T3" in cases:
        Z3 = set()
        for r in rem_locked:
            for a in av_list:
                z = r ^ a
                if z and z not in avail and z not in Pf:
                    Z3.add(z)
        Pfset = Pf if isinstance(Pf, set) else set(Pf)
        for z in Z3:
            for x in PfL:
                y = z ^ x
                if x < y and y in Pfset and y not in avail:
                    if _try_triple(st, (x, y, z)):
                        tag("T3")
                        return [x, y, z]
            if deadline and time.time() > deadline:
                return None
    return None


# --------------------------------------------------------------------------
# window-level wrapper (mirrors xw.solve_window, but exact at budget 3)
# --------------------------------------------------------------------------
def solve_window3(full_set, window, time_cap=None, stats=None):
    kept = [m for m in full_set if m not in window]
    t0 = time.time()
    st = xw.WinState(kept)
    if time_cap:
        st.deadline = t0 + time_cap
    if st.u_left == 0:
        return {"status": "free", "W": [], "tests": 0, "rem": len(st.rem),
                "time": time.time() - t0}
    W = solve3(st, stats)
    el = time.time() - t0
    timed_out = st.deadline is not None and time.time() > st.deadline
    if W is not None:
        return {"status": "win", "W": W, "tests": st.tests,
                "rem": len(st.rem), "time": el}
    return {"status": "nosol" if timed_out else "irreducible",
            "W": None, "tests": st.tests, "rem": len(st.rem), "time": el}


# --------------------------------------------------------------------------
# independent complete brute (for validation on SMALL instances only):
# at every level try EVERY mask buildable from the current avail (= pfull).
# --------------------------------------------------------------------------
def brute(st, budget):
    if st.u_left == 0:
        return []
    if budget <= 0:
        return None
    Pf = st.pfull()
    for w in sorted(Pf):
        if w in st.avail or w == 0:
            continue
        saved_u = st.u_left
        n0 = len(st.news)
        added, u = st.try_add(w)
        st.u_left = u
        st.news.extend(added)
        res = brute(st, budget - 1)
        del st.news[n0:]
        st.u_left = saved_u
        st.rollback(added)
        if res is not None:
            return [w] + res
    return None


def brute_window(full_set, window, budget):
    kept = [m for m in full_set if m not in window]
    st = xw.WinState(kept)
    return brute(st, budget)
