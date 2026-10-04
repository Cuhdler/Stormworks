"""Lagezentrale v2.2 (Andre 03.10.: Helis neben 5 gelockten Schiffen ignoriert; Ziel 2 sprang herum und wechselte die Art):
- "Figet Marena Lage" -> build_lage.VERSION: Plaetze 1-2 Luft, 3-4 See, 5 frei (Raketen); Topf fuer Ziele ohne Platz;
  haltendes Radar fuehrt nur sein eigenes Ziel nach (enger Fangbereich, Hoehe voll); Radar 1 sucht flach, Radar 6 hoch
- "Figet Marena Bildschirm" -> build_lage.VERSION_BILD: Ziele ueber die Kennung behalten (koennen den Platz wechseln),
  Kanonen verteilen sich, leere Plaetze zeigen ihre Art
Lage, Kabel, Steckplaetze bleiben; Eigenschaften aus dem Schiff. Probe: sonst aendert sich nichts.
Aufruf: python lage22_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import build_lage  # noqa: E402
import build_flak  # noqa: E402
from waffen_update import tausche  # noqa: E402

TAUSCH = [("Figet Marena Lage", "Figet Marena Lage %s.xml" % build_lage.VERSION, {"Mindestabstand m": 30}),
          ("Figet Marena Flak L", "Figet Marena Flak L %s.xml" % build_flak.VERSION, {}),
          ("Figet Marena Flak R", "Figet Marena Flak R %s.xml" % build_flak.VERSION, {"AA Radar Richtung": -1}),
          ("Figet Marena Bildschirm", "Figet Marena Bildschirm %s.xml" % build_lage.VERSION_BILD, {})]


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    for name, datei, vorgabe in TAUSCH:
        s = tausche(s, name, datei, vorgabe)
    namen = "|".join(re.escape(n) for n, _, _ in TAUSCH)

    def ohne(x):
        return re.sub(r'<microprocessor_definition name="(%s)".*?</microprocessor_definition>' % namen, "", x, flags=re.S)
    assert ohne(s0) == ohne(s), "ausser den Chip-Definitionen geaendert"
    print("Probe: nur %d Chip-Definitionen" % len(TAUSCH))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
