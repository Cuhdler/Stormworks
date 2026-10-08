"""Baut den Chip "Figet Marena Licht" (2 x 2): 55 RGB-Lampen immer an, Tag/Nacht-Helligkeit nach der Uhr, Steuerungsraum
bei Bedrohung rot - Skript lua/licht.lua (Andre 08.10.).
- mit --install zusaetzlich nach %APPDATA%/Stormworks/data/microprocessors kopieren
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import MC, minify, fmt, LUA_LIMIT, LUA_DIR, BUILD  # noqa: E402

VERSION = "v1.0"
PROPS = [
    ("Tag ab Uhr", 6.5, "Ab dieser Uhrzeit (Stunde, Mitte der Daemmerung) Tag-Helligkeit"),
    ("Nacht ab Uhr", 19.5, "Ab dieser Uhrzeit Nacht-Helligkeit"),
    ("Daemmerung h", 1, "So lange (Stunden) geht die Helligkeit von Nacht zu Tag und zurueck ueber"),
    ("Hell Tag", 1, "Helligkeit am Tag (0-1)"),
    ("Hell Nacht", 0.35, "Helligkeit in der Nacht (0-1)"),
    ("Farbe R", 1, "Lichtfarbe Rot (0-1)"),
    ("Farbe G", 0.92, "Lichtfarbe Gruen (0-1)"),
    ("Farbe B", 0.8, "Lichtfarbe Blau (0-1)"),
    ("Rot hell", 1, "Steuerungsraum bei Bedrohung: so hell rot (mal Tag/Nacht-Helligkeit)"),
    ("Rot halten s", 5, "So lange bleibt der Steuerungsraum nach der letzten Bedrohungs-Meldung rot"),
]


def build(src):
    mc = MC("Figet Marena Licht", "Licht %s: 55 RGB-Lampen immer an, Tag/Nacht-Helligkeit nach der Uhr, Steuerungsraum bei "
            "Bedrohung rot" % VERSION, 2, 2)
    uhr = mc.node("Uhr", 1, 1, "Clock: Time (0 Mitternacht, 0,5 Mittag)", 0, 0, (-6, 2))
    lage = mc.node("Lage", 1, 5, "Lage-Chip: Ausgang 'Lage' (Bool 25 Bedrohung)", 0, 1, (-6, 1))
    w = mc.comp(40, (-3, 1), {"count": 1, "offset": 0}, [("inc", (lage, 0)), (uhr, 0)])
    lua = mc.comp(56, (0, 1), {"script": src}, [(w, 0)])
    sr = mc.comp(40, (2, 0), {"count": 3, "offset": 0},
                 [(mc.comp(31, (1, -1 - .5 * j), {"i": ch}, [(lua, 0)]), 0) for j, ch in enumerate((3, 4, 5))])
    for k, (name, val, desc) in enumerate(PROPS):
        mc.comp(34, (-10 - 2 * (k // 8), 8 - (k % 8)), {"n": name}, extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))
    mc.node("Licht", 0, 5, "an alle RGB-Lampen ausser Steuerungsraum: Color Data", 1, 1, (5, 1), (lua, 0))
    mc.node("Licht Steuerraum", 0, 5, "an die 4 Deckenlampen im Steuerungsraum: Color Data (bei Bedrohung rot)", 1, 0,
            (5, 0), (sr, 0))
    return mc


def main():
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(LUA_DIR, "licht.lua"), encoding="utf-8") as f:
        src = minify(f.read())
    print("licht %5d Zeichen %s" % (len(src), "OK" if len(src) <= LUA_LIMIT else "ZU LANG"))
    mc = build(src)
    assert len(mc.desc) <= 128, len(mc.desc)
    fname = "Figet Marena Licht %s.xml" % VERSION
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
