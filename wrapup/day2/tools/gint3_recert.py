#!/usr/bin/env python3
"""S2 — re-certify G_int(3) >= 92 as an INFEASIBILITY, not a solver's best bound.

DOSSIER.md §7.2: the value on the board comes from ONE line of
`fleet6/laneTOOL2/logs/wave3` — CP-SAT status FEASIBLE at 1200 s on 4 cores,
incumbent 94, BestObjectiveBound 92, bracket [92,94].  That is an optimisation
run's dual bound, not an optimality certificate and not an infeasibility.

The referee-checkable form is the DECISION problem:

    is  3*|A| + |Y|  <=  B  feasible over the same universe?
    INFEASIBLE  =>  G_int(3) >= B+1.

This runs a LADDER of such decisions, low B first, appending each verdict to a
jsonl.  Every INFEASIBLE rung is a permanent, independently re-checkable
certificate that survives a reboot; a rung that comes back UNKNOWN costs only
its own time limit.  The target rung is B = 91.

Reuses laneTOOL2's own encoding verbatim (`u1_uncond.solve_G`, ub=B) so the
model is the same object the original number came from -- with `Minimize`
dropped, because a pure decision propagates far better than a bounded optimise.

  python3 gint3_recert.py --bounds 63,79,85,89,91 --timeout 7200 --cores 1
  python3 gint3_recert.py --smoke          # B=40, 8 s, seconds total
"""
import argparse, json, os, sys, time
from fractions import Fraction

ROOT = "/home/joebachir20/xor_ui/slp-plateau-search"
sys.path.insert(0, ROOT + "/fleet6/laneTOOL2/code")
import t2lib as L                                   # noqa: E402
from phi2 import split_pairs                        # noqa: E402
from t2lib import popcount                          # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work",
                   "gint3_recert.jsonl")


# ------------------------------------------------------ the Z/4 byte gauge ---
# t2lib layout: mask bit (byte*8 + bit_index).  rho = rotate the four bytes by
# one.  mixcolumns_targets() builds target (j, out_bit) from input bytes
# (j+k)%4, so rho carries target (j,out_bit) to target ((j+1)%4, out_bit): the
# target SET is preserved, hence so is U (submasks of targets) and so is the
# split structure (split_pairs is bitwise, hence equivariant under any bit
# permutation).  LEADS #45 / beat88 U-10 / fleet5_8 L6: this gauge is completely
# unbroken in the G_int encodings -- every solution comes in an orbit of up to 4.
def rho(m):
    out = 0
    for byte in range(4):
        out |= ((m >> (byte * 8)) & 0xFF) << (((byte + 1) % 4) * 8)
    return out


def rho_pow(m, k):
    for _ in range(k % 4):
        m = rho(m)
    return m


def gauge_check(targets):
    """Pure-arithmetic prerequisites for soundness of the lex-leader cut.
    Returns (ok, dict-of-findings).  No solver involved."""
    U = set(L.universe(targets))
    T = set(targets)
    f = {}
    f["rho^4 == id"] = all(rho_pow(m, 4) == m for m in U)
    f["rho(TARGETS) == TARGETS"] = {rho(t) for t in T} == T
    f["rho(U) == U"] = {rho(m) for m in U} == U
    f["rho preserves popcount"] = all(popcount(rho(m)) == popcount(m) for m in U)
    bad = 0
    for m in U:
        want = {tuple(sorted((rho(s1), rho(s2)))) for s1, s2 in split_pairs(m)}
        got = {tuple(sorted(p)) for p in split_pairs(rho(m))}
        if want != got:
            bad += 1
    f["split_pairs equivariant (all %d masks)" % len(U)] = (bad == 0)
    f["orbit sizes"] = sorted({len({rho_pow(m, k) for k in range(4)}) for m in U})
    return all(v is True for k, v in f.items() if k != "orbit sizes"), f


def gauge_vector(U, a, y):
    """The indicator vector the lex-leader constraint orders: a-block then
    y-block, both over sorted(U)."""
    return [a[m] for m in U] + [y[m] for m in U]


def add_gauge(mdl, U, a, y, prefix=None):
    """Impose  v >= _lex  rho.v  for the single generator rho.

    SOUNDNESS: rho induces a bijection of the feasible set that preserves the
    objective, so every orbit contains a lex-maximum, and the lex-maximum
    satisfies v >= _lex g.v for EVERY g in the group -- in particular for the
    generator.  Hence at least one representative of every feasible orbit
    survives.  Truncating the comparison to a prefix only weakens the cut
    (full lex >= implies prefix lex >=), so it stays sound at any length.
    Returns the number of positions constrained."""
    v = gauge_vector(U, a, y)
    rv = gauge_vector(U, {m: a[rho(m)] for m in U}, {m: y[rho(m)] for m in U})
    n = len(v) if prefix is None else min(prefix, len(v))
    eq = mdl.NewBoolVar("eq0")
    mdl.Add(eq == 1)
    for i in range(n):
        vi, ri = v[i], rv[i]
        if vi is ri:                       # rho fixes this coordinate
            continue
        # equal-so-far => v_i >= r_i    (clause: -eq | vi | -ri)
        mdl.AddBoolOr([eq.Not(), vi, ri.Not()])
        nxt = mdl.NewBoolVar("eq%d" % (i + 1))
        mdl.AddImplication(nxt, eq)                    # C1
        mdl.AddBoolOr([nxt.Not(), vi.Not(), ri])       # C2a: nxt & vi -> ri
        mdl.AddBoolOr([nxt.Not(), vi, ri.Not()])       # C2b: nxt & ri -> vi
        mdl.AddBoolOr([eq.Not(), vi, ri, nxt])         # C3: eq & -vi & -ri -> nxt
        mdl.AddBoolOr([eq.Not(), vi.Not(), ri.Not(), nxt])   # C4
        eq = nxt
    return n


def decide(targets, lam, B, cores, timeout, log_progress=False, minimize=True,
           gauge=False, gauge_prefix=None, fix=None):
    """Is lam*|A| + |Y| <= B feasible?  INFEASIBLE certifies G_int(lam) >= B+1."""
    from ortools.sat.python import cp_model
    lam = Fraction(lam)
    num, den = lam.numerator, lam.denominator
    U = sorted(L.universe(targets))
    mdl = cp_model.CpModel()
    a = {m: mdl.NewBoolVar("a%d" % m) for m in U}
    y = {m: mdl.NewBoolVar("y%d" % m) for m in U}
    b = {m: mdl.NewBoolVar("b%d" % m) for m in U}
    for m in U:
        mdl.Add(a[m] + y[m] <= 1)
        lits = [a[m]]
        for s1, s2 in split_pairs(m):
            parts = [p for p in (s1, s2) if popcount(p) > 1]
            sp = mdl.NewBoolVar("")
            mdl.AddBoolAnd([y[m]] + [b[p] for p in parts]).OnlyEnforceIf(sp)
            lits.append(sp)
        mdl.AddBoolOr(lits + [b[m].Not()])
    for t in targets:
        if popcount(t) > 1:
            mdl.Add(b[t] == 1)
    ngauge = add_gauge(mdl, U, a, y, gauge_prefix) if gauge else 0
    if fix is not None:                            # planted-assignment control
        Af, Yf = set(fix[0]), set(fix[1])
        for m in U:
            mdl.Add(a[m] == (1 if m in Af else 0))
            mdl.Add(y[m] == (1 if m in Yf else 0))
    obj = num * sum(a.values()) + den * sum(y.values())
    mdl.Add(obj <= B * den)                       # the decision cut
    # Keeping Minimize costs nothing and KEEPS CP-SAT's objective-bound
    # machinery (the LP/dual reasoning that drove the original run's bound from
    # 32 to 92).  Measured here: as a pure decision, B=50 is UNKNOWN at 60 s;
    # the original optimisation reached bound 86 in 600 s.  Status INFEASIBLE
    # is the certificate either way.
    if minimize:
        mdl.Minimize(obj)
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = cores
    s.parameters.max_time_in_seconds = float(timeout)
    s.parameters.log_search_progress = log_progress
    t0 = time.time()
    st = s.Solve(mdl)
    out = dict(lam=str(lam), B=B, status=s.StatusName(st),
               seconds=round(time.time() - t0, 1), n_masks=len(U),
               cores=cores, timeout=timeout, minimize=minimize,
               gauge=bool(gauge), gauge_positions=ngauge,
               planted=(fix is not None),
               best_bound=float(s.BestObjectiveBound()) / den if minimize else None)
    if st == cp_model.INFEASIBLE:
        out["certifies"] = "G_int(%s) >= %d" % (lam, B + 1)
    elif st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        A = sorted(m for m in U if s.Value(a[m]))
        Y = sorted(m for m in U if s.Value(y[m]))
        out.update(refutes="G_int(%s) <= %d" % (lam, B),
                   A_size=len(A), Y_size=len(Y),
                   A_hex=[hex(m) for m in A], Y_hex=[hex(m) for m in Y])
    return out


def lex_ge_rho(U, A, Y):
    """Python mirror of add_gauge's constraint, for a concrete assignment."""
    v = [(1 if m in A else 0) for m in U] + [(1 if m in Y else 0) for m in U]
    rv = [(1 if rho(m) in A else 0) for m in U] + \
         [(1 if rho(m) in Y else 0) for m in U]
    for x, r in zip(v, rv):
        if x != r:
            return x > r
    return True


def control(cores, timeout, out_path):
    """Soundness control for the Z/4 gauge break.  Writes to out_path."""
    T = L.mixcolumns_targets()
    U = sorted(L.universe(T))
    res = {"kind": "gauge_control", "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                        time.gmtime())}
    ok, findings = gauge_check(T)
    res["arithmetic"] = {k: v for k, v in findings.items()}
    res["arithmetic_ok"] = ok
    print("--- CONTROL A: arithmetic prerequisites ---")
    for k, v in findings.items():
        print("   %-45s %s" % (k, v))
    if not ok:
        res["verdict"] = "FAIL (arithmetic)"
        json.dump(res, open(out_path, "w"), indent=1)
        return res

    # CONTROL B: plant the published G(3) witness (obj 94) and its lex-max
    # rotation, and require the gauge-broken model to accept it.
    wit = json.load(open(ROOT + "/fleet6/laneTOOL2/results/u1_uncond.json"))
    w3 = [r for r in wit if r["lam"] == "3"][0]
    A0 = [int(h, 16) for h in w3["A_hex"]]
    Y0 = [int(h, 16) for h in w3["Y_hex"]]
    obj0 = 3 * len(A0) + len(Y0)
    print("\n--- CONTROL B: planted witness (published G(3) incumbent) ---")
    print("   |A|=%d |Y|=%d  obj=%d  (published G=%s)"
          % (len(A0), len(Y0), obj0, w3.get("G")))
    orbit = []
    for k in range(4):
        Ak = {rho_pow(m, k) for m in A0}
        Yk = {rho_pow(m, k) for m in Y0}
        assert Ak <= set(U) and Yk <= set(U), "rotation left the universe"
        orbit.append((k, Ak, Yk, lex_ge_rho(U, Ak, Yk)))
    survivors = [k for k, _, _, g in orbit if g]
    print("   orbit members satisfying the lex-leader cut: %s of [0,1,2,3]"
          % survivors)
    res["orbit_survivors"] = survivors
    res["orbit_distinct"] = len({tuple(sorted(Ak)) for _, Ak, _, _ in orbit})
    if not survivors:
        res["verdict"] = "FAIL (gauge cuts every representative of a real orbit)"
        json.dump(res, open(out_path, "w"), indent=1)
        return res
    k = survivors[0]
    _, Ak, Yk, _ = orbit[k]
    r = decide(T, "3", obj0, cores, timeout, minimize=False, gauge=True,
               fix=(Ak, Yk))
    print("   planted rotation k=%d into the GAUGE-BROKEN model at B=%d -> %s "
          "(%.1fs)" % (k, obj0, r["status"], r["seconds"]))
    res["planted_gauged"] = r
    r0 = decide(T, "3", obj0, cores, timeout, minimize=False, gauge=False,
                fix=(set(A0), set(Y0)))
    print("   same witness, UNGAUGED model at B=%d -> %s (%.1fs)"
          % (obj0, r0["status"], r0["seconds"]))
    res["planted_ungauged"] = r0
    good = (r["status"] in ("FEASIBLE", "OPTIMAL") and
            r0["status"] in ("FEASIBLE", "OPTIMAL"))
    res["verdict"] = "PASS" if good else "FAIL (planted witness rejected)"
    print("\n=== GAUGE CONTROL VERDICT: %s ===" % res["verdict"])
    json.dump(res, open(out_path, "w"), indent=1)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lam", default="3")
    ap.add_argument("--bounds", default="63,79,85,89,91")
    ap.add_argument("--timeout", type=float, default=7200)
    ap.add_argument("--cores", type=int, default=1)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--pure-decision", action="store_true",
                    help="drop Minimize (measured: much weaker; not recommended)")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--gauge", action="store_true",
                    help="impose the Z/4 lex-leader cut (run --control first)")
    ap.add_argument("--gauge-prefix", type=int, default=None)
    ap.add_argument("--control", default=None, metavar="JSON",
                    help="run the gauge soundness control, write it here, exit")
    a = ap.parse_args()
    if a.control:
        r = control(a.cores, a.timeout, a.control)
        return 0 if r.get("verdict") == "PASS" else 1
    if a.smoke:
        a.bounds, a.timeout = "40", 8.0
    if a.gauge:
        ok, _ = gauge_check(L.mixcolumns_targets())
        if not ok:
            print("REFUSING: gauge arithmetic prerequisites fail"); return 1
    done = set()
    if os.path.exists(a.out):
        for line in open(a.out):
            try:
                r = json.loads(line)
                if r["status"] in ("INFEASIBLE", "OPTIMAL", "FEASIBLE"):
                    done.add((r["lam"], r["B"], bool(r.get("gauge"))))
            except Exception:
                pass
    T = L.mixcolumns_targets()
    fh = open(a.out, "a")
    for bs in a.bounds.split(","):
        B = int(bs)
        if (a.lam, B, bool(a.gauge)) in done:
            print("B=%d already decided, skipping" % B, flush=True)
            continue
        r = decide(T, a.lam, B, a.cores, a.timeout, a.verbose,
                   minimize=not a.pure_decision, gauge=a.gauge,
                   gauge_prefix=a.gauge_prefix)
        fh.write(json.dumps(r, sort_keys=True) + "\n"); fh.flush()
        print("lam=%s B=%d gauge=%s -> %s  %.1fs  best_bound=%s  %s"
              % (a.lam, B, a.gauge, r["status"], r["seconds"], r.get("best_bound"),
                 r.get("certifies") or r.get("refutes") or "(no verdict)"),
              flush=True)
        if r["status"] in ("OPTIMAL", "FEASIBLE"):
            print("  ladder stops: a solution at or below %d exists" % B)
            break
    fh.close()


if __name__ == "__main__":
    main()
