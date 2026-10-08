"""Baut den Chip "Figet Marena Seeradar" (2 x 3): Radar 6 am Mast kreist flach, der Monitor 3x3 zeigt ein 2D-Radar mit
See- und Bodenzielen - Skript lua/seeradar.lua (Andre 06.10.).
- mit --install zusaetzlich nach %APPDATA%/Stormworks/data/microprocessors kopieren
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import MC, minify, fmt, LUA_LIMIT, LUA_DIR, BUILD  # noqa: E402
from build_lage import schreiber_props, kopf  # noqa: E402

VERSION = "v2.1"
PROPS = [
    ("Such Tempo", 0.25, "So schnell kreist Radar 6 (U/s; der Schirm schafft hoechstens 0,28) - eine Runde = Zeit bis zum Verblassen"),
    ("Strahl Hoehe Grad", 0, "Strahl gegen das Deck (Grad); flach fuer See- und Bodenziele"),
    ("Vergessen s", 12, "So lange bleibt ein Kontakt ohne neue Ortung auf dem Schirm"),
    ("Mindestabstand m", 60, "Naeher zaehlt nicht (eigenes Schiff)"),
    ("Reichweite max m", 10000, "Weiter zaehlt nicht"),
    ("See Hoehe max m", 7, "Hoeher (Mittel der Ortungen, + 0,1 % der Entfernung) = Bodenziel (gruen), sonst Seeziel (blau)"),
    ("Luft ab m", 60, "Hoeher (+ 1 % der Entfernung) = Luftziel, wird nicht gezeigt"),
    ("Luft Tempo m/s", 28, "Schneller (von Runde zu Runde) = Luftziel, wird nicht gezeigt"),
    ("Kompass Richtung", -1, "-1: der Kompass des Physik-Sensors zaehlt gegen den Uhrzeigersinn (wie Lage)"),
    ("Radar ueber Physik m", 2.25, "Radar 6 (y 36) liegt so viel hoeher als der Physik-Sensor (y 27)"),
    ("Abstand Pixel", 5, "Reichweite (1 / 2,5 / 5 / 10 km) so gross wie moeglich, aber keine zwei See-/Bodenziele naeher als das"),
    ("Auswahl Pixel", 7, "Antippen waehlt das naechste Ziel, wenn es naeher als das am Finger liegt"),
    ("Geschuetz Zeit s", 20, "So lange schiesst die gewaehlte vordere Kanone auf das angetippte Ziel, dann wieder Automatik"),
    ("Bild drehen", 2, "Bild um so viele Viertel im Uhrzeigersinn drehen (2 = halbe Drehung: der Monitor liegt flach links neben dem Sitz)"),
]


def build(src, src2):
    mc = MC("Figet Marena Seeradar", "Seeradar %s: Radar 6 2D, See blau / Land gruen, Zoom selbst; Tippen = Ziel fuer BC/AC "
            "(20 s) oder Koordinaten" % VERSION, 4, 3)
    radar = mc.node("Radar", 1, 5, "Radar (Phalanx) 6 am Mast (5,36,-51): Radar Data", 0, 0, (-8, 3))
    phys = mc.node("Physik-Sensor", 1, 5, "Physics Sensor (0,27,-38): Composite Output", 1, 0, (-8, 2))
    touch = mc.node("Touch", 1, 5, "Monitor 3x3: Touch Output", 0, 1, (-8, 1))
    # v2.0: neue Anschluesse hinten (die alten behalten Lage und Kabel)
    bed = mc.node("Bedienung ein", 1, 5, "Bildschirm-Chip: Ausgang 'Bedienung'", 2, 0, (-8, -1), late=True)

    def rd(q, ch, pos, typ=31):
        return mc.comp(typ, pos, {"i": ch} if ch else {}, [(q, 0)])

    # SEERADAR: Physik x, Hoehe, z, Nick, Roll, Kompass -> Zahl 25-30; Touch x/y -> 21/22, gewaehlte Waffe -> 23;
    # Touch gedrueckt -> Bool 32
    w = mc.comp(40, (-4, 3), {"count": 6, "offset": 24},
                [("inc", (radar, 0))] + [(rd(phys, ch, (-6, 3 - .5 * j)), 0) for j, ch in enumerate((0, 1, 2, 14, 15, 16))])
    w = mc.comp(40, (-4, 1.5), {"count": 3, "offset": 20},
                [("inc", (w, 0)), (rd(touch, 2, (-6, 0.5)), 0), (rd(touch, 3, (-6, 0)), 0), (rd(bed, 1, (-6, -1)), 0)])
    w = mc.comp(41, (-3, 1), {"count": 1, "offset": 31}, [("inc", (w, 0)), (rd(touch, 0, (-6, -.5), 29), 0)])
    lua = mc.comp(56, (0, 2), {"script": src}, [(w, 0)])
    # UEBERGABE: Bedienung + Zahl 26-32 von SEERADAR (Ausgang 3-9) + Bool 32 (Koordinaten da)
    wb = mc.comp(40, (2, -1), {"count": 7, "offset": 25},
                 [("inc", (bed, 0))] + [(rd(lua, ch, (1, -1 - .5 * k)), 0) for k, ch in enumerate(range(2, 9))])
    wb = mc.comp(41, (3, -2), {"count": 1, "offset": 31}, [("inc", (wb, 0)), (rd(lua, 0, (1, -5), 29), 0)])
    lua2 = mc.comp(56, (4, -1), {"script": src2}, [(wb, 0)])
    for k, (name, val, desc) in enumerate(PROPS):
        mc.comp(34, (-10 - 2 * (k // 8), 8 - (k % 8)), {"n": name}, extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))
    schreiber_props(mc, -16, 8)
    mc.node("Gimbal", 0, 5, "Radar (Phalanx) 6: Gimbal Input", 1, 1, (6, 3), (lua, 0))
    mc.node("Monitor", 0, 6, "Monitor 3x3: Video Signal", 0, 2, (6, 2), (lua, 1))
    mc.node("Bedienung aus", 0, 5, "an Kanone BC, Kanone AC ('Lage') und Kamera-Chip ('Bedienung'): Bedienung mit Seeradar-Ziel",
            3, 0, (6, -1), (lua2, 0), late=True)
    mc.node("Ziel X", 0, 1, "Koordinate X (Ost, m) des zuletzt angetippten Ziels (ohne Kanone)", 2, 1, (6, -2),
            (rd(lua, 7, (4, -3)), 0), late=True)
    mc.node("Ziel Y", 0, 1, "Koordinate Y (Nord, m) des zuletzt angetippten Ziels (ohne Kanone)", 3, 1, (6, -3),
            (rd(lua, 8, (4, -3.5)), 0), late=True)
    mc.node("Monitor 1x2", 0, 6, "Monitor 1x2 vor dem Sitz: Video Signal (Koordinaten)", 2, 2, (6, -4), (lua2, 1), late=True)
    mc.node("Monitor 1x2 an", 0, 0, "Monitor 1x2: Power Switch", 3, 2, (6, -5), (rd(lua2, 16, (4, -5), 29), 0), late=True)
    folge = ["Bedienung ein", "Bedienung aus", "Ziel X", "Ziel Y", "Monitor 1x2", "Monitor 1x2 an"]
    mc.late.sort(key=lambda e: folge.index(e[1]))
    return mc


def main():
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(LUA_DIR, "seeradar.lua"), encoding="utf-8") as f:
        src = kopf(minify(f.read()), "sr")
    with open(os.path.join(LUA_DIR, "uebergabe.lua"), encoding="utf-8") as f:
        src2 = minify(f.read())
    for name, q in (("seeradar", src), ("uebergabe", src2)):
        print("%-9s %5d Zeichen %s" % (name, len(q), "OK" if len(q) <= LUA_LIMIT else "ZU LANG"))
        if len(q) > LUA_LIMIT:
            sys.exit("Skript zu lang")
    mc = build(src, src2)
    assert len(mc.desc) <= 128, len(mc.desc)
    fname = "Figet Marena Seeradar %s.xml" % VERSION
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
