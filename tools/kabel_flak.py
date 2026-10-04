"""Flak-Chips in den Chip-Raum der Figet Marena setzen und alles verkabeln (Andre 03.10.: "du kannst Microcontroller
nach Belieben bearbeiten/loeschen/neu bauen/verschieben").

Chip-Raum: zwischen den Waenden x -6/+6, Rueckwand z -60, Boden y 1, Decke y 14. Andres 10 Platzhalter (1x1,
x +-5, y 2-6, z -59) fliegen raus; die Chips haengen senkrecht an den Seitenwaenden wie Schalttafeln:
- Flak L (4 x 5) an der linken Wand: vp (-5, 9, -58), r 0,-1,0,1,0,0,0,0,1 -> Feld (x, z) = Welt (-5, 9-x, -58+z)
- Flak R (4 x 5) an der rechten Wand: vp (5, 6, -58), r 0,1,0,-1,0,0,0,0,1 -> Feld (x, z) = Welt (5, 6+x, -58+z)
  (z -59 bleibt frei: rechts hinten steht ein Konstanten-Baustein bei (5, 7, -59))
Kabel: Sitz, Physik-Sensor, Turm-Radar (Daten, Drehung, Gimbal, an), Drehkranz, beide Rohr-Pivots, beide Rohre
(Abzug, Zuender, Loaded links), beide Zufuehrungen, Kamera-Pivot; Strom von der Batterie der Seite an alle Teile.
Turm-Radare: manueller Modus (m_sweep_mode 4 wie die Swifter-Flak).
Anschluss-Lage: Definition + Drehung; Spiegeln t = Bitmaske auf die Teil-Achsen (1 x, 2 y, 4 z) VOR der Drehung
(an allen eindeutigen Kabeln in Figet Marena, Rescue Heli, Swifter geprueft, 03.10.).
Probe: ausser Platzhaltern, den 2 Chips, den neuen Kabeln und dem Radar-Modus aendert sich nichts.
Aufruf: python kabel_flak.py [--schreiben]   (danach Schiff im Spiel neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import build_flak  # noqa: E402
from build_schiff import BUILD  # noqa: E402

DEF = r"E:\SteamLibrary\steamapps\common\Stormworks\rom\data\definitions"
SITZ = ("seat_compact", (0, 17, -10), "Seat data")
PHYSIK = ("physics_sensor", (0, 27, -38), "Composite Output")
BATT = {"L": ("battery_medium", (-8, -19, -65)), "R": ("battery_medium", (8, -19, -65))}
CHIPS = {"L": ((-5, 9, -58), "0,-1,0,1,0,0,0,0,1"), "R": ((5, 6, -58), "0,1,0,-1,0,0,0,0,1")}
# Teile je Turm: (Teil, Position); links/rechts = Rohr mit kleinerem/groesserem x
TURM = {
    "L": {"radar": ("radar_advanced", (-10, 21, -104)), "ring": ("multibody_turret_medium_a", (-10, 14, -105)),
          "piv_l": ("multibody_robotic_pivot_01_a", (-13, 18, -102)), "piv_r": ("multibody_robotic_pivot_01_a", (-7, 18, -102)),
          "gun_l": ("gun_m", (-11, 18, -102)), "gun_r": ("gun_m", (-9, 18, -102)),
          "lad_l": ("gun_belt_loader", (-11, 17, -102)), "lad_r": ("gun_belt_loader", (-9, 17, -102)),
          "kpiv": ("multibody_compact_pivot_robotic_a", (-14, 20, -100)), "kam": ("camera_med", (-15, 20, -99))},
    "R": {"radar": ("radar_advanced", (10, 21, -104)), "ring": ("multibody_turret_medium_a", (10, 14, -105)),
          "piv_l": ("multibody_robotic_pivot_01_a", (7, 18, -102)), "piv_r": ("multibody_robotic_pivot_01_a", (13, 18, -102)),
          "gun_l": ("gun_m", (9, 18, -102)), "gun_r": ("gun_m", (11, 18, -102)),
          "lad_l": ("gun_belt_loader", (9, 17, -102)), "lad_r": ("gun_belt_loader", (11, 17, -102)),
          "kpiv": ("multibody_compact_pivot_robotic_a", (14, 20, -100)), "kam": ("camera_med", (15, 20, -99))},
}
# (Quelle, Ziel, Typ): Quelle/Ziel = ("chip", Anschluss) oder (Teil-Schluessel, Knoten)
KABEL = [
    (("SITZ", None), ("chip", "Sitz"), 5),
    (("PHYSIK", None), ("chip", "Physik-Sensor"), 5),
    (("radar", "Radar Data"), ("chip", "Radar"), 5),
    (("radar", "Radar Rotation"), ("chip", "Radar Drehung"), 1),
    (("ring", "Current Rotation"), ("chip", "Turm Drehung"), 1),
    (("gun_l", "Loaded"), ("chip", "Geladen"), 0),
    (("chip", "Turm Tempo"), ("ring", "Rotational Speed"), 1),
    (("chip", "Hoehe Rohr links"), ("piv_l", "Rotation Target"), 1),
    (("chip", "Hoehe Rohr rechts"), ("piv_r", "Rotation Target"), 1),
    (("chip", "Zuender"), ("gun_l", "Fuse Timer"), 1),
    (("chip", "Zuender"), ("gun_r", "Fuse Timer"), 1),
    (("chip", "Feuer"), ("gun_l", "Trigger"), 0),
    (("chip", "Feuer"), ("gun_r", "Trigger"), 0),
    (("chip", "Zufuehrung"), ("lad_l", "Feed"), 0),
    (("chip", "Zufuehrung"), ("lad_r", "Feed"), 0),
    (("chip", "Radar an"), ("radar", "Activate"), 0),
    (("chip", "Radar Gimbal"), ("radar", "Gimbal Input"), 5),
    (("chip", "Kamera Hoehe"), ("kpiv", "Rotation Target"), 1),
]
STROM = ["radar", "ring", "piv_l", "piv_r", "gun_l", "gun_r", "lad_l", "lad_r", "kpiv", "kam"]


def def_knoten(d, cache={}):
    if d not in cache:
        t = open(os.path.join(DEF, d + ".xml"), encoding="utf-8", errors="replace").read()
        out = {}
        for m in re.finditer(r'<logic_node ([^>]*)>(.*?)</logic_node>', t, re.S):
            at = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
            ps = re.search(r'<position([^/]*)/>', m.group(2))
            pa = dict(re.findall(r'(\w)="(-?\d+)"', ps.group(1))) if ps else {}
            out[at.get("label")] = (int(at.get("mode", 0)), int(at.get("type", 0)), tuple(int(pa.get(k, 0)) for k in "xyz"))
        cache[d] = out
    return cache[d]


def teile(s):
    """(Teil, Position) -> (Drehung, t) fuer alle Teile."""
    out = {}
    s2 = re.sub(r"<microprocessor_definition.*?</microprocessor_definition>", "", s, flags=re.S)
    for m in re.finditer(r'<c d="([^"]+)"(?: t="(\d+)")?><o ([^>]*)>(?:(?!</c>).)*?<vp([^/]*)/>', s2, re.S):
        r = re.search(r'r="([^"]*)"', m.group(3))
        rr = [int(float(q)) for q in (r.group(1) if r else "1,0,0,0,1,0,0,0,1").split(",")]
        out.setdefault((m.group(1), u.xyz(m.group(4))), []).append((rr, int(m.group(2) or 0)))
    return out


def anschluss(tl, d, vp, label):
    kand = tl.get((d, vp), [])
    assert len(kand) == 1, ("Teil nicht (eindeutig) gefunden", d, vp, len(kand))
    r, t = kand[0]
    mode, typ, p = def_knoten(d)[label]
    p = [(-1 if t & (1 << i) else 1) * p[i] for i in range(3)]
    R = [r[0:3], r[3:6], r[6:9]]
    q = [sum(R[j][i] * p[j] for j in range(3)) for i in range(3)]
    return tuple(vp[i] + q[i] for i in range(3)), mode, typ


def chip_teil(seite):
    """Fertiges Bauteil <c d="microprocessor">...</c> fuer Flak L/R und seine Anschluesse (Name -> Welt, Eingang?)."""
    u.CHIP = os.path.join(BUILD, "Figet Marena Flak %s %s.xml" % (seite, build_flak.VERSION))
    d = u.chip_eingebettet()
    w = int(re.search(r'<microprocessor_definition [^>]*width="(\d+)"', d).group(1))
    ln = int(re.search(r'<microprocessor_definition [^>]*length="(\d+)"', d).group(1))
    vp, r = CHIPS[seite]
    nk = len(re.findall(r"<n id=", d))
    teil = '<c d="microprocessor"><o r="%s" sc="%d">%s%s<logic_slots>%s</logic_slots></o></c>' % (
        r, 2 * w * ln + 2 * (w + ln), d, u.vox("vp", vp), "<slot/>" * nk)
    R = [[int(v) for v in r.split(",")][i * 3:i * 3 + 3] for i in range(3)]
    kn = {}
    for m in re.finditer(r'<node label="([^"]*)"([^>]*?)(?:/>|><position([^/]*)/></node>)', d):
        pa = dict(re.findall(r'(\w)="(-?\d+)"', m.group(3) or ""))
        x, z = int(pa.get("x", 0)), int(pa.get("z", 0))
        q = [R[0][i] * x + R[2][i] * z for i in range(3)]
        kn[m.group(1)] = (tuple(vp[i] + q[i] for i in range(3)), 'mode="1"' in m.group(2))
    return teil, kn, (w, ln)


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    # 1. Andres Platzhalter (1x1 'Microcontroller' bei x +-5, y 2-6, z -59) entfernen
    weg = 0
    for m in list(re.finditer(r'<c d="microprocessor"><o [^>]*><microprocessor_definition name="Microcontroller"', s)):
        pass
    while True:
        i = s.find('<microprocessor_definition name="Microcontroller"')
        if i < 0:
            break
        a = s.rindex('<c d="microprocessor"', 0, i)
        e = s.index("</o></c>", s.index("</microprocessor_definition>", i)) + len("</o></c>")
        vp = u.xyz(re.search(r"</microprocessor_definition><vp([^/]*)/>", s[a:e]).group(1))
        assert abs(vp[0]) == 5 and 2 <= vp[1] <= 6 and vp[2] == -59, ("unerwarteter Microcontroller", vp)
        s = s[:a] + s[e:]
        weg += 1
    print("Platzhalter entfernt: %d" % weg)
    tl = teile(s)
    # Platz frei? (alle Koerper)
    belegt = set(p for (_, p) in tl)
    # Reste des ersten Versuchs (03.10. 15:2x: die Chips waren in die Bausteinliste eines Quarter Panel geraten, das
    # Spiel machte daraus leere <c/>) entfernen
    if s.count("<c/>"):
        print("leere Bausteine <c/> entfernt: %d" % s.count("<c/>"))
        s = s.replace("<c/>", "")
    # 2. Chips einsetzen: ans Ende der Teileliste des Rumpf-Koerpers (der mit den meisten Teilen). ACHTUNG: Microcontroller
    # haben innen eigene <components>-Listen - das Ende der Rumpf-Liste ist das letzte </components> vor </body>
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
    for seite in ("L", "R"):
        teil, kn, (w, ln) = chip_teil(seite)
        vp, r = CHIPS[seite]
        R = [[int(v) for v in r.split(",")][i * 3:i * 3 + 3] for i in range(3)]
        flaeche = [tuple(vp[i] + R[0][i] * x + R[2][i] * z for i in range(3)) for x in range(w) for z in range(ln)]
        frei = [p for p in flaeche if p in belegt]
        assert not frei, ("Platz fuer Flak %s belegt" % seite, frei)
        neu_teile += teil
        chipkn[seite] = kn
        print("Flak %s eingesetzt: %d x %d, vp %s, Flaeche %s .. %s" % (seite, w, ln, vp, flaeche[0], flaeche[-1]))
    s = s[:einfueg] + neu_teile + s[einfueg:]
    # kein Microcontroller darf in einem anderen stecken
    for m in re.finditer(r"<microprocessor_definition ", s):
        assert s.find("<microprocessor_definition ", m.end()) > s.index("</microprocessor_definition>", m.end()) or             s.find("<microprocessor_definition ", m.end()) < 0, ("Microcontroller verschachtelt bei", m.start())
    # Rohr-Test fuer die erste Pruefung im Spiel einschalten
    if "--test-rohre" in sys.argv:
        for seite in ("L", "R"):
            i = s.index('<microprocessor_definition name="Figet Marena Flak %s"' % seite)
            e = s.index("</microprocessor_definition>", i)
            t = re.sub(r'(n="Test Rohre"><pos[^/]*/>)<v text="[^"]*"(?: value="[^"]*")?/>', r'\g<1><v text="1" value="1"/>', s[i:e])
            s = s[:i] + t + s[e:]
        print("Rohr-Test eingeschaltet")
    tl = teile(s)
    # 3. Kabel
    li, le = s.index("<logic_node_links>"), s.index("</logic_node_links>")
    alt = re.findall(r"<logic_node_link.*?</logic_node_link>", s[li:le])
    plan = []
    for seite in ("L", "R"):
        T, kn = TURM[seite], chipkn[seite]

        def ort(q, soll_ein):
            schl, lab = q
            if schl == "chip":
                p, ein = kn[lab]
                assert ein == soll_ein, ("Richtung Chip-Anschluss", lab)
                return p, None
            if schl == "SITZ":
                p, mo, ty = anschluss(tl, SITZ[0], SITZ[1], SITZ[2])
            elif schl == "PHYSIK":
                p, mo, ty = anschluss(tl, PHYSIK[0], PHYSIK[1], PHYSIK[2])
            else:
                p, mo, ty = anschluss(tl, T[schl][0], T[schl][1], lab)
            assert mo == (1 if soll_ein else 0), ("Richtung", q, mo)
            return p, ty

        for von, nach, typ in KABEL:
            p0, t0 = ort(von, False)
            p1, t1 = ort(nach, True)
            for tt in (t0, t1):
                assert tt is None or tt == typ, ("Typ passt nicht", von, nach, tt, typ)
            plan.append((typ, p0, p1, "Flak %s: %s %s -> %s %s" % (seite, von[0], von[1] or "", nach[0], nach[1] or "")))
        bp, bm, bt = anschluss(tl, BATT[seite][0], BATT[seite][1], "Electric Store")
        for schl in STROM:
            ep, em, et = anschluss(tl, T[schl][0], T[schl][1], "Electric")
            assert et == 4
            plan.append((4, bp, ep, "Flak %s: Strom Batterie -> %s" % (seite, T[schl][0])))
    zu = []
    for typ, p0, p1, was in plan:
        k = "<logic_node_link%s>%s%s</logic_node_link>" % (' type="%d"' % typ if typ else "", u.vox("voxel_pos_0", p0), u.vox("voxel_pos_1", p1))
        if k not in alt and k not in zu:
            zu.append(k)
        print("  %-62s %s -> %s%s" % (was, p0, p1, "  (schon da)" if k in alt else ""))
    s = s[:le] + "".join(zu) + s[le:]
    print("Kabel vorher %d, neu %d" % (len(alt), len(zu)))
    # 4. Turm-Radare in den manuellen Modus
    for seite in ("L", "R"):
        d, vp = TURM[seite]["radar"]
        m = re.search(r'<c d="%s"(?: t="\d+")?><o ([^>]*)>(?:(?!</c>).)*?%s' % (d, re.escape(u.vox("vp", vp))), s, re.S)
        o = m.group(1)
        o2 = re.sub(r' m_sweep_mode="\d+"', "", o) + ' m_sweep_mode="4"'
        s = s[:m.start(1)] + o2 + s[m.end(1):]
        print("Radar Flak %s: manueller Modus (%s)" % (seite, "war " + re.search(r'm_sweep_mode="(\d+)"', o).group(1) if "m_sweep_mode" in o else "neu"))
    # Probe: ohne Platzhalter/Chips/Kabel/Radar-Modus gleich
    def ohne(x):
        x = x.replace("<c/>", "").replace('n="Test Rohre"><pos x="-18" y="8"/><v text="1" value="1"/>', 'n="Test Rohre"><pos x="-18" y="8"/><v text="0"/>')
        x = re.sub(r'<c d="microprocessor"><o [^>]*><microprocessor_definition name="(Microcontroller|Figet Marena Flak [LR])".*?</o></c>', "", x, flags=re.S)
        x = x.replace(' m_sweep_mode="4"', "")
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0) == ohne(s), "ausser Platzhaltern/Chips/Kabeln/Radar-Modus geaendert"
    k0 = re.findall(r"<logic_node_link.*?</logic_node_link>", s0[s0.index("<logic_node_links>"):s0.index("</logic_node_links>")])
    k1 = re.findall(r"<logic_node_link.*?</logic_node_link>", s[s.index("<logic_node_links>"):s.index("</logic_node_links>")])
    assert k1[:len(k0)] == k0 and len(k1) == len(k0) + len(zu), "alte Kabel veraendert"
    print("Probe: nur Platzhalter weg, 2 Chips, %d neue Kabel, Radar-Modus" % len(zu))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
