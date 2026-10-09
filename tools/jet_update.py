"""Ferngesteuerter Jet - Chips einbauen (Andre 08.10.: small Jet mit Maussteuerung vom Schiff, Kamera; Bild auf den
3x3-Monitor vor dem zweiten Sitz; Platzhalter-Chip 4x4 im Jet gesetzt).
small Jet:
- Andres Platzhalter (vp (-3,-3,-21), 4x4) -> Chip "Jet Flug" (gleiche Stelle und Drehung)
- Kabel: Funk Empfang (2,2,-22) Data Recv -> 'Befehle'; Physik-Sensor (0,3,-18) -> 'Physik'; Liquid Meter -> 'Tank';
  Ruder (-6/6,-6,-21), Seitenruder (0,-6,-21), Brennkammer Throttle, Kamera unten Field of View, Frequenzen (Funk
  Empfang + Video vorn / Funk Senden + Video unten), Verdichter, 6 Booster, Lampen/Scheinwerfer/Horizont, 4 Magnete,
  Funk Senden Transmit Mode + Data Send; Strom Batterie (0,5,-18) -> Physik-Sensor
Figet Marena:
- Chip "Figet Marena Jet Steuerung" 4x3 an der Decke des Chip-Raums vp (-2,13,-54) (x -2..1, z -56..-54)
- Kabel: zweiter Sitz (-5,16,-26) -> 'Sitz'; Funk Empfang (7,24,-50) Data Recv -> 'Flugdaten', Signal -> 'Signal';
  Physik-Sensor -> 'Physik'; Video-Empfaenger (0,24,-44) -> 'Kamera'; 'Befehle' -> Funk Senden (-7,24,-50) Data Send;
  Frequenzen und Transmit Mode; 'Monitor' -> Monitor 3x3 (-5,20,-24), 'Monitor an' -> Power Switch;
  Strom Batterie (-4,-13,-46) -> beide Funkgeraete und Video-Empfaenger
Probe je Fahrzeug: ausser Chip und Kabeln aendert sich nichts.
Aufruf: python jet_update.py [--schreiben]   (vorher sichern; danach beide neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import sperrprofil  # noqa: E402
import build_jet as bj  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from autopilot_update import link, chip_flaeche, flaeche, BATT, LINKS, AP  # noqa: E402

JET = os.path.join(os.environ["APPDATA"], "Stormworks", "data", "vehicles", "small Jet.xml")


def chip_teil(name, r_, vp, bc=""):
    u.CHIP = os.path.join(BUILD, "%s %s.xml" % (name, bj.VERSION))
    d = u.chip_eingebettet()
    w = int(re.search(r'<microprocessor_definition [^>]*width="(\d+)"', d).group(1))
    ln = int(re.search(r'<microprocessor_definition [^>]*length="(\d+)"', d).group(1))
    nk = len(re.findall(r"<n id=", d))
    return '<c d="microprocessor"><o r="%s"%s sc="%d">%s%s<logic_slots>%s</logic_slots></o></c>' % (
        r_, bc, 2 * w * ln + 2 * (w + ln), d, u.vox("vp", vp), "<slot/>" * nk), w, ln


def kabel_dazu(s, neu):
    li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
    alt = re.findall(LINKS, s[li:le])
    assert "".join(alt) == s[li:le], "Kabelliste nicht vollstaendig erfasst"
    belegt = set((int(t or 0), p1) for t, p1 in re.findall(
        r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0[^>]*/>(<voxel_pos_1[^>]*/>)', "".join(alt)))
    zu = []
    for typ, p0, p1, was in neu:
        assert (typ, u.vox("voxel_pos_1", p1)) not in belegt, ("Eingang schon belegt", was, p1)
        zu.append(link(typ, p0, p1))
    return s[:li] + "".join(alt + zu) + s[le:], len(zu)


def jet():
    s0 = open(JET, encoding="utf-8", newline="").read()
    mcs = list(re.finditer(r'<c d="microprocessor"><o r="([^"]*)"[^>]*>', s0))
    assert len(mcs) == 1, "genau ein Chip (Andres Platzhalter) erwartet"
    a = mcs[0].start()
    e = s0.index("</o></c>", a) + len("</o></c>")
    alt = s0[a:e]
    assert 'width="4" length="4"' in alt, "Platzhalter ist nicht 4x4"
    vp = u.xyz(re.findall(r"<vp([^/]*)/>", alt)[-1])
    r_ = mcs[0].group(1)
    teil, w, ln = chip_teil("Jet Flug", r_, vp)
    s = s0[:a] + teil + s0[e:]
    kn = chip_knoten(s, "Jet Flug")
    tl = kf.teile(s)

    def an(d, p, lab, mo, ty):
        q, m_, t_ = kf.anschluss(tl, d, p, lab)
        assert (m_, t_) == (mo, ty), (d, p, lab, m_, t_)
        return q
    rx, tx = (2, 2, -22), (-2, 1, -22)
    neu = [(5, an("rx_huge_v2", rx, "Data Recv", 0, 5), kn["Befehle"], "Funk Empfang -> Befehle"),
           (5, an("physics_sensor", (0, 3, -18), "Composite Output", 0, 5), kn["Physik"], "Physik -> Physik"),
           (1, an("water_measure", (0, -3, -19), "Liquid Level", 0, 1), kn["Tank"], "Tank -> Tank"),
           (1, kn["Ruder links"], an("control_surface_medium", (-6, -6, -21), "Rotation", 1, 1), "Ruder links"),
           (1, kn["Ruder rechts"], an("control_surface_medium", (6, -6, -21), "Rotation", 1, 1), "Ruder rechts"),
           (1, kn["Seitenruder"], an("control_surface_small", (0, -6, -21), "Rotation", 1, 1), "Seitenruder"),
           (1, kn["Gas"], an("jet_engine_combustion_chamber", (0, 7, -21), "Throttle", 1, 1), "Gas"),
           (1, kn["Zoom"], an("camera_med", (0, 4, -19), "Field of View", 1, 1), "Zoom Kamera unten"),
           (1, kn["Freq Befehle"], an("rx_huge_v2", rx, "Frequency", 1, 1), "Freq Funk Empfang"),
           (1, kn["Freq Befehle"], an("rx_video_x", (0, -5, -23), "Frequency Send", 1, 1), "Freq Video vorn"),
           (1, kn["Freq Daten"], an("rx_huge_v2", tx, "Frequency", 1, 1), "Freq Funk Senden"),
           (1, kn["Freq Daten"], an("rx_video_x", (1, 2, -23), "Frequency Send", 1, 1), "Freq Video unten"),
           (0, kn["Verdichter"], an("jet_engine_compressor", (0, 11, -21), "Compressor", 1, 0), "Verdichter"),
           (0, kn["Senden an"], an("rx_huge_v2", tx, "Transmit Mode", 1, 0), "Funk Senden Transmit Mode"),
           (5, kn["Flugdaten"], an("rx_huge_v2", tx, "Data Send", 1, 5), "Flugdaten -> Funk Senden"),
           (4, an("battery_medium", (0, 5, -18), "Electric Store", 1, 4), an("physics_sensor", (0, 3, -18), "Electric", 1, 4),
            "Strom -> Physik-Sensor")]
    for (d, p) in sorted(k for k in tl if k[0] == "solid_rocket_nozzle_small"):
        neu.append((0, kn["Booster"], an(d, p, "Trigger", 1, 0), "Booster %s" % (p,)))
    for (d, p) in sorted(k for k in tl if k[0] in ("small_light", "searchlight_small")):
        neu.append((0, kn["Licht"], an(d, p, "Light Switch", 1, 0), "Licht %s" % (p,)))
    neu.append((0, kn["Licht"], an("artificial_horizon", (0, -1, -24), "Backlight", 1, 0), "Horizont Licht"))
    for (d, p) in sorted(k for k in tl if k[0] == "magall"):
        neu.append((0, kn["Magnete"], an(d, p, "Magnet Toggle", 1, 0), "Magnet %s" % (p,)))
    s, n = kabel_dazu(s, neu)

    def ohne(x):
        i = x.index('<c d="microprocessor">')
        x = x[:i] + x[x.index("</o></c>", i) + 8:]
        li, le = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li] + x[le:]
    assert ohne(s0) == ohne(s), "Jet: ausser Chip und Kabeln geaendert"
    print("Jet: Chip 'Jet Flug' %dx%d an Andres Platzhalter %s (r %s), %d Kabel neu" % (w, ln, vp, r_, n))
    return s0, s


def schiff():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    name = "Figet Marena Jet Steuerung"
    assert '<microprocessor_definition name="%s"' % name not in s0, "schon eingebaut"
    vp, r_ = (-2, 13, -54), "1,0,0,0,-1,0,0,0,-1"
    teil, w, ln = chip_teil(name, r_, vp, ' bc="70787D"')
    R = [[int(v) for v in r_.split(",")][i * 3:i * 3 + 3] for i in range(3)]
    fl = flaeche(R, vp, w, ln)
    teile_vox = set(p for t in sperrprofil.koerper() for dd, p in t if dd != "microprocessor")
    chips_vox = set()
    for mm in re.finditer(r'<microprocessor_definition name="([^"]*)"', s0):
        chips_vox |= chip_flaeche(s0, mm.group(1))
    assert not (fl & (teile_vox | chips_vox)), ("Platz belegt", sorted(fl & (teile_vox | chips_vox)))
    vor = set((p[0] + R[1][0], p[1] + R[1][1], p[2] + R[1][2]) for p in fl)
    hinter = set((p[0] - R[1][0], p[1] - R[1][1], p[2] - R[1][2]) for p in fl)
    assert not (vor & (teile_vox | chips_vox)), ("unter dem Chip kein Raum", sorted(vor & (teile_vox | chips_vox)))
    assert hinter <= teile_vox, ("ueber dem Chip keine Decke", sorted(hinter - teile_vox))
    _, e = u.mc_bereich(s0, AP)
    s = s0[:e] + teil + s0[e:]
    kn = chip_knoten(s, name)
    tl = kf.teile(s)

    def an(d, p, lab, mo, ty):
        q, m_, t_ = kf.anschluss(tl, d, p, lab)
        assert (m_, t_) == (mo, ty), (d, p, lab, m_, t_)
        return q
    tx, rx, vr, mon = (-7, 24, -50), (7, 24, -50), (0, 24, -44), (-5, 20, -24)
    strom = an(BATT[0], BATT[1], "Electric Store", 1, 4)
    neu = [(5, an("seat_compact", (-5, 16, -26), "Seat data", 0, 5), kn["Sitz"], "zweiter Sitz -> Sitz"),
           (5, an("rx_huge_v2", rx, "Data Recv", 0, 5), kn["Flugdaten"], "Funk Empfang -> Flugdaten"),
           (1, an("rx_huge_v2", rx, "Signal Strength", 0, 1), kn["Signal"], "Funk Empfang Signal"),
           (5, an("physics_sensor", (0, 27, -38), "Composite Output", 0, 5), kn["Physik"], "Physik -> Physik"),
           (6, an("rx_video_r", vr, "Video Recv", 0, 6), kn["Kamera"], "Video-Empfaenger -> Kamera"),
           (5, kn["Befehle"], an("rx_huge_v2", tx, "Data Send", 1, 5), "Befehle -> Funk Senden"),
           (1, kn["Freq Senden"], an("rx_huge_v2", tx, "Frequency", 1, 1), "Freq Senden"),
           (1, kn["Freq Empfang"], an("rx_huge_v2", rx, "Frequency", 1, 1), "Freq Empfang"),
           (1, kn["Freq Video"], an("rx_video_r", vr, "Frequency Recv", 1, 1), "Freq Video"),
           (0, kn["Senden an"], an("rx_huge_v2", tx, "Transmit Mode", 1, 0), "Funk Senden Transmit Mode"),
           (6, kn["Monitor"], an("monitor_3", mon, "Video Signal", 1, 6), "Monitor 3x3 Video"),
           (0, kn["Monitor an"], an("monitor_3", mon, "Power Switch", 1, 0), "Monitor 3x3 Power Switch"),
           (4, strom, an("rx_huge_v2", tx, "Electric", 1, 4), "Strom -> Funk Senden"),
           (4, strom, an("rx_huge_v2", rx, "Electric", 1, 4), "Strom -> Funk Empfang"),
           (4, strom, an("rx_video_r", vr, "Electric", 1, 4), "Strom -> Video-Empfaenger")]
    s, n = kabel_dazu(s, neu)

    def ohne(x, neu_):
        if neu_:
            a2, e2 = u.mc_bereich(x, name)
            x = x[:a2] + x[e2:]
        li, le = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li] + x[le:]
    assert ohne(s0, False) == ohne(s, True), "Schiff: ausser Chip und Kabeln geaendert"
    print("Schiff: Chip '%s' %dx%d an der Decke %s, %d Kabel neu" % (name, w, ln, vp, n))
    return s0, s


def main():
    import xml.etree.ElementTree as ET
    ziele = []
    for pfad, (s0, s) in ((JET, jet()), (u.VEH, schiff())):
        ET.fromstring(s.encode("utf-8"))
        ziel = pfad if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."),
                                                                    "probe_" + os.path.basename(pfad))
        with open(ziel, "w", encoding="utf-8", newline="") as f:
            f.write(s)
        ziele.append(ziel)
    print("Probe: XML gueltig; geschrieben:", ziele)


if __name__ == "__main__":
    main()
