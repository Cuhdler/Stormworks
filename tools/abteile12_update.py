"""Abteile v1.2 + Lenzpumpen ins Schiff (Andre 08.10.: "eine Pumpe fuer die ganzen Abteile sollte reichen, der Schalter
'Auto water pumps' soll das automatische Pumpen aktivieren, wenn Wasser reinkommt; auf dem grossen Monitor soll immer
stehen, ob gerade gepumpt wird, wie viel und wie viel Wasser insgesamt schon rausgepumpt wurde"; "der Monitor ist
kopfueber"). Grundlage: Andres Stand 21:00 (Lenzleitung mit Pumpe (0,-4,-5); Abteile v1.0, Monitor ohne Drehangabe).
- Monitor 9x5 (8,21,-23): hatte keine Drehangabe = 0,0,1,-1,0,0,0,-1,0 (steht senkrecht an Steuerbord, Bild nach
  Backbord, kopfueber) -> 0,0,-1,-1,0,0,0,1,0 (180 Grad um die Bildachse, gleiche Flaeche)
- Chip "Figet Marena Abteile" 4x6 (-5,5,-58) raus, v1.2 4x8 an derselben Wand vp (-5,5,-59) (y 5..2, z -59..-52),
  Eigenschaften uebernommen
- Kabel des alten Abteil-Chips weg, alle neu; dazu Instrumentenblock 'Out Signal' -> 'Instrumente' (Bool 4 = Schalter
  'Auto water pumps'), Flow Rate der 3 Lenzpumpen -> 'Fluss 1-3', 'Pumpen' -> On/Off der 3 Lenzpumpen (die zwei alten
  bisher vom Schutz-Chip 'Pumpen' - diese 2 Kabel weg), Strom Batterie (-4,-13,-46) -> neue Pumpe
- Sammler: Fluid Capacity der Sensoren 17/18 (-1/1,-19,-61; ohne Drehangabe, Anschluss also bei x -2/2) neu - die
  Kabel vom 20:39-Stand zeigten auf die falsche Stelle, das Spiel hatte sie verworfen
Probe: ausser Monitor-Drehung, Abteil-Chip und Kabeln aendert sich nichts.
Aufruf: python abteile12_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
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
from flak_tauschen import werte, setze  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from autopilot_update import link, enden, chip_flaeche, flaeche, teil_bereich, BATT, LINKS  # noqa: E402

SA, AB = "Figet Marena Abteile Sammler", "Figet Marena Abteile"
VP, R_ = (-5, 5, -59), "0,-1,0,1,0,0,0,0,1"
MON = ("monitor_9", (8, 21, -23))
MON_R = "0,0,-1,-1,0,0,0,1,0"


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    assert 'description="Abteile v1.0' in s, "Abteile v1.0 nicht gefunden"
    tl = kf.teile(s)
    for k in [MON] + [("water_pump_large", p) for p in ba.PUMPEN]:
        assert len(tl.get(k, [])) == 1, ("Teil fehlt", k)
    # Monitor drehen (Teil ohne r)
    a, e = teil_bereich(s, *MON)
    assert s[a:e].startswith('<c d="monitor_9"><o sc='), s[a:e][:60]
    s = s[:a] + s[a:e].replace('<o sc=', '<o r="%s" sc=' % MON_R, 1) + s[e:]
    # alten Abteil-Chip raus (Eigenschaften und Anschluss-Lage merken)
    alt_kn = chip_knoten(s, AB)
    a, e = u.mc_bereich(s, AB)
    alt_w = werte(s[a:e])
    s = s[:a] + s[e:]
    u.CHIP = os.path.join(BUILD, "%s %s.xml" % (AB, ba.VERSION))
    d = u.chip_eingebettet()
    for n, v in alt_w.items():
        d = setze(d, n, v)
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
    voll = sorted(p for p in fl if p in belegt)
    assert not voll, ("Platz belegt", voll)
    vor = set((p[0] + R[1][0], p[1] + R[1][1], p[2] + R[1][2]) for p in fl)
    hinter = set((p[0] - R[1][0], p[1] - R[1][1], p[2] - R[1][2]) for p in fl)
    # vor dem Chip darf ein anderer Chip liegen (Ecke an der Rueckwand: Waffenwahl), aber kein anderes Teil
    assert not (vor & teile_vox), ("vor dem Chip ist kein Raum", sorted(vor & teile_vox))
    assert hinter <= belegt, ("hinter dem Chip keine Wand", sorted(hinter - belegt))
    teil = '<c d="microprocessor"><o r="%s" bc="70787D" sc="%d">%s%s<logic_slots>%s</logic_slots></o></c>' % (
        R_, 2 * w * ln + 2 * (w + ln), d, u.vox("vp", VP), "<slot/>" * nk)
    s = s[:a] + teil + s[a:]
    ka, ks = chip_knoten(s, AB), chip_knoten(s, SA)
    print("Abteile %s %dx%d bei %s (z %d..%d); Eigenschaften uebernommen: %s" % (
        ba.VERSION, w, ln, VP, min(p[2] for p in fl), max(p[2] for p in fl), sorted(alt_w)))
    tl = kf.teile(s)

    def an(d_, vp, lab, mo_soll, ty_soll):
        p, mo, ty = kf.anschluss(tl, d_, vp, lab)
        assert mo == mo_soll and ty == ty_soll, (d_, vp, lab, mo, ty)
        return p
    li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
    alt_l = re.findall(LINKS, s[li:le])
    assert "".join(alt_l) == s[li:le], "Kabelliste nicht vollstaendig erfasst"
    alte_pos = set(alt_kn.values())
    schutz = chip_knoten(s, "Figet Marena Schutz")
    pumpen_an = [an("water_pump_large", p, "On/Off", 1, 0) for p in ba.PUMPEN]
    instr = [enden(x)[0] for x in alt_l if enden(x)[1] == schutz["Instrumente"]]
    assert len(instr) == 1, instr
    weg = [x for x in alt_l if alte_pos & set(enden(x))]
    weg_schutz = [x for x in alt_l if enden(x)[0] == schutz["Pumpen"] and enden(x)[1] in pumpen_an]
    assert len(weg_schutz) == 2, weg_schutz
    bleibt = [x for x in alt_l if x not in weg and x not in weg_schutz]
    strom = an(BATT[0], BATT[1], "Electric Store", 1, 4)
    neu = []
    for k, vp in enumerate(ba.SENSOREN[:9]):
        neu.append((1, an("water_measure", vp, "Liquid Level", 0, 1), ka["Fuellstand %d" % (k + 1)], "Sensor %d" % (k + 1)))
        neu.append((1, an("water_measure", vp, "Fluid Capacity", 0, 1), ka["Kapazitaet %d" % (k + 1)], "Sensor %d" % (k + 1)))
    for k in (16, 17):
        vp = ba.SENSOREN[k]
        neu.append((1, an("water_measure", vp, "Fluid Capacity", 0, 1), ks["Kapazitaet %d" % (k + 1)],
                    "Sensor %d Kapazitaet -> Sammler" % (k + 1)))
    neu += [(5, ks["Abteile"], ka["Sammler"], "Sammler -> Abteile"),
            (5, an(*MON, "Touch Output", 0, 5), ka["Touch"], "Monitor 9x5 Touch -> Abteile"),
            (6, ka["Monitor"], an(*MON, "Video Signal", 1, 6), "Abteile -> Monitor 9x5 Video"),
            (0, ka["Monitor an"], an(*MON, "Power Switch", 1, 0), "Abteile -> Monitor 9x5 Power Switch"),
            (5, instr[0], ka["Instrumente"], "Instrumentenblock -> Abteile 'Instrumente'"),
            (4, strom, an("water_pump_large", ba.PUMPEN[0], "Electric", 1, 4), "Strom -> neue Lenzpumpe")]
    for k, p in enumerate(ba.PUMPEN):
        neu.append((1, an("water_pump_large", p, "Flow Rate", 0, 1), ka["Fluss %d" % (k + 1)], "Pumpe %s Flow Rate" % (p,)))
        neu.append((0, ka["Pumpen"], pumpen_an[k], "Abteile 'Pumpen' -> Pumpe %s On/Off" % (p,)))
    for vp in sorted(v for (dd, v) in tl if dd == "door"):
        neu.append((0, ka["Schotten auf"], an("door", vp, "Open/Close", 1, 0), "Schotten -> Tuer %s" % (vp,)))
    belegte_eing = set((int(t or 0), p1) for t, p1 in re.findall(
        r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0[^>]*/>(<voxel_pos_1[^>]*/>)', "".join(bleibt)))
    zu = []
    for typ, p0, p1, was in neu:
        assert (typ, u.vox("voxel_pos_1", p1)) not in belegte_eing, ("Eingang schon belegt", was, p1)
        zu.append(link(typ, p0, p1))
    for typ, p0, p1, was in neu[18:]:
        print("  %-48s %s -> %s" % (was, p0, p1))
    print("  Kabel weg: %d am alten Abteil-Chip, %d Schutz 'Pumpen' -> alte Pumpen" % (len(weg), len(weg_schutz)))
    s = s[:li] + "".join(bleibt + zu) + s[le:]

    # Probe
    def ohne(x, neu_):
        a2, e2 = u.mc_bereich(x, AB)
        x = x[:a2] + x[e2:]
        if neu_:
            x = x.replace('<c d="monitor_9"><o r="%s" sc=' % MON_R, '<c d="monitor_9"><o sc=', 1)
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0, False) == ohne(s, True), "ausser Monitor, Abteil-Chip und Kabeln geaendert"
    assert re.findall(LINKS, s[s.index("<logic_node_links>"):s.index("</logic_node_links>")]) == bleibt + zu
    print("Probe: Monitor gedreht, Abteil-Chip v1.2, %d Kabel weg, %d neu, sonst nichts" % (len(weg) + len(weg_schutz),
                                                                                           len(zu)))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
