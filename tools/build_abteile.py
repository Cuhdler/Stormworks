"""Baut die Chips fuer die Abteil-Anzeige (Andre 08.10.): "Figet Marena Abteile Sammler" (4 x 5, Sensor 10-18 gepackt,
lua/abteile_sammler.lua) und "Figet Marena Abteile" (v1.2: 4 x 8, Sensor 1-9, Anzeige auf dem Monitor 9x5, alle
Schotten zu/auf, Lenzpumpen automatisch mit dem Schalter 'Auto water pumps', lua/abteile.lua). Zwei Chips, weil
18 Liquid Meter je 2 Werte (Fuellstand, Kapazitaet) liefern.
- mit --install zusaetzlich nach %APPDATA%/Stormworks/data/microprocessors kopieren
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import MC, minify, fmt, LUA_LIMIT, LUA_DIR, BUILD  # noqa: E402

VERSION = "v1.6"
VERSION_SAMMLER = "v1.1"
# Liquid Meter 1-18 vom Bug zum Heck (Reihenfolge wie SX/SZ in lua/abteile.lua); 1-9 an den Abteil-Chip, 10-18 an den
# Sammler. (0,-16,-129) misst fuer den Flossen-Chip das Heck-Wasser und gehoert nicht dazu.
SENSOREN = [(-2, -7, 41), (2, -7, 41), (-1, -15, 16), (1, -15, 16), (-4, -19, 15), (4, -19, 15), (-2, -19, -1),
            (2, -19, -1), (-1, -15, -17), (1, -15, -17), (-2, -19, -19), (2, -19, -19), (-18, -15, -40), (18, -15, -40),
            (-2, -19, -42), (2, -19, -42), (-1, -19, -61), (1, -19, -61)]
PROPS = [
    ("Gelb ab %", 1, "Abteil gelb ab so viel Wasser (Prozent der Kapazitaet)"),
    ("Rot ab %", 20, "Abteil rot ab so viel Wasser"),
    ("Auto zu ab %", 0.5, "Wasser in einem Abteil ab so viel: alle Schotten gehen selbst zu (0 = aus)"),
    ("Pumpe ab %", 0.3, "Schalter 'Auto water pumps' an: Lenzpumpen an, sobald ein Abteil so viel Wasser hat"),
    ("Nachlauf s", 20, "So lange laufen die Pumpen nach dem letzten Wasser weiter"),
]
# Lenzpumpen (Large Fluid Pump): Lenzleitung (Andre 08.10.) und die zwei alten an der Maschinenraum-Wand
PUMPEN = [(0, -4, -5), (-15, -19, -56), (15, -19, -56)]
# Sensoren 5-8, 11, 12, 15, 16 (y -19, Doppelboden mit Fluid Spawner) messen die Treibstofftanks (Andre 08.10.)
TANKS = [5, 6, 7, 8, 11, 12, 15, 16]
# Batterien (alle 6 in einem Netz): eine grosse (Monitore, Lampen) und eine mittlere (Maschinenraum)
BATTERIEN = [("battery_large", (-4, -13, -46)), ("battery_medium", (-8, -19, -65))]


def raster(w, ln):
    return [(x, z) for z in range(ln) for x in range(w)]


def build_sammler(src):
    mc = MC("Figet Marena Abteile Sammler", "Abteile Sammler %s: Liquid Meter 10-18 (Heckhaelfte) gepackt / Liter an den "
            "Abteil-Chip" % VERSION_SAMMLER, 4, 5)
    pl = raster(4, 5)
    ein = []
    for k in range(9):
        ein.append(mc.node("Fuellstand %d" % (10 + k), 1, 1, "Liquid Meter %s: Liquid Level" % (SENSOREN[9 + k],),
                           *pl[k], (-8, 9 - k)))
    for k in range(9):
        ein.append(mc.node("Kapazitaet %d" % (10 + k), 1, 1, "Liquid Meter %s: Fluid Capacity" % (SENSOREN[9 + k],),
                           *pl[9 + k], (-8, -1 - k)))
    w = mc.comp(40, (-4, 0), {"count": 18, "offset": 0}, [(n, 0) for n in ein])
    lua = mc.comp(56, (0, 0), {"script": src}, [(w, 0)])
    mc.node("Abteile", 0, 5, "an den Abteil-Chip (Eingang 'Sammler'): Sensor 10-18 gepackt", *pl[19], (4, 0), (lua, 0))
    return mc


def build_abteile(src):
    mc = MC("Figet Marena Abteile", "Abteile %s: Monitor 9x5 Abteile/Sprit/Batterie, Schotten zu/auf, Lenzpumpen "
            "automatisch" % VERSION, 4, 8)
    pl = raster(4, 8)
    ein = []
    for k in range(9):
        ein.append(mc.node("Fuellstand %d" % (1 + k), 1, 1, "Liquid Meter %s: Liquid Level" % (SENSOREN[k],),
                           *pl[k], (-8, 9 - k)))
    for k in range(9):
        ein.append(mc.node("Kapazitaet %d" % (1 + k), 1, 1, "Liquid Meter %s: Fluid Capacity" % (SENSOREN[k],),
                           *pl[9 + k], (-8, -1 - k)))
    sam = mc.node("Sammler", 1, 5, "Sammel-Chip: Ausgang 'Abteile'", *pl[18], (-8, -11))
    touch = mc.node("Touch", 1, 5, "Monitor 9x5 (8,21,-23): Touch Output", *pl[19], (-8, -12))
    knopf = mc.node("Knopf Schotten", 1, 0, "frei fuer einen Knopf: Druck = alle Schotten zu/auf", *pl[20], (-8, -13))
    instr = mc.node("Instrumente", 1, 5, "Instrumentenblock (-2,19,-8): Out Signal (Bool 4 = Schalter 'Auto water pumps')",
                    *pl[21], (-8, -14))
    fluss = [mc.node("Fluss %d" % (k + 1), 1, 1, "Lenzpumpe %s: Flow Rate (L/s)" % (p,), *pl[22 + k], (-8, -15 - k))
             for k, p in enumerate(PUMPEN)]

    def rd(q, ch, pos, typ=31):
        return mc.comp(typ, pos, {"i": ch} if ch else {}, [(q, 0)])
    w = mc.comp(40, (-4, 2), {"count": 18, "offset": 9}, [("inc", (sam, 0))] + [(n, 0) for n in ein])
    # v1.3: Batterie-Ladung (hinten angehaengt); Fluss = Summe der 3 Pumpen, Batterie = hoechste der 2 (Formel-Bausteine)
    bat = [mc.node("Batterie %d" % (k + 1), 1, 1, "%s %s: Charge (0-1)" % b, *pl[29 + k], (-8, -18 - k), late=True)
           for k, b in enumerate(BATTERIEN)]
    summe = mc.comp(10, (-6, -16), {"e": "max(x,0)+max(y,0)+max(z,0)"}, [(f, 0) for f in fluss])
    bmax = mc.comp(10, (-6, -18), {"e": "max(x,y)"}, [(b, 0) for b in bat])
    # v1.5: Zustand der 5 Schottwaende vom Schotten-Chip (Bool 1-5 -> Bool 4-8)
    tueren = mc.node("Tueren", 1, 5, "Schotten-Chip: Ausgang 'Zustand' (Bool 1-5 Wand 1-5 auf)", *pl[31], (-8, -20), late=True)
    w = mc.comp(40, (-4, 0), {"count": 4, "offset": 27},
                [("inc", (w, 0)), (rd(touch, 2, (-6, -12)), 0), (rd(touch, 3, (-6, -12.5)), 0), (summe, 0), (bmax, 0)])
    w = mc.comp(41, (-3, -1), {"count": 3, "offset": 0}, [("inc", (w, 0)), (rd(touch, 0, (-6, -13), 29), 0), (knopf, 0),
                                                         (rd(instr, 3, (-6, -14), 29), 0)])
    w = mc.comp(41, (-3, -2), {"count": 5, "offset": 3},
                [("inc", (w, 0))] + [(rd(tueren, k, (-6, -20 - .5 * k), 29), 0) for k in range(5)])
    lua = mc.comp(56, (0, 0), {"script": src}, [(w, 0)])
    for k, (name, val, desc) in enumerate(PROPS):
        mc.comp(34, (-10, 8 - k), {"n": name}, extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))
    mc.node("Monitor", 0, 6, "Monitor 9x5 (8,21,-23): Video Signal", *pl[25], (4, 2), (lua, 1))
    mc.node("Monitor an", 0, 0, "Monitor 9x5: Power Switch", *pl[26], (4, 1), (rd(lua, 1, (2, 1), 29), 0))
    mc.node("Schotten auf", 0, 0, "an den Schotten-Chip ('Alle auf'; bis v1.4 direkt an die 10 Schiebetueren)", *pl[27],
            (4, 0), (rd(lua, 0, (2, 0), 29), 0))
    mc.node("Pumpen", 0, 0, "alle Lenzpumpen: On/Off", *pl[28], (4, -1), (rd(lua, 2, (2, -1), 29), 0))
    return mc


def main():
    os.makedirs(BUILD, exist_ok=True)
    for name, datei, bau in (("Figet Marena Abteile Sammler", "abteile_sammler.lua", build_sammler),
                             ("Figet Marena Abteile", "abteile.lua", build_abteile)):
        with open(os.path.join(LUA_DIR, datei), encoding="utf-8") as f:
            src = minify(f.read())
        print("%-22s %5d Zeichen %s" % (datei, len(src), "OK" if len(src) <= LUA_LIMIT else "ZU LANG"))
        if len(src) > LUA_LIMIT:
            sys.exit("Skript zu lang")
        mc = bau(src)
        assert len(mc.desc) <= 128, (name, len(mc.desc))
        fname = "%s %s.xml" % (name, VERSION_SAMMLER if "Sammler" in name else VERSION)
        out = os.path.join(BUILD, fname)
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(mc.xml())
        print("geschrieben:", out)
        if "--install" in sys.argv:
            dst = os.path.join(os.environ["APPDATA"], "Stormworks", "data", "microprocessors", fname)
            shutil.copyfile(out, dst)
            print("installiert:", dst)


if __name__ == "__main__":
    main()
