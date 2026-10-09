"""Pruefstand: Lagezentrale + Bildschirm-Chip des Landkreuzers an Land (mit dem Pruefstand der Figet Marena,
tools/test_lage.py). Der Panzer steht 100 m ueber dem Meer; Ziele: zwei fahrende Bodenfahrzeuge, ein Hubschrauber,
ein tief fliegender Jet, ein stehendes Gebaeude.

Erwartung mit den Land-Aenderungen (bau_landkreuzer.land_lua, LAGE_LAND):
- die Kanonen (BC, AC) nehmen nur die fahrenden Bodenfahrzeuge, nie das Gebaeude, nie Luftziele
- die Flaks nehmen nur Luftziele
Zum Vergleich laeuft dieselbe Szene mit den unveraenderten Schiffs-Skripten (dort gilt alles ueber 120 m ueber dem
Meer als Luftziel - die Bodenfahrzeuge auf 100 m wuerden falsch eingeordnet).

Aufruf (mit lupa): python landkreuzer/tools/test_land_lage.py
"""
import math
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HIER))
sys.path.insert(0, HIER)
import build_mc  # noqa: E402

sys.modules["build_mc"] = build_mc
sys.path.insert(1, os.path.join(ROOT, "tools"))
os.environ.setdefault("APPDATA", "/tmp/kein_appdata")
import sperrprofil  # noqa: E402

_k = sperrprofil.koerper
sperrprofil.koerper = lambda pfad=os.path.join(ROOT, "fahrzeug", "Figet Marena.xml"): _k(pfad)
import test_lage  # noqa: E402
import bau_landkreuzer as B  # noqa: E402

HOEHE = 100.0


def szene(land, sek=90):
    if land:
        quellen = B.land_lua()
        alt = test_lage.quelle
        test_lage.quelle = lambda n: quellen[n] if n in quellen else alt(n)
        pr = dict(test_lage.PR)
        pr.update(B.LAGE_LAND)
    else:
        pr = dict(test_lage.PR)
    hd = 30
    b = lambda brg, r, h: (r * math.sin(math.radians(brg + hd)), r * math.cos(math.radians(brg + hd)), h)
    w = lambda brg, v: (v * math.sin(math.radians(brg + hd)), v * math.cos(math.radians(brg + hd)), 0.0)
    ziele = [(b(20, 900, HOEHE + 4), w(100, 8)),          # 0 Bodenfahrzeug, faehrt quer
             (b(-60, 1500, HOEHE - 6), w(200, 6)),        # 1 Bodenfahrzeug
             (b(120, 700, HOEHE + 130), w(0, 3)),          # 2 Hubschrauber (130 m ueber uns)
             (b(200, 2500, HOEHE + 60), w(90, 120)),       # 3 Jet tief (60 m ueber uns)
             (b(60, 400, HOEHE + 8), (0, 0, 0))]           # 4 Gebaeude, steht
    L = test_lage.Lage(ziele, own=(0, 0, 0), hdg=hd, roll=1.0, nick=1.0, props=pr, behalten=True, frisch=True)
    L.S = [0.0, 0.0, HOEHE]
    if land:
        test_lage.quelle = alt
    zaehl = {"kan_boden": 0, "kan_falsch": 0, "flak_luft": 0, "flak_falsch": 0, "n": 0}
    for _ in range(int(sek * 4)):
        L.laufe(0.25)
        z, tr = L.zuordnung(tol=80)
        ids = {i: tr[z[i][0]][5] for i in range(len(ziele)) if z[i]}
        zaehl["n"] += 1
        kan = [L.bed.get(7), L.bed.get(11)]
        flak = [L.bed.get(15), L.bed.get(19)]
        boden = {ids.get(0), ids.get(1)} - {None}
        luft = {ids.get(2), ids.get(3)} - {None}
        falsch_kan = {ids.get(2), ids.get(3), ids.get(4)} - {None}
        falsch_flak = {ids.get(0), ids.get(1), ids.get(4)} - {None}
        if any(k and k in boden for k in kan):
            zaehl["kan_boden"] += 1
        if any(k and k in falsch_kan for k in kan):
            zaehl["kan_falsch"] += 1
        if any(f and f in luft for f in flak):
            zaehl["flak_luft"] += 1
        if any(f and f in falsch_flak for f in flak):
            zaehl["flak_falsch"] += 1
    return zaehl


def main():
    ok = True
    for land in (True, False):
        z = szene(land)
        n = z["n"]
        print("%s: Kanone auf Bodenfahrzeug %d/%d, Kanone falsch %d; Flak auf Luftziel %d/%d, Flak falsch %d"
              % ("LAND (Landkreuzer)" if land else "SCHIFF (unveraendert)", z["kan_boden"], n, z["kan_falsch"],
                 z["flak_luft"], n, z["flak_falsch"]))
        if land:
            pruef = [("Kanonen meist auf einem Bodenfahrzeug", z["kan_boden"] >= n * 0.5),
                     ("Kanonen nie auf Luft oder Gebaeude", z["kan_falsch"] == 0),
                     ("Flaks auf Luftzielen", z["flak_luft"] >= n * 0.3),
                     ("Flaks nie auf Bodenzielen", z["flak_falsch"] == 0)]
            for t, g in pruef:
                print("   %-45s %s" % (t, "ok" if g else "FEHLER"))
                ok &= g
    print("ALLES OK" if ok else "FEHLER")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
