"""wedding-wishes motifs (lib_c family): couple silhouettes, varmala, agni kund, gathbandhan knot,
mehendi hands, doli, rose petals."""
from lib_c import *


from motifs_people_c import groom, bride, couple_back  # refined figures


def varmala(d, hx, hy, L=200, w=70, s=1, vars_=("red", "wine"), tilt=0):
    """garland loop hanging from a hand point"""
    pts = []
    for i in range(34):
        t = i / 33 * 2 * math.pi
        px = hx + w / 2 * math.sin(t) * s
        py = hy + (L / 2 - L / 2 * math.cos(t)) * s
        if tilt:
            dx = (py - hy) * math.tan(math.radians(tilt))
            px += dx
        pts.append((px, py, 0))
    o = []
    for i, (px, py, _) in enumerate(pts):
        if i % 2:
            o.append(jasmine(d, px, py, 7 * s, i * 20))
        else:
            o.append(rose(d, px, py, 10 * s, vars_[(i // 2) % len(vars_)], i * 33))
    bx, by = pts[17][0], pts[17][1]
    o.append(tassel(d, bx, by + 6 * s, 0.6 * s, "#C21F3A"))
    return "".join(o)


# ------------------------------------------------------------------ agni kund (havan) with flames
def flame_d(k=1.0, lean=0):
    return "M0,0 C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s 0,0Z" % tuple(n(v * k) for v in (
        -44, -8, -54, -64, -22 + lean * 0.3, -112,
        -10 + lean * 0.5, -134, -12 + lean, -164, 0 + lean, -200,
        14 + lean, -156, 34 + lean * 0.5, -132, 36 + lean * 0.3, -100,
        54, -58, 44, -8))


def agni_kund(d, cx, by, s=1, glow=True):
    o = []
    if glow:
        o.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (n(cx), n(by - 170 * s), n(300 * s), n(260 * s), d.rg([(0, "#FFB347", 0.75), (0.5, "#FF7A1A", 0.25), (1, "#FF7A1A", 0)])))
    copper = d.lg([(0, "#6E2A0E"), (0.3, "#C8642A"), (0.5, "#F2A36A"), (0.7, "#B8521E"), (1, "#5A200A")], 0, 0, 1, 0, key="copper")
    # tiers (front view trapezoids)
    for i, (w_, h_) in enumerate([(230, 34), (190, 30), (150, 28)]):
        yy = by - sum(hh for _, hh in [(230, 34), (190, 30), (150, 28)][:i + 1])
        o.append('<path d="M%s,%s L%s,%s L%s,%s L%s,%sZ" fill="%s"/>' % (
            n(cx - w_ / 2 * s), n(yy + h_ * s), n(cx + w_ / 2 * s), n(yy + h_ * s), n(cx + (w_ / 2 - 10) * s), n(yy), n(cx - (w_ / 2 - 10) * s), n(yy), copper))
        o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (n(cx - (w_ / 2 - 10) * s), n(yy), n((w_ - 20) * s), n(4 * s), d.gold()))
        if i == 0:
            for k in range(7):
                o.append(sparkle(cx + (-90 + k * 30) * s, yy + h_ * s * 0.55, 5 * s, "#FFE2A8", .9))
    top = by - 92 * s
    # flames
    fl = [(-40, 0.62, -20, "#D7261E"), (40, 0.66, 20, "#D7261E"), (0, 1.0, 0, "#E8451A"), (-22, 0.72, -10, "#F57C12"), (24, 0.76, 12, "#F57C12"),
          (0, 0.8, 4, "#FFA41B"), (-8, 0.55, -6, "#FFD23F"), (8, 0.5, 6, "#FFE98A"), (0, 0.32, 0, "#FFF8D6")]
    gl = d.glow(10, "#FFB347", 0.8)
    parts = []
    for dx, k, lean, col in fl:
        parts.append('<path d="%s" fill="%s" transform="translate(%s %s)"/>' % (flame_d(k * s, lean), col, n(cx + dx * s), n(top + 8 * s)))
    o.append('<g filter="%s">%s</g>' % (gl, "".join(parts)))
    # logs
    for a in (-18, 18):
        o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="#4A2A14" transform="rotate(%s %s %s)"/>' % (
            n(cx - 70 * s), n(top - 4 * s), n(140 * s), n(14 * s), n(6 * s), a, n(cx), n(top)))
    # sparks
    rr = random.Random(5)
    for i in range(26):
        o.append('<circle cx="%s" cy="%s" r="%s" fill="#FFD27A" opacity="%s"/>' % (n(cx + rr.uniform(-110, 110) * s), n(top - rr.uniform(60, 320) * s), n(rr.uniform(1.2, 3.4) * s), n(rr.uniform(.4, .95))))
    return "".join(o)


# ------------------------------------------------------------------ gathbandhan knot
def fabric_band(d, fn, w, fill, border, dot=None, steps=80, dot_sp=18):
    pts, L, R = tube_pts(fn, w, w, steps)
    o = ['<path d="M%s Z" fill="%s"/>' % (" L".join("%s,%s" % (n(a), n(b)) for a, b in L + R[::-1]), fill)]
    # folds
    o.append('<path d="M%s" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="%s"/>' % (" L".join("%s,%s" % (n((a[0] + p[0]) / 2), n((a[1] + p[1]) / 2)) for a, p in zip(L, pts)), n(w * 0.12)))
    o.append('<path d="M%s" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="%s"/>' % (" L".join("%s,%s" % (n((a[0] + p[0]) / 2), n((a[1] + p[1]) / 2)) for a, p in zip(R, pts)), n(w * 0.1)))
    for edge in (L, R):
        o.append('<path d="M%s" fill="none" stroke="%s" stroke-width="%s"/>' % (" L".join("%s,%s" % (n(a), n(b)) for a, b in edge), border, n(max(3, w * 0.09))))
    if dot:
        acc = 0
        for i in range(1, len(pts)):
            acc += math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
            if acc > dot_sp:
                acc = 0
                for f in (-0.28, 0, 0.28):
                    px = pts[i][0] + (L[i][0] - pts[i][0]) * f * 2
                    py = pts[i][1] + (L[i][1] - pts[i][1]) * f * 2
                    o.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(px), n(py), n(w * 0.05), dot))
    return "".join(o)


def gathbandhan(d, cx, cy, s=1, red=("#C8102E", "#8E0A1E"), cream=("#FFF3DC", "#E9D3A8")):
    gf = d.gold()
    gr = d.lg([(0, red[0]), (1, red[1])], 0, 0, 1, 1, key="gbr")
    gc = d.lg([(0, cream[0]), (1, cream[1])], 0, 0, 1, 1, key="gbc")
    o = []
    # incoming bands
    o.append(fabric_band(d, cub((-560, -330), (-360, -300), (-160, -100), (-30, -10)), 96, gr, gf, "#FFD23F"))
    o.append(fabric_band(d, cub((560, -330), (360, -300), (160, -100), (30, -10)), 96, gc, gf, "#D4A020"))
    # tails
    o.append(fabric_band(d, cub((-20, 20), (-60, 80), (-150, 150), (-180, 290)), 80, gr, gf, "#FFD23F"))
    o.append(fabric_band(d, cub((20, 20), (60, 90), (130, 160), (150, 300)), 80, gc, gf, "#D4A020"))
    for tx, ty_, col in ((-180, 300, red[1]), (150, 310, "#B8862A")):
        for k in range(9):
            o.append('<path d="M%s,%s l%s,32" stroke="%s" stroke-width="3"/>' % (n(tx - 32 + k * 8), n(ty_ - 12), n(-4 + k), gf))
    k = []
    # knot body: two wrapped loops
    k.append('<ellipse cx="0" cy="0" rx="78" ry="62" fill="%s" filter="%s"/>' % (gr, d.shadow(0, 8, 10, "#000", .35)))
    k.append('<path d="M-70,-20 C-40,-70 50,-70 76,-6 C50,-30 -30,-40 -70,-20Z" fill="%s"/>' % gc)
    k.append('<path d="M-76,10 C-40,60 50,60 72,22 C40,40 -30,40 -76,10Z" fill="%s"/>' % gc)
    k.append('<path d="M-70,-20 C-40,-70 50,-70 76,-6 M-76,10 C-40,60 50,60 72,22" stroke="%s" stroke-width="4" fill="none"/>' % gf)
    k.append('<path d="M-30,-8 C-10,-20 20,-20 32,-4 C20,8 -10,10 -30,-8Z" fill="%s" opacity=".35"/>' % red[1])
    # coin + betel nut + rice tucked in
    k.append('<circle cx="0" cy="-4" r="16" fill="%s" stroke="#8A5A12" stroke-width="2"/><circle cx="0" cy="-4" r="9" fill="none" stroke="#8A5A12" stroke-width="1.5"/>' % gf)
    for (px, py) in ((-40, 4), (36, 10), (-10, 30), (22, -30)):
        k.append('<ellipse cx="%s" cy="%s" rx="4" ry="2" fill="#FFFDF4" transform="rotate(30 %s %s)"/>' % (px, py, px, py))
    o.append(g("".join(k), 0, 0, 1.35))
    return g("".join(o), cx, cy, s)


# ------------------------------------------------------------------ mehendi hand
def mehendi_hand(d, x, y, s=1, flip=False, rot=0, skin=("#F3C7A1", "#D99A70"), henna="#8A2E0C", cuff=("#B3122E", "#7A0A1E")):
    """right hand, palm facing viewer, fingers up; wrist bottom at (x,y); ~220 wide, 470 tall"""
    gs = d.lg([(0, skin[0]), (1, skin[1])], 0, 0, 1, 1, key="skin%s" % skin[0])
    shapes = []
    fingers = [(-62, -270, 118, -6), (-22, -300, 150, -2), (20, -296, 146, 2), (58, -262, 116, 7)]
    for fx, fy, L, a in fingers:
        ty_ = fy - L + 80
        shapes.append('<path d="M%s,%s L%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%sZ" transform="rotate(%s %s %s)"/>' % (
            n(fx - 19), n(fy + 80), n(fx - 15), n(ty_ + 16), n(fx - 15), n(ty_ - 6), n(fx + 15), n(ty_ - 6), n(fx + 15), n(ty_ + 16),
            n(fx + 15), n(ty_ + 16), n(fx + 19), n(fy + 80), n(fx + 19), n(fy + 80), a, n(fx), n(fy + 60)))
    # thumb
    shapes.append('<rect x="-18" y="-120" width="40" height="120" rx="20" transform="translate(-86 -110) rotate(-42)"/>')
    palm = "M-84,-210 C-86,-140 -84,-90 -64,-40 L-56,20 L60,20 L66,-40 C84,-90 86,-150 80,-210 C40,-230 -40,-232 -84,-210Z"
    shapes.append('<path d="%s"/>' % palm)
    clipid = d.clip("".join(shapes))
    o = ['<g fill="%s">%s</g>' % (gs, "".join(shapes))]
    art = []
    hs = 'fill="none" stroke="%s" stroke-linecap="round"' % henna
    # palm mandala
    art.append(ring_petals(12, 14, 46, 9, "none", henna, 2.4, 0, 0, -118))
    art.append('<circle cx="0" cy="-118" r="13" fill="%s"/><circle cx="0" cy="-118" r="56" %s stroke-width="3"/>' % (henna, hs))
    art.append(dots_ring(24, 64, 2.6, henna, 0, -118))
    art.append('<circle cx="0" cy="-118" r="74" %s stroke-width="1.6" stroke-dasharray="1 6"/>' % hs)
    art.append(ring_petals(8, 76, 100, 12, "none", henna, 2, 22.5, 0, -118))
    # wrist bands
    for yy in (-10, 4):
        art.append('<path d="M-70,%d Q0,%d 70,%d" %s stroke-width="3"/>' % (yy, yy + 10, yy, hs))
    art.append('<path d="M-70,-24 Q0,-14 70,-24" %s stroke-width="1.6" stroke-dasharray="6 5"/>' % hs)
    for k in range(9):
        art.append('<path d="M%s,-24 q8,-16 16,0" %s stroke-width="2"/>' % (n(-68 + k * 16), hs))
    # fingers: caps, bands, vines
    for fx, fy, L, a in fingers:
        tipy = fy - L + 80
        g_ = []
        g_.append('<rect x="%s" y="%s" width="36" height="30" fill="%s" opacity=".85"/>' % (n(fx - 18), n(tipy - 8), henna))
        for k, yy in enumerate((tipy + 50, tipy + 58, tipy + 96)):
            g_.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"/>' % (n(fx - 18), n(yy), n(fx + 18), n(yy), henna, 2.4 if k < 2 else 1.6))
        g_.append('<path d="M%s,%s q-8,10 0,20 q8,10 0,20" %s stroke-width="2"/>' % (n(fx), n(tipy + 62), hs))
        for k in range(3):
            g_.append('<circle cx="%s" cy="%s" r="2.4" fill="%s"/>' % (n(fx - 8 + k * 8), n(tipy + 110), henna))
        g_.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.8" transform="translate(%s %s)"/>' % (leaf_d(20, 7), henna, n(fx), n(tipy + 150)))
        art.append('<g transform="rotate(%s %s %s)">%s</g>' % (a, n(fx), n(fy + 60), "".join(g_)))
    # thumb pattern
    art.append('<g transform="translate(-86 -110) rotate(-42)"><rect x="-18" y="-120" width="40" height="30" rx="16" fill="%s"/><line x1="-18" y1="-72" x2="22" y2="-72" stroke="%s" stroke-width="2.4"/><path d="M2,-60 q-8,12 0,24 q8,12 0,24" %s stroke-width="2"/></g>' % (henna, henna, hs))
    # side paisleys
    art.append('<g transform="translate(-60 -205) scale(.22) rotate(-30)"><path d="%s" %s stroke-width="9"/></g>' % (paisley_d(1), hs))
    art.append('<g transform="translate(62 -205) scale(-.22 .22) rotate(-30)"><path d="%s" %s stroke-width="9"/></g>' % (paisley_d(1), hs))
    o.append('<g clip-path="%s">%s</g>' % (clipid, "".join(art)))
    # subtle shading
    o.append('<path d="M-56,20 C-80,-60 -86,-150 -84,-210" stroke="#8A4A2A" stroke-opacity=".25" stroke-width="6" fill="none"/>')
    # sleeve cuff (lehenga fabric) with gold border
    gc = d.lg([(0, cuff[0]), (1, cuff[1])], 0, 0, 0, 1, key="cuff%s" % cuff[0])
    o.append('<path d="M-74,16 L74,16 L96,160 L-96,160Z" fill="%s"/>' % gc)
    o.append('<path d="M-74,16 L74,16 L76,34 L-76,34Z" fill="%s"/>' % d.gold())
    for k in range(8):
        o.append('<circle cx="%s" cy="25" r="3" fill="%s"/>' % (n(-60 + k * 17), cuff[1]))
    for k in range(10):
        o.append('<path d="%s" fill="%s" opacity=".6" transform="translate(%s %s) scale(.12)"/>' % (paisley_d(1), d.gold(), n(-70 + (k % 5) * 34 + (k // 5) * 14), n(70 + (k // 5) * 50)))
    sc = "scale(%s %s)" % (n(-s if flip else s), n(s))
    return '<g transform="translate(%s %s) rotate(%s) %s">%s</g>' % (n(x), n(y), n(rot), sc, "".join(o))


# ------------------------------------------------------------------ doli
def doli(d, cx, by, s=1, body=("#C8102E", "#7A0A1E"), roses=("red", "pink")):
    gf = d.gold()
    gb = d.lg([(0, body[0]), (1, body[1])], 0, 0, 0, 1, key="dolib%s" % body[0])
    o = ['<ellipse cx="0" cy="4" rx="220" ry="16" fill="#000" opacity=".25"/>']
    # legs/base
    o.append('<rect x="-170" y="-40" width="340" height="30" fill="%s"/>' % gb)
    o.append('<rect x="-176" y="-44" width="352" height="8" fill="%s"/><rect x="-176" y="-14" width="352" height="6" fill="%s"/>' % (gf, gf))
    for lx in (-160, -60, 60, 160):
        o.append('<path d="M%d,-10 L%d,-10 L%d,4 L%d,4Z" fill="%s"/>' % (lx - 10, lx + 10, lx + 6, lx - 6, gf))
    # body box
    o.append('<rect x="-150" y="-250" width="300" height="210" fill="%s"/>' % gb)
    # arched window with curtain of flowers
    win = foil_arch_d(-86, -226, 172, 176, 0.45, 7)
    o.append('<path d="%s" fill="#3A0610"/>' % win)
    o.append('<path d="%s" fill="%s" opacity=".7"/>' % (win, d.lg([(0, "#FFD9A0"), (1, "#B3122E")])))
    cp = d.clip('<path d="%s"/>' % win)
    strs = []
    for k in range(7):
        px = -72 + k * 24
        for j in range(8):
            strs.append(jasmine(d, px, -214 + j * 22, 7, j * 30) if (j + k) % 2 else rose(d, px, -214 + j * 22, 8, roses[(k + j) % 2]))
    o.append('<g clip-path="%s">%s</g>' % (cp, "".join(strs)))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="6"/>' % (win, gf))
    # side panels paisley
    for sx in (-120, 120):
        o.append(paisley(d, sx, -150, 0.34, 0, body[1], "#F2C45A", "#FFE9C2", flip=sx > 0, detail=1))
    o.append('<rect x="-150" y="-250" width="300" height="210" fill="none" stroke="%s" stroke-width="6"/>' % gf)
    # roof
    o.append('<path d="M-176,-250 L176,-250 L150,-280 L-150,-280Z" fill="%s"/>' % gf)
    o.append('<path d="M-150,-280 C-150,-360 -60,-390 0,-420 C60,-390 150,-360 150,-280Z" fill="%s"/>' % gb)
    o.append('<path d="M-150,-280 C-150,-360 -60,-390 0,-420 C60,-390 150,-360 150,-280" fill="none" stroke="%s" stroke-width="6"/>' % gf)
    o.append('<path d="M-100,-300 C-90,-350 -40,-370 0,-392" stroke="#fff" stroke-opacity=".3" stroke-width="8" fill="none" stroke-linecap="round"/>')
    o.append('<path d="M0,-420 L0,-460" stroke="%s" stroke-width="5"/><circle cx="0" cy="-444" r="8" fill="%s"/><circle cx="0" cy="-466" r="6" fill="%s"/>' % (gf, gf, gf))
    # carrying pole
    o.append('<rect x="-330" y="-300" width="660" height="18" rx="9" fill="%s"/>' % d.lg([(0, "#8A5A12"), (0.5, "#F7DC8C"), (1, "#6E420C")], 0, 0, 0, 1, key="pole"))
    for px in (-330, 330):
        o.append('<circle cx="%d" cy="-291" r="14" fill="%s"/>' % (px, gf))
    # rose garland swags on roof edge + hanging strings at corners
    o.append(rose_swag(d, -170, -262, 170, -262, 30, 10, roses, jas=True))
    for px in (-165, 165):
        for j in range(9):
            o.append(jasmine(d, px, -236 + j * 20, 7, j * 40) if j % 2 else rose(d, px, -236 + j * 20, 9, roses[j % 2]))
        o.append(tassel(d, px, -52, 0.6, body[1]))
    # flowers on roof
    for k in range(-2, 3):
        o.append(rose(d, k * 30, -392 + abs(k) * 12, 12, roses[k % 2]))
    return g("".join(o), cx, by, s)


# ------------------------------------------------------------------ petals
def petal_sym(d, var="red"):
    c = ROSE[var]
    gp = d.lg([(0, c[3]), (0.6, c[2]), (1, c[1])], 0, 0, 1, 1, key="pt%s" % var)
    return d.sym("petal" + var, '<path d="M0,-12 C10,-12 14,-2 8,8 C4,13 -4,13 -8,8 C-14,-2 -10,-12 0,-12Z" fill="%s"/>'
                 '<path d="M-2,-8 C2,-4 3,2 0,8" stroke="%s" stroke-width="1" fill="none" opacity=".5"/>' % (gp, c[0]))


def petals(d, rnd, cnt, x0, y0, x1, y1, r0, r1, vars_=("red",), avoid=None, op=(0.75, 1)):
    o = []
    for i in range(cnt):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if avoid and avoid[0] < x < avoid[2] and avoid[1] < y < avoid[3]:
            continue
        sc = rnd.uniform(r0, r1) / 12
        o.append(d.use(petal_sym(d, rnd.choice(vars_)), x, y, (sc, sc * rnd.uniform(0.55, 1)), rnd.uniform(0, 360), ' opacity="%s"' % n(rnd.uniform(*op))))
    return "".join(o)
