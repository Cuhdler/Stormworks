"""Tauscht die Definition eines eingebauten Chips der Figet Marena gegen eine neue Bau-Datei aus build/ - Anschluesse
muessen an derselben Stelle bleiben (neue duerfen hinten dazukommen), Eigenschaften bleiben. Sonst aendert sich nichts.
Aufruf: python chip_tauschen.py "<Chip-Name>" "<Datei in build/>" ["Eigenschaft=Wert" ...] [--schreiben]
  z. B. python chip_tauschen.py "Figet Marena Abteile" "Figet Marena Abteile v1.4.xml" --schreiben
Eigenschaften, die es schon gab, behalten ihren alten Wert - ausser sie werden mit "Eigenschaft=Wert" neu vorgegeben
(z. B. "Temp Ziel=70", wenn sich die Bedeutung oder der Standardwert geaendert hat).
(vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
from waffen_update import tausche  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402


def main():
    name, datei = sys.argv[1], sys.argv[2]
    vorgabe = dict(a.split("=", 1) for a in sys.argv[3:] if "=" in a)
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    kn0 = chip_knoten(s0, name)
    s = tausche(s0, name, datei, vorgabe)
    kn = chip_knoten(s, name)
    assert all(kn[k] == p for k, p in kn0.items()), "Anschluesse verschoben"
    a0, e0 = u.mc_bereich(s0, name)
    a1, e1 = u.mc_bereich(s, name)
    assert a0 == a1 and s0[:a0] == s[:a1] and s0[e0:] == s[e1:], "ausser dem Chip geaendert"
    print("Probe: nur '%s' getauscht (%s), Anschluesse an derselben Stelle" % (name, datei))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
