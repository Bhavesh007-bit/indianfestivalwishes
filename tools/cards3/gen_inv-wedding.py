"""inv-wedding: 10 premium Indian wedding invitation templates (lib_c family)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motifs_invw_c import *
from render import render_cards

CAT = "inv-wedding"


def base_bg(d, c0, c1, c2=None, pat=None):
    st = [(0, c0), (1, c1)] if not c2 else [(0, c0), (0.55, c1), (1, c2)]
    o = '<rect width="1080" height="1350" fill="%s"/>' % d.lg(st)
    if pat:
        o += '<rect width="1080" height="1350" fill="%s"/>' % pat
    return o


def parchment(d, x, y, w, h, r=0, c0="#FFF8EA", c1="#F6E6C8", shadow=True, grain=True):
    f = ' filter="%s"' % d.shadow(0, 14, 18, "#000", 0.35) if shadow else ""
    o = '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"%s/>' % (n(x), n(y), n(w), n(h), n(r), d.rg([(0, c0), (1, c1)], 0.5, 0.45, 0.75), f)
    if grain:
        cp = d.clip('<rect x="%s" y="%s" width="%s" height="%s" rx="%s"/>' % (n(x), n(y), n(w), n(h), n(r)))
        o += grain_rect(d, x, y, w, h, 0.05, "#8A6A3A", 0.8, cp)
    return o


def shehnai_at(d, x, y, ang, s=1):
    """mouthpiece at (x,y), pointing at angle ang (deg) with tassel kept below"""
    flipv = 90 < (ang % 360) < 270
    sc = "scale(%s %s)" % (n(s), n(-s if flipv else s))
    return '<g transform="translate(%s %s) rotate(%s) %s">%s</g>' % (n(x), n(y), n(ang), sc, shehnai(d, 0, 0, 1))


# ------------------------------------------------------------------ 1 royal mandap
def card1():
    d = Doc(11)
    o = [base_bg(d, "#3E0410", "#6E0A1C", "#3A0410", damask_pattern(d, "#E9B949", None, 150, 0.10))]
    o.append('<ellipse cx="540" cy="300" rx="520" ry="330" fill="%s"/>' % d.rg([(0, "#FFB35C", 0.55), (1, "#FFB35C", 0)]))
    o.append(bokeh(d, d.rnd, 26, 20, 20, 1060, 480, 6, 22, ["#FFD27A", "#FF9E6B", "#FFF1C9"], 0.15, 0.45))
    o.append(mandap(d, 540, 505, 880, 425, seed=4))
    # parchment panel
    o.append(parchment(d, 64, 520, 952, 772, 18))
    o.append(gold_frame_rect(d, 84, 540, 912, 732, 10, 5))
    o.append(gota_border(d, 106, 562, 868, 688, "#C8922E", 20))
    o.append(corners(d, 112, 568, 968, 1244, 0.55, sw=3))
    # paisleys at panel sides (outside zone)
    for y_ in (720, 1090):
        o.append(paisley(d, 30, y_, 0.36, 0, "#7A0A1E", "#E9C46A", "#FFF3D6"))
        o.append(paisley(d, 1050, y_, 0.36, 0, "#7A0A1E", "#E9C46A", "#FFF3D6", flip=True))
    return d.svg("".join(o)), spec("E-inv-wedding-1", (150, 580, 930, 1235), "#7A0A1E", "#3A1E14", "#8A5A0A", "light", "deco", bg="#FBF0DC")


# ------------------------------------------------------------------ 2 elephant pair, royal blue
def card2():
    d = Doc(12)
    o = [base_bg(d, "#0B2340", "#113A63", "#0A1F38", damask_pattern(d, "#E9C46A", None, 130, 0.12))]
    o.append('<ellipse cx="540" cy="1150" rx="620" ry="260" fill="%s"/>' % d.rg([(0, "#3B7BC0", 0.55), (1, "#3B7BC0", 0)]))
    # top toran with bells (skip centre)
    o.append(toran(d, -20, 1100, 18, 64, 14, bells=False))
    for px in (150, 330, 750, 930):
        o.append('<line x1="%s" y1="18" x2="%s" y2="96" stroke="#6B3A12" stroke-width="1.5"/>' % (px, px))
        o.append(marigold(d, px, 64, 11, "red"))
        o.append(bell(d, px, 80, 0.4))
    # panel with foil-arch crest
    o.append('<path d="%s" fill="%s" filter="%s"/>' % (foil_arch_d(380, 108, 320, 120, 0.6, 7), d.gold(), d.shadow(0, 8, 10, "#000", .35)))
    o.append(parchment(d, 96, 160, 888, 790, 22, "#FFFBF2", "#F3E5CC"))
    o.append('<path d="%s" fill="%s"/>' % (foil_arch_d(396, 124, 288, 110, 0.6, 7), d.lg([(0, "#FFFBF2"), (1, "#F9EFDC")])))
    o.append(ganesh(d, 540, 186, 0.28, sw=7, bg="#FFF8EA"))
    o.append(gold_frame_rect(d, 114, 178, 852, 754, 14, 4))
    for (cx_, cy_, rot) in ((114, 178, 0), (966, 178, 90), (966, 932, 180), (114, 932, 270)):
        o.append(g('<path d="M0,0 L60,0 A60,60 0 0 1 0,60Z" fill="%s" opacity=".9"/>' % d.gold() + '<path d="M0,0 L40,0 A40,40 0 0 1 0,40Z" fill="#0F325A"/>' + mandala(d, 16, 16, 14, "#B3122E", "#7A0A1E", "#FFF3D6", detail=0), cx_, cy_, 1, rot))
    # elephants + kalash on a carpet ledge
    o.append('<rect x="0" y="1262" width="1080" height="88" fill="%s"/>' % d.lg([(0, "#07182B"), (1, "#0B2340")]))
    o.append('<rect x="0" y="1258" width="1080" height="8" fill="%s"/>' % d.lg(GOLD, 0, 0, 1, 0, key="goldh"))
    o.append('<ellipse cx="220" cy="1262" rx="200" ry="16" fill="#000" opacity=".35"/><ellipse cx="860" cy="1262" rx="200" ry="16" fill="#000" opacity=".35"/>')
    o.append(elephant(d, 28, 1266, 0.8, cloth=("#B3122E", "#6E0A1C"), seed=3))
    o.append(elephant(d, 676, 1266, 0.8, flip=True, cloth=("#B3122E", "#6E0A1C"), seed=5))
    o.append(kalash(d, 540, 1262, 0.98))
    o.append(swag(d, 400, 1000, 680, 1000, 60, 12, ("orange", "yellow")))
    return d.svg("".join(o)), spec("E-inv-wedding-2", (150, 205, 930, 905), "#0F2F57", "#26211C", "#8A5A0A", "light", "classic", bg="#FBF4E6")


# ------------------------------------------------------------------ 3 pink palace jharokha
def card3():
    d = Doc(13)
    stone = d.lg([(0, "#F2B7AE"), (0.5, "#E39A92"), (1, "#C97A74")])
    o = ['<rect width="1080" height="1350" fill="%s"/>' % stone]
    # block courses
    blk = []
    for yy in range(0, 1350, 54):
        blk.append('<line x1="0" y1="%d" x2="1080" y2="%d" stroke="#B36962" stroke-width="1.4" opacity=".35"/>' % (yy, yy))
        off = 0 if (yy // 54) % 2 else 60
        for xx in range(off, 1080, 120):
            blk.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#B36962" stroke-width="1.2" opacity=".3"/>' % (xx, yy, xx, yy + 54))
    o.append("".join(blk))
    o.append(grain_rect(d, 0, 0, 1080, 1350, 0.06, "#6E2E2A", 0.7))
    # outer carved ring (marble)
    ring_out = foil_arch_d(40, 84, 1000, 1110, 0.30, 11, 0)
    o.append('<path d="%s" fill="%s" filter="%s"/>' % (ring_out, d.lg([(0, "#FFFDF8"), (1, "#EADBC8")]), d.shadow(0, 10, 16, "#5A1E1A", .4)))
    # inlay flowers on marble ring (pietra dura), sampled along the arch
    pts = pointed_arch_pts(66, 112, 948, 1090 * 0.30 / 0.30, 0.285, 0.62, 200)
    for i, (px, py) in enumerate(pts[6:-6:8]):
        o.append('<g transform="translate(%s %s)">%s%s</g>' % (n(px), n(py), ring_petals(6, 2, 11, 4.5, "#C0405E", "none", 1, i * 15), '<circle r="3" fill="#2F7A5A"/>'))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="5"/>' % (foil_arch_d(62, 104, 956, 1090, 0.30, 11), d.gold()))
    # opening
    op = foil_arch_d(90, 140, 900, 1045, 0.27, 13)
    o.append('<path d="%s" fill="%s"/>' % (op, d.rg([(0, "#FFFCF4"), (0.7, "#FBEFDC"), (1, "#F2DCC0")], 0.5, 0.45, 0.8)))
    cp = d.clip('<path d="%s"/>' % op)
    o.append('<g clip-path="%s">%s</g>' % (cp, grain_rect(d, 90, 140, 900, 1045, 0.04, "#8A6A3A")))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="3"/>' % (op, "#B98A3A"))
    # marigold festoon inside the arch top
    pts = pointed_arch_pts(118, 170, 844, 1000, 0.25, 0.62, 400)
    seg = [p for p in pts if p[1] < 420]
    fl = path_pts(seg, 21)
    o.append(flower_ring(d, fl, 11, "marigold", ("orange", "yellow"), 4, cx=540, cy=700))
    for (px, py, a) in fl[::7]:
        o.append(marigold_string(d, px, py, py + 34, 8, ("red", "yellow")))
    # chhatris top corners
    for cx_ in (100, 980):
        o.append(chhatri(d, cx_, 250, 118, d.lg([(0, "#F7C9C0"), (1, "#C97A74")], 0.2, 0, 0.8, 1, key="pinkd"), d.gold(), "#FFF4EA"))
    # apex finial
    o.append(dome(d, 540, 84, 110, 58, d.gold(), d.gold()))
    # balcony
    o.append('<rect x="60" y="1184" width="960" height="26" fill="%s"/>' % d.lg([(0, "#FFFDF8"), (1, "#E0CDB8")]))
    for k in range(25):
        x_ = 78 + k * 38.5
        o.append('<path d="M%s,1212 q-9,16 0,30 q9,-14 0,-30Z" fill="#EADBC8" stroke="#B98A8A" stroke-width="1"/>' % n(x_))
    o.append('<rect x="50" y="1240" width="980" height="16" fill="%s"/>' % d.gold())
    for k in range(7):
        x_ = 110 + k * 143
        if 300 < x_ < 780:
            continue
        o.append('<path d="M%s,1256 L%s,1256 C%s,1296 %s,1316 %s,1322 C%s,1300 %s,1280 %s,1256Z" fill="#E7D3C0" stroke="#B98A8A"/>' % (
            n(x_ - 26), n(x_ + 26), n(x_ + 24), n(x_ + 8), n(x_), n(x_ - 10), n(x_ - 24), n(x_ - 26)))
    return d.svg("".join(o)), spec("E-inv-wedding-3", (150, 450, 930, 1150), "#8E1B3A", "#3B1F2B", "#8A4B12", "light", "deco", bg="#FBF0E0")


# ------------------------------------------------------------------ 4 emerald jharokha photo + shehnai
def card4():
    d = Doc(14)
    o = [base_bg(d, "#0D4A38", "#0A3528", "#062219", jali_pattern(d, "#E9C46A", None, 44, 1.2))]
    o.append('<rect width="1080" height="1350" fill="%s"/>' % d.lg([(0, "#0A3528", 0.55), (1, "#062219", 0.85)]))
    o.append('<ellipse cx="540" cy="270" rx="430" ry="300" fill="%s"/>' % d.rg([(0, "#F7D98C", 0.45), (1, "#F7D98C", 0)]))
    ph = {"shape": "arch", "x": 380, "y": 104, "w": 320, "h": 340}
    # outer cusped jharokha outline
    o.append('<path d="%s" fill="%s" filter="%s"/>' % (foil_arch_d(330, 64, 420, 420, 0.42, 9, 0), d.gold(), d.shadow(0, 10, 14, "#000", .45)))
    o.append('<path d="%s" fill="#0B3F30"/>' % foil_arch_d(342, 76, 396, 404, 0.42, 9))
    o.append('<path d="%s" fill="%s"/>' % (foil_arch_d(342, 76, 396, 404, 0.42, 9), jali_pattern(d, "#E9C46A", None, 26, 1.4)))
    o.append(photo_slot(d, ph, "#FFF8EA", "#F1DEBF", "#C9A98A", ring_w=12, inner="#7A4A0E"))
    o.append(dome(d, 540, 64, 120, 60, d.gold(), d.gold()))
    # side pillars of the window
    for x_ in (318, 740):
        o.append('<rect x="%d" y="160" width="22" height="330" fill="%s"/>' % (x_, d.lg(GOLD, 0, 0, 1, 0, key="goldh")))
    o.append('<rect x="300" y="478" width="480" height="18" rx="4" fill="%s"/>' % d.gold())
    # shehnais heralding
    o.append(shehnai_at(d, 318, 420, 215, 0.72))
    o.append(shehnai_at(d, 762, 420, -35, 0.72))
    # side marigold strings
    for x_, L in ((34, 470), (82, 330), (998, 330), (1046, 470)):
        o.append(marigold_string(d, x_, 0, L, 13, ("orange", "yellow")))
    # panel
    o.append(parchment(d, 92, 500, 896, 790, 26, "#FFFBF1", "#F4E7CE"))
    o.append(gold_frame_rect(d, 110, 518, 860, 754, 18, 4))
    o.append(corners(d, 124, 532, 956, 1258, 0.5, sw=3))
    return d.svg("".join(o)), spec("E-inv-wedding-4", (150, 540, 930, 1245), "#0B4A36", "#23261F", "#8A5A0A", "light", "classic", photo=ph, bg="#FBF3E4")


# ------------------------------------------------------------------ 5 marigold curtain, peacock blue
def card5():
    d = Doc(15)
    o = [base_bg(d, "#0E5566", "#0B3E4C", "#072A34", buti_pattern(d, "#F2C45A", None, 70, 0.18))]
    o.append('<ellipse cx="540" cy="760" rx="600" ry="520" fill="%s"/>' % d.rg([(0, "#35A3AE", 0.35), (1, "#35A3AE", 0)]))
    # rod + valance
    o.append('<rect x="0" y="18" width="1080" height="14" fill="%s"/>' % d.lg(GOLD, 0, 0, 0, 1, key="goldv"))
    val = "M0,32 " + " ".join("Q%s,%s %s,32" % (n(i * 60 + 30), 92, n(i * 60 + 60)) for i in range(18)) + " L1080,0 L0,0Z"
    o.append('<path d="%s" fill="%s"/>' % (val, d.lg([(0, "#C2185B"), (1, "#7B0F3A")])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="4"/>' % (" ".join("M%s,32 Q%s,92 %s,32" % (n(i * 60), n(i * 60 + 30), n(i * 60 + 60)) for i in range(18)), d.gold()))
    for i in range(18):
        o.append(tassel(d, i * 60 + 30, 62, 0.45, "#7B0F3A"))
    # curtain strings
    L = [620, 520, 300, 250, 215, 190, 175, 165, 160, 165, 175, 190, 215, 250, 300, 520, 620]
    o.append(curtain_strings(d, 30, 1050, 90, L, 13, ("orange", "yellow")))
    # scroll panel
    o.append('<rect x="100" y="372" width="880" height="800" fill="%s" filter="%s"/>' % (d.lg([(0, "#FFF8E8"), (0.5, "#FBEBCB"), (1, "#FFF6E2")], 0, 0, 1, 0), d.shadow(0, 14, 18, "#000", .4)))
    o.append(grain_rect(d, 100, 372, 880, 800, 0.05, "#8A6A3A"))
    for yy, flip in ((352, False), (1172, True)):
        roll = d.lg([(0, "#E7C9A0"), (0.4, "#FFF6E2"), (0.6, "#F1D9B0"), (1, "#B98D5A")], 0, 0, 0, 1)
        o.append('<rect x="78" y="%d" width="924" height="42" rx="21" fill="%s" filter="%s"/>' % (yy, roll, d.shadow(0, 6, 6, "#000", .35)))
        for ex in (78, 1002):
            o.append('<ellipse cx="%d" cy="%d" rx="12" ry="21" fill="%s"/><circle cx="%d" cy="%d" r="9" fill="%s"/>' % (ex, yy + 21, "#B98D5A", ex + (-12 if ex < 500 else 12), yy + 21, d.gold()))
    o.append('<rect x="124" y="410" width="832" height="728" fill="none" stroke="%s" stroke-width="3"/>' % d.gold())
    o.append('<rect x="134" y="420" width="812" height="708" fill="none" stroke="#C2185B" stroke-width="1.5" opacity=".6"/>')
    # bottom paisleys
    for x_, fl in ((150, False), (930, True)):
        o.append(paisley(d, x_, 1290, 0.55, -20 if not fl else 20, "#C2185B", "#F2C45A", "#FFE9C2", flip=fl))
    o.append(dots_ring(1, 0, 5, "#F2C45A", 280, 1300) + dots_ring(1, 0, 5, "#F2C45A", 800, 1300))
    return d.svg("".join(o)), spec("E-inv-wedding-5", (150, 430, 930, 1128), "#0B4A5A", "#2A2320", "#9A2458", "light", "deco", bg="#FDF3E0")


# ------------------------------------------------------------------ 6 henna kraft with Ganesh medallion
def henna_vine(d, x1, y1, x2, y2, col, sag=0, leaves=10):
    fn = swag_fn(x1, y1, x2, y2, sag)
    o = ['<path d="%s" fill="none" stroke="%s" stroke-width="3"/>' % (swag_d(x1, y1, x2, y2, sag), col)]
    for i, ((px, py), a) in enumerate(sample(fn, max(20, math.hypot(x2 - x1, y2 - y1) / leaves))):
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="2" transform="translate(%s %s) rotate(%s)"/>' % (leaf_d(22, 7), col, n(px), n(py), n(a + (60 if i % 2 else 120))))
        o.append('<circle cx="%s" cy="%s" r="2.4" fill="%s"/>' % (n(px), n(py), col))
    return "".join(o)


def card6():
    d = Doc(16)
    H_ = "#5E2410"
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.rg([(0, "#E9C79E"), (1, "#C99A68")], 0.5, 0.4, 0.8)]
    o.append(grain_rect(d, 0, 0, 1080, 1350, 0.10, "#5E3A1A", 0.75))
    # border lines
    o.append('<rect x="22" y="22" width="1036" height="1306" fill="none" stroke="%s" stroke-width="3"/>' % H_)
    o.append('<rect x="34" y="34" width="1012" height="1282" fill="none" stroke="%s" stroke-width="1.5" stroke-dasharray="2 7" stroke-linecap="round"/>' % H_)
    # scalloped henna edge along sides
    for side in ("l", "r"):
        x_ = 46 if side == "l" else 1034
        for k in range(26):
            y_ = 60 + k * 48
            if y_ > 1260:
                break
            sg = 1 if side == "l" else -1
            o.append('<path d="M%s,%s q%s,24 0,48" fill="none" stroke="%s" stroke-width="2.4"/>' % (x_, y_, 22 * sg, H_))
            o.append('<circle cx="%s" cy="%s" r="3" fill="%s"/>' % (x_ + 8 * sg, y_ + 24, H_))
    # big crest: mandala fan behind Ganesh medallion
    o.append(mandala(d, 540, 180, 170, "#8A3A18", "#6B2A10", "#F6E2C4", gold=H_))
    o.append('<circle cx="540" cy="180" r="92" fill="#FFF3DF" stroke="%s" stroke-width="4"/>' % H_)
    o.append('<circle cx="540" cy="180" r="80" fill="none" stroke="%s" stroke-width="1.5" stroke-dasharray="3 6"/>' % H_)
    o.append(ganesh(d, 540, 196, 0.56, H_, "#FFF3DF", sw=6))
    # paisleys flanking crest
    for x_, fl in ((250, False), (830, True)):
        o.append(paisley(d, x_, 210, 1.15, -30 if not fl else 30, "#7A2E12", "#F6E2C4", "#E9C79E", flip=fl))
        o.append(henna_vine(d, 100 if not fl else 980, 70, 380 if not fl else 700, 90, H_, 50, 8))
    # parchment cartouche
    cart = ("M150,380 L930,380 C950,410 980,420 1000,420 L1000,1160 C980,1160 950,1170 930,1200 L150,1200 C130,1170 100,1160 80,1160 L80,420 C100,420 130,410 150,380Z")
    o.append('<path d="%s" fill="%s" filter="%s"/>' % (cart, d.rg([(0, "#FFF8EC"), (1, "#F6E4C8")], 0.5, 0.45, 0.8), d.shadow(0, 10, 16, "#3A1A08", .35)))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="3" transform="translate(540 790) scale(.975) translate(-540 -790)"/>' % (cart, H_))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.2" stroke-dasharray="2 6" stroke-linecap="round" transform="translate(540 790) scale(.955) translate(-540 -790)"/>' % (cart, H_))
    # bottom henna ornaments
    for x_, fl in ((150, False), (930, True)):
        o.append(paisley(d, x_, 1285, 0.62, 200 if not fl else 160, "#7A2E12", "#F6E2C4", "#E9C79E", flip=fl))
    o.append(henna_vine(d, 230, 1255, 330, 1250, H_, 10, 4) + henna_vine(d, 750, 1250, 850, 1255, H_, 10, 4))
    return d.svg("".join(o)), spec("E-inv-wedding-6", (150, 430, 930, 1150), "#6E2A0E", "#3A1A0C", "#8E3E14", "light", "deco", bg="#FCF0DE")


# ------------------------------------------------------------------ 7 plum: toran + kalash pair + rounded photo
def card7():
    d = Doc(17)
    o = [base_bg(d, "#3E1250", "#2A0B38", "#1A0624", buti_pattern(d, "#E9C46A", None, 80, 0.14, 0))]
    o.append('<ellipse cx="540" cy="320" rx="460" ry="300" fill="%s"/>' % d.rg([(0, "#D9A0FF", 0.3), (1, "#D9A0FF", 0)]))
    o.append(toran(d, -20, 1100, 10, 62, 13, bells=False))
    ph = {"shape": "rounded", "x": 385, "y": 150, "w": 310, "h": 300}
    pts = [(p[0], p[1]) for p in rrect_pts(ph["x"] - 30, ph["y"] - 30, ph["w"] + 60, ph["h"] + 60, 50, 400)]
    o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="50" fill="%s" filter="%s"/>' % (n(ph["x"] - 30), n(ph["y"] - 30), n(ph["w"] + 60), n(ph["h"] + 60), "#4A1760", d.shadow(0, 10, 16, "#000", .5)))
    o.append(flower_ring(d, path_pts(pts + [pts[0]], 23), 12.5, "marigold", ("orange", "yellow", "orange", "red"), 3, cx=540, cy=300))
    o.append(photo_slot(d, ph, "#FFF8EA", "#F1E2C8", "#C9A98A", ring_w=10, inner="#6E4A12"))
    for x_, fl in ((200, False), (880, True)):
        o.append('<ellipse cx="%d" cy="466" rx="90" ry="14" fill="#000" opacity=".35"/>' % x_)
        o.append(kalash(d, x_, 466, 1.0, cloth="#C8102E"))
    o.append(parchment(d, 88, 506, 904, 782, 30, "#FFF9F2", "#F2E6F2"))
    o.append(gold_frame_rect(d, 106, 524, 868, 746, 22, 4))
    for (x_, y_) in ((106, 897), (974, 897)):
        o.append('<path d="M%d,%d l14,-14 l14,14 l-14,14Z M%d,%d l14,-14 l14,14 l-14,14Z" fill="%s"/>' % (x_ - 14, y_, x_ - 14, y_, d.gold()))
    return d.svg("".join(o)), spec("E-inv-wedding-7", (150, 548, 930, 1248), "#5B1466", "#2E1633", "#7A4A0E", "light", "classic", photo=ph, bg="#FBF5F6")


# ------------------------------------------------------------------ 8 midnight palace arcade (dark)
def card8():
    d = Doc(18)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.lg([(0, "#080C26"), (0.55, "#161A48"), (0.8, "#35214F"), (1, "#1A1030")])]
    rr = random.Random(8)
    st = []
    for i in range(130):
        x_, y_ = rr.uniform(10, 1070), rr.uniform(10, 880)
        if 120 < x_ < 960 and 130 < y_ < 880:
            if rr.random() < 0.75:
                continue
        st.append('<circle cx="%s" cy="%s" r="%s" fill="#FFF6D8" opacity="%s"/>' % (n(x_), n(y_), n(rr.uniform(0.6, 2.2)), n(rr.uniform(0.25, 0.8))))
    o.append("".join(st))
    for (x_, y_, r_) in ((90, 120, 14), (1000, 200, 11), (70, 560, 9), (1010, 640, 12)):
        o.append(sparkle(x_, y_, r_, "#FFE7A8", .9))
    # gold lace fringe top
    lace = []
    for i in range(27):
        cx_ = 20 + i * 40
        lace.append('<path d="M%s,0 L%s,0 L%s,34 Q%s,56 %s,34Z" fill="%s"/>' % (n(cx_ - 20), n(cx_ + 20), n(cx_ + 14), n(cx_), n(cx_ - 14), d.gold()))
        lace.append('<circle cx="%s" cy="50" r="5" fill="%s"/><circle cx="%s" cy="22" r="5" fill="#161A48"/>' % (n(cx_), d.gold(), n(cx_)))
    o.append("".join(lace))
    # glow behind arcade
    o.append('<ellipse cx="540" cy="1100" rx="620" ry="240" fill="%s"/>' % d.rg([(0, "#FF9E4A", 0.45), (1, "#FF9E4A", 0)]))
    # arcade building
    wall = d.lg([(0, "#F1D3B5"), (1, "#C99F7E")])
    o.append('<rect x="0" y="950" width="1080" height="400" fill="%s"/>' % wall)
    o.append('<rect x="0" y="950" width="1080" height="400" fill="#1A1030" opacity=".35"/>')
    # parapet
    o.append('<rect x="0" y="934" width="1080" height="22" fill="%s"/>' % d.gold())
    for k in range(36):
        o.append('<path d="M%s,934 l0,-14 q15,-14 30,0 l0,14Z" fill="#D9B48E"/>' % n(k * 30))
    for cx_ in (84, 996):
        o.append(chhatri(d, cx_, 924, 120, d.lg([(0, "#FFE6B0"), (1, "#C8922E")], 0.2, 0, 0.8, 1, key="chd8"), d.gold(), "#F1D3B5"))
    # arches
    xs = [30 + i * 205 for i in range(6)]
    for i in range(5):
        x0 = xs[i] + 30
        w_ = 145
        arch = foil_arch_d(x0, 990, w_, 270, 0.42, 7)
        o.append('<path d="%s" fill="%s"/>' % (arch, d.lg([(0, "#FFE9A8"), (0.5, "#FFB356"), (1, "#E0762B")])))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="4"/>' % (arch, d.gold()))
        cx_ = x0 + w_ / 2
        o.append('<ellipse cx="%s" cy="1180" rx="60" ry="60" fill="#FFF3C4" opacity=".55" filter="%s"/>' % (n(cx_), d.blur(18)))
        for dx in (-38, 38):
            o.append(marigold_string(d, cx_ + dx, 1060, 1180, 9, ("orange", "yellow")))
        o.append(marigold_string(d, cx_, 1040, 1120, 9, ("red", "yellow")))
    for i in range(6):
        px = xs[i] + 15
        o.append('<rect x="%s" y="990" width="30" height="270" fill="%s"/>' % (n(px - 15 + 15), d.lg([(0, "#C99F7E"), (0.5, "#F6E0C6"), (1, "#A77E60")], 0, 0, 1, 0, key="col8")))
    o.append('<rect x="0" y="1260" width="1080" height="90" fill="%s"/>' % d.lg([(0, "#2A1838"), (1, "#120A1E")]))
    o.append('<rect x="0" y="1256" width="1080" height="6" fill="%s"/>' % d.gold())
    return d.svg("".join(o)), spec("E-inv-wedding-8", (150, 150, 930, 870), "gold", "#FFF3DC", "#F2C45A", "dark", "deco")


# ------------------------------------------------------------------ 9 haldi yellow + pink, oval photo at bottom
def card9():
    d = Doc(19)
    o = [base_bg(d, "#FFD84D", "#FDB426", "#F28A12", buti_pattern(d, "#D6246E", None, 64, 0.22, 0))]
    # panel
    o.append(parchment(d, 64, 56, 952, 804, 36, "#FFFAF0", "#FDEBD8"))
    o.append('<rect x="80" y="72" width="920" height="772" rx="28" fill="none" stroke="#D6246E" stroke-width="5"/>')
    o.append(gota_border(d, 96, 88, 888, 740, "#E0A21E", 18))
    for (x_, y_, r_) in ((96, 88, 0), (984, 88, 90), (984, 828, 180), (96, 828, 270)):
        o.append(g(mandala(d, 0, 0, 30, "#D6246E", "#9E1450", "#FFF3D6", detail=0), x_, y_, 1, r_))
    # oval slot with marigold wreath
    ph = {"shape": "oval", "x": 395, "y": 900, "w": 290, "h": 330}
    cx_, cy_ = 540, 1065
    o.append('<ellipse cx="%d" cy="%d" rx="190" ry="210" fill="%s"/>' % (cx_, cy_, d.rg([(0, "#FFF3C4", .7), (1, "#FFF3C4", 0)])))
    ring = [(p[0], p[1], p[2]) for p in ellipse_pts(cx_, cy_, 170, 190, 44)]
    o.append(flower_ring(d, ring, 15, "marigold", ("orange", "red", "yellow"), 2, cx=cx_, cy=cy_))
    o.append(photo_slot(d, ph, "#FFF8EA", "#FBE3C8", "#D9A98A", ring_w=10, ring=d.lg([(0, "#E23A7E"), (1, "#9E1450")]), inner="#7A0E3A"))
    o.append(elephant(d, 36, 1258, 0.62, cloth=("#D6246E", "#8E0E46"), seed=2))
    o.append(elephant(d, 752, 1258, 0.62, flip=True, cloth=("#D6246E", "#8E0E46"), seed=6))
    o.append('<rect x="0" y="1262" width="1080" height="88" fill="%s"/>' % d.lg([(0, "#C2410C"), (1, "#8A2A06")]))
    o.append('<rect x="0" y="1258" width="1080" height="7" fill="%s"/>' % d.gold())
    return d.svg("".join(o)), spec("E-inv-wedding-9", (150, 118, 930, 818), "#A3124F", "#3A1A1E", "#8A4B00", "light", "deco", photo=ph, bg="#FEF4E6")


# ------------------------------------------------------------------ 10 ivory line-art mandap with photo
def card10():
    d = Doc(20)
    o = ['<rect width="1080" height="1350" fill="%s"/>' % d.rg([(0, "#FFFDF8"), (1, "#F4E9DA")], 0.5, 0.35, 0.9)]
    o.append('<rect width="1080" height="1350" fill="%s"/>' % damask_pattern(d, "#D8C3A5", None, 110, 0.35))
    o.append('<rect x="18" y="18" width="1044" height="1314" fill="none" stroke="%s" stroke-width="3"/>' % d.gold())
    # blush floral corner clusters
    rr = random.Random(10)
    for (cx_, cy_, sg) in ((20, 20, 1), (1060, 20, -1)):
        cl = []
        for k in range(12):
            a = math.radians(rr.uniform(0, 90))
            rad = rr.uniform(10, 130)
            cl.append(leaf(d, cx_ + sg * rad * math.cos(a), cy_ + rad * math.sin(a), rr.uniform(34, 56), 13, rr.uniform(0, 360), "#8FB08A", "#4E7A52"))
        for k, (dx, dy, r_) in enumerate([(40, 40, 38), (100, 26, 26), (26, 104, 28), (84, 86, 20), (150, 18, 16), (20, 160, 18)]):
            cl.append(bloom(d, cx_ + sg * dx, cy_ + dy, r_, ["blush", "peach", "white"][k % 3], k * 40))
        o.append("".join(cl))
    # trailing rose vines along both edges
    for x_ in (62, 1018):
        o.append('<path d="M%d,150 C%d,400 %d,700 %d,1250" stroke="#6E8F6A" stroke-width="3" fill="none"/>' % (x_, x_ + 30, x_ - 30, x_))
        for k in range(16):
            yy = 190 + k * 66
            xx = x_ + 22 * math.sin(k * 1.3)
            o.append(leaf(d, xx, yy, 34, 11, (60 if k % 2 else -60) + (180 if x_ > 500 else 0), "#8FB08A", "#4E7A52"))
            if k % 3 == 1:
                o.append(bloom(d, xx, yy + 20, 17, ["blush", "peach", "white"][k % 3], k * 30))
            elif k % 3 == 2:
                o.append(jasmine(d, xx + 8, yy + 14, 8))
    # line-art mandap framing the photo (wide)
    gf = d.gold()
    ph = {"shape": "rect", "x": 320, "y": 952, "w": 440, "h": 268}
    XL, XR = 262, 818
    o.append('<rect x="190" y="1244" width="700" height="14" fill="%s"/><rect x="220" y="1230" width="640" height="14" fill="%s"/>' % (gf, d.lg([(0, "#E8D2B0"), (1, "#C9A56A")])))
    for x_ in (XL, XR):
        o.append('<rect x="%d" y="930" width="18" height="302" fill="%s"/>' % (x_ - 9, gf))
        o.append('<rect x="%d" y="1200" width="40" height="30" fill="%s"/><rect x="%d" y="930" width="40" height="18" fill="%s"/>' % (x_ - 20, gf, x_ - 20, gf))
        for k in range(7):
            o.append('<circle cx="%d" cy="%d" r="3" fill="#FFF8EA"/>' % (x_, 966 + k * 36))
    can = []
    can.append('<path d="M%d,860 L%d,860 L%d,832 L%d,832Z" fill="%s"/>' % (XL - 60, XR + 60, XR + 36, XL - 36, gf))
    can.append('<path d="M%d,832 C%d,780 420,770 540,736 C660,770 %d,780 %d,832" fill="none" stroke="%s" stroke-width="6"/>' % (XL + 20, XL + 30, XR - 30, XR - 20, gf))
    can.append('<path d="M%d,832 C%d,794 440,786 540,762 C640,786 %d,794 %d,832" fill="none" stroke="%s" stroke-width="2.5"/>' % (XL + 70, XL + 80, XR - 80, XR - 70, gf))
    can.append('<path d="M540,736 L540,712" stroke="%s" stroke-width="4"/><circle cx="540" cy="706" r="8" fill="%s"/>' % (gf, gf))
    for x_ in (XL - 10, XR + 10):
        can.append(dome(d, x_, 832, 64, 40, gf, gf))
    can.append('<path d="%s" fill="none" stroke="%s" stroke-width="3"/>' % (" ".join("M%s,860 Q%s,884 %s,860" % (n(XL - 40 + i * 42), n(XL - 19 + i * 42), n(XL + 2 + i * 42)) for i in range(15)), gf))
    can.append(rose_swag(d, XL + 10, 872, 540, 872, 40, 11, ("blush", "peach"), jas=True))
    can.append(rose_swag(d, 540, 872, XR - 10, 872, 40, 11, ("peach", "blush"), jas=True))
    can.append(bloom(d, 540, 880, 22, "blush") + bloom(d, XL, 872, 20, "peach") + bloom(d, XR, 872, 20, "peach"))
    o.append(g("".join(can), 0, 70))
    for x_ in (XL - 26, XR + 26):
        o.append(rose_swag(d, x_, 972, x_, 1200, 0, 10, ("blush", "white"), jas=True))
    o.append(photo_slot(d, ph, "#FFFBF4", "#F2E3D0", "#D9C0A4", ring_w=10, inner="#9A7A4A"))
    # flower clusters at base
    for (x_, sg) in ((XL - 50, 1), (XR + 50, -1)):
        o.append(bloom(d, x_, 1228, 26, "blush") + bloom(d, x_ + sg * 30, 1238, 18, "peach") + leaf(d, x_ - sg * 26, 1238, 40, 12, -60 * sg, "#8FB08A", "#4E7A52"))
    return d.svg("".join(o)), spec("E-inv-wedding-10", (150, 64, 930, 764), "#7A4A12", "#3A2A20", "#85561A", "light", "script", photo=ph, bg="#FBF5EC")


CARDS = [card1, card2, card3, card4, card5, card6, card7, card8, card9, card10]

if __name__ == "__main__":
    only = [int(a) for a in sys.argv[1:]]
    arts, specs = {}, []
    for i, fn in enumerate(CARDS, 1):
        svg, sp = fn()
        specs.append(sp)
        if not only or i in only:
            arts[sp["id"]] = svg
    render_cards(arts)
    write_specs(CAT, specs)
