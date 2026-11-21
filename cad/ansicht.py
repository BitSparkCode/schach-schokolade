"""Renderings mit three.js im Browser (Chrome per CDP): python3 cad/ansicht.py"""
import functools
import http.server
import json
import pathlib
import threading
import urllib.parse

from playwright.sync_api import sync_playwright

import box
import form

WURZEL = pathlib.Path(__file__).resolve().parent.parent
# Schokolade dunkel und weiss, Filament PLA Pure White, Apricot, Black
DUNKEL, WEISS, PLA, APRIKOSE, SCHWARZ = "#4a2c22", "#efe6d6", "#f4f2ee", "#f0b98d", "#262626"


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
    return sz


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


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
