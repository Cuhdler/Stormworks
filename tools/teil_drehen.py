"""Dreht ein Bauteil der Figet Marena an seiner Stelle (neue Drehung r) - nur fuer Teile, deren Flaeche und Anschluesse
dabei gleich bleiben (alle Anschluesse am vp, Flaeche symmetrisch um vp). Sonst aendert sich nichts.
Aufruf: python teil_drehen.py <teil> <x,y,z> <r neu> [--schreiben]
  z. B. python teil_drehen.py monitor_9 8,21,-23 0,0,-1,-1,0,0,0,1,0 --schreiben   (Monitor 9x5 um 180 Grad)
Achtung: ein Teil OHNE r-Attribut hat im Spiel die Drehung 0,0,1,-1,0,0,0,-1,0 (nicht die Grunddrehung)!
(vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
from autopilot_update import teil_bereich  # noqa: E402


def main():
    d, vp, r_neu = sys.argv[1], tuple(int(v) for v in sys.argv[2].split(",")), sys.argv[3]
    R = [[int(v) for v in r_neu.split(",")][i * 3:i * 3 + 3] for i in range(3)]
    det = (R[0][0] * (R[1][1] * R[2][2] - R[1][2] * R[2][1]) - R[0][1] * (R[1][0] * R[2][2] - R[1][2] * R[2][0])
           + R[0][2] * (R[1][0] * R[2][1] - R[1][1] * R[2][0]))
    assert det == 1, "keine Drehung (Determinante %d)" % det
    assert all(p == (0, 0, 0) for _, _, p in kf.def_knoten(d).values()), "Anschluesse nicht alle am vp"
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    a, e = teil_bereich(s0, d, vp)
    alt = s0[a:e]
    m = re.match(r'<c d="%s"(?: t="\d+")?><o ((?:r="([^"]*)" )?)' % d, alt)
    assert m, alt[:80]
    neu = alt[:m.start(1)] + 'r="%s" ' % r_neu + alt[m.end(1):]
    s = s0[:a] + neu + s0[e:]
    print("%s %s: r %s -> %s" % (d, vp, m.group(2) or "(keine = 0,0,1,-1,0,0,0,-1,0)", r_neu))
    assert s.replace(neu, alt, 1) == s0
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("Probe: nur dieses Teil gedreht; geschrieben:", ziel)


if __name__ == "__main__":
    main()
