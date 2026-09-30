"""Dussehra wish-card art (agent A). python3 tools/cards3/gen_dussehra.py"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_a import *
from dussehra_motifs_a import *

CAT = "dussehra"


def stars(c, box, n, col="#FFF3D6", rmax=1.8):
    x0, y0, x1, y1 = box
    return '<g fill="%s">%s</g>' % (col, "".join('<circle cx="%s" cy="%s" r="%s" opacity="%s"/>' % (
        f(c.rnd.uniform(x0, x1)), f(c.rnd.uniform(y0, y1)), f(c.rnd.uniform(0.5, rmax)), f(c.rnd.uniform(0.3, 0.9))) for _ in range(n)))


def ground(c, y_left, y_right, color, bumps=6, amp=14):
    p = [(0, y_left)]
    for i in range(1, bumps):
        t = i / bumps
        p.append((W * t, y_left + (y_right - y_left) * t + c.rnd.uniform(-amp, amp)))
    p.append((W, y_right))
    d = "M0,%d L%s L%d,%d Z" % (H, pts(p), W, H)
    return '<path d="%s" fill="%s"/>' % (d, color)


# ---------------------------------------------------------------- 1 dusk dahan
def card1():
    c = Card(101)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#12061F"), (0.34, "#3B0F3F"), (0.6, "#8E1F2E"), (0.8, "#E2571C"), (1, "#F7A35C")]))
    c.add(stars(c, (40, 30, 1040, 520), 90))
    c.add(smoke(c, 640, 760, 360, 520, "#2A1224", 0.55))
    c.add(bokeh(c, 26, (60, 620, 1020, 1200), ["#FFB74D", "#FF7043", "#FFE082"], 3, 14, (0.2, 0.6)))
    c.add(ravan(c, 610, 1215, 0.58, burn=0.9))
    c.add(sparks(c, (300, 640, 960, 1150), 110))
    c.add(ground(c, 1215, 1235, "#1A0710", 8, 6))
    c.add(ram_archer(c, 120, 1236, 0.46, fill="#1A0710", rim="#FFB74D", rimw=3))
    c.add(flaming_arrow(c, 270, 1062, 596, 905, 0.9))
    c.add(crowd(c, 700, 1080, 1350, 95, "#12040A"))
    c.add(crowd(c, 0, 320, 1350, 80, "#12040A"))
    c.add('<rect x="0" y="1262" width="1080" height="88" fill="%s"/>' % c.lg([(0, "#12040A", 0), (0.4, "#12040A", 1)], 0, 0, 0, 1))
    c.add(glass_panel(c, 92, 72, 896, 548, 36, "#16061E", 0.74, "#E9B949"))
    c.add(gold_frame(c, 22, 5, corner_s=0.9))
    s = spec("E-dussehra-1", (140, 116, 940, 576), "gold", "#FFF4E6", "#FFB74D", "dark", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 2 Ram at sunset + scroll
def card2():
    c = Card(202)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#FFF0CF"), (0.42, "#FBB866"), (0.7, "#E0561F"), (1, "#6E1A1A")]))
    c.add(rays(540, 1000, 36, 1400, "#FFF6DA", 0.1, 0.45))
    c.add('<circle cx="760" cy="1010" r="330" fill="%s"/>' % c.rg([(0, "#FFE7A0", 0.9), (0.35, "#FFB74D", 0.35), (1, "#FF7043", 0)]))
    c.add('<circle cx="760" cy="1010" r="120" fill="%s"/>' % c.rg([(0, "#FFFDE7"), (0.6, "#FFD54F"), (1, "#FF9800")]))
    for y, col, amp in ((1090, "#B8452A", 22), (1150, "#7E2320", 16)):
        c.add(ground(c, y + 20, y - 10, col, 9, amp))
    c.add(ravan(c, 880, 1180, 0.33, burn=0.9))
    c.add(sparks(c, (720, 820, 1040, 1150), 50))
    c.add(ground(c, 1215, 1250, "#2A0E0E", 7, 8))
    c.add('<path d="M0,1350 L0,1250 C80,1236 190,1230 290,1244 C330,1262 340,1300 350,1350 Z" fill="#2A0E0E"/>')
    c.add(ram_archer(c, 175, 1262, 0.86, fill="#2A0E0E", rim="#FFD180", rimw=3))
    c.add('<path d="M470,1040 C600,1000 720,990 840,1030" stroke="#FFE7A0" stroke-width="2" stroke-dasharray="3 10" fill="none" opacity="0.8"/>')
    c.add(scroll_panel(c, 118, 90, 844, 548, rolls="v"))
    c.add(corners(40, 40, 1040, 1310, 0.9, "#7A1E1E", 0.9))
    s = spec("E-dussehra-2", (160, 132, 920, 596), "#7A1010", "#3B1E12", "#B3541E", "light", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 3 close-up effigy + crest plaque
def card3():
    c = Card(303)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.rg([(0, "#43245E"), (0.6, "#1C0F33"), (1, "#0B0616")], 0.5, 0.25, 0.8))
    c.add(stars(c, (30, 30, 1050, 700), 120))
    c.add(rays(540, 520, 28, 900, "#FFB74D", 0.06, 0.4))
    c.add('<circle cx="540" cy="520" r="420" fill="%s"/>' % c.rg([(0, "#FF8F00", 0.35), (1, "#FF8F00", 0)]))
    c.add(ravan(c, 540, 1250, 1.0))
    c.add(fire(c, 150, 1300, 300, 560, n=7))
    c.add(fire(c, 930, 1300, 300, 560, n=7))
    c.add(sparks(c, (40, 520, 1040, 1100), 120))
    x, y, w, h = 108, 700, 864, 562
    d = "M%s,%s H%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s H%s V%s H%s Z" % (
        f(x), f(y), f(x + w * 0.36), f(x + w * 0.44), f(y), f(x + w * 0.46), f(y - 56), f(x + w * 0.5), f(y - 62),
        f(x + w * 0.54), f(y - 56), f(x + w * 0.56), f(y), f(x + w * 0.64), f(y), f(x + w), f(y + h), f(x))
    c.add(panel(c, x, y, w, h, 0, ("#FFF8EA", "#F3E1BC"), "#C9A25A", inner=False, path=d, sw=4))
    c.add('<path d="%s" fill="none" stroke="#C9A25A" stroke-width="1.5" transform="translate(540,981) scale(0.955,0.93) translate(-540,-981)"/>' % d)
    c.add('<circle cx="540" cy="690" r="11" fill="#B71C1C" stroke="#E9B949" stroke-width="3"/>')
    c.add(gold_frame(c, 22, 5, corner_s=0.85))
    s = spec("E-dussehra-3", (152, 744, 928, 1220), "#6A1B1B", "#2B1A2E", "#B7791F", "light", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 4 bow & arrow emblem + apta wreath
def card4():
    c = Card(404)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.rg([(0, "#9C1F33"), (0.6, "#5A0E1C"), (1, "#2A0409")], 0.5, 0.3, 0.9))
    c.add('<rect width="1080" height="1350" fill="%s"/>' % damask(c, "none", "#FFD27A", 0.1, 110))
    cx, cy = 540, 370
    c.add('<circle cx="%d" cy="%d" r="380" fill="%s"/>' % (cx, cy, c.rg([(0, "#FFD27A", 0.45), (0.5, "#FF8F00", 0.12), (1, "#FF8F00", 0)])))
    c.add(rays(cx, cy, 40, 420, "#FFE7A0", 0.1, 0.5))
    # wreath of apta leaves and shami sprigs (lower arc)
    for k in range(15):
        a = math.radians(160 + k * 15.7)
        R = 262
        lx, ly = cx + R * math.cos(a), cy - R * math.sin(a) * 0.95
        rot = 90 - math.degrees(a)
        if 0 < k < 14 and k % 3 == 1:
            c.add(shami_sprig(c, lx, ly, 120, rot - 10))
        c.add(apta_leaf(c, lx, ly, 0.62 if k % 2 else 0.54, rot + (8 if k % 2 else -8),
                        None if k % 2 else c.lg([(0, "#C5E1A5"), (0.5, "#7CB342"), (1, "#33691E")], 0, 0, 1, 1), "#4E3B06" if k % 2 else "#1B3A0C"))
    # bow + flaming arrow on the diagonal
    rot = -38
    c.add(bow(c, cx - 10, cy + 10, 520, drawn=0.32, rot=rot))
    ra = math.radians(rot)
    ux, uy = math.cos(ra), math.sin(ra)
    k = 520 / 600.0
    tail = (cx - 10 - (0.32 * 260 * k + 30) * ux, cy + 10 - (0.32 * 260 * k + 30) * uy)
    tip = (cx - 10 + 250 * ux, cy + 10 + 250 * uy)
    c.add(flaming_arrow(c, tail[0], tail[1], tip[0], tip[1], 1.2, trail=False))
    c.add('<circle cx="%s" cy="%s" r="70" fill="%s"/>' % (f(tip[0]), f(tip[1]), c.rg([(0, "#FFFDE7", 1), (0.3, "#FFD54F", 0.8), (1, "#FF6D00", 0)])))
    c.add(fire(c, tip[0] + 6, tip[1] + 8, 60, 110, n=3, glow=False, logs=False))
    for i in range(14):
        c.add(sparkle(c.rnd.uniform(150, 930), c.rnd.uniform(80, 660), c.rnd.uniform(6, 14), "#FFE7A0", c.rnd.uniform(0.5, 1)))
    x, y, w, h = 112, 716, 856, 548
    d = cut_corner(x, y, w, h, 44)
    c.add(panel(c, x, y, w, h, 0, ("#FFF8EA", "#F6E3BF"), "#D4A64A", inner=False, path=d, sw=5))
    c.add('<path d="%s" fill="none" stroke="#B7791F" stroke-width="1.6"/>' % cut_corner(x + 16, y + 16, w - 32, h - 32, 34))
    c.add(gold_frame(c, 24, 5, corner_s=0.95))
    s = spec("E-dussehra-4", (160, 760, 920, 1222), "#7A0F1E", "#3A1A1A", "#B7791F", "light", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 5 chariot at sunrise + silk banner
def card5():
    c = Card(505)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#FFF4DE"), (0.45, "#FFD7A0"), (0.72, "#F58D5C"), (1, "#8C2F39")]))
    c.add(rays(540, 1010, 44, 1300, "#FFFFFF", 0.13, 0.45))
    c.add(sun_disc(c, 540, 1010, 170))
    for y, col, amp in ((1120, "#C45A45", 18), (1170, "#8E3036", 12)):
        c.add(ground(c, y, y + 10, col, 10, amp))
    for x, h, fl in ((120, 560, False), (960, 560, True)):
        if fl:
            c.add('<g transform="translate(%d,0) scale(-1,1)">%s</g>' % (2 * x, dhwaj(c, x, 1246, h, 210, wave=1.1)))
        else:
            c.add(dhwaj(c, x, 1246, h, 210, wave=1.1))
    c.add(chariot(c, 530, 1236, 0.8, flag=False))
    c.add('<rect x="0" y="1236" width="1080" height="114" fill="%s"/>' % c.lg(["#5A1A22", "#3A0E14"]))
    for k in range(9):
        c.add(apta_leaf(c, [60, 250, 800, 1000, 320, 760, 110, 960, 230][k], [1300, 1296, 1300, 1290, 1318, 1320, 1330, 1334, 1334][k], 0.32, c.rnd.uniform(-70, 70)))
    # hanging silk banner from a gold rod
    c.add('<rect x="96" y="58" width="888" height="16" rx="8" fill="%s"/>' % gold(c, True))
    for ex in (96, 984):
        c.add('<circle cx="%d" cy="66" r="18" fill="%s"/>' % (ex, gold(c, True)))
    x, y, w, h = 118, 74, 844, 520
    d = "M%d,%d H%d V%d L%d,%d L%d,%d L%d,%d Z" % (x, y, x + w, y + h, x + w * 0.75, y + h - 6, 540, y + h + 28, x + w * 0.25, y + h - 6) + " M%d,%d" % (x, y)
    d = "M%s,%s H%s V%s Q%s,%s 540,%s Q%s,%s %s,%s Z" % (f(x), f(y), f(x + w), f(y + h), f(x + w * 0.7), f(y + h + 10), f(y + h + 34), f(x + w * 0.3), f(y + h + 10), f(x), f(y + h))
    c.add(panel(c, x, y, w, h + 34, 0, ("#FFFAF0", "#FBEBD0"), None, inner=False, path=d))
    c.add('<path d="M%s,%s H%s" stroke="#E65100" stroke-width="14"/><path d="M%s,%s H%s" stroke="%s" stroke-width="4" stroke-dasharray="10 6"/>' % (
        f(x), f(y + 14), f(x + w), f(x), f(y + 14), f(x + w), "#FFD27A"))
    c.add('<path d="M%s,%s V%s Q%s,%s 540,%s Q%s,%s %s,%s V%s" fill="none" stroke="#E65100" stroke-width="5"/>' % (
        f(x + 14), f(y + 24), f(y + h - 8), f(x + w * 0.3), f(y + h + 2), f(y + h + 22), f(x + w * 0.7), f(y + h + 2), f(x + w - 14), f(y + h - 8), f(y + 24)))
    c.add('<path d="M540,%s v26" stroke="#E65100" stroke-width="3"/><path d="M540,%s l-12,34 h24 z" fill="#E65100"/><circle cx="540" cy="%s" r="9" fill="%s"/>' % (
        f(y + h + 34), f(y + h + 56), f(y + h + 58), gold(c, True)))
    s = spec("E-dussehra-5", (160, 118, 920, 578), "#8A1C1C", "#3A2012", "#C0661A", "light", "deco")
    return c.svg(), s


def sun_disc(c, cx, cy, r):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(r * 2.6), c.rg([(0, "#FFF3C4", 0.9), (0.4, "#FFCC80", 0.4), (1, "#FF8A65", 0)])) +
            '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(r), c.rg([(0, "#FFFFFF"), (0.5, "#FFE082"), (1, "#FFA726")], 0.45, 0.4, 0.6)))


# ---------------------------------------------------------------- 6 apta-leaf 'sona' corners, emerald
def leaf_fan(c, ox, oy, base_ang, spread, n, R, scale, thread="#C62828"):
    out = []
    for i in range(n):
        a = base_ang - spread / 2 + spread * i / (n - 1)
        ar = math.radians(a)
        lx, ly = ox + R * 0.25 * math.cos(ar), oy + R * 0.25 * math.sin(ar)
        out.append(shami_sprig(c, lx, ly, R * 1.05, a + 90 + 7, "#2E6B22", "#7CB342") if i % 2 else "")
    for i in range(n):
        a = base_ang - spread / 2 + spread * i / (n - 1)
        ar = math.radians(a)
        lx, ly = ox + R * 0.22 * math.cos(ar), oy + R * 0.22 * math.sin(ar)
        g = None if i % 3 else c.lg([(0, "#DCEDC8"), (0.5, "#8BC34A"), (1, "#33691E")], 0, 0, 1, 1)
        out.append(apta_leaf(c, lx, ly, scale * (1 - abs(i - (n - 1) / 2) / n * 0.3), a + 90, g, "#4E3B06" if g is None else "#1B3A0C"))
    out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(ox + R * 0.2 * math.cos(math.radians(base_ang))), f(oy + R * 0.2 * math.sin(math.radians(base_ang))), f(R * 0.09), c.rg([(0, "#FF5252"), (1, "#8E0000")])))
    for k in range(3):
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width="4" transform="rotate(%s %s %s)"/>' % (
            f(ox + R * 0.2 * math.cos(math.radians(base_ang))), f(oy + R * 0.2 * math.sin(math.radians(base_ang))), f(R * 0.1), f(R * 0.04), thread if k != 1 else "#FFD27A",
            f(base_ang + 90 + k * 12), f(ox + R * 0.2 * math.cos(math.radians(base_ang))), f(oy + R * 0.2 * math.sin(math.radians(base_ang)))))
    return "".join(out)


def card6():
    c = Card(606)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#0B3327"), (0.5, "#15503C"), (1, "#0A2A20")], 0, 0, 1, 1))
    c.add('<rect width="1080" height="1350" fill="%s"/>' % damask(c, "none", "#E9C46A", 0.09, 96))
    c.add(bokeh(c, 40, (0, 0, 1080, 1350), ["#FFD27A", "#FFF1B0"], 3, 16, (0.1, 0.45)))
    ox, oy = 540, 560
    c.add('<circle cx="%d" cy="%d" r="470" fill="%s"/>' % (ox, oy - 120, c.rg([(0, "#FFE7A0", 0.4), (0.6, "#FFD27A", 0.08), (1, "#FFD27A", 0)])))
    c.add(rays(ox, oy, 36, 700, "#FFE7A0", 0.04, 0.45))
    # crossed bow + flaming arrow behind the bouquet
    c.add(bow(c, ox - 150, oy - 250, 470, drawn=0.0, rot=-35))
    c.add(flaming_arrow(c, ox - 330, oy - 40, ox + 330, oy - 470, 1.0))
    c.add(leaf_fan(c, ox, oy + 30, -90, 140, 7, 600, 1.55))
    c.add(leaf_fan(c, -20, 1370, -45, 80, 5, 330, 0.85))
    c.add(leaf_fan(c, 1100, 1370, -135, 80, 5, 330, 0.85))
    x, y, w, h = 112, 590, 856, 560
    c.add(panel(c, x, y, w, h, 40, ("#FFFDF5", "#F7EED6"), "#C9A25A", sw=3))
    c.add(corners(x + 26, y + 26, x + w - 26, y + h - 26, 0.42, "#B7791F", 0.9))
    c.add(gold_frame(c, 22, 4, corner_s=0.8))
    s = spec("E-dussehra-6", (160, 636, 920, 1104), "#0E5A40", "#1E2B24", "#B7791F", "light", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 7 victory flags + distant effigies, maroon banner
def card7():
    c = Card(707)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#240818"), (0.3, "#5E1530"), (0.52, "#C0442A"), (0.62, "#F28C3C"), (1, "#F7B267")]))
    c.add(stars(c, (40, 30, 1040, 300), 60))
    hy = 720
    sil = silhouette(c, "#2A0A12")
    for x, s_, hd in ((250, 0.26, 0), (560, 0.36, 1), (850, 0.24, 0)):
        c.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="%s"/>' % (x, hy - 60, int(260 * s_ / 0.3), int(260 * s_ / 0.3), c.rg([(0, "#FFB300", 0.6), (1, "#FF5722", 0)])))
        if hd:
            c.add('<g filter="%s">%s</g>' % (sil, ravan(c, x, hy, s_)))
        else:
            c.add(effigy_silhouette(c, x, hy, s_ * 1.3, "#2A0A12", 1))
        c.add(fire(c, x, hy + 4, 180 * s_ / 0.3, 200 * s_ / 0.3, n=6, logs=False))
    c.add(smoke(c, 560, 520, 300, 420, "#3A1A2A", 0.45))
    c.add(sparks(c, (100, 300, 980, 720), 120))
    c.add(ground(c, hy, hy + 10, "#1E060C", 12, 5))
    c.add(crowd(c, 0, 1080, hy + 70, 60, "#140409"))
    c.add('<rect x="0" y="%d" width="1080" height="%d" fill="#140409"/>' % (hy + 60, H - hy - 60))
    c.add(dhwaj(c, 120, 820, 660, 470, wave=1.3))
    c.add('<g transform="translate(1920,0) scale(-1,1)">%s</g>' % dhwaj(c, 960, 820, 560, 360, color=("#FFB74D", "#F57C00"), wave=0.9, emblem=False))
    # maroon cloth banner on gold rod
    c.add('<rect x="74" y="724" width="932" height="18" rx="9" fill="%s"/>' % gold(c, True))
    for ex in (74, 1006):
        c.add('<circle cx="%d" cy="733" r="17" fill="%s"/>' % (ex, gold(c, True)))
    x, y, w, h = 100, 742, 880, 520
    c.add(panel(c, x, y, w, h, 0, ("#7A1024", "#4A0716"), None, inner=False, texture=True, path=rr(x, y, w, h, 6)))
    c.add('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#E9B949" stroke-width="3"/>' % (x + 16, y + 16, w - 32, h - 32))
    c.add('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#E9B949" stroke-width="1.2" stroke-dasharray="2 6"/>' % (x + 26, y + 26, w - 52, h - 52))
    for tx in list(range(x + 20, 320, 34)) + list(range(772, x + w - 10, 34)):
        c.add('<path d="M%d,%d v26" stroke="#E9B949" stroke-width="2"/><path d="M%d,%d l-6,18 h12 z" fill="#E9B949"/>' % (tx, y + h, tx, y + h + 22))
    c.add(gold_frame(c, 22, 4, corner_s=0.8))
    s = spec("E-dussehra-7", (144, 774, 936, 1236), "gold", "#FFF1E0", "#FFC76B", "dark", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 8 diagonal: blazing heads top-right, golden Ram bottom-left
def card8():
    c = Card(808)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.rg([(0, "#4A0F0F"), (0.55, "#240707"), (1, "#0E0303")], 0.7, 0.2, 1.0))
    c.add(smoke(c, 780, 360, 420, 380, "#1A0606", 0.5))
    c.add('<circle cx="820" cy="190" r="480" fill="%s"/>' % c.rg([(0, "#FF9100", 0.5), (0.5, "#FF3D00", 0.15), (1, "#FF3D00", 0)]))
    c.add(ravan(c, 800, 200 + 760 * 0.68, 0.68, heads_only=True))
    c.add(fire(c, 800, 400, 760, 120, n=14, logs=False))
    c.add(sparks(c, (380, 40, 1080, 380), 130))
    gr = gold(c, True)
    c.add(flaming_arrow(c, 380, 1000, 700, 330, 1.1))
    c.add(ram_archer(c, 120, 1292, 0.6, fill=c.lg(["#FFE7A0", "#E0A526", "#9C6516"], 0, 0, 0, 1), rim="#5A1A00", rimw=2, arrow=True, arrow_flame=True))
    c.add('<path d="M0,1350 L0,1300 C120,1290 260,1296 330,1330 L330,1350 Z" fill="#2A0808"/>')
    c.add(glass_panel(c, 104, 352, 872, 548, 30, "#0E0303", 0.9, "#E9B949"))
    c.add(gold_frame(c, 22, 4, corner_s=0.8))
    s = spec("E-dussehra-8", (150, 396, 930, 856), "gold", "#FFF3E3", "#FFB74D", "dark", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 9 lakeside panorama with reflections
def card9():
    c = Card(909)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#0A1A2E"), (0.4, "#13324A"), (0.62, "#6B3A4A"), (0.7, "#D9723A"), (1, "#0A1A2E")]))
    c.add(stars(c, (40, 30, 1040, 560), 120))
    hz = 1000
    grp = []
    grp.append('<circle cx="540" cy="%d" r="420" fill="%s"/>' % (hz - 200, c.rg([(0, "#FF9800", 0.55), (1, "#FF5722", 0)])))
    for x, s_ in ((200, 0.9), (880, 0.8)):
        grp.append(effigy_silhouette(c, x, hz - 6, s_ * 0.42, "#1B0A12", 1))
        grp.append(fire(c, x, hz, 150, 190, n=5, logs=False))
    grp.append(ravan(c, 540, hz - 4, 0.42, burn=0.95))
    grp.append(ground(c, hz - 10, hz - 14, "#140A14", 12, 4))
    scene = "".join(grp)
    c.add(scene)
    c.add(sparks(c, (100, 620, 980, 980), 110))
    # lake + reflection
    c.add('<rect x="0" y="%d" width="1080" height="%d" fill="%s"/>' % (hz, H - hz, c.lg(["#3A1F2A", "#0C1624"])))
    cp = c.clip('<rect x="0" y="%d" width="1080" height="%d"/>' % (hz, H - hz))
    c.add('<g clip-path="%s" opacity="0.4" filter="%s"><g transform="translate(0,%s) scale(1,-0.6)">%s</g></g>' % (cp, c.blur(2.5), f(hz + hz * 0.6), scene))
    for i in range(40):
        y = hz + 10 + (i / 40.0) ** 1.4 * 250
        w = c.rnd.uniform(40, 260)
        c.add('<rect x="%s" y="%s" width="%s" height="2.4" rx="1" fill="#FFB74D" opacity="%s"/>' % (f(540 + c.rnd.uniform(-240, 240) - w / 2), f(y), f(w), f(c.rnd.uniform(0.15, 0.5))))
    c.add('<rect x="0" y="1262" width="1080" height="88" fill="%s"/>' % c.lg([(0, "#0C1624", 0), (0.5, "#0C1624", 1)], 0, 0, 0, 1))
    # parchment panel with gold border on top
    c.add(panel(c, 104, 70, 872, 540, 26, ("#FFF7E8", "#F4E2C2"), "#C9A25A", sw=4))
    c.add(corners(130, 96, 950, 584, 0.42, "#B7791F"))
    c.add(gold_frame(c, 22, 4, corner_s=0.8))
    s = spec("E-dussehra-9", (150, 114, 930, 574), "#5A1A2E", "#241A2A", "#B7791F", "light", "deco")
    return c.svg(), s


# ---------------------------------------------------------------- 10 paper-cut layers
def card10():
    c = Card(1010)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg(["#FFE3C2", "#FFC89A", "#F79A6A"]))
    sh = c.shadow(6, 7, 0.35, "#4A0E0E")
    cols = ["#F8B26A", "#EF8E4F", "#E0673B", "#C44A30", "#9E2F2A"]
    for k, colr in enumerate(reversed(cols)):
        yb = 300 - k * 52
        p = [(0, 0)]
        for i in range(13):
            t = i / 12
            p.append((W * t, yb + 30 * math.sin(t * math.pi * 3 + k * 1.3) + 16 * math.sin(t * math.pi * 7 + k)))
        p.append((W, 0))
        c.add('<path d="M%s Z" fill="%s" filter="%s"/>' % (" L".join("%s,%s" % (f(a), f(b)) for a, b in p), colr, sh))
    for i in range(10):
        c.add(sparkle(c.rnd.uniform(60, 1020), c.rnd.uniform(30, 200), c.rnd.uniform(5, 10), "#FFF3D6", 0.8))
    # bottom paper hills
    for k, (yb, colr) in enumerate(((1010, "#E0673B"), (1080, "#B23A2E"), (1160, "#7A1F24"))):
        p = []
        for i in range(13):
            t = i / 12
            p.append((W * t, yb + 26 * math.sin(t * math.pi * 2.4 + k * 2) + 10 * math.sin(t * math.pi * 6)))
        c.add('<path d="M0,1350 L%s L1080,1350 Z" fill="%s" filter="%s"/>' % (pts(p), colr, sh))
    sil = silhouette(c, "#4A0E14")
    c.add('<g filter="%s">%s</g>' % (c.shadow(6, 7, 0.4, "#2A0508"), '<g filter="%s">%s</g>' % (sil, ravan(c, 850, 1236, 0.42))))
    c.add(fire(c, 850, 1242, 190, 210, n=6, logs=False))
    c.add('<path d="M0,1350 L0,1236 C160,1222 360,1232 420,1260 C400,1300 380,1330 330,1350 Z" fill="#4A0E14" filter="%s"/>' % sh)
    c.add(ram_archer(c, 150, 1250, 0.62, fill="#4A0E14", rim="#FFD7A8", rimw=2))
    c.add('<path d="M360,1000 C520,960 640,960 760,1010" stroke="#4A0E14" stroke-width="2" stroke-dasharray="4 10" fill="none" opacity="0.7"/>')
    # paper tag panel
    x, y, w, h = 108, 348, 864, 560
    c.add('<path d="%s" fill="#FFFBF4" filter="%s"/>' % (rr(x, y, w, h, 28), c.shadow(10, 12, 0.35, "#4A0E0E")))
    c.add('<path d="%s" fill="none" stroke="#E0673B" stroke-width="3" stroke-dasharray="12 8"/>' % rr(x + 18, y + 18, w - 36, h - 36, 18))
    for (px, py) in ((x + 40, y + 40), (x + w - 40, y + 40)):
        c.add('<circle cx="%d" cy="%d" r="9" fill="#F7A06A"/>' % (px, py))
    s = spec("E-dussehra-10", (156, 392, 924, 864), "#8E1B1B", "#3A1A14", "#D2572A", "light", "deco")
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
