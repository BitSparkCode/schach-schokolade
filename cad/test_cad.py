"""Prüfungen ohne Zusatzpakete: python3 cad/test_cad.py"""
import box
import figuren
import form
import netz
import pruefen

BAURAUM = 256.0


def test_figuren():
    for k, f in figuren.SET.items():
        koerper = figuren.figur(k).val()
        assert koerper.isValid(), k
        bb = koerper.BoundingBox()
        assert abs(bb.zlen - f.hoehe) < 0.1, (k, bb.zlen)
        assert abs(max(bb.xlen, bb.ylen) - f.fuss_d) < 0.1, (k, bb.xlen, bb.ylen)
        b = pruefen.bericht(k, netz.zu_netz(koerper), f.hoehe)
        assert b["hinterschnitt_mm2"] < 1.0, b
        assert b["zu_flach_mm2"] < 1.0, b
        assert b["luftfallen"] == 0, b
    assert sum(f.anzahl for f in figuren.SET.values()) == 16


def test_form(reihen):
    f = form.Form(reihen)
    assert sum(len(r) for r in reihen) == len(f.kavitaeten())
    platten = f.platten()
    assert len(platten) == len(reihen) + 1
    for n, p in platten:
        bb = p.val().BoundingBox()
        assert p.val().isValid(), n
        assert max(bb.xlen, bb.ylen, bb.zlen) <= BAURAUM, n
    for k, x, y, _ in f.kavitaeten():
        assert abs(y) in [abs(e) for e in f.ebenen], k
    bb = f.trichterplatte().val().BoundingBox()
    assert max(bb.xlen, bb.ylen) <= BAURAUM


def test_box():
    b = box.Box()
    assert b.innen_hoehe >= max(f.hoehe for f in figuren.SET.values()) + 2
    pos = b.positionen()
    assert len(pos) == 32
    for k, x, y, _ in pos:
        r = (figuren.SET[k].fuss_d + b.m.loch_spiel) / 2 + b.m.rohr_wand
        assert abs(x) + r < b.innen / 2 - b.m.einlage_spiel, k
        assert abs(y) + r < b.innen / 2 - b.m.einlage_spiel, k
    abstand = b.m.raster - max(figuren.SET[k].fuss_d for k in figuren.SET) - b.m.loch_spiel
    assert abstand > 0
    for name in ["unterteil", "einlage", "deckel", "deckel_felder", "beschriftung"]:
        teil = getattr(b, name)().val()
        bb = teil.BoundingBox()
        assert max(bb.xlen, bb.ylen, bb.zlen) <= BAURAUM, name
    assert b.unterteil().val().isValid() and b.deckel().val().isValid() and b.einlage().val().isValid()
    assert b.deckel().val().BoundingBox().xlen == b.m.deckel_aussen


if __name__ == "__main__":
    test_figuren(); print("figuren ok")
    test_form(form.PROBE); print("probeform ok")
    test_box(); print("box ok")
    test_form(form.VOLLSATZ); print("buchform ok")
