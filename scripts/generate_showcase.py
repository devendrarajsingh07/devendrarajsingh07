"""SVG assets for the banner-showcase profile layout.

Everything here is generated from config.yml so the profile stays editable
from one place. GitHub serves README images through a sandboxed proxy, so
each SVG is self-contained: no external fonts, scripts or linked images
(the banner photo is embedded as a data URI).
"""

import base64
import json
import math
import io
import os
from xml.sax.saxutils import escape

FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"


def _palette(config):
    p = config.get("palette", {})
    return {
        "bg": p.get("background", "#0c1330"),
        "accent": p.get("accent", "#2563eb"),
        "cyan": p.get("cyan", "#0ea5e9"),
        "text": p.get("text", "#e7f0ff"),
        "muted": p.get("muted", "#cfdcf5"),
        "chip": p.get("chip", "#13204a"),
        "border": p.get("border", "#2d3c68"),
    }


def _photo_data_uri(project_dir, size=220):
    """Return the portrait as a small JPEG data URI (keeps the banner light)."""
    path = os.path.join(project_dir, "assets", "photo.jpg")
    try:
        from PIL import Image
        im = Image.open(path).convert("RGB")
        im.thumbnail((size, size))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=82, optimize=True)
        data = buf.getvalue()
    except ImportError:
        with open(path, "rb") as f:
            data = f.read()
    return "data:image/jpeg;base64," + base64.b64encode(data).decode("ascii")


def _globe(x, y, color):
    return (f'<g transform="translate({x},{y})" fill="none" stroke="{color}" stroke-width="1.8">'
            '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.2 3 14.8 0 18M12 3c-3 3.2-3 14.8 0 18"/></g>')


def _mail(x, y, color):
    return (f'<g transform="translate({x},{y})" fill="none" stroke="{color}" stroke-width="1.8">'
            '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></g>')


def generate_banner_svg(output_path, config, project_dir):
    c = _palette(config)
    w, h = 1280, 330
    name = escape(config.get("name", "").upper())
    subtitle = escape(config.get("banner_subtitle", config.get("role", "")))
    website = escape(config.get("website", ""))
    email = escape(config.get("email", ""))
    photo = _photo_data_uri(project_dir)

    def slashes(x0, direction):
        out = []
        for i in range(3):
            x = x0 + i * 62 * direction
            skew = 36 * direction
            pts = [(x, 298), (x + 42 * direction, 298), (x + 42 * direction + skew, 228), (x + skew, 228)]
            out.append('<polygon points="%s" fill="none" stroke="%s" stroke-opacity="0.55" stroke-width="1.6"/>'
                       % (" ".join(f"{a},{b}" for a, b in pts), c["text"]))
        return "".join(out)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{name}: {subtitle}">
  <defs>
    <radialGradient id="arc">
      <stop offset="0%" stop-color="{c['accent']}"/>
      <stop offset="55%" stop-color="{c['cyan']}" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="{c['bg']}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="photo"><circle cx="{w // 2}" cy="92" r="52"/></clipPath>
    <style>
      .glow {{ animation: pulse 6s ease-in-out infinite; transform-origin: 50% 100%; }}
      @keyframes pulse {{ 0%,100% {{ opacity: 0.9; }} 50% {{ opacity: 1; }} }}
    </style>
  </defs>
  <rect width="{w}" height="{h}" rx="18" fill="{c['bg']}"/>
  <ellipse class="glow" cx="{w // 2}" cy="{h + 70}" rx="620" ry="400" fill="url(#arc)"/>
  {slashes(48, 1)}
  {slashes(w - 48, -1)}
  {_globe(52, 34, c['muted'])}
  <text x="84" y="52" font-family="{FONT}" font-size="17" fill="{c['muted']}">{website}</text>
  {_mail(w - 52 - 24, 34, c['muted'])}
  <text x="{w - 86}" y="52" text-anchor="end" font-family="{FONT}" font-size="17" fill="{c['muted']}">{email}</text>
  <circle cx="{w // 2}" cy="92" r="56" fill="{c['text']}"/>
  <image href="{photo}" x="{w // 2 - 52}" y="40" width="104" height="104" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo)"/>
  <text x="{w // 2}" y="222" text-anchor="middle" font-family="{FONT}" font-size="60" font-weight="800" letter-spacing="2" fill="{c['text']}">{name}</text>
  <text x="{w // 2}" y="262" text-anchor="middle" font-family="{FONT}" font-size="18" letter-spacing="4" fill="{c['muted']}">{subtitle}</text>
</svg>
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Successfully generated banner SVG: {output_path}")


def _luminance(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _load_brand_icons():
    """Logo paths from Simple Icons (CC0), vendored in scripts/brand_icons.json."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand_icons.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def generate_orbit_svg(output_path, config, mode="dark"):
    """Tech stack as app-icon tiles on two counter-rotating rings.

    Each ring spins around the centre while every tile counter-spins, so the
    logos stay upright. Pure CSS animation, so it plays inside GitHub READMEs.
    """
    c = _palette(config)
    icons = _load_brand_icons()
    orbit = config.get("orbit", {})
    rings = [
        (orbit.get("inner", []), 112, 60, 48, "spin-r"),
        (orbit.get("outer", []), 200, 52, 80, "spin"),
    ]
    size = 470
    cx = cy = size / 2

    if mode == "dark":
        tile, stroke, track, dark_logo = c["chip"], c["border"], "#2d3c68", c["text"]
    else:
        tile, stroke, track, dark_logo = "#ffffff", "#d5deec", "#c7d3e8", None

    parts, names = [], []
    for slugs, radius, tile_size, duration, direction in rings:
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{track}" '
                     f'stroke-width="1.2" stroke-dasharray="3 7"/>')
        tiles = []
        for k, slug in enumerate(slugs):
            icon = icons.get(slug)
            if not icon:
                print(f"  warning: no icon data for '{slug}', skipped")
                continue
            names.append(icon["title"])
            angle = 2 * math.pi * k / len(slugs) - math.pi / 2
            x = cx + radius * math.cos(angle) - tile_size / 2
            y = cy + radius * math.sin(angle) - tile_size / 2
            color = "#" + icon["hex"]
            if dark_logo and _luminance(color) < 0.22:
                color = dark_logo
            logo = tile_size * 0.56
            off = (tile_size - logo) / 2
            scale = logo / 24
            tiles.append(
                f'<g transform="translate({x:.1f},{y:.1f})"><g class="up {direction}-u" style="animation-duration:{duration}s">'
                f'<rect width="{tile_size}" height="{tile_size}" rx="{tile_size * 0.26:.1f}" fill="{tile}" stroke="{stroke}" stroke-width="1.2"/>'
                f'<path transform="translate({off:.1f},{off:.1f}) scale({scale:.3f})" d="{icon["path"]}" fill="{color}"/>'
                '</g></g>')
        parts.append(f'<g class="{direction}" style="animation-duration:{duration}s">{"".join(tiles)}</g>')

    centre = (f'<circle cx="{cx}" cy="{cy}" r="46" fill="{c["accent"]}" fill-opacity="0.18"/>'
              f'<circle cx="{cx}" cy="{cy}" r="34" fill="{c["accent"]}"/>'
              f'<path d="M{cx - 9} {cy - 10} l-10 10 10 10 M{cx + 9} {cy - 10} l10 10 -10 10" fill="none" '
              'stroke="#ffffff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}" role="img" aria-label="Tech stack: {escape(", ".join(names))}">
  <style>
    .spin, .spin-r {{ transform-origin: {cx}px {cy}px; animation-timing-function: linear; animation-iteration-count: infinite; }}
    .spin {{ animation-name: cw; }}
    .spin-r {{ animation-name: ccw; }}
    .up {{ transform-box: fill-box; transform-origin: center; animation-timing-function: linear; animation-iteration-count: infinite; }}
    .spin-u {{ animation-name: ccw; }}
    .spin-r-u {{ animation-name: cw; }}
    @keyframes cw {{ to {{ transform: rotate(360deg); }} }}
    @keyframes ccw {{ to {{ transform: rotate(-360deg); }} }}
  </style>
  {"".join(parts)}
  {centre}
</svg>
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Successfully generated tech-stack orbit SVG ({mode}): {output_path}")


ICONS = {
    "email": '<rect x="17" y="19" width="22" height="17" rx="2.5" fill="none" stroke="{t}" stroke-width="2"/>'
             '<path d="M17 21.5l11 7.5 11-7.5" fill="none" stroke="{t}" stroke-width="2"/>',
    "linkedin": '<text x="28" y="35" text-anchor="middle" font-family="' + FONT + '" font-size="21" font-weight="800" fill="{t}">in</text>',
    "portfolio": '<g transform="translate(16,16)" fill="none" stroke="{t}" stroke-width="2">'
                 '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2c3.4 3.6 3.4 16.4 0 20M12 2c-3.4 3.6-3.4 16.4 0 20"/></g>',
    "github": '<path d="M23 21l-6 7 6 7M33 21l6 7-6 7" fill="none" stroke="{t}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
}


def generate_icons(output_dir, config):
    c = _palette(config)
    os.makedirs(output_dir, exist_ok=True)
    for name, body in ICONS.items():
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 56 56" width="56" height="56" role="img" aria-label="{name}">'
               f'<circle cx="28" cy="28" r="26.5" fill="{c["chip"]}" stroke="{c["border"]}" stroke-width="1.5"/>'
               + body.format(t=c["text"]) + '</svg>\n')
        with open(os.path.join(output_dir, f"{name}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)
    print(f"Successfully generated contact icons in: {output_dir}")


def generate_footer_svg(output_path, config):
    c = _palette(config)
    w, h = 1280, 90
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">
  <style>
    .a {{ animation: drift 9s ease-in-out infinite alternate; }}
    .b {{ animation: drift 12s ease-in-out infinite alternate-reverse; }}
    @keyframes drift {{ from {{ transform: translateX(-40px); }} to {{ transform: translateX(0); }} }}
  </style>
  <path class="a" d="M-40 46 C 170 0, 380 92, 640 46 S 1110 0, 1320 46 L 1320 {h} L -40 {h} Z" fill="{c['accent']}" fill-opacity="0.6"/>
  <path class="b" d="M-40 62 C 210 24, 430 104, 670 60 S 1120 28, 1320 64 L 1320 {h} L -40 {h} Z" fill="{c['cyan']}" fill-opacity="0.5"/>
</svg>
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Successfully generated footer SVG: {output_path}")


def _wrap(text, max_chars):
    words, lines, line = text.split(), [], ""
    for word in words:
        if len(line) + len(word) + 1 > max_chars and line:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        lines.append(line)
    return lines


def generate_project_card_svg(output_path, config):
    """A pinned-repo style card for the newest project in config.yml."""
    c = _palette(config)
    p = config.get("projects", [{}])[0]
    desc = _wrap(p.get("desc", ""), 58)[:5]
    w, h = 470, 140 + len(desc) * 21
    desc_svg = "".join(
        f'<text x="24" y="{96 + i * 21}" font-family="{FONT}" font-size="14" fill="{c["muted"]}">{escape(line)}</text>'
        for i, line in enumerate(desc))
    meta = escape(f'{p.get("area", "")} · {p.get("date", "")}'.strip(" ·"))
    live = ""
    if p.get("demo"):
        live = (f'<circle cx="{w - 98}" cy="35" r="4" fill="#4ade80"/>'
                f'<text x="{w - 88}" y="40" font-family="{FONT}" font-size="13" fill="#4ade80">live demo</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Latest project: {escape(p.get("name", ""))}">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="{c['bg']}"/><stop offset="100%" stop-color="#1e3a8a"/></linearGradient></defs>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="url(#g)" stroke="{c['border']}"/>
  <text x="24" y="42" font-family="{FONT}" font-size="22" font-weight="700" fill="{c['text']}">{escape(p.get("name", ""))}</text>
  {live}
  <text x="24" y="66" font-family="{MONO}" font-size="12" fill="#7dd3fc">{meta}</text>
  {desc_svg}
  <text x="24" y="{h - 22}" font-family="{MONO}" font-size="12" fill="#8ea2c8">{escape(p.get("tech", ""))}</text>
</svg>
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Successfully generated project card SVG: {output_path}")
