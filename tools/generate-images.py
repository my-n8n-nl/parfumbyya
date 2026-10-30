#!/usr/bin/env python3
"""Genereert de flacon-illustraties voor de parfumbyya demo (SVG).

Elke afbeelding is een losstaand SVG-bestand in assets/img/.
Vervang ze later gerust door echte productfoto's (zelfde bestandsnaam).
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- producten
PRODUCTS = [
    dict(slug="noir-ambre",      bg=("#F2EBE1", "#E4D9C9"), liquid=("#8A4A1B", "#3A1B08"), cap="dark",   shape="B", label="#2A1A10", name="NOIR AMBRÉ",     sub="EXTRAIT DE PARFUM"),
    dict(slug="fleur-de-sel",    bg=("#E9EFED", "#D6E0DC"), liquid=("#D7E7E1", "#9FBDB4"), cap="silver", shape="C", label="#2B3532", name="FLEUR DE SEL",   sub="EAU DE PARFUM"),
    dict(slug="oud-royal",       bg=("#F0E7DB", "#DFD2C1"), liquid=("#5A2C13", "#1F0E05"), cap="gold",   shape="A", label="#2A1A10", name="OUD ROYAL",      sub="EXTRAIT DE PARFUM"),
    dict(slug="vanille-blanche", bg=("#F7F0E5", "#EADDC8"), liquid=("#F6E8CB", "#DCC098"), cap="cream",  shape="B", label="#3A3128", name="VANILLE BLANCHE",sub="EAU DE PARFUM"),
    dict(slug="citrus-no-7",     bg=("#F4F5E7", "#E2E5CD"), liquid=("#F1EDA9", "#C7C266"), cap="dark",   shape="C", label="#33351F", name="CITRUS Nº 7",    sub="EAU DE COLOGNE"),
    dict(slug="rose-sombre",     bg=("#F6E8E7", "#E7D2D1"), liquid=("#BE6469", "#6E2C33"), cap="gold",   shape="B", label="#3A1F22", name="ROSE SOMBRE",    sub="EAU DE PARFUM"),
    dict(slug="bois-de-nuit",    bg=("#E9EBED", "#D5D9DC"), liquid=("#443026", "#150C07"), cap="dark",   shape="A", label="#241A14", name="BOIS DE NUIT",   sub="EXTRAIT DE PARFUM"),
    dict(slug="musc-intime",     bg=("#F3ECF0", "#E1D4DC"), liquid=("#EDDFE9", "#C3A9BE"), cap="silver", shape="C", label="#2F2430", name="MUSC INTIME",    sub="EAU DE PARFUM"),
]

CAPS = {
    "dark":   ("#454545", "#151515", "#0A0A0A"),
    "gold":   ("#E0C68F", "#A2834B", "#6E5527"),
    "silver": ("#F2F2EE", "#C3C6C5", "#8C9091"),
    "cream":  ("#FAF6EE", "#DCD4C4", "#B9AF9C"),
}

BODY = {
    "A": dict(w=340, r=8,  shoulder="straight"),
    "B": dict(w=350, r=38, shoulder="round"),
    "C": dict(w=268, r=30, shoulder="tall"),
}

BODY_TOP, BODY_BOTTOM = 596, 986


def body_path(shape, top=BODY_TOP, bottom=BODY_BOTTOM):
    g = BODY[shape]
    w, r = g["w"], g["r"]
    x0, x1 = 500 - w / 2, 500 + w / 2
    if g["shoulder"] == "straight":
        return (f"M{x0},{top+r} Q{x0},{top} {x0+r},{top} L{x1-r},{top} "
                f"Q{x1},{top} {x1},{top+r} L{x1},{bottom-r} Q{x1},{bottom} {x1-r},{bottom} "
                f"L{x0+r},{bottom} Q{x0},{bottom} {x0},{bottom-r} Z")
    if g["shoulder"] == "round":
        return (f"M{x0},{top+96} C{x0},{top+22} {x0+58},{top} {500},{top} "
                f"C{x1-58},{top} {x1},{top+22} {x1},{top+96} L{x1},{bottom-r} "
                f"Q{x1},{bottom} {x1-r},{bottom} L{x0+r},{bottom} Q{x0},{bottom} {x0},{bottom-r} Z")
    return (f"M{x0},{top+66} C{x0},{top+16} {x0+44},{top} {500},{top} "
            f"C{x1-44},{top} {x1},{top+16} {x1},{top+66} L{x1},{bottom-r} "
            f"Q{x1},{bottom} {x1-r},{bottom} L{x0+r},{bottom} Q{x0},{bottom} {x0},{bottom-r} Z")


def bottle(p, x=500, scale=1.0, bottom=1160, dark=False, shadow=True):
    """Losse flacon, gecentreerd op x, onderkant op `bottom`."""
    g = BODY[p["shape"]]
    w = g["w"]
    cap_w = 148 if p["shape"] != "C" else 128
    cap_h = 150
    cap_y = 300
    c1, c2, c3 = CAPS[p["cap"]]
    label_fill = "#F6F1E9" if dark else p["label"]
    uid = p["slug"] + ("-d" if dark else "")
    y = bottom - BODY_BOTTOM * scale
    liquid_top = BODY_BOTTOM - 292
    path = body_path(p["shape"])

    return f"""
  <g transform="translate({x},{y}) scale({scale}) translate(-500,0)">
    <defs>
      <linearGradient id="gv-{uid}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#ffffff" stop-opacity=".14"/>
        <stop offset=".35" stop-color="#ffffff" stop-opacity=".04"/>
        <stop offset=".78" stop-color="#ffffff" stop-opacity=".03"/>
        <stop offset="1" stop-color="#ffffff" stop-opacity=".12"/>
      </linearGradient>
      <linearGradient id="gh-{uid}" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#ffffff" stop-opacity=".62"/>
        <stop offset=".12" stop-color="#ffffff" stop-opacity=".10"/>
        <stop offset=".55" stop-color="#ffffff" stop-opacity="0"/>
        <stop offset=".88" stop-color="#ffffff" stop-opacity=".14"/>
        <stop offset="1" stop-color="#ffffff" stop-opacity=".48"/>
      </linearGradient>
      <linearGradient id="liq-{uid}" x1="0" y1="0" x2=".4" y2="1">
        <stop offset="0" stop-color="{p['liquid'][0]}"/>
        <stop offset=".55" stop-color="{p['liquid'][1]}"/>
        <stop offset="1" stop-color="{p['liquid'][1]}"/>
      </linearGradient>
      <linearGradient id="cap-{uid}" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="{c3}"/>
        <stop offset=".14" stop-color="{c2}"/>
        <stop offset=".40" stop-color="{c1}"/>
        <stop offset=".70" stop-color="{c2}"/>
        <stop offset="1" stop-color="{c3}"/>
      </linearGradient>
      <linearGradient id="neck-{uid}" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#ffffff" stop-opacity=".55"/>
        <stop offset=".22" stop-color="#ffffff" stop-opacity=".10"/>
        <stop offset=".8" stop-color="#ffffff" stop-opacity=".12"/>
        <stop offset="1" stop-color="#ffffff" stop-opacity=".5"/>
      </linearGradient>
      <clipPath id="clip-{uid}"><path d="{path}"/></clipPath>
      <filter id="blur-{uid}" x="-60%" y="-60%" width="220%" height="220%">
        <feGaussianBlur stdDeviation="16"/>
      </filter>
      <filter id="soft-{uid}" x="-30%" y="-30%" width="160%" height="160%">
        <feGaussianBlur stdDeviation="6"/>
      </filter>
    </defs>

    {'<ellipse cx="500" cy="1002" rx="' + str(w * 0.60) + '" ry="22" fill="#000" opacity="' + ('.55' if dark else '.20') + '" filter="url(#blur-' + uid + ')"/>' if shadow else ''}

    <!-- glaslichaam -->
    <path d="{path}" fill="#ffffff" fill-opacity="{'.05' if dark else '.16'}"/>
    <g clip-path="url(#clip-{uid})">
      <rect x="0" y="{liquid_top}" width="1000" height="{BODY_BOTTOM - liquid_top + 4}" fill="url(#liq-{uid})"/>
      <rect x="0" y="{liquid_top}" width="1000" height="3" fill="#ffffff" opacity=".5"/>
      <rect x="0" y="{liquid_top + 3}" width="1000" height="10" fill="#000" opacity=".12"/>
      <rect x="0" y="{BODY_TOP}" width="1000" height="{BODY_BOTTOM - BODY_TOP}" fill="url(#gv-{uid})"/>
      <rect x="0" y="{BODY_TOP}" width="1000" height="{BODY_BOTTOM - BODY_TOP}" fill="url(#gh-{uid})"/>
      <!-- specular highlight -->
      <rect x="{500 - w / 2 + 30}" y="{BODY_TOP + 40}" width="14" height="{BODY_BOTTOM - BODY_TOP - 110}"
            rx="7" fill="#ffffff" opacity="{'.26' if dark else '.5'}" filter="url(#soft-{uid})"/>
      <rect x="{500 + w / 2 - 40}" y="{BODY_TOP + 26}" width="6" height="{BODY_BOTTOM - BODY_TOP - 80}"
            rx="3" fill="#ffffff" opacity=".26"/>
    </g>
    <path d="{path}" fill="none" stroke="#ffffff" stroke-opacity="{'.22' if dark else '.6'}" stroke-width="2.5"/>

    <!-- hals -->
    <rect x="{500 - cap_w / 2 + 22}" y="470" width="{cap_w - 44}" height="140" rx="10"
          fill="#ffffff" fill-opacity="{'.04' if dark else '.10'}"/>
    <rect x="{500 - cap_w / 2 + 22}" y="470" width="{cap_w - 44}" height="140" rx="10" fill="url(#neck-{uid})"/>
    <rect x="{500 - cap_w / 2 + 22}" y="470" width="3" height="140" fill="#ffffff" opacity=".55"/>
    <rect x="{500 + cap_w / 2 - 25}" y="470" width="3" height="140" fill="#ffffff" opacity=".4"/>

    <!-- kraag -->
    <rect x="{500 - cap_w / 2 + 12}" y="452" width="{cap_w - 24}" height="26" rx="8" fill="url(#cap-{uid})"/>
    <rect x="{500 - cap_w / 2 + 12}" y="452" width="{cap_w - 24}" height="5" rx="2.5" fill="#ffffff" opacity=".4"/>

    <!-- dop -->
    <rect x="{500 - cap_w / 2}" y="{cap_y}" width="{cap_w}" height="{cap_h}" rx="16" fill="url(#cap-{uid})"/>
    <rect x="{500 - cap_w / 2 + 4}" y="{cap_y + 4}" width="{cap_w - 8}" height="10" rx="5" fill="#ffffff" opacity=".38"/>
    <rect x="{500 - cap_w / 2 + 14}" y="{cap_y + 26}" width="12" height="{cap_h - 52}" rx="6" fill="#ffffff" opacity=".26"/>
    <rect x="{500 - cap_w / 2}" y="{cap_y + cap_h - 12}" width="{cap_w}" height="12" rx="6" fill="#000" opacity=".18"/>

    <!-- label -->
    <text x="500" y="{BODY_TOP + 186}" text-anchor="middle" fill="{label_fill}" opacity=".9"
          font-family="Georgia, 'Times New Roman', serif" font-size="{32 if p['shape'] != 'C' else 21}"
          letter-spacing="{6 if p['shape'] != 'C' else 4}">{p['name']}</text>
    <line x1="{500 - 60}" y1="{BODY_TOP + 216}" x2="{500 + 60}" y2="{BODY_TOP + 216}"
          stroke="{label_fill}" stroke-opacity=".45" stroke-width="1.5"/>
    <text x="500" y="{BODY_TOP + 248}" text-anchor="middle" fill="{label_fill}" opacity=".6"
          font-family="Helvetica, Arial, sans-serif" font-size="{12 if p['shape'] != 'C' else 10}"
          letter-spacing="{4 if p['shape'] != 'C' else 3}">{p['sub']}</text>
  </g>"""


def frame(bg, w=1000, h=1250, vignette=True, grain=".09"):
    b1, b2 = bg
    vig = (f'<radialGradient id="vig" cx=".5" cy=".44" r=".8">'
           f'<stop offset=".4" stop-color="#000" stop-opacity="0"/>'
           f'<stop offset="1" stop-color="#000" stop-opacity=".18"/></radialGradient>')
    return f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2=".55" y2="1">
    <stop offset="0" stop-color="{b1}"/><stop offset="1" stop-color="{b2}"/>
  </linearGradient>
  {vig}
  <radialGradient id="spot" cx=".5" cy=".38" r=".5">
    <stop offset="0" stop-color="#ffffff" stop-opacity=".55"/>
    <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
  </radialGradient>
  <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/></filter>
</defs>
<rect width="{w}" height="{h}" fill="url(#bg)"/>
{'<rect width="' + str(w) + '" height="' + str(h) + '" fill="url(#spot)"/>' if vignette else ''}
{'<rect width="' + str(w) + '" height="' + str(h) + '" fill="url(#vig)"/>' if vignette else ''}
"""


def svg(w, h, inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" preserveAspectRatio="xMidYMid slice">{inner}'
            f'<rect width="{w}" height="{h}" filter="url(#grain)" opacity=".08" '
            f'style="mix-blend-mode:overlay"/></svg>')


# ------------------------------------------------------------ productkaarten
for p in PRODUCTS:
    inner = frame(p["bg"]) + bottle(p, scale=1.28, bottom=1168)
    (OUT / f"{p['slug']}.svg").write_text(svg(1000, 1250, inner), encoding="utf-8")

# ------------------------------------------------------------------- hero
hero = """<defs>
  <linearGradient id="bg" x1="0" y1="0" x2=".8" y2="1">
    <stop offset="0" stop-color="#2B241C"/><stop offset=".55" stop-color="#191512"/><stop offset="1" stop-color="#0C0A09"/>
  </linearGradient>
  <radialGradient id="beam" cx=".62" cy=".18" r=".75">
    <stop offset="0" stop-color="#EBD5B0" stop-opacity=".48"/>
    <stop offset=".4" stop-color="#8A6B44" stop-opacity=".16"/>
    <stop offset="1" stop-color="#000" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="vig2" cx=".55" cy=".45" r=".8">
    <stop offset=".35" stop-color="#000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity=".6"/>
  </radialGradient>
  <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#000" stop-opacity="0"/>
    <stop offset=".5" stop-color="#000" stop-opacity=".45"/>
    <stop offset="1" stop-color="#000" stop-opacity=".75"/>
  </linearGradient>
  <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/></filter>
</defs>
<rect width="1600" height="1000" fill="url(#bg)"/>
<rect width="1600" height="1000" fill="url(#beam)"/>
"""
hero += '<rect y="740" width="1600" height="260" fill="url(#floor)"/>'
hero += bottle(PRODUCTS[7], x=1470, scale=0.62, bottom=880, dark=True)
hero += bottle(PRODUCTS[0], x=1240, scale=1.18, bottom=900, dark=True)
hero += bottle(PRODUCTS[1], x=910, scale=0.82, bottom=900, dark=True)
hero += '<rect width="1600" height="1000" fill="url(#vig2)"/>'
(OUT / "hero.svg").write_text(svg(1600, 1000, hero), encoding="utf-8")

# --------------------------------------------------------- editorial tiles
ed1 = """<defs>
  <linearGradient id="bg" x1="0" y1="0" x2=".7" y2="1">
    <stop offset="0" stop-color="#2A2119"/><stop offset="1" stop-color="#0B0908"/>
  </linearGradient>
  <radialGradient id="beam" cx=".7" cy=".25" r=".8">
    <stop offset="0" stop-color="#F0D9B2" stop-opacity=".5"/>
    <stop offset=".45" stop-color="#8A6B44" stop-opacity=".14"/>
    <stop offset="1" stop-color="#000" stop-opacity="0"/>
  </radialGradient>
  <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/></filter>
</defs>
<rect width="1200" height="900" fill="url(#bg)"/>
<rect width="1200" height="900" fill="url(#beam)"/>"""
ed1 += bottle(PRODUCTS[6], x=790, scale=0.95, bottom=742, dark=True)
(OUT / "editorial-detail.svg").write_text(svg(1200, 900, ed1), encoding="utf-8")

ed2 = frame(("#F2EBE0", "#DFD2BD"), 1200, 900)
ed2 += bottle(PRODUCTS[4], x=520, scale=0.82, bottom=790)
ed2 += bottle(PRODUCTS[5], x=800, scale=0.68, bottom=772)
(OUT / "editorial-duo.svg").write_text(svg(1200, 900, ed2), encoding="utf-8")

# ---------------------------------------------------------------- favicon
fav = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="14" fill="#12100E"/>
<rect x="24" y="14" width="16" height="9" rx="2" fill="#D9BE86"/>
<rect x="27" y="23" width="10" height="6" fill="#F3EDE4" opacity=".8"/>
<path d="M22 31h20a4 4 0 0 1 4 4v15a4 4 0 0 1-4 4H22a4 4 0 0 1-4-4V35a4 4 0 0 1 4-4z" fill="#F3EDE4"/>
<path d="M20 44h24v6a4 4 0 0 1-4 4H24a4 4 0 0 1-4-4z" fill="#C9A86A"/>
</svg>"""
(OUT / "favicon.svg").write_text(fav, encoding="utf-8")

print("kaart-images:", len(list(OUT.glob("*.svg"))))
