"""Pruefstand fuer den ganzen KI-Chip (wie gebaut, mit chip_sim): stimmen die Kanaele zwischen KI_KLEBER, KI_FAHREN,
KI_KARTE, KI_STATUS und KI_LENKUNG? Einfaches Fahrzeug-Modell (Skid-Lenkung), Physik-Composite wie im Spiel.
Aufruf (mit lupa): python landkreuzer/tools/test_ki_chip.py
"""
import math
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import build_ki  # noqa: E402
from chip_sim import ChipSim  # noqa: E402


def lauf(sek, schalter=(False, False, False, False), tipp=None, sitz=None, ziel=None, batterie=0.0, laser=4000.0):
    """Panzer auf flachem Land (Hoehe 50 m), Kurs Nord. tipp = (Tick, Pixel x, y[, Ticks gehalten]) auf dem Kartenmonitor.
    -> Liste je Tick (Ort, Ausgaenge)"""
    sim = ChipSim(build_ki.build())
    x, z, hd, v = 0.0, 0.0, 0.0, 0.0                     # hd Kurs im Uhrzeigersinn (U)
    out, rl, rr = [], 0.0, 0.0
    for t in range(int(sek * 60)):
        # Fahrzeug: Antrieb links/rechts (Rad-Richtung: rechts -1 eingebaut -> wieder umdrehen)
        L, R = rl, -rr
        v += ((L + R) / 2 * 10 - v) * 0.02
        hd += (L - R) * 0.02 / 60
        x += v * math.sin(hd * 2 * math.pi) / 60
        z += v * math.cos(hd * 2 * math.pi) / 60
        phys = ({1: x, 2: 50.0, 3: z, 9: v, 13: abs(v), 15: 0.0, 16: 0.0, 17: -hd}, {})
        las = {n: laser for n in build_ki.LASER_NAMEN}
        las["Laser unten"] = 0.6 if laser else 0.0
        tn = {1: 96.0, 2: 96.0}
        tb = {}
        if tipp and tipp[0] <= t < tipp[0] + (tipp[3] if len(tipp) > 3 else 3):
            tn.update({3: float(tipp[1]), 4: float(tipp[2])})
            tb[1] = True
        sn, sb = {}, {}
        if sitz:
            sn.update({1: sitz[0], 2: sitz[1]})
            sb[32] = True
        bed_n, bed_b = {}, {}
        if ziel:
            bed_n.update({8: ziel[0] - x, 9: ziel[1] - z, 10: 52.0})
            bed_b[9] = True
        e = {"Physik-Sensor": phys, "Sitz": (sn, sb), "Instrumente": ({}, dict(enumerate(schalter, 1))),
             "Bedienung": (bed_n, bed_b), "Karte Touch": (tn, tb), "Batterie": batterie}
        e.update(las)
        a = sim.tick(e)
        rl, rr = a.get("Links") or 0.0, a.get("Rechts") or 0.0
        out.append(((x, z), a))
    return out


def main():
    rueck = []
    r = lauf(20)
    a9, a19 = r[9 * 60][1], r[-1][1]
    zustand = lambda a: (a.get("Zustand") or ({}, {}))[0].get(3, -1)
    rueck.append(("Start: 9 s steht (Zustand %d, Links %.2f), nach 20 s faehrt er (Zustand %d, %.0f m vom Start)" % (
        zustand(a9), a9.get("Links") or 0, zustand(a19), math.hypot(*r[-1][0])),
        abs(a9.get("Links") or 0) < 1e-6 and zustand(a19) in (2, 3, 9) and math.hypot(*r[-1][0]) > 5))
    w = r[-1][1].get("Wahl") or ({}, {})
    rueck.append(("Wahl an den Bildschirm: Master Arm erst nach 60 s (nach 20 s: %s)" % w[1].get(1), not w[1].get(1)))
    r = lauf(65)
    w = r[-1][1].get("Wahl") or ({}, {})
    s = r[-1][1].get("Schutz") or ({}, {})
    rueck.append(("nach 65 s ohne Gegner: Master Arm %s, Auto-Chaff %s (erst mit Ziel)" % (w[1].get(1), s[1].get(3)),
                  w[1].get(1) and not s[1].get(3)))
    r = lauf(65, ziel=(0.0, 3000.0))
    s = r[-1][1].get("Schutz") or ({}, {})
    rueck.append(("nach 65 s mit Ziel in 3 km: Auto-Chaff %s" % s[1].get(3), s[1].get(3)))
    r = lauf(65, schalter=(True, False, True, False))
    w = r[-1][1].get("Wahl") or ({}, {})
    rueck.append(("Schalter 'Waffen sperren' + 'KI Pause': kein Master Arm, steht (%.1f m)" % math.hypot(*r[-1][0]),
                  not w[1].get(1) and math.hypot(*r[-1][0]) < 0.5))
    # Karte: Tipp in die rechte obere Ecke der Karte -> Wegpunkt; die KI faehrt dorthin
    r = lauf(40, tipp=(700, 80, 20))
    z = r[-1][1].get("Zustand") or ({}, {})
    rueck.append(("Karten-Tipp: %d Wegpunkt(e) bei %.0f/%.0f, Zustand %d" % (z[0].get(10, 0), z[0].get(12, 0), z[0].get(13, 0),
                                                                          z[0].get(3, -1)), z[0].get(10, 0) >= 1))
    # Freund-Punkt: KI Pause, Finger 2 s auf der Karte (Pixel 80/20 = Ost 333 / Nord 292 m beim Zoom 1, wie beim
    # Karten-Tipp oben), dann ein Ziel der Kanonen genau dort -> kein Master Arm; ohne Freund-Punkt -> Master Arm
    r = lauf(66, schalter=(False, False, True, False), tipp=(700, 80, 20, 120), ziel=(333.3, 291.7))
    w1 = (r[-1][1].get("Wahl") or ({}, {}))[1].get(1)
    r = lauf(66, schalter=(False, False, True, False), ziel=(333.3, 291.7))
    w2 = (r[-1][1].get("Wahl") or ({}, {}))[1].get(1)
    rueck.append(("Freund-Punkt (Finger 2 s auf der Karte): Ziel dort -> Master Arm %s, ohne Freund-Punkt %s" % (w1, w2),
                  w1 is False and w2 is True))
    # Sitz: W gedrueckt (KI Pause) -> faehrt von Hand vorwaerts
    r = lauf(5, schalter=(True, False, True, False), sitz=(0.0, 1.0))
    rueck.append(("Selbst fahren (W): Links %.2f, Rechts %.2f, %.1f m gefahren" % (
        r[-1][1].get("Links") or 0, r[-1][1].get("Rechts") or 0, math.hypot(*r[-1][0])), math.hypot(*r[-1][0]) > 2))
    # Lenkung: A/D rechts -> Gelenke vorn +, hinten -
    r = lauf(3, schalter=(True, False, True, False), sitz=(1.0, 0.5))
    lv, lh = r[-1][1].get("Lenkung vorn") or 0, r[-1][1].get("Lenkung hinten") or 0
    rueck.append(("Lenkung (D): vorn %.3f, hinten %.3f" % (lv, lh), lv > 0.1 and lh < -0.1))
    # Laser melden 0 (nicht eingeschaltet / kein Strom): die KI faehrt nicht, Zustand 10 (LASER?)
    r = lauf(20, laser=0.0)
    rueck.append(("Laser melden 0: Zustand %d (10 = LASER?), %.1f m gefahren" % (zustand(r[-1][1]), math.hypot(*r[-1][0])),
                  zustand(r[-1][1]) == 10 and math.hypot(*r[-1][0]) < 0.5))
    r = lauf(1)
    la = (r[-1][1].get("Laser an"))
    rueck.append(("Ausgang 'Laser an' ist an (%s)" % la, la is True))
    # Ziel in 600 m: Kampf (Zustand 6)
    r = lauf(20, ziel=(0.0, 600.0))
    rueck.append(("Ziel der Kanonen 600 m voraus: Zustand %d (6 = Kampf)" % zustand(r[-1][1]), zustand(r[-1][1]) == 6))
    ok = True
    for t, g in rueck:
        print("%-90s %s" % (t, "ok" if g else "FEHLER"))
        ok &= bool(g)
    print("ALLES OK" if ok else "FEHLER")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
