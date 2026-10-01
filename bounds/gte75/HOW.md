# `bounds/gte75/` — how it works

Read `PROOF_NOTE_75.md`; this page is the map.

| step | what it proves | where in the note | what the machine does |
|---|---|---|---|
| gate accounting | G = 32 + x + y + h | section 1 | nothing |
| even span | x >= 24 in both orientations | section 2, fact F1 | enumerates the short graph-code words and every seven-packing (1,485,213 states for M, 91,485 for M^T) |
| transposition | L(M) = L(M^T); canonical accumulation trees; d_v <= 3 + 2 f_v | section 3 | nothing |
| odd-signal graph | exact edge counts; r_i <= 3; 32 <= 2h + y + z + C(q,2) | section 4, facts F2-F4 | Sidon check, triple histograms, full-value rank facts |
| universal lemma | h_C + Y >= 13 for every minimum circuit; L(M) >= 69 | section 5 | nothing |
| weighted degrees | Q = 2x'; inequality (B) | section 6 | nothing |
| double transposition | origin identity; x(T(T(C))) = x(C); y(T(T(C))) >= y(C); no odd helper leaves | section 7 | nothing (stress-tested) |
| bounded potential | 69, 70, 71 excluded | section 8 | `check72.py` (4, 12, 23 pairs) |
| steady regime | 72 excluded | section 9, fact F5 | `check73.py` (1,010 tuples; rho_6(M^T) = 28) |
| helper-type rows | 23 necessary linear inequalities per phase | section 10, facts F5-F14 | `finite_facts.py` (all facts), `check_dark_source.py` |
| certificates | 73 and 74 excluded | section 11 | `certify74.py` / `independent74.py` (484 certificates), `certify75.py` / `independent75.py` (4,057 certificates, 2,204 claims, 927 direct exclusions) |

The programs compute numbers about the fixed matrix and check integer certificates. They cannot check that
the inequalities are necessary conditions for circuits or that the potential argument is sound; that is the
text, sections 1-11, and it is what a reviewer must read (note, section 12).

Entry point: `sh checks/run_all.sh` from this directory (about 2 minutes), or the commands in `RUN.md`.
