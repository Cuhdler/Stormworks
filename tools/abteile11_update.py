"""Abteil-Anzeige v1.1 ins Schiff (Andre 08.10.: "der Monitor ist kopfueber" - Monitor 9x5 per teil_drehen.py um 180 Grad
gedreht; Grundriss jetzt mit Bug unten / Steuerbord links wie mit Blick zum Heck): nur die Definition des Chips
"Figet Marena Abteile" getauscht - Anschluesse und Kabel gleich, Eigenschaften bleiben (neu 'Bug unten' 1).
Aufruf: python abteile11_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import build_abteile  # noqa: E402
from waffen_update import tausche  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402

AB = "Figet Marena Abteile"


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    assert 'description="Abteile v1.0' in s0, "Abteile v1.0 nicht gefunden"
    kn0 = chip_knoten(s0, AB)
    s = tausche(s0, AB, "%s %s.xml" % (AB, build_abteile.VERSION), {})
    assert chip_knoten(s, AB) == kn0, "Anschluesse verschoben"
    a0, e0 = u.mc_bereich(s0, AB)
    a1, e1 = u.mc_bereich(s, AB)
    assert a0 == a1 and s0[:a0] == s[:a1] and s0[e0:] == s[e1:], "ausser dem Abteil-Chip geaendert"
    print("Probe: nur der Abteil-Chip getauscht (%s), Anschluesse gleich" % build_abteile.VERSION)
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
