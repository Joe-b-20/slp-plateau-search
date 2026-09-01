/* delcert.c -- corpus-wide single-mask deletion-realisability certificate.
 *
 * For every mask set M (k masks, containing the 32 MixColumns targets) in a
 * flat binary file of k x uint32 records, and for every NON-TARGET mask m of M,
 * decide whether M \ {m} is realisable as an XOR-SLP over the 32 inputs.
 *
 * Semantics are a literal port of the project's own two checks:
 *   local necessary condition  = the project's Python near-87 check, part 2
 *   full greedy closure        = the project's Python realisability check
 * Both are reproduced verbatim in tools/pycheck.py, which exists so this
 * port can be diffed against the Python it ports on the same records.
 *
 * Port notes (why this is the same computation, faster):
 *  - A = inputs u M.  Any mask ever available to the greedy lies in A, so
 *    "exists s in avail with x^s in avail" is exactly "exists a pair (a,b) with
 *    a^b = x and a,b both in A and both available".  Pair lists P(x) over A are
 *    therefore precomputed once per set (the same `deriv` table the Python
 *    builds) and reused by the local filter and by all k-32 greedy runs.
 *  - Local filter: the Python marks m bad iff some x != m has ALL its pairs
 *    containing m.  Equivalently, crit(x) = intersection of the element sets of
 *    x's pairs (at most 2 elements, and never x itself, since a^b=x with a=x
 *    forces b=0 which is not in A); m is bad iff m in crit(x) for some x.  The
 *    "x != m" guard is therefore vacuous, exactly as in the Python.
 *  - The greedy adds a mask the moment it becomes derivable inside the pass,
 *    like the Python; the closure is monotone so the fixpoint is order-free.
 *
 * Build: gcc -O2 -o delcert delcert.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXK 96            /* record length (masks per set) upper bound      */
#define MAXU 128           /* 32 inputs + MAXK, must fit two uint64 words    */
#define MAXP 64            /* pairs per mask; <= (32+MAXK)/2 = 64            */
#define HB 9
#define HSZ (1 << HB)      /* 512-slot open-addressing table                 */

static uint32_t targets[64];
static int ntargets = 0;

static uint32_t hval[HSZ];
static int16_t hidx[HSZ];

static inline void h_clear(void) { memset(hval, 0, sizeof hval); }

static inline void h_put(uint32_t v, int i)
{
    uint32_t s = (v * 2654435761u) >> (32 - HB);
    while (hval[s]) {
        if (hval[s] == v) return;          /* duplicate value: keep first */
        s = (s + 1) & (HSZ - 1);
    }
    hval[s] = v;
    hidx[s] = (int16_t)i;
}

static inline int h_get(uint32_t v)
{
    uint32_t s = (v * 2654435761u) >> (32 - HB);
    while (hval[s]) {
        if (hval[s] == v) return hidx[s];
        s = (s + 1) & (HSZ - 1);
    }
    return -1;
}

#define BIT(av, i)  ((av)[(i) >> 6] >> ((i) & 63) & 1ull)
#define SET(av, i)  ((av)[(i) >> 6] |= 1ull << ((i) & 63))

int main(int argc, char **argv)
{
    const char *binpath = NULL, *tgtpath = NULL, *outpath = NULL, *tag = "0";
    long start = 0, count = -1, every = 20000;
    int K = 88;

    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--bin")) binpath = argv[++i];
        else if (!strcmp(argv[i], "--targets")) tgtpath = argv[++i];
        else if (!strcmp(argv[i], "--out")) outpath = argv[++i];
        else if (!strcmp(argv[i], "--tag")) tag = argv[++i];
        else if (!strcmp(argv[i], "--start")) start = atol(argv[++i]);
        else if (!strcmp(argv[i], "--count")) count = atol(argv[++i]);
        else if (!strcmp(argv[i], "--every")) every = atol(argv[++i]);
        else if (!strcmp(argv[i], "--k")) K = atoi(argv[++i]);
        else { fprintf(stderr, "bad arg %s\n", argv[i]); return 2; }
    }
    if (!binpath || !tgtpath) { fprintf(stderr, "need --bin --targets\n"); return 2; }
    if (K < 33 || K > MAXK) { fprintf(stderr, "bad --k\n"); return 2; }

    FILE *tf = fopen(tgtpath, "r");
    if (!tf) { perror("targets"); return 2; }
    { unsigned x; while (fscanf(tf, "%x", &x) == 1) targets[ntargets++] = x; }
    fclose(tf);
    if (ntargets != 32) { fprintf(stderr, "expected 32 targets, got %d\n", ntargets); return 2; }

    FILE *f = fopen(binpath, "rb");
    if (!f) { perror("bin"); return 2; }
    fseek(f, 0, SEEK_END);
    long fsz = ftell(f);
    long nrec = fsz / (long)(4 * K);
    if (count < 0 || start + count > nrec) count = nrec - start;
    fseek(f, start * (long)(4 * K), SEEK_SET);

    FILE *out = outpath ? fopen(outpath, "a") : stdout;
    if (!out) { perror("out"); return 2; }

    uint32_t S[MAXK], A[MAXU];
    uint16_t P[MAXK][MAXP];
    uint8_t np[MAXK];
    uint8_t crit[MAXU];
    int rem[MAXK];
    int U = 32 + K;
    if (U > MAXU) { fprintf(stderr, "U too big\n"); return 2; }

    long long tested = 0, survivors = 0, realisable = 0;
    long done = 0, badtarget = 0, allfail_sets = 0;
    struct timespec t0, tn;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    for (long r = 0; r < count; r++) {
        if (fread(S, 4, K, f) != (size_t)K) { fprintf(stderr, "short read at %ld\n", r); break; }
        long ridx = start + r;

        for (int i = 0; i < 32; i++) A[i] = 1u << i;
        for (int i = 0; i < K; i++) A[32 + i] = S[i];
        h_clear();
        for (int i = 0; i < U; i++) h_put(A[i], i);

        int ntg = 0;
        uint8_t istgt[MAXK];
        memset(istgt, 0, sizeof istgt);
        for (int i = 0; i < K; i++)
            for (int t = 0; t < 32; t++)
                if (S[i] == targets[t]) { istgt[i] = 1; ntg++; break; }
        if (ntg != 32) badtarget++;

        /* pair lists over A */
        for (int ix = 0; ix < K; ix++) {
            uint32_t x = S[ix];
            int n = 0;
            for (int a = 0; a < U; a++) {
                int b = h_get(x ^ A[a]);
                if (b > a) {
                    if (n >= MAXP) { fprintf(stderr, "PAIR OVERFLOW rec %ld\n", ridx); return 3; }
                    P[ix][n++] = (uint16_t)((a << 8) | b);
                }
            }
            np[ix] = (uint8_t)n;
        }

        /* local necessary condition: crit(x) = intersection over x's pairs */
        memset(crit, 0, sizeof crit);
        int allfail = 0;
        for (int ix = 0; ix < K; ix++) {
            if (np[ix] == 0) { allfail = 1; break; }
            int c0 = P[ix][0] >> 8, c1 = P[ix][0] & 255;
            for (int p = 1; p < np[ix] && (c0 >= 0 || c1 >= 0); p++) {
                int a = P[ix][p] >> 8, b = P[ix][p] & 255;
                if (c0 >= 0 && c0 != a && c0 != b) c0 = -1;
                if (c1 >= 0 && c1 != a && c1 != b) c1 = -1;
            }
            if (c0 >= 0) crit[c0] = 1;
            if (c1 >= 0) crit[c1] = 1;
        }
        if (allfail) allfail_sets++;

        for (int im = 0; im < K; im++) {
            if (istgt[im]) continue;              /* deleting a target loses an output */
            tested++;
            if (allfail || crit[32 + im]) continue;
            survivors++;

            uint64_t av[2] = {0xffffffffull, 0};  /* the 32 inputs */
            int nrem = 0;
            for (int ix = 0; ix < K; ix++) if (ix != im) rem[nrem++] = ix;
            int prog = 1;
            while (nrem && prog) {
                prog = 0;
                int w = 0;
                for (int i = 0; i < nrem; i++) {
                    int ix = rem[i], ok = 0;
                    for (int p = 0; p < np[ix]; p++) {
                        int a = P[ix][p] >> 8, b = P[ix][p] & 255;
                        if (BIT(av, a) && BIT(av, b)) { ok = 1; break; }
                    }
                    if (ok) { SET(av, 32 + ix); prog = 1; }
                    else rem[w++] = ix;
                }
                nrem = w;
            }
            if (nrem == 0) {
                realisable++;
                fprintf(out, "{\"FIRING\":1,\"shard\":\"%s\",\"record\":%ld,"
                        "\"deleted_mask\":\"%08x\",\"masks\":[", tag, ridx, S[im]);
                for (int i = 0; i < K; i++)
                    fprintf(out, "%s\"%08x\"", i ? "," : "", S[i]);
                fprintf(out, "]}\n");
                fflush(out);
                fprintf(stderr, "!!! FIRING record %ld deleted %08x\n", ridx, S[im]);
                fflush(stderr);
            }
        }
        done++;
        if (every > 0 && (done % every == 0 || r == count - 1)) {
            clock_gettime(CLOCK_MONOTONIC, &tn);
            double el = (tn.tv_sec - t0.tv_sec) + 1e-9 * (tn.tv_nsec - t0.tv_nsec);
            fprintf(out, "{\"shard\":\"%s\",\"start\":%ld,\"count\":%ld,\"done\":%ld,"
                    "\"tested\":%lld,\"local_pass\":%lld,\"realisable\":%lld,"
                    "\"sets_not_32_targets\":%ld,\"sets_local_allfail\":%ld,"
                    "\"secs\":%.1f,\"sets_per_sec\":%.1f}\n",
                    tag, start, count, done, tested, survivors, realisable,
                    badtarget, allfail_sets, el, done / (el > 0 ? el : 1));
            fflush(out);
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &tn);
    double el = (tn.tv_sec - t0.tv_sec) + 1e-9 * (tn.tv_nsec - t0.tv_nsec);
    fprintf(out, "{\"DONE\":1,\"shard\":\"%s\",\"start\":%ld,\"count\":%ld,\"done\":%ld,"
            "\"tested\":%lld,\"local_pass\":%lld,\"realisable\":%lld,"
            "\"sets_not_32_targets\":%ld,\"sets_local_allfail\":%ld,\"secs\":%.1f}\n",
            tag, start, count, done, tested, survivors, realisable,
            badtarget, allfail_sets, el);
    fflush(out);
    return 0;
}
