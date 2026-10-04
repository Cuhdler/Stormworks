"""Figet Marena auf Schiff v2.1 (4 Motoren): Chip im Fahrzeug durch build/<MC_FILE> (6 x 6) ersetzen und die Kabel der
neuen oberen Motoren L2/R2 legen - als Kopie der Kabel von L1/R1, 8 Bloecke hoeher (die oberen Motoren sind Kopien):

- Chip-Anschluesse L1/R1 (RPS, Zylinder, Luft, Treibstoff, Anlasser, Kupplung) -> dieselben Kabel zu L2/R2-Anschluessen
- 'Motor L/R an' -> Pumpen und Kuehler-Luefter der oberen Motoren
- Strom von den Batterien -> Anlasser, Pumpen, Kuehler, Transponder der oberen Motoren

Jedes neue Kabelende wird geprueft: an der verschobenen Stelle muss dasselbe Teil mit demselben Anschluss sitzen.
Aufruf: python kabel_v21.py [--schreiben] [--scratch=PFAD fuer umbau_analyse]   (Schiff im Spiel nicht offen!)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1  # noqa: E402
from build_schiff import BUILD, MC_FILE, LAGE  # noqa: E402

SCRATCH = r"C:\Users\andre\AppData\Local\Temp\claude\C--Users-andre-Documents-Rok-Main-Cloude\e7277567-683d-4c4a-b442-a2cba45af6e9\scratchpad"
for a in sys.argv:
    if a.startswith("--scratch="):
        SCRATCH = a.split("=", 1)[1]
sys.path.insert(0, SCRATCH)
import umbau_analyse as ua  # noqa: E402

HOCH = (0, 8, 0)
chip = umbau_v1.chip
# alte Anschluesse (Lage wie v1.x) -> neue Anschluesse der oberen Motoren
CHIP_MAP = {}
for unten, oben in (("L1", "L2"), ("R1", "R2")):
    for (a, b) in zip(LAGE[unten], LAGE[oben]):
        CHIP_MAP[chip(*a)] = chip(*b)
MOTOR_AN = {chip(0, 3), chip(1, 3)}
BATTERIE = {(-8, -18, -64), (8, -18, -64)}


def plus(p, d=HOCH):
    return tuple(a + b for a, b in zip(p, d))


def im_unteren_motorraum(p):
    return 2 <= abs(p[0]) <= 14 and -20 <= p[1] <= -12 and -92 <= p[2] <= -60


def main():
    umbau_v1.CHIP = os.path.join(BUILD, MC_FILE)
    s = open(umbau_v1.VEH, encoding="utf-8", newline="").read()
    root, comps, idx, links = ua.load(umbau_v1.VEH)
    typ_an = {}
    for (c, d, name, v) in comps:
        typ_an[v] = (d, c.find("o").get("r"))

    def gleich(p, q):
        """q ist dieselbe Art Anschluss wie p (gleiche Teile/Labels); unbekannte Teile (Zylinder): gleiches Teil in der Naehe."""
        a, b = idx.get(p), idx.get(q)
        if a or b:
            return bool(a and b) and sorted((x[0], x[2], x[4]) for x in a) == sorted((x[0], x[2], x[4]) for x in b)
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    v = plus(p, (dx, dy, dz))
                    if v in typ_an and "piston" in typ_an[v][0]:
                        return typ_an.get(plus(v)) == typ_an[v]
        return False

    vorhanden = {(t, a, b) for (_, t, a, b) in links}
    neu, fehler, arten = [], [], {}
    for (_, t, a, b) in links:
        kopie = None
        if a in CHIP_MAP and b not in CHIP_MAP:          # Chip-Ausgang L1/R1 -> Teil
            kopie, art = (t, CHIP_MAP[a], plus(b)), "Chip-Ausgang"
            pruef = (b, plus(b))
        elif b in CHIP_MAP:                               # Teil -> Chip-Eingang L1/R1
            kopie, art = (t, plus(a), CHIP_MAP[b]), "Chip-Eingang"
            pruef = (a, plus(a))
        elif a in MOTOR_AN and im_unteren_motorraum(b):   # Motor an -> Pumpe/Kuehler
            kopie, art = (t, a, plus(b)), "Motor an"
            pruef = (b, plus(b))
        elif t == 4 and a in BATTERIE and b not in BATTERIE and im_unteren_motorraum(b):
            kopie, art = (t, a, plus(b)), "Strom"
            pruef = (b, plus(b))
        if kopie is None:
            continue
        if not gleich(*pruef):
            fehler.append((art, pruef, idx.get(pruef[0]), idx.get(pruef[1])))
            continue
        if kopie in vorhanden:
            continue
        vorhanden.add(kopie)
        neu.append(kopie)
        arten[art] = arten.get(art, 0) + 1
    print("neue Kabel:", len(neu), arten)
    for f in fehler:
        print("NICHT GEFUNDEN:", f)
    assert not fehler, "Teile der oberen Motoren nicht an der erwarteten Stelle"

    # Chip ersetzen (6 x 6: sc = Flaechen = 2*6*6 + 2*(6+6) = 96, ein logic_slot je Anschluss)
    a, e = umbau_v1.mc_bereich(s, "Figet Marena Schiffsfuehrung")
    teil = s[a:e]
    d0 = teil.index("<microprocessor_definition")
    d1 = teil.index("</microprocessor_definition>") + len("</microprocessor_definition>")
    neu_def = umbau_v1.chip_eingebettet()
    knoten = neu_def.count("<n id=")
    kopf = re.sub(r' sc="\d+"', ' sc="96"', teil[:d0], count=1)
    rest = re.sub(r"<logic_slots>(<slot/>)*</logic_slots>", "<logic_slots>" + "<slot/>" * knoten + "</logic_slots>", teil[d1:], count=1)
    s = s[:a] + kopf + neu_def + rest + s[e:]
    print("Chip %s eingesetzt (%d Anschluesse)" % (MC_FILE, knoten))

    # Kabel anhaengen
    li = s.index("</logic_node_links>")
    s = s[:li] + "".join('<logic_node_link%s>%s%s</logic_node_link>' % (' type="%d"' % t if t else "", umbau_v1.vox("voxel_pos_0", p0),
                                                                        umbau_v1.vox("voxel_pos_1", p1)) for t, p0, p1 in neu) + s[li:]
    if "--schreiben" in sys.argv:
        with open(umbau_v1.VEH, "w", encoding="utf-8", newline="") as f:
            f.write(s)
        print("geschrieben:", umbau_v1.VEH)
    else:
        out = os.path.join(SCRATCH, "marena_v21_probe.xml")
        with open(out, "w", encoding="utf-8", newline="") as f:
            f.write(s)
        print("Probelauf nach", out)


if __name__ == "__main__":
    main()
