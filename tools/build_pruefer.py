"""Baut das Mini-Fahrzeug 'Lua Pruefer' (ein Block + ein Chip 2x2 mit lua/pruefer.lua) und legt es in den
Fahrzeug-Ordner des Spiels. Im Spiel spawnen, waehrend tools/pruefer_empfang.py laeuft - der Chip schickt die Liste
aller Lua-Funktionen, die Stormworks anbietet, an den PC.
Aufruf: python tools/build_pruefer.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import MC, minify, LUA_LIMIT, LUA_DIR, BUILD  # noqa: E402
import umbau_v1 as u  # noqa: E402

NAME = "Lua Pruefer"


def main():
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(LUA_DIR, "pruefer.lua"), encoding="utf-8") as f:
        src = minify(f.read())
    print("pruefer %d Zeichen %s" % (len(src), "OK" if len(src) <= LUA_LIMIT else "ZU LANG"))
    if len(src) > LUA_LIMIT:
        sys.exit("Skript zu lang")
    mc = MC(NAME, "Schickt die Liste aller Lua-Funktionen im Spiel an tools/pruefer_empfang.py (Port 8769)", 2, 2)
    mc.comp(56, (0, 0), {"script": src}, [])
    chip = os.path.join(BUILD, NAME + ".xml")
    with open(chip, "w", encoding="utf-8", newline="\n") as f:
        f.write(mc.xml())
    u.CHIP = chip
    d = u.chip_eingebettet()
    w, ln = 2, 2
    teil = '<c d="microprocessor"><o r="1,0,0,0,1,0,0,0,1" sc="%d">%s<vp y="1"/><logic_slots/></o></c>' % (
        2 * w * ln + 2 * (w + ln), d)
    fz = ('<?xml version="1.0" encoding="UTF-8"?><vehicle data_version="3" bodies_id="1"><authors/><bodies>'
          '<body unique_id="1"><components><c><o r="1,0,0,0,1,0,0,0,1" sc="6"/></c>%s</components></body></bodies>'
          '<logic_node_links/></vehicle>' % teil)
    ziel = os.path.join(os.environ["APPDATA"], "Stormworks", "data", "vehicles", NAME + ".xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(fz)
    print("Fahrzeug geschrieben:", ziel)


if __name__ == "__main__":
    main()
