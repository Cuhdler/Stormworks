"""Baut die beiden Flak-Chips der Figet Marena ("Figet Marena Flak L" und "... R", je 4 x 5): FLAKRADAR (Spuren,
Zielwahl, Turm-Radar) + FLAK (Feuerleitung, Zeitzuender) fuer einen Flak-Turm hinten (Turret Ring Medium, 2 Heavy
Autocannons auf eigenen Robotic Pivots, Radar (Basic) auf dem Turm).
Das Sperrprofil (tools/sperrprofil.py) wird je Turm aus dem Fahrzeug berechnet und ins FLAK-Skript eingesetzt.

- mit --install zusaetzlich nach %APPDATA%/Stormworks/data/microprocessors kopieren
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import MC, minify, fmt, LUA_LIMIT, LUA_DIR, BUILD  # noqa: E402
from build_lage import schreiber_props, kopf  # noqa: E402
import sperrprofil  # noqa: E402

VERSION = "v2.8"
# Turm: Name, Drehmitte (x, z), Hoehe der Rohr-Drehachse (y)
TUERME = [("L", -10, -105, 18), ("R", 10, -105, 18)]
# v1.3: Vorgabe vom Bildschirm-Chip (Ausgang 'Bedienung', am Anschluss 'Lage'): Waffe 3 = Flak L, 4 = Flak R ->
# Zahl 4+4w..6+4w Ost/Nord/Hoehe (0-basiert 3+4w..5+4w), Bool 4+w Feuer frei, 8+w Vorgabe da (0-basiert 3+w, 7+w)
WAFFE = {"L": 3, "R": 4}

PROPS = [
    ("AA Turm Richtung", 1, "1 oder -1: Drehkranz dreht vom Ziel weg statt hin"),
    ("AA Turm Tempo", 10, "Wie kraeftig der Drehkranz Zielfehler ausgleicht (Swifter-Wert)"),
    ("AA Turm Bremsen", 0.3, "Wie schnell der Drehkranz abbremsen kann (U/s pro s); pendelt er ueber das Ziel: kleiner"),
    ("AA Hoehe Richtung links", 1, "1 oder -1: linkes Rohr geht falsch herum hoch/runter (mit 'Test Rohre' pruefen)"),
    ("AA Hoehe Richtung rechts", 1, "1 oder -1: rechtes Rohr geht falsch herum hoch/runter (mit 'Test Rohre' pruefen)"),
    ("AA Turm Null Grad", 0, "Wohin die Rohre bei Turmdrehung 0 zeigen (0 = nach vorn)"),
    ("AA Radar Richtung", 1, "1 oder -1: Seitenwinkel vom Radar falsch herum"),
    ("AA Radar Hoehe Richtung", 1, "1 oder -1: Hoehenwinkel vom Radar falsch herum"),
    ("AA Radar auf Turm", 1, "1 = das Radar sitzt auf dem Flak-Turm und dreht mit"),
    ("AA Radar Null Grad", 0, "Wohin die Vorderseite des Radars zeigt (0 = wie die Rohre)"),
    ("AA Mindesthoehe m", 15, "Nur Ziele, die so hoch ueber dem Meer sind (keine Schiffe) - auch wenn die Lagezentrale anderes vorgibt"),
    ("AA Suchtempo", 0.25, "So schnell kreist der Radarstrahl beim Suchen (Umdrehungen pro Sekunde)"),
    ("AA Suchhoehe Grad", 3, "Hoehe des Strahls in der ersten Suchrunde"),
    ("AA Suchstufe Grad", 6, "So viel hoeher schaut jede weitere Suchrunde (etwa die Strahlbreite)"),
    ("AA Suchstufen", 4, "So viele Suchrunden mit verschiedener Hoehe, dann wieder von unten"),
    ("AA Reichweite m", 1800, "Bis zu dieser Entfernung schiesst die Flak (Heavy Autocannon: Geschosse fliegen 10 s, ca. 2,8 km)"),
    ("Kompass Richtung", -1, "-1: der Kompass des Physik-Sensors zaehlt gegen den Uhrzeigersinn (wie beim Heli/Swifter)"),
    ("AA v0", 900, "Muendungsgeschwindigkeit Heavy Autocannon m/s"),
    ("AA Drag", 0.005, "Luftwiderstand pro Tick Heavy Autocannon"),
    ("Geschoss g", 30, "Schwerkraft fuer Geschosse im Spiel (m/s2, Swifter-Wert)"),
    ("AA Toleranz Grad", 1, "Feuert nur, wenn so genau ausgerichtet"),
    ("AA Toleranz m", 3, "Nahe Ziele: feuert schon, wenn sie am Ziel hoechstens so viele Meter daneben zeigt"),
    ("AA tiefster Winkel Grad", 3, "Rohre nie flacher als das (dazu das Sperrprofil aus dem Schiff)"),
    ("AA Radar ueber Rohr m", 0.75, "So viele Meter sitzt das Radar ueber den Rohren"),
    ("AA Streuung m", 3, "Streumuster: groesster Abstand der Spiralen vom Ziel, am Ziel gemessen (0 = genau)"),
    ("AA Zuender", 1, "1 = Zeitzuender auf die Flugzeit (Fragmentation platzt am Ziel), 0 = Aufschlag"),
    ("AA Zuender Zugabe s", 0, "So viel spaeter zuenden (+) bzw. frueher (-); v2.0: schon auf den Tick nach dem Zielpunkt gerundet"),
    ("AA Takt Ticks", 38, "v2.0: Rohre abwechselnd - so viele Ticks laedt ein Rohr nach (gemessen 38); je Haelfte darf ein Rohr"),
    ("Lader Zeit s", 0, "v2.1: 0 = Autocannon (Zufuehrung immer an); > 0 = Battle Cannon: so lange Verschluss offen je Ladeversuch"),
    ("Lader Nachlauf Ticks", 10, "v2.5 Battle Cannon mit Meldern: so lange bleibt der Verschluss offen, nachdem die Zufuehrung ihre Granate abgab (+5 je Fehlversuch)"),
    ("Rohre", 2, "v2.3 Battle Cannon: 2 = zwei Rohre an einem Magazin mit Weiche (abwechselnd laden und schiessen), 1 = eins"),
    ("Ziel Tempo max m/s", 400, "v2.4 Flak-Radar: schneller ist keine Spur (Kanonen 20 m/s - gegen Fantasie-Tempo im Hafen)"),
    ("Spur Alpha", 0.1, "v2.0 Flak-Radar: wie stark eine neue Ortung den Ort der Spur verschiebt (kleiner = ruhiger)"),
    ("Spur Beta", 0.005, "v2.0 Flak-Radar: wie stark sie das Tempo der Spur aendert (kleiner = ruhiger, folgt langsamer)"),
    ("Ziel Hoehe fest m", -999, "v2.2: Schiffsziele - so hoch ueber dem Meer zielen statt der Radar-Hoehe (-999 = aus, Flak)"),
    ("Radar ueber Physik m", 0, "v2.2: so viele Meter sitzt das Turm-Radar hoeher als der Physik-Sensor (nur fuer 'Ziel Hoehe fest m')"),
    ("Radar vor Physik m", 0, "v2.2: so viele Meter sitzt das Turm-Radar weiter vorn als der Physik-Sensor (Nicken hebt es an)"),
    ("Test Rohre", 0, "1 = Flak aus, Turm nach vorn, beide Rohre und die Kamera 20 Grad hoch (Richtungen pruefen); 2 = dazu Turm 90 Grad nach rechts; danach wieder 0"),
    ("Kamera Hoehe Richtung", 1, "1 oder -1: die Kamera auf dem Turm neigt sich falsch herum (mit 'Test Rohre' pruefen)"),
    ("Kamera Zielgroesse m", 20, "v2.6 Auto-Zoom: so gross ist ein Ziel etwa (Flugzeug 20, Schiff 40)"),
    ("Kamera Bildanteil", 0.4, "v2.6 Auto-Zoom: so viel der Bildbreite fuellt das Ziel (kleiner = weiter weg gezoomt)"),
    ("Kamera FOV ohne Ziel rad", 1.0, "v2.6 Auto-Zoom: Bildwinkel ohne Ziel"),
    ("Kamera FOV weit rad", 2.2, "Camera Medium: Bildwinkel bei Zoom-Eingang 0"),
    ("Kamera FOV eng rad", 0.025, "Camera Medium: Bildwinkel bei Zoom-Eingang 1"),
    ("Kamera Null Grad", 0, "Korrektur, falls die Kamera bei Pivot 0 nicht waagerecht schaut"),
]


def build(radar_src, flak_src, seite, src, titel=None, beschr=None, waffe=None, props=None, turm="Flak-Turm",
          gname="Heavy Autocannon", rechts=True, verschluss=False, zwilling=False):
    """Chip bauen; die Kanonen vorn (build_kanone) nutzen dieselbe Schaltung mit eigenem Namen, Waffe im Bildschirm,
    Eigenschaften, ohne zweites Rohr ('rechts') und mit Verschluss (Battle Cannon)."""
    waffe = waffe or WAFFE[seite]
    mc = MC(titel or "Figet Marena Flak %s" % seite,
            beschr or ("Flak %s %s: Ziel und Feuer frei von der Lagezentrale, Turm-Radar verfolgt, Vorhalt, Zeitzuender, Schreiber"
                       % (seite, VERSION)), 4, 7 if zwilling else 5)
    # Eingaenge: Reihe 0 und 1
    mc.node("Sitz", 1, 5, "Steuersitz: Seat data (seit v1.3 nicht mehr gebraucht)", 0, 0, (-10, 7))
    phys = mc.node("Physik-Sensor", 1, 5, "Physics Sensor (Composite, derselbe wie am Schiffs-Chip)", 1, 0, (-10, 6))
    radar = mc.node("Radar", 1, 5, "Radar auf dem %s: Radar Data (manueller Modus)" % turm, 2, 0, (-10, 5))
    rdreh = mc.node("Radar Drehung", 1, 1, "Radar auf dem %s: Radar Rotation" % turm, 3, 0, (-10, 4))
    tdreh = mc.node("Turm Drehung", 1, 1, "Turret Ring des %ss: Current Rotation" % turm, 0, 1, (-10, 3))
    gel = mc.node("Geladen", 1, 0, "%s%s: Loaded - Schusszaehler" % (gname, " (linkes Rohr)" if rechts else ""), 1, 1,
                  (-10, 2))
    lage = mc.node("Lage", 1, 5, "Bildschirm-Chip: Ausgang 'Bedienung' (Ziel-Vorgabe, Feuer frei, Einzelschuss)", 2, 1,
                   (-10, 1))

    def rd(src, ch, pos, typ=31):
        return mc.comp(typ, pos, {"i": ch} if ch else {}, [(src, 0)])

    # Radar-Composite: Kanaele 4, 8 .. 32 ('Zeit seit Meldung' der Ziele) mit Turm, Physik x, Kompass, Nick, Roll,
    # Hoehe, Radar-Drehung, Physik z ueberschreiben
    werte = [(tdreh, 0), (rd(phys, 0, (-7, 7)), 0), (rd(phys, 16, (-7, 6)), 0), (rd(phys, 14, (-7, 5)), 0),
             (rd(phys, 15, (-7, 4)), 0), (rd(phys, 1, (-7, 3)), 0), (rdreh, 0), (rd(phys, 2, (-7, 2)), 0)]
    w = (radar, 0)
    for k, quelle in enumerate(werte):
        w = (mc.comp(40, (-5 + k * 0.5, 6 - (k % 2) * 0.5), {"count": 1, "offset": 3 + 4 * k}, [("inc", w), quelle]), 0)
    w0 = 4 * waffe + 3
    vg = [rd(lage, w0 + j, (-7, -1 - 0.5 * j)) for j in range(3)]
    w = (mc.comp(40, (-4.5, 3.5), {"count": 3, "offset": 28}, [("inc", w)] + [(c, 0) for c in vg]), 0)
    # v1.4: Zielnummer (Bedienung 3+4w) auf Kanal 25 (Hardlock)
    w = (mc.comp(40, (-4.5, 2.5), {"count": 1, "offset": 24}, [("inc", w), (rd(lage, w0 - 1, (-7, -2.5)), 0)]), 0)
    frei, da = rd(lage, 3 + waffe, (-7, -3), 29), rd(lage, 7 + waffe, (-7, -3.5), 29)
    # v1.9: Einzelschuss (Bedienung Bool 12+w, Leertaste) auf Bool 12
    einzel = rd(lage, 11 + waffe, (-7, -4), 29)
    wb = mc.comp(41, (-4, 3), {"count": 3, "offset": 9}, [("inc", w), (da, 0), (frei, 0), (einzel, 0)])
    fr = mc.comp(56, (-2, 4), {"script": radar_src}, [(wb, 0)])
    # FLAK: FLAKRADAR-Ausgang + Loaded (Bool 3)
    fw = mc.comp(41, (-1, 1), {"count": 1, "offset": 2}, [("inc", (fr, 0)), (gel, 0)])
    if zwilling:
        # v2.3: 'Loaded' des rechten Rohrs auf Bool 5
        gelr = mc.node("Geladen rechts", 1, 0, "%s (rechtes Rohr): Loaded" % gname, 1, 5, (-10, 0))
        fw = mc.comp(41, (-1, 0.5), {"count": 1, "offset": 4}, [("inc", (fw, 0)), (gelr, 0)])
        # v2.5: 'Contains Ammo' der Zufuehrungen auf Bool 6/7 (neue Anschluesse, die alten behalten ihre Kabel)
        muL = mc.node("Munition links", 1, 0, "Battle Cannon Belt (Feeder) links: Contains Ammo (Lade-Ablauf)", 2, 5,
                      (-10, -1), late=True)
        muR = mc.node("Munition rechts", 1, 0, "Battle Cannon Belt (Feeder) rechts: Contains Ammo", 3, 5, (-10, -2), late=True)
        fw = mc.comp(41, (-1, 0), {"count": 2, "offset": 5}, [("inc", (fw, 0)), (muL, 0), (muR, 0)])
    # v2.8: Korrektur vom Kamera-Chip (Zahl 2+2w seitlich, 3+2w Hoehe, U) -> Zahl 27/28 der Feuerleitung
    korr = mc.node("Korrektur", 1, 5, "Kamera-Chip: Ausgang 'Korrektur' (Zielpunkt-Korrektur per Blick)",
                   1 if zwilling else 3, 6 if zwilling else 4, (-10, -3), late=True)
    fw = mc.comp(40, (-1, -0.5), {"count": 2, "offset": 26}, [("inc", (fw, 0)), (rd(korr, 1 + 2 * waffe, (-3, -1)), 0),
                                                              (rd(korr, 2 + 2 * waffe, (-3, -1.5)), 0)])
    fl = mc.comp(56, (1, 2), {"script": flak_src}, [(fw, 0)])
    for k, (name, val, desc) in enumerate(props or PROPS):
        mc.comp(34, (-12 - 2 * (k // 10), 8 - (k % 10)), {"n": name},
                extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))
    # v1.8: Schreiber v2 steckt in FLAKRADAR und FLAK selbst (fXr, fXf); hier nur die Eigenschaften
    schreiber_props(mc, -20, 8)

    def aus(label, ch, ntype, desc, x, z, y, typ=31):
        mc.node(label, 0, ntype, desc, x, z, (7, y), (rd(fl, ch, (4, y), typ), 0))

    # Ausgaenge: Reihe 1 (rechts) bis 4
    aus("Turm Tempo", 0, 1, "Turret Ring des %ss: Rotational Speed" % turm, 3, 1, 7)
    zwei = "linken Rohr" if rechts else "Rohr (links)"
    aus("Hoehe Rohr links", 1, 1, "Robotic Pivot links am %s: Rotation Target" % zwei, 0, 2, 6)
    aus("Hoehe Rohr rechts", 2, 1, "Robotic Pivot rechts am %s: Rotation Target" % ("rechten Rohr" if rechts else "Rohr"), 1, 2, 5)
    aus("Zuender", 3, 1, "%s: Fuse Timer (s)" % ("beide Heavy Autocannons" if rechts else gname), 2, 2, 4)
    aus("Feuer", 0, 0, "linke Heavy Autocannon: Trigger (v2.0: abwechselnd mit 'Feuer rechts')" if rechts else
        "%s: Trigger" % gname, 3, 2, 3, typ=29)
    aus("Zufuehrung", 2, 0, "Autocannon Belt (Feeder) beider Rohre: Feed" if rechts else "Belt (Feeder) der %s: Feed" % gname,
        0, 3, 2, typ=29)
    aus("Radar an", 1, 0, "Radar auf dem %s: Activate" % turm, 1, 3, 1, typ=29)
    mc.node("Radar Gimbal", 0, 5, "Radar auf dem %s: Gimbal Input" % turm, 2, 3, (7, 0), (fr, 0))
    aus("Kamera Hoehe", 4, 1, "Compact Robotic Pivot unter der Kamera des %ss: Rotation Target" % turm, 3, 3, -1)
    # v2.6: Auto-Zoom an 'Field of View' der Turm-Kamera (neuer Anschluss am Ende; BC-Chip dafuer 4 x 7)
    mc.node("Kamera Zoom", 0, 1, "Camera Medium des %ss: Field of View (Auto-Zoom nach Entfernung)" % turm,
            0 if zwilling else 2, 6 if zwilling else 4, (7, -7), (rd(fl, 18, (4, -7)), 0), late=True)
    mc.node("Flak Daten" if rechts else "Daten", 0, 5, "Zustand fuer die Anzeige (Ziel-Entfernung, Zustand, Schuesse ...)",
            0, 4, (7, -2), (fl, 0))
    if rechts:
        # v2.0: rechtes Rohr eigener Abzug (abwechselnd) - neuer Anschluss am Ende, die alten behalten ihre Kabel
        mc.node("Feuer rechts", 0, 0, "%s (rechtes Rohr): Trigger (abwechselnd mit 'Feuer')" % gname, 1, 4, (7, -3),
                (rd(fl, 4, (4, -3), 29), 0), late=True)
    if verschluss:
        mc.node("Verschluss", 0, 0, "%s%s: Open Breech (Lade-Ablauf)" % (gname, " (linkes Rohr)" if zwilling else ""),
                2 if zwilling else 1, 4, (7, -4), (rd(fl, 5, (4, -4), 29), 0))
    if zwilling:
        mc.node("Verschluss rechts", 0, 0, "%s (rechtes Rohr): Open Breech" % gname, 3, 4, (7, -5), (rd(fl, 7, (4, -5), 29), 0))
        mc.node("Weiche", 0, 0, "Belt Junction zwischen den Rohren: Junction Switch (Seite lernt der Chip)", 0, 5, (7, -6),
                (rd(fl, 6, (4, -6), 29), 0))
    # neue Anschluesse in der Reihenfolge, in der sie dazukamen (die alten behalten ihre Kabel)
    folge = ["Feuer rechts", "Munition links", "Munition rechts", "Kamera Zoom", "Korrektur"]
    mc.late.sort(key=lambda e: folge.index(e[1]))
    return mc


def main():
    os.makedirs(BUILD, exist_ok=True)
    src = {}
    for name in ("flakradar", "flak"):
        with open(os.path.join(LUA_DIR, name + ".lua"), encoding="utf-8") as f:
            src[name] = minify(f.read())
    kp = sperrprofil.koerper()
    for seite, cx, cz, gy in TUERME:
        prf = sperrprofil.profil(cx, cz, gy, kp)
        fl = src["flak"].replace("PRF='0'", "PRF='%s'" % ",".join(fmt(float(v)) for v in prf))
        assert fl != src["flak"], "PRF nicht gefunden"
        fl = kopf(fl, "f%sf" % seite)
        fr = kopf(src["flakradar"], "f%sr" % seite)
        for name, s in (("flakradar " + seite, fr), ("flak " + seite, fl)):
            print("%-10s %5d Zeichen %s" % (name, len(s), "OK" if len(s) <= LUA_LIMIT else "ZU LANG"))
            if len(s) > LUA_LIMIT:
                sys.exit("Skript zu lang")
        fname = "Figet Marena Flak %s %s.xml" % (seite, VERSION)
        out = os.path.join(BUILD, fname)
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write(build(fr, fl, seite, src).xml())
        print("geschrieben:", out)
        if "--install" in sys.argv:
            dst = os.path.join(os.environ["APPDATA"], "Stormworks", "data", "microprocessors", fname)
            shutil.copyfile(out, dst)
            print("installiert:", dst)


if __name__ == "__main__":
    main()
