"""Generates assets/languages.svg (donut) from your public GitHub repos."""
import json, math, os, pathlib, sys, urllib.request
from xml.sax.saxutils import escape
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import theme as t

USER = os.environ.get("GH_USER", "pham-02")
TOKEN = os.environ.get("GITHUB_TOKEN")
COLORS = ["#ff6ba8", "#ff3b5c", "#5b9cff", "#b794f6", "#f9b4d1", "#7c6a85"]
W, H = 254, 148

def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def collect():
    totals = {}
    for repo in get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner"):
        if repo.get("fork"):
            continue
        for lang, n in get(repo["languages_url"]).items():
            totals[lang] = totals.get(lang, 0) + n
    return totals

def build_svg(totals):
    head = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Language distribution">
  <defs>{t.defs()}</defs>
  {t.card(W, H)}
  <text x="20" y="28" font-family="{t.FONT}" font-size="14" font-weight="600" fill="{t.TEXT}">Languages</text>
'''
    if not totals:
        return head + f'  <text x="20" y="80" font-family="{t.FONT}" font-size="12" fill="{t.MUTED}">No data yet</text>\n</svg>\n'
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])
    top, rest = ranked[:5], sum(v for _, v in ranked[5:])
    if rest:
        top.append(("other", rest))
    total = sum(v for _, v in top)
    cx, cy, r, w = 64, 88, 34, 14
    C = 2 * math.pi * r
    out, offset = [], 0.0
    for i, (name, v) in enumerate(top):
        frac = v / total
        seg = max(frac * C - (1.5 if len(top) > 1 else 0), 0.5)
        out.append(f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{COLORS[i]}" stroke-width="{w}" '
                   f'stroke-dasharray="{seg:.2f} {C - seg:.2f}" stroke-dashoffset="{-offset:.2f}" '
                   f'transform="rotate(-90 {cx} {cy})"/>')
        offset += frac * C
    for i, (name, v) in enumerate(top):
        y = 56 + i * 16
        out.append(f'  <rect x="120" y="{y - 9}" width="9" height="9" rx="2" fill="{COLORS[i]}"/>'
                   f'<text x="135" y="{y}" font-family="{t.FONT}" font-size="12" fill="{t.SOFT}">{escape(name)}</text>')
    return head + "\n".join(out) + "\n</svg>\n"

def main():
    out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "languages.svg"
    out.write_text(build_svg(collect()), encoding="utf-8")

if __name__ == "__main__":
    main()
