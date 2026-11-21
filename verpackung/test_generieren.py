import unittest
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from xml.etree import ElementTree

from pypdf import PdfReader

import generieren as g


SVG = "{http://www.w3.org/2000/svg}"


class VerpackungTest(unittest.TestCase):
    def assert_mm(self, pt, mm):
        self.assertAlmostEqual(float(pt) * 25.4 / 72, mm, places=3)

    def test_dateien_und_massstab(self):
        with TemporaryDirectory() as verzeichnis:
            ziel = Path(verzeichnis)
            g.generieren(ziel)
            pdf = PdfReader(ziel / "falzmuster.pdf")
            self.assertEqual(len(pdf.pages), 3)
            for name, seite, (breite, hoehe) in zip(("unterteil", "deckel", "einlage"), pdf.pages,
                                                    ((414, 451), (342, 379), (296, 353))):
                svg = ElementTree.parse(ziel / f"{name}.svg").getroot()
                self.assertEqual(svg.attrib["width"], f"{breite}mm")
                self.assertEqual(svg.attrib["height"], f"{hoehe}mm")
                self.assert_mm(seite.mediabox.width, breite)
                self.assert_mm(seite.mediabox.height, hoehe)
            einlage = ElementTree.parse(ziel / "einlage.svg")
            self.assertEqual(Counter(float(loch.attrib["r"]) * 2 for loch in einlage.iter(f"{SVG}circle")),
                             {27.5: 2, 26.5: 2, 24.5: 12, 21.5: 16})
            druck = PdfReader(ziel / "deckeldruck.pdf").pages[0]
            self.assert_mm(druck.trimbox.width, 252)
            self.assert_mm(druck.trimbox.height, 252)
            self.assert_mm(druck.bleedbox.width, 258)
            self.assert_mm(druck.trimbox.left, 3)
            felder = list(ElementTree.parse(ziel / "deckeldruck.svg").iter(f"{SVG}rect"))[1:]
            self.assertEqual(len(felder), 64)
            self.assertEqual(felder[0].attrib["fill"], g.CREME)
            self.assertEqual(felder[-8].attrib["fill"], g.BRAUN)

    def test_raster_und_figuren_aendern(self):
        with patch.object(g, "FELD", 32), patch.dict(g.FIGUREN, {"König": (64, 27)}):
            g.pruefe_masse()
            self.assertEqual(g.masse(), (256, 266, 268, 262, 69))
            loecher = list(g.loecher(262))
            self.assertEqual(Counter(farbe for farbe, *_ in loecher), {"dunkel": 16, "weiss": 16})
            self.assertEqual(loecher[4], ("dunkel", "König", 147, 19, 28.5))
        with patch.object(g, "FELD", 29):
            with self.assertRaisesRegex(ValueError, "Lochsteg zu schmal"):
                g.pruefe_masse()
