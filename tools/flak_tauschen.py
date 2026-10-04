"""Flak-Chips in der Figet Marena gegen eine neue Bau-Fassung tauschen (build/Figet Marena Flak L/R <VERSION>.xml):
nur die Chip-Definition; Lage, Kabel und Steckplaetze bleiben. Die Anschluesse muessen gleich bleiben (sonst Abbruch).
Eigenschaften: die Werte aus dem Schiff werden uebernommen (Andre kann sie im Editor nicht aendern - geaendert wird
nur hier), neue Eigenschaften bekommen ihren Standardwert; mit --setze "Name=Wert" (beide Chips) bzw.
--setze "L:Name=Wert" / "R:Name=Wert" (ein Chip) gezielt aendern (mehrfach moeglich).
Aufruf: python flak_tauschen.py [--setze "Test Rohre=2"] [--schreiben]   (danach neu laden, NICHT vorher speichern)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
import build_flak  # noqa: E402
from build_schiff import BUILD, fmt  # noqa: E402
from chip_einsetzen import knoten  # noqa: E402

PROP = r'(<c type="34"><object id="\d+" n="%s">(?:<pos[^/]*/>)?)<v [^/]*/>'


def werte(t):
    return {n: v for n, v in re.findall(r'<c type="34"><object id="\d+" n="([^"]*)">(?:<pos[^/]*/>)?<v text="([^"]*)"', t)}


def setze(t, name, wert):
    v = fmt(float(wert)) if re.fullmatch(r"-?[\d.]+", str(wert)) else wert
    t2, n = re.subn(PROP % re.escape(name), lambda m: m.group(1) + '<v text="%s" value="%s"/>' % (v, v), t)
    assert n == 1, ("Eigenschaft nicht gefunden", name)
    return t2


def main():
    vorgaben = {"L": {}, "R": {}}
    for k, a in enumerate(sys.argv):
        if a == "--setze":
            n, w = sys.argv[k + 1].split("=", 1)
            seiten = "LR"
            if n[:2] in ("L:", "R:"):
                seiten, n = n[0], n[2:]
            for x in seiten:
                vorgaben[x][n.strip()] = w.strip()
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    s = s0
    for seite in ("L", "R"):
        vorgabe = vorgaben[seite]
        a, e = u.mc_bereich(s, "Figet Marena Flak %s" % seite)
        teil = s[a:e]
        d0 = teil.index("<microprocessor_definition")
        d1 = teil.index("</microprocessor_definition>") + len("</microprocessor_definition>")
        u.CHIP = os.path.join(BUILD, "Figet Marena Flak %s %s.xml" % (seite, build_flak.VERSION))
        neu = u.chip_eingebettet()
        assert knoten(teil[d0:d1]) == knoten(neu), "Anschluss-Lage/Typen geaendert - Kabel wuerden nicht mehr passen"
        alt_w, neu_w = werte(teil[d0:d1]), werte(neu)
        for n, v in alt_w.items():
            if n in neu_w and n not in vorgabe:
                neu = setze(neu, n, v)
        for n, v in vorgabe.items():
            neu = setze(neu, n, v)
        geaendert = {n: (alt_w.get(n), werte(neu)[n]) for n in werte(neu) if alt_w.get(n) != werte(neu)[n]}
        print("Flak %s -> %s: Anschluesse gleich; Eigenschaften geaendert/neu: %s" % (seite, build_flak.VERSION, geaendert))
        s = s[:a] + teil[:d0] + neu + teil[d1:] + s[e:]
    ohne = lambda x: re.sub(r'<microprocessor_definition name="Figet Marena Flak [LR]".*?</microprocessor_definition>', "", x, flags=re.S)
    assert ohne(s0) == ohne(s), "ausser den Flak-Chips geaendert"
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
