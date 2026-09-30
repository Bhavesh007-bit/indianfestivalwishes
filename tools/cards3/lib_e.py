"""Shared SVG helpers for agent E (birthday, inv-birthday-party, inv-naming-ceremony).

Every drawing function takes an Art instance `a` which collects <defs>
(gradients, filters, patterns) so components can register what they need.
"""
import math, random, json, os, sys

W, H = 1080, 1350
HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------- colours
def _h2r(c):
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _r2h(r):
    return "#%02X%02X%02X" % tuple(max(0, min(255, int(round(v)))) for v in r)


def mix(c1, c2, t):
    a, b = _h2r(c1), _h2r(c2)
    return _r2h([a[i] + (b[i] - a[i]) * t for i in range(3)])


def lt(c, t=0.3):
    return mix(c, "#FFFFFF", t)


def dk(c, t=0.3):
    return mix(c, "#000000", t)


def lum(c):
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = _h2r(c)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(c1, c2):
    a, b = lum(c1), lum(c2)
    if a < b:
        a, b = b, a
    return (a + 0.05) / (b + 0.05)


# ---------------------------------------------------------------- Art
class Art:
    def __init__(self, seed=1):
        self.defs = []
        self.n = 0
        self.cache = {}
        self.rnd = random.Random(seed)

    def uid(self, p="e"):
        self.n += 1
        return "%s%d" % (p, self.n)

    def add(self, s):
        self.defs.append(s)

    # gradients -------------------------------------------------------
    def lg(self, stops, x1=0, y1=0, x2=0, y2=1, units=None, key=None):
        k = ("lg", tuple(map(tuple, stops)), x1, y1, x2, y2, units)
        if k in self.cache:
            return self.cache[k]
        i = self.uid("lg")
        u = ' gradientUnits="userSpaceOnUse"' if units else ""
        st = "".join('<stop offset="%s" stop-color="%s"%s/>' % (s[0], s[1], (' stop-opacity="%s"' % s[2]) if len(s) > 2 else "") for s in stops)
        self.add('<linearGradient id="%s" x1="%s" y1="%s" x2="%s" y2="%s"%s>%s</linearGradient>' % (i, x1, y1, x2, y2, u, st))
        self.cache[k] = "url(#%s)" % i
        return self.cache[k]

    def rg(self, stops, cx=0.5, cy=0.5, r=0.5, fx=None, fy=None, units=None):
        k = ("rg", tuple(map(tuple, stops)), cx, cy, r, fx, fy, units)
        if k in self.cache:
            return self.cache[k]
        i = self.uid("rg")
        u = ' gradientUnits="userSpaceOnUse"' if units else ""
        f = (' fx="%s" fy="%s"' % (fx, fy)) if fx is not None else ""
        st = "".join('<stop offset="%s" stop-color="%s"%s/>' % (s[0], s[1], (' stop-opacity="%s"' % s[2]) if len(s) > 2 else "") for s in stops)
        self.add('<radialGradient id="%s" cx="%s" cy="%s" r="%s"%s%s>%s</radialGradient>' % (i, cx, cy, r, f, u, st))
        self.cache[k] = "url(#%s)" % i
        return self.cache[k]

    # filters ---------------------------------------------------------
    def shadow(self, blur=10, dy=6, op=0.3, color="#000000", dx=0):
        k = ("sh", blur, dy, op, color, dx)
        if k in self.cache:
            return self.cache[k]
        i = self.uid("sh")
        self.add('<filter id="%s" x="-30%%" y="-30%%" width="160%%" height="160%%"><feDropShadow dx="%s" dy="%s" stdDeviation="%s" flood-color="%s" flood-opacity="%s"/></filter>' % (i, dx, dy, blur, color, op))
        self.cache[k] = "url(#%s)" % i
        return self.cache[k]

    def blur(self, sd=8):
        k = ("bl", sd)
        if k in self.cache:
            return self.cache[k]
        i = self.uid("bl")
        self.add('<filter id="%s" x="-50%%" y="-50%%" width="200%%" height="200%%"><feGaussianBlur stdDeviation="%s"/></filter>' % (i, sd))
        self.cache[k] = "url(#%s)" % i
        return self.cache[k]

    def glow(self, sd=6):
        k = ("gl", sd)
        if k in self.cache:
            return self.cache[k]
        i = self.uid("gl")
        self.add('<filter id="%s" x="-80%%" y="-80%%" width="260%%" height="260%%"><feGaussianBlur stdDeviation="%s" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>' % (i, sd))
        self.cache[k] = "url(#%s)" % i
        return self.cache[k]

    def noise(self, op=0.08, freq=0.9, seed=3):
        k = ("nz", op, freq, seed)
        if k in self.cache:
            return self.cache[k]
        i = self.uid("nz")
        self.add('<filter id="%s" x="0" y="0" width="100%%" height="100%%"><feTurbulence type="fractalNoise" baseFrequency="%s" numOctaves="3" seed="%s" result="t"/>'
                 '<feColorMatrix in="t" type="matrix" values="0 0 0 0 0.35  0 0 0 0 0.25  0 0 0 0 0.15  0 0 0 %s 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>' % (i, freq, seed, op * 6))
        self.cache[k] = "url(#%s)" % i
        return self.cache[k]

    def pattern(self, w, h, body, transform=None):
        i = self.uid("pt")
        t = (' patternTransform="%s"' % transform) if transform else ""
        self.add('<pattern id="%s" width="%s" height="%s" patternUnits="userSpaceOnUse"%s>%s</pattern>' % (i, w, h, t, body))
        return "url(#%s)" % i

    def clip(self, body):
        i = self.uid("cp")
        self.add('<clipPath id="%s">%s</clipPath>' % (i, body))
        return "url(#%s)" % i

    def mask(self, body):
        i = self.uid("mk")
        self.add('<mask id="%s" maskUnits="userSpaceOnUse" x="0" y="0" width="1080" height="1350">%s</mask>' % (i, body))
        return "url(#%s)" % i

    def svg(self, body):
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">'
                '<defs>%s</defs>%s</svg>' % ("".join(self.defs), body))


# ---------------------------------------------------------------- basics
def g(body, tr=None, **kw):
    at = "".join(' %s="%s"' % (k.replace("_", "-"), v) for k, v in kw.items() if v is not None)
    t = (' transform="%s"' % tr) if tr else ""
    return "<g%s%s>%s</g>" % (t, at, body)


def P(d, fill="none", **kw):
    at = "".join(' %s="%s"' % (k.replace("_", "-"), v) for k, v in kw.items() if v is not None)
    return '<path d="%s" fill="%s"%s/>' % (d, fill, at)


def C(x, y, r, fill, **kw):
    at = "".join(' %s="%s"' % (k.replace("_", "-"), v) for k, v in kw.items() if v is not None)
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"%s/>' % (x, y, r, fill, at)


def E(x, y, rx, ry, fill, **kw):
    at = "".join(' %s="%s"' % (k.replace("_", "-"), v) for k, v in kw.items() if v is not None)
    return '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s"%s/>' % (x, y, rx, ry, fill, at)


def R(x, y, w, h, fill, rx=0, **kw):
    at = "".join(' %s="%s"' % (k.replace("_", "-"), v) for k, v in kw.items() if v is not None)
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s"%s/>' % (x, y, w, h, rx, fill, at)


def poly(pts):
    return "M" + " L".join("%.1f,%.1f" % p for p in pts) + "Z"


def star_pts(x, y, r, r2=None, n=5, rot=-90):
    r2 = r2 if r2 is not None else r * 0.45
    pts = []
    for i in range(n * 2):
        rr = r if i % 2 == 0 else r2
        an = math.radians(rot + i * 180.0 / n)
        pts.append((x + rr * math.cos(an), y + rr * math.sin(an)))
    return poly(pts)


def star(x, y, r, fill, r2=None, n=5, rot=-90, **kw):
    return P(star_pts(x, y, r, r2, n, rot), fill, **kw)


def sparkle(x, y, r, fill="#FFFFFF", **kw):
    """4 point twinkle."""
    k = r * 0.18
    d = "M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1fZ" % (
        x, y - r, x + k, y - k, x + r, y, x + k, y + k, x, y + r, x - k, y + k, x - r, y, x - k, y - k, x, y - r)
    return P(d, fill, **kw)


def heart_path(x, y, s):
    """heart centred on x, top notch at y, size s (width ~ 2s)."""
    return ("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (
        x, y + s * 0.3,
        x - s * 0.1, y - s * 0.3, x - s, y - s * 0.3, x - s, y + s * 0.35,
        x - s, y + s * 0.85, x - s * 0.3, y + s * 1.2, x, y + s * 1.55,
        x + s * 0.3, y + s * 1.2, x + s, y + s * 0.85, x + s, y + s * 0.35,
        x + s, y - s * 0.3, x + s * 0.1, y - s * 0.3, x, y + s * 0.3))


def inside(x, y, rects, pad=0):
    for r in rects:
        if r[0] - pad <= x <= r[2] + pad and r[1] - pad <= y <= r[3] + pad:
            return True
    return False


WM = (330, 1262, 750, 1350)  # watermark strip (with margin)


# ---------------------------------------------------------------- scatter
def confetti(a, n, box, colors, avoid=(), seed=None, size=(8, 20), kinds="rcsqt", op=1.0):
    rnd = random.Random(seed if seed is not None else a.rnd.random())
    out = []
    tries = 0
    while len(out) < n and tries < n * 30:
        tries += 1
        x = rnd.uniform(box[0], box[2]); y = rnd.uniform(box[1], box[3])
        if inside(x, y, list(avoid) + [WM], 12):
            continue
        s = rnd.uniform(*size); c = rnd.choice(colors); k = rnd.choice(kinds); ang = rnd.uniform(0, 180)
        if k == "r":
            out.append(R(x - s / 2, y - s / 4, s, s / 2, c, 1.5, transform="rotate(%.0f %.1f %.1f)" % (ang, x, y), opacity=op))
        elif k == "c":
            out.append(C(x, y, s / 3.2, c, opacity=op))
        elif k == "s":  # streamer curl
            d = "M%.1f,%.1f q%.1f,%.1f %.1f,0 t%.1f,0" % (x - s, y, s / 2, -s * 0.8, s, s)
            out.append(P(d, "none", stroke=c, stroke_width="%.1f" % (s / 4.5), stroke_linecap="round", transform="rotate(%.0f %.1f %.1f)" % (ang, x, y), opacity=op))
        elif k == "q":
            out.append(R(x - s / 3, y - s / 3, s / 1.5, s / 1.5, c, 1, transform="rotate(%.0f %.1f %.1f)" % (ang, x, y), opacity=op))
        else:
            out.append(star(x, y, s / 2, c, rot=ang, opacity=op))
    return "".join(out)


def bokeh(a, n, box, colors, rr=(10, 60), op=(0.08, 0.3), avoid=(), seed=None, blur=None):
    rnd = random.Random(seed if seed is not None else a.rnd.random())
    out = []
    t = 0
    while len(out) < n and t < n * 20:
        t += 1
        x = rnd.uniform(box[0], box[2]); y = rnd.uniform(box[1], box[3])
        if inside(x, y, avoid, 20):
            continue
        r = rnd.uniform(*rr)
        c = rnd.choice(colors)
        out.append(C(x, y, r, a.rg([(0, c, 0.9), (0.7, c, 0.55), (1, c, 0)]), opacity="%.2f" % rnd.uniform(*op)))
    body = "".join(out)
    return g(body, filter=a.blur(blur)) if blur else body


def twinkles(a, n, box, color="#FFFFFF", rr=(4, 14), avoid=(), seed=None, op=(0.5, 1)):
    rnd = random.Random(seed if seed is not None else a.rnd.random())
    out = []
    t = 0
    while len(out) < n and t < n * 20:
        t += 1
        x = rnd.uniform(box[0], box[2]); y = rnd.uniform(box[1], box[3])
        if inside(x, y, list(avoid) + [WM], 10):
            continue
        r = rnd.uniform(*rr)
        if rnd.random() < 0.55:
            out.append(sparkle(x, y, r, color, opacity="%.2f" % rnd.uniform(*op)))
        else:
            out.append(C(x, y, r / 4, color, opacity="%.2f" % rnd.uniform(*op)))
    return "".join(out)


def dots_pattern(a, color, sp=40, r=3, op=0.25, offset=True):
    body = C(sp / 4, sp / 4, r, color, opacity=op)
    if offset:
        body += C(sp * 3 / 4, sp * 3 / 4, r, color, opacity=op)
    return a.pattern(sp, sp, body)


# ---------------------------------------------------------------- panels
def panel(a, x, y, w, h, fill, rx=36, stroke=None, sw=3, inner=None, shadow=True, op=1, dash=None):
    s = ""
    f = a.shadow(22, 12, 0.22) if shadow else None
    s += R(x, y, w, h, fill, rx, filter=f, opacity=op)
    if stroke:
        s += R(x + 14, y + 14, w - 28, h - 28, "none", max(rx - 12, 0), stroke=stroke, stroke_width=sw, stroke_dasharray=dash)
    if inner:
        s += R(x + 24, y + 24, w - 48, h - 48, "none", max(rx - 20, 0), stroke=inner, stroke_width=1.5)
    return s


# ---------------------------------------------------------------- birthday things
def balloon(a, x, y, r, col, tail=None, rot=0, shine=True, knot=True, sw=2.2, strc="#9A8C98", op=1):
    """Latex balloon, centre x,y radius r.  tail=(tx,ty) end of string."""
    ry = r * 1.15
    d = "M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (
        x, y - ry, x + r * 1.38, y - ry, x + r * 0.95, y + ry * 0.78, x, y + ry,
        x - r * 0.95, y + ry * 0.78, x - r * 1.38, y - ry, x, y - ry)
    fill = a.rg([(0, lt(col, 0.55)), (0.35, lt(col, 0.12)), (0.8, col), (1, dk(col, 0.28))], 0.38, 0.32, 0.75, 0.32, 0.25)
    s = ""
    if tail:
        tx, ty = tail
        mx = (x + tx) / 2 + (r * 0.4 if tx < x else -r * 0.4)
        s += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f T%.1f,%.1f" % (x, y + ry + 10, x + (mx - x) * 0.3 + 14, y + ry + (ty - y) * 0.25, mx, (y + ry + ty) / 2, tx, ty),
               stroke=strc, stroke_width=sw, fill="none")
    b = P(d, fill)
    if knot:
        b += P("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1fZ" % (x - r * 0.1, y + ry + 12, x, y + ry - 3, x + r * 0.1, y + ry + 12), dk(col, 0.2))
    if shine:
        b += E(x - r * 0.38, y - ry * 0.42, r * 0.18, r * 0.34, "#FFFFFF", opacity=0.55, transform="rotate(28 %.1f %.1f)" % (x - r * 0.38, y - ry * 0.42))
        b += C(x - r * 0.12, y - ry * 0.72, r * 0.06, "#FFFFFF", opacity=0.7)
        b += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (x + r * 0.55, y + ry * 0.1, x + r * 0.5, y + ry * 0.5, x + r * 0.2, y + ry * 0.72), stroke="#FFFFFF", stroke_width=r * 0.05, stroke_linecap="round", opacity=0.28)
    tr = "rotate(%s %.1f %.1f)" % (rot, x, y + ry) if rot else None
    return s + g(b, tr, opacity=op if op != 1 else None)


def foil_star_balloon(a, x, y, r, col, tail=None, rot=0):
    s = ""
    if tail:
        s += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (x, y + r * 0.8, x - 20, (y + tail[1]) / 2, tail[0], tail[1]), stroke="#B0A6B8", stroke_width=2)
    fill = a.lg([(0, lt(col, 0.6)), (0.35, col), (0.55, lt(col, 0.35)), (0.8, dk(col, 0.2)), (1, lt(col, 0.2))], 0, 0, 1, 1)
    body = star(x, y, r, fill, r2=r * 0.55, rot=-90 + rot)
    body += star(x, y, r * 0.78, "none", r2=r * 0.43, rot=-90 + rot, stroke="#FFFFFF", stroke_width=2, opacity=0.35)
    body += E(x - r * 0.25, y - r * 0.3, r * 0.1, r * 0.3, "#FFFFFF", opacity=0.6, transform="rotate(35 %.1f %.1f)" % (x - r * 0.25, y - r * 0.3))
    return s + body


def candle(a, x, ybot, h, w, col, stripe="#FFFFFF", flame=True, glow=True):
    s = ""
    body = R(x - w / 2, ybot - h, w, h, a.lg([(0, dk(col, 0.15)), (0.35, lt(col, 0.35)), (1, dk(col, 0.25))], 0, 0, 1, 0), w * 0.2)
    # spiral stripes
    cp = a.clip(R(x - w / 2, ybot - h, w, h, "#000", w * 0.2))
    st = ""
    k = ybot - h - w
    while k < ybot + w:
        st += P("M%.1f,%.1f L%.1f,%.1f" % (x - w / 2, k + w * 0.9, x + w / 2, k), stroke=stripe, stroke_width=w * 0.28, opacity=0.9)
        k += w * 1.1
    s += body + g(st, clip_path=cp)
    s += R(x - w / 2 + 2, ybot - h, w * 0.18, h, "#FFFFFF", w * 0.1, opacity=0.35)
    # wick
    s += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (x, ybot - h, x + 2, ybot - h - 8, x, ybot - h - 14), stroke="#3A2A20", stroke_width=2.5, stroke_linecap="round")
    if flame:
        fy = ybot - h - 14
        fh = max(28, w * 2.2)
        if glow:
            s += C(x, fy - fh * 0.45, fh * 1.25, a.rg([(0, "#FFE9A8", 0.75), (0.4, "#FFC85A", 0.3), (1, "#FFB030", 0)]))
        fl = "M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (
            x, fy - fh, x + fh * 0.45, fy - fh * 0.45, x + fh * 0.32, fy + 2, x, fy + 2, x - fh * 0.32, fy + 2, x - fh * 0.45, fy - fh * 0.45, x, fy - fh)
        s += P(fl, a.rg([(0, "#FFFFFF"), (0.3, "#FFF3B0"), (0.7, "#FFB23A"), (1, "#FF7A1A")], 0.5, 0.75, 0.7))
        s += E(x, fy - fh * 0.25, fh * 0.1, fh * 0.2, "#6FB7FF", opacity=0.5)
    return s


def gift(a, x, y, w, h, box, rib, pat=None, lid=None, bow=True, depth=0.28, bowscale=1.0):
    """Gift box in slight 3/4 view.  x,y = top-left of front face (below lid)."""
    s = ""
    dpt = w * depth
    lid = lid or box
    # side face
    s += P(poly([(x + w, y), (x + w + dpt, y - dpt * 0.55), (x + w + dpt, y + h - dpt * 0.55), (x + w, y + h)]), dk(box, 0.28))
    # front face
    s += R(x, y, w, h, a.lg([(0, lt(box, 0.08)), (1, dk(box, 0.1))]))
    if pat:
        s += R(x, y, w, h, pat)
    s += R(x, y, w, h * 0.12, "#000", opacity=0.12)
    # ribbon vertical front + side band
    rw = w * 0.16
    s += R(x + w / 2 - rw / 2, y, rw, h, a.lg([(0, dk(rib, 0.12)), (0.5, lt(rib, 0.25)), (1, dk(rib, 0.12))], 0, 0, 1, 0))
    s += P(poly([(x + w, y + h * 0.42), (x + w + dpt, y + h * 0.42 - dpt * 0.55), (x + w + dpt, y + h * 0.42 - dpt * 0.55 + rw * 0.8), (x + w, y + h * 0.42 + rw * 0.8)]), dk(rib, 0.25))
    # lid
    lh = h * 0.2
    lx, ly, lw = x - w * 0.05, y - lh, w * 1.1
    s += P(poly([(lx + lw, ly), (lx + lw + dpt, ly - dpt * 0.55), (lx + lw + dpt, ly + lh - dpt * 0.55), (lx + lw, ly + lh)]), dk(lid, 0.3))
    s += P(poly([(lx, ly), (lx + dpt, ly - dpt * 0.55), (lx + lw + dpt, ly - dpt * 0.55), (lx + lw, ly)]), lt(lid, 0.2))
    s += R(lx, ly, lw, lh, a.lg([(0, lt(lid, 0.12)), (1, dk(lid, 0.08))]))
    if pat:
        s += R(lx, ly, lw, lh, pat)
    s += R(lx + lw / 2 - rw / 2, ly, rw, lh, lt(rib, 0.1))
    s += P(poly([(lx + lw / 2 - rw / 2, ly), (lx + lw / 2 - rw / 2 + dpt, ly - dpt * 0.55), (lx + lw / 2 + rw / 2 + dpt, ly - dpt * 0.55), (lx + lw / 2 + rw / 2, ly)]), lt(rib, 0.3))
    s += R(lx, ly + lh - 4, lw, 6, "#000", opacity=0.15)
    if bow:
        bx, by = lx + lw / 2 + dpt / 2, ly - dpt * 0.28
        s += bow_shape(a, bx, by, w * 0.34 * bowscale, rib)
    return g(s, filter=a.shadow(12, 10, 0.25))


def bow_shape(a, x, y, s, col):
    fill = a.lg([(0, lt(col, 0.3)), (0.6, col), (1, dk(col, 0.25))], 0, 0, 1, 1)
    o = ""
    # tails
    o += P("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1fZ" % (x - 4, y + 4, x - s * 0.5, y + s * 0.9, x - s * 0.3, y + s * 0.8, x - s * 0.22, y + s * 1.0), dk(col, 0.15))
    o += P("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1fZ" % (x + 4, y + 4, x + s * 0.5, y + s * 0.9, x + s * 0.3, y + s * 0.8, x + s * 0.22, y + s * 1.0), dk(col, 0.15))
    # loops
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (x, y, x - s * 0.4, y - s * 0.9, x - s * 1.25, y - s * 0.45, x - s * 0.95, y + s * 0.1, x - s * 0.7, y + s * 0.45, x - s * 0.2, y + s * 0.15, x, y), fill)
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (x, y, x + s * 0.4, y - s * 0.9, x + s * 1.25, y - s * 0.45, x + s * 0.95, y + s * 0.1, x + s * 0.7, y + s * 0.45, x + s * 0.2, y + s * 0.15, x, y), fill)
    o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (x - s * 0.15, y - s * 0.05, x - s * 0.55, y - s * 0.45, x - s * 0.85, y - s * 0.05), stroke=dk(col, 0.3), stroke_width=2, opacity=0.5)
    o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (x + s * 0.15, y - s * 0.05, x + s * 0.55, y - s * 0.45, x + s * 0.85, y - s * 0.05), stroke=dk(col, 0.3), stroke_width=2, opacity=0.5)
    o += E(x, y, s * 0.2, s * 0.17, a.lg([(0, lt(col, 0.3)), (1, dk(col, 0.2))]))
    return o


def sprinkles(a, n, box, colors, seed=1, clip=None, ln=10, wd=3.5):
    rnd = random.Random(seed)
    out = ""
    for _ in range(n):
        x = rnd.uniform(box[0], box[2]); y = rnd.uniform(box[1], box[3]); an = rnd.uniform(0, 180)
        out += R(x - ln / 2, y - wd / 2, ln, wd, rnd.choice(colors), wd / 2, transform="rotate(%.0f %.1f %.1f)" % (an, x, y))
    return g(out, clip_path=clip) if clip else out


def drip_path(x0, x1, y, rnd, depth=(18, 60), step=(26, 46), top=None):
    """closed path of frosting drips along the top edge from x0..x1 at y (drips go down)."""
    top = y - 30 if top is None else top
    d = "M%.1f,%.1f L%.1f,%.1f" % (x0, top, x0, y)
    x = x0
    while x < x1:
        st = rnd.uniform(*step)
        dp = rnd.uniform(*depth)
        xm = min(x + st, x1)
        w = (xm - x)
        # drip: down and round up
        d += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (x + w * 0.1, y, x + w * 0.08, y + dp, x + w * 0.5, y + dp)
        d += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (x + w * 0.92, y + dp, x + w * 0.9, y, xm, y)
        x = xm
    d += " L%.1f,%.1fZ" % (x1, top)
    return d


def cake_tier(a, cx, ybot, w, h, col, icing, seed=1, deco="pearls", deco_col="#FFFFFF", sprink=None):
    """Cylindrical tier; ybot is bottom edge centre."""
    rnd = random.Random(seed)
    ey = w * 0.12  # ellipse half-height
    x0, x1 = cx - w / 2, cx + w / 2
    top = ybot - h
    s = ""
    side = a.lg([(0, dk(col, 0.22)), (0.25, lt(col, 0.12)), (0.45, lt(col, 0.2)), (0.8, col), (1, dk(col, 0.3))], 0, 0, 1, 0)
    body = "M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f L%.1f,%.1fZ" % (x0, top, x0, ybot, w / 2, ey, x1, ybot, x1, top)
    s += P(body, side)
    # icing drip
    dp = drip_path(x0, x1, top + ey * 0.6, rnd, depth=(h * 0.12, h * 0.42), top=top)
    ic = a.lg([(0, dk(icing, 0.12)), (0.3, lt(icing, 0.25)), (0.5, lt(icing, 0.35)), (1, dk(icing, 0.18))], 0, 0, 1, 0)
    s += P(dp, ic)
    s += E(cx, top, w / 2, ey, a.lg([(0, lt(icing, 0.3)), (1, icing)]))
    s += E(cx - w * 0.12, top - ey * 0.15, w * 0.28, ey * 0.4, "#FFFFFF", opacity=0.25)
    if sprink:
        cp = a.clip(E(cx, top, w / 2 - 6, ey - 3, "#000"))
        s += sprinkles(a, int(w / 6), (x0, top - ey, x1, top + ey), sprink, seed=seed + 5, clip=cp, ln=9, wd=3)
    # decorations
    if deco == "pearls":
        n = int(w / 22)
        for i in range(n + 1):
            t = i / n
            an = math.pi * t
            px = cx - math.cos(an) * w / 2 * 0.98
            py = ybot + math.sin(an) * ey * 0.98 - 9
            s += C(px, py, 8.5, a.rg([(0, "#FFFFFF"), (0.6, deco_col), (1, dk(deco_col, 0.25))], 0.35, 0.3, 0.7))
    elif deco == "stripes":
        for i in range(1, 9):
            t = i / 9.0
            an = math.pi * t
            px = cx - math.cos(an) * w / 2
            s += P("M%.1f,%.1f L%.1f,%.1f" % (px, top + h * 0.45, px, ybot + math.sin(an) * ey - 4), stroke=deco_col, stroke_width=w * 0.022 * math.sin(an) + 1, opacity=0.8, stroke_linecap="round")
    elif deco == "dots":
        for row in (0.55, 0.8):
            for i in range(1, 10):
                t = i / 10.0
                an = math.pi * t
                px = cx - math.cos(an) * w / 2
                py = top + h * row + math.sin(an) * ey * 0.9
                s += E(px, py, 6 * math.sin(an) + 1.5, 6, deco_col, opacity=0.95)
    elif deco == "scallop":
        n = 12
        for i in range(n):
            t0, t1 = i / n, (i + 1) / n
            a0, a1 = math.pi * t0, math.pi * t1
            p0 = (cx - math.cos(a0) * w / 2, ybot - h * 0.3 + math.sin(a0) * ey)
            p1 = (cx - math.cos(a1) * w / 2, ybot - h * 0.3 + math.sin(a1) * ey)
            s += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (p0[0], p0[1], (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + 16, p1[0], p1[1]), stroke=deco_col, stroke_width=4, stroke_linecap="round")
            s += C(p1[0], p1[1], 4.5, deco_col)
    elif deco == "rosettes":
        n = 8
        for i in range(n):
            t = (i + 0.5) / n
            an = math.pi * t
            px = cx - math.cos(an) * w / 2 * 0.95
            py = ybot + math.sin(an) * ey - 14
            s += rosette(a, px, py, 13 + 3 * math.sin(an), deco_col)
    return s


def rosette(a, x, y, r, col):
    s = C(x, y, r, a.rg([(0, lt(col, 0.4)), (1, dk(col, 0.15))], 0.4, 0.35, 0.7))
    s += P("M%.1f,%.1f A%.1f,%.1f 0 1 1 %.1f,%.1f" % (x - r * 0.55, y, r * 0.55, r * 0.55, x + r * 0.2, y - r * 0.3), stroke=dk(col, 0.2), stroke_width=1.6, opacity=0.6)
    s += P("M%.1f,%.1f A%.1f,%.1f 0 1 0 %.1f,%.1f" % (x + r * 0.5, y + r * 0.1, r * 0.35, r * 0.35, x - r * 0.1, y + r * 0.15), stroke=dk(col, 0.2), stroke_width=1.4, opacity=0.5)
    return s


def cake_stand(a, cx, y, w, col="#E9E4EF", metal=False):
    """plate top at y."""
    if metal:
        f = a.lg([(0, "#B8862E"), (0.3, "#FFE7A6"), (0.55, "#D9A441"), (0.8, "#FFF1C4"), (1, "#A8741F")], 0, 0, 1, 0)
    else:
        f = a.lg([(0, dk(col, 0.18)), (0.35, lt(col, 0.5)), (1, dk(col, 0.2))], 0, 0, 1, 0)
    s = E(cx, y + 10, w / 2, w * 0.07, dk(col, 0.25) if not metal else "#8C5E14")
    s += E(cx, y, w / 2, w * 0.07, f)
    s += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f L%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (
        cx - w * 0.07, y + 14, cx - w * 0.05, y + 60, cx - w * 0.2, y + 80, cx - w * 0.22, y + 100,
        cx + w * 0.22, y + 100, cx + w * 0.2, y + 80, cx + w * 0.05, y + 60, cx + w * 0.07, y + 14), f)
    s += E(cx, y + 100, w * 0.22, w * 0.03, dk(col, 0.2) if not metal else "#9A6A18")
    return s


def cupcake(a, cx, ybot, s, wrap, frost, cherry=True, sprink=None, seed=1, candle_col=None):
    """cupcake with base width ~ s."""
    o = ""
    top_w, bot_w, wh = s * 1.1, s * 0.82, s * 0.62
    wy = ybot - wh
    wr = poly([(cx - top_w / 2, wy), (cx + top_w / 2, wy), (cx + bot_w / 2, ybot), (cx - bot_w / 2, ybot)])
    o += P(wr, a.lg([(0, dk(wrap, 0.25)), (0.4, lt(wrap, 0.2)), (1, dk(wrap, 0.3))], 0, 0, 1, 0))
    n = 9
    for i in range(1, n):
        t = i / n
        o += P("M%.1f,%.1f L%.1f,%.1f" % (cx - top_w / 2 + top_w * t, wy + 3, cx - bot_w / 2 + bot_w * t, ybot - 2), stroke=dk(wrap, 0.3), stroke_width=2, opacity=0.5)
    o += P("M%.1f,%.1f L%.1f,%.1f" % (cx - top_w / 2, wy + 6, cx + top_w / 2, wy + 6), stroke=lt(wrap, 0.5), stroke_width=3, opacity=0.6)
    # frosting swirl: 3 tiers
    ff = a.lg([(0, lt(frost, 0.45)), (0.5, frost), (1, dk(frost, 0.18))], 0, 0, 0.3, 1)
    lays = [(s * 0.66, wy + 2, s * 0.26), (s * 0.52, wy - s * 0.2, s * 0.24), (s * 0.34, wy - s * 0.4, s * 0.2)]
    for rw, yy, rh in lays:
        o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (
            cx - rw, yy, cx - rw * 1.12, yy - rh * 1.1, cx - rw * 0.3, yy - rh * 1.25, cx, yy - rh * 1.05,
            cx + rw * 0.35, yy - rh * 1.3, cx + rw * 1.15, yy - rh * 1.0, cx + rw, yy, cx + rw * 0.5, yy + rh * 0.3, cx - rw * 0.5, yy + rh * 0.3, cx - rw, yy), ff)
        o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (cx - rw * 0.7, yy - rh * 0.55, cx - rw * 0.2, yy - rh * 1.0, cx + rw * 0.3, yy - rh * 0.8), stroke="#FFFFFF", stroke_width=s * 0.035, stroke_linecap="round", opacity=0.45)
    tipy = wy - s * 0.66
    o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1fZ" % (cx - s * 0.14, tipy + s * 0.08, cx - s * 0.05, tipy - s * 0.1, cx + s * 0.02, tipy - s * 0.12, cx + s * 0.02, tipy - s * 0.02, cx + s * 0.14, tipy + s * 0.08), ff)
    if sprink:
        o += sprinkles(a, 22, (cx - s * 0.55, wy - s * 0.6, cx + s * 0.55, wy - s * 0.02), sprink, seed=seed, ln=s * 0.07, wd=s * 0.025)
    if candle_col:
        o += candle(a, cx, tipy + 4, s * 0.45, s * 0.1, candle_col)
    elif cherry:
        o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (cx + 2, tipy - s * 0.1, cx + s * 0.05, tipy - s * 0.28, cx + s * 0.16, tipy - s * 0.34), stroke="#4E7A2C", stroke_width=s * 0.025, stroke_linecap="round")
        o += C(cx, tipy - s * 0.05, s * 0.1, a.rg([(0, "#FF8A8A"), (0.5, "#D81E3A"), (1, "#7A0A1C")], 0.35, 0.3, 0.7))
        o += C(cx - s * 0.035, tipy - s * 0.09, s * 0.025, "#FFFFFF", opacity=0.8)
    return g(o, filter=a.shadow(8, 6, 0.2))


def sparkler(a, x0, y0, x1, y1, r=90, seed=1, col="#FFD36B"):
    """stick from x0,y0 (handle) to x1,y1 (burning tip) with burst radius r."""
    rnd = random.Random(seed)
    o = P("M%.1f,%.1f L%.1f,%.1f" % (x0, y0, x1, y1), stroke="#6B6B73", stroke_width=5, stroke_linecap="round")
    o += P("M%.1f,%.1f L%.1f,%.1f" % (x0 + (x1 - x0) * 0.55, y0 + (y1 - y0) * 0.55, x1, y1), stroke="#3A3036", stroke_width=9, stroke_linecap="round")
    o += C(x1, y1, r * 0.9, a.rg([(0, "#FFF6D0", 0.9), (0.25, col, 0.5), (1, col, 0)]))
    rays = ""
    for i in range(60):
        an = rnd.uniform(0, math.pi * 2); ln = rnd.uniform(0.3, 1.0) * r
        sx, sy = x1 + math.cos(an) * ln * 0.15, y1 + math.sin(an) * ln * 0.15
        ex, ey = x1 + math.cos(an) * ln, y1 + math.sin(an) * ln
        rays += P("M%.1f,%.1f L%.1f,%.1f" % (sx, sy, ex, ey), stroke=rnd.choice(["#FFFFFF", "#FFF1B8", col]), stroke_width="%.1f" % rnd.uniform(1, 2.6), stroke_linecap="round", opacity="%.2f" % rnd.uniform(0.5, 1))
        if rnd.random() < 0.35:
            rays += sparkle(ex, ey, rnd.uniform(4, 9), "#FFFFFF")
    o += g(rays, filter=a.glow(2.5))
    o += C(x1, y1, 7, "#FFFFFF")
    return o


def ribbon_curl(x, y, ln, col, sw=3, seed=1, turns=3):
    rnd = random.Random(seed)
    d = "M%.1f,%.1f" % (x, y)
    for i in range(turns):
        d += " q%.1f,%.1f %.1f,%.1f" % (rnd.uniform(-1, 1) * ln * 0.4, ln * 0.3, rnd.uniform(-0.2, 0.2) * ln, ln * 0.5)
    return P(d, stroke=col, stroke_width=sw, stroke_linecap="round")


# ---------------------------------------------------------------- party (invites)
def bunting(a, x0, y0, x1, y1, sag, colors, n, fw=None, fh=None, seed=1, pat=True, string="#6D5A4B", shape="tri"):
    """flag line along quadratic curve."""
    rnd = random.Random(seed)
    cxp, cyp = (x0 + x1) / 2, (y0 + y1) / 2 + sag * 2
    def pt(t):
        return ((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cxp + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cyp + t * t * y1)
    L = math.hypot(x1 - x0, y1 - y0)
    fw = fw or L / n * 0.82
    fh = fh or fw * 1.15
    o = P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (x0, y0, cxp, cyp, x1, y1), stroke=string, stroke_width=3)
    for i in range(n):
        t = (i + 0.5) / n
        px, py = pt(t)
        ta, tb = pt(max(0, t - 0.01)), pt(min(1, t + 0.01))
        an = math.degrees(math.atan2(tb[1] - ta[1], tb[0] - ta[0]))
        c = colors[i % len(colors)]
        if shape == "tri":
            fl = poly([(-fw / 2, 0), (fw / 2, 0), (0, fh)])
        else:  # pennant with swallow tail
            fl = poly([(-fw / 2, 0), (fw / 2, 0), (fw / 2, fh), (0, fh * 0.75), (-fw / 2, fh)])
        f = P(fl, a.lg([(0, lt(c, 0.15)), (1, dk(c, 0.12))]))
        if pat and i % 3 == 1:
            f += P(fl, dots_pattern(a, "#FFFFFF", 14, 2.2, 0.7))
        elif pat and i % 3 == 2:
            f += P(fl, a.pattern(12, 12, R(0, 0, 6, 12, "#FFFFFF", opacity=0.35), "rotate(45)"))
        f += P("M%.1f,%.1f L%.1f,%.1f" % (-fw / 2 + 4, 5, fw / 2 - 4, 5), stroke="#FFFFFF", stroke_width=1.5, stroke_dasharray="4 4", opacity=0.7)
        f += P("M0,0 L%.1f,%.1f L%.1f,%.1fZ" % (fw / 2, 0, 0, fh) if shape == "tri" else "M0,0", "#000", opacity=0.08)
        o += g(f, "translate(%.1f %.1f) rotate(%.1f)" % (px, py, an), filter=a.shadow(3, 3, 0.18))
    return o


def party_popper(a, x, y, ang, s, cols, seed=1, burst=True, cone=("#FFB400", "#7A3DD6")):
    """cone tip at x,y pointing away from opening; ang = direction of opening (deg)."""
    rnd = random.Random(seed)
    L, Wd = s, s * 0.42
    cone_p = poly([(0, 0), (L, -Wd / 2), (L, Wd / 2)])
    st = ""
    for i in range(5):
        t0 = 0.15 + i * 0.18
        st += P(poly([(L * t0, -Wd / 2 * t0), (L * (t0 + 0.09), -Wd / 2 * (t0 + 0.09)), (L * (t0 + 0.09), Wd / 2 * (t0 + 0.09)), (L * t0, Wd / 2 * t0)]), cone[1], opacity=0.95)
    body = P(cone_p, a.lg([(0, lt(cone[0], 0.3)), (0.5, cone[0]), (1, dk(cone[0], 0.25))], 0, 0, 0, 1)) + st
    body += E(L, 0, Wd * 0.14, Wd / 2, dk(cone[0], 0.4))
    body += P("M%.1f,%.1f L%.1f,%.1f" % (L * 0.1, -Wd * 0.03, L * 0.95, -Wd * 0.4), stroke="#FFFFFF", stroke_width=3, opacity=0.4)
    o = g(body, "translate(%.1f %.1f) rotate(%.1f)" % (x, y, ang), filter=a.shadow(8, 6, 0.25))
    if burst:
        ox, oy = x + math.cos(math.radians(ang)) * L, y + math.sin(math.radians(ang)) * L
        bs = ""
        for i in range(14):
            da = math.radians(ang + rnd.uniform(-40, 40)); ln = rnd.uniform(0.6, 1.5) * s
            ex, ey = ox + math.cos(da) * ln, oy + math.sin(da) * ln
            mx, my = ox + math.cos(da) * ln * 0.5 + rnd.uniform(-40, 40), oy + math.sin(da) * ln * 0.5 + rnd.uniform(-40, 40)
            bs += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (ox, oy, mx, my, ex, ey), stroke=rnd.choice(cols), stroke_width="%.1f" % rnd.uniform(3, 6), stroke_linecap="round")
        for i in range(40):
            da = math.radians(ang + rnd.uniform(-50, 50)); ln = rnd.uniform(0.3, 1.8) * s
            ex, ey = ox + math.cos(da) * ln, oy + math.sin(da) * ln
            c = rnd.choice(cols); k = rnd.random()
            if k < 0.4:
                bs += R(ex - 6, ey - 3, 12, 6, c, 1, transform="rotate(%d %.1f %.1f)" % (rnd.randint(0, 180), ex, ey))
            elif k < 0.7:
                bs += C(ex, ey, rnd.uniform(3, 6), c)
            else:
                bs += star(ex, ey, rnd.uniform(6, 11), c, rot=rnd.uniform(0, 90))
        o = bs + o
    return o


# ---------------------------------------------------------------- soft / baby
def cloud(a, x, y, s, fill="#FFFFFF", shade=None, op=1):
    """flat-bottom cloud, width ~ 2.6s, base at y."""
    shade = shade or dk(fill, 0.08)
    d = ("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (
        x - s * 1.3, y,
        x - s * 1.55, y, x - s * 1.5, y - s * 0.6, x - s * 0.95, y - s * 0.55,
        x - s * 0.9, y - s * 1.25, x + s * 0.1, y - s * 1.35, x + s * 0.35, y - s * 0.8,
        x + s * 0.7, y - s * 1.05, x + s * 1.35, y - s * 0.75, x + s * 1.2, y - s * 0.3,
        x + s * 1.6, y - s * 0.2, x + s * 1.55, y, x + s * 1.3, y))
    return P(d, a.lg([(0, fill), (0.7, fill), (1, shade)]), opacity=op if op != 1 else None)


def crescent(a, x, y, r, fill, cut=0.62, rot=0):
    """crescent: circle r at x,y, cut by circle offset to upper-right."""
    m = a.mask(R(0, 0, 1080, 1350, "#000") + C(x, y, r, "#FFF") + C(x + r * cut, y - r * cut * 0.55, r * 0.92, "#000"))
    return g(C(x, y, r, fill), "rotate(%s %.1f %.1f)" % (rot, x, y) if rot else None, mask=m)


def footprint(a, x, y, s, fill, ang=0, left=False, stroke=None):
    """baby footprint centred on sole, heel downward before rotation. s ~ foot length."""
    m = -1 if left else 1
    sole = ("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (
        0, s * 0.5,
        m * s * 0.22, s * 0.5, m * s * 0.26, s * 0.25, m * s * 0.22, s * 0.05,
        m * s * 0.2, -s * 0.12, m * s * 0.3, -s * 0.2, m * s * 0.22, -s * 0.3,
        m * s * 0.1, -s * 0.36, -m * s * 0.22, -s * 0.34, -m * s * 0.2, -s * 0.12,
        -m * s * 0.18, s * 0.08, -m * s * 0.22, s * 0.5, 0, s * 0.5))
    o = P(sole, fill, stroke=stroke, stroke_width=2 if stroke else None)
    toes = [(-0.17, -0.47, 0.085), (-0.03, -0.5, 0.068), (0.08, -0.47, 0.058), (0.17, -0.42, 0.05), (0.24, -0.35, 0.043)]
    for tx, ty, tr in toes:
        o += C(m * tx * s, ty * s, tr * s, fill, stroke=stroke, stroke_width=2 if stroke else None)
    return g(o, "translate(%.1f %.1f) rotate(%.1f)" % (x, y, ang))


def peacock_feather(a, x, y, ln, ang, seed=1, scale_w=1.0, eye=True):
    """feather base at x,y; points in direction ang (deg, 0 = up)."""
    rnd = random.Random(seed)
    o = ""
    wmax = ln * 0.2 * scale_w
    # barbs
    barbs = ""
    for i in range(160):
        t = 0.08 + 0.92 * (i / 160.0)
        yy = -ln * t
        wv = wmax * math.sin(math.pi * min(1, t * 1.05)) ** 0.7 * (0.6 + 0.4 * t)
        for side in (-1, 1):
            ex = side * wv * rnd.uniform(0.85, 1.05)
            ey = yy - wv * 0.55 * rnd.uniform(0.6, 1.0)
            col = mix("#2F7D4A", "#B7C43A", rnd.random() * 0.6) if t < 0.7 else mix("#2C8F6A", "#9BC53D", rnd.random())
            barbs += P("M0,%.1f Q%.1f,%.1f %.1f,%.1f" % (yy, ex * 0.5, yy - wv * 0.1, ex, ey), stroke=col, stroke_width="%.1f" % rnd.uniform(0.9, 1.8), opacity="%.2f" % rnd.uniform(0.55, 0.95))
    o += barbs
    o += P("M0,0 Q%.1f,%.1f 0,%.1f" % (wmax * 0.06, -ln * 0.5, -ln * 1.02), stroke="#8A7A3E", stroke_width=3.2, stroke_linecap="round")
    if eye:
        ey0 = -ln * 0.8
        e = ln * 0.12
        o += E(0, ey0, e * 1.35, e * 1.6, a.rg([(0, "#D6B24A"), (1, "#8C9A2E")]), opacity=0.95)
        o += E(0, ey0 + e * 0.1, e * 1.05, e * 1.25, a.rg([(0, "#1B8F8C"), (0.8, "#1F7A74"), (1, "#0E4F55")]))
        o += E(0, ey0 + e * 0.15, e * 0.78, e * 0.92, a.rg([(0, "#D59A3A"), (1, "#A9652A")]))
        o += E(0, ey0 + e * 0.22, e * 0.52, e * 0.62, a.rg([(0, "#2FA0B0"), (1, "#146D8A")]))
        o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (
            0, ey0 - e * 0.25, e * 0.42, ey0 - e * 0.1, e * 0.3, ey0 + e * 0.55, 0, ey0 + e * 0.62,
            -e * 0.3, ey0 + e * 0.55, -e * 0.42, ey0 - e * 0.1, 0, ey0 - e * 0.25), a.rg([(0, "#28306E"), (1, "#0E1440")]))
        o += E(-e * 0.12, ey0 + e * 0.05, e * 0.08, e * 0.16, "#FFFFFF", opacity=0.6)
    return g(o, "translate(%.1f %.1f) rotate(%.1f)" % (x, y, ang))


def flower5(a, x, y, r, col, center="#FFD36B", rot=0, petals=5):
    o = ""
    pf = a.rg([(0, lt(col, 0.5)), (1, col)], 0.5, 0.9, 0.9)
    for i in range(petals):
        an = rot + i * 360.0 / petals
        o += E(x, y - r * 0.55, r * 0.42, r * 0.6, pf, transform="rotate(%.1f %.1f %.1f)" % (an, x, y))
    o += C(x, y, r * 0.26, a.rg([(0, lt(center, 0.4)), (1, dk(center, 0.15))]))
    return o


def leaf(a, x, y, ln, ang, col, vein=True):
    d = "M0,0 C%.1f,%.1f %.1f,%.1f 0,%.1f C%.1f,%.1f %.1f,%.1f 0,0Z" % (ln * 0.38, -ln * 0.25, ln * 0.3, -ln * 0.75, -ln, -ln * 0.3, -ln * 0.75, -ln * 0.38, -ln * 0.25)
    o = P(d, a.lg([(0, dk(col, 0.1)), (1, lt(col, 0.2))], 0, 1, 1, 0))
    if vein:
        o += P("M0,0 L0,%.1f" % (-ln * 0.9), stroke=lt(col, 0.35), stroke_width=1.5, opacity=0.7)
    return g(o, "translate(%.1f %.1f) rotate(%.1f)" % (x, y, ang))


def garland_flowers(a, x0, y0, x1, y1, sag, cols, n, r, seed=1, leafc="#7FB069"):
    """draped flower garland (swag)."""
    rnd = random.Random(seed)
    cxp, cyp = (x0 + x1) / 2, (y0 + y1) / 2 + sag * 2
    o = ""
    for i in range(n + 1):
        t = i / float(n)
        px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cxp + t * t * x1
        py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cyp + t * t * y1
        if i % 2 == 0:
            o += leaf(a, px, py, r * 1.8, rnd.uniform(-160, 160), leafc, vein=False)
    for i in range(n + 1):
        t = i / float(n)
        px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cxp + t * t * x1
        py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cyp + t * t * y1
        o += flower5(a, px, py, r * rnd.uniform(0.85, 1.1), cols[i % len(cols)], rot=rnd.uniform(0, 72))
    return g(o, filter=a.shadow(4, 3, 0.18))


# ---------------------------------------------------------------- output
def write_spec(cat, specs):
    p = os.path.join(HERE, "out", cat + ".json")
    json.dump(specs, open(p, "w"), ensure_ascii=False, indent=1)
    print("wrote", p)


def check_spec(specs, invite):
    minw, minh = (780, 700) if invite else (760, 460)
    for s in specs:
        z = s["zone"]
        w, h = z[2] - z[0], z[3] - z[1]
        msg = []
        if w < minw or h < minh:
            msg.append("zone small %dx%d" % (w, h))
        if z[3] > 1262:
            msg.append("zone into watermark")
        if s.get("photo"):
            p = s["photo"]
            if p["shape"] == "circle":
                bx = (p["x"] - p["r"], p["y"] - p["r"], p["x"] + p["r"], p["y"] + p["r"])
            else:
                bx = (p["x"], p["y"], p["x"] + p["w"], p["y"] + p["h"])
            if not (bx[2] <= z[0] or bx[0] >= z[2] or bx[3] <= z[1] or bx[1] >= z[3]):
                msg.append("photo overlaps zone")
        for k in ("title", "text"):
            pass
        if msg:
            print("WARN", s["id"], "; ".join(msg))


# ================================================================ v2 motifs: party invite
def lmask(a, body, box=(-3000, -3000, 6000, 6000)):
    """mask usable inside transformed groups (local coords)."""
    i = a.uid("lm")
    a.add('<mask id="%s" maskUnits="userSpaceOnUse" x="%s" y="%s" width="%s" height="%s">%s</mask>' % ((i,) + tuple(box) + (body,)))
    return "url(#%s)" % i


def metal(a, col, horiz=True):
    return a.lg([(0, dk(col, 0.35)), (0.22, lt(col, 0.35)), (0.42, lt(col, 0.6)), (0.7, col), (1, dk(col, 0.4))], 0, 0, 1 if horiz else 0, 0 if horiz else 1)


GOLD = [(0, "#A8741F"), (0.3, "#FFE7A6"), (0.55, "#D4A13A"), (0.8, "#FFF1C4"), (1, "#9A6A18")]


def gold(a, diag=True):
    return a.lg(GOLD, 0, 0, 1, 1 if diag else 0)


def flame(a, x, y, ln, w, glow=True):
    """downward exhaust flame, top centre x,y."""
    o = ""
    if glow:
        o += E(x, y + ln * 0.45, w * 1.6, ln * 0.7, a.rg([(0, "#FFE7A0", 0.8), (0.5, "#FF9A3C", 0.3), (1, "#FF6A00", 0)]))
    for k, col in [(1.0, "#FF6A1A"), (0.78, "#FFA630"), (0.55, "#FFE066"), (0.32, "#FFFFFF")]:
        ww, ll = w * k, ln * k
        o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (
            x - ww / 2, y, x - ww * 0.6, y + ll * 0.45, x - ww * 0.1, y + ll * 0.7, x, y + ll,
            x + ww * 0.1, y + ll * 0.7, x + ww * 0.6, y + ll * 0.45, x + ww / 2, y), col)
    return o


def rocket(a, x, y, s, ang=0, body="#F4F6FB", nose="#E8413C", fin="#E8413C", win="#58C4F6", fl=True):
    """rocket centred at x,y, length s, pointing up rotated by ang."""
    w = s * 0.34
    o = ""
    hull = "M0,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f L%.1f,%.1f C%.1f,%.1f %.1f,%.1f 0,%.1fZ" % (
        -s / 2, w * 0.62, -s * 0.36, w * 0.52, -s * 0.08, w * 0.46, s * 0.28, -w * 0.46, s * 0.28, -w * 0.52, -s * 0.08, -w * 0.62, -s * 0.36, -s / 2)
    if fl:
        o += flame(a, 0, s * 0.33, s * 0.62, w * 0.62)
    # fins (behind)
    fg = a.lg([(0, lt(fin, 0.2)), (1, dk(fin, 0.3))], 0, 0, 1, 1)
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f L%.1f,%.1f L%.1f,%.1fZ" % (-w * 0.44, s * 0.0, -w * 0.95, s * 0.12, -w * 1.02, s * 0.3, -w * 0.98, s * 0.42, -w * 0.62, s * 0.3, -w * 0.44, s * 0.27), fg)
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f L%.1f,%.1f L%.1f,%.1fZ" % (w * 0.44, s * 0.0, w * 0.95, s * 0.12, w * 1.02, s * 0.3, w * 0.98, s * 0.42, w * 0.62, s * 0.3, w * 0.44, s * 0.27), a.lg([(0, dk(fin, 0.1)), (1, dk(fin, 0.4))], 0, 0, 1, 1))
    # nozzle
    o += P(poly([(-w * 0.3, s * 0.27), (w * 0.3, s * 0.27), (w * 0.38, s * 0.35), (-w * 0.38, s * 0.35)]), metal(a, "#8C95A8"))
    # hull
    o += P(hull, a.lg([(0, dk(body, 0.28)), (0.3, lt(body, 0.5)), (0.55, body), (1, dk(body, 0.35))], 0, 0, 1, 0))
    cp = a.clip(P(hull, "#000"))
    band = R(-w, -s / 2 - 5, w * 2, s * 0.2 + 5, a.lg([(0, dk(nose, 0.3)), (0.3, lt(nose, 0.35)), (0.55, nose), (1, dk(nose, 0.4))], 0, 0, 1, 0))
    band += R(-w, s * 0.16, w * 2, s * 0.05, a.lg([(0, dk(nose, 0.3)), (0.3, lt(nose, 0.35)), (1, dk(nose, 0.4))], 0, 0, 1, 0))
    band += R(-w, -s * 0.3, w * 2, s * 0.012, "#000", opacity=0.2)
    # rivets
    for yy in (s * 0.12, s * 0.23):
        for xx in (-w * 0.3, -w * 0.15, 0, w * 0.15, w * 0.3):
            band += C(xx, yy, s * 0.006, dk(body, 0.4), opacity=0.6)
    o += g(band, clip_path=cp)
    # centre fin
    o += R(-w * 0.07, s * 0.08, w * 0.14, s * 0.3, a.lg([(0, lt(fin, 0.2)), (1, dk(fin, 0.35))], 0, 0, 1, 0), w * 0.07)
    # window
    wy = -s * 0.07
    o += C(0, wy, w * 0.3, metal(a, "#AEB7C8"))
    o += C(0, wy, w * 0.22, a.rg([(0, lt(win, 0.6)), (0.6, win), (1, dk(win, 0.45))], 0.35, 0.3, 0.75))
    o += P("M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f" % (-w * 0.14, wy - w * 0.02, w * 0.14, w * 0.14, 0, wy - w * 0.15), stroke="#FFFFFF", stroke_width=w * 0.04, stroke_linecap="round", opacity=0.8)
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (-w * 0.32, -s * 0.25, -w * 0.36, -s * 0.05, -w * 0.33, s * 0.1, -w * 0.3, s * 0.25), stroke="#FFFFFF", stroke_width=w * 0.07, stroke_linecap="round", opacity=0.45)
    return g(o, "translate(%.1f %.1f) rotate(%.1f)" % (x, y, ang), filter=a.shadow(14, 10, 0.3))


def smoke_puffs(a, x, y, wdt, n, seed=1, col="#FFFFFF", shade="#C9CFE0"):
    rnd = random.Random(seed)
    o = ""
    for i in range(n):
        px = x + rnd.uniform(-wdt / 2, wdt / 2); py = y + rnd.uniform(-wdt * 0.12, wdt * 0.12)
        r = rnd.uniform(wdt * 0.08, wdt * 0.17)
        o += C(px, py, r, a.rg([(0, col), (0.7, col), (1, shade)], 0.4, 0.35, 0.7))
    return o


def planet(a, x, y, r, col, ring=None, tilt=-18, bands=True, seed=1):
    rnd = random.Random(seed)
    o = ""
    rx, ry = r * 1.9, r * 0.5
    rg_ = None
    if ring:
        rg_ = a.lg([(0, dk(ring, 0.2)), (0.5, lt(ring, 0.45)), (1, dk(ring, 0.25))], 0, 0, 1, 0)
        o += g(E(0, 0, rx, ry, "none", stroke=rg_, stroke_width=r * 0.2) + E(0, 0, rx * 0.86, ry * 0.8, "none", stroke=lt(ring, 0.3), stroke_width=r * 0.05, opacity=0.8),
               "translate(%.1f %.1f) rotate(%.1f)" % (x, y, tilt))
    body = C(x, y, r, a.rg([(0, lt(col, 0.45)), (0.55, col), (1, dk(col, 0.45))], 0.35, 0.3, 0.8))
    if bands:
        cp = a.clip(C(x, y, r, "#000"))
        bb = ""
        for i in range(5):
            yy = y - r + (i + 0.6) * r * 0.4 + rnd.uniform(-8, 8)
            bb += E(x, yy, r * 1.2, r * rnd.uniform(0.04, 0.09), dk(col, 0.2) if i % 2 else lt(col, 0.25), opacity=0.55, transform="rotate(%.1f %.1f %.1f)" % (tilt, x, y))
        bb += C(x + r * 0.35, y + r * 0.3, r * 1.0, "#000", opacity=0.18)
        body += g(bb, clip_path=cp)
    o += body
    if ring:
        o += g(P("M%.1f,0 A%.1f,%.1f 0 0 0 %.1f,0" % (-rx, rx, ry, rx), stroke=rg_, stroke_width=r * 0.2),
               "translate(%.1f %.1f) rotate(%.1f)" % (x, y, tilt))
    return g(o, filter=a.shadow(10, 6, 0.25))


def astronaut(a, cx, cy, r, suit="#F2F4F8", trim="#FF7A45", visor="#FFB347"):
    """helmet whose visor is the photo circle (cx,cy,r); shoulders below."""
    o = ""
    # shoulders / suit
    sh = "M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f L%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (
        cx - r * 1.9, cy + r * 2.25, cx - r * 1.95, cy + r * 1.1, cx - r * 1.3, cy + r * 0.9, cx, cy + r * 0.95,
        cx, cy + r * 0.95, cx + r * 1.3, cy + r * 0.9, cx + r * 1.95, cy + r * 1.1, cx + r * 1.9, cy + r * 2.25)
    o += P(sh, a.lg([(0, dk(suit, 0.25)), (0.3, lt(suit, 0.5)), (0.6, suit), (1, dk(suit, 0.3))], 0, 0, 1, 0))
    # chest control box
    o += R(cx - r * 0.5, cy + r * 1.35, r, r * 0.6, a.lg([(0, "#5B6478"), (1, "#39404F")]), r * 0.1)
    for i, c in enumerate(["#FF5A5F", "#FFD166", "#06D6A0", "#4CC9F0"]):
        o += C(cx - r * 0.33 + i * r * 0.22, cy + r * 1.52, r * 0.07, c)
    o += R(cx - r * 0.35, cy + r * 1.7, r * 0.7, r * 0.1, "#8FE3FF", r * 0.05, opacity=0.8)
    # shoulder trims
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (cx - r * 1.75, cy + r * 1.6, cx - r * 1.6, cy + r * 1.2, cx - r * 1.3, cy + r * 1.05, cx - r * 0.95, cy + r * 1.0), stroke=trim, stroke_width=r * 0.14, stroke_linecap="round")
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (cx + r * 1.75, cy + r * 1.6, cx + r * 1.6, cy + r * 1.2, cx + r * 1.3, cy + r * 1.05, cx + r * 0.95, cy + r * 1.0), stroke=trim, stroke_width=r * 0.14, stroke_linecap="round")
    # neck ring
    o += E(cx, cy + r * 1.0, r * 0.95, r * 0.2, metal(a, "#AEB7C8"))
    # helmet shell
    o += C(cx, cy, r * 1.32, a.rg([(0, "#FFFFFF"), (0.6, suit), (1, dk(suit, 0.3))], 0.35, 0.3, 0.8))
    # side pods
    for sx in (-1, 1):
        o += R(cx + sx * r * 1.32 - r * 0.14, cy - r * 0.35, r * 0.28, r * 0.7, a.lg([(0, lt(trim, 0.2)), (1, dk(trim, 0.3))], 0, 0, 1, 0), r * 0.1)
    # antenna
    o += P("M%.1f,%.1f L%.1f,%.1f" % (cx + r * 0.9, cy - r * 0.95, cx + r * 1.25, cy - r * 1.6), stroke="#9AA3B5", stroke_width=r * 0.05, stroke_linecap="round")
    o += C(cx + r * 1.25, cy - r * 1.6, r * 0.09, trim, filter=a.glow(4))
    # visor rim
    o += C(cx, cy, r * 1.1, a.lg([(0, dk(visor, 0.2)), (0.5, lt(visor, 0.35)), (1, dk(visor, 0.3))], 0, 0, 1, 1))
    o += C(cx, cy, r * 1.02, "#1D2340")
    # placeholder: visor glass with reflection + faint kid silhouette
    o += C(cx, cy, r, a.rg([(0, "#3E4F8C"), (0.7, "#1F2A55"), (1, "#141A3A")], 0.4, 0.35, 0.8))
    o += C(cx, cy - r * 0.18, r * 0.3, "#FFFFFF", opacity=0.12) + P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (cx - r * 0.6, cy + r * 0.8, cx - r * 0.55, cy + r * 0.2, cx + r * 0.55, cy + r * 0.2, cx + r * 0.6, cy + r * 0.8), "#FFFFFF", opacity=0.12)
    o += P("M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f" % (cx - r * 0.75, cy - r * 0.1, r * 0.8, r * 0.8, cx - r * 0.1, cy - r * 0.78), stroke="#FFFFFF", stroke_width=r * 0.08, stroke_linecap="round", opacity=0.45)
    return g(o, filter=a.shadow(16, 12, 0.35))


def monstera(a, x, y, s, ang, col="#2E8B57", seed=1):
    rnd = random.Random(seed)
    shape = "M0,0 C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f 0,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f 0,0Z" % (
        -s * 0.3, s * 0.02, -s * 0.62, -s * 0.2, -s * 0.6, -s * 0.55, -s * 0.58, -s * 0.85, -s * 0.25, -s * 1.02, -s * 0.95,
        s * 0.25, -s * 1.02, s * 0.58, -s * 0.85, s * 0.6, -s * 0.55, s * 0.62, -s * 0.2, s * 0.3, s * 0.02)
    cuts = ""
    for side in (-1, 1):
        for i in range(5):
            t = 0.2 + i * 0.15
            my = -s * (0.08 + t * 0.8)
            ex, ey = side * s * 0.75, my - s * (0.02 + 0.06 * i) + s * 0.12
            cuts += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (side * s * rnd.uniform(0.2, 0.3), my, side * s * 0.45, my - s * 0.02, ex, ey), stroke="#000", stroke_width=s * 0.035, stroke_linecap="round")
        for i in range(2):
            hy = -s * (0.35 + i * 0.25)
            cuts += E(side * s * 0.14, hy, s * 0.025, s * 0.05, "#000")
    m = lmask(a, P(shape, "#FFF") + cuts)
    body = P(shape, a.lg([(0, lt(col, 0.25)), (0.5, col), (1, dk(col, 0.35))], 0, 0, 1, 1))
    veins = P("M0,0 Q%.1f,%.1f 0,%.1f" % (s * 0.03, -s * 0.5, -s * 0.94), stroke=lt(col, 0.4), stroke_width=s * 0.018)
    for side in (-1, 1):
        for i in range(6):
            my = -s * (0.12 + i * 0.13)
            veins += P("M0,%.1f Q%.1f,%.1f %.1f,%.1f" % (my, side * s * 0.2, my - s * 0.02, side * s * 0.5, my - s * 0.05), stroke=lt(col, 0.3), stroke_width=s * 0.008, opacity=0.6)
    inner = g(body + veins, mask=m)
    stem = P("M0,%.1f Q%.1f,%.1f %.1f,%.1f" % (-s * 0.05, -s * 0.05, s * 0.3, -s * 0.02, s * 0.6), stroke=dk(col, 0.2), stroke_width=s * 0.035, stroke_linecap="round")
    return g(stem + inner, "translate(%.1f %.1f) rotate(%.1f)" % (x, y, ang), filter=a.shadow(8, 6, 0.25))


def palm_leaf(a, x, y, s, ang, col="#3FA34D", n=13, curl=0.25):
    """frond: rachis bends; leaflets both sides. base at x,y, points up."""
    o = ""
    def pt(t):
        return (s * curl * t * t, -s * t)
    for i in range(n):
        t = 0.12 + 0.85 * i / (n - 1)
        px, py = pt(t)
        ln = s * 0.42 * math.sin(math.pi * (0.15 + 0.85 * t)) + s * 0.05
        for side in (-1, 1):
            an = math.radians(-90 + side * (58 - 25 * t) + curl * 40 * t)
            ex, ey = px + math.cos(an) * ln, py + math.sin(an) * ln
            nx, ny = -math.sin(an) * ln * 0.09, math.cos(an) * ln * 0.09
            d = "M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1fZ" % (px, py, (px + ex) / 2 + nx, (py + ey) / 2 + ny, ex, ey, (px + ex) / 2 - nx, (py + ey) / 2 - ny, px, py)
            o += P(d, a.lg([(0, dk(col, 0.25)), (1, lt(col, 0.2))], 0, 0, 1, 0))
            o += P("M%.1f,%.1f L%.1f,%.1f" % (px, py, ex, ey), stroke=dk(col, 0.35), stroke_width=1.2, opacity=0.5)
    ex, ey = pt(1)
    o = P("M0,0 Q%.1f,%.1f %.1f,%.1f" % (0, -s * 0.5, ex, ey), stroke=dk(col, 0.35), stroke_width=s * 0.018) + o
    return g(o, "translate(%.1f %.1f) rotate(%.1f)" % (x, y, ang), filter=a.shadow(6, 5, 0.2))


def eye(x, y, r, look=(0.15, 0.1)):
    return E(x, y, r * 0.8, r, "#2A1A12") + C(x + r * look[0] - r * 0.2, y - r * 0.35, r * 0.32, "#FFFFFF") + C(x + r * 0.25, y + r * 0.3, r * 0.14, "#FFFFFF", opacity=0.8)


def lion(a, x, y, s):
    """cute lion head centred x,y; s = face radius."""
    o = ""
    mane = ""
    for i in range(18):
        an = math.radians(i * 20)
        px, py = x + math.cos(an) * s * 1.18, y + math.sin(an) * s * 1.12
        mane += E(px, py, s * 0.42, s * 0.32, a.rg([(0, "#E07A1F"), (1, "#A8480F")], 0.4, 0.4, 0.8), transform="rotate(%.1f %.1f %.1f)" % (i * 20, px, py))
    o += mane + C(x, y, s * 1.2, a.rg([(0, "#F39A2E"), (1, "#C45F13")]))
    for sx in (-1, 1):
        o += C(x + sx * s * 0.72, y - s * 0.7, s * 0.26, "#F2B84B") + C(x + sx * s * 0.72, y - s * 0.7, s * 0.14, "#E88F5A")
    o += C(x, y, s, a.rg([(0, "#FFD77A"), (0.7, "#F6BE4F"), (1, "#E0A032")], 0.45, 0.4, 0.7))
    o += eye(x - s * 0.36, y - s * 0.15, s * 0.13) + eye(x + s * 0.36, y - s * 0.15, s * 0.13)
    o += E(x - s * 0.6, y + s * 0.2, s * 0.14, s * 0.09, "#FF8FA3", opacity=0.6) + E(x + s * 0.6, y + s * 0.2, s * 0.14, s * 0.09, "#FF8FA3", opacity=0.6)
    o += E(x - s * 0.18, y + s * 0.33, s * 0.24, s * 0.2, "#FFF4DC") + E(x + s * 0.18, y + s * 0.33, s * 0.24, s * 0.2, "#FFF4DC")
    for sx in (-1, 1):
        for k in range(3):
            o += C(x + sx * (s * 0.12 + k * s * 0.07), y + s * 0.3 + (k % 2) * s * 0.07, s * 0.018, "#A0653A")
    o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1fZ" % (x - s * 0.14, y + s * 0.12, x, y + s * 0.08, x + s * 0.14, y + s * 0.12, x, y + s * 0.32, x - s * 0.14, y + s * 0.12), "#6B3A1E")
    o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (x, y + s * 0.28, x - s * 0.06, y + s * 0.52, x - s * 0.2, y + s * 0.48, x, y + s * 0.28, x + s * 0.06, y + s * 0.52, x + s * 0.2, y + s * 0.48), stroke="#6B3A1E", stroke_width=s * 0.035, stroke_linecap="round")
    return g(o, filter=a.shadow(10, 8, 0.25))


def giraffe(a, x, ybot, h, s=1.0, face_left=True):
    """neck rising from (x, ybot) height h; head at top."""
    o = ""
    nw = 70 * s
    hx, hy = x - 40 * s, ybot - h
    neck = "M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f L%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (
        x - nw, ybot, x - nw * 0.9, ybot - h * 0.5, hx - nw * 0.2, hy + h * 0.25, hx - nw * 0.3, hy + 40 * s,
        hx + nw * 0.55, hy + 40 * s, hx + nw * 0.7, hy + h * 0.3, x + nw * 0.9, ybot - h * 0.4, x + nw, ybot)
    base = a.lg([(0, "#F2B63C"), (0.5, "#FFD166"), (1, "#E09A25")], 0, 0, 1, 0)
    o += P(neck, base)
    cp = a.clip(P(neck, "#000"))
    rnd = random.Random(3)
    sp = ""
    yy = ybot - 20 * s
    while yy > hy + 50 * s:
        for k in range(2):
            px = x - nw * 0.6 + k * nw * 0.9 + rnd.uniform(-10, 10) * s + (hx - x) * (1 - (yy - hy) / h)
            r = rnd.uniform(24, 34) * s
            pts = [(px + math.cos(math.radians(an)) * r * rnd.uniform(0.75, 1.1), yy + math.sin(math.radians(an)) * r * rnd.uniform(0.7, 1.0)) for an in range(0, 360, 60)]
            sp += P(poly(pts), "#B5651D", stroke="#B5651D", stroke_width=10 * s, stroke_linejoin="round")
        yy -= 72 * s
    o += g(sp, clip_path=cp)
    # mane
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (x + nw * 0.95, ybot - 20, x + nw * 0.8, ybot - h * 0.45, hx + nw * 0.8, hy + h * 0.25, hx + nw * 0.55, hy + 50 * s), stroke="#8A4A18", stroke_width=14 * s, stroke_linecap="round", stroke_dasharray="%d %d" % (10 * s, 6 * s))
    # head
    head = E(hx - 20 * s, hy + 10 * s, 88 * s, 56 * s, a.rg([(0, "#FFE08A"), (1, "#EBA93A")], 0.4, 0.35, 0.8), transform="rotate(-18 %.1f %.1f)" % (hx - 20 * s, hy + 10 * s))
    head += E(hx - 92 * s, hy + 32 * s, 42 * s, 34 * s, "#F7D9A8", transform="rotate(-18 %.1f %.1f)" % (hx - 92 * s, hy + 32 * s))
    head += C(hx - 110 * s, hy + 26 * s, 5 * s, "#7A4A2A") + C(hx - 88 * s, hy + 20 * s, 5 * s, "#7A4A2A")
    head += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (hx - 110 * s, hy + 48 * s, hx - 92 * s, hy + 60 * s, hx - 72 * s, hy + 48 * s), stroke="#7A4A2A", stroke_width=4 * s, stroke_linecap="round")
    # ossicones + ears
    for dx in (0, 34):
        head += P("M%.1f,%.1f L%.1f,%.1f" % (hx + dx * s - 10 * s, hy - 38 * s, hx + dx * s - 16 * s, hy - 88 * s), stroke="#D08A2A", stroke_width=12 * s, stroke_linecap="round")
        head += C(hx + dx * s - 16 * s, hy - 90 * s, 13 * s, "#8A4A18")
    head += E(hx + 62 * s, hy - 26 * s, 34 * s, 14 * s, "#F2B63C", transform="rotate(-25 %.1f %.1f)" % (hx + 62 * s, hy - 26 * s))
    head += E(hx + 62 * s, hy - 26 * s, 22 * s, 7 * s, "#F59E8B", transform="rotate(-25 %.1f %.1f)" % (hx + 62 * s, hy - 26 * s))
    head += eye(hx - 12 * s, hy - 12 * s, 13 * s)
    head += E(hx - 50 * s, hy + 12 * s, 14 * s, 9 * s, "#FF8FA3", opacity=0.55)
    o += head
    if not face_left:
        o = g(o, "translate(%.1f 0) scale(-1 1)" % (2 * x))
    return g(o, filter=a.shadow(12, 8, 0.25))


def fish(a, x, y, s, col, stripes=None, ang=0, face_left=False):
    o = ""
    body = "M%.1f,0 C%.1f,%.1f %.1f,%.1f %.1f,0 C%.1f,%.1f %.1f,%.1f %.1f,0Z" % (s * 0.6, s * 0.35, -s * 0.45, -s * 0.45, -s * 0.4, -s * 0.5, -s * 0.45, s * 0.45, s * 0.35, s * 0.45, s * 0.6)
    tail = "M%.1f,0 L%.1f,%.1f Q%.1f,0 %.1f,%.1fZ" % (-s * 0.42, -s * 0.8, -s * 0.36, -s * 0.66, -s * 0.8, s * 0.36)
    o += P(tail, a.lg([(0, dk(col, 0.25)), (1, lt(col, 0.1))], 0, 0, 1, 0))
    o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Z" % (-s * 0.15, -s * 0.36, s * 0.05, -s * 0.62, s * 0.25, -s * 0.34), dk(col, 0.15))
    o += P(body, a.rg([(0, lt(col, 0.4)), (0.6, col), (1, dk(col, 0.3))], 0.6, 0.35, 0.8))
    if stripes:
        cp = a.clip(P(body, "#000"))
        st = ""
        for sx in (0.3, -0.05, -0.36):
            st += P("M%.1f,%.1f Q%.1f,0 %.1f,%.1f" % (s * sx, -s * 0.6, s * (sx - 0.12), s * sx, s * 0.6), stroke="#1E1E28", stroke_width=s * 0.14)
            st += P("M%.1f,%.1f Q%.1f,0 %.1f,%.1f" % (s * sx, -s * 0.6, s * (sx - 0.12), s * sx, s * 0.6), stroke=stripes, stroke_width=s * 0.09)
        o += g(st, clip_path=cp)
    o += C(s * 0.36, -s * 0.08, s * 0.1, "#FFFFFF") + C(s * 0.38, -s * 0.08, s * 0.06, "#1E1E28") + C(s * 0.36, -s * 0.11, s * 0.02, "#FFFFFF")
    o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (s * 0.08, s * 0.05, -s * 0.02, s * 0.2, s * 0.14, s * 0.25), fill=dk(col, 0.12), opacity=0.8)
    o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (s * 0.52, s * 0.1, s * 0.47, s * 0.15, s * 0.44, s * 0.12), stroke="#1E1E28", stroke_width=s * 0.02, stroke_linecap="round")
    tr = "translate(%.1f %.1f) rotate(%.1f)%s" % (x, y, ang, " scale(-1 1)" if face_left else "")
    return g(o, tr, filter=a.shadow(6, 5, 0.2))


def seaweed(a, x, ybot, h, col, seed=1, blades=3):
    rnd = random.Random(seed)
    o = ""
    for b_ in range(blades):
        bx = x + rnd.uniform(-30, 30); w = rnd.uniform(14, 24); hh = h * rnd.uniform(0.65, 1.0)
        n = 6
        L, Rr = [], []
        for i in range(n + 1):
            t = i / n
            cx = bx + math.sin(t * math.pi * 2.2 + b_) * 28 * t
            ww = w * (1 - t * 0.85)
            L.append((cx - ww, ybot - hh * t)); Rr.append((cx + ww, ybot - hh * t))
        d = "M%.1f,%.1f" % L[0]
        for i in range(1, n + 1):
            d += " Q%.1f,%.1f %.1f,%.1f" % (L[i - 1][0] - 8, (L[i - 1][1] + L[i][1]) / 2, L[i][0], L[i][1])
        d += " L%.1f,%.1f" % Rr[-1]
        for i in range(n - 1, -1, -1):
            d += " Q%.1f,%.1f %.1f,%.1f" % (Rr[i + 1][0] + 8, (Rr[i + 1][1] + Rr[i][1]) / 2, Rr[i][0], Rr[i][1])
        d += "Z"
        c = mix(col, "#0B6E4F", rnd.uniform(0, 0.4))
        o += P(d, a.lg([(0, lt(c, 0.25)), (1, dk(c, 0.2))], 0, 0, 1, 0))
    return o


def coral(a, x, ybot, h, col, seed=1):
    rnd = random.Random(seed)
    o = ""
    def branch(x0, y0, ln, an, w, depth):
        nonlocal o
        x1 = x0 + math.cos(math.radians(an)) * ln; y1 = y0 + math.sin(math.radians(an)) * ln
        o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (x0, y0, (x0 + x1) / 2 + rnd.uniform(-10, 10), (y0 + y1) / 2, x1, y1), stroke=col, stroke_width=w, stroke_linecap="round")
        if depth > 0:
            for d_ in (-1, 1):
                branch(x1, y1, ln * rnd.uniform(0.6, 0.8), an + d_ * rnd.uniform(18, 35), w * 0.72, depth - 1)
        else:
            o += C(x1, y1, w * 0.6, lt(col, 0.3))
    branch(x, ybot, h * 0.4, -90, h * 0.1, 3)
    return g(o, filter=a.shadow(4, 3, 0.2))


def bubbles(a, n, box, seed=1, avoid=(), rr=(6, 26), col="#FFFFFF"):
    rnd = random.Random(seed)
    o = ""
    t = 0
    c = 0
    while c < n and t < n * 20:
        t += 1
        x = rnd.uniform(box[0], box[2]); y = rnd.uniform(box[1], box[3])
        if inside(x, y, list(avoid) + [WM], 12):
            continue
        r = rnd.uniform(*rr)
        o += C(x, y, r, a.rg([(0, col, 0.0), (0.75, col, 0.12), (1, col, 0.55)]), stroke=col, stroke_width=1.5, stroke_opacity=0.6)
        o += P("M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f" % (x - r * 0.6, y - r * 0.1, r * 0.6, r * 0.6, x - r * 0.05, y - r * 0.6), stroke=col, stroke_width=max(1.5, r * 0.15), stroke_linecap="round", opacity=0.85)
        c += 1
    return o


def whale(a, x, y, s, col="#3F7FD9"):
    """cute whale centred at x,y, length ~2s, facing left, with spout."""
    o = ""
    body = "M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (
        -s, 0,
        -s, -s * 0.62, -s * 0.2, -s * 0.72, s * 0.35, -s * 0.45,
        s * 0.6, -s * 0.32, s * 0.72, -s * 0.2, s * 0.95, -s * 0.5,
        s * 0.9, -s * 0.1, s * 0.75, s * 0.35, s * 0.2, s * 0.36,
        -s * 0.4, s * 0.4, -s, s * 0.3, -s, 0)
    tail = "M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (
        s * 0.85, -s * 0.35, s * 0.9, -s * 0.7, s * 1.15, -s * 0.8, s * 1.3, -s * 0.72, s * 1.1, -s * 0.62, s * 1.05, -s * 0.45, s * 0.95, -s * 0.3)
    tail2 = "M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (
        s * 0.85, -s * 0.35, s * 0.75, -s * 0.7, s * 0.65, -s * 0.9, s * 0.5, -s * 0.92, s * 0.72, -s * 0.72, s * 0.8, -s * 0.5, s * 0.95, -s * 0.3)
    bf = a.rg([(0, lt(col, 0.35)), (0.6, col), (1, dk(col, 0.3))], 0.35, 0.3, 0.9)
    o += P(tail, bf) + P(tail2, bf)
    o += P(body, bf)
    cp = a.clip(P(body, "#000"))
    belly = E(-s * 0.25, s * 0.35, s * 0.85, s * 0.3, "#E8F4FF")
    for i in range(6):
        belly += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (-s * 0.85 + i * s * 0.2, s * 0.12, -s * 0.8 + i * s * 0.2, s * 0.3, -s * 0.78 + i * s * 0.2, s * 0.45), stroke=lt(col, 0.4), stroke_width=s * 0.02, opacity=0.8)
    o += g(belly, clip_path=cp)
    o += E(-s * 0.55, -s * 0.08, s * 0.07, s * 0.08, "#1C2440") + C(-s * 0.57, -s * 0.11, s * 0.025, "#FFFFFF")
    o += E(-s * 0.72, s * 0.06, s * 0.1, s * 0.06, "#FF8FA3", opacity=0.6)
    o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (-s * 0.95, s * 0.12, -s * 0.75, s * 0.24, -s * 0.5, s * 0.12), stroke="#1C2440", stroke_width=s * 0.025, stroke_linecap="round")
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (-s * 0.15, s * 0.2, s * 0.05, s * 0.35, s * 0.1, s * 0.55, -s * 0.05, s * 0.6, -s * 0.1, s * 0.45, -s * 0.2, s * 0.3, -s * 0.15, s * 0.2), dk(col, 0.15))
    # spout
    sp = ""
    sx, sy = -s * 0.25, -s * 0.66
    for k in (-1, 0, 1):
        sp += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (sx, sy, sx + k * s * 0.05, sy - s * 0.3, sx + k * s * 0.25, sy - s * 0.45, sx + k * s * 0.42, sy - s * 0.32), stroke="#BDEBFF", stroke_width=s * 0.05, stroke_linecap="round")
    for k in (-1, 1):
        sp += C(sx + k * s * 0.45, sy - s * 0.28, s * 0.05, "#BDEBFF")
    sp += C(sx, sy - s * 0.42, s * 0.05, "#BDEBFF")
    o += sp
    return g(o, "translate(%.1f %.1f)" % (x, y), filter=a.shadow(12, 8, 0.25))


def starfish(a, x, y, r, col, rot=0):
    o = P(star_pts(x, y, r, r * 0.45, 5, -90 + rot), a.rg([(0, lt(col, 0.35)), (1, dk(col, 0.2))]), stroke=dk(col, 0.1), stroke_width=r * 0.25, stroke_linejoin="round")
    for i in range(5):
        an = math.radians(-90 + rot + i * 72)
        for k in (0.3, 0.55):
            o += C(x + math.cos(an) * r * k, y + math.sin(an) * r * k, r * 0.06, lt(col, 0.6))
    return o


def circus_tent(a, cx, top, ey, hw, bot, cols=("#D7263D", "#FFF6E8"), n=12, door=True):
    """big top: peak at (cx,top), eaves at y=ey spanning cx+-hw, walls down to bot."""
    o = ""
    c1, c2 = cols
    # walls
    for i in range(n):
        x0 = cx - hw * 0.92 + i * (hw * 1.84 / n)
        o += R(x0, ey, hw * 1.84 / n + 0.5, bot - ey, a.lg([(0, dk(c1 if i % 2 == 0 else c2, 0.12)), (1, c1 if i % 2 == 0 else c2)], 0, 0, 1, 0))
    o += R(cx - hw * 0.92, ey, hw * 1.84, bot - ey, a.lg([(0, "#000", 0.25), (0.25, "#000", 0), (0.75, "#000", 0), (1, "#000", 0.3)], 0, 0, 1, 0))
    if door:
        dw = hw * 0.42
        o += P("M%.1f,%.1f L%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Z" % (cx - dw / 2, bot, cx - dw / 2, ey + 70, cx, ey + 10, cx + dw / 2, ey + 70) + " L%.1f,%.1fZ" % (cx + dw / 2, bot), "#2A0F2E")
        o += P("M%.1f,%.1f L%.1f,%.1f Q%.1f,%.1f %.1f,%.1fZ" % (cx - dw / 2, ey + 70, cx - dw / 2, bot, cx - dw * 0.28, ey + (bot - ey) * 0.55, cx, ey + 10), a.lg([(0, dk(c1, 0.2)), (1, lt(c1, 0.15))], 0, 0, 1, 0))
        o += P("M%.1f,%.1f L%.1f,%.1f Q%.1f,%.1f %.1f,%.1fZ" % (cx + dw / 2, ey + 70, cx + dw / 2, bot, cx + dw * 0.28, ey + (bot - ey) * 0.55, cx, ey + 10), a.lg([(0, lt(c1, 0.15)), (1, dk(c1, 0.2))], 0, 0, 1, 0))
        o += C(cx - dw * 0.34, ey + (bot - ey) * 0.55, 9, gold(a)) + C(cx + dw * 0.34, ey + (bot - ey) * 0.55, 9, gold(a))
    # roof sections
    roof = ""
    for i in range(n):
        x0 = cx - hw + i * (2 * hw / n); x1 = x0 + 2 * hw / n
        col = c1 if i % 2 == 0 else c2
        roof += P("M%.1f,%.1f L%.1f,%.1f Q%.1f,%.1f %.1f,%.1fZ" % (cx, top, x0, ey, (x0 + x1) / 2, ey + 14, x1, ey), a.lg([(0, lt(col, 0.15)), (1, dk(col, 0.12))]))
    o += roof
    o += P("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1fZ" % (cx, top, cx + hw, ey, cx, ey), "#000", opacity=0.1)
    # scalloped valance
    sw = 2 * hw / n
    val = ""
    for i in range(n):
        x0 = cx - hw + i * sw
        col = c2 if i % 2 == 0 else c1
        val += P("M%.1f,%.1f L%.1f,%.1f Q%.1f,%.1f %.1f,%.1fZ" % (x0, ey - 4, x0 + sw, ey - 4, x0 + sw / 2, ey + sw * 0.75, x0, ey - 4), col)
        val += C(x0 + sw / 2, ey + sw * 0.52, 5, gold(a))
    o += g(val, filter=a.shadow(4, 4, 0.25))
    o += P("M%.1f,%.1f L%.1f,%.1f" % (cx - hw, ey - 2, cx + hw, ey - 2), stroke=gold(a, False), stroke_width=8, stroke_linecap="round")
    # flag
    o += P("M%.1f,%.1f L%.1f,%.1f" % (cx, top + 4, cx, top - 70), stroke="#6B4A2B", stroke_width=5)
    o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f L%.1f,%.1f Q%.1f,%.1f %.1f,%.1fZ" % (cx, top - 70, cx + 30, top - 80, cx + 62, top - 60, cx + 50, top - 48, cx + 26, top - 56, cx, top - 42), a.lg([(0, "#FFD166"), (1, "#F4A300")]))
    o += C(cx, top - 72, 7, gold(a))
    return g(o, filter=a.shadow(16, 10, 0.3))


def bulb(a, x, y, r, col="#FFE9A8", lit=True):
    o = ""
    if lit:
        o += C(x, y, r * 2.6, a.rg([(0, col, 0.55), (1, col, 0)]))
    o += C(x, y, r * 1.25, "#7A5A1E")
    o += C(x, y, r, a.rg([(0, "#FFFFFF"), (0.45, col), (1, dk(col, 0.25))], 0.4, 0.35, 0.7))
    return o


def bulbs_rect(a, x0, y0, x1, y1, sp, r, col="#FFE9A8"):
    o = ""
    nx = max(2, int(round((x1 - x0) / sp))); ny = max(2, int(round((y1 - y0) / sp)))
    for i in range(nx + 1):
        xx = x0 + (x1 - x0) * i / nx
        o += bulb(a, xx, y0, r, col) + bulb(a, xx, y1, r, col)
    for j in range(1, ny):
        yy = y0 + (y1 - y0) * j / ny
        o += bulb(a, x0, yy, r, col) + bulb(a, x1, yy, r, col)
    return o


def ticket_path(x, y, w, h, notch=34, cr=26):
    """ticket with concave corners and side notches."""
    return ("M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f "
            "L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1fZ") % (
        x + cr, y, x + w - cr, y, cr, cr, x + w, y + cr,
        x + w, y + h / 2 - notch, notch, notch, x + w, y + h / 2 + notch,
        x + w, y + h - cr, cr, cr, x + w - cr, y + h,
        x + cr, y + h, cr, cr, x, y + h - cr,
        x, y + h / 2 + notch, notch, notch, x, y + h / 2 - notch,
        x, y + cr, cr, cr, x + cr, y)


def curtain(a, x0, x1, top, bot, col="#B3122E", side="left", tie=0.62, folds=7):
    """side curtain drape gathered to a tie-back."""
    o = ""
    w = x1 - x0
    ty = top + (bot - top) * tie
    if side == "left":
        d = "M%.1f,%.1f L%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f L%.1f,%.1fZ" % (
            x0, top, x1, top, x1, top + (ty - top) * 0.5, x0 + w * 0.35, ty - 40, x0 + w * 0.3, ty, x0 + w * 0.32, ty + 60, x0 + w * 0.6, bot - 60, x0 + w * 0.55, bot, x0, bot)
    else:
        d = "M%.1f,%.1f L%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f L%.1f,%.1fZ" % (
            x1, top, x0, top, x0, top + (ty - top) * 0.5, x1 - w * 0.35, ty - 40, x1 - w * 0.3, ty, x1 - w * 0.32, ty + 60, x1 - w * 0.6, bot - 60, x1 - w * 0.55, bot, x1, bot)
    stops = []
    for i in range(folds * 2 + 1):
        stops.append((round(i / (folds * 2.0), 3), dk(col, 0.45) if i % 2 == 0 else lt(col, 0.18)))
    o += P(d, a.lg(stops, 0, 0, 1, 0), filter=a.shadow(14, 6, 0.4))
    tx = x0 + w * 0.3 if side == "left" else x1 - w * 0.3
    o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (tx - 50, ty - 10, tx, ty + 18, tx + 50, ty - 10), stroke=gold(a, False), stroke_width=12, stroke_linecap="round")
    o += C(tx + (50 if side == "left" else -50), ty - 6, 14, gold(a))
    o += P("M%.1f,%.1f l-10,70 l20,0Z" % (tx + (50 if side == "left" else -50), ty + 4), gold(a))
    return o


def valance(a, x0, x1, top, h, col="#B3122E", n=5):
    o = ""
    sw = (x1 - x0) / n
    for i in range(n):
        xa = x0 + i * sw
        d = "M%.1f,%.1f L%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Z" % (xa - 10, top, xa + sw + 10, top, xa + sw / 2, top + h * 2, xa - 10, top)
        o += P(d, a.lg([(0, dk(col, 0.35)), (0.6, col), (1, lt(col, 0.2))]), filter=a.shadow(8, 6, 0.35))
        o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (xa - 6, top + 6, xa + sw / 2, top + h * 1.95, xa + sw + 6, top + 6), stroke=gold(a, False), stroke_width=7)
        for k in range(1, 8):
            t = k / 8.0
            px = (1 - t) ** 2 * (xa - 6) + 2 * (1 - t) * t * (xa + sw / 2) + t * t * (xa + sw + 6)
            py = (1 - t) ** 2 * (top + 6) + 2 * (1 - t) * t * (top + h * 1.95) + t * t * (top + 6)
            o += P("M%.1f,%.1f l0,18" % (px, py), stroke="#E8B64C", stroke_width=4, stroke_linecap="round")
    o += R(x0 - 20, top - 30, x1 - x0 + 40, 40, a.lg([(0, dk(col, 0.4)), (1, col)]))
    return o


def disco_ball(a, cx, cy, r, tint=("#DDE3F0", "#9AA6C4", "#FFFFFF", "#C9B8FF", "#8FD8FF", "#6E7898"), seed=1):
    rnd = random.Random(seed)
    o = C(cx, cy, r, "#4A5270")
    rows = 12
    tiles = ""
    for i in range(rows):
        la0 = -math.pi / 2 + i * math.pi / rows
        la1 = la0 + math.pi / rows
        n = max(6, int(24 * math.cos((la0 + la1) / 2)))
        for j in range(n):
            lo0 = -math.pi / 2 + j * math.pi / n
            lo1 = lo0 + math.pi / n
            pts = []
            for la, lo in ((la0, lo0), (la0, lo1), (la1, lo1), (la1, lo0)):
                pts.append((cx + r * math.cos(la) * math.sin(lo) * 0.985, cy + r * math.sin(la) * 0.985))
            # lighting: light from upper left
            lx = math.cos((la0 + la1) / 2) * math.sin((lo0 + lo1) / 2); ly = math.sin((la0 + la1) / 2)
            br = 0.5 - 0.35 * lx - 0.35 * ly + rnd.uniform(-0.25, 0.25)
            c = rnd.choice(tint)
            c = lt(c, max(0, br) * 0.6) if br > 0.4 else dk(c, (0.4 - br) * 0.8)
            tiles += P(poly(pts), c, stroke="#3A4060", stroke_width=0.8)
    o += tiles
    o += C(cx, cy, r, a.rg([(0, "#FFFFFF", 0), (0.8, "#000", 0.05), (1, "#000", 0.4)], 0.4, 0.35, 0.7))
    o += C(cx - r * 0.35, cy - r * 0.38, r * 0.25, a.rg([(0, "#FFFFFF", 0.9), (1, "#FFFFFF", 0)]))
    for (dx, dy, s) in [(-0.35, -0.38, 0.35), (0.3, -0.1, 0.2), (-0.1, 0.4, 0.18), (0.5, 0.45, 0.14)]:
        o += sparkle(cx + dx * r, cy + dy * r, r * s, "#FFFFFF", filter=a.glow(3))
    # cap and chain
    o += R(cx - r * 0.12, cy - r - r * 0.12, r * 0.24, r * 0.16, metal(a, "#AEB7C8"), 3)
    return o


def party_hat(a, x, ybot, h, col, col2="#FFFFFF", pom="#FFD166", ang=0, pat="stripe"):
    w = h * 0.62
    o = ""
    cone = poly([(-w / 2, 0), (w / 2, 0), (0, -h)])
    o += P(cone, a.lg([(0, dk(col, 0.2)), (0.4, lt(col, 0.2)), (1, dk(col, 0.25))], 0, 0, 1, 0))
    cp = a.clip(P(cone, "#000"))
    deco = ""
    if pat == "stripe":
        for k in range(-3, 6):
            deco += P("M%.1f,0 L%.1f,%.1f" % (-w / 2 + k * w * 0.28, -w / 2 + k * w * 0.28 + h * 0.6, -h), stroke=col2, stroke_width=w * 0.09, opacity=0.9)
    else:
        rnd = random.Random(int(h))
        for k in range(26):
            deco += C(rnd.uniform(-w / 2, w / 2), -rnd.uniform(0, h), w * 0.05, col2, opacity=0.9)
    deco += P(poly([(0, -h), (w / 2, 0), (0, 0)]), "#000", opacity=0.1)
    o += g(deco, clip_path=cp)
    # fringe band
    o += E(0, 0, w / 2 + 4, h * 0.05, lt(pom, 0.2))
    for k in range(9):
        o += P("M%.1f,%.1f l%.1f,%.1f" % (-w / 2 + k * w / 8, 0, 0, h * 0.07), stroke=pom, stroke_width=4, stroke_linecap="round")
    # pompom
    for k in range(10):
        an = math.radians(k * 36)
        o += P("M0,%.1f l%.1f,%.1f" % (-h, math.cos(an) * h * 0.1, math.sin(an) * h * 0.1), stroke=pom, stroke_width=h * 0.045, stroke_linecap="round")
    o += C(0, -h, h * 0.07, lt(pom, 0.3))
    return g(o, "translate(%.1f %.1f) rotate(%.1f)" % (x, ybot, ang), filter=a.shadow(8, 6, 0.25))


def rosette_badge(a, cx, cy, r, col="#E63973", col2="#FFD166", tails=True):
    """award rosette around a circle (photo) of radius r."""
    o = ""
    if tails:
        for sx, rot in ((-1, 14), (1, -14)):
            tx = cx + sx * r * 0.35
            d = "M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1fZ" % (tx - r * 0.2, cy + r * 0.6, tx + r * 0.2, cy + r * 0.6, tx + r * 0.22, cy + r * 1.75, tx, cy + r * 1.55, tx - r * 0.22, cy + r * 1.75)
            o += P(d, a.lg([(0, dk(col, 0.1)), (0.5, lt(col, 0.2)), (1, dk(col, 0.3))], 0, 0, 1, 0), transform="rotate(%d %.1f %.1f)" % (rot, tx, cy + r * 0.6))
    n = 28
    pl = ""
    for i in range(n):
        an = math.radians(i * 360.0 / n)
        pl += E(cx + math.cos(an) * r * 1.22, cy + math.sin(an) * r * 1.22, r * 0.2, r * 0.13, a.lg([(0, lt(col, 0.3)), (1, dk(col, 0.2))]), transform="rotate(%.1f %.1f %.1f)" % (i * 360.0 / n, cx + math.cos(an) * r * 1.22, cy + math.sin(an) * r * 1.22))
    o += C(cx, cy, r * 1.3, dk(col, 0.1)) + pl
    for i in range(n):
        an = math.radians(i * 360.0 / n + 6)
        o += C(cx + math.cos(an) * r * 1.1, cy + math.sin(an) * r * 1.1, r * 0.08, col2)
    o += C(cx, cy, r * 1.06, gold(a))
    o += C(cx, cy, r * 1.01, "#FFFFFF")
    return g(o, filter=a.shadow(14, 10, 0.3))


def kid_silhouette(a, cx, cy, r, col, op=0.35):
    """faint child placeholder inside a photo slot (circle-ish region radius r)."""
    return g(C(cx, cy - r * 0.2, r * 0.3, col) + P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" % (cx - r * 0.62, cy + r * 0.85, cx - r * 0.58, cy + r * 0.2, cx + r * 0.58, cy + r * 0.2, cx + r * 0.62, cy + r * 0.85), col), opacity=op)


def monkey(a, x, y, s):
    """monkey hanging by one arm; hand at x,y."""
    o = ""
    br = "#7A4A2A"; fc = "#F2D1A5"
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (x, y, x - s * 0.1, y + s * 0.4, x - s * 0.3, y + s * 0.6, x - s * 0.2, y + s * 0.9), stroke=br, stroke_width=s * 0.14, stroke_linecap="round")
    o += C(x, y, s * 0.1, br)
    # tail
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (x - s * 0.1, y + s * 1.7, x + s * 0.5, y + s * 2.0, x + s * 0.7, y + s * 1.5, x + s * 0.5, y + s * 1.35, x + s * 0.35, y + s * 1.25, x + s * 0.4, y + s * 1.5, x + s * 0.55, y + s * 1.5), stroke=br, stroke_width=s * 0.08, stroke_linecap="round")
    # body
    o += E(x - s * 0.15, y + s * 1.35, s * 0.36, s * 0.45, a.rg([(0, lt(br, 0.2)), (1, dk(br, 0.2))], 0.4, 0.3, 0.8))
    o += E(x - s * 0.15, y + s * 1.42, s * 0.22, s * 0.3, fc)
    # legs
    o += P("M%.1f,%.1f q%.1f,%.1f %.1f,%.1f M%.1f,%.1f q%.1f,%.1f %.1f,%.1f" % (x - s * 0.35, y + s * 1.7, -s * 0.1, s * 0.25, s * 0.05, s * 0.35, x + s * 0.05, y + s * 1.7, s * 0.1, s * 0.25, -s * 0.05, s * 0.35), stroke=br, stroke_width=s * 0.13, stroke_linecap="round")
    # other arm waving
    o += P("M%.1f,%.1f q%.1f,%.1f %.1f,%.1f" % (x + s * 0.12, y + s * 1.15, s * 0.3, s * 0.0, s * 0.45, -s * 0.3), stroke=br, stroke_width=s * 0.13, stroke_linecap="round")
    # head
    hx, hy = x - s * 0.2, y + s * 0.78
    o += C(hx - s * 0.36, hy, s * 0.14, br) + C(hx + s * 0.36, hy, s * 0.14, br) + C(hx - s * 0.36, hy, s * 0.08, fc) + C(hx + s * 0.36, hy, s * 0.08, fc)
    o += C(hx, hy, s * 0.34, a.rg([(0, lt(br, 0.2)), (1, dk(br, 0.2))], 0.4, 0.3, 0.8))
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (
        hx, hy - s * 0.12, hx - s * 0.1, hy - s * 0.3, hx - s * 0.36, hy - s * 0.18, hx - s * 0.26, hy + s * 0.05,
        hx - s * 0.32, hy + s * 0.3, hx + s * 0.32, hy + s * 0.3, hx + s * 0.26, hy + s * 0.05,
        hx + s * 0.36, hy - s * 0.18, hx + s * 0.1, hy - s * 0.3, hx, hy - s * 0.12), fc)
    o += eye(hx - s * 0.12, hy - s * 0.04, s * 0.06) + eye(hx + s * 0.12, hy - s * 0.04, s * 0.06)
    o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (hx - s * 0.1, hy + s * 0.15, hx, hy + s * 0.24, hx + s * 0.1, hy + s * 0.15), stroke="#5A3018", stroke_width=s * 0.03, stroke_linecap="round")
    return g(o, filter=a.shadow(8, 6, 0.25))


def toucan(a, x, y, s, flip=False):
    o = ""
    o += P("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1fZ" % (x + s * 0.1, y + s * 0.5, x + s * 0.5, y + s * 1.1, x + s * 0.3, y + s * 0.4), "#1B1B24")
    o += E(x, y + s * 0.35, s * 0.32, s * 0.5, a.rg([(0, "#3A3A48"), (1, "#101018")], 0.4, 0.3, 0.8), transform="rotate(15 %.1f %.1f)" % (x, y + s * 0.35))
    o += E(x - s * 0.12, y + s * 0.2, s * 0.17, s * 0.25, "#FFF3C4")
    o += C(x - s * 0.02, y, s * 0.24, "#1B1B24")
    o += C(x - s * 0.08, y - s * 0.03, s * 0.09, "#6FD6FF") + C(x - s * 0.08, y - s * 0.03, s * 0.04, "#101018") + C(x - s * 0.1, y - s * 0.05, s * 0.015, "#FFFFFF")
    beak = "M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (x - s * 0.18, y - s * 0.1, x - s * 0.5, y - s * 0.25, x - s * 0.8, y - s * 0.05, x - s * 0.82, y + s * 0.1, x - s * 0.6, y + s * 0.08, x - s * 0.4, y + s * 0.12, x - s * 0.16, y + s * 0.08)
    o += P(beak, a.lg([(0, "#FF3D2E"), (0.35, "#FF9F1C"), (1, "#FFD23F")], 1, 0, 0, 0))
    o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (x - s * 0.18, y + s * 0.0, x - s * 0.5, y + s * 0.02, x - s * 0.8, y + s * 0.06), stroke="#8A3A10", stroke_width=s * 0.02, opacity=0.5)
    o += P("M%.1f,%.1f L%.1f,%.1f" % (x - s * 0.3, y + s * 0.82, x + s * 0.4, y + s * 0.82), stroke="#6B4A2B", stroke_width=s * 0.08, stroke_linecap="round")
    tr = "translate(%.1f 0) scale(-1 1)" % (2 * x) if flip else None
    return g(o, tr, filter=a.shadow(8, 6, 0.25))


def vine(a, x0, y0, x1, y1, sag, seed=1, col="#3B8A3E"):
    rnd = random.Random(seed)
    cxp, cyp = (x0 + x1) / 2, (y0 + y1) / 2 + sag * 2
    o = P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (x0, y0, cxp, cyp, x1, y1), stroke="#6B5A2B", stroke_width=7)
    for i in range(1, 22):
        t = i / 22.0
        px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cxp + t * t * x1
        py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cyp + t * t * y1
        o += leaf(a, px, py, rnd.uniform(26, 40), rnd.choice([-150, -120, 120, 150, 170, -170]), mix(col, "#7FC75A", rnd.random() * 0.5), vein=True)
    return o


# ================================================================ v2 motifs: naming ceremony (namkaran)
def sleeping_baby(a, cx, cy, s, cap="#F7C6D9", blanket="#BFD9F5"):
    """baby head + swaddle, lying horizontally, head on the left. s = head radius."""
    o = ""
    # swaddle body
    o += E(cx + s * 1.5, cy + s * 0.35, s * 1.8, s * 0.85, a.lg([(0, lt(blanket, 0.4)), (1, dk(blanket, 0.12))]))
    o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (cx + s * 0.4, cy - s * 0.3, cx + s * 1.3, cy + s * 0.5, cx + s * 0.9, cy + s * 1.1), stroke=dk(blanket, 0.15), stroke_width=s * 0.08, opacity=0.6)
    o += R(cx + s * 0.6, cy - s * 0.4, s * 2.2, s * 1.4, dots_pattern(a, "#FFFFFF", s * 0.4, s * 0.05, 0.6), s * 0.5, opacity=0.9)
    # head
    o += C(cx, cy, s, a.rg([(0, "#FFE3CF"), (0.8, "#F7C9A8"), (1, "#E9AE8A")], 0.45, 0.4, 0.75))
    # cap
    o += P("M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f Q%.1f,%.1f %.1f,%.1fZ" % (cx - s * 0.95, cy - s * 0.25, s, s, cx + s * 0.75, cy - s * 0.65, cx - s * 0.1, cy - s * 0.2, cx - s * 0.95, cy - s * 0.25), a.lg([(0, lt(cap, 0.3)), (1, dk(cap, 0.1))]))
    o += C(cx - s * 0.2, cy - s * 1.02, s * 0.2, lt(cap, 0.4))
    # face
    for dx in (-0.35, 0.2):
        o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (cx + s * (dx - 0.14), cy + s * 0.12, cx + s * dx, cy + s * 0.24, cx + s * (dx + 0.14), cy + s * 0.12), stroke="#8A5A44", stroke_width=s * 0.05, stroke_linecap="round")
    o += E(cx - s * 0.52, cy + s * 0.38, s * 0.16, s * 0.1, "#FF9DB0", opacity=0.6) + E(cx + s * 0.4, cy + s * 0.38, s * 0.16, s * 0.1, "#FF9DB0", opacity=0.6)
    o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (cx - s * 0.12, cy + s * 0.52, cx - s * 0.04, cy + s * 0.58, cx + s * 0.04, cy + s * 0.52), stroke="#C0706A", stroke_width=s * 0.04, stroke_linecap="round")
    # details: hair curl, lashes, tiny hand, swaddle bow + fold highlight
    o += P("M%.1f,%.1f q%.1f,%.1f %.1f,%.1f q%.1f,%.1f %.1f,%.1f" % (cx + s * 0.5, cy - s * 0.55, s * 0.18, -s * 0.05, s * 0.2, s * 0.12, -s * 0.02, s * 0.1, -s * 0.12, s * 0.06), stroke="#A0704E", stroke_width=s * 0.05, stroke_linecap="round")
    for dx in (-0.35, 0.2):
        for k in (-1, 0, 1):
            o += P("M%.1f,%.1f l%.1f,%.1f" % (cx + s * (dx + k * 0.08), cy + s * 0.21, k * s * 0.03, s * 0.07), stroke="#8A5A44", stroke_width=s * 0.025, stroke_linecap="round")
    o += E(cx + s * 0.78, cy + s * 0.55, s * 0.2, s * 0.16, a.rg([(0, "#FFE3CF"), (1, "#EDB595")]))
    for k in range(3):
        o += C(cx + s * (0.68 + k * 0.1), cy + s * 0.43, s * 0.055, "#F7C9A8")
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (cx + s * 1.1, cy - s * 0.4, cx + s * 1.8, cy - s * 0.2, cx + s * 2.4, cy - s * 0.1, cx + s * 3.1, cy + s * 0.1), stroke="#FFFFFF", stroke_width=s * 0.1, stroke_linecap="round", opacity=0.55)
    bx, by_ = cx + s * 1.9, cy + s * 0.35
    o += bow_shape(a, bx, by_, s * 0.45, cap)
    return o


def zzz(a, x, y, s, col):
    """sleep swirl (no letters): three small crescents rising."""
    o = ""
    for i in range(3):
        o += crescent(a, x + i * s * 0.9, y - i * s * 1.1, s * (0.35 + i * 0.12), col, 0.5)
    return o


def palna_hanging(a, cx, ytop, ybot, w, wood="#C98B4E", cloth="#F9D5E0", flowers=("#FFFFFF", "#FFB7C9", "#FFE08A"), baby=True, rope="#E8C27A"):
    """hanging jhula-style cradle: ropes from (cx,ytop) hook, wrapped with flowers, cradle body ends at ybot."""
    o = ""
    bh = w * 0.34
    by = ybot - bh
    x0, x1 = cx - w / 2, cx + w / 2
    # ropes (four, two visible sides)
    rp = ""
    for sx in (x0 + w * 0.06, x1 - w * 0.06):
        rp += P("M%.1f,%.1f L%.1f,%.1f" % (cx, ytop + 26, sx, by + 6), stroke=rope, stroke_width=6)
        # flower wraps along rope
        n = 9
        for i in range(1, n):
            t = i / n
            px, py = cx + (sx - cx) * t, ytop + 26 + (by - ytop - 26) * t
            rp += flower5(a, px, py, 13, flowers[i % len(flowers)], center="#F6C343", rot=i * 23)
    o += rp
    # hook + ring
    o += C(cx, ytop + 14, 16, "none", stroke=gold(a), stroke_width=6) + R(cx - 4, ytop - 40, 8, 44, gold(a))
    # cradle basket (boat shape)
    body = "M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" % (
        x0, by, x0 + w * 0.02, ybot - bh * 0.1, x0 + w * 0.25, ybot, cx, ybot,
        x1 - w * 0.25, ybot, x1 - w * 0.02, ybot - bh * 0.1, x1, by)
    # back rim (inside)
    o += E(cx, by, w / 2, bh * 0.22, dk(wood, 0.35))
    if baby:
        o += sleeping_baby(a, cx - w * 0.2, by - bh * 0.2, bh * 0.36)
    o += P(body, a.lg([(0, lt(wood, 0.25)), (0.5, wood), (1, dk(wood, 0.35))]))
    cp = a.clip(P(body, "#000"))
    # cloth drape panel with scallop
    drape = R(x0, by, w, bh * 0.55, a.lg([(0, lt(cloth, 0.3)), (1, dk(cloth, 0.08))]))
    sc = ""
    k = 14
    for i in range(k):
        xx = x0 + (i + 0.5) * w / k
        sc += C(xx, by + bh * 0.55, w / k / 2, lt(cloth, 0.1))
        sc += C(xx, by + bh * 0.62, 3.5, gold(a))
    drape += sc
    # carved band
    band = ""
    for i in range(1, 16):
        xx = x0 + i * w / 16
        band += C(xx, ybot - bh * 0.22, 7, gold(a)) + C(xx, ybot - bh * 0.22, 3, dk(wood, 0.4))
    o += g(drape + band + R(x0, by, w * 0.08, bh, "#000", opacity=0.08), clip_path=cp)
    # front rim
    o += P("M%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f" % (x0, by, w / 2, bh * 0.22, x1, by), stroke=gold(a, False), stroke_width=9, stroke_linecap="round")
    # end finials
    for xx in (x0, x1):
        o += C(xx, by - 4, 16, gold(a))
        o += C(xx, by - 4, 7, dk(wood, 0.3))
    # tassels hanging below
    for xx in (x0 + w * 0.15, cx, x1 - w * 0.15):
        yb = ybot - (bh * 0.05 if xx != cx else 0)
        o += P("M%.1f,%.1f L%.1f,%.1f" % (xx, yb - 6, xx, yb + 26), stroke=gold(a, False), stroke_width=3)
        o += P("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1fZ" % (xx - 9, yb + 50, xx, yb + 22, xx + 9, yb + 50), "#F4A6B8")
        o += C(xx, yb + 24, 6, gold(a))
    return g(o, filter=a.shadow(14, 10, 0.25))


def palna_stand(a, cx, ybot, w, h, wood="#B9793F", cloth="#FBE3EA", baby=True, garl=("#FFFFFF", "#FFB7C9", "#FFE08A"), photo=None):
    """traditional wooden palna: two carved posts with a top beam; cradle swings between.
    photo=(cx,cy,r) : a circular window in the cradle's pillow region instead of the baby."""
    o = ""
    wf = a.lg([(0, dk(wood, 0.3)), (0.35, lt(wood, 0.3)), (0.6, wood), (1, dk(wood, 0.4))], 0, 0, 1, 0)
    x0, x1 = cx - w / 2, cx + w / 2
    top = ybot - h
    # feet
    for xx in (x0, x1):
        o += P("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1fZ" % (xx - 90, ybot, xx - 20, ybot - 30, xx + 20, ybot - 30, xx + 90, ybot), a.lg([(0, lt(wood, 0.1)), (1, dk(wood, 0.35))]))
        o += R(xx - 96, ybot - 6, 192, 12, dk(wood, 0.3), 6)
    # posts (turned)
    for xx in (x0, x1):
        o += R(xx - 16, top + 30, 32, h - 60, wf, 8)
        for t in (0.25, 0.5, 0.75):
            yy = top + 30 + (h - 60) * t
            o += E(xx, yy, 24, 12, wf) + E(xx, yy, 24, 4, lt(wood, 0.3), opacity=0.6)
        # finial
        o += C(xx, top + 6, 22, gold(a)) + P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1fZ" % (xx - 12, top - 10, xx, top - 50, xx, top - 58, xx, top - 50, xx + 12, top - 10), gold(a))
    # top beam
    o += R(x0 - 30, top + 14, w + 60, 30, a.lg([(0, lt(wood, 0.3)), (1, dk(wood, 0.35))]), 12)
    o += R(x0 - 30, top + 22, w + 60, 5, gold(a, False), 2)
    # garland on the beam
    o += garland_flowers(a, x0 + 10, top + 40, cx, top + 44, 36, list(garl), 12, 14, seed=4)
    o += garland_flowers(a, cx, top + 44, x1 - 10, top + 40, 36, list(garl), 12, 14, seed=5)
    # cradle
    cw = w * 0.74
    cb = ybot - h * 0.2
    ch = h * 0.3
    cy_ = cb - ch
    c0, c1 = cx - cw / 2, cx + cw / 2
    for xx in (c0 + 20, c1 - 20):
        o += P("M%.1f,%.1f L%.1f,%.1f" % (xx, top + 44, xx, cy_ + 4), stroke="#C9A24A", stroke_width=5, stroke_dasharray="10 4")
    body = "M%.1f,%.1f L%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f L%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" % (
        c0 - 20, cy_, c1 + 20, cy_, c1 + 10, cy_ + ch * 0.5, c1 - 20, cb, c1 - 50, cb, c0 + 50, cb, c0 + 20, cb, c0 - 10, cy_ + ch * 0.5, c0 - 20, cy_)
    o += E(cx, cy_, cw / 2 + 20, ch * 0.16, dk(wood, 0.4))
    if baby and not photo:
        o += sleeping_baby(a, cx - cw * 0.26, cy_ - ch * 0.36, ch * 0.44)
    o += P(body, wf)
    cp = a.clip(P(body, "#000"))
    inner = R(c0 - 30, cy_ + ch * 0.18, cw + 60, ch * 0.5, a.lg([(0, lt(cloth, 0.3)), (1, dk(cloth, 0.08))]))
    k = 12
    for i in range(k):
        xx = c0 - 20 + (i + 0.5) * (cw + 40) / k
        inner += C(xx, cy_ + ch * 0.68, (cw + 40) / k / 2, lt(cloth, 0.05))
    # spindles
    sp = ""
    for i in range(1, 12):
        xx = c0 + i * cw / 12
        sp += R(xx - 4, cy_ + ch * 0.18, 8, ch * 0.5, gold(a), 4, opacity=0.0)
    o += g(inner + sp, clip_path=cp)
    o += P("M%.1f,%.1f L%.1f,%.1f" % (c0 - 24, cy_, c1 + 24, cy_), stroke=gold(a, False), stroke_width=10, stroke_linecap="round")
    for xx in (c0 - 24, c1 + 24):
        o += C(xx, cy_, 14, gold(a))
    return g(o, filter=a.shadow(14, 10, 0.25))


def lullaby_moon(a, x, y, r, col="#FFE7A3", face=True, rot=-20):
    """crescent moon with a sleeping face; opening to the right."""
    o = C(x, y, r * 1.8, a.rg([(0, col, 0.45), (1, col, 0)]))
    m = a.mask(R(0, 0, 1080, 1350, "#000") + C(x, y, r, "#FFF") + C(x + r * 0.55, y - r * 0.3, r * 0.85, "#000"))
    body = C(x, y, r, a.rg([(0, lt(col, 0.5)), (0.7, col), (1, dk(col, 0.2))], 0.3, 0.4, 0.8))
    body += C(x - r * 0.55, y + r * 0.2, r * 0.1, dk(col, 0.1), opacity=0.5) + C(x - r * 0.35, y + r * 0.6, r * 0.06, dk(col, 0.1), opacity=0.5)
    o += g(body, mask=m)
    if face:
        ex, ey = x - r * 0.52, y - r * 0.05
        o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (ex - r * 0.1, ey, ex, ey + r * 0.09, ex + r * 0.1, ey), stroke=dk(col, 0.55), stroke_width=r * 0.035, stroke_linecap="round")
        o += E(ex - r * 0.02, ey + r * 0.18, r * 0.08, r * 0.05, "#FF9DB0", opacity=0.6)
        o += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (ex + r * 0.02, ey + r * 0.3, ex + r * 0.1, ey + r * 0.34, ex + r * 0.16, ey + r * 0.28), stroke=dk(col, 0.55), stroke_width=r * 0.03, stroke_linecap="round")
    return g(o, "rotate(%s %.1f %.1f)" % (rot, x, y))


def hanging_star(a, x, ytop, ln, r, col, string="#E8D9B0"):
    return P("M%.1f,%.1f L%.1f,%.1f" % (x, ytop, x, ytop + ln), stroke=string, stroke_width=2) + \
        star(x, ytop + ln + r * 0.8, r, a.rg([(0, lt(col, 0.5)), (1, col)]), r2=r * 0.5, stroke=lt(col, 0.6), stroke_width=2, stroke_linejoin="round", filter=a.shadow(4, 3, 0.2))


def rattle(a, x, y, s, ang, col="#F7A8C4", col2="#9ED8C8"):
    o = ""
    o += R(-s * 0.07, 0, s * 0.14, s * 0.9, a.lg([(0, dk(col2, 0.2)), (0.4, lt(col2, 0.4)), (1, dk(col2, 0.2))], 0, 0, 1, 0), s * 0.07)
    o += C(0, s * 0.95, s * 0.14, a.rg([(0, lt(col, 0.4)), (1, col)]))
    o += E(0, s * 0.05, s * 0.2, s * 0.06, gold(a))
    o += C(0, -s * 0.3, s * 0.36, a.rg([(0, lt(col, 0.5)), (0.7, col), (1, dk(col, 0.2))], 0.35, 0.3, 0.8))
    o += E(0, -s * 0.3, s * 0.36, s * 0.09, "none", stroke=gold(a), stroke_width=s * 0.04)
    o += C(-s * 0.12, -s * 0.44, s * 0.06, "#FFFFFF", opacity=0.7)
    o += C(0, -s * 0.3, s * 0.36, "none", stroke=dk(col, 0.15), stroke_width=1.5)
    return g(o, "translate(%.1f %.1f) rotate(%.1f)" % (x, y, ang), filter=a.shadow(6, 5, 0.2))


def stack_rings(a, x, ybot, s, cols=("#F4A6B8", "#FFD58A", "#A8DCC8", "#A9C8F0", "#D6B8F0")):
    o = ""
    o += R(x - s * 0.55, ybot - s * 0.12, s * 1.1, s * 0.12, a.lg([(0, "#E6C08A"), (1, "#B98A4E")]), s * 0.04)
    o += R(x - s * 0.05, ybot - s * 1.25, s * 0.1, s * 1.15, "#D9B27A", s * 0.05)
    yy = ybot - s * 0.12
    for i, c in enumerate(cols):
        rw = s * (0.5 - i * 0.07); rh = s * 0.17
        o += E(x, yy - rh / 2, rw, rh / 2, a.lg([(0, lt(c, 0.35)), (0.5, c), (1, dk(c, 0.2))]))
        yy -= rh * 0.92
    o += C(x, yy - s * 0.08, s * 0.12, a.rg([(0, lt(cols[0], 0.4)), (1, cols[0])]))
    return g(o, filter=a.shadow(6, 5, 0.2))


def toy_block(a, x, y, s, col, emb="star"):
    """3/4 wooden block; embossed shape (no letters)."""
    d = s * 0.28
    o = P(poly([(x, y), (x + d, y - d), (x + s + d, y - d), (x + s, y)]), lt(col, 0.3))
    o += P(poly([(x + s, y), (x + s + d, y - d), (x + s + d, y + s - d), (x + s, y + s)]), dk(col, 0.2))
    o += R(x, y, s, s, a.lg([(0, lt(col, 0.1)), (1, dk(col, 0.05))]))
    o += R(x + s * 0.1, y + s * 0.1, s * 0.8, s * 0.8, "none", s * 0.06, stroke="#FFFFFF", stroke_width=3, opacity=0.8)
    if emb == "star":
        o += star(x + s / 2, y + s / 2, s * 0.25, "#FFFFFF", opacity=0.9)
    elif emb == "heart":
        o += P(heart_path(x + s / 2, y + s * 0.32, s * 0.2), "#FFFFFF", opacity=0.9)
    else:
        o += crescent(a, x + s / 2, y + s / 2, s * 0.22, "#FFFFFF", 0.5)
    return g(o, filter=a.shadow(6, 5, 0.2))


def pastel_sky_clouds(a, cols, seed=1, box=(0, 0, 1080, 1350), n=6, avoid=()):
    rnd = random.Random(seed)
    o = ""
    k = 0
    t = 0
    while k < n and t < 200:
        t += 1
        x = rnd.uniform(box[0], box[2]); y = rnd.uniform(box[1], box[3])
        if inside(x, y, avoid, 60):
            continue
        o += cloud(a, x, y, rnd.uniform(40, 80), rnd.choice(cols), op=rnd.uniform(0.6, 0.95))
        k += 1
    return o
