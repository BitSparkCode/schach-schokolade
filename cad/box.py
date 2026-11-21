"""Box für 32 Figuren, 3D-gedruckt, wiederverwendbar.

Unterteil mit Stülpdeckel. Die erhöhte Einlage hat Löcher in Grundstellung
(Reihen 1, 2, 7, 8). Die Füsse stehen auf dem Boden, die Lochwand fasst Fuss
und unteren Schaft. Deckel oben mit Schachbrett in zwei Farben (AMS),
Beschriftung unten auf dem Unterteil.
"""
from dataclasses import dataclass

import cadquery as cq

import figuren

GRUNDREIHE = ["turm", "springer", "laeufer", "dame", "koenig", "laeufer", "springer", "turm"]


@dataclass
class BoxMasse:
    deckel_aussen: float = 240.0   # = Schachbrett, 8 Felder à 30 mm
    wand: float = 2.4
    boden: float = 2.0
    spiel: float = 0.3             # Deckel über Unterteil
    luft_oben: float = 3.0         # über dem König
    raster: float = 28.0           # Abstand der Löcher in der Einlage
    loch_spiel: float = 0.8        # Loch Ø = Fuss Ø + loch_spiel
    einlage_hoehe: float = 8.0
    einlage_decke: float = 2.0
    einlage_spiel: float = 0.5
    rohr_wand: float = 1.6         # Material um das Loch bis zum Rand des Bands
    deckel_schuerze: float = 20.0
    deckel_decke: float = 2.4
    brett_tiefe: float = 0.6       # dunkle Felder, eigene Farbe
    text: str = "Max' Schach Schokolade"
    text_unten: str = "Schokolade dunkel und weiss · kühl und trocken lagern"
    text_tiefe: float = 0.6


class Box:
    def __init__(self, m=None):
        self.m = m = m or BoxMasse()
        self.unterteil_aussen = m.deckel_aussen - 2 * (m.wand + m.spiel)
        self.innen = self.unterteil_aussen - 2 * m.wand
        self.koenig = max(f.hoehe for f in figuren.SET.values())
        self.innen_hoehe = self.koenig + m.luft_oben
        self.unterteil_hoehe = m.boden + self.innen_hoehe

    def positionen(self):
        """(schlüssel, x, y, farbe) in Grundstellung, Mitte der Box = 0."""
        r = self.m.raster
        pos = []
        for spalte, k in enumerate(GRUNDREIHE):
            x = (spalte - 3.5) * r
            pos += [(k, x, -3.5 * r, "weiss"), ("bauer", x, -2.5 * r, "weiss")]
            pos += [(k, x, 3.5 * r, "dunkel"), ("bauer", x, 2.5 * r, "dunkel")]
        return pos

    def unterteil(self):
        m = self.m
        a, h = self.unterteil_aussen, self.unterteil_hoehe
        teil = (
            cq.Workplane("XY").box(a, a, h, centered=(True, True, False))
            .edges("|Z").fillet(3.0)
            .faces(">Z").shell(-m.wand)
        )
        return teil.cut(self._text_koerper(tief=True))

    def _text_koerper(self, tief):
        """Beschriftung auf der Unterseite, von unten lesbar."""
        m = self.m
        ebene = cq.Plane(origin=(0, 0, 0), xDir=(1, 0, 0), normal=(0, 0, -1))
        titel = cq.Workplane(ebene).center(0, 8).text(m.text, 14, -m.text_tiefe, combine=False, halign="center", valign="center")
        zeile = cq.Workplane(ebene).center(0, -12).text(m.text_unten, 6, -m.text_tiefe, combine=False, halign="center", valign="center")
        return titel.union(zeile)

    def beschriftung(self):
        """Füllkörper für die Gravur, in zweiter Farbe drucken."""
        return self._text_koerper(tief=True)

    def einlage(self):
        m = self.m
        a = self.innen - 2 * m.einlage_spiel
        decke = cq.Workplane("XY").box(a, a, m.einlage_decke, centered=(True, True, False)).translate((0, 0, m.einlage_hoehe - m.einlage_decke))
        schuerze = (
            cq.Workplane("XY").box(a, a, m.einlage_hoehe, centered=(True, True, False))
            .cut(cq.Workplane("XY").box(a - 2 * m.wand, a - 2 * m.wand, m.einlage_hoehe, centered=(True, True, False)))
        )
        teil = decke.union(schuerze)
        innen = min(abs(y) - (figuren.SET[k].fuss_d + m.loch_spiel) / 2 - m.rohr_wand for k, _, y, _ in self.positionen())
        for seite in (-1, 1):
            band = cq.Workplane("XY").box(a, a / 2 - innen, m.einlage_hoehe, centered=(True, False, False))
            teil = teil.union(band.translate((0, innen, 0)) if seite > 0 else band.translate((0, -a / 2, 0)))
        for k, x, y, _ in self.positionen():
            d = figuren.SET[k].fuss_d + m.loch_spiel
            loch = cq.Workplane("XY").circle(d / 2).extrude(m.einlage_hoehe + 1).translate((x, y, -0.5))
            fase = cq.Solid.makeCone(d / 2, d / 2 + 1.0, 1.0, cq.Vector(x, y, m.einlage_hoehe - 1.0))
            teil = teil.cut(loch).cut(cq.Workplane().add(fase))
        for x in (-20.0, 20.0):
            griff = cq.Workplane("XY").slot2D(24, 14).extrude(m.einlage_hoehe + 1).translate((x, 0, -0.5))
            teil = teil.cut(griff)
        return teil

    def _brett(self):
        """Dunkle Felder auf der Deckeloberseite, bündig eingelegt."""
        m = self.m
        feld = m.deckel_aussen / 8
        oben = m.deckel_schuerze + m.deckel_decke
        felder = None
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    # 0.05 mm kleiner: Felder berühren sich an den Ecken nicht
                    f = cq.Workplane("XY").box(feld - 0.1, feld - 0.1, m.brett_tiefe, centered=(True, True, False)).translate(
                        ((i - 3.5) * feld, (j - 3.5) * feld, oben - m.brett_tiefe))
                    felder = f if felder is None else felder.union(f)
        return felder

    def deckel(self):
        m = self.m
        a, h = m.deckel_aussen, m.deckel_schuerze + m.deckel_decke
        teil = (
            cq.Workplane("XY").box(a, a, h, centered=(True, True, False))
            .edges("|Z").fillet(3.0 + m.wand)
            .faces("<Z").shell(-m.wand)
        )
        for y in (-a / 2, a / 2):
            griff = cq.Workplane("XZ").center(0, 0).slot2D(40, 16).extrude(10, both=True).translate((0, y, 0))
            teil = teil.cut(griff)
        return teil.cut(self._brett())

    def deckel_felder(self):
        return self._brett()
