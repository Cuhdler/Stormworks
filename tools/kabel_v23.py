"""Figet Marena, Schiff v2.3: Gear-Switch-Kabel vom Schiffs-Chip zu den Getrieben (Andres Umbau 01.10.).

Je Seite 4 Getriebe 1x1 auf der Welle (x = -8 links, +8 rechts, y = -16), Pfeil zum Motor:
  z = -98  gear_ratio_2 2 = 6:5   -> 'Getriebe A'
  z = -99  gear_ratio_2 3 = 3:2   -> 'Getriebe B'
  z = -100 (kein Eintrag)         -> 'Getriebe C' (soll 2:1 sein - im Editor pruefen)
  z = -101 gear_ratio_2 0 = 1:-1  -> 'Rueckwaerts L/R'
Index-Zuordnung: 2 = 6:5 und 3 = 3:2 aus dem Getriebe-Umbau 27.09.; 0 = 1:-1 und 1 = 1:1 aus dem Rueckwaerts-Getriebe
(Claude trug 1 ein, Andre sah im Editor '1:1 - 1:1' und stellte es um, danach stand dort 0).
Gear Switch liegt in der Getriebe-Mitte (Welt = Position des Getriebes). Chip-Anschluss (x, z) -> umbau_v1.chip.
Jedes Ziel wird geprueft (Getriebe an der Stelle, Strom vorhanden), vorhandene Kabel bleiben, doppelte entfallen.
Aufruf: python kabel_v23.py [--schreiben]   (Schiff im Spiel nicht offen bzw. danach ohne Speichern neu laden!)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402

ZIELE = {
    "Rueckwaerts L": [(-8, -16, -101)],
    "Rueckwaerts R": [(8, -16, -101)],
    "Getriebe A": [(-8, -16, -98), (8, -16, -98)],
    "Getriebe B": [(-8, -16, -99), (8, -16, -99)],
    "Getriebe C": [(-8, -16, -100), (8, -16, -100)],
}


def main():
    s = open(u.VEH, encoding="utf-8", newline="").read()
    a, e = u.mc_bereich(s, "Figet Marena Schiffsfuehrung")
    teil = s[a:e]
    assert re.search(r'</microprocessor_definition><vp y="-12" z="-41"/>', teil), "Chip nicht mehr bei (0,-12,-41)"
    assert 'r="0,-1,0,1,0,0,0,0,1"' in teil[:200], "Chip anders gedreht"
    knoten = {}
    for m in re.finditer(r'<node label="([^"]*)"([^>]*?)(?:/>|><position([^/]*)/></node>)', teil):
        pa = dict(re.findall(r'(\w)="(-?\d+)"', m.group(3) or ""))
        knoten[m.group(1)] = (u.chip(int(pa.get("x", 0)), int(pa.get("z", 0))), 'mode="1"' in m.group(2))
    getriebe = {}
    for m in re.finditer(r'<c d="modular_engine_gearbox_1x1"(?: t="\d+")?><o ([^>]*)><vp([^/]*)/>', s):
        getriebe[u.xyz(m.group(2))] = m.group(1)
    li, le = s.index("<logic_node_links>"), s.index("</logic_node_links>")
    alt = re.findall(r"<logic_node_link.*?</logic_node_link>", s[li:le])
    strom = {u.xyz(p) for t, a0, a1 in re.findall(r'<logic_node_link( type="4")><voxel_pos_0([^/]*)/><voxel_pos_1([^/]*)/>', s[li:le])
             for p in (a0, a1)}
    neu = []
    for label, ziele in ZIELE.items():
        pos, eingang = knoten[label]
        assert not eingang, (label, "ist ein Eingang")
        for z in ziele:
            assert z in getriebe, ("kein Getriebe bei", z)
            assert z in strom, ("Getriebe ohne Strom", z)
            k = "<logic_node_link>%s%s</logic_node_link>" % (u.vox("voxel_pos_0", pos), u.vox("voxel_pos_1", z))
            print("  %-14s %s -> Getriebe %s (%s)" % (label, pos, z, getriebe[z].strip()))
            if k not in alt:
                neu.append(k)
    print("vorhandene Kabel %d, neu %d" % (len(alt), len(neu)))
    s = s[:le] + "".join(neu) + s[le:]
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
