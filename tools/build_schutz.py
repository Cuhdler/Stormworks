"""Baut den Chip "Figet Marena Schutz" (2 x 3): Auto-Chaff (Radar Detector -> beide Werfer-Ketten gleichzeitig) und
Lenzpumpen, beide ueber Schalter im Instrumentenblock - Skript lua/schutz.lua (Andre 04.10.).
- mit --install zusaetzlich nach %APPDATA%/Stormworks/data/microprocessors kopieren
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import MC, minify, fmt, LUA_LIMIT, LUA_DIR, BUILD  # noqa: E402
from build_lage import schreiber_props, kopf  # noqa: E402

VERSION = "v1.0"
PROPS = [
    ("Chaff Abstand s", 1.5, "Solange der Radar Detector ortet: so oft eine Salve (beide Seiten gleichzeitig)"),
    ("Chaff je Ortung", 8, "Hoechstens so viele Salven je Ortung (jede Kette hat 60 Werfer)"),
    ("Chaff Pause s", 3, "So lange keine Ortung, dann zaehlt die naechste als neue Ortung"),
]


def build(src):
    mc = MC("Figet Marena Schutz", "Schutz %s: Auto-Chaff (Radar Detector, beide Seiten) und Lenzpumpen ueber den Instrumentenblock"
            % VERSION, 2, 3)
    inst = mc.node("Instrumente", 1, 5, "Instrumentenblock: Out Signal (Bool 3 Auto-Chaff, 4 Pumpen)", 0, 0, (-6, 2))
    rw = mc.node("Radarwarner", 1, 0, "Radar Detector (unter der Dachkamera): Detected", 1, 0, (-6, 1))

    def rd(q, ch, pos, typ=31):
        return mc.comp(typ, pos, {"i": ch} if ch else {}, [(q, 0)])

    w = mc.comp(41, (-3, 2), {"count": 1, "offset": 4}, [("inc", (inst, 0)), (rw, 0)])
    lua = mc.comp(56, (0, 1), {"script": src}, [(w, 0)])
    for k, (name, val, desc) in enumerate(PROPS):
        mc.comp(34, (-10, 4 - k), {"n": name}, extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))
    schreiber_props(mc, -14, 4)
    mc.node("Chaff links", 0, 0, "Erster Werfer der linken Kette: Launch", 0, 2, (5, 2), (rd(lua, 0, (3, 2), 29), 0))
    mc.node("Chaff rechts", 0, 0, "Erster Werfer der rechten Kette: Launch", 1, 2, (5, 1), (rd(lua, 1, (3, 1), 29), 0))
    mc.node("Pumpen", 0, 0, "Beide Large Fluid Pumps: On/Off", 0, 1, (5, 0), (rd(lua, 2, (3, 0), 29), 0))
    return mc


def main():
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(LUA_DIR, "schutz.lua"), encoding="utf-8") as f:
        src = kopf(minify(f.read()), "sc")
    print("schutz %5d Zeichen %s" % (len(src), "OK" if len(src) <= LUA_LIMIT else "ZU LANG"))
    if len(src) > LUA_LIMIT:
        sys.exit("Skript zu lang")
    mc = build(src)
    assert len(mc.desc) <= 128, len(mc.desc)
    fname = "Figet Marena Schutz %s.xml" % VERSION
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
