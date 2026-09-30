"""inv-baby-shower (godh bharai invitation): expecting mother, bangles, fruit basket & coconut lap ritual,
flower jewellery, baby clothes line, flower swing, soft clouds, pastel florals. No cradle."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_d import *
from render import render_cards

CAT = "inv-baby-shower"
SPECS = []


def S(n, zone, title, text, accent, **kw):
    SPECS.append(spec(CAT, n, zone, title, text, accent, **kw))


PINK = ("#D96C8C", "#F4A8BE", "#FFE3EC")
PEACH = ("#E8906A", "#F6C3A6", "#FFEEE2")
LILAC = ("#9B6FC0", "#C9A8E2", "#F1E6FA")
YEL = ("#E0A72E", "#F6D36B", "#FFF3C4")


def pastel_cluster(cx, cy, seed, k=1.0, pals=(PINK, PEACH, LILAC)):
    R = random.Random(seed)
    out = ""
    for _ in range(7):
        out += leaf(cx, cy, R.uniform(60, 95) * k, R.uniform(0, 360), "#A8CBA0", "#5E8F5A")
    out += eucalyptus(cx, cy, 120 * k, R.uniform(0, 360)) + eucalyptus(cx, cy, 110 * k, R.uniform(0, 360))
    for i in range(5):
        a = R.uniform(0, math.tau)
        d = R.uniform(10, 50) * k
        p = pals[i % len(pals)]
        if i % 2:
            out += peony(cx + math.cos(a) * d, cy + math.sin(a) * d, R.uniform(26, 36) * k, p)
        else:
            out += rose(cx + math.cos(a) * d, cy + math.sin(a) * d, R.uniform(22, 30) * k, p, rot=R.uniform(0, 90))
    for _ in range(5):
        out += blossom(cx + R.uniform(-70, 70) * k, cy + R.uniform(-60, 60) * k, 12 * k, "#FFFFFF", "#F2B7C4", 5, R.uniform(0, 60))
    return out


# ------------------------------------------------------------------ 1 lilac: mother silhouette + florals at the bottom, cloud panel top
def card1():
    b = bg_grad(["#F6F0FB", "#E7DAF3", "#D9C6EC"])
    b += bokeh(1, 30, (0, 0, W, H), ["#FFFFFF", "#F4C6D6"], 8, 30, (.25, .6))
    b += cloud(200, 1180, 260, "#FFFFFF", .8, "#E4D6F0") + cloud(900, 1210, 240, "#FFFFFF", .85, "#E4D6F0")
    b += fancy_panel(90, 44, 900, 766, "#FFFFFF", ROSEGOLD, r=40, corners=False, bw=2, op=.95)
    b += '<rect x="112" y="66" width="856" height="722" rx="30" fill="none" stroke="#C9A8E2" stroke-width="2" stroke-dasharray="2 9" stroke-linecap="round"/>'
    b += glow_spot(300, 1050, 300, "#FFFFFF", .8)
    b += pastel_cluster(90, 1270, 3, 1.1) + pastel_cluster(430, 1250, 4, .9)
    b += mother(300, 1268, 106, "#6B3E8C", "#EBD9F7", "#F2CF74")
    # bangles & fruit on the right
    b += thal(800, 1170, 210, ry=64)
    b += coconut(730, 1080, 60, wrap=("#3FA26B", "#F2CF74"), rot=-10)
    b += apple(830, 1100, 38) + pomegranate(900, 1120, 40) + banana_bunch(800, 1140, 80, -20) + bangle_stack(880, 1190, 44, ["#C0223B", "#3FA26B", "#F2B544"], 9, 8)
    b += pastel_cluster(1030, 1000, 5, .9)
    S(1, [150, 76, 930, 778], "#6B3E8C", "#3A2A48", "#B0507A", tfont="script")
    return page(b)


# ------------------------------------------------------------------ 2 mint & pink: bangle stand hero
def card2():
    b = bg_grad(["#E6F6EF", "#CDEBDD"])
    b += pat_rect(dots_pattern("d2", 42, 2, "#9CD1B8", .5), "d2")
    b += glow_spot(540, 280, 380, "#FFFFFF", .85)
    # two bangle stands (gold pole + stacked glass bangles)
    for cx, cols in ((420, ["#C0223B", "#F2B544", "#2E8B57", "#E86C8C", "#C0223B", "#F2B544", "#7B3FA0", "#E86C8C", "#2E8B57", "#C0223B"]),
                     (660, ["#E86C8C", "#F9D776", "#8FD1B8", "#D96C8C", "#F9D776", "#8FD1B8", "#E86C8C", "#F9D776"])):
        gid, g = lin(GOLD, 0, 0, 1, 0)
        top = 110 if cx == 420 else 160
        b += defs(g) + '<rect x="%d" y="%d" width="12" height="%d" fill="url(#%s)"/>' % (cx - 6, top, 470 - top, gid)
        b += '<ellipse cx="%d" cy="470" rx="90" ry="22" fill="url(#%s)" filter="url(#sh)"/>' % (cx, gid)
        b += '<circle cx="%d" cy="%d" r="14" fill="url(#%s)"/>' % (cx, top, gid)
        b += bangle_stack(cx, 450, 70 if cx == 420 else 62, cols, 13, 15)
    # loose bangles + flowers on the ground
    for i, (x, c) in enumerate(((220, "#C0223B"), (280, "#F2B544"), (820, "#2E8B57"), (880, "#E86C8C"))):
        b += bangle(x, 470 - (i % 2) * 8, 52, 16, c, 10)
    b += pastel_cluster(150, 400, 21, .8) + pastel_cluster(940, 390, 22, .8)
    b += sparkles(2, 14, (200, 90, 900, 450), "#FFFFFF", 6, 14)
    # arched-top pink panel
    b += '<path d="M90,1290 L90,690 Q90,540 540,540 Q990,540 990,690 L990,1290 Z" fill="#FFF7FA" filter="url(#shb)"/>'
    b += '<path d="M112,1270 L112,694 Q112,562 540,562 Q968,562 968,694 L968,1270 Z" fill="none" stroke="#E6A2B8" stroke-width="2.5"/>'
    b += grain(90, 540, 900, 750)
    S(2, [150, 560, 930, 1264], "#B03A62", "#3A2A30", "#2E8B6E", tfont="deco")
    return page(b)


# ------------------------------------------------------------------ 3 peach & green: fruit basket + coconut lap ritual at bottom
def card3():
    b = bg_grad(["#FFF3EA", "#FBE0CF"])
    b += grain()
    # green saree drape across the bottom (the lap / godh)
    gid, g = lin(["#5FBF8C", "#2E8B57", "#1F6B42"], 0, 0, 0, 1)
    b += defs(g) + '<path d="M0,1080 C250,1030 420,1130 560,1110 C760,1080 880,1030 1080,1070 L1080,1350 L0,1350Z" fill="url(#%s)"/>' % gid
    gb, gg = lin(GOLD, 0, 0, 1, 0)
    b += defs(gg) + '<path d="M0,1080 C250,1030 420,1130 560,1110 C760,1080 880,1030 1080,1070" stroke="url(#%s)" stroke-width="20" fill="none"/>' % gb
    for k in range(5):
        b += '<path d="M%d,1040 C%d,1120 %d,1200 %d,1350" stroke="#000" stroke-opacity=".12" stroke-width="8" fill="none"/>' % (120 + k * 210, 150 + k * 200, 110 + k * 210, 160 + k * 200)
    R = random.Random(3)
    for _ in range(90):
        b += '<circle cx="%s" cy="%s" r="2.4" fill="#F6D36B" opacity=".7"/>' % (f(R.uniform(0, 1080)), f(R.uniform(1060, 1350)))
    # basket of fruits, left
    b += grapes(170, 990, 110) + banana_bunch(340, 1040, 120, 20)
    b += basket(260, 1060, 300, 170)
    b += apple(160, 1030, 40) + pomegranate(250, 1010, 46) + apple(330, 1030, 36, ("#F2B544", "#C9851A", "#FFE08A"))
    # coconut wrapped in chunri with rice, right
    b += thal(800, 1170, 200, ry=60)
    b += coconut(800, 1070, 78, wrap=("#D4203E", "#F2CF74"), rot=6)
    b += bowl(670, 1180, 40, BRASS, "#F4C43C") + bowl(930, 1180, 40, BRASS, "#D4203E")
    b += bangle_stack(975, 1110, 38, ["#2E8B57", "#F2B544", "#C0223B"], 8, 7)
    b += pastel_cluster(545, 1120, 31, .8, (PEACH, PINK))
    # hanging jasmine + rose strings along the top edge
    for i, x in enumerate(range(40, 1080, 80)):
        L = 50 + 40 * (i % 3)
        b += jasmine_string([(x, 0), (x, L)], 12, pink_every=3) + rose(x, L + 12, 13, PEACH)
    b += fancy_panel(90, 136, 900, 770, "#FFFCF8", GOLD, r=30, corner_size=90)
    S(3, [150, 172, 930, 874], "#C0502E", "#3F2A22", "#2E8B57", tfont="deco")
    return page(b)


# ------------------------------------------------------------------ 4 sky blue: baby clothes on a line + clouds
def card4():
    b = bg_grad(["#DDF0FB", "#C4E3F6", "#EAF6FD"])
    b += cloud(160, 150, 180, "#FFFFFF", .9, "#D6E9F6") + cloud(900, 110, 200, "#FFFFFF", .9, "#D6E9F6") + cloud(560, 70, 140, "#FFFFFF", .8, "#D6E9F6")
    pts = catenary(-10, 170, 1090, 150, 120, 60)
    b += '<path d="%s" stroke="#9B7A5A" stroke-width="3" fill="none"/>' % pts_d(pts)
    items = [(110, lambda x, y: onesie(x, y, 130, "#F9C8D4")), (270, lambda x, y: jhabla(x, y, 120, "#FFE3A3", "#E8A0B4")),
             (430, lambda x, y: sock(x - 20, y, 90, "#BFE3D0") + sock(x + 30, y + 4, 90, "#BFE3D0")),
             (600, lambda x, y: onesie(x, y, 130, "#C9E4F6", "#FFFFFF")), (760, lambda x, y: jhabla(x, y, 120, "#E3D0F2", "#F2CF74")),
             (930, lambda x, y: onesie(x, y, 125, "#FFE3A3"))]
    for x, fn in items:
        i = min(range(len(pts)), key=lambda k: abs(pts[k][0] - x))
        y = pts[i][1]
        b += fn(x, y)
        b += peg(x - 30, y) + peg(x + 30, y)
    # pastel bunting of flowers on the line
    b += cloud(120, 1260, 260, "#FFFFFF", 1, "#D6E9F6") + cloud(960, 1270, 260, "#FFFFFF", 1, "#D6E9F6")
    # cloud-shaped text panel
    d = ("M150,470 C150,420 220,395 270,420 C300,360 400,350 440,400 C480,340 600,340 640,400 C680,350 780,360 810,420 "
         "C860,395 930,420 930,470 C990,480 1010,540 980,580 L980,1190 C1010,1230 990,1280 940,1280 L140,1280 C90,1280 70,1230 100,1190 "
         "L100,580 C70,540 90,480 150,470Z")
    b += '<path d="%s" fill="#FFFFFF" filter="url(#shb)"/>' % d
    b += '<rect x="130" y="500" width="820" height="752" rx="30" fill="none" stroke="#9CCBE8" stroke-width="2" stroke-dasharray="2 9" stroke-linecap="round"/>'
    b += pastel_cluster(110, 520, 41, .75, (PINK, YEL)) + pastel_cluster(970, 520, 42, .75, (PINK, YEL))
    S(4, [150, 540, 930, 1244], "#2F6FA0", "#2A3A48", "#D0607A", tfont="script")
    return page(b)


# ------------------------------------------------------------------ 5 peach: flower jewellery (phoolon ka gehna) displayed at the top
def card5():
    b = bg_grad(["#FFE9DD", "#FAD2C0"])
    b += pat_rect(damask_pattern("dm5", 110, "#E8906A", .1), "dm5")
    b += glow_spot(540, 220, 380, "#FFFFFF", .7)
    # flower tiara / necklace set hanging from a gold rod
    gid, g = lin(GOLD, 0, 0, 0, 1)
    b += defs(g) + '<rect x="120" y="60" width="840" height="12" rx="6" fill="url(#%s)" filter="url(#shs)"/>' % gid
    b += '<circle cx="120" cy="66" r="16" fill="url(#%s)"/><circle cx="960" cy="66" r="16" fill="url(#%s)"/>' % (gid, gid)
    b += flower_necklace(540, 72, 620, 250, main="#FFFFFF", accent="#E86C8C")
    # bajuband (armlets) and earrings of flowers on the sides
    for cx in (170, 910):
        pts = ellipse_points(cx, 260, 80, 80, 40)
        b += jasmine_string(pts, 12, pink_every=4)
        b += rose(cx, 180, 22, PINK) + rose(cx - 30, 188, 14, PEACH) + rose(cx + 30, 188, 14, PEACH)
        b += jasmine_string([(cx, 340), (cx, 420)], 12) + tassel(cx, 420, 60, "#E86C8C") + pastel_cluster(cx + (-60 if cx < 500 else 60), 80, cx, .7, (PINK, PEACH))
        b += jasmine_string([(cx, 72), (cx, 170)], 12)
    b += petals(5, 12, (40, 80, 1040, 520), (8, 14), ("#F4A8BE", "#D96C8C"), avoid=[(250, 70, 830, 520)])
    b += fancy_panel(90, 560, 900, 730, "#FFFBF8", ROSEGOLD, r=24, corner_size=80)
    S(5, [150, 580, 930, 1264], "#B04A2E", "#3F2A22", "#C0507A", tfont="deco")
    return page(b)


# ------------------------------------------------------------------ 6 soft pink: arch photo of the mother-to-be, floral arch + veni strands
def card6():
    b = bg_grad(["#FFF1F5", "#F9DCE6"])
    b += grain()
    R = random.Random(6)
    for _ in range(40):
        b += blossom(R.uniform(0, W), R.uniform(0, 560), R.uniform(8, 14), "#FFFFFF", "#F2B7C4", 5, R.uniform(0, 70), op=.6)
    ph = dict(shape="arch", x=330, y=110, w=420, h=420)
    b += frame_ring("arch", ph["x"], ph["y"], ph["w"], ph["h"], ROSEGOLD, 9, 0)
    b += slot_placeholder("arch", ph["x"], ph["y"], ph["w"], ph["h"], "#FFF6F9", "#F2D0DC", kind="mother")
    # florals along the arch edge
    pts = [(x, y) for x, y in ellipse_points(540, 110 + 420 * .34, 236, 256, 30, 180, 360)]
    fl = [lambda x, y, r: peony(x, y, 30, PINK, r), lambda x, y, r: rose(x, y, 24, PEACH, r),
          lambda x, y, r: rose(x, y, 22, LILAC, r), lambda x, y, r: blossom(x, y, 16, "#FFFFFF", "#F2B7C4", 5, r)]
    b += floral_along(pts[2:-2], 61, fl, every=2, leaves=("#A8CBA0", "#5E8F5A"), leaf_len=44)
    # veni strands either side
    for x, L in ((230, 330), (170, 260), (110, 190), (850, 330), (910, 260), (970, 190)):
        b += jasmine_string([(x, 0), (x, L)], 12, pink_every=4) + rose(x, L + 14, 15, PINK)
    b += bangle_stack(250, 540, 44, ["#E86C8C", "#F2CF74", "#9FDCC2"], 9, 8) + bangle_stack(830, 540, 44, ["#9FDCC2", "#F2CF74", "#E86C8C"], 9, 8)
    b += fancy_panel(90, 560, 900, 730, "#FFFFFF", ROSEGOLD, r=36, corners=False, bw=2)
    b += '<rect x="112" y="582" width="856" height="686" rx="26" fill="none" stroke="#F2B7C4" stroke-width="2" stroke-dasharray="2 9" stroke-linecap="round"/>'
    S(6, [150, 568, 930, 1270], "#B03A62", "#3A2A30", "#9B6FC0", tfont="script", photo=ph)
    return page(b)


# ------------------------------------------------------------------ 7 lemon yellow: godh bharai thal at the bottom, text on top
def card7():
    b = bg_grad(["#FFFBE6", "#FCEFB8"])
    b += pat_rect(dots_pattern("d7", 36, 2, "#E8C660", .45), "d7")
    b += light_rays(540, 1150, 20, 900, "#FFFFFF", .35, 180, -180, .04)
    b += fancy_panel(90, 70, 900, 790, "#FFFFFF", GOLD, r=30, corner_size=90)
    b += thal(540, 1130, 360, ry=110)
    b += coconut(540, 1010, 80, wrap=("#2E8B57", "#F2CF74"))
    b += bangle_stack(370, 1110, 60, ["#C0223B", "#2E8B57", "#F2B544", "#C0223B", "#2E8B57"], 11, 9)
    b += apple(700, 1080, 34) + pomegranate(760, 1100, 36) + apple(820, 1090, 30, ("#F2B544", "#C9851A", "#FFE08A"))
    b += bowl(640, 1160, 40, SILVER, "#F4C43C") + bowl(450, 1170, 40, SILVER, "#D4203E")
    b += dryfruits(7, 540, 1170, 80, 20, 20)
    b += pastel_cluster(230, 1000, 71, .9, (YEL, PINK)) + pastel_cluster(870, 990, 72, .9, (YEL, PINK))
    for x in (260, 820):
        b += jasmine_string(catenary(x - 140, 900, x + 140, 900, 60, 20), 12, pink_every=3)
    S(7, [150, 116, 930, 820], "#A0542A", "#3F3322", "#2E8B57", tfont="deco")
    return page(b)


# ------------------------------------------------------------------ 8 mint paper-cut: large white mother silhouette in a floral oval halo
def card8():
    b = bg_grad(["#DDF2EA", "#BFE3D3"])
    # paper-cut layered hills at the top
    for k, col in enumerate(("#A9D9C4", "#CBEBDD", "#E9F7F1")):
        y = 40 + k * 60
        b += '<path d="M0,%d C200,%d 360,%d 540,%d C720,%d 880,%d 1080,%d L1080,0 L0,0Z" fill="%s" filter="url(#sh)" transform="scale(1 1)"/>' % (
            y + 100, y + 30, y + 150, y + 90, y + 30, y + 150, y + 90, col) if False else ""
    gid, g = rad([(0, "#FFFFFF", .95), (1, "#FFFFFF", .15)])
    b += defs(g) + '<ellipse cx="540" cy="290" rx="270" ry="270" fill="url(#%s)"/>' % gid
    pts = ellipse_points(540, 290, 270, 250, 60, 110, 430)
    fl = [lambda x, y, r: peony(x, y, 26, PINK, r), lambda x, y, r: rose(x, y, 22, PEACH, r),
          lambda x, y, r: blossom(x, y, 16, "#FFFFFF", "#F2B7C4", 5, r), lambda x, y, r: rose(x, y, 20, LILAC, r)]
    b += floral_along(pts, 81, fl, every=3, leaves=("#7FB08A", "#2F6B4A"), leaf_len=36)
    b += mother(540, 520, 112, "#FFFFFF", "#9CCFB8", "#E8B04A", facing=1, pallu_col="#F3FBF7")
    b += '<path d="M380,524 L700,524" stroke="#9CCFB8" stroke-width="3"/>'
    # paper-cut cloud layers at the bottom
    for k, (col, dy) in enumerate((("#A9D9C4", 0), ("#CBEBDD", 30), ("#F3FBF7", 60))):
        d = "M0,%d " % (1220 + dy)
        for i in range(7):
            d += "a80,60 0 0 1 160,0 " if i % 2 == 0 else "a80,46 0 0 1 160,0 "
        d += "L1120,1350 L0,1350 Z"
        b += '<path d="%s" fill="%s" filter="url(#sh)" transform="translate(%d 0)"/>' % (d, col, -40 * k)
    b += fancy_panel(90, 545, 900, 745, "#FFFFFF", GOLD, r=30, corners=False, bw=2, op=.95)
    S(8, [150, 565, 930, 1270], "#2E7A5E", "#26382F", "#C0507A", tfont="script")
    return page(b)


# ------------------------------------------------------------------ 9 coral: rounded photo framed by bangles and pastel corners
def card9():
    b = bg_grad(["#FFE4DE", "#F9C6BA"])
    b += pat_rect(damask_pattern("dm9", 96, "#FFFFFF", .22), "dm9")
    ph = dict(shape="rounded", x=250, y=70, w=580, h=420)
    # border of bangles around the photo
    b += '<path d="%s" fill="#FFFFFF" opacity=".75" filter="url(#sh)"/>' % scallop_path_rect(214, 36, 652, 490, 16)
    b += jasmine_string([(222, 44), (858, 44)], 13, pink_every=4) + jasmine_string([(222, 518), (858, 518)], 13, pink_every=4)
    for cx in (140, 940):
        b += bangle_stack(cx, 530, 56, ["#C0223B", "#F2B544", "#2E8B57", "#E86C8C", "#F2B544"], 10, 9)
    b += frame_ring("rounded", ph["x"], ph["y"], ph["w"], ph["h"], GOLD, 10, 0)
    b += slot_placeholder("rounded", ph["x"], ph["y"], ph["w"], ph["h"], "#FFF4F1", "#F2CFC6", kind="mother")
    b += pastel_cluster(250, 90, 91, 1.0, (PINK, PEACH)) + pastel_cluster(830, 490, 92, 1.0, (PINK, PEACH))
    b += flower_necklace(120, 150, 150, 200, pendant=False) + rose(120, 360, 22, PINK) + tassel(120, 372, 70, "#E86C8C")
    b += flower_necklace(960, 150, 150, 200, pendant=False) + rose(960, 360, 22, PINK) + tassel(960, 372, 70, "#E86C8C")
    b += fancy_panel(90, 548, 900, 742, "#FFFBF9", GOLD, r=26, corner_size=80)
    S(9, [150, 570, 930, 1272], "#B0402E", "#3F2A26", "#C0507A", tfont="deco", photo=ph)
    return page(b)


# ------------------------------------------------------------------ 10 blush & lilac: decorated flower swing (jhula)
def card10():
    b = bg_grad(["#F7EEFB", "#EBD8F2", "#F9E6EE"])
    b += bokeh(10, 30, (0, 0, W, 700), ["#FFFFFF", "#F4C6D6"], 6, 26, (.25, .6))
    # top beam wrapped with leaves and flowers
    gid, g = lin(["#C98B4E", "#8C5A24"], 0, 0, 0, 1)
    b += defs(g) + '<rect x="0" y="40" width="1080" height="30" fill="url(#%s)" filter="url(#sh)"/>' % gid
    for x in range(0, 1100, 50):
        b += leaf(x, 55, 44, 150 if (x // 50) % 2 else 30, "#8DB38A", "#4E7A4A", vein=False)
    for x in range(20, 1100, 90):
        b += peony(x, 58, 22, [PINK, LILAC, PEACH][(x // 90) % 3])
    b += jhula(540, 70, 380, 340, ("#F4C9D6", "#D9899F"))
    # side flower curtains
    for i, x in enumerate((70, 130, 190, 890, 950, 1010)):
        L = 260 - (i % 3) * 50
        b += jasmine_string([(x, 72), (x, 72 + L)], 12, pink_every=3) + rose(x, 72 + L + 14, 14, LILAC)
    b += pastel_cluster(300, 420, 101, .8) + pastel_cluster(780, 420, 102, .8)
    b += fancy_panel(90, 548, 900, 742, "#FFFFFF", ROSEGOLD, r=30, corners=True, corner_size=80, bw=2)
    S(10, [150, 566, 930, 1270], "#8A3FA0", "#3A2A48", "#C0507A", tfont="script")
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
