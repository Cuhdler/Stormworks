"""Chips tauschen wie lage22_update, dazu die Kanonen-Chips (Kabel, Lage, Eigenschaften bleiben).
04.10.: Flak v2.4 / Kanone v1.2 - gehaltene Spur wird nie verdraengt (im Hafen fror sie ein, die Kanonen schossen nie),
Tempo-Grenze fuer Kanonen-Spuren, BC-Toleranz 6 m.
Probe: ausser den Chip-Definitionen aendert sich nichts.
Aufruf: python kanone_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import build_kanone  # noqa: E402
from lage22_update import TAUSCH as T0  # noqa: E402
from waffen_update import tausche  # noqa: E402

# BC-Toleranz 6 m (v1.2: der grosse Drehkranz steht bei kleinen Befehlen; das Schiff ist gross genug)
TAUSCH = T0 + [("Figet Marena Kanone %s" % n, "Figet Marena Kanone %s %s.xml" % (n, build_kanone.VERSION), v)
               for n, v in (("BC", {"AA Toleranz m": 6}), ("AC", {}))]


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    for name, datei, vorgabe in TAUSCH:
        s = tausche(s, name, datei, vorgabe)
    namen = "|".join(re.escape(n) for n, _, _ in TAUSCH)

    def ohne(x):
        x = re.sub(r'<microprocessor_definition name="(%s)".*?</microprocessor_definition>' % namen, "", x, flags=re.S)
        return re.sub(r"<logic_slots>(<slot(?: editor_connected=\"1\")?/>)*</logic_slots>", "<logic_slots/>", x)
    assert ohne(s0) == ohne(s), "ausser den Chip-Definitionen geaendert"
    print("Probe: nur %d Chip-Definitionen" % len(TAUSCH))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
