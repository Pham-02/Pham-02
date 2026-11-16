"""Shared look for every card: thin gradient rim, rounded corners, soft plum surface."""
FONT = "-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
ACCENT = "#ff6ba8"      # labels / highlights
TEXT = "#fff6fa"
MUTED = "#b49aaa"
SOFT = "#f0d3e0"

def defs(prefix=""):
    return f'''<linearGradient id="{prefix}surface" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#241529"/><stop offset="100%" stop-color="#160d1b"/></linearGradient>
    <linearGradient id="{prefix}rim" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6b3257"/><stop offset="100%" stop-color="#3a2040"/></linearGradient>'''

def card(w, h, prefix="", r=13):
    """Background + rim rect. Inset by 1px so the 1px stroke is never clipped."""
    return (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="url(#{prefix}surface)" '
            f'stroke="url(#{prefix}rim)" stroke-width="1"/>')

def rim(w, h, prefix="", r=13):
    return (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="none" '
            f'stroke="url(#{prefix}rim)" stroke-width="1"/>')
