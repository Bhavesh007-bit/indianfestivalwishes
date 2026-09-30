"""Griha Pravesh invitations: 10 house-warming designs (house, door, toran, kalash, key, milk pot, rangoli)."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_f import *
from render import render_cards

CAT = "inv-griha-pravesh"
SPECS = []


def S(n, zone, title, text, accent, **kw):
    SPECS.append(spec(CAT, n, zone, title, text, accent, **kw))


def frame_lines(x0, y0, x1, y1, c1, c2=None, r=0, w1=6, w2=2, gap=12):
    c2 = c2 or c1
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="none" stroke="%s" stroke-width="%d"/>'
            '<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="none" stroke="%s" stroke-width="%d"/>'
            % (x0, y0, x1 - x0, y1 - y0, r, c1, w1, x0 + gap, y0 + gap, x1 - x0 - 2 * gap, y1 - y0 - 2 * gap, max(0, r - gap), c2, w2))


# ------------------------------------------------------------------ 1
def card1():
    """Sunny day: two-storey decorated house on top, parchment panel with leaf toran."""
    rng = random.Random(1)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#FFD9A8", "#FFEBD0", "#FFF6EA"], 0, 0, 0, 1)]
    b.append(rays(540, 300, 30, 900, "#FFFFFF", .5, .45))
    b.append('<circle cx="540" cy="260" r="260" fill="#FFF3D6" opacity=".6" filter="url(#b30)"/>')
    # distant trees and hills
    b.append('<path d="M0 470 C160 380 300 420 420 400 C560 380 700 360 820 400 C930 430 1000 390 1080 400 V560 H0Z" fill="#C8D9A0" opacity=".7"/>')
    for x, r in ((70, 90), (160, 70), (930, 85), (1020, 95)):
        b.append('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (x, 440 - r * .3, r, lin(["#7FA650", "#4E7A2E"], 0, 0, 0, 1)))
    b.append(house(540 - 400 * .66, 38, .66, wall=("#FFF1D6", "#F4CF95"), trim="#7A1F0A", roof=("#8E1E0C", "#C8421A")))
    b.append(rangoli(540, 495, 70, flat=.32, n=14))
    b.append(plant_pot(110, 500, .8, "#B5561E"))
    b.append(plant_pot(970, 500, .8, "#B5561E"))
    # panel
    b.append(panel_rect(70, 500, 1010, 1310, 26, "#FFFAF0", gold(), "#E7B45A"))
    b.append(toran(96, 984, 504, 34, hues=("orange", "yellow")))
    b.append(corners(92, 1246, 988, 1246, .55) if False else "")
    for (x, y, r) in ((100, 530, 0), (980, 530, 90)):
        b.append(corner_flourish(x, y, .5, r))
    # edge: garland swags on top
    b.append(garland_swag(-10, 10, 540, 6, 70, 15, ("orange", "yellow")))
    b.append(garland_swag(540, 6, 1090, 10, 70, 15, ("yellow", "orange")))
    b.append(marigold(540, 8, 22, "red"))
    b.append(marigold_strand(24, 10, 440, 13))
    b.append(marigold_strand(1056, 10, 440, 13, ("yellow", "orange")))
    S(1, [110, 540, 970, 1262], "#8C1C00", "#3A2318", "#B7791F", tfont="deco")
    return card("".join(b))


# ------------------------------------------------------------------ 2
def card2():
    """The whole card is the carved front door, flung open; text sits in the glowing doorway."""
    rng = random.Random(2)
    b = ['<rect width="1080" height="1350" fill="#5A0F14"/>']
    b.append('<rect width="1080" height="1350" fill="%s"/>' % jaali_pattern("jl2", "#F4C542", .16, 70))
    # frame opening
    ox0, ox1, oy0, oy1 = 58, 1022, 150, 1110
    interior = rad([(0, "#FFFFF6", 1), (.5, "#FFF1CF", 1), (.85, "#F6D38A", 1), (1, "#E0A546", 1)], .5, .45, .75)
    arch = "M%d %d V%d Q%d %d 540 %d Q%d %d %d %d V%dZ" % (ox0, oy1, oy0 + 90, ox0, oy0, oy0 - 30, ox1, oy0, ox1, oy0 + 90, oy1)
    # carved outer frame (wood)
    b.append('<path d="M0 1350 V%d Q0 %d 540 %d Q1080 %d 1080 %d V1350Z" fill="%s"/>' % (oy0 + 60, oy0 - 70, oy0 - 110, oy0 - 70, oy0 + 60, lin(["#3a1504", "#8B4513", "#5A2A0C"], 0, 0, 1, 0)))
    for i in range(12):
        yy = 290 + i * 70
        for xx in (29, 1051):
            b.append('<circle cx="%d" cy="%d" r="14" fill="none" stroke="#E7B45A" stroke-width="3"/><circle cx="%d" cy="%d" r="5" fill="#F4C542"/>' % (xx, yy, xx, yy))
            b.append('<path d="M%d %d l-10 20 l10 20 l10 -20Z" fill="none" stroke="#E7B45A" stroke-width="2" opacity=".7"/>' % (xx, yy + 15))
    b.append('<path d="%s" fill="%s"/>' % (arch, interior))
    b.append('<path d="%s" fill="none" stroke="%s" stroke-width="8"/>' % (arch, gold()))
    # door leaves open inward (thin perspective slivers)
    b.append('<path d="M%d %d L%d %d L%d %d L%d %dZ" fill="%s" stroke="#2a0f02" stroke-width="3"/>' % (ox0, oy0 + 90, ox0 + 46, oy0 + 120, ox0 + 46, oy1 - 30, ox0, oy1, lin(["#4A1F08", "#9A5626"], 0, 0, 1, 0)))
    b.append('<path d="M%d %d L%d %d L%d %d L%d %dZ" fill="%s" stroke="#2a0f02" stroke-width="3"/>' % (ox1, oy0 + 90, ox1 - 46, oy0 + 120, ox1 - 46, oy1 - 30, ox1, oy1, lin(["#9A5626", "#4A1F08"], 0, 0, 1, 0)))
    for k in range(5):
        y = oy0 + 160 + k * 170
        b.append('<rect x="%d" y="%d" width="26" height="120" rx="4" fill="none" stroke="#E7B45A" stroke-width="2"/>' % (ox0 + 10, y))
        b.append('<rect x="%d" y="%d" width="26" height="120" rx="4" fill="none" stroke="#E7B45A" stroke-width="2"/>' % (ox1 - 36, y))
        b.append('<circle cx="%d" cy="%d" r="5" fill="%s"/><circle cx="%d" cy="%d" r="5" fill="%s"/>' % (ox0 + 23, y + 60, gold(), ox1 - 23, y + 60, gold()))
    # light rays from inside
    b.append('<path d="M300 %d L140 1110 H940 L780 %dZ" fill="#FFFFFF" opacity=".25" filter="url(#b14)"/>' % (oy0, oy0))
    # toran over the doorway
    b.append(toran(20, 1060, 120, 62, hues=("orange", "yellow")))
    for x in (36, 1044):
        b.append(marigold_strand(x, 124, 520, 14))
    for x in (210, 380, 540, 700, 870):
        b.append(marigold_strand(x, 130, 60 if x != 540 else 80, 12, ("yellow", "orange")))
    # threshold, rangoli, footprints, kalash pair
    b.append('<rect x="0" y="1110" width="1080" height="240" fill="%s"/>' % lin(["#C9A26A", "#8E6A3E"], 0, 0, 0, 1))
    b.append('<rect x="40" y="1104" width="1000" height="26" rx="6" fill="%s"/>' % lin(["#6B3A15", "#3E1E08"], 0, 0, 0, 1))
    b.append('<path d="M40 1117 H1040" stroke="#E7B45A" stroke-width="2" stroke-dasharray="4 10"/>')
    b.append(rangoli(540, 1195, 150, flat=.34, n=18, cols=("#AD1457", "#FF9800", "#FFEB3B", "#2E7D32", "#1565C0", "#FFFFFF")))
    b.append(footprint(470, 1250, .6, -8, "#C8102E"))
    b.append(footprint(610, 1250, .6, 8, "#C8102E", left=True))
    b.append(kalash(170, 1290, 260, "copper"))
    b.append(kalash(910, 1290, 260, "copper"))
    S(2, [150, 290, 930, 1040], "#8C1C00", "#3B1E10", "#A0521D", tfont="deco")
    return card("".join(b))


# ------------------------------------------------------------------ 3
def card3():
    """Twilight: glowing house at the bottom, text on the calm starry sky."""
    rng = random.Random(3)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#0E1238", "#23205A", "#5A2E6E", "#C4607A", "#F2A66A"], 0, 0, 0, 1)]
    b.append(stars(rng, (20, 20, 1060, 700), 110, avoid=[(90, 50, 990, 790)]))
    b.append(stars(rng, (100, 80, 980, 800), 25, op=(.15, .35)))
    b.append('<ellipse cx="540" cy="1030" rx="520" ry="240" fill="#FFB86A" opacity=".35" filter="url(#b30)"/>')
    # hills
    b.append('<path d="M0 1010 C200 940 330 980 480 960 C650 940 820 930 1080 990 V1350 H0Z" fill="#2B1B3E"/>')
    b.append(house(540 - 400 * .72, 792, .72, wall=("#F6D9AE", "#D9A56A"), trim="#4A1405", roof=("#5A1A0C", "#8E2E14"), night=True))
    b.append('<rect x="0" y="1262" width="1080" height="88" fill="%s"/>' % lin(["#3A2340", "#1E1226"], 0, 0, 0, 1))
    for x, s in ((110, 1.0), (975, 1.0)):
        b.append(plant_pot(x, 1266, .9 * s, "#8E3A14"))
    # edge: gold arch lines + toran at top
    b.append('<rect x="22" y="22" width="1036" height="1306" rx="30" fill="none" stroke="%s" stroke-width="3" opacity=".8"/>' % gold())
    b.append(toran(-10, 1090, 18, 46, hues=("yellow", "orange")))
    b.append(sparkle(170, 190, .9) + sparkle(930, 240, .7) + sparkle(880, 120, .5))
    S(3, [110, 78, 970, 780], "gold", "#FFF3DC", "#F4C542", tone="dark", tfont="deco")
    return card("".join(b))


# ------------------------------------------------------------------ 4
def card4():
    """Teal tiled wall, big milk pot boiling over on a clay stove; key and rangoli on the floor."""
    rng = random.Random(4)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#0B4A50", "#11626A"], 0, 0, 0, 1)]
    tile = pattern_tile("tl4", 90, '<rect width="90" height="90" fill="none" stroke="#7FD1C9" stroke-opacity=".18" stroke-width="2"/>'
                        '<path d="M45 10 L80 45 L45 80 L10 45Z" fill="none" stroke="#F4C542" stroke-opacity=".22" stroke-width="2"/><circle cx="45" cy="45" r="7" fill="#F4C542" fill-opacity=".2"/>')
    b.append('<rect width="1080" height="1350" fill="%s"/>' % tile)
    # floor
    b.append('<path d="M0 1010 H1080 V1350 H0Z" fill="%s"/>' % lin(["#C0643A", "#8E3E1E"], 0, 0, 0, 1))
    for i in range(1, 6):
        b.append('<path d="M0 %d H1080" stroke="#6E2A10" stroke-width="2" opacity=".35"/>' % (1010 + i * 60))
    # hero: milk pot on stove
    b.append(milk_pot(300, 1255, 400, "brass"))
    b.append(rangoli(800, 1175, 170, flat=.34, n=16, cols=("#C2185B", "#FF9800", "#FFEB3B", "#00897B", "#3949AB", "#FFFFFF")))
    b.append(ornate_key(640, 1020, 360, -12, house_bow=True))
    # panel: ivory with crown
    b.append('<path d="M50 70 H470 Q540 20 610 70 H1030 V840 H50Z" fill="#FFF8EC" filter="url(#shp)"/>')
    b.append('<path d="M50 70 H470 Q540 20 610 70 H1030 V840 H50Z" fill="#FFF8EC" filter="url(#paper)"/>')
    b.append('<path d="M64 84 H474 Q540 38 606 84 H1016 V826 H64Z" fill="none" stroke="#0B4A50" stroke-width="5"/>')
    b.append('<path d="M76 96 H478 Q540 54 602 96 H1004 V814 H76Z" fill="none" stroke="%s" stroke-width="2"/>' % gold())
    b.append(swastik(540, 62, 26, "#B3121D", 4))
    b.append(bead_line(76, 840, 1004, 840, 20, 5))
    b.append(marigold(990, 1240, 22) + marigold(1030, 1210, 18, "yellow") + marigold(560, 1250, 16, "yellow"))
    # edge: mango-leaf sprigs at top corners of the wall
    for x, a in ((0, 30), (1080, -30)):
        for k in range(5):
            b.append(mango_leaf(x, 0, 120 - k * 10, a + (k - 2) * 22 + (180 if x == 0 else 180)))
    S(4, [90, 110, 990, 815], "#0B4A50", "#23302F", "#B5561E", tfont="classic")
    return card("".join(b))


# ------------------------------------------------------------------ 5
def card5():
    """Sage green: a big golden house-key with ribbon over a house-shaped invitation panel."""
    rng = random.Random(5)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#DDE8D2", "#B9CFA7"], 0, 0, 0, 1)]
    b.append('<rect width="1080" height="1350" fill="%s"/>' % floral_pattern("fp5", "#4E6B3A", .12, 110))
    b.append(bokeh(rng, 18, (0, 0, 1080, 400), ["#FFFFFF", "#F4E3A1"], 20, 60, (.2, .5)))
    # house-shaped panel
    pth = "M60 1310 V470 L540 250 L1020 470 V1310Z"
    b.append('<path d="%s" fill="#FFFDF6" filter="url(#shp)"/><path d="%s" fill="#FFFDF6" filter="url(#paper)"/>' % (pth, pth))
    b.append('<path d="M78 1292 V480 L540 272 L1002 480 V1292Z" fill="none" stroke="#4E6B3A" stroke-width="5"/>')
    b.append('<path d="M92 1278 V488 L540 288 L988 488 V1278Z" fill="none" stroke="%s" stroke-width="2"/>' % gold())
    # roof: tiles band on top
    b.append('<path d="M34 482 L540 232 L1046 482" fill="none" stroke="#8E2E14" stroke-width="26" stroke-linejoin="round"/>')
    b.append('<path d="M34 482 L540 232 L1046 482" fill="none" stroke="#C8421A" stroke-width="12" stroke-dasharray="18 8" stroke-linejoin="round"/>')
    # gable vent with kalash
    b.append('<circle cx="540" cy="378" r="58" fill="#EEF3E6" stroke="%s" stroke-width="5"/>' % gold())
    b.append(kalash(540, 424, 100, "copper"))
    b.append(toran(110, 970, 494, 30, hues=("orange", "yellow")))
    # hero: key across the top with ribbon
    b.append(ornate_key(170, 140, 760, -6, "#B3121D", house_bow=True))
    b.append(sparkle(900, 90, .9) + sparkle(960, 220, .6) + sparkle(80, 300, .7))
    # edge: leafy vines at the bottom corners
    for x, sgn in ((0, 1), (1080, -1)):
        for k in range(7):
            b.append(mango_leaf(x + sgn * 10, 1350 - k * 55, 90, sgn * (-60 - k * 4) + (0 if sgn > 0 else 0), "#2F5A1F", "#6FA048"))
    S(5, [120, 540, 960, 1255], "#355026", "#2B2A22", "#B5561E", tfont="classic")
    return card("".join(b))


# ------------------------------------------------------------------ 6
def card6():
    """Kota-stone floor seen from above: rangoli in the corners, footprints walking in, kalash."""
    rng = random.Random(6)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#E9E2D2", "#D6CCB6"], 0, 0, 1, 1)]
    tile = pattern_tile("ks6", 270, '<rect width="270" height="270" fill="none" stroke="#B9AD92" stroke-width="3"/><rect x="6" y="6" width="258" height="258" fill="#fff" fill-opacity=".08"/>')
    b.append('<rect width="1080" height="1350" fill="%s"/>' % tile)
    b.append(rangoli(90, 70, 330, n=20, cols=("#AD1457", "#FF8F00", "#FFEB3B", "#2E7D32", "#6A1B9A", "#FFFFFF")))
    b.append(rangoli(1010, 1290, 300, n=18, cols=("#1565C0", "#FF8F00", "#FFEB3B", "#AD1457", "#2E7D32", "#FFFFFF"), rot=10))
    # marigold petal border lines
    b.append(petals(rng, (0, 0, 1080, 1350), 70, avoid=[(60, 250, 1020, 1160), (330, 1260, 750, 1350)]))
    # kalash on a small brass plate, top-right
    b.append('<ellipse cx="860" cy="262" rx="120" ry="30" fill="%s"/>' % lin(METAL["brass"], 0, 0, 1, 0))
    b.append(kalash(860, 262, 250, "brass"))
    # footprints entering from bottom-left
    b.append(footsteps(120, 1300, 200, 1160, 3, .85))
    # panel
    b.append(panel_rect(70, 290, 1010, 1150, 40, "#FFFFFF", lin(["#AD1457", "#FF8F00"], 0, 0, 1, 0), "#F2B8C6"))
    b.append(scallop_border(110, 290, 970, 290, 10, "#FF8F00"))
    S(6, [110, 330, 970, 1110], "#A01347", "#35232C", "#E65100", tfont="deco")
    return card("".join(b))


# ------------------------------------------------------------------ 7
def card7():
    """Mustard wall, full-width toran; red silk banner hangs from a rod; threshold still life below."""
    rng = random.Random(7)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#F4C04E", "#E5A22A"], 0, 0, 0, 1)]
    b.append('<rect width="1080" height="1350" fill="%s"/>' % floral_pattern("fp7", "#8E4A06", .12, 80))
    b.append('<rect y="1000" width="1080" height="350" fill="%s"/>' % lin(["#8E4A1E", "#5A2A10"], 0, 0, 0, 1))
    b.append('<rect y="996" width="1080" height="14" fill="%s"/>' % gold())
    # banner
    bx0, bx1, by0, by1 = 110, 970, 130, 960
    ban = "M%d %d H%d V%d L540 %d L%d %dZ" % (bx0, by0, bx1, by1, by1 + 50, bx0, by1)
    b.append('<path d="%s" fill="%s" filter="url(#shp)"/>' % (ban, lin(["#7E0A14", "#A8121F", "#7E0A14"], 0, 0, 1, 0)))
    b.append('<path d="%s" fill="%s" opacity=".35"/>' % (ban, lin([(0, "#fff", 0), (.5, "#fff", .15), (1, "#fff", 0)], 0, 0, 1, 1)))
    b.append('<path d="M%d %d H%d V%d L540 %d L%d %dZ" fill="none" stroke="%s" stroke-width="6"/>' % (bx0 + 16, by0 + 18, bx1 - 16, by1 - 12, by1 + 30, bx0 + 16, by1 - 12, gold()))
    b.append('<path d="M%d %d H%d V%d L540 %d L%d %dZ" fill="none" stroke="#F4C542" stroke-width="1.5" stroke-dasharray="3 7"/>' % (bx0 + 30, by0 + 32, bx1 - 30, by1 - 22, by1 + 14, bx0 + 30, by1 - 22))
    b.append(tassel(540, by1 + 48, 1.1, "#F4C542"))
    b.append(tassel(bx0 + 4, by1, .9, "#F4C542") + tassel(bx1 - 4, by1, .9, "#F4C542"))
    b.append('<rect x="80" y="112" width="920" height="22" rx="11" fill="%s" filter="url(#shs)"/>' % gold(0, 0, 0, 1))
    b.append('<circle cx="80" cy="123" r="20" fill="%s"/><circle cx="1000" cy="123" r="20" fill="%s"/>' % (gold(), gold()))
    b.append('<path d="M320 112 L540 40 L760 112" stroke="#6E440A" stroke-width="3" fill="none"/>')
    # toran over everything
    b.append(toran(-10, 1090, 30, 56))
    b.append(marigold_strand(40, 34, 820, 15) + marigold_strand(1040, 34, 820, 15, ("yellow", "orange")))
    # threshold still life
    b.append(milk_pot(220, 1262, 330))
    b.append(kalash(870, 1262, 320, "copper"))
    b.append(footsteps(470, 1250, 520, 1060, 4, .6))
    b.append(footprint(640, 1110, .5, 10, left=True) + footprint(600, 1190, .55, 10))
    b.append(rangoli(540, 1150, 90, flat=.35, n=12) if False else "")
    S(7, [150, 170, 930, 920], "gold", "#FFF1DC", "#F4C542", tone="dark", tfont="deco")
    return card("".join(b))


# ------------------------------------------------------------------ 8
def card8():
    """Peach wall with a wide window thrown open, shutters, toran and a marigold window box."""
    rng = random.Random(8)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#F7C9B0", "#EFA98A"], 0, 0, 0, 1)]
    b.append('<rect width="1080" height="1350" fill="%s"/>' % dots_pattern("dp8", "#B5502E", .18, 30))
    # shutters (partly cut by the card edge)
    for x0, sgn in ((0, 1), (1080, -1)):
        pts = "M%d 150 L%d 190 L%d 1030 L%d 1060Z" % (x0, x0 + sgn * 78, x0 + sgn * 78, x0)
        b.append('<path d="%s" fill="%s" stroke="#2F4A3A" stroke-width="4"/>' % (pts, lin(["#2F6B55", "#4E9A7C"], 0, 0, 1, 0)))
        for k in range(22):
            y = 210 + k * 37
            b.append('<path d="M%d %d L%d %d" stroke="#1E4A3A" stroke-width="5" opacity=".6"/>' % (x0, y, x0 + sgn * 78, y + 10))
    # window frame
    b.append('<rect x="78" y="150" width="924" height="910" rx="8" fill="%s" filter="url(#shp)"/>' % lin(["#FFFFFF", "#F1E6D6"], 0, 0, 1, 1))
    b.append('<rect x="104" y="176" width="872" height="858" fill="%s"/>' % lin(["#FFFBF2", "#FFF1DE"], 0, 0, 0, 1))
    b.append('<rect x="104" y="176" width="872" height="858" fill="none" stroke="#C9A06A" stroke-width="3"/>')
    b.append('<path d="M104 176 L300 176 L104 520Z" fill="#fff" opacity=".6"/>')
    # sill and window box
    b.append('<rect x="50" y="1050" width="980" height="34" rx="6" fill="%s" filter="url(#shs)"/>' % lin(["#FFFFFF", "#D9C9B0"], 0, 0, 0, 1))
    b.append('<path d="M110 1084 H970 L950 1190 H130Z" fill="%s"/>' % lin(["#8E3A14", "#B5561E", "#8E3A14"], 0, 0, 1, 0))
    b.append('<path d="M130 1110 H950" stroke="#F4C542" stroke-width="3" stroke-dasharray="2 12" stroke-linecap="round"/>')
    for k in range(20):
        b.append(marigold(130 + k * 43, 1090 + (k % 2) * 8, 22, ("orange", "yellow", "red")[k % 3], k * 30))
    for k in range(9):
        b.append(mango_leaf(150 + k * 95, 1100, 70, 20 if k % 2 else -20))
    for x in (160, 420, 680, 920):
        b.append('<path d="M%d 1180 C%d 1220 %d 1240 %d 1262" stroke="#2E7D32" stroke-width="3" fill="none"/>' % (x, x - 20, x + 10, x - 6))
        for j in range(3):
            b.append(mango_leaf(x - 6 + j * 3, 1200 + j * 20, 26, 40 if j % 2 else -40, "#2E7D32", "#81C784"))
    # toran across the window top + strands
    b.append(toran(60, 1020, 144, 50, hues=("red", "yellow")))
    for x in (100, 980):
        b.append(marigold_strand(x, 150, 220, 12, ("red", "yellow")))
    # small kalash on the lintel
    b.append(kalash(540, 120, 110, "brass"))
    S(8, [144, 216, 936, 994], "#9E2A12", "#3A2A22", "#2F6B55", tfont="script")
    return card("".join(b))


# ------------------------------------------------------------------ 9
def card9():
    """Photo of the new home in an arched carved doorway with toran and kalash; cream panel below."""
    rng = random.Random(9)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#8E1B1B", "#5E0D12"], 0, 0, 0, 1)]
    b.append('<rect width="1080" height="1350" fill="%s"/>' % jaali_pattern("jl9", "#F4C542", .12, 54))
    b.append(rays(540, 260, 26, 700, "#FFD27A", .35, .4))
    px, py, pw, ph = 370, 70, 340, 400
    arch = arch_path(px, py, px + pw, py + ph, pw * .45)
    # carved frame around arch
    fr = arch_path(px - 44, py - 40, px + pw + 44, py + ph + 10, (pw + 88) * .45)
    b.append('<path d="%s" fill="%s" filter="url(#sh)"/>' % (fr, lin(["#3a1504", "#9A5626", "#5A2A0C"], 0, 0, 1, 0)))
    b.append('<path d="%s" fill="none" stroke="%s" stroke-width="5" transform="translate(0 0)"/>' % (arch_path(px - 26, py - 22, px + pw + 26, py + ph + 10, (pw + 52) * .45), gold()))
    b.append('<path d="%s" fill="%s"/>' % (arch, lin(["#FFF4DD", "#F3D7A6"], 0, 0, 0, 1)))
    # placeholder: faint house silhouette
    b.append('<path d="M%d %d l100 -80 l100 80 v110 h-200Z" fill="#D9B27A" opacity=".45"/>' % (px + 70, py + 290))
    b.append('<rect x="%d" y="%d" width="46" height="70" rx="20" fill="#FFF4DD" opacity=".8"/>' % (px + 147, py + 330))
    b.append(toran(px - 70, px + pw + 70, py + 90, 40))
    b.append(marigold_strand(px - 40, py + 94, 300, 11) + marigold_strand(px + pw + 40, py + 94, 300, 11, ("yellow", "orange")))
    b.append(kalash(240, 488, 230, "copper") + kalash(840, 488, 230, "copper"))
    b.append(footprint(160, 330, .7, -20) + footprint(930, 330, .7, 20, left=True))
    # panel
    b.append(panel_rect(60, 500, 1020, 1310, 22, "#FFF8EA", gold(), "#E0B06A"))
    b.append(corner_flourish(84, 524, .5, 0) + corner_flourish(996, 524, .5, 90))
    # edge
    b.append('<rect x="14" y="14" width="1052" height="1322" rx="18" fill="none" stroke="%s" stroke-width="4"/>' % gold())
    S(9, [100, 540, 980, 1265], "#7A1414", "#33211A", "#B7791F", tfont="deco",
      photo={"shape": "arch", "x": px, "y": py, "w": pw, "h": ph})
    return card("".join(b))


# ------------------------------------------------------------------ 10
def card10():
    """Mint and coral: offset panel, vertical marigold strings on the left, cottage and key below."""
    rng = random.Random(10)
    b = ['<rect width="1080" height="1350" fill="%s"/>' % lin(["#E4F4EC", "#CBE8DA"], 0, 0, 1, 1)]
    b.append('<circle cx="160" cy="1080" r="360" fill="#FFD6C4" opacity=".6"/>')
    b.append('<circle cx="1000" cy="120" r="200" fill="#FFE9B8" opacity=".6"/>')
    b.append(bokeh(rng, 20, (0, 820, 1080, 1350), ["#FFFFFF", "#FFC7A8"], 10, 40, (.3, .6)))
    # panel offset right/top
    b.append(panel_rect(140, 40, 1046, 830, 36, "#FFFFFF", lin(["#E8765A", "#F4B34C"], 0, 0, 1, 0), "#F7C9B8"))
    # vertical marigold strings on the left
    for k, x in enumerate((30, 72, 114)):
        b.append(marigold_strand(x, -10, 760 - k * 90, 15, (("orange", "yellow"), ("red", "orange"), ("yellow", "orange"))[k]))
    b.append(toran(-10, 150, 0, 40))
    # cottage bottom-left
    b.append(house(30, 830, .54, wall=("#FFF7EC", "#F7D7BD"), trim="#C24A2C", roof=("#B03A1E", "#E8765A"), storeys=1))
    b.append(rangoli(246, 1200, 60, flat=.3, n=12))
    # key and tulsi on the right
    b.append(ornate_key(610, 900, 360, -4, "#E8765A", house_bow=False))
    b.append(plant_pot(960, 1262, 1.0, "#C24A2C"))
    b.append(milk_pot(770, 1262, 250, "brass", stove=False))
    b.append(footsteps(470, 1250, 330, 1215, 3, .5))
    S(10, [180, 80, 1006, 790], "#C24A2C", "#2F3B36", "#D98A1E", tfont="script")
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
