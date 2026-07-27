#!/usr/bin/env python3
"""Generate docs/lineage.svg: the fully-logged lineage of the 88-gates-at-depth-7
record, from the from-scratch 97 through the 89@5 basin and the rho^2-symmetric
94 seed.

Every step has a timestamped log line and a verified circuit in the run
archives. Data: ../evidence/RESULTS.md (the ladder rungs down to 89@5) and the
campaign-87 facts for the last two steps (the rho^2-symmetric 94@5 seed and the
merged-engine worker w10_sym94 that found the 88@7).

Provenance note kept in the caption: the 88@7 *ties* the published 88@7 (Jean,
ePrint 2026/1481) with an independent circuit; the 88@8 third family is NOT in
this chain -- its seed chain passes through Jean's published circuit -- so it is
deliberately not drawn here.

Stdlib only; writes the SVG next to this script.
"""

from pathlib import Path

RHO2 = "&#961;&#178;"  # rho-squared, kept as entities so the file stays ASCII

# (label, sub-label, run-index, kind)
CHAIN = [
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
RUNS = {0: "parallel ladder run (2026-07-13)",
        1: "sub-89 run (2026-07-14)",
        2: "structure-algebra (2026-07-26)",
        3: "merged-engine hunt (2026-07-26)"}
FILL = {"start": "#ffffff", "step": "#eef2f7", "record": "#1f6feb", "sym": "#fcefd0"}
TEXT = {"start": "#222222", "step": "#222222", "record": "#ffffff", "sym": "#222222"}

BW, BH, GAP, X0, Y0 = 86, 40, 22, 20, 56
HEIGHT = 210
CAPTIONS = [
    "gates@depth per node; every arrow is a seeded search step with a timestamped log line and a verified circuit in evidence/.",
    "Root 97@3 from scratch (anneal3, 2026-07-13, t = 235 s); 89@6 at t = 39 725 s of the 21 h ladder; 89@5 by one reroute (t = 592 s).",
    "The +5-gate exactly " + RHO2 + "-symmetric 94@5 shares 82/94 masks with the 89@5; the 88@7 came from merged-engine worker w10_sym94 at t = 1 973 s (2026-07-26 22:08:19).",
    "The 88@7 ties the published 88@7 (Jean, ePrint 2026/1481) with an independent circuit - 61/88 shared masks. The 88@8 third family is not shown: its seed chain passes through Jean's published 88.",
]


def main():
    n = len(CHAIN)
    width = X0 * 2 + n * BW + (n - 1) * GAP + 40
    e = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {HEIGHT}" '
         f'font-family="Helvetica,Arial,sans-serif" font-size="14" '
         f'role="img" aria-labelledby="ltitle ldesc">',
         '<title id="ltitle">Lineage of the 88-gate depth-7 AES MixColumns '
         'circuit</title>',
         '<desc id="ldesc">A left-to-right chain of boxes, each a verified '
         'circuit labelled gates-at-depth. From scratch to 97 at depth 3, then '
         'down the 2026-07-13 parallel ladder (96, 95, 94, 93, 92, 92) to 89 at '
         'depth 6, then 89 at depth 5 in the 2026-07-14 sub-89 run by a single '
         'reroute. From there an uphill step to an exactly rho-squared-symmetric '
         '94 at depth 5 (five gates worse than the record, 82 of 94 masks shared '
         'with the 89), used as the seed from which the merged-engine worker '
         'w10_sym94 found the 88-gate depth-7 circuit on 2026-07-26. The 97, the '
         '89 at depth 5 and the 88 are highlighted as records.</desc>',
         f'<rect width="{width}" height="{HEIGHT}" fill="white"/>']

    # run-group brackets, staggered onto two label rows so short groups do not
    # collide
    first_last = {}
    for i, (_, _, r, _) in enumerate(CHAIN):
        first_last.setdefault(r, [i, i])[1] = i
    for r, (i0, i1) in sorted(first_last.items()):
        x0 = X0 + i0 * (BW + GAP)
        x1 = X0 + i1 * (BW + GAP) + BW
        ly = 20 if r % 2 == 0 else 34
        e.append(f'<line x1="{x0}" y1="42" x2="{x1}" y2="42" stroke="#aaaaaa"/>')
        e.append(f'<line x1="{x0}" y1="42" x2="{x0}" y2="48" stroke="#aaaaaa"/>')
        e.append(f'<line x1="{x1}" y1="42" x2="{x1}" y2="48" stroke="#aaaaaa"/>')
        e.append(f'<text x="{(x0+x1)//2}" y="{ly}" text-anchor="middle" '
                 f'fill="#666666" font-size="12">{RUNS[r]}</text>')

    for i, (lab, sub, _, kind) in enumerate(CHAIN):
        x = X0 + i * (BW + GAP)
        e.append(f'<rect x="{x}" y="{Y0}" width="{BW}" height="{BH}" rx="7" '
                 f'fill="{FILL[kind]}" stroke="#8899aa"/>')
        e.append(f'<text x="{x+BW/2:.0f}" y="{Y0+25}" text-anchor="middle" '
                 f'fill="{TEXT[kind]}" font-weight="bold">{lab}</text>')
        if sub:
            e.append(f'<text x="{x+BW/2:.0f}" y="{Y0+BH+18}" text-anchor="middle" '
                     f'fill="#888888" font-size="11">{sub}</text>')
        if i < n - 1:
            ax0, ax1 = x + BW, x + BW + GAP
            e.append(f'<line x1="{ax0}" y1="{Y0+BH/2:.0f}" x2="{ax1-6}" '
                     f'y2="{Y0+BH/2:.0f}" stroke="#556677" stroke-width="1.6"/>')
            e.append(f'<path d="M{ax1-6} {Y0+BH/2-4:.0f} L{ax1} {Y0+BH/2:.0f} '
                     f'L{ax1-6} {Y0+BH/2+4:.0f}" fill="#556677"/>')

    for j, cap in enumerate(CAPTIONS):
        e.append(f'<text x="{X0}" y="{144 + j*17}" fill="#666666" font-size="11.5">{cap}</text>')
    e.append("</svg>")
    out = Path(__file__).resolve().parent / "lineage.svg"
    out.write_text("\n".join(e) + "\n", encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
