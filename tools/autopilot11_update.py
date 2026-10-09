"""Autopilot v1.1 ins Schiff (Andre 08.10.: "mit Blickrichtung bewegt man ein Kreuz auf der Karte (nicht schiffzentriert),
Leertaste macht einen Wegpunkt, nochmal an derselben Stelle wieder weg; Touchscreen kommt ganz raus, Zoom ist jetzt
hoch/runter; standardmaessig ist der Bug-Laser aus, mit dem Knopf 'Automatic anti kollision' wird er angeschaltet"):
- Chip-Definition getauscht (Anschluesse gleich; 'Touch' heisst 'Griff', neu hinten 'Knopf Anti-Kollision' auf dem
  freien Feld (2,2) = (-2,10,-59)); Eigenschaften bleiben (u. a. 'Laser Hoehe Richtung' -1)
- Kabel: Monitor 5x3 Touch -> Autopilot weg; Control Handle (-6,19,-21) Seat data -> 'Griff'; Knopf 'Automatic anti
  kollision' (-8,19,-22) Pressed -> 'Knopf Anti-Kollision'; Strom Batterie (-4,-13,-46) -> dieser Knopf
Probe: ausser Autopilot-Chip und Kabeln aendert sich nichts.
Aufruf: python autopilot11_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import build_autopilot  # noqa: E402
from waffen_update import tausche  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from autopilot_update import link, enden, teil_bereich, AP, MON, BATT, LINKS  # noqa: E402

GRIFF = ("seat_handle", (-6, 19, -21))
KN_AK = ("button_push", (-8, 19, -22))


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    assert 'description="Autopilot v1.0' in s, "Autopilot v1.0 nicht gefunden (schon v1.1?)"
    tl = kf.teile(s)
    for d, vp in (GRIFF, KN_AK, MON, BATT):
        assert len(tl.get((d, vp), [])) == 1, ("Teil fehlt", d, vp)
    a, e = teil_bereich(s, *KN_AK)
    assert 'custom_name="Automatic anti kollision"' in s[a:e], "Knopf 'Automatic anti kollision' nicht an (-8,19,-22)"
    alt_kn = chip_knoten(s, AP)
    s = tausche(s, AP, "%s %s.xml" % (AP, build_autopilot.VERSION), {})
    ak = chip_knoten(s, AP)
    assert ak["Griff"] == alt_kn["Touch"] and all(ak[k] == p for k, p in alt_kn.items() if k != "Touch"), "Lage geaendert"
    print("Autopilot-Chip -> %s; 'Griff' %s, 'Knopf Anti-Kollision' %s" % (build_autopilot.VERSION, ak["Griff"],
                                                                         ak["Knopf Anti-Kollision"]))

    def an(teil_, lab, mo_soll, ty_soll):
        p, mo, ty = kf.anschluss(tl, teil_[0], teil_[1], lab)
        assert mo == mo_soll and ty == ty_soll, (teil_, lab, mo, ty)
        return p
    touch = an(MON, "Touch Output", 0, 5)
    li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
    alt_l = re.findall(LINKS, s[li:le])
    assert "".join(alt_l) == s[li:le], "Kabelliste nicht vollstaendig erfasst"
    weg = [x for x in alt_l if enden(x) == [touch, ak["Griff"]] and 'type="5"' in x]
    assert len(weg) == 1, ("Kabel Touch -> Autopilot", weg)
    bleibt = [x for x in alt_l if x not in weg]
    neu = [(5, an(GRIFF, "Seat data", 0, 5), ak["Griff"], "Control Handle Seat data -> Autopilot 'Griff'"),
           (0, an(KN_AK, "Pressed", 0, 0), ak["Knopf Anti-Kollision"], "Knopf 'Automatic anti kollision' -> Autopilot"),
           (4, an(BATT, "Electric Store", 1, 4), an(KN_AK, "Electric", 1, 4), "Strom -> Knopf Anti-Kollision")]
    belegte_eing = set((int(t or 0), p1) for t, p1 in re.findall(
        r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0[^>]*/>(<voxel_pos_1[^>]*/>)', "".join(bleibt)))
    zu = []
    for typ, p0, p1, was in neu:
        assert (typ, u.vox("voxel_pos_1", p1)) not in belegte_eing, ("Eingang schon belegt", was, p1)
        zu.append(link(typ, p0, p1))
        print("  %-48s %s -> %s" % (was, p0, p1))
    for x in weg:
        print("  Kabel weg: %s" % x)
    s = s[:li] + "".join(bleibt + zu) + s[le:]

    # Probe
    def ohne(x):
        a2, e2 = u.mc_bereich(x, AP)
        x = x[:a2] + x[e2:]
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0) == ohne(s), "ausser Autopilot-Chip und Kabeln geaendert"
    assert re.findall(LINKS, s[s.index("<logic_node_links>"):s.index("</logic_node_links>")]) == bleibt + zu
    print("Probe: Autopilot-Chip getauscht, %d Kabel weg, %d neu, sonst nichts" % (len(weg), len(zu)))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
