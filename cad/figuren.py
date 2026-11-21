"""Figurenset Max' Schach Schokolade.

Alle Figuren stehen aufrecht, Standfläche bei z = 0, Achse = Z.
Trennebene der Giessform ist y = 0, entformt wird in Richtung ±Y.
Regeln (docs/03-figuren.md): keine Hinterschnitte in Y, Unterseiten
mindestens 45° steil, damit die Form entlüftet und ohne Stützen druckbar ist.
"""
from dataclasses import dataclass

import cadquery as cq

from profil import drehkoerper, kontur


@dataclass(frozen=True)
class Figur:
    name: str
    hoehe: float
    fuss_d: float
    anzahl: int


SET = {
    "koenig": Figur("König", 60.0, 26.0, 1),
    "dame": Figur("Dame", 55.0, 25.0, 1),
    "laeufer": Figur("Läufer", 48.0, 23.0, 2),
    "springer": Figur("Springer", 44.0, 23.0, 2),
    "turm": Figur("Turm", 40.0, 23.0, 2),
    "bauer": Figur("Bauer", 34.0, 20.0, 8),
}


def _fuss(r, oben_r, oben_z):
    """Standfuss mit Fase unten und Kehle nach oben."""
    return [
        (0, 0, 0),
        (r - 0.6, 0, 0),
        (r, 0.6, 0),
        (r, 3.4, 0.8),
        (oben_r, oben_z, 1.5),
    ]


def bauer():
    p = _fuss(10.0, 7.6, 5.0) + [
        (5.0, 14.0, 2.0),
        (4.4, 18.0, 1.5),
        (7.0, 21.0, 0.8),
        (7.0, 22.0, 0.8),
        (4.6, 23.2, 1.0),
        (4.6, 23.8, 1.0),
        (6.6, 26.0, 2.0),
        (6.6, 28.0, 3.0),
        (3.0, 34.0, 3.0),
        (0, 34.0, 0),
    ]
    return drehkoerper(p)


def turm():
    p = _fuss(11.5, 9.0, 5.5) + [
        (7.0, 12.0, 2.0),
        (6.6, 28.0, 1.5),
        (9.0, 31.0, 0.8),
        (9.0, 40.0, 0.8),
        (0, 40.0, 0),
    ]
    koerper = drehkoerper(p)
    # Zinnenlücke quer zur Trennebene: Wände parallel zur Entformrichtung Y
    luecke = cq.Workplane("XY").box(4.5, 30, 5.0, centered=(True, True, False)).translate((0, 0, 35.0))
    return koerper.cut(luecke)


def laeufer():
    p = _fuss(11.5, 9.0, 5.5) + [
        (5.0, 22.0, 3.0),
        (4.6, 27.0, 1.2),
        (7.2, 30.0, 0.8),
        (7.2, 31.0, 0.8),
        (4.6, 32.2, 1.0),
        (4.6, 33.0, 1.0),
        (6.8, 36.0, 2.5),
        (6.8, 39.0, 4.0),
        (2.0, 45.6, 0.8),
        (2.8, 46.5, 0.6),
        (2.8, 47.0, 0.8),
        (1.4, 48.0, 0.8),
        (0, 48.0, 0),
    ]
    return drehkoerper(p)


def dame():
    p = _fuss(12.5, 9.8, 6.0) + [
        (5.0, 30.0, 3.0),
        (5.0, 32.0, 1.2),
        (7.8, 35.2, 0.8),
        (7.8, 36.2, 0.8),
        (5.2, 37.4, 1.0),
        (5.2, 38.0, 1.0),
        (8.0, 47.5, 2.0),
        (8.0, 48.5, 0.8),
        (4.5, 49.5, 1.0),
        (2.2, 50.5, 0.6),
        (3.5, 52.0, 0.8),
        (3.5, 53.0, 1.2),
        (1.5, 55.0, 1.0),
        (0, 55.0, 0),
    ]
    return drehkoerper(p)


def _flach(umriss, dicke, schraege=4.0, kante=1.0):
    """Flacher Körper in der Trennebene, nach aussen verjüngt (Entformschräge)."""
    haelfte = kontur("XZ", umriss).extrude(dicke / 2, taper=schraege)
    try:
        haelfte = haelfte.faces("<Y").edges().fillet(kante)
    except Exception:
        pass
    return haelfte.union(haelfte.mirror("XZ"))


def koenig():
    p = _fuss(13.0, 10.4, 6.0) + [
        (5.4, 32.0, 3.0),
        (5.4, 34.0, 1.2),
        (8.4, 37.4, 0.8),
        (8.4, 38.4, 0.8),
        (5.6, 39.6, 1.0),
        (5.6, 40.2, 1.0),
        (8.4, 48.0, 2.0),
        (8.4, 49.0, 0.8),
        (4.0, 50.2, 0),
        (0, 50.2, 0),
    ]
    koerper = drehkoerper(p)
    kreuz = [
        (-2.25, 48.0, 0),
        (2.25, 48.0, 0),
        (2.25, 50.5, 0.6),
        (5.2, 53.5, 0.6),
        (5.2, 57.8, 0.8),
        (2.25, 57.8, 0.6),
        (2.25, 60.0, 0.8),
        (-2.25, 60.0, 0.8),
        (-2.25, 57.8, 0.6),
        (-5.2, 57.8, 0.8),
        (-5.2, 53.5, 0.6),
        (-2.25, 50.5, 0.6),
    ]
    return koerper.union(_flach(kreuz, 6.0, schraege=3.0, kante=0.8))


def springer():
    p = _fuss(11.5, 9.0, 5.5) + [
        (8.0, 9.0, 1.0),
        (0, 9.0, 0),
    ]
    fuss = drehkoerper(p)
    umriss = [
        (-6.5, 7.5, 0),
        (6.5, 7.5, 0),
        (4.2, 22.0, 2.0),
        (10.0, 30.0, 1.6),
        (9.0, 33.5, 1.6),
        (2.5, 40.0, 1.5),
        (-0.5, 44.0, 1.2),
        (-4.0, 44.0, 1.5),
        (-6.5, 38.0, 3.0),
        (-8.0, 28.0, 4.0),
    ]
    kopf = _flach(umriss, 14.0, schraege=5.0, kante=2.0)
    return fuss.union(kopf)


BAUER = {
    "koenig": koenig,
    "dame": dame,
    "laeufer": laeufer,
    "springer": springer,
    "turm": turm,
    "bauer": bauer,
}


def figur(schluessel):
    return BAUER[schluessel]()
