# `bounds/gte56/` — how to run it

Everything below is typed from the **pack root** (`bounds/`). Python 3, standard
library only. One C file, compiled with any C compiler.

## Files

| file | what it is |
|---|---|
| `STATEMENT.md` | the claim, the technique, the proof sketch |
| `HOW.md` | the machinery: which parts are arithmetic, how the searcher works, what is taken on trust |
| `cert56.json` | the certificate: keep-set, symmetry, `m`, `e_K`, provenance |
| `check_gte56.py` | the checker — reads `../matrix.txt` and the certificate |
| `mine.c` | the extras-tree searcher (single file, no dependencies) |

---

## 1. The closed-form check (the certificate)

```
python3 gte56/check_gte56.py
```

Expected output — this is the real transcript, not a paraphrase:

```
matrix        : matrix.txt  (32 rows x 32 columns)
certificate   : gte56/cert56.json  (cert5)
technique     : adaptive gate elimination (Lemma F + Theorem N), level m = 1

A. matrix hypotheses
  [PASS] A1 square                                                  32 rows, 32 columns
  [PASS] A2 columns nonzero                                         32/32 nonzero
  [PASS] A3 columns pairwise distinct                               32 distinct
  [PASS] A4 every row has weight >= 2                               min row weight = 5
  [PASS] A5 rows pairwise distinct                                  32 distinct targets

B. the certificate symmetry is an automorphism of the matrix
  [PASS] B1 sigma is a permutation of the columns
  [PASS] B2 M[sigma(r)][sigma(c)] == M[r][c] for all r,c            checked all 1024 entries
  [PASS] B3 sigma has order 4

C. Theorem-N admissibility of K and all its sigma-conjugates
  [PASS] C1 |K|=14 admissible   ok  K=[2, 4, 7, 9, 15, 18, 20, 21, 22, 24, 25, 29, 30, 31]
  [PASS] C2 |K|=14 admissible   ok  K=[0, 1, 5, 6, 7, 10, 12, 15, 17, 23, 26, 28, 29, 30]
  [PASS] C3 |K|=14 admissible   ok  K=[2, 4, 5, 6, 8, 9, 13, 14, 15, 18, 20, 23, 25, 31]
  [PASS] C4 |K|=14 admissible   ok  K=[1, 7, 10, 12, 13, 14, 16, 17, 21, 22, 23, 26, 28, 31]

D. level-m covering hypothesis (m = 1)
  [PASS] D1 every column is avoided by some conjugate               intersection of the 4 conjugates = {}

E. necessary screen on the claimed e_K
  [PASS] E1 e_K <= jam(K)   e_K = 5, jam(K) = 8, free closure 24/32, |avail| = 38

F. the bound arithmetic
  [PASS] F1 m + (n-|K|) + #targets + e_K == stated bound            1 + 18 + 32 + 5 = 56
  [PASS] F2 stated terms match the matrix and certificate

G. control: the recorded 4-extra witness for the FAILING keep-set
  [PASS] G1 witness completes cert1 with 4 extras   extras ['0x0003', '0x0042', '0x0082', '0x004a'], undone targets = 0  => minE(cert1) <= 4
  [PASS] G2 the same keep-set is NOT completable with 0 extras      undone targets with no extras = 5

H. e_K: the one term that is not a closed-form check
     ... provenance of the depth-4 exhaustion ...

==========================================================================
RESULT: every closed-form hypothesis of Theorem N holds for this matrix.
  Self-contained here            :  L(M) >= 1 + 18 + 32 + e_K
  With e_K = 5 (cited exhaustion) :  L(M) >= 56
```

| | |
|---|---|
| **measured wall time (re-run 2026-09-01)** | **0.03 s** (0.11 s on a cold page cache) |
| historical cost | the structural hypotheses were hand-checked and then machine-checked at negligible cost; they were never the expensive half |

---

## 2. Re-deriving `e_K` yourself — the exhaustion

Compile the searcher once:

```
cc -O2 -o gte56/mine gte56/mine.c
```

### Depth 3 → `minE >= 4` → `L(M) >= 55`

```
python3 gte56/check_gte56.py --minE-depth 3
```

Expected output (the last three lines; sections A–G are as above):

```
     re-running the exhaustion at depth 3 ...
     k=14 depth=3 jam=8 shard=0/1 nodes=5784927 result=NONE   (0.8 s)   <- second run: (0.4 s), same node count
  [PASS] H1 depth-3 exhaustion finds no completion => minE >= 4     re-derived bound with e_K = 4 is 55
```

| | |
|---|---|
| **measured wall time (re-run 2026-09-01, twice)** | **0.47 s** and **0.9 s**, of which 0.4 s / 0.8 s in the searcher; one core |
| nodes | **5,784,927**, byte-identical on both runs — the searcher is deterministic, so the node count is a reproducible fingerprint even when the wall time is not |
| historical cost | 200–730 s per certificate in the originating lane's Python searcher (its depth-3 pass over cert5 took 675 s / 8,162,465 nodes); ~15 s in the referee's C searcher |

### Depth 4 → `minE >= 5` → `L(M) >= 56`

```
python3 gte56/check_gte56.py --minE-depth 4
```

Expected output (the last three lines):

```
     re-running the exhaustion at depth 4 ...
     k=14 depth=4 jam=8 shard=0/1 nodes=1895523772 result=NONE   (166.0 s)   <- second run: (156.8 s), same node count
  [PASS] H1 depth-4 exhaustion finds no completion => minE >= 5     re-derived bound with e_K = 5 is 56
```

| | |
|---|---|
| **measured wall time (re-run 2026-09-01, twice)** | **166.0 s** and **156.8 s**, one core, `nice -n 19` (the spread is machine load) |
| nodes | **1,895,523,772**, identical on both runs |
| historical cost | 16 workers, 114 shards per certificate, run twice: `9.43e10` nodes (unpruned C) and `4.75e9` nodes (pruned Python), both `NO COMPLETION` on all 511/511 root branches |

**How this run differs from the historical one.** The 166 s run here is the
*pruned* code path (`-p` last-level restriction and `-o` canonical order, both
proved sound in the header comment of `mine.c`). It reproduces the published
result single-core because it is neither sharded nor deliberately unpruned. The
value of the historical `9.43e10`-node run is that it used *no* prunings at all,
so the result does not depend on those two arguments being correct. That run is
cited, not reproduced here.

---

## 3. Running the machinery on a different matrix

`check_gte56.py --matrix YOURMATRIX.txt --cert YOURCERT.json` works on any 0/1
matrix file (one row per line, one character per column). `mine` likewise takes
an arbitrary target list:

```
gte56/mine <k> <t0,t1,...> <depth> [-p] [-o] [-w]
```

[`../validation/`](../validation/) does exactly this on small matrices whose
optimum is known exactly, and checks the bound never exceeds it.
