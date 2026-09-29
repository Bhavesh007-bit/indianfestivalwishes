"""Build designed card templates: 10 layouts x category kits -> static/cards/T-<cat>-<n>.webp + templates.json
Run: python3 tools/templates.py   (needs playwright + chromium)"""
import json, os, sys, asyncio
sys.path.insert(0, os.path.dirname(__file__))
from art import *  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "static", "cards")

# ------------------------------------------------------------------ palettes
def P(**k):
    base = dict(paper="#FFF8EE", ink="#3A2330", title="#8B1030", accent="#B7791F", frame="#C9973B",
                dark1="#4A0E1F", dark2="#1E0610", flower1="#E85D75", flower2="#F4A259", leaf="#3A7D44",
                dot="#F2C14E", pastel1="#FDE2E4", pastel2="#E2ECE9", bg1="#8B1030", bg2="#5A0A1F")
    base.update(k)
    return base

ROYAL = P()
MAROON_GOLD = P(bg1="#7A0F2E", bg2="#3D0715", title="#7A0F2E")
EMERALD = P(bg1="#0F5132", bg2="#073322", title="#0F5132", dark1="#0F3D2E", dark2="#04160F", flower1="#F4A259", flower2="#FFFFFF", accent="#A87B1C")
NAVY = P(bg1="#1B2A4A", bg2="#0B1428", title="#1B2A4A", dark1="#172440", dark2="#070D1C", flower1="#F7C6D0", flower2="#FFFFFF", accent="#B7892F", pastel1="#E6ECF5", pastel2="#F3F0EA", paper="#FAF8F3")
PEACH = P(bg1="#F28C8C", bg2="#E76F51", title="#B23A48", paper="#FFF6F0", flower1="#F4978E", flower2="#FBC4AB", pastel1="#FFE5D9", pastel2="#FAD2E1")
SAGE = P(bg1="#6B8F71", bg2="#3F5E47", title="#3F5E47", paper="#F7F5EE", flower1="#FFFFFF", flower2="#E9C8C0", leaf="#6B8F71", accent="#9C7A3C", pastel1="#E3EBDD", pastel2="#F3E9E2")
BLUSH = P(bg1="#E7A4B2", bg2="#C86B85", title="#A23E5B", paper="#FFF7F8", flower1="#F4B6C2", flower2="#FFFFFF", leaf="#8FB996", pastel1="#FBE4EA", pastel2="#F6EEF7", accent="#B48A4A")
LILAC = P(bg1="#9D8BC9", bg2="#6C5B9E", title="#5B4A8B", paper="#FAF7FF", flower1="#CDB4DB", flower2="#FFC8DD", leaf="#8FB996", pastel1="#EDE7F6", pastel2="#E3F2FD")
SAFFRON = P(bg1="#E85D04", bg2="#9D0208", title="#9D0208", paper="#FFF6E5", flower1="#FF9F1C", flower2="#FFD166", leaf="#2D6A4F", accent="#B7791F", dark1="#6A040F", dark2="#2B0105")
MAGENTA = P(bg1="#C9184A", bg2="#800F2F", title="#A4133C", paper="#FFF5F7", flower1="#FF758F", flower2="#FFB3C1", leaf="#2D6A4F", dark1="#590D22", dark2="#23040E")
PURPLE = P(bg1="#5A189A", bg2="#240046", title="#5A189A", paper="#FBF6FF", flower1="#F72585", flower2="#FFBA08", leaf="#2D6A4F", dark1="#3C096C", dark2="#10002B")
TEAL = P(bg1="#087E8B", bg2="#05505A", title="#05505A", paper="#F2FBFB", flower1="#FF5A5F", flower2="#FFD166", leaf="#2D6A4F", dark1="#073B4C", dark2="#021A22", accent="#C08B30")
SKY = P(bg1="#8EC5FC", bg2="#5A9BD5", title="#1F4E89", paper="#F5FAFF", flower1="#FFD6E0", flower2="#FFF1B8", leaf="#8FB996", pastel1="#E0F0FF", pastel2="#FFF3D6", accent="#D4A017")
MINT = P(bg1="#95D5B2", bg2="#52B788", title="#1B4332", paper="#F4FBF6", flower1="#FFFFFF", flower2="#FFD6A5", leaf="#40916C", pastel1="#D8F3DC", pastel2="#FFF1E6")
PARTY = P(bg1="#3A0CA3", bg2="#7209B7", title="#7209B7", paper="#FFFBF2", flower1="#F72585", flower2="#4CC9F0", leaf="#80ED99", dark1="#240046", dark2="#0D001A", pastel1="#FFE5EC", pastel2="#E0F7FA")
CANDY = P(bg1="#FF6B9A", bg2="#FF8E3C", title="#D62869", paper="#FFF9F1", flower1="#FFD166", flower2="#06D6A0", pastel1="#FFE0EC", pastel2="#E0FBF1", accent="#118AB2")
GREY = P(bg1="#6B7280", bg2="#374151", title="#374151", ink="#374151", paper="#F7F6F3", flower1="#FFFFFF", flower2="#EDEAE4", leaf="#8A9A8B", accent="#8A7A5C", frame="#9CA3AF", dark1="#2F3437", dark2="#121416", pastel1="#EFEDE8", pastel2="#E7ECEF")
IVORY = P(bg1="#C9B79C", bg2="#8D7B63", title="#5C4A32", ink="#3F3A34", paper="#FBF8F2", flower1="#FFFFFF", flower2="#F1E7D6", leaf="#9AA88B", accent="#9C7A3C", frame="#B8A57F", dark1="#2B2620", dark2="#0F0D0A", pastel1="#F4EFE6", pastel2="#EEF0EA")
SUNRISE = P(bg1="#FFB703", bg2="#FB8500", title="#9C4A00", paper="#FFFBEF", flower1="#FFD166", flower2="#FF8FAB", leaf="#6A994E", pastel1="#FFF1C1", pastel2="#E7F5DC", accent="#219EBC")
KARVA = P(bg1="#8B1E3F", bg2="#3C0919", title="#8B1E3F", paper="#FFF5F2", flower1="#E63946", flower2="#FFB703", dark1="#1D1A39", dark2="#07061A", accent="#C9973B")

# ------------------------------------------------------------------ kits (motif sets per category)
def k_top_toran(p): return toran(0, (p["flower2"], "#F77F00", "#FFD166"), p["leaf"])
def k_top_bunting(p): return bunting(40, [p["flower1"], p["flower2"], p["bg1"], p.get("dot", "#FFD166")])
def k_top_lanterns(p): return "".join(lantern(x, y, 0, p["flower1"] if i % 2 else p["bg1"], "#B7791F", s) for i, (x, y, s) in enumerate([(150, 180, 1), (330, 110, .8), (750, 110, .8), (930, 180, 1)]))
def k_top_bells(p): return "".join(bell(x, y, s) for x, y, s in [(180, 160, 1), (360, 100, .8), (720, 100, .8), (900, 160, 1)])
def k_top_balloons(p): return "".join(balloon(x, y, r, c) for x, y, r, c in [(140, 150, 70, p["flower1"]), (260, 90, 60, p["flower2"]), (820, 90, 60, p["bg1"]), (950, 160, 72, p["flower1"])])
def k_top_stars(p): return moon(880, 170, 70, "#FFF3C4") + "".join(star(x, y, r, "#FFE08A") for x, y, r in [(180, 130, 18), (300, 220, 12), (620, 110, 14), (720, 240, 10), (420, 160, 9)])
def k_top_clouds(p): return cloud(80, 160, 1.2, "#FFFFFF", .9) + cloud(760, 110, 1.4, "#FFFFFF", .9) + sun(560, 150, 60)
def k_top_lilies(p): return lily(170, 250, 1.1, -30) + lily(910, 250, 1.1, 30) + "".join(leaf(x, y, 90, a, p["leaf"], .8) for x, y, a in [(120, 280, -70), (960, 280, 250)])

def k_hero_kalash(p, x, y, s): return kalash(x, y, s, leafc=p["leaf"])
def k_hero_diya(p, x, y, s): return diya(x - 110 * s, y, s * .8) + diya(x, y - 10, s) + diya(x + 110 * s, y, s * .8)
def k_hero_rings(p, x, y, s): return rings(x, y, s * 1.2)
def k_hero_cake(p, x, y, s): return cake(x, y + 60 * s, s * .8, p["pastel1"], "#FFFFFF", p["title"])
def k_hero_house(p, x, y, s): return house(x, y, s * .9, p["title"]) + key(x + 150 * s, y + 120 * s, s * .8, -30, p["accent"])
def k_hero_ribbon(p, x, y, s): return scissors(x, y, s * .8) + sparkles(6, "#FFD166", 11, (x - 200, y - 150, x + 200, y + 100))
def k_hero_baby(p, x, y, s): return moon(x, y, 60 * s, "#FFF3C4") + star(x + 120 * s, y - 40 * s, 20 * s, "#FFD166") + star(x - 120 * s, y + 20 * s, 14 * s, "#FFD166") + cloud(x - 90 * s, y + 50 * s, .7 * s, "#FFFFFF")
def k_hero_feet(p, x, y, s): return footprint(x - 40 * s, y, s, -12, p["title"]) + footprint(x + 40 * s, y - 30 * s, s, 12, p["title"])
def k_hero_candle(p, x, y, s): return candle(x, y, s)
def k_hero_dandiya(p, x, y, s): return dandiya(x - 40, y, s * .6, -30, p["flower1"], "#FFD166") + dandiya(x + 40, y, s * .6, 30, p["bg1"], "#FFD166") + garbo(x, y + 60 * s, s * .5)
def k_hero_bow(p, x, y, s): return bow_arrow(x, y, s * .6)
def k_hero_sieve(p, x, y, s): return moon(x + 110 * s, y - 60 * s, 55 * s, "#FFF3C4") + sieve(x - 30 * s, y + 10 * s, s * .8)
def k_hero_sun(p, x, y, s): return sun(x, y, 60 * s) + cup(x + 130 * s, y + 90 * s, s * .6)
def k_hero_heart(p, x, y, s): return heart(x - 40 * s, y, 1.6 * s, p["flower1"]) + heart(x + 40 * s, y - 20 * s, 1.2 * s, p["title"], .9)

KITS = {
    # invitations
    "inv-wedding": dict(pals=[MAROON_GOLD, ROYAL, EMERALD, NAVY, SAGE], top=k_top_toran, hero=k_hero_kalash, flowers="roses", tag="om"),
    "inv-engagement": dict(pals=[BLUSH, SAGE, NAVY, LILAC, IVORY], top=k_top_lanterns, hero=k_hero_rings, flowers="roses"),
    "inv-birthday-party": dict(pals=[PARTY, CANDY, SKY, MINT, PEACH], top=k_top_balloons, hero=k_hero_cake, flowers="flowers", confetti=True),
    "inv-griha-pravesh": dict(pals=[SAFFRON, EMERALD, TEAL, MAROON_GOLD, IVORY], top=k_top_toran, hero=k_hero_house, flowers="marigold"),
    "inv-baby-shower": dict(pals=[BLUSH, SKY, MINT, LILAC, PEACH], top=k_top_clouds, hero=k_hero_baby, flowers="flowers"),
    "inv-naming-ceremony": dict(pals=[SKY, BLUSH, LILAC, MINT, SUNRISE], top=k_top_stars, hero=k_hero_feet, flowers="flowers"),
    "inv-puja": dict(pals=[SAFFRON, MAROON_GOLD, EMERALD, ROYAL, TEAL], top=k_top_bells, hero=k_hero_kalash, flowers="marigold", tag="om"),
    "inv-shop-opening": dict(pals=[MAROON_GOLD, NAVY, EMERALD, PURPLE, SAFFRON], top=k_top_toran, hero=k_hero_ribbon, flowers="marigold", confetti=True),
    "shraddhanjali": dict(pals=[GREY, IVORY, NAVY, SAGE, IVORY], top=k_top_lilies, hero=k_hero_candle, flowers="lilies", sober=True),
    # festivals
    "navratri": dict(pals=[MAGENTA, SAFFRON, PURPLE, TEAL, MAROON_GOLD], top=k_top_toran, hero=k_hero_dandiya, flowers="marigold"),
    "dussehra": dict(pals=[SAFFRON, MAROON_GOLD, ROYAL, EMERALD, NAVY], top=k_top_toran, hero=k_hero_bow, flowers="marigold"),
    "karva-chauth": dict(pals=[KARVA, NAVY, MAGENTA, ROYAL, PURPLE], top=k_top_stars, hero=k_hero_sieve, flowers="roses"),
    "diwali": dict(pals=[PURPLE, MAROON_GOLD, NAVY, SAFFRON, EMERALD], top=k_top_lanterns, hero=k_hero_diya, flowers="marigold"),
    # occasions
    "birthday": dict(pals=[CANDY, PARTY, SKY, MINT, BLUSH], top=k_top_balloons, hero=k_hero_cake, flowers="flowers", confetti=True),
    "anniversary": dict(pals=[MAGENTA, BLUSH, NAVY, MAROON_GOLD, IVORY], top=k_top_lanterns, hero=k_hero_heart, flowers="roses"),
    "wedding": dict(pals=[MAROON_GOLD, ROYAL, EMERALD, BLUSH, SAGE], top=k_top_toran, hero=k_hero_kalash, flowers="roses"),
    "engagement": dict(pals=[BLUSH, LILAC, NAVY, SAGE, IVORY], top=k_top_lanterns, hero=k_hero_rings, flowers="roses"),
    "good-morning": dict(pals=[SUNRISE, SKY, MINT, PEACH, SAGE], top=k_top_clouds, hero=k_hero_sun, flowers="flowers"),
}


def corner_flowers(p, kit, x, y, sc, flip, rnd, fy=1):
    kind = kit["flowers"]
    if kind == "lilies":
        return f'<g transform="translate({x} {y}) scale({flip * sc} {fy * sc})">' + lily(60, 160, 1, -20, "#FFFFFF") + lily(150, 120, .8, 20, p["flower2"]) + leaf(20, 190, 110, -40, p["leaf"], .85) + leaf(120, 200, 90, 10, p["leaf"], .85) + "</g>"
    return floral_cluster(x, y, sc, p, flip, "roses" if kind == "roses" else ("marigold" if kind == "marigold" else "flowers"), kind == "flowers", rnd, fy)


def extras(p, kit, area=(60, 60, W - 60, H - 60), seed=1, dark=False):
    s = ""
    if kit.get("confetti"):
        s += confetti(70, [p["flower1"], p["flower2"], p["bg1"], "#FFD166"], seed, area)
    elif not kit.get("sober"):
        s += sparkles(14, "#FFE08A" if dark else p["accent"], seed, area, 16)
    return s


# ------------------------------------------------------------------ layouts: return (svg parts, spec)
LIGHT = lambda p: {"title": p["title"], "text": p["ink"], "accent": p["accent"]}
DARK = {"title": "gold", "text": "#FFF8EC", "accent": "#FFD36B"}


def L0_arch(p, kit, i):
    parts = [grad_bg(p["bg1"], p["bg2"]), corner_mandalas("#FFFFFF", 300, .16), mandala(540, 560, 520, "#FFFFFF", .08), texture(.6),
             "".join(bell(x, y, .8) for x, y in [(70, 260), (1010, 260)]),
             arch_window(150, 150, 780, 1090, p["paper"]), mandala(540, 1240, 260, p["accent"], .12),
             corner_flowers(p, kit, -30, H + 30, 1.5, 1, i, -1), corner_flowers(p, kit, W + 30, H + 30, 1.5, -1, i + 7, -1),
             corner_flowers(p, kit, 250, 240, .55, -1, i + 2), corner_flowers(p, kit, 830, 240, .55, 1, i + 4)]
    parts.append(mandala(540, 330, 70, p["accent"], .25))
    return parts, dict(zone=[230, 450, 850, 1160], align="center", colors=LIGHT(p), tone="light", title="deco", photo=dict(shape="circle", x=540, y=330, r=110))


def L1_classic(p, kit, i):
    parts = [rect_bg(p["paper"]), texture(1), mandala(540, 700, 430, p["frame"], .10), corner_mandalas(p["frame"], 210, .55, p["pastel1"]), double_frame(p["frame"]),
             corner_flowers(p, kit, 70, H - 70, .85, 1, i, -1), corner_flowers(p, kit, W - 70, H - 70, .85, -1, i + 1, -1), kit["hero"](p, 540, 250, .8)]
    return parts, dict(zone=[150, 400, 930, 1210], align="center", colors=LIGHT(p), tone="light", title="classic", photo=dict(shape="circle", x=540, y=250, r=105))


def L2_floral(p, kit, i):
    parts = [radial_bg(p["paper"], p["pastel1"]), texture(1),
             corner_flowers(p, kit, -40, -40, 2.3, 1, i), corner_flowers(p, kit, W + 40, H + 40, 2.3, -1, i + 3, -1),
             corner_flowers(p, kit, W + 20, -20, 1.0, -1, i + 5), corner_flowers(p, kit, -20, H + 20, 1.0, 1, i + 6, -1),
             extras(p, kit, (200, 300, 880, 1050), i)]
    return parts, dict(zone=[170, 420, 910, 1040], align="center", colors=LIGHT(p), tone="light", title="script", photo=dict(shape="circle", x=540, y=330, r=100))


def L3_dark(p, kit, i):
    parts = [radial_bg(p["dark1"], p["dark2"]), mandala(540, 675, 470, "#FFD36B", .16, None, 3),
             f'<rect x="60" y="60" width="{W - 120}" height="{H - 120}" rx="28" fill="none" stroke="url(#gold)" stroke-width="4"/>',
             f'<rect x="80" y="80" width="{W - 160}" height="{H - 160}" rx="20" fill="none" stroke="url(#gold)" stroke-width="1.5"/>',
             kit["top"](p) if kit["top"] in (k_top_lanterns, k_top_bells, k_top_stars) else "",
             extras(p, kit, (100, 300, W - 100, H - 120), i, True), kit["hero"](p, 540, 1150, .75),
             corner_mandalas("#FFD36B", 150, .35)]
    return parts, dict(zone=[150, 330, 930, 990], align="center", colors=DARK, tone="dark", title="deco", photo=dict(shape="circle", x=540, y=330, r=110))


def L4_medallion(p, kit, i):
    parts = [grad_bg(p["bg1"], p["bg2"], False), texture(.5)]
    parts.append("".join(paisley(x, y, .9, a, "#FFFFFF", "none").replace('stroke="#FFFFFF"', 'stroke="#FFFFFF" stroke-opacity=".18"').replace('fill="#FFFFFF"', 'fill="#FFFFFF" fill-opacity=".18"') for x, y, a in [(100, 120, 20), (930, 160, 200), (120, 1180, -40), (960, 1200, 150), (80, 650, 0), (1000, 700, 180)]))
    parts.append(circle_medallion(540, 690, 440, p["paper"]))
    parts.append(corner_flowers(p, kit, 150, 330, 1.0, 1, i))
    parts.append(corner_flowers(p, kit, 930, 1060, 1.0, -1, i + 3, -1))
    parts.append(kit["hero"](p, 540, 330, .55))
    return parts, dict(zone=[210, 440, 870, 1010], align="center", colors=LIGHT(p), tone="light", title="classic", photo=dict(shape="circle", x=540, y=350, r=95))


def L5_split(p, kit, i):
    parts = [rect_bg(p["paper"]), texture(1), f'<rect width="{W}" height="520" fill="{p["bg1"]}"/>', mandala(540, 250, 300, "#FFFFFF", .10),
             kit["top"](p) if kit["top"] not in (k_top_lilies,) else lily(540, 420, 1.3, 0), kit["hero"](p, 540, 330, .9) if kit["top"] not in (k_top_lilies,) else "", scallop_edge(520, p["paper"], 26, 16, True),
             corner_flowers(p, kit, W + 20, H + 20, 1.3, -1, i, -1), corner_flowers(p, kit, -20, H + 20, 1.0, 1, i + 2, -1)]
    return parts, dict(zone=[120, 640, 960, 1250], align="center", colors=LIGHT(p), tone="light", title="deco", photo=dict(shape="circle", x=540, y=520, r=120))


def L6_side(p, kit, i):
    parts = [rect_bg(p["paper"]), texture(1), f'<rect width="300" height="{H}" fill="{p["bg1"]}"/>',
             "".join(mandala(150, y, 95, "#FFFFFF", .22, None, 2) for y in (200, 520, 840, 1160)),
             f'<line x1="330" y1="80" x2="330" y2="{H - 80}" stroke="{p["frame"]}" stroke-width="3"/>',
             "".join(marigold(150, y, 16) for y in range(40, H, 60)) if kit["flowers"] == "marigold" else "",
             corner_flowers(p, kit, W + 20, -20, 1.4, -1, i), corner_flowers(p, kit, W + 20, H + 20, 1.1, -1, i + 3, -1)]
    return parts, dict(zone=[380, 330, 1010, 1230], align="left", colors=LIGHT(p), tone="light", title="classic", photo=dict(shape="rounded", x=380, y=110, w=200, h=200))


def L7_modern(p, kit, i):
    parts = [rect_bg(p["pastel1"]), f'<circle cx="930" cy="160" r="300" fill="{p["pastel2"]}"/>', f'<circle cx="80" cy="1260" r="330" fill="{p["bg1"]}" opacity=".18"/>',
             f'<circle cx="960" cy="1150" r="120" fill="{p["flower1"]}" opacity=".35"/>', f'<path d="M110 300 L380 300" stroke="{p["title"]}" stroke-width="8" stroke-linecap="round"/>',
             kit["hero"](p, 820, 1080, 1.0), corner_flowers(p, kit, W + 20, -20, 1.2, -1, i), extras(p, kit, (560, 700, 1040, 1300), i)]
    return parts, dict(zone=[110, 350, 900, 920], align="left", colors=LIGHT(p), tone="light", title="deco", photo=dict(shape="rounded", x=110, y=80, w=190, h=190))


def L8_hanging(p, kit, i):
    dark = not kit.get("sober")
    parts = [radial_bg(p["dark1"], p["dark2"]) if dark else radial_bg(p["paper"], p["pastel1"]), texture(.4),
             kit["top"](p), kit["hero"](p, 540, 1200, .9) if kit["hero"] not in (k_hero_house,) else kit["hero"](p, 540, 1120, .7),
             extras(p, kit, (100, 420, W - 100, 1050), i, dark)]
    return parts, dict(zone=[150, 400, 930, 1030], align="center", colors=DARK if dark else LIGHT(p), tone="dark" if dark else "light", title="script", photo=dict(shape="circle", x=540, y=400, r=100))


def L9_photo(p, kit, i):
    parts = [radial_bg(p["paper"], p["pastel2"]), texture(1),
             f'<path d="{arch_path(290, 110, 500, 600)}" fill="{p["pastel1"]}" stroke="url(#gold)" stroke-width="12" filter="url(#shadow)"/>',
             mandala(540, 460, 170, p["accent"], .35, None, 2),
             corner_flowers(p, kit, 200, 520, 1.1, 1, i), corner_flowers(p, kit, 880, 520, 1.1, -1, i + 5), corner_flowers(p, kit, 380, 160, .6, -1, i + 7), corner_flowers(p, kit, 700, 160, .6, 1, i + 8)]
    return parts, dict(zone=[140, 760, 940, 1260], align="center", colors=LIGHT(p), tone="light", title="classic",
                       photo=dict(shape="arch", x=302, y=122, w=476, h=576), slot=True)


LAYOUTS = [L0_arch, L1_classic, L2_floral, L3_dark, L4_medallion, L5_split, L6_side, L7_modern, L8_hanging, L9_photo]
TITLE_BY_CAT = {"shraddhanjali": {"script": "classic", "deco": "classic"}}


def build_svgs(only=None):
    specs = {}
    files = []
    for cat, kit in KITS.items():
        if only and cat not in only:
            continue
        specs[cat] = []
        for i, lay in enumerate(LAYOUTS):
            p = kit["pals"][i % len(kit["pals"])]
            parts, spec = lay(p, kit, i + 1)
            tid = f"T-{cat}-{i + 1}"
            spec["title"] = TITLE_BY_CAT.get(cat, {}).get(spec["title"], spec["title"])
            spec.update(id=tid, tpl=True)
            specs[cat].append(spec)
            files.append((tid, svg(parts)))
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


if __name__ == "__main__":
    only = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    specs, files = build_svgs(only)
    asyncio.run(render(files))
    path = os.path.join(ROOT, "content", "templates.json")
    allspecs = json.load(open(path)) if (only and os.path.exists(path)) else {}
    allspecs.update(specs)
    json.dump(allspecs, open(path, "w"), indent=1)
    print("rendered", len(files))
