"""inv-wedding motifs (lib_c family): mandap, chhatri, jharokha frame, toran, marigold curtain, matka stack."""
from lib_c import *


def matka_stack(d, x, y, s=1, cols=("#C8102E", "#F2B705", "#1E7A4A")):
    """chori: 3 stacked decorated pots, bottom centre at x,y; ~70 wide, 150 tall"""
    o = []
    yy = 0
    for i, (w, h) in enumerate([(70, 56), (58, 48), (46, 40)]):
        c = cols[i % len(cols)]
        gb = d.lg([(0, c), (0.45, "#FFFFFF"), (0.55, c), (1, "#000000")], 0, 0, 1, 0, key="mt%s" % c)
        o.append('<ellipse cx="0" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (n(yy - h / 2), n(w / 2), n(h / 2), c))
        o.append('<ellipse cx="0" cy="%s" rx="%s" ry="%s" fill="%s" opacity=".25"/>' % (n(yy - h / 2), n(w / 2), n(h / 2), gb))
        o.append('<path d="M%s,%s Q0,%s %s,%s" stroke="%s" stroke-width="3" fill="none"/>' % (n(-w / 2 + 3), n(yy - h / 2), n(yy - h / 2 + 10), n(w / 2 - 3), n(yy - h / 2), d.gold()))
        o.append(dots_ring(8, 0, 0, "none"))
        for k in range(5):
            o.append('<circle cx="%s" cy="%s" r="2.6" fill="#FFF3C4"/>' % (n(-w * 0.32 + k * w * 0.16), n(yy - h * 0.3)))
        o.append('<rect x="%s" y="%s" width="%s" height="6" rx="2" fill="%s"/>' % (n(-w * 0.2), n(yy - h - 4), n(w * 0.4), d.gold()))
        yy -= h + 2
    o.append('<ellipse cx="0" cy="%s" rx="10" ry="8" fill="%s"/>' % (n(yy - 2), d.gold()))
    return g("".join(o), x, y, s)


def chhatri(d, cx, by, w, fill, gf, pillar="#F3E2C6", h=None):
    """small domed pavilion: dome on 2 visible columns; base line by; returns svg"""
    h = h or w * 0.9
    o = []
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (n(cx - w * 0.55), n(by - 10), n(w * 1.1), 10, gf))
    ph = h * 0.42
    for dx in (-w * 0.38, w * 0.38):
        o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (n(cx + dx - w * 0.06), n(by - 10 - ph), n(w * 0.12), n(ph), pillar))
    o.append('<path d="%s" fill="#000" opacity=".25"/>' % foil_arch_d(cx - w * 0.3, by - 10 - ph * 0.95, w * 0.6, ph * 0.95, 0.5, 5))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (n(cx - w * 0.6), n(by - 10 - ph - 12), n(w * 1.2), 12, gf))
    o.append('<path d="M%s,%s L%s,%s L%s,%s L%s,%sZ" fill="%s"/>' % (n(cx - w * 0.66), n(by - 10 - ph - 12), n(cx + w * 0.66), n(by - 10 - ph - 12),
                                                                  n(cx + w * 0.5), n(by - 10 - ph - 22), n(cx - w * 0.5), n(by - 10 - ph - 22), pillar))
    o.append(dome(d, cx, by - 10 - ph - 22, w * 0.8, h * 0.5, fill, gf))
    return "".join(o)


def toran(d, x1, x2, y, leaf_len=70, r=15, bells=True):
    """mango-leaf + marigold toran across the top"""
    o = ['<path d="M%s,%s L%s,%s" stroke="#6B3A12" stroke-width="4"/>' % (n(x1), n(y), n(x2), n(y))]
    k = int((x2 - x1) / (leaf_len * 0.55))
    for i in range(k + 1):
        px = x1 + (x2 - x1) * i / k
        L = leaf_len * (1.0 if i % 2 == 0 else 0.8)
        o.append(leaf(d, px, y + 4, L, L * 0.24, 180 + (6 if i % 2 else -6), "#5DA044", "#1F5E22"))
    o.append(swag(d, x1, y + 6, x2, y + 6, 1, r, ("orange", "yellow"), leaves=False))
    if bells:
        for i in range(1, 6):
            px = x1 + (x2 - x1) * i / 6
            o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#6B3A12" stroke-width="1.5"/>' % (n(px), n(y), n(px), n(y + 70)))
            o.append(marigold(d, px, y + 40, r * 0.8, "red"))
            o.append(bell(d, px, y + 58, 0.42))
    return "".join(o)


def curtain_strings(d, x1, x2, y, lengths, r=13, vars_=("orange", "yellow")):
    o = []
    k = len(lengths)
    for i, L in enumerate(lengths):
        px = x1 + (x2 - x1) * i / (k - 1)
        vv = vars_ if i % 2 == 0 else vars_[::-1]
        o.append(marigold_string(d, px, y, y + L, r, vv, tassel=True))
    return "".join(o)


def mandap(d, cx, by, W, H, cloth=("#B3122E", "#6E0A1C"), drape=("#E8456A", "#9E1030"), dome_fill=None, back_glow="#FFD9A0", seed=3):
    """grand decorated wedding mandap. by = ground line (bottom of steps); total height H"""
    gf = d.gold()
    gv = d.lg(GOLD, 0, 0, 0, 1, key="goldv")
    gh = d.lg(GOLD, 0, 0, 1, 0, key="goldh")
    o = []
    yf = by - 66  # floor
    yc = by - H * 0.60  # beam bottom
    beam_h = H * 0.07
    xl, xr = cx - W * 0.40, cx + W * 0.40
    # back glow
    o.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" opacity=".55" filter="%s"/>' % (
        n(cx), n((yf + yc) / 2), n(W * 0.36), n((yf - yc) * 0.55), back_glow, d.blur(30)))
    # backdrop floral wall (behind, between back pillars)
    bx0, bx1 = cx - W * 0.28, cx + W * 0.28
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (n(bx0), n(yc), n(bx1 - bx0), n(yf - yc), d.lg([(0, "#FFF1D6"), (1, "#F6CFA0")], key="mbk")))
    rr = random.Random(seed)
    wall = []
    for i in range(70):
        wall.append(rose(d, rr.uniform(bx0 + 10, bx1 - 10), rr.uniform(yc + 20, yf - 30), rr.uniform(7, 11), rr.choice(["blush", "white", "peach"]), rr.randint(0, 360)))
    cpw = d.clip('<rect x="%s" y="%s" width="%s" height="%s"/>' % (n(bx0), n(yc), n(bx1 - bx0), n(yf - yc)))
    o.append('<g clip-path="%s" opacity=".85">%s</g>' % (cpw, "".join(wall)))
    # jasmine strands on backdrop
    for i in range(9):
        px = bx0 + 20 + i * (bx1 - bx0 - 40) / 8
        for j in range(int((yf - yc - 60) / 18)):
            o.append(jasmine(d, px, yc + 30 + j * 18, 5, j * 30))
    # back pillars
    for px in (bx0, bx1):
        o.append('<rect x="%s" y="%s" width="22" height="%s" fill="%s"/>' % (n(px - 11), n(yc), n(yf - yc), d.lg([(0, "#8C5A17"), (0.5, "#E2B659"), (1, "#7A4A0E")], 0, 0, 1, 0, key="bp")))
    # steps / platform
    for i, (ww, col) in enumerate([(W * 1.0, cloth[1]), (W * 0.94, cloth[0]), (W * 0.88, "#FFF3E0")]):
        yy = by - 22 * (i + 1)
        o.append('<rect x="%s" y="%s" width="%s" height="22" fill="%s"/>' % (n(cx - ww / 2), n(yy), n(ww), col))
        o.append('<rect x="%s" y="%s" width="%s" height="4" fill="%s"/>' % (n(cx - ww / 2), n(yy), n(ww), gh))
        if i == 1:
            for k in range(int(ww / 34)):
                o.append('<path d="M%s,%s l8,8 l-8,8 l-8,-8Z" fill="%s" opacity=".8"/>' % (n(cx - ww / 2 + 17 + k * 34), n(yy + 3), gf))
    # floor rangoli-like carpet (flowers in a grid)
    o.append('<ellipse cx="%s" cy="%s" rx="%s" ry="14" fill="#000" opacity=".12"/>' % (n(cx), n(yf + 2), n(W * 0.3)))
    for k in range(-5, 6):
        o.append(marigold(d, cx + k * W * 0.05, yf - 4, 7, "red" if k % 2 else "yellow"))
    # canopy: beam
    o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (n(xl - 40), n(yc - beam_h), n(xr - xl + 80), n(beam_h), d.lg([(0, cloth[0]), (1, cloth[1])], key="bm%s" % cloth[0])))
    o.append('<rect x="%s" y="%s" width="%s" height="6" fill="%s"/><rect x="%s" y="%s" width="%s" height="6" fill="%s"/>' % (
        n(xl - 40), n(yc - beam_h), n(xr - xl + 80), gh, n(xl - 40), n(yc - 6), n(xr - xl + 80), gh))
    for k in range(int((xr - xl + 80) / 46)):
        px = xl - 20 + k * 46
        o.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/><circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (
            n(px), n(yc - beam_h / 2), n(beam_h * 0.22), gf, n(px), n(yc - beam_h / 2), n(beam_h * 0.1), cloth[1]))
    # cornice + roof tiers
    ty = yc - beam_h
    o.append('<path d="M%s,%s L%s,%s L%s,%s L%s,%sZ" fill="%s"/>' % (n(xl - 60), n(ty), n(xr + 60), n(ty), n(xr + 20), n(ty - 26), n(xl - 20), n(ty - 26), gv))
    o.append('<path d="M%s,%s L%s,%s L%s,%s L%s,%sZ" fill="%s"/>' % (n(xl - 10), n(ty - 26), n(xr + 10), n(ty - 26), n(xr - 30), n(ty - 44), n(xl + 30), n(ty - 44), cloth[0]))
    # dome
    df = dome_fill or d.lg([(0, "#FFF3C4"), (0.3, "#F2C45A"), (0.7, "#C8922E"), (1, "#7A4A0E")], 0.2, 0, 0.8, 1, key="mdome")
    o.append(ring_petals(1, 0, 0, 0, "none"))
    o.append('<path d="M%s,%s Q%s,%s %s,%s L%s,%s Q%s,%s %s,%sZ" fill="%s"/>' % (n(cx - W * 0.2), n(ty - 44), n(cx - W * 0.2), n(ty - 64), n(cx - W * 0.15), n(ty - 66), n(cx + W * 0.15), n(ty - 66), n(cx + W * 0.2), n(ty - 64), n(cx + W * 0.2), n(ty - 44), cloth[0]))
    for k in range(9):
        px_ = cx - W * 0.16 + k * W * 0.04
        o.append('<path d="M%s,%s q%s,-20 %s,0Z" fill="%s"/>' % (n(px_ - W * 0.02), n(ty - 64), n(W * 0.02), n(W * 0.04), gf))
    o.append(dome(d, cx, ty - 66, W * 0.30, H * 0.30, df, gf))
    # dome bands
    for k in range(-3, 4):
        o.append(marigold(d, cx + k * W * 0.036, ty - 66 - H * 0.07 - (3 - abs(k)) * 2.5, 7, "red" if k % 2 else "yellow"))
    # corner chhatris
    for px in (xl, xr):
        o.append(chhatri(d, px, ty - 26, W * 0.12, df, gf, pillar="#F3E2C6"))
    # scalloped fringe valance under beam
    fr = []
    k = 14
    for i in range(k):
        x0 = xl - 40 + (xr - xl + 80) * i / k
        x1 = xl - 40 + (xr - xl + 80) * (i + 1) / k
        fr.append("M%s,%s Q%s,%s %s,%s" % (n(x0), n(yc), n((x0 + x1) / 2), n(yc + 34), n(x1), n(yc)))
    o.append('<path d="%s L%s,%s Z" fill="%s"/>' % (" ".join(fr).replace(" M", " L"), n(xl - 40), n(yc), cloth[0]))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="3"/>' % (" ".join(fr), gf))
    for i in range(k + 1):
        px = xl - 40 + (xr - xl + 80) * i / k
        o.append(tassel(d, px, yc + 2, 0.4, cloth[1]))
    # drapes (chiffon) from beam corners, tied to pillars
    gd = d.lg([(0, drape[0]), (0.5, drape[1]), (1, drape[0])], 0, 0, 1, 0, key="drp%s" % drape[0])
    for sgn in (-1, 1):
        px = cx + sgn * W * 0.40
        top_in = cx + sgn * W * 0.06
        path = "M%s,%s L%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%sZ" % (
            n(px + sgn * 30), n(yc + 20), n(top_in), n(yc + 20),
            n(top_in + sgn * 30), n(yc + 90), n(px - sgn * 40), n(yc + (yf - yc) * 0.25), n(px - sgn * 18), n(yc + (yf - yc) * 0.62),
            n(px + sgn * 10), n(yc + (yf - yc) * 0.72), n(px + sgn * 36), n(yf - 10), n(px + sgn * 30), n(yf))
        o.append('<path d="%s" fill="%s" opacity=".88"/>' % (path, gd))
        for f in range(4):
            o.append('<path d="M%s,%s C%s,%s %s,%s %s,%s" stroke="#fff" stroke-opacity=".35" stroke-width="2" fill="none"/>' % (
                n(top_in - sgn * f * 40), n(yc + 22), n(top_in - sgn * f * 40 + sgn * 10), n(yc + 70),
                n(px - sgn * (30 - f * 4)), n(yc + (yf - yc) * 0.28), n(px - sgn * 14), n(yc + (yf - yc) * 0.44)))
        o.append('<path d="M%s,%s C%s,%s %s,%s %s,%s" stroke="%s" stroke-width="3" fill="none"/>' % (
            n(top_in), n(yc + 20), n(top_in + sgn * 30), n(yc + 90), n(px - sgn * 40), n(yc + (yf - yc) * 0.25), n(px - sgn * 18), n(yc + (yf - yc) * 0.46), gf))
    # front pillars with spiral bands + marigold wrap
    for px in (xl, xr):
        pw = 38
        o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (n(px - pw / 2), n(yc), n(pw), n(yf - yc), d.lg([(0, "#7A4A0E"), (0.3, "#E2B659"), (0.5, "#FFF0B5"), (0.7, "#D9A441"), (1, "#6E420C")], 0, 0, 1, 0, key="fp")))
        cpp = d.clip('<rect x="%s" y="%s" width="%s" height="%s"/>' % (n(px - pw / 2), n(yc), n(pw), n(yf - yc)))
        sp = []
        yy = yc + 20
        while yy < yf:
            sp.append('<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="7"/>' % (n(px - pw / 2 - 4), n(yy + 14), n(px + pw / 2 + 4), n(yy - 8), cloth[0]))
            yy += 34
        o.append('<g clip-path="%s">%s</g>' % (cpp, "".join(sp)))
        # capital + base
        o.append('<path d="M%s,%s L%s,%s L%s,%s L%s,%sZ" fill="%s"/>' % (n(px - pw / 2 - 12), n(yc), n(px + pw / 2 + 12), n(yc), n(px + pw / 2), n(yc + 24), n(px - pw / 2), n(yc + 24), gv))
        o.append('<rect x="%s" y="%s" width="%s" height="26" fill="%s"/>' % (n(px - pw / 2 - 10), n(yf - 26), n(pw + 20), gv))
        # marigold cluster at capital
        for k, (ddx, ddy) in enumerate([(-22, 36), (22, 36), (0, 44), (-12, 58), (12, 58)]):
            o.append(marigold(d, px + ddx, yc + ddy, 12, ["orange", "yellow", "red"][k % 3], k * 40))
        for k in range(3):
            o.append(leaf(d, px - 30 + k * 30, yc + 40, 30, 9, 200 + k * 60, "#5DA044", "#1F5E22"))
        # hanging marigold string next to pillar (inner side)
        sgn = 1 if px < cx else -1
        o.append(marigold_string(d, px + sgn * 52, yc + 24, yc + (yf - yc) * 0.62, 10, ("yellow", "orange"), tassel=False))
        # chori matkas at pillar base
        o.append(matka_stack(d, px + sgn * 60, yf, 0.8))
    # central hanging strings under the beam
    for i, L in enumerate([0.66, 0.5, 0.4, 0.5, 0.66]):
        px = cx + (i - 2) * W * 0.09
        o.append(marigold_string(d, px, yc + 30, yc + (yf - yc) * L, 9, ("orange", "red") if i % 2 else ("yellow", "orange"), tassel=False))
    return "".join(o)
