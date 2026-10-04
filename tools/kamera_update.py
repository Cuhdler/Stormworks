"""Dachkamera + Lage v3.3 + Turm-Radar v2.3 ins Schiff (Andre 04.10. ~14:40: "ein sehr tief fliegender Eurofighter und
ein Hubschrauber wurden als Schiff von AC und BC beschossen; bei schneller Eigenfahrt haben BC und AC leicht verzogen;
die Kamera hat nicht gut funktioniert, da die Kanonen vorzielen - eine bewegliche Kamera auf dem Dach fuer alle Waffen,
habe sie platziert (Camera Stabilized (0,33,-15)), sie schaut am Anfang 90 Grad nach oben"):
- Chips tauschen (Lage v3.3, Flak L/R v2.7, Bildschirm v3.3, Kanone BC/AC v1.5)
- neuer Chip "Figet Marena Kamera" (4 x 5) an der rechten Wand des Chip-Raums neben dem AC-Chip: vp (5, 10, -53),
  r 0,1,0,-1,0,0,0,0,1 -> Feld (x, z) = Welt (5, 10+x, -53+z)
- Kabel: Bildschirm 'Bedienung' -> Kamera-Chip; Physik-Sensor -> Kamera-Chip; Dachkamera Composite Output / Laser
  Distance -> Kamera-Chip; Kamera-Chip Drehung/Neigung/Zoom/Laser an -> Dachkamera; Strom (linke Batterie) ->
  Dachkamera; Video: die vier Turm-Kameras -> Bildschirm-Chip raus, Dachkamera -> alle vier Kamera-Eingaenge
Probe: ausser Chip-Definitionen, Steckplaetzen, dem neuen Chip und diesen Kabeln aendert sich nichts.
Aufruf: python kamera_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import sperrprofil  # noqa: E402
import build_kamera  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from kanone_update import TAUSCH  # noqa: E402
from waffen_update import tausche  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from zoom_update import chip_lage, flaeche  # noqa: E402

DACH = ("camera_gimbal_laser", (0, 33, -15))
VP, R_ = (5, 10, -53), "0,1,0,-1,0,0,0,0,1"
TURM_KAM = [("camera_med", (4, 19, 11), "Kamera BC"), ("camera_med", (-4, 9, 35), "Kamera AC vorn"),
            ("camera_med", (-15, 20, -99), "Kamera Flak L"), ("camera_med", (15, 20, -99), "Kamera Flak R")]


def link(typ, p0, p1):
    return "<logic_node_link%s>%s%s</logic_node_link>" % (' type="%d"' % typ if typ else "", u.vox("voxel_pos_0", p0),
                                                          u.vox("voxel_pos_1", p1))


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    assert '<microprocessor_definition name="Figet Marena Kamera"' not in s, "Kamera-Chip ist schon eingebaut"
    for name, datei, vorgabe in TAUSCH:
        s = tausche(s, name, datei, vorgabe)
    # 1. Kamera-Chip einsetzen (Flaeche frei? alle Teile ausser Microcontrollern + alle Chips)
    u.CHIP = os.path.join(BUILD, "Figet Marena Kamera %s.xml" % build_kamera.VERSION)
    d = u.chip_eingebettet()
    w = int(re.search(r'<microprocessor_definition [^>]*width="(\d+)"', d).group(1))
    ln = int(re.search(r'<microprocessor_definition [^>]*length="(\d+)"', d).group(1))
    nk = len(re.findall(r"<n id=", d))
    R = [[int(v) for v in R_.split(",")][i * 3:i * 3 + 3] for i in range(3)]
    fl = flaeche(R, VP, w, ln)
    belegt = set(p for teile in sperrprofil.koerper() for dd, p in teile if dd != "microprocessor")
    for m in re.finditer(r'<microprocessor_definition name="([^"]*)"', s):
        try:
            _, R2, vp2, w2, l2, _ = chip_lage(s, m.group(1))
        except (ValueError, AttributeError):
            continue
        belegt |= flaeche(R2, vp2, w2, l2)
    voll = sorted(p for p in fl if p in belegt)
    assert not voll, ("Platz fuer den Kamera-Chip belegt", voll)
    teil = '<c d="microprocessor"><o r="%s" sc="%d">%s%s<logic_slots>%s</logic_slots></o></c>' % (
        R_, 2 * w * ln + 2 * (w + ln), d, u.vox("vp", VP), "<slot/>" * nk)
    i0, e0 = s.index("<bodies>"), s.index("</bodies>")
    koerper, a = [], s.index("<body ", i0)
    while 0 <= a < e0:
        e = s.index("</body>", a)
        koerper.append((a, e))
        a = s.find("<body ", e)
    rumpf = max(koerper, key=lambda q: s.count('<c d="', q[0], q[1]))
    einfueg = s.rindex("</components>", rumpf[0], rumpf[1])
    s = s[:einfueg] + teil + s[einfueg:]
    print("Kamera-Chip %d x %d eingesetzt: vp %s, Flaeche %s frei" % (w, ln, VP, sorted(fl)))
    # 2. Kabel
    tl = kf.teile(s)
    kc = chip_knoten(s, "Figet Marena Kamera")
    bild = chip_knoten(s, "Figet Marena Bildschirm")

    def an(dd, vp, lab, mo_soll, ty_soll):
        p, mo, ty = kf.anschluss(tl, dd, vp, lab)
        assert mo == mo_soll and ty == ty_soll, (dd, vp, lab, mo, ty)
        return p
    li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
    alt = re.findall(r"<logic_node_link[ >].*?</logic_node_link>", s[li:le])
    assert "".join(alt) == s[li:le], "Kabelliste nicht vollstaendig erfasst"
    neu = [(5, bild["Bedienung"], kc["Bedienung"], "Bildschirm 'Bedienung' -> Kamera-Chip"),
           (5, an(*kf.PHYSIK, 0, 5), kc["Physik-Sensor"], "Physik-Sensor -> Kamera-Chip"),
           (5, an(*DACH, "Composite Output", 0, 5), kc["Kamera Daten"], "Dachkamera Composite -> Kamera-Chip"),
           (1, an(*DACH, "Laser Distance", 0, 1), kc["Laser Entfernung"], "Dachkamera Laser Distance -> Kamera-Chip"),
           (1, kc["Drehung"], an(*DACH, "Pivot Rotation", 1, 1), "Kamera-Chip Drehung -> Pivot Rotation"),
           (1, kc["Neigung"], an(*DACH, "Pitch Rotation", 1, 1), "Kamera-Chip Neigung -> Pitch Rotation"),
           (1, kc["Zoom"], an(*DACH, "Field of View", 1, 1), "Kamera-Chip Zoom -> Field of View"),
           (0, kc["Laser an"], an(*DACH, "Enable Laser", 1, 0), "Kamera-Chip Laser an -> Enable Laser"),
           (4, an(*kf.BATT["L"], "Electric Store", 1, 4), an(*DACH, "Electric", 1, 4), "Strom linke Batterie -> Dachkamera")]
    feed = an(*DACH, "Camera Feed", 0, 6)
    weg = []
    for dd, vp, lab in TURM_KAM:
        k = link(6, an(dd, vp, "Camera Feed", 0, 6), bild[lab])
        assert alt.count(k) == 1, ("Video-Kabel nicht genau einmal", lab, alt.count(k))
        weg.append(k)
        neu.append((6, feed, bild[lab], "Dachkamera Video -> Bildschirm '%s' (statt Turm-Kamera)" % lab))
    belegte_eing = set((int(t or 0), p1) for t, p1 in re.findall(
        r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0[^>]*/>(<voxel_pos_1[^>]*/>)', "".join(k for k in alt if k not in weg)))
    zu = []
    for typ, p0, p1, was in neu:
        assert (typ, u.vox("voxel_pos_1", p1)) not in belegte_eing, ("Eingang schon belegt", was, p1)
        zu.append(link(typ, p0, p1))
        print("  %-66s %s -> %s" % (was, p0, p1))
    rest = [k for k in alt if k not in weg]
    s = s[:li] + "".join(rest + zu) + s[le:]
    assert s.count("<logic_node_links>") == 1
    print("Kabel vorher %d, weg %d, neu %d" % (len(alt), len(weg), len(zu)))
    # Probe
    namen = "|".join(re.escape(n) for n, _, _ in TAUSCH)

    def ohne(x):
        x = re.sub(r'<microprocessor_definition name="(%s)".*?</microprocessor_definition>' % namen, "", x, flags=re.S)
        x = re.sub(r"<logic_slots>(<slot(?: editor_connected=\"1\")?/>)*</logic_slots>", "<logic_slots/>", x)
        x = re.sub(r'<c d="microprocessor"><o [^>]*><microprocessor_definition name="Figet Marena Kamera".*?</o></c>', "", x,
                   flags=re.S)
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0) == ohne(s), "ausser Chips und Kabeln geaendert"
    k0 = re.findall(r"<logic_node_link[ >].*?</logic_node_link>", s0[s0.index("<logic_node_links>"):s0.index("</logic_node_links>")])
    k1 = re.findall(r"<logic_node_link[ >].*?</logic_node_link>", s[s.index("<logic_node_links>"):s.index("</logic_node_links>")])
    assert [k for k in k0 if k not in weg] == k1[:len(k0) - len(weg)] and k1[len(k0) - len(weg):] == zu, "andere Kabel veraendert"
    print("Probe: nur %d Chip-Definitionen, Kamera-Chip neu, %d Kabel weg, %d neu" % (len(TAUSCH), len(weg), len(zu)))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
