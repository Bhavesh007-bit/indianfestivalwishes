"""Diwali wish card art: 10 distinct compositions.
Run: python3 tools/cards3/gen_diwali.py [n ...]
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_b import *
from render import render_cards

CAT = "diwali"
DARK = dict(title="gold", text="#FFF6E6", accent="#FFD36B")


def spec(i, zone, tone="dark", colors=None, title="deco", align="center", photo=None):
    d = {"id": "E-%s-%d" % (CAT, i), "tpl": True, "zone": zone, "colors": colors or DARK, "tone": tone, "title": title, "align": align}
    if photo:
        d["photo"] = photo; d["slot"] = True
    return d


PAL = [["#E0115F", "#FF8A00", "#FFD23F", "#1B9AAA", "#6A2C91", "#2EC4B6"],
       ["#C2185B", "#FFB300", "#FFF176", "#00897B", "#5E35B1", "#FF7043"],
       ["#D81B60", "#FFC107", "#FFFFFF", "#8E24AA", "#1E88E5", "#F4511E"]]
LIGHTS = ["#FFD23F", "#FF6FA5", "#8BF1FF", "#FF9F1C", "#B8FF7A"]
cards, specs = {}, []

# 1 ─ big flattened rangoli on the floor with a diya cluster; string lights above; text in the calm night
r = random.Random(1)
b = bg_grad([(0, "#1E0833"), (.55, "#2E0B3F"), (1, "#16052A")])
b += bokeh(r, 26, 0, 0, 1080, 760, ["#FFB347", "#FF6FA5", "#FFD23F"], 10, 34, (.08, .22))
b += stars(r, 60, 0, 0, 1080, 700, "#FFE9B8", 1.6, 4)
b += eglow(540, 1020, 620, 260, "#FF9F1C", .35)
b += string_lights(-20, 30, 1100, 30, 110, 22, LIGHTS, 8, wire="#5A3A2A")
b += string_lights(-20, 70, 540, 40, 60, 10, LIGHTS[::-1], 6, wire="#5A3A2A") + string_lights(540, 40, 1100, 70, 60, 10, LIGHTS[1:], 6, wire="#5A3A2A")
b += rangoli(540, 1010, 500, PAL[0], 0, flat=.44)
b += diya_cluster(540, 975, 1.15, 7, r)
b += akash_kandil_round(88, 60, .5, string_top=40) + akash_kandil_round(992, 60, .5, '#0E7C86', '#E0115F', string_top=40)
b += '<rect x="0" y="1262" width="1080" height="88" fill="#16052A" opacity=".55"/>'
cards["E-%s-1" % CAT] = doc(b)
specs.append(spec(1, [160, 230, 920, 740]))

# 2 ─ three akash kandils hanging from the top on a maroon bokeh wall; text on a parchment panel
r = random.Random(2)
b = bg_grad([(0, "#6B0F1A"), (1, "#3A0610")]) + bokeh(r, 40, 0, 0, 1080, 1350, ["#FFB347", "#FFD23F", "#FF7A59"], 10, 46, (.08, .25))
b += noise(.05, "overlay")
b += akash_kandil_hex(540, 70, .82, "#0E7C86", "#C2185B", "#FFD23F", 0)
b += akash_kandil_star(185, 20, .78, "#E0115F", "#FF8A00", "#FFD23F", 0)
b += akash_kandil_round(895, 40, .8, "#6A2C91", "#FF4F79", "#FFD23F", 0)
b += panel(110, 620, 860, 590, "#FFF6E4", 30, "url(#gGoldH)", 4, True, "fShadow")
b += '<rect x="126" y="636" width="828" height="558" rx="22" fill="url(#gHaloSoft)" opacity=".25"/>'
b += diya_row(40, 300, 1262, 3, .62, r) + diya_row(780, 1040, 1262, 3, .62, r)
cards["E-%s-2" % CAT] = doc(b)
specs.append(spec(2, [150, 660, 930, 1170], "light", dict(title="#8C1C00", text="#3A1F16", accent="#8A4B08")))

# 3 ─ fireworks over a lit city, diyas on the parapet; text on a glass card in the sky
r = random.Random(3)
b = bg_grad([(0, "#0B0B2E"), (.6, "#241046"), (1, "#3B1450")])
b += stars(r, 90, 0, 0, 1080, 900, "#FFFFFF", 1.4, 6)
b += firework(190, 170, 150, "#FFD23F", seed=1) + firework(880, 150, 170, "#FF4F9A", seed=2) + firework(560, 90, 90, "#7CF3FF", seed=3, op=.9)
b += firework(990, 520, 90, "#B388FF", seed=4, op=.8) + firework(90, 560, 80, "#FF9F1C", seed=5, op=.8)
b += eglow(540, 1000, 700, 200, "#FF9F1C", .25)
b += city_skyline(1180, random.Random(7), "#120824", height=(140, 300))
b += '<rect x="0" y="1180" width="1080" height="170" fill="#1A0B2A"/><rect x="0" y="1180" width="1080" height="8" fill="url(#gGoldH)" opacity=".7"/>'
b += diya_row(20, 1060, 1168, 9, .5, r)
b += '<rect x="140" y="300" width="800" height="600" rx="36" fill="#FFFFFF" opacity=".07" stroke="#FFFFFF" stroke-opacity=".25" stroke-width="2"/>'
cards["E-%s-3" % CAT] = doc(b)
specs.append(spec(3, [160, 330, 920, 870]))

# 4 ─ half rangoli crowning the top edge, ring of diyas along its rim; cream parchment, text below (light)
r = random.Random(4)
b = bg_grad([(0, "#FFF6E3"), (1, "#F6E3C2")]) + paper(.1)
b += rangoli(540, -60, 540, PAL[1], 2, chalk="#FFFDF6")
for k in range(11):
    a = math.radians(20 + 140 * k / 10.0)
    b += diya(540 + 600 * math.cos(a) - 40, -60 + 600 * math.sin(a) * .9, .5, ("clay", "brass")[k % 2])
b += border_frame(22, "url(#gGoldH)", 4, 1.4, 10, .9)
b += footprint_pair(150, 1180, .6, 0, "#C2185B") + footprint_pair(930, 1180, .6, 0, "#C2185B")
cards["E-%s-4" % CAT] = doc(b)
specs.append(spec(4, [150, 640, 930, 1180], "light", dict(title="#9A1B1B", text="#3B2416", accent="#8A4B08")))

# 5 ─ Lakshmi footprints walking up the left towards a corner rangoli; deep teal
r = random.Random(5)
b = bg_grad([(0, "#0D4750"), (1, "#062A31")], 0, 0, 1, 1) + noise(.05, "overlay")
b += bokeh(r, 24, 300, 0, 1080, 1350, ["#FFD27A", "#7FE7D6"], 8, 30, (.06, .18))
b += rangoli(160, 170, 300, PAL[2], 1)
for k, (x, y, rot) in enumerate(((150, 1210, -8), (170, 1030, -4), (160, 850, 4), (150, 670, 0))):
    b += footprint_pair(x, y, .72, rot, "#E0115F", "#FFE9B8")
for (x, y) in ((50, 1120), (270, 940), (40, 760), (275, 580)):
    b += diya(x, y, .42, "clay")
b += '<rect x="330" y="0" width="1.5" height="1350" fill="url(#gGoldV)" opacity=".0"/>'
b += corner_ornament(1054, 26, .7, 90) + corner_ornament(1054, 1324, .7, 180)
cards["E-%s-5" % CAT] = doc(b)
specs.append(spec(5, [300, 520, 1060, 1180], align="center"))

# 6 ─ open mithai box with ladoos and kaju katli, sparklers crossing above; royal indigo
r = random.Random(6)
b = bg_grad([(0, "#1B1F5E"), (1, "#0C0E33")]) + stars(r, 70, 0, 0, 1080, 1350, "#FFE9B8", 1.5, 8)
b += eglow(540, 1080, 520, 240, "#FFB347", .3)
b += phuljhadi(40, 330, -38, 300, 1, 5) + phuljhadi(1040, 330, 218, 300, 1, 6)
b += mithai_box(540, 1236, 1.35, "#B0123E")
b += diya(150, 1210, .6, "brass") + diya(900, 1210, .6, "brass")
b += string_lights(-20, 20, 1100, 20, 70, 18, LIGHTS, 7)
cards["E-%s-6" % CAT] = doc(b)
specs.append(spec(6, [160, 250, 920, 750]))

# 7 ─ brass urli with floating diyas, marigolds and petals; wine background with falling petals
r = random.Random(7)
b = bg_grad([(0, "#4A0B2A"), (1, "#240417")]) + noise(.05, "overlay")
b += eglow(540, 1050, 600, 260, "#FF9F1C", .3)
for _ in range(40):
    x, y = r.uniform(0, 1080), r.uniform(0, 1350)
    if 140 < x < 940 and 170 < y < 760:
        continue
    b += '<ellipse cx="%d" cy="%d" rx="9" ry="5" transform="rotate(%d %d %d)" fill="%s" opacity=".8"/>' % (x, y, r.uniform(0, 180), x, y, r.choice(["#FF9E1B", "#E23E57", "#FFC93C"]))
b += urli(540, 1010, 1.25, r)
b += gota_band(0, 0, 1080, 16, ("#B38728", "#6E4A10"), scallop="b") if False else ""
b += four_corners(24, .8)
cards["E-%s-7" % CAT] = doc(b)
specs.append(spec(7, [160, 180, 920, 740]))

# 8 ─ long row of big diyas on a carved stone ledge, bokeh wall; text above
r = random.Random(8)
b = bg_grad([(0, "#2A1206"), (1, "#4A2008")]) + bokeh(r, 50, 0, 0, 1080, 900, ["#FFB347", "#FFD27A", "#FF8A3D"], 12, 56, (.08, .28))
b += '<rect x="0" y="930" width="1080" height="420" fill="#2A1509"/><rect x="0" y="930" width="1080" height="14" fill="url(#gGoldH)"/>'
for k in range(9):
    x = 60 + k * 120
    b += '<g transform="translate(%d 1060)" opacity=".75">%s</g>' % (x, rangoli_mini(44, "#C98A2A", "#FFD27A"))
b += '<rect x="0" y="1150" width="1080" height="6" fill="url(#gGoldH)" opacity=".7"/>'
b += eglow(540, 900, 640, 140, "#FFB347", .4)
b += diya_row(10, 1070, 912, 7, .95, r, "mix")
b += akash_kandil_star(990, -40, .45, string_top=0, tails=True) + akash_kandil_star(90, -40, .45, "#FF8A00", "#E0115F", string_top=0)
cards["E-%s-8" % CAT] = doc(b)
specs.append(spec(8, [160, 250, 920, 760]))

# 9 ─ twin brass samai lamps flanking a rangoli; crimson with flame butis
r = random.Random(9)
b = bg_grad([(0, "#7A0E1E"), (1, "#3E0610")])
for yy in range(40, 1350, 90):
    for xx in range(40 + (yy // 90 % 2) * 45, 1080, 90):
        b += '<path d="M%d,%d c-6,-6 -6,-14 0,-22 c6,8 6,16 0,22Z" fill="#FFD27A" opacity=".12"/>' % (xx, yy)
b += eglow(540, 400, 520, 360, "#3E0610", .8)
b += rangoli(540, 1160, 300, PAL[0], 1, flat=.4)
b += samai(150, 1250, .8) + samai(930, 1250, .8)
b += border_frame(20, "url(#gGoldH)", 5, 1.5, 10)
cards["E-%s-9" % CAT] = doc(b)
specs.append(spec(9, [160, 190, 920, 760]))

# 10 ─ black & gold foil: gold fireworks above, one grand diya below
r = random.Random(10)
b = bg_grad([(0, "#0E0A06"), (1, "#1C130A")]) + noise(.06, "overlay")
b += firework(540, 170, 190, "#E9C46A", "#FFF3C4", 44, 1) + firework(170, 250, 110, "#D9A441", "#FFF3C4", 30, 2, .85) + firework(910, 250, 110, "#D9A441", "#FFF3C4", 30, 3, .85)
b += stars(r, 50, 0, 0, 1080, 1350, "#E9C46A", 1.3, 6)
b += diya(470, 1130, 1.7, "brass", glow_r=260)
b += phuljhadi(130, 1250, -70, 220, .8, 8) + phuljhadi(950, 1250, 250, 220, .8, 9)
b += border_frame(26, "url(#gGoldH)", 3, 1.2, 10)
b += four_corners(26, .9)
cards["E-%s-10" % CAT] = doc(b)
specs.append(spec(10, [160, 440, 920, 950]))

if __name__ == "__main__":
    only = sys.argv[1:]
    render_cards({k: v for k, v in cards.items() if not only or k.split("-")[-1] in only})
    save_specs(CAT, specs)
