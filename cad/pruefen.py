"""Prüfungen für die starre Form.

1. Hinterschnitte: Jede Formhälfte muss senkrecht zur Trennebene (±Y) abheben.
   Fläche bei y > 0 darf nicht gegen -Y zeigen, und umgekehrt.
2. Steilheit: In Giesslage (Kopf unten) darf keine Formdecke flacher als 45°
   sein. Aufrecht heisst das: keine nach unten zeigende Fläche flacher als 45°,
   ausser der Standfläche. Gilt zugleich als Druckregel ohne Stützmaterial.
3. Luftfallen: In Giesslage kein lokaler Hochpunkt der Figur unterhalb der
   Giessebene.
"""
import numpy as np

STEIL = np.cos(np.radians(45.0)) + 0.02
TOLERANZ = 0.02


def hinterschnitte(netz, rand=0.3):
    c, n, a = netz.triangles_center, netz.face_normals, netz.area_faces
    schlecht = ((c[:, 1] > rand) & (n[:, 1] < -TOLERANZ)) | ((c[:, 1] < -rand) & (n[:, 1] > TOLERANZ))
    return float(a[schlecht].sum())


def zu_flach(netz, stand=1.0):
    c, n, a = netz.triangles_center, netz.face_normals, netz.area_faces
    schlecht = (c[:, 2] > stand) & (n[:, 2] < -STEIL)
    return float(a[schlecht].sum())


def luftfallen(netz, hoehe, stand=1.0):
    """Giesslage: z' = hoehe - z. Hochpunkt in Giesslage = Tiefpunkt aufrecht."""
    z = netz.vertices[:, 2]
    fallen = []
    for i, nachbarn in enumerate(netz.vertex_neighbors):
        if z[i] <= stand or not nachbarn:
            continue
        if np.all(z[nachbarn] > z[i] + 1e-4):
            fallen.append(netz.vertices[i])
    return fallen


def bericht(name, netz, hoehe):
    return {
        "figur": name,
        "hinterschnitt_mm2": round(hinterschnitte(netz), 2),
        "zu_flach_mm2": round(zu_flach(netz), 2),
        "luftfallen": len(luftfallen(netz, hoehe)),
        "volumen_cm3": round(netz.volume / 1000, 2),
    }
