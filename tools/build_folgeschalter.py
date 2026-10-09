"""Baut den Folgeschalter (Andre 06.10.) als zwei Chips fuer die Chip-Bibliothek (NICHT ins Schiff):
- "Folgeschalter 54 Teil 1" (6 x 6): Eingang (an/aus), Eingang Zahl, Reset, Ausgang 1-32, Kette (an Teil 2)
- "Folgeschalter 54 Teil 2" (5 x 5): Kette (von Teil 1), Ausgang 33-54
Jedes neue "an" am Eingang schaltet den naechsten Ausgang 'Puls s' lang an (lua/folgeschalter.lua). Ein Chip hat
hoechstens 36 Anschluesse - darum zwei.
Aufruf: python build_folgeschalter.py [--install]   (--install: nach %APPDATA%/Stormworks/data/microprocessors)
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import MC, minify, fmt, LUA_LIMIT, LUA_DIR, BUILD  # noqa: E402

VERSION = "v1.0"
PROPS = [
    ("Puls s", 4, "So lange bleibt ein Ausgang an"),
    ("Sperre s", 2, "Fruehestens so lange nach dem letzten zaehlt ein neues 'an' am Eingang"),
    ("Anzahl Ausgaenge", 54, "So viele Ausgaenge werden der Reihe nach geschaltet (hoechstens 54)"),
    ("Nach dem letzten von vorn", 0, "0 = nach dem letzten Ausgang nichts mehr, 1 = wieder bei Ausgang 1 anfangen"),
]
NAME1 = "Folgeschalter 54 Teil 1"
NAME2 = "Folgeschalter 54 Teil 2"


def felder(w, ln, frei):
    """Freie Felder (x, z) zeilenweise, ohne die schon belegten."""
    return [(x, z) for z in range(ln) for x in range(w) if (x, z) not in frei]


def teil1(src):
    mc = MC(NAME1, "Folgeschalter %s Teil 1: jedes neue 'an' am Eingang -> naechster Ausgang 4 s an; Ausgang 1-32, "
            "Kette an Teil 2" % VERSION, 6, 6)
    ein = mc.node("Eingang", 1, 0, "an/aus: jedes neue 'an' schaltet den naechsten Ausgang (2 s Sperre)", 0, 0, (-8, 4))
    zahl = mc.node("Eingang Zahl", 1, 1, "wie 'Eingang', als Zahl (mindestens 0,5 = an)", 1, 0, (-8, 3))
    rst = mc.node("Reset", 1, 0, "an = wieder bei Ausgang 1 anfangen, alle aus", 2, 0, (-8, 2))
    w = mc.comp(41, (-5, 3), {"count": 2, "offset": 0}, [(ein, 0), (rst, 0)])
    w = mc.comp(40, (-4, 2), {"count": 1, "offset": 0}, [("inc", (w, 0)), (zahl, 0)])
    lua = mc.comp(56, (-2, 2), {"script": src}, [(w, 0)])
    for k, (name, val, desc) in enumerate(PROPS):
        mc.comp(34, (-10, 8 - k), {"n": name}, extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))
    mc.node("Kette", 0, 5, "an 'Kette' von Teil 2 (Ausgang 33-54, Zahl 32 = schon geschaltet)", 3, 0, (6, 8), (lua, 0))
    for k, (x, z) in enumerate(felder(6, 6, {(0, 0), (1, 0), (2, 0), (3, 0)})[:32]):
        rd = mc.comp(29, (2, 7 - k * .5), {"i": k} if k else {}, [(lua, 0)])
        mc.node("Ausgang %d" % (k + 1), 0, 0, "an fuer 'Puls s' beim %d. 'an' am Eingang" % (k + 1), x, z, (6, 7 - k * .5),
                (rd, 0))
    return mc


def teil2():
    src = "function onTick()\nfor i=1,22 do output.setBool(i,input.getNumber(i)>.5) end\nend"
    mc = MC(NAME2, "Folgeschalter %s Teil 2: Ausgang 33-54 (Kette von Teil 1)" % VERSION, 5, 5)
    kette = mc.node("Kette", 1, 5, "von 'Kette' an Teil 1", 0, 0, (-6, 3))
    lua = mc.comp(56, (-3, 3), {"script": src}, [(kette, 0)])
    for k, (x, z) in enumerate(felder(5, 5, {(0, 0)})[:22]):
        rd = mc.comp(29, (0, 7 - k * .5), {"i": k} if k else {}, [(lua, 0)])
        mc.node("Ausgang %d" % (k + 33), 0, 0, "an fuer 'Puls s' beim %d. 'an' am Eingang (Teil 1)" % (k + 33), x, z,
                (4, 7 - k * .5), (rd, 0))
    return mc


def main():
    os.makedirs(BUILD, exist_ok=True)
    with open(os.path.join(LUA_DIR, "folgeschalter.lua"), encoding="utf-8") as f:
        src = minify(f.read())
    print("folgeschalter %d Zeichen %s" % (len(src), "OK" if len(src) <= LUA_LIMIT else "ZU LANG"))
    for mc in (teil1(src), teil2()):
        assert len(mc.desc) <= 128, len(mc.desc)
        fname = "%s.xml" % mc.name
        out = os.path.join(BUILD, fname)
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(mc.xml())
        print("geschrieben:", out, "Anschluesse", len(mc.nodes) + len(mc.late))
        if "--install" in sys.argv:
            dst = os.path.join(os.environ["APPDATA"], "Stormworks", "data", "microprocessors", fname)
            shutil.copyfile(out, dst)
            print("installiert:", dst)


if __name__ == "__main__":
    main()
