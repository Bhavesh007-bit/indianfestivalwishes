"""engagement (wishes): interlocked rings, heart floral wreath, lovebirds, bouquet, couple under string lights.
Romantic, pastel/jewel, big hero art; photo slots never circles."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_d import *
from render import render_cards

CAT = "engagement"
SPECS = []


def S(n, zone, title, text, accent, **kw):
    SPECS.append(spec(CAT, n, zone, title, text, accent, **kw))


RED = ("#8E1027", "#C2264B", "#F07A92")
PINK = ("#D05A7A", "#F08AA2", "#FFD1DC")
BLUSH = ("#E07F98", "#F6BFCB", "#FFEFF2")
WHITE = ("#D9D2C3", "#F4EFE6", "#FFFFFF")
PEACH = ("#E8A07A", "#F6C8A8", "#FFF0E4")


def glass(x, y, w, h, dark=True, r=34, stroke="#F2CF74"):
    fill = "#1A0712" if dark else "#FFFFFF"
    out = '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" opacity="%s" filter="url(#shb)"/>' % (x, y, w, h, r, fill, .55 if dark else .86)
    out += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="%s" stroke-width="2" opacity=".75"/>' % (x + 12, y + 12, w - 24, h - 24, r - 10, stroke)
    return out


# ------------------------------------------------------------------ 1 wine: giant interlocked rings with sparkle
def card1():
    b = bg_grad(["#3A0718", "#5E0E2A", "#2A0512"])
    b += glow_spot(540, 400, 520, "#FF9FB4", .25)
    b += light_rays(540, 380, 26, 900, "#FFE7C4", .12, 360, -180, .035)
    b += bokeh(1, 50, (0, 0, W, H), ["#F7B7C6", "#FFE3A0", "#FFFFFF"], 6, 40, (.12, .45))
    b += linked_rings(540, 420, 200)
    b += sparkles(11, 26, (140, 60, 940, 720), "#FFF6DA", 8, 24)
    b += sparkle(470, 140, 40, "#FFFFFF") + sparkle(700, 330, 30, "#FFFFFF")
    # rose petals drifting
    b += petals(5, 18, (40, 60, 1040, 760), (14, 24), ("#E0506E", "#8E1027"), avoid=[(200, 120, 880, 700)])
    b += glass(110, 770, 860, 520)
    S(1, [160, 810, 920, 1270], "gold", "#FCEFF3", "#F2CF74", tone="dark", tfont="script")
    return page(b)


# ------------------------------------------------------------------ 2 blush: heart-shaped floral wreath around a heart photo
def card2():
    b = bg_grad(["#FFF3F5", "#FBDDE4"])
    b += pat_rect(dots_pattern("d2", 38, 2.4, "#F2A9BA", .45), "d2")
    b += glow_spot(540, 330, 420, "#FFFFFF", .8)
    ph = dict(shape="heart", x=300, y=90, w=480, h=470)
    b += slot_placeholder("heart", ph["x"], ph["y"], ph["w"], ph["h"], "#FFF1F4", "#F2CDD6")
    hp = heart_points(540, 90 - 26, 480 + 64, 470 + 52, 70)
    gid, g = lin(ROSEGOLD, 0, 0, 1, 1)
    b += defs(g) + '<path d="%sZ" fill="none" stroke="url(#%s)" stroke-width="6"/>' % (pts_d(heart_points(540, 90 - 10, 480 + 20, 470 + 18, 120)), gid)
    fl = [lambda x, y, r: rose(x, y, 32, RED, r), lambda x, y, r: peony(x, y, 36, BLUSH, r),
          lambda x, y, r: rose(x, y, 28, PINK, r), lambda x, y, r: blossom(x, y, 20, "#FFFFFF", "#F2B7C4", 5, r)]
    b += floral_along(hp, 22, fl, every=2, leaves=("#8DB38A", "#3F6B45"), leaf_len=52)
    b += gypso(3, 330, 200, 90, 18) + gypso(4, 750, 200, 90, 18)
    # lovely bow at the heart dip
    b += ribbon_bow(540, 205, 70, ("#F29BB0", "#C8577A"))
    b += petals(6, 16, (30, 40, 1050, 700), (10, 18), ("#F08AA2", "#C2264B"), avoid=[(230, 40, 850, 660)])
    b += fancy_panel(120, 740, 840, 540, "#FFFFFF", ROSEGOLD, r=40, corners=False, bw=3)
    S(2, [160, 776, 920, 1250], "#B0284E", "#4A2A34", "#C0607A", tfont="script", photo=ph)
    return page(b)


# ------------------------------------------------------------------ 3 sage: arch photo under a climbing-rose arbour
def card3():
    b = bg_grad(["#EEF3EA", "#DCE7D6"])
    b += grain()
    R = random.Random(3)
    for _ in range(30):
        b += blossom(R.uniform(0, W), R.uniform(0, H), R.uniform(8, 14), "#FFFFFF", "#F2C7D0", 5, R.uniform(0, 90), op=.5)
    ph = dict(shape="arch", x=300, y=150, w=480, h=510)
    b += frame_ring("arch", ph["x"], ph["y"], ph["w"], ph["h"], GOLD, 9, 0)
    b += '<path d="%s" fill="none" stroke="#B89A5A" stroke-width="1.5"/>' % shape_grow("arch", ph["x"], ph["y"], ph["w"], ph["h"], 22)
    b += slot_placeholder("arch", ph["x"], ph["y"], ph["w"], ph["h"], "#F4F7F0", "#D5E0D0")
    # climbing roses: vines up both sides and over the arch top
    for side in (-1, 1):
        pts = []
        for i in range(40):
            t = i / 39
            y = 670 - t * 530
            x = 540 + side * (268 + 14 * math.sin(t * 9))
            if t > .6:
                a = (t - .6) / .4
                x = 540 + side * (268 * (1 - a * .95) + 14 * math.sin(t * 9))
                y = 670 - .6 * 530 - a * (670 - .6 * 530 - 118) * math.sin(a * math.pi / 2)
            pts.append((x, y))
        b += '<path d="%s" stroke="#5E7A4A" stroke-width="5" fill="none"/>' % pts_d(pts)
        fl = [lambda x, y, r: rose(x, y, 26, RED, r), lambda x, y, r: rose(x, y, 22, PINK, r),
              lambda x, y, r: rose_side(x, y, 16, RED, r), lambda x, y, r: blossom(x, y, 14, "#FFFFFF", "#F2B7C4", 5, r)]
        b += floral_along(pts[::2], 30 + side, fl, every=2, leaves=("#7FA07A", "#3F6B45"), leaf_len=40)
    b += rose(540, 118, 38, RED) + rose(490, 128, 26, PINK) + rose(590, 128, 26, PINK)
    # ground cluster at base
    for side in (-1, 1):
        b += peony(540 + side * 290, 672, 46, BLUSH) + rose(540 + side * 240, 690, 30, RED) + eucalyptus(540 + side * 300, 672, 140, 90 - side * 70)
    b += '<path d="%s" fill="#FFFFFF" filter="url(#shb)"/>' % scallop_path_rect(100, 752, 880, 530, 20)
    b += '<rect x="128" y="780" width="824" height="474" rx="6" fill="none" stroke="#9DB89A" stroke-width="2" stroke-dasharray="2 8" stroke-linecap="round"/>'
    S(3, [160, 782, 920, 1262], "#8E1F3A", "#2F3A2D", "#6E8A5A", tfont="script", photo=ph)
    return page(b)


# ------------------------------------------------------------------ 4 dusk: couple silhouette under string lights
def card4():
    b = bg_grad(["#1B1440", "#4A2A6E", "#C0607A", "#F4A578"])
    b += glow_spot(540, 1050, 520, "#FFD1A0", .45)
    b += sparkles(4, 50, (0, 0, W, 700), "#FFFFFF", 2, 6, (.4, 1))
    # string lights: two drooping lines across the top
    b += string_lights(catenary(-20, 40, 1100, 60, 150, 50), 48)
    b += string_lights(catenary(-20, 150, 1100, 120, 110, 50), 52, "#FFD0E0", "#FF8FB0")
    # rolling hill + trees
    b += '<path d="M0,1130 C220,1060 420,1080 560,1100 C760,1130 920,1070 1080,1090 L1080,1350 L0,1350Z" fill="#1E1230"/>'
    b += '<path d="M0,1190 C260,1150 600,1180 1080,1150 L1080,1350 L0,1350Z" fill="#140A22"/>'
    # fireflies
    b += bokeh(8, 40, (0, 700, W, 1140), ["#FFE7A0"], 2, 5, (.5, 1), blur=False)
    b += couple_silhouette(560, 1128, 120, "#170A26")
    # a lamp post with lights draped down to the couple
    b += '<rect x="880" y="820" width="10" height="300" fill="#170A26"/><circle cx="885" cy="815" r="16" fill="#FFE7A0"/>' + glow_spot(885, 815, 90, "#FFE7A0", .7)
    b += string_lights(catenary(885, 830, 1100, 900, 60, 12), 40)
    b += string_lights(catenary(-20, 860, 200, 860, 90, 12), 40)
    b += glass(110, 250, 860, 560, dark=True, stroke="#FFD1A0")
    S(4, [160, 300, 920, 770], "gold", "#FFF1EC", "#FFC7A0", tone="dark", tfont="script")
    return page(b)


# ------------------------------------------------------------------ 5 lavender: bouquet beside a rounded photo
def card5():
    b = bg_grad(["#F4EEFA", "#E4D8F2"])
    b += defs(marble("mb5", vein="#B9A2D8", op=.3)) + '<rect width="1080" height="1350" fill="#fff" filter="url(#mb5)"/>'
    ph = dict(shape="rounded", x=90, y=90, w=540, h=560)
    b += '<rect x="68" y="68" width="584" height="604" rx="40" fill="#FFFFFF" filter="url(#sh)"/>'
    gid, g = lin(ROSEGOLD, 0, 0, 1, 1)
    b += defs(g) + '<rect x="78" y="78" width="564" height="584" rx="34" fill="none" stroke="url(#%s)" stroke-width="3"/>' % gid
    b += slot_placeholder("rounded", ph["x"], ph["y"], ph["w"], ph["h"], "#F7F2FC", "#DDD0EC")
    b += bouquet(850, 690, 125, [("#7A3F9A", "#A974C8", "#E3CBF2"), BLUSH, ("#B8264A", "#E0506E", "#F8A5B5")], bow=("#C9A0DC", "#8E5CA8"))
    b += petals(7, 12, (640, 60, 1060, 720), (10, 16), ("#C9A0DC", "#8E5CA8"), avoid=[(680, 150, 1030, 700)])
    b += fancy_panel(110, 760, 860, 520, "#FFFFFF", ROSEGOLD, r=28, corners=False, bw=2)
    S(5, [160, 790, 920, 1255], "#6A2E8A", "#3A2A48", "#A0508A", tfont="script", photo=ph)
    return page(b)


# ------------------------------------------------------------------ 6 emerald: solitaire resting on a big red rose
def card6():
    b = bg_grad(["#07261E", "#0F3F31", "#062019"])
    b += pat_rect(damask_pattern("dm6", 110, "#E9C46A", .07), "dm6")
    b += glow_spot(540, 400, 460, "#FFD98A", .3)
    for a in (150, 190, 230, 310, 350, 30, 120, 60):
        b += leaf(540, 470, 250, a, "#3F7A4A", "#123A22")
    b += rose(540, 440, 230, ("#5E0A1C", "#B0142E", "#F2667E"))
    b += upright_ring(540, 250, 110, GOLD, -8, True, 1.1)
    b += sparkles(6, 22, (180, 60, 900, 720), "#FFF6DA", 8, 22)
    b += petals(9, 16, (40, 60, 1040, 760), (16, 28), ("#C2264B", "#6E0B1C"), avoid=[(260, 120, 820, 740)])
    b += fancy_panel(100, 770, 880, 515, "#FFF9EF", GOLD, r=30, corner_size=80)
    S(6, [160, 800, 920, 1262], "#8E1027", "#23302A", "#9A6A12", tfont="deco")
    return page(b)


# ------------------------------------------------------------------ 7 champagne: string-light canopy over a rect photo
def card7():
    b = bg_grad(["#FBF4E6", "#F1E3C8"])
    b += grain()
    b += bokeh(7, 40, (0, 0, W, H), ["#F4D58A", "#FFFFFF", "#F1C4A0"], 8, 40, (.2, .55))
    for k in range(5):
        b += string_lights(catenary(-20, 20 + k * 12, 1100, 20 + k * 12, 70 + k * 40, 50), 50 + k * 4, "#FFF1C4", "#FFC857", "#8C6A3A", 6)
    ph = dict(shape="rect", x=170, y=280, w=740, h=440)
    gid, g = lin(GOLD, 0, 0, 1, 1)
    b += '<rect x="146" y="256" width="788" height="488" fill="#2A1E14" filter="url(#shb)"/>'
    b += defs(g) + '<rect x="152" y="262" width="776" height="476" fill="none" stroke="url(#%s)" stroke-width="8"/>' % gid
    b += slot_placeholder("rect", ph["x"], ph["y"], ph["w"], ph["h"], "#F6EFE2", "#E0D2B8")
    # white roses + eucalyptus in the corners of the frame
    for cx, cy, a0 in ((152, 738, -60), (928, 262, 120)):
        for k in range(5):
            b += eucalyptus(cx, cy, 150, a0 + k * 30, n=7)
        b += rose(cx, cy, 44, WHITE) + rose(cx + (50 if cx < 500 else -50), cy + (-10 if cx < 500 else 14), 30, PEACH) + gypso(cx, cx, cy, 70, 16)
    b += linked_rings(540, 250, 42, glow=False)[0:0]
    b += fancy_panel(110, 780, 860, 505, "#1E2A44", GOLD, r=10, corners=True, corner_size=60, bw=3, grain_=False)
    S(7, [160, 800, 920, 1264], "gold", "#F6EEDC", "#F2CF74", tone="dark", tfont="script", photo=ph)
    return page(b)


# ------------------------------------------------------------------ 8 mint & coral: lovebirds perched on an oval photo
def card8():
    b = bg_grad(["#E8F6F0", "#CDEBDF"])
    b += pat_rect(dots_pattern("d8", 46, 2, "#8CCBB0", .45), "d8")
    ph = dict(shape="oval", x=250, y=230, w=580, h=440)
    b += frame_ring("oval", ph["x"], ph["y"], ph["w"], ph["h"], ROSEGOLD, 10, 0)
    b += slot_placeholder("oval", ph["x"], ph["y"], ph["w"], ph["h"], "#F5FBF8", "#D3E9DE")
    # blossoming branch across the top of the oval
    br = qbez((120, 250), (540, 160), (960, 250), 30)
    b += branch(br, 12)
    b += branch(qbez((300, 200), (330, 140), (380, 120), 10), 5) + branch(qbez((760, 200), (740, 140), (700, 116), 10), 5)
    R = random.Random(8)
    for (x, y) in br[::2] + [(380, 120), (700, 116), (340, 150), (730, 150)]:
        b += leaf(x, y, 34, R.uniform(0, 360), "#7FB08A", "#2F6B4A", vein=False)
        b += blossom(x + R.uniform(-14, 14), y + R.uniform(-14, 8), R.uniform(14, 22), "#FFD1C4", "#F08A70", 5, R.uniform(0, 70))
    b += lovebird(476, 196, 95, False, ("#F79A86", "#E0604C", "#FFD6CC"), ("#EE7A64", "#B8442F"))
    b += lovebird(604, 196, 95, True, ("#7CCFB0", "#3E9E7C", "#D2F2E4"), ("#58B894", "#2E7A5E"))
    b += '<path d="M540,92 C528,74 506,82 516,100 L540,120 L564,100 C574,82 552,74 540,92Z" fill="#E0604C"/>'
    # flowers at the bottom of the oval
    for dx, fn in ((-120, lambda x, y: peony(x, y, 40, ("#F08A70", "#FFC4B4", "#FFF0EA"))), (0, lambda x, y: rose(x, y, 36, ("#B8442F", "#EE7A64", "#FFC4B4"))),
                   (120, lambda x, y: peony(x, y, 40, ("#F08A70", "#FFC4B4", "#FFF0EA")))):
        b += leaf(540 + dx, 682, 60, 200) + leaf(540 + dx, 682, 60, 340)
        b += fn(540 + dx, 682)
    b += '<path d="M100,1282 L100,800 Q540,700 980,800 L980,1282 Z" fill="#FFFFFF" filter="url(#shb)"/>'
    b += '<path d="M118,1264 L118,814 Q540,722 962,814 L962,1264 Z" fill="none" stroke="#E0907C" stroke-width="2"/>'
    S(8, [160, 800, 920, 1262], "#C24A34", "#274A3C", "#2E8B6E", tfont="script", photo=ph)
    return page(b)


# ------------------------------------------------------------------ 9 white satin: rose-petal heart cradling the rings
def card9():
    b = bg_grad(["#FFFFFF", "#F4EDEA"])
    b += defs(marble("mb9", vein="#D8C8C0", op=.3)) + '<rect width="1080" height="1350" fill="#fff" filter="url(#mb9)"/>'
    # heart outlined by many rose petals
    hp = heart_points(540, 60, 600, 600, 140)
    R = random.Random(9)
    for (x, y) in hp:
        for k in range(2):
            b += rose_petal(x + R.uniform(-26, 26), y + R.uniform(-26, 26), R.uniform(18, 30), R.uniform(0, 360),
                            R.choice([("#D4203E", "#8E1027"), ("#E0506E", "#B0142E"), ("#F08AA2", "#C2264B")]))
    b += linked_rings(540, 360, 120, metals=(GOLD, SILVER))
    b += sparkles(19, 14, (360, 180, 720, 520), "#FFFFFF", 8, 18)
    b += petals(10, 16, (20, 20, 1060, 720), (12, 22), ("#E0506E", "#8E1027"), avoid=[(200, 30, 880, 740)])
    b += fancy_panel(110, 752, 860, 530, "#FFFFFF", GOLD, r=20, corners=True, corner_size=60, bw=2, shadow="sh")
    S(9, [160, 782, 920, 1262], "#A0142E", "#3A2A2A", "#A0701A", tfont="deco")
    return page(b)


# ------------------------------------------------------------------ 10 red & pink: pill photo, paper-heart garlands
def card10():
    b = bg_grad(["#C2264B", "#8E1027"])
    b += pat_rect(dots_pattern("d10", 40, 2, "#FFB3C4", .35), "d10")
    b += glow_spot(540, 420, 480, "#FF8FB0", .35)

    def heart_item(x, y, s, col):
        return '<path d="M%s,%s c-%s,-%s -%s,-%s 0,-%s c%s,-%s %s,%s 0,%s Z" fill="%s" filter="url(#shs)"/>' % (
            f(x), f(y + s * .5), f(s * .9), f(s * .7), f(s * .5), f(s * 1.5), f(s * .9), f(s * .5), f(s * 1.5), f(s * .4), f(s * .7), f(s * .9), col)
    cols = ["#FFFFFF", "#FFD1DC", "#F9C04A", "#FF8FB0"]
    for k, (y0, sag) in enumerate(((10, 70), (60, 90))):
        pts = catenary(-20, y0, 1100, y0, sag, 60)
        b += '<path d="%s" stroke="#FFE3EA" stroke-width="1.5" fill="none"/>' % pts_d(pts)
        idx = [0]

        def it(x, y, a, k=k):
            idx[0] += 1
            return heart_item(x, y + 16, 16, cols[(idx[0] + k) % 4])
        b += strand(pts, it, step=62 + k * 8)
    ph = dict(shape="pill", x=310, y=150, w=460, h=540)
    b += frame_ring("pill", ph["x"], ph["y"], ph["w"], ph["h"], GOLD, 12, 0)
    b += '<path d="%s" fill="none" stroke="#FFD1DC" stroke-width="2" stroke-dasharray="1 10" stroke-linecap="round"/>' % shape_grow("pill", ph["x"], ph["y"], ph["w"], ph["h"], 30)
    b += slot_placeholder("pill", ph["x"], ph["y"], ph["w"], ph["h"], "#FFF1F4", "#F2CDD6")
    # sparkling ring pair beside the photo + roses at its foot
    b += linked_rings(170, 520, 70, glow=True)
    b += linked_rings(910, 380, 56, metals=(ROSEGOLD, GOLD))
    for dx in (-200, -130, 130, 200):
        b += leaf(540 + dx, 700, 70, 200 if dx < 0 else -20) + leaf(540 + dx, 700, 60, 250 if dx < 0 else -70)
    b += rose(540 - 180, 700, 40, WHITE) + rose(540 - 120, 720, 30, PINK) + rose(540 + 180, 700, 40, WHITE) + rose(540 + 120, 720, 30, PINK)
    b += sparkles(12, 20, (40, 140, 1040, 740), "#FFFFFF", 5, 14)
    b += '<path d="M60,770 L1020,770 L980,1027 L1020,1285 L60,1285 L100,1027 Z" fill="#FFF6F8" filter="url(#shb)"/>'
    b += '<path d="M86,786 L994,786 L958,1027 L994,1269 L86,1269 L122,1027 Z" fill="none" stroke="#D9A94A" stroke-width="3"/>'
    S(10, [160, 798, 920, 1262], "#A0142E", "#4A2030", "#B0284E", tfont="script", photo=ph)
    return page(b)


if __name__ == "__main__":
    cards = {}
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7, card8, card9, card10], 1):
        cards["E-%s-%d" % (CAT, i)] = fn()
    write_specs(CAT, SPECS)
    only = sys.argv[1:]
    if only:
        cards = {k: v for k, v in cards.items() if k.split("-")[-1] in only}
    render_cards(cards)
