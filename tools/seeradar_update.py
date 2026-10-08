"""Seeradar ins Schiff (Andre 06.10.: "die restlichen Funktionen muessen ohne Radar 6 weiterkommen; mach, dass Radar 6
auf dem 3x3-Bildschirm ein 2D-Radar macht - nur Boden- und Seeziele, mit dem Strich und dem Verblassen"):
- alter Raketen-Chip "Figet Marena Raketen" (3x3, vp (0,6,-59)) samt seinen Kabeln raus
- Kabel Lage 'Gimbal 6' -> Radar 6 Gimbal Input raus (Radar 6 gehoert jetzt dem Seeradar; die Lage bekommt seit der
  Raketen-Fassung keine Daten von Radar 6 mehr, Platz 5 wurde nie vergeben)
- neuer Chip "Figet Marena Seeradar" (2x3) an derselben Stelle: vp (0,6,-59), r 1,0,0,0,0,1,0,-1,0
  -> Feld (x, z) = Welt (x, 6-z, -59)
- Kabel: Radar 6 Radar Data -> Seeradar; Physik-Sensor -> Seeradar; Monitor 3x3 Touch -> Seeradar;
  Seeradar Gimbal -> Radar 6 Gimbal Input; Seeradar Monitor -> Monitor 3x3 Video Signal
Bleiben: Strom von Radar 6 und Monitor, Andres Kabel Sitz 'Occupied' -> Monitor 'Power Switch', Radar 'Activate'.
Probe: ausser den zwei Chips und diesen Kabeln aendert sich nichts.
Aufruf: python seeradar_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import sperrprofil  # noqa: E402
import build_seeradar  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from zoom_update import chip_lage, flaeche  # noqa: E402

ALT = "Figet Marena Raketen"
NEU = "Figet Marena Seeradar"
VP, R_ = (0, 6, -59), "1,0,0,0,0,1,0,-1,0"
RADAR = ("radar_advanced_phalanx", (5, 36, -51))
MONITOR = ("monitor_3", (-3, 20, -10))
LINKS = r"<logic_node_link[ >].*?</logic_node_link>"


def link(typ, p0, p1):
    return "<logic_node_link%s>%s%s</logic_node_link>" % (' type="%d"' % typ if typ else "", u.vox("voxel_pos_0", p0),
                                                          u.vox("voxel_pos_1", p1))


def enden(x):
    return [u.xyz(v) for v in re.findall(r"<voxel_pos_\d([^/]*)/>", x)]


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    assert '<microprocessor_definition name="%s"' % NEU not in s, "Seeradar ist schon eingebaut"
    tl = kf.teile(s)

    def an(dd, vp, lab, mo_soll, ty_soll):
        p, mo, ty = kf.anschluss(tl, dd, vp, lab)
        assert mo == mo_soll and ty == ty_soll, (dd, vp, lab, mo, ty)
        return p
    gimbal6 = an(*RADAR, "Gimbal Input", 1, 5)
    lage_g6 = chip_knoten(s, "Figet Marena Lage")["Gimbal 6"]
    alt_kn = set(chip_knoten(s, ALT).values())
    # 1. alten Raketen-Chip raus
    a, e = u.mc_bereich(s, ALT)
    s = s[:a] + s[e:]
    # 2. Kabel: die des alten Chips und Lage Gimbal 6 -> Radar 6 raus
    li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
    alt = re.findall(LINKS, s[li:le])
    assert "".join(alt) == s[li:le], "Kabelliste nicht vollstaendig erfasst"
    weg = [x for x in alt if set(enden(x)) & alt_kn or enden(x) == [lage_g6, gimbal6]]
    assert sum(1 for x in weg if enden(x) == [lage_g6, gimbal6]) == 1, "Kabel Lage Gimbal 6 -> Radar 6 nicht gefunden"
    for x in weg:
        print("  Kabel weg: %s" % x)
    bleibt = [x for x in alt if x not in weg]
    # 3. Seeradar-Chip einsetzen (Flaeche frei?)
    u.CHIP = os.path.join(BUILD, "%s %s.xml" % (NEU, build_seeradar.VERSION))
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
    assert not voll, ("Platz fuer das Seeradar belegt", voll)
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
    print("Seeradar-Chip %d x %d eingesetzt: vp %s, Flaeche %s frei" % (w, ln, VP, sorted(fl)))
    # 4. neue Kabel
    sk = chip_knoten(s, NEU)
    neu = [(5, an(*RADAR, "Radar Data", 0, 5), sk["Radar"], "Radar 6 Radar Data -> Seeradar"),
           (5, an(*kf.PHYSIK, 0, 5), sk["Physik-Sensor"], "Physik-Sensor -> Seeradar"),
           (5, an(*MONITOR, "Touch Output", 0, 5), sk["Touch"], "Monitor 3x3 Touch -> Seeradar"),
           (5, sk["Gimbal"], gimbal6, "Seeradar Gimbal -> Radar 6 Gimbal Input"),
           (6, sk["Monitor"], an(*MONITOR, "Video Signal", 1, 6), "Seeradar -> Monitor 3x3 Video")]
    belegte_eing = set((int(t or 0), p1) for t, p1 in re.findall(
        r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0[^>]*/>(<voxel_pos_1[^>]*/>)', "".join(bleibt)))
    zu = []
    for typ, p0, p1, was in neu:
        assert (typ, u.vox("voxel_pos_1", p1)) not in belegte_eing, ("Eingang schon belegt", was, p1)
        zu.append(link(typ, p0, p1))
        print("  %-45s %s -> %s" % (was, p0, p1))
    li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
    s = s[:li] + "".join(bleibt + zu) + s[le:]
    print("Kabel vorher %d, weg %d, neu %d" % (len(alt), len(weg), len(zu)))
    # Probe: ohne die beiden Chips und die Kabelliste gleich
    def ohne(x):
        for name in (ALT, NEU):
            if '<microprocessor_definition name="%s"' % name in x:
                a, e = u.mc_bereich(x, name)
                x = x[:a] + x[e:]
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0) == ohne(s), "ausser Chips und Kabeln geaendert"
    k1 = re.findall(LINKS, s[s.index("<logic_node_links>"):s.index("</logic_node_links>")])
    assert k1 == bleibt + zu
    assert s.count("<microprocessor_definition ") == s0.count("<microprocessor_definition ")
    print("Probe: alter Raketen-Chip raus, Seeradar rein, %d Kabel weg, %d neu, sonst nichts" % (len(weg), len(zu)))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
