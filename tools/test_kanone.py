"""Pruefstand fuer die Anti-Schiffs-Kanonen vorn (Chips 'Figet Marena Kanone BC/AC', Skripte FLAKRADAR + FLAK wie die
Flak) - der Flak-Pruefstand (test_flak.lauf) mit Schiffszielen: Einschlag auf dem Wasser zaehlt (waagerechter Abstand
zum Ziel), Sperrprofil des Turms, Turm-Radar mit Strahl 0,05 und bis 9 km, Battle Cannon mit Lade-Ablauf.
Treffer: beim Vorbeiflug am Ziel hoechstens 5 m seitlich und 2,5 m ueber/unter dem Zielpunkt (Rumpf)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_kanone  # noqa: E402
import sperrprofil  # noqa: E402
from test_flak import lauf, kamera  # noqa: E402
from test_schiff import pruefe  # noqa: E402

KP = None


def kanone(k):
    """Eigenschaften und Sperrprofil der Kanone k ('B' / 'A')."""
    global KP
    KP = KP or sperrprofil.koerper()
    _, _, _, cx, cz, gy, _, _, _ = next(q for q in build_kanone.KANONEN if q[0] == k)
    pr = {n: v for n, v, _ in build_kanone.props(k)}
    pr["Schreiber Port"], pr["Schreiber Zeichen"] = 0, 3000
    # Der Pruefstand bildet Drehkranz, Pivots und Radar mit Richtung +1 nach (wie Flak-Pruefstand); die echten
    # Richtungen der Tuerme (aus den Teilen abgeleitet) stehen in build_kanone und werden im Spiel mit 'Test Rohre' geprueft
    for n in ("AA Turm Richtung", "AA Hoehe Richtung links", "AA Hoehe Richtung rechts", "AA Radar Richtung",
              "AA Radar Hoehe Richtung"):
        pr[n] = 1
    # Pruefstand: Physik-Sensor = Turm-Radar (kein Versatz), Schiffe 2 m hoch
    pr["Radar ueber Physik m"], pr["Radar vor Physik m"], pr["Ziel Hoehe fest m"] = 0, 0, 2.0
    return pr, sperrprofil.profil(cx, cz, gy, KP)


def schiff(k, r, brg, v=(0.0, 0.0), secs=40, own=(0.0, 5.0, 0.0), roll=2.0, nick=1.0, **kw):
    """Schiff in r m, Richtung brg Grad ab Bug (Kurs 0), 2 m hoch, Welt-Tempo v; wir 8 m hoch."""
    pr, pf = kanone(k)
    pr.update(kw.pop("props", {}))
    b = math.radians(brg)
    return lauf((r * math.sin(b), r * math.cos(b), -6.0), (v[0], v[1], 0.0), secs=secs, own=(own[0], own[1], 0.0),
                roll=roll, nick=nick, fov=(0.05, 0.05), props=pr, prf=pf, see=True, rmax=kw.pop("rmax", 9000),
                vfehler=(15.0, -10.0, 1.0), **kw)


def test_kanone():
    rueck = []
    t = lambda r: "%d Schuss, %d Treffer (Rumpf), Einschlaege %d/%d naeher 8 m" % (r["schuss"], r["treffer"], r["nah"], r["bursts"])
    # Battle Cannon
    r = schiff("B", 1500, 40, v=(-6.0, 4.0))
    rueck.append(("BC (2 Rohre): Schiff 1,5 km rechts voraus, faehrt quer: " + t(r) + ", links %d / rechts %d, alle %.1f s ein Schuss"
                  % (r["je"].get("L", 0), r["je"].get("R", 0), r["abst"] / 60),
                  r["schuss"] >= 10 and r["treffer"] >= r["schuss"] * 0.6 and abs(r["je"].get("L", 0) - r["je"].get("R", 0)) <= 2))
    # Auto-Zoom (v2.6): Schiff 1,5 km faehrt quer - ab 10 s im Bild, fuellt etwa 'Kamera Bildanteil' (0,4) der Breite
    for kk, rr, brg, vv in (("B", 1500, 40, (-6.0, 4.0)), ("A", 1200, -30, (6.0, 6.0)), ("B", 4500, -20, (5.0, 3.0))):
        r = schiff(kk, rr, brg, v=vv, secs=25)
        dr, fvm, tm = kamera(r, 10, 40)
        rueck.append(("Auto-Zoom %s, Schiff %.1f km: im Bild %.0f %%, Bildwinkel Median %.3f rad, Ziel fuellt %.0f %% der Breite" % (
            "BC" if kk == "B" else "AC", rr / 1000, dr * 100, fvm, tm * 100), dr >= 0.95 and 0.2 <= tm <= 0.45))
    # Andres Test 04.10. ~14:25: bei schneller Fahrt zielten BC und AC daneben (Turm-Radar v2.2 deckelte das Relativ-Tempo
    # auf 20 m/s - Pruefstand: 0 Treffer bei 36 m/s eigener Fahrt). Ab v2.3 laufen die Spuren in der Welt
    for kk in ("B", "A"):
        for own, brg, vv in (((0.0, 36.0), 40, (-6.0, 4.0)), ((0.0, 36.0), -60, (5.0, -3.0)), ((25.0, 25.0), 20, (0.0, 8.0))):
            r = schiff(kk, 1500, brg, v=vv, own=own, secs=30)
            rueck.append(("%s bei schneller Fahrt (%.0f m/s), Schiff 1,5 km/%d Grad: " % ("BC" if kk == "B" else "AC",
                          (own[0] ** 2 + own[1] ** 2) ** .5, brg) + t(r), r["schuss"] >= 10 and r["treffer"] >= r["schuss"] * 0.4))
    # Korrektur per Blick (Flak v2.8): 0,002 U nach rechts verschiebt die Einschlaege um ~19 m quer zur Schussrichtung
    import statistics
    quer = {}
    for kx in (0.0, 0.002):
        r = schiff("B", 1500, 40, v=(-6.0, 4.0), secs=30, korr=(kx, 0.0))
        b = math.radians(40)
        quer[kx] = statistics.median(dx * math.cos(b) - dy * math.sin(b) for dx, dy, *_ in r["einschlag"][3:])
    rueck.append(("Korrektur 0,002 U rechts: Einschlaege quer %.1f m -> %.1f m (soll +%.0f m)" % (
        quer[0.0], quer[0.002], 1500 * 2 * math.pi * 0.002), 14 <= quer[0.002] - quer[0.0] <= 24))
    r = schiff("B", 1500, 40, v=(-6.0, 4.0), weiche=-1)
    rueck.append(("BC: Weiche andersherum (lernt der Chip): " + t(r) + ", links %d / rechts %d" % (r["je"].get("L", 0), r["je"].get("R", 0)),
                  r["schuss"] >= 6 and r["je"].get("L", 0) > 0 and r["je"].get("R", 0) > 0))
    r1 = schiff("B", 1500, 40, secs=20, props={"Rohre": 1})
    rueck.append(("BC mit 'Rohre' 1: nur das linke Rohr schiesst (%s)" % r1["je"], r1["je"].get("R", 0) == 0 and r1["je"].get("L", 0) >= 3))
    r = schiff("B", 3000, 20, v=(-6.0, 4.0))
    rueck.append(("BC: Schiff 3 km voraus-rechts, faehrt quer: " + t(r), r["schuss"] >= 6 and r["treffer"] >= r["schuss"] * 0.5))
    r = schiff("B", 4500, -20, v=(5.0, 3.0), secs=50)
    rueck.append(("BC: Schiff 4,5 km links voraus: " + t(r), r["schuss"] >= 6 and r["treffer"] >= r["schuss"] * 0.4))
    r = schiff("B", 5500, -40, v=(5.0, 3.0), secs=40)
    rueck.append(("BC: Schiff 5,5 km (mit 800 m/s / Drag 0,002 kaum erreichbar): nur Schuesse mit Bahnloesung - " + t(r),
                  r["treffer"] >= r["schuss"] * 0.3))
    r = schiff("B", 7500, 10, secs=25)
    rueck.append(("BC: Schiff 7,5 km (ueber 'AA Reichweite m' 6000): kein Schuss (%d)" % r["schuss"], r["schuss"] == 0))
    r = schiff("B", 1500, 90, secs=12, rmax=10)
    rueck.append(("BC: Radar sieht das Ziel nicht (90 Grad rechts) - der Turm dreht trotzdem zur Vorgabe (Turm %.0f Grad)" % (
        r["turm"] * 360), abs(r["turm"] * 360 - 90) < 10 and r["schuss"] == 0))
    r = schiff("B", 1500, 180, secs=25)
    rueck.append(("BC: Schiff genau achteraus (Bruecke/Mast im Weg): kein Schuss ins Schiff (%d Schuss, %d gesperrt)" % (
        r["schuss"], r["gesperrt"]), r["gesperrt"] == 0))
    # Heavy Autocannon vorn
    r = schiff("A", 1200, -30, v=(6.0, 6.0), secs=30)
    rueck.append(("AC: Schiff 1,2 km links voraus: " + t(r), r["schuss"] >= 20 and r["treffer"] >= r["schuss"] * 0.4))
    r = schiff("A", 1900, 30, v=(5.0, -5.0), secs=30)
    rueck.append(("AC: Schiff 1,9 km rechts voraus: " + t(r), r["schuss"] >= 20 and r["treffer"] >= r["schuss"] * 0.35))
    r = schiff("A", 400, 60, v=(0.0, 8.0), secs=20)
    rueck.append(("AC: Schiff 400 m rechts: " + t(r), r["schuss"] >= 10 and r["treffer"] >= r["schuss"] * 0.4))
    r = schiff("A", 2600, 0, secs=20)
    rueck.append(("AC: Schiff 2,6 km (ueber 'AA Reichweite m' 2000): kein Schuss (%d)" % r["schuss"], r["schuss"] == 0))
    r = schiff("A", 800, 180, secs=20)
    rueck.append(("AC: Schiff achteraus (BC-Turm im Weg): kein Schuss ins Schiff (%d Schuss, %d gesperrt)" % (
        r["schuss"], r["gesperrt"]), r["gesperrt"] == 0))
    r = schiff("A", 1200, -30, v=(6.0, 6.0), secs=20, frei=False)
    rueck.append(("AC ohne Feuer frei: kein Schuss (%d)" % r["schuss"], r["schuss"] == 0))
    # Andres Test 04.10. im Hafen: Turm-Radar meldete oft 6 Dinge (Ziel 650-750 m, andere bei 900 m und 6,3 km) -> 16 Spuren
    # voll, die gehaltene Spur wurde verdraengt und fror ein. Nachgestellt: 32 Dinge bei 0,9-1,1 km und 6,3-6,5 km im Strahl
    # (mit dem alten Radar-Skript: AC 0 Schuss)
    gewimmel = []
    for r_ in (900, 1100, 6300, 6500):
        for db in (-8, -6, -4, -2, 2, 4, 6, 8):
            bb = math.radians(27 + db)
            gewimmel.append(((r_ * math.sin(bb), r_ * math.cos(bb), -6.0), (0.0, 0.0, 0.0)))
    for kk in ("A", "B"):
        r = schiff(kk, 750, 27, v=(-4.0, -5.0), secs=30, ziele=gewimmel)
        rueck.append(("%s im Hafen (32 Dinge im Strahl, Spuren voll): " % ("BC" if kk == "B" else "AC") + t(r),
                      r["schuss"] >= (6 if kk == "B" else 20) and r["treffer"] >= r["schuss"] * 0.4))
    # Lader v2.5 (Andres Log 04.10.: 11 Schuss in 51 s, ein Rohr 295 Ticks, beide nacheinander): mit den Meldern der
    # Zufuehrungen laden beide Rohre gleichzeitig, geschossen wird abwechselnd mit gleichem Abstand. Unbekannte Zeiten
    # des Spiels (Verschluss auf, Zufuehrung -> Rohr, Weiche, Magazin) in drei Annahmen; ohne Melder wie bisher
    for name, bc, w, mel, mind in (("Standard-Zeiten", None, 1, True, 25), ("langsamer Nachschub", {"auf": 79, "rein": 30, "weiche": 40, "nach": 120}, 1, True, 12),
                                   ("langsam, Weiche verkehrt", {"auf": 79, "rein": 30, "weiche": 40, "nach": 120}, -1, True, 12),
                                   ("Granate braucht 25 Ticks zum Sitzen (Nachlauf lernen)", {"sitz": 25}, 1, True, 15),
                                   ("ohne Melder (alter Ablauf)", None, 1, False, 6)):
        r = schiff("B", 1500, 40, v=(-6.0, 4.0), bc=bc, weiche=w, melder=mel)
        l_, r_ = r["je"].get("L", 0), r["je"].get("R", 0)
        rueck.append(("BC-Lader %s: %d Schuss (links %d / rechts %d), Abstand Median %d Ticks, %d Treffer" % (
            name, r["schuss"], l_, r_, r["abst"], r["treffer"]),
            r["schuss"] >= mind and abs(l_ - r_) <= 2 and r["abst"] >= 20 and r["treffer"] >= r["schuss"] * 0.6))
    r = schiff("B", 2000, 30, secs=20, frei=False, einzel=(300,))
    rueck.append(("BC Einzelschuss ohne Feuer frei: genau ein Schuss (%d)" % r["schuss"], r["schuss"] == 1))
    return pruefe(rueck)


def main():
    ok = test_kanone()
    print("ALLES OK" if ok else "FEHLER")


if __name__ == "__main__":
    main()
