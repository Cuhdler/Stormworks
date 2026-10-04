"""Gespiegelte Radare zaehlen wohl doch nicht gespiegelt (Andres Test 03.10.: die rechte Flak - Radar gespiegelt, 'AA
Radar Richtung' -1, von mir geraten - schoss auf 'Geister' und weit vorbei, die linke mit +1 traf punktgenau; der
Pruefstand zeigt mit falschem Vorzeichen genau das).
- "Figet Marena Flak L/R" -> build_flak.VERSION (Sicherung: eigene Spur 2 s weit neben der Vorgabe -> loslassen);
  Flak R 'AA Radar Richtung' -1 -> 1
- "Figet Marena Lage" -> build_lage.VERSION (Mast-Radar 6, ebenfalls gespiegelt: Vorzeichen +1)
Lage, Kabel, Steckplaetze bleiben; uebrige Eigenschaften aus dem Schiff. Probe: sonst aendert sich nichts.
Aufruf: python vorzeichen_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import build_lage  # noqa: E402
import build_flak  # noqa: E402
from waffen_update import tausche  # noqa: E402

TAUSCH = [("Figet Marena Lage", "Figet Marena Lage %s.xml" % build_lage.VERSION, {}),
          ("Figet Marena Flak L", "Figet Marena Flak L %s.xml" % build_flak.VERSION, {}),
          ("Figet Marena Flak R", "Figet Marena Flak R %s.xml" % build_flak.VERSION, {"AA Radar Richtung": 1})]


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
