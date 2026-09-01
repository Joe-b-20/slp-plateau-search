#!/usr/bin/env python3
"""Draw the shippable ~500-set sample of the 88-gate MixColumns mask corpus.

THIS SCRIPT IS THE PROVENANCE RECORD, NOT A PUBLIC ENTRY POINT.  It reads the
two large intermediates of the full-corpus certificate run -- the streamed mask
file and its parallel provenance table -- which are 554 MB and 158 MB and do NOT
ship.  It is included so the draw is auditable: the selection is deterministic
(evenly spaced indices inside each stratum, no RNG), so anyone who regenerates
the intermediates regenerates this exact sample.

To CHECK the shipped sample instead -- which needs nothing but this pack --
run ``tools/check_sample.py``.

Outputs (written next to this script's parent directory):
  corpus88_sample.jsonl   one row per sampled mask set: canon, source label,
                          lineage prose, and the 88 masks as '%08x' strings
  corpus88_sample.bin     the same masks, 88 x uint32 LE per record, sorted
  SAMPLE.sha256           sha256 of both, plus of the full corpus index
"""
import hashlib
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.dirname(HERE)

# ---- the private intermediates (not shipped) --------------------------------
# Override with: build_sample.py <masks.bin> <canon.tsv> <corpus_index.jsonl>
SRC_BIN = sys.argv[1] if len(sys.argv) > 3 else None
SRC_TSV = sys.argv[2] if len(sys.argv) > 3 else None
SRC_IDX = sys.argv[3] if len(sys.argv) > 3 else None
# The five published record circuits, for the published_record stratum.
SRC_RECORDS = sys.argv[4] if len(sys.argv) > 4 else None

if not SRC_BIN:
    sys.exit(__doc__)

sys.path.insert(0, PACK)

# --- MixColumns targets, from the spec, recomputed here (no import needed) ---
def _xtime(a):
    a <<= 1
    return (a ^ 0x11B) & 0xFF if (a & 0x100) else (a & 0xFF)


def _gf_mul(a, b):
    r = 0
    for i in range(8):
        if (b >> i) & 1:
            t = a
            for _ in range(i):
                t = _xtime(t)
            r ^= t
    return r & 0xFF


def target_masks():
    coef = [2, 3, 1, 1]
    M = [[0] * 32 for _ in range(32)]
    for col in range(4):
        for k in range(4):
            c, ib = coef[k], (col + k) % 4
            for in_bit in range(8):
                v = _gf_mul(c, 1 << in_bit)
                for out_bit in range(8):
                    if (v >> out_bit) & 1:
                        M[col * 8 + out_bit][ib * 8 + in_bit] ^= 1
    return [sum(1 << c for c in range(32) if M[r][c]) for r in range(32)]


TARGETS = set(target_masks())


def canon(masks):
    return hashlib.sha256(
        ','.join('%08x' % m for m in sorted(masks)).encode()).hexdigest()[:16]


def replay(pairs):
    sig = [1 << i for i in range(32)]
    for a, b in pairs:
        sig.append(sig[a] ^ sig[b])
    return sig[32:]


# ---- strata -----------------------------------------------------------------
# (label, lineage prose, how many to draw, predicate on the provenance line)
#
# The predicate sees (source, path) from the private provenance table.  The
# bare strings it compares against are that table's own SOURCE KEYS -- keys of
# an index, not filesystem paths; no path from the private tree is reproduced
# here or in the shipped output.  This table is the auditable record of how
# each private source key was mapped to the public lineage label that appears
# in the sample; without it those labels could not be checked by anyone
# regenerating the draw.
STRATA = [
    ('published_record', 'one of the five published record 88-gate circuits '
     '(depths 5, 5-from-scratch, 6, 7, 8)', 5, None),                # special
    ('atlas_corner_jean', 'atlas corner enumeration seeded from the '
     'independently-authored (foreign-lineage) published 88', 40,
     lambda s, p: s == 'atlas_corner_plat' and '_jean_' in p),
    ('atlas_corner', 'atlas corner enumeration, own-lineage seeds', 40,
     lambda s, p: s == 'atlas_corner_plat' and '_jean_' not in p),
    ('basin_lateral', 'lateral moves inside a basin around a known 88', 20,
     lambda s, p: s == 'fleet1-4_basin_lateral'),
    ('census', 'exhaustive-population census of 88s at fixed depth', 60,
     lambda s, p: s == 'e15_census_pop88'),
    ('oracle_worklist', 'SAT/oracle-driven worklist descent to 88', 50,
     lambda s, p: s == 'beat88_pop88_worklist'),
    ('oracle_misc', 'assorted oracle-guided descent runs', 30,
     lambda s, p: s == 'beat88'),
    ('nrpa', 'nested rollout policy adaptation search, sub-92 pool', 100,
     lambda s, p: s == 'campaign_87_nrpa_sub92'),
    ('merged_engine', 'merged multi-heuristic engine hunt populations', 60,
     lambda s, p: s == 'campaign_87_merged_engine_pop'),
    ('deep_hunt', 'deep-hunt 88 population', 50,
     lambda s, p: s == 'campaign_87_population88_new'),
    ('layer89_descent', '88s found by descending from a 89-gate layer', 20,
     lambda s, p: s == 'campaign_87_found88_layer89'),
    ('campaign_misc', 'assorted search-campaign outputs', 20,
     lambda s, p: s == 'campaign_87'),
    ('fleet_late', 'late-wave distributed fleet runs', 10,
     lambda s, p: s == 'fleet9-12'),
    ('atlas_misc', 'assorted atlas ladder/ring outputs', 6,
     lambda s, p: s == 'atlas'),
    ('fleet_mid', 'mid-wave distributed fleet runs', 2,
     lambda s, p: s == 'fleet5-8'),
    ('fleet_early', 'early-wave distributed fleet runs', 1,
     lambda s, p: s == 'fleet1-4'),
    ('experiment_readd', 'gate re-addition experiment', 5,
     lambda s, p: s == 'experiments_early/e5_readd'),
    ('experiment_plateau', 'plateau-87 experiment outputs', 2,
     lambda s, p: s == 'experiments_late/e14_plateau87'),
]


def main():
    # 1. published record circuits -> canon set
    pub = {}
    if SRC_RECORDS and os.path.isdir(SRC_RECORDS):
        for fn in sorted(os.listdir(SRC_RECORDS)):
            if '88gates' not in fn or not fn.endswith('.json'):
                continue
            d = json.load(open(os.path.join(SRC_RECORDS, fn)))
            gates = d['gates'] if isinstance(d, dict) else d
            masks = replay([list(g) for g in gates])
            assert len(set(masks)) == 88 and TARGETS <= set(masks), fn
            pub[canon(masks)] = fn[:-5]
    print('published record 88s: %d  %s' % (len(pub), sorted(pub.values())))

    # 2. one pass over the provenance table, bucketing record indices
    buckets = {lab: [] for lab, _, _, _ in STRATA}
    pubhit = {}
    with open(SRC_TSV) as f:
        for i, line in enumerate(f):
            c, s, p = line.rstrip('\n').split('\t')
            if c in pub:
                pubhit[c] = i
            for lab, _, _, pred in STRATA:
                if pred and pred(s, p):
                    buckets[lab].append(i)
                    break
    print('bucket sizes: %s' % {k: len(v) for k, v in buckets.items()})
    missing = set(pub) - set(pubhit)
    assert not missing, 'published 88 not found in the corpus: %s' % missing

    # 3. deterministic even-stride pick inside each stratum
    picks = {}                       # record index -> (label, lineage, extra)
    for lab, prose, want, pred in STRATA:
        if lab == 'published_record':
            for c, i in sorted(pubhit.items(), key=lambda kv: kv[1]):
                picks[i] = (lab, prose, {'record_circuit': pub[c]})
            continue
        idxs = buckets[lab]
        if not idxs:
            print('WARNING stratum empty: %s' % lab)
            continue
        n = min(want, len(idxs))
        stride = len(idxs) / n
        for j in range(n):
            i = idxs[int(j * stride)]
            picks.setdefault(i, (lab, prose, {}))

    order = sorted(picks)
    print('sampled %d distinct mask sets across %d strata'
          % (len(order), len(set(p[0] for p in picks.values()))))

    # 4. pull the masks, re-check every one, write the sample
    canons = [l.split('\t', 1)[0] for l in open(SRC_TSV)]
    outj = os.path.join(PACK, 'corpus88_sample.jsonl')
    outb = os.path.join(PACK, 'corpus88_sample.bin')
    bf = open(outb, 'wb')
    jf = open(outj, 'w')
    with open(SRC_BIN, 'rb') as mf:
        for i in order:
            mf.seek(i * 88 * 4)
            masks = list(struct.unpack('<88I', mf.read(352)))
            # BUILD-TIME RE-CHECK, every row, no exceptions
            assert len(set(masks)) == 88, 'row %d: not 88 distinct masks' % i
            assert TARGETS <= set(masks), 'row %d: missing targets' % i
            c = canon(masks)
            assert c == canons[i], 'row %d: canon mismatch' % i
            lab, prose, extra = picks[i]
            row = {'canon': c, 'source': lab, 'lineage': prose,
                   'n_masks_distinct': 88, 'n_targets_present': 32,
                   'masks': ['%08x' % m for m in sorted(masks)]}
            row.update(extra)
            jf.write(json.dumps(row) + '\n')
            bf.write(struct.pack('<88I', *sorted(masks)))
    jf.close()
    bf.close()

    # 5. provenance hashes
    def sha(p):
        h = hashlib.sha256()
        with open(p, 'rb') as f:
            for blk in iter(lambda: f.read(1 << 20), b''):
                h.update(blk)
        return h.hexdigest()

    with open(os.path.join(PACK, 'SAMPLE.sha256'), 'w') as f:
        f.write('%s  corpus88_sample.jsonl\n' % sha(outj))
        f.write('%s  corpus88_sample.bin\n' % sha(outb))
        f.write('%s  corpus88_index.jsonl  (the FULL index, not shipped;'
                ' %d bytes)\n' % (sha(SRC_IDX), os.path.getsize(SRC_IDX)))
    print(open(os.path.join(PACK, 'SAMPLE.sha256')).read())


if __name__ == '__main__':
    main()
