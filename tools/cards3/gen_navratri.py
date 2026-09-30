"""Navratri wish-card art (agent A). python3 tools/cards3/gen_navratri.py [n ...]"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_a import *
from navratri_motifs_a import *
from navratri_dancers_a import dancer_f, dancer_m

CAT = "navratri"

PAL = {
    "pink": {"skirt": ["#D81B60", "#FFB300", "#1E88E5", "#43A047", "#8E24AA", "#F4511E"], "choli": "#1B5E20", "dup": "#E53935", "border": "#FFC53D"},
    "blue": {"skirt": ["#1565C0", "#E91E63", "#FFC107", "#00897B", "#7B1FA2", "#EF6C00"], "choli": "#C2185B", "dup": "#FF9800", "border": "#FFD54F"},
    "red": {"skirt": ["#C62828", "#FDD835", "#2E7D32", "#EC407A", "#1E88E5", "#FF7043"], "choli": "#4A148C", "dup": "#00897B", "border": "#FFC53D"},
}
MPAL = {
    "a": {"kediyu": "#FFF4E0", "trim": "#D81B60", "pagdi": ["#E53935", "#FFB300", "#43A047"], "pant": "#F3E5C8"},
    "b": {"kediyu": "#FFE082", "trim": "#1565C0", "pagdi": ["#8E24AA", "#FFEB3B", "#E91E63"], "pant": "#FFF8E1"},
}


def stars(c, box, n, col="#FFF3D6", rmax=1.8):
    x0, y0, x1, y1 = box
    return '<g fill="%s">%s</g>' % (col, "".join('<circle cx="%s" cy="%s" r="%s" opacity="%s"/>' % (
        f(c.rnd.uniform(x0, x1)), f(c.rnd.uniform(y0, y1)), f(c.rnd.uniform(0.5, rmax)), f(c.rnd.uniform(0.3, 0.9))) for _ in range(n)))


def mirror_frame(c, x, y, w, h, t=44, bg="#1A1033", threads=("#E53935", "#FFC53D", "#1E9E6A", "#EC407A")):
    """Four embroidered mirror-work bands forming a frame around a box, with mirror roundels at the corners."""
    out = [mirror_band(c, x, y, w, t, bg, threads), mirror_band(c, x, y + h - t, w, t, bg, threads),
           mirror_band(c, x, y + t, t, h - 2 * t, bg, threads, vertical=True), mirror_band(c, x + w - t, y + t, t, h - 2 * t, bg, threads, vertical=True)]
    for cx, cy in ((x + t / 2, y + t / 2), (x + w - t / 2, y + t / 2), (x + t / 2, y + h - t / 2), (x + w - t / 2, y + h - t / 2)):
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(t * 0.62), bg))
        out.append(mirror(c, cx, cy, t * 0.26, threads[0], threads[1]))
    return "".join(out)


def swirl(cx, cy, rx, ry, color, op=0.5, w=3, a0=200, a1=340):
    p = []
    for i in range(31):
        a = math.radians(a0 + (a1 - a0) * i / 30)
        p.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    return '<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" opacity="%s"/>' % (pts(p), color, f(w), f(op))


def spark_burst(c, cx, cy, r, col="#FFF3C4"):
    out = ['<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(r * 1.3), c.rg([(0, col, 0.9), (0.4, "#FFD54F", 0.35), (1, "#FFD54F", 0)]))]
    for k in range(16):
        a = math.radians(k * 22.5 + 5)
        L = r * (1.1 if k % 2 else 0.7)
        out.append('<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
            f(cx + r * 0.35 * math.cos(a)), f(cy + r * 0.35 * math.sin(a)), f(cx + L * math.cos(a)), f(cy + L * math.sin(a)), col, f(r * 0.05)))
    out.append(sparkle(cx, cy, r * 0.5, "#FFFFFF"))
    return "".join(out)


def cloth_banner(c, x, y, w, h, cloth=("#2A0B4A", "#1A0630"), border="#C2185B", dot="#FFE9B0", points=9):
    """Hanging embroidered cloth banner: gold rod with finials, bandhani border, pointed (toran) hem with tassels."""
    out = []
    pt = 46  # point depth
    # outline with pointed hem
    d = "M%s,%s H%s V%s " % (f(x), f(y), f(x + w), f(y + h))
    step = w / points
    for i in range(points):
        xa = x + w - i * step
        d += "L%s,%s L%s,%s " % (f(xa - step / 2), f(y + h + pt), f(xa - step), f(y + h))
    d += "Z"
    out.append('<path d="%s" fill="%s" filter="%s"/>' % (d, c.lg([cloth[0], cloth[1]]), c.shadow(16, 20, 0.5)))
    cp = c.clip('<path d="%s"/>' % d)
    bt = 34
    band = bandhani(c, border, dot, 20, 0.95)
    out.append('<g clip-path="%s">' % cp)
    out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (f(x), f(y), f(w), f(h + pt), band))
    inner = "M%s,%s H%s V%s H%s Z" % (f(x + bt), f(y + bt), f(x + w - bt), f(y + h - bt), f(x + bt))
    out.append('<path d="%s" fill="%s"/>' % (inner, c.lg([cloth[0], cloth[1]])))
    out.append('<path d="%s" fill="%s"/>' % (inner, c.rg([(0, "#fff", 0.07), (1, "#fff", 0)], 0.5, 0.2, 0.7)))
    out.append('</g>')
    out.append('<path d="%s" fill="none" stroke="#FFC53D" stroke-width="3" stroke-dasharray="1 7" stroke-linecap="round"/>' % inner)
    out.append('<path d="%s" fill="none" stroke="#FFC53D" stroke-width="2"/>' % rr(x + bt + 12, y + bt + 12, w - 2 * bt - 24, h - 2 * bt - 24, 6))
    for i in range(points):
        xa = x + w - i * step - step / 2
        out.append(mirror(c, xa, y + h + pt - 26, 9, "#FFC53D", "#FFE9B0"))
        out.append('<path d="M%s,%s v18" stroke="#FFC53D" stroke-width="2.5"/>' % (f(xa), f(y + h + pt)))
        out.append('<path d="M%s,%s l-8,26 h16 z" fill="%s"/>' % (f(xa), f(y + h + pt + 14), ["#E53935", "#FFC53D", "#1E9E6A", "#EC407A"][i % 4]))
        out.append('<circle cx="%s" cy="%s" r="5" fill="#FFC53D"/>' % (f(xa), f(y + h + pt + 14)))
    # rod
    g = c.lg(["#FFF1B8", "#E0A526", "#8A5A12"], 0, 0, 0, 1)
    out.append('<rect x="%s" y="%s" width="%s" height="18" rx="9" fill="%s" filter="%s"/>' % (f(x - 50), f(y - 12), f(w + 100), g, c.shadow(4, 5, 0.4)))
    for ex in (x - 50, x + w + 50):
        out.append('<circle cx="%s" cy="%s" r="16" fill="%s"/><circle cx="%s" cy="%s" r="6" fill="#B71C1C"/>' % (f(ex), f(y - 3), g, f(ex), f(y - 3)))
    for k in range(6):
        rx = x + 30 + k * (w - 60) / 5
        out.append('<rect x="%s" y="%s" width="14" height="30" rx="6" fill="%s"/>' % (f(rx - 7), f(y - 16), g))
    return "".join(out)


# ---------------------------------------------------------------- 1 night garba circle
def card1():
    c = Card(11)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#0D0A2E"), (0.45, "#2A0F4F"), (0.75, "#5B1467"), (1, "#20082E")]))
    c.add(stars(c, (30, 60, 1050, 800), 140))
    c.add('<circle cx="880" cy="760" r="240" fill="%s"/>' % c.rg([(0, "#FFF3D6", 0.25), (1, "#FFF3D6", 0)]))
    c.add(bokeh(c, 30, (0, 650, 1080, 1100), ["#FFC53D", "#EC407A", "#7C4DFF", "#FF7043"], 4, 20, (0.15, 0.5)))
    # stage glow + floor
    c.add('<ellipse cx="540" cy="1150" rx="620" ry="190" fill="%s"/>' % c.rg([(0, "#FFB300", 0.45), (0.5, "#FF6F00", 0.12), (1, "#FF6F00", 0)]))
    c.add('<rect x="0" y="1150" width="1080" height="200" fill="%s"/>' % c.lg([(0, "#3A0E3F"), (1, "#14051C")]))
    sil = "#2B0B3F"
    for x, sc, fl, m in ((170, 0.62, False, 0), (400, 0.58, True, 1), (680, 0.58, False, 1), (920, 0.62, True, 0)):
        c.add((dancer_m(c, x, 1150, sc, fl, sil=sil) if m else dancer_f(c, x, 1150, sc, fl, "c", sil=sil)))
    c.add(garbo(c, 540, 1070, 110))
    c.add(dancer_f(c, 250, 1268, 1.02, False, "a", PAL["pink"]))
    c.add(dancer_m(c, 830, 1268, 0.98, True, MPAL["a"], pose="cross"))
    c.add('<rect x="0" y="1262" width="1080" height="88" fill="%s"/>' % c.lg([(0, "#14051C", 0), (0.4, "#14051C", 1)], 0, 0, 0, 1))
    c.add(mirror_band(c, 0, 0, 1080, 58, "#14051C"))
    c.add(tassel_fringe(c, 20, 1060, 58, 22, ["#E53935", "#FFC53D", "#1E9E6A", "#EC407A"], 34))
    c.add(cloth_banner(c, 90, 118, 900, 570))
    s = spec("E-navratri-1", (148, 184, 932, 644), "gold", "#FFF4E6", "#FFC53D", "dark", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 2 Maa Amba chunri + trishul + garbos
def card2():
    """Maa Amba's chunri flowing diagonally across the card: trishul top-right, garbos bottom-left."""
    c = Card(22)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % bandhani(c, "#8E0E1A", "#FFE9B0", 38, 0.55))
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.rg([(0, "#FF8A00", 0.4), (0.6, "#7A0010", 0.1), (1, "#2A0006", 0.6)], 0.75, 0.15, 0.9))
    c.add(rays(880, 250, 40, 900, "#FFE9A8", 0.08, 0.45))
    c.add('<circle cx="880" cy="230" r="260" fill="%s"/>' % c.rg([(0, "#FFE082", 0.6), (1, "#FFB300", 0)]))
    # the chunri: a wide flowing cloth from top-left to bottom-right
    top = "M-140,40 C220,90 380,420 560,640 C740,860 880,1060 1220,1130"
    bot = "L1220,1400 C880,1330 700,1100 520,880 C340,660 180,330 -140,300 Z"
    cl = top + " " + bot
    c.add('<path d="%s" fill="#000" opacity="0.35" filter="%s" transform="translate(10,22)"/>' % (cl, c.blur(14)))
    c.add('<path d="%s" fill="%s"/>' % (cl, c.lg([(0, "#E53935"), (0.5, "#C62828"), (1, "#8E0E1A")], 0, 0, 1, 1)))
    dots = c.pattern(22, 22, '<circle cx="5" cy="5" r="2.1" fill="#FFF3C4"/><circle cx="16" cy="16" r="2.1" fill="#FFF3C4"/><circle cx="16" cy="5" r="1.1" fill="#FFF3C4"/><circle cx="5" cy="16" r="1.1" fill="#FFD54F"/>')
    c.add('<path d="%s" fill="%s" opacity="0.85"/>' % (cl, dots))
    # soft folds
    for k, op in ((0.3, 0.22), (0.62, 0.18)):
        c.add('<path d="M-140,%s C220,%s 360,%s 540,%s C720,%s 880,%s 1220,%s" stroke="#4A0008" stroke-opacity="%s" stroke-width="34" fill="none" filter="%s"/>' % (
            f(40 + 260 * k), f(90 + 240 * k), f(420 + 240 * k), f(640 + 240 * k), f(860 + 240 * k), f(1060 + 270 * k), f(1130 + 270 * k), f(op), c.blur(10)))
    for edge in ("M-140,40 C220,90 380,420 560,640 C740,860 880,1060 1220,1130", "M-140,300 C180,330 340,660 520,880 C700,1100 880,1330 1220,1400"):
        c.add('<path d="%s" stroke="#FFC53D" stroke-width="16" fill="none"/>' % edge)
        c.add('<path d="%s" stroke="#8B1A1A" stroke-width="2.5" stroke-dasharray="7 7" fill="none"/>' % edge)
    # trishul with its own chunri knot
    c.add(trishul(c, 880, 600, 520, "#D50000"))
    # garbos bottom-left
    c.add(garbo(c, 190, 1130, 108))
    c.add(garbo(c, 380, 1196, 62, ("#E91E63", "#6A0F33"), spill=False))
    # panel framed with a bandhani border
    x, y, w, h = 96, 470, 888, 580
    c.add('<rect x="%d" y="%d" width="%d" height="%d" rx="18" fill="%s" filter="%s"/>' % (x, y, w, h, bandhani(c, "#B71C1C", "#FFE9B0", 18, 0.95), c.shadow(16, 24, 0.5)))
    c.add('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s"/>' % (x + 24, y + 24, w - 48, h - 48, c.lg(["#FFF9EC", "#F6E6C4"])))
    c.add('<rect x="%d" y="%d" width="%d" height="%d" rx="18" fill="none" stroke="#FFC53D" stroke-width="4"/>' % (x, y, w, h))
    c.add('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="none" stroke="#FFC53D" stroke-width="3"/>' % (x + 24, y + 24, w - 48, h - 48))
    c.add('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="none" stroke="#C9A25A" stroke-width="1.5"/>' % (x + 38, y + 38, w - 76, h - 76))
    for (mx, my) in ((x + 12, y + 12), (x + w - 12, y + 12), (x + 12, y + h - 12), (x + w - 12, y + h - 12)):
        c.add(mirror(c, mx, my, 15, "#1E9E6A", "#FFC53D"))
    c.add(watermark_calm(c, "#2A0006", 0.7))
    s = spec("E-navratri-2", (150, 524, 930, 996), "#9C0D1C", "#3A1A14", "#B7791F", "light", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 3 big couple + garbo, mirror-work frame panel
def card3():
    c = Card(33)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#0B5D4B"), (0.55, "#0E7A5F"), (1, "#064034")]))
    c.add('<rect width="1080" height="1350" fill="%s" opacity="0.12"/>' % leheriya(c, ["#FFFFFF", "#0E7A5F", "#FFD54F", "#0E7A5F"], 40, -35))
    c.add('<circle cx="540" cy="1020" r="420" fill="%s"/>' % c.rg([(0, "#FFE082", 0.55), (0.5, "#FFB300", 0.15), (1, "#FFB300", 0)]))
    c.add(swirl(540, 1180, 470, 90, "#FFE082", 0.5, 4, 180, 360))
    c.add(swirl(540, 1200, 520, 110, "#FFFFFF", 0.3, 2, 180, 360))
    c.add(garbo(c, 540, 1090, 100))
    c.add(dancer_f(c, 270, 1262, 1.2, False, "c", PAL["blue"]))
    c.add(dancer_m(c, 820, 1262, 1.08, True, MPAL["b"], pose="cross"))
    c.add(spark_burst(c, 540, 770, 60))
    c.add('<rect x="0" y="1270" width="1080" height="80" fill="%s"/>' % c.lg([(0, "#064034", 0), (0.5, "#064034", 1)]))
    # panel with mirror-work frame
    x, y, w, h = 70, 50, 940, 640
    c.add('<rect x="%d" y="%d" width="%d" height="%d" fill="#FFF8EC" filter="%s"/>' % (x, y, w, h, c.shadow(12, 18, 0.4)))
    c.add(mirror_frame(c, x, y, w, h, 46, "#5A0B3C", ("#FFC53D", "#FFE9B0", "#26C6DA", "#EC407A")))
    c.add('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#C2185B" stroke-width="2"/>' % (x + 58, y + 58, w - 116, h - 116))
    s = spec("E-navratri-3", (150, 128, 930, 612), "#A0105A", "#2B1A2E", "#0E7A5F", "light", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 4 giant garbo on maroon bandhani
def card4():
    c = Card(44)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % bandhani(c, "#4A0A2A", "#F8BBD0", 30, 0.55, "#FFD54F"))
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.rg([(0, "#000", 0), (0.7, "#000", 0.25), (1, "#000", 0.6)], 0.5, 0.75, 0.8))
    c.add(rays(540, 1010, 48, 900, "#FFD54F", 0.08, 0.45))
    # floor
    c.add('<ellipse cx="540" cy="1250" rx="620" ry="120" fill="%s"/>' % c.rg([(0, "#FF8A00", 0.5), (1, "#FF8A00", 0)]))
    for (x1, y1, x2, y2, col) in ((250, 1230, 470, 740, ("#E91E63", "#FFD740")), (830, 1230, 610, 740, ("#1E88E5", "#FFD740")),
                                  (150, 1150, 420, 820, ("#43A047", "#FFEB3B")), (930, 1150, 660, 820, ("#8E24AA", "#FFC107"))):
        c.add(dandiya(c, x1, y1, x2, y2, 20, col))
    c.add(garbo(c, 540, 1060, 175))
    for k in range(11):
        a = math.radians(200 + k * 14)
        c.add(mirror(c, 540 + 430 * math.cos(a), 1060 + 300 * math.sin(a), 11, ["#E91E63", "#26A69A", "#FFB300"][k % 3], "#FFD54F"))
    # panel: cut-corner with mirror studs on its edge
    x, y, w, h = 90, 90, 900, 560
    d = cut_corner(x, y, w, h, 60)
    c.add(panel(c, x, y, w, h, path=d, fill=("#FFF7EE", "#F9E4D0"), stroke="#D4A64A", sw=5))
    c.add('<path d="%s" fill="none" stroke="#8E0E4E" stroke-width="2"/>' % cut_corner(x + 18, y + 18, w - 36, h - 36, 48))
    for k in range(10):
        px = x + 90 + k * (w - 180) / 9
        c.add(mirror(c, px, y, 11, "#C2185B", "#FFC53D"))
        c.add(mirror(c, px, y + h, 11, "#C2185B", "#FFC53D"))
    for (cx, cy) in ((x + 30, y + 30), (x + w - 30, y + 30), (x + 30, y + h - 30), (x + w - 30, y + h - 30)):
        c.add(mirror(c, cx, cy, 14, "#1E9E6A", "#FFC53D"))
    c.add(watermark_calm(c, "#2A0616", 0.8))
    s = spec("E-navratri-4", (150, 140, 930, 600), "#8E0E4E", "#3A1A2E", "#B7791F", "light", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 5 leheriya + diagonal corners: dandiya burst & garbo
def card5():
    c = Card(55)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % leheriya(c, ["#FF7043", "#FFB300", "#EC407A", "#FFD54F", "#F4511E", "#FF8A65"], 60, -32))
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.rg([(0, "#FFF3E0", 0.35), (1, "#8E1B3A", 0.45)], 0.5, 0.5, 0.75))
    # top-left dandiya burst
    c.add(spark_burst(c, 300, 270, 150))
    for (x1, y1, x2, y2, col) in ((40, 560, 520, 40, ("#C2185B", "#FFD740")), (20, 80, 560, 500, ("#1565C0", "#FFD740")),
                                  (120, 620, 420, 20, ("#2E7D32", "#FFEB3B")), (10, 330, 600, 230, ("#6A1B9A", "#FFC107"))):
        c.add(dandiya(c, x1, y1, x2, y2, 22, col))
    c.add(spark_burst(c, 300, 270, 70, "#FFFFFF"))
    # bottom-right garbo with dancer silhouettes
    c.add(garbo(c, 850, 1120, 130))
    c.add(dancer_f(c, 640, 1290, 0.62, False, "c", sil="#7A1A3A"))
    c.add(dancer_m(c, 1030, 1290, 0.6, True, sil="#7A1A3A"))
    x, y, w, h = 70, 420, 940, 560
    c.add(panel(c, x, y, w, h, 150, ("#FFFFFF", "#FFF4E8"), "#E91E63", inner=False, sw=6))
    c.add('<path d="%s" fill="none" stroke="#FFB300" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/>' % rr(x + 16, y + 16, w - 32, h - 32, 134))
    s = spec("E-navratri-5", (150, 470, 930, 930), "#B0124E", "#3A1A2E", "#D84315", "light", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 6 single twirling dancer, saffron
def card6():
    """Garba stage: chunri curtains frame a twirling dancer who stands on the mirror-work stage (text panel)."""
    c = Card(66)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % bandhani(c, "#F57C00", "#FFF3C4", 34, 0.6, "#B71C1C"))
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.rg([(0, "#FFF3C4", 0.75), (0.45, "#FFB300", 0.1), (1, "#8A2A00", 0.55)], 0.5, 0.33, 0.75))
    c.add(rays(540, 60, 30, 900, "#FFFFFF", 0.1, 0.4, 70))
    # spotlight
    c.add('<path d="M430,0 L650,0 L860,720 L220,720 Z" fill="%s" filter="%s"/>' % (c.lg([(0, "#FFFFFF", 0.35), (1, "#FFFFFF", 0.05)]), c.blur(14)))
    for k in range(5):
        c.add(swirl(540, 640 + k * 8, 300 + k * 36, 56 + k * 10, "#FFFFFF" if k % 2 else "#B71C1C", 0.5, 3, 150, 390))
    for i in range(16):
        a = c.rnd.uniform(0, 2 * math.pi)
        r = c.rnd.uniform(270, 380)
        c.add(mirror(c, 540 + r * math.cos(a), 420 + r * 0.6 * math.sin(a), c.rnd.uniform(6, 10), "#B71C1C", "#FFF3C4"))
    # curtains (Amba's chunri) at both sides, tied back
    for side in (-1, 1):
        def X(v):
            return v if side < 0 else 1080 - v
        d = "M%s,0 L%s,0 C%s,220 %s,420 %s,560 C%s,640 %s,760 %s,900 L%s,900 Z" % (
            f(X(-10)), f(X(230)), f(X(200)), f(X(150)), f(X(118)), f(X(150)), f(X(190)), f(X(210)), f(X(-10)))
        c.add('<path d="%s" fill="%s" filter="%s"/>' % (d, c.lg([(0, "#8E0E1A"), (0.5, "#D32F2F"), (1, "#8E0E1A")], 0, 0, 1, 0), c.shadow(6, 16, 0.45)))
        c.add('<path d="%s" fill="%s" opacity="0.7"/>' % (d, c.pattern(22, 22, '<circle cx="5" cy="5" r="2" fill="#FFF3C4"/><circle cx="16" cy="16" r="2" fill="#FFF3C4"/>')))
        for k in range(3):
            c.add('<path d="M%s,0 C%s,240 %s,440 %s,560" stroke="#4A0008" stroke-opacity="0.3" stroke-width="10" fill="none"/>' % (f(X(50 + k * 55)), f(X(45 + k * 48)), f(X(40 + k * 30)), f(X(110 + k * 3))))
        c.add('<path d="M%s,0 C%s,220 %s,420 %s,560 C%s,640 %s,760 %s,900" stroke="#FFC53D" stroke-width="12" fill="none"/>' % (f(X(230)), f(X(200)), f(X(150)), f(X(118)), f(X(150)), f(X(190)), f(X(210))))
        # tie-back rope with tassel
        c.add('<path d="M%s,560 Q%s,590 %s,560" stroke="#FFC53D" stroke-width="8" fill="none"/>' % (f(X(-10)), f(X(60)), f(X(126))))
        c.add('<path d="M%s,570 v40" stroke="#FFC53D" stroke-width="4"/><path d="M%s,600 l-12,44 h24 z" fill="#FFC53D"/><circle cx="%s" cy="600" r="9" fill="#B71C1C"/>' % (f(X(120)), f(X(120)), f(X(120))))
    c.add(chunri_swag(c, -20, 1100, 60, 5, 90))
    # the dancer, centre stage, with dandiyas
    c.add('<ellipse cx="540" cy="700" rx="260" ry="34" fill="#5A1A00" opacity="0.35" filter="%s"/>' % c.blur(8))
    c.add(dancer_f(c, 540, 700, 1.13, False, "a", PAL["red"]))
    # stage front = text panel
    x, y, w, h = 90, 690, 900, 580
    c.add('<path d="%s" fill="%s" filter="%s"/>' % (rr(x, y, w, h, 20), c.lg(["#4A0A2A", "#2A0418"]), c.shadow(14, 22, 0.45)))
    c.add(mirror_band(c, x, y, w, 44, "#2A0418", ("#FFC53D", "#FFE9B0", "#26A69A", "#EC407A")))
    c.add('<path d="%s" fill="none" stroke="#FFC53D" stroke-width="2"/>' % rr(x + 18, y + 60, w - 36, h - 78, 12))
    s = spec("E-navratri-6", (140, 770, 940, 1236), "gold", "#FFF4E6", "#FFC53D", "dark", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 7 golden silhouette frieze on magenta dusk
def card7():
    c = Card(77)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#FCE4EC"), (0.4, "#F48FB1"), (0.7, "#C2185B"), (1, "#4A0D2E")]))
    c.add('<circle cx="540" cy="960" r="360" fill="%s"/>' % c.rg([(0, "#FFF3C4", 0.8), (0.5, "#FFD54F", 0.25), (1, "#FFD54F", 0)]))
    c.add(rays(540, 960, 40, 900, "#FFFFFF", 0.08, 0.45))
    g = c.lg(["#FFF1B8", "#E0A526", "#8A5A12"], 0, 0, 0, 1)
    c.add('<ellipse cx="540" cy="1250" rx="560" ry="50" fill="#4A0D2E" opacity="0.6"/>')
    c.add(garbo(c, 540, 1110, 95, body=("#E0A526", "#7A4E08"), paint="#FFF1B8"))
    for x, sc, fl, m, pose in ((110, 0.78, False, 0, "c"), (300, 0.84, True, 1, ""), (780, 0.84, False, 1, ""), (970, 0.78, True, 0, "a")):
        c.add(dancer_m(c, x, 1250, sc, fl, sil=g) if m else dancer_f(c, x, 1250, sc, fl, pose, sil=g))
    c.add('<rect x="0" y="1250" width="1080" height="100" fill="#4A0D2E"/>')
    for k in range(40):
        c.add(sparkle(c.rnd.uniform(40, 1040), c.rnd.uniform(700, 1150), c.rnd.uniform(3, 9), "#FFF3C4", c.rnd.uniform(0.4, 1)))
    # cowrie fringe on top
    c.add('<rect x="0" y="0" width="1080" height="40" fill="%s"/>' % c.lg(["#8A5A12", "#E0A526", "#8A5A12"], 0, 0, 1, 0))
    c.add(tassel_fringe(c, 0, 1080, 40, 30, ["#C2185B", "#FFC53D", "#FFFFFF"], 30))
    x, y, w, h = 104, 132, 872, 552
    c.add(panel(c, x, y, w, h, 24, ("#FFFBF4", "#FBEEE2"), "#C9A25A", sw=3))
    s = spec("E-navratri-7", (150, 178, 930, 638), "#A0105A", "#3A1A2E", "#B7791F", "light", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 8 kutchi embroidered textile
def card8():
    """Kutchi textile: four embroidered medallions (garbo, dandiya, dancers) at the corners of a central plaque."""
    c = Card(88)
    c.add('<rect width="1080" height="1350" fill="#140C0C"/>')
    th = ("#E53935", "#FFC53D", "#43A047", "#EC407A")
    lat = c.pattern(90, 90, '<path d="M45,4 L86,45 L45,86 L4,45 Z" fill="none" stroke="#C62828" stroke-width="2"/>'
                           '<path d="M45,18 L72,45 L45,72 L18,45 Z" fill="none" stroke="#FFC53D" stroke-width="1.5" stroke-dasharray="4 3"/>'
                           '<circle cx="45" cy="45" r="6" fill="#DDE6F2"/><circle cx="45" cy="45" r="8" fill="none" stroke="#43A047" stroke-width="2"/>'
                           '<circle cx="0" cy="0" r="4" fill="#EC407A"/><circle cx="90" cy="0" r="4" fill="#EC407A"/><circle cx="0" cy="90" r="4" fill="#EC407A"/><circle cx="90" cy="90" r="4" fill="#EC407A"/>')
    c.add('<rect width="1080" height="1350" fill="%s" opacity="0.5"/>' % lat)
    c.add(mirror_frame(c, 0, 0, 1080, 1350, 54, "#140C0C", th))

    def medallion(cx, cy, R, inner):
        out = ['<circle cx="%s" cy="%s" r="%s" fill="#1E1212" filter="%s"/>' % (f(cx), f(cy), f(R + 18), c.shadow(8, 12, 0.6))]
        for k in range(20):
            a = math.radians(k * 18)
            px, py = cx + (R + 4) * math.cos(a), cy + (R + 4) * math.sin(a)
            out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" transform="rotate(%s %s %s)"/>' % (f(px), f(py), f(R * 0.14), f(R * 0.06), th[k % 4], f(k * 18 + 90), f(px), f(py)))
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(R - 8), c.rg([(0, "#FFB74D", 0.55), (1, "#3A1010", 1)])))
        cp = c.clip('<circle cx="%s" cy="%s" r="%s"/>' % (f(cx), f(cy), f(R - 8)))
        out.append('<g clip-path="%s">%s</g>' % (cp, inner))
        out.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#FFC53D" stroke-width="4" stroke-dasharray="10 6"/>' % (f(cx), f(cy), f(R - 8)))
        for k in range(8):
            a = math.radians(k * 45 + 22.5)
            out.append(mirror(c, cx + (R + 4) * math.cos(a), cy + (R + 4) * math.sin(a), R * 0.07, th[k % 4], "#FFC53D"))
        return "".join(out)

    R = 150
    c.add(medallion(215, 225, R, garbo(c, 215, 250, 72)))
    c.add(medallion(865, 225, R, dandiya(c, 780, 320, 950, 130, 16, ("#E53935", "#FFD740")) + dandiya(c, 950, 320, 780, 130, 16, ("#43A047", "#FFD740")) + spark_burst(c, 865, 225, 44)))
    c.add(medallion(215, 1105, R, dancer_f(c, 225, 1214, 0.5, False, "b", PAL["pink"])))
    c.add(medallion(865, 1105, R, dancer_m(c, 855, 1226, 0.5, True, MPAL["b"])))
    # trishul between the top medallions
    c.add('<circle cx="540" cy="190" r="120" fill="%s"/>' % c.rg([(0, "#FFB74D", 0.45), (1, "#FFB74D", 0)]))
    c.add(trishul(c, 540, 380, 300, "#D50000"))
    # central plaque
    x, y, w, h = 96, 390, 888, 570
    c.add(panel(c, x, y, w, h, 14, ("#FFF8EC", "#F4E4C8"), "#C62828", sw=4))
    for k in range(12):
        c.add(mirror(c, x + 60 + k * (w - 120) / 11, y + h, 9, th[k % 4], "#FFC53D"))
    s = spec("E-navratri-8", (150, 440, 930, 910), "#B71C1C", "#2A1A14", "#2E7D32", "light", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 9 nine garbos (nine nights) arc around trishul
def card9():
    c = Card(99)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#1A1446"), (0.55, "#2E1F6B"), (1, "#120C30")]))
    c.add(stars(c, (30, 30, 1050, 900), 140, "#FFE9B0"))
    c.add('<circle cx="540" cy="700" r="560" fill="%s"/>' % c.rg([(0, "#FFB300", 0.3), (1, "#FFB300", 0)]))
    c.add('<rect x="0" y="1180" width="1080" height="170" fill="%s"/>' % c.lg([(0, "#120C30", 0), (1, "#0A0620", 1)]))
    # nine garbos (nine nights) in an arc around the arch-shaped panel
    cols = [("#C8531E", "#7A2208"), ("#E91E63", "#6A0F33"), ("#1E88E5", "#0D3C73"), ("#43A047", "#1B5E20"), ("#FFB300", "#8A5A12")]
    cx, cy, R = 540, 760, 490
    for k in range(9):
        if k == 4:
            continue
        a = math.radians(180 + k * 22.5)
        c.add(garbo(c, cx + R * math.cos(a), cy + R * math.sin(a) * 1.02 + 20, 50, cols[k % 5], spill=False))
    c.add(chunri_swag(c, -20, 1100, 60, 4, 90))
    # arch panel
    x, y, w, h = 96, 316, 888, 914
    d = arch_path(x, y, w, h)
    c.add('<path d="%s" fill="#0E0A26" opacity="0.92" filter="%s"/>' % (d, c.shadow(16, 26, 0.5)))
    c.add('<path d="%s" fill="%s"/>' % (d, c.rg([(0, "#3B2A7A", 0.55), (1, "#3B2A7A", 0)], 0.5, 0.25, 0.6)))
    c.add('<path d="%s" fill="none" stroke="#FFC53D" stroke-width="4"/>' % d)
    c.add('<path d="%s" fill="none" stroke="#FFC53D" stroke-width="1.5" opacity="0.6"/>' % arch_path(x + 18, y + 18, w - 36, h - 36))
    c.add('<circle cx="540" cy="560" r="190" fill="%s"/>' % c.rg([(0, "#FFC247", 0.45), (1, "#FFC247", 0)]))
    c.add(trishul(c, 540, 735, 360, "#D50000"))
    # mirror studs along arch
    for k in range(13):
        a = math.radians(180 + k * 15)
        c.add(mirror(c, x + w / 2 + (w / 2) * math.cos(a), y + w / 2 + (w / 2) * math.sin(a), 9, "#E91E63", "#FFC53D"))
    s = spec("E-navratri-9", (146, 748, 934, 1210), "gold", "#FFF4E6", "#FFC53D", "dark", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 10 patchwork colour-blocks + dancing pair
def card10():
    c = Card(1010)
    c.add('<rect width="1080" height="1350" fill="#FFF3E6"/>')
    colors = ["#D81B60", "#FFB300", "#1E88E5", "#43A047", "#8E24AA", "#F4511E", "#00897B", "#FDD835"]
    S = 135
    for i in range(8):
        for j in range(4):
            colr = colors[(i * 3 + j * 5) % len(colors)]
            x, y = i * S, j * S - 30
            c.add('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, y, S, S, colr))
            k = (i + j) % 3
            if k == 0:
                c.add('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, y, S, S, bandhani(c, "none", "#FFF3C4", 22, 0.9)))
            elif k == 1:
                c.add(mirror(c, x + S / 2, y + S / 2, 16, "#FFFFFF", "#FFC53D"))
                c.add('<path d="M%d,%d L%d,%d L%d,%d L%d,%d Z" fill="none" stroke="#FFF3C4" stroke-width="3"/>' % (x + S / 2, y + 12, x + S - 12, y + S / 2, x + S / 2, y + S - 12, x + 12, y + S / 2))
            else:
                c.add('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" opacity="0.5"/>' % (x, y, S, S, leheriya(c, ["#FFFFFF", "none"], 20, -40)))
            c.add('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#FFF3C4" stroke-width="2" stroke-dasharray="6 4"/>' % (x + 4, y + 4, S - 8, S - 8))
    c.add('<rect x="0" y="0" width="1080" height="510" fill="%s"/>' % c.lg([(0, "#000", 0), (1, "#000", 0.35)]))
    c.add(mirror_band(c, 0, 490, 1080, 50, "#2A0F3F"))
    c.add(tassel_fringe(c, 10, 1070, 540, 20, ["#D81B60", "#FFB300", "#1E88E5", "#43A047"], 30))
    # couple dancing, bottom
    c.add('<rect x="0" y="560" width="1080" height="790" fill="%s"/>' % c.rg([(0, "#FFE0B2", 0.9), (1, "#FFF3E6", 0)], 0.5, 0.75, 0.6))
    c.add(rays(540, 1000, 36, 700, "#FFB300", 0.08, 0.45))
    c.add('<ellipse cx="540" cy="1240" rx="500" ry="52" fill="#E8C9A8"/>')
    c.add(swirl(540, 1225, 470, 70, "#D81B60", 0.55, 4, 180, 360))
    c.add(swirl(540, 1235, 510, 80, "#1E88E5", 0.35, 3, 180, 360))
    c.add(dancer_f(c, 360, 1250, 1.12, False, "c", PAL["pink"]))
    c.add(dancer_m(c, 740, 1250, 1.0, True, MPAL["a"], pose="cross"))
    c.add(spark_burst(c, 552, 862, 46))
    x, y, w, h = 96, 136, 888, 548
    # (panel sits over the patchwork top)
    c.add(panel(c, x, y, w, h, 20, ("#FFFFFF", "#FFF6EC"), "#2A0F3F", sw=5))
    s = spec("E-navratri-10", (142, 180, 938, 640), "#A0105A", "#2A1A2E", "#2A0F3F", "light", "deco")
    return c.svg(), s


CARDS = [card1, card2, card3, card4, card5, card6, card7, card8, card9, card10]

if __name__ == "__main__":
    from render import render_cards
    only = [int(a) for a in sys.argv[1:]]
    arts, specs = {}, []
    for i, fn in enumerate(CARDS, 1):
        svg, s = fn()
        specs.append(s)
        if not only or i in only:
            arts[s["id"]] = svg
    write_spec(CAT, specs)
    render_cards(arts)
