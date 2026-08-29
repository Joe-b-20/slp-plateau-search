# Follow-up email to Jérémy Jean — DRAFT for Joe to review and send

**To:** Jérémy Jean
**From:** joebachir20@gmail.com
**Subject:** MixColumns: our search is closed at 88 — and a request

---

Dear Jérémy,

Thank you for your August reply. I wanted to answer properly rather than quickly,
so I waited until our full accounting was written up. It is done, and both
repositories are now current:

- https://github.com/Joe-b-20/slp-plateau-search — the search, the certificates
- https://github.com/Joe-b-20/aes-mixcolumns-xor-circuits — the records, circuits, verifier

The short answer: no 87. Our search is over, and we finish on the bracket
56 <= L(MixColumns) <= 88. One computation is still live: two of the blocks an 87
would need can be built jointly in 15 gates, and we have proved 9, 10, 11, 12 and
13 impossible (the first three under a second, independent encoding). Whether 14
is possible is the open instance — 87 of its 528 cubes closed UNSAT so far, none SAT.

Since your intuition is that 88 is the lower bound, here is our evidence for it,
strongest first. It is structural, and none of it is a proof.

**1. A count that never varies.** Let B be the number of gates whose output is
not one of the 32 MixColumns outputs but is consumed by a later gate. Small
theorem: for any valid 88-gate circuit, either B = 56, or one gate can be deleted
to give an 87 — so B = 56 is exactly the statement that no gate is free to drop.
We hold 1,575,516 distinct verified 88-gate mask sets. Not one has a repeated
mask, and every one of the 28,796 for which we have a build order on disk has
B = 56, without exception. (The remaining ~1.5 M are mask sets only; the
consumer-less half of the test needs a build order, so it is undecided there.)

**2. Relaxations do not pay.** We repeatedly dissolved structure we had imposed —
merging adjacent blocks, opening interfaces, pricing sub-problems jointly instead
of separately — and the price came back at exactly the split total: 19 of 21
dissolved boundaries (2 undecided), and 131 further merges whose lower bound
alone already equals the unmerged total.

**3. The plateau is wide but flat.** Under our two cost-free moves
(re-association and re-parenting) the five 88s we publish lie in five
pairwise-distinct closed components — 44,793 wirings, containing zero 87s.

**The ask.** Would you share your unpublished 88s? Any format is fine — the 88
XOR equations in a text file is plenty; we need no code and no provenance.

The reason is specific. All of our 88s come from one family of methods; yours do
not, so everything above is measured on a single search distribution and the
honest caveat is selection bias. Yours are the only foreign lineage we could test
against. We would run them through the battery above and report back either way.
Both outcomes are worth having: B = 56 on your circuits too is genuinely
independent evidence for your intuition, and B != 56 on any one of them is an 87
on the spot.

In return, anything of ours is yours for the asking — corpora, certificates, SAT
encodings, methods; all listed as available on request in the repositories. And I
would enjoy comparing notes on what a proof of optimality would even have to look
like. Our view after all this is that the local arguments are exhausted and
something global is needed, but we cannot see what.

Best regards,
Joe

---

## Notes for Joe

**Facts asserted, and where each is verified**

| # | assertion in the email | source |
|---|---|---|
| 1 | Bracket `56 <= L(M) <= 88`; lower bound unconditional and refereed | `wrapup/MANIFEST.md` §0 row "The bracket" (atlas §3.3, cert 5 depth 4) |
| 2 | Merged block: k = 9,10,11,12,13 all UNSAT ⇒ needs >= 14; merged ∈ {14,15} | `MANIFEST.md` §0 "Joint-level UNSATs" (`fleet8/unified/results/joint_levels.jsonl`) |
| 3 | k = 9/10/11 re-proved by an independent CNF encoding | `MANIFEST.md` §0 "independent cross-check" (`fleet11/laneCUBE`) |
| 4 | 87 of 528 cubes UNSAT, 0 SAT, at k = 14 | `CONFLICTS_RESOLVED.md` B8 PUBLIC-SAFE — **timestamped 2026-08-29 08:27 −0400, and the run is live** |
| 5 | B theorem: on any valid 88, either B = 56 or an 87 is available by deleting one gate | `CORPUS88.md` §4; `experiments/e15_campaign3/tools/sweep.py:296` docstring (ARCH3 R53) |
| 6 | 1,575,516 distinct verified 88-gate mask sets; 0 with a repeated mask; 28,796 with a build order, all B = 56 | `CORPUS88.md` §2 totals table + §4 check table; `CONFLICTS_RESOLVED.md` B10 PUBLIC-SAFE |
| 7 | 19 of 21 dissolved boundaries price exactly the split total (2 undecided); 131 no-solver merge bounds already equal the split; 20 distinct cells all price >= 88 | `MANIFEST.md` §2.6 (`fleet5/laneMERGE/results/FINAL_TALLY.txt` §B, `bounds.json`, `fleet5/laneMENU/results/cellprice.json`) |
| 8 | Five published 88s = five pairwise-distinct closed components, 44,793 wirings, zero 87s | `MANIFEST.md` §2.4 "five e14 free-move orbits"; wording follows `CONFLICTS_RESOLVED.md` B4 PUBLIC-SAFE |
| 9 | Jean's lineage is foreign (Codex) | his paper, quoted in the correspondence memory; the email does not name Codex, only "one family of methods; yours do not" |

**Judgement calls you should check before sending**

1. **The corpus sentence was weakened on purpose.** It is *not* true that all
   1,575,516 have B = 56. The full `count_B` test ran on the 28,796 sets that
   carry a build order (all 56, zero alarms); the other 1,546,720 are mask-set
   only and pass only the duplicate-mask half. `CORPUS88.md` §4 calls this "the
   one honest gap". The draft says exactly that, including the parenthetical.
   Please do not let it get tightened back up in editing.

2. **Item 4 is live and dated.** The house rule (`CONFLICTS_RESOLVED.md` B8) is
   that no cube figure may be quoted without a timestamp. The email deliberately
   says "so far" instead of carrying a date, which reads better but ages. If you
   send more than a few days from now, re-tally and adjust the number.

3. **I did not assert "SAT ⟺ an 87 exists."** `MANIFEST.md` §0 does state that
   for `experiments/sat_package/k14_joint_W3U4.cnf`, but `CONFLICTS_RESOLVED.md`
   B8 insists the level is a coverage bracket and never a refutation. The email
   calls it "the open instance" and stops there. Add the biconditional only if
   you are confident of its scope.

4. **Repo URLs** are the real `git remote` values, not placeholders — confirm
   both pages are actually pushed and current before sending.

5. **Depth frontier: deliberately omitted.** Your July letter quoted 97@3 /
   92@4 / 89@5. The project now holds **97@3 / 91@4 / 88@5**
   (`CONFLICTS_RESOLVED.md` B7 PUBLIC-SAFE), but the public repos reportedly
   still say 92@4 (`MANIFEST.md` §0, CONFLICT #4). Once the repos are patched,
   consider adding one line after the two links: *"The depth-constrained records
   moved since July as well: 97 at depth 3, 91 at depth 4, 88 at depth 5."*
   Do not add it while the repos still say 92.

6. **Tone check.** No internal codenames anywhere (no B37/W3/U4, no lane or
   fleet names). "B" is defined in one clause. The ask is framed as a mutual
   experiment, not a favour, and explicitly says both outcomes are useful — which
   matches the register of his short August reply.
