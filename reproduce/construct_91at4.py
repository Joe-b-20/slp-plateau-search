#!/usr/bin/env python3
"""construct_91at4.py — build a verified 91-gate, depth-4 MixColumns circuit
by exact construction, in a few seconds.

    python3 construct_91at4.py                 # writes construct91_out.json
    python3 construct_91at4.py --out FILE
    python3 construct_91at4.py --keep-cache DIR   # reuse solves across runs

OPTIONAL DEPENDENCIES — this is the one script in `reproduce/` that is not
standard-library Python. It needs

    numpy        (array bookkeeping inside the block solver)
    python-sat   (`pip install python-sat`; the SAT back end the block solver
                  calls, via `pysat.solvers`)

and it exits with a named message if either is missing. Everything else in
`reproduce/` remains stdlib-only; that contract is why this route had no
command here until now.

WHAT IT DOES

The other records in `reproduce/` are re-*searched*. This one is not searched
at all. The ladder model prices a family of MixColumns constructions from the
field: eight sector blocks, each solved exactly for its minimum gate count
under a depth cap, plus a currency and diagonal prelude. Its optimum is
exactly 91 gates, so asking the model for 91 at depth 4 either emits one or
fails loudly. The eight block solves are the only expensive step, and they
take about a second in total from an empty cache.

The optimum of that model class is 91. That is not a lower bound on
MixColumns and says nothing about whether 90 @ depth 4 exists.

FROM SCRATCH

Targets come from GF(2^8) and FIPS-197 through `construct91/theory.py`, which
reads no file. No record circuit, and no data derived from a record circuit,
is opened at any point: the record-read currency menus that the working tree's
generator imports live in `cells.py`, which this driver does not import.

What is inherited is one configuration — the eight currency shapes and three
diagonal menus below — which is the result of an exact DP over the ladder
configuration space. The DP is theory-generated; every block it names is
re-solved from scratch here before anything is emitted, so only the search
over configurations is inherited, not any circuit.

WHAT IT PRODUCES

Not the shipped record circuit: an independent circuit at the same frontier
point, sharing 53 of its 91 masks with the shipped 91 @ 4. It reproduces the
claim, not the artifact.

PROVENANCE OF THE CODE

`construct91/` is the working tree's `fleet8/unified/code/`, vendored. The
modules are copies; `ledger.py` is a replacement that writes nothing unless
`SLP_LEDGER` names a file, so this package never writes inside the repository.
"""
import argparse, json, os, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "construct91")
REPO = os.path.dirname(HERE)
VERIFY = os.path.join(REPO, "verify_circuit.py")

# The ladder configuration priced at 91 by the exact DP over the model's
# configuration space. `C[line]` is that line's currency shapes; `D[tap]` is
# that tap's diagonal menu.
LADDER_91 = {
    "C": [[2, 10, 12], [4, 6, 12, 14], [2, 4, 10], [2, 10, 12],
          [6, 12, 14], [4, 6, 14], [2, 4, 10], [2, 4, 10, 12]],
    "D": {"1": [2, 10, 12], "3": [2, 4, 10], "4": [2, 10, 12]},
    "price": 91,
}


def require_deps():
    missing = []
    try:
        import numpy  # noqa: F401
    except ImportError:
        missing.append("numpy")
    try:
        from pysat.solvers import Solver  # noqa: F401
    except ImportError:
        missing.append("python-sat  (pip install python-sat)")
    if missing:
        sys.stderr.write(
            "construct_91at4.py needs two packages this folder otherwise does "
            "without:\n  " + "\n  ".join(missing) + "\n"
            "Every other command in reproduce/ is standard-library only.\n")
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=os.path.join(HERE, "construct91_out.json"))
    ap.add_argument("--depth", type=int, default=4)
    ap.add_argument("--cores", type=int, default=1)
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--keep-cache", default=None,
                    help="directory for the block-solve cache; without it the "
                         "cache is temporary and every run solves cold")
    a = ap.parse_args()
    require_deps()

    tmp = None
    if a.keep_cache:
        os.makedirs(a.keep_cache, exist_ok=True)
        cache = os.path.join(a.keep_cache, "solve_cache.jsonl")
    else:
        tmp = tempfile.TemporaryDirectory(prefix="construct91_")
        cache = os.path.join(tmp.name, "solve_cache.jsonl")
    os.environ["SLP_SOLVE_CACHE"] = cache

    sys.path.insert(0, PKG)
    import plan as P, engine
    from assemble import (min_depth_schedule, strip_dead_gates, circuit_stats,
                          verify_inprocess)

    t0 = time.monotonic()
    pl = P.ladder_plan(LADDER_91, a.depth)
    print(f"  ladder model, depth cap {a.depth}, cache "
          f"{'kept' if a.keep_cache else 'cold'}")
    ms, terms, price, rows = engine.assemble(
        pl, a.depth, a.cores, a.timeout, lb_hints={}, tag="construct91")

    gates, depth, _order = min_depth_schedule(ms.order)
    gates, n_dead = strip_dead_gates(gates)
    if n_dead:
        depth = circuit_stats(gates)[1]
    built, n, struct_ok = verify_inprocess(gates)
    wall = time.monotonic() - t0

    json.dump({"n_inputs": 32, "gates": gates,
               "meta": {"tool": "reproduce/construct_91at4.py",
                        "model": "ladder", "model_price": price,
                        "depth_cap": a.depth, "dead_gates_removed": n_dead}},
              open(a.out, "w"))

    print(f"  model price   : {price}")
    print(f"  emitted count : {n}")
    print(f"  in-process    : {built}/32 targets, structure "
          f"{'ok' if struct_ok else 'BAD'}")
    print(f"  wall          : {wall:.1f} s")
    print(f"  -> {a.out}")

    p = subprocess.run([sys.executable, VERIFY, a.out, str(a.depth)],
                       capture_output=True, text=True)
    print("\n".join("  " + l for l in p.stdout.strip().splitlines()[-4:]))
    ok = (p.returncode == 0 and built == 32 and struct_ok and n == 91
          and depth == a.depth)
    print(f"\n  {'OK' if ok else 'FAILED'}  {n} gates @ depth {depth}")
    if tmp:
        tmp.cleanup()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
