#!/usr/bin/env python3
"""assemble.py — mask set -> circuit, with the exact minimum-depth schedule
and with the COUNT DELTA ACCOUNTED FOR.

Separation this tool keeps (inherited from lane G, and correct):
    the MODEL chooses a SET of masks;
    the DEPTH of a circuit is a property of the SCHEDULE, not of the set.
`min_depth_schedule` computes, by level-BFS over the set, the provably minimum
depth at which each mask can be produced using only masks of that same set.
Level L is exactly the masks expressible as an XOR of two masks of level < L,
so no schedule can place any mask earlier.  (Lane DEPTH measured the value of
assembly-order optimisation at EXACTLY ZERO on 12/12 circuits, so this is
book-keeping, not a lever.)

CHARTER ITEM 4 -- BE HONEST ABOUT COUNT.  A circuit is a SET, so when two
blocks independently build the same mask the set de-duplicates and the emitted
count lands BELOW the model price.  Lane G measured asked-97 -> emitted-95 and
asked-100 -> emitted-98 and could not say why.  `MaskSet` here records every
collision with the two block tags involved, so `collisions()` names the exact
cause of every gate of the delta.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from theory import TARGET_MASKS


class MaskSet:
    """An ordered, de-duplicated set of masks with a validity witness and a
    full record of cross-block collisions."""

    def __init__(self):
        self.order = [1 << i for i in range(32)]
        self.have = {1 << i for i in range(32)}
        self.parents = {}
        self.tags = {}
        self.hits = []          # [(mask, first_tag, second_tag)] -- the delta
        # witness arrival level.  This is an UPPER bound on the level the final
        # min-depth schedule will give the mask, so quoting it to a block as an
        # input level is conservative: the emitted circuit can only be
        # shallower than the block programs were solved for, never deeper.
        self.lvl = {1 << i: 0 for i in range(32)}

    def add(self, a, b, tag=None):
        assert a in self.have and b in self.have, "operand not available"
        m = a ^ b
        l = max(self.lvl[a], self.lvl[b]) + 1
        if m in self.have:
            first = self.tags.get(m, "INPUT")
            if first != tag:
                self.hits.append((m, first, tag))
            if l < self.lvl[m]:
                self.lvl[m] = l
            return m
        self.have.add(m)
        self.order.append(m)
        self.parents[m] = (a, b)
        self.tags[m] = tag
        self.lvl[m] = l
        return m

    def add_chain(self, bits, tag=None):
        cur = 1 << bits[0]
        for i in bits[1:]:
            cur = self.add(cur, 1 << i, tag)
        return cur

    def n_gates(self):
        return len(self.order) - 32

    def collisions(self):
        """The named cause of every gate by which the emitted count falls
        below the model price."""
        by_pair = {}
        for m, f, s in self.hits:
            by_pair.setdefault((f, s), []).append(m)
        return [{"first_built_by": f, "rebuilt_by": s, "n": len(ms),
                 "masks": [hex(x) for x in sorted(ms)]}
                for (f, s), ms in sorted(by_pair.items(),
                                         key=lambda kv: -len(kv[1]))]

    def per_block(self):
        n = {}
        for m in self.order[32:]:
            t = self.tags.get(m)
            n[t] = n.get(t, 0) + 1
        return n


def min_depth_schedule(masks, on_level=None):
    """(gates, depth, order).  Raises ValueError if the set is not closed."""
    S = list(dict.fromkeys(masks))
    inputs = [1 << i for i in range(32)]
    for m in inputs:
        assert m in S, "input singleton missing"
    rest = [m for m in S if m not in set(inputs)]
    settled = {m: 0 for m in inputs}
    by_level = {0: list(inputs)}
    remaining = set(rest)
    parents = {}
    level = 0
    while remaining:
        level += 1
        avail = list(settled.keys())
        xor_index = {}
        for i in range(len(avail)):
            ai = avail[i]
            for j in range(i + 1, len(avail)):
                x = ai ^ avail[j]
                if x in remaining and x not in xor_index:
                    xor_index[x] = (ai, avail[j])
        if not xor_index:
            raise ValueError(f"mask set not closed: {len(remaining)} unreachable")
        newly = list(xor_index)
        for m in newly:
            parents[m] = xor_index[m]
            settled[m] = level
            remaining.discard(m)
        by_level[level] = newly
        if on_level is not None:
            on_level(level, len(newly), len(remaining))
    order = list(inputs)
    for L in range(1, level + 1):
        order.extend(sorted(by_level.get(L, [])))
    idx = {m: i for i, m in enumerate(order)}
    gates = [[idx[parents[m][0]], idx[parents[m][1]]] for m in order[32:]]
    return gates, max(settled.values()), order


def strip_dead_gates(gates):
    """(gates, n_removed) — DEAD-GATE ELIMINATION.  lane LIB (fleet12), audit
    defect D6 / §6.4 rank 6.

    A gate is DEAD when its output signal is neither one of the 32 FIPS-197
    target masks nor consumed by a surviving gate.  Dropping one cannot change
    what the circuit computes, so the result still builds all 32 targets, has
    no greater depth, and is strictly shorter: `L(M) <= len(stripped)` remains
    a true certificate and is a better one.

    Why the package needed this: the model chooses a SET of masks, and a
    currency shape that no block ends up consuming still costs a gate in the
    emitted circuit.  REF-V15 measured every artefact in `results/`:
    `reg_116at3` carries **8** dead gates, `reg_92at4` / `reg_93at5` /
    `reg_94at5` one each; all four 88s, `reg_89`, `reg_90at5`, `reg_91at5` and
    `gen_88_noQ27` are clean.  Stripped and re-replayed: 116@3 -> 108@3,
    92@4 -> 91@4, 93@5 -> 92@5, 94@5 -> 93@5, all 32/32 targets at unchanged
    depth.  THE RECORD IS UNTOUCHED -- every 88 this tool has emitted is
    already clean, which is why this pass costs the headline nothing.

    One backwards pass reaches the fixpoint: a gate's operands always have
    strictly smaller indices, so marking need in decreasing index order can
    never have to revisit a gate.
    """
    n = len(gates)
    sig = [1 << i for i in range(32)]
    for a, b in gates:
        sig.append(sig[a] ^ sig[b])
    T = set(TARGET_MASKS)
    need = [v in T for v in sig]
    for k in range(n - 1, -1, -1):
        if need[32 + k]:
            a, b = gates[k]
            need[a] = True
            need[b] = True
    newidx = {i: i for i in range(32)}
    out = []
    for k, (a, b) in enumerate(gates):
        if not need[32 + k]:
            continue
        newidx[32 + k] = 32 + len(out)
        out.append([newidx[a], newidx[b]])
    return out, n - len(out)


def circuit_stats(gates):
    sig = [1 << i for i in range(32)]
    depth = [0] * 32
    for a, b in gates:
        sig.append(sig[a] ^ sig[b])
        depth.append(max(depth[a], depth[b]) + 1)
    return len(gates), max(depth), sig


def verify_inprocess(gates):
    """Independent check #1: replay the gate list and count how many of the 32
    FIPS-197 targets it produces.  TARGET_MASKS is REBUILT inside theory.py
    from the field and the matrix, never read from a file."""
    sig = [1 << i for i in range(32)]
    ok = True
    for k, (a, b) in enumerate(gates):
        if not (0 <= a < 32 + k and 0 <= b < 32 + k):
            ok = False
            break
        sig.append(sig[a] ^ sig[b])
    have = set(sig)
    built = sum(1 for t in TARGET_MASKS if t in have)
    return built, len(gates), ok
