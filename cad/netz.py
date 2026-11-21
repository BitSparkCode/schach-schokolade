"""CadQuery-Körper zu trimesh-Netz."""
import os
import tempfile

import cadquery as cq
import trimesh


def zu_netz(koerper, toleranz=0.02, winkel=0.1):
    with tempfile.TemporaryDirectory() as ordner:
        pfad = os.path.join(ordner, "teil.stl")
        cq.exporters.export(koerper, pfad, tolerance=toleranz, angularTolerance=winkel)
        return trimesh.load(pfad)
