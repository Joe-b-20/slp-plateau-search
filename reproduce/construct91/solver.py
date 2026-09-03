#!/usr/bin/env python3
"""solver.py — THE one solver interface.

Three lanes previously had three: lane G called `atlas/slp_opt.py` through a
subprocess (`modules.solve` / `modules.solve_raw`), lane F4 called the same
binary through its own wrapper (`f4model.solve`), and lane DEPTH called its
own in-process CNF (`dslp.solve_depth`).  Here there is one entry point,

    solve_block(name, lines, free, targets, depth=None, ...)

and the depth cap is an OPTIONAL argument.  With `depth=None` the encoding
emits no level variables at all and the question is exactly the plain
minimal-SLP question that `atlas/slp_opt.py` answers -- an equivalence this
module re-verifies for itself in `capoff_control()` (charter item 1), on the
real block instances rather than on toys.

CACHE HYGIENE (three inherited errata, all honoured here)
--------------------------------------------------------
  * The key CONTAINS THE BLOCK'S LINE LIST.  Lane G's freesupply cache omitted
    it, narrowed U4 from dim 16 to dim 12 mid-session, and silently served the
    dim-16 witness re-indexed against a dim-12 input vector (lane G erratum).
  * An `error` row is NEVER served from cache.  Lane MERGE cached a solve that
    was killed 2 s into a queue cutover and served it back forever.
  * When `depth is None`, every per-target cap is forced to None.  Lane DEPTH's
    erratum E1 was verifying an interface cap against a CNF that had never been
    told to constrain it.
  * A `timeout` row is served only if it was at least as patient as the new
    request, and a timeout is UNDECIDED -- never folded into a negative.
"""
import hashlib, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(LANE))
SLP_OPT = os.path.join(REPO, "atlas", "slp_opt.py")
# lane HINTS (fleet12): the cache path may be redirected by an environment
# variable so that an experiment which changes something NOT in `key_of` -- and
# `lb_hint` and `max_gates` are both missing from it (audit defect D3) -- can be
# run against a fresh bank instead of being served the old answer.  When
# SLP_SOLVE_CACHE is unset this is byte-for-byte the original line.
CACHE = os.environ.get("SLP_SOLVE_CACHE") or os.path.join(
    LANE, "results", "solve_cache.jsonl")
sys.path.insert(0, HERE)

from dslp import solve_depth, verify_depth
from algebra import pack, unpack, hexlines
from theory import support
from ledger import log

_MEM = None


# ------------------------------------------------------------------ instance
def make_instance(lines, free, targets, depth=None):
    """(instance dict) from 8-line values.

    free    : [(value, level)]        level = arrival level of that value
    targets : [(value, cap)]          cap   = the level it must arrive by
    depth   : the block cap, or None for the uncapped question.

    Inputs are de-duplicated keeping the MINIMUM arrival level; targets are
    de-duplicated keeping the TIGHTEST cap.  Packing is ASCENDING-line (lane
    F4's own convention, so agreement with lane F4 / lane G numbers remains a
    genuine cross-check rather than a shared bug).
    """
    L = sorted(lines)
    Ls = set(L)
    seen, I, IL = {}, [], []
    for v, lvl in free:
        if not any(v):
            continue
        assert support(v) <= Ls, f"free value {hexlines(v)} outside lines {L}"
        p = pack(v, L)
        if p in seen:
            if lvl < IL[seen[p]]:
                IL[seen[p]] = lvl
            continue
        seen[p] = len(I)
        I.append(p)
        IL.append(lvl)
    tseen, T, TC = {}, [], []
    for v, cap in targets:
        if not any(v):
            continue
        assert support(v) <= Ls, f"target {hexlines(v)} outside lines {L}"
        # E1: with the cap off, no target may carry a cap.
        c = None if depth is None else cap
        p = pack(v, L)
        if p in tseen:
            i = tseen[p]
            if c is not None and (TC[i] is None or c < TC[i]):
                TC[i] = c
            continue
        tseen[p] = len(T)
        T.append(p)
        TC.append(c)
    return {"dim": 4 * len(L), "lines": L, "inputs": I, "input_levels": IL,
            "targets": T, "target_caps": TC, "depth": depth}


KEY_SCHEMA = "u2"      # bump whenever the KEY's field list changes (see below)


def key_of(inst, lb_hint=None, max_gates=None):
    """Cache key.  THE LINE LIST IS IN THE KEY (lane G erratum).

    lane LIB (fleet12), audit defect D3, severity 1, LIVE: `lb_hint` and
    `max_gates` are ARGUMENTS OF THE SOLVE and were not in the key, so an
    explicitly UNHINTED query was served the HINTED answer -- which is what
    made `check_l5.json`'s ten-block agreement circular.  Both are now in the
    key, and the schema tag is bumped `u1` -> `u2` so that no row written
    under the old key list can ever be matched by a new one.  The shipped
    bank `results/solve_cache.jsonl` stays on disk as readable history; it is
    simply never a hit again.

    KEY COMPLETENESS, argued against `solve_block`/`solve_depth`.  The answer
    (`min_gates`, `status`) is a function of exactly:
      * the instance -- `dim`, `lines`, `inputs`+`input_levels`,
        `targets`+`target_caps`, `depth`: all in the key, and `make_instance`
        derives every one of them from (lines, free, targets, depth);
      * `lb_hint` -- raises `lb_start`, so it decides which k-levels are ever
        tested (dslp.py:510-515).  NOW IN THE KEY;
      * `max_gates` -- sets `hi`, so it decides `capped_unsat`.  NOW IN THE KEY;
      * `timeout` -- handled separately by the patience rule in `solve_block`
        (a `timeout` row is only served to a request no more patient);
      * `solver_name` -- a complete SAT solver, so SAT/UNSAT is independent of
        it, and no caller varies it;
      * `ncores`, `verbose`, `on_level` -- search order and telemetry only.
        They do NOT change `min_gates` (SAT/UNSAT is a property of the
        formula) but they DO change WHICH witness returns (audit D11); the
        cached `slp` is therefore one witness of many, which every consumer
        already re-verifies.
    What is still NOT in the key is a hash of `dslp.py`/`solver.py`/`engine.py`
    (audit defect D4, LATENT): the schema tag is a manual bump, not a
    fingerprint.  Bump `KEY_SCHEMA` by hand when the CNF or the instance
    construction changes.
    """
    return hashlib.sha1(json.dumps(
        [KEY_SCHEMA, inst["lines"], inst["dim"],
         sorted(zip(inst["inputs"], inst["input_levels"])),
         sorted(zip(inst["targets"],
                    [-1 if c is None else c for c in inst["target_caps"]])),
         inst["depth"],
         (None if lb_hint is None else int(lb_hint)),
         (None if max_gates is None else int(max_gates))],
        sort_keys=True).encode()).hexdigest()


def legacy_key_u1(inst):
    """The PRE-lane-LIB cache key (schema `u1`, no `lb_hint`, no `max_gates`).

    Kept as a reading aid, never used to serve: every row in the shipped bank
    `results/solve_cache.jsonl` is keyed this way, and at least one other lane
    PINS such a digest as a refuse-to-run assertion --
    `fleet11/laneCUBE/code/inst16.py` imports `key_of` from this file and
    asserts `f04dcb3ecf180a30204434a0bd32453e7635e8b6` for the merged
    `W3|U4` instance.  After the D3 fix that assertion fails CLOSED (it
    refuses to run; it cannot mis-serve), and a successor resuming that lane
    re-pins with this function or with `key_of`'s new digest."""
    return hashlib.sha1(json.dumps(
        ["u1", inst["lines"], inst["dim"],
         sorted(zip(inst["inputs"], inst["input_levels"])),
         sorted(zip(inst["targets"],
                    [-1 if c is None else c for c in inst["target_caps"]])),
         inst["depth"]], sort_keys=True).encode()).hexdigest()


def _cache():
    global _MEM
    if _MEM is None:
        _MEM = {}
        if os.path.exists(CACHE):
            for line in open(CACHE):
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                _MEM[r["key"]] = r
    return _MEM


def solve_block(name, lines, free, targets, depth=None, max_gates=None,
                lb_hint=None, timeout=1800, cores=8, tag=None, force=False,
                verbose=False, on_level=None):
    """EXACT minimum gates for one block, optionally under a depth cap.

    Returns the cache record; `status` is one of
        exact | capped_unsat | infeasible_depth | infeasible_span
      | timeout | undecided_gate_cap | error
    Only `capped_unsat`, `infeasible_depth` and `infeasible_span` are
    NEGATIVES.  `timeout` is UNDECIDED and carries `lower_bound_proven` when
    lower k-levels were exhaustively UNSAT; `undecided_gate_cap` (lane LIB,
    audit D5) is UNDECIDED too -- dslp's DEFAULT gate ceiling ran out, which
    is a bracket, not a proof; `error` is a CRASH and is never served from
    cache and never a negative (lane LIB, audit D1).
    """
    inst = make_instance(lines, free, targets, depth)
    k = key_of(inst, lb_hint, max_gates)          # lane LIB: D3 -- both in the key
    c = _cache()
    if not force and k in c:
        r = c[k]
        served = True
        if r["status"] == "error":
            served = False                       # lane MERGE erratum
        elif r["status"] == "timeout" and (r.get("timeout") or 0) < 0.8 * timeout:
            served = False                       # be at least as patient
        if served:
            r = dict(r)
            r["cached"] = True
            return r, inst
    t0 = time.monotonic()
    try:
        res = solve_depth(inst["dim"], inst["inputs"], inst["targets"],
                          depth=inst["depth"], in_levels=inst["input_levels"],
                          target_caps=inst["target_caps"], max_gates=max_gates,
                          ncores=cores, timeout=timeout, lb_hint=lb_hint,
                          verbose=verbose, on_level=on_level)
    except Exception as e:                        # never cache a crash as a fact
        rec = {"key": k, "block": name, "status": "error", "min_gates": None,
               "error": repr(e), "wall": round(time.monotonic() - t0, 2)}
        log(kind="solve", block=name, status="error", error=repr(e))
        return rec, inst
    ver = None
    if res.get("slp") is not None:
        # independent replay of the witness before it is ever believed
        ver = verify_depth(res["in_vals"], res["in_levels"], inst["targets"],
                           res["slp"], inst["depth"], inst["target_caps"])
        assert ver[0], f"{name}: witness failed replay: {ver[1]}"
    rec = {"key": k, "block": name, "tag": tag, "lines": inst["lines"],
           "lb_hint": lb_hint, "max_gates": max_gates,   # lane LIB: in the key
           "depth": inst["depth"], "dim": inst["dim"],
           "n_inputs": len(inst["inputs"]), "n_targets": len(inst["targets"]),
           "input_levels": inst["input_levels"],
           "target_caps": inst["target_caps"],
           "status": res["status"], "min_gates": res.get("min_gates"),
           "lower_bound_proven": res.get("lower_bound_proven"),
           "realised_depth": res.get("realised_depth"),
           "reason": res.get("reason"),
           "slp": res.get("slp"), "in_vals": res.get("in_vals"),
           "in_levels": res.get("in_levels"), "lb_start": res.get("lb_start"),
           "timeout": timeout, "wall": round(time.monotonic() - t0, 2),
           "verified": (ver[0] if ver else None), "log": res.get("log")}
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "a") as f:
        f.write(json.dumps(rec) + "\n")
    _cache()[k] = rec
    log(kind="solve", block=name, tag=tag, depth=inst["depth"],
        lines=inst["lines"], status=rec["status"], min_gates=rec["min_gates"],
        lower_bound_proven=rec["lower_bound_proven"], wall=rec["wall"],
        dim=rec["dim"], n_inputs=rec["n_inputs"], n_targets=rec["n_targets"],
        target_caps=rec["target_caps"], verified=rec["verified"], key=k)
    return rec, inst


# -------------------------------------------- the cap-off equivalence control
def slp_opt_reference(inst, timeout=1800, cores=8, tag="ctrl"):
    """Run the repository's own `atlas/slp_opt.py` on the SAME instance with
    no depth information at all.  Independent second implementation."""
    idir = os.path.join(LANE, "inst")
    ldir = os.path.join(LANE, "logs")
    os.makedirs(idir, exist_ok=True)
    os.makedirs(ldir, exist_ok=True)
    payload = {"dim": inst["dim"], "inputs": inst["inputs"],
               "targets": inst["targets"]}
    h = hashlib.sha1(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:12]
    ip = os.path.join(idir, f"ctrl_{tag}_{h}.json")
    op = os.path.join(ldir, f"ctrl_{tag}_{h}.out")
    json.dump(payload, open(ip, "w"))
    t0 = time.monotonic()
    with open(op, "w") as fo:
        # -v is MANDATORY: slp_opt block-buffers under redirection and a killed
        # long solve otherwise loses every completed level.  NEVER pipe it.
        pr = subprocess.Popen([sys.executable, "-u", SLP_OPT, ip,
                               "--cores", str(cores), "--timeout", str(timeout),
                               "-v"],
                              stdout=fo, stderr=subprocess.STDOUT,
                              start_new_session=True)
        pr.wait()
    wall = time.monotonic() - t0
    res = None
    for line in reversed(open(op).read().strip().splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                res = json.loads(line)
                break
            except Exception:
                continue
    return {"min_gates": (res or {}).get("min_gates"), "wall": round(wall, 2),
            "log": os.path.relpath(op, LANE)}


def capoff_control(cases, timeout=1800, cores=8):
    """CHARTER ITEM 1: with the cap switched off, the merged solver must
    reproduce the plain oracle.  `cases` is a list of (name, lines, free,
    targets).  Returns a row per case; agreement is checked, not assumed."""
    rows = []
    for name, lines, free, targets in cases:
        rec, inst = solve_block(name, lines, free, [(t, None) for t in targets],
                                depth=None, timeout=timeout, cores=cores,
                                tag="capoff")
        ref = slp_opt_reference(inst, timeout=timeout, cores=cores, tag=name)
        rows.append({"block": name, "lines": list(inst["lines"]),
                     "dim": inst["dim"], "dslp_capoff": rec.get("min_gates"),
                     "slp_opt": ref["min_gates"],
                     "agree": rec.get("min_gates") == ref["min_gates"],
                     "dslp_wall": rec["wall"], "slp_opt_wall": ref["wall"],
                     "dslp_cached": rec.get("cached", False)})
        log(kind="capoff_control", **rows[-1])
    return rows
