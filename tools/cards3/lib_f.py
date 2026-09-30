"""lib_f: shared SVG illustration helpers for inv-griha-pravesh, inv-puja, inv-shop-opening.

Every function returns an SVG fragment string. Gradients are registered per card via
lin()/rad() and emitted by card(). Call card(body) to wrap everything into a 1080x1350 svg.
"""
import math, random

W, H = 1080, 1350
_DEFS = {}
_EXTRA = []


def reset():
    _DEFS.clear(); _EXTRA.clear()


def _stops(stops):
    out = []
    n = len(stops)
    for i, s in enumerate(stops):
        if isinstance(s, str):
            off, col, op = (i / (n - 1) if n > 1 else 0), s, 1
        elif len(s) == 2:
            off, col, op = s[0], s[1], 1
        else:
            off, col, op = s
        out.append('<stop offset="%.3f" stop-color="%s" stop-opacity="%s"/>' % (off, col, op))
    return "".join(out)


def lin(stops, x1=0, y1=0, x2=0, y2=1, user=None):
    key = ("l", tuple(map(str, stops)), x1, y1, x2, y2, user)
    if key not in _DEFS:
        gid = "g%d" % len(_DEFS)
        units = ' gradientUnits="userSpaceOnUse"' if user else ""
        _DEFS[key] = (gid, '<linearGradient id="%s" x1="%s" y1="%s" x2="%s" y2="%s"%s>%s</linearGradient>'
                      % (gid, x1, y1, x2, y2, units, _stops(stops)))
    return "url(#%s)" % _DEFS[key][0]


def rad(stops, cx=0.5, cy=0.5, r=0.5, fx=None, fy=None, user=None):
    fx = cx if fx is None else fx
    fy = cy if fy is None else fy
    key = ("r", tuple(map(str, stops)), cx, cy, r, fx, fy, user)
    if key not in _DEFS:
        gid = "g%d" % len(_DEFS)
        units = ' gradientUnits="userSpaceOnUse"' if user else ""
        _DEFS[key] = (gid, '<radialGradient id="%s" cx="%s" cy="%s" r="%s" fx="%s" fy="%s"%s>%s</radialGradient>'
                      % (gid, cx, cy, r, fx, fy, units, _stops(stops)))
    return "url(#%s)" % _DEFS[key][0]


def defs(markup):
    _EXTRA.append(markup)


BASE_DEFS = """
<filter id="sh" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#2a1205" flood-opacity=".38"/></filter>
<filter id="shs" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#2a1205" flood-opacity=".35"/></filter>
<filter id="shp" x="-10%" y="-10%" width="120%" height="125%"><feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#1c0a02" flood-opacity=".35"/></filter>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="glow2" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="22"/></filter>
<filter id="b3"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="b6" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="b14" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="b30" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="30"/></filter>
<filter id="paper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="7" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 .45  0 0 0 0 .32  0 0 0 0 .18  0 0 0 .09 0" result="c"/><feComposite in="c" in2="SourceGraphic" operator="in" result="t"/>
<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="t"/></feMerge></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".55" numOctaves="2" seed="3" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .07 0" result="c"/><feComposite in="c" in2="SourceGraphic" operator="in" result="t"/>
<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="t"/></feMerge></filter>
"""

GOLD = ["#7A4E0E", "#C8962E", "#F9E39A", "#D9A63C", "#FFF1BF", "#B07A1C", "#6E440A"]
GOLD_SOFT = ["#A87422", "#E8C164", "#FFF3C4", "#E0B452", "#9C6A1A"]


def gold(x1=0, y1=0, x2=1, y2=1):
    return lin(GOLD, x1, y1, x2, y2)


def goldv():
    return lin(GOLD_SOFT, 0, 0, 0, 1)


def card(body, bg="#fff"):
    d = "".join(v[1] for v in _DEFS.values()) + "".join(_EXTRA)
    s = ('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">'
         '<defs>%s%s</defs><rect width="1080" height="1350" fill="%s"/>%s</svg>' % (BASE_DEFS, d, bg, body))
    reset()
    return s


def T(x=0, y=0, s=1, r=0, sx=None, sy=None):
    t = "translate(%.1f %.1f)" % (x, y)
    if r:
        t += " rotate(%.2f)" % r
    if sx is not None or sy is not None:
        t += " scale(%.3f %.3f)" % (sx if sx is not None else s, sy if sy is not None else s)
    elif s != 1:
        t += " scale(%.3f)" % s
    return t


def G(inner, x=0, y=0, s=1, r=0, sx=None, sy=None, extra=""):
    return '<g transform="%s"%s>%s</g>' % (T(x, y, s, r, sx, sy), (" " + extra) if extra else "", inner)


# ------------------------------------------------------------------ backgrounds
def rays(cx, cy, n=24, r=1400, color="#FFFFFF", op=0.18, width=0.5, rot=0):
    out = []
    for i in range(n):
        a0 = math.radians(rot + i * 360 / n)
        a1 = a0 + math.radians(360 / n * width)
        out.append("M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" % (cx, cy, cx + r * math.cos(a0), cy + r * math.sin(a0),
                                                          cx + r * math.cos(a1), cy + r * math.sin(a1)))
    f = rad([(0, color, op), (1, color, 0)], cx, cy, r, user=1)
    return '<path d="%s" fill="%s"/>' % (" ".join(out), f)


def bokeh(rng, n, box, colors, rmin=6, rmax=40, op=(0.15, 0.5)):
    x0, y0, x1, y1 = box
    out = []
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        r = rng.uniform(rmin, rmax)
        c = rng.choice(colors)
        o = rng.uniform(*op)
        out.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" opacity="%.2f"/>' % (x, y, r, rad([(0, c, 1), (0.7, c, .6), (1, c, 0)]), o))
    return "".join(out)


def sparkle(x, y, s=1, color="#FFF6D0", op=1):
    p = "M0 -20 C2 -4 4 -2 20 0 C4 2 2 4 0 20 C-2 4 -4 2 -20 0 C-4 -2 -2 -4 0 -20Z"
    return '<path transform="%s" d="%s" fill="%s" opacity="%s"/>' % (T(x, y, s), p, color, op)


def pattern_tile(pid, size, inner, bg=None):
    b = '<rect width="%d" height="%d" fill="%s"/>' % (size, size, bg) if bg else ""
    defs('<pattern id="%s" width="%d" height="%d" patternUnits="userSpaceOnUse">%s%s</pattern>' % (pid, size, size, b, inner))
    return "url(#%s)" % pid


def jaali_pattern(pid, color, op=0.12, size=60):
    s = size
    inner = ('<g fill="none" stroke="%s" stroke-opacity="%s" stroke-width="1.6">'
             '<path d="M%d 0 Q%d %d %d %d Q%d %d %d %d Q%d %d %d %d Q%d %d %d 0Z"/>'
             '<circle cx="%d" cy="%d" r="%d"/><circle cx="0" cy="0" r="%d"/><circle cx="%d" cy="0" r="%d"/><circle cx="0" cy="%d" r="%d"/><circle cx="%d" cy="%d" r="%d"/></g>'
             % (color, op, s / 2, s / 2 + 2, s / 4, s, s / 2, s / 2 + 2, 3 * s / 4, s / 2, s, s / 2 - 2, 3 * s / 4, 0, s / 2, s / 2 - 2, s / 4, s / 2,
                s / 2, s / 2, s / 8, s / 10, s, s / 10, s, s / 10, s, s, s / 10))
    return pattern_tile(pid, s, inner)


def dots_pattern(pid, color, op=0.15, size=34, r=2.2):
    inner = '<circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity="%s"/><circle cx="0" cy="0" r="%s" fill="%s" fill-opacity="%s"/><circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity="%s"/>' % (
        size / 2, size / 2, r, color, op, r * .7, color, op, size, size, r * .7, color, op)
    return pattern_tile(pid, size, inner)


def floral_pattern(pid, color, op=0.12, size=90):
    s = size; c = s / 2
    pet = "".join('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" transform="rotate(%d %s %s)"/>' % (c, c - s * .12, s * .045, s * .11, a, c, c) for a in range(0, 360, 45))
    inner = '<g fill="%s" fill-opacity="%s">%s<circle cx="0" cy="0" r="%s"/><circle cx="%s" cy="0" r="%s"/><circle cx="0" cy="%s" r="%s"/><circle cx="%s" cy="%s" r="%s"/></g>' % (
        color, op, pet, s * .04, s, s * .04, s, s * .04, s, s, s * .04)
    return pattern_tile(pid, s, inner)


def stripes_pattern(pid, c1, c2, w=26, angle=0):
    defs('<pattern id="%s" width="%d" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(%s)"><rect width="%d" height="10" fill="%s"/><rect x="%d" width="%d" height="10" fill="%s"/></pattern>'
         % (pid, 2 * w, angle, w, c1, w, w, c2))
    return "url(#%s)" % pid


# ------------------------------------------------------------------ flowers & leaves
MARI = {
    "orange": ["#B83A00", "#E25A00", "#F7811B", "#FFA02A", "#FFC04A"],
    "yellow": ["#C07A00", "#E59A00", "#F6B80E", "#FFD23F", "#FFE68A"],
    "red": ["#7E0F0F", "#A8171A", "#CC2A22", "#E4472E", "#F2744A"],
}


def marigold(cx, cy, r, hue="orange", rot=0):
    c = MARI[hue]
    out = ['<g transform="translate(%.1f %.1f) rotate(%d)">' % (cx, cy, rot)]
    out.append('<circle r="%.1f" fill="%s"/>' % (r * 1.02, c[0]))
    rings = [(r * 0.98, 16, c[1]), (r * 0.8, 14, c[2]), (r * 0.6, 12, c[3]), (r * 0.38, 9, c[4])]
    for i, (rr, n, col) in enumerate(rings):
        for k in range(n):
            a = k * 360.0 / n + i * 11
            out.append('<ellipse cx="0" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%.1f)" fill="%s" stroke="%s" stroke-width="%.2f"/>'
                       % (-rr * 0.55, rr * 0.36, rr * 0.46, a, col, c[0], max(0.4, r * 0.03)))
    out.append('<circle r="%.1f" fill="%s"/>' % (r * 0.16, c[0]))
    out.append('<circle r="%.1f" fill="%s"/>' % (r, rad([(0, "#fff", 0), (0.55, "#fff", 0), (1, "#3a0a00", .35)], .45, .4, .6)))
    out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#fff" opacity=".25"/>' % (-r * .3, -r * .35, r * .3, r * .18))
    out.append("</g>")
    return "".join(out)


def leaf_path(L, w=None):
    w = w if w is not None else L * 0.22
    return "M0 0 C%.1f %.1f %.1f %.1f 0 %.1f C%.1f %.1f %.1f %.1f 0 0Z" % (w, L * .22, w * .8, L * .72, L, -w * .8, L * .72, -w, L * .22)


def mango_leaf(x, y, L, angle=0, dark="#1E5B1E", light="#5FA83A", vein="#B9E08A"):
    f = lin([dark, light, dark], 0, 0, 1, 0)
    w = L * 0.2
    half = "M0 0 C%.1f %.1f %.1f %.1f 0 %.1f Z" % (w, L * .22, w * .8, L * .72, L)
    return ('<g transform="translate(%.1f %.1f) rotate(%.1f)"><path d="%s" fill="%s"/><path d="%s" fill="#0c3a0c" opacity=".22"/>'
            '<path d="M0 %.1f Q%.1f %.1f 0 %.1f" stroke="%s" stroke-width="%.1f" fill="none" opacity=".75"/></g>'
            % (x, y, angle, leaf_path(L, w), f, half, L * .02, L * .04, L * .5, L * .95, vein, max(1, L * .025)))


def rope(x0, y0, x1, y1, c1="#B8141B", c2="#F4C542", w=9):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" stroke-linecap="round"/>'
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" stroke-dasharray="%s %s" stroke-linecap="round" opacity=".9"/>'
            % (x0, y0, x1, y1, c1, w, x0, y0, x1, y1, c2, w * .55, w * .5, w * 1.1))


def toran(x0, x1, y, leaf=70, strands=0, strand_len=160, hues=("orange", "yellow"), rope_c=("#B8141B", "#F4C542"), flower_r=None):
    """Mango-leaf + marigold door toran. strands: number of hanging marigold strings."""
    out = ['<g filter="url(#shs)">']
    n = max(2, int((x1 - x0) / (leaf * 0.48)))
    step = (x1 - x0) / n
    # hanging strands first (behind)
    if strands:
        for k in range(strands):
            sx = x0 + (x1 - x0) * (k + .5) / strands
            out.append(marigold_strand(sx, y + 6, strand_len, flower_r or leaf * .17, hues))
    for i in range(n + 1):
        lx = x0 + i * step
        L = leaf * (1 if i % 2 == 0 else 0.82)
        ang = (-14 if i % 3 == 0 else (12 if i % 3 == 1 else 0))
        out.append(mango_leaf(lx, y + 2, L, ang))
    out.append(rope(x0 - 10, y, x1 + 10, y, *rope_c))
    fr = flower_r or leaf * 0.2
    for i in range(n):
        lx = x0 + (i + .5) * step
        out.append(marigold(lx, y + 4, fr, hues[i % 2], i * 17))
    out.append("</g>")
    return "".join(out)


def marigold_strand(x, y, length, r, hues=("orange", "yellow"), tassel=True):
    out = ['<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#7a3b00" stroke-width="2"/>' % (x, y, x, y + length)]
    n = max(2, int(length / (r * 1.7)))
    for i in range(n):
        yy = y + r + i * (length - r) / n
        if i % 4 == 3:
            out.append(mango_leaf(x, yy - r * .6, r * 2.2, 25 if i % 8 == 3 else -25))
        out.append(marigold(x, yy, r * (1 if i % 2 else .9), hues[i % len(hues)], i * 23))
    if tassel:
        ty = y + length + r * .4
        out.append('<path d="M%.1f %.1f l%.1f %.1f l%.1f 0Z" fill="#B8141B"/>' % (x, ty, -r * .6, r * 2.4, r * 1.2))
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (x, ty, r * .45, gold()))
    return "".join(out)


def garland_swag(x0, y0, x1, y1, sag, r=16, hues=("orange", "yellow"), leaves=True, rot=0):
    """Drooping marigold garland along a quadratic curve."""
    mx, my = (x0 + x1) / 2, max(y0, y1) + sag
    pts = []
    L = math.hypot(x1 - x0, y1 - y0) + sag
    n = max(3, int(L / (r * 1.45)))
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1
        yy = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1
        pts.append((x, yy))
    out = []
    if leaves:
        for i, (x, yy) in enumerate(pts):
            if i % 3 == 1:
                out.append(mango_leaf(x, yy, r * 2.3, 15 if i % 2 else -15))
    for i, (x, yy) in enumerate(pts):
        out.append(marigold(x, yy, r, hues[i % len(hues)], i * 31))
    return '<g filter="url(#shs)">%s</g>' % "".join(out)


def lotus(cx, cy, s=1, c1="#F7C6D6", c2="#E0578A", c3="#B42A5E", leaves=False):
    """Lotus bloom, width about 220*s, base at (cx,cy)."""
    pet = "M0 0 C-34 -40 -30 -95 0 -130 C30 -95 34 -40 0 0Z"
    fb = lin([c3, c2, c1], 0, 1, 0, 0)
    ff = lin([c2, c1, "#FFF3F7"], 0, 1, 0, 0)
    out = ['<g transform="translate(%.1f %.1f) scale(%.3f)">' % (cx, cy, s)]
    if leaves:
        lf = lin(["#1F6E4A", "#3FA46E", "#1F6E4A"], 0, 0, 1, 0)
        out.append('<ellipse cx="-95" cy="6" rx="95" ry="22" fill="%s"/><ellipse cx="95" cy="8" rx="95" ry="20" fill="%s"/>' % (lf, lf))
        out.append('<path d="M-170 6 L-40 8 M40 8 L170 8" stroke="#8fd3a8" stroke-width="2" opacity=".6"/>')
    for a in (-72, 72, -52, 52):
        out.append('<path d="%s" transform="rotate(%d) scale(.8 .78)" fill="%s" stroke="%s" stroke-width="1.5"/>' % (pet, a, fb, c3))
    for a in (-34, 34):
        out.append('<path d="%s" transform="rotate(%d) scale(.95)" fill="%s" stroke="%s" stroke-width="1.5"/>' % (pet, a, fb, c3))
    for a in (-16, 16, 0):
        out.append('<path d="%s" transform="rotate(%d) scale(%s)" fill="%s" stroke="%s" stroke-width="1.5"/>' % (pet, a, 1 if a == 0 else .96, ff, c2))
        out.append('<path d="M0 -10 Q%d -70 0 -120" transform="rotate(%d)" stroke="#fff" stroke-width="2" fill="none" opacity=".55"/>' % (4, a))
    out.append('<ellipse cx="0" cy="-6" rx="26" ry="10" fill="#F4C430"/>')
    out.append("</g>")
    return "".join(out)


# ------------------------------------------------------------------ vessels
METAL = {
    "copper": ["#5E2508", "#A4471A", "#E08A4E", "#F8C49A", "#C0602A", "#6A2A0A"],
    "brass": ["#6B4208", "#B98320", "#F2D27A", "#FFF0B8", "#CF9A30", "#6E440A"],
    "silver": ["#5c6068", "#9aa0aa", "#e4e8ee", "#ffffff", "#b4bac4", "#62666e"],
}


def swastik(cx, cy, s, color="#C1121F", w=None):
    w = w or s * .16
    a = s / 2
    d = ("M{0} {1}V{2}M{3} {4}H{5}M{0} {6}H{7}M{0} {2}H{8}M{3} {4}V{9}M{5} {4}V{10}"
         .format(cx, cy - a, cy + a, cx - a, cy, cx + a, cy - a, cx + a, cx - a, cy - a, cy + a))
    dots = "".join('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx + dx * a * .5, cy + dy * a * .5, w * .55, color)
                   for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)))
    return '<path d="%s" stroke="%s" stroke-width="%.1f" stroke-linecap="square" fill="none"/>%s' % (d, color, w, dots)


def coconut(cx, cy, s=1):
    f = rad(["#A0612B", "#6B3A15", "#3E1E08"], .35, .3, .75)
    out = ['<g transform="translate(%.1f %.1f) scale(%.3f)">' % (cx, cy, s)]
    out.append('<path d="M-44 20 C-50 -20 -26 -58 0 -64 C26 -58 50 -20 44 20 C30 40 -30 40 -44 20Z" fill="%s"/>' % f)
    for i in range(-3, 4):
        out.append('<path d="M%d 30 Q%d -10 %d -60" stroke="#C88B4A" stroke-width="1.6" fill="none" opacity=".55"/>' % (i * 11, i * 16, i * 3))
    out.append('<path d="M-6 -62 q-10 -22 -22 -26 M0 -64 q2 -24 -2 -34 M6 -62 q12 -20 24 -22" stroke="#8B5A2B" stroke-width="4" fill="none" stroke-linecap="round"/>')
    out.append('<ellipse cx="-16" cy="-24" rx="10" ry="18" fill="#fff" opacity=".15"/>')
    out.append("</g>")
    return "".join(out)


def kalash(cx, by, h, metal="copper", sw=True, leaves=True, coco=True, cloth="#C1121F", mauli=True):
    """Kalash standing with base at y=by, total height ~h (including coconut)."""
    s = h / 300.0
    m = METAL[metal]
    body = lin(m, 0, 0, 1, 0)
    out = ['<g transform="translate(%.1f %.1f) scale(%.3f)">' % (cx, by, s)]
    out.append('<ellipse cx="0" cy="4" rx="92" ry="14" fill="#000" opacity=".22" filter="url(#b6)"/>')
    if leaves:
        for a, L in ((-68, 95), (68, 95), (-44, 110), (44, 110), (-20, 118), (20, 118), (0, 112)):
            out.append(mango_leaf(0, -198, L, 180 + a))
    if coco:
        out.append(coconut(0, -206, 1.0))
        out.append('<path d="M-30 -196 L0 -168 L30 -196 L22 -150 L-22 -150Z" fill="%s" opacity=".95"/>' % cloth)
    # foot
    out.append('<path d="M-46 0 L46 0 L36 -22 L-36 -22Z" fill="%s"/>' % body)
    out.append('<rect x="-40" y="-26" width="80" height="6" rx="3" fill="%s"/>' % lin(m[::-1], 0, 0, 1, 0))
    # body
    out.append('<path d="M-36 -22 C-110 -40 -104 -150 -40 -168 L40 -168 C104 -150 110 -40 36 -22Z" fill="%s"/>' % body)
    out.append('<path d="M-36 -22 C-110 -40 -104 -150 -40 -168 L40 -168 C104 -150 110 -40 36 -22Z" fill="%s"/>' % rad([(0, "#fff", .45), (.35, "#fff", 0), (1, "#000", .25)], .32, .35, .8))
    # bands
    out.append('<path d="M-94 -70 Q0 -52 94 -70" stroke="%s" stroke-width="7" fill="none"/>' % gold())
    out.append('<path d="M-92 -118 Q0 -104 92 -118" stroke="%s" stroke-width="5" fill="none"/>' % gold())
    for i in range(-4, 5):
        out.append('<circle cx="%d" cy="%.1f" r="3.2" fill="#FFF3C0"/>' % (i * 20, -61 - (16 - i * i) * .25))
    if sw:
        out.append(swastik(0, -94, 34, "#B3121D", 5))
        out.append('<circle cx="-40" cy="-94" r="5" fill="#E4A10E"/><circle cx="40" cy="-94" r="5" fill="#E4A10E"/>')
    # neck and rim
    out.append('<path d="M-40 -168 L-32 -186 L32 -186 L40 -168Z" fill="%s"/>' % body)
    if mauli:
        for k, c in enumerate(("#C1121F", "#F4B400", "#C1121F")):
            out.append('<rect x="-37" y="%d" width="74" height="4.5" fill="%s"/>' % (-181 + k * 5, c))
    out.append('<ellipse cx="0" cy="-189" rx="52" ry="11" fill="%s" stroke="%s" stroke-width="2"/>' % (lin(m[::-1], 0, 0, 1, 0), m[0]))
    out.append('<ellipse cx="-30" cy="-120" rx="12" ry="34" fill="#fff" opacity=".28" transform="rotate(14 -30 -120)"/>')
    out.append("</g>")
    return "".join(out)


def diya_flame(cx, cy, s=1):
    return ('<g transform="translate(%.1f %.1f) scale(%.3f)">'
            '<ellipse cx="0" cy="-18" rx="26" ry="34" fill="#FFB02E" opacity=".35" filter="url(#b6)"/>'
            '<path d="M0 -44 C12 -24 14 -8 0 0 C-14 -8 -12 -24 0 -44Z" fill="%s"/>'
            '<path d="M0 -30 C6 -18 6 -8 0 -3 C-6 -8 -6 -18 0 -30Z" fill="#FFF8D8"/></g>'
            % (cx, cy, s, lin(["#FF6A00", "#FFB300", "#FFE27A"], 0, 1, 0, 0)))


def clay_lamp(cx, cy, s=1, color="#B5561E"):
    f = lin(["#6E2A08", color, "#E09055", color, "#6E2A08"], 0, 0, 1, 0)
    return ('<g transform="translate(%.1f %.1f) scale(%.3f)"><path d="M-40 -6 Q0 36 40 -6 Q46 -12 56 -16 Q30 -2 0 -4 Q-30 -2 -40 -6Z" fill="%s"/>'
            '<ellipse cx="0" cy="-6" rx="40" ry="8" fill="#4a1d05"/>%s</g>' % (cx, cy, s, f, diya_flame(40, -12, .8)))


def milk_pot(cx, by, h, metal="brass", stove=True):
    """Brass pot of milk boiling over on a small clay stove. Base at by, height ~h."""
    s = h / 360.0
    m = METAL[metal]
    body = lin(m, 0, 0, 1, 0)
    milk = lin(["#FFFFFF", "#FFF8EA", "#EFE6D2"], 0, 0, 0, 1)
    out = ['<g transform="translate(%.1f %.1f) scale(%.3f)">' % (cx, by, s)]
    out.append('<ellipse cx="0" cy="2" rx="150" ry="16" fill="#000" opacity=".22" filter="url(#b6)"/>')
    if stove:
        clay = lin(["#6B2A10", "#A8502A", "#C9723F", "#A8502A", "#6B2A10"], 0, 0, 1, 0)
        out.append('<path d="M-120 0 L-108 -110 L108 -110 L120 0Z" fill="%s"/>' % clay)
        out.append('<path d="M-46 0 L-46 -64 Q0 -104 46 -64 L46 0Z" fill="#2b0d02"/>')
        # fire in mouth
        out.append('<ellipse cx="0" cy="-30" rx="48" ry="36" fill="#FF7A00" opacity=".6" filter="url(#b6)"/>')
        for dx, sc in ((-18, .8), (16, .9), (0, 1.1)):
            out.append('<path transform="translate(%d -6) scale(%.2f)" d="M0 -70 C18 -40 26 -18 0 0 C-26 -18 -18 -40 0 -70Z" fill="%s"/>' % (dx, sc, lin(["#E0200B", "#FF8A00", "#FFE066"], 0, 1, 0, 0)))
        out.append('<rect x="-60" y="-12" width="120" height="10" rx="4" fill="#5a2a0a" transform="rotate(-8)"/>')
        for i, c in enumerate(("#FFFFFF", "#F4C542", "#C1121F")):
            pass
        out.append('<path d="M-112 -76 H112 M-114 -46 H114" stroke="#FFF3E0" stroke-width="4" stroke-dasharray="2 10" stroke-linecap="round" opacity=".85"/>')
        out.append('<rect x="-126" y="-122" width="252" height="16" rx="6" fill="%s"/>' % lin(["#7a3414", "#b35e2f", "#7a3414"], 0, 0, 1, 0))
        oy = -118
    else:
        oy = 0
    out.append('<g transform="translate(0 %d)">' % oy)
    out.append('<path d="M-70 0 C-130 -10 -136 -120 -84 -150 L84 -150 C136 -120 130 -10 70 0Z" fill="%s"/>' % body)
    out.append('<path d="M-70 0 C-130 -10 -136 -120 -84 -150 L84 -150 C136 -120 130 -10 70 0Z" fill="%s"/>' % rad([(0, "#fff", .5), (.4, "#fff", 0), (1, "#000", .25)], .3, .35, .8))
    out.append('<path d="M-122 -64 Q0 -44 122 -64" stroke="%s" stroke-width="6" fill="none"/>' % gold())
    out.append(swastik(0, -96, 30, "#B3121D", 5))
    out.append('<path d="M-84 -150 L-96 -168 L96 -168 L84 -150Z" fill="%s"/>' % body)
    out.append('<ellipse cx="0" cy="-170" rx="100" ry="18" fill="%s" stroke="%s" stroke-width="3"/>' % (lin(m[::-1], 0, 0, 1, 0), m[0]))
    # milk surface and foam overflowing
    out.append('<ellipse cx="0" cy="-172" rx="92" ry="14" fill="%s"/>' % milk)
    drips = ("M-96 -170 C-104 -150 -110 -130 -104 -112 C-98 -104 -92 -118 -94 -136 C-92 -150 -86 -160 -80 -170Z",
             "M60 -172 C74 -150 88 -120 82 -86 C78 -74 68 -80 70 -100 C72 -126 58 -150 40 -170Z",
             "M-30 -176 C-40 -160 -38 -140 -30 -132 C-22 -130 -20 -146 -12 -170Z",
             "M96 -168 C110 -150 118 -120 112 -96 C108 -88 100 -94 102 -110 C104 -130 96 -150 84 -168Z")
    for d in drips:
        out.append('<path d="%s" fill="%s" stroke="#e8dcc6" stroke-width="1"/>' % (d, milk))
    rng = random.Random(4)
    foam = [(-70, -190, 30), (-30, -206, 38), (16, -210, 40), (58, -196, 32), (86, -182, 22), (-92, -178, 18), (-8, -236, 26), (36, -238, 22), (-48, -230, 20), (0, -258, 16)]
    for x, y, r in foam:
        out.append('<circle cx="%d" cy="%d" r="%d" fill="%s" stroke="#e4d8c0" stroke-width="1.2"/>' % (x, y, r, rad(["#FFFFFF", "#FFFDF6", "#E9E0CC"], .4, .35, .7)))
    for _ in range(10):
        x, y = rng.uniform(-80, 80), rng.uniform(-250, -190)
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#d8ccb2" stroke-width="1.2"/>' % (x, y, rng.uniform(3, 7)))
    # steam
    for dx in (-40, 10, 56):
        out.append('<path d="M%d -262 C%d -290 %d -300 %d -330 C%d -350 %d -364 %d -380" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" opacity=".45" filter="url(#b3)"/>' % (dx, dx - 16, dx + 14, dx, dx - 14, dx + 8, dx))
    out.append('</g></g>')
    return "".join(out)


# ------------------------------------------------------------------ griha pravesh items
def ornate_key(cx, cy, L, angle=0, ribbon="#C1121F", house_bow=False):
    """Ornate gold key, length L, centre of bow at (cx,cy), pointing along +x at angle."""
    s = L / 420.0
    g = gold(0, 0, 0, 1)
    dk = "#6B420A"
    out = ['<g transform="translate(%.1f %.1f) rotate(%.1f) scale(%.3f)" filter="url(#sh)">' % (cx, cy, angle, s)]
    # ribbon tails behind bow
    rb = lin([ribbon, "#FF5A5F", ribbon, "#7a0710"], 0, 0, 1, 1) if ribbon else ""
    if ribbon:
        out.append('<path d="M-40 30 C-70 90 -80 140 -110 190 L-80 180 L-66 206 C-50 150 -30 100 -20 40Z" fill="%s"/>' % rb)
        out.append('<path d="M-10 40 C0 100 20 150 10 210 L34 190 L56 206 C50 150 30 90 16 36Z" fill="%s"/>' % rb)
    if house_bow:
        out.append('<path d="M-70 40 L-70 -20 L0 -80 L70 -20 L70 40Z" fill="%s" stroke="%s" stroke-width="4"/>' % (g, dk))
        out.append('<path d="M-46 28 L-46 -12 L0 -52 L46 -12 L46 28Z" fill="none" stroke="%s" stroke-width="4"/>' % dk)
        out.append('<path d="M-14 28 V-2 A14 14 0 0 1 14 -2 V28" fill="%s" stroke="%s" stroke-width="3"/>' % ("#7a4a0a", dk))
        out.append('<rect x="-38" y="-14" width="16" height="16" fill="%s" stroke="%s" stroke-width="3"/><rect x="22" y="-14" width="16" height="16" fill="%s" stroke="%s" stroke-width="3"/>' % ("#FFF1BF", dk, "#FFF1BF", dk))
    else:
        for a in (0, 90, 180, 270):
            out.append('<circle cx="%.1f" cy="%.1f" r="30" fill="%s" stroke="%s" stroke-width="4"/>' % (46 * math.cos(math.radians(a)) - 0, 46 * math.sin(math.radians(a)), g, dk))
        out.append('<circle r="56" fill="%s" stroke="%s" stroke-width="5"/>' % (g, dk))
        out.append('<circle r="30" fill="none" stroke="%s" stroke-width="4"/>' % dk)
        for a in range(0, 360, 45):
            out.append('<ellipse cx="0" cy="-18" rx="6" ry="12" transform="rotate(%d)" fill="%s" stroke="%s" stroke-width="2"/>' % (a, "#FFF1BF", dk))
        out.append('<circle r="7" fill="#C1121F"/>')
    # collar + shaft
    out.append('<rect x="60" y="-16" width="26" height="32" rx="6" fill="%s" stroke="%s" stroke-width="4"/>' % (g, dk))
    out.append('<rect x="84" y="-10" width="310" height="20" rx="8" fill="%s" stroke="%s" stroke-width="4"/>' % (lin(GOLD, 0, 0, 0, 1), dk))
    out.append('<rect x="150" y="-15" width="14" height="30" rx="5" fill="%s" stroke="%s" stroke-width="3"/>' % (g, dk))
    # bit
    out.append('<path d="M300 8 V62 H330 V40 H350 V70 H380 V8Z" fill="%s" stroke="%s" stroke-width="4" stroke-linejoin="round"/>' % (lin(GOLD, 0, 0, 0, 1), dk))
    out.append('<path d="M100 -4 H380" stroke="#FFF6D4" stroke-width="4" opacity=".7"/>')
    if ribbon:
        # ribbon bow
        out.append('<g transform="translate(-20 44)">')
        out.append('<path d="M0 0 C-60 -50 -110 -20 -96 20 C-86 50 -40 30 0 0Z" fill="%s"/>' % rb)
        out.append('<path d="M0 0 C60 -50 110 -20 96 20 C86 50 40 30 0 0Z" fill="%s"/>' % rb)
        out.append('<path d="M-6 0 C-50 -30 -80 -12 -76 10" stroke="#7a0710" stroke-width="3" fill="none" opacity=".5"/>')
        out.append('<ellipse rx="18" ry="15" fill="%s"/>' % lin(["#7a0710", ribbon, "#FF6B6B"], 0, 1, 0, 0))

        out.append('</g>')
    out.append('</g>')
    return "".join(out)


def rangoli(cx, cy, r, cols=("#C2185B", "#FF9800", "#FFEB3B", "#2E7D32", "#1565C0", "#FFFFFF"), n=16, flat=1.0, rot=0):
    """Detailed rangoli seen with perspective squash flat (1 = top-down)."""
    c = cols
    out = ['<g transform="translate(%.1f %.1f) scale(1 %.3f) rotate(%.1f)">' % (cx, cy, flat, rot)]
    out.append('<circle r="%.1f" fill="%s"/>' % (r, c[5]))
    out.append('<circle r="%.1f" fill="%s"/>' % (r * .97, c[0]))
    # outer petals
    for k in range(n):
        a = k * 360.0 / n
        out.append('<path d="M0 %.1f C%.1f %.1f %.1f %.1f 0 %.1f C%.1f %.1f %.1f %.1f 0 %.1f" transform="rotate(%.1f)" fill="%s" stroke="%s" stroke-width="%.1f"/>'
                   % (-r * .55, r * .16, -r * .66, r * .1, -r * .9, -r * .96, -r * .1, -r * .9, -r * .16, -r * .66, -r * .55, a, c[1], c[5], r * .012))
        out.append('<circle cx="0" cy="%.1f" r="%.1f" transform="rotate(%.1f)" fill="%s"/>' % (-r * .72, r * .035, a, c[2]))
        out.append('<circle cx="0" cy="%.1f" r="%.1f" transform="rotate(%.1f)" fill="%s"/>' % (-r * .9, r * .028, a + 180.0 / n, c[5]))
    out.append('<circle r="%.1f" fill="%s" stroke="%s" stroke-width="%.1f"/>' % (r * .56, c[3], c[5], r * .014))
    for k in range(n):
        a = (k + .5) * 360.0 / n
        out.append('<circle cx="0" cy="%.1f" r="%.1f" transform="rotate(%.1f)" fill="%s"/>' % (-r * .5, r * .02, a, c[5]))
    m = n // 2
    for k in range(m):
        a = k * 360.0 / m
        out.append('<path d="M0 0 C%.1f %.1f %.1f %.1f 0 %.1f C%.1f %.1f %.1f %.1f 0 0" transform="rotate(%.1f)" fill="%s" stroke="%s" stroke-width="%.1f"/>'
                   % (r * .14, -r * .12, r * .12, -r * .38, -r * .46, -r * .12, -r * .38, -r * .14, -r * .12, a, c[4], c[5], r * .01))
        out.append('<path d="M0 %.1f C%.1f %.1f %.1f %.1f 0 %.1f C%.1f %.1f %.1f %.1f 0 %.1f" transform="rotate(%.1f)" fill="%s"/>'
                   % (-r * .1, r * .07, -r * .16, r * .06, -r * .3, -r * .36, -r * .06, -r * .3, -r * .07, -r * .16, -r * .1, a, c[2]))
    out.append('<circle r="%.1f" fill="%s" stroke="%s" stroke-width="%.1f"/>' % (r * .13, c[0], c[5], r * .012))
    out.append('<circle r="%.1f" fill="%s"/>' % (r * .06, c[2]))
    out.append('</g>')
    return "".join(out)


FOOT = "M0 -40 C14 -40 18 -20 16 0 C14 22 12 34 0 38 C-12 34 -14 18 -12 0 C-10 -16 -12 -40 0 -40Z"


def footprint(x, y, s=1, angle=0, color="#C8102E", left=False):
    fx = -1 if left else 1
    toes = [(-8, -50, 6.5), (2, -54, 5.2), (10, -51, 4.6), (16, -45, 4), (20, -37, 3.4)]
    t = "".join('<circle cx="%.1f" cy="%.1f" r="%.1f"/>' % (dx * fx, dy, r) for dx, dy, r in toes)
    return ('<g transform="translate(%.1f %.1f) rotate(%.1f) scale(%.3f)" fill="%s"><path d="%s" transform="scale(%d 1)"/>%s'
            '<circle cx="0" cy="-8" r="5" fill="#FFD54F" opacity=".9"/></g>' % (x, y, angle, s, color, FOOT, fx, t))


def footsteps(x0, y0, x1, y1, n=4, s=1, color="#C8102E"):
    out = []
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0)) + 90
    for i in range(n):
        t = i / max(1, n - 1)
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        off = 16 * s * (1 if i % 2 else -1)
        nx, ny = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        out.append(footprint(x + off * nx, y + off * ny, s * (0.75 + 0.25 * t) if y1 > y0 else s * (1 - 0.25 * t), ang, color, left=i % 2 == 0))
    return "".join(out)


def nameplate(x, y, w, h, metal="brass"):
    m = METAL[metal]
    return ('<g filter="url(#shs)"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s" stroke="%s" stroke-width="3"/>'
            '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="none" stroke="%s" stroke-width="2" opacity=".8"/>'
            '<circle cx="%.1f" cy="%.1f" r="3.5" fill="%s"/><circle cx="%.1f" cy="%.1f" r="3.5" fill="%s"/></g>'
            % (x, y, w, h, h * .18, lin(m, 0, 0, 1, 1), m[0], x + 8, y + 8, w - 16, h - 16, h * .12, m[0], x + 14, y + h / 2, m[0], x + w - 14, y + h / 2, m[0]))


def plant_pot(cx, by, s=1, pot="#B5561E", leaf="#2E7D32", kind="tulsi"):
    f = lin(["#5e2308", pot, "#E7945D", pot, "#5e2308"], 0, 0, 1, 0)
    out = ['<g transform="translate(%.1f %.1f) scale(%.3f)">' % (cx, by, s)]
    rng = random.Random(int(cx + by))
    if kind == "tulsi":
        for i in range(26):
            a = rng.uniform(-70, 70)
            L = rng.uniform(40, 80)
            x = math.sin(math.radians(a)) * L
            y = -60 - math.cos(math.radians(a)) * L
            out.append('<line x1="0" y1="-60" x2="%.1f" y2="%.1f" stroke="#4a6b1f" stroke-width="2"/>' % (x, y))
            out.append('<ellipse cx="%.1f" cy="%.1f" rx="9" ry="5" transform="rotate(%.1f %.1f %.1f)" fill="%s"/>' % (x, y, a - 90, x, y, rng.choice([leaf, "#43A047", "#1B5E20"])))
            if i % 4 == 0:
                out.append('<ellipse cx="%.1f" cy="%.1f" rx="3" ry="8" fill="#7B3F7A" transform="rotate(%.1f %.1f %.1f)"/>' % (x, y - 8, a, x, y - 8))
    else:
        for i in range(9):
            a = -60 + i * 15
            out.append(mango_leaf(0, -56, rng.uniform(60, 90), 180 + a, "#1B5E20", "#66BB6A"))
    out.append('<path d="M-42 -60 L42 -60 L32 0 L-32 0Z" fill="%s"/>' % f)
    out.append('<rect x="-48" y="-68" width="96" height="14" rx="4" fill="%s"/>' % f)
    out.append(swastik(0, -30, 18, "#FFF3C0", 3))
    out.append('</g>')
    return "".join(out)


def house(x, y, s=1, wall=("#FCE3B8", "#F2C98A"), trim="#8C2F0E", roof=("#9E2A12", "#C9481F"), night=False, storeys=2,
          door_glow="#FFE9A8", hues=("orange", "yellow"), kalash_metal="copper", rangoli_cols=None, variant=0):
    """Detailed two-storey house facade with open door, toran, kalash, rangoli. Local width 800, height 640 (base at y+640)."""
    out = ['<g transform="translate(%.1f %.1f) scale(%.3f)">' % (x, y, s)]
    wg = lin([wall[0], wall[1]], 0, 0, 0, 1)
    wside = lin([wall[1], wall[0]], 0, 0, 1, 0)
    trimg = lin([trim, "#000"], 0, 0, 0, 3)
    rf = lin([roof[1], roof[0]], 0, 0, 0, 1)
    win = rad([(0, door_glow, 1), (.6, "#FFC766", 1), (1, "#E08A1E", 1)], .5, .6, .8) if night else lin(["#CFE8F2", "#9CC7D8", "#E6F4F8"], 0, 0, 1, 1)
    out.append('<ellipse cx="400" cy="644" rx="440" ry="26" fill="#000" opacity=".25" filter="url(#b14)"/>')
    top = 40
    if storeys == 2:
        # upper storey
        out.append('<rect x="90" y="150" width="620" height="220" fill="%s"/>' % wg)
        out.append('<rect x="90" y="150" width="620" height="220" fill="url(#none)"/>')
        # roof
        out.append('<path d="M40 160 L400 %d L760 160 Z" fill="%s"/>' % (top, rf))
        for i in range(1, 9):
            yy = top + (160 - top) * i / 9
            half = 360 * (yy - top) / (160 - top)
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2" opacity=".5"/>' % (400 - half, yy, 400 + half, yy, roof[0]))
        out.append('<path d="M28 166 L400 %d L772 166" stroke="%s" stroke-width="14" fill="none" stroke-linejoin="round"/>' % (top - 8, trim))
        out.append('<circle cx="400" cy="%d" r="26" fill="%s" stroke="%s" stroke-width="4"/>' % (top + 58, win, trim))
        out.append('<path d="M400 %d v-40" stroke="%s" stroke-width="4"/><path d="M400 %d l44 12 l-44 12Z" fill="#F57C00"/>' % (top - 8, trim, top - 48))
        # upper windows
        for wx in (150, 355, 560):
            out.append('<rect x="%d" y="190" width="90" height="120" rx="6" fill="%s" stroke="%s" stroke-width="8"/>' % (wx, win, trim))
            out.append('<path d="M%d 190 v120 M%d 250 h90" stroke="%s" stroke-width="5"/>' % (wx + 45, wx, trim))
            out.append('<path d="M%d 182 h110 l-10 -14 h-90Z" fill="%s"/>' % (wx - 10, trim))
            if not night:
                out.append('<path d="M%d 200 l30 0 l-40 50Z" fill="#fff" opacity=".45"/>' % (wx + 6))
        # balcony
        out.append('<rect x="70" y="330" width="660" height="16" fill="%s"/>' % trimg)
        for i in range(34):
            bx = 82 + i * 19
            out.append('<rect x="%d" y="346" width="8" height="36" rx="3" fill="%s"/>' % (bx, trim))
        out.append('<rect x="70" y="380" width="660" height="12" fill="%s"/>' % trimg)
        out.append(garland_swag(80, 336, 280, 336, 34, 11, hues))
        out.append(garland_swag(280, 336, 520, 336, 38, 11, hues))
        out.append(garland_swag(520, 336, 720, 336, 34, 11, hues))
        gy = 392
    else:
        # single storey with tiled roof
        out.append('<path d="M10 330 L140 180 L660 180 L790 330Z" fill="%s"/>' % rf)
        for i in range(1, 7):
            yy = 180 + 150 * i / 7
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3" opacity=".45"/>' % (140 - 130 * i / 7, yy, 660 + 130 * i / 7, yy, roof[0]))
        for i in range(0, 25):
            xx = 150 + i * 21
            out.append('<line x1="%.1f" y1="180" x2="%.1f" y2="330" stroke="%s" stroke-width="1.5" opacity=".3"/>' % (xx, 10 + (xx - 10) * 1.0 if False else xx + (xx - 400) * 0.5, roof[0]))
        out.append('<path d="M0 334 L800 334" stroke="%s" stroke-width="14"/>' % trim)
        gy = 340
    # ground floor
    out.append('<rect x="50" y="%d" width="700" height="%d" fill="%s"/>' % (gy, 600 - gy, wg))
    out.append('<rect x="50" y="%d" width="700" height="%d" fill="%s" opacity=".12"/>' % (gy, 600 - gy, "#000"))
    out.append('<rect x="50" y="%d" width="40" height="%d" fill="%s" opacity=".35"/>' % (gy, 600 - gy, wside))
    out.append('<rect x="710" y="%d" width="40" height="%d" fill="#000" opacity=".08"/>' % (gy, 600 - gy))
    # side windows (arched with shutters)
    for wx in (110, 580):
        wy = gy + 60
        out.append('<path d="M%d %d v-60 a55 55 0 0 1 110 0 v60Z" fill="%s" stroke="%s" stroke-width="8"/>' % (wx, wy + 110, win, trim))
        out.append('<path d="M%d %d v-110 M%d %d h110" stroke="%s" stroke-width="5"/>' % (wx + 55, wy + 110, wx, wy + 40, trim))
        out.append('<path d="M%d %d v-120 l-26 12 v100Z" fill="%s" opacity=".9"/>' % (wx - 4, wy + 110, trim))
        out.append('<path d="M%d %d v-120 l26 12 v100Z" fill="%s" opacity=".9"/>' % (wx + 114, wy + 110, trim))
        out.append('<rect x="%d" y="%d" width="126" height="12" rx="3" fill="%s"/>' % (wx - 8, wy + 110, trimg))
        # flower box
        for k in range(6):
            out.append(marigold(wx + 8 + k * 19, wy + 106, 9, hues[k % 2]))
    # door frame
    dx0, dx1, dy0 = 300, 500, gy + 40
    out.append('<path d="M%d 600 V%d Q400 %d %d %d V600Z" fill="%s"/>' % (dx0 - 26, dy0 + 20, dy0 - 50, dx1 + 26, dy0 + 20, trimg))
    out.append('<path d="M%d 600 V%d Q400 %d %d %d V600Z" fill="%s"/>' % (dx0, dy0 + 30, dy0 - 22, dx1, dy0 + 30, rad([(0, "#FFFDF0", 1), (.45, door_glow, 1), (1, "#E0A040", 1)], .5, .75, .8)))
    # interior hint: floor & diya glow
    out.append('<path d="M%d 600 L%d 540 L%d 540 L%d 600Z" fill="#E9B85A" opacity=".55"/>' % (dx0, dx0 + 40, dx1 - 40, dx1))
    out.append('<ellipse cx="400" cy="%d" rx="70" ry="90" fill="#FFF7D6" opacity=".7" filter="url(#b14)"/>' % (dy0 + 120))
    # open door leaves (perspective)
    leaf = lin(["#5A2A0C", "#8B4513", "#A0582A"], 0, 0, 1, 0)
    out.append('<path d="M%d %d L%d %d L%d 588 L%d 600Z" fill="%s" stroke="#3a1a05" stroke-width="3"/>' % (dx0, dy0 + 30, dx0 + 56, dy0 + 58, dx0 + 56, dx0, leaf))
    out.append('<path d="M%d %d L%d %d L%d 588 L%d 600Z" fill="%s" stroke="#3a1a05" stroke-width="3"/>' % (dx1, dy0 + 30, dx1 - 56, dy0 + 58, dx1 - 56, dx1, lin(["#A0582A", "#8B4513", "#5A2A0C"], 0, 0, 1, 0)))
    for k in range(3):
        yy = dy0 + 80 + k * 55
        out.append('<path d="M%d %d L%d %d L%d %d L%d %d Z" fill="none" stroke="#E0A85A" stroke-width="2" opacity=".7"/>' % (dx0 + 10, yy, dx0 + 46, yy + 12, dx0 + 46, yy + 50, dx0 + 10, yy + 44))
        out.append('<path d="M%d %d L%d %d L%d %d L%d %d Z" fill="none" stroke="#E0A85A" stroke-width="2" opacity=".7"/>' % (dx1 - 10, yy, dx1 - 46, yy + 12, dx1 - 46, yy + 50, dx1 - 10, yy + 44))
    # toran above door
    out.append(toran(dx0 - 30, dx1 + 30, dy0 - 18, 50, strands=0))
    out.append(marigold_strand(dx0 - 18, dy0 - 16, 130, 10, hues))
    out.append(marigold_strand(dx1 + 18, dy0 - 16, 130, 10, hues))
    # nameplate
    out.append(nameplate(dx1 + 44, dy0 + 70, 86, 46))
    # steps
    for k, (w, c) in enumerate(((240, "#E9DCC6"), (280, "#DCCCB0"), (320, "#CBB896"))):
        yy = 600 + k * 16
        out.append('<path d="M%d %d h%d l10 16 h-%dZ" fill="%s"/>' % (400 - w / 2, yy, w, w + 20, c))
        out.append('<rect x="%.1f" y="%d" width="%d" height="16" fill="%s"/>' % (400 - w / 2 - 10, yy, w + 20, c))
    # kalash either side of steps
    out.append(kalash(236, 640, 150, kalash_metal))
    out.append(kalash(564, 640, 150, kalash_metal))
    out.append('</g>')
    return "".join(out)


def ornate_door(cx, by, w, h, wood=("#4A1F08", "#8B4513", "#B8703A"), frame="#6B2A0C", glow="#FFE9A8", hues=("orange", "yellow")):
    """Big close-up carved doorway, open, glowing interior; base at by (threshold)."""
    x0 = cx - w / 2
    y0 = by - h
    fw = w * .09
    out = []
    fg = lin([frame, "#A0552A", frame, "#3a1504"], 0, 0, 1, 0)
    # outer frame with carved bands
    out.append('<path d="M%.1f %.1f V%.1f Q%.1f %.1f %.1f %.1f V%.1fZ" fill="%s" filter="url(#sh)"/>' % (x0 - fw, by, y0 + h * .2, cx, y0 - h * .12, x0 + w + fw, y0 + h * .2, by, fg))
    # carved rosettes on frame
    n = 9
    for i in range(n):
        yy = y0 + h * .24 + i * (h * .74) / n
        for xx in (x0 - fw / 2, x0 + w + fw / 2):
            out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#E0A85A" stroke-width="2.5"/>' % (xx, yy, fw * .3))
            out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#E0A85A"/>' % (xx, yy, fw * .1))
    # interior
    out.append('<path d="M%.1f %.1f V%.1f Q%.1f %.1f %.1f %.1f V%.1fZ" fill="%s"/>' % (x0, by, y0 + h * .22, cx, y0 - h * .04, x0 + w, y0 + h * .22, by,
                                                                                  rad([(0, "#FFFFF6", 1), (.4, glow, 1), (1, "#D98F2B", 1)], .5, .62, .75)))
    # interior floor & back wall details
    out.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1fZ" fill="#D7A24E" opacity=".5"/>' % (x0, by, x0 + w * .2, by - h * .16, x0 + w * .8, by - h * .16, x0 + w, by))
    out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#FFFBE6" opacity=".8" filter="url(#b14)"/>' % (cx, by - h * .45, w * .25, h * .3))
    # open door leaves
    lg1 = lin([wood[0], wood[1], wood[2]], 0, 0, 1, 0)
    lg2 = lin([wood[2], wood[1], wood[0]], 0, 0, 1, 0)
    lw = w * .26
    out.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1fZ" fill="%s" stroke="#2a0f02" stroke-width="3"/>' % (x0, y0 + h * .22, x0 + lw, y0 + h * .3, x0 + lw, by - h * .05, x0, by, lg1))
    out.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1fZ" fill="%s" stroke="#2a0f02" stroke-width="3"/>' % (x0 + w, y0 + h * .22, x0 + w - lw, y0 + h * .3, x0 + w - lw, by - h * .05, x0 + w, by, lg2))
    for k in range(4):
        t0 = .3 + k * .16
        for side in (0, 1):
            xa = x0 if side == 0 else x0 + w
            xb = x0 + lw if side == 0 else x0 + w - lw
            ya0 = y0 + h * (.22 + (t0 - .22) * 1.0)
            pa = [(xa + (xb - xa) * .18, y0 + h * (t0 + .02)), (xa + (xb - xa) * .82, y0 + h * (t0 + .045)),
                  (xa + (xb - xa) * .82, y0 + h * (t0 + .135)), (xa + (xb - xa) * .18, y0 + h * (t0 + .14))]
            out.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1fZ" fill="#000" fill-opacity=".15" stroke="#E0A85A" stroke-width="2.5"/>' % sum(pa, ()))
            mx = sum(p[0] for p in pa) / 4
            my = sum(p[1] for p in pa) / 4
            out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (mx, my, lw * .07, gold()))
    # threshold
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (x0 - fw * 1.3, by, w + fw * 2.6, h * .035, lin(["#8A5A2B", "#5A3212"], 0, 0, 0, 1)))
    # toran & strands
    out.append(toran(x0 - fw, x0 + w + fw, y0 + h * .13, w * .12, strands=0, hues=hues))
    out.append(marigold_strand(x0 - fw * .5, y0 + h * .14, h * .5, w * .028, hues))
    out.append(marigold_strand(x0 + w + fw * .5, y0 + h * .14, h * .5, w * .028, hues))
    return "".join(out)


# ------------------------------------------------------------------ puja items
def temple_bell(cx, top, chain, size, metal="brass"):
    m = METAL[metal]
    out = ['<g filter="url(#shs)">']
    k = 0
    y = top
    while y < top + chain:
        if k % 2 == 0:
            out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" stroke-width="%.1f"/>' % (cx, y + size * .06, size * .045, size * .075, gold(), size * .025))
        else:
            out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" stroke-width="%.1f"/>' % (cx, y + size * .06, size * .02, size * .075, m[1], size * .022))
        y += size * .12
        k += 1
    s = size / 200.0
    b = lin(m, 0, 0, 1, 0)
    out.append('<g transform="translate(%.1f %.1f) scale(%.3f)">' % (cx, y, s))
    out.append('<circle cx="0" cy="6" r="14" fill="%s"/>' % b)
    out.append('<path d="M-22 26 C-24 16 24 16 22 26Z" fill="%s"/>' % b)
    out.append('<path d="M-22 26 C-60 36 -62 110 -70 150 C-78 176 -92 184 -96 196 L96 196 C92 184 78 176 70 150 C62 110 60 36 22 26Z" fill="%s"/>' % b)
    out.append('<path d="M-22 26 C-60 36 -62 110 -70 150 C-78 176 -92 184 -96 196 L96 196 C92 184 78 176 70 150 C62 110 60 36 22 26Z" fill="%s"/>' % rad([(0, "#fff", .5), (.35, "#fff", 0), (1, "#000", .3)], .35, .3, .8))
    out.append('<path d="M-60 90 Q0 100 60 90 M-70 150 Q0 162 70 150" stroke="%s" stroke-width="5" fill="none" opacity=".8"/>' % m[0])
    out.append('<path d="M-64 120 Q0 130 64 120" stroke="#FFF6D4" stroke-width="3" fill="none" opacity=".6"/>')
    out.append('<ellipse cx="0" cy="196" rx="98" ry="14" fill="%s" stroke="%s" stroke-width="3"/>' % (lin(m[::-1], 0, 0, 1, 0), m[0]))
    out.append('<ellipse cx="0" cy="197" rx="84" ry="8" fill="%s"/>' % m[0])
    out.append('<line x1="0" y1="190" x2="0" y2="222" stroke="%s" stroke-width="6"/><circle cx="0" cy="230" r="15" fill="%s"/>' % (m[0], b))
    out.append('<ellipse cx="-30" cy="90" rx="10" ry="40" fill="#fff" opacity=".3" transform="rotate(12 -30 90)"/>')
    out.append('</g></g>')
    return "".join(out)


def shankh(cx, cy, s=1, angle=0):
    body = lin(["#F7E9DD", "#FFFDF8", "#F2D7C6", "#E6BFA8"], 0, 0, 1, 1)
    inner = lin(["#F8B195", "#F67280", "#C06C84"], 0, 0, 1, 1)
    out = ['<g transform="translate(%.1f %.1f) rotate(%.1f) scale(%.3f)" filter="url(#sh)">' % (cx, cy, angle, s)]
    out.append('<path d="M-150 10 C-120 -60 -20 -90 60 -70 C120 -56 160 -20 170 10 C150 40 100 70 30 76 C-50 82 -120 60 -150 10Z" fill="%s" stroke="#C9A48C" stroke-width="3"/>' % body)
    # spire
    out.append('<path d="M-150 10 C-170 0 -196 -2 -214 8 C-196 18 -170 22 -150 10Z" fill="%s" stroke="#C9A48C" stroke-width="3"/>' % body)
    for k, x in enumerate((-150, -120, -86, -48)):
        out.append('<path d="M%d %d C%d %d %d %d %d %d" stroke="#C9A48C" stroke-width="3" fill="none"/>' % (x, -40 + k * 4, x - 10, -10, x - 8, 30, x + 6, 56 - k * 2))
    # aperture
    out.append('<path d="M10 -40 C80 -46 150 -20 168 8 C140 34 90 54 30 56 C60 30 50 -10 10 -40Z" fill="%s"/>' % inner)
    out.append('<path d="M20 -34 C70 -36 130 -18 150 6" stroke="#fff" stroke-width="3" fill="none" opacity=".6"/>')
    # knobs
    for x, y in ((-100, -52), (-60, -70), (-20, -80), (20, -80)):
        out.append('<circle cx="%d" cy="%d" r="8" fill="%s" stroke="#C9A48C" stroke-width="2"/>' % (x, y, body))
    out.append('<path d="M-130 -10 C-60 -50 20 -56 80 -48" stroke="#fff" stroke-width="6" fill="none" opacity=".7"/>')
    # gold cap band
    out.append('<path d="M-156 -14 C-150 10 -150 20 -140 40" stroke="%s" stroke-width="12" fill="none"/>' % gold())
    out.append('</g>')
    return "".join(out)


def _bez(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    u = 1 - t
    x = u**3*x0 + 3*u*u*t*x1 + 3*u*t*t*x2 + t**3*x3
    y = u**3*y0 + 3*u*u*t*y1 + 3*u*t*t*y2 + t**3*y3
    dx = 3*u*u*(x1-x0) + 6*u*t*(x2-x1) + 3*t*t*(x3-x2)
    dy = 3*u*u*(y1-y0) + 6*u*t*(y2-y1) + 3*t*t*(y3-y2)
    L = math.hypot(dx, dy) or 1
    return x, y, -dy / L, dx / L


def curved_leaf(p, W, greens=("#1B5E20", "#43A047", "#9CCC65"), rng=None, tears=3, vein="#DDEFB0", n=28, veins=16):
    """Broad banana-type leaf along cubic bezier midrib p=[(x,y)*4]; W = half width."""
    rng = rng or random.Random(1)
    A, B = [], []
    for i in range(n + 1):
        t = i / n
        x, y, nx, ny = _bez(p, t)
        w = W * min(1, (t / .12)) ** .6 * max(0, 1 - t ** 5) ** .5
        A.append((x + nx * w, y + ny * w)); B.append((x - nx * w * .92, y - ny * w * .92))
    mid = [(_bez(p, i / n)[0], _bez(p, i / n)[1]) for i in range(n + 1)]
    def poly(pts):
        return "M" + " L".join("%.1f %.1f" % q for q in pts)
    ga = lin([greens[0], greens[1], greens[2]], 0, 0, 1, 1)
    gb = lin([greens[0], greens[1]], 1, 1, 0, 0)
    out = ['<path d="%sZ" fill="%s"/>' % (poly(A + mid[::-1]), ga)]
    out.append('<path d="%sZ" fill="%s"/>' % (poly(B + mid[::-1]), gb))
    out.append('<path d="%sZ" fill="#000" opacity=".12"/>' % poly(B + mid[::-1]))
    # veins
    vv = []
    for i in range(2, veins):
        t = i / veins
        k = int(t * n)
        mx, my = mid[k]
        k2 = min(n, k + 3)
        vv.append("M%.1f %.1f L%.1f %.1f" % (mx, my, A[k2][0] * .96 + mx * .04, A[k2][1] * .96 + my * .04))
        vv.append("M%.1f %.1f L%.1f %.1f" % (mx, my, B[k2][0] * .96 + mx * .04, B[k2][1] * .96 + my * .04))
    out.append('<path d="%s" stroke="%s" stroke-width="1.4" opacity=".35" fill="none"/>' % (" ".join(vv), greens[0]))
    out.append('<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" stroke-linecap="round"/>' % (poly(mid[:-2]), vein, max(2, W * .09)))
    # tears (splits along veins)
    for _ in range(tears):
        k = rng.randint(int(n * .3), int(n * .85))
        side = A if rng.random() < .5 else B
        mx, my = mid[k]
        ex, ey = side[min(n, k + 3)]
        f = rng.uniform(.25, .55)
        out.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (ex, ey, ex + (mx - ex) * f, ey + (my - ey) * f, "#FFFFFF00"))
        out.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="2.4" opacity=".75"/>' % (ex, ey, ex + (mx - ex) * f, ey + (my - ey) * f, "#0b3510"))
    return "".join(out)


BANANA_TONES = [("#1B5E20", "#43A047", "#AED581"), ("#1E5631", "#3E9B55", "#B5D96A"), ("#2E5E1E", "#5A9A2A", "#C5E17A")]


def banana_plant(x, by, h, flip=False, seed=1, flower=False, tone=0):
    """Banana plant: layered pseudo-stem and broad arching torn leaves. Base (x,by), height ~h."""
    rng = random.Random(seed)
    s = h / 600.0
    sx = -s if flip else s
    greens = BANANA_TONES[tone % 3]
    out = ['<g transform="translate(%.1f %.1f) scale(%.3f %.3f)">' % (x, by, sx, s)]
    out.append('<ellipse cx="0" cy="0" rx="90" ry="14" fill="#000" opacity=".25" filter="url(#b6)"/>')
    stem = lin(["#4E6A20", "#8DAE4A", "#D4E39A", "#9DBE5A", "#56731F"], 0, 0, 1, 0)
    out.append('<path d="M-36 0 C-32 -140 -24 -260 -16 -330 L16 -330 C24 -260 32 -140 36 0Z" fill="%s"/>' % stem)
    for k in range(5):
        yy = -30 - k * 62
        out.append('<path d="M%d %d C%d %d %d %d %d %d" stroke="#5B6B22" stroke-width="3" fill="none" opacity=".55"/>' % (-30 + k * 3, yy, -10, yy - 30, 10, yy - 50, 22 - k * 2, yy - 70))
    out.append('<path d="M-30 -8 C-26 -120 -20 -230 -12 -320" stroke="#EEF5C8" stroke-width="5" fill="none" opacity=".35"/>')
    # leaves: (angle of emergence, length, droop)
    specs = [(-70, 300, .32), (72, 290, .34), (-44, 340, .16), (46, 330, .18), (-20, 360, .05), (18, 350, .04), (-2, 320, -.02)]
    back = specs[:2]
    for a, L, droop in specs:
        a += rng.uniform(-5, 5); L *= rng.uniform(.92, 1.05)
        ra = math.radians(a)
        dx, dy = math.sin(ra), -math.cos(ra)
        p0 = (0, -320)
        p1 = (dx * L * .3, -320 + dy * L * .4)
        p2 = (dx * L * .7, -320 + dy * L * .8 + L * droop * .3)
        p3 = (dx * L * 1.0, -320 + dy * L * .85 + L * droop * 1.0)
        out.append(curved_leaf([p0, p1, p2, p3], L * .13, greens, rng, tears=rng.randint(2, 4)))
    if flower:
        out.append('<path d="M6 -330 C60 -300 84 -240 80 -180" stroke="#6B7A2A" stroke-width="10" fill="none"/>')
        for k in range(4):
            yy = -300 + k * 22
            for j in range(4):
                out.append('<path d="M%d %d c10 -4 22 -2 30 8 c-12 4 -22 2 -30 -8Z" fill="%s" stroke="#6b7a2a" stroke-width="1"/>' % (38 + k * 8 + j * 6 - 14, yy + j * 3, lin(["#C5D86D", "#9CB43A"], 0, 0, 1, 1)))
        out.append('<path d="M80 -200 C110 -180 110 -120 80 -96 C50 -120 50 -180 80 -200Z" fill="%s"/>' % lin(["#4A148C", "#8E24AA", "#AD1457"], 0, 0, 1, 1))
        out.append('<path d="M72 -186 C80 -160 80 -130 76 -110" stroke="#fff" stroke-width="3" fill="none" opacity=".35"/>')
    out.append('</g>')
    return "".join(out)


def flames(cx, by, w, h, seed=3):
    rng = random.Random(seed)
    out = ['<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#FF7A00" opacity=".55" filter="url(#glow2)"/>' % (cx, by - h * .4, w * .7, h * .6)]
    layers = [(["#B71C1C", "#E65100", "#FF8F00"], 1.0), (["#E65100", "#FF9800", "#FFC107"], .78), (["#FF9800", "#FFD54F", "#FFF59D"], .55), (["#FFE082", "#FFFDE7", "#FFFFFF"], .3)]
    for cols, k in layers:
        f = lin(cols, 0, 1, 0, 0)
        n = 5 if k > .5 else 3
        for i in range(n):
            fx = cx + (i - (n - 1) / 2) * w * .22 * k + rng.uniform(-6, 6)
            fh = h * k * rng.uniform(.75, 1.0) * (1.0 if i == n // 2 else .8)
            fw = w * .28 * k + 6
            bend = rng.uniform(-.25, .25) * fw
            out.append('<path d="M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1fZ" fill="%s"/>'
                       % (fx - fw, by, fx - fw * 1.1, by - fh * .5, fx - fw * .2 + bend, by - fh * .7, fx + bend * 2, by - fh,
                          fx + fw * .4 + bend, by - fh * .6, fx + fw * 1.1, by - fh * .4, fx + fw, by, f))
    return "".join(out)


def sparks(rng, cx, by, w, h, n=30, color="#FFD54F"):
    out = []
    for _ in range(n):
        x = cx + rng.gauss(0, w * .35)
        y = by - rng.uniform(h * .3, h * 1.4)
        r = rng.uniform(1.5, 4.5)
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="%.2f" filter="url(#glow)"/>' % (x, y, r, color, rng.uniform(.5, 1)))
    return "".join(out)


def smoke(x, y, h, s=1, op=.35, seed=1, color="#FFFFFF", width=7):
    rng = random.Random(seed)
    out = []
    for k in range(3):
        dx = (k - 1) * 10 * s
        d = "M%.1f %.1f" % (x + dx, y)
        yy = y
        amp = 18 * s
        side = 1 if k % 2 else -1
        while yy > y - h:
            yy2 = yy - rng.uniform(50, 80) * s
            d += " C%.1f %.1f %.1f %.1f %.1f %.1f" % (x + dx + amp * side, yy - 20 * s, x + dx + amp * side, yy2 + 20 * s, x + dx, yy2)
            side *= -1
            amp *= 1.12
            yy = yy2
        out.append('<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" stroke-linecap="round" opacity="%.2f" filter="url(#b3)"/>' % (d, color, width * s * (1 - k * .25), op * (1 - k * .2)))
    return "".join(out)


def havan_kund(cx, by, w, metal="copper", seed=2, fire=True, fire_h=330, spark_n=26):
    """Stepped havan kund with logs and fire. Width w, base at by."""
    m = METAL[metal]
    s = w / 400.0
    out = ['<g transform="translate(%.1f %.1f) scale(%.3f)">' % (cx, by, s)]
    out.append('<ellipse cx="0" cy="6" rx="240" ry="26" fill="#000" opacity=".3" filter="url(#b6)"/>')
    tiers = [(120, 0, 44), (160, -44, 44), (200, -88, 44)]
    for i, (hw, y, th) in enumerate(tiers):
        f = lin(m, 0, 0, 1, 0)
        out.append('<path d="M%d %d L%d %d L%d %d L%d %dZ" fill="%s" stroke="%s" stroke-width="2"/>' % (-hw + 10, y, hw - 10, y, hw, y - th, -hw, y - th, f, m[0]))
        out.append('<path d="M%d %d L%d %d" stroke="#FFF1C8" stroke-width="3" opacity=".6"/>' % (-hw + 4, y - th + 4, hw - 4, y - th + 4))
        for k in range(-3, 4):
            out.append('<circle cx="%d" cy="%d" r="4" fill="%s"/>' % (k * hw / 4, y - th / 2, m[0]))
    top = -132
    out.append('<path d="M-200 %d L200 %d L170 %d L-170 %dZ" fill="#2a0d04"/>' % (top, top, top - 30, top - 30))
    # logs
    for a, dx in ((-14, -40), (12, 30), (-4, 0), (20, -70), (-22, 80)):
        out.append('<rect x="-70" y="-10" width="140" height="20" rx="10" transform="translate(%d %d) rotate(%d)" fill="%s" stroke="#2b1204" stroke-width="2"/>' % (dx, top - 14, a, lin(["#3b1b08", "#7a4a22", "#3b1b08"], 0, 0, 0, 1)))
    if fire:
        out.append(flames(0, top - 10, 230, fire_h, seed))
        out.append(sparks(random.Random(seed), 0, top - 60, 240, fire_h * .8, spark_n))
    # samagri bowls and ladle
    out.append('<g transform="translate(-270 0)"><ellipse cx="0" cy="-10" rx="46" ry="16" fill="%s"/><ellipse cx="0" cy="-24" rx="46" ry="12" fill="%s"/><ellipse cx="0" cy="-26" rx="38" ry="9" fill="#6D3B1A"/>' % (lin(m, 0, 0, 1, 0), lin(m[::-1], 0, 0, 1, 0)))
    for k in range(9):
        out.append('<circle cx="%d" cy="%d" r="3" fill="#C8A060"/>' % (-24 + k * 6, -30 - (k % 3) * 3))
    out.append('</g>')
    out.append('<g transform="translate(270 0)"><ellipse cx="0" cy="-10" rx="46" ry="16" fill="%s"/><ellipse cx="0" cy="-24" rx="46" ry="12" fill="%s"/><ellipse cx="0" cy="-26" rx="38" ry="9" fill="#F9D56E"/></g>' % (lin(m, 0, 0, 1, 0), lin(m[::-1], 0, 0, 1, 0)))
    out.append('<path d="M210 -40 L330 -110" stroke="%s" stroke-width="8" stroke-linecap="round"/><ellipse cx="206" cy="-36" rx="18" ry="10" fill="%s" transform="rotate(-30 206 -36)"/>' % (gold(), gold()))
    out.append('</g>')
    return "".join(out)


def thali(cx, cy, r, metal="brass", items=True, seed=5):
    """Puja thali (plate) in perspective with diya, kumkum, haldi, rice, flowers."""
    m = METAL[metal]
    rng = random.Random(seed)
    s = r / 200.0
    out = ['<g transform="translate(%.1f %.1f) scale(%.3f)">' % (cx, cy, s)]
    out.append('<ellipse cx="0" cy="30" rx="210" ry="66" fill="#000" opacity=".3" filter="url(#b6)"/>')
    out.append('<ellipse cx="0" cy="12" rx="204" ry="70" fill="%s"/>' % lin(m, 0, 0, 1, 0))
    out.append('<ellipse cx="0" cy="0" rx="204" ry="68" fill="%s" stroke="%s" stroke-width="3"/>' % (lin(m[::-1], 0, 0, 1, 1), m[0]))
    out.append('<ellipse cx="0" cy="2" rx="176" ry="56" fill="%s"/>' % lin(m, 0, 0, 1, 1))
    for k in range(36):
        a = math.radians(k * 10)
        out.append('<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (190 * math.cos(a), 62 * math.sin(a), "#FFF3C0"))
    out.append('<ellipse cx="0" cy="2" rx="120" ry="38" fill="none" stroke="%s" stroke-width="2" opacity=".7"/>' % m[0])
    out.append('<ellipse cx="-60" cy="-14" rx="70" ry="12" fill="#fff" opacity=".25"/>')
    if items:
        # flowers scattered (rose petals)
        for _ in range(22):
            a = rng.uniform(0, 6.28); rr = rng.uniform(100, 160)
            x, y = rr * math.cos(a), rr * math.sin(a) * .3 + 4
            out.append('<ellipse cx="%.1f" cy="%.1f" rx="9" ry="5" transform="rotate(%d %.1f %.1f)" fill="%s"/>' % (x, y, rng.randint(0, 180), x, y, rng.choice(["#C2185B", "#E91E63", "#AD1457", "#FF7043"])))
        # rice heap
        out.append('<ellipse cx="-110" cy="10" rx="40" ry="14" fill="#F4EEDD"/>')
        for _ in range(26):
            out.append('<ellipse cx="%.1f" cy="%.1f" rx="3.2" ry="1.6" fill="#fff" transform="rotate(%d)" />' % (-110 + rng.uniform(-32, 32), rng.uniform(-4, 14), 0))
        # kumkum & haldi bowls
        for bx, col in ((-40, "#C1121F"), (30, "#F2B705")):
            out.append('<ellipse cx="%d" cy="14" rx="32" ry="12" fill="%s"/><ellipse cx="%d" cy="6" rx="32" ry="10" fill="%s"/><path d="M%d 6 q26 -26 52 0Z" fill="%s"/>' % (bx, lin(m, 0, 0, 1, 0), bx, lin(m[::-1], 0, 0, 1, 0), bx - 26, col))
        out.append(clay_lamp(110, 8, .9))
        out.append(lotus(-10, -20, .22))
    out.append('</g>')
    return "".join(out)


def incense(cx, by, h, seed=2, smoke_c="#FFFFFF", smoke_op=.4):
    out = []
    ang = (-14, 0, 14)
    for i, a in enumerate(ang):
        x2 = cx + math.sin(math.radians(a)) * h
        y2 = by - math.cos(math.radians(a)) * h
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#5B2A0E" stroke-width="4" stroke-linecap="round"/>' % (cx, by, x2, y2))
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#8D5A3A" stroke-width="6" stroke-linecap="round"/>' % (cx + (x2 - cx) * .35, by + (y2 - by) * .35, x2, y2))
        out.append('<circle cx="%.1f" cy="%.1f" r="4" fill="#FF6F00" filter="url(#glow)"/>' % (x2, y2))
        out.append(smoke(x2, y2 - 4, h * 1.4, h / 260, smoke_op, seed + i, smoke_c))
    out.append('<path d="M%.1f %.1f q34 -34 68 0Z" fill="%s"/><rect x="%.1f" y="%.1f" width="84" height="10" rx="5" fill="%s"/>' % (cx - 34, by + 6, gold(), cx - 42, by + 4, gold()))
    return "".join(out)


OM_PATH = "M1203 1396Q1255 1396 1277.5 1426.0Q1300 1456 1300 1508V1518Q1300 1569 1277.5 1599.0Q1255 1629 1203 1629Q1151 1629 1128.0 1599.0Q1105 1569 1105 1518V1508Q1105 1456 1128.0 1426.0Q1151 1396 1203 1396ZM1558 1499 1405 1500V1470Q1405 1377 1355.0 1332.0Q1305 1287 1202 1287Q1098 1287 1049.5 1331.5Q1001 1376 1001 1469V1499H848Q845 1480 845.0 1469.0Q845 1458 845 1451Q845 1304 936.0 1228.0Q1027 1152 1202 1152Q1380 1152 1470.5 1228.0Q1561 1304 1561 1452Q1561 1459 1560.5 1469.5Q1560 1480 1558 1499ZM1081 344 1094 182Q1133 161 1182.5 149.5Q1232 138 1295 138Q1471 138 1567.5 237.0Q1664 336 1664 550V612Q1664 824 1580.0 925.5Q1496 1027 1320 1027Q1187 1027 1110.0 969.0Q1033 911 985 786L964 734Q946 687 926.0 661.0Q906 635 878.0 625.0Q850 615 809 615Q764 615 723.0 625.0Q682 635 643 646L691 548Q735 511 783.5 490.0Q832 469 891 469Q978 469 1027.5 506.5Q1077 544 1117 646L1138 700Q1174 794 1211.5 832.0Q1249 870 1316 870Q1397 870 1434.5 809.0Q1472 748 1472 613V569Q1472 468 1447.5 408.5Q1423 349 1376.5 322.5Q1330 296 1263 296Q1213 296 1167.5 308.5Q1122 321 1081 344ZM54 281 65 102Q136 62 228.0 39.5Q320 17 434 17Q576 17 668.0 54.0Q760 91 805.5 164.5Q851 238 851 349Q851 350 851.0 355.5Q851 361 851 362Q851 432 821.5 497.0Q792 562 732.5 607.0Q673 652 581 659V667Q673 677 729.0 714.5Q785 752 810.5 810.5Q836 869 836 943Q836 944 836.0 952.0Q836 960 836 961Q836 1066 794.0 1138.0Q752 1210 664.5 1247.5Q577 1285 440 1285Q340 1285 257.5 1267.0Q175 1249 111 1219L99 1051Q176 1088 253.5 1108.0Q331 1128 416 1128Q541 1128 594.0 1081.5Q647 1035 647 941Q647 941 647.0 933.5Q647 926 647 926Q647 864 620.5 824.5Q594 785 534.0 765.0Q474 745 372 742L223 738V589L382 584Q481 581 542.5 561.0Q604 541 632.0 500.5Q660 460 660 396Q660 394 660.0 386.0Q660 378 660 376Q660 272 599.5 224.5Q539 177 415 177Q311 177 223.5 204.5Q136 232 54 281Z"


def om_symbol(cx, cy, size, fill=None, stroke=None, sw=None):
    """Om drawn as a vector path (no font). size ~ glyph height."""
    fill = fill or gold(0, 0, 0, 1)
    s = size / 1612.0
    st = ' stroke="%s" stroke-width="%.1f" paint-order="stroke"' % (stroke, (sw or size * .03) / s) if stroke else ""
    return ('<path transform="translate(%.1f %.1f) scale(%.4f %.4f) translate(-859 -823)" d="%s" fill="%s"%s/>'
            % (cx, cy, s, -s, OM_PATH, fill, st))


def temple(cx, by, h, stone=("#F3D9A4", "#D9A95E", "#A86F2E"), flag="#F57C00", glow="#FFE9A8", silhouette=None):
    """Nagara-style temple: curvilinear shikhara, mandapa, steps. Base at by, height h."""
    s = h / 600.0
    out = ['<g transform="translate(%.1f %.1f) scale(%.3f)">' % (cx, by, s)]
    if silhouette:
        st = [silhouette, silhouette, silhouette]
        f1 = f2 = f3 = silhouette
    else:
        st = stone
        f1 = lin([stone[2], stone[0], stone[1], stone[2]], 0, 0, 1, 0)
        f2 = lin([stone[1], stone[0], stone[2]], 0, 0, 1, 0)
        f3 = lin([stone[0], stone[1]], 0, 0, 0, 1)
    # plinth & steps
    out.append('<rect x="-300" y="-40" width="600" height="40" fill="%s"/>' % f3)
    out.append('<rect x="-270" y="-70" width="540" height="30" fill="%s"/>' % f2)
    # main shikhara (behind)
    out.append('<path d="M-120 -250 C-120 -380 -70 -500 -20 -545 L20 -545 C70 -500 120 -380 120 -250Z" fill="%s"/>' % f1)
    if not silhouette:
        for k in range(1, 9):
            yy = -250 - k * 34
            t = (yy + 250) / -295.0
            hw = 120 - 100 * t ** 1.6
            out.append('<path d="M%.1f %.1f Q0 %.1f %.1f %.1f" stroke="%s" stroke-width="4" fill="none" opacity=".55"/>' % (-hw, yy, yy + 10, hw, yy, stone[2]))
        for xx in (-60, 0, 60):
            out.append('<path d="M%d -250 C%d -380 %d -480 %d -540" stroke="%s" stroke-width="3" fill="none" opacity=".45"/>' % (xx, xx * .9, xx * .5, xx * .15, stone[2]))
    out.append('<ellipse cx="0" cy="-552" rx="42" ry="12" fill="%s"/>' % f2)
    out.append('<ellipse cx="0" cy="-564" rx="30" ry="10" fill="%s"/>' % f1)
    out.append('<path d="M-10 -574 Q0 -610 10 -574Z" fill="%s"/><circle cx="0" cy="-606" r="9" fill="%s"/>' % (gold(), gold()))
    out.append('<line x1="0" y1="-606" x2="0" y2="-680" stroke="#5a3a1a" stroke-width="4"/>')
    out.append('<path d="M0 -680 L70 -662 L0 -640Z" fill="%s"/>' % flag)
    # side mini shikharas
    for sx in (-1, 1):
        out.append('<path d="M%d -200 C%d -270 %d -330 %d -350 L%d -350 C%d -330 %d -270 %d -200Z" fill="%s"/>' % (
            sx * 250, sx * 250, sx * 225, sx * 205, sx * 185, sx * 165, sx * 140, sx * 140, f2))
        out.append('<circle cx="%d" cy="-356" r="10" fill="%s"/>' % (sx * 195, gold()))
    # mandapa body
    out.append('<rect x="-250" y="-200" width="500" height="130" fill="%s"/>' % f2)
    out.append('<path d="M-270 -200 L-230 -250 L230 -250 L270 -200Z" fill="%s"/>' % f1)
    if not silhouette:
        for k in range(-4, 5):
            if abs(k) <= 1:
                continue
            out.append('<rect x="%d" y="-196" width="18" height="126" fill="%s" opacity=".55"/>' % (k * 52 - 9, stone[2]))
            out.append('<rect x="%d" y="-200" width="30" height="10" fill="%s"/>' % (k * 52 - 15, stone[2]))
    # door
    out.append('<path d="M-60 -70 V-150 Q0 -210 60 -150 V-70Z" fill="%s"/>' % (stone[2] if not silhouette else silhouette))
    out.append('<path d="M-44 -70 V-148 Q0 -192 44 -148 V-70Z" fill="%s"/>' % rad([(0, "#FFFFF0", 1), (.5, glow, 1), (1, "#E09A30", 1)], .5, .7, .8))
    out.append('<ellipse cx="0" cy="-110" rx="20" ry="30" fill="#FFF6D0" filter="url(#b6)"/>')
    out.append('</g>')
    return "".join(out)


def chowki(cx, by, w, h=80, cloth="#B71C1C", border="#F4C542"):
    out = []
    x0 = cx - w / 2
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (x0 + 20, by - h, 24, h, "#5A2A0C"))
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (x0 + w - 44, by - h, 24, h, "#5A2A0C"))
    top = by - h
    cl = lin([cloth, "#E53935", cloth, "#7F0000"], 0, 0, 1, 0)
    out.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f Z" fill="%s" filter="url(#shs)"/>' % (
        x0 - 10, top - 12, x0 + w + 10, top - 12, x0 + w + 16, top + h * .62, cx + w / 4, top + h * .7, cx, top + h * .62, cx - w / 4, top + h * .7, x0 - 16, top + h * .62, cl))
    out.append('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f Q%.1f %.1f %.1f %.1f" stroke="%s" stroke-width="8" fill="none"/>' % (
        x0 - 14, top + h * .55, cx - w / 4, top + h * .63, cx, top + h * .55, cx + w / 4, top + h * .63, x0 + w + 14, top + h * .55, border))
    for k in range(int(w / 26)):
        xx = x0 + 6 + k * 26
        out.append('<circle cx="%.1f" cy="%.1f" r="4" fill="%s"/>' % (xx, top + h * .66 + 4 * math.sin(k), border))
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="14" fill="%s"/>' % (x0 - 12, top - 18, w + 24, lin(["#7a3a14", "#b0662e", "#7a3a14"], 0, 0, 1, 0)))
    return "".join(out)


# ------------------------------------------------------------------ shop opening items
def coin(cx, cy, r, tilt=1.0, rot=0, emboss=True):
    g1 = lin(["#8A5A0E", "#E7B83E", "#FFF1B0", "#F2C94C", "#A8741E"], 0, 0, 1, 1)
    g2 = lin(["#FFF1B0", "#E0A93A", "#8A5A0E"], 0, 0, 1, 1)
    out = ['<g transform="translate(%.1f %.1f) rotate(%.1f) scale(1 %.3f)">' % (cx, cy, rot, tilt)]
    if tilt < .9:
        out.append('<ellipse cx="0" cy="%.1f" rx="%.1f" ry="%.1f" fill="#7A4E0E"/>' % (r * .16 / max(tilt, .2), r, r))
    out.append('<circle r="%.1f" fill="%s" stroke="#6E440A" stroke-width="%.1f"/>' % (r, g1, r * .04))
    out.append('<circle r="%.1f" fill="none" stroke="%s" stroke-width="%.1f"/>' % (r * .8, "#9C6A1A", r * .05))
    out.append('<circle r="%.1f" fill="%s"/>' % (r * .76, g2))
    if emboss:
        for a in range(0, 360, 45):
            out.append('<ellipse cx="0" cy="%.1f" rx="%.1f" ry="%.1f" transform="rotate(%d)" fill="none" stroke="#9C6A1A" stroke-width="%.1f"/>' % (-r * .32, r * .1, r * .24, a, r * .035))
        out.append('<circle r="%.1f" fill="#B8862A"/>' % (r * .12))
    for a in range(0, 360, 12):
        out.append('<line x1="0" y1="%.1f" x2="0" y2="%.1f" transform="rotate(%d)" stroke="#8A5A0E" stroke-width="%.1f" opacity=".6"/>' % (-r * .86, -r * .96, a, r * .025))
    out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#fff" opacity=".35" transform="rotate(-35)"/>' % (-r * .1, -r * .55, r * .5, r * .14))
    out.append('</g>')
    return "".join(out)


def coin_stack(cx, by, r, n, tilt=.34):
    out = ['<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#000" opacity=".25" filter="url(#b6)"/>' % (cx, by + 4, r * 1.2, r * tilt * 1.2)]
    th = r * .2
    side = lin(["#6E440A", "#C8962E", "#F9E39A", "#B07A1C", "#6E440A"], 0, 0, 1, 0)
    for i in range(n):
        y = by - i * th
        dx = ((i * 7) % 5 - 2) * r * .02
        out.append('<path d="M%.1f %.1f v%.1f a%.1f %.1f 0 0 0 %.1f 0 v%.1f Z" fill="%s" stroke="#6E440A" stroke-width="1"/>' % (cx + dx - r, y - th, th, r, r * tilt, 2 * r, -th, side))
        for k in range(10):
            xx = cx + dx - r + (k + .5) * 2 * r / 10
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#7A4E0E" stroke-width="1" opacity=".5"/>' % (xx, y - th + 2 + r * tilt * math.sqrt(max(0, 1 - ((xx - cx - dx) / r) ** 2)), xx, y - 2 + r * tilt * math.sqrt(max(0, 1 - ((xx - cx - dx) / r) ** 2))))
    top = by - n * th
    out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="#6E440A" stroke-width="1.5"/>' % (cx, top, r, r * tilt, lin(["#8A5A0E", "#F2C94C", "#FFF1B0", "#E7B83E"], 0, 0, 1, 1)))
    out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="#9C6A1A" stroke-width="2"/>' % (cx, top, r * .75, r * tilt * .75))
    return "".join(out)


def starburst(cx, cy, r, n=24, inner=.84, fill=None, stroke="#8A5A0E", rot=0):
    pts = []
    for i in range(n * 2):
        a = math.radians(rot + i * 180.0 / n)
        rr = r if i % 2 == 0 else r * inner
        pts.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy + rr * math.sin(a)))
    fill = fill or lin(["#FFF1B0", "#F2C94C", "#C8962E", "#F9E39A", "#B07A1C"], 0, 0, 1, 1)
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>' % (" ".join(pts), fill, stroke)


def confetti(rng, box, n, colors=("#F9E39A", "#E7B83E", "#FFF1B0", "#C8962E"), avoid=None, size=(8, 22)):
    x0, y0, x1, y1 = box
    out = []
    k = 0
    tries = 0
    while k < n and tries < n * 20:
        tries += 1
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if avoid and any(a[0] <= x <= a[2] and a[1] <= y <= a[3] for a in avoid):
            continue
        k += 1
        c = rng.choice(colors)
        s = rng.uniform(*size)
        r = rng.uniform(0, 180)
        t = rng.random()
        if t < .45:
            out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" transform="rotate(%.0f %.1f %.1f)"/>' % (x - s / 2, y - s / 4, s, s / 2, c, r, x, y))
        elif t < .7:
            out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (x, y, s / 4, c))
        elif t < .85:
            out.append('<path d="M%.1f %.1f q%.1f %.1f %.1f 0 t%.1f 0" stroke="%s" stroke-width="%.1f" fill="none" transform="rotate(%.0f %.1f %.1f)"/>' % (x - s, y, s / 2, -s / 2, s, s, c, s / 6, r, x, y))
        else:
            out.append(sparkle(x, y, s / 30, c))
    return "".join(out)


def ribbon_band(x0, y0, x1, y1, w=46, c=("#8E0B18", "#D7263D", "#FF6B6B")):
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
    L = math.hypot(x1 - x0, y1 - y0)
    f = lin([c[0], c[1], c[2], c[1], c[0]], 0, 0, 0, 1)
    return ('<g transform="translate(%.1f %.1f) rotate(%.2f)" filter="url(#shs)"><rect x="0" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>'
            '<line x1="0" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#FFD27A" stroke-width="3" opacity=".8"/><line x1="0" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#FFD27A" stroke-width="3" opacity=".8"/></g>'
            % (x0, y0, ang, -w / 2, L, w, f, -w / 2 + 5, L, -w / 2 + 5, w / 2 - 5, L, w / 2 - 5))


def ribbon_bow(cx, cy, s=1, c=("#8E0B18", "#D7263D", "#FF6B6B")):
    f = lin([c[0], c[1], c[2], c[1]], 0, 0, 1, 1)
    f2 = lin([c[2], c[1], c[0]], 0, 0, 1, 1)
    out = ['<g transform="translate(%.1f %.1f) scale(%.3f)" filter="url(#sh)">' % (cx, cy, s)]
    out.append('<path d="M-10 10 C-30 60 -60 110 -80 160 L-50 150 L-36 176 C-20 120 0 70 6 16Z" fill="%s"/>' % f2)
    out.append('<path d="M10 10 C30 60 50 110 70 166 L90 142 L112 156 C80 110 40 60 16 8Z" fill="%s"/>' % f)
    out.append('<path d="M0 0 C-70 -90 -170 -60 -150 10 C-136 60 -60 40 0 0Z" fill="%s"/>' % f)
    out.append('<path d="M0 0 C70 -90 170 -60 150 10 C136 60 60 40 0 0Z" fill="%s"/>' % f2)
    out.append('<path d="M-12 -4 C-70 -60 -130 -40 -124 6" stroke="%s" stroke-width="5" fill="none" opacity=".5"/>' % c[0])
    out.append('<path d="M12 -4 C70 -60 130 -40 124 6" stroke="%s" stroke-width="5" fill="none" opacity=".5"/>' % c[0])
    out.append('<path d="M-40 -30 C-80 -60 -120 -50 -130 -20" stroke="#fff" stroke-width="4" fill="none" opacity=".35"/>')
    out.append('<rect x="-26" y="-24" width="52" height="48" rx="16" fill="%s" stroke="%s" stroke-width="2"/>' % (lin([c[0], c[1], c[2]], 0, 1, 0, 0), c[0]))
    out.append('</g>')
    return "".join(out)


def scissors(cx, cy, s=1, angle=0, handle="#D7263D", open_=22):
    """Gold ceremonial scissors, pivot at (cx,cy), blades pointing along +x (rotated by angle)."""
    blade = lin(["#FFF8DC", "#F9E39A", "#C8962E", "#7A4E0E"], 0, 0, 0, 1)
    hg = lin([handle, "#FF8A8A", handle, "#5a0610"], 0, 0, 1, 1)
    out = ['<g transform="translate(%.1f %.1f) rotate(%.1f) scale(%.3f)" filter="url(#sh)">' % (cx, cy, angle, s)]
    for sgn in (1, -1):
        out.append('<g transform="rotate(%.1f)">' % (sgn * open_ / 2))
        # blade: wide at pivot, tapering to point, bevel highlight
        by = -8 * sgn
        out.append('<path d="M-10 %d L230 %d C250 %d 262 %d 270 0 C240 %d 120 %d -10 %dZ" fill="%s" stroke="#6E440A" stroke-width="2"/>'
                   % (by - 14 * sgn, by - 2 * sgn, by, -2 * sgn, 4 * sgn, 14 * sgn, 14 * sgn, blade))
        out.append('<path d="M10 %d L230 %d" stroke="#FFFBEA" stroke-width="3" opacity=".8"/>' % (by - 8 * sgn, by - 1 * sgn))
        # shank and ring handle on the opposite side
        out.append('<g transform="rotate(%.1f)">' % (-sgn * open_))
        out.append('<path d="M0 -8 L-70 -12 L-70 12 L0 8Z" fill="%s" stroke="#6E440A" stroke-width="2"/>' % gold(0, 0, 0, 1))
        out.append('<ellipse cx="-130" cy="%d" rx="62" ry="42" fill="none" stroke="#5a0610" stroke-width="26"/>' % (sgn * 10))
        out.append('<ellipse cx="-130" cy="%d" rx="62" ry="42" fill="none" stroke="%s" stroke-width="20"/>' % (sgn * 10, hg))
        out.append('<ellipse cx="-130" cy="%d" rx="62" ry="42" fill="none" stroke="%s" stroke-width="4" stroke-dasharray="3 7"/>' % (sgn * 10, "#FFE9A8"))
        out.append('</g></g>')
    out.append('<circle r="16" fill="%s" stroke="#6E440A" stroke-width="3"/><circle r="5" fill="#6E440A"/>' % gold())
    out.append('</g>')
    return "".join(out)


def money_pot(cx, by, h, metal="brass", cloth="#C1121F", seed=3):
    s = h / 360.0
    m = METAL[metal]
    rng = random.Random(seed)
    out = ['<g transform="translate(%.1f %.1f) scale(%.3f)">' % (cx, by, s)]
    out.append('<ellipse cx="0" cy="4" rx="170" ry="22" fill="#000" opacity=".28" filter="url(#b6)"/>')
    # spilled coins on ground
    for k in range(9):
        x = rng.choice([-1, 1]) * rng.uniform(110, 200)
        out.append(coin(x, rng.uniform(-10, 10), rng.uniform(18, 26), .38, rng.uniform(-10, 10), False))
    body = lin(m, 0, 0, 1, 0)
    out.append('<path d="M-60 0 C-170 -20 -176 -190 -80 -230 L80 -230 C176 -190 170 -20 60 0Z" fill="%s"/>' % body)
    out.append('<path d="M-60 0 C-170 -20 -176 -190 -80 -230 L80 -230 C176 -190 170 -20 60 0Z" fill="%s"/>' % rad([(0, "#fff", .5), (.4, "#fff", 0), (1, "#000", .25)], .3, .35, .8))
    out.append('<path d="M-150 -100 Q0 -76 150 -100" stroke="%s" stroke-width="7" fill="none"/>' % gold())
    out.append('<path d="M-146 -150 Q0 -128 146 -150" stroke="%s" stroke-width="5" fill="none"/>' % gold())
    out.append(swastik(0, -126, 36, "#B3121D", 5.5))
    out.append('<path d="M-80 -230 L-70 -250 L70 -250 L80 -230Z" fill="%s"/>' % body)
    out.append('<path d="M-76 -246 Q0 -222 76 -246 L70 -228 Q0 -206 -70 -228Z" fill="%s"/>' % cloth)
    out.append('<path d="M60 -232 q30 30 20 70 l-16 -6 q6 -34 -14 -56Z" fill="%s"/>' % cloth)
    out.append('<ellipse cx="0" cy="-252" rx="94" ry="18" fill="%s" stroke="%s" stroke-width="3"/>' % (lin(m[::-1], 0, 0, 1, 0), m[0]))
    # heap of coins
    heap = []
    for k in range(34):
        x = rng.gauss(0, 42)
        y = -262 - abs(rng.gauss(0, 1)) * 30 - (60 - min(60, abs(x))) * .8
        heap.append((y, x))
    for y, x in sorted(heap):
        out.append(coin(x, y, rng.uniform(20, 26), rng.uniform(.3, .6), rng.uniform(-30, 30), False))
    # spilling coins along side
    for k in range(5):
        out.append(coin(96 + k * 14, -236 + k * 44, 20, .5, 50 + k * 10, False))
    out.append('<ellipse cx="-50" cy="-150" rx="16" ry="50" fill="#fff" opacity=".28" transform="rotate(16 -50 -150)"/>')
    out.append('</g>')
    return "".join(out)


def awning(x0, y0, w, h, c1="#C62828", c2="#FFF6E5", n=10, scallop=True):
    """Striped scalloped awning, trapezoid from (x0,y0) width w, height h."""
    sw = w / n
    out = ['<g filter="url(#sh)">']
    inset = h * .18
    for i in range(n):
        xa = x0 + inset + i * (w - 2 * inset) / n
        xb = x0 + inset + (i + 1) * (w - 2 * inset) / n
        xc = x0 + i * sw
        xd = x0 + (i + 1) * sw
        out.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1fZ" fill="%s"/>' % (xa, y0, xb, y0, xd, y0 + h, xc, y0 + h, c1 if i % 2 == 0 else c2))
    out.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1fZ" fill="%s"/>' % (x0 + inset, y0, x0 + w - inset, y0, x0 + w, y0 + h, x0, y0 + h, lin([(0, "#000", .25), (.5, "#000", 0), (1, "#fff", .15)], 0, 0, 0, 1)))
    if scallop:
        for i in range(n):
            xc = x0 + (i + .5) * sw
            out.append('<path d="M%.1f %.1f a%.1f %.1f 0 0 0 %.1f 0Z" fill="%s"/>' % (xc - sw / 2, y0 + h - 1, sw / 2, sw * .45, sw, c1 if i % 2 == 0 else c2))
            out.append('<path d="M%.1f %.1f a%.1f %.1f 0 0 0 %.1f 0" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="3"/>' % (xc - sw / 2, y0 + h + 2, sw / 2, sw * .45, sw))
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="10" rx="5" fill="%s"/>' % (x0 + inset - 6, y0 - 6, w - 2 * inset + 12, gold()))
    out.append('</g>')
    return "".join(out)


def products_shelf(x, y, w, h, rng, palette=("#E53935", "#1E88E5", "#FDD835", "#43A047", "#8E24AA", "#FB8C00", "#00897B")):
    out = []
    rows = 3
    rh = h / rows
    for r in range(rows):
        yy = y + (r + 1) * rh
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="7" fill="#8D6E63"/>' % (x, yy - 7, w))
        xx = x + 6
        while xx < x + w - 24:
            kind = rng.random()
            c = rng.choice(palette)
            if kind < .45:
                bw, bh = rng.uniform(18, 34), rng.uniform(rh * .35, rh * .7)
                out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="%s"/><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#fff" opacity=".35"/>' % (xx, yy - 7 - bh, bw, bh, c, xx + 3, yy - 7 - bh * .7, bw - 6, bh * .2))
            elif kind < .75:
                bw, bh = rng.uniform(20, 28), rng.uniform(rh * .4, rh * .62)
                out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="%s" opacity=".85"/><rect x="%.1f" y="%.1f" width="%.1f" height="8" rx="2" fill="#5D4037"/>' % (xx, yy - 7 - bh, bw, bh, c, xx + 2, yy - 13 - bh, bw - 4))
            else:
                bw, bh = rng.uniform(26, 38), rng.uniform(rh * .3, rh * .5)
                out.append('<path d="M%.1f %.1f q%.1f %.1f %.1f 0 l-3 %.1f h-%.1f Z" fill="%s"/>' % (xx, yy - 7, bw / 2, -bh * 2.2, bw, 0, bw, c))
            xx += bw + rng.uniform(4, 10)
    return "".join(out)


def storefront(x, y, w, h, awn=("#C62828", "#FFF6E5"), wall=("#FFF3E0", "#F6D7B0"), trim="#3E2723", seed=4, ribbon=True, sign=True,
               sign_fill=None, glass=("#D7EEF7", "#9CCBDC")):
    """Shop facade. Local geometry scaled to w x h (base at y+h)."""
    s = w / 800.0
    sy = h / 620.0
    rng = random.Random(seed)
    out = ['<g transform="translate(%.1f %.1f) scale(%.3f %.3f)">' % (x, y, s, sy)]
    out.append('<ellipse cx="400" cy="626" rx="440" ry="22" fill="#000" opacity=".25" filter="url(#b14)"/>')
    out.append('<rect x="20" y="40" width="760" height="580" fill="%s"/>' % lin([wall[0], wall[1]], 0, 0, 0, 1))
    out.append('<rect x="0" y="20" width="800" height="30" fill="%s"/>' % lin([trim, "#6D4C41", trim], 0, 0, 0, 1))
    # sign board (blank, ornamental)
    sb = sign_fill or lin(["#1B1B2F", "#2E2E4A"], 0, 0, 0, 1)
    out.append('<rect x="120" y="66" width="560" height="96" rx="12" fill="%s" stroke="%s" stroke-width="7"/>' % (sb, gold()))
    out.append('<rect x="136" y="80" width="528" height="68" rx="8" fill="none" stroke="%s" stroke-width="2" opacity=".8"/>' % gold())
    for k in range(3):
        out.append(sparkle(250 + k * 150, 114, .9, "#F9E39A"))
    # awning
    out.append(awning(40, 176, 720, 96, awn[0], awn[1], 12))
    # windows
    gl = lin([glass[0], glass[1], glass[0]], 0, 0, 1, 1)
    for wx in (60, 520):
        out.append('<rect x="%d" y="310" width="220" height="250" fill="#FFF8EE"/>' % wx)
        out.append(products_shelf(wx + 10, 316, 200, 236, rng))
        out.append('<rect x="%d" y="310" width="220" height="250" fill="%s" opacity=".45"/>' % (wx, gl))
        out.append('<path d="M%d 310 l70 0 l-110 180 l0 -70Z" fill="#fff" opacity=".35"/>' % (wx + 60))
        out.append('<rect x="%d" y="310" width="220" height="250" fill="none" stroke="%s" stroke-width="12"/>' % (wx, trim))
        out.append('<rect x="%d" y="560" width="236" height="16" fill="%s"/>' % (wx - 8, trim))
    # door
    out.append('<rect x="316" y="300" width="168" height="300" fill="%s"/>' % rad([(0, "#FFFBEA", 1), (.6, "#FFE3A0", 1), (1, "#E3A24A", 1)], .5, .6, .8))
    out.append('<rect x="316" y="300" width="168" height="300" fill="none" stroke="%s" stroke-width="12"/>' % trim)
    out.append('<path d="M400 300 V600" stroke="%s" stroke-width="6"/>' % trim)
    out.append('<rect x="382" y="430" width="8" height="54" rx="4" fill="%s"/><rect x="410" y="430" width="8" height="54" rx="4" fill="%s"/>' % (gold(), gold()))
    out.append('<path d="M330 310 l40 0 l-50 90Z" fill="#fff" opacity=".4"/>')
    if sign:
        out.append('<path d="M370 300 L400 262 L430 300" stroke="%s" stroke-width="3" fill="none"/>' % gold())
        out.append('<rect x="352" y="326" width="96" height="52" rx="10" fill="%s" stroke="%s" stroke-width="4" filter="url(#shs)"/>' % (awn[0], gold()))
        out.append('<rect x="362" y="336" width="76" height="32" rx="6" fill="none" stroke="#fff" stroke-width="2" opacity=".8"/>')
        out.append(sparkle(400, 352, .55, "#FFF6D0"))
    # step
    out.append('<rect x="290" y="600" width="220" height="20" fill="#BCAAA4"/>')
    # plants
    out.append(plant_pot(290, 620, .55, "#6D4C41", kind="leafy"))
    out.append(plant_pot(510, 620, .55, "#6D4C41", kind="leafy"))
    # wall lamps
    for lx in (40, 760):
        out.append('<rect x="%d" y="300" width="8" height="30" fill="%s"/><path d="M%d 330 h28 l-6 34 h-16Z" fill="%s"/><ellipse cx="%d" cy="360" rx="30" ry="30" fill="#FFE9A8" opacity=".5" filter="url(#b6)"/>' % (lx - 4, trim, lx - 14, gold(), lx))
    if ribbon:
        out.append(ribbon_band(300, 450, 500, 450, 30))
        out.append(ribbon_bow(400, 450, .45))
    out.append('</g>')
    return "".join(out)


# ------------------------------------------------------------------ frames, panels, corners
def corner_flourish(x, y, s=1, rot=0, color=None, op=1):
    color = color or gold()
    d = ("M0 0 C40 0 70 10 90 40 C100 56 96 76 80 80 C64 84 58 66 70 58 "
         "M0 0 C0 40 10 70 40 90 C56 100 76 96 80 80 "
         "M20 20 C60 24 100 50 130 20 C140 8 156 10 160 22 "
         "M20 20 C24 60 50 100 20 130 C8 140 10 156 22 160")
    return ('<g transform="%s" opacity="%s"><path d="%s" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round"/>'
            '<circle cx="12" cy="12" r="9" fill="%s"/><circle cx="165" cy="26" r="6" fill="%s"/><circle cx="26" cy="165" r="6" fill="%s"/>'
            '<path d="M44 44 l14 -6 l-6 14 z" fill="%s"/></g>' % (T(x, y, s, rot), op, d, color, color, color, color, color))


def corners(x0, y0, x1, y1, s=1, color=None, op=1):
    return (corner_flourish(x0, y0, s, 0, color, op) + corner_flourish(x1, y0, s, 90, color, op) +
            corner_flourish(x1, y1, s, 180, color, op) + corner_flourish(x0, y1, s, 270, color, op))


def panel_rect(x0, y0, x1, y1, r=28, fill="#FFF8EC", stroke=None, inner=None, texture=True, shadow=True, op=1):
    stroke = stroke or gold()
    out = []
    f = ' filter="url(#shp)"' if shadow else ""
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s" fill-opacity="%s"%s/>' % (x0, y0, x1 - x0, y1 - y0, r, fill, op, f))
    if texture:
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s" fill-opacity="%s" filter="url(#paper)"/>' % (x0, y0, x1 - x0, y1 - y0, r, fill, op))
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="none" stroke="%s" stroke-width="6"/>' % (x0 + 12, y0 + 12, x1 - x0 - 24, y1 - y0 - 24, max(2, r - 10), stroke))
    if inner:
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="none" stroke="%s" stroke-width="2"/>' % (x0 + 24, y0 + 24, x1 - x0 - 48, y1 - y0 - 48, max(2, r - 18), inner))
    return "".join(out)


def arch_path(x0, y0, x1, y1, peak=None):
    """Mughal-ish pointed arch top, flat bottom."""
    w = x1 - x0
    cx = (x0 + x1) / 2
    sh = y0 + (peak or w * .36)
    return ("M%.1f %.1f V%.1f C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f V%.1fZ"
            % (x0, y1, sh, x0, sh - w * .2, cx - w * .2, y0 + w * .05, cx, y0,
               cx + w * .2, y0 + w * .05, x1, sh - w * .2, x1, sh, y1))


def scallop_border(x0, y0, x1, y1, r=14, color="#fff"):
    out = []
    n = int((x1 - x0) / (2 * r))
    for i in range(n):
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (x0 + r + i * 2 * r, y0, r, color))
    return "".join(out)


def bead_line(x0, y0, x1, y1, step=18, r=4, color=None):
    color = color or gold()
    L = math.hypot(x1 - x0, y1 - y0)
    n = int(L / step)
    return "".join('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n, r if i % 2 == 0 else r * .6, color) for i in range(n + 1))


def border_band(pid, c1, c2, c3, size=40):
    """Repeating ornamental band (small lotus-dot motif) as pattern for edge strips."""
    s = size
    inner = ('<rect width="%d" height="%d" fill="%s"/><path d="M%d %d L%d %d L%d %d L%d %dZ" fill="%s"/><circle cx="%d" cy="%d" r="%d" fill="%s"/>'
             '<circle cx="0" cy="%d" r="%d" fill="%s"/><circle cx="%d" cy="%d" r="%d" fill="%s"/>'
             % (s, s, c1, s / 2, s * .15, s * .85, s / 2, s / 2, s * .85, s * .15, s / 2, c2, s / 2, s / 2, s * .12, c3, s / 2, s * .08, c3, s, s / 2, s * .08, c3))
    return pattern_tile(pid, s, inner)


# ------------------------------------------------------------------ extra motifs (v2)
def spec(cat, n, zone, title, text, accent, tone="light", tfont="deco", align="center", photo=None):
    d = {"id": "E-%s-%d" % (cat, n), "tpl": True, "zone": [int(v) for v in zone],
         "colors": {"title": title, "text": text, "accent": accent}, "tone": tone, "title": tfont, "align": align}
    if photo:
        d["photo"] = photo
        d["slot"] = True
    return d


def write_specs(cat, specs):
    import json, os
    here = os.path.dirname(os.path.abspath(__file__))
    for s in specs:
        z = s["zone"]
        w, h = z[2] - z[0], z[3] - z[1]
        assert w >= 780 and h >= 700, (s["id"], w, h)
    json.dump(specs, open(os.path.join(here, "out", cat + ".json"), "w"), indent=1)


def lotus_pad(cx, cy, rx, ry=None, rot=0, c=("#1B5E3A", "#3E9B55", "#8BC34A")):
    ry = ry or rx * .32
    f = rad([c[2], c[1], c[0]], .45, .4, .7)
    notch = 14
    return ('<g transform="translate(%.1f %.1f) rotate(%.1f)"><ellipse cx="0" cy="4" rx="%.1f" ry="%.1f" fill="#000" opacity=".18"/>'
            '<path d="M0 0 L%.1f %.1f A%.1f %.1f 0 1 1 %.1f %.1f Z" fill="%s"/>'
            '<path d="M0 0 L%.1f 0 M0 0 L%.1f 0 M0 0 L0 %.1f M0 0 L%.1f %.1f M0 0 L%.1f %.1f" stroke="%s" stroke-width="1.5" opacity=".5"/></g>'
            % (cx, cy, rot, rx, ry, rx * math.cos(math.radians(-notch)), ry * math.sin(math.radians(-notch)), rx, ry,
               rx * math.cos(math.radians(notch)), ry * math.sin(math.radians(notch)), f,
               -rx * .9, rx * .9 * 0, ry * .9, -rx * .6, -ry * .7, rx * .6, -ry * .7, c[2]))


def ripples(cx, cy, rx, n=3, color="#FFFFFF", op=.35):
    return "".join('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" stroke-width="2" opacity="%.2f"/>'
                   % (cx, cy, rx * (1 + i * .45), rx * .18 * (1 + i * .45), color, op * (1 - i * .28)) for i in range(n))


def bell_beam(x0, x1, y, bells, metal="brass", wood=("#3E1A06", "#7A3E14")):
    """Carved wooden beam with bells hanging. bells: list of (x, chain, size)."""
    out = []
    for bx, ch, sz in bells:
        out.append(temple_bell(bx, y + 20, ch, sz, metal))
    out.append('<g filter="url(#sh)"><rect x="%.1f" y="%.1f" width="%.1f" height="44" rx="8" fill="%s"/>' % (x0, y - 10, x1 - x0, lin([wood[1], wood[0]], 0, 0, 0, 1)))
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="8" fill="%s"/>' % (x0, y + 26, x1 - x0, gold()))
    n = int((x1 - x0) / 36)
    for i in range(n):
        out.append('<circle cx="%.1f" cy="%.1f" r="6" fill="none" stroke="#E0A85A" stroke-width="2" opacity=".7"/>' % (x0 + 18 + i * 36, y + 10))
    out.append('</g>')
    return "".join(out)


def brick_pattern(pid, c1="#B5502E", c2="#9A3F22", mortar="#E8CDB4", w=90, h=36):
    inner = ('<rect width="%d" height="%d" fill="%s"/>' % (w, h * 2, mortar) +
             '<rect x="2" y="2" width="%d" height="%d" rx="3" fill="%s"/>' % (w - 4, h - 4, c1) +
             '<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s"/>' % (-w / 2 + 2, h + 2, w - 4, h - 4, c2) +
             '<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s"/>' % (w / 2 + 2, h + 2, w - 4, h - 4, c1))
    defs('<pattern id="%s" width="%d" height="%d" patternUnits="userSpaceOnUse">%s</pattern>' % (pid, w, h * 2, inner))
    return "url(#%s)" % pid


def tassel(x, y, s=1, c="#C1121F"):
    return ('<g transform="translate(%.1f %.1f) scale(%.2f)"><line x1="0" y1="0" x2="0" y2="16" stroke="%s" stroke-width="3"/>'
            '<circle cx="0" cy="20" r="8" fill="%s"/><path d="M-9 26 L9 26 L13 62 L-13 62Z" fill="%s"/>'
            '<path d="M-6 30 V60 M0 30 V62 M6 30 V60" stroke="#000" stroke-opacity=".25" stroke-width="1.5"/></g>' % (x, y, s, c, gold(), c))


def lotus_top(cx, cy, r, c=("#FCE4EC", "#F48FB1", "#C2185B")):
    """Lotus seen from above (flat-lay)."""
    out = ['<g transform="translate(%.1f %.1f)">' % (cx, cy)]
    for ring, (n, rr, col) in enumerate(((10, r, c[2]), (10, r * .78, c[1]), (8, r * .55, c[0]))):
        f = lin([col, "#FFFFFF"], 0, 0, 0, 1)
        for k in range(n):
            a = k * 360.0 / n + ring * 18
            out.append('<path d="M0 0 C%.1f %.1f %.1f %.1f 0 %.1f C%.1f %.1f %.1f %.1f 0 0Z" transform="rotate(%.1f)" fill="%s" stroke="%s" stroke-width="1.2"/>'
                       % (rr * .3, -rr * .3, rr * .22, -rr * .8, -rr, -rr * .22, -rr * .8, -rr * .3, -rr * .3, a, f, c[2]))
    out.append('<circle r="%.1f" fill="#F9C74F"/><circle r="%.1f" fill="#E9A23B" opacity=".6"/>' % (r * .18, r * .1))
    out.append('</g>')
    return "".join(out)


def petals(rng, box, n, colors=("#E65100", "#F9A825", "#C2185B", "#FB8C00"), avoid=None, s=(8, 16)):
    x0, y0, x1, y1 = box
    out = []
    k = t = 0
    while k < n and t < n * 30:
        t += 1
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if avoid and any(a[0] <= x <= a[2] and a[1] <= y <= a[3] for a in avoid):
            continue
        k += 1
        r = rng.uniform(*s)
        out.append('<path d="M0 0 C%.1f %.1f %.1f %.1f 0 %.1f C%.1f %.1f %.1f %.1f 0 0Z" transform="translate(%.1f %.1f) rotate(%d)" fill="%s" opacity=".92"/>'
                   % (r * .6, -r * .3, r * .5, -r * .9, -r * 1.1, -r * .5, -r * .9, -r * .6, -r * .3, x, y, rng.randint(0, 360), rng.choice(colors)))
    return "".join(out)


def stars(rng, box, n, color="#FFF6D0", avoid=None, op=(.4, 1)):
    x0, y0, x1, y1 = box
    out = []
    k = t = 0
    while k < n and t < n * 30:
        t += 1
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if avoid and any(a[0] <= x <= a[2] and a[1] <= y <= a[3] for a in avoid):
            continue
        k += 1
        if rng.random() < .15:
            out.append(sparkle(x, y, rng.uniform(.3, .6), color, rng.uniform(*op)))
        else:
            out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="%.2f"/>' % (x, y, rng.uniform(1, 2.6), color, rng.uniform(*op)))
    return "".join(out)
