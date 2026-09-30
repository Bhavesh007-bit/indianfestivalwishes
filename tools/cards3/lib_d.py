"""lib_d: shared SVG drawing helpers for inv-engagement, engagement and inv-baby-shower cards.

Every primitive returns an SVG markup string. Gradients used by a primitive are
emitted inline with unique ids, so pieces can be freely combined.
"""
import math, random

W, H = 1080, 1350
_n = [0]


def uid(p="g"):
    _n[0] += 1
    return "%s%d" % (p, _n[0])


def f(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


# ------------------------------------------------------------------ gradients
def lin(stops, x1=0, y1=0, x2=0, y2=1, units=None, gid=None):
    gid = gid or uid("l")
    u = ' gradientUnits="userSpaceOnUse"' if units else ""
    s = "".join('<stop offset="%s" stop-color="%s"%s/>' % (
        o, c, (' stop-opacity="%s"' % a) if a is not None else "") for o, c, a in _norm(stops))
    return gid, '<linearGradient id="%s" x1="%s" y1="%s" x2="%s" y2="%s"%s>%s</linearGradient>' % (
        gid, f(x1), f(y1), f(x2), f(y2), u, s)


def rad(stops, cx=0.5, cy=0.5, r=0.5, fx=None, fy=None, units=None, gid=None):
    gid = gid or uid("r")
    u = ' gradientUnits="userSpaceOnUse"' if units else ""
    fxy = ' fx="%s" fy="%s"' % (f(fx), f(fy)) if fx is not None else ""
    s = "".join('<stop offset="%s" stop-color="%s"%s/>' % (
        o, c, (' stop-opacity="%s"' % a) if a is not None else "") for o, c, a in _norm(stops))
    return gid, '<radialGradient id="%s" cx="%s" cy="%s" r="%s"%s%s>%s</radialGradient>' % (
        gid, f(cx), f(cy), f(r), fxy, u, s)


def _norm(stops):
    out = []
    n = len(stops)
    for i, s in enumerate(stops):
        if isinstance(s, str):
            out.append((f(i / max(1, n - 1)), s, None))
        elif len(s) == 2:
            out.append((f(s[0]), s[1], None))
        else:
            out.append((f(s[0]), s[1], s[2]))
    return out


def defs(*items):
    return "<defs>%s</defs>" % "".join(items)


# metal presets (vertical gradients)
GOLD = ["#8A5A12", "#E9C46A", "#FFF3C4", "#D4A437", "#9C6B17", "#F3D27A"]
ROSEGOLD = ["#8E4B3D", "#E7A58E", "#FFE3D6", "#D58C75", "#9A5646", "#F2C0AC"]
SILVER = ["#7D8591", "#DDE3EA", "#FFFFFF", "#B9C2CC", "#7F8893", "#E6ECF2"]
BRASS = ["#6E4308", "#C98B1E", "#FFE08A", "#E0A93A", "#8C5A10", "#F5C85A"]


def metal(stops=GOLD, vertical=True, gid=None):
    if vertical:
        return lin(stops, 0, 0, 0, 1, gid=gid)
    return lin(stops, 0, 0, 1, 1, gid=gid)


# ------------------------------------------------------------------ page
BASE_DEFS = """
<filter id="sh" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#2A1020" flood-opacity=".35"/></filter>
<filter id="shs" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#2A1020" flood-opacity=".35"/></filter>
<filter id="shb" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="16" stdDeviation="22" flood-color="#1E0A14" flood-opacity=".38"/></filter>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="bl2"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="bl6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="bl14" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="bl30" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="30"/></filter>
<filter id="paper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" seed="7" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.35  0 0 0 0 0.25  0 0 0 .07 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<filter id="silk" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".004 .06" numOctaves="2" seed="3" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .16 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
"""


def page(body, bg="#FFFFFF"):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">'
            '<defs>%s</defs><rect width="1080" height="1350" fill="%s"/>%s</svg>') % (BASE_DEFS, bg, body)


def grain(x=0, y=0, w=W, h=H, op=1.0):
    """subtle paper grain over a region"""
    return '<rect x="%s" y="%s" width="%s" height="%s" fill="#fff" filter="url(#paper)" opacity="%s"/>' % (x, y, w, h, op)


def silk(x, y, w, h, op=1.0, clip=None):
    c = ' clip-path="url(#%s)"' % clip if clip else ""
    return '<rect x="%s" y="%s" width="%s" height="%s" fill="#fff" filter="url(#silk)" opacity="%s"%s/>' % (x, y, w, h, op, c)


def bg_grad(stops, angle="v"):
    if angle == "v":
        gid, g = lin(stops, 0, 0, 0, 1)
    else:
        gid, g = lin(stops, 0, 0, 1, 1)
    return defs(g) + '<rect width="1080" height="1350" fill="url(#%s)"/>' % gid


def glow_spot(cx, cy, r, color, op=0.6):
    gid, g = rad([(0, color, op), (1, color, 0)])
    return defs(g) + '<circle cx="%s" cy="%s" r="%s" fill="url(#%s)"/>' % (f(cx), f(cy), f(r), gid)


def bokeh(seed, n, box, colors, rmin=6, rmax=34, op=(0.15, 0.55), blur=True):
    R = random.Random(seed)
    x0, y0, x1, y1 = box
    out = []
    for _ in range(n):
        r = R.uniform(rmin, rmax)
        c = R.choice(colors)
        o = R.uniform(*op)
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"%s/>' % (
            f(R.uniform(x0, x1)), f(R.uniform(y0, y1)), f(r), c, f(o), ' filter="url(#bl2)"' if blur and r > 14 else ""))
    return "<g>%s</g>" % "".join(out)


def sparkle(x, y, s, color="#FFF6D8", op=1.0, rot=0):
    d = "M0,-1 C.08,-.2 .2,-.08 1,0 C.2,.08 .08,.2 0,1 C-.08,.2 -.2,.08 -1,0 C-.2,-.08 -.08,-.2 0,-1Z"
    return ('<g transform="translate(%s %s) rotate(%s) scale(%s)" opacity="%s"><path d="%s" fill="%s"/>'
            '<circle r=".18" fill="#fff"/></g>') % (f(x), f(y), rot, f(s), op, d, color)


def sparkles(seed, n, box, color="#FFF4D0", smin=6, smax=18, op=(0.5, 1)):
    R = random.Random(seed)
    x0, y0, x1, y1 = box
    return "".join(sparkle(R.uniform(x0, x1), R.uniform(y0, y1), R.uniform(smin, smax), color, f(R.uniform(*op)), R.choice([0, 0, 45]))
                   for _ in range(n))


def dots_pattern(pid, size, r, color, op=0.25, offset=True):
    s = size
    extra = '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (s / 2, s / 2, r, color) if offset else ""
    return ('<pattern id="%s" width="%s" height="%s" patternUnits="userSpaceOnUse"><g opacity="%s">'
            '<circle cx="0" cy="0" r="%s" fill="%s"/><circle cx="%s" cy="0" r="%s" fill="%s"/><circle cx="0" cy="%s" r="%s" fill="%s"/>'
            '<circle cx="%s" cy="%s" r="%s" fill="%s"/>%s</g></pattern>') % (
        pid, s, s, op, r, color, s, r, color, s, r, color, s, s, r, color, extra)


def damask_pattern(pid, size, color, op=0.12):
    """ornamental lattice / damask style tile"""
    s = size
    h = s / 2
    m = ('<path d="M{h},{a} C{b},{c} {b},{d} {h},{e} C{g},{d} {g},{c} {h},{a}Z" fill="{col}"/>'
         '<path d="M{h},{e} C{i},{j} {k},{j} {h},{l} C{m},{j} {n},{j} {h},{e}Z" fill="{col}"/>'
         '<circle cx="0" cy="0" r="{r}" fill="{col}"/><circle cx="{s}" cy="0" r="{r}" fill="{col}"/>'
         '<circle cx="0" cy="{s}" r="{r}" fill="{col}"/><circle cx="{s}" cy="{s}" r="{r}" fill="{col}"/>'
         '<path d="M0,{h} Q{q},{h2} {h},{h} Q{q3},{h2} {s},{h}" stroke="{col}" stroke-width="{sw}" fill="none"/>'
         '<path d="M0,{h} Q{q},{h3} {h},{h} Q{q3},{h3} {s},{h}" stroke="{col}" stroke-width="{sw}" fill="none"/>'
         ).format(h=f(h), a=f(s * .12), b=f(h - s * .14), c=f(s * .22), d=f(s * .36), e=f(s * .44), g=f(h + s * .14),
                  i=f(h - s * .05), j=f(s * .47), k=f(h - s * .02), l=f(s * .56), m=f(h + s * .02), n=f(h + s * .05),
                  r=f(s * .06), s=f(s), q=f(s * .25), q3=f(s * .75), h2=f(h - s * .12), h3=f(h + s * .12), sw=f(s * .015), col=color)
    return ('<pattern id="%s" width="%s" height="%s" patternUnits="userSpaceOnUse"><g opacity="%s">%s</g></pattern>' % (
        pid, f(s), f(s), op, m))


def pattern_fill(pat_markup, pid, x=0, y=0, w=W, h=H, extra=""):
    return defs(pat_markup) + '<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)" %s/>' % (x, y, w, h, pid, extra)


# ------------------------------------------------------------------ shapes matching the engine's photo paths
def shape_d(shape, x, y, w, h):
    if shape == "arch":
        cx = x + w / 2
        sh = y + h * 0.34
        return ("M{x},{yh} L{x},{sh} C{x},{a} {b},{c} {d},{e} C{g},{i} {cx},{j} {cx},{y} C{cx},{j} {k},{i} {l},{e} "
                "C{m},{c} {xw},{a} {xw},{sh} L{xw},{yh} Z").format(
            x=f(x), yh=f(y + h), sh=f(sh), a=f(sh - h * .12), b=f(x + w * .18), c=f(y + h * .1), d=f(cx - w * .1),
            e=f(y + h * .045), g=f(cx - w * .04), i=f(y + h * .02), cx=f(cx), j=f(y + h * .01), y=f(y),
            k=f(cx + w * .04), l=f(cx + w * .1), m=f(x + w - w * .18), xw=f(x + w))
    if shape == "heart":
        cx = x + w / 2
        return "M{cx},{yh} C{a},{b} {x},{c} {cx},{d} C{xw},{c} {e},{b} {cx},{yh} Z".format(
            cx=f(cx), yh=f(y + h), a=f(x - w * .2), b=f(y + h * .55), x=f(x), c=f(y - h * .05), d=f(y + h * .22),
            xw=f(x + w), e=f(x + w * 1.2))
    if shape in ("rounded", "pill", "rect"):
        r = 28 if shape == "rounded" else (min(w, h) / 2 if shape == "pill" else 0)
        r = min(r, w / 2, h / 2)
        return ("M{a},{y} L{b},{y} A{r},{r} 0 0 1 {xw},{c} L{xw},{d} A{r},{r} 0 0 1 {b},{yh} L{a},{yh} "
                "A{r},{r} 0 0 1 {x},{d} L{x},{c} A{r},{r} 0 0 1 {a},{y} Z").format(
            a=f(x + r), b=f(x + w - r), y=f(y), r=f(r), xw=f(x + w), c=f(y + r), d=f(y + h - r), yh=f(y + h), x=f(x))
    if shape == "oval":
        rx, ry = w / 2, h / 2
        cx, cy = x + rx, y + ry
        return "M{a},{cy} A{rx},{ry} 0 1 1 {b},{cy} A{rx},{ry} 0 1 1 {a},{cy} Z".format(
            a=f(cx - rx), b=f(cx + rx), cy=f(cy), rx=f(rx), ry=f(ry))
    raise ValueError(shape)


def shape_grow(shape, x, y, w, h, d):
    """outline grown by d px (approximate for arch/heart, exact for others)."""
    if shape == "rounded":
        r = 28 + d
        X, Y, Wd, Hd = x - d, y - d, w + 2 * d, h + 2 * d
        return ("M{a},{y} L{b},{y} A{r},{r} 0 0 1 {xw},{c} L{xw},{e} A{r},{r} 0 0 1 {b},{yh} L{a},{yh} "
                "A{r},{r} 0 0 1 {x},{e} L{x},{c} A{r},{r} 0 0 1 {a},{y} Z").format(
            a=f(X + r), b=f(X + Wd - r), y=f(Y), r=f(max(r, 1)), xw=f(X + Wd), c=f(Y + r), e=f(Y + Hd - r), yh=f(Y + Hd), x=f(X))
    if shape == "heart":
        k = d * 1.25
        return shape_d(shape, x - k, y - d * 1.6, w + 2 * k, h + d * 2.6)
    return shape_d(shape, x - d, y - d, w + 2 * d, h + 2 * d)


def slot_placeholder(shape, x, y, w, h, fill="#F6EEE8", ink="#E3D3C8", kind="couple", pat_color=None):
    """Soft placeholder painted in the photo slot (visible when the user adds no photo)."""
    cid = uid("cp")
    d = shape_d(shape, x, y, w, h)
    gid, g = rad([(0, "#FFFFFF", .9), (1, fill, 1)], .5, .4, .7)
    cx, by = x + w / 2, y + h
    s = min(w, h * 0.9) / 400.0
    if kind == "couple":
        sil = ('<g transform="translate(%s %s) scale(%s)" fill="%s">'
               # man
               '<circle cx="-62" cy="-250" r="44"/>'
               '<path d="M-150,0 C-150,-120 -130,-185 -62,-190 C6,-185 26,-120 24,0Z"/>'
               # woman
               '<circle cx="64" cy="-232" r="40"/>'
               '<path d="M96,-262 C130,-250 128,-200 112,-170 C140,-150 150,-90 158,0 L-22,0 C-14,-90 -4,-150 22,-172 C10,-200 20,-262 64,-272Z"/>'
               '</g>') % (f(cx), f(by + 2), f(s), ink)
    elif kind == "mother":
        sil = ('<g transform="translate(%s %s) scale(%s)" fill="%s">'
               '<circle cx="-10" cy="-270" r="46"/><circle cx="34" cy="-300" r="22"/>'
               '<path d="M-90,0 C-100,-120 -80,-200 -10,-212 C40,-205 50,-170 58,-140 C110,-120 118,-60 90,-30 L96,0Z"/>'
               '</g>') % (f(cx), f(by + 2), f(s), ink)
    else:
        sil = ""
    pat = ""
    if pat_color:
        pid = uid("pp")
        pat = defs(dots_pattern(pid, 36, 2.2, pat_color, 0.5)) + '<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)"/>' % (
            x, y, w, h, pid)
    return (defs(g, '<clipPath id="%s"><path d="%s"/></clipPath>' % (cid, d)) +
            '<g clip-path="url(#%s)"><rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)"/>%s%s</g>' % (
                cid, x - 2, y - 2, w + 4, h + 4, gid, pat, sil))


def frame_ring(shape, x, y, w, h, metal_stops=GOLD, width=10, gap=0, inner_line=None, shadow=True):
    """Metallic frame band hugging the slot shape (drawn outside the slot)."""
    gid, g = lin(metal_stops, 0, 0, 1, 1)
    d_out = shape_grow(shape, x, y, w, h, gap + width)
    d_in = shape_grow(shape, x, y, w, h, gap) if gap else shape_d(shape, x, y, w, h)
    s = defs(g)
    s += '<path d="%s %s" fill="url(#%s)" fill-rule="evenodd"%s/>' % (d_out, _reverse_hint(d_in), gid, ' filter="url(#sh)"' if shadow else "")
    if inner_line:
        s += '<path d="%s" fill="none" stroke="%s" stroke-width="2"/>' % (shape_grow(shape, x, y, w, h, gap + width + 8), inner_line)
    return s


def _reverse_hint(d):
    return d


# ------------------------------------------------------------------ botanicals
def leaf(x, y, L, ang, c1="#5F8B4C", c2="#2F5A2A", wid=0.36, vein=True, op=1):
    gid, g = lin([c1, c2], 0, 0, 1, 1)
    w = L * wid
    d = "M0,0 C{a},{b} {c},{b} {L},0 C{c},{nb} {a},{nb} 0,0Z".format(a=f(L * .25), b=f(-w), c=f(L * .7), L=f(L), nb=f(w * .7))
    v = '<path d="M2,0 Q%s,%s %s,0" stroke="rgba(255,255,255,.35)" stroke-width="%s" fill="none"/>' % (
        f(L * .5), f(-w * .12), f(L * .92), f(max(1, L / 60))) if vein else ""
    return defs(g) + '<g transform="translate(%s %s) rotate(%s)" opacity="%s"><path d="%s" fill="url(#%s)"/>%s</g>' % (
        f(x), f(y), f(ang), op, d, gid, v)


def eucalyptus(x, y, L, ang, col="#8FAF9A", col2="#5E8570", n=7):
    """stem with round leaves"""
    out = ['<g transform="translate(%s %s) rotate(%s)">' % (f(x), f(y), f(ang))]
    out.append('<path d="M0,0 Q%s,%s %s,0" stroke="%s" stroke-width="3" fill="none"/>' % (f(L / 2), f(-L * .06), f(L), col2))
    gid, g = rad([col, col2], .35, .35, .8)
    out.append(defs(g))
    for i in range(n):
        t = (i + 0.6) / n
        px = L * t
        r = L * 0.075 * (1.1 - t * 0.45)
        side = -1 if i % 2 else 1
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%s)" transform="rotate(%s %s %s)"/>' % (
            f(px), f(side * r * 0.9 - L * .03), f(r), f(r * .82), gid, side * 25, f(px), f(side * r * .9)))
    out.append("</g>")
    return "".join(out)


def fern(x, y, L, ang, col="#7FA07A", n=12, op=1):
    out = ['<g transform="translate(%s %s) rotate(%s)" opacity="%s" fill="%s">' % (f(x), f(y), f(ang), op, col)]
    out.append('<path d="M0,0 Q%s,%s %s,0" stroke="%s" stroke-width="2" fill="none"/>' % (f(L / 2), f(-L * .05), f(L), col))
    for i in range(n):
        t = (i + 1) / (n + 1)
        l = L * 0.22 * (1 - t * 0.7)
        px = L * t
        for s in (-1, 1):
            out.append('<path d="M{px},0 Q{a},{b} {c},{d} Q{e},{g} {px},0Z"/>'.format(
                px=f(px), a=f(px + l * .3), b=f(s * l * .5), c=f(px + l * .55), d=f(s * l), e=f(px + l * .1), g=f(s * l * .5)))
    out.append("</g>")
    return "".join(out)


def rose(x, y, r, pal=("#7A0F2B", "#C2264B", "#F07A92"), rot=0, open_=1.0):
    """layered rose seen from above: outer petals, cupped middle, spiral centre."""
    dark, mid, light = pal
    g1, gg1 = rad([(0, dark), (0.55, mid), (1, light)], .5, .5, .5)
    g2, gg2 = rad([(0, dark), (0.7, mid), (1, light)], .5, .6, .6)
    out = [defs(gg1, gg2), '<g transform="translate(%s %s) rotate(%s)">' % (f(x), f(y), rot)]
    # outer petals
    for i in range(6):
        a = i * 60 + 15
        out.append('<path d="M0,0 C{a},{b} {c},{d} 0,{e} C{nc},{d} {na},{b} 0,0Z" fill="url(#{g})" transform="rotate({ang})" '
                   'stroke="{dk}" stroke-opacity=".25" stroke-width="{sw}"/>'.format(
            a=f(r * .55), b=f(-r * .25), c=f(r * .7), d=f(-r * .95), e=f(-r * 1.05 * open_), nc=f(-r * .7), na=f(-r * .55),
            g=g1, ang=a, dk=dark, sw=f(max(0.6, r / 40))))
    # middle cup petals
    for i in range(5):
        a = i * 72
        out.append('<path d="M0,0 C{a},{b} {c},{d} 0,{e} C{nc},{d} {na},{b} 0,0Z" fill="url(#{g})" transform="rotate({ang})" '
                   'stroke="{dk}" stroke-opacity=".3" stroke-width="{sw}"/>'.format(
            a=f(r * .4), b=f(-r * .15), c=f(r * .5), d=f(-r * .66), e=f(-r * .72), nc=f(-r * .5), na=f(-r * .4),
            g=g2, ang=a, dk=dark, sw=f(max(0.6, r / 40))))
    # centre
    out.append('<circle r="%s" fill="%s"/>' % (f(r * .42), mid))
    out.append('<path d="M{a},0 A{b},{b} 0 1 1 0,{nb} A{c},{c} 0 1 1 {d},0 A{e},{e} 0 1 1 0,{e}" fill="none" stroke="{dk}" '
               'stroke-width="{sw}" stroke-linecap="round" opacity=".75"/>'.format(
        a=f(r * .36), b=f(r * .36), nb=f(-r * .36), c=f(r * .25), d=f(-r * .14), e=f(r * .12), dk=dark, sw=f(max(1, r / 14))))
    out.append('<path d="M%s,%s A%s,%s 0 0 1 %s,%s" stroke="%s" stroke-width="%s" fill="none" opacity=".55" stroke-linecap="round"/>' % (
        f(-r * .3), f(-r * .3), f(r * .45), f(r * .45), f(r * .25), f(-r * .38), light, f(max(1, r / 18))))
    out.append("</g>")
    return "".join(out)


def rose_side(x, y, r, pal=("#7A0F2B", "#C2264B", "#F07A92"), rot=0):
    """rose bud seen from the side"""
    dark, mid, light = pal
    gid, g = lin([light, mid, dark], 0, 0, 0, 1)
    return (defs(g) + '<g transform="translate(%s %s) rotate(%s)">' % (f(x), f(y), rot) +
            '<path d="M0,{a} C{b},{c} {d},{e} {f_},{g} C{h},{i} {j},{k} 0,{l} C{nj},{k} {nh},{i} {nf},{g} C{nd},{e} {nb},{c} 0,{a}Z" fill="url(#{id})"/>'.format(
                a=f(r), b=f(r * .9), c=f(r * .8), d=f(r * .95), e=f(-r * .2), f_=f(r * .6), g=f(-r * .7), h=f(r * .35),
                i=f(-r * 1.05), j=f(r * .15), k=f(-r * .8), l=f(-r * .95), nj=f(-r * .15), nh=f(-r * .35), nf=f(-r * .6),
                nd=f(-r * .95), nb=f(-r * .9), id=gid) +
            '<path d="M{a},{b} C{c},{d} {e},{d} {g},{b}" stroke="{dk}" stroke-width="{sw}" fill="none" opacity=".5"/>'.format(
                a=f(-r * .6), b=f(-r * .55), c=f(-r * .2), d=f(-r * .1), e=f(r * .2), g=f(r * .6), dk=dark, sw=f(max(1, r / 12))) +
            '<path d="M{a},{b} C{c},{d} {e},{g} {h},{i}" stroke="{dk}" stroke-width="{sw}" fill="none" opacity=".45"/>'.format(
                a=f(-r * .75), b=f(r * .05), c=f(-r * .3), d=f(r * .55), e=f(r * .4), g=f(r * .4), h=f(r * .8), i=f(-r * .1), dk=dark,
                sw=f(max(1, r / 12))) +
            '<path d="M{a},{b} Q0,{c} {d},{b}" fill="#4E7A3A"/>'.format(a=f(-r * .7), b=f(r * .75), c=f(r * 1.25), d=f(r * .7)) +
            '</g>')


def blossom(x, y, r, petal="#F7C6D3", center="#E08AA2", n=5, rot=0, dot="#FFE9A8", op=1):
    gid, g = rad([(0, "#FFFFFF"), (1, petal)], .5, .9, .9)
    out = [defs(g), '<g transform="translate(%s %s) rotate(%s)" opacity="%s">' % (f(x), f(y), rot, op)]
    for i in range(n):
        out.append('<path d="M0,0 C{a},{b} {c},{d} 0,{e} C{nc},{d} {na},{b} 0,0Z" fill="url(#{g})" transform="rotate({ang})"/>'.format(
            a=f(r * .6), b=f(-r * .3), c=f(r * .6), d=f(-r * .95), e=f(-r), nc=f(-r * .6), na=f(-r * .6), g=gid, ang=f(i * 360 / n)))
    out.append('<circle r="%s" fill="%s"/>' % (f(r * .22), center))
    for i in range(6):
        a = math.radians(i * 60)
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(math.cos(a) * r * .3), f(math.sin(a) * r * .3), f(r * .06), dot))
    out.append("</g>")
    return "".join(out)


def peony(x, y, r, pal=("#E88AA0", "#F6BFCB", "#FFE7EC"), rot=0):
    """fluffy peony: many ruffled petals"""
    dark, mid, light = pal
    gid, g = rad([(0, dark), (0.6, mid), (1, light)], .5, .5, .55)
    out = [defs(g), '<g transform="translate(%s %s) rotate(%s)">' % (f(x), f(y), rot)]
    R = random.Random(int(x * 7 + y * 3))
    for layer, (rr, n) in enumerate([(1.0, 9), (0.78, 8), (0.56, 7), (0.36, 6)]):
        for i in range(n):
            a = i * 360 / n + layer * 17 + R.uniform(-6, 6)
            L = r * rr * R.uniform(.92, 1.05)
            wd = L * 0.55
            out.append('<path d="M0,0 C{a},{b} {c},{d} {e},{g} Q0,{h} {ne},{g} C{nc},{d} {na},{b} 0,0Z" fill="url(#{id})" '
                       'transform="rotate({ang})" stroke="{dk}" stroke-opacity=".18" stroke-width="1"/>'.format(
                a=f(wd), b=f(-L * .3), c=f(wd * 1.05), d=f(-L * .85), e=f(wd * .4), g=f(-L), h=f(-L * 1.08), ne=f(-wd * .4),
                nc=f(-wd * 1.05), na=f(-wd), id=gid, ang=f(a), dk=dark))
    out.append('<circle r="%s" fill="%s" opacity=".9"/>' % (f(r * .16), dark))
    out.append("</g>")
    return "".join(out)


def marigold_free_mum(x, y, r, col="#F4D35E", col2="#D99A2B"):
    """small pom-pom flower (chrysanthemum-like) for pastel sets"""
    out = ['<g transform="translate(%s %s)">' % (f(x), f(y))]
    for k, rr in enumerate([1, .75, .5]):
        n = int(18 * rr) + 4
        for i in range(n):
            a = i * 360 / n + k * 9
            out.append('<ellipse cx="0" cy="%s" rx="%s" ry="%s" fill="%s" transform="rotate(%s)"/>' % (
                f(-r * rr * .6), f(r * .12), f(r * rr * .42), col if k % 2 == 0 else col2, f(a)))
    out.append('<circle r="%s" fill="%s"/></g>' % (f(r * .18), col2))
    return "".join(out)


def gypso(seed, cx, cy, spread, n=18, col="#FFFFFF", r=(2.5, 5)):
    R = random.Random(seed)
    out = []
    for _ in range(n):
        a = R.uniform(0, math.tau)
        d = R.uniform(0, spread)
        px, py = cx + math.cos(a) * d, cy + math.sin(a) * d
        out.append('<path d="M%s,%s L%s,%s" stroke="#8FA88A" stroke-width="1"/>' % (f(cx), f(cy), f(px), f(py)))
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(px), f(py), f(R.uniform(*r)), col))
    return "".join(out)


def jasmine_bud(x, y, L, ang, col="#FFFFFF", tip="#F3E7C9"):
    gid, g = lin([col, tip], 0, 0, 1, 0)
    return defs(g) + '<g transform="translate(%s %s) rotate(%s)"><path d="M0,0 C%s,%s %s,%s %s,0 C%s,%s %s,%s 0,0Z" fill="url(#%s)" stroke="#D9CBB0" stroke-width=".6"/></g>' % (
        f(x), f(y), f(ang), f(L * .3), f(-L * .22), f(L * .8), f(-L * .12), f(L), f(L * .8), f(L * .12), f(L * .3), f(L * .22), gid)


def jasmine_flower(x, y, r, rot=0):
    out = ['<g transform="translate(%s %s) rotate(%s)">' % (f(x), f(y), rot)]
    for i in range(6):
        out.append('<ellipse cx="0" cy="%s" rx="%s" ry="%s" fill="#FFFFFF" stroke="#E4D8C0" stroke-width=".8" transform="rotate(%s)"/>' % (
            f(-r * .55), f(r * .28), f(r * .55), i * 60))
    out.append('<circle r="%s" fill="#F2D98A"/></g>' % f(r * .18))
    return "".join(out)


def strand(points, item, step=18, jitter=0, seed=1):
    """place `item(x,y,angle)` along a polyline (list of (x,y))"""
    out = []
    R = random.Random(seed)
    acc = 0
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        seg = math.hypot(x1 - x0, y1 - y0)
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        while acc <= seg:
            t = acc / seg if seg else 0
            out.append(item(x0 + (x1 - x0) * t + R.uniform(-jitter, jitter), y0 + (y1 - y0) * t + R.uniform(-jitter, jitter), ang))
            acc += step
        acc -= seg
    return "".join(out)


def catenary(x0, y0, x1, y1, sag, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)
        pts.append((x, y))
    return pts


def qbez(p0, p1, p2, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts


def pearl(x, y, r, col="#FFF8EE"):
    gid = "pearlg"
    return '<circle cx="%s" cy="%s" r="%s" fill="url(#pearlG)"/>' % (f(x), f(y), f(r))


PEARL_DEF = defs(rad([(0, "#FFFFFF"), (.5, "#F6EEE3"), (1, "#C8B8A6")], .35, .3, .75, gid="pearlG")[1])


def pearl_string(points, r=5, step=None):
    step = step or r * 2.1
    return PEARL_DEF + strand(points, lambda x, y, a: pearl(x, y, r), step=step)


def pts_d(points):
    return "M" + " L".join("%s,%s" % (f(x), f(y)) for x, y in points)


# ------------------------------------------------------------------ rings & jewels
def diamond(x, y, s, rot=0, tint="#EAF6FF"):
    """brilliant-cut diamond seen from the side (crown + pavilion facets)"""
    g1, a = lin(["#FFFFFF", tint, "#A9C6DD"], 0, 0, 1, 1)
    g2, b = lin(["#D5E9F7", "#8FB3CF", "#FFFFFF"], 0, 0, 1, 1)
    w, hc, hp = s, s * .32, s * .62
    return (defs(a, b) + '<g transform="translate(%s %s) rotate(%s)">' % (f(x), f(y), rot) +
            # pavilion
            '<path d="M%s,0 L%s,0 L0,%s Z" fill="url(#%s)"/>' % (f(-w / 2), f(w / 2), f(hp), g2) +
            '<path d="M%s,0 L0,%s L%s,0 Z" fill="#FFFFFF" opacity=".45"/>' % (f(-w * .18), f(hp), f(w * .05)) +
            '<path d="M%s,0 L0,%s L%s,0" fill="none" stroke="#7FA2BF" stroke-width="%s" opacity=".6"/>' % (f(-w * .36), f(hp), f(w * .36), f(s / 60)) +
            # crown
            '<path d="M%s,0 L%s,%s L%s,%s L%s,0 Z" fill="url(#%s)"/>' % (f(-w / 2), f(-w * .28), f(-hc), f(w * .28), f(-hc), f(w / 2), g1) +
            '<path d="M%s,%s L%s,0 L0,%s L%s,0 L%s,%s" fill="none" stroke="#9DBAD2" stroke-width="%s" opacity=".7"/>' % (
                f(-w * .28), f(-hc), f(-w * .18), f(-hc), f(w * .18), f(w * .28), f(-hc), f(s / 60)) +
            '<path d="M%s,%s L%s,%s L%s,0 Z" fill="#FFFFFF" opacity=".7"/>' % (f(-w * .28), f(-hc), f(-w * .05), f(-hc), f(-w * .3)) +
            '<line x1="%s" y1="0" x2="%s" y2="0" stroke="#FFFFFF" stroke-width="%s"/>' % (f(-w / 2), f(w / 2), f(s / 40)) +
            sparkle(-w * .1, -hc * .6, s * .28, "#FFFFFF", 1) +
            '</g>')


def ring(x, y, r, tilt=0.38, rot=0, metal_stops=GOLD, stone=True, band=None, stone_scale=1.0, back=True, front=True):
    """3D ring: elliptical band with depth, optional solitaire on top.
    back/front allow interlocking: draw back halves first, then front halves."""
    band = band or r * 0.16
    ry = r * tilt
    g_front, a = lin(metal_stops, 0, 0, 1, 1)
    g_back, b = lin(["#5E3A0C", "#A8792A", "#6E470F"] if metal_stops is GOLD else
                    ["#6B3A2E", "#B97C68", "#7A4538"] if metal_stops is ROSEGOLD else ["#5B626C", "#A9B2BC", "#646C76"], 0, 0, 1, 0)
    out = [defs(a, b), '<g transform="translate(%s %s) rotate(%s)">' % (f(x), f(y), rot)]
    if back:
        # back half (upper arc, seen through): darker, thinner
        out.append('<path d="M%s,0 A%s,%s 0 0 1 %s,0" fill="none" stroke="url(#%s)" stroke-width="%s"/>' % (
            f(-r), f(r), f(ry), f(r), g_back, f(band * 0.85)))
    if front:
        out.append('<path d="M%s,0 A%s,%s 0 0 0 %s,0" fill="none" stroke="url(#%s)" stroke-width="%s"/>' % (
            f(-r), f(r), f(ry), f(r), g_front, f(band)))
        # highlight on the front band
        out.append('<path d="M%s,%s A%s,%s 0 0 0 %s,%s" fill="none" stroke="#FFFBEA" stroke-width="%s" opacity=".75" stroke-linecap="round"/>' % (
            f(-r * .72), f(ry * .62), f(r), f(ry), f(r * .2), f(ry * .98), f(band * .22)))
        out.append('<path d="M%s,%s A%s,%s 0 0 0 %s,%s" fill="none" stroke="#5E3A0C" stroke-width="%s" opacity=".35"/>' % (
            f(-r * .98), f(band * .3), f(r), f(ry), f(r * .98), f(band * .3), f(band * .16)))
    if stone and back:
        s = r * 0.62 * stone_scale
        # setting / prongs at top of ring
        out.append('<path d="M%s,%s L%s,%s L%s,%s L%s,%s Z" fill="url(#%s)"/>' % (
            f(-s * .28), f(-ry - band * .2), f(-s * .42), f(-ry - s * .38), f(s * .42), f(-ry - s * .38), f(s * .28), f(-ry - band * .2), g_front))
        out.append(diamond(0, -ry - s * .72, s))
        for px in (-s * .42, s * .42):
            out.append('<path d="M%s,%s L%s,%s" stroke="url(#%s)" stroke-width="%s" stroke-linecap="round"/>' % (
                f(px * .8), f(-ry - s * .4), f(px * 1.05), f(-ry - s * .82), g_front, f(s * .06)))
    out.append("</g>")
    return "".join(out)


def interlocked_rings(x, y, r, metals=(GOLD, ROSEGOLD), stones=(True, False), rot=(-14, 16), sep=0.62, tilt=0.42):
    """Two rings interlinked: back halves, then fronts, so bands weave."""
    ax, bx = x - r * sep, x + r * sep
    ay, by = y, y + r * 0.1
    s = ""
    s += ring(ax, ay, r, tilt, rot[0], metals[0], stones[0], back=True, front=False)
    s += ring(bx, by, r * .92, tilt, rot[1], metals[1], stones[1], back=True, front=False)
    s += ring(ax, ay, r, tilt, rot[0], metals[0], False, back=False, front=True)
    s += ring(bx, by, r * .92, tilt, rot[1], metals[1], False, back=False, front=True)
    return s


def upright_ring(x, y, r, metal_stops=GOLD, rot=0, stone=True, stone_scale=1.0, band=None):
    """Ring standing upright (as in a box / held up): a near-circular band seen slightly from the side."""
    band = band or r * .18
    gid, g = lin(metal_stops, 0, 0, 1, 0)
    gi, gi_ = lin(["#6B4410", "#C4933A", "#6B4410"] if metal_stops is GOLD else ["#6B3A2E", "#C2877A", "#6B3A2E"] if metal_stops is ROSEGOLD
                  else ["#555D66", "#B6BEC7", "#555D66"], 0, 0, 1, 0)
    out = [defs(g, gi_), '<g transform="translate(%s %s) rotate(%s)">' % (f(x), f(y), rot)]
    out.append('<ellipse cx="0" cy="0" rx="%s" ry="%s" fill="none" stroke="url(#%s)" stroke-width="%s"/>' % (
        f(r * .78), f(r), gi, f(band * 1.05)))
    out.append('<ellipse cx="%s" cy="0" rx="%s" ry="%s" fill="none" stroke="url(#%s)" stroke-width="%s"/>' % (
        f(r * .08), f(r * .78), f(r), gid, f(band)))
    out.append('<path d="M%s,%s A%s,%s 0 0 1 %s,%s" fill="none" stroke="#FFFDF0" stroke-width="%s" opacity=".8" stroke-linecap="round"/>' % (
        f(-r * .55), f(r * .55), f(r * .78), f(r), f(-r * .55), f(-r * .55), f(band * .22)))
    if stone:
        s = r * .9 * stone_scale
        out.append('<path d="M%s,%s L%s,%s L%s,%s L%s,%s Z" fill="url(#%s)"/>' % (
            f(-s * .22), f(-r - band * .1), f(-s * .36), f(-r - s * .34), f(s * .36), f(-r - s * .34), f(s * .22), f(-r - band * .1), gid))
        out.append(diamond(0, -r - s * .66, s))
    out.append("</g>")
    return "".join(out)


def ring_box(x, y, s, velvet=("#5A0E1E", "#9E1B35", "#C8334F"), trim=GOLD, ring_metal=GOLD, open_=True, rings=1):
    """Open velvet ring box, front 3/4 view. (x,y) = bottom centre, s = width."""
    dk, md, lt = velvet
    gv, a = lin([lt, md, dk], 0, 0, 0, 1)
    gv2, b = lin([md, dk], 0, 0, 1, 0)
    gt, c = lin(trim, 0, 0, 1, 0)
    gc, d = rad([(0, lt), (1, dk)], .5, .3, .7)
    gl, e = lin([dk, md, dk], 0, 0, 1, 0)
    w = s
    hb = s * .5    # base height
    top = y - hb
    out = [defs(a, b, c, d, e), '<g>']
    # shadow
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#000" opacity=".28" filter="url(#bl14)"/>' % (f(x), f(y + 6), f(w * .6), f(w * .08)))
    if open_:
        # lid (open, behind): trapezoid going up
        lh = s * .62
        out.append('<path d="M{a},{t} L{b},{u} Q{x},{v} {c},{u} L{d},{t} Z" fill="url(#{g})"/>'.format(
            a=f(x - w / 2), t=f(top), b=f(x - w * .47), u=f(top - lh), x=f(x), v=f(top - lh - s * .06), c=f(x + w * .47), d=f(x + w / 2), g=gl))
        # lid inner satin
        out.append('<path d="M{a},{t} L{b},{u} Q{x},{v} {c},{u} L{d},{t} Z" fill="#F7EEE6"/>'.format(
            a=f(x - w * .43), t=f(top - s * .03), b=f(x - w * .41), u=f(top - lh + s * .07), x=f(x), v=f(top - lh + s * .02), c=f(x + w * .41), d=f(x + w * .43)))
        gs, sat = lin(["#FFFFFF", "#EADBD0", "#FFFFFF", "#E2D0C4"], 0, 0, 1, 1)
        out.append(defs(sat) + '<path d="M{a},{t} L{b},{u} Q{x},{v} {c},{u} L{d},{t} Z" fill="url(#{g})" opacity=".9"/>'.format(
            a=f(x - w * .43), t=f(top - s * .03), b=f(x - w * .41), u=f(top - lh + s * .07), x=f(x), v=f(top - lh + s * .02), c=f(x + w * .41), d=f(x + w * .43), g=gs))
        # gold trim on lid
        out.append('<path d="M{a},{t} L{b},{u} Q{x},{v} {c},{u} L{d},{t}" fill="none" stroke="url(#{g})" stroke-width="{sw}"/>'.format(
            a=f(x - w / 2), t=f(top), b=f(x - w * .47), u=f(top - lh), x=f(x), v=f(top - lh - s * .06), c=f(x + w * .47), d=f(x + w / 2), g=gt, sw=f(s * .018)))
    # base top surface (cushion area)
    out.append('<path d="M{a},{t} L{b},{t} L{c},{u} L{d},{u} Z" fill="url(#{g})"/>'.format(
        a=f(x - w / 2), t=f(top), b=f(x + w / 2), c=f(x + w * .46), u=f(top + s * .12), d=f(x - w * .46), g=gv2))
    # cushion
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%s)"/>' % (f(x), f(top + s * .04), f(w * .44), f(s * .1), gc))
    out.append('<path d="M%s,%s Q%s,%s %s,%s" stroke="%s" stroke-width="%s" fill="none"/>' % (
        f(x - w * .36), f(top + s * .03), f(x), f(top + s * .07), f(x + w * .36), f(top + s * .03), dk, f(s * .018)))
    # ring(s) in the slit
    if rings == 1:
        out.append(upright_ring(x, top - s * .14, s * .2, ring_metal, 0, True, 1.0))
    else:
        out.append(upright_ring(x - s * .14, top - s * .12, s * .16, ring_metal, -8, True, .9))
        out.append(upright_ring(x + s * .14, top - s * .11, s * .15, ROSEGOLD if ring_metal is GOLD else GOLD, 8, False))
    # front of base
    out.append('<path d="M{a},{u} L{b},{u} L{c},{y} Q{x},{yy} {d},{y} Z" fill="url(#{g})"/>'.format(
        a=f(x - w * .46), u=f(top + s * .12), b=f(x + w * .46), c=f(x + w * .46), y=f(y), x=f(x), yy=f(y + s * .02), d=f(x - w * .46), g=gv))
    out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)"/>' % (f(x - w * .46), f(top + s * .1), f(w * .92), f(s * .03), gt))
    out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)" opacity=".9"/>' % (f(x - w * .46), f(y - s * .04), f(w * .92), f(s * .02), gt))
    # clasp
    out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="url(#%s)"/>' % (f(x - s * .05), f(top + s * .12), f(s * .1), f(s * .09), f(s * .02), gt))
    # velvet sheen
    out.append('<path d="M%s,%s L%s,%s L%s,%s L%s,%s Z" fill="#fff" opacity=".08"/>' % (
        f(x - w * .4), f(top + s * .15), f(x - w * .25), f(top + s * .15), f(x - w * .32), f(y - s * .05), f(x - w * .44), f(y - s * .05)))
    out.append("</g>")
    return "".join(out)


# ------------------------------------------------------------------ thal and sweets
def thal(x, y, rx, metal_stops=BRASS, ry=None, depth=None, engraving=True):
    ry = ry or rx * .3
    depth = depth or rx * .07
    g, a = lin(metal_stops, 0, 0, 1, 0)
    g2, b = rad([(0, "#FFE7A0"), (.6, "#E3AE45"), (1, "#A56E14")], .45, .4, .65)
    out = [defs(a, b)]
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#000" opacity=".3" filter="url(#bl14)"/>' % (f(x), f(y + depth + 10), f(rx * 1.02), f(ry * .9)))
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%s)"/>' % (f(x), f(y + depth), f(rx), f(ry), g))
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%s)"/>' % (f(x), f(y), f(rx), f(ry), g))
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%s)"/>' % (f(x), f(y), f(rx * .86), f(ry * .84), g2))
    if engraving:
        n = 36
        for i in range(n):
            a_ = i * math.tau / n
            px, py = x + math.cos(a_) * rx * .93, y + math.sin(a_) * ry * .92
            out.append('<circle cx="%s" cy="%s" r="%s" fill="#8A5A10" opacity=".55"/>' % (f(px), f(py), f(rx * .012)))
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="#9C6A14" stroke-width="%s" opacity=".5" stroke-dasharray="%s %s"/>' % (
            f(x), f(y), f(rx * .72), f(ry * .7), f(rx * .01), f(rx * .03), f(rx * .02)))
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#FFF6D0" opacity=".35"/>' % (f(x - rx * .3), f(y - ry * .35), f(rx * .3), f(ry * .18)))
    return "".join(out)


def laddoo(x, y, r, col=("#E88A1A", "#F9C04A", "#B8620A")):
    g, a = rad([(0, col[1]), (.7, col[0]), (1, col[2])], .38, .35, .7)
    R = random.Random(int(x * 13 + y))
    dots = "".join('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".55"/>' % (
        f(x + R.uniform(-r * .7, r * .7)), f(y + R.uniform(-r * .7, r * .6)), f(r * .07), R.choice(["#FFE08A", "#A34E05"])) for _ in range(10))
    return defs(a) + '<circle cx="%s" cy="%s" r="%s" fill="url(#%s)" filter="url(#shs)"/>' % (f(x), f(y), f(r), g) + dots


def katli(x, y, s, rot=0):
    g, a = lin(["#FBF3E4", "#E9D8B8"], 0, 0, 1, 1)
    return defs(a) + '<g transform="translate(%s %s) rotate(%s) scale(1 .55)"><rect x="%s" y="%s" width="%s" height="%s" transform="rotate(45)" fill="url(#%s)" stroke="#CDBB98" stroke-width="1"/>' \
        '<rect x="%s" y="%s" width="%s" height="%s" transform="rotate(45)" fill="#EDEFF2" opacity=".85"/></g>' % (
            f(x), f(y), rot, f(-s / 2), f(-s / 2), f(s), f(s), g, f(-s * .38), f(-s * .38), f(s * .76), f(s * .76))


def coconut(x, y, r, wrap=None, rot=0):
    """coconut with tuft; optional wrap = (cloth colour, border colour) chunri wrap"""
    g, a = rad([(0, "#B07A45"), (.7, "#7A4B22"), (1, "#4E2C10")], .4, .35, .75)
    out = [defs(a), '<g transform="translate(%s %s) rotate(%s)">' % (f(x), f(y), rot)]
    out.append('<ellipse cx="0" cy="0" rx="%s" ry="%s" fill="url(#%s)"/>' % (f(r * .85), f(r), g))
    R = random.Random(int(x + y))
    for i in range(14):
        yy = R.uniform(-r * .8, r * .8)
        out.append('<path d="M%s,%s q%s,%s %s,%s" stroke="#3E220A" stroke-width="1.2" fill="none" opacity=".5"/>' % (
            f(-r * .6), f(yy), f(r * .6), f(R.uniform(-4, 4)), f(r * 1.2), f(R.uniform(-3, 3))))
    # tuft
    for k in range(7):
        out.append('<path d="M0,%s q%s,%s %s,%s" stroke="#8C5A2B" stroke-width="%s" fill="none" stroke-linecap="round"/>' % (
            f(-r * .95), f((k - 3) * r * .05), f(-r * .25), f((k - 3) * r * .09), f(-r * .35), f(r * .05)))
    if wrap:
        cl, bd = wrap
        gw, b = lin([cl, _shade(cl, -.25)], 0, 0, 1, 1)
        out.append(defs(b))
        out.append('<path d="M%s,%s C%s,%s %s,%s %s,%s L%s,%s C%s,%s %s,%s %s,%s Z" fill="url(#%s)"/>' % (
            f(-r * .86), f(-r * .05), f(-r * .6), f(r * .2), f(r * .6), f(r * .2), f(r * .86), f(-r * .05),
            f(r * .7), f(r * .7), f(r * .3), f(r * 1.06), f(-r * .3), f(r * 1.06), f(-r * .7), f(r * .7), gw))
        out.append('<path d="M%s,%s C%s,%s %s,%s %s,%s" stroke="%s" stroke-width="%s" fill="none"/>' % (
            f(-r * .86), f(-r * .05), f(-r * .6), f(r * .2), f(r * .6), f(r * .2), f(r * .86), f(-r * .05), bd, f(r * .1)))
        for i in range(9):
            out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(-r * .5 + i * r * .13), f(r * .45 + (i % 2) * r * .18), f(r * .035), bd))
    out.append('</g>')
    return "".join(out)


def _shade(hexc, k):
    hexc = hexc.lstrip("#")
    r, g, b = int(hexc[0:2], 16), int(hexc[2:4], 16), int(hexc[4:6], 16)
    if k < 0:
        r, g, b = [int(v * (1 + k)) for v in (r, g, b)]
    else:
        r, g, b = [int(v + (255 - v) * k) for v in (r, g, b)]
    return "#%02X%02X%02X" % (r, g, b)


shade = _shade


def dryfruits(seed, cx, cy, rx, ry, n=22):
    R = random.Random(seed)
    out = []
    for _ in range(n):
        a = R.uniform(0, math.tau)
        d = math.sqrt(R.uniform(0, 1))
        x, y = cx + math.cos(a) * rx * d, cy + math.sin(a) * ry * d
        kind = R.choice(["almond", "cashew", "pista"])
        rot = R.uniform(0, 360)
        if kind == "almond":
            out.append('<ellipse cx="%s" cy="%s" rx="7" ry="4" fill="#B5733A" transform="rotate(%s %s %s)" stroke="#7C4A1F" stroke-width=".8"/>' % (f(x), f(y), f(rot), f(x), f(y)))
        elif kind == "cashew":
            out.append('<path d="M%s,%s a7,7 0 1 0 8,-6 a3.5,3.5 0 1 1 -4,4" fill="#EED8AE" stroke="#C7A56E" stroke-width=".8" transform="rotate(%s %s %s)"/>' % (f(x - 4), f(y), f(rot), f(x), f(y)))
        else:
            out.append('<ellipse cx="%s" cy="%s" rx="5" ry="3.2" fill="#8DB255" transform="rotate(%s %s %s)" stroke="#5E7F32" stroke-width=".6"/>' % (f(x), f(y), f(rot), f(x), f(y)))
    return "".join(out)


def bowl(x, y, rx, metal_stops=SILVER, fill=None):
    g, a = lin(metal_stops, 0, 0, 1, 0)
    out = [defs(a)]
    ry = rx * .28
    out.append('<path d="M%s,%s Q%s,%s %s,%s Z" fill="url(#%s)"/>' % (f(x - rx), f(y), f(x), f(y + rx * 1.3), f(x + rx), f(y), g))
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (f(x), f(y), f(rx), f(ry), fill or "#E9EDF1"))
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="url(#%s)" stroke-width="3"/>' % (f(x), f(y), f(rx), f(ry), g))
    return "".join(out)


# ------------------------------------------------------------------ cloth, borders, ornaments
def gota_border_h(x, y, w, h, gold=GOLD, dot="#FFF3C4", scallop=True):
    g, a = lin(gold, 0, 0, 0, 1)
    out = [defs(a), '<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)"/>' % (f(x), f(y), f(w), f(h), g)]
    n = int(w / (h * 1.1))
    for i in range(n + 1):
        cx = x + i * w / n
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".85"/>' % (f(cx), f(y + h / 2), f(h * .18), dot))
        if scallop:
            out.append('<path d="M%s,%s a%s,%s 0 0 0 %s,0" fill="url(#%s)"/>' % (f(cx - h * .45), f(y + h), f(h * .45), f(h * .45), f(h * .9), g))
    return "".join(out)


def corner_filigree(x, y, s, sx=1, sy=1, col="url(#gfil)", stroke=None, op=1):
    """ornamental corner flourish. (x,y) corner point, sx/sy = direction (+1/-1)."""
    st = stroke or col
    p = ('<g transform="translate(%s %s) scale(%s %s)" opacity="%s" fill="none" stroke="%s" stroke-linecap="round">' % (
        f(x), f(y), f(sx * s / 100), f(sy * s / 100), op, st) +
        '<path d="M6,120 C6,50 50,6 120,6" stroke-width="4"/>'
        '<path d="M18,150 C14,70 70,14 150,18" stroke-width="2"/>'
        '<path d="M30,60 C44,40 60,34 80,40 C64,44 56,56 58,70 C46,62 36,62 30,60Z" fill="%s" stroke-width="1"/>'
        '<path d="M40,108 C54,98 70,100 80,112 C68,110 60,118 58,130" stroke-width="2.5"/>'
        '<path d="M108,40 C98,54 100,70 112,80 C110,68 118,60 130,58" stroke-width="2.5"/>'
        '<circle cx="24" cy="24" r="9" fill="%s" stroke-width="0"/>'
        '<circle cx="24" cy="24" r="16" stroke-width="2"/>'
        '<path d="M150,18 C170,20 186,12 196,4" stroke-width="2"/><path d="M18,150 C20,170 12,186 4,196" stroke-width="2"/>'
        '<circle cx="170" cy="10" r="4" fill="%s" stroke-width="0"/><circle cx="10" cy="170" r="4" fill="%s" stroke-width="0"/>'
        '</g>') % (col, col, col, col)
    return p


def gold_def(gid="gfil", stops=GOLD):
    return defs(lin(stops, 0, 0, 1, 1, gid=gid)[1])


def lace_edge_h(y, col="#FFFFFF", r=22, down=True, x0=0, x1=W, op=1, hole=True):
    """paper-cut scallop lace along a horizontal line."""
    out = ['<g fill="%s" opacity="%s">' % (col, op)]
    n = int((x1 - x0) / (r * 2)) + 1
    d = "M%s,%s " % (x0, y)
    for i in range(n):
        cx = x0 + i * r * 2 + r
        d += "A%s,%s 0 0 %d %s,%s " % (r, r, 0 if down else 1, cx + r, y)
    d += "L%s,%s L%s,%s Z" % (x1, y - (1 if down else -1) * 4, x0, y - (1 if down else -1) * 4)
    out.append('<path d="%s"/>' % d)
    out.append("</g>")
    if hole:
        holes = "".join('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".0"/>' % (x0 + i * r * 2 + r, y + (r * .5 if down else -r * .5), r * .22, col) for i in range(n))
        out.append(holes)
    return "".join(out)


def scallop_path_rect(x, y, w, h, r):
    """a rectangle whose edges are scalloped (for lace panels)."""
    d = "M%s,%s " % (f(x), f(y))
    n = max(1, int(round(w / (2 * r))))
    rr = w / n / 2
    for i in range(n):
        d += "A%s,%s 0 0 1 %s,%s " % (f(rr), f(rr), f(x + (i + 1) * 2 * rr), f(y))
    n2 = max(1, int(round(h / (2 * r))))
    r2 = h / n2 / 2
    for i in range(n2):
        d += "A%s,%s 0 0 1 %s,%s " % (f(r2), f(r2), f(x + w), f(y + (i + 1) * 2 * r2))
    for i in range(n):
        d += "A%s,%s 0 0 1 %s,%s " % (f(rr), f(rr), f(x + w - (i + 1) * 2 * rr), f(y + h))
    for i in range(n2):
        d += "A%s,%s 0 0 1 %s,%s " % (f(r2), f(r2), f(x), f(y + h - (i + 1) * 2 * r2))
    return d + "Z"


def rrect(x, y, w, h, r, fill, extra=""):
    return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" %s/>' % (f(x), f(y), f(w), f(h), f(r), fill, extra)


def panel(x, y, w, h, r=30, fill="#FFFBF4", stroke=None, sw=2, inset=12, inset_stroke=None, shadow="shb", op=1, grain_=True):
    out = ['<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" opacity="%s"%s/>' % (
        f(x), f(y), f(w), f(h), f(r), fill, op, ' filter="url(#%s)"' % shadow if shadow else "")]
    if grain_:
        cid = uid("pc")
        out.append(defs('<clipPath id="%s"><rect x="%s" y="%s" width="%s" height="%s" rx="%s"/></clipPath>' % (cid, f(x), f(y), f(w), f(h), f(r))))
        out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#fff" filter="url(#paper)" clip-path="url(#%s)"/>' % (f(x), f(y), f(w), f(h), cid))
    if stroke:
        out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (
            f(x), f(y), f(w), f(h), f(r), stroke, sw))
    if inset_stroke:
        out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="%s" stroke-width="1.5"/>' % (
            f(x + inset), f(y + inset), f(w - 2 * inset), f(h - 2 * inset), f(max(2, r - inset)), inset_stroke))
    return "".join(out)


# ------------------------------------------------------------------ birds & people
def lovebird(x, y, s, flip=False, body=("#F28FA8", "#D9577A", "#FFD1DC"), wing=("#E86C8C", "#B23A5C"), beak="#F2B544"):
    """perched lovebird, facing right (flip -> left). (x,y)= feet point"""
    b1, b2, b3 = body
    gb, a = rad([(0, b3), (.55, b1), (1, b2)], .6, .35, .8)
    gw, b = lin([wing[0], wing[1]], 0, 0, 1, 1)
    sx = -1 if flip else 1
    return (defs(a, b) + '<g transform="translate(%s %s) scale(%s %s)">' % (f(x), f(y), f(sx * s / 100), f(s / 100)) +
            # tail
            '<path d="M-40,-30 C-80,-18 -110,-4 -128,6 C-104,8 -76,0 -48,-12Z" fill="%s"/>' % wing[1] +
            '<path d="M-44,-24 C-84,-4 -104,12 -118,24 C-94,20 -70,6 -50,-8Z" fill="%s"/>' % wing[0] +
            # body
            '<path d="M-52,-30 C-50,-78 -8,-100 26,-96 C54,-94 70,-76 66,-54 C62,-26 34,-2 -2,2 C-30,4 -52,-6 -52,-30Z" fill="url(#%s)"/>' % gb +
            # head
            '<circle cx="42" cy="-86" r="30" fill="url(#%s)"/>' % gb +
            # wing
            '<path d="M-30,-60 C-2,-78 30,-66 36,-44 C24,-24 -8,-14 -44,-18 C-40,-34 -38,-48 -30,-60Z" fill="url(#%s)"/>' % gw +
            '<path d="M-20,-52 C0,-60 18,-54 24,-44 M-26,-40 C-4,-46 14,-40 20,-32 M-30,-28 C-10,-32 4,-28 10,-22" stroke="#fff" stroke-opacity=".35" stroke-width="2.5" fill="none"/>' +
            # beak
            '<path d="M68,-92 C82,-90 86,-80 80,-72 C76,-76 70,-78 64,-78Z" fill="%s"/>' % beak +
            # eye
            '<circle cx="54" cy="-92" r="5" fill="#2A1520"/><circle cx="55.5" cy="-93.5" r="1.6" fill="#fff"/>' +
            # blush
            '<ellipse cx="50" cy="-76" rx="8" ry="5" fill="#fff" opacity=".35"/>' +
            # feet
            '<path d="M6,0 l-4,10 M14,0 l2,10" stroke="#B5704A" stroke-width="3.5" stroke-linecap="round"/>' +
            '</g>')


def branch(points, width=10, col=("#6D4A33", "#9B7253")):
    g, a = lin(col, 0, 0, 0, 1)
    return defs(a) + '<path d="%s" stroke="url(#%s)" stroke-width="%s" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' % (
        points if isinstance(points, str) else pts_d(points), g, width)


def string_lights(points, step=46, bulb="#FFE6A0", glow="#FFC857", wire="#2B2238", r=7, seed=3):
    out = ['<path d="%s" stroke="%s" stroke-width="2.2" fill="none"/>' % (pts_d(points), wire)]
    gid, g = rad([(0, "#FFFFFF"), (.35, bulb), (1, glow, 0)])
    out.append(defs(g))

    def item(x, y, a):
        return ('<circle cx="%s" cy="%s" r="%s" fill="url(#%s)"/>'
                '<rect x="%s" y="%s" width="%s" height="%s" rx="1.5" fill="%s"/>'
                '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>'
                '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#FFFFFF" opacity=".8"/>') % (
            f(x), f(y + r * 1.6), f(r * 3.4), gid, f(x - r * .45), f(y - 1), f(r * .9), f(r * .8), wire,
            f(x), f(y + r * 1.4), f(r * .72), f(r * 1.05), bulb, f(x - r * .2), f(y + r * 1.1), f(r * .22), f(r * .4))
    out.append(strand(points, item, step=step))
    return "".join(out)


def couple_silhouette(x, y, s, col="#2A1633"):
    """Man & woman facing each other, foreheads close, holding hands (full length). (x,y)=ground centre."""
    return ('<g transform="translate(%s %s) scale(%s)" fill="%s">' % (f(x), f(y), f(s / 100), col) +
            # man (left) head
            '<ellipse cx="-38" cy="-322" rx="16" ry="19"/>'
            '<path d="M-52,-332 C-50,-346 -30,-348 -22,-336 C-26,-338 -40,-338 -52,-332Z"/>'
            # neck + torso (kurta) + legs
            '<path d="M-44,-306 L-32,-306 L-30,-296 C-14,-292 -6,-284 -4,-268 L2,-220 L-6,-218 L-12,-250 L-14,-196 '
            'C-12,-160 -12,-130 -14,-104 L-16,-4 L-22,0 L-34,0 L-34,-6 L-28,-8 L-32,-100 L-40,-100 L-44,-6 L-38,-4 L-40,0 L-58,0 L-56,-104 '
            'C-60,-140 -62,-170 -60,-200 L-66,-262 C-66,-286 -56,-294 -44,-298Z"/>'
            # man's arm reaching to woman (holding hands)
            '<path d="M-10,-262 C0,-240 6,-222 20,-212 L26,-206 L18,-198 C4,-208 -8,-226 -18,-248Z"/>'
            # woman (right) head with bun
            '<ellipse cx="30" cy="-306" rx="14.5" ry="17.5"/>'
            '<circle cx="44" cy="-316" r="10"/>'
            # woman: neck, blouse, lehenga flare, dupatta
            '<path d="M24,-290 L36,-290 L38,-280 C52,-276 58,-266 58,-252 L56,-214 C54,-200 52,-194 50,-186 '
            'C70,-140 86,-70 98,0 L-2,0 C8,-70 18,-140 26,-186 C22,-196 18,-210 18,-230 L14,-252 C14,-268 20,-278 24,-282Z"/>'
            '<path d="M44,-282 C62,-270 72,-240 74,-200 C80,-150 96,-100 110,-40 L100,-40 C86,-96 70,-150 62,-196 C58,-232 54,-260 44,-270Z"/>'
            # woman's arm to hand
            '<path d="M22,-258 C18,-236 22,-218 24,-208 L16,-202 C12,-214 10,-236 14,-258Z"/>'
            '</g>')


def pregnant_profile(x, y, s, col="#6E3B5C", saree=None, hair="#3A1E2C", gajra=True, skin=None, facing=1):
    """Expecting mother, side profile, standing, one hand under belly, one on top. (x,y)=feet centre.
    If saree colours given (tuple main, dark, border), draws a coloured illustration, else a silhouette."""
    sx = facing * s / 100
    if saree:
        main, dark, border = saree
        gs, a = lin([_shade(main, .25), main, dark], 0, 0, 1, 0)
        sk = skin or ("#C98A6A", "#A86B4E")
        gk, b = lin([sk[0], sk[1]], 0, 0, 1, 0)
        fill_body, fill_saree, fill_skin, fill_hair = "url(#%s)" % gk, "url(#%s)" % gs, "url(#%s)" % gk, hair
        dd = defs(a, b)
    else:
        dd = ""
        fill_body = fill_saree = fill_skin = fill_hair = col
        border = col
    out = [dd, '<g transform="translate(%s %s) scale(%s %s)">' % (f(x), f(y), f(sx), f(s / 100))]
    # back hair + bun
    out.append('<path d="M-22,-386 C-30,-410 -10,-428 12,-426 C32,-424 42,-410 40,-392 C30,-398 10,-400 -6,-394 C-12,-386 -18,-380 -22,-386Z" fill="%s"/>' % fill_hair)
    out.append('<circle cx="-30" cy="-392" r="17" fill="%s"/>' % fill_hair)
    if gajra:
        for i in range(11):
            a_ = math.radians(90 + i * 22)
            out.append('<circle cx="%s" cy="%s" r="3.6" fill="#FFFFFF" stroke="#E6DCC4" stroke-width=".6"/>' % (
                f(-30 + math.cos(a_) * 19), f(-392 + math.sin(a_) * 19)))
        out.append('<circle cx="-44" cy="-404" r="5" fill="#F07A92"/>')
    # face profile (facing right)
    out.append('<path d="M-12,-398 C0,-414 26,-416 36,-398 C40,-390 40,-384 44,-378 C48,-372 46,-370 42,-368 '
               'C44,-362 42,-358 40,-356 C42,-350 38,-344 32,-344 C28,-340 22,-338 18,-340 L16,-330 L-4,-330 '
               'C-8,-344 -16,-356 -18,-370 C-20,-382 -18,-392 -12,-398Z" fill="%s"/>' % fill_skin)
    if saree:
        out.append('<path d="M-12,-398 C0,-412 24,-414 34,-400 C24,-398 14,-394 8,-386 C0,-380 -6,-372 -10,-362 C-16,-372 -18,-388 -12,-398Z" fill="%s"/>' % fill_hair)
        out.append('<circle cx="30" cy="-382" r="2" fill="#2A1520"/>')  # eye hint
        out.append('<circle cx="16" cy="-362" r="3.5" fill="#F2C94C"/>')  # earring
        out.append('<circle cx="26" cy="-400" r="2.6" fill="#C0223B"/>')  # bindi hint on forehead line
    # neck + torso (blouse), back
    out.append('<path d="M-6,-334 L16,-334 L18,-318 C34,-312 44,-296 46,-276 C50,-260 58,-246 70,-228 '
               'C96,-196 106,-156 98,-124 C92,-100 74,-86 52,-80 L-36,-80 C-44,-130 -46,-190 -42,-240 '
               'C-40,-280 -32,-306 -10,-318Z" fill="%s"/>' % fill_body)
    # saree: pleated skirt down to feet, pallu over shoulder flowing back
    out.append('<path d="M-38,-150 C-30,-150 20,-146 60,-130 C84,-120 98,-110 98,-100 C96,-86 80,-78 60,-74 '
               'C66,-50 74,-24 82,0 L-60,0 C-58,-40 -50,-100 -38,-150Z" fill="%s"/>' % fill_saree)
    out.append('<path d="M-12,-322 C8,-310 30,-296 42,-270 C54,-246 76,-222 94,-190 C104,-170 104,-146 98,-128 '
               'C80,-140 60,-150 40,-156 C10,-166 -20,-170 -40,-168 C-44,-220 -40,-270 -30,-300 C-26,-312 -20,-320 -12,-322Z" fill="%s" opacity="%s"/>' % (
                   fill_saree, 1 if saree else 1))
    # pallu flowing behind the back
    out.append('<path d="M-12,-322 C-40,-300 -56,-240 -62,-180 C-68,-120 -76,-60 -92,-6 L-60,0 C-58,-60 -50,-130 -42,-200 C-38,-250 -32,-290 -12,-322Z" fill="%s"/>' % fill_saree)
    if saree:
        out.append('<path d="M-12,-322 C-40,-300 -56,-240 -62,-180 C-68,-120 -76,-60 -92,-6" stroke="%s" stroke-width="7" fill="none"/>' % border)
        out.append('<path d="M-12,-322 C8,-310 30,-296 42,-270 C54,-246 76,-222 94,-190 C104,-170 104,-146 98,-128" stroke="%s" stroke-width="6" fill="none"/>' % border)
        out.append('<path d="M-60,0 L82,0" stroke="%s" stroke-width="10"/>' % border)
        for px in (-30, 0, 30, 56):
            out.append('<path d="M%s,-70 C%s,-40 %s,-20 %s,0" stroke="%s" stroke-width="2" fill="none" opacity=".35"/>' % (px, px + 2, px + 6, px + 8, dark))
    # arms: one hand under belly, one resting on top of belly
    out.append('<path d="M-10,-300 C-24,-270 -26,-230 -12,-196 C0,-170 30,-146 62,-132 L70,-124 C74,-118 66,-110 58,-114 '
               'C26,-126 -6,-150 -24,-180 C-40,-214 -36,-262 -22,-300Z" fill="%s"/>' % fill_skin)
    out.append('<path d="M-2,-290 C8,-262 16,-236 36,-222 C52,-212 64,-206 76,-208 L82,-204 C84,-196 76,-194 70,-196 '
               'C54,-196 34,-204 20,-214 C2,-230 -8,-258 -14,-286Z" fill="%s"/>' % fill_skin)
    if saree:
        # bangles on wrists
        for bx, by in ((52, -126), (58, -129), (64, -205), (69, -206)):
            out.append('<ellipse cx="%s" cy="%s" rx="3" ry="8" fill="#C0223B" stroke="#F2C94C" stroke-width="1.5" transform="rotate(20 %s %s)"/>' % (bx, by, bx, by))
    out.append("</g>")
    return "".join(out)


def cloud(x, y, s, col="#FFFFFF", op=1, shadow="#E9DDF2"):
    return ('<g transform="translate(%s %s) scale(%s)" opacity="%s">' % (f(x), f(y), f(s / 100), op) +
            '<path d="M-100,20 C-120,20 -124,-8 -104,-14 C-108,-40 -76,-52 -58,-36 C-50,-66 -6,-72 8,-44 C22,-64 60,-58 60,-30 '
            'C84,-36 100,-12 86,6 C100,14 96,34 76,34 L-90,34 C-104,34 -110,24 -100,20Z" fill="%s"/>' % shadow +
            '<path d="M-100,14 C-120,14 -124,-14 -104,-20 C-108,-46 -76,-58 -58,-42 C-50,-72 -6,-78 8,-50 C22,-70 60,-64 60,-36 '
            'C84,-42 100,-18 86,0 C100,8 96,28 76,28 L-90,28 C-104,28 -110,18 -100,14Z" fill="%s"/>' % col +
            '</g>')


def bangle(cx, cy, rx, ry, col, band=8, gold_edge=True):
    g, a = lin([_shade(col, .45), col, _shade(col, -.35), col, _shade(col, .3)], 0, 0, 1, 0)
    out = [defs(a), '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="url(#%s)" stroke-width="%s"/>' % (
        f(cx), f(cy), f(rx), f(ry), g, f(band))]
    if gold_edge:
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="#F2CF74" stroke-width="%s" opacity=".9"/>' % (
            f(cx), f(cy - band * .45), f(rx), f(ry), f(band * .18)))
    out.append('<path d="M%s,%s A%s,%s 0 0 0 %s,%s" fill="none" stroke="#FFFFFF" stroke-width="%s" opacity=".55" stroke-linecap="round"/>' % (
        f(cx - rx * .8), f(cy + ry * .5), f(rx), f(ry), f(cx - rx * .1), f(cy + ry), f(band * .25)))
    return "".join(out)


def bangle_stack(cx, base_y, rx, colors, band=12, step=None, ry_k=.26):
    """vertical stack of bangles (like on a bangle stand). returns markup."""
    step = step or band * 1.05
    ry = rx * ry_k
    out = []
    for i, c in enumerate(colors):
        out.append(bangle(cx, base_y - i * step, rx, ry, c, band))
    return "".join(out)


def apple(x, y, r, col=("#E0303F", "#9B1422", "#FF8A8A")):
    g, a = rad([(0, col[2]), (.5, col[0]), (1, col[1])], .38, .35, .75)
    return (defs(a) + '<path d="M%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s Z" fill="url(#%s)"/>' % (
        f(x), f(y - r * .7), f(x + r * .9), f(y - r * 1.1), f(x + r * 1.2), f(y + r * .3), f(x + r * .5), f(y + r * .9),
        f(x + r * .2), f(y + r * 1.05), f(x - r * .2), f(y + r * 1.05), f(x - r * .5), f(y + r * .9),
        f(x - r * 1.2), f(y + r * .3), f(x - r * .9), f(y - r * 1.1), f(x), f(y - r * .7), g) +
        '<path d="M%s,%s q%s,%s %s,%s" stroke="#5A3A1E" stroke-width="%s" fill="none" stroke-linecap="round"/>' % (
            f(x), f(y - r * .65), f(r * .05), f(-r * .3), f(r * .18), f(-r * .45), f(r * .08)) +
        leaf(x + r * .15, y - r * .9, r * .6, -30, "#7DB34E", "#3F7A2A", vein=False) +
        '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff" opacity=".35" transform="rotate(-30 %s %s)"/>' % (
            f(x - r * .45), f(y - r * .2), f(r * .15), f(r * .3), f(x - r * .45), f(y - r * .2)))


def pomegranate(x, y, r):
    g, a = rad([(0, "#FF8A8A"), (.5, "#C8233B"), (1, "#7A0F22")], .38, .35, .75)
    return (defs(a) + '<circle cx="%s" cy="%s" r="%s" fill="url(#%s)"/>' % (f(x), f(y), f(r), g) +
            '<path d="M%s,%s l%s,%s l%s,%s l%s,%s l%s,%s l%s,%s l%s,%s Z" fill="#8A1426"/>' % (
                f(x - r * .25), f(y - r * .85), f(r * .06), f(-r * .3), f(r * .1), f(r * .15), f(r * .09), f(-r * .2),
                f(r * .09), f(r * .2), f(r * .1), f(-r * .15), f(r * .06), f(r * .3)) +
            '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff" opacity=".3"/>' % (f(x - r * .4), f(y - r * .3), f(r * .18), f(r * .28)))


def banana_bunch(x, y, s, rot=0):
    g, a = lin(["#FFF1A6", "#F5D33E", "#C99A12"], 0, 0, 0, 1)
    out = [defs(a), '<g transform="translate(%s %s) rotate(%s) scale(%s)">' % (f(x), f(y), rot, f(s / 100))]
    for i, (dx, rr) in enumerate([(-30, -20), (-10, -8), (10, 6), (30, 18)]):
        out.append('<path d="M0,0 C%s,-30 %s,-80 %s,-120 C%s,-110 %s,-70 %s,-4 Z" fill="url(#%s)" stroke="#B68912" stroke-width="1.5" transform="rotate(%s)"/>' % (
            dx - 20, dx - 30, dx - 8, dx + 4, dx + 8, 12, g, rr))
        out.append('<path d="M%s,-120 l-2,-8 l6,0 Z" fill="#4B3A12" transform="rotate(%s)"/>' % (dx - 8, rr))
    out.append('<rect x="-8" y="-6" width="18" height="16" rx="4" fill="#7C8B35"/></g>')
    return "".join(out)


def grapes(x, y, s):
    out = []
    g, a = rad([(0, "#D8F29A"), (.6, "#8DBF3A"), (1, "#557A1E")], .35, .35, .7)
    out.append(defs(a))
    rows = [5, 4, 4, 3, 2, 1]
    for j, n in enumerate(rows):
        for i in range(n):
            out.append('<circle cx="%s" cy="%s" r="%s" fill="url(#%s)" stroke="#4F6E1A" stroke-width=".6"/>' % (
                f(x + (i - (n - 1) / 2) * s * .2), f(y + j * s * .17), f(s * .11), g))
    out.append('<path d="M%s,%s q%s,%s %s,%s" stroke="#6B5A2B" stroke-width="3" fill="none"/>' % (f(x), f(y - s * .08), f(s * .05), f(-s * .15), f(s * .15), f(-s * .2)))
    return "".join(out)


def basket(x, y, w, h, col=("#C8904E", "#8C5A24", "#E8BC7C")):
    """wicker basket front. (x,y)=top centre of the rim."""
    g, a = lin([col[2], col[0], col[1]], 0, 0, 0, 1)
    cid = uid("bk")
    body = "M%s,%s L%s,%s Q%s,%s %s,%s L%s,%s Q%s,%s %s,%s Z" % (
        f(x - w / 2), f(y), f(x + w / 2), f(y), f(x + w * .46), f(y + h), f(x + w * .36), f(y + h),
        f(x - w * .36), f(y + h), f(x - w * .46), f(y + h), f(x - w / 2), f(y))
    out = [defs(a, '<clipPath id="%s"><path d="%s"/></clipPath>' % (cid, body))]
    out.append('<path d="%s" fill="url(#%s)" filter="url(#sh)"/>' % (body, g))
    weave = []
    rows = int(h / 16) + 1
    for r_ in range(rows):
        yy = y + r_ * 16 + 8
        for c_ in range(int(w / 24) + 2):
            xx = x - w / 2 + c_ * 24 + (12 if r_ % 2 else 0)
            weave.append('<ellipse cx="%s" cy="%s" rx="10" ry="6" fill="%s" opacity=".55"/>' % (f(xx), f(yy), col[2]))
            weave.append('<path d="M%s,%s q12,-4 24,0" stroke="%s" stroke-width="1.4" fill="none" opacity=".6"/>' % (f(xx - 12), f(yy + 6), col[1]))
    out.append('<g clip-path="url(#%s)">%s</g>' % (cid, "".join(weave)))
    # rim
    out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>' % (f(x - w / 2 - 6), f(y - 8), f(w + 12), f(18), f(9), col[1]))
    out.append('<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="4" stroke-dasharray="10 6"/>' % (f(x - w / 2), f(y + 1), f(x + w / 2), f(y + 1), col[2]))
    return "".join(out)


def onesie(x, y, s, col="#F9C8D4", trim="#FFFFFF", rot=0):
    g, a = lin([_shade(col, .3), col], 0, 0, 0, 1)
    return (defs(a) + '<g transform="translate(%s %s) rotate(%s) scale(%s)">' % (f(x), f(y), rot, f(s / 100)) +
            '<path d="M-24,0 C-18,8 18,8 24,0 L52,14 L64,40 L44,52 L36,40 L34,96 C34,110 20,116 10,110 L0,104 L-10,110 '
            'C-20,116 -34,110 -34,96 L-36,40 L-44,52 L-64,40 L-52,14 Z" fill="url(#%s)" stroke="%s" stroke-width="2"/>' % (g, _shade(col, -.2)) +
            '<path d="M-24,0 C-18,10 18,10 24,0" stroke="%s" stroke-width="4" fill="none"/>' % trim +
            '<circle cx="0" cy="36" r="3" fill="%s"/><circle cx="0" cy="54" r="3" fill="%s"/>' % (trim, trim) +
            '<path d="M-10,64 C-10,56 -2,56 0,62 C2,56 10,56 10,64 C10,72 0,78 0,78 C0,78 -10,72 -10,64Z" fill="%s" opacity=".8"/>' % trim +
            '</g>')


def jhabla(x, y, s, col="#BFE3D0", trim="#F2CF74", rot=0):
    """little Indian baby top (jhabla) with frilly edge"""
    g, a = lin([_shade(col, .3), col], 0, 0, 0, 1)
    frill = "".join('<circle cx="%s" cy="92" r="6" fill="%s"/>' % (i, trim) for i in range(-42, 46, 12))
    return (defs(a) + '<g transform="translate(%s %s) rotate(%s) scale(%s)">' % (f(x), f(y), rot, f(s / 100)) +
            '<path d="M-20,0 C-12,10 12,10 20,0 L56,18 L66,48 L46,56 L40,40 L46,90 L-46,90 L-40,40 L-46,56 L-66,48 L-56,18Z" fill="url(#%s)" stroke="%s" stroke-width="2"/>' % (g, _shade(col, -.2)) +
            frill + '<path d="M0,8 L0,60" stroke="%s" stroke-width="3" stroke-dasharray="3 5"/>' % trim +
            '<circle cx="-20" cy="50" r="4" fill="%s"/><circle cx="20" cy="50" r="4" fill="%s"/>' % (trim, trim) +
            '</g>')


def sock(x, y, s, col="#FFE3A3", rot=0):
    return ('<g transform="translate(%s %s) rotate(%s) scale(%s)">' % (f(x), f(y), rot, f(s / 100)) +
            '<path d="M-14,0 L14,0 L14,50 C30,54 44,62 44,74 C44,86 30,88 16,86 L-6,84 C-16,82 -16,70 -14,60Z" fill="%s" stroke="%s" stroke-width="2"/>' % (col, _shade(col, -.2)) +
            '<rect x="-14" y="0" width="28" height="12" fill="%s"/>' % _shade(col, -.12) +
            '</g>')


def peg(x, y, col="#D9A96A"):
    return '<rect x="%s" y="%s" width="7" height="20" rx="2" fill="%s" stroke="%s" stroke-width="1"/>' % (f(x - 3.5), f(y - 6), col, _shade(col, -.3))


# ================================================================== v2 additions
def linked_rings(x, y, r, metals=(GOLD, ROSEGOLD), stone=True, band=None, rot=(-10, 12), glow=True):
    """Two upright rings truly interlocked (A over B at the bottom crossing, B over A at the top).
    (x,y)=centre of the pair, r = ring radius (vertical)."""
    band = band or r * .15
    ax, bx = x - r * .5, x + r * .5
    A = upright_ring(ax, y, r, metals[0], rot[0], stone, 1.0, band)
    B = upright_ring(bx, y + r * .06, r * .95, metals[1], rot[1], False, 1.0, band * .95)
    cid = uid("lk")
    clip = defs('<clipPath id="%s"><rect x="%s" y="%s" width="%s" height="%s"/></clipPath>' % (
        cid, f(x - r * .45), f(y + r * .15), f(r * .9), f(r * 1.2)))
    out = ""
    if glow:
        out += glow_spot(x, y, r * 2.2, "#FFF4D6", .55)
    out += A + B + clip + '<g clip-path="url(#%s)">%s</g>' % (cid, upright_ring(ax, y, r, metals[0], rot[0], False, 1.0, band))
    return out


def mother(x, y, s, col="#6E3B5C", detail="#F6D9E6", gold="#F2CF74", flowers=True, facing=1, pallu_col=None):
    """Elegant expecting-mother silhouette facing right, hand resting on the belly; flower gajra,
    earring, bangles and pallu border drawn as light detail. (x,y)=feet centre, s=scale (100 -> ~410px tall)."""
    sx = facing * s / 100
    gid, g = lin([shade(col, .18), col, shade(col, -.2)], 0, 0, 1, 0)
    out = [defs(g), '<g transform="translate(%s %s) scale(%s %s)">' % (f(x), f(y), f(sx), f(s / 100))]
    body = ("M-6,-336 C-16,-350 -20,-372 -10,-390 C0,-406 24,-410 38,-396 C44,-388 44,-380 43,-374 "
            "C47,-368 50,-364 46,-360 C44,-358 44,-356 45,-352 C46,-348 42,-346 40,-344 C42,-340 40,-336 34,-335 "
            "C28,-333 22,-334 18,-330 L20,-316 C36,-310 46,-296 48,-280 C50,-266 46,-258 48,-250 "
            "C74,-236 100,-206 102,-172 C104,-146 90,-128 72,-122 C74,-80 80,-36 88,0 L-64,0 "
            "C-60,-40 -52,-90 -46,-140 C-42,-170 -46,-196 -44,-226 C-42,-262 -38,-294 -22,-314 C-14,-322 -8,-328 -6,-336Z")
    out.append('<path d="%s" fill="url(#%s)"/>' % (body, gid))
    # bun
    out.append('<circle cx="-24" cy="-368" r="19" fill="url(#%s)"/>' % gid)
    # pallu flowing back
    pc = pallu_col or shade(col, -.12)
    out.append('<path d="M-18,-318 C-46,-290 -60,-230 -66,-170 C-72,-110 -84,-50 -104,4 L-64,0 C-60,-60 -54,-120 -48,-180 C-44,-240 -38,-290 -18,-318Z" fill="%s"/>' % pc)
    # detail: pallu border
    out.append('<path d="M-18,-318 C-46,-290 -60,-230 -66,-170 C-72,-110 -84,-50 -104,4" stroke="%s" stroke-width="5" fill="none" opacity=".9"/>' % gold)
    out.append('<path d="M-12,-322 C10,-306 34,-290 46,-262" stroke="%s" stroke-width="4" fill="none" opacity=".85"/>' % gold)
    # saree pleats + hem
    for px in (-30, -6, 18, 42, 62):
        out.append('<path d="M%s,-110 C%s,-70 %s,-30 %s,-2" stroke="%s" stroke-width="2" fill="none" opacity=".35"/>' % (
            px, px + 2, px + 5, px + 8, detail))
    out.append('<path d="M-64,-4 L88,-4" stroke="%s" stroke-width="8" opacity=".9"/>' % gold)
    # arm + hand on belly (detail outline)
    out.append('<path d="M-8,-306 C-22,-276 -24,-236 -10,-206 C4,-182 34,-170 62,-176 C76,-178 86,-186 90,-194" '
               'stroke="%s" stroke-width="3" fill="none" opacity=".8" stroke-linecap="round"/>' % detail)
    out.append('<path d="M-2,-300 C-10,-270 -8,-236 4,-216 C18,-198 40,-192 60,-194 C72,-196 80,-200 86,-206" '
               'stroke="%s" stroke-width="2" fill="none" opacity=".55" stroke-linecap="round"/>' % detail)
    # fingers
    for k in range(4):
        out.append('<path d="M%s,%s q10,-4 18,-12" stroke="%s" stroke-width="2.4" fill="none" opacity=".75" stroke-linecap="round"/>' % (
            70 + k * 4, -182 - k * 5, detail))
    # bangles at wrist
    for k in range(4):
        out.append('<ellipse cx="%s" cy="%s" rx="3.2" ry="10" fill="none" stroke="%s" stroke-width="2.6" transform="rotate(-25 %s %s)"/>' % (
            46 + k * 6, -180 - k * 1.5, gold if k % 2 == 0 else "#E8577A", 46 + k * 6, -180 - k * 1.5))
    # other hand under belly
    out.append('<path d="M40,-126 C58,-122 76,-126 88,-134" stroke="%s" stroke-width="3" fill="none" opacity=".7" stroke-linecap="round"/>' % detail)
    # earring + bindi + nose ring
    out.append('<circle cx="10" cy="-352" r="4.5" fill="%s"/><circle cx="10" cy="-344" r="2.6" fill="%s"/>' % (gold, gold))
    out.append('<circle cx="41" cy="-362" r="3" fill="none" stroke="%s" stroke-width="1.6"/>' % gold)
    if flowers:
        for i in range(12):
            a_ = math.radians(70 + i * 20)
            out.append('<circle cx="%s" cy="%s" r="4.4" fill="#FFFFFF" stroke="#E6DCC4" stroke-width=".7"/>' % (
                f(-24 + math.cos(a_) * 21), f(-368 + math.sin(a_) * 21)))
        out.append('<circle cx="-40" cy="-384" r="6" fill="#F07A92"/><circle cx="-44" cy="-376" r="4.5" fill="#F6B2C2"/>')
        # flower strand down the back
        for i in range(8):
            out.append('<circle cx="%s" cy="%s" r="3.6" fill="#FFFFFF" stroke="#E6DCC4" stroke-width=".6"/>' % (f(-30 - i * 1.2), f(-346 + i * 9)))
    out.append("</g>")
    return "".join(out)


def light_rays(cx, cy, n, length, color="#FFFFFF", op=.18, spread=180, start=-180, width=.05):
    out = []
    for i in range(n):
        a = math.radians(start + i * spread / max(1, n - 1))
        p = [(cx, cy), (cx + math.cos(a - width) * length, cy + math.sin(a - width) * length),
             (cx + math.cos(a + width) * length, cy + math.sin(a + width) * length)]
        out.append('<path d="%sZ" fill="%s" opacity="%s"/>' % (pts_d(p), color, op))
    return '<g filter="url(#bl6)">%s</g>' % "".join(out)


def tassel(x, y, L, col="#C8233B", cap=GOLD):
    g, a = lin(cap, 0, 0, 1, 0)
    out = [defs(a), '<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="2"/>' % (f(x), f(y), f(x), f(y + L * .35), shade(col, -.3))]
    out.append('<circle cx="%s" cy="%s" r="%s" fill="url(#%s)"/>' % (f(x), f(y + L * .38), f(L * .09), g))
    out.append('<path d="M%s,%s L%s,%s L%s,%s L%s,%s Z" fill="url(#%s)"/>' % (
        f(x - L * .07), f(y + L * .44), f(x + L * .07), f(y + L * .44), f(x + L * .1), f(y + L * .55), f(x - L * .1), f(y + L * .55), g))
    for k in range(9):
        dx = (k - 4) * L * .025
        out.append('<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
            f(x + dx * .8), f(y + L * .55), f(x + dx * 1.4), f(y + L), col if k % 2 else shade(col, -.2), f(L * .03)))
    return "".join(out)


def chunri_swag(x0, x1, y, sag, depth, col=("#C8233B", "#8E1027"), border=GOLD, n=3, dots="#F6D36B", tassels=True):
    """Draped cloth swags hanging from the top, gota border on the lower edge."""
    g, a = lin([col[0], col[1]], 0, 0, 0, 1)
    gb, b = lin(border, 0, 0, 1, 0)
    out = [defs(a, b)]
    wseg = (x1 - x0) / n
    for i in range(n):
        sx0, sx1 = x0 + i * wseg, x0 + (i + 1) * wseg
        mx = (sx0 + sx1) / 2
        top = "M%s,%s Q%s,%s %s,%s" % (f(sx0), f(y), f(mx), f(y + sag), f(sx1), f(y))
        bot = "Q%s,%s %s,%s" % (f(mx), f(y + sag + depth * 2), f(sx0), f(y))
        out.append('<path d="%s L%s,%s %s Z" fill="url(#%s)" filter="url(#sh)"/>' % (top, f(sx1), f(y), bot, g))
        # folds
        for k in range(1, 4):
            out.append('<path d="M%s,%s Q%s,%s %s,%s" stroke="#000" stroke-opacity=".12" stroke-width="3" fill="none"/>' % (
                f(sx0 + 8), f(y), f(mx), f(y + sag + depth * 2 * k / 4), f(sx1 - 8), f(y)))
        # gota border along the lower edge (quadratic midpoint approx)
        pts = qbez((sx0, y), (mx, y + sag + depth * 2), (sx1, y), 40)
        out.append('<path d="%s" stroke="url(#%s)" stroke-width="12" fill="none"/>' % (pts_d(pts), gb))
        out.append(strand(pts[3:-3], lambda px, py, an: '<circle cx="%s" cy="%s" r="2.6" fill="%s"/>' % (f(px), f(py), dots), step=14))
        # bandhej-free dot print on cloth
        R = random.Random(i + 7)
        for _ in range(30):
            t = R.uniform(.1, .9)
            yy = y + (sag + depth * 2 * R.uniform(.1, .45)) * 4 * t * (1 - t)
            out.append('<circle cx="%s" cy="%s" r="2" fill="%s" opacity=".55"/>' % (f(sx0 + t * wseg), f(yy), dots))
        if tassels:
            out.append(tassel(sx0, y - 4, 90, col[0]))
    if tassels:
        out.append(tassel(x1, y - 4, 90, col[0]))
    return "".join(out)


def ribbon_bow(x, y, s, col=("#F29BB0", "#C8577A")):
    g, a = lin([shade(col[0], .3), col[0], col[1]], 0, 0, 0, 1)
    return (defs(a) + '<g transform="translate(%s %s) scale(%s)">' % (f(x), f(y), f(s / 100)) +
            '<path d="M0,0 C-20,20 -30,70 -46,96 L-30,90 L-22,104 C-12,74 -4,40 0,0Z" fill="url(#%s)"/>' % g +
            '<path d="M0,0 C18,22 26,70 42,98 L26,92 L18,106 C10,76 2,40 0,0Z" fill="url(#%s)"/>' % g +
            '<path d="M0,0 C-30,-40 -84,-44 -86,-12 C-88,14 -40,14 0,0Z" fill="url(#%s)"/>' % g +
            '<path d="M0,0 C30,-40 84,-44 86,-12 C88,14 40,14 0,0Z" fill="url(#%s)"/>' % g +
            '<path d="M-6,-4 C-30,-26 -66,-30 -72,-12" stroke="#fff" stroke-opacity=".4" stroke-width="3" fill="none"/>' +
            '<ellipse cx="0" cy="0" rx="12" ry="14" fill="%s"/>' % col[1] + '</g>')


def gift_box(x, y, w, h, col=("#F4A8B8", "#D66F8A"), ribbon=GOLD, lid=True, pattern=None):
    """(x,y)= bottom centre"""
    g, a = lin([shade(col[0], .15), col[0], col[1]], 0, 0, 1, 0)
    gr, b = lin(ribbon, 0, 0, 1, 0)
    out = [defs(a, b)]
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#000" opacity=".22" filter="url(#bl6)"/>' % (f(x), f(y + 4), f(w * .55), f(w * .06)))
    out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)"/>' % (f(x - w / 2), f(y - h), f(w), f(h), g))
    if pattern:
        R = random.Random(int(x + y))
        for i in range(int(w * h / 900)):
            out.append('<circle cx="%s" cy="%s" r="2.2" fill="%s" opacity=".6"/>' % (f(x - w / 2 + R.uniform(4, w - 4)), f(y - h + R.uniform(4, h - 4)), pattern))
    out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)"/>' % (f(x - w * .07), f(y - h), f(w * .14), f(h), gr))
    if lid:
        out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="3" fill="url(#%s)" filter="url(#shs)"/>' % (f(x - w * .54), f(y - h - h * .16), f(w * 1.08), f(h * .2), g))
        out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)"/>' % (f(x - w * .07), f(y - h - h * .16), f(w * .14), f(h * .2), gr))
    out.append('<path d="M%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s Z" fill="url(#%s)"/>' % (
        f(x), f(y - h - h * .16), f(x - w * .3), f(y - h * 1.6), f(x - w * .42), f(y - h * 1.1), f(x), f(y - h - h * .16),
        f(x + w * .42), f(y - h * 1.1), f(x + w * .3), f(y - h * 1.6), f(x), f(y - h - h * .16), gr))
    return "".join(out)


def heart_points(cx, top, w, h, n=90):
    """points along a heart outline (matches the engine heart shape family)."""
    x, y = cx - w / 2, top
    segs = [((cx, y + h), (x - w * .2, y + h * .55), (x, y - h * .05), (cx, y + h * .22)),
            ((cx, y + h * .22), (x + w, y - h * .05), (x + w * 1.2, y + h * .55), (cx, y + h))]
    pts = []
    for p0, p1, p2, p3 in segs:
        for i in range(n // 2):
            t = i / (n // 2)
            mt = 1 - t
            pts.append((mt ** 3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t ** 3 * p3[0],
                        mt ** 3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t ** 3 * p3[1]))
    pts.append(pts[0])
    return pts


def ellipse_points(cx, cy, rx, ry, n=80, a0=0, a1=360):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def floral_along(points, seed, flowers, every=3, leaves=("#7FA07A", "#4E7A4A"), leaf_len=44, scale=1.0):
    """Garland: leaves then flowers along a path. flowers = list of callables(x,y,rot) -> svg"""
    R = random.Random(seed)
    L, F = [], []
    for i, (px, py) in enumerate(points):
        if i % 2 == 0:
            for sgn in (-1, 1):
                L.append(leaf(px, py, leaf_len * scale * R.uniform(.75, 1.1), R.uniform(0, 360), leaves[0], leaves[1]))
        if i % every == 0:
            fn = R.choice(flowers)
            F.append(fn(px + R.uniform(-6, 6), py + R.uniform(-6, 6), R.uniform(0, 360)))
    return "".join(L) + "".join(F)


def bouquet(x, y, s, flowers_pal=None, wrap=("#F7E6DA", "#E3C4AE"), bow=("#C9A0DC", "#8E5CA8")):
    """Hand-tied bouquet in a paper cone. (x,y)=bottom tip of the cone, s=scale (100 -> ~360px tall)."""
    k = s / 100
    gw, a = lin([shade(wrap[0], .3), wrap[0], wrap[1]], 0, 0, 1, 0)
    out = [defs(a)]
    # back wrap flare
    out.append('<path d="M%s,%s L%s,%s C%s,%s %s,%s %s,%s Z" fill="%s"/>' % (
        f(x), f(y), f(x - 150 * k), f(y - 250 * k), f(x - 60 * k), f(y - 300 * k), f(x + 60 * k), f(y - 300 * k), f(x + 150 * k), f(y - 250 * k), wrap[1]))
    # greenery
    R = random.Random(int(x))
    for i in range(12):
        ang = -90 + R.uniform(-70, 70)
        out.append(leaf(x + R.uniform(-60, 60) * k, y - 240 * k, R.uniform(60, 90) * k, ang, "#8DB38A", "#4E7A4A"))
    out.append(eucalyptus(x - 40 * k, y - 250 * k, 150 * k, -140, n=7))
    out.append(eucalyptus(x + 40 * k, y - 250 * k, 150 * k, -40, n=7))
    pal = flowers_pal or [("#B8264A", "#E0506E", "#F8A5B5"), ("#E88AA0", "#F6BFCB", "#FFE7EC")]
    out.append(gypso(int(x) + 3, x, y - 330 * k, 150 * k, 34, "#FFFFFF", (2.5 * k, 5 * k)))
    spots = [(-70, -300, 44), (0, -330, 52), (70, -300, 44), (-35, -270, 40), (38, -268, 40), (-100, -250, 30), (100, -250, 30), (0, -390, 34),
             (-60, -365, 30), (62, -362, 30)]
    for i, (dx, dy, r) in enumerate(spots):
        p = pal[i % len(pal)]
        if i % 3 == 1:
            out.append(peony(x + dx * k, y + dy * k, r * k, p))
        else:
            out.append(rose(x + dx * k, y + dy * k, r * k, p, rot=i * 37))
    # front wrap cone
    out.append('<path d="M%s,%s L%s,%s C%s,%s %s,%s %s,%s Z" fill="url(#%s)" filter="url(#sh)"/>' % (
        f(x), f(y), f(x - 120 * k), f(y - 210 * k), f(x - 50 * k), f(y - 230 * k), f(x + 50 * k), f(y - 230 * k), f(x + 120 * k), f(y - 210 * k), gw))
    out.append('<path d="M%s,%s L%s,%s" stroke="#fff" stroke-opacity=".5" stroke-width="%s"/>' % (f(x - 4 * k), f(y - 10 * k), f(x - 70 * k), f(y - 205 * k), f(3 * k)))
    out.append(ribbon_bow(x, y - 110 * k, 70 * k, bow))
    return "".join(out)


def jasmine_string(points, step=12, col="#FFFFFF", pink_every=0):
    """veni-style flower string: jasmine buds with occasional pink bud"""
    idx = [0]

    def it(x, y, a):
        idx[0] += 1
        c = "#F7A8BC" if pink_every and idx[0] % pink_every == 0 else col
        return ('<circle cx="%s" cy="%s" r="6.4" fill="%s" stroke="#D9CFB8" stroke-width=".8"/>'
                '<circle cx="%s" cy="%s" r="2" fill="#fff" opacity=".9"/>') % (f(x), f(y), c, f(x - 2), f(y - 2))
    return strand(points, it, step=step)


def jhula(x, top, w, rope_len, seat_col=("#F4C9D6", "#D9899F"), flower_cols=("#FFFFFF", "#F7A8BC", "#F9D776")):
    """Flower swing (jhula) seen from the front. ropes wrapped with flower strings, cushioned seat."""
    out = []
    xl, xr = x - w / 2, x + w / 2
    yb = top + rope_len
    # ropes
    for xx in (xl, xr):
        out.append('<path d="M%s,%s L%s,%s" stroke="#B0885A" stroke-width="6"/>' % (f(xx), f(top), f(xx), f(yb)))
        R = random.Random(int(xx))
        for i in range(int(rope_len / 15)):
            yy = top + 8 + i * 15
            c = flower_cols[i % len(flower_cols)]
            out.append('<circle cx="%s" cy="%s" r="9" fill="%s" stroke="#D8C8B0" stroke-width=".8"/>' % (f(xx + (4 if i % 2 else -4)), f(yy), c))
            if i % 3 == 0:
                out.append(leaf(xx, yy, 22, 180 if i % 2 else 0, "#8DB38A", "#4E7A4A", vein=False))
    # seat plank + cushion
    g, a = lin(["#C98B4E", "#8C5A24"], 0, 0, 0, 1)
    gc, b = lin([shade(seat_col[0], .3), seat_col[0], seat_col[1]], 0, 0, 0, 1)
    out.append(defs(a, b))
    out.append('<rect x="%s" y="%s" width="%s" height="26" rx="8" fill="url(#%s)" filter="url(#sh)"/>' % (f(xl - 30), f(yb), f(w + 60), g))
    out.append('<path d="M%s,%s C%s,%s %s,%s %s,%s L%s,%s C%s,%s %s,%s %s,%s Z" fill="url(#%s)"/>' % (
        f(xl - 20), f(yb + 2), f(xl), f(yb - 44), f(xr), f(yb - 44), f(xr + 20), f(yb + 2),
        f(xr + 10), f(yb + 4), f(x + 40), f(yb + 10), f(x - 40), f(yb + 10), f(xl - 10), f(yb + 4), gc))
    # hanging garland under the seat
    pts = catenary(xl - 20, yb + 22, xr + 20, yb + 22, 50, 40)
    out.append(jasmine_string(pts, 13, pink_every=4))
    for px in range(int(xl), int(xr) + 1, int(w / 6)):
        out.append(jasmine_string([(px, yb + 26), (px, yb + 26 + 70)], 13, pink_every=3))
    return "".join(out)


def flower_necklace(cx, top, w, drop, seed=1, main="#FFFFFF", accent="#F07A92", pendant=True):
    """floral jewellery (phoolon ka haar/gehna): layered jasmine strands with rose pendants."""
    out = []
    for k, (dd, st) in enumerate([(drop, 13), (drop * .72, 13), (drop * .45, 12)]):
        pts = catenary(cx - w / 2 + k * w * .08, top, cx + w / 2 - k * w * .08, top, dd, 60)
        out.append(jasmine_string(pts, st, main, pink_every=5 + k))
    if pendant:
        py = top + drop + 26
        out.append(rose(cx, py, 26, ("#B8264A", "#E0506E", "#F8A5B5")))
        for dx in (-1, 1):
            out.append(rose(cx + dx * 60, top + drop * .92 + 14, 16, ("#D05A7A", "#F08AA2", "#FFD1DC")))
        out.append(jasmine_string([(cx, py + 26), (cx, py + 110)], 12))
        out.append(tassel(cx, py + 110, 60, accent))
    return "".join(out)


def marble(pid, base="#FFFFFF", vein="#C9B8A6", seed=5, op=.35):
    return ('<filter id="%s" x="0" y="0" width="100%%" height="100%%"><feTurbulence type="fractalNoise" baseFrequency=".006 .012" numOctaves="4" seed="%d" result="n"/>'
            '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -9 5.2" result="m"/>'
            '<feFlood flood-color="%s" flood-opacity="%s"/><feComposite in2="m" operator="in"/></filter>') % (pid, seed, vein, op)


def jharokha(x, y, w, h, gold_stops=GOLD, fill=None, cusps=7):
    """Carved multifoil (cusped) arch frame: (x,y,w,h) bounding box of the opening; returns frame drawn around it."""
    g, a = lin(gold_stops, 0, 0, 1, 1)
    out = [defs(a)]
    cx = x + w / 2
    # outer pillars
    pw = 34
    for px in (x - pw - 14, x + w + 14):
        out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)" filter="url(#sh)"/>' % (f(px), f(y + h * .3), pw, f(h * .7 + 30), g))
        for k in range(int(h * .7 / 26)):
            out.append('<rect x="%s" y="%s" width="%s" height="8" rx="4" fill="#fff" opacity=".22"/>' % (f(px + 8), f(y + h * .32 + k * 26), pw - 16))
        # capital
        out.append('<path d="M%s,%s L%s,%s L%s,%s L%s,%s Z" fill="url(#%s)"/>' % (
            f(px - 10), f(y + h * .3), f(px + pw + 10), f(y + h * .3), f(px + pw), f(y + h * .3 - 22), f(px), f(y + h * .3 - 22), g))
        # base
        out.append('<rect x="%s" y="%s" width="%s" height="22" fill="url(#%s)"/>' % (f(px - 10), f(y + h + 16), pw + 20, g))
    # cusped arch outline following the arch shape grown outward
    d_out = shape_grow("arch", x, y, w, h, 34)
    d_in = shape_grow("arch", x, y, w, h, 12)
    out.append('<path d="%s %s" fill="url(#%s)" fill-rule="evenodd" filter="url(#sh)"/>' % (d_out, d_in, g))
    # cusps (small semicircle scallops) along the inner arch
    top_pts = []
    sh = y + h * .34
    for i in range(cusps * 6 + 1):
        t = i / (cusps * 6)
        ang = math.pi + t * math.pi
        top_pts.append((cx + math.cos(ang) * (w / 2 + 23), sh + math.sin(ang) * (sh - y + 23) * 1.0))
    for i in range(0, len(top_pts), 3):
        px, py = top_pts[i]
        out.append('<circle cx="%s" cy="%s" r="7" fill="url(#%s)" stroke="#8A5A12" stroke-width="1"/>' % (f(px), f(py), g))
    # finial on top
    out.append('<path d="M%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s Z" fill="url(#%s)"/>' % (
        f(cx), f(y - 110), f(cx - 26), f(y - 70), f(cx - 40), f(y - 40), f(cx), f(y - 30),
        f(cx + 40), f(y - 40), f(cx + 26), f(y - 70), f(cx), f(y - 110), g))
    out.append('<circle cx="%s" cy="%s" r="9" fill="url(#%s)"/>' % (f(cx), f(y - 118), g))
    return "".join(out)


# ================================================================== composition helpers
import json as _json, os as _os


def spec(cat, n, zone, title, text, accent, tone="light", tfont="deco", align="center", photo=None, slot=None):
    d = {"id": "E-%s-%d" % (cat, n), "tpl": True, "zone": [int(v) for v in zone],
         "colors": {"title": title, "text": text, "accent": accent}, "tone": tone, "title": tfont, "align": align}
    if photo:
        d["photo"] = photo
        d["slot"] = True if slot is None else slot
    return d


def write_specs(cat, specs):
    p = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "out", cat + ".json")
    _os.makedirs(_os.path.dirname(p), exist_ok=True)
    _json.dump(specs, open(p, "w"), ensure_ascii=False, indent=1)


def fancy_panel(x, y, w, h, fill="#FFF9EF", border=GOLD, r=26, bw=5, inner=True, corners=True, corner_size=90, shadow="shb",
                grain_=True, op=1):
    g, a = lin(border, 0, 0, 1, 1)
    out = [defs(a), panel(x, y, w, h, r, fill, shadow=shadow, grain_=grain_, op=op)]
    out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="url(#%s)" stroke-width="%s"/>' % (
        f(x), f(y), f(w), f(h), f(r), g, bw))
    if inner:
        out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="url(#%s)" stroke-width="1.6" opacity=".8"/>' % (
            f(x + 14), f(y + 14), f(w - 28), f(h - 28), f(max(4, r - 12)), g))
    if corners:
        c = "url(#%s)" % g
        s = corner_size
        out.append(corner_filigree(x + 20, y + 20, s, 1, 1, c))
        out.append(corner_filigree(x + w - 20, y + 20, s, -1, 1, c))
        out.append(corner_filigree(x + 20, y + h - 20, s, 1, -1, c))
        out.append(corner_filigree(x + w - 20, y + h - 20, s, -1, -1, c))
    return "".join(out)


def pat_rect(pat, pid, x=0, y=0, w=W, h=H):
    return defs(pat) + '<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)"/>' % (f(x), f(y), f(w), f(h), pid)


def rose_petal(x, y, s, rot, col=("#C2264B", "#8E1027")):
    g, a = lin([shade(col[0], .25), col[0], col[1]], 0, 0, 1, 1)
    return defs(a) + '<path d="M0,0 C%s,%s %s,%s 0,%s C%s,%s %s,%s 0,0Z" fill="url(#%s)" transform="translate(%s %s) rotate(%s)" opacity=".95"/>' % (
        f(s * .7), f(-s * .2), f(s * .6), f(-s * 1.1), f(-s * .9), f(-s * .6), f(-s * 1.1), f(-s * .7), f(-s * .2), g, f(x), f(y), f(rot))


def petals(seed, n, box, s=(14, 26), col=("#C2264B", "#8E1027"), avoid=None):
    R = random.Random(seed)
    x0, y0, x1, y1 = box
    out = []
    k = 0
    while len(out) < n and k < n * 20:
        k += 1
        px, py = R.uniform(x0, x1), R.uniform(y0, y1)
        if avoid and any(a[0] < px < a[2] and a[1] < py < a[3] for a in avoid):
            continue
        out.append(rose_petal(px, py, R.uniform(*s), R.uniform(0, 360), col))
    return "".join(out)
