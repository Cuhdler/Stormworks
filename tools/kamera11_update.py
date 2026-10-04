"""Kamera-Chip v1.1 ins Schiff (Andres Test 04.10. 15:01: "die Kamera hat sich nicht mal bewegt" - Pivot/Pitch sind
Tempo-Eingaenge mit Totzone 0,1, die Befehle von v1.0 lagen darunter). Nur die Chip-Definition 'Figet Marena Kamera'
wird getauscht (Anschluesse gleich, Kabel bleiben; Eigenschaften: neue mit Vorgabe, gleichnamige aus dem Schiff).
Probe: ausser dieser Chip-Definition aendert sich nichts.
Aufruf: python kamera11_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import build_kamera  # noqa: E402
from waffen_update import tausche  # noqa: E402

TAUSCH = [("Figet Marena Kamera", "Figet Marena Kamera %s.xml" % build_kamera.VERSION, {"Drehung 0 ab Bug U": 0.5, "Kreis Grad": 8, "Totzone Grad": 0.8, "Kreis Pixel": 16})]


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    for name, datei, vorgabe in TAUSCH:
        s = tausche(s, name, datei, vorgabe)
    namen = "|".join(re.escape(n) for n, _, _ in TAUSCH)

    def ohne(x):
        return re.sub(r'<microprocessor_definition name="(%s)".*?</microprocessor_definition>' % namen, "", x, flags=re.S)
    assert ohne(s0) == ohne(s), "ausser der Chip-Definition geaendert"
    print("Probe: nur %d Chip-Definition" % len(TAUSCH))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
