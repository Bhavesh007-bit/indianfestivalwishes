"""Birthday wishes: 10 cake / balloon / gift / cupcake / sparkler designs."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_e import *
from render import render_cards

CAT = "birthday"


def spec(n, zone, title, text, accent, tone="light", tfont="deco", align="center"):
    return {"id": "E-%s-%d" % (CAT, n), "tpl": True, "zone": zone,
            "colors": {"title": title, "text": text, "accent": accent},
            "tone": tone, "title": tfont, "align": align}


# ------------------------------------------------------------------ 1
def card1():
    """Blush + gold: grand three-tier cake on a gold stand at the bottom, sparklers either side."""
    a = Art(11)
    zone = [150, 110, 930, 620]
    b = R(0, 0, W, H, a.lg([(0, "#FFF3F5"), (0.5, "#FBD9E1"), (1, "#F2B8C6")]))
    # soft rays from the cake
    rays = ""
    for i in range(14):
        an = math.radians(-180 + i * 180 / 13.0)
        rays += P(poly([(540, 980), (540 + math.cos(an - 0.05) * 1400, 980 + math.sin(an - 0.05) * 1400), (540 + math.cos(an + 0.05) * 1400, 980 + math.sin(an + 0.05) * 1400)]), "#FFFFFF", opacity=0.18)
    b += rays
    b += bokeh(a, 26, (0, 0, W, H), ["#FFFFFF", "#F7C873", "#F48FB1"], (14, 55), (0.25, 0.6), avoid=[(110, 70, 970, 660)], seed=4)
    # frame: gold rounded border with star corners
    gf = a.lg([(0, "#B8862E"), (0.3, "#FFE39A"), (0.5, "#D4A13A"), (0.75, "#FFF0C0"), (1, "#A8741F")], 0, 0, 1, 1)
    b += R(26, 26, W - 52, H - 52, "none", 40, stroke=gf, stroke_width=6)
    b += R(40, 40, W - 80, H - 80, "none", 30, stroke="#FFFFFF", stroke_width=2, stroke_dasharray="2 10", stroke_linecap="round", opacity=0.9)
    for (x, y) in [(26, 26), (W - 26, 26), (26, H - 26), (W - 26, H - 26)]:
        b += star(x, y, 30, gf, r2=12, filter=a.shadow(3, 2, 0.25))
    # text panel (cream card)
    b += panel(a, 110, 70, 860, 590, "#FFFBF7", 44, stroke="#E9B9C6", sw=2.5, dash="10 8")
    b += confetti(a, 70, (40, 40, W - 40, 1000), ["#F06292", "#FFC107", "#BA68C8", "#4DD0E1", "#FFFFFF"], avoid=[(100, 60, 980, 680), (330, 700, 750, 1260)], seed=7)
    # cake
    cake = ""
    cake += E(540, 1268, 330, 18, "#B06A7E", opacity=0.25, filter=a.blur(6))
    cake += cake_stand(a, 540, 1162, 560, metal=True)
    cake += cake_tier(a, 540, 1170, 440, 150, "#F8BBD0", "#FFFFFF", seed=2, deco="pearls", deco_col="#FFF6E0")
    cake += cake_tier(a, 540, 1035, 340, 128, "#FFFFFF", "#F48FB1", seed=3, deco="dots", deco_col="#F06292")
    cake += cake_tier(a, 540, 922, 240, 110, "#F48FB1", "#FFF3E0", seed=4, deco="rosettes", deco_col="#FFFFFF", sprink=["#FFC107", "#4DD0E1", "#BA68C8", "#FFFFFF"])
    # topper candles
    for i, (dx, hh, c) in enumerate([(-70, 62, "#4DD0E1"), (-35, 74, "#FFC107"), (0, 84, "#BA68C8"), (35, 74, "#F06292"), (70, 62, "#81C784")]):
        cake += candle(a, 540 + dx, 812 + abs(dx) * 0.08, hh, 13, c)
    # side rosettes / strawberries on bottom tier
    for x in (360, 720):
        cake += C(x, 1035 - 6, 18, a.rg([(0, "#FF8A80"), (0.6, "#E53935"), (1, "#8E1B1B")], 0.35, 0.3, 0.7))
        cake += P("M%d,1008 l-10,-8 M%d,1008 l0,-12 M%d,1008 l10,-8" % (x, x, x), stroke="#4E7A2C", stroke_width=4, stroke_linecap="round")
    b += g(cake, filter=a.shadow(14, 10, 0.22))
    # gifts beside cake
    b += gift(a, 110, 1110, 150, 130, "#BA68C8", "#FFD54F", pat=dots_pattern(a, "#FFFFFF", 22, 3, 0.35))
    b += gift(a, 830, 1140, 130, 100, "#4DD0E1", "#F06292", pat=a.pattern(20, 20, R(0, 0, 10, 20, "#FFFFFF", opacity=0.25), "rotate(45)"))
    # sparklers
    b += sparkler(a, 180, 1080, 250, 820, 95, seed=3)
    b += sparkler(a, 900, 1110, 840, 850, 95, seed=5)
    return a.svg(b), spec(1, zone, "#B0174F", "#3B1B2E", "#C2185B", tfont="deco")


# ------------------------------------------------------------------ 2
def card2():
    """Midnight navy + gold foil: balloon bouquet rising on the right, gifts bottom-left, text top-left."""
    a = Art(22)
    zone = [80, 110, 860, 590]
    b = R(0, 0, W, H, a.lg([(0, "#0F1733"), (0.55, "#1B1F4A"), (1, "#2A1E4E")]))
    b += R(0, 0, W, H, a.rg([(0, "#3A3F8F", 0.55), (1, "#3A3F8F", 0)], 0.8, 0.65, 0.6))
    b += bokeh(a, 30, (0, 0, W, H), ["#FFD36B", "#F6A5C0", "#9FA8FF"], (10, 45), (0.15, 0.45), avoid=[(60, 80, 880, 620)], seed=9)
    b += twinkles(a, 60, (20, 20, W - 20, H - 20), "#FFE9B0", (4, 12), avoid=[(60, 80, 880, 620)], seed=10)
    # gold confetti band along top-left edges (dense, fading)
    b += confetti(a, 60, (0, 0, W, 70), ["#FFD36B", "#F2C14E", "#FFF1C4", "#E7A33E"], seed=11, size=(8, 16))
    b += confetti(a, 45, (0, 0, 60, H), ["#FFD36B", "#F2C14E", "#FFF1C4"], seed=12, size=(8, 16))
    b += confetti(a, 45, (W - 60, 0, W, H), ["#FFD36B", "#F2C14E", "#FFF1C4"], seed=13, size=(8, 16))
    # gold frame corners (art-deco)
    gf = a.lg([(0, "#A8741F"), (0.35, "#FFE7A6"), (0.6, "#D4A13A"), (1, "#FFF1C4")], 0, 0, 1, 1)
    for sx, sy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
        x0 = 30 if sx == 1 else W - 30
        y0 = 30 if sy == 1 else H - 30
        d = "M%d,%d L%d,%d M%d,%d L%d,%d M%d,%d L%d,%d L%d,%d" % (x0, y0 + sy * 150, x0, y0, x0, y0, x0 + sx * 150, y0,
                                                               x0 + sx * 18, y0 + sy * 90, x0 + sx * 18, y0 + sy * 18, x0 + sx * 90, y0 + sy * 18)
        b += P(d, stroke=gf, stroke_width=4)
        b += C(x0 + sx * 18, y0 + sy * 18, 6, gf)
    # balloon bouquet
    tie = (780, 1210)
    ball = [
        (660, 820, 86, "#F2C14E"), (880, 760, 92, "#E9A6B9"), (770, 700, 80, "#FFF3E0"),
        (970, 930, 80, "#D4A13A"), (570, 980, 72, "#C9A0DC"), (830, 940, 96, "#F6D38A"),
        (990, 640, 66, "#F2C14E"), (700, 1040, 62, "#E9A6B9"),
    ]
    bs = ""
    for x, y, r, c in sorted(ball, key=lambda t: t[1]):
        bs += balloon(a, x, y, r, c, tail=tie, strc="#E8D6A8", sw=1.8)
    bs += foil_star_balloon(a, 560, 790, 66, "#F2C14E", tail=tie, rot=10)
    b += g(bs, filter=a.shadow(14, 12, 0.35))
    b += bow_shape(a, tie[0], tie[1], 48, "#F2C14E")
    for i in range(4):
        b += ribbon_curl(tie[0] - 10 + i * 8, tie[1] + 30, 34, ["#F2C14E", "#E9A6B9", "#FFF1C4", "#D4A13A"][i], 2.5, seed=i + 3)
    # gifts bottom-left
    b += gift(a, 90, 1060, 190, 170, "#E9A6B9", "#F2C14E", pat=dots_pattern(a, "#FFFFFF", 26, 3.5, 0.35))
    b += gift(a, 310, 1140, 130, 100, "#F2C14E", "#FFF3E0", pat=a.pattern(22, 22, R(0, 0, 11, 22, "#FFFFFF", opacity=0.25), "rotate(45)"), depth=0.22)
    # glass plaque behind text
    b += R(50, 80, 850, 540, "#FFFFFF", 36, opacity=0.06)
    b += R(64, 94, 822, 512, "none", 28, stroke=gf, stroke_width=2, opacity=0.8)
    return a.svg(b), spec(2, zone, "gold", "#FFF6E6", "#FFD36B", tone="dark", tfont="script", align="left")


# ------------------------------------------------------------------ 3
def card3():
    """Mint polka dot: three giant cupcakes along the bottom, stitched cream card for text."""
    a = Art(33)
    zone = [150, 150, 930, 700]
    b = R(0, 0, W, H, a.lg([(0, "#E3F6EF"), (1, "#BFE8DA")]))
    b += R(0, 0, W, H, dots_pattern(a, "#FFFFFF", 54, 7, 0.55))
    # scalloped paper-cut edge on left and right
    sc = ""
    for y in range(0, H + 60, 60):
        sc += C(0, y, 34, "#F7A8B8") + C(W, y, 34, "#F7A8B8")
        sc += C(0, y, 22, "#FFFFFF", opacity=0.5) + C(W, y, 22, "#FFFFFF", opacity=0.5)
    b += g(sc, filter=a.shadow(4, 0, 0.18))
    # text card
    b += panel(a, 100, 90, 880, 680, "#FFFDF8", 48, stroke="#F48FB1", sw=3, dash="14 10")
    b += R(100, 90, 880, 680, a.noise(0.05), 48)
    # sprinkles scattered around the card edge
    b += sprinkles(a, 60, (60, 20, W - 60, 90), ["#F06292", "#FFCA28", "#4FC3F7", "#AB47BC", "#66BB6A"], seed=3, ln=16, wd=5)
    b += sprinkles(a, 40, (60, 770, W - 60, 900), ["#F06292", "#FFCA28", "#4FC3F7", "#AB47BC", "#66BB6A"], seed=4, ln=16, wd=5)
    # cupcakes
    b += E(540, 1262, 470, 16, "#2E7D6A", opacity=0.18, filter=a.blur(6))
    b += cupcake(a, 215, 1250, 250, "#F48FB1", "#FFF3F8", sprink=["#F06292", "#FFCA28", "#4FC3F7", "#AB47BC"], seed=5)
    b += cupcake(a, 865, 1250, 250, "#7E57C2", "#FFE0B2", sprink=["#F06292", "#FFFFFF", "#4FC3F7"], seed=6)
    b += cupcake(a, 540, 1248, 290, "#FFB74D", "#F8BBD0", sprink=["#FFFFFF", "#AB47BC", "#4FC3F7", "#FFCA28"], seed=7)
    return a.svg(b), spec(3, zone, "#C2185B", "#2F3A36", "#00695C", tfont="deco")


# ------------------------------------------------------------------ 4
def card4():
    """Lilac gift-wrap card: satin ribbon bands with a huge bow top-right, text on a hanging gift tag."""
    a = Art(44)
    zone = [150, 430, 910, 950]
    base = "#E6D8F5"
    b = R(0, 0, W, H, a.lg([(0, "#F1E8FB"), (1, "#D9C5F0")]))
    # wrapping paper pattern: stars + dots
    wp = star(20, 20, 9, "#FFFFFF", opacity=0.7) + C(60, 60, 4, "#B79BE0", opacity=0.8) + star(60, 20, 5, "#B79BE0", opacity=0.6) + C(20, 60, 3, "#FFFFFF", opacity=0.8)
    b += R(0, 0, W, H, a.pattern(80, 80, wp))
    rib = "#D81B60"
    rf = a.lg([(0, dk(rib, 0.2)), (0.35, lt(rib, 0.25)), (0.5, lt(rib, 0.4)), (0.65, lt(rib, 0.2)), (1, dk(rib, 0.25))], 0, 0, 1, 0)
    rfh = a.lg([(0, dk(rib, 0.2)), (0.35, lt(rib, 0.25)), (0.5, lt(rib, 0.4)), (0.65, lt(rib, 0.2)), (1, dk(rib, 0.25))], 0, 0, 0, 1)
    b += g(R(0, 175, W, 90, rfh) + R(935, 0, 90, H, rf), filter=a.shadow(8, 4, 0.25))
    b += R(0, 186, W, 3, "#FFFFFF", opacity=0.35) + R(0, 251, W, 3, "#FFFFFF", opacity=0.35)
    b += R(946, 0, 3, H, "#FFFFFF", opacity=0.35) + R(1011, 0, 3, H, "#FFFFFF", opacity=0.35)
    # big bow
    bw = ""
    bw += P("M980,230 C940,330 900,420 870,470 L905,480 L925,452 L950,470 C970,380 985,300 990,232Z", a.lg([(0, lt(rib, 0.2)), (1, dk(rib, 0.25))]))
    bw += P("M980,230 C1010,320 1040,390 1060,440 L1030,455 L1015,425 L992,440 C990,360 985,300 980,232Z", a.lg([(0, lt(rib, 0.1)), (1, dk(rib, 0.3))]))
    lf = a.rg([(0, lt(rib, 0.45)), (0.55, rib), (1, dk(rib, 0.3))], 0.5, 0.5, 0.6)
    bw += P("M980,220 C900,60 720,70 730,190 C740,300 900,280 980,230Z", lf)
    bw += P("M980,220 C1060,60 1200,90 1170,200 C1140,300 1040,270 980,230Z", lf)
    bw += P("M965,215 C900,120 790,120 780,185", stroke=dk(rib, 0.35), stroke_width=4, opacity=0.5)
    bw += P("M995,215 C1050,130 1120,140 1130,195", stroke=dk(rib, 0.35), stroke_width=4, opacity=0.5)
    bw += P("M760,170 C780,120 850,110 900,150", stroke="#FFFFFF", stroke_width=6, stroke_linecap="round", opacity=0.35)
    bw += E(980, 225, 42, 36, a.rg([(0, lt(rib, 0.4)), (1, dk(rib, 0.25))], 0.4, 0.35, 0.7))
    bw += P("M955,215 Q980,240 1005,215", stroke=dk(rib, 0.35), stroke_width=3, opacity=0.6)
    b += g(bw, filter=a.shadow(14, 10, 0.35))
    # tag string from knot to tag hole
    b += P("M975,240 C900,330 700,300 540,380", stroke="#C9A227", stroke_width=4)
    # gift tag
    tag = "M130,380 L950,380 Q970,380 970,400 L970,980 Q970,1000 950,1000 L130,1000 Q110,1000 110,980 L110,400 Q110,380 130,380Z"
    tag = poly([(100, 440), (440, 380), (640, 380), (980, 440), (980, 990), (100, 990)])
    b += g(P(tag, "#FFFCF5"), filter=a.shadow(20, 12, 0.3))
    b += P(tag, a.noise(0.05))
    b += P(poly([(128, 460), (446, 404), (634, 404), (952, 460), (952, 962), (128, 962)]), "none", stroke="#B39DDB", stroke_width=3, stroke_dasharray="12 9")
    b += C(540, 410, 16, "#E6D8F5", stroke="#C9A227", stroke_width=5)
    # bottom: gift pile
    b += gift(a, 70, 1080, 200, 160, "#7E57C2", "#FFD54F", pat=dots_pattern(a, "#FFFFFF", 24, 3.5, 0.4))
    b += gift(a, 300, 1150, 120, 90, "#26C6DA", rib, depth=0.22)
    b += gift(a, 770, 1110, 150, 130, "#FFB300", "#7E57C2", pat=a.pattern(24, 24, R(0, 0, 12, 24, "#FFFFFF", opacity=0.25), "rotate(45)"))
    b += confetti(a, 40, (40, 1010, W - 140, 1250), ["#D81B60", "#7E57C2", "#FFD54F", "#26C6DA"], avoid=[(60, 1040, 440, 1260), (760, 1060, 960, 1260)], seed=5)
    b += confetti(a, 30, (30, 20, 880, 170), ["#D81B60", "#7E57C2", "#FFD54F", "#26C6DA"], seed=6)
    return a.svg(b), spec(4, zone, "#6A1B9A", "#2E1A47", "#D81B60", tfont="script")


# ------------------------------------------------------------------ 5
def cake_slice(a, x, y, s):
    """wedge slice seen 3/4; x,y = front-left bottom corner."""
    o = ""
    # geometry
    fw, fh = s * 0.95, s * 0.62          # front face (the cut face)
    tipx, tipy = x + s * 1.02, y - s * 0.48  # wedge point at back
    top = [(x, y - fh), (x + fw, y - fh), (tipx + s * 0.02, tipy - fh + s * 0.02)]
    # side (curved crust) goes from front-right to tip
    side = poly([(x + fw, y - fh), (tipx + s * 0.02, tipy - fh + s * 0.02), (tipx, tipy), (x + fw, y)])
    o += P(side, a.lg([(0, "#F7C9A6"), (1, "#C98B62")], 0, 0, 1, 0))
    o += P(side, "#FFFFFF", opacity=0.0)
    # front face with layers
    layers = [("#8B4A2B", 0.26), ("#FFF1F4", 0.1), ("#F48FB1", 0.12), ("#8B4A2B", 0.24), ("#FFF1F4", 0.1), ("#F48FB1", 0.18)]
    yy = y
    for c, t in layers:
        hh = fh * t
        o += R(x, yy - hh, fw, hh, a.lg([(0, lt(c, 0.12)), (1, dk(c, 0.1))], 0, 0, 1, 0))
        yy -= hh
    # sponge texture dots
    rnd = random.Random(5)
    for i in range(50):
        px = rnd.uniform(x + 6, x + fw - 6); py = rnd.uniform(y - fh + 6, y - 6)
        o += C(px, py, rnd.uniform(1, 2.6), "#5A2A18", opacity=0.3)
    # frosting top with drip over front edge
    tp = poly(top)
    o += P(tp, a.lg([(0, "#FFFFFF"), (1, "#FCE4EC")], 0, 0, 1, 1))
    dr = drip_path(x, x + fw, y - fh + 16, rnd, depth=(10, 46), step=(24, 40), top=y - fh - 2)
    o += P(dr, a.lg([(0, "#FFFFFF"), (1, "#F8D3DF")]))
    # rosettes on the top back edge + strawberry
    for i in range(3):
        t = 0.25 + i * 0.28
        px = x + fw + (tipx - x - fw) * t
        py = y - fh + (tipy - y) * t
        o += rosette(a, px, py - 8, 16, "#F8BBD0")
    sx, sy = x + fw * 0.45, y - fh - s * 0.05
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1fZ" % (sx, sy + s * 0.1, sx - s * 0.12, sy + s * 0.02, sx - s * 0.1, sy - s * 0.12, sx, sy - s * 0.12, sx + s * 0.1, sy - s * 0.12, sx + s * 0.12, sy + s * 0.02, sx, sy + s * 0.1),
           a.rg([(0, "#FF8A80"), (0.6, "#E53935"), (1, "#8E1B1B")], 0.4, 0.35, 0.7))
    for i in range(9):
        o += E(sx + rnd.uniform(-s * 0.07, s * 0.07), sy + rnd.uniform(-s * 0.08, s * 0.06), 1.8, 2.8, "#FFE082")
    o += P("M%.1f,%.1f l-14,-8 M%.1f,%.1f l0,-14 M%.1f,%.1f l14,-8" % (sx, sy - s * 0.12, sx, sy - s * 0.12, sx, sy - s * 0.12), stroke="#4E7A2C", stroke_width=5, stroke_linecap="round")
    return o, (x + fw * 0.72, y - fh - 10)


def card5():
    """Plum night + gold: cake slice on a gold-rim plate with a lit sparkler candle, bottom-right."""
    a = Art(55)
    zone = [110, 110, 890, 620]
    b = R(0, 0, W, H, a.lg([(0, "#2B0F2E"), (0.6, "#44173F"), (1, "#5A1E47")]))
    b += R(0, 0, W, H, a.rg([(0, "#9C3D6E", 0.55), (1, "#9C3D6E", 0)], 0.72, 0.78, 0.55))
    # velvet diagonal texture
    b += R(0, 0, W, H, a.pattern(18, 18, R(0, 0, 2, 18, "#FFFFFF", opacity=0.03), "rotate(35)"))
    b += bokeh(a, 36, (0, 650, W, H), ["#FFD36B", "#F48FB1", "#FFB199"], (12, 60), (0.2, 0.5), seed=4)
    b += twinkles(a, 50, (20, 20, W - 20, H - 20), "#FFE6A8", (4, 12), avoid=[(70, 70, 930, 660)], seed=5)
    # gold ornamental frame: double arc corners
    gf = a.lg([(0, "#A8741F"), (0.35, "#FFE7A6"), (0.6, "#D4A13A"), (1, "#FFF1C4")], 0, 0, 1, 1)
    b += R(34, 34, W - 68, H - 68, "none", 0, stroke=gf, stroke_width=3)
    for (x, y, rot) in [(34, 34, 0), (W - 34, 34, 90), (W - 34, H - 34, 180), (34, H - 34, 270)]:
        orn = P("M0,0 Q70,0 90,40 Q40,20 0,90 Q0,40 0,0Z", gf) + C(26, 26, 8, gf) + P("M0,120 Q10,60 60,60 M120,0 Q60,10 60,60", stroke=gf, stroke_width=2)
        b += g(orn, "translate(%d %d) rotate(%d)" % (x, y, rot))
    # text plaque: deep glass
    b += R(70, 70, 860, 590, "#1A0819", 40, opacity=0.45)
    b += R(86, 86, 828, 558, "none", 30, stroke=gf, stroke_width=2, opacity=0.9)
    # plate
    pl = ""
    pl += E(730, 1180, 300, 70, "#000", opacity=0.35, filter=a.blur(10))
    pl += E(730, 1160, 300, 74, gf)
    pl += E(730, 1154, 280, 64, a.lg([(0, "#FFFFFF"), (1, "#E9DDE8")]))
    pl += E(730, 1158, 200, 42, "#F3E9F1")
    pl += E(730, 1158, 200, 42, "none", stroke="#E1CCDD", stroke_width=2)
    b += pl
    # fork
    fk = gf
    b += g(P("M0,0 L14,0 L12,190 Q7,200 2,190Z", fk) + P("M-12,-10 L26,-10 L24,-80 L20,-80 L18,-24 L15,-24 L13,-80 L9,-80 L7,-24 L4,-24 L2,-80 L-2,-80 L-4,-24 Q-10,-24 -12,-10Z", fk),
           "translate(420 1080) rotate(-62)", filter=a.shadow(4, 3, 0.4))
    sl, tip = cake_slice(a, 560, 1170, 380)
    b += g(sl, filter=a.shadow(12, 10, 0.35))
    # sparkler candle in the slice
    b += sparkler(a, tip[0], tip[1] + 20, tip[0] + 30, tip[1] - 170, 150, seed=8)
    # crossed sparklers top corners? keep lower-left sparkle cluster
    b += sparkler(a, 150, 1240, 240, 1020, 110, seed=9)
    b += confetti(a, 40, (40, 700, 520, 1250), ["#FFD36B", "#F48FB1", "#FFF1C4"], avoid=[(100, 950, 330, 1260)], seed=10, size=(8, 14))
    return a.svg(b), spec(5, zone, "gold", "#FFF1F6", "#FFD36B", tone="dark", tfont="deco")


# ------------------------------------------------------------------ 6
def card6():
    """Sky full of balloons at different depths; text on a big cloud panel in the middle."""
    a = Art(66)
    zone = [150, 440, 930, 950]
    b = R(0, 0, W, H, a.lg([(0, "#8FD3FF"), (0.55, "#CBEBFF"), (1, "#FFE3D3")]))
    b += C(900, 150, 380, a.rg([(0, "#FFFFFF", 0.7), (1, "#FFFFFF", 0)]))
    # far clouds
    b += cloud(a, 180, 260, 70, "#FFFFFF", op=0.7) + cloud(a, 820, 1150, 90, "#FFFFFF", op=0.7) + cloud(a, 950, 330, 55, "#FFFFFF", op=0.6)
    cols = ["#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF", "#C77DFF", "#FF9CEE", "#FF9F45"]
    rnd = random.Random(6)
    # far, blurred small balloons
    far = ""
    for i in range(18):
        x = rnd.uniform(40, W - 40); y = rnd.uniform(40, H - 120)
        if inside(x, y, [(90, 360, 990, 1030)]):
            continue
        far += balloon(a, x, y, rnd.uniform(16, 26), rnd.choice(cols), tail=(x + rnd.uniform(-10, 10), y + 110), sw=1.2, strc="#FFFFFF")
    b += g(far, filter=a.blur(2.2), opacity=0.7)
    # mid balloons
    mid = ""
    for (x, y, r, c) in [(120, 130, 48, cols[3]), (330, 90, 40, cols[1]), (760, 70, 42, cols[4]), (960, 180, 50, cols[2]),
                          (70, 1120, 46, cols[5]), (260, 1180, 40, cols[6]), (1010, 1060, 44, cols[1])]:
        mid += balloon(a, x, y, r, c, tail=(x - 8, y + 200), sw=1.6, strc="#FFFFFF")
    b += g(mid, filter=a.shadow(6, 6, 0.15))
    # the cloud panel
    cp = ("M150,420 C120,330 250,300 300,350 C330,270 470,260 520,330 C580,260 720,270 750,345 C810,290 950,320 930,420 "
          "C1020,440 1020,560 960,600 L960,860 C1030,900 1010,1020 930,1010 C930,1090 800,1100 760,1040 C700,1110 560,1100 530,1040 "
          "C480,1110 330,1100 310,1030 C230,1080 110,1030 140,950 C60,930 60,820 120,800 L120,600 C60,560 70,440 150,420Z")
    b += g(P(cp, a.lg([(0, "#FFFFFF"), (0.8, "#FFFFFF"), (1, "#EEF6FF")])), filter=a.shadow(24, 14, 0.2))
    b += P(cp, "none", stroke="#BFE0FF", stroke_width=3, stroke_dasharray="6 10", transform="translate(54 58) scale(0.9)")
    # near big balloons at edges (cropped)
    near = ""
    near += balloon(a, -10, 560, 110, cols[0], tail=(40, 900), sw=2, strc="#FFFFFF")
    near += balloon(a, 1080, 700, 120, cols[4], tail=(1020, 1100), sw=2, strc="#FFFFFF")
    near += balloon(a, 90, 1270, 90, cols[1], sw=2)
    near += balloon(a, 1000, 1290, 80, cols[3], sw=2)
    near += foil_star_balloon(a, 930, 1180, 60, "#FFC93C")
    b += g(near, filter=a.shadow(12, 10, 0.2))
    b += confetti(a, 40, (20, 20, W - 20, H - 20), cols, avoid=[(80, 280, 1000, 1110), (380, 20, 700, 440)], seed=7, size=(8, 16))
    ph = {"shape": "oval", "x": 405, "y": 48, "w": 270, "h": 310}
    b += photo_balloon(a, ph, "#FF5C8A")
    sp = spec(6, zone, "#1F5FBF", "#243047", "#C62828", tfont="deco")
    sp["photo"] = ph; sp["slot"] = True
    return a.svg(b), sp


def photo_balloon(a, ph, col):
    """a big glossy balloon whose face is the oval photo window."""
    cx, cy, rx, ry = ph["x"] + ph["w"] / 2, ph["y"] + ph["h"] / 2, ph["w"] / 2, ph["h"] / 2
    o = ""
    bot = cy + ry + 16
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (cx, bot + 14, cx + 30, bot + 40, cx - 26, bot + 55, cx + 12, bot + 76), stroke="#FFFFFF", stroke_width=2.5)
    o += P("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1fZ" % (cx - 16, bot + 16, cx, bot - 4, cx + 16, bot + 16), dk(col, 0.2))
    o += E(cx, cy, rx + 18, ry + 18, a.rg([(0, lt(col, 0.5)), (0.5, col), (1, dk(col, 0.3))], 0.35, 0.3, 0.8), filter=a.shadow(14, 10, 0.25))
    o += E(cx, cy, rx, ry, a.lg([(0, "#FFF4F7"), (1, "#FFE0EA")]))
    o += C(cx, cy - ry * 0.18, rx * 0.3, lt(col, 0.7))
    o += P("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" % (cx - rx * 0.62, cy + ry, cx - rx * 0.6, cy + ry * 0.3, cx + rx * 0.6, cy + ry * 0.3, cx + rx * 0.62, cy + ry), lt(col, 0.7))
    o += E(cx, cy, rx + 9, ry + 9, "none", stroke="#FFFFFF", stroke_width=3, opacity=0.8)
    o += P("M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f" % (cx - rx - 8, cy - 20, rx + 8, ry + 8, cx - rx * 0.35, cy - ry - 7), stroke="#FFFFFF", stroke_width=7, stroke_linecap="round", opacity=0.55)
    return o


# ------------------------------------------------------------------ 7
def card7():
    """Boho: organic balloon garland with eucalyptus over an arch backdrop."""
    a = Art(77)
    zone = [160, 610, 920, 1080]
    b = R(0, 0, W, H, a.lg([(0, "#F6EDE3"), (1, "#EADBCB")]))
    b += R(0, 0, W, H, a.noise(0.06, 0.8))
    # arch backdrop
    arch = "M120,1240 L120,560 C120,300 320,150 540,150 C760,150 960,300 960,560 L960,1240Z"
    b += g(P(arch, a.lg([(0, "#DCC4B0"), (1, "#C9AE98")])), filter=a.shadow(18, 10, 0.18))
    arch2 = "M150,1240 L150,570 C150,330 340,185 540,185 C740,185 930,330 930,570 L930,1240Z"
    b += P(arch2, "#FBF6F0")
    b += P(arch2, a.noise(0.04, 0.8))
    # floor
    b += R(0, 1240, W, 110, a.lg([(0, "#D8C3AE"), (1, "#C8AF97")]))
    cols = ["#C8745A", "#E8B7A4", "#F3E3D3", "#9CAF88", "#D9A15B", "#B25B4A"]
    rnd = random.Random(7)
    # garland path points: from left side (70,760) up over arch to right (1010,520)
    pts = []
    for i in range(60):
        t = i / 59.0
        an = math.pi * (1.0 - 1.0 * t)
        x = 540 + math.cos(an) * 430
        y = 560 - math.sin(an) * 380
        if y > 560:
            y = 560 + (y - 560) * 1.4
        pts.append((x, y))
    gar = ""
    # eucalyptus leaves behind
    for (x, y) in pts[::2]:
        for k in range(2):
            ang = rnd.uniform(0, 360)
            ln = rnd.uniform(40, 70)
            gar += g(E(0, -ln / 2, ln * 0.33, ln / 2, a.lg([(0, "#8FA88A"), (1, "#6E8B6A")])) + P("M0,0 L0,%.1f" % -ln, stroke="#5E7A5A", stroke_width=1.5),
                     "translate(%.1f %.1f) rotate(%.1f)" % (x + rnd.uniform(-40, 40), y + rnd.uniform(-40, 40), ang), opacity=0.9)
    # balloons
    bl = []
    for i, (x, y) in enumerate(pts):
        if i % 2:
            continue
        for k in range(2):
            r = rnd.choice([22, 30, 40, 52, 62])
            bl.append((x + rnd.uniform(-45, 45), y + rnd.uniform(-45, 45), r, rnd.choice(cols)))
    bl.sort(key=lambda t: -t[2])
    for (x, y, r, c) in bl:
        fill = a.rg([(0, lt(c, 0.5)), (0.4, lt(c, 0.1)), (0.85, c), (1, dk(c, 0.25))], 0.38, 0.32, 0.72, 0.32, 0.25)
        gar += C(x, y, r, fill) + E(x - r * 0.35, y - r * 0.4, r * 0.16, r * 0.28, "#FFFFFF", opacity=0.45, transform="rotate(30 %.1f %.1f)" % (x - r * 0.35, y - r * 0.4))
    # pampas grass plumes at right cluster
    for k in range(5):
        x0, y0 = 1000 + k * 8, 420
        ang = -30 + k * 10
        pl = ""
        for j in range(26):
            t = j / 26.0
            pl += E(0, -t * 200, 16 * (1 - t * 0.5), 9, "#E9D8BF", opacity=0.75, transform="rotate(%d 0 %.1f)" % (rnd.randint(-40, 40), -t * 200))
        gar = g(pl + P("M0,0 L0,-200", stroke="#C9B08A", stroke_width=2), "translate(%d %d) rotate(%d)" % (x0 - 40, y0 + 160, ang)) + gar
    b += g(gar, filter=a.shadow(8, 8, 0.2))
    # bottom-right: cake-less boho: stack of gifts wrapped in kraft with twine
    b += gift(a, 760, 1130, 170, 115, "#C9A27A", "#F3E3D3", depth=0.22, bowscale=0.9)
    b += gift(a, 120, 1150, 130, 95, "#9CAF88", "#F3E3D3", depth=0.22, bowscale=0.9)
    return a.svg(b), spec(7, zone, "#8E3B2A", "#3E2C22", "#4E6B40", tfont="script")


# ------------------------------------------------------------------ 8
def card8():
    """Deep teal: an open gift box bursting with stars, streamers and confetti from the bottom centre."""
    a = Art(88)
    zone = [150, 110, 930, 610]
    b = R(0, 0, W, H, a.lg([(0, "#073B4C"), (0.6, "#0B5563"), (1, "#127A7A")]))
    # rays from gift
    rays = ""
    for i in range(22):
        an = math.radians(-180 + i * (180 / 21.0))
        rays += P(poly([(540, 1060), (540 + math.cos(an - 0.035) * 1500, 1060 + math.sin(an - 0.035) * 1500), (540 + math.cos(an + 0.035) * 1500, 1060 + math.sin(an + 0.035) * 1500)]), "#FFFFFF", opacity=0.05)
    b += rays
    b += C(540, 1000, 420, a.rg([(0, "#FFE8A3", 0.55), (0.5, "#FFD166", 0.15), (1, "#FFD166", 0)]))
    # frosted panel
    b += R(90, 60, 900, 600, "#032A36", 40, opacity=0.55)
    gf = a.lg([(0, "#E9B949"), (0.5, "#FFF1C4"), (1, "#E9B949")], 0, 0, 1, 0)
    b += R(106, 76, 868, 568, "none", 30, stroke=gf, stroke_width=2)
    # burst out of box
    cols = ["#FF6F61", "#FFD166", "#06D6A0", "#FFFFFF", "#EF476F", "#9B8CFF"]
    rnd = random.Random(8)
    bst = ""
    ox, oy = 540, 960
    for i in range(18):
        an = math.radians(rnd.uniform(-160, -20)); ln = rnd.uniform(200, 330)
        ex, ey = ox + math.cos(an) * ln, oy + math.sin(an) * ln
        if ey < 690:
            ey = 690 + rnd.uniform(0, 30)
        mx, my = (ox + ex) / 2 + rnd.uniform(-60, 60), (oy + ey) / 2 + rnd.uniform(-40, 40)
        bst += P("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (ox + rnd.uniform(-60, 60), oy, mx, my, ex, ey), stroke=rnd.choice(cols), stroke_width="%.1f" % rnd.uniform(4, 8), stroke_linecap="round")
    for i in range(22):
        an = math.radians(rnd.uniform(-170, -10)); ln = rnd.uniform(120, 340)
        ex, ey = ox + math.cos(an) * ln, oy + math.sin(an) * ln
        if ey < 700:
            continue
        bst += star(ex, ey, rnd.uniform(12, 26), a.lg([(0, "#FFF6C8"), (1, "#FFC233")]), rot=rnd.uniform(0, 60))
    b += g(bst, filter=a.glow(3))
    b += confetti(a, 90, (60, 680, W - 60, 1250), cols, avoid=[(330, 940, 760, 1260)], seed=9, size=(10, 20))
    b += confetti(a, 40, (20, 20, W - 20, 60), cols, seed=10, size=(8, 14))
    b += twinkles(a, 40, (20, 20, W - 20, H - 20), "#FFF1C4", (5, 14), avoid=[(80, 50, 1000, 670)], seed=11)
    # open box
    box, rib = "#EF476F", "#FFD166"
    bx, by, bw_, bh = 400, 1000, 280, 230
    bxs = ""
    bxs += P(poly([(bx, by), (bx + bw_, by), (bx + bw_ + 60, by - 40), (bx + 60, by - 40)]), dk(box, 0.45))  # inside
    bxs += C(540, 970, 90, a.rg([(0, "#FFF6C8", 0.95), (1, "#FFD166", 0)]))
    bxs += P(poly([(bx + bw_, by), (bx + bw_ + 60, by - 40), (bx + bw_ + 60, by + bh - 40), (bx + bw_, by + bh)]), dk(box, 0.3))
    bxs += R(bx, by, bw_, bh, a.lg([(0, lt(box, 0.1)), (1, dk(box, 0.12))]))
    bxs += R(bx, by, bw_, bh, dots_pattern(a, "#FFFFFF", 30, 4, 0.35))
    bxs += R(bx + bw_ / 2 - 22, by, 44, bh, a.lg([(0, dk(rib, 0.1)), (0.5, lt(rib, 0.3)), (1, dk(rib, 0.1))], 0, 0, 1, 0))
    bxs += P(poly([(bx + bw_, by + 90), (bx + bw_ + 60, by + 50), (bx + bw_ + 60, by + 86), (bx + bw_, by + 126)]), dk(rib, 0.2))
    b += g(bxs, filter=a.shadow(14, 10, 0.4))
    # flying lid
    lid = R(-170, -40, 340, 70, a.lg([(0, lt(box, 0.15)), (1, dk(box, 0.1))])) + R(-170, -40, 340, 70, dots_pattern(a, "#FFFFFF", 30, 4, 0.35))
    lid += R(-22, -40, 44, 70, rib) + bow_shape(a, 0, -46, 70, rib)
    b += g(lid, "translate(300 820) rotate(-24)", filter=a.shadow(14, 12, 0.4))
    return a.svg(b), spec(8, zone, "gold", "#F2FFFC", "#FFD166", tone="dark", tfont="deco")


# ------------------------------------------------------------------ 9
def card9():
    """Close-up of a round cake in perspective at the top, candles lit; text on a lace doily card."""
    a = Art(99)
    zone = [160, 690, 920, 1190]
    b = R(0, 0, W, H, "#FBEDE6")
    # gingham tablecloth
    gp = R(0, 0, 60, 60, "#FBEDE6") + R(0, 0, 30, 60, "#F3B7B0", opacity=0.55) + R(0, 0, 60, 30, "#F3B7B0", opacity=0.55)
    b += R(0, 0, W, H, a.pattern(60, 60, gp))
    b += R(0, 0, W, H, a.rg([(0, "#FFFFFF", 0), (1, "#7A2E2E", 0.25)], 0.5, 0.45, 0.8))
    # cake board
    cx, cy, rx, ry = 540, 150, 520, 230
    ck = ""
    ck += E(cx, cy + 220, rx + 30, ry + 30, "#000", opacity=0.25, filter=a.blur(14))
    ck += E(cx, cy + 190, rx + 36, ry + 36, a.lg([(0, "#FFF1C4"), (0.5, "#D4A13A"), (1, "#8C5E14")], 0, 0, 1, 0))
    # side of cake
    sh = 170
    side = "M%d,%d L%d,%d A%d,%d 0 0 0 %d,%d L%d,%d A%d,%d 0 0 1 %d,%dZ" % (cx - rx, cy, cx - rx, cy + sh, rx, ry, cx + rx, cy + sh, cx + rx, cy, rx, ry, cx - rx, cy)
    ck += P(side, a.lg([(0, "#E57373"), (0.3, "#FFCDD2"), (0.6, "#F8A5AE"), (1, "#C44B55")], 0, 0, 1, 0))
    # scallop piping on side
    for i in range(1, 24):
        t = i / 24.0
        an = math.pi * t
        px = cx - math.cos(an) * rx
        py = cy + sh + math.sin(an) * ry - 26
        ck += rosette(a, px, py, 12 + 8 * math.sin(an), "#FFFFFF")
    # top
    ck += E(cx, cy, rx, ry, a.rg([(0, "#FFFFFF"), (0.8, "#FFF3F3"), (1, "#FAD4D8")], 0.5, 0.6, 0.6))
    # drips over the front edge
    rnd = random.Random(9)
    dr = ""
    for i in range(1, 26):
        t = i / 26.0
        an = math.pi * t
        px = cx - math.cos(an) * rx
        py = cy + math.sin(an) * ry
        dl = rnd.uniform(20, 80) * math.sin(an)
        dr += P("M%.1f,%.1f L%.1f,%.1f A9,9 0 0 0 %.1f,%.1f L%.1f,%.1fZ" % (px - 9, py - 4, px - 9, py + dl, px + 9, py + dl, px + 9, py - 4), "#FFFFFF")
    ck += dr
    ck += E(cx, cy, rx, ry, "none", stroke="#FFFFFF", stroke_width=10)
    # rosette ring on top edge
    for i in range(22):
        an = math.pi * 2 * i / 22.0
        px = cx + math.cos(an) * (rx - 40); py = cy + math.sin(an) * (ry - 22)
        if py < 0:
            continue
        ck += rosette(a, px, py, 16, "#F48FB1")
    # sprinkles in the middle
    cpp = a.clip(E(cx, cy, rx - 70, ry - 45, "#000"))
    ck += sprinkles(a, 160, (cx - rx, 0, cx + rx, cy + ry), ["#FF7043", "#FFCA28", "#4FC3F7", "#AB47BC", "#66BB6A", "#EC407A"], seed=3, clip=cpp, ln=12, wd=4)
    # strawberries
    for (sx, sy) in [(260, 250), (820, 250), (540, 330), (390, 305), (690, 305)]:
        ck += C(sx, sy, 22, a.rg([(0, "#FF8A80"), (0.6, "#E53935"), (1, "#8E1B1B")], 0.4, 0.35, 0.7))
        ck += C(sx - 7, sy - 8, 5, "#FFFFFF", opacity=0.6)
    # candles standing on top
    cands = [(300, 180, "#4FC3F7"), (420, 240, "#FFCA28"), (540, 260, "#AB47BC"), (660, 240, "#66BB6A"), (780, 180, "#EC407A"), (400, 120, "#FF7043"), (680, 120, "#4FC3F7"), (540, 100, "#FFCA28")]
    for (x, y, c) in sorted(cands, key=lambda t: t[1]):
        ck += E(x, y + 2, 12, 5, "#000", opacity=0.15)
        ck += candle(a, x, y, 110 if y > 150 else 95, 16, c)
    b += ck
    # doily card
    rr = 30
    doily = ""
    for i in range(0, 25):
        x = 130 + i * 34.2
        doily += C(x, 640, 20, "#FFFFFF") + C(x, 1240, 20, "#FFFFFF")
    for i in range(0, 18):
        y = 640 + i * 35.3
        doily += C(130, y, 20, "#FFFFFF") + C(950, y, 20, "#FFFFFF")
    doily += R(130, 640, 820, 600, "#FFFFFF")
    b += g(doily, filter=a.shadow(14, 10, 0.25))
    holes = ""
    for i in range(0, 25):
        x = 130 + i * 34.2
        holes += C(x, 640, 5, "#F6D9D5") + C(x, 1240, 5, "#F6D9D5")
    for i in range(1, 17):
        y = 640 + i * 35.3
        holes += C(130, y, 5, "#F6D9D5") + C(950, y, 5, "#F6D9D5")
    b += holes
    b += R(152, 662, 776, 556, "none", 18, stroke="#EF9A9A", stroke_width=2, stroke_dasharray="3 7", stroke_linecap="round")
    return a.svg(b), spec(9, zone, "#B71C3C", "#3A2327", "#BF360C", tfont="deco")


# ------------------------------------------------------------------ 10
def card10():
    """Emerald + gold: row of tall spiral candles on a frosted cake edge across the top, glowing."""
    a = Art(1010)
    zone = [150, 610, 930, 1170]
    b = R(0, 0, W, H, a.lg([(0, "#062B26"), (0.5, "#0B3D35"), (1, "#0F4A3F")]))
    b += R(0, 0, W, H, a.pattern(60, 60, P("M30,0 L60,30 L30,60 L0,30Z", "none", stroke="#FFFFFF", stroke_width=1, opacity=0.035)))
    b += R(0, 0, W, 560, a.rg([(0, "#FFD36B", 0.35), (1, "#FFD36B", 0)], 0.5, 0.35, 0.6))
    b += twinkles(a, 70, (20, 20, W - 20, 560), "#FFF1C4", (4, 12), seed=4)
    # candles row
    cols = ["#F48FB1", "#FFD54F", "#4DD0E1", "#FFFFFF", "#CE93D8", "#FF8A65", "#AED581"]
    xs = [140, 270, 400, 540, 680, 810, 940]
    hs = [190, 240, 210, 280, 220, 250, 185]
    for x, h_, c in zip(xs, hs, cols):
        b += candle(a, x, 470, h_, 30, c, stripe="#FFFFFF" if c != "#FFFFFF" else "#F48FB1")
        # wax drips
        b += P("M%d,%d q4,20 0,34 a6,6 0 0 0 12,0 q-4,-14 0,-34Z" % (x - 12, 470 - h_ + 2), lt(c, 0.4), opacity=0.9)
    # frosted cake edge across
    rnd = random.Random(10)
    top = 450
    ce = "M0,%d L%d,%d L%d,%d L0,%dZ" % (top, W, top, W, 560, 560)
    b += g(P(ce, a.lg([(0, "#F8BBD0"), (1, "#EC8FB0")])), filter=a.shadow(10, 8, 0.4))
    b += P(drip_path(0, W, 520, rnd, depth=(20, 70), step=(40, 70), top=top - 4), a.lg([(0, "#FFFFFF"), (1, "#F6E7EE")]))
    b += R(0, top - 8, W, 14, "#FFFFFF", 7)
    b += sprinkles(a, 90, (10, top - 2, W - 10, top + 40), ["#FFD54F", "#4DD0E1", "#CE93D8", "#FF8A65", "#AED581"], seed=6, ln=12, wd=4)
    for x in range(40, W, 80):
        b += C(x, 548, 9, a.rg([(0, "#FFFFFF"), (0.6, "#FFE9A8"), (1, "#C9A227")], 0.35, 0.3, 0.7))
    # gold filigree band bottom
    gf = a.lg([(0, "#A8741F"), (0.35, "#FFE7A6"), (0.6, "#D4A13A"), (1, "#FFF1C4")], 0, 0, 1, 0)
    b += R(40, 580, W - 80, 640, "none", 36, stroke=gf, stroke_width=3)
    b += R(56, 596, W - 112, 608, "none", 28, stroke=gf, stroke_width=1, opacity=0.6)
    for x in (40, W - 40):
        for y in (580, 1220):
            b += C(x, y, 12, gf) + C(x, y, 5, "#0B3D35")
    b += confetti(a, 40, (40, 1230, W - 40, 1330), ["#FFD36B", "#F48FB1", "#4DD0E1"], seed=12, size=(8, 14))
    b += bokeh(a, 20, (0, 600, W, H), ["#FFD36B", "#6FE0C4"], (20, 60), (0.08, 0.2), avoid=[(80, 590, 1000, 1210)], seed=13)
    return a.svg(b), spec(10, zone, "gold", "#F3FFF9", "#FFD36B", tone="dark", tfont="script")


CARDS = [card1, card2, card3, card4, card5, card6, card7, card8, card9, card10]

if __name__ == "__main__":
    only = [int(x) for x in sys.argv[1:]]
    arts, specs = {}, []
    for i, fn in enumerate(CARDS, 1):
        svg, sp = fn()
        specs.append(sp)
        if not only or i in only:
            arts[sp["id"]] = svg
    check_spec(specs, False)
    write_spec(CAT, specs)
    render_cards(arts)
