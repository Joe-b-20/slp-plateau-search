#!/usr/bin/env python3
"""S3 — the wiring-randomised null for the surviving-side zero.

laneDELTA/RESULT.md §6(e), DOSSIER.md §9.2, REF_DELTA/VERDICT.md F5:
a "site" is a property of the WIRING, and every corpus wiring comes from one
deterministic rule (`_closure_core`: parents[v] = (u, v^u), first pair in build
order).  So the surviving-side zero (0 / 54,561) has never had a null that
varies only the parent choice.

This holds each corpus 88's MASK SET exactly fixed, re-wires it W random valid
ways, and recomputes lane536's site frame `delta` split by side (laneDELTA's
`sidesplit`).  Row 0 of every circuit is the as-found wiring (control).

Append-only jsonl, resumable: --out is re-read on start and (file, wiring)
pairs already present are skipped.  Single-threaded, ~200 MB.

  python3 wiring_null.py --circuits 200 --wirings 50 --out ../work/wiring_null.jsonl
  python3 wiring_null.py --smoke            # 3 circuits x 3 wirings, seconds
"""
import argparse, collections, glob, json, os, random, sys, time

ROOT = "/home/joebachir20/xor_ui/slp-plateau-search"
sys.path.insert(0, ROOT + "/experiments/e15_campaign3/compose")
sys.path.insert(0, ROOT + "/experiments/e16_lastwish/lane536")
from frame import Frame, TARGET                       # noqa: E402
from slp3 import pairset, minrep_S                    # noqa: E402


class Wiring(object):
    """A Frame-compatible view of an explicit gate list (no file needed)."""

    def __init__(self, pairs):
        self.pairs = list(pairs)
        sig = [1 << i for i in range(32)]
        for a, b in self.pairs:
            sig.append(sig[a] ^ sig[b])
        self.sig = sig
        self.n = len(self.pairs)
        self.mask = {32 + k: sig[32 + k] for k in range(self.n)}
        self.out = {}
        for oi, tm in enumerate(TARGET):
            hit = [s for s in range(32, 32 + self.n) if sig[s] == tm]
            if not hit:
                raise ValueError("output %d missing" % oi)
            self.out[oi] = hit[0]
        self.outsig = {v: k for k, v in self.out.items()}
        self.consumers = {s: [] for s in range(32 + self.n)}
        for k, (a, b) in enumerate(self.pairs):
            self.consumers[a].append(32 + k)
            self.consumers[b].append(32 + k)


def desc(f, s):
    out = set(); st = [s]
    while st:
        x = st.pop()
        for c in f.consumers[x]:
            if c not in out:
                out.add(c); st.append(c)
    return out


def sites(f):                       # verbatim lane536 / laneDELTA
    for u in range(32, 32 + f.n):
        if u in f.outsig: continue
        cs = f.consumers[u]
        if len(cs) != 2: continue
        c1, c2 = cs
        a, b = f.pairs[c1 - 32]; x1 = b if a == u else a
        a, b = f.pairs[c2 - 32]; x2 = b if a == u else a
        once = [x for x in (x1, x2) if x >= 32 and x not in f.outsig
                and len(f.consumers[x]) == 1]
        if not once: continue
        bad = desc(f, c1) | desc(f, c2) | {c1, c2, u} | set(once)
        S = sorted({f.sig[s] for s in range(32 + f.n) if s not in bad})
        yield u, c1, c2, x1, x2, once, S


def sidesplit(f):                   # verbatim laneDELTA/witness.py
    cnt = collections.Counter()
    for u, c1, c2, x1, x2, once, S in sites(f):
        P = pairset(S)
        for c, xs in ((c1, x1), (c2, x2)):
            d = minrep_S(f.mask[c], S, P)
            cnt["%s_%s" % ("del" if xs in once else "surv", d)] += 1
    return cnt


def random_wiring(masks, rng):
    """A uniformly-random-order valid realisation of `masks` (32 inputs).
    Buildability is a monotone closure, so any greedy order terminates."""
    units = [1 << i for i in range(32)]
    idx = {u: i for i, u in enumerate(units)}
    built = list(units); bset = set(units)
    rest = [m for m in masks if m not in bset]
    pairs = []
    while rest:
        rng.shuffle(rest)
        avail = None
        for i, m in enumerate(rest):
            ps = [(a, m ^ a) for a in built if (m ^ a) in bset and (m ^ a) != a]
            if ps:
                avail = (i, m, ps); break
        if avail is None:
            return None
        i, m, ps = avail
        a, b = ps[rng.randrange(len(ps))]
        pairs.append((idx[a], idx[b]))
        idx[m] = 32 + len(pairs) - 1
        built.append(m); bset.add(m); rest.pop(i)
    return pairs


def legal_parents(f):
    """For every gate mask of `f`, the parent pairs that are BOTH available in
    the signal set and acyclic (neither parent a descendant of the gate).
    |legal| = 1 means the wiring of that mask is FORCED by the mask set."""
    sigs = f.sig
    idxby = collections.defaultdict(list)
    for s in range(32 + f.n):
        idxby[sigs[s]].append(s)
    hist = collections.Counter()
    for k in range(f.n):
        s = 32 + k; m = sigs[s]; D = desc(f, s) | {s}
        legal = set()
        for a in range(32 + f.n):
            if a in D:
                continue
            q = m ^ sigs[a]
            if q == 0 or q == sigs[a]:
                continue
            for bi in idxby.get(q, []):
                if bi not in D:
                    legal.add(tuple(sorted((sigs[a], q)))); break
        hist[len(legal)] += 1
    return hist


def census(files, n_circuits):
    """Headline: how much wiring freedom does an 88's mask set actually have?"""
    tot = collections.Counter(); nc = 0
    for path in files:
        if nc >= n_circuits:
            break
        try:
            f = Frame(path, "x")
        except Exception:
            continue
        if f.n != 88:
            continue
        nc += 1
        tot += legal_parents(f)
    print("WIRING-FREEDOM CENSUS over %d 88-gate circuits (%d gate masks)"
          % (nc, sum(tot.values())))
    for k in sorted(tot):
        print("   %d legal parent pair(s): %d masks" % (k, tot[k]))
    print("   forced fraction: %.4f" % (tot[1] / max(1, sum(tot.values()))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--census", action="store_true",
                    help="report wiring freedom instead of running the null")
    ap.add_argument("--circuits", type=int, default=200)
    ap.add_argument("--wirings", type=int, default=50)
    ap.add_argument("--seed", type=int, default=20260829)
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "work",
        "wiring_null.jsonl"))
    ap.add_argument("--smoke", action="store_true")
    a = ap.parse_args()
    if a.smoke:
        a.circuits, a.wirings = 3, 3
    done = set()
    if os.path.exists(a.out):
        for line in open(a.out):
            try:
                r = json.loads(line); done.add((r["f"], r["w"]))
            except Exception:
                pass
    files = sorted(glob.glob(ROOT + "/**/*88gates*.json", recursive=True))
    random.Random(17).shuffle(files)
    if a.census:
        census(files, a.circuits)
        return
    fh = open(a.out, "a")
    agg = collections.Counter(); nc = 0; t0 = time.time()
    for path in files:
        if nc >= a.circuits:
            break
        try:
            f = Frame(path, "x")
        except Exception:
            continue
        if f.n != 88:
            continue
        nc += 1
        masks = [f.sig[s] for s in range(32, 32 + f.n)]
        rng = random.Random((a.seed, path).__hash__() & 0xFFFFFFFF)
        for w in range(a.wirings + 1):
            if (path, w) in done:
                continue
            if w == 0:
                g = f                                     # as-found control
            else:
                p = random_wiring(masks, rng)
                if p is None:
                    continue
                try:
                    g = Wiring(p)
                except ValueError:
                    continue
            cnt = sidesplit(g)
            agg += cnt
            fh.write(json.dumps({"f": os.path.relpath(path, ROOT), "w": w,
                                 "n": g.n, **cnt}) + "\n")
        if nc % 20 == 0:
            fh.flush()
            print("  %d circuits %.0fs  surv_2=%d surv_3=%d surv_4=%d "
                  "del_2=%d" % (nc, time.time() - t0, agg["surv_2"],
                                agg["surv_3"], agg["surv_4"], agg["del_2"]),
                  flush=True)
    fh.flush(); fh.close()
    print("=== %d circuits x %d wirings, %.0fs" % (nc, a.wirings, time.time() - t0))
    for k in sorted(agg, key=str):
        print("   %-10s %d" % (k, agg[k]))


if __name__ == "__main__":
    main()
