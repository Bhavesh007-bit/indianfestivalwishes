"""anniversary motifs (lib_c family): swans heart, candle-lit table, pocket watch + infinity chain,
love lock + key, twin coffee cups, ribbon bouquet, anniversary cake with couple topper."""
from lib_c import *


# ------------------------------------------------------------------ swan (faces right; heart-neck)
def swan(d, x, y, s=1, flip=False, body=("#FFFFFF", "#E6E4EE", "#B9B6C8"), beak="#F28A1E", reflect=False):
    gb = d.lg([(0, body[0]), (0.6, body[1]), (1, body[2])], 0, 0, 0.3, 1, key="swb%s" % body[0])
    gw = d.lg([(0, body[0]), (1, body[2])], 0, 0, 1, 1, key="sww%s" % body[0])
    o = []
    # body
    o.append('<path d="M20,-6 C24,30 -20,52 -110,48 C-190,44 -236,20 -262,-40 C-240,-26 -214,-22 -196,-30 C-170,-60 -110,-70 -60,-58 C-20,-50 12,-34 20,-6Z" fill="%s"/>' % gb)
    # neck tube (S / heart lobe)
    nfn = cub((-6, -40), (-96, -150), (-76, -300), (30, -300))
    o.append('<path d="%s" fill="%s"/>' % (tube_d(nfn, 46, 24, 70), gb))
    # head
    o.append('<ellipse cx="44" cy="-290" rx="30" ry="22" fill="%s" transform="rotate(35 44 -290)"/>' % body[0])
    o.append('<path d="M56,-300 C74,-290 90,-270 98,-246 C84,-258 70,-266 52,-276Z" fill="%s"/>' % beak)
    o.append('<path d="M40,-308 C56,-310 66,-298 66,-284 C56,-290 48,-294 40,-294Z" fill="#1E1A22"/>')
    o.append('<circle cx="46" cy="-297" r="3.2" fill="#1E1A22"/><circle cx="47" cy="-298" r="1" fill="#fff"/>')
    # neck highlight
    pts, L, R = tube_pts(nfn, 46, 24, 40)
    o.append('<path d="M%s" stroke="#fff" stroke-width="5" stroke-opacity=".7" fill="none" stroke-linecap="round"/>' % " L".join("%s,%s" % (n((a[0] * 2 + p[0]) / 3), n((a[1] * 2 + p[1]) / 3)) for a, p in list(zip(R, pts))[6:34]))
    # wing: layered feathers
    fe = []
    for row, (cnt, r0, yoff) in enumerate([(7, 60, -44), (6, 50, -30), (5, 40, -16)]):
        for k in range(cnt):
            px = -40 - k * 28 - row * 12
            py = yoff - k * 5 + row * 4
            fe.append('<path d="M%s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%sZ" fill="%s" stroke="%s" stroke-width="1.2"/>' % (
                n(px), n(py), n(px - 20), n(py - 26), n(px - r0 * 0.9), n(py - 30), n(px - r0 * 1.2), n(py - 38 + row * 6),
                n(px - r0 * 0.8), n(py + 6), n(px - 24), n(py + 10), n(px), n(py), gw, body[2]))
    o.append("".join(reversed(fe)))
    o.append('<path d="M-60,-58 C-110,-100 -200,-110 -250,-80 C-210,-70 -160,-56 -120,-40Z" fill="%s" stroke="%s" stroke-width="1.2"/>' % (gw, body[2]))
    for k in range(5):
        o.append('<path d="M%s,-%s C%s,-%s %s,-%s %s,-%s" stroke="%s" stroke-width="1.4" fill="none" opacity=".8"/>' % (
            n(-80 - k * 34), n(70 + k * 6), n(-100 - k * 34), n(90 + k * 4), n(-130 - k * 30), n(96 + k * 2), n(-160 - k * 22), n(92 - k * 2), body[2]))
    sc = "scale(%s %s)" % (n(-s if flip else s), n(-s if reflect else s))
    return '<g transform="translate(%s %s) %s">%s</g>' % (n(x), n(y), sc, "".join(o))


def swans_heart(d, cx, wy, s=1, body=("#FFFFFF", "#E6E4EE", "#B9B6C8"), water="#0E2A4A"):
    """two swans whose necks form a heart; wy = waterline; beaks meet at cx"""
    o = []
    # reflection
    refl = swan(d, cx - 100 * s, wy + 4, s, reflect=True, body=body) + swan(d, cx + 100 * s, wy + 4, s, flip=True, reflect=True, body=body)
    cp = d.clip('<rect x="0" y="%s" width="1080" height="600"/>' % n(wy))
    o.append('<g clip-path="%s" opacity=".28" filter="%s">%s</g>' % (cp, d.blur(2.5), refl))
    o.append(swan(d, cx - 100 * s, wy, s, body=body))
    o.append(swan(d, cx + 100 * s, wy, s, flip=True, body=body))
    # ripples
    for k in range(5):
        o.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="#fff" stroke-opacity="%s" stroke-width="2"/>' % (
            n(cx), n(wy + 10 + k * 8), n(300 * s + k * 60), n(12 + k * 4), n(0.45 - k * 0.07)))
    return "".join(o)


# ------------------------------------------------------------------ candles
def candle(d, x, by, w=46, h=180, wax=("#FFF8EC", "#EADCC4"), flame=True, glow=True):
    gw = d.lg([(0, wax[1]), (0.35, wax[0]), (0.7, wax[0]), (1, wax[1])], 0, 0, 1, 0, key="cw%s" % wax[0])
    o = []
    if glow:
        o.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(x), n(by - h - 30), n(w * 2.6), d.rg([(0, "#FFD27A", .75), (0.4, "#FFB347", .3), (1, "#FFB347", 0)])))
    o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="4" fill="%s"/>' % (n(x - w / 2), n(by - h), n(w), n(h), gw))
    o.append('<path d="M%s,%s C%s,%s %s,%s %s,%s L%s,%s C%s,%s %s,%s %s,%sZ" fill="%s"/>' % (
        n(x - w / 2), n(by - h + 2), n(x - w / 4), n(by - h + 14), n(x - w / 8), n(by - h + 30), n(x - w / 10), n(by - h + 40),
        n(x), n(by - h + 20), n(x + w / 6), n(by - h + 26), n(x + w / 3), n(by - h + 12), n(x + w / 2), n(by - h + 2), wax[0]))
    o.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (n(x), n(by - h), n(w / 2), n(w * 0.12), wax[0]))
    o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#3A2A1A" stroke-width="2"/>' % (n(x), n(by - h), n(x), n(by - h - 10)))
    if flame:
        f = "M0,0 C-10,-8 -12,-26 0,-50 C12,-26 10,-8 0,0Z"
        o.append('<g transform="translate(%s %s) scale(%s)" filter="%s"><path d="%s" fill="#FFB347"/><path d="%s" fill="#FFF3C4" transform="scale(.55) translate(0 -4)"/></g>' % (
            n(x), n(by - h - 8), n(w / 46), d.glow(6, "#FFB347", 0.9), f, f))
    return "".join(o)


def wine_glass(d, x, by, s=1, drink="#E8456A"):
    o = []
    o.append('<ellipse cx="0" cy="0" rx="34" ry="7" fill="#fff" opacity=".55"/>')
    o.append('<rect x="-3" y="-110" width="6" height="110" fill="#fff" opacity=".6"/>')
    o.append('<path d="M-40,-240 C-44,-180 -26,-120 0,-112 C26,-120 44,-180 40,-240Z" fill="#fff" opacity=".22" stroke="#fff" stroke-opacity=".7" stroke-width="2"/>')
    o.append('<path d="M-40,-190 C-36,-150 -22,-120 0,-114 C22,-120 36,-150 40,-190Z" fill="%s" opacity=".85"/>' % drink)
    o.append('<ellipse cx="0" cy="-190" rx="40" ry="6" fill="%s"/>' % drink)
    o.append('<path d="M-30,-230 C-32,-190 -24,-150 -12,-130" stroke="#fff" stroke-width="4" stroke-opacity=".7" fill="none" stroke-linecap="round"/>')
    return g("".join(o), x, by, s)


def candle_table(d, cx, by, s=1, cloth=("#FFF8F0", "#E8D6C8"), drink="#E8456A", roses=("red", "wine")):
    """round dinner table (front view) with candles, vase of roses and two glasses; by = floor line"""
    gc = d.lg([(0, cloth[0]), (1, cloth[1])], 0, 0, 0, 1, key="tc%s" % cloth[0])
    o = ['<ellipse cx="0" cy="0" rx="330" ry="26" fill="#000" opacity=".3"/>']
    top = -300
    # cloth drape
    o.append('<path d="M-300,%d C-310,-150 -320,-60 -340,0 L340,0 C320,-60 310,-150 300,%dZ" fill="%s"/>' % (top, top, gc))
    for k in range(-5, 6):
        o.append('<path d="M%s,%d C%s,-150 %s,-60 %s,0" stroke="#000" stroke-opacity=".07" stroke-width="10" fill="none"/>' % (n(k * 55), top + 20, n(k * 56), n(k * 60), n(k * 62)))
    o.append('<ellipse cx="0" cy="%d" rx="300" ry="40" fill="%s"/>' % (top, cloth[0]))
    # lace hem
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="3"/>' % (" ".join("M%s,-6 q%s,16 %s,0" % (n(-338 + i * 26), 13, 26) for i in range(26)), d.gold()))
    # runner: lies across the table top and hangs over the front edge
    gr_ = d.lg([(0, "#B3123E"), (1, "#6E0A28")], key="runner")
    o.append('<path d="M-38,%d L38,%d L58,%d L-58,%dZ" fill="%s" opacity=".9"/>' % (top - 36, top - 36, top + 38, top + 38, gr_))
    o.append('<path d="M-58,%d L58,%d L62,%d L-62,%dZ" fill="%s"/>' % (top + 38, top + 38, top + 170, top + 170, gr_))
    o.append('<path d="M-62,%d L62,%d" stroke="%s" stroke-width="5"/>' % (top + 170, top + 170, d.gold()))
    o.append('<path d="M-58,%d L58,%d" stroke="%s" stroke-width="2" opacity=".8"/>' % (top + 40, top + 40, d.gold()))
    for k in range(-2, 3):
        o.append(dots_ring(1, 0, 0, "none") + '<path d="M%s,%d l7,9 l-7,9 l-7,-9Z" fill="%s"/>' % (n(k * 22), top + 90, d.gold()))
    o.append(tassel(d, -62, top + 170, 0.5, "#6E0A28") + tassel(d, 62, top + 170, 0.5, "#6E0A28"))
    # candelabra candles
    gold = d.gold()
    o.append(candle(d, -170, top - 6, 30, 150))
    o.append(candle(d, 170, top - 6, 30, 150))
    o.append('<rect x="-190" y="%d" width="40" height="10" rx="4" fill="%s"/><rect x="150" y="%d" width="40" height="10" rx="4" fill="%s"/>' % (top - 10, gold, top - 10, gold))
    # vase with roses
    o.append('<path d="M-36,%d C-60,%d -50,%d -24,%d L24,%d C50,%d 60,%d 36,%dZ" fill="%s"/>' % (top - 10, top - 50, top - 100, top - 120, top - 120, top - 100, top - 50, top - 10, d.lg([(0, "#FFFFFF"), (1, "#C9D6E8")], 0, 0, 1, 0)))
    rr = random.Random(4)
    for k in range(12):
        a = math.radians(-90 + rr.uniform(-70, 70))
        o.append(leaf(d, 70 * math.cos(a), top - 150 + 50 * math.sin(a), 44, 13, math.degrees(a) + 90, "#4E7A3A", "#1F4E22"))
    for k, (dx, dy, r_) in enumerate([(0, -190, 24), (-40, -160, 20), (40, -162, 20), (-20, -212, 17), (24, -214, 17), (-62, -134, 16), (62, -136, 16)]):
        o.append(rose(d, dx, top + dy + 10, r_, roses[k % 2], k * 40))
    # glasses
    o.append(wine_glass(d, -90, top + 4, 0.62, drink))
    o.append(wine_glass(d, 90, top + 4, 0.62, drink))
    # rose petals on cloth
    return g("".join(o), cx, by, s)


# ------------------------------------------------------------------ pocket watch + infinity chain
def pocket_watch(d, cx, cy, R=150, face=("#FFFDF6", "#EFE3CC"), accent="#1E2A44"):
    gold = d.gold()
    o = []
    o.append('<circle cx="%s" cy="%s" r="%s" fill="#000" opacity=".3" filter="%s"/>' % (n(cx + 6), n(cy + 14), n(R + 18), d.blur(10)))
    # bow + crown
    o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="6" fill="%s"/>' % (n(cx - R * 0.14), n(cy - R - 34), n(R * 0.28), 40, gold))
    o.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (n(cx), n(cy - R - 58), n(R * 0.17), gold, n(R * 0.06)))
    for k in range(5):
        o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#7A4A0E" stroke-width="2"/>' % (n(cx - R * 0.12 + k * R * 0.06), n(cy - R - 32), n(cx - R * 0.12 + k * R * 0.06), n(cy - R + 4)))
    # case
    o.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(cx), n(cy), n(R + 16), gold))
    o.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="#7A4A0E" stroke-width="2"/>' % (n(cx), n(cy), n(R + 6)))
    o.append(dots_ring(60, R + 10, 2.2, "#FFF3C4", cx, cy))
    o.append('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (n(cx), n(cy), n(R), d.rg([(0, face[0]), (1, face[1])], 0.4, 0.35, 0.8)))
    # guilloche rosette
    o.append(ring_petals(24, R * 0.12, R * 0.52, R * 0.06, "none", "#C8A46A", 1, 0, cx, cy))
    o.append(ring_petals(24, R * 0.12, R * 0.52, R * 0.06, "none", "#C8A46A", 1, 7.5, cx, cy))
    o.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="2"/>' % (n(cx), n(cy), n(R * 0.72), accent))
    for k in range(60):
        a = math.radians(k * 6)
        r0 = R * (0.8 if k % 5 == 0 else 0.86)
        o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"/>' % (
            n(cx + r0 * math.cos(a)), n(cy + r0 * math.sin(a)), n(cx + R * 0.92 * math.cos(a)), n(cy + R * 0.92 * math.sin(a)), accent, 4 if k % 5 == 0 else 1.5))
    for k in range(12):
        a = math.radians(k * 30)
        o.append('<path d="M0,-9 L7,0 L0,9 L-7,0Z" fill="%s" transform="translate(%s %s) rotate(%s)"/>' % (gold, n(cx + R * 0.64 * math.cos(a)), n(cy + R * 0.64 * math.sin(a)), n(k * 30)))
    # hands: heart tip
    def hand(ang, L, w):
        a = math.radians(ang - 90)
        ex, ey = cx + L * math.cos(a), cy + L * math.sin(a)
        return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (n(cx), n(cy), n(ex), n(ey), accent, w) +
                '<path d="%s" fill="%s" transform="rotate(%s %s %s)"/>' % (shape_d("heart", ex - 9, ey - 9, 18, 16), accent, n(ang), n(ex), n(ey)))
    o.append(hand(300, R * 0.48, 6) + hand(62, R * 0.7, 4))
    o.append('<circle cx="%s" cy="%s" r="8" fill="%s"/><circle cx="%s" cy="%s" r="3" fill="%s"/>' % (n(cx), n(cy), gold, n(cx), n(cy), accent))
    # glass glare
    o.append('<path d="M%s,%s A%s,%s 0 0 1 %s,%s" stroke="#fff" stroke-width="%s" stroke-opacity=".5" fill="none" stroke-linecap="round"/>' % (
        n(cx - R * 0.7), n(cy - R * 0.3), n(R * 0.76), n(R * 0.76), n(cx - R * 0.2), n(cy - R * 0.74), n(R * 0.06)))
    return "".join(o)


def chain(d, pts_fn, link=14, col=None):
    """chain of alternating ellipse links along parametric fn"""
    c = col or d.gold()
    o = []
    for i, ((x, y), a) in enumerate(sample(pts_fn, link * 0.9, 800)):
        if i % 2:
            o.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width="3.2" transform="rotate(%s %s %s)"/>' % (n(x), n(y), n(link * 0.6), n(link * 0.34), c, n(a), n(x), n(y)))
        else:
            o.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" transform="rotate(%s %s %s)"/>' % (n(x), n(y), n(link * 0.6), n(link * 0.16), c, n(a), n(x), n(y)))
    return "".join(o)


def infinity_fn(cx, cy, a, b=None):
    b = b or a * 0.5
    return lambda t: (cx + a * math.cos(2 * math.pi * t) / (1 + math.sin(2 * math.pi * t) ** 2),
                      cy + a * 1.3 * math.sin(2 * math.pi * t) * math.cos(2 * math.pi * t) / (1 + math.sin(2 * math.pi * t) ** 2))


# ------------------------------------------------------------------ love lock + key
def love_lock(d, cx, cy, s=1, body=None, engrave=True):
    gold = body or d.lg([(0, "#FFF0B5"), (0.35, "#E9C46A"), (0.7, "#C8922E"), (1, "#7A4A0E")], 0.2, 0, 0.8, 1, key="lockg")
    o = []
    # shackle
    o.append('<path d="M-62,-40 L-62,-120 C-62,-190 62,-190 62,-120 L62,-40" fill="none" stroke="%s" stroke-width="22" stroke-linecap="round"/>' % d.lg(SILVER, 0, 0, 1, 0, key="silh"))
    o.append('<path d="M-70,-120 C-66,-170 -30,-186 0,-186" fill="none" stroke="#fff" stroke-width="5" stroke-opacity=".6" stroke-linecap="round"/>')
    # heart body
    o.append('<path d="%s" fill="%s" filter="%s"/>' % (shape_d("heart", -120, -80, 240, 230), gold, d.shadow(0, 10, 12, "#000", .35)))
    o.append('<path d="%s" fill="none" stroke="#7A4A0E" stroke-width="2.5"/>' % shape_d("heart", -106, -64, 212, 204))
    o.append('<path d="M-80,-50 C-110,-40 -110,10 -80,50" stroke="#fff" stroke-width="10" stroke-opacity=".45" fill="none" stroke-linecap="round"/>')
    # keyhole
    o.append('<circle cx="0" cy="30" r="16" fill="#3A220A"/><path d="M-9,36 L9,36 L14,80 L-14,80Z" fill="#3A220A"/>')
    if engrave:
        o.append(dots_ring(18, 70, 2.4, "#7A4A0E", 0, 30, 0, 0.6))
    return g("".join(o), cx, cy, s)


def heart_key(d, x, y, s=1, rot=0):
    gold = d.lg([(0, "#FFF0B5"), (0.4, "#E9C46A"), (1, "#8C5A17")], 0, 0, 1, 1, key="keyg")
    o = []
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="14"/>' % (shape_d("heart", -54, -58, 108, 100), gold))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="6"/>' % (shape_d("heart", -30, -34, 60, 56), gold))
    o.append('<rect x="-8" y="40" width="16" height="200" rx="5" fill="%s"/>' % gold)
    o.append('<rect x="-18" y="44" width="36" height="10" rx="4" fill="%s"/>' % gold)
    o.append('<path d="M8,180 L44,180 L44,196 L30,196 L30,208 L44,208 L44,236 L8,236Z" fill="%s"/>' % gold)
    o.append('<line x1="-2" y1="60" x2="-2" y2="230" stroke="#fff" stroke-opacity=".55" stroke-width="3"/>')
    return g("".join(o), x, y, s, rot)


def satin_bow(d, x, y, s=1, col=("#E8456A", "#9E1030")):
    gr = d.lg([(0, col[0]), (1, col[1])], 0, 0, 1, 1, key="bow%s" % col[0])
    o = []
    o.append('<path d="M-6,6 C-30,60 -50,110 -70,160 L-44,150 L-30,176 C-16,120 0,60 6,10Z" fill="%s"/>' % gr)
    o.append('<path d="M6,6 C30,60 56,110 78,150 L52,146 L42,172 C24,120 8,60 -2,10Z" fill="%s"/>' % gr)
    o.append('<path d="M0,0 C-40,-60 -120,-70 -110,-10 C-104,30 -40,20 0,0Z" fill="%s"/>' % gr)
    o.append('<path d="M0,0 C40,-60 120,-70 110,-10 C104,30 40,20 0,0Z" fill="%s"/>' % gr)
    o.append('<path d="M-10,-4 C-40,-40 -90,-44 -92,-14" stroke="#fff" stroke-opacity=".35" stroke-width="5" fill="none"/>')
    o.append('<path d="M10,-4 C40,-40 90,-44 92,-14" stroke="#000" stroke-opacity=".15" stroke-width="5" fill="none"/>')
    o.append('<ellipse cx="0" cy="0" rx="18" ry="22" fill="%s"/>' % col[1])
    return g("".join(o), x, y, s)


# ------------------------------------------------------------------ twin coffee cups
def coffee_cup(d, x, by, s=1, flip=False, cup=("#FFFFFF", "#D9D2C8"), band="#B3123E", latte=True):
    gc = d.lg([(0, cup[1]), (0.3, cup[0]), (0.6, cup[0]), (1, cup[1])], 0, 0, 1, 0, key="cup%s" % cup[0])
    o = []
    # saucer
    o.append('<ellipse cx="0" cy="-6" rx="150" ry="26" fill="%s"/>' % gc)
    o.append('<ellipse cx="0" cy="-12" rx="110" ry="16" fill="%s"/>' % cup[1])
    # handle
    o.append('<path d="M86,-150 C150,-150 150,-60 70,-60" fill="none" stroke="%s" stroke-width="20"/>' % cup[1])
    o.append('<path d="M86,-150 C140,-150 140,-66 72,-66" fill="none" stroke="%s" stroke-width="10"/>' % cup[0])
    # body
    o.append('<path d="M-104,-176 L104,-176 C100,-90 70,-24 0,-20 C-70,-24 -100,-90 -104,-176Z" fill="%s"/>' % gc)
    o.append('<path d="M-102,-150 L102,-150 L99,-128 L-99,-128Z" fill="%s"/>' % band)
    o.append(dots_ring(1, 0, 0, "none"))
    for k in range(9):
        o.append('<path d="M%s,-139 m0,-6 l6,6 l-6,6 l-6,-6Z" fill="%s"/>' % (n(-80 + k * 20), d.gold()))
    o.append('<path d="M-80,-160 C-78,-100 -60,-60 -34,-40" stroke="#fff" stroke-width="8" stroke-opacity=".7" fill="none" stroke-linecap="round"/>')
    # rim + coffee
    o.append('<ellipse cx="0" cy="-176" rx="104" ry="20" fill="%s"/>' % cup[0])
    o.append('<ellipse cx="0" cy="-174" rx="92" ry="15" fill="%s"/>' % d.rg([(0, "#D9A878"), (0.7, "#8A5230"), (1, "#5A3018")]))
    if latte:
        o.append('<path d="%s" fill="#FFF3E0" opacity=".9" transform="translate(0 -174) scale(1 .32) translate(0 -8)"/>' % shape_d("heart", -30, -26, 60, 52))
    sc = "scale(%s %s)" % (n(-s if flip else s), n(s))
    return '<g transform="translate(%s %s) %s">%s</g>' % (n(x), n(by), sc, "".join(o))


def steam_heart(d, x1, y1, x2, y2, top, col="#FFFFFF", op=0.8, hw=None):
    """two steam wisps rising from x1,y1 and x2,y2 that meet in a soft heart whose top is at `top`"""
    cx = (x1 + x2) / 2
    hw = hw or (x2 - x1) * 0.62
    hh = hw * 0.9
    hy = top
    o = []
    # heart outline as a tapered stroke (thick at the lobes, thin at the point)
    pts = heart_pts(cx - hw / 2, hy, hw, hh, 240)
    for half in (pts[:121], pts[120:]):
        fn = lambda t, h=half: h[min(len(h) - 1, int(t * (len(h) - 1)))]
        o.append('<path d="%s" fill="%s" opacity="%s"/>' % (tube_d(fn, 8, 8, 120, lambda t: 5 + 15 * math.sin(math.pi * t) ** 0.7), col, op))
    by = hy + hh
    for sg, xs, ys in ((-1, x1, y1), (1, x2, y2)):
        fn = cub((xs, ys), (xs - sg * 40, ys - (ys - by) * 0.35), (cx + sg * 70, by + (ys - by) * 0.5), (cx, by))
        o.append('<path d="%s" fill="%s" opacity="%s"/>' % (tube_d(fn, 6, 14, 60, lambda t: 5 + 12 * math.sin(math.pi * t)), col, op * 0.85))
    return '<g filter="%s">%s</g>' % (d.blur(1.8), "".join(o))


# ------------------------------------------------------------------ bouquet
def bouquet(d, cx, by, s=1, wrap=("#F7E7D6", "#D9BFA4"), flowers=("blush", "peach", "white", "pink"), ribbon=("#C9A0DC", "#7E58A6"), seed=3):
    rr = random.Random(seed)
    o = []
    # stems
    for k in range(9):
        o.append('<path d="M%s,-40 L%s,160" stroke="#4E7A3A" stroke-width="7"/>' % (n(-30 + k * 7), n(-10 + k * 2.5)))
    # back leaves / greenery
    for k in range(26):
        a = rr.uniform(-160, -20)
        rad = rr.uniform(120, 200)
        o.append(leaf(d, rad * math.cos(math.radians(a)) * 0.9, -170 + rad * math.sin(math.radians(a)) * 0.8 + 80, rr.uniform(60, 96), rr.uniform(16, 24), a + 90, rr.choice(["#6E9E5A", "#8FB08A"]), "#2F5E2A"))
    # eucalyptus sprigs
    for sg in (-1, 1):
        for k in range(7):
            px, py = sg * (120 + k * 16), -200 - k * 24
            o.append('<circle cx="%s" cy="%s" r="11" fill="#A9C4B0" stroke="#6E8F7A" stroke-width="1.5"/>' % (n(px), n(py)))
    # flowers dome
    spots = [(0, -250, 58), (-90, -220, 50), (90, -220, 50), (-45, -170, 46), (48, -168, 46), (-150, -160, 40), (150, -160, 40), (0, -140, 40),
             (-60, -300, 38), (60, -300, 38), (-110, -280, 30), (110, -280, 30), (0, -330, 30)]
    for i, (px, py, r_) in enumerate(spots):
        f = bloom if i % 3 == 0 else rose
        o.append(f(d, px, py, r_, flowers[i % len(flowers)], i * 37))
    # baby's breath
    for k in range(40):
        a = rr.uniform(0, math.pi)
        o.append('<circle cx="%s" cy="%s" r="%s" fill="#FFFFFF"/>' % (n(rr.uniform(-190, 190)), n(rr.uniform(-340, -110)), n(rr.uniform(2.5, 5))))
    # wrap paper cone
    gw = d.lg([(0, wrap[0]), (0.5, "#FFFFFF"), (1, wrap[1])], 0, 0, 1, 0, key="wrap%s" % wrap[0])
    o.append('<path d="M-200,-150 L-40,180 L40,180 L200,-150 C120,-110 60,-120 0,-90 C-60,-120 -120,-110 -200,-150Z" fill="%s"/>' % gw)
    o.append('<path d="M-200,-150 C-120,-110 -60,-120 0,-90 L-20,180 L-40,180Z" fill="%s" opacity=".6"/>' % wrap[1])
    o.append('<path d="M-200,-150 L-40,180 M200,-150 L40,180" stroke="%s" stroke-width="2" opacity=".6"/>' % wrap[1])
    o.append(satin_bow(d, 0, 70, 0.9, ribbon))
    return g("".join(o), cx, by, s)


# ------------------------------------------------------------------ anniversary cake with couple topper
def couple_topper(d, x, y, s=1, col="#2A1A22", trim=None):
    gf = trim or d.gold()
    o = []
    # man (left) in suit
    o.append('<circle cx="-30" cy="-190" r="16" fill="%s"/>' % col)
    o.append('<path d="M-52,-168 C-44,-176 -16,-176 -8,-168 L-4,-80 L-12,-80 L-14,0 L-26,0 L-30,-70 L-34,0 L-46,0 L-48,-80 L-56,-80Z" fill="%s"/>' % col)
    o.append('<path d="M-30,-168 L-26,-150 L-34,-150Z" fill="%s"/>' % gf)
    # woman (right) in gown, leaning in
    o.append('<circle cx="12" cy="-180" r="14" fill="%s"/><circle cx="24" cy="-178" r="9" fill="%s"/>' % (col, col))
    o.append('<path d="M2,-162 L22,-162 C26,-140 26,-120 22,-104 C40,-60 56,-20 64,0 L-20,0 C-12,-30 -4,-70 4,-104 C0,-120 0,-140 2,-162Z" fill="%s"/>' % col)
    o.append('<path d="M-16,-8 Q20,2 60,-8" stroke="%s" stroke-width="3" fill="none"/>' % gf)
    # joined hands
    o.append('<path d="M-10,-150 C0,-130 4,-120 6,-112" stroke="%s" stroke-width="8" stroke-linecap="round" fill="none"/>' % col)
    # heart above
    o.append('<path d="%s" fill="%s"/>' % (shape_d("heart", -22, -250, 36, 32), gf))
    return g("".join(o), x, y, s)


def cake(d, cx, by, s=1, icing=("#FFF7F2", "#F3DCD6"), drip="#F2A7C1", roses=("pink", "blush", "white"), stand=True):
    gi = d.lg([(0, icing[1]), (0.3, icing[0]), (0.7, icing[0]), (1, icing[1])], 0, 0, 1, 0, key="ice%s" % icing[0])
    o = []
    y = 0
    if stand:
        gs = d.gold()
        o.append('<ellipse cx="0" cy="0" rx="120" ry="16" fill="%s"/><rect x="-16" y="-60" width="32" height="60" fill="%s"/>' % (gs, gs))
        o.append('<ellipse cx="0" cy="-60" rx="250" ry="22" fill="%s"/><ellipse cx="0" cy="-66" rx="236" ry="16" fill="#FFFFFF" opacity=".5"/>' % gs)
        y = -66
    tiers = [(420, 150), (310, 130), (210, 110)]
    for i, (w_, h_) in enumerate(tiers):
        top = y - h_
        o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="10" fill="%s"/>' % (n(-w_ / 2), n(top), n(w_), n(h_), gi))
        o.append('<ellipse cx="0" cy="%s" rx="%s" ry="14" fill="%s"/>' % (n(top), n(w_ / 2), icing[0]))
        # drips
        dp = "M%s,%s " % (n(-w_ / 2), n(top))
        k = int(w_ / 26)
        rr = random.Random(i + 3)
        for j in range(k):
            x0 = -w_ / 2 + j * w_ / k
            L = rr.uniform(14, 42)
            dp += "L%s,%s C%s,%s %s,%s %s,%s " % (n(x0 + 3), n(top + L - 8), n(x0 + 3), n(top + L + 6), n(x0 + w_ / k - 3), n(top + L + 6), n(x0 + w_ / k - 3), n(top + L - 8))
        dp += "L%s,%s Z" % (n(w_ / 2), n(top))
        o.append('<path d="%s" fill="%s"/>' % (dp, drip))
        o.append('<ellipse cx="0" cy="%s" rx="%s" ry="12" fill="%s"/>' % (n(top - 1), n(w_ / 2 - 2), drip))
        # pearls at base
        o.append(bead_line(-w_ / 2 + 8, y - 6, w_ / 2 - 8, y - 6, 14, 5, "#FFFFFF"))
        o.append(bead_line(-w_ / 2 + 8, y - 6, w_ / 2 - 8, y - 6, 14, 2, "#E9D6C8"))
        # swag piping
        for j in range(int(w_ / 70)):
            x0 = -w_ / 2 + 12 + j * 70
            o.append('<path d="M%s,%s q35,26 70,0" stroke="#FFFFFF" stroke-width="4" fill="none"/>' % (n(x0), n(top + h_ * 0.5)))
            o.append('<circle cx="%s" cy="%s" r="5" fill="%s"/>' % (n(x0), n(top + h_ * 0.5), d.gold()))
        # side highlight
        o.append('<rect x="%s" y="%s" width="10" height="%s" rx="5" fill="#fff" opacity=".6"/>' % (n(-w_ / 2 + 22), n(top + 44), n(h_ - 60)))
        y = top
    # roses cascade
    cas = [(-150, -196, 26), (-120, -210, 20), (-176, -180, 18), (120, -340, 22), (96, -350, 17), (140, -330, 16), (-70, -470, 18), (-50, -480, 14)]
    for i, (px, py, r_) in enumerate(cas):
        o.append(leaf(d, px + 20, py + 6, 30, 10, 60 + i * 40, "#6E9E5A", "#2F5E2A"))
        o.append(rose(d, px, py + (y and 0), r_, roses[i % len(roses)], i * 40))
    o.append(couple_topper(d, 0, y - 6, 0.95))
    return g("".join(o), cx, by, s)
