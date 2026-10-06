"""Render data/contributions.json as an animated 53-week heatmap SVG."""
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data" / "contributions.json").read_text())
OUT = ROOT / "contrib-heatmap.svg"

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL, GAP, LEFT, TOP = 12, 3, 38, 52
STEP = CELL + GAP
W = 860

days = data["days"]
first = date.fromisoformat(days[0]["date"])
start = first - timedelta(days=(first.weekday() + 1) % 7)  # back to Sunday
weeks = (date.fromisoformat(days[-1]["date"]) - start).days // 7 + 1
H = TOP + 7 * STEP + 62

peak = max((d["count"] for d in days), default=0)
neon_at = max(1, round(peak * 0.6))


def level(d):
    lv = d["level"]
    return 5 if lv >= 4 and d["count"] >= neon_at else lv


css = """
text{font-family:Menlo,Consolas,'DejaVu Sans Mono',monospace}
.t{fill:#8b949e;font-size:10px}
.b{transform-box:fill-box;animation:drop .5s ease-out backwards}
@keyframes drop{from{opacity:0;transform:translateY(-10px)}to{opacity:1;transform:translateY(0)}}
"""
p = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
    f"<style>{css}</style>",
    f'<rect width="{W}" height="{H}" rx="8" fill="#0d1117" stroke="#30363d"/>',
    '<text x="16" y="26" fill="#39d353" font-size="13">$ git log --contributions --last-year</text>',
]

# month labels
last_m = None
for w in range(weeks):
    d = start + timedelta(days=7 * w)
    if d.month != last_m:
        if w > 0 or d.day <= 7:
            p.append(f'<text class="t" x="{LEFT + w * STEP}" y="{TOP - 8}">{d.strftime("%b")}</text>')
        last_m = d.month
for r, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    p.append(f'<text class="t" x="10" y="{TOP + r * STEP + 10}">{name}</text>')

for d in days:
    dt = date.fromisoformat(d["date"])
    idx = (dt - start).days
    col, row = idx // 7, idx % 7
    delay = (col + row) * 0.012
    n = d["count"]
    p.append(
        f'<rect class="b" x="{LEFT + col * STEP}" y="{TOP + row * STEP}" width="{CELL}" height="{CELL}" rx="3" '
        f'fill="{PALETTE[level(d)]}" style="animation-delay:{delay:.3f}s">'
        f'<title>{n} contribution{"s" if n != 1 else ""} on {d["date"]}</title></rect>'
    )

fy = TOP + 7 * STEP + 22
p.append(f'<text class="t" x="{LEFT}" y="{fy + 9}" style="font-size:12px;fill:#c9d1d9">{data["total"]:,} contributions in the last year</text>')
p.append(
    f'<text class="t" x="{LEFT}" y="{fy + 28}">streak {data["current_streak"]}d · longest {data["longest_streak"]}d · '
    f'best day {data["best_day"]["count"]} ({data["best_day"]["date"]})</text>'
)
lx = W - 16 - (6 * STEP) - 70
p.append(f'<text class="t" x="{lx}" y="{fy + 9}">Less</text>')
for i, c in enumerate(PALETTE):
    p.append(f'<rect x="{lx + 30 + i * STEP}" y="{fy}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>')
p.append(f'<text class="t" x="{lx + 34 + 6 * STEP}" y="{fy + 9}">More</text>')
p.append("</svg>")
OUT.write_text("\n".join(p), encoding="utf-8")
print(f"wrote {OUT}")
