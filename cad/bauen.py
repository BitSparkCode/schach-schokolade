"""Erzeugt alle STL-Dateien in Drucklage und stl/masse.json (lokal, nicht im Repo): python3 cad/bauen.py

Drucklage: Formplatten stehend in Giesslage (Giessebene oben). Trichterplatte,
Einlage und Deckel liegen umgedreht, Sichtfläche auf dem Druckbett.
"""
import json
import pathlib

import cadquery as cq
import trimesh

import box
import figuren
import form
import netz
import pruefen

WURZEL = pathlib.Path(__file__).resolve().parent.parent
STL = WURZEL / "stl"
BAURAUM = 256.0


def umgedreht(koerper, oben):
    """180° um X, Oberkante oben liegt danach auf z = 0."""
    return koerper.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, oben))


def export(koerper, pfad):
    pfad.parent.mkdir(parents=True, exist_ok=True)
    m = netz.zu_netz(koerper)
    m.merge_vertices(digits_vertex=4)
    trimesh.repair.fill_holes(m)
    trimesh.repair.fix_normals(m)
    m.export(str(pfad))
    groesse = [round(float(v), 1) for v in m.extents]
    return {"datei": str(pfad.relative_to(WURZEL)), "mm": groesse, "volumen_cm3": round(float(m.volume) / 1000, 1),
            "wasserdicht": bool(m.is_watertight), "passt_p2s": max(groesse) <= BAURAUM}


def figuren_bauen():
    berichte = []
    for k, f in figuren.SET.items():
        koerper = figuren.figur(k)
        info = export(koerper, STL / "figuren" / f"{k}.stl")
        info.update(pruefen.bericht(k, netz.zu_netz(koerper), f.hoehe))
        berichte.append(info)
    return berichte


def form_bauen(name, reihen):
    f = form.Form(reihen)
    teile = [export(p, STL / f"form_{name}" / f"{n}.stl") for n, p in f.platten()]
    oben = f.hoehe + f.m.trichter_hoehe
    mitte = (f.grenzen[0] + f.grenzen[-1]) / 2
    trichter = f.trichterplatte().translate((0, -mitte, 0))
    teile.append(export(umgedreht(trichter, oben), STL / f"form_{name}" / "trichterplatte.stl"))
    return {"form": name, "aussen_mm": [f.breite, round(f.tiefe, 1), f.hoehe],
            "plattendicken_mm": [round(b - a, 1) for a, b in zip(f.grenzen, f.grenzen[1:])],
            "trichter_versatz_y": round(mitte, 2), "teile": teile}


def box_bauen():
    b = box.Box()
    oben_deckel = b.m.deckel_schuerze + b.m.deckel_decke
    teile = [
        export(b.unterteil(), STL / "box" / "unterteil.stl"),
        export(b.beschriftung(), STL / "box" / "unterteil_beschriftung.stl"),
        export(umgedreht(b.einlage(), b.m.einlage_hoehe), STL / "box" / "einlage.stl"),
        export(umgedreht(b.deckel(), oben_deckel), STL / "box" / "deckel.stl"),
        export(umgedreht(b.deckel_felder(), oben_deckel), STL / "box" / "deckel_felder_dunkel.stl"),
    ]
    return {"deckel_aussen_mm": b.m.deckel_aussen, "unterteil_aussen_mm": round(b.unterteil_aussen, 1),
            "innen_mm": round(b.innen, 1), "innen_hoehe_mm": b.innen_hoehe, "unterteil_hoehe_mm": b.unterteil_hoehe,
            "box_hoehe_mm": round(b.unterteil_hoehe + b.m.deckel_decke, 1), "teile": teile}


if __name__ == "__main__":
    ergebnis = {"figuren": figuren_bauen(),
                "formen": [form_bauen("probe", form.PROBE), form_bauen("vollsatz", form.VOLLSATZ)],
                "box": box_bauen()}
    (STL / "masse.json").write_text(json.dumps(ergebnis, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(ergebnis, indent=1, ensure_ascii=False))
