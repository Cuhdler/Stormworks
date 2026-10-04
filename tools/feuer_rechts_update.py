"""Flak v2.0 ins Schiff (04.10., Andre: "die Flak-Turm-Kanonen sollen abwechselnd feuern"):
- die vier Waffen-Chips wie lage22_update tauschen (Flak bekommt den neuen Anschluss 'Feuer rechts' am Ende)
- je Flak-Turm das Kabel 'Feuer' -> Trigger des RECHTEN Rohrs auf 'Feuer rechts' umlegen ('Feuer' bleibt am linken)
Probe: ausser den Chip-Definitionen und diesen zwei Kabeln aendert sich nichts.
Aufruf: python feuer_rechts_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
from lage22_update import TAUSCH  # noqa: E402
from waffen_update import tausche  # noqa: E402


def chip_knoten(s, name):
    """Welt-Positionen der Anschluesse eines eingebauten Chips (Name -> (x, y, z))."""
    i = s.index('<microprocessor_definition name="%s"' % name)
    a = s.rindex('<c d="microprocessor"><o ', 0, i)
    r = re.match(r'<c d="microprocessor"><o r="([^"]*)"', s[a:])
    R = [[int(float(v)) for v in r.group(1).split(",")][k * 3:k * 3 + 3] for k in range(3)]
    e = s.index("</microprocessor_definition>", i)
    vp = u.xyz(re.match(r"<vp([^/]*)/>", s[e + len("</microprocessor_definition>"):]).group(1))
    out = {}
    for m in re.finditer(r'<node label="([^"]*)"[^>]*?(?:/>|><position([^/]*)/></node>)', s[i:e]):
        pa = dict(re.findall(r'(\w)="(-?\d+)"', m.group(2) or ""))
        x, z = int(pa.get("x", 0)), int(pa.get("z", 0))
        out[m.group(1)] = tuple(vp[k] + R[0][k] * x + R[2][k] * z for k in range(3))
    return out


def kabel(p0, p1):
    return "<logic_node_link>%s%s</logic_node_link>" % (u.vox("voxel_pos_0", p0), u.vox("voxel_pos_1", p1))


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    for name, datei, vorgabe in TAUSCH:
        s = tausche(s, name, datei, vorgabe)
    tl = kf.teile(s)
    umgelegt = []
    for seite in ("L", "R"):
        kn = chip_knoten(s, "Figet Marena Flak %s" % seite)
        d, vp = kf.TURM[seite]["gun_r"]
        abzug, mo, ty = kf.anschluss(tl, d, vp, "Trigger")
        assert mo == 1 and ty == 0, ("Trigger rechts", seite, mo, ty)
        alt, neu = kabel(kn["Feuer"], abzug), kabel(kn["Feuer rechts"], abzug)
        li, le = s.index("<logic_node_links>"), s.index("</logic_node_links>")
        if s[li:le].count(neu) == 1 and s[li:le].count(alt) == 0:
            print("Flak %s: schon umgelegt" % seite)
            continue
        assert s[li:le].count(alt) == 1, ("Kabel Feuer -> rechtes Rohr nicht genau einmal gefunden", seite, s[li:le].count(alt))
        assert s[li:le].count(kabel(kn["Feuer"], kf.anschluss(tl, *kf.TURM[seite]["gun_l"], "Trigger")[0])) == 1, \
            ("Kabel Feuer -> linkes Rohr fehlt", seite)
        j = s.index(alt, li)
        s = s[:j] + neu + s[j + len(alt):]
        umgelegt.append((alt, neu))
        print("Flak %s: rechtes Rohr (Trigger %s) jetzt an 'Feuer rechts' %s statt 'Feuer' %s" % (
            seite, abzug, kn["Feuer rechts"], kn["Feuer"]))
    namen = "|".join(re.escape(n) for n, _, _ in TAUSCH)

    def ohne(x):
        x = re.sub(r'<microprocessor_definition name="(%s)".*?</microprocessor_definition>' % namen, "", x, flags=re.S)
        x = re.sub(r"<logic_slots>(<slot/>)*</logic_slots>", "<logic_slots/>", x)
        for alt, neu in umgelegt:
            x = x.replace(neu, alt)
        return x
    assert ohne(s0) == ohne(s), "ausser Chip-Definitionen, Steckplaetzen und den umgelegten Kabeln geaendert"
    print("Probe: nur %d Chip-Definitionen und %d umgelegte Kabel" % (len(TAUSCH), len(umgelegt)))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
