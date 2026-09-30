"""lib_c: shared SVG drawing helpers for inv-wedding / wedding / anniversary card art.

Every card is authored as one 1080x1350 SVG. A Doc collects <defs> (gradients,
filters, patterns, reusable symbols) and wraps the body.
"""
import math, random, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
W, H = 1080, 1350


def n(v):
    s = "%.1f" % v
    return s[:-2] if s.endswith(".0") else s


def P(*pts):
    """points -> 'x,y x,y'"""
    return " ".join("%s,%s" % (n(a), n(b)) for a, b in pts)


def stops_s(stops):
    out = []
    for s in stops:
        off, col = s[0], s[1]
        op = s[2] if len(s) > 2 else 1
        out.append('<stop offset="%s" stop-color="%s"%s/>' % (n(off * 100) + "%", col,
                                                             "" if op == 1 else ' stop-opacity="%s"' % op))
    return "".join(out)


GOLD = [(0, "#7A4A0E"), (0.22, "#C8922E"), (0.42, "#F7DC8C"), (0.52, "#FFF3C4"), (0.66, "#E2AE45"), (0.85, "#A56C1A"), (1, "#6E420C")]
GOLD_SOFT = [(0, "#A8741E"), (0.35, "#E9C46A"), (0.5, "#FFF0B5"), (0.7, "#D9A441"), (1, "#8F5E17")]
ROSEGOLD = [(0, "#8E4B45"), (0.3, "#D39A8C"), (0.5, "#F7D9CF"), (0.7, "#C98476"), (1, "#7E3F3A")]
SILVER = [(0, "#6F7580"), (0.35, "#C9CED6"), (0.5, "#FFFFFF"), (0.7, "#AEB4BE"), (1, "#5E646E")]


class Doc:
    def __init__(self, seed=1):
        self.defs = []
        self.k = 0
        self.cache = {}
        self.rnd = random.Random(seed)

    def uid(self, p="i"):
        self.k += 1
        return "%s%d" % (p, self.k)

    # ---------- paint servers ----------
    def lg(self, stops, x1=0, y1=0, x2=0, y2=1, user=False, key=None):
        if key and key in self.cache:
            return self.cache[key]
        i = self.uid("g")
        u = ' gradientUnits="userSpaceOnUse"' if user else ""
        self.defs.append('<linearGradient id="%s" x1="%s" y1="%s" x2="%s" y2="%s"%s>%s</linearGradient>'
                         % (i, n(x1), n(y1), n(x2), n(y2), u, stops_s(stops)))
        r = "url(#%s)" % i
        if key:
            self.cache[key] = r
        return r

    def rg(self, stops, cx=0.5, cy=0.5, r=0.5, fx=None, fy=None, user=False, key=None):
        if key and key in self.cache:
            return self.cache[key]
        i = self.uid("r")
        u = ' gradientUnits="userSpaceOnUse"' if user else ""
        f = ""
        if fx is not None:
            f = ' fx="%s" fy="%s"' % (n(fx), n(fy))
        self.defs.append('<radialGradient id="%s" cx="%s" cy="%s" r="%s"%s%s>%s</radialGradient>'
                         % (i, n(cx), n(cy), n(r), f, u, stops_s(stops)))
        r_ = "url(#%s)" % i
        if key:
            self.cache[key] = r_
        return r_

    def gold(self, vertical=False, stops=None):
        st = stops or GOLD
        key = "gold%s%s" % (vertical, id(st))
        if vertical:
            return self.lg(st, 0, 0, 0, 1, key=key)
        return self.lg(st, 0, 0, 1, 1, key=key)

    # ---------- filters ----------
    def filt(self, key, body, pad=40):
        if key in self.cache:
            return self.cache[key]
        i = self.uid("f")
        self.defs.append('<filter id="%s" x="-%d%%" y="-%d%%" width="%d%%" height="%d%%" color-interpolation-filters="sRGB">%s</filter>'
                         % (i, pad, pad, 100 + 2 * pad, 100 + 2 * pad, body))
        self.cache[key] = "url(#%s)" % i
        return self.cache[key]

    def shadow(self, dx=0, dy=8, blur=12, color="#000", op=0.35):
        return self.filt("sh%s_%s_%s_%s_%s" % (dx, dy, blur, color, op),
                         '<feDropShadow dx="%s" dy="%s" stdDeviation="%s" flood-color="%s" flood-opacity="%s"/>' % (dx, dy, blur, color, op))

    def blur(self, sd):
        return self.filt("bl%s" % sd, '<feGaussianBlur stdDeviation="%s"/>' % sd, pad=60)

    def glow(self, sd=8, color="#FFD27A", op=0.9):
        return self.filt("gl%s%s%s" % (sd, color, op),
                         '<feGaussianBlur in="SourceAlpha" stdDeviation="%s" result="b"/><feFlood flood-color="%s" flood-opacity="%s"/>'
                         '<feComposite in2="b" operator="in" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>' % (sd, color, op), pad=80)

    def grain(self, freq=0.85, op=0.10, color="#3A2A1A"):
        """fine paper grain; use on a rect covering the area"""
        c = color.lstrip("#")
        r, g, b = [int(c[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        return self.filt("gr%s%s%s" % (freq, op, color),
                         '<feTurbulence type="fractalNoise" baseFrequency="%s" numOctaves="3" seed="7" stitchTiles="stitch"/>'
                         '<feColorMatrix type="matrix" values="0 0 0 0 %.3f  0 0 0 0 %.3f  0 0 0 0 %.3f  %s 0 0 0 %s"/>'
                         % (freq, r, g, b, n(op * 5), n(-op * 2.2)), pad=0)

    def silk(self, op=0.12, color="#FFFFFF", fx=0.004, fy=0.09, seed=3):
        c = color.lstrip("#")
        r, g, b = [int(c[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        return self.filt("sk%s%s%s%s" % (op, color, fx, fy),
                         '<feTurbulence type="fractalNoise" baseFrequency="%s %s" numOctaves="2" seed="%d"/>'
                         '<feColorMatrix type="matrix" values="0 0 0 0 %.3f  0 0 0 0 %.3f  0 0 0 0 %.3f  %s 0 0 0 %s"/>'
                         % (fx, fy, seed, r, g, b, n(op * 4), n(-op * 1.6)), pad=0)

    def watercolor(self, seed=2, scale=40):
        return self.filt("wc%s%s" % (seed, scale),
                         '<feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="3" seed="%d" result="t"/>'
                         '<feDisplacementMap in="SourceGraphic" in2="t" scale="%d" xChannelSelector="R" yChannelSelector="G" result="d"/>'
                         '<feGaussianBlur in="d" stdDeviation="3"/>' % (seed, scale), pad=20)

    # ---------- reuse ----------
    def sym(self, key, content):
        if ("sym", key) not in self.cache:
            i = self.uid("s")
            self.defs.append('<g id="%s">%s</g>' % (i, content))
            self.cache[("sym", key)] = i
        return self.cache[("sym", key)]

    def use(self, sid, x, y, s=1, rot=0, extra=""):
        t = "translate(%s %s)" % (n(x), n(y))
        if rot:
            t += " rotate(%s)" % n(rot)
        if s != 1:
            if isinstance(s, tuple):
                t += " scale(%s %s)" % (n(s[0]), n(s[1]))
            else:
                t += " scale(%s)" % n(s)
        return '<use href="#%s" transform="%s"%s/>' % (sid, t, extra)

    def pattern(self, w, h, content, transform="", key=None):
        if key and key in self.cache:
            return self.cache[key]
        i = self.uid("p")
        tr = ' patternTransform="%s"' % transform if transform else ""
        self.defs.append('<pattern id="%s" width="%s" height="%s" patternUnits="userSpaceOnUse"%s>%s</pattern>' % (i, n(w), n(h), tr, content))
        r = "url(#%s)" % i
        if key:
            self.cache[key] = r
        return r

    def clip(self, content):
        i = self.uid("c")
        self.defs.append('<clipPath id="%s">%s</clipPath>' % (i, content))
        return "url(#%s)" % i

    def mask(self, content):
        i = self.uid("m")
        self.defs.append('<mask id="%s" maskUnits="userSpaceOnUse" x="0" y="0" width="%d" height="%d">%s</mask>' % (i, W, H, content))
        return "url(#%s)" % i

    def svg(self, body):
        return ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%d" height="%d" viewBox="0 0 %d %d">'
                '<defs>%s</defs>%s</svg>' % (W, H, W, H, "".join(self.defs), body))


# ---------------------------------------------------------------- geometry
def g(content, x=0, y=0, s=1, rot=0, extra="", flip=False):
    t = []
    if x or y:
        t.append("translate(%s %s)" % (n(x), n(y)))
    if rot:
        t.append("rotate(%s)" % n(rot))
    if flip:
        t.append("scale(%s %s)" % (n(-s), n(s)))
    elif s != 1:
        t.append("scale(%s)" % n(s))
    tr = ' transform="%s"' % " ".join(t) if t else ""
    return "<g%s%s>%s</g>" % (tr, extra, content)


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def qbez(p0, p1, p2, t):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0], u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


def sample(fn, spacing, steps=400):
    """evenly spaced points (and tangent angle) along parametric fn(t) t in [0,1]"""
    pts = [fn(i / steps) for i in range(steps + 1)]
    out = [(pts[0], 0)]
    acc = 0
    for i in range(1, len(pts)):
        d = math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
        acc += d
        if acc >= spacing:
            acc = 0
            a = math.degrees(math.atan2(pts[i][1] - pts[i - 1][1], pts[i][0] - pts[i - 1][0]))
            out.append((pts[i], a))
    a0 = math.degrees(math.atan2(pts[1][1] - pts[0][1], pts[1][0] - pts[0][0]))
    out[0] = (pts[0], a0)
    return out


def swag_fn(x1, y1, x2, y2, sag):
    c = ((x1 + x2) / 2, max(y1, y2) + sag)
    return lambda t: qbez((x1, y1), c, (x2, y2), t)


def swag_d(x1, y1, x2, y2, sag):
    return "M%s,%s Q%s,%s %s,%s" % (n(x1), n(y1), n((x1 + x2) / 2), n(max(y1, y2) + sag), n(x2), n(y2))


def scallop_d(r, bumps, amp, rot=0, cx=0, cy=0):
    N = bumps * 8
    pts = []
    for i in range(N):
        t = 2 * math.pi * i / N + rot
        rr = r * (1 - amp) + r * amp * abs(math.sin(bumps * t / 2)) ** 0.6
        pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
    return "M" + " L".join("%s,%s" % (n(a), n(b)) for a, b in pts) + "Z"


def petal_d(r0, r1, width, ang, cx=0, cy=0, tip=0.0):
    """pointed petal from radius r0 to r1 at angle ang (deg)"""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)

    def rot(u, v):
        return (cx + u * ca - v * sa, cy + u * sa + v * ca)
    L = r1 - r0
    p0 = rot(r0, 0)
    c1 = rot(r0 + L * 0.35, width)
    c2 = rot(r0 + L * (0.85 - tip), width * 0.9)
    p1 = rot(r1, 0)
    c3 = rot(r0 + L * (0.85 - tip), -width * 0.9)
    c4 = rot(r0 + L * 0.35, -width)
    return "M%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%sZ" % (
        n(p0[0]), n(p0[1]), n(c1[0]), n(c1[1]), n(c2[0]), n(c2[1]), n(p1[0]), n(p1[1]),
        n(c3[0]), n(c3[1]), n(c4[0]), n(c4[1]), n(p0[0]), n(p0[1]))


def ring_petals(cnt, r0, r1, width, fill, stroke="none", sw=1, off=0, cx=0, cy=0, tip=0, op=1):
    ds = " ".join(petal_d(r0, r1, width, off + i * 360 / cnt, cx, cy, tip) for i in range(cnt))
    o = "" if op == 1 else ' opacity="%s"' % op
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (ds, fill, stroke, sw, o)


def dots_ring(cnt, r, dr, fill, cx=0, cy=0, off=0, op=1):
    o = "" if op == 1 else ' opacity="%s"' % op
    return "".join('<circle cx="%s" cy="%s" r="%s" fill="%s"%s/>' % (
        n(cx + r * math.cos(math.radians(off + i * 360 / cnt))), n(cy + r * math.sin(math.radians(off + i * 360 / cnt))), n(dr), fill, o)
        for i in range(cnt))


def mandala(d, cx, cy, R, c1, c2, c3, gold=None, detail=1):
    """layered lotus rosette"""
    gf = gold or d.gold()
    s = []
    s.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".9"/>' % (n(cx), n(cy), n(R), c3))
    s.append(ring_petals(24, R * 0.62, R * 1.0, R * 0.09, c1, gf, max(1, R * 0.012), 7.5, cx, cy))
    s.append(ring_petals(16, R * 0.45, R * 0.86, R * 0.13, c2, gf, max(1, R * 0.012), 0, cx, cy))
    s.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (n(cx), n(cy), n(R * 0.46), gf, n(R * 0.025)))
    s.append(ring_petals(12, R * 0.18, R * 0.46, R * 0.1, gf, "none", 1, 15, cx, cy))
    s.append(dots_ring(24, R * 0.52, R * 0.018, gf, cx, cy))
    s.append('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (n(cx), n(cy), n(R * 0.16), c1, gf, n(R * 0.02)))
    s.append(ring_petals(8, R * 0.03, R * 0.14, R * 0.045, gf, "none", 1, 0, cx, cy))
    if detail:
        s.append(dots_ring(24, R * 1.06, R * 0.022, gf, cx, cy, 7.5))
    return "".join(s)


# ---------------------------------------------------------------- flowers
MARI = {
    "orange": ["#7A2300", "#C2410C", "#EA6A12", "#F98A1E", "#FFB347"],
    "yellow": ["#8A4B00", "#D98A00", "#F2B705", "#FFD23F", "#FFE98A"],
    "red": ["#5C0F05", "#A3240B", "#D6420F", "#EF6A21", "#FF9E4A"],
}


def marigold_sym(d, var="orange"):
    c = MARI[var]
    s = ['<ellipse cx="1.5" cy="3" rx="20" ry="18" fill="#000" opacity=".22"/>']
    layers = [(20, 26, 0.2, 0), (16, 22, 0.24, 0.3), (12, 17, 0.26, 0.1), (8, 12, 0.3, 0.5), (4.6, 8, 0.3, 0.2)]
    for i, (r, b, a, rot) in enumerate(layers):
        gid = d.rg([(0, c[min(i + 1, 4)]), (0.7, c[min(i + 1, 4)]), (1, c[max(i - 0, 0) if i < 2 else i - 1])], 0.45, 0.4, 0.7,
                   key="mg%s%d" % (var, i))
        s.append('<path d="%s" fill="%s" stroke="%s" stroke-width=".7" stroke-opacity=".55"/>' % (scallop_d(r, b, a, rot), gid, c[0]))
    s.append('<circle cx="-5" cy="-6" r="6" fill="#fff" opacity=".18"/>')
    s.append(dots_ring(6, 2.2, 0.9, c[0], 0, 0, 0, 0.6))
    return d.sym("mari" + var, "".join(s))


def marigold(d, x, y, r=20, var="orange", rot=0):
    return d.use(marigold_sym(d, var), x, y, r / 20.0, rot)


ROSE = {
    "red": ["#4A0610", "#8E0E22", "#C21F3A", "#E24A5E", "#F58A94"],
    "pink": ["#7A1F45", "#C0406E", "#E27A9E", "#F2A7C1", "#FFD6E4"],
    "blush": ["#8A4A4A", "#D08E88", "#EDB8AE", "#F8D5CC", "#FFF0EA"],
    "white": ["#8C8076", "#CFC3B5", "#EDE4D8", "#F8F3EA", "#FFFFFF"],
    "peach": ["#8A3B1A", "#D9754A", "#F2A07A", "#F9C4A6", "#FFE6D6"],
    "wine": ["#2A0412", "#5C0B26", "#86163A", "#A83256", "#CF6A86"],
    "lilac": ["#4C2A6A", "#7E58A6", "#A889CF", "#C9B2E6", "#EEE3FA"],
    "coral": ["#7A2616", "#C9493A", "#EE7263", "#F8A294", "#FFD5CC"],
}


def rose_sym(d, var="red"):
    c = ROSE[var]
    s = ['<ellipse cx="2" cy="4" rx="20" ry="18" fill="#000" opacity=".25"/>']
    s.append('<circle r="20" fill="%s"/>' % d.rg([(0, c[1]), (1, c[0])], key="rs0" + var))
    gp = d.rg([(0, c[3]), (0.6, c[2]), (1, c[1])], 0.5, 0.2, 0.9, key="rs1" + var)
    for i in range(5):
        a = math.radians(i * 72 - 90)
        s.append('<circle cx="%s" cy="%s" r="11" fill="%s" stroke="%s" stroke-width=".8"/>' % (n(8.5 * math.cos(a)), n(8.5 * math.sin(a)), gp, c[0]))
    gp2 = d.rg([(0, c[4]), (0.6, c[3]), (1, c[2])], 0.5, 0.3, 0.9, key="rs2" + var)
    for i in range(4):
        a = math.radians(i * 90 - 45)
        s.append('<circle cx="%s" cy="%s" r="7.6" fill="%s" stroke="%s" stroke-width=".7"/>' % (n(4.6 * math.cos(a)), n(4.6 * math.sin(a)), gp2, c[1]))
    s.append('<circle r="5.5" fill="%s"/>' % c[2])
    s.append('<path d="M0,0 C2.5,-1 3,2 0.5,3.2 C-3,4.2 -5,0 -3.2,-3 C-1,-6 5,-5.5 5.5,-1 C6,3.5 2,6.5 -1.5,6" fill="none" stroke="%s" stroke-width="1.3" stroke-linecap="round"/>' % c[0])
    s.append('<path d="M-12,-10 C-8,-15 -2,-17 4,-16" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1.6" stroke-linecap="round"/>')
    return d.sym("rose" + var, "".join(s))


def rose(d, x, y, r=20, var="red", rot=0):
    return d.use(rose_sym(d, var), x, y, r / 20.0, rot)


def bloom_sym(d, var="blush"):
    """peony / ranunculus style layered bloom"""
    c = ROSE[var]
    s = ['<ellipse cx="2" cy="4" rx="21" ry="19" fill="#000" opacity=".2"/>']
    for i, (r, b, a) in enumerate([(21, 9, 0.22), (17, 8, 0.25), (13, 7, 0.28), (9, 6, 0.3), (5, 5, 0.3)]):
        gid = d.rg([(0, c[min(4, i + 1)]), (1, c[max(0, i - 1) + 1])], 0.4, 0.35, 0.8, key="bl%s%d" % (var, i))
        s.append('<path d="%s" fill="%s" stroke="%s" stroke-width=".6" stroke-opacity=".5"/>' % (scallop_d(r, b, a, i * 0.5), gid, c[1]))
    s.append(dots_ring(7, 2.5, 0.9, c[1], 0, 0, 0, 0.7))
    return d.sym("bloom" + var, "".join(s))


def bloom(d, x, y, r=20, var="blush", rot=0):
    return d.use(bloom_sym(d, var), x, y, r / 20.0, rot)


def leaf_d(L, Wd):
    return "M0,0 C%s,%s %s,%s 0,%s C%s,%s %s,%s 0,0Z" % (n(Wd), n(-L * 0.25), n(Wd * 0.7), n(-L * 0.8), n(-L),
                                                           n(-Wd * 0.7), n(-L * 0.8), n(-Wd), n(-L * 0.25))


def leaf(d, x, y, L=40, Wd=12, rot=0, c1="#2F7A3A", c2="#14502A", vein=True):
    gid = d.lg([(0, c1), (1, c2)], 0, 0, 1, 0, key="lf%s%s" % (c1, c2))
    v = '<path d="M0,-2 L0,%s" stroke="%s" stroke-width="%s" opacity=".55"/>' % (n(-L * 0.9), c2, n(max(0.8, Wd * 0.08))) if vein else ""
    return '<g transform="translate(%s %s) rotate(%s)"><path d="%s" fill="%s"/>%s</g>' % (n(x), n(y), n(rot), leaf_d(L, Wd), gid, v)


def jasmine(d, x, y, r=8, rot=0, col="#FFFFFF"):
    s = ring_petals(5, 0.5, r, r * 0.34, col, "#D8D2C4", 0.6, rot)
    s += '<circle r="%s" fill="#F2D06B"/>' % n(r * 0.18)
    return '<g transform="translate(%s %s)">%s</g>' % (n(x), n(y), s)


def mango_leaf(d, x, y, L=60, rot=0):
    return leaf(d, x, y, L, L * 0.2, rot, "#4E9A3A", "#1F5E22")


# ---------------------------------------------------------------- garlands
def marigold_string(d, x, y0, y1, r=13, vars_=("orange", "yellow"), tassel=True, spacing=None):
    sp = spacing or r * 1.55
    s = ['<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#5B3A12" stroke-width="1.2"/>' % (n(x), n(y0), n(x), n(y1))]
    k = 0
    y = y0 + r * 0.6
    while y < y1:
        s.append(marigold(d, x, y, r, vars_[k % len(vars_)], k * 37))
        k += 1
        y += sp
    if tassel:
        s.append(bell(d, x, y1 - r * 0.2, r * 0.028))
    return "".join(s)


def swag(d, x1, y1, x2, y2, sag, r=14, vars_=("orange", "yellow"), leaves=True, pattern=(0, 0, 1)):
    fn = swag_fn(x1, y1, x2, y2, sag)
    pts = sample(fn, r * 1.45)
    s = []
    if leaves:
        for i, ((px, py), a) in enumerate(pts):
            if i % 4 == 2:
                s.append(mango_leaf(d, px, py, r * 2.4, a + 90 + (25 if i % 8 == 2 else -25)))
    for i, ((px, py), a) in enumerate(pts):
        v = vars_[pattern[i % len(pattern)] % len(vars_)]
        s.append(marigold(d, px, py, r, v, i * 41))
    return "".join(s)


def rose_swag(d, x1, y1, x2, y2, sag, r=13, vars_=("red", "pink"), jas=True):
    fn = swag_fn(x1, y1, x2, y2, sag)
    pts = sample(fn, r * 1.5)
    s = []
    for i, ((px, py), a) in enumerate(pts):
        if i % 3 == 1:
            s.append(leaf(d, px, py, r * 2.2, r * 0.6, a + 90 + (30 if i % 2 else -30), "#6E9E5A", "#2F5E2A"))
    for i, ((px, py), a) in enumerate(pts):
        if jas and i % 2 == 1:
            s.append(jasmine(d, px, py, r * 0.75, i * 20))
        else:
            s.append(rose(d, px, py, r, vars_[(i // 2) % len(vars_)], i * 33))
    return "".join(s)


def bell(d, x, y, s=1):
    gf = d.lg(GOLD, 0, 0, 1, 0, key="bellg")
    body = ('<path d="M-4,-40 L4,-40 L4,-30 L-4,-30Z" fill="%s"/>'
            '<circle cx="0" cy="-44" r="6" fill="none" stroke="%s" stroke-width="3"/>'
            '<path d="M0,-32 C-16,-32 -18,-10 -20,6 C-21,14 -30,16 -30,22 L30,22 C30,16 21,14 20,6 C18,-10 16,-32 0,-32Z" fill="%s"/>'
            '<path d="M-30,22 L30,22 L28,28 L-28,28Z" fill="#8A5A12"/>'
            '<circle cx="0" cy="32" r="6" fill="%s"/>'
            '<path d="M-8,-24 C-12,-12 -13,0 -14,10" stroke="#FFF6D0" stroke-width="3" opacity=".7" fill="none" stroke-linecap="round"/>') % (gf, gf, gf, gf)
    sid = d.sym("bell", body)
    return d.use(sid, x, y + 44 * s, s)


def tassel(d, x, y, s=1, col="#B3122E"):
    gf = d.gold()
    return g('<circle cx="0" cy="0" r="7" fill="%s"/><path d="M-6,6 L6,6 L9,40 L-9,40Z" fill="%s"/>'
             '<path d="M-6,6 L6,6 L9,40 L-9,40Z" fill="none" stroke="#000" stroke-opacity=".15" stroke-dasharray="1 3" stroke-width="10"/>'
             '<rect x="-7" y="8" width="14" height="5" fill="%s"/>' % (gf, col, gf), x, y, s)


# ---------------------------------------------------------------- ornaments
def paisley_d(k=1):
    """paisley (kairi): round base at bottom, tip curling to upper right; ~90 wide, 140 tall"""
    pts = [(0, 40), (-30, 40), (-46, 12), (-40, -12), (-34, -38), (-8, -52), (10, -68), (22, -78), (26, -90), (22, -104),
           (42, -92), (52, -66), (46, -40), (42, -14), (44, 10), (36, 24), (28, 36), (16, 40), (0, 40)]
    q = [(n(a * k), n(b * k)) for a, b in pts]
    s = "M%s,%s" % q[0]
    for i in range(1, len(q), 3):
        s += " C%s,%s %s,%s %s,%s" % (q[i] + q[i + 1] + q[i + 2])
    return s + "Z"


def paisley(d, x, y, s=1, rot=0, fill="#B3122E", line="#F2C45A", inner="#FFF3D6", flip=False, detail=2):
    out = ['<path d="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (paisley_d(1), fill, line, n(2.2))]
    out.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.4" transform="translate(3 6) scale(.78)"/>' % (paisley_d(1), line))
    out.append('<path d="%s" fill="%s" opacity=".9" transform="translate(5 12) scale(.5)"/>' % (paisley_d(1), inner))
    out.append('<path d="%s" fill="%s" transform="translate(7 16) scale(.28)"/>' % (paisley_d(1), fill))
    if detail > 1:
        out.append(dots_ring(10, 44, 2.2, line, 2, 2))
        for i in range(7):
            a = math.radians(200 + i * 22)
            out.append('<circle cx="%s" cy="%s" r="2.5" fill="%s"/>' % (n(-2 + 30 * math.cos(a)), n(8 + 26 * math.sin(a)), line))
    sc = "scale(%s %s)" % (n(-s if flip else s), n(s))
    return '<g transform="translate(%s %s) rotate(%s) %s">%s</g>' % (n(x), n(y), n(rot), sc, "".join(out))


def flourish(d, x, y, s=1, rot=0, col=None, flip=False, sw=3):
    """corner scroll ornament; corner at 0,0, extends to +x and +y (~200)"""
    c = col or d.gold()
    paths = [
        "M6,6 C60,6 120,4 170,18 C200,26 206,52 186,58 C170,62 160,48 172,40",
        "M6,6 C6,60 4,120 18,170 C26,200 52,206 58,186 C62,170 48,160 40,172",
        "M20,20 C60,24 90,40 104,70 C112,88 96,100 86,90 C78,82 86,72 94,76",
        "M20,20 C24,60 40,90 70,104 C88,112 100,96 90,86 C82,78 72,86 76,94",
        "M30,30 C54,44 64,54 78,78",
    ]
    out = ['<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (p, c, n(sw)) for p in paths]
    for (lx, ly, a) in [(120, 10, -80), (10, 120, 170), (140, 14, 100), (14, 140, -10), (60, 32, -60), (32, 60, 150)]:
        out.append('<path d="%s" fill="%s" transform="translate(%s %s) rotate(%s)"/>' % (leaf_d(26, 8), c, lx, ly, a))
    out.append('<circle cx="14" cy="14" r="9" fill="%s"/><circle cx="14" cy="14" r="4" fill="#fff" opacity=".5"/>' % c)
    out.append(dots_ring(1, 0, 4, c, 110, 110))
    for (cx, cy) in [(190, 30), (30, 190), (100, 58), (58, 100)]:
        out.append('<circle cx="%s" cy="%s" r="3.5" fill="%s"/>' % (cx, cy, c))
    sc = "scale(%s %s)" % (n(-s if flip else s), n(s))
    return '<g transform="translate(%s %s) rotate(%s) %s">%s</g>' % (n(x), n(y), n(rot), sc, "".join(out))


def corners(d, x0, y0, x1, y1, s=1, col=None, sw=3):
    return (flourish(d, x0, y0, s, 0, col, sw=sw) + flourish(d, x1, y0, s, 90, col, sw=sw) +
            flourish(d, x1, y1, s, 180, col, sw=sw) + flourish(d, x0, y1, s, 270, col, sw=sw))


def bead_line(x1, y1, x2, y2, sp, r, fill, r2=None):
    L = math.hypot(x2 - x1, y2 - y1)
    k = max(1, int(L / sp))
    out = []
    for i in range(k + 1):
        t = i / k
        rr = r2 if (r2 and i % 2) else r
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(x1 + (x2 - x1) * t), n(y1 + (y2 - y1) * t), n(rr), fill))
    return "".join(out)


def rrect(x, y, w, h, r, fill, extra=""):
    return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"%s/>' % (n(x), n(y), n(w), n(h), n(r), fill, extra)


# ---------------------------------------------------------------- photo slot shapes (match static/cards.js)
def shape_d(shape, x, y, w, h):
    if shape == "arch":
        cx, sh = x + w / 2, y + h * 0.34
        return ("M%s,%s L%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s L%s,%sZ" % tuple(n(v) for v in (
            x, y + h, x, sh,
            x, sh - h * 0.12, x + w * 0.18, y + h * 0.1, cx - w * 0.1, y + h * 0.045,
            cx - w * 0.04, y + h * 0.02, cx, y + h * 0.01, cx, y,
            cx, y + h * 0.01, cx + w * 0.04, y + h * 0.02, cx + w * 0.1, y + h * 0.045,
            x + w - w * 0.18, y + h * 0.1, x + w, sh - h * 0.12, x + w, sh,
            x + w, y + h)))
    if shape == "heart":
        cx = x + w / 2
        return "M%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%sZ" % tuple(n(v) for v in (
            cx, y + h, x - w * 0.2, y + h * 0.55, x, y - h * 0.05, cx, y + h * 0.22,
            x + w, y - h * 0.05, x + w * 1.2, y + h * 0.55, cx, y + h))
    if shape in ("rounded", "pill", "rect"):
        r = {"rounded": 28, "pill": min(w, h) / 2, "rect": 0}[shape]
        if r == 0:
            return "M%s,%s H%s V%s H%sZ" % (n(x), n(y), n(x + w), n(y + h), n(x))
        return ("M%s,%s H%s A%s,%s 0 0 1 %s,%s V%s A%s,%s 0 0 1 %s,%s H%s A%s,%s 0 0 1 %s,%s V%s A%s,%s 0 0 1 %s,%sZ" % tuple(n(v) for v in (
            x + r, y, x + w - r, r, r, x + w, y + r, y + h - r, r, r, x + w - r, y + h, x + r, r, r, x, y + h - r, y + r, r, r, x + r, y)))
    if shape == "oval":
        cx, cy, rx, ry = x + w / 2, y + h / 2, w / 2, h / 2
        return "M%s,%s A%s,%s 0 1 0 %s,%s A%s,%s 0 1 0 %s,%sZ" % tuple(n(v) for v in (cx - rx, cy, rx, ry, cx + rx, cy, rx, ry, cx - rx, cy))
    raise ValueError(shape)


def couple_ghost(x, y, w, h, col, op=0.35):
    """faint two-person silhouette placeholder inside a slot box"""
    cx, by = x + w / 2, y + h
    r = min(w, h) * 0.13
    out = []
    for dx, sc in ((-r * 1.25, 1.0), (r * 1.2, 0.92)):
        hx = cx + dx
        hy = by - h * 0.42 * sc - r * 0.2
        out.append('<circle cx="%s" cy="%s" r="%s"/>' % (n(hx), n(hy), n(r * sc)))
        out.append('<path d="M%s,%s C%s,%s %s,%s %s,%s L%s,%s C%s,%s %s,%s %s,%sZ"/>' % (
            n(hx - r * 1.9 * sc), n(by), n(hx - r * 1.9 * sc), n(hy + r * 1.3), n(hx - r * 0.9), n(hy + r * 1.25), n(hx), n(hy + r * 1.25),
            n(hx), n(hy + r * 1.25), n(hx + r * 0.9), n(hy + r * 1.25), n(hx + r * 1.9 * sc), n(hy + r * 1.3), n(hx + r * 1.9 * sc), n(by)))
    return '<g fill="%s" opacity="%s">%s</g>' % (col, op, "".join(out))


def photo_slot(d, ph, fill1="#FBF3E6", fill2="#EFDCC4", ghost="#C9A98A", ring=None, ring_w=14, inner="#7A4A0E", shadow=True, pat=None):
    """frame + soft placeholder for a slot spec dict {shape,x,y,w,h}"""
    sh, x, y, w, hh = ph["shape"], ph["x"], ph["y"], ph["w"], ph["h"]
    rg_ = ring or d.gold()
    out = []
    f = ' filter="%s"' % d.shadow(0, 10, 14, "#000", 0.35) if shadow else ""
    out.append('<path d="%s" fill="%s"%s/>' % (shape_d(sh, x - ring_w, y - ring_w, w + 2 * ring_w, hh + 2 * ring_w), rg_, f))
    out.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.5" opacity=".6"/>' % (shape_d(sh, x - ring_w * 0.5, y - ring_w * 0.5, w + ring_w, hh + ring_w), inner))
    fg = d.lg([(0, fill1), (1, fill2)], 0, 0, 0, 1)
    out.append('<path d="%s" fill="%s"/>' % (shape_d(sh, x, y, w, hh), fg))
    cp = d.clip('<path d="%s"/>' % shape_d(sh, x, y, w, hh))
    inner_art = ""
    if pat:
        inner_art += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (n(x), n(y), n(w), n(hh), pat)
    inner_art += couple_ghost(x, y + hh * 0.08, w, hh * 0.92, ghost)
    out.append('<g clip-path="%s">%s</g>' % (cp, inner_art))
    out.append('<path d="%s" fill="none" stroke="%s" stroke-width="2"/>' % (shape_d(sh, x, y, w, hh), inner))
    return "".join(out)


# ---------------------------------------------------------------- output
def contrast(c1, c2):
    def lum(c):
        c = c.lstrip("#")
        v = [int(c[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        v = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in v]
        return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
    a, b = lum(c1), lum(c2)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def spec(cid, zone, title, text, accent, tone="light", tstyle="deco", align="center", photo=None, bg=None):
    s = {"id": cid, "tpl": True, "zone": list(zone), "colors": {"title": title, "text": text, "accent": accent},
         "tone": tone, "title": tstyle, "align": align}
    if photo:
        s["photo"] = dict(photo)
        s["slot"] = True
    if bg:
        for k, c in (("title", title), ("text", text), ("accent", accent)):
            if c != "gold":
                cr = contrast(c, bg)
                if cr < 4.5:
                    print("  !! contrast %s %s on %s = %.2f (%s)" % (k, c, bg, cr, cid))
    return s


def write_specs(cat, specs):
    p = os.path.join(HERE, "out", cat + ".json")
    json.dump(specs, open(p, "w"), ensure_ascii=False, indent=1)
    print("wrote", p)


# ---------------------------------------------------------------- tubes (tapered strokes as filled outlines)
def tube_pts(fn, w0, w1, steps=60, wfn=None):
    pts = [fn(i / steps) for i in range(steps + 1)]
    L, R = [], []
    for i, p in enumerate(pts):
        a = pts[min(i + 1, steps)]
        b = pts[max(i - 1, 0)]
        dx, dy = a[0] - b[0], a[1] - b[1]
        m = math.hypot(dx, dy) or 1
        nx, ny = -dy / m, dx / m
        t = i / steps
        w = wfn(t) if wfn else w0 + (w1 - w0) * t
        L.append((p[0] + nx * w / 2, p[1] + ny * w / 2))
        R.append((p[0] - nx * w / 2, p[1] - ny * w / 2))
    return pts, L, R


def tube_d(fn, w0, w1, steps=60, wfn=None):
    pts, L, R = tube_pts(fn, w0, w1, steps, wfn)
    poly = L + R[::-1]
    return "M" + " L".join("%s,%s" % (n(a), n(b)) for a, b in poly) + "Z"


def cub(p0, p1, p2, p3):
    return lambda t: bez(p0, p1, p2, p3, t)


# ================================================================ INVITATION motifs
def elephant(d, x, y, s=1, flip=False, skin=("#9AA0AB", "#6B7180", "#4A4F5C"), cloth=("#B3122E", "#7A0A1E"),
             trim=None, style="painted", seed=1):
    """caparisoned elephant facing right (flip=True faces left). (x,y)=left-bottom of ~470x380 box scaled by s"""
    gf = trim or d.gold()
    if style == "gold":
        skinfill = d.lg([(0, "#F4D98A"), (0.5, "#D6A443"), (1, "#8C5A17")], 0, 0, 0.3, 1, key="elgold")
        far = d.lg([(0, "#B98A35"), (1, "#6E450F")], 0, 0, 0, 1, key="elgoldfar")
        line = "#6E420C"
    else:
        skinfill = d.lg([(0, skin[0]), (0.6, skin[1]), (1, skin[2])], 0, 0, 0.25, 1, key="elsk%s" % skin[0])
        far = d.lg([(0, skin[1]), (1, skin[2])], 0, 0, 0, 1, key="elfar%s" % skin[0])
        line = skin[2]
    o = []
    # tail
    o.append('<path d="%s" fill="%s"/>' % (tube_d(cub((50, 160), (30, 190), (40, 240), (30, 272)), 7, 3), far))
    o.append('<path d="M30,268 C22,280 26,296 30,300 C34,296 40,282 30,268Z" fill="%s"/>' % line)
    # far legs
    o.append('<path d="M112,250 L152,250 L154,366 C154,376 120,378 114,368Z" fill="%s"/>' % far)
    o.append('<path d="M282,236 L322,236 L326,364 C326,374 292,376 286,366Z" fill="%s"/>' % far)
    for lx in (114, 286):
        o.append('<rect x="%d" y="338" width="40" height="10" rx="3" fill="%s"/>' % (lx, gf))
    # body + head
    body = ("M45,150 C80,95 190,72 255,86 C285,58 352,55 378,96 C392,118 394,150 386,176 C378,200 362,214 346,210 "
            "C342,226 340,242 338,262 L341,366 C341,378 306,380 302,370 L298,292 C270,300 180,300 150,292 L146,370 "
            "C144,380 108,380 104,370 L96,296 C70,290 50,250 45,210 C42,185 42,165 45,150Z")
    o.append('<path d="%s" fill="%s"/>' % (body, skinfill))
    # trunk
    tfn = cub((372, 150), (405, 262), (478, 238), (462, 96))
    tip = cub((462, 96), (458, 66), (432, 64), (436, 86))
    o.append('<path d="%s" fill="%s"/>' % (tube_d(tfn, 50, 16), skinfill))
    o.append('<path d="%s" fill="%s"/>' % (tube_d(tip, 16, 9, 20), skinfill))
    # trunk wrinkles
    pts, L, R = tube_pts(tfn, 50, 16, 30)
    for i in range(6, 28, 2):
        o.append('<path d="M%s,%s Q%s,%s %s,%s" stroke="%s" stroke-width="1.6" fill="none" opacity=".45"/>' % (
            n(L[i][0]), n(L[i][1]), n(pts[i][0] + (L[i][0] - pts[i][0]) * 0.2 + 3), n(pts[i][1] + 3), n(R[i][0]), n(R[i][1]), line))
    # painted dots on trunk
    for i in range(4, 26, 4):
        px, py = pts[i]
        o.append('<circle cx="%s" cy="%s" r="5" fill="%s"/><circle cx="%s" cy="%s" r="2.2" fill="%s"/>' % (n(px), n(py), gf, n(px), n(py), cloth[0]))
    # ear
    o.append('<path d="M300,100 C255,95 234,150 244,198 C254,240 292,244 314,222 C330,200 334,140 300,100Z" fill="%s" stroke="%s" stroke-width="2" stroke-opacity=".5"/>' % (far, line))
    o.append('<path d="M296,116 C266,116 252,156 260,192 C268,222 292,226 306,210" fill="none" stroke="%s" stroke-width="5" opacity=".8"/>' % gf)
    o.append(dots_ring(1, 0, 6, cloth[0], 280, 170))
    # tusk
    o.append('<path d="M352,198 C366,228 398,234 414,214 C398,224 372,216 362,194Z" fill="#FFF8E6" stroke="#CDBE9E" stroke-width="1.5"/>')
    # eye
    o.append('<path d="M340,126 Q352,116 362,126 Q352,132 340,126Z" fill="#1E1A1A"/><circle cx="353" cy="125" r="1.6" fill="#fff"/>')
    o.append('<path d="M338,118 Q352,108 366,120" stroke="%s" stroke-width="2" fill="none" opacity=".6"/>' % line)
    # forehead ornament (mathapatti)
    o.append('<path d="M322,76 C342,60 372,68 384,96 C384,126 372,150 356,164 C348,132 336,104 322,76Z" fill="%s" stroke="%s" stroke-width="1.5"/>' % (gf, line))
    o.append('<path d="M334,84 C348,76 366,82 374,100 C372,120 364,136 356,146 C350,124 342,102 334,84Z" fill="%s"/>' % cloth[0])
    o.append('<circle cx="358" cy="104" r="7" fill="#1E8F5A" stroke="%s" stroke-width="2"/>' % gf)
    for i, (px, py) in enumerate([(362, 150), (372, 138), (380, 122)]):
        o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.5"/>' % (px, py, px + 6, py + 22, gf))
        o.append('<circle cx="%d" cy="%d" r="3.5" fill="%s"/>' % (px + 6, py + 24, gf))
    # caparison cloth
    cl = ("M126,98 C180,80 240,78 274,90 L288,232 C274,248 256,232 242,248 C228,232 212,248 198,232 "
          "C184,248 168,232 154,248 C140,232 126,246 114,236Z")
    clf = d.lg([(0, cloth[0]), (1, cloth[1])], 0, 0, 0, 1, key="cl%s" % cloth[0])
    o.append('<path d="%s" fill="%s"/>' % (cl, clf))
    cp = d.clip('<path d="%s"/>' % cl)
    inner = []
    rr = random.Random(seed)
    for (px, py) in [(160, 140), (215, 130), (250, 190), (185, 200), (140, 205), (262, 128)]:
        inner.append(paisley(d, px, py, 0.32, rr.randint(-30, 30), cloth[1], gf, cloth[0], detail=1))
    for i in range(40):
        inner.append('<circle cx="%d" cy="%d" r="1.8" fill="%s" opacity=".8"/>' % (rr.randint(120, 285), rr.randint(95, 240), gf))
    o.append('<g clip-path="%s">%s</g>' % (cp, "".join(inner)))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="7"/>' % (cl, gf))
    o.append('<path d="M126,98 C180,80 240,78 274,90" fill="none" stroke="%s" stroke-width="3" transform="translate(0 12)" opacity=".7"/>' % gf)
    for tx in (154, 198, 242, 288, 114):
        o.append(tassel(d, tx, 244 if tx != 114 else 236, 0.55, cloth[0]))
    # saddle blanket roll
    o.append('<path d="M150,90 C190,70 240,70 262,84 L262,96 C236,84 190,84 150,102Z" fill="%s"/>' % gf)
    # anklets near legs
    for lx in (104, 302):
        o.append('<rect x="%d" y="332" width="40" height="12" rx="3" fill="%s"/>' % (lx - 1, gf))
        o.append(bead_line(lx + 4, 350, lx + 36, 350, 8, 3, gf))
    # toenails
    for lx in (108, 306):
        o.append('<path d="M%d,370 q5,-6 10,0 M%d,370 q5,-6 10,0" stroke="#EDE3CF" stroke-width="3" fill="none"/>' % (lx + 4, lx + 18))
    # highlight on back
    o.append('<path d="M70,140 C110,100 180,84 240,88" stroke="#fff" stroke-opacity=".22" stroke-width="8" fill="none" stroke-linecap="round"/>')
    sc = "scale(%s %s)" % (n(-s if flip else s), n(s))
    tx = x + (470 * s if flip else 0)
    return '<g transform="translate(%s %s) %s translate(0 -380)">%s</g>' % (n(tx), n(y), sc, "".join(o))


def kalash(d, x, y, s=1, body=("#E6A23C", "#B8732A", "#7A4515"), cloth="#C8102E", swastik=True, leaves=7):
    """kalash with mango leaves and coconut. (x,y)=bottom centre; ~160 wide x 250 tall"""
    gb = d.lg([(0, body[2]), (0.3, body[0]), (0.45, "#FFE6A8"), (0.6, body[0]), (1, body[2])], 0, 0, 1, 0, key="kb%s" % body[0])
    o = ['<ellipse cx="0" cy="2" rx="60" ry="10" fill="#000" opacity=".25"/>']
    for i in range(leaves):
        a = -75 + i * 150 / (leaves - 1)
        o.append(leaf(d, 0, -128, 78, 16, a, "#5DA044", "#1F5E22"))
    # coconut
    o.append('<ellipse cx="0" cy="-165" rx="30" ry="38" fill="%s"/>' % d.rg([(0, "#A0673A"), (1, "#4E2E14")], 0.4, 0.35, 0.7, key="coco"))
    for i in range(7):
        o.append('<path d="M%d,-200 C%d,-190 %d,-170 %d,-150" stroke="#3A200C" stroke-width="1.2" fill="none" opacity=".6"/>' % (-14 + i * 5, -16 + i * 5, -18 + i * 6, -20 + i * 7))
    o.append('<path d="M-6,-203 C-2,-214 6,-214 8,-204" stroke="#4E2E14" stroke-width="4" fill="none"/>')
    # cloth over coconut shoulders
    o.append('<path d="M-34,-150 C-20,-168 20,-168 34,-150 C38,-136 28,-128 20,-126 L-20,-126 C-28,-128 -38,-136 -34,-150Z" fill="%s"/>' % cloth)
    o.append('<path d="M-34,-150 C-20,-168 20,-168 34,-150" stroke="%s" stroke-width="4" fill="none"/>' % d.gold())
    # neck and rim
    o.append('<rect x="-24" y="-126" width="48" height="18" fill="%s"/>' % gb)
    o.append('<ellipse cx="0" cy="-126" rx="34" ry="8" fill="%s" stroke="%s" stroke-width="1"/>' % (gb, body[2]))
    for i, c in enumerate(["#D7261E", "#F2C12E", "#D7261E"]):
        o.append('<rect x="-24" y="%d" width="48" height="3" fill="%s"/>' % (-120 + i * 4, c))
    # body
    o.append('<path d="M-38,0 C-76,-14 -80,-78 -40,-100 L-24,-108 L24,-108 L40,-100 C80,-78 76,-14 38,0Z" fill="%s"/>' % gb)
    o.append('<path d="M-60,-40 C-20,-30 20,-30 60,-40" stroke="%s" stroke-width="3" fill="none" opacity=".8"/>' % d.gold())
    o.append('<path d="M-66,-60 C-20,-50 20,-50 66,-60" stroke="%s" stroke-width="1.5" fill="none" opacity=".6"/>' % body[2])
    o.append('<ellipse cx="0" cy="0" rx="40" ry="7" fill="%s"/>' % body[2])
    o.append('<path d="M-46,-86 C-58,-70 -60,-40 -48,-16" stroke="#FFF1C9" stroke-opacity=".55" stroke-width="5" fill="none" stroke-linecap="round"/>')
    if swastik:
        sw = ('<g transform="translate(0 -70)" stroke="#C8102E" stroke-width="3.2" fill="none" stroke-linecap="square">'
              '<path d="M0,-12 L0,12 M-12,0 L12,0 M0,-12 L10,-12 M12,0 L12,10 M0,12 L-10,12 M-12,0 L-12,-10"/></g>'
              '<g fill="#C8102E"><circle cx="-6" cy="-76" r="2"/><circle cx="6" cy="-76" r="2"/><circle cx="-6" cy="-64" r="2"/><circle cx="6" cy="-64" r="2"/></g>')
        o.append(sw)
    return g("".join(o), x, y, s)


def shehnai(d, x, y, s=1, rot=0, wood=("#6B3A1A", "#A8622E"), flip=False):
    """shehnai pointing right, mouth at (0,0); ~330 long"""
    gw = d.lg([(0, wood[0]), (0.45, wood[1]), (0.6, "#D89A5E"), (1, wood[0])], 0, 0, 0, 1, key="sw%s" % wood[0])
    gm = d.lg(GOLD, 0, 0, 0, 1, key="goldv")
    o = []
    o.append('<path d="M-22,-2 L0,-4 L0,4 L-22,2Z" fill="#D8C49A"/>')  # reed
    o.append('<rect x="0" y="-7" width="16" height="14" rx="3" fill="%s"/>' % gm)
    o.append('<path d="M14,-7 L240,-13 L240,13 L14,7Z" fill="%s"/>' % gw)
    for bx in (40, 90, 140, 190, 232):
        o.append('<rect x="%d" y="-12" width="7" height="24" rx="2" fill="%s"/>' % (bx, gm))
    for hx in (60, 78, 104, 122, 158, 176, 206):
        o.append('<circle cx="%d" cy="-3" r="3" fill="#2A140A"/>' % hx)
    o.append('<path d="M238,-14 C270,-16 300,-40 322,-48 L322,48 C300,40 270,16 238,14Z" fill="%s"/>' % gm)
    o.append('<ellipse cx="322" cy="0" rx="9" ry="48" fill="%s" stroke="#7A4A0E" stroke-width="2"/>' % d.lg([(0, "#8A5A12"), (1, "#E9C46A")], 0, 0, 1, 0, key="bellin"))
    o.append('<path d="M250,-10 C272,-14 292,-28 312,-36" stroke="#FFF6D0" stroke-width="3" fill="none" opacity=".7"/>')
    # tassel cord
    o.append('<path d="M120,10 C124,40 150,50 152,74" stroke="#C8102E" stroke-width="2.5" fill="none"/>')
    o.append(tassel(d, 152, 72, 0.7))
    return g("".join(o), x, y, s, rot, flip=flip)


def ganesh(d, cx, cy, s=1, col=None, bg="#7A0A1E", sw=4.5):
    """stylised geometric Ganesh (line art) centred at cx,cy; ~200 tall"""
    c = col or d.gold()
    o = []
    st = 'fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"' % (c, n(sw))
    # crown
    o.append('<path d="M-34,-58 L-40,-92 L-20,-78 L0,-112 L20,-78 L40,-92 L34,-58Z" fill="%s"/>' % c)
    o.append('<circle cx="0" cy="-118" r="6" fill="%s"/>' % c)
    o.append('<path d="M-32,-64 L32,-64" stroke="%s" stroke-width="3"/>' % bg)
    o.append('<circle cx="0" cy="-84" r="4" fill="%s"/>' % bg)
    # head
    o.append('<path d="M-38,-56 C-44,-30 -40,-4 -20,10 M38,-56 C44,-30 40,-4 20,10" %s/>' % st)
    # ears
    o.append('<path d="M-40,-50 C-80,-64 -104,-30 -94,0 C-86,26 -58,34 -36,16" %s/>' % st)
    o.append('<path d="M40,-50 C80,-64 104,-30 94,0 C86,26 58,34 36,16" %s/>' % st)
    o.append('<path d="M-52,-36 C-76,-40 -86,-16 -78,2 C-72,16 -56,20 -44,10" %s opacity=".7"/>' % st.replace('stroke-width="%s"' % n(sw), 'stroke-width="%s"' % n(sw * 0.6)))
    o.append('<path d="M52,-36 C76,-40 86,-16 78,2 C72,16 56,20 44,10" %s opacity=".7"/>' % st.replace('stroke-width="%s"' % n(sw), 'stroke-width="%s"' % n(sw * 0.6)))
    # eyes
    o.append('<path d="M-24,-30 Q-16,-38 -8,-30 M24,-30 Q16,-38 8,-30" %s/>' % st)
    # tilak
    o.append('<path d="M-8,-56 L-8,-44 Q0,-38 8,-44 L8,-56" %s/><circle cx="0" cy="-48" r="3.5" fill="%s"/>' % (st, c))
    # trunk
    o.append('<path d="M-12,-20 C-14,10 -10,40 4,62 C14,78 34,82 42,70 C48,60 38,50 30,56" %s/>' % st)
    o.append('<path d="M12,-20 C10,8 12,30 22,46" %s/>' % st)
    # tusk
    o.append('<path d="M-20,10 L-30,26" %s/>' % st)
    # dots
    o.append(dots_ring(1, 0, 4, c, 0, 30))
    return g("".join(o), cx, cy, s)


def cusped_arch_d(x, y, w, h, spring=0.42, lobes=7):
    """Mughal multi-foil arch outline (closed), opening box x,y,w,h"""
    cx = x + w / 2
    sy = y + h * spring
    pts = []
    # arch curve: pointed ogee-ish from left spring to apex
    top = []
    N = 120
    for i in range(N + 1):
        t = i / N
        # base shape: pointed arch
        ang = math.pi * (1 - t)
        px = cx + (w / 2) * math.cos(ang)
        py = sy - (sy - y) * (math.sin(ang) ** 0.8) - (sy - y) * 0.12 * (1 - abs(math.cos(ang))) ** 6
        # lobes (foils)
        lob = abs(math.sin(lobes * math.pi * t))
        k = 1 - 0.05 * lob
        px = cx + (px - cx) * k
        py = sy - (sy - py) * k
        top.append((px, py))
    s = "M%s,%s L%s,%s " % (n(x), n(y + h), n(x), n(sy))
    s += " ".join("L%s,%s" % (n(a), n(b)) for a, b in top)
    s += " L%s,%s Z" % (n(x + w), n(y + h))
    return s


def jali_pattern(d, col="#F3D9A4", bg=None, sz=36, sw=2.2):
    c = ('<rect width="%d" height="%d" fill="%s"/>' % (sz, sz, bg) if bg else "")
    h = sz / 2
    c += ('<path d="M%s,0 L%s,%s L%s,%s L%s,%s Z" fill="none" stroke="%s" stroke-width="%s"/>' % (n(h), n(sz), n(h), n(h), n(sz), 0, n(h), col, n(sw)))
    c += '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (n(h), n(h), n(sz * 0.18), col, n(sw * 0.8))
    c += '<circle cx="0" cy="0" r="%s" fill="%s"/><circle cx="%d" cy="0" r="%s" fill="%s"/><circle cx="0" cy="%d" r="%s" fill="%s"/><circle cx="%d" cy="%d" r="%s" fill="%s"/>' % (
        n(sz * 0.08), col, sz, n(sz * 0.08), col, sz, n(sz * 0.08), col, sz, sz, n(sz * 0.08), col)
    return d.pattern(sz, sz, c, key="jali%s%s%s" % (col, bg, sz))


def dome(d, cx, by, w, h, fill, gf, finial=True):
    """onion dome sitting on baseline by"""
    o = ['<path d="M%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%sZ" fill="%s"/>' % (
        n(cx - w / 2), n(by), n(cx - w * 0.62), n(by - h * 0.55), n(cx - w * 0.1), n(by - h * 0.7), n(cx), n(by - h),
        n(cx + w * 0.1), n(by - h * 0.7), n(cx + w * 0.62), n(by - h * 0.55), n(cx + w / 2), n(by), fill)]
    o.append('<path d="M%s,%s C%s,%s %s,%s %s,%s" stroke="#fff" stroke-opacity=".3" stroke-width="%s" fill="none" stroke-linecap="round"/>' % (
        n(cx - w * 0.32), n(by - h * 0.12), n(cx - w * 0.36), n(by - h * 0.45), n(cx - w * 0.1), n(by - h * 0.62), n(cx - w * 0.04), n(by - h * 0.8), n(max(2, w * 0.05))))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>' % (n(cx - w * 0.55), n(by - 2), n(w * 1.1), n(max(6, h * 0.08)), n(3), gf))
    if finial:
        o.append('<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="%s"/>' % (n(cx), n(by - h), n(cx), n(by - h - h * 0.35), gf, n(max(2, w * 0.03))))
        o.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(cx), n(by - h - h * 0.12), n(max(3, w * 0.05)), gf))
        o.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(cx), n(by - h - h * 0.26), n(max(2, w * 0.035)), gf))
    return "".join(o)


# ================================================================ v2 additions: arches, panels, patterns
def pointed_arch_pts(x, y, w, h, spring=0.4, k=0.62, N=160):
    """points along a pointed (two-centred) arch from left spring to right spring; apex at (x+w/2, y)"""
    cx = x + w / 2
    sy = y + h * spring
    R = w * k
    # left arc centre at (x+R, sy): must reach apex (cx, y)
    # scale vertical so apex hits y
    cLx = x + R
    ca = (cx - cLx) / R
    a_apex = math.acos(max(-1, min(1, ca)))
    top = R * math.sin(a_apex)
    sc = (sy - y) / top if top else 1
    pts = []
    for i in range(N // 2 + 1):
        a = math.pi - (math.pi - a_apex) * i / (N // 2)
        pts.append((cLx + R * math.cos(a), sy - R * math.sin(a) * sc))
    right = [(2 * cx - px, py) for px, py in reversed(pts[:-1])]
    return pts + right


def foil_arch_d(x, y, w, h, spring=0.4, lobes=11, amp=None, k=0.62, base=True):
    """Mughal multi-foil (cusped) arch outline: closed shape (opening) with bottom at y+h"""
    amp = amp if amp is not None else w * 0.022
    pts = pointed_arch_pts(x, y, w, h, spring, k, 360)
    cx = x + w / 2
    L = [0]
    for i in range(1, len(pts)):
        L.append(L[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    tot = L[-1]
    out = []
    for i, (px, py) in enumerate(pts):
        s = L[i] / tot
        dd = amp * (1 - abs(math.sin(math.pi * lobes * s))) ** 1.6
        # inward normal
        a = pts[min(i + 1, len(pts) - 1)]
        b = pts[max(i - 1, 0)]
        dx, dy = a[0] - b[0], a[1] - b[1]
        m = math.hypot(dx, dy) or 1
        nx, ny = dy / m, -dx / m  # points inward for left->right traversal (clockwise on screen)
        nx, ny = -nx, -ny
        out.append((px + nx * dd, py + ny * dd))
    sy = y + h * spring
    s = "M%s,%s L%s,%s " % (n(x), n(y + h), n(out[0][0]), n(out[0][1]))
    s += " ".join("L%s,%s" % (n(a), n(b)) for a, b in out[1:])
    s += " L%s,%s Z" % (n(x + w), n(y + h))
    return s


def ogee_arch_d(x, y, w, h, spring=0.45):
    """simple pointed arch (smooth) with tiny ogee tip"""
    pts = pointed_arch_pts(x, y, w, h, spring, 0.62, 120)
    return "M%s,%s " % (n(x), n(y + h)) + " ".join("L%s,%s" % (n(a), n(b)) for a, b in pts) + " L%s,%sZ" % (n(x + w), n(y + h))


def arch_ring_d(x, y, w, h, t, spring=0.4, lobes=9, amp=None):
    """frame ring = outer foil arch minus inner (evenodd)"""
    return foil_arch_d(x - t, y - t * 1.3, w + 2 * t, h + t * 1.3, spring, lobes, 0) + " " + foil_arch_d(x, y, w, h, spring, lobes, amp)


def grain_rect(d, x, y, w, h, op=0.08, color="#3A2A1A", freq=0.9, clip=None):
    c = ' clip-path="%s"' % clip if clip else ""
    return '<rect x="%s" y="%s" width="%s" height="%s" fill="#fff" filter="%s"%s/>' % (n(x), n(y), n(w), n(h), d.grain(freq, op, color), c)


def damask_pattern(d, col, bg, sz=120, op=0.5, key=None):
    """small symmetric floral damask (paisley pair + dots) repeat"""
    h = sz / 2
    m = []
    if bg:
        m.append('<rect width="%s" height="%s" fill="%s"/>' % (n(sz), n(sz), bg))
    s = sz / 260.0
    for (px, py) in ((h, h), (0, 0), (sz, 0), (0, sz), (sz, sz)):
        m.append('<g transform="translate(%s %s) scale(%s)" opacity="%s">' % (n(px), n(py), n(s), op))
        m.append('<path d="M0,-70 C22,-40 22,-10 0,8 C-22,-10 -22,-40 0,-70Z" fill="%s"/>' % col)
        m.append('<path d="M0,70 C14,50 14,30 0,18 C-14,30 -14,50 0,70Z" fill="%s"/>' % col)
        m.append('<path d="M-70,0 C-50,-14 -30,-14 -18,0 C-30,14 -50,14 -70,0Z M70,0 C50,-14 30,-14 18,0 C30,14 50,14 70,0Z" fill="%s"/>' % col)
        m.append('<circle r="8" fill="%s"/>' % col)
        for a in range(45, 360, 90):
            r_ = math.radians(a)
            m.append('<circle cx="%s" cy="%s" r="6" fill="%s"/>' % (n(46 * math.cos(r_)), n(46 * math.sin(r_)), col))
        m.append('</g>')
    return d.pattern(sz, sz, "".join(m), key=key or "dam%s%s%s" % (col, bg, sz))


def buti_pattern(d, col, bg=None, sz=90, op=0.35, rot=0):
    """tiny paisley buti repeat in a half-drop"""
    m = []
    if bg:
        m.append('<rect width="%s" height="%s" fill="%s"/>' % (n(sz), n(sz * 2), bg))
    for (px, py, fl) in ((sz * 0.5, sz * 0.5, False), (0, sz * 1.5, True), (sz, sz * 1.5, True)):
        m.append('<g transform="translate(%s %s) scale(%s %s) rotate(-20)" opacity="%s"><path d="%s" fill="%s"/>'
                 '<path d="%s" fill="none" stroke="%s" stroke-width="3" transform="translate(4 8) scale(.55)" opacity=".6"/></g>' % (
                     n(px), n(py), n(-sz / 420 if fl else sz / 420), n(sz / 420), op, paisley_d(1), col, paisley_d(1), bg or "#fff"))
    return d.pattern(sz, sz * 2, "".join(m), transform="rotate(%s)" % rot if rot else "", key="buti%s%s%s%s" % (col, bg, sz, rot))


def gold_frame_rect(d, x, y, w, h, r=0, sw=6, gf=None, inner=True, col2=None):
    gf = gf or d.gold()
    o = ['<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (n(x), n(y), n(w), n(h), n(r), gf, n(sw))]
    if inner:
        o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (
            n(x + sw * 2.2), n(y + sw * 2.2), n(w - sw * 4.4), n(h - sw * 4.4), n(max(0, r - sw * 2)), col2 or gf, n(max(1.2, sw * 0.3))))
    return "".join(o)


def gota_border(d, x, y, w, h, col="#E9C46A", sz=22, bg=None):
    """gota-patti lace: repeating little leaf/scallop along a rectangle, returns strokes"""
    o = []
    def run(x1, y1, x2, y2, ang):
        L = math.hypot(x2 - x1, y2 - y1)
        k = int(L / sz)
        for i in range(k):
            t = (i + 0.5) / k
            px, py = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
            o.append('<g transform="translate(%s %s) rotate(%s)"><path d="M0,0 C%s,%s %s,%s 0,%s C%s,%s %s,%s 0,0Z" fill="%s"/><circle cx="0" cy="%s" r="%s" fill="%s"/></g>' % (
                n(px), n(py), ang, n(sz * 0.35), n(sz * 0.2), n(sz * 0.3), n(sz * 0.6), n(sz * 0.75), n(-sz * 0.3), n(sz * 0.6), n(-sz * 0.35), n(sz * 0.2), col,
                n(-sz * 0.2), n(sz * 0.1), col))
    run(x, y, x + w, y, 0)
    run(x + w, y, x + w, y + h, 90)
    run(x + w, y + h, x, y + h, 180)
    run(x, y + h, x, y, 270)
    return "".join(o)


def bokeh(d, rnd, n_, x0, y0, x1, y1, r0, r1, cols, op0=0.12, op1=0.35):
    b = d.blur(3)
    o = []
    for i in range(n_):
        o.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>' % (
            n(rnd.uniform(x0, x1)), n(rnd.uniform(y0, y1)), n(rnd.uniform(r0, r1)), rnd.choice(cols), n(rnd.uniform(op0, op1))))
    return '<g filter="%s">%s</g>' % (b, "".join(o))


def rays(cx, cy, n_, r, col, op=0.12, w=6):
    o = []
    for i in range(n_):
        a = 2 * math.pi * i / n_
        a2 = a + math.radians(w / 2)
        a1 = a - math.radians(w / 2)
        o.append("M%s,%s L%s,%s L%s,%sZ" % (n(cx), n(cy), n(cx + r * math.cos(a1)), n(cy + r * math.sin(a1)), n(cx + r * math.cos(a2)), n(cy + r * math.sin(a2))))
    return '<path d="%s" fill="%s" opacity="%s"/>' % (" ".join(o), col, op)


def sparkle(x, y, r, col="#FFF6D0", op=1):
    return '<path d="M%s,%s Q%s,%s %s,%s Q%s,%s %s,%s Q%s,%s %s,%s Q%s,%s %s,%sZ" fill="%s" opacity="%s"/>' % (
        n(x), n(y - r), n(x + r * 0.12), n(y - r * 0.12), n(x + r), n(y), n(x + r * 0.12), n(y + r * 0.12), n(x), n(y + r),
        n(x - r * 0.12), n(y + r * 0.12), n(x - r), n(y), n(x - r * 0.12), n(y - r * 0.12), n(x), n(y - r), col, op)


def ellipse_pts(cx, cy, rx, ry, cnt, a0=-90):
    return [(cx + rx * math.cos(math.radians(a0 + 360 * i / cnt)), cy + ry * math.sin(math.radians(a0 + 360 * i / cnt)), a0 + 360 * i / cnt) for i in range(cnt)]


def path_pts(dstr_pts, spacing):
    """evenly spaced points along a polyline [(x,y),...]"""
    out = []
    acc = 0
    for i in range(1, len(dstr_pts)):
        (x0, y0), (x1, y1) = dstr_pts[i - 1], dstr_pts[i]
        seg = math.hypot(x1 - x0, y1 - y0)
        t = 0
        while acc + seg - t >= spacing:
            t += spacing - acc
            acc = 0
            f = t / seg
            out.append((x0 + (x1 - x0) * f, y0 + (y1 - y0) * f, math.degrees(math.atan2(y1 - y0, x1 - x0))))
        acc += seg - t
    return out


def rrect_pts(x, y, w, h, r, N=240):
    pts = []
    per = 2 * (w + h - 4 * r) + 2 * math.pi * r
    # sample by walking
    segs = []
    import itertools
    for i in range(N):
        s = per * i / N
        pts.append(_rr_at(x, y, w, h, r, s))
    return pts


def _rr_at(x, y, w, h, r, s):
    a = w - 2 * r
    b = h - 2 * r
    q = math.pi * r / 2
    for seg in range(8):
        L = [a, q, b, q, a, q, b, q][seg]
        if s <= L or seg == 7:
            t = s
            if seg == 0: return (x + r + t, y)
            if seg == 1: an = -90 + 90 * t / q; return (x + w - r + r * math.cos(math.radians(an)), y + r + r * math.sin(math.radians(an)))
            if seg == 2: return (x + w, y + r + t)
            if seg == 3: an = 90 * t / q; return (x + w - r + r * math.cos(math.radians(an)), y + h - r + r * math.sin(math.radians(an)))
            if seg == 4: return (x + w - r - t, y + h)
            if seg == 5: an = 90 + 90 * t / q; return (x + r + r * math.cos(math.radians(an)), y + h - r + r * math.sin(math.radians(an)))
            if seg == 6: return (x, y + h - r - t)
            an = 180 + 90 * t / q; return (x + r + r * math.cos(math.radians(an)), y + r + r * math.sin(math.radians(an)))
        s -= L


def flower_ring(d, pts, r, kind="marigold", vars_=("orange", "yellow", "red"), leaf_every=3, leafcol=("#5DA044", "#1F5E22"), cx=None, cy=None):
    """place flowers at points [(x,y,ang)...]; leaves peek outward"""
    o = []
    fn = marigold if kind == "marigold" else (rose if kind == "rose" else bloom)
    for i, p in enumerate(pts):
        x, y = p[0], p[1]
        if leaf_every and i % leaf_every == 0:
            if cx is not None:
                a = math.degrees(math.atan2(y - cy, x - cx)) + 90
            else:
                a = (p[2] if len(p) > 2 else 0) - 90
            o.append(leaf(d, x, y, r * 2.6, r * 0.7, a + (20 if i % 2 else -20), leafcol[0], leafcol[1]))
    for i, p in enumerate(pts):
        o.append(fn(d, p[0], p[1], r, vars_[i % len(vars_)], i * 47))
    return "".join(o)


def heart_pts(x, y, w, h, N=200):
    cx = x + w / 2
    a = [(cx, y + h), (x - w * 0.2, y + h * 0.55), (x, y - h * 0.05), (cx, y + h * 0.22)]
    b = [(cx, y + h * 0.22), (x + w, y - h * 0.05), (x + w * 1.2, y + h * 0.55), (cx, y + h)]
    pts = [bez(*a, i / (N // 2)) for i in range(N // 2)] + [bez(*b, i / (N // 2)) for i in range(N // 2 + 1)]
    return pts


def arch_pts(x, y, w, h, N=200):
    """points along the engine 'arch' shape top curve (left bottom -> right bottom)"""
    cx, sh = x + w / 2, y + h * 0.34
    segs = [((x, sh), (x, sh - h * 0.12), (x + w * 0.18, y + h * 0.1), (cx - w * 0.1, y + h * 0.045)),
            ((cx - w * 0.1, y + h * 0.045), (cx - w * 0.04, y + h * 0.02), (cx, y + h * 0.01), (cx, y)),
            ((cx, y), (cx, y + h * 0.01), (cx + w * 0.04, y + h * 0.02), (cx + w * 0.1, y + h * 0.045)),
            ((cx + w * 0.1, y + h * 0.045), (x + w - w * 0.18, y + h * 0.1), (x + w, sh - h * 0.12), (x + w, sh))]
    pts = [(x, y + h)]
    for sgm in segs:
        pts += [bez(*sgm, i / 30) for i in range(31)]
    pts.append((x + w, y + h))
    return pts
