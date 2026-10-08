"""Autopilot v1.2 ins Schiff (Andre 08.10.: "das Rein-/Rauszoomen per Hoch/Runter-Taste geht nicht"): nur die
Chip-Definition getauscht - Anschluesse und Kabel wie v1.1, Eigenschaften bleiben.
Probe: ausser dem Autopilot-Chip aendert sich nichts.
Aufruf: python autopilot12_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import build_autopilot  # noqa: E402
from waffen_update import tausche  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from autopilot_update import AP  # noqa: E402


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    assert 'description="Autopilot v1.1' in s0, "Autopilot v1.1 nicht gefunden"
    kn0 = chip_knoten(s0, AP)
    s = tausche(s0, AP, "%s %s.xml" % (AP, build_autopilot.VERSION), {})
    assert chip_knoten(s, AP) == kn0, "Anschluesse verschoben"
    a0, e0 = u.mc_bereich(s0, AP)
    a1, e1 = u.mc_bereich(s, AP)
    assert a0 == a1 and s0[:a0] == s[:a1] and s0[e0:] == s[e1:], "ausser dem Autopilot-Chip geaendert"
    print("Probe: nur der Autopilot-Chip getauscht (%s), Anschluesse gleich" % build_autopilot.VERSION)
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
