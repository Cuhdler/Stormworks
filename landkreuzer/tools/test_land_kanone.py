"""Pruefstand: Kanonen des Landkreuzers (BC, AC) gegen Bodenziele am Hang (mit dem Pruefstand der Figet Marena,
tools/test_kanone.py + test_flak.lauf). Unterschied zum Schiff: 'Ziel Hoehe fest m' -999 (die Kanone zielt auf die
gemessene Hoehe des Ziels, nicht 1,5 m ueber dem Meer), Land-Aenderung im Turm-Radar, eigenes Tempo 5 m/s, Gelaende
schaukelt wenig.
Treffer: wie beim Schiff (Vorbeiflug hoechstens 5 m seitlich, 2,5 m ueber/unter dem Zielpunkt).

Aufruf (mit lupa): python landkreuzer/tools/test_land_kanone.py
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
sperrprofil.koerper = lambda pfad=os.path.join(ROOT, "fahrzeug", "Figet Marena.xml"): [
    t for t in _k(pfad) if not any(d == "solid_rocket_medium" for d, _ in t)]
import test_flak  # noqa: E402
import test_kanone  # noqa: E402
import bau_landkreuzer as B  # noqa: E402

QUELLEN = B.land_lua()


def land_lua_ordner():
    """Ordner mit den Schiffs-Skripten, das Turm-Radar mit der Land-Aenderung (test_schiff.load liest dort)."""
    import shutil
    import tempfile
    import test_schiff
    d = tempfile.mkdtemp(prefix="land_lua_")
    for f in os.listdir(test_schiff.LUA_DIR):
        shutil.copy(os.path.join(test_schiff.LUA_DIR, f), d)
    with open(os.path.join(d, "flakradar.lua"), "w", encoding="utf-8") as f:
        f.write(QUELLEN["flakradar"])
    test_schiff.LUA_DIR = d


def boden(k, r, brg, dh, v=(0.0, 0.0), secs=40, own=(0.0, 5.0), **kw):
    pr, pf = test_kanone.kanone(k)
    pr.update(B.KANONE_LAND)
    b = math.radians(brg)
    return test_flak.lauf((r * math.sin(b), r * math.cos(b), dh), (v[0], v[1], 0.0), secs=secs, own=(own[0], own[1], 0.0),
                          roll=1.0, nick=1.0, fov=(0.05, 0.05), props=pr, prf=pf, see=True, rmax=9000,
                          vfehler=(15.0, -10.0, 1.0), **kw)


def main():
    land_lua_ordner()
    rueck = []
    t = lambda r: "%d Schuss, %d Treffer" % (r["schuss"], r["treffer"])
    for k, r_, brg, dh, v, mind in (("B", 1500, 30, 20, (-6.0, 4.0), 0.4), ("B", 3000, -20, 45, (5.0, 3.0), 0.4),
                                    ("B", 2000, 60, -25, (0.0, 8.0), 0.4), ("A", 800, -30, 15, (6.0, 6.0), 0.4),
                                    ("A", 1200, 20, -12, (8.0, -4.0), 0.35)):
        r = boden(k, r_, brg, dh, v=v)
        rueck.append(("%s: Bodenziel %.1f km, %+d m Hoehe, %d Grad, faehrt %.0f m/s: %s" % (
            "BC" if k == "B" else "AC", r_ / 1000, dh, brg, math.hypot(*v), t(r)),
            r["schuss"] >= 6 and r["treffer"] >= r["schuss"] * mind))
    # zum Vergleich: alte Schiffs-Einstellung (Zielhoehe fest 1,5 m ueber dem Meer) gegen ein Ziel 20 m hoeher
    pr, pf = test_kanone.kanone("B")
    pr.update(B.KANONE_LAND)
    pr["Ziel Hoehe fest m"] = 1.5
    b = math.radians(30)
    r = test_flak.lauf((1500 * math.sin(b), 1500 * math.cos(b), 20), (-6.0, 4.0, 0.0), secs=40, own=(0.0, 5.0, 0.0),
                       roll=1.0, nick=1.0, fov=(0.05, 0.05), props=pr, prf=pf, see=True, rmax=9000, vfehler=(15.0, -10.0, 1.0))
    print("  zum Vergleich mit fester Zielhoehe (Schiffs-Einstellung): %s" % t(r))
    ok = True
    for txt, g in rueck:
        print("%-95s %s" % (txt, "ok" if g else "FEHLER"))
        ok &= g
    print("ALLES OK" if ok else "FEHLER")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
