"""Baut den Flugcomputer-Microcontroller fuer Stormworks.

- verkleinert lua/*.lua (Kommentare und Einrueckung raus) nach build/*.min.lua
- erzeugt build/<MC_FILE> und build/<MC_FILE_W>
- dazu die englische Fassung build/<MC_FILE_EN> und build/<MC_FILE_W_EN> (tools/english.py, gleiche Anschluesse)
- mit --install zusaetzlich nach %APPDATA%/Stormworks/data/microprocessors kopieren
"""
import os
import shutil
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import english  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LUA_DIR = os.path.join(ROOT, "lua")
BUILD = os.path.join(ROOT, "build")
LUA_LIMIT = 8192          # Stormworks: 8192 Zeichen je Lua-Skript (bis 02.10. faelschlich mit 4096 gerechnet)
MC_FILE = "Flugpanzer Hover v4.0.xml"
MC_FILE_EN = "Swifter Hover EN v4.0.xml"

# Name, Standardwert, Erklaerung (Reihenfolge = Reihenfolge im Eigenschaften-Fenster)
PROPS = [
    ("Duese Grad pro 1", 180, "Wie viel Grad sich die Duese bei Wert 1 dreht (laut Spiel 0.5 Umdrehungen)"),
    ("Duese links Richtung", 1, "1 oder -1: Drehrichtung der linken Duesen"),
    ("Duese rechts Richtung", 1, "1 oder -1: Drehrichtung der rechten Duesen"),
    ("Max Tempo kmh", 300, "Hoechste einstellbare Fluggeschwindigkeit"),
    ("Max Duesenwinkel", 40, "Wie weit die Duesen fuer Vorwaertsflug nach hinten drehen duerfen (mehr = schneller, aber ab ca. 45 Grad kippt der Duesenschub die Nase, wenn die Duesen tief unter dem Schwerpunkt sitzen)"),
    ("Schwebe-Schub", 0.5, "Startwert: Anteil Schub zum Schweben (lernt sich selbst, das Gas haelt ihn bei 0.5)"),
    ("Lage P", 3, "Lageregler: Staerke"),
    ("Lage D", 3, "Lageregler: Daempfung"),
    ("Lage I", 4, "Lageregler: gleicht Schwerpunkt-Fehler aus"),
    ("Steig P", 0.06, "Hoehenregler: Staerke"),
    ("Steig I", 0.05, "Hoehenregler: Lernrate Schwebe-Schub"),
    ("Tempo P", 2, "Geschwindigkeitsregler: Grad Duese pro m/s Abweichung"),
    ("Tempo I", 0.5, "Geschwindigkeitsregler: Nachfuehrung"),
    ("Gier P", 150, "Drehregler (Hochachse)"),
    ("Jet Anlaufzeit s", 8, "Wartezeit nach dem Jet-Start bis zum Abheben"),
    ("Jet Gas Start", 0.5, "Jet-Gas beim Anlassen und Abheben (danach regelt der Chip)"),
    ("Jet Gas min", 0.15, "Kleinstes Jet-Gas im Flug, damit die Jets nicht ausgehen"),
    ("Jet Gas max", 1, "Groesstes Jet-Gas im Flug"),
    ("Gas Tempo", 2, "Wie viel Prozent pro Sekunde der Chip das Jet-Gas im Flug hoechstens aendert (Jets reagieren traege)"),
    ("Schub per Duesen", 0, "1 = Schub nach oben ueber Duesen-Spreizung regeln (wenn die Schubklappen kaum wirken)"),
    ("Schwebehoehe m", 3, "Gleithoehe ueber Grund nach dem Start (Pfeil hoch/runter aendert sie)"),
    ("Voraus-Laser Winkel", 0, "Neigung des Voraus-Lasers nach unten in Grad (0 = genau geradeaus)"),
    ("Kompass umkehren", 0, "0 oder 1: wenn KURS beim Rechtsdrehen faellt"),
    ("Nick umkehren", 0, "0 oder 1: wenn NICK bergauf negativ ist"),
    ("Roll umkehren", 0, "0 oder 1: wenn ROLL bei rechter Seite unten negativ ist"),
]

# Voreinstellungen fuer Andres Fahrzeug (aus seinen Tests), ueberschreiben die Standardwerte oben.
# Der Simulator nutzt weiter PROPS, weil er die Duesen physikalisch richtig herum annimmt.
USER_VALUES = {
    "Duese links Richtung": -1,   # Duesentest zeigte nach vorn
    "Duese rechts Richtung": -1,
    "Schwebehoehe m": 1.5,        # Erstflug, danach auf 3
    # "Kompass umkehren" bleibt 0: mit 1 drehte er sich im Flug, mit 0 stabil (Test 2026-09-24)
    "Jet Gas Start": 0.35,        # Schubtest: hebt mit offenen Klappen bei 29 % Gas ab
    "Jet Gas max": 0.8,           # 0.6 gegen das 100-dann-5-Problem; mit Turm (schwerer) sank er bei Hoechsttempo -> 0.8
    "Jet Gas min": 0.05,          # mit 0.15 konnte er den Schub nicht weit genug senken (stieg auf 100 m, kippte)
    # "Schub per Duesen" bleibt 0: im Simulator bei so starken Jets instabil, erst Schubtest auswerten
}


def minify(src, drop_local=False):
    """Entfernt Kommentare, Einrueckung und Leerzeilen. Strings bleiben unberuehrt.
    drop_local: 'local ' vor Zuweisungen weglassen und reine Deklarationen streichen (spart Zeichen;
    nur fuer Skripte ohne gleichnamige Variablen in verschiedenen Bereichen, wie flug.lua)."""
    out, i, n, quote = [], 0, len(src), None
    while i < n:
        ch = src[i]
        if quote:
            out.append(ch)
            if ch == "\\":
                out.append(src[i + 1])
                i += 1
            elif ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
            out.append(ch)
        elif src.startswith("--", i):
            while i < n and src[i] != "\n":
                i += 1
            continue
        else:
            out.append(ch)
        i += 1
    lines = [ln.strip() for ln in "".join(out).splitlines()]
    if drop_local:
        kept = []
        for ln in lines:
            if ln.startswith("local "):
                if "=" not in ln:
                    continue
                ln = ln[6:]
            kept.append(ln)
        lines = kept
    return "\n".join(ln for ln in lines if ln)


def fmt(v):
    return ("%g" % v) if isinstance(v, float) else str(v)


class MC:
    def __init__(self, name, desc, width, length):
        self.name, self.desc, self.width, self.length = name, desc, width, length
        self.nodes, self.comps, self.bridges = [], [], []
        self.late = []
        self.next_id = 1

    def _add(self, lst, ctype, attrs, links, pos, extra=""):
        cid = self.next_id
        self.next_id += 1
        lst.append((ctype, cid, attrs, links, pos, extra))
        return cid

    def comp(self, ctype, pos, attrs=None, links=None, extra=""):
        return self._add(self.comps, ctype, attrs or {}, links or [], pos, extra)

    def node(self, label, mode, ntype, desc, x, z, pos, link=None, late=False):
        # mode 1 = Eingang, 0 = Ausgang. Brueckentyp je nach Signalart.
        # late: Anschluss kommt ans Ende der Liste (neue Anschluesse, damit die Kabel der alten beim Ueberschreiben bleiben)
        btype = {(0, 1): 0, (0, 0): 1, (1, 1): 2, (1, 0): 3,
                 (5, 1): 4, (5, 0): 5, (6, 1): 6, (6, 0): 7}[(ntype, mode)]
        cid = self._add(self.bridges, btype, {}, [link] if link else [], pos)
        (self.late if late else self.nodes).append((cid, label, mode, ntype, desc, x, z))
        return cid

    @staticmethod
    def _inner(cid, attrs, links, pos, extra):
        a = "".join(' %s="%s"' % (k, escape(str(v), {'"': "&quot;"})) for k, v in attrs.items())
        body = '<pos x="%s" y="%s"/>' % pos
        idx = 0
        for link in links:
            # Link ist (quelle, node_index) oder ("inc", (quelle, node_index)) fuer den Composite-Basiseingang
            if isinstance(link[0], str):
                tag, (src, node_index) = link
            else:
                idx += 1
                tag, (src, node_index) = "in%d" % idx, link
            ni = ' node_index="%d"' % node_index if node_index else ""
            body += '<%s component_id="%d"%s/>' % (tag, src, ni)
        return ' id="%d"%s>%s%s' % (cid, a, body, extra)

    def xml(self):
        x = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<microprocessor name="%s" description="%s" width="%d" length="%d" id_counter="%d" id_counter_node="%d">'
             % (escape(self.name), escape(self.desc), self.width, self.length, self.next_id - 1,
                len(self.nodes) + len(self.late)),
             "\t<nodes>"]
        for nid, (cid, label, mode, ntype, desc, nx, nz) in enumerate(self.nodes + self.late, 1):
            x.append('\t\t<n id="%d" component_id="%d"><node label="%s" mode="%d" type="%d" description="%s">'
                     '<position x="%d" y="0" z="%d"/></node></n>'
                     % (nid, cid, escape(label), mode, ntype, escape(desc, {'"': "&quot;"}), nx, nz))
        x += ["\t</nodes>", "\t<group>", "\t\t<data><inputs/><outputs/></data>", "\t\t<components>"]
        for ctype, cid, attrs, links, pos, extra in self.comps:
            x.append('\t\t\t<c type="%d"><object%s</object></c>' % (ctype, self._inner(cid, attrs, links, pos, extra)))
        x += ["\t\t</components>", "\t\t<components_bridge>"]
        for ctype, cid, attrs, links, pos, extra in self.bridges:
            x.append('\t\t\t<c type="%d"><object%s</object></c>' % (ctype, self._inner(cid, attrs, links, pos, extra)))
        x += ["\t\t</components_bridge>", "\t\t<groups/>", "\t\t<component_states>"]
        for i, (ctype, cid, attrs, links, pos, extra) in enumerate(self.comps):
            x.append("\t\t\t<c%d%s</c%d>" % (i, self._inner(cid, attrs, links, pos, extra), i))
        x += ["\t\t</component_states>", "\t\t<component_bridge_states>"]
        for i, (ctype, cid, attrs, links, pos, extra) in enumerate(self.bridges):
            x.append("\t\t\t<c%d%s</c%d>" % (i, self._inner(cid, attrs, links, pos, extra), i))
        x += ["\t\t</component_bridge_states>", "\t\t<group_states/>", "\t</group>", "</microprocessor>", ""]
        return "\n".join(x)


def build_flight_mc(flug_src, mix_src, hud_src):
    # Das Spiel speichert hoechstens 128 Zeichen Beschreibung
    mc = MC("Hover-Flugcomputer", "Flugpanzer Hover v4.0: Jet-Start, Gas, Gleiten ueber Grund/Wasser, Flug, Landung, HUD, Parkbremse. "
            "H1 Start/Landen, H2 Stopp", 3, 6)

    sitz = mc.node("Sitz", 1, 5, "Sitz: Ausgang 'Seat data' anschliessen", 0, 0, (-8, 4))
    phys = mc.node("Physik-Sensor", 1, 5, "Physik-Sensor (mittig, Pfeil nach vorn)", 1, 0, (-8, 2))
    laser = mc.node("Boden-Laser", 1, 1, "Laser Distance Sensor, zeigt senkrecht nach unten", 2, 0, (-8, 0))
    ahead = mc.node("Voraus-Laser", 1, 1, "Laser Distance Sensor ganz vorn, zeigt genau geradeaus", 2, 1, (-8, -1))

    # Sitzwerte aus dem Sitz-Composite lesen
    seat_num = [mc.comp(31, (-5, 6 - k), {"i": i} if i else {}, [(sitz, 0)]) for k, i in enumerate([0, 1, 2, 3, 8, 9])]
    seat_bool = [mc.comp(29, (-5, -1 - k), {"i": i} if i else {}, [(sitz, 0)]) for k, i in enumerate([0, 1, 2, 3, 4, 5, 30, 31])]

    # Physik-Composite + Sitz-Zahlen (Kanal 20-25) + Boden-Laser (26) + Voraus-Laser (27)
    wnum = mc.comp(40, (-2, 3), {"count": 8, "offset": 19},
                   [("inc", (phys, 0))] + [(c, 0) for c in seat_num] + [(laser, 0), (ahead, 0)])
    # + Sitz-Knoepfe (Bool 1-8)
    wbool = mc.comp(41, (-2, -2), {"count": 8}, [("inc", (wnum, 0))] + [(c, 0) for c in seat_bool])

    # Flug-Logik -> Schubverteilung/Gas -> HUD
    flug = mc.comp(56, (1, 1), {"script": flug_src}, [(wbool, 0)])
    mix = mc.comp(56, (3, 1), {"script": mix_src}, [(flug, 0)])
    hud = mc.comp(56, (4, -4), {"script": hud_src}, [(mix, 0)])

    for k, (name, val, desc) in enumerate(PROPS):
        val = USER_VALUES.get(name, val)
        mc.comp(34, (-8 - 2 * (k // 8), -6 - (k % 8)), {"n": name},
                extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))

    outs = [("Klappe VL", 0, 0, 1, "Schubklappe (Thrust Spoiler) Duese vorne links"),
            ("Klappe VR", 1, 1, 1, "Schubklappe Duese vorne rechts"),
            ("Klappe HL", 2, 0, 2, "Schubklappe Duese hinten links"),
            ("Klappe HR", 3, 1, 2, "Schubklappe Duese hinten rechts"),
            ("Duese VL", 4, 0, 3, "Rotation Target Duese vorne links"),
            ("Duese VR", 5, 1, 3, "Rotation Target Duese vorne rechts"),
            ("Duese HL", 6, 0, 4, "Rotation Target Duese hinten links"),
            ("Duese HR", 7, 1, 4, "Rotation Target Duese hinten rechts"),
            ("Jet Gas", 8, 2, 2, "Throttle aller 4 Brennkammern")]
    for k, (label, ch, nx, nz, desc) in enumerate(outs):
        rd = mc.comp(31, (5, 5 - k), {"i": ch} if ch else {}, [(mix, 0)])
        mc.node(label, 0, 1, desc, nx, nz, (8, 5 - k), (rd, 0))
    jr = mc.comp(29, (5, -7), {}, [(mix, 0)])
    mc.node("Jets An", 0, 0, "Compressor aller 4 Jets", 2, 3, (8, -7), (jr, 0))
    mc.node("HUD", 0, 6, "Helm-Display (Headset Video am Sitz) oder Monitor", 0, 5, (8, -9), (hud, 1))
    mc.node("Flugdaten", 0, 5, "Alle Werte fuer spaetere Waffen-Chips", 1, 5, (8, -10), (mix, 0))
    # neu in v4.0 (Workshop-Wunsch): Parkbremse, Mix Bool 2; letzter Anschluss, damit die alten ihre Nummer behalten
    br = mc.comp(29, (5, -8), {"i": 1}, [(mix, 0)])
    mc.node("Bremse", 0, 0, "Wheel Coaster: Brake (alle 4) - an im Stand und beim Jet-Start", 2, 4, (8, -8), (br, 0), late=True)
    return mc


MC_FILE_W = "Flugpanzer Waffen v25.xml"
MC_FILE_W_EN = "Swifter Weapons EN v25.xml"

# Waffen-Chip: Name, Standardwert, Erklaerung
PROPS_W = [
    ("Blick X Richtung", 1, "1, wenn BLICK x beim Blick nach rechts groesser wird, sonst -1 (dann auch Turm Richtung umdrehen)"),
    ("Blick Y Richtung", 1, "1, wenn BLICK y beim Blick nach oben groesser wird, sonst -1 (dann auch Kanone Hoehe Richtung umdrehen)"),
    ("Monitor Mitte X Grad", 0, "BLICK x, wenn du auf das Fadenkreuz in der Monitormitte schaust"),
    ("Monitor Mitte Y Grad", 0, "BLICK y, wenn du auf das Fadenkreuz in der Monitormitte schaust"),
    ("Totzone Grad", 0.2, "So weit darfst du neben das Fadenkreuz schauen, ohne dass sich etwas bewegt (groesser = ruhiger, aber ungenauer)"),
    ("Turm Richtung", 1, "1 oder -1: wenn der Turm beim Blick nach rechts nach links dreht"),
    ("Turm Tempo", 10, "Wie schnell der Turm dreht, wenn du neben das Fadenkreuz schaust"),
    ("Turm Grenze Grad", 50, "Turm dreht hoechstens so weit nach links und rechts (von vorn gemessen)"),
    ("Hoehe Tempo", 1.5, "Wie schnell das Ziel hoch/runter faehrt (Grad pro Sekunde je Grad Blick neben das Fadenkreuz)"),
    ("Kanone Hoehe Richtung", 1, "1 oder -1: wenn das Rohr hoch geht, obwohl das Ziel runter geht"),
    ("Kanone Hoehe Null Grad", 0, "Korrektur, falls die Kanone bei Wert 0 nicht waagerecht steht"),
    ("Kanone tiefster Winkel Grad", 0, "Rohr nie tiefer als das (0 = wie gebaut; mit Rohr-Test ausmessen)"),
    ("Kanone hoechster Winkel Grad", 10, "Rohr nie hoeher als das (mit Rohr-Test ausmessen)"),
    ("Kanone v0", 800, "Muendungsgeschwindigkeit m/s (beim Einschiessen anpassen)"),
    ("Kanone Drag", 0.002, "Luftwiderstand pro Tick"),
    ("Geschoss g", 30, "Schwerkraft fuer Geschosse im Spiel (m/s2)"),
    ("Kamera ueber Kanone m", 1, "Wie hoch die Zielkamera ueber der Kanonenachse sitzt"),
    ("Visier Richtung", 1, "1 oder -1: wenn das Kamerabild beim Rohr-Test andersherum laeuft als das Rohr"),
    ("Visier Null Grad", 0, "Korrektur, falls die Kamera bei Pivot 0 nicht parallel zum Rohr schaut (Einschiessen auf 100-200 m)"),
    ("Kamera Sicht", 0.5, "Field of View ohne Zoom (0 = weit, 1 = Tele)"),
    ("Zoom Stufe 2", 0.82, "Field of View Zoom-Stufe 2 (Hotkey 4), etwa 3-fach"),
    ("Zoom Stufe 3", 0.94, "Field of View Zoom-Stufe 3 (Hotkey 4 nochmal), etwa 8-fach"),
    ("Zoom Stufe 4", 0.976, "Field of View Zoom-Stufe 4 (Hotkey 4 nochmal), etwa 16-fach (1 = 50-fach)"),
    ("Monitor kopfueber", 0, "1, wenn der Monitor um 180 Grad gedreht eingebaut ist (Zahlen stehen sonst auf dem Kopf)"),
    ("Eigenbewegung", 1, "1 = eigene Bewegung (vor/zurueck, steigen) beim Zielen einrechnen"),
    ("Lader Zeit s", 3.6, "So lange bleibt der Verschluss offen (Feeder schiebt ab 1 s), dann zu und 2 s auf Loaded warten"),
    ("Zuender Luft", 0, "1 = HE zuendet in der gemessenen Entfernung (Luftsprengung), 0 = beim Aufschlag"),
    ("AA Turm Richtung", 1, "1 oder -1: Flugabwehr-Turm dreht vom Ziel weg statt hin"),
    ("AA Turm Tempo", 10, "Wie kraeftig der Flugabwehr-Turm Zielfehler ausgleicht (kleiner = ruhiger, groesser = schneller)"),
    ("AA Turm Bremsen", 0.3, "Wie schnell der Flugabwehr-Drehkranz abbremsen kann (U/s pro s). Schiesst der Turm ueber das Ziel hinaus und pendelt: kleiner. Kommt er zu zaghaft an: groesser"),
    ("AA Hoehe Richtung", 1, "1 oder -1: Flugabwehr-Rohr geht falsch herum hoch/runter"),
    ("AA Radar Richtung", 1, "1 oder -1: Seitenwinkel vom Radar falsch herum"),
    ("AA Radar Hoehe Richtung", 1, "1 oder -1: Hoehenwinkel vom Radar falsch herum"),
    ("AA Radar auf Turm", 1, "1 = das Radar sitzt auf dem Flak-Turm und dreht mit, 0 = fest auf dem Panzer"),
    ("AA Radar Null Grad", 0, "Wohin die Vorderseite des Radars zeigt (0 = wie das Flak-Rohr bzw. nach vorn, 180 = nach hinten)"),
    ("AA Turm Null Grad", 0, "Wohin das Flak-Rohr bei Turmdrehung 0 zeigt (0 = nach vorn, 180 = nach hinten)"),
    ("AA Suchtempo", 0.25, "So schnell dreht der Radarschirm beim Suchen (Umdrehungen pro Sekunde)"),
    ("AA Suchhoehe Grad", 10, "So weit nach oben schaut der Radarschirm beim Suchen"),
    ("AA tiefster Winkel Grad", 0, "Flak-Rohr nie flacher als das (zur Seite und nach hinten)"),
    ("AA vorne tiefster Winkel Grad", 12, "Flak-Rohr nach vorn nie flacher als das (sonst trifft es den eigenen Hauptturm)"),
    ("AA vorne Sektor Grad", 30, "So weit links und rechts vom Bug gilt der vordere Mindestwinkel"),
    ("AA Radar ueber Rohr m", 1, "So viele Meter sitzt das Radar ueber den Flak-Rohren"),
    ("AA Streuung m", 2, "Streumuster: groesster Abstand der Spiralen vom Ziel, am Ziel gemessen (0 = genau auf den Zielpunkt)"),
    ("AA v0", 1000, "Muendungsgeschwindigkeit Light Autocannon m/s"),
    ("AA Drag", 0.02, "Luftwiderstand pro Tick Light Autocannon"),
    ("AA Reichweite m", 800, "Bis zu dieser Entfernung schiesst die Flugabwehr"),
    ("AA Verfolgen bis m", 1500, "Bis zu dieser Entfernung dreht die Flugabwehr schon zum Ziel (ohne zu schiessen)"),
    ("AA Mindesthoehe m", 15, "Nur Ziele, die so hoch ueber dem Boden sind (keine Bodenfahrzeuge)"),
    ("AA Toleranz Grad", 1, "Flugabwehr feuert nur, wenn so genau ausgerichtet"),
    ("AA Schuss pro Rohr", 1400, "Munition je Flak-Rohr beim Start; der Chip zieht jeden Schuss ab (Eingang 'AA Geladen'). 0 = Trommel-Eingang 'AA Munition' anzeigen"),
    ("AA Toleranz m", 3, "Nahe Ziele: Flugabwehr feuert schon, wenn sie am Ziel hoechstens so viele Meter daneben zeigt"),
    ("AA Nahbereich m", 150, "So nah zaehlt jedes Objekt hoeher als 'AA Mindesthoehe m' als Luftziel, auch wenn es langsam und flach ist (schwebender Hubschrauber)"),
    ("Flares nach s", 1, "Flares erst, wenn uns ein Radar so lange ununterbrochen erfasst (Such-Radar streicht nur kurz vorbei)"),
]
USER_VALUES_W = {
    # Andres Tests v1/v1.1: mit allen Richtungen 1 liefen links/rechts und hoch/runter verkehrt herum.
    # Blick bleibt 1 (wird im Einrichten mit BLICK geprueft), dafuer Turm und Rohr umgedreht.
    "Turm Richtung": -1,
    "Kanone Hoehe Richtung": -1,
    # Test v3: beim Blick aufs Fadenkreuz zeigte BLICK -17.6 -19.3 (Monitor links unten -> Blick zaehlt normal herum)
    "Monitor Mitte X Grad": -17.6,
    "Monitor Mitte Y Grad": -19.3,
    # Rohr-Test v4: sicher von -5.4 bis +11.7 Grad, je 1 Grad Abstand
    "Monitor kopfueber": 1,               # Andre (2026-09-26): Zoom und Entfernung im Monitor standen auf dem Kopf
    "Kanone tiefster Winkel Grad": -7.5,    # Andre (2026-09-26): -7.5 geht noch (Rechnung aus Bild: geradeaus ca. -10, seitlich ca. -6..-8)
    "Kanone hoechster Winkel Grad": 10.7,
    # Test v12: Flak-Turm drehte hin und her, Einzelschuesse -> Drehkranz zaehlt wie der Hauptturm andersherum
    "AA Turm Richtung": -1,
}


def build_weapons_mc(w_src, a_src, h1_src, h2_src, h3_src, r_src):
    # Das Spiel speichert hoechstens 128 Zeichen Beschreibung. Bedienung: Abzug = Kanone, Hotkey 4 = Zoom (4 Stufen),
    # Hotkey 5 = Waermebild (1 s halten: Zielen aus/an), Hotkey 6 = Flugabwehr an/aus
    mc = MC("Waffen-Computer", "Flugpanzer Waffen v25: Zielen per Blick am Monitor, Battle Cannon mit Autolader und Flugbahn, "
            "Radar-Flak, Radarwarner, Flares", 6, 6)
    # Eingaenge (Reihen 0 und 1 des Chips)
    sitz = mc.node("Sitz", 1, 5, "Sitz: Ausgang 'Seat data'", 0, 0, (-12, 8))
    flugd = mc.node("Flugdaten", 1, 5, "Flug-Chip: Ausgang 'Flugdaten'", 1, 0, (-12, 6))
    vid = mc.node("Video rein", 1, 6, "Camera Medium: Camera Feed (Bild fuer den Monitor)", 2, 0, (-12, 4))
    kent = mc.node("Kamera Entfernung", 1, 1, "Laser Distance Sensor: Distance", 3, 0, (-12, 3))
    kziel = mc.node("Kamera Ziel", 1, 5, "Zielkamera: Composite Output (seit v2 unbenutzt, darf dran bleiben)", 4, 0, (-12, 2))
    turm = mc.node("Turm Drehung", 1, 1, "Turret Ring (Large): Current Rotation", 5, 0, (-12, 1))
    gel = mc.node("Kanone geladen", 1, 0, "Battle Cannon: Loaded", 0, 1, (-12, 0))
    voll = mc.node("Lader voll", 1, 0, "Battle Cannon Belt (Feeder): Contains Ammo", 1, 1, (-12, -1))
    radar = mc.node("AA Radar", 1, 5, "Radar (Phalanx): Radar Data", 2, 1, (-12, -3))
    aarot = mc.node("AA Drehung", 1, 1, "Turret Ring (Small): Current Rotation", 3, 1, (-12, -4))
    aamun = mc.node("AA Munition", 1, 1, "Flugabwehr-Trommel: Ammo Count", 4, 1, (-12, -5))
    warn = mc.node("Radarwarner", 1, 0, "Radar Detector: Detected", 5, 1, (-12, -6))

    # Sitz: Blick X/Y, Abzug, Hotkeys 4-6, besetzt
    rd = lambda src, i, pos, t=31: mc.comp(t, pos, {"i": i} if i else {}, [(src, 0)])
    lookx, looky = rd(sitz, 8, (-9, 9)), rd(sitz, 9, (-9, 8))
    trig, hk4, hk5, hk6, occ = (rd(sitz, 30, (-9, 7), 29), rd(sitz, 3, (-9, 6), 29), rd(sitz, 4, (-9, 5), 29),
                                rd(sitz, 5, (-9, 4), 29), rd(sitz, 31, (-9, 3), 29))
    # Sitz A/D und W/S: drehen beim Einrichten die Kamera bzw. im Rohr-Test das Rohr
    ad, ws = rd(sitz, 0, (-9, 2)), rd(sitz, 1, (-9, 1))
    # Hauptturm-Logik: Flugdaten + Zahl 1-6 + Bool 5-11
    ww = mc.comp(40, (-6, 6), {"count": 6, "offset": 0},
                 [("inc", (flugd, 0))] + [(c, 0) for c in (lookx, looky, kent, turm, ad, ws)])
    wwb = mc.comp(41, (-6, 4), {"count": 7, "offset": 4},
                  [("inc", (ww, 0))] + [(c, 0) for c in (trig, hk4, hk5, hk6, occ, gel, voll)])
    waffen = mc.comp(56, (-3, 5), {"script": w_src}, [(wwb, 0)])

    # Flugabwehr: Radar-Composite (Ziele 1-8) + Turm, Munition und Flugdaten + Bool 9-11
    # Radar belegt alle 32 Zahlenkanaele (8 Ziele); die Kanaele 4, 8 .. 24 ("Zeit seit Meldung" der Ziele 1-6) braucht
    # die Flak nicht, dort hinein: Turm-Drehung, Munition, Kurs, Nick, Roll, Hoehe ueber Grund (aus den Flugdaten)
    # (neu in v16, Anschluss am Ende der Liste) Kanal 28: Drehung des Radarschirms
    dreh = mc.node("AA Radar Drehung", 1, 1, "Radar (Phalanx): Radar Rotation", 0, 5, (-12, -8), late=True)
    # Kanaele 4 Turm, 8 eigenes Tempo vorwaerts, 12 Kurs, 16 Nick, 20 Roll, 24 Hoehe ueber Grund, 28 Schirm, 32 Tempo seitlich
    fd = [rd(flugd, i, (-9, -2 - k)) for k, i in enumerate([14, 17, 18, 19, 13, 15])]
    wa = (radar, 0)
    for k, (c, off) in enumerate(zip([aarot] + fd[:5] + [dreh] + fd[5:], [3, 7, 11, 15, 19, 23, 27, 31])):
        wa = (mc.comp(40, (-7 + k * 0.5, -4 - (k % 2) * 0.5), {"count": 1, "offset": off}, [("inc", wa), (c, 0)]), 0)
    wab = mc.comp(41, (-6, -6), {"count": 3, "offset": 8}, [("inc", wa)] + [(c, 0) for c in (hk6, warn, occ)])
    # AARADAR: Spuren, Zielwahl, Radarschirm; FLAK: Vorhalt, Turm, Rohr, Feuer (bekommt den Radarwarner als Bool 3)
    aar = mc.comp(56, (-3, -5), {"script": r_src}, [(wab, 0)])
    # fuer FLAK: Kanal 23-25 eigenes Tempo (vorwaerts, seitlich, steigen), 26 Munition, Bool 3 Radarwarner
    vt = [rd(flugd, i, (-4, -8 - k * 0.5)) for k, i in enumerate([14, 15, 16])]
    aarn = mc.comp(40, (-2.5, -6), {"count": 4, "offset": 22}, [("inc", (aar, 0))] + [(c, 0) for c in vt + [aamun]])
    # neu in v23: 'Loaded' einer Flak-Autocannon (Schusszaehler) als Bool 4; Anschluss kommt ganz ans Ende (siehe unten)
    aagel = mc.node("AA Geladen", 1, 0, "Light Autocannon (Flugabwehr, eine davon): Loaded", 2, 5, (-12, -9), late=True)
    aarw = mc.comp(41, (-2, -6), {"count": 2, "offset": 2}, [("inc", (aarn, 0)), (warn, 0), (aagel, 0)])
    flak = mc.comp(56, (-1, -5), {"script": a_src}, [(aarw, 0)])

    # Helm: Fluganzeigen, darueber Waffenanzeigen und Einstellhilfe. Monitor: Kamerabild mit kleinem Fadenkreuz
    h1 = mc.comp(56, (0, 0), {"script": h1_src}, [(flugd, 0)])
    fa = [rd(flak, i, (0, -3 - k)) for k, i in enumerate([9, 10, 11, 12, 13, 14, 15, 16])]
    fb = [rd(flak, i, (0, -7 - k), 29) for k, i in enumerate([2, 3, 4])]
    hw = mc.comp(40, (2, -3), {"count": 8, "offset": 20}, [("inc", (waffen, 0))] + [(c, 0) for c in fa])
    hwb = mc.comp(41, (2, -5), {"count": 3, "offset": 9}, [("inc", (hw, 0))] + [(c, 0) for c in fb])
    h2 = mc.comp(56, (4, -2), {"script": h2_src}, [(hwb, 0), (h1, 1)])
    h3 = mc.comp(56, (4, 2), {"script": h3_src}, [(waffen, 0), (vid, 0)])

    for k, (name, val, desc) in enumerate(PROPS_W):
        val = USER_VALUES_W.get(name, val)
        mc.comp(34, (-16 - 2 * (k // 10), 8 - (k % 10)), {"n": name},
                extra='<v text="%s" value="%s"/>' % (fmt(val), fmt(val)))

    # Ausgaenge (Reihen 2 bis 4)
    mc.node("HUD raus", 0, 6, "Monitor vor dem Sitz: Video (Kamerabild mit kleinem Fadenkreuz)", 0, 2, (8, 0), (h3, 1))
    outs = [("Turm Tempo", waffen, 0, 1, "Turret Ring (Large): Rotational Speed", 1, 2),
            ("Kanone Hoehe", waffen, 1, 1, "Robotic Pivot (Kanone): Rotation Target", 2, 2),
            ("Kanone Feuer", waffen, 0, 0, "Battle Cannon: Trigger", 3, 2),
            ("Verschluss", waffen, 1, 0, "Battle Cannon: Open Breech", 4, 2),
            ("Lader", waffen, 2, 0, "Battle Cannon Belt (Feeder): Feed", 5, 2),
            ("Zuender", waffen, 2, 1, "Battle Cannon: Fuse Timer", 0, 3),
            ("Kamera Schwenk", waffen, 3, 1, "frei lassen (seit v4 nicht mehr gebraucht)", 1, 3),
            ("Kamera Neigung", waffen, 4, 1, "Visier: Compact Robotic Pivot unter Kamera und Laser, Rotation Target", 2, 3),
            ("Kamera Zoom", waffen, 5, 1, "Camera Medium: Field of View", 3, 3),
            ("Kamera Laser", waffen, 3, 0, "Laser Distance Sensor: Active", 4, 3),
            ("Kamera IR", waffen, 4, 0, "Camera Medium: Infrared Mode", 5, 3),
            ("AA Tempo", flak, 0, 1, "Turret Ring (Small): Rotational Speed", 0, 4),
            ("AA Hoehe", flak, 1, 1, "Compact Robotic Pivot (Flugabwehr): Rotation Target", 1, 4),
            ("AA Feuer", flak, 0, 0, "Light Autocannon (Flugabwehr): Trigger", 2, 4),
            ("Radar an", flak, 1, 0, "Radar (Phalanx): Activate", 3, 4),
            ("Flares", flak, 2, 0, "Flare Launcher: Launch", 4, 4)]
    for k, (label, src, ch, ntype, desc, nx, nz) in enumerate(outs):
        r = rd(src, ch, (6, 7 - k), 31 if ntype == 1 else 29)
        mc.node(label, 0, ntype, desc, nx, nz, (8, 7 - k), (r, 0))
    # neu in v3, als letzter Anschluss, damit die Reihenfolge der alten gleich bleibt (Kabel bleiben beim Ueberschreiben)
    mc.node("Helm", 0, 6, "Sitz: Headset Video (Flug- und Waffenanzeigen, Einstellhilfe)", 5, 4, (8, -12), (h2, 1))
    # neu in v16: Radarschirm steuern (Radar im manuellen Modus); Kanal 1 Seite, 2 Hoehe
    mc.node("Radar Gimbal", 0, 5, "Radar (Phalanx): Gimbal Input", 1, 5, (8, -13), (aar, 0), late=True)
    # 'AA Geladen' (v23) hinter 'Radar Gimbal' einsortieren, damit alle alten Anschluesse ihre Nummer behalten
    i = [e[0] for e in mc.late].index(aagel)
    mc.late.append(mc.late.pop(i))
    return mc


def main():
    os.makedirs(BUILD, exist_ok=True)
    mins = {}
    ok = True
    for name in ("flug", "mix", "hud", "waffen", "flak", "whud", "mon", "aaradar"):
        with open(os.path.join(LUA_DIR, name + ".lua"), encoding="utf-8") as f:
            mins[name] = minify(f.read(), drop_local=(name == "flug"))
        with open(os.path.join(BUILD, name + ".min.lua"), "w", encoding="utf-8", newline="\n") as f:
            f.write(mins[name])
        size = len(mins[name])
        print("%-6s %5d Zeichen %s" % (name, size, "OK" if size <= LUA_LIMIT else "ZU LANG"))
        ok &= size <= LUA_LIMIT
    if not ok:
        sys.exit("Skript ueber %d Zeichen" % LUA_LIMIT)
    flight = lambda: build_flight_mc(mins["flug"], mins["mix"], mins["hud"])
    weapons = lambda: build_weapons_mc(mins["waffen"], mins["flak"], mins["hud"], mins["whud"], mins["mon"], mins["aaradar"])
    chips = [(MC_FILE, flight()), (MC_FILE_W, weapons()),
             (MC_FILE_EN, english.uebersetze(flight())), (MC_FILE_W_EN, english.uebersetze(weapons()))]
    for fname, mc in chips:
        assert len(mc.desc) <= english.DESC_MAX, (fname, len(mc.desc))
        for ctype, cid, attrs, links, pos, extra in mc.comps:
            if "script" in attrs and len(attrs["script"]) > LUA_LIMIT:
                sys.exit("%s: Skript %d hat %d Zeichen" % (fname, cid, len(attrs["script"])))
    print("englisch: flug %d, hud %d, whud %d, waffen %d Zeichen" % tuple(
        len(english.lua_en(mins[n])) for n in ("flug", "hud", "whud", "waffen")))
    for fname, mc in chips:
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
