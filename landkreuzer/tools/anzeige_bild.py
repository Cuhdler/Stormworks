"""Vorschau der beiden KI-Monitore (Karte 3x3 und KI-Status 2x3) als Bild: laesst den KI-Chip (chip_sim) eine kurze
Fahrt mit zwei Karten-Tipps rechnen und zeichnet dann onDraw von ki_karte und ki_status in einen nachgebauten
Bildschirm (Schrift 4 x 5 Pixel wie im Spiel, Karte nur als einfarbige Flaeche).
Zum Pruefen, dass nichts uebereinander steht - und damit Andre vorher sieht, was die Monitore zeigen.

Aufruf (mit lupa und pillow): python landkreuzer/tools/anzeige_bild.py  -> landkreuzer/bilder/anzeigen.png
"""
import math
import os
import sys

from PIL import Image, ImageDraw

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import build_ki  # noqa: E402
from chip_sim import ChipSim  # noqa: E402

# 3 x 5-Schrift (Stormworks: 4 x 5, Abstand 5 Pixel je Zeichen) - X = Pixel an
FONT = {
    "A": ".X.|X.X|XXX|X.X|X.X", "B": "XX.|X.X|XX.|X.X|XX.", "C": ".XX|X..|X..|X..|.XX", "D": "XX.|X.X|X.X|X.X|XX.",
    "E": "XXX|X..|XX.|X..|XXX", "F": "XXX|X..|XX.|X..|X..", "G": ".XX|X..|X.X|X.X|.XX", "H": "X.X|X.X|XXX|X.X|X.X",
    "I": "XXX|.X.|.X.|.X.|XXX", "J": "..X|..X|..X|X.X|.X.", "K": "X.X|X.X|XX.|X.X|X.X", "L": "X..|X..|X..|X..|XXX",
    "M": "X.X|XXX|XXX|X.X|X.X", "N": "X.X|XXX|XXX|XXX|X.X", "O": ".X.|X.X|X.X|X.X|.X.", "P": "XX.|X.X|XX.|X..|X..",
    "Q": ".X.|X.X|X.X|XX.|.XX", "R": "XX.|X.X|XX.|X.X|X.X", "S": ".XX|X..|.X.|..X|XX.", "T": "XXX|.X.|.X.|.X.|.X.",
    "U": "X.X|X.X|X.X|X.X|XXX", "V": "X.X|X.X|X.X|X.X|.X.", "W": "X.X|X.X|X.X|XXX|X.X", "X": "X.X|X.X|.X.|X.X|X.X",
    "Y": "X.X|X.X|.X.|.X.|.X.", "Z": "XXX|..X|.X.|X..|XXX",
    "0": "XXX|X.X|X.X|X.X|XXX", "1": ".X.|XX.|.X.|.X.|XXX", "2": "XX.|..X|.X.|X..|XXX", "3": "XX.|..X|.X.|..X|XX.",
    "4": "X.X|X.X|XXX|..X|..X", "5": "XXX|X..|XX.|..X|XX.", "6": ".XX|X..|XXX|X.X|XXX", "7": "XXX|..X|.X.|.X.|.X.",
    "8": "XXX|X.X|XXX|X.X|XXX", "9": "XXX|X.X|XXX|..X|XX.",
    " ": "...|...|...|...|...", "-": "...|...|XXX|...|...", "+": "...|.X.|XXX|.X.|...", "/": "..X|..X|.X.|X..|X..",
    "%": "X.X|..X|.X.|X..|X.X", "?": "XX.|..X|.X.|...|.X.", ".": "...|...|...|...|.X.", ":": "...|.X.|...|.X.|...",
    ">": "X..|.X.|..X|.X.|X..", "<": "..X|.X.|X..|.X.|..X", ",": "...|...|...|.X.|X..", "(": ".X.|X..|X..|X..|.X.",
    ")": ".X.|..X|..X|..X|.X.", "!": ".X.|.X.|.X.|...|.X.", "_": "...|...|...|...|XXX", "=": "...|XXX|...|XXX|...",
}


class Schirm:
    """Nachbau von screen.* fuer ein Skript: zeichnet in ein PIL-Bild (w x h Pixel)."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.bild = Image.new("RGB", (w, h), (0, 0, 0))
        self.d = ImageDraw.Draw(self.bild, "RGBA")
        self.farbe = (255, 255, 255, 255)

    def setColor(self, r, g, b, a=255):
        self.farbe = (int(r), int(g), int(b), int(a))

    def drawClear(self):
        self.d.rectangle([0, 0, self.w, self.h], fill=self.farbe[:3] + (255,))

    def drawRectF(self, x, y, w, h):
        if w > 0 and h > 0:
            self.d.rectangle([x, y, x + w - 1, y + h - 1], fill=self.farbe)

    def drawRect(self, x, y, w, h):
        self.d.rectangle([x, y, x + w, y + h], outline=self.farbe)

    def drawLine(self, a, b, c, d):
        self.d.line([a, b, c, d], fill=self.farbe)

    def drawCircle(self, x, y, r):
        self.d.ellipse([x - r, y - r, x + r, y + r], outline=self.farbe)

    def drawCircleF(self, x, y, r):
        self.d.ellipse([x - r, y - r, x + r, y + r], fill=self.farbe)

    def drawTriangleF(self, a, b, c, d, e, f):
        self.d.polygon([(a, b), (c, d), (e, f)], fill=self.farbe)

    def drawTriangle(self, a, b, c, d, e, f):
        self.d.polygon([(a, b), (c, d), (e, f)], outline=self.farbe)

    def drawText(self, x, y, text):
        cx = x
        for ch in str(text).upper():
            g = FONT.get(ch, FONT["?"])
            for j, zeile in enumerate(g.split("|")):
                for i, c in enumerate(zeile):
                    if c == "X":
                        self.d.point((cx + i, y + j), fill=self.farbe)
            cx += 5

    def drawTextBox(self, x, y, w, h, text, ha=-1, va=-1):
        t = str(text)
        tw, th = len(t) * 5 - 1, 5
        px = x if ha < 0 else x + w - tw if ha > 0 else x + (w - tw) / 2
        py = y if va < 0 else y + h - th if va > 0 else y + (h - th) / 2
        self.drawText(int(px), int(py), t)

    def drawMap(self, x, z, zoom):
        self.d.rectangle([0, 0, self.w, self.h], fill=(96, 120, 70))
        # grobes Gitter alle 100 m (wie die Karte im Spiel ungefaehr)
        k = zoom * 1000 / self.w
        for g in range(-50, 51):
            sx = self.w / 2 + (g * 100 - x % 100) / k
            sy = self.h / 2 + (g * 100 - z % 100) / k
            self.d.line([sx, 0, sx, self.h], fill=(110, 135, 82))
            self.d.line([0, sy, self.w, sy], fill=(110, 135, 82))

    def getWidth(self):
        return self.w

    def getHeight(self):
        return self.h


def binde(g, schirm):
    for name in ("setColor", "drawClear", "drawRectF", "drawRect", "drawLine", "drawCircle", "drawCircleF",
                 "drawTriangleF", "drawTriangle", "drawText", "drawTextBox", "drawMap", "getWidth", "getHeight"):
        setattr(g.screen, name, getattr(schirm, name))


def fahrt(sek=40):
    """Kurze Fahrt: Panzer auf freiem Land, nach 12 s zwei Tipps auf die Karte. -> ChipSim nach der Fahrt"""
    sim = ChipSim(build_ki.build(eigen=build_ki.props_mit(**{"Start Verzoegerung s": 10})))
    x, z, hd, v, rl, rr = 1200.0, -800.0, 0.0, 0.0, 0.0, 0.0
    tipps = {720: (78, 22), 780: (30, 30)}
    for t in range(int(sek * 60)):
        L, R = rl, -rr
        v += ((L + R) / 2 * 10 - v) * 0.02
        hd += (L - R) * 0.02 / 60
        x += v * math.sin(hd * 2 * math.pi) / 60
        z += v * math.cos(hd * 2 * math.pi) / 60
        phys = ({1: x, 2: 50.0, 3: z, 9: v, 13: abs(v), 15: 0.01, 16: -0.006, 17: -hd}, {})
        laser = {n: 4000.0 for n in build_ki.LASER_NAMEN}
        laser["Laser unten"] = 1.6
        laser["Laser vorn rechts"] = 31.0
        tn, tb = {1: 96.0, 2: 96.0}, {}
        for t0, (px, py) in tipps.items():
            if t0 <= t < t0 + 3:
                tn.update({3: float(px), 4: float(py)})
                tb[1] = True
        e = {"Physik-Sensor": phys, "Sitz": ({}, {}), "Instrumente": ({}, {}), "Bedienung": ({}, {}),
             "Karte Touch": (tn, tb), "Batterie": 0.83}
        e.update(laser)
        a = sim.tick(e)
        rl, rr = a.get("Links") or 0.0, a.get("Rechts") or 0.0
    return sim


def main():
    sim = fahrt()
    bilder = []
    for name, (w, h) in (("ki_karte", (96, 96)), ("ki_status", (64, 96)), ("ki_status", (288, 160))):
        quelle = build_ki.lua(name)
        cid = next(c for c, (typ, *_r) in sim.comps.items() if typ == 56 and _r[3]["script"] == quelle)
        g, _ = sim.lua[cid]
        s = Schirm(w, h)
        binde(g, s)
        g.onDraw()
        bilder.append((name, s.bild))
    k = 4
    rand = 12
    breite = sum(b.width * k for _, b in bilder[:2]) + rand * 3
    hoehe = max(b.height * k for _, b in bilder[:2]) + 24 + rand * 4 + 30
    out = Image.new("RGB", (max(breite, bilder[2][1].width * 2 + 2 * rand), hoehe), (40, 40, 40))
    d = ImageDraw.Draw(out)
    xo = rand
    for (name, b), titel in zip(bilder[:2], ("Karte (Monitor 3x3, links)", "KI-Status (Monitor 2x3, rechts)")):
        out.paste(b.resize((b.width * k, b.height * k), Image.NEAREST), (xo, rand + 14))
        d.text((xo, 2), titel, fill=(230, 230, 230))
        xo += b.width * k + rand
    b = bilder[2][1]
    y = rand * 2 + 14 + 96 * k + 14
    d.text((rand, y - 14), "Helm (Zeile unten, Ausschnitt)", fill=(230, 230, 230))
    unten = b.crop((0, b.height - 12, b.width, b.height))
    out.paste(unten.resize((unten.width * 2, unten.height * 2), Image.NEAREST), (rand, y))
    pfad = os.path.join(os.path.dirname(HIER), "bilder", "anzeigen.png")
    out.save(pfad)
    print("gezeichnet:", pfad)


if __name__ == "__main__":
    main()
