#!/usr/bin/env python3
"""CORPUS-88 consolidator.

ONE deduplicated index of every distinct verified 88-gate MixColumns circuit /
mask-set held on this machine.

IDENTITY (reused, not invented).  The project's standard notion of circuit
identity is the SORTED MULTISET OF GATE OUTPUT MASKS (32-bit ints), exactly as
in experiments/e15_campaign3/tools/cache_pop.py:38 --

    key = tuple(sorted(gm))     # gm = masks_of(pairs) = sig[32:]

and the masks themselves are produced by replaying index pairs with the oracle's
own semantics (verify_circuit.load_index_pairs + sig[a]^sig[b]), which is what
sweep.py:validity() does too.  We hash that key:

    canon = sha256(",".join("%08x" % m for m in sorted(masks))).hexdigest()[:16]

A row is admitted only if it is a VALID 88: exactly 88 masks and all 32
MixColumns target masks present among them (verify_circuit's own spec code
supplies the targets).  For gate-list sources this is the full replay test.
For mask-set-only sources it is the set-level test (no build order on disk).

B = 56 TRIPWIRE (bonus, e15 sweep.py:296 count_B).  B = number of non-output
gates that have a consumer.  On a valid 88 not already reducible to 87, B == 56.
B != 56 => an 87 is available by deletion.
  * gate-list sources: full count_B (needs the DAG).
  * mask-only sources: the two set-level halves of the same theorem --
    88 DISTINCT masks, and all 32 targets present.  A duplicate mask is an
    immediate 87; the consumer-less half cannot be decided without a DAG.

Usage:  nice -n 19 python3 corpus88.py --stage <name> ...
"""
import argparse, hashlib, json, os, pickle, sys, time

ROOT = '/home/joebachir20/xor_ui/slp-plateau-search'
RECORDS = '/home/joebachir20/xor_ui/aes_mc_records'
WORK = os.path.join(ROOT, 'wrapup', 'work')
sys.path.insert(0, ROOT)
from verify_circuit import mixcolumns_target_masks, load_index_pairs  # noqa: E402

TARGETS = set(mixcolumns_target_masks())


def canon(masks):
    return hashlib.sha256(
        ','.join('%08x' % m for m in sorted(masks)).encode()).hexdigest()[:16]


def replay(pairs):
    """-> (masks, depth) or (None, None) if the pair list is malformed."""
    sig = [1 << i for i in range(32)]
    dep = [0] * 32
    for a, b in pairs:
        if not (isinstance(a, int) and isinstance(b, int)):
            return None, None
        if not (0 <= a < len(sig) and 0 <= b < len(sig)):
            return None, None
        sig.append(sig[a] ^ sig[b])
        dep.append(max(dep[a], dep[b]) + 1)
    return sig[32:], max(dep)


def count_B(pairs, masks):
    """e15 sweep.py count_B: non-output gates that have a consumer."""
    n = len(pairs)
    cons = [0] * n
    for a, b in pairs:
        for x in (a, b):
            if x >= 32:
                cons[x - 32] += 1
    return sum(1 for g in range(n) if masks[g] not in TARGETS and cons[g])


# ---------------------------------------------------------------- ingest sink

class Sink:
    """hash -> record.  Incarnations capped so the index stays readable."""
    CAP = 8

    def __init__(self):
        self.d = {}
        self.per_source = {}
        self.stats = {}

    def add(self, masks, source, path, depth=None, pairs=None, note=None):
        if len(masks) != 88:
            return None
        ms = set(masks)
        if not TARGETS <= ms:
            return None
        h = canon(masks)
        r = self.d.get(h)
        if r is None:
            r = self.d[h] = {'canon': h, 'gates': 88, 'depth': depth,
                             'n_masks_distinct': len(ms),
                             'incarnations': [], 'n_incarnations': 0,
                             'sources': []}
        r['n_incarnations'] += 1
        if depth is not None and (r['depth'] is None or depth < r['depth']):
            r['depth'] = depth
        if source not in r['sources']:
            r['sources'].append(source)
        if len(r['incarnations']) < self.CAP:
            e = {'source': source, 'file': path}
            if depth is not None:
                e['depth'] = depth
            if note:
                e['note'] = note
            r['incarnations'].append(e)
        if pairs is not None and 'B' not in r:
            r['B'] = count_B(pairs, masks)
            r['B_theorem_ok'] = (r['B'] == 56)
        self.per_source.setdefault(source, set()).add(h)
        return h

    def dump(self, tag):
        with open(os.path.join(WORK, 'sink_%s.pkl' % tag), 'wb') as f:
            pickle.dump({'d': self.d,
                         'per_source': self.per_source,
                         'stats': self.stats}, f, 2)

    def load(self, tag):
        p = os.path.join(WORK, 'sink_%s.pkl' % tag)
        if not os.path.exists(p):
            return False
        o = pickle.load(open(p, 'rb'))
        self.d, self.per_source, self.stats = o['d'], o['per_source'], o['stats']
        return True


# ------------------------------------------------------------------- sources

SKIP_DIRS = {'.git', '__pycache__', 'venv', '.venv', 'node_modules',
             '.pytest_cache', '.claude', 'wrapup'}


def walk_files(sink):
    """Every .json on disk that parses as an 88-gate circuit.

    EXCLUDED: beat88 m3_census exports/ (1.25 M files, 6.7 GB on disk) -- see
    CORPUS88.md 'Not indexed'.
    """
    n_files = n_read = n_ok = 0
    t0 = time.monotonic()
    for root in (ROOT, RECORDS):
        for dp, dn, fn in os.walk(root):
            dn[:] = [d for d in dn if d not in SKIP_DIRS]
            if os.path.basename(dp) == 'exports' and 'm3_census' in dp:
                dn[:] = []
                continue
            for f in fn:
                if not f.endswith('.json'):
                    continue
                n_files += 1
                p = os.path.join(dp, f)
                try:
                    st = os.stat(p)
                except OSError:
                    continue
                if st.st_size < 500 or st.st_size > 4_000_000:
                    continue
                try:
                    b = open(p, 'rb').read()
                except OSError:
                    continue
                if b'"gates"' not in b and b'"gateCount"' not in b \
                        and not b.lstrip()[:2] == b'[[':
                    continue
                n_read += 1
                try:
                    pairs = [tuple(x) for x in load_index_pairs(json.loads(b))]
                except Exception:
                    continue
                if len(pairs) != 88 or any(len(g) != 2 for g in pairs):
                    continue
                masks, depth = replay(pairs)
                if masks is None:
                    continue
                src = source_of(p)
                if sink.add(masks, src, os.path.relpath(p, os.path.dirname(ROOT)),
                            depth=depth, pairs=pairs):
                    n_ok += 1
    sink.stats['walk'] = {'json_seen': n_files, 'json_parsed': n_read,
                          'valid88_files': n_ok,
                          'secs': round(time.monotonic() - t0, 1)}
    return sink.stats['walk']


def source_of(p):
    """Map an absolute path to a source label used in the per-source table."""
    if p.startswith(RECORDS):
        return 'records_repo'
    rel = os.path.relpath(p, ROOT)
    top = rel.split(os.sep)[0]
    if top == 'experiments':
        e = rel.split(os.sep)[1]
        if e.startswith(('e13', 'e14', 'e15', 'e16', 'e17')):
            return 'experiments_late/' + e
        return 'experiments_early/' + e
    if top in ('evidence', 'pipeline', 'reproduce'):
        return 'evidence'
    if top.startswith('fleet'):
        n = int(''.join(c for c in top if c.isdigit()) or 0)
        if n <= 4:
            return 'fleet1-4'
        if n <= 8:
            return 'fleet5-8'
        return 'fleet9-12'
    return top


def plats(sink):
    import glob
    t0 = time.monotonic()
    rows = ok = 0
    for p in sorted(glob.glob(os.path.join(ROOT, 'atlas/corner/out/*.plat'))):
        rel = os.path.relpath(p, os.path.dirname(ROOT))
        for ln, line in enumerate(open(p)):
            t = line.split()
            if not t:
                continue
            n = int(t[0])
            rows += 1
            if n != 88:
                continue
            v = [int(x) for x in t[1:]]
            if len(v) != 2 * n:
                continue
            pairs = [(v[2 * i], v[2 * i + 1]) for i in range(n)]
            masks, depth = replay(pairs)
            if masks is None:
                continue
            if sink.add(masks, 'atlas_corner_plat', rel + '#L%d' % (ln + 1),
                        depth=depth, pairs=pairs):
                ok += 1
    sink.stats['plat'] = {'rows': rows, 'valid88_rows': ok,
                          'secs': round(time.monotonic() - t0, 1)}
    return sink.stats['plat']


def census_pkl(sink):
    """e15's Run-A census population: the 17,283 baseline."""
    p = os.path.join(ROOT, 'experiments/e15_campaign3/tools/pop88.pkl')
    pop = pickle.load(open(p, 'rb'))
    got = set()
    for path, gm in pop:
        h = sink.add(gm, 'e15_census_pop88', os.path.relpath(path, os.path.dirname(ROOT)))
        if h:
            got.add(h)
    sink.stats['e15_census'] = {'rows': len(pop), 'admitted': len(got)}
    return sink.stats['e15_census']


def bank_jsonl(sink, relpath, source, extract, prefilter=None, label=None):
    p = os.path.join(ROOT, relpath)
    if not os.path.exists(p):
        sink.stats[source] = {'MISSING': relpath}
        return sink.stats[source]
    t0 = time.monotonic()
    rows = ok = 0
    with open(p, 'rb') as f:
        for i, raw in enumerate(f):
            rows += 1
            if prefilter and prefilter not in raw:
                continue
            try:
                o = json.loads(raw)
            except Exception:
                continue
            m = extract(o)
            if not m:
                continue
            sink.add(m, source, relpath + '#L%d' % (i + 1))
            ok += 1
    sink.stats[source] = {'file': relpath, 'rows': rows, 'admitted': ok,
                          'secs': round(time.monotonic() - t0, 1)}
    return sink.stats[source]


def bank_glob(sink, pattern, source, extract, prefilter=None):
    """Same as bank_jsonl over a glob of population dumps."""
    import glob
    t0 = time.monotonic()
    rows = ok = 0
    files = sorted(glob.glob(os.path.join(ROOT, pattern)))
    for p in files:
        rel = os.path.relpath(p, ROOT)
        with open(p, 'rb') as f:
            for i, raw in enumerate(f):
                rows += 1
                if prefilter and prefilter not in raw:
                    continue
                try:
                    o = json.loads(raw)
                except Exception:
                    continue
                m = extract(o)
                if not m:
                    continue
                sink.add(m, source, rel + '#L%d' % (i + 1))
                ok += 1
    sink.stats[source] = {'glob': pattern, 'files': len(files), 'rows': rows,
                          'admitted': ok, 'secs': round(time.monotonic() - t0, 1)}
    return sink.stats[source]


def basin_laterals(sink):
    """fleet1 laneD: the 99 'lateral 88s never compiled'.

    Each HIT-3 row is {triple deleted, 3 gates paid}.  The mask set is therefore
    materialisable WITHOUT re-solving: parent \\ triple u gates.  We also check
    realisability greedily (every non-input mask must be an XOR of two earlier
    available masks) so an unbuildable set is never admitted.
    """
    par = {
        'basin_88at6.jsonl': 'evidence/circuits/mixcolumns_88gates_depth6.json',
        'basin_88at5fs.jsonl': 'evidence/circuits/mixcolumns_88gates_depth5_fromscratch.json',
    }
    out = {}
    for fn, pj in par.items():
        p = os.path.join(ROOT, 'fleet1/laneD_completions', fn)
        if not os.path.exists(p):
            out[fn] = 'MISSING'
            continue
        pairs = [tuple(x) for x in load_index_pairs(json.load(open(os.path.join(ROOT, pj))))]
        pmask, _ = replay(pairs)
        hits = admitted = unreal = 0
        for i, raw in enumerate(open(p, 'rb')):
            if b'HIT-3' not in raw:
                continue
            o = json.loads(raw)
            hits += 1
            tri = [int(x, 16) for x in o['triple']]
            new = [int(x, 16) for x in o['gates']]
            ms = list(pmask)
            okdel = True
            for t in tri:
                if t in ms:
                    ms.remove(t)
                else:
                    okdel = False
            if not okdel or len(ms) + len(new) != 88:
                continue
            ms = ms + new
            if not realisable(ms):
                unreal += 1
                continue
            if sink.add(ms, 'fleet1-4_basin_lateral',
                        'slp-plateau-search/fleet1/laneD_completions/%s#L%d' % (fn, i + 1),
                        note='materialised from parent %s minus triple plus paid gates' % pj):
                admitted += 1
        out[fn] = {'hit3_rows': hits, 'admitted': admitted, 'unrealisable': unreal}
    sink.stats['basin_lateral'] = out
    return out


def realisable(masks):
    """Greedy topological check: can this multiset be built by 2-input XORs
    from the 32 inputs?  (Same idea as experiments_early's e_upstream check.)"""
    avail = set(1 << i for i in range(32))
    rem = list(masks)
    prog = True
    while rem and prog:
        prog = False
        nxt = []
        for m in rem:
            got = False
            for s in avail:
                if (m ^ s) in avail:
                    got = True
                    break
            if got:
                avail.add(m)
                prog = True
            else:
                nxt.append(m)
        rem = nxt
    return not rem


# ----------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', required=True)
    a = ap.parse_args()
    s = Sink()
    if a.stage == 'curated':
        print('walk   ', walk_files(s), flush=True)
        s.dump('curated')
        print('plat   ', plats(s), flush=True)
        s.dump('curated')
        print('basin  ', basin_laterals(s), flush=True)
        s.dump('curated')
        print('census ', census_pkl(s), flush=True)
        s.dump('curated')
        print('DISTINCT after curated:', len(s.d), flush=True)
    elif a.stage == 'banks':
        assert s.load('curated'), 'run --stage curated first'
        print('beat88 ', bank_jsonl(
            s, 'beat88/methods/m2_oracle/runs/pop88_worklist.jsonl',
            'beat88_pop88_worklist',
            lambda o: [int(x, 16) for x in o['masks_hex'].split(',')]
            if o.get('gates') == 88 and o.get('masks_hex') else None,
            prefilter=b'masks_hex'), flush=True)
        s.dump('curated')
        print('c87new ', bank_jsonl(
            s, 'campaign_87/agents/hunt-deeper/population88_new.jsonl',
            'campaign_87_population88_new',
            lambda o: o if isinstance(o, list) and len(o) == 88 else None), flush=True)
        s.dump('curated')
        print('c87l89 ', bank_jsonl(
            s, 'campaign_87/hunt87_layer89/found88.jsonl',
            'campaign_87_found88_layer89',
            lambda o: o.get('masks') if o.get('gates') == 88 else None,
            prefilter=b'"masks"'), flush=True)
        s.dump('curated')
        print('c87merg', bank_glob(
            s, 'campaign_87/agents/merged-engine/runs_hunt/*.pop.jsonl',
            'campaign_87_merged_engine_pop',
            lambda o: o if isinstance(o, list) and len(o) == 88 else None), flush=True)
        s.dump('curated')
        print('DISTINCT after banks:', len(s.d), flush=True)
    elif a.stage == 'nrpa':
        assert s.load('curated')
        print('nrpa   ', bank_jsonl(
            s, 'campaign_87/wave5_2026-08-04/nrpa/out/sub92.jsonl',
            'campaign_87_nrpa_sub92',
            lambda o: o.get('masks') if o.get('gates') == 88 else None,
            prefilter=b'"gates": 88,'), flush=True)
        s.dump('curated')
        print('DISTINCT after nrpa:', len(s.d), flush=True)
    elif a.stage == 'emit':
        assert s.load('curated')
        emit(s)
    else:
        raise SystemExit('unknown stage')


def emit(s):
    out = os.path.join(ROOT, 'wrapup', 'corpus88_index.jsonl')
    census = s.per_source.get('e15_census_pop88', set())
    alarms = []
    depth_hist = {}
    dupmask = []
    with open(out, 'w') as f:
        for h in sorted(s.d):
            r = dict(s.d[h])
            r['in_e15_census'] = h in census
            f.write(json.dumps(r, separators=(',', ':')) + '\n')
            if r.get('B_theorem_ok') is False:
                alarms.append(r)
            if r['n_masks_distinct'] != 88:
                dupmask.append(r)
            d = r['depth']
            depth_hist[d] = depth_hist.get(d, 0) + 1
    srcs = sorted(s.per_source)
    summary = {
        'distinct_total': len(s.d),
        'per_source': {k: len(v) for k, v in sorted(s.per_source.items())},
        'per_source_unique_to_it': {
            k: len(v - set().union(*[s.per_source[o] for o in srcs if o != k]))
            for k, v in s.per_source.items()},
        'overlap_matrix': {a: {b: len(s.per_source[a] & s.per_source[b])
                               for b in srcs} for a in srcs},
        'e15_census_size': len(census),
        'not_in_e15_census': len(s.d) - len(census),
        'census_rows_not_recovered': 0,
        'depth_known_hist': {str(k): v for k, v in sorted(
            depth_hist.items(), key=lambda t: (t[0] is None, t[0]))},
        'B_checked_full': sum(1 for r in s.d.values() if 'B' in r),
        'B_eq_56': sum(1 for r in s.d.values() if r.get('B') == 56),
        'B_ALARMS': alarms,
        'duplicate_mask_sets': dupmask[:20],
        'n_duplicate_mask_sets': len(dupmask),
        'stats': s.stats,
    }
    with open(os.path.join(ROOT, 'wrapup', 'work', 'summary.json'), 'w') as f:
        json.dump(summary, f, indent=1, default=str)
    print('wrote', out, len(s.d), 'rows')
    print(json.dumps({k: v for k, v in summary.items()
                      if k not in ('overlap_matrix',)}, indent=1, default=str))


if __name__ == '__main__':
    main()
