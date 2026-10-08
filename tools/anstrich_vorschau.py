"""Vorschau des Anstrichs als PNG (Seitenansicht Steuerbord, Backbord, Draufsicht, von vorn) aus einer Fahrzeugdatei.
Aufruf: python anstrich_vorschau.py <fahrzeug.xml> <ausgabe.png>
"""
import math
import re
import struct
import sys
import zlib

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import umbau_v1 as u  # noqa: E402
from anstrich import wasserlinie  # noqa: E402

GRUND = (230, 236, 240)
UNGESTRICHEN = (178, 178, 178)
BAUTEIL = (120, 120, 120)


def png(pfad, w, h, px):
    roh = b"".join(b"\x00" + bytes(c for p in px[y * w:(y + 1) * w] for c in p) for y in range(h))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    with open(pfad, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(roh, 9)) + chunk(b"IEND", b""))


def main():
    s = open(sys.argv[1], encoding="utf-8").read()
    s = re.sub(r"<microprocessor_definition.*?</microprocessor_definition>", "", s, flags=re.S)
    teile = {}
    for m in re.finditer(r'<c(?: d="([^"]+)")?(?: t="\d+")?><o ([^>]*?)(/?)>((?:<vp[^/]*/>)?)', s):
        vp = u.xyz(m.group(4)[3:-2]) if m.group(4) else (0, 0, 0)
        sc = re.search(r'sc="\d+,([0-9A-F]{6})', m.group(2))
        if sc:
            c = sc.group(1)
            farbe = tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
        else:
            farbe = UNGESTRICHEN if (m.group(1) or "block")[:2] in ("bl", "01", "02", "03", "04", "05", "06", "07", "08",
                                                                    "09", "10", "11", "12", "13", "14", "15", "16") \
                else BAUTEIL
        teile[vp] = farbe
    S = 3
    ansichten = []
    # (Titel, Achse der Blickrichtung, Richtung, Bild-x-Achse (Index, Vorzeichen), Bild-y-Achse)
    for titel, ax, rz, bx, by in (("Steuerbord", 0, 1, (2, 1), (1, -1)), ("Backbord", 0, -1, (2, -1), (1, -1)),
                                  ("Draufsicht", 1, 1, (2, 1), (0, 1)), ("von vorn", 2, 1, (0, -1), (1, -1))):
        best = {}
        for p, f in teile.items():
            k = (p[bx[0]], p[by[0]])
            if k not in best or (p[ax] - best[k][0]) * rz > 0:
                best[k] = (p[ax], f)
        xs = [k[0] for k in best]
        ys = [k[1] for k in best]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        w, h = (x1 - x0 + 1), (y1 - y0 + 1)
        bild = [GRUND] * (w * h)
        for (a, b), (_, f) in best.items():
            ix = (a - x0) if bx[1] > 0 else (x1 - a)
            iy = (b - y0) if by[1] > 0 else (y1 - b)
            bild[iy * w + ix] = f
        if ax == 0:           # Wasserlinie einzeichnen
            for a in range(x0, x1 + 1):
                b = int(round(wasserlinie(a)))
                if y0 <= b <= y1:
                    ix = (a - x0) if bx[1] > 0 else (x1 - a)
                    iy = y1 - b
                    if bild[iy * w + ix] == GRUND:
                        bild[iy * w + ix] = (60, 120, 200)
        ansichten.append((titel, w, h, bild))
    W = max(a[1] for a in ansichten) * S + 20
    H = sum(a[2] * S + 20 for a in ansichten) + 10
    px = [(255, 255, 255)] * (W * H)
    oy = 10
    for titel, w, h, bild in ansichten:
        for y in range(h * S):
            for x in range(w * S):
                px[(oy + y) * W + 10 + x] = bild[(y // S) * w + x // S]
        oy += h * S + 20
    png(sys.argv[2], W, H, px)
    print("geschrieben:", sys.argv[2], W, "x", H)


if __name__ == "__main__":
    main()
