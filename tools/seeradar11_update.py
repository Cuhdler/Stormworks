"""Seeradar v1.1 + Bildschirm v3.4 ins Schiff (Andres Test 06.10.: "Seeradar kopfueber, man muss klar erkennen, wohin
das Schiff zeigt; auf dem grossen Bildschirm steht oben links 200 m, das kann nicht sein"):
- Seeradar v1.1: Bild um 'Bild drehen' Viertel gedreht (2), Bug-Strich, groesseres Schiff
- Bildschirm v3.4: Radar-Zoom zaehlt nur Ziele fuer die Waffen (stehende Hafen-Dinge hielten ihn auf 200 m)
Nur die zwei Chip-Definitionen werden getauscht (Anschluesse gleich, Kabel bleiben, Eigenschaften bleiben).
Aufruf: python seeradar11_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import build_seeradar  # noqa: E402
import build_lage  # noqa: E402
from waffen_update import tausche  # noqa: E402

TAUSCH = [("Figet Marena Seeradar", "Figet Marena Seeradar %s.xml" % build_seeradar.VERSION, {}),
          ("Figet Marena Bildschirm", "Figet Marena Bildschirm %s.xml" % build_lage.VERSION_BILD, {})]


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    for name, datei, vorgabe in TAUSCH:
        s = tausche(s, name, datei, vorgabe)
    namen = "|".join(re.escape(n) for n, _, _ in TAUSCH)

    def ohne(x):
        return re.sub(r'<microprocessor_definition name="(%s)".*?</microprocessor_definition>' % namen, "", x, flags=re.S)
    assert ohne(s0) == ohne(s), "ausser den zwei Chip-Definitionen geaendert"
    for name, _, _ in TAUSCH:
        print("  %s: %s" % (name, re.search(r'<microprocessor_definition name="%s" description="([^"]*)"' % re.escape(name),
                                            s).group(1)[:60]))
    print("Probe: nur die zwei Chip-Definitionen getauscht")
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
