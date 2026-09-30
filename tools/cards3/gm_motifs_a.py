"""Good-morning motifs (agent A): sunrise sun, layered hills, sea, birds, tea cup + steam, mug,
dewy leaves, sunflowers, morning-glory, window with sunlight, sparrow on branch, clouds."""
import math
from lib_a import f, pts, rr, sparkle, W, H


# ------------------------------------------------------------------ sky
def sun(c, cx, cy, r, core=("#FFFDE7", "#FFE082", "#FFB300"), halo="#FFD180", halo_r=3.2, rays_n=0, rays_col="#FFF3C4", rays_op=0.18):
    out = []
    out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(r * halo_r), c.rg([(0, halo, 0.75), (0.35, halo, 0.3), (1, halo, 0)])))
    if rays_n:
        L = r * 9
        step = 360.0 / rays_n
        d = []
        for i in range(rays_n):
            a0 = math.radians(i * step); a1 = math.radians(i * step + step * 0.42)
            d.append("M%s,%s L%s,%s L%s,%s Z" % (f(cx), f(cy), f(cx + L * math.cos(a0)), f(cy + L * math.sin(a0)), f(cx + L * math.cos(a1)), f(cy + L * math.sin(a1))))
        out.append('<path d="%s" fill="%s" opacity="%s" filter="%s"/>' % (" ".join(d), c.rg([(0, rays_col, 1), (1, rays_col, 0)], 0.5, 0.5, 0.5, user=False), f(rays_op), c.blur(3)))
    out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(r * 1.25), c.rg([(0, core[0], 0.9), (1, core[1], 0)])))
    out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(r), c.rg([(0, core[0]), (0.55, core[1]), (1, core[2])], 0.45, 0.4, 0.6)))
    return "".join(out)


def cloud(c, cx, cy, s=1.0, color="#FFFFFF", shade="#F8C9B8", op=0.9):
    """Soft cumulus cloud with lit top and tinted underside."""
    blobs = [(-90, 10, 50), (-40, -18, 62), (20, -30, 72), (80, -8, 56), (130, 14, 40), (-130, 22, 34), (0, 12, 60), (50, 14, 50), (-60, 18, 44)]
    g = c.lg([(0, color), (0.55, color), (1, shade)], 0, cy - 110 * s, 0, cy + 60 * s, user=True)
    circ = "".join('<circle cx="%s" cy="%s" r="%s"/>' % (f(cx + x * s), f(cy + y * s), f(r * s)) for x, y, r in blobs)
    base = '<rect x="%s" y="%s" width="%s" height="%s" rx="%s"/>' % (f(cx - 150 * s), f(cy + 4 * s), f(300 * s), f(50 * s), f(25 * s))
    return '<g opacity="%s" filter="%s" fill="%s">%s%s</g>' % (f(op), c.blur(2.5 * s), g, circ, base)


def hills(c, layers, x0=0, x1=W, bottom=H):
    """layers: list of (base_y, amplitude, (top_colour, bottom_colour), seed_phase, n_bumps). Drawn back to front with mist."""
    out = []
    for k, (y, amp, cols, ph, nb) in enumerate(layers):
        p = []
        N = 60
        for i in range(N + 1):
            t = i / N
            x = x0 + (x1 - x0) * t
            v = (math.sin(t * math.pi * nb + ph) * 0.6 + math.sin(t * math.pi * nb * 2.3 + ph * 1.7) * 0.25 + math.sin(t * math.pi * nb * 0.5 + ph * 0.3) * 0.4)
            p.append((x, y - amp * v))
        d = "M%s,%s L%s L%s,%s Z" % (f(x0), f(bottom), pts(p), f(x1), f(bottom))
        out.append('<path d="%s" fill="%s"/>' % (d, c.lg([cols[0], cols[1]], 0, 0, 0, 1)))
        # rim light on ridge
        out.append('<polyline points="%s" fill="none" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="2"/>' % pts(p))
        if k < len(layers) - 1:
            out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (
                f(x0), f(y - amp * 0.2), f(x1 - x0), f(amp * 1.6 + 60),
                c.lg([(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 0.28), (1, "#FFFFFF", 0)], 0, 0, 0, 1)))
    return "".join(out)


def sea(c, horizon, x0, x1, bottom, top_col="#F6B38E", bot_col="#2F5D8A", sun_x=540, glint="#FFE7A8"):
    out = ['<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (f(x0), f(horizon), f(x1 - x0), f(bottom - horizon), c.lg([top_col, bot_col], 0, 0, 0, 1))]
    rnd = c.rnd
    # sun glitter path
    for i in range(70):
        t = (i / 70.0) ** 1.6
        y = horizon + 6 + (bottom - horizon) * t
        w = 20 + 260 * t * rnd.uniform(0.4, 1.0)
        x = sun_x + rnd.uniform(-1, 1) * (30 + 180 * t)
        out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="2" fill="%s" opacity="%s"/>' % (
            f(x - w / 2), f(y), f(w), f(2 + 5 * t), glint, f(rnd.uniform(0.35, 0.9) * (1 - t * 0.5))))
    # wave lines
    for i in range(26):
        t = rnd.random() ** 1.5
        y = horizon + 10 + (bottom - horizon) * t
        x = rnd.uniform(x0, x1)
        w = 40 + 200 * t
        out.append('<path d="M%s,%s q%s,%s %s,0" stroke="#FFFFFF" stroke-opacity="%s" stroke-width="%s" fill="none"/>' % (
            f(x), f(y), f(w / 2), f(-3 - 4 * t), f(w), f(0.12 + 0.1 * t), f(1 + 2 * t)))
    out.append('<rect x="%s" y="%s" width="%s" height="8" fill="%s"/>' % (f(x0), f(horizon - 4), f(x1 - x0), c.lg([(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 0.6), (1, "#FFFFFF", 0)], 0, 0, 1, 0)))
    return "".join(out)


def bird(x, y, s, color="#2B2B3A", flap=0.0, rot=0):
    """Flying bird (gull style), centre (x,y). flap -1..1 changes wing angle."""
    up = 24 + flap * 14
    d = ("M0,0 C-14,%s -34,%s -58,%s C-40,%s -22,%s -6,6 L0,10 L6,6 C22,%s 40,%s 58,%s C34,%s 14,%s 0,0 Z" % (
        f(-up * 0.6), f(-up), f(-up * 0.55), f(-up * 0.8), f(-up * 0.2), f(-up * 0.2), f(-up * 0.8), f(-up * 0.55), f(-up), f(-up * 0.6)))
    return '<path d="%s" fill="%s" transform="translate(%s,%s) rotate(%s) scale(%s)"/>' % (d, color, f(x), f(y), f(rot), f(s))


def flock(c, x, y, n, spread, color="#3B2F45", smin=0.35, smax=0.8):
    out = []
    for i in range(n):
        bx = x + c.rnd.uniform(-spread, spread)
        by = y + c.rnd.uniform(-spread * 0.45, spread * 0.45)
        out.append(bird(bx, by, c.rnd.uniform(smin, smax), color, c.rnd.uniform(-1, 1), c.rnd.uniform(-12, 12)))
    return "".join(out)


# ------------------------------------------------------------------ tea
def steam(c, cx, top, h, n=3, color="#FFFFFF", op=0.7, w=22):
    out = []
    bl = c.blur(2.4)
    for i in range(n):
        x = cx + (i - (n - 1) / 2) * w * 1.5
        d = "M%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s" % (
            f(x), f(top), f(x - w), f(top - h * 0.2), f(x + w), f(top - h * 0.4), f(x), f(top - h * 0.55),
            f(x - w), f(top - h * 0.7), f(x + w * 0.8), f(top - h * 0.85), f(x - w * 0.2), f(top - h))
        g = c.lg([(0, color, 0), (0.25, color, op), (1, color, 0)], 0, 1, 0, 0)
        out.append('<path d="%s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round" filter="%s"/>' % (d, g, f(w * 0.45), bl))
    return "".join(out)


def teacup(c, cx, cy, s=1.0, body=("#FFFFFF", "#D9E2EC"), band="#2E7D6B", accent="#E0A526", tea=("#C1703A", "#7A3B12"), saucer=True, steam_on=True):
    """Porcelain teacup on saucer (3/4 view), rim centre at (cx,cy). ~420*s wide with saucer."""
    out = ['<g transform="translate(%s,%s) scale(%s)">' % (f(cx), f(cy), f(s))]
    bg = c.lg([(0, body[1]), (0.25, body[0]), (0.55, body[0]), (1, body[1])], 0, 0, 1, 0)
    if saucer:
        out.append('<ellipse cx="0" cy="198" rx="230" ry="46" fill="#000" opacity="0.18" filter="%s"/>' % c.blur(8))
        out.append('<ellipse cx="0" cy="184" rx="220" ry="50" fill="%s"/>' % c.lg([body[0], body[1]], 0, 0, 0, 1))
        out.append('<ellipse cx="0" cy="178" rx="210" ry="42" fill="%s"/>' % bg)
        out.append('<ellipse cx="0" cy="178" rx="196" ry="36" fill="none" stroke="%s" stroke-width="5"/>' % accent)
        out.append('<ellipse cx="0" cy="176" rx="120" ry="20" fill="%s"/>' % c.lg([body[1], body[0]], 0, 0, 0, 1))
    # handle
    out.append('<path d="M128,20 C210,10 214,110 120,120" stroke="%s" stroke-width="26" fill="none" stroke-linecap="round"/>' % body[1])
    out.append('<path d="M128,20 C200,14 204,104 120,114" stroke="%s" stroke-width="16" fill="none" stroke-linecap="round"/>' % body[0])
    out.append('<path d="M132,36 C178,34 184,92 128,100" stroke="%s" stroke-width="3" fill="none"/>' % accent)
    # cup body
    cup = "M-150,0 C-150,90 -110,170 0,176 C110,170 150,90 150,0 Z"
    out.append('<path d="%s" fill="%s"/>' % (cup, bg))
    # decorative band + floral dots
    cp = c.clip('<path d="%s"/>' % cup)
    out.append('<g clip-path="%s">' % cp)
    out.append('<path d="M-160,40 C-60,70 60,70 160,40 L160,72 C60,102 -60,102 -160,72 Z" fill="%s"/>' % band)
    for k in range(-5, 6):
        x = k * 26
        y = 70 - abs(k) * 1.5 + 2
        out.append('<circle cx="%s" cy="%s" r="7" fill="%s"/><circle cx="%s" cy="%s" r="3" fill="#FFFFFF"/>' % (f(x), f(y), accent, f(x), f(y)))
    out.append('<path d="M-160,34 C-60,64 60,64 160,34" stroke="%s" stroke-width="4" fill="none"/>' % accent)
    out.append('<path d="M-160,80 C-60,110 60,110 160,80" stroke="%s" stroke-width="4" fill="none"/>' % accent)
    out.append('<ellipse cx="-80" cy="70" rx="26" ry="80" fill="#FFFFFF" opacity="0.45"/>')
    out.append('</g>')
    # rim + tea
    out.append('<ellipse cx="0" cy="0" rx="150" ry="36" fill="%s"/>' % c.lg([body[1], body[0]], 0, 0, 0, 1))
    out.append('<ellipse cx="0" cy="3" rx="136" ry="29" fill="%s"/>' % c.rg([(0, tea[0]), (1, tea[1])], 0.5, 0.4, 0.6))
    out.append('<ellipse cx="-30" cy="-2" rx="50" ry="8" fill="#FFFFFF" opacity="0.25"/>')
    out.append('<ellipse cx="0" cy="0" rx="150" ry="36" fill="none" stroke="%s" stroke-width="4"/>' % accent)
    out.append("</g>")
    if steam_on:
        out.append(steam(c, cx, cy - 20 * s, 220 * s, 3, w=26 * s))
    return "".join(out)


def mug(c, cx, cy, s=1.0, body=("#F48FB1", "#C2185B"), inner="#5D3A1A", heart=True, steam_on=True):
    """Coffee mug (straight sides) with latte heart; rim centre at (cx,cy). ~300*s wide."""
    out = ['<g transform="translate(%s,%s) scale(%s)">' % (f(cx), f(cy), f(s))]
    out.append('<ellipse cx="0" cy="262" rx="160" ry="24" fill="#000" opacity="0.2" filter="%s"/>' % c.blur(8))
    out.append('<path d="M100,50 C190,40 200,170 96,190" stroke="%s" stroke-width="34" fill="none" stroke-linecap="round"/>' % body[1])
    out.append('<path d="M100,56 C176,50 184,164 96,180" stroke="%s" stroke-width="18" fill="none" stroke-linecap="round"/>' % body[0])
    bd = "M-120,0 L-112,236 C-110,262 110,262 112,236 L120,0 Z"
    out.append('<path d="%s" fill="%s"/>' % (bd, c.lg([(0, body[1]), (0.3, body[0]), (0.6, body[0]), (1, body[1])], 0, 0, 1, 0)))
    out.append('<path d="M-80,30 L-76,220" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="18" stroke-linecap="round"/>')
    out.append('<ellipse cx="0" cy="0" rx="120" ry="28" fill="%s"/>' % body[0])
    out.append('<ellipse cx="0" cy="3" rx="106" ry="21" fill="%s"/>' % c.rg([(0, "#E8C39E"), (0.6, "#B07A4A"), (1, inner)], 0.5, 0.5, 0.55))
    if heart:
        out.append('<path d="M0,14 C-26,2 -30,-10 -18,-12 C-10,-13 -4,-8 0,-3 C4,-8 10,-13 18,-12 C30,-10 26,2 0,14 Z" fill="#FFF3E0"/>')
    out.append("</g>")
    if steam_on:
        out.append(steam(c, cx, cy - 16 * s, 200 * s, 3, w=22 * s))
    return "".join(out)


# ------------------------------------------------------------------ plants
def dew(x, y, r, op=0.95):
    return ('<g opacity="%s"><ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#000" opacity="0.12"/>'
            '<circle cx="%s" cy="%s" r="%s" fill="#FFFFFF" fill-opacity="0.28" stroke="#FFFFFF" stroke-opacity="0.7" stroke-width="%s"/>'
            '<circle cx="%s" cy="%s" r="%s" fill="#FFFFFF"/><path d="M%s,%s a%s,%s 0 0 0 %s,%s" stroke="#FFFFFF" stroke-width="%s" fill="none" opacity="0.8"/></g>') % (
        f(op), f(x + r * 0.3), f(y + r * 0.6), f(r * 0.9), f(r * 0.45), f(x), f(y), f(r), f(max(0.8, r * 0.1)),
        f(x - r * 0.35), f(y - r * 0.35), f(r * 0.25), f(x - r * 0.6), f(y + r * 0.2), f(r * 0.7), f(r * 0.7), f(r * 1.0), f(r * 0.5), f(max(0.8, r * 0.12)))


def leaf(c, x, y, L, rot=0, cols=("#9CCC65", "#33691E"), wmul=0.36, vein="#DCEDC8", drops=3, curl=0.0):
    """Big glossy leaf with midrib, side veins and dew drops. Base at (x,y), pointing up (rot deg)."""
    w = L * wmul
    out = ['<g transform="translate(%s,%s) rotate(%s)">' % (f(x), f(y), f(rot))]
    d = "M0,0 C%s,%s %s,%s %s,%s C%s,%s %s,%s 0,0 Z" % (
        f(-w * 1.1), f(-L * 0.25), f(-w * 0.9 + curl * L * 0.2), f(-L * 0.8), f(curl * L * 0.3), f(-L),
        f(w * 0.9 + curl * L * 0.2), f(-L * 0.8), f(w * 1.1), f(-L * 0.25))
    out.append('<path d="%s" fill="%s"/>' % (d, c.lg([(0, cols[0]), (1, cols[1])], 0, 0, 1, 1)))
    out.append('<path d="%s" fill="%s"/>' % (d, c.lg([(0, "#FFFFFF", 0.0), (0.45, "#FFFFFF", 0.0), (0.5, "#000000", 0.14), (1, "#000000", 0.2)], 0, 0, 1, 0)))
    lcp = c.clip('<path d="%s"/>' % d)
    out.append('<g clip-path="%s">' % lcp)
    mid = "M0,0 C%s,%s %s,%s %s,%s" % (f(curl * L * 0.05), f(-L * 0.4), f(curl * L * 0.2), f(-L * 0.75), f(curl * L * 0.3), f(-L * 0.98))
    out.append('<path d="%s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round" opacity="0.9"/>' % (mid, vein, f(max(1.5, L * 0.012))))
    for i in range(1, 8):
        t = i / 8.5
        yy = -L * t
        mx = curl * L * 0.3 * t * t
        ww = w * math.sin(math.pi * (t * 0.85 + 0.1)) * 0.9
        for sx in (-1, 1):
            out.append('<path d="M%s,%s Q%s,%s %s,%s" stroke="%s" stroke-width="%s" fill="none" opacity="0.6"/>' % (
                f(mx), f(yy), f(mx + sx * ww * 0.5), f(yy - L * 0.03), f(mx + sx * ww), f(yy - L * 0.09), vein, f(max(1, L * 0.006))))
    out.append("</g>")
    rnd = c.rnd
    for k in range(drops):
        t = rnd.uniform(0.2, 0.8)
        out.append(dew(rnd.uniform(-w * 0.4, w * 0.4) + curl * L * 0.3 * t * t, -L * t, rnd.uniform(L * 0.015, L * 0.04)))
    out.append("</g>")
    return "".join(out)


def sunflower(c, cx, cy, r, rot=0, tilt=1.0, petals=("#FFD54F", "#F9A825", "#E65100"), center=("#6D4C1F", "#2E1A08")):
    """Face-on sunflower: two petal rings with gradient, fermat-spiral seed head. tilt<1 squashes vertically."""
    out = ['<g transform="translate(%s,%s) rotate(%s) scale(1,%s)">' % (f(cx), f(cy), f(rot), f(tilt))]
    pg = c.lg([(0, petals[2]), (0.35, petals[1]), (1, petals[0])], 0, 1, 0, 0)
    for ring, (n, L, wd, off) in enumerate(((22, r * 1.0, r * 0.2, 0), (22, r * 0.88, r * 0.19, 360 / 44))):
        for i in range(n):
            a = i * 360.0 / n + off
            d = "M0,%s C%s,%s %s,%s 0,%s C%s,%s %s,%s 0,%s Z" % (
                f(-r * 0.38), f(-wd), f(-r * 0.5), f(-wd * 0.8), f(-L * 0.9), f(-L), f(wd * 0.8), f(-L * 0.9), f(wd), f(-r * 0.5), f(-r * 0.38))
            out.append('<path d="%s" fill="%s" stroke="%s" stroke-width="1" stroke-opacity="0.4" transform="rotate(%s)"%s/>' % (
                d, pg, petals[2], f(a), ' opacity="0.92"' if ring else ""))
            if not ring:
                out.append('<path d="M0,%s L0,%s" stroke="%s" stroke-width="1.4" opacity="0.5" transform="rotate(%s)"/>' % (f(-r * 0.45), f(-L * 0.85), petals[2], f(a)))
    out.append('<circle r="%s" fill="%s"/>' % (f(r * 0.44), c.rg([(0, center[0]), (0.7, center[1]), (1, "#1A0E04")])))
    seeds = []
    golden = math.pi * (3 - math.sqrt(5))
    N = int(160 * (r / 120.0) ** 1.2) + 60
    for i in range(N):
        rr_ = r * 0.42 * math.sqrt(i / N)
        a = i * golden
        seeds.append('<circle cx="%s" cy="%s" r="%s"/>' % (f(rr_ * math.cos(a)), f(rr_ * math.sin(a)), f(r * 0.016 + r * 0.012 * (i / N))))
    out.append('<g fill="#C88A2E" opacity="0.8">%s</g>' % "".join(seeds))
    out.append('<circle r="%s" fill="#3A2308"/>' % f(r * 0.1))
    out.append('<circle r="%s" fill="none" stroke="#E0A526" stroke-width="%s" opacity="0.5"/>' % (f(r * 0.44), f(r * 0.02)))
    out.append("</g>")
    return "".join(out)


def stem(x0, y0, x1, y1, bend, color="#558B2F", w=10):
    mx = (x0 + x1) / 2 + bend
    my = (y0 + y1) / 2
    return '<path d="M%s,%s Q%s,%s %s,%s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"/>' % (f(x0), f(y0), f(mx), f(my), f(x1), f(y1), color, f(w))


def morning_glory(c, cx, cy, r, rot=0, col=("#7E57C2", "#3949AB"), throat="#FFF8E1"):
    """Morning-glory trumpet flower face-on with pleated star and pale throat."""
    out = ['<g transform="translate(%s,%s) rotate(%s)">' % (f(cx), f(cy), f(rot))]
    p = "M%s,%s " % (f(r * math.cos(math.radians(-126))), f(r * math.sin(math.radians(-126))))
    for i in range(5):
        am = math.radians(i * 72 - 90)
        a1 = math.radians(i * 72 - 90 + 36)
        p += "Q%s,%s %s,%s " % (f(r * 1.28 * math.cos(am)), f(r * 1.28 * math.sin(am)), f(r * math.cos(a1)), f(r * math.sin(a1)))
    p += "Z"
    out.append('<path d="%s" fill="%s"/>' % (p, c.rg([(0, throat), (0.28, "#FFFFFF"), (0.4, col[0]), (1, col[1])])))
    for i in range(5):
        am = math.radians(i * 72 - 90)
        out.append('<path d="M0,0 L%s,%s" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="%s"/>' % (f(r * 1.05 * math.cos(am)), f(r * 1.05 * math.sin(am)), f(r * 0.06)))
    out.append('<circle r="%s" fill="%s"/>' % (f(r * 0.22), c.rg([(0, "#FFF59D"), (1, throat)])))
    out.append("</g>")
    return "".join(out)


def heart_leaf(c, x, y, s, rot=0, cols=("#81C784", "#2E7D32")):
    d = "M0,0 C-30,-20 -44,-60 -20,-78 C-8,-86 0,-74 0,-66 C0,-74 8,-86 20,-78 C44,-60 30,-20 0,0 Z"
    return '<g transform="translate(%s,%s) rotate(%s) scale(%s)"><path d="%s" fill="%s"/><path d="M0,0 V-66" stroke="#E8F5E9" stroke-width="1.6" opacity="0.7"/></g>' % (
        f(x), f(y), f(rot), f(s), d, c.lg([cols[0], cols[1]], 0, 0, 1, 1))


def vine(c, pts_list, flowers_at=(), col=("#7E57C2", "#3949AB"), leaf_every=2, w=4):
    """Curling vine through the given points with heart leaves and morning-glory flowers."""
    d = "M%s,%s" % (f(pts_list[0][0]), f(pts_list[0][1]))
    for i in range(1, len(pts_list)):
        a = pts_list[i - 1]; b = pts_list[i]
        mx, my = (a[0] + b[0]) / 2 + (b[1] - a[1]) * 0.25, (a[1] + b[1]) / 2 - (b[0] - a[0]) * 0.25
        d += " Q%s,%s %s,%s" % (f(mx), f(my), f(b[0]), f(b[1]))
    out = ['<path d="%s" stroke="#558B2F" stroke-width="%s" fill="none" stroke-linecap="round"/>' % (d, f(w))]
    for i, (x, y) in enumerate(pts_list):
        if i % leaf_every == 0:
            out.append(heart_leaf(c, x, y, c.rnd.uniform(0.5, 0.8), c.rnd.uniform(-70, 70)))
    for (x, y, r) in flowers_at:
        out.append(morning_glory(c, x, y, r, c.rnd.uniform(0, 70), col))
    return "".join(out)


def blossom(c, x, y, r, col=("#FFFFFF", "#F8BBD0"), center="#F9A825"):
    """Five-petal morning blossom."""
    out = ['<g transform="translate(%s,%s) rotate(%s)">' % (f(x), f(y), f(c.rnd.uniform(0, 72)))]
    g = c.rg([(0, col[1]), (1, col[0])], 0.5, 0.9, 0.9)
    for i in range(5):
        out.append('<ellipse cx="0" cy="%s" rx="%s" ry="%s" fill="%s" transform="rotate(%s)"/>' % (f(-r * 0.55), f(r * 0.42), f(r * 0.58), g, i * 72))
    out.append('<circle r="%s" fill="%s"/>' % (f(r * 0.2), center))
    for i in range(8):
        a = math.radians(i * 45)
        out.append('<circle cx="%s" cy="%s" r="%s" fill="#E65100"/>' % (f(r * 0.3 * math.cos(a)), f(r * 0.3 * math.sin(a)), f(r * 0.05)))
    out.append("</g>")
    return "".join(out)


# ------------------------------------------------------------------ birds perched
def sparrow(c, x, y, s=1.0, flip=False, body=("#A1887F", "#5D4037"), breast="#FFE0B2", beak="#FFB300", singing=False):
    """Plump sparrow / bulbul perched, feet at (x,y), facing right. ~130*s long."""
    out = ['<g transform="translate(%s,%s) scale(%s,%s)">' % (f(x), f(y), f(-s if flip else s), f(s))]
    # tail
    out.append('<path d="M-40,-30 L-104,-2 L-96,8 L-36,-14 Z" fill="%s"/>' % body[1])
    # body
    out.append('<path d="M-50,-30 C-40,-72 20,-86 44,-62 C62,-44 50,-10 20,-2 C-10,6 -44,0 -50,-30 Z" fill="%s"/>' % c.lg([body[0], body[1]], 0, 0, 1, 1))
    out.append('<path d="M-10,-12 C10,-10 36,-18 46,-44 C54,-26 40,-6 18,-2 C4,0 -8,-4 -10,-12 Z" fill="%s"/>' % breast)
    # wing
    out.append('<path d="M-46,-40 C-30,-66 10,-62 16,-40 C4,-24 -24,-18 -60,-18 Z" fill="%s"/>' % body[1])
    for k in range(3):
        out.append('<path d="M%s,-%s C%s,-%s %s,-%s %s,-%s" stroke="%s" stroke-width="2" fill="none" opacity="0.6"/>' % (
            f(-40 + k * 10), f(26 + k * 3), f(-30 + k * 10), f(40 + k * 4), f(-10 + k * 6), f(46 + k * 2), f(6), f(36), "#FFE0B2"))
    # head
    out.append('<circle cx="44" cy="-68" r="24" fill="%s"/>' % body[0])
    out.append('<path d="M26,-86 C40,-98 60,-94 66,-80 C54,-84 40,-84 26,-76 Z" fill="%s"/>' % body[1])
    out.append('<path d="M44,-56 C54,-48 62,-50 66,-58 C58,-56 50,-56 44,-56 Z" fill="%s"/>' % breast)
    out.append('<circle cx="54" cy="-72" r="4.6" fill="#1A1A1A"/><circle cx="55.5" cy="-73.5" r="1.4" fill="#FFFFFF"/>')
    if singing:
        out.append('<path d="M64,-72 L86,-74 L66,-66 Z M64,-64 L82,-58 L64,-60 Z" fill="%s"/>' % beak)
    else:
        out.append('<path d="M64,-72 L84,-66 L64,-62 Z" fill="%s"/>' % beak)
    # feet
    out.append('<path d="M0,-2 L-4,10 M14,-2 L16,10" stroke="#6D4C41" stroke-width="3" stroke-linecap="round"/>')
    out.append("</g>")
    return "".join(out)


def branch(c, x0, y0, x1, y1, bend=40, w=12, color="#6D4C41", twigs=4, leaves=True, flowers=True, fcol=("#FFFFFF", "#F8BBD0")):
    out = ['<path d="M%s,%s Q%s,%s %s,%s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"/>' % (
        f(x0), f(y0), f((x0 + x1) / 2), f((y0 + y1) / 2 - bend), f(x1), f(y1), color, f(w))]
    rnd = c.rnd
    for i in range(twigs):
        t = (i + 0.7) / (twigs + 0.5)
        bx = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * (x0 + x1) / 2 + t * t * x1
        by = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * ((y0 + y1) / 2 - bend) + t * t * y1
        sgn = -1 if i % 2 else 1
        tx, ty = bx + rnd.uniform(20, 60) * (1 if x1 > x0 else -1), by + sgn * rnd.uniform(40, 80)
        out.append('<path d="M%s,%s Q%s,%s %s,%s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"/>' % (
            f(bx), f(by), f((bx + tx) / 2), f(by), f(tx), f(ty), color, f(w * 0.45)))
        if leaves:
            out.append(leaf(c, tx, ty, rnd.uniform(60, 90), rnd.uniform(-60, 60) + (0 if sgn < 0 else 180), drops=1))
        if flowers:
            out.append(blossom(c, bx + rnd.uniform(-10, 10), by + sgn * 18, rnd.uniform(16, 24), fcol))
    return "".join(out)


# ------------------------------------------------------------------ window
def window(c, x, y, w, h, frame="#FFFFFF", frame_dark="#C9B79C", view=None, shutters=("#4E8F84", "#2F6B61"), curtain=("#FFE0B2", "#F4B183"), sill_plant=True):
    """Arched-top window, open wooden shutters, morning view inside (callable view(c, box) or default sky+hills),
    sunlight beams falling out, curtain tie-back and a potted plant on the sill."""
    out = []
    r = w / 2
    arch = "M%s,%s V%s A%s,%s 0 0 1 %s,%s V%s Z" % (f(x), f(y + h), f(y + r), f(r), f(r), f(x + w), f(y + r), f(y + h))
    cp = c.clip('<path d="%s"/>' % arch)
    # view
    out.append('<g clip-path="%s">' % cp)
    if view:
        out.append(view(c, (x, y, x + w, y + h)))
    else:
        out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (f(x), f(y), f(w), f(h), c.lg(["#8EC5FC", "#FFE3B3", "#FFB88C"])))
        out.append(sun(c, x + w * 0.55, y + h * 0.62, w * 0.12, halo_r=3.5))
        out.append(hills(c, [(y + h * 0.7, 30, ("#9FB9A8", "#7FA08E"), 0.5, 2), (y + h * 0.82, 26, ("#5E8C6A", "#3F6B4E"), 2.1, 3)], x, x + w, y + h))
        out.append(flock(c, x + w * 0.35, y + h * 0.35, 4, w * 0.12, "#4A3B52", 0.3, 0.5))
    out.append('</g>')
    # glass sheen
    out.append('<path d="%s" fill="%s"/>' % (arch, c.lg([(0, "#FFFFFF", 0.22), (0.4, "#FFFFFF", 0), (0.6, "#FFFFFF", 0.1), (1, "#FFFFFF", 0)], 0, 0, 1, 1)))
    # frame + mullions
    fw = max(14, w * 0.045)
    out.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (arch, frame_dark, f(fw + 8)))
    out.append('<path d="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (arch, frame, f(fw)))
    out.append('<path d="M%s,%s V%s M%s,%s H%s" stroke="%s" stroke-width="%s"/>' % (f(x + r), f(y), f(y + h), f(x), f(y + r + (h - r) * 0.45), f(x + w), frame, f(fw * 0.6)))
    # shutters (open, in perspective)
    sw = w * 0.34
    for side in (-1, 1):
        ex = x if side < 0 else x + w
        ox = ex + side * sw
        d = "M%s,%s L%s,%s L%s,%s L%s,%s Z" % (f(ex), f(y + r * 0.6), f(ox), f(y + r * 0.6 + 40), f(ox), f(y + h - 30), f(ex), f(y + h))
        out.append('<path d="%s" fill="%s" stroke="%s" stroke-width="4"/>' % (d, c.lg([shutters[0], shutters[1]], 0, 0, 1, 0) if side > 0 else c.lg([shutters[1], shutters[0]], 0, 0, 1, 0), frame_dark))
        for k in range(1, 12):
            t = k / 12
            ya = y + r * 0.6 + (h - r * 0.6) * t
            yb = y + r * 0.6 + 40 + (h - 30 - r * 0.6 - 40) * t
            out.append('<path d="M%s,%s L%s,%s" stroke="#000" stroke-opacity="0.18" stroke-width="3"/>' % (f(ex), f(ya), f(ox), f(yb)))
    # sill
    out.append('<path d="M%s,%s h%s l-20,26 h%s Z" fill="%s"/>' % (f(x - 40), f(y + h), f(w + 80), f(-(w + 40)), c.lg([frame, frame_dark], 0, 0, 0, 1)))
    if sill_plant:
        px = x + w * 0.78
        py = y + h
        for k in range(7):
            a = -90 + (k - 3) * 22
            out.append(leaf(c, px, py - 50, 70 + (3 - abs(k - 3)) * 14, a + 90, ("#AED581", "#2E7D32"), drops=0))
        out.append('<path d="M%s,%s L%s,%s L%s,%s L%s,%s Z" fill="%s"/>' % (f(px - 44), f(py - 62), f(px + 44), f(py - 62), f(px + 32), f(py), f(px - 32), f(py),
                                                                          c.lg(["#E07A4F", "#B5522B"], 0, 0, 1, 0)))
        out.append('<rect x="%s" y="%s" width="96" height="14" rx="4" fill="#C8643A"/>' % (f(px - 48), f(py - 70)))
    return "".join(out)


def light_beams(c, x0, y0, x1, y1, spread, n=5, color="#FFF3C4", op=0.22):
    """Soft diagonal god-rays from a light source line (x0,y0)-(x1,y1) toward direction spread vector."""
    out = []
    dx, dy = spread
    for i in range(n):
        t0 = i / n; t1 = t0 + 0.6 / n
        ax, ay = x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0
        bx, by = x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1
        d = "M%s,%s L%s,%s L%s,%s L%s,%s Z" % (f(ax), f(ay), f(bx), f(by), f(bx + dx * 1.1), f(by + dy * 1.1), f(ax + dx), f(ay + dy))
        out.append('<path d="%s" fill="%s"/>' % (d, c.lg([(0, color, op), (1, color, 0)], 0, 0, dx / (abs(dx) + abs(dy) + 1e-9), dy / (abs(dx) + abs(dy) + 1e-9))))
    return '<g filter="%s">%s</g>' % (c.blur(6), "".join(out))
