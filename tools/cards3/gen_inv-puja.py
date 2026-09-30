"""Puja / Satyanarayan katha invitations: temple, kalash, thali, bells, shankh, banana plants, havan, lotus, om."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_f import *
from render import render_cards

CAT = "inv-puja"
SPECS = []


def S(n, zone, title, text, accent, **kw):
    SPECS.append(spec(CAT, n, zone, title, text, accent, **kw))


def banana_bunch(cx, cy, s=1, rot=0):
    out = ['<g transform="translate(%.1f %.1f) rotate(%.1f) scale(%.3f)" filter="url(#shs)">' % (cx, cy, rot, s)]
    for k in range(6):
        a = -40 + k * 16
        out.append('<g transform="rotate(%d)"><path d="M0 0 C30 -10 70 -40 86 -90 C90 -100 84 -104 78 -96 C60 -56 30 -28 -4 -12Z" fill="%s" stroke="#8A6A10" stroke-width="1.5"/>'
                   '<path d="M84 -96 l6 -10" stroke="#4E3A08" stroke-width="5" stroke-linecap="round"/></g>' % (a, lin(["#C9A21A", "#F7D548", "#FFF0A0"], 0, 1, 1, 0)))
    out.append('<circle r="12" fill="#6B5A1A"/></g>')
    return "".join(out)


def thali_top(cx, cy, r, seed=1):
    """Brass plate seen from above with bowls, rice, marigolds and a lit diya."""
    rng = random.Random(seed)
    m = METAL["brass"]
    out = ['<g filter="url(#sh)"><circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r, lin(m, 0, 0, 1, 1))]
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r * .86, lin(m[::-1], 0, 0, 1, 1)))
    for k in range(40):
        a = math.radians(k * 9)
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#FFF3C0"/>' % (cx + r * .93 * math.cos(a), cy + r * .93 * math.sin(a), r * .018))
    out.append('</g>')
    for (dx, dy, c) in ((-.4, -.3, "#C1121F"), (.05, -.48, "#F2B705"), (.42, -.22, "#E65100")):
        x, y = cx + dx * r, cy + dy * r
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/><circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (x, y, r * .16, lin(m, 0, 0, 1, 1), x, y, r * .12, c))
    for _ in range(40):
        a, rr = rng.uniform(0, 6.28), rng.uniform(0, r * .16)
        out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#FFFDF2" transform="rotate(%d %.1f %.1f)"/>' % (cx - r * .35 + rr * math.cos(a), cy + r * .3 + rr * math.sin(a), r * .025, r * .012, rng.randint(0, 180), cx - r * .35 + rr * math.cos(a), cy + r * .3 + rr * math.sin(a)))
    out.append(marigold(cx + r * .2, cy + r * .38, r * .13, "orange") + marigold(cx + r * .45, cy + r * .2, r * .11, "yellow"))
    # diya top-down
    out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s"/>' % (cx, cy + r * .02, r * .2, r * .15, lin(["#6E2A08", "#C0602A", "#6E2A08"], 0, 0, 1, 1)))
    out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#4a1d05"/>' % (cx, cy + r * .02, r * .14, r * .09))
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#FFB02E" opacity=".6" filter="url(#b6)"/>' % (cx + r * .14, cy, r * .12))
    out.append(diya_flame(cx + r * .15, cy + r * .02, r / 200))
    return "".join(out)


def kalash_top(cx, cy, r):
    out = ['<g filter="url(#sh)">']
    for k in range(9):
        out.append(mango_leaf(cx, cy, r * 1.05, k * 40 + 10))
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="3"/>' % (cx, cy, r * .62, lin(METAL["copper"], 0, 0, 1, 1), METAL["copper"][0]))
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r * .4, rad(["#A0612B", "#6B3A15", "#3E1E08"], .4, .35, .7)))
    for k in range(12):
        a = math.radians(k * 30)
        out.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="#C88B4A" stroke-width="2" opacity=".6"/>' % (cx, cy, cx + r * .38 * math.cos(a), cy + r * .38 * math.sin(a)))
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#C1121F" opacity=".85"/>' % (cx, cy, r * .09))
    out.append('</g>')
    return "".join(out)


def lotus_mandala(cx, cy, r, c=("#7B1FA2", "#C2185B", "#F8BBD0")):
    out = []
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#FFD27A" opacity=".45" filter="url(#b30)"/>' % (cx, cy, r * 1.2))
    for ring, (n, rr, rot, col) in enumerate(((20, r, 0, c[0]), (16, r * .82, 11, c[1]), (12, r * .64, 0, c[2]))):
        f = lin([col, "#FFFFFF"], 0, 0, 0, 1) if ring == 2 else lin([col, c[2]], 0, 0, 0, 1)
        for k in range(n):
            a = k * 360.0 / n + rot
            out.append('<path d="M0 %.1f C%.1f %.1f %.1f %.1f 0 %.1f C%.1f %.1f %.1f %.1f 0 %.1fZ" transform="translate(%.1f %.1f) rotate(%.1f)" fill="%s" stroke="%s" stroke-width="2.5"/>'
                       % (-rr * .45, rr * .2, -rr * .6, rr * .12, -rr * .9, -rr, -rr * .12, -rr * .9, -rr * .2, -rr * .6, -rr * .45, cx, cy, a, f, "#E9B949"))
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="6"/>' % (cx, cy, r * .5, rad(["#3A0F4A", "#1E0628"], .5, .4, .7), gold()))
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#E9B949" stroke-width="1.5" stroke-dasharray="3 6"/>' % (cx, cy, r * .44))
    out.append(om_symbol(cx, cy + r * .02, r * .55, stroke="#6B420A"))
    return "".join(out)


# ------------------------------------------------------------------ 1
def card1():
    """Saffron sunrise behind a stone temple; bells in the corners; banana leaves; cream panel with temple band."""
    rng = random.Random(1)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#FF8A3D", "#FFB65C", "#FFE3AE"], 0, 0, 0, 1)]
    b.append('<circle cx="540" cy="300" r="170" fill="#FFF3C8"/><circle cx="540" cy="300" r="240" fill="#FFF3C8" opacity=".5" filter="url(#b30)"/>')
    b.append(rays(540, 300, 36, 900, "#FFFFFF", .45, .45))
    b.append('<path d="M0 420 C200 380 360 400 540 390 C720 380 880 390 1080 410 V520 H0Z" fill="#E08A3C" opacity=".55"/>')
    b.append(banana_plant(-10, 520, 520, seed=3, tone=0))
    b.append(banana_plant(1090, 520, 520, flip=True, seed=4, tone=1, flower=True))
    b.append(temple(540, 500, 460, flag="#E65100"))
    b.append(temple_bell(170, -10, 60, 120) + temple_bell(910, -10, 60, 120))
    # panel with carved temple band
    b.append(panel_rect(60, 500, 1020, 1310, 20, "#FFF8EA", lin(["#8A2B00", "#C8962E", "#8A2B00"], 0, 0, 1, 0), "#E7B45A"))
    band = border_band("bb1", "#8A2B00", "#F4C542", "#FFE9B0", 34)
    b.append('<rect x="60" y="496" width="960" height="34" fill="%s" filter="url(#shs)"/>' % band)
    b.append(bead_line(70, 1296, 1010, 1296, 22, 4) if False else "")
    S(1, [100, 560, 980, 1265], "#8A2B00", "#3A2318", "#C0561A", tfont="deco")
    return card("".join(b))


# ------------------------------------------------------------------ 2
def card2():
    """Satyanarayan mandap: tall banana plants frame the card, kalash on top, chowki with thali and fruits."""
    rng = random.Random(2)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#6E0B14", "#8E1A1A", "#5A0810"], 0, 0, 0, 1)]
    b.append('<rect width="1080" height="1350" fill="%s"/>' % floral_pattern("fp2", "#F4C542", .1, 90))
    b.append('<g transform="translate(70 0) scale(.62 1) translate(-70 0)">%s</g>' % banana_plant(70, 1300, 1150, seed=11, tone=0))
    b.append('<g transform="translate(1010 0) scale(.62 1) translate(-1010 0)">%s</g>' % banana_plant(1010, 1300, 1150, flip=True, seed=12, tone=2))
    # silk backdrop
    b.append('<rect x="110" y="250" width="860" height="800" rx="14" fill="%s" filter="url(#shp)"/>' % lin(["#FFF7DE", "#FFEFC4"], 0, 0, 0, 1))
    b.append('<rect x="110" y="250" width="860" height="800" rx="14" fill="#FFF7DE" filter="url(#paper)" opacity=".7"/>')
    b.append(frame_lines(126, 266, 954, 1034, "#B71C1C", "#E0A43A"))
    b.append(toran(90, 990, 244, 44))
    # kalash on top centre with small garland
    b.append('<ellipse cx="540" cy="232" rx="110" ry="20" fill="%s"/>' % lin(METAL["brass"], 0, 0, 1, 0))
    b.append(kalash(540, 228, 220, "brass"))
    b.append(garland_swag(110, 250, 540, 250, 0, 10) if False else "")
    # chowki with thali and fruit
    b.append(chowki(540, 1262, 760, 150, "#B71C1C", "#F4C542"))
    b.append(thali(540, 1098, 150, "brass", seed=3))
    b.append(banana_bunch(290, 1106, .8, -20) + coconut(790, 1090, .6) + coconut(850, 1098, .5))
    b.append(marigold(230, 1112, 16) + marigold(900, 1112, 16, "yellow"))
    S(2, [150, 295, 930, 1005], "#9E1B1B", "#3A2318", "#B7791F", tfont="deco")
    return card("".join(b))


def frame_lines(x0, y0, x1, y1, c1, c2=None, r=8):
    c2 = c2 or c1
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="none" stroke="%s" stroke-width="5"/>'
            '<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="none" stroke="%s" stroke-width="2"/>'
            % (x0, y0, x1 - x0, y1 - y0, r, c1, x0 + 10, y0 + 10, x1 - x0 - 20, y1 - y0 - 20, r, c2))


# ------------------------------------------------------------------ 3
def card3():
    """Night havan: glowing havan kund with flames at the bottom, kalash and shankh beside, text on smoky dark."""
    rng = random.Random(3)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#12060A", "#2A0A0A", "#4A1408"], 0, 0, 0, 1)]
    b.append('<ellipse cx="540" cy="1150" rx="620" ry="380" fill="#FF6A00" opacity=".35" filter="url(#b30)"/>')
    b.append('<g filter="url(#b6)">%s</g>' % (smoke(60, 1150, 1000, 1.6, .1, 3, "#FFE0C0", 6) + smoke(1020, 1150, 1000, 1.6, .1, 5, "#FFE0C0", 6)))
    b.append('<ellipse cx="540" cy="1060" rx="380" ry="200" fill="#FF7A00" opacity=".3" filter="url(#b30)"/>')
    b.append(havan_kund(540, 1255, 520, "copper", seed=4, fire_h=250, spark_n=0, rich=True))
    b.append(kalash(150, 1262, 260, "brass"))
    b.append('<rect x="850" y="1180" width="160" height="80" rx="10" fill="%s"/>' % lin(["#6B420A", "#B98320", "#6B420A"], 0, 0, 1, 0))
    b.append(shankh(930, 1150, .42, -8))
    b.append(toran(-10, 1090, 10, 46, hues=("orange", "yellow")))
    for x, y, r in ((40, 90, 0), (1040, 90, 90), (1040, 1310, 180), (40, 1310, 270)):
        b.append(corner_flourish(x, y, .55, r, op=.9))
    b.append(stars(rng, (20, 60, 1060, 900), 30, "#FFC266", avoid=[(100, 70, 980, 790)], op=(.3, .8)))
    S(3, [110, 80, 970, 780], "gold", "#FFEBD2", "#FFB74D", tone="dark", tfont="classic")
    return card("".join(b))


# ------------------------------------------------------------------ 4
def card4():
    """Five brass bells from a carved beam over an ivory panel on red jaali; shankh and lotus below."""
    rng = random.Random(4)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#8E0E1C", "#6A0A14"], 0, 0, 0, 1)]
    b.append('<rect width="1080" height="1350" fill="%s"/>' % jaali_pattern("jl4", "#F4C542", .18, 64))
    b.append('<rect x="0" y="0" width="1080" height="1350" fill="%s"/>' % rad([(0, "#000", 0), (1, "#000", .35)], .5, .5, .8))
    b.append(bell_beam(10, 1070, 20, [(130, 70, 120), (335, 120, 140), (540, 160, 150), (745, 120, 140), (950, 70, 120)]))
    b.append(garland_swag(10, 60, 335, 60, 60, 11) + garland_swag(335, 60, 745, 60, 70, 11, ("yellow", "orange")) + garland_swag(745, 60, 1070, 60, 60, 11))
    b.append(panel_rect(60, 390, 1020, 1180, 26, "#FFF9EE", gold(), "#D9A64C"))
    b.append(corner_flourish(80, 410, .45, 0) + corner_flourish(1000, 410, .45, 90) + corner_flourish(1000, 1160, .45, 180) + corner_flourish(80, 1160, .45, 270))
    b.append(shankh(200, 1245, .55, -6))
    b.append(lotus(880, 1270, .55, leaves=True) + lotus(1010, 1270, .4))
    b.append(petals(rng, (0, 1190, 1080, 1340), 26, avoid=[(330, 1260, 750, 1350)]))
    S(4, [100, 430, 980, 1140], "#8E0E1C", "#3A1A1A", "#B7791F", tfont="deco")
    return card("".join(b))


# ------------------------------------------------------------------ 5
def card5():
    """Magenta mandala ground; big brass puja thali with incense smoke up top; lotus-petal crown panel."""
    rng = random.Random(5)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#6E0E3E", "#A3175A", "#C2185B"], 0, 0, 1, 1)]
    for r in (520, 420, 320):
        b.append('<circle cx="540" cy="300" r="%d" fill="none" stroke="#FFD27A" stroke-opacity=".18" stroke-width="2" stroke-dasharray="4 10"/>' % r)
    b.append(rays(540, 300, 40, 800, "#FFD27A", .25, .35))
    b.append(incense(840, 250, 150, 3, "#FFFFFF", .45) + incense(240, 250, 150, 5, "#FFFFFF", .45))
    b.append(thali(540, 300, 320, "brass", seed=7))
    b.append(petals(rng, (0, 0, 1080, 480), 50, ("#FFD54F", "#FF8A65", "#FFFFFF", "#F48FB1"), avoid=[(200, 180, 880, 420)]))
    # panel with lotus-petal crown
    for k in range(17):
        x = 80 + k * 57.5
        h = 46 if k % 2 else 34
        b.append('<path d="M%.1f 492 C%.1f %.1f %.1f %.1f %.1f %.1f C%.1f %.1f %.1f %.1f %.1f 492Z" fill="%s" stroke="%s" stroke-width="2"/>'
                 % (x - 30, x - 28, 492 - h * .6, x - 8, 492 - h, x, 492 - h - 6, x + 8, 492 - h, x + 28, 492 - h * .6, x + 30, lin(["#F8BBD0", "#FFF5F8"], 0, 1, 0, 0), "#E9B949"))
    b.append(panel_rect(60, 490, 1020, 1310, 18, "#FFF6F8", gold(), "#F2B8C6"))
    S(5, [100, 530, 980, 1265], "#8E1446", "#3A1E2A", "#C2185B", tfont="script")
    return card("".join(b))


# ------------------------------------------------------------------ 6
def card6():
    """Indigo night: plum velvet panel on top, glowing Om inside a layered lotus mandala below."""
    rng = random.Random(6)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#1A0F3C", "#2E145A", "#44106A"], 0, 0, 0, 1)]
    b.append(rays(540, 1040, 40, 900, "#FFD27A", .3, .4))
    b.append(stars(rng, (0, 0, 1080, 1350), 70, avoid=[(40, 20, 1040, 840)]))
    b.append(lotus_mandala(540, 1045, 215))
    b.append(lotus(150, 1262, .85, leaves=True) + lotus(930, 1262, .85, leaves=True))
    b.append(panel_rect(50, 30, 1030, 820, 30, "#2A0B3A", gold(), "#B98320", texture=False, op=.92))
    b.append('<rect x="50" y="30" width="980" height="790" rx="30" fill="%s"/>' % lin([(0, "#fff", .08), (.5, "#fff", 0), (1, "#fff", .04)], 0, 0, 1, 1))
    b.append(corner_flourish(76, 56, .5, 0) + corner_flourish(1004, 56, .5, 90) + corner_flourish(1004, 794, .5, 180) + corner_flourish(76, 794, .5, 270))
    S(6, [95, 75, 985, 780], "gold", "#F7ECFF", "#E9B949", tone="dark", tfont="classic")
    return card("".join(b))


# ------------------------------------------------------------------ 7
def card7():
    """Emerald and gold: big kalash with banana leaf at bottom-left, lotus pond at bottom-right."""
    rng = random.Random(7)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#0B3D2E", "#0F5A43"], 0, 0, 0, 1)]
    b.append('<rect width="1080" height="1350" fill="%s"/>' % jaali_pattern("jl7", "#E9C46A", .16, 58))
    # pond
    b.append('<path d="M440 1110 C640 1080 900 1090 1080 1100 V1350 H380 C380 1250 400 1150 440 1110Z" fill="%s"/>' % lin(["#2B7A78", "#17494D"], 0, 0, 0, 1))
    b.append(ripples(700, 1200, 60) + ripples(960, 1150, 40))
    b.append(lotus_pad(620, 1180, 70) + lotus_pad(1010, 1250, 90, rot=10) + lotus_pad(820, 1250, 60, rot=-8))
    b.append(lotus(760, 1190, .7) + lotus(960, 1150, .55, "#FFF3F7", "#F48FB1", "#C2185B"))
    b.append('<path d="M900 1180 C905 1150 910 1120 915 1090" stroke="#2E7D32" stroke-width="5"/><path d="M915 1090 C900 1060 905 1030 915 1020 C925 1030 930 1060 915 1090Z" fill="%s"/>' % lin(["#C2185B", "#F8BBD0"], 0, 1, 0, 0))
    # kalash with banana leaf behind
    b.append(curved_leaf([(170, 1180), (60, 1000), (-10, 900), (-40, 820)], 70, BANANA_TONES[1], random.Random(3)))
    b.append(curved_leaf([(250, 1180), (330, 1020), (400, 960), (470, 900)], 60, BANANA_TONES[0], random.Random(4)))
    b.append('<ellipse cx="220" cy="1262" rx="170" ry="26" fill="%s"/>' % lin(METAL["brass"], 0, 0, 1, 0))
    b.append(kalash(220, 1258, 410, "copper"))
    b.append(panel_rect(50, 40, 1030, 830, 26, "#FFFAEE", gold(), "#C9A34A"))
    b.append(corners(70, 60, 1010, 810, .45) if False else "")
    for x, y, r in ((74, 64, 0), (1006, 64, 90), (1006, 806, 180), (74, 806, 270)):
        b.append(corner_flourish(x, y, .45, r))
    S(7, [90, 80, 990, 790], "#0B4D38", "#1F2E28", "#B7791F", tfont="deco")
    return card("".join(b))


# ------------------------------------------------------------------ 8
def card8():
    """Sandstone shrine: arched deity photo niche with shikhara crown, bells and garland; panel below."""
    rng = random.Random(8)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#F6DEB0", "#E9C68A"], 0, 0, 0, 1)]
    b.append('<rect width="1080" height="1350" fill="%s"/>' % floral_pattern("fp8", "#A0521D", .1, 70))
    b.append(rays(540, 280, 30, 700, "#FFFFFF", .5, .4))
    px, py, pw, ph = 370, 100, 340, 370
    # shrine body
    b.append('<path d="M290 500 V230 Q290 150 360 120 L540 30 L720 120 Q790 150 790 230 V500Z" fill="%s" filter="url(#sh)"/>' % lin(["#C98A3E", "#E9B872", "#B5732E"], 0, 0, 1, 0))
    for k in range(6):
        y = 60 + k * 14
        b.append('<path d="M%d %d H%d" stroke="#8A5220" stroke-width="3" opacity=".5"/>' % (540 - (y - 30) * 2, y, 540 + (y - 30) * 2))
    b.append('<path d="M540 30 v-26" stroke="#5a3a1a" stroke-width="4"/><path d="M540 4 l50 12 l-50 12Z" fill="#E65100"/>')
    b.append('<circle cx="540" cy="30" r="10" fill="%s"/>' % gold())
    for x in (300, 780):
        b.append('<rect x="%d" y="200" width="30" height="300" fill="%s"/>' % (x - 15 + (0 if x < 540 else 0), lin(["#9A5E24", "#E0A85A", "#9A5E24"], 0, 0, 1, 0)))
    b.append('<path d="%s" fill="none" stroke="%s" stroke-width="10"/>' % (arch_path(px - 14, py - 14, px + pw + 14, py + ph + 4, (pw + 28) * .45), gold()))
    b.append('<path d="%s" fill="%s"/>' % (arch_path(px, py, px + pw, py + ph, pw * .45), rad(["#FFF8E6", "#FBE3B0", "#F2C77A"], .5, .55, .7)))
    b.append(om_symbol(540, 300, 130, fill="#E8B96A"))
    b.append(garland_swag(px - 20, py + 110, px + pw + 20, py + 110, 60, 12))
    b.append(marigold_strand(px - 16, py + 112, 220, 11) + marigold_strand(px + pw + 16, py + 112, 220, 11, ("yellow", "orange")))
    b.append(temple_bell(170, -10, 90, 130) + temple_bell(910, -10, 90, 130))
    b.append(incense(180, 470, 120, 2, "#FFFFFF", .5) + clay_lamp(900, 470, 1.2))
    b.append(panel_rect(60, 505, 1020, 1310, 22, "#FFFBF2", lin(["#8A4A10", "#E0A85A", "#8A4A10"], 0, 0, 1, 0), "#E0B06A"))
    S(8, [100, 548, 980, 1265], "#8A3A00", "#35241A", "#C0561A", tfont="deco",
      photo={"shape": "arch", "x": px, "y": py, "w": pw, "h": ph})
    return card("".join(b))


# ------------------------------------------------------------------ 9
def card9():
    """Dusk skyline of temple spires reflected in a lotus lake; frosted panel on the sky."""
    rng = random.Random(9)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#2C1B4A", "#6E2F6B", "#D2645A", "#F6B56A"], 0, 0, 0, 1)]
    b.append('<circle cx="760" cy="1030" r="110" fill="#FFE2A8"/><circle cx="760" cy="1030" r="220" fill="#FFD08A" opacity=".5" filter="url(#b30)"/>')
    b.append(stars(rng, (0, 0, 1080, 300), 30, avoid=[(40, 30, 1040, 850)]))
    far = "#8E4A7A"
    for x, h in ((80, 260), (220, 200), (420, 240), (640, 300), (880, 220), (1020, 280)):
        b.append(temple(x, 1150, h, silhouette=far))
    near = "#3A1840"
    b.append(temple(300, 1175, 330, silhouette=near))
    b.append(temple(800, 1175, 270, silhouette=near))
    b.append(temple(1040, 1175, 200, silhouette=near) + temple(40, 1175, 220, silhouette=near))
    b.append('<rect x="0" y="1170" width="1080" height="180" fill="%s"/>' % lin(["#5A2E5E", "#2A1236"], 0, 0, 0, 1))
    b.append('<g opacity=".35" transform="translate(0 2345) scale(1 -1)">%s</g>' % (temple(300, 1175, 330, silhouette="#1a0a20") + temple(800, 1175, 270, silhouette="#1a0a20")))
    b.append(ripples(760, 1230, 90, 3, "#FFE2A8", .5))
    b.append(lotus_pad(150, 1260, 70) + lotus_pad(960, 1290, 80, rot=8))
    b.append(lotus(150, 1255, .55) + lotus(960, 1285, .6))
    b.append(panel_rect(50, 40, 1030, 830, 30, "#FFFFFF", gold(), "#E7C38A", op=.93))
    S(9, [90, 80, 990, 790], "#5A1E5E", "#2A1B2E", "#C0561A", tfont="deco")
    return card("".join(b))


# ------------------------------------------------------------------ 10
def card10():
    """Flat-lay from above on red cloth: thali, kalash, lotus, marigolds, shankh and a bell around the panel."""
    rng = random.Random(10)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#A3121E", "#7A0A14"], 0, 0, 1, 1)]
    b.append('<rect width="1080" height="1350" fill="%s"/>' % dots_pattern("dp10", "#F4C542", .25, 26, 1.8))
    band = border_band("bb10", "#5A0810", "#F4C542", "#FFE9B0", 36)
    for (x, y, w, h) in ((0, 0, 1080, 36), (0, 1314, 1080, 36), (0, 0, 36, 1350), (1044, 0, 36, 1350)):
        b.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, y, w, h, band))
    b.append('<rect x="36" y="36" width="1008" height="1278" fill="none" stroke="%s" stroke-width="5"/>' % gold())
    b.append(thali_top(210, 170, 150, 2))
    b.append(kalash_top(880, 165, 120))
    b.append(lotus_top(545, 150, 80))
    b.append(marigold(400, 90, 26) + marigold(690, 96, 24, "yellow") + marigold(430, 230, 18, "yellow") + marigold(700, 230, 18))
    b.append(petals(rng, (40, 40, 1040, 290), 30, ("#FFB300", "#FF7043", "#FFF3E0"), avoid=[(60, 20, 360, 320), (740, 20, 1020, 300)]))
    b.append(shankh(210, 1205, .6, -14))
    b.append(temple_bell(900, 1110, 10, 110, "brass").replace('<g filter="url(#shs)">', '<g filter="url(#shs)" transform="rotate(-30 900 1180)">', 1))
    b.append(incense(620, 1270, 80, 4, "#FFFFFF", 0).replace("", "") if False else "")
    b.append(marigold(420, 1230, 22) + marigold(460, 1262, 16, "yellow") + marigold(760, 1240, 20, "yellow"))
    b.append(lotus_top(1000, 1230, 40))
    b.append(panel_rect(70, 300, 1010, 1140, 18, "#FFF8EA", gold(), "#E0B06A"))
    b.append(swastik(540, 322, 22, "#B3121D", 3.5) if False else "")
    S(10, [110, 340, 970, 1100], "#8E0E1C", "#3A2318", "#B7791F", tfont="classic")
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
