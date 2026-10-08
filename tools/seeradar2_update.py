"""Seeradar v2.0 ins Schiff (Andre 06.10.: "alle Zoom-Stufen automatisch; beim 3D-Radar nur von Seezielen, beim 2D-Radar
von Boden- und Seezielen ausgeloest, nie Punkte zu nah aneinander; tippt man auf dem 2D-Radar ein See- oder Landziel an,
waehrend eine der vorderen Kanonen gewaehlt ist, zielt/schiesst diese 20 s darauf, dann wieder Automatik; ohne Kanone
gehen X/Y-Koordinaten an 2 Zahl-Ausgaenge und an den Monitor 1x2"):
- Bildschirm v3.6 (Zoom 1/2,5/5/10 km selbst, nur Seeziele), Flak L/R v2.9 und Kanone BC/AC v1.7 (Bodenziel: Radar-Hoehe
  statt 'Ziel Hoehe fest m') - nur die Chip-Definitionen getauscht (Anschluesse gleich)
- Seeradar v2.0: Chip waechst von 2x3 auf 4x3 (gleiche Stelle vp (0,6,-59), alte Anschluesse an derselben Lage, neue
  Felder x 2..3 frei) - Bauteil neu, Eigenschaften uebernommen
- Kabel: Bildschirm 'Bedienung' -> Seeradar 'Bedienung ein'; Seeradar 'Bedienung aus' -> Kanone BC / AC 'Lage' und
  Kamera 'Bedienung' (statt direkt vom Bildschirm); Seeradar 'Monitor 1x2' -> Monitor 1x2 (0,19,-8) Video Signal,
  'Monitor 1x2 an' -> dessen Power Switch. 'Ziel X' / 'Ziel Y' bleiben frei.
Probe: ausser diesen Chips und Kabeln aendert sich nichts.
Aufruf: python seeradar2_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import sperrprofil  # noqa: E402
import build_seeradar  # noqa: E402
import build_lage  # noqa: E402
import build_flak  # noqa: E402
import build_kanone  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from waffen_update import tausche  # noqa: E402
from flak_tauschen import werte, setze  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from zoom_update import chip_lage, flaeche  # noqa: E402

SR = "Figet Marena Seeradar"
TAUSCH = [("Figet Marena Bildschirm", "Figet Marena Bildschirm %s.xml" % build_lage.VERSION_BILD),
          ("Figet Marena Flak L", "Figet Marena Flak L %s.xml" % build_flak.VERSION),
          ("Figet Marena Flak R", "Figet Marena Flak R %s.xml" % build_flak.VERSION),
          ("Figet Marena Kanone BC", "Figet Marena Kanone BC %s.xml" % build_kanone.VERSION),
          ("Figet Marena Kanone AC", "Figet Marena Kanone AC %s.xml" % build_kanone.VERSION)]
VP, R_ = (0, 6, -59), "1,0,0,0,0,1,0,-1,0"
M12 = ("monitor_1x2", (0, 19, -8))
LINKS = r"<logic_node_link[ >].*?</logic_node_link>"


def link(typ, p0, p1):
    return "<logic_node_link%s>%s%s</logic_node_link>" % (' type="%d"' % typ if typ else "", u.vox("voxel_pos_0", p0),
                                                          u.vox("voxel_pos_1", p1))


def enden(x):
    return [u.xyz(v) for v in re.findall(r"<voxel_pos_\d([^/]*)/>", x)]


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    assert 'description="Seeradar v2' not in s, "Seeradar v2 ist schon eingebaut"
    for name, datei in TAUSCH:
        s = tausche(s, name, datei, {})
    # Seeradar: Bauteil neu (4x3), Eigenschaften uebernehmen
    alt_kn = chip_knoten(s, SR)
    a, e = u.mc_bereich(s, SR)
    teil = s[a:e]
    alt_w = werte(teil[teil.index("<microprocessor_definition"):teil.index("</microprocessor_definition>") + 28])
    u.CHIP = os.path.join(BUILD, "%s %s.xml" % (SR, build_seeradar.VERSION))
    d = u.chip_eingebettet()
    neu_w = werte(d)
    for n, v in alt_w.items():
        if n in neu_w:
            d = setze(d, n, v)
    print("Seeradar-Eigenschaften uebernommen: %s; neu: %s; weg: %s" % (
        sorted(n for n in alt_w if n in neu_w), sorted(set(neu_w) - set(alt_w)), sorted(set(alt_w) - set(neu_w))))
    w = int(re.search(r'<microprocessor_definition [^>]*width="(\d+)"', d).group(1))
    ln = int(re.search(r'<microprocessor_definition [^>]*length="(\d+)"', d).group(1))
    nk = len(re.findall(r"<n id=", d))
    s = s[:a] + s[e:]
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
    neu_teil = '<c d="microprocessor"><o r="%s" sc="%d">%s%s<logic_slots>%s</logic_slots></o></c>' % (
        R_, 2 * w * ln + 2 * (w + ln), d, u.vox("vp", VP), "<slot/>" * nk)
    s = s[:a] + neu_teil + s[a:]
    sk = chip_knoten(s, SR)
    for lab, p in alt_kn.items():
        assert sk[lab] == p, ("Anschluss verschoben", lab, p, sk[lab])
    print("Seeradar %d x %d eingesetzt: vp %s, Flaeche %s frei" % (w, ln, VP, sorted(fl)))
    # Kabel
    tl = kf.teile(s)

    def an(dd, vp, lab, mo_soll, ty_soll):
        p, mo, ty = kf.anschluss(tl, dd, vp, lab)
        assert mo == mo_soll and ty == ty_soll, (dd, vp, lab, mo, ty)
        return p
    bed = chip_knoten(s, "Figet Marena Bildschirm")["Bedienung"]
    ziele = [chip_knoten(s, "Figet Marena Kanone BC")["Lage"], chip_knoten(s, "Figet Marena Kanone AC")["Lage"],
             chip_knoten(s, "Figet Marena Kamera")["Bedienung"]]
    li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
    alt = re.findall(LINKS, s[li:le])
    assert "".join(alt) == s[li:le], "Kabelliste nicht vollstaendig erfasst"
    weg = [x for x in alt if enden(x)[0] == bed and enden(x)[1] in ziele]
    assert len(weg) == 3, ("Kabel Bildschirm -> BC/AC/Kamera", weg)
    bleibt = [x for x in alt if x not in weg]
    neu = [(5, bed, sk["Bedienung ein"], "Bildschirm Bedienung -> Seeradar"),
           (5, sk["Bedienung aus"], ziele[0], "Seeradar Bedienung -> Kanone BC 'Lage'"),
           (5, sk["Bedienung aus"], ziele[1], "Seeradar Bedienung -> Kanone AC 'Lage'"),
           (5, sk["Bedienung aus"], ziele[2], "Seeradar Bedienung -> Kamera 'Bedienung'"),
           (6, sk["Monitor 1x2"], an(*M12, "Video Signal", 1, 6), "Seeradar -> Monitor 1x2 Video"),
           (0, sk["Monitor 1x2 an"], an(*M12, "Power Switch", 1, 0), "Seeradar -> Monitor 1x2 Power Switch")]
    belegte_eing = set((int(t or 0), p1) for t, p1 in re.findall(
        r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0[^>]*/>(<voxel_pos_1[^>]*/>)', "".join(bleibt)))
    zu = []
    for typ, p0, p1, was in neu:
        assert (typ, u.vox("voxel_pos_1", p1)) not in belegte_eing, ("Eingang schon belegt", was, p1)
        zu.append(link(typ, p0, p1))
        print("  %-45s %s -> %s" % (was, p0, p1))
    for x in weg:
        print("  Kabel weg: %s" % x)
    s = s[:li] + "".join(bleibt + zu) + s[le:]
    # Probe
    namen = "|".join(re.escape(n) for n, _ in TAUSCH)

    def ohne(x):
        a2, e2 = u.mc_bereich(x, SR)
        x = x[:a2] + x[e2:]
        x = re.sub(r'<microprocessor_definition name="(%s)".*?</microprocessor_definition>' % namen, "", x, flags=re.S)
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0) == ohne(s), "ausser Chips und Kabeln geaendert"
    assert re.findall(LINKS, s[s.index("<logic_node_links>"):s.index("</logic_node_links>")]) == bleibt + zu
    print("Probe: 5 Chips getauscht, Seeradar 4x3 neu, %d Kabel weg, %d neu, sonst nichts" % (len(weg), len(zu)))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
