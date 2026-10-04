"""Lage v3.2 (Bodenziele) + Auto-Zoom (Flak v2.6, Kanone v1.4) ins Schiff (Andre 04.10.: "2 Testlaeufe, bei beiden
wurden auch Bodenziele beschossen, fixe und optimiere; als neues Feature ein Automatik-Zoom, der mit der bekannten
Entfernung so an das Ziel zoomt, dass man es gut erkennen kann"):
- Chips tauschen wie bc_lader_update (Lage v3.2: Land ist nie Kanonen-Ziel; Flak/Kanonen: neuer Ausgang 'Kamera Zoom'
  am Ende; der BC-Chip waechst dafuer von 4 x 6 auf 4 x 7 - die neue Reihe muss frei sein)
- vier Kabel: 'Kamera Zoom' jedes Turm-Chips -> 'Field of View' seiner Camera Medium
Probe: ausser den Chip-Definitionen, Steckplaetzen, der BC-Groesse und diesen vier Kabeln aendert sich nichts.
Aufruf: python zoom_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import sperrprofil  # noqa: E402
from kanone_update import TAUSCH  # noqa: E402
from waffen_update import tausche  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402

KAMERAS = {"Figet Marena Kanone BC": (4, 19, 11), "Figet Marena Kanone AC": (-4, 9, 35),
           "Figet Marena Flak L": kf.TURM["L"]["kam"][1], "Figet Marena Flak R": kf.TURM["R"]["kam"][1]}


def chip_lage(s, name):
    """(Anfang des <c>, r-Matrix, vp, Breite, Laenge, sc) eines eingebauten Chips."""
    i = s.index('<microprocessor_definition name="%s"' % name)
    a = s.rindex('<c d="microprocessor"><o ', 0, i)
    m = re.match(r'<c d="microprocessor"><o r="([^"]*)" sc="(\d+)">', s[a:])
    R = [[int(float(v)) for v in m.group(1).split(",")][k * 3:k * 3 + 3] for k in range(3)]
    w, ln = map(int, re.match(r'<microprocessor_definition [^>]*width="(\d+)" length="(\d+)"', s[i:]).groups())
    e = s.index("</microprocessor_definition>", i)
    vp = u.xyz(re.match(r"<vp([^/]*)/>", s[e + len("</microprocessor_definition>"):]).group(1))
    return a, R, vp, w, ln, int(m.group(2))


def flaeche(R, vp, w, ln):
    return set(tuple(vp[k] + R[0][k] * x + R[2][k] * z for k in range(3)) for x in range(w) for z in range(ln))


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    _, R, vp, w0, l0, _ = chip_lage(s, "Figet Marena Kanone BC")
    alt_fl = flaeche(R, vp, w0, l0)
    for name, datei, vorgabe in TAUSCH:
        s = tausche(s, name, datei, vorgabe)
    # BC-Chip groesser: neue Felder frei? (alle Teile ausser Microcontrollern + alle anderen Chips)
    a, R, vp, w, ln, sc = chip_lage(s, "Figet Marena Kanone BC")
    neu_fl = flaeche(R, vp, w, ln) - alt_fl
    belegt = set(p for teile in sperrprofil.koerper() for d, p in teile if d != "microprocessor")
    for m in re.finditer(r'<microprocessor_definition name="([^"]*)"', s):
        if m.group(1) == "Figet Marena Kanone BC":
            continue
        try:
            _, R2, vp2, w2, l2, _ = chip_lage(s, m.group(1))
        except (ValueError, AttributeError):
            continue
        belegt |= flaeche(R2, vp2, w2, l2)
    voll = sorted(p for p in neu_fl if p in belegt)
    assert not voll, ("neue BC-Reihe belegt", voll)
    sc_neu = 2 * w * ln + 2 * (w + ln)
    kopf_alt = s[a:s.index(">", s.index("<o ", a)) + 1]
    kopf_neu = kopf_alt.replace(' sc="%d"' % sc, ' sc="%d"' % sc_neu)
    assert kopf_neu != kopf_alt or sc == sc_neu
    s = s[:a] + kopf_neu + s[a + len(kopf_alt):]
    print("BC-Chip %d x %d -> %d x %d, neue Felder %s frei, sc %d -> %d" % (w0, l0, w, ln, sorted(neu_fl), sc, sc_neu))
    # Kabel
    tl = kf.teile(s)
    li, le = s.index("<logic_node_links>"), s.index("</logic_node_links>")
    alt = s[li:le]
    zu = []
    for chip, kvp in KAMERAS.items():
        p0 = chip_knoten(s, chip)["Kamera Zoom"]
        p1, mo, ty = kf.anschluss(tl, "camera_med", kvp, "Field of View")
        assert mo == 1 and ty == 1, ("Field of View", chip, mo, ty)
        assert '<logic_node_link type="1">%s' % u.vox("voxel_pos_0", p0) not in alt, ("Chip-Ausgang schon belegt", chip)
        assert u.vox("voxel_pos_1", p1) + "</logic_node_link>" not in alt.replace("<logic_node_link>", "") or \
            not re.search(r'<logic_node_link type="1"><voxel_pos_0[^>]*/>%s' % re.escape(u.vox("voxel_pos_1", p1)), alt), \
            ("Field of View schon belegt", chip)
        k = '<logic_node_link type="1">%s%s</logic_node_link>' % (u.vox("voxel_pos_0", p0), u.vox("voxel_pos_1", p1))
        zu.append(k)
        print("Kabel: %s 'Kamera Zoom' %s -> Camera Medium %s 'Field of View' %s" % (chip, p0, kvp, p1))
    s = s[:le] + "".join(zu) + s[le:]
    namen = "|".join(re.escape(n) for n, _, _ in TAUSCH)

    def ohne(x):
        x = re.sub(r'<microprocessor_definition name="(%s)".*?</microprocessor_definition>' % namen, "", x, flags=re.S)
        x = re.sub(r"<logic_slots>(<slot(?: editor_connected=\"1\")?/>)*</logic_slots>", "<logic_slots/>", x)
        x = re.sub(r'<c d="microprocessor"><o r="([^"]*)" sc="\d+">', r'<c d="microprocessor"><o r="\1" sc="">', x)
        for k in zu:
            x = x.replace(k, "")
        return x
    assert ohne(s0) == ohne(s), "ausser Chip-Definitionen, Steckplaetzen, Chip-Groesse und den vier Kabeln geaendert"
    print("Probe: nur %d Chip-Definitionen, Steckplaetze, BC-Groesse und %d neue Kabel" % (len(TAUSCH), len(zu)))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
