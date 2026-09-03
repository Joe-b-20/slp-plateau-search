#!/usr/bin/env python3
"""
slp_opt.py -- EXACT minimal-SLP oracle for small GF(2) linear straight-line programs.

Problem
-------
Given a GF(2) vector space of dimension n (n <= 12 in practice), a list of input
vectors and a list of target vectors (both given as ints, bitmask over the basis),
find the EXACT minimum number k of XOR gates such that there is a straight-line
program

    g_j = s_a XOR s_b        (a, b < len(inputs) + j,  a != b)

whose signal set  {inputs} u {gate outputs}  contains every target, and produce a
witness.  Cancellation is fully allowed: no restriction whatsoever is placed on
which pairs may be XORed.

CLI
---
    python3 slp_opt.py instance.json

with instance.json = {"dim": 8, "inputs": [...], "targets": [...], "max_gates": <opt>}

Output (stdout, JSON):
    {"min_gates": k, "slp": [[a,b], ...], ...}
signals numbered:  input i -> i,   gate j output -> len(inputs) + j.
If "max_gates" is given and no SLP with <= max_gates gates exists:
    {"min_gates": null, "lower_bound_proven": max_gates+1, ...}
and that negative claim is EXHAUSTIVELY proven (see below), never heuristic.

Engines (two independent exact methods; either alone is complete)
----------------------------------------------------------------
 * SAT   : for k = lb, lb+1, ... a CNF is built that is satisfiable iff a k-gate
           SLP exists.  Solved with CaDiCaL/Kissat via python-sat.  UNSAT at k is
           a machine-checked proof that no k-gate SLP exists.
 * DFS   : iterative-deepening DFS over gate sequences with an admissible lower
           bound, sound symmetry reduction and a transposition table.

Both engines are used to cross-validate each other in slp_opt_selftest.py.

Correctness arguments for every pruning rule used
-------------------------------------------------
Let S be the multiset of signal values available at some point and, for v in
span(S), let  delta(v) = min { |A| : A subset of S, XOR(A) = v }   (a subset-sum:
using a signal twice cancels, so subsets suffice).  Put dist(v) = delta(v) - 1.

(L1) CONE BOUND.  If a gate at position p (1-based, counting only the gates that
     come after the current state) has value w, then dist(w) <= p.
     Proof: let C be the cone (transitive fan-in) of that gate, |C| = c <= p
     gates.  The c gates have 2c input edges; every non-root gate of C feeds at
     least one gate of C, so at least c-1 of those edges come from inside C,
     hence at most c+1 edges come from S.  The gate value is the XOR of those
     S-signals taken with multiplicity mod 2, i.e. the XOR of a sub(multi)set of
     at most c+1 distinct elements of S.  So delta(w) <= c+1 <= p+1.            []

(L2) ADMISSIBLE LOWER BOUND.  Let t_1, ..., t_u be the targets not yet present in
     S, sorted so that d_1 >= d_2 >= ... >= d_u, d_i = dist(t_i) >= 1.  Then any
     completion needs at least
            LB = max_{1<=j<=u} ( d_j + j - 1 )
     further gates.
     Proof: distinct target values must be produced by distinct gates.  Fix j and
     look at the j targets with the largest distances; they occupy j distinct
     positions p_(1) < ... < p_(j) in the completion.  The target sitting at the
     earliest position p_(1) has distance >= d_j, and by (L1) its distance is
     <= p_(1); hence p_(1) >= d_j and p_(j) >= p_(1) + (j-1) >= d_j + j - 1.    []
     (j=1 gives the classic max-distance bound, j=u gives "one gate per missing
     target"; the max over j is never weaker than either.)

(N1) NO DUPLICATE VALUES.  Some optimal SLP has all its signal values pairwise
     distinct (and non-zero).  Proof: if gate g has the value of an earlier
     signal s, rewire every later use of g to s and delete g: still valid, one
     gate shorter -- so this cannot happen in an optimal SLP.                   []

(N2) EVERY GATE IS USED.  Some optimal SLP has every gate feeding a later gate or
     equal to a target: otherwise delete it.                                    []

(N3) ADJACENT-INDEPENDENCE ORDERING.  Order the pairs (a,b), a<b, by the key
     key(a,b) = b(b-1)/2 + a.  Some optimal SLP satisfies: for every i >= 1, if
     gate i does not read the output of gate i-1, then key(gate i-1) < key(gate i).
     Proof: if gate i does not read gate i-1 the two gates are independent and may
     be swapped (their own input indices are all < i-1 hence untouched; later
     gates are relabelled).  A swap that repairs a violation strictly decreases
     the word (key(gate 0), key(gate 1), ...) lexicographically -- the first
     changed position decreases -- so the lexicographically minimal member of the
     equivalence class of any optimal SLP satisfies the rule.                   []

(N1)-(N3) preserve at least one OPTIMAL solution but may destroy longer ones.
That is harmless because both engines search k upwards from lb and stop at the
first feasible k: for k < opt the restricted problem is UNSAT because the
unrestricted one already is, and for k = opt a solution survives.  The engines
NEVER use an inadmissible rule such as "a new gate must decrease some target's
distance" (that rule is false in the presence of cancellation, which is exactly
the phenomenon this oracle exists to study).

Caveat: 0 as a target
---------------------
A target equal to 0 is refused unless 0 is already an input value, because
producing 0 requires XORing two *distinct signals holding equal values*, whose
cost depends on a modelling convention (is "a XOR a" a legal gate?).  Rather than
guess, the oracle raises an error.

Written for this project, 2026-08-16.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import random
import sys
import time
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

try:
    from pysat.solvers import Solver as _PysatSolver
    HAVE_PYSAT = True
except Exception:                                            # pragma: no cover
    HAVE_PYSAT = False

INF = 63          # "unreachable" marker for the delta array (fits in int8)
DEFAULT_SOLVER = "cadical195"


# ----------------------------------------------------------------------------
# GF(2) linear algebra: coordinates relative to a basis of span(inputs)
# ----------------------------------------------------------------------------

def echelon_basis(vectors: Sequence[int]) -> List[int]:
    """Row-echelon basis (leading bits distinct, sorted descending) of the span."""
    basis: List[int] = []
    for v in vectors:
        cur = v
        for b in basis:
            hb = b.bit_length() - 1
            if (cur >> hb) & 1:
                cur ^= b
        if cur:
            basis.append(cur)
            basis.sort(key=lambda x: -x.bit_length())
    return basis


def coord_of(v: int, basis: List[int]) -> Optional[int]:
    """Coordinate bitmask of v w.r.t. `basis`, or None if v is not in the span."""
    cur, mask = v, 0
    for j, b in enumerate(basis):
        hb = b.bit_length() - 1
        if (cur >> hb) & 1:
            cur ^= b
            mask |= 1 << j
    return None if cur else mask


def value_of(mask: int, basis: List[int]) -> int:
    v = 0
    j = 0
    while mask:
        if mask & 1:
            v ^= basis[j]
        mask >>= 1
        j += 1
    return v


# ----------------------------------------------------------------------------
# delta / distance arrays
# ----------------------------------------------------------------------------

def delta_array(r: int, signals: Sequence[int]) -> np.ndarray:
    """delta[v] = min number of elements of `signals` XORing to v (INF if none)."""
    n = 1 << r
    d = np.full(n, INF, dtype=np.int8)
    d[0] = 0
    ar = np.arange(n, dtype=np.int64)
    for s in signals:
        if s == 0:
            continue
        d = np.minimum(d, np.minimum(d[ar ^ s].astype(np.int16) + 1, INF).astype(np.int8))
    return d


def delta_add(d: np.ndarray, g: int, ar: np.ndarray) -> np.ndarray:
    """Exact incremental update of the delta array when a signal g is added."""
    return np.minimum(d, np.minimum(d[ar ^ g].astype(np.int16) + 1, INF).astype(np.int8))


def lower_bound(d: np.ndarray, targets: Sequence[int]) -> int:
    """Admissible lower bound (L2) on the number of further gates."""
    ds = sorted((int(d[t]) - 1 for t in targets if int(d[t]) > 1), reverse=True)
    lb = 0
    for j, dj in enumerate(ds, start=1):
        v = dj + j - 1
        if v > lb:
            lb = v
    return lb


# ----------------------------------------------------------------------------
# Instance normalisation
# ----------------------------------------------------------------------------

class Instance:
    """Normalised instance: internal coordinates, deduplicated signals."""

    def __init__(self, dim: int, inputs: Sequence[int], targets: Sequence[int]):
        self.dim = dim
        self.inputs = list(inputs)
        self.targets = list(targets)
        mask = (1 << dim) - 1
        for v in list(inputs) + list(targets):
            if v < 0 or (v & ~mask):
                raise ValueError(f"vector {v} does not fit in dim={dim}")

        self.basis = echelon_basis(self.inputs)
        self.r = len(self.basis)

        # internal inputs: distinct non-zero values, first original index kept
        self.in_vals: List[int] = []
        self.in_orig: List[int] = []
        seen: Dict[int, int] = {}
        for i, v in enumerate(self.inputs):
            if v == 0:
                continue                       # a zero signal is never useful
            c = coord_of(v, self.basis)
            if c in seen:
                continue
            seen[c] = i
            self.in_vals.append(c)
            self.in_orig.append(i)
        self.m = len(self.in_vals)
        in_set = set(self.in_vals)

        # targets
        self.infeasible = False
        self.zero_target = False
        tset = []
        for t in self.targets:
            if t == 0:
                if 0 in self.inputs:
                    continue                   # already available as a signal
                self.zero_target = True
                continue
            c = coord_of(t, self.basis)
            if c is None:
                self.infeasible = True         # target outside span(inputs)
                continue
            if c in in_set:
                continue                       # already realised by an input
            tset.append(c)
        # deduplicate, keep deterministic order
        self.tgt_vals = sorted(set(tset))

    def describe(self) -> Dict:
        return {
            "dim": self.dim,
            "rank_of_inputs": self.r,
            "distinct_nonzero_inputs": self.m,
            "unrealised_distinct_targets": len(self.tgt_vals),
        }


# ----------------------------------------------------------------------------
# Witness handling: internal SLP -> original numbering, and verification
# ----------------------------------------------------------------------------

def internal_to_original(inst: Instance, slp: List[Tuple[int, int]]) -> List[List[int]]:
    """Map an internal SLP (indices over deduped inputs) to original numbering."""
    n_in = len(inst.inputs)
    out = []
    for (a, b) in slp:
        aa = inst.in_orig[a] if a < inst.m else n_in + (a - inst.m)
        bb = inst.in_orig[b] if b < inst.m else n_in + (b - inst.m)
        out.append([aa, bb])
    return out


def verify_slp(inputs: Sequence[int], targets: Sequence[int],
               slp: Sequence[Sequence[int]]) -> Tuple[bool, str]:
    """Replay an SLP in the ORIGINAL space and check every target is realised."""
    sig = list(inputs)
    for j, gate in enumerate(slp):
        if len(gate) != 2:
            return False, f"gate {j} is not a pair"
        a, b = gate
        lim = len(sig)
        if not (0 <= a < lim and 0 <= b < lim):
            return False, f"gate {j} references a signal that does not exist yet"
        if a == b:
            return False, f"gate {j} XORs a signal with itself"
        sig.append(sig[a] ^ sig[b])
    have = set(sig)
    for t in targets:
        if t not in have:
            return False, f"target {t} is not computed"
    return True, "ok"


# ----------------------------------------------------------------------------
# Greedy upper bound (Boyar-Peralta style, randomised restarts)
# ----------------------------------------------------------------------------

def greedy_slp(r: int, in_vals: List[int], tgt_vals: List[int],
               rng: random.Random, ar: np.ndarray) -> List[Tuple[int, int]]:
    sig = list(in_vals)
    d = delta_array(r, sig)
    remaining = [t for t in tgt_vals if int(d[t]) > 1]
    slp: List[Tuple[int, int]] = []
    while remaining:
        best = None
        best_key = None
        cand = []
        for q in range(len(sig)):
            sq = sig[q]
            for p in range(q):
                g = sq ^ sig[p]
                if g == 0:
                    continue
                red = 0
                sq2 = 0
                for t in remaining:
                    old = int(d[t])
                    new = min(old, int(d[t ^ g]) + 1)
                    red += old - new
                    sq2 += (new - 1) ** 2
                cand.append((red, -sq2, p, q, g))
        cand.sort(key=lambda c: (-c[0], c[1]))
        top = [c for c in cand if (c[0], c[1]) == (cand[0][0], cand[0][1])]
        red, _, p, q, g = top[rng.randrange(len(top))]
        if red <= 0:
            # cannot happen: a min-representation of any unrealised target always
            # supplies a reducing pair.  Guard anyway.
            raise RuntimeError("greedy stalled")
        slp.append((p, q))
        sig.append(g)
        d = delta_add(d, g, ar)
        remaining = [t for t in remaining if int(d[t]) > 1]
    return slp


def greedy_upper_bound(inst: Instance, restarts: int = 40,
                       seed: int = 12345) -> Tuple[int, List[Tuple[int, int]]]:
    if not inst.tgt_vals:
        return 0, []
    ar = np.arange(1 << inst.r, dtype=np.int64)
    rng = random.Random(seed)
    best: Optional[List[Tuple[int, int]]] = None
    for _ in range(max(1, restarts)):
        s = greedy_slp(inst.r, inst.in_vals, inst.tgt_vals, rng, ar)
        if best is None or len(s) < len(best):
            best = s
    return len(best), best


# ----------------------------------------------------------------------------
# Engine 1: SAT
# ----------------------------------------------------------------------------

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

    def add(self, cl: List[int]):
        self.clauses.append(cl)


def _pairs_upto(s: int) -> List[Tuple[int, int]]:
    """All pairs (p,q), p<q<s, enumerated in key order key(p,q)=q(q-1)/2+p."""
    return [(p, q) for q in range(s) for p in range(q)]


def build_cnf(r: int, in_vals: List[int], tgt_vals: List[int], k: int,
              symmetry: bool = True):
    """CNF that is SAT iff a k-gate SLP exists (under (N1)-(N3) when symmetry).

    Returns (cnf, V, Z) with V[i][b] the value bit vars of gate i and Z[i][j] the
    one-hot pair-selection vars of gate i (j indexes _pairs_upto(m+i)).
    """
    m = len(in_vals)
    cnf = CNF()

    V = [cnf.new(r) for _ in range(k)]
    pairs = [_pairs_upto(m + i) for i in range(k)]
    Z = [cnf.new(len(pairs[i])) for i in range(k)]
    Spref: List[List[int]] = []          # sequential-AMO prefix vars

    def sig_bit(p: int, b: int):
        """('c', 0/1) for an input signal, ('v', var) for a gate signal."""
        if p < m:
            return ("c", (in_vals[p] >> b) & 1)
        return ("v", V[p - m][b])

    for i in range(k):
        zi = Z[i]
        # ---- exactly one pair, sequential encoding (gives prefix vars) -------
        cnf.add(list(zi))                                    # at least one
        P = len(zi)
        s = cnf.new(P)
        Spref.append(s)
        for j in range(P):
            cnf.add([-zi[j], s[j]])
            if j > 0:
                cnf.add([-s[j - 1], s[j]])
                cnf.add([-s[j - 1], -zi[j]])

        # ---- value definition ----------------------------------------------
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
                    if c == 0:                                # vi <-> x
                        cnf.add([-z, -vi, x])
                        cnf.add([-z, vi, -x])
                    else:                                     # vi <-> not x
                        cnf.add([-z, vi, x])
                        cnf.add([-z, -vi, -x])
                else:                                         # vi = x xor y
                    x, y = ap, aq
                    cnf.add([-z, -vi, x, y])
                    cnf.add([-z, vi, -x, y])
                    cnf.add([-z, vi, x, -y])
                    cnf.add([-z, -vi, -x, -y])

        if symmetry:
            # ---- (N1) value distinct from every earlier signal, and non-zero -
            cnf.add(list(V[i]))                               # value != 0
            for p in range(m):
                c = in_vals[p]
                cnf.add([V[i][b] if not ((c >> b) & 1) else -V[i][b] for b in range(r)])
            for jgate in range(i):
                dif = cnf.new(r)
                for b in range(r):
                    cnf.add([-dif[b], V[i][b], V[jgate][b]])
                    cnf.add([-dif[b], -V[i][b], -V[jgate][b]])
                cnf.add(list(dif))

    # ---- (N3) adjacent-independence ordering --------------------------------
    uses = [0] * k
    if symmetry:
        for i in range(1, k):
            Pprev = len(Z[i - 1])
            u = cnf.new1()
            uses[i] = u
            tail = [Z[i][j] for j in range(Pprev, len(Z[i]))]
            for lit in tail:
                cnf.add([-lit, u])
            cnf.add([-u] + tail)
            for j in range(Pprev):
                cl = [-Z[i][j], u]
                if j > 0:
                    cl.append(Spref[i - 1][j - 1])
                cnf.add(cl)

    # ---- implied cone bound (L1): gate i can only hold values v with ---------
    # delta(v) <= i+2, delta measured over the INPUTS.  This is a logical
    # consequence of the encoding (see the (L1) proof in the module docstring),
    # not a normalisation, so it removes no solutions whatsoever; it is added
    # only because unit-propagating it is far cheaper than rediscovering it.
    if symmetry:
        d0 = delta_array(r, in_vals)
        budget = IMPLIED_CLAUSE_BUDGET
        for i in range(k):
            cap = i + 2
            bad = np.nonzero(d0 > cap)[0]
            if len(bad) > budget:
                break        # purely optional clauses: skipping keeps the
                             # encoding faithful, it only prunes less
            budget -= len(bad)
            for v in bad.tolist():
                cnf.add([-V[i][b] if ((v >> b) & 1) else V[i][b]
                         for b in range(r)])

    # ---- target coverage -----------------------------------------------------
    # W[ti][i]  ->  gate i carries target ti.  One direction suffices: the "at
    # least one" clause forces a real witness, and any real solution can set the
    # W vars accordingly, so the encoding is faithful in both directions.
    W: List[List[int]] = []
    d0t = delta_array(r, in_vals) if symmetry else None
    for t in tgt_vals:
        w = cnf.new(k)
        W.append(w)
        cnf.add(list(w))
        if d0t is not None:
            # (L1) again: a target at distance d cannot sit before position d
            first = int(d0t[t]) - 2
            for i in range(max(0, first)):
                cnf.add([-w[i]])
        for i in range(k):
            for b in range(r):
                cnf.add([-w[i], V[i][b] if ((t >> b) & 1) else -V[i][b]])

    # ---- (N2) every gate feeds a later gate or carries a target -------------
    if symmetry:
        for i in range(k):
            sidx = m + i
            lits: List[int] = [W[ti][i] for ti in range(len(tgt_vals))]
            for jgate in range(i + 1, k):
                for j, (p, q) in enumerate(pairs[jgate]):
                    if p == sidx or q == sidx:
                        lits.append(Z[jgate][j])
            cnf.add(lits)

    return cnf, V, Z


def decode_model(model_set, V, Z, m: int, k: int) -> List[Tuple[int, int]]:
    slp = []
    for i in range(k):
        pairs = _pairs_upto(m + i)
        sel = None
        for j, z in enumerate(Z[i]):
            if z in model_set:
                sel = j
                break
        if sel is None:
            raise RuntimeError("model has no pair selected for a gate")
        slp.append(pairs[sel])
    return slp


# solvers that cannot take assumptions: cubes are injected as unit clauses
_NO_ASSUMPTIONS = ("kissat",)


def _sat_worker(args):
    """Solve one (k, chunk-of-cubes) task.  Returns (k, status, slp|None).

    No wall-clock handling lives here on purpose.  pysat's `interrupt()` is a
    no-op for CaDiCaL (measured: a 5s interrupt left it still solving at 120s),
    so an in-process timer cannot be trusted to stop a solve.  Deadlines are
    therefore enforced one level up by terminating the worker PROCESS, which
    works whatever the backend does -- see sat_decide/_run_pool.
    """
    (r, in_vals, tgt_vals, k, cube_idx, solver_name, symmetry) = args
    m = len(in_vals)
    cnf, V, Z = build_cnf(r, in_vals, tgt_vals, k, symmetry=symmetry)
    no_assump = solver_name.lower().startswith(_NO_ASSUMPTIONS)

    def _decode(S):
        return decode_model(set(S.get_model()), V, Z, m, k)

    if cube_idx is None:
        with _PysatSolver(name=solver_name, bootstrap_with=cnf.clauses) as S:
            return (k, "SAT", _decode(S)) if S.solve() else (k, "UNSAT", None)

    if no_assump:
        for j in cube_idx:
            with _PysatSolver(name=solver_name,
                              bootstrap_with=cnf.clauses + [[Z[0][j]]]) as S:
                if S.solve():
                    return (k, "SAT", _decode(S))
        return (k, "UNSAT", None)

    with _PysatSolver(name=solver_name, bootstrap_with=cnf.clauses) as S:
        for j in cube_idx:
            if S.solve(assumptions=[Z[0][j]]):
                return (k, "SAT", _decode(S))
        return (k, "UNSAT", None)


PAR_FROM_SAT = 7      # below this k a single process is faster than forking
PAR_FROM_DFS = 5
# Cap on the optional implied cone-bound clauses (they are a speed device only;
# dropping them never changes an answer, and at dim 16 they would dominate).
IMPLIED_CLAUSE_BUDGET = 60_000


class Timeout(Exception):
    """Raised when a wall-clock deadline expires.  No claim is ever made on the
    strength of an interrupted search."""


def _can_fork() -> bool:
    """False inside a daemonic multiprocessing worker, which may not have
    children.  Callers must not try to build a Pool in that case."""
    try:
        import multiprocessing as mp
        return not mp.current_process().daemon
    except Exception:
        return True


def sat_decide(inst: Instance, k: int, ncores: int, solver_name: str,
               symmetry: bool = True, deadline: Optional[float] = None):
    """Decide 'is there a k-gate SLP?'.  Returns (True, slp) or (False, None).

    Note: with symmetry=True this decides 'is there a k-gate SLP in normal form
    (N1)-(N3)?', which coincides with 'is there an SLP with <= k gates?' only at
    k = the optimum.  Always call it through solve_sat, which scans k upward.
    """
    npairs0 = inst.m * (inst.m - 1) // 2
    # The in-process shortcut is only safe when there is no deadline to honour:
    # a solve running in THIS process cannot be stopped (CaDiCaL ignores
    # interrupt()).  With a deadline we always go through the pool, even on one
    # core, so that the deadline can be enforced by killing the worker -- unless
    # we are ourselves inside a daemonic pool worker, which is forbidden from
    # forking children.  In that case we fall back to solving in-process and the
    # deadline is only honoured BETWEEN k-levels (see solve_sat); that is weaker
    # but never unsound, since a level either completes or is not claimed.
    if (deadline is None or not _can_fork()) and \
            (ncores <= 1 or npairs0 < 2 or k < PAR_FROM_SAT):
        _, status, slp = _sat_worker((inst.r, inst.in_vals, inst.tgt_vals, k,
                                      None, solver_name, symmetry))
        return (status == "SAT"), slp
    if npairs0 < 2:
        tasks = [(inst.r, inst.in_vals, inst.tgt_vals, k, None, solver_name,
                  symmetry)]
        return _run_pool(_sat_worker, tasks, 1, deadline)
    # One task per cube (= per choice of the first gate's input pair).  The cubes
    # partition the search space exactly, because the pair selection of gate 0 is
    # constrained to be exactly-one.  One task per cube rather than one per core
    # lets the pool load-balance dynamically: cube difficulty varies by orders of
    # magnitude.
    tasks = [(inst.r, inst.in_vals, inst.tgt_vals, k, [j], solver_name, symmetry)
             for j in range(npairs0)]
    return _run_pool(_sat_worker, tasks, min(max(ncores, 1), npairs0), deadline)


def _run_pool(worker, tasks, nproc, deadline):
    """Run `tasks`; return (True, witness) on the first SAT, (False, None) if all
    tasks report UNSAT.  Raises Timeout if the deadline expires first."""
    import multiprocessing as mp
    from multiprocessing import TimeoutError as MPTimeout
    pool = mp.Pool(processes=nproc)
    try:
        it = pool.imap_unordered(worker, tasks)
        for _ in range(len(tasks)):
            if deadline is None:
                item = it.next()
            else:
                left = deadline - time.time()
                if left <= 0:
                    raise Timeout()
                try:
                    item = it.next(timeout=left)
                except MPTimeout:
                    raise Timeout()
            status, slp = item[1], item[2]
            if status == "SAT":
                return True, slp
        return False, None
    finally:
        pool.terminate()
        pool.join()


def solve_sat(inst: Instance, lb: int, ub: int, ncores: int,
              solver_name: str = DEFAULT_SOLVER, symmetry: bool = True,
              verbose: bool = False, log=None, deadline: Optional[float] = None):
    """Exact search upward from lb.  Returns (k, slp) with lb <= k <= ub, or
    (None, None) if no SLP with <= ub gates exists (exhaustively proven)."""
    for k in range(lb, ub + 1):
        if deadline is not None and time.time() >= deadline:
            raise Timeout()          # honoured between levels even when the
                                     # in-process fallback is in use
        t0 = time.time()
        ok, slp = sat_decide(inst, k, ncores, solver_name, symmetry, deadline)
        if verbose:
            msg = f"[sat] k={k}: {'SAT' if ok else 'UNSAT'}  ({time.time()-t0:.2f}s)"
            print(msg, file=sys.stderr)
        if log is not None:
            log.append({"k": k, "result": "SAT" if ok else "UNSAT",
                        "seconds": round(time.time() - t0, 3)})
        if ok:
            return k, slp
    return None, None


# ----------------------------------------------------------------------------
# Engine 2: iterative-deepening DFS with admissible pruning
# ----------------------------------------------------------------------------

class _DFS:
    def __init__(self, r: int, in_vals: List[int], tgt_vals: List[int],
                 use_memo: bool = True, memo_cap: int = 4_000_000):
        self.r = r
        self.m = len(in_vals)
        self.in_vals = list(in_vals)
        self.tgt = list(tgt_vals)
        self.ar = np.arange(1 << r, dtype=np.int64)
        self.use_memo = use_memo
        self.memo: Dict[Tuple, int] = {}
        self.memo_cap = memo_cap
        self.nodes = 0

    def search(self, budget: int, prefix: Optional[List[Tuple[int, int]]] = None):
        """Return an SLP with <= budget gates, or None (exhaustive)."""
        sig = list(self.in_vals)
        d = delta_array(self.r, sig)
        slp: List[Tuple[int, int]] = []
        prev_key = -1
        if prefix:
            for (p, q) in prefix:
                if q >= len(sig):
                    return None
                g = sig[p] ^ sig[q]
                if g == 0 or g in sig:
                    return None
                key = q * (q - 1) // 2 + p
                if len(slp) > 0 and q != len(sig) - 1 and key <= prev_key:
                    return None                      # violates (N3)
                prev_key = key
                slp.append((p, q))
                sig.append(g)
                d = delta_add(d, g, self.ar)
        if len(slp) > budget:
            return None
        self.memo.clear()
        return self._rec(sig, d, slp, budget - len(slp), prev_key)

    def _rec(self, sig, d, slp, budget, prev_key):
        self.nodes += 1
        rem = [t for t in self.tgt if int(d[t]) != 1]
        if not rem:
            return list(slp)
        lb = lower_bound(d, rem)
        if lb > budget:
            return None
        mk = None
        if self.use_memo:
            # The key must determine the whole subtree, because the (N3)
            # ordering rule depends on the *order* of the gate signals and on
            # the previous gate's pair key -- memoising on the unordered value
            # set would be unsound in the presence of (N3).
            mk = (tuple(sig[self.m:]), prev_key)
            got = self.memo.get(mk)
            if got is not None and got >= budget:
                return None
        nsig = len(sig)
        sigset = set(sig)
        last = nsig - 1
        for q in range(nsig):
            base = q * (q - 1) // 2
            sq = sig[q]
            for p in range(q):
                key = base + p
                if key <= prev_key and q != last and len(slp) > 0:
                    continue                        # (N3)
                g = sq ^ sig[p]
                if g == 0 or g in sigset:           # (N1)
                    continue
                d2 = delta_add(d, g, self.ar)
                sig.append(g)
                slp.append((p, q))
                res = self._rec(sig, d2, slp, budget - 1, key)
                slp.pop()
                sig.pop()
                if res is not None:
                    return res
        if mk is not None and len(self.memo) < self.memo_cap:
            self.memo[mk] = budget
        return None


def _dfs_worker(args):
    (r, in_vals, tgt_vals, budget, prefix) = args
    eng = _DFS(r, in_vals, tgt_vals)
    res = eng.search(budget, prefix)
    return (budget, "SAT" if res is not None else "UNSAT", res)


def dfs_decide(inst: Instance, k: int, ncores: int,
               deadline: Optional[float] = None):
    """Decide 'is there a k-gate SLP?' by exhaustive IDDFS."""
    if k == 0:
        return (not inst.tgt_vals), []
    prefixes = [[(p, q)] for q in range(inst.m) for p in range(q)]
    if ncores <= 1 or len(prefixes) < 2 or k < PAR_FROM_DFS:
        eng = _DFS(inst.r, inst.in_vals, inst.tgt_vals)
        res = eng.search(k)
        return (res is not None), res
    tasks = [(inst.r, inst.in_vals, inst.tgt_vals, k, pf) for pf in prefixes]
    return _run_pool(_dfs_worker, tasks, min(ncores, len(tasks)), deadline)


def solve_dfs(inst: Instance, lb: int, ub: int, ncores: int,
              verbose: bool = False, log=None, deadline: Optional[float] = None):
    for k in range(lb, ub + 1):
        t0 = time.time()
        ok, slp = dfs_decide(inst, k, ncores, deadline)
        if verbose:
            print(f"[dfs] k={k}: {'SAT' if ok else 'UNSAT'} "
                  f"({time.time()-t0:.2f}s)", file=sys.stderr)
        if log is not None:
            log.append({"k": k, "result": "SAT" if ok else "UNSAT",
                        "seconds": round(time.time() - t0, 3)})
        if ok:
            return k, slp
    return None, None


# ----------------------------------------------------------------------------
# Top-level driver
# ----------------------------------------------------------------------------

def solve_instance(dim: int, inputs: Sequence[int], targets: Sequence[int],
                   max_gates: Optional[int] = None, engine: str = "auto",
                   ncores: Optional[int] = None, solver_name: str = DEFAULT_SOLVER,
                   verbose: bool = False, greedy_restarts: int = 40,
                   symmetry: bool = True,
                   timeout: Optional[float] = None) -> Dict:
    t_start = time.time()
    deadline = (t_start + timeout) if timeout else None
    if ncores is None:
        ncores = os.cpu_count() or 1

    inst = Instance(dim, inputs, targets)
    out: Dict = {"min_gates": None, "slp": None}

    if inst.zero_target:
        raise ValueError(
            "target 0 requested but 0 is not an input value: the cost of "
            "producing the zero signal depends on whether 'a XOR a' is a legal "
            "gate.  Refusing to guess (see module docstring).")

    if inst.infeasible:
        out.update({
            "min_gates": None,
            "slp": None,
            "reason": "a target lies outside span(inputs): no SLP exists at any length",
            "lower_bound_proven": None,
            "exhaustive": True,
            "seconds": round(time.time() - t_start, 3),
        })
        return out

    # trivial case: nothing to compute
    if not inst.tgt_vals:
        ok, why = verify_slp(inputs, targets, [])
        if not ok:
            raise AssertionError("internal error: empty SLP failed verification: " + why)
        out.update({"min_gates": 0, "slp": [], "verified": True,
                    "engine": "trivial", "lower_bound_proven": 0,
                    "exhaustive": True,
                    "seconds": round(time.time() - t_start, 3)})
        return out

    # ---- bounds ------------------------------------------------------------
    d0 = delta_array(inst.r, inst.in_vals)
    lb = lower_bound(d0, inst.tgt_vals)
    lb = max(lb, len(inst.tgt_vals))
    ub, ub_slp = greedy_upper_bound(inst, restarts=greedy_restarts)
    if verbose:
        print(f"[bounds] lb={lb} ub={ub} (greedy)", file=sys.stderr)

    search_hi = ub
    capped = False
    if max_gates is not None:
        if max_gates < ub:
            search_hi = max_gates
            capped = True

    if engine == "auto":
        engine = "sat" if HAVE_PYSAT else "dfs"
    if engine == "sat" and not HAVE_PYSAT:
        raise RuntimeError("python-sat is not installed; use --engine dfs")

    log: List[Dict] = []
    try:
        if lb > search_hi:
            k, slp = None, None                 # bound alone settles it
        elif engine == "sat":
            k, slp = solve_sat(inst, lb, search_hi, ncores, solver_name,
                               symmetry=symmetry, verbose=verbose, log=log,
                               deadline=deadline)
        elif engine == "dfs":
            k, slp = solve_dfs(inst, lb, search_hi, ncores, verbose=verbose,
                               log=log, deadline=deadline)
        elif engine == "both":
            k1, slp1 = solve_sat(inst, lb, search_hi, ncores, solver_name,
                                 symmetry=symmetry, verbose=verbose, log=log,
                                 deadline=deadline)
            k2, slp2 = solve_dfs(inst, lb, search_hi, ncores, verbose=verbose,
                                 log=log, deadline=deadline)
            if k1 != k2:
                raise AssertionError(f"ENGINE DISAGREEMENT: sat={k1} dfs={k2}")
            k, slp = k1, slp1
        else:
            raise ValueError(f"unknown engine {engine!r}")
    except Timeout:
        # Nothing is claimed on the strength of an interrupted search: report the
        # strongest bounds that WERE established, and say plainly that the search
        # is incomplete.
        proven = lb
        for entry in log:
            if entry["result"] == "UNSAT":
                proven = max(proven, entry["k"] + 1)
        ub_slp_orig = internal_to_original(inst, ub_slp)
        ok, why = verify_slp(inputs, targets, ub_slp_orig)
        if not ok:
            raise AssertionError("WITNESS VERIFICATION FAILED: " + why)

        # The bracket may already have closed: `proven` means "no SLP with
        # <= proven-1 gates exists" (an exhaustive UNSAT result, unaffected by
        # the interruption), and ub_slp is a VERIFIED SLP of length ub.  If
        # proven == ub the two meet and the optimum is settled at ub, so
        # reporting a timeout here would understate what was actually proved.
        if proven >= ub:
            out.update({
                "min_gates": ub,
                "slp": ub_slp_orig,
                "verified": True,
                "engine": engine,
                "lower_bound_proven": ub,
                "combinatorial_lower_bound": lb,
                "greedy_upper_bound": ub,
                "exhaustive": True,
                "search_log": log,
                "seconds": round(time.time() - t_start, 3),
                "note": ("the wall-clock limit expired, but the proven lower "
                         "bound had already met the verified witness length, "
                         "so the optimum is settled"),
            })
            return out

        out.update({
            "min_gates": None,
            "slp": None,
            "exhaustive": False,
            "timed_out": True,
            "engine": engine,
            "lower_bound_proven": proven,
            "combinatorial_lower_bound": lb,
            "best_known_upper_bound": ub,
            "best_known_slp": ub_slp_orig,
            "search_log": log,
            "seconds": round(time.time() - t_start, 3),
            "note": (f"search interrupted by the {timeout}s wall-clock limit; "
                     f"the optimum is known only to lie in [{proven}, {ub}]"),
        })
        return out

    if k is None and not capped:
        # greedy already produced an SLP with ub gates, so ub is feasible;
        # UNSAT for all k <= ub would be a contradiction.
        raise AssertionError("internal error: no solution found at or below a "
                             "known-feasible length")

    if k is None:
        out.update({
            "min_gates": None,
            "slp": None,
            "lower_bound_proven": max_gates + 1,
            "combinatorial_lower_bound": lb,
            "exhaustive": True,
            "engine": engine,
            "search_log": log,
            "seconds": round(time.time() - t_start, 3),
            "note": f"exhaustively proven: no SLP with <= {max_gates} gates exists",
        })
        return out

    slp_orig = internal_to_original(inst, slp)
    ok, why = verify_slp(inputs, targets, slp_orig)
    if not ok:
        raise AssertionError("WITNESS VERIFICATION FAILED: " + why)
    if len(slp_orig) != k:
        raise AssertionError("witness length disagrees with reported optimum")

    out.update({
        "min_gates": k,
        "slp": slp_orig,
        "verified": True,
        "engine": engine,
        "lower_bound_proven": k,
        "combinatorial_lower_bound": lb,
        "greedy_upper_bound": ub,
        "exhaustive": True,
        "search_log": log,
        "seconds": round(time.time() - t_start, 3),
    })
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Exact minimal-SLP oracle for GF(2) linear straight-line programs")
    ap.add_argument("instance", help="path to instance JSON ('-' for stdin)")
    ap.add_argument("--engine", default="auto", choices=["auto", "sat", "dfs", "both"])
    ap.add_argument("--cores", type=int, default=None)
    ap.add_argument("--solver", default=DEFAULT_SOLVER,
                    help="python-sat backend (cadical195, kissat404, glucose42, ...)")
    ap.add_argument("--greedy-restarts", type=int, default=40)
    ap.add_argument("--timeout", type=float, default=None,
                    help="wall-clock limit in seconds; on expiry the oracle "
                         "reports bounds only and exhaustive=false")
    ap.add_argument("--no-symmetry", action="store_true",
                    help="disable the sound symmetry-breaking clauses (slower, "
                         "used for validation)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)

    raw = sys.stdin.read() if args.instance == "-" else open(args.instance).read()
    spec = json.loads(raw)
    res = solve_instance(
        dim=int(spec["dim"]),
        inputs=[int(x) for x in spec["inputs"]],
        targets=[int(x) for x in spec["targets"]],
        max_gates=(int(spec["max_gates"]) if spec.get("max_gates") is not None else None),
        engine=args.engine,
        ncores=args.cores,
        solver_name=args.solver,
        verbose=args.verbose,
        greedy_restarts=args.greedy_restarts,
        symmetry=not args.no_symmetry,
        timeout=args.timeout,
    )
    print(json.dumps(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
