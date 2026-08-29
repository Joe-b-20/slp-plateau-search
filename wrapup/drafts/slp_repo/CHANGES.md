# What would change in the real repo

Recommendations only. Nothing here has been applied.

## 1. README.md — replace

Replace `README.md` (13.9 KB, 2026-07-30) with the draft beside this file.
The current one is long, jargon-heavy, and still states the stale depth-4 record.

## 2. METHODS.md — recommendation: keep, demote to one link

`METHODS.md` is 58.7 KB. Nobody arriving at this repo will read it, and it is
not the public face. Two options:

- **Recommended: keep it, link it once.** Add a single line at the bottom of the
  new README: "`METHODS.md` is the original long-form method write-up, kept as
  historical detail." Costs nothing, loses nothing, and the material is real.
- **Alternative: delete.** Only worth it if its content is fully carried by the
  method catalogue that ships on request. It is not, today.

Either way it must not be linked as "start here".

## 3. The stale 92 @ depth 4 — five places need the 91 fix

The verified depth-4 point is **91**, not 92, oracle-verified in three
independent lineages. See `wrapup/CORRECTIONS.md` **C-01** for the exact
document and line list, and `wrapup/CONFLICTS_RESOLVED.md` **§B7** for the
re-verification (`gates=91 depth=4 outputs_built=32/32`, 3 of 3 VALID).

| file | what is stale |
|---|---|
| `README.md:9`, `:13` and the SVG alt-text | "verified frontier: 97 @ 3, 92 @ 4, 88 @ 5" |
| `evidence/RESULTS.md:1` and §2 | same claim |
| `docs/generate_frontier_svg.py:62` | `FRONTIER = [(3,97),(4,92),(5,88)]` |
| `docs/frontier.svg` | the drawn point (regenerate after the script fix) |
| `.github/workflows/verify.yml` | CI verifies the 92 @ 4 circuit |
| `tests/test_invariants.py` | `test_directory_holds_exactly_the_eight_records` |
| `evidence/circuits/` | holds no 91 @ 4 file; `spectrum.json` has no entry |

Two guards that must travel with the fix (`CORRECTIONS.md` C-02):

1. **90 @ 4 is undecided, not refuted.** Never write "optimal at depth 4".
2. **Do not add 108 @ 3.** It is worse than the shipped 97 @ 3.

A ready-made patch with line numbers already exists and has never been applied:
`fleet7/laneCONSOLIDATE/RECORDS_REPO_PATCH.md` (2026-08-24). It targets the
sibling records repo, but the same edits apply here.

## 4. Push commit `23d80d7`

`main` is one commit ahead of `origin/main`. `23d80d7` — "Reprice the
neighbourhood certificates: they are not evidence about 87" — is the commit that
withdraws the inference "certificates ⇒ 87 is unlikely". Until it is pushed the
public copy still carries the withdrawn inference. See `CORRECTIONS.md` **C-05**.

The sibling repo `aes_mc_records` is likewise one ahead (`73ad7ee`), same reason.

## 5. Smaller items worth folding in at the same time

- `CITATION.cff` hardcodes "92 at depth 4" in its title string
  (`CORRECTIONS.md` C-03).
- If the 91 @ 4 circuit is added to `evidence/circuits/`, the record set becomes
  8 circuits with 91 in place of 92, which is what the new README states. Do the
  file addition and the README wording in one commit so they never disagree.
