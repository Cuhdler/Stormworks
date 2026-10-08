"""Baut die Chips fuer den ferngesteuerten Jet (Andre 08.10.):
- "Jet Flug" (4 x 4, in den small Jet an Andres Platzhalter): Regler, Funk, Flugdaten - lua/jet.lua
- "Figet Marena Jet Steuerung" (4 x 3, im Schiff): Maus-Knueppel am zweiten Sitz, Funk, Kamerabild mit Anzeige auf dem
  Monitor 3x3 - lua/jet_steuerung.lua
- mit --install zusaetzlich nach %APPDATA%/Stormworks/data/microprocessors kopieren
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import MC, minify, fmt, LUA_LIMIT, LUA_DIR, BUILD  # noqa: E402
from build_lage import schreiber_props, kopf  # noqa: E402

VERSION = "v1.0"
FUNK = [("Funk Befehle", 7301, "Frequenz der Steuerbefehle (Schiff sendet, Jet empfaengt) und der Kamera vorn"),
        ("Funk Daten", 7302, "Frequenz der Flugdaten (Jet sendet, Schiff empfaengt) und der Kamera unten")]
PROPS_JET = [
    ("Querlage max Grad", 60, "Knueppel ganz zur Seite = so viel Querlage"),
    ("Nick max Grad", 30, "Knueppel ganz hoch/runter = so viel Nick (zur Trimmung dazu)"),
    ("Trimm Grad", 4, "Knueppel in der Mitte: diesen Nick halten"),
    ("Kurve Nick", 0.1, "In der Kurve so viel Nick mehr je Grad Querlage (gegen Hoehenverlust)"),
    ("Quer Band Grad", 40, "So viel Querlage-Fehler = volles Querruder"),
    ("Quer Daempfung s", 0.25, "Rollrate (Grad/s) mal so viel wird vom Fehler abgezogen"),
    ("Nick Band Grad", 20, "So viel Nick-Fehler = volles Hoehenruder"),
    ("Nick Daempfung s", 0.3, "Nickrate (Grad/s) mal so viel wird vom Fehler abgezogen"),
    ("Tempo Bezug m/s", 60, "Bei diesem Tempo wirken die Ruder voll; langsamer mehr, schneller weniger Ausschlag"),
    ("Kompass Richtung", -1, "-1: Kompass zaehlt gegen den Uhrzeigersinn (wie beim Schiff)"),
    ("Hoehe Richtung", 1, "-1, wenn der Jet bei Knueppel hoch nach unten geht"),
    ("Quer Richtung", 1, "-1, wenn der Jet bei Knueppel rechts nach links rollt"),
    ("Seite Richtung", 1, "-1, wenn das Seitenruder verkehrt arbeitet"),
    ("Funk weg s", 1, "So lange ohne Lebenszeichen vom Schiff = Notprogramm"),
    ("Notnick Grad", 5, "Notprogramm: diesen Nick halten (Fluegel gerade)"),
    ("Notgas", 0.6, "Notprogramm: so viel Gas"),
    ("Start s", 3, "Nach dem Zuenden der Booster so lange 'Start Nick Grad' halten"),
    ("Start Nick Grad", 45, "Nick waehrend des Starts"),
] + FUNK
PROPS_ST = [
    ("Blick X U", 0.08, "So weit nach rechts/links schauen (Umdrehungen ab Mitte) = voller Querlage-Ausschlag"),
    ("Blick Y U", 0.06, "So weit nach oben/unten schauen = voller Nick-Ausschlag"),
    ("Blick X Richtung", 1, "-1, wenn der Knueppel-Kreis links/rechts verkehrt laeuft"),
    ("Blick Y Richtung", 1, "-1, wenn der Knueppel-Kreis oben/unten verkehrt laeuft"),
    ("Totzone", 0.1, "Knueppel-Anteil um die Mitte ohne Wirkung"),
    ("Gas Tempo", 0.4, "W/S verstellt das Gas so schnell (Anteil je Sekunde)"),
    ("Zoom Tempo", 0.5, "Pfeil hoch/runter verstellt den Zoom so schnell"),
] + FUNK


def rd(mc, q, ch, pos, typ=31):
    return mc.comp(typ, pos, {"i": ch} if ch else {}, [(q, 0)])


def props(mc, liste, x0):
    for k, (name, val, desc) in enumerate(liste):
        mc.comp(34, (x0 - 2 * (k // 8), 8 - (k % 8)), {"n": name}, extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))


def build_jet(src):
    mc = MC("Jet Flug", "Jet Flug %s: Regler (Querlage/Nick), Funk-Befehle, Flugdaten, Notprogramm - Steuerung vom Schiff "
            "per Maus" % VERSION, 4, 4)
    pl = [(x, z) for z in range(4) for x in range(4)]
    bef = mc.node("Befehle", 1, 5, "Funkgeraet Empfang (2,2,-22): Data Recv", *pl[0], (-8, 3))
    phys = mc.node("Physik", 1, 5, "Physics Sensor (0,3,-18): Composite Output", *pl[1], (-8, 2))
    tank = mc.node("Tank", 1, 1, "Liquid Meter (0,-3,-19): Liquid Level", *pl[2], (-8, 1))
    w = mc.comp(40, (-4, 2), {"count": 7, "offset": 19},
                [("inc", (bef, 0))] + [(rd(mc, phys, ch, (-6, 3 - .5 * j)), 0) for j, ch in enumerate((0, 1, 2, 12, 14, 15, 16))])
    w = mc.comp(40, (-4, 0), {"count": 1, "offset": 26}, [("inc", (w, 0)), (tank, 0)])
    lua = mc.comp(56, (0, 1), {"script": src}, [(w, 0)])
    props(mc, PROPS_JET, -10)
    zahl = [("Ruder links", "Control Surface (-6,-6,-21): Rotation"), ("Ruder rechts", "Control Surface (6,-6,-21): Rotation"),
            ("Seitenruder", "Control Surface klein (0,-6,-21): Rotation"), ("Gas", "Jet Combustion Chamber: Throttle"),
            ("Zoom", "Camera Medium (unten): Field of View"),
            ("Freq Befehle", "Funkgeraet Empfang (2,2,-22) + Video-Sender Kamera vorn (0,-5,-23): Frequenz"),
            ("Freq Daten", "Funkgeraet Senden (-2,1,-22) + Video-Sender Kamera unten (1,2,-23): Frequenz")]
    for k, (n, d) in enumerate(zahl):
        mc.node(n, 0, 1, d, *pl[3 + k], (6, 3 - k), (rd(mc, lua, k, (3, 3 - k)), 0))
    an = [("Verdichter", "Jet Compressor: Compressor"), ("Booster", "6 Solid Rocket Booster: Trigger"),
          ("Licht", "Lampen, Scheinwerfer, Horizont: Light Switch / Backlight"), ("Magnete", "4 Mag All: Magnet Toggle"),
          ("Senden an", "Funkgeraet Senden (-2,1,-22): Transmit Mode")]
    for k, (n, d) in enumerate(an):
        mc.node(n, 0, 0, d, *pl[10 + k], (6, -4 - k), (rd(mc, lua, k, (3, -4 - k), 29), 0))
    mc.node("Flugdaten", 0, 5, "Funkgeraet Senden (-2,1,-22): Data Send", *pl[15], (6, -9), (lua, 0))
    return mc


def build_steuerung(src):
    mc = MC("Figet Marena Jet Steuerung", "Jet Steuerung %s: zweiter Sitz, Maus = Knueppel, Funk zum Jet, Kamerabild mit "
            "Anzeige auf Monitor 3x3" % VERSION, 4, 3)
    pl = [(x, z) for z in range(3) for x in range(4)]
    sitz = mc.node("Sitz", 1, 5, "Zweiter Sitz (-5,16,-26): Seat data", *pl[0], (-8, 3))
    fd = mc.node("Flugdaten", 1, 5, "Funkgeraet Empfang (7,24,-50): Data Recv", *pl[1], (-8, 2))
    phys = mc.node("Physik", 1, 5, "Physics Sensor (0,27,-38): Composite Output (Entfernung zum Jet)", *pl[2], (-8, 1))
    sig = mc.node("Signal", 1, 1, "Funkgeraet Empfang: Signal Strength", *pl[3], (-8, 0))
    kam = mc.node("Kamera", 1, 6, "Video-Empfaenger (0,24,-44): Video Recv", *pl[4], (-8, -1))
    w = mc.comp(40, (-4, 3), {"count": 6, "offset": 0},
                [("inc", (fd, 0))] + [(rd(mc, sitz, ch, (-6, 3 - .5 * j)), 0) for j, ch in enumerate((0, 1, 2, 3, 8, 9))])
    w = mc.comp(40, (-4, 1), {"count": 3, "offset": 6},
                [("inc", (w, 0)), (rd(mc, phys, 0, (-6, 0)), 0), (rd(mc, phys, 2, (-6, -.5)), 0), (sig, 0)])
    w = mc.comp(41, (-3, 0), {"count": 8, "offset": 0},
                [("inc", (w, 0))] + [(rd(mc, sitz, ch, (-6, -1 - .5 * j), 29), 0) for j, ch in enumerate((0, 1, 2, 3, 4, 5, 30, 31))])
    lua = mc.comp(56, (0, 1), {"script": src}, [(w, 0), (kam, 0)])
    props(mc, PROPS_ST, -10)
    schreiber_props(mc, -14, 8)
    mc.node("Befehle", 0, 5, "Funkgeraet Senden (-7,24,-50): Data Send", *pl[5], (6, 3), (lua, 0))
    mc.node("Freq Senden", 0, 1, "Funkgeraet Senden: Frequency", *pl[6], (6, 2), (rd(mc, lua, 9, (3, 2)), 0))
    mc.node("Freq Empfang", 0, 1, "Funkgeraet Empfang: Frequency", *pl[7], (6, 1), (rd(mc, lua, 10, (3, 1)), 0))
    mc.node("Freq Video", 0, 1, "Video-Empfaenger: Frequency Recv (Kamera vorn/unten)", *pl[8], (6, 0), (rd(mc, lua, 11, (3, 0)), 0))
    mc.node("Senden an", 0, 0, "Funkgeraet Senden: Transmit Mode", *pl[9], (6, -1), (rd(mc, lua, 9, (3, -1), 29), 0))
    mc.node("Monitor", 0, 6, "Monitor 3x3 vor dem zweiten Sitz (-5,20,-24): Video Signal", *pl[10], (6, -2), (lua, 1))
    mc.node("Monitor an", 0, 0, "Monitor 3x3: Power Switch", *pl[11], (6, -3), (rd(mc, lua, 10, (3, -3), 29), 0))
    return mc


def main():
    os.makedirs(BUILD, exist_ok=True)
    for name, datei, bau, q in (("Jet Flug", "jet.lua", build_jet, None),
                                ("Figet Marena Jet Steuerung", "jet_steuerung.lua", build_steuerung, "js")):
        with open(os.path.join(LUA_DIR, datei), encoding="utf-8") as f:
            src = minify(f.read())
        if q:
            src = kopf(src, q)
        print("%-18s %5d Zeichen %s" % (datei, len(src), "OK" if len(src) <= LUA_LIMIT else "ZU LANG"))
        if len(src) > LUA_LIMIT:
            sys.exit("Skript zu lang")
        mc = bau(src)
        assert len(mc.desc) <= 128, (name, len(mc.desc))
        fname = "%s %s.xml" % (name, VERSION)
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
