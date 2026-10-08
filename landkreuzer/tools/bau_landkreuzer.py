"""Baut den KI-Landkreuzer als Stormworks-Fahrzeugdatei: landkreuzer/fahrzeug/KI Landkreuzer.xml

Grundidee: alles, was im Schiff schon funktioniert, wird als genaue Text-Kopie uebernommen und nur verschoben:
- die vier Geschuetztuerme samt Munitionsmagazin, Rohren, Turm-Radar und Turm-Kamera (Module, siehe MODULE)
- Physik-Sensor, Steuersitz, Monitore, Instrumentenblock, Dachkamera, die 6 Mast-Radare (Einzelteile, siehe EINZEL)
- alle Kabel dazwischen (aus den Schiffs-Kabeln umgerechnet)
- alle Waffen-Chips (mit den Schiffs-Bauskripten neu gebaut, Geometrie vom Landkreuzer, Land-Aenderungen)
Neu dazu: Rumpf aus Bloecken, Fahrwerksraum mit 14 Elektromotoren und Wellen-Stummeln fuer die Raeder, Batterien,
Laser fuer die Fahr-KI, KI-Chip, Karten-Monitor.

Raeder: die Spiel-Definition der Raeder liegt nur auf Andres PC (rom/data/definitions); darum setzt Andre EIN Rad im
Editor an den vorderen linken Wellen-Stummel, und tools/raeder.py kopiert es an alle 14 Stummel.

Koordinaten in Bloecken (0,25 m): x rechts, y oben, z vorn. Boden des Fahrwerksraums y -4, Hauptboden y 1.
Aufruf: python landkreuzer/tools/bau_landkreuzer.py [--schreiber]   (--schreiber: Waffen-Schreiber an Port 8768 an)
"""
import math
import os
import re
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HIER))
LK = os.path.dirname(HIER)
sys.path.insert(0, HIER)
import build_mc  # noqa: E402
import fz  # noqa: E402

sys.modules["build_mc"] = build_mc
sys.path.insert(1, os.path.join(ROOT, "tools"))
os.environ.setdefault("APPDATA", os.path.join(LK, "kein_appdata"))

AUS_DATEI = os.path.join(LK, "fahrzeug", "KI Landkreuzer.xml")
SCHIFF_LUA = os.path.join(ROOT, "lua")
LK_LUA = os.path.join(LK, "lua")
VERSION = "v1.0"

# ---------------------------------------------------------------------------------------------------------------------
# Plan
# ---------------------------------------------------------------------------------------------------------------------
# Module aus dem Schiff: Name, Kasten im Rumpf des Schiffs (lo, hi), Verschiebung ins Panzer-System, Schiffs-Koerper
# (Index in der Schiffsdatei) der Tuerme/Rohre/Kameras/Monitor-Gelenke, die mitkommen
MODULE = [
    ("AC", (-6, 1, 16), (6, 6, 36), (0, 0, 0), [6, 7, 14]),            # Heavy-Autocannon-Turm vorn + 10 Trommeln
    ("BC", (-6, 1, 0), (6, 10, 15), (0, 0, 0), [4, 5, 13]),            # Battle-Cannon-Turm (2 Rohre) + Gurt-Magazin
    ("BRUECKE", (-14, 15, -16), (14, 34, -3), (0, 0, 0), [17, 27]),    # Bruecke: Sitz, Monitore, Fenster, Tueren, Dachkamera
    ("HECK", (-15, 6, -110), (15, 14, -76), (0, -5, 45), [8, 10, 12, 15, 9, 11, 2, 16]),   # 2 Flak-Tuerme + 48 Trommeln
]
NICHT_MIT = ("inventory_", "sign_", "microprocessor")   # (die 2 solid_rocket_small auf dem Bruecken-Dach tragen die Kamera)

# Rumpf: x -15..15, z HINTEN..VORN; Decks je Abschnitt (z von, z bis, Deck-Hoehe)
X0, X1 = -15, 15
HINTEN, VORN = -66, 37
BODEN, HAUPTBODEN = -4, 1
ABSCHNITTE = [(16, 36, 6), (0, 15, 10), (-30, -1, 10), (-65, -31, 9)]
SOCKEL = ((-14, 11, -16), (14, 14, -3))
# Bug als Keil (wie die obere und untere Front-Platte eines Panzers): oben 45 Grad vom vorderen Deck (y 6) herab, unten
# 45 Grad vom Boden herauf; die Spitze liegt bei z VORN + 5, y 0,5 (1,25 m ueber der Rumpf-Unterkante). Eine Spitze
# unten am Boden 3 m vor den Vorderraedern wuerde schon an maessigen Haengen aufsetzen.
BUG_SCHRITTE = 6
R_SCHRAEGE = (-1, 0, 0, 0, 1, 0, 0, 0, -1)       # 02_wedge so gedreht: offene Seiten +y und +z (aus dem Schiff gelesen)
R_SCHRAEGE_UNTEN = (1, 0, 0, 0, -1, 0, 0, 0, -1)  # ... um x gedreht: offene Seiten -y und +z (untere Bug-Schraege)
# Heck: die letzten 3 Reihen unten 45 Grad hochgezogen (mehr Boden-Abstand beim Herunterfahren von Haengen)
HECK_SCHRITTE = 3
R_SCHRAEGE_HECK = (-1, 0, 0, 0, -1, 0, 0, 0, 1)   # offene Seiten -y und -z

# Fahrwerk: Rad-Achsen je Seite (z), Achs-Hoehe y, Motor-Spalte x
RAD_Z = [35, 20, 5, -10, -25, -40, -55]          # Mitte -10 = Schwerpunkt (grob geschaetzt)
# Lenk-Variante (--lenkung): diese Achsen sitzen auf senkrechten Gelenken (vorn 2, hinten 2), gebaut wie die Ruder der
# Figet Marena: Robotic Pivot (Teil a am Rumpf, Teil b am Rad-Koerper), daneben ein kleiner E-Motor mit Winkel-Welle, der
# das Gelenk antreibt (Gas fest 1 ueber eine Konstante, wie im Schiff); am Rad-Koerper haengt der Rad-Motor.
LENK_VORN, LENK_HINTEN = [35, 20], [-40, -55]
LENK_X = 17                                       # Gelenk-Spalte (aussen neben der Seitenwand x +-15)
LENK_Y = 3                                        # Hoehe von Gelenk-Teil b (a eins darueber)
# Ruder-Gelenk im Schiff je Seite: Teil b, Teil a, Gelenk-Motor, Winkel-Welle (x -9 links, +9 rechts)
RUDER = {"L": {"b": (-9, -12, -144), "a": (-9, -11, -144), "m": (-9, -10, -142), "w": (-9, -11, -142), "k": 1},
         "R": {"b": (9, -12, -144), "a": (9, -11, -144), "m": (9, -10, -142), "w": (9, -11, -142), "k": 3}}
ACHSE_Y = -3
MOTOR_X = 13

# Einzelteile aus dem Schiff: Name -> (Schiffs-Position des Teils, Art, neue Position)
EINZEL = {
    "phys": ((0, 27, -38), "physics_sensor", (0, 2, -12)),
    # Konstanten aus dem Chip-Raum des Schiffs: Gelenk-Winkel der beiden kleinen Monitore, Strom-Schalter des grossen
    "k_wahl": ((5, 7, -59), "gate_float_constant", (12, 2, -29)),
    "k_karte": ((5, 5, -59), "gate_float_constant", (12, 2, -27)),
    "k_monitor": ((-5, 6, -59), "gate_bool_constant", (12, 2, -25)),
    "k_chaff": ((5, 6, -59), "gate_float_constant", (12, 2, -23)),        # Winkel der 8 Chaff-Gelenke
}
EINZEL_LENKUNG = {"k_lenkmotor": ((0, -12, -99), "gate_float_constant", (12, 2, -21))}   # Gas 1 fuer die Gelenk-Motoren
# Chaff: 8 Werfer-Ketten (je 15 Flare Launcher auf einem Compact Pivot) wie an Deck der Figet Marena, auf dem Mitteldeck
CHAFF_KOERPER = list(range(18, 26))
CHAFF_GELENKE = [(sx, 16, z) for sx in (-9, 9) for z in (-39, -44, -49, -54)]
CHAFF_WEG = (0, -5, 18)
# Teile der Bruecke, die der Bau braucht (Position im Schiff = im Panzer, Verschiebung 0)
BRUECKE_TEILE = {"sitz": ("seat_compact", (0, 17, -10)), "monitor": ("monitor_9", (0, 22, -6)),
                 "instrumente": ("instrument_display", (-2, 19, -8)), "karte": ("monitor_3", (-3, 20, -10)),
                 "kamera": ("camera_gimbal_laser", (0, 33, -15)), "wahlmonitor": ("monitor_2x3", (4, 18, -8))}
# Mast-Radare: Schiff -> Panzer um MAST verschoben (Anordnung wie im Schiff, Lage-Chip unveraendert)
MAST = (0, -10, 27)
RADARE_SCHIFF = [(0, 42, -56), (0, 42, -46), (0, 36, -44), (0, 36, -58), (-5, 36, -51), (5, 36, -51)]
MAST_TURM = ((-1, 11, -25), (1, 31, -23))          # Turm aus Bloecken (lo, hi)

# Laser der Fahr-KI: (Name, Position, Drehung) - Strahl = lokale +y-Achse (wie der Laser an der Turm-Kamera)
R_VORN = (1, 0, 0, 0, 0, 1, 0, -1, 0)
R_LINKS = (0, 0, 1, -1, 0, 0, 0, -1, 0)
R_RECHTS = (0, 0, -1, 1, 0, 0, 0, -1, 0)
R_HINTEN = (-1, 0, 0, 0, 0, -1, 0, -1, 0)
R_UNTEN = (1, 0, 0, 0, -1, 0, 0, 0, -1)
SEITEN_LASER_X = 19
LASER = [
    # Lage wie die Fahr-KI rechnet: aeussere Front-Laser 3,5 m seitlich, Seiten-Laser 4,75 m (= 'Breite m' / 2, aussen
    # ueber den Raedern auf einem kurzen Ausleger)
    ("Laser vorn links", (-14, 3, VORN + 4), R_VORN),          # auf der Bug-Schraege (dort liegt sie bei y 2)
    ("Laser vorn Mitte", (0, 3, VORN + 4), R_VORN),
    ("Laser vorn rechts", (14, 3, VORN + 4), R_VORN),
    ("Laser links", (-SEITEN_LASER_X, 6, -8), R_LINKS),      # ueber den Raedern (Rad-Radius bis 6 Bloecke frei)
    ("Laser rechts", (SEITEN_LASER_X, 6, -8), R_RECHTS),
    ("Laser unten", (0, BODEN + BUG_SCHRITTE - 2, VORN + BUG_SCHRITTE - 1), R_UNTEN),  # in der Bugspitze, nach unten
    ("Laser hinten", (0, 3, HINTEN - 1), R_HINTEN),
]
# Batterien (Battery Large, Anschluss oben +2): im Fahrwerksraum
# 24 Stueck ueber die ganze Laenge verteilt (nur Batterien, kein Generator: der Schiffs-Diesel kuehlt mit Seewasser)
BATTERIEN = [(x, BODEN + 1, z) for z in (-6, -22, 28, 12, -38, -50) for x in (-9, -4, 4, 9)]
# Strom-Anschluesse im Schiff (Batterien, Generatoren): Kabel dorthin gehen im Panzer an die erste Batterie
SCHIFF_STROM = {(8, -18, -64), (-8, -18, -64), (4, -11, -39), (-4, -11, -39), (4, -11, -46), (-4, -11, -46),
                (8, -15, -96), (-8, -15, -96)}

# Chips auf dem Hauptboden (liegend, Drehung 1): Name -> (x, z) der Ecke; Feld (fx, fz) liegt bei (x+fx, 2, z+fz)
CHIP_Y = 2
CHIP_PLATZ = {
    "Lage": (-14, -29), "Bildschirm": (-9, -29), "Flak L": (-4, -29), "Flak R": (1, -29), "Kamera": (6, -29),
    "Kanone BC": (-14, -22), "Kanone AC": (-9, -22), "KI": (-4, -22), "Schutz": (6, -22),
}
# Schiffs-Chip -> Chip im Landkreuzer (gleiche Anschluesse)
CHIP_NAMEN = {"Figet Marena Lage": "Lage", "Figet Marena Bildschirm": "Bildschirm", "Figet Marena Flak L": "Flak L",
              "Figet Marena Flak R": "Flak R", "Figet Marena Kanone BC": "Kanone BC",
              "Figet Marena Kanone AC": "Kanone AC", "Figet Marena Kamera": "Kamera", "Figet Marena Schutz": "Schutz"}
# Chip-Eingaenge, die im Landkreuzer anders verkabelt sind als im Schiff (Schiffs-Kabel dorthin entfallen)
NEU_VERKABELT = {("Figet Marena Schutz", "Instrumente")}

FARBE_RUMPF = "4B5320"      # Oliv
FARBE_DECK = "3E4419"
FARBE_BODEN = "2B2B2B"


# ---------------------------------------------------------------------------------------------------------------------
def inbox(p, lo, hi):
    return all(lo[i] <= p[i] <= hi[i] for i in range(3))


def rstr(r):
    return ",".join(str(v) for v in r)


def teil(d, vp, r=None, extra_o="", innen="", t=0):
    """Neues Teil aus Text."""
    tt = ' t="%d"' % t if t else ""
    rr = ' r="%s"' % rstr(r) if r else ""
    return fz.Teil('<c%s%s><o%s%s>%s%s</o></c>' % (' d="%s"' % d if d != "block" else "", tt, rr, extra_o,
                                                    fz.vox("vp", vp), innen))


def block(vp, farbe=FARBE_RUMPF):
    return fz.Teil('<c><o bc="%s" ac="%s" sc="6">%s</o></c>' % (farbe, farbe, fz.vox("vp", vp)))


def vorlage(F, d, vp):
    """Genaue Text-Kopie des Schiffs-Teils (Art d an Position vp, irgendein Koerper)."""
    for _, ts in F.koerper:
        for t in ts:
            if t.d == d and t.vp == vp:
                return t
    raise KeyError((d, vp))




def schiff_lua(n):
    return build_mc.minify(open(os.path.join(SCHIFF_LUA, n + ".lua"), encoding="utf-8").read())


def land_lua():
    """Schiffs-Skripte (verkleinert) mit den Land-Aenderungen: Hoehen gegen die eigene Hoehe statt gegen das Meer
    (an Land liegt der Boden nicht bei 0 m)."""
    def patch(s, alt, neu):
        assert s.count(alt) == 1, ("Land-Aenderung passt nicht mehr", alt)
        return s.replace(alt, neu)

    src = {n: schiff_lua(n) for n in ("flakradar", "flak", "mastradar", "lage", "bild", "kamera")}
    src["flakradar"] = patch(src["flakradar"], "if cp and hg>ahm and", "if cp and hg-agl>ahm and")
    src["flakradar"] = patch(src["flakradar"], "cq.a<120 and cq.g>ahm then", "cq.a<120 and cq.g-agl>ahm then")
    src["lage"] = patch(src["lage"], "local U,R=t.p[3]+t.v[3]*t.a/60,dist(t)", "local U,R=t.p[3]+t.v[3]*t.a/60-AH,dist(t)")
    src["lage"] = patch(src["lage"], "local x,z,al=N(19),N(20),N(21)", "local x,z,al=N(19),N(20),N(21)\nAH=al")
    src["lage"] = patch(src["lage"], "t.air==true and U>sz)", "t.air==true and U-al>sz)")
    return src


# Land-Eigenschaften (ueberschreiben die Werte der Schiffs-Chips)
LAGE_LAND = {"See Hoehe max m": 100000, "Luft sicher ab m": 40, "Luft ab m": 20, "See Tempo max m/s": 35,
             "See Ziel bis Grad": 180, "Radar Reichweite m": 6000}
FLAK_LAND = {"AA Mindesthoehe m": 10}
KANONE_LAND = {"Ziel Hoehe fest m": -999, "Ziel Tempo max m/s": 35, "AA Mindesthoehe m": -200,
               "AA tiefster Winkel Grad": -10}


def chip_sc(w, l):
    """'sc' eines Microcontrollers = Zahl der Flaechen (im Schiff: 2x3 -> 22, 4x5 -> 58, 6x6 -> 96)."""
    return 2 * w * l + 2 * w + 2 * l


class Bau:
    def __init__(self, schreiber=False, lenkung=False):
        self.F = fz.Fahrzeug.lesen()
        self.schreiber = schreiber
        self.lenkung = lenkung
        self.lenk = []             # (vorn/hinten, Gelenk-Teil a, Gelenk-Motor)
        self.rumpf = []            # Teile des Rumpf-Koerpers
        self.koerper = []          # weitere Koerper: Listen von Teilen
        self.teil_voxel = set()    # Positionen der Rumpf-Teile
        self.kasten = set()        # reservierte Voxel (Module, Umfeld von Teilen): Rumpf-Bloecke nur ausnahmsweise
        self.kabel = []
        self.weg = {}              # (Schiffs-Koerper, Schiffs-vp) -> Verschiebung (uebernommene Teile)
        self.neu = {}              # Name -> Teil (Teile, die der Bau braucht)
        self.motoren = {"L": [], "R": []}
        self.stummel = []          # (Seite, Position des aeussersten Wellen-Blocks)
        self.chips = {}            # Name -> (MC, Teil)
        self.meldungen = []

    def plus(self, t):
        self.rumpf.append(t)
        self.teil_voxel.add(t.vp)

    def reserviere(self, p, lo, hi):
        for x in range(lo[0], hi[0] + 1):
            for y in range(lo[1], hi[1] + 1):
                for z in range(lo[2], hi[2] + 1):
                    self.kasten.add(fz.add(p, (x, y, z)))

    # ---------------- Module ----------------
    def module(self):
        F = self.F
        for name, lo, hi, d, kliste in MODULE:
            for t in F.koerper[0][1]:
                if inbox(t.vp, lo, hi) and not t.d.startswith(NICHT_MIT):
                    n = t.verschoben(d)
                    self.plus(n)
                    self.weg[(0, t.vp)] = d
            for bi in kliste:
                neu = [t.verschoben(d) for t in F.koerper[bi][1]]
                for t in F.koerper[bi][1]:
                    self.weg[(bi, t.vp)] = d
                self.koerper.append(neu)
            self.reserviere(d, lo, hi)
        alle = self.rumpf + [t for k in self.koerper for t in k]
        for key, (dd, pos) in BRUECKE_TEILE.items():
            self.neu[key] = next(t for t in alle if t.d == dd and t.vp == pos)
        # Instrumentenblock: Schalter fuer den Landkreuzer. Schalter aus = KI faehrt und schiesst (komplett autonom);
        # Bool 1 'Waffen sperren', 2 Zielkorrektur (Knopf, wie im Schiff), 3 'KI Pause', 4 'Nach Hause'
        ins = self.neu["instrumente"]
        x = ins.xml
        for alt, neu in (('name="Master arm"', 'name="Waffen sperren"'), ('name="Auto Chaff"', 'name="KI Pause"'),
                         ('name="Water Pumps"', 'name="Nach Hause"')):
            assert x.count(alt) == 1, alt
            x = x.replace(alt, neu)
        n = fz.Teil(x)
        self.rumpf[self.rumpf.index(ins)] = n
        self.neu["instrumente"] = n

    # ---------------- Einzelteile ----------------
    def einzel(self):
        F = self.F
        einzel = dict(EINZEL, **(EINZEL_LENKUNG if self.lenkung else {}))
        for name, (alt, d, neu) in einzel.items():
            t = vorlage(F, d, alt)
            n = t.verschoben(fz.sub(neu, alt))
            self.plus(n)
            self.neu[name] = n
            self.weg[(0, alt)] = fz.sub(neu, alt)
            self.reserviere(neu, (-1, 0, -1), (1, 1, 1))
        for k, alt in enumerate(RADARE_SCHIFF):
            t = vorlage(F, "radar_advanced_phalanx", alt)
            n = t.verschoben(MAST)
            self.plus(n)
            self.neu["radar%d" % (k + 1)] = n
            self.weg[(0, alt)] = MAST
            self.reserviere(n.vp, (-1, 0, -1), (1, 3, 1))

    def chaff(self):
        F = self.F
        d = CHAFF_WEG
        for p in CHAFF_GELENKE:
            t = vorlage(F, "multibody_compact_pivot_robotic_a", p)
            self.plus(t.verschoben(d))
            self.weg[(0, p)] = d
            self.reserviere(fz.add(p, d), (-1, 0, -2), (1, 1, 2))
        for bi in CHAFF_KOERPER:
            self.koerper.append([t.verschoben(d) for t in F.koerper[bi][1]])
            for t in F.koerper[bi][1]:
                self.weg[(bi, t.vp)] = d
                self.kasten.add(fz.add(t.vp, d))

    # ---------------- Fahrwerk ----------------
    def fahrwerk(self):
        F = self.F
        motor = vorlage(F, "motor_medium", (0, -12, 41))
        for seite, sx in (("L", -1), ("R", 1)):
            # Winkel-Welle wie am Bugstrahlruder: verbindet lokal +y (Motor darueber) und lokal -x (nach aussen)
            rw = (1, 0, 0, 0, 1, 0, 0, 0, 1) if sx < 0 else (-1, 0, 0, 0, 1, 0, 0, 0, -1)
            for z in RAD_Z:
                if self.lenkung and z in LENK_VORN + LENK_HINTEN:
                    self.lenkachse(seite, sx, z, motor, rw)
                    continue
                mx = sx * MOTOR_X
                m = motor.verschoben(fz.sub((mx, ACHSE_Y + 2, z), motor.vp))
                self.plus(m)
                self.motoren[seite].append(m)
                self.plus(fz.Teil('<c d="trans_block_angle"><o r="%s" sc="6">%s</o></c>'
                                  % (rstr(rw), fz.vox("vp", (mx, ACHSE_Y, z)))))
                for x in range(MOTOR_X + 1, X1 + 1):
                    self.plus(fz.Teil('<c d="trans_block_straight"><o r="1,0,0,0,1,0,0,0,1" sc="6">%s</o></c>'
                                      % fz.vox("vp", (sx * x, ACHSE_Y, z))))
                self.stummel.append((seite, (sx * X1, ACHSE_Y, z)))
                self.reserviere((mx, ACHSE_Y, z), (-1, 0, -1), (1, 3, 1))
        bat = vorlage(F, "battery_large", (-4, -13, -39))
        self.batterien = []
        for p in BATTERIEN:
            b = bat.verschoben(fz.sub(p, bat.vp))
            self.plus(b)
            self.batterien.append(b)
            self.reserviere(p, (-1, 0, -1), (1, 2, 1))

    def lenkachse(self, seite, sx, z, motor, rw):
        """Lenkbare Achse: Gelenk wie das Ruder im Schiff, Rad-Motor und Stummel auf dem Gelenk-Koerper."""
        F = self.F
        R = RUDER[seite]
        xs = sx * LENK_X
        d = fz.sub((xs, LENK_Y, z - 1), R["b"])            # Teil b -> (xs, 3, z-1); Rad-Spalte bei z (wie Ruderblatt)
        a = vorlage(F, "multibody_robotic_pivot_01_a", R["a"]).verschoben(d)
        self.plus(a)
        gm = vorlage(F, "motor_small", R["m"]).verschoben(d)
        self.plus(gm)
        self.plus(vorlage(F, "trans_block_angle", R["w"]).verschoben(d))
        self.lenk.append(("vorn" if z in LENK_VORN else "hinten", a, gm))
        # Ausleger vom Rumpf zum Gelenk, zum Gelenk-Motor und zu seiner Welle
        for p in ((sx * 16, LENK_Y + 1, z - 1), (sx * 16, LENK_Y + 1, z), (sx * 16, LENK_Y + 1, z + 1),
                  (sx * 16, LENK_Y + 2, z + 1)):
            self.plus(block(p))
        # Rad-Koerper: Teil b, Saeule bis zum Rad-Motor, Rad-Motor (Kraft unten), Winkel-Welle = Stummel
        b = vorlage(F, "multibody_robotic_pivot_01_b", R["b"]).verschoben(d)
        k = [b] + [block((xs, y, z)) for y in range(ACHSE_Y + 4, LENK_Y + 1)]
        m = motor.verschoben(fz.sub((xs, ACHSE_Y + 2, z), motor.vp))
        k.append(m)
        k.append(fz.Teil('<c d="trans_block_angle"><o r="%s" sc="6">%s</o></c>' % (rstr(rw), fz.vox("vp", (xs, ACHSE_Y, z)))))
        self.koerper.append(k)
        self.motoren[seite].append(m)
        self.stummel.append((seite, (xs, ACHSE_Y, z)))
        self.reserviere((xs, ACHSE_Y, z), (-1, 0, -2), (1, LENK_Y + 2 - ACHSE_Y, 2))

    def batterie_knoten(self, k=0):
        return fz.add(self.batterien[k].vp, (0, 2, 0))

    # ---------------- Laser ----------------
    def laser(self):
        t = vorlage(self.F, "laser_distance_sensor", (3, 19, 10))
        self.laser_teile = []
        for name, p, r in LASER:
            xml = t.xml.replace('r="1,0,0,0,0,1,0,-1,0"', 'r="%s"' % rstr(r))
            n = fz.Teil(xml).verschoben(fz.sub(p, t.vp))
            self.plus(n)
            self.laser_teile.append((name, n))

    # ---------------- Rumpf ----------------
    def deck(self, z):
        for z0, z1, h in ABSCHNITTE:
            if z0 <= z <= z1:
                return h
        return None

    def rumpf_bauen(self):
        neu = []

        def setze(p, farbe=FARBE_RUMPF, aussen=False):
            """Block setzen, wenn frei. aussen=True: auch in Modul-Kaesten (Aussenwand), solange dort kein Teil sitzt."""
            if p in self.teil_voxel or (p in self.kasten and not aussen):
                return
            self.teil_voxel.add(p)
            neu.append(block(p, farbe))

        def schraege(p, r):
            if p not in self.teil_voxel:
                self.teil_voxel.add(p)
                neu.append(fz.Teil('<c d="02_wedge"><o r="%s" bc="%s" ac="%s" sc="5">%s</o></c>'
                                   % (rstr(r), FARBE_RUMPF, FARBE_RUMPF, fz.vox("vp", p))))

        # Bug-Keil: je Reihe oben eine Schraege (y top), unten eine (y lo - 1, ab der 2. Reihe), dazwischen hohl
        # (unterste und oberste Lage, Seitenwaende)
        for k in range(BUG_SCHRITTE):
            z = VORN + k
            top, lo = 6 - k, BODEN + k
            for x in range(X0, X1 + 1):
                for y in range(lo, top):
                    if y in (lo, top - 1) or x in (X0, X1):
                        setze((x, y, z), FARBE_BODEN if y == lo else FARBE_RUMPF, True)
                schraege((x, top, z), R_SCHRAEGE)
                if k:
                    schraege((x, lo - 1, z), R_SCHRAEGE_UNTEN)
        for z in range(HINTEN, VORN):
            # Unterkante: am Heck in HECK_SCHRITTE Reihen 45 Grad hochgezogen
            unten = BODEN + max(0, HINTEN + HECK_SCHRITTE - z)
            for x in range(X0, X1 + 1):
                setze((x, unten, z), FARBE_BODEN, True)
                if unten > BODEN:
                    schraege((x, unten - 1, z), R_SCHRAEGE_HECK)
            for y in range(unten + 1, HAUPTBODEN):
                setze((X0, y, z), aussen=True)
                setze((X1, y, z), aussen=True)
            h = self.deck(z)
            if h is None:
                # Bug- und Heckplatte bis zur Deckhoehe dahinter/davor
                top = self.deck(z - 1) if z > 0 else self.deck(z + 1)
                for x in range(X0, X1 + 1):
                    for y in range(unten + 1, top + 1):
                        setze((x, y, z), aussen=True)
                continue
            for x in range(X0, X1 + 1):
                setze((x, HAUPTBODEN, z), FARBE_BODEN)
                setze((x, h, z), FARBE_DECK)
            for y in range(HAUPTBODEN + 1, h):
                setze((X0, y, z), aussen=True)
                setze((X1, y, z), aussen=True)
            # Stufe zum Nachbar-Abschnitt mit tieferem Deck
            for nb in (z - 1, z + 1):
                h2 = self.deck(nb)
                if h2 is not None and h2 < h:
                    for x in range(X0, X1 + 1):
                        for y in range(h2 + 1, h):
                            setze((x, y, z))
        # Sockel unter der Bruecke: Aussenwaende und vier Saeulen
        (sx0, sy0, sz0), (sx1, sy1, sz1) = SOCKEL
        for y in range(sy0, sy1 + 1):
            for x in range(sx0, sx1 + 1):
                for z in range(sz0, sz1 + 1):
                    rand = x in (sx0, sx1) or z in (sz0, sz1)
                    saeule = x in (-7, 7) and z in (-12, -7)
                    if rand or saeule:
                        setze((x, y, z), aussen=True)
        # Aufstieg zur Bruecke: Plattform hinter den beiden Bruecken-Tueren (Tueren in der Rueckwand bei x +-14, z -16;
        # Bruecken-Boden y 15), von hinten ueber eine Leiter (ab Deck y 10) zu erreichen
        for sx in (-1, 1):
            for x in range(11, 15):
                for z in range(-19, -16):
                    for y in range(11, 16):
                        setze((sx * x, y, z), aussen=True)
        # Stuetzen unter Chaff-Gelenken, die ueber dem tieferen Heck-Deck stehen
        for p in CHAFF_GELENKE:
            q = fz.add(p, CHAFF_WEG)
            h = self.deck(q[2])
            for y in range(h + 1, q[1]):
                if (q[0], y, q[2]) not in self.teil_voxel:
                    self.teil_voxel.add((q[0], y, q[2]))
                    neu.append(block((q[0], y, q[2])))
        # Ausleger fuer die Seiten-Laser (von der Bordwand bis zum Laser)
        for sx in (-1, 1):
            for x in range(X1 + 1, SEITEN_LASER_X):
                setze((sx * x, 6, -8), aussen=True)
        # Mast-Turm
        lo, hi = MAST_TURM
        for x in range(lo[0], hi[0] + 1):
            for y in range(lo[1], hi[1] + 1):
                for z in range(lo[2], hi[2] + 1):
                    setze((x, y, z), aussen=True)
        # Arme zu den Radaren: ein Block unter jedem Radar und eine gerade Reihe bis zum Turm
        for k in range(6):
            p = self.neu["radar%d" % (k + 1)].vp
            y = p[1] - 1
            if lo[0] <= p[0] <= hi[0]:
                zs = range(p[2], lo[2]) if p[2] < lo[2] else range(hi[2] + 1, p[2] + 1)
                for z in zs:
                    setze((p[0], y, z), aussen=True)
            else:
                xs = range(p[0], lo[0]) if p[0] < lo[0] else range(hi[0] + 1, p[0] + 1)
                for x in xs:
                    setze((x, y, p[2]), aussen=True)
        self.rumpf.extend(neu)
        return len(neu)

    def leitern(self):
        """Leitern (wie im Schiff, 2 Bloecke hoch): hinten vom Boden aufs Deck, hinter der Bruecke auf die Plattform."""
        lt = vorlage(self.F, "ladder_small", (14, 3, -20))
        r = (1, 0, 0, 0, 0, -1, 0, 1, 0)          # Leiter an einer Wand, die nach -z (hinten) schaut
        # hinten: unterstes Stueck haengt vor der Heck-Schraege (Boden-Abstand), die anderen an der Heckplatte
        orte = [(-3, y, HINTEN - 1) for y in range(BODEN + 1, 10, 2)] + [(sx * 12, y, -20) for sx in (-1, 1) for y in (11, 13, 15)]
        for p in orte:
            xml = lt.xml.replace('r="0,0,1,1,0,0,0,1,0"', 'r="%s"' % rstr(r))
            self.plus(fz.Teil(xml).verschoben(fz.sub(p, lt.vp)))

    def bemalen(self):
        """Tarnanstrich (Wald, 4 Farben) auf alle Bloecke und Schraegen aller Koerper - Fenster und Bauteile bleiben."""
        farben = ["4B5320", "2F3B1E", "5C4A32", "1E1E1E"]
        wellen = [(0.11, 0.07, 0.05, 1.3), (0.05, 0.13, 0.09, 4.1), (0.08, 0.04, 0.12, 2.2), (0.15, 0.10, 0.03, 5.7)]

        def muster(p):
            # Schlamm: unten am Rumpf (Spritzer der Raeder), nach oben immer seltener, fleckig
            h = p[1] - BODEN
            if h < 6:
                k = math.sin(0.9 * p[2] + 0.3 * p[0]) * math.sin(0.37 * p[2] + 1.1 * p[1] + 0.5) * 0.5 + 0.5
                if k > h / 6:
                    return "6B5A3E" if (p[0] + p[2] + p[1]) % 3 else "4A3B28"
            v = sum(math.sin(a * p[0] + b * p[1] + c * p[2] + ph) for a, b, c, ph in wellen)
            # Summe von 4 Sinus ~ Normalverteilung (Streuung 1,41): 40 % Oliv, 30 % Dunkelgruen, 20 % Braun, 10 % Schwarz
            return farben[0 if v < -0.36 else 1 if v < 0.74 else 2 if v < 1.81 else 3]

        def neu(t):
            if t.d not in fz.STRUKTUR:
                return t
            f = muster(t.vp)
            x = re.sub(r' (bc|ac)="[0-9A-Fa-f]*"', "", t.xml, count=2)
            x = re.sub(r'<o( r="[^"]*")?', lambda m: m.group(0) + ' bc="%s" ac="%s"' % (f, f), x, count=1)
            return fz.Teil(x)

        self.rumpf = [neu(t) for t in self.rumpf]
        self.koerper = [[neu(t) for t in k] for k in self.koerper]
        # self.neu zeigt auf Bauteile (keine Bloecke) - bleibt gueltig
        self.kennung()
        self.abzeichen()

    def kennung(self, text="KL-1", z0=-12, y0=7, farbe="E6E6E6"):
        """Kennung in Blockschrift (3 x 5) auf beide Seitenwaende, von aussen lesbar."""
        schrift = {"K": ["X.X", "XX.", "X..", "XX.", "X.X"], "L": ["X..", "X..", "X..", "X..", "XXX"],
                   "-": ["...", "...", "XXX", "...", "..."], "1": [".X.", "XX.", ".X.", ".X.", "XXX"]}
        punkte = set()
        for i, ch in enumerate(text):
            for zeile, muster in enumerate(schrift[ch]):
                for sp, c in enumerate(muster):
                    if c == "X":
                        punkte.add((4 * i + sp, y0 - zeile))      # (Spalte von links, y)
        breite = 4 * len(text) - 1
        ziele = set()
        for spalte, y in punkte:
            ziele.add((X0, y, z0 - spalte))                        # links: von vorn nach hinten lesen
            ziele.add((X1, y, z0 - breite + 1 + spalte))           # rechts: von hinten nach vorn lesen
        for k, t in enumerate(self.rumpf):
            if t.vp in ziele and t.d == "block":
                x = re.sub(r' (bc|ac)="[0-9A-Fa-f]*"', "", t.xml, count=2)
                x = re.sub(r'<o( r="[^"]*")?', lambda m: m.group(0) + ' bc="%s" ac="%s"' % (farbe, farbe), x, count=1)
                self.rumpf[k] = fz.Teil(x)

    def farbe_setzen(self, ziele):
        """ziele: {Position: Farbe} - nur Bau-Bloecke des Rumpfs werden umgefaerbt."""
        for k, t in enumerate(self.rumpf):
            f = ziele.get(t.vp)
            if f and t.d == "block":
                x = re.sub(r' (bc|ac)="[0-9A-Fa-f]*"', "", t.xml, count=2)
                x = re.sub(r'<o( r="[^"]*")?', lambda m: m.group(0) + ' bc="%s" ac="%s"' % (f, f), x, count=1)
                self.rumpf[k] = fz.Teil(x)

    def abzeichen(self):
        """Nur Farbe: Lueftungsgitter (Batterie-Raum) auf dem Heckdeck und ein Abzeichen (gelber Blitz auf schwarzem
        Feld) an beiden Seiten hinter der Kennung."""
        ziele = {}
        y = self.deck(-46)
        for x in range(-6, 7):
            for z in range(-51, -40):
                rand = x in (-6, 6) or z in (-51, -41)
                ziele[(x, y, z)] = "2F3B1E" if rand else ("151515" if z % 2 == 0 else "3A3A3A")
        blitz = ["...Y.", "..Y..", ".YYY.", "..Y..", ".Y..."]
        for zeile, muster in enumerate(blitz):
            for sp, c in enumerate(muster):
                f = "E8C21A" if c == "Y" else "151515"
                yy = 7 - zeile
                ziele[(X0, yy, -32 - sp)] = f          # links: von vorn nach hinten
                ziele[(X1, yy, -36 + sp)] = f          # rechts: von hinten nach vorn (von aussen gleich herum)
        self.farbe_setzen(ziele)

    # ---------------- Chips ----------------
    def koerper_liste(self):
        """Fuer sperrprofil: Liste der Koerper als [(Art, vp)], der Rumpf zuerst."""
        return [[(t.d, t.vp) for t in k] for k in [self.rumpf] + self.koerper]

    @staticmethod
    def schiff_werte(F, name):
        """Eigenschafts-Werte des eingebauten Schiffs-Chips (dort im Spiel erprobt): {Name: Wert}."""
        for _, ts in F.koerper:
            for t in ts:
                if t.d == "microprocessor" and '<microprocessor_definition name="%s"' % name in t.xml:
                    return {n: float(v) for n, v in re.findall(r'n="([^"]*)"><pos[^>]*/><v text="([^"]*)"', t.xml)}
        return {}

    def chips_bauen(self):
        import sperrprofil
        import build_lage
        import build_flak
        import build_kanone
        import build_kamera
        import build_ki
        F = self.F
        kp = self.koerper_liste()
        sperrprofil.koerper = lambda pfad=None: kp
        build_flak.TUERME = [("L", -10, -60, 13), ("R", 10, -60, 13)]
        build_kanone.KANONEN = [("B", "BC", 1, 0, 5, 14, "Battle Cannon", "BC-Turm", True),
                                ("A", "AC", 2, 0, 31, 9, "Heavy Autocannon", "AC-Turm vorn", False)]
        port = 8768 if self.schreiber else 0
        build_lage.SCHREIBER_PROPS = [(n, port if n == "Schreiber Port" else v, d) for n, v, d in build_lage.SCHREIBER_PROPS]
        mini = schiff_lua
        src = land_lua()

        def mit(props, werte, land):
            out = []
            for n, v, d in props:
                v = werte.get(n, v)
                v = land.get(n, v)
                out.append((n, int(v) if float(v) == int(v) else v, d))
            return out

        # Flak
        flak_land = FLAK_LAND
        for seite, cx, cz, gy in build_flak.TUERME:
            prf = sperrprofil.profil(cx, cz, gy, kp)
            fl = src["flak"].replace("PRF='0'", "PRF='%s'" % ",".join(build_mc.fmt(float(v)) for v in prf))
            fl = build_lage.kopf(fl, "f%sf" % seite)
            fr = build_lage.kopf(src["flakradar"], "f%sr" % seite)
            pr = mit(build_flak.PROPS, self.schiff_werte(F, "Figet Marena Flak %s" % seite), flak_land)
            mc = build_flak.build(fr, fl, seite, src, titel="Landkreuzer Flak %s" % seite,
                                  beschr="Flak %s (Landkreuzer %s): Ziel vom Bildschirm-Chip, Turm-Radar, Vorhalt, Zeitzuender"
                                  % (seite, VERSION), props=pr)
            self.chip("Flak %s" % seite, mc)
        # Kanonen
        kan_land = KANONE_LAND
        for k, name, waffe, cx, cz, gy, gname, turm, verschluss in build_kanone.KANONEN:
            prf = sperrprofil.profil(cx, cz, gy, kp)
            fl = src["flak"].replace("PRF='0'", "PRF='%s'" % ",".join(build_mc.fmt(float(v)) for v in prf))
            fl = build_lage.kopf(fl, "k%sf" % k)
            fr = build_lage.kopf(src["flakradar"], "k%sr" % k)
            pr = mit(build_kanone.props(k), self.schiff_werte(F, "Figet Marena Kanone %s" % name), kan_land)
            mc = build_flak.build(fr, fl, k, src, titel="Landkreuzer Kanone %s" % name,
                                  beschr="Kanone %s (Landkreuzer %s): Bodenziel vom Bildschirm-Chip, Turm-Radar, Vorhalt"
                                  % (name, VERSION), waffe=waffe, props=pr, turm=turm, gname=gname,
                                  rechts=verschluss, verschluss=verschluss, zwilling=verschluss)
            self.chip("Kanone %s" % name, mc)
        # Lage (Mast-Radare): Bodenziele sind Ziele ('See Hoehe max' aus), Luft relativ zur eigenen Hoehe
        lage_land = LAGE_LAND
        build_lage.PROPS = mit(build_lage.PROPS, self.schiff_werte(F, "Figet Marena Lage"), lage_land)
        ls = {"mastradar": src["mastradar"], "lage": build_lage.kopf(src["lage"], "la"),
              "bild": build_lage.kopf(build_lage.bild_flak(src["bild"]), "ba")}
        mc = build_lage.build_lage(ls)
        mc.name, mc.desc = "Landkreuzer Lage", "Lage (Landkreuzer %s): 6 Mast-Radare, Luft-/Bodenziele, Bedrohung" % VERSION
        self.chip("Lage", mc)
        mc = build_lage.build_bild(ls)
        mc.name = "Landkreuzer Bildschirm"
        mc.desc = "Bildschirm (Landkreuzer %s): 3D-Radar | Kamera | Zielliste; Waffen waehlen Ziele selbst" % VERSION
        self.chip("Bildschirm", mc)
        # Dachkamera
        cam, phys = self.neu["kamera"].vp, self.neu["phys"].vp
        assert cam[0] == phys[0], "Kamera und Physik-Sensor muessen auf der Mittellinie liegen"
        kam_land = {"Kamera vor Physik m": (cam[2] - phys[2]) * .25, "Kamera ueber Physik m": (cam[1] - phys[1]) * .25,
                    "Ziel See m": 10}
        build_kamera.PROPS = mit(build_kamera.PROPS, self.schiff_werte(F, "Figet Marena Kamera"), kam_land)
        mc = build_kamera.build(build_lage.kopf(src["kamera"], "ka"))
        mc.name = "Landkreuzer Kamera"
        mc.desc = "Kamera (Landkreuzer %s): Dachkamera schaut auf das Ziel der gewaehlten Waffe, Zoom" % VERSION
        self.chip("Kamera", mc)
        # Schutz (Auto-Chaff; Pumpen gibt es an Land nicht): Schalter kommen vom KI-Chip ('Schutz': Bool 3 = Waffen frei)
        import build_schutz
        src["schutz"] = mini("schutz")
        mc = build_schutz.build(build_lage.kopf(src["schutz"], "sc"))
        mc.name, mc.desc = "Landkreuzer Schutz", "Schutz (Landkreuzer %s): Auto-Chaff, wenn die Waffen frei sind" % VERSION
        self.chip("Schutz", mc)
        # KI
        self.chip("KI", build_ki.build())
        for name, (mc, t) in self.chips.items():
            assert len(mc.desc) <= 128, (name, len(mc.desc))

    def chip(self, name, mc):
        x, z = CHIP_PLATZ[name]
        vp = (x, CHIP_Y, z)
        xml = '<c d="microprocessor"><o r="1,0,0,0,1,0,0,0,1" sc="%d">%s%s%s</o></c>' % (
            chip_sc(mc.width, mc.length), mc.embedded(), fz.vox("vp", vp), mc.slots())
        t = fz.Teil(xml)
        self.plus(t)
        self.chips[name] = (mc, t)
        for fx in range(mc.width):
            for fzz in range(mc.length):
                self.teil_voxel.add((x + fx, CHIP_Y, z + fzz))

    def knoten(self, chip, label):
        """Weltposition eines Chip-Anschlusses im Landkreuzer."""
        mc, t = self.chips[chip]
        for lab, mode, typ, fx, fzz in mc.node_liste():
            if lab == label:
                return (t.vp[0] + fx, t.vp[1], t.vp[2] + fzz)
        raise KeyError((chip, label))

    # ---------------- Kabel ----------------
    def kabel_bauen(self):
        F = self.F
        # Schiffs-Chip-Anschluesse: (Position, Typ, mode) -> (Chip, Label)
        sch = {}
        for name, nodes in F.chip_anschluesse().items():
            for lab, mode, typ, w in nodes:
                sch[(w, typ, mode)] = (name, lab)
        # Schiffs-Teile (ohne Bloecke, ohne Chips) fuer "zu welchem Teil gehoert dieser Kabel-Anschluss?"
        gitter = {}
        for bi, (_, ts) in enumerate(F.koerper):
            for t in ts:
                if t.d in fz.STRUKTUR or t.d == "microprocessor":
                    continue
                gitter.setdefault(tuple(v // 4 for v in t.vp), []).append((bi, t))

        def teil_bei(p):
            best = None
            g = tuple(v // 4 for v in p)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        for bi, t in gitter.get((g[0] + dx, g[1] + dy, g[2] + dz), []):
                            d = max(abs(t.vp[i] - p[i]) for i in range(3))
                            if d <= 3:
                                k = (d, 0 if (bi, t.vp) in self.weg else 1)
                                if best is None or k < best[0]:
                                    best = (k, bi, t)
            return best

        bat = self.batterie_knoten(0)

        def abbilden(p, typ, mode):
            n = sch.get((p, typ, mode))
            if n:
                neu = CHIP_NAMEN.get(n[0])
                return self.knoten(neu, n[1]) if neu else None
            if typ == 4 and p in SCHIFF_STROM:
                return bat
            b = teil_bei(p)
            if b and (b[1], b[2].vp) in self.weg:
                return fz.add(p, self.weg[(b[1], b[2].vp)])
            return None

        alt = 0
        for typ, a, b in F.kabel:
            if sch.get((b, typ, 1)) in NEU_VERKABELT:
                continue
            na, nb = abbilden(a, typ, 0), abbilden(b, typ, 1)
            if na is not None and nb is not None and na != nb:
                self.kabel.append((typ, na, nb))
                alt += 1
        # --- neue Kabel ---
        neu = []
        # Batterien zusammen
        for k in range(1, len(self.batterien)):
            neu.append((4, self.batterie_knoten(k), bat))
        # Motoren: Strom (Anschluss eins ueber vp) und Gas (vp) vom KI-Chip
        for seite, label in (("L", "Links"), ("R", "Rechts")):
            for m in self.motoren[seite]:
                neu.append((4, bat, fz.add(m.vp, (0, 1, 0))))
                neu.append((1, self.knoten("KI", label), m.vp))
        # Lenk-Variante: Gelenke (Strom, Winkel vom KI-Chip), Gelenk-Motoren (Strom, Gas fest 1)
        for wo, a, gm in self.lenk:
            neu.append((4, bat, a.vp))
            neu.append((1, self.knoten("KI", "Lenkung " + wo), a.vp))
            neu.append((4, bat, gm.vp))
            neu.append((1, self.neu["k_lenkmotor"].vp, gm.vp))
        # Laser: Strom und Entfernung (alle Anschluesse am einzigen Block des Lasers)
        for name, t in self.laser_teile:
            neu.append((4, bat, t.vp))
            neu.append((1, t.vp, self.knoten("KI", name)))
        # Ladestand der ersten Batterie (Annahme: am Strom-Anschluss oben; fehlt er, liest die KI 0 = unbekannt)
        neu.append((1, bat, self.knoten("KI", "Batterie")))
        # KI-Chip
        phys = self.neu["phys"].vp
        neu.append((5, phys, self.knoten("KI", "Physik-Sensor")))
        neu.append((5, fz.add(self.neu["sitz"].vp, (0, 0, 1)), self.knoten("KI", "Sitz")))
        neu.append((5, self.neu["instrumente"].vp, self.knoten("KI", "Instrumente")))
        neu.append((5, self.knoten("Bildschirm", "Bedienung"), self.knoten("KI", "Bedienung")))
        neu.append((5, self.neu["karte"].vp, self.knoten("KI", "Karte Touch")))
        neu.append((6, self.knoten("KI", "Karte"), self.neu["karte"].vp))
        neu.append((6, self.knoten("KI", "Status"), self.neu["wahlmonitor"].vp))
        # Helm (Headset Video des Sitzes; im Schiff kam dort die Schiffsfuehrung an, Sitz (0,17,-10) + (1,4,0))
        neu.append((6, self.knoten("KI", "Status"), fz.add(self.neu["sitz"].vp, (1, 4, 0))))
        neu.append((5, self.knoten("KI", "Wahl"), self.knoten("Bildschirm", "Wahl")))
        neu.append((5, self.knoten("KI", "Schutz"), self.knoten("Schutz", "Instrumente")))
        # Lage: Radar 6 (im Schiff an den Raketen-Chip vergeben) wieder an den Lage-Chip
        neu.append((5, self.neu["radar6"].vp, self.knoten("Lage", "Radar 6")))
        for k in neu:
            if k not in self.kabel:
                self.kabel.append(k)
        # Doppelte weg, Eingaenge pruefen (ein Eingang hat hoechstens ein Kabel seiner Art - ausser Strom)
        rein, doppelt = [], set()
        for k in self.kabel:
            if k in doppelt:
                continue
            doppelt.add(k)
            rein.append(k)
        self.kabel = rein
        ein = {}
        for typ, a, b in self.kabel:
            if typ != 4:
                ein.setdefault((typ, b), []).append(a)
        mehr = {k: v for k, v in ein.items() if len(v) > 1}
        if mehr:
            self.meldungen.append("Eingaenge mit mehreren Kabeln: %s" % list(mehr.items())[:5])
        return alt, len(neu)

    # ---------------- Ausgabe ----------------
    def text(self):
        koerper = [('<body unique_id="%d">' % (k + 1), teile) for k, teile in enumerate([self.rumpf] + self.koerper)]
        kopf = ('<?xml version="1.0" encoding="UTF-8"?><vehicle data_version="3" bodies_id="%d">'
                '<editor_placement_offset/><authors/>' % len(koerper))
        return fz.schreiben(kopf, koerper, self.kabel)

    def pruefen(self, txt):
        """Grobe Pruefungen: Datei liest sich wieder, keine zwei Teile auf demselben Platz im selben Koerper."""
        G = fz.Fahrzeug(txt)
        for bi, (_, ts) in enumerate(G.koerper):
            pos = {}
            for t in ts:
                if t.d.startswith("multibody"):
                    continue
                pos.setdefault(t.vp, []).append(t.d)
            dop = {p: d for p, d in pos.items() if len(d) > 1}
            if dop:
                self.meldungen.append("Koerper %d: %d Plaetze doppelt belegt, z. B. %s" % (bi, len(dop), list(dop.items())[:3]))
        return G


def main():
    lenkung = "--lenkung" in sys.argv
    b = Bau(schreiber="--schreiber" in sys.argv, lenkung=lenkung)
    b.module()
    b.einzel()
    b.chaff()
    b.fahrwerk()
    b.laser()
    n = b.rumpf_bauen()
    b.leitern()
    b.bemalen()
    b.chips_bauen()
    alt, neu = b.kabel_bauen()
    txt = b.text()
    G = b.pruefen(txt)
    import pruefen
    fehler, _ = pruefen.pruefe(txt, b.F)
    aus_datei = AUS_DATEI.replace(".xml", " Lenkung.xml") if lenkung else AUS_DATEI
    os.makedirs(os.path.dirname(aus_datei), exist_ok=True)
    with open(aus_datei, "w", encoding="utf-8", newline="") as f:
        f.write(txt)
    teile = sum(len(ts) for _, ts in G.koerper)
    print("KI Landkreuzer %s: %d Koerper, %d Teile (davon %d neue Rumpf-Bloecke), %d Kabel (%d aus dem Schiff, %d neu)"
          % (VERSION, len(G.koerper), teile, n, len(G.kabel), alt, neu))
    print("Chips:", ", ".join("%s %dx%d" % (k, m.width, m.length) for k, (m, _) in b.chips.items()))
    print("Rad-Stummel:", len(b.stummel), "(davon %d gelenkt)" % (len(b.lenk)), " Datei:", aus_datei, "(%d KB)" % (len(txt) // 1024))
    for m in b.meldungen:
        print("HINWEIS:", m)
    if fehler:
        sys.exit("Pruefung mit Fehlern - Datei trotzdem geschrieben")


if __name__ == "__main__":
    main()
