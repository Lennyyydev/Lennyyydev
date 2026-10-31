#!/usr/bin/env python3
"""Erzeugt die Projekt-Karten (assets/cards/*.svg) und Link-Knöpfe (assets/links/*.svg) fürs GitHub-Profil.

Gleicher Look wie Banner und Portfolio: Schwarz, blaues Licht, Kode Mono. Schrift und Icons sind eingebettet,
weil GitHub in SVGs nichts von außen nachlädt. Ausführen: python3 .source/cards.py
"""
import base64
from html import escape
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent / "assets"
FONT = base64.b64encode((SRC / "kode-mono.woff2").read_bytes()).decode()
STYLE = f'@font-face{{font-family:"Kode Mono";src:url(data:font/woff2;base64,{FONT}) format("woff2");font-weight:400 700}}text{{font-family:"Kode Mono",ui-monospace,monospace}}'
CHAR = 0.6  # Kode Mono: jedes Zeichen ist 0,6 em breit


def icon(name):
    return "data:image/png;base64," + base64.b64encode((SRC / "icons" / f"{name}.png").read_bytes()).decode()


def wrap(text, width):
    lines, line = [], ""
    for word in text.split():
        if len(line) + len(word) + (1 if line else 0) > width:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + [line] if line else lines


def backdrop(w, h, key):
    return f'''<defs>
  <radialGradient id="g1{key}" cx="15%" cy="0%" r="80%"><stop offset="0" stop-color="#2d68c4" stop-opacity=".38"/><stop offset="1" stop-color="#2d68c4" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2{key}" cx="90%" cy="0%" r="70%"><stop offset="0" stop-color="#2d68c4" stop-opacity=".22"/><stop offset="1" stop-color="#2d68c4" stop-opacity="0"/></radialGradient>
  <clipPath id="c{key}"><rect width="{w}" height="{h}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#c{key})"><rect width="{w}" height="{h}" fill="#000"/><rect width="{w}" height="{h}" fill="url(#g1{key})"/><rect width="{w}" height="{h}" fill="url(#g2{key})"/></g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="13.5" fill="none" stroke="#fff" stroke-opacity=".1"/>'''


# ---------- Projekt-Karten ----------
STATUS = {"live": ("#3ccf7a", "live"), "private": ("#a1a1aa", "private"), "dev": ("#3f7bd9", "in development")}
PROJECTS = [
    ("bmsl", "bmsl", "Best Minecraft Serverlist", "live",
     "german minecraft server list with votes, votifier, live player counts and dashboards for server teams.", "best-minecraft-serverlist.com ↗"),
    ("bmsl-agent", "bmsl-agent", "BMSL Agent", "live",
     "discord bot for the server list community: team alerts, tickets, role sync and slash commands.", "discord bot"),
    ("wildmine-bot", "wildmine", "WildMine Bot", "private",
     "ticket bot for the wildmine discord. saves every ticket as a transcript, with stats for each supporter.", "discord bot"),
    ("wildmine-dashboard", "wildmine", "WildMine Admin Dashboard", "private",
     "staff dashboard with player records, punishments with evidence, team chat and fine-grained permissions.", "internal tool"),
    ("portfolio", "portfolio", "lennylee.dev", "live",
     "my portfolio: projects, skills and github stats. hand-written, self-hosted, no framework.", "lennylee.dev ↗"),
    ("mission-control", "dashboard", "Mission Control", "private",
     "my control center for all servers: status, logs and alerts through lenny's agent. passkey only.", "lk.lennylee.dev"),
]
W, H = 440, 158


def card(key, icon_name, title, status, desc, foot):
    dot, label = STATUS[status]
    lines = wrap(desc, int((W - 112 - 24) / (12.5 * CHAR)))[:3]
    pill_w = len(label) * 11 * CHAR + 30
    text = "".join(f'<text x="100" y="{78 + i * 19}" class="d">{escape(l)}</text>' for i, l in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<style>{STYLE}.t{{font-size:18px;font-weight:700;fill:#fff;letter-spacing:-.01em}}.d{{font-size:12.5px;fill:rgba(255,255,255,.62)}}.f{{font-size:11.5px;fill:rgba(255,255,255,.42)}}.p{{font-size:11px;fill:#d4d4d8}}</style>
{backdrop(W, H, key)}
<rect x="24" y="24" width="60" height="60" rx="14" fill="#111114" stroke="#fff" stroke-opacity=".08"/>
<image href="{icon(icon_name)}" x="30" y="30" width="48" height="48"/>
<text x="100" y="50" class="t">{escape(title)}</text>
<rect x="{W - 20 - pill_w}" y="{H - 36}" width="{pill_w}" height="22" rx="11" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".1"/>
<circle cx="{W - 20 - pill_w + 13}" cy="{H - 25}" r="3.5" fill="{dot}"/>
<text x="{W - 20 - pill_w + 22}" y="{H - 21}" class="p">{escape(label)}</text>
{text}
<text x="100" y="{H - 18}" class="f">{escape(foot)}</text>
</svg>
'''


# ---------- Link-Knöpfe ----------
GLOBE = '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18" fill="none" stroke="currentColor" stroke-width="2"/>'
DISCORD = '<path fill="currentColor" d="M20.32 4.37A19.8 19.8 0 0 0 15.4 2.85a13.6 13.6 0 0 0-.63 1.29 18.4 18.4 0 0 0-5.53 0 13 13 0 0 0-.64-1.29 19.7 19.7 0 0 0-4.92 1.52C.53 9.05-.32 13.6.1 18.09a19.9 19.9 0 0 0 6.03 3.05c.49-.66.92-1.36 1.29-2.1a12.9 12.9 0 0 1-2.03-.97l.5-.39a14.2 14.2 0 0 0 12.22 0l.5.39c-.65.38-1.33.71-2.04.97.37.74.8 1.44 1.29 2.1a19.8 19.8 0 0 0 6.04-3.05c.5-5.2-.84-9.71-3.58-13.72ZM8.02 15.33c-1.18 0-2.16-1.08-2.16-2.42 0-1.33.96-2.42 2.16-2.42 1.21 0 2.18 1.1 2.16 2.42 0 1.34-.96 2.42-2.16 2.42Zm7.97 0c-1.18 0-2.16-1.08-2.16-2.42 0-1.33.96-2.42 2.16-2.42 1.21 0 2.18 1.1 2.16 2.42 0 1.34-.95 2.42-2.16 2.42Z"/>'
BLOCK = '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M12 2.5 20.5 7v10L12 21.5 3.5 17V7Z M3.5 7 12 11.5 20.5 7M12 11.5v10"/>'
SHIELD = '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M12 2.5 19.5 5.5v6c0 4.8-3.2 8.2-7.5 10-4.3-1.8-7.5-5.2-7.5-10v-6Z"/><path d="m8.5 12 2.5 2.5 4.5-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
LINKS = [
    ("lennylee", "lennylee.dev", GLOBE, True),
    ("discord", "discord", DISCORD, False),
    ("serverlist", "serverlist", BLOCK, False),
    ("dashboard", "dashboard", SHIELD, False),
]


def button(key, label, glyph, primary):
    w = int(46 + len(label) * 14 * CHAR + 18)
    bg = 'fill="#3f7bd9"' if primary else 'fill="#0a0a0c" stroke="#fff" stroke-opacity=".14"'
    color = "#ffffff" if primary else "#d4d4d8"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="40" viewBox="0 0 {w} 40" role="img" aria-label="{escape(label)}">
<title>{escape(label)}</title>
<style>{STYLE}.l{{font-size:14px;font-weight:{700 if primary else 400};fill:{color}}}</style>
<rect x=".5" y=".5" width="{w - 1}" height="39" rx="11" {bg}/>
<g transform="translate(16 9) scale(.92)" color="{color}">{glyph}</g>
<text x="46" y="25.5" class="l">{escape(label)}</text>
</svg>
'''


for args in PROJECTS:
    (OUT / "cards" / f"{args[0]}.svg").write_text(card(*args))
for key, label, glyph, primary in LINKS:
    (OUT / "links" / f"{key}.svg").write_text(button(key, label, glyph, primary))
print("ok:", len(PROJECTS), "Karten,", len(LINKS), "Knöpfe")
