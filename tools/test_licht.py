"""Pruefstand fuer den Licht-Chip (lua/licht.lua): Tag/Nacht-Helligkeit nach der Uhr, Steuerungsraum bei Bedrohung rot."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_lage import lade  # noqa: E402
from test_schiff import pruefe  # noqa: E402
from build_schiff import minify, LUA_DIR  # noqa: E402
import build_licht as bl  # noqa: E402

PR = {n: v for n, v, _ in bl.PROPS}


def test_licht():
    src = minify(open(os.path.join(LUA_DIR, "licht.lua"), encoding="utf-8").read())
    _, g, io = lade(src, PR)

    def tick(uhr, thr=False):
        io["n"] = {1: uhr / 24.0}
        io["b"] = {25: thr}
        g.onTick()
        o = io["on"]
        return [o.get(i) for i in range(1, 7)]
    r = []
    mittag, nacht, frueh = tick(12), tick(2), tick(6.5)
    r.append(("Mittag: Farbe voll %s" % mittag, mittag[:3] == [1, 0.92, 0.8] and mittag[3:] == mittag[:3]))
    r.append(("Nacht: 0,35 %s" % [round(v, 3) for v in nacht], abs(nacht[0] - 0.35) < 1e-9 and nacht[3:] == nacht[:3]))
    r.append(("6:30 Mitte der Daemmerung: halb (%.3f)" % frueh[0], abs(frueh[0] - (0.35 + 0.65 / 2)) < 1e-9))
    r.append(("19:00 noch heller als 20:00", tick(19)[0] > tick(20)[0] and tick(21)[0] == nacht[0]))
    rot = tick(12, True)
    r.append(("Bedrohung: Steuerungsraum rot, Rest weiss %s" % rot, rot[3:] == [1, 0, 0] and rot[:3] == mittag[:3]))
    for _ in range(4 * 60):
        x = tick(12)
    r.append(("4 s nach der Meldung noch rot", x[3:] == [1, 0, 0]))
    for _ in range(61):
        x = tick(12)
    r.append(("nach 5 s wieder normal", x[3:] == mittag[:3]))
    rn = tick(2, True)
    r.append(("Bedrohung nachts: rot gedimmt %s" % [round(v, 3) for v in rn[3:]], abs(rn[3] - 0.35) < 1e-9 and rn[4] == 0))
    return pruefe(r)


if __name__ == "__main__":
    print("ALLES OK" if test_licht() else "FEHLER")
