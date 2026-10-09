"""Abteil-Anzeige ins Schiff (Andre 08.10.: "Liquid Meter und Schotten (elektrische Schiebetuer) sind eingebaut, der
andere grosse 9x5-Bildschirm soll fuer die Abteil-Anzeige sein"):
- Chip "Figet Marena Abteile Sammler" 4x5 an der rechten Wand des Chip-Raums unter Flak R: vp (5,2,-58), y 2..5,
  z -58..-54 (Drehung wie Flak R); Chip "Figet Marena Abteile" 4x6 an der linken Wand unter Flak L: vp (-5,5,-58),
  y 5..2, z -58..-53 (Drehung wie Flak L)
- Kabel: Liquid Meter 1-9 (Bughaelfte) Liquid Level / Fluid Capacity -> Abteile 'Fuellstand k' / 'Kapazitaet k',
  10-18 -> Sammler; Sammler 'Abteile' -> Abteile 'Sammler'; Monitor 9x5 (8,21,-23) Touch -> 'Touch', 'Monitor' ->
  Video, 'Monitor an' -> Power Switch; 'Schotten auf' -> Open/Close der 10 Schiebetueren
- Strom: Batterie (-4,-13,-46) -> Monitor 9x5 und die 10 Schiebetueren
Probe: ausser den zwei Chips und den Kabeln aendert sich nichts.
Aufruf: python abteile_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import sperrprofil  # noqa: E402
import build_abteile as ba  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from autopilot_update import link, chip_flaeche, flaeche, BATT, LINKS  # noqa: E402

SA, AB = "Figet Marena Abteile Sammler", "Figet Marena Abteile"
LAGE = {SA: ((5, 2, -58), "0,1,0,-1,0,0,0,0,1"), AB: ((-5, 5, -58), "0,-1,0,1,0,0,0,0,1")}
MON = ("monitor_9", (8, 21, -23))


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    for n in (SA, AB):
        assert '<microprocessor_definition name="%s"' % n not in s, (n, "schon eingebaut")
    tl = kf.teile(s)
    tueren = sorted(vp for (d, vp) in tl if d == "door")
    assert len(tueren) == 10, tueren
    for vp in ba.SENSOREN:
        assert len(tl.get(("water_measure", vp), [])) == 1, ("Liquid Meter fehlt", vp)
    assert len(tl.get(MON, [])) == 1, "Monitor 9x5 fehlt"
    belegt = set(p for teile in sperrprofil.koerper() for dd, p in teile if dd != "microprocessor")
    for mm in re.finditer(r'<microprocessor_definition name="([^"]*)"', s):
        belegt |= chip_flaeche(s, mm.group(1))
    teile = ""
    for n in (SA, AB):
        vp, r_ = LAGE[n]
        u.CHIP = os.path.join(BUILD, "%s %s.xml" % (n, ba.VERSION))
        d = u.chip_eingebettet()
        w = int(re.search(r'<microprocessor_definition [^>]*width="(\d+)"', d).group(1))
        ln = int(re.search(r'<microprocessor_definition [^>]*length="(\d+)"', d).group(1))
        nk = len(re.findall(r"<n id=", d))
        R = [[int(v) for v in r_.split(",")][i * 3:i * 3 + 3] for i in range(3)]
        fl = flaeche(R, vp, w, ln)
        voll = sorted(p for p in fl if p in belegt)
        assert not voll, ("Platz belegt", n, voll)
        vor = set((p[0] + R[1][0], p[1] + R[1][1], p[2] + R[1][2]) for p in fl)
        assert not (vor & belegt), ("vor dem Chip ist kein Raum", n, sorted(vor & belegt))
        belegt |= fl
        teile += '<c d="microprocessor"><o r="%s" bc="70787D" sc="%d">%s%s<logic_slots>%s</logic_slots></o></c>' % (
            r_, 2 * w * ln + 2 * (w + ln), d, u.vox("vp", vp), "<slot/>" * nk)
        print("%s %dx%d bei %s: y %d..%d, z %d..%d frei" % (n, w, ln, vp, min(p[1] for p in fl), max(p[1] for p in fl),
                                                         min(p[2] for p in fl), max(p[2] for p in fl)))
    _, e = u.mc_bereich(s, "Figet Marena Seeradar")
    s = s[:e] + teile + s[e:]
    ks, ka = chip_knoten(s, SA), chip_knoten(s, AB)
    tl = kf.teile(s)

    def an(d_, vp, lab, mo_soll, ty_soll):
        p, mo, ty = kf.anschluss(tl, d_, vp, lab)
        assert mo == mo_soll and ty == ty_soll, (d_, vp, lab, mo, ty)
        return p
    strom = an(BATT[0], BATT[1], "Electric Store", 1, 4)
    neu = []
    for k, vp in enumerate(ba.SENSOREN):
        ziel = ka if k < 9 else ks
        neu.append((1, an("water_measure", vp, "Liquid Level", 0, 1), ziel["Fuellstand %d" % (k + 1)], "Sensor %d" % (k + 1)))
        neu.append((1, an("water_measure", vp, "Fluid Capacity", 0, 1), ziel["Kapazitaet %d" % (k + 1)], "Sensor %d" % (k + 1)))
    neu += [(5, ks["Abteile"], ka["Sammler"], "Sammler -> Abteile"),
            (5, an(*MON, "Touch Output", 0, 5), ka["Touch"], "Monitor 9x5 Touch -> Abteile"),
            (6, ka["Monitor"], an(*MON, "Video Signal", 1, 6), "Abteile -> Monitor 9x5 Video"),
            (0, ka["Monitor an"], an(*MON, "Power Switch", 1, 0), "Abteile -> Monitor 9x5 Power Switch"),
            (4, strom, an(*MON, "Electric", 1, 4), "Strom -> Monitor 9x5")]
    for vp in tueren:
        neu.append((0, ka["Schotten auf"], an("door", vp, "Open/Close", 1, 0), "Schotten -> Tuer %s" % (vp,)))
        neu.append((4, strom, an("door", vp, "Electric", 1, 4), "Strom -> Tuer %s" % (vp,)))
    li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
    alt_l = re.findall(LINKS, s[li:le])
    assert "".join(alt_l) == s[li:le], "Kabelliste nicht vollstaendig erfasst"
    belegte_eing = set((int(t or 0), p1) for t, p1 in re.findall(
        r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0[^>]*/>(<voxel_pos_1[^>]*/>)', "".join(alt_l)))
    zu = []
    for typ, p0, p1, was in neu:
        assert (typ, u.vox("voxel_pos_1", p1)) not in belegte_eing, ("Eingang schon belegt", was, p1)
        zu.append(link(typ, p0, p1))
    for typ, p0, p1, was in neu[36:41]:
        print("  %-40s %s -> %s" % (was, p0, p1))
    print("  36 Sensor-Kabel, 10 Tueren (Open/Close + Strom) %s" % tueren)
    s = s[:li] + "".join(alt_l + zu) + s[le:]

    # Probe
    def ohne(x, neu_teile):
        if neu_teile:
            a2, _ = u.mc_bereich(x, SA)
            _, e2 = u.mc_bereich(x, AB)
            assert x[a2:e2] == teile
            x = x[:a2] + x[e2:]
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0, False) == ohne(s, True), "ausser den Abteil-Chips und Kabeln geaendert"
    assert re.findall(LINKS, s[s.index("<logic_node_links>"):s.index("</logic_node_links>")]) == alt_l + zu
    print("Probe: 2 Chips neu, %d Kabel neu, sonst nichts" % len(zu))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
