"""Karva Chauth wish card art: 10 distinct compositions.
Run: python3 tools/cards3/gen_karva-chauth.py [n ...]
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_kc import *
from lib_kc import _around
from render import render_cards

CAT = "karva-chauth"
DARK = dict(title="gold", text="#FFF6EA", accent="#FFD36B")
LIGHT = dict(title="#9A0F2A", text="#3A1A1E", accent="#8A4B08")


def spec(i, zone, tone="dark", colors=None, title="script", photo=None):
    d = {"id": "E-%s-%d" % (CAT, i), "tpl": True, "zone": zone, "colors": colors or DARK, "tone": tone, "title": title, "align": "center"}
    if photo:
        d["photo"] = photo; d["slot"] = True
    return d


def silk_panel(x, y, w, h, c0, c1, r=30, gota=True):
    gid, gd = lg([(0, c0), (1, c1)], 0, 0, 0, 1)
    g = '<defs>%s</defs><rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="url(#%s)" filter="url(#fShadow)"/>' % (gd, x, y, w, h, r, gid)
    g += '<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="none" stroke="url(#gGoldH)" stroke-width="5"/>' % (x, y, w, h, r)
    g += '<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="none" stroke="#FFD86B" stroke-width="1.4" opacity=".7" stroke-dasharray="2 6" stroke-linecap="round"/>' % (x + 12, y + 12, w - 24, h - 24, r - 10)
    return g


cards, specs = {}, []

# 1 ─ terrace: woman in red chunri raises the channi to a giant moon over the rooftops; maroon silk plaque below
r = random.Random(1)
b = sky([(0, "#0C0B30"), (.55, "#261246"), (1, "#4A1840")], 1, 650, haze=[(760, 260, 520, 300, "#8E6BC8", .18)])
b += moon(790, 235, 158, seed=11)
b += soft_clouds(random.Random(1), 3, 520, 380, 1080, 450, "#C9B8E8", .22)
b += rooftops(632, random.Random(5), "#1A0C26", "#FFB347")
b += '<rect x="0" y="632" width="1080" height="720" fill="#2A0A1E"/>' + zari_pattern(0, 632, 1080, 720, "#FFD86B", .07)
b += '<rect x="0" y="624" width="1080" height="14" fill="url(#gGoldH)"/>'
b += gota_band(0, 638, 1080, 26, ("#9E0F2E", "#6E0A20"), scallop="b")
w, _ = woman_moon(235, 630, .86)
b += w
b += diya_row(600, 1040, 618, 4, .4, r)
b += silk_panel(96, 700, 888, 562, "#5E0C26", "#3C0618")
cards["E-%s-1" % CAT] = doc(b)
specs.append(spec(1, [140, 735, 940, 1230]))

# 2 ─ close-up: the moon seen through a huge decorated channi; indigo sky, maroon silk plaque
b = sky([(0, "#0A0C2C"), (.6, "#1E1240"), (1, "#2D0C30")], 2, haze=[(540, 360, 560, 420, "#6A5AC8", .2)])
b += moon(540, 318, 180, seed=5, halo=1.2)
b += channi(540, 318, 228, tilt=.93, rot=0, rim="url(#gGoldH)")
for k in range(12):
    a = math.radians(k * 30 + 15)
    b += sparkle(540 + 300 * math.cos(a), 318 + 300 * math.sin(a), 10 + (k % 3) * 4, "#FFE9B8", .9)
b += silk_panel(100, 640, 880, 622, "#3A1E6A", "#1E0E3E")
b += mehendi_corner(118, 658, .42, 0, "#E9B95B", .55) + mehendi_corner(962, 658, .42, 90, "#E9B95B", .55)
b += mehendi_corner(962, 1242, .42, 180, "#E9B95B", .55) + mehendi_corner(118, 1242, .42, 270, "#E9B95B", .55)
cards["E-%s-2" % CAT] = doc(b)
specs.append(spec(2, [140, 690, 940, 1222]))

# 3 ─ cream: chunri band with tassels on top; big puja thali on a faint mehendi mandala (light)
b = bg_grad([(0, "#FFF6E6"), (1, "#F6DEC0")]) + paper(.1)
b += mehendi_mandala(540, 1090, 470, "#B5651D", .16, 2.4)
b += eglow(540, 1080, 560, 240, "#FFB347", .28)
b += gota_band(0, 0, 1080, 118, ("#B3001B", "#7A0012"), scallop="b")
for k in range(13):
    b += tassel(40 + k * 83, 124, .9, "#B3001B" if k % 2 else "#0F7B3F")
b += thali(540, 1085, 1.5, random.Random(3))
b += mehendi_corner(26, 1324, .5, 270, "#9A3A12", .7) + mehendi_corner(1054, 1324, .5, 180, "#9A3A12", .7)
cards["E-%s-3" % CAT] = doc(b)
specs.append(spec(3, [150, 250, 930, 820], "light", LIGHT))

# 4 ─ two mehendi hands with bangles cupping the moon; violet night with a faint gold mandala
b = sky([(0, "#140A30"), (.6, "#2C0E3E"), (1, "#4A0F2E")], 4, haze=[(540, 950, 520, 360, "#C86BA0", .22)])
b += mehendi_mandala(540, 930, 360, "#E9B95B", .14, 2)
b += moon(540, 900, 135, seed=7, halo=1.1)
b += mehendi_hand(245, 1255, .98, 16)
b += mehendi_hand(835, 1255, .98, -16, True)
cards["E-%s-4" % CAT] = doc(b)
specs.append(spec(4, [150, 120, 930, 690]))

# 5 ─ large painted karwa with lid diya, bangles, mehendi vine; deep wine with zari lattice
b = bg_grad([(0, "#3E0722"), (1, "#1A0412")]) + zari_pattern(0, 0, 1080, 1350, "#FFD86B", .06, 80) + noise(.05, "overlay")
b += moon(150, 150, 88, seed=3, halo=.9)
b += stars(random.Random(5), 40, 0, 0, 1080, 400, "#FFF6DA", 1.6, 3)
b += eglow(770, 1150, 460, 220, "#FF9F1C", .25)
b += karwa(770, 1238, 1.42, "clay")
b += bangle_stack(250, 1225, .9)
b += mehendi_vine(1040, 60, 700, flip=True, s=.9)
cards["E-%s-5" % CAT] = doc(b)
specs.append(spec(5, [150, 270, 930, 800]))

# 6 ─ PHOTO heart: couple photo in a bead-strung heart under the moon; red chunri drape holds the text
b = sky([(0, "#0B1034"), (.5, "#1C1446"), (1, "#2A0E36")], 6, 700, haze=[(900, 160, 400, 300, "#8E7BD8", .2)])
b += moon(930, 150, 105, seed=9)
hx, hy, hw, hh = 330, 70, 420, 400
b += '<path d="%s" fill="#000" opacity=".45" filter="url(#fB16)" transform="translate(0 14)"/>' % heart_d(hx - 26, hy - 26, hw + 52, hh + 52)
b += '<path d="%s" fill="url(#gGold)"/>' % heart_d(hx - 30, hy - 30, hw + 60, hh + 60)
b += '<path d="%s" fill="none" stroke="#FFF3C4" stroke-width="2" opacity=".8"/>' % heart_d(hx - 27, hy - 27, hw + 54, hh + 54)
b += '<path d="%s" fill="#6E0A20"/>' % heart_d(hx - 8, hy - 8, hw + 16, hh + 16)
b += placeholder_fill(heart_d(hx, hy, hw, hh), hx - 60, hy - 20, hw + 120, hh + 40)
b += bead_string(resample(heart_pts(hx - 18, hy - 18, hw + 36, hh + 36), 17), 6.5)
b += bead_string(resample(heart_pts(hx - 46, hy - 46, hw + 92, hh + 92), 20), 5, ("#FFF3C4",))
# chunri drape
b += '<path d="M0,640 C260,600 820,600 1080,640 L1080,1350 L0,1350Z" fill="#8E0A24"/>'
b += gota_band(0, 640, 1080, 1, ("#8E0A24", "#8E0A24"), scallop="a") if False else ""
gid, gd = lg([(0, "#A0102C"), (1, "#5A0616")], 0, 0, 0, 1)
b += '<defs>%s</defs><path d="M0,640 C260,600 820,600 1080,640 L1080,1350 L0,1350Z" fill="url(#%s)"/>' % (gd, gid)
b += zari_pattern(0, 610, 1080, 740, "#FFD86B", .1, 60)
b += '<path d="M0,640 C260,600 820,600 1080,640" fill="none" stroke="url(#gGoldH)" stroke-width="14"/>'
b += '<path d="M0,660 C260,620 820,620 1080,660" fill="none" stroke="#FFD86B" stroke-width="2" stroke-dasharray="2 9" stroke-linecap="round"/>'
b += thali(540, 640, .78, random.Random(6), with_karwa=False)
b += channi(150, 520, 88, .5, -18, "url(#gGoldH)")
b += karwa(930, 650, .6, "clay")
b += silk_panel(120, 740, 840, 515, "#4A0414", "#2E020C")
cards["E-%s-6" % CAT] = doc(b)
specs.append(spec(6, [165, 780, 915, 1225], photo={"shape": "heart", "x": hx, "y": hy, "w": hw, "h": hh}))

# 7 ─ red-gold chunri wall with a round night window (moon + silhouette); cream panel below (light)
b = gota_band(0, 0, 1080, 1350, ("#A0001A", "#5E0012"), scallop="none")
b += '<circle cx="540" cy="350" r="290" fill="#000" opacity=".35" filter="url(#fB16)"/>'
b += '<defs><clipPath id="win7"><circle cx="540" cy="340" r="272"/></clipPath></defs><g clip-path="url(#win7)">'
b += sky([(0, "#0E0E36"), (1, "#3A1240")], 7, 640, 90)
b += moon(650, 230, 105, seed=4)
b += rooftops(580, random.Random(9), "#1A0A22")
w, _ = woman_moon(440, 604, .56)
b += w + '<rect x="0" y="576" width="1080" height="80" fill="#1A0A20"/></g>'
b += '<circle cx="540" cy="340" r="272" fill="none" stroke="url(#gGold)" stroke-width="16"/>'
b += "".join('<circle cx="%s" cy="%s" r="7" fill="url(#gGold)"/>' % (n(540 + 292 * math.cos(a / 18.0 * math.pi)), n(340 + 292 * math.sin(a / 18.0 * math.pi))) for a in range(36))
b += panel(100, 672, 880, 596, "#FFF5E6", 30, "url(#gGoldH)", 4, True, "fShadow")
b += mehendi_corner(114, 686, .38, 0, "#B5651D", .6) + mehendi_corner(966, 686, .38, 90, "#B5651D", .6)
cards["E-%s-7" % CAT] = doc(b)
specs.append(spec(7, [140, 715, 940, 1228], "light", LIGHT))

# 8 ─ moonrise over a still lake between hills: huge moon, shimmering reflection, ghat step with karwa + thali
b = sky([(0, "#06132C"), (.5, "#10284A"), (1, "#3A3F66")], 8, 1010, 120, haze=[(540, 880, 760, 300, "#FFD9A0", .25)])
b += moon(540, 900, 240, seed=8, halo=1.15)
b += soft_clouds(random.Random(3), 4, 120, 780, 960, 860, "#C8C4E8", .18)
# layered hills in front of the moon's lower edge
b += '<path d="M0,930 C90,900 170,880 250,902 C320,920 360,960 420,985 L660,985 C720,960 780,915 860,896 C950,876 1020,900 1080,920 L1080,1012 L0,1012Z" fill="#1A2748"/>'
b += '<path d="M0,968 C80,952 160,958 240,975 C300,988 360,1000 420,1004 L660,1004 C740,996 820,978 900,966 C980,956 1040,962 1080,970 L1080,1012 L0,1012Z" fill="#0E1A36"/>'
gid, gd = lg([(0, "#22375E"), (.4, "#12244A"), (1, "#060E22")], 0, 0, 0, 1)
b += '<defs>%s</defs><rect x="0" y="1008" width="1080" height="342" fill="url(#%s)"/>' % (gd, gid)
b += '<ellipse cx="540" cy="1080" rx="200" ry="90" fill="#FFE7B0" opacity=".25" filter="url(#fB30)"/>'
rr = random.Random(8)
for k in range(30):
    y = 1014 + k * 8.5
    wdt = (260 - k * 6) * rr.uniform(.6, 1.1)
    for part in range(rr.randint(1, 3)):
        x0 = 540 - wdt / 2 + rr.uniform(-40, 40)
        b += '<rect x="%s" y="%s" width="%s" height="%s" rx="1.5" fill="#FFF1C8" opacity="%s"/>' % (n(x0), n(y), n(wdt * rr.uniform(.25, .6)), n(2 + rr.uniform(0, 2)), round(max(.08, .6 - k * .018), 2))
for k in range(40):
    y = 1020 + rr.uniform(0, 150)
    x0 = rr.uniform(0, 1080)
    b += '<rect x="%s" y="%s" width="%s" height="1.6" fill="#9FB4E0" opacity="%s"/>' % (n(x0), n(y), n(rr.uniform(20, 60)), round(rr.uniform(.08, .2), 2))
# stone ghat step
b += '<rect x="0" y="1178" width="1080" height="172" fill="#1A1420"/><rect x="0" y="1172" width="1080" height="10" fill="url(#gGoldH)" opacity=".85"/>'
b += zari_pattern(0, 1182, 1080, 168, "#FFD86B", .06, 56)
b += thali(215, 1162, .6, random.Random(9), with_karwa=False)
b += karwa(885, 1180, .66, "brass")
b += four_corners(24, .7, op=.9)
cards["E-%s-8" % CAT] = doc(b)
specs.append(spec(8, [150, 130, 930, 650]))

# 9 ─ PHOTO arch: couple photo in a gold arch under red chunri swags; maroon with zari lattice
b = bg_grad([(0, "#6E0A20"), (1, "#34050F")]) + zari_pattern(0, 0, 1080, 1350, "#FFD86B", .07, 72) + noise(.05, "overlay")
b += bokeh(random.Random(9), 26, 0, 0, 1080, 1350, ["#FFD27A", "#FF7A59"], 8, 30, (.05, .15))
ax, ay, aw, ah = 330, 120, 420, 520
b += moon(952, 250, 62, seed=1, halo=.8)
b += frame("arch", ax, ay, aw, ah, "mgold", 0, 22).replace("#8C7A55", "#8A5A16").replace("#E6D8B2", "#FFE7A8").replace("#6F603F", "#7A4E12")
b += placeholder_fill(shape_d("arch", ax, ay, aw, ah), ax, ay, aw, ah)
b += bead_string(shape_pts("arch", ax, ay, aw, ah, 36, 20)[1:-1], 5.5)
b += chunri_swag(-20, 540, 16, 40, 40) + chunri_swag(540, 1100, 16, 40, 40)
b += channi(185, 470, 95, .6, -12, "url(#gGoldH)")
b += bangle_stack(90, 1238, .58) + bangle_stack(990, 1238, .58, ("#FFB000", "#C8102E", "#0F7B3F"))
cards["E-%s-9" % CAT] = doc(b)
specs.append(spec(9, [160, 700, 920, 1232], photo={"shape": "arch", "x": ax, "y": ay, "w": aw, "h": ah}))

# 10 ─ PHOTO oval: couple seen through the channi held up to a huge moon; midnight-blue glass panel
b = sky([(0, "#081030"), (.5, "#141A4A"), (1, "#0A0C26")], 10, haze=[(860, 200, 520, 420, "#7A8AE0", .18)])
b += moon(880, 190, 250, seed=6, halo=1.0)
b += soft_clouds(random.Random(10), 4, 560, 330, 1080, 460, "#B8B4E8", .2)
b += mehendi_mandala(400, 335, 380, "#E9B95B", .12, 2)
b += karwa(860, 704, .6, "brass") + diya(700, 700, .38, "clay") + diya(1010, 700, .34, "clay")
ox, oy, ow, oh = 195, 70, 410, 470
cx_, cy_ = ox + ow / 2, oy + oh / 2
b += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#000" opacity=".5" filter="url(#fB16)"/>' % (cx_ + 10, cy_ + 16, ow / 2 + 40, oh / 2 + 40)
for i in range(48):  # red lace beads
    a = 2 * math.pi * i / 48
    b += '<circle cx="%s" cy="%s" r="15" fill="#C8102E"/><circle cx="%s" cy="%s" r="6" fill="#FFD86B"/>' % (
        n(cx_ + (ow / 2 + 50) * math.cos(a)), n(cy_ + (oh / 2 + 50) * math.sin(a)), n(cx_ + (ow / 2 + 50) * math.cos(a)), n(cy_ + (oh / 2 + 50) * math.sin(a)))
b += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="url(#gGold)" stroke-width="40"/>' % (cx_, cy_, ow / 2 + 22, oh / 2 + 22)
b += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="#FFF3C4" stroke-width="2" opacity=".8"/>' % (cx_, cy_, ow / 2 + 38, oh / 2 + 38)
for i in range(36):
    a = 2 * math.pi * (i + .5) / 36
    b += '<circle cx="%s" cy="%s" r="5" fill="#8E0F2A"/>' % (n(cx_ + (ow / 2 + 22) * math.cos(a)), n(cy_ + (oh / 2 + 22) * math.sin(a)))
b += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="#5A3A0E" stroke-width="3"/>' % (cx_, cy_, ow / 2 + 3, oh / 2 + 3)
b += placeholder_fill("M%s,%s a%s,%s 0 1 0 %s,0 a%s,%s 0 1 0 %s,0 Z" % (ox, cy_, ow / 2, oh / 2, ow, ow / 2, oh / 2, -ow), ox, oy, ow, oh, ("#E9E4F6", "#C9C0E4"), "#B3A8D6")
for i in range(5):
    t = (i + 1) / 6.0
    a = math.pi * (.3 + .4 * t)
    b += tassel(cx_ + (ow / 2 + 60) * math.cos(a), cy_ + (oh / 2 + 60) * math.sin(a) - 6, .8)
b += panel(100, 700, 880, 560, "#FFFFFF", 34, "url(#gGoldH)", 3, True, "fShadow", op=1).replace('fill="#FFFFFF"', 'fill="#1A2058" fill-opacity=".78"', 1)
b += mehendi_corner(114, 714, .36, 0, "#E9B95B", .5) + mehendi_corner(966, 714, .36, 90, "#E9B95B", .5)
b += mehendi_corner(966, 1246, .36, 180, "#E9B95B", .5) + mehendi_corner(114, 1246, .36, 270, "#E9B95B", .5)
cards["E-%s-10" % CAT] = doc(b)
specs.append(spec(10, [150, 745, 930, 1215], photo={"shape": "oval", "x": ox, "y": oy, "w": ow, "h": oh}))

if __name__ == "__main__":
    only = sys.argv[1:]
    render_cards({k: v for k, v in cards.items() if not only or k.split("-")[-1] in only})
    save_specs(CAT, specs)
