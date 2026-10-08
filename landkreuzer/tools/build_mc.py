"""Microcontroller-Baukasten (Nachbau von build_mc.py aus stormworks_flugpanzer/tools, das im Repo fehlt).

Gleiche Schnittstelle wie das Original, so wie die Schiffs-Werkzeuge (tools/build_*.py) es benutzen:

    mc = MC(name, beschreibung, breite, laenge)
    n  = mc.node(label, mode, typ, beschreibung, x, z, editor_pos, quelle=None, late=False)
         mode 1 = Eingang, 0 = Ausgang; typ 0 An/Aus, 1 Zahl, 5 Composite, 6 Video; (x, z) Feld auf dem Chip;
         quelle (Komponente, Ausgang-Nummer) nur bei Ausgaengen; late=True haengt den Anschluss hinten an
    c  = mc.comp(typ, editor_pos, attrs, eingaenge, extra='')
         typ 29 Composite lesen An/Aus, 31 Composite lesen Zahl, 40 Composite schreiben Zahl, 41 ... An/Aus,
         34 Eigenschaft Zahl, 56 Lua, 57 Video-Umschalter; eingaenge = [(quelle, nr), ...] oder ('inc', (quelle, nr))
         fuer den Composite-Eingang eines Schreib-Bausteins
    mc.embedded()  -> <microprocessor_definition ...> so, wie das Spiel ihn im Fahrzeug speichert (alles in einer Zeile)
    mc.xml()       -> Datei fuer data/microprocessors (Form wie im Spiel-Ordner; ungetestet, nur fuer die Bibliothek)

minify(lua, drop_local=False): Kommentare, Einrueckung und Leerzeilen weg (genau wie das Original: das eingebaute
Schutz-Skript der Figet Marena kommt Zeichen fuer Zeichen gleich heraus, siehe test_build_mc.py).
"""
import re
from xml.sax.saxutils import escape

LUA_LIMIT = 8192

# Anschluss-Typ -> Bruecken-Typ (Eingang); Ausgang = +1
BRUECKE = {0: 0, 1: 2, 5: 4, 6: 6}


def fmt(v):
    """Zahl so schreiben wie das Spiel: 1.0 -> '1', 0.25 -> '0.25', -999 -> '-999'."""
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, int):
        return str(v)
    v = float(v)
    if v == int(v) and abs(v) < 1e15:
        return str(int(v))
    s = repr(v)
    if "e" in s:
        s = ("%.10f" % v).rstrip("0").rstrip(".")
    return s


def _attr(v):
    """Attribut-Wert mit Anfuehrungszeichen, wie das Spiel schreibt: enthaelt er ", dann in '...' mit &apos;."""
    v = escape(str(v))
    if '"' in v:
        return "'%s'" % v.replace("'", "&apos;")
    return '"%s"' % v


def _lua_strip_comments(src):
    """Kommentare entfernen, Zeichenketten unangetastet lassen."""
    out = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c == "-" and src.startswith("--", i):
            m = re.match(r"--\[(=*)\[", src[i:])
            if m:
                ende = "]" + m.group(1) + "]"
                j = src.find(ende, i + len(m.group(0)))
                i = n if j < 0 else j + len(ende)
                continue
            j = src.find("\n", i)
            i = n if j < 0 else j
            continue
        if c in "'\"":
            j = i + 1
            while j < n and src[j] != c:
                if src[j] == "\\":
                    j += 1
                j += 1
            out.append(src[i:j + 1])
            i = j + 1
            continue
        if c == "[":
            m = re.match(r"\[(=*)\[", src[i:])
            if m:
                ende = "]" + m.group(1) + "]"
                j = src.find(ende, i + len(m.group(0)))
                j = n if j < 0 else j + len(ende)
                out.append(src[i:j])
                i = j
                continue
        out.append(c)
        i += 1
    return "".join(out)


def minify(src, drop_local=False):
    s = _lua_strip_comments(src)
    zeilen = [z.strip() for z in s.split("\n")]
    s = "\n".join(z for z in zeilen if z)
    if drop_local:
        # 'local ' weg spart Zeichen (Variablen werden global - nur fuer Skripte, die das vertragen)
        s = re.sub(r"(?<![\w'])local function ", "function ", s)
        s = re.sub(r"(?<![\w'])local (?=[A-Za-z_])", "", s)
    return s


class MC:
    def __init__(self, name, desc, width, length):
        self.name, self.desc, self.width, self.length = name, desc, width, length
        self.ids = 0
        self.nodes = []      # [nid, label, mode, typ, desc, x, z, cid]
        self.late = []       # wie nodes, kommen hinten dran (Reihenfolge darf der Aufrufer sortieren)
        self.comps = []      # [typ, cid, pos, eingaenge, attrs, extra]
        self.bridges = []    # [btyp, cid, pos, eingaenge]

    def _id(self):
        self.ids += 1
        return self.ids

    def node(self, label, mode, typ, desc, x, z, pos, src=None, late=False):
        cid = self._id()
        btyp = BRUECKE[typ] + (0 if mode else 1)
        self.bridges.append([btyp, cid, pos, [src] if src is not None else []])
        eintrag = [None, label, mode, typ, desc, x, z, cid]
        (self.late if late else self.nodes).append(eintrag)
        return cid

    def comp(self, typ, pos, attrs=None, inputs=(), extra=""):
        cid = self._id()
        self.comps.append([typ, cid, pos, list(inputs), dict(attrs or {}), extra])
        return cid

    # ---------- Ausgabe ----------
    @staticmethod
    def _pos(tag, p):
        a = "".join(' %s="%s"' % (k, fmt(v)) for k, v in zip("xy", p) if v)
        return "<%s%s/>" % (tag, a)

    @staticmethod
    def _ins(inputs):
        out, k = [], 0
        for e in inputs:
            if e[0] == "inc":
                q, nr = e[1]
                tag = "inc"
            else:
                q, nr = e
                k += 1
                tag = "in%d" % k
            out.append('<%s component_id="%d"%s/>' % (tag, q, ' node_index="%d"' % nr if nr else ""))
        # inc steht immer vorn
        out.sort(key=lambda t: 0 if t.startswith("<inc") else 1)
        return "".join(out)

    def _alle_nodes(self):
        alle = self.nodes + self.late
        for k, e in enumerate(alle):
            e[0] = k + 1
        return alle

    def embedded(self):
        alle = self._alle_nodes()
        t = ['<microprocessor_definition name="%s" description="%s" width="%d" length="%d" id_counter="%d" '
             'id_counter_node="%d"><nodes>' % (_attr(self.name)[1:-1], _attr(self.desc)[1:-1], self.width, self.length, self.ids,
                                              len(alle))]
        for nid, label, mode, typ, desc, x, z, cid in alle:
            a = ' label=%s' % _attr(label)
            if mode:
                a += ' mode="%d"' % mode
            if typ:
                a += ' type="%d"' % typ
            a += ' description=%s' % _attr(desc)
            p = "".join(' %s="%s"' % (k, fmt(v)) for k, v in (("x", x), ("z", z)) if v)
            node = "<node%s><position%s/></node>" % (a, p) if p else "<node%s/>" % a
            t.append('<n id="%d" component_id="%d">%s</n>' % (nid, cid, node))
        t.append("</nodes><group><data><inputs/><outputs/></data><components>")
        for typ, cid, pos, inputs, attrs, extra in self.comps:
            # Werte 0 schreibt das Spiel nicht (z. B. offset 0, i 0)
            a = "".join(' %s=%s' % (k, _attr(fmt(v) if isinstance(v, (int, float)) else v)) for k, v in attrs.items()
                        if not (isinstance(v, (int, float)) and v == 0))
            # wie das Spiel: Eigenschaft 0 als <v text="0"/>
            ex = extra.replace('<v text="0" value="0"/>', '<v text="0"/>')
            t.append('<c%s><object id="%d"%s>%s%s%s</object></c>' % (
                ' type="%d"' % typ if typ else "", cid, a, self._pos("pos", pos), self._ins(inputs), ex))
        t.append("</components><components_bridge>")
        for btyp, cid, pos, inputs in self.bridges:
            t.append('<c%s><object id="%d">%s%s</object></c>' % (
                ' type="%d"' % btyp if btyp else "", cid, self._pos("pos", pos), self._ins(inputs)))
        t.append("</components_bridge><groups/></group></microprocessor_definition>")
        return "".join(t)

    def slots(self):
        return "<logic_slots>%s</logic_slots>" % ("<slot/>" * (len(self.nodes) + len(self.late)))

    def node_liste(self):
        """[(label, mode, typ, x, z)] in Anschluss-Reihenfolge."""
        return [(e[1], e[2], e[3], e[5], e[6]) for e in self._alle_nodes()]

    def xml(self):
        """Datei fuer die Bibliothek (data/microprocessors). Form nach umbau_v1.chip_eingebettet() rueckwaerts:
        dort werden component_states, mode/type 0 und Null-Positionen entfernt. Ungetestet im Spiel - fuer das Fahrzeug
        zaehlt nur embedded()."""
        e = self.embedded()
        e = e.replace("<microprocessor_definition ", "<microprocessor ", 1)
        e = e.replace("</microprocessor_definition>", "</microprocessor>")
        e = re.sub(r' id_counter="\d+" id_counter_node="\d+"', "", e, count=1)
        e = e.replace("<groups/></group>", "<groups/><component_states/><component_bridge_states/><group_states/></group>")
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + e + "\n"
