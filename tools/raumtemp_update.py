"""Chip "Figet Marena Raumtemperatur" 2x1 ins Schiff (Andre 10.10.: zwei Temperature Probes im Maschinenraum):
- an die Decke des Chip-Raums neben den Schotten-Chip: vp (-4,13,-50), Bild nach unten (x -4..-3, z -50)
- Kabel: Temperature der Probe (-2,-7,-82) -> 'Temperatur BB', der Probe (2,-7,-82) -> 'Temperatur SB'
Probe: ausser dem neuen Chip und 2 Kabeln aendert sich nichts.
Aufruf: python raumtemp_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import sperrprofil  # noqa: E402
import build_raumtemp as br  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from autopilot_update import link, chip_flaeche, flaeche  # noqa: E402

RT, NEBEN = "Figet Marena Raumtemperatur", "Figet Marena Schotten"
VP, R_ = (-4, 13, -50), "1,0,0,0,-1,0,0,0,-1"


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    assert '<microprocessor_definition name="%s"' % RT not in s0, "Raumtemperatur-Chip ist schon eingebaut"
    u.CHIP = os.path.join(BUILD, "%s %s.xml" % (RT, br.VERSION))
    d = u.chip_eingebettet()
    w = int(re.search(r'<microprocessor_definition [^>]*width="(\d+)"', d).group(1))
    ln = int(re.search(r'<microprocessor_definition [^>]*length="(\d+)"', d).group(1))
    nk = len(re.findall(r"<n id=", d))
    R = [[int(v) for v in R_.split(",")][i * 3:i * 3 + 3] for i in range(3)]
    fl = flaeche(R, VP, w, ln)
    teile_vox = set(p for teile in sperrprofil.koerper() for dd, p in teile if dd != "microprocessor")
    chips_vox = set()
    for mm in re.finditer(r'<microprocessor_definition name="([^"]*)"', s0):
        chips_vox |= chip_flaeche(s0, mm.group(1))
    belegt = teile_vox | chips_vox
    assert not (fl & belegt), ("Platz belegt", sorted(fl & belegt))
    vor = set((p[0] + R[1][0], p[1] + R[1][1], p[2] + R[1][2]) for p in fl)
    hinter = set((p[0] - R[1][0], p[1] - R[1][1], p[2] - R[1][2]) for p in fl)
    assert not (vor & belegt), ("unter dem Chip ist kein Raum", sorted(vor & belegt))
    assert hinter <= teile_vox, ("ueber dem Chip keine Decke", sorted(hinter - teile_vox))
    teil = '<c d="microprocessor"><o r="%s" bc="70787D" sc="%d">%s%s<logic_slots>%s</logic_slots></o></c>' % (
        R_, 2 * w * ln + 2 * (w + ln), d, u.vox("vp", VP), "<slot/>" * nk)
    _, e = u.mc_bereich(s0, NEBEN)
    s = s0[:e] + teil + s0[e:]
    kr = chip_knoten(s, RT)
    tl = kf.teile(s)
    neu = []
    for name, vp in br.SONDEN:
        p, mo, ty = kf.anschluss(tl, "temperature_probe", vp, "Temperature")
        assert (mo, ty) == (0, 1), (vp, mo, ty)
        neu.append(link(1, p, kr[name]))
        print("  Probe %s Temperature -> '%s'   %s -> %s" % (vp, name, p, kr[name]))
    le = s.index("</logic_node_links>")
    s = s[:le] + "".join(neu) + s[le:]

    def ohne(x, mit_chip):
        if mit_chip:
            a2, e2 = u.mc_bereich(x, RT)
            x = x[:a2] + x[e2:]
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0, False) == ohne(s, True), "ausser Chip und Kabeln geaendert"
    print("Probe: Chip %s %dx%d an der Decke %s, 2 Kabel neu, sonst nichts" % (RT, w, ln, VP))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
