"""Vergleicht die Kabel des Schiffs mit dem Landkreuzer: Welcher Eingang eines uebernommenen Teils oder Chips hatte im
Schiff eine Quelle, die es im Panzer nicht mehr gibt? (So fiel auf, dass der Monitor 2x3 sein Einschalt-Signal vom
Waffenwahl-Chip bekam, den der Panzer nicht hat.)

Bekannte Faelle (der KI-Chip ersetzt die Quelle, oder die Quelle gehoert zu Teilen, die der Panzer nicht braucht)
stehen in ERWARTET; alles andere ist ein Fehler.
Aufruf: python landkreuzer/tools/kabel_vergleich.py [--lenkung]
"""
import collections
import os
import sys
import types

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)

TYP = {0: "An/Aus", 1: "Zahl", 4: "Strom", 5: "Composite", 6: "Video", 8: "Gurt"}
# (Kabel-Art, Quelle) -> warum das Fehlen in Ordnung ist
ERWARTET = {
    ("Composite", "Figet Marena Waffenwahl:Wahl"): "KI-Chip-Ausgang 'Wahl' (Master Arm)",
    ("Video", "Figet Marena Waffenwahl:Monitor"): "KI-Chip-Ausgang 'Status'",
    ("An/Aus", "Figet Marena Waffenwahl:Monitor an"): "KI-Chip-Ausgang 'Immer an'",
    ("Video", "Figet Marena Schiffsfuehrung:Helm"): "KI-Chip-Ausgang 'Status' (Helm)",
    ("Video", "Figet Marena Raketen:Video"): "KI-Chip-Ausgang 'Karte'",
    ("An/Aus", "Figet Marena Raketen:Freigabe"): "Raketen gibt es im Panzer nicht",
}


def vergleich(lenkung=False):
    src = open(os.path.join(HIER, "bau_landkreuzer.py"), encoding="utf-8").read()
    a = "            na, nb = abbilden(a, typ, 0), abbilden(b, typ, 1)\n"
    assert a in src, "bau_landkreuzer.kabel_bauen hat sich geaendert"
    src = src.replace(a, a + "            self.fehlend.append((typ, na, nb, sch.get((a, typ, 0)), teil_bei(a)))\n")
    src = src.replace("        alt = 0\n", "        alt = 0\n        self.fehlend = []\n", 1)
    m = types.ModuleType("bau_kopie")
    m.__file__ = os.path.join(HIER, "bau_landkreuzer.py")
    exec(compile(src, "bau_kopie", "exec"), m.__dict__)
    b = m.Bau(lenkung=lenkung)
    b.module()
    b.einzel()
    b.chaff()
    b.fahrwerk()
    b.laser()
    b.rumpf_bauen()
    b.leitern()
    b.bemalen()
    b.chips_bauen()
    b.kabel_bauen()
    fehlt = collections.Counter()
    for typ, na, nb, chip_a, teil_a in b.fehlend:
        if nb is None or na is not None or typ == 4:          # Strom-Kabel sind ungerichtet (alle an die Batterie)
            continue
        quelle = "%s:%s" % chip_a if chip_a else (teil_a[2].d if teil_a else "?")
        fehlt[(TYP.get(typ, str(typ)), quelle)] += 1
    return fehlt


def main():
    fehlt = vergleich("--lenkung" in sys.argv)
    ok = True
    for (typ, quelle), n in sorted(fehlt.items()):
        grund = ERWARTET.get((typ, quelle))
        print("%-9s %-45s %dx  %s" % (typ, quelle, n, ("ok: " + grund) if grund else "FEHLER: Eingang ohne Quelle"))
        ok &= bool(grund)
    print("ALLES OK" if ok else "FEHLER")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
