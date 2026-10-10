"""Stormworks-Simulator ("Kopie von Stormworks") fuer Andres Fahrzeuge: fuehrt die Microcontroller einer echten
Fahrzeugdatei Tick fuer Tick aus wie das Spiel - einzeln, als ganzes Netz mit Kabeln, oder als Host + Mitspieler.
Keine Physik: Fuehler-Werte kommen aus einem Szenario. Anleitung: sim/README.md.

Benutzen aus Python:
    import sys; sys.path.insert(0, "sim")
    import swsim
    fz = swsim.Fahrzeug("Figet Marena", chips=["Figet Marena Licht"])
    fz.teil(d="clock").setze("Time", 0.5)
    fz.tick(10)
    print(fz.chip("Figet Marena Licht").lese("Licht"))

Aufruf von der Kommandozeile (python sim/swsim.py ...):
    liste [Fahrzeug]                    Chips, Kabel-Pruefung, verworfene Kabel (Standard: Figet Marena)
    verbindungen <Fahrzeug> <Chip>      was an jedem Anschluss des Chips haengt
    lauf <Fahrzeug> [Chip ...] [--ticks N]   Chips ohne Fuehler-Werte laufen lassen, Ausgaenge und Fehler zeigen
    datei <Chip-Datei.xml> [--ticks N]  eine Chip-Datei (build/ oder Spiel-Ordner) laufen lassen
    typen                               alle Baustein-Typen in allen Chips auf dem PC: kennt der Simulator sie?
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chip import (Chip, ChipDef, Composite, LEER, SimFehler, chipdef, composite, f32, leer, zeichne, texte,  # noqa
                  TYPEN, SIGNAL, chip_dateien)
from fahrzeug import Fahrzeug, FahrzeugDaten, TeilGriff, finde_fahrzeug, FAHRZEUGE  # noqa
from mehrspieler import Mehrspieler  # noqa


def chip_aus_fahrzeug(fahrzeug, name, **opt):
    """Einen Chip aus der Fahrzeugdatei allein laufen lassen (Eingaenge mit chip.setze)."""
    d = FahrzeugDaten.lesen(fahrzeug)
    t = [t for t in d.chips() if t.name == name]
    if not t:
        raise SimFehler("Chip '%s' nicht in %s" % (name, d.pfad))
    return Chip(t[0].chipdef, **opt)


def _kurz(v):
    if isinstance(v, Composite):
        return repr(v)
    if isinstance(v, tuple):
        return "Bild(%d Ebenen)" % len(v)
    if isinstance(v, float):
        return "%.6g" % v
    return repr(v)


def _arg(args, name, standard):
    if name in args:
        i = args.index(name)
        v = args[i + 1]
        del args[i:i + 2]
        return v
    return standard


def main(args):
    if not args:
        print(__doc__)
        return 0
    befehl, args = args[0], list(args[1:])
    ticks = int(_arg(args, "--ticks", 60))
    if befehl == "liste":
        fz = Fahrzeug(args[0] if args else "Figet Marena", chips=[])
        for z in fz.bericht():
            print(z)
        print("Chips:")
        for t in fz.daten.chips():
            ty = t.chipdef.typen()
            print("   %-42s %-14s %2d Anschluesse, Bausteine %s" % (t.name, t.vp, len(t.chipdef.knoten),
                                                                   " ".join("%d:%d" % kv for kv in sorted(ty.items()))))
    elif befehl == "verbindungen":
        fz = Fahrzeug(args[0], chips=[])
        for z in fz.verbindungen(args[1]):
            print(z)
    elif befehl == "lauf":
        fz = Fahrzeug(args[0], chips=args[1:] or None)
        fz.tick(ticks)
        for ch in fz.laufend.values():
            print("Chip '%s' nach %d Ticks:" % (ch.name, ticks))
            for k in ch.aus_knoten:
                print("   %-24s %s" % (k.label, _kurz(ch.werte[k.nr])))
        for z in fz.bericht():
            print(z)
    elif befehl == "datei":
        ch = Chip.aus_datei(args[0])
        for _ in range(ticks):
            ch.tick()
        print("Chip '%s' nach %d Ticks:" % (ch.name, ticks))
        for k in ch.aus_knoten:
            print("   %-24s %s" % (k.label, _kurz(ch.werte[k.nr])))
        for f in ch.fehler() + ch.hinweise():
            print("   " + f)
    elif befehl == "typen":
        gefunden = {}
        for f in chip_dateien() + glob.glob(os.path.join(FAHRZEUGE, "*.xml")):
            s = open(f, encoding="utf-8", errors="replace", newline="").read()
            for m in re.finditer(r"<microprocessor(?:_definition)?\b.*?</microprocessor(?:_definition)?>", s, re.S):
                try:
                    cd = chipdef(m.group(0))
                except SimFehler as e:
                    print("nicht lesbar in %s: %s" % (os.path.basename(f), e))
                    continue
                for ty, n in cd.typen().items():
                    g = gefunden.setdefault(ty, [0, set()])
                    g[0] += n
                    g[1].add(cd.name)
        for ty in sorted(gefunden):
            k = TYPEN.get(ty)
            print("%3d %-52s %6d mal in %3d Chips" % (ty, (k.name + (" [V]" if k.vermutet else "")) if k else "UNBEKANNT",
                                                      gefunden[ty][0], len(gefunden[ty][1])))
    else:
        print("unbekannter Befehl %r" % befehl)
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except SimFehler as e:
        print("FEHLER:", e)
        sys.exit(1)
