# DRAT proofs

An UNSAT verdict is a solver's word for it. A **DRAT refutation** is a
certificate: a checker replays it against the CNF, deriving each lemma by unit
propagation, and needs to trust nothing whatever about the solver that wrote it.

This directory holds refutations for **every level of the ladder this pack can
afford to prove**, plus the positive control's negative leg.

---

## What is here

Proofs are shipped `xz`-compressed. Decompress before checking — `drat-trim`
reads plain text.

| level | CNF it refutes | lemmas | deletions | proof, uncompressed | `.xz` | emit time |
|---|---|---|---|---|---|---|
| k = 6 (control) | `../positive_control/k6_SUB_U4tgts.cnf` | 18 711 | 33 794 | 7 848 148 B | 333 196 B, **shipped** | 0.98 s |
| k = 9 | `../cnf/k9_joint_W3U4.cnf` | 23 230 | 42 275 | 9 182 138 B | 357 264 B, **shipped** | 1.45 s |
| k = 10 | `../cnf/k10_joint_W3U4.cnf` | 148 849 | 206 209 | 135 064 503 B | 6 342 520 B, **shipped** | 15.96 s |
| k = 11 | `../cnf/k11_joint_W3U4.cnf` | 640 177 | 643 793 | 845 830 878 B | 40 038 556 B, **not shipped** | 110.39 s |

### Why k = 11's proof is not in the repository

Its compressed refutation is **40 MB**, four times the rest of this repository
put together, and it would sit in the history of every clone for ever. It is
cheaper to make than to fetch: **110 s** of single-core proof logging, from the
same shipped CNF, with one command.

```bash
cd encodings
sh run_proofs.sh                      # emits k = 6, 9, 10 and 11
# or just the one:
python3 code/emit_proof.py cnf/k11_joint_W3U4.cnf --out proofs/k11_joint_W3U4.drat
xz -k proofs/k11_joint_W3U4.drat
```

The digests below record exactly what was emitted here on 2026-09-01, so a
regenerated file can be compared against them — but see the last section: DRAT
output is not bit-reproducible across solver builds, so reproduce the
`s VERIFIED`, not the digest. `SHA256SUMS` at the pack root covers the three
shipped proofs only.

**k = 12, 13 and 14 carry no proof.** k = 14's solve alone was ≈ 99 core-hours
and its refutation would be very large. So the decisive level of the theorem
rests on complete solvers being correct rather than on a checked certificate.
That is the honest boundary of this pack's evidence.

## Digests

Check the `.xz` you received, then check the `.drat` you decompressed. The
second digest is the one that matters: it fixes exactly what a checker checks.

`.drat.xz`, as shipped:

```
1f06855aa60fdb6f8b0735b61c740fbd9f559af954b24d05225cf7775e9c5efb  k6_SUB_U4tgts.drat.xz
72018d6f0ee10d2c235aaa7df0a4b512843a66d8f5522785277d9f137265914b  k9_joint_W3U4.drat.xz
5ae77838b916b897d240ff91550a62a39934649bcffd110e8e96abf7399e3080  k10_joint_W3U4.drat.xz
3e5e01f71d3c0b68e7cbfe389d52a0df10084cf74c1efd14c05fc77fdd307494  k11_joint_W3U4.drat.xz
```

`.drat`, after `xz -dk`:

```
ecbd46f55434a2070ce41108310d1d24653fbc65ee2ac1027b8c336aa57166e8  k6_SUB_U4tgts.drat
3b7134efb93eddffa0cc337e814e9215a7b7011aaa9a2c0104275736a717f2ca  k9_joint_W3U4.drat
e6b0692b6a0248093e80d4014531096089f889d47c7d5b74fec17475396c914c  k10_joint_W3U4.drat
888b38c3ac43e9bb57a1b00238c9b168889b11587e0bf59a30a0191f176c039b  k11_joint_W3U4.drat
```

The `.xz` digests are also in the pack's `SHA256SUMS`.

## Checking one — the exact commands

`drat-trim` is a single C file with no dependencies.

```bash
git clone https://github.com/marijnheule/drat-trim && (cd drat-trim && make)

cd <pack root>
xz -dk proofs/k9_joint_W3U4.drat.xz
sha256sum proofs/k9_joint_W3U4.drat          # compare with the table above
drat-trim cnf/k9_joint_W3U4.cnf proofs/k9_joint_W3U4.drat
# expect the last line: s VERIFIED
```

The other two shipped proofs, verbatim:

```bash
xz -dk proofs/k6_SUB_U4tgts.drat.xz
drat-trim positive_control/k6_SUB_U4tgts.cnf proofs/k6_SUB_U4tgts.drat

xz -dk proofs/k10_joint_W3U4.drat.xz
drat-trim cnf/k10_joint_W3U4.cnf proofs/k10_joint_W3U4.drat
```

And k = 11, after regenerating it as above:

```bash
drat-trim cnf/k11_joint_W3U4.cnf proofs/k11_joint_W3U4.drat
```

`drat-trim` needs a `-t` larger than its default timeout for the bigger proofs
(e.g. `-t 20000`), and roughly the proof's own size in RAM. For an LRAT
certificate that `cake_lpr` or `lrat-check` can consume:

```bash
drat-trim cnf/k11_joint_W3U4.cnf proofs/k11_joint_W3U4.drat -L /tmp/k11.lrat
```

Note the argument order: **CNF first, proof second.** A swapped pair is the
usual cause of a confusing failure.

## What was and was not done here

**Emitted here.** All four proofs — the three shipped and k = 11 — were produced
on the machine that assembled this pack, by `../code/emit_proof.py`, which parses the clauses **out of the
shipped DIMACS file** — so each certificate refutes the shipped artifact, not
something rebuilt in memory. Solver: CaDiCaL 1.9.5 through `python-sat`, one
core, `nice -n 19`. Proof logging cost roughly 1.5× the plain solve.

**Validated here — structurally.** `../code/check_proof_format.py` confirmed for
each file that every line parses as a clause terminated by `0` (with `d ` for
deletions), that no variable exceeds the CNF's variable count, and that the file
**ends in the empty clause**, which is what makes it a refutation and not a log.
All four: `WELL-FORMED DRAT`. Reports in `../results/proof_format_*.json`.

**Not checked here.** No DRAT checker is installed on this machine. These proofs
have *not* been verified — the commands above are how anyone does that, and the
published digests mean what they check is exactly what was emitted. Do not read
"well-formed" as "verified"; the format checker says as much about itself in its
own docstring.

## Regenerating instead of downloading

Every proof here is reproducible in the time given in the table, which for three
of the four is faster than fetching the file:

```bash
sh run_proofs.sh        # emit all four, validate each, compress
```

DRAT output is not bit-reproducible across solver versions or builds — a
different CaDiCaL will emit a different, equally valid refutation. Reproduce the
*verdict* and the `s VERIFIED`, not the digest.
