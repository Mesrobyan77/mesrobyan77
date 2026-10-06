"""Hand-author a neofetch-style info card SVG. Set STATIC=1 for a frozen frame."""
import os
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "info-card.svg"
STATIC = os.environ.get("STATIC") == "1"

# ---- edit your content here -------------------------------------------------
USER_HOST = "khachik@github"
SECTIONS = [
    ("about", [
        ("Name", "Khachik Mesrobyan"),
        ("Role", "Full-Stack Developer"),
        ("Focus", "Animation, design systems, backends"),
        ("Motto", "Turning ideas into beautiful code."),
    ]),
    ("stack", [
        ("Frontend", "React, TypeScript, Redux, Tailwind"),
        ("Backend", "Node.js, Express, Sequelize"),
        ("Data", "PostgreSQL, MySQL, MongoDB"),
        ("Tools", "Git, Figma, Linux"),
    ]),
    ("contact", [
        ("Mail", "khachik.mesrobyan@gmail.com"),
        ("GitHub", "github.com/mesrobyan77"),
        ("LinkedIn", "in/khachik-mesrobyan"),
    ]),
]
W = 440
TARGET_H = 565   # match the portrait's rendered height (420px wide -> ~565px tall)
# -----------------------------------------------------------------------------

PAD, LINE_H, TOP, FS = 22, 30, 78, 12
KEY_COLORS = ["#61dafb", "#39d353", "#f0883e", "#d2a8ff"]
lines = []
for title, rows in SECTIONS:
    lines.append(("sec", title, ""))
    lines += [("row", k, v) for k, v in rows]
H = max(TARGET_H, TOP + len(lines) * LINE_H + 66)

css = f"""
text{{font-family:Menlo,Consolas,'DejaVu Sans Mono',monospace;font-size:{FS}px}}
.k{{font-weight:700}}.v{{fill:#c9d1d9}}.s{{fill:#6e7681}}
"""
if not STATIC:
    css += """
.ln{animation:in .4s ease-out backwards}
@keyframes in{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:translateX(0)}}
"""

p = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
    f"<style>{css}</style>",
    f'<rect width="{W}" height="{H}" rx="8" fill="#0d1117" stroke="#30363d"/>',
    f'<rect width="{W}" height="30" rx="8" fill="#161b22"/><rect y="20" width="{W}" height="10" fill="#161b22"/>',
    '<circle cx="18" cy="15" r="5" fill="#ff5f56"/><circle cx="36" cy="15" r="5" fill="#ffbd2e"/><circle cx="54" cy="15" r="5" fill="#27c93f"/>',
    f'<text x="{W / 2}" y="19" text-anchor="middle" fill="#8b949e" font-size="11">{USER_HOST}: ~</text>',
]


def anim(i):
    return "" if STATIC else f' class="ln" style="animation-delay:{0.15 + i * 0.09:.2f}s"'


p.append(f'<text x="{PAD}" y="56"{anim(0)}><tspan fill="#39d353">{USER_HOST}</tspan><tspan fill="#8b949e"> ~ $ </tspan><tspan class="v">neofetch</tspan></text>')
n = 0
ci = 0
for i, (kind, a, b) in enumerate(lines, start=1):
    y = TOP + (i - 1) * LINE_H + 14
    if kind == "sec":
        cls = "s" if STATIC else "s ln"
        sty = "" if STATIC else f' style="animation-delay:{0.15 + i * 0.09:.2f}s"'
        p.append(f'<text x="{PAD}" y="{y}" class="{cls}"{sty}>── {escape(a)} ──────────────────</text>')
        ci = 0
    else:
        c = KEY_COLORS[ci % len(KEY_COLORS)]
        ci += 1
        p.append(
            f'<text x="{PAD}" y="{y}"{anim(i)}><tspan class="k" fill="{c}">{escape(a)}</tspan>'
            f'<tspan fill="#8b949e">: </tspan><tspan class="v">{escape(b)}</tspan></text>'
        )

# bottom prompt with blinking cursor + colour strip
py = H - 46
p.append(f'<text x="{PAD}" y="{py}"><tspan fill="#39d353">{USER_HOST}</tspan><tspan fill="#8b949e"> ~ $ </tspan></text>')
cx = PAD + (len(USER_HOST) + 5) * FS * 0.6
blink = '' if STATIC else '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/>'
p.append(f'<rect x="{cx:.1f}" y="{py - 10}" width="7" height="13" fill="#39d353">{blink}</rect>')
y = H - 24
for j, col in enumerate(["#ff5f56", "#ffbd2e", "#27c93f", "#61dafb", "#d2a8ff", "#c9d1d9"]):
    p.append(f'<rect x="{PAD + j * 26}" y="{y}" width="22" height="10" rx="2" fill="{col}"/>')
p.append("</svg>")
OUT.write_text("\n".join(p), encoding="utf-8")
print(f"wrote {OUT} ({W}x{H})")
