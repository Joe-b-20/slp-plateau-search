# Decisions

A short note on the choices behind this repository, in my own words. The
proofs and numbers are elsewhere; this is about why things were done the way
they were.

## Why I split the matrix into blocks

The block decomposition that the main theorem is stated over was a choice,
and I want to say plainly why I made it.

Early on I set myself a rule: write the simplest version of the search that
anyone could follow, then go through it piece by piece and mark each piece as
either a fact about the problem or a choice I had made. Facts stay. Choices
get changed, one at a time, and each result gets recorded before the next
change. The block decomposition was one of the choices. It comes from the
field arithmetic — the way MixColumns is built from multiplying bytes by 2
and 3 — and it groups the intermediate values a circuit has to compute into
a few blocks that can each be priced exactly with a SAT solver.

I kept it for one reason: it is where the problem stays decidable. Every
time I tried to widen a block toward the whole 32-bit problem, the solver
stopped terminating. The decomposition is the largest piece of structure I
could afford to ask exact questions about. That is also its weakness, and
the README says so: whether every known 88-gate circuit respects this
decomposition was never verified, and a 91-gate circuit in the circuits
repository has a gate that sits across two blocks. So the theorem excludes
an 87 that is built the way I read the 88s, and nothing more.

One thing I got from this that I did not expect: the search is best run over
choices, not over circuits. Because the solver returns the optimum of a whole
class, each changed choice needs exactly one run. About two hundred such runs
all came back at 88. That is most of why I believe the number.

## The 56 bound, as I understand it

Every gate in a circuit produces one new value, the XOR of two values that
already exist. Start with the 32 inputs. The question is how many gates you
need before all 32 output rows of MixColumns are among the values you hold.
The lower bound comes from counting what is reachable: after a fixed number
of gates, only so many values of the shape MixColumns needs can exist, and
you can enumerate the early levels completely. Doing that enumeration to
depth 4 shows that no arrangement of fewer than 56 gates covers the outputs.
The certificate in `bounds/gte56/` is that enumeration made checkable, and
the exhaustion itself re-runs in about three minutes. It is a weak bound —
32 gates below the record — but it is the only unconditional one I know of,
and I would rather ship a weak bound with a checker than a strong claim
without one.

## A belief I held that was wrong

For a long time I assumed that once you have any 88-gate circuit, you can
turn it into one at depth 5 by rescheduling the gates. I planned the
reproduction section around that: find any 88 fast, then convert. It is
false. A circuit's wiring is almost entirely forced by the set of values it
computes, every circuit here is already at its own minimum depth, and the
depth-5 circuits form small closed pockets that no rescheduling reaches. You
have to land in a pocket; you cannot walk into one. I found this out by
having the conversion tested instead of assumed, and the test is now in
`corpus/depth_forced/`. I mention it because it is the kind of thing I would
have stated as obvious a month ago.

A smaller one: I believed the shared vocabulary of values that all known 88s
draw from was forced by how small they are. A verified 89 that uses a value
from outside that vocabulary ended that.

## Why I stopped

I stopped when the last computation that could have changed the answer
finished. The k = 14 level of the block ladder was the one open question that
a solver could settle; it came back UNSAT, twice, on two different solvers.
After that, everything left on the board was a lead with a price on it, and
I decided to price the leads rather than run them. They are in `leads.md`.
My own view is in the Opinion section: the local arguments are used up, and
if an 87 exists it will come from a different way of decomposing the matrix,
not from anywhere near the circuits we have.

Two things made stopping easier. The tripwire — a check that would have
handed me an 87 for free if any known 88 had a wasted gate — stayed silent
over 1.58 million value sets. And the calibration audit told me that most of
my negative results, the ones I was proudest of, carry almost no information
about whether an 87 exists. Knowing that, more of the same search was not
worth anyone's time.

## What I would do first on a new matrix

InvMixColumns is the natural next one, and the instruments already point at
it: the verifier and the tripwire take any 32×32 matrix, and the matrix,
the naive baseline and a first greedy circuit are done. The published record
there is 92 gates, from a single paper, with no depth ever reported and no
lower bound at all. I would start with the depth-restricted records, because
the whole frontier is unclaimed and the first points cost hours, not months.
Then the bounds, before any large search — this time with the calibration
audit run first, so I know what a negative result is worth before I collect
any.

## What surprised me most

That the best circuits were lying in debug output nobody had opened. Almost
five hundred distinct 88-gate circuits sat in a trace file the analysis
tools could not even read, produced an hour after the write-up that would
have described them was frozen. Most of the reorganisation work at the end
was making sure that could not happen again: every result with its command,
every count with the line that produced it.

---

The decisions above are mine. Like everything else here, the text was
prepared with the AI collaboration described at the top of the README.
