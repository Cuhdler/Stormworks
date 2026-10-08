"""Abteile v1.3 / Sammler v1.1 ins Schiff (Andre 08.10.: "das waren die Sensoren fuer den Sprit, das ist der Tank; solche
Daten sollten mit auf den 2. grossen Bildschirm: Batterie, Sprit etc."):
- Chip-Definitionen getauscht (Anschluesse gleich, Abteile hinten + 'Batterie 1/2'); Eigenschaften bleiben
- Kabel: Charge der Batterie gross (-4,-13,-46) und mittel (-8,-19,-65) -> 'Batterie 1/2' (alle 6 in einem Netz)
Probe: ausser den zwei Chips und den 2 Kabeln aendert sich nichts.
Aufruf: python abteile13_update.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import kabel_flak as kf  # noqa: E402
import build_abteile as ba  # noqa: E402
from waffen_update import tausche  # noqa: E402
from feuer_rechts_update import chip_knoten  # noqa: E402
from autopilot_update import link, LINKS  # noqa: E402

SA, AB = "Figet Marena Abteile Sammler", "Figet Marena Abteile"


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    assert 'description="Abteile v1.2' in s0 and 'description="Abteile Sammler v1.0' in s0, "Stand passt nicht"
    kn0 = {n: chip_knoten(s0, n) for n in (SA, AB)}
    s = tausche(s0, AB, "%s %s.xml" % (AB, ba.VERSION), {})
    s = tausche(s, SA, "%s %s.xml" % (SA, ba.VERSION_SAMMLER), {})
    for n in (SA, AB):
        kn = chip_knoten(s, n)
        assert all(kn[k] == p for k, p in kn0[n].items()), (n, "Anschluesse verschoben")
    ka = chip_knoten(s, AB)
    tl = kf.teile(s)
    neu = []
    for k, (d, vp) in enumerate(ba.BATTERIEN):
        p, mo, ty = kf.anschluss(tl, d, vp, "Charge")
        assert (mo, ty) == (0, 1), (d, mo, ty)
        neu.append(link(1, p, ka["Batterie %d" % (k + 1)]))
        print("  %s %s Charge %s -> Abteile 'Batterie %d' %s" % (d, vp, p, k + 1, ka["Batterie %d" % (k + 1)]))
    li, le = s.index("<logic_node_links>") + len("<logic_node_links>"), s.index("</logic_node_links>")
    alt_l = re.findall(LINKS, s[li:le])
    assert "".join(alt_l) == s[li:le]
    s = s[:li] + "".join(alt_l + neu) + s[le:]

    def ohne(x):
        for n in (SA, AB):
            a2, e2 = u.mc_bereich(x, n)
            x = x[:a2] + x[e2:]
        li2, le2 = x.index("<logic_node_links>"), x.index("</logic_node_links>")
        return x[:li2] + x[le2:]
    assert ohne(s0) == ohne(s), "ausser den Abteil-Chips und Kabeln geaendert"
    print("Probe: Abteile %s, Sammler %s, 2 Kabel neu, sonst nichts" % (ba.VERSION, ba.VERSION_SAMMLER))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
