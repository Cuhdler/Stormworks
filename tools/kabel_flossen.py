"""Figet Marena: Flossen-Chip einsetzen und alle Kabel legen (Andres Umbau 02.10.).

- Andres leerer Microcontroller 1x1 bei (0,-5,-44) wird der Chip build/<build_flossen.MC_FILE> (ab v1.5 3 x 4, sc 38);
  Chip-Feld (x, z) -> Welt (0, -5-x, -44+z) (gleiche Drehung wie der Schiffs-Chip). Ist er schon eingesetzt, wird er
  erneuert (Lage gleich).
- Physik-Sensor (0,27,-38) Composite -> Flossen-Chip 'Physik-Sensor' (zweites Kabel, das zum Schiffs-Chip bleibt)
- Flossen-Ausgaenge -> 'Rotation' der 10 Control Fin Medium; Strom je Flosse von der Batterie ihrer Seite
- Schiffs-Chip 'Ruder' -> neu gesetztes linkes Ruder-Bauteil (-9,-11,-148) (das alte Kabel ist mit dem Teil weg)
- ab Flossen v1.7: 'Physik weiter' -> Schiffs-Chip 'Physik-Sensor' (Wellen-Skript braucht das Heck-Wasser); das direkte
  Kabel Physik-Sensor -> Schiffs-Chip entfaellt (ein Eingang nimmt nur ein Kabel)
Jeder Anschluss wird aus der Bauteil-Definition berechnet (vp + R^T * p, gespiegelt t=1/2: x) und geprueft;
vorhandene Kabel bleiben, doppelte entfallen.
Aufruf: python kabel_flossen.py [--test] [--schreiben]   (--test: Test-Chip statt v1.2; danach Schiff im Spiel neu laden,
NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import build_flossen  # noqa: E402
from build_schiff import BUILD  # noqa: E402

DEF = r"E:\SteamLibrary\steamapps\common\Stormworks\rom\data\definitions"
CHIP_VP = (0, -5, -44)
PHYSIK = ("physics_sensor", (0, 27, -38), "Composite Output")
# Ausgang -> Flossen (Teil, Position); die beiden hintersten sind seit 02.10. abends Control Fin Large
M, L = "control_fin_medium", "control_fin_large"
FLOSSEN = {
    "Flossen vorn L": [(M, (-1, -21, 25)), (M, (-1, -21, 28))],
    "Flossen vorn R": [(M, (1, -21, 25)), (M, (1, -21, 28))],
    "Flossen hinten L": [(M, (-10, -16, -120)), (L, (-10, -16, -134))],
    "Flossen hinten R": [(M, (10, -16, -120)), (L, (10, -16, -134))],
    "Flossen Mitte L": [(M, (-9, -21, -92))],
    "Flossen Mitte R": [(M, (9, -21, -92))],
    "Flossen vorn-Mitte L": [(L, (-9, -21, -2))],
    "Flossen vorn-Mitte R": [(L, (9, -21, -2))],
}
# Heck-Wasser: Liquid Meter (water_measure) am Heck (z < -110), falls Andre einen gesetzt hat
BATTERIE = {-1: (-8, -19, -65), 1: (8, -19, -65)}       # battery_medium links/rechts
RUDER_NEU = ("rudder", (-9, -11, -148), "Rotation")
SCHIFF_RUDER = u.chip(2, 2)                               # Schiffs-Chip 'Ruder'
SCHIFF_PHYSIK = u.chip(1, 0)                              # Schiffs-Chip 'Physik-Sensor' (Eingang)


def knoten_def(d):
    t = open(os.path.join(DEF, d + ".xml"), encoding="utf-8", errors="replace").read()
    out = {}
    for m in re.finditer(r'<logic_node ([^>]*)>(.*?)</logic_node>', t, re.S):
        at = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        ps = re.search(r'<position([^/]*)/>', m.group(2))
        pa = dict(re.findall(r'(\w)="(-?\d+)"', ps.group(1))) if ps else {}
        out.setdefault(at.get("label"), []).append((int(at.get("mode", 0)), int(at.get("type", 0)),
                                                    tuple(int(pa.get(k, 0)) for k in "xyz")))
    return out


def teile(s):
    out = {}
    for m in re.finditer(r'<c d="([^"]+)"(?: t="(\d)")?><o ([^>]*)><vp([^/]*)/>', s):
        r = re.search(r'r="([^"]*)"', m.group(3))
        out.setdefault(u.xyz(m.group(4)), []).append((m.group(1), [int(float(q)) for q in (r.group(1) if r else "1,0,0,0,1,0,0,0,1").split(",")], m.group(2)))
    return out


def anschluss(tl, d, vp, label):
    """Welt-Position, Richtung (mode), Typ des Anschlusses 'label' am Teil d bei vp."""
    kand = [x for x in tl.get(vp, []) if x[0] == d]
    assert len(kand) == 1, ("Teil nicht (eindeutig) gefunden", d, vp, tl.get(vp))
    _, r, t = kand[0]
    (mode, typ, p), = knoten_def(d)[label]
    R = [r[0:3], r[3:6], r[6:9]]
    q = [sum(R[j][i] * p[j] for j in range(3)) for i in range(3)]
    if t in ("1", "2"):
        q[0] = -q[0]
    return tuple(vp[i] + q[i] for i in range(3)), mode, typ


def main():
    s = einbauen(open(u.VEH, encoding="utf-8", newline="").read())
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


def einbauen(s):
    """Flossen-Chip einsetzen und Kabel legen; gibt die neue Fahrzeug-Zeichenkette zurueck."""
    tl = teile(s)
    # --- Chip einsetzen
    m = None
    for name in ("Microcontroller", "Figet Marena Flossen"):
        for mm in re.finditer(r'<c d="microprocessor"><o ([^>]*)><microprocessor_definition name="%s"' % re.escape(name), s):
            ende = s.index("</c>", s.index("</microprocessor_definition>", mm.end()))
            if re.search(r'</microprocessor_definition><vp([^/]*)/>', s[mm.start():ende + 4]).group(1) and \
                    u.xyz(re.search(r'</microprocessor_definition><vp([^/]*)/>', s[mm.start():ende + 4]).group(1)) == CHIP_VP:
                m = (mm.start(), ende + 4, mm.group(1))
    assert m, "kein Microcontroller bei %s" % (CHIP_VP,)
    a, e, oattr = m
    teil = s[a:e]
    assert 'r="0,-1,0,1,0,0,0,0,1"' in oattr, ("Chip anders gedreht", oattr)
    u.CHIP = os.path.join(BUILD, build_flossen.TEST_FILE if "--test" in sys.argv else build_flossen.MC_FILE)
    neu_def = u.chip_eingebettet()
    nk = len(re.findall(r"<n id=", neu_def))
    d0 = teil.index("<microprocessor_definition")
    d1 = teil.index("</microprocessor_definition>") + len("</microprocessor_definition>")
    rest = re.sub(r"<logic_slots>.*?</logic_slots>", "<logic_slots>" + "<slot/>" * nk + "</logic_slots>", teil[d1:], count=1)
    w, l = (int(re.search(r'<microprocessor_definition [^>]*%s="(\d+)"' % k, neu_def).group(1)) for k in ("width", "length"))
    kopf = re.sub(r' sc="\d+"', ' sc="%d"' % (2 * w * l + 2 * (w + l)), teil[:d0])
    s = s[:a] + kopf + neu_def + rest + s[e:]
    print("Flossen-Chip eingesetzt bei %s (%d x %d, %d Anschluesse, sc %d)" % (CHIP_VP, w, l, nk, 2 * w * l + 2 * (w + l)))
    knoten = {}
    for mm in re.finditer(r'<node label="([^"]*)"([^>]*?)(?:/>|><position([^/]*)/></node>)', neu_def):
        pa = dict(re.findall(r'(\w)="(-?\d+)"', mm.group(3) or ""))
        x, z = int(pa.get("x", 0)), int(pa.get("z", 0))
        knoten[mm.group(1)] = ((CHIP_VP[0], CHIP_VP[1] - x, CHIP_VP[2] + z), 'mode="1"' in mm.group(2))
    # --- Kabel planen
    neu = []
    ppos, pm, pt = anschluss(tl, *PHYSIK)
    assert pt == 5 and pm == 0
    neu.append((5, ppos, knoten["Physik-Sensor"][0], "Physik-Sensor -> Flossen-Chip"))
    for label, ziele in FLOSSEN.items():
        cpos, ein = knoten[label]
        assert not ein
        for d, vp in ziele:
            rpos, rm, rt = anschluss(tl, d, vp, "Rotation")
            assert rt == 1 and rm == 1
            neu.append((1, cpos, rpos, "%s -> Flosse %s" % (label, vp)))
            epos, em, et = anschluss(tl, d, vp, "Electric")
            bpos, bm, bt = anschluss(tl, "battery_medium", BATTERIE[1 if vp[0] > 0 else -1], "Electric Store")
            assert et == 4 and bt == 4
            neu.append((4, bpos, epos, "Strom Batterie %s -> Flosse %s" % (bpos, vp)))
    messer = [vp for vp, lst in tl.items() for (d, r, t) in lst if d == "water_measure" and vp[2] < -110]
    if len(messer) == 1 and "Heck-Wasser" in knoten:
        mpos, mm, mt = anschluss(tl, "water_measure", messer[0], "Liquid Level")
        assert mt == 1 and mm == 0
        neu.append((1, mpos, knoten["Heck-Wasser"][0], "Heck-Wasser: Liquid Meter %s -> Flossen-Chip" % (messer[0],)))
    else:
        print("  Heck-Wasser: kein (eindeutiger) Liquid Meter am Heck gefunden %s - Eingang bleibt frei" % (messer,))
    rpos, rm, rt = anschluss(tl, *RUDER_NEU)
    assert rt == 1 and rm == 1
    neu.append((1, SCHIFF_RUDER, rpos, "Schiffs-Chip Ruder -> linkes Ruder-Bauteil %s" % (RUDER_NEU[1],)))
    weg = []
    if "Physik weiter" in knoten:
        wpos, wein = knoten["Physik weiter"]
        assert not wein
        neu.append((5, wpos, SCHIFF_PHYSIK, "Flossen-Chip 'Physik weiter' -> Schiffs-Chip 'Physik-Sensor'"))
        weg.append("<logic_node_link type=\"5\">%s%s</logic_node_link>" % (u.vox("voxel_pos_0", ppos), u.vox("voxel_pos_1", SCHIFF_PHYSIK)))
    li, le = s.index("<logic_node_links>"), s.index("</logic_node_links>")
    alt = re.findall(r"<logic_node_link.*?</logic_node_link>", s[li:le])
    for k in weg:
        if k in alt:
            s = s[:li] + s[li:le].replace(k, "", 1) + s[le:]
            alt.remove(k)
            li, le = s.index("<logic_node_links>"), s.index("</logic_node_links>")
            print("  entfernt: direktes Kabel Physik-Sensor -> Schiffs-Chip 'Physik-Sensor'")
    am_eingang = [k for k in alt if u.vox("voxel_pos_1", SCHIFF_PHYSIK) in k or u.vox("voxel_pos_0", SCHIFF_PHYSIK) in k]
    if weg:
        assert not am_eingang, ("noch andere Kabel am Schiffs-Chip 'Physik-Sensor'", am_eingang)
    zu = []
    for typ, p0, p1, was in neu:
        k = "<logic_node_link%s>%s%s</logic_node_link>" % (' type="%d"' % typ if typ else "", u.vox("voxel_pos_0", p0), u.vox("voxel_pos_1", p1))
        print("  %-60s %s -> %s%s" % (was, p0, p1, "" if k not in alt else "  (schon da)"))
        if k not in alt and k not in zu:
            zu.append(k)
    s = s[:le] + "".join(zu) + s[le:]
    print("vorhandene Kabel %d, neu %d" % (len(alt), len(zu)))
    return s


if __name__ == "__main__":
    main()
