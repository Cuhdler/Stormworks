"""Fahrzeug-Dateien lesen und schreiben (Stormworks), fuer den Bau des KI-Landkreuzers.

Lesen: die Figet Marena vom 05.10. (landkreuzer/fahrzeug/Schiff Teilelager.xml) dient als Teile-Lager - jedes Teil, das der Landkreuzer benutzt,
kommt als genaue Text-Kopie von dort (Art, Drehung, Farben, Einstellungen), nur an eine neue Stelle verschoben.

Begriffe (wie im SCHIFFSDATEI_TUTORIAL.md):
- Position vp in Bloecken (0,25 m); x rechts, y oben, z vorn
- r Drehung (9 Zahlen; fehlt sie, gilt 0,0,1,-1,0,0,0,-1,0), t Spiegelung (Bit 1 x, 2 y, 4 z; lokal vor der Drehung)
- Kabel: (Typ, Ausgang-Position, Eingang-Position); Typ 0 An/Aus, 1 Zahl, 4 Strom, 5 Composite, 6 Video, 8 Riemen
"""
import os
import re

HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HIER))
SCHIFF_PFAD = os.path.join(ROOT, "landkreuzer", "fahrzeug", "Schiff Teilelager.xml")

R_OHNE = "0,0,1,-1,0,0,0,-1,0"
STRUKTUR = {"block", "01_block_weight", "02_wedge", "03_pyramid", "04_invpyramid", "05_wedge_2", "06_pyramid_2",
            "07_invpyramid_2", "08_wedge_4", "09_pyramid_4", "10_invpyramid_4", "11_pyramid_2x2", "12_pyramid_2x4",
            "13_pyramid_4x4", "14_invpyramid_2x2", "15_invpyramid_2x4", "16_invpyramid_4x4"}


def xyz(attr):
    d = dict(re.findall(r'(\w)="(-?\d+)"', attr or ""))
    return tuple(int(d.get(k, 0)) for k in "xyz")


def vox(tag, p):
    return "<%s%s/>" % (tag, "".join(' %s="%d"' % (k, v) for k, v in zip("xyz", p) if v))


def add(a, b):
    return tuple(a[i] + b[i] for i in range(3))


def sub(a, b):
    return tuple(a[i] - b[i] for i in range(3))


class Teil:
    """Ein Bauteil als Text. xml beginnt mit <c ...><o ...> und endet mit </o></c>."""
    __slots__ = ("xml", "d", "t", "r", "vp")

    def __init__(self, xml):
        self.xml = xml
        m = re.match(r'<c(?: d="([^"]+)")?(?: t="(\d+)")?><o( [^>]*)?>', xml)
        assert m, xml[:80]
        self.d = m.group(1) or "block"
        self.t = int(m.group(2) or 0)
        rr = re.search(r'\br="([^"]*)"', m.group(3) or "")
        # ohne r-Attribut: im Spiel die Drehung 0,0,1,-1,0,0,0,-1,0, nicht die Grunddrehung (Befund 08.10., aus den Kabeln
        # aller Fahrzeuge bestimmt - SCHIFF_UEBERSICHT.md)
        self.r = tuple(int(float(v)) for v in (rr.group(1) if rr else R_OHNE).split(","))
        if self.d == "microprocessor":
            e = xml.index("</microprocessor_definition>")
            self.vp = xyz(re.match(r"<vp([^/]*)/>", xml[e + len("</microprocessor_definition>"):]).group(1))
        else:
            self.vp = xyz(re.search(r"<vp([^/]*)/>", xml).group(1))

    def verschoben(self, d):
        """Kopie um d verschoben."""
        neu = add(self.vp, d)
        if self.d == "microprocessor":
            e = self.xml.index("</microprocessor_definition>") + len("</microprocessor_definition>")
            m = re.match(r"<vp[^/]*/>", self.xml[e:])
            xml = self.xml[:e] + vox("vp", neu) + self.xml[e + m.end():]
        else:
            m = re.search(r"<vp[^/]*/>", self.xml)
            xml = self.xml[:m.start()] + vox("vp", neu) + self.xml[m.end():]
        return Teil(xml)

    def lokal_zu_welt(self, p):
        """Punkt im Teil (Definition) -> Welt (Spiegeln, Drehen, Verschieben)."""
        p = list(p)
        for i in range(3):
            if self.t >> i & 1:
                p[i] = -p[i]
        r = self.r
        return tuple(self.vp[i] + r[i] * p[0] + r[3 + i] * p[1] + r[6 + i] * p[2] for i in range(3))


def teile_zerlegen(txt):
    """<c ...>...</c><c ...>... (Inhalt von <components>) -> Liste Teil. Microcontroller enthalten selbst <c>."""
    out, i, n = [], 0, len(txt)
    while i < n:
        assert txt.startswith("<c", i), txt[i:i + 80]
        kopf = txt[i:txt.index(">", txt.index("<o", i)) + 1]
        if 'd="microprocessor"' in kopf:
            e = txt.index("</microprocessor_definition>", i)
            e = txt.index("</o></c>", e) + len("</o></c>")
        else:
            e = txt.index("</o></c>", i) + len("</o></c>")
        out.append(Teil(txt[i:e]))
        i = e
    return out


class Fahrzeug:
    def __init__(self, text):
        self.text = text
        self.kopf = text[:text.index("<bodies>")]
        self.koerper = []          # Liste (Kopf '<body ...>', [Teil])
        i, e = text.index("<bodies>") + len("<bodies>"), text.index("</bodies>")
        while i < e:
            m = re.match(r"(<body[^>]*>)<components>", text[i:])
            assert m, text[i:i + 100]
            a = i + m.end()
            # Ende dieses Koerpers: '</components></body>' nach dem letzten Teil - Microcontroller enthalten
            # '</components>', darum Teil fuer Teil weiterlesen
            j = a
            teile = []
            while not text.startswith("</components></body>", j):
                kopf = text[j:text.index(">", text.index("<o", j)) + 1]
                if 'd="microprocessor"' in kopf:
                    k = text.index("</o></c>", text.index("</microprocessor_definition>", j)) + len("</o></c>")
                else:
                    k = text.index("</o></c>", j) + len("</o></c>")
                teile.append(Teil(text[j:k]))
                j = k
            self.koerper.append((m.group(1), teile))
            i = j + len("</components></body>")
        li, le = text.index("<logic_node_links>"), text.index("</logic_node_links>")
        self.kabel = [(int(t or 0), xyz(a), xyz(b)) for t, a, b in re.findall(
            r'<logic_node_link(?: type="(\d+)")?><voxel_pos_0([^/]*)/><voxel_pos_1([^/]*)/></logic_node_link>',
            text[li:le])]
        self.fuss = text[le + len("</logic_node_links>"):]

    @classmethod
    def lesen(cls, pfad=SCHIFF_PFAD):
        return cls(open(pfad, encoding="utf-8", newline="").read())

    def chip_anschluesse(self):
        """Alle Microcontroller: {Name: [(Label, mode, typ, Weltposition)]} (Name doppelt -> Name#2 ...)."""
        out = {}
        for _, teile in self.koerper:
            for t in teile:
                if t.d != "microprocessor":
                    continue
                name = re.search(r'<microprocessor_definition name="([^"]*)"', t.xml).group(1)
                k, nm = 1, name
                while nm in out:
                    k += 1
                    nm = "%s#%d" % (name, k)
                out[nm] = chip_knoten(t)
        return out


def chip_knoten(t):
    """Anschluesse eines Microcontroller-Teils: [(Label, mode, typ, Weltposition)] in Reihenfolge."""
    i = t.xml.index("<nodes>")
    e = t.xml.index("</nodes>")
    out = []
    for m in re.finditer(r'<node label=("[^"]*"|\'[^\']*\')([^>]*?)(?:/>|><position([^/]*)/></node>)', t.xml[i:e]):
        lab = m.group(1)[1:-1]
        a = m.group(2)
        mode = int(re.search(r'mode="(\d+)"', a).group(1)) if 'mode="' in a else 0
        typ = int(re.search(r'type="(\d+)"', a).group(1)) if 'type="' in a else 0
        x, _, z = xyz(m.group(3))
        r = t.r
        welt = tuple(t.vp[k] + r[k] * x + r[6 + k] * z for k in range(3))
        out.append((lab, mode, typ, welt))
    return out


def kabel_xml(k):
    typ, a, b = k
    return "<logic_node_link%s>%s%s</logic_node_link>" % (' type="%d"' % typ if typ else "", vox("voxel_pos_0", a),
                                                          vox("voxel_pos_1", b))


def schreiben(kopf, koerper, kabel, fuss="</vehicle>"):
    """koerper: Liste (Kopf, [Teil]); kabel: Liste (typ, a, b)."""
    t = [kopf, "<bodies>"]
    for k, teile in koerper:
        t.append(k + "<components>" + "".join(x.xml for x in teile) + "</components></body>")
    t.append("</bodies><logic_node_links>")
    t.extend(kabel_xml(k) for k in kabel)
    t.append("</logic_node_links>")
    t.append(fuss)
    return "".join(t)
