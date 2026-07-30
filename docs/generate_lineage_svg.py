#!/usr/bin/env python3
"""Generate docs/lineage.svg: the two fully-logged own-lineage chains.

Chain A, from the from-scratch 97 through the 89@5 basin and the rho^2-symmetric
94 seed to the 88 @ depth 7. Chain B, entirely separate: from a random 139-gate
construction to the 88 @ depth 6, in 37 minutes on one restart of one worker.

Every step has a timestamped log line and a verified circuit in the run
archives. Data: ../evidence/RESULTS.md sections 3-4 (chain A) and 6 (chain B),
i.e. the archived worker logs in
../evidence/campaign87_run_2026-07-26_got_88at7/runs_hunt/w10_sym94.log and
../evidence/campaign87_run_2026-07-28_got_88at6_fromscratch/runs_hunt/c_naive.log.

Provenance note kept in the caption: neither chain contains imported material,
and the two derived circuits (88 @ depth 8 and 88 @ depth 5) are deliberately
NOT drawn here -- both of their seed chains pass through Jean's published 88
(ePrint 2026/1481), and RESULTS.md sections 5 and 7 spell them out link by link.

Stdlib only; writes the SVG next to this script.
"""

from pathlib import Path

RHO2 = "&#961;&#178;"  # rho-squared, kept as entities so the file stays ASCII

# (label, sub-label, run-index, kind)
CHAIN_A = [
    ("scratch", "", 0, "start"),
    ("97@3", "d3", 0, "record"),
    ("96@4", "d4", 0, "step"),
    ("95@5", "d5", 0, "step"),
    ("94@4", "d6", 0, "step"),
    ("93@7", "d7", 0, "step"),
    ("92@7", "d8", 0, "step"),
    ("92@7", "d9", 0, "step"),
    ("89@6", "d10", 0, "step"),
    ("89@5", "reroute", 1, "record"),
    ("94@5", RHO2 + "-sym, +5", 2, "sym"),
    ("88@7", "w10_sym94", 3, "record"),
]
CHAIN_B = [
    ("scratch", "", 4, "start"),
    ("139@3", "naive#2163", 4, "step"),
    ("95 &#8594; 89", "walk + lns chunks", 4, "step"),
    ("88@7", "it = 37 270", 4, "step"),
    ("88@6", "it = 37 501", 4, "record"),
]
RUNS = {0: "parallel ladder run (2026-07-13)",
        1: "sub-89 run (2026-07-14)",
        2: "structure-algebra (2026-07-26)",
        3: "merged-engine hunt (2026-07-26)",
        4: "87-hunt fleet, worker c_naive, restart 18 (2026-07-28) &#8212; 37 min, no seed circuit"}
FILL = {"start": "#ffffff", "step": "#eef2f7", "record": "#1f6feb", "sym": "#fcefd0"}
TEXT = {"start": "#222222", "step": "#222222", "record": "#ffffff", "sym": "#222222"}

BW, BH, GAP, X0 = 86, 40, 22, 20
ROW_Y = {0: 56, 1: 176}          # box top per row
HEIGHT = 380
CAPTIONS = [
    "gates@depth per node; every arrow is a search step with a timestamped log line and a verified circuit in evidence/.",
    "Top chain: root 97@3 from scratch (anneal3, 2026-07-13, t = 235 s); 89@6 at t = 39 725 s of the 21 h ladder; 89@5 by one reroute (t = 592 s).",
    "The +5-gate exactly " + RHO2 + "-symmetric 94@5 shares 82/94 masks with the 89@5; the 88@7 came from worker w10_sym94 at t = 1 973 s (2026-07-26 22:08:19).",
    "Bottom chain: no seed circuit at all - randomized balanced XOR trees over the 32 raw inputs (139 gates at depth 3), reduced to 88 gates in 37 min,",
    "the depth-6 tie-break landing 0.5 s after the depth-7 one (2026-07-28 17:19:45). A fourth 88-gate family, at Jaccard 0.313-0.323 to every other known 88.",
    "The 88@7 ties the published 88@7 (Jean, ePrint 2026/1481) with an independent circuit - 61/88 shared masks; 88 is Jean\'s count and Jean has priority.",
    "Not shown: the seed chains of the 88@8 and the 88@5 both pass through Jean\'s published 88 - see evidence/RESULTS.md sections 5 and 7.",
]


def main():
    n = max(len(CHAIN_A), len(CHAIN_B))
    width = X0 * 2 + n * BW + (n - 1) * GAP + 40
    e = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {HEIGHT}" '
         f'font-family="Helvetica,Arial,sans-serif" font-size="14" '
         f'role="img" aria-labelledby="ltitle ldesc">',
         '<title id="ltitle">The two own-lineage chains: to the 88-gate depth-7 '
         'circuit, and to the 88-gate depth-6 circuit found from scratch</title>',
         '<desc id="ldesc">Two left-to-right chains of boxes, each box a verified '
         'circuit labelled gates-at-depth. The top chain runs from scratch to 97 '
         'at depth 3, then down the 2026-07-13 parallel ladder (96, 95, 94, 93, '
         '92, 92) to 89 at depth 6, then 89 at depth 5 in the 2026-07-14 sub-89 '
         'run by a single reroute, then an uphill step to an exactly '
         'rho-squared-symmetric 94 at depth 5 (five gates worse than the record, '
         '82 of 94 masks shared with the 89), used as the seed from which the '
         'merged-engine worker w10_sym94 found the 88-gate depth-7 circuit on '
         '2026-07-26. The bottom chain is independent of the top one and of all '
         'published work: on 2026-07-28 a from-scratch worker of the 87-hunt '
         'fleet built a randomized 139-gate depth-3 circuit as its root and '
         'reduced it through 95, 92, 90 and 89 to 88 gates at depth 7 and then, '
         'half a second later, depth 6. The 97, the 89 at depth 5, the 88 at '
         'depth 7 and the 88 at depth 6 are highlighted as records.</desc>',
         f'<rect width="{width}" height="{HEIGHT}" fill="white"/>']

    for row, chain in ((0, CHAIN_A), (1, CHAIN_B)):
        y0 = ROW_Y[row]
        # run-group brackets, staggered onto two label rows so short groups do
        # not collide
        first_last = {}
        for i, (_, _, r, _) in enumerate(chain):
            first_last.setdefault(r, [i, i])[1] = i
        for j, (r, (i0, i1)) in enumerate(sorted(first_last.items())):
            x0 = X0 + i0 * (BW + GAP)
            x1 = X0 + i1 * (BW + GAP) + BW
            by = y0 - 14
            ly = by - 22 if j % 2 == 0 else by - 8
            e.append(f'<line x1="{x0}" y1="{by}" x2="{x1}" y2="{by}" stroke="#aaaaaa"/>')
            e.append(f'<line x1="{x0}" y1="{by}" x2="{x0}" y2="{by+6}" stroke="#aaaaaa"/>')
            e.append(f'<line x1="{x1}" y1="{by}" x2="{x1}" y2="{by+6}" stroke="#aaaaaa"/>')
            e.append(f'<text x="{(x0+x1)//2}" y="{ly}" text-anchor="middle" '
                     f'fill="#666666" font-size="12">{RUNS[r]}</text>')

        for i, (lab, sub, _, kind) in enumerate(chain):
            x = X0 + i * (BW + GAP)
            e.append(f'<rect x="{x}" y="{y0}" width="{BW}" height="{BH}" rx="7" '
                     f'fill="{FILL[kind]}" stroke="#8899aa"/>')
            e.append(f'<text x="{x+BW/2:.0f}" y="{y0+25}" text-anchor="middle" '
                     f'fill="{TEXT[kind]}" font-weight="bold">{lab}</text>')
            if sub:
                e.append(f'<text x="{x+BW/2:.0f}" y="{y0+BH+18}" text-anchor="middle" '
                         f'fill="#888888" font-size="11">{sub}</text>')
            if i < len(chain) - 1:
                ax0, ax1 = x + BW, x + BW + GAP
                e.append(f'<line x1="{ax0}" y1="{y0+BH/2:.0f}" x2="{ax1-6}" '
                         f'y2="{y0+BH/2:.0f}" stroke="#556677" stroke-width="1.6"/>')
                e.append(f'<path d="M{ax1-6} {y0+BH/2-4:.0f} L{ax1} {y0+BH/2:.0f} '
                         f'L{ax1-6} {y0+BH/2+4:.0f}" fill="#556677"/>')

    for j, cap in enumerate(CAPTIONS):
        e.append(f'<text x="{X0}" y="{258 + j*17}" fill="#666666" font-size="11.5">{cap}</text>')
    e.append("</svg>")
    out = Path(__file__).resolve().parent / "lineage.svg"
    out.write_text("\n".join(e) + "\n", encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
