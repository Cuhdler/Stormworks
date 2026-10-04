"""Setzt den gebauten Schiffs-Chip (build/<MC_FILE>) direkt in die Figet Marena ein - nur die Chip-Definition, alles
andere in der Fahrzeug-Datei bleibt, wie es ist. Die Anschluss-Lage muss gleich bleiben (sonst Abbruch).

Aufruf: python chip_einsetzen.py [--schreiben]   (vorher sichern; Schiff im Spiel nicht offen/gespawnt)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1  # noqa: E402
from build_schiff import BUILD, MC_FILE  # noqa: E402


def knoten(t):
    return re.findall(r'<node label="[^"]*"( mode="\d")?( type="\d")?[^>]*?(?:/>|><position([^/]*)/></node>)', t)


def main():
    umbau_v1.CHIP = os.path.join(BUILD, MC_FILE)
    s = open(umbau_v1.VEH, encoding="utf-8", newline="").read()
    a, e = umbau_v1.mc_bereich(s, "Figet Marena Schiffsfuehrung")
    teil = s[a:e]
    d0 = teil.index("<microprocessor_definition")
    d1 = teil.index("</microprocessor_definition>") + len("</microprocessor_definition>")
    neu = umbau_v1.chip_eingebettet()
    alt_k, neu_k = knoten(teil[d0:d1]), knoten(neu)
    assert alt_k == neu_k, "Anschluss-Lage/Typen geaendert - Kabel wuerden nicht mehr passen"
    s = s[:a] + teil[:d0] + neu + teil[d1:] + s[e:]
    print("Chip %s eingesetzt (%d Anschluesse, Lage unveraendert)" % (MC_FILE, len(neu_k)))
    if "--schreiben" in sys.argv:
        with open(umbau_v1.VEH, "w", encoding="utf-8", newline="") as f:
            f.write(s)
        print("geschrieben:", umbau_v1.VEH)
    else:
        print("Probelauf - nichts geschrieben (mit --schreiben ausfuehren)")


if __name__ == "__main__":
    main()
