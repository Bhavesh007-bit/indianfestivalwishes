"""lib_kc: extra Karva Chauth motifs (builds on lib_b helpers)."""
import math, random
from lib_b import *  # noqa
from lib_b import _bez, _around


def _blob(cx, cy, r, rng, k=11, jit=.28):
    P = []
    for i in range(k):
        a = 2 * math.pi * i / k
        rr = r * (1 + rng.uniform(-jit, jit))
        P.append((cx + rr * math.cos(a), cy + rr * .8 * math.sin(a)))
    d = "M%s,%s " % (n((P[0][0] + P[-1][0]) / 2), n((P[0][1] + P[-1][1]) / 2))
    for i in range(k):
        p, q = P[i], P[(i + 1) % k]
        d += "Q%s,%s %s,%s " % (n(p[0]), n(p[1]), n((p[0] + q[0]) / 2), n((p[1] + q[1]) / 2))
    return d + "Z"


def moon(cx, cy, r, seed=3, halo=1.0, tint=("#FFFDF3", "#F8EDCC", "#E2CD98"), glowc="#FFF1C8"):
    """luminous full moon: layered halo, soft maria, fine texture, limb darkening, crisp rim light."""
    rng = random.Random(seed)
    g = ""
    if halo:
        hid, hd = rg([(0, glowc, .5 * halo), (.3, glowc, .2 * halo), (.6, glowc, .06 * halo), (1, glowc, 0)])
        g += '<defs>%s</defs><circle cx="%s" cy="%s" r="%s" fill="url(#%s)"/>' % (hd, n(cx), n(cy), n(r * 4), hid)
        g += '<circle cx="%s" cy="%s" r="%s" fill="#FFF8E2" opacity="%s" filter="url(#fB16)"/>' % (n(cx), n(cy), n(r * 1.08), .55 * halo)
        g += '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#FFF6DA" stroke-width="%s" opacity="%s" filter="url(#fB8)"/>' % (
            n(cx), n(cy), n(r * 1.02), n(r * .06), .6 * halo)
    mid, md = rg([(0, tint[0]), (.55, tint[1]), (1, tint[2])], cx=.4, cy=.38, r=.7)
    lid, ld = rg([(0, "#000", 0), (.72, "#000", 0), (1, "#6B5634", .32)], cx=.5, cy=.5, r=.5)
    cid = uid("mn")
    fid = uid("mt")
    g += ('<defs>%s%s<clipPath id="%s"><circle cx="%s" cy="%s" r="%s"/></clipPath>'
          '<filter id="%s" x="0" y="0" width="100%%" height="100%%"><feTurbulence type="fractalNoise" baseFrequency="%s" numOctaves="4" seed="%d"/>'
          '<feColorMatrix type="matrix" values="0 0 0 0 .45  0 0 0 0 .38  0 0 0 0 .25  0 0 0 -2.2 1.25"/></filter></defs>') % (
        md, ld, cid, n(cx), n(cy), n(r), fid, n(3.2 / r), seed)
    g += '<circle cx="%s" cy="%s" r="%s" fill="url(#%s)"/>' % (n(cx), n(cy), n(r), mid)
    g += '<g clip-path="url(#%s)">' % cid
    # maria (dark seas) - irregular soft blobs, clustered upper-left like the real moon
    seas = [(-.28, -.22, .30), (.05, -.38, .2), (.22, -.12, .22), (-.05, .1, .2), (-.38, .15, .18), (.3, .28, .14), (-.15, -.02, .16)]
    for dx, dy, rr in seas:
        g += '<path d="%s" fill="#BCA676" opacity="%s" filter="url(#fB8)"/>' % (
            _blob(cx + dx * r, cy + dy * r, rr * r, rng), round(rng.uniform(.14, .22), 2))
    g += '<rect x="%s" y="%s" width="%s" height="%s" filter="url(#%s)" opacity=".35"/>' % (n(cx - r), n(cy - r), n(2 * r), n(2 * r), fid)
    # craters: small, bright-rimmed
    for _ in range(9):
        a, d = rng.uniform(0, 6.28), math.sqrt(rng.uniform(0, .7)) * r
        rr = rng.uniform(.018, .045) * r
        x_, y_ = cx + d * math.cos(a), cy + d * math.sin(a)
        g += '<circle cx="%s" cy="%s" r="%s" fill="#A8966E" opacity=".28"/><path d="M%s,%s a%s,%s 0 0 0 %s,%s" fill="none" stroke="#FFFFFF" stroke-width="%s" opacity=".7"/>' % (
            n(x_), n(y_), n(rr), n(x_ + rr), n(y_), n(rr), n(rr), n(-2 * rr), 0, n(max(.8, rr * .3)))
    # Tycho-like ray crater lower half
    tx, ty = cx + .12 * r, cy + .55 * r
    for k in range(10):
        a = 2 * math.pi * k / 10 + .2
        g += '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#FFFFFF" stroke-width="%s" opacity=".25" stroke-linecap="round"/>' % (
            n(tx), n(ty), n(tx + math.cos(a) * r * rng.uniform(.18, .35)), n(ty + math.sin(a) * r * rng.uniform(.18, .35)), n(r * .012))
    g += '<circle cx="%s" cy="%s" r="%s" fill="#FFFFFF" opacity=".8"/>' % (n(tx), n(ty), n(r * .025))
    g += '<circle cx="%s" cy="%s" r="%s" fill="url(#%s)"/>' % (n(cx), n(cy), n(r), lid)
    g += '</g>'
    g += '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#FFFFFF" stroke-width="%s" opacity=".55"/>' % (n(cx), n(cy), n(r - 1), n(max(1, r * .012)))
    return g


def sky(stops, seed, y1=1350, n_stars=140, haze=None, x0=0, y0=0, x1=1080):
    """night sky: gradient + faint milky haze + 3 sizes of stars + a few sparkles."""
    r = random.Random(seed)
    gid, gd = lg(stops, 0, 0, 0, 1)
    g = '<defs>%s</defs><rect x="%d" y="%d" width="%d" height="%d" fill="url(#%s)"/>' % (gd, x0, y0, x1 - x0, y1 - y0, gid)
    for (hx, hy, rx, ry, c, o) in (haze or []):
        g += eglow(hx, hy, rx, ry, c, o)
    g += noise(.05, "overlay", x0, y0, x1 - x0, y1 - y0)
    g += stars(r, n_stars, x0, y0, x1, y1, "#FFF6DA", 1.6, 0)
    g += stars(r, n_stars // 5, x0, y0, x1, y1, "#FFE9C4", 2.8, 0)
    for _ in range(7):
        g += sparkle(r.uniform(x0 + 20, x1 - 20), r.uniform(y0 + 20, y1 - 20), r.uniform(8, 16), "#FFF6DA", .9)
    return g


def zari_pattern(x, y, w, h, col="#FFD86B", op=.12, step=64):
    """woven zari trellis: diamond lattice with a tiny buti at each node (background texture)."""
    pid = uid("zp")
    s = step
    tile = ('<path d="M0,%s L%s,0 L%s,%s L%s,%s Z" fill="none" stroke="%s" stroke-width="1.2"/>' % (s / 2, s / 2, s, s / 2, s / 2, s, col) +
            '<g transform="translate(%s %s)"><path d="M0,-7 C4,-3 4,3 0,7 C-4,3 -4,-3 0,-7Z" fill="%s"/><circle cx="7" cy="0" r="1.6" fill="%s"/><circle cx="-7" cy="0" r="1.6" fill="%s"/></g>' % (
                s / 2, s / 2, col, col, col) +
            '<circle cx="0" cy="0" r="2" fill="%s"/><circle cx="%s" cy="0" r="2" fill="%s"/><circle cx="0" cy="%s" r="2" fill="%s"/><circle cx="%s" cy="%s" r="2" fill="%s"/>' % (
                col, s, col, s, col, s, s, col))
    return ('<defs><pattern id="%s" x="%s" y="%s" width="%s" height="%s" patternUnits="userSpaceOnUse">%s</pattern></defs>'
            '<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)" opacity="%s"/>') % (pid, x, y, s, s, tile, x, y, w, h, pid, op)


def mehendi_mandala(cx, cy, R, col="#7A2E0E", op=1, sw=2.2, seed=1):
    """line-art mehendi mandala (henna style): rings of petals, dots, scallops, paisley ring."""
    g = '<g transform="translate(%s %s)" opacity="%s" fill="none" stroke="%s" stroke-width="%s">' % (n(cx), n(cy), op, col, sw)
    g += '<circle r="%s" fill="%s" stroke="none"/><circle r="%s"/>' % (n(R * .06), col, n(R * .11))
    g += _around(8, '<path d="%s"/>' % petal_path(R * .11, R * .3, R * .08))
    g += _around(8, '<path d="%s"/>' % petal_path(R * .14, R * .24, R * .03), 22.5)
    g += '<circle r="%s"/><circle r="%s" stroke-dasharray="1 %s" stroke-linecap="round" stroke-width="%s"/>' % (n(R * .34), n(R * .38), n(R * .035), n(sw * 2))
    g += _around(16, '<path d="%s"/>' % petal_path(R * .42, R * .6, R * .06, "round"))
    g += _around(16, '<circle cx="0" cy="%s" r="%s" fill="%s" stroke="none"/>' % (n(-R * .52), n(R * .015), col))
    g += '<circle r="%s"/>' % n(R * .64)
    # scallop ring
    k = 32
    d = ""
    for i in range(k):
        a0, a1 = 2 * math.pi * i / k, 2 * math.pi * (i + 1) / k
        p0 = (R * .64 * math.cos(a0), R * .64 * math.sin(a0))
        p1 = (R * .64 * math.cos(a1), R * .64 * math.sin(a1))
        am = (a0 + a1) / 2
        c = (R * .74 * math.cos(am), R * .74 * math.sin(am))
        d += "M%s,%s Q%s,%s %s,%s " % (n(p0[0]), n(p0[1]), n(c[0]), n(c[1]), n(p1[0]), n(p1[1]))
    g += '<path d="%s"/>' % d
    g += _around(32, '<circle cx="0" cy="%s" r="%s" fill="%s" stroke="none"/>' % (n(-R * .76), n(R * .012), col), 360 / 64.)
    # outer leaf ring
    g += _around(24, '<path d="%s"/><path d="M0,%s V%s" stroke-width="%s"/>' % (petal_path(R * .8, R * 1.0, R * .07), n(-R * .82), n(-R * .97), n(sw * .6)))
    g += _around(24, '<circle cx="0" cy="%s" r="%s" fill="%s" stroke="none"/>' % (n(-R * 1.05), n(R * .014), col), 7.5)
    g += '</g>'
    return g


def mehendi_corner(x, y, s=1, rot=0, col="#7A2E0E", op=1):
    """henna paisley + vine corner (drawn for top-left)."""
    g = '<g transform="translate(%s %s) rotate(%s) scale(%s)" opacity="%s" fill="none" stroke="%s" stroke-width="2.4" stroke-linecap="round">' % (n(x), n(y), rot, s, op, col)
    # paisley
    g += '<path d="M60,60 C120,40 170,90 150,150 C135,195 80,190 78,150 C76,120 110,112 118,132"/>'
    g += '<path d="M72,72 C118,58 156,98 140,146 C128,178 92,176 92,150"/>'
    g += '<path d="M104,110 C112,100 124,104 124,116" />'
    for i in range(9):
        a = math.radians(200 + i * 22)
        g += '<circle cx="%s" cy="%s" r="2.6" fill="%s" stroke="none"/>' % (n(112 + 62 * math.cos(a)), n(118 + 62 * math.sin(a)), col)
    # vines along both edges
    for flip in (0, 1):
        tr = ' transform="matrix(0 1 1 0 0 0)"' if flip else ""
        v = '<g%s><path d="M150,20 C200,40 250,10 300,26 C340,38 370,20 400,26"/>' % tr
        for (lx, ly, a) in ((190, 30, -30), (240, 22, 20), (290, 26, -25), (340, 30, 25)):
            v += '<path d="M%s,%s c8,-16 22,-18 30,-12 c-6,12 -18,18 -30,12Z" transform="rotate(%s %s %s)" fill="%s" fill-opacity=".85"/>' % (lx, ly, a, lx, ly, col)
        v += "".join('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="none"/>' % (410 + k * 12, 26, 3 - k * .7, col) for k in range(3))
        v += '</g>'
        g += v
    g += '<path d="M24,24 L60,60" />' + '<circle cx="24" cy="24" r="8" fill="%s" stroke="none"/>' % col
    g += '</g>'
    return g


def heart_d(x, y, w, h):
    cx = x + w / 2
    return "M%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s Z" % (
        n(cx), n(y + h), n(x - w * .2), n(y + h * .55), n(x), n(y - h * .05), n(cx), n(y + h * .22),
        n(x + w), n(y - h * .05), n(x + w * 1.2), n(y + h * .55), n(cx), n(y + h))


def heart_pts(x, y, w, h, k=60):
    cx = x + w / 2
    P = _bez((cx, y + h), (x - w * .2, y + h * .55), (x, y - h * .05), (cx, y + h * .22), k)
    P += _bez((cx, y + h * .22), (x + w, y - h * .05), (x + w * 1.2, y + h * .55), (cx, y + h), k)[1:]
    return P


def resample(P, step):
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


def bead_string(P, r=7, cols=("#C8102E", "url(#gGold)"), pearl=True):
    g = ""
    for i, (x_, y_) in enumerate(P):
        c = cols[i % len(cols)]
        g += '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(x_), n(y_), n(r), c)
        if pearl:
            g += '<circle cx="%s" cy="%s" r="%s" fill="#FFFFFF" opacity=".55"/>' % (n(x_ - r * .3), n(y_ - r * .3), n(r * .3))
    return g


def placeholder_fill(d, x, y, w, h, bg=("#F7E4D4", "#E9C6AE"), fig="#D9A98C", bust=True):
    """soft warm placeholder inside path d (two faint busts = couple)."""
    pid, pd = lg([(0, bg[0]), (1, bg[1])], 0, 0, 0, 1)
    cid = uid("ph")
    g = '<defs>%s<clipPath id="%s"><path d="%s"/></clipPath></defs><g clip-path="url(#%s)">' % (pd, cid, d, cid)
    g += '<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s)"/>' % (n(x), n(y), n(w), n(h), pid)
    g += '<circle cx="%s" cy="%s" r="%s" fill="#FFFFFF" opacity=".55" filter="url(#fB30)"/>' % (n(x + w * .5), n(y + h * .35), n(min(w, h) * .35))
    if bust:
        for (fx, sc) in ((.38, 1.0), (.64, .92)):
            bx, by = x + w * fx, y + h * .52
            rr = min(w, h) * .13 * sc
            g += '<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".75"/>' % (n(bx), n(by - rr * .4), n(rr), fig)
            g += '<path d="M%s,%s C%s,%s %s,%s %s,%s S%s,%s %s,%s Z" fill="%s" opacity=".75"/>' % (
                n(bx - rr * 2.1), n(y + h), n(bx - rr * 2), n(by + rr * 1.3), n(bx - rr), n(by + rr * .9), n(bx), n(by + rr * .9),
                n(bx + rr * 2), n(by + rr * 1.3), n(bx + rr * 2.1), n(y + h), fig)
    g += '</g>'
    return g


def tassel(x, y, s=1, col="#C8102E"):
    g = '<g transform="translate(%s %s) scale(%s)">' % (n(x), n(y), s)
    g += '<line x1="0" y1="0" x2="0" y2="22" stroke="#FFD86B" stroke-width="2"/><circle cx="0" cy="24" r="7" fill="url(#gGold)"/>'
    g += '<path d="M-7,30 L-10,62 L10,62 L7,30Z" fill="%s"/>' % col
    g += '<path d="M-6,34 L-7,60 M0,34 V61 M6,34 L7,60" stroke="#000" stroke-opacity=".25" stroke-width="1.2"/>'
    g += '<rect x="-8" y="30" width="16" height="5" fill="url(#gGoldH)"/></g>'
    return g


def rooftops(y, rng, col="#150A1E", lit="#FFB347"):
    """low haveli rooftops with parapets and a few lit windows (terrace silhouette)."""
    g = ""
    x = -20
    while x < 1100:
        w = rng.uniform(90, 190)
        h = rng.uniform(30, 120)
        g += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (n(x), n(y - h), n(w), n(h + 400), col)
        # parapet crenels
        for k in range(int(w // 22)):
            g += '<rect x="%s" y="%s" width="12" height="8" fill="%s"/>' % (n(x + 5 + k * 22), n(y - h - 8), col)
        for _ in range(rng.randint(0, 2)):
            wx, wy = x + rng.uniform(12, w - 26), y - h + rng.uniform(14, max(15, h - 20))
            g += '<rect x="%s" y="%s" width="12" height="16" rx="6" fill="%s" opacity="%s"/>' % (n(wx), n(wy), lit, round(rng.uniform(.5, .9), 2))
        x += w + rng.uniform(-10, 10)
    return g
