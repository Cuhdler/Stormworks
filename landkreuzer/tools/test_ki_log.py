"""Pruefstand Fahrtenschreiber der KI von vorn bis hinten: der ganze KI-Chip (chip_sim, Schreiber Port 8768) faehrt
eine Minute mit einem Wegpunkt; die Pakete des Status-Skripts werden wie in tools/waffen_logger.py zu ki.csv
zusammengesetzt und mit ki_log.py ausgewertet.
Aufruf (mit lupa): python landkreuzer/tools/test_ki_log.py
"""
import math
import os
import sys
import tempfile
import urllib.parse

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HIER)), "tools"))
import build_ki  # noqa: E402
import ki_log  # noqa: E402
from chip_sim import ChipSim  # noqa: E402
from schreiber_spalten import spalten  # noqa: E402


def fahrt(sek=60):
    pr = build_ki.props_mit(**{"Schreiber Port": 8768, "Start Verzoegerung s": 10})
    sim = ChipSim(build_ki.build(eigen=pr))
    quelle = build_ki.lua("ki_status")
    cid = next(c for c, (typ, *r) in sim.comps.items() if typ == 56 and r[3]["script"] == quelle)
    g, _ = sim.lua[cid]
    zeilen, antwort = [], []

    def http(port, url):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        zeilen.extend(q.get("d", [""])[0].split(";"))
        antwort.append((port, url))                  # die Antwort kommt im Spiel spaeter (hier: naechster Tick)
    g["async"].httpGet = http
    x, z, hd, v, rl, rr = 500.0, 300.0, 0.0, 0.0, 0.0, 0.0
    for t in range(int(sek * 60)):
        while antwort:
            g.httpReply(*antwort.pop(0), "ok")
        L, R = rl, -rr
        v += ((L + R) / 2 * 10 - v) * 0.02
        hd += (L - R) * 0.02 / 60
        x += v * math.sin(hd * 2 * math.pi) / 60
        z += v * math.cos(hd * 2 * math.pi) / 60
        phys = ({1: x, 2: 40.0, 3: z, 9: v, 13: abs(v), 15: 0.01, 16: -0.005, 17: -hd}, {})
        las = {n: 4000.0 for n in build_ki.LASER_NAMEN}
        las["Laser unten"] = 1.6
        tn, tb = {1: 96.0, 2: 96.0}, {}
        if 700 <= t < 703:
            tn.update({3: 80.0, 4: 20.0})
            tb[1] = True
        e = {"Physik-Sensor": phys, "Sitz": ({}, {}), "Instrumente": ({}, {}), "Bedienung": ({}, {}),
             "Karte Touch": (tn, tb), "Batterie": 0.9 - t * 0.0000025}
        e.update(las)
        a = sim.tick(e)
        rl, rr = a.get("Links") or 0.0, a.get("Rechts") or 0.0
    return zeilen, (x, z)


def main():
    zeilen, ende = fahrt()
    sp = spalten("ki")
    ordner = tempfile.mkdtemp(prefix="ki_log_")
    with open(os.path.join(ordner, "ki.csv"), "w", encoding="utf-8") as f:
        f.write("tick," + ",".join(sp) + "\n")
        for z in zeilen:
            if z:
                f.write(z + "\n")
    rueck = []
    daten = ki_log.lade(ordner, "ki")
    rueck.append(("%d Zeilen im Log (je Tick eine, %d Spalten)" % (len(daten), len(daten[0]) if daten else 0),
                  len(daten) > 3000 and len(daten[0]) == len(sp) + 1))
    text = ki_log.zusammenfassung(daten)
    for t in text:
        print("   ", t)
    gef = float(text[0].split("gefahren ")[1].split(" m")[0])
    rueck.append(("Strecke im Log %.0f m, Ende bei (%.0f, %.0f) wie gefahren (%.0f, %.0f)" % (
        gef, daten[-1]["x"], daten[-1]["z"], ende[0], ende[1]),
        gef > 50 and abs(daten[-1]["x"] - ende[0]) < 5 and abs(daten[-1]["z"] - ende[1]) < 5))
    rueck.append(("Batterie-Verbrauch erkannt (0,9 %% je Minute)", any("0.90 % je Minute" in t for t in text)))
    try:
        b = ki_log.bild(daten, os.path.join(ordner, "ki_auswertung.png"))
        rueck.append(("Bild gezeichnet (%s)" % os.path.basename(b), os.path.getsize(b) > 10000))
    except ImportError:
        pass
    ok = True
    for t, g in rueck:
        print("%-90s %s" % (t, "ok" if g else "FEHLER"))
        ok &= bool(g)
    print("ALLES OK" if ok else "FEHLER")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
