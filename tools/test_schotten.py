"""Pruefstand fuer den Schotten-Chip v2.0 (lua/schotten.lua): alle zu/auf vom Abteil-Chip, neben jeder Tuer ein
Kippschalter fuer genau diese Tuer (Backbord Bool 2-6, Steuerbord 7-11)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_lage import lade  # noqa: E402
from test_schiff import pruefe  # noqa: E402
from build_schiff import minify, LUA_DIR  # noqa: E402


def test_schotten():
    _, g, io = lade(minify(open(os.path.join(LUA_DIR, "schotten.lua"), encoding="utf-8").read()), {})
    kn = [False] * 10                  # 0-4 Backbord Wand 1-5, 5-9 Steuerbord Wand 1-5

    def tick(alle):
        io["b"] = {1: alle}
        io["b"].update({2 + j: kn[j] for j in range(10)})
        g.onTick()
        wand = [bool(io["on"].get(101 + k)) for k in range(5)]
        tuer = [bool(io["on"].get(106 + j)) for j in range(10)]
        return wand, tuer
    r = []
    kn[2] = True                       # ein Schalter steht beim Laden schon auf an
    r.append(("Laden mit 'alle auf': alle 10 Tueren auf (Schalterstellung beim Laden zaehlt nicht)",
              tick(True) == ([True] * 5, [True] * 10)))
    r.append(("Wasser: alle zu", tick(False) == ([False] * 5, [False] * 10)))
    kn[3] = True
    w, t = tick(False)
    r.append(("Backbord-Schalter Wand 4: nur die Backbord-Tuer Wand 4 auf, Wand 4 gilt als offen",
              t == [False] * 3 + [True] + [False] * 6 and w == [False, False, False, True, False]))
    kn[8] = True
    w, t = tick(False)
    r.append(("Steuerbord-Schalter Wand 4: Steuerbord-Tuer Wand 4 auch auf", t[3] and t[8] and sum(t) == 2))
    kn[3] = not kn[3]
    w, t = tick(False)
    r.append(("Backbord Wand 4 wieder umgelegt: nur Backbord zu, Wand 4 bleibt offen (Steuerbord auf)",
              not t[3] and t[8] and w[3]))
    kn[8] = not kn[8]
    w, t = tick(False)
    r.append(("Steuerbord Wand 4 wieder umgelegt: Wand 4 ganz zu", t == [False] * 10 and w == [False] * 5))
    kn[5] = True
    w, t = tick(False)
    r.append(("Steuerbord-Schalter Wand 1: nur Steuerbord Wand 1 auf", t == [False] * 5 + [True] + [False] * 4 and w[0]))
    r.append(("Feld 'alle auf': alle auf", tick(True) == ([True] * 5, [True] * 10)))
    kn[0] = True
    w, t = tick(True)
    r.append(("Backbord Wand 1 bei 'alle auf': nur diese Tuer zu", t == [False] + [True] * 9 and w == [True] * 5))
    r.append(("Feld 'alle zu' (Wasser): alle zu", tick(False) == ([False] * 5, [False] * 10)))
    return pruefe(r)


if __name__ == "__main__":
    print("ALLES OK" if test_schotten() else "FEHLER")
