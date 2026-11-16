"""Generates assets/weather.svg for Tokyo using Open-Meteo (free, no API key)."""
import base64, json, pathlib, sys, urllib.request
from xml.sax.saxutils import escape
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import theme as t

CITY, LAT, LON, TZ = "TOKYO", 35.6762, 139.6503, "Asia/Tokyo"
W, H = 414, 148
URL = (f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}"
       "&current=temperature_2m,weather_code"
       "&daily=temperature_2m_max,temperature_2m_min,weather_code"
       f"&timezone={TZ.replace('/', '%2F')}&forecast_days=2")

CODES = {0: "Clear sky", 1: "Mostly clear", 2: "Partly cloudy", 3: "Overcast",
         45: "Fog", 48: "Fog", 51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
         56: "Freezing drizzle", 57: "Freezing drizzle", 61: "Light rain", 63: "Rain",
         65: "Heavy rain", 66: "Freezing rain", 67: "Freezing rain", 71: "Light snow",
         73: "Snow", 75: "Heavy snow", 77: "Snow grains", 80: "Rain showers",
         81: "Rain showers", 82: "Heavy showers", 85: "Snow showers", 86: "Snow showers",
         95: "Thunderstorm", 96: "Thunderstorm", 99: "Thunderstorm"}

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"

def background():
    """assets/weather-bg.gif (animated) or .webp/.jpg/.png if present, else the plain card surface."""
    for name, mime in (("weather-bg.gif", "gif"), ("weather-bg.webp", "webp"),
                       ("weather-bg.jpg", "jpeg"), ("weather-bg.png", "png")):
        f = ASSETS / name
        if f.exists():
            b64 = base64.b64encode(f.read_bytes()).decode()
            return (f'<image href="data:image/{mime};base64,{b64}" x="0" y="0" width="{W}" height="{H}" '
                    'preserveAspectRatio="xMidYMid slice" clip-path="url(#clip)"/>'
                    f'<rect width="{W}" height="{H}" fill="url(#shade)" clip-path="url(#clip)"/>')
    return ""

def build_svg(d):
    cur, day = d["current"], d["daily"]
    temp = round(cur["temperature_2m"])
    now = cur["time"]                       # 2026-11-16T08:00
    stamp = f"{now[5:7]}/{now[8:10]} {now[11:16]}"
    cond = CODES.get(cur["weather_code"], "-")
    hi, lo = round(day["temperature_2m_max"][0]), round(day["temperature_2m_min"][0])
    t_cond = CODES.get(day["weather_code"][1], "-")
    t_hi, t_lo = round(day["temperature_2m_max"][1]), round(day["temperature_2m_min"][1])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(CITY.title())}: now {temp}°C, {escape(cond)}. Today high {hi}°, low {lo}°. Tomorrow {escape(t_cond)}, high {t_hi}°, low {t_lo}°.">
  <defs>{t.defs()}
    <clipPath id="clip"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="13"/></clipPath>
    <linearGradient id="shade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#12081a" stop-opacity="0.78"/><stop offset="1" stop-color="#12081a" stop-opacity="0.38"/></linearGradient>
  </defs>
  {t.card(W, H)}
  {background()}
  {t.rim(W, H)}
  <g font-family="{t.FONT}">
    <text x="20" y="28" fill="{t.ACCENT}" font-size="15" font-weight="600" letter-spacing="1.2">{escape(CITY)}</text>
    <text x="394" y="28" text-anchor="end" fill="{t.MUTED}" font-size="11">{escape(stamp)}</text>
    <text x="81.5" y="86" text-anchor="middle" dominant-baseline="central" fill="{t.TEXT}" font-size="54" font-weight="600">{temp}<tspan font-size="28">°C</tspan></text>
    <line x1="163" y1="45" x2="163" y2="127" stroke="#6b3257" stroke-opacity="0.8"/>
    <text x="180" y="58" fill="{t.TEXT}" font-size="17">{escape(cond)}</text>
    <text x="180" y="83" fill="{t.SOFT}" font-size="15">High {hi}° / Low {lo}°</text>
    <text x="180" y="110" fill="{t.MUTED}" font-size="12">Tomorrow</text>
    <text x="248" y="110" fill="{t.SOFT}" font-size="14">{escape(t_cond)}</text>
    <text x="180" y="131" fill="{t.SOFT}" font-size="15">High {t_hi}° / Low {t_lo}°</text>
  </g>
</svg>
'''

def main():
    with urllib.request.urlopen(URL, timeout=30) as r:
        data = json.load(r)
    (ASSETS / "weather.svg").write_text(build_svg(data), encoding="utf-8")

if __name__ == "__main__":
    main()
