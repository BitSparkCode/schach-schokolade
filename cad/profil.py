"""2D-Profile aus Punkten mit Radien: Geraden und Kreisbögen, exakt."""
import math

import cadquery as cq


def _bogen(p0, p1, p2, radius):
    """Tangentenpunkte und Bogenmitte für die Ecke p1 zwischen p0 und p2."""
    ax, ay = p0[0] - p1[0], p0[1] - p1[1]
    bx, by = p2[0] - p1[0], p2[1] - p1[1]
    la, lb = math.hypot(ax, ay), math.hypot(bx, by)
    ax, ay, bx, by = ax / la, ay / la, bx / lb, by / lb
    cos_w = max(-1.0, min(1.0, ax * bx + ay * by))
    winkel = math.acos(cos_w)
    if radius <= 0 or winkel > math.pi - 1e-3:
        return None
    abstand = radius / math.tan(winkel / 2)
    grenze = 0.45 * min(la, lb)
    if abstand > grenze:
        abstand = grenze
        radius = abstand * math.tan(winkel / 2)
    t1 = (p1[0] + ax * abstand, p1[1] + ay * abstand)
    t2 = (p1[0] + bx * abstand, p1[1] + by * abstand)
    hx, hy = ax + bx, ay + by
    lh = math.hypot(hx, hy)
    mitte_abstand = radius / math.sin(winkel / 2)
    zentrum = (p1[0] + hx / lh * mitte_abstand, p1[1] + hy / lh * mitte_abstand)
    mx, my = p1[0] - zentrum[0], p1[1] - zentrum[1]
    lm = math.hypot(mx, my)
    m = (zentrum[0] + mx / lm * radius, zentrum[1] + my / lm * radius)
    return t1, m, t2


def kontur(ebene, punkte, offen_am_ende=False):
    """Geschlossene Kontur. punkte: Liste (x, y, radius)."""
    n = len(punkte)
    wp = cq.Workplane(ebene)
    pts = [(p[0], p[1]) for p in punkte]
    segmente = []
    for i in range(n):
        r = punkte[i][2]
        b = _bogen(pts[i - 1], pts[i], pts[(i + 1) % n], r) if r > 0 else None
        segmente.append(b)
    start = segmente[0][2] if segmente[0] else pts[0]
    wp = wp.moveTo(*start)
    for i in list(range(1, n)) + [0]:
        b = segmente[i]
        if b:
            wp = wp.lineTo(*b[0]).threePointArc(b[1], b[2])
        elif i != 0:
            wp = wp.lineTo(*pts[i])
    return wp.close()


def drehkoerper(profil):
    """profil: Liste (r, z, radius), beginnt und endet auf der Achse."""
    return kontur("XZ", profil).revolve(360, (0, 0, 0), (0, 1, 0))
