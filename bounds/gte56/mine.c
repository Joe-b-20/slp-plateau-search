/* mine.c -- exhaustive minimum-extras searcher (proof-side lane, from scratch).
 *
 * Inputs e_0..e_{k-1} in F2^k; 32 targets (distinct, weight>=2).  A mask set G
 * is realizable if it can be ordered so every element is an input or the XOR of
 * two strictly earlier elements.  minE = min |G \ T| over realizable G >= T.
 * Deciding "minE >= d+1" = exhausting all uses of <= d extras.
 *
 * Search model (re-derived, not copied):
 *  - state = committed mask set `avail`, always closed under "a target that is
 *    the XOR of two avail masks is itself committed" (greedy target closure is
 *    WLOG: a realizable G contains every target, so committing a derivable
 *    target early only enlarges avail, which never destroys a later derivation);
 *  - the next non-target element of a realizable ordering is a pairsum of avail,
 *    so branching over distinct pairsums is complete;
 *  - -p LAST-LEVEL restriction: with one extra left, adding it must start the
 *    final cascade, so it equals t^a for an undone target t and a in avail;
 *  - -o CANONICAL ORDER: for a successful extras set E, explore it in the order
 *    "smallest currently-addable member of E first" (the target closure has a
 *    unique fixpoint per E, so success depends only on the set).  If candidate x
 *    was already addable in the PARENT state and x < the extra just chosen, that
 *    branch is a permutation of one explored elsewhere.  Sound; up to d! saving.
 *
 * usage: mine <k> <t0,...> <depth> [-p] [-o] [-w] [-s shard -n nshards]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int K, NMASK, NT = 32;
static uint32_t TGT[32];
static unsigned char *inav;
static uint32_t *stamp;
static uint32_t stampctr = 0;
static uint32_t avail[4096];
static int navail;
static unsigned char tdone[32];
static int ndone;
static long long nodes = 0;
static int want_witness = 0, prune_last = 0, order_prune = 0;
static uint32_t witness[16];

#define MAXLVL 10
static uint32_t *lvl_stamp[MAXLVL];
static uint32_t lvl_id[MAXLVL];
static uint32_t nodectr = 0;

static void add_mask(uint32_t m) { inav[m] = 1; avail[navail++] = m; }

static void commit(uint32_t m)
{
    int start = navail;
    add_mask(m);
    for (int i = start; i < navail; i++) {
        uint32_t a = avail[i];
        for (int t = 0; t < NT; t++) {
            if (tdone[t]) continue;
            uint32_t x = TGT[t] ^ a;
            if (x && inav[x]) { tdone[t] = 1; ndone++; add_mask(TGT[t]); }
        }
    }
}

static void undo(int mark, unsigned char *sv, int sn)
{
    for (int i = mark; i < navail; i++) inav[avail[i]] = 0;
    navail = mark;
    memcpy(tdone, sv, NT);
    ndone = sn;
}

static int search(int depth, int shard, int nshards, int toplevel, int lvl, uint32_t lastx)
{
    nodes++;
    if (ndone == NT) return 1;
    if (depth == 0) return 0;

    unsigned char savedone[32];
    int savendone = ndone, mark = navail;
    memcpy(savedone, tdone, NT);
    uint32_t myid = ++nodectr;

    if (prune_last && depth == 1) {
        uint32_t myst = ++stampctr;
        for (int i = 0; i < navail; i++)
            for (int j = i + 1; j < navail; j++) {
                uint32_t x = avail[i] ^ avail[j];
                if (x && !inav[x]) stamp[x] = myst;
            }
        uint32_t tried = ++stampctr;
        for (int t = 0; t < NT; t++) {
            if (tdone[t]) continue;
            for (int i = 0; i < navail; i++) {
                uint32_t x = TGT[t] ^ avail[i];
                if (!x || inav[x]) continue;
                if (stamp[x] != myst) continue;        /* not a pairsum, or already tried */
                stamp[x] = tried;
                if (order_prune && lvl > 0 && x < lastx &&
                    lvl_stamp[lvl - 1][x] == lvl_id[lvl - 1]) continue;
                commit(x);
                nodes++;
                if (ndone == NT) { if (want_witness) witness[0] = x; return 1; }
                undo(mark, savedone, savendone);
            }
        }
        return 0;
    }

    uint32_t myst = ++stampctr;
    int cnt = 0;
    static uint32_t buf[3][8192];
    uint32_t local[8192];
    uint32_t *cand = (depth <= 3) ? buf[depth - 1] : local;
    for (int i = 0; i < navail; i++)
        for (int j = i + 1; j < navail; j++) {
            uint32_t x = avail[i] ^ avail[j];
            if (!x || inav[x] || stamp[x] == myst) continue;
            stamp[x] = myst;
            if (order_prune && lvl > 0 && x < lastx &&
                lvl_stamp[lvl - 1][x] == lvl_id[lvl - 1]) continue;
            cand[cnt++] = x;
        }
    if (order_prune && lvl < MAXLVL) {
        lvl_id[lvl] = myid;
        for (int c = 0; c < cnt; c++) lvl_stamp[lvl][cand[c]] = myid;
    }
    for (int c = 0; c < cnt; c++) {
        if (toplevel && nshards > 1 && (c % nshards) != shard) continue;
        commit(cand[c]);
        if (search(depth - 1, shard, nshards, 0, lvl + 1, cand[c])) {
            if (want_witness) witness[depth - 1] = cand[c];
            return 1;
        }
        undo(mark, savedone, savendone);
    }
    return 0;
}

int main(int argc, char **argv)
{
    if (argc < 4) { fprintf(stderr, "usage: mine k t0,.. depth [-p][-o][-w][-s i -n N]\n"); return 2; }
    K = atoi(argv[1]); NMASK = 1 << K;
    char *p = argv[2]; int n = 0;
    while (*p && n < 32) { TGT[n++] = (uint32_t)strtoul(p, &p, 10); if (*p == ',') p++; }
    NT = n;
    int depth = atoi(argv[3]), shard = 0, nsh = 1;
    for (int i = 4; i < argc; i++) {
        if (!strcmp(argv[i], "-p")) prune_last = 1;
        else if (!strcmp(argv[i], "-o")) order_prune = 1;
        else if (!strcmp(argv[i], "-w")) want_witness = 1;
        else if (!strcmp(argv[i], "-s")) shard = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-n")) nsh = atoi(argv[++i]);
    }
    inav = calloc(NMASK, 1);
    stamp = calloc(NMASK, sizeof(uint32_t));
    for (int i = 0; i < MAXLVL; i++) lvl_stamp[i] = calloc(NMASK, sizeof(uint32_t));

    navail = 0; ndone = 0; memset(tdone, 0, sizeof tdone);
    for (int i = 0; i < K; i++) add_mask(1u << i);
    for (int i = 0; i < navail; i++) {
        uint32_t a = avail[i];
        for (int t = 0; t < NT; t++) {
            if (tdone[t]) continue;
            uint32_t x = TGT[t] ^ a;
            if (x && inav[x]) { tdone[t] = 1; ndone++; add_mask(TGT[t]); }
        }
    }
    int jam = NT - ndone;
    int r = search(depth, shard, nsh, 1, 0, 0);
    printf("k=%d depth=%d jam=%d shard=%d/%d nodes=%lld result=%s\n",
           K, depth, jam, shard, nsh, nodes, r ? "COMPLETION" : "NONE");
    if (r && want_witness) {
        printf("witness extras:");
        for (int i = depth - 1; i >= 0; i--) printf(" %u", witness[i]);
        printf("\n");
    }
    return r ? 1 : 0;
}
