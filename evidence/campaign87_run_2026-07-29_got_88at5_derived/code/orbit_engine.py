#!/usr/bin/env python3
"""rho^2-equivariant orbit-space machinery for the MixColumns 87 hunt.

sigma = rho^2 rotates input bytes by 2, i.e. bit b -> (b+16) mod 32, so on
32-bit masks sigma(m) is a 16-bit rotation.  MixColumns commutes with sigma
and TARGET_SET is sigma-closed (16 orbit pairs).

An orbit variable is a representative r = min(m, sigma(m)):
  - size-2 orbit  {r, sigma(r)}   costs 2 gates
  - fixed mask    sigma(r) == r   (byte pattern ABAB) costs 1 gate
A sigma-closed value-set S costs |S| = 2a + b.  87 = 43*2 + 1 lives in the
exactly-symmetric space; the mixed mode additionally allows a few unpaired
("loose") masks: cost = 2a + b + u.

Realizability is always decided on the FULL flattened mask set with the fast
early-stop worklist closure from closure-kernel (engines_closure) and every
improvement is emitted as an index-pair circuit and checked by the GF(2^8)
oracle (mixcolumns_core.verify) before being saved.
"""
import random, time

import mixcolumns_core as core
import engines_closure as EC        # fast worklist closure + _WalkState
import engines_relax as ER          # fast relax / indexpairs_from_masks

T = core.TARGETS
TSET = core.TARGET_SET
ISET = core.INPUT_SET
M32 = 0xFFFFFFFF


def sig(m):
    return ((m << 16) | (m >> 16)) & M32


def orep(m):
    s = sig(m)
    return m if m <= s else s


def osize(r):
    return 1 if sig(r) == r else 2


def oset(r):
    return {r, sig(r)}


TARGET_OREPS = frozenset(orep(t) for t in T)
assert len(TARGET_OREPS) == 16 and all(osize(r) == 2 for r in TARGET_OREPS)
# sanity: sigma really commutes with the map (input rotation == output rotation)
assert all(sig(t) in TSET for t in T)


def flatten(reps, loose=()):
    S = set()
    for r in reps:
        S.add(r); S.add(sig(r))
    S.update(loose)
    return S


def cost_of(reps, loose=()):
    return sum(osize(r) for r in reps) + len(loose)


def state_from_masks(masks):
    """Symmetrize a mask set: orbit closure. Returns set of orbit reps."""
    return {orep(m) for m in masks}


def closure_info(S):
    """(reachable, avail, order, parents) for full mask set S (targets must
    be members of S)."""
    avail, order, parents, _rem = EC._closure_core(set(S), stop_at_targets=True)
    return TSET <= avail, avail, order, parents


def trim_lift(S):
    """Trim S to what one witness derivation needs for the targets, then lift
    to orbit reps.  Returns rep set or None if targets unreachable."""
    ok, avail, order, parents = closure_info(S)
    if not ok:
        return None
    needed = set(); stack = list(TSET)
    while stack:
        v = stack.pop()
        if v in needed or v in ISET:
            continue
        needed.add(v)
        a, b = parents[v]
        stack.append(a); stack.append(b)
    return {orep(m) for m in needed}


def orbit_peel(reps, loose, rng):
    """Greedy removal of whole orbits (and loose masks) while the flattened
    set stays realizable.  Exact fixpoint per pass; order randomized."""
    reps = set(reps); loose = set(loose)
    improved = True
    while improved:
        improved = False
        items = [(0, r) for r in reps if r not in TARGET_OREPS] + \
                [(1, m) for m in loose]
        rng.shuffle(items)
        # heavier orbits first is a good default: try size-2 before fixed
        items.sort(key=lambda it: -(osize(it[1]) if it[0] == 0 else 1))
        F = flatten(reps, loose)
        for kind, x in items:
            D = oset(x) if kind == 0 else {x}
            F2 = F - D
            if EC.realizable(F2):
                if kind == 0:
                    reps.discard(x)
                else:
                    loose.discard(x)
                F = F2
                improved = True
    return reps, loose


def demote_pass(reps, loose, budget, rng):
    """Mixed mode: try dropping ONE HALF of a size-2 orbit (orbit -> loose),
    -1 gate each time, while realizable and loose budget holds."""
    reps = set(reps); loose = set(loose)
    F = flatten(reps, loose)
    order = [r for r in reps if osize(r) == 2 and r not in TARGET_OREPS]
    rng.shuffle(order)
    for r in order:
        if len(loose) >= budget:
            break
        for keep, drop in ((r, sig(r)), (sig(r), r)):
            F2 = F - {drop}
            if EC.realizable(F2):
                reps.discard(r); loose.add(keep)
                F = F2
                break
    return reps, loose


def repair_candidates(unre, avail2, rng, max_u=24, max_c=4000):
    """Complete candidate list for single-addition repair after a removal:
    any single mask w whose addition can restore realizability must satisfy
    w = u ^ a with u unrealized, a available, AND w derivable from avail2
    (w in pairwise sums of avail2) -- see repair-move REPORT (proof: every
    unrealized mask needs w first, so w must build from avail2 alone).
    Returns list of candidate masks (not reps; caller decides orbit/loose)."""
    U = list(unre)
    if len(U) > max_u:
        U = rng.sample(U, max_u)
    AV = list(avail2)
    pairs = set()
    for i, a in enumerate(AV):
        for b in AV[i + 1:]:
            pairs.add(a ^ b)
    cands = set()
    for u in U:
        for a in AV:
            w = u ^ a
            if w and w not in avail2 and w in pairs:
                cands.add(w)
                if len(cands) >= max_c:
                    return list(cands)
    return list(cands)


def verify_and_save(reps, loose, path, note, log):
    """Emit, oracle-verify, save. Returns (gates, depth) or None."""
    F = flatten(reps, loose)
    gates = ER.indexpairs_from_masks(F, None)
    r = core.verify(gates)
    if not r["ok"]:
        log("ORACLE REJECT (%s): %s" % (note, r))
        return None
    core.save(gates, path, extra={"depth": r["depth"], "note": note,
                                  "rho2_loose": sorted(loose)})
    log("saved %s: %d gates depth %d (%s)" % (path, r["gates"], r["depth"], note))
    return r["gates"], r["depth"]
