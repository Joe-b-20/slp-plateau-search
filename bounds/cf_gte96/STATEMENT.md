# Cancellation-free circuits: `96 <= L_cf(M) <= 102`

## The claim

Same object as [`../cf_gte92/STATEMENT.md`](../cf_gte92/STATEMENT.md): an XOR-SLP is
**cancellation-free** when the two operand values of every gate have disjoint support, and
`L_cf(M)` is the minimum size of a cancellation-free XOR-SLP for MixColumns (`../matrix.txt`).

> **`L_cf(M) >= 96`.** A *split-price* certificate: a JSON table of integers keyed by
> (target, mask, split), checked in well under a second with the Python standard library, no
> solver in the loop. Derived twice independently (two LPs written from the statement by two
> parties, two exactified tables, both shipped) and refereed shared-nothing (an independent
> checker, shipped here too, agrees to the digit; brute force over all 126,840 hierarchies
> agrees with the dynamic programme).

> **`L_cf(M) <= 102`.** The witness is unchanged: `../cf_gte92/cf_102gates_depth5.json`,
> re-checked with `../cf_gte92/check_cancellation_free.py`. It is not duplicated here.

This supersedes the 92 of `../cf_gte92/`, which is kept because it is the published and
cited value. What changes downstream:

| statement | with 92 | with 96 |
|---|---|---|
| every SLP for `M` with at most … gates contains a cancelling gate | 91 | **95** |
| the 88-gate records buy at least … gates with cancellation | 4 | **8** |
| an 87-gate circuit would have to buy at least … | 5 | **9** |
| cancellation-free bracket | `92 <= L_cf <= 102` | **`96 <= L_cf <= 102`** |

`L(M) = 88` is still not claimed and not proved; this bound says nothing about circuits that
cancel, and every record circuit cancels.

## The technique: price the split, not only the mask

The 92 certificate priced (target, mask) pairs. In a cancellation-free circuit every gate `m`
has **one** parent pair, so the internal node `m` of a target's hierarchy `H_t` is split in
exactly one way, by its own operands `s(m)`. Two targets that share a gate share its split.
So the budget can be handed out per (mask, split) instead of per mask:

    n[t][(S,A)] >= 0   for target t, mask S inside supp(t) with |S| >= 2, split {A, S^A} of S,

    (C')   for every (S, A):   sum_t n[t][(S,A)]  <=  D .

**Soundness, three lines, for every cancellation-free circuit `G` (no minimality needed):**

    |G|  =  sum_{m in G} 1
         >= sum_{m in G} sum_t n[t][(m, s(m))] / D                      by (C')
         >= sum_t sum_{m in H_t} n[t][(m, s(m))] / D                    H_t subset of G
         >= sum_t min_H sum_{(S,A) in H} n[t][(S,A)] / D   =:  B .

Hence `L_cf(M) >= ceil(B)` for **any** table satisfying (C'). The minimum over hierarchies is
the same subset DP as before with the split as part of the key; a split with no entry costs 0.
Prices that ignore the split are exactly the old family, so this family contains it: fed the
old tables (embedded once per split), the checker returns their old constants (see RUN.md).

## The two derivations

| file | how the table was found | `B` | bound |
|---|---|---|---|
| `cert_cf96_split.json` | exact LP over the split family (13,293 priced triples, 12,840 columns), exactified to integers over `10^7` | `958521517/10^7 = 95.8521517` | `>= 96` |
| `cert_cf96_split_referee.json` | the referee's own LP, written from the statement only, exactified the same way | `958521565/10^7 = 95.8521565` | `>= 96` |

## Where this line stops

| quantity | value | status |
|---|---|---|
| optimum of the mask-only family (`../cf_gte92/`) | `91.409884` | COMPUTED (19 exact LP solves, 2026-09) |
| optimum of the split family | `95.852164` | COMPUTED (two independent LPs, 2026-09-26, agree to six places) |
| `L_cf >= 97` would need | `B > 96` | **unreachable** by any split-price table |
| exact model, branch-and-bound dual after 3000 s | `99.005`, incumbent `102` | COMPUTED, a solver run that hit its time limit; **not a certificate** |

So the split family is another closed door at 96, and the true value is probably 100 to 102.
Cite **`96 <= L_cf(M) <= 102`**; quote the 99 only as a run.

## Controls

| control | result |
|---|---|
| old tables embedded in the split family (`cert_cf92_sharper_as_split.json` shipped; the published one also converted) | `91.4098776` and `91.0019782`, exactly the old constants, bound 92 |
| the 102-gate cancellation-free witness | its 32 cones are trees; priced along them the chain is `95.8521517 <= 98.1596411 <= 101.3335800 <= 102` |
| the 88-gate record | the chain breaks at its first link, as it must for a circuit that cancels |
| exact small instances (cancellation-free optimum by exhaustive enumeration and by SAT) | 0 violations of `B <= L_cf` on 545 instances (lane) and on 507 (referee); on 9 of them the same certificate exceeds the *cancelling* optimum, so the test can detect a false bound |
| mutation test | deliberately broken copies of the certificate are rejected |

## Generality

As before: hierarchy lemma, DP and pricing take any target set; the checker takes `--matrix`.
The certificate is matrix-specific and must be regenerated for another matrix.
