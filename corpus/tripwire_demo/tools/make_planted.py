#!/usr/bin/env python3
"""Build the two planted-defect positive controls for tripwire.py.

An instrument that cannot fire is not evidence, so the demo needs a circuit the
tripwire MUST fire on.  Both are the published depth-6 record 88 with one gate
added; both are one gate larger than they need to be, by construction.

  planted_dup.json   gate K is duplicated exactly, and the copy is given a
                     consumer so that the DEAD-GATE rule cannot explain the
                     firing.  The duplicated value is not one of the 32 target
                     masks, so both copies count as working gates and
                     B reads 57 -- its expected value for an 89-gate circuit --
                     while a gate is still plainly deletable.  This is the
                     demonstration that B is a screen and not a decision
                     procedure: "B != n-q implies a deletable gate" is sound,
                     and its converse is false.

  planted_dead.txt   the same circuit plus one gate nobody reads, written in
                     the plain-text `a b` input format rather than JSON, so the
                     demo also exercises the second reader.

usage: make_planted.py <depth6_circuit.json> [outdir]

With no <outdir> the two controls are written to a fresh temporary directory,
whose path is printed, so the script never writes inside the repository. The
shipped copies in `circuits/` are what a run reproduces; regenerate them in
place only on purpose, by naming `circuits` explicitly.
"""
import json
import os
import sys
import tempfile

src = sys.argv[1]
outdir = sys.argv[2] if len(sys.argv) > 2 else tempfile.mkdtemp(prefix="planted_")
print("outdir: %s" % outdir)
d = json.load(open(src))
g = [list(x) for x in (d["gates"] if isinstance(d, dict) else d)]

# ---- 1. a duplicated value, with a consumer --------------------------------
K = 20
res = []
for i, x in enumerate(g):
    res.append(list(x))
    if i == K:
        res.append(list(g[K]))                  # an exact copy of gate K


def sh(v):
    return v + 1 if v >= 32 + K + 1 else v      # everything after K shifts by 1


res = [p if i <= K + 1 else [sh(p[0]), sh(p[1])] for i, p in enumerate(res)]
done = False
for i in range(K + 2, len(res)):                # give the copy a consumer
    for j in (0, 1):
        if res[i][j] == 32 + K:
            res[i][j] = 32 + K + 1
            done = True
            break
    if done:
        break
assert done, "no consumer of gate K found to rewire"
json.dump({"gates": res}, open(os.path.join(outdir, "planted_dup.json"), "w"))
print("planted_dup.json  : %d gates (duplicate of gate %d, given a consumer)"
      % (len(res), K))

# ---- 2. a gate nobody reads, in the plain-text format ----------------------
g2 = [list(x) for x in g] + [[0, 1]]
with open(os.path.join(outdir, "planted_dead.txt"), "w") as f:
    f.write("# same circuit, plus one gate nobody reads\n")
    f.write("\n".join("%d %d" % (a, b) for a, b in g2) + "\n")
print("planted_dead.txt  : %d gates (last one has no consumer)" % len(g2))
