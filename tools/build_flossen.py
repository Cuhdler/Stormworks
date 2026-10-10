"""Baut den Chip "Figet Marena Flossen" (3 x 4, bis v1.4 3 x 3) fuer die 12 Steuerflossen (lua/flossen.lua).
Er sitzt auf Andres leerem Microcontroller bei (0,-5,-44) ueber dem Schiffs-Chip (gleiche Drehung):
Chip-Feld (x, z) -> Welt (0, -5-x, -44+z).

- mit --install zusaetzlich nach %APPDATA%/Stormworks/data/microprocessors kopieren
- mit --test den Test-Chip (lua/flossen_test.lua: alle Flossen +0.7) als build/<TEST_FILE> bauen (gleiche Anschluesse)
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import MC, minify, fmt, LUA_LIMIT, LUA_DIR, BUILD  # noqa: E402

MC_FILE = "Figet Marena Flossen v1.8.xml"
TEST_FILE = "Figet Marena Flossen TEST.xml"

PROPS = [
    ("Flossen an", 1, "0 = Flossen bleiben gerade"),
    ("Flossen Richtung", 1, "1 oder -1: dreht alle Flossen (wenn das Schiff mit Flossen staerker statt ruhiger nickt/rollt)"),
    ("Richtung links", 1, "Linke Flossen: + = Vorderkante hoch (Test-Chip 02.10.)"),
    ("Richtung rechts", 1, "Rechte Flossen (gespiegelt gesetzt): + = ebenfalls Vorderkante hoch (Test-Chip 02.10.)"),
    ("Flossen Test", 0, "1 = im Stand (unter 'Ab Tempo kn') alle Flossen auf Vorderkante hoch - zum Nachsehen; danach wieder 0"),
    ("Ziel Nick Grad", 0, "So soll das Schiff in Fahrt liegen (+ = Nase hoch)"),
    ("Nick P", 0.15, "Flossen-Ausschlag je Grad Nick-Fehler (bei Bezugs-Tempo)"),
    ("Nick D", 0.05, "Flossen-Ausschlag je Grad/s Nick-Drehung (daempft das Nicken)"),
    ("Roll P", 0.15, "Flossen-Ausschlag je Grad Schraeglage"),
    ("Roll D", 0.05, "Flossen-Ausschlag je Grad/s Roll-Drehung"),
    ("Nick I", 0.03, "Langsamer Ausgleich je Grad und Sekunde Nick-Fehler (Trimm in Fahrt)"),
    ("Roll I", 0.03, "Langsamer Ausgleich je Grad und Sekunde Schraeglage (dauernde Schlagseite)"),
    ("Hub D", 0.1, "Vordere Flossen: Ausschlag je m/s Steigen/Sinken des Bugs"),
    ("Heck runter", 0.5, "Hintere Flossen: Ausschlag nach unten je m/s, mit dem das Heck gleich steigen wird (Schrauben im Wasser halten)"),
    ("Heck hoch", 0.1, "Hintere Flossen: Ausschlag nach oben je m/s, mit dem das Heck gleich sinkt (schwach: tiefes Heck stoert nicht)"),
    ("Vorhalt s", 0.3, "So weit schaut der Chip voraus (die Flossen wirken verzoegert)"),
    ("Bug Abstand m", 16, "Abstand vordere Flossen - Physik-Sensor (m, laengs)"),
    ("Heck Abstand m", 22, "Abstand hintere Flossen - Physik-Sensor (m, laengs)"),
    ("Roll hinten Anteil", 0.5, "So viel von der Roll-Regelung bekommen die hinteren (sie hoben dabei oft eine Schraube an)"),
    ("Roll vorn-Mitte Anteil", 1, "Roll-Regelung der vorderen mittleren Flossen (+-9,-21,-2)"),
    ("Nick vorn-Mitte Anteil", 0.3, "Nick-Regelung der vorderen mittleren Flossen"),
    ("Schraube tief min m", 1.5, "Heck-Wasser (Liquid Meter auf Schrauben-Hoehe): laeuft die Schraube (mit Vorhalt) flacher, Heck runter (m; Fahrt 02.10.: normal 1.5-2.5)"),
    ("Heck-Wasser Richtung", -1, "-1 = der Messer meldet die Tiefe (+ unter Wasser; Andres seitlich eingebauter Messer, Fahrt 02.10. 18:07), 1 = Hoehe ueber dem Wasser"),
    ("Wasser Druck", 1.5, "Hintere/mittlere Flossen: Ausschlag nach unten je m, den die Schraube zu flach ist"),
    ("Vorn Nick Anteil", 0.5, "So viel von der Nick-Regelung bekommen die vorderen (den Bug runterdruecken hebelt das Heck hoch)"),
    ("Bezugs-Tempo kn", 60, "Bei diesem Tempo gelten die Werte; langsamer mehr Ausschlag ((Bezug/Tempo)^2), schneller weniger"),
    ("Ab Tempo kn", 6, "Darunter stehen die Flossen gerade"),
    ("Verstaerkung max", 4, "Hoechstens so viel mehr Ausschlag bei langsamer Fahrt"),
    ("Roll vorn Anteil", 0, "Die vorderen Flossen sitzen nah an der Mitte: so viel von der Roll-Regelung bekommen sie"),
    ("Mitte Nick Anteil", 0.6, "Die mittleren Flossen sitzen naeher am Schwerpunkt: so viel von der Nick-Regelung bekommen sie"),
    ("Log Port", 8767, "Flossen-Schreiber: Port von tools/logger.py (0 = aus; Schiffs-Schreiber 8766)"),
]

# Anschluesse: (Name, Eingang?, Typ, Beschreibung, Feld x, z, Ausgangskanal)
NODES = [
    ("Physik-Sensor", True, 5, "Physics Sensor: Composite Output (derselbe wie am Schiffs-Chip)", 0, 0, None),
    ("Flossen vorn L", False, 1, "Control Fin Medium vorn links (x=-1, z 25 und 28): Rotation", 1, 0, 0),
    ("Flossen vorn R", False, 1, "Control Fin Medium vorn rechts (x=+1, z 25 und 28): Rotation", 2, 0, 1),
    ("Flossen hinten L", False, 1, "Control Fin Medium hinten links (x=-10, z -120 und -134): Rotation", 0, 1, 2),
    ("Flossen hinten R", False, 1, "Control Fin Medium hinten rechts (x=+10, z -120 und -134): Rotation", 1, 1, 3),
    ("Flossen Mitte L", False, 1, "Control Fin Medium Mitte hinten links (x=-9, z -92): Rotation", 2, 1, 4),
    ("Flossen Mitte R", False, 1, "Control Fin Medium Mitte hinten rechts (x=+9, z -92): Rotation", 0, 2, 5),
    ("Flossen vorn-Mitte L", False, 1, "Control Fin Large vorn-Mitte links (x=-9, z -2): Rotation", 1, 2, 6),
    ("Flossen vorn-Mitte R", False, 1, "Control Fin Large vorn-Mitte rechts (x=+9, z -2): Rotation", 2, 2, 7),
    ("Heck-Wasser", True, 1, "Liquid Meter am Heck auf Schrauben-Hoehe (aussen, nicht kopfueber): Liquid Level", 0, 3, None),
]


def build(src, test=False):
    mc = MC("Figet Marena Flossen", "TEST: alle Flossen +0.7 - danach wieder den Flossen-Chip einsetzen" if test else
            "Flossen v1.8: 12 Steuerflossen halten Nick/Roll gerade; Heck zuerst, Heck-Messer; Physik + Batterie weiter", 3, 4)
    phys = mc.node(NODES[0][0], 1, NODES[0][2], NODES[0][3], NODES[0][4], NODES[0][5], (-8, 2))
    wn = NODES[-1]
    wasser = mc.node(wn[0], 1, wn[2], wn[3], wn[4], wn[5], (-8, 0))
    # Heck-Wasser auf Kanal 20 des Physik-Composite, v1.8 Batterie-Ladung auf Kanal 21 (Eingang kommt unten dazu)
    wk = mc.comp(40, (-5, 2), {"count": 2, "offset": 19}, [("inc", (phys, 0)), (wasser, 0)])
    lua = mc.comp(56, (-3, 2), {"script": src}, [(wk, 0)])
    for k, (name, val, desc) in enumerate(PROPS):
        mc.comp(34, (-10 - 2 * (k // 8), -4 - (k % 8)), {"n": name},
                extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))
    for k, (label, ein, typ, desc, x, z, ch) in enumerate(NODES[1:-1]):
        r = mc.comp(31, (5, 4 - k), {"i": ch} if ch else {}, [(lua, 0)])
        mc.node(label, 0, typ, desc, x, z, (8, 4 - k), (r, 0))
    # v1.7: Physik-Sensor mit Heck-Wasser auf Kanal 20 weiter an den Schiffs-Chip (dessen Wellen-Skript); letzter Anschluss
    mc.node("Physik weiter", 0, 5, "An den Schiffs-Chip, Eingang 'Physik-Sensor' (Physics Sensor + Heck-Wasser auf Kanal 20)", 1, 3, (0, -2), (wk, 0), late=True)
    # v1.8 (10.10.): Batterie-Ladung fuer die E-Motoren der Schiffsfuehrung - neuer Anschluss am Ende, Kanal 21
    batt = mc.node("Batterie", 1, 1, "Electric Battery Large (-4,-13,-46): Charge (0..1)", 2, 3, (-8, -1), late=True)
    next(c for c in mc.comps if c[1] == wk)[3].append((batt, 0))
    return mc


def main():
    test = "--test" in sys.argv
    with open(os.path.join(LUA_DIR, "flossen_test.lua" if test else "flossen.lua"), encoding="utf-8") as f:
        src = minify(f.read())
    print("flossen %5d Zeichen %s" % (len(src), "OK" if len(src) <= LUA_LIMIT else "ZU LANG"))
    if len(src) > LUA_LIMIT:
        sys.exit("Skript zu lang")
    os.makedirs(BUILD, exist_ok=True)
    out = os.path.join(BUILD, TEST_FILE if test else MC_FILE)
    with open(out, "w", encoding="utf-8") as f:
        f.write(build(src, test).xml())
    print("geschrieben:", out)
    if "--install" in sys.argv:
        dst = os.path.join(os.environ["APPDATA"], "Stormworks", "data", "microprocessors", MC_FILE)
        shutil.copy(out, dst)
        print("installiert:", dst)


if __name__ == "__main__":
    main()
