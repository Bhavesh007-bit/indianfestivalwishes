"""Shared SVG helpers for agent A (navratri, dussehra, good-morning).

Card builder, gradients, filters, textures, panels, generic ornaments.
Event-specific motifs live in gen_<cat>.py.
"""
import math, random, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
W, H = 1080, 1350


def f(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


def pts(p):
    return " ".join("%s,%s" % (f(x), f(y)) for x, y in p)


class Card:
    """Collects <defs> and body markup; hands out unique ids."""

    def __init__(self, seed=1):
        self.defs = []
        self.body = []
        self.n = 0
        self.rnd = random.Random(seed)
        self.defs.append(BASE_FILTERS)

    def uid(self, p="g"):
        self.n += 1
        return "%s%d" % (p, self.n)

    def add(self, *s):
        self.body.extend(s)
        return self

    # ---- gradients ----
    def lg(self, stops, x1=0, y1=0, x2=0, y2=1, user=False, spread=None):
        i = self.uid("lg")
        u = ' gradientUnits="userSpaceOnUse"' if user else ""
        sp = ' spreadMethod="%s"' % spread if spread else ""
        st = "".join(_stop(s) for s in _norm(stops))
        self.defs.append('<linearGradient id="%s" x1="%s" y1="%s" x2="%s" y2="%s"%s%s>%s</linearGradient>'
                         % (i, f(x1), f(y1), f(x2), f(y2), u, sp, st))
        return "url(#%s)" % i

    def rg(self, stops, cx=0.5, cy=0.5, r=0.5, fx=None, fy=None, user=False):
        i = self.uid("rg")
        u = ' gradientUnits="userSpaceOnUse"' if user else ""
        fxy = ""
        if fx is not None:
            fxy = ' fx="%s" fy="%s"' % (f(fx), f(fy))
        st = "".join(_stop(s) for s in _norm(stops))
        self.defs.append('<radialGradient id="%s" cx="%s" cy="%s" r="%s"%s%s>%s</radialGradient>'
                         % (i, f(cx), f(cy), f(r), fxy, u, st))
        return "url(#%s)" % i

    def clip(self, inner):
        i = self.uid("cp")
        self.defs.append('<clipPath id="%s">%s</clipPath>' % (i, inner))
        return "url(#%s)" % i

    def pattern(self, w, h, inner, transform=None):
        i = self.uid("pt")
        t = ' patternTransform="%s"' % transform if transform else ""
        self.defs.append('<pattern id="%s" width="%s" height="%s" patternUnits="userSpaceOnUse"%s>%s</pattern>'
                         % (i, f(w), f(h), t, inner))
        return "url(#%s)" % i

    def blur(self, sd):
        i = self.uid("bl")
        self.defs.append('<filter id="%s" x="-50%%" y="-50%%" width="200%%" height="200%%"><feGaussianBlur stdDeviation="%s"/></filter>' % (i, f(sd)))
        return "url(#%s)" % i

    def shadow(self, dy=10, sd=14, op=0.35, color="#000"):
        i = self.uid("sh")
        self.defs.append('<filter id="%s" x="-30%%" y="-30%%" width="160%%" height="170%%"><feDropShadow dx="0" dy="%s" stdDeviation="%s" flood-color="%s" flood-opacity="%s"/></filter>'
                         % (i, f(dy), f(sd), color, f(op)))
        return "url(#%s)" % i

    def glow(self, sd=8, color="#FFD36B", op=0.9):
        i = self.uid("gw")
        self.defs.append(
            '<filter id="%s" x="-80%%" y="-80%%" width="260%%" height="260%%"><feGaussianBlur in="SourceGraphic" stdDeviation="%s" result="b"/>'
            '<feFlood flood-color="%s" flood-opacity="%s"/><feComposite in2="b" operator="in" result="c"/>'
            '<feMerge><feMergeNode in="c"/><feMergeNode in="c"/><feMergeNode in="SourceGraphic"/></feMerge></filter>' % (i, f(sd), color, f(op)))
        return "url(#%s)" % i

    def svg(self):
        return ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%d" height="%d" viewBox="0 0 %d %d">'
                '<defs>%s</defs>%s</svg>') % (W, H, W, H, "".join(self.defs), "".join(self.body))


def _norm(stops):
    out = []
    n = len(stops)
    for k, s in enumerate(stops):
        if isinstance(s, str):
            out.append((k / max(1, n - 1), s, 1))
        elif len(s) == 2:
            out.append((s[0], s[1], 1))
        else:
            out.append(s)
    return out


def _stop(s):
    o, c, a = s
    return '<stop offset="%s" stop-color="%s"%s/>' % (f(o), c, "" if a == 1 else ' stop-opacity="%s"' % f(a))


BASE_FILTERS = (
    '<filter id="grain" x="0" y="0" width="100%" height="100%">'
    '<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" stitchTiles="stitch"/>'
    '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.55 0"/></filter>'
    '<filter id="paper" x="0" y="0" width="100%" height="100%">'
    '<feTurbulence type="fractalNoise" baseFrequency="0.018 0.03" numOctaves="4" seed="3"/>'
    '<feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.3  0 0 0 0 0.1  0 0 0 0.9 0"/></filter>'
)


def grain(op=0.07, x=0, y=0, w=W, h=H):
    return '<rect x="%d" y="%d" width="%d" height="%d" filter="url(#grain)" opacity="%s"/>' % (x, y, w, h, f(op))


# ---------------------------------------------------------------- colours
GOLD = ["#8A5A12", "#E9B949", "#FFF1B8", "#D9A23A", "#9C6516"]
GOLD2 = [(0, "#7A4B0C"), (0.3, "#D69A2D"), (0.5, "#FFE9A6"), (0.7, "#C98A22"), (1, "#7A4B0C")]


def gold(c, vertical=False):
    return c.lg(GOLD2, 0, 0, 0, 1) if vertical else c.lg(GOLD2, 0, 0, 1, 1)


# ---------------------------------------------------------------- shapes
def rr(x, y, w, h, r):
    return "M%s,%s h%s a%s,%s 0 0 1 %s,%s v%s a%s,%s 0 0 1 %s,%s h%s a%s,%s 0 0 1 %s,%s v%s a%s,%s 0 0 1 %s,%s z" % (
        f(x + r), f(y), f(w - 2 * r), f(r), f(r), f(r), f(r), f(h - 2 * r), f(r), f(r), f(-r), f(r),
        f(-(w - 2 * r)), f(r), f(r), f(-r), f(-r), f(-(h - 2 * r)), f(r), f(r), f(r), f(-r))


def arch_path(x, y, w, h, rise=None):
    """Round-top arch (semicircle top)."""
    r = w / 2
    return "M%s,%s V%s A%s,%s 0 0 1 %s,%s V%s Z" % (f(x), f(y + h), f(y + r), f(r), f(r), f(x + w), f(y + r), f(y + h))


def ogee_arch(x, y, w, h):
    """Pointed/ogee arch top panel."""
    cx = x + w / 2
    sh = y + w * 0.42
    return ("M%s,%s V%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s V%s Z" % (
        f(x), f(y + h), f(sh), f(x), f(sh - w * 0.28), f(cx - w * 0.2), f(y + w * 0.08), f(cx), f(y),
        f(cx + w * 0.2), f(y + w * 0.08), f(x + w), f(sh - w * 0.28), f(x + w), f(sh), f(y + h)))


def star(cx, cy, r1, r2, n=5, rot=-90):
    p = []
    for i in range(n * 2):
        a = math.radians(rot + i * 180 / n)
        r = r1 if i % 2 == 0 else r2
        p.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return "M" + " L".join("%s,%s" % (f(a), f(b)) for a, b in p) + "Z"


def sparkle(cx, cy, r, fill="#FFF6D2", op=1):
    """4-point twinkle."""
    k = r * 0.18
    d = "M%s,%s Q%s,%s %s,%s Q%s,%s %s,%s Q%s,%s %s,%s Q%s,%s %s,%s Z" % (
        f(cx), f(cy - r), f(cx + k), f(cy - k), f(cx + r), f(cy), f(cx + k), f(cy + k), f(cx), f(cy + r),
        f(cx - k), f(cy + k), f(cx - r), f(cy), f(cx - k), f(cy - k), f(cx), f(cy - r))
    return '<path d="%s" fill="%s" opacity="%s"/>' % (d, fill, f(op))


def bokeh(c, n, box, colors, rmin=6, rmax=34, op=(0.12, 0.45), blur=True):
    x0, y0, x1, y1 = box
    out = []
    bl = c.blur(2.5) if blur else None
    for _ in range(n):
        x = c.rnd.uniform(x0, x1); y = c.rnd.uniform(y0, y1)
        r = c.rnd.uniform(rmin, rmax)
        col = c.rnd.choice(colors)
        o = c.rnd.uniform(*op)
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"%s/>' % (
            f(x), f(y), f(r), col, f(o), ' filter="%s"' % bl if bl and r > 12 else ""))
    return "".join(out)


def rays(cx, cy, n, r, color, op=0.12, width=0.5, rot=0):
    """Soft light rays: alternating wedges."""
    out = []
    step = 360 / n
    for i in range(n):
        a0 = math.radians(rot + i * step)
        a1 = math.radians(rot + i * step + step * width)
        out.append("M%s,%s L%s,%s L%s,%s Z" % (f(cx), f(cy), f(cx + r * math.cos(a0)), f(cy + r * math.sin(a0)),
                                              f(cx + r * math.cos(a1)), f(cy + r * math.sin(a1))))
    return '<path d="%s" fill="%s" opacity="%s"/>' % (" ".join(out), color, f(op))


# ---------------------------------------------------------------- panels
def panel(c, x, y, w, h, r=36, fill=("#FFFBF1", "#F6E9CF"), stroke="#C9A25A", inner=True, shadow=True,
          op=1, texture=True, path=None, sw=3):
    """Calm text plaque with soft shadow, optional inner rule and paper texture."""
    d = path or rr(x, y, w, h, r)
    g = c.lg([fill[0], fill[1]], 0, 0, 0, 1) if isinstance(fill, (tuple, list)) else fill
    out = []
    sh = c.shadow(14, 22, 0.35) if shadow else None
    out.append('<path d="%s" fill="%s" opacity="%s"%s/>' % (d, g, f(op), ' filter="%s"' % sh if sh else ""))
    if texture:
        cp = c.clip('<path d="%s"/>' % d)
        out.append('<g clip-path="%s"><rect x="%s" y="%s" width="%s" height="%s" filter="url(#paper)" opacity="0.10"/></g>'
                   % (cp, f(x), f(y), f(w), f(h)))
    if stroke:
        out.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (d, stroke, f(sw)))
    if inner and not path:
        out.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.5" opacity="0.7"/>' % (rr(x + 14, y + 14, w - 28, h - 28, max(4, r - 12)), stroke))
    return "".join(out)


def corner_flourish(x, y, s, color, rot=0, op=1):
    """Ornamental corner scroll (generic filigree), anchored at the corner point."""
    d = ("M0,0 C40,0 70,10 90,34 C100,48 96,66 82,70 C68,74 60,60 68,52 C74,46 84,50 82,58 "
         "M0,0 C0,40 10,70 34,90 C48,100 66,96 70,82 C74,68 60,60 52,68 C46,74 50,84 58,82 "
         "M0,0 C30,18 44,30 52,52 M18,6 C36,6 50,12 58,22 M6,18 C6,36 12,50 22,58")
    return ('<g transform="translate(%s,%s) rotate(%s) scale(%s)" opacity="%s"><path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"/>'
            '<circle cx="0" cy="0" r="7" fill="%s"/><circle cx="100" cy="100" r="0"/></g>') % (
        f(x), f(y), f(rot), f(s), f(op), d, color, f(3 / s), color)


def corners(x0, y0, x1, y1, s, color, op=1):
    return (corner_flourish(x0, y0, s, color, 0, op) + corner_flourish(x1, y0, s, color, 90, op)
            + corner_flourish(x1, y1, s, color, 180, op) + corner_flourish(x0, y1, s, color, 270, op))


def dotted_line(x0, y0, x1, y1, gap, r, color, op=1):
    n = int(math.hypot(x1 - x0, y1 - y0) / gap)
    out = []
    for i in range(n + 1):
        t = i / max(1, n)
        out.append('<circle cx="%s" cy="%s" r="%s"/>' % (f(x0 + (x1 - x0) * t), f(y0 + (y1 - y0) * t), f(r)))
    return '<g fill="%s" opacity="%s">%s</g>' % (color, f(op), "".join(out))


def watermark_calm(c, color, op=0.85):
    """Soft calm fade behind the engine's watermark pill (x 330-750, y 1275-1350)."""
    g = c.rg([(0, color, op), (1, color, 0)], 0.5, 0.5, 0.5)
    return '<ellipse cx="540" cy="1318" rx="300" ry="62" fill="%s"/>' % g


# ---------------------------------------------------------------- output
def _lum(h):
    h = h.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    fx = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * fx(r) + 0.7152 * fx(g) + 0.0722 * fx(b)


def contrast(a, b):
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def ensure_contrast(col, bg, target=4.5):
    """Darken (light bg) or lighten (dark bg) col until it reaches the target contrast ratio."""
    h = col.lstrip("#")
    rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    dark_bg = _lum(bg) < 0.2
    for _ in range(60):
        cur = "#%02X%02X%02X" % tuple(rgb)
        if contrast(cur, bg) >= target:
            return cur
        rgb = [min(255, int(v + (255 - v) * 0.08 + 1)) if dark_bg else max(0, int(v * 0.93)) for v in rgb]
    return "#%02X%02X%02X" % tuple(rgb)


def write_spec(cat, specs):
    for s in specs:
        bg = "#FFF6E6" if s["tone"] == "light" else "#1E1028"
        for k in ("title", "text", "accent"):
            v = s["colors"][k]
            if v != "gold":
                nv = ensure_contrast(v, bg)
                if nv != v:
                    print("  contrast fix %s %s: %s -> %s" % (s["id"], k, v, nv))
                s["colors"][k] = nv
    p = os.path.join(HERE, "out", cat + ".json")
    json.dump(specs, open(p, "w"), ensure_ascii=False, indent=1)
    print("wrote", p)


def spec(cid, zone, title, text, accent, tone="light", tstyle="deco", align="center", photo=None):
    s = {"id": cid, "tpl": True, "zone": list(zone), "colors": {"title": title, "text": text, "accent": accent},
         "tone": tone, "title": tstyle, "align": align}
    if photo:
        s["photo"] = photo
        s["slot"] = True
    return s


def panel_for(zone, pad=48):
    x0, y0, x1, y1 = zone
    return x0 - pad, y0 - pad, x1 - x0 + 2 * pad, y1 - y0 + 2 * pad


# ---------------------------------------------------------------- extra panels / frames (v2)
def cut_corner(x, y, w, h, k):
    return "M%s,%s H%s L%s,%s V%s L%s,%s H%s L%s,%s V%s Z" % (
        f(x + k), f(y), f(x + w - k), f(x + w), f(y + k), f(y + h - k), f(x + w - k), f(y + h), f(x + k), f(x), f(y + h - k), f(y + k))


def scroll_panel(c, x, y, w, h, paper=("#FFF6E0", "#F1DDB2"), roll=("#E7C98E", "#9C6B2E"), edge="#B7862F", rolls="h"):
    """Parchment scroll: flat sheet with rolled cylinders at top and bottom (rolls='v') or left/right ('h')."""
    out = []
    sh = c.shadow(12, 18, 0.35)
    out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" filter="%s"/>' % (f(x), f(y), f(w), f(h), c.lg([paper[0], paper[1]], 0, 0, 0, 1), sh))
    cp = c.clip('<rect x="%s" y="%s" width="%s" height="%s"/>' % (f(x), f(y), f(w), f(h)))
    out.append('<g clip-path="%s"><rect x="%s" y="%s" width="%s" height="%s" filter="url(#paper)" opacity="0.13"/>' % (cp, f(x), f(y), f(w), f(h)))
    out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/></g>' % (f(x), f(y), f(w), f(h), c.rg([(0, "#fff", 0), (0.7, "#fff", 0), (1, "#8A5A12", 0.18)])))
    out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="2" opacity="0.8"/>' % (f(x + 18), f(y + 18), f(w - 36), f(h - 36), edge))
    rg = lambda vert: c.lg([(0, roll[1]), (0.35, roll[0]), (0.55, "#FFF3D0"), (0.75, roll[0]), (1, roll[1])], 0, 0, 0, 1) if vert else c.lg([(0, roll[1]), (0.35, roll[0]), (0.55, "#FFF3D0"), (0.75, roll[0]), (1, roll[1])], 0, 0, 1, 0)
    R = 26
    if rolls == "v":
        for yy in (y - R, y + h - R):
            out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" filter="%s"/>' % (f(x - 30), f(yy), f(w + 60), f(2 * R), f(R), rg(True), c.shadow(6, 8, 0.3)))
            for ex in (x - 30, x + w + 30):
                out.append('<ellipse cx="%s" cy="%s" rx="10" ry="%s" fill="%s"/>' % (f(ex), f(yy + R), f(R), roll[1]))
                out.append('<ellipse cx="%s" cy="%s" rx="5" ry="%s" fill="#5A3A12"/>' % (f(ex), f(yy + R), f(R * 0.5)))
    else:
        for xx in (x - R, x + w - R):
            out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" filter="%s"/>' % (f(xx), f(y - 30), f(2 * R), f(h + 60), f(R), rg(False), c.shadow(6, 8, 0.3)))
            for ey in (y - 30, y + h + 30):
                out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="10" fill="%s"/>' % (f(xx + R), f(ey), f(R), roll[1]))
                out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="5" fill="#5A3A12"/>' % (f(xx + R), f(ey), f(R * 0.5)))
    return "".join(out)


def torn_edge(x0, x1, y, amp, step, rnd, down=True):
    """Points for a torn-paper edge from x0 to x1 around y."""
    p = []
    x = x0
    while x < x1:
        p.append((x, y + rnd.uniform(-amp, amp)))
        x += rnd.uniform(step * 0.5, step * 1.4)
    p.append((x1, y))
    return p


def glass_panel(c, x, y, w, h, r=34, tint="#140A1E", op=0.72, stroke="#E9B949", sw=2.5, blur_bg=True):
    out = []
    d = rr(x, y, w, h, r)
    out.append('<path d="%s" fill="%s" opacity="%s" filter="%s"/>' % (d, tint, f(op), c.shadow(16, 26, 0.45)))
    out.append('<path d="%s" fill="%s"/>' % (d, c.lg([(0, "#FFFFFF", 0.10), (0.35, "#FFFFFF", 0.02), (1, "#FFFFFF", 0)], 0, 0, 1, 1)))
    out.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (d, stroke, f(sw)))
    out.append('<path d="%s" fill="none" stroke="%s" stroke-width="1" opacity="0.5"/>' % (rr(x + 12, y + 12, w - 24, h - 24, max(6, r - 10)), stroke))
    return "".join(out)


def gold_frame(c, inset=26, sw=6, color=None, corner_s=1.0, inner=True, corner_color=None):
    """Card-wide ornamental gold frame: double rule + filigree corner pieces with a gem."""
    g = color or gold(c)
    cc = corner_color or g
    x0, y0, x1, y1 = inset, inset, W - inset, H - inset
    out = ['<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (f(x0), f(y0), f(x1 - x0), f(y1 - y0), g, f(sw))]
    if inner:
        out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="1.8"/>' % (f(x0 + 14), f(y0 + 14), f(x1 - x0 - 28), f(y1 - y0 - 28), g))
    for (cx, cy, rot) in ((x0, y0, 0), (x1, y0, 90), (x1, y1, 180), (x0, y1, 270)):
        out.append('<g transform="translate(%s,%s) rotate(%s) scale(%s)">' % (f(cx), f(cy), rot, f(corner_s)))
        out.append('<path d="M-6,-6 H110 C84,4 64,10 50,24 C38,36 30,56 24,84 C18,60 14,40 -6,110 Z" fill="%s"/>' % cc)
        out.append('<path d="M14,14 C60,14 88,30 100,56 C80,40 58,34 40,40 C34,58 40,80 56,100 C30,88 14,60 14,14 Z" fill="%s" opacity="0.85"/>' % cc)
        out.append('<circle cx="30" cy="30" r="9" fill="#B71C1C" stroke="#FFE7A0" stroke-width="3"/>')
        out.append('<path d="M120,6 q14,10 28,0 M6,120 q10,14 0,28" stroke="%s" stroke-width="4" fill="none"/>' % cc)
        out.append('</g>')
    return "".join(out)


def damask(c, bg, fg, op=0.12, s=120):
    """Subtle damask/buti repeat pattern (generic ornament, paisley-free)."""
    inner = ('<rect width="%s" height="%s" fill="%s"/>' % (f(s), f(s), bg) +
             '<g fill="%s" opacity="%s">' % (fg, f(op)) +
             '<path d="M%s,%s c%s,%s %s,%s 0,%s c%s,%s %s,%s 0,%s Z"/>' % (f(s / 2), f(s * 0.18), f(s * 0.2), f(s * 0.12), f(s * 0.2), f(s * 0.52), f(s * 0.64), f(-s * 0.2), f(-s * 0.12), f(-s * 0.2), f(-s * 0.52), f(-s * 0.64)) +
             '<circle cx="0" cy="0" r="%s"/><circle cx="%s" cy="0" r="%s"/><circle cx="0" cy="%s" r="%s"/><circle cx="%s" cy="%s" r="%s"/>' % (
                 f(s * 0.06), f(s), f(s * 0.06), f(s), f(s * 0.06), f(s), f(s), f(s * 0.06)) + '</g>')
    return c.pattern(s, s, inner)
