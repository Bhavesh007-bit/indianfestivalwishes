"""anniversary (wishes): 10 premium anniversary card designs (lib_c family).
Motifs: swans heart, candle-lit table, pocket watch + infinity chain, love lock + key, twin coffee cups,
ribbon bouquet, photo collage, anniversary cake with couple topper."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motifs_anniv_c import *
from render import render_cards

CAT = "anniversary"


def glass(d, x, y, w, h, r=36, fill="#FFFFFF", op=0.84, stroke=None, sh=0.22):
    o = '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" opacity="%s" filter="%s"/>' % (n(x), n(y), n(w), n(h), n(r), fill, op, d.shadow(0, 12, 22, "#000", sh))
    if stroke:
        o += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="%s" stroke-width="2.5"/>' % (n(x + 12), n(y + 12), n(w - 24), n(h - 24), n(max(4, r - 10)), stroke)
    return o


def stars(rr, cnt, x0, y0, x1, y1, avoid=None, col="#FFF6D8"):
    o = []
    for i in range(cnt):
        x, y = rr.uniform(x0, x1), rr.uniform(y0, y1)
        if avoid and avoid[0] < x < avoid[2] and avoid[1] < y < avoid[3] and rr.random() < 0.8:
            continue
        o.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>' % (n(x), n(y), n(rr.uniform(0.6, 2.2)), col, n(rr.uniform(0.3, 0.9))))
    return "".join(o)


def fairy_lights(d, x1, y1, x2, y2, sag, cnt=16, bulb="#FFE7A8", wire="#3A2A1A"):
    fn = swag_fn(x1, y1, x2, y2, sag)
    o = ['<path d="%s" stroke="%s" stroke-width="2" fill="none"/>' % (swag_d(x1, y1, x2, y2, sag), wire)]
    gl = d.glow(8, bulb, 0.9)
    b = []
    for i in range(cnt + 1):
        x, y = fn(i / cnt)
        b.append('<ellipse cx="%s" cy="%s" rx="6" ry="9" fill="%s"/>' % (n(x), n(y + 10), bulb))
        o.append('<rect x="%s" y="%s" width="6" height="6" fill="%s"/>' % (n(x - 3), n(y), wire))
    o.append('<g filter="%s">%s</g>' % (gl, "".join(b)))
    return "".join(o)


def heart_confetti(d, rr, cnt, x0, y0, x1, y1, cols, r0=8, r1=18, avoid=None, op=(0.5, 0.95)):
    o = []
    for i in range(cnt):
        x, y = rr.uniform(x0, x1), rr.uniform(y0, y1)
        if avoid and avoid[0] < x < avoid[2] and avoid[1] < y < avoid[3]:
            continue
        r_ = rr.uniform(r0, r1)
        o.append('<path d="%s" fill="%s" opacity="%s" transform="rotate(%s %s %s)"/>' % (shape_d("heart", x - r_, y - r_, 2 * r_, 1.8 * r_), rr.choice(cols), n(rr.uniform(*op)), rr.randint(-30, 30), n(x), n(y)))
    return "".join(o)


# ------------------------------------------------------------------ 1 swans heart on moonlit lake
def card1():
    d = Doc(51)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.lg([(0, "#0B1633"), (0.45, "#1E2A5A"), (0.72, "#4A3A78"), (1, "#1A1438")])]
    o.append(stars(random.Random(3), 170, 0, 0, 1080, 760, (130, 90, 950, 620)))
    o.append('<circle cx="540" cy="760" r="330" fill="%s"/>' % d.rg([(0, "#FFF3D6", .55), (1, "#FFF3D6", 0)]))
    o.append('<circle cx="540" cy="770" r="150" fill="%s"/>' % d.rg([(0, "#FFFBEE"), (0.8, "#F6E7C6"), (1, "#E9D2A4")], 0.4, 0.4, 0.7))
    # distant hills
    o.append('<path d="M0,900 C160,850 280,880 420,860 C560,840 700,880 860,850 C960,834 1030,850 1080,860 L1080,940 L0,940Z" fill="#1A1A40"/>')
    # water
    o.append('<rect x="0" y="930" width="1080" height="420" fill="%s"/>' % d.lg([(0, "#2A3470"), (0.4, "#18204A"), (1, "#0A1030")]))
    for k in range(18):
        yy = 950 + k * 18
        o.append('<path d="M%d,%d h%d" stroke="#FFF3D6" stroke-opacity="%s" stroke-width="2" stroke-linecap="round"/>' % (540 - 60 - k * 6, yy, 120 + k * 12, n(0.5 - k * 0.025)))
    o.append(swans_heart(d, 540, 1150, 1.05))
    # reeds + cattails on both edges
    for side in (-1, 1):
        rr = random.Random(7 + side)
        for k in range(14):
            x0 = 540 + side * rr.uniform(400, 560)
            h_ = rr.uniform(160, 330)
            bend = rr.uniform(-30, 30)
            o.append('<path d="%s" fill="#0A0E24"/>' % tube_d(cub((x0, 1300), (x0 + bend * 0.3, 1300 - h_ * 0.4), (x0 + bend * 0.7, 1300 - h_ * 0.8), (x0 + bend, 1300 - h_)), 9, 2))
            if k % 3 == 0:
                o.append('<rect x="%s" y="%s" width="12" height="46" rx="6" fill="#3A2418" transform="rotate(%s %s %s)"/>' % (n(x0 + bend * 0.9 - 6), n(1300 - h_ * 0.95), n(bend * 0.3), n(x0 + bend), n(1300 - h_)))
    o.append('<rect x="0" y="1290" width="1080" height="60" fill="#070A1C"/>')
    # fireflies
    for (x_, y_) in ((120, 1000), (180, 1080), (930, 1020), (980, 1110), (860, 960), (230, 960)):
        o.append('<circle cx="%d" cy="%d" r="4" fill="#FFE7A8" filter="%s"/>' % (x_, y_, d.glow(6, "#FFE7A8", 0.9)))
    o.append(corners(d, 30, 30, 1050, 1320, 0.75, sw=2.5))
    return d.svg("".join(o)), spec("E-anniversary-1", (150, 100, 930, 600), "gold", "#F6F1FF", "#F2C45A", "dark", "script")


# ------------------------------------------------------------------ 2 candle-lit dinner (warm amber room)
def card2():
    d = Doc(52)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.rg([(0, "#7A3A1E"), (0.55, "#3E1A0E"), (1, "#1E0A05")], 0.5, 0.72, 0.9)]
    o.append('<rect width="1080" height="1350" fill="%s"/>' % damask_pattern(d, "#E9B949", None, 150, 0.07))
    # curtains
    for sg in (-1, 1):
        x0 = 0 if sg < 0 else 1080
        cur = "M%d,0 L%d,0 C%d,300 %d,700 %d,1260 L%d,1260Z" % (x0, x0 - sg * 170, x0 - sg * 150, x0 - sg * 60, x0 - sg * 120, x0)
        gc = d.lg([(0, "#8E0E2A"), (0.5, "#5A0618"), (1, "#8E0E2A")], 0, 0, 1, 0, key="cur")
        o.append('<path d="%s" fill="%s"/>' % (cur, gc))
        for k in range(4):
            o.append('<path d="M%d,0 C%d,300 %d,700 %d,1260" stroke="#000" stroke-opacity=".2" stroke-width="8" fill="none"/>' % (x0 - sg * (30 + k * 32), x0 - sg * (30 + k * 30), x0 - sg * (10 + k * 12), x0 - sg * (20 + k * 24)))
        o.append('<path d="M%d,640 C%d,660 %d,680 %d,700" stroke="%s" stroke-width="10" stroke-linecap="round" fill="none"/>' % (x0, x0 - sg * 80, x0 - sg * 140, x0 - sg * 100, d.gold()))
        o.append(tassel(d, x0 - sg * 100, 700, 0.9, "#8E0E2A"))
    # valance
    o.append('<path d="M0,0 L1080,0 L1080,50 ' + " ".join("Q%s,110 %s,50" % (n(1080 - i * 108 - 54), n(1080 - i * 108 - 108)) for i in range(10)) + ' Z" fill="%s"/>' % d.lg([(0, "#9E1030"), (1, "#5A0618")]))
    o.append('<path d="M0,50 ' + " ".join("Q%s,110 %s,50" % (n(i * 108 + 54), n(i * 108 + 108)) for i in range(10)) + '" stroke="%s" stroke-width="4" fill="none"/>' % d.gold())
    o.append(fairy_lights(d, 60, 70, 1020, 70, 60, 22))
    o.append(bokeh(d, d.rnd, 22, 160, 700, 920, 900, 8, 22, ["#FFD27A", "#FFB347"], 0.15, 0.4))
    o.append(candle_table(d, 540, 1262, 1.2, drink="#F28A5A"))
    o.append('<rect x="0" y="1262" width="1080" height="88" fill="%s"/><rect x="0" y="1258" width="1080" height="5" fill="%s"/>' % (d.lg([(0, "#2A0E06"), (1, "#140602")]), d.gold()))
    rr = random.Random(9)
    o.append(petals_(d, rr, 22, 200, 1268, 880, 1300))
    return d.svg("".join(o)), spec("E-anniversary-2", (190, 140, 890, 600), "gold", "#FFF3E0", "#FFC56B", "dark", "script")


def petals_(d, rr, cnt, x0, y0, x1, y1, cols=("#C21F3A", "#E24A5E", "#86163A")):
    o = []
    for i in range(cnt):
        x, y = rr.uniform(x0, x1), rr.uniform(y0, y1)
        if 330 < x < 750 and y > 1272:
            continue
        o.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" transform="rotate(%s %s %s)"/>' % (n(x), n(y), n(rr.uniform(6, 10)), n(rr.uniform(3, 6)), rr.choice(cols), rr.randint(0, 180), n(x), n(y)))
    return "".join(o)


# ------------------------------------------------------------------ 3 anniversary cake, blush
def card3():
    d = Doc(53)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.lg([(0, "#FFF1EE"), (0.6, "#F9D9D6"), (1, "#EDB5B6")])]
    o.append('<rect width="1080" height="1350" fill="#fff" filter="%s"/>' % d.silk(0.08, "#FFFFFF"))
    # pearl strands draping from the top
    for (x1, x2, sag) in ((-20, 560, 70), (520, 1100, 70), (-20, 1100, 150)):
        fn = swag_fn(x1, 0, x2, 0, sag)
        for i, ((x, y), a) in enumerate(sample(fn, 16)):
            o.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(x), n(y), 6 if i % 4 else 8, d.rg([(0, "#FFFFFF"), (1, "#E6D2C8")], 0.35, 0.35, 0.7, key="pearl")))
    o.append(heart_confetti(d, random.Random(4), 60, 0, 120, 1080, 1260, ["#E9C46A", "#F2A7C1", "#FFFFFF"], 6, 14, avoid=(110, 110, 970, 640)))
    o.append(glass(d, 110, 110, 860, 530, 44, "#FFFDFB", 0.9, "#E6A9B0", 0.12))
    o.append('<ellipse cx="540" cy="1100" rx="420" ry="170" fill="%s"/>' % d.rg([(0, "#FFFFFF", .8), (1, "#FFFFFF", 0)]))
    o.append(cake(d, 540, 1262, 0.85))
    o.append('<rect x="0" y="1262" width="1080" height="88" fill="%s"/><rect x="0" y="1258" width="1080" height="5" fill="%s"/>' % (d.lg([(0, "#D98A96"), (1, "#B8687A")]), d.gold()))
    return d.svg("".join(o)), spec("E-anniversary-3", (160, 150, 920, 610), "#A3284E", "#3A1E26", "#9E2A4A", "light", "script", bg="#FFFBF9")


# ------------------------------------------------------------------ 4 bouquet + rounded photo, peach
def card4():
    d = Doc(54)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.lg([(0, "#FFE9DC"), (0.5, "#FBD2BC"), (1, "#F2B498")])]
    wc = d.watercolor(6, 60)
    for (x_, y_, r_, c) in ((900, 180, 260, "#FFC9B0"), (120, 700, 200, "#FFDCC8"), (980, 1250, 240, "#F7B89C")):
        o.append('<circle cx="%d" cy="%d" r="%d" fill="%s" opacity=".6" filter="%s"/>' % (x_, y_, r_, c, wc))
    ph = {"shape": "rounded", "x": 500, "y": 90, "w": 470, "h": 420}
    o.append(photo_slot(d, ph, "#FFF8F2", "#F6E2D6", "#E0B8A4", ring_w=14, ring="#FFFFFF", inner="#D9A48A"))
    o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="36" fill="none" stroke="%s" stroke-width="3"/>' % (ph["x"] - 26, ph["y"] - 26, ph["w"] + 52, ph["h"] + 52, d.lg(ROSEGOLD, 0, 0, 1, 1, key="rgf")))
    o.append(g(bouquet(d, 0, 0, 0.92, ("#FFF4EA", "#E8C8AE"), ("peach", "blush", "white", "coral"), ("#E8A48A", "#B8624A"), 5), 250, 470, 1, -18))
    o.append(glass(d, 90, 600, 900, 640, 40, "#FFFCF8", 0.92, "#E3B39C", 0.14))
    o.append(heart_confetti(d, random.Random(8), 26, 0, 540, 1080, 1340, ["#E8A48A", "#FFFFFF"], 6, 12, avoid=(80, 590, 1000, 1250)))
    return d.svg("".join(o)), spec("E-anniversary-4", (150, 640, 930, 1200), "#A33A22", "#3A2420", "#9A3E24", "light", "script", photo=ph, bg="#FFFBF6")


# ------------------------------------------------------------------ 5 photo collage board, sage
def card5():
    d = Doc(55)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.lg([(0, "#E6EEE2"), (1, "#C6D6C0")])]
    o.append('<rect width="1080" height="1350" fill="#fff" filter="%s"/>' % d.grain(0.8, 0.06, "#5A6A50"))
    # back collage cards (illustrated, tilted)
    back = [(150, 160, 300, 260, -9, "#F4D9D2"), (650, 140, 320, 250, 8, "#D8E6F0")]
    for (x_, y_, w_, h_, a, c) in back:
        inner = '<rect x="%d" y="%d" width="%d" height="%d" fill="#FFFFFF"/>' % (x_, y_, w_, h_)
        inner += '<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x_ + 14, y_ + 14, w_ - 28, h_ - 28, c)
        inner += '<path d="%s" fill="#FFFFFF" opacity=".7"/>' % shape_d("heart", x_ + w_ / 2 - 40, y_ + h_ / 2 - 36, 80, 72)
        o.append('<g transform="rotate(%s %s %s)" filter="%s">%s</g>' % (a, x_ + w_ / 2, y_ + h_ / 2, d.shadow(0, 8, 10, "#2F3A2A", .25), inner))
    ph = {"shape": "rect", "x": 250, "y": 110, "w": 580, "h": 400}
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#FFFFFF" filter="%s"/>' % (ph["x"] - 20, ph["y"] - 20, ph["w"] + 40, ph["h"] + 40, d.shadow(0, 12, 16, "#2F3A2A", .3)))
    o.append(photo_slot(d, ph, "#F8F6F0", "#E6E2D6", "#C9C0AA", ring_w=4, ring="#FFFFFF", inner="#C9B89A", shadow=False))
    # washi tapes
    for (x_, y_, a, c) in ((250, 96, -30, "#E8A4B0"), (830, 96, 30, "#9CC4B0"), (820, 520, -25, "#E8C87A")):
        o.append('<rect x="%d" y="%d" width="130" height="36" fill="%s" opacity=".85" transform="rotate(%d %d %d)"/>' % (x_ - 65, y_ - 18, c, a, x_, y_))
        o.append('<rect x="%d" y="%d" width="130" height="36" fill="%s" transform="rotate(%d %d %d)"/>' % (x_ - 65, y_ - 18, d.pattern(12, 12, '<circle cx="6" cy="6" r="2" fill="#fff" opacity=".6"/>', key="washi"), a, x_, y_))
    # eucalyptus sprigs
    for (x_, y_, a, s) in ((110, 560, 20, 1), (980, 560, -20, 1), (1000, 1230, 200, 0.9), (80, 1230, 160, 0.9)):
        sp = ['<path d="M0,0 C10,-100 0,-200 -10,-280" stroke="#5E7A62" stroke-width="4" fill="none"/>']
        for k in range(9):
            yy = -24 - k * 30
            for sg in (-1, 1):
                sp.append('<ellipse cx="%s" cy="%s" rx="18" ry="13" fill="%s" stroke="#5E7A62" stroke-width="1.2" transform="rotate(%s %s %s)"/>' % (
                    n(sg * 18 - k * 1.2), n(yy), "#A9C4B0" if k % 2 else "#94B39C", sg * 25, n(sg * 18 - k * 1.2), n(yy)))
        o.append(g("".join(sp), x_, y_, s, a))
    # note card
    o.append('<rect x="100" y="620" width="880" height="620" rx="10" fill="#FFFEFA" filter="%s"/>' % d.shadow(0, 10, 16, "#2F3A2A", .22))
    o.append('<rect x="120" y="640" width="840" height="580" rx="6" fill="none" stroke="#9CB8A4" stroke-width="2" stroke-dasharray="10 8"/>')
    o.append(g('<path d="M0,0 C14,-6 30,-6 40,4" stroke="#C9A46A" stroke-width="3" fill="none"/>' + '<circle cx="0" cy="0" r="10" fill="%s"/>' % d.gold(), 540, 624))
    return d.svg("".join(o)), spec("E-anniversary-5", (160, 680, 920, 1180), "#2F5A3E", "#26302A", "#8A5A2A", "light", "script", photo=ph, bg="#FFFEFA")


# ------------------------------------------------------------------ 6 pocket watch + infinity chain, ivory
def gear(cx, cy, R, teeth, col, op, sw=3):
    pts = []
    for i in range(teeth * 4):
        a = 2 * math.pi * i / (teeth * 4)
        r_ = R if (i % 4) in (1, 2) else R * 0.86
        pts.append((cx + r_ * math.cos(a), cy + r_ * math.sin(a)))
    return ('<path d="M%sZ" fill="none" stroke="%s" stroke-width="%s" opacity="%s"/>' % (" L".join("%s,%s" % (n(a), n(b)) for a, b in pts), col, sw, op) +
            '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="%s" opacity="%s"/>' % (n(cx), n(cy), n(R * 0.35), col, sw, op))


def card6():
    d = Doc(56)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.rg([(0, "#FFFDF6"), (1, "#EFE3CC")], 0.5, 0.35, 0.9)]
    o.append('<rect width="1080" height="1350" fill="%s"/>' % damask_pattern(d, "#D8C3A5", None, 110, 0.3))
    for (x_, y_, R, t) in ((80, 760, 120, 18), (1000, 700, 90, 14), (960, 1240, 150, 22), (120, 1270, 80, 12), (900, 860, 50, 10)):
        o.append(gear(x_, y_, R, t, "#C8A46A", 0.35))
    o.append('<rect x="24" y="24" width="1032" height="1302" fill="none" stroke="%s" stroke-width="3"/>' % d.gold())
    o.append('<rect x="38" y="38" width="1004" height="1274" fill="none" stroke="#1E2A44" stroke-width="1.2"/>')
    o.append(corners(d, 50, 50, 1030, 1300, 0.6, sw=2.5))
    # hero: watch + infinity chain
    o.append(chain(d, infinity_fn(700, 990, 240), 16))
    o.append(pocket_watch(d, 330, 990, 185))
    # roses tucked by the watch
    for (x_, y_, r_, v) in ((180, 1170, 30, "wine"), (230, 1200, 22, "blush"), (140, 1130, 20, "blush"), (520, 1160, 24, "wine"), (555, 1135, 17, "blush")):
        o.append(leaf(d, x_ + 20, y_ + 10, 44, 13, 70, "#6E8F6A", "#2F4E2A") + rose(d, x_, y_, r_, v))
    return d.svg("".join(o)), spec("E-anniversary-6", (150, 110, 930, 640), "#1E2A44", "#26221C", "#8A5A12", "light", "classic", bg="#FCF7EC")


# ------------------------------------------------------------------ 7 love lock on bridge railing, sunset
def card7():
    d = Doc(57)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.lg([(0, "#FFF4EC"), (0.4, "#FBD7CC"), (0.62, "#F2A6A0"), (0.8, "#9A6A9E"), (1, "#3E3A6E")])]
    o.append('<circle cx="820" cy="780" r="220" fill="%s"/>' % d.rg([(0, "#FFF3D6", .9), (1, "#FFF3D6", 0)]))
    # distant city/bridge silhouette
    sk = "M0,900 "
    rr = random.Random(12)
    x = 0
    while x < 1080:
        w_ = rr.uniform(30, 70)
        h_ = rr.uniform(20, 90)
        sk += "L%s,%s L%s,%s " % (n(x), n(900 - h_), n(x + w_), n(900 - h_))
        x += w_
    sk += "L1080,900 L1080,960 L0,960Z"
    o.append('<path d="%s" fill="#6E5A8E" opacity=".55"/>' % sk)
    o.append('<rect x="0" y="930" width="1080" height="420" fill="%s"/>' % d.lg([(0, "#5A4E86"), (1, "#2A2650")]))
    for k in range(12):
        o.append('<path d="M%d,%d h%d" stroke="#FFD9C0" stroke-opacity="%s" stroke-width="2"/>' % (700 - k * 4, 950 + k * 14, 220 - k * 8, n(0.5 - k * 0.035)))
    # railing
    rail = d.lg([(0, "#3A3A4E"), (0.5, "#8A8AA0"), (1, "#2A2A3A")], 0, 0, 0, 1, key="rail")
    for yy in (880, 1100):
        o.append('<rect x="0" y="%d" width="1080" height="22" fill="%s"/>' % (yy, rail))
    for xx in range(20, 1080, 90):
        o.append('<rect x="%d" y="880" width="12" height="400" fill="%s"/>' % (xx, d.lg([(0, "#2A2A3A"), (0.5, "#8A8AA0"), (1, "#2A2A3A")], 0, 0, 1, 0, key="railv")))
    # mesh
    o.append('<rect x="0" y="902" width="1080" height="198" fill="%s"/>' % d.pattern(30, 30, '<path d="M0,0 L30,30 M30,0 L0,30" stroke="#4A4A60" stroke-width="1.6"/>', key="mesh"))
    # small locks on the mesh
    cols = ["#E9C46A", "#C0406E", "#5A9AC0", "#E8845A", "#9CC4B0", "#C9A0DC", "#D7263D"]
    for i in range(16):
        x_ = rr.uniform(40, 1040)
        if 350 < x_ < 730:
            continue
        y_ = rr.uniform(930, 1060)
        c = rr.choice(cols)
        sh = rr.choice(["rounded", "heart"])
        o.append('<path d="M%s,%s c0,-26 30,-26 30,0" stroke="#9A9AB0" stroke-width="5" fill="none"/>' % (n(x_ - 15), n(y_)))
        o.append('<path d="%s" fill="%s" stroke="#000" stroke-opacity=".25"/>' % (shape_d("heart" if sh == "heart" else "rect", x_ - 22, y_ - 2, 44, 38), c))
    # hero lock + key on ribbon
    o.append('<path d="M540,720 C520,800 500,830 470,870" stroke="#D7263D" stroke-width="8" fill="none"/>')
    o.append(love_lock(d, 540, 1020, 1.25))
    o.append('<path d="M640,1040 C700,1060 720,1110 760,1130" stroke="#D7263D" stroke-width="6" fill="none"/>')
    o.append(heart_key(d, 800, 1110, 0.78, -30))
    o.append(satin_bow(d, 640, 1040, 0.45, ("#E23A5E", "#9E1030")))
    o.append('<rect x="0" y="1280" width="1080" height="70" fill="%s"/>' % d.lg([(0, "#2A2650"), (1, "#16142E")]))
    o.append(glass(d, 90, 80, 900, 580, 40, "#FFFCFA", 0.86, "#E6A9B0", 0.15))
    return d.svg("".join(o)), spec("E-anniversary-7", (150, 120, 930, 620), "#8E1B3A", "#2E2233", "#9E2A4A", "light", "script", bg="#FDF3F0")


# ------------------------------------------------------------------ 8 twin coffee cups, cafe
def card8():
    d = Doc(58)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.lg([(0, "#F6ECDD"), (1, "#E8D6BC")])]
    # wall panel stripes
    o.append('<rect width="1080" height="880" fill="%s"/>' % d.pattern(60, 60, '<rect width="30" height="60" fill="#EFE0C8" opacity=".6"/>', key="strp"))
    o.append(fairy_lights(d, -20, 40, 1100, 40, 70, 20, "#FFE0A0", "#6E4A2A"))
    # shelf with small plants
    o.append('<rect x="0" y="880" width="1080" height="16" fill="#C9A77E"/>')
    # table
    wood = d.lg([(0, "#9A6A3E"), (0.5, "#7A4E2A"), (1, "#5A361C")], 0, 0, 0, 1, key="wood")
    o.append('<path d="M-40,1030 L1120,1030 L1120,1350 L-40,1350Z" fill="%s"/>' % wood)
    for k in range(7):
        o.append('<path d="M0,%d C300,%d 700,%d 1080,%d" stroke="#3E2410" stroke-opacity=".25" stroke-width="2" fill="none"/>' % (1060 + k * 36, 1052 + k * 36, 1070 + k * 36, 1058 + k * 36))
    o.append('<rect x="0" y="1024" width="1080" height="10" fill="#B8864E"/>')
    # steam heart + cups
    o.append(steam_heart(d, 380, 900, 700, 900, 640, "#FFFFFF", 0.95))
    o.append(g(steam_heart(d, 380, 900, 700, 900, 640, "#A8805A", 0.25), 3, 4))
    o.append(coffee_cup(d, 350, 1190, 1.15, band="#B3123E"))
    o.append(coffee_cup(d, 730, 1190, 1.15, flip=True, band="#1E6A56"))
    # biscuits & roses on table
    o.append(rose(d, 130, 1180, 26, "red") + rose(d, 170, 1210, 18, "pink") + leaf(d, 110, 1216, 46, 13, 220, "#6E9E5A", "#2F5E2A"))
    for (x_, y_) in ((930, 1190), (970, 1220)):
        o.append('<circle cx="%d" cy="%d" r="30" fill="#D9A060" stroke="#A8702E" stroke-width="3"/>' % (x_, y_) + dots_ring(6, 16, 2.5, "#8A5A2A", x_, y_))
    o.append(glass(d, 90, 120, 900, 540, 36, "#FFFCF6", 0.88, "#C9A77E", 0.14))
    return d.svg("".join(o)), spec("E-anniversary-8", (150, 160, 930, 620), "#6E3A1A", "#33241A", "#8A4A1A", "light", "script", bg="#FDF7EE")


# ------------------------------------------------------------------ 9 heart photo in infinity ribbon, wine
def card9():
    d = Doc(59)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.rg([(0, "#7A1638"), (0.6, "#4A0A22"), (1, "#260411")], 0.5, 0.3, 0.9)]
    o.append('<rect width="1080" height="1350" fill="%s"/>' % d.pattern(40, 40, '<path d="%s" fill="#F2C45A" opacity=".07"/>' % shape_d("heart", 12, 13, 16, 14), key="hp"))
    o.append(bokeh(d, d.rnd, 24, 0, 0, 1080, 560, 8, 26, ["#FFD6E4", "#F2C45A"], 0.12, 0.35))
    # infinity ribbon behind heart
    rg = d.lg(ROSEGOLD, 0, 0, 1, 1, key="rgr")
    fn = infinity_fn(540, 300, 440)
    o.append('<path d="%s" fill="%s" opacity=".95"/>' % (tube_d(fn, 16, 16, 300), rg))
    for i, ((x, y), a) in enumerate(sample(fn, 60, 800)):
        if abs(x - 540) > 220:
            o.append(rose(d, x, y, 12, ["blush", "pink", "wine"][i % 3], i * 30))
    ph = {"shape": "heart", "x": 360, "y": 110, "w": 360, "h": 330}
    o.append('<path d="%s" fill="#000" opacity=".4" filter="%s"/>' % (shape_d("heart", 340, 110, 400, 380), d.blur(16)))
    o.append(photo_slot(d, ph, "#FFF4F4", "#F4D6DA", "#D9A0AA", ring_w=14, ring=d.gold(), inner="#6E0A28"))
    pts = heart_pts(ph["x"] - 14, ph["y"] - 14, ph["w"] + 28, ph["h"] + 28, 300)
    o.append(flower_ring(d, [p + (0,) for p in pts[150:230:9]], 13, "rose", ("wine", "red", "blush"), 2, cx=540, cy=260))
    # lace bottom
    o.append('<path d="%s" fill="%s"/>' % ("M0,1350 L0,1300 " + " ".join("Q%s,1268 %s,1300" % (n(i * 60 + 30), n(i * 60 + 60)) for i in range(18)) + " L1080,1350Z", d.gold()))
    o.append('<path d="%s" fill="#260411"/>' % ("M0,1350 L0,1312 " + " ".join("Q%s,1284 %s,1312" % (n(i * 60 + 30), n(i * 60 + 60)) for i in range(18)) + " L1080,1350Z"))
    o.append(g(flourish(d, 0, 0, 0.6, 0, sw=2.5) + flourish(d, 0, 0, 0.6, 90, sw=2.5), 0, 0))
    o.append(flourish(d, 36, 580, 0.5, 0, sw=2.5) + flourish(d, 1044, 580, 0.5, 90, sw=2.5))
    return d.svg("".join(o)), spec("E-anniversary-9", (150, 600, 930, 1220), "gold", "#FFF1F4", "#F2C45A", "dark", "script", photo=ph)


# ------------------------------------------------------------------ 10 candlesticks + oval photo (bottom), lavender dusk
def candlestick(d, x, by, s=1):
    gf = d.lg(GOLD, 0, 0, 1, 0, key="goldh")
    o = []
    o.append('<ellipse cx="0" cy="0" rx="70" ry="14" fill="%s"/>' % gf)
    o.append('<path d="M-60,-4 C-40,-30 -20,-40 -14,-70 L14,-70 C20,-40 40,-30 60,-4Z" fill="%s"/>' % gf)
    for k, (w_, y_) in enumerate([(22, -110), (30, -150), (16, -230), (26, -270)]):
        o.append('<ellipse cx="0" cy="%d" rx="%d" ry="%d" fill="%s"/>' % (y_, w_, 12 if k % 2 else 26, gf))
    o.append('<rect x="-10" y="-300" width="20" height="230" fill="%s"/>' % gf)
    o.append('<path d="M-44,-300 L44,-300 L30,-318 L-30,-318Z" fill="%s"/>' % gf)
    o.append(candle(d, 0, -316, 38, 200, ("#FFF3F6", "#E6CCD6")))
    return g("".join(o), x, by, s)


def card10():
    d = Doc(60)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.lg([(0, "#F3ECF8"), (0.5, "#D8C8EA"), (1, "#8E76B4")])]
    o.append('<rect width="1080" height="1350" fill="%s"/>' % damask_pattern(d, "#FFFFFF", None, 120, 0.3))
    o.append(glass(d, 80, 60, 920, 640, 40, "#FFFFFF", 0.88, "#B8A0D6", 0.15))
    ph = {"shape": "oval", "x": 385, "y": 800, "w": 310, "h": 400}
    o.append('<ellipse cx="540" cy="1000" rx="260" ry="290" fill="%s"/>' % d.rg([(0, "#FFE7A8", .5), (1, "#FFE7A8", 0)]))
    ring = ellipse_pts(540, 1000, 180, 224, 46)
    o.append(flower_ring(d, [p for i, p in enumerate(ring) if 14 <= i <= 32], 14, "rose", ("lilac", "white", "pink"), 2, cx=540, cy=1000, leafcol=("#8FB08A", "#4E7A52")))
    o.append(photo_slot(d, ph, "#FBF6FF", "#EBDDF6", "#C9B2E6", ring_w=12, inner="#6E4A12"))
    o.append(satin_bow(d, 540, 772, 0.55, ("#B8A0D6", "#6E4E9E")))
    o.append(candlestick(d, 210, 1262, 1.0) + candlestick(d, 870, 1262, 1.0))
    o.append(fairy_lights(d, 60, 730, 1020, 730, 60, 20, "#FFE7A8", "#8E76B4"))
    o.append('<rect x="0" y="1262" width="1080" height="88" fill="%s"/><rect x="0" y="1258" width="1080" height="5" fill="%s"/>' % (d.lg([(0, "#5E4A86"), (1, "#3E2E62")]), d.gold()))
    return d.svg("".join(o)), spec("E-anniversary-10", (150, 110, 930, 650), "#5A2A86", "#2E2240", "#7A3A8A", "light", "script", photo=ph, bg="#FAF7FD")


CARDS = [card1, card2, card3, card4, card5, card6, card7, card8, card9, card10]

if __name__ == "__main__":
    only = [int(a) for a in sys.argv[1:]]
    arts, specs = {}, []
    for i, fn in enumerate(CARDS, 1):
        svg, sp = fn()
        specs.append(sp)
        if not only or i in only:
            arts[sp["id"]] = svg
    render_cards(arts)
    write_specs(CAT, specs)
