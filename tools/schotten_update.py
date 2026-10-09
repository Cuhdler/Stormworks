"""Schotten-Chip + Abteile v1.5 ins Schiff (Andre 08.10.: "wenn Wasser reinkommt automatisch alle Schotten zu, und falls
man unten ist, habe ich neben jede Tuer einen Knopf platziert, damit man sie manuell oeffnen kann - die musst du noch
verbinden"; "'ABTEILE' steht ueber einem Strich, die kleinen Punkte sind viel zu unuebersichtlich"):
- Chip "Figet Marena Schotten" 4x3 an der Decke des Chip-Raums: vp (-2,13,-50), Bild nach unten (x -2..1, z -52..-50)
- Abteile -> v1.5 (Liste statt Grundriss, Tueren je Schottwand; 'Auto zu ab %' 0,5 statt 5; neuer Eingang 'Tueren')
- Kabel: Abteile 'Schotten auf' -> 10 Tueren weg; dafuer -> Schotten 'Alle auf'; Schotten 'Tueren Wand k' -> Open/Close
  der 2 Tueren der Wand; Kippschalter (Toggled) -> 'Knopf Wand k'; Schotten 'Zustand' -> Abteile 'Tueren';
  Strom Batterie (-4,-13,-46) -> 5 Kippschalter
Probe: ausser den zwei Chips und den Kabeln aendert sich nichts.
Aufruf: python schotten_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import sperrprofil  # noqa: E402
import build_abteile as ba  # noqa: E402
import build_schotten as bs  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from waffen_update import tausche  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from autopilot_update import link, enden, chip_flaeche, flaeche, BATT, LINKS, AP  # noqa: E402

SCH, AB = "Figet Marena Schotten", "Figet Marena Abteile"
VP, R_ = (-2, 13, -50), "1,0,0,0,-1,0,0,0,-1"


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    assert 'description="Abteile v1.4' in s and '<microprocessor_definition name="%s"' % SCH not in s, "Stand passt nicht"
    tl = kf.teile(s)
    for wd in bs.WAENDE:
        assert len(tl.get(("door", wd[0]), [])) == 1 and len(tl.get(("door", wd[1]), [])) == 1, wd
        assert len(tl.get(("button_toggle_2side", wd[2]), [])) == 1, wd
    # Abteile tauschen ('Auto zu ab %' neu 0,5)
    ka0 = chip_knoten(s, AB)
    s = tausche(s, AB, "%s %s.xml" % (AB, ba.VERSION), {"Auto zu ab %": 0.5})
    ka = chip_knoten(s, AB)
    assert all(ka[k] == p for k, p in ka0.items()), "Abteile: Anschluesse verschoben"
    # Schotten-Chip an die Decke
    u.CHIP = os.path.join(BUILD, "%s %s.xml" % (SCH, bs.VERSION))
    d = u.chip_eingebettet()
    w = int(re.search(r'<microprocessor_definition [^>]*width="(\d+)"', d).group(1))
    ln = int(re.search(r'<microprocessor_definition [^>]*length="(\d+)"', d).group(1))
    nk = len(re.findall(r"<n id=", d))
    R = [[int(v) for v in R_.split(",")][i * 3:i * 3 + 3] for i in range(3)]
    fl = flaeche(R, VP, w, ln)
    teile_vox = set(p for teile in sperrprofil.koerper() for dd, p in teile if dd != "microprocessor")
    chips_vox = set()
    for mm in re.finditer(r'<microprocessor_definition name="([^"]*)"', s):
        chips_vox |= chip_flaeche(s, mm.group(1))
    belegt = teile_vox | chips_vox
    assert not (fl & belegt), ("Platz belegt", sorted(fl & belegt))
    vor = set((p[0] + R[1][0], p[1] + R[1][1], p[2] + R[1][2]) for p in fl)
    hinter = set((p[0] - R[1][0], p[1] - R[1][1], p[2] - R[1][2]) for p in fl)
    assert not (vor & belegt), ("unter dem Chip ist kein Raum", sorted(vor & belegt))
    assert hinter <= teile_vox, ("ueber dem Chip keine Decke", sorted(hinter - teile_vox))
    teil = '<c d="microprocessor"><o r="%s" bc="70787D" sc="%d">%s%s<logic_slots>%s</logic_slots></o></c>' % (
        R_, 2 * w * ln + 2 * (w + ln), d, u.vox("vp", VP), "<slot/>" * nk)
    _, e = u.mc_bereich(s, AP)
    s = s[:e] + teil + s[e:]
    ks = chip_knoten(s, SCH)
    print("Schotten %dx%d an der Decke %s: x %d..%d, z %d..%d" % (w, ln, VP, min(p[0] for p in fl), max(p[0] for p in fl),
                                                             min(p[2] for p in fl), max(p[2] for p in fl)))
    tl = kf.teile(s)

    def an(d_, vp, lab, mo_soll, ty_soll):
        p, mo, ty = kf.anschluss(tl, d_, vp, lab)
        assert mo == mo_soll and ty == ty_soll, (d_, vp, lab, mo, ty)
        return p
    li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
    alt_l = re.findall(LINKS, s[li:le])
    assert "".join(alt_l) == s[li:le]
    tueren_oc = set(an("door", vp, "Open/Close", 1, 0) for wd in bs.WAENDE for vp in wd[:2])
    weg = [x for x in alt_l if enden(x)[0] == ka["Schotten auf"] and enden(x)[1] in tueren_oc]
    assert len(weg) == 10, len(weg)
    bleibt = [x for x in alt_l if x not in weg]
    strom = an(BATT[0], BATT[1], "Electric Store", 1, 4)
    neu = [(0, ka["Schotten auf"], ks["Alle auf"], "Abteile 'Schotten auf' -> Schotten 'Alle auf'"),
           (5, ks["Zustand"], ka["Tueren"], "Schotten 'Zustand' -> Abteile 'Tueren'")]
    for k, wd in enumerate(bs.WAENDE):
        for vp in wd[:2]:
            neu.append((0, ks["Tueren Wand %d" % (k + 1)], an("door", vp, "Open/Close", 1, 0), "Wand %d -> Tuer %s" % (k + 1, vp)))
        neu.append((0, an("button_toggle_2side", wd[2], "Toggled", 0, 0), ks["Knopf Wand %d" % (k + 1)],
                    "Kippschalter %s -> Wand %d" % (wd[2], k + 1)))
        neu.append((4, strom, an("button_toggle_2side", wd[2], "Electric", 1, 4), "Strom -> Kippschalter %s" % (wd[2],)))
    belegte_eing = set((int(t or 0), p1) for t, p1 in re.findall(
        r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0[^>]*/>(<voxel_pos_1[^>]*/>)', "".join(bleibt)))
    zu = []
    for typ, p0, p1, was in neu:
        assert (typ, u.vox("voxel_pos_1", p1)) not in belegte_eing, ("Eingang schon belegt", was, p1)
        zu.append(link(typ, p0, p1))
        print("  %-48s %s -> %s" % (was, p0, p1))
    s = s[:li] + "".join(bleibt + zu) + s[le:]

    def ohne(x, neu_):
        a2, e2 = u.mc_bereich(x, AB)
        x = x[:a2] + x[e2:]
        if neu_:
            a2, e2 = u.mc_bereich(x, SCH)
            x = x[:a2] + x[e2:]
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0, False) == ohne(s, True), "ausser den Chips und Kabeln geaendert"
    print("Probe: Schotten-Chip neu, Abteile %s, %d Kabel weg, %d neu, sonst nichts" % (ba.VERSION, len(weg), len(zu)))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
