"""Lagezentrale der Figet Marena einbauen: Chips "Figet Marena Lage" (4 x 4) und "Figet Marena Bildschirm" (4 x 3) an
die Rueckwand des Chip-Raums setzen und alles verkabeln (Andre 03.10.: Microcontroller nach Belieben bauen/setzen).

Rueckwand z -59 (Innenseite), Gesicht zum Raum (+z): r 1,0,0,0,0,1,0,-1,0 -> Feld (x, z) = Welt (vx + x, vy - z, -59)
- Lage:       vp (-4, 9, -59) -> Welt x -4..-1, y 9..6
- Bildschirm: vp (1, 9, -59)  -> Welt x 1..4, y 9..7   (rechts unten bei (5, 7, -59) steht der Konstanten-Baustein)
Kabel:
- 6 Radar (Phalanx) am Mast: Radar Data -> Lage 'Radar i', Lage 'Gimbal i' -> Gimbal Input, 'Radare an' -> Activate
- Physik-Sensor -> Lage; Lage 'Lage' -> Bildschirm 'Lage'; Bildschirm 'Bedienung' -> Lage 'Bedienung'
- Monitor 9x5: Touch Output -> Bildschirm 'Touch', Bildschirm 'Monitor' -> Video Signal; Steuersitz -> 'Sitz'
- Flak L/R 'Flak Daten' -> Bildschirm; 4 Kameras (BC, AC vorn, Flak L, Flak R): Camera Feed -> Bildschirm
- Strom: linke Batterie -> 6 Radare, Monitor; rechte Batterie -> Kameras BC und AC vorn (Flak-Kameras haben schon)
Mast-Radare: manueller Modus (m_sweep_mode 4), Strahl m_fov_x/y 'FOV' (0,02 -> 0,04: breiter, dafuer etwas weniger
Reichweite - "Sensitivity is based on FOV").
Probe: ausser den 2 Chips, den neuen Kabeln und den Radar-Einstellungen aendert sich nichts.
Aufruf: python kabel_lage.py [--schreiben]   (vorher sichern; danach Schiff im Spiel neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import build_lage  # noqa: E402
import kabel_flak as kf  # noqa: E402
from build_schiff import BUILD  # noqa: E402

FOV = "0.04"
R_WAND = "1,0,0,0,0,1,0,-1,0"
CHIPS = {"Lage": ((-4, 9, -59), R_WAND), "Bildschirm": ((1, 9, -59), R_WAND)}
TEILE = {
    "SITZ": ("seat_compact", (0, 17, -10)),
    "PHYSIK": ("physics_sensor", (0, 27, -38)),
    "MONITOR": ("monitor_9", (0, 22, -6)),
    "KAM_BC": ("camera_med", (4, 19, 11)),
    "KAM_AC": ("camera_med", (-4, 9, 35)),
    "KAM_FL": ("camera_med", (-15, 20, -99)),
    "KAM_FR": ("camera_med", (15, 20, -99)),
    "BATT_L": ("battery_medium", (-8, -19, -65)),
    "BATT_R": ("battery_medium", (8, -19, -65)),
}
for k, (pos, _, _, _) in enumerate(build_lage.RADARE):
    TEILE["RADAR%d" % (k + 1)] = ("radar_advanced_phalanx", pos)

# (Quelle, Ziel, Typ): ("Lage"/"Bildschirm"/"Flak L"/"Flak R", Anschluss) oder (Teil, Knoten)
KABEL = []
for k in range(1, 7):
    KABEL += [(("RADAR%d" % k, "Radar Data"), ("Lage", "Radar %d" % k), 5),
              (("Lage", "Gimbal %d" % k), ("RADAR%d" % k, "Gimbal Input"), 5),
              (("Lage", "Radare an"), ("RADAR%d" % k, "Activate"), 0)]
KABEL += [
    (("PHYSIK", "Composite Output"), ("Lage", "Physik-Sensor"), 5),
    (("Lage", "Lage"), ("Bildschirm", "Lage"), 5),
    (("Bildschirm", "Bedienung"), ("Lage", "Bedienung"), 5),
    (("MONITOR", "Touch Output"), ("Bildschirm", "Touch"), 5),
    (("Bildschirm", "Monitor"), ("MONITOR", "Video Signal"), 6),
    (("SITZ", "Seat data"), ("Bildschirm", "Sitz"), 5),
    (("Flak L", "Flak Daten"), ("Bildschirm", "Flak L Daten"), 5),
    (("Flak R", "Flak Daten"), ("Bildschirm", "Flak R Daten"), 5),
    (("KAM_BC", "Camera Feed"), ("Bildschirm", "Kamera BC"), 6),
    (("KAM_AC", "Camera Feed"), ("Bildschirm", "Kamera AC vorn"), 6),
    (("KAM_FL", "Camera Feed"), ("Bildschirm", "Kamera Flak L"), 6),
    (("KAM_FR", "Camera Feed"), ("Bildschirm", "Kamera Flak R"), 6),
]
STROM = [("BATT_L", "RADAR%d" % k) for k in range(1, 7)] + [("BATT_L", "MONITOR"), ("BATT_R", "KAM_BC"), ("BATT_R", "KAM_AC")]


def chip_teil(datei, vp, r):
    """MC-Datei -> Bauteil <c d="microprocessor">..</c>, Anschluesse (Name -> Welt, Eingang?), Groesse."""
    u.CHIP = datei
    d = u.chip_eingebettet()
    w = int(re.search(r'<microprocessor_definition [^>]*width="(\d+)"', d).group(1))
    ln = int(re.search(r'<microprocessor_definition [^>]*length="(\d+)"', d).group(1))
    nk = len(re.findall(r"<n id=", d))
    teil = '<c d="microprocessor"><o r="%s" sc="%d">%s%s<logic_slots>%s</logic_slots></o></c>' % (
        r, 2 * w * ln + 2 * (w + ln), d, u.vox("vp", vp), "<slot/>" * nk)
    return teil, knoten(d, vp, r), (w, ln)


def knoten(d, vp, r):
    R = [[int(v) for v in r.split(",")][i * 3:i * 3 + 3] for i in range(3)]
    kn = {}
    for m in re.finditer(r'<node label="([^"]*)"([^>]*?)(?:/>|><position([^/]*)/></node>)', d):
        pa = dict(re.findall(r'(\w)="(-?\d+)"', m.group(3) or ""))
        x, z = int(pa.get("x", 0)), int(pa.get("z", 0))
        q = [R[0][i] * x + R[2][i] * z for i in range(3)]
        kn[m.group(1)] = (tuple(vp[i] + q[i] for i in range(3)), 'mode="1"' in m.group(2))
    return kn


def vorhandener_chip(s, name):
    """Anschluesse eines schon eingebauten Chips (Flak L/R) aus dem Fahrzeug."""
    i = s.index('<microprocessor_definition name="%s"' % name)
    e = s.index("</microprocessor_definition>", i) + len("</microprocessor_definition>")
    a = s.rindex('<c d="microprocessor"><o ', 0, i)
    r = re.search(r'r="([^"]*)"', s[a:i]).group(1)
    vp = u.xyz(re.match(r"<vp([^/]*)/>", s[e:]).group(1))
    return knoten(s[i:e], vp, r)


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    for name in ("Figet Marena Lage", "Figet Marena Bildschirm"):
        assert '<microprocessor_definition name="%s"' % name not in s, name + " ist schon eingebaut"
    tl = kf.teile(s)
    belegt = set(p for (_, p) in tl)
    # Chip-Flaechen: auch die schon eingebauten Microcontroller belegen ihre ganze Flaeche
    for m in re.finditer(r'<c d="microprocessor"><o r="([^"]*)"[^>]*><microprocessor_definition [^>]*width="(\d+)" length="(\d+)"', s):
        e = s.index("</microprocessor_definition>", m.end())
        vp = u.xyz(re.match(r"<vp([^/]*)/>", s[e + len("</microprocessor_definition>"):]).group(1))
        R = [[int(v) for v in m.group(1).split(",")][i * 3:i * 3 + 3] for i in range(3)]
        for x in range(int(m.group(2))):
            for z in range(int(m.group(3))):
                belegt.add(tuple(vp[i] + R[0][i] * x + R[2][i] * z for i in range(3)))
    # Einfuegestelle: Ende der Teileliste des Rumpf-Koerpers (letztes </components> vor </body>, s. kabel_flak)
    i0, e0 = s.index("<bodies>"), s.index("</bodies>")
    koerper = []
    a = s.index("<body ", i0)
    while 0 <= a < e0:
        e = s.index("</body>", a)
        koerper.append((a, e))
        a = s.find("<body ", e)
    rumpf = max(koerper, key=lambda q: s.count('<c d="', q[0], q[1]))
    einfueg = s.rindex("</components>", rumpf[0], rumpf[1])
    neu_teile, chipkn = "", {}
    for name, (vp, r) in CHIPS.items():
        datei = os.path.join(BUILD, "Figet Marena %s %s.xml" % (name, build_lage.VERSION))
        teil, kn, (w, ln) = chip_teil(datei, vp, r)
        R = [[int(v) for v in r.split(",")][i * 3:i * 3 + 3] for i in range(3)]
        flaeche = [tuple(vp[i] + R[0][i] * x + R[2][i] * z for i in range(3)) for x in range(w) for z in range(ln)]
        frei = [p for p in flaeche if p in belegt]
        assert not frei, ("Platz fuer %s belegt" % name, frei)
        belegt |= set(flaeche)
        neu_teile += teil
        chipkn[name] = kn
        print("%-10s eingesetzt: %d x %d, vp %s, Flaeche %s .. %s" % (name, w, ln, vp, flaeche[0], flaeche[-1]))
    s = s[:einfueg] + neu_teile + s[einfueg:]
    for m in re.finditer(r"<microprocessor_definition ", s):
        nxt = s.find("<microprocessor_definition ", m.end())
        assert nxt < 0 or nxt > s.index("</microprocessor_definition>", m.end()), ("Microcontroller verschachtelt", m.start())
    for seite in ("L", "R"):
        chipkn["Flak " + seite] = vorhandener_chip(s, "Figet Marena Flak " + seite)
    tl = kf.teile(s)

    def ort(q, soll_ein):
        schl, lab = q
        if schl in chipkn:
            p, ein = chipkn[schl][lab]
            assert ein == soll_ein, ("Richtung Chip-Anschluss", q)
            return p, None
        p, mo, ty = kf.anschluss(tl, TEILE[schl][0], TEILE[schl][1], lab)
        assert mo == (1 if soll_ein else 0), ("Richtung", q, mo)
        return p, ty

    li, le = s.index("<logic_node_links>"), s.index("</logic_node_links>")
    alt = re.findall(r"<logic_node_link.*?</logic_node_link>", s[li:le])
    plan = []
    for von, nach, typ in KABEL:
        p0, t0 = ort(von, False)
        p1, t1 = ort(nach, True)
        for tt in (t0, t1):
            assert tt is None or tt == typ, ("Typ passt nicht", von, nach, tt, typ)
        plan.append((typ, p0, p1, "%s %s -> %s %s" % (von[0], von[1], nach[0], nach[1])))
    for batt, teil in STROM:
        bp, _, _ = kf.anschluss(tl, TEILE[batt][0], TEILE[batt][1], "Electric Store")
        ep, _, et = kf.anschluss(tl, TEILE[teil][0], TEILE[teil][1], "Electric")
        assert et == 4
        plan.append((4, bp, ep, "Strom %s -> %s" % (batt, teil)))
    zu = []
    for typ, p0, p1, was in plan:
        k = "<logic_node_link%s>%s%s</logic_node_link>" % (' type="%d"' % typ if typ else "", u.vox("voxel_pos_0", p0), u.vox("voxel_pos_1", p1))
        if k not in alt and k not in zu:
            zu.append(k)
        print("  %-58s %s -> %s%s" % (was, p0, p1, "  (schon da)" if k in alt else ""))
    s = s[:le] + "".join(zu) + s[le:]
    print("Kabel vorher %d, neu %d" % (len(alt), len(zu)))
    # Mast-Radare: manueller Modus, Strahlbreite
    for k in range(1, 7):
        d, vp = TEILE["RADAR%d" % k]
        m = re.search(r'<c d="%s"(?: t="\d+")?><o ([^>]*)>(?:(?!</c>).)*?%s' % (d, re.escape(u.vox("vp", vp))), s, re.S)
        o = m.group(1)
        o2 = re.sub(r' m_sweep_mode="\d+"', "", o) + ' m_sweep_mode="4"'
        o2 = re.sub(r'm_fov_x="[^"]*"', 'm_fov_x="%s"' % FOV, o2)
        o2 = re.sub(r'm_fov_y="[^"]*"', 'm_fov_y="%s"' % FOV, o2)
        s = s[:m.start(1)] + o2 + s[m.end(1):]
        print("Radar %d %s: %s -> %s" % (k, vp, o, o2))
    # Probe
    def ohne(x):
        x = re.sub(r'<c d="microprocessor"><o [^>]*><microprocessor_definition name="Figet Marena (Lage|Bildschirm)".*?</o></c>', "", x, flags=re.S)
        x = re.sub(r'(<c d="radar_advanced_phalanx"(?: t="\d+")?><o [^>]*?) m_fov_x="[^"]*" m_fov_y="[^"]*"( m_sweep_mode="4")?', r"\g<1>", x)
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0) == ohne(s), "ausser Chips/Kabeln/Radar-Einstellungen geaendert"
    k0 = re.findall(r"<logic_node_link.*?</logic_node_link>", s0[s0.index("<logic_node_links>"):s0.index("</logic_node_links>")])
    k1 = re.findall(r"<logic_node_link.*?</logic_node_link>", s[s.index("<logic_node_links>"):s.index("</logic_node_links>")])
    assert k1[:len(k0)] == k0 and len(k1) == len(k0) + len(zu), "alte Kabel veraendert"
    print("Probe: nur 2 Chips, %d neue Kabel, 6 Radar-Einstellungen" % len(zu))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
