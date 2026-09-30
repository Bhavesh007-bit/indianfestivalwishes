"""Dussehra motifs (agent A): 10-headed Ravan effigy, fire, sparks, Ram archer, flaming arrow,
bow, apta/shami leaves, dhwaj, chariot, crowd."""
import math
from lib_a import f, pts, rr, sparkle, W, H

GOLDS = [(0, "#6E3F07"), (0.28, "#C8871E"), (0.5, "#FFE7A0"), (0.72, "#D39A2C"), (1, "#6E3F07")]


def gld(c, v=False):
    return c.lg(GOLDS, 0, 0, 0, 1) if v else c.lg(GOLDS, 0, 0, 1, 1)


# ------------------------------------------------------------------ fire
def flame_path(x, y, w, h, lean=0.0, k=0):
    """Single tongue of flame, base centre (x,y)."""
    tipx = x + lean * h
    return ("M%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s Z" % (
        f(x - w / 2), f(y),
        f(x - w * 0.62), f(y - h * 0.38), f(x - w * 0.1 + lean * h * 0.4), f(y - h * 0.55), f(tipx), f(y - h),
        f(x + w * 0.05 + lean * h * 0.5), f(y - h * 0.62), f(x + w * 0.62), f(y - h * 0.4), f(x + w / 2), f(y),
        f(x + w * 0.2), f(y + w * 0.12), f(x - w * 0.2), f(y + w * 0.12), f(x - w / 2), f(y)))


def fire(c, cx, base, width, height, n=None, glow=True, intensity=1.0, logs=True):
    """Blazing fire: heat glow, blurred halo, 4 gradient flame layers, white-hot core, embers/logs at the base."""
    rnd = c.rnd
    n = n or max(5, int(width / 38))
    out = []
    if glow:
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (
            f(cx), f(base - height * 0.45), f(width * 1.1), f(height * 1.0),
            c.rg([(0, "#FFB300", 0.55 * intensity), (0.5, "#FF5A00", 0.22 * intensity), (1, "#FF3D00", 0)])))
    tongues = []
    for i in range(n):
        t = (i + 0.5) / n
        x = cx - width / 2 + width * t
        env = math.sin(math.pi * t) ** 0.8
        h = height * (0.35 + 0.65 * env) * rnd.uniform(0.7, 1.12)
        w = width / n * rnd.uniform(1.6, 2.4)
        lean = rnd.uniform(-0.16, 0.16)
        tongues.append((x, h, w, lean))
    layers = [
        ([(0, "#7F0000"), (0.45, "#D32F2F"), (1, "#FF6D00")], 1.0, 1.0),
        ([(0, "#E64A19"), (0.5, "#FF8F00"), (1, "#FFB300")], 0.8, 0.8),
        ([(0, "#FFA000"), (0.5, "#FFD54F"), (1, "#FFF59D")], 0.6, 0.58),
        ([(0, "#FFF59D"), (1, "#FFFFFF")], 0.36, 0.34),
    ]
    outer = " ".join(flame_path(x, base, w, h, lean) for x, h, w, lean in tongues)
    out.append('<path d="%s" fill="#FF6D00" opacity="0.75" filter="%s"/>' % (outer, c.blur(max(6, width / 40))))
    for stops, ws, hs in layers:
        d = " ".join(flame_path(x + lean * h * 0.08, base, w * ws, h * hs, lean) for x, h, w, lean in tongues)
        out.append('<path d="%s" fill="%s"/>' % (d, c.lg(stops, 0, 0, 0, 1)))
    for _ in range(max(3, n // 2)):
        x = cx + rnd.uniform(-width * 0.38, width * 0.38)
        y = base - height * rnd.uniform(0.55, 0.95)
        out.append('<path d="%s" fill="%s" opacity="0.9"/>' % (flame_path(x, y, width * 0.05, height * 0.2, rnd.uniform(-0.3, 0.3)),
                                                             rnd.choice(("#FF7043", "#FFA726", "#FFCA28"))))
    if logs:
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (f(cx), f(base + 6), f(width * 0.55), f(width * 0.06),
                                                                         c.rg([(0, "#FFCC80"), (0.4, "#E65100"), (1, "#3E0D00")])))
        for k in range(-3, 4):
            out.append('<path d="M%s,%s L%s,%s" stroke="#2B0B02" stroke-width="%s" stroke-linecap="round"/>' % (
                f(cx + k * width * 0.08 - width * 0.06), f(base + 12), f(cx + k * width * 0.06 + width * 0.05), f(base - 6), f(width * 0.025)))
    return "".join(out)


def sparks(c, box, n, colors=("#FFE082", "#FFB300", "#FF7043", "#FFF8E1"), rmax=3.8, streak=True):
    x0, y0, x1, y1 = box
    rnd = c.rnd
    out = []
    for _ in range(n):
        x = rnd.uniform(x0, x1); y = rnd.uniform(y0, y1)
        r = rnd.uniform(1, rmax)
        col = rnd.choice(colors)
        if streak and rnd.random() < 0.45:
            L = rnd.uniform(8, 26)
            a = math.radians(rnd.uniform(-115, -65))
            out.append('<path d="M%s,%s l%s,%s" stroke="%s" stroke-width="%s" stroke-linecap="round" opacity="%s"/>' % (
                f(x), f(y), f(L * math.cos(a)), f(L * math.sin(a)), col, f(r * 0.8), f(rnd.uniform(0.5, 1))))
        else:
            out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>' % (f(x), f(y), f(r), col, f(rnd.uniform(0.45, 1))))
    return '<g>%s</g>' % "".join(out)


def smoke(c, x, y, w, h, color="#3A2A30", op=0.5):
    """Billowing smoke plume rising from (x,y)."""
    bl = c.blur(14)
    out = []
    for i in range(9):
        t = i / 8
        cx = x + math.sin(t * 3.2) * w * 0.25 + t * w * 0.3
        cy = y - h * t
        r = w * (0.18 + 0.32 * t)
        out.append('<circle cx="%s" cy="%s" r="%s"/>' % (f(cx), f(cy), f(r)))
    return '<g fill="%s" opacity="%s" filter="%s">%s</g>' % (color, f(op), bl, "".join(out))


def silhouette(c, color):
    """Filter that paints any artwork as a flat silhouette of `color` (for distant effigies)."""
    i = c.uid("sil")
    c.defs.append('<filter id="%s"><feFlood flood-color="%s"/><feComposite in2="SourceAlpha" operator="in"/></filter>' % (i, color))
    return "url(#%s)" % i


# ------------------------------------------------------------------ Ravan
def _zigzag(x0, x1, y, h, n, down=True):
    step = (x1 - x0) / n
    p = []
    for i in range(n):
        a = x0 + i * step
        p.append("M%s,%s L%s,%s L%s,%s Z" % (f(a), f(y), f(a + step / 2), f(y + (h if down else -h)), f(a + step), f(y)))
    return " ".join(p)


def ravan_head(c, cx, cy, w, face=("#FFD27A", "#E8962E"), crown_h=1.0, main=False, dark=False):
    """One demon head of the effigy: face, angry brows, big eyes, curled moustache, kundal, mukut.
    (cx,cy) is the face centre, w the face width."""
    s = w / 100.0
    out = ['<g transform="translate(%s,%s) scale(%s)">' % (f(cx), f(cy), f(s))]
    fg = c.lg([face[0], face[1]], 0, 0, 0, 1)
    # ears + kundal
    for sx in (-1, 1):
        out.append('<ellipse cx="%s" cy="2" rx="10" ry="17" fill="%s"/>' % (f(sx * 50), face[1]))
        out.append('<circle cx="%s" cy="34" r="12" fill="none" stroke="%s" stroke-width="6"/>' % (f(sx * 52), gld(c, True)))
        out.append('<circle cx="%s" cy="46" r="4.5" fill="#C62828"/>' % f(sx * 52))
    face_d = "M-50,-46 C-50,-72 -28,-80 0,-80 C28,-80 50,-72 50,-46 L50,18 C50,52 26,74 0,76 C-26,74 -50,52 -50,18 Z"
    out.append('<path d="%s" fill="%s" stroke="#6B2A06" stroke-width="3"/>' % (face_d, fg))
    # cheek blush + jaw shade
    out.append('<ellipse cx="-30" cy="18" rx="12" ry="8" fill="#E53935" opacity="0.35"/><ellipse cx="30" cy="18" rx="12" ry="8" fill="#E53935" opacity="0.35"/>')
    out.append('<path d="M-50,30 C-40,64 40,64 50,30 C50,52 26,74 0,76 C-26,74 -50,52 -50,30 Z" fill="#8B3A06" opacity="0.18"/>')
    # tilak
    out.append('<path d="M-9,-58 C-9,-40 -5,-32 0,-30 C5,-32 9,-40 9,-58" stroke="#FFFFFF" stroke-width="4" fill="none"/>')
    out.append('<path d="M0,-60 V-34" stroke="#D50000" stroke-width="5" stroke-linecap="round"/>')
    # brows (angry)
    out.append('<path d="M-44,-34 C-34,-46 -18,-40 -5,-22 L-9,-17 C-20,-30 -32,-34 -42,-26 Z" fill="#1A0A06"/>')
    out.append('<path d="M44,-34 C34,-46 18,-40 5,-22 L9,-17 C20,-30 32,-34 42,-26 Z" fill="#1A0A06"/>')
    # eyes
    for sx in (-1, 1):
        ex = sx * 22
        out.append('<path d="M%s,-12 C%s,-24 %s,-24 %s,-12 C%s,-2 %s,-2 %s,-12 Z" fill="#FFFFFF" stroke="#B71C1C" stroke-width="2.5"/>' % (
            f(ex - 16), f(ex - 8), f(ex + 8), f(ex + 16), f(ex + 8), f(ex - 8), f(ex - 16)))
        out.append('<circle cx="%s" cy="-12" r="6.5" fill="#1A0A06"/><circle cx="%s" cy="-14" r="2" fill="#fff"/>' % (f(ex + sx * 2), f(ex + sx * 2 - 2)))
    # nose
    out.append('<path d="M-3,-14 C-4,0 -12,8 -10,14 C-4,18 4,18 10,14 C12,8 4,0 3,-14" fill="%s" stroke="#6B2A06" stroke-width="2"/>' % face[1])
    # moustache
    out.append('<path d="M0,22 C-14,12 -36,12 -48,24 C-56,32 -66,26 -64,14 C-62,6 -54,6 -54,14 C-56,20 -50,22 -46,16 '
               'C-34,2 -14,2 0,14 C14,2 34,2 46,16 C50,22 56,20 54,14 C54,6 62,6 64,14 C66,26 56,32 48,24 C36,12 14,12 0,22 Z" fill="#1A0A06"/>')
    # mouth with fangs
    out.append('<path d="M-16,34 C-8,46 8,46 16,34 C8,38 -8,38 -16,34 Z" fill="#B71C1C"/>')
    out.append('<path d="M-11,36 l3,8 l3,-7 Z M11,36 l-3,8 l-3,-7 Z" fill="#fff"/>')
    # beard tuft
    out.append('<path d="M-10,58 C-6,72 6,72 10,58 C4,66 -4,66 -10,58 Z" fill="#1A0A06"/>')
    # mukut (crown)
    g = gld(c, True)
    ch = 70 * crown_h
    crown = ("M-56,-48 L-60,-%s L-44,-%s L-34,-%s L-18,-%s L0,-%s L18,-%s L34,-%s L44,-%s L60,-%s L56,-48 Z" % (
        f(48 + ch * 0.55), f(48 + ch * 0.4), f(48 + ch * 0.85), f(48 + ch * 0.62), f(48 + ch * 1.25),
        f(48 + ch * 0.62), f(48 + ch * 0.85), f(48 + ch * 0.4), f(48 + ch * 0.55)))
    out.append('<path d="%s" fill="%s" stroke="#5A3004" stroke-width="2.5" stroke-linejoin="round"/>' % (crown, g))
    out.append('<path d="M-56,-48 C-30,-40 30,-40 56,-48 L56,-60 C30,-52 -30,-52 -56,-60 Z" fill="#B71C1C" stroke="#5A3004" stroke-width="2"/>')
    for gx in (-38, -19, 0, 19, 38):
        out.append('<circle cx="%s" cy="-52" r="4" fill="#FFF3C4"/>' % gx)
    out.append('<circle cx="0" cy="%s" r="9" fill="#1E88E5" stroke="#FFE7A0" stroke-width="3"/>' % f(-48 - ch * 0.62))
    out.append('<circle cx="-34" cy="%s" r="5" fill="#2E7D32"/><circle cx="34" cy="%s" r="5" fill="#2E7D32"/>' % (f(-48 - ch * 0.5), f(-48 - ch * 0.5)))
    out.append('<circle cx="0" cy="%s" r="6" fill="#FFE7A0"/>' % f(-48 - ch * 1.25 - 4))
    if dark:
        out.append('<path d="%s" fill="#2A0E08" opacity="0.28"/>' % face_d)
    out.append("</g>")
    return "".join(out)


def ravan(c, cx, base, s=1.0, burn=0.0, colors=None, heads_only=False, arrow=False):
    """The Ravan effigy (~1000*s tall, ~940*s wide at the heads), feet at (cx, base).
    burn: 0 = none, 1 = flames up to the waist. arrow: flaming arrow lodged in chest."""
    col = colors or {}
    skirt = col.get("skirt", ["#C62828", "#F9A825", "#2E7D32", "#6A1B9A", "#EF6C00"])
    body = col.get("body", "#7B1FA2")
    trim = col.get("trim", "#FFC107")
    face = col.get("face", ("#FFD27A", "#E8962E"))
    out = ['<g transform="translate(%s,%s) scale(%s)">' % (f(cx), f(base), f(s))]
    g = gld(c, True)
    if not heads_only:
        # bamboo scaffold legs
        for lx in (-70, 70):
            out.append('<path d="M%s,-190 L%s,0" stroke="#5D3A1A" stroke-width="34" stroke-linecap="square"/>' % (f(lx), f(lx * 1.05)))
            for yy in range(-180, 0, 26):
                out.append('<path d="M%s,%s h36" stroke="%s" stroke-width="10"/>' % (f(lx * 1.02 - 18), yy, skirt[(yy // 26) % 2]))
            out.append('<path d="M%s,-8 h%s v8 h%s Z" fill="#3E2410"/>' % (f(lx * 1.05 - 30), f(60), f(-60)))
        # skirt / dhoti
        sk = "M-95,-430 L95,-430 L190,-180 L-190,-180 Z"
        cp = c.clip('<path d="%s"/>' % sk)
        panels = []
        for i in range(10):
            a0 = -190 + i * 38; a1 = a0 + 38
            t0 = -95 + i * 19; t1 = t0 + 19
            panels.append('<path d="M%s,-430 L%s,-430 L%s,-180 L%s,-180 Z" fill="%s"/>' % (f(t0), f(t1), f(a1), f(a0), skirt[i % len(skirt)]))
        out.append('<g clip-path="%s">%s<path d="%s" fill="%s"/></g>' % (cp, "".join(panels), sk, c.lg([(0, "#fff", 0.18), (0.5, "#fff", 0), (1, "#000", 0.3)], 0, 0, 1, 0)))
        for yy, ww in ((-360, 1), (-280, 1)):
            k = (yy + 430) / 250.0
            hw = 95 + 95 * k
            out.append('<path d="M%s,%s H%s" stroke="%s" stroke-width="10"/>' % (f(-hw), yy, f(hw), trim))
            out.append('<path d="M%s,%s H%s" stroke="#B71C1C" stroke-width="3" stroke-dasharray="4 6"/>' % (f(-hw), yy, f(hw)))
        out.append('<path d="%s" fill="%s"/>' % (_zigzag(-190, 190, -180, 26, 14), trim))
        out.append('<path d="%s" fill="#C62828"/>' % _zigzag(-178, 178, -180, 14, 14))
        # torso
        tor = "M-150,-640 C-120,-650 120,-650 150,-640 L110,-430 L-110,-430 Z"
        out.append('<path d="%s" fill="%s" stroke="#3A0E3A" stroke-width="3"/>' % (tor, body))
        out.append('<path d="%s" fill="%s"/>' % (tor, c.lg([(0, "#fff", 0.2), (0.5, "#fff", 0), (1, "#000", 0.35)], 0, 0, 1, 0)))
        # breastplate
        out.append('<path d="M-92,-610 C-60,-560 60,-560 92,-610 L70,-470 C30,-450 -30,-450 -70,-470 Z" fill="%s" stroke="#5A3004" stroke-width="3"/>' % g)
        out.append('<circle cx="0" cy="-535" r="34" fill="#B71C1C" stroke="#FFE7A0" stroke-width="5"/>')
        for k in range(12):
            a = math.radians(k * 30)
            out.append('<circle cx="%s" cy="%s" r="4" fill="#FFF3C4"/>' % (f(46 * math.cos(a)), f(-535 + 46 * math.sin(a))))
        out.append('<circle cx="0" cy="-535" r="14" fill="#1E88E5"/>')
        # belt
        out.append('<rect x="-116" y="-448" width="232" height="30" rx="6" fill="%s" stroke="#5A3004" stroke-width="2"/>' % g)
        for bx in range(-96, 100, 32):
            out.append('<rect x="%s" y="-441" width="14" height="16" rx="3" fill="#C62828"/>' % (bx - 7))
        # garlands
        for k, colr in enumerate(("#FFC107", "#E53935")):
            out.append('<path d="M-120,-630 C-80,%s 80,%s 120,-630" stroke="%s" stroke-width="12" stroke-dasharray="1 13" stroke-linecap="round" fill="none"/>' % (
                f(-470 + k * 40), f(-470 + k * 40), colr))
        # arms
        for sx in (-1, 1):
            sh = (sx * 150, -630)
            el = (sx * 250, -520)
            hd = (sx * 270, -620) if sx < 0 else (sx * 285, -455)
            out.append('<path d="M%s,%s L%s,%s L%s,%s" stroke="%s" stroke-width="58" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' % (
                f(sh[0]), f(sh[1]), f(el[0]), f(el[1]), f(hd[0]), f(hd[1]), body))
            out.append('<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="14" stroke-dasharray="14 10"/>' % (f(sh[0]), f(sh[1]), f(el[0]), f(el[1]), trim))
            out.append('<circle cx="%s" cy="%s" r="22" fill="%s" stroke="#5A3004" stroke-width="2"/>' % (f(el[0]), f(el[1]), g))
            out.append('<circle cx="%s" cy="%s" r="26" fill="%s" stroke="#6B2A06" stroke-width="2"/>' % (f(hd[0]), f(hd[1]), face[1]))
            out.append('<path d="M%s,%s l%s,0" stroke="%s" stroke-width="12"/>' % (f(hd[0] - 24), f(hd[1] + sx * 0 + 26), 48, g))
        # sword (left hand, raised)
        out.append('<path d="M-272,-640 L-282,-900 L-262,-930 L-250,-900 L-258,-640 Z" fill="%s" stroke="#455A64" stroke-width="3"/>' % c.lg(["#ECEFF1", "#90A4AE", "#FFFFFF", "#78909C"], 0, 0, 1, 0))
        out.append('<rect x="-305" y="-650" width="80" height="16" rx="7" fill="%s"/>' % g)
        out.append('<circle cx="-266" cy="-600" r="10" fill="%s"/>' % g)
        # shield (right hand)
        out.append('<circle cx="300" cy="-455" r="78" fill="%s" stroke="#5A3004" stroke-width="4"/>' % c.rg([(0, "#E53935"), (1, "#7F0000")], 0.4, 0.35, 0.7))
        out.append('<circle cx="300" cy="-455" r="62" fill="none" stroke="%s" stroke-width="8"/>' % g)
        for k in range(4):
            a = math.radians(45 + k * 90)
            out.append('<circle cx="%s" cy="%s" r="9" fill="%s"/>' % (f(300 + 36 * math.cos(a)), f(-455 + 36 * math.sin(a)), g))
        out.append('<circle cx="300" cy="-455" r="16" fill="%s"/>' % g)
        # neck
        out.append('<rect x="-40" y="-690" width="80" height="60" fill="%s"/>' % face[1])
        out.append('<path d="M-70,-640 C-30,-615 30,-615 70,-640 L60,-660 C30,-640 -30,-640 -60,-660 Z" fill="%s" stroke="#5A3004" stroke-width="2"/>' % g)
    # heads: centre + 4 left + 4 right in a row, + one on top  => ten heads
    hy = -760
    order = [(-4, 0.64), (4, 0.64), (-3, 0.7), (3, 0.7), (-2, 0.76), (2, 0.76), (-1, 0.84), (1, 0.84)]
    xs = {1: 128, 2: 236, 3: 336, 4: 428}
    for k, sc in order:
        x = (1 if k > 0 else -1) * xs[abs(k)]
        out.append(ravan_head(c, x, hy + abs(k) * 6, 120 * sc, face, 0.75, dark=True))
    out.append(ravan_head(c, 0, hy - 190, 84, face, 0.8))
    out.append(ravan_head(c, 0, hy, 132, face, 0.55, main=True))
    if arrow:
        out.append(flaming_arrow(c, -560, -470, -20, -540, 1.4))
    out.append("</g>")
    body_svg = "".join(out)
    if burn > 0:
        # char overlay on lower body + fire
        fire_svg = fire(c, cx, base + 8 * s, 520 * s, (260 + 380 * burn) * s, n=11)
        char = '<g transform="translate(%s,%s) scale(%s)"><path d="M-190,-180 L-95,-430 L95,-430 L190,-180 L80,0 L-80,0 Z" fill="%s"/></g>' % (
            f(cx), f(base), f(s), c.lg([(0, "#1A0500", 0), (0.6, "#1A0500", 0.55 * burn), (1, "#1A0500", 0.8 * burn)], 0, 0, 0, 1))
        extra = ""
        if burn >= 0.8:
            for fx, fy, fw in ((-250, -500, 70), (270, -420, 80), (-120, -610, 60), (130, -600, 60)):
                extra += fire(c, cx + fx * s, base + fy * s, fw * s, fw * 2.2 * s, n=3, glow=False, logs=False)
        return body_svg + char + fire_svg + extra
    return body_svg


# ------------------------------------------------------------------ arrow / bow
def flaming_arrow(c, x1, y1, x2, y2, s=1.0, trail=True):
    """Arrow flying from (x1,y1) (tail) to (x2,y2) (tip) with a blazing head and fire trail."""
    L = math.hypot(x2 - x1, y2 - y1)
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    out = ['<g transform="translate(%s,%s) rotate(%s)">' % (f(x1), f(y1), f(ang))]
    if trail:
        tg = c.lg([(0, "#FF6D00", 0), (0.6, "#FF9100", 0.55), (1, "#FFEB3B", 0.95)], 0, 0, 1, 0)
        out.append('<path d="M%s,0 C%s,%s %s,%s %s,0 C%s,%s %s,%s %s,0 Z" fill="%s"/>' % (
            f(L * 0.05), f(L * 0.4), f(-24 * s), f(L * 0.8), f(-30 * s), f(L - 10 * s), f(L * 0.8), f(30 * s), f(L * 0.4), f(24 * s), f(L * 0.05), tg))
        out.append('<path d="M%s,0 C%s,%s %s,%s %s,0 C%s,%s %s,%s %s,0 Z" fill="%s" opacity="0.9"/>' % (
            f(L * 0.35), f(L * 0.6), f(-10 * s), f(L * 0.85), f(-14 * s), f(L - 6 * s), f(L * 0.85), f(14 * s), f(L * 0.6), f(10 * s), f(L * 0.35),
            c.lg([(0, "#FFF59D", 0), (1, "#FFFFFF", 1)], 0, 0, 1, 0)))
    out.append('<rect x="0" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>' % (f(-3.5 * s), f(L - 30 * s), f(7 * s), f(3 * s), gld(c, True)))
    # fletching
    for sy in (-1, 1):
        out.append('<path d="M0,0 L%s,%s L%s,%s L%s,0 Z" fill="#D32F2F" stroke="#7F0000" stroke-width="1"/>' % (
            f(-10 * s), f(sy * 18 * s), f(46 * s), f(sy * 18 * s), f(58 * s)))
    # head
    out.append('<path d="M%s,%s L%s,0 L%s,%s L%s,0 Z" fill="%s" stroke="#5A3004" stroke-width="1.5"/>' % (
        f(L - 34 * s), f(-13 * s), f(L + 6 * s), f(L - 34 * s), f(13 * s), f(L - 26 * s), gld(c, True)))
    # blazing head
    out.append('<circle cx="%s" cy="0" r="%s" fill="%s"/>' % (f(L - 10 * s), f(46 * s), c.rg([(0, "#FFFDE7", 1), (0.25, "#FFD54F", 0.9), (0.6, "#FF6D00", 0.4), (1, "#FF3D00", 0)])))
    out.append("</g>")
    return "".join(out)


def bow(c, cx, cy, h, s_w=1.0, color=None, drawn=0.0, rot=0):
    """Ornate recurve bow standing vertically, grip at (cx,cy). drawn=0..1 pulls the string back (to the left)."""
    g = color or gld(c, True)
    k = h / 600.0
    out = ['<g transform="translate(%s,%s) rotate(%s) scale(%s)">' % (f(cx), f(cy), f(rot), f(k))]
    limb = ("M0,-40 C40,-120 50,-220 20,-290 C12,-300 -2,-300 -6,-292 C-10,-284 0,-278 6,-282 "
            "C30,-220 22,-120 -14,-40 Z")
    for sy in (1, -1):
        out.append('<path d="%s" fill="%s" stroke="#4A2804" stroke-width="3" transform="scale(1,%s)"/>' % (limb, g, sy))
        for t in (-120, -200):
            out.append('<ellipse cx="%s" cy="%s" rx="14" ry="6" fill="#B71C1C" transform="scale(1,%s)"/>' % (f(26 if t == -120 else 30), t, sy))
    out.append('<rect x="-18" y="-46" width="30" height="92" rx="10" fill="#7B1F1F" stroke="%s" stroke-width="4"/>' % g)
    for yy in (-30, -10, 10, 30):
        out.append('<path d="M-18,%d h30" stroke="%s" stroke-width="3"/>' % (yy, g))
    sx = -drawn * 260
    out.append('<path d="M-2,-292 L%s,0 L-2,292" stroke="#FFF3D6" stroke-width="3" fill="none"/>' % f(sx))
    out.append("</g>")
    return "".join(out)


# ------------------------------------------------------------------ Ram archer silhouette
def ram_archer(c, x, y, s=1.0, fill="#1B0B12", rim="#FFB74D", rimw=3, arrow=True, flip=False, arrow_flame=True, glow=None):
    """Silhouette of Shri Ram in a lunge drawing a bow (facing right). Feet at (x,y); ~600*s tall.
    rim: colour of the thin back-light outline. glow: optional halo colour behind the figure."""
    fid = c.uid("rim")
    c.defs.append('<filter id="%s" x="-20%%" y="-20%%" width="140%%" height="140%%"><feMorphology in="SourceAlpha" operator="dilate" radius="%s" result="d"/>'
                  '<feFlood flood-color="%s"/><feComposite in2="d" operator="in" result="r"/><feGaussianBlur in="r" stdDeviation="1.2" result="rb"/>'
                  '<feMerge><feMergeNode in="rb"/><feMergeNode in="SourceGraphic"/></feMerge></filter>' % (fid, f(rimw / max(s, 0.3)), rim))
    o = ['<g transform="translate(%s,%s) scale(%s,%s)">' % (f(x), f(y), f(-s if flip else s), f(s))]
    if glow:
        o.append('<ellipse cx="40" cy="-400" rx="260" ry="260" fill="%s"/>' % c.rg([(0, glow, 0.55), (1, glow, 0)]))
    F = fill
    p = []
    def stroke(d, w):
        p.append('<path d="%s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' % (d, F, w))
    def fillp(d):
        p.append('<path d="%s" fill="%s"/>' % (d, F))
    # uttariya scarf billowing behind
    fillp("M-18,-418 C-70,-410 -130,-392 -190,-350 C-168,-356 -146,-360 -128,-358 C-160,-336 -186,-308 -206,-276 "
          "C-176,-298 -146,-316 -112,-326 C-126,-306 -134,-286 -140,-262 C-110,-296 -70,-330 -22,-372 Z")
    # hair
    fillp("M-26,-486 C-40,-460 -44,-440 -50,-418 C-54,-400 -60,-388 -64,-372 C-50,-380 -42,-396 -36,-410 C-36,-392 -40,-378 -42,-362 C-28,-380 -22,-410 -16,-440 Z")
    # quiver + arrow fletchings
    fillp("M-46,-452 L-24,-458 L-4,-334 L-26,-328 Z")
    for k in range(3):
        bx, by = -44 + k * 8, -456 - k * 2
        fillp("M%s,%s L%s,%s L%s,%s L%s,%s Z" % (f(bx), f(by), f(bx - 10), f(by - 26), f(bx - 2), f(by - 34), f(bx + 6), f(by - 6)))
    # legs (lunge): back leg straight, front knee bent
    stroke("M-6,-292 L-58,-150 L-118,-18", 40)
    stroke("M18,-292 L78,-160 L74,-20", 40)
    fillp("M-140,-26 C-132,-8 -104,-4 -86,-2 C-84,-12 -96,-26 -110,-30 Z")
    fillp("M60,-30 L64,-2 C80,0 104,0 116,-4 C110,-18 92,-22 84,-30 Z")
    # dhoti drape (flared folds between legs + front pleat)
    fillp("M-32,-310 L38,-310 C50,-270 80,-200 104,-150 C80,-156 60,-168 46,-186 L40,-150 C20,-176 6,-200 2,-230 "
          "C-14,-190 -44,-160 -84,-136 C-60,-190 -44,-250 -32,-310 Z")
    # torso
    fillp("M-30,-424 C-12,-432 20,-434 36,-424 C46,-396 44,-350 32,-306 L-26,-306 C-36,-346 -40,-392 -30,-424 Z")
    # waist sash with hanging ends
    fillp("M-30,-318 L36,-318 L38,-300 L-30,-300 Z M-24,-304 C-36,-280 -40,-256 -52,-232 L-42,-230 C-32,-254 -24,-276 -16,-302 Z")
    # neck + head profile facing right
    fillp("M-8,-440 L14,-440 L16,-420 L-10,-420 Z")
    fillp("M-30,-470 C-32,-492 -14,-506 6,-506 C22,-506 32,-498 34,-482 C35,-476 36,-472 44,-462 C45,-458 40,-457 38,-456 "
          "C40,-452 39,-449 36,-448 C38,-444 37,-440 33,-438 C32,-430 22,-428 12,-430 C0,-432 -10,-438 -18,-446 C-26,-452 -30,-460 -30,-470 Z")
    # mukut (tiered tall crown) + side ornaments
    fillp("M-24,-496 C-26,-520 -20,-534 -14,-540 C-18,-548 -16,-560 -8,-566 C-10,-576 -4,-590 4,-608 "
          "C12,-590 18,-576 16,-566 C24,-560 26,-548 22,-540 C28,-534 34,-520 30,-496 Z")
    fillp("M-28,-500 L34,-500 L32,-488 L-26,-488 Z")
    fillp("M4,-608 C0,-620 8,-628 4,-640 C12,-630 12,-618 4,-608 Z")
    # bow arm extended forward (to the right) with armlet and fist
    stroke("M22,-414 L100,-410 L184,-408", 20)
    fillp("M60,-424 h12 v30 h-12 Z")
    fillp("M178,-424 C194,-428 204,-418 202,-404 C200,-392 188,-388 178,-394 Z")
    # draw arm: shoulder -> elbow high behind -> hand at the cheek
    stroke("M-4,-414 L-96,-436", 20)
    stroke("M-96,-436 L4,-446", 17)
    fillp("M-6,-460 C8,-462 16,-452 12,-440 C8,-432 -4,-432 -8,-440 Z")
    # bow limbs
    fillp("M190,-414 C236,-470 250,-560 214,-640 C208,-652 196,-654 190,-646 C186,-640 190,-632 198,-636 C224,-556 214,-476 180,-420 Z")
    fillp("M190,-398 C236,-342 250,-252 214,-172 C208,-160 196,-158 190,-166 C186,-172 190,-180 198,-176 C224,-256 214,-336 180,-392 Z")
    o.append('<g filter="url(#%s)">%s</g>' % (fid, "".join(p)))
    o.append('<path d="M196,-640 L6,-448 L196,-172" stroke="%s" stroke-width="2.2" fill="none" opacity="0.95"/>' % rim)
    if arrow:
        o.append('<path d="M0,-450 L312,-386" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % F)
        o.append('<path d="M0,-450 L312,-386" stroke="%s" stroke-width="1.4" opacity="0.8"/>' % rim)
        o.append('<path d="M304,-398 L338,-380 L300,-376 Z" fill="%s" stroke="%s" stroke-width="2"/>' % (F, rim))
        if arrow_flame:
            o.append('<circle cx="326" cy="-382" r="40" fill="%s"/>' % c.rg([(0, "#FFFDE7", 1), (0.3, "#FFD54F", 0.9), (0.7, "#FF6D00", 0.35), (1, "#FF3D00", 0)]))
            o.append('<path d="M338,-380 C306,-404 284,-404 250,-420 C276,-398 282,-392 304,-384 C282,-380 270,-370 246,-362 C280,-366 306,-362 338,-380 Z" fill="#FF9100" opacity="0.92"/>')
            o.append('<path d="M338,-380 C316,-392 302,-392 284,-398 C300,-386 306,-384 314,-382 C302,-376 298,-372 286,-366 C304,-370 318,-370 338,-380 Z" fill="#FFF59D"/>')
    o.append("</g>")
    return "".join(o)



# ------------------------------------------------------------------ leaves
def apta_leaf(c, x, y, s=1.0, rot=0, fill=None, vein="#6E4A07", stem=True):
    """Apta (Bauhinia) two-lobed leaf, exchanged as 'gold' on Dussehra. Stem base at (x,y), pointing up."""
    g = fill or c.lg([(0, "#FFF1B0"), (0.35, "#E6B437"), (0.7, "#B7801A"), (1, "#7A4E08")], 0, 0, 1, 1)
    out = ['<g transform="translate(%s,%s) rotate(%s) scale(%s)">' % (f(x), f(y), f(rot), f(s))]
    d = ("M0,-10 C-10,-30 -60,-40 -78,-90 C-92,-130 -70,-170 -40,-168 C-18,-166 -6,-146 0,-128 "
         "C6,-146 18,-166 40,-168 C70,-170 92,-130 78,-90 C60,-40 10,-30 0,-10 Z")
    out.append('<path d="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (d, g, vein))
    out.append('<path d="M0,-10 V-126" stroke="%s" stroke-width="2.4"/>' % vein)
    for sx in (-1, 1):
        for k, (ex, ey) in enumerate(((46, -150), (70, -120), (74, -80), (54, -48))):
            out.append('<path d="M0,-%d Q%s,%s %s,%s" stroke="%s" stroke-width="1.6" fill="none" opacity="0.8"/>' % (
                20 + k * 8, f(sx * ex * 0.4), f(ey * 0.8), f(sx * ex), f(ey), vein))
    out.append('<path d="M-30,-150 C-50,-140 -64,-110 -60,-86" stroke="#FFFBE6" stroke-width="4" fill="none" opacity="0.55" stroke-linecap="round"/>')
    if stem:
        out.append('<path d="M0,-10 C2,6 -2,18 -6,30" stroke="%s" stroke-width="5" fill="none" stroke-linecap="round"/>' % vein)
    out.append("</g>")
    return "".join(out)


def shami_sprig(c, x, y, L, rot=0, color="#4E7D2A", color2="#8BC34A"):
    """Shami (Prosopis) sprig: fine pinnate leaflets along a stem, base at (x,y), pointing up."""
    out = ['<g transform="translate(%s,%s) rotate(%s)">' % (f(x), f(y), f(rot))]
    out.append('<path d="M0,0 C4,%s -4,%s 0,%s" stroke="#5D4037" stroke-width="3.5" fill="none"/>' % (f(-L * 0.3), f(-L * 0.6), f(-L)))
    n = int(L / 16)
    for i in range(2, n):
        t = i / n
        yy = -L * t
        ll = 26 * (1 - t * 0.5)
        for sx in (-1, 1):
            out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" transform="rotate(%s %s %s)"/>' % (
                f(sx * ll * 0.55), f(yy), f(ll * 0.55), f(ll * 0.16), color if i % 2 else color2, f(sx * -28), f(sx * ll * 0.55), f(yy)))
    out.append("</g>")
    return "".join(out)


# ------------------------------------------------------------------ flag, chariot, crowd
def dhwaj(c, x, y, h, flag_w=None, color=("#FF9800", "#E65100"), wave=1.0, pole=None, tails=True, emblem=True):
    """Victory flag: saffron pennant on a gold-topped pole, pole base at (x,y)."""
    fw = flag_w or h * 0.55
    pg = pole or gld(c, True)
    out = []
    out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="4" fill="%s"/>' % (f(x - 6), f(y - h), 12, f(h), pg))
    out.append('<path d="M%s,%s L%s,%s L%s,%s Z" fill="%s"/>' % (f(x - 10), f(y - h), f(x), f(y - h - 38), f(x + 10), f(y - h), pg))
    out.append('<circle cx="%s" cy="%s" r="9" fill="%s"/>' % (f(x), f(y - h - 2), pg))
    top = y - h + 14
    fh = fw * 0.62
    wv = 26 * wave
    if tails:
        d = ("M%s,%s C%s,%s %s,%s %s,%s L%s,%s L%s,%s C%s,%s %s,%s %s,%s Z" % (
            f(x + 5), f(top), f(x + fw * 0.35), f(top - wv), f(x + fw * 0.65), f(top + wv), f(x + fw), f(top + fh * 0.12),
            f(x + fw * 0.72), f(top + fh * 0.45), f(x + fw * 0.95), f(top + fh * 0.88),
            f(x + fw * 0.6), f(top + fh + wv * 0.6), f(x + fw * 0.3), f(top + fh - wv * 0.8), f(x + 5), f(top + fh)))
    else:
        d = "M%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s Z" % (
            f(x + 5), f(top), f(x + fw * 0.4), f(top - wv), f(x + fw * 0.7), f(top + wv), f(x + fw), f(top + fh * 0.5),
            f(x + fw * 0.6), f(top + fh + wv * 0.5), f(x + fw * 0.3), f(top + fh - wv * 0.6), f(x + 5), f(top + fh))
    out.append('<path d="%s" fill="%s"/>' % (d, c.lg([color[0], color[1]], 0, 0, 1, 1)))
    out.append('<path d="%s" fill="%s"/>' % (d, c.lg([(0, "#000", 0.0), (0.3, "#fff", 0.22), (0.55, "#000", 0.18), (0.8, "#fff", 0.15), (1, "#000", 0.2)], 0, 0, 1, 0)))
    if emblem:
        ex, ey = x + fw * 0.4, top + fh * 0.45
        r = fh * 0.2
        out.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#FFF3C4" stroke-width="%s" opacity="0.9"/>' % (f(ex), f(ey), f(r), f(r * 0.14)))
        for k in range(12):
            a = math.radians(k * 30)
            out.append('<path d="M%s,%s L%s,%s" stroke="#FFF3C4" stroke-width="%s" opacity="0.9"/>' % (
                f(ex + r * 1.25 * math.cos(a)), f(ey + r * 1.25 * math.sin(a)), f(ex + r * 1.6 * math.cos(a)), f(ey + r * 1.6 * math.sin(a)), f(r * 0.12)))
        out.append('<circle cx="%s" cy="%s" r="%s" fill="#FFF3C4" opacity="0.9"/>' % (f(ex), f(ey), f(r * 0.5)))
    out.append('<path d="%s" fill="none" stroke="#FFD54F" stroke-width="3" opacity="0.7"/>' % d)
    return "".join(out)


def chariot(c, x, y, s=1.0, body="#8E1B1B", flag=True):
    """Ornate ratha (side view) with big spoked wheel, pillared canopy and shikhara; ground contact at (x,y).
    ~560*s wide, ~720*s tall with flag."""
    g = gld(c, True)
    out = ['<g transform="translate(%s,%s) scale(%s)">' % (f(x), f(y), f(s))]
    # shadow
    out.append('<ellipse cx="0" cy="4" rx="300" ry="18" fill="#000" opacity="0.3"/>')
    # platform
    out.append('<path d="M-270,-150 L270,-150 L250,-100 L-250,-100 Z" fill="%s" stroke="#4A1010" stroke-width="3"/>' % body)
    out.append('<path d="M-280,-170 L280,-170 L270,-150 L-270,-150 Z" fill="%s" stroke="#5A3004" stroke-width="2"/>' % g)
    for k in range(-5, 6):
        out.append('<circle cx="%d" cy="-125" r="9" fill="%s"/>' % (k * 45, g))
    out.append('<path d="M-250,-100 %s" fill="none" stroke="%s" stroke-width="0"/>' % ("", g))
    # yoke pole to the right
    out.append('<path d="M250,-130 C320,-130 360,-120 400,-96" stroke="%s" stroke-width="12" fill="none" stroke-linecap="round"/>' % g)
    # pillars
    for px in (-230, -80, 80, 230):
        out.append('<rect x="%d" y="-440" width="22" height="270" fill="%s" stroke="#5A3004" stroke-width="2"/>' % (px - 11, g))
        for yy in (-420, -300, -200):
            out.append('<rect x="%d" y="%d" width="32" height="14" rx="4" fill="%s"/>' % (px - 16, yy, "#B71C1C"))
    # seat / throne back
    out.append('<path d="M-120,-170 L-120,-300 C-120,-340 -60,-360 0,-360 C60,-360 120,-340 120,-300 L120,-170 Z" fill="%s" stroke="#5A3004" stroke-width="3"/>' % "#B71C1C")
    out.append('<path d="M-90,-190 L-90,-290 C-90,-316 -40,-330 0,-330 C40,-330 90,-316 90,-290 L90,-190 Z" fill="none" stroke="%s" stroke-width="5"/>' % g)
    # canopy roof
    out.append('<path d="M-290,-440 L290,-440 L250,-490 L-250,-490 Z" fill="%s" stroke="#5A3004" stroke-width="3"/>' % g)
    # hanging fringe
    for k in range(-13, 14):
        out.append('<path d="M%d,-440 v18" stroke="%s" stroke-width="3"/><circle cx="%d" cy="-418" r="5" fill="%s"/>' % (k * 21, g, k * 21, "#E53935" if k % 2 else "#FFE7A0"))
    # shikhara
    out.append('<path d="M-200,-490 C-180,-560 -110,-620 0,-700 C110,-620 180,-560 200,-490 Z" fill="%s" stroke="#4A1010" stroke-width="3"/>' % body)
    for k in range(1, 4):
        yy = -490 - k * 50
        ww = 200 - k * 48
        out.append('<path d="M%d,%d H%d" stroke="%s" stroke-width="8"/>' % (-ww, yy, ww, g))
    out.append('<path d="M-200,-490 C-180,-560 -110,-620 0,-700 C110,-620 180,-560 200,-490" fill="none" stroke="%s" stroke-width="6"/>' % g)
    out.append('<path d="M0,-700 C-12,-718 -8,-736 0,-750 C8,-736 12,-718 0,-700 Z" fill="%s"/>' % g)
    out.append('<circle cx="0" cy="-702" r="12" fill="%s"/>' % g)
    if flag:
        out.append(dhwaj(c, 0, -700, 160, 150, wave=0.8, emblem=False))
    # wheels (front big wheel)
    for wx, R in ((-150, 120), (160, 120)):
        out.append('<circle cx="%d" cy="-%d" r="%d" fill="none" stroke="#3E1C08" stroke-width="30"/>' % (wx, R, R))
        out.append('<circle cx="%d" cy="-%d" r="%d" fill="none" stroke="%s" stroke-width="18"/>' % (wx, R, R, g))
        for k in range(12):
            a = math.radians(k * 30)
            out.append('<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="8"/>' % (
                f(wx), f(-R), f(wx + (R - 12) * math.cos(a)), f(-R + (R - 12) * math.sin(a)), g))
        for k in range(24):
            a = math.radians(k * 15)
            out.append('<circle cx="%s" cy="%s" r="3.5" fill="#FFE7A0"/>' % (f(wx + R * math.cos(a)), f(-R + R * math.sin(a))))
        out.append('<circle cx="%d" cy="-%d" r="26" fill="%s" stroke="#5A3004" stroke-width="3"/><circle cx="%d" cy="-%d" r="10" fill="#B71C1C"/>' % (wx, R, g, wx, R))
    out.append("</g>")
    return "".join(out)


def crowd(c, x0, x1, y, h, color="#12060A", n=None, arms=0.35):
    """Silhouette crowd of spectators (heads and shoulders, a few raised arms)."""
    rnd = c.rnd
    n = n or int((x1 - x0) / 34)
    d = []
    extra = []
    for i in range(n):
        x = x0 + (x1 - x0) * (i + rnd.uniform(0.1, 0.9)) / n
        hh = h * rnd.uniform(0.7, 1.0)
        r = hh * 0.2
        top = y - hh
        d.append("M%s,%s C%s,%s %s,%s %s,%s L%s,%s C%s,%s %s,%s %s,%s Z" % (
            f(x - r * 1.9), f(y), f(x - r * 1.9), f(top + r * 3.2), f(x - r * 1.4), f(top + r * 2.3), f(x - r * 0.5), f(top + r * 2.1),
            f(x + r * 0.5), f(top + r * 2.1), f(x + r * 1.4), f(top + r * 2.3), f(x + r * 1.9), f(top + r * 3.2), f(x + r * 1.9), f(y)))
        d.append("M%s,%s m-%s,0 a%s,%s 0 1,0 %s,0 a%s,%s 0 1,0 -%s,0" % (f(x), f(top + r), f(r), f(r), f(r), f(r * 2), f(r), f(r), f(r * 2)))
        if rnd.random() < arms:
            sx = rnd.choice((-1, 1))
            ex, ey = x + sx * r * 1.3, top + r * 2.4
            hx, hy = x + sx * r * rnd.uniform(1.8, 3.0), top - r * rnd.uniform(0.6, 1.8)
            extra.append('<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (f(ex), f(ey), f(hx), f(hy), color, f(r * 0.85)))
    return '<path d="%s" fill="%s"/>' % (" ".join(d), color) + "".join(extra)


def effigy_silhouette(c, cx, base, s, color="#2A0E14", heads=1):
    """Distant effigy silhouette (Kumbhakarna/Meghnad style) for backgrounds."""
    out = ['<g transform="translate(%s,%s) scale(%s)" fill="%s">' % (f(cx), f(base), f(s), color)]
    out.append('<path d="M-60,0 L-50,-180 L-90,-180 L-60,-400 L-120,-400 L-200,-300 L-180,-290 L-110,-360 L-100,-400 '
               'L-70,-420 L-40,-440 L40,-440 L70,-420 L100,-400 L110,-360 L180,-290 L200,-300 L120,-400 L60,-400 L90,-180 L50,-180 L60,0 Z"/>')
    for k in range(heads):
        hx = (k - (heads - 1) / 2) * 90
        out.append('<ellipse cx="%s" cy="-500" rx="52" ry="64"/>' % f(hx))
        out.append('<path d="M%s,-548 L%s,-620 L%s,-590 L%s,-650 L%s,-590 L%s,-620 L%s,-548 Z"/>' % (
            f(hx - 50), f(hx - 40), f(hx - 20), f(hx), f(hx + 20), f(hx + 40), f(hx + 50)))
    out.append("</g>")
    return "".join(out)
