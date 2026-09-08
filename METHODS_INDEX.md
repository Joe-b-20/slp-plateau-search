# Methods index

Every method this repository ships as runnable code, with a `HOW.md` explaining
the mechanism — the idea in plain words, the algorithm as a diagram, what it
measured, and the exact command. One screen; the HOW docs carry the detail.

| method | what it does | where | how it works |
|---|---|---|---|
| search engine | finds smaller or shallower circuits: destroy-and-rebuild, plateau walk, depth-3 annealer, run as parallel workers under one coordinator | [`pipeline/`](pipeline/) | [`pipeline/HOW.md`](pipeline/HOW.md) |
| record reproductions | one command per record: the depth-3 annealer from nothing, an exact construction for the 91 @ depth 4, and harnesses that re-run one archived worker from its exact root | [`reproduce/`](reproduce/) | [`reproduce/HOW.md`](reproduce/HOW.md) |
| `>= 56` lower bound | counts gates from three independent sources, with one term decided by an exhaustive depth-limited search over extra masks | [`bounds/gte56/`](bounds/gte56/) | [`bounds/gte56/HOW.md`](bounds/gte56/HOW.md) |
| depth-3 lower bound | turns the forced shape of a depth-3 circuit into a linear program and proves a bound from one exact rational dual vector | [`bounds/depth3_gte81/`](bounds/depth3_gte81/) | [`bounds/depth3_gte81/HOW.md`](bounds/depth3_gte81/HOW.md) |
| cancellation-free bound | prices each target's cheapest gate hierarchy under a per-gate budget; solver-free to check | [`bounds/cf_gte92/`](bounds/cf_gte92/) | [`bounds/cf_gte92/HOW.md`](bounds/cf_gte92/HOW.md) |
| bound validation | runs the same bound machinery on small matrices with independently proved optima, including one instance designed to make it overclaim | [`bounds/validation/`](bounds/validation/) | [`bounds/validation/HOW.md`](bounds/validation/HOW.md) |
| SAT encoding | asks a solver whether a `k`-gate program exists for one subproblem, with a normal form, a cube partition and a positive control | [`encodings/`](encodings/) | [`encodings/HOW.md`](encodings/HOW.md) |
| deletion certificate | tests every single-gate deletion of every known 88-gate circuit for realisability with the wiring re-planned freely | [`corpus/deletion_certificate/`](corpus/deletion_certificate/) | [`corpus/deletion_certificate/HOW.md`](corpus/deletion_certificate/HOW.md) |
| tripwire | replays any circuit and reports a dead gate, a duplicate value, or a working-gate count `B` that proves one of them exists | [`tools/tripwire.py`](tools/tripwire.py) | [`tools/HOW.md`](tools/HOW.md) |
| overlap statistic | counts the values two circuits share — the same-family / independence measure | [`scripts/overlap.py`](scripts/overlap.py) | [`scripts/HOW.md`](scripts/HOW.md) |
| corpus sample | the deterministic, stratified 520-record draw the shipped certificates run over, plus its checker | [`corpus/sample/`](corpus/sample/) | [`corpus/sample/HOW.md`](corpus/sample/HOW.md) |
| depth check | computes the shallowest depth a circuit's value set admits and compares it with the circuit's own depth | [`corpus/depth_forced/`](corpus/depth_forced/) | [`corpus/depth_forced/HOW.md`](corpus/depth_forced/HOW.md) |

Two more runnable pieces have no HOW doc of their own and are documented where
they are used: `verify_circuit.py` at the root — the oracle, which rebuilds
MixColumns from FIPS-197 and computes depth rather than trusting it — and the
per-section checkers in `corpus/` (records, vocabulary, calibration), each with
a `RUN.md` giving its command and real output.

What to run first, if you run one thing: `python3 tools/tripwire.py YOURCIRCUIT.json`
on any 88-gate MixColumns circuit from any source. It takes seconds, and a
fired tripwire on an 88 is an 87.

<a id="provenance-classes"></a>
## Provenance classes

Every circuit this project reports is labelled with exactly one of three
classes. The label is per file, it is inherited (anything a search worker
produces takes the status of its seed), and it is the authority for every
priority claim made anywhere in this repository:

| class | meaning |
|---|---|
| **ours, own lineage** | found by this project's own code from this project's own roots, with **no imported material anywhere in the chain**. |
| **imported** | somebody else's published circuit, transcribed here and credited. **Not this project's result.** The two imported circuits and their attribution are in [`evidence/campaign87_imported_prior_art/PROVENANCE.md`](evidence/campaign87_imported_prior_art/PROVENANCE.md). |
| **derived from published work** | found by this project's code, but with a **lineage that passes through** somebody else's published circuit. Retained, reported, and never counted as independent. |

The per-file application of the scheme, for the nine seed circuits the search
harness ships, is the table in
[`pipeline/seeds/README.md`](pipeline/seeds/README.md); the per-run application
is each `PROVENANCE.md` under [`evidence/`](evidence/).
