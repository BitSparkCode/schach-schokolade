"""Buchform: alle Figuren einer Farbe in einem Guss.

Platten stehen senkrecht hintereinander (Stapelrichtung Y). Zwischen zwei
Platten liegt eine Trennebene mit einer Reihe Kavitäten. Innenplatten tragen
auf beiden Seiten Halbkavitäten. Vier Gewindestangen M5 führen und spannen
den Stapel. Gegossen wird kopfüber, die Standflächen liegen in der Giessebene
oben. Gedruckt wird jede Platte stehend in Giesslage.
"""
from dataclasses import dataclass, field

import cadquery as cq

import figuren


@dataclass
class Massen:
    boden: float = 4.0          # Material unter dem höchsten Kopf
    wand_aussen: float = 6.0    # Endplatten hinter der tiefsten Kavität
    wand_innen: float = 4.0     # Steg zwischen zwei Rücken an Rücken liegenden Kavitäten
    abstand: float = 8.0        # Steg zwischen Kavitäten in einer Reihe
    rand_x: float = 20.0        # seitlich, Platz für die Gewindestangen
    stange_d: float = 5.4       # Bohrung für M5, nach dem Druck mit 5 mm aufbohren
    stange_rand: float = 9.0    # Mitte Stange bis Plattenrand
    stange_z: tuple = (12.0, 44.0)
    stift_d: float = 4.1        # Edelstahl-Passstift 4 × 16 mm, je Trennebene zwei
    stift_tiefe: float = 8.2
    trichter_hoehe: float = 10.0
    trichter_rand: float = 3.0  # Trichteröffnung oben = Fuss Ø + 2 × rand
    trichter_schuerze: float = 5.0
    spiel: float = 0.4


VOLLSATZ = [
    ["koenig", "dame", "laeufer", "laeufer"],
    ["springer", "springer", "turm", "turm"],
    ["bauer", "bauer", "bauer", "bauer"],
    ["bauer", "bauer", "bauer", "bauer"],
]
PROBE = [["bauer", "springer"]]


@dataclass
class Form:
    reihen: list
    m: Massen = field(default_factory=Massen)

    def __post_init__(self):
        m = self.m
        self.hoehe = max(figuren.SET[k].hoehe for r in self.reihen for k in r) + m.boden
        self.radien = [max(figuren.SET[k].fuss_d / 2 for k in r) for r in self.reihen]
        self.laengen = [sum(figuren.SET[k].fuss_d for k in r) + m.abstand * (len(r) - 1) for r in self.reihen]
        self.breite = max(self.laengen) + 2 * m.rand_x
        y = [0.0]
        for a, b in zip(self.radien, self.radien[1:]):
            y.append(y[-1] + a + m.wand_innen + b)
        self.ebenen = y
        self.grenzen = [y[0] - self.radien[0] - m.wand_aussen] + y + [y[-1] + self.radien[-1] + m.wand_aussen]
        self.tiefe = self.grenzen[-1] - self.grenzen[0]

    def kavitaeten(self):
        """Figuren in Giesslage: Kopf unten, Standfläche in z = hoehe."""
        teile = []
        for reihe, y, laenge in zip(self.reihen, self.ebenen, self.laengen):
            x = -laenge / 2
            for k in reihe:
                f = figuren.SET[k]
                x += f.fuss_d / 2
                fig = figuren.figur(k).rotate((0, 0, 0), (1, 0, 0), 180).translate((x, y, self.hoehe))
                teile.append((k, x, y, fig))
                x += f.fuss_d / 2 + self.m.abstand
        return teile

    def stangen(self):
        m = self.m
        xs = (-self.breite / 2 + m.stange_rand, self.breite / 2 - m.stange_rand)
        return [(x, z) for x in xs for z in m.stange_z]

    def platten(self):
        m = self.m
        hohl = None
        for _, _, _, fig in self.kavitaeten():
            hohl = fig if hohl is None else hohl.union(fig)
        for x, z in self.stangen():
            bohrung = cq.Workplane("XZ").circle(m.stange_d / 2).extrude(self.tiefe + 20, both=True).translate((x, 0, z))
            hohl = hohl.union(bohrung)
        for x, _ in self.stangen()[::2]:
            for y in self.ebenen:
                stift = cq.Workplane("XZ").circle(m.stift_d / 2).extrude(m.stift_tiefe, both=True).translate((x, y, self.hoehe / 2))
                hohl = hohl.union(stift)
        teile = []
        for i, (y0, y1) in enumerate(zip(self.grenzen, self.grenzen[1:])):
            block = cq.Workplane("XY").box(self.breite, y1 - y0, self.hoehe, centered=(True, False, False)).translate((0, y0, 0))
            teile.append((f"platte_{i + 1}", block.cut(hohl)))
        return teile

    def trichterplatte(self):
        """Liegt auf der Giessebene, Schürze rundum fixiert sie auf dem Stapel."""
        m = self.m
        b, t = self.breite + 2 * (m.spiel + 2.4), self.tiefe + 2 * (m.spiel + 2.4)
        y_mitte = (self.grenzen[0] + self.grenzen[-1]) / 2
        platte = cq.Workplane("XY").box(b, t, m.trichter_hoehe, centered=(True, True, False)).translate((0, y_mitte, self.hoehe))
        schuerze = (
            cq.Workplane("XY").box(b, t, m.trichter_schuerze, centered=(True, True, False))
            .cut(cq.Workplane("XY").box(self.breite + 2 * m.spiel, self.tiefe + 2 * m.spiel, m.trichter_schuerze, centered=(True, True, False)))
            .translate((0, y_mitte, self.hoehe - m.trichter_schuerze))
        )
        platte = platte.union(schuerze)
        for k, x, y, _ in self.kavitaeten():
            r = figuren.SET[k].fuss_d / 2
            trichter = cq.Solid.makeCone(r, r + m.trichter_rand, m.trichter_hoehe, cq.Vector(x, y, self.hoehe))
            platte = platte.cut(cq.Workplane().add(trichter))
        return platte
