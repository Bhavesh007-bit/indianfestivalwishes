"""Navratri garba / dandiya dancers v2 (agent A).

Properly proportioned figures (~8 heads tall) with filled, tapered limbs, hands,
multi-tier ghera chaniya with mirror-work, flowing odhni, kediyu + pagdi for men.
Both functions draw with feet at (x, y); female ~440*s tall, male ~460*s tall.
Pass sil="<colour or url(#grad)>" for a flat silhouette version (crowds / friezes).
"""
import math
from lib_a import f, pts
from navratri_motifs_a import dandiya, mirror

SKIN = ("#E8AE84", "#B97650")
HAIR = "#1A0F0D"


# ------------------------------------------------------------------ geometry helpers
def _limb_path(points, widths):
    """Closed outline of a tapered limb through points (round caps)."""
    n = len(points)
    L, R = [], []
    for i in range(n):
        if i == 0:
            dx, dy = points[1][0] - points[0][0], points[1][1] - points[0][1]
        elif i == n - 1:
            dx, dy = points[-1][0] - points[-2][0], points[-1][1] - points[-2][1]
        else:
            dx, dy = points[i + 1][0] - points[i - 1][0], points[i + 1][1] - points[i - 1][1]
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        w = widths[i] / 2
        L.append((points[i][0] + nx * w, points[i][1] + ny * w))
        R.append((points[i][0] - nx * w, points[i][1] - ny * w))
    we, ws = widths[-1] / 2, widths[0] / 2
    d = "M%s,%s " % (f(L[0][0]), f(L[0][1]))
    d += " ".join("L%s,%s" % (f(x), f(y)) for x, y in L[1:])
    d += " A%s,%s 0 0 0 %s,%s " % (f(we), f(we), f(R[-1][0]), f(R[-1][1]))
    d += " ".join("L%s,%s" % (f(x), f(y)) for x, y in reversed(R[:-1]))
    d += " A%s,%s 0 0 0 %s,%s Z" % (f(ws), f(ws), f(L[0][0]), f(L[0][1]))
    return d


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 1
    return dx / d, dy / d


def _hand(c, wrist, direction, r, skin, fist=False, sil=None):
    """Hand at the end of a forearm: palm + fingers (open) or a fist."""
    ux, uy = direction
    ang = math.degrees(math.atan2(uy, ux))
    cx, cy = wrist[0] + ux * r * 0.9, wrist[1] + uy * r * 0.9
    out = ['<g transform="translate(%s,%s) rotate(%s)">' % (f(cx), f(cy), f(ang))]
    fill = sil or skin
    if fist:
        out.append('<ellipse cx="0" cy="0" rx="%s" ry="%s" fill="%s"/>' % (f(r * 1.0), f(r * 0.85), fill))
        if not sil:
            for k in range(4):
                out.append('<path d="M%s,%s q%s,0 %s,%s" stroke="#9A5A38" stroke-width="%s" fill="none" opacity="0.55"/>' % (
                    f(r * 0.3), f(-r * 0.6 + k * r * 0.4), f(r * 0.45), f(r * 0.5), f(r * 0.15), f(max(0.8, r * 0.08))))
    else:
        out.append('<ellipse cx="0" cy="0" rx="%s" ry="%s" fill="%s"/>' % (f(r * 0.95), f(r * 0.72), fill))
        for k, (dy, L) in enumerate(((-0.45, 1.25), (-0.15, 1.45), (0.15, 1.4), (0.42, 1.15))):
            out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>' % (
                f(r * 0.4), f(r * dy - r * 0.14), f(r * L), f(r * 0.28), f(r * 0.14), fill))
        out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" transform="rotate(-40)"/>' % (
            f(-r * 0.1), f(-r * 1.15), f(r * 0.9), f(r * 0.3), f(r * 0.15), fill))
        if not sil:
            out.append('<circle cx="%s" cy="0" r="%s" fill="#C0392B" opacity="0.55"/>' % (f(-r * 0.05), f(r * 0.28)))  # mehendi dot
    out.append("</g>")
    return "".join(out)


def _arm(c, sh, el, wr, skin, sleeve=None, sleeve_trim=None, bangles=(), w=17, fist=False, sil=None, shade=True):
    """Full filled arm: upper arm, forearm, hand; optional puff sleeve and bangle stack."""
    out = []
    fill = sil or skin
    pts_ = [sh, _lerp(sh, el, 0.5), el, _lerp(el, wr, 0.5), wr]
    wds = [w * 1.05, w * 0.95, w * 0.82, w * 0.74, w * 0.62]
    d = _limb_path(pts_, wds)
    out.append('<path d="%s" fill="%s"/>' % (d, fill))
    if not sil and shade:
        # soft shading edge + highlight along the limb
        out.append('<path d="%s" fill="none" stroke="#7A3E22" stroke-opacity="0.22" stroke-width="%s"/>' % (d, f(w * 0.12)))
        hl = [(_lerp(sh, el, t)) for t in (0.15, 0.85)] + [_lerp(el, wr, 0.2), _lerp(el, wr, 0.75)]
        ux, uy = _unit(sh, el)
        out.append('<polyline points="%s" fill="none" stroke="#FFE3CC" stroke-opacity="0.45" stroke-width="%s" stroke-linecap="round" transform="translate(%s,%s)"/>' % (
            pts(hl), f(w * 0.16), f(-uy * w * 0.18), f(ux * w * 0.18)))
    if sleeve:
        e2 = _lerp(sh, el, 0.5)
        out.append('<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (f(sh[0]), f(sh[1]), f(e2[0]), f(e2[1]), sil or sleeve, f(w * 1.35)))
        if not sil and sleeve_trim:
            a, b = _lerp(sh, el, 0.5), _unit(sh, el)
            nx, ny = -b[1], b[0]
            out.append('<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
                f(a[0] + nx * w * 0.66), f(a[1] + ny * w * 0.66), f(a[0] - nx * w * 0.66), f(a[1] - ny * w * 0.66), sleeve_trim, f(w * 0.3)))
            m = _lerp(sh, el, 0.3)
            out.append('<circle cx="%s" cy="%s" r="%s" fill="#EAF2FF" stroke="%s" stroke-width="1.2"/>' % (f(m[0]), f(m[1]), f(w * 0.18), sleeve_trim))
    ux, uy = _unit(el, wr)
    if bangles and not sil:
        nx, ny = -uy, ux
        for k, col in enumerate(bangles):
            t = 0.52 + k * 0.085
            bx, by = _lerp(el, wr, t)
            ww = w * (0.46 - t * 0.06)
            out.append('<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
                f(bx + nx * ww), f(by + ny * ww), f(bx - nx * ww), f(by - ny * ww), col, f(w * 0.2)))
            out.append('<path d="M%s,%s L%s,%s" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="%s" stroke-linecap="round"/>' % (
                f(bx + nx * ww * 0.7 - ux), f(by + ny * ww * 0.7 - uy), f(bx + nx * ww * 0.1 - ux), f(by + ny * ww * 0.1 - uy), f(w * 0.07)))
    out.append(_hand(c, wr, (ux, uy), w * 0.55, skin, fist, sil))
    return "".join(out)


def _stick(c, hand, ang, L=150, w=11, cols=("#E53935", "#FFD740"), sil=None):
    a = math.radians(ang)
    x1, y1 = hand[0] - L * 0.3 * math.cos(a), hand[1] - L * 0.3 * math.sin(a)
    x2, y2 = hand[0] + L * 0.7 * math.cos(a), hand[1] + L * 0.7 * math.sin(a)
    if sil:
        return '<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (f(x1), f(y1), f(x2), f(y2), sil, f(w))
    return dandiya(c, x1, y1, x2, y2, w, cols)


# ------------------------------------------------------------------ female
FPOSE = {
    # (front arm elbow, wrist), (back arm elbow, wrist), fist?, skirt swirl (-1 left / 1 right)
    "a": (((58, -420), (38, -474)), ((-64, -346), (-112, -372)), False, 1),
    "b": (((56, -422), (18, -470)), ((-48, -424), (4, -474)), False, -1),
    "c": (((72, -362), (126, -386)), ((-66, -358), (-120, -380)), False, 1),
    "d": (((66, -328), (110, -350)), ((-48, -424), (-28, -476)), False, -1),
    "s": (((66, -398), (78, -452)), ((-60, -392), (-58, -448)), True, 1),  # holding dandiyas up
}


def dancer_f(c, x, y, s=1.0, flip=False, pose="a", col=None, skin=SKIN, sil=None, sticks=None):
    col = col or {}
    skirt = col.get("skirt", ["#C2185B", "#FF8F00", "#1E88E5", "#43A047", "#8E24AA", "#F4511E"])
    choli = col.get("choli", "#1B5E20")
    dup = col.get("dup", "#E53935")
    border = col.get("border", "#FFC53D")
    S = sil
    sk = S or c.lg([(0, skin[0]), (1, skin[1])], 0, 0, 1, 1)
    skf = S or skin[0]
    hair = S or HAIR
    (fe, fw), (be, bw), fist, swirl = FPOSE.get(pose, FPOSE["a"])
    if sticks:
        fist = True
    out = ['<g transform="translate(%s,%s) scale(%s,%s)">' % (f(x), f(y), f(-s if flip else s), f(s))]
    shF, shB = (24, -364), (-22, -364)

    # ---------- odhni flowing behind (drawn first)
    od = ("M-16,-366 C-70,-372 -130,-352 -168,-304 C-196,-268 -206,-226 -236,-196 "
          "C-214,-190 -190,-196 -172,-214 C-150,-238 -132,-268 -100,-292 C-72,-312 -40,-318 -8,-322 Z")
    out.append('<path d="%s" fill="%s"/>' % (od, S or c.lg([(0, dup), (1, "#7A0E18")], 0, 0, 1, 1)))
    if not S:
        dots = c.pattern(14, 14, '<circle cx="3.5" cy="3.5" r="1.6" fill="#FFF3D0"/><circle cx="10.5" cy="10.5" r="1.6" fill="#FFF3D0"/><circle cx="10.5" cy="3.5" r="0.9" fill="#FFF3D0"/>')
        out.append('<path d="%s" fill="%s" opacity="0.8"/>' % (od, dots))
        out.append('<path d="M-236,-196 C-214,-190 -190,-196 -172,-214 C-150,-238 -132,-268 -100,-292" stroke="%s" stroke-width="7" fill="none"/>' % border)
        out.append('<path d="M-16,-366 C-70,-372 -130,-352 -168,-304 C-196,-268 -206,-226 -236,-196" stroke="%s" stroke-width="4" fill="none" stroke-dasharray="6 4"/>' % border)
        for k in range(5):
            tx, ty = -236 + k * 12, -196 + k * -4.5
            out.append('<path d="M%s,%s v14" stroke="%s" stroke-width="2"/><circle cx="%s" cy="%s" r="4" fill="%s"/>' % (f(tx), f(ty), border, f(tx), f(ty + 18), ["#E53935", border, "#1E9E6A"][k % 3]))
    # ---------- back arm
    out.append(_arm(c, shB, be, bw, sk, choli, border, () if S else (border, "#C62828", border, "#1E9E6A"), 20, fist, S))
    if sticks:
        ux, uy = _unit(be, bw)
        out.append(_stick(c, (bw[0] + ux * 9, bw[1] + uy * 9), -118, 150, 11, sticks, S))

    # ---------- chaniya (ghera) geometry
    WY, HY = -292, -18        # waist y, hem centre y
    RX0, RX1, RY = 24, 190, 34
    tilt = 0.09 * swirl

    def ring(t, th):
        rx = RX0 + (RX1 - RX0) * (t ** 1.25)
        cy = WY + (HY - WY) * t
        ry = RY * t
        xx = rx * math.cos(th)
        wave = 0
        if t > 0.5:
            wave = 9 * ((t - 0.5) / 0.5) ** 2 * math.sin(th * 9 + 0.6)
        return xx, cy + ry * math.sin(th) + tilt * xx * t + wave

    N = 72
    left = [ring(i / 20, math.pi) for i in range(21)]
    hem = [ring(1, math.pi - math.pi * i / N) for i in range(N + 1)]
    right = [ring(1 - i / 20, 0) for i in range(21)]
    sk_d = "M" + " L".join("%s,%s" % (f(a), f(b)) for a, b in left + hem + right) + " Z"
    # feet under the hem (behind skirt)
    for (fx, fy, rot) in ((-34, -4, -8), (30, 2, 10)):
        out.append('<g transform="translate(%s,%s) rotate(%s)"><path d="M-18,0 C-18,-12 14,-12 20,-2 C12,6 -12,6 -18,0 Z" fill="%s"/>' % (f(fx), f(fy), f(rot), skf))
        if not S:
            out.append('<path d="M-17,1 C-8,5 10,5 19,-1" stroke="#C62828" stroke-width="3" fill="none"/><path d="M-12,-8 Q0,-3 12,-7" stroke="#E0E0E0" stroke-width="2.4" stroke-dasharray="2 2" fill="none"/>')
        out.append('</g>')
    if S:
        out.append('<path d="%s" fill="%s"/>' % (sk_d, S))
    else:
        # inner lining glimpse where the ghera lifts
        lin = [ring(1, math.pi + math.pi * i / 30) for i in range(31)]
        out.append('<path d="M%s Z" fill="%s"/>' % (pts(lin), c.lg(["#5A0B2E", "#2A0616"], 0, 0, 0, 1)))
        cp = c.clip('<path d="%s"/>' % sk_d)
        g = ['<g clip-path="%s">' % cp]
        # three tiers, each with its own gore colours
        tiers = [(0.0, 0.34, skirt[0:2] or skirt), (0.34, 0.68, skirt[2:4] or skirt), (0.68, 1.02, skirt[4:6] or skirt)]
        M = 18
        for ti, (t0, t1, cols) in enumerate(tiers):
            m = 6 + ti * 6
            for j in range(m):
                th0, th1 = math.pi * j / m, math.pi * (j + 1) / m
                p = [ring(t0, th0), ring(t0, th1), ring(t1, th1), ring(t1, th0)]
                # include some arc samples along the bottom for curvature
                bot = [ring(t1, th1 - (th1 - th0) * k / 4) for k in range(5)]
                poly = [ring(t0, th0), ring(t0, th1)] + bot
                g.append('<path d="M%s Z" fill="%s"/>' % (pts(poly), cols[j % len(cols)]))
                # bandhani dots on alternate gores of the middle tier
                if ti == 1 and j % 2 == 0:
                    mx, my = ring((t0 + t1) / 2, (th0 + th1) / 2)
                    for k in range(3):
                        g.append('<circle cx="%s" cy="%s" r="2.2" fill="#FFF3D0" opacity="0.8"/>' % (f(mx + (k - 1) * 6), f(my + (k % 2) * 6 - 3)))
        # fold shading: dark crease lines from waist to hem
        for j in range(1, M):
            th = math.pi * j / M
            p = [ring(t / 10, th) for t in range(11)]
            g.append('<polyline points="%s" fill="none" stroke="#000" stroke-opacity="0.14" stroke-width="%s"/>' % (pts(p), f(3 + 2 * (j % 2))))
        # volume: horizontal light/shade
        g.append('<rect x="-240" y="-300" width="480" height="340" fill="%s"/>' % c.lg([(0, "#000", 0.32), (0.3, "#000", 0), (0.45, "#fff", 0.18), (0.6, "#fff", 0), (1, "#000", 0.35)], 0, 0, 1, 0))
        # tier seams: gold gota with mirror-work
        for tt in (0.34, 0.68):
            p = [ring(tt, math.pi * i / 40) for i in range(41)]
            g.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (pts(p), border, f(7 + tt * 6)))
            g.append('<polyline points="%s" fill="none" stroke="#8B0000" stroke-width="1.6" stroke-dasharray="3 3"/>' % pts(p))
            for i in range(1, 40, 3):
                mx, my = ring(tt, math.pi * i / 40)
                g.append('<circle cx="%s" cy="%s" r="%s" fill="#EEF4FF" stroke="#8B5A00" stroke-width="1"/>' % (f(mx), f(my), f(2.5 + tt * 2.2)))
        # wide hem border
        hb = [ring(0.92, math.pi * i / 60) for i in range(61)] + [ring(1.0, math.pi - math.pi * i / 60) for i in range(61)]
        g.append('<path d="M%s Z" fill="%s"/>' % (pts(hb), c.lg(["#7A0010", "#B71C1C"], 0, 0, 0, 1)))
        p = [ring(0.925, math.pi * i / 60) for i in range(61)]
        g.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="6"/>' % (pts(p), border))
        for i in range(2, 60, 3):
            mx, my = ring(0.965, math.pi * i / 60)
            g.append(mirror(c, mx, my, 5.5, "#FFC53D", "#FFE9B0", ring=False))
        g.append('</g>')
        out.extend(g)
        # scalloped lace + latkan beads below the hem
        for i in range(0, N, 2):
            hx, hy = hem[i]
            out.append('<circle cx="%s" cy="%s" r="5" fill="%s"/>' % (f(hx), f(hy + 3), border))
        out.append('<polyline points="%s" fill="none" stroke="#7A4E08" stroke-width="1.5" opacity="0.6"/>' % pts(hem))

    # ---------- torso: midriff, choli, kamarbandh
    out.append('<path d="M-19,-316 C-21,-304 -22,-298 -24,-290 L24,-290 C22,-298 21,-306 21,-316 Z" fill="%s"/>' % sk)
    out.append('<path d="M-24,-364 C-4,-374 10,-374 28,-364 C30,-346 26,-330 22,-316 C8,-310 -8,-310 -20,-316 C-26,-332 -28,-348 -24,-364 Z" fill="%s"/>' % (S or choli))
    if not S:
        out.append('<path d="M-24,-364 C-4,-374 10,-374 28,-364 C30,-346 26,-330 22,-316 C8,-310 -8,-310 -20,-316 C-26,-332 -28,-348 -24,-364 Z" fill="%s"/>' % c.lg([(0, "#fff", 0.18), (0.5, "#fff", 0), (1, "#000", 0.28)], 0, 0, 1, 0))
        out.append('<path d="M-20,-316 C-8,-310 8,-310 22,-316" stroke="%s" stroke-width="5" fill="none"/>' % border)
        out.append('<path d="M-8,-366 C-2,-350 8,-350 14,-367" stroke="%s" stroke-width="3" fill="none"/>' % border)
        for (mx, my) in ((-12, -340), (0, -334), (12, -338), (-6, -324), (8, -324), (18, -350), (-16, -352)):
            out.append('<circle cx="%s" cy="%s" r="3" fill="#EEF4FF" stroke="%s" stroke-width="1.3"/>' % (mx, my, border))
        out.append('<path d="M-24,-292 L24,-292" stroke="%s" stroke-width="7" stroke-linecap="round"/>' % border)
        for k in range(-3, 4):
            out.append('<path d="M%s,-290 v%s" stroke="%s" stroke-width="1.6"/><circle cx="%s" cy="%s" r="2" fill="%s"/>' % (f(k * 6), f(8 + abs(k) * 1.5), border, f(k * 6), f(-282 + abs(k) * 1.5), border))
        # navel shading
        out.append('<path d="M1,-303 q2,3 0,5" stroke="#8A4A2A" stroke-width="1.2" fill="none" opacity="0.6"/>')
    # ---------- neck + head
    out.append('<path d="M-6,-384 L10,-384 L11,-364 L-5,-364 Z" fill="%s"/>' % sk)
    if not S:
        out.append('<path d="M-12,-366 C-6,-350 16,-350 20,-366" stroke="%s" stroke-width="3.5" fill="none"/><circle cx="4" cy="-352" r="4" fill="#C62828" stroke="%s" stroke-width="1.5"/>' % (border, border))
    # hair back + bun with gajra
    out.append('<ellipse cx="-4" cy="-404" rx="24" ry="27" fill="%s"/>' % hair)
    out.append('<circle cx="-24" cy="-398" r="13" fill="%s"/>' % hair)
    if not S:
        for a in range(0, 360, 36):
            out.append('<circle cx="%s" cy="%s" r="3.2" fill="#FFFBEF"/>' % (f(-24 + 14 * math.cos(math.radians(a))), f(-398 + 14 * math.sin(math.radians(a)))))
    # face (3/4 to the right)
    face = "M-8,-424 C8,-432 26,-424 28,-406 C30,-398 34,-394 30,-390 C30,-386 28,-384 28,-380 C24,-372 14,-370 6,-372 C-6,-376 -12,-390 -12,-404 C-12,-414 -10,-420 -8,-424 Z"
    out.append('<path d="%s" fill="%s"/>' % (face, sk))
    if not S:
        out.append('<path d="%s" fill="%s"/>' % (face, c.rg([(0, "#fff", 0.25), (0.6, "#fff", 0), (1, "#7A3E22", 0.2)], 0.65, 0.35, 0.7)))
        out.append('<path d="M-12,-404 C-12,-422 2,-434 22,-428 C18,-420 10,-416 0,-414 C-4,-410 -8,-406 -12,-396 Z" fill="%s"/>' % HAIR)  # fringe
        out.append('<path d="M14,-404 q5,-3 10,0" stroke="#2A1510" stroke-width="2.2" fill="none" stroke-linecap="round"/>')  # closed eye
        out.append('<path d="M13,-411 q6,-4 12,-1" stroke="#2A1510" stroke-width="1.6" fill="none"/>')  # brow
        out.append('<path d="M15,-401 l2,3 M19,-400 l1,3 M23,-401 l0,3" stroke="#2A1510" stroke-width="1"/>')  # lashes
        out.append('<ellipse cx="18" cy="-392" rx="5" ry="3" fill="#F28B82" opacity="0.5"/>')  # blush
        out.append('<path d="M20,-381 q4,2 8,-1" stroke="#B0303A" stroke-width="2.6" fill="none" stroke-linecap="round"/>')  # smile
        out.append('<circle cx="26" cy="-416" r="2.2" fill="#C62828"/>')  # bindi
        out.append('<path d="M4,-432 L20,-420" stroke="%s" stroke-width="1.8"/><circle cx="21" cy="-419" r="3.2" fill="%s"/>' % (border, border))  # maang tikka
        out.append('<circle cx="31" cy="-388" r="4" fill="none" stroke="%s" stroke-width="1.6"/>' % border)  # nath
        out.append('<ellipse cx="0" cy="-398" rx="4" ry="6" fill="%s"/>' % skin[1])  # ear
        out.append('<path d="M0,-392 v5" stroke="%s" stroke-width="1.5"/><path d="M-5,-386 h10 l-5,9 z" fill="%s"/><circle cx="0" cy="-376" r="2" fill="%s"/>' % (border, border, border))  # jhumka
        # braid swinging with parandi
        out.append('<path d="M-30,-392 C-44,-374 -48,-350 -60,-330" stroke="%s" stroke-width="9" fill="none" stroke-linecap="round"/>' % HAIR)
        out.append('<path d="M-60,-330 l-6,18 M-60,-330 l0,20 M-60,-330 l6,18" stroke="%s" stroke-width="3"/><circle cx="-60" cy="-330" r="4" fill="%s"/>' % (dup, border))
    else:
        out.append('<path d="M-30,-392 C-44,-374 -48,-350 -60,-330" stroke="%s" stroke-width="9" fill="none" stroke-linecap="round"/>' % S)
    # ---------- front arm
    out.append(_arm(c, shF, fe, fw, sk, choli, border, () if S else ("#C62828", border, "#1E9E6A", border), 20, fist, S))
    if sticks:
        ux, uy = _unit(fe, fw)
        out.append(_stick(c, (fw[0] + ux * 9, fw[1] + uy * 9), -62, 150, 11, sticks, S))
    # twirl swish lines
    if not S:
        out.append('<path d="M-206,-110 C-222,-70 -210,-34 -178,-10 M204,-80 C220,-44 208,-12 184,4" stroke="%s" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.55"/>' % border)
    out.append("</g>")
    return "".join(out)


# ------------------------------------------------------------------ male
MPOSE = {
    # front arm elbow/wrist, back arm elbow/wrist, stick angles
    "up": (((62, -392), (74, -448)), ((-58, -386), (-66, -442)), -60, -122),
    "cross": (((76, -326), (90, -378)), ((-66, -328), (-76, -380)), -78, -102),
}


def dancer_m(c, x, y, s=1.0, flip=False, col=None, skin=SKIN, stick=("#E53935", "#FFD740"), sil=None, pose="up"):
    col = col or {}
    ked = col.get("kediyu", "#FFF4E0")
    trim = col.get("trim", "#D81B60")
    pagdi = col.get("pagdi", ["#E53935", "#FFB300", "#43A047"])
    pant = col.get("pant", "#F3E5C8")
    border = col.get("border", "#FFC53D")
    S = sil
    sk = S or c.lg([(0, skin[0]), (1, skin[1])], 0, 0, 1, 1)
    (fe, fw), (be, bw), af, ab = MPOSE.get(pose, MPOSE["up"])
    out = ['<g transform="translate(%s,%s) scale(%s,%s)">' % (f(x), f(y), f(-s if flip else s), f(s))]
    shF, shB = (34, -368), (-30, -368)
    # ---------- legs (churidar): back leg planted, front leg lifted
    legB = [(-12, -250), (-22, -190), (-34, -128), (-30, -66), (-26, -16)]
    legF = [(16, -250), (46, -212), (78, -172), (70, -128), (58, -80)]
    for lg_, w0 in ((legB, 36), (legF, 36)):
        d = _limb_path(lg_, [w0, w0 * 0.9, w0 * 0.72, w0 * 0.6, w0 * 0.52])
        out.append('<path d="%s" fill="%s"/>' % (d, S or c.lg([(0, pant), (1, "#CDBF9E")], 0, 0, 1, 0)))
        if not S:
            out.append('<path d="%s" fill="none" stroke="#8C7A55" stroke-opacity="0.35" stroke-width="2"/>' % d)
            # churidar gathers near the ankle
            a, b = lg_[-2], lg_[-1]
            ux, uy = _unit(a, b)
            nx, ny = -uy, ux
            for k in range(5):
                px, py = _lerp(a, b, 0.1 + k * 0.18)
                out.append('<path d="M%s,%s q%s,%s %s,%s" stroke="#9E8C66" stroke-width="1.6" fill="none"/>' % (
                    f(px + nx * 9), f(py + ny * 9), f(-nx * 9 + ux * 4), f(-ny * 9 + uy * 4), f(-nx * 18), f(-ny * 18)))
    # mojari shoes with curled toes
    for (fx, fy, rot) in ((-26, -8, 0), (62, -74, -30)):
        out.append('<g transform="translate(%s,%s) rotate(%s)"><path d="M-18,6 C-20,-8 8,-12 22,-4 C30,-2 36,-8 38,-14 C40,-4 34,8 20,8 Z" fill="%s"/>' % (f(fx), f(fy), f(rot), S or trim))
        if not S:
            out.append('<path d="M-12,-2 C0,-6 12,-4 22,-2" stroke="%s" stroke-width="2.5" fill="none"/>' % border)
        out.append('</g>')
    # ---------- back arm + stick
    out.append(_stick(c, _lerp(be, bw, 1.18), ab, 160, 12, stick, S))
    out.append(_arm(c, shB, be, bw, sk, ked, trim, () if S else (border, trim, border), 23, True, S))
    # ---------- kediyu: fitted yoke + pleated flared frock
    tilt = -10
    fr_top_y, fr_bot_y = -300, -206
    hem = []
    for i in range(25):
        t = i / 24
        xx = -86 + 176 * t
        yy = fr_bot_y + tilt * (1 - 2 * t) + 8 * math.sin(t * math.pi * 6)
        hem.append((xx, yy))
    fr = "M-24,%d L26,%d C50,-270 74,-240 90,%s L%s L-86,%s C-72,-240 -50,-270 -24,%d Z" % (
        fr_top_y, fr_top_y, f(hem[-1][1]), " L".join("%s,%s" % (f(a), f(b)) for a, b in reversed(hem)), f(hem[0][1]), fr_top_y)
    out.append('<path d="%s" fill="%s"/>' % (fr, S or ked))
    if not S:
        cp = c.clip('<path d="%s"/>' % fr)
        out.append('<g clip-path="%s">' % cp)
        for k in range(24):
            t = (k + 0.5) / 24
            hx = -86 + 176 * t
            out.append('<path d="M%s,%d L%s,%s" stroke="#000" stroke-opacity="%s" stroke-width="4"/>' % (f(1 + (hx) * 0.25), fr_top_y, f(hx), f(fr_bot_y + 20), "0.12" if k % 2 else "0.05"))
        out.append('<rect x="-100" y="-310" width="200" height="120" fill="%s"/>' % c.lg([(0, "#000", 0.22), (0.35, "#fff", 0.2), (0.6, "#fff", 0), (1, "#000", 0.25)], 0, 0, 1, 0))
        out.append('</g>')
        out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="10"/>' % (pts(hem), trim))
        out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="3 5"/>' % (pts([(a, b - 1) for a, b in hem]), border))
        for a, b in hem[1::3]:
            out.append('<circle cx="%s" cy="%s" r="3" fill="#EEF4FF" stroke="#8B5A00" stroke-width="0.8"/>' % (f(a), f(b)))
    # yoke / bodice
    yoke = "M-32,-370 C-10,-382 16,-382 38,-370 C38,-348 32,-322 27,-300 L-25,-300 C-30,-322 -36,-348 -32,-370 Z"
    out.append('<path d="%s" fill="%s"/>' % (yoke, S or ked))
    if not S:
        out.append('<path d="%s" fill="%s"/>' % (yoke, c.lg([(0, "#fff", 0.2), (0.5, "#fff", 0), (1, "#000", 0.22)], 0, 0, 1, 0)))
        # embroidered chest yoke with mirrors
        out.append('<path d="M-22,-368 C-6,-352 14,-352 30,-368 L28,-346 C12,-334 -4,-334 -22,-346 Z" fill="%s"/>' % trim)
        for (mx, my) in ((-12, -352), (0, -346), (12, -346), (22, -354), (4, -358)):
            out.append('<circle cx="%s" cy="%s" r="3.2" fill="#EEF4FF" stroke="%s" stroke-width="1.3"/>' % (mx, my, border))
        out.append('<path d="M3,-344 V-302" stroke="%s" stroke-width="2"/>' % trim)
        for yy in range(-338, -304, 9):
            out.append('<circle cx="7" cy="%d" r="2" fill="%s"/>' % (yy, border))
        # kamarbandh sash with hanging end
        out.append('<path d="M-26,-306 L28,-306 L28,-292 L-26,-292 Z" fill="%s"/>' % pagdi[1])
        out.append('<path d="M-18,-296 C-30,-276 -40,-256 -56,-242 L-44,-236 C-32,-252 -22,-270 -10,-292 Z" fill="%s"/>' % pagdi[1])
        out.append('<path d="M-56,-242 l-4,10 M-50,-238 l-2,10 M-44,-236 l0,10" stroke="%s" stroke-width="2.5"/>' % pagdi[0])
    # ---------- neck + head
    out.append('<path d="M-4,-396 L12,-396 L13,-372 L-5,-372 Z" fill="%s"/>' % sk)
    face = "M-12,-420 C2,-434 26,-430 30,-410 C32,-402 36,-398 32,-393 C32,-388 30,-386 30,-382 C26,-374 16,-372 8,-374 C-6,-378 -14,-392 -14,-406 Z"
    out.append('<path d="%s" fill="%s"/>' % (face, sk))
    if not S:
        out.append('<path d="%s" fill="%s"/>' % (face, c.rg([(0, "#fff", 0.22), (0.6, "#fff", 0), (1, "#7A3E22", 0.22)], 0.65, 0.35, 0.7)))
        out.append('<path d="M-14,-404 C-14,-392 -10,-384 -4,-382 L-2,-400 Z" fill="%s"/>' % HAIR)  # sideburn
        out.append('<ellipse cx="0" cy="-400" rx="4" ry="6.5" fill="%s"/>' % skin[1])
        out.append('<path d="M16,-406 q5,-3 10,0" stroke="#2A1510" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
        out.append('<path d="M15,-413 q6,-3 12,0" stroke="#2A1510" stroke-width="2" fill="none"/>')
        out.append('<path d="M12,-388 C18,-392 26,-392 34,-388 C30,-384 24,-385 20,-386 C18,-384 14,-384 12,-388 Z" fill="%s"/>' % HAIR)  # mustache
        out.append('<path d="M20,-381 q4,2 8,0" stroke="#8A2A2A" stroke-width="2" fill="none" stroke-linecap="round"/>')
        out.append('<path d="M-8,-372 C0,-362 16,-362 22,-372" stroke="%s" stroke-width="3" fill="none"/>' % border)  # kanthi
        out.append('<circle cx="-1" cy="-392" r="2.4" fill="%s"/>' % border)  # earring
    # pagdi: dome with wrapped bands, tail (chhogu), kalgi
    dome = "M-18,-414 C-26,-446 2,-462 24,-452 C38,-446 40,-428 34,-412 C18,-420 -2,-422 -18,-414 Z"
    out.append('<path d="M-16,-420 C-40,-414 -58,-396 -64,-360 L-50,-362 C-44,-388 -30,-404 -12,-412 Z" fill="%s"/>' % (S or pagdi[0]))
    out.append('<path d="%s" fill="%s"/>' % (dome, S or pagdi[0]))
    if not S:
        dots = c.pattern(10, 10, '<circle cx="3" cy="3" r="1.4" fill="#FFF3D0"/><circle cx="8" cy="8" r="1.4" fill="#FFF3D0"/>')
        out.append('<path d="%s" fill="%s" opacity="0.6"/>' % (dome, dots))
        for k, colr in enumerate(pagdi):
            yy = -418 - k * 9
            out.append('<path d="M%s,%s C-2,%s 18,%s %s,%s" stroke="%s" stroke-width="5" fill="none" stroke-linecap="round"/>' % (
                f(-18 + k * 2), f(yy), f(yy - 8), f(yy - 10), f(35 - k * 2), f(yy + 2), colr if k else pagdi[1]))
        out.append('<path d="%s" fill="%s"/>' % (dome, c.lg([(0, "#fff", 0.25), (0.5, "#fff", 0), (1, "#000", 0.25)], 0, 0, 1, 0)))
        out.append('<path d="M-64,-360 l-3,10 M-58,-361 l-1,10 M-52,-362 l1,10" stroke="%s" stroke-width="2.5"/>' % pagdi[1])
        out.append('<path d="M22,-450 C24,-474 40,-482 46,-470 C38,-468 32,-460 28,-448 Z" fill="%s"/>' % pagdi[2])
        out.append('<circle cx="24" cy="-449" r="4.5" fill="%s" stroke="#fff" stroke-width="1"/>' % border)
    # ---------- front arm + stick
    out.append(_stick(c, _lerp(fe, fw, 1.18), af, 160, 12, stick, S))
    out.append(_arm(c, shF, fe, fw, sk, ked, trim, () if S else (border, trim, border), 23, True, S))
    out.append("</g>")
    return "".join(out)
