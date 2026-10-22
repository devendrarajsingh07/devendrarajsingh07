"""SVG assets for the banner-showcase profile layout.

Everything here is generated from config.yml so the profile stays editable
from one place. GitHub serves README images through a sandboxed proxy, so
each SVG is self-contained: no external fonts, scripts or linked images
(the banner photo is embedded as a data URI).
"""

import base64
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


def _darken(hex_color, amount=0.55):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(int(v * (1 - amount)) for v in (r, g, b))


def generate_skills_svg(output_path, config, mode="dark"):
    """An animated cloud of skill chips; each chip floats on its own rhythm."""
    skills = config.get("skills", [])
    w, h = 460, 400
    cols_per_row = [3, 4, 3, 4, 3]  # a loose hexagonal cloud
    rows = []
    i = 0
    for n in cols_per_row:
        rows.append(skills[i:i + n])
        i += n
    rows = [r for r in rows if r]

    chips = []
    row_h = h / (len(rows) + 1)
    char_w = 9.6
    for r, row in enumerate(rows):
        y = row_h * (r + 1)
        widths = [len(s["name"]) * char_w + 30 + (8 if s.get("big") else 0) for s in row]
        gap = 14
        total = sum(widths) + gap * (len(row) - 1)
        x = (w - total) / 2
        for j, s in enumerate(row):
            k = r * 4 + j
            big = s.get("big", False)
            cw = widths[j]
            ch = 40 if big else 34
            fs = 18 if big else 15
            color = s.get("color", "#38bdf8")
            fill_op = "0.16" if mode == "dark" else "0.14"
            txt = color if mode == "dark" else _darken(color)
            dur = 5 + (k % 4) * 0.8
            delay = -(k * 0.7) % dur
            chips.append(
                f'<g class="f" style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s">'
                f'<rect x="{x:.1f}" y="{y - ch / 2:.1f}" width="{cw:.1f}" height="{ch}" rx="12" '
                f'fill="{color}" fill-opacity="{fill_op}" stroke="{color}" stroke-opacity="0.45"/>'
                f'<text x="{x + cw / 2:.1f}" y="{y + fs * 0.35:.1f}" text-anchor="middle" font-family="{FONT}" '
                f'font-size="{fs}" font-weight="700" fill="{txt}">{escape(s["name"])}</text></g>'
            )
            x += cw + gap

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Skills: {escape(", ".join(s["name"] for s in skills))}">
  <style>
    .f {{ animation-name: float; animation-timing-function: ease-in-out; animation-iteration-count: infinite; }}
    @keyframes float {{ 0%,100% {{ transform: translateY(0); opacity: 0.85; }} 50% {{ transform: translateY(-7px); opacity: 1; }} }}
  </style>
  {"".join(chips)}
</svg>
'''
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Successfully generated skills SVG ({mode}): {output_path}")


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
