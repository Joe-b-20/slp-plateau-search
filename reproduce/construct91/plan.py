#!/usr/bin/env python3
"""plan.py — THE one model layer.

Three lanes previously had three model layers (`recipes.py` + `ladder.py`,
`v2model.py`, `f4model.py`, `model.py`).  Here there is one datatype --

    Block(name, lines, targets, supply, program)

-- and the three regimes are three PLAN BUILDERS that emit lists of it.

    naive   closed form, ZERO solver calls.  The universal ladder scheme:
            per sector S = sum of the four own raws (the socle d_k (x) v^3),
            p_j = S + y^j, T_j = p_j + q_j.  116 gates, depth 3.
    ladder  lane G's M1 configuration model: currency menus per line, DIAGONAL
            menus per tap, one exact sector module per sector.  91..107.
    f4      the derived architecture of `laws.py` with the L5 free-supply rule.
            88.

WHAT THE THREE REGIMES ACTUALLY ARE, in one sentence each, now that they share
a datatype: `naive` fixes every block's program in closed form; `ladder`
RESTRICTS each tap sector's supply to the DIAGONAL subspace of its plane
(so its plane values are one-parameter delta_k(t), never the two-parameter
u(a,b)); `f4` applies the L5 rule and lets the plane be the whole thing.
The 91-vs-88 gap is therefore visible here as one word: `supply`.

SUPPLY
------
  "auto"   : law L5 -- every already-built value whose SUPPORT lies inside the
             block's working line-set, at its true arrival level.  This is what
             derives the shared-plane rule; nothing about D37 is special-cased.
  a list   : an explicit restriction, used by `ladder` (the diagonal ansatz)
             and by the labelled `--no-share` control that reproduces lane G's
             deliberate deletion of the D37 -> W3 edge.
"""
import os, sys
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Any

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from theory import (RAWS, PAIRS, TAPS, CLEAN, PARENT, QLINES, ypow, YBYTE,
                    lines_to_mask, sector_value_lines, SECTOR_TARGETS, support)
from algebra import (lv, vadd, diag, plane, raws, raw_bit, sector_targets,
                     hexlines, t_min_gates, currency_plan)
import laws

def _halo(name, lines):
    """lane HALO (fleet12): audit defect D22 -- the ten-block line partition
    fleet8 enforces is not the nine-block partition lane A measured, its
    B27|W3 and B37|U4 boundaries were never tested on any circuit, and REF-V22
    exhibits a value (91@6 gate 70, support {2,3,4,7}) that fits lane A's U4
    and NO fleet8 block.  LANE_HALO widens one or more blocks' line sets by a
    HALO so that values may straddle a boundary:

        LANE_HALO="U4:+2"            U4  {3,4,7} -> {2,3,4,7}
        LANE_HALO="W3:+4,U4:+2"      both, for a PAIR mutation

    The widened set is returned here and nowhere else, which is the point: the
    Block's `lines` field is the single object that `engine._auto_supply`
    (law L5) and `solver.make_instance` (the CNF and both `support(v) <= Ls`
    asserts) both read, so all three of D22's sites see one consistent set.

    TRACTABILITY GUARD: a widened set of more than 4 lines (dim > 16) is
    refused loudly.  Widening toward dim 32 is the whole-circuit instance and
    does not terminate.

    When LANE_HALO is unset this function returns its argument unchanged and
    the module behaves byte-identically to the shipped one.
    """
    spec = os.environ.get("LANE_HALO", "").strip()
    if not spec:
        return lines
    for item in spec.split(","):
        item = item.strip()
        if not item:
            continue
        if ":" not in item:
            raise SystemExit(f"LANE_HALO: bad item {item!r}, want BLOCK:+LINE")
        who, add = item.split(":", 1)
        if who.strip() != name:
            continue
        new = set(lines)
        for tok in add.replace("+", " ").split():
            new.add(int(tok))
        out = tuple(sorted(new))
        if len(out) > 4:
            raise SystemExit(
                f"LANE_HALO: block {name} widened to {list(out)} = dim "
                f"{4*len(out)}; the tractability guard refuses more than 4 "
                f"lines (dim 16).  REFUSED, not attempted.")
        print(f"  LANE_HALO: block {name} lines {list(lines)} -> {list(out)} "
              f"(dim {4*len(lines)} -> {4*len(out)})", flush=True)
        return out
    return lines


QDEMAND = [q for _, q in SECTOR_TARGETS]        # the four demanded q-shapes
SOCLE = 0x8                                     # v^3 = sum of the four raws


# ------------------------------------------------------------------- Block
@dataclass
class Block:
    name: str
    lines: Tuple[int, ...]
    targets: List[Tuple[Any, Optional[int]]]     # [(8-line value, level cap)]
    supply: Any = "auto"                         # "auto" (L5) or [values]
    program: str = "exact"                       # "exact" | "closed"
    note: str = ""


@dataclass
class Plan:
    regime: str
    blocks: List[Block] = field(default_factory=list)
    prelude: Any = None            # callable(ms) -> {"terms": {...}}
    closed: Any = None             # callable(ms) -> {"terms": {...}}
    menu: dict = field(default_factory=dict)
    cur_depth: Optional[int] = None
    meta: dict = field(default_factory=dict)


# ------------------------------------------------------------ shape helpers
def t_bits(t):
    """the input-bit ring exponents of the T-nibble t on a line (v -> y)."""
    y = [0, 0, 0, 0]
    if t & 1:
        y[0] ^= 1
    if t & 2:
        y[0] ^= 1; y[1] ^= 1
    if t & 4:
        y[0] ^= 1; y[2] ^= 1
    if t & 8:
        for i in range(4):
            y[i] ^= 1
    return [a for a in range(4) if y[a]]


def build_col_element(ms, t, line, tag):
    m = lines_to_mask(lv(line, t))
    if m in ms.have:
        return m
    return ms.add_chain([8 * YBYTE[a] + line for a in t_bits(t)], tag)


def build_diag_element(ms, t, k, tag):
    m = lines_to_mask(diag(k, t))
    if m in ms.have:
        return m
    par = PARENT[k]
    bits = t_bits(t)
    if len(bits) == 1:                       # a unit shape: always one gate
        a = bits[0]
        return ms.add(raw_bit(par, a), raw_bit(7, a), tag)
    return ms.add(build_col_element(ms, t, par, tag),
                  build_col_element(ms, t, 7, tag), tag)


# ------------------------------------------------------------ regime: naive
def naive_plan():
    """The closed-form universal ladder scheme.  ZERO solver calls."""
    def closed(ms):
        terms = {}
        for line in range(8):
            n0 = ms.n_gates()
            for t in QDEMAND:
                build_col_element(ms, t, line, f"COL{line}")
            terms[f"COL{line}"] = ms.n_gates() - n0
        for k in TAPS:
            n0 = ms.n_gates()
            for t in QDEMAND:
                build_diag_element(ms, t, k, f"DIAG{k}")
            terms[f"DIAG{k}"] = ms.n_gates() - n0
        for k in range(8):
            n0 = ms.n_gates()
            tag = f"S{k}"
            s1 = ms.add(raw_bit(k, 0), raw_bit(k, 1), tag)
            s2 = ms.add(raw_bit(k, 2), raw_bit(k, 3), tag)
            S = ms.add(s1, s2, tag)                 # the socle d_k (x) v^3
            assert S == lines_to_mask(lv(k, SOCLE))
            for j in range(4):
                p, q = SECTOR_TARGETS[j]
                pj = ms.add(S, raw_bit(k, j), tag)
                assert pj == lines_to_mask(sector_value_lines(k, p, 0))
                qm = lines_to_mask(lv(PARENT[k], q) if k in CLEAN else diag(k, q))
                ms.add(pj, qm, tag)
            terms[tag] = ms.n_gates() - n0
        return {"terms": terms, "oracle_calls": 0}
    return Plan(regime="naive", closed=closed,
                meta={"oracle_calls": 0, "closed_form": True})


# ----------------------------------------------------------- regime: ladder
def dcost(D, Cpar, C7):
    """lane G's diagonal manufacture price: a unit shape costs 1 gate; a pair
    shape costs 1 plus one for each of its two halves that is not already on
    that line's menu."""
    pure_units = [u for u in RAWS if u not in PAIRS]
    c = 0
    for t in D:
        c += 1 if t in pure_units else 1 + (0 if t in Cpar else 1) \
                                        + (0 if t in C7 else 1)
    return c


def ladder_plan(cfg, D=None):
    """cfg = {"C": [8 shape lists], "D": {"1": [...], "3": [...], "4": [...]}}"""
    C = [tuple(sorted(x)) for x in cfg["C"]]
    Dg = {int(k): tuple(sorted(v)) for k, v in cfg["D"].items()}

    def prelude(ms):
        terms = {}
        for line in range(8):
            n0 = ms.n_gates()
            for t in C[line]:
                build_col_element(ms, t, line, f"COL{line}")
            terms[f"COL{line}"] = ms.n_gates() - n0
        for k in TAPS:
            n0 = ms.n_gates()
            for t in Dg[k]:
                build_diag_element(ms, t, k, f"DIAG{k}")
            terms[f"DIAG{k}"] = ms.n_gates() - n0
        return {"terms": terms}

    blocks = []
    for k in range(8):
        if k in CLEAN:
            par = PARENT[k]
            sup = (raws(k) + raws(par) + [lv(k, t) for t in C[k]]
                   + [lv(par, t) for t in C[par]])
            lines = tuple(sorted({k, par}))
            note = "clean sector: its q-line is a single dual line, so the four neighbour raws are ordinary input bits and are FREE"
        else:
            sup = raws(k) + [lv(k, t) for t in C[k]] + [diag(k, t) for t in Dg[k]]
            lines = tuple(sorted({k, PARENT[k], 7}))
            note = ("tap sector: supply RESTRICTED to the DIAGONAL subspace of "
                    "the plane -- this restriction IS the ladder model, and it "
                    "is what prices 91 instead of 88")
        blocks.append(Block(name=f"S{k}", lines=lines,
                            targets=[(t, D) for t in sector_targets(k)],
                            supply=sup, note=note))
    return Plan(regime="ladder", blocks=blocks, prelude=prelude,
                meta={"config": {"C": [list(x) for x in C],
                                 "D": {str(k): list(v) for k, v in Dg.items()}},
                      "currency": sum(len(c) for c in C),
                      "diagonals": sum(dcost(Dg[k], set(C[PARENT[k]]), set(C[7]))
                                       for k in TAPS)})


# --------------------------------------------------------------- regime: f4
def f4_plan(menu, commit, iface_lvl=None, D=None, dcur=None, share=True):
    """The DERIVED architecture (laws.py) instantiated with a currency menu
    and an interface commitment.

    menu      {line: (shapes,)}                     -- flag F1 unless derived
    commit    {tap: [values]}                       -- Q1 / Q27 / D37
    iface_lvl {tap: level}                          -- the level each committed
                                                        set must arrive at
    D         the global depth cap, or None
    share     False deletes the D37 -> W3 edge (lane G's model), as a LABELLED
              CONTROL.  Under law L5 that edge is not optional, so switching it
              off is an explicit deletion, not a configuration.
    """
    arch, iface = laws.architecture()
    order = laws.block_order()
    iface_lvl = dict(iface_lvl or {})
    blocks = []
    for name in order:
        b = arch[name]
        tg = []
        if b["sector"] is not None:
            tg += [(t, D) for t in sector_targets(b["sector"])]
        for k in b["produces"]:
            cap = iface_lvl.get(k, D)
            tg += [(tuple(v), cap) for v in commit.get(k, [])]
        if not tg:
            continue
        supply = "auto"
        if not share and name == "W3":
            # the labelled control: delete the L5 edge that gives W3 the
            # shared plane.  Everything else is unchanged.
            supply = ("auto_except", [tuple(v) for v in commit.get(4, [])])
        blocks.append(Block(name=name, lines=_halo(name, tuple(b["lines"])),
                            targets=tg,
                            supply=supply,
                            note=("dedicated interface block for tap "
                                  f"{b['produces']}" if b["sector"] is None
                                  else f"sector {b['sector']} work"
                                       + (f" + interface for tap {b['produces']}"
                                          if b["produces"] else ""))))
    return Plan(regime="f4", blocks=blocks, menu=dict(menu), cur_depth=dcur,
                meta={"commit": {str(k): [list(v) for v in vs]
                                 for k, vs in commit.items()},
                      "iface_levels": {str(k): v for k, v in iface_lvl.items()},
                      "share": share,
                      "architecture": {n: arch[n]["lines"] for n in order},
                      "interfaces": {laws.iface_name(k): iface[k] for k in iface}})


# ------------------------------------------------------------ currency phase
def currency_prelude(menu, dcur):
    """Build a menu's currency at the exact gates-vs-depth optimum and return
    the arrival LEVEL of every menu shape."""
    tot, lvls, steps = currency_plan(menu, dcur)
    if tot is None:
        return None, None

    def prelude(ms):
        terms = {}
        for m in range(8):
            n0 = ms.n_gates()
            vals = {ypow(a): raw_bit(m, a) for a in range(4)}
            for a, b in steps[m]:
                vals[a ^ b] = ms.add(vals[a], vals[b], f"COL{m}")
            for t in menu.get(m, ()):
                assert t in vals, (m, t)
            terms[f"COL{m}"] = ms.n_gates() - n0
        return {"terms": terms}
    return prelude, lvls
