"""Schreiber v2 ins Schiff (04.10.):
- die vier Waffen-Chips (Lage, Bildschirm, Flak L/R) wie lage22_update tauschen (Kabel, Lage, Eigenschaften bleiben;
  Flak R 'AA Radar Richtung' -1)
- Schiffsfuehrung und Flossen: nur die Eigenschaft 'Log Port' auf 0 (ihr Fahrtenschreiber schickte an 8766/8767, wo
  niemand lauscht - jede Anfrage blockierte die HTTP-Warteschlange des Spiels ~4 s, der Waffen-Log hinkte Minuten
  hinterher). Zurueck: Wert wieder 8766 / 8767 und tools/logger.py starten.
Probe: ausser diesen Stellen aendert sich nichts.
Aufruf: python schreiber2_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
from lage22_update import TAUSCH  # noqa: E402
from waffen_update import tausche  # noqa: E402

LOG_AUS = {"Figet Marena Schiffsfuehrung": "8766", "Figet Marena Flossen": "8767"}


def log_aus(s, name, alt):
    m = re.search(r'<microprocessor_definition name="%s".*?</microprocessor_definition>' % re.escape(name), s, re.S)
    assert m, name
    d = m.group(0)
    muster = r'(n="Log Port"><pos[^>]*/><v text=")%s(" value=")%s(")' % (alt, alt)
    neu, n = re.subn(muster, r"\g<1>0\g<2>0\g<3>", d)
    if n == 0 and re.search(r'n="Log Port"><pos[^>]*/><v text="0"', d):
        print("%s: Log Port ist schon 0" % name)
        return s
    assert n == 1, (name, "Log Port %s nicht genau einmal gefunden" % alt, n)
    print("%s: Log Port %s -> 0" % (name, alt))
    return s[:m.start()] + neu + s[m.end():]


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    for name, datei, vorgabe in TAUSCH:
        s = tausche(s, name, datei, vorgabe)
    for name, alt in LOG_AUS.items():
        s = log_aus(s, name, alt)
    namen = "|".join(re.escape(n) for n, _, _ in TAUSCH)

    def ohne(x):
        x = re.sub(r'<microprocessor_definition name="(%s)".*?</microprocessor_definition>' % namen, "", x, flags=re.S)
        return re.sub(r'(n="Log Port"><pos[^>]*/><v text=")\d+(" value=")\d+(")', r"\1X\2X\3", x)
    assert ohne(s0) == ohne(s), "ausser Chip-Definitionen und Log Port geaendert"
    print("Probe: nur %d Chip-Definitionen und Log Port" % len(TAUSCH))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
