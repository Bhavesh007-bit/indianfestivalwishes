"""Shop / business opening invitations: storefront, awning, ribbon + scissors, gold coins, starburst, confetti, keys."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_f import *
from render import render_cards

CAT = "inv-shop-opening"
SPECS = []
GOLDC = ("#F9E39A", "#E7B83E", "#FFF1B0", "#C8962E", "#FFFFFF")


def S(n, zone, title, text, accent, **kw):
    SPECS.append(spec(CAT, n, zone, title, text, accent, **kw))


def ribbon_across(x0, x1, y, w=40, c=("#8E0B18", "#D7263D", "#FF6B6B"), wave=10):
    f = lin([c[0], c[1], c[2], c[1], c[0]], 0, 0, 0, 1)
    top = "M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f" % (x0, y - w / 2, (x0 * 2 + x1) / 3, y - w / 2 - wave, (x0 + 2 * x1) / 3, y - w / 2 + wave, x1, y - w / 2)
    bot = "L%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1fZ" % (x1, y + w / 2, (x0 + 2 * x1) / 3, y + w / 2 + wave, (x0 * 2 + x1) / 3, y + w / 2 - wave, x0, y + w / 2)
    return ('<g filter="url(#shs)"><path d="%s %s" fill="%s"/><path d="M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f" stroke="#FFD27A" stroke-width="2.5" fill="none" opacity=".8"/></g>'
            % (top, bot, f, x0, y - w / 2 + 5, (x0 * 2 + x1) / 3, y - w / 2 - wave + 5, (x0 + 2 * x1) / 3, y - w / 2 + wave + 5, x1, y - w / 2 + 5))


def coin_rain(rng, box, n, rmin=14, rmax=30, avoid=None):
    x0, y0, x1, y1 = box
    out = []
    k = t = 0
    while k < n and t < n * 30:
        t += 1
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if avoid and any(a[0] - 30 <= x <= a[2] + 30 and a[1] - 30 <= y <= a[3] + 30 for a in avoid):
            continue
        k += 1
        out.append(coin(x, y, rng.uniform(rmin, rmax), rng.uniform(.35, 1), rng.uniform(-60, 60), rng.random() < .6))
    return '<g filter="url(#shs)">%s</g>' % "".join(out)


def key_ring(cx, cy, s=1, ribbon="#C1121F"):
    out = ['<g transform="translate(%.1f %.1f) scale(%.3f)">' % (cx, cy, s)]
    for ang in (62, 118, 90):
        a = math.radians(ang)
        out.append(ornate_key(118 * math.cos(a), 118 * math.sin(a), 380 if ang == 90 else 330, ang, None))
    out.append('<circle r="72" fill="none" stroke="#6E440A" stroke-width="16"/><circle r="72" fill="none" stroke="%s" stroke-width="11"/>' % gold())
    out.append(ribbon_bow(0, -74, .75, (ribbon, "#E53945", "#FF8A8A")))
    out.append('</g>')
    return "".join(out)


# ------------------------------------------------------------------ 1
def card1():
    """Cream and red: the decorated storefront with ribbon across the door; gold confetti; panel below."""
    rng = random.Random(1)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#FFE7C7", "#FFF6EA"], 0, 0, 0, 1)]
    b.append(rays(540, 260, 32, 900, "#FFFFFF", .6, .45))
    b.append('<path d="M0 470 H1080 V520 H0Z" fill="#E8CFA8"/>')
    b.append(storefront(160, 20, 760, 470, ("#C62828", "#FFF6E5"), seed=3))
    b.append(toran(190, 890, 24, 34, hues=("orange", "yellow")))
    b.append(kalash(90, 500, 200, "brass") + kalash(990, 500, 200, "brass"))
    b.append(confetti(rng, (0, 0, 1080, 480), 70, GOLDC + ("#D7263D",), avoid=[(160, 20, 920, 490)]))
    b.append(panel_rect(60, 505, 1020, 1310, 24, "#FFFBF4", lin(["#8E0B18", "#D7263D", "#8E0B18"], 0, 0, 1, 0), "#E7B83E"))
    b.append(starburst(990, 540, 60, 20, .8) + starburst(90, 540, 44, 18, .8))
    S(1, [100, 560, 980, 1265], "#B3121D", "#33201C", "#B7791F", tfont="deco")
    return card("".join(b))


# ------------------------------------------------------------------ 2
def card2():
    """Midnight navy: layered gold grand-opening starburst, ribbon being cut, gold confetti; glass panel."""
    rng = random.Random(2)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % rad(["#243B6B", "#131F42", "#0A1128"], .5, .25, .9)]
    b.append(rays(540, 260, 40, 1000, "#F9E39A", .25, .35))
    b.append('<circle cx="540" cy="260" r="260" fill="#F9E39A" opacity=".25" filter="url(#b30)"/>')
    b.append('<g filter="url(#sh)">%s</g>' % starburst(540, 260, 235, 28, .86, rot=4))
    b.append(starburst(540, 260, 200, 28, .9, lin(["#B07A1C", "#F9E39A", "#C8962E"], 0, 0, 1, 1), "#FFF1B0", rot=10))
    b.append('<circle cx="540" cy="260" r="150" fill="%s" stroke="%s" stroke-width="6"/>' % (rad(["#1E3366", "#0E1838"], .4, .35, .8), gold()))
    b.append('<circle cx="540" cy="260" r="132" fill="none" stroke="#F9E39A" stroke-width="2" stroke-dasharray="2 8"/>')
    for k in range(5):
        a = math.radians(-90 + (k - 2) * 26)
        b.append(sparkle(540 + 80 * math.cos(a), 250 + 80 * math.sin(a), .8, "#F9E39A"))
    # blank banner across the badge
    b.append('<path d="M300 268 L360 268 L346 300 L360 332 L300 332 L318 300Z" fill="#8E0B18"/><path d="M780 268 L720 268 L734 300 L720 332 L780 332 L762 300Z" fill="#8E0B18"/>')
    b.append('<path d="M350 250 H730 V316 H350Z" fill="%s" filter="url(#shs)"/>' % lin(["#8E0B18", "#D7263D", "#8E0B18"], 0, 0, 0, 1))
    b.append('<path d="M350 258 H730 M350 308 H730" stroke="#F9E39A" stroke-width="3"/>')
    b.append('<circle cx="540" cy="283" r="10" fill="%s"/>' % gold())
    # ribbon across and scissors
    b.append(ribbon_across(-10, 1090, 490, 42))
    b.append(scissors(840, 486, .75, 188))
    b.append(confetti(rng, (0, 0, 1080, 1350), 120, GOLDC, avoid=[(60, 520, 1020, 1310), (290, 20, 790, 500)]))
    b.append(panel_rect(60, 525, 1020, 1310, 30, "#0F1A3A", gold(), "#C8962E", texture=False, op=.9))
    S(2, [100, 565, 980, 1265], "gold", "#F3ECDA", "#F2C94C", tone="dark", tfont="deco")
    return card("".join(b))


# ------------------------------------------------------------------ 3
def card3():
    """Emerald: a sweeping red ribbon with a big bow across the top, gold scissors about to cut, coins."""
    rng = random.Random(3)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#0C5C45", "#084434"], 0, 0, 0, 1)]
    b.append('<rect width="1080" height="1350" fill="%s"/>' % stripes_pattern("st3", "#FFFFFF00", "#FFFFFF08", 30, 45))
    b.append(coin_rain(rng, (20, 10, 1060, 460), 16, avoid=[(0, 150, 1080, 360)]))
    b.append(ribbon_band(-40, 170, 1120, 320, 86))
    b.append(scissors(930, 330, .85, 200))
    b.append(panel_rect(60, 440, 1020, 1310, 24, "#FFFBF2", gold(), "#E7B83E"))
    b.append(ribbon_bow(470, 232, 1.25))
    b.append(confetti(rng, (0, 440, 1080, 1350), 40, GOLDC, avoid=[(40, 420, 1040, 1320)]))
    S(3, [100, 485, 980, 1265], "#0C5C45", "#22302A", "#B3121D", tfont="classic")
    return card("".join(b))


# ------------------------------------------------------------------ 4
def card4():
    """The card is the shop: teal awning on top, the text sits in the big shop window, plants and kalash at the step."""
    rng = random.Random(4)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#F3E7D3", "#E3CFAF"], 0, 0, 0, 1)]
    b.append('<rect width="1080" height="1350" fill="%s"/>' % brick_pattern("br4", "#EAD8BC", "#E2CCAC", "#F3E7D3", 80, 30))
    # window
    b.append('<rect x="56" y="210" width="968" height="880" rx="10" fill="%s" filter="url(#shp)"/>' % lin(["#3E2723", "#6D4C41", "#3E2723"], 0, 0, 1, 0))
    b.append('<rect x="80" y="234" width="920" height="832" fill="%s"/>' % lin(["#FFFDF6", "#FFF3DE"], 0, 0, 0, 1))
    b.append('<path d="M80 234 L300 234 L80 600Z" fill="#fff" opacity=".7"/><path d="M1000 700 L1000 1066 L820 1066Z" fill="#E9D8B8" opacity=".35"/>')
    b.append('<rect x="80" y="234" width="920" height="832" fill="none" stroke="%s" stroke-width="4"/>' % gold())
    b.append('<rect x="40" y="1086" width="1000" height="26" rx="6" fill="%s"/>' % lin(["#6D4C41", "#3E2723"], 0, 0, 0, 1))
    # awning full width
    b.append('<rect x="0" y="0" width="1080" height="40" fill="#3E2723"/>')
    b.append(awning(-30, 30, 1140, 150, "#00796B", "#FFF6E5", 12))
    b.append(garland_swag(60, 214, 540, 214, 40, 12) + garland_swag(540, 214, 1020, 214, 40, 12, ("yellow", "orange")))
    # step
    b.append('<rect x="0" y="1112" width="1080" height="238" fill="%s"/>' % lin(["#BCAAA4", "#8D7B74"], 0, 0, 0, 1))
    b.append(plant_pot(90, 1262, 1.3, "#00796B", kind="leafy") + plant_pot(990, 1262, 1.3, "#00796B", kind="leafy"))
    b.append(kalash(240, 1262, 220, "copper") + money_pot(840, 1262, 190, "brass"))
    b.append(ribbon_across(56, 1024, 1110, 26, wave=4))
    b.append(ribbon_bow(540, 1112, .55))
    S(4, [120, 280, 960, 1020], "#00695C", "#2C2522", "#C62828", tfont="deco")
    return card("".join(b))


# ------------------------------------------------------------------ 5
def card5():
    """Maroon and gold: overflowing money pot and shubh kalash below, coin stacks, gold confetti."""
    rng = random.Random(5)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#4A0A14", "#7A1022", "#4A0A14"], 0, 0, 1, 1)]
    b.append('<rect width="1080" height="1350" fill="%s"/>' % floral_pattern("fp5", "#F2C94C", .1, 100))
    b.append('<ellipse cx="540" cy="1150" rx="560" ry="200" fill="#F2C94C" opacity=".22" filter="url(#b30)"/>')
    b.append(money_pot(260, 1262, 430, "brass"))
    b.append('<ellipse cx="850" cy="1262" rx="140" ry="22" fill="%s"/>' % lin(METAL["brass"], 0, 0, 1, 0))
    b.append(kalash(850, 1258, 380, "brass"))
    b.append(coin_stack(560, 1262, 46, 7) + coin_stack(640, 1262, 38, 4) + coin_stack(520, 1266, 30, 2) if False else coin_stack(560, 1240, 44, 7) + coin_stack(660, 1250, 36, 4))
    b.append(confetti(rng, (0, 820, 1080, 1340), 50, GOLDC, avoid=[(330, 1270, 750, 1350)]))
    b.append(panel_rect(50, 40, 1030, 820, 30, "#FFF9EC", gold(), "#E7B83E"))
    for x, y, r in ((74, 64, 0), (1006, 64, 90), (1006, 796, 180), (74, 796, 270)):
        b.append(corner_flourish(x, y, .5, r))
    S(5, [90, 80, 990, 780], "#7A1022", "#33201C", "#B7791F", tfont="deco")
    return card("".join(b))


# ------------------------------------------------------------------ 6
def card6():
    """Terracotta brick wall; a big blank shop board hangs on chains; plants, coins and confetti below."""
    rng = random.Random(6)
    b = ['<rect width="1080" height="1350" fill="#A8472A"/>']
    b.append('<rect width="1080" height="1350" fill="%s"/>' % brick_pattern("br6"))
    b.append('<rect width="1080" height="1350" fill="%s"/>' % rad([(0, "#FFE0B0", .35), (.6, "#000", 0), (1, "#000", .35)], .5, .4, .8))
    # rod with brackets
    b.append('<rect x="60" y="56" width="960" height="18" rx="9" fill="%s" filter="url(#shs)"/>' % gold(0, 0, 0, 1))
    for x in (60, 1020):
        b.append('<circle cx="%d" cy="65" r="22" fill="%s" stroke="#6E440A" stroke-width="3"/>' % (x, gold()))
    for x in (200, 880):
        for k in range(8):
            y = 76 + k * 15
            b.append('<ellipse cx="%d" cy="%d" rx="%.1f" ry="9" fill="none" stroke="%s" stroke-width="4"/>' % (x, y, 6 if k % 2 else 2.5, gold()))
    # board
    b.append('<rect x="80" y="190" width="920" height="850" rx="26" fill="%s" filter="url(#shp)"/>' % lin(["#5D3A1A", "#8B5A2B", "#5D3A1A"], 0, 0, 1, 1))
    b.append('<rect x="104" y="214" width="872" height="802" rx="16" fill="#FFF8EA"/><rect x="104" y="214" width="872" height="802" rx="16" fill="#FFF8EA" filter="url(#paper)"/>')
    b.append('<rect x="120" y="230" width="840" height="770" rx="10" fill="none" stroke="%s" stroke-width="4"/>' % gold())
    for x in (200, 880):
        b.append('<circle cx="%d" cy="202" r="10" fill="%s"/>' % (x, gold()))
    b.append(garland_swag(110, 200, 540, 200, 30, 11) + garland_swag(540, 200, 970, 200, 30, 11, ("yellow", "orange")))
    # pavement and props
    b.append('<rect y="1110" width="1080" height="240" fill="%s"/>' % lin(["#7A6A60", "#5A4C44"], 0, 0, 0, 1))
    b.append('<path d="M0 1110 H1080" stroke="#C9B8A8" stroke-width="6"/>')
    b.append(plant_pot(110, 1262, 1.5, "#6D4C41", kind="leafy") + plant_pot(970, 1262, 1.5, "#6D4C41", kind="leafy"))
    b.append(money_pot(290, 1262, 200) + coin_stack(800, 1250, 40, 6))
    b.append(confetti(rng, (0, 0, 1080, 1340), 70, GOLDC, avoid=[(80, 180, 1000, 1050), (330, 1260, 750, 1350)]))
    S(6, [150, 260, 930, 980], "#8B3A1A", "#3A2A20", "#B7791F", tfont="deco")
    return card("".join(b))


# ------------------------------------------------------------------ 7
def card7():
    """Royal purple: a ring of golden shop keys with a red bow, coins raining, panel below."""
    rng = random.Random(7)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#3A0F5C", "#5B1A7E", "#2A0A44"], 0, 0, 1, 1)]
    b.append(rays(760, 200, 36, 900, "#F9E39A", .25, .4))
    b.append('<circle cx="760" cy="200" r="240" fill="#F9E39A" opacity=".2" filter="url(#b30)"/>')
    b.append(coin_rain(rng, (30, 20, 520, 440), 14, avoid=[(560, 20, 1060, 460)]))
    b.append(key_ring(760, 110, .8))
    b.append(confetti(rng, (0, 0, 1080, 1350), 90, GOLDC, avoid=[(50, 480, 1030, 1310), (560, 40, 1060, 470)]))
    b.append(panel_rect(50, 480, 1030, 1310, 30, "#FFF9F0", gold(), "#C9A0DC"))
    b.append(starburst(90, 500, 50, 18, .8))
    S(7, [90, 520, 990, 1265], "#4A1470", "#2E2338", "#B7791F", tfont="classic")
    return card("".join(b))


# ------------------------------------------------------------------ 8
def card8():
    """Blue-sky market street: three shopfronts, the middle one ribboned and garlanded; panel in the sky."""
    rng = random.Random(8)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#6EC6F0", "#BDE8F7", "#FFF4DE"], 0, 0, 0, 1)]
    for x, y, s in ((140, 880, 1), (900, 860, 1.2)):
        b.append('<g opacity=".9"><ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="#fff"/><ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="#fff"/></g>' % (x, y, 70 * s, 26 * s, x + 50 * s, y - 16 * s, 50 * s, 30 * s))
    b.append('<rect y="1240" width="1080" height="110" fill="%s"/>' % lin(["#B0A090", "#8A7A6A"], 0, 0, 0, 1))
    b.append(storefront(0, 960, 350, 290, ("#1565C0", "#FFFFFF"), seed=8, ribbon=False, sign=False, wall=("#E3F2FD", "#BBDEFB")))
    b.append(storefront(730, 960, 350, 290, ("#2E7D32", "#FFFFFF"), seed=9, ribbon=False, sign=False, wall=("#F1F8E9", "#DCEDC8")))
    b.append(storefront(330, 880, 420, 370, ("#C62828", "#FFF6E5"), seed=10))
    b.append(toran(350, 730, 884, 28))
    b.append(confetti(rng, (0, 840, 1080, 1250), 40, GOLDC + ("#D7263D",), avoid=[(0, 950, 1080, 1260)]))
    b.append(panel_rect(50, 40, 1030, 830, 30, "#FFFFFF", gold(), "#90CAF9", op=.96))
    b.append(starburst(1010, 60, 48, 18, .8) + starburst(70, 60, 40, 18, .8))
    S(8, [90, 80, 990, 790], "#0D47A1", "#1E2A36", "#C62828", tfont="deco")
    return card("".join(b))


# ------------------------------------------------------------------ 9
def card9():
    """Photo of the shop in a window frame under a striped awning, ribbon and bow below; cream panel."""
    rng = random.Random(9)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#FFF1E0", "#FFE0C2"], 0, 0, 0, 1)]
    b.append('<rect width="1080" height="1350" fill="%s"/>' % dots_pattern("dp9", "#E65100", .18, 28))
    px, py, pw, ph = 230, 120, 620, 330
    b.append('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" filter="url(#shp)"/>' % (px - 22, py - 22, pw + 44, ph + 44, lin(["#3E2723", "#6D4C41", "#3E2723"], 0, 0, 1, 0)))
    b.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (px, py, pw, ph, lin(["#FFF8EE", "#F7E2C4"], 0, 0, 1, 1)))
    b.append(products_shelf(px + 20, py + 20, pw - 40, ph - 40, rng))
    b.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#FFF8EE" opacity=".55"/>' % (px, py, pw, ph))
    b.append(awning(px - 60, 30, pw + 120, 100, "#E65100", "#FFF6E5", 10))
    b.append(ribbon_across(20, 1060, 476, 30, wave=6))
    b.append(ribbon_bow(540, 476, .6, ("#8E0B18", "#D7263D", "#FF6B6B")))
    b.append(coin_stack(110, 440, 40, 7) + coin_stack(970, 440, 40, 5) + coin(160, 300, 30, .9, 10) + coin(930, 290, 26, .9, -20))
    b.append(confetti(rng, (0, 0, 1080, 500), 40, GOLDC + ("#E65100",), avoid=[(150, 20, 930, 470)]))
    b.append(panel_rect(60, 505, 1020, 1310, 24, "#FFFBF5", lin(["#E65100", "#F2C94C"], 0, 0, 1, 0), "#F2C9A0"))
    S(9, [100, 545, 980, 1265], "#BF360C", "#33241C", "#B7791F", tfont="deco",
      photo={"shape": "rect", "x": px, "y": py, "w": pw, "h": ph})
    return card("".join(b))


# ------------------------------------------------------------------ 10
def card10():
    """Golden hour: rolling shutter raised on a lit shop, marigold toran; hang-tag shaped panel on a string."""
    rng = random.Random(10)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#2D2A32", "#3F3A44"], 0, 0, 0, 1)]
    b.append('<rect width="1080" height="1350" fill="%s"/>' % brick_pattern("br10", "#4A434F", "#423C47", "#2D2A32", 90, 34))
    # shop opening
    b.append('<rect x="120" y="40" width="840" height="420" fill="%s"/>' % rad(["#FFF6D8", "#FFD98A", "#E0A040"], .5, .7, .8))
    b.append(products_shelf(150, 200, 300, 240, rng) + products_shelf(630, 200, 300, 240, rng))
    b.append('<rect x="470" y="220" width="140" height="240" fill="%s"/>' % lin(["#FFFBEA", "#FFE3A0"], 0, 0, 0, 1))
    # shutter (raised) with slats
    b.append('<rect x="120" y="40" width="840" height="140" fill="%s"/>' % lin(["#9EA7B0", "#D5DCE2", "#8A939C"], 0, 0, 0, 1))
    for k in range(9):
        b.append('<path d="M120 %d H960" stroke="#6E767E" stroke-width="3"/>' % (52 + k * 15))
    b.append('<rect x="440" y="166" width="200" height="14" rx="7" fill="#5A6068"/>')
    b.append('<rect x="100" y="30" width="20" height="440" fill="#1E1B22"/><rect x="960" y="30" width="20" height="440" fill="#1E1B22"/>')
    b.append('<rect x="80" y="0" width="920" height="40" fill="%s"/>' % lin(["#3E2723", "#6D4C41"], 0, 0, 0, 1))
    b.append(toran(100, 980, 180, 36))
    b.append('<path d="M120 460 L0 560 H1080 L960 460Z" fill="#FFD98A" opacity=".18"/>')
    b.append(ribbon_across(100, 980, 380, 32, wave=5))
    b.append(ribbon_bow(540, 380, .6))
    b.append('<rect x="0" y="460" width="1080" height="20" fill="#1E1B22"/>')
    # tag panel on a string
    tag = "M140 500 H940 L1020 580 V1310 H60 V580Z"
    b.append('<path d="M540 520 C520 470 560 430 540 395" stroke="%s" stroke-width="4" fill="none"/>' % gold())
    b.append('<path d="%s" fill="#FFF8E8" filter="url(#shp)"/><path d="%s" fill="#FFF8E8" filter="url(#paper)"/>' % (tag, tag))
    b.append('<path d="M150 516 H930 L1004 590 V1296 H76 V590Z" fill="none" stroke="%s" stroke-width="5"/>' % gold())
    b.append('<circle cx="540" cy="532" r="15" fill="#2D2A32" stroke="%s" stroke-width="6"/>' % gold())
    b.append(confetti(rng, (0, 480, 1080, 1350), 40, GOLDC, avoid=[(50, 490, 1030, 1320)]))
    S(10, [100, 565, 980, 1265], "#6B2A0C", "#2F2A26", "#B7791F", tfont="deco")
    return card("".join(b))


if __name__ == "__main__":
    fns = [card1, card2, card3, card4, card5, card6, card7, card8, card9, card10]
    only = [int(a) for a in sys.argv[1:]]
    arts = {}
    for i, f in enumerate(fns, 1):
        svg = f()
        if not only or i in only:
            arts["E-%s-%d" % (CAT, i)] = svg
    write_specs(CAT, SPECS)
    render_cards(arts)
