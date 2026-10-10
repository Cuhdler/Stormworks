"""Baut den Schiffsfuehrungs-Microcontroller der Figet Marena (Stormworks), 4 Motoren:

- verkleinert lua/*.lua nach build/*.min.lua (gleicher Minifier wie beim Flugpanzer)
- erzeugt build/<MC_FILE> (6 x 6)
- mit --install zusaetzlich nach %APPDATA%/Stormworks/data/microprocessors kopieren
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "stormworks_flugpanzer", "tools"))
from build_mc import MC, minify, fmt, LUA_LIMIT  # noqa: E402

LUA_DIR = os.path.join(ROOT, "lua")
BUILD = os.path.join(ROOT, "build")
MC_FILE = "Figet Marena Schiff v3.5.xml"

# Name, Standardwert, Erklaerung
PROPS = [
    ("Hebel Tempo", 0.25, "Wie schnell W/S den Fahrhebel verstellt (Anteil pro Sekunde)"),
    ("Rueckwaerts max", 0.5, "So weit laesst sich der Fahrhebel unter null ziehen (rueckwaerts)"),
    ("Ruder max", 0.5, "Groesster Ruder-Befehl: Robotic Pivot 1 = 90 Grad, Ruder-Bauteil 1 = 45 Grad (0.5 = 45 bzw. 22.5 Grad; bis v2.4 0.125 = nur 11 bzw. 5.6 Grad)"),
    ("Ruder Richtung", 1, "1 oder -1: wenn das Schiff mit D nach links dreht"),
    ("Ruder Tempo", 1, "Wie schnell das Ruder umlegt (Befehl pro Sekunde; 1 = von 0 auf Ruder max 0.5 in 0.5 s)"),
    ("Bugstrahl Richtung", 1, "1 oder -1: wenn Pfeil rechts den Bug nach links drueckt"),
    ("Bugstrahl beim Lenken", 1, "So stark hilft das Bugstrahlruder beim Lenken mit A/D mit (0 = nur Pfeil links/rechts)"),
    ("Lenk-Schub", 0.6, "Beim Lenken bekommt die kurveninnere Seite so viel weniger Gas (0 = aus; negativ, wenn das Schiff dadurch schlechter dreht)"),
    ("Kupplung ab RPS", 3, "Erst einkuppeln, wenn der Motor so schnell dreht (laeuft sicher)"),
    ("Kupplung Zeit s", 3, "So lange dauert das sanfte Einkuppeln von 0 auf voll"),
    ("Temp Ziel", 70, "Diese Temperatur haelt der Chip (alle 4 Motoren gleich, nach dem heissesten). Bis 75 Grad volle Leistung, bei 80-85 nur noch die Haelfte (07.10.)"),
    ("Temp Anflug s", 60, "So sanft naehert sich die Temperatur dem Ziel: erlaubter Anstieg = Abstand zum Ziel / diese Zeit (10 Grad unter Ziel: 0.17 Grad/s)"),
    ("Temp Regel", 0.2, "Wie schnell die Gas-Grenze nachregelt (Gas-Anteil pro Sekunde je 1 Grad/s zu schnellem Anstieg; kleiner = ruhiger)"),
    ("Motor heiss Grad", 115, "Notfall: ueber dieser Temperatur kuppelt der Chip den Motor aus"),
    ("Motor Ausfall s", 5, "Laeuft ein Motor so lange nicht (unter 2 RPS), gilt er als ausgefallen und bleibt ausgekuppelt"),
    ("Leerlauf RPS", 4, "Drehzahl ausgekuppelt (Fahrhebel auf null)"),
    ("RPS Notgrenze", 120, "Nur Schutz gegen Durchdrehen (z. B. Schraube aus dem Wasser); im normalen Betrieb begrenzt die Temperatur"),
    ("Gemisch", 0.5, "Ziel-Stoechiometrie wie am Zylinder angezeigt: 0.5 kraeftig, 0.2 sparsam (nur mit 'Gemisch Regler' > 0)"),
    ("Gemisch Regler", 0, "0 = festes Luft/Treibstoff-Verhaeltnis (Q 7.1, v3.2); > 0 (z. B. 0.0002) = Chip regelt Q nach dem gemessenen Gemisch"),
    ("Hoch ab RPS", 18, "Automatik: hochschalten, wenn die Motoren 1 s lang schneller drehen (v2.9: 18 statt 22 - mit Vollgas schaffen die Motoren nur ca. 19-20 RPS, in Gang 4 schwankend 16-22)"),
    ("Runter unter RPS", 13, "Automatik: runterschalten, wenn die Motoren langsamer drehen (hoch nur, wenn der Motor danach noch 10 % darueber liegt; v2.8: 13 statt 15 fuer Gang 7)"),
    ("Schaltzeit s", 1, "So lange muss die Drehzahl ueber/unter der Grenze sein; nach dem Schalten doppelt so lange Pause"),
    ("Getriebe A", 1.2, "Uebersetzung von Getriebe A, wenn an (6:5 = 1.2), Pfeil zum Motor"),
    ("Getriebe B", 1.5, "Uebersetzung von Getriebe B, wenn an (3:2 = 1.5)"),
    ("Getriebe C", 2, "Uebersetzung von Getriebe C, wenn an (2:1 = 2)"),
    # v3.5 E-Motoren (Andre 10.10.: zwei grosse E-Motoren an der Welle vor den Getrieben)
    ("E-Motor Anteil", 1, "E-Motoren bekommen so viel vom Fahrhebel, wie die Temperatur-Grenze den Dieseln wegnimmt (0 = E-Motoren aus)"),
    ("E-Motor ab Batterie", 0.5, "Unter dieser Batterie-Ladung bleiben die E-Motoren aus (Anlasser, Pumpen, Luefter brauchen Strom); 5 % darueber wieder an"),
    ("E-Motor Test", 0, "1 = Diesel bleiben ausgekuppelt, E-Motoren fahren mit dem Fahrhebel (Drehrichtung pruefen); danach wieder 0"),
    ("Log Port", 8766, "Fahrtenschreiber: Port von tools/logger.py auf dem PC (0 = aus; Heli-Flugschreiber nutzt 8765)"),
    # v2.7 Wellen-Skript (lua/wellen.lua)
    ("Frei unter m", 0.3, "Wellen: Schrauben gelten als 'frei', wenn der Heck-Messer (mit Vorhalt) flacher meldet"),
    ("Frei Vorhalt s", 0.3, "Wellen: so weit schaut die Erkennung voraus (die Schraube taucht schnell aus)"),
    ("Wellen ab kn", 15, "Wellen: Schutz erst ab diesem Tempo (im Stand meldet der Messer beim Rollen manchmal sehr flach)"),
    ("Frei max RPS Faktor", 0, "Wellen: Schrauben in der Luft drehen hoechstens so viel mal schneller als vorher (Gas weg; z. B. 1.5). 0 = aus: im Modell kostete jede Grenze Tempo (der Schubstoss beim Eintauchen fehlt)"),
    ("Drehzahl Daempfung", 0.05, "Gegen Schaukeln (kleine Gaenge): je RPS/s steigender Drehzahl so viel Gas weg (0.05: bei 3 RPS/s 15 %, hoechstens 30 %; 0 = aus)"),
    ("Wellen Sperre s", 2, "Wellen: so lange nach dem Wiedereintauchen nicht schalten (danach noch die normale Pause nach 'Schaltzeit s')"),
    ("Heck-Wasser Richtung", -1, "-1 = der Heck-Messer meldet die Tiefe (+ unter Wasser, Andres Messer), 1 = Hoehe ueber dem Wasser"),
]

MOTOREN = ["L1", "L2", "R1", "R2"]
# Anschluss-Lage je Motor: RPS, Zylinder, Luft, Treibstoff, Anlasser, Kupplung.
# L1/R1 wie seit v1.0 (Kabel bleiben), L2/R2 auf frueher freien Plaetzen und in der neuen Spalte 5.
LAGE = {
    "L1": [(2, 0), (3, 0), (2, 1), (0, 5), (1, 4), (3, 1)],
    "R1": [(0, 1), (1, 1), (0, 2), (1, 5), (3, 4), (1, 2)],
    "L2": [(2, 5), (3, 5), (4, 0), (4, 1), (4, 2), (4, 3)],
    "R2": [(4, 4), (4, 5), (5, 0), (5, 1), (5, 2), (5, 3)],
}
SEITE = {"L": "Linker", "R": "Rechter"}
STOCK = {"1": "unterer", "2": "oberer"}


def build(schiff_src, hud_src, wellen_src):
    # Beschreibung kurz halten: das Spiel kuerzt sie im Fahrzeug auf 128 Zeichen.
    mc = MC("Figet Marena Schiffsfuehrung", "Schiff v3.5: 4 Diesel + 2 E-Motoren, Temperatur 70, 8 Gaenge, Wellen-Schutz. H1 an/aus, H2 Stopp, H3 Automatik, H4 Werte", 6, 6)
    sitz = mc.node("Sitz", 1, 5, "Steuersitz (Helm): Ausgang 'Seat data'", 0, 0, (-8, 6))
    phys = mc.node("Physik-Sensor", 1, 5, "Flossen-Chip 'Physik weiter' (Physics Sensor + Heck-Wasser auf Kanal 20; ohne Messer: Physics Sensor direkt)", 1, 0, (-8, 5))
    rps, zyl = {}, {}
    for k, n in enumerate(MOTOREN):
        wer = "%s %s Motor (%s)" % (SEITE[n[0]], STOCK[n[1]], n)
        (rx, rz), (zx, zz) = LAGE[n][0], LAGE[n][1]
        rps[n] = mc.node("Motor %s RPS" % n, 1, 1, wer + ": Kurbelwelle (Crankshaft) Ausgang RPS", rx, rz, (-8, 4 - 2 * k))
        zyl[n] = mc.node("Motor %s Zylinder" % n, 1, 5, wer + ": Zylinder 3x3 Composite (Luft, Treibstoff, Temperatur)",
                         zx, zz, (-8, 3 - 2 * k))

    seat_num = [mc.comp(31, (-5, 7 - k), {"i": i} if i else {}, [(sitz, 0)]) for k, i in enumerate([0, 1, 2, 3])]
    tempo = mc.comp(31, (-5, 3), {"i": 12}, [(phys, 0)])
    kurs = mc.comp(31, (-5, 2), {"i": 16}, [(phys, 0)])
    # je Motor: RPS, Temperatur (Kanal 3), Luft (1), Treibstoff (2)
    werte = []
    for k, n in enumerate(MOTOREN):
        werte += [rps[n]] + [mc.comp(31, (-11 - k, 7 - j), {"i": i} if i else {}, [(zyl[n], 0)]) for j, i in enumerate([2, 0, 1])]
    seat_bool = [mc.comp(29, (-5, -1 - k), {"i": i} if i else {}, [(sitz, 0)]) for k, i in enumerate([0, 1, 2, 3, 4, 5, 30, 31])]
    # Sitz-Achsen 1-4, Tempo 5, Kurs 6, Motoren 7-22
    w = mc.comp(40, (-2, 5), {"count": 6}, [(c, 0) for c in seat_num + [tempo, kurs]])
    for k in range(2):
        w = mc.comp(40, (-2, 4 - k), {"count": 8, "offset": 6 + 8 * k},
                    [("inc", (w, 0))] + [(c, 0) for c in werte[8 * k:8 * k + 8]])
    # v2.7: Heck-Wasser (Physik-Composite Kanal 20 vom Flossen-Chip) auf Kanal 23
    wasser = mc.comp(31, (-5, 1), {"i": 19}, [(phys, 0)])
    # v3.5: Batterie-Ladung (Physik-Composite Kanal 21 vom Flossen-Chip v1.8) auf Kanal 25; Kanal 24 schreibt danach das
    # Wellen-Skript (Gas-Abzug), hier nur Platzhalter
    batt = mc.comp(31, (-5, 0.5), {"i": 20}, [(phys, 0)])
    w = mc.comp(40, (-2, 2), {"count": 3, "offset": 22}, [("inc", (w, 0)), (wasser, 0), (wasser, 0), (batt, 0)])
    wbool = mc.comp(41, (-2, -2), {"count": 8}, [("inc", (w, 0))] + [(c, 0) for c in seat_bool])
    # Wellen-Skript: Gas-Abzug auf Kanal 24, Schaltsperre auf Bool 9
    wellen = mc.comp(56, (-1, -4), {"script": wellen_src}, [(wbool, 0)])
    abzug = mc.comp(31, (0, -4), {}, [(wellen, 0)])
    sperre = mc.comp(29, (0, -5), {}, [(wellen, 0)])
    w2 = mc.comp(40, (0, -2), {"count": 1, "offset": 23}, [("inc", (wbool, 0)), (abzug, 0)])
    w2 = mc.comp(41, (0, -3), {"count": 1, "offset": 8}, [("inc", (w2, 0)), (sperre, 0)])
    schiff = mc.comp(56, (1, 1), {"script": schiff_src}, [(w2, 0)])
    hud = mc.comp(56, (3, -3), {"script": hud_src}, [(schiff, 0)])
    for k, (name, val, desc) in enumerate(PROPS):
        mc.comp(34, (-8 - 2 * (k // 8), -6 - (k % 8)), {"n": name},
                extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))

    def aus(label, ctype, ch, ntype, desc, xz, y):
        r = mc.comp(ctype, (5, y), {"i": ch} if ch else {}, [(schiff, 0)])
        mc.node(label, 0, ntype, desc, xz[0], xz[1], (8, y), (r, 0))

    def e_aus(label, seite, xz, y):
        r = mc.comp(31, (5, y), {"i": 19}, [(schiff, 0)])
        rv = mc.comp(34, (5, y + 0.5), {"n": "E-Motor Richtung %s" % seite}, extra='<v text="1" value="1"/>')
        f = mc.comp(10, (6.5, y), {"e": "x*y"}, [(r, 0), (rv, 0)])
        mc.node(label, 0, 1, "Grosser E-Motor %s (x %s8, z -96): Throttle" % ({"L": "links", "R": "rechts"}[seite], "-" if seite == "L" else "+"),
                xz[0], xz[1], (8, y), (f, 0))

    y = 7
    for k, n in enumerate(MOTOREN):
        wer = "%s %s Motor (%s)" % (SEITE[n[0]], STOCK[n[1]], n)
        aus("Luft %s" % n, 31, 3 * k, 1, wer + ": beide Air Manifolds, Throttle", LAGE[n][2], y)
        aus("Treibstoff %s" % n, 31, 3 * k + 1, 1, wer + ": beide Fuel Manifolds, Throttle", LAGE[n][3], y - 1)
        aus("Anlasser %s" % n, 29, 1 + k, 0, wer + ": alle Anlasser (Starter)", LAGE[n][4], y - 2)
        aus("Kupplung %s" % n, 31, 3 * k + 2, 1, wer + ": Kupplung (Clutch 3x3), Clutch Pressure", LAGE[n][5], y - 3)
        y -= 4
    aus("Ruder", 31, 12, 1, "Beide Ruder-Gelenke (Robotic Pivot): Rotation Target", (2, 2), y)
    aus("Bugstrahlruder", 31, 13, 1, "Elektromotor am Bugstrahlruder: Throttle", (3, 2), y - 1)
    # v3.5: 'Motor L/R an' und 'Rueckwaerts L/R' waren je dasselbe Signal (beide Seiten schalten im selben Tick) - je
    # einer reicht; auf den frei gewordenen Plaetzen die E-Motoren (E-Gas Zahl 20 mal 'E-Motor Richtung L/R')
    aus("Motoren an", 29, 0, 0, "Pumpen und Kuehler-Luefter aller 4 Motoren", (0, 3), y - 2)
    e_aus("E-Motor L", "L", (1, 3), y - 3)
    aus("Rueckwaerts", 29, 5, 0, "Rueckwaerts-Getriebe beider Seiten (aus 1:1 / an 1:-1): Gear Switch", (0, 4), y - 4)
    e_aus("E-Motor R", "R", (2, 4), y - 5)
    mc.node("Helm", 0, 6, "Steuersitz: Headset Video (Anzeige im Helm)", 2, 3, (8, y - 6), (hud, 1))
    # Gaenge: Getriebe A/B/C (je an beide Seiten); A auf dem frueheren Platz 'Schiffsdaten' (war nie verbunden)
    for k, (xz, stand) in enumerate([((3, 3), "6:5"), ((5, 4), "3:2"), ((5, 5), "2:1")]):
        aus("Getriebe %s" % "ABC"[k], 29, 8 + k, 0,
            "Gear Switch der Getriebe %s beider Seiten (aus 1:1 / an %s, Pfeil zum Motor)" % ("ABC"[k], stand), xz, y - 7 - k)
    return mc


def main():
    os.makedirs(BUILD, exist_ok=True)
    mins = {}
    for name in ("schiff", "shud", "wellen"):
        with open(os.path.join(LUA_DIR, name + ".lua"), encoding="utf-8") as f:
            mins[name] = minify(f.read(), drop_local=(name == "schiff"))   # 'local' weg spart ~110 Zeichen
        with open(os.path.join(BUILD, name + ".min.lua"), "w", encoding="utf-8", newline="\n") as f:
            f.write(mins[name])
        size = len(mins[name])
        print("%-6s %5d Zeichen %s" % (name, size, "OK" if size <= LUA_LIMIT else "ZU LANG"))
        if size > LUA_LIMIT:
            sys.exit("Skript zu lang")
    out = os.path.join(BUILD, MC_FILE)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(build(mins["schiff"], mins["shud"], mins["wellen"]).xml())
    print("geschrieben:", out)
    if "--install" in sys.argv:
        dst = os.path.join(os.environ["APPDATA"], "Stormworks", "data", "microprocessors", MC_FILE)
        shutil.copyfile(out, dst)
        print("installiert:", dst)


if __name__ == "__main__":
    main()
