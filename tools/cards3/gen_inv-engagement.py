"""inv-engagement (sagai / roka invitation): jharokha frames, ring boxes, roka thal, chunri, save-the-date layouts."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_d import *
from render import render_cards

CAT = "inv-engagement"
SPECS = []


def S(n, zone, title, text, accent, **kw):
    SPECS.append(spec(CAT, n, zone, title, text, accent, **kw))


def hanging_strand(x, y0, L, pink=4, end_rose=True, tas="#B8264A"):
    s = jasmine_string([(x, y0), (x, y0 + L)], 13, pink_every=pink)
    if end_rose:
        s += rose(x, y0 + L + 16, 17, ("#8E1027", "#C2264B", "#F07A92"))
        s += tassel(x, y0 + L + 26, 70, tas)
    return s


# ------------------------------------------------------------------ 1 royal jharokha, arch photo
def card1():
    b = bg_grad(["#3E0512", "#6E0F24", "#4A0816"])
    b += pat_rect(damask_pattern("dm1", 120, "#E9C46A", .13), "dm1")
    b += glow_spot(540, 300, 420, "#FFB36B", .28)
    b += bokeh(11, 30, (0, 0, W, 520), ["#FFD98A", "#FFF1C9"], 4, 16, (.25, .7))
    ph = dict(shape="arch", x=355, y=112, w=370, h=368)
    b += slot_placeholder("arch", ph["x"], ph["y"], ph["w"], ph["h"], "#F8ECE0", "#E6D2C0")
    b += jharokha(ph["x"], ph["y"], ph["w"], ph["h"])
    # jasmine strands either side of the jharokha
    for x, L in ((80, 250), (150, 320), (220, 210), (1000, 250), (930, 320), (860, 210)):
        b += hanging_strand(x, 0, L)
    b += fancy_panel(84, 522, 912, 772, "#FFF8EA", r=30, corner_size=110)
    # little rose clusters on the panel top corners, outside the zone
    for cx in (84, 996):
        b += leaf(cx, 522, 60, -150 if cx < 500 else -30) + leaf(cx, 522, 60, 150 if cx < 500 else 30)
        b += rose(cx, 522, 30, ("#8E1027", "#C2264B", "#F07A92")) + rose(cx + (40 if cx < 500 else -40), 542, 18, ("#B8264A", "#E0506E", "#F8A5B5"))
    S(1, [150, 562, 930, 1264], "#7A1028", "#3A1E22", "#9A6A12", tfont="deco", photo=ph)
    return page(b)


# ------------------------------------------------------------------ 2 blush save-the-date: photo + ring box side by side
def card2():
    b = bg_grad(["#FCEFEA", "#F6DCD6"])
    b += defs(marble("mb2", vein="#C98E7C", op=.25)) + '<rect width="1080" height="1350" fill="#fff" filter="url(#mb2)"/>'
    b += grain()
    ph = dict(shape="rounded", x=90, y=80, w=560, h=440)
    b += frame_ring("rounded", ph["x"], ph["y"], ph["w"], ph["h"], ROSEGOLD, 12, 0)
    b += '<path d="%s" fill="none" stroke="#C98E7C" stroke-width="1.6"/>' % shape_grow("rounded", ph["x"], ph["y"], ph["w"], ph["h"], 26)
    b += slot_placeholder("rounded", ph["x"], ph["y"], ph["w"], ph["h"], "#FBE9E4", "#EBCFC6")
    # floral cluster tucked at the top-left corner
    for L, a in ((110, 200), (90, 250), (120, 170), (80, 290)):
        b += leaf(92, 82, L, a, "#9DB89A", "#557A55")
    b += eucalyptus(96, 86, 170, 110) + eucalyptus(96, 86, 150, 330)
    b += peony(80, 70, 62, ("#E07F98", "#F6BFCB", "#FFEFF2")) + rose(148, 40, 36, ("#B8264A", "#E0506E", "#F8A5B5")) + rose(30, 150, 34, ("#D06A84", "#F2A4B6", "#FFE1E8"))
    b += blossom(170, 118, 20, "#FFFFFF", "#F2B7C4") + gypso(5, 110, 90, 90, 20)
    # ring box hero on the right, with petals
    b += glow_spot(850, 330, 230, "#FFFFFF", .7)
    b += ring_box(850, 470, 300, velvet=("#7E3346", "#B85A70", "#E08DA0"), trim=ROSEGOLD, ring_metal=ROSEGOLD, rings=2)
    b += petals(21, 14, (680, 120, 1060, 540), (12, 20), ("#E07F98", "#B8264A"), avoid=[(90, 60, 670, 540)])
    b += sparkles(3, 10, (690, 90, 1050, 300), "#FFFFFF", 6, 14)
    # text card
    b += fancy_panel(70, 580, 940, 700, "#FFFDFB", ROSEGOLD, r=18, corners=False, bw=3)
    b += '<path d="M470,610 Q540,590 610,610" stroke="#C98E7C" stroke-width="2" fill="none"/>'
    S(2, [130, 600, 950, 1262], "#8A3A4E", "#3F2A2E", "#B0605A", tfont="script", photo=ph)
    return page(b)


# ------------------------------------------------------------------ 3 emerald: heart photo, pearl swags, velvet glass panel
def card3():
    b = bg_grad(["#062B22", "#0E4A3A", "#072E25"])
    b += pat_rect(damask_pattern("dm3", 96, "#E9C46A", .1), "dm3")
    b += glow_spot(540, 250, 380, "#9FE0C0", .22)
    ph = dict(shape="heart", x=375, y=86, w=330, h=330)
    hp = heart_points(540, 86 - 16, 330 + 40, 330 + 34, 120)
    gid, g = lin(GOLD, 0, 0, 1, 1)
    b += defs(g) + '<path d="%sZ" fill="none" stroke="url(#%s)" stroke-width="18" filter="url(#sh)"/>' % (pts_d(hp), gid)
    b += '<path d="%s" fill="#FFF" opacity="0"/>' % shape_d("heart", ph["x"], ph["y"], ph["w"], ph["h"])
    b += slot_placeholder("heart", ph["x"], ph["y"], ph["w"], ph["h"], "#EAF3EC", "#C9DDCE")
    b += pearl_string(heart_points(540, 86 - 34, 330 + 76, 330 + 62, 160), 5)
    # pearl swags from the top corners with emerald drops
    for side in (-1, 1):
        for k, (sag, x1) in enumerate(((120, 380), (190, 330), (70, 420))):
            x0 = 540 + side * 540
            xe = 540 + side * (540 - x1)
            pts = catenary(x0, 30 + k * 30, xe, 20, sag)
            b += pearl_string(pts, 4.5)
        b += tassel(540 + side * 470, 150, 110, "#0E6B4F")
        b += tassel(540 + side * 400, 210, 90, "#0E6B4F")
    # white roses + gold leaves at the heart tip
    for a_ in (200, 240, 300, 340, 160, 20):
        b += leaf(540, 440, 70, a_, "#E9C46A", "#9C6B17")
    b += rose(540, 452, 34, ("#D9D2C3", "#F4EFE6", "#FFFFFF")) + rose(488, 440, 24, ("#D9D2C3", "#F4EFE6", "#FFFFFF")) + rose(592, 440, 24, ("#D9D2C3", "#F4EFE6", "#FFFFFF"))
    # dark velvet glass panel
    b += fancy_panel(80, 520, 920, 770, "#0A3A2E", GOLD, r=30, corner_size=100, grain_=False)
    b += '<rect x="80" y="520" width="920" height="770" rx="30" fill="#000" opacity=".18"/>'
    S(3, [150, 566, 930, 1250], "gold", "#F6EBD0", "#E9C46A", tone="dark", tfont="deco", photo=ph)
    return page(b)


# ------------------------------------------------------------------ 4 navy: text top, pill photo + rings on thal bottom
def card4():
    b = bg_grad(["#0B1633", "#16295A", "#0E1C40"])
    b += glow_spot(820, 1050, 380, "#F4C874", .25)
    b += sparkles(4, 40, (0, 0, W, H), "#FFF1C9", 3, 9, (.3, .9))
    b += bokeh(6, 18, (0, 0, W, H), ["#F4C874", "#FFFFFF"], 3, 10, (.2, .5))
    # gold art-deco border
    gid, g = lin(GOLD, 0, 0, 1, 1)
    b += defs(g) + '<rect x="28" y="28" width="1024" height="1294" rx="6" fill="none" stroke="url(#%s)" stroke-width="4"/>' % gid
    for cx, cy, sx, sy in ((28, 28, 1, 1), (1052, 28, -1, 1), (28, 1322, 1, -1), (1052, 1322, -1, -1)):
        b += '<g transform="translate(%d %d) scale(%d %d)" fill="none" stroke="url(#%s)" stroke-width="3"><path d="M0,70 L40,70 L40,40 L70,40 L70,0"/><path d="M0,100 L60,100 L60,60 L100,60 L100,0" stroke-width="1.5"/><circle cx="40" cy="40" r="6" fill="url(#%s)"/></g>' % (cx, cy, sx, sy, gid, gid)
    # text: ivory glass
    b += fancy_panel(80, 70, 920, 770, "#FBF5E8", GOLD, r=24, corners=False, bw=4)
    b += '<path d="M540,88 l14,14 l-14,14 l-14,-14Z" fill="url(#%s)"/>' % gid
    ph = dict(shape="pill", x=90, y=890, w=560, h=330)
    b += frame_ring("pill", ph["x"], ph["y"], ph["w"], ph["h"], GOLD, 10, 0)
    b += pearl_string(ellipse_points(0, 0, 1, 1, 2), 1)[:0]
    # pearl outline around pill
    r = (ph["h"] + 48) / 2
    x0, x1, cy = ph["x"] + ph["h"] / 2, ph["x"] + ph["w"] - ph["h"] / 2, ph["y"] + ph["h"] / 2
    pts = [(x0 + (x1 - x0) * i / 30, cy - r) for i in range(31)] + ellipse_points(x1, cy, r, r, 30, -90, 90)[1:] + \
          [(x1 - (x1 - x0) * i / 30, cy + r) for i in range(1, 31)] + ellipse_points(x0, cy, r, r, 30, 90, 270)[1:]
    b += pearl_string(pts, 5)
    b += slot_placeholder("pill", ph["x"], ph["y"], ph["w"], ph["h"], "#EEF0F6", "#CCD3E2")
    # rings on a decorated thal
    b += thal(860, 1150, 190, ry=70)
    gc, c = rad([(0, "#E0506E"), (1, "#8E1027")], .4, .35, .7)
    b += defs(c) + '<ellipse cx="860" cy="1126" rx="110" ry="42" fill="url(#%s)" filter="url(#shs)"/>' % gc
    for i in range(18):
        a_ = i * 20
        b += '<circle cx="%s" cy="%s" r="3" fill="#F2CF74"/>' % (f(860 + 105 * math.cos(math.radians(a_))), f(1126 + 39 * math.sin(math.radians(a_))))
    b += upright_ring(820, 1062, 54, GOLD, -10, True) + upright_ring(900, 1070, 50, ROSEGOLD, 10, False)
    b += petals(8, 10, (700, 1080, 1030, 1200), (10, 16), ("#E0506E", "#8E1027"), avoid=[(760, 1060, 960, 1150)])
    b += sparkles(9, 6, (740, 960, 1000, 1060), "#FFFFFF", 8, 16)
    S(4, [150, 110, 930, 810], "#14265A", "#2A2A3A", "#9A6A12", tfont="classic", photo=ph)
    return page(b)


# ------------------------------------------------------------------ 5 ivory & sage botanical: rect photo with mat, rings at corner
def card5():
    b = bg_grad(["#FBF8F0", "#F1EEE2"])
    b += grain()
    R = random.Random(5)
    for _ in range(26):
        b += eucalyptus(R.uniform(0, W), R.uniform(0, H), R.uniform(80, 140), R.uniform(0, 360), "#D5E0D2", "#C3D2C0", 6)
    b += '<rect x="0" y="0" width="1080" height="1350" fill="#FBF8F0" opacity=".55"/>'
    ph = dict(shape="rect", x=250, y=86, w=580, h=400)
    b += '<rect x="226" y="62" width="628" height="448" fill="#FFFFFF" filter="url(#sh)"/>'
    gid, g = lin(GOLD, 0, 0, 1, 1)
    b += defs(g) + '<rect x="226" y="62" width="628" height="448" fill="none" stroke="url(#%s)" stroke-width="5"/>' % gid
    b += '<rect x="244" y="80" width="592" height="412" fill="none" stroke="#C9B37A" stroke-width="1.2"/>'
    b += slot_placeholder("rect", ph["x"], ph["y"], ph["w"], ph["h"], "#F1F3EC", "#D8DFD2")
    # botanical corner swags (top-left + bottom-right of the frame)
    for (cx, cy, base) in ((236, 70, 200), (846, 502, 20)):
        for k in range(7):
            b += eucalyptus(cx, cy, R.uniform(120, 190), base + k * 20 - 60, "#9DB89A", "#5E8570", 7)
        for k in range(6):
            b += fern(cx, cy, R.uniform(90, 140), base + k * 25 - 70, "#7FA07A")
        b += rose(cx, cy, 44, ("#D9D2C3", "#F4EFE6", "#FFFFFF")) + rose(cx + (54 if cx < 500 else -54), cy + (20 if cx < 500 else -20), 30, ("#E8C9B8", "#F6E3D8", "#FFFFFF"))
        b += rose(cx + (10 if cx < 500 else -10), cy + (60 if cx < 500 else -60), 26, ("#D9D2C3", "#F4EFE6", "#FFFFFF"))
        b += gypso(int(cx), cx, cy, 80, 22)
    # interlocked rings at the frame's top-right, tied with a sage ribbon
    b += linked_rings(950, 190, 58, stone=True)
    b += '<path d="M950,250 C930,290 960,320 940,360 M950,250 C975,290 955,330 980,350" stroke="#7FA07A" stroke-width="5" fill="none" stroke-linecap="round"/>'
    # botanical border: sage ornament band at the bottom corners
    b += '<rect x="36" y="36" width="1008" height="1278" fill="none" stroke="#9DB89A" stroke-width="2"/>'
    b += '<rect x="48" y="48" width="984" height="1254" fill="none" stroke="#C9B37A" stroke-width="1"/>'
    for cx, sx in ((60, 1), (1020, -1)):
        for k in range(5):
            b += fern(cx, 1290, 150 - k * 12, -90 + sx * (10 + k * 14) if sx > 0 else -90 - (10 + k * 14), "#9DB89A", op=.9)
    S(5, [150, 560, 930, 1262], "#3E5A40", "#2F3A2D", "#8A7440", tfont="script", photo=ph)
    return page(b)


# ------------------------------------------------------------------ 6 roka thal hero + chunri swag
def card6():
    b = bg_grad(["#7E0E22", "#A8162E", "#6E0B1C"])
    b += pat_rect(dots_pattern("dt6", 34, 2.2, "#F6D36B", .35), "dt6")
    b += glow_spot(540, 1100, 520, "#FFB347", .35)
    b += fancy_panel(96, 132, 888, 790, "#FFF6E6", GOLD, r=22, corner_size=100)
    b += chunri_swag(-30, 1110, -6, 40, 44, ("#D4203E", "#8E1027"), n=4)
    # the roka thal
    b += thal(540, 1150, 340, ry=104)
    b += dryfruits(4, 330, 1150, 70, 30, 26) + dryfruits(7, 750, 1150, 70, 30, 26)
    # coconut in chunri (left), ring box (centre), laddoo pyramid (right)
    b += coconut(360, 1080, 60, wrap=("#D4203E", "#F2CF74"), rot=-8)
    for (x, y) in ((670, 1130), (722, 1130), (774, 1130), (696, 1090), (748, 1090), (722, 1050)):
        b += laddoo(x, y, 28)
    b += ring_box(520, 1160, 190, rings=2)
    b += bowl(430, 1170, 44, SILVER, "#E23A4A") + bowl(860, 1180, 40, SILVER, "#F4B63C")
    b += petals(3, 18, (180, 1060, 900, 1250), (10, 18), ("#E23A4A", "#9E1B35"), avoid=[(300, 960, 800, 1170)])
    S(6, [150, 180, 930, 890], "#8E1027", "#3B1D14", "#A8741F", tfont="deco")
    return page(b)


# ------------------------------------------------------------------ 7 royal purple: big open ring box with light rays
def card7():
    b = bg_grad(["#2A0C36", "#4E1A60", "#2A0C36"])
    b += light_rays(540, 330, 22, 900, "#FFE7B0", .16, 360, -180, .04)
    b += glow_spot(540, 300, 330, "#FFD98A", .5)
    b += sparkles(7, 36, (60, 30, 1020, 520), "#FFF1C9", 5, 14)
    b += ring_box(540, 505, 380, velvet=("#2E0A3E", "#5B1F6B", "#8A3FA0"), rings=1)
    b += petals(12, 22, (60, 60, 1020, 520), (12, 22), ("#C2264B", "#7A0F2B"), avoid=[(300, 90, 780, 520)])
    # lilac satin text panel with scalloped top edge
    d = scallop_path_rect(80, 560, 920, 740, 23)
    gid, g = lin(["#FFFFFF", "#F6EEF8"], 0, 0, 0, 1)
    b += defs(g) + '<path d="%s" fill="url(#%s)" filter="url(#shb)"/>' % (d, gid)
    gg, g2 = lin(GOLD, 0, 0, 1, 1)
    b += defs(g2) + '<rect x="110" y="590" width="860" height="680" rx="8" fill="none" stroke="url(#%s)" stroke-width="3"/>' % gg
    b += '<rect x="122" y="602" width="836" height="656" rx="4" fill="none" stroke="url(#%s)" stroke-width="1"/>' % gg
    b += corner_filigree(122, 602, 80, 1, 1, "url(#%s)" % gg) + corner_filigree(958, 602, 80, -1, 1, "url(#%s)" % gg)
    S(7, [160, 620, 920, 1250], "#4E1A60", "#2E2236", "#9A6A12", tfont="classic")
    return page(b)


# ------------------------------------------------------------------ 8 teal & peach: oval photo with floral crescent
def card8():
    b = bg_grad(["#0C4F55", "#146A6E", "#0C4F55"])
    b += pat_rect(dots_pattern("dt8", 44, 1.8, "#F7C9A8", .3), "dt8")
    # paper-cut layered arcs behind the oval
    for k, (col, op) in enumerate((("#1C7E80", 1), ("#248F8F", 1), ("#2FA19D", .9))):
        rr = 380 - k * 40
        b += '<ellipse cx="540" cy="300" rx="%d" ry="%d" fill="%s" opacity="%s" filter="url(#sh)"/>' % (rr + 40, rr - 30, col, op)
    ph = dict(shape="oval", x=280, y=100, w=520, h=400)
    b += frame_ring("oval", ph["x"], ph["y"], ph["w"], ph["h"], GOLD, 12, 0)
    b += slot_placeholder("oval", ph["x"], ph["y"], ph["w"], ph["h"], "#FFF3EA", "#EED3C2")
    # floral crescent along the lower-left of the oval
    pts = ellipse_points(540, 300, 280, 222, 26, 95, 215)
    fl = [lambda x, y, r: peony(x, y, 34, ("#E98E6E", "#F7C4A8", "#FFE9DC"), r),
          lambda x, y, r: rose(x, y, 28, ("#C2264B", "#E0506E", "#F8A5B5"), r),
          lambda x, y, r: rose(x, y, 24, ("#E8A07A", "#F6C8A8", "#FFF0E4"), r),
          lambda x, y, r: blossom(x, y, 18, "#FFFFFF", "#F2B7C4", 5, r)]
    b += floral_along(pts, 8, fl, every=2, leaves=("#7FB08A", "#2F6B4A"), leaf_len=50)
    pts2 = ellipse_points(540, 300, 280, 222, 12, -40, 5)
    b += floral_along(pts2, 9, fl, every=3, leaves=("#7FB08A", "#2F6B4A"), leaf_len=44)
    b += gypso(8, 300, 440, 110, 26) + gypso(9, 810, 180, 80, 16)
    # scalloped peach cloth banner
    d = scallop_path_rect(90, 568, 900, 718, 22)
    gid, g = lin(["#FFF4EC", "#FCE3D2"], 0, 0, 0, 1)
    b += defs(g) + '<path d="%s" fill="url(#%s)" filter="url(#shb)"/>' % (d, gid)
    b += '<rect x="120" y="598" width="840" height="658" rx="10" fill="none" stroke="#D9A07A" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round"/>'
    S(8, [150, 612, 930, 1244], "#0E555B", "#3A2A26", "#B0603A", tfont="script", photo=ph)
    return page(b)


# ------------------------------------------------------------------ 9 diagonal chunri drape + mithai & coconut corner
def card9():
    b = bg_grad(["#F8EBD8", "#EED8B8"])
    b += grain()
    b += pat_rect(damask_pattern("dm9", 110, "#B7791F", .08), "dm9")
    # flowing red chunri from top-right sweeping down the left edge
    g1, a = lin(["#E0344E", "#B01A33", "#7E0E22"], 0, 0, 1, 1)
    gb, bb = lin(GOLD, 0, 0, 1, 0)
    d = ("M1080,0 L1080,190 C900,240 700,170 520,210 C330,250 190,360 150,560 C120,720 150,900 100,1080 C80,1160 40,1230 0,1270 "
         "L0,0 Z")
    b += defs(a, bb) + '<path d="%s" fill="url(#%s)" filter="url(#shb)"/>' % (d, g1)
    edge = "M1080,190 C900,240 700,170 520,210 C330,250 190,360 150,560 C120,720 150,900 100,1080 C80,1160 40,1230 0,1270"
    b += '<path d="%s" stroke="url(#%s)" stroke-width="26" fill="none"/>' % (edge, gb)
    b += '<path d="%s" stroke="#FFF3C4" stroke-width="3" fill="none" stroke-dasharray="3 9" transform="translate(0 0)"/>' % edge
    # folds and dot print on the cloth
    for k in range(6):
        b += '<path d="M%d,0 C%d,%d %d,%d %d,%d" stroke="#000" stroke-opacity=".1" stroke-width="6" fill="none"/>' % (
            900 - k * 150, 800 - k * 150, 120, 500 - k * 120, 200 + k * 40, 60 + k * 10, 900 - k * 140)
    R = random.Random(9)
    for _ in range(170):
        x, y = R.uniform(0, 1080), R.uniform(0, 1250)
        # keep dots inside the cloth region roughly
        if (y < 180 and x > 0) or (x < 130 and y < 1200) or (y < 220 and x < 700) or (x < 300 and y < 450):
            b += '<circle cx="%s" cy="%s" r="2.6" fill="#F6D36B" opacity=".7"/>' % (f(x), f(y))
    for x in range(1060, 520, -70):
        pass
    # tassels hanging from the chunri edge
    for x, y in ((980, 215), (820, 222), (660, 196), (480, 222)):
        b += tassel(x, y, 80, "#B01A33")
    # coconut + mithai in the bottom-right corner
    b += thal(900, 1180, 150, SILVER, ry=48)
    b += coconut(880, 1120, 50, wrap=("#D4203E", "#F2CF74"), rot=12)
    for x, y in ((960, 1160), (1000, 1176), (930, 1180)):
        b += katli(x, y, 30, 10)
    b += laddoo(820, 1170, 20) + laddoo(850, 1185, 20)
    b += leaf(760, 1170, 80, 190, "#5F8B4C", "#2F5A2A") + leaf(1040, 1120, 70, -60, "#5F8B4C", "#2F5A2A")
    # parchment panel
    b += fancy_panel(160, 300, 862, 860, "#FFFBF3", GOLD, r=20, corner_size=80)
    S(9, [201, 350, 981, 1110], "#9E1B35", "#3B1D14", "#A8741F", tfont="deco")
    return page(b)


# ------------------------------------------------------------------ 10 pink & mint: flower-string curtain + shagun gift boxes
def card10():
    b = bg_grad(["#FDF1F4", "#F8DDE5"])
    b += pat_rect(dots_pattern("dt10", 40, 2, "#E8A0B4", .4), "dt10")
    # top rail with flower-string curtain
    gid, g = lin(GOLD, 0, 0, 0, 1)
    b += defs(g) + '<rect x="0" y="0" width="1080" height="22" fill="url(#%s)"/>' % gid
    R = random.Random(10)
    for i, x in enumerate(range(20, 1080, 44)):
        L = 90 + 70 * abs(math.sin(i * .55)) + R.uniform(0, 30)
        b += jasmine_string([(x, 20), (x, 20 + L)], 12, pink_every=3 + i % 3)
        b += rose(x, 20 + L + 12, 12, ("#D05A7A", "#F08AA2", "#FFD1DC") if i % 2 else ("#2E8B6E", "#7FC8A9", "#D5F2E4"))
    # swags of green leaves along the rail
    for x in range(0, 1100, 60):
        b += leaf(x, 22, 40, 120, "#7FC8A9", "#2E8B6E", vein=False)
    # mint panel with gold border
    b += fancy_panel(90, 250, 900, 790, "#FFFFFF", GOLD, r=26, corner_size=90)
    b += '<rect x="90" y="250" width="900" height="790" rx="26" fill="#E7F6EF" opacity=".35"/>'
    # shagun gift boxes (left) and sweets boxes (right) at the bottom
    b += gift_box(170, 1250, 170, 120, ("#F4A8B8", "#D66F8A"), GOLD, pattern="#FFFFFF")
    b += gift_box(300, 1250, 110, 170, ("#9FDCC2", "#5CAE8E"), GOLD)
    b += gift_box(250, 1115, 110, 70, ("#FFFFFF", "#EAD7DD"), ROSEGOLD)
    b += gift_box(920, 1250, 170, 110, ("#9FDCC2", "#5CAE8E"), ROSEGOLD, pattern="#FFFFFF")
    b += gift_box(790, 1250, 110, 160, ("#F4A8B8", "#D66F8A"), GOLD)
    b += gift_box(900, 1125, 100, 80, ("#FFF1C9", "#E3C27A"), GOLD)
    b += ring_box(560, 1250, 110, velvet=("#7E3346", "#B85A70", "#E08DA0"), trim=GOLD, rings=2)
    b += petals(2, 10, (380, 1060, 700, 1260), (8, 14), ("#E07F98", "#B8264A"), avoid=[(470, 1100, 650, 1300)])
    S(10, [150, 296, 930, 996], "#A8325A", "#3A2A30", "#2E8B6E", tfont="script")
    return page(b)


if __name__ == "__main__":
    cards = {}
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7, card8, card9, card10], 1):
        cards["E-%s-%d" % (CAT, i)] = fn()
    write_specs(CAT, SPECS)
    only = [a for a in sys.argv[1:]]
    if only:
        cards = {k: v for k, v in cards.items() if k.split("-")[-1] in only}
    render_cards(cards)
