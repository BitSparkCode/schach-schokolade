"""Erzeugt die Druckaufträge für Bambu Studio als 3MF in druck/.

python3 cad/druckplatte.py   (zuerst python3 cad/bauen.py)
Ein Auftrag ist eine P2S-Druckplatte. Einzelteile werden mit Abstand
nebeneinander gelegt. Mehrfarbige Teile (AMS) bleiben zueinander ausgerichtet.
"""
import pathlib
import zipfile

import trimesh

WURZEL = pathlib.Path(__file__).resolve().parent.parent
STL = WURZEL / "stl"
DRUCK = WURZEL / "druck"
PLATTE = 256.0
ABSTAND = 12.0

# (Datei, Teile, mehrfarbig). Mehrfarbig: Teile behalten ihre Lage zueinander.
AUFTRAEGE = [
    ("01_probeform.3mf", ["form_probe/trichterplatte", "form_probe/platte_1", "form_probe/platte_2"], False),
    ("02_vollsatz_formplatten.3mf", "form_vollsatz/platte_*", False),
    ("03_vollsatz_trichter.3mf", ["form_vollsatz/trichterplatte"], False),
    ("04_box_unterteil.3mf", ["box/unterteil", "box/unterteil_beschriftung"], True),
    ("05_box_einlage.3mf", ["box/einlage"], False),
    ("06_box_deckel.3mf", ["box/deckel", "box/deckel_felder_dunkel"], True),
]


def _mitte_auf_platte(netze, y=None):
    unten = trimesh.util.concatenate(netze).bounds[0]
    breite, tiefe = trimesh.util.concatenate(netze).extents[:2]
    y = (PLATTE - tiefe) / 2 if y is None else y
    verschiebung = [(PLATTE - breite) / 2 - unten[0], y - unten[1], -unten[2]]
    for m in netze:
        m.apply_translation(verschiebung)


def _platten(muster):
    return [str(p.relative_to(STL).with_suffix("")) for p in
            sorted(STL.glob(f"{muster}.stl"), key=lambda p: int(p.stem.rsplit("_", 1)[1]))]


def _objekt(nr, name, m):
    ecken = "".join(f'<vertex x="{x:.4f}" y="{y:.4f}" z="{z:.4f}"/>' for x, y, z in m.vertices)
    flaechen = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in m.faces)
    return (f'<object id="{nr}" type="model" name="{name}"><mesh><vertices>{ecken}</vertices>'
            f'<triangles>{flaechen}</triangles></mesh></object>')


def schreibe_3mf(ziel, namen, netze, mehrfarbig):
    """Mehrfarbig: ein Objekt aus Teilen (components), sonst ein Objekt pro Teil."""
    objekte = [_objekt(i + 1, n, m) for i, (n, m) in enumerate(zip(namen, netze))]
    if mehrfarbig:
        nr = len(netze) + 1
        teile = "".join(f'<component objectid="{i + 1}"/>' for i in range(len(netze)))
        objekte.append(f'<object id="{nr}" type="model" name="{namen[0]}"><components>{teile}</components></object>')
        aufbau = f'<item objectid="{nr}"/>'
    else:
        aufbau = "".join(f'<item objectid="{i + 1}"/>' for i in range(len(netze)))
    modell = ('<?xml version="1.0" encoding="UTF-8"?>'
              '<model unit="millimeter" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
              f'<resources>{"".join(objekte)}</resources><build>{aufbau}</build></model>')
    typen = ('<?xml version="1.0" encoding="UTF-8"?>'
             '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
             '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
             '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>'
             '</Types>')
    bezug = ('<?xml version="1.0" encoding="UTF-8"?>'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Target="/3D/3dmodel.model" Id="rel0" '
             'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    with zipfile.ZipFile(ziel, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", typen)
        z.writestr("_rels/.rels", bezug)
        z.writestr("3D/3dmodel.model", modell)


def auftrag(datei, teile, mehrfarbig):
    if isinstance(teile, str):
        teile = _platten(teile)
    netze = [trimesh.load(STL / f"{t}.stl") for t in teile]
    if mehrfarbig:
        _mitte_auf_platte(netze)
        tiefe = netze[0].extents[1]
    else:
        tiefe = sum(m.extents[1] for m in netze) + ABSTAND * (len(netze) - 1)
        y = (PLATTE - tiefe) / 2
        for m in netze:
            _mitte_auf_platte([m], y)
            y += m.extents[1] + ABSTAND
    breite = max(m.extents[0] for m in netze)
    if max(tiefe, breite) > PLATTE:
        raise SystemExit(f"{datei}: passt nicht auf eine Druckplatte ({breite:.0f} × {tiefe:.0f} mm)")
    ziel = DRUCK / datei
    schreibe_3mf(ziel, [pathlib.Path(t).stem for t in teile], netze, mehrfarbig)
    return ziel


if __name__ == "__main__":
    DRUCK.mkdir(exist_ok=True)
    for alt in DRUCK.glob("*.3mf"):
        alt.unlink()
    for a in AUFTRAEGE:
        print(auftrag(*a))
