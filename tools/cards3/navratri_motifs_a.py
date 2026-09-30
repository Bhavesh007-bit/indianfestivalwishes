"""Navratri motifs (agent A): garba dancers, garbo, dandiya, trishul, chunri, bandhani, mirror-work."""
import math
from lib_a import f, pts, rr, sparkle, W, H

SKIN = ("#E3A57A", "#B8744C")
HAIR = "#1C1110"


def _arm(c, sh, el, hd, sleeve, skin, bangles=("#E0115F", "#FFD36B", "#1E9E6A"), w=13):
    sg = skin
    out = []
    out.append('<path d="M%s,%s L%s,%s L%s,%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"/>'
               % (f(sh[0]), f(sh[1]), f(el[0]), f(el[1]), f(hd[0]), f(hd[1]), sg, f(w)))
    # sleeve on upper arm
    sx = sh[0] + (el[0] - sh[0]) * 0.45
    sy = sh[1] + (el[1] - sh[1]) * 0.45
    out.append('<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (f(sh[0]), f(sh[1]), f(sx), f(sy), sleeve, f(w + 4)))
    # bangles near wrist
    dx, dy = hd[0] - el[0], hd[1] - el[1]
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    for k, t in enumerate((0.62, 0.7, 0.78)):
        bx, by = el[0] + dx * t, el[1] + dy * t
        out.append('<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % (
            f(bx + nx * 8), f(by + ny * 8), f(bx - nx * 8), f(by - ny * 8), bangles[k % len(bangles)]))
    out.append('<circle cx="%s" cy="%s" r="7.5" fill="%s"/>' % (f(hd[0] + ux * 4), f(hd[1] + uy * 4), sg))
    return "".join(out)


def _hem(t, left=(-150, -56), right=(154, -24), sag=34):
    x = left[0] + (right[0] - left[0]) * t
    y = left[1] + (right[1] - left[1]) * t + sag * math.sin(math.pi * t)
    return x, y


def dancer_f(c, x, y, s=1.0, flip=False, pose="a", col=None, skin=SKIN, sil=None):
    """Female garba dancer in twirling chaniya choli. Feet at (x,y); ~425*s tall.
    sil: if a colour is given, draws a flat silhouette in that colour (for crowds)."""
    col = col or {}
    skirt = col.get("skirt", ["#C2185B", "#FF8F00", "#1E88E5", "#43A047", "#8E24AA", "#F4511E"])
    choli = col.get("choli", "#1B5E20")
    dup = col.get("dup", "#E53935")
    border = col.get("border", "#FFC53D")
    sk = sil or c.lg([skin[0], skin[1]], 0, 0, 1, 1)
    hair = sil or HAIR
    out = ['<g transform="translate(%s,%s) scale(%s,%s)">' % (f(x), f(y), f(-s if flip else s), f(s))]
    waist = (2, -282)
    N = 14
    hem = [_hem(i / N) for i in range(N + 1)]
    # skirt outline with rippled hem
    d = "M-16,-282 C-44,-226 -112,-140 %s,%s " % (f(hem[0][0]), f(hem[0][1]))
    for i in range(N):
        a, b = hem[i], hem[i + 1]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 13
        d += "Q%s,%s %s,%s " % (f(mx), f(my), f(b[0]), f(b[1]))
    d += "C120,-116 50,-226 20,-282 Z"
    # arms poses (shoulder, elbow, hand)
    P = {
        "a": (((18, -336), (54, -382), (36, -428)), ((-14, -336), (-56, -318), (-76, -350))),
        "b": (((18, -336), (52, -374), (24, -414)), ((-14, -336), (-46, -380), (-10, -416))),
        "c": (((18, -336), (72, -332), (110, -356)), ((-14, -336), (-64, -324), (-102, -342))),
        "d": (((18, -336), (60, -300), (92, -318)), ((-14, -336), (-40, -384), (-20, -430))),
    }[pose]
    if sil:
        # dupatta
        out.append('<path d="M20,-340 C-40,-330 -110,-300 -160,-238 C-120,-250 -70,-262 -30,-300 Z" fill="%s" opacity="0.8"/>' % sil)
        out.append('<ellipse cx="-34" cy="-6" rx="16" ry="7" fill="%s"/><ellipse cx="38" cy="-2" rx="16" ry="7" fill="%s"/>' % (sil, sil))
        out.append('<path d="%s" fill="%s"/>' % (d, sil))
        out.append('<path d="M-18,-342 L24,-342 L24,-300 L20,-280 L-14,-280 L-17,-305 Z" fill="%s"/>' % sil)
        for arm in P:
            out.append('<path d="M%s,%s L%s,%s L%s,%s" fill="none" stroke="%s" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>'
                       % (f(arm[0][0]), f(arm[0][1]), f(arm[1][0]), f(arm[1][1]), f(arm[2][0]), f(arm[2][1]), sil))
            out.append('<circle cx="%s" cy="%s" r="8" fill="%s"/>' % (f(arm[2][0]), f(arm[2][1]), sil))
        out.append('<rect x="0" y="-354" width="12" height="16" fill="%s"/><circle cx="6" cy="-373" r="25" fill="%s"/><circle cx="-18" cy="-388" r="14" fill="%s"/>' % (sil, sil, sil))
        out.append('<path d="M31,-376 L38,-368 L30,-366 Z" fill="%s"/>' % sil)
        out.append('<path d="M-14,-366 C-40,-340 -44,-310 -64,-290" stroke="%s" stroke-width="9" fill="none" stroke-linecap="round"/>' % sil)
        out.append("</g>")
        return "".join(out)

    # back dupatta (behind body)
    bdots = c.pattern(16, 16, '<circle cx="4" cy="4" r="1.8" fill="#FFF3D0"/><circle cx="12" cy="12" r="1.8" fill="#FFF3D0"/>')
    dp = "M22,-342 C-30,-336 -86,-318 -136,-262 C-124,-250 -116,-236 -108,-214 C-94,-250 -56,-282 -20,-298 Z"
    out.append('<path d="%s" fill="%s" opacity="0.92"/>' % (dp, dup))
    out.append('<path d="%s" fill="%s" opacity="0.5"/>' % (dp, bdots))
    out.append('<path d="M-136,-262 C-124,-250 -116,-236 -108,-214" stroke="%s" stroke-width="7" fill="none"/>' % border)
    # tassels at dupatta end
    for k in range(4):
        tx, ty = -134 + k * 9, -259 + k * 15
        out.append('<path d="M%s,%s l-10,10" stroke="%s" stroke-width="2"/><circle cx="%s" cy="%s" r="3.5" fill="%s"/>' % (
            f(tx), f(ty), border, f(tx - 11), f(ty + 11), border))
    # braid with parandi
    out.append('<path d="M-12,-368 C-34,-344 -40,-316 -58,-292" stroke="%s" stroke-width="10" fill="none" stroke-linecap="round"/>' % hair)
    for k in range(5):
        bx, by = -16 - k * 8.5, -360 + k * 14
        out.append('<ellipse cx="%s" cy="%s" rx="6" ry="4" fill="#3A2420" transform="rotate(-50 %s %s)"/>' % (f(bx), f(by), f(bx), f(by)))
    out.append('<path d="M-58,-292 l-6,20 M-58,-292 l0,22 M-58,-292 l6,20" stroke="%s" stroke-width="2.5"/><circle cx="-58" cy="-292" r="5" fill="%s"/>' % (dup, border))
    # back arm
    out.append(_arm(c, *P[1], sleeve=choli, skin=sk))
    # feet
    out.append('<path d="M-52,-10 C-50,-22 -20,-22 -14,-8 C-26,-2 -46,-2 -52,-10 Z" fill="%s"/>' % sk)
    out.append('<path d="M22,-4 C28,-16 56,-14 62,-2 C50,4 30,4 22,-4 Z" fill="%s"/>' % sk)
    out.append('<path d="M-46,-16 L-20,-16 M28,-10 L54,-10" stroke="%s" stroke-width="3" stroke-dasharray="2 3"/>' % border)
    # skirt gores
    cp = c.clip('<path d="%s"/>' % d)
    g = ['<g clip-path="%s">' % cp]
    M = 12
    for i in range(M):
        a = _hem(i / M); b = _hem((i + 1) / M)
        g.append('<path d="M%s,%s L%s,%s L%s,%s Z" fill="%s"/>' % (f(waist[0]), f(waist[1] - 30), f(a[0] - 8), f(a[1] + 30), f(b[0] + 8), f(b[1] + 30), skirt[i % len(skirt)]))
    # fold shading
    for i in range(M):
        a = _hem((i + 0.5) / M)
        g.append('<path d="M%s,%s L%s,%s" stroke="#000" stroke-opacity="0.16" stroke-width="10"/>' % (f(waist[0]), f(waist[1]), f(a[0]), f(a[1] + 20)))
    g.append('<path d="%s" fill="%s"/>' % (d, c.lg([(0, "#fff", 0.25), (0.45, "#fff", 0), (1, "#000", 0.25)], 0, 0, 1, 0)))
    g.append("</g>")
    out.extend(g)

    # bands: hem border + mid band + mirror dots
    def band(k, wdt, colr, dots=True, dotc="#EAF2FF"):
        pp = []
        for i in range(N * 2 + 1):
            hx, hy = _hem(i / (N * 2))
            pp.append((waist[0] + (hx - waist[0]) * k, waist[1] + (hy - waist[1]) * k))
        o = '<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (pts(pp), colr, f(wdt))
        if dots:
            for i in range(0, len(pp), 1):
                px, py = pp[i]
                o += '<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="#7A3B00" stroke-width="0.8"/>' % (f(px), f(py), f(wdt * 0.26), dotc)
        return o

    out.append(band(0.97, 22, border))
    out.append(band(0.97, 6, "#8B0000", dots=False))
    out.append(band(0.6, 12, border))
    out.append(band(0.3, 7, border, dots=False))
    # hem scallop lace
    lace = []
    for i in range(N * 2):
        hx, hy = _hem((i + 0.5) / (N * 2))
        lace.append('<circle cx="%s" cy="%s" r="5" fill="%s"/>' % (f(hx), f(hy + 4), border))
    out.append("".join(lace))
    # waist band + midriff
    out.append('<path d="M-15,-303 L21,-303 L19,-280 L-14,-280 Z" fill="%s"/>' % sk)
    out.append('<rect x="-18" y="-290" width="40" height="11" rx="4" fill="%s"/>' % border)
    out.append('<path d="M-16,-286 C-30,-270 -34,-248 -26,-230" stroke="%s" stroke-width="3" fill="none"/><circle cx="-26" cy="-228" r="4" fill="%s"/>' % (border, dup))
    # choli
    out.append('<path d="M-18,-342 C0,-348 14,-348 24,-342 L25,-306 C12,-300 -6,-300 -17,-305 Z" fill="%s"/>' % choli)
    for (mx, my) in ((-8, -330), (6, -326), (16, -316), (-4, -314), (10, -336)):
        out.append('<circle cx="%s" cy="%s" r="3" fill="#EAF2FF" stroke="%s" stroke-width="1.2"/>' % (mx, my, border))
    out.append('<path d="M-17,-305 C-6,-300 12,-300 25,-306" stroke="%s" stroke-width="4" fill="none"/>' % border)
    # necklace
    out.append('<path d="M-2,-342 C2,-332 12,-332 16,-342" stroke="%s" stroke-width="4" fill="none"/>' % border)
    # neck + head
    out.append('<rect x="0" y="-356" width="12" height="18" fill="%s"/>' % sk)
    out.append('<circle cx="6" cy="-373" r="25" fill="%s"/>' % sk)
    out.append('<path d="M31,-378 L38,-368 L30,-365 Z" fill="%s"/>' % sk)  # nose
    out.append('<path d="M-19,-362 C-26,-378 -16,-400 6,-399 C22,-399 30,-390 31,-383 C20,-390 10,-386 6,-376 C0,-366 -10,-360 -19,-362 Z" fill="%s"/>' % hair)
    out.append('<circle cx="-18" cy="-388" r="14" fill="%s"/>' % hair)
    for a in range(0, 360, 40):
        out.append('<circle cx="%s" cy="%s" r="3.2" fill="#FFF8E7"/>' % (f(-18 + 15 * math.cos(math.radians(a))), f(-388 + 15 * math.sin(math.radians(a)))))
    out.append('<path d="M18,-378 q4,-3 8,0" stroke="#2A1510" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    out.append('<circle cx="27" cy="-386" r="2.4" fill="#C62828"/>')
    out.append('<circle cx="33" cy="-365" r="4" fill="none" stroke="%s" stroke-width="1.6"/>' % border)
    out.append('<path d="M4,-362 l-5,10 h10 z" fill="%s"/><circle cx="4" cy="-350" r="2.5" fill="%s"/>' % (border, border))
    out.append('<path d="M6,-398 L20,-392" stroke="%s" stroke-width="2"/><circle cx="21" cy="-391" r="3" fill="%s"/>' % (border, border))
    # front arm
    out.append(_arm(c, *P[0], sleeve=choli, skin=sk))
    # swish lines
    out.append('<path d="M-164,-96 C-178,-60 -168,-30 -140,-10 M166,-60 C178,-30 168,-6 148,6" stroke="%s" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.6"/>' % border)
    out.append("</g>")
    return "".join(out)


def dancer_m(c, x, y, s=1.0, flip=False, col=None, skin=SKIN, stick=("#E53935", "#FFD740"), sil=None):
    """Male garba/dandiya dancer in kediyu with a pair of dandiya. Feet at (x,y); ~440*s tall."""
    col = col or {}
    ked = col.get("kediyu", "#FFF4E0")
    trim = col.get("trim", "#D81B60")
    pagdi = col.get("pagdi", ["#E53935", "#FFB300", "#43A047"])
    pant = col.get("pant", "#F3E5C8")
    border = col.get("border", "#FFC53D")
    sk = sil or c.lg([skin[0], skin[1]], 0, 0, 1, 1)
    out = ['<g transform="translate(%s,%s) scale(%s,%s)">' % (f(x), f(y), f(-s if flip else s), f(s))]
    R = (((24, -356), (64, -326), (86, -372)), ((-18, -356), (-58, -322), (-66, -366)))
    sticks = []
    for (sh, el, hd), ang in zip(R, (-62, -118)):
        a = math.radians(ang)
        sx, sy = hd[0] + 100 * math.cos(a), hd[1] + 100 * math.sin(a)
        sticks.append((hd[0] - 34 * math.cos(a), hd[1] - 34 * math.sin(a), sx, sy))
    if sil:
        o = sil
        out.append('<path d="M-8,-236 L-44,-130 L-34,-6 M14,-236 L64,-150 L44,-70" stroke="%s" stroke-width="30" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' % o)
        out.append('<path d="M-22,-362 L28,-362 L24,-300 L64,-226 L-60,-226 L-18,-300 Z" fill="%s"/>' % o)
        for sh, el, hd in R:
            out.append('<path d="M%s,%s L%s,%s L%s,%s" stroke="%s" stroke-width="15" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' % (
                f(sh[0]), f(sh[1]), f(el[0]), f(el[1]), f(hd[0]), f(hd[1]), o))
        for s_ in sticks:
            out.append('<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="8" stroke-linecap="round"/>' % (f(s_[0]), f(s_[1]), f(s_[2]), f(s_[3]), o))
        out.append('<rect x="-2" y="-376" width="14" height="18" fill="%s"/><circle cx="4" cy="-392" r="24" fill="%s"/>' % (o, o))
        out.append('<path d="M-24,-398 C-26,-430 30,-436 32,-402 Z M-22,-400 C-44,-396 -60,-380 -66,-356 L-54,-360 C-44,-380 -30,-392 -18,-396 Z" fill="%s"/>' % o)
        out.append('<path d="M30,-394 L37,-386 L29,-384 Z" fill="%s"/>' % o)
        out.append("</g>")
        return "".join(out)
    # legs: back leg straight, front leg lifted
    out.append('<path d="M-8,-236 L-44,-130 L-34,-14" stroke="%s" stroke-width="30" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' % pant)
    out.append('<path d="M-8,-236 L-44,-130 L-34,-14" stroke="#000" stroke-opacity="0.12" stroke-width="6" fill="none" transform="translate(8,0)"/>')
    out.append('<path d="M-52,-8 C-50,-22 -26,-22 -14,-10 C-6,-2 -30,2 -52,-2 Z" fill="%s"/>' % trim)
    out.append('<path d="M14,-236 L64,-150 L44,-72" stroke="%s" stroke-width="30" fill="none" stroke-linecap="round" stroke-linejoin="round"/>' % pant)
    out.append('<path d="M38,-78 C48,-84 70,-76 78,-62 C62,-58 46,-60 38,-66 Z" fill="%s"/>' % trim)
    for yy in (-120, -100, -40, -26):
        pass
    # churidar gathers
    out.append('<path d="M-40,-60 l12,4 M-40,-48 l12,4 M-40,-36 l12,4 M52,-104 l12,6 M50,-92 l12,6" stroke="#B8A27A" stroke-width="2"/>')
    # kediyu flare
    fl = "M-20,-300 L24,-300 C44,-270 58,-248 70,-224 C30,-214 -30,-214 -66,-226 C-54,-250 -38,-272 -20,-300 Z"
    out.append('<path d="%s" fill="%s"/>' % (fl, ked))
    for k in range(-5, 6):
        out.append('<path d="M%s,-298 L%s,-222" stroke="#C9B48E" stroke-width="1.6"/>' % (f(2 + k * 3.4), f(2 + k * 12)))
    out.append('<path d="M-66,-226 C-30,-214 30,-214 70,-224" stroke="%s" stroke-width="9" fill="none"/>' % trim)
    out.append('<path d="M-66,-226 C-30,-214 30,-214 70,-224" stroke="%s" stroke-width="3" stroke-dasharray="3 5" fill="none"/>' % border)
    # bodice
    out.append('<path d="M-22,-362 C0,-368 16,-368 28,-362 L24,-298 L-20,-298 Z" fill="%s"/>' % ked)
    out.append('<path d="M-22,-362 C0,-368 16,-368 28,-362 L24,-298 L-20,-298 Z" fill="%s"/>' % c.lg([(0, "#fff", 0.1), (1, "#000", 0.14)], 0, 0, 1, 0))
    out.append('<path d="M2,-364 L2,-300 M-6,-356 L10,-356" stroke="%s" stroke-width="5"/>' % trim)
    for yy in range(-352, -300, 10):
        out.append('<circle cx="9" cy="%d" r="2.2" fill="%s"/>' % (yy, border))
    # sash
    out.append('<rect x="-22" y="-306" width="48" height="12" rx="4" fill="%s"/>' % pagdi[1])
    out.append('<path d="M-18,-300 C-34,-280 -44,-262 -60,-252 L-50,-246 C-38,-260 -26,-276 -14,-294 Z" fill="%s"/>' % pagdi[1])
    # back arm + stick
    out.append(dandiya(c, *sticks[1], w=10, cols=stick))
    out.append(_arm(c, *R[1], sleeve=ked, skin=sk, bangles=(border, border, border), w=14))
    # head
    out.append('<rect x="-2" y="-378" width="14" height="18" fill="%s"/>' % sk)
    out.append('<circle cx="4" cy="-392" r="24" fill="%s"/>' % sk)
    out.append('<path d="M30,-396 L37,-386 L29,-384 Z" fill="%s"/>' % sk)
    out.append('<path d="M12,-382 C18,-378 30,-378 34,-384 C28,-380 22,-380 12,-382 Z" fill="%s"/>' % HAIR)  # mustache
    out.append('<path d="M16,-396 q4,-3 8,0" stroke="#2A1510" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    out.append('<path d="M-20,-386 C-22,-376 -16,-370 -10,-372 L-8,-388 Z" fill="%s"/>' % HAIR)
    # pagdi (turban) with folds and tail
    out.append('<path d="M-24,-398 C-28,-432 30,-440 32,-402 C18,-410 -6,-410 -24,-398 Z" fill="%s"/>' % pagdi[0])
    for k, colr in enumerate(pagdi):
        out.append('<path d="M%s,%s C-4,%s 14,%s %s,%s" stroke="%s" stroke-width="4" fill="none"/>' % (
            f(-22 + k * 2), f(-404 - k * 8), f(-418 - k * 7), f(-420 - k * 7), f(30 - k * 3), f(-406 - k * 7), colr if k else pagdi[1]))
    out.append('<path d="M-22,-402 C-44,-396 -62,-378 -68,-352 L-56,-356 C-46,-376 -32,-390 -18,-396 Z" fill="%s"/>' % pagdi[0])
    out.append('<path d="M-66,-352 l-2,8 M-60,-354 l0,8" stroke="%s" stroke-width="2.5"/>' % pagdi[1])
    out.append('<path d="M20,-428 C26,-448 40,-452 44,-440 C36,-440 30,-434 24,-424 Z" fill="%s"/>' % pagdi[2])
    out.append('<circle cx="21" cy="-424" r="4" fill="%s"/>' % border)
    # front arm + stick
    out.append(dandiya(c, *sticks[0], w=10, cols=stick))
    out.append(_arm(c, *R[0], sleeve=ked, skin=sk, bangles=(border, border, border), w=14))
    out.append("</g>")
    return "".join(out)


def dandiya(c, x1, y1, x2, y2, w=14, cols=("#E53935", "#FFD740"), tassel=True):
    """Decorated dandiya stick with spiral bands, gold caps and ghungroo tassel."""
    L = math.hypot(x2 - x1, y2 - y1)
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    out = ['<g transform="translate(%s,%s) rotate(%s)">' % (f(x1), f(y1), f(ang))]
    out.append('<rect x="0" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>' % (f(-w / 2), f(L), f(w), f(w / 2), cols[0]))
    cp = c.clip('<rect x="0" y="%s" width="%s" height="%s" rx="%s"/>' % (f(-w / 2), f(L), f(w), f(w / 2)))
    band = []
    step = w * 1.6
    k = 0
    xx = w
    while xx < L - w:
        colr = cols[1] if k % 2 == 0 else "#FFFFFF"
        band.append('<path d="M%s,%s l%s,%s l%s,0 l%s,%s z" fill="%s"/>' % (
            f(xx), f(-w / 2), f(w * 0.7), f(w), f(w * 0.45), f(-w * 0.7), f(-w), colr))
        xx += step
        k += 1
    out.append('<g clip-path="%s">%s<rect x="0" y="%s" width="%s" height="%s" fill="%s"/></g>' % (
        cp, "".join(band), f(-w / 2), f(L), f(w), c.lg([(0, "#fff", 0.45), (0.4, "#fff", 0), (1, "#000", 0.35)], 0, 0, 0, 1)))
    gcap = c.lg(["#FFF1B8", "#E0A526", "#8A5A12"], 0, 0, 0, 1)
    for cx in (w * 0.4, L - w * 0.4):
        out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="3" fill="%s"/>' % (f(cx - w * 0.55), f(-w * 0.62), f(w * 1.1), f(w * 1.24), gcap))
    # mirror bead mid
    out.append('<circle cx="%s" cy="0" r="%s" fill="#EAF2FF" stroke="%s" stroke-width="1.5"/>' % (f(L * 0.5), f(w * 0.36), "#B7791F"))
    if tassel:
        tx = L - w * 0.3
        for k, dy in enumerate((-2, 6, 14)):
            out.append('<path d="M%s,%s q%s,%s %s,%s" stroke="#B7791F" stroke-width="1.6" fill="none"/>' % (
                f(tx), f(w * 0.5), f(4 + k * 2), f(10 + dy), f(2 + k * 3), f(18 + dy)))
            out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(tx + 2 + k * 3), f(w * 0.5 + 18 + dy), f(w * 0.3), gcap))
    out.append("</g>")
    return "".join(out)


def garbo(c, cx, cy, R, body=("#C8531E", "#7A2208"), paint="#FFE08A", hole="#FFF4C8", glow=True, spill=True, flame=True):
    """Pierced garbo pot with lamp inside (light shining through holes)."""
    out = []
    if glow:
        out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(R * 2.3), c.rg([(0, "#FFC247", 0.55), (0.45, "#FF8A00", 0.18), (1, "#FF8A00", 0)])))
    if spill:
        for k in range(70):
            a = c.rnd.uniform(0, 2 * math.pi)
            rr_ = c.rnd.uniform(R * 1.35, R * 2.4)
            px, py = cx + rr_ * math.cos(a), cy + rr_ * math.sin(a) * 0.9
            out.append('<circle cx="%s" cy="%s" r="%s" fill="#FFE7A0" opacity="%s"/>' % (f(px), f(py), f(c.rnd.uniform(1.5, 4.5)), f(c.rnd.uniform(0.25, 0.8))))
    # foot
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (f(cx), f(cy + R * 0.95), f(R * 0.45), f(R * 0.12), body[1]))
    # neck
    nk = "M%s,%s L%s,%s L%s,%s L%s,%s Z" % (f(cx - R * 0.46), f(cy - R * 0.8), f(cx - R * 0.36), f(cy - R * 1.08),
                                            f(cx + R * 0.36), f(cy - R * 1.08), f(cx + R * 0.46), f(cy - R * 0.8))
    out.append('<path d="%s" fill="%s"/>' % (nk, c.lg([body[1], body[0], body[1]], 0, 0, 1, 0)))
    # body
    bg = c.rg([(0, "#FFB074"), (0.35, body[0]), (1, body[1])], 0.38, 0.32, 0.75)
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (f(cx), f(cy), f(R), f(R * 0.94), bg))
    # painted latitude bands + holes
    def proj(lat, th):
        la, t = math.radians(lat), math.radians(th)
        return cx + R * math.cos(la) * math.sin(t), cy + R * 0.94 * math.sin(la) + R * 0.16 * math.cos(la) * math.cos(t)

    hg = c.glow(5, "#FFD54F", 0.9)
    for lat in (-52, -22, 12, 44):
        p = [proj(lat, th) for th in range(-88, 89, 4)]
        out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (pts(p), paint, f(R * 0.03)))
        # small painted triangles under line
        for th in range(-80, 81, 10):
            x0, y0 = proj(lat, th)
            sc = math.cos(math.radians(th))
            out.append('<path d="M%s,%s l%s,%s l%s,%s z" fill="%s" opacity="0.9"/>' % (
                f(x0 - R * 0.035 * sc), f(y0), f(R * 0.035 * sc), f(R * 0.06), f(R * 0.035 * sc), f(-R * 0.06), paint))
    holes = []
    for row, lat in enumerate((-37, -5, 28)):
        for th in range(-78 + (row % 2) * 7, 80, 14):
            x0, y0 = proj(lat, th)
            sc = math.cos(math.radians(th))
            r = R * 0.055
            if row == 1:
                holes.append('<path d="M%s,%s l%s,%s l%s,%s l%s,%s z" fill="%s"/>' % (
                    f(x0), f(y0 - r * 1.3), f(r * sc), f(r * 1.3), f(-r * sc), f(r * 1.3), f(-r * sc), f(-r * 1.3), hole))
            else:
                holes.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (f(x0), f(y0), f(r * sc), f(r), hole))
            # tiny holes pair
            for dd in (-1, 1):
                x1, y1 = proj(lat + dd * 8.5, th)
                holes.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(x1), f(y1), f(R * 0.022 * max(0.3, sc)), hole))
    out.append('<g filter="%s">%s</g>' % (hg, "".join(holes)))
    # highlight
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff" opacity="0.18" transform="rotate(-30 %s %s)"/>' % (
        f(cx - R * 0.45), f(cy - R * 0.45), f(R * 0.22), f(R * 0.12), f(cx - R * 0.45), f(cy - R * 0.45)))
    # rim
    gld = c.lg(["#FFF1B8", "#E0A526", "#8A5A12"], 0, 0, 0, 1)
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (f(cx), f(cy - R * 1.08), f(R * 0.5), f(R * 0.13), gld))
    out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#3A1204"/>' % (f(cx), f(cy - R * 1.09), f(R * 0.38), f(R * 0.08)))
    if flame:
        out.append(flame_(c, cx, cy - R * 1.1, R * 0.7))
    return "".join(out)


def flame_(c, x, y, h):
    """Layered lamp flame with glow, base at (x,y)."""
    w = h * 0.36
    def fl(hh, ww):
        return "M%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s Z" % (
            f(x), f(y), f(x - ww * 1.3), f(y - hh * 0.25), f(x - ww * 0.3), f(y - hh * 0.6), f(x + ww * 0.1), f(y - hh),
            f(x + ww * 0.5), f(y - hh * 0.55), f(x + ww * 1.3), f(y - hh * 0.25), f(x), f(y))
    out = ['<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(x), f(y - h * 0.45), f(h * 0.9), c.rg([(0, "#FFE082", 0.6), (1, "#FF9800", 0)]))]
    out.append('<path d="%s" fill="%s"/>' % (fl(h, w), c.lg(["#FFEB3B", "#FF9800", "#E65100"], 0, 0, 0, 1)))
    out.append('<path d="%s" fill="%s"/>' % (fl(h * 0.68, w * 0.62), c.lg(["#FFFDE7", "#FFE082"], 0, 0, 0, 1)))
    out.append('<path d="%s" fill="#FFFFFF" opacity="0.9"/>' % fl(h * 0.32, w * 0.3))
    return "".join(out)


def trishul(c, x, y, h, chunri="#D50000", gold=None, cloth=True):
    """Gold trishul with a chunri tied below the head. Base of shaft at (x,y)."""
    g = gold or c.lg(["#8A5A12", "#E9B949", "#FFF1B8", "#D9A23A", "#8A5A12"], 0, 0, 1, 0)
    s = h / 600.0
    out = ['<g transform="translate(%s,%s) scale(%s)">' % (f(x), f(y), f(s))]
    out.append('<rect x="-9" y="-470" width="18" height="470" rx="6" fill="%s"/>' % g)
    for yy in (-120, -250, -380):
        out.append('<rect x="-14" y="%d" width="28" height="12" rx="4" fill="%s"/>' % (yy, g))
    head = ("M0,-600 C14,-560 18,-520 12,-480 L-12,-480 C-18,-520 -14,-560 0,-600 Z "
            "M-12,-470 C-60,-470 -96,-500 -104,-560 C-90,-534 -70,-520 -46,-520 C-60,-540 -62,-566 -54,-590 C-40,-540 -30,-500 -12,-490 Z "
            "M12,-470 C60,-470 96,-500 104,-560 C90,-534 70,-520 46,-520 C60,-540 62,-566 54,-590 C40,-540 30,-500 12,-490 Z")
    out.append('<path d="%s" fill="%s" stroke="#6B3E08" stroke-width="2"/>' % (head, g))
    out.append('<rect x="-26" y="-484" width="52" height="16" rx="6" fill="%s" stroke="#6B3E08" stroke-width="2"/>' % g)
    out.append('<circle cx="0" cy="-476" r="7" fill="#C62828"/>')
    if cloth:
        dots = c.pattern(14, 14, '<circle cx="3" cy="3" r="1.6" fill="#FFF3C0"/><circle cx="10" cy="10" r="1.6" fill="#FFF3C0"/>')
        cl = "M-16,-455 C-60,-440 -80,-400 -74,-330 C-50,-360 -30,-380 -8,-420 L8,-420 C30,-380 50,-360 74,-330 C80,-400 60,-440 16,-455 Z"
        out.append('<path d="%s" fill="%s"/><path d="%s" fill="%s"/>' % (cl, chunri, cl, dots))
        out.append('<path d="M-74,-330 C-50,-360 -30,-380 -8,-420 M74,-330 C50,-360 30,-380 8,-420" stroke="#FFC53D" stroke-width="6" fill="none"/>')
        out.append('<rect x="-18" y="-462" width="36" height="16" rx="8" fill="%s" stroke="#FFC53D" stroke-width="3"/>' % chunri)
    out.append("</g>")
    return "".join(out)


def bandhani(c, bg, dot="#FFE9B0", size=34, op=1, alt=None):
    """Bandhani tie-dye pattern fill (dot clusters)."""
    a = alt or dot
    s = size
    inner = ('<rect width="%s" height="%s" fill="%s"/>' % (f(s), f(s), bg) +
             "".join('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>' % (f(s / 4 + dx), f(s / 4 + dy), f(s * 0.045), dot, f(op))
                     for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3))) +
             '<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>' % (f(s * 0.75), f(s * 0.75), f(s * 0.06), a, f(op)) +
             "".join('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>' % (f(s * 0.75 + dx), f(s * 0.75 + dy), f(s * 0.03), a, f(op * 0.8))
                     for dx, dy in ((-6, 0), (6, 0), (0, -6), (0, 6))))
    return c.pattern(s, s, inner)


def leheriya(c, cols, size=26, angle=-35):
    inner = "".join('<rect x="0" y="%s" width="400" height="%s" fill="%s"/>' % (f(i * size / len(cols)), f(size / len(cols) + 0.5), col) for i, col in enumerate(cols))
    return c.pattern(400, size, inner, "rotate(%s)" % f(angle))


def mirror(c, cx, cy, r, thread="#E53935", petal="#FFC53D", ring=True):
    """One abhla mirror with thread ring and petal stitches."""
    m = c.rg([(0, "#FFFFFF"), (0.5, "#CFD8E6"), (1, "#7C8BA3")], 0.35, 0.3, 0.7)
    out = []
    for k in range(8):
        a = k * 45
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" transform="rotate(%s %s %s)"/>' % (
            f(cx + r * 1.5 * math.cos(math.radians(a))), f(cy + r * 1.5 * math.sin(math.radians(a))), f(r * 0.5), f(r * 0.24), petal if k % 2 == 0 else thread,
            f(a), f(cx + r * 1.5 * math.cos(math.radians(a))), f(cy + r * 1.5 * math.sin(math.radians(a)))))
    if ring:
        out.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="%s" stroke-dasharray="%s %s"/>' % (
            f(cx), f(cy), f(r * 1.12), thread, f(r * 0.34), f(r * 0.18), f(r * 0.12)))
    out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(cx), f(cy), f(r), m))
    out.append('<path d="M%s,%s a%s,%s 0 0 1 %s,%s" stroke="#fff" stroke-width="%s" fill="none" opacity="0.9"/>' % (
        f(cx - r * 0.55), f(cy - r * 0.1), f(r * 0.6), f(r * 0.6), f(r * 0.5), f(-r * 0.45), f(max(1, r * 0.12))))
    return "".join(out)


def mirror_band(c, x, y, w, h, bg="#1A1033", threads=("#E53935", "#FFC53D", "#1E9E6A", "#EC407A"), step=None, vertical=False):
    """Kutchi mirror-work embroidered band."""
    out = []
    if vertical:
        out.append('<g transform="translate(%s,%s) rotate(90)">' % (f(x + w), f(y)))
        x, y, w, h = 0, 0, h, w
    out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (f(x), f(y), f(w), f(h), bg))
    r = h * 0.2
    step = step or h * 1.05
    n = int(w / step)
    off = (w - n * step) / 2
    # edges: running stitch + herringbone
    for yy, sgn in ((y + h * 0.08, 1), (y + h * 0.92, -1)):
        out.append('<path d="M%s,%s H%s" stroke="%s" stroke-width="%s" stroke-dasharray="%s %s"/>' % (
            f(x), f(yy), f(x + w), threads[1], f(h * 0.04), f(h * 0.12), f(h * 0.06)))
        zz = []
        for i in range(int(w / (h * 0.12)) + 1):
            zz.append((x + i * h * 0.12, yy + sgn * (h * 0.05 if i % 2 else h * 0.11)))
        out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (pts(zz), threads[2], f(h * 0.025)))
    for i in range(n):
        cx = x + off + step * (i + 0.5)
        cy = y + h / 2
        out.append(mirror(c, cx, cy, r, threads[i % 2 * 3 if len(threads) > 3 else 0], threads[1]))
        # diamonds between
        dx = cx + step / 2
        if i < n - 1:
            out.append('<path d="M%s,%s l%s,%s l%s,%s l%s,%s z" fill="%s"/>' % (
                f(dx), f(cy - h * 0.2), f(h * 0.09), f(h * 0.2), f(-h * 0.09), f(h * 0.2), f(-h * 0.09), f(-h * 0.2), threads[2]))
            out.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (f(dx), f(cy), f(h * 0.04), threads[1]))
    if vertical:
        out.append("</g>")
    return "".join(out)


def cowrie(cx, cy, s, rot=0):
    return ('<g transform="translate(%s,%s) rotate(%s)"><ellipse rx="%s" ry="%s" fill="#FFF8E8" stroke="#B89B6A" stroke-width="1.2"/>'
            '<path d="M0,%s V%s" stroke="#8A6D3B" stroke-width="%s"/>'
            '<path d="M%s,%s h%s M%s,%s h%s M%s,0 h%s M%s,%s h%s" stroke="#8A6D3B" stroke-width="1"/></g>') % (
        f(cx), f(cy), f(rot), f(s * 0.62), f(s), f(-s * 0.7), f(s * 0.7), f(s * 0.12),
        f(-s * 0.2), f(-s * 0.4), f(s * 0.4), f(-s * 0.2), f(s * 0.4), f(s * 0.4), f(-s * 0.2), f(s * 0.4), f(-s * 0.2), f(-s * 0.4), f(s * 0.4))


def tassel_fringe(c, x0, x1, y, n, cols, length=70, cowries=True):
    """Hanging fringe of beaded strings ending in cowrie + woollen tassel."""
    out = []
    for i in range(n):
        x = x0 + (x1 - x0) * (i + 0.5) / n
        L = length * (0.75 + 0.25 * ((i % 3) / 2))
        colr = cols[i % len(cols)]
        out.append('<path d="M%s,%s V%s" stroke="%s" stroke-width="2"/>' % (f(x), f(y), f(y + L), colr))
        for b in range(3):
            out.append('<circle cx="%s" cy="%s" r="3.4" fill="%s"/>' % (f(x), f(y + 10 + b * 12), cols[(i + b + 1) % len(cols)]))
        if cowries:
            out.append(cowrie(x, y + L + 8, 8))
        out.append('<path d="M%s,%s l-5,20 M%s,%s l0,22 M%s,%s l5,20" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (
            f(x), f(y + L + 16), f(x), f(y + L + 16), f(x), f(y + L + 16), colr))
    return "".join(out)


def chunri_swag(c, x0, x1, y, n, depth, color="#C62828", zari="#FFC53D", dots="#FFE9A8"):
    """Draped red chunri swags across the top with gold zari lace edge and gota tassels."""
    pat = c.pattern(20, 20, '<circle cx="5" cy="5" r="1.9" fill="%s"/><circle cx="15" cy="15" r="1.9" fill="%s"/><circle cx="15" cy="5" r="1" fill="%s"/>' % (dots, dots, dots))
    out = []
    sw = (x1 - x0) / n
    shade = c.lg([(0, "#000", 0.25), (0.5, "#000", 0), (1, "#000", 0.3)], 0, 0, 0, 1)
    for i in range(n):
        a = x0 + i * sw
        b = a + sw
        m = (a + b) / 2
        d = "M%s,%s C%s,%s %s,%s %s,%s L%s,%s C%s,%s %s,%s %s,%s Z" % (
            f(a), f(y - 30), f(a + sw * 0.2), f(y + depth), f(b - sw * 0.2), f(y + depth), f(b), f(y - 30),
            f(b), f(y - 60), f(m + sw * 0.1), f(y + depth * 0.3), f(m - sw * 0.1), f(y + depth * 0.3), f(a), f(y - 60))
        out.append('<path d="%s" fill="%s"/><path d="%s" fill="%s"/><path d="%s" fill="%s"/>' % (d, color, d, pat, d, shade))
        edge = "M%s,%s C%s,%s %s,%s %s,%s" % (f(a), f(y - 30), f(a + sw * 0.2), f(y + depth), f(b - sw * 0.2), f(y + depth), f(b), f(y - 30))
        out.append('<path d="%s" fill="none" stroke="%s" stroke-width="10"/>' % (edge, zari))
        out.append('<path d="%s" fill="none" stroke="#8B1A1A" stroke-width="2" stroke-dasharray="6 6"/>' % edge)
        # tassel at swag joints
        out.append('<path d="M%s,%s v34" stroke="%s" stroke-width="3"/><path d="M%s,%s l-8,26 h16 z" fill="%s"/><circle cx="%s" cy="%s" r="6" fill="%s"/>' % (
            f(a), f(y - 30), zari, f(a), f(y + 4), zari, f(a), f(y + 4), color))
    return "".join(out)
