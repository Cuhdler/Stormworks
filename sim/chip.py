"""Chip-Kern des Simulators: eine Microcontroller-Definition lesen und Tick fuer Tick ausfuehren.

Lesen: <microprocessor_definition> (im Fahrzeug) oder <microprocessor> (Chip-Datei aus build/ oder dem
Spiel-Ordner microprocessors). Anschluesse (<nodes>), Bausteine (<components>), Bruecken (<components_bridge>),
innere Kabel (<inN component_id=".." node_index=".."/>).

Takt (Wahl beim Anlegen, takt=...):
  "spiel"  (Standard) jeder Baustein braucht einen Tick: er rechnet mit den Ausgaben seiner Quellen vom letzten Tick,
           alle Bausteine gleichzeitig. So beschreibt es das Wissen ueber das Spiel [V, nicht einzeln gemessen].
  "sofort" alles im selben Tick in Kabel-Reihenfolge (keine Verzoegerung). Nur zum Vergleich mit den direkten
           Lua-Pruefstaenden in tools/test_*.py, im Spiel ist es nicht so.
bruecken_takt=False (Standard): die Anschluss-Bruecken des Chips kosten keinen eigenen Tick [V].
float32=True: Zahlen werden wie im Spiel als 32-Bit-Kommazahl gespeichert (ganze Zahlen bis 16 777 216 exakt) [G].
lua_halten=True: ein Lua-Ausgang behaelt seinen Wert, bis das Skript ihn neu setzt [V]; False = jeden Tick auf 0.
"""
import math
import os
import re
import struct
import xml.etree.ElementTree as ET

from ausdruck import zahl_formel, logik_formel, AusdruckFehler, _div, _mod
from lua_block import LuaBlock


class SimFehler(Exception):
    """Fehler mit deutscher Meldung (unbekannter Baustein, falscher Name ...)."""


# ---- Signale -------------------------------------------------------------------------------------------------------

class Composite:
    """32 Zahlen + 32 An/Aus. n[0] = Kanal 1. Wird nach dem Anlegen nicht mehr veraendert."""
    __slots__ = ("n", "b")

    def __init__(self, n=None, b=None):
        self.n = n if n is not None else [0.0] * 32
        self.b = b if b is not None else [False] * 32

    def zahl(self, k):
        return self.n[k - 1]

    def an(self, k):
        return self.b[k - 1]

    def __eq__(self, o):
        return isinstance(o, Composite) and self.n == o.n and self.b == o.b

    def __repr__(self):
        zn = ", ".join("%d: %.6g" % (i + 1, v) for i, v in enumerate(self.n) if v)
        zb = [i + 1 for i, v in enumerate(self.b) if v]
        return "Composite(zahlen={%s}, an=%s)" % (zn, zb)


LEER = Composite()


def composite(zahlen=None, an=None, f32=None):
    """Composite bauen: zahlen = {Kanal: Wert} oder Liste (Kanal 1 zuerst), an = {Kanal: bool} oder Liste."""
    f = f32 or (lambda v: v)
    n, b = [0.0] * 32, [False] * 32
    if zahlen:
        it = zahlen.items() if isinstance(zahlen, dict) else enumerate(zahlen, 1)
        for k, v in it:
            if 1 <= k <= 32:
                n[k - 1] = f(float(v))
    if an:
        it = an.items() if isinstance(an, dict) else enumerate(an, 1)
        for k, v in it:
            if 1 <= k <= 32:
                b[k - 1] = bool(v)
    return Composite(n, b)


def f32(v):
    """Wert wie im Spiel als 32-Bit-Kommazahl."""
    try:
        return struct.unpack("f", struct.pack("f", v))[0]
    except OverflowError:
        return math.copysign(math.inf, v)


def _gleich(v):
    return v


def leer(typ):
    """Wert eines Anschlusses ohne Kabel: An/Aus aus, Zahl 0, Composite leer, Video ohne Bild, Ton nichts."""
    return {0: False, 1: 0.0, 5: LEER, 6: ()}.get(typ)


def als_signal(typ, v, f):
    """Wert von aussen (Szenario) in die Form des Simulators bringen."""
    if typ == 0:
        return bool(v)
    if typ == 1:
        return f(float(v or 0.0))
    if typ == 5:
        if v is None:
            return LEER
        if isinstance(v, Composite):
            return v if f is _gleich else Composite([f(x) for x in v.n], list(v.b))
        if isinstance(v, tuple) and len(v) == 2:
            return composite(v[0], v[1], f)
        if isinstance(v, dict):
            return composite(v, None, f)
        raise SimFehler("Composite erwartet (swsim.composite(...)), bekommen: %r" % (v,))
    if typ == 6:
        return tuple(v) if v else ()
    return v


SIGNAL = {0: "An/Aus", 1: "Zahl", 2: "Welle", 3: "Fluessigkeit", 4: "Strom", 5: "Composite", 6: "Video", 7: "Ton",
          8: "Seil/Gurt"}


# ---- Chip-Definition lesen -------------------------------------------------------------------------------------------

class Knoten:
    """Ein Anschluss des Chips."""
    __slots__ = ("nr", "label", "eingang", "typ", "x", "z", "bruecke", "beschreibung")

    def __init__(self, nr, label, eingang, typ, x, z, bruecke, beschreibung):
        self.nr, self.label, self.eingang, self.typ = nr, label, eingang, typ
        self.x, self.z, self.bruecke, self.beschreibung = x, z, bruecke, beschreibung

    def __repr__(self):
        return "<%s '%s' %s (%d,%d)>" % ("Eingang" if self.eingang else "Ausgang", self.label, SIGNAL.get(self.typ),
                                         self.x, self.z)


class Teildef:
    """Ein Baustein oder eine Bruecke so, wie er in der Datei steht."""
    __slots__ = ("typ", "cid", "attr", "kinder", "ein")

    def __init__(self, typ, cid, attr, kinder, ein):
        self.typ, self.cid, self.attr, self.kinder, self.ein = typ, cid, attr, kinder, ein


def _xml(text):
    """Chip-Text -> XML-Baum. Echte Zeilenumbrueche (Lua-Skripte!) bleiben erhalten."""
    a = text.find("<microprocessor")
    if a < 0:
        raise SimFehler("keine Microcontroller-Definition im Text")
    m = re.match(r"<(microprocessor(?:_definition)?)\b", text[a:])
    e = text.find("</%s>" % m.group(1), a)
    if e < 0:
        raise SimFehler("Microcontroller-Definition ohne Ende")
    t = text[a:e + len(m.group(1)) + 3]
    t = t.replace("\r", "&#13;").replace("\n", "&#10;").replace("\t", "&#9;")
    return ET.fromstring(t)


def _teildef(c):
    typ = int(c.get("type", 0))
    o = c.find("object")
    if o is None:
        raise SimFehler("Baustein ohne <object>")
    ein, kinder = {}, {}
    for k in o:
        if re.fullmatch(r"in\d+|inc|inoff", k.tag):
            q = int(k.get("component_id", 0))
            if q:
                ein[k.tag] = (q, int(k.get("node_index", 0)))
        else:
            kinder[k.tag] = k
    return Teildef(typ, int(o.get("id")), dict(o.attrib), kinder, ein)


class ChipDef:
    """Gelesene Chip-Definition (unveraenderlich; mehrere laufende Chips koennen sie teilen)."""

    def __init__(self, text):
        root = _xml(text)
        self.name = root.get("name", "")
        self.beschreibung = root.get("description", "")
        self.breite, self.laenge = int(root.get("width", 1)), int(root.get("length", 1))
        self.knoten = []
        for nr, n in enumerate(root.findall("./nodes/n")):
            nd = n.find("node")
            p = nd.find("position")
            x = int(float(p.get("x", 0))) if p is not None else 0
            z = int(float(p.get("z", 0))) if p is not None else 0
            self.knoten.append(Knoten(nr, nd.get("label", ""), nd.get("mode", "0") == "1", int(nd.get("type", 0)), x, z,
                                      int(n.get("component_id")), nd.get("description", "")))
        grp = root.find("group")
        if grp is None:
            raise SimFehler("Chip '%s': kein <group>" % self.name)
        if grp.find("groups") is not None and len(grp.find("groups")):
            raise SimFehler("Chip '%s': Untergruppen (<groups>) kann der Simulator noch nicht" % self.name)
        self.bausteine = [_teildef(c) for c in grp.findall("./components/c")]
        self.bruecken = {t.cid: t for t in (_teildef(c) for c in grp.findall("./components_bridge/c"))}
        for k in self.knoten:
            if k.bruecke not in self.bruecken:
                raise SimFehler("Chip '%s': Anschluss '%s' ohne Bruecke %d" % (self.name, k.label, k.bruecke))

    def typen(self):
        """{Baustein-Typ: Anzahl} in diesem Chip."""
        out = {}
        for b in self.bausteine:
            out[b.typ] = out.get(b.typ, 0) + 1
        return out


_DEF_CACHE = {}


def chipdef(text):
    """ChipDef mit Zwischenspeicher (gleicher Text -> dieselbe Definition, nur einmal gelesen)."""
    d = _DEF_CACHE.get(text)
    if d is None:
        d = _DEF_CACHE[text] = ChipDef(text)
    return d


# ---- Bausteine -----------------------------------------------------------------------------------------------------

def _lies(w, q, leerwert):
    if q is None:
        return leerwert
    t = w.get(q[0])
    if t is None or q[1] >= len(t):
        return leerwert
    v = t[q[1]]
    return leerwert if v is None else v


def _nz(kinder, name, standard=0.0):
    """Zahl-Eigenschaft als Kind-Element: <name text=".." value=".."/> (value fehlt = 0)."""
    k = kinder.get(name)
    if k is None:
        return standard
    for v in (k.get("value"), k.get("text")):
        if v is not None:
            try:
                return float(v)
            except ValueError:
                pass
    return 0.0


class Baustein:
    typ, name, vermutet = None, "?", False

    def __init__(self, d, chip):
        self.cid, self.ein, self.attr, self.k = d.cid, d.ein, d.attr, d.kinder
        self.f = chip.f32
        self.chip = chip
        self.einrichten()

    def einrichten(self):
        pass

    def an(self, w, tag):
        return bool(_lies(w, self.ein.get(tag), False))

    def zahl(self, w, tag):
        return float(_lies(w, self.ein.get(tag), 0.0))

    def comp(self, w, tag):
        return _lies(w, self.ein.get(tag), LEER)

    def quellen(self):
        return [q[0] for q in self.ein.values()]

    def attr_zahl(self, name, standard):
        try:
            return float(self.attr.get(name, standard))
        except ValueError:
            return standard


def _zwei(name, typ, f, zahl=False):
    class B(Baustein):
        def rechne(self, w):
            if zahl:
                return (self.f(f(self.zahl(w, "in1"), self.zahl(w, "in2"))),)
            return (f(self.an(w, "in1"), self.an(w, "in2")),)
    B.typ, B.name = typ, name
    return B


class Nicht(Baustein):
    typ, name = 0, "NICHT"

    def rechne(self, w):
        return (not self.an(w, "in1"),)


Und = _zwei("UND", 1, lambda a, b: a and b)
Oder = _zwei("ODER", 2, lambda a, b: a or b)
EntwederOder = _zwei("XOR", 3, lambda a, b: a != b)
NichtUnd = _zwei("NAND", 4, lambda a, b: not (a and b))
NichtOder = _zwei("NOR", 5, lambda a, b: not (a or b))
Plus = _zwei("Plus", 6, lambda a, b: a + b, True)
Minus = _zwei("Minus", 7, lambda a, b: a - b, True)
Mal = _zwei("Mal", 8, lambda a, b: a * b, True)


class Geteilt(Baustein):
    typ, name, vermutet = 9, "Geteilt (durch 0 = unendlich vermutet)", True

    def rechne(self, w):
        return (self.f(_div(self.zahl(w, "in1"), self.zahl(w, "in2"))),)


class Formel(Baustein):
    typ, name, anzahl = 10, "Formel f(x,y,z)", 3

    def einrichten(self):
        try:
            self.formel = zahl_formel(self.attr.get("e", ""), self.anzahl)
        except AusdruckFehler as e:
            raise SimFehler("Chip '%s', Baustein %d: %s" % (self.chip.name, self.cid, e))
        self.tags = ["in%d" % i for i in range(1, self.anzahl + 1)]

    def rechne(self, w):
        return (self.f(self.formel(*[self.zahl(w, t) for t in self.tags])),)


class Formel8(Formel):
    typ, name, anzahl = 36, "Formel mit 8 Eingaengen", 8


class Formel1(Formel):
    typ, name, anzahl = 45, "Formel mit 1 Eingang", 1


class Logik4(Baustein):
    typ, name, anzahl = 46, "An/Aus-Formel mit 4 Eingaengen", 4

    def einrichten(self):
        try:
            self.formel = logik_formel(self.attr.get("e", ""), self.anzahl)
        except AusdruckFehler as e:
            raise SimFehler("Chip '%s', Baustein %d: %s" % (self.chip.name, self.cid, e))
        self.tags = ["in%d" % i for i in range(1, self.anzahl + 1)]

    def rechne(self, w):
        return (self.formel(*[self.an(w, t) for t in self.tags]),)


class Logik8(Logik4):
    typ, name, anzahl = 47, "An/Aus-Formel mit 8 Eingaengen", 8


class Begrenzen(Baustein):
    typ, name = 11, "Begrenzen (clamp)"

    def einrichten(self):
        self.mn, self.mx = _nz(self.k, "min"), _nz(self.k, "max")

    def rechne(self, w):
        return (self.f(min(max(self.zahl(w, "in1"), self.mn), self.mx)),)


class Schwelle(Baustein):
    typ, name = 12, "Schwelle (min <= x <= max)"

    def einrichten(self):
        self.mn, self.mx = _nz(self.k, "min"), _nz(self.k, "max")

    def rechne(self, w):
        return (self.mn <= self.zahl(w, "in1") <= self.mx,)


class Speicher(Baustein):
    typ, name, vermutet = 13, "Zahlen-Speicher (Reset vor Set vermutet)", True

    def einrichten(self):
        self.r, self.v = _nz(self.k, "r"), 0.0

    def rechne(self, w):
        if self.an(w, "in2"):
            self.v = self.r
        elif self.an(w, "in1"):
            self.v = self.zahl(w, "in3")
        return (self.f(self.v),)


class Betrag(Baustein):
    typ, name = 14, "Betrag (abs)"

    def rechne(self, w):
        return (abs(self.zahl(w, "in1")),)


class KonstanteZahl(Baustein):
    typ, name = 15, "Konstante Zahl"

    def einrichten(self):
        self.v = (self.f(_nz(self.k, "n")),)

    def rechne(self, w):
        return self.v


class KonstanteAn(Baustein):
    typ, name = 16, "Konstante An"

    def rechne(self, w):
        return (True,)


class Groesser(Baustein):
    typ, name = 17, "Groesser (in1 > in2)"

    def rechne(self, w):
        return (self.zahl(w, "in1") > self.zahl(w, "in2"),)


class Kleiner(Baustein):
    typ, name = 18, "Kleiner (in1 < in2)"

    def rechne(self, w):
        return (self.zahl(w, "in1") < self.zahl(w, "in2"),)


class Schieber(Baustein):
    typ, name = 19, "Eigenschaft Schieber"

    def einrichten(self):
        self.v = (self.f(_nz(self.k, "v")),)

    def rechne(self, w):
        return self.v


def auswahl_wert(d):
    """Eigenschaft Auswahl (20): Wert des gewaehlten Eintrags (Attribut i = Nummer ab 0)."""
    items = d.kinder.get("items")
    wahl = int(float(d.attr.get("i", 0)))
    eintraege = list(items) if items is not None else []
    if 0 <= wahl < len(eintraege):
        return _nz({k.tag: k for k in eintraege[wahl]}, "v")
    return 0.0


class Auswahl(Baustein):
    typ, name = 20, "Eigenschaft Auswahl"

    def einrichten(self):
        d = Teildef(self.typ, self.cid, self.attr, self.k, self.ein)
        self.v = (self.f(auswahl_wert(d)),)

    def rechne(self, w):
        return self.v


class Weiche(Baustein):
    typ, name, vermutet = 21, "Zahlen-Weiche (Ausgang 0 bei an, 1 bei aus vermutet)", True

    def rechne(self, w):
        x, s = self.zahl(w, "in1"), self.an(w, "in2")
        return (x, 0.0) if s else (0.0, x)


class Umschalter(Baustein):
    """22 Zahl, 53 Composite, 57 Video, 59 Ton: in1 bei an, in2 bei aus, in3 Schalter."""
    typ, name = 22, "Zahlen-Umschalter"
    leerwert = 0.0

    def rechne(self, w):
        return (_lies(w, self.ein.get("in1" if self.an(w, "in3") else "in2"), self.leerwert),)


class CompUmschalter(Umschalter):
    typ, name, leerwert = 53, "Composite-Umschalter", LEER


class VideoUmschalter(Umschalter):
    typ, name, leerwert = 57, "Video-Umschalter", ()


class TonUmschalter(Umschalter):
    typ, name, leerwert = 59, "Ton-Umschalter", None


class PID(Baustein):
    """in1 Soll, in2 Ist, in3 aktiv; kp ki kd. Rechenweise [V]: P = kp*e, I += ki*e/60, D = kd*(e - e_alt)*60."""
    typ, name, vermutet = 23, "PID (Rechenweise vermutet)", True

    def einrichten(self):
        self.kp, self.ki, self.kd = _nz(self.k, "kp"), _nz(self.k, "ki"), _nz(self.k, "kd")
        self.i, self.e_alt = 0.0, None

    def werte(self, w):
        return self.kp, self.ki, self.kd, self.an(w, "in3")

    def rechne(self, w):
        kp, ki, kd, aktiv = self.werte(w)
        if not aktiv:
            self.i, self.e_alt = 0.0, None
            return (0.0,)
        e = self.zahl(w, "in1") - self.zahl(w, "in2")
        self.i += ki * e / 60.0
        d = 0.0 if self.e_alt is None else kd * (e - self.e_alt) * 60.0
        self.e_alt = e
        return (self.f(kp * e + self.i + d),)


class PIDErweitert(PID):
    typ, name = 39, "PID erweitert (Rechenweise vermutet)"

    def werte(self, w):
        return self.zahl(w, "in3"), self.zahl(w, "in4"), self.zahl(w, "in5"), self.an(w, "in6")


class SRSpeicher(Baustein):
    typ, name, vermutet = 24, "SR-Speicher (Reset gewinnt vermutet)", True

    def einrichten(self):
        self.q = False

    def rechne(self, w):
        if self.an(w, "in2"):
            self.q = False
        elif self.an(w, "in1"):
            self.q = True
        return (self.q, not self.q)


class JKFlipFlop(Baustein):
    typ, name, vermutet = 25, "JK-Flipflop (beide an = umschalten je Tick vermutet)", True

    def einrichten(self):
        self.q = False

    def rechne(self, w):
        j, k = self.an(w, "in1"), self.an(w, "in2")
        if j and k:
            self.q = not self.q
        elif j:
            self.q = True
        elif k:
            self.q = False
        return (self.q, not self.q)


class Kondensator(Baustein):
    """in1 laden; ct Ladezeit s, dt Entladezeit s (fehlt = 1). Ausgang an, wenn voll geladen, bis ganz leer [V]."""
    typ, name, vermutet = 26, "Kondensator (Verhalten vermutet)", True

    def einrichten(self):
        self.ct, self.dt = self.attr_zahl("ct", 1.0), self.attr_zahl("dt", 1.0)
        self.ladung, self.aus = 0.0, False

    def rechne(self, w):
        if self.an(w, "in1"):
            self.ladung = 1.0 if self.ct <= 0 else min(1.0, self.ladung + 1.0 / (self.ct * 60))
        else:
            self.ladung = 0.0 if self.dt <= 0 else max(0.0, self.ladung - 1.0 / (self.dt * 60))
        if self.ladung >= 1.0:
            self.aus = True
        elif self.ladung <= 0.0:
            self.aus = False
        return (self.aus,)


class Blinker(Baustein):
    """in1 Steuerung; on/off = Dauer an/aus in s (fehlt = 1). Beginnt mit an [V]."""
    typ, name, vermutet = 27, "Blinker (Verhalten vermutet)", True

    def einrichten(self):
        self.t_an = max(1, round(self.attr_zahl("on", 1.0) * 60))
        self.t_aus = max(1, round(self.attr_zahl("off", 1.0) * 60))
        self.t = 0

    def rechne(self, w):
        if not self.an(w, "in1"):
            self.t = 0
            return (False,)
        v = (self.t % (self.t_an + self.t_aus)) < self.t_an
        self.t += 1
        return (v,)


class Taster(Baustein):
    typ, name = 28, "Druck-Schalter (Push to Toggle)"

    def einrichten(self):
        self.q, self.alt = False, False

    def rechne(self, w):
        e = self.an(w, "in1")
        if e and not self.alt:
            self.q = not self.q
        self.alt = e
        return (self.q,)


class CompLesenAn(Baustein):
    """Kanal = Attribut i ab 0 (fehlt = Kanal 1); in2 (variabler Kanal, ab 1) [V]."""
    typ, name, zahlen = 29, "Composite lesen An/Aus", False

    def einrichten(self):
        self.kanal = int(float(self.attr.get("i", 0)))

    def rechne(self, w):
        c = self.comp(w, "in1")
        k = self.kanal
        if "in2" in self.ein:
            k = int(round(self.zahl(w, "in2"))) - 1
        if not 0 <= k < 32:
            return (0.0 if self.zahlen else False,)
        return (c.n[k] if self.zahlen else c.b[k],)


class CompLesenZahl(CompLesenAn):
    typ, name, zahlen = 31, "Composite lesen Zahl", True


class CompSchreibenZahl(Baustein):
    """inc = Grund-Composite, in1..inN = Werte ab Kanal offset+1 (count Stueck, fehlt = 32); nur angeschlossene
    Eingaenge aendern ihren Kanal. inoff = Start-Kanal als Zahl ab 1 [V]."""
    typ, name, zahlen = 40, "Composite schreiben Zahl", True

    def einrichten(self):
        anzahl = int(float(self.attr.get("count", 32)))
        self.start = int(float(self.attr.get("offset", 0)))
        self.plaetze = [(i, "in%d" % (i + 1)) for i in range(anzahl) if "in%d" % (i + 1) in self.ein]

    def rechne(self, w):
        c = self.comp(w, "inc")
        start = self.start
        if "inoff" in self.ein:
            start = int(round(self.zahl(w, "inoff"))) - 1
        if self.zahlen:
            n = list(c.n)
            for i, tag in self.plaetze:
                if 0 <= start + i < 32:
                    n[start + i] = self.f(self.zahl(w, tag))
            return (Composite(n, c.b),)
        b = list(c.b)
        for i, tag in self.plaetze:
            if 0 <= start + i < 32:
                b[start + i] = self.an(w, tag)
        return (Composite(c.n, b),)


class CompSchreibenAn(CompSchreibenZahl):
    typ, name, zahlen = 41, "Composite schreiben An/Aus", False


class EigenschaftSchalter(Baustein):
    typ, name = 33, "Eigenschaft Schalter"

    def rechne(self, w):
        return (self.attr.get("v", "false") == "true",)


class EigenschaftZahl(Baustein):
    typ, name = 34, "Eigenschaft Zahl"

    def einrichten(self):
        self.v = (self.f(_nz(self.k, "v")),)

    def rechne(self, w):
        return self.v


class Delta(Baustein):
    typ, name = 35, "Delta (Aenderung je Tick)"

    def einrichten(self):
        self.alt = 0.0

    def rechne(self, w):
        x = self.zahl(w, "in1")
        d, self.alt = x - self.alt, x
        return (self.f(d),)


class Zaehler(Baustein):
    """in1 hoch, in2 runter, in3 zuruecksetzen; i Schritt, r Startwert nach Reset, min/max, m="1" begrenzen.
    Zaehlt jeden Tick, solange hoch/runter an ist; Startwert 0 [V]."""
    typ, name, vermutet = 37, "Zaehler (Verhalten vermutet)", True

    def einrichten(self):
        self.schritt, self.r = _nz(self.k, "i", 1.0), _nz(self.k, "r")
        self.mn, self.mx, self.grenze = _nz(self.k, "min"), _nz(self.k, "max"), self.attr.get("m") == "1"
        self.v = 0.0

    def rechne(self, w):
        if self.an(w, "in3"):
            self.v = self.r
        else:
            if self.an(w, "in1"):
                self.v += self.schritt
            if self.an(w, "in2"):
                self.v -= self.schritt
        if self.grenze:
            self.v = min(max(self.v, self.mn), self.mx)
        return (self.f(self.v),)


class Rest(Baustein):
    typ, name, vermutet = 38, "Modulo (wie fmod vermutet)", True

    def rechne(self, w):
        return (self.f(_mod(self.zahl(w, "in1"), self.zahl(w, "in2"))),)


class Gleich(Baustein):
    typ, name, vermutet = 42, "Gleich (|a-b| < e vermutet)", True

    def einrichten(self):
        self.e = _nz(self.k, "e")

    def rechne(self, w):
        return (abs(self.zahl(w, "in1") - self.zahl(w, "in2")) < self.e,)


class Anzeige(Baustein):
    """43/44 Tooltip (nur Anzeige im Editor), 58 Eigenschaft Text (nur fuer Lua): keine Ausgaenge."""
    typ, name = 43, "Tooltip Zahl"

    def rechne(self, w):
        return ()


class AnzeigeAn(Anzeige):
    typ, name = 44, "Tooltip An/Aus"


class EigenschaftText(Anzeige):
    typ, name = 58, "Eigenschaft Text"


class Puls(Baustein):
    """m: 0 an->aus, 1 aus->an (fehlt = 1), 2 jede Aenderung (sw_mc_lib)."""
    typ, name = 48, "Puls"

    def einrichten(self):
        self.m, self.alt = int(float(self.attr.get("m", 1))), False

    def rechne(self, w):
        e = self.an(w, "in1")
        v = (e and not self.alt) if self.m == 1 else ((self.alt and not e) if self.m == 0 else e != self.alt)
        self.alt = e
        return (v,)


class Zeitglied(Baustein):
    """49 TON, 50 TOF, 51 RTO, 52 RTF: in1 an, in2 Dauer, in3 Reset (RTO/RTF); u = 0 Sekunden, 1 Ticks [V]."""
    typ, name, vermutet = 49, "Zeitglied TON (vermutet)", True

    def einrichten(self):
        self.tick_je = 1.0 if self.attr.get("u", "0") == "1" else 60.0
        self.t, self.aus = 0, False

    def rechne(self, w):
        an, dauer = self.an(w, "in1"), self.zahl(w, "in2") * self.tick_je
        if self.typ == 49:
            self.t = self.t + 1 if an else 0
            return (an and self.t >= dauer,)
        if self.typ == 50:
            self.t = 0 if an else self.t + 1
            return (an or self.t < dauer,)
        if self.an(w, "in3"):
            self.t = 0
        if self.typ == 51:
            if an:
                self.t += 1
            return (self.t >= dauer,)
        if not an:
            self.t += 1
        return (an or self.t < dauer,)


class ZeitTOF(Zeitglied):
    typ, name = 50, "Zeitglied TOF (vermutet)"


class ZeitRTO(Zeitglied):
    typ, name = 51, "Zeitglied RTO (vermutet)"


class ZeitRTF(Zeitglied):
    typ, name = 52, "Zeitglied RTF (vermutet)"


class Lua(Baustein):
    """in1 Composite, in2 Video; Ausgang 0 Composite, 1 Video (Eingangsbild + eigenes Bild darueber)."""
    typ, name = 56, "Lua-Skript"

    def einrichten(self):
        c = self.chip
        self.block = LuaBlock(self.attr.get("script", ""), c.eigenschaften, "Chip '%s', Lua-Baustein %d" % (c.name, self.cid),
                              f32=c.f32, halten=c.lua_halten, http=c.http)

    def rechne(self, w):
        n, b = self.block.tick(self.comp(w, "in1"))
        bild = _lies(w, self.ein.get("in2"), ())
        return (Composite(n, b), tuple(bild) + (self.block,))


TYPEN = {k.typ: k for k in (Nicht, Und, Oder, EntwederOder, NichtUnd, NichtOder, Plus, Minus, Mal, Geteilt, Formel,
                             Begrenzen, Schwelle, Speicher, Betrag, KonstanteZahl, KonstanteAn, Groesser, Kleiner,
                             Schieber, Auswahl, Weiche, Umschalter, PID, SRSpeicher, JKFlipFlop, Kondensator, Blinker,
                             Taster, CompLesenAn, CompLesenZahl, EigenschaftSchalter, EigenschaftZahl, Delta, Formel8,
                             Zaehler, Rest, PIDErweitert, CompSchreibenZahl, CompSchreibenAn, Gleich, Anzeige, AnzeigeAn,
                             Formel1, Logik4, Logik8, Puls, Zeitglied, ZeitTOF, ZeitRTO, ZeitRTF, CompUmschalter, Lua,
                             VideoUmschalter, EigenschaftText, TonUmschalter)}
# 30/32 alte Composite-Schreib-Bausteine, 54/55 Zahl <-> Composite-Bits: in keiner Datei auf Andres PC (10.10.)
BRUECKE = {0: ("Eingang", 0), 1: ("Ausgang", 0), 2: ("Eingang", 1), 3: ("Ausgang", 1), 4: ("Eingang", 5),
           5: ("Ausgang", 5), 6: ("Eingang", 6), 7: ("Ausgang", 6), 8: ("Eingang", 7), 9: ("Ausgang", 7)}


# ---- laufender Chip ------------------------------------------------------------------------------------------------

class Chip:
    """Ein laufender Microcontroller (eigener Zustand, eigene Lua-Skripte).

        chip = Chip(chipdef(text))       oder   Chip.aus_datei("build/Figet Marena Licht v1.0.xml")
        chip.setze("Uhr", 0.5); chip.tick(); chip.lese("Licht")
    """

    def __init__(self, cdef, takt="spiel", bruecken_takt=False, float32=True, lua_halten=True, http=None, name=None):
        if takt not in ("spiel", "sofort"):
            raise SimFehler("takt muss 'spiel' oder 'sofort' sein, nicht %r" % (takt,))
        self.cdef, self.name = cdef, name or cdef.name
        self.takt, self.bruecken_takt, self.lua_halten, self.http = takt, bruecken_takt, lua_halten, http
        self.f32 = f32 if float32 else _gleich
        self.eigenschaften = self._eigenschaften()
        self.bausteine = []
        for d in cdef.bausteine:
            k = TYPEN.get(d.typ)
            if k is None:
                raise SimFehler("Baustein-Typ %d (Chip '%s', Baustein %d) kennt der Simulator nicht" % (d.typ, self.name, d.cid))
            self.bausteine.append(k(d, self))
        self.vermutet = sorted({b.name for b in self.bausteine if b.vermutet})
        self.lua = [b.block for b in self.bausteine if isinstance(b, Lua)]
        self.ein_knoten = [k for k in cdef.knoten if k.eingang]
        self.aus_knoten = [k for k in cdef.knoten if not k.eingang]
        for k in cdef.knoten:
            bt = cdef.bruecken[k.bruecke].typ
            if bt not in BRUECKE or BRUECKE[bt][0] != ("Eingang" if k.eingang else "Ausgang"):
                raise SimFehler("Chip '%s', Anschluss '%s': Bruecken-Typ %d passt nicht" % (self.name, k.label, bt))
        self.werte = [leer(k.typ) for k in cdef.knoten]           # aktueller Wert je Anschluss (Eingaenge von aussen)
        self.w = {}                                               # Baustein-Nummer -> Ausgaenge (Tupel)
        for k in self.ein_knoten:
            self.w[k.bruecke] = (leer(k.typ),)
        self.reihenfolge = self._reihenfolge() if takt == "sofort" else self.bausteine
        self.ticks = 0

    @classmethod
    def aus_datei(cls, pfad, **opt):
        with open(pfad, encoding="utf-8", newline="") as f:
            return cls(chipdef(f.read()), **opt)

    def _eigenschaften(self):
        e = {"zahl": {}, "an": {}, "text": {}}
        for d in self.cdef.bausteine:
            if d.typ == 34:
                e["zahl"][d.attr.get("n", "")] = self.f32(_nz(d.kinder, "v"))
            elif d.typ == 19:
                e["zahl"][d.attr.get("name", "")] = self.f32(_nz(d.kinder, "v"))
            elif d.typ == 20:
                e["zahl"][d.attr.get("name", "")] = self.f32(auswahl_wert(d))
            elif d.typ == 33:
                e["an"][d.attr.get("n", "")] = d.attr.get("v", "false") == "true"
            elif d.typ == 58:
                e["text"][d.attr.get("n", "")] = d.attr.get("v", "")
        return e

    def _reihenfolge(self):
        """Bausteine so sortiert, dass jede Quelle vor ihrem Ziel rechnet (Kreise: Wert vom letzten Tick)."""
        nach_id = {b.cid: b for b in self.bausteine}
        fertig, out, besucht = set(), [], set()
        for start in self.bausteine:
            if start.cid in fertig:
                continue
            stapel = [(start, iter(start.quellen()))]
            besucht.add(start.cid)
            while stapel:
                b, it = stapel[-1]
                weiter = False
                for q in it:
                    qb = nach_id.get(q)
                    if qb is not None and qb.cid not in besucht:
                        besucht.add(qb.cid)
                        stapel.append((qb, iter(qb.quellen())))
                        weiter = True
                        break
                if not weiter:
                    stapel.pop()
                    fertig.add(b.cid)
                    out.append(b)
        return out

    # ---- Anschluesse von aussen --------------------------------------------------------------------------------------

    def knoten(self, label):
        treffer = [k for k in self.cdef.knoten if k.label == label]
        if len(treffer) != 1:
            raise SimFehler("Chip '%s': Anschluss '%s' %s (vorhanden: %s)" % (
                self.name, label, "gibt es nicht" if not treffer else "gibt es mehrfach",
                ", ".join(k.label for k in self.cdef.knoten)))
        return treffer[0]

    def setze(self, label, wert):
        """Wert an einen Eingang legen (bleibt, bis er neu gesetzt wird)."""
        k = self.knoten(label) if isinstance(label, str) else self.cdef.knoten[label]
        if not k.eingang:
            raise SimFehler("Chip '%s': '%s' ist ein Ausgang" % (self.name, k.label))
        self.werte[k.nr] = als_signal(k.typ, wert, self.f32)

    def lese(self, label):
        """Wert eines Anschlusses (Ausgang: nach dem letzten Tick)."""
        k = self.knoten(label) if isinstance(label, str) else self.cdef.knoten[label]
        return self.werte[k.nr]

    # ---- Takt ------------------------------------------------------------------------------------------------------

    def tick(self):
        """Ein Spiel-Tick. Rueckgabe: {Ausgang: Wert}."""
        werte = self.werte
        if self.takt == "sofort":
            w = self.w
            for k in self.ein_knoten:
                w[k.bruecke] = (werte[k.nr],)
            for b in self.reihenfolge:
                w[b.cid] = b.rechne(w)
            quelle = w
        else:
            alt, neu = self.w, {}
            if not self.bruecken_takt:
                for k in self.ein_knoten:
                    alt[k.bruecke] = (werte[k.nr],)
            for b in self.bausteine:
                neu[b.cid] = b.rechne(alt)
            for k in self.ein_knoten:
                neu[k.bruecke] = (werte[k.nr],)
            quelle = alt if self.bruecken_takt else neu
            w = self.w = neu
        for k in self.aus_knoten:
            q = self.cdef.bruecken[k.bruecke].ein.get("in1")
            v = _lies(quelle, q, leer(k.typ))
            w[k.bruecke] = (v,)
            werte[k.nr] = v
        self.ticks += 1
        return {k.label: werte[k.nr] for k in self.aus_knoten}

    # ---- Auswertung ------------------------------------------------------------------------------------------------

    def wert(self, cid, nr=0):
        """Ausgang nr eines inneren Bausteins (nach dem letzten Tick)."""
        return _lies(self.w, (cid, nr), None)

    def verzoegerung(self, von, zu):
        """Wie viele Ticks spaeter eine Aenderung am Eingang 'von' fruehestens am Ausgang 'zu' ankommt (kuerzester Weg
        durch die Bausteine; ohne die Rechenzeit im Lua-Skript selbst). None = kein Weg."""
        start, ziel = self.knoten(von).bruecke, self.knoten(zu)
        nach = {}
        for b in self.bausteine:
            for q in b.quellen():
                nach.setdefault(q, []).append(b.cid)
        q_aus = self.cdef.bruecken[ziel.bruecke].ein.get("in1")
        if q_aus is None:
            return None
        weite, rand = {start: 0}, [start]
        while rand:
            neu = []
            for c in rand:
                for z in nach.get(c, []):
                    if z not in weite:
                        weite[z] = weite[c] + 1
                        neu.append(z)
            rand = neu
        if q_aus[0] not in weite:
            return None
        if self.takt == "sofort":
            return 0
        if self.bruecken_takt:
            return weite[q_aus[0]] + 1
        return max(0, weite[q_aus[0]] - 1)

    def fehler(self):
        """Liste der Lua-Fehler (abgestuerzte Skripte)."""
        return [b.fehler for b in self.lua if b.fehler]

    def hinweise(self):
        out = []
        for b in self.lua:
            out += ["%s: %s" % (b.ort, h) for h in b.hinweise]
        return out

    def bild(self, label):
        """Video-Ausgang -> Liste der Bild-Ebenen (Lua-Bloecke, unten zuerst)."""
        return list(self.lese(label))

    def zeichne(self, label, breite=96, hoehe=96):
        """onDraw aller Lua-Skripte, deren Bild an diesem Video-Ausgang ankommt. Rueckgabe: alle screen-Aufrufe."""
        return zeichne(self.lese(label), breite, hoehe)


def zeichne(bild, breite=96, hoehe=96):
    """Ein Video-Signal (Tupel der Ebenen) zeichnen: onDraw jeder Lua-Ebene, unten zuerst."""
    out = []
    for e in bild or ():
        if isinstance(e, LuaBlock):
            out += e.zeichne(breite, hoehe)
        else:
            out.append(("Bild", str(e)))
    return out


def texte(bild, breite=96, hoehe=96):
    """Nur die Texte eines Video-Signals (drawText/drawTextBox)."""
    out = []
    for z in zeichne(bild, breite, hoehe):
        if z[0] == "drawText" and len(z) >= 4:
            out.append(str(z[3]))
        elif z[0] == "drawTextBox" and len(z) >= 6:
            out.append(str(z[5]))
    return out


def chip_dateien(ordner=None):
    """Alle Chip-Dateien im Spiel-Ordner microprocessors (nur lesen)."""
    ordner = ordner or os.path.join(os.environ.get("APPDATA", ""), "Stormworks", "data", "microprocessors")
    return sorted(os.path.join(ordner, f) for f in os.listdir(ordner) if f.lower().endswith(".xml"))
