#!/usr/bin/env python3
"""Generate docs/lineage.svg: the fully-logged from-scratch lineage of the
89-gates-at-depth-5 record (data: ../evidence/RESULTS.md; every step has a
timestamped log line and a verified circuit in the run archives)."""

from pathlib import Path

# (label, rung, run-index) -- run 0 = 21h ladder (2026-07-13), run 1 = sub-89 (2026-07-14)
CHAIN = [
    ("scratch", "", 0), ("97@3", "d3", 0), ("96@4", "d4", 0), ("95@5", "d5", 0),
    ("94@4", "d6", 0), ("93@7", "d7", 0), ("92@7", "d8", 0), ("92@7", "d9", 0),
    ("89@6", "d10", 0), ("89@5", "", 1),
]
RUNS = {0: "parallel ladder run (2026-07-13, old acceptance rule)",
        1: "sub-89 run (2026-07-14, Pareto tie-break)"}
BW, BH, GAP, X0, Y0 = 86, 40, 22, 20, 52

def main():
    n = len(CHAIN)
    width = X0 * 2 + n * BW + (n - 1) * GAP
    e = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 150" '
         f'font-family="Helvetica,Arial,sans-serif" font-size="14">']
    e.append(f'<rect width="{width}" height="150" fill="white"/>')
    # run group brackets
    first_last = {}
    for i, (_, _, r) in enumerate(CHAIN):
        first_last.setdefault(r, [i, i])[1] = i
    for r, (i0, i1) in first_last.items():
        x0 = X0 + i0 * (BW + GAP)
        x1 = X0 + i1 * (BW + GAP) + BW
        e.append(f'<line x1="{x0}" y1="24" x2="{x1}" y2="24" stroke="#aaaaaa"/>')
        e.append(f'<line x1="{x0}" y1="24" x2="{x0}" y2="32" stroke="#aaaaaa"/>')
        e.append(f'<line x1="{x1}" y1="24" x2="{x1}" y2="32" stroke="#aaaaaa"/>')
        e.append(f'<text x="{(x0+x1)//2}" y="18" text-anchor="middle" fill="#666666" font-size="12">{RUNS[r]}</text>')
    for i, (label, rung, r) in enumerate(CHAIN):
        x = X0 + i * (BW + GAP)
        record = label in ("97@3", "89@5")
        fill = "#1f6feb" if record else ("#eef2f7" if label != "scratch" else "#ffffff")
        tcol = "#ffffff" if record else "#222222"
        e.append(f'<rect x="{x}" y="{Y0}" width="{BW}" height="{BH}" rx="7" fill="{fill}" stroke="#8899aa"/>')
        e.append(f'<text x="{x+BW/2:.0f}" y="{Y0+25}" text-anchor="middle" fill="{tcol}" font-weight="bold">{label}</text>')
        if rung:
            e.append(f'<text x="{x+BW/2:.0f}" y="{Y0+BH+18}" text-anchor="middle" fill="#888888" font-size="11">{rung}</text>')
        if i < n - 1:
            ax0, ax1 = x + BW, x + BW + GAP
            e.append(f'<line x1="{ax0}" y1="{Y0+BH/2:.0f}" x2="{ax1-6}" y2="{Y0+BH/2:.0f}" stroke="#556677" stroke-width="1.6"/>')
            e.append(f'<path d="M{ax1-6} {Y0+BH/2-4:.0f} L{ax1} {Y0+BH/2:.0f} L{ax1-6} {Y0+BH/2+4:.0f}" fill="#556677"/>')
    e.append(f'<text x="{X0}" y="140" fill="#666666" font-size="12">'
             'gates@depth per rung; every arrow is a seeded search step with a timestamped log line and a verified circuit in evidence/.</text>')
    e.append("</svg>")
    out = Path(__file__).resolve().parent / "lineage.svg"
    out.write_text("\n".join(e) + "\n", encoding="utf-8")
    print(f"wrote {out}")

if __name__ == "__main__":
    main()
