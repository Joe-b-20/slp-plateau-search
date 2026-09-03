#!/usr/bin/env python3
"""laws.py — the project's structural laws, expressed as CODE THAT DERIVES
THEM rather than tables that record them.

Everything in this file is computed from `theory.py` alone (i.e. from GF(2^8),
the AES reduction polynomial 0x11B, and the FIPS-197 matrix).  Nothing is read
off a record circuit and nothing is a constant lifted from a RESULT.md.

WHAT IS DERIVED HERE (each has a machine check in `selftest()`)
--------------------------------------------------------------
 L0  TAPS = {k : tau_k = 1} = {1,3,4}.  From the dual xtime chain
     2 d_k = d_{k-1} + tau_k d_7, whose tau IS the reduction polynomial.
     (Already in theory.py; restated so the chain of reasoning is visible.)

 L1  WORKSET.  The block that owns line j must work on lines
        {j} u {PARENT[j]} u ({7} if j is a tap else {})
     because sector j's targets have a p-part on line j and a q-part on
     QLINES[j] = {PARENT[j]} u ({7} if tau_j else {}).
     COROLLARY, used constantly below (for j != 7, the hub's own line):
        7 in WORKSET(j)  <=>  j in TAPS u {0}
     (for clean j not in {0,7} the workset is {j, j-1}, and PARENT[0] = 7).
     Line 7 is excluded because it *is* the hub; no plane ever sits above it,
     since PLANE(k) = {k-1, 7} and k-1 is 0, 2 or 3.

 L2  PLANE.  Tap k's q-carrier lives on PLANE(k) = QLINES[k] = {k-1, 7}.

 L3  SHARED / UNSHARED.  PLANE(k) is paid for by the block below it iff
        PLANE(k) subset of WORKSET(k-1)   <=>   7 in WORKSET(k-1)
                                          <=>   k-1 in TAPS u {0}
     i.e. **a tap's plane pays for itself iff it sits directly above another
     tap or the root**.  For AES: 1 is above the root (shared), 4 is above tap
     3 (shared), 3 is above the CLEAN line 2 (UNSHARED).
     => TAP 3 IS THE UNIQUE UNSHARED INTERFACE.  Derived, not configured.

 L4  SUPPLIER.  If WORKSET(k-1) == PLANE(k) the plane's supplier IS the block
     that owns line k-1 (its targets simply gain the plane values); otherwise
     the plane needs a DEDICATED interface block on PLANE(k).
     For AES: WORKSET(0) == {0,7} == PLANE(1)  -> merged into U07 (this is Q1);
              WORKSET(2) == {1,2} != PLANE(3)  -> dedicated B27  (this is Q27);
              WORKSET(3) == {2,3,7} != PLANE(4)-> dedicated B37  (this is D37).
     That reproduces lane F4's ten-block architecture exactly, with no table.

 L5  FREE SUPPLY (this is lane F4's "shared-plane RULE", derived).
     A value that has already been built is available, at no further cost, to
     every block whose WORKSET contains its support.  Applying this rule
     mechanically gives D37 (support {3,7}) to BOTH W3 (workset {2,3,7}) and
     U4 (workset {3,4,7}) -- which is precisely the single edge worth the
     three gates between 91 and 88.  Lane G's model routed D37 to U4 only;
     under L5 that restriction is not expressible without deliberately
     deleting an edge (`--no-share`, kept as the labelled control).
     L5 also explains why Q27 (support {2,7}) reaches only W3: no other
     workset contains {2,7}.  UNSHARED is a consequence, not a stipulation.

WHAT IS *NOT* DERIVED HERE (stated so the boundary is visible)
-------------------------------------------------------------
 * The RANK at each interface.  `interface_rank_curve()` MEASURES it with the
   solver (it does not assume 1); see `derive.py`.
 * The shared-plane CONSERVATION law B37 + U4 >= 11.  `conservation_bound()`
   re-derives it here as the REPLAY BOUND, which is a proof modulo one exact
   solve of U4-with-no-D37; it is not a closed-form theorem.
 * The currency menus (flag F1).
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from theory import TAPS, CLEAN, PARENT, QLINES, support
from algebra import sector_targets

ROOT_LINE = 0          # sector 0 is the base of the ladder: PARENT[0] = 7


# --------------------------------------------------------------- L1 workset
def workset(j):
    """The lines the block that owns line j must work on (L1)."""
    return tuple(sorted({j, PARENT[j]} | ({7} if j in TAPS else set())))


def touches_hub(j):
    """7 in WORKSET(j).  Derived corollary of L1."""
    return 7 in workset(j)


# ----------------------------------------------------------------- L2 plane
def plane_of(k):
    """Tap k's q-carrier plane = QLINES[k] = {k-1, 7}."""
    assert k in TAPS, f"line {k} is not a tap"
    return tuple(sorted(QLINES[k]))


# ------------------------------------------------------ L3 shared / unshared
def plane_is_shared(k):
    """True iff tap k's plane is paid for by the block below it.
    Derived: PLANE(k) subset WORKSET(k-1)  <=>  k-1 in TAPS u {root}."""
    below = PARENT[k]
    return set(plane_of(k)) <= set(workset(below))


def unshared_taps():
    return tuple(k for k in TAPS if not plane_is_shared(k))


def shared_taps():
    return tuple(k for k in TAPS if plane_is_shared(k))


def why_shared(k):
    below = PARENT[k]
    if plane_is_shared(k):
        why = ("the root (PARENT[0] = 7, so sector 0 already works on the hub)"
               if below == ROOT_LINE else f"tap {below} (which drags in the hub)")
        return f"tap {k}: plane {plane_of(k)} SHARED -- it sits directly above {why}"
    return (f"tap {k}: plane {plane_of(k)} UNSHARED -- it sits above the CLEAN "
            f"line {below}, whose block works on {workset(below)} and never "
            f"touches the hub")


# -------------------------------------------------------------- L4 supplier
# canonical names, so the derived architecture is legible against lane F4's
OWNER_NAME = {0: "U07", 1: "U1", 3: "W3", 4: "U4"}


def owner_name(j):
    return OWNER_NAME.get(j, f"S{j}W")


def iface_name(k):
    """the committed set produced for tap k's plane."""
    return {1: "Q1", 3: "Q27", 4: "D37"}.get(k, f"P{k}")


def supplier_of(k):
    """(kind, block-name) for tap k's plane.  kind is 'merged' or 'dedicated'."""
    below = PARENT[k]
    if tuple(workset(below)) == plane_of(k):
        return "merged", owner_name(below)
    a, b = plane_of(k)
    return "dedicated", f"B{a}{b}"


def architecture():
    """DERIVE the whole block architecture.  Returns an ordered list of
    {name, lines, sector, produces_iface:[tap...]} plus the interface map."""
    blocks = {}
    for j in range(8):
        blocks[owner_name(j)] = {"name": owner_name(j), "lines": list(workset(j)),
                                 "sector": j, "produces": []}
    iface = {}
    for k in TAPS:
        kind, who = supplier_of(k)
        if kind == "dedicated" and who not in blocks:
            blocks[who] = {"name": who, "lines": list(plane_of(k)),
                           "sector": None, "produces": []}
        blocks[who]["produces"].append(k)
        iface[k] = {"tap": k, "name": iface_name(k), "plane": list(plane_of(k)),
                    "supplier": who, "supplier_kind": kind,
                    "shared": plane_is_shared(k),
                    "consumers": sorted(b["name"] for b in blocks.values()
                                        if b["sector"] is not None
                                        and set(plane_of(k)) <= set(b["lines"])
                                        and b["name"] != who)}
    # L5 consumers: recompute now that every block exists
    for k in TAPS:
        who = iface[k]["supplier"]
        iface[k]["consumers"] = sorted(
            b["name"] for b in blocks.values()
            if b["sector"] is not None and b["name"] != who
            and set(plane_of(k)) <= set(b["lines"]))
    return blocks, iface


def block_order():
    """Dependency order: a block must run after every block that supplies a
    value it consumes (L5).  Derived by topological sort, not tabulated."""
    blocks, iface = architecture()
    dep = {n: set() for n in blocks}
    for k, info in iface.items():
        for c in info["consumers"]:
            dep[c].add(info["supplier"])
    # deterministic Kahn: prefer interface blocks, then low sector index
    def rank(n):
        b = blocks[n]
        return (0 if b["sector"] is None else 1,
                b["sector"] if b["sector"] is not None else 0, n)
    out, done = [], set()
    while len(out) < len(blocks):
        ready = sorted((n for n in blocks if n not in done and dep[n] <= done),
                       key=rank)
        if not ready:
            raise RuntimeError("cyclic architecture")
        out.append(ready[0])
        done.add(ready[0])
    return _lane_order(out, dep)


# ---------------------------------------------------- lane ORDER (fleet12)
SPINE_NAMES = ("B27", "B37", "U07", "U1", "W3", "U4")
_LANE_ORDER_SAID = [False]


def _lane_order(shipped, dep):
    """lane ORDER (fleet12): audit rows R39/R40, the rank-5 axis.

    The order this function returns is the ONE object that decides both the
    execution order of the blocks (`engine.py:88`) and, through it, what
    `engine._auto_supply` (law L5, `engine.py:57-68`) finds already built when
    each block solves -- hence each block's free supply, hence its exact
    instance and possibly its exact price.  Everything about that order beyond
    the four forced dependency edges is decided by the hand-written tie-break
    `rank()` above (R39), and the assertion at the bottom of `selftest()` (R40)
    pins the one it happens to produce out of 75 legal spine orders.

        LANE_ORDER="B27,B37,U4,W3,U07,U1"     one of the 75

    The six spine SLOTS of the shipped order are refilled left to right with
    the requested spine order; the four S-blocks, which carry no dependency
    edge at all, keep their shipped slots.  The shipped spine order therefore
    maps to the shipped full order exactly.

    REFUSAL, not silent repair: the requested order is validated against `dep`
    -- the dictionary this function's caller just built from
    `architecture()`, not a typed-in copy of the audit's four edges -- on the
    spine and again on the assembled ten-block order.  An order that violates
    a forced edge exits loudly and no CNF is generated.

    When LANE_ORDER is unset or empty this returns its argument unchanged and
    the module behaves byte-identically to the shipped one.
    """
    spec = os.environ.get("LANE_ORDER", "").strip()
    if not spec:
        return shipped
    want = [x.strip() for x in spec.split(",") if x.strip()]
    spine = [n for n in shipped if n in SPINE_NAMES]
    if sorted(want) != sorted(spine):
        raise SystemExit(f"LANE_ORDER: want a permutation of {spine}, "
                         f"got {want}.  REFUSED.")
    pos = {n: i for i, n in enumerate(want)}
    for n in want:
        for d in dep[n]:
            if d in pos and pos[d] >= pos[n]:
                raise SystemExit(
                    f"LANE_ORDER: {d} supplies {n} (a forced edge), so it must "
                    f"strictly precede it; in {want} it does not.  REFUSED, "
                    f"not attempted.")
    it = iter(want)
    out = [next(it) if n in SPINE_NAMES else n for n in shipped]
    fpos = {n: i for i, n in enumerate(out)}
    for n, ds in dep.items():
        for d in ds:
            if fpos[d] >= fpos[n]:
                raise SystemExit(
                    f"LANE_ORDER: assembled order {out} violates the forced "
                    f"edge {d} -> {n}.  REFUSED, not attempted.")
    if not _LANE_ORDER_SAID[0]:
        _LANE_ORDER_SAID[0] = True
        print(f"  LANE_ORDER: block order {shipped} -> {out}", flush=True)
    return out


# ---------------------------------------------------- L5 free-supply predicate
def is_free_to(value, block_lines):
    """L5: an already-built value is free to a block iff its support lies
    inside the block's working line-set."""
    return support(value) <= set(block_lines)


# -------------------------------------------- the conservation law, as a proof
def conservation_statement():
    """The REPLAY BOUND, stated in derived terms rather than as a constant.

    For a shared plane P(k) with supplier block S and consumer block C:
    S's inputs are raws+currency on P(k), and C's workset contains P(k), so C
    has every one of S's inputs.  Therefore C can replay S's entire program
    verbatim, giving
            price(S, any commitment) + price(C, that commitment)
                                          >=  price(C, no commitment at all).
    The right-hand side is ONE exact solve and bounds the sum for EVERY
    commitment, of any rank, cardinality or gate cost.  That is why the tool
    never tries to re-choose a shared plane to save gates upstream.
    """
    out = []
    for k in shared_taps():
        kind, S = supplier_of(k)
        if kind != "dedicated":
            continue
        for C in architecture()[1][k]["consumers"]:
            out.append({"tap": k, "supplier": S, "consumer": C,
                        "claim": f"{S} + {C}(committed) >= {C}(no {iface_name(k)})"})
    return out


# ------------------------------------------------------------------ selftest
def selftest(verbose=True):
    assert TAPS == [1, 3, 4]
    assert CLEAN == [0, 2, 5, 6, 7]
    # L1
    assert workset(0) == (0, 7) and workset(1) == (0, 1, 7)
    assert workset(2) == (1, 2) and workset(3) == (2, 3, 7)
    assert workset(4) == (3, 4, 7) and workset(5) == (4, 5)
    assert workset(6) == (5, 6) and workset(7) == (6, 7)
    # L1 corollary
    for j in range(8):
        if j == 7:
            continue          # line 7 IS the hub; no plane sits above it
        assert touches_hub(j) == (j in TAPS or j == ROOT_LINE), j
    # and no tap's plane ever sits above the hub, so the exclusion is harmless
    assert all(PARENT[k] != 7 for k in TAPS)
    # L2 / L3
    assert plane_of(1) == (0, 7) and plane_of(3) == (2, 7) and plane_of(4) == (3, 7)
    assert unshared_taps() == (3,), unshared_taps()
    assert shared_taps() == (1, 4)
    # L4
    assert supplier_of(1) == ("merged", "U07")
    assert supplier_of(3) == ("dedicated", "B27")
    assert supplier_of(4) == ("dedicated", "B37")
    # the architecture must reproduce lane F4's ten blocks and its ORDER
    blocks, iface = architecture()
    assert set(blocks) == {"U07", "U1", "W3", "U4", "S2W", "S5W", "S6W", "S7W",
                           "B27", "B37"}, sorted(blocks)
    order = block_order()
    assert set(order) == set(blocks) and len(order) == len(blocks)
    # every supplier strictly precedes every consumer (this is what is
    # load-bearing; the position of the four independent clean sectors is a
    # free tie and the emitted MASK SET does not depend on it, because
    # min_depth_schedule re-derives the schedule from the set alone)
    pos = {n: i for i, n in enumerate(order)}
    for k, info in iface.items():
        for c in info["consumers"]:
            assert pos[info["supplier"]] < pos[c], (k, info["supplier"], c)
    # ---- lane LIB (fleet12): audit row R40, THE TRAP ROW -------------------
    # This line used to read
    #     assert spine == ["B27","B37","U07","U1","W3","U4"], spine
    # i.e. it asserted that the DERIVED order EQUALS the one lane F4 wrote by
    # hand.  REF-V9 measured what that is worth: the block poset has FOUR
    # forced edges and **75** legal linear extensions, and which one comes out
    # is decided by the hand-written tie-break at `rank()` above, whose last
    # component is the block NAME STRING (`B27 < B37` because `2 < 3`).
    # Whether that key was written first or tuned until this assertion passed
    # is unrecoverable from the code -- so the agreement is ~1/75 evidence and
    # the assertion asserted more than the package knows.
    # What the package DOES know, and all it knows, is the dependency relation
    # it derived itself from `architecture()`: every supplier precedes every
    # consumer.  That is what is now asserted, against the derived edges.
    spine = [n for n in order if n in SPINE_NAMES]
    dep = {n: set() for n in blocks}
    for k, info in iface.items():
        for c in info["consumers"]:
            dep[c].add(info["supplier"])
    spos = {n: i for i, n in enumerate(spine)}
    for n in spine:
        for d in dep[n]:
            if d in spos:
                assert spos[d] < spos[n], (d, "must precede", n, spine)
    # NOTE (recorded, deliberately NOT asserted): the shipped tie-break does
    # reproduce lane F4's ORDER, and `fleet12/laneORDER` then priced the whole
    # axis -- all 75 legal spine orders were run, EVERY one prices 88, every
    # block was handed a byte-identical instance in all 75, and all 75 emitted
    # the byte-identical circuit.  So this order is one of 75, it is the one
    # lane F4 chose, and the choice is measured at zero gates.
    _f4_order = list(SPINE_NAMES)
    if verbose:
        print(f"  spine order: {spine}"
              + ("  (== lane F4's ORDER; 1 of 75 legal, priced identical"
                 " by fleet12/laneORDER)" if spine == _f4_order
                 else "  (a legal order other than lane F4's)"))
    # L5: THE RULE, derived.  D37 reaches BOTH W3 and U4; Q27 reaches only W3.
    assert iface[4]["consumers"] == ["U4", "W3"], iface[4]["consumers"]
    assert iface[3]["consumers"] == ["W3"], iface[3]["consumers"]
    assert iface[1]["consumers"] == ["U1"], iface[1]["consumers"]
    # every sector target really is inside its owner's workset
    for j in range(8):
        for t in sector_targets(j):
            assert support(t) <= set(workset(j)), (j, t)
    if verbose:
        print("laws selftest OK — all of the following are DERIVED from")
        print("theory.py (GF(2^8) + 0x11B + FIPS-197), nothing tabulated:\n")
        print("  L0  taps (tau_k = 1)           :", TAPS, " clean:", CLEAN)
        print("  L1  worksets                   :",
              {j: workset(j) for j in range(8)})
        for k in TAPS:
            print("  L3 ", why_shared(k))
        print("  L3  => UNIQUE unshared tap     :", unshared_taps())
        for k in TAPS:
            kind, who = supplier_of(k)
            print(f"  L4  tap {k} plane {plane_of(k)} -> {kind:9s} supplier "
                  f"{who:4s} (the set called {iface_name(k)})")
        for k in TAPS:
            print(f"  L5  {iface_name(k):4s} support {plane_of(k)} is free to "
                  f"{iface[k]['consumers']}"
                  + ("   <-- THE SHARED-PLANE RULE" if len(iface[k]['consumers']) > 1 else ""))
        print("  L4/L5 derived block order      :", block_order())
        print("\n  conservation (replay-bound) claims this architecture implies:")
        for c in conservation_statement():
            print("   ", c["claim"])
    return True


if __name__ == "__main__":
    selftest()
