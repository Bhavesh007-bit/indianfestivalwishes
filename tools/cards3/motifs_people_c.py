"""Refined bride & groom figures (lib_c family) for wedding wishes.

Both are drawn in profile facing right (flip=True faces left), feet at (0,0), ~540 units tall at s=1.
groom: sherwani with gold embroidery, churidar, juttis, maroon stole, pearl malas, saffa with kalgi,
       turra tail and a pearl sehra over the face.
bride: lehenga with pleats and heavy gold border, choli, sheer dupatta over the head with gota edge,
       maang tikka, nath with chain, jhumka, rani haar, chooda with kaleeras, bindi.
Poses: "stand", "walk" (groom), "varmala" (hands raised forward holding a garland).
Varmala hand points (unscaled): groom (108,-358), bride (98,-338).
shade=(color, opacity) darkens the whole figure for backlit scenes; rim=color adds rim light.
"""
from lib_c import *

SKIN = ("#F0C29C", "#D99A70", "#A8663E")


def _shade_filter(d, col, op):
    return d.filt("shade%s%s" % (col, op),
                  '<feFlood flood-color="%s" flood-opacity="%s" result="f"/><feComposite in="f" in2="SourceAlpha" operator="in" result="s"/>'
                  '<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="s"/></feMerge>' % (col, op), pad=5)


def _wrap(d, o, x, y, s, flip, shade):
    body = "".join(o)
    if shade:
        body = '<g filter="%s">%s</g>' % (_shade_filter(d, shade[0], shade[1]), body)
    sc = "scale(%s %s)" % (n(-s if flip else s), n(s))
    return '<g transform="translate(%s %s) %s">%s</g>' % (n(x), n(y), sc, body)


def _limb(fn, w0, w1, fill, steps=30):
    return '<path d="%s" fill="%s"/>' % (tube_d(fn, w0, w1, steps), fill)


def _poly(pts):
    return "M" + " L".join("%s,%s" % (n(a), n(b)) for a, b in pts)


def _arm_fn(p0, p1, p2):
    """shoulder -> elbow -> hand as a smooth quadratic-ish cubic"""
    return cub(p0, (p0[0] + (p1[0] - p0[0]) * 1.2, p0[1] + (p1[1] - p0[1]) * 1.2), (p1[0] + (p2[0] - p1[0]) * 0.2, p1[1] + (p2[1] - p1[1]) * 0.2), p2)


# ================================================================== GROOM
def groom(d, x, y, s=1, flip=False, pose="stand", sherwani=("#FFF8E8", "#EBD8B0", "#B8966A"), safa=("#F9A825", "#E0591B", "#B3261E"),
          stole=("#9E1030", "#5A0618"), skin=SKIN, rim=None, shade=None, body=None, trim=None):
    gold = trim or d.gold()
    goldv = d.lg(GOLD, 0, 0, 0, 1, key="goldv")
    gs = d.lg([(0, sherwani[2]), (0.3, sherwani[1]), (0.62, sherwani[0]), (1, sherwani[1])], 0, 0, 1, 0, key="shw%s" % sherwani[0])
    gsk = d.lg([(0, skin[2]), (0.45, skin[1]), (1, skin[0])], 0, 0, 1, 0, key="gsk%s" % skin[0])
    gch = d.lg([(0, "#D9CDB6"), (0.5, "#FFFBF2"), (1, "#E6DCC8")], 0, 0, 1, 0, key="chur")
    gst = d.lg([(0, stole[0]), (1, stole[1])], 0, 0, 1, 1, key="stl%s" % stole[0])
    gsf = d.rg([(0, safa[0]), (0.55, safa[1]), (1, safa[2])], 0.7, 0.3, 0.9, key="safa%s" % safa[0])
    o = []
    # ---- turra (safa tail) behind the back
    o.append(_limb(cub((-26, -452), (-52, -430), (-50, -380), (-62, -318)), 26, 18, gsf))
    o.append('<path d="M-72,-322 L-50,-314 L-52,-300 L-74,-306Z" fill="%s"/>' % goldv)
    for k in range(6):
        o.append('<line x1="%s" y1="-304" x2="%s" y2="-286" stroke="%s" stroke-width="2"/>' % (n(-72 + k * 4), n(-73 + k * 4), gold))
    # ---- back arm (behind body) for walk / varmala
    if pose == "walk":
        o.append(_limb(_arm_fn((-18, -380), (-44, -300), (-54, -236)), 28, 22, sherwani[2]))
        o.append('<ellipse cx="-55" cy="-228" rx="10" ry="12" fill="%s"/>' % skin[2])
    # ---- legs (churidar)
    if pose == "walk":
        legs = [((-18, -186), (-50, -14)), ((12, -186), (46, -12))]
    else:
        legs = [((-20, -186), (-22, -12)), ((10, -186), (14, -12))]
    for (a, b) in legs:
        fn = cub(a, (a[0] + (b[0] - a[0]) * 0.3, a[1] + 60), (b[0], b[1] - 60), b)
        o.append(_limb(fn, 34, 22, gch))
        for k in range(5):  # ruching near ankle
            t = 0.72 + k * 0.05
            px, py = fn(t)
            o.append('<path d="M%s,%s q11,5 22,0" stroke="#C9BBA0" stroke-width="1.5" fill="none"/>' % (n(px - 11), n(py)))
    # juttis with curled toe
    for (a, b) in legs:
        bx = b[0]
        o.append('<path d="M%s,-12 L%s,-12 C%s,-14 %s,-6 %s,-16 C%s,-4 %s,0 %s,0 L%s,0Z" fill="%s"/>' % (
            n(bx - 16), n(bx + 18), n(bx + 28), n(bx + 36), n(bx + 44), n(bx + 42), n(bx + 36), n(bx + 26), n(bx - 16), d.lg([(0, "#B3261E"), (1, "#6E0A1C")], key="jut")))
        o.append('<path d="M%s,-11 L%s,-11" stroke="%s" stroke-width="3"/>' % (n(bx - 14), n(bx + 22), gold))
    # ---- sherwani body
    sh = "M-40,-394 C-54,-372 -56,-332 -52,-292 L-62,-172 Q-4,-160 58,-172 L46,-292 C50,-322 48,-362 36,-388 C22,-400 -18,-402 -40,-394Z"
    o.append('<path d="%s" fill="%s"/>' % (sh, gs))
    cp = d.clip('<path d="%s"/>' % sh)
    emb = []
    rr = random.Random(11)
    for k in range(46):
        px, py = rr.uniform(-58, 50), rr.uniform(-380, -190)
        emb.append('<g transform="translate(%s %s)">%s</g>' % (n(px), n(py), ring_petals(4, 0.5, 4.5, 2, sherwani[2], "none", 1, rr.randint(0, 90))))
    emb.append('<path d="M-60,-212 Q-4,-200 56,-212 L58,-172 Q-4,-160 -62,-172Z" fill="%s"/>' % goldv)
    for k in range(12):
        emb.append('<path d="M%s,-196 l6,-7 l6,7 l-6,7Z" fill="%s"/>' % (n(-54 + k * 9.5), stole[0]))
    emb.append('<path d="M28,-388 C40,-340 42,-260 52,-172" stroke="%s" stroke-width="9" fill="none"/>' % goldv)
    emb.append('<path d="M-46,-300 C-20,-296 20,-296 46,-300" stroke="#000" stroke-opacity=".08" stroke-width="10" fill="none"/>')
    o.append('<g clip-path="%s">%s</g>' % (cp, "".join(emb)))
    for k in range(7):
        px = 34 + k * 1.6
        o.append('<circle cx="%s" cy="%s" r="3.2" fill="#FFF3C4" stroke="#8A5A12" stroke-width="1"/>' % (n(px), n(-370 + k * 26)))
    # stole: over the shoulder, hanging at back + across chest
    o.append('<path d="M-34,-396 C-14,-404 6,-404 18,-398 L20,-386 C4,-392 -16,-390 -30,-384Z" fill="%s"/>' % gst)
    o.append(_limb(cub((-36, -390), (-58, -340), (-60, -280), (-66, -222)), 28, 30, gst))
    o.append('<path d="M-80,-226 L-52,-218 L-54,-206 L-82,-212Z" fill="%s"/>' % goldv)
    o.append('<path d="M-36,-390 C-58,-340 -60,-280 -66,-222" stroke="%s" stroke-width="3" fill="none" transform="translate(12 0)"/>' % gold)
    # pearl malas
    for k, (dy, cnt) in enumerate(((0, 14), (14, 16), (28, 18))):
        fn = cub((-6, -388), (-2, -360 + dy), (18, -336 + dy), (40, -350 + dy * 0.6))
        for i, ((px, py), a) in enumerate(sample(fn, 5.6)):
            o.append('<circle cx="%s" cy="%s" r="2.6" fill="%s"/>' % (n(px), n(py), "#FFFDF4" if (i + k) % 5 else "#1E8F5A"))
    o.append('<path d="M34,-326 l6,8 l-6,10 l-6,-10Z" fill="#1E8F5A" stroke="%s" stroke-width="2"/>' % gold)
    # ---- neck + head
    o.append('<path d="M-6,-412 L16,-412 L18,-386 L-8,-386Z" fill="%s"/>' % gsk)
    o.append('<path d="M-8,-392 L20,-392 L22,-384 L-10,-384Z" fill="%s"/>' % goldv)  # bandhgala collar
    o.append('<circle cx="4" cy="-428" r="28" fill="%s"/>' % gsk)
    face = ("M12,-454 C26,-456 34,-450 36,-440 L38,-434 C40,-430 46,-424 48,-419 C46,-415 42,-414 38,-415 "
            "C40,-411 40,-409 38,-407 C40,-405 39,-403 37,-401 C38,-396 35,-390 29,-388 C21,-386 11,-390 5,-397 L3,-432Z")
    o.append('<path d="%s" fill="%s"/>' % (face, d.lg([(0, skin[1]), (1, skin[0])], 0, 0, 1, 0, key="fac%s" % skin[0])))
    o.append('<path d="M30,-433 Q34,-436 38,-433" stroke="#2A1810" stroke-width="2" fill="none"/>')
    o.append('<path d="M28,-440 Q34,-444 40,-440" stroke="#2A1810" stroke-width="2.6" fill="none"/>')
    o.append('<path d="M34,-416 C38,-414 44,-415 46,-417 C44,-411 38,-410 33,-412Z" fill="#2A1810"/>')  # moustache
    o.append('<path d="M36,-406 Q38,-404 36,-402" stroke="#8E3A2A" stroke-width="2" fill="none"/>')
    o.append('<ellipse cx="-2" cy="-424" rx="6" ry="9" fill="%s"/>' % skin[2])
    o.append('<path d="M-12,-436 C-22,-430 -26,-420 -22,-412 C-16,-418 -12,-426 -6,-432Z" fill="#1E1410"/>')  # hair under safa
    o.append('<path d="M6,-436 L10,-436 L9,-420 L5,-420Z" fill="#1E1410"/>')  # sideburn
    o.append('<circle cx="-2" cy="-414" r="3" fill="%s"/>' % gold)  # ear stud
    # ---- safa (turban)
    saf = "M40,-448 C48,-470 40,-498 16,-506 C-10,-512 -34,-500 -38,-472 C-40,-452 -32,-436 -22,-428 L-6,-436 C10,-446 26,-450 40,-448Z"
    o.append('<path d="%s" fill="%s"/>' % (saf, gsf))
    cps = d.clip('<path d="%s"/>' % saf)
    folds = []
    for k in range(7):
        folds.append('<path d="M%s,-440 C%s,%s %s,%s %s,-512" stroke="%s" stroke-width="%s" fill="none" opacity=".75"/>' % (
            n(-40 + k * 14), n(-30 + k * 14), n(-470), n(-20 + k * 12), n(-492), n(-10 + k * 10), safa[2] if k % 2 else safa[0], 6 if k % 2 else 4))
    for k in range(5):
        folds.append('<path d="M-40,%s C-10,%s 20,%s 44,%s" stroke="%s" stroke-width="3" fill="none" opacity=".55"/>' % (
            n(-446 - k * 12), n(-452 - k * 12), n(-458 - k * 11), n(-452 - k * 10), "#FFF3C4" if k % 2 else safa[2]))
    rr = random.Random(5)
    for k in range(40):
        folds.append('<circle cx="%s" cy="%s" r="1.6" fill="#FFF6E0" opacity=".85"/>' % (n(rr.uniform(-38, 44)), n(rr.uniform(-508, -432))))
    o.append('<g clip-path="%s">%s</g>' % (cps, "".join(folds)))
    o.append('<path d="M-28,-432 C-4,-446 22,-452 42,-450" stroke="%s" stroke-width="6" fill="none"/>' % goldv)
    # kalgi: jewelled brooch + plume
    o.append('<path d="M26,-478 C18,-500 20,-532 36,-552 C40,-528 36,-500 32,-478Z" fill="%s"/>' % d.lg([(0, "#FFFFFF"), (1, "#E6DCC8")], key="plume"))
    o.append('<path d="M29,-480 C26,-504 28,-528 36,-548" stroke="#C9BBA0" stroke-width="1.5" fill="none"/>')
    o.append('<circle cx="30" cy="-476" r="10" fill="%s" stroke="#7A4A0E" stroke-width="1.5"/><circle cx="30" cy="-476" r="4.5" fill="#C21F3A"/>' % goldv)
    for k in range(3):
        o.append('<circle cx="%s" cy="%s" r="2.6" fill="#FFFDF4"/>' % (n(24 + k * 6), n(-462 + (k % 2) * 3)))
    o.append(sparkle(34, -480, 7, "#FFFFFF", .95))
    # sehra: strands of pearls + tiny rosebuds over the face
    for k in range(6):
        sx = 16 + k * 7.5
        top = -449 - k * 0.2
        L = 54 + (3 - abs(k - 3)) * 4
        for j in range(int(L / 6)):
            py = top + 4 + j * 6
            px = sx + (py - top) * 0.12
            if j % 4 == 3:
                o.append('<circle cx="%s" cy="%s" r="2.2" fill="#E8456A" opacity=".9"/>' % (n(px), n(py)))
            elif j % 2 == 0:
                o.append('<circle cx="%s" cy="%s" r="1.9" fill="#FFFDF4" stroke="#D9CDB6" stroke-width=".5" opacity=".92"/>' % (n(px), n(py)))
        o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="#F3E6C8" stroke-width=".8" opacity=".8"/>' % (n(sx), n(top), n(sx + L * 0.12), n(top + L)))
        o.append('<circle cx="%s" cy="%s" r="2.6" fill="%s"/>' % (n(sx + L * 0.12), n(top + L + 4), gold))
    # ---- front arm
    if pose == "varmala":
        fn = _arm_fn((12, -382), (56, -300), (100, -350))
        o.append(_limb(fn, 30, 22, gs))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.5" opacity=".6"/>' % (tube_d(fn, 30, 22, 30), sherwani[2]))
        o.append('<path d="M92,-356 L104,-342 L98,-336 L86,-350Z" fill="%s"/>' % goldv)
        o.append('<ellipse cx="106" cy="-360" rx="11" ry="12" fill="%s"/>' % gsk)
    else:
        fn = _arm_fn((12, -382), (26, -310), (34, -238))
        o.append(_limb(fn, 30, 22, gs))
        o.append('<path d="M22,-248 L46,-246 L46,-236 L22,-238Z" fill="%s"/>' % goldv)
        o.append('<ellipse cx="35" cy="-226" rx="10" ry="12" fill="%s"/>' % gsk)
    # ---- rim light
    if rim:
        rs = 'stroke="%s" stroke-width="3" fill="none" stroke-linecap="round" opacity=".95"' % rim
        o.append('<path d="M40,-448 C48,-470 40,-498 16,-506" %s/>' % rs)
        o.append('<path d="M36,-440 L38,-434 C40,-430 46,-424 48,-419 M38,-407 C40,-405 39,-403 37,-401 C38,-396 35,-390 29,-388" %s/>' % rs)
        o.append('<path d="M36,-388 C48,-362 50,-322 46,-292 L58,-172" %s/>' % rs)
        o.append('<path d="M-38,-472 C-40,-452 -32,-436 -22,-428 M-40,-394 C-54,-372 -56,-332 -52,-292 L-62,-172" %s opacity=".6"/>' % rs)
    return _wrap(d, o, x, y, s, flip, shade)


# ================================================================== BRIDE
def bride(d, x, y, s=1, flip=False, pose="stand", lehenga=("#E0304A", "#B3122E", "#6E0A1C"), dupatta=("#F0506E", "#B3123E"),
          skin=SKIN, rim=None, shade=None, body=None, trim=None, veil_op=0.82):
    gold = trim or d.gold()
    goldv = d.lg(GOLD, 0, 0, 0, 1, key="goldv")
    gl = d.lg([(0, lehenga[2]), (0.3, lehenga[1]), (0.65, lehenga[0]), (1, lehenga[1])], 0, 0, 1, 0, key="lhg%s" % lehenga[0])
    gd = d.lg([(0, dupatta[1]), (1, dupatta[0])], 0, 0, 1, 1, key="dup%s" % dupatta[0])
    gsk = d.lg([(0, skin[2]), (0.45, skin[1]), (1, skin[0])], 0, 0, 1, 0, key="gsk%s" % skin[0])
    o = []
    # ---- dupatta drape behind (head -> ground)
    veil = ("M22,-424 C8,-446 -30,-444 -44,-406 C-62,-330 -110,-200 -158,-24 C-162,-10 -170,0 -182,4 "
            "L-104,4 C-96,-80 -78,-200 -52,-306 C-44,-350 -30,-384 -12,-404Z")
    o.append('<path d="%s" fill="%s" opacity="%s"/>' % (veil, gd, veil_op))
    cpv = d.clip('<path d="%s"/>' % veil)
    rr = random.Random(21)
    bt = []
    for k in range(70):
        bt.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".85"/>' % (n(rr.uniform(-180, 10)), n(rr.uniform(-430, 0)), n(rr.uniform(1.4, 2.6)), "#FFE9A8"))
    o.append('<g clip-path="%s">%s</g>' % (cpv, "".join(bt)))
    o.append('<path d="M-44,-406 C-62,-330 -110,-200 -158,-24 C-162,-10 -170,0 -182,4" stroke="%s" stroke-width="7" fill="none"/>' % goldv)
    for i, ((px, py), a) in enumerate(sample(cub((-44, -406), (-62, -330), (-110, -200), (-170, 0)), 14)):
        o.append('<path d="M%s,%s l-5,8 l10,0Z" fill="%s"/>' % (n(px - 4), n(py), gold))
    # ---- back arm for varmala
    # ---- lehenga skirt
    sk = "M-30,-274 L30,-274 C58,-190 102,-80 134,0 L-126,0 C-98,-80 -58,-190 -30,-274Z"
    o.append('<path d="%s" fill="%s"/>' % (sk, gl))
    cp = d.clip('<path d="%s"/>' % sk)
    pl = []
    for k in range(11):
        t = k / 10
        xw, xh = -28 + 56 * t, -124 + 256 * t
        pl.append('<path d="M%s,-274 L%s,0" stroke="%s" stroke-width="%s" opacity="%s"/>' % (n(xw), n(xh), "#000" if k % 2 else "#fff", 10 if k % 2 else 5, ".12" if k % 2 else ".14"))
    rr = random.Random(7)
    for k in range(60):
        px, py = rr.uniform(-110, 120), rr.uniform(-250, -60)
        pl.append('<g transform="translate(%s %s)">%s<circle r="1.4" fill="%s"/></g>' % (n(px), n(py), ring_petals(5, 0.6, 5, 2.2, "#F2C45A", "none", 1, rr.randint(0, 72)), lehenga[2]))
    # heavy border
    pl.append('<path d="M-140,-50 Q0,-36 150,-50 L150,4 L-140,4Z" fill="%s"/>' % goldv)
    pl.append('<path d="M-140,-40 Q0,-26 150,-40 L150,-30 Q0,-16 -140,-30Z" fill="%s"/>' % lehenga[2])
    for k in range(16):
        px = -120 + k * 16
        pl.append('<path d="M%s,-12 C%s,-24 %s,-24 %s,-12Z" fill="%s"/><circle cx="%s" cy="-6" r="2" fill="%s"/>' % (n(px - 7), n(px - 4), n(px + 4), n(px + 7), lehenga[1], n(px), lehenga[2]))
    pl.append('<path d="M-100,-118 Q0,-104 108,-118" stroke="%s" stroke-width="6" fill="none"/>' % goldv)
    pl.append('<path d="M-104,-108 Q0,-94 112,-108" stroke="%s" stroke-width="2" fill="none"/>' % gold)
    o.append('<g clip-path="%s">%s</g>' % (cp, "".join(pl)))
    # ---- choli / torso
    tor = "M-26,-354 C-14,-364 18,-364 28,-352 C34,-328 30,-298 26,-274 L-28,-274 C-32,-302 -32,-332 -26,-354Z"
    o.append('<path d="%s" fill="%s"/>' % (tor, gl))
    o.append('<path d="M-28,-282 L27,-282 L26,-272 L-29,-272Z" fill="%s"/>' % goldv)
    # front dupatta fold across shoulder to waist
    o.append('<path d="M-18,-360 C0,-340 16,-312 30,-278 L18,-274 C6,-306 -8,-332 -26,-352Z" fill="%s" opacity=".9"/>' % gd)
    o.append('<path d="M-18,-360 C0,-340 16,-312 30,-278" stroke="%s" stroke-width="3" fill="none"/>' % gold)
    # ---- neck, head
    o.append('<path d="M-8,-376 L10,-376 L12,-350 L-10,-350Z" fill="%s"/>' % gsk)
    o.append('<circle cx="-4" cy="-396" r="24" fill="#1E1410"/>')
    face = ("M8,-420 C20,-420 26,-414 27,-404 L28,-400 C30,-396 34,-392 35,-389 C33,-386 30,-386 27,-387 "
            "C29,-384 28,-382 27,-380 C29,-378 28,-376 26,-375 C26,-370 22,-366 16,-365 C8,-364 0,-368 -4,-374 L-6,-404Z")
    o.append('<path d="%s" fill="%s"/>' % (face, d.lg([(0, skin[1]), (1, skin[0])], 0, 0, 1, 0, key="fac%s" % skin[0])))
    o.append('<path d="M-6,-410 C0,-422 12,-424 22,-418 C12,-416 2,-412 -4,-404Z" fill="#1E1410"/>')  # hair parting
    o.append('<path d="M17,-399 Q22,-403 27,-399 Q22,-397 17,-399Z" fill="#1E1410"/>')  # kajal eye
    o.append('<path d="M16,-406 Q22,-410 28,-406" stroke="#1E1410" stroke-width="1.6" fill="none"/>')
    o.append('<path d="M26,-383 Q29,-381 27,-379 Q29,-377 26,-376" stroke="#B3122E" stroke-width="2.6" fill="none"/>')
    o.append('<circle cx="24" cy="-412" r="2.4" fill="#C21F3A"/>')  # bindi
    # ---- dupatta over the head (front edge)
    hd = "M24,-422 C12,-450 -28,-448 -44,-406 L-34,-398 C-24,-428 2,-434 14,-416Z"
    o.append('<path d="%s" fill="%s"/>' % (hd, gd))
    o.append('<path d="M24,-422 C12,-450 -28,-448 -44,-406" stroke="%s" stroke-width="5" fill="none"/>' % goldv)
    for i, ((px, py), a) in enumerate(sample(cub((24, -422), (12, -450), (-28, -448), (-44, -406)), 9)):
        o.append('<circle cx="%s" cy="%s" r="2" fill="#FFF3C4"/>' % (n(px), n(py)))
    # ---- jewellery
    o.append('<path d="M8,-432 L18,-418" stroke="%s" stroke-width="1.6"/>' % gold)
    o.append('<path d="M18,-420 l5,5 l-5,8 l-5,-8Z" fill="%s" stroke="#7A4A0E" stroke-width=".8"/><circle cx="18" cy="-406" r="2.2" fill="#FFFDF4"/>' % goldv)  # maang tikka
    o.append('<circle cx="30" cy="-387" r="4.6" fill="none" stroke="%s" stroke-width="1.6"/>' % gold)  # nath
    o.append('<circle cx="34" cy="-385" r="1.5" fill="#FFFDF4"/>')
    o.append('<path d="M33,-384 C24,-380 8,-384 -2,-392" stroke="%s" stroke-width=".9" fill="none"/>' % gold)
    o.append('<path d="M-6,-392 L-6,-386 C-14,-384 -14,-372 -6,-370 C2,-372 2,-384 -6,-386Z" fill="%s"/>' % goldv)  # jhumka
    o.append(dots_ring(6, 5, 1.4, "#FFFDF4", -6, -368))
    for k, (dy, sw) in enumerate(((0, 6), (12, 5), (24, 7))):  # rani haar
        o.append('<path d="M-8,-360 C-4,%s 14,%s 28,%s" stroke="%s" stroke-width="%s" fill="none"/>' % (n(-340 + dy), n(-324 + dy), n(-338 + dy * 0.7), goldv, sw))
    o.append(dots_ring(1, 0, 4, "#1E8F5A", 26, -322))
    o.append('<circle cx="24" cy="-330" r="3" fill="#C21F3A"/>')
    o.append(sparkle(21, -414, 6, "#FFFFFF", .95) + sparkle(31, -380, 5, "#FFFFFF", .9) + sparkle(20, -334, 7, "#FFFFFF", .9))
    # ---- front arm with chooda + kaleeras
    if pose == "varmala":
        sh_, el, hd_ = (8, -350), (54, -290), (94, -334)
    else:
        sh_, el, hd_ = (8, -350), (22, -298), (30, -236)
    o.append(_limb(cub(sh_, (sh_[0] + 6, sh_[1] + 20), (el[0] - 6, el[1] - 16), el), 26, 20, gl))  # sleeve
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="4"/>' % (_poly([(el[0] - 12, el[1] - 6), (el[0] + 10, el[1] + 4)]), goldv))
    fore = cub(el, (el[0] + (hd_[0] - el[0]) * 0.3, el[1] + (hd_[1] - el[1]) * 0.3), (el[0] + (hd_[0] - el[0]) * 0.7, el[1] + (hd_[1] - el[1]) * 0.7), hd_)
    o.append(_limb(fore, 18, 14, gsk))
    ang = math.degrees(math.atan2(hd_[1] - el[1], hd_[0] - el[0]))
    for k in range(9):  # chooda stack
        px, py = fore(0.35 + k * 0.055)
        o.append('<rect x="%s" y="%s" width="5" height="24" rx="2" fill="%s" transform="rotate(%s %s %s)"/>' % (
            n(px - 2.5), n(py - 12), "#FFFDF4" if k in (2, 6) else ("#E9C46A" if k in (0, 8) else "#C21F3A"), n(ang), n(px), n(py)))
    px, py = fore(0.86)
    for k in range(3):  # kaleeras
        o.append('<path d="M%s,%s q%s,10 %s,18" stroke="%s" stroke-width="2.2" fill="none"/><circle cx="%s" cy="%s" r="2.4" fill="%s"/>' % (
            n(px - 4 + k * 4), n(py + 6), n(-3 + k * 2), n(-2 + k * 2), gold, n(px - 6 + k * 6), n(py + 24), gold))
    o.append('<ellipse cx="%s" cy="%s" rx="10" ry="11" fill="%s"/>' % (n(hd_[0] + 4), n(hd_[1] - 2), gsk))
    o.append('<circle cx="%s" cy="%s" r="3" fill="none" stroke="%s" stroke-width="1.5"/>' % (n(hd_[0] + 8), n(hd_[1] - 6), gold))
    # ---- rim light
    if rim:
        rs = 'stroke="%s" stroke-width="3" fill="none" stroke-linecap="round" opacity=".95"' % rim
        o.append('<path d="M24,-422 C12,-450 -28,-448 -44,-406" %s/>' % rs)
        o.append('<path d="M27,-404 L28,-400 C30,-396 34,-392 35,-389 M28,-352 C34,-328 30,-298 26,-274 M30,-274 C58,-190 102,-80 134,0" %s/>' % rs)
        o.append('<path d="M-44,-406 C-62,-330 -110,-200 -158,-24" %s opacity=".6"/>' % rs)
    return _wrap(d, o, x, y, s, flip, shade)


# ================================================================== couple seen from behind, walking away
def couple_back(d, cx, by, s=1, body=None, trim=None, cloth=("#C8102E",), sherwani=("#FFF8E8", "#EBD8B0", "#B8966A"),
                safa=("#F9A825", "#E0591B", "#B3261E"), lehenga=("#E0304A", "#B3122E", "#6E0A1C")):
    gold = trim or d.gold()
    goldv = d.lg(GOLD, 0, 0, 0, 1, key="goldv")
    gs = d.lg([(0, sherwani[2]), (0.35, sherwani[1]), (0.6, sherwani[0]), (1, sherwani[2])], 0, 0, 1, 0, key="shwb%s" % sherwani[0])
    gl = d.lg([(0, lehenga[2]), (0.35, lehenga[1]), (0.6, lehenga[0]), (1, lehenga[2])], 0, 0, 1, 0, key="lhgb%s" % lehenga[0])
    gsf = d.rg([(0, safa[0]), (0.6, safa[1]), (1, safa[2])], 0.4, 0.3, 0.9, key="safab%s" % safa[0])
    gd = d.lg([(0, "#F0506E"), (1, cloth[0])], 0, 0, 0, 1, key="dupb%s" % cloth[0])
    o = []
    gx = -74
    # groom legs + juttis
    for dx, lift in ((-20, 0), (18, 10)):
        o.append('<path d="M%s,-176 L%s,-176 L%s,%s L%s,%sZ" fill="%s"/>' % (n(gx + dx - 16), n(gx + dx + 16), n(gx + dx + 10), n(-14 - lift), n(gx + dx - 10), n(-14 - lift), d.lg([(0, "#D9CDB6"), (0.5, "#FFFBF2"), (1, "#D9CDB6")], 0, 0, 1, 0, key="churb")))
        o.append('<ellipse cx="%s" cy="%s" rx="14" ry="8" fill="#8E0A1E"/>' % (n(gx + dx), n(-8 - lift)))
    # sherwani (back view)
    shp = "M%s,-392 C%s,-404 %s,-404 %s,-392 C%s,-360 %s,-300 %s,-170 L%s,-170 C%s,-300 %s,-360 %s,-392Z" % tuple(
        n(v) for v in (gx - 50, gx - 20, gx + 20, gx + 50, gx + 58, gx + 60, gx + 68, gx - 68, gx - 60, gx - 58, gx - 50))
    o.append('<path d="%s" fill="%s"/>' % (shp, gs))
    cp = d.clip('<path d="%s"/>' % shp)
    rr = random.Random(4)
    emb = ['<rect x="%s" y="-212" width="150" height="42" fill="%s"/>' % (n(gx - 75), goldv)]
    for k in range(40):
        emb.append('<g transform="translate(%s %s)">%s</g>' % (n(gx + rr.uniform(-60, 60)), n(rr.uniform(-380, -220)), ring_petals(4, 0.5, 4.5, 2, sherwani[2], "none", 1, rr.randint(0, 90))))
    emb.append('<path d="M%s,-392 L%s,-212" stroke="#000" stroke-opacity=".08" stroke-width="6"/>' % (n(gx), n(gx)))
    o.append('<g clip-path="%s">%s</g>' % (cp, "".join(emb)))
    # arms
    o.append(_limb(cub((gx - 48, -384), (gx - 58, -330), (gx - 62, -280), (gx - 60, -236)), 26, 20, gs))
    o.append(_limb(cub((gx + 48, -384), (gx + 64, -330), (gx + 80, -290), (gx + 104, -262)), 26, 20, gs))
    # stole across the back
    o.append(_limb(cub((gx - 46, -390), (gx - 10, -350), (gx + 20, -300), (gx + 52, -250)), 24, 22, d.lg([(0, "#9E1030"), (1, "#5A0618")], key="stlb")))
    # neck + head + safa (back)
    o.append('<rect x="%s" y="-414" width="22" height="24" fill="%s"/>' % (n(gx - 11), SKIN[1]))
    o.append('<circle cx="%s" cy="-424" r="28" fill="#1E1410"/>' % n(gx))
    saf = "M%s,-420 C%s,-470 %s,-500 %s,-500 C%s,-500 %s,-470 %s,-420 C%s,-432 %s,-432 %s,-420Z" % tuple(n(v) for v in (
        gx - 36, gx - 40, gx - 16, gx, gx + 16, gx + 40, gx + 36, gx + 20, gx - 20, gx - 36))
    o.append('<path d="%s" fill="%s"/>' % (saf, gsf))
    cps = d.clip('<path d="%s"/>' % saf)
    f = []
    for k in range(6):
        f.append('<path d="M%s,-424 C%s,-450 %s,-480 %s,-500" stroke="%s" stroke-width="5" fill="none" opacity=".7"/>' % (
            n(gx - 36 + k * 14), n(gx - 30 + k * 12), n(gx - 16 + k * 6), n(gx - 6 + k * 3), safa[2] if k % 2 else safa[0]))
    o.append('<g clip-path="%s">%s</g>' % (cps, "".join(f)))
    o.append('<path d="M%s,-428 C%s,-440 %s,-440 %s,-428" stroke="%s" stroke-width="5" fill="none"/>' % (n(gx - 36), n(gx - 12), n(gx + 12), n(gx + 36), goldv))
    o.append(_limb(cub((gx + 6, -440), (gx + 16, -400), (gx + 10, -360), (gx + 18, -300)), 22, 16, gsf))  # turra
    o.append('<path d="M%s,-304 L%s,-300 L%s,-286 L%s,-290Z" fill="%s"/>' % (n(gx + 8), n(gx + 28), n(gx + 28), n(gx + 8), goldv))
    # ---- bride (back view)
    bx = 84
    sk = "M%s,-274 L%s,-274 C%s,-190 %s,-80 %s,0 L%s,0 C%s,-80 %s,-190 %s,-274Z" % tuple(n(v) for v in (
        bx - 30, bx + 30, bx + 58, bx + 102, bx + 132, bx - 132, bx - 102, bx - 58, bx - 30))
    o.append('<path d="%s" fill="%s"/>' % (sk, gl))
    cpk = d.clip('<path d="%s"/>' % sk)
    pl = []
    for k in range(11):
        t = k / 10
        pl.append('<path d="M%s,-274 L%s,0" stroke="%s" stroke-width="%s" opacity=".12"/>' % (n(bx - 28 + 56 * t), n(bx - 130 + 260 * t), "#000" if k % 2 else "#fff", 10 if k % 2 else 5))
    pl.append('<path d="M%s,-48 Q%s,-34 %s,-48 L%s,4 L%s,4Z" fill="%s"/>' % (n(bx - 140), n(bx), n(bx + 140), n(bx + 140), n(bx - 140), goldv))
    pl.append('<path d="M%s,-38 Q%s,-24 %s,-38 L%s,-28 Q%s,-14 %s,-28Z" fill="%s"/>' % (n(bx - 140), n(bx), n(bx + 140), n(bx + 140), n(bx), n(bx - 140), lehenga[2]))
    o.append('<g clip-path="%s">%s</g>' % (cpk, "".join(pl)))
    o.append('<path d="M%s,-354 C%s,-364 %s,-364 %s,-354 L%s,-274 L%s,-274Z" fill="%s"/>' % (n(bx - 26), n(bx - 12), n(bx + 12), n(bx + 26), n(bx + 28), n(bx - 28), gl))
    o.append('<circle cx="%s" cy="-392" r="25" fill="#1E1410"/>' % n(bx))
    # veil: over the head down the back to a train
    veil = "M%s,-420 C%s,-430 %s,-430 %s,-408 C%s,-330 %s,-200 %s,-10 L%s,-10 C%s,-200 %s,-330 %s,-408Z" % tuple(n(v) for v in (
        bx - 30, bx - 12, bx + 12, bx + 30, bx + 52, bx + 80, bx + 96, bx - 96, bx - 80, bx - 52, bx - 30))
    o.append('<path d="%s" fill="%s" opacity=".85"/>' % (veil, gd))
    cpv = d.clip('<path d="%s"/>' % veil)
    rr = random.Random(9)
    o.append('<g clip-path="%s">%s</g>' % (cpv, "".join('<circle cx="%s" cy="%s" r="%s" fill="#FFE9A8" opacity=".85"/>' % (
        n(bx + rr.uniform(-90, 90)), n(rr.uniform(-420, -20)), n(rr.uniform(1.4, 2.6))) for _ in range(70))))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="6"/>' % (veil, goldv))
    # holding hands + gathbandhan
    o.append(_limb(cub((bx - 24, -350), (bx - 40, -310), (bx - 50, -290), (gx + 112, -262)), 18, 14, gl))
    o.append('<circle cx="%s" cy="-262" r="10" fill="%s"/>' % (n(gx + 110), SKIN[1]))
    o.append('<path d="M%s,-360 C%s,-250 %s,-240 %s,-250" stroke="#FFF3DC" stroke-width="12" fill="none"/>' % (n(gx + 40), n(gx + 50), n(bx - 44), n(bx - 30)))
    o.append('<path d="M%s,-360 C%s,-250 %s,-240 %s,-250" stroke="%s" stroke-width="3" fill="none"/>' % (n(gx + 40), n(gx + 50), n(bx - 44), n(bx - 30), gold))
    return g("".join(o), cx, by, s)
