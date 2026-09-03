#!/usr/bin/env python3
"""live.py — a watchable, STREAMING view of the generator working.

    python3 generate.py --count 88 --depth 5 --live
    python3 generate.py --count 88 --depth 5 --live=json | jq -c .

This is PRESENTATION, not computation.  It adds no solves, changes no result,
and -- this is a hard rule -- **never touches the ledger**.  The ledger stays
the single source of truth; this is a view of the same events.  When `--live`
is absent, `emit()` returns on its first line and the cost is one comparison
per event.

Five things are streamed, in the order they actually happen:

  1. THE DERIVATION      taps appearing, each block's workset, the sharing
                         predicate FIRING value by value, the supplier
                         assignment, and the topological order.  This is the
                         part that makes the algorithm legible: you watch the
                         three gates being DERIVED rather than configured.
  2. EACH BLOCK SOLVING  the bound climbing live -- k=6 UNSAT 0.3s / k=7 UNSAT
                         2.1s / k=8 SAT -- with the block's name, dimension,
                         and whether it is WARM (cache hit) or COLD.
  3. THE MASK SET        a running gate count and the model price so far
                         against the target.
  4. THE DEPTH SCHEDULE  levels resolving in the level-BFS, ending in the
                         achieved depth.
  5. THE VERIFICATIONS   in-process and the fresh subprocess, with the verdict.

Modes: "text" (default) is plain stdout, flushed per line, so it survives
`tee`, `|` and redirection with no curses dependency.  "json" emits one JSON
object per line so the stream can drive other tools.
"""
import json, sys, time

_MODE = None
_T0 = None
_STATE = {"gates": 0, "price": 0, "target": None}

C = {"dim": "\033[2m", "b": "\033[1m", "g": "\033[32m", "y": "\033[33m",
     "c": "\033[36m", "r": "\033[31m", "0": "\033[0m"}


def configure(mode, color=None):
    """mode: None (off) | "text" | "json"."""
    global _MODE, _T0
    _MODE = mode
    _T0 = time.monotonic()
    if mode and (color is False or (color is None and not sys.stdout.isatty())):
        for k in C:
            C[k] = ""


def on():
    return _MODE is not None


def _el():
    return time.monotonic() - _T0 if _T0 else 0.0


def emit(kind, text=None, **fields):
    """The whole cost when live is off is this first line."""
    if _MODE is None:
        return
    if _MODE == "json":
        row = {"t": round(_el(), 3), "event": kind}
        row.update(fields)
        sys.stdout.write(json.dumps(row, default=str) + "\n")
    elif text is not None:
        sys.stdout.write(f"{C['dim']}{_el():7.2f}s{C['0']} {text}\n")
    sys.stdout.flush()


# ------------------------------------------------------------ 1. derivation
def narrate_derivation():
    """Stream the derivation of the architecture from theory alone."""
    if _MODE is None:
        return
    import laws
    from theory import TAPS, CLEAN, PARENT, QLINES
    emit("phase", f"{C['b']}== 1. DERIVATION =={C['0']}  "
                  f"(from GF(2^8), 0x11B and FIPS-197 only)", phase="derivation")
    emit("taps", f"  dual xtime chain 2*d_k = d_(k-1) + tau_k*d_7 ; tau IS the "
                 f"reduction polynomial", taps=list(TAPS), clean=list(CLEAN))
    emit("taps2", f"  -> TAPS {C['c']}{TAPS}{C['0']}   CLEAN {CLEAN}",
         taps=list(TAPS))
    for j in range(8):
        w = laws.workset(j)
        emit("workset", f"  L1  line {j}: block {laws.owner_name(j):4s} must work "
                        f"on {C['c']}{list(w)}{C['0']}"
                        f"{'   (touches the hub)' if 7 in w and j != 7 else ''}",
             line=j, block=laws.owner_name(j), workset=list(w))
    for k in TAPS:
        pl = laws.plane_of(k)
        below = PARENT[k]
        sh = laws.plane_is_shared(k)
        emit("plane", f"  L2  tap {k}: q-carrier plane = {C['c']}{list(pl)}{C['0']}",
             tap=k, plane=list(pl))
        emit("predicate",
             f"  L3  is {list(pl)} inside workset({below}) = "
             f"{list(laws.workset(below))} ?  "
             + (f"{C['g']}YES -> SHARED{C['0']}" if sh
                else f"{C['y']}NO -> UNSHARED{C['0']}"),
             tap=k, below=below, shared=bool(sh))
    emit("unshared", f"  L3  => unique unshared tap: "
                     f"{C['b']}{list(laws.unshared_taps())}{C['0']}",
         unshared=list(laws.unshared_taps()))
    for k in TAPS:
        kind, who = laws.supplier_of(k)
        emit("supplier", f"  L4  tap {k} plane {list(laws.plane_of(k))} -> "
                         f"{kind:9s} supplier {C['c']}{who:4s}{C['0']} "
                         f"(the set called {laws.iface_name(k)})",
             tap=k, supplier=who, supplier_kind=kind,
             iface=laws.iface_name(k))
    _blocks, iface = laws.architecture()
    for k in TAPS:
        cons = iface[k]["consumers"]
        mark = (f"   {C['b']}<-- THE SHARED-PLANE RULE, DERIVED{C['0']}"
                if len(cons) > 1 else "")
        emit("free_supply",
             f"  L5  {laws.iface_name(k):4s} support {list(laws.plane_of(k))} "
             f"is free to {C['c']}{cons}{C['0']}{mark}",
             iface=laws.iface_name(k), consumers=cons,
             shared_plane_rule=len(cons) > 1)
    emit("order", f"  L4/L5 dependency order (topological sort, not a table):\n"
                  f"        {C['c']}{laws.block_order()}{C['0']}",
         order=laws.block_order())


# --------------------------------------------------------- 2. block solving
def block_start(name, lines, dim, n_free, n_targets, depth, cached):
    emit("block_start",
         f"  {C['b']}{name:5s}{C['0']} lines={str(list(lines)):12s} dim={dim:2d} "
         f"free={n_free:3d} targets={n_targets}  cap={depth}  "
         + (f"{C['g']}WARM (cache hit){C['0']}" if cached
            else f"{C['y']}COLD{C['0']}"),
         block=name, lines=list(lines), dim=dim, n_free=n_free,
         n_targets=n_targets, depth_cap=depth, cached=bool(cached))


def sat_step(name, k, result, seconds):
    col = C['g'] if result == "SAT" else C['dim']
    emit("sat_step",
         f"         k={k:2d}: {col}{result:5s}{C['0']} {seconds:8.2f}s",
         block=name, k=k, result=result, seconds=seconds)


def block_done(name, gates, status, wall, realised_depth=None):
    emit("block_done",
         f"         {C['b']}-> {gates} gates{C['0']} ({status}, {wall}s"
         + (f", realised depth {realised_depth}" if realised_depth is not None
            else "") + ")",
         block=name, gates=gates, status=status, wall=wall,
         realised_depth=realised_depth)


def block_failed(name, status, reason):
    emit("block_failed",
         f"         {C['r']}-> {status}{C['0']}: {reason}",
         block=name, status=status, reason=reason)


# ------------------------------------------------------------- 3. mask set
def maskset(n_gates, price, target=None):
    _STATE.update(gates=n_gates, price=price)
    bar = ""
    if target:
        w = 40
        f = min(w, int(w * n_gates / max(target, 1)))
        bar = f"  [{'#' * f}{'.' * (w - f)}] {n_gates}/{target}"
    emit("maskset",
         f"         mask set: {C['c']}{n_gates}{C['0']} gates, model price "
         f"{price}{bar}",
         n_gates=n_gates, model_price=price, target=target)


# -------------------------------------------------------- 4. depth schedule
def schedule_start():
    emit("phase", f"\n{C['b']}== 4. DEPTH SCHEDULE =={C['0']}  "
                  f"(level-BFS: level L is exactly the masks expressible as an "
                  f"XOR of two masks of level < L)", phase="schedule")


def level(l, n_new, n_remaining):
    emit("level",
         f"  level {l}: {C['c']}{n_new:3d}{C['0']} masks resolve, "
         f"{n_remaining} still unplaced",
         level=l, n_new=n_new, n_remaining=n_remaining)


def schedule_done(depth, n_gates):
    emit("schedule_done",
         f"  {C['b']}-> depth {depth}{C['0']} for {n_gates} gates "
         f"(provably minimal for this mask set)",
         depth=depth, n_gates=n_gates)


# --------------------------------------------------------- 5. verifications
def verify_start():
    emit("phase", f"\n{C['b']}== 5. VERIFICATION (twice, independently) =={C['0']}",
         phase="verify")


def verify_inproc(built, n, ok):
    good = built == 32 and ok
    emit("verify_inproc",
         f"  in-process   : {C['g'] if good else C['r']}{built}/32 targets"
         f"{C['0']} rebuilt from FIPS-197 inside theory.py, structure "
         f"{'ok' if ok else 'BAD'}",
         targets_built=built, n_gates=n, structure_ok=bool(ok))


def verify_subproc(rc, verdict):
    emit("verify_subproc",
         f"  subprocess   : {C['g'] if rc == 0 else C['r']}{verdict}{C['0']} "
         f"(fresh verify_circuit.py, rc={rc})",
         rc=rc, verdict=verdict)


def result(n, depth, price, delta, collisions, path):
    emit("result",
         f"\n  {C['b']}{n} gates @ depth {depth}{C['0']}   "
         f"(model price {price}, delta {-delta:+d})\n  -> {path}",
         emitted=n, depth=depth, model_price=price, delta=delta,
         collisions=collisions, path=str(path))
