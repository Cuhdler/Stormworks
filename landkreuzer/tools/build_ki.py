"""Baut den Chip "Landkreuzer KI" (5 x 4): KI_KLEBER (Schalter, Start-Verzoegerung, Ziel) -> KI_FAHREN (Fahr-KI, Skid-
Steuerung) -> KI_KARTE (Karten-Monitor 3x3 mit Touch: Wegpunkte setzen).

Anschluesse (Feld x, z):
  Eingaenge  (0,0) Physik-Sensor  (1,0) Sitz  (2,0) Instrumente  (3,0) Bedienung (Bildschirm-Chip)  (4,0) Karte Touch
             (0..4,1) Laser vorn links / vorn Mitte / vorn rechts / links / rechts   (0,2) Laser unten  (1,2) Laser hinten
             (2,2) Batterie (Ladestand, darf fehlen)
  Ausgaenge  (0,3) Links (alle linken Motoren)  (1,3) Rechts  (2,3) Karte (Video)  (3,3) Wahl (an den Bildschirm-Chip:
             Bool 1 Master Arm)  (4,3) Zustand (Ausgang von KI_FAHREN)
"""
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
from build_mc import MC, minify, fmt, LUA_LIMIT  # noqa: E402

LK_LUA = os.path.join(os.path.dirname(HIER), "lua")
VERSION = "v1.0"

LASER_NAMEN = ["Laser vorn links", "Laser vorn Mitte", "Laser vorn rechts", "Laser links", "Laser rechts",
               "Laser unten", "Laser hinten"]
PROPS_KLEBER = [
    ("Start Verzoegerung s", 10, "Nach dem Spawnen so lange warten, bis die KI faehrt und die Waffen frei sind"),
]


def lua(name):
    pfad = os.path.join(LK_LUA, name + ".lua")
    return minify(open(pfad, encoding="utf-8").read())


def props():
    """Eigenschaften aller drei Skripte (ki_props.py vom Fahr-KI-Teil, falls vorhanden)."""
    out = list(PROPS_KLEBER)
    try:
        import ki_props
        for liste in (getattr(ki_props, "PROPS_FAHREN", []), getattr(ki_props, "PROPS_KARTE", [])):
            for p in liste:
                if p[0] not in [q[0] for q in out]:
                    out.append(tuple(p[:3]))
    except ImportError:
        pass
    return out


def build(src=None, eigen=None):
    src = src or {n: lua(n) for n in ("ki_kleber", "ki_fahren", "ki_karte")}
    for n, s in src.items():
        assert len(s) <= LUA_LIMIT, (n, len(s))
    mc = MC("Landkreuzer KI", "KI %s: faehrt selbst (Wegpunkte, Revier, Ausweichen, nach Hause), Karte mit Touch, Waffen frei"
            % VERSION, 5, 4)
    phys = mc.node("Physik-Sensor", 1, 5, "Physics Sensor (derselbe wie an allen Waffen-Chips)", 0, 0, (-14, 8))
    sitz = mc.node("Sitz", 1, 5, "Steuersitz: Seat data (W/S, A/D zum Selberfahren, besetzt)", 1, 0, (-14, 7))
    inst = mc.node("Instrumente", 1, 5, "Instrumentenblock: Out Signal (1 Waffen sperren, 3 KI Pause, 4 Nach Hause)", 2, 0,
                   (-14, 6))
    bed = mc.node("Bedienung", 1, 5, "Bildschirm-Chip: Ausgang 'Bedienung' (Ziele der Waffen)", 3, 0, (-14, 5))
    touch = mc.node("Karte Touch", 1, 5, "Monitor 3x3 links am Sitz: Touch Output", 4, 0, (-14, 4))
    las = [mc.node(n, 1, 1, "%s: Distance" % n.replace("Laser", "Laser Distance Sensor"), k % 5, 1 + k // 5,
                   (-14, 3 - k)) for k, n in enumerate(LASER_NAMEN)]
    bat = mc.node("Batterie", 1, 1, "Battery: Charge Level (0..1; darf fehlen)", 2, 2, (-14, -4))

    def rd(q, ch, pos, typ=31):
        return mc.comp(typ, pos, {"i": ch} if ch else {}, [(q, 0)])

    # --- KI_KLEBER: Physik-Composite + Bedienung (BC/AC-Ziel) + Instrumente + 'Ziel da'
    w = mc.comp(40, (-10, 8), {"count": 6, "offset": 20}, [("inc", (phys, 0))] + [
        (rd(bed, ch, (-12, 8 - .5 * j)), 0) for j, ch in enumerate((7, 8, 9, 11, 12, 13))])
    w = mc.comp(41, (-10, 6), {"count": 6}, [("inc", (w, 0))] + [(rd(inst, ch, (-12, 5 - .5 * j), 29), 0)
                                                              for j, ch in enumerate((0, 1, 2, 3))] +
                [(rd(bed, ch, (-12, 3 - .5 * j), 29), 0) for j, ch in enumerate((8, 9))])
    kleber = mc.comp(56, (-8, 6), {"script": src["ki_kleber"]}, [(w, 0)])

    # --- KI_FAHREN: Kleber-Ausgang + Physik, Laser, Sitz, Karten-Befehle
    werte = [rd(phys, ch, (-8, 3 - .5 * j)) for j, ch in enumerate((0, 1, 2, 16, 14, 15, 12, 8))]
    werte += las + [bat] + [rd(sitz, ch, (-8, -3 - .5 * j)) for j, ch in enumerate((0, 1))]
    w = mc.comp(40, (-5, 6), {"count": len(werte)}, [("inc", (kleber, 0))] + [(c, 0) for c in werte])
    w = mc.comp(41, (-5, 5), {"count": 1, "offset": 1}, [("inc", (w, 0)), (rd(sitz, 31, (-8, -5), 29), 0)])
    fahren_in = w                                  # Karten-Befehle kommen unten dazu (Kreis ueber KI_KARTE)
    fahren = mc.comp(56, (-2, 5), {"script": src["ki_fahren"]}, [])

    # --- KI_KARTE: Ausgang von KI_FAHREN + Monitor-Touch (Zahl 29-32, Bool 32)
    k = mc.comp(40, (0, 3), {"count": 4, "offset": 28}, [("inc", (fahren, 0))] + [
        (rd(touch, ch, (-2, 2 - .5 * j)), 0) for j, ch in enumerate((0, 1, 2, 3))])
    k = mc.comp(41, (0, 2), {"count": 1, "offset": 31}, [("inc", (k, 0)), (rd(touch, 0, (-2, 0), 29), 0)])
    karte = mc.comp(56, (2, 2), {"script": src["ki_karte"]}, [(k, 0)])
    # Karten-Befehle (Zahl 23-25, Bool 3/5) zurueck in den Eingang von KI_FAHREN
    w = mc.comp(40, (-3, 3), {"count": 3, "offset": 22}, [("inc", (fahren_in, 0))] + [
        (rd(karte, ch, (-4, 1 - .5 * j)), 0) for j, ch in enumerate((22, 23, 24))])
    w = mc.comp(41, (-3, 2), {"count": 1, "offset": 2}, [("inc", (w, 0)), (rd(karte, 2, (-4, -1), 29), 0)])
    w = mc.comp(41, (-3, 1.5), {"count": 1, "offset": 4}, [("inc", (w, 0)), (rd(karte, 4, (-4, -1.5), 29), 0)])
    next(c for c in mc.comps if c[1] == fahren)[3].append((w, 0))

    for j, (name, val, desc) in enumerate(eigen or props()):
        mc.comp(34, (-18 - 2 * (j // 12), 8 - (j % 12)), {"n": name}, extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))

    def aus(label, q, ch, ntype, desc, x, y, typ=31):
        mc.node(label, 0, ntype, desc, x, 3, (8, y), (rd(q, ch, (5, y), typ), 0))

    aus("Links", fahren, 0, 1, "alle Elektromotoren der linken Raeder: Throttle", 0, 6)
    aus("Rechts", fahren, 1, 1, "alle Elektromotoren der rechten Raeder: Throttle", 1, 5)
    mc.node("Karte", 0, 6, "Monitor 3x3 links am Sitz: Video", 2, 3, (8, 4), (karte, 1))
    wahl = mc.comp(41, (5, 3), {"count": 1}, [(rd(kleber, 9, (3, 3), 29), 0)])
    mc.node("Wahl", 0, 5, "an den Bildschirm-Chip (Eingang 'Wahl'): Bool 1 Master Arm", 3, 3, (8, 3), (wahl, 0))
    mc.node("Zustand", 0, 5, "Ausgang der Fahr-KI (Zustand, Wegpunkte) - frei fuer Anzeigen", 4, 3, (8, 2), (fahren, 0))
    assert len(mc.desc) <= 128, len(mc.desc)
    return mc


if __name__ == "__main__":
    m = build()
    print(len(m.embedded()), "Zeichen;", [n[0] for n in m.node_liste()])
