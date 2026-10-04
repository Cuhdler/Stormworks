"""Baut den Chip "Figet Marena Kamera" (4 x 5): steuert die Dachkamera (Camera Stabilized auf dem Bruecken-Dach) fuer
alle Waffen - Skript lua/kamera.lua (Andre 04.10.: "eine bewegliche Kamera auf dem Dach, die fuer alle Waffen ist").
- mit --install zusaetzlich nach %APPDATA%/Stormworks/data/microprocessors kopieren
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import MC, minify, fmt, LUA_LIMIT, LUA_DIR, BUILD  # noqa: E402
from build_lage import schreiber_props, kopf  # noqa: E402

VERSION = "v2.2"
PROPS = [
    ("Messfahrt", 1, "1 = beim Spawnen ~6 s messen: Tempo, Kipp-Seite, wohin Drehung 0 zeigt (Laser); 0 = Werte unten"),
    ("Ziel See m", 40, "So gross ist ein Schiff etwa (Zoom fuer BC/AC)"),
    ("Ziel Luft m", 20, "So gross ist ein Flugziel etwa (Zoom fuer die Flaks)"),
    ("Bildanteil", 0.5, "So viel der sichtbaren Bildbreite fuellt das Ziel (kleiner = weiter)"),
    ("Sichtbar Anteil", 0.333, "Der grosse Monitor zeigt nur das mittlere Drittel des Kamerabilds"),
    ("FOV ohne Ziel rad", 1.2, "Bildwinkel ohne Waffe oder Ziel"),
    ("FOV weit rad", 2.2, "Camera Stabilized: Bildwinkel bei Zoom-Eingang 0"),
    ("FOV eng rad", 0.025, "Camera Stabilized: Bildwinkel bei Zoom-Eingang 1"),
    ("Kamera vor Physik m", 5.75, "Kamera (0,33,-15) liegt so weit vor dem Physik-Sensor (0,27,-38)"),
    ("Kamera ueber Physik m", 1.5, "... und so hoch darueber"),
    ("Blick Mitte X Grad", 0, "Blick X (Grad) beim Blick aufs Fadenkreuz in der Monitormitte (Hotkey 6 2 s halten lernt es)"),
    ("Blick Mitte Y Grad", 15, "Blick Y (Grad) beim Blick aufs Fadenkreuz (geschaetzt; im Log 'blick_mitte_y' nach dem Lernen)"),
    ("Blick X Richtung", 1, "1, wenn Blick X beim Blick nach rechts groesser wird, sonst -1"),
    ("Blick Y Richtung", 1, "1, wenn Blick Y beim Blick nach oben groesser wird, sonst -1"),
    ("Kreis Grad", 8, "Nur wenn die Blickmitte so nah am Fadenkreuz ist, wird korrigiert (sonst Umschauen)"),
    ("Totzone Grad", 0.8, "So nah am Fadenkreuz bewegt sich nichts (ruhig halten)"),
    ("Korrektur mrad/s", 2, "Am Kreisrand wandert der Zielpunkt so schnell (2 mrad/s = 4 m/s auf 2 km), innen langsamer"),
    ("Kreis Pixel", 16, "Halbmesser des gezeichneten Kreises um das Fadenkreuz"),
    ("Totzone", 0.1, "Pivot/Pitch sind Tempo-Eingaenge: darunter bewegt sich nichts (gemessen 04.10.: 0,1)"),
    ("Tempo je Befehl U/s", 0.106, "Drehtempo je 1 ueber der Totzone (gemessen 0,106 U/s; die Messfahrt misst es neu)"),
    ("Kipp Befehl", -1, "Zu dieser Seite kippt die Messfahrt (+1 kippte ueber die Stirn: Bild stand auf dem Kopf)"),
    ("Drehung 0 ab Bug U", 0.5, "Ohne Laser-Treffer bei der Messfahrt: dahin schaut die Kamera bei Drehung 0 (U ab Bug)"),
    ("Drehung Vorzeichen", 1, "Ohne Laser-Treffer: 1 = Drehung waechst im Uhrzeigersinn, -1 = gegen"),
]


def build(src):
    mc = MC("Figet Marena Kamera", "Kamera %s: Dachkamera schaut auf das Ziel der gewaehlten Waffe und zoomt nach Entfernung"
            % VERSION, 4, 5)
    bed = mc.node("Bedienung", 1, 5, "Bildschirm-Chip: Ausgang 'Bedienung' (gewaehlte Waffe und ihr Ziel)", 0, 0, (-10, 4))
    phys = mc.node("Physik-Sensor", 1, 5, "Physics Sensor (Composite, derselbe wie am Schiffs-Chip)", 1, 0, (-10, 3))
    kd = mc.node("Kamera Daten", 1, 5, "Camera Stabilized: Composite Output (Laser-Ziel x/y/z, Neigung, Gier)", 2, 0, (-10, 2))
    le = mc.node("Laser Entfernung", 1, 1, "Camera Stabilized: Laser Distance", 3, 0, (-10, 1))

    def rd(q, ch, pos, typ=31):
        return mc.comp(typ, pos, {"i": ch} if ch else {}, [(q, 0)])

    w = mc.comp(40, (-6, 4), {"count": 5, "offset": 6}, [("inc", (bed, 0))] + [(rd(kd, j, (-8, 3 - .5 * j)), 0) for j in range(5)])
    w = mc.comp(40, (-5, 3), {"count": 3, "offset": 25}, [("inc", (w, 0))] + [(rd(phys, j, (-8, 0 - .5 * j)), 0) for j in range(3)])
    w = mc.comp(40, (-4, 2), {"count": 2, "offset": 28}, [("inc", (w, 0)), (rd(phys, 14, (-8, -2)), 0), (rd(phys, 15, (-8, -2.5)), 0)])
    w = mc.comp(40, (-3, 1), {"count": 1, "offset": 31}, [("inc", (w, 0)), (le, 0)])
    # v2.0: Blick X/Y (Sitz 9/10) auf Zahl 12/13, Hotkey 6 / besetzt auf Bool 1/2; Video der Dachkamera durch BILD-artig
    sitz = mc.node("Sitz", 1, 5, "Steuersitz: Seat data (Blick X/Y, Hotkey 6, besetzt)", 0, 1, (-10, 0), late=True)
    vin = mc.node("Video ein", 1, 6, "Camera Stabilized: Camera Feed", 1, 1, (-10, -1), late=True)
    w = mc.comp(40, (-2, 0), {"count": 2, "offset": 11}, [("inc", (w, 0)), (rd(sitz, 8, (-8, -3)), 0), (rd(sitz, 9, (-8, -3.5)), 0)])
    w = mc.comp(41, (-1, 0), {"count": 2, "offset": 0}, [("inc", (w, 0)), (rd(sitz, 5, (-8, -4), 29), 0),
                                                         (rd(sitz, 31, (-8, -4.5), 29), 0)])
    # v2.2: Knopf 'Aim correction' des Instrumentenblocks (dort Bool 2) auf Bool 3
    inst = mc.node("Instrumente", 1, 5, "Instrumentenblock: Out Signal (Bool 2 Knopf Zielkorrektur)", 2, 1, (-10, -2), late=True)
    w = mc.comp(41, (-1, -1), {"count": 1, "offset": 2}, [("inc", (w, 0)), (rd(inst, 1, (-8, -5), 29), 0)])
    lua = mc.comp(56, (0, 1), {"script": src}, [(w, 0), (vin, 0)])
    for k, (name, val, desc) in enumerate(PROPS):
        mc.comp(34, (-12 - 2 * (k // 10), 8 - (k % 10)), {"n": name}, extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))
    schreiber_props(mc, -20, 8)

    def aus(label, ch, ntype, desc, x, z, y, typ=31):
        mc.node(label, 0, ntype, desc, x, z, (7, y), (rd(lua, ch, (4, y), typ), 0))

    aus("Drehung", 0, 1, "Camera Stabilized: Pivot Rotation", 0, 2, 4)
    aus("Neigung", 1, 1, "Camera Stabilized: Pitch Rotation", 1, 2, 3)
    aus("Zoom", 2, 1, "Camera Stabilized: Field of View", 2, 2, 2)
    aus("Laser an", 0, 0, "Camera Stabilized: Enable Laser", 3, 2, 1, typ=29)
    mc.node("Video aus", 0, 6, "an den Bildschirm-Chip (alle 4 Kamera-Eingaenge): Kamerabild mit Kreis und Marke", 0, 3, (7, 0),
            (lua, 1), late=True)
    mc.node("Korrektur", 0, 5, "an die 4 Turm-Chips: Zielpunkt-Korrektur je Waffe (Zahl 2+2w / 3+2w, U)", 1, 3, (7, -1),
            (lua, 0), late=True)
    # neue Anschluesse in der Reihenfolge, in der sie dazukamen (die alten behalten ihre Kabel)
    folge = ["Sitz", "Video ein", "Video aus", "Korrektur", "Instrumente"]
    mc.late.sort(key=lambda e: folge.index(e[1]))
    return mc


def main():
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(LUA_DIR, "kamera.lua"), encoding="utf-8") as f:
        src = kopf(minify(f.read()), "ka")
    print("kamera %5d Zeichen %s" % (len(src), "OK" if len(src) <= LUA_LIMIT else "ZU LANG"))
    if len(src) > LUA_LIMIT:
        sys.exit("Skript zu lang")
    mc = build(src)
    assert len(mc.desc) <= 128, len(mc.desc)
    fname = "Figet Marena Kamera %s.xml" % VERSION
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
