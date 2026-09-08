# Cancellation-free circuits: `92 <= L_cf(M) <= 102`

## The claim

An XOR-SLP is **cancellation-free** when the two operand values of every gate
have disjoint support: no gate ever destroys a bit an earlier gate produced. (A
*value*, or mask, is the bit vector of which inputs a signal is the XOR of — see
[`../../DEFINITIONS.md`](../../DEFINITIONS.md).) Write `L_cf(M)` for the minimum
size of a cancellation-free XOR-SLP for MixColumns (`../matrix.txt`).

> **`L_cf(M) >= 92`.** A price certificate: a JSON table of integers, checked in
> **0.03 s** with the Python standard library, no solver anywhere in the loop.
> Derived twice, independently.

> **`L_cf(M) <= 102`.** An explicit 102-gate circuit with `kappa = 0`, all 32
> outputs built, depth 5 — re-verified by the checker in this directory, and
> published as a first-class record circuit in the records repository
> (`circuits/mixcolumns_102gates_cf.json`, v3.2.0).

**What this bound rules out.** It is the only proved quantity anywhere in this
programme that lies *above* the 88-gate record. Every other lower bound is below
88 and therefore says nothing about whether an 87-gate circuit exists. This one
is unconditional:

> **Every XOR circuit for MixColumns with at most 91 gates contains a cancelling
> gate.** The 88-gate record is 4 gates below the cancellation-free floor, so
> cancellation is not an optimisation trick in these circuits — it is forced.

(The record 88 measured here has `kappa = 22`. See [`RUN.md`](RUN.md).)

## The technique: a laminar price certificate

**The hierarchy lemma.** In a cancellation-free SLP, the gates that contribute
to one target `t` form a *laminar hierarchy* `H_t` over `supp(t)`: the target is
an XOR of two disjoint sub-masks, each of which is an XOR of two disjoint
sub-masks, and so on down to single inputs. Every internal node of `H_t` (every
subset of size `>= 2`) is the mask of an actual gate, so `H_t ⊆ G` where `G` is
the set of gate masks. This is where cancellation-freeness is spent, and it is
the only place it is used.

**The prices.** Assign integers `n[t][m] >= 0`, one per target `t` and mask `m`
inside `supp(t)`, over a common denominator `D`, subject to a single family of
constraints:

    for every mask m :      sum_t n[t][m]  <=  D .                        (C)

Read (C) as: a mask is *one* gate however many targets would like to use it.

**Soundness, in three lines, with no optimality of the table required.**

    |G|  =  sum_{m in G} 1
         >= sum_{m in G} sum_t n[t][m]/D                              by (C)
         >= sum_t sum_{m in H_t} n[t][m]/D                            H_t subset of G
         >= sum_t min_H sum_{m in H} n[t][m]/D   =:  B .

Hence `L_cf(M) >= ceil(B)` for **any** table satisfying (C). Nothing about how
the table was found enters the proof — which is exactly why this is a
certificate and not a solver result.

**Checking it** is (C), one sum per mask, plus 32 independent subset DPs, each
over `2^w(t) <= 2^7 = 128` states. All integer arithmetic.

## The two independent derivations

Both are shipped; both check with the same script.

| file | how the table was found | `B` | bound |
|---|---|---|---|
| `cert_cf92.json` | projected subgradient ascent (Polyak step, true Euclidean projection onto `{x >= 0, sum_t x <= 1}`, exactified) | `910019782/10^7 = 91.0019782` | `>= 92` |
| `cert_cf92_sharper.json` | the same pricing problem *recognised as a finite LP* (~5.9 k variables, ~18.6 k constraints), solved exactly with a different solver, then exactified to a rational table | `914098776/10^7 = 91.4098776` | `>= 92` |

The second is not a re-run of the first: it comes from a separate lane that
rebuilt the hierarchy lemma, the DP and the pricing from the statement, arrived
at the LP form, and produced a *better constant* for the same integer
conclusion. A third party rebuilt the check itself, with its own DP, and
reproduced `Check 1 max column sum = 1.0000000, exactly tight, FEASIBLE`.

`cert_cf92_sharper.json` is the stronger artifact and is what a reader should
cite for the constant; `cert_cf92.json` is the published one and is kept so the
literature value stays checkable.

## Where this line stops: the family's optimum is 91.409884

The 19 exact LP solves behind the sharper table also pin down the **optimum** of
this entire price family:

    G*(lambda) = 32*lambda for lambda <= 5/2, then slope 12,
                 saturating at  B* = 91.409884  from lambda = 7/2 on.

So `B* = 91.409884` is the best constant *any* table in this family can ever
give. The two thresholds anyone would want next —

* `B > 92`, which would give `L_cf >= 93`, and
* `B > 91.9738`, which would force a structural property of every hypothetical
  87-gate circuit —

**both lie above `B*` and are therefore unreachable by optimising this LP at
all**, symmetric or not. Exploiting the matrix's order-4 symmetry is worth
`+0.0000003`: the optimum is already symmetric to seven places.

This is a closed door. The certificate remains useful as a bound *generator*
for other matrices; for this matrix it is a dead end as an *upgrade path*.

Two by-products of the LP form are unconditional, solver-free, and about
ordinary (cancelling) circuits:

* for every XOR-SLP for `M`, `|C| >= 58` **or** `kappa >= 16`;
* no price table and no multiplier can ever prove `n >= 57` for a circuit with
  `kappa >= 22` — and the records have `kappa` in 18..28, so this family of
  arguments is capped below the record's own regime, by proof.

## The upper bound, and what it is not

`cf_102gates_depth5.json` is an explicit circuit: 102 gates, 32/32 targets,
`kappa = 0`, depth 5 (all four figures **computed** by
`check_cancellation_free.py`, not asserted). It bounds `L_cf(M) <= 102`.

**Where it is published.** The same circuit ships in the records repository from
**v3.2.0** as `circuits/mixcolumns_102gates_cf.json`, with a full `bounds.json`
entry (`sha256_circuit_json`
`ded0a186062bae38217a3363b973c4b8466c7819a386960db0f49b3d4056b675`,
`cancellationFree: true`, `cancellingGateCount: 0`, `measuredDepth: 5`), a
plain-text listing and a Verilog netlist + testbench. The copy in this directory
is the same gate list, gate for gate, kept next to the certificate so that the
bound and its witness can be checked without leaving this pack.

Do not confuse this with the general MixColumns record: 102 here is a
*cancellation-free* cost, while the unrestricted record is 88.

**A number collision.** "102" also appears in the literature as a published
*unrestricted* 2-input XOR count for MixColumns. That is a different quantity
that happens to share the value; the 102 in this directory is a bound on `L_cf`,
and it is not a claim about `L`. Within this programme, values of
103, 104 and 133 appear in older material for `L_cf`; those are superseded
incumbents, not competing bounds, and should not be quoted.

## Generality

The machinery is **circuit-generic, the certificate is matrix-specific.** The
hierarchy lemma, the DP and the pricing all take an arbitrary target set, and
the mask universe (1,648 masks here) is *derived* per matrix rather than
assumed. `check_cf_cert.py` and `check_cancellation_free.py` both take
`--matrix`. Retargeting to another matrix means rebuilding the targets,
re-running the ascent or the LP, and re-verifying — the check itself does not
change.
