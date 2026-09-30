"""Naming ceremony (namkaran) invitations: palna, footprints, lullaby moon, peacock feather, toys, pastels."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_e import *
from render import render_cards

CAT = "inv-naming-ceremony"


def spec(n, zone, title, text, accent, tone="light", tfont="classic", align="center", photo=None):
    d = {"id": "E-%s-%d" % (CAT, n), "tpl": True, "zone": zone,
         "colors": {"title": title, "text": text, "accent": accent},
         "tone": tone, "title": tfont, "align": align}
    if photo:
        d["photo"] = photo
        d["slot"] = True
    return d


def baby_silhouette(a, cx, cy, r, col, op=0.45):
    """soft baby placeholder (round head, little tuft, swaddle)."""
    o = C(cx, cy - r * 0.15, r * 0.34, col)
    o += P("M%.1f,%.1f q%.1f,%.1f %.1f,%.1f" % (cx - r * 0.05, cy - r * 0.48, r * 0.1, -r * 0.12, r * 0.14, -r * 0.02), stroke=col, stroke_width=r * 0.04, stroke_linecap="round")
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" % (cx - r * 0.6, cy + r * 0.9, cx - r * 0.55, cy + r * 0.2, cx + r * 0.55, cy + r * 0.2, cx + r * 0.6, cy + r * 0.9), col)
    return g(o, opacity=op)


def lace_panel(a, x, y, w, h, fill="#FFFDF9", edge="#FFFFFF", r=14, shadow=0.2):
    """scalloped lace-edged panel."""
    o = ""
    n = int(w / (r * 1.8))
    for i in range(n + 1):
        xx = x + i * w / n
        o += C(xx, y, r, edge) + C(xx, y + h, r, edge)
    m = int(h / (r * 1.8))
    for j in range(m + 1):
        yy = y + j * h / m
        o += C(x, yy, r, edge) + C(x + w, yy, r, edge)
    o += R(x, y, w, h, fill)
    s = g(o, filter=a.shadow(18, 10, shadow))
    holes = ""
    for i in range(n + 1):
        xx = x + i * w / n
        holes += C(xx, y - r * 0.35, r * 0.28, dk(edge, 0.08)) + C(xx, y + h + r * 0.35, r * 0.28, dk(edge, 0.08))
    for j in range(m + 1):
        yy = y + j * h / m
        holes += C(x - r * 0.35, yy, r * 0.28, dk(edge, 0.08)) + C(x + w + r * 0.35, yy, r * 0.28, dk(edge, 0.08))
    return s + holes


# ------------------------------------------------------------------ 1 lavender night, hanging palna
def card1():
    a = Art(111)
    b = R(0, 0, W, H, a.lg([(0, "#E9E1F7"), (0.55, "#CDBDEB"), (1, "#A995D6")]))
    b += C(540, 300, 480, a.rg([(0, "#FFFFFF", 0.55), (1, "#FFFFFF", 0)]))
    b += twinkles(a, 60, (10, 10, W - 10, 520), "#FFFFFF", (4, 12), seed=2, avoid=[(220, 0, 860, 520)])
    b += pastel_sky_clouds(a, ["#FFFFFF", "#F4EEFF"], seed=3, box=(40, 380, 1040, 470), n=4, avoid=[(260, 300, 820, 520)])
    b += lullaby_moon(a, 140, 170, 95, "#FFE7A3", rot=-10)
    for (x, ln, r, c) in [(880, 60, 22, "#FFE08A"), (960, 140, 16, "#FFFFFF"), (1030, 70, 18, "#FFD6E7")]:
        b += hanging_star(a, x, 0, ln, r, c, string="#FFFFFF")
    b += palna_hanging(a, 540, 30, 450, 560, wood="#E9B97A", cloth="#F9D5E0", rope="#F2D49A")
    # panel
    b += R(90, 505, 900, 755, "#FFFCF6", 40, filter=a.shadow(22, 12, 0.22))
    b += R(110, 525, 860, 715, "none", 30, stroke="#B79CE0", stroke_width=2.5)
    b += R(122, 537, 836, 691, "none", 24, stroke="#E7C98A", stroke_width=1.2)
    for x in (110, 970):
        for y in (525, 1240):
            b += flower5(a, x, y, 22, "#F6C1D6", center="#F6C343")
    zone = [150, 540, 930, 1240]
    return a.svg(b), spec(1, zone, "#6A3FA0", "#2E2340", "#B0567E", tfont="script")


# ------------------------------------------------------------------ 2 peach, arch photo with feathers
def card2():
    a = Art(222)
    b = R(0, 0, W, H, a.lg([(0, "#FFF1E6"), (1, "#FFD9C2")]))
    b += R(0, 0, W, H, a.pattern(64, 64, footprint(a, 20, 22, 20, "#F6B99B", 0) + footprint(a, 44, 50, 20, "#F6B99B", 0, left=True)), opacity=0.22)
    ph = {"shape": "arch", "x": 390, "y": 55, "w": 300, "h": 360}
    x, y, w, h = ph["x"], ph["y"], ph["w"], ph["h"]
    # feathers flanking
    b += peacock_feather(a, 330, 470, 400, -28, seed=1)
    b += peacock_feather(a, 750, 470, 400, 28, seed=2)
    b += peacock_feather(a, 260, 470, 300, -55, seed=3)
    b += peacock_feather(a, 820, 470, 300, 55, seed=4)
    arch = "M%d,%d L%d,%d A%d,%d 0 0 1 %d,%d L%d,%dZ"
    b += P(arch % (x - 22, y + h + 16, x - 22, y + w / 2, w / 2 + 22, w / 2 + 22, x + w + 22, y + w / 2, x + w + 22, y + h + 16), gold(a), filter=a.shadow(14, 10, 0.3))
    b += P(arch % (x - 10, y + h + 6, x - 10, y + w / 2, w / 2 + 10, w / 2 + 10, x + w + 10, y + w / 2, x + w + 10, y + h + 6), "#FFFFFF")
    b += P(arch % (x, y + h, x, y + w / 2, w / 2, w / 2, x + w, y + w / 2, x + w, y + h), a.lg([(0, "#FFF6EF"), (1, "#FFE4D4")]))
    b += baby_silhouette(a, x + w / 2, y + h * 0.6, w * 0.45, "#F4B79A", 0.55)
    # flower garland over the arch
    fl = ""
    rnd = random.Random(2)
    for i in range(19):
        an = math.pi * (1 - i / 18.0)
        px, py = x + w / 2 + math.cos(an) * (w / 2 + 22), y + w / 2 - math.sin(an) * (w / 2 + 22)
        fl += leaf(a, px, py, 30, math.degrees(-an) + 90 + rnd.choice([-50, 50]), "#8CC084", vein=False)
    for i in range(19):
        an = math.pi * (1 - i / 18.0)
        px, py = x + w / 2 + math.cos(an) * (w / 2 + 22), y + w / 2 - math.sin(an) * (w / 2 + 22)
        fl += flower5(a, px, py, 16 if i % 2 else 12, ["#FFFFFF", "#F7A8B8", "#FFD58A"][i % 3], center="#F6C343", rot=i * 17)
    b += g(fl, filter=a.shadow(4, 3, 0.2))
    # panel
    b += R(90, 470, 900, 778, "#FFFDFA", 36, filter=a.shadow(22, 12, 0.2))
    b += R(108, 488, 864, 742, "none", 28, stroke="#E6A77F", stroke_width=2.5, stroke_dasharray="1 9", stroke_linecap="round")
    b += R(120, 500, 840, 718, "none", 22, stroke="#E8C27A", stroke_width=1.5)
    # footprints bottom corners
    b += footprint(a, 60, 1300, 44, "#E7A084", -15, left=True) + footprint(a, 110, 1265, 44, "#E7A084", 10)
    b += footprint(a, 970, 1265, 44, "#E7A084", -10, left=True) + footprint(a, 1020, 1300, 44, "#E7A084", 15)
    zone = [150, 520, 930, 1220]
    return a.svg(b), spec(2, zone, "#B4532A", "#3C2A22", "#2E7D6B", tfont="script", photo=ph)


# ------------------------------------------------------------------ 3 peacock fan, mint + gold
def card3():
    a = Art(333)
    b = R(0, 0, W, H, a.lg([(0, "#E6F6F1"), (1, "#BFE5DA")]))
    b += R(0, 0, W, H, a.pattern(120, 120, P("M60,0 C80,30 80,50 60,60 C40,50 40,30 60,0Z", "#FFFFFF", opacity=0.35) + C(0, 60, 3, "#8FCFBE", opacity=0.6)))
    # flower swag on top edge
    b += garland_flowers(a, -20, 20, 540, 30, 45, ["#FFFFFF", "#F7B8C8", "#FFE08A"], 18, 17, seed=3, leafc="#6FB08F")
    b += garland_flowers(a, 540, 30, 1100, 20, 45, ["#FFE08A", "#FFFFFF", "#F7B8C8"], 18, 17, seed=4, leafc="#6FB08F")
    # feather fans
    for i, an in enumerate([-60, -38, -16, 6, 28]):
        b += peacock_feather(a, 130, 1330, 470 - abs(an + 16) * 1.6, an, seed=10 + i)
    for i, an in enumerate([60, 38, 16, -6]):
        b += peacock_feather(a, 950, 1330, 420 - abs(an - 16) * 1.6, an, seed=20 + i)
    b += C(130, 1330, 30, gold(a)) + C(950, 1330, 26, gold(a))
    # rattle across
    b += rattle(a, 540, 1060, 150, 70, "#F7A8C4", "#9ED8C8")
    # silk plaque
    b += P("M100,120 L980,120 L980,880 Q540,920 100,880Z", "#FFFBF2", filter=a.shadow(22, 12, 0.22))
    b += P("M100,120 L980,120 L980,880 Q540,920 100,880Z", a.lg([(0, "#FFFFFF", 0.4), (0.5, "#FFFFFF", 0), (1, "#E9DCC0", 0.25)], 0, 0, 1, 0))
    b += P("M122,142 L958,142 L958,860 Q540,898 122,860Z", "none", stroke=gold(a), stroke_width=3)
    b += R(100, 120, 880, 26, gold(a, False))
    zone = [150, 200, 930, 820]
    zone = [150, 165, 930, 865]
    return a.svg(b), spec(3, zone, "#1D6B5A", "#243B35", "#9A6A18", tfont="classic")


# ------------------------------------------------------------------ 4 blush, wooden palna stand
def card4():
    a = Art(444)
    b = R(0, 0, W, H, a.lg([(0, "#FDEEF2"), (1, "#F7CCD8")]))
    b += R(0, 0, W, H, dots_pattern(a, "#FFFFFF", 44, 4, 0.7))
    b += C(540, 1080, 520, a.rg([(0, "#FFFFFF", 0.7), (1, "#FFFFFF", 0)]))
    b += lace_panel(a, 110, 60, 860, 700, "#FFFDFB", "#FFFFFF", 16)
    b += R(140, 90, 800, 640, "none", 18, stroke="#E7A3B8", stroke_width=2, stroke_dasharray="10 7")
    b += E(540, 1255, 420, 22, "#B96A80", opacity=0.25, filter=a.blur(8))
    b += palna_stand(a, 540, 1250, 720, 450, wood="#C48A52", cloth="#FBE3EA", garl=("#FFFFFF", "#F7A8C0", "#FFE08A"))
    b += zzz(a, 560, 950, 18, "#B08BD9")
    # footprints either side
    b += footprint(a, 70, 1180, 60, "#E79AB2", -12, left=True) + footprint(a, 120, 1110, 60, "#E79AB2", 8)
    b += footprint(a, 960, 1110, 60, "#9CC7E8", -8, left=True) + footprint(a, 1010, 1180, 60, "#9CC7E8", 12)
    zone = [150, 95, 930, 725]
    zone = [150, 75, 930, 775]
    return a.svg(b), spec(4, zone, "#A3234F", "#3A2530", "#8A5A2B", tfont="classic")


# ------------------------------------------------------------------ 5 sky blue crib mobile with photo
def card5():
    a = Art(555)
    b = R(0, 0, W, H, a.lg([(0, "#DCEFFD"), (1, "#B7DAF5")]))
    b += pastel_sky_clouds(a, ["#FFFFFF", "#F2F9FF"], seed=5, box=(20, 60, 1060, 1320), n=10, avoid=[(90, 480, 990, 1250), (330, 60, 750, 450)])
    b += twinkles(a, 40, (10, 10, W - 10, H - 10), "#FFFFFF", (4, 12), avoid=[(90, 480, 990, 1250)], seed=6)
    # mobile
    wood = a.lg([(0, "#E9C89A"), (1, "#C09060")])
    b += P("M540,0 L540,70", stroke="#C09060", stroke_width=6)
    b += P("M150,110 Q540,40 930,110", stroke=wood, stroke_width=10, stroke_linecap="round")
    b += C(540, 72, 12, gold(a))
    hangs = [(170, 140, "moon"), (300, 220, "star"), (780, 220, "star"), (910, 140, "cloud")]
    for (x, ln, kind) in hangs:
        ytop = 110 - (1 - abs(x - 540) / 390.0) * 30
        b += P("M%d,%.1f L%d,%.1f" % (x, ytop, x, ytop + ln), stroke="#FFFFFF", stroke_width=2)
        yy = ytop + ln
        if kind == "moon":
            b += crescent(a, x, yy + 50, 52, "#FFE08A", 0.55)
        elif kind == "star":
            b += star(x, yy + 30, 34, a.rg([(0, "#FFF6CC"), (1, "#F7C948")]), r2=17, stroke="#FFFFFF", stroke_width=3, stroke_linejoin="round", filter=a.shadow(4, 3, 0.2))
        else:
            b += cloud(a, x, yy + 70, 36, "#FFFFFF") + P("M%d,%d l0,40" % (x - 20, yy + 70), stroke="#9CC7E8", stroke_width=3, stroke_dasharray="2 7", stroke_linecap="round") + P("M%d,%d l0,30" % (x + 16, yy + 70), stroke="#9CC7E8", stroke_width=3, stroke_dasharray="2 7", stroke_linecap="round")
    # photo in the middle as the mobile's centrepiece
    cx, cy, r = 540, 265, 135
    b += P("M540,70 L540,%d" % (cy - r - 26), stroke="#FFFFFF", stroke_width=3)
    rays = ""
    for i in range(16):
        an = i * 22.5
        rays += E(cx, cy - r - 22, 16, 30, a.lg([(0, "#FFE9A6"), (1, "#F7C948")]), transform="rotate(%.1f %d %d)" % (an, cx, cy))
    b += g(rays, filter=a.shadow(6, 4, 0.2))
    b += C(cx, cy, r + 16, gold(a), filter=a.shadow(10, 6, 0.25))
    b += C(cx, cy, r + 6, "#FFFFFF")
    b += C(cx, cy, r, a.lg([(0, "#F4FAFF"), (1, "#DDEEFB")]))
    b += baby_silhouette(a, cx, cy + r * 0.1, r * 0.9, "#A9CBEA", 0.6)
    # cloud-top panel
    cp = "M90,560 C90,500 160,470 210,500 C240,440 340,440 370,490 C410,430 520,430 550,490 C590,430 700,440 720,495 C760,450 860,460 870,510 C930,480 990,520 990,570 L990,1210 Q990,1250 950,1250 L130,1250 Q90,1250 90,1210Z"
    b += P(cp, "#FFFFFF", filter=a.shadow(22, 12, 0.18))
    b += R(118, 560, 844, 664, "none", 24, stroke="#9CC7E8", stroke_width=2.5, stroke_dasharray="12 8")
    zone = [150, 515, 930, 1215]
    return a.svg(b), spec(5, zone, "#23609E", "#243447", "#C0507A", tfont="script",
                          photo={"shape": "circle", "x": cx, "y": cy, "r": r})


# ------------------------------------------------------------------ 6 footprints in rose-gold
def card6():
    a = Art(666)
    b = R(0, 0, W, H, a.lg([(0, "#FFF7F2"), (1, "#F9E3DA")]))
    b += R(0, 0, W, H, a.noise(0.05, 0.8))
    rg_ = a.lg([(0, "#B76E5A"), (0.3, "#F6C6B2"), (0.55, "#D18D78"), (0.8, "#FBE0D4"), (1, "#A9604D")], 0, 0, 1, 1)
    # halo + laurel
    b += C(540, 250, 250, a.rg([(0, "#FFFFFF", 0.95), (1, "#FFFFFF", 0)]))
    lau = ""
    for side in (-1, 1):
        for i in range(14):
            t = i / 13.0
            an = math.radians(110 + t * 140) if side == -1 else math.radians(70 - t * 140)
            px, py = 540 + math.cos(an) * 215, 260 + math.sin(an) * 205
            deg = math.degrees(an) + (90 if side == 1 else -90)
            lau += leaf(a, px, py, 42 - t * 12, deg + side * 30, "#9CBF9A", vein=False)
            if i % 3 == 1:
                lau += C(px + side * 8, py, 6, "#F7B8C8")
    b += g(lau, filter=a.shadow(3, 2, 0.15))
    b += g(footprint(a, 470, 265, 250, rg_, -10, left=True) + footprint(a, 610, 245, 250, rg_, 10), filter=a.shadow(10, 6, 0.25))
    b += twinkles(a, 26, (300, 60, 780, 470), "#FFFFFF", (6, 16), seed=7, avoid=[(390, 110, 690, 400)])
    # tiny footprint trail along the bottom
    for i, x in enumerate(range(60, 330, 64)):
        b += footprint(a, x, 1300 - (i % 2) * 26, 30, "#E3A99A", 80, left=i % 2 == 0)
    for i, x in enumerate(range(780, 1060, 64)):
        b += footprint(a, x, 1300 - (i % 2) * 26, 30, "#E3A99A", 80, left=i % 2 == 0)
    # panel with ornamental corners
    b += R(90, 478, 900, 770, "#FFFFFF", 30, filter=a.shadow(22, 12, 0.18))
    b += R(110, 498, 860, 730, "none", 20, stroke=rg_, stroke_width=3)
    for (x, y, rot) in [(110, 498, 0), (970, 498, 90), (970, 1228, 180), (110, 1228, 270)]:
        orn = P("M0,0 Q60,0 70,40 Q30,16 0,70 Q0,30 0,0Z", rg_) + C(22, 22, 7, rg_)
        b += g(orn, "translate(%d %d) rotate(%d)" % (x, y, rot))
    zone = [150, 515, 930, 1218]
    return a.svg(b), spec(6, zone, "#9C4A3A", "#3B2A27", "#9C4A3A", tfont="script")


# ------------------------------------------------------------------ 7 mint toys shelf
def card7():
    a = Art(777)
    b = R(0, 0, W, H, a.lg([(0, "#EAF7EF"), (1, "#CBEBD9")]))
    b += R(0, 0, W, H, a.pattern(80, 80, star(20, 20, 7, "#FFFFFF", opacity=0.8) + crescent(a, 60, 60, 7, "#FFFFFF", 0.5)))
    # panel (quilted)
    b += R(90, 45, 900, 790, "#FFFEFA", 36, filter=a.shadow(22, 12, 0.2))
    b += R(90, 45, 900, 790, "none", 36, stroke="#F7B8C8", stroke_width=10)
    b += R(112, 67, 856, 746, "none", 26, stroke="#9ED8C8", stroke_width=2.5, stroke_dasharray="8 8")
    # shelf
    b += R(40, 1175, 1000, 26, a.lg([(0, "#E3BD8B"), (1, "#B8864E")]), 8, filter=a.shadow(10, 8, 0.25))
    b += P("M120,1201 L150,1250 L170,1201Z M960,1201 L930,1250 L910,1201Z", "#B8864E")
    # toys
    b += stack_rings(a, 190, 1178, 280)
    b += toy_block(a, 380, 1075, 100, "#F7A8C0", "star") + toy_block(a, 500, 1075, 100, "#A9C8F0", "moon") + toy_block(a, 440, 975, 100, "#FFD58A", "heart")
    b += rattle(a, 720, 1030, 190, -20, "#C9B3F0", "#F7B8C8")
    # wooden rocking duck toy (simple pull toy)
    dk_ = ""
    dk_ += E(900, 1100, 70, 48, a.rg([(0, "#FFF0B0"), (1, "#F7C948")], 0.4, 0.3, 0.8))
    dk_ += C(940, 1040, 36, a.rg([(0, "#FFF0B0"), (1, "#F7C948")], 0.4, 0.3, 0.8))
    dk_ += P("M970,1040 L1004,1048 L972,1058Z", "#FF9F43") + C(950, 1032, 5, "#3A2A20")
    dk_ += P("M860,1090 Q880,1070 910,1092", stroke="#E0A92E", stroke_width=5, stroke_linecap="round")
    dk_ += C(870, 1150, 20, "#C48A52") + C(930, 1150, 20, "#C48A52") + C(870, 1150, 7, "#8A5A2B") + C(930, 1150, 7, "#8A5A2B")
    b += g(dk_, filter=a.shadow(6, 5, 0.2))
    b += peacock_feather(a, 610, 1175, 260, 30, seed=7)
    # hanging bunting of stars above panel? no: little stars at top corners
    zone = [150, 95, 930, 795]
    return a.svg(b), spec(7, zone, "#1F6B4F", "#2A3530", "#C0507A", tfont="classic")


# ------------------------------------------------------------------ 8 baby asleep on the moon (dark)
def card8():
    a = Art(888)
    b = R(0, 0, W, H, a.lg([(0, "#1B2550"), (0.6, "#2B2F6B"), (1, "#3E3478")]))
    b += C(540, 280, 480, a.rg([(0, "#8C7AE6", 0.35), (1, "#8C7AE6", 0)]))
    b += twinkles(a, 110, (10, 10, W - 10, H - 10), "#FFF3C4", (3, 12), seed=8, avoid=[(90, 500, 990, 1250)])
    # hanging stars from top
    for (x, ln, r, c) in [(120, 90, 24, "#FFE08A"), (230, 170, 18, "#FFFFFF"), (850, 160, 20, "#FFD6E7"), (960, 80, 26, "#FFE08A")]:
        b += hanging_star(a, x, 0, ln, r, c, string="#C9C3F0")
    # moon cradle
    mx, my, mr = 540, 250, 200
    b += C(mx, my, mr * 1.6, a.rg([(0, "#FFE7A3", 0.35), (1, "#FFE7A3", 0)]))
    m = a.mask(R(0, 0, 1080, 1350, "#000") + C(mx, my, mr, "#FFF") + C(mx, my - mr * 0.62, mr * 0.86, "#000"))
    b += g(C(mx, my, mr, a.rg([(0, "#FFF6D6"), (0.6, "#FFE7A3"), (1, "#E9C46A")], 0.4, 0.8, 0.8)) + C(mx - 60, my + 150, 14, "#E9C46A", opacity=0.6) + C(mx + 90, my + 120, 9, "#E9C46A", opacity=0.6), mask=m, filter=a.shadow(16, 10, 0.3))
    s = mr * 0.19
    b += sleeping_baby(a, mx - mr * 0.42, my + mr * 0.2 - s * 1.05, s, cap="#BFD9F5", blanket="#F7C6D9")
    b += zzz(a, mx + mr * 0.55, my - mr * 0.15, 16, "#FFF3C4")
    b += pastel_sky_clouds(a, ["#E7E3FF", "#FFFFFF"], seed=4, box=(330, 430, 750, 470), n=3)
    b += cloud(a, 330, 455, 60, "#E9E4FF") + cloud(a, 760, 460, 70, "#F4F1FF")
    # glass panel
    b += R(90, 495, 900, 755, "#101838", 34, opacity=0.62, filter=a.shadow(20, 10, 0.3))
    b += R(108, 513, 864, 719, "none", 26, stroke="#FFE7A3", stroke_width=2, opacity=0.8)
    for (x, y) in [(108, 513), (972, 513), (108, 1232), (972, 1232)]:
        b += star(x, y, 14, "#FFE7A3", r2=6)
    zone = [150, 530, 930, 1230]
    return a.svg(b), spec(8, zone, "gold", "#F6F2FF", "#FFD6E7", tone="dark", tfont="script")


# ------------------------------------------------------------------ 9 photo oval at bottom, feathers + wreath
def card9():
    a = Art(999)
    b = R(0, 0, W, H, a.lg([(0, "#FFFBEA"), (1, "#FCEBC0")]))
    b += R(0, 0, W, H, a.pattern(100, 100, P("M50,20 Q60,50 50,80 Q40,50 50,20Z", "#EBCB7A", opacity=0.25)))
    # panel on top
    b += P("M100,40 L980,40 L980,800 C760,800 700,860 540,860 C380,860 320,800 100,800Z", "#FFFFFF", filter=a.shadow(20, 10, 0.18))
    b += P("M122,62 L958,62 L958,780 C750,780 690,838 540,838 C390,838 330,780 122,780Z", "none", stroke=gold(a), stroke_width=2.5)
    # photo oval
    ph = {"shape": "oval", "x": 410, "y": 885, "w": 260, "h": 320}
    cx, cy = ph["x"] + ph["w"] / 2, ph["y"] + ph["h"] / 2
    b += peacock_feather(a, cx - 40, cy + 170, 420, -58, seed=5)
    b += peacock_feather(a, cx + 40, cy + 170, 420, 58, seed=6)
    b += peacock_feather(a, cx - 20, cy + 180, 330, -78, seed=7)
    b += peacock_feather(a, cx + 20, cy + 180, 330, 78, seed=8)
    # wreath
    wr = ""
    rnd = random.Random(9)
    for i in range(36):
        an = math.radians(i * 10)
        px, py = cx + math.cos(an) * (ph["w"] / 2 + 26), cy + math.sin(an) * (ph["h"] / 2 + 26)
        wr += leaf(a, px, py, 34, i * 10 + rnd.choice([30, 150]), "#86B97A", vein=False)
    for i in range(18):
        an = math.radians(i * 20 + 5)
        px, py = cx + math.cos(an) * (ph["w"] / 2 + 24), cy + math.sin(an) * (ph["h"] / 2 + 24)
        wr += flower5(a, px, py, 15, ["#FFFFFF", "#F7B8C8", "#FFD58A"][i % 3], center="#F6C343", rot=i * 13)
    b += g(wr, filter=a.shadow(4, 3, 0.2))
    b += E(cx, cy, ph["w"] / 2 + 8, ph["h"] / 2 + 8, gold(a))
    b += E(cx, cy, ph["w"] / 2, ph["h"] / 2, a.lg([(0, "#FFF8EE"), (1, "#FCE8D8")]))
    b += baby_silhouette(a, cx, cy + 30, 120, "#EBC3A5", 0.6)
    zone = [150, 90, 930, 790]
    return a.svg(b), spec(9, zone, "#8A5A12", "#35291C", "#1D6B5A", tfont="classic", photo=ph)


# ------------------------------------------------------------------ 10 lemon, bead-frame photo + toys
def card10():
    a = Art(1010)
    b = R(0, 0, W, H, a.lg([(0, "#FFF9DE"), (1, "#FFEBB0")]))
    b += R(0, 0, W, H, a.pattern(90, 90, C(22, 22, 12, "#FFFFFF", opacity=0.6) + C(67, 67, 7, "#FFFFFF", opacity=0.6)))
    ph = {"shape": "rounded", "x": 380, "y": 55, "w": 320, "h": 330}
    x, y, w, h = ph["x"], ph["y"], ph["w"], ph["h"]
    # wooden frame
    b += R(x - 34, y - 34, w + 68, h + 68, a.lg([(0, "#F0CF9C"), (1, "#C99A5E")]), 40, filter=a.shadow(14, 10, 0.3))
    beads = ["#F7A8C0", "#A9C8F0", "#A8DCC8", "#FFD58A", "#C9B3F0"]
    k = 0
    per = [(x - 17 + i * (w + 34) / 10, y - 17) for i in range(11)] + [(x + w + 17, y - 17 + i * (h + 34) / 10) for i in range(1, 11)] + \
          [(x + w + 17 - i * (w + 34) / 10, y + h + 17) for i in range(1, 11)] + [(x - 17, y + h + 17 - i * (h + 34) / 10) for i in range(1, 10)]
    for (px, py) in per:
        c = beads[k % 5]; k += 1
        b += C(px, py, 14, a.rg([(0, lt(c, 0.5)), (1, dk(c, 0.1))], 0.35, 0.3, 0.8))
    b += R(x, y, w, h, a.lg([(0, "#FFFDF2"), (1, "#FFF1C9")]), 26)
    b += baby_silhouette(a, x + w / 2, y + h * 0.58, w * 0.45, "#EBCB7A", 0.6)
    # toys flanking photo
    b += toy_block(a, 90, 300, 90, "#A9C8F0", "star") + toy_block(a, 190, 300, 90, "#F7A8C0", "heart") + toy_block(a, 140, 210, 90, "#A8DCC8", "moon")
    b += stack_rings(a, 900, 400, 220)
    b += rattle(a, 260, 120, 120, -35, "#FFB3C7", "#A8DCC8")
    b += rattle(a, 830, 110, 110, 40, "#A9C8F0", "#FFD58A")
    # panel
    b += lace_panel(a, 100, 470, 880, 770, "#FFFFFF", "#FFFFFF", 14, 0.18)
    b += R(126, 496, 828, 718, "none", 20, stroke="#E8B64C", stroke_width=2)
    b += R(136, 506, 808, 698, "none", 16, stroke="#F7A8C0", stroke_width=1.2, stroke_dasharray="6 6")
    zone = [150, 520, 930, 1220]
    return a.svg(b), spec(10, zone, "#9A5B00", "#3A2C1A", "#B0406E", tfont="script", photo=ph)


CARDS = [card1, card2, card3, card4, card5, card6, card7, card8, card9, card10]

if __name__ == "__main__":
    only = [int(x) for x in sys.argv[1:]]
    arts, specs = {}, []
    for i, fn in enumerate(CARDS, 1):
        svg, sp = fn()
        specs.append(sp)
        if not only or i in only:
            arts[sp["id"]] = svg
    check_spec(specs, True)
    write_spec(CAT, specs)
    render_cards(arts)
