"""wedding (wishes): 10 premium wedding-wish card designs (lib_c family).
Motifs: varmala couple, pheras around agni, gathbandhan knot, rose-petal shower, mehendi hands, doli."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motifs_wed_c import *
from render import render_cards

CAT = "wedding"


def glass(d, x, y, w, h, r=36, fill="#FFFFFF", op=0.84, stroke=None):
    o = '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" opacity="%s" filter="%s"/>' % (n(x), n(y), n(w), n(h), n(r), fill, op, d.shadow(0, 12, 22, "#000", .22))
    if stroke:
        o += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="%s" stroke-width="2.5"/>' % (n(x + 12), n(y + 12), n(w - 24), n(h - 24), n(max(4, r - 10)), stroke)
    return o


def bush(d, x, y, s, flip, dark, roses=("red", "pink"), seed=1):
    rr = random.Random(seed)
    o = []
    for i in range(46):
        a = rr.uniform(-80, 80)
        rad = rr.uniform(0, 1) ** 0.6
        o.append(leaf(d, 120 * rad * math.sin(math.radians(a)), -20 - 130 * rad * math.cos(math.radians(a)) * 0.8, rr.uniform(40, 64), rr.uniform(16, 24), a + rr.uniform(-40, 40), dark[0], dark[1], vein=False))
    for i in range(9):
        o.append(rose(d, rr.uniform(-100, 100), rr.uniform(-150, -20), rr.uniform(14, 22), rr.choice(roses), rr.randint(0, 360)))
    return g("".join(o), x, y, s, flip=flip)


# ------------------------------------------------------------------ 1 varmala at sunset
def card1():
    d = Doc(31)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.lg([(0, "#6B1B45"), (0.35, "#C2406A"), (0.62, "#F07A6A"), (0.82, "#FFB27A"), (1, "#FFD59A")])]
    o.append('<circle cx="540" cy="1010" r="330" fill="%s"/>' % d.rg([(0, "#FFF6D0", 1), (0.45, "#FFE09A", .9), (1, "#FFB27A", 0)]))
    o.append('<circle cx="540" cy="1010" r="190" fill="#FFF3C8" opacity=".85"/>')
    o.append(rays(540, 1010, 36, 900, "#FFF3C8", 0.08, 4))
    o.append(bokeh(d, d.rnd, 30, 0, 600, 1080, 1250, 5, 18, ["#FFF3C8", "#FFD08A"], 0.2, 0.5))
    o.append(petals(d, random.Random(2), 36, 0, 640, 1080, 1200, 8, 14, ("red", "pink", "coral"), op=(0.6, 0.95)))
    body = "#3A0A22"
    o.append(groom(d, 392, 1262, 1.12, pose="varmala", shade=("#5A1030", 0.28), rim="#FFE3A8"))
    o.append(bride(d, 700, 1262, 1.12, flip=True, pose="varmala", shade=("#5A1030", 0.28), rim="#FFE3A8"))
    o.append(varmala(d, 392 + 108 * 1.12, 1262 - 358 * 1.12, 230, 66, 1, ("red", "wine")))
    o.append(varmala(d, 700 - 98 * 1.12, 1262 - 338 * 1.12, 220, 64, 1, ("pink", "coral"), tilt=-4))
    o.append(bush(d, 90, 1270, 1.1, False, ("#4A1030", "#2A0618"), ("red", "coral"), 3))
    o.append(bush(d, 990, 1270, 1.1, True, ("#4A1030", "#2A0618"), ("red", "coral"), 4))
    o.append('<rect x="0" y="1258" width="1080" height="92" fill="%s"/>' % d.lg([(0, "#3A0A22"), (1, "#22051A")]))
    o.append(glass(d, 84, 56, 912, 552, 40, "#FFF8F4", 0.88, "#D98A96"))
    return d.svg("".join(o)), spec("E-wedding-1", (150, 100, 930, 564), "#8E1B4A", "#3A1A26", "#A3284E", "light", "script", bg="#FDEFEF")


# ------------------------------------------------------------------ 2 pheras around agni (dark)
def card2():
    d = Doc(32)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.rg([(0, "#6E1428"), (0.6, "#3A0716"), (1, "#1C030B")], 0.5, 0.8, 0.9)]
    o.append('<rect width="1080" height="1350" fill="%s"/>' % damask_pattern(d, "#E9B949", None, 140, 0.06))
    o.append(corners(d, 34, 34, 1046, 1316, 0.9, sw=2.5))
    # hanging rose-jasmine strands at edges
    for x_, L in ((70, 360), (120, 250), (960, 250), (1010, 360)):
        for j in range(int(L / 22)):
            o.append(jasmine(d, x_, 20 + j * 22, 8, j * 30) if j % 2 else rose(d, x_, 20 + j * 22, 10, "red" if j % 4 else "wine"))
    # gathbandhan arc behind the fire
    o.append(fabric_band(d, cub((284, 1022), (400, 1160), (660, 1160), (768, 1040)), 22, d.lg([(0, "#FFF3DC"), (1, "#F2C45A")]), d.gold(), None))
    o.append(agni_kund(d, 540, 1256, 1.05))
    body = "#12030A"
    o.append(bride(d, 262, 1256, 0.86, pose="stand", shade=("#1A0308", 0.42), rim="#FFB347"))
    o.append(groom(d, 800, 1256, 0.86, pose="walk", flip=True, shade=("#1A0308", 0.42), rim="#FFB347"))
    o.append('<rect x="0" y="1256" width="1080" height="94" fill="%s"/>' % d.lg([(0, "#2A0510"), (1, "#12020A")]))
    o.append(petals(d, random.Random(3), 26, 60, 1262, 1020, 1300, 8, 12, ("red", "coral"), avoid=(300, 1262, 780, 1350)))
    return d.svg("".join(o)), spec("E-wedding-2", (150, 150, 930, 700), "gold", "#FFF3E6", "#FFC56B", "dark", "script")


# ------------------------------------------------------------------ 3 gathbandhan knot
def card3():
    d = Doc(33)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.lg([(0, "#FBE3E3"), (0.5, "#F6CFD2"), (1, "#EDB7BE")])]
    o.append('<rect width="1080" height="1350" fill="#fff" filter="%s"/>' % d.silk(0.10, "#FFFFFF"))
    o.append('<ellipse cx="540" cy="380" rx="520" ry="360" fill="%s"/>' % d.rg([(0, "#FFF6EE", .9), (1, "#FFF6EE", 0)]))
    o.append(petals(d, random.Random(4), 40, 0, 0, 1080, 700, 9, 16, ("red", "pink", "blush"), op=(0.7, 1)))
    o.append(gathbandhan(d, 540, 330, 1.0))
    rr = random.Random(7)
    for i in range(40):
        x_, y_ = rr.uniform(300, 780), rr.uniform(420, 680)
        o.append('<ellipse cx="%s" cy="%s" rx="4" ry="2" fill="#FFFDF4" stroke="#E0C9A0" stroke-width=".6" transform="rotate(%s %s %s)"/>' % (n(x_), n(y_), rr.randint(0, 180), n(x_), n(y_)))
    for (x_, y_) in ((250, 640), (830, 610), (420, 690)):
        o.append('<circle cx="%d" cy="%d" r="14" fill="%s" stroke="#8A5A12" stroke-width="1.5"/>' % (x_, y_, d.gold()))
    # panel
    o.append('<path d="M100,760 Q540,700 980,760 L980,1250 L100,1250Z" fill="#FFFBF7" filter="%s"/>' % d.shadow(0, -6, 18, "#8E1B3A", .18))
    o.append('<path d="M122,782 Q540,724 958,782 L958,1228 L122,1228Z" fill="none" stroke="#D98A96" stroke-width="2"/>')
    o.append('<path d="M130,790 Q540,733 950,790" fill="none" stroke="%s" stroke-width="2.5"/>' % d.gold())
    return d.svg("".join(o)), spec("E-wedding-3", (150, 790, 930, 1210), "#9E1B45", "#3A1E26", "#A3284E", "light", "script", bg="#FFFBF7")


# ------------------------------------------------------------------ 4 heart photo + rose-petal shower
def card4():
    d = Doc(34)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.rg([(0, "#E7A3AE"), (0.55, "#B8506A"), (1, "#6E1A36")], 0.5, 0.25, 0.95)]
    o.append(bokeh(d, d.rnd, 26, 0, 0, 1080, 560, 8, 26, ["#FFE0E6", "#FFFFFF"], 0.15, 0.4))
    ph = {"shape": "heart", "x": 350, "y": 96, "w": 380, "h": 350}
    pts = heart_pts(ph["x"] - 26, ph["y"] - 26, ph["w"] + 52, ph["h"] + 52, 400)
    o.append('<path d="%s" fill="#5A0F28" opacity=".35" filter="%s"/>' % (shape_d("heart", ph["x"] - 30, ph["y"] - 20, ph["w"] + 60, ph["h"] + 60), d.blur(14)))
    o.append(flower_ring(d, path_pts(pts, 22), 14, "rose", ("red", "wine", "pink", "red"), 3, cx=540, cy=260, leafcol=("#6E9E5A", "#2F5E2A")))
    o.append(photo_slot(d, ph, "#FFF4F4", "#F4D6DA", "#D9A0AA", ring_w=9, ring=d.lg(ROSEGOLD, 0, 0, 1, 1), inner="#8E3A4A"))
    o.append(petals(d, random.Random(5), 90, 0, 0, 1080, 560, 8, 16, ("red", "pink", "wine", "blush"), avoid=(330, 70, 750, 480)))
    o.append(parchment_arch(d, 88, 540, 904, 740))
    o.append(petals(d, random.Random(6), 30, 0, 540, 1080, 1340, 8, 14, ("red", "pink", "wine"), avoid=(120, 560, 960, 1300)))
    return d.svg("".join(o)), spec("E-wedding-4", (150, 620, 930, 1230), "#8E1B3A", "#3A1E26", "#9E2A4A", "light", "script", photo=ph, bg="#FFF8F4")


def parchment_arch(d, x, y, w, h):
    top = "M%s,%s Q%s,%s %s,%s L%s,%s L%s,%sZ" % (n(x), n(y + 60), n(x + w / 2), n(y - 30), n(x + w), n(y + 60), n(x + w), n(y + h), n(x), n(y + h))
    o = '<path d="%s" fill="%s" filter="%s"/>' % (top, d.rg([(0, "#FFFBF6"), (1, "#FBEDE6")], 0.5, 0.4, 0.8), d.shadow(0, 12, 20, "#3A0A1A", .35))
    o += '<path d="M%s,%s Q%s,%s %s,%s L%s,%s L%s,%sZ" fill="none" stroke="%s" stroke-width="3"/>' % (
        n(x + 18), n(y + 74), n(x + w / 2), n(y - 10), n(x + w - 18), n(y + 74), n(x + w - 18), n(y + h - 18), n(x + 18), n(y + h - 18), d.lg(ROSEGOLD, 0, 0, 1, 1, key="rgf"))
    return o


# ------------------------------------------------------------------ 5 mehendi hands
def card5():
    d = Doc(35)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.lg([(0, "#EEF3E6"), (0.6, "#CFDDC4"), (1, "#A9C09C")])]
    o.append(bokeh(d, d.rnd, 30, 0, 700, 1080, 1260, 10, 34, ["#FFFFFF", "#F6E7B8"], 0.2, 0.5))
    rr = random.Random(9)
    for i in range(18):
        x_ = rr.choice([rr.uniform(0, 150), rr.uniform(930, 1080)])
        o.append(leaf(d, x_, rr.uniform(760, 1250), rr.uniform(50, 80), 16, rr.uniform(-60, 60), "#8FB08A", "#4E7A52"))
    o.append(glass(d, 84, 56, 912, 640, 40, "#FFFDF6", 0.9, "#B8A36A"))
    o.append(mehendi_hand(d, 400, 1172, 1.08, rot=-10))
    o.append(mehendi_hand(d, 680, 1172, 1.08, flip=True, rot=10))
    o.append(rose(d, 540, 1150, 22, "red") + rose(d, 510, 1170, 16, "pink") + rose(d, 570, 1172, 16, "pink") + jasmine(d, 540, 1186, 9))
    o.append('<rect x="0" y="1262" width="1080" height="88" fill="%s"/>' % d.lg([(0, "#6E8F62"), (1, "#4E6E46")]))
    o.append('<rect x="0" y="1258" width="1080" height="6" fill="%s"/>' % d.gold())
    return d.svg("".join(o)), spec("E-wedding-5", (150, 100, 930, 652), "#2F5A2A", "#2A2A22", "#8A5A0A", "light", "script", bg="#FDFBF2")


# ------------------------------------------------------------------ 6 doli with flowers
def card6():
    d = Doc(36)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.lg([(0, "#F4ECFA"), (0.45, "#D9C6EC"), (0.8, "#A98BCB"), (1, "#7C62A6")])]
    o.append('<ellipse cx="540" cy="1040" rx="520" ry="260" fill="%s"/>' % d.rg([(0, "#FFE6F0", .8), (1, "#FFE6F0", 0)]))
    o.append(bokeh(d, d.rnd, 30, 0, 700, 1080, 1250, 6, 20, ["#FFFFFF", "#FFD6E4"], 0.2, 0.55))
    # petal carpet in perspective
    o.append('<path d="M380,1262 L700,1262 L620,1150 L460,1150Z" fill="#FFD6E4" opacity=".45"/>')
    o.append(petals(d, random.Random(12), 70, 250, 1180, 830, 1262, 7, 12, ("red", "pink", "coral")))
    o.append(doli(d, 540, 1250, 1.2, ("#B3123E", "#6E0A28"), ("red", "pink")))
    o.append(petals(d, random.Random(13), 50, 0, 700, 1080, 1240, 8, 14, ("pink", "red", "lilac"), avoid=(120, 620, 960, 1250)))
    for x_, L in ((40, 520), (1040, 520)):
        for j in range(int(L / 22)):
            o.append(jasmine(d, x_, 20 + j * 22, 8, j * 30) if j % 2 else rose(d, x_, 20 + j * 22, 10, "pink" if j % 4 else "red"))
    o.append('<rect x="0" y="1262" width="1080" height="88" fill="%s"/>' % d.lg([(0, "#5E4A86"), (1, "#3E2E62")]))
    o.append(glass(d, 90, 50, 900, 580, 40, "#FFFFFF", 0.84, "#B8A0D6"))
    return d.svg("".join(o)), spec("E-wedding-6", (150, 94, 930, 586), "#5A2A86", "#2E2240", "#8E2A6A", "light", "script", bg="#F8F4FC")


# ------------------------------------------------------------------ 7 album photo + chunri knot
def card7():
    d = Doc(37)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.rg([(0, "#FFFDF8"), (1, "#F6E8DE")], 0.5, 0.5, 0.8)]
    o.append('<rect width="1080" height="1350" fill="#fff" filter="%s"/>' % d.grain(0.8, 0.05, "#8A6A5A"))
    wc = d.watercolor(4, 60)
    for (x_, y_, r_, c) in ((80, 120, 220, "#F4B8C2"), (1000, 520, 200, "#F9CFC2"), (60, 1240, 240, "#F4B8C2"), (1020, 1300, 200, "#F7D6B8")):
        o.append('<circle cx="%d" cy="%d" r="%d" fill="%s" opacity=".55" filter="%s"/>' % (x_, y_, r_, c, wc))
    ph = {"shape": "rect", "x": 250, "y": 110, "w": 580, "h": 400}
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#FFFFFF" filter="%s" transform="rotate(-2 540 310)"/>' % (ph["x"] - 30, ph["y"] - 30, ph["w"] + 60, ph["h"] + 60, d.shadow(0, 12, 16, "#5A2A2A", .3)))
    o.append(photo_slot(d, ph, "#FBF3F0", "#F1DCD6", "#D9B0AA", ring_w=6, inner="#B8862A", shadow=False))
    # chunri ribbon across top-left corner with knot
    gr = d.lg([(0, "#D7263D"), (1, "#8E0A1E")], 0, 0, 1, 1, key="rib7")
    o.append(fabric_band(d, cub((150, 40), (200, 90), (230, 120), (290, 170)), 60, gr, d.gold(), "#FFD23F"))
    o.append(fabric_band(d, cub((290, 170), (240, 220), (200, 300), (190, 380)), 50, gr, d.gold(), "#FFD23F"))
    o.append(fabric_band(d, cub((290, 170), (340, 200), (360, 260), (330, 330)), 46, gr, d.gold(), "#FFD23F"))
    o.append('<ellipse cx="290" cy="170" rx="34" ry="28" fill="%s" stroke="%s" stroke-width="3" transform="rotate(40 290 170)"/>' % (gr, d.gold()))
    for k in range(7):
        o.append('<line x1="%d" y1="380" x2="%d" y2="410" stroke="%s" stroke-width="3"/>' % (172 + k * 6, 170 + k * 6, d.gold()))
    for (cx_, cy_, sc) in ((850, 110, 1.0), (240, 520, 0.8)):
        rr = random.Random(int(cx_))
        cl = []
        for k in range(10):
            cl.append(leaf(d, rr.uniform(-70, 70), rr.uniform(-50, 50), rr.uniform(40, 60), 15, rr.uniform(0, 360), "#6E9E5A", "#2F5E2A"))
        for k, (dx, dy, r_, v) in enumerate([(0, 0, 36, "red"), (-44, -16, 24, "pink"), (40, 24, 26, "pink"), (-20, 40, 18, "coral"), (46, -30, 16, "red")]):
            cl.append(rose(d, dx, dy, r_, v, k * 50))
        cl.append(jasmine(d, -46, 30, 11) + jasmine(d, 20, -40, 10))
        o.append(g("".join(cl), cx_, cy_, sc))
    o.append(petals(d, random.Random(14), 80, 0, 0, 1080, 1350, 8, 15, ("red", "pink", "coral"), avoid=(110, 560, 970, 1280)))
    o.append(petals(d, random.Random(15), 20, 0, 560, 110, 1280, 8, 14, ("red", "pink")))
    return d.svg("".join(o)), spec("E-wedding-7", (150, 600, 930, 1230), "#A3123A", "#3A2226", "#9E2A1A", "light", "script", photo=ph, bg="#FCF5F0")


# ------------------------------------------------------------------ 8 mint: arch photo in varmalas (bottom)
def card8():
    d = Doc(38)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.lg([(0, "#E4F4EE"), (0.6, "#BFE3D6"), (1, "#8CC7B4")])]
    o.append('<rect width="1080" height="1350" fill="%s"/>' % damask_pattern(d, "#FFFFFF", None, 120, 0.35))
    o.append(glass(d, 84, 50, 912, 610, 40, "#FFFFFB", 0.9, "#6FB09A"))
    ph = {"shape": "arch", "x": 380, "y": 740, "w": 320, "h": 470}
    o.append('<path d="%s" fill="#0F5A48" opacity=".25" filter="%s"/>' % (shape_d("arch", 356, 730, 368, 500), d.blur(12)))
    o.append(photo_slot(d, ph, "#FFFAF6", "#F2E2DA", "#D9B8AA", ring_w=12, ring=d.lg(GOLD_SOFT, 0, 0, 1, 1), inner="#7A4A0E"))
    # rose garland along the arch
    ap = arch_pts(ph["x"] - 30, ph["y"] - 30, ph["w"] + 60, ph["h"] + 30, 200)
    o.append(flower_ring(d, path_pts(ap[1:-1], 21), 12, "rose", ("red", "pink", "white"), 3, cx=540, cy=980))
    # two big varmalas hanging either side
    o.append(varmala(d, 250, 720, 460, 120, 1, ("red", "wine")))
    o.append(varmala(d, 830, 720, 460, 120, 1, ("pink", "red")))
    for x_ in (250, 830):
        o.append(bloom(d, x_, 716, 22, "white") + rose(d, x_ - 22, 724, 14, "red") + rose(d, x_ + 22, 724, 14, "red"))
    o.append(petals(d, random.Random(16), 36, 0, 700, 1080, 1260, 8, 13, ("red", "pink"), avoid=(150, 680, 930, 1260)))
    o.append('<rect x="0" y="1262" width="1080" height="88" fill="%s"/><rect x="0" y="1258" width="1080" height="6" fill="%s"/>' % (d.lg([(0, "#3E8A74"), (1, "#256454")]), d.gold()))
    return d.svg("".join(o)), spec("E-wedding-8", (150, 96, 930, 614), "#9E1B3A", "#1E3A32", "#1E6A56", "light", "script", photo=ph, bg="#F8FCF8")


# ------------------------------------------------------------------ 9 couple walking away on petal path
def card9():
    d = Doc(39)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.lg([(0, "#FFF9EE"), (0.55, "#F8E6C4"), (1, "#E9C68E")])]
    o.append(rays(540, 780, 48, 1100, "#FFFFFF", 0.18, 3))
    o.append('<ellipse cx="540" cy="800" rx="420" ry="200" fill="%s"/>' % d.rg([(0, "#FFFFFF", .9), (1, "#FFFFFF", 0)]))
    # path
    o.append('<path d="M200,1350 L880,1350 L600,800 L480,800Z" fill="%s"/>' % d.lg([(0, "#F6D7C8"), (1, "#E7A99A")]))
    rr = random.Random(21)
    pts_ = []
    for i in range(260):
        t = rr.random() ** 0.7
        y_ = 800 + t * 470
        half = 60 + t * 340
        x_ = 540 + rr.uniform(-half, half)
        pts_.append((x_, y_, 6 + t * 10))
    pts_.sort(key=lambda p: p[1])
    for x_, y_, r_ in pts_:
        if 330 < x_ < 750 and y_ > 1272:
            continue
        o.append(d.use(petal_sym(d, rr.choice(["red", "pink", "coral"])), x_, y_, (r_ / 12, r_ / 20), rr.uniform(0, 360)))
    # flower pots/bushes lining the path
    for k in range(5):
        t = k / 4
        y_ = 820 + t * 400
        half = 90 + t * 300
        sc = 0.35 + t * 0.55
        for sg in (-1, 1):
            o.append(bush(d, 540 + sg * (half + 50 * sc), y_, sc, sg > 0, ("#7A9A5A", "#3E6A32"), ("pink", "red", "white"), k * 3 + (sg > 0)))
    o.append(couple_back(d, 530, 1170, 1.0, cloth=("#B3122E",)))
    o.append(petals(d, random.Random(22), 30, 0, 700, 1080, 1100, 8, 13, ("red", "pink"), avoid=(200, 700, 880, 1100)))
    return d.svg("".join(o)), spec("E-wedding-9", (150, 100, 930, 600), "#7A2E14", "#3A2A1E", "#8E3A1A", "light", "script", bg="#FDF3E2")


# ------------------------------------------------------------------ 10 teal: oval photo in rose hoop (dark)
def card10():
    d = Doc(40)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.rg([(0, "#16707A"), (0.6, "#0C4650"), (1, "#062A31")], 0.5, 0.3, 0.9)]
    o.append('<rect width="1080" height="1350" fill="%s"/>' % buti_pattern(d, "#F2C45A", None, 60, 0.10))
    ph = {"shape": "oval", "x": 368, "y": 66, "w": 344, "h": 436}
    o.append('<ellipse cx="540" cy="300" rx="330" ry="330" fill="%s"/>' % d.rg([(0, "#9FE3DA", .35), (1, "#9FE3DA", 0)]))
    o.append(rays(540, 290, 40, 700, "#BFF3EA", 0.05, 4))
    o.append('<ellipse cx="540" cy="284" rx="204" ry="250" fill="none" stroke="%s" stroke-width="6"/>' % d.gold())
    ring = ellipse_pts(540, 284, 204, 250, 60)
    o.append(flower_ring(d, ring, 15, "rose", ("blush", "pink", "white", "blush", "red"), 2, cx=540, cy=284, leafcol=("#7FB08A", "#2F5E3A")))
    o.append(photo_slot(d, ph, "#FDF6F2", "#F0DDD8", "#D9B8B0", ring_w=10, inner="#6E4A12"))
    # stage + couple flanking the portrait
    o.append('<ellipse cx="540" cy="652" rx="520" ry="26" fill="%s"/>' % d.rg([(0, "#F2C45A", .45), (1, "#F2C45A", 0)]))
    o.append('<path d="M60,650 Q540,628 1020,650" stroke="%s" stroke-width="5" fill="none"/>' % d.gold())
    o.append(groom(d, 196, 648, 1.06, pose="stand", rim="#FFE3A8"))
    o.append(bride(d, 884, 648, 1.06, flip=True, pose="stand", rim="#FFE3A8"))
    o.append(petals(d, random.Random(23), 50, 0, 0, 1080, 660, 8, 14, ("blush", "pink", "red"), avoid=(320, 20, 760, 560)))
    # lace bottom border
    o.append('<path d="%s" fill="%s"/>' % ("M0,1350 L0,1290 " + " ".join("Q%s,%s %s,1290" % (n(i * 60 + 30), 1262, n(i * 60 + 60)) for i in range(18)) + " L1080,1350Z", d.gold()))
    o.append('<path d="%s" fill="#062A31"/>' % ("M0,1350 L0,1300 " + " ".join("Q%s,%s %s,1300" % (n(i * 60 + 30), 1276, n(i * 60 + 60)) for i in range(18)) + " L1080,1350Z"))
    o.append(corners(d, 30, 30, 1050, 1250, 0.7, sw=2.5))
    return d.svg("".join(o)), spec("E-wedding-10", (150, 700, 930, 1200), "gold", "#F4FBF8", "#F2C45A", "dark", "script", photo=ph)


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
