"""Pruefstand fuer den Folgeschalter (lua/folgeschalter.lua, Chips 'Folgeschalter 54 Teil 1/2')."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_lage import lade  # noqa: E402
from test_schiff import pruefe  # noqa: E402
from build_schiff import minify, LUA_DIR  # noqa: E402
import build_folgeschalter as bf  # noqa: E402

PR = {n: v for n, v, _ in bf.PROPS}


def lauf(eingabe, ticks, pr=None, zahl=False, reset=()):
    """eingabe(t) -> an?; -> Liste je Tick: Menge der Ausgaenge (1-54), die an sind"""
    src = minify(open(os.path.join(LUA_DIR, "folgeschalter.lua"), encoding="utf-8").read())
    _, g, io = lade(src, pr or PR)
    out = []
    for t in range(ticks):
        e = eingabe(t)
        io["n"] = {1: 1.0 if (zahl and e) else 0.0}
        io["b"] = {1: e and not zahl, 2: t in reset}
        io["on"].clear()
        g.onTick()
        o = io["on"]
        an = {i for i in range(1, 33) if o.get(100 + i)} | {i + 32 for i in range(1, 23) if o.get(i, 0) > .5}
        out.append(an)
    return out


def test_folgeschalter():
    rueck = []
    # 3 kurze Druecke im Abstand 3 s
    out = lauf(lambda t: t % 180 < 5 and t < 540, 900)
    rueck.append(("1. Druck: Ausgang 1 genau 4 s an (Ticks 0-239)", out[0] == {1} and 1 in out[239] and 1 not in out[240]))
    rueck.append(("2. Druck nach 3 s: Ausgang 2, 3. Druck: Ausgang 3 (je 4 s, ueberlappend)", out[180] == {1, 2}
                  and out[360] == {2, 3} and out[599] == {3} and out[600] == set()))
    # gehaltener Eingang = ein Druck
    out = lauf(lambda t: t < 600, 700)
    rueck.append(("10 s gehalten = nur Ausgang 1", all(o <= {1} for o in out) and out[0] == {1}))
    # schnelle Druecke innerhalb 2 s zaehlen nicht
    out = lauf(lambda t: (t // 10) % 2 == 0 and t < 300, 400)
    gesehen = set().union(*out)
    rueck.append(("Druecke alle 1/3 s ueber 5 s: Ausgang 1-3 (alle 2 s einer), gesehen %s" % sorted(gesehen),
                  gesehen == {1, 2, 3}))
    # Zahl-Eingang 1 statt an
    out = lauf(lambda t: t < 5, 60, zahl=True)
    rueck.append(("Zahl-Eingang 1 wirkt wie an", out[0] == {1}))
    # alle 54 der Reihe nach, danach nichts mehr
    out = lauf(lambda t: t % 130 < 3, 130 * 60)
    starts = [min(i for i in range(len(out)) if k in out[i]) if any(k in o for o in out) else None for k in range(1, 56)]
    rueck.append(("54 Druecke: Ausgang 1..54 der Reihe nach, 55. Druck nichts",
                  all(starts[k] == 130 * k for k in range(54)) and starts[54] is None))
    # von vorn
    pr = dict(PR)
    pr["Nach dem letzten von vorn"] = 1
    pr["Anzahl Ausgaenge"] = 3
    out = lauf(lambda t: t % 130 < 3, 130 * 5, pr=pr)
    rueck.append(("'von vorn' bei 3 Ausgaengen: 4. Druck = Ausgang 1", 1 in out[390] and out[390] - {3} == {1}))
    # Reset
    out = lauf(lambda t: t % 200 < 3 and t < 600, 700, reset={250})
    rueck.append(("Reset nach 2 Druecken: alles aus, naechster Druck = Ausgang 1", out[251] == set() and out[400] == {1}))
    return pruefe(rueck)


if __name__ == "__main__":
    print("ALLES OK" if test_folgeschalter() else "FEHLER")
