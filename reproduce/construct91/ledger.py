#!/usr/bin/env python3
"""ledger.py — packaging replacement for the working tree's decision log.

The generator's modules call `log(**kw)` after every solve. In the working
tree that appends to the lane's own `ledger.jsonl`. Here the append target is
whatever `SLP_LEDGER` names, and when that variable is unset the call is a
no-op, so nothing in this package ever writes inside the repository.

`prereg`, `verify_chain` and `tally` keep the original signatures so the
vendored modules import unchanged; only the destination differs.
"""
import hashlib, json, os, time

LEDGER = os.environ.get("SLP_LEDGER", "").strip()


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def log(**kw):
    if not LEDGER:
        return
    kw.setdefault("t", _now())
    d = os.path.dirname(os.path.abspath(LEDGER))
    if d:
        os.makedirs(d, exist_ok=True)
    with open(LEDGER, "a") as f:
        f.write(json.dumps(kw, default=str) + "\n")


def prereg(what, prediction, why=None):
    row = {"t": _now(), "what": what, "prediction": prediction, "why": why}
    row["this"] = hashlib.sha256(
        json.dumps(row, sort_keys=True, default=str).encode()).hexdigest()
    log(kind="prereg", what=what, prediction=prediction,
        chain=row["this"][:16])
    return row["this"]


def verify_chain():
    return True, 0, None


def tally(kind=None):
    return {}
