"""Anti-Schiffs-Kanonen vorn einbauen (Andre 04.10.: "lass uns jetzt die Anti-Schiffs-Kanonen machen"; "du kannst
Microcontroller nach Belieben bearbeiten/loeschen/neu bauen/verschieben"):
- die vier Waffen-Chips wie lage22_update tauschen (Lage, Bildschirm v3.2 mit Reichweite je Waffe, Flak v2.2)
- Chips "Figet Marena Kanone BC" und "... AC" (4 x 5) an die Seitenwaende des Chip-Raums ueber die Flak-Chips:
  BC links  vp (-5, 13, -58), r 0,-1,0,1,0,0,0,0,1 -> Feld (x, z) = Welt (-5, 13-x, -58+z)  (y 13..10)
  AC rechts vp (5, 10, -58),  r 0,1,0,-1,0,0,0,0,1 -> Feld (x, z) = Welt (5, 10+x, -58+z)   (y 10..13)
- Kabel je Turm: Physik-Sensor, Turm-Radar (Daten, Drehung, Gimbal, an), Drehkranz, beide Hoehen-Pivots, Geschuetz
  (Abzug, Zuender, Loaded; BC: Verschluss), Zufuehrung, Kamera-Pivot, Bildschirm 'Bedienung' -> 'Lage'; Strom (BC von
  der linken, AC von der rechten Batterie) an alle Teile ausser Kamera (hat schon) und Laser (noch nicht gebraucht)
- Turm-Radare in den manuellen Modus (m_sweep_mode 4 wie die Flak-Radare)
v1.1 (Andre 04.10.: "die Kanonen haben sich nicht bewegt ... bei der Battle Cannon ist einer der 2 Laeufe nicht
verbunden; beide Rohre haben dasselbe Magazin, von einer Junction geteilt - die muss auch Input bekommen"): sind die
Kanonen-Chips schon eingebaut, fliegen sie samt ihren Kabeln raus und werden neu gesetzt; BC jetzt 4 x 6 mit zweitem
Rohr (Abzug, Zuender, Loaded, Verschluss), zweitem Zufuehrer (Feed, Strom) und Weiche (Junction Switch).
Probe: ausser den Chip-Definitionen, den Kanonen-Chips, ihren Kabeln und dem Radar-Modus aendert sich nichts.
Aufruf: python kabel_kanone.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import build_kanone  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from lage22_update import TAUSCH  # noqa: E402
from waffen_update import tausche  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402

CHIPS = {"BC": ((-5, 13, -58), "0,-1,0,1,0,0,0,0,1"), "AC": ((5, 10, -58), "0,1,0,-1,0,0,0,0,1")}
BATT = {"BC": kf.BATT["L"], "AC": kf.BATT["R"]}
TURM = {
    "BC": {"radar": ("radar_advanced", (0, 17, 11)), "ring": ("multibody_turret_large_a", (0, 10, 5)),
           "piv_l": ("multibody_robotic_pivot_01_a", (-4, 14, 9)), "piv_r": ("multibody_robotic_pivot_01_a", (4, 14, 9)),
           "gun": ("gun_l", (-2, 14, 9)), "lad": ("gun_belt_loader_l", (-1, 14, 7)),
           "gun_r": ("gun_l", (2, 14, 9)), "lad_r": ("gun_belt_loader_l", (1, 14, 7)),
           "weiche": ("gun_belt_junction_l", (0, 14, 7)),
           "kpiv": ("multibody_compact_pivot_robotic_a", (4, 18, 12))},
    "AC": {"radar": ("radar_advanced", (0, 12, 35)), "ring": ("multibody_turret_medium_a", (0, 6, 31)),
           "piv_l": ("multibody_robotic_pivot_01_a", (-2, 9, 34)), "piv_r": ("multibody_robotic_pivot_01_a", (2, 9, 34)),
           "gun": ("gun_m", (0, 9, 34)), "lad": ("gun_belt_loader", (0, 8, 34)),
           "kpiv": ("multibody_compact_pivot_robotic_a", (-3, 8, 36))},
}
KABEL = [
    (("PHYSIK", None), ("chip", "Physik-Sensor"), 5),
    (("BILD", "Bedienung"), ("chip", "Lage"), 5),
    (("radar", "Radar Data"), ("chip", "Radar"), 5),
    (("radar", "Radar Rotation"), ("chip", "Radar Drehung"), 1),
    (("ring", "Current Rotation"), ("chip", "Turm Drehung"), 1),
    (("gun", "Loaded"), ("chip", "Geladen"), 0),
    (("chip", "Turm Tempo"), ("ring", "Rotational Speed"), 1),
    (("chip", "Hoehe Rohr links"), ("piv_l", "Rotation Target"), 1),
    (("chip", "Hoehe Rohr rechts"), ("piv_r", "Rotation Target"), 1),
    (("chip", "Zuender"), ("gun", "Fuse Timer"), 1),
    (("chip", "Feuer"), ("gun", "Trigger"), 0),
    (("chip", "Zufuehrung"), ("lad", "Feed"), 0),
    (("chip", "Radar an"), ("radar", "Activate"), 0),
    (("chip", "Radar Gimbal"), ("radar", "Gimbal Input"), 5),
    (("chip", "Kamera Hoehe"), ("kpiv", "Rotation Target"), 1),
]
NUR_BC = [(("chip", "Verschluss"), ("gun", "Open Breech"), 0),
          (("gun_r", "Loaded"), ("chip", "Geladen rechts"), 0),
          (("chip", "Zuender"), ("gun_r", "Fuse Timer"), 1),
          (("chip", "Feuer rechts"), ("gun_r", "Trigger"), 0),
          (("chip", "Verschluss rechts"), ("gun_r", "Open Breech"), 0),
          (("chip", "Zufuehrung"), ("lad_r", "Feed"), 0),
          (("chip", "Weiche"), ("weiche", "Junction Switch"), 0)]


def chip_teil(name, datei):
    """Fertiges Bauteil <c d="microprocessor">...</c> und die Flaeche, die es belegt."""
    u.CHIP = os.path.join(BUILD, datei)
    d = u.chip_eingebettet()
    w = int(re.search(r'<microprocessor_definition [^>]*width="(\d+)"', d).group(1))
    ln = int(re.search(r'<microprocessor_definition [^>]*length="(\d+)"', d).group(1))
    vp, r = CHIPS[name]
    nk = len(re.findall(r"<n id=", d))
    teil = '<c d="microprocessor"><o r="%s" sc="%d">%s%s<logic_slots>%s</logic_slots></o></c>' % (
        r, 2 * w * ln + 2 * (w + ln), d, u.vox("vp", vp), "<slot/>" * nk)
    R = [[int(v) for v in r.split(",")][i * 3:i * 3 + 3] for i in range(3)]
    flaeche = [tuple(vp[i] + R[0][i] * x + R[2][i] * z for i in range(3)) for x in range(w) for z in range(ln)]
    return teil, flaeche


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    for name, datei, vorgabe in TAUSCH:
        s = tausche(s, name, datei, vorgabe)
    # v1.1: alte Kanonen-Chips samt Kabeln entfernen
    weg_kabel = []
    for name in ("BC", "AC"):
        tag = '<microprocessor_definition name="Figet Marena Kanone %s"' % name
        if tag not in s:
            continue
        orte = set(chip_knoten(s, "Figet Marena Kanone %s" % name).values())
        i = s.index(tag)
        a = s.rindex('<c d="microprocessor"><o ', 0, i)
        e = s.index("</o></c>", s.index("</microprocessor_definition>", i)) + len("</o></c>")
        s = s[:a] + s[e:]
        li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
        alle = re.findall(r"<logic_node_link[ >].*?</logic_node_link>", s[li:le])
        bleibt = []
        for k in alle:
            p0 = u.xyz(re.search(r"<voxel_pos_0([^/]*)/>", k).group(1))
            p1 = u.xyz(re.search(r"<voxel_pos_1([^/]*)/>", k).group(1))
            (weg_kabel if p0 in orte or p1 in orte else bleibt).append(k)
        assert "".join(alle) == s[li:le], "Kabelliste nicht vollstaendig erfasst"
        s = s[:li] + "".join(bleibt) + s[le:]
        print("alter Chip Kanone %s entfernt" % name)
    print("alte Kanonen-Kabel entfernt: %d" % len(weg_kabel))
    # 1. Chips einsetzen (Flaeche frei? - alle Koerper inkl. Bloecke, alle Chips)
    import sperrprofil
    # Teile von der Platte (ohne Microcontroller - die Chips zaehlen unten aus dem bearbeiteten Stand)
    belegt = set(p for teile in sperrprofil.koerper() for d, p in teile if d != "microprocessor")
    for m in re.finditer(r'<c d="microprocessor"><o r="([^"]*)"[^>]*><microprocessor_definition [^>]*width="(\d+)" length="(\d+)"', s):
        e = s.index("</microprocessor_definition>", m.end())
        vp = u.xyz(re.match(r"<vp([^/]*)/>", s[e + len("</microprocessor_definition>"):]).group(1))
        R = [[int(float(v)) for v in m.group(1).split(",")][i * 3:i * 3 + 3] for i in range(3)]
        belegt |= set(tuple(vp[i] + R[0][i] * x + R[2][i] * z for i in range(3)) for x in range(int(m.group(2)))
                      for z in range(int(m.group(3))))
    i0, e0 = s.index("<bodies>"), s.index("</bodies>")
    koerper = []
    a = s.index("<body ", i0)
    while 0 <= a < e0:
        e = s.index("</body>", a)
        koerper.append((a, e))
        a = s.find("<body ", e)
    rumpf = max(koerper, key=lambda q: s.count('<c d="', q[0], q[1]))
    einfueg = s.rindex("</components>", rumpf[0], rumpf[1])
    neu = ""
    for name in ("BC", "AC"):
        teil, flaeche = chip_teil(name, "Figet Marena Kanone %s %s.xml" % (name, build_kanone.VERSION))
        voll = [p for p in flaeche if p in belegt]
        assert not voll, ("Platz fuer Kanone %s belegt" % name, voll)
        neu += teil
        print("Kanone %s eingesetzt: vp %s, Flaeche %s .. %s" % (name, CHIPS[name][0], flaeche[0], flaeche[-1]))
    s = s[:einfueg] + neu + s[einfueg:]
    for m in re.finditer(r"<microprocessor_definition ", s):
        nxt = s.find("<microprocessor_definition ", m.end())
        assert nxt < 0 or nxt > s.index("</microprocessor_definition>", m.end()), ("Chip verschachtelt", m.start())
    # 2. Kabel
    tl = kf.teile(s)
    bild = chip_knoten(s, "Figet Marena Bildschirm")
    li, le = s.index("<logic_node_links>"), s.index("</logic_node_links>")
    alt = re.findall(r"<logic_node_link.*?</logic_node_link>", s[li:le])
    # belegte Eingaenge je Kabeltyp (an einer Stelle liegen oft mehrere Anschluesse, z. B. Strom und Drehzahl)
    belegte_eing = set((int(t or 0), p1) for t, p1 in re.findall(r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0[^>]*/>(<voxel_pos_1[^>]*/>)',
                                                                  s[li:le]))
    plan = []
    for name in ("BC", "AC"):
        T, kn = TURM[name], chip_knoten(s, "Figet Marena Kanone %s" % name)
        ein = set(re.findall(r'<node label="([^"]*)"[^>]*mode="1"', s[s.index('<microprocessor_definition name="Figet Marena Kanone %s"' % name):]
                             .split("</microprocessor_definition>")[0]))

        def ort(q, soll_ein):
            schl, lab = q
            if schl == "chip":
                assert (lab in ein) == soll_ein, ("Richtung Chip-Anschluss", name, lab)
                return kn[lab], None
            if schl == "PHYSIK":
                p, mo, ty = kf.anschluss(tl, kf.PHYSIK[0], kf.PHYSIK[1], kf.PHYSIK[2])
            elif schl == "BILD":
                return bild[lab], None
            else:
                p, mo, ty = kf.anschluss(tl, T[schl][0], T[schl][1], lab)
            assert mo == (1 if soll_ein else 0), ("Richtung", name, q, mo)
            return p, ty

        for von, nach, typ in KABEL + (NUR_BC if name == "BC" else []):
            p0, t0 = ort(von, False)
            p1, t1 = ort(nach, True)
            for tt in (t0, t1):
                assert tt is None or tt == typ, ("Typ passt nicht", name, von, nach, tt, typ)
            if nach[0] != "chip":
                assert (typ, u.vox("voxel_pos_1", p1)) not in belegte_eing, ("Eingang schon belegt", name, nach, p1)
            plan.append((typ, p0, p1, "Kanone %s: %s %s -> %s %s" % (name, von[0], von[1] or "", nach[0], nach[1] or "")))
        bp, bm, bt = kf.anschluss(tl, BATT[name][0], BATT[name][1], "Electric Store")
        for schl in ("radar", "ring", "piv_l", "piv_r", "gun", "lad", "kpiv") + (("gun_r", "lad_r") if name == "BC" else ()):
            d, vp = T[schl]
            if "Electric" not in kf.def_knoten(d):
                print("  %s: %s braucht keinen Strom" % (name, d))
                continue
            ep, em, et = kf.anschluss(tl, d, vp, "Electric")
            assert et == 4
            plan.append((4, bp, ep, "Kanone %s: Strom Batterie -> %s" % (name, d)))
    zu = []
    for typ, p0, p1, was in plan:
        k = "<logic_node_link%s>%s%s</logic_node_link>" % (' type="%d"' % typ if typ else "", u.vox("voxel_pos_0", p0),
                                                          u.vox("voxel_pos_1", p1))
        if k in alt:
            assert typ == 4, ("Kabel schon da", was)
            print("  %-62s schon da" % was)
            continue
        zu.append(k)
        print("  %-62s %s -> %s" % (was, p0, p1))
    s = s[:le] + "".join(zu) + s[le:]
    print("Kabel vorher %d, neu %d" % (len(alt), len(zu)))
    # 3. Turm-Radare in den manuellen Modus
    for name in ("BC", "AC"):
        d, vp = TURM[name]["radar"]
        m = re.search(r'<c d="%s"(?: t="\d+")?><o ([^>]*)>(?:(?!</c>).)*?%s' % (d, re.escape(u.vox("vp", vp))), s, re.S)
        o = m.group(1)
        o2 = re.sub(r' m_sweep_mode="\d+"', "", o) + ' m_sweep_mode="4"'
        s = s[:m.start(1)] + o2 + s[m.end(1):]
        print("Radar %s: manueller Modus (%s)" % (name, "war " + re.search(r'm_sweep_mode="(\d+)"', o).group(1)
                                                    if "m_sweep_mode" in o else "neu"))
    # Probe
    namen = "|".join(re.escape(n) for n, _, _ in TAUSCH)

    def ohne(x):
        x = re.sub(r'<microprocessor_definition name="(%s)".*?</microprocessor_definition>' % namen, "", x, flags=re.S)
        x = re.sub(r'<c d="microprocessor"><o [^>]*><microprocessor_definition name="Figet Marena Kanone (BC|AC)".*?</o></c>',
                   "", x, flags=re.S)
        for name in ("BC", "AC"):
            vp = TURM[name]["radar"][1]
            x = re.sub(r'(<c d="radar_advanced"(?: t="\d+")?><o [^>]*?) m_sweep_mode="4"(>(?:(?!</c>).)*?%s)' % re.escape(u.vox("vp", vp)),
                       r"\1\2", x, flags=re.S)
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0) == ohne(s), "ausser Chips/Kabeln/Radar-Modus geaendert"
    k0 = re.findall(r"<logic_node_link.*?</logic_node_link>", s0[s0.index("<logic_node_links>"):s0.index("</logic_node_links>")])
    k1 = re.findall(r"<logic_node_link.*?</logic_node_link>", s[s.index("<logic_node_links>"):s.index("</logic_node_links>")])
    rest = [k for k in k0 if k not in weg_kabel]
    if rest != k1[:len(rest)] or len(k1) != len(rest) + len(zu):
        i = next((j for j, (a_, b_) in enumerate(zip(rest, k1)) if a_ != b_), None)
        print("ABWEICHUNG", len(k0), len(weg_kabel), len(rest), len(zu), len(k1), i, rest[i] if i is not None else None,
              k1[i] if i is not None else None)
        raise AssertionError("andere Kabel veraendert")
    print("Probe: nur %d Chip-Definitionen, Kanonen-Chips neu, %d alte Kabel weg, %d neue, Radar-Modus" % (
        len(TAUSCH), len(weg_kabel), len(zu)))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
