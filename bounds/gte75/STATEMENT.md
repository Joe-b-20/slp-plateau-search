# `bounds/gte75/` — statement

**Claim.** Every acyclic circuit of two-input XOR gates computing one column of AES MixColumns (the
32 x 32 matrix `../matrix.txt`) has at least **75** gates. With the verified 88-gate circuits:
`75 <= L(M) <= 88`. Not claimed: that 88 is optimal, or any 87-gate circuit.

**Status: computer-assisted, review draft (version 1.0, 2026-10-01).** The argument is written out in full in
`PROOF_NOTE_75.md` (also as PDF, 18 pages); fourteen finite facts about the matrix are computed by
`checks/finite_facts.py`; the last two steps (73 and 74 gates) are exact Farkas certificates checked by two
independent standard-library programs each. The argument was produced with large-language-model assistance
and has been reviewed by programs and by independent machine reviews (note, section 13); no human
mathematician has refereed it; nothing is formalized. The canonical copy of the note is in the records
repository, `aes-mixcolumns-xor-circuits`, folder `lower_bounds/` (tag v4.0.0); the files here are identical.

**Technique, in one paragraph.** Classify every signal by the parity of its mask. Then G = 32 + x + y + h
(odd+odd gates, even+even gates, odd non-output gates). The even span is the parity space of a partition of
the inputs whose blocks give disjoint words of the graph code of M; the code has no nine-part partition, so
x >= 24. Exact transposition turns a minimum circuit into a minimum circuit of M^T with the same gate count;
a canonical association maximizes the even+even gates of the transpose and bounds every fan-out. The
odd-signal graph (edges = gate equations with two odd signals, labelled by the even one) gives exact
incidence identities and, with the Sidon property of the 64 boundary masks, the inequality
32 <= 2h + y + z + C(q,2). A weighted-degree identity on adjoint parities couples a circuit to its transpose;
the number of even+even gates with odd adjoint is a bounded potential that must grow along repeated
transposition unless the count profile is one of finitely many; those profiles are excluded one by one, the
last 1,364 of them by linear inequalities on helper types whose infeasibility is certified by nonnegative
integer multipliers.

**Where the line stops.** The same system at 75 gates leaves 1,476 feasible count profiles; the extension to
76 (`bound_76/README.md`) needed mask-level facts beyond this note and is certified but not yet published.
The ≥ 56 pack (`../gte56/`) is superseded by this one and kept checkable.

**Controls.** Every inequality of the note and every identity was tested with zero violations on all record
circuits and on 24,619 further 88-gate circuits with their canonical and second transposes (note, section
13); `checks/stress.py` repeats the test on the circuits shipped here.
