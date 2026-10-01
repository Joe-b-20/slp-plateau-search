# The 76 extension: facts and status

**Claim.** No circuit of 75 two-input XOR gates computes AES MixColumns, hence 76 <= L(M) <= 88.

**What it is.** A proof document of about 2,200 lines (dated 2026-09-30) that extends the 75 argument of the
parent folder. It keeps the same framework (the steady two-cycle of canonical transposes, the bounded
potential, the helper-type systems) and adds about twenty further families of inequalities of three kinds:

1. special-output geometry of M^T (the four outputs of weight 11 cut out the weight <= 10 relation space; a
   rank lemma for the gate defects; co-location of missing labels);
2. "palette triangles" on the M side (three helpers or even+even gates pairwise sharing missing labels form a
   weight-6 relation);
3. realizability of every candidate helper-type vector (two helpers share at most one missing label, each label
   has a bounded capacity, heavy labels are dark), applied to every candidate rather than to sampled witnesses.

Its theorem is stated conditionally: *if* the shipped checkers accept the certificates of one of three
routes (they do), then no 75-gate circuit exists.

**How it was checked.** Every exclusion carries an exact integer certificate checked by standard-library
Python (levels 1-2: 50,048 certificates; level 3: 772 cases with two independent certificate sets, 2,445
records); the coverage of the whole domain (3,708 scalar states, 7,416 oriented profiles, 585,660 potential
pairs) is checked; the new inequalities went through four independent machine referee passes, an exact
full-domain rescan, and three final audits (the mathematics; the checkers against the document, 6.4 million
rows compared; the one single-implementation premise, re-implemented). No human has reviewed it. The
package's own verification prints `ROUTE lite: VERIFIED`, `ROUTE main_noqk: VERIFIED`, `ROUTE main: VERIFIED`
in about six minutes on eight cores.

**Why only this description is here.** The proof document is an internal working document written during a
two-day campaign (2026-09-29/30) and has not yet been consolidated into a standalone note like
`PROOF_NOTE_75.md`; its certificates are about 180 MB and the self-contained package 948 MB. The package is
kept by the author (SHA-256 manifest over 4,842 files) and will be published once the document has been
rewritten to the standard of the 75 note; it can be shared on request before that.

**Assessment.** The 76 is a genuine, machine-certified result at the level of its stated condition, but it
has had far less independent scrutiny than the 75, its argument is long, and it is not yet in citable form.
Treat it as "certified, less reviewed".
