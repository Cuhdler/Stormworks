"""Pruefstand fuer den Schotten-Chip (lua/schotten.lua): alle zu/auf vom Abteil-Chip, Kippschalter je Schottwand."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_lage import lade  # noqa: E402
from test_schiff import pruefe  # noqa: E402
from build_schiff import minify, LUA_DIR  # noqa: E402


def test_schotten():
    _, g, io = lade(minify(open(os.path.join(LUA_DIR, "schotten.lua"), encoding="utf-8").read()), {})
    kn = [False] * 5

    def tick(alle):
        io["b"] = {1: alle}
        io["b"].update({2 + k: kn[k] for k in range(5)})
        g.onTick()
        return [bool(io["on"].get(101 + k)) for k in range(5)]
    r = []
    kn[2] = True                       # ein Schalter steht beim Laden schon auf an
    r.append(("Laden mit 'alle auf': alle 5 Waende auf (Schalterstellung beim Laden zaehlt nicht)",
              tick(True) == [True] * 5))
    r.append(("Wasser: alle zu", tick(False) == [False] * 5))
    kn[3] = True
    r.append(("Kippschalter Wand 4 umgelegt: nur Wand 4 auf", tick(False) == [False, False, False, True, False]))
    kn[3] = False
    r.append(("nochmal umgelegt: Wand 4 wieder zu", tick(False) == [False] * 5))
    kn[0] = True
    tick(False)
    r.append(("Feld 'alle auf': alle auf", tick(True) == [True] * 5))
    kn[0] = False
    r.append(("Kippschalter Wand 1 bei 'alle auf': Wand 1 zu", tick(True) == [False, True, True, True, True]))
    r.append(("Feld 'alle zu': alle zu", tick(False) == [False] * 5))
    return pruefe(r)


if __name__ == "__main__":
    print("ALLES OK" if test_schotten() else "FEHLER")
