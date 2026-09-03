#!/usr/bin/env python3
"""engine.py — THE one assembler.

Walks a `Plan` (any regime), solves each block through THE one solver
interface, replays every witness into one global mask set, and schedules that
set at its provably minimum depth.

CHARTER ITEM 3 -- DEPTH IS A CONSTRAINT, NOT A CHECK.
In `fleet2/laneG_generator/generate.py` the `--depth` argument is accepted by
`plan_ladder(count, depth, ...)` and then never used; the only thing that ever
looks at it is a post-emit comparison, which is why asking for <= 4 could emit
depth 5 and asking for <= 3 could emit depth 6.  Here the cap reaches the
model: currency is chosen by the exact gates-vs-depth curve so every currency
value's ARRIVAL LEVEL is known, every block program is chosen by the exact
minimum-gates-under-a-depth-cap oracle with its inputs at their true levels and
its targets capped, and interface levels are explicit.  If any block is
infeasible under the cap the run FAILS LOUDLY, naming the block and the reason
(`InfeasibleAtDepth`), and never emits a circuit that misses the request.

Soundness of the emitted depth: every block program respects the cap when its
inputs are taken at the levels quoted to it; those levels are witness levels,
which upper-bound the levels the final level-BFS assigns.  So a schedule of
depth <= D exists for the emitted set, and `min_depth_schedule` returns the
MINIMUM, which is therefore <= D.
"""
import os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from theory import mask_to_lines, lines_to_mask, support
from algebra import unpack, hexlines
from assemble import MaskSet, min_depth_schedule
from solver import solve_block
from ledger import log


class InfeasibleAtDepth(Exception):
    """A block cannot meet the requested cap.  Carries the block-level reason
    so the failure is diagnostic rather than a bare 'no'."""

    def __init__(self, block, reason, detail=None):
        self.block, self.reason, self.detail = block, reason, detail
        super().__init__(f"block {block}: {reason}"
                         + (f" [{detail}]" if detail else ""))


class Undecided(Exception):
    """A block solve timed out.  UNDECIDED is not REFUTED -- this must never
    be reported as infeasibility."""

    def __init__(self, block, lb=None, seconds=None):
        self.block, self.lb, self.seconds = block, lb, seconds
        super().__init__(f"block {block}: UNDECIDED (timeout after {seconds}s"
                         + (f", lower bound proven {lb}" if lb else "") + ")")


class SolverFailed(Exception):
    """lane LIB (fleet12), audit defect D1, severity 1.

    THE SOLVER DID NOT ANSWER.  A crash (`status:"error"`), or any status this
    file does not recognise, or a record with no witness and no negative
    status.  It is NOT infeasibility and it is NOT a timeout: it is a broken
    instrument, and it gets its own exception and its own exit code (7) so it
    can never be published as *"a block is provably infeasible"*.

    `solver.py:159-163` is careful never to CACHE a crash as a fact; before
    this class existed `engine.py` published it as a proof one file later,
    because `status:"error"` matched none of the handled branches and fell
    through to `raise InfeasibleAtDepth`."""

    def __init__(self, block, status, detail=None):
        self.block, self.status, self.detail = block, status, detail
        super().__init__(f"block {block}: SOLVER FAILED ({status})"
                         + (f" [{detail}]" if detail else ""))


def _auto_supply(ms, lines, exclude=()):
    """LAW L5: every already-built value whose support lies inside the block's
    working line-set, at its witness arrival level.  This is what makes the
    shared plane shared; there is no special case for D37 anywhere."""
    Ls = set(lines)
    ex = {tuple(v) for v in exclude}
    out = []
    for m in ms.order:
        v = mask_to_lines(m)
        if support(v) <= Ls and any(v) and v not in ex:
            out.append((v, ms.lvl[m]))
    return out


def assemble(plan, D=None, cores=8, timeout=1800, lb_hints=None, tag=None,
             verbose=True, collect=None):
    """Returns (ms, terms, price, rows).  If `collect` is a list, every block's
    (name, instance, record) is appended to it -- used by the cap-off control,
    which needs the REAL instances rather than toys."""
    ms = MaskSet()
    terms, rows = {}, []
    lb_hints = lb_hints or {}

    if plan.closed is not None:                     # the naive regime
        info = plan.closed(ms)
        terms.update(info["terms"])
        return ms, terms, sum(terms.values()), rows

    if plan.prelude is not None:
        terms.update(plan.prelude(ms)["terms"])

    for b in plan.blocks:
        if not b.targets:
            terms[b.name] = 0
            continue
        # ---- free supply -------------------------------------------------
        if b.supply == "auto":
            free = _auto_supply(ms, b.lines)
        elif isinstance(b.supply, tuple) and b.supply[0] == "auto_except":
            free = _auto_supply(ms, b.lines, exclude=b.supply[1])
        else:
            free = []
            for v in b.supply:
                mk = lines_to_mask(tuple(v))
                if mk not in ms.have:
                    raise SystemExit(f"block {b.name}: restricted supply value "
                                     f"{hexlines(v)} was never built")
                free.append((tuple(v), ms.lvl[mk]))
        # ---- solve -------------------------------------------------------
        import live
        _pre = None
        if live.on():
            _inst_peek = __import__("solver").make_instance(b.lines, free,
                                                            b.targets, D)
            # lane LIB (D3): the peek must use the SAME key the solve will use
            _k = __import__("solver").key_of(_inst_peek,
                                             lb_hints.get(b.name), None)
            _pre = _k in __import__("solver")._cache()
            live.block_start(b.name, b.lines, _inst_peek["dim"],
                             len(_inst_peek["inputs"]),
                             len(_inst_peek["targets"]), D, _pre)
        rec, inst = solve_block(b.name, b.lines, free, b.targets, depth=D,
                                lb_hint=lb_hints.get(b.name), timeout=timeout,
                                cores=cores, tag=tag,
                                on_level=((lambda k, r, sec: live.sat_step(b.name, k, r, sec))
                                          if live.on() and not _pre else None))
        if live.on():
            if rec.get("min_gates") is None:
                live.block_failed(b.name, rec.get("status"), rec.get("reason"))
            else:
                live.block_done(b.name, rec["min_gates"], rec["status"],
                                rec["wall"], rec.get("realised_depth"))
        if collect is not None:
            collect.append((b.name, inst, rec))
        st = rec["status"]
        # lane LIB (fleet12), audit D1/D5: this switch is exhaustive and its
        # DEFAULT is loud.  Exactly three statuses are NEGATIVES; a crash and
        # an exhausted default loop are not among them.
        if st in ("infeasible_depth", "infeasible_span"):
            raise InfeasibleAtDepth(b.name, st, rec.get("reason"))
        if st == "timeout":
            raise Undecided(b.name, rec.get("lower_bound_proven"), rec.get("wall"))
        if st == "capped_unsat":
            # a CALLER-SET gate cap: "no program at or below max_gates" really
            # is a proof of what was asked (dslp.py sets this status only when
            # `max_gates` was supplied).
            raise InfeasibleAtDepth(b.name, "capped_unsat",
                                    f"no program at or below the gate cap; "
                                    f"lower bound proven "
                                    f"{rec.get('lower_bound_proven')}")
        if st == "undecided_gate_cap":
            # D5: dslp's DEFAULT `hi = 64` ran out.  A loop bound is not a
            # proof of impossibility -- it is a bracket, and it is UNDECIDED.
            raise Undecided(b.name, rec.get("lower_bound_proven"), rec.get("wall"))
        if st == "error":
            raise SolverFailed(b.name, "error", rec.get("error"))
        if st != "exact" or rec.get("slp") is None:
            raise SolverFailed(b.name, st or "no status",
                               rec.get("reason") or "no witness returned")
        # ---- replay into the global mask set -----------------------------
        sig = []
        for v in rec["in_vals"]:
            mk = lines_to_mask(unpack(v, inst["lines"]))
            if mk not in ms.have:
                raise SystemExit(f"block {b.name}: free input {hex(v)} was "
                                 f"never built -- dependency order is wrong")
            sig.append(mk)
        for a, bb in rec["slp"]:
            sig.append(ms.add(sig[a], sig[bb], b.name))
        for v, _cap in b.targets:
            assert lines_to_mask(tuple(v)) in ms.have, (b.name, hexlines(v))
        terms[b.name] = rec["min_gates"]
        if live.on():
            live.maskset(ms.n_gates(), sum(terms.values()), live._STATE.get("target"))
        rows.append({"block": b.name, "lines": list(b.lines),
                     "gates": rec["min_gates"], "status": st, "cap": D,
                     "dim": rec["dim"], "n_free": rec["n_inputs"],
                     "target_caps": rec["target_caps"],
                     "realised_depth": rec.get("realised_depth"),
                     "wall": rec["wall"], "cached": rec.get("cached", False)})
        if verbose:
            print(f"    {b.name:5s} lines={list(b.lines)} -> {rec['min_gates']:3d} "
                  f"gates  ({st}, {rec['wall']}s"
                  f"{', cached' if rec.get('cached') else ''})", flush=True)
    price = sum(terms.values())
    return ms, terms, price, rows


def price_only(plan, D=None, cores=8, timeout=1800, lb_hints=None, tag=None):
    """Price a plan WITHOUT assembling: used by the interface-level scheduler
    and the reachability map, where thousands of prices are wanted and most
    will never be emitted.  Returns (price, terms, rows) or raises."""
    ms, terms, price, rows = assemble(plan, D, cores, timeout, lb_hints, tag,
                                      verbose=False)
    return price, terms, rows
