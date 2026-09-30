"""lib_b: shared SVG helpers + motifs for diwali, karva-chauth and shraddhanjali cards.

Every motif returns an SVG fragment (string). Gradients/filters that a motif
needs are emitted inline in its own <defs> with unique ids, so fragments can
be combined freely.
"""
import math, random

W, H = 1080, 1350
_n = [0]


def uid(p="u"):
    _n[0] += 1
    return "%s%d" % (p, _n[0])


def n(v):
    s = "%.1f" % v
    return s[:-2] if s.endswith(".0") else s


def pts(seq):
    return " ".join("%s,%s" % (n(x), n(y)) for x, y in seq)


# ---------------------------------------------------------------- basics
def lg(stops, x1=0, y1=0, x2=0, y2=1, units="objectBoundingBox", gid=None):
    gid = gid or uid("lg")
    s = "".join('<stop offset="%s" stop-color="%s"%s/>' % (o, c, (' stop-opacity="%s"' % a) if a is not None else "")
                for o, c, a in [(t + (None,))[:3] for t in stops])
    return gid, '<linearGradient id="%s" x1="%s" y1="%s" x2="%s" y2="%s" gradientUnits="%s">%s</linearGradient>' % (
        gid, x1, y1, x2, y2, units, s)


def rg(stops, cx=.5, cy=.5, r=.5, fx=None, fy=None, units="objectBoundingBox", gid=None):
    gid = gid or uid("rg")
    s = "".join('<stop offset="%s" stop-color="%s"%s/>' % (o, c, (' stop-opacity="%s"' % a) if a is not None else "")
                for o, c, a in [(t + (None,))[:3] for t in stops])
    fxy = ""
    if fx is not None:
        fxy = ' fx="%s" fy="%s"' % (fx, fy)
    return gid, '<radialGradient id="%s" cx="%s" cy="%s" r="%s"%s gradientUnits="%s">%s</radialGradient>' % (
        gid, cx, cy, r, fxy, units, s)


COMMON_DEFS = """
<filter id="fGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="fGlowBig" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="14" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="fB2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="fB4" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="fB8" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="fB16" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="fB30" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="30"/></filter>
<filter id="fB60" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="60"/></filter>
<filter id="fShadow" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#000" flood-opacity=".35"/></filter>
<filter id="fShadowS" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000" flood-opacity=".28"/></filter>
<filter id="fShadowSoft" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="12" stdDeviation="22" flood-color="#3a3024" flood-opacity=".22"/></filter>
<filter id="fNoise" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" seed="7" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="linear" slope="1"/></feComponentTransfer></filter>
<filter id="fPaper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".035 .06" numOctaves="4" seed="11"/><feColorMatrix type="saturate" values="0"/></filter>
<filter id="fPowder" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="4" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="4" xChannelSelector="R" yChannelSelector="G"/></filter>
<linearGradient id="gGold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7A4E12"/><stop offset=".25" stop-color="#E4B95B"/><stop offset=".45" stop-color="#FFF0B5"/><stop offset=".62" stop-color="#D7A43E"/><stop offset="1" stop-color="#7A4E12"/></linearGradient>
<linearGradient id="gGoldV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF1BC"/><stop offset=".35" stop-color="#E6BC5C"/><stop offset=".7" stop-color="#B8842A"/><stop offset="1" stop-color="#6E440E"/></linearGradient>
<linearGradient id="gGoldH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8A5A16"/><stop offset=".2" stop-color="#E2B657"/><stop offset=".5" stop-color="#FFF3C4"/><stop offset=".8" stop-color="#D2A03A"/><stop offset="1" stop-color="#8A5A16"/></linearGradient>
<linearGradient id="gMGold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8C7A55"/><stop offset=".35" stop-color="#CDBB8E"/><stop offset=".5" stop-color="#EFE4C6"/><stop offset=".7" stop-color="#B7A274"/><stop offset="1" stop-color="#7C6B48"/></linearGradient>
<linearGradient id="gSilver" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8E918F"/><stop offset=".3" stop-color="#D9DBD8"/><stop offset=".5" stop-color="#FAFAF7"/><stop offset=".7" stop-color="#C3C6C2"/><stop offset="1" stop-color="#7E817F"/></linearGradient>
<linearGradient id="gBrass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6B3F0C"/><stop offset=".22" stop-color="#C98A2A"/><stop offset=".42" stop-color="#FFE3A0"/><stop offset=".6" stop-color="#D99A33"/><stop offset="1" stop-color="#5E360A"/></linearGradient>
<linearGradient id="gClay" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5A1C08"/><stop offset=".3" stop-color="#B4471B"/><stop offset=".5" stop-color="#D8683A"/><stop offset=".75" stop-color="#9E3A14"/><stop offset="1" stop-color="#4A1605"/></linearGradient>
<linearGradient id="gFlame" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FFF8D8"/><stop offset=".25" stop-color="#FFE27A"/><stop offset=".6" stop-color="#FFA41B"/><stop offset="1" stop-color="#E8480C"/></linearGradient>
<linearGradient id="gFlameIn" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".5" stop-color="#FFF3B0"/><stop offset="1" stop-color="#FFD24A"/></linearGradient>
<radialGradient id="gHalo"><stop offset="0" stop-color="#FFD27A" stop-opacity=".9"/><stop offset=".35" stop-color="#FFA53A" stop-opacity=".45"/><stop offset="1" stop-color="#FF7A00" stop-opacity="0"/></radialGradient>
<radialGradient id="gHaloSoft"><stop offset="0" stop-color="#FFF1CF" stop-opacity=".85"/><stop offset=".4" stop-color="#F6DDAE" stop-opacity=".35"/><stop offset="1" stop-color="#F6DDAE" stop-opacity="0"/></radialGradient>
<radialGradient id="gWhiteHalo"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".95"/><stop offset=".45" stop-color="#FFFFFF" stop-opacity=".35"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
"""


def doc(body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1080" height="1350" '
            'viewBox="0 0 1080 1350"><defs>%s%s</defs>%s</svg>' % (COMMON_DEFS, defs, body))


def noise(op=.08, blend="multiply", x=0, y=0, w=W, h=H, clip=None):
    c = (' clip-path="url(#%s)"' % clip) if clip else ""
    return '<rect x="%s" y="%s" width="%s" height="%s" filter="url(#fNoise)" opacity="%s" style="mix-blend-mode:%s"%s/>' % (
        x, y, w, h, op, blend, c)


def paper(op=.10, blend="multiply"):
    return '<rect width="1080" height="1350" filter="url(#fPaper)" opacity="%s" style="mix-blend-mode:%s"/>' % (op, blend)


def vignette(color="#000", op=.55, inner=.55):
    gid, g = rg([(0, color, 0), (inner, color, 0), (1, color, op)], cx=.5, cy=.5, r=.75)
    return '<defs>%s</defs><rect width="1080" height="1350" fill="url(#%s)"/>' % (g, gid)


def bg_grad(stops, x1=0, y1=0, x2=0, y2=1):
    gid, g = lg(stops, x1, y1, x2, y2)
    return '<defs>%s</defs><rect width="1080" height="1350" fill="url(#%s)"/>' % (g, gid)


def glow(cx, cy, r, color="#FFB347", op=.8):
    gid, g = rg([(0, color, op), (.4, color, op * .45), (1, color, 0)])
    return '<defs>%s</defs><circle cx="%s" cy="%s" r="%s" fill="url(#%s)"/>' % (g, n(cx), n(cy), n(r), gid)


def eglow(cx, cy, rx, ry, color="#FFB347", op=.8):
    gid, g = rg([(0, color, op), (.45, color, op * .4), (1, color, 0)])
    return '<defs>%s</defs><ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%s)"/>' % (g, n(cx), n(cy), n(rx), n(ry), gid)


def bokeh(rng, count, x0, y0, x1, y1, colors, rmin=8, rmax=40, op=(.12, .4)):
    out = []
    for _ in range(count):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        r = rng.uniform(rmin, rmax)
        c = rng.choice(colors)
        o = rng.uniform(*op)
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>' % (n(x), n(y), n(r), c, n(o * 100) and round(o, 2)))
    return '<g filter="url(#fB4)">%s</g>' % "".join(out)


def stars(rng, count, x0, y0, x1, y1, color="#FFF6DA", rmax=2.4, twinkle=6):
    out = []
    for _ in range(count):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        r = rng.uniform(.5, rmax)
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>' % (n(x), n(y), n(r), color, round(rng.uniform(.35, 1), 2)))
    for _ in range(twinkle):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        out.append(sparkle(x, y, rng.uniform(8, 18), color))
    return "".join(out)


def sparkle(x, y, s, color="#FFF6DA", op=1):
    d = "M0,-1 C.08,-.2 .2,-.08 1,0 C.2,.08 .08,.2 0,1 C-.08,.2 -.2,.08 -1,0 C-.2,-.08 -.08,-.2 0,-1Z"
    return '<path d="%s" transform="translate(%s %s) scale(%s)" fill="%s" opacity="%s"/>' % (d, n(x), n(y), n(s), color, op)


def rpoly(cx, cy, r, k, rot=0):
    return [(cx + r * math.cos(rot + 2 * math.pi * i / k), cy + r * math.sin(rot + 2 * math.pi * i / k)) for i in range(k)]


def star_pts(cx, cy, r1, r2, k, rot=-math.pi / 2):
    out = []
    for i in range(2 * k):
        r = r1 if i % 2 == 0 else r2
        a = rot + math.pi * i / k
        out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


def ring(cx, cy, k, r, elem, rot0=0, scale=1):
    """repeat `elem` (drawn pointing up, centred at 0,-r) k times around (cx,cy)."""
    out = []
    for i in range(k):
        a = rot0 + 360.0 * i / k
        out.append('<g transform="rotate(%s %s %s) translate(%s %s) scale(%s)">%s</g>' % (
            n(a), n(cx), n(cy), n(cx), n(cy - r), scale, elem))
    return "".join(out)


# ---------------------------------------------------------------- edge / panels
def corner_ornament(x, y, s=1, rot=0, fill="url(#gGold)", op=1):
    """gold filigree corner (drawn for top-left, rotate for others)."""
    d = ("M0,0 L90,0 C70,6 40,10 26,26 C10,40 6,70 0,90 Z "
         "M18,18 C40,14 70,16 120,10 C90,22 62,24 44,34 C34,42 26,58 20,92 C18,62 14,40 18,18Z")
    curl = ("M40,40 C60,30 86,36 92,54 C96,68 84,78 74,72 C66,67 70,58 78,60 "
            "M40,40 C30,60 36,86 54,92 C68,96 78,84 72,74 C67,66 58,70 60,78")
    dots = "".join('<circle cx="%s" cy="%s" r="%s"/>' % (a, b, r) for a, b, r in
                   [(132, 10, 4), (146, 10, 2.6), (10, 132, 4), (10, 146, 2.6), (62, 62, 5)])
    return ('<g transform="translate(%s %s) rotate(%s) scale(%s)" opacity="%s"><path d="%s" fill="%s"/>'
            '<path d="%s" fill="none" stroke="%s" stroke-width="3.2" stroke-linecap="round"/><g fill="%s">%s</g></g>') % (
        n(x), n(y), rot, s, op, d, fill, curl, fill, fill, dots)


def four_corners(m=26, s=1, fill="url(#gGold)", op=1):
    return (corner_ornament(m, m, s, 0, fill, op) + corner_ornament(W - m, m, s, 90, fill, op) +
            corner_ornament(W - m, H - m, s, 180, fill, op) + corner_ornament(m, H - m, s, 270, fill, op))


def border_frame(m=22, color="url(#gGoldH)", w1=5, w2=1.6, gap=10, op=1, r=0):
    return ('<g fill="none" opacity="%s"><rect x="%s" y="%s" width="%s" height="%s" rx="%s" stroke="%s" stroke-width="%s"/>'
            '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" stroke="%s" stroke-width="%s"/></g>') % (
        op, m, m, W - 2 * m, H - 2 * m, r, color, w1, m + gap, m + gap, W - 2 * (m + gap), H - 2 * (m + gap), max(0, r - gap), color, w2)


def panel(x, y, w, h, fill, r=36, stroke="url(#gGoldH)", sw=3, inner=True, shadow="fShadow", op=1, inner_col=None):
    s = '<g opacity="%s"><rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" filter="url(#%s)"/>' % (op, x, y, w, h, r, fill, shadow)
    if stroke:
        s += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (x, y, w, h, r, stroke, sw)
    if inner:
        s += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="%s" stroke-width="1.4" opacity=".75"/>' % (
            x + 12, y + 12, w - 24, h - 24, max(0, r - 10), inner_col or stroke)
    return s + "</g>"


# ================================================================= DIWALI
def flame(x, y, s=1, glow_r=None, halo=True, calm=False):
    """flame with base at (x,y), height ~70*s."""
    out = ""
    if halo:
        gr = glow_r or 95 * s
        out += '<circle cx="%s" cy="%s" r="%s" fill="url(#gHalo)"/>' % (n(x), n(y - 30 * s), n(gr))
    sway = 0 if calm else 6
    d = "M0,0 C-15,-8 -16,-34 -3,-52 C2,-60 %s,-66 %s,-78 C14,-54 17,-30 13,-12 C10,-3 5,0 0,0Z" % (sway * .3, sway)
    di = "M0,-2 C-7,-6 -8,-20 -1,-34 C2,-26 7,-18 6,-9 C5,-4 3,-2 0,-2Z"
    out += ('<g transform="translate(%s %s) scale(%s)"><path d="%s" fill="url(#gFlame)" filter="url(#fGlow)"/>'
            '<path d="%s" fill="url(#gFlameIn)"/><ellipse cx="0" cy="-3" rx="3.5" ry="5" fill="#5A7BD6" opacity=".55"/></g>') % (
        n(x), n(y), s, d, di)
    return out


def diya(x, y, s=1, kind="clay", deco="#FFD86B", deco2="#FFFFFF", lit=True, glow_r=None, calm=False):
    """side-view diya; (x,y)= centre of the rim; bowl ~140*s wide."""
    body = kind == "clay" and "url(#gClay)" or "url(#gBrass)"
    rim_in = "#3A1406" if kind == "clay" else "#5A3508"
    g = '<g transform="translate(%s %s) scale(%s)">' % (n(x), n(y), s)
    g += '<ellipse cx="0" cy="52" rx="66" ry="9" fill="#000" opacity=".28" filter="url(#fB4)"/>'
    # foot
    g += '<path d="M-22,38 L22,38 L28,50 L-28,50Z" fill="%s"/>' % body
    # bowl with spout (spout on the right)
    g += '<path d="M-66,-2 C-64,26 -34,44 2,44 C34,44 56,30 64,8 C70,2 80,-6 92,-14 C78,-12 70,-8 62,-4 Z" fill="%s"/>' % body
    # oil surface
    g += '<ellipse cx="0" cy="-2" rx="66" ry="11" fill="%s"/>' % rim_in
    g += '<ellipse cx="0" cy="-1" rx="56" ry="7" fill="#E89A2A" opacity=".55"/>'
    g += '<path d="M-66,-2 C-40,10 40,10 66,-2" fill="none" stroke="%s" stroke-width="3"/>' % ("#E9884E" if kind == "clay" else "#FFE7A8")
    # painted decoration band
    band = ""
    for i in range(9):
        t = -52 + i * 13
        yy = 22 - abs(t) * .06
        band += '<circle cx="%s" cy="%s" r="3.2" fill="%s"/>' % (t, n(yy), deco)
    band += '<path d="M-58,12 C-30,26 30,26 58,12" fill="none" stroke="%s" stroke-width="2.2" opacity=".9"/>' % deco2
    band += '<path d="M-48,31 C-20,40 20,40 48,31" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="6 5"/>' % deco
    g += band
    # highlight
    g += '<path d="M-54,6 C-50,22 -36,32 -22,36" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".28"/>'
    # wick
    g += '<path d="M70,-8 C74,-14 76,-18 78,-24" stroke="#2A1206" stroke-width="4" stroke-linecap="round"/>'
    g += "</g>"
    if lit:
        g += flame(x + 78 * s, y - 22 * s, .95 * s, glow_r=glow_r, calm=calm)
    return g


def diya_top(x, y, s=1, rim="url(#gBrass)", lit=True):
    """three-quarter view, spout pointing up: good for rows seen from above."""
    g = '<g transform="translate(%s %s) scale(%s)">' % (n(x), n(y), s)
    g += '<ellipse cx="0" cy="20" rx="46" ry="10" fill="#000" opacity=".3" filter="url(#fB4)"/>'
    g += '<path d="M-44,0 C-44,22 -20,30 0,30 C20,30 44,22 44,0 Z" fill="url(#gClay)"/>'
    g += '<path d="M-44,0 C-44,-14 -20,-20 0,-34 C20,-20 44,-14 44,0 C44,10 20,14 0,14 C-20,14 -44,10 -44,0Z" fill="#E3782F"/>'
    g += '<path d="M-36,0 C-36,-9 -16,-14 0,-26 C16,-14 36,-9 36,0 C36,6 16,9 0,9 C-16,9 -36,6 -36,0Z" fill="#4A1805"/>'
    g += '<ellipse cx="-6" cy="0" rx="22" ry="4" fill="#F0A33A" opacity=".5"/>'
    g += '<g fill="#FFD86B">%s</g>' % "".join('<circle cx="%s" cy="%s" r="2.6"/>' % (t, n(18 - abs(t) * .12)) for t in range(-32, 33, 11))
    g += "</g>"
    if lit:
        g += flame(x, y - 24 * s, .8 * s)
    return g


def diya_cluster(cx, cy, s=1, n_=5, rng=None, kinds=("clay", "brass")):
    rng = rng or random.Random(3)
    out = []
    spots = [(-150, 20, .8), (150, 24, .82), (-70, -8, .95), (80, -4, .9), (0, 30, 1.12), (-230, 44, .62), (230, 46, .64)][:n_]
    spots.sort(key=lambda t: t[1])
    for i, (dx, dy, sc) in enumerate(spots):
        out.append(diya(cx + dx * s, cy + dy * s, sc * s, kind=kinds[i % len(kinds)],
                        deco=rng.choice(["#FFD86B", "#FFF3C4", "#7FE7D6"]), deco2="#FFFFFF"))
    return "".join(out)


def petal_path(r1, r2, w, tip="point"):
    """petal from radius r1 to r2 (pointing up, i.e. -y), half-width w."""
    m = r1 + (r2 - r1) * .45
    if tip == "round":
        return "M0,%s C%s,%s %s,%s 0,%s C%s,%s %s,%s 0,%sZ" % (
            n(-r1), n(w * 1.25), n(-m), n(w * .9), n(-r2 - w * .15), n(-r2), n(-w * .9), n(-r2 - w * .15), n(-w * 1.25), n(-m), n(-r1))
    if tip == "heart":
        return "M0,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s 0,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s 0,%sZ" % (
            n(-r1), n(w * 1.3), n(-m), n(w * 1.1), n(-r2 + w * .2), n(w * .5), n(-r2),
            n(w * .2), n(-r2), n(w * .06), n(-r2 + w * .3), n(-r2 + w * .5),
            n(-w * .06), n(-r2 + w * .3), n(-w * .2), n(-r2), n(-w * .5), n(-r2),
            n(-w * 1.1), n(-r2 + w * .2), n(-w * 1.3), n(-m), n(-r1))
    return "M0,%s C%s,%s %s,%s 0,%s C%s,%s %s,%s 0,%sZ" % (
        n(-r1), n(w * 1.3), n(-m), n(w * .35), n(-r2 + (r2 - r1) * .15), n(-r2),
        n(-w * .35), n(-r2 + (r2 - r1) * .15), n(-w * 1.3), n(-m), n(-r1))


def _around(k, body, rot0=0):
    return "".join('<g transform="rotate(%s)">%s</g>' % (n(rot0 + 360.0 * i / k), body) for i in range(k))


def rangoli(cx, cy, R, pal, style=0, flat=1.0, center=None, chalk="#FFFFFF", powder=True):
    """large detailed rangoli. pal: 6+ colours. style 0 floral, 1 geometric star, 2 lotus-rich."""
    c = pal
    ch = chalk
    L = []
    sw = max(1.2, R / 170.0)

    def pet(r1, r2, w, fill, tip="point", stroke=True, k=None, rot=0, inner=None):
        d = petal_path(r1, r2, w, tip)
        e = '<path d="%s" fill="%s"%s/>' % (d, fill, (' stroke="%s" stroke-width="%s"' % (ch, n(sw))) if stroke else "")
        if inner:
            d2 = petal_path(r1 + (r2 - r1) * .22, r2 - (r2 - r1) * .18, w * .5, tip)
            e += '<path d="%s" fill="%s"/>' % (d2, inner)
            e += '<circle cx="0" cy="%s" r="%s" fill="%s"/>' % (n(-(r1 + (r2 - r1) * .35)), n(max(1.5, w * .14)), ch)
        return _around(k, e, rot)

    def dots(r, k, rr, col=None, rot=0):
        return _around(k, '<circle cx="0" cy="%s" r="%s" fill="%s"/>' % (n(-r), n(rr), col or ch), rot)

    def band(r1, r2, fill):
        return '<circle r="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (n((r1 + r2) / 2), fill, n(r2 - r1)) + \
               '<circle r="%s" fill="none" stroke="%s" stroke-width="%s"/><circle r="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (
                   n(r1), ch, n(sw), n(r2), ch, n(sw))

    def zig(r1, r2, k, fill):
        pts_ = []
        for i in range(2 * k + 1):
            a = -math.pi / 2 + math.pi * i / k
            r = r2 if i % 2 == 0 else r1
            pts_.append((r * math.cos(a), r * math.sin(a)))
        return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (pts(pts_), fill, ch, n(sw * .8))

    def scallop(r, k, rr, fill):
        return _around(k, '<circle cx="0" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (n(-r), n(rr), fill, ch, n(sw * .8)))

    if style == 0:
        L.append(pet(R * .80, R * 1.0, R * .075, c[0], "point", k=24, inner=c[1]))
        L.append(pet(R * .80, R * .93, R * .045, c[2], "round", k=24, rot=7.5))
        L.append(dots(R * 1.035, 24, R * .012))
        L.append(band(R * .70, R * .80, c[3]))
        L.append(dots(R * .75, 48, R * .008))
        L.append(pet(R * .44, R * .71, R * .085, c[4], "heart", k=12, inner=c[5]))
        L.append(pet(R * .44, R * .64, R * .06, c[1], "point", k=12, rot=15, inner=c[2]))
        L.append(scallop(R * .44, 24, R * .03, c[2]))
        L.append(band(R * .34, R * .42, c[0]))
        L.append(dots(R * .38, 32, R * .008))
        L.append(pet(R * .10, R * .34, R * .09, c[5], "point", k=8, inner=c[3]))
        L.append(pet(R * .10, R * .28, R * .06, c[2], "round", k=8, rot=22.5))
        L.append('<circle r="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (n(R * .12), c[1], ch, n(sw)))
        L.append('<circle r="%s" fill="%s"/>' % (n(R * .05), c[3]))
    elif style == 1:
        L.append(zig(R * .86, R * 1.0, 32, c[0]))
        L.append(dots(R * 1.03, 32, R * .012))
        L.append(band(R * .78, R * .86, c[2]))
        L.append(_around(16, '<path d="M0,%s L%s,%s L0,%s L%s,%sZ" fill="%s" stroke="%s" stroke-width="%s"/>' % (
            n(-R * .78), n(R * .06), n(-R * .64), n(-R * .52), n(-R * .06), n(-R * .64), c[3], ch, n(sw))))
        L.append(_around(16, '<path d="M0,%s L%s,%s L0,%s L%s,%sZ" fill="%s" stroke="%s" stroke-width="%s"/>' % (
            n(-R * .74), n(R * .045), n(-R * .64), n(-R * .56), n(-R * .045), n(-R * .64), c[4], ch, n(sw * .6)), 11.25))
        L.append(dots(R * .66, 16, R * .014, c[1], 11.25))
        L.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (
            pts(star_pts(0, 0, R * .56, R * .40, 8)), c[1], ch, n(sw)))
        L.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (
            pts(star_pts(0, 0, R * .50, R * .36, 8, -math.pi / 2 + math.pi / 8)), c[5], ch, n(sw)))
        L.append(band(R * .30, R * .36, c[0]))
        L.append(dots(R * .33, 24, R * .008))
        L.append(pet(R * .06, R * .30, R * .07, c[2], "heart", k=8, inner=c[4]))
        L.append('<circle r="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (n(R * .09), c[3], ch, n(sw)))
    else:
        L.append(pet(R * .66, R * 1.0, R * .12, c[0], "round", k=16, inner=c[2]))
        L.append(pet(R * .66, R * .90, R * .07, c[4], "point", k=16, rot=11.25, inner=c[1]))
        L.append(dots(R * 1.03, 16, R * .014))
        L.append(dots(R * .92, 16, R * .01, None, 11.25))
        L.append(band(R * .58, R * .66, c[3]))
        L.append(dots(R * .62, 40, R * .008))
        L.append(pet(R * .30, R * .58, R * .11, c[1], "point", k=8, inner=c[5]))
        L.append(pet(R * .30, R * .52, R * .085, c[5], "point", k=8, rot=22.5, inner=c[0]))
        L.append(scallop(R * .30, 16, R * .03, c[2]))
        L.append(pet(R * .08, R * .28, R * .07, c[3], "round", k=8, inner=c[2]))
        L.append('<circle r="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (n(R * .09), c[0], ch, n(sw)))
    inner = "".join(L)
    cid = uid("rc")
    tex = ('<clipPath id="%s"><circle r="%s"/></clipPath>' % (cid, n(R * 1.06)))
    grain = '<rect x="%s" y="%s" width="%s" height="%s" filter="url(#fNoise)" opacity=".22" style="mix-blend-mode:multiply" clip-path="url(#%s)"/>' % (
        n(-R * 1.1), n(-R * 1.1), n(R * 2.2), n(R * 2.2), cid)
    filt = ' filter="url(#fPowder)"' if powder else ""
    return '<defs>%s</defs><g transform="translate(%s %s) scale(1 %s)"><g%s>%s</g>%s</g>%s' % (
        tex, n(cx), n(cy), flat, filt, inner, grain, center or "")


def akash_kandil_star(cx, top, s=1, c1="#E0115F", c2="#FF8A00", c3="#FFD23F", string_top=0, tails=True):
    """star kandil (8-point 3D paper star) hanging from a string; body centre at (cx, top+170*s)."""
    cy = top + 170 * s
    R, r = 150 * s, 62 * s
    g = '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#E9C46A" stroke-width="2.4"/>' % (n(cx), n(string_top), n(cx), n(cy - R))
    g += '<circle cx="%s" cy="%s" r="%s" fill="url(#gHalo)"/>' % (n(cx), n(cy), n(R * 1.7))
    # tails first
    if tails:
        for side, col in ((-1, c1), (1, c2)):
            a = math.pi / 2 + side * math.pi / 4
            bx, by = cx + R * .7 * math.cos(a), cy + R * .7 * math.sin(a)
            for k in range(5):
                x0 = bx + side * k * 7 * s - side * 12 * s
                ln = (150 + 30 * ((k * 7) % 3)) * s
                col2 = [c1, c2, c3, "#FFFFFF", c1][k]
                d = "M%s,%s C%s,%s %s,%s %s,%s" % (n(x0), n(by), n(x0 + side * 8 * s), n(by + ln * .35),
                                                   n(x0 - side * 10 * s), n(by + ln * .7), n(x0 + side * 4 * s), n(by + ln))
                g += '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" opacity=".95"/>' % (d, col2, n(6 * s))
    P = star_pts(cx, cy, R, r, 8, -math.pi / 2)
    # facets
    for i in range(16):
        a, b = P[i], P[(i + 1) % 16]
        light = (i % 2 == 0)
        base = [c1, c2][(i // 2) % 2]
        g += '<polygon points="%s" fill="%s"/>' % (pts([(cx, cy), a, b]), base)
        if not light:
            g += '<polygon points="%s" fill="#000" opacity=".22"/>' % pts([(cx, cy), a, b])
        else:
            g += '<polygon points="%s" fill="#fff" opacity=".10"/>' % pts([(cx, cy), a, b])
    g += '<polygon points="%s" fill="none" stroke="url(#gGold)" stroke-width="%s" stroke-linejoin="round"/>' % (pts(P), n(3.5 * s))
    for i in range(0, 16, 2):
        g += '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" opacity=".7"/>' % (
            n(cx), n(cy), n(P[i][0]), n(P[i][1]), c3, n(1.6 * s))
    # inner glowing lit core with cut pattern
    g += '<circle cx="%s" cy="%s" r="%s" fill="url(#gHalo)"/>' % (n(cx), n(cy), n(r * 1.6))
    g += '<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="url(#gGold)" stroke-width="%s"/>' % (n(cx), n(cy), n(r * .78), c3, n(3 * s))
    g += '<polygon points="%s" fill="%s"/>' % (pts(star_pts(cx, cy, r * .66, r * .3, 8)), c1)
    g += '<circle cx="%s" cy="%s" r="%s" fill="#FFF6D0"/>' % (n(cx), n(cy), n(r * .2))
    # tip bobbles
    for i in range(0, 16, 2):
        g += '<circle cx="%s" cy="%s" r="%s" fill="url(#gGold)"/>' % (n(P[i][0]), n(P[i][1]), n(5 * s))
    return g


def akash_kandil_hex(cx, top, s=1, c1="#1B9AAA", c2="#E0115F", c3="#FFD23F", string_top=0):
    """hexagonal paper lantern with cut-work windows and tassels; ~ 190 wide, 300 tall at s=1."""
    w, hgt = 190 * s, 210 * s
    y0 = top + 60 * s
    g = '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#E9C46A" stroke-width="2.4"/>' % (n(cx), n(string_top), n(cx), n(top))
    g += '<circle cx="%s" cy="%s" r="%s" fill="url(#gHalo)"/>' % (n(cx), n(y0 + hgt / 2), n(w * 1.25))
    # top cap
    g += '<polygon points="%s" fill="url(#gGoldV)"/>' % pts([(cx - 22 * s, top), (cx + 22 * s, top), (cx + w / 2 + 10 * s, y0), (cx - w / 2 - 10 * s, y0)])
    g += '<polygon points="%s" fill="%s" opacity=".6"/>' % (pts([(cx - 18 * s, top + 6 * s), (cx + 18 * s, top + 6 * s), (cx + w / 2 - 6 * s, y0 - 4 * s), (cx - w / 2 + 6 * s, y0 - 4 * s)]), c2)
    # faces
    fw = w * .56
    xs = [cx - w / 2, cx - fw / 2, cx + fw / 2, cx + w / 2]
    faces = [(xs[0], xs[1], .38), (xs[1], xs[2], 0), (xs[2], xs[3], .3)]
    lid = uid("lk")
    gl, gdef = lg([(0, "#FFF7C8"), (.5, c3), (1, "#FF9A1F")], 0, 0, 0, 1, gid=lid)
    g += "<defs>%s</defs>" % gdef
    for a, b, dk in faces:
        g += '<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)"/>' % (n(a), n(y0), n(b - a), n(hgt), lid)
        # cut-work: rhombus lattice painted in c1 with openings showing glow
        cols = max(2, int((b - a) / (22 * s)))
        cw = (b - a) / cols
        rows = 7
        rh = hgt / rows
        for i in range(cols):
            for j in range(rows):
                x_ = a + cw * (i + .5)
                y_ = y0 + rh * (j + .5)
                g += '<polygon points="%s" fill="%s"/>' % (pts([(x_, y_ - rh * .5), (x_ + cw * .5, y_), (x_, y_ + rh * .5), (x_ - cw * .5, y_)]), c1)
                g += '<polygon points="%s" fill="#FFF2B0"/>' % pts([(x_, y_ - rh * .26), (x_ + cw * .24, y_), (x_, y_ + rh * .26), (x_ - cw * .24, y_)])
        g += '<rect x="%s" y="%s" width="%s" height="%s" fill="#000" opacity="%s"/>' % (n(a), n(y0), n(b - a), n(hgt), dk * .6)
        g += '<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="url(#gGoldV)" stroke-width="%s"/>' % (n(a), n(y0), n(b - a), n(hgt), n(3 * s))
    # bands
    for yy in (y0, y0 + hgt):
        g += '<rect x="%s" y="%s" width="%s" height="%s" fill="url(#gGoldH)"/>' % (n(cx - w / 2 - 4 * s), n(yy - 7 * s), n(w + 8 * s), n(14 * s))
    # bottom cap
    yb = y0 + hgt
    g += '<polygon points="%s" fill="%s"/>' % (pts([(cx - w / 2, yb + 6 * s), (cx + w / 2, yb + 6 * s), (cx + 30 * s, yb + 52 * s), (cx - 30 * s, yb + 52 * s)]), c2)
    g += '<polygon points="%s" fill="#000" opacity=".25"/>' % pts([(cx + fw / 2, yb + 6 * s), (cx + w / 2, yb + 6 * s), (cx + 30 * s, yb + 52 * s), (cx + 16 * s, yb + 52 * s)])
    # tassels
    for k, dx in enumerate((-60, -30, 0, 30, 60)):
        x_ = cx + dx * s
        yy = yb + (8 if abs(dx) > 40 else 50) * s
        ln = (90 + (k % 2) * 30) * s
        g += '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"/>' % (n(x_), n(yy), n(x_), n(yy + ln * .6), c3, n(2 * s))
        g += '<circle cx="%s" cy="%s" r="%s" fill="url(#gGold)"/>' % (n(x_), n(yy + ln * .6), n(6 * s))
        g += '<path d="M%s,%s L%s,%s L%s,%s Z" fill="%s"/>' % (n(x_ - 7 * s), n(yy + ln * .62), n(x_ + 7 * s), n(yy + ln * .62), n(x_), n(yy + ln), c2)
        g += '<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="%s"/>' % (n(x_), n(yy + ln * .62), n(x_), n(yy + ln * 1.05), c1, n(2.4 * s))
    return g


def akash_kandil_round(cx, top, s=1, c1="#6A2C91", c2="#FF4F79", c3="#FFD23F", string_top=0):
    """round paper lantern with vertical ribs + frill; body r~110*s."""
    r = 110 * s
    cy = top + 30 * s + r
    g = '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#E9C46A" stroke-width="2.4"/>' % (n(cx), n(string_top), n(cx), n(top))
    g += '<circle cx="%s" cy="%s" r="%s" fill="url(#gHalo)"/>' % (n(cx), n(cy), n(r * 1.7))
    gid, gd = rg([(0, "#FFF8D0"), (.35, c3), (.8, c2), (1, c1)], cx=.45, cy=.42, r=.6)
    g += "<defs>%s</defs>" % gd
    g += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="url(#gGoldV)"/>' % (n(cx - 30 * s), n(top), n(60 * s), n(34 * s), n(6 * s))
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%s)"/>' % (n(cx), n(cy), n(r), n(r * .92), gid)
    for k in range(-4, 5):
        rx = r * abs(k) / 4.4
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width="%s" opacity=".55"/>' % (
            n(cx), n(cy), n(max(1, rx)), n(r * .92), c1, n(2 * s))
    # decorative band with dots
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (n(cx), n(cy), n(r * .99), n(r * .2), c1, n(14 * s))
    for k in range(13):
        a = math.pi * k / 12
        g += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(cx - r * .97 * math.cos(a)), n(cy + r * .2 * math.sin(a)), n(4 * s), c3)
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff" opacity=".25"/>' % (n(cx - r * .35), n(cy - r * .4), n(r * .22), n(r * .35))
    # bottom frill
    yb = cy + r * .9
    g += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="url(#gGoldV)"/>' % (n(cx - 34 * s), n(yb - 6 * s), n(68 * s), n(18 * s), n(5 * s))
    for k in range(-5, 6):
        x_ = cx + k * 7 * s
        ln = (70 + (abs(k) % 3) * 16) * s
        g += '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
            n(x_), n(yb + 10 * s), n(x_ + k * 1.5 * s), n(yb + ln), [c2, c3, c1][k % 3], n(3.4 * s))
    return g


def firework(cx, cy, r, color, color2="#FFFFFF", k=36, seed=1, op=1):
    rng = random.Random(seed)
    out = ['<g opacity="%s">' % op]
    out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".18" filter="url(#fB16)"/>' % (n(cx), n(cy), n(r * .8), color))
    gid, gd = rg([(0, color2, 0), (.35, color, .25), (1, color, 1)], cx=.5, cy=.5, r=.5)
    for i in range(k):
        a = 2 * math.pi * i / k + rng.uniform(-.04, .04)
        rr = r * rng.uniform(.78, 1.0)
        x2, y2 = cx + rr * math.cos(a), cy + rr * math.sin(a) + rr * .06
        x1, y1 = cx + rr * .25 * math.cos(a), cy + rr * .25 * math.sin(a)
        mx, my = cx + rr * .7 * math.cos(a), cy + rr * .7 * math.sin(a) + rr * .02
        out.append('<path d="M%s,%s Q%s,%s %s,%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" opacity=".8"/>' % (
            n(x1), n(y1), n(mx), n(my), n(x2), n(y2), color, n(max(1.4, r / 70))))
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(x2), n(y2 + 3), n(max(2, r / 45)), color2))
        if i % 2 == 0:
            out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".8"/>' % (
                n(cx + rr * .55 * math.cos(a + .05)), n(cy + rr * .55 * math.sin(a + .05)), n(max(1.4, r / 70)), color))
    out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" filter="url(#fB4)"/>' % (n(cx), n(cy), n(r * .08), color2))
    out.append("</g>")
    return '<g filter="url(#fGlow)">%s</g>' % "".join(out)


def string_lights(x0, y0, x1, y1, sag, count, colors, bulb=7, seed=2, wire="#3A2A1A"):
    out = []
    mx, my = (x0 + x1) / 2, max(y0, y1) + sag
    out.append('<path d="M%s,%s Q%s,%s %s,%s" fill="none" stroke="%s" stroke-width="2"/>' % (n(x0), n(y0), n(mx), n(my), n(x1), n(y1), wire))
    for i in range(1, count):
        t = i / float(count)
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1
        c = colors[i % len(colors)]
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".5" filter="url(#fB8)"/>' % (n(x), n(y + bulb), n(bulb * 2.6), c))
        out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="1.5" fill="%s"/>' % (n(x - bulb * .35), n(y - 2), n(bulb * .7), n(bulb * .7), wire))
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (n(x), n(y + bulb * 1.1), n(bulb * .75), n(bulb * 1.05), c))
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff" opacity=".75"/>' % (n(x - bulb * .2), n(y + bulb * .85), n(bulb * .22), n(bulb * .4)))
    return "".join(out)


def footprint(x, y, s=1, rot=0, mirror=False, col="#C2185B", dotc="#FFF3D6"):
    """Lakshmi footprint, toes up. ~ 60x130 at s=1."""
    sx = -1 if mirror else 1
    g = '<g transform="translate(%s %s) rotate(%s) scale(%s %s)">' % (n(x), n(y), rot, n(sx * s), n(s))
    g += '<path d="M-6,-40 C18,-44 30,-20 26,6 C22,30 20,44 12,58 C4,70 -18,70 -22,54 C-26,40 -14,26 -18,6 C-22,-14 -24,-36 -6,-40Z" fill="%s"/>' % col
    for tx, ty, tr in ((-14, -54, 9.5), (4, -58, 8), (17, -52, 7), (26, -43, 6), (32, -32, 5)):
        g += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (tx, ty, tr, col)
    g += '<circle cx="2" cy="-6" r="6" fill="none" stroke="%s" stroke-width="2"/><circle cx="2" cy="-6" r="2" fill="%s"/>' % (dotc, dotc)
    g += '<path d="M-8,20 C0,26 8,26 14,20" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="2 4" stroke-linecap="round"/>' % dotc
    g += '<circle cx="2" cy="44" r="4" fill="none" stroke="%s" stroke-width="2"/>' % dotc
    return g + "</g>"


def footprint_pair(x, y, s=1, rot=0, col="#C2185B", dotc="#FFF3D6"):
    a = math.radians(rot)
    ox, oy = 30 * s * math.cos(a), 30 * s * math.sin(a)
    return footprint(x - ox, y - oy + 8 * s, s, rot, False, col, dotc) .replace("scale(%s %s)" % (n(s), n(s)), "scale(%s %s)" % (n(-s), n(s)), 1) + \
        footprint(x + ox, y + oy, s, rot, False, col, dotc)


def ladoo(x, y, r, c1="#F6A623", c2="#C46A08", seed=0):
    rng = random.Random(seed)
    gid, gd = rg([(0, "#FFE19A"), (.45, c1), (1, c2)], cx=.38, cy=.34, r=.7)
    g = '<defs>%s</defs><circle cx="%s" cy="%s" r="%s" fill="url(#%s)"/>' % (gd, n(x), n(y), n(r), gid)
    for _ in range(int(r * .9)):
        a, d = rng.uniform(0, 6.28), rng.uniform(0, r * .85)
        g += '<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".55"/>' % (n(x + d * math.cos(a)), n(y + d * math.sin(a)), n(r * .06), rng.choice(["#FFF0C0", c2]))
    return g


def kaju(x, y, s=1):
    return ('<g transform="translate(%s %s) scale(%s 1)"><polygon points="0,-%s %s,0 0,%s -%s,0" fill="url(#gSilver)" stroke="#B9B6AE" stroke-width="1"/>'
            '<polygon points="0,-%s %s,0 0,%s -%s,0" fill="#F2E7D0" opacity=".6"/></g>') % (
        n(x), n(y), 1, n(20 * s), n(34 * s), n(20 * s), n(34 * s), n(14 * s), n(24 * s), n(14 * s), n(24 * s))


def mithai_box(cx, cy, s=1, box="#B0123E", trim="url(#gGoldH)"):
    """open sweets box (3/4 view) with ladoo pyramid and kaju katli; cy = front-bottom edge."""
    w, d_, h = 360 * s, 120 * s, 70 * s
    x0 = cx - w / 2
    g = '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#000" opacity=".35" filter="url(#fB8)"/>' % (n(cx), n(cy + 6 * s), n(w * .6), n(20 * s))
    # lid leaning behind
    g += '<g transform="rotate(-8 %s %s)"><rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>' % (
        n(cx), n(cy - h - d_), n(x0 + 20 * s), n(cy - h - d_ - 150 * s), n(w - 40 * s), n(150 * s), n(8 * s), box)
    g += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (
        n(x0 + 34 * s), n(cy - h - d_ - 136 * s), n(w - 68 * s), n(122 * s), n(6 * s), trim, n(4 * s))
    g += '<g transform="translate(%s %s)" opacity=".9">%s</g>' % (n(cx), n(cy - h - d_ - 75 * s), rangoli_mini(38 * s, "#FFD86B", "#FFF1C1"))
    g += "</g>"
    # inner back & floor
    g += '<polygon points="%s" fill="#6E0A26"/>' % pts([(x0, cy - h), (x0 + 40 * s, cy - h - d_), (x0 + w - 40 * s, cy - h - d_), (x0 + w, cy - h)])
    g += '<polygon points="%s" fill="#F4E4C4"/>' % pts([(x0 + 10 * s, cy - h - 4 * s), (x0 + 46 * s, cy - h - d_ + 10 * s), (x0 + w - 46 * s, cy - h - d_ + 10 * s), (x0 + w - 10 * s, cy - h - 4 * s)])
    # sweets: kaju rows at back, ladoo pyramid front-left, more at right
    for row in range(2):
        for i in range(5):
            g += kaju(x0 + (205 + i * 30 + row * 14) * s, cy - h - d_ + (30 + row * 30) * s, .72 * s)
    lx = x0 + 100 * s
    base_y = cy - h - 10 * s
    for i in range(4):
        g += ladoo(lx - 60 * s + i * 40 * s, base_y, 22 * s, seed=i)
    for i in range(3):
        g += ladoo(lx - 40 * s + i * 40 * s, base_y - 30 * s, 22 * s, seed=10 + i)
    for i in range(2):
        g += ladoo(lx - 20 * s + i * 40 * s, base_y - 60 * s, 22 * s, seed=20 + i)
    g += ladoo(lx, base_y - 90 * s, 22 * s, seed=30)
    for i in range(4):
        g += ladoo(x0 + (212 + i * 38) * s, base_y - 4 * s, 19 * s, "#F7E6B8", "#C9A76A", seed=40 + i)
    # front face
    fid, fd = lg([(0, box), (1, "#5E0620")], 0, 0, 0, 1)
    g += '<defs>%s</defs><rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="url(#%s)"/>' % (fd, n(x0), n(cy - h), n(w), n(h), n(6 * s), fid)
    g += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (n(x0), n(cy - h), n(w), n(8 * s), trim)
    g += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (n(x0), n(cy - 12 * s), n(w), n(6 * s), trim)
    for i in range(12):
        g += '<circle cx="%s" cy="%s" r="%s" fill="#FFD86B"/>' % (n(x0 + 20 * s + i * 29 * s), n(cy - h / 2), n(4 * s))
        g += '<path d="M%s,%s l%s,%s l%s,%s l%s,%sZ" fill="none" stroke="#FFD86B" stroke-width="1.5" opacity=".7"/>' % (
            n(x0 + 34 * s + i * 29 * s), n(cy - h / 2 - 12 * s), n(8 * s), n(12 * s), n(-8 * s), n(12 * s), n(-8 * s), n(-12 * s))
    return g


def rangoli_mini(r, c1, c2):
    e = '<path d="%s" fill="%s"/>' % (petal_path(r * .25, r, r * .18), c1)
    return _around(8, e) + '<circle r="%s" fill="%s"/>' % (n(r * .25), c2)


def phuljhadi(x, y, ang, ln=260, s=1, seed=5):
    """sparkler: stick from (x,y) along angle, burning tip with sparks."""
    rng = random.Random(seed)
    a = math.radians(ang)
    tx, ty = x + ln * math.cos(a), y + ln * math.sin(a)
    mx, my = x + ln * .55 * math.cos(a), y + ln * .55 * math.sin(a)
    g = '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#7A7A7A" stroke-width="%s" stroke-linecap="round"/>' % (n(x), n(y), n(mx), n(my), n(4 * s))
    g += '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#3A2A20" stroke-width="%s" stroke-linecap="round"/>' % (n(mx), n(my), n(tx), n(ty), n(7 * s))
    g += '<circle cx="%s" cy="%s" r="%s" fill="url(#gHalo)"/>' % (n(tx), n(ty), n(130 * s))
    sp = []
    for i in range(70):
        b = rng.uniform(0, 6.283)
        r1 = rng.uniform(8, 30) * s
        r2 = r1 + rng.uniform(20, 95) * s
        sp.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
            n(tx + r1 * math.cos(b)), n(ty + r1 * math.sin(b)), n(tx + r2 * math.cos(b)), n(ty + r2 * math.sin(b)),
            rng.choice(["#FFF6D0", "#FFD66B", "#FFFFFF", "#FFB23F"]), n(rng.uniform(1, 2.6) * s)))
        if i % 3 == 0:
            ex, ey = tx + r2 * math.cos(b), ty + r2 * math.sin(b)
            sp.append(sparkle(ex, ey, rng.uniform(4, 9) * s, "#FFF6D0"))
    g += '<g filter="url(#fGlow)">%s<circle cx="%s" cy="%s" r="%s" fill="#FFFFFF"/></g>' % ("".join(sp), n(tx), n(ty), n(9 * s))
    return g


def samai(cx, base_y, s=1):
    """tall brass standing lamp (deep samai) with 5 wicks and a peacock-free finial; ~ 520*s tall."""
    g = '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#000" opacity=".35" filter="url(#fB8)"/>' % (n(cx), n(base_y), n(150 * s), n(18 * s))
    # base (stepped)
    g += '<path d="M%s,%s C%s,%s %s,%s %s,%s L%s,%s C%s,%s %s,%s %s,%s Z" fill="url(#gBrass)"/>' % (
        n(cx - 140 * s), n(base_y), n(cx - 120 * s), n(base_y - 50 * s), n(cx - 40 * s), n(base_y - 60 * s), n(cx - 30 * s), n(base_y - 90 * s),
        n(cx + 30 * s), n(base_y - 90 * s), n(cx + 40 * s), n(base_y - 60 * s), n(cx + 120 * s), n(base_y - 50 * s), n(cx + 140 * s), n(base_y))
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#gBrass)"/>' % (n(cx), n(base_y), n(140 * s), n(14 * s))
    # stem with knots
    g += '<rect x="%s" y="%s" width="%s" height="%s" fill="url(#gBrass)"/>' % (n(cx - 14 * s), n(base_y - 330 * s), n(28 * s), n(250 * s))
    for k, yy in enumerate((110, 170, 230, 300)):
        rr = (36 if k % 2 == 0 else 26) * s
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#gBrass)"/>' % (n(cx), n(base_y - yy * s), n(rr), n(rr * .45))
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff" opacity=".2"/>' % (n(cx - rr * .3), n(base_y - yy * s - rr * .12), n(rr * .3), n(rr * .12))
    # lamp bowl with 5 spouts
    by = base_y - 360 * s
    g += '<path d="M%s,%s C%s,%s %s,%s %s,%s Z" fill="url(#gBrass)"/>' % (
        n(cx - 150 * s), n(by), n(cx - 120 * s), n(by + 60 * s), n(cx + 120 * s), n(by + 60 * s), n(cx + 150 * s), n(by))
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#5A3508"/>' % (n(cx), n(by), n(150 * s), n(18 * s))
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#E8A33A" opacity=".5"/>' % (n(cx), n(by + 2 * s), n(120 * s), n(10 * s))
    g += '<path d="M%s,%s C%s,%s %s,%s %s,%s" fill="none" stroke="#FFE7A8" stroke-width="%s"/>' % (
        n(cx - 150 * s), n(by), n(cx - 60 * s), n(by + 20 * s), n(cx + 60 * s), n(by + 20 * s), n(cx + 150 * s), n(by), n(3 * s))
    # finial
    g += '<path d="M%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s Z" fill="url(#gBrass)"/>' % (
        n(cx - 16 * s), n(by - 10 * s), n(cx - 40 * s), n(by - 60 * s), n(cx - 6 * s), n(by - 100 * s), n(cx), n(by - 130 * s),
        n(cx + 6 * s), n(by - 100 * s), n(cx + 40 * s), n(by - 60 * s), n(cx + 16 * s), n(by - 10 * s))
    g += '<circle cx="%s" cy="%s" r="%s" fill="url(#gGold)"/>' % (n(cx), n(by - 134 * s), n(9 * s))
    for dx, dy in ((-150, -4), (-80, 8), (0, 12), (80, 8), (150, -4)):
        if dx == 0:
            continue
        g += flame(cx + dx * s, by + dy * s - 8 * s, .95 * s, glow_r=120 * s)
    g += flame(cx, by + 18 * s - 8 * s, 0.001, glow_r=1, halo=False)
    return g




def footprint(x, y, s=1, rot=0, mirror=False, col="#C2185B", dotc="#FFF3D6"):
    """Lakshmi footprint (kumkum), toes up, big toe on the inner side. ~70x150 at s=1."""
    sx = -1 if mirror else 1
    g = '<g transform="translate(%s %s) rotate(%s) scale(%s %s)">' % (n(x), n(y), rot, n(sx * s), n(s))
    g += ('<path d="M-4,-44 C16,-46 28,-30 28,-8 C28,14 20,26 20,40 C20,58 12,72 -2,72 C-18,72 -24,58 -22,42 '
          'C-20,28 -28,12 -28,-8 C-28,-30 -20,-42 -4,-44Z" fill="%s"/>') % col
    for tx, ty, tr in ((-15, -60, 10), (2, -64, 7.5), (15, -60, 6.5), (25, -52, 5.5), (32, -41, 4.8)):
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (tx, ty, tr, n(tr * 1.2), col)
    g += '<circle cx="0" cy="-12" r="8" fill="none" stroke="%s" stroke-width="2.2"/><circle cx="0" cy="-12" r="2.6" fill="%s"/>' % (dotc, dotc)
    g += _around(8, '<circle cx="0" cy="-14" r="1.6" fill="%s"/>' % dotc).replace('<g transform="rotate(', '<g transform="translate(0 -12) rotate(')
    g += '<path d="M-10,22 C-2,28 6,28 12,22" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="1 5" stroke-linecap="round"/>' % dotc
    g += '<circle cx="0" cy="50" r="5" fill="none" stroke="%s" stroke-width="2"/>' % dotc
    return g + "</g>"


def footprint_pair(x, y, s=1, rot=0, col="#C2185B", dotc="#FFF3D6"):
    a = math.radians(rot)
    ox, oy = 34 * s * math.cos(a), 34 * s * math.sin(a)
    return footprint(x - ox, y - oy, s, rot, True, col, dotc) + footprint(x + ox, y + oy, s, rot, False, col, dotc)


def diya_row(x0, x1, y, count, s=1, rng=None, kind="clay"):
    """a straight row of diyas along a ledge (y = rim line)."""
    rng = rng or random.Random(9)
    out = []
    for i in range(count):
        t = (i + .5) / count
        out.append(diya(x0 + (x1 - x0) * t, y + rng.uniform(-3, 3), s * rng.uniform(.92, 1.05), kind=kind if kind != "mix" else ("clay", "brass")[i % 2],
                        deco=rng.choice(["#FFD86B", "#FFF3C4", "#7FE7D6"])))
    return "".join(out)


def urli(cx, cy, s=1, rng=None, petals=("#FF9E1B", "#E23E57", "#FFC93C", "#FFFFFF")):
    """brass urli bowl (3/4 view) with water, floating diyas and petals; cy = rim centre, rim rx=300*s."""
    rng = rng or random.Random(12)
    rx, ry = 300 * s, 82 * s
    g = '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#000" opacity=".4" filter="url(#fB16)"/>' % (n(cx), n(cy + 150 * s), n(rx * .9), n(30 * s))
    # bowl body
    g += '<path d="M%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s Z" fill="url(#gBrass)"/>' % (
        n(cx - rx), n(cy), n(cx - rx * .96), n(cy + 120 * s), n(cx - rx * .45), n(cy + 150 * s), n(cx), n(cy + 150 * s),
        n(cx + rx * .45), n(cy + 150 * s), n(cx + rx * .96), n(cy + 120 * s), n(cx + rx), n(cy))
    g += '<path d="M%s,%s C%s,%s %s,%s %s,%s" fill="none" stroke="#FFF1C4" stroke-width="%s" opacity=".35" stroke-linecap="round"/>' % (
        n(cx - rx * .85), n(cy + 30 * s), n(cx - rx * .8), n(cy + 90 * s), n(cx - rx * .5), n(cy + 120 * s), n(cx - rx * .3), n(cy + 128 * s), n(8 * s))
    # engraved band
    for k in range(15):
        t = (k + .5) / 15
        a = math.pi * t
        g += '<circle cx="%s" cy="%s" r="%s" fill="#6B3F0C" opacity=".55"/>' % (n(cx - rx * .9 * math.cos(a)), n(cy + 60 * s + 30 * s * math.sin(a)), n(4 * s))
    # foot
    g += '<path d="M%s,%s L%s,%s L%s,%s L%s,%sZ" fill="url(#gBrass)"/>' % (n(cx - 90 * s), n(cy + 146 * s), n(cx + 90 * s), n(cy + 146 * s), n(cx + 110 * s), n(cy + 172 * s), n(cx - 110 * s), n(cy + 172 * s))
    # rim + water
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#gGoldH)"/>' % (n(cx), n(cy), n(rx + 14 * s), n(ry + 10 * s))
    wid, wd = rg([(0, "#3A7C8C"), (.7, "#15414F"), (1, "#0B2530")], cx=.5, cy=.4, r=.6)
    g += '<defs>%s</defs><ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%s)"/>' % (wd, n(cx), n(cy), n(rx), n(ry), wid)
    cid = uid("uc")
    g += '<defs><clipPath id="%s"><ellipse cx="%s" cy="%s" rx="%s" ry="%s"/></clipPath></defs><g clip-path="url(#%s)">' % (cid, n(cx), n(cy), n(rx), n(ry), cid)
    for k in range(6):
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="#9FE3EC" stroke-width="1.4" opacity=".25"/>' % (
            n(cx + rng.uniform(-rx * .5, rx * .5)), n(cy + rng.uniform(-ry * .4, ry * .4)), n(rng.uniform(30, 70) * s), n(rng.uniform(8, 16) * s))
    # petals
    for _ in range(46):
        a = rng.uniform(0, 6.283); d = rng.uniform(.1, .95)
        px, py = cx + rx * d * math.cos(a), cy + ry * d * math.sin(a)
        c = rng.choice(petals)
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" transform="rotate(%s %s %s)" fill="%s" opacity=".95"/>' % (
            n(px), n(py), n(rng.uniform(7, 12) * s), n(rng.uniform(4, 6) * s), n(rng.uniform(0, 180)), n(px), n(py), c)
    # floating marigold heads
    for fx, fy in ((-.55, .2), (.5, -.3), (.1, .55), (-.2, -.5), (.75, .3)):
        g += marigold(cx + rx * fx, cy + ry * fx * 0 + ry * fy, 26 * s, seed=int(fx * 100))
    g += "</g>"
    # floating diyas (reflections)
    for fx, fy, sc in ((-.35, -.15, .55), (.3, .05, .6), (-.02, -.45, .45)):
        x_, y_ = cx + rx * fx, cy + ry * fy
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#FFD27A" opacity=".35" filter="url(#fB8)"/>' % (n(x_ + 40 * s * sc), n(y_ + 40 * s * sc), n(40 * s * sc), n(70 * s * sc))
        g += diya_top(x_, y_, sc * s * 1.1)
    return g


def marigold(x, y, r, c1="#FFB000", c2="#E86A00", seed=0):
    rng = random.Random(seed)
    g = '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(x), n(y), n(r), c2)
    for ring_, (rr, k, c) in enumerate(((r * .95, 18, c2), (r * .78, 16, c1), (r * .58, 13, "#FFC53A"), (r * .36, 9, c1))):
        for i in range(k):
            a = 2 * math.pi * i / k + ring_ * .3 + rng.uniform(-.1, .1)
            g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" transform="rotate(%s %s %s)" fill="%s" stroke="%s" stroke-width=".8"/>' % (
                n(x + rr * .75 * math.cos(a)), n(y + rr * .75 * math.sin(a)), n(rr * .32), n(rr * .2), n(math.degrees(a)),
                n(x + rr * .75 * math.cos(a)), n(y + rr * .75 * math.sin(a)), c, c2)
    g += '<circle cx="%s" cy="%s" r="%s" fill="#FFE07A"/>' % (n(x - r * .1), n(y - r * .1), n(r * .18))
    return g


def city_skyline(y_base, rng, col="#120824", win=("#FFD27A", "#FFB347", "#FFF1B8"), height=(120, 320)):
    """row of house/building silhouettes with lit windows and tiny diyas on parapets."""
    out = []
    x = -20
    while x < 1100:
        w = rng.uniform(70, 150)
        h = rng.uniform(*height)
        top = y_base - h
        kind = rng.random()
        if kind < .3:  # dome
            out.append('<path d="M%s,%s L%s,%s C%s,%s %s,%s %s,%s Z" fill="%s"/>' % (
                n(x), n(y_base), n(x), n(top), n(x), n(top - w * .6), n(x + w), n(top - w * .6), n(x + w), n(top), col))
            out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (n(x + w), n(top), 1, n(h), col))
            out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (n(x), n(top), n(w), n(h), col))
            out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="3"/>' % (n(x + w / 2), n(top - w * .45), n(x + w / 2), n(top - w * .45 - 26), col))
        else:
            out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (n(x), n(top), n(w), n(h), col))
            if kind < .6:
                out.append('<polygon points="%s" fill="%s"/>' % (pts([(x - 6, top), (x + w / 2, top - 40), (x + w + 6, top)]), col))
        # windows
        for yy in range(int(top + 22), int(y_base - 20), 34):
            for xx in range(int(x + 14), int(x + w - 18), 26):
                if rng.random() < .55:
                    c = rng.choice(win)
                    out.append('<rect x="%s" y="%s" width="10" height="16" rx="2" fill="%s" opacity="%s"/>' % (xx, yy, c, round(rng.uniform(.6, 1), 2)))
        # string of tiny lights along the roof
        for xx in range(int(x + 6), int(x + w), 12):
            out.append('<circle cx="%s" cy="%s" r="2.2" fill="%s"/>' % (xx, n(top + 6 + 4 * math.sin(xx * .3)), rng.choice(("#FFE27A", "#FF6FA5", "#8BF1FF"))))
        x += w + rng.uniform(-10, 6)
    return '<g>%s</g>' % "".join(out)


# ================================================================= KARVA CHAUTH
def full_moon(cx, cy, r, halo=True, warm=False, seed=3):
    rng = random.Random(seed)
    c0, c1, c2 = ("#FFFDF4", "#FBF0CF", "#E9D6A4") if warm else ("#FFFFFF", "#F4F1E6", "#D8D3C2")
    g = ""
    if halo:
        hid, hd = rg([(0, "#FFF6DA", .55), (.35, "#FFF1C8", .22), (1, "#FFF1C8", 0)])
        g += '<defs>%s</defs><circle cx="%s" cy="%s" r="%s" fill="url(#%s)"/>' % (hd, n(cx), n(cy), n(r * 3.2), hid)
        g += '<circle cx="%s" cy="%s" r="%s" fill="#FFF8E4" opacity=".35" filter="url(#fB16)"/>' % (n(cx), n(cy), n(r * 1.12))
    mid, md = rg([(0, c0), (.6, c1), (1, c2)], cx=.42, cy=.4, r=.62)
    cid = uid("mc")
    g += '<defs>%s<clipPath id="%s"><circle cx="%s" cy="%s" r="%s"/></clipPath></defs>' % (md, cid, n(cx), n(cy), n(r))
    g += '<circle cx="%s" cy="%s" r="%s" fill="url(#%s)"/>' % (n(cx), n(cy), n(r), mid)
    g += '<g clip-path="url(#%s)">' % cid
    for (dx, dy, a, b, rot) in ((-.3, -.2, .34, .22, 20), (.2, -.35, .25, .16, -10), (.25, .15, .3, .2, 40), (-.1, .35, .22, .14, 0), (-.45, .2, .16, .12, 60)):
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" transform="rotate(%s %s %s)" fill="#BFB292" opacity=".38" filter="url(#fB8)"/>' % (
            n(cx + dx * r), n(cy + dy * r), n(a * r), n(b * r), rot, n(cx + dx * r), n(cy + dy * r))
    for _ in range(14):
        a, d = rng.uniform(0, 6.28), rng.uniform(0, .85) * r
        rr = rng.uniform(.02, .07) * r
        x_, y_ = cx + d * math.cos(a), cy + d * math.sin(a)
        g += '<circle cx="%s" cy="%s" r="%s" fill="#B7AB8C" opacity=".35"/><circle cx="%s" cy="%s" r="%s" fill="none" stroke="#FFFFFF" stroke-width="%s" opacity=".5"/>' % (
            n(x_), n(y_), n(rr), n(x_ - rr * .15), n(y_ - rr * .15), n(rr), n(max(.8, rr * .18)))
    g += noise(.18, "multiply", n(cx - r), n(cy - r), n(2 * r), n(2 * r))
    g += '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#8C7F62" stroke-width="%s" opacity=".25" filter="url(#fB8)"/>' % (n(cx + r * .08), n(cy + r * .08), n(r), n(r * .12))
    g += "</g>"
    return g


def channi(cx, cy, r, tilt=.82, rot=0, rim="url(#gSilver)", lace="#C8102E", mesh="#E9ECEF", see_through=True, beads="#FFD86B"):
    """sieve seen at an angle (ellipse rx=r*tilt, ry=r) rotated by rot degrees; rim with red gota lace and a small handle ring."""
    rx, ry = r * tilt, r
    cid = uid("ch")
    g = '<g transform="rotate(%s %s %s)">' % (rot, n(cx), n(cy))
    g += '<defs><clipPath id="%s"><ellipse cx="%s" cy="%s" rx="%s" ry="%s"/></clipPath></defs>' % (cid, n(cx), n(cy), n(rx * .9), n(ry * .9))
    # outer decorative lace (scallops) beyond rim
    for i in range(36):
        a = 2 * math.pi * i / 36
        x_, y_ = cx + rx * 1.1 * math.cos(a), cy + ry * 1.1 * math.sin(a)
        g += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(x_), n(y_), n(r * .065), lace)
        g += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(x_), n(y_), n(r * .025), beads)
    # mesh area
    if not see_through:
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#2B2B35" opacity=".45"/>' % (n(cx), n(cy), n(rx * .9), n(ry * .9))
    else:
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#FFFFFF" opacity=".08"/>' % (n(cx), n(cy), n(rx * .9), n(ry * .9))
    step = r / 11.0
    lines = []
    k = -r
    while k <= r:
        lines.append('<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (n(cx - r), n(cy + k), n(cx + r), n(cy + k)))
        lines.append('<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % (n(cx + k * tilt), n(cy - r), n(cx + k * tilt), n(cy + r)))
        k += step
    g += '<g clip-path="url(#%s)" stroke="%s" stroke-width="%s" opacity=".7">%s</g>' % (cid, mesh, n(max(1, r / 150)), "".join(lines))
    # rim (thick band) + inner shadow
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (n(cx), n(cy), n(rx * .95), n(ry * .95), rim, n(r * .1))
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="#FFFFFF" stroke-width="%s" opacity=".6"/>' % (n(cx), n(cy), n(rx * .99), n(ry * .99), n(r * .015))
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="#000" stroke-width="%s" opacity=".25"/>' % (n(cx), n(cy), n(rx * .9), n(ry * .9), n(r * .02))
    # gold band with red rhombus inlay
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="url(#gGoldH)" stroke-width="%s"/>' % (n(cx), n(cy), n(rx * 1.02), n(ry * 1.02), n(r * .04))
    for i in range(24):
        a = 2 * math.pi * (i + .5) / 24
        x_, y_ = cx + rx * .95 * math.cos(a), cy + ry * .95 * math.sin(a)
        g += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(x_), n(y_), n(r * .022), lace)
    g += "</g>"
    return g


def karwa(cx, base_y, s=1, body="clay", paint="#FFF3D6", paint2="#C8102E", lid_diya=True):
    """karwa pot with spout (tonti), painted belly, lid with a small diya. ~ 300*s tall incl. flame."""
    grad = {"clay": "url(#gClay)", "brass": "url(#gBrass)"}.get(body, body)
    g = '<g transform="translate(%s %s) scale(%s)">' % (n(cx), n(base_y), s)
    g += '<ellipse cx="0" cy="4" rx="110" ry="14" fill="#000" opacity=".35" filter="url(#fB8)"/>'
    # spout
    g += '<path d="M60,-110 C95,-128 118,-160 128,-196 L144,-190 C132,-150 110,-104 72,-78Z" fill="%s"/>' % grad
    g += '<ellipse cx="136" cy="-193" rx="10" ry="5" transform="rotate(20 136 -193)" fill="#3A1406"/>'
    # belly
    g += '<path d="M-40,-196 C-44,-176 -112,-160 -112,-96 C-112,-34 -64,0 0,0 C64,0 112,-34 112,-96 C112,-160 44,-176 40,-196Z" fill="%s"/>' % grad
    # neck & rim
    g += '<path d="M-40,-196 L40,-196 L46,-214 L-46,-214Z" fill="%s"/>' % grad
    g += '<ellipse cx="0" cy="-214" rx="54" ry="11" fill="%s"/><ellipse cx="0" cy="-214" rx="40" ry="6" fill="#3A1406"/>' % grad
    # painted decoration
    g += '<path d="M-104,-120 C-60,-100 60,-100 104,-120" fill="none" stroke="%s" stroke-width="6"/>' % paint2
    g += '<path d="M-106,-110 C-60,-90 60,-90 106,-110" fill="none" stroke="%s" stroke-width="2.5" stroke-dasharray="2 7" stroke-linecap="round"/>' % paint
    for i in range(7):
        x_ = -72 + i * 24
        y_ = -72 + abs(x_) * .12
        g += '<path d="M%s,%s c-10,-14 -10,-26 0,-34 c10,8 10,20 0,34Z" fill="%s"/>' % (n(x_), n(y_), paint)
        g += '<circle cx="%s" cy="%s" r="3" fill="%s"/>' % (n(x_), n(y_ - 18), paint2)
    g += '<path d="M-90,-36 C-50,-18 50,-18 90,-36" fill="none" stroke="%s" stroke-width="3"/>' % paint
    g += '<path d="M-86,-150 C-50,-136 50,-136 86,-150" fill="none" stroke="%s" stroke-width="3"/>' % paint
    # swastik mark on belly (sacred sign, drawn as graphic)
    g += '<g transform="translate(0 -168) scale(.8)" stroke="%s" stroke-width="4" fill="none" stroke-linecap="round"><path d="M0,-12 V12 M-12,0 H12 M0,-12 H10 M12,0 V10 M0,12 H-10 M-12,0 V-10"/></g>' % paint2
    # highlight
    g += '<path d="M-86,-140 C-100,-100 -92,-56 -62,-30" fill="none" stroke="#FFFFFF" stroke-width="9" opacity=".22" stroke-linecap="round"/>'
    # rice/kheel in the mouth + lid diya
    if lid_diya:
        g += '<ellipse cx="0" cy="-222" rx="56" ry="12" fill="url(#gClay)"/>'
        g += '<ellipse cx="0" cy="-226" rx="44" ry="7" fill="#F7EBD0"/>'
    g += "</g>"
    if lid_diya:
        g += diya(cx, base_y - 240 * s, .42 * s, "clay")
    return g


def thali(cx, cy, s=1, rng=None, flower="#E0115F", flower2="#FF9E1B", with_karwa=True):
    """puja thali seen at an angle: brass plate with diya, sindoor & haldi bowls, rice, flowers, mathri, small karwa."""
    rng = rng or random.Random(5)
    rx, ry = 260 * s, 95 * s
    g = '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#000" opacity=".4" filter="url(#fB16)"/>' % (n(cx), n(cy + 26 * s), n(rx), n(ry))
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#gBrass)"/>' % (n(cx), n(cy + 12 * s), n(rx), n(ry))
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#gGoldH)"/>' % (n(cx), n(cy), n(rx), n(ry))
    pid, pd = rg([(0, "#FFE9A6"), (.6, "#D9A441"), (1, "#8C5A14")], cx=.45, cy=.4, r=.6)
    g += '<defs>%s</defs><ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%s)"/>' % (pd, n(cx), n(cy), n(rx * .88), n(ry * .84), pid)
    # beaded rim
    for i in range(40):
        a = 2 * math.pi * i / 40
        g += '<circle cx="%s" cy="%s" r="%s" fill="#FFF3C4" opacity=".85"/>' % (n(cx + rx * .94 * math.cos(a)), n(cy + ry * .92 * math.sin(a)), n(3 * s))
    # engraved lotus in the centre (faint)
    g += '<g transform="translate(%s %s) scale(1 %s)" opacity=".25">%s</g>' % (n(cx), n(cy), n(ry / rx), rangoli_mini(rx * .45, "#8C5A14", "#8C5A14"))
    # rice grains
    for _ in range(90):
        a, d = rng.uniform(0, 6.28), rng.uniform(.1, .75)
        x_, y_ = cx - 60 * s + rx * .35 * d * math.cos(a), cy + 10 * s + ry * .3 * d * math.sin(a)
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" transform="rotate(%s %s %s)" fill="#FFFDF2"/>' % (n(x_), n(y_), n(3 * s), n(1.4 * s), n(rng.uniform(0, 180)), n(x_), n(y_))
    # kumkum & haldi bowls
    for bx, col in ((-150, "#C8102E"), (-95, "#F4B400")):
        x_, y_ = cx + bx * s, cy - 22 * s
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#gBrass)"/>' % (n(x_), n(y_ + 8 * s), n(26 * s), n(13 * s))
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#gGoldH)"/>' % (n(x_), n(y_), n(26 * s), n(10 * s))
        g += '<path d="M%s,%s C%s,%s %s,%s %s,%s Z" fill="%s"/>' % (n(x_ - 20 * s), n(y_ + 1 * s), n(x_ - 10 * s), n(y_ - 16 * s), n(x_ + 10 * s), n(y_ - 16 * s), n(x_ + 20 * s), n(y_ + 1 * s), col)
    # mathri (round fried snacks) stack
    for i, (mx, my) in enumerate(((120, 30), (160, 12), (140, -8), (100, 6))):
        x_, y_ = cx + mx * s, cy + my * s
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#D9A55A" stroke="#A8702E" stroke-width="%s"/>' % (n(x_), n(y_), n(26 * s), n(11 * s), n(1.5 * s))
        for _ in range(5):
            g += '<circle cx="%s" cy="%s" r="%s" fill="#8A5620" opacity=".7"/>' % (n(x_ + rng.uniform(-16, 16) * s), n(y_ + rng.uniform(-5, 5) * s), n(1.4 * s))
    # flowers
    for fx, fy, c in ((-190, 30, flower), (-40, 55, flower2), (190, -30, flower), (60, 60, flower2), (-120, 60, flower2)):
        g += rose_top(cx + fx * s, cy + fy * s, 16 * s, c)
    if with_karwa:
        g += karwa(cx + 20 * s, cy - 10 * s, .38 * s, lid_diya=False)
    g += diya(cx - 30 * s, cy + 20 * s, .55 * s, "brass")
    return g


def rose_top(x, y, r, col):
    g = '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(x), n(y), n(r), col)
    for k, rr in enumerate((r * .8, r * .55, r * .32)):
        g += '<path d="M%s,%s a%s,%s 0 1,1 %s,0" fill="none" stroke="#000" stroke-opacity=".28" stroke-width="%s" transform="rotate(%s %s %s)"/>' % (
            n(x - rr), n(y), n(rr), n(rr), n(2 * rr), n(max(1, r * .08)), k * 70, n(x), n(y))
    g += '<circle cx="%s" cy="%s" r="%s" fill="#fff" opacity=".18"/>' % (n(x - r * .3), n(y - r * .35), n(r * .35))
    return g


def gota_band(x, y, w, h, base=("#B3001B", "#7A0012"), horizontal=True, rng=None, scallop="both"):
    """red silk chunri band with gold gota lace edges and zari butis."""
    rng = rng or random.Random(7)
    gid, gd = lg([(0, base[0]), (1, base[1])], 0, 0, 0 if horizontal else 1, 1 if horizontal else 0)
    g = '<defs>%s</defs><rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)"/>' % (gd, n(x), n(y), n(w), n(h), gid)
    L = w if horizontal else h
    sc = 22
    cnt = int(L / sc) + 1
    edges = []
    if scallop in ("both", "a"):
        edges.append(0)
    if scallop in ("both", "b"):
        edges.append(1)
    for e in edges:
        if horizontal:
            yy = y + (h if e else 0)
            g += '<rect x="%s" y="%s" width="%s" height="8" fill="url(#gGoldH)"/>' % (n(x), n(yy - (8 if e else 0)), n(w))
            d = "M%s,%s " % (n(x), n(yy))
            for i in range(cnt):
                d += "a%s,%s 0 0,%s %s,0 " % (sc / 2, sc / 2 * .9, 0 if e else 1, sc)
            g += '<path d="%s" fill="url(#gGoldV)" transform="%s"/>' % (d, "")
            for i in range(cnt):
                g += '<circle cx="%s" cy="%s" r="2.6" fill="#FFF3C4"/>' % (n(x + sc / 2 + i * sc), n(yy + (5 if e else -5)))
        else:
            xx = x + (w if e else 0)
            g += '<rect x="%s" y="%s" width="8" height="%s" fill="url(#gGoldV)"/>' % (n(xx - (8 if e else 0)), n(y), n(h))
            d = "M%s,%s " % (n(xx), n(y))
            for i in range(cnt):
                d += "a%s,%s 0 0,%s 0,%s " % (sc / 2 * .9, sc / 2, 1 if e else 0, sc)
            g += '<path d="%s" fill="url(#gGold)"/>' % d
            for i in range(cnt):
                g += '<circle cx="%s" cy="%s" r="2.6" fill="#FFF3C4"/>' % (n(xx + (5 if e else -5)), n(y + sc / 2 + i * sc))
    # zari butis (small leaf/dot motifs) in a lattice
    if (h if horizontal else w) > 40:
        step = 46
        a0, a1 = (x, x + w) if horizontal else (y, y + h)
        b0, b1 = (y + 16, y + h - 16) if horizontal else (x + 16, x + w - 16)
        rows = max(1, int((b1 - b0) / step))
        for j in range(rows):
            bb = b0 + (b1 - b0) * (j + .5) / rows
            off = (j % 2) * step / 2
            t = a0 + step / 2 + off
            while t < a1:
                px, py = (t, bb) if horizontal else (bb, t)
                g += '<g transform="translate(%s %s)"><path d="M0,-8 C5,-3 5,3 0,8 C-5,3 -5,-3 0,-8Z" fill="url(#gGold)"/><circle cx="8" cy="0" r="1.8" fill="#FFE9A6"/><circle cx="-8" cy="0" r="1.8" fill="#FFE9A6"/></g>' % (n(px), n(py))
                t += step
    return g


def mehendi_hand(x, y, s=1, rot=0, mirror=False, skin=("#F1C29A", "#D99A6C", "#B97448"), ink="#7A2E0E", bangles=("#C8102E", "#FFB000", "#C8102E")):
    """open palm facing viewer, fingers up, with detailed mehendi and a stack of bangles; (x,y) = wrist centre. ~260x520 at s=1."""
    sx = -1 if mirror else 1
    gid, gd = lg([(0, skin[0]), (.7, skin[1]), (1, skin[2])], 0, 0, 1, 1)
    hid = uid("hc")
    # finger geometry: (base x, base y, length, width, angle)
    fingers = [(-62, -250, 118, 40, -8), (-20, -262, 142, 42, -2), (22, -258, 134, 41, 4), (60, -240, 104, 37, 11)]
    palm = "M-86,-10 C-92,-80 -96,-170 -84,-236 C-60,-262 60,-262 84,-232 C94,-170 92,-80 84,-10 Z"
    thumb = '<rect x="-24" y="-120" width="48" height="128" rx="24" transform="translate(-92 -92) rotate(-38)"/>'
    shape = '<path d="%s"/>%s%s' % (palm, thumb, "".join(
        '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" transform="rotate(%s %s %s)"/>' % (
            n(bx - fw / 2), n(by - ln), n(fw), n(ln + 30), n(fw / 2), a, bx, by) for bx, by, ln, fw, a in fingers))
    g = '<g transform="translate(%s %s) rotate(%s) scale(%s %s)">' % (n(x), n(y), rot, n(sx * s), n(s))
    g += '<defs>%s<clipPath id="%s">%s</clipPath></defs>' % (gd, hid, shape)
    # wrist / forearm
    g += '<path d="M-78,-20 L78,-20 L86,200 L-86,200Z" fill="url(#%s)"/>' % gid
    g += '<g fill="url(#%s)">%s</g>' % (gid, shape)
    # shading between fingers
    m = []
    for bx, by, ln, fw, a in fingers:
        tipx = bx + math.sin(math.radians(a)) * (ln - fw * .4)
        tipy = by - math.cos(math.radians(a)) * (ln - fw * .4)
        # fingertip caps
        m.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(tipx), n(tipy), n(fw * .52), ink))
        # knuckle bands
        for t, kind in ((.38, 0), (.7, 1)):
            px = bx + math.sin(math.radians(a)) * ln * t
            py = by - math.cos(math.radians(a)) * ln * t
            m.append('<g transform="translate(%s %s) rotate(%s)">' % (n(px), n(py), a))
            if kind == 0:
                m.append('<path d="M%s,0 H%s M%s,7 H%s" stroke="%s" stroke-width="2.4"/>' % (n(-fw / 2), n(fw / 2), n(-fw / 2), n(fw / 2), ink))
                m.append("".join('<circle cx="%s" cy="-7" r="2.2" fill="%s"/>' % (n(k), ink) for k in (-12, -4, 4, 12)))
            else:
                m.append('<path d="M%s,0 L0,-12 L%s,0 L0,12Z" fill="none" stroke="%s" stroke-width="2.2"/><circle r="3" fill="%s"/>' % (n(-fw * .36), n(fw * .36), ink, ink))
            m.append("</g>")
    # palm mandala
    mand = '<g transform="translate(0 -128)">'
    mand += '<circle r="44" fill="none" stroke="%s" stroke-width="3"/>' % ink
    mand += '<circle r="18" fill="%s"/>' % ink + '<circle r="8" fill="%s"/>' % skin[0]
    mand += _around(12, '<path d="%s" fill="none" stroke="%s" stroke-width="2.2"/>' % (petal_path(20, 42, 7), ink))
    mand += _around(16, '<path d="%s" fill="%s"/>' % (petal_path(46, 66, 6, "round"), ink))
    mand += _around(32, '<circle cx="0" cy="-72" r="2.4" fill="%s"/>' % ink)
    mand += '</g>'
    m.append(mand)
    # palm lower: net + wrist bands
    m.append('<path d="M-80,-40 C-40,-58 40,-58 80,-40" fill="none" stroke="%s" stroke-width="3"/>' % ink)
    m.append('<path d="M-80,-30 C-40,-48 40,-48 80,-30" fill="none" stroke="%s" stroke-width="1.8" stroke-dasharray="3 5"/>' % ink)
    for k in range(-3, 4):
        m.append('<path d="M%s,-44 c-8,-14 -8,-22 0,-30 c8,8 8,16 0,30Z" fill="%s"/>' % (k * 22, ink))
    # thumb vine
    m.append('<path d="M-150,-170 C-128,-150 -112,-132 -90,-110" fill="none" stroke="%s" stroke-width="2.4"/>' % ink)
    for t in range(4):
        px, py = -148 + t * 15, -166 + t * 14
        m.append('<path d="M%s,%s c10,-10 18,-8 20,0 c-8,6 -14,6 -20,0Z" fill="%s"/>' % (n(px), n(py), ink))
    # side paisley
    m.append('<path d="M60,-60 C90,-80 88,-130 62,-140 C40,-146 34,-120 50,-112 C64,-106 64,-86 60,-60Z" fill="none" stroke="%s" stroke-width="2.4"/>' % ink)
    m.append('<path d="M-66,-190 C-40,-205 40,-205 66,-190" fill="none" stroke="%s" stroke-width="2.2"/>' % ink)
    m.append(_around(1, "") )
    g += '<g clip-path="url(#%s)">%s</g>' % (hid, "".join(m))
    # wrist mehendi bracelet
    g += '<path d="M-80,10 C-40,0 40,0 80,10" fill="none" stroke="%s" stroke-width="3"/>' % ink
    g += "".join('<circle cx="%s" cy="18" r="3" fill="%s"/>' % (k, ink) for k in range(-70, 71, 14))
    g += '<path d="M-82,30 C-40,20 40,20 82,30" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="6 4"/>' % ink
    # bangles
    for i in range(9):
        yy = 60 + i * 14
        col = bangles[i % len(bangles)]
        if i in (0, 8):
            col = "url(#gGoldH)"
        g += '<ellipse cx="0" cy="%s" rx="%s" ry="16" fill="none" stroke="%s" stroke-width="12"/>' % (yy, 92 + i * .6, col)
        g += '<ellipse cx="0" cy="%s" rx="%s" ry="16" fill="none" stroke="#FFFFFF" stroke-width="2" opacity=".45" stroke-dasharray="20 40"/>' % (yy - 3, 92 + i * .6)
    g += "</g>"
    return g


def bangle_stack(cx, cy, s=1, cols=("#C8102E", "#FFB000", "#0F7B3F", "#C8102E"), count=9, tilt=.28):
    """a stack of glass bangles lying on their side (seen at an angle)."""
    g = '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#000" opacity=".35" filter="url(#fB8)"/>' % (n(cx), n(cy + 20 * s), n(130 * s), n(30 * s))
    for i in range(count):
        yy = cy - i * 13 * s
        col = cols[i % len(cols)] if i not in (0, count - 1) else "url(#gGoldH)"
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (n(cx), n(yy), n(110 * s), n(110 * s * tilt), col, n(12 * s))
        g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="#FFFFFF" stroke-width="%s" opacity=".5" stroke-dasharray="%s %s"/>' % (
            n(cx), n(yy - 3 * s), n(110 * s), n(110 * s * tilt), n(2 * s), n(30 * s), n(60 * s))
        if col == "url(#gGoldH)":
            for k in range(20):
                a = 2 * math.pi * k / 20
                g += '<circle cx="%s" cy="%s" r="%s" fill="#FFF3C4"/>' % (n(cx + 110 * s * math.cos(a)), n(yy + 110 * s * tilt * math.sin(a)), n(2.2 * s))
    return g


def woman_moon(x, base, s=1, fill="#1A0B24", rim="#FFE7A8", zari="url(#gGoldH)", facing=1, chunri="#8E0F2A"):
    """woman in saree, profile, head covered, both hands raising a channi towards the upper right. (x,base) = feet.
    Returns (svg, channi_centre)."""
    f = facing
    T = lambda px, py: (x + f * px * s, base + py * s)
    g = '<g transform="translate(%s %s) scale(%s %s)">' % (n(x), n(base), n(f * s), n(s))
    body = ("M72,0 C66,-60 58,-150 52,-250 C48,-320 44,-380 40,-430 C52,-452 64,-480 64,-508 "
            "C64,-540 50,-560 36,-574 C30,-580 28,-592 34,-600 "
            "L44,-606 C48,-614 50,-620 48,-628 L56,-640 C58,-646 52,-652 46,-656 "
            "C46,-672 40,-692 26,-706 C8,-722 -24,-724 -44,-708 "
            "C-66,-690 -78,-660 -84,-620 C-96,-560 -110,-480 -122,-400 C-128,-360 -126,-330 -112,-320 "
            "C-96,-312 -80,-330 -70,-360 C-72,-300 -78,-200 -84,-100 C-88,-60 -96,-20 -104,0 Z")
    g += '<path d="%s" fill="%s"/>' % (body, fill)
    # chunri over head (slightly lighter so it reads) with zari border along its front edge
    ch = ("M26,-706 C8,-722 -24,-724 -44,-708 C-66,-690 -78,-660 -84,-620 C-96,-560 -110,-480 -122,-400 "
          "C-128,-360 -126,-330 -112,-320 C-96,-312 -80,-330 -70,-360 C-66,-420 -52,-500 -30,-560 "
          "C-12,-610 10,-640 38,-660 C40,-680 36,-694 26,-706Z")
    g += '<path d="%s" fill="%s"/>' % (ch, chunri)
    g += '<path d="M38,-660 C10,-640 -12,-610 -30,-560 C-52,-500 -66,-420 -70,-360 C-80,-330 -96,-312 -112,-320" fill="none" stroke="%s" stroke-width="7"/>' % zari
    g += '<path d="M40,-668 C30,-700 0,-722 -36,-712" fill="none" stroke="%s" stroke-width="5"/>' % zari
    # zari dots over chunri
    for (px, py) in ((-60, -640), (-80, -560), (-96, -480), (-40, -680), (-104, -400), (-70, -600), (-86, -520)):
        g += '<circle cx="%s" cy="%s" r="3" fill="#FFD86B" opacity=".9"/>' % (px, py)
    # saree pleats and pallu lines (subtle)
    g += '<path d="M20,-400 C26,-300 34,-160 40,0 M0,-390 C4,-300 8,-160 10,0" fill="none" stroke="%s" stroke-width="2" opacity=".25"/>' % rim
    g += '<path d="M-60,-330 C-40,-300 20,-280 50,-250" fill="none" stroke="%s" stroke-width="10" opacity=".9"/>' % zari
    g += '<path d="M-100,0 L72,0" stroke="%s" stroke-width="8"/>' % zari
    # arms: upper arm and forearm raised forward
    g += '<path d="M10,-560 C40,-560 70,-575 92,-600 L108,-630 L120,-626 L106,-592 C84,-560 50,-540 16,-534Z" fill="%s"/>' % fill
    g += '<path d="M0,-548 C36,-540 66,-560 88,-590 L100,-624 L112,-618 L100,-584 C80,-548 44,-526 4,-526Z" fill="%s" opacity=".92"/>' % fill
    # bangles
    for k in range(4):
        g += '<path d="M%s,%s l10,5" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (86 + k * 3, -596 - k * 6, "#FFD86B")
    # rim light along the front profile
    g += ('<path d="M34,-600 L44,-606 C48,-614 50,-620 48,-628 L56,-640 C58,-646 52,-652 46,-656 C46,-672 40,-692 26,-706" '
          'fill="none" stroke="%s" stroke-width="3" opacity=".85" stroke-linecap="round"/>') % rim
    g += '<path d="M64,-508 C64,-480 52,-452 40,-430 C44,-380 48,-320 52,-250 C58,-150 66,-60 72,0" fill="none" stroke="%s" stroke-width="2.4" opacity=".55"/>' % rim
    # nose ring / bindi hints
    g += '<circle cx="50" cy="-636" r="4" fill="none" stroke="#FFD86B" stroke-width="1.6"/>'
    g += "</g>"
    return g, T(172, -640)


def woman_moon(x, base, s=1, fill="#1A0B24", rim="#FFE7A8", zari="url(#gGoldH)", facing=1, chunri="#9E0F2E",
               chunri2="#6E0A20", sieve_rim="url(#gSilver)", thali_diya=True):
    """woman in saree (profile, facing right when facing=1), head covered with a red-gold chunri, one hand raising
    the channi in front of her face towards the moon, the other holding a small diya thali. (x, base) = feet."""
    g = '<g transform="translate(%s %s) scale(%s %s)">' % (n(x), n(base), n(facing * s), n(s))
    fid, fd = lg([(0, fill), (.55, fill), (1, "#000000")], 1, 0, 0, 0)
    cid, cd = lg([(0, chunri), (1, chunri2)], 1, 0, 0, 1)
    g += "<defs>%s%s</defs>" % (fd, cd)
    body = ("M-5,-682 C14,-684 30,-674 36,-662 C40,-652 42,-644 43,-636 C48,-628 54,-622 57,-617 C58,-613 52,-611 47,-610 "
            "C48,-606 48,-603 46,-601 C47,-598 47,-595 45,-592 C44,-586 42,-580 38,-577 C32,-574 26,-572 22,-568 "
            "C22,-556 24,-546 28,-536 C44,-520 52,-500 54,-478 C54,-462 48,-452 40,-446 C34,-430 30,-418 30,-404 "
            "C36,-340 50,-240 60,-140 C66,-80 76,-30 88,0 L-94,0 C-80,-60 -66,-160 -58,-260 C-52,-320 -50,-360 -50,-390 "
            "C-44,-420 -36,-450 -38,-480 C-40,-500 -36,-520 -30,-532 C-46,-560 -56,-600 -52,-636 C-46,-664 -28,-682 -5,-682Z")
    g += '<path d="%s" fill="url(#%s)"/>' % (body, fid)
    # saree folds and hem
    g += '<path d="M8,-400 C14,-300 22,-160 30,0 M-14,-396 C-12,-300 -8,-160 -6,0 M-34,-392 C-34,-300 -34,-160 -36,0" fill="none" stroke="%s" stroke-width="1.6" opacity=".22"/>' % rim
    g += '<path d="M-94,-4 C-30,2 30,2 88,-4" fill="none" stroke="%s" stroke-width="10"/>' % zari
    g += '<path d="M-90,-20 C-30,-14 30,-14 84,-20" fill="none" stroke="%s" stroke-width="2.4" stroke-dasharray="2 8" stroke-linecap="round"/>' % "#FFD86B"
    # pallu crossing the waist
    g += '<path d="M40,-446 C10,-420 -30,-400 -60,-360 L-54,-338 C-26,-380 12,-404 36,-420Z" fill="url(#%s)"/>' % cid
    g += '<path d="M40,-446 C10,-420 -30,-400 -60,-360" fill="none" stroke="%s" stroke-width="5"/>' % zari
    # chunri over head, falling down the back
    ch = ("M38,-664 C30,-684 6,-694 -16,-690 C-44,-686 -62,-664 -70,-636 C-82,-590 -94,-520 -104,-450 "
          "C-110,-410 -114,-380 -116,-350 C-104,-344 -86,-344 -72,-350 C-60,-400 -46,-470 -34,-530 "
          "C-26,-570 -12,-610 6,-636 C16,-650 28,-660 38,-664Z")
    g += '<path d="%s" fill="url(#%s)"/>' % (ch, cid)
    g += '<path d="M38,-664 C28,-660 16,-650 6,-636 C-12,-610 -26,-570 -34,-530 C-46,-470 -60,-400 -72,-350" fill="none" stroke="%s" stroke-width="7"/>' % zari
    g += '<path d="M-72,-350 C-86,-344 -104,-344 -116,-350" fill="none" stroke="%s" stroke-width="7"/>' % zari
    for i in range(8):
        t = i / 7.0
        g += '<circle cx="%s" cy="%s" r="3.4" fill="#FFD86B"/>' % (n(-116 + 44 * t), n(-338 + 6 * math.sin(t * 3.14)))
    rngz = random.Random(4)
    for _ in range(26):
        t = rngz.uniform(.05, .95)
        px = -30 - 60 * t + rngz.uniform(-18, 18)
        py = -660 + 300 * t
        g += '<circle cx="%s" cy="%s" r="%s" fill="#FFD86B" opacity=".85"/>' % (n(px), n(py), n(rngz.uniform(1.6, 3)))
    # jewellery: maang tikka, nath, earring
    g += '<circle cx="30" cy="-652" r="4.5" fill="url(#gGold)"/><circle cx="52" cy="-612" r="5" fill="none" stroke="#FFD86B" stroke-width="1.6"/>'
    # far arm raising the channi
    g += '<path d="M-6,-520 C20,-530 44,-540 62,-556 C74,-570 84,-590 90,-612" fill="none" stroke="%s" stroke-width="24" stroke-linecap="round"/>' % fill
    g += '<path d="M-6,-520 C20,-530 44,-540 62,-556 C74,-570 84,-590 90,-612" fill="none" stroke="%s" stroke-width="2" opacity=".5" transform="translate(0 -11)"/>' % rim
    g += "</g>"
    # channi (in card coords) held in front of the face
    ccx, ccy = x + facing * 128 * s, base - 628 * s
    g += channi(ccx, ccy, 74 * s, tilt=.46, rot=-8 * facing, rim=sieve_rim)
    g += '<g transform="translate(%s %s) scale(%s %s)">' % (n(x), n(base), n(facing * s), n(s))
    g += '<ellipse cx="92" cy="-616" rx="11" ry="15" fill="%s"/>' % fill  # hand gripping rim
    for k in range(4):
        g += '<path d="M%s,%s l12,4" stroke="#FFD86B" stroke-width="3" stroke-linecap="round"/>' % (n(76 + k * 2.5), n(-586 - k * 6))
    # near arm with the diya thali
    if thali_diya:
        g += '<path d="M-2,-512 C4,-480 10,-458 22,-448 C38,-440 56,-452 70,-462" fill="none" stroke="%s" stroke-width="24" stroke-linecap="round"/>' % fill
        for k in range(4):
            g += '<path d="M%s,%s l3,-12" stroke="#FFD86B" stroke-width="3" stroke-linecap="round"/>' % (n(44 + k * 5), n(-446 - k * 2))
        g += '<ellipse cx="86" cy="-470" rx="52" ry="11" fill="url(#gBrass)"/><ellipse cx="86" cy="-474" rx="46" ry="8" fill="url(#gGoldH)"/>'
    # rim light along the profile
    g += ('<path d="M36,-662 C40,-652 42,-644 43,-636 C48,-628 54,-622 57,-617 C58,-613 52,-611 47,-610 C48,-606 48,-603 46,-601 '
          'C47,-598 47,-595 45,-592 C44,-586 42,-580 38,-577" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round" opacity=".9"/>') % rim
    g += '<path d="M28,-536 C44,-520 52,-500 54,-478 C54,-462 48,-452 40,-446 M30,-404 C36,-340 46,-240 54,-140 C58,-80 62,-30 70,0" fill="none" stroke="%s" stroke-width="2.2" opacity=".55"/>' % rim
    g += "</g>"
    if thali_diya:
        g += diya(x + facing * 84 * s, base - 480 * s, .3 * s, "brass", glow_r=90 * s)
    return g, (ccx, ccy)


# ================================================================= SHRADDHANJALI
def _bez(p0, p1, p2, p3, k=24):
    out = []
    for i in range(k + 1):
        t = i / float(k)
        a = (1 - t) ** 3; b = 3 * (1 - t) ** 2 * t; c = 3 * (1 - t) * t * t; d = t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def shape_d(shape, x, y, w, h, pad=0):
    """SVG path matching the engine's photo shape (static/cards.js), grown by pad."""
    x, y, w, h = x - pad, y - pad, w + 2 * pad, h + 2 * pad
    if shape == "rect":
        return "M%s,%s h%s v%s h%s Z" % (n(x), n(y), n(w), n(h), n(-w))
    if shape in ("rounded", "pill"):
        r = 28 + pad if shape == "rounded" else min(w, h) / 2
        return "M%s,%s h%s a%s,%s 0 0 1 %s,%s v%s a%s,%s 0 0 1 %s,%s h%s a%s,%s 0 0 1 %s,%s v%s a%s,%s 0 0 1 %s,%s Z" % (
            n(x + r), n(y), n(w - 2 * r), n(r), n(r), n(r), n(r), n(h - 2 * r), n(r), n(r), n(-r), n(r), n(-(w - 2 * r)),
            n(r), n(r), n(-r), n(-r), n(-(h - 2 * r)), n(r), n(r), n(r), n(-r))
    if shape == "oval":
        return "M%s,%s a%s,%s 0 1 0 %s,0 a%s,%s 0 1 0 %s,0 Z" % (n(x), n(y + h / 2), n(w / 2), n(h / 2), n(w), n(w / 2), n(h / 2), n(-w))
    if shape == "arch":
        cx, sh = x + w / 2, y + h * .34
        return ("M%s,%s L%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s L%s,%s Z") % (
            n(x), n(y + h), n(x), n(sh), n(x), n(sh - h * .12), n(x + w * .18), n(y + h * .1), n(cx - w * .1), n(y + h * .045),
            n(cx - w * .04), n(y + h * .02), n(cx), n(y + h * .01), n(cx), n(y),
            n(cx), n(y + h * .01), n(cx + w * .04), n(y + h * .02), n(cx + w * .1), n(y + h * .045),
            n(x + w - w * .18), n(y + h * .1), n(x + w), n(sh - h * .12), n(x + w), n(sh), n(x + w), n(y + h))
    raise ValueError(shape)


def shape_pts(shape, x, y, w, h, pad=0, step=10):
    """points along the outline (clockwise from bottom-left for arch, top-left otherwise), evenly resampled."""
    x, y, w, h = x - pad, y - pad, w + 2 * pad, h + 2 * pad
    P = []
    if shape == "rect":
        P = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
    elif shape in ("rounded", "pill"):
        r = 28 + pad if shape == "rounded" else min(w, h) / 2
        def arc(cx, cy, a0, a1):
            return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / 12.0)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / 12.0))) for i in range(13)]
        P = arc(x + r, y + r, 180, 270) + arc(x + w - r, y + r, 270, 360) + arc(x + w - r, y + h - r, 0, 90) + arc(x + r, y + h - r, 90, 180)
        P.append(P[0])
    elif shape == "oval":
        P = [(x + w / 2 + w / 2 * math.cos(math.pi + 2 * math.pi * i / 120.0), y + h / 2 + h / 2 * math.sin(math.pi + 2 * math.pi * i / 120.0)) for i in range(121)]
    elif shape == "arch":
        cx, sh = x + w / 2, y + h * .34
        P = [(x, y + h), (x, sh)]
        P += _bez((x, sh), (x, sh - h * .12), (x + w * .18), (cx - w * .1, y + h * .045)) if False else []
        P += _bez((x, sh), (x, sh - h * .12), (x + w * .18, y + h * .1), (cx - w * .1, y + h * .045))
        P += _bez((cx - w * .1, y + h * .045), (cx - w * .04, y + h * .02), (cx, y + h * .01), (cx, y))
        P += _bez((cx, y), (cx, y + h * .01), (cx + w * .04, y + h * .02), (cx + w * .1, y + h * .045))
        P += _bez((cx + w * .1, y + h * .045), (x + w - w * .18, y + h * .1), (x + w, sh - h * .12), (x + w, sh))
        P += [(x + w, y + h), (x, y + h)]
    # resample
    out = [P[0]]
    acc = 0.0
    for i in range(1, len(P)):
        (ax, ay), (bx, by) = P[i - 1], P[i]
        seg = math.hypot(bx - ax, by - ay)
        if seg == 0:
            continue
        t = step - acc
        while t <= seg:
            out.append((ax + (bx - ax) * t / seg, ay + (by - ay) * t / seg))
            t += step
        acc = (acc + seg) % step
    return out


def jasmine(x, y, r, rot=0, col="#FFFFFF", shade="#E4E0D4", center="#EFE3B8"):
    """single mogra/jasmine bloom seen from the front."""
    pet = petal_path(r * .12, r, r * .34, "round")
    g = '<g transform="translate(%s %s) rotate(%s)">' % (n(x), n(y), n(rot))
    g += _around(5, '<path d="%s" fill="%s"/>' % (pet, shade), 36)
    g += _around(5, '<path d="%s" fill="%s" stroke="%s" stroke-width=".6"/>' % (pet, col, shade))
    g += '<circle r="%s" fill="%s"/>' % (n(r * .2), center)
    return g + "</g>"


def jasmine_bud(x, y, r, rot, col="#FFFFFF", shade="#DCD6C6", tip="#E9EEDC"):
    return ('<g transform="translate(%s %s) rotate(%s)"><path d="M0,0 C%s,%s %s,%s 0,%s C%s,%s %s,%s 0,0Z" fill="%s" stroke="%s" stroke-width=".7"/>'
            '<path d="M0,%s C%s,%s %s,%s 0,%s" fill="none" stroke="%s" stroke-width="1"/></g>') % (
        n(x), n(y), n(rot), n(r * .55), n(-r * .3), n(r * .5), n(-r * 1.6), n(-r * 2.1), n(-r * .5), n(-r * 1.6), n(-r * .55), n(-r * .3),
        col, shade, n(-r * .2), n(r * .15), n(-r * .8), n(r * .12), n(-r * 1.3), n(-r * 1.8), tip)


def leaf(x, y, ln, rot, col="#8FA58A", vein="#C9D6C2"):
    return ('<g transform="translate(%s %s) rotate(%s)"><path d="M0,0 C%s,%s %s,%s 0,%s C%s,%s %s,%s 0,0Z" fill="%s"/>'
            '<path d="M0,0 L0,%s" stroke="%s" stroke-width="1"/></g>') % (
        n(x), n(y), n(rot), n(ln * .35), n(-ln * .25), n(ln * .3), n(-ln * .8), n(-ln), n(-ln * .3), n(-ln * .8), n(-ln * .35), n(-ln * .25), col, n(-ln * .9), vein)


def jasmine_garland(shape, x, y, w, h, pad=24, rng=None, thick=1.0, leaves=True, tassel=True, col="#FFFFFF", shade="#E2DDCF"):
    """dense jasmine (mogra) garland following the photo outline; optional hanging tassel at the bottom centre."""
    rng = rng or random.Random(21)
    P = shape_pts(shape, x, y, w, h, pad, step=9 / thick)
    g = ['<g filter="url(#fShadowS)">']
    base = []
    for i, (px, py) in enumerate(P):
        if leaves and i % 7 == 0:
            base.append(leaf(px + rng.uniform(-6, 6), py + rng.uniform(-6, 6), rng.uniform(16, 24) * thick, rng.uniform(0, 360)))
    g.append("".join(base))
    fl = []
    for i, (px, py) in enumerate(P):
        for k in range(2):
            ox, oy = rng.uniform(-10, 10) * thick, rng.uniform(-10, 10) * thick
            if rng.random() < .62:
                fl.append(jasmine(px + ox, py + oy, rng.uniform(9, 12.5) * thick, rng.uniform(0, 72), col, shade))
            else:
                fl.append(jasmine_bud(px + ox, py + oy, rng.uniform(5, 7) * thick, rng.uniform(0, 360), col, shade))
    g.append("".join(fl))
    g.append("</g>")
    if tassel:
        bx, by = x + w / 2, y + h + pad
        g.append(jasmine_tassel(bx, by, 1.0 * thick, rng))
    return "".join(g)


def jasmine_tassel(x, y, s=1, rng=None):
    """a knot of jasmine with 3 short hanging strands (for the bottom of a photo garland)."""
    rng = rng or random.Random(5)
    g = ""
    for dx, ln in ((-22, 70), (0, 96), (22, 70)):
        for k in range(int(ln / 10)):
            g += jasmine_bud(x + dx * s + rng.uniform(-2, 2), y + (10 + k * 10) * s, 5.5 * s, 180 + rng.uniform(-20, 20))
        g += jasmine(x + dx * s, y + (ln + 14) * s, 10 * s, 0)
    for k in range(9):
        g += jasmine(x + rng.uniform(-20, 20) * s, y + rng.uniform(-8, 10) * s, rng.uniform(10, 13) * s, rng.uniform(0, 72))
    return '<g filter="url(#fShadowS)">%s</g>' % g


def jasmine_strand(x, y0, y1, s=1, rng=None, sway=0):
    """vertical hanging jasmine string (ladi) ending in a bloom."""
    rng = rng or random.Random(int(x))
    g = '<path d="M%s,%s Q%s,%s %s,%s" stroke="#CFC8B6" stroke-width="1.2" fill="none"/>' % (n(x), n(y0), n(x + sway), n((y0 + y1) / 2), n(x), n(y1))
    y = y0 + 8
    while y < y1:
        t = (y - y0) / max(1, (y1 - y0))
        xx = x + sway * 2 * t * (1 - t) * 2
        if rng.random() < .55:
            g += jasmine(xx + rng.uniform(-2, 2), y, rng.uniform(7, 9) * s, rng.uniform(0, 72))
        else:
            g += jasmine_bud(xx, y, 5 * s, 180 + rng.uniform(-30, 30))
        y += rng.uniform(11, 14) * s
    g += jasmine(x, y1 + 8 * s, 11 * s, 10)
    return g


def rajnigandha_rope(shape, x, y, w, h, pad=24, rng=None, s=1.0, tassel=True):
    """tuberose (rajnigandha) rope garland: long white buds laid in a braided pattern along the outline."""
    rng = rng or random.Random(33)
    P = shape_pts(shape, x, y, w, h, pad, step=7)
    g = ['<g filter="url(#fShadowS)">']
    for i in range(len(P) - 1):
        (ax, ay), (bx, by) = P[i], P[(i + 1) % len(P)]
        ang = math.degrees(math.atan2(by - ay, bx - ax))
        for side in (-1, 1):
            rot = ang + 90 + side * 55 + rng.uniform(-10, 10)
            col = "#FFFFFF" if rng.random() < .8 else "#F2F4E6"
            g.append(jasmine_bud(ax + side * 3, ay, rng.uniform(6.5, 8.5) * s, rot, col, "#D8D2C0", "#DDE6C8"))
        if i % 9 == 0:
            g.append(jasmine(ax, ay, 8 * s, rng.uniform(0, 72), "#FFFFFF", "#DAD4C2"))
    g.append("</g>")
    if tassel:
        g.append(jasmine_tassel(x + w / 2, y + h + pad, s, rng))
    return "".join(g)


def sandal_garland(shape, x, y, w, h, pad=22, s=1.0, bead="#B08A62"):
    """sukhad (sandalwood bead) garland along the outline, muted brown beads with gold spacers and a tassel."""
    P = shape_pts(shape, x, y, w, h, pad, step=15 * s)
    bid, bd = rg([(0, "#E3C9A4"), (.55, bead), (1, "#6D5238")], cx=.38, cy=.35, r=.7)
    g = '<defs>%s</defs><g filter="url(#fShadowS)">' % bd
    for i, (px, py) in enumerate(P):
        if i % 6 == 0:
            g += '<circle cx="%s" cy="%s" r="%s" fill="url(#gMGold)"/>' % (n(px), n(py), n(4.5 * s))
        else:
            g += '<circle cx="%s" cy="%s" r="%s" fill="url(#%s)"/>' % (n(px), n(py), n(7.2 * s), bid)
    g += "</g>"
    return g


def frame(shape, x, y, w, h, style="wood", pad=0, width=26):
    """refined moulding frame drawn around the photo shape: wood | mgold | marble | silver."""
    grads = {"wood": ("#5A4636", "#8A7058", "#3A2C22"), "mgold": ("#8C7A55", "#E6D8B2", "#6F603F"),
             "marble": ("#E9E6DF", "#FFFFFF", "#C9C4BA"), "silver": ("#9A9C9A", "#EEEFEC", "#7E817F")}[style]
    fid, fd = lg([(0, grads[0]), (.45, grads[1]), (1, grads[2])], 0, 0, 1, 1)
    outer = shape_d(shape, x, y, w, h, pad + width)
    inner = shape_d(shape, x, y, w, h, pad)
    g = '<defs>%s</defs>' % fd
    g += '<path d="%s %s" fill="url(#%s)" fill-rule="evenodd" filter="url(#fShadowSoft)"/>' % (outer, inner, fid)
    g += '<path d="%s" fill="none" stroke="url(#gMGold)" stroke-width="3"/>' % shape_d(shape, x, y, w, h, pad + 4)
    g += '<path d="%s" fill="none" stroke="#FFFFFF" stroke-width="1.4" opacity=".45"/>' % shape_d(shape, x, y, w, h, pad + width - 5)
    g += '<path d="%s" fill="none" stroke="#000" stroke-width="2" opacity=".18"/>' % shape_d(shape, x, y, w, h, pad + width)
    return g


def photo_placeholder(shape, x, y, w, h, bg=("#EFEBE3", "#DCD6CB"), fig="#CFC7BA"):
    """soft neutral fill + faint bust silhouette, shown when no photo is added."""
    pid, pd = lg([(0, bg[0]), (1, bg[1])], 0, 0, 0, 1)
    cid = uid("pc")
    cx, cy = x + w / 2, y + h / 2
    r = min(w, h) / 2
    g = '<defs>%s<clipPath id="%s"><path d="%s"/></clipPath></defs>' % (pd, cid, shape_d(shape, x, y, w, h))
    g += '<g clip-path="url(#%s)"><rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)"/>' % (cid, n(x), n(y), n(w), n(h), pid)
    g += '<circle cx="%s" cy="%s" r="%s" fill="#FFFFFF" opacity=".5" filter="url(#fB30)"/>' % (n(cx), n(y + h * .3), n(r * .7))
    g += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(cx), n(cy - r * .12), n(r * .3), fig)
    g += '<path d="M%s,%s C%s,%s %s,%s %s,%s L%s,%s C%s,%s %s,%s %s,%s Z" fill="%s"/>' % (
        n(cx - r * .72), n(y + h), n(cx - r * .7), n(cy + r * .35), n(cx - r * .35), n(cy + r * .22), n(cx), n(cy + r * .22),
        n(cx), n(cy + r * .22), n(cx + r * .35), n(cy + r * .22), n(cx + r * .7), n(cy + r * .35), n(cx + r * .72), n(y + h), fig)
    g += '</g>'
    return g


def lily(x, y, s=1, rot=0, col="#FFFFFF", shade="#E3E1D8", vein="#D6D9C8", stamen="#A99A6B"):
    """white Easter/Madonna lily, trumpet facing viewer-ish, 6 recurved petals; (x,y)=throat. ~180px at s=1."""
    g = '<g transform="translate(%s %s) rotate(%s) scale(%s)">' % (n(x), n(y), rot, s)
    pet = "M0,0 C22,-20 26,-60 10,-92 C6,-100 2,-104 0,-106 C-2,-104 -6,-100 -10,-92 C-26,-60 -22,-20 0,0Z"
    for k in range(3):  # back petals
        g += '<g transform="rotate(%s)"><path d="%s" fill="%s"/><path d="M0,-6 C2,-40 2,-70 0,-100" stroke="%s" stroke-width="1.4" fill="none"/></g>' % (k * 120 + 60, pet, shade, vein)
    for k in range(3):  # front petals
        g += '<g transform="rotate(%s)"><path d="%s" fill="%s" stroke="%s" stroke-width=".8"/>' % (k * 120, pet, col, shade)
        g += '<path d="M0,-6 C2,-40 2,-70 0,-100" stroke="%s" stroke-width="1.6" fill="none"/>' % vein
        g += '<path d="M0,-8 C10,-30 12,-50 8,-70 M0,-8 C-10,-30 -12,-50 -8,-70" stroke="%s" stroke-width=".8" fill="none" opacity=".7"/></g>' % vein
    g += '<circle r="16" fill="#F4F5E6"/><circle r="9" fill="#E3E8C8"/>'
    for k in range(6):
        a = math.radians(k * 60 + 30)
        ex, ey = 38 * math.cos(a), 38 * math.sin(a)
        g += '<path d="M0,0 Q%s,%s %s,%s" stroke="#D9D6BF" stroke-width="1.6" fill="none"/>' % (n(ex * .4), n(ey * .6), n(ex), n(ey))
        g += '<ellipse cx="%s" cy="%s" rx="5" ry="2.4" transform="rotate(%s %s %s)" fill="%s"/>' % (n(ex), n(ey), n(k * 60 + 30), n(ex), n(ey), stamen)
    g += '<circle cx="0" cy="0" r="3.4" fill="#C9CFAE"/>'
    return g + "</g>"


def lily_spray(x, y, s=1, mirror=False, rng=None, stem="#8FA08A", leafc="#9DB096"):
    """spray of 3 white lilies + buds on sage stems growing up-right from (x,y)."""
    rng = rng or random.Random(8)
    sx = -1 if mirror else 1
    g = '<g transform="translate(%s %s) scale(%s %s)">' % (n(x), n(y), n(sx * s), n(s))
    g += '<path d="M0,0 C20,-80 40,-160 70,-230 M0,0 C40,-60 100,-100 170,-120 M0,0 C0,-90 -10,-170 -20,-250" stroke="%s" stroke-width="5" fill="none" stroke-linecap="round"/>' % stem
    for (lx, ly, ln, r) in ((10, -60, 90, -30), (30, -120, 80, 30), (60, -60, 90, 60), (-4, -140, 80, -20), (90, -90, 70, 70)):
        g += leaf(lx, ly, ln, r, leafc, "#C6D2BF")
    g += '<g transform="translate(-20 -262) rotate(-12)"><path d="M0,0 C10,-20 10,-60 0,-80 C-10,-60 -10,-20 0,0Z" fill="#F1F2EA" stroke="#D5D8CA"/></g>'
    g += "</g>"
    # blooms (in card coords so they stay upright)
    for (bx, by, bs, br) in ((70, -238, .78, 10), (176, -126, .72, 70), (-8, -176, .5, -40)):
        g += lily(x + sx * bx * s, y + by * s, bs * s, br * sx)
    return g


def lotus(x, y, s=1, col="#FFFFFF", shade="#E6E2D8", tip="#F1E6E0", base="#D5DCC7", open_=1.0):
    """white lotus (side view) sitting on the water line (x,y)=base centre. ~260 wide at s=1."""
    g = '<g transform="translate(%s %s) scale(%s)">' % (n(x), n(y), s)
    pid, pd = lg([(0, tip), (.35, col), (1, base)], 0, 0, 0, 1)
    sid, sd = lg([(0, shade), (1, "#C9CCBA")], 0, 0, 0, 1)
    g += "<defs>%s%s</defs>" % (pd, sd)
    def petal(ang, ln, wd, fill, op=1):
        return ('<g transform="rotate(%s)" opacity="%s"><path d="M0,0 C%s,%s %s,%s 0,%s C%s,%s %s,%s 0,0Z" fill="%s" stroke="%s" stroke-width=".8"/>'
                '<path d="M0,-6 L0,%s" stroke="%s" stroke-width=".9" opacity=".6"/></g>') % (
            ang, op, n(wd), n(-ln * .3), n(wd * .7), n(-ln * .85), n(-ln), n(-wd * .7), n(-ln * .85), n(-wd), n(-ln * .3), fill, "#D9D5C8", n(-ln * .8), "#D6D2C4")
    for a in (-78, 78, -58, 58):
        g += petal(a * open_, 110, 38, "url(#%s)" % sid)
    for a in (-36, 36, -18, 18):
        g += petal(a * open_, 130, 40, "url(#%s)" % pid)
    g += petal(0, 140, 42, "url(#%s)" % pid)
    for a in (-46, 46):
        g += petal(a * open_, 100, 34, "url(#%s)" % pid)
    g += '<ellipse cx="0" cy="-2" rx="54" ry="10" fill="%s" opacity=".6"/>' % base
    g += "</g>"
    return g


def lotus_leaf(x, y, rx, ry, col="#9FB09A", dark="#7E9079", rot=0):
    g = '<g transform="rotate(%s %s %s)">' % (rot, n(x), n(y))
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (n(x), n(y + ry * .15), n(rx), n(ry), dark)
    g += '<path d="M%s,%s A%s,%s 0 1 1 %s,%s L%s,%s Z" fill="%s"/>' % (n(x + rx * .1), n(y - ry), n(rx), n(ry), n(x - rx * .1), n(y - ry), n(x), n(y), col)
    for k in range(9):
        a = math.pi * (k / 8.0) - math.pi
        g += '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#C8D3C1" stroke-width="1.2" opacity=".6"/>' % (n(x), n(y), n(x + rx * .9 * math.cos(a + math.pi)), n(y + ry * .9 * math.sin(a + math.pi)))
    return g + "</g>"


def calm_diya(x, y, s=1, glow=True):
    """single brass diya with a steady flame and a restrained warm glow."""
    g = ""
    if glow:
        g += '<circle cx="%s" cy="%s" r="%s" fill="url(#gHaloSoft)"/>' % (n(x + 60 * s), n(y - 40 * s), n(150 * s))
    g += diya(x, y, s, "brass", deco="#F3E3B6", deco2="#F3E3B6", glow_r=70 * s, calm=True)
    return g


def incense(x, y, s=1, sticks=3, rng=None, smoke="#8E8A84", holder="url(#gMGold)"):
    """small brass incense holder with sticks and soft rising smoke curls; (x,y) = holder base."""
    rng = rng or random.Random(14)
    g = '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#000" opacity=".2" filter="url(#fB4)"/>' % (n(x), n(y + 4 * s), n(46 * s), n(8 * s))
    g += '<path d="M%s,%s C%s,%s %s,%s %s,%s L%s,%s C%s,%s %s,%s %s,%s Z" fill="%s"/>' % (
        n(x - 44 * s), n(y), n(x - 40 * s), n(y - 20 * s), n(x - 20 * s), n(y - 28 * s), n(x - 10 * s), n(y - 30 * s),
        n(x + 10 * s), n(y - 30 * s), n(x + 20 * s), n(y - 28 * s), n(x + 40 * s), n(y - 20 * s), n(x + 44 * s), n(y), holder)
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (n(x), n(y - 30 * s), n(12 * s), n(4 * s), "#6F603F")
    for k in range(sticks):
        a = math.radians(-90 + (k - (sticks - 1) / 2.0) * 9)
        ln = 210 * s
        tx, ty = x + ln * math.cos(a), y - 30 * s + ln * math.sin(a)
        mx, my = x + ln * .45 * math.cos(a), y - 30 * s + ln * .45 * math.sin(a)
        g += '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#6D4C35" stroke-width="%s" stroke-linecap="round"/>' % (n(x), n(y - 30 * s), n(mx), n(my), n(2.2 * s))
        g += '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#4A3A30" stroke-width="%s" stroke-linecap="round"/>' % (n(mx), n(my), n(tx), n(ty), n(4 * s))
        g += '<circle cx="%s" cy="%s" r="%s" fill="#E86A2A"/><circle cx="%s" cy="%s" r="%s" fill="#FFB067" opacity=".6" filter="url(#fB2)"/>' % (
            n(tx), n(ty), n(2.6 * s), n(tx), n(ty), n(6 * s))
        # smoke
        d = "M%s,%s" % (n(tx), n(ty))
        cx_, cy_ = tx, ty
        amp = rng.uniform(14, 22) * s
        for j in range(6):
            nx, ny = cx_ + rng.uniform(-6, 6) * s, cy_ - rng.uniform(55, 75) * s
            sgn = 1 if (j + k) % 2 == 0 else -1
            d += " C%s,%s %s,%s %s,%s" % (n(cx_ + sgn * amp), n(cy_ - 20 * s), n(nx + sgn * amp), n(ny + 20 * s), n(nx), n(ny))
            cx_, cy_ = nx, ny
            amp *= 1.18
        sid, sd = lg([(0, smoke, .7), (.6, smoke, .3), (1, smoke, 0)], 0, 1, 0, 0)
        g += '<defs>%s</defs><path d="%s" fill="none" stroke="url(#%s)" stroke-width="%s" stroke-linecap="round" filter="url(#fB2)"/>' % (sd, d, sid, n(3.2 * s))
        g += '<path d="%s" fill="none" stroke="url(#%s)" stroke-width="%s" stroke-linecap="round" opacity=".6" filter="url(#fB4)" transform="translate(%s 0)"/>' % (d, sid, n(8 * s), n(5 * s))
    return g


def dove(x, y, s=1, rot=0, mirror=False, col="#FFFFFF", shade="#D9D9D4", eye="#6B6B6B"):
    """flying dove, wings raised; ~ 240 wide at s=1, facing right."""
    sx = -1 if mirror else 1
    g = '<g transform="translate(%s %s) rotate(%s) scale(%s %s)" filter="url(#fShadowS)">' % (n(x), n(y), rot, n(sx * s), n(s))
    # far wing
    g += '<path d="M-10,-6 C-20,-50 -10,-100 30,-140 C26,-110 30,-80 46,-60 C40,-40 26,-20 10,-8Z" fill="%s"/>' % shade
    # body
    g += '<path d="M-110,20 C-86,4 -60,-4 -30,-6 C0,-10 30,-12 52,-20 C62,-30 76,-34 86,-28 C94,-24 98,-18 108,-16 C100,-10 92,-8 86,-6 C80,10 60,26 30,30 C0,34 -40,30 -70,34 C-90,44 -112,48 -130,44 C-118,36 -112,30 -110,20Z" fill="%s"/>' % col
    # tail feathers
    g += '<path d="M-110,20 C-130,16 -150,20 -168,30 C-150,32 -140,40 -130,44 C-118,36 -112,30 -110,20Z" fill="%s"/>' % shade
    # near wing with feathers
    g += '<path d="M-40,-2 C-60,-60 -40,-130 20,-170 C18,-140 26,-120 40,-104 C30,-80 34,-56 44,-40 C20,-20 -10,-6 -40,-2Z" fill="%s"/>' % col
    for k in range(5):
        g += '<path d="M%s,%s C%s,%s %s,%s %s,%s" fill="none" stroke="%s" stroke-width="1.4"/>' % (
            -30 + k * 10, -8 - k * 4, -20 + k * 6, -60 - k * 6, 0 + k * 4, -110 - k * 8, 16 + k * 4, -150 + k * 10, shade)
    g += '<circle cx="84" cy="-24" r="2.6" fill="%s"/>' % eye
    g += '<path d="M104,-18 L116,-14 L104,-12Z" fill="#C9B9A0"/>'
    # olive twig
    g += '<path d="M106,-14 C120,-6 130,4 138,16" stroke="#8FA08A" stroke-width="2" fill="none"/>'
    for k in range(3):
        g += leaf(116 + k * 9, -6 + k * 9, 16, 120 + k * 10, "#9DB096", "#C6D2BF")
    return g + "</g>"


def light_rays(x, y, angles, length=1600, spread=5, col="#FFFFFF", op=.22):
    out = []
    for a in angles:
        a1, a2 = math.radians(a - spread / 2.0), math.radians(a + spread / 2.0)
        out.append('<polygon points="%s" fill="%s"/>' % (pts([(x, y), (x + length * math.cos(a1), y + length * math.sin(a1)), (x + length * math.cos(a2), y + length * math.sin(a2))]), col))
    return '<g opacity="%s" filter="url(#fB16)">%s</g>' % (op, "".join(out))


def rajnigandha_stem(x, y, ln, s=1, rot=0, rng=None):
    """one tuberose stem: dense white buds/blooms over the top half."""
    rng = rng or random.Random(int(x * 3 + y))
    g = '<g transform="translate(%s %s) rotate(%s)">' % (n(x), n(y), rot)
    g += '<path d="M0,0 C4,%s -4,%s 0,%s" stroke="#8FA08A" stroke-width="%s" fill="none"/>' % (n(-ln * .3), n(-ln * .7), n(-ln), n(4 * s))
    g += leaf(0, -ln * .12, ln * .22, -18, "#9DB096", "#C6D2BF") + leaf(0, -ln * .2, ln * .2, 20, "#8FA08A", "#C6D2BF")
    yy = -ln * .42
    side = 1
    while yy > -ln:
        t = (-yy - ln * .42) / (ln * .58)
        g += '<path d="M0,%s l%s,-6" stroke="#9DB096" stroke-width="1.6"/>' % (n(yy), n(side * 8 * s))
        if t < .6 and rng.random() < .6:
            g += jasmine(side * 12 * s, yy - 6 * s, (15 - 4 * t) * s, rng.uniform(0, 72), "#FFFFFF", "#DCD7C8")
        else:
            g += jasmine_bud(side * 8 * s, yy - 4 * s, (9 - 3.5 * t) * s, side * 30, "#FFFFFF", "#D8D2C0", "#DDE6C8")
        side *= -1
        yy -= 9 * s
    g += jasmine_bud(0, -ln, 5 * s, 0, "#EEF2E2", "#CAD2B6", "#C6D2AE")
    return '<g filter="url(#fShadowS)">' + g + "</g></g>"


def glass_vase(cx, base, w, h):
    """clear glass cylinder vase with water line and highlights."""
    gid, gd = lg([(0, "#FFFFFF", .25), (.2, "#FFFFFF", .05), (.8, "#FFFFFF", .05), (1, "#FFFFFF", .3)], 0, 0, 1, 0)
    g = '<defs>%s</defs>' % gd
    g += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#000" opacity=".12" filter="url(#fB4)"/>' % (n(cx), n(base + 4), n(w * .6), n(10))
    g += '<rect x="%s" y="%s" width="%s" height="%s" rx="10" fill="url(#%s)" stroke="#FFFFFF" stroke-opacity=".7" stroke-width="2"/>' % (n(cx - w / 2), n(base - h), n(w), n(h), gid)
    g += '<rect x="%s" y="%s" width="%s" height="%s" fill="#C9D6D0" opacity=".25"/>' % (n(cx - w / 2 + 3), n(base - h * .55), n(w - 6), n(h * .55 - 3))
    g += '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#FFFFFF" stroke-width="5" opacity=".6" stroke-linecap="round"/>' % (n(cx - w / 2 + 12), n(base - h + 16), n(cx - w / 2 + 12), n(base - 16))
    return g


def soft_clouds(rng, count, x0, y0, x1, y1, col="#FFFFFF", op=.5):
    out = []
    for _ in range(count):
        cx, cy = rng.uniform(x0, x1), rng.uniform(y0, y1)
        for k in range(5):
            out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (n(cx + rng.uniform(-80, 80)), n(cy + rng.uniform(-14, 14)), n(rng.uniform(60, 120)), n(rng.uniform(24, 40)), col))
    return '<g opacity="%s" filter="url(#fB16)">%s</g>' % (op, "".join(out))


def thin_ornament_line(cx, y, half, col="url(#gMGold)", op=1):
    """quiet centred divider ornament: two tapering lines with a small lotus bud."""
    g = '<g opacity="%s">' % op
    g += '<path d="M%s,%s L%s,%s L%s,%s Z" fill="%s"/>' % (n(cx - half), n(y), n(cx - 24), n(y - 1.6), n(cx - 24), n(y + 1.6), col)
    g += '<path d="M%s,%s L%s,%s L%s,%s Z" fill="%s"/>' % (n(cx + half), n(y), n(cx + 24), n(y - 1.6), n(cx + 24), n(y + 1.6), col)
    g += '<path d="M%s,%s c-10,-6 -12,-16 0,-24 c12,8 10,18 0,24Z" fill="%s"/>' % (n(cx), n(y + 6), col)
    g += '<path d="M%s,%s c-14,0 -18,-8 -18,-14 c8,0 14,4 18,14Z M%s,%s c14,0 18,-8 18,-14 c-8,0 -14,4 -18,14Z" fill="%s"/>' % (n(cx), n(y + 6), n(cx), n(y + 6), col)
    return g + "</g>"


def garland_points(shape, x, y, w, h, pad, step, sag=None):
    """outline points; with sag, the bottom edge is replaced by a hanging U-curve (garland draped over the frame)."""
    P = shape_pts(shape, x, y, w, h, pad, step)
    if sag is None:
        return P
    ycut = y + h + pad - 2 if shape != "oval" else y + h * .78
    kept = [p for p in P if p[1] <= ycut]
    low = [p for p in kept if p[1] > ycut - 3 * step - 2]
    L = min(low, key=lambda p: p[0])
    R = max(low, key=lambda p: p[0])
    by = y + h + pad + sag
    C = ((L[0] + R[0]) / 2, 2 * by - (L[1] + R[1]) / 2)
    curve = []
    k = 200
    prev = L
    acc = 0
    for i in range(1, k + 1):
        t = i / float(k)
        px = (1 - t) ** 2 * L[0] + 2 * (1 - t) * t * C[0] + t * t * R[0]
        py = (1 - t) ** 2 * L[1] + 2 * (1 - t) * t * C[1] + t * t * R[1]
        acc += math.hypot(px - prev[0], py - prev[1])
        prev = (px, py)
        if acc >= step:
            curve.append((px, py)); acc = 0
    return kept + curve


def jasmine_garland2(shape, x, y, w, h, pad=30, rng=None, thick=1.0, sag=40, leaves=True, tassel=True, col="#FFFFFF", shade="#E2DDCF"):
    rng = rng or random.Random(21)
    P = garland_points(shape, x, y, w, h, pad, 9 / thick, sag)
    g = ['<g filter="url(#fShadowS)">']
    for i, (px, py) in enumerate(P):
        if leaves and i % 6 == 0:
            g.append(leaf(px + rng.uniform(-6, 6), py + rng.uniform(-6, 6), rng.uniform(16, 24) * thick, rng.uniform(0, 360)))
    for i, (px, py) in enumerate(P):
        for k in range(2):
            ox, oy = rng.uniform(-10, 10) * thick, rng.uniform(-10, 10) * thick
            if rng.random() < .62:
                g.append(jasmine(px + ox, py + oy, rng.uniform(9, 12.5) * thick, rng.uniform(0, 72), col, shade))
            else:
                g.append(jasmine_bud(px + ox, py + oy, rng.uniform(5, 7) * thick, rng.uniform(0, 360), col, shade))
    g.append("</g>")
    if tassel:
        g.append(jasmine_tassel(x + w / 2, y + h + pad + (sag or 0), .8 * thick, rng))
    return "".join(g)


def rajnigandha_rope2(shape, x, y, w, h, pad=30, rng=None, s=1.0, sag=40, tassel=False):
    rng = rng or random.Random(33)
    P = garland_points(shape, x, y, w, h, pad, 7, sag)
    g = ['<g filter="url(#fShadowS)">']
    for i in range(len(P) - 1):
        (ax, ay), (bx, by) = P[i], P[i + 1]
        if math.hypot(bx - ax, by - ay) > 30:
            continue
        ang = math.degrees(math.atan2(by - ay, bx - ax))
        for side in (-1, 1):
            rot = ang + 90 + side * 55 + rng.uniform(-10, 10)
            col = "#FFFFFF" if rng.random() < .8 else "#F2F4E6"
            g.append(jasmine_bud(ax + side * 3, ay, rng.uniform(6.5, 8.5) * s, rot, col, "#D8D2C0", "#DDE6C8"))
        if i % 9 == 0:
            g.append(jasmine(ax, ay, 8 * s, rng.uniform(0, 72), "#FFFFFF", "#DAD4C2"))
    g.append("</g>")
    if tassel:
        g.append(jasmine_tassel(x + w / 2, y + h + pad + (sag or 0), .8 * s, rng))
    return "".join(g)


def sandal_garland2(shape, x, y, w, h, pad=22, s=1.0, sag=40, bead="#B08A62"):
    P = garland_points(shape, x, y, w, h, pad, 15 * s, sag)
    bid, bd = rg([(0, "#E3C9A4"), (.55, bead), (1, "#6D5238")], cx=.38, cy=.35, r=.7)
    g = '<defs>%s</defs><g filter="url(#fShadowS)">' % bd
    for i, (px, py) in enumerate(P):
        if i % 6 == 0:
            g += '<circle cx="%s" cy="%s" r="%s" fill="url(#gMGold)"/>' % (n(px), n(py), n(4.5 * s))
        else:
            g += '<circle cx="%s" cy="%s" r="%s" fill="url(#%s)"/>' % (n(px), n(py), n(7.2 * s), bid)
    return g + "</g>"


def marble(op=.5, seed=3, col="#9C978E"):
    rng = random.Random(seed)
    out = []
    for _ in range(9):
        x0, y0 = rng.uniform(-200, 1080), rng.uniform(-100, 1350)
        d = "M%s,%s" % (n(x0), n(y0))
        x, y = x0, y0
        for _ in range(5):
            nx, ny = x + rng.uniform(80, 220), y + rng.uniform(-60, 140)
            d += " Q%s,%s %s,%s" % (n((x + nx) / 2 + rng.uniform(-60, 60)), n((y + ny) / 2 + rng.uniform(-60, 60)), n(nx), n(ny))
            x, y = nx, ny
        out.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s" opacity="%s"/>' % (d, col, n(rng.uniform(1, 3.5)), n(rng.uniform(.2, .5))))
    return '<g opacity="%s" filter="url(#fB2)">%s</g>' % (op, "".join(out))


def linen(op=.08):
    lines = "".join('<line x1="0" y1="%s" x2="1080" y2="%s" stroke="#000" stroke-width="1" opacity="%s"/>' % (y, y, .5 if y % 6 == 0 else .25) for y in range(0, 1350, 3))
    lines += "".join('<line x1="%s" y1="0" x2="%s" y2="1350" stroke="#000" stroke-width="1" opacity=".2"/>' % (x, x) for x in range(0, 1080, 4))
    return '<g opacity="%s">%s</g>' % (op, lines)


def mcorners(m=34, s=.55, fill="url(#gMGold)", op=.9):
    """quiet bracket corners (stepped lines + a small lotus bud) for sober cards."""
    def one(x, y, sx, sy):
        L = 120 * s * 1.6
        g = '<g transform="translate(%s %s) scale(%s %s)" opacity="%s">' % (x, y, sx, sy, op)
        g += '<path d="M0,%s V0 H%s" fill="none" stroke="%s" stroke-width="3"/>' % (n(L), n(L), fill)
        g += '<path d="M10,%s V10 H%s" fill="none" stroke="%s" stroke-width="1.4"/>' % (n(L * .7), n(L * .7), fill)
        g += '<path d="M20,20 L34,20 L20,34Z" fill="%s"/>' % fill
        g += '<circle cx="%s" cy="0" r="3" fill="%s"/><circle cx="0" cy="%s" r="3" fill="%s"/>' % (n(L + 8), fill, n(L + 8), fill)
        return g + "</g>"
    return one(m, m, 1, 1) + one(W - m, m, -1, 1) + one(m, H - m, 1, -1) + one(W - m, H - m, -1, -1)


def hairline_frame(m=30, col="url(#gMGold)", op=.9, r=0):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="%s" stroke-width="2" opacity="%s"/>' % (
        m, m, W - 2 * m, H - 2 * m, r, col, op))


def save_specs(cat, specs):
    import json, os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", cat + ".json")
    json.dump(specs, open(p, "w"), ensure_ascii=False, indent=1)
    print("wrote", p)


def mehendi_vine(x, y0, y1, col="url(#gGold)", amp=26, s=1, flip=False):
    """vertical mehendi-style vine: sinuous stem, alternating leaves, dot trails, small flowers."""
    f = -1 if flip else 1
    d = "M%s,%s" % (n(x), n(y0))
    seg = 80 * s
    y = y0
    k = 0
    out = []
    while y < y1:
        ny = min(y1, y + seg)
        sgn = 1 if k % 2 == 0 else -1
        d += " C%s,%s %s,%s %s,%s" % (n(x + f * sgn * amp), n(y + seg * .3), n(x + f * sgn * amp), n(y + seg * .7), n(x), n(ny))
        lx = x + f * sgn * amp * .75
        out.append(leaf(lx, y + seg * .5, 34 * s, 90 * sgn * f + 20, col, "#7A2E0E"))
        out.append("".join('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(x - f * sgn * (10 + j * 8) * s), n(y + seg * .5 - j * 6 * s), n((3 - j * .6) * s), col) for j in range(3)))
        if k % 3 == 1:
            out.append('<g transform="translate(%s %s)">%s<circle r="%s" fill="#7A2E0E"/></g>' % (n(x), n(ny), _around(6, '<path d="%s" fill="%s"/>' % (petal_path(3 * s, 15 * s, 5 * s, "round"), col)), n(3.5 * s)))
        y = ny
        k += 1
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s"/>%s' % (d, col, n(2.6 * s), "".join(out))


def chunri_swag(x0, x1, y, sag, depth=60, base=("#B3001B", "#6E0A20")):
    """red chunri fabric swag hanging between two points, with gold gota edge and tassel beads."""
    gid, gd = lg([(0, base[0]), (1, base[1])], 0, 0, 0, 1)
    mx = (x0 + x1) / 2.0
    top = "M%s,%s Q%s,%s %s,%s" % (n(x0), n(y), n(mx), n(y + sag), n(x1), n(y))
    bot = "Q%s,%s %s,%s" % (n(mx), n(y + sag + depth * 2), n(x0), n(y))
    g = '<defs>%s</defs><path d="%s L%s,%s %s Z" fill="url(#%s)" filter="url(#fShadowS)"/>' % (gd, top, n(x1), n(y), bot, gid)
    for k in range(1, 4):
        t = k / 4.0
        g += '<path d="M%s,%s Q%s,%s %s,%s" fill="none" stroke="#000" stroke-opacity=".18" stroke-width="3"/>' % (n(x0), n(y), n(mx), n(y + sag + depth * 2 * t), n(x1), n(y))
    g += '<path d="M%s,%s %s" fill="none" stroke="url(#gGoldH)" stroke-width="8"/>' % (n(x1), n(y), bot)
    for k in range(1, 12):
        t = k / 12.0
        px = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * mx + t * t * x0
        py = (1 - t) ** 2 * y + 2 * (1 - t) * t * (y + sag + depth * 2) + t * t * y
        g += '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#FFD86B" stroke-width="1.6"/><circle cx="%s" cy="%s" r="4" fill="url(#gGold)"/>' % (n(px), n(py), n(px), n(py + 16), n(px), n(py + 18))
    return g
