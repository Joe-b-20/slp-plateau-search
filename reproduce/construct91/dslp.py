#!/usr/bin/env python3
"""dslp.py — EXACT minimum-gate SLP oracle SUBJECT TO A DEPTH CAP,
              with LEVELLED INPUTS.

This is lane DEPTH's new instrument.  `atlas/slp_opt.py` decides the minimum
gate count of a linear SLP with no depth constraint whatsoever; this file
decides

    min { k : there is a k-gate SLP for the targets in which every target
              signal sits at DEPTH <= D, where an input signal p is deemed to
              already sit at depth in_levels[p] }

UNSAT at k under the cap is a machine-checked proof that no k-gate SLP of
depth <= D exists (under the normalisation rules below, which preserve at
least one optimum -- see `atlas/slp_opt.py`'s docstring for the proofs; every
one of them is depth-safe, argued in DEPTH-SAFETY below).

Levelled inputs matter.  A block's inputs are not free: currency values are
themselves built by gates and arrive at level 1, 2 or 3.  Asking the oracle
for a "depth-3 block program" while pretending its inputs are at level 0 is
the mistake that makes a block model depth-blind.  Here every input carries
its own arrival level and the cap is measured from the true circuit root.

ENCODING
--------
Base CNF (gate-position encoding, one-hot pair selection, N1/N2/N3 symmetry
breaking, L1 cone bound) is re-implemented here rather than imported, so that
"my depth solver with the cap switched off reproduces slp_opt" is a genuine
two-implementation control and not a tautology.

Depth is added with an ORDER encoding: for gate i and 1 <= l <= D-1,
`a[i][l]` means "level(gate i) <= l".  `a[i][0]` is the constant FALSE (every
gate is at level >= 1) and `a[i][D]` is the constant TRUE (the cap).  Clauses:

  monotone      a[i][l] -> a[i][l+1]
  input operand z_{i,(p,q)} with p an input of level L:
                    L+1 > D           ->  the pair is forbidden:  -z
                    otherwise         ->  -z, -a[i][l]   for 1 <= l <= min(L, D-1)
  gate operand  z_{i,(p,q)}, p = m+j:
                    -z, -a[i][l], a[j][l-1]     (1 <= l <= D-1, a[j][0] = FALSE)
                    -z, a[j][D-1]               (from a[i][D] = TRUE)

That is exactly "level(i) >= level(operand) + 1", so a satisfying assignment
exists iff the gate DAG has depth <= D measured from the levelled inputs.

DEPTH-SAFETY OF THE NORMALISATION RULES
---------------------------------------
(N1) duplicate-value elimination rewires later uses of gate g to an EARLIER
     signal s with the same value; level(s) <= level(g), so no level rises.
(N2) deleting an unused gate cannot raise any level.
(N3) swaps two ADJACENT INDEPENDENT gates; the DAG, and hence every level, is
     unchanged.
(L1) is a statement about a gate's position in the sequence, independent of
     levels, and is a logical consequence of the encoding.
So the lex-minimal normal form of a depth-<= D optimum is itself depth <= D.

REACHABILITY PRECHECK / IMPLIED CLAUSES
---------------------------------------
With rank r <= 16 the whole value space is enumerable.  `reach_levels`
computes, exactly, the set R_l of values producible at depth <= l from the
levelled inputs.  A target outside R_D makes the instance INFEASIBLE at any
gate count (reported as such, never as a gate bound).  Values outside R_l are
forbidden to gates asserted at level <= l -- implied, so removing no solution.
"""
from __future__ import annotations

import argparse, itertools, json, os, sys, time
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

try:
    from pysat.solvers import Solver as _PysatSolver
    HAVE_PYSAT = True
except Exception:
    HAVE_PYSAT = False

DEFAULT_SOLVER = "cadical153"
IMPLIED_BUDGET = 60_000


class Timeout(Exception):
    pass


# --------------------------------------------------------------- linear algebra
def echelon_basis(vectors: Sequence[int]) -> List[int]:
    basis: List[int] = []
    for v in vectors:
        x = v
        for b in basis:
            x = min(x, x ^ b)
        if x:
            basis.append(x)
            basis.sort(reverse=True)
    return basis


def coord_of(v: int, basis: List[int]) -> Optional[int]:
    x, c = v, 0
    for i, b in enumerate(basis):
        if x ^ b < x:
            x ^= b
            c |= 1 << i
    return c if x == 0 else None


def delta_array(r: int, signals: Sequence[int]) -> np.ndarray:
    """delta[v] = min number of signals XORing to v (subset-sum), inf if none."""
    N = 1 << r
    d = np.full(N, 1 << 20, dtype=np.int32)
    d[0] = 0
    for s in signals:
        nd = np.empty_like(d)
        idx = np.arange(N, dtype=np.int64) ^ s
        np.minimum(d, d[idx] + 1, out=nd)
        d = nd
    # repeat until fixed point (order matters for a single pass)
    for _ in range(2):
        for s in signals:
            idx = np.arange(N, dtype=np.int64) ^ s
            np.minimum(d, d[idx] + 1, out=d)
    return d


def lower_bound(d: np.ndarray, targets: Sequence[int]) -> int:
    ds = sorted((int(d[t]) - 1 for t in targets), reverse=True)
    best = 0
    for j, dj in enumerate(ds):
        best = max(best, dj + j)
    return max(best, 0)


def reach_levels(r: int, in_vals: Sequence[int], in_lvls: Sequence[int],
                 D: int) -> List[np.ndarray]:
    """R[l] : boolean array over 2^r, True where the value is producible at
    depth <= l from the levelled inputs.  Exact."""
    N = 1 << r
    R = []
    cur = np.zeros(N, dtype=bool)
    for l in range(D + 1):
        for v, lv in zip(in_vals, in_lvls):
            if lv <= l:
                cur[v] = True
        if l > 0:
            vals = np.nonzero(R[l - 1])[0].astype(np.int64)
            if len(vals):
                x = np.bitwise_xor.outer(vals, vals).ravel()
                cur[x] = True
        R.append(cur.copy())
    return R


# ------------------------------------------------------------------------ CNF
class CNF:
    __slots__ = ("clauses", "nv")

    def __init__(self):
        self.clauses: List[List[int]] = []
        self.nv = 0

    def new1(self) -> int:
        self.nv += 1
        return self.nv

    def new(self, count: int) -> List[int]:
        base = self.nv
        self.nv += count
        return list(range(base + 1, self.nv + 1))

    def add(self, cl):
        self.clauses.append(list(cl))


def _pairs_upto(s: int) -> List[Tuple[int, int]]:
    return [(p, q) for q in range(s) for p in range(q)]


def build_cnf(r: int, in_vals: List[int], tgt_vals: List[int], k: int,
              depth: Optional[int] = None, in_lvls: Optional[List[int]] = None,
              symmetry: bool = True, tgt_caps: Optional[List[int]] = None):
    m = len(in_vals)
    if in_lvls is None:
        in_lvls = [0] * m
    D = depth
    cnf = CNF()
    V = [cnf.new(r) for _ in range(k)]
    pairs = [_pairs_upto(m + i) for i in range(k)]
    Z = [cnf.new(len(pairs[i])) for i in range(k)]
    Spref: List[List[int]] = []

    # ---- level vars (order encoding) ---------------------------------------
    A: List[List[Optional[int]]] = []
    if D is not None:
        for i in range(k):
            row: List[Optional[int]] = [False]          # a[i][0] = FALSE
            for l in range(1, D):
                row.append(cnf.new1())
            row.append(True)                            # a[i][D] = TRUE
            A.append(row)
        for i in range(k):
            for l in range(1, D - 1):
                cnf.add([-A[i][l], A[i][l + 1]])

    def sig_bit(p: int, b: int):
        if p < m:
            return ("c", (in_vals[p] >> b) & 1)
        return ("v", V[p - m][b])

    for i in range(k):
        zi = Z[i]
        cnf.add(list(zi))
        P = len(zi)
        s = cnf.new(P)
        Spref.append(s)
        for j in range(P):
            cnf.add([-zi[j], s[j]])
            if j > 0:
                cnf.add([-s[j - 1], s[j]])
                cnf.add([-s[j - 1], -zi[j]])

        for j, (p, q) in enumerate(pairs[i]):
            z = zi[j]
            for b in range(r):
                vi = V[i][b]
                tp, ap = sig_bit(p, b)
                tq, aq = sig_bit(q, b)
                if tp == "c" and tq == "c":
                    c = ap ^ aq
                    cnf.add([-z, vi if c else -vi])
                elif tp == "c" or tq == "c":
                    c = ap if tp == "c" else aq
                    x = aq if tp == "c" else ap
                    if c == 0:
                        cnf.add([-z, -vi, x]); cnf.add([-z, vi, -x])
                    else:
                        cnf.add([-z, vi, x]); cnf.add([-z, -vi, -x])
                else:
                    x, y = ap, aq
                    cnf.add([-z, -vi, x, y]); cnf.add([-z, vi, -x, y])
                    cnf.add([-z, vi, x, -y]); cnf.add([-z, -vi, -x, -y])

            # ---- DEPTH: level(i) >= level(operand) + 1 ---------------------
            if D is not None:
                for o in (p, q):
                    if o < m:
                        L = in_lvls[o]
                        if L + 1 > D:
                            cnf.add([-z])
                            break
                        for l in range(1, min(L, D - 1) + 1):
                            cnf.add([-z, -A[i][l]])
                    else:
                        jj = o - m
                        # from a[i][D] = TRUE:  level(jj) <= D-1
                        if D - 1 == 0:
                            cnf.add([-z])
                            break
                        cnf.add([-z, A[jj][D - 1]])
                        for l in range(1, D):
                            prev = A[jj][l - 1]
                            if prev is False:
                                cnf.add([-z, -A[i][l]])
                            else:
                                cnf.add([-z, -A[i][l], prev])

        if symmetry:
            cnf.add(list(V[i]))
            for p in range(m):
                c = in_vals[p]
                cnf.add([V[i][b] if not ((c >> b) & 1) else -V[i][b] for b in range(r)])
            for jg in range(i):
                dif = cnf.new(r)
                for b in range(r):
                    cnf.add([-dif[b], V[i][b], V[jg][b]])
                    cnf.add([-dif[b], -V[i][b], -V[jg][b]])
                cnf.add(list(dif))

    if symmetry:
        for i in range(1, k):
            Pprev = len(Z[i - 1])
            u = cnf.new1()
            tail = [Z[i][j] for j in range(Pprev, len(Z[i]))]
            for lit in tail:
                cnf.add([-lit, u])
            cnf.add([-u] + tail)
            for j in range(Pprev):
                cl = [-Z[i][j], u]
                if j > 0:
                    cl.append(Spref[i - 1][j - 1])
                cnf.add(cl)

    # ---- (L1) implied cone bound -------------------------------------------
    d0 = delta_array(r, in_vals)
    if symmetry:
        budget = IMPLIED_BUDGET
        for i in range(k):
            bad = np.nonzero(d0 > i + 2)[0]
            if len(bad) > budget:
                break
            budget -= len(bad)
            for v in bad.tolist():
                cnf.add([-V[i][b] if ((v >> b) & 1) else V[i][b] for b in range(r)])

    # ---- implied depth-reachability clauses --------------------------------
    if D is not None:
        R = reach_levels(r, in_vals, in_lvls, D)
        budget = IMPLIED_BUDGET
        for l in range(1, D):
            bad = np.nonzero(~R[l])[0]
            if len(bad) * k > budget:
                continue
            budget -= len(bad) * k
            for i in range(k):
                ail = A[i][l]
                for v in bad.tolist():
                    cnf.add([-ail] + [-V[i][b] if ((v >> b) & 1) else V[i][b]
                                      for b in range(r)])

    # ---- target coverage ----------------------------------------------------
    W: List[List[int]] = []
    for t in tgt_vals:
        w = cnf.new(k)
        W.append(w)
        cnf.add(list(w))
        first = int(d0[t]) - 2
        for i in range(max(0, first)):
            cnf.add([-w[i]])
        for i in range(k):
            for b in range(r):
                cnf.add([-w[i], V[i][b] if ((t >> b) & 1) else -V[i][b]])
    # ---- PER-TARGET caps ----------------------------------------------------
    # W[ti][i] -> gate i sits at level <= cap(ti).  With cap = D this is
    # vacuous (a[i][D] is the constant TRUE), so the uniform case is unchanged.
    if D is not None and tgt_caps is not None:
        for ti, cap in enumerate(tgt_caps):
            if cap >= D:
                continue
            for i in range(k):
                lit = A[i][cap]
                if lit is False:
                    cnf.add([-W[ti][i]])
                else:
                    cnf.add([-W[ti][i], lit])

    if symmetry:
        for i in range(k):
            sidx = m + i
            lits: List[int] = [W[ti][i] for ti in range(len(tgt_vals))]
            for jg in range(i + 1, k):
                for j, (p, q) in enumerate(pairs[jg]):
                    if p == sidx or q == sidx:
                        lits.append(Z[jg][j])
            cnf.add(lits)

    return cnf, V, Z, A


def decode_model(model_set, V, Z, A, m: int, k: int, D):
    slp = []
    for i in range(k):
        pr = _pairs_upto(m + i)
        sel = None
        for j, z in enumerate(Z[i]):
            if z in model_set:
                sel = j
                break
        if sel is None:
            raise RuntimeError("no pair selected")
        slp.append(pr[sel])
    return slp


# ------------------------------------------------------------------- solving
def _worker(args):
    (r, in_vals, tgt_vals, k, D, in_lvls, cube, solver_name, symmetry, tcaps) = args
    m = len(in_vals)
    cnf, V, Z, A = build_cnf(r, in_vals, tgt_vals, k, D, in_lvls, symmetry, tcaps)
    boot = cnf.clauses if cube is None else cnf.clauses + [[Z[0][cube]]]
    with _PysatSolver(name=solver_name, bootstrap_with=boot) as S:
        if S.solve():
            return (k, "SAT", decode_model(set(S.get_model()), V, Z, A, m, k, D))
        return (k, "UNSAT", None)


def _run_pool(tasks, nproc, deadline):
    import multiprocessing as mp
    from multiprocessing import TimeoutError as MPTimeout
    pool = mp.Pool(processes=nproc)
    try:
        it = pool.imap_unordered(_worker, tasks)
        for _ in range(len(tasks)):
            if deadline is None:
                item = it.next()
            else:
                left = deadline - time.monotonic()
                if left <= 0:
                    raise Timeout()
                try:
                    item = it.next(timeout=left)
                except MPTimeout:
                    raise Timeout()
            if item[1] == "SAT":
                return True, item[2]
        return False, None
    finally:
        pool.terminate()
        pool.join()


PAR_FROM = 7


def pool_enabled():
    """lane LIB (fleet12): THE POOL IS OPT-IN.  See `decide`."""
    return os.environ.get("SLP_USE_POOL", "").strip().lower() in (
        "1", "true", "yes", "on")


def decide(r, in_vals, tgt_vals, k, D, in_lvls, ncores, solver_name,
           symmetry=True, deadline=None, tcaps=None):
    """SAT/UNSAT at exactly `k` gates.

    lane LIB (fleet12): THE SERIAL PATH IS THE DEFAULT.  `_run_pool`
    DEADLOCKS -- lane HALO hit it twice (`RESULT.md` §5.1: `STAT=Sl`, 21
    minutes wall against 3 seconds of CPU, `wchan = futex_wait_queue`, all
    four workers `Z`/defunct, the parent blocked forever on the result queue)
    -- and *the per-block timeout cannot rescue it*, because `_run_pool`
    enforces its deadline through `it.next(timeout=left)` and a parent blocked
    in `futex` is not counting.  Nothing in `engine.py`, `solver.py` or
    `generate.py` can then distinguish a hang from a slow solve.

    The serial path it deadlocks *instead of* is **1.2x to 31x faster** on
    these instances with byte-identical level logs (lane HALO §5.2: nine
    shared instances, all eight ladders byte-identical, block prices 10/10).
    The reason is structural: for `k >= PAR_FROM` the pooled path splits into
    `m(m-1)/2` cube tasks -- 325 solver calls for a 26-input block, *all* of
    which must be refuted to call one level UNSAT -- where the serial path
    solves one monolithic CNF with symmetry breaking.

    Soundness is unaffected: the number this function decides is SAT/UNSAT of
    a formula, which is a property of the formula and not of the search order.
    What the two paths can differ on is WHICH witness comes back, hence the
    collisions and the emitted depth (audit D11) -- never `min_gates`.

    The pool is NOT fixed here (that is a rabbit hole); it is routed around
    and kept reachable behind `SLP_USE_POOL=1` / `generate.py --pool`.

    Note the corollary this replaces: with the shipped default `--timeout
    1800`, `deadline` was never `None`, so EVERY solve in the repository's
    default configuration took the pooled, hang-prone path.

    One cost, stated: in the serial path the deadline is only tested BETWEEN
    k-levels (`solve_depth`'s loop head), so a single very slow level can
    overrun `--timeout` instead of self-bracketing into a `timeout` row.  The
    pooled path nominally checked mid-level -- except when it deadlocked, when
    it checked never."""
    m = len(in_vals)
    npairs0 = m * (m - 1) // 2
    if (not pool_enabled()) or ncores <= 1 or npairs0 < 2 or k < PAR_FROM:
        _, st, slp = _worker((r, in_vals, tgt_vals, k, D, in_lvls, None,
                              solver_name, symmetry, tcaps))
        return st == "SAT", slp
    if npairs0 < 2:
        tasks = [(r, in_vals, tgt_vals, k, D, in_lvls, None, solver_name,
                  symmetry, tcaps)]
        return _run_pool(tasks, 1, deadline)
    tasks = [(r, in_vals, tgt_vals, k, D, in_lvls, j, solver_name, symmetry, tcaps)
             for j in range(npairs0)]
    return _run_pool(tasks, min(max(ncores, 1), npairs0), deadline)


def solve_depth(dim, inputs, targets, depth=None, in_levels=None,
                max_gates=None, ncores=6, timeout=None, verbose=False,
                solver_name=DEFAULT_SOLVER, target_caps=None, lb_hint=None,
                on_level=None):
    # `on_level(k, "SAT"|"UNSAT", seconds)` is an OPTIONAL progress callback used
    # only by the --live display.  Default None => this function behaves exactly
    # as lane DEPTH shipped it; nothing below depends on the callback.
    """EXACT min gates subject to depth <= `depth` from levelled inputs."""
    t0 = time.monotonic()
    deadline = (t0 + timeout) if timeout else None
    inputs = list(inputs)
    if in_levels is None:
        in_levels = [0] * len(inputs)
    in_levels = list(in_levels)
    assert len(in_levels) == len(inputs)

    # dedupe inputs keeping the MINIMUM arrival level
    best: Dict[int, int] = {}
    for v, l in zip(inputs, in_levels):
        if v == 0:
            continue
        if v not in best or l < best[v]:
            best[v] = l
    raw_in = sorted(best)
    raw_lv = [best[v] for v in raw_in]

    basis = echelon_basis(raw_in)
    r = len(basis)
    in_vals = [coord_of(v, basis) for v in raw_in]

    out: Dict = {"min_gates": None, "slp": None, "depth_cap": depth,
                 "status": None, "r": r, "m": len(in_vals),
                 "in_vals": raw_in, "in_levels": raw_lv}

    if target_caps is None:
        target_caps = [depth] * len(list(targets))
    assert len(target_caps) == len(list(targets))
    if depth is not None:
        assert max(target_caps) <= depth, "a target cap exceeds the block cap"
    capof: Dict[int, int] = {}
    for t, cp in zip(targets, target_caps):
        if t == 0:
            continue
        c = coord_of(t, basis)
        if c is None:
            out.update(status="infeasible_span",
                       reason="target outside span(inputs)")
            return out
        if c not in capof or (cp is not None and cp < capof[c]):
            capof[c] = cp
    tset = []
    for c, cp in capof.items():
        if c in in_vals:
            lv = raw_lv[in_vals.index(c)]
            if cp is None or lv <= cp:
                continue
        tset.append(c)
    tgt_vals = sorted(set(tset))
    tgt_caps = [capof[c] for c in tgt_vals]
    out["n_targets"] = len(tgt_vals)
    out["target_caps"] = tgt_caps

    if not tgt_vals:
        out.update(min_gates=0, slp=[], status="exact", levels=[],
                   seconds=round(time.monotonic() - t0, 3))
        return out

    if depth is not None:
        R = reach_levels(r, in_vals, raw_lv, depth)
        miss = [t for t, cp in zip(tgt_vals, tgt_caps) if not R[cp][t]]
        if miss:
            out.update(status="infeasible_depth",
                       reason=f"{len(miss)} target(s) unreachable at depth {depth} "
                              f"from the levelled inputs, at ANY gate count",
                       seconds=round(time.monotonic() - t0, 3))
            return out

    d0 = delta_array(r, in_vals)
    lb = max(lower_bound(d0, tgt_vals), len(tgt_vals))
    if lb_hint is not None:
        # SOUND: the minimum under a depth cap is never below the minimum
        # without one, so an UNCAPPED optimum is a valid lower bound here.
        # It only skips k-levels that are provably UNSAT.
        lb = max(lb, int(lb_hint))
    out["lb_start"] = lb
    hi = max_gates if max_gates is not None else 64
    log = []
    try:
        for k in range(lb, hi + 1):
            if deadline is not None and time.monotonic() >= deadline:
                raise Timeout()
            tk = time.monotonic()
            ok, slp = decide(r, in_vals, tgt_vals, k, depth, raw_lv, ncores,
                             solver_name, deadline=deadline, tcaps=tgt_caps)
            dt = round(time.monotonic() - tk, 2)
            log.append({"k": k, "result": "SAT" if ok else "UNSAT", "seconds": dt})
            if on_level is not None:
                on_level(k, "SAT" if ok else "UNSAT", dt)
            if verbose:
                print(f"[dslp] D={depth} k={k}: {'SAT' if ok else 'UNSAT'} ({dt}s)",
                      file=sys.stderr, flush=True)
            if ok:
                lv = _replay_levels(raw_in, raw_lv, slp)
                out.update(min_gates=k, slp=[list(p) for p in slp],
                           status="exact", levels=lv, log=log,
                           realised_depth=max(lv[len(raw_in):]) if slp else 0,
                           seconds=round(time.monotonic() - t0, 3))
                return out
        # lane LIB (fleet12), audit defect D5: a LOOP BOUND IS NOT A PROOF OF
        # IMPOSSIBILITY.  If the caller set `max_gates`, exhausting it answers
        # exactly the question the caller asked ("is there a program with at
        # most max_gates gates?") and `capped_unsat` is a real negative.  If it
        # did NOT -- `hi` was this file's undefended default 64, which is
        # nowhere derived (a 16-dim block with n targets can need n*(r-1)
        # gates) -- then all that is known is a BRACKET: every k <= 64 is
        # UNSAT, the minimum is >= 65, and the question is UNDECIDED.
        out.update(status=("capped_unsat" if max_gates is not None
                           else "undecided_gate_cap"),
                   lower_bound_proven=hi + 1, log=log,
                   reason=(None if max_gates is not None else
                           f"the default gate ceiling hi={hi} was exhausted; "
                           f"every k <= {hi} is proved UNSAT, so the minimum is "
                           f">= {hi + 1}.  This is a BRACKET, not a proof of "
                           f"impossibility -- re-run with a larger max_gates."),
                   seconds=round(time.monotonic() - t0, 3))
        return out
    except Timeout:
        lbp = None
        for e in log:
            if e["result"] == "UNSAT":
                lbp = e["k"] + 1
        out.update(status="timeout", lower_bound_proven=lbp, log=log,
                   seconds=round(time.monotonic() - t0, 3))
        return out


def _replay_levels(raw_in, raw_lv, slp):
    lv = list(raw_lv)
    for a, b in slp:
        lv.append(max(lv[a], lv[b]) + 1)
    return lv


def verify_depth(inputs, in_levels, targets, slp, depth, target_caps=None):
    """independent replay: values correct, every target present, depth <= cap."""
    n_in = len(inputs)
    sig = list(inputs)
    lv = list(in_levels)
    for a, b in slp:
        if not (0 <= a < len(sig) and 0 <= b < len(sig)) or a == b:
            return False, "bad gate"
        sig.append(sig[a] ^ sig[b])
        lv.append(max(lv[a], lv[b]) + 1)
    have = {}
    for v, l in zip(sig, lv):
        if v not in have or l < have[v]:
            have[v] = l
    if target_caps is None:
        target_caps = [depth] * len(list(targets))
    for t, cp in zip(targets, target_caps):
        if t not in have:
            return False, f"target {t} missing"
        if cp is not None and have[t] > cp:
            return False, f"target {t} at level {have[t]} > cap {cp}"
    gl = lv[n_in:]
    if depth is not None and gl and max(gl) > depth:
        return False, f"a gate sits at level {max(gl)} > cap {depth}"
    return True, "ok"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("instance")
    ap.add_argument("--depth", type=int, default=None)
    ap.add_argument("--cores", type=int, default=6)
    ap.add_argument("--timeout", type=float, default=None)
    ap.add_argument("--max-gates", type=int, default=None)
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args(argv)
    inst = json.load(open(a.instance))
    res = solve_depth(inst["dim"], inst["inputs"], inst["targets"],
                      depth=a.depth if a.depth is not None else inst.get("depth"),
                      in_levels=inst.get("input_levels"),
                      target_caps=inst.get("target_caps"),
                      max_gates=a.max_gates if a.max_gates is not None
                      else inst.get("max_gates"),
                      ncores=a.cores, timeout=a.timeout, verbose=a.verbose)
    if res.get("slp") is not None:
        ok, why = verify_depth(res["in_vals"], res["in_levels"],
                               inst["targets"], res["slp"], res["depth_cap"],
                               inst.get("target_caps"))
        res["verified"] = ok
        res["verify_msg"] = why
    print(json.dumps(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
