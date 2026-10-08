"""Baut den Chip "Landkreuzer KI" (5 x 5): KI_KLEBER (Schalter, Start-Verzoegerung, Ziel) -> KI_FAHREN (Fahr-KI, Skid-
Steuerung) -> KI_KARTE (Karten-Monitor 3x3 mit Touch: Wegpunkte setzen).

Anschluesse (Feld x, z):
  Eingaenge  (0,0) Physik-Sensor  (1,0) Sitz  (2,0) Instrumente  (3,0) Bedienung (Bildschirm-Chip)  (4,0) Karte Touch
             (0..4,1) Laser vorn links / vorn Mitte / vorn rechts / links / rechts   (0,2) Laser unten  (1,2) Laser hinten
             (2,2) Batterie (Ladestand, darf fehlen)   Ausgaenge (3,2) Schutz (an den Schutz-Chip: Auto-Chaff),
             (4,2) Status (Video an den Monitor 2x3)   (0,4) Lenkung vorn, (1,4) Lenkung hinten (nur Lenk-Variante)
             (4,4) Immer an (Ausgang: schaltet alle Laser und den Monitor 2x3 ein)
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
    ("Start Verzoegerung s", 10, "Nach dem Spawnen so lange warten, bis die KI faehrt"),
    ("Waffen Verzoegerung s", 60, "Nach dem Spawnen so lange warten, bis die Waffen frei sind (die KI kennt keinen Freund)"),
    # 0,4: Elektromotoren werden mit sinkender Ladung schwaecher (Forum) - bei 20 % kaeme er nicht mehr den Hang hoch
    ("Heim Batterie", 0.4, "Batterie darunter (0 bis 1): die KI faehrt von selbst nach Hause (0 = aus)"),
    ("Schutzzone m", 300, "Ziele so nah am Startpunkt (Werkbank, eigene Basis): keine Waffe schiesst (0 = aus)"),
]
PROPS_LENKUNG = [
    ("Lenk Faktor", 1, "Lenk-Variante: Lenkwinkel je Kurven-Befehl (1 = voller Befehl gibt 'Lenk max Grad')"),
    ("Lenk max Grad", 25, "Lenk-Variante: groesster Lenkwinkel der Gelenke vorn/hinten"),
    ("Lenk Richtung", 1, "Lenk-Variante: 1 oder -1, wenn er bei 'rechts' nach links lenkt"),
    ("Lenk Tempo m/s", 10, "Lenk-Variante: ab diesem Tempo wird der Lenkwinkel kleiner (doppeltes Tempo = halber Winkel)"),
    ("Lenk Tempo Grad/s", 30, "Lenk-Variante: so schnell schwenken die Gelenke hoechstens"),
]


def lua(name):
    pfad = os.path.join(LK_LUA, name + ".lua")
    return minify(open(pfad, encoding="utf-8").read())


# Schreiber im Status-Skript (wie die Waffen-Chips; bau_landkreuzer --schreiber setzt den Port auf 8768)
PROPS_SCHREIBER = [
    ("Schreiber Port", 0, "Schreiber: Port von tools/waffen_logger.py auf dem PC (0 = aus; 8768 wie die Waffen)"),
    ("Schreiber Zeichen", 3000, "Schreiber: hoechstens so viele Zeichen je Paket"),
]


def props():
    """Eigenschaften aller Skripte (ki_props.py vom Fahr-KI-Teil, falls vorhanden)."""
    out = list(PROPS_KLEBER) + list(PROPS_LENKUNG) + list(PROPS_SCHREIBER)
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
    src = src or {n: lua(n) for n in ("ki_kleber", "ki_fahren", "ki_karte", "ki_status", "ki_lenkung")}
    for n, s in src.items():
        assert len(s) <= LUA_LIMIT, (n, len(s))
    mc = MC("Landkreuzer KI", "KI %s: faehrt selbst (Wegpunkte, Revier, Ausweichen, nach Hause), Karte mit Touch, Waffen frei"
            % VERSION, 5, 5)
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

    # --- KI_KLEBER: Physik-Composite + Bedienung (Ziele von BC, AC, Flak L/R) + Instrumente + 'Ziel da'
    #     (Composite: nur Kanal 1-32! Flak-Ziele ohne Hoehe: 28/29 Flak L, 30/31 Flak R)
    w = mc.comp(40, (-10, 8), {"count": 11, "offset": 20}, [("inc", (phys, 0))] + [
        (rd(bed, ch, (-12, 8 - .5 * j)), 0) for j, ch in enumerate((7, 8, 9, 11, 12, 13))] + [(bat, 0)] + [
        (rd(bed, ch, (-12, 1 - .5 * j)), 0) for j, ch in enumerate((15, 16, 19, 20))])
    w = mc.comp(41, (-10, 6), {"count": 8}, [("inc", (w, 0))] + [(rd(inst, ch, (-12, 5 - .5 * j), 29), 0)
                                                              for j, ch in enumerate((0, 1, 2, 3))] +
                [(rd(bed, ch, (-12, 3 - .5 * j), 29), 0) for j, ch in enumerate((8, 9, 10, 11))])
    kleber_in = w                                  # Freund-Punkte der Karte kommen unten dazu (Kreis ueber KI_KARTE)
    kleber = mc.comp(56, (-8, 6), {"script": src["ki_kleber"]}, [])

    # --- KI_FAHREN: Kleber-Ausgang + Physik, Laser, Sitz, Karten-Befehle
    werte = [rd(phys, ch, (-8, 3 - .5 * j)) for j, ch in enumerate((0, 1, 2, 16, 14, 15, 12, 8))]
    werte += las + [bat] + [rd(sitz, ch, (-8, -3 - .5 * j)) for j, ch in enumerate((0, 1))]
    w = mc.comp(40, (-5, 6), {"count": len(werte)}, [("inc", (kleber, 0))] + [(c, 0) for c in werte])
    w = mc.comp(41, (-5, 5), {"count": 1, "offset": 1}, [("inc", (w, 0)), (rd(sitz, 31, (-8, -5), 29), 0)])
    fahren_in = w                                  # Karten-Befehle kommen unten dazu (Kreis ueber KI_KARTE)
    fahren = mc.comp(56, (-2, 5), {"script": src["ki_fahren"]}, [])

    # --- KI_KARTE: Ausgang von KI_FAHREN, ueberschrieben Zahl 1/2 Touch x/y (Monitor 3/4), 29/30 eigener Ort Ost/Nord
    #     (Physik 1/3), Bool 32 Touch gedrueckt (Monitor-Bool 1)
    k = mc.comp(40, (0, 3), {"count": 2}, [("inc", (fahren, 0))] + [
        (rd(touch, ch, (-2, 2 - .5 * j)), 0) for j, ch in enumerate((2, 3))])
    k = mc.comp(40, (0, 2.5), {"count": 2, "offset": 28}, [("inc", (k, 0))] + [
        (rd(phys, ch, (-2, 1 - .5 * j)), 0) for j, ch in enumerate((0, 2))])
    k = mc.comp(41, (0, 2), {"count": 1, "offset": 31}, [("inc", (k, 0)), (rd(touch, 0, (-2, 0), 29), 0)])
    karte = mc.comp(56, (2, 2), {"script": src["ki_karte"]}, [(k, 0)])
    # Karten-Befehle (Zahl 23-25, Bool 3/5) zurueck in den Eingang von KI_FAHREN
    w = mc.comp(40, (-3, 3), {"count": 3, "offset": 22}, [("inc", (fahren_in, 0))] + [
        (rd(karte, ch, (-4, 1 - .5 * j)), 0) for j, ch in enumerate((22, 23, 24))])
    w = mc.comp(41, (-3, 2), {"count": 1, "offset": 2}, [("inc", (w, 0)), (rd(karte, 2, (-4, -1), 29), 0)])
    w = mc.comp(41, (-3, 1.5), {"count": 1, "offset": 4}, [("inc", (w, 0)), (rd(karte, 4, (-4, -1.5), 29), 0)])
    next(c for c in mc.comps if c[1] == fahren)[3].append((w, 0))
    # Freund-Punkte der Karte (Zahl 1-8, 9 = Zahl der Punkte) -> Kleber Zahl 4-12 (dort ungenutzte Physik-Kanaele)
    kf = mc.comp(40, (-10, 7), {"count": 9, "offset": 3}, [("inc", (kleber_in, 0))] + [
        (rd(karte, ch, (-11, 7 - .5 * j)), 0) for j, ch in enumerate(range(9))])
    next(c for c in mc.comps if c[1] == kleber)[3].append((kf, 0))

    # --- KI_STATUS: Eingang von KI_FAHREN + dessen Ausgang (Zahl 26-32: Zustand, Zahl Wegpunkte, Soll-Tempo,
    #     aktueller Wegpunkt, Lenk- und Fahrbefehl roh, Tempo; Bool 7-9) -> Monitor 2x3 und Helm
    st = mc.comp(40, (1, -2), {"count": 7, "offset": 25}, [("inc", (w, 0))] + [
        (rd(fahren, ch, (-1, -1 - .5 * j)), 0) for j, ch in enumerate((2, 9, 27, 10, 28, 29, 31))])
    st = mc.comp(41, (1, -3), {"count": 3, "offset": 6}, [("inc", (st, 0))] + [
        (rd(fahren, ch, (-1, -4.5 - .5 * j), 29), 0) for j, ch in enumerate((0, 1, 2))])
    # Bool 13/14: Richtung links/rechts umgelernt (KI_FAHREN Bool 5/6) - Hinweis fuer Andre
    st = mc.comp(41, (1, -3.5), {"count": 2, "offset": 12}, [("inc", (st, 0))] + [
        (rd(fahren, ch, (-1, -6.5 - .5 * j), 29), 0) for j, ch in enumerate((4, 5))])
    status = mc.comp(56, (3, -2), {"script": src["ki_status"]}, [(st, 0)])
    # --- KI_LENKUNG (nur Lenk-Variante): Ausgang von KI_FAHREN + Tempo (Physik 13) auf Zahl 32
    lk = mc.comp(40, (1, -5), {"count": 1, "offset": 31}, [("inc", (fahren, 0)), (rd(phys, 12, (-1, -6)), 0)])
    lenkung = mc.comp(56, (3, -5), {"script": src["ki_lenkung"]}, [(lk, 0)])

    for j, (name, val, desc) in enumerate(eigen or props()):
        mc.comp(34, (-18 - 2 * (j // 12), 8 - (j % 12)), {"n": name}, extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))

    def aus(label, q, ch, ntype, desc, x, y, typ=31, fz=3):
        mc.node(label, 0, ntype, desc, x, fz, (8, y), (rd(q, ch, (5, y), typ), 0))

    aus("Links", fahren, 0, 1, "alle Elektromotoren der linken Raeder: Throttle", 0, 6)
    aus("Rechts", fahren, 1, 1, "alle Elektromotoren der rechten Raeder: Throttle", 1, 5)
    mc.node("Karte", 0, 6, "Monitor 3x3 links am Sitz: Video", 2, 3, (8, 4), (karte, 1))
    wahl = mc.comp(41, (5, 3), {"count": 1}, [(rd(kleber, 9, (3, 3), 29), 0)])
    mc.node("Wahl", 0, 5, "an den Bildschirm-Chip (Eingang 'Wahl'): Bool 1 Master Arm", 3, 3, (8, 3), (wahl, 0))
    mc.node("Zustand", 0, 5, "Ausgang der Fahr-KI (Zustand, Wegpunkte) - frei fuer Anzeigen", 4, 3, (8, 2), (fahren, 0))
    # Schutz-Chip (Auto-Chaff): Bool 3 'Auto-Chaff' = Waffen frei und ein Ziel da (Kleber Bool 12), Bool 4 'Pumpen' aus
    schutz = mc.comp(41, (5, 1), {"count": 1, "offset": 2}, [(rd(kleber, 11, (3, 1), 29), 0)])
    mc.node("Status", 0, 6, "Monitor 2x3 rechts am Sitz: Video (KI-Zustand, Tempo, Batterie, Laser)", 4, 2, (8, 0),
            (status, 1))
    aus("Lenkung vorn", lenkung, 0, 1, "Lenk-Variante: Robotic Pivots der vorderen Achsen: Rotation Target", 0, -6, fz=4)
    aus("Lenkung hinten", lenkung, 1, 1, "Lenk-Variante: Robotic Pivots der hinteren Achsen: Rotation Target", 1, -7, fz=4)
    aus("Immer an", kleber, 12, 0, "immer an: alle Laser Distance Sensors (Laser an) und Monitor 2x3 (Power Switch)", 4, -8,
        typ=29, fz=4)
    mc.node("Schutz", 0, 5, "an den Schutz-Chip (Eingang 'Instrumente'): Bool 3 Auto-Chaff = Waffen frei + Ziel", 3, 2, (8, 1),
            (schutz, 0))
    assert len(mc.desc) <= 128, len(mc.desc)
    return mc


if __name__ == "__main__":
    m = build()
    print(len(m.embedded()), "Zeichen;", [n[0] for n in m.node_liste()])
