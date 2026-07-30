#!/usr/bin/env python3
"""Generate docs/frontier.svg: the published depth-count Pareto frontier for
AES MixColumns against this project's verified circuits.

Data sources (no number here is invented):
  - published frontier and the off-frontier Sun-Yang-Li point: ../README.md and
    ../evidence/RESULTS.md "Notes" (99@3 Shi-Feng-Xu ToSC 2023; 97@4 and 94@5
    Osvik-Canright ePrint 2024/1076; 92@6 Maximov; 88@7 Jean ePrint 2026/1481;
    89 Sun-Yang-Li ePrint 2025/1493). Neither Jean nor Sun-Yang-Li states a
    depth: the 7 and the 9 are both this repo's measurements of its own
    transcriptions, and are marked as such symmetrically.
  - this project's circuits: ../evidence/circuits/spectrum.json
    (97@3, 92@4, 89@5, 88@5 twice, 88@6, 88@7, 88@8), all oracle-verified.
  - ONE frontier is drawn now (v3.1). Until 2026-07-30 the (88, 5) point was held
    only by a circuit whose seed chain runs through Jean's published work, so the
    figure carried a solid own-lineage line and a dotted combined one. A
    from-scratch 88@5 (root constructors.build("naive", 1958)) now holds that
    point, so the two lines collapse into one:
      verified frontier (solid blue)  97@3, 92@4, 88@5, entirely own lineage.
    That is a statement about OUR provenance, not about Jean's result: 88 is his
    published count, he has priority, and nothing here beats it. What changed is
    that this project no longer depends on his circuit to reach depth 5.
  - TWO circuits sit at (88, 5): the from-scratch one (filled blue, the frontier
    point) and the derived one (hollow ring drawn concentrically around it,
    retained and still disclosed as derived work), as is the dominated 88@8.
  - our own 89@5 and 88@6 are verified own-lineage circuits that the from-scratch
    88@5 now dominates: filled blue dots, off the frontier line.
  - our 88@7 ties Jean's published 88@7 with a different circuit (61/88 shared
    masks) -- it does not beat it.
  - the three "superseded" crosses (98@3, 91@6, 89@10) are this project's own
    earlier results, carried over unchanged from the v1 figure.

Stdlib only; writes the SVG next to this script.
"""

from pathlib import Path

# ---- geometry (unchanged from the v1 figure) -------------------------------
W, H = 670, 390
XL, XR, YT, YB = 70, 630, 30, 330          # plot box
DMIN, DMAX = 3, 10                          # depth axis
GMIN, GMAX = 86, 100                        # gate axis
BLUE, GREY, FAINT = "#1f6feb", "#888888", "#bbbbbb"

# (depth, gates, label, dx, dy, anchor)
PUBLISHED = [(3, 99, "99 SFX23", 9, -8, "start"),
             (4, 97, "97 OC24", 9, -8, "start"),
             (5, 94, "94 OC24", 9, -8, "start"),
             (6, 92, "92 Max19", 9, -8, "start"),
             # depth 7 is our own measurement of our transcription -- Jean's
             # note states no depth either (same caveat as SYL25 below)
             (7, 88, "88 Jean26", 9, -22, "start")]
# published but dominated by 88@7, so not a frontier point (depth is our own
# measurement of our transcription -- the paper states none)
PUBLISHED_OFF = [(9, 89, "89 SYL25", 9, -9, "start")]
# this project, verified (spectrum.json). OURS is THE frontier -- one line, all
# own lineage; its depth-5 point was found from scratch.
# label offsets are chosen so no count label is crossed by the frontier line
OURS = [(3, 97, "97", 11, -8, "start"),
        (4, 92, "92", -10, 4, "end"),
        (5, 88, "88 @ 5 from scratch", -12, 20, "end")]
FRONTIER = [(3, 97), (4, 92), (5, 88)]
# ours, own lineage, verified, but dominated by the frontier point above
OURS_DOMINATED = [(5, 89, "89", 8, -8, "start"),
                  (6, 88, "88 @ 6 from scratch", 10, 20, "start")]
TIE = (7, 88)                                # ours == published count and depth
# ours, but the seed chain runs through Jean's published 88 (METHODS.md S9).
# The depth-5 entry is drawn as a ring AROUND the frontier dot: same Pareto
# point, two different circuits, one of them derived.
OURS_DERIVED_RING = (5, 88)
OURS_DERIVED = [(8, 88, "88 @ 8 derived, dominated", 10, 20, "start")]
SUPERSEDED = [(3, 98), (6, 91), (10, 89)]


def x(d):
    return XL + (d - DMIN) * (XR - XL) / (DMAX - DMIN)


def y(g):
    return YB - (g - GMIN) * (YB - YT) / (GMAX - GMIN)


def dot(e, cx, cy, r, fill):
    e.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}"/>')


def hollow(e, cx, cy, stroke, r=5.5):
    e.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="#ffffff" '
             f'stroke="{stroke}" stroke-width="2"/>')


def cross(e, cx, cy, r=5):
    e.append(f'<path d="M{cx-r:.1f} {cy-r:.1f} L{cx+r:.1f} {cy+r:.1f} '
             f'M{cx-r:.1f} {cy+r:.1f} L{cx+r:.1f} {cy-r:.1f}" '
             f'stroke="{FAINT}" stroke-width="2"/>')


def half_dot(e, cx, cy, r=6):
    """Left half published-grey, right half this-work-blue: the same point was
    reached independently by both, with different circuits."""
    e.append(f'<path d="M{cx:.1f} {cy-r:.1f} A{r} {r} 0 0 0 {cx:.1f} {cy+r:.1f} Z" fill="{GREY}"/>')
    e.append(f'<path d="M{cx:.1f} {cy-r:.1f} A{r} {r} 0 0 1 {cx:.1f} {cy+r:.1f} Z" fill="{BLUE}"/>')
    e.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="none" stroke="#444444" stroke-width="0.8"/>')


def label(e, cx, cy, dx, dy, text, fill, anchor="start", size=None, weight=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    s = f' font-size="{size}"' if size else ""
    w = ' font-weight="bold"' if weight else ""
    e.append(f'<text x="{cx+dx:.1f}" y="{cy+dy:.1f}"{a}{s}{w} fill="{fill}">{text}</text>')


def main():
    e = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'font-family="Helvetica,Arial,sans-serif" font-size="13" '
         f'role="img" aria-labelledby="ftitle fdesc">',
         '<title id="ftitle">AES MixColumns: the published depth-count Pareto '
         'frontier versus this work</title>',
         '<desc id="fdesc">Scatter plot, 2-input XOR gate count against circuit '
         'depth. The published frontier (dashed grey) runs 99 gates at depth 3 '
         '(Shi-Feng-Xu 2023), 97 at depth 4 and 94 at depth 5 (Osvik-Canright '
         '2024), 92 at depth 6 (Maximov) and 88 at depth 7 (Jean, ePrint '
         '2026/1481; that paper states no depth either, so the 7 is likewise '
         'this repository\'s own measurement of its transcription). This work '
         'draws a single frontier (solid blue): 97 gates at depth 3, 92 at '
         'depth 4 and 88 at depth 5, every point of it this project\'s own '
         'lineage with no imported material. The depth-5 point is an 88-gate '
         'circuit found from scratch, from a randomized XOR tree over the 32 raw '
         'inputs; it dominates Jean\'s 88 at depth 7 and Maximov\'s 92 at '
         'depth 6 and improves on the published 94 at depth 5 by six gates. It '
         'is not a gate-count record: 88 is Jean\'s published count and Jean has '
         'priority, and what changed is only that this project no longer needs '
         'his circuit to reach depth 5. A hollow blue ring is drawn around that '
         'same depth-5 point for a second, derived 88-gate circuit whose seed '
         'chain passes through Jean\'s published work, retained and still '
         'labelled derived. Filled blue dots off the line mark this project\'s '
         'own 89 at depth 5 and 88 at depth 6, both verified, both dominated by '
         'the depth-5 point; the 88 at depth 6 was also found from scratch and '
         'is a different family. The depth-7 '
         'point is drawn as a half-grey half-blue marker because our 88 there '
         'ties the published 88 with an independent circuit (61 of 88 masks '
         'shared) rather than beating it. A hollow blue marker shows our 88 at '
         'depth 8, derived and dominated by our own 88 at depth 7. A hollow grey '
         'marker shows the published Sun-Yang-Li 89 (ePrint 2025/1493), off '
         'the frontier; that paper states no depth, so it is placed at depth 9, '
         'this repository\'s own measurement of its transcription. Crosses mark '
         'this project\'s own superseded earlier results.</desc>',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="white"/>']

    # gridlines + axis ticks
    for g in range(GMIN, GMAX + 1, 2):
        gy = y(g)
        e.append(f'<line x1="{XL}" y1="{gy:.1f}" x2="{XR}" y2="{gy:.1f}" stroke="#dddddd" stroke-width="1"/>')
        e.append(f'<text x="{XL-8}" y="{gy+4:.1f}" text-anchor="end" fill="#555555">{g}</text>')
    for d in range(DMIN, DMAX + 1):
        gx = x(d)
        e.append(f'<line x1="{gx:.1f}" y1="{YT}" x2="{gx:.1f}" y2="{YB}" stroke="#eeeeee" stroke-width="1"/>')
        e.append(f'<text x="{gx:.1f}" y="{YB+20}" text-anchor="middle" fill="#555555">{d}</text>')
    e.append(f'<rect x="{XL}" y="{YT}" width="{XR-XL}" height="{YB-YT}" fill="none" stroke="#999999"/>')
    e.append(f'<text x="{(XL+XR)//2}" y="{YB+45}" text-anchor="middle" fill="#333333">circuit depth</text>')
    e.append(f'<text x="18" y="180" text-anchor="middle" fill="#333333" '
             f'transform="rotate(-90 18 180)">2-input XOR gates</text>')

    # published frontier
    pts = " ".join(f"{x(d):.1f},{y(g):.1f}" for d, g, *_ in PUBLISHED)
    e.append(f'<polyline points="{pts}" fill="none" stroke="{GREY}" stroke-width="2.5" stroke-dasharray="6,4"/>')
    for d, g, txt, dx, dy, anch in PUBLISHED:
        if (d, g) != TIE:
            dot(e, x(d), y(g), 5, GREY)
        label(e, x(d), y(g), dx, dy, txt, "#666666", anch)

    # published but off the frontier (dominated by 88@7)
    for d, g, txt, dx, dy, anch in PUBLISHED_OFF:
        hollow(e, x(d), y(g), GREY)
        label(e, x(d), y(g), dx, dy, txt, "#666666", anch, size=12)

    # this project's own superseded earlier results
    for d, g in SUPERSEDED:
        cross(e, x(d), y(g))

    # this work: our own verified points that the frontier dominates, then the
    # frontier line, then the frontier dots on top
    for d, g, txt, dx, dy, anch in OURS_DOMINATED:
        dot(e, x(d), y(g), 6, BLUE)
        label(e, x(d), y(g), dx, dy, txt, BLUE, anch,
              size=(12 if len(txt) > 3 else None), weight=(len(txt) <= 3))

    pts = " ".join(f"{x(d):.1f},{y(g):.1f}" for d, g in FRONTIER)
    e.append(f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width="2.5"/>')

    # the derived circuit sits on the SAME Pareto point as the frontier's
    # depth-5 one: a ring around it. fill="none" so the frontier line, which
    # terminates at this point, is not occluded by it.
    rd, rg = OURS_DERIVED_RING
    e.append(f'<circle cx="{x(rd):.1f}" cy="{y(rg):.1f}" r="10" fill="none" '
             f'stroke="{BLUE}" stroke-width="2"/>')

    for d, g, txt, dx, dy, anch in OURS:
        dot(e, x(d), y(g), 6, BLUE)
        label(e, x(d), y(g), dx, dy, txt, BLUE, anch,
              size=(12 if len(txt) > 3 else None), weight=(len(txt) <= 3))
    e.append(f'<text x="{XL+10}" y="322" font-size="11" fill="{BLUE}">'
             f'depth 5: from scratch (filled) + derived (ring)</text>')

    # the tie: same count, same depth, different circuit
    half_dot(e, x(TIE[0]), y(TIE[1]))
    e.append(f'<text x="{x(7)+9:.1f}" y="322" font-size="11" '
             f'fill="{BLUE}">ours: 88 @ 7 ties it - independent, 61/88 masks</text>')

    # ours, derived from published work
    for d, g, txt, dx, dy, anch in OURS_DERIVED:
        hollow(e, x(d), y(g), BLUE)
        label(e, x(d), y(g), dx, dy, txt, BLUE, anch, size=12)

    # legend
    lx, tx = 407, 432
    rows = [("dashline", "published frontier"),
            ("blueline", "this work, verified frontier"),
            ("bluedot", "ours, own lineage, dominated"),
            ("half", "88 @ 7: ours ties published"),
            ("hollowblue", "ours, derived from published"),
            ("hollowgrey", "published, off-frontier"),
            ("cross", "this project, superseded (v1)")]
    for i, (kind, txt) in enumerate(rows):
        ly = 44 + i * 22
        if kind == "dashline":
            e.append(f'<line x1="{lx-17}" y1="{ly-4}" x2="{lx+17}" y2="{ly-4}" stroke="{GREY}" '
                     f'stroke-width="2.5" stroke-dasharray="6,4"/>')
            dot(e, lx, ly - 4, 5, GREY)
        elif kind == "blueline":
            e.append(f'<line x1="{lx-17}" y1="{ly-4}" x2="{lx+17}" y2="{ly-4}" stroke="{BLUE}" stroke-width="2.5"/>')
            dot(e, lx, ly - 4, 6, BLUE)
        elif kind == "bluedot":
            dot(e, lx, ly - 4, 6, BLUE)
        elif kind == "half":
            half_dot(e, lx, ly - 4)
        elif kind == "hollowblue":
            hollow(e, lx, ly - 4, BLUE)
        elif kind == "hollowgrey":
            hollow(e, lx, ly - 4, GREY)
        else:
            cross(e, lx, ly - 4)
        e.append(f'<text x="{tx}" y="{ly}" font-size="12" fill="#333333">{txt}</text>')

    e.append("</svg>")
    out = Path(__file__).resolve().parent / "frontier.svg"
    out.write_text("\n".join(e) + "\n", encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
