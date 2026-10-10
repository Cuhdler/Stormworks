"""Baut den Chip "Figet Marena Autopilot" (4 x 3): Kurs und Tempo halten, Karte mit Wegpunkten auf dem Monitor 5x3,
Laser am Bug gegen Hindernisse - Skript lua/autopilot.lua (Andre 08.10.).
v1.1: Wegpunkte per Control Handle (Blick = Kreuz, Leertaste, hoch/runter = Zoom) statt Touch; Anschluss 'Touch' heisst
'Griff' (gleiche Stelle und Art), neu hinten 'Knopf Anti-Kollision' (Bug-Laser an/aus).
v1.2: Zoom ab Achse 0,2 und per Hotkey 3/4; alle Griff-Achsen ins Log (Anschluesse wie v1.1).
Der Chip haengt zwischen Fahrersitz und Schiffsfuehrung: ein Composite-Umschalter im Chip (nicht das Skript) laesst das
Sitz-Signal unveraendert durch, solange der Autopilot aus ist; an = Achse 1/2 vom Skript.
- mit --install zusaetzlich nach %APPDATA%/Stormworks/data/microprocessors kopieren
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import MC, minify, fmt, LUA_LIMIT, LUA_DIR, BUILD  # noqa: E402
from build_lage import schreiber_props, kopf  # noqa: E402

VERSION = "v1.3"
PROPS = [
    ("Kompass Richtung", -1, "-1: der Kompass des Physik-Sensors zaehlt gegen den Uhrzeigersinn (wie Lage)"),
    ("Kurs Band Grad", 25, "So viel Kursfehler = volles Ruder"),
    ("Kurs Daempfung s", 3, "Drehrate (Grad/s) mal so viel wird vom Kursfehler abgezogen - gegen Ueberschwingen"),
    ("Kurs I", 0.005, "Gegen Wind/Stroemung: Ruder-Anteil je Grad Fehler und Sekunde (hoechstens 0,3, nur unter 10 Grad Fehler)"),
    ("Kurs Tempo Grad/s", 10, "A/D verstellt den Soll-Kurs so schnell"),
    ("Tempo Schritt kn/s", 5, "W/S verstellt das Soll-Tempo so schnell"),
    ("Tempo max kn", 60, "Hoechstes Soll-Tempo"),
    ("Tempo P", 0.08, "Fahrhebel je m/s Tempo-Fehler"),
    ("Tempo I", 0.005, "Fahrhebel je m/s Tempo-Fehler und Sekunde"),
    ("Hebel Tempo", 0.25, "Wie 'Hebel Tempo' der Schiffsfuehrung (der Autopilot rechnet ihren Fahrhebel mit)"),
    ("Rueckwaerts max", 0.5, "Wie 'Rueckwaerts max' der Schiffsfuehrung"),
    ("Wegpunkt Radius m", 150, "Naeher = Wegpunkt erreicht, weiter zum naechsten"),
    ("Am Ziel stoppen", 1, "1: nach dem letzten Wegpunkt Soll-Tempo 0; 0: weiterfahren"),
    ("Laser Schwenk U", 0.06, "Laser schwenkt so weit nach links und rechts (Umdrehungen, hoechstens 0,125)"),
    ("Laser Seite", 1, "-1, wenn die roten Laser-Punkte auf der Karte auf der falschen Seite liegen"),
    ("Laser Ticks", 4, "So lange bleibt der Laser auf jedem der 9 Felder"),
    ("Laser Winkel Grad", 0.3, "Strahl so viel ueber waagerecht (das Nicken gleicht der Pivot Y aus)"),
    ("Laser Hoehe Richtung", -1, "Bei Andres Laser kippt Pivot Y plus den Strahl nach unten (Log 08.10.: mit 1 sah er 7,6 Grad "
     "nach unten den Meeresboden) - daher -1"),
    ("Laser vor Physik m", 25.5, "Laser (0,2,64) liegt so weit vor dem Physik-Sensor (0,27,-38)"),
    ("Laser ueber Physik m", -6.25, "Laser liegt so viel hoeher als der Physik-Sensor (negativ = tiefer)"),
    ("Wasser bis m", 0.7, "Treffer tiefer als das ueber dem Meer zaehlen nicht (Wellen)"),
    ("Warnen ab m", 400, "Hindernis naeher als das (oder Tempo mal 'Warnen Vorlauf s') = ausweichen"),
    ("Warnen Vorlauf s", 40, "Warn-Entfernung = Tempo mal so viele Sekunden (wenn groesser als 'Warnen ab m')"),
    ("Stopp ab m", 150, "Hindernis naeher als das = Fahrhebel auf null"),
    ("Gasse halb m", 30, "Treffer so weit links/rechts der Fahrtlinie zaehlen als Hindernis"),
    ("Ausweichen Grad", 35, "Bei Hindernis so viel zur freieren Seite drehen"),
    ("Ausweichen halten s", 15, "So lange nach dem letzten Treffer weiter ausweichen"),
    ("Blick X U", 0.09, "So weit nach links/rechts schauen (Umdrehungen ab Blick-Mitte) = Kreuz am Bildrand"),
    ("Blick Y U", 0.055, "So weit nach oben/unten schauen = Kreuz am Bildrand"),
    ("Blick X Richtung", 1, "-1, wenn das Kreuz links/rechts verkehrt laeuft"),
    ("Blick Y Richtung", 1, "-1, wenn das Kreuz oben/unten verkehrt laeuft"),
    ("Rand Tempo px/s", 60, "Blick knapp ueber den Bildrand schiebt die Karte so schnell"),
]


def build(src):
    mc = MC("Figet Marena Autopilot", "Autopilot %s: Kurs/Tempo halten, Karte mit Wegpunkten (Control Handle), Anti-Kollision "
            "mit Bug-Laser" % VERSION, 4, 3)
    sitz = mc.node("Sitz", 1, 5, "Fahrersitz (0,17,-10): Seat data", 0, 2, (-8, 3))
    phys = mc.node("Physik", 1, 5, "Physics Sensor (0,27,-38): Composite Output", 0, 1, (-8, 2))
    griff = mc.node("Griff", 1, 5, "Control Handle (-6,19,-21): Seat data (bis v1.0 'Touch')", 0, 0, (-8, 1))
    kap = mc.node("Knopf Autopilot", 1, 0, "Knopf 'Activate Autopilot': Pressed", 1, 2, (-8, 0))
    krs = mc.node("Knopf Reset", 1, 0, "Knopf 'Reset': Pressed (Route loeschen)", 1, 1, (-8, -1))
    las = mc.node("Laser Entfernung", 1, 1, "Laser am Bug (0,2,64): Distance", 1, 0, (-8, -2))
    # v1.1: neuer Anschluss hinten (die alten behalten Lage und Kabel)
    kak = mc.node("Knopf Anti-Kollision", 1, 0, "Knopf 'Automatic anti kollision': Pressed (Bug-Laser an/aus)", 2, 2,
                  (-8, -3), late=True)

    def rd(q, ch, pos, typ=31):
        return mc.comp(typ, pos, {"i": ch} if ch else {}, [(q, 0)])

    # AUTOPILOT-Eingang: Sitz + Zahl 7-12 Physik x, Hoehe, z, Nick, Kompass, Tempo; 13/14 Griff Blick X/Y (Kanal 9/10),
    # 15 Laser, 16/17 Griff W/S und Pfeil hoch/runter, 18/19 Griff A/D und Pfeil links/rechts; Bool 10 Griff Leertaste
    # (31), 11 Knopf Autopilot, 12 Knopf Reset, 13 Knopf Anti-Kollision, 14 Griff besetzt (32), 15-18 Griff Hotkey 1-4
    w = mc.comp(40, (-4, 3), {"count": 6, "offset": 6},
                [("inc", (sitz, 0))] + [(rd(phys, ch, (-6, 3 - .5 * j)), 0) for j, ch in enumerate((0, 1, 2, 14, 16, 12))])
    w = mc.comp(40, (-4, 1), {"count": 7, "offset": 12},
                [("inc", (w, 0)), (rd(griff, 8, (-6, 0)), 0), (rd(griff, 9, (-6, -.5)), 0), (las, 0),
                 (rd(griff, 1, (-6, -1)), 0), (rd(griff, 3, (-6, -1.5)), 0), (rd(griff, 0, (-7, -1)), 0),
                 (rd(griff, 2, (-7, -1.5)), 0)])
    w = mc.comp(41, (-3, 0), {"count": 9, "offset": 9},
                [("inc", (w, 0)), (rd(griff, 30, (-6, -2), 29), 0), (kap, 0), (krs, 0), (kak, 0),
                 (rd(griff, 31, (-6, -2.5), 29), 0), (rd(griff, 0, (-6, -3), 29), 0), (rd(griff, 1, (-6, -3.5), 29), 0),
                 (rd(griff, 2, (-7, -3), 29), 0), (rd(griff, 3, (-7, -3.5), 29), 0)])
    lua = mc.comp(56, (0, 2), {"script": src}, [(w, 0)])
    # Sitz mit Achse 1/2 vom Autopiloten; Umschalter: Autopilot an -> diese, aus -> Sitz unveraendert
    ws = mc.comp(40, (2, 3), {"count": 2, "offset": 0},
                 [("inc", (sitz, 0)), (rd(lua, 2, (1, 3)), 0), (rd(lua, 3, (1, 2.5)), 0)])
    # v1.3 (10.10.): Bool 29 im Sitz-Composite = Autopilot steuert - die Schiffsfuehrung (v3.6) schiebt den Hebel dann
    # anteilig wie bisher; von Hand gilt dort: Taste gedrueckt = volle Hebel-Geschwindigkeit, losgelassen = steht
    apf = mc.comp(41, (3, 3.5), {"count": 1, "offset": 28}, [("inc", (ws, 0)), (rd(lua, 0, (2, 2), 29), 0)])
    um = mc.comp(53, (4, 3), {}, [(apf, 0), (sitz, 0), (rd(lua, 0, (2, 1.5), 29), 0)])
    for k, (name, val, desc) in enumerate(PROPS):
        mc.comp(34, (-10 - 2 * (k // 8), 8 - (k % 8)), {"n": name}, extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))
    schreiber_props(mc, -18, 8)
    mc.node("Sitz aus", 0, 5, "an Schiffsfuehrung 'Sitz' (statt direkt vom Fahrersitz)", 3, 2, (6, 3), (um, 0))
    mc.node("Monitor", 0, 6, "Monitor 5x3: Video Signal (Karte)", 3, 1, (6, 2), (lua, 1))
    mc.node("Monitor an", 0, 0, "Monitor 5x3: Power Switch", 3, 0, (6, 1), (rd(lua, 1, (4, 1), 29), 0))
    mc.node("Laser an", 0, 0, "Laser am Bug: Active", 2, 1, (6, 0), (rd(lua, 2, (4, 0), 29), 0))
    mc.node("Laser Pivot", 0, 5, "Laser am Bug: Pivot (Zahl 1 X, 2 Y)", 2, 0, (6, -1), (lua, 0))
    return mc


def main():
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(LUA_DIR, "autopilot.lua"), encoding="utf-8") as f:
        src = kopf(minify(f.read()), "ap")
    print("autopilot %5d Zeichen %s" % (len(src), "OK" if len(src) <= LUA_LIMIT else "ZU LANG"))
    if len(src) > LUA_LIMIT:
        sys.exit("Skript zu lang")
    mc = build(src)
    assert len(mc.desc) <= 128, len(mc.desc)
    fname = "Figet Marena Autopilot %s.xml" % VERSION
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
