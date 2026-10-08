"""Baut den Chip "Figet Marena Schotten" (4 x 3): 5 Schottwaende je 2 Schiebetueren - alle zu/auf vom Abteil-Chip,
dazu je Wand ein Kippschalter zum Oeffnen/Schliessen von Hand - Skript lua/schotten.lua (Andre 08.10.).
- mit --install zusaetzlich nach %APPDATA%/Stormworks/data/microprocessors kopieren
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import MC, minify, LUA_LIMIT, LUA_DIR, BUILD  # noqa: E402

VERSION = "v1.0"
# Schottwaende vom Bug zum Heck: (Tuer Backbord, Tuer Steuerbord, Kippschalter)
WAENDE = [((-4, -12, 3), (4, -12, 3), (-8, -11, 3)),
          ((-10, 5, -13), (10, 5, -13), (-6, 6, -14)),
          ((-11, -12, -15), (11, -12, -15), (-7, -11, -16)),
          ((-5, -12, -29), (5, -12, -29), (-7, -11, -28)),
          ((-9, -12, -53), (9, -12, -53), (-13, -11, -53))]


def build(src):
    mc = MC("Figet Marena Schotten", "Schotten %s: 5 Schottwaende (je 2 Tueren) - alle zu/auf vom Abteil-Chip, je Wand ein "
            "Kippschalter" % VERSION, 4, 3)
    pl = [(x, z) for z in range(3) for x in range(4)]
    alle = mc.node("Alle auf", 1, 0, "Abteil-Chip: Ausgang 'Schotten auf'", *pl[0], (-6, 3))
    kn = [mc.node("Knopf Wand %d" % (k + 1), 1, 0, "Kippschalter %s: Toggled" % (w[2],), *pl[1 + k], (-6, 2 - k))
          for k, w in enumerate(WAENDE)]
    w = mc.comp(41, (-3, 0), {"count": 6, "offset": 0}, [(alle, 0)] + [(n, 0) for n in kn])
    lua = mc.comp(56, (0, 0), {"script": src}, [(w, 0)])
    for k, wd in enumerate(WAENDE):
        mc.node("Tueren Wand %d" % (k + 1), 0, 0, "Schiebetueren %s und %s: Open/Close" % (wd[0], wd[1]), *pl[6 + k],
                (4, 3 - k), (mc.comp(29, (2, 3 - k), {"i": k} if k else {}, [(lua, 0)]), 0))
    mc.node("Zustand", 0, 5, "an den Abteil-Chip (Eingang 'Tueren'): Bool 1-5 Wand 1-5 auf", *pl[11], (4, -3), (lua, 0))
    return mc


def main():
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(LUA_DIR, "schotten.lua"), encoding="utf-8") as f:
        src = minify(f.read())
    print("schotten %5d Zeichen %s" % (len(src), "OK" if len(src) <= LUA_LIMIT else "ZU LANG"))
    mc = build(src)
    assert len(mc.desc) <= 128, len(mc.desc)
    fname = "Figet Marena Schotten %s.xml" % VERSION
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
