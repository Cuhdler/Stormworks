"""Setzt eine Eigenschaft (Zahl) eines eingebauten Chips direkt in der Figet Marena - sonst aendert sich nichts.
Aufruf: python chip_eigenschaft.py "<Chip-Name>" "<Eigenschaft>" <Wert> [--schreiben]
  z. B. python chip_eigenschaft.py "Figet Marena Autopilot" "Laser Hoehe Richtung" -1 --schreiben
(vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
from flak_tauschen import werte, setze  # noqa: E402


def main():
    chip, name, wert = sys.argv[1], sys.argv[2], sys.argv[3]
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    a, e = u.mc_bereich(s0, chip)
    teil = s0[a:e]
    alt = werte(teil)
    assert name in alt, ("Eigenschaft fehlt", name, sorted(alt))
    neu = setze(teil, name, wert)
    s = s0[:a] + neu + s0[e:]
    nw = werte(neu)
    geaendert = [k for k in alt if alt[k] != nw[k]]
    assert geaendert == [name], geaendert
    assert len(s) - len(s0) == len(neu) - len(teil) and s[:a] == s0[:a] and s[a + len(neu):] == s0[e:]
    print("%s: '%s' %s -> %s (sonst nichts geaendert)" % (chip, name, alt[name], nw[name]))
    if "--schreiben" in sys.argv:
        with open(u.VEH, "w", encoding="utf-8", newline="") as f:
            f.write(s)
        print("geschrieben:", u.VEH)
    else:
        print("Probelauf - nichts geschrieben (mit --schreiben ausfuehren)")


if __name__ == "__main__":
    main()
