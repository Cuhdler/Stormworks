"""Korrektur per Blick ins Schiff (Andre 04.10.: "Korrektur bei ausgewaehlter Waffe: je weiter die Sicht vom Fadenkreuz
weg, desto weiter korrigiert er in die Richtung - wie beim Swifter, nur wenn der Mittelpunkt meines Sichtfelds in einem
kleinen Kreis um das Fadenkreuz ist"; wie ein Joystick, bleibt):
- Chips tauschen (Flak L/R v2.8, Kanone BC/AC v1.6: neuer Eingang 'Korrektur'; Kamera v2.0: neue Anschluesse 'Sitz',
  'Video ein', 'Video aus', 'Korrektur'; Lage/Bildschirm wie bisher)
- Kabel: Kamera-Chip 'Korrektur' -> 'Korrektur' der 4 Turm-Chips; Sitz 'Seat data' -> Kamera-Chip 'Sitz'; Video:
  Dachkamera -> Kamera-Chip 'Video ein' (zeichnet Kreis und Marke), Kamera-Chip 'Video aus' -> die 4 Kamera-Eingaenge
  des Bildschirm-Chips (statt Dachkamera direkt)
Probe: ausser Chip-Definitionen, Steckplaetzen und diesen Kabeln aendert sich nichts.
Aufruf: python korrektur_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import build_kamera  # noqa: E402
from kanone_update import TAUSCH as T0  # noqa: E402
from waffen_update import tausche  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402

TAUSCH = T0 + [("Figet Marena Kamera", "Figet Marena Kamera %s.xml" % build_kamera.VERSION, {})]
DACH = ("camera_gimbal_laser", (0, 33, -15))
SITZ = ("seat_compact", (0, 17, -10))
TUERME = ["Figet Marena Kanone BC", "Figet Marena Kanone AC", "Figet Marena Flak L", "Figet Marena Flak R"]
BILD_KAM = ["Kamera BC", "Kamera AC vorn", "Kamera Flak L", "Kamera Flak R"]


def link(typ, p0, p1):
    return "<logic_node_link%s>%s%s</logic_node_link>" % (' type="%d"' % typ if typ else "", u.vox("voxel_pos_0", p0),
                                                          u.vox("voxel_pos_1", p1))


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    for name, datei, vorgabe in TAUSCH:
        s = tausche(s, name, datei, vorgabe)
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
    feed = an(*DACH, "Camera Feed", 0, 6)
    neu = [(5, kc["Korrektur"], chip_knoten(s, t)["Korrektur"], "Kamera-Chip Korrektur -> %s" % t) for t in TUERME]
    neu.append((5, an(*SITZ, "Seat data", 0, 5), kc["Sitz"], "Sitz Seat data -> Kamera-Chip Sitz"))
    neu.append((6, feed, kc["Video ein"], "Dachkamera Video -> Kamera-Chip Video ein"))
    weg = []
    for lab in BILD_KAM:
        k = link(6, feed, bild[lab])
        assert alt.count(k) == 1, ("Video-Kabel Dachkamera -> Bildschirm nicht genau einmal", lab, alt.count(k))
        weg.append(k)
        neu.append((6, kc["Video aus"], bild[lab], "Kamera-Chip Video aus -> Bildschirm '%s'" % lab))
    rest = [k for k in alt if k not in weg]
    belegte_eing = set((int(t or 0), p1) for t, p1 in re.findall(
        r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0[^>]*/>(<voxel_pos_1[^>]*/>)', "".join(rest)))
    zu = []
    for typ, p0, p1, was in neu:
        assert (typ, u.vox("voxel_pos_1", p1)) not in belegte_eing, ("Eingang schon belegt", was, p1)
        zu.append(link(typ, p0, p1))
        print("  %-60s %s -> %s" % (was, p0, p1))
    s = s[:li] + "".join(rest + zu) + s[le:]
    assert s.count("<logic_node_links>") == 1
    print("Kabel vorher %d, weg %d, neu %d" % (len(alt), len(weg), len(zu)))
    namen = "|".join(re.escape(n) for n, _, _ in TAUSCH)

    def ohne(x):
        x = re.sub(r'<microprocessor_definition name="(%s)".*?</microprocessor_definition>' % namen, "", x, flags=re.S)
        x = re.sub(r"<logic_slots>(<slot(?: editor_connected=\"1\")?/>)*</logic_slots>", "<logic_slots/>", x)
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0) == ohne(s), "ausser Chips und Kabeln geaendert"
    k0 = re.findall(r"<logic_node_link[ >].*?</logic_node_link>", s0[s0.index("<logic_node_links>"):s0.index("</logic_node_links>")])
    k1 = re.findall(r"<logic_node_link[ >].*?</logic_node_link>", s[s.index("<logic_node_links>"):s.index("</logic_node_links>")])
    assert [k for k in k0 if k not in weg] == k1[:len(k0) - len(weg)] and k1[len(k0) - len(weg):] == zu, "andere Kabel veraendert"
    print("Probe: nur %d Chip-Definitionen, Steckplaetze, %d Kabel weg, %d neu" % (len(TAUSCH), len(weg), len(zu)))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
