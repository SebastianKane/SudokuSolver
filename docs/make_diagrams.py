#!/usr/bin/env python3
"""Generates the README diagrams. Reproducible: python docs/make_diagrams.py"""
import pathlib

OUT = pathlib.Path(__file__).parent
# palette chosen to read on GitHub light AND dark (solid card background)
BG, GRID, THICK = "#FAF8F2", "#B9B2A4", "#3A3348"
INK, SOFT = "#2A2438", "#8A8296"
GOLD, GOLD_SOFT = "#C9A34A", "#EFE3C4"
PEER = "#DCE7F2"
GOOD, BAD = "#4F7040", "#9C4A38"
C = 30  # cell px

def grid_svg(w, h, body, title=""):
    W, H = 9*C + 40, 9*C + (58 if title else 40)
    ty = 30 if title else 0
    t = (f'<text x="{W/2}" y="22" text-anchor="middle" font-family="Georgia,serif" '
         f'font-size="15" fill="{INK}" font-style="italic">{title}</text>') if title else ""
    lines = []
    for i in range(10):
        sw, col = (2.5, THICK) if i % 3 == 0 else (1, GRID)
        lines.append(f'<line x1="20" y1="{ty+20+i*C}" x2="{20+9*C}" y2="{ty+20+i*C}" stroke="{col}" stroke-width="{sw}"/>')
        lines.append(f'<line x1="{20+i*C}" y1="{ty+20}" x2="{20+i*C}" y2="{ty+20+9*C}" stroke="{col}" stroke-width="{sw}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<rect width="{W}" height="{H}" fill="{BG}" rx="8"/>{t}{body}{"".join(lines)}</svg>')

def cell_rect(r, c, fill, ty=0):
    return f'<rect x="{20+c*C}" y="{ty+20+r*C}" width="{C}" height="{C}" fill="{fill}"/>'

def cell_text(r, c, s, fill=INK, size=15, ty=0, bold=False):
    fw = ' font-weight="bold"' if bold else ""
    return (f'<text x="{20+c*C+C/2}" y="{ty+20+r*C+C/2+5}" text-anchor="middle" '
            f'font-family="Helvetica,Arial,sans-serif" font-size="{size}" fill="{fill}"{fw}>{s}</text>')

# 1 — constraint graph: target cell + its 20 peers
tr, tc = 3, 4
body = []
for c in range(9):
    if c != tc: body.append(cell_rect(tr, c, PEER))
for r in range(9):
    if r != tr: body.append(cell_rect(r, tc, PEER))
for r in range(3, 6):
    for c in range(3, 6):
        if (r, c) != (tr, tc): body.append(cell_rect(r, c, PEER))
body.append(cell_rect(tr, tc, GOLD))
body.append(cell_text(tr, tc, "?", "#FFFFFF", 17, bold=True))
(OUT/"constraint-graph.svg").write_text(grid_svg(9, 9, "".join(body),
    ""))

# 2 — domain by subtraction (zoom on one row/box context)
body = []
row_vals = {0:"5", 2:"3", 6:"9", 8:"1"}
for c, v in row_vals.items():
    body.append(cell_text(3, c, v, SOFT))
col_vals = {0:"7", 5:"2", 8:"4"}
for r, v in col_vals.items():
    body.append(cell_text(r, 4, v, SOFT))
box_vals = {(4,3):"8", (5,5):"6"}
for (r,c), v in box_vals.items():
    body.append(cell_text(r, c, v, SOFT))
body.append(cell_rect(3, 4, GOLD_SOFT))
body.append(cell_text(3, 4, "?", GOLD, 16, bold=True))
(OUT/"domain-subtraction.svg").write_text(grid_svg(9, 9, "".join(body),
    ""))

# 3 — MRV: candidate counts, minimum speaks first
body = []
counts = {(0,1):"4",(0,7):"5",(1,3):"3",(2,5):"6",(4,2):"2",(4,6):"4",
          (6,0):"5",(6,8):"3",(7,4):"7",(8,2):"4"}
for (r,c), n in counts.items():
    if (r,c) == (4,2):
        body.append(cell_rect(r, c, GOLD))
        body.append(cell_text(r, c, n, "#FFFFFF", 15, bold=True))
    else:
        body.append(cell_text(r, c, n, SOFT, 13))
(OUT/"mrv-choice.svg").write_text(grid_svg(9, 9, "".join(body),
    ""))

print("diagrams written:", [p.name for p in OUT.glob("*.svg")])
