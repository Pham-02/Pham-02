"""Generates assets/languages.svg (donut) from your public GitHub repos."""
import json, os, math, pathlib, urllib.request
from xml.sax.saxutils import escape

USER = os.environ.get("GH_USER", "pham-02")
TOKEN = os.environ.get("GITHUB_TOKEN")
COLORS = ["#ff4d8d", "#ff3b5c", "#3b82f6", "#a78bfa", "#f9a8d4", "#64748b"]

def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def collect():
    totals = {}
    repos = get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
    for repo in repos:
        if repo.get("fork"):
            continue
        for lang, n in get(repo["languages_url"]).items():
            totals[lang] = totals.get(lang, 0) + n
    return totals

def build_svg(totals):
    font = "-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
    head = f'''<svg xmlns="http://www.w3.org/2000/svg" width="254" height="180" viewBox="0 0 254 180" font-family="{font}">
  <rect x="1" y="1" width="252" height="178" rx="12" fill="#1c1220" stroke="#ff4d8d" stroke-opacity="0.45" stroke-width="2"/>
  <text x="20" y="30" font-size="14" font-weight="700" fill="#ffffff">Languages</text>
'''
    if not totals:
        return head + '  <text x="20" y="100" font-size="12" fill="#c9a8b8">No data yet</text>\n</svg>\n'
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])
    top, rest = ranked[:5], sum(v for _, v in ranked[5:])
    if rest:
        top.append(("other", rest))
    total = sum(v for _, v in top)
    cx, cy, r, w = 66, 106, 40, 16
    C = 2 * math.pi * r
    parts, offset = [], 0.0
    for i, (name, v) in enumerate(top):
        frac = v / total
        seg = max(frac * C - (1.5 if len(top) > 1 else 0), 0.5)
        parts.append(f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{COLORS[i]}" stroke-width="{w}" '
                     f'stroke-dasharray="{seg:.2f} {C - seg:.2f}" stroke-dashoffset="{-offset:.2f}" '
                     f'transform="rotate(-90 {cx} {cy})"/>')
        offset += frac * C
    legend = []
    for i, (name, v) in enumerate(top):
        y = 62 + i * 19
        legend.append(f'  <rect x="130" y="{y - 9}" width="10" height="10" rx="2" fill="{COLORS[i]}"/>'
                      f'<text x="146" y="{y}" font-size="12" fill="#e8d5de">{escape(name)}</text>')
    return head + "\n".join(parts) + "\n" + "\n".join(legend) + "\n</svg>\n"

def main():
    out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "languages.svg"
    out.write_text(build_svg(collect()), encoding="utf-8")

if __name__ == "__main__":
    main()
