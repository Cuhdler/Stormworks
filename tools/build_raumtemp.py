"""Baut den Chip "Figet Marena Raumtemperatur" (2 x 1): zwei Temperature Probes im Maschinenraum mitschreiben
(lua/raumtemp.lua, Strom 'mr' an tools/waffen_logger.py). Andre 10.10.
- mit --install zusaetzlich nach %APPDATA%/Stormworks/data/microprocessors kopieren
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import MC, minify, LUA_LIMIT, LUA_DIR, BUILD  # noqa: E402
from build_lage import schreiber_props, kopf  # noqa: E402

VERSION = "v1.0"
SONDEN = [("Temperatur BB", (-2, -7, -82)), ("Temperatur SB", (2, -7, -82))]


def build(src):
    mc = MC("Figet Marena Raumtemperatur", "Raumtemperatur %s: 2 Temperature Probes im Maschinenraum - schreibt beide an den "
            "Waffen-Schreiber (mr)" % VERSION, 2, 1)
    ein = [mc.node(n, 1, 1, "Temperature Probe %s: Temperature" % (p,), k, 0, (-6, 1 - k)) for k, (n, p) in enumerate(SONDEN)]
    w = mc.comp(40, (-3, 0), {"count": 2}, [(e, 0) for e in ein])
    mc.comp(56, (0, 0), {"script": src}, [(w, 0)])
    schreiber_props(mc, -8, 4)
    return mc


def main():
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(LUA_DIR, "raumtemp.lua"), encoding="utf-8") as f:
        src = kopf(minify(f.read()), "mr")
    print("raumtemp %5d Zeichen %s" % (len(src), "OK" if len(src) <= LUA_LIMIT else "ZU LANG"))
    mc = build(src)
    assert len(mc.desc) <= 128, len(mc.desc)
    fname = "Figet Marena Raumtemperatur %s.xml" % VERSION
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
