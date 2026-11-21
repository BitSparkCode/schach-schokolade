from html import escape
from io import BytesIO
from pathlib import Path

import cairosvg
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject


# Masse in mm
FIGUREN = {
    "König": (60, 26),
    "Dame": (55, 25),
    "Läufer": (48, 23),
    "Springer": (44, 23),
    "Turm": (40, 23),
    "Bauer": (34, 20),
}
FELD = 30
RAND_UNTERTEIL = 5
DECKELSPIEL = 1  # je Seite, zwischen den Rillachsen
EINLAGENSPIEL = 2  # je Seite, zwischen den Rillachsen
KOPFSPIEL = 5
DECKELTIEFE = 28
EINLAGENHOEHE = 8
LOCHZUGABE = 1.5  # Durchmesser, inkl. vorgesehener Einzelhülle
ANSCHNITT = 3
MIN_STEG = 3
KLEBELASCHE = 14

SCHNITT = "#a5263c"
FALZ = "#205595"
KLEBUNG = "#3c795a"
MASS = "#4d4d49"
BRAUN = "#4b3027"
CREME = "#e9dccc"
BRETTRAND = "#b99a6a"
WEISS = "#f7f0e5"

GRUNDREIHE = ("Turm", "Springer", "Läufer", "Dame", "König", "Läufer", "Springer", "Turm")
BAUERNREIHE = ("Bauer",) * 8


def masse():
    brett = 8 * FELD
    boden = brett + 2 * RAND_UNTERTEIL
    deckel = boden + 2 * DECKELSPIEL
    einlage = boden - 2 * EINLAGENSPIEL
    hoehe = max(h for h, _ in FIGUREN.values()) + KOPFSPIEL
    return brett, boden, deckel, einlage, hoehe


def loecher(seite):
    rand = (seite - 8 * FELD) / 2
    reihen = (("dunkel", 0, GRUNDREIHE), ("dunkel", 1, BAUERNREIHE),
              ("weiss", 6, BAUERNREIHE), ("weiss", 7, GRUNDREIHE))
    for farbe, reihe, figuren in reihen:
        for spalte, figur in enumerate(figuren):
            _, fuss = FIGUREN[figur]
            yield farbe, figur, rand + (spalte + 0.5) * FELD, rand + (reihe + 0.5) * FELD, fuss + LOCHZUGABE


def pruefe_masse():
    brett, boden, deckel, einlage, hoehe = masse()
    if min(FELD, DECKELSPIEL, EINLAGENSPIEL, KOPFSPIEL, ANSCHNITT, LOCHZUGABE) <= 0:
        raise ValueError("Feld, Spiele, Lochzugabe und Anschnitt müssen positiv sein.")
    if (deckel - brett) / 2 < 3:
        raise ValueError("Brettrand für die Koordinaten zu schmal.")
    if not (0 < DECKELTIEFE < hoehe and 0 < EINLAGENHOEHE < hoehe):
        raise ValueError("Deckeltiefe oder Einlagenhöhe prüfen.")
    if min(DECKELTIEFE, EINLAGENHOEHE, hoehe, KLEBELASCHE + 1) < 7:
        raise ValueError("Wände oder Klebelaschen für den Zuschnitt zu klein.")
    for figur, (h, fuss) in FIGUREN.items():
        if h <= EINLAGENHOEHE or fuss <= 0:
            raise ValueError(f"Ungültige Figur: {figur}")
    punkte = list(loecher(einlage))
    for i, (_, figur, x, y, d) in enumerate(punkte):
        if min(x, y, einlage - x, einlage - y) - d / 2 < MIN_STEG:
            raise ValueError(f"Randsteg zu schmal: {figur}")
        for _, andere, xx, yy, dd in punkte[:i]:
            if ((x - xx) ** 2 + (y - yy) ** 2) ** 0.5 - (d + dd) / 2 < MIN_STEG:
                raise ValueError(f"Lochsteg zu schmal: {figur} / {andere}")


def zahl(val):
    return f"{val:.5f}".rstrip("0").rstrip(".")


def mm(val):
    return zahl(val).replace(".", ",")


def element(tag, **attrs):
    return f"<{tag}{attribute(attrs)}/>"


def attribute(attrs):
    return "".join(
        f' {key.replace("_", "-")}="{escape(zahl(val) if isinstance(val, (int, float)) else val, quote=True)}"'
        for key, val in attrs.items()
    )


def linie(x1, y1, x2, y2, **attrs):
    return element("line", x1=x1, y1=y1, x2=x2, y2=y2, **attrs)


def flaeche(punkte, **attrs):
    return element("polygon", points=" ".join(f"{zahl(x)},{zahl(y)}" for x, y in punkte), **attrs)


def text(x, y, beschriftung, **attrs):
    return f'<text{attribute(dict(x=x, y=y, **attrs))}>{escape(beschriftung)}</text>'


def svg(w, h, inhalt, *, raster=False):
    einheit = "" if raster else "mm"
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{zahl(w)}{einheit}" '
        f'height="{zahl(h)}{einheit}" viewBox="0 0 {zahl(w)} {zahl(h)}" '
        'font-family="DejaVu Sans, sans-serif">\n'
        + "\n".join(inhalt) + "\n</svg>\n"
    )


def tray(kante, tiefe):
    a = kante
    d = tiefe
    l = min(KLEBELASCHE, d - 1)
    schraege = min(2, l / 3)
    abstand = 1
    kontur = [
        (-l, -d + schraege), (0, -d), (a, -d), (a + l, -d + schraege),
        (a + l, -abstand - schraege), (a, 0), (a + d, 0), (a + d, a),
        (a, a), (a + l, a + abstand + schraege), (a + l, a + d - schraege),
        (a, a + d), (0, a + d), (-l, a + d - schraege),
        (-l, a + abstand + schraege), (0, a), (-d, a), (-d, 0),
        (0, 0), (-l, -abstand - schraege),
    ]
    falze = [
        (0, 0, a, 0), (a, 0, a, a), (a, a, 0, a), (0, a, 0, 0),
        (0, -d, 0, 0), (a, -d, a, 0), (0, a, 0, a + d), (a, a, a, a + d),
    ]
    klebeflaechen = [
        (x, y, l - 2, d - 5.6)
        for x in (-l + 1, a + 1) for y in (-d + 2.8, a + 2.8)
    ]
    return kontur, falze, klebeflaechen, l


def masslinie(x1, y1, x2, y2, wert):
    dx, dy = (0, 1.5) if y1 == y2 else (1.5, 0)
    u, v = (x1 + x2) / 2, (y1 + y2) / 2
    attrs = dict(fill=MASS, font_size=3, text_anchor="middle")
    if x1 == x2:
        attrs["transform"] = f"rotate(-90 {zahl(u - 1.2)} {zahl(v)})"
    return [
        linie(x1, y1, x2, y2, stroke=MASS, stroke_width=0.2),
        linie(x1 - dx, y1 - dy, x1 + dx, y1 + dy, stroke=MASS, stroke_width=0.2),
        linie(x2 - dx, y2 - dy, x2 + dx, y2 + dy, stroke=MASS, stroke_width=0.2),
        text(u - (1.2 if dx else 0), v - (1.2 if dy else 0), mm(wert), **attrs),
    ]


def dieline(titel, a, d, *, einlage=False):
    falzstrich = "4 1 0.7 1" if einlage else "4 2"
    falzname = "Bergfalz (Wände nach unten)" if einlage else "Talfalz (Wände nach oben)"
    gesamt = a + 2 * d
    links, oben = d + 17, d + 38
    unten = gesamt + 38
    w, h = gesamt + 34, unten + (53 if einlage else 33)
    kontur, falze, klebeflaechen, lasche = tray(a, d)
    inhalt = [
        text(22, 13, titel, fill=MASS, font_size=6),
        text(22, 20, "1:1  |  mm  |  Ansicht von oben  |  Masse ab Rillachse", fill=MASS, font_size=3),
        f'<g transform="translate({zahl(links)} {zahl(oben)})">',
        flaeche(kontur, fill="none", stroke=SCHNITT, stroke_width=0.3, id="schnitt-aussen"),
    ]
    inhalt.extend(
        linie(*coords, stroke=FALZ, stroke_width=0.28, stroke_dasharray=falzstrich)
        for coords in falze
    )
    inhalt.extend(
        element("rect", x=x, y=y, width=w, height=h, fill="#e4efe7", stroke=KLEBUNG,
                stroke_width=0.25, stroke_dasharray="0.7 0.8")
        for x, y, w, h in klebeflaechen
    )
    if einlage:
        for farbe, figur, x, y, durchmesser in loecher(a):
            inhalt.append(element("circle", cx=x, cy=y, r=durchmesser / 2, fill="none",
                                  stroke=SCHNITT, stroke_width=0.3))
        for y, farbe, figurengruppe in ((a / 2 - 15, "Dunkel", "Grundreihe, dann Bauern"),
                                       (a / 2 + 13, "Weiss", "Bauern, dann Grundreihe")):
            inhalt.append(text(a / 2, y, f"{farbe}: {figurengruppe}", fill=MASS, font_size=3,
                               text_anchor="middle"))
    inhalt.append("</g>")
    inhalt.extend(masslinie(links, 31, links + a, 31, a))
    inhalt.extend(masslinie(12, oben, 12, oben + a, a))
    inhalt.extend(masslinie(12, oben - d, 12, oben, d))
    inhalt.extend(masslinie(17, unten + 8, w - 17, unten + 8, gesamt))
    for x, farbe, strich, name in (
        (22, SCHNITT, None, "Schnitt"),
        (58, FALZ, falzstrich, falzname),
        (143, KLEBUNG, "0.7 0.8", "Klebefläche"),
    ):
        attrs = {"stroke_dasharray": strich} if strich else {}
        inhalt.append(linie(x, unten + 17, x + 10, unten + 17, stroke=farbe, stroke_width=0.3, **attrs))
        inhalt.append(text(x + 12, unten + 18, name, fill=MASS, font_size=3))
    inhalt.extend(masslinie(22, unten + 27, 72, unten + 27, 50))
    inhalt.append(text(76, unten + 28, "Kontrollmass", fill=MASS, font_size=3))
    inhalt.append(text(143, unten + 28, f"Lasche {mm(lasche)}", fill=MASS, font_size=3))
    if einlage:
        rand = (a - 8 * FELD) / 2
        inhalt.append(text(22, unten + 36, f"Lochmitten: Raster {mm(FELD)}; Abstand zur nächsten Rillachse am Rand {mm(rand + FELD / 2)}.",
                           fill=MASS, font_size=3))
        inhalt.append(text(22, unten + 43, f"Reihenmitten ab oberer Rille: {', '.join(mm(rand + (n + 0.5) * FELD) for n in (0, 1, 6, 7))}.",
                           fill=MASS, font_size=3))
        inhalt.append(text(22, unten + 50, "Loch-Ø: " + " · ".join(f"{figur} {mm(fuss + LOCHZUGABE)}"
                           for figur, (_, fuss) in FIGUREN.items()), fill=MASS, font_size=3))
    return svg(w, h, inhalt)


def felder():
    for reihe in range(8):
        for spalte in range(8):
            yield spalte * FELD, reihe * FELD, CREME if (reihe + spalte) % 2 == 0 else BRAUN


def brettgrafik(brett, kante, anschnitt=0):
    w = kante + 2 * anschnitt
    rand = (kante - brett) / 2
    start = anschnitt + rand
    links = anschnitt + rand / 2
    unten = anschnitt + kante - rand / 2
    schrift = min(3.4, rand * 0.65)
    basis = schrift * 0.35
    attrs = dict(fill=BRAUN, font_size=schrift, text_anchor="middle", font_weight="bold")
    inhalt = [element("rect", x=0, y=0, width=w, height=w, fill=BRETTRAND)]
    inhalt.extend(element("rect", x=start + x, y=start + y, width=FELD, height=FELD, fill=farbe)
                  for x, y, farbe in felder())
    for i, spalte in enumerate("abcdefgh"):
        mitte = start + (i + 0.5) * FELD
        inhalt.append(text(mitte, unten + basis, spalte, **attrs))
        inhalt.append(text(links, mitte + basis, str(8 - i), **attrs))
    return inhalt


def vorschau(brett, boden, deckel, einlage, hoehe):
    teile = [element("rect", x=0, y=0, width=1120, height=805, fill=WEISS)]

    def titel(x, y, beschriftung, groesse=20):
        teile.append(text(x, y, beschriftung, fill=BRAUN, font_size=groesse, font_weight="bold"))

    def info(x, y, beschriftung):
        teile.append(text(x, y, beschriftung, fill=BRAUN, font_size=15))

    def projektion(ox, oy, faktor):
        return lambda x, y, z: (ox + faktor * (x - 0.68 * y), oy + faktor * (0.26 * x + 0.38 * y - z))

    def polygon(proj, punkte, farbe, **attrs):
        teile.append(flaeche([proj(*p) for p in punkte], fill=farbe, **attrs))

    def ebene(proj, x, y, seite, z, farbe):
        polygon(proj, [(x, y, z), (x + seite, y, z), (x + seite, y + seite, z), (x, y + seite, z)], farbe)

    def wand(proj, start, ende, oben, unten, farbe):
        polygon(proj, [(*start, oben), (*ende, oben), (*ende, unten), (*start, unten)], farbe,
                stroke=BRAUN, stroke_width=0.6)

    titel(56, 70, "Schachschokolade", 38)
    info(58, 99, "Entwurf für 32 Figuren in zwei Farben")
    teile.append(linie(56, 122, 1064, 122, stroke="#b8a28f", stroke_width=1))
    titel(58, 162, "01   Deckel aussen")
    titel(586, 162, "02   Unterteil mit Einlage")
    p = projektion(246, 220, 0.96)
    wand(p, (0, deckel), (deckel, deckel), 0, -DECKELTIEFE, "#c5ab93")
    wand(p, (deckel, 0), (deckel, deckel), 0, -DECKELTIEFE, "#b89c84")
    ebene(p, 0, 0, deckel, 0, "#e0cbb7")
    p = projektion(780, 270, 0.96)
    ebene(p, 0, 0, boden, 0, "#b0957f")
    wand(p, (0, 0), (boden, 0), hoehe, 0, "#bc9e85")
    wand(p, (0, 0), (0, boden), hoehe, 0, "#ab8d77")
    offset = (boden - einlage) / 2
    ebene(p, offset, offset, einlage, EINLAGENHOEHE, CREME)
    # Vorderwände links und rechts sind zur Sicht auf die Einlage ausgeblendet.
    for _, _, x, y, d in loecher(einlage):
        px, py = p(x + offset, y + offset, EINLAGENHOEHE)
        teile.append(element("ellipse", cx=px, cy=py, rx=d * 0.54, ry=d * 0.20, fill="#a98b74"))
    teile.append(linie(*p(0, boden, hoehe), *p(boden, boden, hoehe), stroke="#a08470",
                       stroke_width=1, stroke_dasharray="5 5"))
    teile.append(linie(*p(boden, 0, hoehe), *p(boden, boden, hoehe), stroke="#a08470",
                       stroke_width=1, stroke_dasharray="5 5"))
    info(58, 450, "Aussenseite bleibt unbedruckt")
    info(586, 450, "Vordere Wände zur Ansicht ausgeblendet")
    teile.append(linie(56, 480, 1064, 480, stroke="#b8a28f", stroke_width=1))
    titel(58, 522, "03   Schachbrett im Deckel")
    teile.append(element("rect", x=58, y=552, width=217, height=217, fill="#b89c84"))
    teile.append(f'<g transform="translate(64 558) scale({zahl(205 / deckel)})">')
    teile.extend(brettgrafik(brett, deckel))
    teile.append("</g>")
    info(295, 637, "Deckel wenden und spielen")
    info(295, 661, f"Spielfeld {mm(brett)} × {mm(brett)} mm")
    titel(586, 522, "04   Erhöhte Einlage")
    k = 205 / einlage
    teile.append(element("rect", x=588, y=553, width=205, height=205, fill=CREME,
                         stroke="#9e7d65", stroke_width=1))
    for farbe, _, x, y, d in loecher(einlage):
        teile.append(element("circle", cx=588 + x * k, cy=553 + y * k, r=d * k / 2,
                             fill=BRAUN if farbe == "dunkel" else WEISS, stroke="#876551", stroke_width=1))
    info(816, 578, "16 dunkle Figuren")
    info(816, 652, f"{mm(EINLAGENHOEHE)} mm über dem Boden")
    info(816, 676, "Mitte frei für eine Einlegekarte")
    info(816, 746, "16 weisse Figuren")
    return svg(1120, 805, teile, raster=True)


def schreibe_svg(pfad, inhalt):
    pfad.write_text(inhalt, encoding="utf-8")


def pdf_blatt(inhalt):
    return PdfReader(BytesIO(cairosvg.svg2pdf(bytestring=inhalt.encode("utf-8")))).pages[0]


def generieren(ziel):
    pruefe_masse()
    ziel.mkdir(exist_ok=True)
    brett, boden, deckel, einlage, hoehe = masse()
    blaetter = (
        ("unterteil", dieline("01  Unterteil", boden, hoehe)),
        ("deckel", dieline("02  Stülpdeckel", deckel, DECKELTIEFE)),
        ("einlage", dieline("03  Erhöhte Einlage", einlage, EINLAGENHOEHE, einlage=True)),
    )
    sammlung = PdfWriter()
    for name, inhalt in blaetter:
        schreibe_svg(ziel / f"{name}.svg", inhalt)
        sammlung.add_page(pdf_blatt(inhalt))
    sammlung.write(ziel / "falzmuster.pdf")

    format_mit_anschnitt = deckel + 2 * ANSCHNITT
    druck = svg(format_mit_anschnitt, format_mit_anschnitt, brettgrafik(brett, deckel, ANSCHNITT))
    schreibe_svg(ziel / "brettdruck.svg", druck)
    blatt = pdf_blatt(druck)
    pts = 72 / 25.4
    anschnitt = ANSCHNITT * pts
    blatt.trimbox = RectangleObject((anschnitt, anschnitt, (deckel + ANSCHNITT) * pts,
                                    (deckel + ANSCHNITT) * pts))
    blatt.bleedbox = blatt.mediabox
    druck_pdf = PdfWriter()
    druck_pdf.add_page(blatt)
    druck_pdf.write(ziel / "brettdruck.pdf")
    grafik = vorschau(brett, boden, deckel, einlage, hoehe)
    cairosvg.svg2png(bytestring=grafik.encode("utf-8"), write_to=str(ziel / "vorschau.png"),
                     output_width=1680, output_height=1208)


if __name__ == "__main__":
    generieren(Path(__file__).resolve().parent / "vorlagen")
