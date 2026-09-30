"""Good-morning wish-card art (agent A). python3 tools/cards3/gen_good-morning.py [n ...]"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_a import *
from gm_motifs_a import *

CAT = "good-morning"


def engine_arch(x, y, w, h):
    """Exact copy of the engine's archPath (static/cards.js) so the slot frame hugs the photo."""
    cx = x + w / 2
    sh = y + h * 0.34
    return ("M%s,%s L%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s L%s,%s Z" % (
        f(x), f(y + h), f(x), f(sh),
        f(x), f(sh - h * 0.12), f(x + w * 0.18), f(y + h * 0.1), f(cx - w * 0.1), f(y + h * 0.045),
        f(cx - w * 0.04), f(y + h * 0.02), f(cx), f(y + h * 0.01), f(cx), f(y),
        f(cx), f(y + h * 0.01), f(cx + w * 0.04), f(y + h * 0.02), f(cx + w * 0.1), f(y + h * 0.045),
        f(x + w - w * 0.18), f(y + h * 0.1), f(x + w), f(sh - h * 0.12), f(x + w), f(sh), f(x + w), f(y + h)))


def mat_edge(c, color="#FFF8EE", inset=22, r=34, line="#E0A526"):
    """Card edge: a cream mat around the art with rounded inner corners and a fine gold line."""
    d = "M0,0 H1080 V1350 H0 Z " + rr(inset, inset, W - 2 * inset, H - 2 * inset, r)
    return ('<path d="%s" fill="%s" fill-rule="evenodd"/>' % (d, color) +
            '<path d="%s" fill="none" stroke="%s" stroke-width="2.5"/>' % (rr(inset, inset, W - 2 * inset, H - 2 * inset, r), line) +
            '<path d="%s" fill="none" stroke="#000" stroke-opacity="0.12" stroke-width="6" filter="%s"/>' % (rr(inset + 3, inset + 3, W - 2 * inset - 6, H - 2 * inset - 6, r), c.blur(3)))


def grass(c, y, x0=0, x1=W, n=160, cols=("#7CB342", "#33691E"), hmin=20, hmax=60):
    out = []
    for i in range(n):
        x = c.rnd.uniform(x0, x1)
        h = c.rnd.uniform(hmin, hmax)
        lean = c.rnd.uniform(-14, 14)
        out.append('<path d="M%s,%s Q%s,%s %s,%s Q%s,%s %s,%s Z" fill="%s"/>' % (
            f(x - 3), f(y), f(x + lean * 0.3), f(y - h * 0.6), f(x + lean), f(y - h), f(x + lean * 0.3 + 4), f(y - h * 0.5), f(x + 4), f(y), cols[i % 2]))
    return "".join(out)


def sunflower_plant(c, x, y, top, r, rot=0, tilt=1.0, bend=20):
    """Sunflower on a stem with two leaves; stem base (x,y), head at (x+bend*.5, top)."""
    hx = x + bend * 0.5
    out = [stem(x, y, hx, top, bend, "#4E7D2A", max(6, r * 0.12))]
    my = (y + top) / 2
    out.append(leaf(c, x + bend * 0.3, my + 30, r * 1.2, -55, ("#8BC34A", "#2E5E1A"), drops=1))
    out.append(leaf(c, x + bend * 0.3, my - 20, r * 1.05, 60, ("#8BC34A", "#2E5E1A"), drops=1))
    out.append(sunflower(c, hx, top, r, rot, tilt))
    return "".join(out)


def cloud_panel(c, x, y, w, h):
    """Fluffy white cloud-shaped text panel."""
    circ = []
    n = 7
    for i in range(n):
        cx = x + 40 + i * (w - 80) / (n - 1)
        rr_ = 70 + (i % 3) * 22
        circ.append((cx, y + 20 - (i % 2) * 18, rr_))
        circ.append((cx + 30, y + h - 10 + (i % 2) * 14, 60 + ((i + 1) % 3) * 16))
    for yy in (y + h * 0.3, y + h * 0.7):
        circ.append((x + 8, yy, 70))
        circ.append((x + w - 8, yy, 70))
    shape = "".join('<circle cx="%s" cy="%s" r="%s"/>' % (f(a), f(b), f(r)) for a, b, r in circ) + '<rect x="%s" y="%s" width="%s" height="%s" rx="40"/>' % (f(x), f(y), f(w), f(h))
    out = ['<g fill="#8FB8D8" opacity="0.45" filter="%s" transform="translate(0,18)">%s</g>' % (c.blur(14), shape)]
    out.append('<g fill="%s">%s</g>' % (c.lg([(0, "#FFFFFF"), (0.7, "#FFFFFF"), (1, "#E6F1FA")]), shape))
    return "".join(out)


def coffee_bean(x, y, s, rot):
    return ('<g transform="translate(%s,%s) rotate(%s) scale(%s)"><ellipse rx="16" ry="11" fill="#4A2A16"/>'
            '<ellipse rx="16" ry="11" fill="none" stroke="#2A1408" stroke-width="1"/>'
            '<path d="M-13,0 C-6,-5 6,5 13,0" stroke="#1E0E04" stroke-width="2.4" fill="none"/>'
            '<ellipse cx="-5" cy="-5" rx="5" ry="2" fill="#fff" opacity="0.18"/></g>') % (f(x), f(y), f(rot), f(s))


# ================================================================ 1 sunrise over the sea
def card1():
    c = Card(301)
    hz = 820
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#8FB3E0"), (0.35, "#F7C9C0"), (0.62, "#FDB98A"), (0.61, "#FFD9A6")], 0, 0, 0, 1))
    c.add('<rect width="1080" height="%d" fill="%s"/>' % (hz, c.lg([(0, "#9DBBE3"), (0.45, "#F6C7C4"), (0.8, "#FFC79A"), (1, "#FFE0AE")])))
    c.add(sun(c, 540, hz + 4, 104, halo_r=4.2, rays_n=28, rays_op=0.3))
    for (x, y, s) in ((170, 560, 0.9), (900, 610, 1.1), (360, 690, 0.6), (760, 720, 0.55), (60, 740, 0.7)):
        c.add(cloud(c, x, y, s, "#FFF4EC", "#F4A99A", 0.85))
    c.add(sea(c, hz, 0, W, H, "#F7B28A", "#2C4C7A", 540))
    c.add('<rect x="0" y="%d" width="1080" height="%d" fill="%s"/>' % (hz, H - hz, c.lg([(0, "#1E3A63", 0), (0.7, "#1E3A63", 0.25), (1, "#12284A", 0.7)])))
    # distant sail boat
    c.add('<g transform="translate(830,%d)"><path d="M-40,0 H40 L30,12 H-30 Z" fill="#2A2F4A"/><path d="M0,-4 V-78 L34,-8 Z" fill="#3A3F5E"/><path d="M-4,-8 V-62 L-30,-8 Z" fill="#4A4F70"/></g>' % (hz + 30))
    c.add(flock(c, 760, 690, 5, 110, "#3E3450", 0.35, 0.7))
    c.add(bird(300, 760, 0.55, "#3E3450", 0.4, -8))
    c.add(watermark_calm(c, "#1A3050", 0.6))
    # frosted glass panel
    x, y, w, h = 92, 96, 896, 560
    d = rr(x, y, w, h, 44)
    c.add('<path d="%s" fill="#FFFFFF" opacity="0.82" filter="%s"/>' % (d, c.shadow(18, 28, 0.25, "#5A3A5A")))
    c.add('<path d="%s" fill="%s"/>' % (d, c.lg([(0, "#FFFFFF", 0.5), (1, "#FFE9DC", 0.3)])))
    c.add('<path d="%s" fill="none" stroke="#E7A77A" stroke-width="2"/>' % rr(x + 14, y + 14, w - 28, h - 28, 32))
    for (sx, sy) in ((x + 46, y + 46), (x + w - 46, y + 46)):
        c.add(sparkle(sx, sy, 14, "#E7A77A"))
    c.add(mat_edge(c, "#FFF6EE", 22, 36, "#E7A77A"))
    s = spec("E-good-morning-1", (150, 146, 930, 606), "#B23A1E", "#2E2A3A", "#D0703C", "light", "script")
    return c.svg(), s


# ================================================================ 2 tea on the table in window light
def card2():
    c = Card(302)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#FCEFDD"), (1, "#F1D2AE")]))
    c.add('<rect width="1080" height="1350" fill="%s"/>' % damask(c, "none", "#C58A4A", 0.07, 110))
    # window-light patches on the wall
    for (x0, y0) in ((520, 560), (760, 560)):
        c.add('<path d="M%d,%d l200,-60 l0,190 l-200,60 Z" fill="#FFF8E6" opacity="0.55" filter="%s"/>' % (x0, y0, c.blur(8)))
    c.add(light_beams(c, 900, 0, 1080, 200, (-700, 900), 6, "#FFF6D8", 0.35))
    # table
    ty = 1090
    c.add('<rect x="0" y="%d" width="1080" height="%d" fill="%s"/>' % (ty, H - ty, c.lg([(0, "#A0643A"), (0.12, "#8A5230"), (1, "#4E2C18")])))
    for k in range(9):
        yy = ty + 20 + k * 28 + c.rnd.uniform(-5, 5)
        c.add('<path d="M0,%s C300,%s 700,%s 1080,%s" stroke="#3A1F0E" stroke-opacity="0.18" stroke-width="2" fill="none"/>' % (f(yy), f(yy + c.rnd.uniform(-10, 10)), f(yy + c.rnd.uniform(-10, 10)), f(yy)))
    c.add('<rect x="0" y="%d" width="1080" height="8" fill="#C58A57"/>' % ty)
    # checked runner under the cup
    rx0, rx1 = 420, 1080
    c.add('<path d="M%d,%d H%d V%d H%d Z" fill="%s"/>' % (rx0, ty + 20, rx1, H, rx0 - 60, c.pattern(40, 40, '<rect width="40" height="40" fill="#F4EDE0"/><rect width="20" height="40" fill="#D9534F" opacity="0.55"/><rect width="40" height="20" fill="#D9534F" opacity="0.55"/>')))
    c.add('<path d="M%d,%d H%d" stroke="#B53B36" stroke-width="4"/>' % (rx0, ty + 20, rx1))
    # bud vase with sunflower
    vx = 230
    c.add(stem(vx, ty - 150, vx - 10, 740, -30, "#4E7D2A", 9))
    c.add(leaf(c, vx - 6, 900, 120, -50, ("#8BC34A", "#2E5E1A"), drops=1))
    c.add(leaf(c, vx - 4, 860, 100, 55, ("#8BC34A", "#2E5E1A"), drops=1))
    c.add(sunflower(c, vx - 12, 740, 96, 12))
    c.add('<path d="M%d,%d C%d,%d %d,%d %d,%d L%d,%d C%d,%d %d,%d %d,%d Z" fill="%s" filter="%s"/>' % (
        vx - 26, ty - 200, vx - 30, ty - 150, vx - 76, ty - 90, vx - 60, ty + 30, vx + 60, ty + 30, vx + 76, ty - 90, vx + 30, ty - 150, vx + 26, ty - 200,
        c.lg([(0, "#5DA3A0"), (0.4, "#9ED5CF"), (1, "#2F6F6B")], 0, 0, 1, 0), c.shadow(10, 10, 0.3)))
    c.add('<ellipse cx="%d" cy="%d" rx="28" ry="8" fill="#2F6F6B"/>' % (vx, ty - 200))
    c.add('<path d="M%d,%d q10,60 0,130" stroke="#fff" stroke-opacity="0.35" stroke-width="10" fill="none" stroke-linecap="round"/>' % (vx - 34, ty - 110))
    # teacup hero
    c.add(teacup(c, 700, 900, 1.05, ("#FFFFFF", "#D6DEE8"), "#2E6D8E", "#D9A23A", ("#C8793E", "#7A3B12")))
    # biscuits
    for k, (bx, by) in enumerate(((930, 1175), (990, 1205))):
        c.add('<ellipse cx="%d" cy="%d" rx="58" ry="22" fill="%s" filter="%s"/>' % (bx, by, c.lg(["#E9B872", "#B67A34"]), c.shadow(5, 5, 0.3)))
        for d_ in range(6):
            c.add('<circle cx="%s" cy="%s" r="2.5" fill="#8A5020"/>' % (f(bx - 30 + d_ * 12), f(by - 4 + (d_ % 2) * 6)))
    c.add(watermark_calm(c, "#3A200E", 0.55))
    # notebook panel with spiral binding
    x, y, w, h = 104, 96, 872, 540
    c.add('<rect x="%d" y="%d" width="%d" height="%d" rx="14" fill="%s" filter="%s"/>' % (x, y, w, h, c.lg(["#FFFDF7", "#FBF3E4"]), c.shadow(14, 20, 0.3, "#5A3A1A")))
    c.add('<rect x="%d" y="%d" width="%d" height="%d" rx="14" fill="none" stroke="#E4CFAE" stroke-width="2"/>' % (x, y, w, h))
    c.add('<path d="M%d,%d V%d" stroke="#E57373" stroke-width="2" opacity="0.6"/>' % (x + 46, y + 40, y + h - 10))
    for k in range(17):
        sx = x + 60 + k * (w - 120) / 16
        c.add('<circle cx="%s" cy="%d" r="8" fill="#6B4A2A"/>' % (f(sx), y + 26))
        c.add('<path d="M%s,%d C%s,%d %s,%d %s,%d" stroke="%s" stroke-width="5" fill="none" stroke-linecap="round"/>' % (
            f(sx), y + 26, f(sx - 4), y - 6, f(sx + 10), y - 14, f(sx + 12), y + 6, c.lg(["#F5F5F5", "#9E9E9E"], 0, 0, 1, 0)))
    s = spec("E-good-morning-2", (170, 150, 940, 612), "#9A3412", "#3A2A1E", "#2E6D8E", "light", "script")
    return c.svg(), s


# ================================================================ 3 sunflower field + cloud panel
def card3():
    c = Card(303)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#5FB3EA"), (0.5, "#A8DBF7"), (0.8, "#FFF1C8"), (1, "#FFE39A")]))
    c.add(sun(c, 930, 140, 80, halo_r=4, rays_n=24, rays_op=0.35))
    c.add(cloud(c, 150, 150, 0.8, "#FFFFFF", "#CFE3F2"))
    c.add(flock(c, 700, 160, 4, 90, "#2F4A66", 0.35, 0.6))
    # distant field
    c.add(hills(c, [(940, 20, ("#B7D66A", "#8CB23E"), 0.4, 3), (1010, 16, ("#8FB33A", "#5E8A22"), 1.8, 4)]))
    for k in range(40):
        x = c.rnd.uniform(20, 1060); y = c.rnd.uniform(950, 1010)
        c.add('<circle cx="%s" cy="%s" r="%s" fill="#F9C23C"/><circle cx="%s" cy="%s" r="%s" fill="#6D4C1F"/>' % (f(x), f(y), f(9 + (y - 950) * 0.12), f(x), f(y), f(3 + (y - 950) * 0.04)))
    # foreground sunflowers
    c.add('<rect x="0" y="1100" width="1080" height="250" fill="%s"/>' % c.lg([(0, "#5E8A22"), (1, "#2E4F12")]))
    for (x, y, top, r, rot, bend) in ((70, 1350, 1000, 118, -10, 30), (250, 1350, 1070, 96, 8, -20), (860, 1350, 1060, 104, 12, 30), (1020, 1350, 980, 124, -6, -30),
                                      (420, 1350, 1150, 70, 0, 10), (660, 1350, 1150, 74, 0, -10)):
        c.add(sunflower_plant(c, x, y, top, r, rot, 0.96, bend))
    c.add(grass(c, 1350, 0, 1080, 200, ("#6FA02E", "#3B6A18"), 30, 90))
    c.add(watermark_calm(c, "#1E3A0C", 0.6))
    c.add(cloud_panel(c, 110, 290, 860, 520))
    s = spec("E-good-morning-3", (160, 320, 920, 786), "#C25B00", "#1F3348", "#2F7FB5", "light", "classic")
    return c.svg(), s


# ================================================================ 4 window with sunlight (photo in the window)
def card4():
    c = Card(304)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#E4EEE0"), (1, "#CFE0CB")]))
    sprig = c.pattern(90, 90, '<g fill="#6E9A6A" opacity="0.13"><path d="M20,70 C28,50 36,40 50,30" stroke="#6E9A6A" stroke-width="2" fill="none"/>'
                              '<ellipse cx="30" cy="54" rx="9" ry="4" transform="rotate(-50 30 54)"/><ellipse cx="42" cy="40" rx="9" ry="4" transform="rotate(-30 42 40)"/>'
                              '<circle cx="70" cy="20" r="3"/><circle cx="80" cy="80" r="2"/></g>')
    c.add('<rect width="1080" height="1350" fill="%s"/>' % sprig)
    wx, wy, ww, wh = 300, 70, 480, 520
    arch = engine_arch(wx, wy, ww, wh)
    # sunlight falling from the window
    c.add('<path d="M%d,%d L%d,%d L1080,1350 L0,1350 Z" fill="%s" filter="%s"/>' % (wx, wy + wh, wx + ww, wy + wh, c.lg([(0, "#FFF4C8", 0.55), (1, "#FFF4C8", 0)]), c.blur(10)))
    # open shutters
    sw = 150
    for side in (-1, 1):
        ex = wx if side < 0 else wx + ww
        ox = ex + side * sw
        d = "M%s,%s L%s,%s L%s,%s L%s,%s Z" % (f(ex), f(wy + 110), f(ox), f(wy + 150), f(ox), f(wy + wh - 20), f(ex), f(wy + wh))
        c.add('<path d="%s" fill="%s" stroke="#7F9A8E" stroke-width="4" filter="%s"/>' % (d, c.lg(["#5F9E92", "#3E7A6E"], 0, 0, 1, 0), c.shadow(6, 8, 0.25)))
        for k in range(1, 14):
            t = k / 14
            ya = wy + 110 + (wh - 110) * t
            yb = wy + 150 + (wh - 170) * t
            c.add('<path d="M%s,%s L%s,%s" stroke="#1F4A40" stroke-opacity="0.35" stroke-width="3"/>' % (f(ex), f(ya), f(ox), f(yb)))
        c.add('<circle cx="%s" cy="%s" r="6" fill="#D9A23A"/>' % (f(ox - side * 22), f(wy + wh * 0.55)))
    # view (placeholder when no photo)
    cp = c.clip('<path d="%s"/>' % arch)
    c.add('<g clip-path="%s">' % cp)
    c.add('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (wx, wy, ww, wh, c.lg(["#8EC5FC", "#FFE3B3", "#FFB88C"])))
    c.add(sun(c, wx + ww * 0.5, wy + wh * 0.68, 50, halo_r=4))
    c.add(hills(c, [(wy + wh * 0.72, 30, ("#A9BFD0", "#88A3B8"), 0.5, 2), (wy + wh * 0.84, 26, ("#6E9A7A", "#4A7556"), 2.1, 3)], wx, wx + ww, wy + wh))
    c.add(flock(c, wx + ww * 0.35, wy + wh * 0.34, 4, 60, "#4A3B52", 0.3, 0.5))
    c.add('</g>')
    # frame
    c.add('<path d="%s" fill="none" stroke="#B9A88A" stroke-width="34"/>' % arch)
    c.add('<path d="%s" fill="none" stroke="#FFFDF6" stroke-width="24"/>' % arch)
    c.add('<path d="%s" fill="none" stroke="#D9C9A8" stroke-width="2"/>' % engine_arch(wx - 12, wy - 12, ww + 24, wh + 24))
    # sill + plants
    c.add('<path d="M%d,%d h%d l-22,30 h%d Z" fill="%s" filter="%s"/>' % (wx - 60, wy + wh + 8, ww + 120, -(ww + 76), c.lg(["#FFFDF6", "#D8CBB0"]), c.shadow(8, 8, 0.25)))
    for (px, sc) in ((wx - 44, 0.9), (wx + ww + 44, 1.0)):
        py = wy + wh + 8
        for k in range(7):
            a = (k - 3) * 22
            c.add(leaf(c, px, py - 50 * sc, (64 + (3 - abs(k - 3)) * 16) * sc, a, ("#AED581", "#2E7D32"), drops=0))
        c.add('<path d="M%s,%s L%s,%s L%s,%s L%s,%s Z" fill="%s"/>' % (f(px - 40 * sc), f(py - 58 * sc), f(px + 40 * sc), f(py - 58 * sc), f(px + 30 * sc), f(py), f(px - 30 * sc), f(py), c.lg(["#E07A4F", "#B5522B"], 0, 0, 1, 0)))
        c.add('<rect x="%s" y="%s" width="%s" height="%s" rx="4" fill="#C8643A"/>' % (f(px - 44 * sc), f(py - 66 * sc), f(88 * sc), f(12 * sc)))
    # hanging vines from the top corners
    c.add(vine(c, [(40, -10), (70, 90), (40, 190), (80, 290), (50, 390), (90, 470)], ((66, 150, 26), (60, 330, 30), (92, 460, 22)), ("#F48FB1", "#C2185B")))
    c.add(vine(c, [(1040, -10), (1010, 100), (1040, 200), (1000, 300), (1030, 400)], ((1016, 120, 28), (1010, 300, 24)), ("#F48FB1", "#C2185B")))
    # plaque
    x, y, w, h = 96, 690, 888, 560
    c.add(panel(c, x, y, w, h, 30, ("#FFFFFF", "#F6FAF3"), "#8DB08A", sw=2.5))
    for (sx, sy, rot) in ((x + 30, y + 30, 0), (x + w - 30, y + 30, 90), (x + w - 30, y + h - 30, 180), (x + 30, y + h - 30, 270)):
        c.add('<g transform="translate(%d,%d) rotate(%d)">%s%s</g>' % (sx, sy, rot, heart_leaf(c, 18, 4, 0.34, 120, ("#A5D6A7", "#43A047")), heart_leaf(c, 4, 18, 0.34, 150, ("#A5D6A7", "#43A047"))))
    photo = {"shape": "arch", "x": wx, "y": wy, "w": ww, "h": wh}
    s = spec("E-good-morning-4", (150, 738, 930, 1202), "#2E6B3A", "#23302A", "#C07A2A", "light", "script", photo=photo)
    return c.svg(), s


# ================================================================ 5 layered hills at dawn, text on the dark hill
def card5():
    c = Card(305)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#6F5BB0"), (0.3, "#B39AD8"), (0.52, "#FFC2A8"), (0.62, "#FFE3B8")]))
    c.add(sun(c, 540, 590, 120, halo_r=4.5, rays_n=32, rays_op=0.28))
    for (x, y, s) in ((150, 200, 0.9), (880, 150, 1.1), (560, 300, 0.6), (80, 420, 0.7), (1000, 400, 0.75)):
        c.add(cloud(c, x, y, s, "#FFF1F4", "#C9A2D8", 0.8))
    c.add(flock(c, 280, 330, 6, 120, "#3A2A5A", 0.35, 0.75))
    c.add(bird(820, 300, 0.7, "#3A2A5A", -0.4, 6))
    c.add(hills(c, [(640, 40, ("#E8A6B8", "#D08AA6"), 0.2, 2), (690, 50, ("#B67AA6", "#98628E"), 1.4, 3),
                    (740, 40, ("#7E4F86", "#643E70"), 2.6, 2)]))
    # foreground calm hill
    p = []
    for i in range(41):
        t = i / 40
        p.append((W * t, 770 - 34 * math.sin(t * math.pi) - 12 * math.sin(t * math.pi * 3 + 1)))
    d = "M0,1350 L%s L1080,1350 Z" % pts(p)
    c.add('<path d="%s" fill="%s"/>' % (d, c.lg([(0, "#3E2352"), (0.4, "#2C173E"), (1, "#1C0E2A")])))
    c.add('<polyline points="%s" fill="none" stroke="#FFC9A8" stroke-opacity="0.5" stroke-width="3"/>' % pts(p))
    # tiny trees on the ridge
    for tx in (70, 120, 160, 900, 950, 1000):
        ty = 770 - 34 * math.sin(tx / W * math.pi) - 12 * math.sin(tx / W * math.pi * 3 + 1)
        c.add('<path d="M%s,%s l-14,34 h28 Z M%s,%s l-18,40 h36 Z" fill="#2C173E"/>' % (f(tx), f(ty - 60), f(tx), f(ty - 36)))
    c.add(bokeh(c, 18, (60, 820, 1020, 1300), ["#FFC9A8", "#E8A6B8"], 2, 5, (0.15, 0.4), blur=False))
    # gold hairline frame on the hill
    c.add('<path d="%s" fill="none" stroke="#F3C27A" stroke-width="2" opacity="0.8"/>' % rr(110, 786, 860, 480, 26))
    for (sx, sy) in ((110, 786), (970, 786), (110, 1266), (970, 1266)):
        c.add(sparkle(sx, sy, 16, "#F3C27A"))
    s = spec("E-good-morning-5", (150, 798, 930, 1260), "gold", "#FFF3E8", "#FFB88C", "dark", "classic")
    return c.svg(), s


# ================================================================ 6 dewy leaves, deep green
def card6():
    c = Card(306)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#1E5E43"), (0.5, "#15462F"), (1, "#0B2A1C")]))
    c.add(light_beams(c, 700, -40, 1100, 60, (-700, 1000), 7, "#EFFFD8", 0.22))
    c.add('<circle cx="930" cy="80" r="360" fill="%s"/>' % c.rg([(0, "#FFF6C8", 0.55), (1, "#FFF6C8", 0)]))
    c.add(bokeh(c, 40, (0, 0, 1080, 1350), ["#DDF5B8", "#FFF6C8", "#9CCC65"], 6, 40, (0.08, 0.3)))
    # fern-like narrow leaves behind
    for (x, y, L, rot) in ((-30, 620, 360, 60), (-20, 760, 300, 80), (1110, 700, 340, -70), (1100, 560, 280, -100), (300, -40, 300, 200), (560, -60, 220, 185)):
        c.add(leaf(c, x, y, L, rot, ("#5E9B3A", "#1D4A14"), wmul=0.22, drops=2))
    # leaf cluster top-left
    TL = ((-20, 330, 420, 70, ("#9CCC65", "#2E6B1E"), 0.1), (-30, 120, 380, 110, ("#B5D96F", "#3C7A22"), -0.1), (40, -30, 360, 150, ("#8BC34A", "#255E18"), 0.15),
          (220, -40, 300, 180, ("#AED581", "#33691E"), -0.1), (-40, 520, 300, 60, ("#7CB342", "#1F4F12"), 0.1))
    for (x, y, L, rot, cols, curl) in TL:
        c.add(leaf(c, x, y, L, rot, cols, wmul=0.3, drops=4, curl=curl))
    # leaf cluster bottom-right
    BR = ((1100, 1020, 420, -110, ("#9CCC65", "#2E6B1E"), 0.1), (1110, 1220, 400, -80, ("#B5D96F", "#3C7A22"), -0.12), (980, 1380, 380, -40, ("#8BC34A", "#255E18"), 0.1),
          (820, 1390, 280, -20, ("#AED581", "#33691E"), -0.1))
    for (x, y, L, rot, cols, curl) in BR:
        c.add(leaf(c, x, y, L, rot, cols, wmul=0.3, drops=4, curl=curl))
    # bottom-left: one big dewy leaf rising
    c.add(leaf(c, -40, 1400, 460, 38, ("#C5E1A5", "#3C7A22"), wmul=0.3, drops=0, curl=-0.08))
    for (dx, dy, r) in ((130, 1180, 18), (170, 1120, 10), (90, 1250, 12), (210, 1060, 14), (60, 1310, 8)):
        c.add(dew(dx, dy, r))
    for (x, y, r) in ((300, 150, 26), (190, 330, 22), (370, 70, 18), (870, 1130, 26), (760, 1250, 20), (250, 1020, 20)):
        c.add(blossom(c, x, y, r, ("#FFFFFF", "#FFF3C4")))
    c.add(flock(c, 760, 230, 4, 90, "#0E3322", 0.35, 0.6))
    # glass panel
    x, y, w, h = 110, 390, 860, 560
    d = rr(x, y, w, h, 36)
    c.add('<path d="%s" fill="#F6FFF0" opacity="0.93" filter="%s"/>' % (d, c.shadow(18, 28, 0.45)))
    c.add('<path d="%s" fill="none" stroke="#C5E1A5" stroke-width="3"/>' % d)
    c.add('<path d="%s" fill="none" stroke="#8BC34A" stroke-width="1.5" stroke-dasharray="2 8" stroke-linecap="round"/>' % rr(x + 16, y + 16, w - 32, h - 32, 26))
    # drops on the glass edge
    for (dx, dy, r) in ((x + w - 70, y + 6, 9), (x + w - 40, y + 24, 6), (x + 60, y + h - 4, 8)):
        c.add(dew(dx, dy, r))
    # one leaf tip over the panel corner
    c.add(leaf(c, 60, 470, 200, 55, ("#C5E1A5", "#558B2F"), drops=2, curl=0.1))
    s = spec("E-good-morning-6", (160, 440, 920, 900), "#1F6B30", "#1E2E22", "#7A9A2A", "light", "classic")
    return c.svg(), s


# ================================================================ 7 sparrows on a blossom branch holding a hanging sign
def card7():
    c = Card(307)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#BFE3F5"), (0.5, "#FDE3E6"), (1, "#FFE9D2")]))
    c.add(sun(c, 150, 1030, 90, ("#FFFDE7", "#FFE082", "#FFB74D"), "#FFD1A1", 4, 26, "#FFF3C4", 0.25))
    for (x, y, s) in ((820, 330, 0.8), (220, 700, 0.6), (930, 820, 0.7)):
        c.add(cloud(c, x, y, s, "#FFFFFF", "#F6C8D0", 0.85))
    # meadow
    c.add(hills(c, [(1120, 40, ("#C5E1A5", "#9CCC65"), 0.8, 2), (1210, 30, ("#9CCC65", "#689F38"), 2.2, 3)]))
    c.add(grass(c, 1350, 0, 1080, 220, ("#7CB342", "#558B2F"), 20, 70))
    for k in range(18):
        x = c.rnd.uniform(20, 1060)
        if 300 < x < 780:
            continue
        c.add(blossom(c, x, c.rnd.uniform(1230, 1320), c.rnd.uniform(8, 14), ("#FFFFFF", "#F8BBD0")))
    c.add(watermark_calm(c, "#446E22", 0.45))
    # branch across the top
    bx0, by0, bx1, by1 = -20, 200, 1100, 150
    c.add('<path d="M%d,%d Q540,%d %d,%d" stroke="%s" stroke-width="22" fill="none" stroke-linecap="round"/>' % (bx0, by0, 60, bx1, by1, c.lg(["#8D6E63", "#4E342E"], 0, 0, 0, 1)))

    def bpt(t):
        return ((1 - t) ** 2 * bx0 + 2 * (1 - t) * t * 540 + t * t * bx1, (1 - t) ** 2 * by0 + 2 * (1 - t) * t * 60 + t * t * by1)
    for k, t in enumerate((0.06, 0.16, 0.3, 0.44, 0.58, 0.7, 0.84, 0.95)):
        px, py = bpt(t)
        sgn = -1 if k % 2 else 1
        tx, ty = px + c.rnd.uniform(40, 80), py + sgn * c.rnd.uniform(50, 90)
        c.add('<path d="M%s,%s Q%s,%s %s,%s" stroke="#5D4037" stroke-width="8" fill="none" stroke-linecap="round"/>' % (f(px), f(py), f((px + tx) / 2), f(py), f(tx), f(ty)))
        c.add(leaf(c, tx, ty, c.rnd.uniform(60, 90), c.rnd.uniform(-60, 60) + (0 if sgn < 0 else 180), ("#AED581", "#558B2F"), drops=1))
        for j in range(3):
            c.add(blossom(c, px + c.rnd.uniform(-30, 30), py + c.rnd.uniform(-34, 24), c.rnd.uniform(14, 22), ("#FFFFFF", "#F48FB1")))
    # hanging ropes + sign
    x, y, w, h = 92, 360, 896, 610
    for rx in (x + 120, x + w - 120):
        t = (rx + 20) / 1120.0
        px, py = bpt(t)
        c.add('<path d="M%s,%s L%s,%s" stroke="#8D6E63" stroke-width="5"/>' % (f(px), f(py + 6), f(rx), f(y + 14)))
        c.add('<circle cx="%s" cy="%s" r="9" fill="#6D4C41"/>' % (f(rx), f(y + 14)))
    c.add('<rect x="%d" y="%d" width="%d" height="%d" rx="22" fill="%s" filter="%s"/>' % (x, y, w, h, c.lg(["#C8A27A", "#8D6444"], 0, 0, 1, 1), c.shadow(16, 22, 0.3, "#6A3A3A")))
    c.add('<rect x="%d" y="%d" width="%d" height="%d" rx="14" fill="%s"/>' % (x + 20, y + 20, w - 40, h - 40, c.lg(["#FFFDF8", "#FFF3EA"])))
    c.add('<rect x="%d" y="%d" width="%d" height="%d" rx="14" fill="none" stroke="#6D4C41" stroke-opacity="0.3" stroke-width="2"/>' % (x + 20, y + 20, w - 40, h - 40))
    for k in range(5):
        yy = y + 6 + k * (h - 12) / 4
        c.add('<path d="M%d,%s q8,4 0,10 M%d,%s q-8,4 0,10" stroke="#5D4037" stroke-opacity="0.35" stroke-width="2" fill="none"/>' % (x + 8, f(yy), x + w - 8, f(yy)))
    # sparrows on the branch
    p1 = bpt(0.36); p2 = bpt(0.64)
    c.add(sparrow(c, p1[0], p1[1] - 8, 1.25, False, singing=True))
    c.add(sparrow(c, p2[0], p2[1] - 8, 1.15, True, ("#BCAAA4", "#6D4C41")))
    # notes of song: small hearts-free sparkles
    for (sx, sy) in ((p1[0] + 130, p1[1] - 120), (p1[0] + 170, p1[1] - 80)):
        c.add(sparkle(sx, sy, 10, "#F48FB1"))
    s = spec("E-good-morning-7", (160, 420, 920, 910), "#B03A5B", "#3A2A30", "#6D4C41", "light", "script")
    return c.svg(), s


# ================================================================ 8 coffee mug, morning glory, torn paper
def card8():
    c = Card(308)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#5A3522"), (0.6, "#3E2417"), (1, "#26150C")]))
    c.add('<circle cx="760" cy="760" r="520" fill="%s"/>' % c.rg([(0, "#FFB870", 0.35), (1, "#FFB870", 0)]))
    c.add(bokeh(c, 26, (0, 600, 1080, 1100), ["#FFCC80", "#FFB74D", "#FFE0B2"], 6, 30, (0.1, 0.35)))
    # table
    ty = 1150
    c.add('<rect x="0" y="%d" width="1080" height="%d" fill="%s"/>' % (ty, H - ty, c.lg([(0, "#7A4A2C"), (1, "#2E1A0E")])))
    c.add('<rect x="0" y="%d" width="1080" height="6" fill="#A06A42"/>' % ty)
    # vine down the right side
    c.add(vine(c, [(1090, 560), (1030, 660), (1060, 780), (1000, 880), (1040, 990), (980, 1080), (1010, 1160)],
               ((1030, 700, 44), (990, 900, 50), (1050, 1040, 38)), ("#9575CD", "#4527A0")))
    c.add(vine(c, [(-10, 700), (50, 800), (20, 900), (70, 1000), (40, 1100)], ((40, 840, 36), (60, 1040, 30)), ("#9575CD", "#4527A0")))
    # mug hero
    c.add(mug(c, 520, 845, 1.22, ("#FFF4E0", "#D8C3A0"), "#4A2A16"))
    for (bx, by, rot) in ((230, 1200, 20), (270, 1225, -30), (205, 1240, 60), (800, 1210, -15), (840, 1236, 40), (770, 1250, 80), (330, 1260, -60)):
        c.add(coffee_bean(bx, by, 1.2, rot))
    # croissant-free: small saucer of sugar cubes
    c.add('<ellipse cx="860" cy="1150" rx="110" ry="26" fill="%s" filter="%s"/>' % (c.lg(["#FFFFFF", "#D8D0C4"]), c.shadow(6, 6, 0.35)))
    for (sx, sy) in ((830, 1122), (866, 1116), (884, 1134), (846, 1138)):
        c.add('<rect x="%d" y="%d" width="30" height="26" rx="4" fill="#FFFDF8" stroke="#E0D6C6"/>' % (sx - 15, sy - 13))
    c.add(watermark_calm(c, "#1E1008", 0.6))
    # torn paper panel
    x0, x1, y0, y1 = 70, 1010, 96, 650
    top = torn_edge(x0, x1, y0, 7, 26, c.rnd)
    bot = torn_edge(x0, x1, y1, 9, 22, c.rnd)
    d = "M%s L%s Z" % (pts(top), pts(list(reversed(bot))))
    c.add('<path d="%s" fill="%s" filter="%s"/>' % (d, c.lg(["#FFF9EE", "#F6EAD6"]), c.shadow(14, 20, 0.5)))
    cp = c.clip('<path d="%s"/>' % d)
    c.add('<g clip-path="%s"><rect x="0" y="0" width="1080" height="700" filter="url(#paper)" opacity="0.12"/></g>' % cp)
    c.add('<path d="M%s" fill="none" stroke="#E2CFAE" stroke-width="3"/>' % pts(bot))
    # washi tape
    for (tx, ty_, rot) in ((200, 96, -8), (880, 96, 7)):
        c.add('<rect x="-70" y="-18" width="140" height="36" fill="#B39DDB" opacity="0.8" transform="translate(%d,%d) rotate(%d)"/>' % (tx, ty_, rot))
    s = spec("E-good-morning-8", (140, 150, 940, 612), "#6B3410", "#2E1E14", "#7E57C2", "light", "classic")
    return c.svg(), s


# ================================================================ 9 golden sun holding the photo
def card9():
    c = Card(309)
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.lg([(0, "#FFF4D0"), (0.45, "#FFD98A"), (1, "#FFB25E")]))
    cx, cy, R = 540, 350, 190
    c.add(rays(cx, cy, 36, 1100, "#FFFFFF", 0.22, 0.5, 3))
    c.add('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (cx, cy, R * 2.6, c.rg([(0, "#FFF6C8", 0.9), (0.5, "#FFE08A", 0.3), (1, "#FFE08A", 0)])))
    # gold sun petals around the slot
    gp = c.lg(["#FFF1B8", "#F2B632", "#C9791A"], 0, 0, 0, 1)
    for k in range(24):
        a = k * 15
        L = R + (70 if k % 2 == 0 else 46)
        c.add('<path d="M-18,%s L0,%s L18,%s Z" fill="%s" transform="translate(%d,%d) rotate(%d)"/>' % (f(-R + 6), f(-L), f(-R + 6), gp, cx, cy, a))
    c.add('<circle cx="%d" cy="%d" r="%d" fill="%s" filter="%s"/>' % (cx, cy, R + 22, c.lg(["#FFF1B8", "#E9A92A", "#B8741A"]), c.shadow(10, 16, 0.3, "#8A4A00")))
    c.add('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#FFF6D8" stroke-width="3"/>' % (cx, cy, R + 12))
    c.add('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (cx, cy, R, c.rg([(0, "#FFFDF0"), (0.6, "#FFE9A6"), (1, "#FFC857")])))
    c.add('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#FFFFFF" stroke-opacity="0.6" stroke-width="6"/>' % (cx, cy, R - 30))
    c.add(flock(c, 170, 250, 4, 80, "#8A4A1A", 0.35, 0.6))
    c.add(flock(c, 920, 330, 4, 70, "#8A4A1A", 0.3, 0.55))
    c.add(cloud(c, 150, 610, 0.85, "#FFFFFF", "#FFD2A0"))
    c.add(cloud(c, 950, 590, 0.95, "#FFFFFF", "#FFD2A0"))
    # panel
    x, y, w, h = 96, 656, 888, 560
    c.add(panel(c, x, y, w, h, 40, ("#FFFFFF", "#FFF7E6"), "#E9A92A", sw=3))
    # morning flower clusters at the bottom corners
    for (bx, by, sgn) in ((40, 1360, 1), (1040, 1360, -1)):
        for k in range(4):
            c.add(leaf(c, bx, by, 130 + k * 22, sgn * (10 + k * 22), ("#9CCC65", "#33691E"), drops=1))
        c.add(sunflower(c, bx + sgn * 40, by - 130, 72, 0))
        c.add(blossom(c, bx + sgn * 130, by - 50, 26, ("#FFFFFF", "#FFCC80")))
        c.add(blossom(c, bx + sgn * 100, by - 170, 22, ("#FFFFFF", "#FFCC80")))
    photo = {"shape": "circle", "x": cx, "y": cy, "cx": cx, "cy": cy, "r": R}
    s = spec("E-good-morning-9", (150, 706, 930, 1166), "#B34700", "#3A2410", "#C77700", "light", "script", photo=photo)
    return c.svg(), s


# ================================================================ 10 flat-lay: tea from above, note card
def card10():
    c = Card(310)
    # light wood planks from above
    c.add('<rect width="1080" height="1350" fill="#EBD9C0"/>')
    for k in range(7):
        x = k * 160
        c.add('<rect x="%d" y="0" width="160" height="1350" fill="%s"/>' % (x, ["#EEDCC3", "#E6D1B4", "#F0E0C9", "#E8D5BA"][k % 4]))
        c.add('<path d="M%d,0 V1350" stroke="#C9AE8A" stroke-width="2"/>' % x)
        for j in range(6):
            gx = x + c.rnd.uniform(20, 140)
            c.add('<path d="M%s,%s q%s,%s 0,%s" stroke="#C9AE8A" stroke-opacity="0.35" stroke-width="1.5" fill="none"/>' % (
                f(gx), f(c.rnd.uniform(0, 1200)), f(c.rnd.uniform(-8, 8)), f(c.rnd.uniform(60, 120)), f(c.rnd.uniform(140, 260))))
    c.add('<rect width="1080" height="1350" fill="%s"/>' % c.rg([(0, "#FFF8E8", 0.5), (1, "#FFF8E8", 0)], 0.8, 0.1, 0.8))
    # cup from above (top-right)
    ux, uy = 880, 200
    c.add('<circle cx="%d" cy="%d" r="210" fill="#000" opacity="0.15" filter="%s"/>' % (ux + 14, uy + 20, c.blur(14)))
    c.add('<circle cx="%d" cy="%d" r="206" fill="%s"/>' % (ux, uy, c.rg([(0, "#FFFFFF"), (0.8, "#F4F1EC"), (1, "#DCD4C8")])))
    c.add('<circle cx="%d" cy="%d" r="190" fill="none" stroke="#2E6D8E" stroke-width="5"/>' % (ux, uy))
    c.add('<circle cx="%d" cy="%d" r="180" fill="none" stroke="#2E6D8E" stroke-width="1.5" stroke-dasharray="4 6"/>' % (ux, uy))
    c.add('<path d="M%d,%d c-60,40 -80,90 -60,120" stroke="#DCD4C8" stroke-width="30" fill="none" stroke-linecap="round"/>' % (ux - 110, uy + 90))
    c.add('<path d="M%d,%d c-60,40 -80,90 -60,120" stroke="#FFFFFF" stroke-width="20" fill="none" stroke-linecap="round"/>' % (ux - 110, uy + 90))
    c.add('<circle cx="%d" cy="%d" r="132" fill="%s" filter="%s"/>' % (ux, uy, c.rg([(0, "#FFFFFF"), (1, "#E4DED4")]), c.shadow(4, 6, 0.25)))
    c.add('<circle cx="%d" cy="%d" r="112" fill="%s"/>' % (ux, uy, c.rg([(0, "#D9955A"), (0.7, "#B06A34"), (1, "#7A3F16")])))
    c.add('<ellipse cx="%d" cy="%d" rx="40" ry="14" fill="#FFFFFF" opacity="0.3" transform="rotate(-30 %d %d)"/>' % (ux - 40, uy - 50, ux - 40, uy - 50))
    c.add('<path d="M%d,%d c30,-30 60,10 30,40 c-30,30 -70,-10 -40,-50" stroke="#FFE7C4" stroke-opacity="0.5" stroke-width="4" fill="none"/>' % (ux - 10, uy))
    # spoon
    c.add('<g transform="translate(%d,%d) rotate(35)"><rect x="-6" y="0" width="12" height="160" rx="6" fill="%s"/><ellipse cx="0" cy="-10" rx="26" ry="36" fill="%s"/></g>' % (
        ux - 250, uy + 210, c.lg(["#F5F5F5", "#9E9E9E"], 0, 0, 1, 0), c.lg(["#FFFFFF", "#A8A8A8"], 0, 0, 1, 1)))
    # sunflower + leaves top-left
    for (lx, ly, L, rot) in ((40, 330, 260, 40), (200, -10, 240, 160), (-20, 120, 220, 70)):
        c.add(leaf(c, lx, ly, L, rot, ("#9CCC65", "#2E6B1E"), drops=2))
    c.add(sunflower(c, 150, 160, 120, 20))
    c.add(blossom(c, 330, 90, 30, ("#FFFFFF", "#FFE0B2")))
    c.add(blossom(c, 60, 400, 24, ("#FFFFFF", "#FFE0B2")))
    # bottom corners
    for (lx, ly, L, rot) in ((1100, 1150, 280, -120), (960, 1380, 260, -30), (-20, 1240, 240, 60), (140, 1380, 200, 20)):
        c.add(leaf(c, lx, ly, L, rot, ("#AED581", "#33691E"), drops=2))
    c.add(sunflower(c, 990, 1230, 84, -10))
    c.add(blossom(c, 90, 1170, 30, ("#FFFFFF", "#FFE0B2")))
    for k in range(7):
        px, py = c.rnd.uniform(200, 320), c.rnd.uniform(1150, 1260)
        c.add('<ellipse cx="%s" cy="%s" rx="20" ry="6" fill="#F9C23C" transform="rotate(%s %s %s)"/>' % (f(px), f(py), f(c.rnd.uniform(0, 180)), f(px), f(py)))
    c.add(watermark_calm(c, "#EBD9C0", 0.9))
    # note card
    x, y, w, h = 104, 450, 872, 640
    c.add('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="#FFFFFF" filter="%s" transform="rotate(-1.2 540 770)"/>' % (x + 6, y + 6, w - 12, h - 12, c.shadow(6, 10, 0.2)))
    c.add('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" filter="%s"/>' % (x, y, w, h, c.lg(["#FFFFFF", "#FFFBF3"]), c.shadow(12, 18, 0.28, "#6A4A2A")))
    c.add('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#E9C77B" stroke-width="2"/>' % (x + 22, y + 22, w - 44, h - 44))
    c.add('<rect x="-90" y="-20" width="180" height="40" fill="%s" opacity="0.85" transform="translate(540,%d) rotate(-3)"/>' % (
        c.pattern(20, 20, '<rect width="20" height="20" fill="#F6C35C"/><rect width="10" height="20" fill="#FFE29A"/>', "rotate(45)"), y))
    s = spec("E-good-morning-10", (160, 500, 920, 1040), "#A04A00", "#33291E", "#2E6D8E", "light", "script")
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
