"""Event-specific card templates (10 per page). Each design is hand-composed for its event.
Run: python3 tools/templates2.py [cat,cat]   -> static/cards/T-<cat>-<n>.webp + content/templates.json"""
import json, os, sys, asyncio
sys.path.insert(0, os.path.dirname(__file__))
from art import *  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "static", "cards")


def L(title, text, accent):
    return {"title": title, "text": text, "accent": accent}


DK = {"title": "gold", "text": "#FFF8EC", "accent": "#FFD36B"}


def S(zone, colors, tone="light", title="deco", photo=None, align="center", slot=False):
    d = dict(zone=zone, colors=colors, tone=tone, title=title, align=align, tpl=True)
    if photo:
        d["photo"] = photo
    if slot:
        d["slot"] = True
    return d


def circ(x, y, r): return dict(shape="circle", x=x, y=y, r=r)
def rct(x, y, w, h, shape="rounded"): return dict(shape=shape, x=x, y=y, w=w, h=h)


def frame_line(inset, color, w=3, rx=0):
    return f'<rect x="{inset}" y="{inset}" width="{W - 2 * inset}" height="{H - 2 * inset}" rx="{rx}" fill="none" stroke="{color}" stroke-width="{w}"/>'


def paper(c="#FFF8EE"):
    return rect_bg(c) + texture(1)


# ======================================================================== SHRADDHANJALI (sober only)
def tribute():
    D = []
    ink, grey, gold = "#2F2F35", "#6B6B73", "#9C7A3C"
    # 1 white, rect photo + white garland, lilies
    D.append(([paper("#FBFAF7"), frame_line(40, "#CFC8BA", 2), garland_frame(340, 150, 400, 470, "rect", "#FFFFFF", "#F4E3B5"),
               f'<rect x="340" y="150" width="400" height="470" fill="#ECE7DE"/>', lily(120, 1290, 1.1, -25), lily(960, 1290, 1.1, 25)],
              S([150, 760, 930, 1250], L(ink, ink, gold), photo=rct(340, 150, 400, 470, "rect"), slot=True, title="classic")))
    # 2 cream, oval photo + marigold/white garland, diya below
    D.append(([paper("#FFF7EA"), double_frame("#C9A66B", 44, 16, 3, 1.5, False),
               f'<ellipse cx="540" cy="380" rx="190" ry="235" fill="#EFE6D6"/>', garland_frame(350, 145, 380, 470, "oval", "#FFFFFF", "#F2A541"),
               diya(540, 730, .55)],
              S([150, 790, 930, 1260], L("#6B2C1F", ink, "#8B5A2B"), photo=rct(350, 145, 380, 470, "oval"), slot=True, title="classic")))
    # 3 charcoal dark, circle photo gold ring, lotus bottom
    D.append(([radial_bg("#3A3A40", "#141418"), f'<circle cx="540" cy="360" r="215" fill="none" stroke="url(#gold)" stroke-width="6"/>',
               f'<circle cx="540" cy="360" r="200" fill="#2A2A2F"/>', lotus(540, 1265, .9, "#F4F1EA", "#D9D2C5", "#5F6B5F")],
              S([150, 610, 930, 1180], DK, tone="dark", photo=circ(540, 360, 200), slot=True, title="classic")))
    # 4 soft grey, hanging diya top, arch photo, candles
    D.append(([grad_bg("#F1F1F3", "#DADADF"), hanging_diya(540, 170, .7, "#9CA3AF"),
               f'<path d="{arch_path(360, 230, 360, 440)}" fill="#E4E4E8" stroke="#A7A9B0" stroke-width="6"/>',
               candle(150, 1230, .8), candle(930, 1230, .8)],
              S([150, 720, 930, 1200], L(ink, ink, grey), photo=rct(372, 242, 336, 416, "arch"), slot=True, title="classic")))
    # 5 sage, eucalyptus sprigs, rounded photo
    D.append(([paper("#F2F5EF")] + [leaf(x, y, 90, a, "#8FA58A", .8) for x, y, a in [(60, 140, -20), (110, 90, 20), (60, 240, 10), (1020, 1210, 160), (970, 1260, 200), (1020, 1110, 170)]] +
              [f'<rect x="330" y="150" width="420" height="460" rx="40" fill="#DDE5D8"/>'],
              S([150, 700, 930, 1230], L("#3F5E47", ink, "#6B8F71"), photo=rct(330, 150, 420, 460), slot=True, title="classic")))
    # 6 navy + muted gold frame, oval photo with leaf wreath
    wreath = "".join(leaf(540 + math.cos(math.radians(a)) * 230, 380 + math.sin(math.radians(a)) * 270, 50, a + 90, "#B8962E", .9) for a in range(0, 360, 15))
    D.append(([radial_bg("#23325A", "#0E1630"), frame_line(50, "#B8962E", 2, 24), wreath, f'<ellipse cx="540" cy="380" rx="190" ry="232" fill="#1B2748"/>'],
              S([150, 700, 930, 1240], DK, tone="dark", photo=rct(350, 148, 380, 464, "oval"), slot=True, title="classic")))
    # 7 off-white + mandala watermark grey, circle photo
    D.append(([paper("#F8F7F4"), mandala(540, 380, 330, "#B9B6AE", .35, None, 2), f'<circle cx="540" cy="380" r="190" fill="#ECEAE5" stroke="#B9B6AE" stroke-width="4"/>'],
              S([150, 650, 930, 1230], L(ink, ink, grey), photo=circ(540, 380, 190), slot=True, title="classic")))
    # 8 beige, incense smoke + three small diyas bottom, rect photo
    smoke = "".join(f'<path d="M{x} 1200 C {x - 30} 1120, {x + 30} 1060, {x} 980 C {x - 30} 920, {x + 20} 860, {x} 800" stroke="#B9AFA0" stroke-width="4" fill="none" opacity=".45"/>' for x in (180, 900))
    D.append(([paper("#F6F0E6"), smoke, f'<rect x="170" y="1195" width="20" height="60" fill="#8B5A2B"/><rect x="890" y="1195" width="20" height="60" fill="#8B5A2B"/>',
               diya_row(1270, 3, .5, 420, 660), f'<rect x="330" y="140" width="420" height="480" fill="#E7DDCC" stroke="#C9B79C" stroke-width="10"/>'],
              S([150, 680, 930, 1190], L("#5C4A32", ink, "#8B5A2B"), photo=rct(330, 140, 420, 480, "rect"), slot=True, title="classic")))
    # 9 black & white minimal, big square photo top
    D.append(([rect_bg("#FFFFFF"), f'<rect x="0" y="0" width="{W}" height="640" fill="#E9E9E9"/>', f'<rect x="80" y="690" width="920" height="2" fill="#1F1F1F"/>'],
              S([120, 720, 960, 1250], L("#111111", "#2B2B2B", "#555555"), photo=rct(0, 0, W, 640, "rect"), slot=True, title="classic")))
    # 10 cream + maroon Indian style, rajnigandha strings sides, photo with garland
    strings = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#E8E2D2" stroke-width="3"/>' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="14" fill="#FFFFFF" stroke="#E0D8C4"/>' for y in range(20, H, 42)) for x in (70, 1010))
    D.append(([paper("#FFF8F0"), f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#7B1E1E" stroke-width="18"/>', strings,
               garland_frame(355, 150, 370, 440, "rect", "#FFFFFF", "#F4D35E"), f'<rect x="355" y="150" width="370" height="440" fill="#EFE6DA"/>'],
              S([150, 740, 930, 1250], L("#7B1E1E", ink, "#7B1E1E"), photo=rct(355, 150, 370, 440, "rect"), slot=True, title="classic")))
    return D


# ======================================================================== DIWALI
def diwali():
    D = []
    NIGHT, PURP, MAR = ("#14224A", "#0B1430"), ("#3D1A5B", "#1C0A2E"), ("#6D0F24", "#2E0510")
    D.append(([radial_bg(*NIGHT), "".join(akash_kandil(x, y, s, "#FF8C00", "#FFD166") for x, y, s in [(170, 260, .9), (390, 170, .7), (690, 170, .7), (910, 260, .9)]),
               diya_row(1250, 6, .7), sparkles(20, "#FFE08A", 3, (80, 380, 1000, 1100))],
              S([140, 400, 940, 1120], DK, tone="dark", title="deco", photo=circ(540, 470, 100))))
    D.append(([radial_bg(*PURP), rangoli(540, 1350, 420, ["#FF8C00", "#F72585", "#FFD166", "#4CC9F0"]), fireworks(200, 200, 150, "#FFD166", 20, 1), fireworks(880, 260, 120, "#F72585", 18, 2)],
              S([140, 380, 940, 980], DK, tone="dark", title="script", photo=circ(540, 360, 100))))
    D.append(([paper("#FFF6E5"), rangoli(540, 330, 230, ["#E85D04", "#9D0208", "#FFBA08", "#2D6A4F"]), diya(540, 330, .7), toran(0, ("#FF9F1C", "#F77F00", "#FFD166"), "#2D6A4F", 0)[:0],
               diya_row(1260, 5, .6, 180, 900)],
              S([140, 590, 940, 1180], L("#9D0208", "#3A2330", "#B7791F"), title="deco")))
    D.append(([radial_bg(*MAR), frame_line(46, "url(#gold)", 4, 20), frame_line(64, "url(#gold)", 1.5, 14), corner_mandalas("#FFD36B", 160, .35),
               coins(160, 1210, .8), coins(880, 1210, .8), diya(540, 1210, .8)],
              S([150, 250, 930, 1080], DK, tone="dark", title="deco", photo=circ(540, 330, 105))))
    D.append(([grad_bg("#FFE8CC", "#FFC9A3"), f'<path d="{arch_path(150, 170, 780, 1050)}" fill="#FFF8EC" stroke="url(#gold)" stroke-width="10"/>',
               "".join(lantern(x, y, 0, "#E85D04", "#B7791F", .9) for x, y in [(75, 330), (1005, 330)]), diya_row(1270, 7, .5)],
              S([220, 380, 860, 1150], L("#9D0208", "#3A2330", "#B7791F"), title="classic", photo=circ(540, 330, 100))))
    D.append(([rect_bg("#0E0A1F"), fireworks(540, 250, 230, "#FFD166", 26, 3), fireworks(170, 420, 120, "#4CC9F0", 18, 4), fireworks(900, 460, 130, "#F72585", 18, 5),
               f'<path d="M0 1150 L{W} 1150 L{W} {H} L0 {H} Z" fill="#1C1433"/>', diya_row(1180, 8, .45)],
              S([140, 560, 940, 1120], DK, tone="dark", title="deco")))
    D.append(([paper("#FFFBF2"), f'<rect width="320" height="{H}" fill="#6D0F24"/>', "".join(akash_kandil(160, y, .7, "#FFD166", "#E85D04") for y in (240, 620, 1000)),
               f'<line x1="350" y1="80" x2="350" y2="{H - 80}" stroke="#C9973B" stroke-width="3"/>', diya(840, 1210, .8)],
              S([390, 260, 1010, 1100], L("#6D0F24", "#3A2330", "#B7791F"), title="classic", align="left", photo=rct(390, 90, 180, 180))))
    D.append(([radial_bg("#2B0A3D", "#12031C"), rangoli(540, 620, 470, ["#6A1B9A", "#8E24AA", "#AB47BC", "#FFD166"], .28), sparkles(18, "#FFE08A", 7),
               "".join(hanging_diya(x, y, .6) for x, y in [(200, 260), (880, 260)])],
              S([150, 360, 930, 1180], DK, tone="dark", title="script", photo=circ(540, 400, 100))))
    D.append(([grad_bg("#FDF0D5", "#F6C28B"), rangoli(0, 0, 330, ["#C1121F", "#FF8C00", "#FFD166", "#2D6A4F"]), rangoli(W, H, 330, ["#C1121F", "#FF8C00", "#FFD166", "#2D6A4F"]),
               diya(880, 260, .8), diya(200, 1110, .8)],
              S([160, 360, 920, 1060], L("#9D0208", "#3A2330", "#B7791F"), title="deco", photo=circ(540, 330, 100))))
    D.append(([radial_bg("#10243E", "#050B16"), f'<rect x="300" y="110" width="480" height="560" rx="30" fill="#1E3350" stroke="url(#gold)" stroke-width="8"/>',
               "".join(akash_kandil(x, 110, .45, "#FF8C00", "#FFD166") for x in (160, 920)), diya_row(1260, 5, .55, 220, 860)],
              S([150, 720, 930, 1200], DK, tone="dark", title="deco", photo=rct(300, 110, 480, 560), slot=True)))
    return D


# ======================================================================== KARVA CHAUTH
def karva():
    D = []
    NIGHT = ("#1D2A55", "#070B1E")
    stars = lambda seed: "".join(star(x, y, r, "#FFE9A8", .9) for x, y, r in [(150, 180, 10), (330, 90, 7), (720, 120, 8), (960, 220, 11), (260, 330, 6), (840, 380, 7)])
    D.append(([radial_bg(*NIGHT), stars(1), moon(780, 280, 150, "#FFF3C4"), sieve(300, 330, .9), karwa(160, 1180, .9), thali(820, 1230, .8)],
              S([140, 560, 940, 1080], DK, tone="dark", title="script")))
    D.append(([grad_bg("#8B1E3F", "#3C0919"), mehendi_border(60, "#F4C27A"), mehendi_border(H - 60, "#F4C27A", True), moon(540, 300, 120, "#FFF3C4")],
              S([150, 480, 930, 1160], DK, tone="dark", title="deco", photo=circ(540, 300, 120), slot=False)))
    D.append(([paper("#FFF4EE"), moon(540, 230, 110, "#FFE8B0"), sieve(540, 230, .95).replace('fill="#8B1E3F"', 'fill="#8B1E3F" fill-opacity=".25"'), mehendi_border(H - 50, "#C75B12", True),
               bangles(120, 1110, .8), bangles(960, 1110, .8)],
              S([150, 420, 930, 1040], L("#8B1E3F", "#3A2330", "#C75B12"), title="script")))
    D.append(([radial_bg("#3A0F2E", "#12030D"), moon(820, 230, 110, "#FFF3C4"), stars(2), f'<path d="{heart_frame_path(240, 260, 600, 560)}" fill="#2A0A20" stroke="url(#gold)" stroke-width="10"/>'],
              S([150, 860, 930, 1260], DK, tone="dark", title="script", photo=rct(310, 330, 460, 440, "heart"), slot=True)))
    D.append(([paper("#FFF8E7"), f'<rect width="{W}" height="480" fill="#B3001B"/>', moon(540, 230, 120, "#FFF3C4"), scallop_edge(480, "#FFF8E7", 24, 16, True), karwa(540, 1190, .8)],
              S([130, 560, 950, 1080], L("#B3001B", "#3A2330", "#C9973B"), title="deco")))
    D.append(([radial_bg(*NIGHT), moon(540, 520, 330, "#FFF6D5"), stars(3), f'<path d="M0 1120 C 300 1040, 700 1180, {W} 1080 L{W} {H} L0 {H}Z" fill="#0B1024"/>', diya_row(1210, 5, .5, 200, 880)],
              S([180, 330, 900, 760], L("#6D0F1A", "#3A2330", "#8B5A2B"), title="script")))
    D.append(([paper("#FDF2F4"), f'<rect width="300" height="{H}" fill="#6D0F1A"/>', "".join(paisley(150, y, .8, 0, "#F4C27A") for y in (180, 520, 860, 1200)),
               moon(860, 200, 90, "#FFE8B0"), sieve(880, 1180, .6)],
              S([370, 330, 1010, 1080], L("#6D0F1A", "#3A2330", "#C75B12"), title="classic", align="left", photo=rct(370, 110, 190, 190))))
    D.append(([grad_bg("#2B1A4A", "#0E0820"), moon(540, 230, 130, "#FFF3C4"), thali(540, 1200, 1.1), stars(4)],
              S([150, 420, 930, 1060], DK, tone="dark", title="deco", photo=circ(540, 230, 125))))
    D.append(([paper("#FFF7F0"), mehendi_border(50, "#B3001B"), f'<circle cx="540" cy="430" r="250" fill="#FDE3E3" stroke="#B3001B" stroke-width="6"/>',
               moon(620, 360, 70, "#FFE8B0"), karwa(470, 500, .75)],
              S([150, 720, 930, 1260], L("#B3001B", "#3A2330", "#C9973B"), title="script")))
    D.append(([radial_bg("#3C0919", "#12020A"), frame_line(50, "url(#gold)", 4, 26), moon(540, 1180, 200, "#FFF3C4"),
               "".join(bangles(x, 190, .6, ("#FFD166", "#C1121F", "#FFFFFF")) for x in (220, 860))],
              S([150, 330, 930, 940], DK, tone="dark", title="deco", photo=circ(540, 300, 100))))
    return D


# ======================================================================== NAVRATRI
def navratri():
    D = []
    rainbow = ["#FF7A00", "#FFFFFF", "#C1121F", "#1E3A8A", "#F4C430", "#2E7D32", "#8D99AE", "#6A1B9A", "#0F7C7A"]
    D.append(([radial_bg("#C1121F", "#5E0612"), dancers(1290, "#2B0306", 6), dandiya(170, 230, .7, -30), dandiya(910, 230, .7, 30), sparkles(14, "#FFD166", 2)],
              S([150, 380, 930, 1030], DK, tone="dark", title="deco", photo=circ(540, 350, 100))))
    D.append(([paper("#FFF6E5"), "".join(f'<rect x="{i * W / 9:.1f}" y="0" width="{W / 9 + 1:.1f}" height="70" fill="{c}"/>' for i, c in enumerate(rainbow)),
               "".join(f'<rect x="{i * W / 9:.1f}" y="{H - 70}" width="{W / 9 + 1:.1f}" height="70" fill="{c}"/>' for i, c in enumerate(rainbow)), garbo(540, 300, .9)],
              S([140, 520, 940, 1200], L("#C1121F", "#3A2330", "#6A1B9A"), title="deco")))
    D.append(([grad_bg("#6A1B9A", "#2D0A45"), mandala(540, 620, 520, "#FFD166", .18), "".join(dandiya(x, 1150, .55, a, "#FF7A00", "#FFD166") for x, a in [(160, -25), (300, 25), (780, -25), (920, 25)])],
              S([150, 280, 930, 980], DK, tone="dark", title="script", photo=circ(540, 300, 100))))
    bandhani = "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#FFFFFF" opacity=".7"/>' for x in range(20, W, 40) for y in range(20, 330, 40))
    D.append(([paper("#FFF8EE"), f'<rect width="{W}" height="330" fill="#D81B60"/>', bandhani, garbo(540, 330, .8), mehendi_border(H - 50, "#D81B60", True)],
              S([140, 520, 940, 1200], L("#D81B60", "#3A2330", "#E0A800"), title="deco")))
    mirror = "".join(f'<circle cx="{x}" cy="{y}" r="16" fill="#E8EEF2" stroke="#E0A800" stroke-width="5"/>' for x, y in [(100, 100), (980, 100), (100, 1250), (980, 1250), (540, 70), (540, 1280), (70, 675), (1010, 675)])
    D.append(([radial_bg("#0F7C7A", "#073D3C"), frame_line(40, "#E0A800", 6, 30), mirror, dancers(1200, "#063534", 5)],
              S([150, 250, 930, 960], DK, tone="dark", title="deco", photo=circ(540, 300, 100))))
    D.append(([grad_bg("#FF7A00", "#C1121F"), f'<path d="{arch_path(160, 200, 760, 1030)}" fill="#FFF3DC" stroke="url(#gold)" stroke-width="10"/>',
               toran(0, ("#FFD166", "#F77F00", "#FFD166"), "#2E7D32", 0), garbo(540, 1100, .6)],
              S([230, 400, 850, 960], L("#C1121F", "#3A2330", "#6A1B9A"), title="classic", photo=circ(540, 360, 95))))
    D.append(([paper("#FFFBF2"), f'<rect width="300" height="{H}" fill="#1E3A8A"/>', "".join(dandiya(150, y, .45, 90, "#FFD166", "#D81B60") for y in (200, 480, 760, 1040)),
               peacock_feather(900, 1150, 1.2, 20)],
              S([370, 300, 1010, 1080], L("#1E3A8A", "#3A2330", "#D81B60"), title="classic", align="left", photo=rct(370, 90, 180, 180))))
    D.append(([radial_bg("#3A0A0A", "#120202"), rangoli(540, 1350, 460, ["#C1121F", "#FF7A00", "#FFD166", "#2E7D32"]), sparkles(16, "#FFD166", 5, (80, 80, 1000, 800)),
               dandiya(240, 200, .6, -35, "#C1121F", "#FFD166"), dandiya(840, 200, .6, 35, "#C1121F", "#FFD166")],
              S([150, 300, 930, 880], DK, tone="dark", title="script")))
    D.append(([paper("#FDF5FF"), peacock_feather(120, 320, 1.1, -30), peacock_feather(960, 1080, 1.1, 150), f'<circle cx="540" cy="675" r="360" fill="none" stroke="#6A1B9A" stroke-width="3" stroke-dasharray="4 10"/>'],
              S([220, 380, 860, 980], L("#6A1B9A", "#3A2330", "#0F7C7A"), title="script", photo=circ(540, 360, 95))))
    D.append(([grad_bg("#F4C430", "#E07A00"), mandala(540, 400, 280, "#FFFFFF", .35), f'<rect x="120" y="760" width="840" height="470" rx="30" fill="#FFF8E7" opacity=".95"/>', garbo(540, 400, .75)],
              S([160, 790, 920, 1200], L("#C1121F", "#3A2330", "#6A1B9A"), title="deco")))
    return D


# ======================================================================== DUSSEHRA
def dussehra():
    D = []
    D.append(([radial_bg("#FF7A00", "#8C1C00"), bow_arrow(820, 1050, .9), flaming_arrow(420, 1180, .9, -12), sparkles(14, "#FFE08A", 2)],
              S([130, 230, 900, 860], DK, tone="dark", title="deco", align="left")))
    D.append(([paper("#FFF1D0"), toran(0, ("#FF9F1C", "#F77F00", "#FFD166"), "#2D6A4F", 7), "".join(apta_leaf(x, 1210, .9, a) for x, a in [(150, -20), (280, 10), (800, -10), (930, 20)])],
              S([140, 380, 940, 1100], L("#8C1C00", "#3A2330", "#B7791F"), title="deco", photo=circ(540, 340, 100))))
    D.append(([radial_bg("#1A1A1A", "#000000"), flaming_arrow(540, 300, 1.2, -8), fireworks(200, 1100, 140, "#FF7A00", 18, 3), fireworks(880, 1120, 140, "#F2B705", 18, 4)],
              S([150, 480, 930, 1000], DK, tone="dark", title="deco")))
    D.append(([paper("#FFF8EE"), double_frame("#C9973B"), mandala(540, 280, 170, "#C9973B", .6, "#FDE8C8"), bow_arrow(540, 280, .35)],
              S([150, 500, 930, 1220], L("#8C1C00", "#3A2330", "#B7791F"), title="classic")))
    D.append(([grad_bg("#FF9F1C", "#F77F00"), f'<circle cx="540" cy="700" r="430" fill="#FFF3DC" stroke="url(#gold)" stroke-width="10"/>', "".join(apta_leaf(x, y, .7, a) for x, y, a in [(110, 150, -30), (970, 150, 30), (110, 1230, -150), (970, 1230, 150)])],
              S([200, 420, 880, 1000], L("#8C1C00", "#3A2330", "#9D0208"), title="deco", photo=circ(540, 370, 90))))
    D.append(([radial_bg("#6A1B1A", "#2A0606"), frame_line(50, "url(#gold)", 4), "".join(marigold(x, y, 20) for x in range(80, W, 70) for y in (80, H - 80)), bow_arrow(540, 1080, .5)],
              S([150, 200, 930, 880], DK, tone="dark", title="script", photo=circ(540, 260, 100))))
    D.append(([paper("#FFFBF2"), f'<rect width="{W}" height="520" fill="#C62828"/>', flaming_arrow(540, 260, 1, -8), scallop_edge(520, "#FFFBF2", 26, 16, True)],
              S([130, 600, 950, 1250], L("#C62828", "#3A2330", "#B7791F"), title="deco")))
    D.append(([grad_bg("#14213D", "#0B132B"), "".join(marigold(x, 40 + (i % 2) * 20, 22) for i, x in enumerate(range(40, W, 60))), fireworks(540, 1150, 200, "#F2B705", 24, 6)],
              S([150, 250, 930, 900], DK, tone="dark", title="classic", photo=circ(540, 290, 100))))
    D.append(([paper("#FFF6E5"), f'<rect width="300" height="{H}" fill="#F77F00"/>', "".join(apta_leaf(150, y, .8, 0, "#2D6A4F") for y in (220, 560, 900, 1240)), bow_arrow(860, 1150, .45)],
              S([370, 280, 1010, 1060], L("#8C1C00", "#3A2330", "#2D6A4F"), title="classic", align="left", photo=rct(370, 80, 180, 180))))
    D.append(([radial_bg("#F2B705", "#C75B12"), mandala(540, 675, 520, "#FFFFFF", .22), f'<rect x="130" y="330" width="820" height="700" rx="40" fill="#FFFBF0" opacity=".96"/>', flaming_arrow(540, 200, .8, 0)],
              S([170, 370, 910, 1000], L("#8C1C00", "#3A2330", "#C62828"), title="deco")))
    return D


# ======================================================================== invitations and occasions
def wedding_inv():
    D = []
    D.append(([grad_bg("#7A0F2E", "#3D0715"), f'<path d="{arch_path(150, 150, 780, 1090)}" fill="#FFF8EE" stroke="url(#gold)" stroke-width="10"/>', "".join(bell(x, 260, .8) for x in (75, 1005)),
               kalash(540, 380, .55), floral_cluster(-30, H + 30, 1.4, dict(flower1="#C9184A", flower2="#FF9F1C", leaf="#2D6A4F", dot="#F2C14E"), 1, "roses", False, 2, -1),
               floral_cluster(W + 30, H + 30, 1.4, dict(flower1="#C9184A", flower2="#FF9F1C", leaf="#2D6A4F", dot="#F2C14E"), -1, "roses", False, 3, -1)],
              S([230, 440, 850, 1160], L("#7A0F2E", "#3A2330", "#B7791F"), title="deco")))
    D.append(([paper("#FFF8EE"), mandap(540, 600, 1.0), toran(0, ("#FF9F1C", "#F77F00", "#FFD166"), "#2D6A4F", 0)],
              S([140, 680, 940, 1260], L("#8B1030", "#3A2330", "#B7791F"), title="deco")))
    D.append(([radial_bg("#0F3D2E", "#04160F"), frame_line(50, "url(#gold)", 5, 30), frame_line(72, "url(#gold)", 1.5, 22), peacock_feather(150, 1150, 1.1, -25), peacock_feather(930, 1150, 1.1, 25), kalash(540, 280, .5)],
              S([150, 380, 930, 1000], DK, tone="dark", title="deco")))
    D.append(([paper("#FFF6EC")] + [banana_leaf(x, H + 40, 1.1, a) for x, a in [(60, 15), (1020, -15)]] + [toran(0, ("#FF9F1C", "#F77F00", "#FFD166"), "#2D6A4F", 0), kalash(540, 1250, .7)],
              S([200, 300, 880, 1000], L("#8B1030", "#3A2330", "#2D6A4F"), title="classic")))
    D.append(([radial_bg("#1B2A4A", "#0B1428"), mandala(540, 675, 500, "#FFD36B", .16), f'<circle cx="540" cy="675" r="420" fill="#FFF8EE" stroke="url(#gold)" stroke-width="10"/>', "".join(bell(x, 140, .7) for x in (140, 940))],
              S([200, 350, 880, 1000], L("#1B2A4A", "#3A2330", "#B7892F"), title="classic")))
    D.append(([paper("#FFF4E6"), f'<rect width="{W}" height="500" fill="#C9184A"/>', mandap(540, 450, .55, drape="#7A0F2E"), scallop_edge(500, "#FFF4E6", 26, 16, True)],
              S([130, 580, 950, 1260], L("#7A0F2E", "#3A2330", "#B7791F"), title="deco")))
    D.append(([paper("#FFFDF7"), f'<rect width="300" height="{H}" fill="#7A0F2E"/>', "".join(marigold(150, y, 18) for y in range(40, H, 58)), f'<line x1="330" y1="80" x2="330" y2="{H - 80}" stroke="#C9973B" stroke-width="3"/>', kalash(860, 250, .45)],
              S([380, 380, 1010, 1240], L("#7A0F2E", "#3A2330", "#B7791F"), title="classic", align="left")))
    D.append(([grad_bg("#FDE2E4", "#F9C6CF"), floral_cluster(-40, -40, 2.2, dict(flower1="#E85D75", flower2="#FFFFFF", leaf="#6B8F71", dot="#F2C14E", center="#F2C14E"), 1, "flowers", True, 4),
               floral_cluster(W + 40, H + 40, 2.2, dict(flower1="#E85D75", flower2="#FFFFFF", leaf="#6B8F71", dot="#F2C14E", center="#F2C14E"), -1, "flowers", True, 5, -1)],
              S([170, 360, 910, 1060], L("#A4133C", "#3A2330", "#9C7A3C"), title="script")))
    D.append(([radial_bg("#5A0A1F", "#200309"), "".join(akash_kandil(x, y, .6, "#FFD166", "#C9184A") for x, y in [(160, 200), (920, 200)]), toran(0, ("#FFD166", "#F77F00", "#FFD166"), "#2D6A4F", 0)[:0],
               corner_mandalas("#FFD36B", 200, .3), diya_row(1260, 5, .5, 250, 830)],
              S([150, 300, 930, 1150], DK, tone="dark", title="script")))
    D.append(([paper("#FAF4EA"), f'<path d="{arch_path(290, 110, 500, 560)}" fill="#F3E3D3" stroke="url(#gold)" stroke-width="12"/>', mandap(540, 560, .45),
               floral_cluster(220, 560, 1, dict(flower1="#C9184A", flower2="#FF9F1C", leaf="#2D6A4F", dot="#F2C14E"), 1, "roses", False, 6),
               floral_cluster(860, 560, 1, dict(flower1="#C9184A", flower2="#FF9F1C", leaf="#2D6A4F", dot="#F2C14E"), -1, "roses", False, 7)],
              S([140, 720, 940, 1260], L("#7A0F2E", "#3A2330", "#B7791F"), title="classic", photo=rct(302, 122, 476, 536, "arch"), slot=True)))
    return D


COUPLE_MAPS = {
    # replace the base (engagement) colours per page so each page has its own look
    "eng": {},
    "inv-eng": {"#FFF7F8": "#F7F5EE", "#F6E1E6": "#E3EBDD", "#E7A4B2": "#A8B89A", "#A23E5B": "#3F5E47", "#3A0A1E": "#1F2A44", "#12030A": "#0B1224", "#2A0A18": "#16203A", "#FFF5F7": "#F7F5EE", "#F9E0E6": "#E8EFE3", "#F1C5D0": "#CFDCC6", "#5A0A2A": "#26324F", "#1E0312": "#0B1224", "#F6EEF7": "#EEF2EA", "#C9184A": "#C8A45D"},
    "anni": {"#FFF7F8": "#FFF5F5", "#F6E1E6": "#FFD9DE", "#E7A4B2": "#C9184A", "#A23E5B": "#800F2F", "#3A0A1E": "#4A0418", "#FFF5F7": "#FFF1F2", "#F9E0E6": "#FFCCD5", "#F1C5D0": "#FF9EB0", "#F6EEF7": "#FFF0F3"},
    "wed": {"#FFF7F8": "#FFF6EA", "#F6E1E6": "#F7E3C8", "#E7A4B2": "#C9973B", "#A23E5B": "#7A0F2E", "#3A0A1E": "#5A0A1F", "#12030A": "#200309", "#FFF5F7": "#FFF8EE", "#F9E0E6": "#F8E7CF", "#F1C5D0": "#EFCB94", "#5A0A2A": "#6D0F24", "#F6EEF7": "#FBF3E6"},
}


def couple_set(kind):
    """Engagement / anniversary / wedding-wish designs: big couple photo frames (arch, heart, rect, pill)."""
    D = []
    hero = rings if kind in ("eng", "inv-eng") else (lambda x, y, s: heart(x - 30 * s, y, 1.4 * s, "#C9184A") + heart(x + 30 * s, y - 16 * s, 1.1 * s, "#FFB3C1", .9)) if kind == "anni" else (lambda x, y, s: kalash(x, y + 60 * s, .45 * s))
    P = dict(flower1="#E7A4B2", flower2="#FFFFFF", leaf="#8FB996", dot="#C8A45D", center="#F2C14E", dark="#A23E5B")
    ROSE = dict(flower1="#C9184A", flower2="#FFB3C1", leaf="#2D6A4F", dot="#D4AF37", dark="#800F2F")
    title_c = "#A23E5B"
    D.append(([paper("#FFF7F8"), f'<path d="{arch_path(260, 90, 560, 660)}" fill="#F6E1E6" stroke="url(#gold)" stroke-width="12"/>', hero(540, 420, 1.1),
               floral_cluster(200, 640, 1.2, P, 1, "roses", False, 1), floral_cluster(880, 640, 1.2, P, -1, "roses", False, 2)],
              S([130, 800, 950, 1270], L(title_c, "#3A2330", "#B48A4A"), title="script", photo=rct(272, 102, 536, 636, "arch"), slot=True)))
    D.append(([radial_bg("#3A0A1E", "#12030A"), f'<path d="{heart_frame_path(220, 110, 640, 620)}" fill="#2A0A18" stroke="url(#gold)" stroke-width="10"/>', heart(540, 400, 2.2, "#C9184A", .6), sparkles(16, "#FFE08A", 3)],
              S([140, 780, 940, 1260], DK, tone="dark", title="script", photo=rct(290, 180, 500, 500, "heart"), slot=True)))
    D.append(([paper("#FAF7F2"), f'<rect x="200" y="100" width="680" height="620" fill="#FFFFFF" filter="url(#shadow)"/>', f'<rect x="230" y="130" width="620" height="500" fill="#EFE7DD"/>', hero(540, 380, 1.3),
               floral_cluster(W + 20, -20, 1.2, ROSE, -1, "roses", False, 3)],
              S([140, 780, 940, 1260], L(title_c, "#3A2330", "#9C7A3C"), title="script", photo=rct(230, 130, 620, 500, "rect"), slot=True)))
    D.append(([grad_bg("#1F2A44", "#0B1224"), frame_line(50, "url(#gold)", 3, 24), hero(540, 300, 1.4), sparkles(14, "#FFE08A", 4)],
              S([150, 500, 930, 1220], DK, tone="dark", title="deco", photo=rct(340, 110, 400, 380, "rounded"))))
    D.append(([paper("#F7F5EE"), floral_cluster(-40, -40, 2.0, dict(flower1="#FFFFFF", flower2="#E9C8C0", leaf="#6B8F71", dot="#C8A45D", center="#F2C14E"), 1, "flowers", True, 5),
               floral_cluster(W + 40, H + 40, 2.0, dict(flower1="#FFFFFF", flower2="#E9C8C0", leaf="#6B8F71", dot="#C8A45D", center="#F2C14E"), -1, "flowers", True, 6, -1), hero(540, 330, .9)],
              S([170, 470, 910, 1080], L("#3F5E47", "#3A2330", "#9C7A3C"), title="script", photo=rct(340, 150, 400, 340, "rounded"))))
    D.append(([paper("#FFF5F7"), f'<rect width="{W}" height="620" fill="#E7A4B2"/>', "".join(heart(x, y, s, "#FFFFFF", .5) for x, y, s in [(150, 120, 1), (930, 180, 1.3), (820, 520, .8), (240, 480, .7)]),
               f'<rect x="290" y="120" width="500" height="560" rx="250" fill="#FFFFFF" stroke="url(#gold)" stroke-width="10"/>', scallop_edge(620, "#FFF5F7", 26, 16, True)],
              S([130, 730, 950, 1270], L(title_c, "#3A2330", "#B48A4A"), title="script", photo=rct(302, 132, 476, 536, "pill"), slot=True)))
    D.append(([radial_bg("#F9E0E6", "#F1C5D0"), "".join(balloon(x, y, r, c) for x, y, r, c in [(120, 170, 70, "#FFFFFF"), (260, 110, 55, "#E7A4B2"), (820, 110, 55, "#E7A4B2"), (960, 170, 70, "#FFFFFF")]),
               hero(540, 1170, .9)],
              S([150, 420, 930, 1030], L(title_c, "#3A2330", "#B48A4A"), title="deco", photo=rct(360, 150, 360, 250, "rounded"))))
    D.append(([paper("#FFFDF8"), f'<rect width="300" height="{H}" fill="#A23E5B"/>', "".join(heart(150, y, 1.1, "#FFFFFF", .35) for y in (200, 520, 840, 1160)), floral_cluster(W + 20, H + 20, 1.3, ROSE, -1, "roses", False, 7, -1)],
              S([370, 460, 1010, 1180], L(title_c, "#3A2330", "#B48A4A"), title="classic", align="left", photo=rct(370, 100, 330, 330, "rounded"))))
    D.append(([radial_bg("#5A0A2A", "#1E0312"), floral_cluster(-30, H + 30, 1.6, ROSE, 1, "roses", False, 8, -1), floral_cluster(W + 30, H + 30, 1.6, ROSE, -1, "roses", False, 9, -1), hero(540, 200, .8)],
              S([150, 330, 930, 1000], DK, tone="dark", title="script", photo=rct(360, 330, 360, 300, "rounded"))))
    D.append(([paper("#F6EEF7"), f'<rect x="120" y="120" width="400" height="480" fill="#FFFFFF" transform="rotate(-6 320 360)" filter="url(#shadow)"/>',
               f'<rect x="560" y="140" width="400" height="480" fill="#FFFFFF" transform="rotate(5 760 380)" filter="url(#shadow)"/>', heart(540, 660, 1.2, "#C9184A")],
              S([140, 740, 940, 1260], L(title_c, "#3A2330", "#B48A4A"), title="script", photo=rct(170, 150, 740, 420, "rounded"))))
    m = COUPLE_MAPS.get(kind, {})
    out = []
    for parts, spec in D:
        def fix(t):
            for a, b in m.items():
                t = t.replace(a, b)
            return t
        parts = [fix(p) for p in parts]
        spec = json.loads(fix(json.dumps(spec)))
        out.append((parts, spec))
    return out


PARTY_MAP = {"#FFF9F1": "#FFF8E7", "#3A0CA3": "#0B132B", "#10002B": "#050814", "#FFFBF2": "#F4F9FF", "#FFE0EC": "#E0F2FE", "#FF6B9A": "#7B2CBF", "#FF8E3C": "#3A0CA3",
             "#111111": "#2B0A3D", "#F0F9FF": "#FFF4E6", "#5BC0EB": "#FF8E3C", "#FFFDF7": "#F7FFF7", "#B79CED": "#06D6A0", "#FFE5EC": "#E8F7FF", "#FFC2D4": "#BDE0FE",
             "#D62869": "#3A0CA3", "#06D6A0": "#FF5FA2", "#118AB2": "#FFB703"}


def simple_set(kind):
    if kind == "party":
        out = []
        for parts, spec in simple_set("birthday"):
            def fix(t):
                for a, b in PARTY_MAP.items():
                    t = t.replace(a, b)
                return t
            out.append(([fix(p) for p in parts], json.loads(fix(json.dumps(spec)))))
        return out[5:] + out[:5]
    D = []
    if kind in ("birthday", "party"):
        C = ["#FF5FA2", "#FFD23F", "#5BC0EB", "#B79CED", "#06D6A0"]
        D.append(([paper("#FFF9F1"), "".join(balloon(x, y, r, c) for x, y, r, c in [(120, 170, 80, C[0]), (270, 100, 64, C[2]), (810, 100, 64, C[1]), (960, 170, 80, C[3])]), cake(540, 1190, .9, "#FFB3C7", "#FFFFFF", "#E0115F"), confetti(40, C, 1, (80, 350, 1000, 1000))],
                  S([150, 420, 930, 1000], L("#D62869", "#3A2330", "#118AB2"), title="deco", photo=circ(540, 400, 100))))
        D.append(([radial_bg("#3A0CA3", "#10002B"), confetti(90, C, 2), "".join(party_hat(x, y, 1, a, C[i], "#FFD23F") for i, (x, y, a) in enumerate([(160, 180, -20), (920, 180, 20)])), "".join(gift(x, 1200, 1, C[i]) for i, x in enumerate((180, 380, 700, 900)))],
                  S([150, 330, 930, 1050], DK, tone="dark", title="script", photo=circ(540, 330, 100))))
        D.append(([paper("#FFFBF2"), bunting(40, C, 11, 50), f'<circle cx="540" cy="700" r="400" fill="#FFE0EC"/>', confetti(30, C, 3)],
                  S([190, 380, 890, 1020], L("#D62869", "#3A2330", "#118AB2"), title="deco", photo=circ(540, 380, 100))))
        D.append(([grad_bg("#FF6B9A", "#FF8E3C"), f'<rect x="100" y="180" width="880" height="990" rx="40" fill="#FFFFFF" opacity=".95"/>', "".join(balloon(x, 120, 60, c) for x, c in [(160, C[1]), (920, C[2])]), cake(540, 1110, .6)],
                  S([160, 240, 920, 940], L("#D62869", "#3A2330", "#118AB2"), title="classic", photo=circ(540, 280, 90))))
        D.append(([rect_bg("#111111"), "".join(balloon(x, y, r, "#D4AF37") for x, y, r in [(130, 200, 90), (950, 220, 90), (260, 110, 60)]), confetti(60, ["#D4AF37", "#FFFFFF"], 4), frame_line(50, "#D4AF37", 2)],
                  S([150, 420, 930, 1150], DK, tone="dark", title="deco", photo=circ(540, 400, 100))))
        D.append(([paper("#F0F9FF"), f'<rect width="{W}" height="480" fill="#5BC0EB"/>', "".join(balloon(x, y, 55, c) for x, y, c in [(150, 180, C[0]), (330, 120, C[1]), (750, 120, C[3]), (930, 180, C[4])]), scallop_edge(480, "#F0F9FF", 24, 16, True), cake(540, 360, .5)],
                  S([130, 560, 950, 1250], L("#1F4E89", "#3A2330", "#D62869"), title="deco")))
        D.append(([paper("#FFFDF7"), f'<rect width="300" height="{H}" fill="#B79CED"/>', "".join(balloon(150, y, 60, c) for y, c in [(180, C[0]), (520, C[1]), (860, C[4])]), gift(860, 1190, 1.1, C[0])],
                  S([370, 330, 1010, 1080], L("#6C4AB6", "#3A2330", "#D62869"), title="classic", align="left", photo=rct(370, 90, 200, 200))))
        D.append(([radial_bg("#FFE5EC", "#FFC2D4"), "".join(star(x, y, r, "#FFD23F") for x, y, r in [(150, 150, 30), (930, 200, 24), (200, 1180, 26), (880, 1150, 34)]), cake(540, 1180, .7)],
                  S([160, 280, 920, 960], L("#D62869", "#3A2330", "#6C4AB6"), title="script", photo=circ(540, 300, 100))))
        D.append(([paper("#FFFFFF"), f'<rect x="200" y="100" width="680" height="620" fill="#FFFFFF" filter="url(#shadow)"/>', f'<rect x="230" y="130" width="620" height="500" fill="#FFE0EC"/>', confetti(40, C, 6, (60, 700, 1020, 1300)), "".join(balloon(x, 740, 40, c) for x, c in [(150, C[0]), (930, C[2])])],
                  S([140, 770, 940, 1260], L("#D62869", "#3A2330", "#118AB2"), title="script", photo=rct(230, 130, 620, 500, "rect"), slot=True)))
        D.append(([grad_bg("#06D6A0", "#118AB2"), f'<circle cx="540" cy="700" r="430" fill="#FFFFFF" opacity=".95"/>', "".join(party_hat(x, y, 1, a, C[i], "#FFFFFF") for i, (x, y, a) in enumerate([(130, 160, -25), (950, 160, 25), (130, 1190, -10), (950, 1190, 10)]))],
                  S([200, 420, 880, 1000], L("#118AB2", "#3A2330", "#D62869"), title="deco", photo=circ(540, 380, 90))))
        return D
    if kind == "griha":
        D.append(([paper("#FFF3D6"), toran(0, ("#FF9F1C", "#F77F00", "#FFD166"), "#2D6A4F", 0), house(540, 420, 1.0, "#7B1E1E"), kalash(380, 640, .45), kalash(700, 640, .45)],
                  S([140, 720, 940, 1260], L("#7B1E1E", "#3A2330", "#B7791F"), title="deco")))
        D.append(([radial_bg("#0F7C7A", "#073B3A"), swastik(540, 200, .9, "#FFD166"), f'<rect x="130" y="330" width="820" height="880" rx="30" fill="#FFF8EE"/>', key(760, 1230, 1, -20, "#FFD166")],
                  S([180, 370, 900, 1180], L("#0F5C5A", "#3A2330", "#B7791F"), title="classic")))
        D.append(([paper("#FFFAF0"), f'<rect width="{W}" height="520" fill="#7B1E1E"/>', house(540, 280, .8, "#FFD166"), scallop_edge(520, "#FFFAF0", 24, 16, True), rangoli(540, 1350, 300, ["#C1121F", "#FF9F1C", "#FFD166", "#2D6A4F"])],
                  S([130, 600, 950, 1150], L("#7B1E1E", "#3A2330", "#B7791F"), title="deco")))
        D.append(([grad_bg("#F9A825", "#F28C28"), f'<path d="{arch_path(160, 170, 760, 1060)}" fill="#FFF8EC" stroke="url(#gold)" stroke-width="10"/>', swastik(540, 330, .6, "#C1121F"), diya_row(1270, 5, .5, 200, 880)],
                  S([230, 430, 850, 1150], L("#9D0208", "#3A2330", "#B7791F"), title="classic")))
        D.append(([paper("#F5F9F4"), house(820, 1080, .9, "#3F5E47"), "".join(leaf(x, y, 80, a, "#6B8F71", .9) for x, y, a in [(180, 1200, -80), (200, 1160, -110), (220, 1210, -60)]), key(200, 250, 1, 30, "#9C7A3C")],
                  S([120, 360, 900, 900], L("#3F5E47", "#3A2330", "#9C7A3C"), title="deco", align="left")))
        D.append(([radial_bg("#6D0F24", "#2E0510"), frame_line(46, "url(#gold)", 4, 20), kalash(540, 330, .6), "".join(footprint(x, 1180, .9, 0, "#E0A800") for x in (470, 610))],
                  S([150, 460, 930, 1080], DK, tone="dark", title="deco")))
        D.append(([paper("#FFF6E8"), f'<rect width="300" height="{H}" fill="#F28C28"/>', "".join(marigold(150, y, 18) for y in range(40, H, 58)), house(860, 1150, .55, "#7B1E1E")],
                  S([370, 300, 1010, 1040], L("#7B1E1E", "#3A2330", "#B7791F"), title="classic", align="left")))
        D.append(([paper("#FFFBF2"), rangoli(540, 330, 250, ["#C1121F", "#FF9F1C", "#FFD166", "#2D6A4F"]), swastik(540, 330, .45, "#FFFFFF"), "".join(diya(x, 1240, .5) for x in (150, 930))],
                  S([150, 620, 930, 1210], L("#9D0208", "#3A2330", "#B7791F"), title="deco")))
        D.append(([grad_bg("#BFE3C0", "#7FB77E"), f'<rect x="120" y="130" width="840" height="1090" rx="30" fill="#FFFFFF" opacity=".94"/>', house(540, 330, .55, "#2D6A4F"), toran(0, ("#FF9F1C", "#F77F00", "#FFD166"), "#2D6A4F", 0)[:0]],
                  S([170, 520, 910, 1180], L("#2D6A4F", "#3A2330", "#B7791F"), title="classic")))
        D.append(([radial_bg("#3D2A1A", "#140C06"), house(540, 1060, 1.1, "#E0A800"), diya_row(1270, 4, .45, 300, 780), sparkles(12, "#FFE08A", 5, (80, 80, 1000, 700))],
                  S([150, 180, 930, 820], DK, tone="dark", title="script")))
        return D
    if kind in ("baby", "naming"):
        pink, blue = "#F7C6C7", "#AED6F1"
        cloudset = cloud(80, 160, 1.2, "#FFFFFF", .9) + cloud(760, 110, 1.3, "#FFFFFF", .9)
        if kind == "baby":
            D.append(([grad_bg("#CDE8D0", "#9DD1A6"), cradle(540, 520, .9, cloth="#F7C6C7"), f'<rect x="120" y="640" width="840" height="620" rx="30" fill="#FFFFFF" opacity=".95"/>'],
                      S([160, 670, 920, 1240], L("#3E8E41", "#3A2330", "#D4A64A"), title="script")))
            D.append(([paper("#FFF7F8"), bangles(200, 1150, 1.1, ("#C1121F", "#3E8E41", "#F4C430")), bangles(880, 1150, 1.1, ("#C1121F", "#3E8E41", "#F4C430")), floral_cluster(-30, -30, 1.8, dict(flower1="#F4978E", flower2="#F7C6C7", leaf="#3E8E41", dot="#F4C430", center="#F4C430"), 1, "flowers", True, 1)],
                      S([150, 380, 930, 980], L("#B23A48", "#3A2330", "#3E8E41"), title="script", photo=circ(540, 330, 95))))
        else:
            D.append(([grad_bg("#E0F0FF", "#B8DBF5"), cradle(540, 520, .9, cloth="#AED6F1"), f'<rect x="120" y="640" width="840" height="620" rx="30" fill="#FFFFFF" opacity=".95"/>', star(900, 120, 26, "#F4C430")],
                      S([160, 670, 920, 1240], L("#1F6F8B", "#3A2330", "#D4AF37"), title="script")))
            D.append(([paper("#FFFDF5"), "".join(footprint(x, y, 1, a, "#F8BBD0") for x, y, a in [(160, 1150, -15), (250, 1080, 10), (830, 1150, -10), (920, 1080, 15)]), moon(540, 220, 90, "#FFF3B0"), star(660, 170, 20, "#F4C430")],
                      S([150, 380, 930, 1000], L("#1F6F8B", "#3A2330", "#D4AF37"), title="script", photo=circ(540, 250, 100))))
        D.append(([radial_bg("#2A3A6A", "#101838"), moon(820, 230, 110, "#FFF3C4", "#2A3A6A"), "".join(star(x, y, r, "#FFE08A") for x, y, r in [(150, 180, 16), (330, 110, 10), (560, 150, 12), (250, 320, 8)]), cloud(-40, 1180, 1.8, "#FFFFFF", .95), cloud(640, 1210, 1.6, "#FFFFFF", .95)],
                  S([150, 400, 930, 1030], DK, tone="dark", title="script", photo=circ(540, 380, 100))))
        D.append(([paper("#FFF9FB"), cloudset, f'<path d="{arch_path(160, 330, 760, 950)}" fill="{pink if kind == "baby" else blue}" opacity=".45"/>', "".join(balloon(x, 330, 45, c) for x, c in [(150, "#F7C6C7"), (930, "#AED6F1")])],
                  S([230, 560, 850, 1220], L("#B23A48" if kind == "baby" else "#1F6F8B", "#3A2330", "#D4A64A"), title="script", photo=circ(540, 500, 95))))
        D.append(([paper("#FFFFFF"), f'<rect width="{W}" height="520" fill="{pink if kind == "baby" else blue}"/>', cloudset, moon(540, 300, 90, "#FFF3B0"), scallop_edge(520, "#FFFFFF", 24, 16, True)],
                  S([130, 600, 950, 1250], L("#B23A48" if kind == "baby" else "#1F6F8B", "#3A2330", "#D4A64A"), title="deco")))
        D.append(([grad_bg("#FFF3B0", "#FAD4B5"), peacock_feather(150, 330, 1.1, -25), peacock_feather(930, 330, 1.1, 25), f'<circle cx="540" cy="760" r="400" fill="#FFFFFF" opacity=".9"/>'],
                  S([200, 480, 880, 1080], L("#1F6F8B", "#3A2330", "#D4A64A"), title="deco", photo=circ(540, 420, 95))))
        D.append(([paper("#F5FBF6"), f'<rect width="300" height="{H}" fill="#CDE8D0"/>', "".join(star(150, y, 22, "#F4C430") for y in (180, 460, 740, 1020, 1260)), cradle(860, 1180, .5, cloth=pink if kind == "baby" else blue)],
                  S([370, 360, 1010, 1060], L("#3E8E41", "#3A2330", "#D4A64A"), title="classic", align="left", photo=rct(370, 110, 200, 200))))
        D.append(([radial_bg("#FDE2E4" if kind == "baby" else "#E3F2FD", "#F6D6E0" if kind == "baby" else "#C9E4F7"), "".join(balloon(x, y, r, c) for x, y, r, c in [(130, 1080, 70, "#FFFFFF"), (260, 1150, 60, pink), (820, 1150, 60, blue), (950, 1080, 70, "#FFFFFF")]), moon(540, 200, 70, "#FFF3B0")],
                  S([150, 330, 930, 950], L("#B23A48" if kind == "baby" else "#1F6F8B", "#3A2330", "#D4A64A"), title="deco")))
        D.append(([paper("#FFFDF7"), f'<path d="{arch_path(290, 110, 500, 560)}" fill="#F3EEE4" stroke="url(#gold)" stroke-width="12"/>', cradle(540, 560, .55, cloth=pink if kind == "baby" else blue),
                   "".join(star(x, y, 18, "#F4C430") for x, y in [(230, 200), (850, 220), (200, 560), (880, 600)])],
                  S([140, 720, 940, 1260], L("#B23A48" if kind == "baby" else "#1F6F8B", "#3A2330", "#D4A64A"), title="classic", photo=rct(302, 122, 476, 536, "arch"), slot=True)))
        D.append(([grad_bg("#6B4C9A", "#3E2A66"), "".join(star(x, y, r, "#FFE08A") for x, y, r in [(120, 150, 18), (960, 180, 22), (200, 1200, 20), (900, 1180, 16)]), cloud(380, 1130, 1.2, "#FFFFFF", .9), moon(540, 220, 80, "#FFF3C4")],
                  S([150, 380, 930, 1000], DK, tone="dark", title="script", photo=circ(540, 250, 100))))
        return D
    if kind == "puja":
        D.append(([paper("#FFF8E1")] + [banana_leaf(x, H + 40, 1.2, a) for x, a in [(50, 12), (1030, -12)]] + [kalash(540, 330, .6), "".join(bell(x, 120, .6) for x in (300, 780))],
                  S([200, 480, 880, 1150], L("#B71C1C", "#3A2330", "#4C8C2B"), title="deco")))
        D.append(([radial_bg("#B71C1C", "#5E0A0A"), f'<path d="{arch_path(150, 160, 780, 1070)}" fill="#FFF8E1" stroke="url(#gold)" stroke-width="10"/>', havan(540, 1180, .7), "".join(bell(x, 250, .8) for x in (75, 1005))],
                  S([230, 380, 850, 1010], L("#B71C1C", "#3A2330", "#C9A227"), title="classic")))
        D.append(([paper("#FFFBF0"), thali(540, 300, 1.1), lotus(160, 1230, .9), lotus(920, 1230, .9)],
                  S([150, 460, 930, 1130], L("#B71C1C", "#3A2330", "#C9A227"), title="deco")))
        D.append(([grad_bg("#FF9933", "#E65100"), mandala(540, 675, 520, "#FFFFFF", .2), f'<rect x="120" y="300" width="840" height="850" rx="30" fill="#FFF8E1"/>', "".join(bell(x, 150, .8) for x in (220, 540, 860))],
                  S([170, 340, 910, 1120], L("#B71C1C", "#3A2330", "#C9A227"), title="classic")))
        D.append(([radial_bg("#2A0A0A", "#0D0202"), frame_line(46, "url(#gold)", 4, 20), havan(540, 330, .9), diya_row(1250, 5, .5, 220, 860)],
                  S([150, 520, 930, 1180], DK, tone="dark", title="deco")))
        D.append(([paper("#FFF6E5"), f'<rect width="{W}" height="500" fill="#F4C430"/>', kalash(540, 400, .55), "".join(bell(x, y, .6) for x, y in [(160, 180), (920, 180)]), scallop_edge(500, "#FFF6E5", 26, 16, True)],
                  S([130, 580, 950, 1250], L("#B71C1C", "#3A2330", "#4C8C2B"), title="deco")))
        D.append(([paper("#FFFDF7"), f'<rect width="300" height="{H}" fill="#B71C1C"/>', "".join(bell(150, y, .7) for y in (260, 640, 1020)), lotus(860, 1210, .9)],
                  S([370, 300, 1010, 1060], L("#B71C1C", "#3A2330", "#C9A227"), title="classic", align="left")))
        D.append(([grad_bg("#FDF3D8", "#F7D794"), rangoli(540, 1350, 380, ["#B71C1C", "#FF9933", "#F4C430", "#4C8C2B"]), swastik(540, 200, .7, "#B71C1C"), "".join(diya(x, 330, .6) for x in (180, 900))],
                  S([150, 330, 930, 960], L("#B71C1C", "#3A2330", "#4C8C2B"), title="deco")))
        D.append(([radial_bg("#4C8C2B", "#1F3D12")] + [banana_leaf(x, 120, .9, a) for x, a in [(60, 160), (1020, -160)]] + [f'<circle cx="540" cy="700" r="420" fill="#FFF8E1"/>', lotus(540, 1060, .6)],
                  S([200, 400, 880, 960], L("#1F5E1B", "#3A2330", "#B7791F"), title="classic")))
        D.append(([paper("#FFF8EE"), double_frame("#C9A227"), lotus(540, 300, .9), "".join(marigold(x, y, 18) for x, y in [(130, 130), (950, 130), (130, 1220), (950, 1220)])],
                  S([150, 480, 930, 1220], L("#B71C1C", "#3A2330", "#C9A227"), title="deco")))
        return D
    if kind == "shop":
        D.append(([paper("#F5EFE6"), ribbon_band(320, "#D62828", "#9D0208"), scissors(820, 170, .7), confetti(40, ["#D4AF37", "#D62828", "#1B2A4A"], 1, (80, 600, 1000, 1250))],
                  S([140, 520, 940, 1220], L("#D62828", "#1B2A4A", "#B7791F"), title="deco")))
        D.append(([rect_bg("#111111"), "".join(balloon(x, y, r, "#D4AF37") for x, y, r in [(130, 200, 80), (950, 220, 80)]), coins(540, 1230, .9), frame_line(50, "#D4AF37", 2), sparkles(14, "#FFE08A", 2)],
                  S([150, 300, 930, 1080], DK, tone="dark", title="deco")))
        D.append(([paper("#FFF8EE"), storefront(540, 330, .9), toran(0, ("#FF9F1C", "#F77F00", "#FFD166"), "#2D6A4F", 0)],
                  S([140, 600, 940, 1250], L("#6A0F1A", "#3A2330", "#B7791F"), title="deco")))
        D.append(([radial_bg("#6A0F1A", "#2A0508"), frame_line(46, "url(#gold)", 4, 20), kalash(540, 300, .55), fireworks(170, 1150, 120, "#FFD166", 18, 3), fireworks(910, 1150, 120, "#FFD166", 18, 4)],
                  S([150, 460, 930, 1060], DK, tone="dark", title="deco")))
        D.append(([grad_bg("#1B2A4A", "#0B1428"), ribbon_band(H - 200, "#D62828", "#9D0208"), scissors(540, 220, .7), sparkles(16, "#FFE08A", 5, (80, 400, 1000, 1000))],
                  S([150, 400, 930, 1000], DK, tone="dark", title="deco")))
        D.append(([paper("#FFFBF2"), f'<rect width="{W}" height="500" fill="#D62828"/>', storefront(540, 330, .55), scallop_edge(500, "#FFFBF2", 26, 16, True)],
                  S([130, 580, 950, 1250], L("#D62828", "#3A2330", "#B7791F"), title="deco")))
        D.append(([paper("#FFFDF7"), f'<rect width="300" height="{H}" fill="#1B2A4A"/>', "".join(balloon(150, y, 55, c) for y, c in [(180, "#D4AF37"), (520, "#D62828"), (860, "#FFFFFF")]), coins(860, 1220, .7)],
                  S([370, 280, 1010, 1080], L("#1B2A4A", "#3A2330", "#D62828"), title="classic", align="left")))
        D.append(([radial_bg("#FFF3D6", "#F5D491"), "".join(marigold(x, 40 + (i % 2) * 18, 20) for i, x in enumerate(range(40, W, 58))), swastik(540, 240, .6, "#C1121F"), coins(180, 1220, .7), coins(900, 1220, .7)],
                  S([150, 370, 930, 1090], L("#9D0208", "#3A2330", "#B7791F"), title="classic")))
        D.append(([paper("#F5EFE6"), f'<circle cx="540" cy="675" r="450" fill="#FFFFFF" stroke="url(#gold)" stroke-width="10"/>', ribbon_band(1210, "#D62828", "#9D0208", False), scissors(900, 1180, .45)],
                  S([190, 380, 890, 980], L("#D62828", "#1B2A4A", "#B7791F"), title="deco")))
        D.append(([radial_bg("#0F3D2E", "#04160F"), fireworks(540, 230, 200, "#FFD166", 24, 6), confetti(60, ["#FFD166", "#FFFFFF", "#D62828"], 7, (60, 500, 1020, 1300))],
                  S([150, 480, 930, 1100], DK, tone="dark", title="script")))
        return D
    if kind == "morning":
        D.append(([grad_bg("#FFD6A5", "#FFF1C1"), sun(540, 820, 150, "#FFB703", "#FFD166"), hills(930, "#95D5B2", "#52B788"), birds(700, 300, 1)],
                  S([150, 150, 930, 640], L("#9C4A00", "#3A2330", "#219EBC"), title="script")))
        D.append(([paper("#F7EFE5"), cup(540, 1120, 1.3, "#6F4E37"), "".join(leaf(x, y, 80, a, "#7BB661", .8) for x, y, a in [(120, 1200, -60), (160, 1150, -100), (940, 1200, 240)])],
                  S([150, 200, 930, 850], L("#6F4E37", "#3A2330", "#C08552"), title="script")))
        D.append(([grad_bg("#8ECAE6", "#E0F2FB"), cloud(60, 1130, 1.6, "#FFFFFF"), cloud(620, 1180, 1.5, "#FFFFFF"), sun(870, 200, 70), birds(200, 250, 1)],
                  S([150, 330, 930, 980], L("#1F4E89", "#3A2330", "#FB8500"), title="deco")))
        D.append(([paper("#FFFBEF"), "".join(sunflower(x, y, r) for x, y, r in [(120, 1200, 100), (300, 1260, 80), (960, 150, 110), (800, 90, 70)])],
                  S([150, 330, 930, 1050], L("#9C4A00", "#3A2330", "#6A994E"), title="script")))
        D.append(([radial_bg("#FFE5D9", "#FFCAD4"), lotus(540, 1200, 1.3), lotus(200, 1260, .7), lotus(880, 1260, .7), birds(640, 200, 1, "#7A5C61")],
                  S([150, 300, 930, 950], L("#B23A48", "#3A2330", "#6A994E"), title="script")))
        D.append(([grad_bg("#FFB703", "#FB8500"), f'<circle cx="540" cy="675" r="450" fill="#FFFBEF" opacity=".95"/>', "".join(f'<rect x="{540 - 8}" y="0" width="16" height="140" rx="8" fill="#FFFFFF" opacity=".5" transform="rotate({a} 540 675)"/>' for a in range(0, 360, 30))],
                  S([190, 400, 890, 960], L("#9C4A00", "#3A2330", "#219EBC"), title="deco")))
        D.append(([paper("#F4FBF6"), f'<rect width="300" height="{H}" fill="#95D5B2"/>', "".join(leaf(150, y, 100, a, "#40916C") for y, a in [(200, -30), (420, 200), (640, -30), (860, 200), (1080, -30)]), sun(860, 200, 60)],
                  S([370, 330, 1010, 1080], L("#1B4332", "#3A2330", "#FB8500"), title="classic", align="left")))
        D.append(([radial_bg("#FFF1C1", "#FFD166"), sun(540, 260, 110), cup(820, 1170, .9, "#B5541C"), "".join(flower(x, y, 40, c, "#FFD166", 5, 1, True) for x, y, c in [(160, 1180, "#FF8FAB"), (260, 1250, "#FFFFFF"), (120, 1280, "#FF8FAB")])],
                  S([150, 430, 930, 1030], L("#9C4A00", "#3A2330", "#6A994E"), title="deco")))
        D.append(([grad_bg("#CDB4DB", "#FFC8DD"), hills(1050, "#BDE0FE", "#A2D2FF"), sun(250, 950, 90, "#FFF1C1", "#FFE5A0"), birds(620, 250, 1, "#5E548E")],
                  S([150, 200, 930, 780], L("#5E548E", "#3A2330", "#B23A48"), title="script")))
        D.append(([paper("#FFFDF7"), frame_line(50, "#E9C46A", 3, 30), sunflower(540, 260, 110), "".join(leaf(x, y, 70, a, "#6A994E") for x, y, a in [(440, 380, 150), (640, 380, 30)])],
                  S([150, 470, 930, 1210], L("#9C4A00", "#3A2330", "#6A994E"), title="deco")))
        return D
    return D


CATS = {
    "shraddhanjali": tribute, "diwali": diwali, "karva-chauth": karva, "navratri": navratri, "dussehra": dussehra,
    "inv-wedding": wedding_inv, "wedding": lambda: couple_set("wed"),
    "inv-engagement": lambda: couple_set("inv-eng"), "engagement": lambda: couple_set("eng"), "anniversary": lambda: couple_set("anni"),
    "birthday": lambda: simple_set("birthday"), "inv-birthday-party": lambda: simple_set("party"),
    "inv-griha-pravesh": lambda: simple_set("griha"), "inv-baby-shower": lambda: simple_set("baby"), "inv-naming-ceremony": lambda: simple_set("naming"),
    "inv-puja": lambda: simple_set("puja"), "inv-shop-opening": lambda: simple_set("shop"), "good-morning": lambda: simple_set("morning"),
}


def build(only=None):
    specs, files = {}, []
    for cat, fn in CATS.items():
        if only and cat not in only:
            continue
        specs[cat] = []
        for i, (parts, spec) in enumerate(fn()):
            tid = f"T-{cat}-{i + 1}"
            spec = dict(spec, id=tid)
            specs[cat].append(spec)
            files.append((tid, svg([p for p in parts if p])))
    return specs, files


async def render(files):
    from playwright.async_api import async_playwright
    from PIL import Image
    import io
    os.makedirs(os.path.join(OUT, "thumb"), exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H})
        for tid, s in files:
            await pg.set_content(f'<html><body style="margin:0">{s}</body></html>')
            png = await pg.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
            im = Image.open(io.BytesIO(png)).convert("RGB")
            im.save(os.path.join(OUT, tid + ".webp"), "WEBP", quality=88, method=5)
            im.resize((432, 540), Image.LANCZOS).save(os.path.join(OUT, "thumb", tid + ".webp"), "WEBP", quality=82)
        await b.close()




def flute(x, y, s, a):
    return (f'<g transform="translate({x} {y}) rotate({a}) scale({s})"><rect x="-160" y="-10" width="320" height="20" rx="10" fill="#8B5A2B"/>'
            + "".join(f'<circle cx="{i}" cy="0" r="5" fill="#3E2415"/>' for i in range(-90, 100, 36))
            + '<rect x="-150" y="-12" width="14" height="24" fill="#F2C14E"/><rect x="136" y="-12" width="14" height="24" fill="#F2C14E"/></g>')


def naming_set():
    D = []
    B, G = "#1F6F8B", "#3E8E41"
    D.append(([paper("#FFFDF2"), peacock_feather(170, 360, 1.3, -20), flute(760, 250, 1.1, -25), f'<circle cx="540" cy="520" r="170" fill="#E6F4F1" stroke="url(#gold)" stroke-width="8"/>'],
              S([150, 740, 930, 1250], L(B, "#3A2330", "#D4AF37"), title="deco", photo=circ(540, 520, 170), slot=True)))
    D.append(([paper("#F6FBF3")] + [banana_leaf(x, H + 40, 1.1, a) for x, a in [(40, 14), (1040, -14)]] + [cradle(540, 440, .8, cloth="#AED6F1")],
              S([200, 560, 880, 1150], L(G, "#3A2330", "#D4AF37"), title="script")))
    moon_cradle = moon(540, 280, 160, "#FFF3C4", "#16254D") + '<path d="M480 420 L420 560 M600 420 L660 560" stroke="#FFF3C4" stroke-width="3"/>' + '<path d="M400 560 C 440 620, 640 620, 680 560 Z" fill="#AED6F1" stroke="#FFF3C4" stroke-width="4"/>'
    D.append(([radial_bg("#2A3A6A", "#0E1634"), moon_cradle, "".join(star(x, y, r, "#FFE08A") for x, y, r in [(150, 180, 16), (900, 160, 20), (220, 460, 10), (860, 480, 12), (130, 700, 8), (960, 720, 9)])],
              S([150, 700, 930, 1240], DK, tone="dark", title="script")))
    trail = "".join(footprint(160 + i * 110, 1250 - i * 70 + (30 if i % 2 else 0), .8, 35, "#F8BBD0" if i % 2 else "#AED6F1") for i in range(8))
    D.append(([paper("#FFF8FB"), trail],
              S([140, 230, 940, 820], L("#C2185B", "#3A2330", B), title="script", photo=circ(540, 250, 100))))
    D.append(([grad_bg("#DCEFFB", "#AED6F1"), f'<path d="{arch_path(270, 110, 540, 640)}" fill="#FFFFFF" stroke="url(#gold)" stroke-width="12"/>', "".join(star(x, y, r, "#F4C430") for x, y, r in [(180, 180, 26), (900, 200, 22), (200, 640, 18), (880, 660, 24)])],
              S([140, 800, 940, 1270], L(B, "#3A2330", "#D4AF37"), title="classic", photo=rct(282, 122, 516, 616, "arch"), slot=True)))
    border = "".join(leaf(x, y, 70, a, "#6BAA75", .9) for x in range(30, W, 70) for y, a in ((30, 20), (H - 30, 200))) + "".join(leaf(x, y, 70, a, "#6BAA75", .9) for y in range(80, H - 60, 70) for x, a in ((30, 100), (W - 30, 280)))
    D.append(([paper("#FFFDF7"), border, "".join(flower(x, y, 26, "#F8BBD0", "#F4C430", 5) for x, y in [(60, 60), (W - 60, 60), (60, H - 60), (W - 60, H - 60)])],
              S([150, 300, 930, 1080], L(G, "#3A2330", "#C2185B"), title="deco", photo=circ(540, 300, 100))))
    D.append(([paper("#FFFBEA"), f'<rect width="{W}" height="520" fill="#F4C430"/>', cradle(540, 470, .6, cloth="#F8BBD0"), scallop_edge(520, "#FFFBEA", 24, 16, True)],
              S([130, 600, 950, 1250], L("#8C5A00", "#3A2330", B), title="deco")))
    mobile = '<path d="M240 60 L840 60" stroke="#B7791F" stroke-width="5"/>' + "".join(f'<line x1="{x}" y1="60" x2="{x}" y2="{y}" stroke="#B7791F" stroke-width="2"/>' + (moon(x, y + 30, 36, "#FFF3C4", "#FDF6EC") if i == 2 else star(x, y + 30, 30, ["#F8BBD0", "#AED6F1", "#FFD166", "#C5E1A5", "#F8BBD0"][i])) for i, (x, y) in enumerate([(260, 180), (400, 250), (540, 200), (680, 250), (820, 180)]))
    D.append(([paper("#FDF6EC"), mobile],
              S([150, 420, 930, 1150], L("#6B4C9A", "#3A2330", B), title="script")))
    D.append(([radial_bg("#0F4C5C", "#062A33"), frame_line(50, "url(#gold)", 4, 26), cradle(540, 1180, .55, "url(#gold)", "#FFFFFF")],
              S([150, 250, 930, 900], DK, tone="dark", title="deco", photo=circ(540, 300, 100))))
    D.append(([grad_bg("#E8F5E9", "#C8E6C9"), mandala(540, 675, 480, "#1F6F8B", .12), peacock_feather(900, 1100, 1.2, 20), f'<rect x="130" y="260" width="820" height="820" rx="410" fill="#FFFFFF" opacity=".92"/>'],
              S([220, 400, 860, 960], L(B, "#3A2330", G), title="classic", photo=circ(540, 400, 95))))
    return D


def anniversary_set():
    D = []
    ROSE = dict(flower1="#C9184A", flower2="#FFB3C1", leaf="#2D6A4F", dot="#D4AF37", dark="#800F2F")
    D.append(([rect_bg("#111111"), frame_line(50, "url(#gold)", 3), "".join(heart(x, y, s, "#D4AF37", o) for x, y, s, o in [(160, 200, 1.2, .9), (920, 260, 1, .7), (200, 1150, .8, .6), (880, 1120, 1.3, .9)])],
              S([150, 330, 930, 1080], DK, tone="dark", title="script", photo=rct(360, 110, 360, 280, "rounded"))))
    D.append(([paper("#FFF5F5"), floral_cluster(-30, -30, 1.9, ROSE, 1, "roses", False, 1), floral_cluster(W + 30, H + 30, 1.9, ROSE, -1, "roses", False, 2, -1), f'<path d="{heart_frame_path(300, 330, 480, 440)}" fill="#FFE3E8" stroke="#C9184A" stroke-width="6"/>'],
              S([150, 820, 930, 1220], L("#C9184A", "#3A2330", "#B48A4A"), title="script", photo=rct(360, 380, 360, 360, "heart"), slot=True)))
    D.append(([paper("#F4ECE3"), f'<rect x="90" y="110" width="460" height="560" fill="#FFFFFF" transform="rotate(-5 320 390)" filter="url(#shadow)"/>',
               f'<rect x="120" y="140" width="400" height="440" fill="#EADBC8" transform="rotate(-5 320 390)"/>', "".join(heart(x, y, .7, "#C9184A") for x, y in [(700, 200), (860, 320), (760, 480)]),
               f'<path d="M620 560 C 700 620, 820 600, 900 680" stroke="#8B5A2B" stroke-width="3" fill="none" stroke-dasharray="8 6"/>'],
              S([140, 760, 940, 1260], L("#8B1030", "#3A2330", "#8B5A2B"), title="script", photo=rct(120, 140, 400, 440, "rect"))))
    D.append(([radial_bg("#800F2F", "#3A0414"), "".join(candle(x, 1230, .7, "#FFF3E6") for x in (160, 320, 760, 920)), sparkles(14, "#FFE08A", 3, (80, 80, 1000, 900))],
              S([150, 330, 930, 1000], DK, tone="dark", title="deco", photo=circ(540, 300, 110))))
    garland = "".join(marigold(540 + math.cos(math.radians(a)) * 300, 360 + math.sin(math.radians(a)) * 190, 16) for a in range(200, 341, 10))
    D.append(([paper("#FFF8EE"), garland, "".join(rose(x, 170, 22, "#C9184A", "#800F2F") for x in (240, 840)), f'<circle cx="540" cy="400" r="150" fill="#FDE2E4" stroke="url(#gold)" stroke-width="8"/>'],
              S([150, 620, 930, 1230], L("#800F2F", "#3A2330", "#B7791F"), title="deco", photo=circ(540, 400, 150), slot=True)))
    D.append(([grad_bg("#FFCCD5", "#FF8FA3"), "".join(heart(x, y, s, "#FFFFFF", o) for x, y, s, o in [(120, 130, 1.4, .5), (960, 220, 1, .5), (140, 1200, 1, .4), (930, 1150, 1.6, .5), (540, 110, .8, .6)]), f'<rect x="120" y="300" width="840" height="820" rx="40" fill="#FFFFFF" opacity=".93"/>'],
              S([170, 340, 910, 1090], L("#C9184A", "#3A2330", "#800F2F"), title="deco")))
    D.append(([radial_bg("#1D3557", "#0B1A33"), f'<circle cx="540" cy="360" r="220" fill="none" stroke="url(#gold)" stroke-width="10"/>', f'<circle cx="540" cy="360" r="200" fill="#14284A"/>', floral_cluster(W + 30, H + 30, 1.3, ROSE, -1, "roses", False, 4, -1)],
              S([150, 640, 930, 1200], DK, tone="dark", title="classic", photo=circ(540, 360, 200), slot=True)))
    D.append(([paper("#FFFDFB"), f'<rect width="300" height="{H}" fill="#C9184A"/>', "".join(rose(150, y, 34, "#FFB3C1", "#C9184A") for y in (200, 520, 840, 1160)), heart(860, 1180, 1.4, "#C9184A")],
              S([370, 460, 1010, 1100], L("#C9184A", "#3A2330", "#B48A4A"), title="classic", align="left", photo=rct(370, 100, 330, 330, "rounded"))))
    D.append(([paper("#EDE0D4"), "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFFFFF" transform="rotate({r} {x + w / 2} {y + h / 2})" filter="url(#shadow)"/>' for x, y, w, h, r in [(90, 120, 300, 340, -8), (390, 90, 300, 340, 4), (690, 130, 300, 340, -3)]), heart(540, 560, 1, "#C9184A")],
              S([140, 650, 940, 1250], L("#8B1030", "#3A2330", "#8B5A2B"), title="script", photo=rct(410, 110, 260, 300, "rect"))))
    D.append(([grad_bg("#FFF1F2", "#FFD6DD"), f'<rect x="170" y="100" width="740" height="600" rx="300" fill="#FFFFFF" stroke="#C9184A" stroke-width="5"/>', "".join(balloon(x, y, 50, c) for x, y, c in [(120, 820, "#C9184A"), (960, 820, "#FFB3C1")])],
              S([140, 760, 940, 1260], L("#C9184A", "#3A2330", "#B48A4A"), title="script", photo=rct(182, 112, 716, 576, "pill"), slot=True)))
    return D


CATS["inv-naming-ceremony"] = naming_set
CATS["anniversary"] = anniversary_set
WED_WISH_MAP = {"#7A0F2E": "#8B1030", "#3D0715": "#4A0418", "#FFF8EE": "#FFF5F0", "#0F3D2E": "#1B2A4A", "#04160F": "#0B1428", "#FFF6EC": "#FFF9F0", "#1B2A4A": "#0F3D2E", "#0B1428": "#04160F", "#FFF4E6": "#FFF1F2", "#C9184A": "#B7791F", "#FDE2E4": "#FFF3D6", "#F9C6CF": "#F5D491", "#5A0A1F": "#2B0A3D", "#200309": "#12031C"}


def wedding_wish():
    out = []
    for parts, spec in wedding_inv():
        def fix(t):
            for a, b in WED_WISH_MAP.items():
                t = t.replace(a, b)
            return t
        out.append(([fix(p) for p in parts], json.loads(fix(json.dumps(spec)))))
    return out[4:] + out[:4]


CATS["wedding"] = wedding_wish


if __name__ == "__main__":  # noqa
    only = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    specs, files = build(only)
    asyncio.run(render(files))
    path = os.path.join(ROOT, "content", "templates.json")
    allspecs = json.load(open(path)) if os.path.exists(path) else {}
    allspecs.update(specs)
    json.dump(allspecs, open(path, "w"), indent=1)
    print("rendered", len(files))
