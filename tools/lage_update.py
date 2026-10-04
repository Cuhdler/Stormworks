"""Lagezentrale v1.1 + Schiff v3.3 in die Figet Marena (Andres Test 03.10.: Bild gespiegelt, Helm verdeckt den Monitor,
Ziele flackern):

- Chips "Figet Marena Lage", "... Bildschirm" (build_lage.VERSION) und "... Schiffsfuehrung" (build_schiff.MC_FILE)
  tauschen: nur die Definition; Lage, Kabel, Steckplaetze bleiben, die Anschluesse muessen gleich sein. Eigenschaften:
  Werte aus dem Schiff bleiben, neue bekommen ihren Standardwert.
- Mast-Radare: Strahl m_fov_x/y = build_lage.FOV
- Monitor 9x5: wie die meisten Monitore im Spiel ausrichten (r 1,0,0,0,0,-1,0,1,0, nicht gespiegelt). Andre hatte ihn
  gedreht eingebaut (Bild auf dem Kopf) und dann gespiegelt (t 4) - das richtete die Hoehe, links/rechts blieb vertauscht.
  Gleiche Flaeche (x -4..4, y 20..24) und gleicher Anschluss-Ort, die Kabel bleiben.
Probe: sonst aendert sich nichts.
Aufruf: python lage_update.py [--schreiben]   (vorher sichern; danach Schiff im Spiel neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import build_lage  # noqa: E402
import build_schiff  # noqa: E402
from build_schiff import BUILD  # noqa: E402
from chip_einsetzen import knoten  # noqa: E402
from flak_tauschen import werte, setze  # noqa: E402

CHIPS = [("Figet Marena Lage", "Figet Marena Lage %s.xml" % build_lage.VERSION),
         ("Figet Marena Bildschirm", "Figet Marena Bildschirm %s.xml" % build_lage.VERSION),
         ("Figet Marena Schiffsfuehrung", build_schiff.MC_FILE)]
MONITOR = ((0, 22, -6), "1,0,0,0,0,-1,0,1,0")


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    for name, datei in CHIPS:
        a, e = u.mc_bereich(s, name)
        teil = s[a:e]
        d0 = teil.index("<microprocessor_definition")
        d1 = teil.index("</microprocessor_definition>") + len("</microprocessor_definition>")
        u.CHIP = os.path.join(BUILD, datei)
        neu = u.chip_eingebettet()
        assert knoten(teil[d0:d1]) == knoten(neu), (name, "Anschluss-Lage/Typen geaendert - Kabel wuerden nicht mehr passen")
        alt_w, neu_w = werte(teil[d0:d1]), werte(neu)
        for n, v in alt_w.items():
            if n in neu_w:
                neu = setze(neu, n, v)
        geaendert = {n: (alt_w.get(n), werte(neu)[n]) for n in werte(neu) if alt_w.get(n) != werte(neu)[n]}
        print("%s -> %s: Anschluesse gleich; Eigenschaften neu/geaendert: %s" % (name, datei, geaendert))
        s = s[:a] + teil[:d0] + neu + teil[d1:] + s[e:]
    # Mast-Radare
    for k, (pos, _, _, _) in enumerate(build_lage.RADARE):
        m = re.search(r'<c d="radar_advanced_phalanx"(?: t="\d+")?><o ([^>]*)>(?:(?!</c>).)*?%s' % re.escape(u.vox("vp", pos)), s, re.S)
        o = m.group(1)
        o2 = re.sub(r'm_fov_x="[^"]*"', 'm_fov_x="%s"' % build_lage.FOV, o)
        o2 = re.sub(r'm_fov_y="[^"]*"', 'm_fov_y="%s"' % build_lage.FOV, o2)
        assert 'm_sweep_mode="4"' in o2
        s = s[:m.start(1)] + o2 + s[m.end(1):]
        print("Radar %d %s: %s" % (k + 1, pos, o2))
    # Monitor
    vp, r = MONITOR
    m = re.search(r'<c d="monitor_9"( t="\d+")?><o r="([^"]*)"((?:(?!</c>).)*?%s)' % re.escape(u.vox("vp", vp)), s, re.S)
    assert m, "Monitor 9x5 nicht gefunden"
    print("Monitor 9x5 %s: t%s r %s -> ohne t, r %s" % (vp, m.group(1) or " -", m.group(2), r))
    s = s[:m.start()] + '<c d="monitor_9"><o r="%s"' % r + m.group(3) + s[m.end():]
    # Probe
    def ohne(x):
        for name, _ in CHIPS:
            x = re.sub(r'<microprocessor_definition name="%s".*?</microprocessor_definition>' % name, "", x, flags=re.S)
        x = re.sub(r'(<c d="radar_advanced_phalanx"(?: t="\d+")?><o [^>]*?) m_fov_x="[^"]*" m_fov_y="[^"]*"', r"\g<1>", x)
        x = re.sub(r'<c d="monitor_9"(?: t="\d+")?><o r="[^"]*"', '<c d="monitor_9"><o', x)
        return x
    assert ohne(s0) == ohne(s), "ausser Chips/Radar-Strahl/Monitor geaendert"
    print("Probe: nur 3 Chip-Definitionen, 6 Radar-Strahlen, Monitor-Lage")
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
