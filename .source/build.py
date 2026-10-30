#!/usr/bin/env python3
"""Erzeugt die zwei Bilder des GitHub-Profils: assets/banner.svg und assets/activity.svg.

Die Zahlen kommen aus der github.json des Portfolios (erzeugt von /srv/portfolio/.source/github.py).
Schrift und Bilder werden eingebettet, weil GitHub in SVGs nichts von außen nachlädt.
"""
import base64
import json
from datetime import date, timedelta
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent / "assets"
GH = json.loads(Path("/srv/portfolio/.source/github.json").read_text())


def b64(name):
    return base64.b64encode((SRC / name).read_bytes()).decode()


FONT = f'@font-face{{font-family:"Kode Mono";src:url(data:font/woff2;base64,{b64("kode-mono.woff2")}) format("woff2");font-weight:400 700}}'
MONO = "font-family:'Kode Mono',ui-monospace,monospace"
CHAR = 0.6  # Kode Mono: jedes Zeichen ist 0,6 em breit
W = 840

# Blaues Licht wie auf der Portfolio-Seite
BACKDROP = '''<defs>
  <radialGradient id="r1" cx="18%" cy="0%" r="75%"><stop offset="0" stop-color="#2d68c4" stop-opacity=".42"/><stop offset="1" stop-color="#2d68c4" stop-opacity="0"/></radialGradient>
  <radialGradient id="r2" cx="85%" cy="0%" r="70%"><stop offset="0" stop-color="#2d68c4" stop-opacity=".3"/><stop offset="1" stop-color="#2d68c4" stop-opacity="0"/></radialGradient>
  <clipPath id="card"><rect width="{w}" height="{h}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{w}" height="{h}" fill="#000"/>
  <rect width="{w}" height="{h}" fill="url(#r1)"/>
  <rect width="{w}" height="{h}" fill="url(#r2)"/>
</g>
<rect x=".5" y=".5" width="{w1}" height="{h1}" rx="15.5" fill="none" stroke="#fff" stroke-opacity=".08"/>'''


def backdrop(h):
    return BACKDROP.format(w=W, h=h, w1=W - 1, h1=h - 1)


# ---------- Banner ----------
PHRASES = [
    "building best-minecraft-serverlist.com",
    "next.js and typescript, mostly after midnight",
    "self-hosting everything on my own server",
    "writing discord bots for minecraft communities",
]
SLOT = 5.5  # Sekunden pro Satz
H_BANNER = 240
TITLE, SUB = 44, 15
X0, Y_TITLE, Y_SUB = 52, 118, 160


def pct(t):
    return f"{t / (SLOT * len(PHRASES)) * 100:.3f}%"


def typewriter():
    css, out = [], []
    wmax = max(len(p) for p in PHRASES) * SUB * CHAR
    for i, text in enumerate(PHRASES):
        n, w = len(text), len(text) * SUB * CHAR
        s, typed, gone = i * SLOT, i * SLOT + n * .055, (i + 1) * SLOT
        held = gone - .7
        # Clip-Rechteck und Cursor wandern gemeinsam von links nach rechts (Schritt = ein Zeichen)
        css.append(f'''@keyframes t{i}{{0%{{transform:translateX(-{wmax:.1f}px)}}
{pct(s)}{{transform:translateX(-{w:.1f}px);animation-timing-function:steps({n},end)}}
{pct(typed)}{{transform:translateX(0)}}
{pct(held)}{{transform:translateX(0);animation-timing-function:steps({n},end)}}
{pct(gone)}{{transform:translateX(-{w:.1f}px)}}
100%{{transform:translateX(-{wmax:.1f}px)}}}}
@keyframes v{i}{{0%,{pct(s - .001) if i else "0%"}{{opacity:0}}{pct(s)},{pct(gone - .001)}{{opacity:1}}{pct(gone)},100%{{opacity:0}}}}
.t{i}{{animation:t{i} {SLOT * len(PHRASES)}s infinite}}
.v{i}{{animation:v{i} {SLOT * len(PHRASES)}s infinite step-end}}''')
        out.append(f'''<clipPath id="c{i}"><rect class="t{i}" x="0" y="-20" width="{w:.1f}" height="30"/></clipPath>
<g class="v{i} moving"><text class="sub" clip-path="url(#c{i})">{text}</text>
<g class="t{i}"><rect class="caret" x="{w + 2:.1f}" y="-12" width="9" height="16"/></g></g>''')
    return "\n".join(css), "\n".join(out)


def banner():
    tw_css, tw = typewriter()
    name_x = X0 + len("hi, i'm ") * TITLE * CHAR
    name_w = len("lenny") * TITLE * CHAR
    uy = Y_TITLE + 12
    # Zwei leicht schiefe Striche, wie mit dem Stift gezogen
    line1 = f"M{name_x - 3:.0f} {uy + 1} C{name_x + name_w * .3:.0f} {uy - 2}, {name_x + name_w * .7:.0f} {uy + 3}, {name_x + name_w + 4:.0f} {uy - 1}"
    line2 = f"M{name_x + 2:.0f} {uy + 5} C{name_x + name_w * .35:.0f} {uy + 2}, {name_x + name_w * .65:.0f} {uy + 6}, {name_x + name_w - 2:.0f} {uy + 3}"
    cx, cy, r = W - 52 - 84, H_BANNER / 2, 70
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H_BANNER}" viewBox="0 0 {W} {H_BANNER}" role="img" aria-label="hi, i'm lenny">
<title>hi, i'm lenny</title>
<style>{FONT}
.title{{{MONO};font-size:{TITLE}px;font-weight:700;letter-spacing:-.02em;fill:#fff}}
.sub{{{MONO};font-size:{SUB}px;font-weight:300;fill:rgba(255,255,255,.62)}}
.caret{{fill:rgba(255,255,255,.75);animation:blink 1s steps(1) infinite}}
.ink{{fill:none;stroke:#3f7bd9;stroke-width:2;stroke-linecap:round;stroke-dasharray:170;stroke-dashoffset:170;animation:draw .9s cubic-bezier(.4,0,.2,1) forwards}}
.ink2{{animation-delay:.75s}}
.fade{{animation:in .7s cubic-bezier(.2,.7,.2,1) both}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes in{{from{{opacity:0;transform:translateY(-6px)}}}}
{tw_css}
.still{{display:none}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.ink{{stroke-dashoffset:0}}.moving{{display:none}}.still{{display:inline}}}}
</style>
{backdrop(H_BANNER)}
<g class="fade"><text class="title" x="{X0}" y="{Y_TITLE}">hi, i'm lenny</text></g>
<path class="ink" d="{line1}"/><path class="ink ink2" d="{line2}"/>
<g transform="translate({X0} {Y_SUB})">
<text class="sub still">{PHRASES[0]}</text>
{tw}
</g>
<clipPath id="pfp"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
<circle cx="{cx}" cy="{cy + 10}" r="{r - 6}" fill="#2d68c4" opacity=".35" filter="url(#glow)"/>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
<image href="data:image/webp;base64,{b64("avatar.webp")}" x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" clip-path="url(#pfp)"/>
<image href="data:image/webp;base64,{b64("deco.webp")}" x="{cx - r * 1.2:.0f}" y="{cy - r * 1.2:.0f}" width="{r * 2.4:.0f}" height="{r * 2.4:.0f}"/>
</svg>
'''


# ---------- Aktivität ----------
LANG_COLORS = {
    "TypeScript": "#3178c6", "JavaScript": "#f1e05a", "PLpgSQL": "#336790", "Java": "#b07219",
    "CSS": "#663399", "HTML": "#e34c26", "Python": "#3572a5", "Shell": "#89e051",
}
LEVELS = ["rgba(255,255,255,.06)", "#16305a", "#1f4b8f", "#2d68c4", "#6a9ff0"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
CELL, GAP = 11, 3
PAD = 32


def level(n):
    return 0 if n == 0 else 1 if n < 4 else 2 if n < 10 else 3 if n < 20 else 4


def activity():
    today = date.fromisoformat(GH["updated"])
    days = GH["days"]
    # Letzte 53 Wochen, Spalte = Woche (Sonntag oben), endet mit der aktuellen Woche
    end = today + timedelta(days=(5 - today.weekday()) % 7)
    start = end - timedelta(weeks=53) + timedelta(days=1)
    year = sum(n for d, n in days.items() if date.fromisoformat(d) > today - timedelta(days=365))
    best = max(days.values())
    streak, d = 0, today if days.get(today.isoformat()) else today - timedelta(days=1)
    while days.get(d.isoformat()):
        streak, d = streak + 1, d - timedelta(days=1)

    stats = [(year, "commits, past year"), (GH["repos"], "repositories"), (best, "best day"), (streak, "day streak")]
    col_w = (W - 2 * PAD) / len(stats)
    stat_svg = "".join(
        f'<text class="num" x="{PAD + i * col_w:.0f}" y="78">{v}</text><text class="lbl" x="{PAD + i * col_w:.0f}" y="98">{k}</text>'
        for i, (v, k) in enumerate(stats))

    y_bar = 130
    bar, x = [], 0.0
    span = W - 2 * PAD
    total = sum(p for _, p in GH["languages"])
    for name, p in GH["languages"]:
        w = p / total * span
        bar.append(f'<rect x="{PAD + x:.2f}" y="{y_bar}" width="{w:.2f}" height="6" fill="{LANG_COLORS.get(name, "#8b8b8b")}"/>')
        x += w
    # Legende bricht in eine zweite Zeile um, wenn sie nicht mehr passt
    lx, ly, legend = PAD, y_bar + 27, []
    for name, p in GH["languages"]:
        w = 13 + len(f"{name} {p}%") * 12 * CHAR
        if lx + w > W - PAD:
            lx, ly = PAD, ly + 22
        legend.append(f'<circle cx="{lx + 4}" cy="{ly}" r="4" fill="{LANG_COLORS.get(name, "#8b8b8b")}"/>'
                      f'<text class="lang" x="{lx + 13}" y="{ly + 4}">{name} <tspan class="dim">{p}%</tspan></text>')
        lx += w + 20

    y_cal = ly + 50
    cells, months, d = [], [], start
    grid_w = 53 * (CELL + GAP) - GAP
    ox = PAD + (span - grid_w) / 2
    while d <= end:
        col, row = (d - start).days // 7, (d.weekday() + 1) % 7
        x, y = ox + col * (CELL + GAP), y_cal + row * (CELL + GAP)
        n = days.get(d.isoformat(), 0) if d <= today else 0
        fill = LEVELS[level(n)] if d <= today else "rgba(255,255,255,.025)"
        cells.append(f'<rect x="{x:.0f}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{fill}"/>')
        if d.day == 1 and col < 52:
            months.append(f'<text class="lbl" x="{x:.0f}" y="{y_cal - 9}">{MONTHS[d.month - 1]}</text>')
        d += timedelta(days=1)

    h = y_cal + 7 * (CELL + GAP) + 40
    kx = W - PAD - 30 - len(LEVELS) * 15  # Kästchen zwischen „less“ und „more“
    key = "".join(f'<rect x="{kx + i * 15}" y="{h - 34}" width="{CELL}" height="{CELL}" rx="2.5" fill="{c}"/>' for i, c in enumerate(LEVELS))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{year} commits in the last year">
<title>GitHub activity of Lennyyydev</title>
<style>{FONT}
text{{{MONO}}}
.head{{font-size:13px;font-weight:500;fill:rgba(255,255,255,.6)}}
.num{{font-size:26px;font-weight:700;fill:#fff;letter-spacing:-.02em}}
.lbl{{font-size:11px;font-weight:300;fill:rgba(255,255,255,.42)}}
.lang{{font-size:12px;fill:#d4d4d8}}
.dim{{fill:rgba(255,255,255,.42);font-weight:300}}
</style>
{backdrop(h)}
<text class="head" x="{PAD}" y="40">activity</text>
<text class="lbl" x="{W - PAD}" y="40" text-anchor="end">updated {MONTHS[today.month - 1].lower()} {today.day}, {today.year}</text>
{stat_svg}
<clipPath id="bar"><rect x="{PAD}" y="{y_bar}" width="{span}" height="6" rx="3"/></clipPath>
<g clip-path="url(#bar)">{"".join(bar)}</g>
{"".join(legend)}
{"".join(months)}
{"".join(cells)}
<text class="lbl" x="{PAD}" y="{h - 25}">commits in private repos, last 12 months</text>
<text class="lbl" x="{kx - 8}" y="{h - 25}" text-anchor="end">less</text>{key}<text class="lbl" x="{W - PAD}" y="{h - 25}" text-anchor="end">more</text>
</svg>
'''


OUT.mkdir(exist_ok=True)
(OUT / "banner.svg").write_text(banner())
(OUT / "activity.svg").write_text(activity())
print("ok", (OUT / "banner.svg").stat().st_size, (OUT / "activity.svg").stat().st_size)
