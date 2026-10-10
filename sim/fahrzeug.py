"""Fahrzeug-Netz des Simulators: alle Teile, Anschluesse und Kabel einer Fahrzeugdatei; mehrere Chips zusammen laufen.

Lesen (nur lesen, nie schreiben):
- Teile mit Art d, Position vp, Drehung r (fehlt = 0,0,1,-1,0,0,0,-1,0) und Spiegelung t (Bit 1 x, 2 y, 4 z, lokal vor
  der Drehung) - Regeln aus wissen/fahrzeugdatei.md.
- Anschluesse: normale Teile aus wissen/bauteile/bauteile.json (sonst aus den Spieldaten), Microcontroller aus ihrer
  eingebetteten Definition (Feld x, z auf dem Chip).
- Kabel (<logic_node_links>): Ausgang voxel_pos_0 -> Eingang voxel_pos_1. Ein Kabel, das auf keinen passenden Anschluss
  zeigt (Ort, Signal-Art, Richtung), verwirft das Spiel beim Laden stumm [G] -> Liste .verworfen.

Laufen: Fahrzeug(daten) legt fuer jeden gewaehlten Chip einen laufenden Chip an. Alle anderen Teile sind Fuehler
(ihre Ausgaenge setzt das Szenario) oder Stellglieder (ihre Eingaenge liest das Szenario). Nicht gewaehlte Chips
verhalten sich wie Fuehler: ihre Ausgaenge kann das Szenario setzen.

Zeit zwischen Teilen (Takt "spiel"): ein Chip liest am Anfang des Ticks, was Fuehler in diesem Tick zeigen und was die
anderen Chips im letzten Tick ausgegeben haben [V]. Takt "sofort": Chips in Kabel-Reihenfolge, alles im selben Tick.
"""
import json
import os
import re

from chip import Chip, SimFehler, chipdef, leer, als_signal, f32, _gleich, zeichne, texte, SIGNAL

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HIER)
BAUTEILE = os.path.join(ROOT, "wissen", "bauteile", "bauteile.json")
SPIEL_DEF = r"E:\SteamLibrary\steamapps\common\Stormworks\rom\data\definitions"
FAHRZEUGE = os.path.join(os.environ.get("APPDATA", ""), "Stormworks", "data", "vehicles")
R_OHNE = (0, 0, 1, -1, 0, 0, 0, -1, 0)
LOGIK = (0, 1, 5, 6, 7)          # Signal-Arten, die der Simulator weitergibt (Strom, Seil: nur geprueft)


def xyz(attr):
    d = dict(re.findall(r'(\w)="(-?\d+)"', attr or ""))
    return tuple(int(d.get(k, 0)) for k in "xyz")


def welt(vp, r, t, p):
    """Lokaler Punkt p eines Teils -> Weltposition (erst spiegeln, dann drehen, dann verschieben)."""
    p = [(-p[i] if t & (1 << i) else p[i]) for i in range(3)]
    return tuple(vp[i] + r[i] * p[0] + r[3 + i] * p[1] + r[6 + i] * p[2] for i in range(3))


_BAUTEILE = {}
_SPIEL = {}


def def_anschluesse(d):
    """Anschluesse einer Bauteil-Art: Liste (Label, Eingang?, Typ, Position lokal) oder None, wenn unbekannt."""
    if not _BAUTEILE and os.path.exists(BAUTEILE):
        with open(BAUTEILE, encoding="utf-8") as f:
            _BAUTEILE.update(json.load(f))
    b = _BAUTEILE.get(d)
    if b is not None:
        return [(a["label"], a["ein"] == 1, a["typ"], tuple(a["pos"])) for a in b["anschluesse"]]
    if d not in _SPIEL:
        pfad = os.path.join(SPIEL_DEF, d + ".xml")
        out = None
        if os.path.exists(pfad):
            t = open(pfad, encoding="utf-8", errors="replace").read()
            out = []
            for m in re.finditer(r"<logic_node ([^>]*)>(.*?)</logic_node>", t, re.S):
                at = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
                ps = re.search(r"<position([^/]*)/>", m.group(2))
                out.append((at.get("label", ""), at.get("mode", "0") == "1", int(at.get("type", 0)), xyz(ps.group(1) if ps else "")))
        _SPIEL[d] = out
    return _SPIEL[d]


class Teil:
    __slots__ = ("nr", "d", "vp", "r", "t", "name", "chipdef")

    def __init__(self, nr, d, vp, r, t, name, cdef):
        self.nr, self.d, self.vp, self.r, self.t, self.name, self.chipdef = nr, d, vp, r, t, name, cdef

    def __repr__(self):
        return "<%s%s @ %s>" % (self.d, " '%s'" % self.name if self.name else "", self.vp)


class Anschluss:
    __slots__ = ("nr", "teil", "label", "eingang", "typ", "welt", "knoten")

    def __init__(self, nr, teil, label, eingang, typ, wpos, knoten):
        self.nr, self.teil, self.label, self.eingang, self.typ, self.welt, self.knoten = nr, teil, label, eingang, typ, wpos, knoten

    def __repr__(self):
        return "<%s '%s' %s %s>" % ("Eingang" if self.eingang else "Ausgang", self.label, SIGNAL.get(self.typ), self.welt)


class Kabel:
    __slots__ = ("typ", "a", "b", "quelle", "ziel", "grund")

    def __init__(self, typ, a, b):
        self.typ, self.a, self.b, self.quelle, self.ziel, self.grund = typ, a, b, None, None, None


class FahrzeugDaten:
    """Gelesene Fahrzeugdatei (wird je Datei und Aenderungszeit nur einmal gelesen)."""
    _cache = {}

    @classmethod
    def lesen(cls, pfad):
        pfad = finde_fahrzeug(pfad)
        st = os.stat(pfad)
        key = (os.path.abspath(pfad), st.st_mtime_ns, st.st_size)
        if key not in cls._cache:
            cls._cache[key] = cls(pfad)
        return cls._cache[key]

    def __init__(self, pfad):
        self.pfad = pfad
        with open(pfad, encoding="utf-8", newline="") as f:
            s = f.read()
        mcs = []

        def ersatz(m):
            mcs.append(m.group(0))
            return "<MC%d/>" % (len(mcs) - 1)
        s2 = re.sub(r"<microprocessor_definition.*?</microprocessor_definition>", ersatz, s, flags=re.S)
        self.teile, self.anschluesse, self.unbekannt = [], [], set()
        for m in re.finditer(r'<c d="([^"]+)"(?: t="(\d+)")?><o ([^>]*)>((?:(?!</c>).)*?)<vp([^/]*)/>', s2, re.S):
            d, t, o, mitte, vp = m.groups()
            rr = re.search(r'(?:^|\s)r="([^"]*)"', o)
            r = tuple(int(float(q)) for q in rr.group(1).split(",")) if rr else R_OHNE
            name = re.search(r'(?:^|\s)custom_name="([^"]*)"', o)
            teil = Teil(len(self.teile), d, xyz(vp), r, int(t or 0), name.group(1) if name else "", None)
            if d == "microprocessor":
                k = re.search(r"<MC(\d+)/>", mitte)
                if k:
                    teil.chipdef = chipdef(mcs[int(k.group(1))])
                    teil.name = teil.chipdef.name
                    for kn in teil.chipdef.knoten:
                        self._neu(teil, kn.label, kn.eingang, kn.typ, (kn.x, 0, kn.z), kn.nr)
            else:
                anschl = def_anschluesse(d)
                if anschl is None:
                    self.unbekannt.add(d)
                for label, ein, typ, p in anschl or ():
                    self._neu(teil, label, ein, typ, p, None)
            self.teile.append(teil)
        self.kabel = []
        a, e = s.find("<logic_node_links>"), s.find("</logic_node_links>")
        if a >= 0:
            for t, p0, p1 in re.findall(r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0([^/]*)/><voxel_pos_1([^/]*)/>'
                                        r"</logic_node_link>", s[a:e]):
                self.kabel.append(Kabel(int(t or 0), xyz(p0), xyz(p1)))
        self._verbinden()

    def _neu(self, teil, label, ein, typ, p, knoten):
        self.anschluesse.append(Anschluss(len(self.anschluesse), teil.nr, label, ein, typ, welt(teil.vp, teil.r, teil.t, p), knoten))

    def _verbinden(self):
        ort = {}
        for an in self.anschluesse:
            ort.setdefault((an.welt, an.typ), []).append(an)
        self.quelle = {}            # Eingang-Nr -> Ausgang-Nr (nur Signal-Arten in LOGIK)
        self.verworfen, self.mehrdeutig, self.doppelt = [], [], []
        for k in self.kabel:
            frei = k.typ in (4, 8)
            qa = [an for an in ort.get((k.a, k.typ), []) if frei or not an.eingang]
            qb = [an for an in ort.get((k.b, k.typ), []) if frei or an.eingang]
            if not qa or not qb:
                k.grund = "kein %s bei %s" % ("Ausgang" if not qa else "Eingang", k.a if not qa else k.b)
                self.verworfen.append(k)
                continue
            if len(qa) > 1 or len(qb) > 1:
                self.mehrdeutig.append(k)
            k.quelle, k.ziel = qa[0].nr, qb[0].nr
            if k.typ in LOGIK:
                if k.ziel in self.quelle:
                    self.doppelt.append(k)
                    continue
                self.quelle[k.ziel] = k.quelle
        self.ziele = {}
        for z, q in self.quelle.items():
            self.ziele.setdefault(q, []).append(z)

    # ---- Abfragen --------------------------------------------------------------------------------------------------

    def chips(self):
        return [t for t in self.teile if t.chipdef is not None]

    def nach_art(self):
        """{Art d: [Teile]} (einmal gebaut, fuer schnelles Suchen)."""
        if not hasattr(self, "_nach_art"):
            self._nach_art = {}
            for t in self.teile:
                self._nach_art.setdefault(t.d, []).append(t)
        return self._nach_art

    def anschluesse_von(self, teil_nr):
        """Alle Anschluesse eines Teils."""
        if not hasattr(self, "_je_teil"):
            self._je_teil = {}
            for a in self.anschluesse:
                self._je_teil.setdefault(a.teil, []).append(a)
        return self._je_teil.get(teil_nr, [])

    def beschreibe(self, an_nr):
        an = self.anschluesse[an_nr]
        t = self.teile[an.teil]
        return "%s%s %s '%s'" % (t.d if t.chipdef is None else "Chip", " '%s'" % t.name if t.name else "", t.vp, an.label)

    def kabel_text(self, k):
        return "%s-Kabel %s -> %s: %s" % (SIGNAL.get(k.typ, k.typ), k.a, k.b, k.grund or "")


def finde_fahrzeug(name):
    """Pfad oder Name ('Figet Marena') -> Pfad der Fahrzeugdatei."""
    if os.path.exists(name):
        return name
    p = os.path.join(FAHRZEUGE, name if name.lower().endswith(".xml") else name + ".xml")
    if os.path.exists(p):
        return p
    raise SimFehler("Fahrzeug '%s' nicht gefunden (weder als Pfad noch in %s)" % (name, FAHRZEUGE))


# ---- laufendes Fahrzeug ----------------------------------------------------------------------------------------------

class TeilGriff:
    """Zugriff auf ein Teil im laufenden Fahrzeug: Fuehler-Ausgang setzen, Stellglied-Eingang lesen."""

    def __init__(self, fz, teil):
        self.fz, self.teil = fz, teil

    def anschluss(self, label):
        alle = self.fz.daten.anschluesse_von(self.teil.nr)
        treffer = [a for a in alle if a.label == label]
        if len(treffer) != 1:
            alle = [a.label for a in alle]
            raise SimFehler("%r: Anschluss '%s' %s (vorhanden: %s)" % (self.teil, label, "fehlt" if not treffer else "mehrfach", alle))
        return treffer[0]

    def setze(self, label, wert):
        """Ausgang dieses Teils setzen (Fuehler oder nicht simulierter Chip). Bleibt, bis er neu gesetzt wird."""
        an = self.anschluss(label)
        if an.eingang:
            raise SimFehler("%r: '%s' ist ein Eingang, setzen geht nur bei Ausgaengen" % (self.teil, label))
        if self.teil.nr in self.fz.laufend:
            raise SimFehler("%r laeuft im Simulator, seine Ausgaenge rechnet er selbst" % (self.teil,))
        v = als_signal(an.typ, wert, self.fz.f32)
        self.fz.wert[an.nr] = v
        self.fz.gesetzt[an.nr] = v

    def lese(self, label):
        """Eingang: was ueber das Kabel ankommt; Ausgang: aktueller Wert."""
        an = self.anschluss(label)
        return self.fz.am_eingang(an.nr) if an.eingang else self.fz.wert.get(an.nr, leer(an.typ))

    def zeichne(self, label, breite=96, hoehe=96):
        """Video-Eingang (z. B. Monitor): onDraw aller Lua-Skripte, deren Bild hier ankommt."""
        return zeichne(self.lese(label), breite, hoehe)

    def texte(self, label, breite=96, hoehe=96):
        return texte(self.lese(label), breite, hoehe)


class Fahrzeug:
    """Laufendes Fahrzeug. chips = Liste von Chip-Namen (None = alle Chips)."""

    def __init__(self, daten, chips=None, takt="spiel", bruecken_takt=False, float32=True, lua_halten=True,
                 http_antwort=None):
        self.daten = daten if isinstance(daten, FahrzeugDaten) else FahrzeugDaten.lesen(daten)
        self.takt, self.f32 = takt, (f32 if float32 else _gleich)
        self.http, self.http_log, self.antworten, self.http_antwort = [], [], [], http_antwort
        alle = self.daten.chips()
        if chips is None:
            gewaehlt = alle
        else:
            namen = [t.name for t in alle]
            for n in chips:
                if n not in namen:
                    raise SimFehler("Chip '%s' ist nicht im Fahrzeug (vorhanden: %s)" % (n, ", ".join(sorted(set(namen)))))
            gewaehlt = [t for t in alle if t.name in chips]
        self.laufend = {}             # Teil-Nr -> Chip
        self.chip_ein, self.chip_aus = {}, {}
        for t in gewaehlt:
            ch = Chip(t.chipdef, takt=takt, bruecken_takt=bruecken_takt, float32=float32, lua_halten=lua_halten,
                      http=self.http, name=t.name)
            self.laufend[t.nr] = ch
            ans = self.daten.anschluesse_von(t.nr)
            self.chip_ein[t.nr] = [(a.knoten, a.nr) for a in ans if a.eingang and a.typ in LOGIK]
            self.chip_aus[t.nr] = [(a.knoten, a.nr) for a in ans if not a.eingang and a.typ in LOGIK]
        self.reihe = self._reihenfolge()
        self.wert = {a.nr: leer(a.typ) for a in self.daten.anschluesse if not a.eingang and a.typ in LOGIK}
        self.gesetzt = {}             # vom Szenario gesetzte Fuehler-Ausgaenge
        self.tick_nr = 0

    def _reihenfolge(self):
        if self.takt != "sofort":
            return list(self.laufend)
        an = self.daten.anschluesse
        vor = {t: set() for t in self.laufend}
        for t in self.laufend:
            for _, e in self.chip_ein[t]:
                q = self.daten.quelle.get(e)
                if q is not None and an[q].teil in self.laufend and an[q].teil != t:
                    vor[t].add(an[q].teil)
        out, besucht = [], set()

        def besuche(t):
            besucht.add(t)
            for v in vor[t]:
                if v not in besucht:
                    besuche(v)
            out.append(t)
        for t in self.laufend:
            if t not in besucht:
                besuche(t)
        return out

    # ---- Zugriff ---------------------------------------------------------------------------------------------------

    def teil(self, d=None, pos=None, name=None):
        """Ein Teil eindeutig finden: Art d, Position pos (Bezugsblock vp), Name (custom_name oder Chip-Name)."""
        idx = self.daten.nach_art()
        kand = idx.get(d, []) if d is not None else self.daten.teile
        treffer = [t for t in kand if (pos is None or t.vp == tuple(pos)) and (name is None or t.name == name)]
        if len(treffer) != 1:
            raise SimFehler("Teil d=%r pos=%r name=%r %s%s" % (d, pos, name, "nicht gefunden" if not treffer else
                            "%d-mal gefunden: " % len(treffer), ", ".join(map(repr, treffer[:8]))))
        return TeilGriff(self, treffer[0])

    def chip(self, name):
        """Laufender Chip nach Namen."""
        for nr, ch in self.laufend.items():
            if ch.name == name:
                return ch
        raise SimFehler("Chip '%s' laeuft nicht (laufend: %s)" % (name, ", ".join(c.name for c in self.laufend.values())))

    def am_eingang(self, an_nr):
        q = self.daten.quelle.get(an_nr)
        if q is None:
            return leer(self.daten.anschluesse[an_nr].typ)
        return self.wert.get(q, leer(self.daten.anschluesse[q].typ))

    # ---- Takt ------------------------------------------------------------------------------------------------------

    def tick(self, n=1, szenario=None):
        """n Ticks. szenario(fz, tick) wird vor jedem Tick gerufen und setzt die Fuehler."""
        for _ in range(n):
            if szenario is not None:
                szenario(self, self.tick_nr)
            self.ein_tick()
        return self

    def ein_tick(self, fremd=None):
        """Ein Tick. fremd = Fahrzeug des Hosts: dessen Chip-Eingaenge ersetzen die eigenen (Mehrspieler-Abgleich)."""
        for blk, port, anfrage, antwort in self.antworten:
            blk.antwort(port, anfrage, antwort)
        self.antworten = []
        sofort = self.takt == "sofort"
        spaeter = []
        for t in self.reihe:
            ch = self.laufend[t]
            if fremd is not None and t in fremd.laufend:
                fw = fremd.laufend[t].werte
                for kn, e in self.chip_ein[t]:
                    ch.werte[kn] = fw[kn] if self.daten.anschluesse[e].typ != 6 else self.am_eingang(e)
            else:
                for kn, e in self.chip_ein[t]:
                    ch.werte[kn] = self.am_eingang(e)
            ch.tick()
            if sofort:
                for kn, a in self.chip_aus[t]:
                    self.wert[a] = ch.werte[kn]
            else:
                spaeter.append(t)
        for t in spaeter:
            ch = self.laufend[t]
            for kn, a in self.chip_aus[t]:
                self.wert[a] = ch.werte[kn]
        if self.http:                                   # hoechstens eine Anfrage je Tick fuer das ganze Fahrzeug [G]
            blk, port, anfrage = self.http.pop(0)
            antwort = self.http_antwort(port, anfrage) if self.http_antwort else None
            self.http_log.append((self.tick_nr, blk.ort, port, anfrage, antwort))
            if antwort is not None:
                self.antworten.append((blk, port, anfrage, antwort))
        self.tick_nr += 1

    # ---- Berichte --------------------------------------------------------------------------------------------------

    def verbindungen(self, name):
        """Was haengt an jedem Anschluss dieses Chips? Liste von Textzeilen."""
        d = self.daten
        teil = [t for t in d.teile if t.name == name and t.chipdef is not None]
        if len(teil) != 1:
            raise SimFehler("Chip '%s' %s im Fahrzeug" % (name, "nicht" if not teil else "mehrfach"))
        out = []
        for an in d.anschluesse_von(teil[0].nr):
            if an.eingang:
                q = d.quelle.get(an.nr)
                ziel = [d.beschreibe(q)] if q is not None else []
            else:
                ziel = [d.beschreibe(z) for z in d.ziele.get(an.nr, [])]
            out.append("%-8s %-22s %-10s %s" % ("Eingang" if an.eingang else "Ausgang", an.label, SIGNAL.get(an.typ),
                                                  "; ".join(ziel) if ziel else "(kein Kabel)"))
        return out

    def fuehler(self):
        """Ausgaenge nicht simulierter Teile, die an einem laufenden Chip ankommen: (Teil, Anschluss) - die setzt das Szenario."""
        d, out = self.daten, []
        for t in self.laufend:
            for _, e in self.chip_ein[t]:
                q = d.quelle.get(e)
                if q is not None and d.anschluesse[q].teil not in self.laufend:
                    out.append(d.beschreibe(q))
        return sorted(set(out))

    def stellglieder(self):
        """Eingaenge nicht simulierter Teile, die von einem laufenden Chip kommen."""
        d, out = self.daten, []
        for t in self.laufend:
            for _, a in self.chip_aus[t]:
                for z in d.ziele.get(a, []):
                    if d.anschluesse[z].teil not in self.laufend:
                        out.append(d.beschreibe(z))
        return sorted(set(out))

    def bericht(self):
        d = self.daten
        z = ["Fahrzeug %s: %d Teile, %d Anschluesse, %d Kabel, %d Chips (%d laufen im Simulator)" % (
            os.path.basename(d.pfad), len(d.teile), len(d.anschluesse), len(d.kabel), len(d.chips()), len(self.laufend))]
        if d.unbekannt:
            z.append("Bauteile ohne Definition (keine Anschluesse): %s" % ", ".join(sorted(d.unbekannt)))
        z.append("Kabel, die das Spiel verwirft (zeigen auf keinen passenden Anschluss): %d" % len(d.verworfen))
        z += ["   " + d.kabel_text(k) for k in d.verworfen]
        if d.mehrdeutig:
            z.append("Kabel mit mehreren passenden Anschluessen am selben Ort (erster genommen): %d" % len(d.mehrdeutig))
        if d.doppelt:
            z.append("Eingaenge mit mehr als einem Kabel (erstes genommen): %d" % len(d.doppelt))
            z += ["   " + d.kabel_text(k) for k in d.doppelt]
        for ch in self.laufend.values():
            for f in ch.fehler():
                z.append("FEHLER " + f)
            for h in ch.hinweise():
                z.append("Hinweis " + h)
            if ch.vermutet:
                z.append("Chip '%s' nutzt Bausteine mit vermutetem Verhalten: %s" % (ch.name, ", ".join(ch.vermutet)))
        return z
