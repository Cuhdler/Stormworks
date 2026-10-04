"""Waffen-Runde 03.10. abends (Andres Test der Lage v1.1): Zuweisung/AUTO, Blick-Markieren, Waffenwahl-Monitor 2x3,
Flak folgt der Lagezentrale, Kameras richtig herum.

1. Chip-Definitionen tauschen (Lage, Kabel, Steckplaetze bleiben; Eigenschaften: Werte aus dem Schiff, ausser VORGABE):
   - "Figet Marena Lage" -> build_lage.VERSION ('Ziel vergessen s' 12 -> 6)
   - "Figet Marena Bildschirm" -> build_lage.VERSION_BILD: ein Anschluss mehr ('Wahl', hinten angehaengt; die alten
     bleiben gleich, ein Steckplatz dazu)
   - "Figet Marena Flak L/R" -> build_flak.VERSION (gleiche Anschluesse; 'Lage' bekommt jetzt ein Kabel)
2. Chip "Figet Marena Waffenwahl" (3 x 2) an die Rueckwand unter den Lage-Chip: vp (-4, 5, -59) -> x -4..-2, y 5..4
3. Kabel: Bildschirm 'Bedienung' -> Flak L 'Lage', Flak R 'Lage', Waffenwahl 'Bedienung'; Monitor 2x3 (auf dem
   Gelenk neben dem Sitz) Touch -> Waffenwahl 'Touch'; Waffenwahl 'Monitor' -> Video, 'Monitor an' -> Power Switch,
   'Wahl' -> Bildschirm 'Wahl'. Strom hat der 2x3 schon (ueber sein Gelenk von der rechten Batterie).
4. Die 4 Kameras (BC, AC vorn, Flak L/R) zeigten das Bild auf dem Kopf (Andres Bild: Himmel unten): um die Blickachse
   180 Grad drehen, r 1,0,0,0,0,1,0,-1,0 -> -1,0,0,0,0,1,0,1,0; die rechte Flak-Kamera war dazu gespiegelt (t 1) - weg.
   Gleiche Bloecke (die Kamera liegt auf der Blickachse), Anschluesse am Teil-Ursprung, Kabel bleiben.
Probe: sonst aendert sich nichts.
Aufruf: python waffen_update.py [--schreiben]   (vorher sichern; danach Schiff im Spiel neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import build_lage  # noqa: E402
import build_flak  # noqa: E402
import kabel_flak as kf  # noqa: E402
import kabel_lage as kl  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from chip_einsetzen import knoten  # noqa: E402
from flak_tauschen import werte, setze  # noqa: E402

TAUSCH = [("Figet Marena Lage", "Figet Marena Lage %s.xml" % build_lage.VERSION, {"Ziel vergessen s": 6}),
          ("Figet Marena Bildschirm", "Figet Marena Bildschirm %s.xml" % build_lage.VERSION_BILD, {}),
          ("Figet Marena Flak L", "Figet Marena Flak L %s.xml" % build_flak.VERSION, {}),
          ("Figet Marena Flak R", "Figet Marena Flak R %s.xml" % build_flak.VERSION, {})]
WAHL = ("Figet Marena Waffenwahl %s.xml" % build_lage.VERSION_WAHL, (-4, 5, -59), kl.R_WAND)
MON23 = ("monitor_2x3", (4, 18, -8))
KABEL = [
    (("Bildschirm", "Bedienung"), ("Flak L", "Lage"), 5),
    (("Bildschirm", "Bedienung"), ("Flak R", "Lage"), 5),
    (("Bildschirm", "Bedienung"), ("Waffenwahl", "Bedienung"), 5),
    (("MON23", "Touch Output"), ("Waffenwahl", "Touch"), 5),
    (("Waffenwahl", "Monitor"), ("MON23", "Video Signal"), 6),
    (("Waffenwahl", "Monitor an"), ("MON23", "Power Switch"), 0),
    (("Waffenwahl", "Wahl"), ("Bildschirm", "Wahl"), 5),
]
KAMERAS = [(4, 19, 11), (-4, 9, 35), (-15, 20, -99), (15, 20, -99)]
KAM_R = "-1,0,0,0,0,1,0,1,0"


def typ_von(k):
    m = re.search(r'<logic_node_link type="(\d+)"', k)
    return int(m.group(1)) if m else 0


def tausche(s, name, datei, vorgabe):
    a, e = u.mc_bereich(s, name)
    teil = s[a:e]
    d0 = teil.index("<microprocessor_definition")
    d1 = teil.index("</microprocessor_definition>") + len("</microprocessor_definition>")
    u.CHIP = os.path.join(BUILD, datei)
    neu = u.chip_eingebettet()
    ka, kn = knoten(teil[d0:d1]), knoten(neu)
    assert kn[:len(ka)] == ka, (name, "Anschluss-Lage/Typen geaendert - Kabel wuerden nicht mehr passen")
    alt_w, neu_w = werte(teil[d0:d1]), werte(neu)
    for n, v in alt_w.items():
        if n in neu_w and n not in vorgabe:
            neu = setze(neu, n, v)
    for n, v in vorgabe.items():
        neu = setze(neu, n, v)
    rest = teil[d1:]
    if len(kn) > len(ka):
        sl = "<logic_slots>%s</logic_slots>" % ("<slot/>" * len(ka))
        assert rest.count(sl) == 1, (name, "Steckplaetze unerwartet")
        rest = rest.replace(sl, "<logic_slots>%s</logic_slots>" % ("<slot/>" * len(kn)))
    nw = werte(neu)
    print("%s -> %s: %d Anschluesse (%+d); Eigenschaften neu/geaendert: %s; weg: %s" % (
        name, datei, len(kn), len(kn) - len(ka), {n: (alt_w.get(n), nw[n]) for n in nw if alt_w.get(n) != nw[n]},
        sorted(set(alt_w) - set(nw))))
    return s[:a] + teil[:d0] + neu + rest + s[e:]


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    assert '<microprocessor_definition name="Figet Marena Waffenwahl"' not in s, "Waffenwahl ist schon eingebaut"
    for name, datei, vorgabe in TAUSCH:
        s = tausche(s, name, datei, vorgabe)
    # Waffenwahl einsetzen (wie kabel_lage: Flaeche frei, Ende der Rumpf-Teileliste, nicht verschachtelt)
    tl = kf.teile(s)
    belegt = set(p for (_, p) in tl)
    for m in re.finditer(r'<c d="microprocessor"><o r="([^"]*)"[^>]*><microprocessor_definition [^>]*width="(\d+)" length="(\d+)"', s):
        e = s.index("</microprocessor_definition>", m.end())
        vp = u.xyz(re.match(r"<vp([^/]*)/>", s[e + len("</microprocessor_definition>"):]).group(1))
        R = [[int(v) for v in m.group(1).split(",")][i * 3:i * 3 + 3] for i in range(3)]
        for x in range(int(m.group(2))):
            for z in range(int(m.group(3))):
                belegt.add(tuple(vp[i] + R[0][i] * x + R[2][i] * z for i in range(3)))
    datei, vp, r = WAHL
    teil, kn_wahl, (w, ln) = kl.chip_teil(os.path.join(BUILD, datei), vp, r)
    R = [[int(v) for v in r.split(",")][i * 3:i * 3 + 3] for i in range(3)]
    flaeche = [tuple(vp[i] + R[0][i] * x + R[2][i] * z for i in range(3)) for x in range(w) for z in range(ln)]
    assert not [p for p in flaeche if p in belegt], ("Platz belegt", [p for p in flaeche if p in belegt])
    i0, e0 = s.index("<bodies>"), s.index("</bodies>")
    koerper, a = [], s.index("<body ", i0)
    while 0 <= a < e0:
        e = s.index("</body>", a)
        koerper.append((a, e))
        a = s.find("<body ", e)
    rumpf = max(koerper, key=lambda q: s.count('<c d="', q[0], q[1]))
    einfueg = s.rindex("</components>", rumpf[0], rumpf[1])
    s = s[:einfueg] + teil + s[einfueg:]
    print("Waffenwahl eingesetzt: %d x %d, vp %s, Flaeche %s .. %s" % (w, ln, vp, flaeche[0], flaeche[-1]))
    for m in re.finditer(r"<microprocessor_definition ", s):
        nxt = s.find("<microprocessor_definition ", m.end())
        assert nxt < 0 or nxt > s.index("</microprocessor_definition>", m.end()), ("Microcontroller verschachtelt", m.start())
    # Kabel
    chipkn = {"Waffenwahl": kn_wahl}
    for n in ("Bildschirm", "Flak L", "Flak R"):
        chipkn[n] = kl.vorhandener_chip(s, "Figet Marena " + n)
    tl = kf.teile(s)

    def ort(q, soll_ein):
        schl, lab = q
        if schl in chipkn:
            p, ein = chipkn[schl][lab]
            assert ein == soll_ein, ("Richtung Chip-Anschluss", q)
            return p, None
        p, mo, ty = kf.anschluss(tl, MON23[0], MON23[1], lab)
        assert mo == (1 if soll_ein else 0), ("Richtung", q, mo)
        return p, ty

    li, le = s.index("<logic_node_links>"), s.index("</logic_node_links>")
    alt = re.findall(r"<logic_node_link.*?</logic_node_link>", s[li:le])
    zu = []
    for von, nach, typ in KABEL:
        p0, t0 = ort(von, False)
        p1, t1 = ort(nach, True)
        for tt in (t0, t1):
            assert tt is None or tt == typ, ("Typ passt nicht", von, nach, tt, typ)
        k = "<logic_node_link%s>%s%s</logic_node_link>" % (' type="%d"' % typ if typ else "", u.vox("voxel_pos_0", p0), u.vox("voxel_pos_1", p1))
        # ein Eingang nimmt nur ein Kabel: keines gleicher Art darf schon dort enden
        schon = [x for x in alt if u.vox("voxel_pos_1", p1) in x and typ_von(x) == typ]
        assert not schon or k in alt, ("Eingang hat schon ein Kabel", nach, schon)
        if k not in alt:
            zu.append(k)
        print("  %-52s %s -> %s%s" % ("%s %s -> %s %s" % (von[0], von[1], nach[0], nach[1]), p0, p1, "" if k not in alt else "  (schon da)"))
    s = s[:le] + "".join(zu) + s[le:]
    print("Kabel vorher %d, neu %d" % (len(alt), len(zu)))
    # Kameras
    for p in KAMERAS:
        m = re.search(r'<c d="camera_med"( t="\d+")?><o r="([^"]*)"((?:(?!</c>).)*?%s)' % re.escape(u.vox("vp", p)), s, re.S)
        assert m and m.group(2) == "1,0,0,0,0,1,0,-1,0", ("Kamera", p)
        print("Kamera %s: t%s r %s -> r %s" % (p, m.group(1) or " -", m.group(2), KAM_R))
        s = s[:m.start()] + '<c d="camera_med"><o r="%s"' % KAM_R + m.group(3) + s[m.end():]
    # Probe
    def ohne(x):
        x = re.sub(r'<microprocessor_definition name="Figet Marena (Lage|Bildschirm|Flak [LR])".*?</microprocessor_definition>', "", x, flags=re.S)
        x = re.sub(r'<c d="microprocessor"><o [^>]*><microprocessor_definition name="Figet Marena Waffenwahl".*?</o></c>', "", x, flags=re.S)
        x = re.sub(r'<c d="camera_med"(?: t="\d+")?><o r="[^"]*"', '<c d="camera_med"><o', x)
        x = re.sub(r"<logic_slots>(<slot/>)+</logic_slots>", "<logic_slots/>", x)
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0) == ohne(s), "ausser Chips/Kabeln/Kameras geaendert"
    k0 = re.findall(r"<logic_node_link.*?</logic_node_link>", s0[s0.index("<logic_node_links>"):s0.index("</logic_node_links>")])
    k1 = re.findall(r"<logic_node_link.*?</logic_node_link>", s[s.index("<logic_node_links>"):s.index("</logic_node_links>")])
    assert k1[:len(k0)] == k0 and len(k1) == len(k0) + len(zu), "alte Kabel veraendert"
    print("Probe: nur 4 Chip-Definitionen, Waffenwahl-Chip, %d neue Kabel, 4 Kameras" % len(zu))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
