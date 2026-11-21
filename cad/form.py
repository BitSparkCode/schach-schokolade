"""Buchform: alle Figuren einer Farbe in einem Guss.

Platten stehen senkrecht hintereinander (Stapelrichtung Y). Zwischen zwei
Platten liegt eine Trennebene mit einer Reihe Kavitäten. Innenplatten tragen
auf beiden Seiten Halbkavitäten. Vier Gewindestangen M5 führen und spannen
den Stapel. Gedruckte Kegelnoppen richten die Platten aus: Die ungeraden
Platten (1, 3, 5) tragen die Noppen, die geraden die Aufnahmen. Gegossen wird kopfüber, die Standflächen liegen in der Giessebene
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
    noppe_d: float = 8.0        # Kegelnoppe am Fuss, 45° Flanke, je Trennebene zwei
    noppe_h: float = 3.0
    noppe_versatz: float = 4.0  # links tiefer, rechts höher: Platte passt nur richtig herum
    noppe_spiel: float = 0.1    # Aufnahme radial grösser
    noppe_luft: float = 0.5     # Aufnahme tiefer, die Trennflächen schliessen zuerst
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
        bloecke = []
        for y0, y1 in zip(self.grenzen, self.grenzen[1:]):
            bloecke.append(cq.Workplane("XY").box(self.breite, y1 - y0, self.hoehe, centered=(True, False, False)).translate((0, y0, 0)))
        for j, y in enumerate(self.ebenen):
            noppe, aufnahme, richtung = (j, j + 1, 1) if j % 2 == 0 else (j + 1, j, -1)
            for x, z in self.noppen():
                fuss, achse = cq.Vector(x, y, z), cq.Vector(0, richtung, 0)
                r, rs, h = m.noppe_d / 2, m.noppe_d / 2 + m.noppe_spiel, m.noppe_h + m.noppe_luft
                bloecke[noppe] = bloecke[noppe].union(cq.Workplane().add(cq.Solid.makeCone(r, r - m.noppe_h, m.noppe_h, fuss, achse)))
                bloecke[aufnahme] = bloecke[aufnahme].cut(cq.Workplane().add(cq.Solid.makeCone(rs, rs - h, h, fuss, achse)))
        return [(f"platte_{i + 1}", b.cut(hohl)) for i, b in enumerate(bloecke)]

    def noppen(self):
        """(x, z) der zwei Noppen je Trennebene, auf der Höhe der Gewindestangen."""
        m = self.m
        (xl, _), _, (xr, _), _ = self.stangen()
        return [(xl, self.hoehe / 2 - m.noppe_versatz), (xr, self.hoehe / 2 + m.noppe_versatz)]

    def schleifbahn(self):
        """Breiteste Schleifbahn zwischen den Noppen der ungeraden Platten."""
        return round(self.breite - 2 * (self.m.stange_rand + self.m.noppe_d / 2) - 2, 1)

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
