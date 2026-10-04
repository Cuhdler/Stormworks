"""Halbautomatik (Andre 03.10. abends): Chip-Definitionen tauschen - Lage, Bildschirm, Waffenwahl, Flak L/R.
- "Figet Marena Lage" -> build_lage.VERSION (Freund statt Markierung, kein AUTO-Markieren)
- "Figet Marena Bildschirm" -> build_lage.VERSION_BILD (Waffen suchen selbst, Flaks nie auf dasselbe, Master Arm,
  Leertaste fuer die gewaehlte Waffe, Radar zoomt selbst; Eingaenge nur noch in onTick - 'draw error 202')
- "Figet Marena Waffenwahl" -> build_lage.VERSION_WAHL (Anschluss 'Master Arm' dazu, hinten angehaengt; Eingaenge
  nur in onTick)
- "Figet Marena Flak L/R" -> build_flak.VERSION (Hardlock auf die zugewiesene Zielnummer)
Lage, Kabel und Steckplaetze bleiben (Waffenwahl: ein Steckplatz dazu). Der Master-Arm-Schalter ist noch nicht
gebaut: bis er am Anschluss 'Master Arm' haengt, schiesst keine Waffe.
Aufruf: python halbauto_update.py [--schreiben]   (vorher sichern; danach Schiff im Spiel neu laden, NICHT vorher speichern)
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
          ("Figet Marena Bildschirm", "Figet Marena Bildschirm %s.xml" % build_lage.VERSION_BILD, {}),
          ("Figet Marena Waffenwahl", "Figet Marena Waffenwahl %s.xml" % build_lage.VERSION_WAHL, {}),
          ("Figet Marena Flak L", "Figet Marena Flak L %s.xml" % build_flak.VERSION, {}),
          ("Figet Marena Flak R", "Figet Marena Flak R %s.xml" % build_flak.VERSION, {})]


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    for name, datei, vorgabe in TAUSCH:
        s = tausche(s, name, datei, vorgabe)
    namen = "|".join(re.escape(n) for n, _, _ in TAUSCH)

    def ohne(x):
        x = re.sub(r'<microprocessor_definition name="(%s)".*?</microprocessor_definition>' % namen, "", x, flags=re.S)
        return re.sub(r"<logic_slots>(<slot/>)+</logic_slots>", "<logic_slots/>", x)
    assert ohne(s0) == ohne(s), "ausser den Chip-Definitionen geaendert"
    print("Probe: nur %d Chip-Definitionen (und ein Steckplatz mehr an der Waffenwahl)" % len(TAUSCH))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
