#!/usr/bin/env python3
"""Stream every distinct verified 88-gate MASK SET out of the corpus-88 sources
into a flat binary file, for the C deletion-realisability certificate.

REUSE, NOT REINVENTION.  This imports the corpus consolidator module and calls its own
source readers (walk_files / plats / basin_laterals / census_pkl / bank_jsonl /
bank_glob) with a drop-in sink that, instead of building the index record, emits
the 88 masks.  Admission (88 masks, all 32 MixColumns targets present) and
identity (canon = sha256 of the sorted '%08x' mask list, 16 hex) are corpus88's
own, unchanged -- so the stream is exactly the population of
the corpus index, 1,575,516 rows.

Outputs (CORPUS_OUT):
  masks.bin   88 x uint32 LE per record, masks sorted ascending
  canon.tsv   one line per record, in the SAME order: canon \t source \t file
  producer_stats.json
"""
import json, os, struct, sys, time

# REFERENCE COPY.  This is the full-corpus producer: it re-streams all
# 1,575,516 distinct 88-gate mask sets out of the search-campaign banks that
# hold them.  Those banks are ~40 GB of raw run output and are NOT part of this
# pack, so this script cannot run from the pack -- it is shipped so the
# provenance of the certified population is auditable, and so the full-scale run
# can be reproduced by anyone holding the sources.  ~24 min, one thread.
#
# Point ROOT at a tree holding the search-campaign output and the corpus
# consolidator module; OUT at where masks.bin / canon.tsv should be written.
ROOT = os.environ.get('CORPUS_ROOT', '.')
OUT = os.environ.get('CORPUS_OUT', '.')
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import corpus88                                                    # noqa: E402

# The five bulk source banks, by public lineage label.  Their locations are
# specific to the tree that produced the corpus and are NOT recorded here;
# supply them in a JSON file and point CORPUS_SOURCES at it.  See
# sources.example.json for the required keys.
SOURCES = json.load(open(os.environ['CORPUS_SOURCES']))

TARGETS = corpus88.TARGETS


class StreamSink:
    """Drop-in for corpus88.Sink: same admission test, same canon, but writes
    the masks to disk and keeps only a 64-bit dedup key in memory."""

    def __init__(self, binf, tsvf):
        self.bin = binf
        self.tsv = tsvf
        self.seen = set()
        self.n = 0
        self.d = {}            # unused; present so corpus88 code paths work
        self.per_source = {}
        self.stats = {}

    def add(self, masks, source, path, depth=None, pairs=None, note=None):
        if len(masks) != 88:
            return None
        ms = set(masks)
        if not TARGETS <= ms:
            return None
        h = corpus88.canon(masks)
        self.per_source.setdefault(source, 0)
        key = int(h, 16)
        if key in self.seen:
            self.per_source[source] += 1
            return h
        self.seen.add(key)
        self.bin.write(struct.pack('<88I', *sorted(ms)))
        self.tsv.write('%s\t%s\t%s\n' % (h, source, path))
        self.n += 1
        self.per_source[source] += 1
        return h

    def dump(self, tag):
        pass

    def load(self, tag):
        return True


def main():
    t0 = time.monotonic()
    with open(os.path.join(OUT, 'masks.bin'), 'wb') as bf, \
            open(os.path.join(OUT, 'canon.tsv'), 'w') as tf:
        s = StreamSink(bf, tf)
        # ORDER MATTERS: the five bulk JSONL banks + the census pickle + the
        # .plat rows carry >99% of the 1,575,516 distinct sets and stream in
        # minutes.  corpus88.walk_files (580,278 loose .json stat+reads) is the
        # slow tail and goes LAST, so that a prefix of masks.bin is always a
        # usable, certifiable population if the run is cut short.
        steps = [
            ('plat', lambda: corpus88.plats(s)),
            ('basin', lambda: corpus88.basin_laterals(s)),
            ('census', lambda: corpus88.census_pkl(s)),
            ('oracle_worklist', lambda: corpus88.bank_jsonl(
                s, SOURCES['oracle_worklist'],
                'oracle_worklist',
                lambda o: [int(x, 16) for x in o['masks_hex'].split(',')]
                if o.get('gates') == 88 and o.get('masks_hex') else None,
                prefilter=b'masks_hex')),
            ('deep_hunt', lambda: corpus88.bank_jsonl(
                s, SOURCES['deep_hunt'],
                'deep_hunt',
                lambda o: o if isinstance(o, list) and len(o) == 88 else None)),
            ('layer89_descent', lambda: corpus88.bank_jsonl(
                s, SOURCES['layer89_descent'],
                'layer89_descent',
                lambda o: o.get('masks') if o.get('gates') == 88 else None,
                prefilter=b'"masks"')),
            ('merged_engine', lambda: corpus88.bank_glob(
                s, SOURCES['merged_engine'],
                'merged_engine',
                lambda o: o if isinstance(o, list) and len(o) == 88 else None)),
            ('nrpa', lambda: corpus88.bank_jsonl(
                s, SOURCES['nrpa'],
                'nrpa',
                lambda o: o.get('masks') if o.get('gates') == 88 else None,
                prefilter=b'"gates": 88,')),
            ('walk', lambda: corpus88.walk_files(s)),
        ]
        for name, fn in steps:
            r = fn()
            print('%-22s distinct_so_far=%d  %s' % (name, s.n, r), flush=True)
            bf.flush()
            tf.flush()
    stats = {'distinct_written': s.n,
             'rows_admitted_per_source': s.per_source,
             'secs': round(time.monotonic() - t0, 1),
             'stage_stats': s.stats}
    json.dump(stats, open(os.path.join(OUT, 'producer_stats.json'), 'w'),
              indent=1, default=str)
    print('TOTAL distinct mask sets written:', s.n, flush=True)


if __name__ == '__main__':
    main()
