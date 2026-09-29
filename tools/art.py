"""Vector art kit for card templates (1080x1350). Every function returns an SVG fragment string."""
import math, random

W, H = 1080, 1350


def defs(gold=("#FFF3C4", "#F2C14E", "#B7791F")):
    return f'''<defs>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{gold[0]}"/><stop offset=".5" stop-color="{gold[1]}"/><stop offset="1" stop-color="{gold[2]}"/></linearGradient>
<linearGradient id="goldv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{gold[0]}"/><stop offset=".55" stop-color="{gold[1]}"/><stop offset="1" stop-color="{gold[2]}"/></linearGradient>
<radialGradient id="flame" cx=".5" cy=".7" r=".6"><stop offset="0" stop-color="#FFFBE0"/><stop offset=".45" stop-color="#FFC94A"/><stop offset="1" stop-color="#FF6A00" stop-opacity="0"/></radialGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFE9A8" stop-opacity=".9"/><stop offset="1" stop-color="#FFE9A8" stop-opacity="0"/></radialGradient>
<filter id="paper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .07 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2"/></filter>
<filter id="wc" x="-30%" y="-30%" width="160%" height="160%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="3" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="14"/><feGaussianBlur stdDeviation="1.2"/></filter>
<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity=".25"/></filter>
</defs>'''


def rect_bg(c):
    return f'<rect width="{W}" height="{H}" fill="{c}"/>'


def grad_bg(c1, c2, vertical=True, gid="bgg"):
    x2, y2 = ("0", "1") if vertical else ("1", "1")
    return f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#{gid})"/>'


def radial_bg(c1, c2, gid="bgr", cx=.5, cy=.45):
    return f'<defs><radialGradient id="{gid}" cx="{cx}" cy="{cy}" r=".75"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></radialGradient></defs><rect width="{W}" height="{H}" fill="url(#{gid})"/>'


def texture(op=1):
    return f'<rect width="{W}" height="{H}" fill="#fff" filter="url(#paper)" opacity="{op}"/>'


def petal_ring(cx, cy, r, n, pl, pw, color, op=1, rot=0, stroke=None, sw=2):
    out = []
    for i in range(n):
        a = rot + 360 * i / n
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        out.append(f'<ellipse cx="{cx}" cy="{cy - r - pl / 2}" rx="{pw / 2}" ry="{pl / 2}" fill="{color}"{st} opacity="{op}" transform="rotate({a:.2f} {cx} {cy})"/>')
    return "".join(out)


def mandala(cx, cy, r, color, op=1, fill2=None, detail=3):
    """Concentric petal rings + dots."""
    g = [f'<g opacity="{op}">']
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r * .16}" fill="none" stroke="{color}" stroke-width="{max(1.5, r * .012)}"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r * .08}" fill="{color}"/>')
    rings = [(.2, 12, .16, .07), (.42, 16, .22, .085), (.7, 24, .24, .07), (.93, 36, .12, .045)][:detail + 1]
    for i, (rr, n, pl, pw) in enumerate(rings):
        col = fill2 if (fill2 and i % 2) else "none"
        g.append(petal_ring(cx, cy, r * rr, n, r * pl, r * pw, col, 1, 180 / n * (i % 2), color, max(1.2, r * .008)))
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{r * (rr + pl + .015)}" fill="none" stroke="{color}" stroke-width="{max(1, r * .006)}" stroke-dasharray="{r * .012} {r * .02}"/>')
    for i in range(36):
        a = math.radians(i * 10)
        g.append(f'<circle cx="{cx + math.cos(a) * r * 1.02:.1f}" cy="{cy + math.sin(a) * r * 1.02:.1f}" r="{max(1.5, r * .012):.1f}" fill="{color}"/>')
    g.append("</g>")
    return "".join(g)


def corner_mandalas(color, r=230, op=.9, fill2=None):
    return "".join(mandala(x, y, r, color, op, fill2) for x, y in [(0, 0), (W, 0), (0, H), (W, H)])


def double_frame(color, inset=46, gap=18, w1=5, w2=2, flourish=True):
    s = f'<rect x="{inset}" y="{inset}" width="{W - 2 * inset}" height="{H - 2 * inset}" fill="none" stroke="{color}" stroke-width="{w1}"/>'
    s += f'<rect x="{inset + gap}" y="{inset + gap}" width="{W - 2 * (inset + gap)}" height="{H - 2 * (inset + gap)}" fill="none" stroke="{color}" stroke-width="{w2}"/>'
    if flourish:
        for x, y, sx, sy in [(inset, inset, 1, 1), (W - inset, inset, -1, 1), (inset, H - inset, 1, -1), (W - inset, H - inset, -1, -1)]:
            s += f'<g transform="translate({x} {y}) scale({sx} {sy})" fill="none" stroke="{color}" stroke-width="3">'
            s += '<path d="M0 90 C 30 60, 60 30, 90 0"/><path d="M20 120 C 40 60, 60 40, 120 20"/><circle cx="46" cy="46" r="12"/><circle cx="46" cy="46" r="4" fill="' + color + '"/>'
            s += '<path d="M70 70 c 20 -10 40 -10 60 0 M70 70 c -10 20 -10 40 0 60"/></g>'
        for y, sy in [(inset, 1), (H - inset, -1)]:
            s += f'<g transform="translate({W / 2} {y}) scale(1 {sy})" fill="{color}"><path d="M-70 0 C -40 30, -15 30, 0 50 C 15 30, 40 30, 70 0 C 40 12, 15 14, 0 30 C -15 14, -40 12, -70 0z"/><circle cx="0" cy="62" r="6"/></g>'
    return s


def arch_path(x, y, w, h, cusp=.34):
    """Mughal-style pointed arch: rectangle body with ogee top."""
    top = y
    shoulder = y + h * cusp
    cx = x + w / 2
    return (f'M{x} {y + h} L{x} {shoulder} '
            f'C{x} {shoulder - h * .12} {x + w * .18} {top + h * .1} {cx - w * .1} {top + h * .045} '
            f'C{cx - w * .04} {top + h * .02} {cx} {top + h * .01} {cx} {top} '
            f'C{cx} {top + h * .01} {cx + w * .04} {top + h * .02} {cx + w * .1} {top + h * .045} '
            f'C{x + w - w * .18} {top + h * .1} {x + w} {shoulder - h * .12} {x + w} {shoulder} L{x + w} {y + h} Z')


def arch_window(x, y, w, h, fill, stroke="url(#gold)", sw=10, inner=True):
    p = arch_path(x, y, w, h)
    s = f'<path d="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" filter="url(#shadow)"/>'
    if inner:
        s += f'<path d="{arch_path(x + 22, y + 34, w - 44, h - 56)}" fill="none" stroke="{stroke}" stroke-width="2.5"/>'
    return s


def circle_medallion(cx, cy, r, fill, ring="url(#gold)"):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r + 26}" fill="none" stroke="{ring}" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{ring}" stroke-width="9" filter="url(#shadow)"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r - 18}" fill="none" stroke="{ring}" stroke-width="2"/>'
    return s


def scallop_edge(y, color, amp=26, n=18, flip=False):
    step = W / n
    d = f"M0 {y}"
    for i in range(n):
        x0 = i * step
        d += f" Q{x0 + step / 2} {y + (amp if not flip else -amp)} {x0 + step} {y}"
    d += f" L{W} {0 if not flip else H} L0 {0 if not flip else H} Z"
    return f'<path d="{d}" fill="{color}"/>'


def wave_band(y, color, amp=40, top=True):
    d = f"M0 {y} C {W * .25} {y + amp}, {W * .5} {y - amp}, {W * .75} {y + amp * .6} S {W} {y - amp * .2}, {W} {y}"
    d += f" L{W} {0 if top else H} L0 {0 if top else H} Z"
    return f'<path d="{d}" fill="{color}"/>'


# ---------------------------------------------------------------- botanicals
def leaf(x, y, l, a, color, op=1):
    return f'<path d="M0 0 C {l * .3} {-l * .22}, {l * .7} {-l * .22}, {l} 0 C {l * .7} {l * .22}, {l * .3} {l * .22}, 0 0Z" fill="{color}" opacity="{op}" transform="translate({x} {y}) rotate({a})"/><path d="M0 0 L{l * .9} 0" stroke="#ffffff" stroke-opacity=".35" stroke-width="1.5" transform="translate({x} {y}) rotate({a})"/>'


def flower(x, y, r, c, center="#FFD166", n=5, op=1, wc=False):
    f = ' filter="url(#wc)"' if wc else ""
    s = f'<g opacity="{op}"{f}>'
    for i in range(n):
        a = 360 * i / n
        s += f'<ellipse cx="{x}" cy="{y - r * .55}" rx="{r * .42}" ry="{r * .6}" fill="{c}" transform="rotate({a} {x} {y})"/>'
    s += f'<circle cx="{x}" cy="{y}" r="{r * .28}" fill="{center}"/></g>'
    return s


def rose(x, y, r, c, dark, op=1):
    s = f'<g opacity="{op}"><circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
    for k, rr in enumerate([.8, .6, .42, .26]):
        s += f'<path d="M{x - r * rr} {y} A {r * rr} {r * rr} 0 1 1 {x + r * rr * .6} {y + r * rr * .8}" fill="none" stroke="{dark}" stroke-width="{max(1.5, r * .07)}" stroke-linecap="round" transform="rotate({k * 70} {x} {y})"/>'
    return s + "</g>"


def marigold(x, y, r, c1="#FF9F1C", c2="#F77F00"):
    s = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c2}"/>'
    for i in range(14):
        a = math.radians(i * 360 / 14)
        s += f'<circle cx="{x + math.cos(a) * r * .62:.1f}" cy="{y + math.sin(a) * r * .62:.1f}" r="{r * .42:.1f}" fill="{c1}"/>'
    s += f'<circle cx="{x}" cy="{y}" r="{r * .45}" fill="{c1}"/><circle cx="{x}" cy="{y}" r="{r * .2}" fill="{c2}"/>'
    return s


def lily(x, y, s, a, c="#FFFFFF", edge="#D9D2C5"):
    g = f'<g transform="translate({x} {y}) rotate({a}) scale({s})">'
    for k in (-40, -14, 14, 40):
        g += f'<path d="M0 0 C -16 -40, -8 -92, 0 -120 C 8 -92, 16 -40, 0 0Z" fill="{c}" stroke="{edge}" stroke-width="2" transform="rotate({k})"/>'
    g += '<path d="M0 0 L -6 -60 M0 0 L 6 -60 M0 0 L0 -66" stroke="#C9A227" stroke-width="2"/><circle cx="-6" cy="-62" r="4" fill="#B5651D"/><circle cx="6" cy="-62" r="4" fill="#B5651D"/><circle cx="0" cy="-68" r="4" fill="#B5651D"/></g>'
    return g


def floral_cluster(x, y, scale, pal, flip=1, kind="flowers", wc=True, rnd=1, flipy=1):
    """Corner bouquet. pal: dict(flower1, flower2, leaf, center)."""
    random.seed(rnd)
    s = f'<g transform="translate({x} {y}) scale({flip * scale} {flipy * scale})">'
    for i in range(9):
        a = random.uniform(-20, 110)
        s += leaf(random.uniform(-20, 140), random.uniform(-20, 140), random.uniform(70, 120), a, pal["leaf"], .9)
    pts = [(40, 40, 52), (140, 20, 38), (20, 150, 40), (130, 120, 30), (210, 60, 26), (60, 230, 24)]
    for i, (px, py, r) in enumerate(pts):
        c = pal["flower1"] if i % 2 == 0 else pal["flower2"]
        if kind == "roses":
            s += rose(px, py, r, c, pal.get("dark", "#8B1030"))
        elif kind == "marigold":
            s += marigold(px, py, r * .8)
        else:
            s += flower(px, py, r, c, pal.get("center", "#FFD166"), 6 if i % 2 else 5, 1, wc)
    for i in range(10):
        s += f'<circle cx="{random.uniform(0, 260):.0f}" cy="{random.uniform(0, 260):.0f}" r="{random.uniform(3, 7):.1f}" fill="{pal.get("dot", pal["flower2"])}" opacity=".8"/>'
    return s + "</g>"


def toran(y, colors=("#FF9F1C", "#F77F00", "#FFD166"), leafc="#2D6A4F", drops=9):
    """Marigold garland scallops across the top with hanging strings."""
    s = ""
    n = 5
    step = W / n
    for i in range(n):
        x0 = i * step
        for k in range(15):
            t = k / 14
            px = x0 + step * t
            py = y + math.sin(math.pi * t) * 70
            s += marigold(px, py, 17, colors[0], colors[1])
        s += leaf(x0 + step / 2 - 10, y + 80, 46, 70, leafc) + leaf(x0 + step / 2 + 10, y + 80, 46, 110, leafc)
    for i in range(drops):
        x = W * (i + .5) / drops
        ln = 90 + (i % 3) * 40
        s += f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + ln}" stroke="{colors[1]}" stroke-width="3"/>'
        for k in range(4):
            s += marigold(x, y + 10 + k * ln / 4, 11, colors[k % 2], colors[1])
        s += f'<path d="M{x - 9} {y + ln} L{x} {y + ln + 26} L{x + 9} {y + ln}Z" fill="{leafc}"/>'
    return s


def diya(x, y, s=1, bowl="#B5541C", rim="#E09F3E"):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    g += '<ellipse cx="0" cy="-58" rx="60" ry="80" fill="url(#glow)"/>'
    g += f'<path d="M-62 0 C -52 34, 52 34, 62 0 Z" fill="{bowl}"/><ellipse cx="0" cy="0" rx="62" ry="12" fill="{rim}"/>'
    g += '<path d="M0 -62 C 14 -40, 12 -18, 0 -8 C -12 -18, -14 -40, 0 -62Z" fill="url(#flame)"/><path d="M0 -40 C 6 -28, 5 -18, 0 -12 C -5 -18, -6 -28, 0 -40Z" fill="#FFF8D6"/>'
    return g + "</g>"


def lantern(x, y, len_, c1, c2, s=1):
    g = f'<line x1="{x}" y1="0" x2="{x}" y2="{y}" stroke="{c2}" stroke-width="2.5"/>'
    g += f'<g transform="translate({x} {y}) scale({s})"><rect x="-20" y="-6" width="40" height="12" rx="3" fill="{c2}"/>'
    g += f'<path d="M-44 6 C -60 60, -40 110, 0 118 C 40 110, 60 60, 44 6 Z" fill="{c1}"/>'
    g += f'<path d="M-22 12 C -30 60, -20 100, 0 112 M22 12 C 30 60, 20 100, 0 112" stroke="{c2}" stroke-width="3" fill="none" opacity=".6"/>'
    g += '<ellipse cx="0" cy="60" rx="30" ry="40" fill="url(#glow)" opacity=".7"/>'
    g += f'<rect x="-16" y="116" width="32" height="10" rx="3" fill="{c2}"/><path d="M-10 126 L-14 168 M0 126 L0 176 M10 126 L14 168" stroke="{c1}" stroke-width="3"/></g>'
    return g


def bell(x, y, s, c="url(#gold)"):
    return f'<line x1="{x}" y1="0" x2="{x}" y2="{y}" stroke="#B7791F" stroke-width="2.5"/><g transform="translate({x} {y}) scale({s})"><path d="M-30 50 C -30 10, -18 0, 0 0 C 18 0, 30 10, 30 50 L 38 60 L -38 60 Z" fill="{c}"/><circle cx="0" cy="66" r="8" fill="{c}"/></g>'


def kalash(x, y, s=1, pot="url(#gold)", leafc="#2D6A4F"):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    for a in (-60, -35, -12, 12, 35, 60):
        g += leaf(0, -120, 90, -90 + a, leafc)
    g += '<ellipse cx="0" cy="-150" rx="38" ry="44" fill="#8B5A2B"/><path d="M-30 -168 C -10 -190, 10 -190, 30 -168" stroke="#5C3A1A" stroke-width="4" fill="none"/>'
    g += f'<path d="M-40 -118 L40 -118 L34 -100 C 90 -80, 90 20, 0 30 C -90 20, -90 -80, -34 -100 Z" fill="{pot}"/>'
    g += '<path d="M-62 -40 C -20 -30, 20 -30, 62 -40" stroke="#B80D4D" stroke-width="7" fill="none"/><circle cx="0" cy="-12" r="10" fill="#B80D4D"/>'
    return g + "</g>"


def balloon(x, y, r, c, string="#9CA3AF"):
    return (f'<path d="M{x} {y + r * 1.15} C {x - 20} {y + r * 1.8}, {x + 20} {y + r * 2.3}, {x} {y + r * 3}" stroke="{string}" stroke-width="2" fill="none"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 1.18}" fill="{c}"/><path d="M{x - 8} {y + r * 1.16} L{x + 8} {y + r * 1.16} L{x} {y + r * 1.06}Z" fill="{c}"/>'
            f'<ellipse cx="{x - r * .35}" cy="{y - r * .45}" rx="{r * .18}" ry="{r * .3}" fill="#fff" opacity=".45" transform="rotate(-25 {x - r * .35} {y - r * .45})"/>')


def confetti(n, colors, seed=2, area=(0, 0, W, H)):
    random.seed(seed)
    s = ""
    for _ in range(n):
        x = random.uniform(area[0], area[2]); y = random.uniform(area[1], area[3])
        c = random.choice(colors); a = random.uniform(0, 180)
        if random.random() < .5:
            s += f'<rect x="{x:.0f}" y="{y:.0f}" width="14" height="6" rx="2" fill="{c}" transform="rotate({a:.0f} {x:.0f} {y:.0f})"/>'
        else:
            s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(3, 7):.1f}" fill="{c}"/>'
    return s


def bunting(y, colors, n=11, sag=60):
    s = f'<path d="M0 {y} Q {W / 2} {y + sag * 2} {W} {y}" stroke="#6B7280" stroke-width="2.5" fill="none"/>'
    for i in range(n):
        t = (i + .5) / n
        x = W * t
        yy = y + 4 * sag * t * (1 - t)
        s += f'<path d="M{x - 36} {yy - 4} L{x + 36} {yy - 4} L{x} {yy + 70}Z" fill="{colors[i % len(colors)]}"/>'
    return s


def star(x, y, r, c, op=1):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * .45
        a = math.radians(-90 + i * 36)
        pts.append(f"{x + math.cos(a) * rr:.1f},{y + math.sin(a) * rr:.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{c}" opacity="{op}"/>'


def sparkle(x, y, r, c, op=1):
    return f'<path d="M{x} {y - r} C {x + r * .12} {y - r * .12}, {x + r * .12} {y - r * .12}, {x + r} {y} C {x + r * .12} {y + r * .12}, {x + r * .12} {y + r * .12}, {x} {y + r} C {x - r * .12} {y + r * .12}, {x - r * .12} {y + r * .12}, {x - r} {y} C {x - r * .12} {y - r * .12}, {x - r * .12} {y - r * .12}, {x} {y - r}Z" fill="{c}" opacity="{op}"/>'


def sparkles(n, c, seed=5, area=(60, 60, W - 60, H - 60), rmax=18):
    random.seed(seed)
    return "".join(sparkle(random.uniform(area[0], area[2]), random.uniform(area[1], area[3]), random.uniform(6, rmax), c, random.uniform(.5, 1)) for _ in range(n))


def moon(x, y, r, c="#FFF3C4", bg=None):
    s = f'<circle cx="{x}" cy="{y}" r="{r * 1.6}" fill="url(#glow)" opacity=".7"/><circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
    if bg:
        s += f'<circle cx="{x + r * .42}" cy="{y - r * .2}" r="{r * .9}" fill="{bg}"/>'
    return s


def cloud(x, y, s, c="#FFFFFF", op=1):
    return f'<g transform="translate({x} {y}) scale({s})" fill="{c}" opacity="{op}"><circle cx="0" cy="0" r="40"/><circle cx="45" cy="-18" r="52"/><circle cx="100" cy="0" r="40"/><rect x="0" y="0" width="100" height="40"/></g>'


def paisley(x, y, s, a, c, fill="none"):
    return f'<g transform="translate({x} {y}) rotate({a}) scale({s})"><path d="M0 0 C 60 -10, 90 60, 40 110 C 10 140, -50 120, -40 70 C -30 30, 20 40, 10 70" fill="{fill}" stroke="{c}" stroke-width="5"/><circle cx="12" cy="48" r="10" fill="{c}"/><path d="M-20 90 C 0 110, 30 105, 45 80" fill="none" stroke="{c}" stroke-width="3" stroke-dasharray="6 6"/></g>'


def rings(x, y, s, c="url(#gold)"):
    return f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{c}" stroke-width="10"><circle cx="-26" cy="0" r="46"/><circle cx="26" cy="0" r="46"/></g><g transform="translate({x - 26 * s} {y - 50 * s}) scale({s})">{sparkle(0, -10, 16, "#FFFFFF")}</g>'


def heart(x, y, s, c, op=1):
    return f'<path d="M{x} {y + 30 * s} C {x - 60 * s} {y - 10 * s}, {x - 30 * s} {y - 50 * s}, {x} {y - 20 * s} C {x + 30 * s} {y - 50 * s}, {x + 60 * s} {y - 10 * s}, {x} {y + 30 * s}Z" fill="{c}" opacity="{op}"/>'


def house(x, y, s, c, stroke_w=6):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{c}" stroke-width="{stroke_w}" stroke-linejoin="round" stroke-linecap="round">'
            '<path d="M-150 20 L0 -110 L150 20"/><path d="M-120 0 L-120 150 L120 150 L120 0"/><path d="M-30 150 L-30 60 L30 60 L30 150"/>'
            '<rect x="-95" y="30" width="45" height="45"/><rect x="50" y="30" width="45" height="45"/><path d="M80 -40 L80 -90 L105 -90 L105 -18"/></g>')


def key(x, y, s, a, c):
    return f'<g transform="translate({x} {y}) rotate({a}) scale({s})" fill="none" stroke="{c}" stroke-width="7"><circle cx="0" cy="0" r="26"/><path d="M26 0 L120 0 M95 0 L95 22 M112 0 L112 16"/></g>'


def ribbon_band(y, c1, c2, bow=True):
    s = f'<rect x="0" y="{y - 26}" width="{W}" height="52" fill="{c1}"/><rect x="0" y="{y - 26}" width="{W}" height="8" fill="{c2}" opacity=".5"/>'
    if bow:
        cx = W / 2
        s += f'<path d="M{cx} {y} C {cx - 140} {y - 120}, {cx - 190} {y + 40}, {cx} {y} C {cx + 190} {y + 40}, {cx + 140} {y - 120}, {cx} {y}Z" fill="{c1}" stroke="{c2}" stroke-width="4"/>'
        s += f'<path d="M{cx} {y} L{cx - 70} {y + 150} L{cx - 40} {y + 140} L{cx - 20} {y + 170}Z M{cx} {y} L{cx + 70} {y + 150} L{cx + 40} {y + 140} L{cx + 20} {y + 170}Z" fill="{c1}"/>'
        s += f'<circle cx="{cx}" cy="{y}" r="26" fill="{c2}"/>'
    return s


def scissors(x, y, s, c="url(#gold)"):
    return f'<g transform="translate({x} {y}) scale({s}) rotate(-30)" fill="none" stroke="{c}" stroke-width="9"><circle cx="-40" cy="60" r="28"/><circle cx="40" cy="60" r="28"/><path d="M-22 40 L60 -120 M22 40 L-60 -120"/></g>'


def cake(x, y, s, c1="#FFB3C7", c2="#FFFFFF", c3="#E0115F"):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    g += f'<rect x="-130" y="-60" width="260" height="120" rx="18" fill="{c1}"/><path d="M-130 -40 C -100 -10, -70 -10, -40 -40 C -10 -10, 20 -10, 50 -40 C 80 -10, 110 -10, 130 -40 L130 -60 L-130 -60Z" fill="{c2}"/>'
    g += f'<rect x="-90" y="-150" width="180" height="92" rx="14" fill="{c2}"/><path d="M-90 -130 C -60 -105, -30 -105, 0 -130 C 30 -105, 60 -105, 90 -130 L90 -150 L-90 -150Z" fill="{c1}"/>'
    for cx in (-40, 0, 40):
        g += f'<rect x="{cx - 6}" y="-200" width="12" height="52" rx="4" fill="{c3}"/>' + f'<path d="M{cx} -232 C {cx + 10} -216, {cx + 8} -206, {cx} -202 C {cx - 8} -206, {cx - 10} -216, {cx} -232Z" fill="url(#flame)"/>'
    g += '<rect x="-160" y="60" width="320" height="16" rx="8" fill="#E5E7EB"/></g>'
    return g


def dandiya(x, y, s, a, c1="#E0115F", c2="#FFC94A"):
    g = f'<g transform="translate({x} {y}) rotate({a}) scale({s})"><rect x="-8" y="-170" width="16" height="340" rx="8" fill="{c1}"/>'
    for k in range(-150, 170, 34):
        g += f'<rect x="-9" y="{k}" width="18" height="10" fill="{c2}"/>'
    return g + f'<circle cx="0" cy="-176" r="12" fill="{c2}"/><circle cx="0" cy="176" r="12" fill="{c2}"/></g>'


def garbo(x, y, s):
    g = f'<g transform="translate({x} {y}) scale({s})"><path d="M-70 -80 L70 -80 C 130 -40, 130 80, 0 110 C -130 80, -130 -40, -70 -80Z" fill="#B5541C"/>'
    random.seed(9)
    for i in range(26):
        g += f'<circle cx="{random.uniform(-85, 85):.0f}" cy="{random.uniform(-50, 85):.0f}" r="7" fill="#FFD166"/>'
    g += '<rect x="-74" y="-96" width="148" height="20" rx="6" fill="#E09F3E"/><ellipse cx="0" cy="-110" rx="40" ry="46" fill="url(#glow)"/><path d="M0 -150 C 10 -134, 9 -118, 0 -110 C -9 -118, -10 -134, 0 -150Z" fill="url(#flame)"/></g>'
    return g


def bow_arrow(x, y, s, c="url(#gold)"):
    return f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{c}" stroke-width="8" stroke-linecap="round"><path d="M-60 -200 C 60 -120, 60 120, -60 200"/><path d="M-60 -200 L-60 200" stroke-width="3"/><path d="M-120 0 L120 0"/><path d="M120 0 L96 -16 M120 0 L96 16"/><path d="M-120 0 L-140 -16 M-120 0 L-140 16"/></g>'


def sieve(x, y, s, c="url(#gold)"):
    g = f'<g transform="translate({x} {y}) scale({s})"><circle r="110" fill="#8B1E3F" stroke="{c}" stroke-width="12"/><circle r="92" fill="none" stroke="{c}" stroke-width="3"/>'
    for i in range(-80, 90, 16):
        g += f'<line x1="{i}" y1="-90" x2="{i}" y2="90" stroke="#E8C87A" stroke-width="1.2" opacity=".7"/><line x1="-90" y1="{i}" x2="90" y2="{i}" stroke="#E8C87A" stroke-width="1.2" opacity=".7"/>'
    return g + "</g>"


def fireworks(x, y, r, c, rays=18, seed=1):
    random.seed(seed)
    s = ""
    for i in range(rays):
        a = math.radians(i * 360 / rays + random.uniform(-4, 4))
        l = r * random.uniform(.7, 1)
        s += f'<line x1="{x + math.cos(a) * r * .2:.0f}" y1="{y + math.sin(a) * r * .2:.0f}" x2="{x + math.cos(a) * l:.0f}" y2="{y + math.sin(a) * l:.0f}" stroke="{c}" stroke-width="3" stroke-linecap="round"/><circle cx="{x + math.cos(a) * l:.0f}" cy="{y + math.sin(a) * l:.0f}" r="4" fill="{c}"/>'
    return s


def sun(x, y, r, c="#FFC94A", rays="#FFB703"):
    s = ""
    for i in range(16):
        a = i * 22.5
        s += f'<rect x="{x - 6}" y="{y - r * 1.7}" width="12" height="{r * .45}" rx="6" fill="{rays}" transform="rotate({a} {x} {y})"/>'
    return s + f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def cup(x, y, s, c="#B5541C"):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M-70 -60 L70 -60 L56 60 C 50 80, -50 80, -56 60Z" fill="{c}"/><ellipse cx="0" cy="-60" rx="70" ry="16" fill="#E9C46A"/><ellipse cx="0" cy="-60" rx="58" ry="10" fill="#C08552"/><path d="M-20 -90 C -40 -120, 0 -140, -20 -170 M20 -90 C 0 -120, 40 -140, 20 -170" stroke="#FFFFFF" stroke-width="5" fill="none" opacity=".7"/></g>'


def footprint(x, y, s, a, c):
    g = f'<g transform="translate({x} {y}) rotate({a}) scale({s})" fill="{c}"><ellipse cx="0" cy="0" rx="26" ry="40"/>'
    for i, (dx, dy, r) in enumerate([(-22, -50, 8), (-8, -58, 9), (8, -58, 9), (22, -50, 8), (32, -36, 7)]):
        g += f'<circle cx="{dx}" cy="{dy}" r="{r}"/>'
    return g + "</g>"


def candle(x, y, s, c="#FFFFFF"):
    return f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="-150" rx="50" ry="70" fill="url(#glow)"/><rect x="-26" y="-110" width="52" height="170" rx="8" fill="{c}" stroke="#E5DFD3" stroke-width="3"/><path d="M0 -150 C 12 -130, 10 -116, 0 -108 C -10 -116, -12 -130, 0 -150Z" fill="url(#flame)"/></g>'


def svg(parts, gold=None):
    body = "".join(parts)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs(gold) if gold else defs()}{body}</svg>'


# ================================================================ event-specific motifs (v2)
def rangoli(cx, cy, r, colors, op=1):
    """Filled colourful rangoli (top view)."""
    s = f'<g opacity="{op}">'
    rings = [(.95, 32, .16, .07), (.72, 20, .26, .11), (.46, 14, .24, .12), (.22, 8, .2, .12)]
    for i, (rr, n, pl, pw) in enumerate(rings):
        s += f'<circle cx="{cx}" cy="{cy}" r="{r * (rr + .02)}" fill="{colors[(i + 1) % len(colors)]}" opacity=".35"/>'
        s += petal_ring(cx, cy, r * (rr - pl), n, r * pl, r * pw, colors[i % len(colors)], 1, 180 / n * (i % 2))
    s += f'<circle cx="{cx}" cy="{cy}" r="{r * .12}" fill="{colors[0]}"/><circle cx="{cx}" cy="{cy}" r="{r * .05}" fill="#FFF3C4"/>'
    for i in range(24):
        a = math.radians(i * 15)
        s += f'<circle cx="{cx + math.cos(a) * r:.1f}" cy="{cy + math.sin(a) * r:.1f}" r="{r * .03:.1f}" fill="{colors[-1]}"/>'
    return s + "</g>"


def diya_row(y, n, s=.7, x0=90, x1=W - 90):
    return "".join(diya(x0 + (x1 - x0) * i / max(1, n - 1), y, s) for i in range(n))


def akash_kandil(x, y, s, c1, c2):
    """Star-shaped sky lantern with tassels."""
    g = f'<line x1="{x}" y1="0" x2="{x}" y2="{y - 70 * s}" stroke="#C9973B" stroke-width="2.5"/><g transform="translate({x} {y}) scale({s})">'
    g += '<circle r="70" fill="url(#glow)"/>' + star(0, 0, 70, c1) + star(0, 0, 38, c2) + f'<circle r="12" fill="#FFF3C4"/>'
    for dx in (-30, -10, 10, 30):
        g += f'<path d="M{dx} 40 L{dx * 1.1} 130" stroke="{c1}" stroke-width="4"/><circle cx="{dx * 1.1}" cy="134" r="5" fill="{c2}"/>'
    return g + "</g>"


def lotus(x, y, s, c="#F4A6C1", c2="#E56B8F", leafc="#3A7D44"):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    g += f'<ellipse cx="0" cy="20" rx="120" ry="18" fill="{leafc}" opacity=".85"/>'
    for a, l, col in [(-70, 80, c), (70, 80, c), (-40, 105, c2), (40, 105, c2), (-15, 120, c), (15, 120, c), (0, 128, c2)]:
        g += f'<path d="M0 10 C -26 -{l * .45}, -10 -{l * .9}, 0 -{l} C 10 -{l * .9}, 26 -{l * .45}, 0 10Z" fill="{col}" stroke="#FFFFFF" stroke-opacity=".5" stroke-width="2" transform="rotate({a * .8})"/>'
    return g + "</g>"


def garland_frame(x, y, w, h, shape="rect", c1="#FFFFFF", c2="#F2C14E", r=13, leafc="#6B8F71"):
    """Flower garland (haar) around a photo frame, with a hanging loop at the bottom."""
    pts = []
    if shape == "oval":
        cx, cy, rx, ry = x + w / 2, y + h / 2, w / 2 + 18, h / 2 + 18
        n = int(2 * math.pi * max(rx, ry) / (r * 1.6))
        pts = [(cx + math.cos(2 * math.pi * i / n) * rx, cy + math.sin(2 * math.pi * i / n) * ry) for i in range(n)]
    else:
        per = 2 * (w + h) + 144
        n = int(per / (r * 1.6))
        for i in range(n):
            d = per * i / n
            X, Y = x - 18, y - 18
            ww, hh = w + 36, h + 36
            if d < ww: pts.append((X + d, Y))
            elif d < ww + hh: pts.append((X + ww, Y + d - ww))
            elif d < 2 * ww + hh: pts.append((X + ww - (d - ww - hh), Y + hh))
            else: pts.append((X, Y + hh - (d - 2 * ww - hh)))
    s = ""
    for i, (px, py) in enumerate(pts):
        s += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="{c1 if i % 3 else c2}" stroke="#E5DCC8" stroke-width="1"/>'
    bx, by = x + w / 2, y + h + 18
    for k in range(9):
        t = k / 8
        s += f'<circle cx="{bx - 60 + 120 * t:.0f}" cy="{by + math.sin(math.pi * t) * 70:.0f}" r="{r}" fill="{c1 if k % 2 else c2}"/>'
    s += leaf(bx - 20, by + 76, 40, 100, leafc) + leaf(bx + 20, by + 76, 40, 80, leafc)
    return s


def hanging_diya(x, y, s=1, chain="#B7791F"):
    g = f'<path d="M{x} 0 L{x} {y - 60 * s}" stroke="{chain}" stroke-width="3" stroke-dasharray="8 5"/>'
    g += f'<path d="M{x} {y - 60 * s} L{x - 50 * s} {y - 6 * s} M{x} {y - 60 * s} L{x + 50 * s} {y - 6 * s}" stroke="{chain}" stroke-width="2"/>'
    return g + diya(x, y, s)


def mandap(x, y, s, c="url(#gold)", drape="#C9184A", flower="#FF9F1C"):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    g += f'<path d="M-230 -260 C -150 -380, 150 -380, 230 -260 Z" fill="{drape}" stroke="{c}" stroke-width="6"/>'
    g += f'<path d="M-240 -260 L240 -260" stroke="{c}" stroke-width="12"/>'
    for px in (-220, 220):
        g += f'<rect x="{px - 12}" y="-260" width="24" height="300" fill="{c}"/><rect x="{px - 24}" y="30" width="48" height="16" fill="{c}"/>'
        g += f'<path d="M{px} -250 C {px + (60 if px < 0 else -60)} -150, {px + (40 if px < 0 else -40)} -60, {px + (70 if px < 0 else -70)} 20" stroke="{drape}" stroke-width="18" fill="none" opacity=".85"/>'
    for i in range(-200, 210, 40):
        g += f'<line x1="{i}" y1="-258" x2="{i}" y2="{-200 - (abs(i) % 80)}" stroke="{flower}" stroke-width="3"/><circle cx="{i}" cy="{-196 - (abs(i) % 80)}" r="8" fill="{flower}"/>'
    g += '<path d="M-60 40 L0 -10 L60 40 Z" fill="#FF6A00" opacity=".8"/><rect x="-80" y="36" width="160" height="16" fill="#8B5A2B"/>'
    return g + "</g>"


def swastik(x, y, s, c="#C1121F"):
    return (f'<g transform="translate({x} {y}) scale({s})" stroke="{c}" stroke-width="10" stroke-linecap="round" fill="none">'
            '<path d="M0 -50 L0 50 M-50 0 L50 0 M0 -50 L40 -50 M50 0 L50 40 M0 50 L-40 50 M-50 0 L-50 -40"/>'
            f'<circle cx="-25" cy="-25" r="6" fill="{c}" stroke="none"/><circle cx="25" cy="-25" r="6" fill="{c}" stroke="none"/><circle cx="-25" cy="25" r="6" fill="{c}" stroke="none"/><circle cx="25" cy="25" r="6" fill="{c}" stroke="none"/></g>')


def thali(x, y, s, plate="url(#gold)"):
    g = f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="0" rx="170" ry="60" fill="{plate}" stroke="#9C6B1E" stroke-width="4"/><ellipse cx="0" cy="-6" rx="140" ry="44" fill="#F6D776" opacity=".6"/>'
    g += '<ellipse cx="-80" cy="-10" rx="26" ry="10" fill="#C1121F"/><ellipse cx="80" cy="-10" rx="26" ry="10" fill="#F4C430"/>'
    g += marigold(-30, 16, 14) + marigold(40, 20, 12)
    return g + diya(0, -20, .6) + "</g>"


def karwa(x, y, s, c="#B5541C", deco="#FFD166"):
    g = f'<g transform="translate({x} {y}) scale({s})"><path d="M-70 -60 C -120 20, -80 90, 0 96 C 80 90, 120 20, 70 -60 Z" fill="{c}"/>'
    g += f'<path d="M60 -30 C 110 -40, 140 -70, 150 -100" stroke="{c}" stroke-width="18" fill="none" stroke-linecap="round"/>'
    g += f'<ellipse cx="0" cy="-62" rx="72" ry="16" fill="#8B3A0F"/><path d="M-80 10 C -30 30, 30 30, 80 10" stroke="{deco}" stroke-width="6" fill="none"/>'
    for i in range(-60, 70, 24):
        g += f'<circle cx="{i}" cy="40" r="6" fill="{deco}"/>'
    return g + "</g>"


def mehendi_border(y, c, flip=False):
    """Paisley/mehendi lace strip."""
    s = f'<g transform="translate(0 {y}) scale(1 {-1 if flip else 1})">'
    for i in range(12):
        x = 45 + i * 90
        s += paisley(x, 0, .45, 180, c, "none")
        s += f'<circle cx="{x + 45}" cy="30" r="5" fill="{c}"/>'
    s += f'<path d="M0 70 L{W} 70" stroke="{c}" stroke-width="3" stroke-dasharray="2 8" stroke-linecap="round"/></g>'
    return s


def peacock_feather(x, y, s, a):
    g = f'<g transform="translate({x} {y}) rotate({a}) scale({s})"><path d="M0 200 C 4 100, 4 40, 0 -40" stroke="#6B8F3E" stroke-width="4" fill="none"/>'
    for i in range(14):
        yy = 180 - i * 14
        g += f'<path d="M0 {yy} C -40 {yy - 30}, -60 {yy - 50}, -70 {yy - 70}" stroke="#2A9D8F" stroke-width="2" fill="none" opacity=".7"/><path d="M0 {yy} C 40 {yy - 30}, 60 {yy - 50}, 70 {yy - 70}" stroke="#2A9D8F" stroke-width="2" fill="none" opacity=".7"/>'
    g += '<ellipse cx="0" cy="-60" rx="46" ry="62" fill="#1B998B"/><ellipse cx="0" cy="-54" rx="30" ry="40" fill="#F2C14E"/><ellipse cx="0" cy="-50" rx="18" ry="24" fill="#264653"/><ellipse cx="0" cy="-46" rx="8" ry="11" fill="#2A9D8F"/>'
    return g + "</g>"


def cradle(x, y, s, c="url(#gold)", cloth="#F7C6D0"):
    g = f'<g transform="translate({x} {y}) scale({s})"><path d="M-200 -260 L200 -260" stroke="{c}" stroke-width="12"/>'
    g += f'<path d="M-150 -260 L-120 -40 M150 -260 L120 -40" stroke="{c}" stroke-width="4"/>'
    g += f'<path d="M-160 -40 C -140 60, 140 60, 160 -40 Z" fill="{cloth}" stroke="{c}" stroke-width="6"/>'
    for i in range(-200, 210, 50):
        g += marigold(i, -262, 12)
    g += '<path d="M-120 -10 C -60 20, 60 20, 120 -10" stroke="#FFFFFF" stroke-width="5" fill="none" opacity=".7"/>'
    return g + "</g>"


def bangles(x, y, s, colors=("#C1121F", "#2D6A4F", "#F2C14E")):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    for i, c in enumerate(colors * 2):
        g += f'<ellipse cx="{i * 14 - 35}" cy="0" rx="60" ry="72" fill="none" stroke="{c}" stroke-width="9"/>'
    return g + "</g>"


def banana_leaf(x, y, s, a, c="#4C8C2B"):
    g = f'<g transform="translate({x} {y}) rotate({a}) scale({s})"><path d="M0 0 C 60 -120, 70 -320, 0 -460 C -70 -320, -60 -120, 0 0Z" fill="{c}"/>'
    g += '<path d="M0 0 L0 -450" stroke="#2F5D1B" stroke-width="5"/>'
    for i in range(1, 16):
        yy = -i * 28
        g += f'<path d="M0 {yy} L{38 - abs(i - 8) * 2} {yy - 26} M0 {yy} L-{38 - abs(i - 8) * 2} {yy - 26}" stroke="#2F5D1B" stroke-width="1.5" opacity=".6"/>'
    return g + "</g>"


def havan(x, y, s):
    g = f'<g transform="translate({x} {y}) scale({s})"><path d="M-120 0 L120 0 L96 60 L-96 60 Z" fill="#8B5A2B"/><path d="M-96 60 L96 60 L80 100 L-80 100 Z" fill="#6B4423"/>'
    g += '<ellipse cx="0" cy="-60" rx="110" ry="120" fill="url(#glow)"/>'
    for dx, h in [(-50, 90), (0, 140), (50, 100)]:
        g += f'<path d="M{dx} 0 C {dx + 30} -{h * .4}, {dx + 10} -{h * .7}, {dx} -{h} C {dx - 10} -{h * .7}, {dx - 30} -{h * .4}, {dx} 0Z" fill="url(#flame)"/>'
    return g + "</g>"


def storefront(x, y, s, awning=("#C1121F", "#FFFFFF"), wall="#FFF3E0"):
    g = f'<g transform="translate({x} {y}) scale({s})"><rect x="-230" y="-120" width="460" height="300" fill="{wall}" stroke="#8B5A2B" stroke-width="5"/>'
    for i in range(8):
        g += f'<path d="M{-240 + i * 60} -120 L{-180 + i * 60} -120 L{-180 + i * 60} -60 C {-195 + i * 60} -40, {-225 + i * 60} -40, {-240 + i * 60} -60Z" fill="{awning[i % 2]}"/>'
    g += '<rect x="-240" y="-190" width="480" height="70" rx="10" fill="#1B2A4A"/><rect x="-60" y="10" width="120" height="170" fill="#8B5A2B"/><rect x="-190" y="0" width="100" height="90" fill="#BDE0FE"/><rect x="90" y="0" width="100" height="90" fill="#BDE0FE"/>'
    return g + "</g>"


def coins(x, y, s):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    for i in range(6):
        g += f'<ellipse cx="{(i % 2) * 10}" cy="{-i * 16}" rx="60" ry="18" fill="url(#gold)" stroke="#9C6B1E" stroke-width="3"/>'
    g += '<ellipse cx="90" cy="0" rx="60" ry="18" fill="url(#gold)" stroke="#9C6B1E" stroke-width="3"/><ellipse cx="90" cy="-16" rx="60" ry="18" fill="url(#gold)" stroke="#9C6B1E" stroke-width="3"/>'
    return g + "</g>"


def gift(x, y, s, c, rib="#FFD166"):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-60" y="-50" width="120" height="100" rx="8" fill="{c}"/><rect x="-66" y="-66" width="132" height="24" rx="6" fill="{c}"/>'
            f'<rect x="-10" y="-66" width="20" height="116" fill="{rib}"/><path d="M0 -66 C -40 -110, -70 -80, 0 -66 C 70 -80, 40 -110, 0 -66Z" fill="{rib}"/></g>')


def party_hat(x, y, s, a, c1, c2):
    return (f'<g transform="translate({x} {y}) rotate({a}) scale({s})"><path d="M-50 60 L0 -90 L50 60 Z" fill="{c1}"/>'
            f'<path d="M-34 10 L34 10 M-20 -30 L20 -30" stroke="{c2}" stroke-width="10"/><circle cx="0" cy="-96" r="14" fill="{c2}"/></g>')


def apta_leaf(x, y, s, a, c="#4C8C2B"):
    return f'<g transform="translate({x} {y}) rotate({a}) scale({s})"><path d="M0 60 C -70 20, -70 -50, -20 -60 C -8 -62, 0 -50, 0 -40 C 0 -50, 8 -62, 20 -60 C 70 -50, 70 20, 0 60Z" fill="{c}"/><path d="M0 60 L0 -40" stroke="#2F5D1B" stroke-width="3"/><path d="M0 60 L0 110" stroke="#6B4423" stroke-width="5"/></g>'


def flaming_arrow(x, y, s, a):
    return (f'<g transform="translate({x} {y}) rotate({a}) scale({s})"><path d="M-260 0 L200 0" stroke="#6B4423" stroke-width="8"/><path d="M200 -22 L260 0 L200 22 Z" fill="url(#gold)"/>'
            '<path d="M-260 0 L-300 -24 M-260 0 L-300 24 M-240 0 L-280 -24 M-240 0 L-280 24" stroke="#C1121F" stroke-width="6"/>'
            '<path d="M150 0 C 180 -60, 220 -70, 250 -40 C 230 -30, 240 -20, 260 0 C 240 20, 230 30, 250 40 C 220 70, 180 60, 150 0Z" fill="url(#flame)" opacity=".95"/></g>')


def birds(x, y, s, c="#3A3A3A"):
    return "".join(f'<path d="M{x + dx} {y + dy} q 14 -14 28 0 q 14 -14 28 0" stroke="{c}" stroke-width="{3 * s}" fill="none" stroke-linecap="round" transform="scale(1)"/>' for dx, dy in [(0, 0), (70, -30), (140, 10), (40, 50)])


def sunflower(x, y, r):
    return petal_ring(x, y, r * .45, 16, r * .6, r * .28, "#FFC300", 1) + f'<circle cx="{x}" cy="{y}" r="{r * .45}" fill="#6B3E26"/>' + "".join(f'<circle cx="{x + math.cos(i) * r * .25:.1f}" cy="{y + math.sin(i) * r * .25:.1f}" r="3" fill="#3E2415"/>' for i in range(0, 20))


def hills(y, c1, c2):
    return (f'<path d="M0 {y} C 200 {y - 120}, 400 {y - 60}, 560 {y - 20} C 720 {y - 140}, 900 {y - 80}, {W} {y - 40} L{W} {H} L0 {H} Z" fill="{c1}"/>'
            f'<path d="M0 {y + 70} C 300 {y - 20}, 600 {y + 80}, {W} {y + 20} L{W} {H} L0 {H} Z" fill="{c2}"/>')


def heart_frame_path(x, y, w, h):
    cx = x + w / 2
    return f'M{cx} {y + h} C {x - w * .2} {y + h * .55}, {x} {y - h * .05}, {cx} {y + h * .22} C {x + w} {y - h * .05}, {x + w * 1.2} {y + h * .55}, {cx} {y + h}Z'


def dancers(y, c, n=5):
    """Simple garba dancer silhouettes (abstract, faceless)."""
    s = ""
    for i in range(n):
        x = 120 + i * (W - 240) / (n - 1)
        s += (f'<g transform="translate({x} {y}) scale({1 if i % 2 else -1} 1)" fill="{c}"><circle cx="0" cy="-150" r="18"/>'
              '<path d="M-10 -130 L10 -130 L20 -60 L-20 -60Z"/><path d="M-20 -60 C -70 -10, -80 20, -90 30 L90 30 C 80 20, 70 -10, 20 -60Z"/>'
              '<path d="M-10 -120 L-60 -170 M10 -120 L50 -80" stroke="' + c + '" stroke-width="8" stroke-linecap="round"/>'
              '<path d="M-60 -170 L-40 -200 M50 -80 L80 -110" stroke="#FFD166" stroke-width="6" stroke-linecap="round"/></g>')
    return s
