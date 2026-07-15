# Harvest — parallel depth-ladder run (2026-07-13, ~21h)

Every rung's best circuit, re-verified independently against the GF(2^8)
oracle at its own depth cap. This directory is archived UNTOUCHED as paper
evidence.

| rung | cap | gates | actual depth | verified |
|---|---|---|---|---|
| d3 | 3 | 97 | 3 | YES |
| d4 | 4 | 94 | 4 | YES |
| d5 | 5 | 92 | 5 | YES |
| d6 | 6 | 91 | 6 | YES |
| d7 | 7 | 89 | 7 | YES |
| d8 | 8 | 90 | 6 | YES |
| d9 | 9 | 90 | 7 | YES |
| d10 | 10 | 89 | 6 | YES |
| d11 | 11 | 90 | 5 | YES |
| final | None | 90 | 5 | YES |

**Best overall (fewest gates, then shallowest): 89 gates @ depth 6 (d10).**

## Cascade timeline (from coordinator.log)
```
[     0.0s 13:58:29] LAUNCH d3       engine=anneal3 depth=3 start=scratch pid=1072331
[  7215.3s 15:58:45] TRIGGER d3 (timeout 7215s, seed=97) -> launch d4 at depth 4
[  7215.3s 15:58:45] LAUNCH d4       engine=lns depth=4 start=seed_from_d3.json pid=1117875
[ 11593.9s 17:11:43] TRIGGER d4 (hit 96<=96, seed=96) -> launch d5 at depth 5
[ 11593.9s 17:11:43] LAUNCH d5       engine=lns depth=5 start=seed_from_d4.json pid=1145668
[ 11731.2s 17:14:01] TRIGGER d5 (hit 95<=95, seed=95) -> launch d6 at depth 6
[ 11731.2s 17:14:01] LAUNCH d6       engine=lns depth=6 start=seed_from_d5.json pid=1146517
[ 11907.1s 17:16:57] TRIGGER d6 (hit 94<=94, seed=94) -> launch d7 at depth 7
[ 11907.1s 17:16:57] LAUNCH d7       engine=lns depth=7 start=seed_from_d6.json pid=1147597
[ 12709.1s 17:30:19] TRIGGER d7 (hit 93<=93, seed=93) -> launch d8 at depth 8
[ 12709.1s 17:30:19] LAUNCH d8       engine=lns depth=8 start=seed_from_d7.json pid=1153354
[ 16979.7s 18:41:29] TRIGGER d8 (hit 92<=92, seed=92) -> launch d9 at depth 9
[ 16979.7s 18:41:29] LAUNCH d9       engine=lns depth=9 start=seed_from_d8.json pid=1180335
[ 24181.3s 20:41:31] TRIGGER d9 (timeout 7202s, seed=92) -> launch d10 at depth 10
[ 24181.3s 20:41:31] LAUNCH d10      engine=lns depth=10 start=seed_from_d9.json pid=1225938
[ 27047.1s 21:29:17] TRIGGER d10 (hit 91<=91, seed=91) -> launch d11 at depth 11
[ 27047.1s 21:29:17] LAUNCH d11      engine=lns depth=11 start=seed_from_d10.json pid=1244306
[ 28006.8s 21:45:16] TRIGGER d11 (hit 90<=90, seed=90) -> launch FINAL (uncapped depth)
[ 28006.8s 21:45:16] LAUNCH final    engine=lns depth=none start=seed_from_d11.json pid=1250164
```
