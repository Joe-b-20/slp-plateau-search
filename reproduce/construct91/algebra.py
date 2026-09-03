#!/usr/bin/env python3
"""algebra.py — line-coordinate VALUES, packing, currency, and the one-gate
interface families.  Everything here sits directly on top of `theory.py`
(the single shared algebra core, md5 90889a780e1179c5b93a8fff2b5ab3c2) and
adds no new algebraic content.

A VALUE is an 8-tuple of T-nibbles (one per dual line), exactly lane F4's
representation.  `lines_to_mask` turns it into a real 32-bit mask.

Contents
--------
  lv / vadd / diag / plane / raws     value constructors  (from lane F4)
  pack / unpack                       ASCENDING-line packing (lane F4's own)
  t_min_gates                         EXACT gates-vs-depth curve for one line's
                                      currency menu; d=None => unconstrained
                                      (then it reproduces lane F4's `costT`)
  one_gate_family                     the CORRECTED enumeration of the values
                                      on a two-line plane that cost exactly one
                                      gate.  lane F4's `planeenum.py` undercounts
                                      (24 where the truth is 64 on {3,7}, 56
                                      where the truth is 71 on {2,7}) -- referee
                                      finding 4, honoured here.
"""
import os, sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from theory import (RAWS, PAIRS, QLINES, PARENT, TAPS, CLEAN, ypow, tmul,
                    YBYTE, lines_to_mask, mask_to_lines, support,
                    sector_value_lines, SECTOR_TARGETS, TARGET_MASKS)


# ------------------------------------------------------------------ values
def lv(line, t):
    x = [0] * 8
    x[line] = t & 0xF
    return tuple(x)


def vadd(*xs):
    o = [0] * 8
    for x in xs:
        for i in range(8):
            o[i] ^= x[i]
    return tuple(o)


def diag(k, t):
    """tap-k diagonal: the sector-k q-carrier, t on every line of QLINES[k]."""
    x = [0] * 8
    for m in QLINES[k]:
        x[m] ^= t & 0xF
    return tuple(x)


def plane(a_line, b_line, a, b):
    return vadd(lv(a_line, a), lv(b_line, b))


def raws(line):
    return [lv(line, ypow(j)) for j in range(4)]


def raw_bit(line, a):
    """the real input bit carrying d_line (x) y^a."""
    return 1 << (8 * YBYTE[a] + line)


def hexlines(x):
    return "[" + " ".join(f"{t:x}" if t else "." for t in x) + "]"


def sector_targets(k):
    return [sector_value_lines(k, p, q) for p, q in SECTOR_TARGETS]


# ----------------------------------------------------------------- packing
def pack(x, L):
    v = 0
    for i, m in enumerate(sorted(L)):
        v |= (x[m] & 0xF) << (4 * i)
    return v


def unpack(v, L):
    x = [0] * 8
    for i, m in enumerate(sorted(L)):
        x[m] ^= (v >> (4 * i)) & 0xF
    return tuple(x)


# ---------------------------------------------------------------- currency
class CurrencyUndecided(Exception):
    """lane LIB (fleet12), audit defect D5, severity 1.

    `t_min_gates` ran out of its `kmax` LOOP BOUND without settling the
    question.  That is a truncation, not a proof, and it must never reach a
    caller as *"provably infeasible"* -- which is exactly what happened before
    this class existed: `currency_plan` returned the same `(None, None, None)`
    for a genuine frontier exhaustion and for a `kmax` overrun, and
    `generate.py` rendered either as `InfeasibleAtDepth("CURRENCY")` -> exit 4,
    documented as *"provably infeasible"*.  REF-V8's witness:
    `t_min_gates((2,4,6,8), kmax=4)` returns `None` though 5 gates suffice."""

    def __init__(self, line, menu, kmax, d):
        self.line, self.menu, self.kmax, self.d = line, menu, kmax, d
        super().__init__(
            f"line {line}: the currency search hit its gate ceiling kmax="
            f"{kmax} on menu {sorted(menu)} at depth<={d} without deciding. "
            f"UNDECIDED (>{kmax} gates, or infeasible) -- NOT a proof of "
            f"impossibility.  Re-run with a larger kmax.")


# lane F1 (fleet12): audit R49 / defect D5.  `kmax = 8` is an undocumented LOOP
# BOUND, not a theorem -- R49 says so in as many words ("8 is not an upper bound
# for an arbitrary menu; a 15-shape menu provably needs >=11") and this lane hit
# it live: a menu offering all eleven non-raw nibbles on a line raises
# `CurrencyUndecided`, correctly, because 11 shapes need 11 gates.  Raising the
# bound is what R49 recommends ("free at the shipped menus"); doing it by
# environment variable keeps the default byte-identical.  Unset or empty => 8.
_KMAX_ENV = os.environ.get("SLP_CURRENCY_KMAX", "").strip()
KMAX_DEFAULT = int(_KMAX_ENV) if _KMAX_ENV else 8


def t_min_gates_ex(menu, d=None, kmax=None):
    """(gates, {shape: level}, [(a,b), ...], status) — as `t_min_gates`, plus
    the STATUS that distinguishes this function's two failure modes:

        "exact"      gates is the proved minimum
        "impossible" the frontier emptied: no state remains to extend, so no
                     number of gates can do it under the depth cap.  A PROOF.
        "undecided"  the `kmax` loop ran out with a non-empty frontier.  A
                     TRUNCATION, indistinguishable from a proof in the
                     3-tuple API (audit R48/R49, defect D5).

    lane LIB (fleet12).  `t_min_gates` below is unchanged for every existing
    caller; it is this function's first three fields."""
    kmax = KMAX_DEFAULT if kmax is None else kmax
    cap = kmax if d is None else d
    menu = tuple(sorted(set(t for t in menu if t)))
    start = {t: 0 for t in RAWS}
    if all(t in start for t in menu):
        return 0, {t: 0 for t in menu}, [], "exact"

    def done(st):
        return all(t in st and st[t] <= cap for t in menu)

    def key(st):
        return tuple(sorted(st.items()))

    frontier = {key(start): (start, [])}
    for g in range(1, kmax + 1):
        nxt = {}
        for st, steps in frontier.values():
            items = sorted(st.items())
            for i in range(len(items)):
                for j in range(i + 1, len(items)):
                    (va, la), (vb, lb) = items[i], items[j]
                    x = va ^ vb
                    nl = max(la, lb) + 1
                    if x == 0 or nl > cap:
                        continue
                    if x in st and st[x] <= nl:
                        continue
                    s2 = dict(st)
                    s2[x] = nl
                    k2 = key(s2)
                    if k2 not in nxt:
                        nxt[k2] = (s2, steps + [(va, vb)])
                        if done(s2):
                            return g, {t: s2[t] for t in menu}, nxt[k2][1], "exact"
        frontier = nxt
        if not frontier:
            # every state has been extended and none can be extended further:
            # the reachable set is closed and does not contain the menu.  A
            # genuine proof (algebra.py:139 in the pre-lane-LIB numbering).
            return None, None, None, "impossible"
    # the `kmax` loop ran out with states still to extend.  A TRUNCATION
    # (algebra.py:140 in the pre-lane-LIB numbering) -- see `CurrencyUndecided`.
    return None, None, None, "undecided"


def t_min_gates(menu, d=None, kmax=None):
    """(gates, {shape: level}, [(a,b), ...]) — the EXACT minimum number of
    gates to have every shape of `menu` available on one line, subject to
    every menu shape arriving at level <= d.  `d=None` drops the depth
    constraint entirely (kmax gates can never exceed depth kmax), in which
    case this reproduces lane F4's `costT`.

    Exhaustive breadth-first over (value -> min level) states.  No solver, no
    heuristic.

    WARNING (lane LIB, fleet12; audit R48/R49/D5).  The docstring used to say
    *"`None` means PROVABLY IMPOSSIBLE, not 'not found'"*.  THAT IS FALSE:
    `t_min_gates((2,4,6,8), kmax=4)` returns `None` although 5 gates suffice.
    There are two `None` paths and this 3-tuple API cannot tell them apart.
    Use `t_min_gates_ex` and read its `status` when the difference matters --
    `currency_plan` now does."""
    return t_min_gates_ex(menu, d, kmax)[:3]


def currency_plan(menu, dcur=None):
    """(total gates, {(line, shape): level}, {line: steps}) for a whole
    8-line menu, or (None, None, None) if PROVABLY infeasible at depth `dcur`.

    lane LIB (fleet12), audit defect D5: raises `CurrencyUndecided` when the
    failure is a `kmax` truncation rather than a proof.  `(None, None, None)`
    now means what it says."""
    tot, lvls, steps = 0, {}, {}
    for m in range(8):
        g, lev, st, status = t_min_gates_ex(menu.get(m, ()), dcur)
        if status == "undecided":
            raise CurrencyUndecided(m, menu.get(m, ()), KMAX_DEFAULT, dcur)
        if g is None:
            return None, None, None
        tot += g
        steps[m] = st
        for t, l in (lev or {}).items():
            lvls[(m, t)] = l
    return tot, lvls, steps


# ------------------------------------------------- one-gate interface family
def one_gate_family(lines, menu, include_singles=True):
    """Every value supported on the two-line plane `lines` that can be built
    with EXACTLY ONE gate from what a block on that plane already has free
    (the 8 raw input bits of the two lines, plus each line's currency menu).

    This is the corrected version of lane F4's `planeenum.py`.  That file only
    enumerated the values u(a,b) with BOTH halves non-zero and the diagonal
    part restricted to vT; the referee's re-enumeration found 64 on {3,7} and
    71 on {2,7} against the lane's 24 and 56.  The 16 / 15 extra values are
    the PURE-LINE commitments (one half zero) -- and they are not inert: the
    referee's free-64 optimum consumes d_3 (x) 4, one of them.

    Returns a sorted list of 8-tuples.
    """
    a_line, b_line = sorted(lines)
    have_a = sorted(set(RAWS) | set(menu.get(a_line, ())))
    have_b = sorted(set(RAWS) | set(menu.get(b_line, ())))
    avail = [lv(a_line, t) for t in have_a] + [lv(b_line, t) for t in have_b]
    free = set(avail)                       # these cost ZERO, not one
    out = set()
    for x, y in combinations(avail, 2):
        v = vadd(x, y)
        if any(v) and v not in free:        # <-- cost EXACTLY one
            out.add(v)
    if not include_singles:
        out = {v for v in out if v[a_line] and v[b_line]}
    return sorted(out)


def plane_family(lines, menu, max_cost=1):
    """Every value on the two-line plane the supplier can mint for AT MOST
    `max_cost` gates from raws + currency.

    WHY THIS EXISTS (found the hard way, 2026-08-24).  `one_gate_family` is the
    right narrowing only where the supplier's marginal cost per value really is
    one gate.  That holds on {2,7} and {3,7} at the 88@7 cell, but NOT on {0,7}:
    line 0's menu is EMPTY there, so every value that mixes a non-raw nibble
    costs 2, and the whole configured Q1 -- delta_1(4), delta_1(6), delta_1(e),
    each 2 gates -- lies OUTSIDE the one-gate family.  A free-supply derive run
    over the one-gate family therefore cannot select the configured Q1 even in
    principle, and its disagreement is VACUOUS rather than evidence.  Always
    check `family_contains_configured` before reading a derive result.
    """
    a_line, b_line = sorted(lines)
    have_a = sorted(set(RAWS) | set(menu.get(a_line, ())))
    have_b = sorted(set(RAWS) | set(menu.get(b_line, ())))
    free = {lv(a_line, t) for t in have_a} | {lv(b_line, t) for t in have_b}
    frontier, out = set(free), set()
    for _g in range(1, max_cost + 1):
        nxt = set()
        cur = sorted(frontier | free)
        for i in range(len(cur)):
            for j in range(i + 1, len(cur)):
                v = vadd(cur[i], cur[j])
                if any(v) and v not in free and v not in out:
                    nxt.add(v)
        out |= nxt
        frontier |= nxt
    return sorted(out)


def value_cost_on_plane(v, lines, menu):
    """the number of gates a block on `lines` must spend to mint value `v`
    from raws+menu, computed exactly by BFS over the 2-line value space
    (used to price a candidate commitment before offering it)."""
    a_line, b_line = sorted(lines)
    have_a = sorted(set(RAWS) | set(menu.get(a_line, ())))
    have_b = sorted(set(RAWS) | set(menu.get(b_line, ())))
    start = frozenset([pack(lv(a_line, t), lines) for t in have_a] +
                      [pack(lv(b_line, t), lines) for t in have_b])
    goal = pack(v, lines)
    if goal in start:
        return 0
    cur = set(start)
    for g in range(1, 5):
        new = set()
        cl = sorted(cur)
        for i in range(len(cl)):
            for j in range(i + 1, len(cl)):
                x = cl[i] ^ cl[j]
                if x and x not in cur:
                    new.add(x)
        if goal in new:
            return g
        cur |= new
    return None


if __name__ == "__main__":
    import json
    print("t_min_gates((6,8,c,d), None) =", t_min_gates((0x6, 0x8, 0xc, 0xd))[:1])
    for d in (1, 2, 3, 4):
        print(f"  ... at depth {d}:", t_min_gates((0x6, 0x8, 0xc, 0xd), d)[0])
    M88at7 = {0: (), 1: (0x6, 0x8, 0xc, 0xd), 2: (0x4, 0x6, 0xc), 3: (0x2, 0xa),
              4: (0x2, 0xa, 0xc), 5: (0x6, 0xc, 0xe), 6: (0x4, 0x6, 0xe),
              7: (0x2, 0x4, 0xa, 0xc)}
    print("one-gate family on {3,7} @88@7 :", len(one_gate_family([3, 7], M88at7)),
          "(referee: 64)")
    print("one-gate family on {2,7} @88@7 :", len(one_gate_family([2, 7], M88at7)),
          "(referee: 71)")
    print("one-gate family on {0,7} @88@7 :", len(one_gate_family([0, 7], M88at7)))
