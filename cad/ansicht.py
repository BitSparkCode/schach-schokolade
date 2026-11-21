"""Renderings mit three.js im Browser (Chrome per CDP): python3 cad/ansicht.py"""
import functools
import http.server
import json
import pathlib
import threading
import urllib.parse

from playwright.sync_api import sync_playwright

import trimesh

import box
import druckplatte
import form

WURZEL = pathlib.Path(__file__).resolve().parent.parent
# Schokolade dunkel und weiss, Filament PLA Pure White, Apricot, Black
DUNKEL, WEISS, PLA, APRIKOSE, SCHWARZ = "#4a2c22", "#efe6d6", "#f4f2ee", "#f0b98d", "#262626"
BETT = "#5a5a5a"


def szenen():
    sz = {}
    namen = ["koenig", "dame", "laeufer", "springer", "turm", "bauer"]
    sz["figuren"] = dict(azim=-90, elev=12, abstand=1.25, teile=[
        dict(stl=f"/stl/figuren/{n}.stl", farbe=DUNKEL if i % 2 == 0 else WEISS, pos=[i * 32, 0, 0]) for i, n in enumerate(namen)])
    for name, reihen in (("probe", form.PROBE), ("vollsatz", form.VOLLSATZ)):
        f = form.Form(reihen)
        n = len(f.grenzen) - 1
        teile = [dict(stl=f"/stl/form_{name}/platte_{i + 1}.stl", farbe=PLA, pos=[0, 22 * i, 0]) for i in range(n)]
        oben = f.hoehe + f.m.trichter_hoehe
        mitte = (f.grenzen[0] + f.grenzen[-1]) / 2
        teile.append(dict(stl=f"/stl/form_{name}/trichterplatte.stl", farbe=PLA, rot=[180, 0, 0], pos=[0, 11 * (n - 1) + mitte, oben + 30]))
        sz[f"form_{name}"] = dict(azim=-60, elev=38, abstand=1.5, teile=teile)
        zu = [dict(stl=f"/stl/form_{name}/platte_{i + 1}.stl", farbe=PLA) for i in range(n)]
        sz[f"form_{name}_geschlossen"] = dict(azim=-60, elev=28, abstand=1.7, teile=zu + [
            dict(stl=f"/stl/form_{name}/trichterplatte.stl", farbe="#cfe3e8", rot=[180, 0, 0], pos=[0, mitte, oben])])
    b = box.Box()
    figs = [dict(stl=f"/stl/figuren/{k}.stl", farbe=DUNKEL if c == "dunkel" else WEISS, pos=[x, y, b.m.boden],
                 rot=[0, 0, 90 if y > 0 else -90] if k == "springer" else [0, 0, 0]) for k, x, y, c in b.positionen()]
    sz["box_gefuellt"] = dict(azim=-70, elev=42, abstand=1.35, teile=[
        dict(stl="/stl/box/unterteil.stl", farbe=APRIKOSE), dict(stl="/stl/box/einlage.stl", farbe=PLA, rot=[180, 0, 0], pos=[0, 0, b.m.boden + b.m.einlage_hoehe])] + figs)
    oben = b.m.deckel_schuerze + b.m.deckel_decke
    deckel = [dict(stl="/stl/box/deckel.stl", farbe=PLA, rot=[180, 0, 0], pos=[0, 0, oben]),
              dict(stl="/stl/box/deckel_felder_dunkel.stl", farbe=SCHWARZ, rot=[180, 0, 0], pos=[0, 0, oben])]
    sz["box_deckel"] = dict(azim=-60, elev=40, abstand=1.5, teile=deckel)
    sz["box_unten"] = dict(azim=-90, elev=-70, abstand=1.3, teile=[
        dict(stl="/stl/box/unterteil.stl", farbe=APRIKOSE), dict(stl="/stl/box/unterteil_beschriftung.stl", farbe=SCHWARZ)])
    sz["box_geschlossen"] = dict(azim=-60, elev=30, abstand=1.6, teile=[
        dict(stl="/stl/box/unterteil.stl", farbe=APRIKOSE),
        *[dict(t, pos=[0, 0, b.unterteil_hoehe + b.m.deckel_decke]) for t in deckel]])
    platte3 = "/stl/form_vollsatz/platte_3.stl"
    v = form.Form(form.VOLLSATZ)
    (xl, zl), _ = v.noppen()
    sz["form_platte_noppen"] = dict(azim=-40, elev=15, abstand=1.5, teile=[dict(stl=platte3, farbe=PLA)])
    sz["form_platte_aufnahmen"] = dict(azim=140, elev=15, abstand=1.5, teile=[dict(stl="/stl/form_vollsatz/platte_2.stl", farbe=PLA)])
    sz["form_noppen_detail"] = dict(azim=-160, elev=12, d=60, abstand=1, ziel=[xl, v.ebenen[1] - 1.5, zl],
                                    teile=[dict(stl=platte3, farbe=PLA)])
    for datei, teile, mehrfarbig in druckplatte.AUFTRAEGE:
        namen, netze = druckplatte.anordnen(datei, teile, mehrfarbig)
        bett = [dict(quader=[druckplatte.PLATTE, druckplatte.PLATTE, 2], farbe=BETT, pos=[druckplatte.PLATTE / 2, druckplatte.PLATTE / 2, -1])]
        for n, m in zip(namen, netze):
            pos = (m.bounds[0] - trimesh.load(druckplatte.STL / f"{n}.stl").bounds[0]).tolist()
            bett.append(dict(stl=f"/stl/{n}.stl", farbe=druckfarbe(n), pos=pos))
        sz["druck_" + datei.removesuffix(".3mf")] = dict(azim=-90, elev=40, abstand=1.35, teile=bett)
    return sz


def schnitt_noppen():
    """Schnitt durch die linke Noppe der Buchform, Platten 1 bis 3, geschlossen."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    v = form.Form(form.VOLLSATZ)
    (xl, zl), _ = v.noppen()
    fig, ax = plt.subplots(figsize=(7, 6))
    for i, farbe in [(1, "#555555"), (2, "#d9822b"), (3, "#3b6ea5")]:
        m = trimesh.load(druckplatte.STL / "form_vollsatz" / f"platte_{i}.stl")
        for linie in m.section(plane_origin=[0, 0, zl], plane_normal=[0, 0, 1]).discrete:
            ax.plot(linie[:, 0], linie[:, 1], color=farbe, lw=1.4)
        ax.plot([], [], color=farbe, label=f"Platte {i}")
    ax.set_xlim(xl - 9, xl + 15)
    ax.set_ylim(v.grenzen[0] - 1, v.grenzen[3] + 4)
    ax.set_aspect("equal")
    ax.set_xlabel("x in mm")
    ax.set_ylabel("y in mm")
    ax.set_title(f"Kegelnoppen geschlossen, Schnitt auf z = {zl:.0f} mm")
    ax.legend(loc="lower right")
    fig.savefig(WURZEL / "bilder" / "form_noppen_schnitt.png", dpi=150, bbox_inches="tight")


def druckfarbe(teil):
    if teil.endswith(("beschriftung", "felder_dunkel")):
        return SCHWARZ
    return APRIKOSE if teil == "box/unterteil" else PLA


def main(nur=None):
    class Leise(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Leise, directory=str(WURZEL))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    port = server.server_address[1]
    (WURZEL / "bilder").mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:29229")
        seite = browser.contexts[0].new_page()
        seite.set_viewport_size({"width": 1400, "height": 900})
        for name, sz in szenen().items():
            if nur and name not in nur:
                continue
            seite.goto(f"http://127.0.0.1:{port}/cad/ansicht.html?n=" + name + "#" + urllib.parse.quote(json.dumps(sz)))
            seite.wait_for_function("document.title === 'fertig'", timeout=120000)
            seite.locator("canvas").screenshot(path=str(WURZEL / "bilder" / f"{name}.png"))
            print(name)
        seite.close()
    server.shutdown()
    if not nur or "form_noppen_schnitt" in nur:
        schnitt_noppen()
        print("form_noppen_schnitt")


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
