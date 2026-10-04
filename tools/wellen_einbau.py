"""Wellen-Schutz einbauen (02.10. abends): Schiffs-Chip v2.7 (build/<build_schiff.MC_FILE>, mit lua/wellen.lua) und
Flossen-Chip v1.7 (build/<build_flossen.MC_FILE>, Ausgang 'Physik weiter') in einem Durchgang, dazu das Kabel
'Physik weiter' -> Schiffs-Chip 'Physik-Sensor' statt Physik-Sensor direkt (kabel_flossen.einbauen).

- Schiffs-Chip: Anschluss-Lage muss gleich bleiben (sonst Abbruch); Eigenschaften im Schiff muessen den Bauwerten
  entsprechen (Andre kann sie im Editor nicht aendern) - neue Eigenschaften kommen mit ihren Standardwerten dazu
- Probe: ausserhalb der beiden Chips aendern sich nur die Kabel (eins weg, eins neu)
Aufruf: python wellen_einbau.py [--schreiben]   (vorher sichern; danach Schiff im Spiel neu laden, NICHT speichern)
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import build_schiff  # noqa: E402
import kabel_flossen  # noqa: E402
from chip_einsetzen import knoten  # noqa: E402

SCHIFF = "Figet Marena Schiffsfuehrung"
FLOSSEN = "Figet Marena Flossen"


def werte(t):
    return {html.unescape(n): float(v) for n, v in
            re.findall(r'<c type="34"><object id="\d+" n="([^"]*)">(?:<pos[^/]*/>)?<v text="([^"]*)"', t)}


def definition(s, name):
    i = s.index('<microprocessor_definition name="%s"' % name)
    return s[i:s.index("</microprocessor_definition>", i) + len("</microprocessor_definition>")]


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    # 1. Schiffs-Chip
    u.CHIP = os.path.join(build_schiff.BUILD, build_schiff.MC_FILE)
    a, e = u.mc_bereich(s0, SCHIFF)
    teil = s0[a:e]
    d0 = teil.index("<microprocessor_definition")
    d1 = teil.index("</microprocessor_definition>") + len("</microprocessor_definition>")
    neu = u.chip_eingebettet()
    assert knoten(teil[d0:d1]) == knoten(neu), "Anschluss-Lage/Typen geaendert - Kabel wuerden nicht mehr passen"
    alt_w, neu_w = werte(teil[d0:d1]), werte(neu)
    anders = {k: (alt_w[k], neu_w.get(k)) for k in alt_w if neu_w.get(k) != alt_w[k]}
    assert not anders, ("Eigenschaften im Schiff weichen ab (Schiff, Bau)", anders)
    print("Schiffs-Chip -> %s: Anschluesse gleich, %d Eigenschaften wie im Schiff, neu: %s" % (
        build_schiff.MC_FILE, len(alt_w), ", ".join("%s %g" % (k, v) for k, v in neu_w.items() if k not in alt_w)))
    s = s0[:a] + teil[:d0] + neu + teil[d1:] + s0[e:]
    # 2. Flossen-Chip + Kabel
    s = kabel_flossen.einbauen(s)
    # Probe
    ohne = lambda t: re.sub(r'<microprocessor_definition name="(%s|%s)".*?</microprocessor_definition>' % (SCHIFF, FLOSSEN),
                            "<CHIP>", t, flags=re.S)
    kabel = lambda t: re.findall(r"<logic_node_link.*?</logic_node_link>", t[t.index("<logic_node_links>"):t.index("</logic_node_links>")])
    k0, k1 = kabel(s0), kabel(s)
    weg = [k for k in k0 if k not in k1]
    dazu = [k for k in k1 if k not in k0]
    rest0 = ohne(s0).replace("".join(k0), "")
    rest1 = ohne(s)
    for k in k1:
        rest1 = rest1.replace(k, "", 1)
    for k in k0:
        rest0 = rest0.replace(k, "", 1)
    slots = lambda t: re.sub(r"<logic_slots>(<slot/>)*</logic_slots>", "<SLOTS>", t)
    print("Kabel: %d weg %s, %d neu %s" % (len(weg), weg, len(dazu), dazu))
    assert slots(rest0) == slots(rest1), "ausserhalb von Chips und Kabeln geaendert"
    assert len(weg) == 1 and len(dazu) == 1, "unerwartete Kabel-Aenderung"
    print("Probe: ausserhalb der beiden Chips nur das eine Kabel umgelegt")
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
