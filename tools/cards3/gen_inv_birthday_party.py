"""Birthday-party invitations: kids' themes, bunting, poppers, ticket, disco. No cake-hero / balloon-bouquet."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_e import *
from render import render_cards

CAT = "inv-birthday-party"


def spec(n, zone, title, text, accent, tone="light", tfont="deco", align="center", photo=None):
    d = {"id": "E-%s-%d" % (CAT, n), "tpl": True, "zone": zone,
         "colors": {"title": title, "text": text, "accent": accent},
         "tone": tone, "title": tfont, "align": align}
    if photo:
        d["photo"] = photo
        d["slot"] = True
    return d


def glass(a, x, y, w, h, fill="#0B0F2A", op=0.62, rx=36, line=None):
    s = R(x, y, w, h, fill, rx, opacity=op, filter=a.shadow(24, 12, 0.35))
    if line:
        s += R(x + 14, y + 14, w - 28, h - 28, "none", rx - 10, stroke=line, stroke_width=2, opacity=0.85)
    return s


# ------------------------------------------------------------------ 1 space launch
def card1():
    a = Art(101)
    b = R(0, 0, W, H, a.lg([(0, "#0A0E2E"), (0.55, "#1C1553"), (1, "#3B1B6B")]))
    b += C(820, 1100, 700, a.rg([(0, "#8E3BD1", 0.45), (1, "#8E3BD1", 0)]))
    b += C(150, 250, 500, a.rg([(0, "#2F6BD6", 0.35), (1, "#2F6BD6", 0)]))
    b += twinkles(a, 150, (10, 10, W - 10, H - 10), "#FFFFFF", (3, 11), seed=3, op=(0.4, 1))
    b += twinkles(a, 30, (10, 10, W - 10, H - 10), "#FFD36B", (6, 14), seed=4)
    # shooting star
    b += P("M760,70 L990,20", stroke=a.lg([(0, "#FFFFFF", 0), (1, "#FFFFFF", 0.9)], 0, 0, 1, 0), stroke_width=4, stroke_linecap="round") + sparkle(990, 20, 16, "#FFFFFF")
    # planets
    b += planet(a, 170, 1060, 120, "#F28C5B", ring="#F7D18A", tilt=-20, seed=2)
    b += planet(a, 460, 1190, 44, "#5BC0EB", seed=3)
    b += planet(a, 1010, 900, 36, "#F25F9A", seed=5)
    # smoke clouds bottom right
    b += g(smoke_puffs(a, 900, 1300, 460, 18, seed=5, col="#F4F1FF", shade="#B9B2D9"), filter=a.shadow(10, -4, 0.2))
    b += rocket(a, 830, 1040, 420, 28, body="#F5F7FF", nose="#FF4D6D", fin="#FF4D6D", win="#6FE3FF")
    b += g(smoke_puffs(a, 700, 1330, 260, 10, seed=6, col="#FFFFFF", shade="#C9C3E6"))
    # panel
    b += glass(a, 100, 50, 880, 800, "#070A24", 0.6, 40, line="#FFD36B")
    for (x, y) in [(114, 64), (966, 64), (114, 836), (966, 836)]:
        b += star(x, y, 16, gold(a), r2=6)
    zone = [150, 95, 930, 805]
    return a.svg(b), spec(1, zone, "gold", "#F4F2FF", "#FFD36B", tone="dark", tfont="deco")


# ------------------------------------------------------------------ 2 jungle safari
def card2():
    a = Art(202)
    b = R(0, 0, W, H, a.lg([(0, "#F3F7E4"), (0.6, "#E3EFC8"), (1, "#C9DFA0")]))
    b += R(0, 0, W, H, a.pattern(90, 90, leaf(a, 45, 60, 26, 30, "#9FC47A", vein=False)), opacity=0.25)
    # back leaves
    lv = ""
    lv += monstera(a, 40, 200, 260, 135, "#2E8B57", seed=1)
    lv += monstera(a, 1060, 180, 250, -130, "#3C9A5F", seed=2)
    lv += palm_leaf(a, 0, 40, 300, 120, "#4CAF50")
    lv += palm_leaf(a, 1080, 60, 300, -115, "#43A047", curl=-0.25)
    b += lv
    # ground
    b += P("M0,1120 C240,1060 420,1120 560,1100 C760,1070 900,1110 1080,1080 L1080,1350 L0,1350Z", a.lg([(0, "#9CC46A"), (1, "#6E9E43")]))
    b += palm_leaf(a, 60, 1350, 330, 30, "#2F8F46") + palm_leaf(a, 1030, 1350, 300, -35, "#2F8F46", curl=-0.25)
    b += monstera(a, 440, 1350, 180, -20, "#2E7D4F", seed=3)
    # giraffe right
    b += giraffe(a, 900, 1350, 400, 0.95)
    # lion left
    b += lion(a, 225, 1105, 105)
    # grass tufts
    rnd = random.Random(4)
    gr = ""
    for x in list(range(20, 330, 26)) + list(range(760, 1070, 26)):
        h = rnd.uniform(30, 60)
        gr += P("M%d,1350 Q%d,%d %d,%d" % (x, x + 4, 1350 - h / 2, x + rnd.uniform(-14, 14), 1350 - h), stroke=rnd.choice(["#4E8A2E", "#6FAE3F", "#3E7A26"]), stroke_width=6, stroke_linecap="round")
    b += gr
    # signboard
    wood = a.lg([(0, "#A86B3C"), (0.5, "#8A5230"), (1, "#6E3F22")])
    b += R(96, 70, 888, 790, wood, 34, filter=a.shadow(22, 12, 0.35))
    b += R(96, 70, 888, 790, a.pattern(200, 26, P("M0,13 C60,6 120,20 200,12", stroke="#5A3218", stroke_width=2, opacity=0.35)), 34)
    b += R(122, 96, 836, 738, a.lg([(0, "#FFF9E8"), (1, "#F6ECCF")]), 22)
    b += R(136, 110, 808, 710, "none", 16, stroke="#6E9E43", stroke_width=2.5, stroke_dasharray="14 8")
    for (x, y) in [(118, 92), (962, 92), (118, 838), (962, 838)]:
        b += C(x, y, 9, metal(a, "#C9B28A")) + C(x - 2, y - 2, 3, "#FFFFFF", opacity=0.6)
    # toucan on the sign
    b += toucan(a, 890, 22, 70, flip=True)
    b += leaf(a, 150, 96, 60, -60, "#43A047") + leaf(a, 160, 90, 50, -20, "#66BB6A") + leaf(a, 930, 848, 60, 150, "#43A047")
    zone = [150, 120, 930, 820]
    return a.svg(b), spec(2, zone, "#2E6B1F", "#3B2A1A", "#A0521D", tfont="deco")


# ------------------------------------------------------------------ 3 under the sea
def card3():
    a = Art(303)
    b = R(0, 0, W, H, a.lg([(0, "#9EE9F2"), (0.35, "#3CC0D8"), (1, "#0D5C8C")]))
    # light rays
    rays = ""
    for i, x in enumerate([120, 330, 560, 760, 960]):
        rays += P(poly([(x - 40, 0), (x + 40, 0), (x + 180 + i * 10, H), (x + 20, H)]), "#FFFFFF", opacity=0.07)
    b += rays
    b += bubbles(a, 45, (20, 20, W - 20, H - 60), seed=4, avoid=[(100, 430, 980, 1220), (620, 70, 980, 400)], rr=(5, 22))
    # sand floor
    b += P("M0,1210 C200,1170 360,1230 540,1215 C720,1200 880,1170 1080,1200 L1080,1350 L0,1350Z", a.lg([(0, "#F7E3B5"), (1, "#E0BE82")]))
    b += R(0, 1190, W, 160, dots_pattern(a, "#C9A266", 22, 2, 0.5))
    b += seaweed(a, 50, 1300, 420, "#2FA36B", seed=1) + seaweed(a, 1030, 1300, 460, "#27966A", seed=2)
    b += coral(a, 150, 1300, 300, "#FF7F7F", seed=3) + coral(a, 930, 1300, 280, "#FF9ACB", seed=4)
    b += starfish(a, 250, 1290, 34, "#FF9F43", 12) + starfish(a, 850, 1300, 28, "#FF6B81", -10)
    # shells
    b += P("M1000,1320 q20,-40 40,0Z", "#FFD6E0") + P("M60,1330 q16,-34 32,0Z", "#FFE9C9")
    # whale top-left
    b += whale(a, 290, 270, 175, "#3F7FD9")
    # photo bubble
    cx, cy, r = 800, 230, 140
    b += C(cx, cy, r + 22, a.rg([(0, "#FFFFFF", 0.0), (0.8, "#FFFFFF", 0.25), (1, "#FFFFFF", 0.7)]), filter=a.shadow(14, 8, 0.2))
    b += C(cx, cy, r + 10, "none", stroke="#FFFFFF", stroke_width=6)
    b += C(cx, cy, r, a.lg([(0, "#E6FBFF"), (1, "#BDEFF7")]))
    b += kid_silhouette(a, cx, cy, r, "#7CCBDA", 0.5)
    b += P("M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f" % (cx - r - 14, cy - 30, r + 14, r + 14, cx - 30, cy - r - 14), stroke="#FFFFFF", stroke_width=9, stroke_linecap="round", opacity=0.8)
    b += bubbles(a, 5, (cx + 100, cy + r - 40, cx + 170, cy + r + 20), seed=9, rr=(6, 14))
    # fish
    b += fish(a, 60, 520, 70, "#FF8C1A", stripes="#FFFFFF", ang=-8)
    b += fish(a, 1030, 700, 60, "#FFD23F", ang=6, face_left=True)
    b += fish(a, 70, 900, 50, "#B388FF", ang=4)
    b += fish(a, 1020, 1060, 52, "#FF6FA8", stripes="#FFE3EE", face_left=True)
    # glass panel
    b += R(100, 425, 880, 790, "#FFFFFF", 44, opacity=0.86, filter=a.shadow(24, 12, 0.3))
    b += R(118, 443, 844, 754, "none", 32, stroke="#3CC0D8", stroke_width=3, stroke_dasharray="2 12", stroke_linecap="round")
    # wave crest on top of panel
    wv = "M100,470 " + " ".join("q%d,-26 %d,0" % (55, 110) for _ in range(8))
    b += P(wv, stroke="#7FDBEA", stroke_width=5, fill="none", opacity=0.8)
    zone = [150, 475, 930, 1180]
    return a.svg(b), spec(3, zone, "#0B5A8A", "#133247", "#D2582B", tfont="deco",
                          photo={"shape": "circle", "x": cx, "y": cy, "r": r})


# ------------------------------------------------------------------ 4 circus big top
def card4():
    a = Art(404)
    b = R(0, 0, W, H, a.lg([(0, "#12264A"), (0.5, "#1B3A63"), (1, "#0E1D3A")]))
    # spotlight beams
    for (x0, x1, c) in [(-100, 380, "#FFE9A8"), (1180, 700, "#FFE9A8")]:
        b += P(poly([(x0, 0), (x0 + (60 if x0 < 0 else -60), 0), (x1 + 160, 520), (x1 - 160, 520)]), a.lg([(0, c, 0.35), (1, c, 0)]))
    b += twinkles(a, 60, (10, 10, W - 10, 480), "#FFF3C4", (3, 10), seed=5)
    # pennant strings from tent peak to corners
    b += bunting(a, 540, 70, 0, 380, 30, ["#FFD166", "#EF476F", "#06D6A0", "#118AB2"], 7, fw=44, fh=56, seed=1, shape="pen", string="#E8D6A8")
    b += bunting(a, 540, 70, 1080, 380, 30, ["#EF476F", "#FFD166", "#118AB2", "#06D6A0"], 7, fw=44, fh=56, seed=2, shape="pen", string="#E8D6A8")
    b += circus_tent(a, 540, 75, 255, 400, 430, cols=("#D7263D", "#FFF6E8"), n=14)
    # ground glow
    b += E(540, 440, 520, 40, "#000", opacity=0.3, filter=a.blur(12))
    # poster panel with striped border
    stripes = a.pattern(40, 40, R(0, 0, 20, 40, "#D7263D") + R(20, 0, 20, 40, "#FFF6E8"), "rotate(45)")
    b += R(90, 445, 900, 810, stripes, 30, filter=a.shadow(22, 12, 0.4))
    b += R(118, 473, 844, 754, "#FFF8EA", 18)
    b += R(118, 473, 844, 754, a.noise(0.04), 18)
    b += R(134, 489, 812, 722, "none", 12, stroke="#D4A13A", stroke_width=3)
    for (x, y) in [(134, 489), (946, 489), (134, 1211), (946, 1211)]:
        b += star(x, y, 18, gold(a), r2=7)
    zone = [150, 505, 930, 1210]
    return a.svg(b), spec(4, zone, "#B3122E", "#2B1A24", "#1B5E7A", tfont="deco")


# ------------------------------------------------------------------ 5 golden ticket + velvet curtain
def card5():
    a = Art(505)
    b = R(0, 0, W, H, a.lg([(0, "#2A0710"), (1, "#14030A")]))
    b += C(540, 700, 650, a.rg([(0, "#FFCF7A", 0.4), (1, "#FFCF7A", 0)]))
    b += curtain(a, -20, 240, 120, H, "#B3122E", "left", 0.78)
    b += curtain(a, 840, 1100, 120, H, "#B3122E", "right", 0.78)
    b += valance(a, -10, 1090, 30, 70, "#9E0F28", 5)
    # ticket
    tp = ticket_path(80, 230, 920, 1010, notch=0.1, cr=30)
    b += g(P(tp, a.lg([(0, "#FFE7A6"), (0.4, "#F6C96A"), (1, "#E0A93F")], 0, 0, 1, 1)), filter=a.shadow(26, 16, 0.5))
    b += P(ticket_path(98, 248, 884, 974, notch=0.1, cr=22), "#FFF8E6")
    b += P(ticket_path(98, 248, 884, 974, notch=0.1, cr=22), a.noise(0.035))
    b += P(ticket_path(132, 282, 816, 906, notch=0.1, cr=16), "none", stroke="#B3122E", stroke_width=3)
    # perforation
    b += P("M160,1090 L920,1090", stroke="#B3122E", stroke_width=4, stroke_dasharray="2 12", stroke_linecap="round")
    b += C(80, 1090, 22, "#1C050C") + C(1000, 1090, 22, "#1C050C")
    # stub ornament: row of stars
    for i, x in enumerate(range(260, 840, 90)):
        b += star(x, 1160, 20 if i % 2 else 26, "#B3122E" if i % 2 else gold(a), r2=9)
    # bulbs around ticket
    b += bulbs_rect(a, 115, 265, 965, 1060, 62, 7, "#FFE38A")
    # popcorn buckets at bottom corners
    for (x, flip) in [(95, 1), (985, -1)]:
        pc = ""
        pc += P(poly([(-60, -140), (60, -140), (44, 0), (-44, 0)]), a.pattern(40, 200, R(0, 0, 20, 200, "#E53935") + R(20, 0, 20, 200, "#FFFFFF")))
        pc += P(poly([(-60, -140), (60, -140), (44, 0), (-44, 0)]), a.lg([(0, "#000", 0.25), (0.4, "#000", 0), (1, "#000", 0.3)], 0, 0, 1, 0))
        rnd = random.Random(x)
        for k in range(22):
            px = rnd.uniform(-55, 55); py = -140 - rnd.uniform(0, 50) * (1 - abs(px) / 80)
            pc += C(px, py, rnd.uniform(12, 18), a.rg([(0, "#FFFFFF"), (0.7, "#FFF3C4"), (1, "#E8C170")]))
        b += g(pc, "translate(%d 1320) rotate(%d)" % (x, -8 * flip), filter=a.shadow(10, 8, 0.4))
    zone = [150, 320, 930, 1040]
    return a.svg(b), spec(5, zone, "#9E0F28", "#2A1410", "#9E0F28", tfont="classic")


# ------------------------------------------------------------------ 6 disco night
def card6():
    a = Art(606)
    b = R(0, 0, W, H, a.lg([(0, "#12051F"), (0.6, "#240A3D"), (1, "#0B0314")]))
    # beams
    cols = ["#FF3CAC", "#2BD2FF", "#FFE53B", "#7CFF6B", "#B266FF", "#FF7A3D"]
    for i, c in enumerate(cols):
        an = math.radians(40 + i * 20)
        ex, ey = 540 + math.cos(an) * 1500, 260 + math.sin(an) * 1500
        an2 = an + 0.09
        b += P(poly([(540, 260), (ex, ey), (540 + math.cos(an2) * 1500, 260 + math.sin(an2) * 1500)]), a.lg([(0, c, 0.55), (1, c, 0)], 0, 0, 0, 1), opacity=0.5)
    # dance floor
    fl = ""
    for j in range(5):
        y0 = 1110 + j * 50 * (1 + j * 0.2)
        y1 = 1110 + (j + 1) * 50 * (1 + (j + 1) * 0.2)
        for i in range(-6, 7):
            def xp(ii, yy):
                return 540 + ii * 90 * (1 + (yy - 1110) / 240.0)
            c = cols[(i + j) % len(cols)]
            fl += P(poly([(xp(i, y0), y0), (xp(i + 1, y0), y0), (xp(i + 1, y1), y1), (xp(i, y1), y1)]), a.lg([(0, c, 0.55), (1, dk(c, 0.5), 0.35)]), stroke="#0B0314", stroke_width=3)
    b += fl
    b += R(0, 1100, W, 250, a.lg([(0, "#12051F", 0.7), (0.3, "#12051F", 0)]))
    b += E(540, 1330, 330, 80, "#0B0314", opacity=0.75, filter=a.blur(20))
    b += twinkles(a, 70, (10, 10, W - 10, H - 10), "#FFFFFF", (3, 12), avoid=[(90, 460, 990, 1220)], seed=6)
    # chain + ball
    b += P("M540,0 L540,80", stroke="#AEB7C8", stroke_width=5, stroke_dasharray="8 4")
    b += g(disco_ball(a, 540, 250, 165, seed=3), filter=a.shadow(20, 10, 0.4))
    b += C(540, 250, 260, a.rg([(0, "#FFFFFF", 0.0), (0.64, "#FFFFFF", 0.0), (0.7, "#C9B8FF", 0.25), (1, "#C9B8FF", 0)]))
    # glass panel
    b += glass(a, 90, 450, 900, 790, "#140624", 0.72, 40)
    b += R(106, 466, 868, 758, "none", 30, stroke=a.lg([(0, "#FF3CAC"), (0.5, "#FFE53B"), (1, "#2BD2FF")], 0, 0, 1, 1), stroke_width=3)
    zone = [150, 490, 930, 1200]
    return a.svg(b), spec(6, zone, "gold", "#FBF4FF", "#FF7ACB", tone="dark", tfont="deco")


# ------------------------------------------------------------------ 7 bunting + poppers + rosette photo
def card7():
    a = Art(707)
    b = R(0, 0, W, H, a.lg([(0, "#FFE9A6"), (1, "#FFD166")]))
    rays = ""
    for i in range(24):
        an0 = math.radians(i * 15); an1 = math.radians(i * 15 + 7.5)
        rays += P(poly([(540, 300), (540 + math.cos(an0) * 1800, 300 + math.sin(an0) * 1800), (540 + math.cos(an1) * 1800, 300 + math.sin(an1) * 1800)]), "#FFFFFF", opacity=0.22)
    b += rays
    cols = ["#EF476F", "#118AB2", "#06D6A0", "#7B2FF7", "#FF8C42"]
    b += confetti(a, 90, (20, 20, W - 20, H - 20), cols, avoid=[(90, 470, 990, 1260), (360, 140, 720, 480)], seed=3, size=(10, 20))
    b += bunting(a, -20, 30, 1100, 30, 60, cols, 12, fw=78, fh=92, seed=1, string="#5A3E2B")
    b += bunting(a, -20, -14, 1100, -14, 100, cols[::-1], 14, fw=56, fh=66, seed=2, shape="pen", string="#5A3E2B")
    b += party_popper(a, 30, 440, -40, 140, cols, seed=3)
    b += party_popper(a, 1050, 440, -140, 140, cols, seed=4, cone=("#7B2FF7", "#FFD166"))
    cx, cy, r = 540, 280, 104
    b += rosette_badge(a, cx, cy, r, "#EF476F", "#FFD166")
    b += C(cx, cy, r, a.lg([(0, "#FFF6F8"), (1, "#FFE0E8")]))
    b += kid_silhouette(a, cx, cy, r, "#F4A6B8", 0.55)
    b += R(90, 480, 900, 778, "#FFFDF7", 34, filter=a.shadow(22, 12, 0.25))
    b += R(90, 480, 900, 778, dots_pattern(a, "#FFD166", 34, 3, 0.35), 34)
    b += R(112, 502, 856, 734, "#FFFDF7", 24)
    b += R(112, 502, 856, 734, "none", 24, stroke="#EF476F", stroke_width=3, stroke_dasharray="16 10")
    zone = [150, 525, 930, 1225]
    return a.svg(b), spec(7, zone, "#C2185B", "#2D2238", "#0E6E91", tfont="deco",
                          photo={"shape": "circle", "x": cx, "y": cy, "r": r})


# ------------------------------------------------------------------ 8 astronaut photo
def card8():
    a = Art(808)
    b = R(0, 0, W, H, a.lg([(0, "#1A0B3B"), (0.5, "#3A1464"), (1, "#5E1F6E")]))
    b += C(540, 250, 520, a.rg([(0, "#FF6FB5", 0.35), (1, "#FF6FB5", 0)]))
    b += C(950, 1150, 500, a.rg([(0, "#4CC9F0", 0.25), (1, "#4CC9F0", 0)]))
    b += twinkles(a, 140, (10, 10, W - 10, H - 10), "#FFFFFF", (3, 10), seed=8, avoid=[(90, 470, 990, 1250)])
    b += planet(a, 930, 150, 70, "#FFB347", ring="#FFE0A3", tilt=15, seed=9)
    b += planet(a, 140, 420, 44, "#4CC9F0", seed=10)
    b += rocket(a, 150, 150, 170, 40, body="#FFFFFF", nose="#FF4D8D", fin="#7B61FF", win="#6FE3FF")
    b += P("M40,300 Q120,250 180,190", stroke="#FFFFFF", stroke_width=3, stroke_dasharray="4 10", stroke_linecap="round", opacity=0.6)
    cx, cy, r = 540, 230, 112
    b += astronaut(a, cx, cy, r, trim="#FF6FB5", visor="#FFC75F")
    b += glass(a, 90, 470, 900, 780, "#120630", 0.66, 40, line="#FFC75F")
    zone = [150, 505, 930, 1215]
    return a.svg(b), spec(8, zone, "gold", "#FFF3FB", "#FFC75F", tone="dark", tfont="deco",
                          photo={"shape": "circle", "x": cx, "y": cy, "r": r})


# ------------------------------------------------------------------ 9 jungle arch photo
def card9():
    a = Art(909)
    b = R(0, 0, W, H, a.lg([(0, "#0F3B2A"), (0.6, "#155A3C"), (1, "#0B2F22")]))
    b += C(540, 250, 500, a.rg([(0, "#F4E6A0", 0.35), (1, "#F4E6A0", 0)]))
    # layered back leaves
    rnd = random.Random(9)
    for i in range(14):
        x = rnd.choice([rnd.uniform(-40, 200), rnd.uniform(880, 1120)]); y = rnd.uniform(0, 1350)
        b += g(monstera(a, x, y, rnd.uniform(160, 240), rnd.uniform(0, 360), rnd.choice(["#1F6B45", "#23794F", "#185C3B"]), seed=i), opacity=0.7)
    b += palm_leaf(a, 0, 1350, 420, 35, "#2E8B57") + palm_leaf(a, 1080, 1350, 420, -35, "#2E8B57", curl=-0.25)
    # arch frame (bamboo)
    ph = {"shape": "arch", "x": 385, "y": 55, "w": 310, "h": 360}
    x, y, w, h = ph["x"], ph["y"], ph["w"], ph["h"]
    arch = "M%d,%d L%d,%d A%d,%d 0 0 1 %d,%d L%d,%dZ" % (x - 26, y + h + 18, x - 26, y + w / 2 + 4, w / 2 + 26, w / 2 + 26, x + w + 26, y + w / 2 + 4, x + w + 26, y + h + 18)
    b += P(arch, a.lg([(0, "#E8C57A"), (0.5, "#C99A45"), (1, "#9C7128")], 0, 0, 1, 0), filter=a.shadow(16, 10, 0.4))
    for k in range(1, 6):
        yy = y + w / 2 + (h - w / 2) * k / 6
        b += R(x - 26, yy, 26, 6, "#8A6020") + R(x + w, yy, 26, 6, "#8A6020")
    inner = "M%d,%d L%d,%d A%d,%d 0 0 1 %d,%d L%d,%dZ" % (x, y + h, x, y + w / 2, w / 2, w / 2, x + w, y + w / 2, x + w, y + h)
    b += P(inner, a.lg([(0, "#FFF8DC"), (1, "#EEF6D8")]))
    b += kid_silhouette(a, x + w / 2, y + h * 0.58, w * 0.5, "#B7D39A", 0.6)
    # vines over the arch
    b += vine(a, 300, 40, 780, 40, 60, seed=3)
    b += vine(a, 345, 450, 360, 60, -40, seed=4)
    b += vine(a, 720, 60, 735, 450, 40, seed=5)
    b += monkey(a, 240, 60, 120)
    b += toucan(a, 820, 350, 90)
    # panel
    b += R(90, 462, 900, 792, "#FFF9E6", 36, filter=a.shadow(24, 12, 0.45))
    b += R(110, 482, 860, 752, "none", 26, stroke="#2E8B57", stroke_width=3)
    b += R(122, 494, 836, 728, "none", 20, stroke="#C99A45", stroke_width=1.5)
    b += leaf(a, 110, 482, 70, -45, "#2E8B57") + leaf(a, 110, 482, 60, -100, "#43A047") + leaf(a, 970, 1230, 70, 135, "#2E8B57") + leaf(a, 970, 1230, 60, 80, "#43A047")
    zone = [150, 510, 930, 1215]
    return a.svg(b), spec(9, zone, "#1F6B45", "#2A2418", "#A0521D", tfont="deco", photo=ph)


# ------------------------------------------------------------------ 10 tassel garland + hats + photo bottom
def card10():
    a = Art(1001)
    b = R(0, 0, W, H, a.lg([(0, "#FFE3EC"), (1, "#FFC9DA")]))
    b += R(0, 0, W, H, a.pattern(70, 70, R(30, 10, 6, 18, "#FFFFFF", 3, opacity=0.6) + C(10, 50, 4, "#FF9BB8", opacity=0.5)))
    cols = ["#FF4F8B", "#FFB400", "#3EC1D3", "#8E6CFF", "#FF7A45"]
    # tassel garland along top
    tg = P("M-10,30 Q540,90 1090,30", stroke="#B07A2E", stroke_width=3)
    for i in range(16):
        t = (i + 0.5) / 16
        px = (1 - t) ** 2 * -10 + 2 * (1 - t) * t * 540 + t * t * 1090
        py = (1 - t) ** 2 * 30 + 2 * (1 - t) * t * 90 + t * t * 30
        c = cols[i % len(cols)]
        ts = C(px, py + 4, 9, lt(c, 0.2))
        for k in range(9):
            ts += P("M%.1f,%.1f L%.1f,%.1f" % (px, py + 8, px - 16 + k * 4, py + 66), stroke=c if k % 2 else dk(c, 0.15), stroke_width=4.5, stroke_linecap="round")
        ts += R(px - 12, py + 12, 24, 10, gold(a), 3)
        tg += ts
    b += g(tg, filter=a.shadow(4, 4, 0.2))
    b += confetti(a, 80, (20, 110, W - 20, H - 20), cols, avoid=[(90, 110, 990, 880), (330, 880, 750, 1250)], seed=5, size=(10, 18), kinds="rcsq")
    # text card
    b += R(90, 110, 900, 770, "#FFFFFF", 36, filter=a.shadow(22, 12, 0.2))
    b += R(108, 128, 864, 734, "none", 26, stroke="#FF4F8B", stroke_width=3)
    b += R(120, 140, 840, 710, "none", 20, stroke="#3EC1D3", stroke_width=1.5, stroke_dasharray="6 6")
    # photo frame bottom (scalloped paper cut)
    ph = {"shape": "rounded", "x": 380, "y": 925, "w": 320, "h": 290}
    fr = ""
    for i in range(0, 12):
        fr += C(ph["x"] - 18 + i * (ph["w"] + 36) / 11, ph["y"] - 18, 16, "#FFFFFF") + C(ph["x"] - 18 + i * (ph["w"] + 36) / 11, ph["y"] + ph["h"] + 18, 16, "#FFFFFF")
    for i in range(0, 12):
        fr += C(ph["x"] - 18, ph["y"] - 18 + i * (ph["h"] + 36) / 11, 16, "#FFFFFF") + C(ph["x"] + ph["w"] + 18, ph["y"] - 18 + i * (ph["h"] + 36) / 11, 16, "#FFFFFF")
    fr += R(ph["x"] - 18, ph["y"] - 18, ph["w"] + 36, ph["h"] + 36, "#FFFFFF")
    b += g(fr, filter=a.shadow(16, 10, 0.25))
    b += R(ph["x"] - 4, ph["y"] - 4, ph["w"] + 8, ph["h"] + 8, "none", 30, stroke="#FFB400", stroke_width=5)
    b += R(ph["x"], ph["y"], ph["w"], ph["h"], a.lg([(0, "#FFF4F8"), (1, "#FFE0EA")]), 26)
    b += kid_silhouette(a, ph["x"] + ph["w"] / 2, ph["y"] + ph["h"] * 0.55, ph["w"] * 0.5, "#F7A8C0", 0.55)
    # hats + poppers flanking
    b += party_hat(a, 175, 1235, 250, "#8E6CFF", "#FFFFFF", "#FFB400", ang=-10)
    b += party_hat(a, 270, 1250, 170, "#3EC1D3", "#FFFFFF", "#FF4F8B", ang=8, pat="dots")
    b += party_hat(a, 905, 1235, 250, "#FF4F8B", "#FFFFFF", "#3EC1D3", ang=10, pat="dots")
    b += party_hat(a, 810, 1250, 170, "#FFB400", "#FFFFFF", "#8E6CFF", ang=-8)
    b += party_popper(a, 40, 1150, -72, 110, cols, seed=6, cone=("#3EC1D3", "#FF4F8B"))
    b += party_popper(a, 1040, 1150, -108, 110, cols, seed=7, cone=("#FFB400", "#8E6CFF"))
    zone = [150, 150, 930, 850]
    return a.svg(b), spec(10, zone, "#D81B60", "#2D1F36", "#6A45D9", tfont="deco", photo=ph)


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
