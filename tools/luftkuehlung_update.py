"""Raumkuehlung des Maschinenraums (Andre 10.10.: "der Kuehler ist im Schiff drin - wenn der Raum sich erhitzt, kann er
nicht helfen, also den ganzen Raum kuehlen"): Andre hat 4 Air-Air Heat Exchanger 3x9x9 mit Rohren, Luftfiltern und
Pumpen eingebaut (Kreis A Maschinenraum, Kreis B Aussenluft). Dieses Programm verkabelt jede Pumpe, die noch kein
Kabel hat: On/Off <- Schiffsfuehrung 'Motoren an' (laufen mit den Motoren), Electric <- Batterie (-4,-13,-46).
Probe: es kommen nur Kabel dazu.
Aufruf: python luftkuehlung_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from autopilot_update import link, BATT  # noqa: E402

SCH = "Figet Marena Schiffsfuehrung"


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    tl = kf.teile(s0)
    li, le = s0.index("<logic_node_links>"), s0.index("</logic_node_links>")
    ends = collections.Counter()
    for t, a, b in re.findall(r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0([^/]*)/><voxel_pos_1([^/]*)/></logic_node_link>',
                              s0[li:le]):
        ends[(int(t or 0), u.xyz(a))] += 1
        ends[(int(t or 0), u.xyz(b))] += 1
    an = chip_knoten(s0, SCH)["Motoren an"]
    strom, mo, ty = kf.anschluss(tl, BATT[0], BATT[1], "Electric Store")
    assert ty == 4
    neu, pumpen = [], set()
    for (d, vp), lst in sorted(tl.items(), key=lambda x: x[0][1]):
        if d not in ("water_pump", "water_pump_large"):
            continue
        p_on, mo1, ty1 = kf.anschluss(tl, d, vp, "On/Off")
        p_el, mo2, ty2 = kf.anschluss(tl, d, vp, "Electric")
        assert (mo1, ty1, mo2, ty2) == (1, 0, 1, 4), (d, vp)
        if ends[(0, p_on)] == 0 or ends[(4, p_el)] == 0:
            pumpen.add(vp)
        if ends[(0, p_on)] == 0:
            neu.append((0, an, p_on, "'Motoren an' -> Pumpe %s On/Off" % (vp,)))
        if ends[(4, p_el)] == 0:
            neu.append((4, strom, p_el, "Strom -> Pumpe %s" % (vp,)))
    assert neu, "keine unverkabelte Pumpe gefunden"
    for typ, p0, p1, was in neu:
        print("  %-44s %s -> %s" % (was, p0, p1))
    s = s0[:le] + "".join(link(t, a, b) for t, a, b, _ in neu) + s0[le:]
    assert s.replace("".join(link(t, a, b) for t, a, b, _ in neu), "", 1) == s0, "ausser den Kabeln geaendert"
    print("Probe: %d Kabel neu (%d Pumpen), sonst nichts" % (len(neu), len(pumpen)))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
