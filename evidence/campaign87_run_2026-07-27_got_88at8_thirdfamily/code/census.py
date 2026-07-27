#!/usr/bin/env python3
"""census.py -- incremental harvest census + new-family detector (wave-3).

Scans runs_hunt/*.pop.jsonl incrementally (offsets persisted), dedupes
88-gate mask sets by md5-of-sorted-json, computes Jaccard to the two known
88 families (Jean's IMPORTED_88 and merged-engine's independent 88), and:
  * appends every NEW distinct 88 line to population88_new.jsonl
  * any 88 with J<0.70 to BOTH families -> oracle-verify -> save as
    NEWFAMILY_88_<nn>_jJ<...>_jN<...>.json at folder top (max 25)
  * prints a one-line summary + running min-J stats.

Usage: python3 census.py [--seed-preseen]  (run from the agent folder)
"""
import os, sys, json, glob, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "work"))
import mixcolumns_core as core
import engines

CDIR = "census"
os.makedirs(CDIR, exist_ok=True)
OFF = os.path.join(CDIR, "offsets.json")
HASHES = os.path.join(CDIR, "hashes.txt")
PRESEEN = os.path.join(CDIR, "preseen.txt")
STATS = os.path.join(CDIR, "stats.json")
POPNEW = "population88_new.jsonl"

refs = json.load(open("family_refs.json"))
JEAN = set(refs["jean"]); NEW88 = set(refs["new88"])


def jac(A, B):
    return len(A & B) / len(A | B)


def h(ms):
    return hashlib.md5(json.dumps(sorted(ms)).encode()).hexdigest()[:16]


def load_lines(path):
    s = set()
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                s.add(line.strip())
    return s


def seed_preseen():
    pre = load_lines(PRESEEN)
    n0 = len(pre)
    with open(PRESEEN, "a") as out:
        for path in glob.glob("../merged-engine/runs_hunt/*.pop.jsonl"):
            with open(path) as f:
                for line in f:
                    try:
                        ms = json.loads(line)
                    except ValueError:
                        continue
                    if len(ms) != 88:
                        continue
                    hh = h(ms)
                    if hh not in pre:
                        pre.add(hh)
                        out.write(hh + "\n")
    print("preseen seeded: %d -> %d wave-2 88-hashes" % (n0, len(pre)))


def main():
    if "--seed-preseen" in sys.argv:
        seed_preseen()
        return
    offsets = json.load(open(OFF)) if os.path.exists(OFF) else {}
    hashes = load_lines(HASHES)
    preseen = load_lines(PRESEEN)
    stats = json.load(open(STATS)) if os.path.exists(STATS) else {
        "minJJ": 1.0, "minJN": 1.0, "minJboth": 1.0, "newfam": 0,
        "n88_lines": 0, "best_pair": None}
    nf_saved = stats["newfam"]
    n_new = 0
    hf = open(HASHES, "a")
    pf = open(POPNEW, "a")
    for path in sorted(glob.glob("runs_hunt/*.pop.jsonl")):
        off = offsets.get(path, 0)
        try:
            f = open(path)
        except OSError:
            continue
        f.seek(off)
        data = f.read()
        f.close()
        end = data.rfind("\n")
        if end < 0:
            offsets[path] = off
            continue
        off += end + 1  # consume only whole lines; partial tail re-read later
        for line in data[:end].split("\n"):
            try:
                ms = json.loads(line)
            except ValueError:
                continue
            if len(ms) != 88:
                continue
            stats["n88_lines"] += 1
            hh = h(ms)
            if hh in hashes:
                continue
            hashes.add(hh)
            hf.write(hh + "\n")
            n_new += 1
            if hh not in preseen:
                pf.write(line + "\n")
            S = set(ms)
            jj = jac(S, JEAN); jn = jac(S, NEW88)
            if jj < stats["minJJ"]:
                stats["minJJ"] = jj
            if jn < stats["minJN"]:
                stats["minJN"] = jn
            jb = max(jj, jn)
            if jb < stats["minJboth"]:
                stats["minJboth"] = jb
                stats["best_pair"] = [round(jj, 3), round(jn, 3)]
            if jj < 0.70 and jn < 0.70 and nf_saved < 25:
                try:
                    gates = engines._walk_gates(S, None)
                    v = core.verify(gates, max_depth=None)
                except Exception:
                    v = {"ok": False}
                if v.get("ok") and v["gates"] == 88:
                    name = "NEWFAMILY_88_%02d_jJ%03d_jN%03d.json" % (
                        nf_saved, round(jj * 1000), round(jn * 1000))
                    core.save(gates, name,
                              extra={"depth": v["depth"], "verified": True,
                                     "J_jean": round(jj, 4),
                                     "J_new88": round(jn, 4)})
                    nf_saved += 1
                    print("*** NEW FAMILY 88 saved: %s" % name)
        offsets[path] = off
    stats["newfam"] = nf_saved
    hf.close(); pf.close()
    json.dump(offsets, open(OFF, "w"))
    json.dump(stats, open(STATS, "w"))
    print("census: distinct88=%d (+%d new this pass, %d beyond wave-2) "
          "minJ_jean=%.3f minJ_new88=%.3f minJ_both=%.3f (pair=%s) newfam=%d"
          % (len(hashes), n_new, len(hashes - preseen),
             stats["minJJ"], stats["minJN"], stats["minJboth"],
             stats["best_pair"], nf_saved))


if __name__ == "__main__":
    main()
