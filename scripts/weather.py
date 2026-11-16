"""Generates assets/weather.svg for Tokyo using Open-Meteo (free, no API key)."""
import base64, json, urllib.request, pathlib
from xml.sax.saxutils import escape

CITY, LAT, LON, TZ = "TOKYO", 35.6762, 139.6503, "Asia/Tokyo"
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
    """Uses assets/weather-bg.gif (animated) or .webp/.jpg/.png if present, else a pink/dark gradient."""
    for name, mime in (("weather-bg.gif", "gif"), ("weather-bg.webp", "webp"), ("weather-bg.jpg", "jpeg"), ("weather-bg.png", "png")):
        f = ASSETS / name
        if f.exists():
            b64 = base64.b64encode(f.read_bytes()).decode()
            return (f'<image href="data:image/{mime};base64,{b64}" x="0" y="0" width="414" height="180" '
                    'preserveAspectRatio="xMidYMid slice" clip-path="url(#card)"/>')
    return '<rect width="414" height="180" fill="url(#fallback)" clip-path="url(#card)"/>'

def build_svg(d):
    cur, day = d["current"], d["daily"]
    temp = round(cur["temperature_2m"])
    now = cur["time"]                       # 2026-11-16T08:00
    stamp = f"{now[5:7]}/{now[8:10]} {now[11:16]}"
    cond = CODES.get(cur["weather_code"], "—")
    hi, lo = round(day["temperature_2m_max"][0]), round(day["temperature_2m_min"][0])
    t_cond = CODES.get(day["weather_code"][1], "—")
    t_hi, t_lo = round(day["temperature_2m_max"][1]), round(day["temperature_2m_min"][1])
    font = "-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="414" height="180" viewBox="0 0 414 180" font-family="{font}">
  <defs>
    <clipPath id="card"><rect x="1" y="1" width="412" height="178" rx="12"/></clipPath>
    <linearGradient id="fallback" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a1330"/><stop offset="1" stop-color="#1c1220"/></linearGradient>
    <linearGradient id="shade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#12081a" stop-opacity="0.82"/><stop offset="1" stop-color="#12081a" stop-opacity="0.45"/></linearGradient>
  </defs>
  {background()}
  <rect width="414" height="180" fill="url(#shade)" clip-path="url(#card)"/>
  <rect x="1" y="1" width="412" height="178" rx="12" fill="none" stroke="#ff4d8d" stroke-opacity="0.55" stroke-width="2"/>
  <text x="24" y="40" font-size="16" font-weight="700" letter-spacing="2.5" fill="#ff4d8d">{escape(CITY)}</text>
  <text x="390" y="40" text-anchor="end" font-size="12" fill="#c9a8b8">{escape(stamp)}</text>
  <text x="24" y="124" font-size="62" font-weight="800" fill="#ffffff">{temp}<tspan font-size="26" dy="-24">°C</tspan></text>
  <line x1="178" y1="62" x2="178" y2="152" stroke="#ff4d8d" stroke-opacity="0.5" stroke-width="2"/>
  <text x="196" y="76" font-size="19" fill="#ffffff">{escape(cond)}</text>
  <text x="196" y="102" font-size="15" fill="#ffd6e4">High {hi}° / Low {lo}°</text>
  <text x="196" y="132" font-size="13" fill="#c9a8b8">Tomorrow</text>
  <text x="270" y="132" font-size="15" fill="#ffffff">{escape(t_cond)}</text>
  <text x="196" y="154" font-size="15" fill="#ffd6e4">High {t_hi}° / Low {t_lo}°</text>
</svg>
'''

def main():
    with urllib.request.urlopen(URL, timeout=30) as r:
        data = json.load(r)
    out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "weather.svg"
    out.write_text(build_svg(data), encoding="utf-8")

if __name__ == "__main__":
    main()
