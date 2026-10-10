"""E-Motoren ins Schiff (Andre 10.10.: zwei grosse E-Motoren (motor_large) an der Welle vor den Getrieben, statt der
kleinen Generatoren; Plan C gegen die Ueberhitzung):
- Flossen v1.7 -> v1.8: neuer Eingang 'Batterie' (Kanal 21 von 'Physik weiter'); Kabel Charge der Batterie
  (-4,-13,-46) -> 'Batterie'
- Schiffsfuehrung v3.4 -> v3.5 (gleiche 36 Anschluesse an gleicher Stelle; Einstellungen behalten ihre Werte):
  'Motor L an' -> 'Motoren an' (alle Pumpen/Luefter: die Kabel von 'Motor R an' gehen jetzt von hier),
  'Motor R an' -> 'E-Motor L' (Zahl) -> Throttle des linken E-Motors (-8,-13,-96),
  'Rueckwaerts L' -> 'Rueckwaerts' (beide Getriebe: das Kabel von 'Rueckwaerts R' geht jetzt von hier),
  'Rueckwaerts R' -> 'E-Motor R' (Zahl) -> Throttle des rechten E-Motors (8,-13,-96)
Probe: ausser den zwei Chips und den Kabeln aendert sich nichts.
Aufruf: python emotor_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import build_schiff as bsch  # noqa: E402
import build_flossen as bfl  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from waffen_update import tausche  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from flak_tauschen import werte, setze  # noqa: E402
from autopilot_update import link, enden, BATT, LINKS  # noqa: E402

SCH, FL = "Figet Marena Schiffsfuehrung", "Figet Marena Flossen"
MOTOR = {"L": ("motor_large", (-8, -13, -96)), "R": ("motor_large", (8, -13, -96))}


def schiff_tauschen(s):
    """Definition der Schiffsfuehrung ersetzen; Anschluss-Lagen muessen gleich bleiben (Art darf sich aendern)."""
    a, e = u.mc_bereich(s, SCH)
    teil = s[a:e]
    d0 = teil.index("<microprocessor_definition")
    d1 = teil.index("</microprocessor_definition>") + len("</microprocessor_definition>")
    alt = teil[d0:d1]
    u.CHIP = os.path.join(BUILD, bsch.MC_FILE)
    neu = u.chip_eingebettet()
    lage = lambda t: [m.group(1) or "" for m in re.finditer(r'<node label="[^"]*"[^>]*?(?:/>|><position([^/]*)/></node>)', t)]
    assert lage(alt) == lage(neu), "Anschluss-Lagen geaendert"
    alt_w, neu_w = werte(alt), werte(neu)
    for n, v in alt_w.items():
        if n in neu_w:
            neu = setze(neu, n, v)
    nw = werte(neu)
    print("%s -> %s: %d Anschluesse; Eigenschaften neu: %s; weg: %s" % (
        SCH, bsch.MC_FILE, len(lage(neu)), sorted(set(nw) - set(alt_w)), sorted(set(alt_w) - set(nw))))
    return s[:a] + teil[:d0] + neu + teil[d1:] + s[e:]


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    assert 'description="Schiff v3.4:' in s and 'description="Flossen v1.7:' in s, "Stand passt nicht"
    ks0 = chip_knoten(s, SCH)
    s = tausche(s, FL, bfl.MC_FILE, {})
    s = schiff_tauschen(s)
    ks, kfl = chip_knoten(s, SCH), chip_knoten(s, FL)
    assert ks["Motoren an"] == ks0["Motor L an"] and ks["E-Motor L"] == ks0["Motor R an"]
    assert ks["Rueckwaerts"] == ks0["Rueckwaerts L"] and ks["E-Motor R"] == ks0["Rueckwaerts R"]
    tl = kf.teile(s)

    def an(d_, vp, lab, mo_soll, ty_soll):
        p, mo, ty = kf.anschluss(tl, d_, vp, lab)
        assert mo == mo_soll and ty == ty_soll, (d_, vp, lab, mo, ty)
        return p
    li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
    alt_l = re.findall(LINKS, s[li:le])
    assert "".join(alt_l) == s[li:le]
    neu_l, umgelegt = [], {"Motor R an": 0, "Rueckwaerts R": 0}
    for x in alt_l:
        p0, p1 = enden(x)
        for alt_name, neu_name in (("Motor R an", "Motoren an"), ("Rueckwaerts R", "Rueckwaerts")):
            if p0 == ks0[alt_name]:
                assert not re.search(r'type="\d"', x), ("kein An/Aus-Kabel", x)
                x = link(0, ks[neu_name], p1)
                umgelegt[alt_name] += 1
            assert p1 != ks0[alt_name], ("Kabel endet an einem Ausgang?", x)
        neu_l.append(x)
    print("umgelegt: %d Kabel 'Motor R an' -> 'Motoren an', %d Kabel 'Rueckwaerts R' -> 'Rueckwaerts'" % (
        umgelegt["Motor R an"], umgelegt["Rueckwaerts R"]))
    assert umgelegt["Motor R an"] > 0 and umgelegt["Rueckwaerts R"] == 1, umgelegt
    neu = [(1, an(BATT[0], BATT[1], "Charge", 0, 1), kfl["Batterie"], "Batterie %s Charge -> Flossen 'Batterie'" % (BATT[1],))]
    for seite, (d_, vp) in MOTOR.items():
        neu.append((1, ks["E-Motor %s" % seite], an(d_, vp, "Throttle", 1, 1), "Schiff 'E-Motor %s' -> E-Motor %s Throttle" % (seite, vp)))
    belegte_eing = set((int(t or 0), p1) for t, p1 in re.findall(
        r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0[^>]*/>(<voxel_pos_1[^>]*/>)', "".join(neu_l)))
    for typ, p0, p1, was in neu:
        assert (typ, u.vox("voxel_pos_1", p1)) not in belegte_eing, ("Eingang schon belegt", was, p1)
        neu_l.append(link(typ, p0, p1))
        print("  %-52s %s -> %s" % (was, p0, p1))
    s = s[:li] + "".join(neu_l) + s[le:]

    def ohne(x, neu_):
        for name in (SCH, FL):
            a2, e2 = u.mc_bereich(x, name)
            x = x[:a2] + "<CHIP/>" + x[e2:]
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0, False) == ohne(s, True), "ausser den Chips und Kabeln geaendert"
    print("Probe: Flossen %s, Schiff %s, Kabel umgelegt und 3 neu, sonst nichts" % (bfl.MC_FILE, bsch.MC_FILE))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
