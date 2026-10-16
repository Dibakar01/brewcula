#!/usr/bin/env python3
"""Generates every brewCula SVG (mascot, app icon, README hero, sandbox diagram, site art), light and dark.
Analogue riso print built from plain SVG: two inks (black and red) on newsprint, the red plate printed
slightly out of register, halftone dots, rough ink edges, paper grain. Run: python3 assets/generate.py"""
import random, pathlib

OUT = pathlib.Path(__file__).parent
SANS = "Helvetica Neue,Helvetica,Arial,sans-serif"

def theme(dark):
    # dark mode is the same print reversed: light ink on black stock
    return dict(dark=dark,
        paper="#141312" if dark else "#ebe9e4", ink="#ebe9e4" if dark else "#151312",
        red="#ea4630" if dark else "#e0301c", muted="#9b9893" if dark else "#6b6862",
        border="#2a2826" if dark else "#d6d3cc", blend="screen" if dark else "multiply")

def defs(t):
    c = 1 if t["dark"] else 0
    return f'''<defs>
  <filter id="rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".045" numOctaves="3" seed="9"/><feDisplacementMap in="SourceGraphic" scale="9"/></filter>
  <filter id="inky" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".05" numOctaves="3" seed="3" result="w"/><feDisplacementMap in="SourceGraphic" in2="w" scale="8" result="d"/><feTurbulence type="fractalNoise" baseFrequency="1.4" seed="5"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -16 14.6"/><feComposite in="d" operator="in"/></filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="2" seed="7" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 {c}  0 0 0 0 {c}  0 0 0 0 {c}  0 0 0 .32 -.08"/></filter>
  <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(22)"><circle cx="8" cy="8" r="4.6" fill="{t['red']}"/></pattern>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="1"><stop offset=".35" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <mask id="fademask" maskContentUnits="objectBoundingBox"><rect width="1" height="1" fill="url(#fade)"/></mask>
</defs>'''

STEAM_CSS = ("<style>@media (prefers-reduced-motion: no-preference){.rise{animation:rise 1.8s infinite ease-out}}"
             "@keyframes rise{0%{opacity:0;transform:translateY(24px)}40%{opacity:1}100%{opacity:0;transform:translateY(-30px)}}</style>")

def grain(x, y, w, h, rx=0, op=.8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" filter="url(#grain)" opacity="{op}"/>'

# ---- the mug, in a 1024 space --------------------------------------------------------------------
MUG = "M318 372h336l-18 330c-2 40-30 68-70 68H406c-40 0-68-28-70-68z"
HANDLE = "M648 462c112-6 124 196 6 214"
FANGS = "M404 370l24 58 24-58zM508 370l24 58 24-58z"
STEAM = "M488 324c-38-34-38-62-6-92s28-66-4-96"
MUG_BOX = (290, 110, 520, 690)   # x, y, w, h of the mug with steam, handle and the red offset

def mug(t, awake=True, steam_class=""):
    """Awake prints both plates: black ink plus the red plate out of register, and steam.
    Asleep prints the black plate only, with a Zz."""
    red = (f'''<g style="mix-blend-mode:{t['blend']}" filter="url(#rough)">
    <g transform="translate(30 24)"><path d="{MUG}" fill="url(#dots)"/><path d="{HANDLE}" fill="none" stroke="url(#dots)" stroke-width="58"/></g>
    <path d="{MUG}" fill="{t['red']}" mask="url(#fademask)" opacity=".9" transform="translate(12 10)"/>
    <g class="{steam_class}"><path d="{STEAM}" fill="none" stroke="{t['red']}" stroke-width="24" stroke-linecap="round" transform="translate(6 4)"/></g>
  </g>''' if awake else
           f'<text x="600" y="300" font-family="{SANS}" font-size="96" font-weight="700" fill="{t["ink"]}">z<tspan dx="8" dy="-56" font-size="66">z</tspan></text>')
    ink = (f'<g filter="url(#inky)" style="mix-blend-mode:{"normal" if t["dark"] else "multiply"}">'
           f'<path d="{MUG}" fill="{t["ink"]}"/><path d="{HANDLE}" fill="none" stroke="{t["ink"]}" stroke-width="58"/></g>')
    return f'{red}\n  {ink}\n  <path d="{FANGS}" fill="{t["paper"]}" filter="url(#rough)"/>'

def place_mug(x, y, h, t, awake=True, steam_class=""):
    bx, by, bw, bh = MUG_BOX; s = h / bh
    return f'<g transform="translate({x} {y}) scale({s:.4f}) translate({-bx} {-by})">{mug(t, awake, steam_class)}</g>'

# ---- the menu bar glyph: same geometry as mugIcon() in app/main.swift (y-up 18pt box) -------------
G_BODY = "M2.4 11L12.4 11L11.9 3.4C11.85 2.2 11.1 1.4 9.9 1.4L4.9 1.4C3.7 1.4 2.95 2.2 2.9 3.4Z"
G_FANGS = "M4.7 11.1L5.6 9.1L6.5 11.1ZM8.3 11.1L9.2 9.1L10.1 11.1Z"
G_HANDLE = "M12.2 9C16.2 9.3 16 3.4 12 3.8"
G_STEAM = "M7.4 12.3C5.9 13.2 8.9 14.1 7.4 15C5.9 15.9 8.9 16.8 7.4 17.6"

def glyph(x, y, s, awake, ink, paper, steam_class=""):
    g = f'<g transform="translate({x} {y}) scale({s} -{s}) translate(0 -18)" stroke="{ink}" stroke-linecap="round" stroke-linejoin="round">'
    g += f'<path d="{G_HANDLE}" fill="none" stroke-width="1.5"/>'
    if awake:
        g += f'<path d="{G_BODY}" fill="{ink}" stroke="none"/><path d="{G_FANGS}" fill="{paper}" stroke="none"/>'
        g += f'<g class="{steam_class}"><path d="{G_STEAM}" fill="none" stroke-width="1.3"/></g>'
    else:
        g += f'<path d="{G_BODY}" fill="none" stroke-width="1.1"/><path d="{G_FANGS}" fill="{ink}" stroke="none"/>'
    return g + "</g>"

# ---- print furniture -----------------------------------------------------------------------------
def torn(x0, y0, x1, y1, seed, amp=5, step=16):
    r = random.Random(seed); pts = []
    x = x0
    while x < x1: pts.append((x, y0 + r.uniform(-amp, amp))); x += r.uniform(step * .5, step * 1.3)
    pts.append((x1, y0 + r.uniform(-amp, amp)))
    y = y0
    while y < y1: pts.append((x1 + r.uniform(-amp, amp) / 3, y)); y += r.uniform(step, step * 2)
    x = x1
    while x > x0: pts.append((x, y1 + r.uniform(-amp, amp))); x -= r.uniform(step * .5, step * 1.3)
    y = y1
    while y > y0: pts.append((x0 + r.uniform(-amp, amp) / 3, y)); y -= r.uniform(step, step * 2)
    return "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts) + "Z"

def reg(x, y, c, r=9):
    """A printer's registration mark."""
    return (f'<g fill="none" stroke="{c}" stroke-width="1.4"><circle cx="{x}" cy="{y}" r="{r * .55}"/>'
            f'<path d="M{x - r} {y}h{2 * r}M{x} {y - r}v{2 * r}"/></g>')

def colour_bar(x, y, t, s=14):
    """The ink swatches printed at the edge of a proof."""
    return (f'<g transform="translate({x} {y})"><rect width="{s}" height="{s}" fill="{t["ink"]}"/>'
            f'<rect x="{s + 4}" width="{s}" height="{s}" fill="{t["red"]}"/>'
            f'<rect x="{2 * s + 8}" width="{s}" height="{s}" fill="url(#dots)"/>'
            f'<rect x="{3 * s + 12.7}" y=".7" width="{s - 1.4}" height="{s - 1.4}" fill="none" stroke="{t["muted"]}" stroke-width="1.4"/></g>')

def frame(t, w, h):
    return (f'<rect width="{w}" height="{h}" rx="18" fill="{t["paper"]}"/>{grain(0, 0, w, h, 18, .7)}'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="17.5" fill="none" stroke="{t["border"]}"/>')

# ---- files ---------------------------------------------------------------------------------------
def write_mascot(dark):
    t = theme(dark); bx, by, bw, bh = MUG_BOX
    (OUT / f"mascot-{'dark' if dark else 'light'}.svg").write_text(
        f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{bx} {by} {bw} {bh}" width="104" height="138" role="img" aria-label="brewCula: a steaming mug with two fangs, printed in black and red ink">
{defs(t)}
  {mug(t)}
</svg>
''')

def write_icon():
    t = theme(False)
    sq = '<rect x="100" y="100" width="824" height="824" rx="185"/>'
    (OUT / "icon.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
{defs(t)}
  <clipPath id="sq">{sq}</clipPath>
  <filter id="shadow" x="-10%" y="-10%" width="120%" height="125%"><feDropShadow dx="0" dy="12" stdDeviation="14" flood-color="#151312" flood-opacity=".28"/></filter>
  <g filter="url(#shadow)">{sq.replace('/>', f' fill="{t["paper"]}"/>')}</g>
  <g clip-path="url(#sq)">
    <g transform="translate(512 528) scale(.92) translate(-504 -470)">{mug(t)}</g>
    {grain(100, 100, 824, 824, op=.8)}
  </g>
  <rect x="101" y="101" width="822" height="822" rx="184" fill="none" stroke="#000" stroke-opacity=".10" stroke-width="2"/>
</svg>
''')

def write_hero(dark):
    t = theme(dark)
    css = '''<style>
    .awake{opacity:1} .asleep{opacity:0} .cursor{opacity:0}
    @media (prefers-reduced-motion: no-preference) {
      .asleep{animation:asleep 8s infinite} .awake{animation:awake 8s infinite}
      .cursor{animation:cursor 8s infinite ease-in-out} .ring{animation:ring 8s infinite ease-out;transform-box:fill-box;transform-origin:center}
      .rise{animation:rise 1.8s infinite ease-out}
    }
    @keyframes asleep{0%,24%{opacity:1}26%,68%{opacity:0}70%,100%{opacity:1}}
    @keyframes awake{0%,24%{opacity:0}26%,68%{opacity:1}70%,100%{opacity:0}}
    @keyframes cursor{0%{opacity:0;transform:translate(-150px,60px)}6%{opacity:1}21%{transform:translate(0,0) scale(1)}24%{transform:translate(0,0) scale(.82)}27%,65%{transform:translate(0,0) scale(1)}68%{transform:translate(0,0) scale(.82)}71%{transform:translate(0,0) scale(1)}84%{opacity:1}90%,100%{opacity:0;transform:translate(80px,70px)}}
    @keyframes ring{0%,23%{opacity:0;transform:scale(.4)}24%{opacity:.7;transform:scale(.4)}32%,67%{opacity:0;transform:scale(1.5)}68%{opacity:.7;transform:scale(.4)}76%,100%{opacity:0;transform:scale(1.5)}}
    @keyframes rise{0%{opacity:0;transform:translateY(24px)}40%{opacity:1}100%{opacity:0;transform:translateY(-30px)}}
  </style>'''
    gx, gy = 424, 218   # menu bar glyph centre
    bar, on_bar = t["ink"], t["paper"]
    cursor = (f'<g transform="translate({gx + 4} {gy + 4})"><g class="cursor"><path d="M0 0v22l6-5.5 4 9 4-1.8-4-8.8h8z" '
              f'fill="{t["ink"]}" stroke="{t["paper"]}" stroke-width="2" stroke-linejoin="round"/></g></g>')
    (OUT / f"hero-{'dark' if dark else 'light'}.svg").write_text(
        f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 380" width="1200" height="380" role="img" aria-label="A two-colour riso print. A cursor clicks the mug icon in a printed menu bar. The red ink plate prints, steam rises from the brewCula mug, and the caption changes from 'Your Mac can sleep' to 'Your Mac stays awake, until you click again.' Sandboxed, no network, no sudo.">
{defs(t)}
  {css}
  {frame(t, 1200, 380)}
  {reg(40, 40, t["muted"])}{reg(1160, 340, t["muted"])}
  {colour_bar(92, 92, t)}
  <text x="166" y="104" font-family="{SANS}" font-size="11" font-weight="700" fill="{t['muted']}" letter-spacing="1.8">PROOF 02 · 2 INKS</text>
  <rect x="98" y="203" width="480" height="42" fill="url(#dots)" style="mix-blend-mode:{t['blend']}" filter="url(#rough)"/>
  <rect x="88" y="196" width="480" height="42" fill="{bar}" filter="url(#inky)"/>
  <text x="112" y="223" font-family="{SANS}" font-size="15" fill="{on_bar}"><tspan font-weight="700">brewCula</tspan><tspan dx="22">File</tspan><tspan dx="20">Edit</tspan><tspan dx="20">View</tspan></text>
  <g class="asleep">{glyph(gx - 11.7, gy - 11.7, 1.3, False, on_bar, bar)}</g>
  <g class="awake">{glyph(gx - 11.7, gy - 11.7, 1.3, True, on_bar, bar)}</g>
  <circle class="ring" cx="{gx}" cy="{gy}" r="22" fill="none" stroke="{t['red']}" stroke-width="2.5" opacity="0"/>
  <rect x="452" y="211" width="22" height="11" rx="3" fill="none" stroke="{on_bar}" stroke-width="1.6"/><rect x="455" y="214" width="12" height="5" rx="1" fill="{on_bar}"/>
  <text x="486" y="222" font-family="{SANS}" font-size="14" fill="{on_bar}">2:47 AM</text>
  {cursor}
  <text x="92" y="318" font-family="{SANS}" font-size="13" font-weight="700" fill="{t['red']}" letter-spacing="2.5">CLICK THE MUG</text>
  <path d="M226 312c60-6 130-24 182-62" fill="none" stroke="{t['red']}" stroke-width="2" stroke-linecap="round" stroke-dasharray="5 6"/>
  <path d="M396 250l13-1-3 12" fill="none" stroke="{t['red']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <g class="asleep">{place_mug(610, 42, 300, t, awake=False)}</g>
  <g class="awake">{place_mug(610, 42, 300, t, awake=True, steam_class="rise")}</g>
  <text x="862" y="148" font-family="{SANS}" font-size="13" font-weight="700" fill="{t['muted']}" letter-spacing="2.5">YOUR MAC</text>
  <g class="asleep">
    <text x="858" y="208" font-family="{SANS}" font-size="54" font-weight="700" fill="{t['ink']}" letter-spacing="-2">can sleep</text>
    <text x="862" y="244" font-family="{SANS}" font-size="18" fill="{t['muted']}">Click the mug to keep it up.</text>
  </g>
  <g class="awake">
    <text x="858" y="208" font-family="{SANS}" font-size="54" font-weight="700" fill="{t['red']}" letter-spacing="-2">stays awake</text>
    <text x="862" y="244" font-family="{SANS}" font-size="18" fill="{t['muted']}">Until you click again.</text>
  </g>
  <text x="862" y="318" font-family="{SANS}" font-size="12" font-weight="700" fill="{t['muted']}" letter-spacing="2">SANDBOXED · NO NETWORK · NO SUDO</text>
</svg>
''')

def write_sandbox(dark):
    t = theme(dark)
    rows = [("keep the display and the Mac awake", True), ("keep disks from spinning down", True),
            ("open itself at login, if you leave that on", True),
            ("open a network connection", False), ("read or write your files", False),
            ("install a background daemon", False), ("ask for your password", False)]
    items = ""
    for i, (label, allowed) in enumerate(rows):
        y = 100 + i * 34
        mark = (f'<path d="M0 0l6 6 12-13" fill="none" stroke="{t["red"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" transform="translate(0 -4)"/>'
                if allowed else f'<path d="M1-10l12 12M13-10 1 2" fill="none" stroke="{t["muted"]}" stroke-width="2.4" stroke-linecap="round"/>')
        strike = "" if allowed else ' text-decoration="line-through"'
        items += (f'<g transform="translate(560 {y})">{mark}<text x="34" y="2" font-family="{SANS}" font-size="19" '
                  f'fill="{t["ink"] if allowed else t["muted"]}"{strike}>{label}</text></g>')
    (OUT / f"sandbox-{'dark' if dark else 'light'}.svg").write_text(
        f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 380" width="1200" height="380" role="img" aria-label="brewCula sits inside the macOS App Sandbox with no permissions granted. It can keep the display and the Mac awake, keep disks from spinning down, and open itself at login if you leave that on. It cannot open a network connection, read or write your files, install a background daemon, or ask for your password.">
{defs(t)}
  {frame(t, 1200, 380)}
  <rect x="70" y="52" width="400" height="276" rx="4" fill="none" stroke="{t['muted']}" stroke-width="2" stroke-dasharray="8 7"/>
  {reg(70, 52, t["muted"])}{reg(470, 328, t["muted"])}
  <text x="94" y="86" font-family="{SANS}" font-size="13" font-weight="700" fill="{t['muted']}" letter-spacing="2.5">APP SANDBOX</text>
  <text x="94" y="106" font-family="{SANS}" font-size="12" fill="{t['muted']}" letter-spacing="1.5">0 PERMISSIONS GRANTED</text>
  {place_mug(200, 118, 196, t)}
  <text x="560" y="66" font-family="{SANS}" font-size="13" font-weight="700" fill="{t['muted']}" letter-spacing="2.5">IT CAN</text>
  {items}
</svg>
''')

def write_site_art():
    """Landing-page art in site/src/art. The stage is a printed proof sheet, so it is always light stock."""
    t = theme(False); out = OUT.parent / "site" / "src" / "art"; out.mkdir(parents=True, exist_ok=True)
    bx, by, bw, bh = MUG_BOX
    for awake in (True, False):
        (out / f"mascot-{'awake' if awake else 'asleep'}.svg").write_text(
            f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{bx} {by} {bw} {bh}" width="104" height="138">
{defs(t)}{STEAM_CSS if awake else ""}
  {mug(t, awake=awake, steam_class="rise")}
</svg>
''')
    (out / "stage.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 520" width="520" height="520">
{defs(t)}
  <g transform="rotate(-2 260 260)">
    <path d="{torn(30, 36, 490, 492, 21)}" fill="{t['paper']}" stroke="{t['border']}" stroke-width="1.5"/>
    <circle cx="272" cy="252" r="150" fill="url(#dots)" filter="url(#rough)" style="mix-blend-mode:multiply"/>
    <circle cx="256" cy="240" r="150" fill="{t['red']}" mask="url(#fademask)" opacity=".85" filter="url(#rough)" style="mix-blend-mode:multiply"/>
    {reg(62, 68, t['muted'])}{reg(458, 68, t['muted'])}{reg(62, 460, t['muted'])}{reg(458, 460, t['muted'])}
    {grain(30, 36, 460, 456, op=.7)}
  </g>
</svg>
''')

if __name__ == "__main__":
    for dark in (False, True):
        write_mascot(dark); write_hero(dark); write_sandbox(dark)
    write_icon(); write_site_art()
    print("wrote", sorted(p.name for p in OUT.glob("*.svg")))
