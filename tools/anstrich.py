"""Anstrich der Figet Marena v2 (Andre 06./07.10.: "militaerisch, cool, professionell" - dann: "ueberall waren weisse
Teile; etwas schraffieren - sehr aehnliche Farben abwechselnd, damit es realistischer wirkt; bitte auch innen alles
anmalen; die meisten schraegen Teile aussen am Rumpf waren nicht bemalt").

Aussen (Marine-Schema), jedes Teil mit einer Seite an freier Aussenluft:
- unter Wasser Antifouling-Rot, an der Wasserlinie schwarzer Streifen (Boot-Top), Rumpf dunkles Marinegrau, Aufbauten
  helleres Grau, Decks/Daecher Dunkelgrau, Tuerme Dunkelgrau, Rohre/Kanonen Gun-Metal, Mastspitze schwarz,
  Rumpfnummer F07 weiss auf der hohen Bordwand achtern
- Schraffur: jede 'Platte' (6 x 4 x 8 Bloecke) bekommt einen eigenen, leicht anderen Ton, dazu feines Rauschen je Teil
Innen: Waende/Decken hellgrau, Boeden dunkelgrau, Technik (Bauteile) mittelgrau - auch leicht schraffiert.
'Aussenluft': freie Voxel, die auf einer Achse (x, y oder z) ausserhalb des aeussersten Teils liegen - so zaehlen
auch Schraegen an Kanten, und offene Tueren machen Innenraeume nicht zu 'aussen'.
Gestrichen werden alle Teile mit Flaechen (sc) im Rumpf und auf Tuermen/Gelenken/Chaff-Werfern, auch Bauteile.
v2.1 (Andre 07.10.: "alles, was ich selbst bemalt habe, ist viel schlechter - bemale es auch; auch Tueren, Knoepfe,
Fensterrahmen, Leitern, Gelaender"): alles wird gestrichen, auch Andres eigene Farben (die gruenen Kuehlleitungen
stehen im Backup 'vor Anstrich v2'). Nicht angefasst: Raketen-Koerper, Ausruestung, Schrauben.
Wasserlinie aus den Logs: in Ruhe liegt der Physik-Sensor (y 27, z -38) 7,45 m ueber dem Meer, Nick -2,3 Grad (Bug tief).
v2.2 (Andres Bild 07.10.: innen noch weisse Treppen-Rahmen und Tueren): Bauteile bekommen auch Haupt-/Zweit-/Drittfarbe
(bc, bc2, bc3) - Fenster nur bc (Rahmen), Lampen/Anzeigen/Bildschirme keine.
Probe: ausser den Farben (sc, bc, bc2, bc3) aendert sich nichts.
Aufruf: python anstrich.py [--schreiben]   (vorher sichern; danach Schiff neu laden, NICHT vorher speichern)
"""
import math
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402

ROT, SCHWARZ, RUMPF, AUFBAU, DECK, TURM, WEISS = "6E2A26", "1B1C1E", "5F686E", "7C858B", "3A3F43", "4D555A", "E6E6E6"
ROHR = "3A3F42"
I_WAND, I_BODEN, I_TECHNIK = "A3AAAF", "4E5458", "6F777C"
SENSOR_Y, SENSOR_Z, SENSOR_H, NICK = 27, -38, 7.45, -2.28
FORMEN = {"block", "01_block_weight", "02_wedge", "03_pyramid", "04_invpyramid", "05_wedge_2", "06_pyramid_2",
          "07_invpyramid_2", "08_wedge_4", "09_pyramid_4", "10_invpyramid_4", "11_pyramid_2x2", "12_pyramid_2x4",
          "13_pyramid_4x4", "14_invpyramid_2x2", "15_invpyramid_2x4", "16_invpyramid_4x4"}
RAKETE = ("solid_rocket", "warhead", "radar_advanced_missile")
LASSEN = ("inventory_", "giga_prop", "prop_")   # Ausruestung (Gewehre, Erste Hilfe ...) und Schrauben
OHNE_GRUND = ("light", "indicator", "monitor", "lamp")   # Grundfarben (bc) bleiben: Licht/Bild
KRAEFTIG = 60          # Farben mit mehr Abstand zwischen hellstem und dunkelstem Kanal sind Markierungen: bleiben
SCHRAFFUR, RAUSCHEN, INNEN_SCHRAFFUR = 0.06, 0.025, 0.03
FONT = {"F": ["111", "100", "110", "100", "100"], "0": ["111", "101", "101", "101", "111"],
        "7": ["111", "001", "010", "010", "010"]}
NUMMER, SKALA, Z_MITTE, Y_UNTEN = "F07", 2, -80, 4
MAST = 40
NACHBARN = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def wasserlinie(z):
    """Block-Hoehe y der Wasserlinie bei z (Schiff in Ruhe)."""
    p = math.radians(NICK)
    return SENSOR_Y - (SENSOR_H + 0.25 * (z - SENSOR_Z) * math.sin(p)) / (0.25 * math.cos(p))


def zufall(*k):
    """fester Pseudo-Zufall in [-1, 1] je Schluessel"""
    h = 2166136261
    for v in k:
        h = ((h ^ (v & 0xffffffff)) * 16777619) & 0xffffffff
    h ^= h >> 13
    h = (h * 0x5bd1e995) & 0xffffffff
    h ^= h >> 15
    return (h / 0xffffffff) * 2 - 1


def ton(farbe, p, staerke):
    """Farbe mit Schraffur: Platten-Ton + feines Rauschen"""
    x, y, z = p
    f = 1 + staerke * zufall(x // 6, y // 4, z // 8, 7) + RAUSCHEN * zufall(x, y, z, 11) * (staerke > 0)
    return "".join("%02X" % max(0, min(255, round(int(farbe[i:i + 2], 16) * f))) for i in (0, 2, 4))


ALT = {ROT, SCHWARZ, RUMPF, AUFBAU, DECK, TURM, WEISS}       # Farben des ersten Anstrichs (06.10.): neu streichen


def kraeftig(werte):
    if all(c in ALT for c in werte if c != "x"):
        return False
    for c in werte:
        if len(c) == 6 and c != "x":
            r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
            if max(r, g, b) - min(r, g, b) > KRAEFTIG:
                return True
    return False


def main():
    s0 = open(u.VEH, encoding="utf-8", newline="").read()
    i0, e0 = s0.index("<bodies>"), s0.index("</bodies>")
    koerper, a = [], s0.index("<body ", i0)
    while 0 <= a < e0:
        e = s0.index("</body>", a)
        koerper.append((a, e))
        a = s0.find("<body ", e)
    rumpf = max(range(len(koerper)), key=lambda k: s0.count('<c', *koerper[k]))
    teile, belegt = [], set()
    for k, (a, e) in enumerate(koerper):
        txt = s0[a:e]
        rakete = k != rumpf and any(n in txt for n in RAKETE)
        for m in re.finditer(r'<c(?: d="([^"]+)")?(?: t="\d+")?><o ([^>]*?)(/?)>', txt):
            d = m.group(1) or "block"
            if m.group(3):
                vp = (0, 0, 0)
            else:
                v = re.match(r"<vp([^/]*)/>", txt[m.end():])
                vp = u.xyz(v.group(1)) if v else (0, 0, 0)
            belegt.add(vp)
            if rakete or d.startswith(LASSEN):
                continue
            sc = re.search(r'sc="([^"]*)"', m.group(2))
            if not sc:
                continue
            werte = sc.group(1).split(",")
            if not werte[0].isdigit():
                continue
            teile.append((k, d, vp, a + m.start(2), a + m.end(2), int(werte[0])))
    # Aussenluft: auf einer Achse ausserhalb des aeussersten Teils
    linien = [defaultdict(lambda: [1e9, -1e9]) for _ in range(3)]
    for p in belegt:
        for ax in range(3):
            schl = tuple(p[i] for i in range(3) if i != ax)
            lo = linien[ax][schl]
            lo[0], lo[1] = min(lo[0], p[ax]), max(lo[1], p[ax])
    linien = [dict(lo) for lo in linien]

    def aussen(p):
        if p in belegt:
            return False
        for ax in range(3):
            lo = linien[ax].get(tuple(p[i] for i in range(3) if i != ax))
            if lo is None or p[ax] < lo[0] or p[ax] > lo[1]:
                return True
        return False

    farbe = {}
    zahl = defaultdict(int)
    for k, d, vp, a, e, n in teile:
        x, y, z = vp
        frei = [aussen((x + dx, y + dy, z + dz)) for dx, dy, dz in NACHBARN]
        turm = k != rumpf
        if any(frei):
            oben, unten, seite = frei[2], frei[3], frei[0] or frei[1] or frei[4] or frei[5]
            wl = wasserlinie(z)
            if y < wl - 1:
                f, art = ROT, "unter Wasser"
            elif not turm and y >= MAST:
                f, art = SCHWARZ, "Mastspitze"
            elif d.startswith("gun_"):
                f, art = ROHR, "Kanonen"
            elif oben and y >= wl + 1 and (not seite or y <= wl + 4) and d in FORMEN:
                f, art = DECK, "Deck"
            elif y <= wl + 2 and (seite or unten):
                f, art = SCHWARZ, "Boot-Top"
            elif oben and not seite and d in FORMEN:
                f, art = DECK, "Deck"
            elif turm:
                f, art = TURM, "Tuerme"
            elif y <= 5 or abs(x) >= 15:
                f, art = RUMPF, "Rumpf"
            else:
                f, art = AUFBAU, "Aufbauten"
            st = 0 if f == SCHWARZ else SCHRAFFUR
        else:
            if d.startswith("gun_"):
                f, art = ROHR, "Kanonen innen"
            elif d not in FORMEN:
                f, art = I_TECHNIK, "innen Technik"
            elif (x, y + 1, z) not in belegt:
                f, art = I_BODEN, "innen Boden"
            else:
                f, art = I_WAND, "innen Wand/Decke"
            st = INNEN_SCHRAFFUR
        farbe[(k, vp)] = ton(f, vp, st)
        zahl[art] += 1
    # Rumpfnummer auf der hohen Bordwand achtern (Steuerbord liest zum Bug, Backbord zum Heck)
    haut = {}
    for k, d, vp, a, e, n in teile:
        if k == rumpf and d in FORMEN:
            for seite in (1, -1):
                if vp[0] * seite >= 15 and aussen((vp[0] + seite, vp[1], vp[2])):
                    q = (seite, vp[1], vp[2])
                    if q not in haut or vp[0] * seite > haut[q][0] * seite:
                        haut[q] = vp
    breite = len(NUMMER) * 4 - 1
    gesetzt = 0
    for seite in (1, -1):
        for ci, ch in enumerate(NUMMER):
            for r, zeile in enumerate(FONT[ch]):
                for c, bit in enumerate(zeile):
                    if bit != "1":
                        continue
                    for dy in range(SKALA):
                        for dz in range(SKALA):
                            spalte = (ci * 4 + c) * SKALA + dz
                            z = Z_MITTE - breite * SKALA // 2 + (spalte if seite > 0 else breite * SKALA - 1 - spalte)
                            y = Y_UNTEN + (4 - r) * SKALA + dy
                            if (seite, y, z) in haut:
                                farbe[(rumpf, haut[(seite, y, z)])] = WEISS
                                gesetzt += 1
    # schreiben (ein Durchgang)
    stuecke, last = [], 0
    for k, d, vp, a, e, n in sorted(teile, key=lambda t: t[3]):
        f = farbe[(k, vp)]
        attr = re.sub(r'sc="[^"]*"', 'sc="%s"' % ",".join([str(n)] + [f] * n), s0[a:e], count=1)
        # v2.2: Bauteile haben dazu Haupt-/Zweit-/Drittfarbe (bc, bc2, bc3; fehlt sie, zeigt das Spiel Weiss - Treppen,
        # Tueren, Gelaender, Leitern). Fenster: nur der Rahmen (bc2 = Glas); Lampen, Anzeigen, Bildschirme: nichts
        if not d.startswith(OHNE_GRUND):
            for name in (("bc",) if d.startswith("window") else ("bc", "bc2", "bc3")):
                if re.search(r'(^| )%s="[^"]*"' % name, attr):
                    attr = re.sub(r'(^| )%s="[^"]*"' % name, lambda m_: '%s%s="%s"' % (m_.group(1), name, f), attr, count=1)
                elif d not in FORMEN:            # Bloecke: nur vorhandene Grundfarben ersetzen
                    attr += ' %s="%s"' % (name, f)
        stuecke.append(s0[last:a])
        stuecke.append(attr)
        last = e
    stuecke.append(s0[last:])
    s = "".join(stuecke)
    for art, n in sorted(zahl.items(), key=lambda x: -x[1]):
        print("  %-18s %6d Teile" % (art, n))
    print("Rumpfnummer %s: %d Bloecke" % (NUMMER, gesetzt))

    def ohne(x):
        x = re.sub(r' bc[23]?="[^"]*"', "", x)
        return re.sub(r'sc="(\d+)(?:,[0-9A-Fx]+)*"', r'sc="\1"', x)
    assert ohne(s0) == ohne(s), "ausser Farben geaendert"
    print("Probe: nur Farben geaendert, %d Teile gestrichen" % len(teile))
    ziel = u.VEH if "--schreiben" in sys.argv else os.path.join(os.environ.get("TEMP", "."), "schiff_probe.xml")
    with open(ziel, "w", encoding="utf-8", newline="") as f:
        f.write(s)
    print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
