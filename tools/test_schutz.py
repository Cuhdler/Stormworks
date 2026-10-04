"""Pruefstand fuer den Schutz-Chip (lua/schutz.lua): Auto-Chaff und Pumpen."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_lage import lade  # noqa: E402
from test_schiff import pruefe  # noqa: E402
from build_schiff import minify, LUA_DIR  # noqa: E402
import build_schutz  # noqa: E402

PR = {n: v for n, v, _ in build_schutz.PROPS}
PR.update({"Schreiber Port": 0, "Schreiber Zeichen": 3000})


def lauf(ortung, auto=lambda t: True, pumpe=lambda t: False, ticks=3000):
    """ortung(t) -> Radar Detector; -> Liste je Tick (links, rechts, pumpen)"""
    _, g, io = lade(minify(open(os.path.join(LUA_DIR, "schutz.lua"), encoding="utf-8").read()), PR)
    out = []
    for t in range(ticks):
        io["n"], io["b"] = {}, {3: auto(t), 4: pumpe(t), 5: ortung(t)}
        io["on"].clear()
        g.onTick()
        out.append((io["on"].get(101, False), io["on"].get(102, False), io["on"].get(103, False)))
    return out


def test_schutz():
    rueck = []
    # Ortung 30 s lang: Salve sofort, dann alle 1,5 s, hoechstens 8
    r = lauf(lambda t: 100 <= t < 1900)
    sv = [t for t, (l, rr, _) in enumerate(r) if l]
    gleich = all(l == rr for l, rr, _ in r)
    rueck.append(("Ortung 30 s: %d Salven bei Tick %s, links und rechts immer gleichzeitig: %s" % (len(sv), sv[:4], gleich),
                  len(sv) == 8 and sv[0] == 100 and sv[1] - sv[0] == 90 and gleich))
    # kurze Pause (1 s) zaehlt nicht als neue Ortung, lange (5 s) schon: 8 + 3 Salven (die neue Ortung dauert 200 Ticks)
    r = lauf(lambda t: 100 <= t < 1000 or 1060 <= t < 1500 or 1800 <= t < 2000)
    sv = [t for t, (l, _, _) in enumerate(r) if l]
    rueck.append(("Ortung mit 1 s Luecke, dann 5 s Pause: %d Salven, die 9. bei Tick %s" % (len(sv), sv[8] if len(sv) > 8 else None),
                  len(sv) == 11 and sv[8] == 1800))
    # Auto-Chaff aus: nichts
    r = lauf(lambda t: True, auto=lambda t: False)
    rueck.append(("Auto-Chaff aus: %d Salven" % sum(1 for l, _, _ in r if l), not any(l for l, _, _ in r)))
    # 60 Salven, dann leer (Ortung mit Pausen, viele Folgen)
    r = lauf(lambda t: (t // 400) % 2 == 0, ticks=20000)
    rueck.append(("viele Ortungen: hoechstens 60 Salven (%d)" % sum(1 for l, _, _ in r if l), sum(1 for l, _, _ in r if l) == 60))
    # Pumpen folgen dem Schalter
    r = lauf(lambda t: False, pumpe=lambda t: 50 <= t < 100, ticks=200)
    rueck.append(("Pumpen folgen dem Schalter", all(p == (50 <= t < 100) for t, (_, _, p) in enumerate(r))))
    return pruefe(rueck)


if __name__ == "__main__":
    print("ALLES OK" if test_schutz() else "FEHLER")
