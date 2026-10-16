#!/usr/bin/env python3
"""Generates every brewCula SVG (mascot, app icon, README hero, sandbox diagram) in light and dark.
Mixed-media collage built from plain SVG: torn paper, halftone dots, washi tape, paper grain,
die-cut sticker edges. Run: python3 assets/generate.py  (no dependencies)."""
import random, pathlib

OUT = pathlib.Path(__file__).parent
RED, INK, GREY, BLUSH, LINE = "#d92819", "#1a1211", "#7a6a68", "#fdf3f2", "#ece4e2"
LINING = "#a51b10"

def theme(dark):
    return dict(
        bg="#171010" if dark else BLUSH, border="#2c2220" if dark else LINE,
        text=BLUSH if dark else INK, muted="#b9a9a6" if dark else GREY,
        night="#0a0606" if dark else INK, night_edge="#3d2f2c" if dark else INK,
        paper="#2a201e" if dark else "#ffffff", paper_text="#efe3e1" if dark else INK,
        sticker=BLUSH if dark else "#ffffff", steam="#b9a9a6" if dark else GREY, moon=BLUSH,
    )

def defs(t):
    return f'''<defs>
    <pattern id="dots" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="2.5" cy="2.5" r="1.15" fill="{INK}"/></pattern>
    <pattern id="moondots" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(20)"><circle cx="3.5" cy="3.5" r="2" fill="{INK}"/></pattern>
    <pattern id="tape" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#f3c9c3"/><rect width="3" height="6" fill="#f7dad6"/></pattern>
    <clipPath id="mugbody"><rect x="24" y="44" width="60" height="72" rx="13"/></clipPath>
    <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="7" stitchTiles="stitch"/><feColorMatrix type="matrix" values="0 0 0 0 .1  0 0 0 0 .07  0 0 0 0 .07  0 0 0 -1.6 1.05"/></filter>
  </defs>'''

# ---- pieces -------------------------------------------------------------------------------
WINGS = "M28 104C14 84 4 58 0 32c16 4 30 10 42 18L28 104zM80 104c14-20 24-46 28-72-16 4-30 10-42 18l14 54z"
WING_LINING = "M27 84C18 70 11 55 8 41c11 3 20 8 28 13zM81 84c9-14 16-29 19-43-11 3-20 8-28 13z"
BODY = '<rect x="24" y="44" width="60" height="72" rx="13"/>'
HANDLE = "M84 62c22 0 22 38 0 38"

def mascot(t, awake=True, steam_class=""):
    """brewCula in its own 120x132 space. Asleep: eyes shut, no steam, a small Zz."""
    s = t["sticker"]
    steam = f'''<g fill="none" stroke="{t['steam']}" stroke-width="4" stroke-linecap="round" opacity=".6" class="{steam_class}">
    <path d="M46 32c-6-6 6-10 0-18"/><path d="M62 32c-6-6 6-10 0-18"/></g>''' if awake else \
        f'<text x="62" y="30" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="15" font-weight="700" fill="{t["steam"]}" opacity=".8">z<tspan dx="1" dy="-8" font-size="11">z</tspan></text>'
    eyes = f'''<circle cx="43" cy="80" r="7" fill="#FFFFFF"/><circle cx="65" cy="80" r="7" fill="#FFFFFF"/>
  <circle cx="44.5" cy="81" r="2.8" fill="{INK}"/><circle cx="66.5" cy="81" r="2.8" fill="{INK}"/>''' if awake else \
        '<path d="M37 79q6 6 12 0M59 79q6 6 12 0" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>'
    mouth = "M44 96q10 9 20 0" if awake else "M47 97q7 5 14 0"
    fangs = "M47.5 99.4h4l-2 5.4zM56.5 99.4h4l-2 5.4z" if awake else "M49.2 99.6h3.4l-1.7 4.2zM55.4 99.6h3.4l-1.7 4.2z"
    return f'''{steam}
  <g stroke="{s}" stroke-width="7" stroke-linejoin="round" fill="{s}"><path d="{WINGS}"/>{BODY}<path d="{HANDLE}" fill="none" stroke-width="20"/></g>
  <path fill="{INK}" d="{WINGS}"/><path fill="{LINING}" d="{WING_LINING}"/>
  <path d="{HANDLE}" fill="none" stroke="{RED}" stroke-width="9" stroke-linecap="round"/>
  <g clip-path="url(#mugbody)">{BODY.replace('/>', f' fill="{RED}"/>')}
    <rect x="62" y="44" width="22" height="72" fill="url(#dots)" opacity=".16"/>
    <path fill="{INK}" d="M20 40h68v22H64l-10 11-10-11H20z"/>
    <path d="M33 52q8-5 16-4" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" opacity=".5"/></g>
  {eyes}
  <path d="{mouth}" fill="none" stroke="#FFFFFF" stroke-width="4.5" stroke-linecap="round"/>
  <path fill="#FFFFFF" d="{fangs}"/>'''

def torn(x0, y0, x1, y1, seed, amp=5, step=16, sides=True):
    r = random.Random(seed); pts = []
    x = x0
    while x < x1: pts.append((x, y0 + r.uniform(-amp, amp))); x += r.uniform(step * .5, step * 1.3)
    pts.append((x1, y0 + r.uniform(-amp, amp)))
    y = y0
    while y < y1: pts.append((x1 + (r.uniform(-amp, amp) / 3 if sides else 0), y)); y += r.uniform(step, step * 2)
    x = x1
    while x > x0: pts.append((x, y1 + r.uniform(-amp, amp))); x -= r.uniform(step * .5, step * 1.3)
    y = y1
    while y > y0: pts.append((x0 + (r.uniform(-amp, amp) / 3 if sides else 0), y)); y -= r.uniform(step, step * 2)
    return "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts) + "Z"

def tape(cx, cy, w, h, rot, seed):
    r = random.Random(seed); teeth = 4; pts = []
    for i in range(teeth + 1): pts.append((-w / 2 + (r.uniform(0, 3) if i % 2 else 0), -h / 2 + h * i / teeth))
    for i in range(teeth, -1, -1): pts.append((w / 2 - (r.uniform(0, 3) if i % 2 else 0), -h / 2 + h * i / teeth))
    d = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts) + "Z"
    return f'<path d="{d}" fill="url(#tape)" opacity=".88" transform="translate({cx} {cy}) rotate({rot})"/>'

BAT = ("M0 0C-6-8-16-10-22-6c4 2 5 6 4 9 4-3 8-2 10 1 2-3 5-3 8-1 3-2 6-2 8 1 2-3 6-4 10-1-1-3 0-7 4-9C16-10 6-8 0 0z"
       "M-2.5-2-2-6.5 0-3.6 2-6.5 2.5-2z")
def bat(x, y, s, fill, edge):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="{BAT}" fill="{edge}" stroke="{edge}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="{BAT}" fill="{fill}"/></g>')

def sparkle(x, y, s, fill, op=.85):
    return f'<path transform="translate({x} {y}) scale({s})" fill="{fill}" opacity="{op}" d="M0-6Q.8-.8 6 0 .8.8 0 6-.8.8-6 0-.8-.8 0-6z"/>'

def moon(cx, cy, r, t):
    return f'''<g><circle cx="{cx}" cy="{cy}" r="{r}" fill="{t['moon']}"/>
    <clipPath id="moonclip{cx}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
    <circle cx="{cx - r * .45}" cy="{cy - r * .2}" r="{r}" fill="url(#moondots)" opacity=".28" clip-path="url(#moonclip{cx})"/></g>'''

def glyph(x, y, s, awake, ink, paper, steam_class=""):
    """The menu bar icon, same geometry as mugIcon() in app/main.swift (y-up 18pt box)."""
    g = f'<g transform="translate({x} {y}) scale({s} -{s}) translate(0 -18)" fill="none" stroke="{ink}" stroke-linecap="round">'
    g += '<path d="M12.4 8.6C16.4 8.8 16.4 3.4 12.4 3.6" stroke-width="1.5"/>'
    if awake:
        g += f'<rect x="2.6" y="1.4" width="9.8" height="9.4" rx="2.2" fill="{ink}" stroke="none"/>'
        g += f'<ellipse cx="5.6" cy="6.65" rx="1" ry="1.25" fill="{paper}" stroke="none"/><ellipse cx="9.4" cy="6.65" rx="1" ry="1.25" fill="{paper}" stroke="none"/>'
        g += f'<g class="{steam_class}" stroke-width="1.2"><path d="M6.2 11.8C4.6 13.6 7.8 15.6 6.2 17.4"/><path d="M8.9 11.8C7.3 13.6 10.5 15.6 8.9 17.4"/></g>'
    else:
        g += '<rect x="3.35" y="2.15" width="8.3" height="7.9" rx="1.6" stroke-width="1"/>'
        g += '<path d="M4.4 6.6C5 5.6 6.2 5.6 6.8 6.6M8.2 6.6C8.8 5.6 10 5.6 10.6 6.6" stroke-width="1.2"/>'
    return g + "</g>"

MONO = "ui-monospace,SFMono-Regular,Menlo,monospace"
SANS = "ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,sans-serif"

# ---- files ---------------------------------------------------------------------------------
def write_mascot(dark):
    t = theme(dark)
    (OUT / f"mascot-{'dark' if dark else 'light'}.svg").write_text(
        f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 0 128 132" width="128" height="132" role="img" aria-label="brewCula, a red mug with a widow's peak, fangs and a Dracula collar">
  {defs(t)}
  {mascot(t)}
  <ellipse cx="54" cy="125" rx="26" ry="4.5" fill="{RED}" opacity=".2"/>
</svg>
''')

def write_icon():
    t = theme(False)
    sq = '<rect x="100" y="100" width="824" height="824" rx="185"/>'
    stars = "".join(sparkle(x, y, s, BLUSH) for x, y, s in [(232, 196, 2.2), (436, 168, 1.5), (604, 236, 1.8), (858, 420, 1.4), (178, 420, 1.3)])
    (OUT / "icon.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
  {defs(t)}
  <clipPath id="sq">{sq}</clipPath>
  <filter id="shadow" x="-10%" y="-10%" width="120%" height="125%"><feDropShadow dx="0" dy="12" stdDeviation="14" flood-color="#1a1211" flood-opacity=".3"/></filter>
  <g filter="url(#shadow)">{sq.replace('/>', f' fill="{BLUSH}"/>')}</g>
  <g clip-path="url(#sq)">
    <path d="{torn(60, 60, 964, 590, 3, amp=14, step=34, sides=False)}" fill="{INK}"/>
    {moon(760, 250, 78, t)}
    {stars}
    {bat(300, 300, 3.2, RED, BLUSH)}
    {bat(612, 386, 1.9, RED, BLUSH)}
    {tape(196, 170, 230, 54, -38, 5)}
    <g transform="translate(216 300) scale(4.95)">{mascot(dict(t, steam="#e9d6d3"))}</g>
    <ellipse cx="483" cy="914" rx="150" ry="20" fill="{RED}" opacity=".18"/>
  </g>
</svg>
''')

def write_hero(dark):
    t = theme(dark)
    stars = "".join(sparkle(x, y, s, t["moon"]) for x, y, s in [(120, 104, 1.3), (196, 160, .9), (372, 92, 1.1), (300, 182, .8), (470, 196, .9)])
    css = f'''<style>
    .awake{{opacity:1}} .asleep{{opacity:0}} .cursor{{opacity:0}}
    @media (prefers-reduced-motion: no-preference) {{
      .asleep{{animation:asleep 8s infinite}} .awake{{animation:awake 8s infinite}}
      .cursor{{animation:cursor 8s infinite ease-in-out}} .ring{{animation:ring 8s infinite ease-out;transform-origin:0 0}}
      .rise{{animation:rise 1.6s infinite ease-out}} .rise2{{animation:rise 1.6s .8s infinite ease-out}}
    }}
    @keyframes asleep{{0%,24%{{opacity:1}}26%,68%{{opacity:0}}70%,100%{{opacity:1}}}}
    @keyframes awake{{0%,24%{{opacity:0}}26%,68%{{opacity:1}}70%,100%{{opacity:0}}}}
    @keyframes cursor{{0%{{opacity:0;transform:translate(-150px,60px)}}6%{{opacity:1}}21%{{transform:translate(0,0) scale(1)}}24%{{transform:translate(0,0) scale(.82)}}27%,65%{{transform:translate(0,0) scale(1)}}68%{{transform:translate(0,0) scale(.82)}}71%{{transform:translate(0,0) scale(1)}}84%{{opacity:1}}90%,100%{{opacity:0;transform:translate(80px,70px)}}}}
    @keyframes ring{{0%,23%{{opacity:0;transform:scale(.4)}}24%{{opacity:.7;transform:scale(.4)}}32%,67%{{opacity:0;transform:scale(1.5)}}68%{{opacity:.7;transform:scale(.4)}}76%,100%{{opacity:0;transform:scale(1.5)}}}}
    @keyframes rise{{0%{{opacity:0;transform:translateY(5px)}}40%{{opacity:1}}100%{{opacity:0;transform:translateY(-7px)}}}}
  </style>'''
    gx, gy = 424, 230   # menu bar glyph centre
    cursor = (f'<g transform="translate({gx + 4} {gy + 4})"><g class="cursor"><path d="M0 0v22l6-5.5 4 9 4-1.8-4-8.8h8z" fill="{INK}" stroke="#ffffff" stroke-width="2" stroke-linejoin="round"/></g></g>')
    (OUT / f"hero-{'dark' if dark else 'light'}.svg").write_text(
        f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 380" width="1200" height="380" role="img" aria-label="A collage: a torn strip of night sky with a moon and paper bats, and a menu bar taped across it. A cursor clicks the mug icon in the menu bar. The mug fills and steams, the brewCula mascot opens its eyes, and the caption changes from 'Your Mac can sleep' to 'Your Mac stays awake, until you click again.' Sandboxed, no network, no sudo.">
  {defs(t)}
  {css}
  <rect width="1200" height="380" rx="18" fill="{t['bg']}"/>
  <rect width="1200" height="380" rx="18" filter="url(#grain)" opacity="{'.16' if dark else '.22'}"/>
  <rect x=".5" y=".5" width="1199" height="379" rx="17.5" fill="none" stroke="{t['border']}"/>
  <g transform="rotate(-1.6 300 190)">
    <path d="{torn(60, 52, 560, 300, 11, amp=6, step=15)}" fill="{t['night']}" stroke="{t['night_edge']}" stroke-width="1.5"/>
    {moon(478, 112, 36, t)}
    {stars}
    {bat(250, 118, 1.15, RED, t['moon'])}
    {bat(330, 78, .7, RED, t['moon'])}
  </g>
  <g transform="rotate(.8 330 230)">
    <rect x="86" y="208" width="480" height="44" rx="3" fill="{t['paper']}"/>
    <text x="110" y="236" font-family="{SANS}" font-size="15" fill="{t['paper_text']}"><tspan font-weight="700">brewCula</tspan><tspan dx="22">File</tspan><tspan dx="20">Edit</tspan><tspan dx="20">View</tspan></text>
    <g class="asleep">{glyph(gx - 11.7, gy - 11.7, 1.3, False, t['paper_text'], t['paper'])}</g>
    <g class="awake">{glyph(gx - 11.7, gy - 11.7, 1.3, True, t['paper_text'], t['paper'])}</g>
    <circle class="ring" cx="0" cy="0" r="22" fill="none" stroke="{RED}" stroke-width="2.5" transform="translate({gx} {gy})" opacity="0"/>
    <rect x="452" y="224" width="22" height="11" rx="3" fill="none" stroke="{t['paper_text']}" stroke-width="1.6"/><rect x="455" y="227" width="12" height="5" rx="1" fill="{t['paper_text']}"/>
    <text x="486" y="236" font-family="{MONO}" font-size="13" fill="{t['paper_text']}">2:47 AM</text>
    {tape(92, 212, 64, 22, -24, 2)}{tape(560, 246, 64, 22, -20, 9)}
  </g>
  {cursor}
  <text x="98" y="334" font-family="{MONO}" font-size="14" fill="{RED}" letter-spacing="2.5">CLICK THE MUG</text>
  <path d="M262 326c40-6 100-20 152-72" fill="none" stroke="{RED}" stroke-width="2" stroke-linecap="round" stroke-dasharray="5 6"/>
  <path d="M404 254l10-2-1 10" fill="none" stroke="{RED}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <g transform="translate(610 66) scale(1.85)">
    <g class="asleep">{mascot(t, awake=False)}</g>
    <g class="awake">{mascot(t, awake=True, steam_class="rise")}</g>
  </g>
  <text x="862" y="150" font-family="{MONO}" font-size="15" fill="{t['muted']}" letter-spacing="2.5">YOUR MAC</text>
  <g class="asleep">
    <text x="860" y="212" font-family="{SANS}" font-size="54" font-weight="700" fill="{t['text']}" letter-spacing="-1.6">can sleep</text>
    <text x="862" y="250" font-family="{SANS}" font-size="18" fill="{t['muted']}">Click the mug to keep it up.</text>
  </g>
  <g class="awake">
    <text x="860" y="212" font-family="{SANS}" font-size="54" font-weight="700" fill="{RED}" letter-spacing="-1.6">stays awake</text>
    <text x="862" y="250" font-family="{SANS}" font-size="18" fill="{t['muted']}">Until you click again.</text>
  </g>
  <text x="862" y="318" font-family="{MONO}" font-size="13" fill="{t['muted']}" letter-spacing="1.5">SANDBOXED · NO NETWORK · NO SUDO</text>
</svg>
''')

def write_sandbox(dark):
    t = theme(dark)
    ok, no = RED, t["muted"]
    rows = [("keep the display and the Mac awake", True), ("keep disks from spinning down", True),
            ("open itself at login, if you leave that on", True),
            ("open a network connection", False), ("read or write your files", False), ("install a background daemon", False),
            ("ask for your password", False)]
    items = ""
    for i, (label, allowed) in enumerate(rows):
        y = 96 + i * 34
        mark = (f'<path d="M0 0l6 6 12-13" fill="none" stroke="{ok}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(0 -4)"/>'
                if allowed else f'<path d="M0-9l14 14M14-9 0 5" fill="none" stroke="{no}" stroke-width="2.6" stroke-linecap="round"/>')
        items += (f'<g transform="translate(560 {y})">{mark}<text x="34" y="2" font-family="{SANS}" font-size="19" '
                  f'fill="{t["text"] if allowed else t["muted"]}"{"" if allowed else " text-decoration=\"line-through\""}>{label}</text></g>')
    (OUT / f"sandbox-{'dark' if dark else 'light'}.svg").write_text(
        f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 380" width="1200" height="380" role="img" aria-label="brewCula sits inside the macOS App Sandbox with no permissions granted. It can keep the display and the Mac awake, keep disks from spinning down, and open itself at login if you leave that on. It cannot open a network connection, read or write your files, install a background daemon, or ask for your password.">
  {defs(t)}
  <rect width="1200" height="380" rx="18" fill="{t['bg']}"/>
  <rect width="1200" height="380" rx="18" filter="url(#grain)" opacity="{'.16' if dark else '.22'}"/>
  <rect x=".5" y=".5" width="1199" height="379" rx="17.5" fill="none" stroke="{t['border']}"/>
  <rect x="70" y="56" width="400" height="270" rx="14" fill="none" stroke="{t['muted']}" stroke-width="2" stroke-dasharray="8 7"/>
  <text x="94" y="92" font-family="{MONO}" font-size="14" fill="{t['muted']}" letter-spacing="2.5">APP SANDBOX</text>
  <text x="94" y="114" font-family="{MONO}" font-size="12" fill="{t['muted']}" letter-spacing="1.5">0 PERMISSIONS GRANTED</text>
  <g transform="translate(190 120) scale(1.45)">{mascot(t)}</g>
  {tape(92, 60, 70, 22, -28, 4)}{tape(452, 320, 70, 22, -24, 6)}
  <text x="560" y="62" font-family="{MONO}" font-size="14" fill="{t['muted']}" letter-spacing="2.5">IT CAN</text>
  {items}
</svg>
''')

def write_site_art():
    """Landing-page art in site/src/art. It always sits on night paper, so one variant each."""
    t = theme(True); out = OUT.parent / "site" / "src" / "art"; out.mkdir(parents=True, exist_ok=True)
    rise = ("<style>@media (prefers-reduced-motion: no-preference){.rise path{animation:rise 1.6s infinite ease-out}"
            ".rise path+path{animation-delay:.8s}}@keyframes rise{0%{opacity:0;transform:translateY(5px)}40%{opacity:1}"
            "100%{opacity:0;transform:translateY(-7px)}}</style>")
    for awake in (True, False):
        (out / f"mascot-{'awake' if awake else 'asleep'}.svg").write_text(
            f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 0 128 132" width="128" height="132">
  {defs(t)}{rise if awake else ""}
  {mascot(t, awake=awake, steam_class="rise")}
</svg>
''')
    stars = "".join(sparkle(x, y, s, t["moon"]) for x, y, s in [(70, 96, 1.4), (132, 300, .9), (420, 70, 1.1), (452, 318, 1.2), (96, 420, .8), (404, 440, 1)])
    (out / "stage.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 520" width="520" height="520">
  {defs(t)}
  <g transform="rotate(-2.4 260 260)">
    <path d="{torn(30, 40, 490, 490, 21, amp=7, step=18)}" fill="{INK}" stroke="#4a3936" stroke-width="2"/>
    <rect x="30" y="40" width="460" height="450" filter="url(#grain)" opacity=".2"/>
    <rect x="300" y="360" width="190" height="130" fill="url(#dots)" opacity=".9"/>
    {moon(392, 132, 44, t)}
    {stars}
    {bat(118, 168, 1.3, RED, t["moon"])}
    {bat(372, 400, .8, RED, t["moon"])}
  </g>
  {tape(72, 52, 96, 28, -32, 3)}{tape(460, 470, 96, 28, -28, 8)}
</svg>
''')

if __name__ == "__main__":
    for dark in (False, True):
        write_mascot(dark); write_hero(dark); write_sandbox(dark)
    write_icon(); write_site_art()
    print("wrote", sorted(p.name for p in OUT.glob("*.svg")))
