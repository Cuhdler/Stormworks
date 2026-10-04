"""Auto-Chaff, Lenzpumpen, Knopf Zielkorrektur ins Schiff (Andre 04.10.: "die Zielkorrektur soll standardmaessig
deaktiviert sein und mit einem Knopf neben Master Arm (Instrumentenblock) aktiviert werden; Chaff hinzugefuegt, beide
Seiten gleichzeitig, du baust Auto-Chaff (der erste in jeder Reihe hat keinen Input; Radar Detector unter der Kamera),
an/aus ueber den anderen Flip Switch; Wasserpumpen eingebaut, die musst du verbinden"):
- Instrumentenblock (-2,19,-8): die vier Elemente schrieben alle auf Kanal 1 (ohne 'channel' = 0) - Master Arm bleibt
  Bool 1, 'Aim correction' -> Bool 2, 'Auto Chaff' -> Bool 3, 'Water Pumps' -> Bool 4
- Kamera-Chip v2.2 (neuer Eingang 'Instrumente': Korrektur nur mit Knopf an)
- neuer Chip "Figet Marena Schutz" (2 x 3) an der linken Wand des Chip-Raums neben dem BC-Chip: vp (-5, 13, -51),
  r 0,-1,0,1,0,0,0,0,1 -> Feld (x, z) = Welt (-5, 13-x, -51+z)
- Kabel: Instrumentenblock -> Kamera-Chip und Schutz-Chip; Radar Detector -> Schutz; Schutz -> Launch der ersten Werfer
  beider Ketten, -> On/Off beider Pumpen; Strom: linke/rechte Batterie -> linke/rechte Pumpe
Probe: ausser Kamera-Chip-Definition, Steckplaetzen, neuem Chip, Kanal-Angaben und diesen Kabeln aendert sich nichts.
Aufruf: python schutz_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import sperrprofil  # noqa: E402
import build_kamera  # noqa: E402
import build_schutz  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from waffen_update import tausche  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from zoom_update import chip_lage, flaeche  # noqa: E402

TAUSCH = [("Figet Marena Kamera", "Figet Marena Kamera %s.xml" % build_kamera.VERSION, {})]
VP, R_ = (-5, 13, -51), "0,-1,0,1,0,0,0,0,1"
PANEL = ("instrument_display", (-2, 19, -8))
RADAR = ("radar_detector", (0, 32, -13))
WERFER = {"Chaff links": ("flare_launcher", (-8, 17, -37)), "Chaff rechts": ("flare_launcher", (8, 17, -37))}
PUMPEN = [("water_pump_large", (-15, -19, -56), "L"), ("water_pump_large", (15, -19, -56), "R")]
KANAL = {2: 1, 3: 2, 4: 3}          # display_N -> channel (0-basiert: Bool N)


def link(typ, p0, p1):
    return "<logic_node_link%s>%s%s</logic_node_link>" % (' type="%d"' % typ if typ else "", u.vox("voxel_pos_0", p0),
                                                          u.vox("voxel_pos_1", p1))


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    assert '<microprocessor_definition name="Figet Marena Schutz"' not in s, "Schutz-Chip ist schon eingebaut"
    for name, datei, vorgabe in TAUSCH:
        s = tausche(s, name, datei, vorgabe)
    # 1. Instrumentenblock: Kanaele
    m = re.search(r'<c d="instrument_display"><o [^>]*>%s' % re.escape(u.vox("vp", PANEL[1])), s)
    a, e = m.start(), s.index("</c>", m.start())
    teil = s[a:e]
    for n, ch in KANAL.items():
        mm = re.search(r'<display_%d ([^>]*)>' % n, teil)
        assert mm and "channel=" not in mm.group(1), ("display", n, mm and mm.group(1))
        teil = teil.replace(mm.group(0), '<display_%d %s channel="%d">' % (n, mm.group(1), ch))
        print("Instrumentenblock display_%d (%s) -> Bool %d" % (n, re.search(r'name="([^"]*)"', mm.group(1)).group(1), ch + 1))
    s = s[:a] + teil + s[e:]
    # 2. Schutz-Chip einsetzen (Flaeche frei?)
    u.CHIP = os.path.join(BUILD, "Figet Marena Schutz %s.xml" % build_schutz.VERSION)
    d = u.chip_eingebettet()
    w = int(re.search(r'<microprocessor_definition [^>]*width="(\d+)"', d).group(1))
    ln = int(re.search(r'<microprocessor_definition [^>]*length="(\d+)"', d).group(1))
    nk = len(re.findall(r"<n id=", d))
    R = [[int(v) for v in R_.split(",")][i * 3:i * 3 + 3] for i in range(3)]
    fl = flaeche(R, VP, w, ln)
    belegt = set(p for teile in sperrprofil.koerper() for dd, p in teile if dd != "microprocessor")
    for mm in re.finditer(r'<microprocessor_definition name="([^"]*)"', s):
        try:
            _, R2, vp2, w2, l2, _ = chip_lage(s, mm.group(1))
        except (ValueError, AttributeError):
            continue
        belegt |= flaeche(R2, vp2, w2, l2)
    voll = sorted(p for p in fl if p in belegt)
    assert not voll, ("Platz fuer den Schutz-Chip belegt", voll)
    chip = '<c d="microprocessor"><o r="%s" sc="%d">%s%s<logic_slots>%s</logic_slots></o></c>' % (
        R_, 2 * w * ln + 2 * (w + ln), d, u.vox("vp", VP), "<slot/>" * nk)
    i0, e0 = s.index("<bodies>"), s.index("</bodies>")
    koerper, a = [], s.index("<body ", i0)
    while 0 <= a < e0:
        e = s.index("</body>", a)
        koerper.append((a, e))
        a = s.find("<body ", e)
    rumpf = max(koerper, key=lambda q: s.count('<c d="', q[0], q[1]))
    einfueg = s.rindex("</components>", rumpf[0], rumpf[1])
    s = s[:einfueg] + chip + s[einfueg:]
    print("Schutz-Chip %d x %d eingesetzt: vp %s, Flaeche %s frei" % (w, ln, VP, sorted(fl)))
    # 3. Kabel
    tl = kf.teile(s)
    sc, kc = chip_knoten(s, "Figet Marena Schutz"), chip_knoten(s, "Figet Marena Kamera")

    def an(dd, vp, lab, mo_soll, ty_soll):
        p, mo, ty = kf.anschluss(tl, dd, vp, lab)
        assert mo == mo_soll and ty == ty_soll, (dd, vp, lab, mo, ty)
        return p
    li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
    alt = re.findall(r"<logic_node_link[ >].*?</logic_node_link>", s[li:le])
    assert "".join(alt) == s[li:le], "Kabelliste nicht vollstaendig erfasst"
    panel = an(*PANEL, "Out Signal", 0, 5)
    neu = [(5, panel, kc["Instrumente"], "Instrumentenblock -> Kamera-Chip Instrumente"),
           (5, panel, sc["Instrumente"], "Instrumentenblock -> Schutz Instrumente"),
           (0, an(*RADAR, "Detected", 0, 0), sc["Radarwarner"], "Radar Detector -> Schutz Radarwarner")]
    for lab, (dd, vp) in WERFER.items():
        neu.append((0, sc[lab], an(dd, vp, "Launch", 1, 0), "Schutz %s -> erster Werfer %s" % (lab, vp)))
    for dd, vp, sd in PUMPEN:
        neu.append((0, sc["Pumpen"], an(dd, vp, "On/Off", 1, 0), "Schutz Pumpen -> Pumpe %s" % (vp,)))
        neu.append((4, an(*kf.BATT[sd], "Electric Store", 1, 4), an(dd, vp, "Electric", 1, 4),
                    "Strom Batterie %s -> Pumpe %s" % (sd, vp)))
    belegte_eing = set((int(t or 0), p1) for t, p1 in re.findall(
        r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0[^>]*/>(<voxel_pos_1[^>]*/>)', "".join(alt)))
    zu = []
    for typ, p0, p1, was in neu:
        assert (typ, u.vox("voxel_pos_1", p1)) not in belegte_eing, ("Eingang schon belegt", was, p1)
        zu.append(link(typ, p0, p1))
        print("  %-62s %s -> %s" % (was, p0, p1))
    s = s[:le] + "".join(zu) + s[le:]
    print("Kabel vorher %d, neu %d" % (len(alt), len(zu)))
    # Probe
    namen = "|".join(re.escape(n) for n, _, _ in TAUSCH)

    def ohne(x):
        x = re.sub(r'<microprocessor_definition name="(%s)".*?</microprocessor_definition>' % namen, "", x, flags=re.S)
        x = re.sub(r"<logic_slots>(<slot(?: editor_connected=\"1\")?/>)*</logic_slots>", "<logic_slots/>", x)
        x = re.sub(r'<c d="microprocessor"><o [^>]*><microprocessor_definition name="Figet Marena Schutz".*?</o></c>', "", x,
                   flags=re.S)
        x = re.sub(r'(<display_[234] [^>]*?) channel="[123]">', r"\1>", x)
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0) == ohne(s), "ausser Chips, Kanaelen und Kabeln geaendert"
    k0 = re.findall(r"<logic_node_link[ >].*?</logic_node_link>", s0[s0.index("<logic_node_links>"):s0.index("</logic_node_links>")])
    k1 = re.findall(r"<logic_node_link[ >].*?</logic_node_link>", s[s.index("<logic_node_links>"):s.index("</logic_node_links>")])
    assert k1[:len(k0)] == k0 and k1[len(k0):] == zu, "andere Kabel veraendert"
    print("Probe: Kamera-Chip, Schutz-Chip neu, 3 Kanal-Angaben, %d neue Kabel" % len(zu))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
