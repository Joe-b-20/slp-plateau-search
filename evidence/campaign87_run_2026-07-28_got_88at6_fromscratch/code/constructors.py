#!/usr/bin/env python3
"""
constructors.py -- diverse FROM-SCRATCH roots for the 87-hunt cascades.

The campaign's certificates say the same thing four different ways: every
known 88 is locally rigid (k<=2 shell exactly empty on all of them, k<=3 on
the 13 canonical ones), and every hunt that starts near a known circuit ends
back inside one of the three known families.  So the from-scratch lane does
not try to be clever -- it tries to be STRUCTURALLY DIFFERENT.  Four
independent root constructors, each feeding an uncapped v2 reduction worker:

  naive    randomized balanced XOR trees per output with opportunistic
           subexpression reuse (mixcolumns_core.naive_circuit, randomized
           pairing order so every restart is a different root).  ~150 gates.
  anneal3  the depth-3 partition annealer (engines.engine_anneal3) -- not
           built here; the worker runs the engine directly.
  paar     Paar's greedy cancellation-free common-subexpression elimination:
           repeatedly contract the pair of signals that co-occurs in the most
           remaining output rows.  Classic, deterministic modulo tie-breaks;
           we randomize the ties.  ~110-130 gates.
  bp       Boyar-Peralta-style greedy: keep a distance-to-target vector over
           the current base, repeatedly add the XOR pair that minimizes the
           total remaining distance, breaking ties by BP's max-Euclidean-norm
           rule.  ~105-125 gates.

HONESTY NOTE on `bp`.  Real BP recomputes an exact distance
    delta(t, B) = (min #elements of B whose XOR is t) - 1
by recursive search; that is far too slow to run inside a candidate-pair loop
in Python.  Because B always contains the 32 unit vectors, the exact distance
is  min over subsets S of the NON-unit base of ( |S| + wt(t ^ XOR S) ) - 1,
and this module computes that minimum over a restricted subset family: only
elements that strictly reduce the residual weight by >= 2 are ever added.
That is an UPPER BOUND on the true delta (a step of a minimal representation
need not reduce weight), so `bp` is "BP-style greedy with a bounded weight-
descent distance", not BP.  It is used as a root generator, not as a claim.

LCB-BP: NOT IMPLEMENTED -- deliberately.  Sun-Yang-Li's Linear-Combinations
Boyar-Peralta (ePrint 2025/1493) is the fourth constructor the brief asked
about.  Everything this repo records about it is two lines in
../agents/lit-88/REPORT.md: "vote on pairs by frequency in linear combinations
of targets, avoiding BP's recursive distance recomputation", plus a conjecture
about picking pairs from the Support set.  The paper's actual voting weights,
which linear combinations are enumerated, and the tie-break rules are nowhere
in the repo (the PDF is archived but not transcribed), so an implementation
would be a guess wearing a published algorithm's name -- and a guess is worth
nothing here that a randomized greedy is not.

SUBSTITUTED, per the brief's fallback: `paar` (a genuinely different,
completely specified classical constructor -- cancellation-free CSE rather
than distance-driven cancellation) and the randomization inside `bp` (each
restart samples a different candidate-pair set, so the "randomized BP" root is
what actually runs).  Two structurally distinct extra roots instead of one
guessed one.
"""
import random

import mixcolumns_core as core

TARGETS = core.TARGETS
TSET = core.TARGET_SET
INPUTS = core.INPUTS
wt = core.wt


# ==========================================================================
# helpers
# ==========================================================================
def masks_from_gates(gates):
    """Value-set (non-input masks) of an index-pair circuit."""
    sig = [1 << i for i in range(32)]
    for a, b in gates:
        sig.append(sig[a] ^ sig[b])
    return set(sig[32:])


def _check(gates, name):
    r = core.verify(gates)
    if not r["ok"]:
        raise AssertionError("%s produced an INVALID circuit: %s" % (name, r))
    return r


# ==========================================================================
# naive -- randomized balanced trees (the v1 cold start, made diverse)
# ==========================================================================
def build_naive(rng):
    sig_index = {1 << i: i for i in range(32)}
    gates = []

    def combine(a, b):
        m = a ^ b
        if m not in sig_index:
            gates.append([sig_index[a], sig_index[b]])
            sig_index[m] = 31 + len(gates)
        return m

    order = list(TARGETS)
    rng.shuffle(order)
    for t in order:
        items = [1 << b for b in core.bits_of(t)]
        rng.shuffle(items)
        while len(items) > 1:
            nxt = []
            for k in range(0, len(items) - 1, 2):
                nxt.append(combine(items[k], items[k + 1]))
            if len(items) % 2 == 1:
                nxt.append(items[-1])
            rng.shuffle(nxt)
            items = nxt
    return gates


# ==========================================================================
# paar -- greedy cancellation-free CSE
# ==========================================================================
def build_paar(rng):
    """Signals start as the 32 inputs; each output row is the SET of signal
    indices that XOR to it.  Repeatedly replace the most frequently co-
    occurring index pair by a new signal.  Cancellation-free by construction,
    so every row shrinks monotonically and the loop always terminates."""
    sigmask = list(INPUTS)
    gates = []
    rows = [set(core.bits_of(t)) for t in TARGETS]

    while True:
        cnt = {}
        for r in rows:
            if len(r) < 2:
                continue
            idx = sorted(r)
            for i in range(len(idx)):
                for j in range(i + 1, len(idx)):
                    key = (idx[i], idx[j])
                    cnt[key] = cnt.get(key, 0) + 1
        if not cnt:
            break
        best = max(cnt.values())
        pairs = [p for p, c in cnt.items() if c == best]
        a, b = pairs[rng.randrange(len(pairs))]
        m = sigmask[a] ^ sigmask[b]
        gates.append([a, b])
        sigmask.append(m)
        new = len(sigmask) - 1
        for r in rows:
            if a in r and b in r:
                r.discard(a); r.discard(b); r.add(new)
    # rows of size 1 whose single signal is not literally the target cannot
    # happen (cancellation-free contraction preserves the XOR), so we are done.
    return gates


# ==========================================================================
# bp -- Boyar-Peralta-style greedy (bounded weight-descent distance)
# ==========================================================================
def _dist(t, helpers, best):
    """Upper bound on (min #base elements XOR-ing to t).  `helpers` is the
    list of non-unit base masks; only elements that cut the residual weight by
    at least 2 are tried, so the recursion depth is <= wt(t)//2."""
    if t == 0:
        return 0
    best = min(best, wt(t))
    if best <= 1:
        return best
    for h in helpers:
        r = t ^ h
        if wt(r) <= wt(t) - 2:
            v = 1 + _dist(r, helpers, best - 1)
            if v < best:
                best = v
                if best <= 1:
                    break
    return best


def _total_dist(unbuilt, helpers):
    ds = [_dist(t, helpers, wt(t)) for t in unbuilt]
    return sum(ds), sum(d * d for d in ds)


def build_bp(rng, samples=30):
    """Greedy: each step adds one XOR of two current base signals, chosen to
    minimize the summed distance of the still-unbuilt targets, tie-broken by
    the LARGEST sum of squared distances (BP's Euclidean-norm rule -- prefer a
    lopsided distance vector, it concentrates the remaining work)."""
    sigmask = list(INPUTS)
    index = {m: i for i, m in enumerate(sigmask)}
    gates = []
    helpers = []                       # non-unit base masks
    built = set(m for m in sigmask)
    unbuilt = [t for t in TARGETS if t not in built]

    guard = 0
    while unbuilt and guard < 400:
        guard += 1
        n = len(sigmask)
        cands = set()
        # (a) random pairs over the whole base -- diversity across restarts
        for _ in range(samples):
            i = rng.randrange(n); j = rng.randrange(n)
            if i != j:
                cands.add(sigmask[i] ^ sigmask[j])
        # (b) every pair among the most recent signals -- local refinement
        recent = sigmask[max(32, n - 10):]
        for i in range(len(recent)):
            for j in range(i + 1, len(recent)):
                cands.add(recent[i] ^ recent[j])
        # (c) one-step completions: residual of an unbuilt target vs a helper
        for t in unbuilt[:6]:
            for h in helpers[-12:]:
                r = t ^ h
                if 1 < wt(r) <= 3:
                    cands.add(r)
        cands = [m for m in cands if m and m not in index]
        if not cands:
            # base saturated for this sample; force a random new pair
            i = rng.randrange(n); j = rng.randrange(n)
            m = sigmask[i] ^ sigmask[j]
            if not m or m in index:
                continue
            cands = [m]

        base_sum, _ = _total_dist(unbuilt, helpers)
        best_key = None; best_m = None
        for m in cands:
            h2 = helpers + [m]
            s, sq = _total_dist(unbuilt, h2)
            key = (s, -sq)
            if best_key is None or key < best_key:
                best_key = key; best_m = m
        if best_m is None:
            break
        # realize best_m as a gate (it is a pair-XOR of existing signals)
        pa = pb = None
        for i in range(len(sigmask)):
            o = best_m ^ sigmask[i]
            if o in index and index[o] != i:
                pa, pb = i, index[o]
                break
        if pa is None:                 # candidate (c) may not be a pair-XOR
            continue
        gates.append([pa, pb])
        sigmask.append(best_m)
        index[best_m] = len(sigmask) - 1
        helpers.append(best_m)
        unbuilt = [t for t in unbuilt if t not in index]
        if best_key[0] >= base_sum and best_key[0] == 0:
            break

    # finish anything left with plain trees over the current base
    for t in unbuilt:
        rest = t
        acc = None
        parts = []
        for h in sorted(helpers, key=lambda x: -wt(x)):
            if wt(rest ^ h) <= wt(rest) - 2:
                parts.append(h); rest ^= h
        parts.extend(1 << b for b in core.bits_of(rest))
        for p in parts:
            if acc is None:
                acc = p; continue
            m = acc ^ p
            if m not in index:
                gates.append([index[acc], index[p]])
                sigmask.append(m); index[m] = len(sigmask) - 1
                helpers.append(m)
            acc = m
    return gates


# ==========================================================================
# dispatch
# ==========================================================================
BUILDERS = {"naive": build_naive, "paar": build_paar, "bp": build_bp}


def build(name, seed):
    """Return (masks, gates, report) for one from-scratch root.  Always
    oracle-verified before it is handed to a reduction worker."""
    rng = random.Random(seed)
    if name not in BUILDERS:
        raise SystemExit("unknown constructor %r (have %s)"
                         % (name, sorted(BUILDERS)))
    gates = BUILDERS[name](rng)
    rep = _check(gates, name)
    return masks_from_gates(gates), gates, rep


if __name__ == "__main__":
    import sys, time
    names = sys.argv[1:] or sorted(BUILDERS)
    for nm in names:
        for s in (1, 2, 3):
            t0 = time.time()
            masks, gates, rep = build(nm, s)
            print("%-6s seed=%d  %3d gates depth %2d  ok=%s  %.1fs"
                  % (nm, s, rep["gates"], rep["depth"], rep["ok"],
                     time.time() - t0))
