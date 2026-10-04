"""Lagezentrale v2 (Andre 03.10. abends: "muss simpler werden"):
- "Figet Marena Lage" -> build_lage.VERSION: Mast-Radar 1 sucht, Radar 2-6 halten je ein Ziel (hoechstens 5; ein
  naeheres verdraengt das entfernteste); 'Ziel vergessen s' 4
- "Figet Marena Bildschirm" -> build_lage.VERSION_BILD: nur Anzeige (nichts antippen), rote Quadrate um beschossene
  Ziele; Waffen nehmen das naechste Ziel und wechseln nur bei weniger als halb so weit; Flaks nie dasselbe
- "Figet Marena Waffenwahl" -> build_lage.VERSION_WAHL: Anschluss 'Master Arm' ist jetzt Composite (Andres Instrument
  Panel, Flip Switch 1) statt Ein/Aus - erlaubt, weil er noch kein Kabel hat
- Kabel: Instrument Panel (-2, 19, -8) 'Out Signal' -> Waffenwahl 'Master Arm'
Lage, Kabel und Steckplaetze der Chips bleiben. Probe: sonst aendert sich nichts.
Aufruf: python lage2_update.py [--schreiben]   (vorher sichern; danach Schiff im Spiel neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import build_lage  # noqa: E402
import kabel_flak as kf  # noqa: E402
import kabel_lage as kl  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from chip_einsetzen import knoten  # noqa: E402
from flak_tauschen import werte, setze  # noqa: E402

TAUSCH = [("Figet Marena Lage", "Figet Marena Lage %s.xml" % build_lage.VERSION, {"Ziel vergessen s": 4}, None),
          ("Figet Marena Bildschirm", "Figet Marena Bildschirm %s.xml" % build_lage.VERSION_BILD, {}, None),
          ("Figet Marena Waffenwahl", "Figet Marena Waffenwahl %s.xml" % build_lage.VERSION_WAHL, {}, "Master Arm")]
PANEL = ("instrument_display", (-2, 19, -8))


def tausche(s, name, datei, vorgabe, darf_anders):
    a, e = u.mc_bereich(s, name)
    teil = s[a:e]
    d0 = teil.index("<microprocessor_definition")
    d1 = teil.index("</microprocessor_definition>") + len("</microprocessor_definition>")
    u.CHIP = os.path.join(BUILD, datei)
    neu = u.chip_eingebettet()
    ka, kn = knoten(teil[d0:d1]), knoten(neu)
    namen = re.findall(r'<node label="([^"]*)"', neu)
    assert len(ka) == len(kn), (name, "Anzahl Anschluesse geaendert")
    for i, (x, y) in enumerate(zip(ka, kn)):
        if x != y:
            assert namen[i] == darf_anders, (name, "Anschluss geaendert", namen[i])
            # nur erlaubt, wenn noch kein Kabel an diesem Anschluss haengt
            p = kl.vorhandener_chip(s, name)[namen[i]][0]
            assert u.vox("voxel_pos_1", p) not in s and u.vox("voxel_pos_0", p) not in s, (name, namen[i], "hat ein Kabel")
            print("  %s: Anschluss '%s' geaendert %s -> %s (ohne Kabel)" % (name, namen[i], x, y))
    alt_w, neu_w = werte(teil[d0:d1]), werte(neu)
    for n, v in alt_w.items():
        if n in neu_w and n not in vorgabe:
            neu = setze(neu, n, v)
    for n, v in vorgabe.items():
        neu = setze(neu, n, v)
    nw = werte(neu)
    print("%s -> %s: Eigenschaften neu/geaendert: %s; weg: %s" % (
        name, datei, {n: (alt_w.get(n), nw[n]) for n in nw if alt_w.get(n) != nw[n]}, sorted(set(alt_w) - set(nw))))
    return s[:a] + teil[:d0] + neu + teil[d1:] + s[e:]


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    for name, datei, vorgabe, frei in TAUSCH:
        s = tausche(s, name, datei, vorgabe, frei)
    # Kabel: Instrument Panel -> Waffenwahl 'Master Arm'
    tl = kf.teile(s)
    p0, mo, ty = kf.anschluss(tl, PANEL[0], PANEL[1], "Out Signal")
    assert mo == 0 and ty == 5, (mo, ty)
    p1, ein = kl.vorhandener_chip(s, "Figet Marena Waffenwahl")["Master Arm"]
    assert ein
    k = '<logic_node_link type="5">%s%s</logic_node_link>' % (u.vox("voxel_pos_0", p0), u.vox("voxel_pos_1", p1))
    li, le = s.index("<logic_node_links>"), s.index("</logic_node_links>")
    assert k not in s[li:le]
    s = s[:le] + k + s[le:]
    print("Kabel: Instrument Panel Out Signal %s -> Waffenwahl Master Arm %s" % (p0, p1))
    namen = "|".join(re.escape(n) for n, _, _, _ in TAUSCH)

    def ohne(x):
        x = re.sub(r'<microprocessor_definition name="(%s)".*?</microprocessor_definition>' % namen, "", x, flags=re.S)
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0) == ohne(s), "ausser Chips/Kabel geaendert"
    k0 = re.findall(r"<logic_node_link.*?</logic_node_link>", s0[s0.index("<logic_node_links>"):s0.index("</logic_node_links>")])
    k1 = re.findall(r"<logic_node_link.*?</logic_node_link>", s[s.index("<logic_node_links>"):s.index("</logic_node_links>")])
    assert k1[:len(k0)] == k0 and len(k1) == len(k0) + 1, "alte Kabel veraendert"
    print("Probe: nur 3 Chip-Definitionen und 1 Kabel")
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
