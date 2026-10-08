"""Baut die Lagezentrale der Figet Marena:

- "Figet Marena Lage" (4 x 4): 6 x MASTRADAR (je ein Radar (Phalanx) am Mast, manueller Modus, kreist auf seiner
  Hoehe) + LAGE (8 Ziele mit festen Nummern in der Welt, Luft/See, Markierung, Bedrohung)
- "Figet Marena Bildschirm" (4 x 3): BILD (Monitor 9x5: 3D-Radar | Kamera der gewaehlten Waffe | Zielliste, Touch)
  + 3 Video Switchboxes fuer die 4 Waffen-Kameras

- mit --install zusaetzlich nach %APPDATA%/Stormworks/data/microprocessors kopieren
"""
import math
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_schiff import MC, minify, fmt, LUA_LIMIT, LUA_DIR, BUILD  # noqa: E402

VERSION = "v3.3"          # Lage-Chip (v2.9 Tempo erst bestaetigt; v3.0 stehend Ziel ab 60 m; v3.1 Hafen: enger Fang, See vorn)
VERSION_BILD = "v3.3"
VERSION_WAHL = "v1.2"
# Mast-Radare: Teil-Position (zum Verkabeln), Strahl-Hoehe (Grad gegen das Deck, Gimbal hoechstens 45), Startphase (U),
# Seitenvorzeichen (-1 = gespiegelt eingebaut).
# v2.2: Radar 1 (oben hinten am Mast) sucht flach (8 Grad); Radar 2-3 halten Luftziele (frei: suchen 38/20 Grad hoch),
# Radar 4-5 Seeziele (frei: suchen flach), Radar 6 spaeter Raketen - bis dahin sucht es hoch (38 Grad) mit.
RADARE = [
    ((0, 42, -56), 8, 0, 1),
    ((0, 42, -46), 38, 0.5, 1),
    ((0, 36, -44), 20, 0.25, 1),
    ((0, 36, -58), 8, 0.75, 1),
    ((-5, 36, -51), 8, 0.25, 1),
    ((5, 36, -51), 38, 0, -1),    # gespiegelt eingebaut (t 1): zaehlt gespiegelt. Andres Log 03.10. 22:30: Radar 2 und 6
]                                   # sahen dasselbe Objekt (250 m, 33 Grad hoch) bei +150 / -150 Grad; mit +1 (21:50-22:35)
#                                     machte Radar 6 Geister-Ziele (Heli rechts bei 142 Grad zusaetzlich links bei 220)
FOV = "0.1"

# Waffen-Schreiber (lua/schreiber.lua -> tools/waffen_logger.py), in Lage-, Bildschirm- und Flak-Chips
SCHREIBER_PROPS = [
    ("Schreiber Port", 8768, "Waffen-Schreiber: Port von tools/waffen_logger.py auf dem PC (0 = aus)"),
    ("Schreiber Zeichen", 3000, "Waffen-Schreiber: hoechstens so viele Zeichen je Paket (laengere: aelteste Zeilen weg, gezaehlt)"),
]


# v2.8: Schreiber v2 steckt in den Skripten selbst (sie schreiben auf, was sie sehen und entscheiden, nicht nur ihre
# Kabel). Name und Sende-Takt je Skript: (alle LT Ticks, Versatz LO) - zusammen hoechstens eine Anfrage je Tick
TAKT = {"la": (16, 0), "ba": (16, 1), "fLr": (8, 2), "fLf": (16, 3), "fRr": (8, 4), "fRf": (16, 5),
        "r1": (16, 6), "r2": (16, 7), "r3": (16, 8), "r4": (16, 9), "r5": (16, 11), "r6": (16, 13),
        # Kanonen vorn (04.10.): Radare auf den freien Takten 14/15; die Feuerleitungen (kurze Zeilen) teilen sich die
        # Takte mit Bildschirm und Flak-L-Feuerleitung - die Warteschlange des Spiels nimmt sie einen Tick spaeter
        "kBr": (16, 14), "kAr": (16, 15), "kBf": (16, 1), "kAf": (16, 3),
        # Dachkamera (04.10.)
        "ka": (16, 0),
        # Schutz-Chip (Chaff, Pumpen)
        "sc": (16, 5)}
_belegt = [lo + i * lt for lt, lo in TAKT.values() for i in range(16 // lt)]
assert max(_belegt.count(t) for t in set(_belegt)) <= 2 and all(t < 16 for t in _belegt), "Schreiber-Takte zu voll"


def kopf(s, q):
    """Schreiber-Kopf eines Skripts setzen: Name q, Sende-Takt aus TAKT."""
    lt, lo = TAKT[q]
    neu = s.replace("LQ='x' LT=16 LO=0", "LQ='%s' LT=%d LO=%d" % (q, lt, lo))
    assert neu != s, ("Schreiber-Kopf nicht gefunden", q)
    return neu


def schreiber_props(mc, x, y):
    for k, (name, val, desc) in enumerate(SCHREIBER_PROPS):
        mc.comp(34, (x, y - k), {"n": name}, extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))


PROPS = [
    ("Such Tempo", 0.25, "So schnell kreisen die Mast-Radare (U/s; der Schirm schafft hoechstens 0,28)"),
    ("Kompass Richtung", -1, "-1: der Kompass des Physik-Sensors zaehlt gegen den Uhrzeigersinn (wie Flak)"),
    ("Ziel vergessen s", 4, "So lange bleibt ein Ziel ohne neue Ortung (v2: das haltende Radar meldet staendig - 4 s ohne heisst weg)"),
    ("Radar Reichweite m", 10000, "Ortungen weiter weg zaehlen nicht (die Radare sehen ueber 20 km - im Hafen fuellte das die Liste)"),
    ("Mindestabstand m", 30, "Ortungen naeher zaehlen nicht (Deck, eigener Heli; Helis kommen naeher als 100 m)"),
    ("Luft immer ab m", 120, "So hoch ueber dem Meer ist sofort ein Luftziel; darunter erst nach der zweiten Ortung"),
    ("See Tempo max m/s", 28, "Schneller (Strecke in 2,5 s) ist kein Schiff - nie Kanonen-Ziel (tief fliegende Hubschrauber/Jets)"),
    ("See Hoehe max m", 7, "Nicht-Luftziele, die (geglaettet) hoeher als das ueber dem Meer liegen, sind an Land - nie Kanonen-Ziel"),
    ("See Ziel bis Grad", 145, "See-Ziele weiter achtern (ab Bug gezaehlt) erreicht keine Kanone - sie zaehlen beim Platz-Vergleich 20-mal so weit"),
    ("Stehend Ziel ab m", 60, "Luftziele hoeher als das ueber dem Meer sind auch stehend ein Ziel (schwebender Heli); tiefer nur, wenn sie sich bewegt haben"),
    ("Luft ab m", 15, "Luftziel: hoeher als das ueber dem Meer und schneller als 15 m/s"),
    ("Luft sicher ab m", 30, "Hoeher als das ueber dem Meer ist immer ein Luftziel (schwebender Hubschrauber)"),
    ("Bedrohung m", 1500, "Bedrohung: Luftziel naeher als das ..."),
    ("Bedrohung Annaeherung", 5, "... und kommt mit mehr als so vielen m/s naeher"),
]


def mastradar(src, k):
    pos, pb, ph, rs = RADARE[k]
    s = src.replace("RN=0 RS=1 PB=0 PH=0", "RN=%d RS=%d PB=%s PH=%s" % (k + 1, rs, fmt(pb), fmt(ph)))
    assert s != src, "RN-Zeile nicht gefunden"
    return kopf(s, "r%d" % (k + 1))


def build_lage(src):
    mc = MC("Figet Marena Lage",
            "Lage %s: Mast-Radar 1 sucht; Radar 2-3 halten Luftziele, 4-5 Seeziele, 6 spaeter Raketen; Bedrohung"
            % VERSION, 4, 4)
    radar = [mc.node("Radar %d" % (k + 1), 1, 5, "Radar (Phalanx) %d am Mast %s: Radar Data (manueller Modus)" % (k + 1, RADARE[k][0]),
                     k % 4, k // 4, (-10, 7 - k)) for k in range(6)]
    phys = mc.node("Physik-Sensor", 1, 5, "Physics Sensor (Composite, derselbe wie an Schiff- und Flak-Chip)", 2, 1, (-10, 0))
    bed = mc.node("Bedienung", 1, 5, "Bildschirm-Chip: Ausgang 'Bedienung' (seit v2 nicht mehr gebraucht)", 3, 1, (-10, -1))

    def rd(q, ch, pos, typ=31):
        return mc.comp(typ, pos, {"i": ch} if ch else {}, [(q, 0)])

    # MASTRADAR bekommt das Radar-Composite + Bool 9/10 von LAGE (ein Radar erkannte 'ab Strahl'/'ab Sockel') - Kreis,
    # darum bekommen die Skripte ihren Eingang erst, wenn LAGE steht
    ms = [mc.comp(56, (-7, 7 - 2 * k), {"script": mastradar(src["mastradar"], k)}, []) for k in range(6)]
    werte, gut, strahl, sockel = [], [], [], []
    for k in range(6):
        werte += [rd(ms[k], ch, (-5 + 0.5 * j, 7.5 - 2 * k - 0.5 * j)) for j, ch in enumerate((2, 3, 4))]
        gut.append(rd(ms[k], 0, (-4, 6.5 - 2 * k), 29))
        strahl.append(rd(ms[k], 1, (-3.5, 6.5 - 2 * k), 29))
        sockel.append(rd(ms[k], 2, (-3, 6.5 - 2 * k), 29))
    werte += [rd(phys, ch, (-7, -1 - 0.5 * j)) for j, ch in enumerate((0, 2, 1, 16, 14, 15))]
    werte.append(rd(bed, 0, (-7, -5)))
    auto = rd(bed, 0, (-7, -6), 29)
    w = mc.comp(40, (-2, 3), {"count": len(werte)}, [(c, 0) for c in werte])
    wb = mc.comp(41, (-2, 1), {"count": 19}, [("inc", (w, 0))] + [(c, 0) for c in gut + [auto] + strahl + sockel])
    lage = mc.comp(56, (0, 1), {"script": src["lage"]}, [(wb, 0)])
    fs, fb = rd(lage, 27, (-9, -3), 29), rd(lage, 28, (-9, -4), 29)
    for k in range(6):
        ein = mc.comp(41, (-8.5, 7 - 2 * k), {"count": 2, "offset": 8}, [("inc", (radar[k], 0)), (fs, 0), (fb, 0)])
        if k > 0:
            # v2: Radar k+1 haelt Platz k: Richtung (LAGE Zahl 19+2k/20+2k) auf Kanal 29/30, 'haelt' (Bool 10+k) auf 11
            ein = mc.comp(40, (-9, 6.5 - 2 * k), {"count": 2, "offset": 28}, [
                ("inc", (ein, 0)), (rd(lage, 18 + 2 * k, (-10.5, 7 - 2 * k)), 0), (rd(lage, 19 + 2 * k, (-10.5, 6.5 - 2 * k)), 0)])
            ein = mc.comp(41, (-9.5, 6.5 - 2 * k), {"count": 1, "offset": 10}, [
                ("inc", (ein, 0)), (rd(lage, 9 + k, (-11, 6.5 - 2 * k), 29), 0)])
        next(c for c in mc.comps if c[1] == ms[k])[3].append((ein, 0))
    for k, (name, val, desc) in enumerate(PROPS):
        mc.comp(34, (-12, 8 - k), {"n": name}, extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))
    schreiber_props(mc, -16, 8)
    for k in range(6):
        mc.node("Gimbal %d" % (k + 1), 0, 5, "Radar (Phalanx) %d am Mast: Gimbal Input" % (k + 1), k % 4, 2 + k // 4, (7, 7 - k), (ms[k], 0))
    an = rd(lage, 26, (4, -1), 29)
    mc.node("Radare an", 0, 0, "alle 6 Radar (Phalanx) am Mast: Activate", 2, 3, (7, -1), (an, 0))
    mc.node("Lage", 0, 5, "Zielliste (5 Ziele) an den Bildschirm-Chip", 3, 3, (7, -2), (lage, 0))
    return mc


def bild_flak(s):
    """v2.8: Sperrprofile und Lage der Flak-Tuerme (dieselben wie in den Flak-Chips) in BILD einsetzen - BILD gibt einer
    Flak nur Ziele, die sie ueber Mast und Aufbauten hinweg erreicht."""
    import build_flak
    import sperrprofil
    kp = sperrprofil.koerper()
    # nur der Physik-Sensor im Rumpf (Koerper mit den meisten Teilen) - seit 05.10. hat jede Rakete einen eigenen
    rum = max(range(len(kp)), key=lambda k: len(kp[k]))
    ps = [p for d, p in kp[rum] if d == "physics_sensor"]
    assert len(ps) == 1, ("Physik-Sensor", ps)
    px, py, pz = ps[0]
    for (seite, cx, cz, gy), ph in zip(build_flak.TUERME, ("PL", "PR")):
        prf = sperrprofil.profil(cx, cz, gy, kp)
        assert max(prf) < 44, "Sperrprofil ueber 43 Grad passt nicht in ein Zeichen"
        neu = s.replace("%s='0'" % ph, "%s='%s'" % (ph, "".join(chr(48 + math.ceil(v)) for v in prf)))
        assert neu != s, ph
        s = neu
    cx, cz, gy = build_flak.TUERME[1][1:]
    assert build_flak.TUERME[0][1:] == (-cx, cz, gy), "Flak-Tuerme nicht spiegelgleich"
    fe = next(p[1] for p in build_flak.PROPS if p[0] == "AA tiefster Winkel Grad")
    # v3.3: tote Winkel der Kanonen vorn - bis wohin (ab Bug, beidseitig) ihr Sperrprofil frei ist (unter 3 Grad:
    # Schiffsziele liegen fast waagerecht), 5 Grad Abstand
    import build_kanone
    gs = []
    for k in ("B", "A"):
        _, _, _, gx, gz, gyy, _, _, _ = next(q for q in build_kanone.KANONEN if q[0] == k)
        gp = sperrprofil.profil(gx, gz, gyy, kp)
        frei_bis = min(min(i, 72 - i) for i in range(72) if gp[i] > 3) * 5
        gs.append(fmt(round((frei_bis - 5) / 360, 3)))
    neu = s.replace("GS={0,0}", "GS={%s}" % ",".join(gs))
    assert neu != s, "GS"
    s = neu
    neu = s.replace("FX,FZ,FH,FE=0,0,0,0", "FX,FZ,FH,FE=%s,%s,%s,%s" % (
        fmt((cx - px) * .25), fmt((cz - pz) * .25), fmt((gy - py) * .25), fmt(fe)))
    assert neu != s, "FX"
    return neu


def build_bild(src):
    mc = MC("Figet Marena Bildschirm",
            "Bildschirm %s: 3D-Radar | Kamera | Zielliste; Waffen waehlen Ziele selbst, Master Arm, Leertaste. H5 Waffe"
            % VERSION_BILD, 4, 3)
    lage = mc.node("Lage", 1, 5, "Lage-Chip: Ausgang 'Lage'", 0, 0, (-10, 6))
    mc.node("Touch", 1, 5, "Monitor 9x5 am Steuersitz: Touch Output (seit v2 nicht mehr gebraucht)", 1, 0, (-10, 5))
    sitz = mc.node("Sitz", 1, 5, "Steuersitz: Seat data (H5 naechste Waffe, Leertaste, besetzt)", 2, 0, (-10, 4))
    fl = mc.node("Flak L Daten", 1, 5, "Flak-L-Chip: Ausgang 'Flak Daten'", 3, 0, (-10, 3))
    fr = mc.node("Flak R Daten", 1, 5, "Flak-R-Chip: Ausgang 'Flak Daten'", 0, 1, (-10, 2))
    kam = [mc.node("Kamera %s" % n, 1, 6, "Kamera %s: Camera Feed" % w, x, z, (-10, 1 - k))
           for k, (n, w, x, z) in enumerate([("BC", "auf dem Battle-Cannon-Turm vorn", 1, 1),
                                             ("AC vorn", "auf dem Autokanonen-Turm vorn", 2, 1),
                                             ("Flak L", "auf dem linken Flak-Turm", 3, 1),
                                             ("Flak R", "auf dem rechten Flak-Turm", 0, 2)])]
    # v1.2: neuer Anschluss am Ende (die alten behalten Nummer und Lage, ihre Kabel bleiben)
    wahl = mc.node("Wahl", 1, 5, "Waffenwahl-Chip: Ausgang 'Wahl' (Monitor 2x3 neben dem Sitz)", 3, 2, (-10, -4), late=True)

    def rd(q, ch, pos, typ=31):
        return mc.comp(typ, pos, {"i": ch} if ch else {}, [(q, 0)])

    # v2: Zahl 21/22 Flak L/R (gepackt, Flak-Kanal 18), 23 Waffenwahl-Wunsch (die Radar-Richtungen dort braucht BILD nicht)
    w = mc.comp(40, (-5, 5), {"count": 3, "offset": 20}, [("inc", (lage, 0))] + [
        (c, 0) for c in (rd(fl, 17, (-7, 5)), rd(fr, 17, (-7, 4.5)), rd(wahl, 0, (-7, 4)))])
    # Bool 26 Master Arm (ueber den Waffenwahl-Chip), 28 H5, 30 Leertaste, 31 Sitz besetzt
    w = mc.comp(41, (-5, 4), {"count": 1, "offset": 25}, [("inc", (w, 0)), (rd(wahl, 0, (-7, 3), 29), 0)])
    w = mc.comp(41, (-5, 3.5), {"count": 1, "offset": 27}, [("inc", (w, 0)), (rd(sitz, 4, (-7, 2.5), 29), 0)])
    wb = mc.comp(41, (-5, 3), {"count": 2, "offset": 29}, [("inc", (w, 0)), (rd(sitz, 30, (-7, 2), 29), 0),
                                                            (rd(sitz, 31, (-7, 1.5), 29), 0)])
    # Video: BC / AC vorn -> s1, Flak L / Flak R -> s2, vorn / Flak -> s3 -> BILD (zeichnet darueber); die Schalter
    # kommen aus BILD (Bool 2-4) - Kreis, darum bekommen die Switchboxes ihren Schalt-Eingang erst danach
    s1 = mc.comp(57, (-5, 0), {}, [(kam[0], 0), (kam[1], 0)])
    s2 = mc.comp(57, (-5, -2), {}, [(kam[2], 0), (kam[3], 0)])
    s3 = mc.comp(57, (-3, -1), {}, [(s1, 0), (s2, 0)])
    bild = mc.comp(56, (-1, 2), {"script": src["bild"]}, [(wb, 0), (s3, 0)])
    for k, s in enumerate((s1, s2, s3)):
        sw = rd(bild, k + 1, (1, -1 - k), 29)
        next(c for c in mc.comps if c[1] == s)[3].append((sw, 0))
    schreiber_props(mc, -12, 6)
    mc.node("Monitor", 0, 6, "Monitor 9x5 am Steuersitz: Video Signal", 1, 2, (7, 2), (bild, 1))
    mc.node("Bedienung", 0, 5, "an Lage-Chip, Waffenwahl-Chip und Flak-Chips ('Lage'): Waffe, Ziele je Waffe, Feuer frei, AUTO",
            2, 2, (7, 1), (bild, 0))
    return mc


def umriss(spalten=96, za=-155, kz=92 / 224):
    """Halbe Schiffsbreite (Bloecke) je Spalte der Waffenwahl-Karte, aus allen Teilen des Rumpf-Koerpers."""
    import re
    import umbau_v1 as u
    s = open(u.VEH, encoding="utf-8").read()
    i0, e0 = s.index("<bodies>"), s.index("</bodies>")
    bod, a = [], s.index("<body ", i0)
    while 0 <= a < e0:
        e = s.index("</body>", a)
        bod.append((a, e))
        a = s.find("<body ", e)
    r = max(bod, key=lambda q: s.count("<c", q[0], q[1]))
    t = re.sub(r"<microprocessor_definition.*?</microprocessor_definition>", "", s[r[0]:r[1]], flags=re.S)
    hw = [0] * spalten
    for m in re.finditer(r"<vp([^/]*)/>", t):
        x, _, z = u.xyz(m.group(1))
        i = int((z - za) * kz + 2)
        if 0 <= i < spalten:
            hw[i] = max(hw[i], abs(x))
    return hw


def build_wahl(src):
    mc = MC("Figet Marena Waffenwahl",
            "Waffenwahl %s: Monitor 2x3 neben dem Sitz zeigt das Schiff von oben; Waffe antippen = waehlen; Master Arm"
            % VERSION_WAHL, 3, 2)
    bed = mc.node("Bedienung", 1, 5, "Bildschirm-Chip: Ausgang 'Bedienung'", 0, 0, (-6, 3))
    touch = mc.node("Touch", 1, 5, "Monitor 2x3 neben dem Sitz: Touch Output", 1, 0, (-6, 2))

    def rd(q, ch, pos, typ=31):
        return mc.comp(typ, pos, {"i": ch} if ch else {}, [(q, 0)])

    w = mc.comp(40, (-3, 2), {"count": 2, "offset": 25}, [("inc", (bed, 0)), (rd(touch, 2, (-4, 3)), 0), (rd(touch, 3, (-4, 2.5)), 0)])
    # v1.2: Anschluss 'Master Arm' ist das Out Signal des Instrument Panels am Armaturenbrett (Flip Switch 1)
    ma = mc.node("Master Arm", 1, 5, "Instrument Panel am Armaturenbrett: Out Signal (Flip Switch 1 = Master Arm)", 2, 1, (-6, 0),
                 late=True)
    wb = mc.comp(41, (-3, 1), {"count": 2, "offset": 12}, [("inc", (w, 0)), (rd(touch, 0, (-4, 1.5), 29), 0),
                                                           (rd(ma, 0, (-4, 1), 29), 0)])
    lua = mc.comp(56, (-1, 1), {"script": src["waffenwahl"]}, [(wb, 0)])
    mc.node("Monitor", 0, 6, "Monitor 2x3 neben dem Sitz: Video Signal", 2, 0, (4, 3), (lua, 1))
    mc.node("Wahl", 0, 5, "an den Bildschirm-Chip (Eingang 'Wahl')", 0, 1, (4, 2), (lua, 0))
    mc.node("Monitor an", 0, 0, "Monitor 2x3 neben dem Sitz: Power Switch", 1, 1, (4, 1), (rd(lua, 3, (2, 1), 29), 0))
    return mc


def main():
    os.makedirs(BUILD, exist_ok=True)
    src = {}
    for name in ("mastradar", "lage", "bild", "waffenwahl"):
        with open(os.path.join(LUA_DIR, name + ".lua"), encoding="utf-8") as f:
            src[name] = minify(f.read())
    hw = umriss()
    neu = src["waffenwahl"].replace("UM='0'", "UM='%s'" % ",".join(str(v) for v in hw))
    assert neu != src["waffenwahl"], "UM nicht gefunden"
    src["waffenwahl"] = neu
    src["bild"] = kopf(bild_flak(src["bild"]), "ba")
    src["lage"] = kopf(src["lage"], "la")
    for name, s in src.items():
        print("%-10s %5d Zeichen %s" % (name, len(s), "OK" if len(s) <= LUA_LIMIT else "ZU LANG"))
        if len(s) > LUA_LIMIT:
            sys.exit("Skript zu lang")
    for mc, fname in ((build_lage(src), "Figet Marena Lage %s.xml" % VERSION),
                      (build_bild(src), "Figet Marena Bildschirm %s.xml" % VERSION_BILD),
                      (build_wahl(src), "Figet Marena Waffenwahl %s.xml" % VERSION_WAHL)):
        assert len(mc.desc) <= 128, (fname, len(mc.desc))
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
