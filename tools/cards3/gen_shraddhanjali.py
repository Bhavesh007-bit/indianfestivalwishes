"""Shraddhanjali (tribute / besnu / uthamnu) card art: 10 sober photo-slot designs.
Run: python3 tools/cards3/gen_shraddhanjali.py
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_b import *
from render import render_cards

CAT = "shraddhanjali"
LIGHT = dict(title="#2E2D2A", text="#34322E", accent="#6F5E3C")


def spec(i, zone, photo, tone="light", colors=None, title="classic"):
    d = {"id": "E-%s-%d" % (CAT, i), "tpl": True, "zone": zone, "colors": colors or LIGHT, "tone": tone,
         "title": title, "align": "center", "photo": photo, "slot": True}
    return d


def P(shape, x, y, w, h):
    return {"shape": shape, "x": x, "y": y, "w": w, "h": h}


def slot(shape, x, y, w, h, frame_style, frame_w=18, dark=False):
    ph = ("#4A4B4D", "#3A3B3D") if dark else ("#EFEBE3", "#DCD6CB")
    fig = "#5B5C5E" if dark else "#CFC7BA"
    return frame(shape, x, y, w, h, frame_style, 0, frame_w) + photo_placeholder(shape, x, y, w, h, ph, fig)


cards, specs = {}, []

# 1 ─ ivory, jasmine-draped arch, diya + incense beside the photo
r = random.Random(1)
b = bg_grad([(0, "#FBF8F1"), (.6, "#F3EEE3"), (1, "#E9E2D4")])
b += light_rays(160, -60, [48, 60, 72, 84], 1700, 6, "#FFFFFF", .55)
b += eglow(540, 250, 420, 300, "#FFFFFF", .7) + paper(.07)
b += hairline_frame(28) + hairline_frame(38, op=.5) + mcorners(28, .5)
b += slot("arch", 390, 60, 300, 380, "mgold", 16)
b += jasmine_garland2("arch", 390, 60, 300, 380, pad=26, rng=r, sag=34, tassel=False)
b += calm_diya(178, 450, .78)
b += incense(900, 470, .85, rng=r)
b += thin_ornament_line(540, 520, 250, op=.8)
cards["E-%s-1" % CAT] = doc(b)
specs.append(spec(1, [150, 548, 930, 1252], P("arch", 390, 60, 300, 380)))

# 2 ─ charcoal, spotlight, rajnigandha rope around an oval, white lilies flanking
r = random.Random(2)
b = bg_grad([(0, "#34363A"), (1, "#1C1D20")])
b += eglow(540, 230, 520, 420, "#6C6E72", .55) + noise(.06, "overlay")
b += '<rect x="26" y="26" width="1028" height="1298" fill="none" stroke="url(#gSilver)" stroke-width="2" opacity=".55"/>'
b += mcorners(26, .5, "url(#gSilver)", .7)
b += lily_spray(300, 470, .9, mirror=True, rng=r) + lily_spray(780, 470, .9, rng=r)
b += slot("oval", 385, 55, 310, 385, "silver", 16, dark=True)
b += rajnigandha_rope2("oval", 385, 55, 310, 385, pad=28, rng=r, sag=30)
b += thin_ornament_line(540, 528, 230, "url(#gSilver)", .7)
cards["E-%s-2" % CAT] = doc(b)
specs.append(spec(2, [150, 556, 930, 1256], P("oval", 385, 55, 310, 385), "dark",
                  dict(title="#F4F1EA", text="#ECE8E0", accent="#D2C6A6")))

# 3 ─ sage wall, carved wood frame with sandalwood garland on a ledge; diya + lotus bowl + incense; cream panel
r = random.Random(3)
b = bg_grad([(0, "#DDE4D8"), (1, "#C4CEBF")])
b += "".join('<rect x="%d" y="0" width="2" height="1350" fill="#FFFFFF" opacity=".18"/>' % x for x in range(0, 1080, 36))
b += paper(.06)
b += '<rect x="60" y="468" width="960" height="20" rx="4" fill="#7A6450" filter="url(#fShadowS)"/><rect x="60" y="468" width="960" height="5" fill="#A48A70"/>'
b += slot("rect", 385, 58, 310, 360, "wood", 26)
b += sandal_garland2("rect", 385, 58, 310, 360, pad=32, sag=26)
b += calm_diya(200, 440, .7)
b += '<ellipse cx="880" cy="452" rx="74" ry="16" fill="url(#gMGold)"/>' + lotus(880, 452, .52)
b += panel(110, 520, 860, 760, "#FBF8F2", 26, "url(#gMGold)", 2, True, "fShadowSoft")
cards["E-%s-3" % CAT] = doc(b)
specs.append(spec(3, [150, 560, 930, 1250], P("rect", 385, 58, 310, 360),
                  colors=dict(title="#2F3A30", text="#303630", accent="#5E6B4E")))

# 4 ─ white marble, rounded photo left, dove flying into soft rays, jasmine
r = random.Random(4)
b = bg_grad([(0, "#FAFAF8"), (1, "#E7E6E2")]) + marble(.55, 4)
b += light_rays(1080, -40, [110, 122, 134, 146, 158], 1600, 5, "#FFFFFF", .8)
b += eglow(860, 120, 300, 200, "#FFF6E0", .6)
b += soft_clouds(r, 3, 640, 330, 1000, 440, "#FFFFFF", .8)
b += slot("rounded", 130, 64, 320, 380, "marble", 18)
b += jasmine_garland2("rounded", 130, 64, 320, 380, pad=26, rng=r, sag=30)
b += dove(790, 250, 1.05, -10)
b += dove(960, 150, .5, -16)
b += hairline_frame(30, "url(#gSilver)", .7)
b += thin_ornament_line(540, 530, 260, "url(#gMGold)", .8)
cards["E-%s-4" % CAT] = doc(b)
specs.append(spec(4, [150, 556, 930, 1256], P("rounded", 130, 64, 320, 380),
                  colors=dict(title="#2C2E33", text="#33353A", accent="#6A6F78")))

# 5 ─ warm beige, tall rajnigandha stems in a glass vase down the left, arch photo, text on the right
r = random.Random(5)
b = bg_grad([(0, "#F1EBDF"), (1, "#E2D8C7")], 0, 0, 1, 1) + paper(.08)
b += eglow(150, 700, 260, 600, "#FFFFFF", .5)
b += glass_vase(130, 1240, 120, 250)
for k, (dx, ln, rot) in enumerate(((-34, 600, -6), (-10, 720, -2), (12, 680, 3), (32, 560, 6), (0, 500, -9))):
    b += rajnigandha_stem(130 + dx, 1100, ln, 1.05, rot, random.Random(k + 50))
b += leaf(100, 1000, 90, -40, "#9DB096") + leaf(160, 1000, 90, 40, "#8FA08A")
b += '<rect x="236" y="40" width="1.6" height="1270" fill="url(#gMGold)" opacity=".7"/>'
b += slot("arch", 502, 60, 300, 370, "mgold", 16)
b += jasmine_garland2("arch", 502, 60, 300, 370, pad=26, rng=r, sag=30)
b += hairline_frame(28, op=.6)
cards["E-%s-5" % CAT] = doc(b)
specs.append(spec(5, [262, 540, 1042, 1250], P("arch", 502, 60, 300, 370),
                  colors=dict(title="#3A2F25", text="#3A332B", accent="#735C3A")))

# 6 ─ warm slate night, rect photo with muted gold frame, one calm diya glowing below, incense smoke at both sides
r = random.Random(6)
b = bg_grad([(0, "#3A3B3E"), (1, "#222326")]) + noise(.05, "overlay")
b += eglow(540, 480, 420, 260, "#8C7A55", .28)
b += incense(92, 620, .9, 2, r, "#B9B5AE") + incense(988, 620, .9, 2, random.Random(66), "#B9B5AE")
b += slot("rect", 390, 56, 300, 330, "mgold", 16, dark=True)
b += jasmine_garland2("rect", 390, 56, 300, 330, pad=26, rng=r, sag=6, tassel=False)
b += calm_diya(506, 492, .6)
b += mcorners(24, .5, "url(#gMGold)", .7)
b += lotus(92, 1252, .36) + lotus(988, 1252, .36)
b += '<rect x="24" y="24" width="1032" height="1302" fill="none" stroke="url(#gMGold)" stroke-width="2" opacity=".6"/>'
cards["E-%s-6" % CAT] = doc(b)
specs.append(spec(6, [150, 548, 930, 1254], P("rect", 390, 56, 300, 330), "dark",
                  dict(title="#F2E9D6", text="#EAE6DE", accent="#D6C49C")))

# 7 ─ soft clouds and heavenly rays behind an oval, two doves
r = random.Random(7)
b = bg_grad([(0, "#E4E7EA"), (.5, "#EEF0F1"), (1, "#F6F5F2")])
b += light_rays(540, 250, list(range(-180, 180, 15)), 900, 5, "#FFFFFF", .9)
b += eglow(540, 250, 360, 300, "#FFFFFF", .9)
b += soft_clouds(r, 7, 0, 330, 1080, 520, "#FFFFFF", .95)
b += slot("oval", 390, 60, 300, 380, "silver", 14)
b += jasmine_garland2("oval", 390, 60, 300, 380, pad=24, rng=r, sag=30)
b += dove(180, 200, .8, -8, True) + dove(900, 160, .8, -8)
b += hairline_frame(30, "url(#gSilver)", .8) + mcorners(30, .5, "url(#gSilver)", .8)
cards["E-%s-7" % CAT] = doc(b)
specs.append(spec(7, [150, 560, 930, 1256], P("oval", 390, 60, 300, 380),
                  colors=dict(title="#2B3036", text="#31363C", accent="#5E6670")))

# 8 ─ lotus pond: marble arch rising above calm water with white lotuses; text on a cream panel
r = random.Random(8)
b = bg_grad([(0, "#F4F0E8"), (1, "#EAE4D8")]) + paper(.06)
b += '<defs><linearGradient id="pond8" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DDE5DC"/><stop offset="1" stop-color="#C3D0C4"/></linearGradient></defs>'
b += '<rect x="0" y="0" width="1080" height="520" fill="url(#pond8)"/>'
b += light_rays(540, -100, [70, 80, 90, 100, 110], 800, 6, "#FFFFFF", .7)
for k in range(9):
    b += '<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="#FFFFFF" stroke-width="1.6" opacity=".5"/>' % (r.randint(60, 1020), r.randint(400, 500), r.randint(40, 120), r.randint(5, 10))
b += slot("arch", 390, 44, 300, 360, "marble", 18)
b += lotus_leaf(210, 488, 120, 22) + lotus_leaf(870, 488, 120, 22) + lotus_leaf(340, 500, 70, 12) + lotus_leaf(745, 500, 70, 12)
b += lotus(200, 470, .62) + lotus(880, 470, .62) + lotus(330, 492, .36) + lotus(752, 492, .36)
b += '<rect x="0" y="516" width="1080" height="10" fill="url(#gMGold)" opacity=".85"/>'
b += panel(100, 560, 880, 730, "#FFFDF8", 20, "url(#gMGold)", 2, True, "fShadowSoft")
cards["E-%s-8" % CAT] = doc(b)
specs.append(spec(8, [150, 590, 930, 1262], P("arch", 390, 44, 300, 360),
                  colors=dict(title="#2E3A33", text="#313732", accent="#5A6A57")))

# 9 ─ taupe linen with a cream plaque; rounded photo overlaps the plaque top; lilies in the top corners
r = random.Random(9)
b = bg_grad([(0, "#D3CCC2"), (1, "#BFB7AB")]) + linen(.08)
b += panel(80, 250, 920, 1020, "#FBF8F2", 24, "url(#gMGold)", 2.4, True, "fShadowSoft")
b += lily_spray(150, 300, .78, rng=r) + lily_spray(930, 300, .78, mirror=True, rng=r)
b += slot("rounded", 395, 44, 290, 340, "mgold", 16)
b += rajnigandha_rope2("rounded", 395, 44, 290, 340, pad=26, rng=r, sag=28, tassel=True)
cards["E-%s-9" % CAT] = doc(b)
specs.append(spec(9, [150, 548, 930, 1236], P("rounded", 395, 44, 290, 340),
                  colors=dict(title="#3A332B", text="#3A352F", accent="#6F5E3C")))

# 10 ─ deep olive-grey with jasmine strings hanging from the top edge, oval photo in the middle
r = random.Random(10)
b = bg_grad([(0, "#434A44"), (1, "#262A27")]) + noise(.05, "overlay")
b += eglow(540, 260, 400, 320, "#8E9A8F", .35)
for k, x in enumerate(range(40, 1060, 44)):
    if 330 < x < 750:
        ln = 20 + abs(540 - x) * .05
    else:
        ln = 180 + (abs(540 - x) - 210) * 1.6 + (k % 3) * 30
    b += jasmine_strand(x, 0, min(ln, 560), .95, random.Random(x))
b += '<path d="M0,6 Q540,40 1080,6" stroke="#E9E4D6" stroke-width="3" fill="none"/>'
b += slot("oval", 395, 70, 290, 370, "mgold", 14, dark=True)
b += jasmine_garland2("oval", 395, 70, 290, 370, pad=24, rng=r, sag=26, tassel=False)
b += thin_ornament_line(540, 540, 220, "url(#gMGold)", .8)
cards["E-%s-10" % CAT] = doc(b)
specs.append(spec(10, [150, 566, 930, 1256], P("oval", 395, 70, 290, 370), "dark",
                  dict(title="#F3EEE2", text="#EAE7DF", accent="#D3C8A8")))

if __name__ == "__main__":
    only = sys.argv[1:]
    render_cards({k: v for k, v in cards.items() if not only or k.split("-")[-1] in only})
    save_specs(CAT, specs)
